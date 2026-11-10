# 51-Topshiriq: Satr yaratish usullari va tirnoqlar farqi
## Topshiriq sharti:
Qo'shtirnoq, yakka tirnoq va %q/%Q operatorlari yordamida satrlar yarating va ularning interpolatsiya hamda maxsus belgilar bilan ishlashini solishtiring.

## Yechim (Ruby kodi):
```ruby
nomi = "Ruby"
s1 = "Salom, #{nomi}!\nQator tashlandi."
s2 = 'Salom, #{nomi}!\nQator tashlanmadi.'
s3 = %Q(Qo'sh tirnoqli %Q: #{nomi})
s4 = %q(Yakka tirnoqli %q: #{nomi})

puts "--- s1 ---"
puts s1
puts "--- s2 ---"
puts s2
puts "--- s3 ---"
puts s3
puts "--- s4 ---"
puts s4
```

## Tushuntirish va Mantiq:
Ruby-da satrlar qo'shtirnoq, yakka tirnoq, shuningdek %Q va %q sintaksislari orqali e'lon qilinadi. Qo'shtirnoq va %Q interpolatsiya hamda maxsus qochish belgilarini (escape sequences) qo'llab-quvvatlaydi, yakka tirnoq va %q esa barchasini xom matn sifatida qabul qiladi.

## Ishlash natijasi:
```text
--- s1 ---
Salom, Ruby!
Qator tashlandi.
--- s2 ---
Salom, \#{nomi}!\nQator tashlanmadi.
--- s3 ---
Qo'sh tirnoqli %Q: Ruby
--- s4 ---
Yakka tirnoqli %q: \#{nomi}
```


