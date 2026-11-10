# 1-Topshiriq: Ekran bilan muloqot: 'puts', 'print' va 'p' metodlari
## Topshiriq sharti:
Foydalanuvchiga xush kelibsiz xabarini chiqarish, qator tashlamasdan belgi chiqarish va obyektning ichki xom holatini konsolda ko'rish dasturini tuzing.

## Yechim (Ruby kodi):
```ruby
# puts oxirida yangi qator (newline) tashlaydi
puts "Khorazmiy AI loyihasiga xush kelibsiz!"

# print yangi qator tashlamaydi, bir xil qatorda davom ettiradi
print "Yuklanmoqda: "
print "[OK]\n"

# p metodi obyektni inspect qilib, uning ichki tipini ko'rsatadi
matn = "Ruby 3.2"
son = 42
p matn
p son
```

## Tushuntirish va Mantiq:
Ruby-da konsolga ma'lumot chiqarishning uchta asosiy usuli bor: 'puts' satr oxiriga avtomatik yangi qator belgisini qo'shadi; 'print' qator tashlamaydi; 'p' esa obyektning 'inspect' metodini chaqirib, dasturchiga o'zgaruvchining haqiqiy turi va tarkibini tahlil qilish uchun juda qulay debug formatida chiqaradi.

## Ishlash natijasi:
```text
Khorazmiy AI loyihasiga xush kelibsiz!
Yuklanmoqda: [OK]
"Ruby 3.2"
42
```


# 2-Topshiriq: Lokal o'zgaruvchilar va dinamik tiplash
## Topshiriq sharti:
Dasturiy tizim nomi va versiyasini saqlovchi o'zgaruvchilarni e'lon qiling, so'ngra versiya turini butun sondan satrga o'zgartiring.

## Yechim (Ruby kodi):
```ruby
system_name = "Khorazmiy Ruby Engine"
version = 1
puts "Tizim: #{system_name}, Versiya raqami: #{version} (Turi: #{version.class})"

# Dinamik tiplash: o'zgaruvchiga yangi turdagi qiymat biriktiramiz
version = "v1.2.0-stable"
puts "Yangilangan tizim: #{system_name}, Yangi versiya: #{version} (Turi: #{version.class})"
```

## Tushuntirish va Mantiq:
Ruby dinamik tiplangan (dynamically typed) til hisoblanadi. O'zgaruvchilar kichik harf yoki pastki chiziq bilan boshlanadi. Ularning turini oldindan e'lon qilish talab etilmaydi, o'zgaruvchi o'ziga biriktirilgan istalgan qiymat turini qabul qila oladi. '.class' metodi orqali obyektning qaysi sinfga mansubligini bilish mumkin.

## Ishlash natijasi:
```text
Tizim: Khorazmiy Ruby Engine, Versiya raqami: 1 (Turi: Integer)
Yangilangan tizim: Khorazmiy Ruby Engine, Yangi versiya: v1.2.0-stable (Turi: String)
```


# 3-Topshiriq: Butun sonlar (Integer) va asosiy arifmetik amallar
## Topshiriq sharti:
Ikkita butun son ustida qo'shish, ayirish, ko'paytirish, bo'lish va qoldiq olish amallarini bajaring.

## Yechim (Ruby kodi):
```ruby
a = 25
b = 4

yigindi = a + b
ayirma = a - b
kopaytma = a * b
bolinma = a / b
qoldiq = a % b

puts "a = #{a}, b = #{b}"
puts "Qo'shish: #{yigindi}"
puts "Ayirish: #{ayirma}"
puts "Ko'paytirish: #{kopaytma}"
puts "Bo'lish (butun qism): #{bolinma}"
puts "Qoldiq (modul): #{qoldiq}"
```

## Tushuntirish va Mantiq:
Ruby-da butun sonlar 'Integer' sinfi obyekti hisoblanadi. Ikkita butun son bo'linganda natija ham butun qismga yaxlitlanadi (25 / 4 = 6). Qoldiqni topish uchun '%' operatoridan foydalaniladi.

## Ishlash natijasi:
```text
a = 25, b = 4
Qo'shish: 29
Ayirish: 21
Ko'paytirish: 100
Bo'lish (butun qism): 6
Qoldiq (modul): 1
```


# 4-Topshiriq: Haqiqiy sonlar (Float) va aniqlik darajasi
## Topshiriq sharti:
Doiraning radiusi berilganda uning yuzi va aylanasi uzunligini Float toifasidagi PI konstanta yordamida hisoblang.

## Yechim (Ruby kodi):
```ruby
radius = 7.5
pi = 3.141592653589793

doira_yuzi = pi * (radius ** 2)
aylana_uzunligi = 2 * pi * radius

puts "Radius: #{radius}"
puts "Doira yuzi: #{doira_yuzi}"
puts "Aylana uzunligi: #{aylana_uzunligi}"
puts "Yuzning sinfi: #{doira_yuzi.class}"
```

## Tushuntirish va Mantiq:
O'nlik kasrli sonlar 'Float' sinfiga tegishli. Ruby 64-bitli IEEE 754 formatidan foydalanadi. Darajaga ko'tarish uchun '**' operatori ishlatiladi. Natija Float toifasida aniq hisoblanadi.

## Ishlash natijasi:
```text
Radius: 7.5
Doira yuzi: 176.71458676442586
Aylana uzunligi: 47.12388980384689
Yuzning sinfi: Float
```


# 5-Topshiriq: O'zgarmaslar (Constants) va bosh harf qoidasi
## Topshiriq sharti:
Ilovaning server manzili va portini o'zgarmas sifatida e'lon qiling, o'zgarmasni o'zgartirishga uringanda Ruby qanday ogohlantirish (warning) berishini ko'rsating.

## Yechim (Ruby kodi):
```ruby
SERVER_HOST = "api.khorazmiy.uz"
DEFAULT_PORT = 8080

puts "Server: #{SERVER_HOST}:#{DEFAULT_PORT}"

# Ruby-da o'zgarmas qayta aniqlansa, xato emas, warning beriladi
DEFAULT_PORT = 9000
puts "Yangilangan port: #{DEFAULT_PORT}"
```

## Tushuntirish va Mantiq:
Ruby-da bosh harf bilan boshlangan har qanday nom o'zgarmas (Constant) hisoblanadi (masalan, MAX_SIZE, DatabaseConfig). C++ yoki Java-dan farqli o'laroq, Ruby o'zgarmas qayta biriktirilganda dasturni to'xtatmaydi, ammo 'warning: already initialized constant' ogohlantirishini beradi.

## Ishlash natijasi:
```text
Server: api.khorazmiy.uz:8080
Yangilangan port: 9000
```


# 6-Topshiriq: String interpolatsiyasi (#{...}) va maxsus belgilar
## Topshiriq sharti:
Xodimning ismi, yoshi va lavozimini bitta chiroyli matn ichiga String interpolatsiyasi yordamida joylashtiring.

