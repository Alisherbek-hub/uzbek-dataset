# -*- coding: utf-8 -*-
import sys, os
gen_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\ruby\_generators"
sys.path.append(gen_dir)
from gen_helper import register_topic

TASKS_03 = [
    (
        101,
        "Oddiy if sharti va end bloki",
        "Foydalanuvchi balansi tekshirilib, agar 0 dan katta bo'lsa xabar chiqaruvchi shartli blok yozing.",
        """balans = 45000
if balans > 0
  puts "Sizning balansingiz ijobiy: #{balans} so'm"
end
""",
        "Ruby-da 'if' shartli operatori shart rost (truthy) bo'lgan taqdirda 'end' gacha bo'lgan kod blokini bajaradi. Qavslar qo'yish majburiy emas.",
        """Sizning balansingiz ijobiy: 45000 so'm"""
    ),
    (
        102,
        "if ... else konstruksiyasi",
        "Foydalanuvchining yoshi 18 dan katta yoki tengligiga qarab ovoz berish huquqini aniqlang.",
        """yosh = 17
if yosh >= 18
  puts "Siz ovoz berish huquqiga egasiz."
else
  puts "Kechirasiz, siz hali voyaga yetmagansiz. Qolgan yillar: #{18 - yosh}"
end
""",
        "'if ... else' shart rost bo'lmaganda 'else' tarmog'idagi muqobil ko'rsatmalarni bajarish imkonini beradi.",
        """Kechirasiz, siz hali voyaga yetmagansiz. Qolgan yillar: 1"""
    ),
    (
        103,
        "if ... elsif ... else ko'p tarmoqli shart",
        "Talabaning to'plagan foiziga qarab uning akademik bahosini (A, B, C, D, F) belgilang.",
        """ball = 82

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
""",
        "Ruby-da ko'p shartli tekshiruvlar uchun 'elsif' (e'tibor bering: 'else if' yoki 'elif' emas, aynan 'elsif') kalit so'zi qo'llaniladi.",
        """Talaba natijasi: 82% -> Baho: B (Yaxshi)"""
    ),
    (
        104,
        "Qator oxiridagi shart (Modifier if)",
        "Dasturiy jurnalga (log) faqat debug rejimi yoqilgan bo'lsa xabar yozuvchi bir qatorli if yozing.",
        """debug_rejim = true
puts "[DEBUG] Tizim xotirasi tekshirilmoqda..." if debug_rejim
""",
        "Ruby sintaksisining go'zalliklaridan biri 'Statement Modifier' bo'lib, harakatni shartdan oldin bitta qatorda yozishga imkon beradi (`kod if shart`). Bu kodni ixcham va ravon qiladi.",
        """[DEBUG] Tizim xotirasi tekshirilmoqda..."""
    ),
    (
        105,
        "unless operatori (inkor shart)",
        "Foydalanuvchi tizimda bloklanmagan bo'lsagina ma'lumotlarni ko'rsating.",
        """bloklangan = false

unless bloklangan
  puts "Xush kelibsiz! Shaxsiy kabinetga kirish muvaffaqiyatli."
end
""",
        "'unless' kalit so'zi 'if not' (agar shunday bo'lmasa) degan ma'noni bildiradi. U shart yolg'on (false yoki nil) bo'lganda ishlaydi. Bu 'if !shart' yozishdan ancha toza va tabiiy o'qiladi.",
        """Xush kelibsiz! Shaxsiy kabinetga kirish muvaffaqiyatli."""
    ),
    (
        106,
        "Qator oxiridagi unless (Modifier unless)",
        "To'lov amalga oshirilmagan bo'lsa darhol xizmatni to'xtatuvchi bitta qatorli modifier unless yozing.",
        """tolangan = false
puts "Ogohlantirish: Hisobingizni to'ldiring!" unless tolangan
""",
        "Modifier unless bir qatorda shart yolg'on bo'lganda bajariladigan amallarni qisqa yozish uchun xizmat qiladi.",
        """Ogohlantirish: Hisobingizni to'ldiring!"""
    ),
    (
        107,
        "unless ... else konstruksiyasi",
        "Foydalanuvchi paroli xavfsizlik talablariga javob bermasa ogohlantiring.",
        """parol_kuchsiz = false

unless parol_kuchsiz
  puts "Parol juda kuchli va xavfsiz."
else
  puts "Iltimos, parolingizni murakkablashtiring."
end
""",
        "'unless ... else' ishlatish mumkin, ammo kod tushunarsiz bo'lib qolmasligi uchun odatda 'if ... else' afzal ko'riladi.",
        """Parol juda kuchli va xavfsiz."""
    ),
    (
        108,
        "case ... when selektori va qiymatlarni solishtirish",
        "Hafta kuni raqami bo'yicha uning nomini o'zbek tilida chiqaruvchi case tuzilmasini yarating.",
        """kun_raqami = 3

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
""",
        "Ruby-dagi 'case ... when' boshqa tillardagi switch-case ga o'xshaydi, lekin unda 'break' yozish talab etilmaydi. Mos kelgan birinchi tarmoq bajariladi va blokdan chiqiladi.",
        """3-kun: Chorshanba"""
    ),
    (
        109,
        "case ichida bir nechta qiymat (vergul bilan)",
        "Oy raqamiga qarab faslni (qish, bahor, yoz, kuz) aniqlang.",
        """oy = 7

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
""",
        "'when' dan keyin bir nechta qiymatlarni vergul bilan yozish mumkin. Agar o'zgaruvchi ularning istalgan biriga teng bo'lsa, tarmoq ishga tushadi.",
        """7-oy: Yoz fasli"""
    ),
    (
        110,
        "case ichida Range (oraliqlar) ishlatish",
        "Mijozning yoshiga qarab toifani (chaqaloq, bola, o'smir, katta, keksalar) Range orqali aniqlang.",
        """yosh = 24

toifa = case yosh
when 0..2   then "Chaqaloq"
when 3..12  then "Bola"
when 13..19 then "O'smir"
when 20..59 then "Katta yoshli fuqaro"
else "Keksa nuroniy"
end

puts "Yosh: #{yosh} -> Toifa: #{toifa}"
""",
        "Ruby-da 'case' operatori sahna ortida '===' (case equality) operatoridan foydalanadi. Range uchun `(20..59) === yosh` son oraliqda borligini tekshiradi.",
        """Yosh: 24 -> Toifa: Katta yoshli fuqaro"""
    ),
    (
        111,
        "case ichida Regex (muntazam ifodalar)",
        "Kiritilgan satrning turini (raqam, telefon raqam, oddiy matn) Regex bilan tekshiring.",
        """kiruvchi = "+998901234567"

turi = case kiruvchi
when /\\A\\+998\\d{9}\\z/
  "O'zbekiston telefon raqami"
when /\\A\\d+\\z/
  "Faqat raqamlardan iborat butun son"
else
  "Oddiy matn"
end

puts "Kiruvchi ma'lumot: #{kiruvchi} -> Turi: #{turi}"
""",
        "Regexp obyekti uchun `regex === satr` amali satrning andozaga mosligini tekshiradi. Bu 'case' ichida kuchli parserlar yaratish imkonini beradi.",
        """Kiruvchi ma'lumot: +998901234567 -> Turi: O'zbekiston telefon raqami"""
    ),
    (
        112,
        "case ichida sinflar (Class) bo'yicha tekshirish",
        "O'zgaruvchining toifasiga qarab mos qayta ishlashni tanlang.",
        """qiymat = 3.1415

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
""",
        "Sinf obyekti uchun `Class === obyekt` amali `obyekt.is_a?(Class)` kabi ishlaydi. Shu tufayli case yordamida polimorfik tiplarni tekshirish mumkin.",
        """Haqiqiy son kiritildi: 3.14"""
    ),
    (
        113,
        "Shartsiz case (Condition-less case)",
        "O'zgaruvchisiz, har bir when tarmog'ida alohida mantiqiy ifoda tekshiriladigan case tuzing.",
        """harorat = 28
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
""",
        "Agar 'case' dan keyin hech qanday o'zgaruvchi ko'rsatilmasa, u 'if ... elsif' zanjirining eng toza va go'zal muqobiliga aylanadi.",
        """Tavsiya: Ajoyib iliq ob-havo, sayr qilish mumkin."""
    ),
    (
        114,
        "case ifoda sifatida (Expression return)",
        "Case blokidan to'g'ridan-to'g'ri qiymat qaytarishni o'zlashtiring.",
        """til = "uz"
salom = case til
        when "uz" then "Salom dunyo!"
        when "en" then "Hello world!"
        when "ru" then "Привет мир!"
        end

puts salom
""",
        "Ruby-da deyarli barcha konstruksiyalar (if, unless, case) ibora (expression) hisoblanadi va qiymat qaytaradi. Ular to'g'ridan-to'g'ri o'zgaruvchiga biriktirilishi mumkin.",
        """Salom dunyo!"""
    ),
    (
        115,
        "Ruby 3.0 Pattern Matching: case ... in asoslari",
        "Ruby 3 dagi zamonaviy pattern matching orqali ma'lumot tuzilmasini solishtiring.",
        """javob = { status: :ok, kod: 200 }

case javob
in { status: :ok, kod: 200 }
  puts "Server muvaffaqiyatli javob berdi (200 OK)"
in { status: :error, kod: 404 }
  puts "Sahifa topilmadi (404 Not Found)"
else
  puts "Noma'lum server javobi"
end
""",
        "Ruby 3.0 da kiritilgan 'case ... in' sintaksisi Pattern Matching imkoniyatini taqdim etadi. U obyektning nafaqat qiymatini, balki shakli va ichki strukturasini chuqur tekshiradi.",
        """Server muvaffaqiyatli javob berdi (200 OK)"""
    ),
    (
        116,
        "Pattern Matching: Massivlar dekonstruksiyasi",
        "Buyruq va parametrlardan iborat massivni pattern matching orqali o'zgaruvchilarga ajrating.",
        """buyruq = ["user", "create", "Alisher"]

case buyruq
in ["user", "create", ism]
  puts "Yangi foydalanuvchi yaratilmoqda: #{ism}"
in ["user", "delete", id]
  puts "Foydalanuvchi o'chirilmoqda: ID = #{id}"
else
  puts "Noma'lum buyruq"
end
""",
        "Massiv dekonstruksiyasida `in [a, b, c]` andozasi mos kelsa, andozadagi o'zgaruvchilar (ism, id) avtomatik qiymatlarni o'ziga oladi (binding).",
        """Yangi foydalanuvchi yaratilmoqda: Alisher"""
    ),
    (
        117,
        "Pattern Matching: Hash dekonstruksiyasi",
        "API dan kelgan JSON ma'lumotining kalitlarini va qiymatlarini pattern matching bilan ushlang.",
        """foydalanuvchi = { id: 101, rol: "admin", ism: "Rustam" }

case foydalanuvchi
in { id:, rol: "admin", ism: }
  puts "Administrator tizimga kirdi: #{ism} (ID: #{id})"
in { rol: "mehmon" }
  puts "Mehmon tashrif buyurdi."
end
""",
        "Hash dekonstruksiyasida `{ id:, ism: }` sintaksisi o'sha nomli kalitlarning qiymatlarini avtomatik bir xil nomli lokal o'zgaruvchilarga biriktiradi.",
        """Administrator tizimga kirdi: Rustam (ID: 101)"""
    ),
    (
        118,
        "Pattern Matching shartli qo'shimchasi (Guard if/unless)",
        "Pattern matching mosligiga qo'shimcha mantiqiy shart qo'shing.",
        """mahsulot = { nom: "Smartfon", narx: 450 }

case mahsulot
in { nom:, narx: } if narx > 500
  puts "Qimmatbaho mahsulot: #{nom} ($#{narx})"
in { nom:, narx: }
  puts "Hamyonbop mahsulot: #{nom} ($#{narx})"
end
""",
        "Pattern matching tarmog'i oxiriga `if` yoki `unless` sharti (Guard clause) qo'shilishi mumkin. Andoza mos kelsa ham, faqat guard sharti rost bo'lsagina ushbu tarmoq tanlanadi.",
        """Hamyonbop mahsulot: Smartfon ($450)"""
    ),
    (
        119,
        "while sikli: shart rost bo'lguncha takrorlash",
        "Hisoblagichni 1 dan 5 gacha oshirib ekranga chiqaring.",
        """i = 1
while i <= 5
  puts "Qadam: #{i}"
  i += 1
end
""",
        "'while shart' berilgan shart rost bo'lib turguncha kod blokini qayta-qayta bajaradi.",
        """Qadam: 1
Qadam: 2
Qadam: 3
Qadam: 4
Qadam: 5"""
    ),
    (
        120,
        "Modifier while (qator oxiridagi while)",
        "Massivdan elementlarni bittalab sug'urib chiqaruvchi bir qatorli modifier while yozing.",
        """navbat = ["Mijoz 1", "Mijoz 2", "Mijoz 3"]
puts "Xizmat ko'rsatildi: #{navbat.shift}" while !navbat.empty?
""",
        "Modifier while bitta qatorda siklni qisqa yozish imkonini beradi (`harakat while shart`).",
        """Xizmat ko'rsatildi: Mijoz 1
Xizmat ko'rsatildi: Mijoz 2
Xizmat ko'rsatildi: Mijoz 3"""
    ),
    (
        121,
        "until sikli: shart yolg'on bo'lguncha takrorlash",
        "Suv sathi 100 litrga yetguncha bakni to'ldiruvchi until siklini tuzing.",
        """suv = 20
until suv >= 100
  suv += 30
  puts "Joriy suv hajmi: #{suv} litr"
end
""",
        "'until shart' 'while !shart' ning muqobili bo'lib, ko'rsatilgan shart to'g'ri bo'lgunga qadar bajariladi.",
        """Joriy suv hajmi: 50 litr
Joriy suv hajmi: 80 litr
Joriy suv hajmi: 110 litr"""
    ),
    (
        122,
        "Modifier until",
        "Son 1 dan kichik bo'lguncha uni ikkiga bo'lib boruvchi bir qatorli until tuzing.",
        """son = 16
son /= 2 until son <= 2
puts "Yakuniy son: #{son}"
""",
        "Modifier until qator oxirida shart bajarilguncha chap tarafdagi amaliyotni takrorlaydi.",
        """Yakuniy son: 2"""
    ),
    (
        123,
        "Cheksiz sikl: loop do ... end",
        "Kernel#loop metodi orqali xavfsiz cheksiz sikl yarating va unga chiqish shartini qo'ying.",
        """soni = 0
loop do
  soni += 1
  puts "Sikl takrori: #{soni}"
  break if soni >= 3
end
""",
        "'loop' Ruby-dagi eng sof sikl mexanizmi bo'lib, shartsiz cheksiz aylanadi. Undan chiqish uchun 'break' buyrug'i ishlatiladi.",
        """Sikl takrori: 1
Sikl takrori: 2
Sikl takrori: 3"""
    ),
    (
        124,
        "Sikldan muddatidan oldin chiqish: break",
        "Raqamlar ro'yxatidan manfiy son uchraganda qidiruvni darhol to'xtating.",
        """sonlar = [12, 45, 67, -3, 89, 90]

sonlar.each do |s|
  if s < 0
    puts "Manfiy son topildi: #{s}. Qidiruv to'xtatildi!"
    break
  end
  puts "Qayta ishlandi: #{s}"
end
""",
        "'break' sikl bajarilishini darhol to'xtatadi va sikldan keyingi qatorga o'tadi.",
        """Qayta ishlandi: 12
Qayta ishlandi: 45
Qayta ishlandi: 67
Manfiy son topildi: -3. Qidiruv to'xtatildi!"""
    ),
    (
        125,
        "Keyingi iteratsiyaga o'tish: next",
        "1 dan 10 gacha bo'lgan sonlar orasidan toq sonlarni tashlab o'tib, faqat juftlarini chiqaring.",
        """(1..6).each do |s|
  next if s.odd?
  puts "Juft son: #{s}"
end
""",
        "'next' operatori (boshqa tillardagi 'continue') joriy iteratsiyaning qolgan qismini bajarmasdan, darhol keyingi iteratsiyaga o'tadi.",
        """Juft son: 2
Juft son: 4
Juft son: 6"""
    ),
    (
        126,
        "Iteratsiyani boshidan qaytarish: redo",
        "Tasodifiy shart bo'yicha joriy qadamni hisoblagichni oshirmasdan qayta bajaring.",
        """urinish = 0
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
""",
        "'redo' sikl shartini tekshirmasdan va yangi elementga o'tmasdan, aynan joriy iteratsiyani boshidan qayta ishga tushiradi. Tarmoq xatolarini qayta urinishda (retry) juda qo'l keladi.",
        """Urinish: 1
redo chaqirilmoqda...
Urinish: 2"""
    ),
    (
        127,
        "break bilan sikldan qiymat qaytarish",
        "Sikl yakunida 'break' orqali topilgan natijani to'g'ridan-to'g'ri o'zgaruvchiga oling.",
        """topilgan = (1..100).each do |n|
  break n if n % 7 == 0 && n % 5 == 0
end

puts "7 va 5 ga bo'linadigan birinchi musbat son: #{topilgan}"
""",
        "Ruby-da 'break qiymat' ifodasi siklni to'xtatish bilan birga, butun sikl blokining qaytaradigan natijasi sifatida berilgan qiymatni taqdim etadi.",
        """7 va 5 ga bo'linadigan birinchi musbat son: 35"""
    ),
    (
        128,
        "times iteratori",
        "Bajarilishi kerak bo'lgan vazifani aniq 4 marta takrorlang.",
        """4.times do
  puts "Salom Khorazmiy AI!"
end
""",
        "Integer sinfining 'times' metodi eng qulay sikllardan biri bo'lib, son miqdoricha marta berilgan kod blokini ishga tushiradi.",
        """Salom Khorazmiy AI!
Salom Khorazmiy AI!
Salom Khorazmiy AI!
Salom Khorazmiy AI!"""
    ),
    (
        129,
        "times iteratori bilan indeks parametrini olish",
        "0 dan boshlanuvchi indeks bilan qadamlarni chiqaring.",
        """3.times do |indeks|
  puts "Iteratsiya indeksi: #{indeks}"
end
""",
        "'times' metodi blok parametriga 0 dan boshlab joriy takrorlanish tartib raqamini uzatadi.",
        """Iteratsiya indeksi: 0
Iteratsiya indeksi: 1
Iteratsiya indeksi: 2"""
    ),
    (
        130,
        "upto iteratori: pastdan yuqoriga qarab sanash",
        "10 dan 14 gacha bo'lgan sonlarni upto orqali chiqaring.",
        """10.upto(13) do |son|
  puts "Son: #{son}"
end
""",
        "'son.upto(limit)' ko'rsatilgan limitgacha 1 tadan qo'shib blokni chaqiradi.",
        """Son: 10
Son: 11
Son: 12
Son: 13"""
    ),
    (
        131,
        "downto iteratori: ortga sanash (Countdown)",
        "Raketa uchirilishi oldidan 3 dan 1 gacha ortga sanang.",
        """3.downto(1) do |son|
  puts "#{son}..."
end
puts "Start! Raketa uchirildi!"
""",
        "'son.downto(limit)' boshlang'ich sondan limitgacha kamayib boruvchi siklni bajaradi.",
        """3...
2...
1...
Start! Raketa uchirildi!"""
    ),
    (
        132,
        "step iteratori bilan sakrash",
        "0 dan 10 gacha juft sonlarni 2 qadam bilan chop eting.",
        """0.step(6, 2) do |son|
  puts "Juft qadam: #{son}"
end
""",
        "'son.step(limit, qadam)' berilgan qadam bo'yicha sakrab hisoblaydi.",
        """Juft qadam: 0
Juft qadam: 2
Juft qadam: 4
Juft qadam: 6"""
    ),
    (
        133,
        "for ... in sikli va uning ko'rinish sohasi (Scope)",
        "for sikli va each metodi o'rtasidagi o'zgaruvchi ko'rinish sohasi (scope) farqini ko'rsating.",
        """for element in [1, 2, 3]
  yashirin = element * 10
end
# for siklida e'lon qilingan o'zgaruvchilar tashqarida ham yashaydi
puts "for dan keyin yashirin o'zgaruvchi: #{yashirin}"
""",
        "Ruby-da 'for x in to'plam' sintaksisi yangi ko'rinish sohasi (scope) yaratmaydi, undagi o'zgaruvchilar tashqarida ham saqlanib qoladi. Shu sababli Ruby jamoasi har doim 'each' metodidan foydalanishni tavsiya qiladi.",
        """for dan keyin yashirin o'zgaruvchi: 30"""
    ),
    (
        134,
        "Ichma-ich (Nested) sikllar va koordinatalar katagi",
        "2x3 o'lchamli katak koordinatalarini ichma-ich sikl bilan hosil qiling.",
        """(1..2).each do |qator|
  (1..3).each do |ustun|
    print "[#{qator},#{ustun}] "
  end
  puts ""
end
""",
        "Ichma-ich sikllar matritsalar, panellar va ko'p o'lchovli koordinatalarni aylanib chiqishda qo'llaniladi.",
        """[1,1] [1,2] [1,3] \n[2,1] [2,2] [2,3]"""
    ),
    (
        135,
        "Ichma-ich sikllardan break orqali chiqish chegarasi",
        "Ichki sikldagi break faqat ichki siklni to'xtatishini ko'rsating.",
        """(1..2).each do |tashqi|
  puts "Tashqi: #{tashqi}"
  (1..5).each do |ichki|
    if ichki == 2
      puts "  Ichki to'xtatildi (break)"
      break
    end
    puts "  Ichki: #{ichki}"
  end
end
""",
        "Oddiy 'break' faqat o'zi joylashgan eng yaqin ichki siklni to'xtatadi, tashqi sikl o'z ishini davom ettiradi.",
        """Tashqi: 1
  Ichki: 1
  Ichki to'xtatildi (break)
Tashqi: 2
  Ichki: 1
  Ichki to'xtatildi (break)"""
    ),
    (
        136,
        "catch va throw orqali chuqur qatlamlardan bir zumda chiqish",
        "Ko'p qavatli ichma-ich sikllardan bitta throw buyrug'i bilan eng tashqariga sakrab chiqing.",
        """natija = catch(:topildi) do
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
""",
        "Ruby-da 'catch' va 'throw' istisnolar (Exceptions) emas, balki chuqur o'ralgan kod bloklaridan zudlik bilan chiqish va kerakli qiymatni qaytarish uchun mo'ljallangan tejamkor boshqaruv oqimi vositasidir.",
        """Mos juftlik topildi: x=6, y=7"""
    ),
    (
        137,
        "Falsy qiymatlar: faqat nil va false",
        "Ruby-da faqat nil va false shartda yolg'on hisoblanishini ko'rsating.",
        """def tekshir(qiymat)
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
""",
        "C, Python yoki JavaScript-dan farqli o'laroq, Ruby-da 0 soni, bo'sh satr \"\" va bo'sh massiv [] ham to'liq ROST (Truthy) hisoblanadi. Faqat ikkita narsa: 'false' va 'nil' yolg'on hisoblanadi.",
        """false -> YOLG'ON (Falsy)
nil -> YOLG'ON (Falsy)
0 -> ROST (Truthy)
"" -> ROST (Truthy)
[] -> ROST (Truthy)"""
    ),
    (
        138,
        "Mantiqiy qisqa tutashuv (Short-circuit evaluation)",
        "Birinchi shart yetarli bo'lganda ikkinchi funksiya chaqirilmasligini isbotlang.",
        """def xavfli_metod
  puts "XAVFLI METOD CHAQIRILDI!"
  true
end

# Chap taraf false bo'lgani uchun && o'ng tarafni umuman bajarmaydi
false && xavfli_metod
puts "&& amali yakunlandi (metod chaqirilmadi)."

# Chap taraf true bo'lgani uchun || o'ng tarafni umuman bajarmaydi
true || xavfli_metod
puts "|| amali yakunlandi (metod chaqirilmadi)."
""",
        "Short-circuit evaluation mantiqiy ifodalarda ortiqcha hisob-kitoblar va xatolarning (masalan nil.metod) oldini oladi.",
        """&& amali yakunlandi (metod chaqirilmadi).
|| amali yakunlandi (metod chaqirilmadi)."""
    ),
    (
        139,
        "Shartli operatorlarda tasodifiy biriktirish xatosi",
        "Solishtirish (==) o'rniga biriktirish (=) yozilganda Ruby qanday ogohlantirish berishini ko'ring.",
        """x = 10
# if x = 20 qilsak, biriktirish yuz beradi va doim true bo'ladi
if x == 20
  puts "Teng"
else
  puts "Teng emas: x ning haqiqiy qiymati #{x}"
end
""",
        "Ruby kompilyatori `if x = 20` kabi kodlarda 'warning: found = in conditional, should be ==' ogohlantirishini beradi.",
        """Teng emas: x ning haqiqiy qiymati 10"""
    ),
    (
        140,
        "Fibonachchi sonlarini while sikli bilan hisoblash",
        "Dastlabki 8 ta Fibonachchi sonlarini hisoblang.",
        """n = 8
fibo = [0, 1]
while fibo.length < n
  fibo << fibo[-1] + fibo[-2]
end

puts "Dastlabki #{n} ta Fibonachchi soni: #{fibo.inspect}"
""",
        "Fibonachchi qatorida har bir yangi son o'zidan oldingi ikkita sonning yig'indisiga teng.",
        """Dastlabki 8 ta Fibonachchi soni: [0, 1, 1, 2, 3, 5, 8, 13]"""
    ),
    (
        141,
        "Tub sonlarni tekshirish algoritmi",
        "Berilgan son tub (faqat 1 ga va o'ziga bo'linadigan) ekanligini sikl orqali aniqlang.",
        """def tub_sonmi?(son)
  return false if son <= 1
  (2..Math.sqrt(son)).each do |i|
    return false if son % i == 0
  end
  true
end

puts "17 tub sonmi? #{tub_sonmi?(17)}"
puts "24 tub sonmi? #{tub_sonmi?(24)}"
""",
        "Sonning kvadrat ildizigacha bo'lgan sonlarga bo'lib ko'rish eng tejamkor tublik tekshiruvlaridan biridir.",
        """17 tub sonmi? true
24 tub sonmi? false"""
    ),
    (
        142,
        "Raqamlar yig'indisini hisoblovchi sikl",
        "Berilgan butun sonning raqamlari yig'indisini bo'lish va qoldiq olish orqali hisoblang.",
        """son = 4857
yigindi = 0
vaqtinchalik = son

while vaqtinchalik > 0
  raqam = vaqtinchalik % 10
  yigindi += raqam
  vaqtinchalik /= 10
end

puts "#{son} sonining raqamlari yig'indisi: #{yigindi}"
""",
        "Har bir qadamda 10 ga bo'lib qoldiq olish oxirgi raqamni ajratadi.",
        """4857 sonining raqamlari yig'indisi: 24"""
    ),
    (
        143,
        "Sonning barcha bo'luvchilarini topish",
        "Berilgan sonning barcha qoldiqsiz bo'luvchilarini massivga yig'ing.",
        """son = 36
boluvchilar = []

1.upto(son) do |i|
  boluvchilar << i if son % i == 0
end

puts "#{son} ning bo'luvchilari: #{boluvchilar.inspect}"
""",
        "1 dan songacha bo'lgan sonlar orasidan qoldiqsiz bo'linuvchilar saralanadi.",
        """36 ning bo'luvchilari: [1, 2, 3, 4, 6, 9, 12, 18, 36]"""
    ),
    (
        144,
        "Evklid algoritmi: EKUB (Eng Katta Umumiy Bo'luvchi)",
        "Ikkita sonning EKUBini until sikli orqali toping.",
        """a = 48
b = 18

until b == 0
  a, b = b, a % b
end

puts "EKUB(48, 18) = #{a}"
""",
        "Evklid algoritmi bo'yicha `(a, b) = (b, a % b)` amali `b == 0` bo'lgunga qadar takrorlanadi.",
        """EKUB(48, 18) = 6"""
    ),
    (
        145,
        "Sonni teskari tartibda yozish (Reverse Integer)",
        "12345 sonini arifmetik sikl orqali 54321 ga aylantiring.",
        """asl_son = 12345
teskari = 0
n = asl_son

while n > 0
  teskari = (teskari * 10) + (n % 10)
  n /= 10
end

puts "Asl son: #{asl_son} -> Teskari: #{teskari}"
""",
        "Raqamlarni arifmetik siljitish orqali yangi teskari son shakllantiriladi.",
        """Asl son: 12345 -> Teskari: 54321"""
    ),
    (
        146,
        "Sikllarda bir nechta shartlar: and/or kombinatsiyasi",
        "Foydalanuvchi urinishlari soni va muvaffaqiyat holatini bir vaqtda boshqaring.",
        """urinishlar = 0
muvaffaqiyat = false

while urinishlar < 3 && !muvaffaqiyat
  urinishlar += 1
  puts "Urinish raqami: #{urinishlar}"
  muvaffaqiyat = true if urinishlar == 2
end

puts "Natija: #{muvaffaqiyat ? 'Muvaffaqiyatli' : 'Muvaffaqiyatsiz'}"
""",
        "Bir nechta mantiqiy shartlar bilan sikl oqimi boshqariladi.",
        """Urinish raqami: 1
Urinish raqami: 2
Natija: Muvaffaqiyatli"""
    ),
    (
        147,
        "Shartli operatorlarda ternary zanjiri",
        "Ballga qarab natijani bitta qatorda ternary zanjiri bilan belgilang.",
        """ball = 75
holat = ball >= 86 ? "A'lo" : (ball >= 71 ? "Yaxshi" : "Qoniqarli")

puts "Natija: #{holat}"
""",
        "Ternary operatorlarini ichma-ich zanjir qilish mumkin, biroq murakkab holatlarda case ishlatish tavsiya etiladi.",
        """Natija: Yaxshi"""
    ),
    (
        148,
        "Kvadrat ildiz qidirish (Nyuton-Rafson usuli)",
        "Matematik yaqinlashish usuli bilan sonning ildizini hisoblang.",
        """son = 25.0
taxmin = son / 2.0
aniqlik = 0.0001

while (taxmin * taxmin - son).abs > aniqlik
  taxmin = (taxmin + son / taxmin) / 2.0
end

puts "25 ning taxminiy kvadrat ildizi: #{taxmin.round(4)}"
""",
        "Nyuton algoritmi har bir qadamda qiymatni haqiqiy ildizga yaqinlashtirib boradi.",
        """25 ning taxminiy kvadrat ildizi: 5.0"""
    ),
    (
        149,
        "Shartlarda oraliq tekshiruvi: between? metodi",
        "Harorat normal chegarada ekanligini between? metodi orqali aniqlang.",
        """harorat = 36.6

if harorat.between?(36.0, 37.0)
  puts "Tana harorati me'yorda: #{harorat}C"
else
  puts "Ogohlantirish: Shifokorga murojaat qiling!"
end
""",
        "Comparable modulidagi 'between?(min, max)' metodi son oraliqda borligini tekshiradi.",
        """Tana harorati me'yorda: 36.6C"""
    ),
    (
        150,
        "Amaliy loyiha: Bankomat (ATM) kassa mashinasi va kupyuralar taqsimoti",
        "Mijoz so'ragan naqd pul summasini 100 000, 50 000, 20 000 va 10 000 so'mlik kupyuralarga optimal taqsimlovchi dastur yozing.",
        """yechib_olinadigan_summa = 380_000
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
""",
        "Ushbu amaliy loyihada Ruby 03 mavzusining asosiy shart va sikl mexanizmlari (each, if, divmod va hisoblagichlar) bitta real bankomat tizimi misolida birlashtirildi.",
        """So'ralgan summa: 380000 so'm
Beriladigan kupyuralar:
  - 100000 so'mlik: 3 dona
  - 50000 so'mlik: 1 dona
  - 20000 so'mlik: 1 dona
  - 10000 so'mlik: 1 dona
Tranzaksiya muvaffaqiyatli yakunlandi."""
    )
]

register_topic("gen_03_shartlar.py", "ruby_03_shart_va_takrorlanish_operatorlari.md", 101, TASKS_03)