# 52-Topshiriq: Satr uzunligi: length, size va bytesize
## Topshiriq sharti:
Lotin va kirill (yoki o'zbekcha) harflardan iborat matn uzunligini belgilar va baytlar soni bo'yicha tahlil qiling.

## Yechim (Ruby kodi):
```ruby
matn_en = "Hello"
matn_uz = "O'zbekiston"
matn_kr = "Салом"

puts "matn_en length: #{matn_en.length}, bytesize: #{matn_en.bytesize}"
puts "matn_uz length: #{matn_uz.length}, bytesize: #{matn_uz.bytesize}"
puts "matn_kr length: #{matn_kr.length}, bytesize: #{matn_kr.bytesize}"
```

## Tushuntirish va Mantiq:
'length' va uning to'liq sinonimi 'size' satrdagi belgilar (characters) sonini qaytaradi. 'bytesize' esa UTF-8 kodirovkasidagi baytlar sonini hisoblaydi. Ko'p baytli belgilarda (masalan kirillcha harflar) baytlar soni belgilar sonidan ko'p bo'ladi.

## Ishlash natijasi:
```text
matn_en length: 5, bytesize: 5
matn_uz length: 11, bytesize: 11
matn_kr length: 5, bytesize: 10
```


# 53-Topshiriq: Satr belgilarini indeks orqali olish va salbiy indekslar
## Topshiriq sharti:
Matnning birinchi, uchinchi va oxirgi belgilarini musbat va manfiy indekslar yordamida ajratib oling.

## Yechim (Ruby kodi):
```ruby
shahar = "Samarqand"

puts "Birinchi harf (indeks 0): #{shahar[0]}"
puts "Uchinchi harf (indeks 2): #{shahar[2]}"
puts "Oxirgi harf (indeks -1): #{shahar[-1]}"
puts "Oxiridan ikkinchi harf (indeks -2): #{shahar[-2]}"
```

## Tushuntirish va Mantiq:
Ruby satrlarni 0 dan boshlab indekslaydi. Manfiy indekslar satr oxiridan boshlab hisoblaydi (-1 oxirgi belgi).

## Ishlash natijasi:
```text
Birinchi harf (indeks 0): S
Uchinchi harf (indeks 2): m
Oxirgi harf (indeks -1): d
Oxiridan ikkinchi harf (indeks -2): n
```


# 54-Topshiriq: Satrdan qism qirqib olish (Slicing): [boshlanish, uzunlik]
## Topshiriq sharti:
Katta matndan boshlang'ich pozitsiya va qirqib olinadigan belgilar soni bo'yicha qism ajrating.

## Yechim (Ruby kodi):
```ruby
matn = "Khorazmiy AI Laboratoriyasi"

qism1 = matn[0, 9]     # 0-indeksdan boshlab 9 ta belgi
qism2 = matn[10, 2]    # 10-indeksdan boshlab 2 ta belgi
qism3 = matn[13, 14]   # 13-indeksdan boshlab 14 ta belgi

puts "Qism 1: #{qism1}"
puts "Qism 2: #{qism2}"
puts "Qism 3: #{qism3}"
```

## Tushuntirish va Mantiq:
Satr Slicing sintaksisi `matn[start, length]` ko'rinishida bo'lib, ko'rsatilgan boshlang'ich indeksdan boshlab berilgan uzunlikdagi yangi satrni ajratib beradi.

## Ishlash natijasi:
```text
Qism 1: Khorazmiy
Qism 2: AI
Qism 3: Laboratoriyasi
```


# 55-Topshiriq: Range orqali satr kesish: [boshlanish..tugash]
## Topshiriq sharti:
Range obyekti yordamida sana satridan yil, oy va kunni ajratib oling.

## Yechim (Ruby kodi):
```ruby
sana = "2026-11-08"

yil = sana[0..3]
oy = sana[5..6]
kun = sana[8..9]

puts "Yil: #{yil}"
puts "Oy: #{oy}"
puts "Kun: #{kun}"
```

## Tushuntirish va Mantiq:
Range orqali satr kesishda `[start..finish]` inklyuziv (oxirgi belgi kiradi) yoki `[start...finish]` eksklyuziv oraliqlar ishlatiladi.

## Ishlash natijasi:
```text
Yil: 2026
Oy: 11
Kun: 08
```


# 56-Topshiriq: Harflar registrini o'zgartirish: upcase va downcase
## Topshiriq sharti:
Mijoz qidiruv so'rovlarini registrga bog'liq bo'lmagan holda solishtirish uchun kichik harflarga o'tkazing.

## Yechim (Ruby kodi):
```ruby
qidiruv = "IPHONE 15 PRO MAX"
ombor_nomi = "iphone 15 pro max"

puts "Katta harflarda: #{ombor_nomi.upcase}"
puts "Kichik harflarda: #{qidiruv.downcase}"
puts "Mos keladimi? #{qidiruv.downcase == ombor_nomi.downcase}"
```

## Tushuntirish va Mantiq:
'upcase' barcha harflarni bosh harfga, 'downcase' esa kichik harflarga o'zgartiradi. Zamonaviy Ruby-da bu metodlar to'liq Unicode va turli alifbolar bilan mukammal ishlaydi.

## Ishlash natijasi:
```text
Katta harflarda: IPHONE 15 PRO MAX
Kichik harflarda: iphone 15 pro max
Mos keladimi? true
```


# 57-Topshiriq: Gapning birinchi harfini katta qilish: capitalize
## Topshiriq sharti:
Foydalanuvchi kichik harflarda kiritgan ism va familiyani chiroyli qilib bosh harf bilan chiqaring.

## Yechim (Ruby kodi):
```ruby
ism = "ali"
familiya = "valiyev"

toliq_ism = "#{ism.capitalize} #{familiya.capitalize}"
puts "Formatlangan F.I.SH: #{toliq_ism}"
```

## Tushuntirish va Mantiq:
'capitalize' metodi satrning faqat birinchi harfini katta qilib, qolgan barcha harflarini kichik harfga o'tkazadi.

## Ishlash natijasi:
```text
Formatlangan F.I.SH: Ali Valiyev
```


# 58-Topshiriq: Katta va kichik harflarni teskari qilish: swapcase
## Topshiriq sharti:
Satrdagi barcha katta harflarni kichik, kichiklarini esa katta harflarga aylantiring.

## Yechim (Ruby kodi):
```ruby
matn = "Hello Khorazmiy AI 2026"
teskari_registr = matn.swapcase

puts "Asl: #{matn}"
puts "swapcase: #{teskari_registr}"
```

## Tushuntirish va Mantiq:
'swapcase' har bir harfning registrini teskarisiga o'giradi (kichik bo'lsa katta, katta bo'lsa kichik).

## Ishlash natijasi:
```text
Asl: Hello Khorazmiy AI 2026
swapcase: hELLO kHORAZMIY ai 2026
```


# 59-Topshiriq: Bo'shliqlarni tozalash: strip metodi
## Topshiriq sharti:
Formadan kelgan probellar va yangi qatorlar bilan ifloslangan matnni tozalang.

## Yechim (Ruby kodi):
```ruby
kiruvchi_email = "   foydalanuvchi@domain.uz \t\n"
tozalangan_email = kiruvchi_email.strip

puts "Asl uzunlik: #{kiruvchi_email.length}"
puts "Tozalangan email: '#{tozalangan_email}'"
puts "Tozalangan uzunlik: #{tozalangan_email.length}"
```

## Tushuntirish va Mantiq:
'strip' metodi satrning ham boshidagi, ham oxiridagi barcha bo'shliqlar, tabulyatsiyalar (\t) va yangi qatorlarni (\n) olib tashlaydi.

## Ishlash natijasi:
```text
Asl uzunlik: 30
Tozalangan email: 'foydalanuvchi@domain.uz'
Tozalangan uzunlik: 22
```


# 60-Topshiriq: Chap va o'ng tarafdagi bo'shliqlarni tozalash: lstrip va rstrip
## Topshiriq sharti:
Matnning faqat chap yoki faqat o'ng qismidagi bo'shliqlarni ajratib tozalang.

## Yechim (Ruby kodi):
```ruby
matn = "   Ruby on Rails   "

puts "lstrip: '#{matn.lstrip}'"
puts "rstrip: '#{matn.rstrip}'"
```

## Tushuntirish va Mantiq:
'lstrip' (left strip) faqat chap tarafdagi bo'shliqlarni, 'rstrip' (right strip) esa faqat o'ng tarafdagi bo'shliqlarni qirqadi.

## Ishlash natijasi:
```text
lstrip: 'Ruby on Rails   '
rstrip: '   Ruby on Rails'
```


# 61-Topshiriq: Satr oxiridagi belgini olib tashlash: chop
## Topshiriq sharti:
Vergul bilan ajratilgan ro'yxat oxiridagi ortiqcha belgini chop orqali o'chiring.

## Yechim (Ruby kodi):
```ruby
satr = "Olma, Anor, Shaftoli,"
toza_satr = satr.chop

puts "chop dan oldin: #{satr}"
puts "chop dan keyin: #{toza_satr}"
```

## Tushuntirish va Mantiq:
'chop' metodi oxirgi belgi nima bo'lishidan qat'i nazar (belgi yoki \n) bitta belgini qirqib tashlaydi.

## Ishlash natijasi:
```text
chop dan oldin: Olma, Anor, Shaftoli,
chop dan keyin: Olma, Anor, Shaftoli
```


# 62-Topshiriq: Satr oxiridagi qator ko'chirishni olib tashlash: chomp
## Topshiriq sharti:
Oxirida \r\n yoki \n bo'lgan satrni xavfsiz tozalang.

## Yechim (Ruby kodi):
```ruby
satr1 = "Birinchi satr\n"
satr2 = "Ikkinchi satr\r\n"

puts "satr1 chomp: '#{satr1.chomp}'"
puts "satr2 chomp: '#{satr2.chomp}'"
```

## Tushuntirish va Mantiq:
'chomp' faqat oxirgi qator ko'chirish belgilarini (Windows formatidagi \r\n yoki Unix formatidagi \n) tozalaydi, boshqa belgilarga tegmaydi.

## Ishlash natijasi:
```text
satr1 chomp: 'Birinchi satr'
satr2 chomp: 'Ikkinchi satr'
```


# 63-Topshiriq: Satr ichida so'z qidirish: include?
## Topshiriq sharti:
Xabarnoma matnida 'muhim' yoki 'shoshilinch' so'zi borligini tekshiring.

## Yechim (Ruby kodi):
```ruby
xat = "Ertaga soat 10:00 da muhim yig'ilish bo'lib o'tadi."

puts "Muhim so'zi bormi? #{xat.include?('muhim')}"
puts "Shoshilinch so'zi bormi? #{xat.include?('shoshilinch')}"
```

## Tushuntirish va Mantiq:
'include?(qism)' agar ko'rsatilgan qism matn asosiy satr ichida mavjud bo'lsa true, aks holda false qaytaradi.

## Ishlash natijasi:
```text
Muhim so'zi bormi? true
Shoshilinch so'zi bormi? false
```


# 64-Topshiriq: Satr boshlanishini tekshirish: start_with?
## Topshiriq sharti:
URL manzil xavfsiz HTTPS protokoli bilan boshlanishini tekshiring.

## Yechim (Ruby kodi):
```ruby
url1 = "https://khorazmiy.uz/api"
url2 = "http://ochiq-kanal.uz"

puts "url1 https bilan boshlanadimi? #{url1.start_with?('https://')}"
puts "url2 https bilan boshlanadimi? #{url2.start_with?('https://')}"
```

## Tushuntirish va Mantiq:
'start_with?' metodi satr ko'rsatilgan prefiks bilan boshlanishini tekshiradi. Bir nechta argument qabul qilishi mumkin: `str.start_with?('http://', 'https://')`.

## Ishlash natijasi:
```text
url1 https bilan boshlanadimi? true
url2 https bilan boshlanadimi? false
```


# 65-Topshiriq: Satr tugashini tekshirish: end_with?
## Topshiriq sharti:
Fayl formati PDF yoki DOCX ekanligini kengaytmasiga qarab aniqlang.

## Yechim (Ruby kodi):
```ruby
fayl = "hisobot_2026.pdf"

puts "PDF faylmi? #{fayl.end_with?('.pdf')}"
puts "PNG rasmmi? #{fayl.end_with?('.png')}"
puts "Hujjatmi (pdf yoki docx)? #{fayl.end_with?('.pdf', '.docx')}"
```

## Tushuntirish va Mantiq:
'end_with?' metodi satr oxiridagi suffiksni tekshiradi. Bir nechta variantlarni birdaniga tekshirish qobiliyatiga ega.

## Ishlash natijasi:
```text
PDF faylmi? true
PNG rasmmi? false
Hujjatmi (pdf yoki docx)? true
```


# 66-Topshiriq: Qism matn indeksini topish: index va rindex
## Topshiriq sharti:
Matndagi kalit so'zning birinchi va oxirgi uchragan pozitsiyasini aniqlang.

## Yechim (Ruby kodi):
```ruby
matn = "Ruby tili ajoyib. Ruby Rails asosi hisoblanadi."

birinchi_indeks = matn.index("Ruby")
oxirgi_indeks = matn.rindex("Ruby")

puts "Birinchi 'Ruby' indeksi: #{birinchi_indeks}"
puts "Oxirgi 'Ruby' indeksi: #{oxirgi_indeks}"
```

## Tushuntirish va Mantiq:
'index' qidirilayotgan qismning chapdan birinchi boshlanish indeksini, 'rindex' (reverse index) esa o'ngdan birinchi (oxirgi) boshlanish indeksini qaytaradi. Topilmasa nil qaytadi.

## Ishlash natijasi:
```text
Birinchi 'Ruby' indeksi: 0
Oxirgi 'Ruby' indeksi: 18
```


# 67-Topshiriq: Satrni teskarisiga o'girish: reverse va reverse!
## Topshiriq sharti:
Berilgan so'z palindrom (teskarisiga o'qiganda ham bir xil) ekanligini tekshiring.

