# 501-Topshiriq: begin ... rescue ... end istisnolarni ushlash
## Topshiriq sharti:
0 ga bo'lish xatosi dasturni qulatmasdan xavfsiz ushlanishini ta'minlang.

## Yechim (Ruby kodi):
```ruby
begin
  natija = 10 / 0
  puts "Natija: #{natija}"
rescue ZeroDivisionError => e
  puts "Xatolik ushlandi: 0 ga bo'lish mumkin emas!"
  puts "Xato xabari: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ruby-da xatolar 'begin ... rescue ... end' bloki orqali ushlanadi. 'rescue ExceptionClass => e' xato haqidagi ma'lumotni 'e' o'zgaruvchisiga biriktiradi.

## Ishlash natijasi:
```text
Xatolik ushlandi: 0 ga bo'lish mumkin emas!
Xato xabari: divided by 0
```


# 502-Topshiriq: rescue StandardError vs rescue Exception
## Topshiriq sharti:
Nega faqat StandardError ni ushlash kerakligini tushuntiring.

## Yechim (Ruby kodi):
```ruby
begin
  # StandardError dan kelib chiqqan xato
  [].fetch(10)
rescue StandardError => e
  puts "Dasturiy xatolik ushlandi: #{e.class}"
end
```

## Tushuntirish va Mantiq:
Ruby xatolar daraxtida 'Exception' eng oliy sinf bo'lib, unga 'SignalException', 'NoMemoryError' va 'SystemExit' ham kiradi. Agar 'rescue Exception' qilinsa, dasturni Ctrl+C bilan ham to'xtatib bo'lmaydi. Shu sababli har doim 'rescue StandardError' (yoki shunchaki 'rescue => e') ishlatiladi.

## Ishlash natijasi:
```text
Dasturiy xatolik ushlandi: IndexError
```


# 503-Topshiriq: ensure bloki: har qanday holatda bajarilish
## Topshiriq sharti:
Xato yuz bergan yoki bermaganidan qat'i nazar resursni tozalovchi ensure blokini tuzing.

## Yechim (Ruby kodi):
```ruby
fayl_ochiq = true
begin
  puts "Fayl bilan ishlanmoqda..."
  raise "Kutilmagan xatolik!"
rescue => e
  puts "Xato qayd etildi: #{e.message}"
ensure
  fayl_ochiq = false
  puts "ensure bloki: Fayl yopildi (ochiqmi: #{fayl_ochiq})."
end
```

## Tushuntirish va Mantiq:
'ensure' bloki hatto xatolik yuz berganda ham, yoki metoddan erta 'return' qilinganda ham 100% bajariladi.

## Ishlash natijasi:
```text
Fayl bilan ishlanmoqda...
Xato qayd etildi: Kutilmagan xatolik!
ensure bloki: Fayl yopildi (ochiqmi: false).
```


# 504-Topshiriq: else bloki: faqat xato bo'lmaganda ishlash
## Topshiriq sharti:
Faqat amaliyot muvaffaqiyatli o'tgandagina xabar beruvchi else blokini qo'llang.

## Yechim (Ruby kodi):
```ruby
begin
  summa = 50000 + 25000
rescue => e
  puts "Xatolik yuz berdi"
else
  puts "Tranzaksiya muvaffaqiyatli! Summa: #{summa} so'm"
end
```

## Tushuntirish va Mantiq:
'else' faqat begin bloki ichida hech qanday istisno ko'tarilmagan holatdagina ishga tushadi.

## Ishlash natijasi:
```text
Tranzaksiya muvaffaqiyatli! Summa: 75000 so'm
```


# 505-Topshiriq: Maxsus istisno sinflari yaratish va raise
## Topshiriq sharti:
Biznes-mantiq uchun maxsus xatolik sinfi yarating va uni raise qiling.

## Yechim (Ruby kodi):
```ruby
class BalansYetarliEmasError < StandardError; end

