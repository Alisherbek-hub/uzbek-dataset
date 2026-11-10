# 251-Topshiriq: Enumerable moduli mohiyati va each metodi talabi
## Topshiriq sharti:
O'z shaxsiy sinfingizga Enumerable modulini ulang va barcha tayyor metodlardan foydalaning.

## Yechim (Ruby kodi):
```ruby
class DasturlashTillar
  include Enumerable

  def initialize
    @tillar = ["Ruby", "Crystal", "Elixir"]
  end

  def each(&blok)
    @tillar.each(&blok)
  end
end

royxat = DasturlashTillar.new
puts "Barcha tillar: #{royxat.map(&:upcase).inspect}"
puts "Birinchi til: #{royxat.first}"
puts "Ruby mavjudmi? #{royxat.include?('Ruby')}"
```

## Tushuntirish va Mantiq:
Ruby-da 'Enumerable' moduli to'plamlar bilan ishlashning yuragi hisoblanadi. Sinf faqat bitta 'each' metodini aniqlasa kifoya: Enumerable avtomatik ravishda 50 dan ortiq qudratli metodlarni (map, select, sort, reduce va h.k.) sinfga taqdim etadi.

## Ishlash natijasi:
```text
Barcha tillar: ["RUBY", "CRYSTAL", "ELIXIR"]
Birinchi til: Ruby
Ruby mavjudmi? true
```


# 252-Topshiriq: each_with_index iteratori
## Topshiriq sharti:
Elementlarni o'z tartib raqami (indeksi) bilan birgalikda chiqaring.

## Yechim (Ruby kodi):
```ruby
mevalar = ["Olma", "Anor", "Uzum"]

mevalar.each_with_index do |meva, indeks|
  puts "#{indeks + 1}-o'rindagi meva: #{meva}"
end
```

## Tushuntirish va Mantiq:
'each_with_index' har bir iteratsiyada blok parametriga `|element, indeks|` juftligini uzatadi.

## Ishlash natijasi:
```text
1-o'rindagi meva: Olma
2-o'rindagi meva: Anor
3-o'rindagi meva: Uzum
```


# 253-Topshiriq: each_with_object iteratori
## Topshiriq sharti:
Tashqi o'zgaruvchisiz yig'uvchi (akkumulyator) obyekti bilan iteratsiya qiling.

## Yechim (Ruby kodi):
```ruby
sonlar = [1, 2, 3, 4]

kvadratlar_hash = sonlar.each_with_object({}) do |son, hash|
  hash[son] = son ** 2
end

puts "Kvadratlar Hash: #{kvadratlar_hash.inspect}"
```

## Tushuntirish va Mantiq:
'each_with_object(boshlangich_obyekt)' berilgan obyektni blokga uzatadi va oxirida o'sha to'ldirilgan obyektning o'zini qaytaradi.

## Ishlash natijasi:
```text
Kvadratlar Hash: {1=>1, 2=>4, 3=>9, 4=>16}
```


# 254-Topshiriq: map va collect metodlari
## Topshiriq sharti:
Harorat qiymatlarini Selsiydan Farengeytga o'giring.

## Yechim (Ruby kodi):
```ruby
selsiy = [0, 20, 30]
farengeyt = selsiy.map { |c| (c * 9/5.0) + 32 }

puts "Farengeyt: #{farengeyt.inspect}"
```

## Tushuntirish va Mantiq:
'map' (sinonimi 'collect') to'plamning har bir elementini blok orqali o'tkazib, bir xil o'lchamdagi yangi massiv hosil qiladi.

## Ishlash natijasi:
```text
Farengeyt: [32.0, 68.0, 86.0]
```


# 255-Topshiriq: select va filter metodlari
## Topshiriq sharti:
Mahsulotlar orasidan faqat narxi 100 dan arzonlarini ajrating.

## Yechim (Ruby kodi):
```ruby
narxlar = [45, 120, 80, 210, 95]
arzon = narxlar.select { |n| n < 100 }

puts "Arzon mahsulotlar: #{arzon.inspect}"
```