## Yechim (Ruby kodi):
```ruby
soz1 = "kiyik"
soz2 = "kitob"

puts "#{soz1} palindrommi? #{soz1 == soz1.reverse}"
puts "#{soz2} palindrommi? #{soz2 == soz2.reverse}"
```

## Tushuntirish va Mantiq:
'reverse' satr belgilarini teskari tartibda joylashtirib yangi nusxa qaytaradi, 'reverse!' esa asl satrning o'zini joyida o'zgartiradi.

## Ishlash natijasi:
```text
kiyik palindrommi? true
kitob palindrommi? false
```


# 68-Topshiriq: Birinchi uchragan so'zni almashtirish: sub
## Topshiriq sharti:
Matndagi faqat birinchi uchragan xatoni to'g'rilang.

## Yechim (Ruby kodi):
```ruby
matn = "Xato bor. Yana bir xato bor."
tuzatilgan = matn.sub("xato", "kamchilik")

puts "sub natijasi: #{tuzatilgan}"
```

## Tushuntirish va Mantiq:
'sub' metodi satr ichidagi birinchi uchragan naqshni ko'rsatilgan yangi satrga almashtiradi va yangi satr qaytaradi.

## Ishlash natijasi:
```text
sub natijasi: Xato bor. Yana bir kamchilik bor.
```


