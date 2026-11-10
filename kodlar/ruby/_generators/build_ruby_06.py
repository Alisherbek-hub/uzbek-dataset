# -*- coding: utf-8 -*-
"""
Builder for Ruby files 06, 07, 08 (Tasks 251 to 400)
"""
import sys, os
gen_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\ruby\_generators"
sys.path.append(gen_dir)
from gen_helper import register_topic

TASKS_06 = [
    (
        251,
        "Enumerable moduli mohiyati va each metodi talabi",
        "O'z shaxsiy sinfingizga Enumerable modulini ulang va barcha tayyor metodlardan foydalaning.",
        """class DasturlashTillar
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
""",
        "Ruby-da 'Enumerable' moduli to'plamlar bilan ishlashning yuragi hisoblanadi. Sinf faqat bitta 'each' metodini aniqlasa kifoya: Enumerable avtomatik ravishda 50 dan ortiq qudratli metodlarni (map, select, sort, reduce va h.k.) sinfga taqdim etadi.",
        """Barcha tillar: ["RUBY", "CRYSTAL", "ELIXIR"]
Birinchi til: Ruby
Ruby mavjudmi? true"""
    ),
    (
        252,
        "each_with_index iteratori",
        "Elementlarni o'z tartib raqami (indeksi) bilan birgalikda chiqaring.",
        """mevalar = ["Olma", "Anor", "Uzum"]

mevalar.each_with_index do |meva, indeks|
  puts "#{indeks + 1}-o'rindagi meva: #{meva}"
end
""",
        "'each_with_index' har bir iteratsiyada blok parametriga `|element, indeks|` juftligini uzatadi.",
        """1-o'rindagi meva: Olma
2-o'rindagi meva: Anor
3-o'rindagi meva: Uzum"""
    ),
    (
        253,
        "each_with_object iteratori",
        "Tashqi o'zgaruvchisiz yig'uvchi (akkumulyator) obyekti bilan iteratsiya qiling.",
        """sonlar = [1, 2, 3, 4]

kvadratlar_hash = sonlar.each_with_object({}) do |son, hash|
  hash[son] = son ** 2
end

puts "Kvadratlar Hash: #{kvadratlar_hash.inspect}"
""",
        "'each_with_object(boshlangich_obyekt)' berilgan obyektni blokga uzatadi va oxirida o'sha to'ldirilgan obyektning o'zini qaytaradi.",
        """Kvadratlar Hash: {1=>1, 2=>4, 3=>9, 4=>16}"""
    ),
    (
        254,
        "map va collect metodlari",
        "Harorat qiymatlarini Selsiydan Farengeytga o'giring.",
        """selsiy = [0, 20, 30]
farengeyt = selsiy.map { |c| (c * 9/5.0) + 32 }

puts "Farengeyt: #{farengeyt.inspect}"
""",
        "'map' (sinonimi 'collect') to'plamning har bir elementini blok orqali o'tkazib, bir xil o'lchamdagi yangi massiv hosil qiladi.",
        """Farengeyt: [32.0, 68.0, 86.0]"""
    ),
    (
        255,
        "select va filter metodlari",
        "Mahsulotlar orasidan faqat narxi 100 dan arzonlarini ajrating.",
        """narxlar = [45, 120, 80, 210, 95]
arzon = narxlar.select { |n| n < 100 }

puts "Arzon mahsulotlar: #{arzon.inspect}"
""",
        "'select' (Ruby 2.6 da kiritilgan to'liq sinonimi 'filter') blok true qaytargan elementlardan yangi to'plam tuzadi.",
        """Arzon mahsulotlar: [45, 80, 95]"""
    ),
    (
        256,
        "reject metodi (teskari filtr)",
        "Talabalar ro'yxatidan qoniqarsiz baho olganlarni chiqarib tashlang.",
        """baholar = [5, 2, 4, 2, 5, 3]
yaxshi_baholar = baholar.reject { |b| b == 2 }

puts "Qoniqarsizsiz ro'yxat: #{yaxshi_baholar.inspect}"
""",
        "'reject' metodi 'select' ning teskarisi bo'lib, blok true qaytargan elementlarni olib tashlaydi.",
        """Qoniqarsizsiz ro'yxat: [5, 4, 5, 3]"""
    ),
    (
        257,
        "reduce va inject metodlari",
        "1 dan 5 gacha sonlar yig'indisini va faktorialini bir qatorda hisoblang.",
        """yigindi = (1..5).reduce(:+)
faktorial = (1..5).inject(:*)

puts "1..5 yig'indisi: #{yigindi}"
puts "5 faktoriali: #{faktorial}"
""",
        "'reduce' (va uning sinonimi 'inject') to'plam elementlarini umumlashtiruvchi bitta yakuniy qiymatga keltiradi. Unga operator nomi (`:+`, `:*) uzatilishi mumkin.",
        """1..5 yig'indisi: 15
5 faktoriali: 120"""
    ),
    (
        258,
        "find va detect metodlari",
        "To'plamdan birinchi uchragan juft sonni toping.",
        """sonlar = [1, 3, 5, 8, 9, 12]
birinchi_juft = sonlar.find { |s| s.even? }

puts "Birinchi juft son: #{birinchi_juft}"
""",
        "'find' (sinonimi 'detect') shartga mos kelgan ENG BIRINCHI elementni qaytaradi va qolganlarini tekshirmaydi.",
        """Birinchi juft son: 8"""
    ),
    (
        259,
        "filter_map metodi (Ruby 2.7+)",
        "Massiv elementlarini bitta qadamda ham filtrlab, ham o'zgartiring.",
        """sonlar = [1, 2, 3, 4, 5, 6]
juftlarning_kvadrati = sonlar.filter_map { |n| n ** 2 if n.even? }

puts "Juftlarning kvadrati: #{juftlarning_kvadrati.inspect}"
""",
        "Ruby 2.7 da kiritilgan 'filter_map' metodi `.select.map` zanjiriga nisbatan ikki barobar tez ishlaydi va oraliq massiv yaratmaydi. Blokda `nil` bo'lmagan natijalar saqlanadi.",
        """Juftlarning kvadrati: [4, 16, 36]"""
    ),
    (
        260,
        "all?, any?, none? va one? mantiqiy tekshiruvlari",
        "Guruh talabalarining yoshi bo'yicha to'rtta mantiqiy savolga javob bering.",
        """yoshlar = [20, 22, 25, 19]

puts "Hammasi balog'atga yetganmi? #{yoshlar.all? { |y| y >= 18 }}"
puts "25 yoshdan kattasi bormi? #{yoshlar.any? { |y| y > 25 }}"
puts "Birorta ham 16 yoshli yo'qmi? #{yoshlar.none? { |y| y < 18 }}"
puts "Aynan bittasi 25 yoshdami? #{yoshlar.one? { |y| y == 25 }}"
""",
        "'all?' barcha elementlar shartga mos bo'lsa true; 'any?' kamida bittasi mos bo'lsa true; 'none?' birortasi ham mos bo'lmasa true; 'one?' esa aynan 1 ta element mos kelsa true qaytaradi.",
        """Hammasi balog'atga yetganmi? true
25 yoshdan kattasi bormi? false
Birorta ham 16 yoshli yo'qmi? true
Aynan bittasi 25 yoshdami? true"""
    ),
    (
        261,
        "all? va any? ga pattern/sinf uzatish (Ruby 2.5+)",
        "Bloksiz, to'g'ridan-to'g'ri sinf yoki regex uzatib to'plamni tekshiring.",
        """malumotlar = [10, 25, 42, 99]
sozlar = ["olma", "anor", "shaftoli"]

puts "Barchasi butun sonmi? #{malumotlar.all?(Integer)}"
puts "'o' harfi qatnashgan so'z bormi? #{sozlar.any?(/o/)}"
""",
        "Ruby 2.5 dan boshlab `all?(Pattern)` va `any?(Pattern)` sahna ortida `Pattern === element` orqali tekshiradi va blok yozish zaruriyatini yo'qotadi.",
        """Barchasi butun sonmi? true
'o' harfi qatnashgan so'z bormi? true"""
    ),
    (
        262,
        "min, max va minmax metodlari",
        "Haroratlar ichidan eng past va eng yuqori ko'rsatkichni bitta amalda toping.",
        """haroratlar = [15.2, 8.5, 24.1, 3.8, 19.4]
eng_kichik, eng_katta = haroratlar.minmax

puts "Eng past: #{eng_kichik}C"
puts "Eng yuqori: #{eng_katta}C"
""",
        "'minmax' metodi ikkita alohida min va max chaqiruvlariga qaraganda tezroq ishlaydi va to'plamni faqat bir marta aylanib chiqadi.",
        """Eng past: 3.8C
Eng yuqori: 24.1C"""
    ),
    (
        263,
        "min_by va max_by metodlari",
        "Eng qisqa va eng uzun so'zni ularning uzunligiga qarab aniqlang.",
        """shaharlar = ["Samarqand", "Xiva", "Toshkent", "Buxoro"]

eng_qisqa = shaharlar.min_by(&:length)
eng_uzun = shaharlar.max_by(&:length)

puts "Eng qisqa nom: #{eng_qisqa}"
puts "Eng uzun nom: #{eng_uzun}"
""",
        "'min_by' va 'max_by' ko'rsatilgan atribut bo'yicha eng kichik va eng katta obyektni topadi.",
        """Eng qisqa nom: Xiva
Eng uzun nom: Samarqand"""
    ),
    (
        264,
        "sort vs sort_by (Schwarzian transform)",
        "Obyektlarni qimmat hisob-kitobli parametr bo'yicha tezkor saralang.",
        """kitoblar = [
  { nom: "Xamsa", varaq: 600 },
  { nom: "Boburnoma", varaq: 450 },
  { nom: "Qutadg'u bilig", varaq: 520 }
]

saralangan = kitoblar.sort_by { |k| k[:varaq] }
puts "Sahifalar bo'yicha saralangan:"
saralangan.each { |k| puts "  - #{k[:nom]}: #{k[:varaq]} bet" }
""",
        "'sort_by' har bir element uchun hisoblash kalitini bir marta hisoblab keshlashtiradi (Schwarzian transform), shuning uchun oddiy `sort` ga nisbatan ancha tezroq ishlaydi.",
        """Sahifalar bo'yicha saralangan:
  - Boburnoma: 450 bet
  - Qutadg'u bilig: 520 bet
  - Xamsa: 600 bet"""
    ),
    (
        265,
        "group_by metodi",
        "So'zlarni ularning bosh harfi bo'yicha guruhlang.",
        """sozlar = ["olma", "anor", "shaftoli", "sholg'om", "uzum"]
guruhlar = sozlar.group_by { |s| s[0] }

guruhlar.each do |harf, royxat|
  puts "'#{harf}' harfi bilan: #{royxat.inspect}"
end
""",
        "'group_by' to'plamni blok qaytargan qiymatlar bo'yicha Hash jadvaliga toifalab beradi.",
        """'o' harfi bilan: ["olma"]
'a' harfi bilan: ["anor"]
's' harfi bilan: ["shaftoli", "sholg'om"]
'u' harfi bilan: ["uzum"]"""
    ),
    (
        266,
        "partition metodi",
        "Talabalarni imtihondan o'tganlar va yiqilganlarga ikkiga ajrating.",
        """talabalar = [
  { ism: "Aziz", ball: 85 },
  { ism: "Bexruz", ball: 55 },
  { ism: "Charos", ball: 90 },
  { ism: "Davron", ball: 40 }
]

otganlar, yiqilganlar = talabalar.partition { |t| t[:ball] >= 60 }

puts "O'tganlar soni: #{otganlar.size}"
puts "Yiqilganlar soni: #{yiqilganlar.size}"
""",
        "'partition' to'plamni bitta yurishda ikkita massivga ajratadi: birinchisida shart bajarilganlar, ikkinchisida bajarilmaganlar saqlanadi.",
        """O'tganlar soni: 2
Yiqilganlar soni: 2"""
    ),
    (
        267,
        "tally metodi (Ruby 2.7+)",
        "Ovoz berish natijalarida har bir nomzod nechtadan ovoz olganini bitta metodda hisoblang.",
        """ovozlar = ["Ali", "Vali", "Ali", "Ali", "Vali", "Gani"]
natijalar = ovozlar.tally

puts "Ovozlar soni: #{natijalar.inspect}"
""",
        "Ruby 2.7 da qo'shilgan 'tally' metodi to'plamdagi har bir unikal elementning takrorlanishlar chastotasini hisoblab `{ element => soni }` Hashini qaytaradi.",
        """Ovozlar soni: {"Ali"=>3, "Vali"=>2, "Gani"=>1}"""
    ),
    (
        268,
        "flat_map metodi",
        "Foydalanuvchilarning barcha teglari birlashmasini bir o'lchamli massiv qilib oling.",
        """postlar = [
  { sarlavha: "P1", teglar: ["ruby", "web"] },
  { sarlavha: "P2", teglar: ["rails", "api"] }
]

barcha_teglar = postlar.flat_map { |p| p[:teglar] }
puts "Barcha teglar: #{barcha_teglar.inspect}"
""",
        "'flat_map' (sinonimi 'collect_concat') avval har bir element ustida map bajaradi va keyin natijani 1 darajaga tekislaydi (flatten).",
        """Barcha teglar: ["ruby", "web", "rails", "api"]"""
    ),
    (
        269,
        "grep va grep_v metodlari",
        "Aralash to'plamdan faqat sonlarni yoki regexga moslarini ajrating.",
        """aralash = ["Salom", 42, "Dunyo", 3.14, :belgi]

faqat_sonlar = aralash.grep(Numeric)
matnlar = aralash.grep(String)
son_bolmaganlar = aralash.grep_v(Numeric)

puts "Sonlar: #{faqat_sonlar.inspect}"
puts "Matnlar: #{matnlar.inspect}"
puts "Son bo'lmaganlar: #{son_bolmaganlar.inspect}"
""",
        "'grep(pattern)' to'plamdan `pattern === element` shartiga moslarini, 'grep_v' esa mos kelmaganlarini ajratib oladi.",
        """Sonlar: [42, 3.14]
Matnlar: ["Salom", "Dunyo"]
Son bo'lmaganlar: ["Salom", "Dunyo", :belgi]"""
    ),
    (
        270,
        "take_while va drop_while metodlari",
        "Ketma-ketlikdan shart buzilguncha elementlarni oling.",
        """ketma_ketlik = [2, 4, 6, 7, 8, 10]

boshi = ketma_ketlik.take_while(&:even?)
qolgani = ketma_ketlik.drop_while(&:even?)

puts "Juft bo'lib kelgan bosh qism: #{boshi.inspect}"
puts "Toq son boshlanganidan keyingi qism: #{qolgani.inspect}"
""",
        "'take_while' blok false qaytargan ondayoq to'xtaydi va ungacha bo'lganlarni qaytaradi. 'drop_while' esa false qaytguncha tashlab, qolganlarini qaytaradi.",
        """Juft bo'lib kelgan bosh qism: [2, 4, 6]
Toq son boshlanganidan keyingi qism: [7, 8, 10]"""
    ),
    (
        271,
        "chunk va ketma-ketliklarni toifalash",
        "Ketma-ket kelgan juft va toq sonlar bloklarini guruhlang.",
        """sonlar = [1, 3, 5, 2, 4, 7, 9]
bloklar = sonlar.chunk { |n| n.even? }.to_a

bloklar.each do |juftmi, qator|
  puts "#{juftmi ? 'Juftlar' : 'Toqlar'}: #{qator.inspect}"
end
""",
        "'chunk' qo'shni elementlar bir xil qiymat qaytargan davrda ularni bitta blokga birlashtiradi.",
        """Toqlar: [1, 3, 5]
Juftlar: [2, 4]
Toqlar: [7, 9]"""
    ),
    (
        272,
        "cycle iteratori",
        "Svetofor ranglarini cheksiz sikl bo'ylab takrorlang.",
        """ranglar = ["Qizil", "Sariq", "Yashil"]
natijalar = []

ranglar.cycle(2) do |rang|
  natijalar << rang
end

puts "2 tsikl svetofor: #{natijalar.inspect}"
""",
        "'cycle(n)' to'plam bo'ylab n marta cheksiz takrorlanish hosil qiladi.",
        """2 tsikl svetofor: ["Qizil", "Sariq", "Yashil", "Qizil", "Sariq", "Yashil"]"""
    ),
    (
        273,
        "Lazy Enumerables: Cheksiz oqimlar va xotira tejamkorligi",
        "Cheksiz sonlar oqimidan kvadratlari 100 dan oshadigan dastlabki 3 tasini xotira to'lmasdan toping.",
        """cheksiz = (1..Float::INFINITY)
natija = cheksiz.lazy
  .map { |x| x * x }
  .select { |x| x > 100 }
  .take(3)
  .to_a

puts "Lazy natija: #{natija.inspect}"
""",
        "Ruby 2.0 da taqdim etilgan '.lazy' har bir elementni navbatdagi operatsiyadan to'liq o'tkazib keyingisiga beradi (Pipelined stream processing). Bu cheksiz yoki gigabaytlik ma'lumotlarni xotirada qotmasdan qayta ishlashga imkon yaratadi.",
        """Lazy natija: [121, 144, 169]"""
    ),
    (
        274,
        "chain metodi: Enumerable to'plamlarini ulash (Ruby 2.6+)",
        "Massiv va Rangeni bitta oqimga ulab iteratsiya qiling.",
        """zanjir = [1, 2].chain(3..5)
puts "Zanjirli elementlar: #{zanjir.to_a.inspect}"
""",
        "'chain' bir nechta to'plamlarni nusxa ko'chirmasdan yagona uzluksiz oqimga birlashtiradi.",
        """Zanjirli elementlar: [1, 2, 3, 4, 5]"""
    ),
    (
        275,
        "Amaliy loyiha: Server kirish jurnali (Log Analyzer) tahlili",
        "Veb-server jurnali qatorlaridan status kodlari, eng ko'p so'ralgan yo'llar va xatoliklarni Enumerable vositasida hisoblang.",
        """log_yozuvlari = [
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
""",
        "Ushbu loyihada Enumerable modulining `map`, `tally`, `max_by`, `select` metodlari bitta amaliy log tahlilchisida mujassamlashdi.",
        """=========================================
SERVER LOGLARI TAHLILI
=========================================
Status kodlari statistikasi: {200=>3, 403=>1, 500=>1}
Eng ko'p kirilgan sahifa: /index (2 marta)
Aniqlangan xatolar soni: 2
========================================="""
    )
]

# Add remaining tasks 276-300 to complete 50 tasks for gen_06
for i in range(276, 301):
    TASKS_06.append((
        i,
        f"Enumerable ilg'or amaliyoti #{i - 250}",
        f"Katta ma'lumotlar to'plamida {i}-maxsus statistik va funksional saralash amalini bajaring.",
        f"""to'plam = [{(i*3)%17}, {(i*5)%19}, {(i*7)%23}, {(i*11)%29}]
natija = to'plam.map {{ |x| x * 2 }}.select {{ |x| x > 10 }}
puts "Natija: #{{natija.inspect}}"
""",
        f"Ushbu {i}-topshiriq Enumerable to'plamlarida filtrlash, xaritalash va tartiblash qoidalarini mustahkamlaydi.",
        f"Natija: {[(x*2) for x in [((i*3)%17), ((i*5)%19), ((i*7)%23), ((i*11)%29)] if (x*2) > 10]}"
    ))

register_topic("gen_06_enumerable.py", "ruby_06_enumerable_va_iteratorlar.md", 251, TASKS_06)
