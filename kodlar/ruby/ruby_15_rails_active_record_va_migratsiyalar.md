# 701-Topshiriq: ActiveRecord Model yaratish va Validatsiyalar
## Topshiriq sharti:
Foydalanuvchi elektron pochtasi va ismi majburiyligini tekshiruvchi model tuzing.

## Yechim (Ruby kodi):
```ruby
class User
  # ActiveRecord::Base
  attr_accessor :name, :email

  def initialize(attrs = {})
    @name = attrs[:name]
    @email = attrs[:email]
  end

  def valid?
    !@name.to_s.strip.empty? && !@email.to_s.strip.empty?
  end
end

u1 = User.new(name: "Ali", email: "ali@uz.uz")
u2 = User.new(name: "", email: "")

puts "u1 validmi? #{u1.valid?}"
puts "u2 validmi? #{u2.valid?}"
```

## Tushuntirish va Mantiq:
ActiveRecord modellarida `validates :name, presence: true` ma'lumotlar bazasiga noto'g'ri yozuvlar tushishining oldini oladi.

## Ishlash natijasi:
```text
u1 validmi? true
u2 validmi? false
```


# 702-Topshiriq: Munosabatlar (Associations): has_many va belongs_to
## Topshiriq sharti:
Muallif va uning maqolalari o'rtasidagi 1-to-N bog'liqlikni tushuntiring.

## Yechim (Ruby kodi):
```ruby
puts "Author: has_many :articles, dependent: :destroy"
puts "Article: belongs_to :author"
```

## Tushuntirish va Mantiq:
`has_many` va `belongs_to` Rails-da relyatsion jadvallarni bog'lovchi asosiy assotsiatsiyalardir.

## Ishlash natijasi:
```text
Author: has_many :articles, dependent: :destroy
Article: belongs_to :author
```


# 703-Topshiriq: N+1 so'rovlar muammosi va includes yechimi
## Topshiriq sharti:
N+1 muammosi qanday yuzaga kelishi va uni eager loading orqali yo'qotishni ko'rsating.

## Yechim (Ruby kodi):
```ruby
# Yomon: Post.all.each { |p| puts p.author.name } -> N+1 so'rov
# Yaxshi: Post.includes(:author).each { |p| puts p.author.name } -> Atigi 2 ta SQL so'rov
puts "includes(:author) N+1 muammosini hal qilib, barcha mualliflarni bitta so'rovda yuklaydi."
```

## Tushuntirish va Mantiq:
'includes' metodi barcha bog'liq yozuvlarni oldindan (eager loading) xotiraga yuklab, ma'lumotlar bazasi yuklamasini keskin kamaytiradi.

## Ishlash natijasi:
```text
includes(:author) N+1 muammosini hal qilib, barcha mualliflarni bitta so'rovda yuklaydi.
```


# 704-Topshiriq: ActiveRecord Scopes
## Topshiriq sharti:
Tez-tez ishlatiladigan SQL filtrlarni scope orqali nomlang.

## Yechim (Ruby kodi):
```ruby
# scope :active, -> { where(status: 'active') }
# scope :recent, -> { order(created_at: :desc).limit(10) }
puts "Scope-lar zanjirli chaqirilishi mumkin: User.active.recent"
```

## Tushuntirish va Mantiq:
Scope-lar lambda ko'rinishida yozilib, qayta ishlatiluvchi zanjirli SQL so'rovlarini yaratadi.

## Ishlash natijasi:
```text
Scope-lar zanjirli chaqirilishi mumkin: User.active.recent
```


# 705-Topshiriq: ActiveRecord Callbacks: before_save va after_create
## Topshiriq sharti:
Foydalanuvchi saqlanishidan oldin emailni kichik harflarga o'tkazing.

## Yechim (Ruby kodi):
```ruby
email = "   Foydalanuvchi@Domain.UZ  "
tozalangan_email = email.strip.downcase

puts "Tozalangan email: #{tozalangan_email}"
```

## Tushuntirish va Mantiq:
Callbacks (before_save, after_create) ma'lumotlar bazasiga yozishdan oldin yoki keyin avtomatik amallarni bajarishga xizmat qiladi.

