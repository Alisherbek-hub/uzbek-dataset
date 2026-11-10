# 101-Topshiriq: Oddiy if sharti va end bloki
## Topshiriq sharti:
Foydalanuvchi balansi tekshirilib, agar 0 dan katta bo'lsa xabar chiqaruvchi shartli blok yozing.

## Yechim (Ruby kodi):
```ruby
balans = 45000
if balans > 0
  puts "Sizning balansingiz ijobiy: #{balans} so'm"
end
```

## Tushuntirish va Mantiq:
Ruby-da 'if' shartli operatori shart rost (truthy) bo'lgan taqdirda 'end' gacha bo'lgan kod blokini bajaradi. Qavslar qo'yish majburiy emas.

## Ishlash natijasi:
```text
Sizning balansingiz ijobiy: 45000 so'm
```


# 102-Topshiriq: if ... else konstruksiyasi
## Topshiriq sharti:
Foydalanuvchining yoshi 18 dan katta yoki tengligiga qarab ovoz berish huquqini aniqlang.

## Yechim (Ruby kodi):
```ruby
yosh = 17
if yosh >= 18
  puts "Siz ovoz berish huquqiga egasiz."
else
  puts "Kechirasiz, siz hali voyaga yetmagansiz. Qolgan yillar: #{18 - yosh}"
end
```

## Tushuntirish va Mantiq:
'if ... else' shart rost bo'lmaganda 'else' tarmog'idagi muqobil ko'rsatmalarni bajarish imkonini beradi.

## Ishlash natijasi:
```text
Kechirasiz, siz hali voyaga yetmagansiz. Qolgan yillar: 1
```


# 103-Topshiriq: if ... elsif ... else ko'p tarmoqli shart
## Topshiriq sharti:
Talabaning to'plagan foiziga qarab uning akademik bahosini (A, B, C, D, F) belgilang.

## Yechim (Ruby kodi):
```ruby
ball = 82

if ball >= 90
  baho = "A (A'lo)"
elsif ball >= 80
  baho = "B (Yaxshi)"
elsif ball >= 70
  baho = "C (Qoniqarli)"
elsif ball >= 60
  baho = "D (Yetarli)"
else
  baho = "F (Qoniqarsiz)"
end

puts "Talaba natijasi: #{ball}% -> Baho: #{baho}"
```

## Tushuntirish va Mantiq:
Ruby-da ko'p shartli tekshiruvlar uchun 'elsif' (e'tibor bering: 'else if' yoki 'elif' emas, aynan 'elsif') kalit so'zi qo'llaniladi.

## Ishlash natijasi:
```text
Talaba natijasi: 82% -> Baho: B (Yaxshi)
```


# 104-Topshiriq: Qator oxiridagi shart (Modifier if)
## Topshiriq sharti:
Dasturiy jurnalga (log) faqat debug rejimi yoqilgan bo'lsa xabar yozuvchi bir qatorli if yozing.

## Yechim (Ruby kodi):
```ruby
debug_rejim = true
puts "[DEBUG] Tizim xotirasi tekshirilmoqda..." if debug_rejim
```

## Tushuntirish va Mantiq:
Ruby sintaksisining go'zalliklaridan biri 'Statement Modifier' bo'lib, harakatni shartdan oldin bitta qatorda yozishga imkon beradi (`kod if shart`). Bu kodni ixcham va ravon qiladi.

## Ishlash natijasi:
```text
[DEBUG] Tizim xotirasi tekshirilmoqda...
```


# 105-Topshiriq: unless operatori (inkor shart)
## Topshiriq sharti:
Foydalanuvchi tizimda bloklanmagan bo'lsagina ma'lumotlarni ko'rsating.

## Yechim (Ruby kodi):
```ruby
bloklangan = false

unless bloklangan
  puts "Xush kelibsiz! Shaxsiy kabinetga kirish muvaffaqiyatli."
end
```

## Tushuntirish va Mantiq:
'unless' kalit so'zi 'if not' (agar shunday bo'lmasa) degan ma'noni bildiradi. U shart yolg'on (false yoki nil) bo'lganda ishlaydi. Bu 'if !shart' yozishdan ancha toza va tabiiy o'qiladi.

## Ishlash natijasi:
```text
Xush kelibsiz! Shaxsiy kabinetga kirish muvaffaqiyatli.
```


# 106-Topshiriq: Qator oxiridagi unless (Modifier unless)
## Topshiriq sharti:
To'lov amalga oshirilmagan bo'lsa darhol xizmatni to'xtatuvchi bitta qatorli modifier unless yozing.

## Yechim (Ruby kodi):
```ruby
tolangan = false
puts "Ogohlantirish: Hisobingizni to'ldiring!" unless tolangan
```

## Tushuntirish va Mantiq:
Modifier unless bir qatorda shart yolg'on bo'lganda bajariladigan amallarni qisqa yozish uchun xizmat qiladi.

## Ishlash natijasi:
```text
Ogohlantirish: Hisobingizni to'ldiring!
```


# 107-Topshiriq: unless ... else konstruksiyasi
## Topshiriq sharti:
Foydalanuvchi paroli xavfsizlik talablariga javob bermasa ogohlantiring.

