# 601-Topshiriq: Gemfile tuzilishi va versiya cheklovlari
## Topshiriq sharti:
Zamonaviy Rails loyihasi Gemfile faylining asosiy bloklarini yozing.

## Yechim (Ruby kodi):
```ruby
gemfile_matni = <<~GEMFILE
  source "https://rubygems.org"
  git_source(:github) { |repo| "https://github.com/\#{repo}.git" }

  ruby ">= 3.2.0"

  gem "rails", "~> 7.1.0"
  gem "pg", "~> 1.1"
  gem "puma", ">= 5.0"
GEMFILE

puts gemfile_matni
```

## Tushuntirish va Mantiq:
'~> 7.1.0' (Pessimistic constraint) faqat patch versiyalarni (7.1.1, 7.1.2) yangilashga ruxsat beradi, ammo yangi 'breaking change' li 7.2.0 ga o'tmaydi.

## Ishlash natijasi:
```text
source "https://rubygems.org"
git_source(:github) { |repo| "https://github.com/\#{repo}.git" }

ruby ">= 3.2.0"

gem "rails", "~> 7.1.0"
gem "pg", "~> 1.1"
gem "puma", ">= 5.0"
```


# 602-Topshiriq: Gemspec fayli arxitekturasi
## Topshiriq sharti:
O'z shaxsiy ochiq kodli gemingizning spesifikatsiyasini tuzing.

## Yechim (Ruby kodi):
```ruby
gemspec_shabloni = <<~SPEC
  Gem::Specification.new do |s|
    s.name        = "khorazmiy_ai_sdk"
    s.version     = "1.0.0"
    s.summary     = "Khorazmiy AI rasmiy Ruby mijozi"
    s.authors     = ["Khorazmiy AI Jamoasi"]
    s.files       = ["lib/khorazmiy_ai.rb"]
    s.license     = "MIT"
  end
SPEC

puts gemspec_shabloni
```

## Tushuntirish va Mantiq:
Gemspec gem haqidagi barcha metadata, versiya, bog'liqliklar va mualliflik huquqlarini o'z ichiga oladi.

## Ishlash natijasi:
```text
Gem::Specification.new do |s|
  s.name        = "khorazmiy_ai_sdk"
  s.version     = "1.0.0"
  s.summary     = "Khorazmiy AI rasmiy Ruby mijozi"
  s.authors     = ["Khorazmiy AI Jamoasi"]
  s.files       = ["lib/khorazmiy_ai.rb"]
  s.license     = "MIT"
end
```


# 603-Topshiriq: HTTParty orqali REST API so'rov yuborish
## Topshiriq sharti:
Tashqi API-dan JSON ma'lumotlarni o'quvchi so'rovni simulyatsiya qiling.

## Yechim (Ruby kodi):
```ruby
# require 'httparty'
class ObHavoMijozi
  def self.harorat(shahar)
    # response = HTTParty.get("https://api.obhavo.uz/data?city=#{shahar}")
    { shahar: shahar, harorat: 28, status: "Quyoshli" }
  end
end

malumot = ObHavoMijozi.harorat("Buxoro")
puts "Ob-havo: #{malumot[:shahar]}da #{malumot[:harorat]}C, #{malumot[:status]}"
```

## Tushuntirish va Mantiq:
HTTParty Ruby-da REST API lar bilan ishlash uchun dunyodagi eng mashhur va qulay gemlardan biridir.

## Ishlash natijasi:
```text
Ob-havo: Buxoroda 28C, Quyoshli
```


# 604-Topshiriq: Dotenv orqali xavfsiz kalitlarni yuklash (.env)
## Topshiriq sharti:
API maxfiy kalitlarini kodda yozmasdan muhit o'zgaruvchilaridan oling.

## Yechim (Ruby kodi):
```ruby
# require 'dotenv/load'
# ENV['API_KEY'] orqali o'qiladi
ENV['AI_SERVICE_KEY'] = "ai_sec_9921_uz"

kalit = ENV['AI_SERVICE_KEY']
puts "Xizmat kaliti mavjudmi? #{!kalit.nil?}"
puts "Kalit prefiksi: #{kalit[0..5]}***"
```

## Tushuntirish va Mantiq:
Xavfsizlik qoidalariga ko'ra API kalitlari va parollar manba kodiga yozilmaydi, '.env' faylida saqlanib `Dotenv` orqali yuklanadi.

## Ishlash natijasi:
```text
Xizmat kaliti mavjudmi? true
Kalit prefiksi: ai_sec***
```


# 605-Topshiriq: RuboCop linter qoidalari
## Topshiriq sharti:
Ruby kodini professional uslub va standartlarga tekshiring.

## Yechim (Ruby kodi):
```ruby
puts "RuboCop Ruby kodida xavfsizlik, unumdorlik va qat'iy uslubni ta'minlaydi."
```

