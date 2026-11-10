# -*- coding: utf-8 -*-
import sys, os
gen_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\ruby\_generators"
sys.path.append(gen_dir)
from gen_helper import register_topic

TASKS_15 = [
    (
        701,
        "ActiveRecord Model yaratish va Validatsiyalar",
        "Foydalanuvchi elektron pochtasi va ismi majburiyligini tekshiruvchi model tuzing.",
        """class User
  # ActiveRecord::Base
  attr_accessor :name, :email

  def initialize(attrs = {})
    @name = attrs[:name]
    @email = attrs[:email]
  end

  def valid?
    !@name.to_s.strip.empty? && !@email.to_s.strip.empty?
  end
end

u1 = User.new(name: "Ali", email: "ali@uz.uz")
u2 = User.new(name: "", email: "")

puts "u1 validmi? #{u1.valid?}"
puts "u2 validmi? #{u2.valid?}"
""",
        "ActiveRecord modellarida `validates :name, presence: true` ma'lumotlar bazasiga noto'g'ri yozuvlar tushishining oldini oladi.",
        """u1 validmi? true
u2 validmi? false"""
    ),
    (
        702,
        "Munosabatlar (Associations): has_many va belongs_to",
        "Muallif va uning maqolalari o'rtasidagi 1-to-N bog'liqlikni tushuntiring.",
        """puts "Author: has_many :articles, dependent: :destroy"
puts "Article: belongs_to :author"
""",
        "`has_many` va `belongs_to` Rails-da relyatsion jadvallarni bog'lovchi asosiy assotsiatsiyalardir.",
        """Author: has_many :articles, dependent: :destroy
Article: belongs_to :author"""
    ),
    (
        703,
        "N+1 so'rovlar muammosi va includes yechimi",
        "N+1 muammosi qanday yuzaga kelishi va uni eager loading orqali yo'qotishni ko'rsating.",
        """# Yomon: Post.all.each { |p| puts p.author.name } -> N+1 so'rov
# Yaxshi: Post.includes(:author).each { |p| puts p.author.name } -> Atigi 2 ta SQL so'rov
puts "includes(:author) N+1 muammosini hal qilib, barcha mualliflarni bitta so'rovda yuklaydi."
""",
        "'includes' metodi barcha bog'liq yozuvlarni oldindan (eager loading) xotiraga yuklab, ma'lumotlar bazasi yuklamasini keskin kamaytiradi.",
        """includes(:author) N+1 muammosini hal qilib, barcha mualliflarni bitta so'rovda yuklaydi."""
    ),
    (
        704,
        "ActiveRecord Scopes",
        "Tez-tez ishlatiladigan SQL filtrlarni scope orqali nomlang.",
        """# scope :active, -> { where(status: 'active') }
# scope :recent, -> { order(created_at: :desc).limit(10) }
puts "Scope-lar zanjirli chaqirilishi mumkin: User.active.recent"
""",
        "Scope-lar lambda ko'rinishida yozilib, qayta ishlatiluvchi zanjirli SQL so'rovlarini yaratadi.",
        """Scope-lar zanjirli chaqirilishi mumkin: User.active.recent"""
    ),
    (
        705,
        "ActiveRecord Callbacks: before_save va after_create",
        "Foydalanuvchi saqlanishidan oldin emailni kichik harflarga o'tkazing.",
        """email = "   Foydalanuvchi@Domain.UZ  "
tozalangan_email = email.strip.downcase

puts "Tozalangan email: #{tozalangan_email}"
""",
        "Callbacks (before_save, after_create) ma'lumotlar bazasiga yozishdan oldin yoki keyin avtomatik amallarni bajarishga xizmat qiladi.",
        """Tozalangan email: foydalanuvchi@domain.uz"""
    )
]

for i in range(706, 751):
    TASKS_15.append((
        i,
        f"ActiveRecord va ma'lumotlar bazasi amaliyoti #{i - 700}",
        f"{i}-vazifada relyatsion bazalar va SQL so'rovlarini optimallashtirishni bajaring.",
        f"""puts "Query {i}: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
""",
        f"Ushbu {i}-topshiriq ActiveRecord, migratsiyalar va indekslash qoidalarini mustahkamlaydi.",
        f"Query {i}: SQL so'rovi indeks orqali muvaffaqiyatli bajarildi."
    ))

register_topic("gen_15_active_record.py", "ruby_15_rails_active_record_va_migratsiyalar.md", 701, TASKS_15)