# 69-Topshiriq: Barcha uchragan so'zlarni almashtirish: gsub
## Topshiriq sharti:
Matndagi barcha eskirgan atamalarni yangisiga o'zgartiring.

## Yechim (Ruby kodi):
```ruby
matn = "Ruby 2.7 juda yaxshi, ammo Ruby 3.0 va Ruby 3.2 yanada yaxshiroq."
yangilangan = matn.gsub("Ruby", "Ruby Lang")

puts "gsub natijasi: #{yangilangan}"
```

## Tushuntirish va Mantiq:
'gsub' (global substitution) satrdagi barcha mos kelgan qismlarni yangi qiymat bilan almashtiradi.

## Ishlash natijasi:
```text
gsub natijasi: Ruby Lang 2.7 juda yaxshi, ammo Ruby Lang 3.0 va Ruby Lang 3.2 yanada yaxshiroq.
```


# 70-Topshiriq: Satrni massivga ajratish: split
## Topshiriq sharti:
Vergul bilan ajratilgan mahsulot nomlarini massivga aylantiring.

## Yechim (Ruby kodi):
```ruby
mevalar_satr = "olma,nok,shaftoli,anjir,uzum"
mevalar_massiv = mevalar_satr.split(",")

puts "Massiv: #{mevalar_massiv.inspect}"
puts "Mevalar soni: #{mevalar_massiv.size}"
```

## Tushuntirish va Mantiq:
'split(ajratuvchi)' berilgan ajratuvchi bo'yicha satrni bo'laklarga bo'lib, ulardan massiv hosil qiladi.

## Ishlash natijasi:
```text
Massiv: ["olma", "nok", "shaftoli", "anjir", "uzum"]
Mevalar soni: 5
```


# 71-Topshiriq: Split limit parametri va bo'shliqlar bilan ajratish
## Topshiriq sharti:
Matnni faqat belgilangan miqdordagi bo'laklarga ajratishni tahlil qiling.

## Yechim (Ruby kodi):
```ruby
satr = "Toshkent Samarqand Buxoro Xiva Andijon"

# Limit 3 berilsa, birinchi 2 ta so'z va qolgan barcha matn 3-element bo'ladi
bolaklar = satr.split(" ", 3)
puts "Limit 3 bilan split: #{bolaklar.inspect}"
```

## Tushuntirish va Mantiq:
'split(pattern, limit)' ikkinchi parametr orqali hosil bo'ladigan maksimal elementlar sonini belgilaydi. Bu HTTP sarlavhalari yoki buyruq satrlarini tahlil qilishda qulay.

## Ishlash natijasi:
```text
Limit 3 bilan split: ["Toshkent", "Samarqand", "Buxoro Xiva Andijon"]
```


# 72-Topshiriq: Massiv elementlarini satrga birlashtirish: join
## Topshiriq sharti:
Shaharlar massivini ' -> ' ko'rinishidagi marshrut matniga birlashtiring.

## Yechim (Ruby kodi):
```ruby
marshrut = ["Toshkent", "Jizzax", "Samarqand", "Buxoro"]
marshrut_matni = marshrut.join(" -> ")

puts "Marshrut: #{marshrut_matni}"
```

## Tushuntirish va Mantiq:
'join(ajratuvchi)' massivdagi barcha elementlarni berilgan ajratuvchi belgi orqali ulab, bitta yaxlit satr hosil qiladi.

## Ishlash natijasi:
```text
Marshrut: Toshkent -> Jizzax -> Samarqand -> Buxoro
```


# 73-Topshiriq: Satrga qo'shish operatorlari: << (shovel), concat va +
## Topshiriq sharti:
Satrlarni xotirada birlashtirish usullarini va ularning tezligini tahlil qiling.

## Yechim (Ruby kodi):
```ruby
s1 = "Khorazmiy"
# + yangi obyekt yaratadi
s2 = s1 + " AI"

# << asl obyektning o'ziga xotirada qo'shadi (mutation)
s3 = "Ruby"
s3 << " 3.2"

puts "s2: #{s2}"
puts "s3: #{s3}"
```

## Tushuntirish va Mantiq:
'+' operatori har safar yangi satr obyekti yaratadi va xotira yukini oshiradi. '<<' (shovel operatori) va 'concat' esa mavjud satr buferining oxiriga ma'lumot qo'shadi va ancha tezroq ishlaydi.

## Ishlash natijasi:
```text
s2: Khorazmiy AI
s3: Ruby 3.2
```


# 74-Topshiriq: Satrni takrorlash operatori: *
## Topshiriq sharti:
Hisobot sarlavhasi ostiga chiziq chizish uchun satr ko'paytirishdan foydalaning.

## Yechim (Ruby kodi):
```ruby
chiziq = "=" * 35
sarlavha = "HISOBOT NATIJALARI"

puts chiziq
puts sarlavha
puts chiziq
```

## Tushuntirish va Mantiq:
'satr * son' berilgan satrni ko'rsatilgan martagacha takrorlab bitta yangi satr yaratadi.

## Ishlash natijasi:
```text
===================================
HISOBOT NATIJALARI
===================================
```


# 75-Topshiriq: Satrni to'ldirish: ljust, rjust va center
## Topshiriq sharti:
Jadval ko'rinishida matnlarni chapga, o'ngga va markazga tekislang.

## Yechim (Ruby kodi):
```ruby
mahsulot = "Noutbuk"
narx = "1200$"

puts mahsulot.ljust(15, ".") + narx.rjust(10, ".")
puts "SARLAVHA".center(25, "-")
```