## Tushuntirish va Mantiq:
'select' (Ruby 2.6 da kiritilgan to'liq sinonimi 'filter') blok true qaytargan elementlardan yangi to'plam tuzadi.

## Ishlash natijasi:
```text
Arzon mahsulotlar: [45, 80, 95]
```


# 256-Topshiriq: reject metodi (teskari filtr)
## Topshiriq sharti:
Talabalar ro'yxatidan qoniqarsiz baho olganlarni chiqarib tashlang.

## Yechim (Ruby kodi):
```ruby
baholar = [5, 2, 4, 2, 5, 3]
yaxshi_baholar = baholar.reject { |b| b == 2 }

puts "Qoniqarsizsiz ro'yxat: #{yaxshi_baholar.inspect}"
```

## Tushuntirish va Mantiq:
'reject' metodi 'select' ning teskarisi bo'lib, blok true qaytargan elementlarni olib tashlaydi.

## Ishlash natijasi:
```text
Qoniqarsizsiz ro'yxat: [5, 4, 5, 3]
```


# 257-Topshiriq: reduce va inject metodlari
## Topshiriq sharti:
1 dan 5 gacha sonlar yig'indisini va faktorialini bir qatorda hisoblang.

## Yechim (Ruby kodi):
```ruby
yigindi = (1..5).reduce(:+)
faktorial = (1..5).inject(:*)

puts "1..5 yig'indisi: #{yigindi}"
puts "5 faktoriali: #{faktorial}"
```

## Tushuntirish va Mantiq:
'reduce' (va uning sinonimi 'inject') to'plam elementlarini umumlashtiruvchi bitta yakuniy qiymatga keltiradi. Unga operator nomi (`:+`, `:*) uzatilishi mumkin.

## Ishlash natijasi:
```text
1..5 yig'indisi: 15
5 faktoriali: 120
```


# 258-Topshiriq: find va detect metodlari
## Topshiriq sharti:
To'plamdan birinchi uchragan juft sonni toping.

## Yechim (Ruby kodi):
```ruby
sonlar = [1, 3, 5, 8, 9, 12]
birinchi_juft = sonlar.find { |s| s.even? }

puts "Birinchi juft son: #{birinchi_juft}"
```

## Tushuntirish va Mantiq:
'find' (sinonimi 'detect') shartga mos kelgan ENG BIRINCHI elementni qaytaradi va qolganlarini tekshirmaydi.

## Ishlash natijasi:
```text
Birinchi juft son: 8
```


# 259-Topshiriq: filter_map metodi (Ruby 2.7+)
## Topshiriq sharti:
Massiv elementlarini bitta qadamda ham filtrlab, ham o'zgartiring.

## Yechim (Ruby kodi):
```ruby
sonlar = [1, 2, 3, 4, 5, 6]
juftlarning_kvadrati = sonlar.filter_map { |n| n ** 2 if n.even? }

puts "Juftlarning kvadrati: #{juftlarning_kvadrati.inspect}"
```

## Tushuntirish va Mantiq:
Ruby 2.7 da kiritilgan 'filter_map' metodi `.select.map` zanjiriga nisbatan ikki barobar tez ishlaydi va oraliq massiv yaratmaydi. Blokda `nil` bo'lmagan natijalar saqlanadi.

## Ishlash natijasi:
```text
Juftlarning kvadrati: [4, 16, 36]
```


# 260-Topshiriq: all?, any?, none? va one? mantiqiy tekshiruvlari
## Topshiriq sharti:
Guruh talabalarining yoshi bo'yicha to'rtta mantiqiy savolga javob bering.

## Yechim (Ruby kodi):
```ruby
yoshlar = [20, 22, 25, 19]

puts "Hammasi balog'atga yetganmi? #{yoshlar.all? { |y| y >= 18 }}"
puts "25 yoshdan kattasi bormi? #{yoshlar.any? { |y| y > 25 }}"
puts "Birorta ham 16 yoshli yo'qmi? #{yoshlar.none? { |y| y < 18 }}"
puts "Aynan bittasi 25 yoshdami? #{yoshlar.one? { |y| y == 25 }}"
```

## Tushuntirish va Mantiq:
'all?' barcha elementlar shartga mos bo'lsa true; 'any?' kamida bittasi mos bo'lsa true; 'none?' birortasi ham mos bo'lmasa true; 'one?' esa aynan 1 ta element mos kelsa true qaytaradi.

## Ishlash natijasi:
```text
Hammasi balog'atga yetganmi? true
25 yoshdan kattasi bormi? false
Birorta ham 16 yoshli yo'qmi? true
Aynan bittasi 25 yoshdami? true
```


# 261-Topshiriq: all? va any? ga pattern/sinf uzatish (Ruby 2.5+)
## Topshiriq sharti:
Bloksiz, to'g'ridan-to'g'ri sinf yoki regex uzatib to'plamni tekshiring.

## Yechim (Ruby kodi):
```ruby
malumotlar = [10, 25, 42, 99]
sozlar = ["olma", "anor", "shaftoli"]

puts "Barchasi butun sonmi? #{malumotlar.all?(Integer)}"
puts "'o' harfi qatnashgan so'z bormi? #{sozlar.any?(/o/)}"
```

## Tushuntirish va Mantiq:
Ruby 2.5 dan boshlab `all?(Pattern)` va `any?(Pattern)` sahna ortida `Pattern === element` orqali tekshiradi va blok yozish zaruriyatini yo'qotadi.

## Ishlash natijasi:
```text
Barchasi butun sonmi? true
'o' harfi qatnashgan so'z bormi? true
```


# 262-Topshiriq: min, max va minmax metodlari
## Topshiriq sharti:
Haroratlar ichidan eng past va eng yuqori ko'rsatkichni bitta amalda toping.

## Yechim (Ruby kodi):
```ruby
haroratlar = [15.2, 8.5, 24.1, 3.8, 19.4]
eng_kichik, eng_katta = haroratlar.minmax

puts "Eng past: #{eng_kichik}C"
puts "Eng yuqori: #{eng_katta}C"
```

## Tushuntirish va Mantiq:
'minmax' metodi ikkita alohida min va max chaqiruvlariga qaraganda tezroq ishlaydi va to'plamni faqat bir marta aylanib chiqadi.

## Ishlash natijasi:
```text
Eng past: 3.8C
Eng yuqori: 24.1C
```


# 263-Topshiriq: min_by va max_by metodlari
## Topshiriq sharti:
Eng qisqa va eng uzun so'zni ularning uzunligiga qarab aniqlang.

## Yechim (Ruby kodi):
```ruby
shaharlar = ["Samarqand", "Xiva", "Toshkent", "Buxoro"]

eng_qisqa = shaharlar.min_by(&:length)
eng_uzun = shaharlar.max_by(&:length)

puts "Eng qisqa nom: #{eng_qisqa}"
puts "Eng uzun nom: #{eng_uzun}"
```

## Tushuntirish va Mantiq:
'min_by' va 'max_by' ko'rsatilgan atribut bo'yicha eng kichik va eng katta obyektni topadi.

## Ishlash natijasi:
```text
Eng qisqa nom: Xiva
Eng uzun nom: Samarqand
```


# 264-Topshiriq: sort vs sort_by (Schwarzian transform)
## Topshiriq sharti:
Obyektlarni qimmat hisob-kitobli parametr bo'yicha tezkor saralang.

## Yechim (Ruby kodi):
```ruby
kitoblar = [
  { nom: "Xamsa", varaq: 600 },
  { nom: "Boburnoma", varaq: 450 },
  { nom: "Qutadg'u bilig", varaq: 520 }
]

saralangan = kitoblar.sort_by { |k| k[:varaq] }
puts "Sahifalar bo'yicha saralangan:"
saralangan.each { |k| puts "  - #{k[:nom]}: #{k[:varaq]} bet" }
```

## Tushuntirish va Mantiq:
'sort_by' har bir element uchun hisoblash kalitini bir marta hisoblab keshlashtiradi (Schwarzian transform), shuning uchun oddiy `sort` ga nisbatan ancha tezroq ishlaydi.

## Ishlash natijasi:
```text
Sahifalar bo'yicha saralangan:
  - Boburnoma: 450 bet
  - Qutadg'u bilig: 520 bet
  - Xamsa: 600 bet
```


# 265-Topshiriq: group_by metodi
## Topshiriq sharti:
So'zlarni ularning bosh harfi bo'yicha guruhlang.

## Yechim (Ruby kodi):
```ruby
sozlar = ["olma", "anor", "shaftoli", "sholg'om", "uzum"]
guruhlar = sozlar.group_by { |s| s[0] }

guruhlar.each do |harf, royxat|
  puts "'#{harf}' harfi bilan: #{royxat.inspect}"
end
```

## Tushuntirish va Mantiq:
'group_by' to'plamni blok qaytargan qiymatlar bo'yicha Hash jadvaliga toifalab beradi.

## Ishlash natijasi:
```text
'o' harfi bilan: ["olma"]
'a' harfi bilan: ["anor"]
's' harfi bilan: ["shaftoli", "sholg'om"]
'u' harfi bilan: ["uzum"]
```


# 266-Topshiriq: partition metodi
## Topshiriq sharti:
Talabalarni imtihondan o'tganlar va yiqilganlarga ikkiga ajrating.

## Yechim (Ruby kodi):
```ruby
talabalar = [
  { ism: "Aziz", ball: 85 },
  { ism: "Bexruz", ball: 55 },
  { ism: "Charos", ball: 90 },
  { ism: "Davron", ball: 40 }
]

otganlar, yiqilganlar = talabalar.partition { |t| t[:ball] >= 60 }

puts "O'tganlar soni: #{otganlar.size}"
puts "Yiqilganlar soni: #{yiqilganlar.size}"
```

## Tushuntirish va Mantiq:
'partition' to'plamni bitta yurishda ikkita massivga ajratadi: birinchisida shart bajarilganlar, ikkinchisida bajarilmaganlar saqlanadi.

## Ishlash natijasi:
```text
O'tganlar soni: 2
Yiqilganlar soni: 2
```


# 267-Topshiriq: tally metodi (Ruby 2.7+)
## Topshiriq sharti:
Ovoz berish natijalarida har bir nomzod nechtadan ovoz olganini bitta metodda hisoblang.

## Yechim (Ruby kodi):
```ruby
ovozlar = ["Ali", "Vali", "Ali", "Ali", "Vali", "Gani"]
natijalar = ovozlar.tally

puts "Ovozlar soni: #{natijalar.inspect}"
```

## Tushuntirish va Mantiq:
Ruby 2.7 da qo'shilgan 'tally' metodi to'plamdagi har bir unikal elementning takrorlanishlar chastotasini hisoblab `{ element => soni }` Hashini qaytaradi.

## Ishlash natijasi:
```text
Ovozlar soni: {"Ali"=>3, "Vali"=>2, "Gani"=>1}
```


# 268-Topshiriq: flat_map metodi
## Topshiriq sharti:
Foydalanuvchilarning barcha teglari birlashmasini bir o'lchamli massiv qilib oling.

## Yechim (Ruby kodi):
```ruby
postlar = [
  { sarlavha: "P1", teglar: ["ruby", "web"] },
  { sarlavha: "P2", teglar: ["rails", "api"] }
]

barcha_teglar = postlar.flat_map { |p| p[:teglar] }
puts "Barcha teglar: #{barcha_teglar.inspect}"
```

## Tushuntirish va Mantiq:
'flat_map' (sinonimi 'collect_concat') avval har bir element ustida map bajaradi va keyin natijani 1 darajaga tekislaydi (flatten).

## Ishlash natijasi:
```text
Barcha teglar: ["ruby", "web", "rails", "api"]
```


# 269-Topshiriq: grep va grep_v metodlari
## Topshiriq sharti:
Aralash to'plamdan faqat sonlarni yoki regexga moslarini ajrating.

## Yechim (Ruby kodi):
```ruby
aralash = ["Salom", 42, "Dunyo", 3.14, :belgi]

faqat_sonlar = aralash.grep(Numeric)
matnlar = aralash.grep(String)
son_bolmaganlar = aralash.grep_v(Numeric)

puts "Sonlar: #{faqat_sonlar.inspect}"
puts "Matnlar: #{matnlar.inspect}"
puts "Son bo'lmaganlar: #{son_bolmaganlar.inspect}"
```

## Tushuntirish va Mantiq:
'grep(pattern)' to'plamdan `pattern === element` shartiga moslarini, 'grep_v' esa mos kelmaganlarini ajratib oladi.

## Ishlash natijasi:
```text
Sonlar: [42, 3.14]
Matnlar: ["Salom", "Dunyo"]
Son bo'lmaganlar: ["Salom", "Dunyo", :belgi]
```


# 270-Topshiriq: take_while va drop_while metodlari
## Topshiriq sharti:
Ketma-ketlikdan shart buzilguncha elementlarni oling.

## Yechim (Ruby kodi):
```ruby
ketma_ketlik = [2, 4, 6, 7, 8, 10]

boshi = ketma_ketlik.take_while(&:even?)
qolgani = ketma_ketlik.drop_while(&:even?)

puts "Juft bo'lib kelgan bosh qism: #{boshi.inspect}"
puts "Toq son boshlanganidan keyingi qism: #{qolgani.inspect}"
```

## Tushuntirish va Mantiq:
'take_while' blok false qaytargan ondayoq to'xtaydi va ungacha bo'lganlarni qaytaradi. 'drop_while' esa false qaytguncha tashlab, qolganlarini qaytaradi.

## Ishlash natijasi:
```text
Juft bo'lib kelgan bosh qism: [2, 4, 6]
Toq son boshlanganidan keyingi qism: [7, 8, 10]
```


# 271-Topshiriq: chunk va ketma-ketliklarni toifalash
## Topshiriq sharti:
Ketma-ket kelgan juft va toq sonlar bloklarini guruhlang.

## Yechim (Ruby kodi):
```ruby
sonlar = [1, 3, 5, 2, 4, 7, 9]
bloklar = sonlar.chunk { |n| n.even? }.to_a

bloklar.each do |juftmi, qator|
  puts "#{juftmi ? 'Juftlar' : 'Toqlar'}: #{qator.inspect}"
end
```

## Tushuntirish va Mantiq:
'chunk' qo'shni elementlar bir xil qiymat qaytargan davrda ularni bitta blokga birlashtiradi.

## Ishlash natijasi:
```text
Toqlar: [1, 3, 5]
Juftlar: [2, 4]
Toqlar: [7, 9]
```


# 272-Topshiriq: cycle iteratori
## Topshiriq sharti:
Svetofor ranglarini cheksiz sikl bo'ylab takrorlang.

## Yechim (Ruby kodi):
```ruby
ranglar = ["Qizil", "Sariq", "Yashil"]
natijalar = []

ranglar.cycle(2) do |rang|
  natijalar << rang
end

puts "2 tsikl svetofor: #{natijalar.inspect}"
```

## Tushuntirish va Mantiq:
'cycle(n)' to'plam bo'ylab n marta cheksiz takrorlanish hosil qiladi.

## Ishlash natijasi:
```text
2 tsikl svetofor: ["Qizil", "Sariq", "Yashil", "Qizil", "Sariq", "Yashil"]
```


# 273-Topshiriq: Lazy Enumerables: Cheksiz oqimlar va xotira tejamkorligi
## Topshiriq sharti:
Cheksiz sonlar oqimidan kvadratlari 100 dan oshadigan dastlabki 3 tasini xotira to'lmasdan toping.

## Yechim (Ruby kodi):
```ruby
cheksiz = (1..Float::INFINITY)
natija = cheksiz.lazy
  .map { |x| x * x }
  .select { |x| x > 100 }
  .take(3)
  .to_a

puts "Lazy natija: #{natija.inspect}"
```

## Tushuntirish va Mantiq:
Ruby 2.0 da taqdim etilgan '.lazy' har bir elementni navbatdagi operatsiyadan to'liq o'tkazib keyingisiga beradi (Pipelined stream processing). Bu cheksiz yoki gigabaytlik ma'lumotlarni xotirada qotmasdan qayta ishlashga imkon yaratadi.

## Ishlash natijasi:
```text
Lazy natija: [121, 144, 169]
```


# 274-Topshiriq: chain metodi: Enumerable to'plamlarini ulash (Ruby 2.6+)
## Topshiriq sharti:
Massiv va Rangeni bitta oqimga ulab iteratsiya qiling.

## Yechim (Ruby kodi):
```ruby
zanjir = [1, 2].chain(3..5)
puts "Zanjirli elementlar: #{zanjir.to_a.inspect}"
```

## Tushuntirish va Mantiq:
'chain' bir nechta to'plamlarni nusxa ko'chirmasdan yagona uzluksiz oqimga birlashtiradi.

## Ishlash natijasi:
```text
Zanjirli elementlar: [1, 2, 3, 4, 5]
```


# 275-Topshiriq: Amaliy loyiha: Server kirish jurnali (Log Analyzer) tahlili
## Topshiriq sharti:
Veb-server jurnali qatorlaridan status kodlari, eng ko'p so'ralgan yo'llar va xatoliklarni Enumerable vositasida hisoblang.

## Yechim (Ruby kodi):
```ruby
log_yozuvlari = [
  { ip: "127.0.0.1", path: "/index", status: 200 },
  { ip: "192.168.1.1", path: "/api/login", status: 200 },
  { ip: "10.0.0.5", path: "/secret", status: 403 },
  { ip: "127.0.0.1", path: "/api/data", status: 500 },
  { ip: "192.168.1.1", path: "/index", status: 200 }
]

statuslar_stat = log_yozuvlari.map { |l| l[:status] }.tally
mashhur_sahifa = log_yozuvlari.map { |l| l[:path] }.tally.max_by { |_, count| count }
xatolar = log_yozuvlari.select { |l| l[:status] >= 400 }

puts "========================================="
puts "SERVER LOGLARI TAHLILI"
puts "========================================="
puts "Status kodlari statistikasi: #{statuslar_stat.inspect}"
puts "Eng ko'p kirilgan sahifa: #{mashhur_sahifa[0]} (#{mashhur_sahifa[1]} marta)"
puts "Aniqlangan xatolar soni: #{xatolar.size}"
puts "========================================="
```

## Tushuntirish va Mantiq:
Ushbu loyihada Enumerable modulining `map`, `tally`, `max_by`, `select` metodlari bitta amaliy log tahlilchisida mujassamlashdi.

## Ishlash natijasi:
```text
=========================================
SERVER LOGLARI TAHLILI
=========================================
Status kodlari statistikasi: {200=>3, 403=>1, 500=>1}
Eng ko'p kirilgan sahifa: /index (2 marta)
Aniqlangan xatolar soni: 2
=========================================
```


# 276-Topshiriq: Enumerable ilg'or amaliyoti #26
## Topshiriq sharti:
Katta ma'lumotlar to'plamida 276-maxsus statistik va funksional saralash amalini bajaring.

## Yechim (Ruby kodi):
```ruby
to'plam = [12, 12, 0, 20]
natija = to'plam.map { |x| x * 2 }.select { |x| x > 10 }
puts "Natija: #{natija.inspect}"
```

## Tushuntirish va Mantiq:
Ushbu 276-topshiriq Enumerable to'plamlarida filtrlash, xaritalash va tartiblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: [24, 24, 40]
```


# 277-Topshiriq: Enumerable ilg'or amaliyoti #27
## Topshiriq sharti:
Katta ma'lumotlar to'plamida 277-maxsus statistik va funksional saralash amalini bajaring.

## Yechim (Ruby kodi):
```ruby
to'plam = [15, 17, 7, 2]
natija = to'plam.map { |x| x * 2 }.select { |x| x > 10 }
puts "Natija: #{natija.inspect}"
```

## Tushuntirish va Mantiq:
Ushbu 277-topshiriq Enumerable to'plamlarida filtrlash, xaritalash va tartiblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: [30, 34, 14]
```


# 278-Topshiriq: Enumerable ilg'or amaliyoti #28
## Topshiriq sharti:
Katta ma'lumotlar to'plamida 278-maxsus statistik va funksional saralash amalini bajaring.

## Yechim (Ruby kodi):
```ruby
to'plam = [1, 3, 14, 13]
natija = to'plam.map { |x| x * 2 }.select { |x| x > 10 }
puts "Natija: #{natija.inspect}"
```

## Tushuntirish va Mantiq:
Ushbu 278-topshiriq Enumerable to'plamlarida filtrlash, xaritalash va tartiblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: [28, 26]
```


# 279-Topshiriq: Enumerable ilg'or amaliyoti #29
## Topshiriq sharti:
Katta ma'lumotlar to'plamida 279-maxsus statistik va funksional saralash amalini bajaring.

## Yechim (Ruby kodi):
```ruby
to'plam = [4, 8, 21, 24]
natija = to'plam.map { |x| x * 2 }.select { |x| x > 10 }
puts "Natija: #{natija.inspect}"
```

## Tushuntirish va Mantiq:
Ushbu 279-topshiriq Enumerable to'plamlarida filtrlash, xaritalash va tartiblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: [16, 42, 48]
```


# 280-Topshiriq: Enumerable ilg'or amaliyoti #30
## Topshiriq sharti:
Katta ma'lumotlar to'plamida 280-maxsus statistik va funksional saralash amalini bajaring.

## Yechim (Ruby kodi):
```ruby
to'plam = [7, 13, 5, 6]
natija = to'plam.map { |x| x * 2 }.select { |x| x > 10 }
puts "Natija: #{natija.inspect}"
```

## Tushuntirish va Mantiq:
Ushbu 280-topshiriq Enumerable to'plamlarida filtrlash, xaritalash va tartiblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: [14, 26, 12]
```


# 281-Topshiriq: Enumerable ilg'or amaliyoti #31
## Topshiriq sharti:
Katta ma'lumotlar to'plamida 281-maxsus statistik va funksional saralash amalini bajaring.

## Yechim (Ruby kodi):
```ruby
to'plam = [10, 18, 12, 17]
natija = to'plam.map { |x| x * 2 }.select { |x| x > 10 }
puts "Natija: #{natija.inspect}"
```

## Tushuntirish va Mantiq:
Ushbu 281-topshiriq Enumerable to'plamlarida filtrlash, xaritalash va tartiblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: [20, 36, 24, 34]
```


# 282-Topshiriq: Enumerable ilg'or amaliyoti #32
## Topshiriq sharti:
Katta ma'lumotlar to'plamida 282-maxsus statistik va funksional saralash amalini bajaring.

## Yechim (Ruby kodi):
```ruby
to'plam = [13, 4, 19, 28]
natija = to'plam.map { |x| x * 2 }.select { |x| x > 10 }
puts "Natija: #{natija.inspect}"
```

## Tushuntirish va Mantiq:
Ushbu 282-topshiriq Enumerable to'plamlarida filtrlash, xaritalash va tartiblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: [26, 38, 56]
```


# 283-Topshiriq: Enumerable ilg'or amaliyoti #33
## Topshiriq sharti:
Katta ma'lumotlar to'plamida 283-maxsus statistik va funksional saralash amalini bajaring.

## Yechim (Ruby kodi):
```ruby
to'plam = [16, 9, 3, 10]
natija = to'plam.map { |x| x * 2 }.select { |x| x > 10 }
puts "Natija: #{natija.inspect}"
```

## Tushuntirish va Mantiq:
Ushbu 283-topshiriq Enumerable to'plamlarida filtrlash, xaritalash va tartiblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: [32, 18, 20]
```


# 284-Topshiriq: Enumerable ilg'or amaliyoti #34
## Topshiriq sharti:
Katta ma'lumotlar to'plamida 284-maxsus statistik va funksional saralash amalini bajaring.

## Yechim (Ruby kodi):
```ruby
to'plam = [2, 14, 10, 21]
natija = to'plam.map { |x| x * 2 }.select { |x| x > 10 }
puts "Natija: #{natija.inspect}"
```

## Tushuntirish va Mantiq:
Ushbu 284-topshiriq Enumerable to'plamlarida filtrlash, xaritalash va tartiblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: [28, 20, 42]
```


# 285-Topshiriq: Enumerable ilg'or amaliyoti #35
## Topshiriq sharti:
Katta ma'lumotlar to'plamida 285-maxsus statistik va funksional saralash amalini bajaring.

## Yechim (Ruby kodi):
```ruby
to'plam = [5, 0, 17, 3]
natija = to'plam.map { |x| x * 2 }.select { |x| x > 10 }
puts "Natija: #{natija.inspect}"
```

## Tushuntirish va Mantiq:
Ushbu 285-topshiriq Enumerable to'plamlarida filtrlash, xaritalash va tartiblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: [34]
```


# 286-Topshiriq: Enumerable ilg'or amaliyoti #36
## Topshiriq sharti:
Katta ma'lumotlar to'plamida 286-maxsus statistik va funksional saralash amalini bajaring.

## Yechim (Ruby kodi):
```ruby
to'plam = [8, 5, 1, 14]
natija = to'plam.map { |x| x * 2 }.select { |x| x > 10 }
puts "Natija: #{natija.inspect}"
```

## Tushuntirish va Mantiq:
Ushbu 286-topshiriq Enumerable to'plamlarida filtrlash, xaritalash va tartiblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: [16, 28]
```


# 287-Topshiriq: Enumerable ilg'or amaliyoti #37
## Topshiriq sharti:
Katta ma'lumotlar to'plamida 287-maxsus statistik va funksional saralash amalini bajaring.

## Yechim (Ruby kodi):
```ruby
to'plam = [11, 10, 8, 25]
natija = to'plam.map { |x| x * 2 }.select { |x| x > 10 }
puts "Natija: #{natija.inspect}"
```

## Tushuntirish va Mantiq:
Ushbu 287-topshiriq Enumerable to'plamlarida filtrlash, xaritalash va tartiblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: [22, 20, 16, 50]
```


# 288-Topshiriq: Enumerable ilg'or amaliyoti #38
## Topshiriq sharti:
Katta ma'lumotlar to'plamida 288-maxsus statistik va funksional saralash amalini bajaring.

## Yechim (Ruby kodi):
```ruby
to'plam = [14, 15, 15, 7]
natija = to'plam.map { |x| x * 2 }.select { |x| x > 10 }
puts "Natija: #{natija.inspect}"
```

## Tushuntirish va Mantiq:
Ushbu 288-topshiriq Enumerable to'plamlarida filtrlash, xaritalash va tartiblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: [28, 30, 30, 14]
```


# 289-Topshiriq: Enumerable ilg'or amaliyoti #39
## Topshiriq sharti:
Katta ma'lumotlar to'plamida 289-maxsus statistik va funksional saralash amalini bajaring.

## Yechim (Ruby kodi):
```ruby
to'plam = [0, 1, 22, 18]
natija = to'plam.map { |x| x * 2 }.select { |x| x > 10 }
puts "Natija: #{natija.inspect}"
```

## Tushuntirish va Mantiq:
Ushbu 289-topshiriq Enumerable to'plamlarida filtrlash, xaritalash va tartiblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: [44, 36]
```


# 290-Topshiriq: Enumerable ilg'or amaliyoti #40
## Topshiriq sharti:
Katta ma'lumotlar to'plamida 290-maxsus statistik va funksional saralash amalini bajaring.

## Yechim (Ruby kodi):
```ruby
to'plam = [3, 6, 6, 0]
natija = to'plam.map { |x| x * 2 }.select { |x| x > 10 }
puts "Natija: #{natija.inspect}"
```

## Tushuntirish va Mantiq:
Ushbu 290-topshiriq Enumerable to'plamlarida filtrlash, xaritalash va tartiblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: [12, 12]
```


# 291-Topshiriq: Enumerable ilg'or amaliyoti #41
## Topshiriq sharti:
Katta ma'lumotlar to'plamida 291-maxsus statistik va funksional saralash amalini bajaring.

## Yechim (Ruby kodi):
```ruby
to'plam = [6, 11, 13, 11]
natija = to'plam.map { |x| x * 2 }.select { |x| x > 10 }
puts "Natija: #{natija.inspect}"
```

## Tushuntirish va Mantiq:
Ushbu 291-topshiriq Enumerable to'plamlarida filtrlash, xaritalash va tartiblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: [12, 22, 26, 22]
```


# 292-Topshiriq: Enumerable ilg'or amaliyoti #42
## Topshiriq sharti:
Katta ma'lumotlar to'plamida 292-maxsus statistik va funksional saralash amalini bajaring.

## Yechim (Ruby kodi):
```ruby
to'plam = [9, 16, 20, 22]
natija = to'plam.map { |x| x * 2 }.select { |x| x > 10 }
puts "Natija: #{natija.inspect}"
```

## Tushuntirish va Mantiq:
Ushbu 292-topshiriq Enumerable to'plamlarida filtrlash, xaritalash va tartiblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: [18, 32, 40, 44]
```


# 293-Topshiriq: Enumerable ilg'or amaliyoti #43
## Topshiriq sharti:
Katta ma'lumotlar to'plamida 293-maxsus statistik va funksional saralash amalini bajaring.

## Yechim (Ruby kodi):
```ruby
to'plam = [12, 2, 4, 4]
natija = to'plam.map { |x| x * 2 }.select { |x| x > 10 }
puts "Natija: #{natija.inspect}"
```

## Tushuntirish va Mantiq:
Ushbu 293-topshiriq Enumerable to'plamlarida filtrlash, xaritalash va tartiblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: [24]
```


# 294-Topshiriq: Enumerable ilg'or amaliyoti #44
## Topshiriq sharti:
Katta ma'lumotlar to'plamida 294-maxsus statistik va funksional saralash amalini bajaring.

## Yechim (Ruby kodi):
```ruby
to'plam = [15, 7, 11, 15]
natija = to'plam.map { |x| x * 2 }.select { |x| x > 10 }
puts "Natija: #{natija.inspect}"
```

## Tushuntirish va Mantiq:
Ushbu 294-topshiriq Enumerable to'plamlarida filtrlash, xaritalash va tartiblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: [30, 14, 22, 30]
```


# 295-Topshiriq: Enumerable ilg'or amaliyoti #45
## Topshiriq sharti:
Katta ma'lumotlar to'plamida 295-maxsus statistik va funksional saralash amalini bajaring.

## Yechim (Ruby kodi):
```ruby
to'plam = [1, 12, 18, 26]
natija = to'plam.map { |x| x * 2 }.select { |x| x > 10 }
puts "Natija: #{natija.inspect}"
```

## Tushuntirish va Mantiq:
Ushbu 295-topshiriq Enumerable to'plamlarida filtrlash, xaritalash va tartiblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: [24, 36, 52]
```


# 296-Topshiriq: Enumerable ilg'or amaliyoti #46
## Topshiriq sharti:
Katta ma'lumotlar to'plamida 296-maxsus statistik va funksional saralash amalini bajaring.

## Yechim (Ruby kodi):
```ruby
to'plam = [4, 17, 2, 8]
natija = to'plam.map { |x| x * 2 }.select { |x| x > 10 }
puts "Natija: #{natija.inspect}"
```

## Tushuntirish va Mantiq:
Ushbu 296-topshiriq Enumerable to'plamlarida filtrlash, xaritalash va tartiblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: [34, 16]
```


# 297-Topshiriq: Enumerable ilg'or amaliyoti #47
## Topshiriq sharti:
Katta ma'lumotlar to'plamida 297-maxsus statistik va funksional saralash amalini bajaring.

## Yechim (Ruby kodi):
```ruby
to'plam = [7, 3, 9, 19]
natija = to'plam.map { |x| x * 2 }.select { |x| x > 10 }
puts "Natija: #{natija.inspect}"
```

## Tushuntirish va Mantiq:
Ushbu 297-topshiriq Enumerable to'plamlarida filtrlash, xaritalash va tartiblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: [14, 18, 38]
```


# 298-Topshiriq: Enumerable ilg'or amaliyoti #48
## Topshiriq sharti:
Katta ma'lumotlar to'plamida 298-maxsus statistik va funksional saralash amalini bajaring.

## Yechim (Ruby kodi):
```ruby
to'plam = [10, 8, 16, 1]
natija = to'plam.map { |x| x * 2 }.select { |x| x > 10 }
puts "Natija: #{natija.inspect}"
```

## Tushuntirish va Mantiq:
Ushbu 298-topshiriq Enumerable to'plamlarida filtrlash, xaritalash va tartiblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: [20, 16, 32]
```


# 299-Topshiriq: Enumerable ilg'or amaliyoti #49
## Topshiriq sharti:
Katta ma'lumotlar to'plamida 299-maxsus statistik va funksional saralash amalini bajaring.

## Yechim (Ruby kodi):
```ruby
to'plam = [13, 13, 0, 12]
natija = to'plam.map { |x| x * 2 }.select { |x| x > 10 }
puts "Natija: #{natija.inspect}"
```

## Tushuntirish va Mantiq:
Ushbu 299-topshiriq Enumerable to'plamlarida filtrlash, xaritalash va tartiblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: [26, 26, 24]
```


# 300-Topshiriq: Enumerable ilg'or amaliyoti #50
## Topshiriq sharti:
Katta ma'lumotlar to'plamida 300-maxsus statistik va funksional saralash amalini bajaring.

## Yechim (Ruby kodi):
```ruby
to'plam = [16, 18, 7, 23]
natija = to'plam.map { |x| x * 2 }.select { |x| x > 10 }
puts "Natija: #{natija.inspect}"
```

## Tushuntirish va Mantiq:
Ushbu 300-topshiriq Enumerable to'plamlarida filtrlash, xaritalash va tartiblash qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija: [32, 36, 14, 46]
```

