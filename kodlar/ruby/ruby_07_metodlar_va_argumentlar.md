# 301-Topshiriq: Metod e'lon qilish va argumentlar
## Topshiriq sharti:
Foydalanuvchini ismi bo'yicha qutlovchi sodda metod yozing.

## Yechim (Ruby kodi):
```ruby
def salom_ber(ism)
  "Assalomu alaykum, #{ism}!"
end

puts salom_ber("Akmal")
```

## Tushuntirish va Mantiq:
Ruby-da metod 'def' kalit so'zi bilan e'lon qilinadi va 'end' bilan tugallanadi. Argumentlar qavs ichida beriladi.

## Ishlash natijasi:
```text
Assalomu alaykum, Akmal!
```


# 302-Topshiriq: Sukut bo'yicha parametrlar (Default Arguments)
## Topshiriq sharti:
Agar foydalanuvchi tilni ko'rsatmasa, sukut bo'yicha o'zbek tilida salom bering.

## Yechim (Ruby kodi):
```ruby
def xush_kelibsiz(ism, til = "uz")
  case til
  when "uz" then "Xush kelibsiz, #{ism}!"
  when "en" then "Welcome, #{ism}!"
  end
end

puts xush_kelibsiz("Anvar")
puts xush_kelibsiz("John", "en")
```

## Tushuntirish va Mantiq:
Default parametrlar `param = qiymat` ko'rinishida beriladi. Agar chaqiruv paytida argument uzatilmasa, ushbu standart qiymat ishlatiladi.

## Ishlash natijasi:
```text
Xush kelibsiz, Anvar!
Welcome, John!
```


# 303-Topshiriq: Implicit Return (Yashirin qaytish qiymati)
## Topshiriq sharti:
Nega Ruby-da 'return' yozish shart emasligini tushuntiring.

## Yechim (Ruby kodi):
```ruby
def kvadrat(son)
  son * son # oxirgi ifoda avtomatik qaytariladi
end

puts "7 ning kvadrati: #{kvadrat(7)}"
```

## Tushuntirish va Mantiq:
Ruby-da metoddagi eng oxirgi bajarilgan ifodaning qiymati avtomatik qaytariladi (Implicit Return). Explicit 'return' faqat metoddan muddatidan oldin (erta) chiqish kerak bo'lganda yoziladi.

## Ishlash natijasi:
```text
7 ning kvadrati: 49
```


# 304-Topshiriq: Endless Methods (Ruby 3.0+ bir qatorli metodlar)
## Topshiriq sharti:
Bir qatorli ixcham metod e'lon qiling.

## Yechim (Ruby kodi):
```ruby
def kub(x) = x ** 3
def juftmi(x) = x.even?

puts "4 ning kubi: #{kub(4)}"
puts "6 juftmi? #{juftmi(6)}"
```

## Tushuntirish va Mantiq:
Ruby 3.0 da kiritilgan Endless Method sintaksisi `def nom(param) = ifoda` shaklida bo'lib, 'end' yozishni talab qilmaydi.

## Ishlash natijasi:
```text
4 ning kubi: 64
6 juftmi? true
```


# 305-Topshiriq: Keyword Arguments (Nomlangan argumentlar)
## Topshiriq sharti:
Buyurtma yaratishda adashmaslik uchun kalit so'zli argumentlardan foydalaning.

## Yechim (Ruby kodi):
```ruby
def buyurtma_yarat(mahsulot:, narx:, soni: 1)
  "Buyurtma: #{mahsulot} (#{soni} dona) -> Jami: $#{narx * soni}"
end

puts buyurtma_yarat(mahsulot: "Klaviatura", narx: 40)
puts buyurtma_yarat(soni: 2, narx: 15, mahsulot: "Sichqoncha")
```

## Tushuntirish va Mantiq:
Keyword arguments `nom:` ko'rinishida yoziladi. Ular tartibga bog'liq emas va kod o'qilishini ancha yaxshilaydi.

## Ishlash natijasi:
```text
Buyurtma: Klaviatura (1 dona) -> Jami: $40
Buyurtma: Sichqoncha (2 dona) -> Jami: $30
```


# 306-Topshiriq: Splat operatori argumentlarda: *args
## Topshiriq sharti:
Ixtiyoriy miqdordagi sonlarni qabul qilib, ularning o'rtacha qiymatini hisoblang.

## Yechim (Ruby kodi):
```ruby
def ortacha(*sonlar)
  return 0 if sonlar.empty?
  sonlar.sum.to_f / sonlar.size
end

puts "O'rtacha(10, 20, 30): #{ortacha(10, 20, 30)}"
puts "O'rtacha(5, 15): #{ortacha(5, 15)}"
```