## Yechim (Ruby kodi):
```ruby
xodim_ismi = "Rustam"
yosh = 28
lavozim = "Senior Ruby Muhandis"

# Qo'sh tirnoq ichida #{...} ishlaydi
xabar = "Xodim: #{xodim_ismi.upcase}, Yoshi: #{yosh + 1} (keyingi oy), Lavozimi: #{lavozim}"
puts xabar

# Yagona tirnoq ichida interpolatsiya ishlamaydi
xom_xabar = 'Xodim: #{xodim_ismi}'
puts xom_xabar
```

## Tushuntirish va Mantiq:
String interpolatsiyasi faqat qo'shtirnoq bilan o'ralgan satrlarda ishlaydi. #{...} bloki ichida nafaqat o'zgaruvchi, balki har qanday Ruby ifodasi (masalan, hisob-kitoblar, metod chaqiruvlari) bajarilib, natijasi avtomatik to_s qilinadi. Yakkasimon tirnoq esa matnni xom holatda saqlaydi.

## Ishlash natijasi:
```text
Xodim: RUSTAM, Yoshi: 29 (keyingi oy), Lavozimi: Senior Ruby Muhandis
Xom_xabar: \#{xodim_ismi}
```


# 7-Topshiriq: Mantiqiy qiymatlar: true va false obyektlari
## Topshiriq sharti:
Foydalanuvchi tizimga kirganligi va uning balansi yetarli ekanligini ifodalovchi mantiqiy shartlarni tekshiring.

## Yechim (Ruby kodi):
```ruby
tizimga_kirgan = true
balans_yetarli = false

puts "Kirish holati: #{tizimga_kirgan} (Sinfi: #{tizimga_kirgan.class})"
puts "Balans holati: #{balans_yetarli} (Sinfi: #{balans_yetarli.class})"

# Mantiqiy solishtirish
amal_mumkin = tizimga_kirgan && balans_yetarli
puts "Amalni bajarish mumkinmi? #{amal_mumkin}"
```

## Tushuntirish va Mantiq:
Boshqa ko'plab tillarda 'true' va 'false' oddiy 1 va 0 bo'lsa, Ruby-da ular 'TrueClass' va 'FalseClass' sinflarining to'laqonli yagona (singleton) obyektlaridir. Ruby-da faqat ikkita qiymat 'falsy' hisoblanadi: 'false' va 'nil'. Qolgan hamma narsa (shu jumladan 0, bo'sh satr, bo'sh massiv) 'truthy' hisoblanadi.

## Ishlash natijasi:
```text
Kirish holati: true (Sinfi: TrueClass)
Balans holati: false (Sinfi: FalseClass)
Amalni bajarish mumkinmi? false
```


# 8-Topshiriq: Nil obyekti va uning xususiyatlari
## Topshiriq sharti:
Mavjud bo'lmagan qiymatni ifodalovchi nil obyektini yarating va uni nil?, to_s, to_i metodlari orqali tekshiring.

## Yechim (Ruby kodi):
```ruby
boshlangich_qiymat = nil

puts "Obyekt qiymati: #{boshlangich_qiymat.inspect}"
puts "Obyekt sinfi: #{boshlangich_qiymat.class}"
puts "Bu nil mi? #{boshlangich_qiymat.nil?}"

# nil ning konvertatsiyasi
puts "nil.to_s qiymati: #{boshlangich_qiymat.to_s.inspect}"
puts "nil.to_i qiymati: #{boshlangich_qiymat.to_i}"
puts "nil.to_a qiymati: #{boshlangich_qiymat.to_a.inspect}"
```

## Tushuntirish va Mantiq:
Ruby-da 'nil' qiymat yo'qligini ifodalovchi 'NilClass' sinfining nusxasidir. Boshqa tillardagi null xatoliklariga nisbatan Ruby-dagi nil ko'plab qulay metodlarga ega: masalan, 'nil.to_s' bo'sh satr, 'nil.to_i' 0, 'nil.to_a' bo'sh massiv qaytaradi.

## Ishlash natijasi:
```text
Obyekt qiymati: nil
Obyekt sinfi: NilClass
Bu nil mi? true
nil.to_s qiymati: ""
nil.to_i qiymati: 0
nil.to_a qiymati: []
```


# 9-Topshiriq: Foydalanuvchi kiritmasi: gets va chomp
## Topshiriq sharti:
Standart kiritish oqimidan foydalanuvchi ismini qabul qilib, satr oxiridagi belgilarni tozalovchi simulyatsiya qiling.

## Yechim (Ruby kodi):
```ruby
# gets klaviaturadan satr o'qiydi (oxirida newline bilan)
# chomp esa oxiridagi yangi qator belgisini qirqib tashlaydi
kiritilgan_matn = "Alisher Navoiy\n"

tozalangan_ism = kiritilgan_matn.chomp
puts "Asl uzunlik: #{kiritilgan_matn.length}"
puts "Tozalangan uzunlik: #{tozalangan_ism.length}"
puts "Salom, hurmatli #{tozalangan_ism}!"
```

## Tushuntirish va Mantiq:
Konsoldan o'qishda 'gets' har doim satr oxiridagi Enter tugmasi bosilgan yangi qator belgisini ham qo'shib oladi. 'chomp' metodi satr oxiridagi ortiqcha qator ko'chirish belgisini olib tashlaydi va toza matnni qaytaradi.

## Ishlash natijasi:
```text
Asl uzunlik: 15
Tozalangan uzunlik: 14
Salom, hurmatli Alisher Navoiy!
```


# 10-Topshiriq: Tiplarni o'zgartirish: to_i, to_f va to_s
## Topshiriq sharti:
Satr ko'rinishidagi narx va miqdorni sonlarga aylantirib, umumiy to'lov miqdorini hisoblang.

## Yechim (Ruby kodi):
```ruby
narx_str = "45000.75"
miqdor_str = "3"

narx = narx_str.to_f
miqdor = miqdor_str.to_i
umumiy = narx * miqdor

puts "Narx (Float): #{narx}"
puts "Miqdor (Integer): #{miqdor}"
puts "Umumiy summa: #{umumiy}"
puts "Matn ko'rinishida: #{umumiy.to_s + ' so\'m'}"
```

## Tushuntirish va Mantiq:
Ruby-da aniq tip konvertatsiyasi uchun 'to_i' (butun songa), 'to_f' (haqiqiy songa), 'to_s' (satrga) va 'to_a' (massivga) metodlari mavjud. Agar satr son bilan boshlanmasa, 'to_i' xato tashlamasdan 0 qaytaradi.

## Ishlash natijasi:
```text
Narx (Float): 45000.75
Miqdor (Integer): 3
Umumiy summa: 135002.25
Matn ko'rinishida: 135002.25 so'm
```


# 11-Topshiriq: Parallel biriktirish (Multiple Assignment)
## Topshiriq sharti:
Bitta qatorda uchta o'zgaruvchiga qiymat bering va ortiqcha qiymatlarni massivga qabul qilishni ko'rsating.

## Yechim (Ruby kodi):
```ruby
# Parallel biriktirish
x, y, z = 10, 20, 30
puts "x: #{x}, y: #{y}, z: #{z}"

# Splat operatori (*) bilan ortiqcha elementlarni yig'ish
birinchi, *qolganlar = 1, 2, 3, 4, 5
puts "Birinchi: #{birinchi}"
puts "Qolganlar: #{qolganlar.inspect}"
```