def pul_yechish(balans, miqdor)
  if miqdor > balans
    raise BalansYetarliEmasError, "Balansda yetarli mablag' mavjud emas! (Kerak: #{miqdor}, Mavjud: #{balans})"
  end
  balans - miqdor
end

begin
  pul_yechish(50_000, 120_000)
rescue BalansYetarliEmasError => e
  puts "Maxsus xato ushlandi: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Dasturda o'ziga xos xatoliklarni ajratish uchun `class MeningXato < StandardError` meros olinadi va `raise MeningXato, 'xabar'` orqali ko'tariladi.

## Ishlash natijasi:
```text
Maxsus xato ushlandi: Balansda yetarli mablag' mavjud emas! (Kerak: 120000, Mavjud: 50000)
```


# 506-Topshiriq: Xatoliklarni boshqarish amaliyoti #6
## Topshiriq sharti:
506-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 506 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 506-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1012
```


# 507-Topshiriq: Xatoliklarni boshqarish amaliyoti #7
## Topshiriq sharti:
507-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 507 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 507-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1014
```


# 508-Topshiriq: Xatoliklarni boshqarish amaliyoti #8
## Topshiriq sharti:
508-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 508 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 508-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1016
```


# 509-Topshiriq: Xatoliklarni boshqarish amaliyoti #9
## Topshiriq sharti:
509-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 509 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 509-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1018
```


# 510-Topshiriq: Xatoliklarni boshqarish amaliyoti #10
## Topshiriq sharti:
510-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 510 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 510-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1020
```


# 511-Topshiriq: Xatoliklarni boshqarish amaliyoti #11
## Topshiriq sharti:
511-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 511 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 511-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1022
```


# 512-Topshiriq: Xatoliklarni boshqarish amaliyoti #12
## Topshiriq sharti:
512-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 512 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 512-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1024
```


# 513-Topshiriq: Xatoliklarni boshqarish amaliyoti #13
## Topshiriq sharti:
513-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 513 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 513-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1026
```


# 514-Topshiriq: Xatoliklarni boshqarish amaliyoti #14
## Topshiriq sharti:
514-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 514 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 514-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1028
```


# 515-Topshiriq: Xatoliklarni boshqarish amaliyoti #15
## Topshiriq sharti:
515-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 515 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 515-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1030
```


# 516-Topshiriq: Xatoliklarni boshqarish amaliyoti #16
## Topshiriq sharti:
516-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 516 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 516-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1032
```


# 517-Topshiriq: Xatoliklarni boshqarish amaliyoti #17
## Topshiriq sharti:
517-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 517 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 517-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1034
```


# 518-Topshiriq: Xatoliklarni boshqarish amaliyoti #18
## Topshiriq sharti:
518-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 518 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 518-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1036
```


# 519-Topshiriq: Xatoliklarni boshqarish amaliyoti #19
## Topshiriq sharti:
519-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 519 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 519-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1038
```


# 520-Topshiriq: Xatoliklarni boshqarish amaliyoti #20
## Topshiriq sharti:
520-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 520 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 520-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1040
```


# 521-Topshiriq: Xatoliklarni boshqarish amaliyoti #21
## Topshiriq sharti:
521-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 521 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 521-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1042
```


# 522-Topshiriq: Xatoliklarni boshqarish amaliyoti #22
## Topshiriq sharti:
522-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 522 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 522-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1044
```


# 523-Topshiriq: Xatoliklarni boshqarish amaliyoti #23
## Topshiriq sharti:
523-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 523 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 523-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1046
```


# 524-Topshiriq: Xatoliklarni boshqarish amaliyoti #24
## Topshiriq sharti:
524-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 524 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 524-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1048
```


# 525-Topshiriq: Xatoliklarni boshqarish amaliyoti #25
## Topshiriq sharti:
525-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 525 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 525-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1050
```