## Tushuntirish va Mantiq:
Yulduzcha `*args` (splat) bir nechta argumentlarni massivga to'playdi.

## Ishlash natijasi:
```text
O'rtacha(10, 20, 30): 20.0
O'rtacha(5, 15): 10.0
```


# 307-Topshiriq: Double Splat operatori: **kwargs
## Topshiriq sharti:
Ixtiyoriy qo'shimcha parametrlarni Hash ko'rinishida qabul qiling.

## Yechim (Ruby kodi):
```ruby
def profil_yarat(ism, **qoshimcha)
  puts "Foydalanuvchi: #{ism}"
  puts "Qo'shimcha ma'lumotlar: #{qoshimcha.inspect}"
end

profil_yarat("Rustam", shahar: "Toshkent", tajriba: "5 yil", daraja: "Senior")
```

## Tushuntirish va Mantiq:
`**kwargs` (double splat) berilgan barcha nomlangan argumentlarni Hash sifatida jamlaydi.

## Ishlash natijasi:
```text
Foydalanuvchi: Rustam
Qo'shimcha ma'lumotlar: {:shahar=>"Toshkent", :tajriba=>"5 yil", :daraja=>"Senior"}
```


# 308-Topshiriq: Argument Forwarding: (...) sintaksisi (Ruby 2.7+ / 3.0+)
## Topshiriq sharti:
Barcha argumentlarni o'zgarishsiz boshqa metodga uzatuvchi wrapper yarating.

## Yechim (Ruby kodi):
```ruby
def log_wrapper(...)
  puts "[LOG] Metod chaqirildi..."
  haqiqiy_hisoblash(...)
end

def haqiqiy_hisoblash(a, b, amal: :+)
  a.send(amal, b)
end

puts "Natija: #{log_wrapper(10, 5, amal: :-)}"
```

## Tushuntirish va Mantiq:
`(...)` uch nuqta barcha pozitsion, keyword va blok argumentlarni to'liq qamrab olib boshqa metodga to'g'ridan-to'g'ri o'tkazadi.

## Ishlash natijasi:
```text
[LOG] Metod chaqirildi...
Natija: 5
```


# 309-Topshiriq: Operatorlarni qayta yuklash (Operator Overloading)
## Topshiriq sharti:
Vektor sinfida `+` operatorini qayta aniqlab, ikkita vektorni qo'shing.

## Yechim (Ruby kodi):
```ruby
class Vektor
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
```

## Tushuntirish va Mantiq:
Ruby-da deyarli barcha operatorlar (`+`, `-`, `*`, `[]`) aslida oddiy metodlardir va ularni istalgan sinfda qayta belgilash mumkin.

## Ishlash natijasi:
```text
v1 + v2 = (6, 8)
```


# 310-Topshiriq: Ko'rinish chegaralari: public, private va protected
## Topshiriq sharti:
Sinfning ichki yordamchi metodlarini private qilib yashiring.

## Yechim (Ruby kodi):
```ruby
class BankHisobi
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
```

## Tushuntirish va Mantiq:
'private' metodlar tashqaridan to'g'ridan-to'g'ri (nuqta orqali) chaqirilishi mumkin emas. Ular faqat sinfning o'z ichki metodlari tomonidan ishlatiladi.

## Ishlash natijasi:
```text
Muvaffaqiyatli: Qolgan balans: 80000
```


# 311-Topshiriq: Metodlar va argumentlar ilg'or namunasi #11
## Topshiriq sharti:
311-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_311(son, koeff = 2)
  son * koeff
end

puts "Natija: #{murakkab_amal_311(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 311-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 20
```


# 312-Topshiriq: Metodlar va argumentlar ilg'or namunasi #12
## Topshiriq sharti:
312-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_312(son, koeff = 3)
  son * koeff
end

puts "Natija: #{murakkab_amal_312(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 312-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 30
```


# 313-Topshiriq: Metodlar va argumentlar ilg'or namunasi #13
## Topshiriq sharti:
313-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_313(son, koeff = 4)
  son * koeff
end

puts "Natija: #{murakkab_amal_313(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 313-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 40
```


# 314-Topshiriq: Metodlar va argumentlar ilg'or namunasi #14
## Topshiriq sharti:
314-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_314(son, koeff = 5)
  son * koeff
end

puts "Natija: #{murakkab_amal_314(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 314-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 50
```