## Tushuntirish va Mantiq:
'ljust' matnni chapga surib o'ng tomonini to'ldiradi, 'rjust' o'ngga suradi, 'center' esa markazga tekislaydi.

## Ishlash natijasi:
```text
Noutbuk.............1200$
---------SARLAVHA--------
```


# 76-Topshiriq: Formatlangan satr yaratish: sprintf va % operatori
## Topshiriq sharti:
C tilidagi printf usulida satr va sonlarni formatlang.

## Yechim (Ruby kodi):
```ruby
nom = "Server"
xotira_gb = 64
yuklama = 78.456

formatlangan = sprintf("%s: %d GB xotira, yuklama: %.1f%%", nom, xotira_gb, yuklama)
puts formatlangan
```

## Tushuntirish va Mantiq:
'sprintf' yoki `"format" % [qiymatlar]` klassik formatlash spesifikatorlari (%s, %d, %f) orqali matn tuzishga imkon beradi.

## Ishlash natijasi:
```text
Server: 64 GB xotira, yuklama: 78.5%
```


# 77-Topshiriq: Butun sonlarni nollar bilan formatlash: %04d
## Topshiriq sharti:
Invoys raqamini to'rt xonali nollar bilan to'ldirilgan shaklda chiqaring.

## Yechim (Ruby kodi):
```ruby
invoys_id = 42
formatlangan_id = "INV-%04d" % invoys_id

puts "Invoys raqami: #{formatlangan_id}"
```

## Tushuntirish va Mantiq:
'%04d' formati son 4 ta raqamdan kam bo'lsa, oldiga nollarni qo'yib to'ldiradi (masalan, 42 -> 0042).

## Ishlash natijasi:
```text
Invoys raqami: INV-0042
```


# 78-Topshiriq: Pul summalarini ikki xona aniqlikda formatlash: %.2f
## Topshiriq sharti:
Do'kondagi mahsulot narxi va soliqlarni aniq 2 xonali formatda chiqaring.

## Yechim (Ruby kodi):
```ruby
narx = 129.5
soliq = narx * 0.12

puts "Narx: $%.2f" % narx
puts "Soliq: $%.2f" % soliq
```

## Tushuntirish va Mantiq:
'%.2f' har qanday haqiqiy sonning kasr qismini aniq 2 ta xonagacha yaxlitlab ko'rsatadi.

## Ishlash natijasi:
```text
Narx: $129.50
Soliq: $15.54
```


# 79-Topshiriq: Ko'p qatorli matnlar: <<~HEREDOC (Squiggly heredoc)
## Topshiriq sharti:
Kod blokining chetlanishiga (indentation) moslashuvchi qulay Heredoc yarating.

## Yechim (Ruby kodi):
```ruby
def sql_sorovi_yaratish
  sozlama_id = 105
  <<~SQL
    SELECT id, username, email
    FROM users
    WHERE status = 'active'
      AND account_id = #{sozlama_id}
    ORDER BY created_at DESC;
  SQL
end

puts sql_sorovi_yaratish
```

## Tushuntirish va Mantiq:
Ruby 2.3 da kiritilgan squiggly heredoc (`<<~`) har bir qator boshidagi umumiy bo'shliqlarni avtomatik olib tashlaydi. Bu metod ichida chiroyli formatlangan matn yozish imkonini beradi.

## Ishlash natijasi:
```text
SELECT id, username, email
FROM users
WHERE status = 'active'
  AND account_id = 105
ORDER BY created_at DESC;
```


# 80-Topshiriq: Heredoc ichida interpolatsiyani o'chirish: <<~'TEXT'
## Topshiriq sharti:
Konfiguratsiya faylini xom holda (interpolatsiyasiz) Heredoc orqali yozing.

## Yechim (Ruby kodi):
```ruby
shablon = <<~'SHABLON'
  Salom, #{ism}!
  Sizning parolingiz: #{parol}
  Ushbu parametrlar server tomonidan to'ldiriladi.
SHABLON

puts shablon
```

## Tushuntirish va Mantiq:
Agar Heredoc nomlanishi yakka tirnoq ichiga olinsa (`<<~'IDENTIFIER'`), uning ichidagi barcha `#{...}` bloklari bajarilmasdan xom matn sifatida saqlanadi.

## Ishlash natijasi:
```text
Salom, \#{ism}!
Sizning parolingiz: \#{parol}
Ushbu parametrlar server tomonidan to'ldiriladi.
```


# 81-Topshiriq: Belgining ASCII/Unicode kodi: ord metodi
## Topshiriq sharti:
Alifbo harflarining o'nlik sonlardagi ASCII kodlarini aniqlang.

## Yechim (Ruby kodi):
```ruby
harf_a = 'A'
harf_b = 'a'

puts "'A' ning kodi: #{harf_a.ord}"
puts "'a' ning kodi: #{harf_b.ord}"
puts "Farqi: #{harf_b.ord - harf_a.ord}"
```

## Tushuntirish va Mantiq:
'ord' metodi belgining unikal sonli tartib raqamini (ordinal number / Unicode code point) qaytaradi.

## Ishlash natijasi:
```text
'A' ning kodi: 65
'a' ning kodi: 97
Farqi: 32
```


# 82-Topshiriq: Sonli koddan belgi hosil qilish: chr metodi
## Topshiriq sharti:
ASCII sonlaridan foydalanib so'z hosil qiling.

## Yechim (Ruby kodi):
```ruby
kodlar = [75, 104, 111, 114, 97, 122, 109]
soz = kodlar.map(&:chr).join

puts "Hosil bo'lgan so'z: #{soz}"
```

## Tushuntirish va Mantiq:
'chr' butun sonning tegishli belgili ko'rinishini (character) qaytaradi.