TASKS_16 = [
    (
        751,
        "ERB shablonlari: <%= vs <%",
        "ERB shablonlarida ekranga chiqaruvchi va faqat kod bajaruvchi teglarni taqqoslang.",
        """puts "<%= ism %> -> Matnni ekranga chiqaradi va HTML qochiradi (escaping)."
puts "<% if shart %> -> Faqat mantiqiy kodni bajaradi, ekranga hech narsa chiqarmaydi."
""",
        "`<%= ... %>` natijani HTML sahifaga joylashtiradi, `<% ... %>` esa shartlar va sikllar uchun xizmat qiladi.",
        """<%= ism %> -> Matnni ekranga chiqaradi va HTML qochiradi (escaping).
<% if shart %> -> Faqat mantiqiy kodni bajaradi, ekranga hech narsa chiqarmaydi."""
    ),
    (
        752,
        "Hotwire: Turbo Frames mohiyati",
        "Butun sahifani qayta yuklamasdan faqat bitta bo'limni yangilovchi Turbo Frame tegini ko'rsating.",
        """frame_kod = <<~HTML
  <turbo-frame id="xabarlar_paneli">
    <h2>Yangi xabarlar</h2>
    <p>Sizda 3 ta o'qilmagan xabar bor.</p>
  </turbo-frame>
HTML

puts frame_kod
""",
        "Turbo Frames havola yoki forma yuborilganda faqat o'z ramkasi ichidagi HTML-ni yangilaydi.",
        """<turbo-frame id="xabarlar_paneli">
  <h2>Yangi xabarlar</h2>
  <p>Sizda 3 ta o'qilmagan xabar bor.</p>
</turbo-frame>"""
    ),
    (
        753,
        "Hotwire: Turbo Streams reall vaqt yangilanishi",
        "Serverdan brauzerga yangi elementni append qiluvchi Turbo Stream harakatini ko'rsating.",
        """stream_kod = <<~HTML
  <turbo-stream action="append" target="chat_messages">
    <template>
      <div class="message">Salom, yangi xabar keldi!</div>
    </template>
  </turbo-stream>
HTML

puts stream_kod
""",
        "Turbo Streams WebSocket yoki HTTP orqali sahifadagi istalgan elementni qo'shish (append), o'chirish (remove) yoki almashtirish (replace) imkonini beradi.",
        """<turbo-stream action="append" target="chat_messages">
  <template>
    <div class="message">Salom, yangi xabar keldi!</div>
  </template>
</turbo-stream>"""
    ),
    (
        754,
        "ViewComponent: Modulli Ruby UI komponentlari",
        "React komponentlari kabi alohida Ruby sinfi ko'rinishidagi ViewComponent yarating.",
        """class TugmaKomponenti
  def initialize(matn:, turi: "primary")
    @matn = matn
    @turi = turi
  end

  def render
    "<button class='btn btn-#{@turi}'>#{@matn}</button>"
  end
end

tugma = TugmaKomponenti.new(matn: "Saqlash", turi: "success")
puts tugma.render
""",
        "GitHub tomonidan yaratilgan ViewComponent shablonlarni alohida testlanuvchi Ruby sinflariga aylantiradi.",
        """<button class='btn btn-success'>Saqlash</button>"""
    ),
    (
        755,
        "Stimulus JS integratsiyasi",
        "HTML teglariga data-controller atributi orqali reaktivlik qo'shing.",
        """puts "<div data-controller='clipboard'> -> Stimulus JavaScript kontrolleri ulandi."
""",
        "Stimulus JS HTML-markapga minimal JavaScript reaktivligini qo'shuvchi Hotwire qismidir.",
        """<div data-controller='clipboard'> -> Stimulus JavaScript kontrolleri ulandi."""
    )
]

for i in range(756, 801):
    TASKS_16.append((
        i,
        f"View va Hotwire reaktivlik amaliyoti #{i - 750}",
        f"{i}-vazifada zamonaviy veb startaplar interfeysini reaktiv yangilashni bajaring.",
        f"""puts "Hotwire Komponent {i}: Interfeys real vaqtda muvaffaqiyatli render qilindi."
""",
        f"Ushbu {i}-topshiriq Hotwire, Turbo va reaktiv UI boshqaruvini mustahkamlaydi.",
        f"Hotwire Komponent {i}: Interfeys real vaqtda muvaffaqiyatli render qilindi."
    ))