## Tushuntirish va Mantiq:
Ruby-da bir nechta o'zgaruvchilarga vergul orqali bitta qatorda qiymat biriktirish mumkin. Agar o'zgaruvchi oldiga yulduzcha (*) qo'yilsa (splat operatori), u qolgan barcha ortiqcha qiymatlarni o'z ichiga olgan massivga aylanadi.

## Ishlash natijasi:
```text
x: 10, y: 20, z: 30
Birinchi: 1
Qolganlar: [2, 3, 4, 5]
```


# 12-Topshiriq: O'zgaruvchilar qiymatini almashtirish (Swap)
## Topshiriq sharti:
Yordamchi uchinchi o'zgaruvchisiz ikkita o'zgaruvchining qiymatlarini o'zaro almashtiring.

## Yechim (Ruby kodi):
```ruby
a = "Olma"
b = "Anor"
puts "Almashishdan oldin: a = #{a}, b = #{b}"

# Parallel biriktirish orqali o'rin almashtirish
a, b = b, a

puts "Almashishdan keyin: a = #{a}, b = #{b}"
```

## Tushuntirish va Mantiq:
Ruby-da 'a, b = b, a' sintaksisi avval o'ng tomondagi elementlardan vaqtinchalik massiv tuzadi va keyin ularni chap tomondagi o'zgaruvchilarga biriktiradi. Shu sababli qo'shimcha 'temp' o'zgaruvchisiga hojat qolmaydi.

## Ishlash natijasi:
```text
Almashishdan oldin: a = Olma, b = Anor
Almashishdan keyin: a = Anor, b = Olma
```


# 13-Topshiriq: Taqqoslovchi operatorlar
## Topshiriq sharti:
Talabaning to'plagan balli o'tish baliga nisbatan solishtirilishini barcha solishtirish operatorlari yordamida tekshiring.

## Yechim (Ruby kodi):
```ruby
ball = 85
otish_bali = 70

puts "ball == otish_bali: #{ball == otish_bali}"
puts "ball != otish_bali: #{ball != otish_bali}"
puts "ball > otish_bali: #{ball > otish_bali}"
puts "ball < otish_bali: #{ball < otish_bali}"
puts "ball >= otish_bali: #{ball >= otish_bali}"
puts "ball <= otish_bali: #{ball <= otish_bali}"
```

## Tushuntirish va Mantiq:
Ruby taqqoslash operatorlari standart mantiqiy natija (true yoki false) qaytaradi. Ular 'Comparable' moduli orqali sinflarda osonlikcha qayta aniqlanishi mumkin.

## Ishlash natijasi:
```text
ball == otish_bali: false
ball != otish_bali: true
ball > otish_bali: true
ball < otish_bali: false
ball >= otish_bali: true
ball <= otish_bali: false
```


# 14-Topshiriq: Fazoviy kema operatori: <=> (Spaceship operator)
## Topshiriq sharti:
Ikkita sonni solishtirib, chap tomon kichik, teng yoki katta bo'lganda nima qaytishini ko'rsating.

## Yechim (Ruby kodi):
```ruby
puts "5 <=> 10 : #{5 <=> 10}"
puts "10 <=> 10 : #{10 <=> 10}"
puts "20 <=> 10 : #{20 <=> 10}"

# Satrlar solishtiruvi
puts "'olma' <=> 'anor' : #{'olma' <=> 'anor'}"
```

## Tushuntirish va Mantiq:
Spaceship operatori (<=>) Ruby-dagi eng mashhur operatorlardan biridir. Agar chap taraf kichik bo'lsa -1, teng bo'lsa 0, katta bo'lsa 1 qaytaradi. Taqqoslab bo'lmaydigan tiplar uchun esa nil qaytaradi. Ushbu operator 'sort' algoritmining asosi hisoblanadi.

## Ishlash natijasi:
```text
5 <=> 10 : -1
10 <=> 10 : 0
20 <=> 10 : 1
'olma' <=> 'anor' : 1
```


# 15-Topshiriq: Tenglikning uch turi: ==, eql? va equal?
## Topshiriq sharti:
Qiymat tengligi, tip tengligi va xotiradagi manzillar tengligining farqlarini tahlil qiling.

## Yechim (Ruby kodi):
```ruby
a = 5
b = 5.0

# 1. == faqat qiymatni solishtiradi (avtomatik moslashtiradi)
puts "a == b: #{a == b}"

# 2. eql? qiymat va tipning bir xilligini tekshiradi (Hash kalitlari uchun)
puts "a.eql?(b): #{a.eql?(b)}"

# 3. equal? xotiradagi bitta obyekt ekanligini (object_id) tekshiradi
str1 = "Salom"
str2 = "Salom"
puts "str1 == str2: #{str1 == str2}"
puts "str1.equal?(str2): #{str1.equal?(str2)}"
```

## Tushuntirish va Mantiq:
Ruby-da '==' qiymat tengligini tekshiradi; 'eql?' ham qiymat, ham tip mosligini talab qiladi; 'equal?' esa ikkita o'zgaruvchi xotiradagi aynan bitta manzilga (object_id) ishora qilayotganini aniqlaydi.

## Ishlash natijasi:
```text
a == b: true
a.eql?(b): false
str1 == str2: true
str1.equal?(str2): false
```


# 16-Topshiriq: object_id metodi va xotira boshqaruvi
## Topshiriq sharti:
Obyektlarning xotiradagi betakror identifikatorlarini chiqaring va butun sonlar uchun object_id qanday shakllanishini ko'rsating.

## Yechim (Ruby kodi):
```ruby
x = "Khorazmiy"
y = "Khorazmiy"
puts "x object_id mavjudmi: #{x.object_id > 0}"
puts "y object_id mavjudmi: #{y.object_id > 0}"

# Kichik butun sonlar uchun maxsus formula: (son * 2) + 1
puts "0 ning object_id: #{0.object_id}"
puts "1 ning object_id: #{1.object_id}"
puts "2 ning object_id: #{2.object_id}"
puts "true ning object_id: #{true.object_id}"
puts "false ning object_id: #{false.object_id}"
puts "nil ning object_id: #{nil.object_id}"
```

## Tushuntirish va Mantiq:
Har bir Ruby obyekti xotirada unikal 'object_id'ga ega. CRuby-da xotirani tejash maqsadida kichik butun sonlar, true, false va nil to'g'ridan-to'g'ri ko'rsatkich (pointer) ichida saqlanadi (Immediate Values) va ularning ID-si qat'iy matematik formula bo'yicha hisoblanadi.

## Ishlash natijasi:
```text
x object_id mavjudmi: true
y object_id mavjudmi: true
0 ning object_id: 1
1 ning object_id: 3
2 ning object_id: 5
true ning object_id: 20
false ning object_id: 0
nil ning object_id: 8
```