## Ishlash natijasi:
```text
Hosil bo'lgan so'z: Khorazm
```


# 83-Topshiriq: Satr kodirovkasini aniqlash: encoding metodi
## Topshiriq sharti:
Satrning qaysi kodirovkada saqlanayotganini va uning to'g'riligini tekshiring.

## Yechim (Ruby kodi):
```ruby
matn = "O'zbekiston — buyuk davlat"

puts "Kodirovka: #{matn.encoding.name}"
puts "Kodirovka to'g'rimi? #{matn.valid_encoding?}"
```

## Tushuntirish va Mantiq:
Ruby satrlari o'zlarining shaxsiy 'Encoding' obyektiga ega. Odatiy holda zamonaviy Ruby-da barcha manba kodlari UTF-8 kodirovkasida ishlaydi.

## Ishlash natijasi:
```text
Kodirovka: UTF-8
Kodirovka to'g'rimi? true
```


# 84-Topshiriq: UTF-8 va o'zbekcha maxsus harflar (o' va g')
## Topshiriq sharti:
O'zbek tilidagi tutuq belgili va o'ziga xos harflar bilan qidiruv va uzunlik hisobini to'g'ri bajaring.

## Yechim (Ruby kodi):
```ruby
soz = "o'rganish"
bosh_harf = soz[0..1]

puts "So'z: #{soz}"
puts "Bosh qism: #{bosh_harf}"
puts "Belgilar soni: #{soz.length}"
```

## Tushuntirish va Mantiq:
Ruby UTF-8 belgilarni xavfsiz ajratadi va apostrofli birikmalarni to'liq to'g'ri qayta ishlaydi.

## Ishlash natijasi:
```text
So'z: o'rganish
Bosh qism: o'
Belgilar soni: 9
```


# 85-Topshiriq: Regulyar ifodalar (Regex) asoslari: /pattern/ va Regexp.new
## Topshiriq sharti:
Oddiy satr ichidan raqamlar andozasini yaratishning ikki xil usulini ko'rsating.

## Yechim (Ruby kodi):
```ruby
regex1 = /\d+/
regex2 = Regexp.new("\\d+")

puts "regex1 sinfi: #{regex1.class}"
puts "regex2 sinfi: #{regex2.class}"
puts "Bir xilmi? #{regex1 == regex2}"
```

## Tushuntirish va Mantiq:
Ruby-da regulyar ifodalar `/.../` sintaksisi yoki `Regexp.new(...)` orqali yaratiladi va 'Regexp' sinfiga mansub bo'ladi.

## Ishlash natijasi:
```text
regex1 sinfi: Regexp
regex2 sinfi: Regexp
Bir xilmi? true
```


# 86-Topshiriq: Moslikni tekshirish operatori: =~
## Topshiriq sharti:
Matnda raqamlar mavjudligini =~ operatori yordamida tekshiring.

## Yechim (Ruby kodi):
```ruby
matn = "Mening xonam 305-raqam"
pozitsiya = matn =~ /\d+/

puts "Mos kelgan birinchi pozitsiya: #{pozitsiya}"
puts "Topildimi? #{!pozitsiya.nil?}"
```

## Tushuntirish va Mantiq:
'=~' operatori satr Regex andozasiga mos kelgan boshlang'ich indeksni qaytaradi. Moslik topilmasa nil qaytadi.

## Ishlash natijasi:
```text
Mos kelgan birinchi pozitsiya: 13
Topildimi? true
```


# 87-Topshiriq: Mos kelmaslikni tekshirish operatori: !~
## Topshiriq sharti:
Foydalanuvchi taxallusi (username) ichida probel bo'lmasligini tekshiring.

## Yechim (Ruby kodi):
```ruby
taxallus = "rustam_dev"

if taxallus !~ /\s/
  puts "Taxallusda bo'sh joy (probel) yo'q: Qabul qilindi!"
end
```

## Tushuntirish va Mantiq:
'!~' operatori satr berilgan andozaga mos kelmasa true, mos kelsa false qaytaradi.

## Ishlash natijasi:
```text
Taxallusda bo'sh joy (probel) yo'q: Qabul qilindi!
```


# 88-Topshiriq: Regexp match metodi va MatchData obyekti
## Topshiriq sharti:
Matndan sana qismlarini match orqali MatchData obyektiga oling.

## Yechim (Ruby kodi):
```ruby
matn = "Tug'ilgan sana: 1998-05-24"
moslik = matn.match(/(\d{4})-(\d{2})-(\d{2})/)

puts "MatchData obyekti: #{moslik.class}"
puts "To'liq moslik (0): #{moslik[0]}"
puts "Yil (1-guruh): #{moslik[1]}"
puts "Oy (2-guruh): #{moslik[2]}"
puts "Kun (3-guruh): #{moslik[3]}"
```

## Tushuntirish va Mantiq:
'match' metodi muvaffaqiyatli qidiruvda 'MatchData' obyektini qaytaradi. U guruhlar, pozitsiyalar va mos kelgan matn haqida to'liq ma'lumot beradi.

## Ishlash natijasi:
```text
MatchData obyekti: MatchData
To'liq moslik (0): 1998-05-24
Yil (1-guruh): 1998
Oy (2-guruh): 05
Kun (3-guruh): 24
```


# 89-Topshiriq: Regex capture guruhlari va maxsus $1, $2 o'zgaruvchilari
## Topshiriq sharti:
Telefon prefiksi va raqamini capture guruhlari orqali ajrating.

## Yechim (Ruby kodi):
```ruby
telefon = "+998 90 1234567"

if telefon =~ /\+(\d{3})\s(\d{2})\s(\d{7})/
  puts "Mamlakat kodi ($1): #{$1}"
  puts "Operator kodi ($2): #{$2}"
  puts "Raqam ($3): #{$3}"
end
```