# 315-Topshiriq: Metodlar va argumentlar ilg'or namunasi #15
## Topshiriq sharti:
315-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_315(son, koeff = 1)
  son * koeff
end

puts "Natija: #{murakkab_amal_315(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 315-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 10
```


# 316-Topshiriq: Metodlar va argumentlar ilg'or namunasi #16
## Topshiriq sharti:
316-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_316(son, koeff = 2)
  son * koeff
end

puts "Natija: #{murakkab_amal_316(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 316-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 20
```


# 317-Topshiriq: Metodlar va argumentlar ilg'or namunasi #17
## Topshiriq sharti:
317-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_317(son, koeff = 3)
  son * koeff
end

puts "Natija: #{murakkab_amal_317(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 317-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 30
```


# 318-Topshiriq: Metodlar va argumentlar ilg'or namunasi #18
## Topshiriq sharti:
318-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_318(son, koeff = 4)
  son * koeff
end

puts "Natija: #{murakkab_amal_318(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 318-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 40
```


# 319-Topshiriq: Metodlar va argumentlar ilg'or namunasi #19
## Topshiriq sharti:
319-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_319(son, koeff = 5)
  son * koeff
end

puts "Natija: #{murakkab_amal_319(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 319-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 50
```


# 320-Topshiriq: Metodlar va argumentlar ilg'or namunasi #20
## Topshiriq sharti:
320-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_320(son, koeff = 1)
  son * koeff
end

puts "Natija: #{murakkab_amal_320(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 320-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 10
```


# 321-Topshiriq: Metodlar va argumentlar ilg'or namunasi #21
## Topshiriq sharti:
321-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_321(son, koeff = 2)
  son * koeff
end

puts "Natija: #{murakkab_amal_321(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 321-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 20
```


# 322-Topshiriq: Metodlar va argumentlar ilg'or namunasi #22
## Topshiriq sharti:
322-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_322(son, koeff = 3)
  son * koeff
end

puts "Natija: #{murakkab_amal_322(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 322-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 30
```


# 323-Topshiriq: Metodlar va argumentlar ilg'or namunasi #23
## Topshiriq sharti:
323-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_323(son, koeff = 4)
  son * koeff
end

puts "Natija: #{murakkab_amal_323(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 323-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 40
```


# 324-Topshiriq: Metodlar va argumentlar ilg'or namunasi #24
## Topshiriq sharti:
324-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_324(son, koeff = 5)
  son * koeff
end

puts "Natija: #{murakkab_amal_324(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 324-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 50
```


# 325-Topshiriq: Metodlar va argumentlar ilg'or namunasi #25
## Topshiriq sharti:
325-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_325(son, koeff = 1)
  son * koeff
end

puts "Natija: #{murakkab_amal_325(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 325-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 10
```


# 326-Topshiriq: Metodlar va argumentlar ilg'or namunasi #26
## Topshiriq sharti:
326-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_326(son, koeff = 2)
  son * koeff
end

puts "Natija: #{murakkab_amal_326(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 326-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 20
```


# 327-Topshiriq: Metodlar va argumentlar ilg'or namunasi #27
## Topshiriq sharti:
327-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_327(son, koeff = 3)
  son * koeff
end

puts "Natija: #{murakkab_amal_327(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 327-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 30
```


# 328-Topshiriq: Metodlar va argumentlar ilg'or namunasi #28
## Topshiriq sharti:
328-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_328(son, koeff = 4)
  son * koeff
end

puts "Natija: #{murakkab_amal_328(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 328-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 40
```


# 329-Topshiriq: Metodlar va argumentlar ilg'or namunasi #29
## Topshiriq sharti:
329-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_329(son, koeff = 5)
  son * koeff
end

puts "Natija: #{murakkab_amal_329(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 329-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 50
```


# 330-Topshiriq: Metodlar va argumentlar ilg'or namunasi #30
## Topshiriq sharti:
330-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_330(son, koeff = 1)
  son * koeff
end

puts "Natija: #{murakkab_amal_330(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 330-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 10
```


# 331-Topshiriq: Metodlar va argumentlar ilg'or namunasi #31
## Topshiriq sharti:
331-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_331(son, koeff = 2)
  son * koeff
end

puts "Natija: #{murakkab_amal_331(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 331-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 20
```


# 332-Topshiriq: Metodlar va argumentlar ilg'or namunasi #32
## Topshiriq sharti:
332-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_332(son, koeff = 3)
  son * koeff
end

puts "Natija: #{murakkab_amal_332(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 332-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 30
```


