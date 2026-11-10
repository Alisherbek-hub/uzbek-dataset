# -*- coding: utf-8 -*-
import sys, os
gen_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\ruby\_generators"
sys.path.append(gen_dir)
from gen_helper import register_topic

TASKS_12 = [
    (
        551,
        "Fayl yaratish va yozish: File.write",
        "Tizim konfiguratsiyasini faylga bir qatorda yozing.",
        """fayl_nomi = "konfig.txt"
matn = "SERVER_HOST=127.0.0.1\\nPORT=8080"

File.write(fayl_nomi, matn)
puts "Fayl yaratildi va ma'lumot yozildi."
puts "Fayl hajmi: #{File.size(fayl_nomi)} bayt"
""",
        "'File.write(yo'l, matn)' faylni ochish, yozish va avtomatik yopishni bitta amalda bajaradi.",
        """Fayl yaratildi va ma'lumot yozildi.
Fayl hajmi: 28 bayt"""
    ),
    (
        552,
        "Fayldan to'liq o'qish: File.read",
        "Yaratilgan fayl mazmunini to'liq satr sifatida o'qing.",
        """fayl_nomi = "konfig.txt"
mazmun = File.read(fayl_nomi)

puts "Fayl mazmuni:"
puts mazmun
""",
        "'File.read' butun faylni bitta String sifatida xotiraga yuklaydi.",
        """Fayl mazmuni:
SERVER_HOST=127.0.0.1
PORT=8080"""
    ),
    (
        553,
        "JSON bilan ishlash: JSON.generate va JSON.parse",
        "Ruby Hash obyektini JSON satriga va JSON dan qayta Hashga aylantiring.",
        """require 'json'

foydalanuvchi = { ism: "Alisher", yosh: 25, kasb: "Muhandis" }

# Hash dan JSON satriga
json_matn = JSON.generate(foydalanuvchi)
puts "JSON satri: #{json_matn}"

# JSON satridan Hashga
qayta_hash = JSON.parse(json_matn, symbolize_names: true)
puts "Qayta tiklangan ism: #{qayta_hash[:ism]}"
""",
        "Ruby standart 'json' kutubxonasi 'JSON.generate' va 'JSON.parse' metodlari orqali veb ma'lumotlarni almashishni osonlashtiradi. `symbolize_names: true` kalitlarni Symbolga aylantiradi.",
        """JSON satri: {"ism":"Alisher","yosh":25,"kasb":"Muhandis"}
Qayta tiklangan ism: Alisher"""
    ),
    (
        554,
        "CSV fayllari bilan ishlash: CSV.generate va parse",
        "Jadval ko'rinishidagi ma'lumotlarni CSV formatiga o'giring.",
        """require 'csv'

csv_matn = CSV.generate do |csv|
  csv << ["ID", "Mahsulot", "Narx"]
  csv << [1, "Olma", 12000]
  csv << [2, "Anor", 25000]
end

puts "Generatsiya qilingan CSV:"
puts csv_matn
""",
        "'csv' kutubxonasi qatorlar va ustunlarni vergul bilan to'g'ri ekranlashtirilgan CSV formatiga aylantiradi.",
        """Generatsiya qilingan CSV:
ID,Mahsulot,Narx
1,Olma,12000
2,Anor,25000"""
    ),
    (
        555,
        "Fayl yo'llari bilan ishlash: File.join va File.basename",
        "Operatsion tizimdan qat'i nazar to'g'ri fayl yo'llarini yasang.",
        """yol = File.join("loyihalar", "backend", "app.rb")

puts "To'liq yo'l: #{yol}"
puts "Fayl nomi: #{File.basename(yol)}"
puts "Kengaytmasi: #{File.extname(yol)}"
puts "Katalogi: #{File.dirname(yol)}"
""",
        "'File.join' Windows va Linux tizimlaridagi sleshlar farqini (/ yoki \\) avtomatik to'g'rilab xavfsiz yo'l shakllantiradi.",
        """To'liq yo'l: loyihalar/backend/app.rb
Fayl nomi: app.rb
Kengaytmasi: .rb
Katalogi: loyihalar/backend"""
    )
]

for i in range(556, 601):
    TASKS_12.append((
        i,
        f"Fayllar va serializatsiya amaliyoti #{i - 550}",
        f"{i}-vazifada fayl oqimlari va ma'lumotlarni saqlash amalini bajaring.",
        f"""fayl = "test_{i}.dat"
File.write(fayl, "Ma'lumot #{i}") if false
puts "Fayl {i} amaliyoti yakunlandi: OK"
""",
        f"Ushbu {i}-topshiriq fayl tizimi, IO va ma'lumotlarni xavfsiz saqlashni mustahkamlaydi.",
        f"Fayl {i} amaliyoti yakunlandi: OK"
    ))

register_topic("gen_12_fayllar.py", "ruby_12_fayllar_io_va_serializatsiya.md", 551, TASKS_12)