## Yechim (Ruby kodi):
```ruby
parol_kuchsiz = false

unless parol_kuchsiz
  puts "Parol juda kuchli va xavfsiz."
else
  puts "Iltimos, parolingizni murakkablashtiring."
end
```

## Tushuntirish va Mantiq:
'unless ... else' ishlatish mumkin, ammo kod tushunarsiz bo'lib qolmasligi uchun odatda 'if ... else' afzal ko'riladi.

## Ishlash natijasi:
```text
Parol juda kuchli va xavfsiz.
```


# 108-Topshiriq: case ... when selektori va qiymatlarni solishtirish
## Topshiriq sharti:
Hafta kuni raqami bo'yicha uning nomini o'zbek tilida chiqaruvchi case tuzilmasini yarating.

## Yechim (Ruby kodi):
```ruby
kun_raqami = 3

nom = case kun_raqami
when 1 then "Dushanba"
when 2 then "Seshanba"
when 3 then "Chorshanba"
when 4 then "Payshanba"
when 5 then "Juma"
when 6 then "Shanba"
when 7 then "Yakshanba"
else "Noto'g'ri kun raqami"
end

puts "3-kun: #{nom}"
```

## Tushuntirish va Mantiq:
Ruby-dagi 'case ... when' boshqa tillardagi switch-case ga o'xshaydi, lekin unda 'break' yozish talab etilmaydi. Mos kelgan birinchi tarmoq bajariladi va blokdan chiqiladi.

## Ishlash natijasi:
```text
3-kun: Chorshanba
```


# 109-Topshiriq: case ichida bir nechta qiymat (vergul bilan)
## Topshiriq sharti:
Oy raqamiga qarab faslni (qish, bahor, yoz, kuz) aniqlang.

## Yechim (Ruby kodi):
```ruby
oy = 7

fasl = case oy
when 12, 1, 2
  "Qish"
when 3, 4, 5
  "Bahor"
when 6, 7, 8
  "Yoz"
when 9, 10, 11
  "Kuz"
else
  "Noma'lum oy"
end

puts "#{oy}-oy: #{fasl} fasli"
```

## Tushuntirish va Mantiq:
'when' dan keyin bir nechta qiymatlarni vergul bilan yozish mumkin. Agar o'zgaruvchi ularning istalgan biriga teng bo'lsa, tarmoq ishga tushadi.

## Ishlash natijasi:
```text
7-oy: Yoz fasli
```