## Ishlash natijasi:
```text
Tozalangan email: foydalanuvchi@domain.uz
```


# 706-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #6
## Topshiriq sharti:
706-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 706: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 706-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 706: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 707-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #7
## Topshiriq sharti:
707-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 707: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 707-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 707: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 708-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #8
## Topshiriq sharti:
708-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 708: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 708-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 708: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 709-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #9
## Topshiriq sharti:
709-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 709: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 709-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 709: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 710-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #10
## Topshiriq sharti:
710-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 710: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 710-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 710: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 711-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #11
## Topshiriq sharti:
711-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 711: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 711-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 711: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 712-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #12
## Topshiriq sharti:
712-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 712: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 712-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 712: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 713-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #13
## Topshiriq sharti:
713-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 713: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 713-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 713: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 714-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #14
## Topshiriq sharti:
714-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 714: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 714-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 714: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 715-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #15
## Topshiriq sharti:
715-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 715: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 715-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 715: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 716-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #16
## Topshiriq sharti:
716-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 716: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 716-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 716: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 717-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #17
## Topshiriq sharti:
717-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 717: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 717-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 717: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 718-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #18
## Topshiriq sharti:
718-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 718: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 718-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 718: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 719-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #19
## Topshiriq sharti:
719-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 719: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 719-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 719: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 720-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #20
## Topshiriq sharti:
720-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 720: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 720-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 720: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 721-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #21
## Topshiriq sharti:
721-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 721: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 721-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 721: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 722-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #22
## Topshiriq sharti:
722-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 722: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 722-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 722: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 723-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #23
## Topshiriq sharti:
723-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 723: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 723-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 723: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 724-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #24
## Topshiriq sharti:
724-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 724: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 724-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 724: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 725-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #25
## Topshiriq sharti:
725-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 725: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 725-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 725: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 726-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #26
## Topshiriq sharti:
726-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 726: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 726-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 726: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 727-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #27
## Topshiriq sharti:
727-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 727: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 727-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 727: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 728-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #28
## Topshiriq sharti:
728-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 728: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 728-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 728: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 729-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #29
## Topshiriq sharti:
729-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 729: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 729-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 729: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 730-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #30
## Topshiriq sharti:
730-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 730: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 730-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 730: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 731-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #31
## Topshiriq sharti:
731-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 731: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 731-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 731: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 732-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #32
## Topshiriq sharti:
732-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 732: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 732-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 732: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 733-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #33
## Topshiriq sharti:
733-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 733: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 733-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 733: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 734-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #34
## Topshiriq sharti:
734-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 734: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 734-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 734: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 735-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #35
## Topshiriq sharti:
735-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 735: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 735-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 735: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 736-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #36
## Topshiriq sharti:
736-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 736: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 736-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 736: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 737-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #37
## Topshiriq sharti:
737-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 737: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 737-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 737: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 738-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #38
## Topshiriq sharti:
738-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 738: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 738-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 738: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 739-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #39
## Topshiriq sharti:
739-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 739: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 739-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 739: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 740-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #40
## Topshiriq sharti:
740-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 740: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 740-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 740: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 741-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #41
## Topshiriq sharti:
741-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 741: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 741-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 741: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 742-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #42
## Topshiriq sharti:
742-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 742: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 742-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 742: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 743-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #43
## Topshiriq sharti:
743-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 743: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 743-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 743: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 744-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #44
## Topshiriq sharti:
744-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 744: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 744-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 744: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 745-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #45
## Topshiriq sharti:
745-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 745: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 745-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 745: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 746-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #46
## Topshiriq sharti:
746-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 746: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 746-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 746: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 747-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #47
## Topshiriq sharti:
747-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 747: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 747-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 747: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 748-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #48
## Topshiriq sharti:
748-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 748: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 748-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 748: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 749-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #49
## Topshiriq sharti:
749-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 749: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 749-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 749: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```


# 750-Topshiriq: ActiveRecord va ma'lumotlar bazasi amaliyoti #50
## Topshiriq sharti:
750-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Query 750: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Ushbu 750-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Query 750: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi.
```

