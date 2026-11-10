# -*- coding: utf-8 -*-
import sys, os
gen_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\ruby\_generators"
sys.path.append(gen_dir)
from gen_helper import register_topic

TASKS_04 = [
    (
        151,
        "Massiv yaratish usullari va %w / %i sintaksisi",
        "Oddiy qavslar, Array.new, %w (so'zlar) va %i (simvollar) yordamida massivlar yarating.",
        """m1 = [1, 2, 3]
m2 = Array.new(3, "ruby")
m3 = %w[olma anor shaftoli]   # String massivi
m4 = %i[id nom narx]          # Symbol massivi

puts "m1: #{m1.inspect}"
puts "m2: #{m2.inspect}"
puts "m3 (%w): #{m3.inspect}"
puts "m4 (%i): #{m4.inspect}"
""",
        "Ruby-da `%w[...]` so'zlarni avtomatik stringlar massiviga, `%i[...]` esa ramzlar (symbols) massiviga aylantiradi. Bu tinish belgilari va qo'shtirnoqlarni ko'p yozishdan asraydi.",
        """m1: [1, 2, 3]
m2: ["ruby", "ruby", "ruby"]
m3 (%w): ["olma", "anor", "shaftoli"]
m4 (%i): [:id, :nom, :narx]"""
    ),
    (
        152,
        "Massiv elementlariga indeks orqali murojaat",
        "Musbat va manfiy indekslar orqali massivdan elementlarni oling.",
        """tilllar = ["Ruby", "Python", "Go", "Rust", "Swift"]

puts "Birinchi (0): #{tilllar[0]}"
puts "Uchinchi (2): #{tilllar[2]}"
puts "Oxirgi (-1): #{tilllar[-1]}"
puts "Oxiridan ikkinchi (-2): #{tilllar[-2]}"
""",
        "Indekslar 0 dan boshlanadi. Manfiy indekslar massiv oxiridan teskari tartibda hisoblaydi.",
        """Birinchi (0): Ruby
Uchinchi (2): Go
Oxirgi (-1): Swift
Oxiridan ikkinchi (-2): Rust"""
    ),
    (
        153,
        "Massivdan qism olish (Slicing): [boshlanish, uzunlik] va Range",
        "Massivning o'rta qismidan bir nechta elementni kesib oling.",
        """sonlar = [10, 20, 30, 40, 50, 60]

qism1 = sonlar[1, 3]    # 1-indeksdan 3 ta element
qism2 = sonlar[2..4]    # 2 dan 4 gacha oraliq

puts "sonlar[1, 3]: #{qism1.inspect}"
puts "sonlar[2..4]: #{qism2.inspect}"
""",
        "Massiv kesish (slicing) yangi massiv nusxasini qaytaradi.",
        """sonlar[1, 3]: [20, 30, 40]
sonlar[2..4]: [30, 40, 50]"""
    ),
    (
        154,
        "Elementlarni o'zgartirish va yangi indeksga biriktirish",
        "Massivdagi mavjud elementni almashtiring va oraliqda bo'sh joy qoldirib yangi element qo'shing.",
        """mevalar = ["Olma", "Nok"]
mevalar[1] = "Gilos"
mevalar[4] = "Anjir"

puts "Yangilangan mevalar: #{mevalar.inspect}"
""",
        "Agar mavjud bo'lmagan yuqori indeksga qiymat berilsa, oraliqdagi barcha kataklar avtomatik nil bilan to'ldiriladi.",
        """Yangilangan mevalar: ["Olma", "Gilos", nil, nil, "Anjir"]"""
    ),
    (
        155,
        "Oxiriga element qo'shish: push va << (shovel)",
        "Massiv oxiriga yangi xaridlarni qo'shing.",
        """savatcha = ["Kitob"]
savatcha.push("Daftar")
savatcha << "Ruchka" << "Chizg'ich"

puts "Savatcha: #{savatcha.inspect}"
""",
        "'<<' (shovel operatori) va 'push' massiv oxiriga element qo'shadi va zanjirli usulda bir nechta chaqirilishi mumkin.",
        """Savatcha: ["Kitob", "Daftar", "Ruchka", "Chizg'ich"]"""
    ),
    (
        156,
        "Boshiga element qo'shish: unshift",
        "Navbat boshiga shoshilinch mijozni qo'shing.",
        """navbat = ["Mijoz A", "Mijoz B"]
navbat.unshift("VIP Mijoz")

puts "Navbat: #{navbat.inspect}"
""",
        "'unshift' metodi elementni massivning eng boshiga (0-indeksga) kiritadi va qolgan barcha elementlarni bitta o'ngga suradi.",
        """Navbat: ["VIP Mijoz", "Mijoz A", "Mijoz B"]"""
    ),
    (
        157,
        "Oxiridan element sug'urib olish: pop",
        "Stek (Stack) tuzilmasidan oxirgi elementni sug'urib oling.",
        """stek = ["Sahifa 1", "Sahifa 2", "Sahifa 3"]
oxirgi = stek.pop

puts "Sug'urib olingan: #{oxirgi}"
puts "Qolgan stek: #{stek.inspect}"
""",
        "'pop' metodi massivning eng oxirgi elementini o'chiradi va o'sha element qiymatini qaytaradi.",
        """Sug'urib olingan: Sahifa 3
Qolgan stek: ["Sahifa 1", "Sahifa 2"]"""
    ),
    (
        158,
        "Boshidan element sug'urib olish: shift",
        "Navbat (Queue - FIFO) tizimida birinchi kelgan mijozga xizmat ko'rsating.",
        """navbat = ["1-Mijoz", "2-Mijoz", "3-Mijoz"]
birinchi = navbat.shift

puts "Xizmat ko'rsatildi: #{birinchi}"
puts "Qolgan navbat: #{navbat.inspect}"
""",
        "'shift' massivning boshidagi elementni o'chirib qaytaradi va barcha elementlarni bitta chapga suradi.",
        """Xizmat ko'rsatildi: 1-Mijoz
Qolgan navbat: ["2-Mijoz", "3-Mijoz"]"""
    ),
    (
        159,
        "Birinchi va oxirgi elementlar: first va last",
        "Massivni o'zgartirmasdan uning boshi va oxiridagi elementlarni oling.",
        """raqamlar = [10, 20, 30, 40, 50]

puts "first: #{raqamlar.first}"
puts "last: #{raqamlar.last}"
puts "first(2): #{raqamlar.first(2).inspect}"
puts "last(2): #{raqamlar.last(2).inspect}"
""",
        "'first' va 'last' parametrsiz bitta elementni, agar argument berilsa dastlabki yoki oxirgi n ta elementdan iborat yangi massivni qaytaradi.",
        """first: 10
last: 50
first(2): [10, 20]
last(2): [40, 50]"""
    ),
    (
        160,
        "take va drop metodlari",
        "Dastlabki elementlarni olish yoki tashlab yuborish amallarini bajaring.",
        """ballar = [95, 88, 76, 64, 52]

puts "take(3): #{ballar.take(3).inspect}"
puts "drop(2): #{ballar.drop(2).inspect}"
""",
        "'take(n)' dastlabki n ta elementni oladi; 'drop(n)' dastlabki n ta elementni tashlab yuborib qolganlarini qaytaradi.",
        """take(3): [95, 88, 76]
drop(2): [76, 64, 52]"""
    ),
    (
        161,
        "Element o'chirish: delete va delete_at",
        "Qiymati bo'yicha yoki indeksi bo'yicha elementlarni o'chiring.",
        """shaharlar = ["Toshkent", "Samarqand", "Buxoro", "Toshkent"]

shaharlar.delete_at(1)   # 1-indeksdagi Samarqandni o'chiradi
puts "delete_at(1) dan keyin: #{shaharlar.inspect}"

shaharlar.delete("Toshkent") # Barcha 'Toshkent' larni o'chiradi
puts "delete('Toshkent') dan keyin: #{shaharlar.inspect}"
""",
        "'delete_at(indeks)' berilgan indeksdagi bitta elementni o'chiradi. 'delete(qiymat)' esa massivdagi ushbu qiymatga teng bo'lgan BARCHA elementlarni o'chiradi.",
        """delete_at(1) dan keyin: ["Toshkent", "Buxoro", "Toshkent"]
delete('Toshkent') dan keyin: ["Buxoro"]"""
    ),
    (
        162,
        "Element mavjudligini tekshirish: include?",
        "Adminlar ro'yxatida berilgan foydalanuvchi borligini tekshiring.",
        """adminlar = ["bobur", "anvar", "nodira"]

puts "anvar adminmi? #{adminlar.include?('anvar')}"
puts "temur adminmi? #{adminlar.include?('temur')}"
""",
        "'include?(element)' agar element massivda mavjud bo'lsa true, aks holda false qaytaradi.",
        """anvar adminmi? true
temur adminmi? false"""
    ),
    (
        163,
        "Element indeksini topish: index va rindex",
        "Ro'yxatda ma'lum element nechanchi o'rinda turganini aniqlang.",
        """baholar = [5, 4, 3, 5, 4]

puts "Birinchi 5 baho indeksi: #{baholar.index(5)}"
puts "Oxirgi 5 baho indeksi: #{baholar.rindex(5)}"
puts "2 baho bormi? #{baholar.index(2).inspect}"
""",
        "'index' birinchi uchragan element indeksini, 'rindex' oxirgisini qaytaradi. Topilmasa nil qaytadi.",
        """Birinchi 5 baho indeksi: 0
Oxirgi 5 baho indeksi: 3
2 baho bormi? nil"""
    ),
    (
        164,
        "Massivlar birlashmasi: + va concat",
        "Ikkita massivni yangi obyekt yaratib yoki joyida birlashtiring.",
        """a = [1, 2]
b = [3, 4]

c = a + b
a.concat([5, 6])

puts "c (yangi massiv): #{c.inspect}"
puts "a (joyida birlashgan): #{a.inspect}"
""",
        "'+' yangi massiv yaratadi, 'concat' esa birinchi massivning o'zini o'zgartiradi (in-place).",
        """c (yangi massiv): [1, 2, 3, 4]
a (joyida birlashgan): [1, 2, 5, 6]"""
    ),
    (
        165,
        "Massivlar ayirmasi: -",
        "Barcha talabalar ro'yxatidan dars qoldirganlarni olib tashlang.",
        """barcha = ["Ali", "Vali", "Gani", "Olim"]
kelmaganlar = ["Vali", "Olim"]

kelganlar = barcha - kelmaganlar
puts "Darsda qatnashayotganlar: #{kelganlar.inspect}"
""",
        "'massiv1 - massiv2' birinchi massivdan ikkinchisida mavjud bo'lgan barcha elementlarni olib tashlaydi.",
        """Darsda qatnashayotganlar: ["Ali", "Gani"]"""
    ),
    (
        166,
        "Massivlar kesishmasi: & (Intersection)",
        "Ikkita jamoaning ikkalasida ham bor umumiy a'zolarni aniqlang.",
        """frontend = ["Aziz", "Malika", "Sardor"]
backend = ["Sardor", "Jasur", "Aziz"]

umumiy = frontend & backend
puts "Har ikkala sohani biladiganlar: #{umumiy.inspect}"
""",
        "'&' operatori faqat ikkala massivda ham mavjud bo'lgan umumiy takrorlanmas elementlarni qaytaradi.",
        """Har ikkala sohani biladiganlar: ["Aziz", "Sardor"]"""
    ),
    (
        167,
        "Massivlar unikal birlashmasi: | (Union)",
        "Ikkita ro'yxatni takrorlanishlarsiz bitta qiling.",
        """m1 = [1, 2, 3]
m2 = [2, 3, 4, 5]

unikal_birlashma = m1 | m2
puts "Birlashma (|): #{unikal_birlashma.inspect}"
""",
        "'|' operatori ikkala massiv elementlarini yagona to'plamga birlashtiradi va takrorlarni avtomatik o'chiradi.",
        """Birlashma (|): [1, 2, 3, 4, 5]"""
    ),
    (
        168,
        "Takroriy elementlarni yo'qotish: uniq va uniq!",
        "Massivdan bir xil elementlarni tozalang.",
        """sonlar = [1, 2, 2, 3, 4, 4, 4, 5]
tozalangan = sonlar.uniq

puts "Asl: #{sonlar.inspect}"
puts "uniq: #{tozalangan.inspect}"
""",
        "'uniq' takroriy elementlarni olib tashlab yangi massiv qaytaradi, 'uniq!' esa asl massivning o'zini tozalaydi.",
        """Asl: [1, 2, 2, 3, 4, 4, 4, 5]
uniq: [1, 2, 3, 4, 5]"""
    ),
    (
        169,
        "Nil qiymatlarni tozalash: compact va compact!",
        "Oraliqdagi bo'sh (nil) qiymatlarni massivdan chiqarib tashlang.",
        """xom_malumot = ["A", nil, "B", nil, "C"]
toza = xom_malumot.compact

puts "Tozalangan massiv: #{toza.inspect}"
""",
        "'compact' massivdan barcha nil elementlarni chiqarib tashlaydi.",
        """Tozalangan massiv: ["A", "B", "C"]"""
    ),
    (
        170,
        "Ko'p o'lchamli massivlarni tekislash: flatten",
        "Ichma-ich joylashgan massivlarni yagona bir o'lchamli massivga keltiring.",
        """ichma_ich = [1, [2, [3, 4]], 5]

puts "To'liq tekislash: #{ichma_ich.flatten.inspect}"
puts "1-darajali tekislash: #{ichma_ich.flatten(1).inspect}"
""",
        "'flatten' rekursiv ravishda barcha ichki massivlarni bitta qatorga yoyadi. Agar daraja parametri berilsa, faqat o'sha chuqurlikkacha tekislaydi.",
        """To'liq tekislash: [1, 2, 3, 4, 5]
1-darajali tekislash: [1, 2, [3, 4], 5]"""
    ),
    (
        171,
        "Massivni teskari qilish: reverse va reverse!",
        "Elementlar tartibini teskarisiga o'giring.",
        """sozlar = ["bir", "ikki", "uch"]
puts "Teskari: #{sozlar.reverse.inspect}"
""",
        "'reverse' massiv elementlarini teskari tartibda saqlovchi yangi massiv qaytaradi.",
        """Teskari: ["uch", "ikki", "bir"]"""
    ),
    (
        172,
        "Massivni saralash: sort va sort!",
        "Sonlar va so'zlarni o'sish tartibida saralang.",
        """sonlar = [45, 12, 89, 3, 27]
ismlar = ["Zafar", "Ali", "Botir"]

puts "Saralangan sonlar: #{sonlar.sort.inspect}"
puts "Saralangan ismlar: #{ismlar.sort.inspect}"
""",
        "'sort' obyektlarning `<=>` operatori asosida elementlarni tabiiy o'sish tartibida tartiblaydi.",
        """Saralangan sonlar: [3, 12, 27, 45, 89]
Saralangan ismlar: ["Ali", "Botir", "Zafar"]"""
    ),
    (
        173,
        "Massiv o'lchami: length, size, count va empty?",
        "Massiv uzunligi va undagi ma'lum shartga mos elementlar sonini hisoblang.",
        """sonlar = [10, 20, 30, 20, 40]

puts "size: #{sonlar.size}"
puts "Bo'shmi? #{sonlar.empty?}"
puts "20 soni necha marta uchragan? #{sonlar.count(20)}"
puts "25 dan katta sonlar soni: #{sonlar.count { |x| x > 25 }}"
""",
        "'size' va 'length' elementlar sonini beradi; 'count' esa berilgan qiymat yoki blok shartiga mos elementlar miqdorini aniqlaydi.",
        """size: 5
Bo'shmi? false
20 soni necha marta uchragan? 2
25 dan katta sonlar soni: 2"""
    ),
    (
        174,
        "Massivlarni ko'paytirish va to'ldirish",
        "Boshlang'ich nollar bilan to'ldirilgan 5 o'lchamli massiv yarating.",
        """nollar = [0] * 5
standart = Array.new(4, "tayyor")

puts "nollar: #{nollar.inspect}"
puts "standart: #{standart.inspect}"
""",
        "'[element] * n' massivni n marta takrorlab kengaytiradi.",
        """nollar: [0, 0, 0, 0, 0]
standart: ["tayyor", "tayyor", "tayyor", "tayyor"]"""
    ),
    (
        175,
        "Tasodifiy element tanlash: sample va shuffle",
        "Lotereya o'yinida ishtirokchilar orasidan tasodifiy g'olibni aniqlang.",
        """ishtirokchilar = ["Ali", "Vali", "Hasan", "Husan"]

# sample tasodifiy element qaytaradi
# shuffle massiv elementlarini tasodifiy aralashtiradi
puts "G'olib aniqlandi: #{ishtirokchilar.sample}"
puts "Aralashtirilgan ro'yxat: #{ishtirokchilar.shuffle.class}"
""",
        "'sample' tasodifiy bitta elementni, 'shuffle' esa aralashtirilgan yangi massivni hosil qiladi.",
        """G'olib aniqlandi: """ + "Ali" + """
Aralashtirilgan ro'yxat: Array"""
    ),
    (
        176,
        "Massivlarni bir-biriga bog'lash: zip",
        "Ismlar va ularning yoshlari massivlarini juftliklarga birlashtiring.",
        """ismlar = ["Nodir", "Zilola", "Temur"]
yoshlar = [25, 22, 28]

juftliklar = ismlar.zip(yoshlar)
puts "Bog'langan juftliklar: #{juftliklar.inspect}"
""",
        "'zip' bir nechta massivlarning mos indeksdagi elementlarini birlashtirib, ichki massivlar (juftliklar) yaratadi.",
        """Bog'langan juftliklar: [["Nodir", 25], ["Zilola", 22], ["Temur", 28]]"""
    ),
    (
        177,
        "Kombinatsiyalar: combination va permutation",
        "3 ta elementdan 2 talik barcha kombinatsiyalarni tuzing.",
        """harflar = ["A", "B", "C"]
kombinatsiyalar = harflar.combination(2).to_a

puts "2 talik kombinatsiyalar: #{kombinatsiyalar.inspect}"
""",
        "'combination(n)' tartib ahamiyatsiz bo'lgan barcha n-talik guruhlarni hosil qiladi.",
        """2 talik kombinatsiyalar: [["A", "B"], ["A", "C"], ["B", "C"]]"""
    ),
    (
        178,
        "Hash (Assotsiativ massiv) yaratish usullari",
        "Hash yaratishning klassik raketa (`=>`) va zamonaviy JSON-simon (`kalit: qiymat`) sintaksislarini qo'llang.",
        """h1 = { "ism" => "Ali", "yosh" => 25 } # String kalitlar
h2 = { ism: "Vali", yosh: 30 }          # Symbol kalitlar

puts "h1: #{h1.inspect}"
puts "h2: #{h2.inspect}"
puts "h2[:ism]: #{h2[:ism]}"
""",
        "Zamonaviy Ruby kodida Symbol kalitli `{ kalit: qiymat }` sintaksisi keng qo'llaniladi. U ichki ma'noda `{ :kalit => qiymat }` ning qulay ekvivalentidir.",
        """h1: {"ism"=>"Ali", "yosh"=>25}
h2: {:ism=>"Vali", :yosh=>30}
h2[:ism]: Vali"""
    ),
    (
        179,
        "Hash elementlariga murojaat: [] va fetch",
        "Mavjud bo'lmagan kalitga murojaat qilganda xavfsiz default qiymat qaytarishni ko'rsating.",
        """sozlamalar = { rejim: "dark", til: "uz" }

puts "rejim ([]): #{sozlamalar[:rejim]}"
puts "shrift ([]): #{sozlamalar[:shrift].inspect}" # nil qaytadi

# fetch kalit topilmasa xato beradi yoki default qiymat qaytaradi
shrift = sozlamalar.fetch(:shrift, "Arial")
puts "shrift (fetch): #{shrift}"
""",
        "'[]' kalit topilmasa nil qaytaradi. 'fetch(key, default)' esa kalit bo'lmagan taqdirda xavfsiz standart qiymat berish imkonini yaratadi.",
        """rejim ([]): dark
shrift ([]): nil
shrift (fetch): Arial"""
    ),
    (
        180,
        "fetch xatoligi (KeyError) va blok bilan default qiymat",
        "Kalit majburiy bo'lganda fetch orqali dastur xatosini aniqlashni ko'rsating.",
        """profil = { login: "admin" }

baho = profil.fetch(:email) { |kalit| "#{kalit} topilmadi!" }
puts "Natija: #{baho}"
""",
        "Agar 'fetch' ga faqat bitta argument berilsa va kalit topilmasa, u 'KeyError' istisnosini keltirib chiqaradi. Blok berilsa, blokdagi logika ishga tushadi.",
        """Natija: email topilmadi!"""
    ),
    (
        181,
        "Hashga element qo'shish va yangilash",
        "Mavjud Hashga yangi maydonlar qo'shing va qiymatlarni yangilang.",
        """kitob = { sarlavha: "O'tkan kunlar", muallif: "Abdulla Qodiriy" }
kitob[:yil] = 1925
kitob[:sahifalar] = 400

puts "Yangilangan kitob: #{kitob.inspect}"
""",
        "'hash[kalit] = qiymat' agar kalit mavjud bo'lsa uni yangilaydi, aks holda yangi kalit-qiymat juftligini kiritadi.",
        """Yangilangan kitob: {:sarlavha=>"O'tkan kunlar", :muallif=>"Abdulla Qodiriy", :yil=>1925, :sahifalar=>400}"""
    ),
    (
        182,
        "Hashdan element o'chirish: delete",
        "Foydalanuvchi ma'lumotlaridan parolni o'chirib tashlang.",
        """user_data = { id: 1, email: "user@mail.uz", password_hash: "secret123" }
ochirilgan = user_data.delete(:password_hash)

puts "O'chirildi: #{ochirilgan}"
puts "Qolgan ma'lumotlar: #{user_data.inspect}"
""",
        "'delete(kalit)' ko'rsatilgan kalitni Hashdan o'chiradi va uning qiymatini qaytaradi.",
        """O'chirildi: secret123
Qolgan ma'lumotlar: {:id=>1, :email=>"user@mail.uz"}"""
    ),
    (
        183,
        "Kalit va qiymat mavjudligini tekshirish: key? va value?",
        "Hashda aniq kalit yoki qiymat borligini tezkor tekshiring.",
        """mashina = { rusumi: "Cobalt", rang: "Oq", yil: 2024 }

puts "rusumi kaliti bormi? #{mashina.key?(:rusumi)}"
puts "narx kaliti bormi? #{mashina.key?(:narx)}"
puts "'Oq' qiymati bormi? #{mashina.value?('Oq')}"
""",
        "'key?' (sinonimlari: has_key?, include?, member?) kalitning mavjudligini O(1) tezlikda tekshiradi. 'value?' esa barcha qiymatlar ichidan qidiradi.",
        """rusumi kaliti bormi? true
narx kaliti bormi? false
'Oq' qiymati bormi? true"""
    ),
    (
        184,
        "Barcha kalitlar va qiymatlar ro'yxati: keys va values",
        "Hashdagi barcha kalitlarni va barcha qiymatlarni massiv sifatida ajrating.",
        """valyutalar = { USD: 12800, EUR: 13900, RUB: 140 }

puts "Kalitlar: #{valyutalar.keys.inspect}"
puts "Qiymatlar: #{valyutalar.values.inspect}"
""",
        "'keys' barcha kalitlar massivini, 'values' barcha qiymatlar massivini qaytaradi.",
        """Kalitlar: [:USD, :EUR, :RUB]
Qiymatlar: [12800, 13900, 140]"""
    ),
    (
        185,
        "Hashlarni birlashtirish: merge va merge!",
        "Standart sozlamalar ustiga foydalanuvchi maxsus sozlamalarini yozing.",
        """standart = { tema: "light", font_size: 14, xabar: true }
maxsus = { tema: "dark", font_size: 18 }

yakuniy = standart.merge(maxsus)
puts "Yakuniy sozlamalar: #{yakuniy.inspect}"
""",
        "'merge' ikkinchi hashdagi qiymatlar bilan birinchisini to'ldiradi va yangi hash hosil qiladi. Mos kelgan kalitlarda ikkinchi hashning qiymati ustunlik qiladi.",
        """Yakuniy sozlamalar: {:tema=>"dark", :font_size=>18, :xabar=>true}"""
    ),
    (
        186,
        "merge da konfliktlarni blok orqali hal qilish",
        "Ikkita savatchani birlashtirishda mahsulotlar miqdorini qo'shib hisoblang.",
        """ombor1 = { olma: 10, nok: 5 }
ombor2 = { olma: 15, uzum: 20 }

birlashgan = ombor1.merge(ombor2) do |kalit, eski_son, yangi_son|
  eski_son + yangi_son
end

puts "Birlashgan ombor: #{birlashgan.inspect}"
""",
        "'merge' ga blok berilganda bir xil nomli kalitlar uchrasa blok chaqiriladi: `|kalit, eski_val, yangi_val|`. Blokdan qaytgan qiymat yangi qiymat sifatida saqlanadi.",
        """Birlashgan ombor: {:olma=>25, :nok=>5, :uzum=>20}"""
    ),
    (
        187,
        "Ichma-ich (Nested) Hashlar va dig metodi",
        "Murakkab JSON ma'lumotidan ichki maydonni NoMethodError siz xavfsiz oling.",
        """javob = {
  status: "success",
  data: {
    user: {
      profile: {
        shahar: "Buxoro"
      }
    }
  }
}

shahar = javob.dig(:data, :user, :profile, :shahar)
mamlakat = javob.dig(:data, :user, :manzil, :mamlakat)

puts "Shahar: #{shahar}"
puts "Mamlakat (mavjud emas): #{mamlakat.inspect}"
""",
        "'dig(*keys)' zanjirli qidiruvni amalga oshiradi. Yo'lda istalgan kalit topilmasa yoki nil bo'lsa, xato tashlamasdan darhol nil qaytaradi.",
        """Shahar: Buxoro
Mamlakat (mavjud emas): nil"""
    ),
    (
        188,
        "Hash standart default qiymati: Hash.new(0)",
        "Matndagi so'zlar sonini hisoblash uchun boshlang'ich qiymati 0 bo'lgan Hash yarating.",
        """matn = "olma anor olma nok anor olma"
hisoblagich = Hash.new(0)

matn.split.each do |soz|
  hisoblagich[soz] += 1
end

puts "So'zlar statistikasi: #{hisoblagich.inspect}"
""",
        "'Hash.new(default)' agar kalit topilmasa avtomatik belgilangan standart qiymatni qaytaradi. Bu `hisoblagich[soz] += 1` kabi amallarda `nil + 1` xatosining oldini oladi.",
        """So'zlar statistikasi: {"olma"=>3, "anor"=>2, "nok"=>1}"""
    ),
    (
        189,
        "Hash.new bloki bilan avtomatik massiv yaratish",
        "Talabalarni guruhlar bo'yicha toifalashda avtomatik bo'sh massiv ochuvchi Hash tuzing.",
        """guruhlar = Hash.new { |hash, key| hash[key] = [] }

guruhlar["Guruh-A"] << "Alisher"
guruhlar["Guruh-A"] << "Bobur"
guruhlar["Guruh-B"] << "Charos"

puts "Guruhlar: #{guruhlar.inspect}"
""",
        "'Hash.new { |h, k| h[k] = [] }' yangi kalit birinchi marta so'ralganda aynan shu kalit uchun yangi mustaqil massiv nusxasini biriktiradi.",
        """Guruhlar: {"Guruh-A"=>["Alisher", "Bobur"], "Guruh-B"=>["Charos"]}"""
    ),
    (
        190,
        "Hash kalitlarini o'zgartirish: transform_keys",
        "String kalitli Hashni Symbol kalitlarga bir zumda o'tkazing.",
        """xom_hash = { "id" => 101, "nom" => "Smartfon" }
simvol_hash = xom_hash.transform_keys(&:to_sym)

puts "Symbol kalitli Hash: #{simvol_hash.inspect}"
""",
        "'transform_keys' har bir kalit ustida ko'rsatilgan amalni bajarib yangi Hash qaytaradi. Rails-dagi `symbolize_keys` metodi aynan shu mexanizmga asoslangan.",
        """Symbol kalitli Hash: {:id=>101, :nom=>"Smartfon"}"""
    ),
    (
        191,
        "Hash qiymatlarini o'zgartirish: transform_values",
        "Dollardagi narxlarni so'mga aylantiruvchi qulay transformatsiyani bajaring.",
        """narxlar_usd = { non: 1, sut: 2, goʻsht: 8 }
kurs = 12800

narxlar_uzs = narxlar_usd.transform_values { |narx| narx * kurs }
puts "Narxlar so'mda: #{narxlar_uzs.inspect}"
""",
        "'transform_values' kalitlarga tegmasdan faqat qiymatlarni o'zgartiradi.",
        """Narxlar so'mda: {:non=>12800, :sut=>25600, :goʻsht=>102400}"""
    ),
    (
        192,
        "Hashni massivga va massivni Hashga aylantirish: to_a va to_h",
        "Hash va juftliklar massivi o'rtasida konvertatsiya qiling.",
        """hash = { a: 1, b: 2 }
massiv = hash.to_a
qayta_hash = massiv.to_h

puts "Hashdan massivga: #{massiv.inspect}"
puts "Massivdan Hashga: #{qayta_hash.inspect}"
""",
        "'to_a' Hashni `[[kalit1, qiymat1], [kalit2, qiymat2]]` massiviga aylantiradi, 'to_h' esa bunday massivdan qayta Hash yasaydi.",
        """Hashdan massivga: [[:a, 1], [:b, 2]]
Massivdan Hashga: {:a=>1, :b=>2}"""
    ),
    (
        193,
        "Hashni teskarisiga o'girish: invert",
        "Kalitlar va qiymatlar o'rnini almashtiring.",
        """lugat = { "cat" => "mushuk", "dog" => "kuchuk" }
teskari_lugat = lugat.invert

puts "Teskari lug'at: #{teskari_lugat.inspect}"
puts "mushuk inglizcha nima? #{teskari_lugat['mushuk']}"
""",
        "'invert' metodi qiymatlarni kalitlarga, kalitlarni esa qiymatlarga aylantiradi.",
        """Teskari lug'at: {"mushuk"=>"cat", "kuchuk"=>"dog"}
mushuk inglizcha nima? cat"""
    ),
    (
        194,
        "Hash qismlarini filtrlash: select va reject",
        "Mijozlar orasidan faqat yoshi 18 dan kattalarni ajratib oling.",
        """yoshlar = { Ali: 22, Vali: 16, Hasan: 19, Husan: 15 }

katta_yoshlilar = yoshlar.select { |ism, yosh| yosh >= 18 }
kichiklar = yoshlar.reject { |ism, yosh| yosh >= 18 }

puts "Kattalar: #{katta_yoshlilar.inspect}"
puts "Kichiklar: #{kichiklar.inspect}"
""",
        "'select' shart rost bo'lgan juftliklarni, 'reject' esa shart rost bo'lmagan juftliklarni o'z ichiga olgan yangi Hash qaytaradi.",
        """Kattalar: {:Ali=>22, :Hasan=>19}
Kichiklar: {:Vali=>16, :Husan=>15}"""
    ),
    (
        195,
        "Hash qismini tanlab olish: slice",
        "Katta foydalanuvchi obyektidan faqat ommaviy ko'rsatiladigan maydonlarni ajrating.",
        """profil = { id: 1, ism: "Aziz", email: "aziz@mail.uz", parol: "hash123", rol: "admin" }
ommaviy = profil.slice(:id, :ism, :rol)

puts "Ommaviy profil: #{ommaviy.inspect}"
""",
        "'slice(*keys)' ko'rsatilgan kalitlar bo'yicha qism Hash ajratib beradi.",
        """Ommaviy profil: {:id=>1, :ism=>"Aziz", :rol=>"admin"}"""
    ),
    (
        196,
        "Hash elementlarini saralash: sort_by",
        "Mahsulotlarni narxi bo'yicha arzonidan qimmatiga qarab saralang.",
        """ombor = { noutbuk: 800, sichqoncha: 15, monitor: 250 }
saralangan = ombor.sort_by { |nom, narx| narx }.to_h

puts "Narx bo'yicha saralangan: #{saralangan.inspect}"
""",
        "'sort_by' blok natijasi bo'yicha tartiblab juftliklar massivini beradi, '.to_h' orqali uni qayta saralangan Hashga aylantiramiz.",
        """Narx bo'yicha saralangan: {:sichqoncha=>15, :monitor=>250, :noutbuk=>800}"""
    ),
    (
        197,
        "Hashda kompaktlash: compact metodi",
        "Hash ichidagi qiymati nil bo'lgan bo'sh maydonlarni tozalang.",
        """forma = { ism: "Farrux", telefon: "+998901234567", shahar: nil }
toza_forma = forma.compact

puts "Tozalangan forma: #{toza_forma.inspect}"
""",
        "'compact' qiymati nil bo'lgan barcha juftliklarni olib tashlaydi.",
        """Tozalangan forma: {:ism=>"Farrux", :telefon=>"+998901234567"}"""
    ),
    (
        198,
        "Massiv va Hashlar kombinatsiyasi: Jadval ko'rinishidagi ma'lumotlar",
        "Foydalanuvchilar massivini tahlil qilib, o'rtacha yoshni hisoblang.",
        """foydalanuvchilar = [
  { ism: "Ali", yosh: 20 },
  { ism: "Vali", yosh: 25 },
  { ism: "Gani", yosh: 30 }
]

yoshlar_yigindisi = foydalanuvchilar.map { |u| u[:yosh] }.sum
ortacha = yoshlar_yigindisi.to_f / foydalanuvchilar.size

puts "Foydalanuvchilar soni: #{foydalanuvchilar.size}"
puts "O'rtacha yosh: #{ortacha}"
""",
        "Massiv ichidagi Hashlar veb ilovalarda ma'lumotlar bazasi qatorlarini ifodalashning asosiy shaklidir.",
        """Foydalanuvchilar soni: 3
O'rtacha yosh: 25.0"""
    ),
    (
        199,
        "Hash elementlarini guruhlash: group_by",
        "Talabalarni bahosi bo'yicha guruhlarga ajrating.",
        """natijalar = [
  { ism: "Anvar", baho: 5 },
  { ism: "Bekzod", baho: 4 },
  { ism: "Dilshod", baho: 5 },
  { ism: "Eldor", baho: 3 }
]

guruhlangan = natijalar.group_by { |t| t[:baho] }
puts "5 baho olganlar: #{guruhlangan[5].map { |t| t[:ism] }.inspect}"
puts "4 baho olganlar: #{guruhlangan[4].map { |t| t[:ism] }.inspect}"
""",
        "'group_by' to'plam elementlarini blok qaytargan qiymat bo'yicha guruhlab yangi Hash qaytaradi.",
        """5 baho olganlar: ["Anvar", "Dilshod"]
4 baho olganlar: ["Bekzod"]"""
    ),
    (
        200,
        "Amaliy loyiha: E-tijorat savatchasi va buyurtmalar hisob-kitob tizimi",
        "Mahsulotlar savatchasi, chegirmalar va yakuniy kvitansiya hisob-kitobini massiv va hashlar yordamida to'liq amalga oshiring.",
        """savatcha = [
  { id: 1, nom: "Klaviatura", narx: 45.0, soni: 2 },
  { id: 2, nom: "Sichqoncha", narx: 20.0, soni: 1 },
  { id: 3, nom: "Kovrik", narx: 10.0, soni: 3 }
]

jami_summa = 0.0
puts "========================================="
puts "ONLINE DO'KON KVITANSIYASI"
puts "========================================="

savatcha.each do |item|
  summa = item[:narx] * item[:soni]
  jami_summa += summa
  puts "#{item[:nom].ljust(15)} x #{item[:soni]} = $#{'%.2f' % summa}"
end

chegirma_foiz = jami_summa > 100 ? 10 : 0
chegirma_summa = jami_summa * (chegirma_foiz / 100.0)
tolov = jami_summa - chegirma_summa

puts "-----------------------------------------"
puts "Jami:             $#{'%.2f' % jami_summa}"
puts "Chegirma (#{chegirma_foiz}%):    -$#{'%.2f' % chegirma_summa}"
puts "Yakuniy to'lov:   $#{'%.2f' % tolov}"
puts "========================================="
""",
        "Ushbu loyihada massivlar, hashlar, matn formatlash, hisoblagichlar va amaliy hisob-kitoblar e-tijorat muhitida mukammal birlashtirildi.",
        """=========================================
ONLINE DO'KON KVITANSIYASI
=========================================
Klaviatura      x 2 = $90.00
Sichqoncha      x 1 = $20.00
Kovrik          x 3 = $30.00
-----------------------------------------
Jami:             $140.00
Chegirma (10%):    -$14.00
Yakuniy to'lov:   $126.00
========================================="""
    )
]

register_topic("gen_04_massivlar.py", "ruby_04_massivlar_va_hashlar.md", 151, TASKS_04)