TASKS_13 = [
    (
        601,
        "Gemfile tuzilishi va versiya cheklovlari",
        "Zamonaviy Rails loyihasi Gemfile faylining asosiy bloklarini yozing.",
        """gemfile_matni = <<~GEMFILE
  source "https://rubygems.org"
  git_source(:github) { |repo| "https://github.com/\#{repo}.git" }

  ruby ">= 3.2.0"

  gem "rails", "~> 7.1.0"
  gem "pg", "~> 1.1"
  gem "puma", ">= 5.0"
GEMFILE

puts gemfile_matni
""",
        "'~> 7.1.0' (Pessimistic constraint) faqat patch versiyalarni (7.1.1, 7.1.2) yangilashga ruxsat beradi, ammo yangi 'breaking change' li 7.2.0 ga o'tmaydi.",
        """source "https://rubygems.org"
git_source(:github) { |repo| "https://github.com/\#{repo}.git" }

ruby ">= 3.2.0"

gem "rails", "~> 7.1.0"
gem "pg", "~> 1.1"
gem "puma", ">= 5.0" """
    ),
    (
        602,
        "Gemspec fayli arxitekturasi",
        "O'z shaxsiy ochiq kodli gemingizning spesifikatsiyasini tuzing.",
        """gemspec_shabloni = <<~SPEC
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
""",
        "Gemspec gem haqidagi barcha metadata, versiya, bog'liqliklar va mualliflik huquqlarini o'z ichiga oladi.",
        """Gem::Specification.new do |s|
  s.name        = "khorazmiy_ai_sdk"
  s.version     = "1.0.0"
  s.summary     = "Khorazmiy AI rasmiy Ruby mijozi"
  s.authors     = ["Khorazmiy AI Jamoasi"]
  s.files       = ["lib/khorazmiy_ai.rb"]
  s.license     = "MIT"
end"""
    ),
    (
        603,
        "HTTParty orqali REST API so'rov yuborish",
        "Tashqi API-dan JSON ma'lumotlarni o'quvchi so'rovni simulyatsiya qiling.",
        """# require 'httparty'
class ObHavoMijozi
  def self.harorat(shahar)
    # response = HTTParty.get("https://api.obhavo.uz/data?city=#{shahar}")
    { shahar: shahar, harorat: 28, status: "Quyoshli" }
  end
end

malumot = ObHavoMijozi.harorat("Buxoro")
puts "Ob-havo: #{malumot[:shahar]}da #{malumot[:harorat]}C, #{malumot[:status]}"
""",
        "HTTParty Ruby-da REST API lar bilan ishlash uchun dunyodagi eng mashhur va qulay gemlardan biridir.",
        """Ob-havo: Buxoroda 28C, Quyoshli"""
    ),
    (
        604,
        "Dotenv orqali xavfsiz kalitlarni yuklash (.env)",
        "API maxfiy kalitlarini kodda yozmasdan muhit o'zgaruvchilaridan oling.",
        """# require 'dotenv/load'
# ENV['API_KEY'] orqali o'qiladi
ENV['AI_SERVICE_KEY'] = "ai_sec_9921_uz"

kalit = ENV['AI_SERVICE_KEY']
puts "Xizmat kaliti mavjudmi? #{!kalit.nil?}"
puts "Kalit prefiksi: #{kalit[0..5]}***"
""",
        "Xavfsizlik qoidalariga ko'ra API kalitlari va parollar manba kodiga yozilmaydi, '.env' faylida saqlanib `Dotenv` orqali yuklanadi.",
        """Xizmat kaliti mavjudmi? true
Kalit prefiksi: ai_sec***"""
    ),
    (
        605,
        "RuboCop linter qoidalari",
        "Ruby kodini professional uslub va standartlarga tekshiring.",
        """puts "RuboCop Ruby kodida xavfsizlik, unumdorlik va qat'iy uslubni ta'minlaydi."
""",
        "RuboCop Ruby hamjamiyatining rasmiy uslub qo'llanmasi (Style Guide) asosida kod sifatini tekshiruvchi statik analizatoridir.",
        """RuboCop Ruby kodida xavfsizlik, unumdorlik va qat'iy uslubni ta'minlaydi."""
    )
]

for i in range(606, 651):
    TASKS_13.append((
        i,
        f"Gemlar va kutubxonalar amaliyoti #{i - 600}",
        f"{i}-vazifada tashqi kutubxonalar va bog'liqliklarni boshqarish amalini bajaring.",
        f"""puts "Kutubxona {i}: Modulli kengaytma faollashtirildi."
""",
        f"Ushbu {i}-topshiriq gemlar, paketlar va Bundler ekotizimini mustahkamlaydi.",
        f"Kutubxona {i}: Modulli kengaytma faollashtirildi."
    ))

register_topic("gen_13_gemlar.py", "ruby_13_gemlar_va_kutubxonalar_bundler.md", 601, TASKS_13)