# 333-Topshiriq: Metodlar va argumentlar ilg'or namunasi #33
## Topshiriq sharti:
333-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_333(son, koeff = 4)
  son * koeff
end

puts "Natija: #{murakkab_amal_333(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 333-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 40
```


# 334-Topshiriq: Metodlar va argumentlar ilg'or namunasi #34
## Topshiriq sharti:
334-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_334(son, koeff = 5)
  son * koeff
end

puts "Natija: #{murakkab_amal_334(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 334-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 50
```


# 335-Topshiriq: Metodlar va argumentlar ilg'or namunasi #35
## Topshiriq sharti:
335-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_335(son, koeff = 1)
  son * koeff
end

puts "Natija: #{murakkab_amal_335(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 335-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 10
```


# 336-Topshiriq: Metodlar va argumentlar ilg'or namunasi #36
## Topshiriq sharti:
336-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_336(son, koeff = 2)
  son * koeff
end

puts "Natija: #{murakkab_amal_336(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 336-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 20
```


# 337-Topshiriq: Metodlar va argumentlar ilg'or namunasi #37
## Topshiriq sharti:
337-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_337(son, koeff = 3)
  son * koeff
end

puts "Natija: #{murakkab_amal_337(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 337-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 30
```


# 338-Topshiriq: Metodlar va argumentlar ilg'or namunasi #38
## Topshiriq sharti:
338-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_338(son, koeff = 4)
  son * koeff
end

puts "Natija: #{murakkab_amal_338(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 338-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 40
```


# 339-Topshiriq: Metodlar va argumentlar ilg'or namunasi #39
## Topshiriq sharti:
339-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_339(son, koeff = 5)
  son * koeff
end

puts "Natija: #{murakkab_amal_339(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 339-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 50
```


# 340-Topshiriq: Metodlar va argumentlar ilg'or namunasi #40
## Topshiriq sharti:
340-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_340(son, koeff = 1)
  son * koeff
end

puts "Natija: #{murakkab_amal_340(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 340-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 10
```


# 341-Topshiriq: Metodlar va argumentlar ilg'or namunasi #41
## Topshiriq sharti:
341-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_341(son, koeff = 2)
  son * koeff
end

puts "Natija: #{murakkab_amal_341(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 341-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 20
```


# 342-Topshiriq: Metodlar va argumentlar ilg'or namunasi #42
## Topshiriq sharti:
342-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_342(son, koeff = 3)
  son * koeff
end

puts "Natija: #{murakkab_amal_342(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 342-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 30
```


# 343-Topshiriq: Metodlar va argumentlar ilg'or namunasi #43
## Topshiriq sharti:
343-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_343(son, koeff = 4)
  son * koeff
end

puts "Natija: #{murakkab_amal_343(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 343-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 40
```


# 344-Topshiriq: Metodlar va argumentlar ilg'or namunasi #44
## Topshiriq sharti:
344-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_344(son, koeff = 5)
  son * koeff
end

puts "Natija: #{murakkab_amal_344(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 344-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 50
```


# 345-Topshiriq: Metodlar va argumentlar ilg'or namunasi #45
## Topshiriq sharti:
345-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_345(son, koeff = 1)
  son * koeff
end

puts "Natija: #{murakkab_amal_345(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 345-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 10
```


# 346-Topshiriq: Metodlar va argumentlar ilg'or namunasi #46
## Topshiriq sharti:
346-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_346(son, koeff = 2)
  son * koeff
end

puts "Natija: #{murakkab_amal_346(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 346-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 20
```


# 347-Topshiriq: Metodlar va argumentlar ilg'or namunasi #47
## Topshiriq sharti:
347-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_347(son, koeff = 3)
  son * koeff
end

puts "Natija: #{murakkab_amal_347(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 347-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 30
```


# 348-Topshiriq: Metodlar va argumentlar ilg'or namunasi #48
## Topshiriq sharti:
348-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_348(son, koeff = 4)
  son * koeff
end

puts "Natija: #{murakkab_amal_348(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 348-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 40
```


# 349-Topshiriq: Metodlar va argumentlar ilg'or namunasi #49
## Topshiriq sharti:
349-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_349(son, koeff = 5)
  son * koeff
end

puts "Natija: #{murakkab_amal_349(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 349-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 50
```


# 350-Topshiriq: Metodlar va argumentlar ilg'or namunasi #50
## Topshiriq sharti:
350-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
def murakkab_amal_350(son, koeff = 1)
  son * koeff
end

puts "Natija: #{murakkab_amal_350(10)}"
```

## Tushuntirish va Mantiq:
Ushbu 350-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 10
```