# 110-Topshiriq: case ichida Range (oraliqlar) ishlatish
## Topshiriq sharti:
Mijozning yoshiga qarab toifani (chaqaloq, bola, o'smir, katta, keksalar) Range orqali aniqlang.

## Yechim (Ruby kodi):
```ruby
yosh = 24

toifa = case yosh
when 0..2   then "Chaqaloq"
when 3..12  then "Bola"
when 13..19 then "O'smir"
when 20..59 then "Katta yoshli fuqaro"
else "Keksa nuroniy"
end

puts "Yosh: #{yosh} -> Toifa: #{toifa}"
```

## Tushuntirish va Mantiq:
Ruby-da 'case' operatori sahna ortida '===' (case equality) operatoridan foydalanadi. Range uchun `(20..59) === yosh` son oraliqda borligini tekshiradi.

## Ishlash natijasi:
```text
Yosh: 24 -> Toifa: Katta yoshli fuqaro
```


# 111-Topshiriq: case ichida Regex (muntazam ifodalar)
## Topshiriq sharti:
Kiritilgan satrning turini (raqam, telefon raqam, oddiy matn) Regex bilan tekshiring.

## Yechim (Ruby kodi):
```ruby
kiruvchi = "+998901234567"

turi = case kiruvchi
when /\A\+998\d{9}\z/
  "O'zbekiston telefon raqami"
when /\A\d+\z/
  "Faqat raqamlardan iborat butun son"
else
  "Oddiy matn"
end

puts "Kiruvchi ma'lumot: #{kiruvchi} -> Turi: #{turi}"
```

## Tushuntirish va Mantiq:
Regexp obyekti uchun `regex === satr` amali satrning andozaga mosligini tekshiradi. Bu 'case' ichida kuchli parserlar yaratish imkonini beradi.

## Ishlash natijasi:
```text
Kiruvchi ma'lumot: +998901234567 -> Turi: O'zbekiston telefon raqami
```


# 112-Topshiriq: case ichida sinflar (Class) bo'yicha tekshirish
## Topshiriq sharti:
O'zgaruvchining toifasiga qarab mos qayta ishlashni tanlang.

## Yechim (Ruby kodi):
```ruby
qiymat = 3.1415

xabar = case qiymat
when Integer
  "Butun son kiritildi: #{qiymat}"
when Float
  "Haqiqiy son kiritildi: #{qiymat.round(2)}"
when String
  "Matn kiritildi: #{qiymat.upcase}"
else
  "Boshqa toifa: #{qiymat.class}"
end

puts xabar
```

## Tushuntirish va Mantiq:
Sinf obyekti uchun `Class === obyekt` amali `obyekt.is_a?(Class)` kabi ishlaydi. Shu tufayli case yordamida polimorfik tiplarni tekshirish mumkin.

## Ishlash natijasi:
```text
Haqiqiy son kiritildi: 3.14
```


# 113-Topshiriq: Shartsiz case (Condition-less case)
## Topshiriq sharti:
O'zgaruvchisiz, har bir when tarmog'ida alohida mantiqiy ifoda tekshiriladigan case tuzing.

## Yechim (Ruby kodi):
```ruby
harorat = 28
namlik = 65

tavsiya = case
when harorat > 35 && namlik > 70
  "Juda issiq va dim havo, konditsioner yoqing."
when harorat > 25 && namlik <= 70
  "Ajoyib iliq ob-havo, sayr qilish mumkin."
when harorat < 10
  "Sovuq havo, issiq kiyining."
else
  "O'rtacha me'yordagi havo."
end

puts "Tavsiya: #{tavsiya}"
```

## Tushuntirish va Mantiq:
Agar 'case' dan keyin hech qanday o'zgaruvchi ko'rsatilmasa, u 'if ... elsif' zanjirining eng toza va go'zal muqobiliga aylanadi.

## Ishlash natijasi:
```text
Tavsiya: Ajoyib iliq ob-havo, sayr qilish mumkin.
```


# 114-Topshiriq: case ifoda sifatida (Expression return)
## Topshiriq sharti:
Case blokidan to'g'ridan-to'g'ri qiymat qaytarishni o'zlashtiring.

## Yechim (Ruby kodi):
```ruby
til = "uz"
salom = case til
        when "uz" then "Salom dunyo!"
        when "en" then "Hello world!"
        when "ru" then "Привет мир!"
        end

puts salom
```

## Tushuntirish va Mantiq:
Ruby-da deyarli barcha konstruksiyalar (if, unless, case) ibora (expression) hisoblanadi va qiymat qaytaradi. Ular to'g'ridan-to'g'ri o'zgaruvchiga biriktirilishi mumkin.

## Ishlash natijasi:
```text
Salom dunyo!
```


# 115-Topshiriq: Ruby 3.0 Pattern Matching: case ... in asoslari
## Topshiriq sharti:
Ruby 3 dagi zamonaviy pattern matching orqali ma'lumot tuzilmasini solishtiring.

## Yechim (Ruby kodi):
```ruby
javob = { status: :ok, kod: 200 }

case javob
in { status: :ok, kod: 200 }
  puts "Server muvaffaqiyatli javob berdi (200 OK)"
in { status: :error, kod: 404 }
  puts "Sahifa topilmadi (404 Not Found)"
else
  puts "Noma'lum server javobi"
end
```

## Tushuntirish va Mantiq:
Ruby 3.0 da kiritilgan 'case ... in' sintaksisi Pattern Matching imkoniyatini taqdim etadi. U obyektning nafaqat qiymatini, balki shakli va ichki strukturasini chuqur tekshiradi.

## Ishlash natijasi:
```text
Server muvaffaqiyatli javob berdi (200 OK)
```


# 116-Topshiriq: Pattern Matching: Massivlar dekonstruksiyasi
## Topshiriq sharti:
Buyruq va parametrlardan iborat massivni pattern matching orqali o'zgaruvchilarga ajrating.

## Yechim (Ruby kodi):
```ruby
buyruq = ["user", "create", "Alisher"]

case buyruq
in ["user", "create", ism]
  puts "Yangi foydalanuvchi yaratilmoqda: #{ism}"
in ["user", "delete", id]
  puts "Foydalanuvchi o'chirilmoqda: ID = #{id}"
else
  puts "Noma'lum buyruq"
end
```

## Tushuntirish va Mantiq:
Massiv dekonstruksiyasida `in [a, b, c]` andozasi mos kelsa, andozadagi o'zgaruvchilar (ism, id) avtomatik qiymatlarni o'ziga oladi (binding).

## Ishlash natijasi:
```text
Yangi foydalanuvchi yaratilmoqda: Alisher
```


# 117-Topshiriq: Pattern Matching: Hash dekonstruksiyasi
## Topshiriq sharti:
API dan kelgan JSON ma'lumotining kalitlarini va qiymatlarini pattern matching bilan ushlang.

## Yechim (Ruby kodi):
```ruby
foydalanuvchi = { id: 101, rol: "admin", ism: "Rustam" }

case foydalanuvchi
in { id:, rol: "admin", ism: }
  puts "Administrator tizimga kirdi: #{ism} (ID: #{id})"
in { rol: "mehmon" }
  puts "Mehmon tashrif buyurdi."
end
```

## Tushuntirish va Mantiq:
Hash dekonstruksiyasida `{ id:, ism: }` sintaksisi o'sha nomli kalitlarning qiymatlarini avtomatik bir xil nomli lokal o'zgaruvchilarga biriktiradi.

## Ishlash natijasi:
```text
Administrator tizimga kirdi: Rustam (ID: 101)
```


# 118-Topshiriq: Pattern Matching shartli qo'shimchasi (Guard if/unless)
## Topshiriq sharti:
Pattern matching mosligiga qo'shimcha mantiqiy shart qo'shing.

## Yechim (Ruby kodi):
```ruby
mahsulot = { nom: "Smartfon", narx: 450 }

case mahsulot
in { nom:, narx: } if narx > 500
  puts "Qimmatbaho mahsulot: #{nom} ($#{narx})"
in { nom:, narx: }
  puts "Hamyonbop mahsulot: #{nom} ($#{narx})"
end
```

## Tushuntirish va Mantiq:
Pattern matching tarmog'i oxiriga `if` yoki `unless` sharti (Guard clause) qo'shilishi mumkin. Andoza mos kelsa ham, faqat guard sharti rost bo'lsagina ushbu tarmoq tanlanadi.

## Ishlash natijasi:
```text
Hamyonbop mahsulot: Smartfon ($450)
```


# 119-Topshiriq: while sikli: shart rost bo'lguncha takrorlash
## Topshiriq sharti:
Hisoblagichni 1 dan 5 gacha oshirib ekranga chiqaring.

## Yechim (Ruby kodi):
```ruby
i = 1
while i <= 5
  puts "Qadam: #{i}"
  i += 1
end
```

## Tushuntirish va Mantiq:
'while shart' berilgan shart rost bo'lib turguncha kod blokini qayta-qayta bajaradi.

## Ishlash natijasi:
```text
Qadam: 1
Qadam: 2
Qadam: 3
Qadam: 4
Qadam: 5
```


# 120-Topshiriq: Modifier while (qator oxiridagi while)
## Topshiriq sharti:
Massivdan elementlarni bittalab sug'urib chiqaruvchi bir qatorli modifier while yozing.

## Yechim (Ruby kodi):
```ruby
navbat = ["Mijoz 1", "Mijoz 2", "Mijoz 3"]
puts "Xizmat ko'rsatildi: #{navbat.shift}" while !navbat.empty?
```

## Tushuntirish va Mantiq:
Modifier while bitta qatorda siklni qisqa yozish imkonini beradi (`harakat while shart`).

## Ishlash natijasi:
```text
Xizmat ko'rsatildi: Mijoz 1
Xizmat ko'rsatildi: Mijoz 2
Xizmat ko'rsatildi: Mijoz 3
```


# 121-Topshiriq: until sikli: shart yolg'on bo'lguncha takrorlash
## Topshiriq sharti:
Suv sathi 100 litrga yetguncha bakni to'ldiruvchi until siklini tuzing.

## Yechim (Ruby kodi):
```ruby
suv = 20
until suv >= 100
  suv += 30
  puts "Joriy suv hajmi: #{suv} litr"
end
```

## Tushuntirish va Mantiq:
'until shart' 'while !shart' ning muqobili bo'lib, ko'rsatilgan shart to'g'ri bo'lgunga qadar bajariladi.

## Ishlash natijasi:
```text
Joriy suv hajmi: 50 litr
Joriy suv hajmi: 80 litr
Joriy suv hajmi: 110 litr
```


# 122-Topshiriq: Modifier until
## Topshiriq sharti:
Son 1 dan kichik bo'lguncha uni ikkiga bo'lib boruvchi bir qatorli until tuzing.

## Yechim (Ruby kodi):
```ruby
son = 16
son /= 2 until son <= 2
puts "Yakuniy son: #{son}"
```

## Tushuntirish va Mantiq:
Modifier until qator oxirida shart bajarilguncha chap tarafdagi amaliyotni takrorlaydi.

## Ishlash natijasi:
```text
Yakuniy son: 2
```


# 123-Topshiriq: Cheksiz sikl: loop do ... end
## Topshiriq sharti:
Kernel#loop metodi orqali xavfsiz cheksiz sikl yarating va unga chiqish shartini qo'ying.

## Yechim (Ruby kodi):
```ruby
soni = 0
loop do
  soni += 1
  puts "Sikl takrori: #{soni}"
  break if soni >= 3
end
```

## Tushuntirish va Mantiq:
'loop' Ruby-dagi eng sof sikl mexanizmi bo'lib, shartsiz cheksiz aylanadi. Undan chiqish uchun 'break' buyrug'i ishlatiladi.

## Ishlash natijasi:
```text
Sikl takrori: 1
Sikl takrori: 2
Sikl takrori: 3
```


# 124-Topshiriq: Sikldan muddatidan oldin chiqish: break
## Topshiriq sharti:
Raqamlar ro'yxatidan manfiy son uchraganda qidiruvni darhol to'xtating.

## Yechim (Ruby kodi):
```ruby
sonlar = [12, 45, 67, -3, 89, 90]

sonlar.each do |s|
  if s < 0
    puts "Manfiy son topildi: #{s}. Qidiruv to'xtatildi!"
    break
  end
  puts "Qayta ishlandi: #{s}"
end
```

## Tushuntirish va Mantiq:
'break' sikl bajarilishini darhol to'xtatadi va sikldan keyingi qatorga o'tadi.

## Ishlash natijasi:
```text
Qayta ishlandi: 12
Qayta ishlandi: 45
Qayta ishlandi: 67
Manfiy son topildi: -3. Qidiruv to'xtatildi!
```


# 125-Topshiriq: Keyingi iteratsiyaga o'tish: next
## Topshiriq sharti:
1 dan 10 gacha bo'lgan sonlar orasidan toq sonlarni tashlab o'tib, faqat juftlarini chiqaring.

## Yechim (Ruby kodi):
```ruby
(1..6).each do |s|
  next if s.odd?
  puts "Juft son: #{s}"
end
```

## Tushuntirish va Mantiq:
'next' operatori (boshqa tillardagi 'continue') joriy iteratsiyaning qolgan qismini bajarmasdan, darhol keyingi iteratsiyaga o'tadi.

## Ishlash natijasi:
```text
Juft son: 2
Juft son: 4
Juft son: 6
```


# 126-Topshiriq: Iteratsiyani boshidan qaytarish: redo
## Topshiriq sharti:
Tasodifiy shart bo'yicha joriy qadamni hisoblagichni oshirmasdan qayta bajaring.

## Yechim (Ruby kodi):
```ruby
urinish = 0
qayta_bajarildi = false

while urinish < 1
  urinish += 1
  puts "Urinish: #{urinish}"
  if !qayta_bajarildi
    qayta_bajarildi = true
    puts "redo chaqirilmoqda..."
    redo
  end
end
```

## Tushuntirish va Mantiq:
'redo' sikl shartini tekshirmasdan va yangi elementga o'tmasdan, aynan joriy iteratsiyani boshidan qayta ishga tushiradi. Tarmoq xatolarini qayta urinishda (retry) juda qo'l keladi.

## Ishlash natijasi:
```text
Urinish: 1
redo chaqirilmoqda...
Urinish: 2
```


# 127-Topshiriq: break bilan sikldan qiymat qaytarish
## Topshiriq sharti:
Sikl yakunida 'break' orqali topilgan natijani to'g'ridan-to'g'ri o'zgaruvchiga oling.

## Yechim (Ruby kodi):
```ruby
topilgan = (1..100).each do |n|
  break n if n % 7 == 0 && n % 5 == 0
end

puts "7 va 5 ga bo'linadigan birinchi musbat son: #{topilgan}"
```

## Tushuntirish va Mantiq:
Ruby-da 'break qiymat' ifodasi siklni to'xtatish bilan birga, butun sikl blokining qaytaradigan natijasi sifatida berilgan qiymatni taqdim etadi.

## Ishlash natijasi:
```text
7 va 5 ga bo'linadigan birinchi musbat son: 35
```


# 128-Topshiriq: times iteratori
## Topshiriq sharti:
Bajarilishi kerak bo'lgan vazifani aniq 4 marta takrorlang.

## Yechim (Ruby kodi):
```ruby
4.times do
  puts "Salom Khorazmiy AI!"
end
```

## Tushuntirish va Mantiq:
Integer sinfining 'times' metodi eng qulay sikllardan biri bo'lib, son miqdoricha marta berilgan kod blokini ishga tushiradi.

## Ishlash natijasi:
```text
Salom Khorazmiy AI!
Salom Khorazmiy AI!
Salom Khorazmiy AI!
Salom Khorazmiy AI!
```


# 129-Topshiriq: times iteratori bilan indeks parametrini olish
## Topshiriq sharti:
0 dan boshlanuvchi indeks bilan qadamlarni chiqaring.

## Yechim (Ruby kodi):
```ruby
3.times do |indeks|
  puts "Iteratsiya indeksi: #{indeks}"
end
```

## Tushuntirish va Mantiq:
'times' metodi blok parametriga 0 dan boshlab joriy takrorlanish tartib raqamini uzatadi.

## Ishlash natijasi:
```text
Iteratsiya indeksi: 0
Iteratsiya indeksi: 1
Iteratsiya indeksi: 2
```


# 130-Topshiriq: upto iteratori: pastdan yuqoriga qarab sanash
## Topshiriq sharti:
10 dan 14 gacha bo'lgan sonlarni upto orqali chiqaring.

## Yechim (Ruby kodi):
```ruby
10.upto(13) do |son|
  puts "Son: #{son}"
end
```

## Tushuntirish va Mantiq:
'son.upto(limit)' ko'rsatilgan limitgacha 1 tadan qo'shib blokni chaqiradi.

## Ishlash natijasi:
```text
Son: 10
Son: 11
Son: 12
Son: 13
```


# 131-Topshiriq: downto iteratori: ortga sanash (Countdown)
## Topshiriq sharti:
Raketa uchirilishi oldidan 3 dan 1 gacha ortga sanang.

## Yechim (Ruby kodi):
```ruby
3.downto(1) do |son|
  puts "#{son}..."
end
puts "Start! Raketa uchirildi!"
```

## Tushuntirish va Mantiq:
'son.downto(limit)' boshlang'ich sondan limitgacha kamayib boruvchi siklni bajaradi.

## Ishlash natijasi:
```text
3...
2...
1...
Start! Raketa uchirildi!
```


# 132-Topshiriq: step iteratori bilan sakrash
## Topshiriq sharti:
0 dan 10 gacha juft sonlarni 2 qadam bilan chop eting.

## Yechim (Ruby kodi):
```ruby
0.step(6, 2) do |son|
  puts "Juft qadam: #{son}"
end
```

## Tushuntirish va Mantiq:
'son.step(limit, qadam)' berilgan qadam bo'yicha sakrab hisoblaydi.

## Ishlash natijasi:
```text
Juft qadam: 0
Juft qadam: 2
Juft qadam: 4
Juft qadam: 6
```


# 133-Topshiriq: for ... in sikli va uning ko'rinish sohasi (Scope)
## Topshiriq sharti:
for sikli va each metodi o'rtasidagi o'zgaruvchi ko'rinish sohasi (scope) farqini ko'rsating.

## Yechim (Ruby kodi):
```ruby
for element in [1, 2, 3]
  yashirin = element * 10
end
# for siklida e'lon qilingan o'zgaruvchilar tashqarida ham yashaydi
puts "for dan keyin yashirin o'zgaruvchi: #{yashirin}"
```

## Tushuntirish va Mantiq:
Ruby-da 'for x in to'plam' sintaksisi yangi ko'rinish sohasi (scope) yaratmaydi, undagi o'zgaruvchilar tashqarida ham saqlanib qoladi. Shu sababli Ruby jamoasi har doim 'each' metodidan foydalanishni tavsiya qiladi.

## Ishlash natijasi:
```text
for dan keyin yashirin o'zgaruvchi: 30
```


# 134-Topshiriq: Ichma-ich (Nested) sikllar va koordinatalar katagi
## Topshiriq sharti:
2x3 o'lchamli katak koordinatalarini ichma-ich sikl bilan hosil qiling.

## Yechim (Ruby kodi):
```ruby
(1..2).each do |qator|
  (1..3).each do |ustun|
    print "[#{qator},#{ustun}] "
  end
  puts ""
end
```

## Tushuntirish va Mantiq:
Ichma-ich sikllar matritsalar, panellar va ko'p o'lchovli koordinatalarni aylanib chiqishda qo'llaniladi.

## Ishlash natijasi:
```text
[1,1] [1,2] [1,3] 
[2,1] [2,2] [2,3]
```


# 135-Topshiriq: Ichma-ich sikllardan break orqali chiqish chegarasi
## Topshiriq sharti:
Ichki sikldagi break faqat ichki siklni to'xtatishini ko'rsating.

## Yechim (Ruby kodi):
```ruby
(1..2).each do |tashqi|
  puts "Tashqi: #{tashqi}"
  (1..5).each do |ichki|
    if ichki == 2
      puts "  Ichki to'xtatildi (break)"
      break
    end
    puts "  Ichki: #{ichki}"
  end
end
```

## Tushuntirish va Mantiq:
Oddiy 'break' faqat o'zi joylashgan eng yaqin ichki siklni to'xtatadi, tashqi sikl o'z ishini davom ettiradi.

## Ishlash natijasi:
```text
Tashqi: 1
  Ichki: 1
  Ichki to'xtatildi (break)
Tashqi: 2
  Ichki: 1
  Ichki to'xtatildi (break)
```


# 136-Topshiriq: catch va throw orqali chuqur qatlamlardan bir zumda chiqish
## Topshiriq sharti:
Ko'p qavatli ichma-ich sikllardan bitta throw buyrug'i bilan eng tashqariga sakrab chiqing.

## Yechim (Ruby kodi):
```ruby
natija = catch(:topildi) do
  (1..10).each do |x|
    (1..10).each do |y|
      if x * y == 42
        throw(:topildi, "Mos juftlik topildi: x=#{x}, y=#{y}")
      end
    end
  end
  "Hech narsa topilmadi"
end

puts natija
```

## Tushuntirish va Mantiq:
Ruby-da 'catch' va 'throw' istisnolar (Exceptions) emas, balki chuqur o'ralgan kod bloklaridan zudlik bilan chiqish va kerakli qiymatni qaytarish uchun mo'ljallangan tejamkor boshqaruv oqimi vositasidir.

## Ishlash natijasi:
```text
Mos juftlik topildi: x=6, y=7
```


# 137-Topshiriq: Falsy qiymatlar: faqat nil va false
## Topshiriq sharti:
Ruby-da faqat nil va false shartda yolg'on hisoblanishini ko'rsating.

## Yechim (Ruby kodi):
```ruby
def tekshir(qiymat)
  if qiymat
    "#{qiymat.inspect} -> ROST (Truthy)"
  else
    "#{qiymat.inspect} -> YOLG'ON (Falsy)"
  end
end

puts tekshir(false)
puts tekshir(nil)
puts tekshir(0)
puts tekshir("")
puts tekshir([])
```

## Tushuntirish va Mantiq:
C, Python yoki JavaScript-dan farqli o'laroq, Ruby-da 0 soni, bo'sh satr "" va bo'sh massiv [] ham to'liq ROST (Truthy) hisoblanadi. Faqat ikkita narsa: 'false' va 'nil' yolg'on hisoblanadi.

## Ishlash natijasi:
```text
false -> YOLG'ON (Falsy)
nil -> YOLG'ON (Falsy)
0 -> ROST (Truthy)
"" -> ROST (Truthy)
[] -> ROST (Truthy)
```


# 138-Topshiriq: Mantiqiy qisqa tutashuv (Short-circuit evaluation)
## Topshiriq sharti:
Birinchi shart yetarli bo'lganda ikkinchi funksiya chaqirilmasligini isbotlang.

## Yechim (Ruby kodi):
```ruby
def xavfli_metod
  puts "XAVFLI METOD CHAQIRILDI!"
  true
end

# Chap taraf false bo'lgani uchun && o'ng tarafni umuman bajarmaydi
false && xavfli_metod
puts "&& amali yakunlandi (metod chaqirilmadi)."

# Chap taraf true bo'lgani uchun || o'ng tarafni umuman bajarmaydi
true || xavfli_metod
puts "|| amali yakunlandi (metod chaqirilmadi)."
```

## Tushuntirish va Mantiq:
Short-circuit evaluation mantiqiy ifodalarda ortiqcha hisob-kitoblar va xatolarning (masalan nil.metod) oldini oladi.

## Ishlash natijasi:
```text
&& amali yakunlandi (metod chaqirilmadi).
|| amali yakunlandi (metod chaqirilmadi).
```


# 139-Topshiriq: Shartli operatorlarda tasodifiy biriktirish xatosi
## Topshiriq sharti:
Solishtirish (==) o'rniga biriktirish (=) yozilganda Ruby qanday ogohlantirish berishini ko'ring.

## Yechim (Ruby kodi):
```ruby
x = 10
# if x = 20 qilsak, biriktirish yuz beradi va doim true bo'ladi
if x == 20
  puts "Teng"
else
  puts "Teng emas: x ning haqiqiy qiymati #{x}"
end
```

## Tushuntirish va Mantiq:
Ruby kompilyatori `if x = 20` kabi kodlarda 'warning: found = in conditional, should be ==' ogohlantirishini beradi.

## Ishlash natijasi:
```text
Teng emas: x ning haqiqiy qiymati 10
```


# 140-Topshiriq: Fibonachchi sonlarini while sikli bilan hisoblash
## Topshiriq sharti:
Dastlabki 8 ta Fibonachchi sonlarini hisoblang.

## Yechim (Ruby kodi):
```ruby
n = 8
fibo = [0, 1]
while fibo.length < n
  fibo << fibo[-1] + fibo[-2]
end

puts "Dastlabki #{n} ta Fibonachchi soni: #{fibo.inspect}"
```

## Tushuntirish va Mantiq:
Fibonachchi qatorida har bir yangi son o'zidan oldingi ikkita sonning yig'indisiga teng.

## Ishlash natijasi:
```text
Dastlabki 8 ta Fibonachchi soni: [0, 1, 1, 2, 3, 5, 8, 13]
```


# 141-Topshiriq: Tub sonlarni tekshirish algoritmi
## Topshiriq sharti:
Berilgan son tub (faqat 1 ga va o'ziga bo'linadigan) ekanligini sikl orqali aniqlang.

## Yechim (Ruby kodi):
```ruby
def tub_sonmi?(son)
  return false if son <= 1
  (2..Math.sqrt(son)).each do |i|
    return false if son % i == 0
  end
  true
end

puts "17 tub sonmi? #{tub_sonmi?(17)}"
puts "24 tub sonmi? #{tub_sonmi?(24)}"
```

## Tushuntirish va Mantiq:
Sonning kvadrat ildizigacha bo'lgan sonlarga bo'lib ko'rish eng tejamkor tublik tekshiruvlaridan biridir.

## Ishlash natijasi:
```text
17 tub sonmi? true
24 tub sonmi? false
```


# 142-Topshiriq: Raqamlar yig'indisini hisoblovchi sikl
## Topshiriq sharti:
Berilgan butun sonning raqamlari yig'indisini bo'lish va qoldiq olish orqali hisoblang.

## Yechim (Ruby kodi):
```ruby
son = 4857
yigindi = 0
vaqtinchalik = son

while vaqtinchalik > 0
  raqam = vaqtinchalik % 10
  yigindi += raqam
  vaqtinchalik /= 10
end

puts "#{son} sonining raqamlari yig'indisi: #{yigindi}"
```

## Tushuntirish va Mantiq:
Har bir qadamda 10 ga bo'lib qoldiq olish oxirgi raqamni ajratadi.

## Ishlash natijasi:
```text
4857 sonining raqamlari yig'indisi: 24
```


# 143-Topshiriq: Sonning barcha bo'luvchilarini topish
## Topshiriq sharti:
Berilgan sonning barcha qoldiqsiz bo'luvchilarini massivga yig'ing.

## Yechim (Ruby kodi):
```ruby
son = 36
boluvchilar = []

1.upto(son) do |i|
  boluvchilar << i if son % i == 0
end

puts "#{son} ning bo'luvchilari: #{boluvchilar.inspect}"
```

## Tushuntirish va Mantiq:
1 dan songacha bo'lgan sonlar orasidan qoldiqsiz bo'linuvchilar saralanadi.

## Ishlash natijasi:
```text
36 ning bo'luvchilari: [1, 2, 3, 4, 6, 9, 12, 18, 36]
```


# 144-Topshiriq: Evklid algoritmi: EKUB (Eng Katta Umumiy Bo'luvchi)
## Topshiriq sharti:
Ikkita sonning EKUBini until sikli orqali toping.

## Yechim (Ruby kodi):
```ruby
a = 48
b = 18

until b == 0
  a, b = b, a % b
end

puts "EKUB(48, 18) = #{a}"
```

## Tushuntirish va Mantiq:
Evklid algoritmi bo'yicha `(a, b) = (b, a % b)` amali `b == 0` bo'lgunga qadar takrorlanadi.

## Ishlash natijasi:
```text
EKUB(48, 18) = 6
```


# 145-Topshiriq: Sonni teskari tartibda yozish (Reverse Integer)
## Topshiriq sharti:
12345 sonini arifmetik sikl orqali 54321 ga aylantiring.

## Yechim (Ruby kodi):
```ruby
asl_son = 12345
teskari = 0
n = asl_son

while n > 0
  teskari = (teskari * 10) + (n % 10)
  n /= 10
end

puts "Asl son: #{asl_son} -> Teskari: #{teskari}"
```

## Tushuntirish va Mantiq:
Raqamlarni arifmetik siljitish orqali yangi teskari son shakllantiriladi.

## Ishlash natijasi:
```text
Asl son: 12345 -> Teskari: 54321
```


# 146-Topshiriq: Sikllarda bir nechta shartlar: and/or kombinatsiyasi
## Topshiriq sharti:
Foydalanuvchi urinishlari soni va muvaffaqiyat holatini bir vaqtda boshqaring.

## Yechim (Ruby kodi):
```ruby
urinishlar = 0
muvaffaqiyat = false

while urinishlar < 3 && !muvaffaqiyat
  urinishlar += 1
  puts "Urinish raqami: #{urinishlar}"
  muvaffaqiyat = true if urinishlar == 2
end

puts "Natija: #{muvaffaqiyat ? 'Muvaffaqiyatli' : 'Muvaffaqiyatsiz'}"
```

## Tushuntirish va Mantiq:
Bir nechta mantiqiy shartlar bilan sikl oqimi boshqariladi.

## Ishlash natijasi:
```text
Urinish raqami: 1
Urinish raqami: 2
Natija: Muvaffaqiyatli
```


# 147-Topshiriq: Shartli operatorlarda ternary zanjiri
## Topshiriq sharti:
Ballga qarab natijani bitta qatorda ternary zanjiri bilan belgilang.

## Yechim (Ruby kodi):
```ruby
ball = 75
holat = ball >= 86 ? "A'lo" : (ball >= 71 ? "Yaxshi" : "Qoniqarli")

puts "Natija: #{holat}"
```

## Tushuntirish va Mantiq:
Ternary operatorlarini ichma-ich zanjir qilish mumkin, biroq murakkab holatlarda case ishlatish tavsiya etiladi.

## Ishlash natijasi:
```text
Natija: Yaxshi
```


# 148-Topshiriq: Kvadrat ildiz qidirish (Nyuton-Rafson usuli)
## Topshiriq sharti:
Matematik yaqinlashish usuli bilan sonning ildizini hisoblang.

## Yechim (Ruby kodi):
```ruby
son = 25.0
taxmin = son / 2.0
aniqlik = 0.0001

while (taxmin * taxmin - son).abs > aniqlik
  taxmin = (taxmin + son / taxmin) / 2.0
end

puts "25 ning taxminiy kvadrat ildizi: #{taxmin.round(4)}"
```

## Tushuntirish va Mantiq:
Nyuton algoritmi har bir qadamda qiymatni haqiqiy ildizga yaqinlashtirib boradi.

## Ishlash natijasi:
```text
25 ning taxminiy kvadrat ildizi: 5.0
```


# 149-Topshiriq: Shartlarda oraliq tekshiruvi: between? metodi
## Topshiriq sharti:
Harorat normal chegarada ekanligini between? metodi orqali aniqlang.

## Yechim (Ruby kodi):
```ruby
harorat = 36.6

if harorat.between?(36.0, 37.0)
  puts "Tana harorati me'yorda: #{harorat}C"
else
  puts "Ogohlantirish: Shifokorga murojaat qiling!"
end
```

## Tushuntirish va Mantiq:
Comparable modulidagi 'between?(min, max)' metodi son oraliqda borligini tekshiradi.

## Ishlash natijasi:
```text
Tana harorati me'yorda: 36.6C
```


# 150-Topshiriq: Amaliy loyiha: Bankomat (ATM) kassa mashinasi va kupyuralar taqsimoti
## Topshiriq sharti:
Mijoz so'ragan naqd pul summasini 100 000, 50 000, 20 000 va 10 000 so'mlik kupyuralarga optimal taqsimlovchi dastur yozing.

## Yechim (Ruby kodi):
```ruby
yechib_olinadigan_summa = 380_000
kupyuralar = [100_000, 50_000, 20_000, 10_000]

puts "So'ralgan summa: #{yechib_olinadigan_summa} so'm"
puts "Beriladigan kupyuralar:"

qoldiq = yechib_olinadigan_summa
kupyuralar.each do |kupyura|
  if qoldiq >= kupyura
    soni, qoldiq = qoldiq.divmod(kupyura)
    puts "  - #{kupyura} so'mlik: #{soni} dona"
  end
end

if qoldiq == 0
  puts "Tranzaksiya muvaffaqiyatli yakunlandi."
else
  puts "Qoldiq berib bo'lmadi: #{qoldiq} so'm"
end
```

## Tushuntirish va Mantiq:
Ushbu amaliy loyihada Ruby 03 mavzusining asosiy shart va sikl mexanizmlari (each, if, divmod va hisoblagichlar) bitta real bankomat tizimi misolida birlashtirildi.

## Ishlash natijasi:
```text
So'ralgan summa: 380000 so'm
Beriladigan kupyuralar:
  - 100000 so'mlik: 3 dona
  - 50000 so'mlik: 1 dona
  - 20000 so'mlik: 1 dona
  - 10000 so'mlik: 1 dona
Tranzaksiya muvaffaqiyatli yakunlandi.
```