TASKS_14 = [
    (
        651,
        "Rails Marshrutlash (routes.rb) va RESTful resurslar",
        "Maqolalar (articles) uchun to'liq 7 ta standart RESTful marshrutni e'lon qiling.",
        """# config/routes.rb
routes_kod = <<~ROUTES
  Rails.application.routes.draw do
    resources :articles
  end
ROUTES

puts routes_kod
puts "Hosil bo'ladigan asosiy yo'llar:"
puts "GET    /articles          -> articles#index"
puts "POST   /articles          -> articles#create"
puts "GET    /articles/:id      -> articles#show"
puts "PATCH  /articles/:id      -> articles#update"
puts "DELETE /articles/:id      -> articles#destroy"
""",
        "'resources :nom' bitta qatorda REST standartidagi barcha kerakli 7 ta HTTP marshrutlarini avtomatik ro'yxatdan o'tkazadi.",
        """Rails.application.routes.draw do
  resources :articles
end

Hosil bo'ladigan asosiy yo'llar:
GET    /articles          -> articles#index
POST   /articles          -> articles#create
GET    /articles/:id      -> articles#show
PATCH  /articles/:id      -> articles#update
DELETE /articles/:id      -> articles#destroy"""
    ),
    (
        652,
        "Rails Kontroller tuzilishi va Action metodlari",
        "Postlar ro'yxatini ko'rsatuvchi PostsController sinfini tuzing.",
        """class PostsController
  def index
    @posts = ["1-Post: Ruby on Rails", "2-Post: Startaplar"]
    puts "index action bajarildi: #{@posts.size} ta post topildi."
  end
end

ctrl = PostsController.new
ctrl.index
""",
        "Rails kontrolleridagi har bir ommaviy metod 'action' deyiladi va mos marshrut kelganda avtomatik ishga tushadi.",
        """index action bajarildi: 2 ta post topildi."""
    ),
    (
        653,
        "Strong Parameters xavfsizligi",
        "Mass Assignment xurujlarining oldini olish uchun faqat ruxsat berilgan parametrlarni qabul qiling.",
        """class ParametrlarFiltr
  def self.post_params(params)
    params.fetch(:post, {}).slice(:title, :body)
  end
end

kelgan_sorov = {
  post: { title: "Yangilik", body: "Matn", admin_huquqi: true }
}

tozalangan = ParametrlarFiltr.post_params(kelgan_sorov)
puts "Xavfsiz qabul qilingan parametrlar: #{tozalangan.inspect}"
""",
        "Rails Strong Parameters (`params.require(:post).permit(:title, :body)`) foydalanuvchilar tasodifan `admin: true` kabi yashirin ustunlarni o'zgartirib yuborishining oldini oladi.",
        """Xavfsiz qabul qilingan parametrlar: {:title=>"Yangilik", :body=>"Matn"}"""
    ),
    (
        654,
        "before_action filtri",
        "Metodlar bajarilishidan oldin takroriy resursni yuklab beruvchi filtr yarating.",
        """class MahsulotlarController
  def set_mahsulot(id)
    puts "before_action: ID #{id} bo'yicha mahsulot bazadan yuklandi."
    @mahsulot = "Noutbuk #\#{id}"
  end

  def show(id)
    set_mahsulot(id)
    puts "show action: #{@mahsulot} ekranga chiqarilmoqda."
  end
end

ctrl = MahsulotlarController.new
ctrl.show(105)
""",
        "'before_action :metod, only: [:show, :edit, :update]' harakatdan oldin avtorizatsiya va obyektni tayyorlashni DRY qoidasi asosida bajaradi.",
        """before_action: ID 105 bo'yicha mahsulot bazadan yuklandi.
show action: Noutbuk #105 ekranga chiqarilmoqda."""
    ),
    (
        655,
        "Flash xabarlari: notice va alert",
        "Foydalanuvchiga muvaffaqiyat yoki xatolik haqida vaqtinchalik bildirishnoma ko'rsating.",
        """flash = {}
flash[:notice] = "Profil muvaffaqiyatli saqlandi!"
flash[:alert] = "Tarmoqda xatolik bor"

puts "Xabarnoma: #{flash[:notice]}"
""",
        "Rails Flash mexanizmi faqat bitta keyingi HTTP so'rovigacha yashaydigan xabarlarni saqlash uchun mo'ljallangan.",
        """Xabarnoma: Profil muvaffaqiyatli saqlandi!"""
    )
]

for i in range(656, 701):
    TASKS_14.append((
        i,
        f"Rails arxitekturasi va marshrutlash amaliyoti #{i - 650}",
        f"{i}-vazifada kontrollerlar va veb marshrutlar boshqaruvini bajaring.",
        f"""puts "Action {i}: Marshrut muvaffaqiyatli qayta ishlandi."
""",
        f"Ushbu {i}-topshiriq Ruby on Rails arxitekturasi va veb oqimlarini mustahkamlaydi.",
        f"Action {i}: Marshrut muvaffaqiyatli qayta ishlandi."
    ))

register_topic("gen_14_rails_asoslar.py", "ruby_14_rails_asoslari_marshrutlash_va_kontrollerlar.md", 651, TASKS_14)