# 526-Topshiriq: Xatoliklarni boshqarish amaliyoti #26
## Topshiriq sharti:
526-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 526 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 526-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1052
```


# 527-Topshiriq: Xatoliklarni boshqarish amaliyoti #27
## Topshiriq sharti:
527-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 527 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 527-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1054
```


# 528-Topshiriq: Xatoliklarni boshqarish amaliyoti #28
## Topshiriq sharti:
528-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 528 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 528-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1056
```


# 529-Topshiriq: Xatoliklarni boshqarish amaliyoti #29
## Topshiriq sharti:
529-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 529 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 529-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1058
```


# 530-Topshiriq: Xatoliklarni boshqarish amaliyoti #30
## Topshiriq sharti:
530-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 530 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 530-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1060
```


# 531-Topshiriq: Xatoliklarni boshqarish amaliyoti #31
## Topshiriq sharti:
531-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 531 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 531-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1062
```


# 532-Topshiriq: Xatoliklarni boshqarish amaliyoti #32
## Topshiriq sharti:
532-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 532 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 532-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1064
```


# 533-Topshiriq: Xatoliklarni boshqarish amaliyoti #33
## Topshiriq sharti:
533-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 533 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 533-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1066
```


# 534-Topshiriq: Xatoliklarni boshqarish amaliyoti #34
## Topshiriq sharti:
534-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 534 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 534-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1068
```


# 535-Topshiriq: Xatoliklarni boshqarish amaliyoti #35
## Topshiriq sharti:
535-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 535 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 535-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1070
```


# 536-Topshiriq: Xatoliklarni boshqarish amaliyoti #36
## Topshiriq sharti:
536-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 536 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 536-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1072
```


# 537-Topshiriq: Xatoliklarni boshqarish amaliyoti #37
## Topshiriq sharti:
537-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 537 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 537-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1074
```


# 538-Topshiriq: Xatoliklarni boshqarish amaliyoti #38
## Topshiriq sharti:
538-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 538 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 538-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1076
```


# 539-Topshiriq: Xatoliklarni boshqarish amaliyoti #39
## Topshiriq sharti:
539-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 539 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 539-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1078
```


# 540-Topshiriq: Xatoliklarni boshqarish amaliyoti #40
## Topshiriq sharti:
540-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 540 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 540-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1080
```


# 541-Topshiriq: Xatoliklarni boshqarish amaliyoti #41
## Topshiriq sharti:
541-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 541 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 541-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1082
```


# 542-Topshiriq: Xatoliklarni boshqarish amaliyoti #42
## Topshiriq sharti:
542-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 542 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 542-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1084
```


# 543-Topshiriq: Xatoliklarni boshqarish amaliyoti #43
## Topshiriq sharti:
543-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 543 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 543-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1086
```


# 544-Topshiriq: Xatoliklarni boshqarish amaliyoti #44
## Topshiriq sharti:
544-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 544 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 544-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1088
```


# 545-Topshiriq: Xatoliklarni boshqarish amaliyoti #45
## Topshiriq sharti:
545-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 545 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 545-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1090
```


# 546-Topshiriq: Xatoliklarni boshqarish amaliyoti #46
## Topshiriq sharti:
546-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 546 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 546-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1092
```


# 547-Topshiriq: Xatoliklarni boshqarish amaliyoti #47
## Topshiriq sharti:
547-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 547 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 547-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1094
```


# 548-Topshiriq: Xatoliklarni boshqarish amaliyoti #48
## Topshiriq sharti:
548-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 548 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 548-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1096
```


# 549-Topshiriq: Xatoliklarni boshqarish amaliyoti #49
## Topshiriq sharti:
549-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 549 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 549-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1098
```


# 550-Topshiriq: Xatoliklarni boshqarish amaliyoti #50
## Topshiriq sharti:
550-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.

## Yechim (Ruby kodi):
```ruby
begin
  qiymat = 550 * 2
  puts "Qiymat: #{qiymat}"
rescue => e
  puts "Xato: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ushbu 550-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Qiymat: 1100
```

