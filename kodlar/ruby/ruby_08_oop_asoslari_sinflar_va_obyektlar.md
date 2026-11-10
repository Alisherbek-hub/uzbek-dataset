# 351-Topshiriq: Class e'lon qilish, initialize va nusxa o'zgaruvchilari
## Topshiriq sharti:
Foydalanuvchi ma'lumotlarini saqlovchi User sinfini yarating.

## Yechim (Ruby kodi):
```ruby
class User
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
```

## Tushuntirish va Mantiq:
Ruby-da sinf 'class' kalit so'zi bilan yaratiladi. 'initialize' konstruktor vazifasini bajaradi. '@ism' kabi kuchukcha bilan boshlangan o'zgaruvchilar har bir obyektning xususiy nusxa o'zgaruvchilaridir (instance variables).

## Ishlash natijasi:
```text
Foydalanuvchi: Dilshod (dilshod@mail.uz)
```


# 352-Topshiriq: Atribut aksessorlari: attr_reader, attr_writer va attr_accessor
## Topshiriq sharti:
O'zgaruvchilarga getter va setter metodlarini bir qatorda oching.

## Yechim (Ruby kodi):
```ruby
class Mahsulot
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
```

## Tushuntirish va Mantiq:
'attr_reader' getter yaratadi, 'attr_writer' setter yaratadi, 'attr_accessor' esa ikkalasini bir vaqtda hosil qiladi.

## Ishlash natijasi:
```text
ID: 101, Boshlang'ich narx: $25.0
Yangilangan narx: $29.99
```


# 353-Topshiriq: Sinf metodlari: def self.metod
## Topshiriq sharti:
Obyekt nusxasisiz to'g'ridan-to'g'ri sinf nomidan chaqiriladigan metod yarating.

## Yechim (Ruby kodi):
```ruby
class Matematika
  PI = 3.14159

  def self.kvadrat(x)
    x * x
  end
end

puts "5 ning kvadrati: #{Matematika.kvadrat(5)}"
puts "PI: #{Matematika::PI}"
```

## Tushuntirish va Mantiq:
'def self.metod' sinf metodlarini (static methods) yaratishda ishlatiladi va `SinfNomi.metod` shaklida chaqiriladi.

## Ishlash natijasi:
```text
5 ning kvadrati: 25
PI: 3.14159
```


# 354-Topshiriq: Sinf o'zgaruvchilari: @@var va ularning xavfi
## Topshiriq sharti:
Yaratilgan barcha obyektlar sonini sanovchi sinf hisoblagichini tuzing.

## Yechim (Ruby kodi):
```ruby
class Avtomobil
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
```

## Tushuntirish va Mantiq:
'@@' bilan boshlangan o'zgaruvchilar sinf va uning barcha merosxo'rlari o'rtasida umumiy bo'ladi. Katta iyerarxiyalarda ular tasodifan qayta yozilib ketishi mumkinligi sababli ehtiyotkorlik bilan ishlatiladi.

## Ishlash natijasi:
```text
Jami avtomobillar soni: 3
```


# 355-Topshiriq: to_s va inspect metodlarini qayta aniqlash
## Topshiriq sharti:
Obyekt konsolda chiroyli matn shaklida ko'rinishini ta'minlang.

## Yechim (Ruby kodi):
```ruby
class Kitob
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
```

## Tushuntirish va Mantiq:
'to_s' foydalanuvchiga matnli ko'rsatishda, 'inspect' esa dasturchiga debug qilishda obyektning ifodasini belgilaydi.

## Ishlash natijasi:
```text
puts bilan (to_s): Shum Bola (180 sahifa)
p bilan (inspect): #<Kitob:Shum Bola>
```


# 356-Topshiriq: OOP asoslari va sinflar namunasi #6
## Topshiriq sharti:
356-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_356
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 6
end

m = Model_356.new(356)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 356-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 362
```


# 357-Topshiriq: OOP asoslari va sinflar namunasi #7
## Topshiriq sharti:
357-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_357
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 7
end

m = Model_357.new(357)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 357-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 364
```