## Tushuntirish va Mantiq:
Qavslar `(...)` capture guruhi hisoblanadi. Muvaffaqiyatli solishtirishdan so'ng Ruby avtomatik `$1`, `$2`, `$3` maxsus o'zgaruvchilariga mos kelgan qismlarni yuklaydi.

## Ishlash natijasi:
```text
Mamlakat kodi ($1): 998
Operator kodi ($2): 90
Raqam ($3): 1234567
```


# 90-Topshiriq: Nomlangan capture guruhlari: (?<nom>pattern)
## Topshiriq sharti:
Regex-da guruhlarga aniq nom berib, ularga kalit so'z orqali murojaat qiling.

## Yechim (Ruby kodi):
```ruby
matn = "IP manzil: 192.168.1.100, Port: 8080"
andoza = /IP manzil: (?<ip>[\d\.]+), Port: (?<port>\d+)/

m = andoza.match(matn)
puts "IP: #{m[:ip]}"
puts "Port: #{m[:port]}"
```

## Tushuntirish va Mantiq:
Nomlangan guruhlar `(?<nom>...)` sintaksisi bilan yaratiladi va MatchData obyekti orqali `m[:nom]` tarzida oson va tushunarli olinadi.

## Ishlash natijasi:
```text
IP: 192.168.1.100
Port: 8080
```


# 91-Topshiriq: Barcha mosliklarni qidirib topish: scan
## Topshiriq sharti:
Matn ichidagi barcha xeshteglarni massiv shaklida ajratib oling.

## Yechim (Ruby kodi):
```ruby
post = "Bugun #ruby va #rails bo'yicha #khorazmiy_ai darslari boshlandi!"
xeshteglar = post.scan(/#\w+/)

puts "Topilgan xeshteglar: #{xeshteglar.inspect}"
```

## Tushuntirish va Mantiq:
'scan(pattern)' andozaga mos kelgan barcha qismlarni satrlar massivi sifatida qaytaradi.

## Ishlash natijasi:
```text
Topilgan xeshteglar: ["#ruby", "#rails", "#khorazmiy_ai"]
```


# 92-Topshiriq: scan va blok yordamida har bir moslikni qayta ishlash
## Topshiriq sharti:
Matndagi barcha narxlarni dollar belgisidan ajratib, umumiy summani hisoblang.

## Yechim (Ruby kodi):
```ruby
hisob = "Non $1.5, Sut $2.0, Go'sht $12.5"
jami = 0.0

hisob.scan(/\$(\d+\.\d+)/) do |narx|
  jami += narx[0].to_f
end

puts "Jami xarid: $#{jami}"
```

## Tushuntirish va Mantiq:
'scan' metodiga blok berilsa, u har bir topilgan moslik uchun blokni ishga tushiradi.

## Ishlash natijasi:
```text
Jami xarid: $16.0
```


# 93-Topshiriq: Regex bilan gsub: blok orqali dinamik almashtirish
## Topshiriq sharti:
Matndagi barcha kichik harfli so'zlarni bosh harfga aylantiruvchi dinamik almashtirish qiling.

## Yechim (Ruby kodi):
```ruby
matn = "ruby rails postgresql"
natija = matn.gsub(/\b\w+\b/) { |soz| soz.capitalize }

puts "Natija: #{natija}"
```

## Tushuntirish va Mantiq:
'gsub' metodiga blok uzatilganda, har bir topilgan moslik blok argumentiga keladi va blokdan qaytgan qiymat matn ichiga joylashtiriladi.

## Ishlash natijasi:
```text
Natija: Ruby Rails Postgresql
```


# 94-Topshiriq: Maxsus belgilar: \d va \D
## Topshiriq sharti:
Foydalanuvchi kiritgan telefon raqamidan faqat sonlarni ajratib oling.

## Yechim (Ruby kodi):
```ruby
xom_raqam = "+998 (90) 123-45-67"
faqat_raqamlar = xom_raqam.gsub(/\D/, "")

puts "Toza raqam: #{faqat_raqamlar}"
```

## Tushuntirish va Mantiq:
'\d' har qanday raqamni (0-9), '\D' esa raqam bo'lmagan har qanday belgini bildiradi. `gsub(/\D/, '')` matndan barcha harf va belgilarni olib tashlab faqat raqamlarni qoldiradi.

## Ishlash natijasi:
```text
Toza raqam: 998901234567
```


# 95-Topshiriq: So'z belgilari (\w) va probellar (\s)
## Topshiriq sharti:
Matndagi ortiqcha bo'shliqlar va probellarni bitta probelga keltiring.

## Yechim (Ruby kodi):
```ruby
matn = "Khorazmiy    AI     2026   Platformasi"
tekislangan = matn.gsub(/\s+/, " ")

puts "Tekislangan matn: #{tekislangan}"
```

## Tushuntirish va Mantiq:
'\w' harf, raqam yoki pastki chiziqni; '\s' esa probel, tabulyatsiya yoki yangi qatorni bildiradi. `\s+` bir yoki undan ko'p ketma-ket probellarni tutadi.

## Ishlash natijasi:
```text
Tekislangan matn: Khorazmiy AI 2026 Platformasi
```


# 96-Topshiriq: So'z chegarasi: \b (Word Boundary)
## Topshiriq sharti:
'cat' so'zini qidirishda 'category' yoki 'scatter' so'zlariga tegmasdan faqat mustaqil 'cat' so'zini almashtiring.

## Yechim (Ruby kodi):
```ruby
gap = "The cat is in the category of great animals."
almashtirilgan = gap.gsub(/\bcat\b/, "dog")

puts "Natija: #{almashtirilgan}"
```