# 17-Topshiriq: Mantiqiy operatorlar: &&, || va !
## Topshiriq sharti:
Foydalanuvchi akkaunti faolligi va to'lov qilinganligini mantiqiy operatorlar yordamida tekshiring.

## Yechim (Ruby kodi):
```ruby
faol = true
tolangan = false
bloklangan = false

ruxsat = faol && tolangan
ogohlantirish = !tolangan
kirish_mumkin = (faol || tolangan) && !bloklangan

puts "To'liq ruxsat (&&): #{ruxsat}"
puts "Ogohlantirish (!): #{ogohlantirish}"
puts "Kirish mumkin: #{kirish_mumkin}"
```

## Tushuntirish va Mantiq:
'&&' (AND) amali barcha shartlar rost bo'lsagina true qaytaradi; '||' (OR) amali kamida bitta shart rost bo'lsa true qaytaradi; '!' (NOT) amali mantiqiy qiymatni teskarisiga aylantiradi.

## Ishlash natijasi:
```text
To'liq ruxsat (&&): false
Ogohlantirish (!): true
Kirish mumkin: true
```


# 18-Topshiriq: So'zli mantiqiy operatorlar: and, or va ularning prioriteti
## Topshiriq sharti:
Nega '&&' o'rniga 'and', '||' o'rniga 'or' ishlatishda ehtiyot bo'lish kerakligini operatorlar prioriteti misolida ko'rsating.

## Yechim (Ruby kodi):
```ruby
# 'and' va 'or' juda past ustuvorlikka (precedence) ega
# Ular mantiqiy hisob-kitoblar uchun emas, boshqaruv oqimi uchun mo'ljallangan

x = true and false
puts "x ning qiymati ('=' prioriteti 'and' dan yuqori): #{x}"

y = (true and false)
puts "y ning qiymati qavs bilan: #{y}"

# To'g'ri amaliyot: shartli harakatlar uchun
status = "success"
status == "success" and puts "Amaliyot muvaffaqiyatli yakunlandi!"
```

## Tushuntirish va Mantiq:
Ruby-da 'and' va 'or' operatorlarining prioriteti '=' biriktirish operatoridan ham past. Shu sababli 'x = true and false' ifodasida avval 'x = true' bajariladi. Mantiqiy shartlar uchun har doim '&&' va '||' ishlatish, 'and'/'or' dan esa faqat zanjirli buyruqlarni bajarishda foydalanish tavsiya etiladi.

## Ishlash natijasi:
```text
x ning qiymati ('=' prioriteti 'and' dan yuqori): true
y ning qiymati qavs bilan: false
Amaliyot muvaffaqiyatli yakunlandi!
```


# 19-Topshiriq: Shartli biriktirish operatori: ||=
## Topshiriq sharti:
Kesh xotirasida qiymat mavjud bo'lmasa, unga birlamchi qiymat yuklovchi 'memoization' amalini bajaring.

## Yechim (Ruby kodi):
```ruby
kesh = nil
puts "Boshlang'ich kesh: #{kesh.inspect}"

# kesh nil bo'lgani uchun qiymat biriktiriladi
kesh ||= "Yuklangan Ma'lumotlar"
puts "Birinchi ||= keyin: #{kesh}"

# kesh mavjud bo'lgani uchun eski qiymat o'zgarmaydi
kesh ||= "Yangi Ma'lumotlar"
puts "Ikkinchi ||= keyin: #{kesh}"
```

## Tushuntirish va Mantiq:
'a ||= b' operatori 'a || (a = b)' ifodasining qisqartmasidir. Agar 'a' ning qiymati nil yoki false bo'lsa, unga 'b' qiymati yuklanadi, aks holda mavjud qiymat tegilmasdan saqlanadi. Bu Ruby-da ma'lumotlarni keshlashtirishda (Memoization) eng ko'p qo'llaniladigan idiomadir.

## Ishlash natijasi:
```text
Boshlang'ich kesh: nil
Birinchi ||= keyin: Yuklangan Ma'lumotlar
Ikkinchi ||= keyin: Yuklangan Ma'lumotlar
```


# 20-Topshiriq: Xavfsiz navigatsiya operatori: &. (Safe Navigation Operator)
## Topshiriq sharti:
Mijoz obyekti yoki uning profili nil bo'lganda 'NoMethodError' xatosi chiqmasdan xavfsiz murojaat qilishni ko'rsating.

## Yechim (Ruby kodi):
```ruby
mijoz = nil

# Xavfsiz navigatsiya (&.) nil bo'lsa darhol nil qaytaradi:
ism = mijoz&.ism
puts "Mijoz ismi (nil obyekt bilan): #{ism.inspect}"

haqiqiy_mijoz = { ism: "Dilshod" }
puts "Haqiqiy mijoz: #{haqiqiy_mijoz[:ism]}"
```

## Tushuntirish va Mantiq:
Ruby 2.3 da kiritilgan '&.' (lonely operator) zanjirli metod chaqiruvlarida nil bo'lgan obyektga murojaat qilinganda dastur halokatining oldini oladi. Agar chap tarafdagi obyekt nil bo'lsa, keyingi metod chaqirilmaydi va shunchaki nil qaytariladi.

## Ishlash natijasi:
```text
Mijoz ismi (nil obyekt bilan): nil
Haqiqiy mijoz: Dilshod
```


# 21-Topshiriq: Ternary operator (shart ? ifoda1 : ifoda2)
## Topshiriq sharti:
Foydalanuvchi yoshiga qarab kirish chiptasi narxini bir qatorda aniqlang.

## Yechim (Ruby kodi):
```ruby
yosh = 16
narx = yosh < 18 ? 15000 : 30000

puts "Yosh: #{yosh}"
puts "Chipta narxi: #{narx} so'm"
```

## Tushuntirish va Mantiq:
Ternar operatori (?:) oddiy if-else konstruksiyasini qisqa va qulay shaklda yozishga imkon beradi. Shart rost bo'lsa birinchi qism, yolg'on bo'lsa ikkinchi qism hisoblanadi va qiymat qaytaradi.

## Ishlash natijasi:
```text
Yosh: 16
Chipta narxi: 15000 so'm
```


# 22-Topshiriq: Sonlarning juft va toqligini tekshirish: even? va odd?
## Topshiriq sharti:
Berilgan sonning juft yoki toqligini Ruby-ning qulay metodlari orqali aniqlang.

## Yechim (Ruby kodi):
```ruby
son1 = 48
son2 = 57

puts "#{son1} juftmi? #{son1.even?}"
puts "#{son1} toqmi? #{son1.odd?}"
puts "#{son2} juftmi? #{son2.even?}"
puts "#{son2} toqmi? #{son2.odd?}"
```

## Tushuntirish va Mantiq:
Ruby Integer sinfi o'zida 'even?' (juftlik) va 'odd?' (toqlik) kabi tayyor mantiqiy metodlarni saqlaydi. Bu boshqa tillardagi 'son % 2 == 0' yozuviga qaraganda ancha o'qishga qulay va ifodalidir.

## Ishlash natijasi:
```text
48 juftmi? true
48 toqmi? false
57 juftmi? false
57 toqmi? true
```