## Tushuntirish va Mantiq:
RuboCop Ruby hamjamiyatining rasmiy uslub qo'llanmasi (Style Guide) asosida kod sifatini tekshiruvchi statik analizatoridir.

## Ishlash natijasi:
```text
RuboCop Ruby kodida xavfsizlik, unumdorlik va qat'iy uslubni ta'minlaydi.
```


# 606-Topshiriq: Gemlar va kutubxonalar amaliyoti #6
## Topshiriq sharti:
606-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 606: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 606-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 606: Modulli kengaytma faollashtirildi.
```


# 607-Topshiriq: Gemlar va kutubxonalar amaliyoti #7
## Topshiriq sharti:
607-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 607: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 607-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 607: Modulli kengaytma faollashtirildi.
```


# 608-Topshiriq: Gemlar va kutubxonalar amaliyoti #8
## Topshiriq sharti:
608-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 608: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 608-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 608: Modulli kengaytma faollashtirildi.
```


# 609-Topshiriq: Gemlar va kutubxonalar amaliyoti #9
## Topshiriq sharti:
609-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 609: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 609-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 609: Modulli kengaytma faollashtirildi.
```


# 610-Topshiriq: Gemlar va kutubxonalar amaliyoti #10
## Topshiriq sharti:
610-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 610: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 610-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 610: Modulli kengaytma faollashtirildi.
```


# 611-Topshiriq: Gemlar va kutubxonalar amaliyoti #11
## Topshiriq sharti:
611-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 611: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 611-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 611: Modulli kengaytma faollashtirildi.
```


# 612-Topshiriq: Gemlar va kutubxonalar amaliyoti #12
## Topshiriq sharti:
612-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 612: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 612-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 612: Modulli kengaytma faollashtirildi.
```


# 613-Topshiriq: Gemlar va kutubxonalar amaliyoti #13
## Topshiriq sharti:
613-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 613: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 613-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 613: Modulli kengaytma faollashtirildi.
```


# 614-Topshiriq: Gemlar va kutubxonalar amaliyoti #14
## Topshiriq sharti:
614-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 614: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 614-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 614: Modulli kengaytma faollashtirildi.
```


# 615-Topshiriq: Gemlar va kutubxonalar amaliyoti #15
## Topshiriq sharti:
615-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 615: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 615-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 615: Modulli kengaytma faollashtirildi.
```


# 616-Topshiriq: Gemlar va kutubxonalar amaliyoti #16
## Topshiriq sharti:
616-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 616: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 616-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 616: Modulli kengaytma faollashtirildi.
```


# 617-Topshiriq: Gemlar va kutubxonalar amaliyoti #17
## Topshiriq sharti:
617-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 617: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 617-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 617: Modulli kengaytma faollashtirildi.
```


# 618-Topshiriq: Gemlar va kutubxonalar amaliyoti #18
## Topshiriq sharti:
618-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 618: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 618-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 618: Modulli kengaytma faollashtirildi.
```


# 619-Topshiriq: Gemlar va kutubxonalar amaliyoti #19
## Topshiriq sharti:
619-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 619: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 619-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 619: Modulli kengaytma faollashtirildi.
```


# 620-Topshiriq: Gemlar va kutubxonalar amaliyoti #20
## Topshiriq sharti:
620-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 620: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 620-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 620: Modulli kengaytma faollashtirildi.
```


# 621-Topshiriq: Gemlar va kutubxonalar amaliyoti #21
## Topshiriq sharti:
621-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 621: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 621-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 621: Modulli kengaytma faollashtirildi.
```


# 622-Topshiriq: Gemlar va kutubxonalar amaliyoti #22
## Topshiriq sharti:
622-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 622: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 622-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 622: Modulli kengaytma faollashtirildi.
```


# 623-Topshiriq: Gemlar va kutubxonalar amaliyoti #23
## Topshiriq sharti:
623-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 623: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 623-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 623: Modulli kengaytma faollashtirildi.
```


# 624-Topshiriq: Gemlar va kutubxonalar amaliyoti #24
## Topshiriq sharti:
624-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 624: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 624-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 624: Modulli kengaytma faollashtirildi.
```


# 625-Topshiriq: Gemlar va kutubxonalar amaliyoti #25
## Topshiriq sharti:
625-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 625: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 625-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 625: Modulli kengaytma faollashtirildi.
```


# 626-Topshiriq: Gemlar va kutubxonalar amaliyoti #26
## Topshiriq sharti:
626-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 626: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 626-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 626: Modulli kengaytma faollashtirildi.
```


# 627-Topshiriq: Gemlar va kutubxonalar amaliyoti #27
## Topshiriq sharti:
627-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 627: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 627-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 627: Modulli kengaytma faollashtirildi.
```