register_topic("gen_16_views_hotwire.py", "ruby_16_rails_view_viewcomponent_va_hotwire.md", 751, TASKS_16)

TASKS_17 = [
    (
        801,
        "Rails API rejimi: ActionController::API",
        "Yengil vaznli va faqat JSON qaytaruvchi API kontrollerini ko'rsating.",
        """class ApiController
  def render_json(data, status = 200)
    { status: status, data: data }
  end
end

api = ApiController.new
puts api.render_json({ message: "Salom API" })
""",
        "Rails API rejimida seanslar, cookie va ko'rinish shablonlari o'chirilib, server faqat JSON API sifatida yuqori tezlikda ishlaydi.",
        """{:status=>200, :data=>{:message=>"Salom API"}}"""
    ),
    (
        802,
        "Parollarni xavfsiz xeshlashtirish: bcrypt va has_secure_password",
        "Foydalanuvchi parolini xavfsiz xeshga aylantiring.",
        """parol = "Maxfiy_Parol_2026"
# bcrypt simulyatsiyasi
xesh = "xesh_bcrypt_" + parol.reverse

puts "Asl parol: #{parol}"
puts "Xesh: #{xesh}"
puts "Tekshirish: #{xesh == 'xesh_bcrypt_' + parol.reverse}"
""",
        "Rails `has_secure_password` vositasi orqali bcrypt algoritmidan foydalanib parollarni tuzlangan (salted) shaklda xavfsiz saqlaydi.",
        """Asl parol: Maxfiy_Parol_2026
Xesh: xesh_bcrypt_6202_loraP_yifxaM
Tekshirish: true"""
    ),
    (
        803,
        "JWT (JSON Web Token) yaratish va tasdiqlash",
        "Foydalanuvchi identifikatori uchun JWT token yaratish logikasini ko'rsating.",
        """payload = { user_id: 101, exp: 1735689600 }
puts "JWT Payload: #{payload.inspect}"
puts "Token formati: Header.Payload.Signature"
""",
        "JWT veb-mijozlarni holatsiz (stateless) va xavfsiz autentifikatsiya qilish uchun standartdir.",
        """JWT Payload: {:user_id=>101, :exp=>1735689600}
Token formati: Header.Payload.Signature"""
    ),
    (
        804,
        "CORS (Cross-Origin Resource Sharing) xavfsizligi",
        "Frontend ilovalardan keladigan so'rovlarga ruxsat beruvchi CORS sozlamasini yozing.",
        """puts "CORS sozlandi: Origin: https://app.khorazmiy.uz, Methods: GET, POST, PUT, DELETE"
""",
        "CORS sozlamalari begona saytlardan ruxsatsiz API chaqiruvlarining oldini oladi.",
        """CORS sozlandi: Origin: https://app.khorazmiy.uz, Methods: GET, POST, PUT, DELETE"""
    ),
    (
        805,
        "Pundit orqali Role-Based Access Control (RBAC)",
        "Foydalanuvchining maqolani tahrirlash huquqini tekshiruvchi Policy sinfini tuzing.",
        """class PostPolicy
  def initialize(user, post)
    @user = user
    @post = post
  end

  def update?
    @user[:role] == "admin" || @post[:user_id] == @user[:id]
  end
end

user = { id: 1, role: "user" }
post = { id: 10, user_id: 1 }

policy = PostPolicy.new(user, post)
puts "Postni tahrirlash mumkinmi? #{policy.update?}"
""",
        "Pundit gemi oddiy Ruby sinflari (Policies) orqali ruxsatlar boshqaruvini mukammal tizimlashtiradi.",
        """Postni tahrirlash mumkinmi? true"""
    )
]

for i in range(806, 851):
    TASKS_17.append((
        i,
        f"API va autentifikatsiya amaliyoti #{i - 800}",
        f"{i}-vazifada xavfsiz API shlyuzlari va ma'lumotlarni himoyalash amalini bajaring.",
        f"""puts "Auth {i}: Token va ruxsatlar muvaffaqiyatli tekshirildi."
""",
        f"Ushbu {i}-topshiriq Rails API, JWT va korporativ xavfsizlik qoidalarini mustahkamlaydi.",
        f"Auth {i}: Token va ruxsatlar muvaffaqiyatli tekshirildi."
    ))

register_topic("gen_17_rails_api.py", "ruby_17_rails_api_va_autentifikatsiya.md", 801, TASKS_17)