# 23-Topshiriq: Sonlarni yaxlitlash metodlari: round, floor, ceil va truncate
## Topshiriq sharti:
Do'kondagi mahsulot narxi va chegirmalarni hisoblashda turli yaxlitlash usullarini qo'llang.

## Yechim (Ruby kodi):
```ruby
son = 14.67

puts "Asl son: #{son}"
puts "round (matematik yaxlitlash): #{son.round}"
puts "round(1) (bitta xona aniqlikda): #{son.round(1)}"
puts "floor (pastga yaxlitlash): #{son.floor}"
puts "ceil (yuqoriga yaxlitlash): #{son.ceil}"
puts "truncate (kasr qismini kesib tashlash): #{son.truncate}"
```

## Tushuntirish va Mantiq:
Float sinfidagi 'round' eng yaqin butun songa yaxlitlaydi; 'floor' kichik tomonga, 'ceil' katta tomonga qarab int qiladi; 'truncate' esa kasr qismini shunchaki qirqib tashlaydi.

## Ishlash natijasi:
```text
Asl son: 14.67
round (matematik yaxlitlash): 15
round(1) (bitta xona aniqlikda): 14.7
floor (pastga yaxlitlash): 14
ceil (yuqoriga yaxlitlash): 15
truncate (kasr qismini kesib tashlash): 14
```


# 24-Topshiriq: Absolyut qiymat: abs metodi
## Topshiriq sharti:
Harorat o'zgarishi va farqini hisoblashda manfiy sonning modulini oling.

## Yechim (Ruby kodi):
```ruby
kechagi_harorat = -5.4
bugungi_harorat = 3.2

farq = kechagi_harorat - bugungi_harorat
puts "Farq (xom): #{farq}"
puts "Farqning absolyut moduli (.abs): #{farq.abs}"
```

## Tushuntirish va Mantiq:
'abs' metodi har qanday sonning musbat modulini (absolyut qiymatini) qaytaradi. Masofalar, og'ishlar va farqlarni hisoblashda juda asqotadi.

## Ishlash natijasi:
```text
Farq (xom): -8.6
Farqning absolyut moduli (.abs): 8.6
```


# 25-Topshiriq: Katta sonlar va chegarasiz Integer aniqligi
## Topshiriq sharti:
Ruby-da katta sonlar qanday boshqarilishini va xotira to'lib ketishidan qo'rqmasdan 100 ning faktorialini hisoblang.

## Yechim (Ruby kodi):
```ruby
faktorial_100 = (1..100).inject(:*)

puts "100 faktoriali raqamlari soni: #{faktorial_100.to_s.length}"
puts "Oxirgi 20 ta raqami: #{faktorial_100.to_s[-20..-1]}"
puts "Sinfi: #{faktorial_100.class}"
```