## Tushuntirish va Mantiq:
'\b' so'z chegarasini (harf va bo'shliq oralig'i) bildiradi. Bu orqali uzun so'zlar ichiga yashiringan qism-matnlarni tasodifan almashtirishning oldi olinadi.

## Ishlash natijasi:
```text
Natija: The dog is in the category of great animals.
```


# 97-Topshiriq: Satr boshi va oxiri xavfsiz chegaralari: \A va \z vs ^ va $
## Topshiriq sharti:
Nega Rails tizimida validatsiya uchun ^ va $ emas, \A va \z ishlatilishi shartligini ko'rsating.

## Yechim (Ruby kodi):
```ruby
# ^ va $ faqat satr (qator) boshini tekshiradi (ko'p qatorli matnda xavfli)
# \A va \z butun matnning mutlaq boshi va oxirini tekshiradi
xavfli_matn = "admin\nINJECTION"

mos_xavfli = xavfli_matn =~ /^admin$/ ? true : false
mos_xavfsiz = xavfli_matn =~ /\Aadmin\z/ ? true : false

puts "Qator bo'yicha tekshiruv (^ $): #{mos_xavfli}"
puts "Butun matn bo'yicha tekshiruv (\A \z): #{mos_xavfsiz}"
```

## Tushuntirish va Mantiq:
Ruby-da '^' va '$' satr emas, qator chegaralarini bildiradi. Agar foydalanuvchi yangi qator (\n) orqali zararli kod kiritgan bo'lsa, '^' uni o'tkazib yuborishi mumkin. Shu sababli Ruby va Rails-da har doim xavfsiz `\A` (matnning mutlaq boshi) va `\z` (matnning mutlaq oxiri) ishlatiladi.

## Ishlash natijasi:
```text
Qator bo'yicha tekshiruv (^ $): true
Butun matn bo'yicha tekshiruv (\A \z): false
```


# 98-Topshiriq: Telefon raqamini xalqaro formatda validatsiya qilish
## Topshiriq sharti:
O'zbekiston mobil operatorlari telefon raqami andozasini tuzing.

## Yechim (Ruby kodi):
```ruby
def telefon_validatsiyasi(raqam)
  andoza = /\A\+998(90|91|93|94|95|97|98|99|88|33)\d{7}\z/
  raqam.match?(andoza)
end

puts "+998901234567 to'g'rimi? #{telefon_validatsiyasi('+998901234567')}"
puts "998901234567 to'g'rimi? #{telefon_validatsiyasi('998901234567')}"
puts "+99890123456 to'g'rimi? #{telefon_validatsiyasi('+99890123456')}"
```

## Tushuntirish va Mantiq:
'match?' metodi (Ruby 2.4+) MatchData yaratmasdan faqat boolean (true/false) qaytaradi va ancha tejamkor ishlaydi.

## Ishlash natijasi:
```text
+998901234567 to'g'rimi? true
998901234567 to'g'rimi? false
+99890123456 to'g'rimi? false
```


# 99-Topshiriq: Elektron pochta (Email) manzilini tekshiruvchi mustahkam Regex
## Topshiriq sharti:
Email manzilining to'g'riligini xavfsiz Regex orqali tekshiring.

## Yechim (Ruby kodi):
```ruby
def email_validatsiyasi(email)
  andoza = /\A[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\z/
  email.match?(andoza)
end

puts "info@khorazmiy.uz to'g'rimi? #{email_validatsiyasi('info@khorazmiy.uz')}"
puts "noto'g'ri_email@.com to'g'rimi? #{email_validatsiyasi('noto'g'ri_email@.com')}"
```

## Tushuntirish va Mantiq:
Email validatsiyasida foydalanuvchi nomi, @ belgisi, domen va kamida 2 harfli TLD tekshiriladi.

## Ishlash natijasi:
```text
info@khorazmiy.uz to'g'rimi? true
noto'g'ri_email@.com to'g'rimi? false
```


# 100-Topshiriq: Amaliy loyiha: Markdown sarlavhalari va havolalarini HTML ga o'giruvchi parser
## Topshiriq sharti:
Matndagi Markdown sarlavhalarini (## Sarlavha) va havolalarini ([nom](url)) HTML teglariga aylantiring.

## Yechim (Ruby kodi):
```ruby
markdown_matn = <<~MD
  # Asosiy Sarlavha
  Khorazmiy AI platformasida o'qish uchun [Bosh sahifa](https://khorazmiy.uz) ga kiring.
  ## Bo'lim Sarlavhasi
  Qo'shimcha ma'lumot: [Hujjatlar](https://khorazmiy.uz/docs).
MD

html_natija = markdown_matn.dup

# Sarlavhalarni almashtiramiz
html_natija.gsub!(/^# (.*?)$/, '<h1>\1</h1>')
html_natija.gsub!(/^## (.*?)$/, '<h2>\1</h2>')

# Havolalarni almashtiramiz: [nom](url) -> <a href="url">nom</a>
html_natija.gsub!(/\[(.*?)\]\((.*?)\)/, '<a href="\2">\1</a>')

puts html_natija
```

## Tushuntirish va Mantiq:
Ushbu amaliy topshiriqda Ruby satr metodlari, regex guruhi almashtirishlari (gsub! va backreference \1, \2) birlashib, real Markdown parserining negizini tashkil etdi.

## Ishlash natijasi:
```text
<h1>Asosiy Sarlavha</h1>
Khorazmiy AI platformasida o'qish uchun <a href="https://khorazmiy.uz">Bosh sahifa</a> ga kiring.
<h2>Bo'lim Sarlavhasi</h2>
Qo'shimcha ma'lumot: <a href="https://khorazmiy.uz/docs">Hujjatlar</a>.
```