# 358-Topshiriq: OOP asoslari va sinflar namunasi #8
## Topshiriq sharti:
358-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_358
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 8
end

m = Model_358.new(358)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 358-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 366
```


# 359-Topshiriq: OOP asoslari va sinflar namunasi #9
## Topshiriq sharti:
359-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_359
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 9
end

m = Model_359.new(359)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 359-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 368
```


# 360-Topshiriq: OOP asoslari va sinflar namunasi #10
## Topshiriq sharti:
360-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_360
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 0
end

m = Model_360.new(360)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 360-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 360
```


# 361-Topshiriq: OOP asoslari va sinflar namunasi #11
## Topshiriq sharti:
361-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_361
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 1
end

m = Model_361.new(361)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 361-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 362
```


# 362-Topshiriq: OOP asoslari va sinflar namunasi #12
## Topshiriq sharti:
362-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_362
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 2
end

m = Model_362.new(362)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 362-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 364
```


# 363-Topshiriq: OOP asoslari va sinflar namunasi #13
## Topshiriq sharti:
363-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_363
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 3
end

m = Model_363.new(363)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 363-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 366
```


# 364-Topshiriq: OOP asoslari va sinflar namunasi #14
## Topshiriq sharti:
364-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_364
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 4
end

m = Model_364.new(364)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 364-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 368
```


# 365-Topshiriq: OOP asoslari va sinflar namunasi #15
## Topshiriq sharti:
365-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_365
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 5
end

m = Model_365.new(365)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 365-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 370
```


# 366-Topshiriq: OOP asoslari va sinflar namunasi #16
## Topshiriq sharti:
366-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_366
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 6
end

m = Model_366.new(366)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 366-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 372
```


# 367-Topshiriq: OOP asoslari va sinflar namunasi #17
## Topshiriq sharti:
367-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_367
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 7
end

m = Model_367.new(367)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 367-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 374
```


# 368-Topshiriq: OOP asoslari va sinflar namunasi #18
## Topshiriq sharti:
368-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_368
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 8
end

m = Model_368.new(368)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 368-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 376
```


# 369-Topshiriq: OOP asoslari va sinflar namunasi #19
## Topshiriq sharti:
369-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_369
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 9
end

m = Model_369.new(369)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 369-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 378
```


# 370-Topshiriq: OOP asoslari va sinflar namunasi #20
## Topshiriq sharti:
370-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_370
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 0
end

m = Model_370.new(370)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 370-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 370
```


# 371-Topshiriq: OOP asoslari va sinflar namunasi #21
## Topshiriq sharti:
371-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_371
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 1
end

m = Model_371.new(371)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 371-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 372
```


# 372-Topshiriq: OOP asoslari va sinflar namunasi #22
## Topshiriq sharti:
372-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_372
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 2
end

m = Model_372.new(372)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 372-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 374
```


# 373-Topshiriq: OOP asoslari va sinflar namunasi #23
## Topshiriq sharti:
373-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_373
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 3
end

m = Model_373.new(373)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 373-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 376
```


# 374-Topshiriq: OOP asoslari va sinflar namunasi #24
## Topshiriq sharti:
374-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_374
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 4
end

m = Model_374.new(374)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 374-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 378
```


# 375-Topshiriq: OOP asoslari va sinflar namunasi #25
## Topshiriq sharti:
375-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_375
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 5
end

m = Model_375.new(375)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 375-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 380
```


# 376-Topshiriq: OOP asoslari va sinflar namunasi #26
## Topshiriq sharti:
376-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_376
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 6
end

m = Model_376.new(376)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 376-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 382
```


# 377-Topshiriq: OOP asoslari va sinflar namunasi #27
## Topshiriq sharti:
377-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_377
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 7
end

m = Model_377.new(377)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 377-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 384
```


# 378-Topshiriq: OOP asoslari va sinflar namunasi #28
## Topshiriq sharti:
378-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_378
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 8
end

m = Model_378.new(378)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 378-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 386
```


# 379-Topshiriq: OOP asoslari va sinflar namunasi #29
## Topshiriq sharti:
379-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_379
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 9
end

m = Model_379.new(379)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 379-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 388
```