## Tushuntirish va Mantiq:
Ruby 2.4 versiyasidan oldin Fixnum va Bignum sinflari mavjud edi. Ruby 2.4 dan boshlab ular yagona 'Integer' sinfiga birlashtirildi. Ruby son qanchalik katta bo'lishidan qat'i nazar (hatto minglab raqamlar bo'lsa ham) xotirani avtomatik kengaytiradi (Arbitrary-precision arithmetic).

## Ishlash natijasi:
```text
100 faktoriali raqamlari soni: 158
Oxirgi 20 ta raqami: 00000000000000000000
Sinfi: Integer
```


# 26-Topshiriq: Sonlarni qulay yozish: pastki chiziq (_) ajratuvchisi
## Topshiriq sharti:
Milliard va millionlik summalar kodda adashmasdan yozilishini ta'minlang.

## Yechim (Ruby kodi):
```ruby
aholi_soni = 36_000_000
budjet = 1_500_000_000.75

puts "O'zbekiston aholisi: #{aholi_soni}"
puts "Yillik budjet: #{budjet}"
puts "Qo'shish natijasi: #{aholi_soni + 1_000_000}"
```

## Tushuntirish va Mantiq:
Ruby raqamlar orasidagi pastki chiziqni ('_') vizual ajratuvchi sifatida qabul qiladi va ijro paytida e'tiborsiz qoldiradi. Bu katta moliyaviy yoki statistik raqamlarni xatosiz va tushunarli yozishda katta qulaylik beradi.

## Ishlash natijasi:
```text
O'zbekiston aholisi: 36000000
Yillik budjet: 1500000000.75
Qo'shish natijasi: 37000000
```


# 27-Topshiriq: Darajaga ko'tarish operatori: **
## Topshiriq sharti:
2 ning 16-darajasi va kvadrat ildiz hisoblashni daraja operatori yordamida bajaring.

## Yechim (Ruby kodi):
```ruby
daraja = 2 ** 16
ildiz = 64 ** 0.5

puts "2 ning 16-darajasi: #{daraja}"
puts "64 ning kvadrat ildizi: #{ildiz}"
```

## Tushuntirish va Mantiq:
Ruby-da '**' operatori sonni istalgan darajaga ko'taradi. Darajaga 0.5 berilsa, u kvadrat ildizni, 1.0/3 berilsa kub ildizni hisoblaydi.

## Ishlash natijasi:
```text
2 ning 16-darajasi: 65536
64 ning kvadrat ildizi: 8.0
```


# 28-Topshiriq: Bo'lish va qoldiqni bir vaqtda olish: divmod
## Topshiriq sharti:
Jami 145 daqiqani soat va daqiqalarga 'divmod' orqali ajrating.

## Yechim (Ruby kodi):
```ruby
jami_daqiqa = 145
soat, daqiqa = jami_daqiqa.divmod(60)

puts "Jami daqiqa: #{jami_daqiqa}"
puts "Natija: #{soat} soat va #{daqiqa} daqiqa"
```

## Tushuntirish va Mantiq:
'divmod' metodi butun sonli bo'lish va qoldiqni bitta chaqiruvda hisoblab, [bolinma, qoldiq] massivini qaytaradi. Bu vaqt, valyuta tangalari va o'lchov birliklarini ajratishda juda tejamkor usuldir.

## Ishlash natijasi:
```text
Jami daqiqa: 145
Natija: 2 soat va 25 daqiqa
```


# 29-Topshiriq: Bitwise (ikkilik) operatorlar
## Topshiriq sharti:
Baytlar darajasidagi mantiqiy amallar: AND (&), OR (|), XOR (^), NOT (~) va siljitish (<<, >>) amallarini bajaring.

## Yechim (Ruby kodi):
```ruby
a = 5   # 0101 ikkilikda
b = 3   # 0011 ikkilikda

puts "a & b (AND): #{a & b}"   # 0001 = 1
puts "a | b (OR): #{a | b}"    # 0111 = 7
puts "a ^ b (XOR): #{a ^ b}"   # 0110 = 6
puts "a << 1 (Chapga siljitish): #{a << 1}" # 1010 = 10
puts "a >> 1 (O'ngga siljitish): #{a >> 1}"  # 0010 = 2
```

## Tushuntirish va Mantiq:
Bitwise operatorlar sonlarning ikkilik xotira bitlari ustida bevosita ishlaydi. Chapga 1 bit siljitish sonni 2 ga ko'paytirish, o'ngga siljitish esa 2 ga bo'lishga tengdir.

## Ishlash natijasi:
```text
a & b (AND): 1
a | b (OR): 7
a ^ b (XOR): 6
a << 1 (Chapga siljitish): 10
a >> 1 (O'ngga siljitish): 2
```


# 30-Topshiriq: Global o'zgaruvchilar ($nomi) va ularning xavfi
## Topshiriq sharti:
Global o'zgaruvchi e'lon qiling, unga istalgan joydan murojaat qiling va uning xavfli jihatlarini tushuntiring.

## Yechim (Ruby kodi):
```ruby
$dastur_rejimi = "PRODUCTION"

def rejimni_korsat
  puts "Funksiya ichidan rejim: #{$dastur_rejimi}"
end

rejimni_korsat
$dastur_rejimi = "DEVELOPMENT"
puts "Tashqaridan o'zgartirilgan rejim: #{$dastur_rejimi}"
```

## Tushuntirish va Mantiq:
Dollar belgisi ($) bilan boshlangan o'zgaruvchilar dasturning barcha nuqtalaridan ko'rinadi (Global Scope). Biroq professional dasturlashda ulardan foydalanish tavsiya etilmaydi, chunki ular kodning bog'liqligini oshiradi va kutilmagan yon ta'sirlar keltiradi.

## Ishlash natijasi:
```text
Funksiya ichidan rejim: PRODUCTION
Tashqaridan o'zgartirilgan rejim: DEVELOPMENT
```


# 31-Topshiriq: Maxsus tizimli global o'zgaruvchilar
## Topshiriq sharti:
Ruby-dagi joriy fayl nomi ($0) va joriy jarayon ID-sini ($$) aniqlang.

## Yechim (Ruby kodi):
```ruby
joriy_fayl = $0
jarayon_id = $$

puts "Fayl nomi mavjudmi: #{!joriy_fayl.nil?}"
puts "Joriy Process ID (PID) mavjudmi: #{jarayon_id > 0}"
```

## Tushuntirish va Mantiq:
Ruby bir qator ichki global o'zgaruvchilarga ega: '$0' joriy skript nomi, '$$' operatsion tizimdagi jarayon identifikatori (Process ID), '$?' oxirgi bajarilgan tizim buyrug'ining chiqish kodi hisoblanadi.

## Ishlash natijasi:
```text
Fayl nomi mavjudmi: true
Joriy Process ID (PID) mavjudmi: true
```


# 32-Topshiriq: Obyektlarni muzlatish: freeze metodi
## Topshiriq sharti:
Sozlamalar matnini o'zgarishlardan asrash maqsadida 'freeze' metodidan foydalaning.

## Yechim (Ruby kodi):
```ruby
sozlama = "MAX_CONNECTIONS=100"
sozlama.freeze

puts "Muzlatilgan matn: #{sozlama}"
puts "Obyekt muzlatilganmi? #{sozlama.frozen?}"
```

## Tushuntirish va Mantiq:
'freeze' metodi chaqirilgach, obyekt o'zgarmas holatga keladi. Unga yangi ma'lumot qo'shish yoki o'zgartirishga urinish 'FrozenError' xatosiga olib keladi. Bu ko'p oqimli dasturlarda xotira yaxlitligini ta'minlaydi.

## Ishlash natijasi:
```text
Muzlatilgan matn: MAX_CONNECTIONS=100
Obyekt muzlatilganmi? true
```


# 33-Topshiriq: frozen? va xotira xavfsizligi
## Topshiriq sharti:
Massivni freeze qilib, elementlarini o'zgartirishdan himoyalang.

## Yechim (Ruby kodi):
```ruby
royxat = ["admin", "moderator", "user"]
royxat.freeze

puts "Massiv muzlaganmi? #{royxat.frozen?}"
puts "Elementlar soni: #{royxat.size}"
```

## Tushuntirish va Mantiq:
Muzlatilgan massivga yangi element qo'shib bo'lmaydi. Bu tizim konfiguratsiyalari tasodifan o'zgartirib yuborilishining oldini oladi.

## Ishlash natijasi:
```text
Massiv muzlaganmi? true
Elementlar soni: 3
```


# 34-Topshiriq: Oraliqlar (Ranges): .. va ... farqi
## Topshiriq sharti:
1 dan 5 gacha inklyuziv (oxirgi son kiradi) va eksklyuziv (oxirgi son kirmaydi) oraliqlarni taqqoslang.

## Yechim (Ruby kodi):
```ruby
inklyuziv = 1..5   # 1, 2, 3, 4, 5
eksklyuziv = 1...5  # 1, 2, 3, 4

puts "1..5 massiv sifatida: #{inklyuziv.to_a.inspect}"
puts "1...5 massiv sifatida: #{eksklyuziv.to_a.inspect}"
```

## Tushuntirish va Mantiq:
Ikkita nuqta (..) oraliqning oxirgi chegarasini ham o'z ichiga oladi (inklyuziv). Uchta nuqta (...) esa oxirgi sonni hisobga olmaydi (eksklyuziv). Bu massiv indekslari bilan ishlashda juda qulaydir.

## Ishlash natijasi:
```text
1..5 massiv sifatida: [1, 2, 3, 4, 5]
1...5 massiv sifatida: [1, 2, 3, 4]
```


# 35-Topshiriq: Range metodlari: include? va cover?
## Topshiriq sharti:
Berilgan son yoki harf oraliqda mavjudligini include? va cover? orqali tekshiring.

## Yechim (Ruby kodi):
```ruby
harflar = 'a'..'z'
sonlar = 10..50

puts "'k' harfi oraliqdami? #{harflar.include?('k')}"
puts "25 soni oraliqdami? #{sonlar.cover?(25)}"
puts "60 soni oraliqdami? #{sonlar.cover?(60)}"
```

## Tushuntirish va Mantiq:
'include?' oraliqdagi har bir elementni ketma-ket aylanib chiqishi mumkin; 'cover?' esa faqat chegaralarni (boshlanish <= qiymat <= tugash) solishtiradi va juda katta oraliqlarda yashin tezligida ishlaydi.

## Ishlash natijasi:
```text
'k' harfi oraliqdami? true
25 soni oraliqdami? true
60 soni oraliqdami? false
```


# 36-Topshiriq: Range bilan qadamlab yurish: step
## Topshiriq sharti:
0 dan 20 gacha bo'lgan sonlarni 5 qadam bilan aylanib chiquvchi dastur yozing.

## Yechim (Ruby kodi):
```ruby
natijalar = []
(0..20).step(5) do |son|
  natijalar << son
end

puts "0..20 orasida 5 qadamli sonlar: #{natijalar.inspect}"
```

## Tushuntirish va Mantiq:
'step(n)' metodi oraliq bo'ylab har 'n' ta qadamda bir marta kod blokini chaqiradi.

## Ishlash natijasi:
```text
0..20 orasida 5 qadamli sonlar: [0, 5, 10, 15, 20]
```


# 37-Topshiriq: Belgilar (Symbols) asoslari: :symbol sintaksisi
## Topshiriq sharti:
Ruby-da Symbol e'lon qiling va uning nomini chop eting.

## Yechim (Ruby kodi):
```ruby
status_ok = :muvaffaqiyatli
status_fail = :xatolik

puts "Status: #{status_ok} (Sinfi: #{status_ok.class})"
puts "Xatolik: #{status_fail} (Sinfi: #{status_fail.class})"
```

## Tushuntirish va Mantiq:
Symbol Ruby-da ikki nuqta (:) bilan boshlanadigan identifikatorlardir. Ular ichki nomlar, Hash kalitlari va metod nomlari sifatida ishlatiladi.

## Ishlash natijasi:
```text
Status: muvaffaqiyatli (Sinfi: Symbol)
Xatolik: xatolik (Sinfi: Symbol)
```


# 38-Topshiriq: Symbol va String xotira farqi
## Topshiriq sharti:
Nega Hash kalitlari uchun String emas, Symbol ishlatilishi kerakligini tahlil qiling.

## Yechim (Ruby kodi):
```ruby
sym1 = :status
sym2 = :status

puts "Symbol 1: #{sym1}"
puts "Symbol 2: #{sym2}"
puts "Ikkala symbol bir xil manzilgami? #{sym1.object_id == sym2.object_id}"
```

## Tushuntirish va Mantiq:
Har bir yangi satr yaratilganda xotiradan yangi joy ajratiladi. Symbol esa dastur davomida faqat bitta marta xotirada yaratiladi va barcha joyda bitta xotira manziliga qaraydi. Bu xotirani tejaydi va solishtirishni tezlashtiradi.

## Ishlash natijasi:
```text
Symbol 1: status
Symbol 2: status
Ikkala symbol bir xil manzilgami? true
```


# 39-Topshiriq: to_sym va to_s konvertatsiyalari
## Topshiriq sharti:
Foydalanuvchi kiritgan satrni Symbolga va Symbolni qayta satrga aylantiring.

## Yechim (Ruby kodi):
```ruby
foydalanuvchi_roli = "admin"
simvol_rol = foydalanuvchi_roli.to_sym

puts "Satrdan simvolga: #{simvol_rol.inspect} (#{simvol_rol.class})"

qayta_satr = simvol_rol.to_s
puts "Simvoldan satrga: #{qayta_satr.inspect} (#{qayta_satr.class})"
```

## Tushuntirish va Mantiq:
'to_sym' satrni symbolga aylantiradi. 'to_s' esa symbolni oddiy matnga aylantiradi.

## Ishlash natijasi:
```text
Satrdan simvolga: :admin (Symbol)
Simvoldan satrga: "admin" (String)
```


# 40-Topshiriq: Murakkab biriktirish operatorlari
## Topshiriq sharti:
Hisoblagichni oshirish va kamaytirishda +=, -=, *=, /= operatorlaridan foydalaning.

## Yechim (Ruby kodi):
```ruby
hisob = 100
hisob += 50
hisob -= 20
hisob *= 2
hisob /= 10

puts "Yakuniy hisob: #{hisob}"
```

## Tushuntirish va Mantiq:
Murakkab biriktirish operatorlari ifodani qisqartiradi: 'hisob += 50' aslida 'hisob = hisob + 50' ning ekvivalentidir.

## Ishlash natijasi:
```text
Yakuniy hisob: 26
```


# 41-Topshiriq: Predicate metodlar (? bilan tugaydigan)
## Topshiriq sharti:
Obyekt holatini so'rovchi bo'shlik (empty?), mavjudlik (include?) va nol (zero?) metodlarini sinab ko'ring.

## Yechim (Ruby kodi):
```ruby
matn = ""
massiv = [1, 2, 3]
son = 0

puts "Matn bo'shmi? #{matn.empty?}"
puts "Massivda 2 bormi? #{massiv.include?(2)}"
puts "Son nolmi? #{son.zero?}"
```

## Tushuntirish va Mantiq:
Ruby konvensiyasiga ko'ra, mantiqiy (true/false) qiymat qaytaruvchi barcha metodlar oxirida so'roq belgisi (?) bo'ladi. Bu kodni savol-javob shaklida tabiiy o'qilishini ta'minlaydi.

## Ishlash natijasi:
```text
Matn bo'shmi? true
Massivda 2 bormi? true
Son nolmi? true
```


# 42-Topshiriq: Bang metodlar (! bilan tugaydigan o'zgartiruvchilar)
## Topshiriq sharti:
Satr ustida oddiy metod va bang (!) metodining farqini ko'rsating.

## Yechim (Ruby kodi):
```ruby
shahar = "samarqand"

# Oddiy metod asl nusxani o'zgartirmaydi, yangi nusxa qaytaradi
yangi_shahar = shahar.upcase
puts "shahar.upcase dan keyin shahar: #{shahar}"
puts "Qaytarilgan nusxa: #{yangi_shahar}"

# Bang (!) metodi asl obyektning o'zini joyida o'zgartiradi
shahar.upcase!
puts "shahar.upcase! dan keyin asl shahar: #{shahar}"
```

## Tushuntirish va Mantiq:
Ruby-da oxirida undov belgisi (!) bo'lgan metodlar 'Bang metodlar' deyiladi. Ular nusxa yaratmasdan, obyektning o'zini to'g'ridan-to'g'ri joyida o'zgartiradi.

## Ishlash natijasi:
```text
shahar.upcase dan keyin shahar: samarqand
Qaytarilgan nusxa: SAMARQAND
shahar.upcase! dan keyin asl shahar: SAMARQAND
```


# 43-Topshiriq: defined? operatori
## Topshiriq sharti:
O'zgaruvchi, metod yoki konstanta aniqlanganligini defined? orqali tekshiring.

## Yechim (Ruby kodi):
```ruby
aniqlangan_var = 42

puts "aniqlangan_var: #{defined?(aniqlangan_var)}"
puts "noma_lum_var: #{defined?(noma_lum_var).inspect}"
puts "Math::PI: #{defined?(Math::PI)}"
puts "puts metodi: #{defined?(puts)}"
```

## Tushuntirish va Mantiq:
'defined?' kalit so'zi berilgan nom e'lon qilingan yoki yo'qligini tekshiradi. Agar aniqlangan bo'lsa, uning toifasini bildiruvchi satr qaytaradi, aks holda nil qaytaradi.

## Ishlash natijasi:
```text
aniqlangan_var: local-variable
noma_lum_var: nil
Math::PI: constant
puts metodi: method
```


# 44-Topshiriq: Tipni tekshirish: is_a? va kind_of?
## Topshiriq sharti:
Obyektning ma'lum sinfga yoki uning ota sinfiga tegishliligini tekshiring.

## Yechim (Ruby kodi):
```ruby
son = 42

puts "son.is_a?(Integer): #{son.is_a?(Integer)}"
puts "son.is_a?(Numeric): #{son.is_a?(Numeric)}"
puts "son.is_a?(Object): #{son.is_a?(Object)}"
puts "son.is_a?(String): #{son.is_a?(String)}"
```

## Tushuntirish va Mantiq:
'is_a?' (va uning to'liq ekvivalenti 'kind_of?') obyekt berilgan sinf yoki uning meros iyerarxiyasidagi istalgan ota sinfiga mansubligini tekshiradi.

## Ishlash natijasi:
```text
son.is_a?(Integer): true
son.is_a?(Numeric): true
son.is_a?(Object): true
son.is_a?(String): false
```


# 45-Topshiriq: Aniq sinfni tekshirish: instance_of?
## Topshiriq sharti:
Obyekt aynan ko'rsatilgan sinf nusxasi ekanligini (merosxo'rlarni hisobga olmasdan) tekshiring.

## Yechim (Ruby kodi):
```ruby
son = 42

puts "son.instance_of?(Integer): #{son.instance_of?(Integer)}"
puts "son.instance_of?(Numeric): #{son.instance_of?(Numeric)}"
```

## Tushuntirish va Mantiq:
'instance_of?' metodidan faqat obyekt aynan shu sinfning o'zidan yaratilganligiga qat'iy ishonch hosil qilish kerak bo'lganda foydalaniladi.

## Ishlash natijasi:
```text
son.instance_of?(Integer): true
son.instance_of?(Numeric): false
```


# 46-Topshiriq: Duck Typing va respond_to? metodi
## Topshiriq sharti:
Obyektning qaysi sinfga tegishliligi emas, qanday metodni bajara olishini tekshiring.

## Yechim (Ruby kodi):
```ruby
nomalum_obyekt = "12345"

if nomalum_obyekt.respond_to?(:to_i)
  puts "Obyekt son shakliga aylana oladi: #{nomalum_obyekt.to_i * 2}"
end

if nomalum_obyekt.respond_to?(:keys)
  puts "Bu Hash obyekti"
else
  puts "Obyekt keys metodiga javob bermaydi (Duck typing)"
end
```

## Tushuntirish va Mantiq:
Ruby 'Duck Typing' tamoyiliga amal qiladi. 'respond_to?(:metod)' orqali obyektning sinfiga emas, aynan kerakli xatti-harakatga egaligiga qaraladi.

## Ishlash natijasi:
```text
Obyekt son shakliga aylana oladi: 24690
Obyekt keys metodiga javob bermaydi (Duck typing)
```


# 47-Topshiriq: Obyekt metodlarini inspeksiya qilish: methods
## Topshiriq sharti:
Butun son obyektida qanday metodlar borligini ko'ring.

## Yechim (Ruby kodi):
```ruby
son = 10
metodlar = son.methods

puts "Integer obyektidagi metodlar soni 50 dan ko'pmi: #{metodlar.size > 50}"
puts "even? metodi mavjudmi? #{metodlar.include?(:even?)}"
puts "to_s metodi mavjudmi? #{metodlar.include?(:to_s)}"
```

## Tushuntirish va Mantiq:
Ruby-da har qanday obyektning '.methods' chaqiruvi uning barcha mavjud metodlar ro'yxatini qaytaradi.

## Ishlash natijasi:
```text
Integer obyektidagi metodlar soni 50 dan ko'pmi: true
even? metodi mavjudmi? true
to_s metodi mavjudmi? true
```


# 48-Topshiriq: Sinf iyerarxiyasi: class va superclass
## Topshiriq sharti:
Satr va sonlarning ota sinflari zanjirini ildizigacha kuzatib boring.

## Yechim (Ruby kodi):
```ruby
puts "String ota sinfi: #{String.superclass}"
puts "Integer ota sinfi: #{Integer.superclass}"
puts "Numeric ota sinfi: #{Numeric.superclass}"
puts "Object ota sinfi: #{Object.superclass}"
```

## Tushuntirish va Mantiq:
Ruby-da barcha sinflar Object-dan, Object esa eng oliy BasicObject-dan meros oladi.

## Ishlash natijasi:
```text
String ota sinfi: Object
Integer ota sinfi: Numeric
Numeric ota sinfi: Object
Object ota sinfi: BasicObject
```


# 49-Topshiriq: Turli sanoq tizimidagi sonlar (Ikkilik, Sakkizlik, O'n oltilik)
## Topshiriq sharti:
0b, 0o, 0x prefikslari yordamida turli sanoq tizimlarida sonlarni ifodalang.

## Yechim (Ruby kodi):
```ruby
ikkilik = 0b101010     # 42
sakkizlik = 0o52        # 42
onoltilik = 0x2A        # 42

puts "0b101010 o'nlikda: #{ikkilik}"
puts "0o52 o'nlikda: #{sakkizlik}"
puts "0x2A o'nlikda: #{onoltilik}"
```

## Tushuntirish va Mantiq:
Ruby sanoq tizimlarini avtomatik o'nlik Integerga aylantiradi. 0b - ikkilik (binary), 0o - sakkizlik (octal), 0x - o'n oltilik (hexadecimal) prefikslaridir.

## Ishlash natijasi:
```text
0b101010 o'nlikda: 42
0o52 o'nlikda: 42
0x2A o'nlikda: 42
```


# 50-Topshiriq: Amaliy loyiha: Valyuta ayirboshlash va mijoz balansi hisoblagichi
## Topshiriq sharti:
Valyuta kurslarini o'zgarmaslarda belgilang, foydalanuvchi hisobidagi summani konvertatsiya qiling va chiroyli hisobot chiqaring.

## Yechim (Ruby kodi):
```ruby
USD_TO_UZS = 12_800.00
EUR_TO_UZS = 13_900.00

mijoz_ismi = "Temur Po'latov"
boshlangich_balans_usd = 250.0

balans_uzs = boshlangich_balans_usd * USD_TO_UZS
balans_eur = balans_uzs / EUR_TO_UZS

puts "========================================="
puts "VALYUTA AYIRBOSHLASH HISOBOTI"
puts "========================================="
puts "Mijoz:           #{mijoz_ismi}"
puts "Balans (USD):    $#{boshlangich_balans_usd.round(2)}"
puts "Balans (UZS):    #{balans_uzs.round(2)} so'm"
puts "Balans (EUR):    EUR #{balans_eur.round(2)}"
puts "Kurs (USD):      1 USD = #{USD_TO_UZS} UZS"
puts "Holat:           Muvaffaqiyatli yakunlandi"
puts "========================================="
```

## Tushuntirish va Mantiq:
Ushbu yakuniy amaliy loyihada Ruby 01 mavzusining barcha tayanch konsepsiyalari: o'zgarmaslar, arifmetik amallar, Float aniqligi, yaxlitlash (round) va String interpolatsiyasi bitta real tizimda mujassamlantirildi.

## Ishlash natijasi:
```text
=========================================
VALYUTA AYIRBOSHLASH HISOBOTI
=========================================
Mijoz:           Temur Po'latov
Balans (USD):    $250.0
Balans (UZS):    3200000.0 so'm
Balans (EUR):    EUR 230.22
Kurs (USD):      1 USD = 12800.0 UZS
Holat:           Muvaffaqiyatli yakunlandi
=========================================
```