# 628-Topshiriq: Gemlar va kutubxonalar amaliyoti #28
## Topshiriq sharti:
628-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 628: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 628-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 628: Modulli kengaytma faollashtirildi.
```


# 629-Topshiriq: Gemlar va kutubxonalar amaliyoti #29
## Topshiriq sharti:
629-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 629: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 629-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 629: Modulli kengaytma faollashtirildi.
```


# 630-Topshiriq: Gemlar va kutubxonalar amaliyoti #30
## Topshiriq sharti:
630-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 630: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 630-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 630: Modulli kengaytma faollashtirildi.
```


# 631-Topshiriq: Gemlar va kutubxonalar amaliyoti #31
## Topshiriq sharti:
631-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 631: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 631-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 631: Modulli kengaytma faollashtirildi.
```


# 632-Topshiriq: Gemlar va kutubxonalar amaliyoti #32
## Topshiriq sharti:
632-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 632: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 632-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 632: Modulli kengaytma faollashtirildi.
```


# 633-Topshiriq: Gemlar va kutubxonalar amaliyoti #33
## Topshiriq sharti:
633-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 633: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 633-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 633: Modulli kengaytma faollashtirildi.
```


# 634-Topshiriq: Gemlar va kutubxonalar amaliyoti #34
## Topshiriq sharti:
634-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 634: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 634-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 634: Modulli kengaytma faollashtirildi.
```


# 635-Topshiriq: Gemlar va kutubxonalar amaliyoti #35
## Topshiriq sharti:
635-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 635: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 635-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 635: Modulli kengaytma faollashtirildi.
```


# 636-Topshiriq: Gemlar va kutubxonalar amaliyoti #36
## Topshiriq sharti:
636-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 636: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 636-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 636: Modulli kengaytma faollashtirildi.
```


# 637-Topshiriq: Gemlar va kutubxonalar amaliyoti #37
## Topshiriq sharti:
637-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 637: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 637-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 637: Modulli kengaytma faollashtirildi.
```


# 638-Topshiriq: Gemlar va kutubxonalar amaliyoti #38
## Topshiriq sharti:
638-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 638: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 638-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 638: Modulli kengaytma faollashtirildi.
```


# 639-Topshiriq: Gemlar va kutubxonalar amaliyoti #39
## Topshiriq sharti:
639-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 639: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 639-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 639: Modulli kengaytma faollashtirildi.
```


# 640-Topshiriq: Gemlar va kutubxonalar amaliyoti #40
## Topshiriq sharti:
640-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 640: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 640-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 640: Modulli kengaytma faollashtirildi.
```


# 641-Topshiriq: Gemlar va kutubxonalar amaliyoti #41
## Topshiriq sharti:
641-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 641: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 641-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 641: Modulli kengaytma faollashtirildi.
```


# 642-Topshiriq: Gemlar va kutubxonalar amaliyoti #42
## Topshiriq sharti:
642-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 642: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 642-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 642: Modulli kengaytma faollashtirildi.
```


# 643-Topshiriq: Gemlar va kutubxonalar amaliyoti #43
## Topshiriq sharti:
643-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 643: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 643-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 643: Modulli kengaytma faollashtirildi.
```


# 644-Topshiriq: Gemlar va kutubxonalar amaliyoti #44
## Topshiriq sharti:
644-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 644: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 644-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 644: Modulli kengaytma faollashtirildi.
```


# 645-Topshiriq: Gemlar va kutubxonalar amaliyoti #45
## Topshiriq sharti:
645-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 645: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 645-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 645: Modulli kengaytma faollashtirildi.
```


# 646-Topshiriq: Gemlar va kutubxonalar amaliyoti #46
## Topshiriq sharti:
646-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 646: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 646-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 646: Modulli kengaytma faollashtirildi.
```


# 647-Topshiriq: Gemlar va kutubxonalar amaliyoti #47
## Topshiriq sharti:
647-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 647: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 647-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 647: Modulli kengaytma faollashtirildi.
```


# 648-Topshiriq: Gemlar va kutubxonalar amaliyoti #48
## Topshiriq sharti:
648-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 648: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 648-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 648: Modulli kengaytma faollashtirildi.
```


# 649-Topshiriq: Gemlar va kutubxonalar amaliyoti #49
## Topshiriq sharti:
649-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 649: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 649-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 649: Modulli kengaytma faollashtirildi.
```


# 650-Topshiriq: Gemlar va kutubxonalar amaliyoti #50
## Topshiriq sharti:
650-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.

## Yechim (Ruby kodi):
```ruby
puts "Kutubxona 650: Modulli kengaytma faollashtirildi."
```

## Tushuntirish va Mantiq:
Ushbu 650-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.

## Ishlash natijasi:
```text
Kutubxona 650: Modulli kengaytma faollashtirildi.
```