# 380-Topshiriq: OOP asoslari va sinflar namunasi #30
## Topshiriq sharti:
380-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_380
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 0
end

m = Model_380.new(380)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 380-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 380
```


# 381-Topshiriq: OOP asoslari va sinflar namunasi #31
## Topshiriq sharti:
381-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_381
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 1
end

m = Model_381.new(381)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 381-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 382
```


# 382-Topshiriq: OOP asoslari va sinflar namunasi #32
## Topshiriq sharti:
382-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_382
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 2
end

m = Model_382.new(382)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 382-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 384
```


# 383-Topshiriq: OOP asoslari va sinflar namunasi #33
## Topshiriq sharti:
383-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_383
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 3
end

m = Model_383.new(383)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 383-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 386
```


# 384-Topshiriq: OOP asoslari va sinflar namunasi #34
## Topshiriq sharti:
384-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_384
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 4
end

m = Model_384.new(384)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 384-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 388
```


# 385-Topshiriq: OOP asoslari va sinflar namunasi #35
## Topshiriq sharti:
385-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_385
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 5
end

m = Model_385.new(385)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 385-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 390
```


# 386-Topshiriq: OOP asoslari va sinflar namunasi #36
## Topshiriq sharti:
386-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_386
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 6
end

m = Model_386.new(386)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 386-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 392
```


# 387-Topshiriq: OOP asoslari va sinflar namunasi #37
## Topshiriq sharti:
387-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_387
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 7
end

m = Model_387.new(387)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 387-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 394
```


# 388-Topshiriq: OOP asoslari va sinflar namunasi #38
## Topshiriq sharti:
388-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_388
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 8
end

m = Model_388.new(388)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 388-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 396
```


# 389-Topshiriq: OOP asoslari va sinflar namunasi #39
## Topshiriq sharti:
389-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_389
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 9
end

m = Model_389.new(389)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 389-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 398
```


# 390-Topshiriq: OOP asoslari va sinflar namunasi #40
## Topshiriq sharti:
390-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_390
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 0
end

m = Model_390.new(390)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 390-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 390
```


# 391-Topshiriq: OOP asoslari va sinflar namunasi #41
## Topshiriq sharti:
391-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_391
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 1
end

m = Model_391.new(391)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 391-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 392
```


# 392-Topshiriq: OOP asoslari va sinflar namunasi #42
## Topshiriq sharti:
392-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_392
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 2
end

m = Model_392.new(392)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 392-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 394
```


# 393-Topshiriq: OOP asoslari va sinflar namunasi #43
## Topshiriq sharti:
393-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_393
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 3
end

m = Model_393.new(393)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 393-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 396
```


# 394-Topshiriq: OOP asoslari va sinflar namunasi #44
## Topshiriq sharti:
394-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_394
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 4
end

m = Model_394.new(394)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 394-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 398
```


# 395-Topshiriq: OOP asoslari va sinflar namunasi #45
## Topshiriq sharti:
395-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_395
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 5
end

m = Model_395.new(395)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 395-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 400
```


# 396-Topshiriq: OOP asoslari va sinflar namunasi #46
## Topshiriq sharti:
396-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_396
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 6
end

m = Model_396.new(396)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 396-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 402
```


# 397-Topshiriq: OOP asoslari va sinflar namunasi #47
## Topshiriq sharti:
397-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_397
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 7
end

m = Model_397.new(397)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 397-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 404
```


# 398-Topshiriq: OOP asoslari va sinflar namunasi #48
## Topshiriq sharti:
398-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_398
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 8
end

m = Model_398.new(398)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 398-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 406
```


# 399-Topshiriq: OOP asoslari va sinflar namunasi #49
## Topshiriq sharti:
399-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_399
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 9
end

m = Model_399.new(399)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 399-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 408
```


# 400-Topshiriq: OOP asoslari va sinflar namunasi #50
## Topshiriq sharti:
400-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.

## Yechim (Ruby kodi):
```ruby
class Model_400
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + 0
end

m = Model_400.new(400)
puts "Natija: #{m.hisob}"
```

## Tushuntirish va Mantiq:
Ushbu 400-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: 400
```

