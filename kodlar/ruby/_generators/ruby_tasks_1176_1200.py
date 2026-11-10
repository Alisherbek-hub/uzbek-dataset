# -*- coding: utf-8 -*-
"""
Ruby 24-modul: 1176 dan 1200 gacha bo'lgan topshiriqlar
Web hujumlaridan himoya (CSRF, XSS, SQLi), Rack::Attack va Kiberxavfsizlik Auditi
"""

TASKS_1176_1200 = [
    {
        "id": 1176,
        "title": "Sessiyalarni o'g'irlashdan himoyalash: Session Fixation va Session Regeneration",
        "desc": "Foydalanuvchi tizimga kirishidan oldin unga berilgan sessiya ID sini saqlab qolib, keyinchalik uning hisobiga kirib olish (Session Fixation) xavfini yo'qotish kerak.",
        "req": "Login vaqtida `reset_session` metodini chaqirish, yangi sessiya ID yaratish va eski ma'lumotlarni tozalash.",
        "code": """# app/controllers/sessions_controller.rb
class SessionsController < ApplicationController
  def create
    user = User.find_by(email: params[:email])

    if user&.authenticate(params[:password])
      # Session Fixation himoyasi: eski sessiya ID sini butunlay yo'q qilish
      reset_session

      # Yangi sessiyani shakllantirish
      session[:user_id] = user.id
      session[:authenticated_at] = Time.now.to_i

      redirect_to dashboard_path, notice: 'Tizimga muvaffaqiyatli kirdingiz'
    else
      flash.now[:alert] = 'Email yoki parol xato'
      render :new, status: :unauthorized
    end
  end
end""",
        "expl": "Session Fixation hujumida xakker qurbonga o'zi bilgan sessiya ID sini (masalan URL yoki cookie orqali) beradi. Agar login paytida `reset_session` chaqirilmasa, foydalanuvchi tizimga kirgach ham xuddi shu ID faol qoladi va xakker foydalanuvchi hisobiga kirib oladi."
    },
    {
        "id": 1177,
        "title": "Brute-Force hujumlaridan himoyalanish: hisobni avtomatik bloklash va ogohlantirish",
        "desc": "Parollarni avtomatlashtirilgan robotlar bilan sinab ko'rishni to'xtatish uchun ketma-ket muvaffaqiyatsiz urinishlarni hisoblab boruvchi va IP/foydalanuvchini bloklovchi modul kerak.",
        "req": "Redis yordamida muvaffaqiyatsiz urinishlarni hisoblash, 5 tadan oshsa bloklash va xavfsizlik xabarini yuborish.",
        "code": """# app/services/login_attempt_tracker.rb
class LoginAttemptTracker
  MAX_ATTEMPTS = 5
  LOCKOUT_DURATION = 15.minutes

  def initialize(email, ip_address)
    @key = "failed_logins:#{Digest::SHA256.hexdigest(email.downcase)}:#{ip_address}"
  end

  def record_failed_attempt!
    count = $redis.incr(@key)
    $redis.expire(@key, LOCKOUT_DURATION.to_i) if count == 1
    count
  end

  def locked_out?
    current = $redis.get(@key).to_i
    current >= MAX_ATTEMPTS
  end

  def reset!
    $redis.del(@key)
  end
end""",
        "expl": "Redis da `failed_logins` hisoblagichini TTL bilan saqlash ma'lumotlar bazasiga ortiqcha yuklama bermasdan, daqiqasiga o'n minglab hujumlarni osonlik bilan filtrlaydi."
    },
    {
        "id": 1178,
        "title": "JWT (JSON Web Token) xavfsiz imzolash va Asimmetrik (RS256) validatsiya",
        "desc": "Mikroxizmatlar arxitekturasida barcha xizmatlarga umumiy sirni (HMAC shared secret) tarqatmaslik uchun autentifikatsiya serveri JWT ni xususiy kalit bilan imzolashi, qolgan servislar esa faqat ochiq kalit bilan tekshirishi lozim.",
        "req": "`jwt` gemi, RS256 algoritmi, `iss`, `aud`, `exp` claims parametrlarini qat'iy tekshirish.",
        "code": """# frozen_string_literal: true
require 'jwt'

class AsymmetricJwtVault
  ALGORITHM = 'RS256'

  def self.encode_token(payload, private_key_pem)
    rsa_private = OpenSSL::PKey::RSA.new(private_key_pem)
    claims = payload.merge(
      iss: 'khorazmiy_auth_server',
      aud: 'khorazmiy_api_gateway',
      exp: Time.now.to_i + 3600 # 1 soat
    )
    JWT.encode(claims, rsa_private, ALGORITHM)
  end

  def self.decode_and_verify(token, public_key_pem)
    rsa_public = OpenSSL::PKey::RSA.new(public_key_pem)
    decoded, = JWT.decode(token, rsa_public, true, {
      algorithm: ALGORITHM,
      verify_iss: true,
      iss: 'khorazmiy_auth_server',
      verify_aud: true,
      aud: 'khorazmiy_api_gateway',
      verify_expiration: true
    })
    decoded
  rescue JWT::DecodeError => e
    warn "[JWT XATO]: #{e.message}"
    nil
  end
end""",
        "expl": "RS256 asimmetrik shifrlash usuli bo'lib, ommaviy kalitni istalgan tashqi mikroxizmat yoki frontendga berish xavfsizdir. Agar biron bir mikroxizmat buzib kirilsa ham, u yangi soxta JWT yarata olmaydi, chunki xususiy kalit faqat markaziy autentifikatsiya serverida saqlanadi."
    },
    {
        "id": 1179,
        "title": "OAuth2 / OpenID Connect Single Sign-On (SSO) provayderi xavfsizligi",
        "desc": "OmniAuth orqali Google, GitHub yoki Apple orqali kirishda CSRF va State tampering hujumlarining oldini olish lozim.",
        "req": "`state` parametrini tekshirish, `origin` va `nonce` parametrlarini tasdiqlash.",
        "code": """# config/initializers/omniauth.rb
Rails.application.config.middleware.use OmniAuth::Builder do
  provider :google_oauth2, ENV['GOOGLE_CLIENT_ID'], ENV['GOOGLE_CLIENT_SECRET'], {
    prompt: 'select_account',
    image_aspect_ratio: 'square',
    image_size: 100,
    # CSRF himoyasi uchun qat'iy state tekshiruvi
    provider_ignores_state: false
  }
end

# OmniAuth faqat POST so'rovlariga ruxsat berishi shart (CVE-2015-9284)
OmniAuth.config.allowed_request_methods = [:post]""",
        "expl": "OmniAuth da GET so'rovlari orqali login qilish xavflidir, chunki tajovuzkor `<img>` teglari orqali qurbonning hisobini o'z akkauntiga ulab qo'yishi mumkin. Faqat POST metodiga ruxsat berish va `state` parametrini tekshirish ushbu zaiflikni bartaraf qiladi."
    },
    {
        "id": 1180,
        "title": "Maxfiy parollarni ma'lumotlar bazasidan qidirishsiz va xeshsiz saqlamaslik auditi",
        "desc": "Ma'lumotlar bazasi zaxira nusxasi sizib chiqqanda ham hech bir parol yoki to'liq karta raqami ochiq holda ko'rinmasligi uchun model darajasida audit tekshiruvi kerak.",
        "req": "Faqat `password_digest` saqlash, `has_secure_password` dan foydalanish, modelda ochiq parol atributlarini xotirada qoldirmaslik.",
        "code": """# app/models/user.rb
class User < ApplicationRecord
  # has_secure_password parolni ochiq holda saqlamaydi,
  # balki uni bcrypt bilan xeshlab password_digest ga yozadi
  has_secure_password

  validates :password, length: { minimum: 12 }, allow_nil: true

  # Bazaga tasodifan parolni ochiq yozishdan himoyalovchi callback
  before_validation do
    self.password = nil if password.blank?
  end
end""",
        "expl": "`has_secure_password` virtual `password` va `password_confirmation` atributlarini yaratadi. Validatsiyadan so'ng parollar darhol xeshlanadi va SQL bazasiga faqat `password_digest` boradi. Ochiq matn hech qachon diskka yozilmaydi."
    },
    {
        "id": 1181,
        "title": "Rails CSRF himoyasi: protect_from_forgery with: :exception va Form Authenticity Token",
        "desc": "Boshqa zararli saytlar foydalanuvchining nomidan soxta POST/DELETE so'rovlarini (masalan pul o'tkazish) yubormasligi (Cross-Site Request Forgery) uchun qat'iy token tekshiruvini yoqish kerak.",
        "req": "`protect_from_forgery with: :exception`, har bir shaklda (form) `authenticity_token` kiritilishi va tekshirilishi.",
        "code": """# app/controllers/application_controller.rb
class ApplicationController < ActionController::Base
  # CSRF token mos kelmasa darhol Exception tashlash
  protect_from_forgery with: :exception

  # API kontrollerlari uchun null_session rejimiga o'tish
  # protect_from_forgery with: :null_session
end""",
        "expl": "Rails CSRF mexanizmi har bir foydalanuvchi sessiyasi uchun unikal kriptografik token yaratadi. Har bir HTML formaga yashirin `authenticity_token` maydoni kiritiladi. Brauzer POST qilganda, Rails tokenni dekodlab, sessiya kaliti bilan solishtiradi. Begona sayt bu tokenni o'qiy olmaydi (Same-Origin Policy tufayli)."
    },
    {
        "id": 1182,
        "title": "AJAX / Single Page Applications (SPA) uchun CSRF token almashinuvi",
        "desc": "React, Vue yoki oddiy `fetch()` chaqiruvlarida Rails backendga JSON so'rovlar yuborilganda CSRF tokenini `X-CSRF-Token` sarlavhasi orqali xavfsiz uzatish lozim.",
        "req": "HTML meta tegdan tokenni olish (`csrf_meta_tags`), har bir JavaScript so'roviga sarlavha qo'shish.",
        "code": """// app/javascript/packs/api_client.js
// Brauzer meta teglaridan CSRF tokenni ajratish
function getCsrfToken() {
  const meta = document.querySelector('meta[name="csrf-token"]');
  return meta ? meta.getAttribute('content') : '';
}

// Xavfsiz fetch chaqiruvi
export async function securePost(url, data) {
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'X-CSRF-Token': getCsrfToken() // Rails tekshiruvchi sarlavha
    },
    body: JSON.stringify(data)
  });

  return response.json();
}""",
        "expl": "SPA ilovalarda Rails sahifani to'liq qayta render qilmaydi. Shuning uchun `csrf_meta_tags` orqali berilgan token JavaScript xotirasiga olinadi va har bir AJAX so'rovida `X-CSRF-Token` HTTP sarlavhasida uzatiladi."
    },
    {
        "id": 1183,
        "title": "Content Security Policy (CSP) konfiguratsiyasi Rails 7 da (content_security_policy.rb)",
        "desc": "Xakker saytga zararli JavaScript kodini joylab ketgan taqdirda ham (XSS), brauzer begona domenlardan skriptlar yuklamasligi va inline skriptlarni bajarmasligi lozim.",
        "req": "`Rails.application.config.content_security_policy` orqali `default-src 'self'`, `script_src`, `nonce_generator` sozlash.",
        "code": """# config/initializers/content_security_policy.rb
Rails.application.configure do
  config.content_security_policy do |policy|
    policy.default_src :self
    policy.font_src    :self, :https, :data
    policy.img_src     :self, :https, :data
    policy.object_src  :none
    policy.script_src  :self, :https
    policy.style_src   :self, :https

    # Inline skriptlar uchun dinamik kriptografik Nonce
    # policy.script_src :self, :https, :nonce
  end

  # Har bir HTTP so'rovi uchun unikal nonce yaratish
  config.content_security_policy_nonce_generator = ->(request) { request.session.id.to_s }
  config.content_security_policy_nonce_directives = %w(script-src)
end""",
        "expl": "CSP (Content Security Policy) zamonaviy brauzer xavfsizligining eng kuchli himoyasidir. Agar sahifada hatto tajovuzkor kiritgan `<script>alert(1)</script>` tegi bo'lsa ham, unda to'g'ri `nonce` attributi bo'lmasa, brauzer skriptni ijro etishdan bosh tortadi."
    },
    {
        "id": 1184,
        "title": "XSS (Cross-Site Scripting) himoyasi: ERB::Util.html_escape, sanitize va SafeBuffer",
        "desc": "Foydalanuvchi sharhlarida va profillarida yozilgan HTML teglarni xavfsiz qabul qilish, zararli `<script>` va `onload=` hodisalarini filtrdan tozalash kerak.",
        "req": "`sanitize` helperidan foydalanish, faqat ruxsat etilgan teglarni (`tags: %w[b i p]`) qoldirish, `raw` yoki `html_safe` ni ehtiyotkorlik bilan ishlatish.",
        "code": """# app/helpers/sanitization_helper.rb
module SanitizationHelper
  # Xavfsiz boyitilgan matn chiqaruvchi
  def safe_render_user_bio(bio_text)
    # Faqat xavfsiz formatlash teglariga ruxsat berish
    sanitize(
      bio_text,
      tags: %w[b i em strong p br a],
      attributes: %w[href title]
    )
  end

  # Xom matnni majburiy ekranlash
  def force_escape(text)
    ERB::Util.html_escape(text)
  end
end""",
        "expl": "Rails ERB shablonlari sukut bo'yicha barcha o'zgaruvchilarni avtomatik tarzda HTML-escape qiladi (`<` belgisi `&lt;` ga aylanadi). Dasturchi hech qachon tekshirilmagan foydalanuvchi ma'lumotlariga `.html_safe` yoki `raw()` qo'llamasligi shart, aks holda Stored XSS zaifligi ochiladi."
    },
    {
        "id": 1185,
        "title": "SQL Injection va Arel: Xom SQL (find_by_sql, where(\"...\")) zaifliklarini audit qilish",
        "desc": "Foydalanuvchi kiritgan satrlarni to'g'ridan-to'g'ri SQL so'roviga birlashtirish (String Interpolation) orqali yuzaga keluvchi SQL Injection zaifligini bartaraf qilish lozim.",
        "req": "Xom SQL satrlarini parametrlangan (Parameterized/Prepared Statements) so'rovlarga o'zgartirish, Arel orqali xavfsiz SQL generatsiyasi.",
        "code": """# app/services/secure_user_search.rb
class SecureUserSearch
  # XAVFLI (SQL Injection mavjud):
  # User.where(\"name LIKE '%#{params[:query]}%'\") -- MUTLAQO MUMKIN EMAS!

  # XAVFSIZ: Parametrlangan so'rov
  def self.search_by_name(query)
    sanitized_query = "%#{ActiveRecord::Base.sanitize_sql_like(query)}%"
    User.where('name ILIKE ?', sanitized_query)
  end

  # Arel yordamida obyektga yo'naltirilgan xavfsiz so'rov
  def self.arel_search(min_age, status)
    users = User.arel_table
    User.where(
      users[:age].gteq(min_age).and(users[:status].eq(status))
    )
  end
end""",
        "expl": "Parametrlangan so'rovlarda ma'lumotlar bazasi drayveri kiruvchi ma'lumotlarni hech qachon SQL buyrug'i deb qabul qilmaydi, balki ularni faqatgina oddiy literallar sifatida qayta ishlaydi. Bu `OR 1=1` kabi barcha klassik SQL Injection hiylalarini bekor qiladi."
    },
    {
        "id": 1186,
        "title": "Strong Parameters orqali Mass Assignment zaifliklarini bartaraf etish",
        "desc": "Foydalanuvchi ro'yxatdan o'tayotganda HTTP so'rovi ichiga `admin: true` parametrini qo'shib yuborib o'zini admin qilib qo'yishining (Mass Assignment) oldini olish lozim.",
        "req": "`params.require(:user).permit(...)` dan foydalanish, faqat ruxsat etilgan maydonlarni filtrdan o'tkazish.",
        "code": """# app/controllers/users_controller.rb
class UsersController < ApplicationController
  def update
    @user = current_user
    if @user.update(user_params)
      redirect_to @user, notice: 'Profil yangilandi'
    else
      render :edit, status: :unprocessable_entity
    end
  end

  private

  # Strong Parameters: Faqat ushbu maydonlarni yangilashga ruxsat
  def user_params
    params.require(:user).permit(
      :name,
      :bio,
      :phone_number
      # :role, :is_admin, :balance kabi maydonlar kiritilmagan!
    )
  end
end""",
        "expl": "Strong Parameters Rails 4 dan boshlab majburiy qilingan. Agar so'rovda `permit` qilinmagan parametrlar kelsa, Rails ularni shunchaki e'tiborsiz qoldiradi va bazaga yozmaydi, bu esa ruxsatsiz huquqlarni oshirishni (Privilege Escalation) to'xtatadi."
    },
    {
        "id": 1187,
        "title": "SSRF (Server-Side Request Forgery) himoyasi: Ichki IP diapazonlarini filtrlash",
        "desc": "Ilova foydalanuvchi ko'rsatgan havola bo'yicha veb-sayt skrinshotini oladigan bo'lsa, xakker `http://169.254.169.254/latest/meta-data/` yoki `http://localhost:6379/` kiritib ichki tarmoqni skanerlashi mumkin.",
        "req": "IP manzilni tekshirish, maxfiy/lokal IP diapazonlarini (`IPAddr.new('127.0.0.0/8')`, `10.0.0.0/8`, `169.254.0.0/16`) bloklash.",
        "code": """# frozen_string_literal: true
require 'ipaddr'
require 'resolv'

class SsrfGuard
  PRIVATE_SUBNETS = [
    IPAddr.new('127.0.0.0/8'),       # Loopback
    IPAddr.new('10.0.0.0/8'),        # Private A
    IPAddr.new('172.16.0.0/12'),     # Private B
    IPAddr.new('192.168.0.0/16'),    # Private C
    IPAddr.new('169.254.0.0/16'),    # AWS Link-Local Metadata
    IPAddr.new('::1')                # IPv6 loopback
  ].freeze

  def self.safe_url?(raw_url)
    uri = URI.parse(raw_url)
    return false unless %w[http https].include?(uri.scheme)

    # DNS orqali barcha IP manzillarini aniqlash
    ips = Resolv.getaddresses(uri.host)
    return false if ips.empty?

    ips.all? do |ip_str|
      ip = IPAddr.new(ip_str)
      PRIVATE_SUBNETS.none? { |subnet| subnet.include?(ip) }
    end
  rescue URI::InvalidURIError, IPAddr::Error
    false
  end
end""",
        "expl": "SSRF bulutli tizimlarda (AWS, GCP) eng xavfli zaiflikdir. Xakker serverni o'zining nomidan ichki AWS Metadata servisiga murojaat qildirib, IAM xavfsizlik rollari va kalitlarini o'g'irlashi mumkin. Har bir tashqi so'rov oldidan IP diapazonlarini tekshirish shart."
    },
    {
        "id": 1188,
        "title": "Clickjacking himoyasi va X-Frame-Options sarlavhasi",
        "desc": "Tajovuzkor o'z saytiga shaffof `<iframe>` orqali bizning saytimizni joylashtirib, foydalanuvchini alqov orqali tugmalarni bosishga majburlashining (Clickjacking) oldini olish lozim.",
        "req": "`X-Frame-Options: SAMEORIGIN` yoki `DENY` sarlavhasini o'rnatish, CSP `frame-ancestors 'self'` ni belgilash.",
        "code": """# config/initializers/security_headers.rb
Rails.application.config.action_dispatch.default_headers.merge!(
  # Clickjacking himoyasi
  'X-Frame-Options' => 'DENY', # Hech qaysi sayt saytimizni iframe ichiga joylay olmaydi

  # XSS filtri
  'X-XSS-Protection' => '1; mode=block',

  # Mime-turi mos kelmasa yuklamaslik
  'X-Content-Type-Options' => 'nosniff'
)""",
        "expl": "`X-Frame-Options: DENY` brauzerga ushbu saytni biron bir boshqa sahifaning `<iframe>` tegi ichida ko'rsatishni qat'iyan taqiqlaydi. Natijada foydalanuvchi aldov yo'li bilan maxfiy amallarni bajarishga jalb qilinmaydi."
    },
    {
        "id": 1189,
        "title": "Fayl yuklash xavfsizligi: Mime-type spoofing va zararli SVG/Polyglot skriptlarni filtrlash",
        "desc": "Foydalanuvchi rasm o'rniga ichiga `<script>` yashiringan soxta SVG yoki PHP/Ruby bajariluvchi skriptlarni (Polyglot files) yuklashining oldini olish kerak.",
        "req": "`marcel` gemi orqali haqiqiy binar sehrli raqamlarni (Magic bytes) tekshirish, fayl kengaytmasi va uning ichki kontentini solishtirish.",
        "code": """# app/validators/secure_attachment_validator.rb
class SecureAttachmentValidator < ActiveModel::EachValidator
  ALLOWED_IMAGE_TYPES = %w[image/jpeg image/png image/webp].freeze

  def validate_each(record, attribute, value)
    return unless value.attached?

    # Fayl sarlavhasidagi emas, haqiqiy binar ma'lumot tahlili
    blob = value.blob
    detected_type = Marcel::MimeType.for(
      blob.download,
      name: blob.filename.to_s
    )

    unless ALLOWED_IMAGE_TYPES.include?(detected_type)
      record.errors.add(attribute, "faqat JPG, PNG yoki WebP formatida bo'lishi shart! Aniqlangan: #{detected_type}")
    end
  end
end""",
        "expl": "Fayl kengaytmasini `.jpg` deb nomlab qo'yish uning rasm ekanligini bildirmaydi. `Marcel` kutubxonasi faylning dastlabki baytlarini (Magic bytes, masalan PNG uchun `89 50 4E 47`) tekshirib, haqiqiy formatni aniqlaydi va zararli fayllarni bloklaydi."
    },
    {
        "id": 1190,
        "title": "Ochiq qayta yo'naltirish (Open Redirect) zaifligini aniqlash va xavfsiz redirect_to",
        "desc": "Saytda login qilingach `params[:return_to]` manziliga yo'naltirish mantig'i bo'lsa, xakker `?return_to=https://evil-phishing.com` berib foydalanuvchini soxta saytga o'g'irlashi mumkin.",
        "req": "`redirect_to` funksiyasida `allow_other_host: false` (Rails 7 standarti) qo'llash yoki faqat ruxsat etilgan domenlarni oq ro'yxatda tekshirish.",
        "code": """# app/controllers/redirect_controller.rb
class RedirectController < ApplicationController
  def after_login
    target_path = params[:return_to]

    # Rails 7 ning xavfsiz qayta yo'naltirishi
    # Agar target_path begona domenga tegishli bo'lsa ActionController::Redirecting::UnsafeRedirectError tashlanadi
    redirect_to(target_path || root_path, allow_other_host: false)
  rescue ActionController::Redirecting::UnsafeRedirectError
    warn "[XAVFSIZLIK] Begona domenga yo'naltirish to'xtatildi!"
    redirect_to root_path
  end
end""",
        "expl": "Open Redirect zaifligi ko'pincha phishing kampaniyalarida qo'llaniladi. Foydalanuvchi manzil satrida haqiqiy bank domenini ko'radi, ammo login qilgach soxta saytga sakrab o'tib ketadi. `allow_other_host: false` bu xavfni to'liq yo'qotadi."
    },
    {
        "id": 1191,
        "title": "Rack::Attack orqali IP bo'yicha Rate Limiting (Throttle)",
        "desc": "Har qanday bitta IP manzildan sekundiga 10 tadan ortiq yoki daqiqasiga 300 tadan ortiq so'rovlar kelganda ularga HTTP 429 Too Many Requests javobini qaytarish lozim.",
        "req": "`Rack::Attack.throttle` sozlamasi, Redis kesh backend, limitdan oshganda maxsus JSON javob qaytarish.",
        "code": """# config/initializers/rack_attack.rb
class Rack::Attack
  # Redis ni kesh xotirasi sifatida ulash
  Rack::Attack.cache.store = ActiveSupport::Cache::RedisCacheStore.new(url: ENV['REDIS_URL'])

  # IP bo'yicha global so'rov tezligini cheklash: 1 daqiqada 300 ta
  throttle('req/ip', limit: 300, period: 1.minute) do |req|
    req.ip unless req.path.start_with?('/assets')
  end

  # Limit buzilganda qaytariladigan xavfsiz javob
  self.throttled_responder = lambda do |env|
    match_data = env['rack.attack.match_data']
    now = match_data[:epoch_time]
    retry_after = match_data[:period] - (now % match_data[:period])

    [
      429,
      {
        'Content-Type' => 'application/json',
        'Retry-After' => retry_after.to_s
      },
      [{ error: 'Tezlik chegarasidan oshildi. Birozdan so\\'ng qayta urining.' }.to_json]
    ]
  end
end""",
        "expl": "`Rack::Attack` Rails so'rovlar zanjirining eng boshida, Rack middleware darajasida ishlaydi. U so'rovlarni Controller yoki Ma'lumotlar bazasiga yetkazmasdanoq filtrlaydi, bu esa serverni DDoS hujumlarida yiqilishdan asraydi."
    },
    {
        "id": 1192,
        "title": "Rack::Attack orqali soxta login urinishlarini cheklash (Fail2ban uslubida)",
        "desc": "Bitta foydalanuvchi hisobiga yoki bitta IP dan login sahifasiga qilinayotgan ketma-ket urinishlarni 20 soniyada 5 tadan oshirmaslik lozim.",
        "req": "Login POST marshrutini filtrlash (`req.path == '/login' && req.post?`), IP va email bo'yicha alohida darchalar o'rnatish.",
        "code": """# config/initializers/rack_attack_login.rb
class Rack::Attack
  # Bitta IP dan login sahifasiga: 1 daqiqada 10 marta
  throttle('logins/ip', limit: 10, period: 1.minute) do |req|
    if req.path == '/login' && req.post?
      req.ip
    end
  end

  # Bitta email manziliga hujum: 1 daqiqada 5 marta
  throttle('logins/email', limit: 5, period: 1.minute) do |req|
    if req.path == '/login' && req.post?
      # Emailni xeshlab kalit sifatida ishlatish
      email = req.params['email'].to_s.downcase.strip
      Digest::SHA256.hexdigest(email) if email.present?
    end
  end
end""",
        "expl": "Bitta tajovuzkor 1000 ta proksi IP orqali bitta maqsadli emailni sindirmoqchi bo'lishi mumkin. Email bo'yicha alohida keshli throttle qo'yish tarmoqlangan kiberhujumlarni ham to'xtata oladi."
    },
    {
        "id": 1193,
        "title": "Rack::Attack orqali zararli skanerlar va User-Agentlarni bloklash (Blocklist)",
        "desc": "Saytni skanerlayotgan avtomatik zaiflik qidiruvchilari (Nikto, SQLMap, WPScan) va `.php`, `.env` kabi fayllarni qidirayotgan robotlarni darhol bloklash talab etiladi.",
        "req": "`Rack::Attack.blocklist` sozlamasi, User-Agent regex filtri va qidirilayotgan xavfli fayllar yo'li.",
        "code": """# config/initializers/rack_attack_blocklist.rb
class Rack::Attack
  # Xakerlik skanerlarini bloklash
  blocklist('block_malicious_user_agents') do |req|
    req.user_agent =~ /(nikto|sqlmap|wpscan|dirbuster|acunetix)/i
  end

  # PHP yoki muhit fayllarini qidirayotgan so'rovlarni darhol to'xtatish
  blocklist('block_probe_paths') do |req|
    req.path =~ /(\\.php|wp-admin|\\.env|\\.git|phpmyadmin)/i
  end
end""",
        "expl": "Rails ilovasi PHP emas, ammo internetdagi botlar barcha saytlarni standart `.env` yoki `wp-admin` bo'yicha doimiy skanerlaydi. Ularni Rack darajasidayoq bloklab qo'yish loglarni toza saqlaydi va keraksiz yuklamani kamaytiradi."
    },
    {
        "id": 1194,
        "title": "Brakeman statik xavfsizlik tahlilchisi (Static Analysis Security Testing) va ogohlantirishlar",
        "desc": "Loyiha kod bazasida yashiringan zaifliklarni (SQLi, XSS, CSRF, Mass Assignment) avtomatlashtirilgan CI/CD konveyerida aniqlash uchun Brakeman tahlilini sozlash lozim.",
        "req": "Brakeman konfiguratsiyasi (`config/brakeman.ignore`), xavflilik darajasi (Confidence: High/Medium) bo'yicha filtrlash va xatolik berilganda CI ni to'xtatish.",
        "code": """# lib/tasks/security_audit.rake
namespace :security do
  desc 'Brakeman statik xavfsizlik tahlilini ishga tushirish'
  task :brakeman do
    require 'brakeman'

    tracker = Brakeman.run(
      app_path: '.',
      print_report: true,
      quiet: false,
      confidence_level: 2 # High va Medium xatolar
    )

    if tracker.filtered_warnings.any?
      puts "[XATOLIK] Brakeman #{tracker.filtered_warnings.size} ta xavfsizlik zaifligini topdi!"
      exit(1)
    else
      puts "[MUVAFFAQIYAT] Kod bazasida kritik zaifliklar aniqlanmadi"
    end
  end
end""",
        "expl": "Brakeman dastur kodini ishga tushirmasdan (Static AST tahlil) o'rganadi. U Rails ning ichki konventsiyalarini chuqur tushunadi va ochiq qolgan `find_by_sql` yoki filtrlanmagan `redirect_to` parametrlarini sekunlar ichida topadi."
    },
    {
        "id": 1195,
        "title": "Bundler-audit orqali zaif Gem qaramliklarini (CVE) aniqlash va avtomat yangilash",
        "desc": "Loyihaga ulangan Gem kutubxonalarida (masalan eski `actionview` yoki `nokogiri`) xalqaro kiberxavfsizlik zaifliklari (CVE) paydo bo'lganda darhol xabar topish kerak.",
        "req": "`bundler-audit` kutubxonasi, zaifliklar bazasini yangilash (`bundle-audit update`) va skanerlash.",
        "code": """# lib/tasks/dependency_audit.rake
namespace :security do
  desc 'Gem qaramliklarini CVE zaifliklari bo\\'yicha tekshirish'
  task :audit_gems do
    require 'bundler/audit/scanner'
    require 'bundler/audit/database'

    Bundler::Audit::Database.update!(quiet: true)
    scanner = Bundler::Audit::Scanner.new

    vulnerabilities = []
    scanner.scan do |result|
      vulnerabilities << result
    end

    if vulnerabilities.any?
      warn "[XAVF! Gev qaramliklarida zaiflik topildi]: #{vulnerabilities.size} ta CVE"
      vulnerabilities.each do |vuln|
        warn " * Gem: #{vuln.gem.name} (#{vuln.gem.version}) - #{vuln.advisory.title} [#{vuln.advisory.cve}]"
      end
      exit(1)
    else
      puts "[TOZA] Barcha Gem kutubxonalari xavfsiz"
    end
  end
end""",
        "expl": "Ko'plab yirik kiberhujumlar uchinchi tomon kutubxonalari (Supply Chain Attacks) orqali amalga oshadi. `bundler-audit` har kuni yangilanadigan Ruby Advisory Database bazasi bilan solishtirib, loyihani o'z vaqtida himoyalaydi."
    },
    {
        "id": 1196,
        "title": "Sensitiv ma'lumotlarni loglardan filtrlash (config.filter_parameters)",
        "desc": "Foydalanuvchining paroli, pasport seriyasi yoki plastik karta raqami server xatolikka uchraganda `log/production.log` fayliga ochiq matnda tushib qolmasligi shart.",
        "req": "`config.filter_parameters` ro'yxatini kengaytirish, parollar va tokenlarni `[FILTERED]` bilan almashtirish.",
        "code": """# config/initializers/filter_parameter_logging.rb
Rails.application.config.filter_parameters += [
  :passw,
  :secret,
  :token,
  :_key,
  :crypt,
  :salt,
  :certificate,
  :otp,
  :ssn,
  :cvv,
  :pan,
  :card_number,
  :passport_number
]""",
        "expl": "Log fayllari ko'pincha tashqi monitoring tizimlariga (ELK, Datadog) yuboriladi va u yerda o'nlab ma'murlar va dasturchilar kirish huquqiga ega bo'ladi. Maxfiy parametrlarni Rails darajasida filtrlab yuborish ma'lumotlar o'g'irlanishini oldini oladi."
    },
    {
        "id": 1197,
        "title": "CORS (Cross-Origin Resource Sharing) xavfsiz sozlamalari (rack-cors gem)",
        "desc": "API shlyuziga boshqa domenlardan (masalan `evil-site.com`) ruxsatsiz so'rovlar yuborilishini to'xtatish uchun faqat ruxsat etilgan frontend domenlarini ko'rsatish lozim.",
        "req": "`rack-cors` gemi, `origins` oq ro'yxati, `credentials: true` bilan faqat ishonchli domenlarga ruxsat berish.",
        "code": """# config/initializers/cors.rb
Rails.application.config.middleware.insert_before 0, Rack::Cors do
  allow do
    # Faqat bizning rasmiy frontend domenlarimiz
    origins 'https://khorazmiy.uz', 'https://app.khorazmiy.uz'

    resource '/api/*',
      headers: :any,
      methods: [:get, :post, :put, :patch, :delete, :options, :head],
      credentials: true, # Cookie va avtorizatsiya sarlavhalarini uzatish huquqi
      max_age: 86400     # Preflight OPTIONS kesh vaqti (24 soat)
  end
end""",
        "expl": "CORS da hech qachon `origins '*'` va `credentials: true` ni birgalikda ishlatmaslik kerak. Bu har qanday zararli saytga foydalanuvchining shaxsiy ma'lumotlarini brauzer orqali o'g'irlashiga ochiq eshik qoldiradi."
    },
    {
        "id": 1198,
        "title": "Xavfsiz HTTP sarlavhalari (Strict-Transport-Security, Permissions-Policy)",
        "desc": "Brauzerni faqat HTTPS orqali ishlashga majburlash (HSTS) va sahifada mikrofon yoki kameradan ruxsatsiz foydalanishni cheklash zarur.",
        "req": "HSTS `max-age=63072000; includeSubDomains; preload`, `Permissions-Policy` sozlamalari.",
        "code": """# config/initializers/hsts_headers.rb
Rails.application.config.action_dispatch.default_headers.merge!(
  # HSTS: 2 yil davomida barcha subdomenlar bilan faqat HTTPS
  'Strict-Transport-Security' => 'max-age=63072000; includeSubDomains; preload',

  # Permissions Policy: Kamera, mikrofon va geolokatsiyani taqiqlash
  'Permissions-Policy' => 'camera=(), microphone=(), geolocation=()'
)""",
        "expl": "HSTS (HTTP Strict Transport Security) brauzerga saytga hech qachon oddiy `http://` orqali ulanmaslikni buyuradi. Bu SSL-Stripping hujumlarini (xakker HTTPS ni HTTP ga tushirib ma'lumotlarni o'g'irlashini) to'liq to'xtatadi."
    },
    {
        "id": 1199,
        "title": "Kiberxavfsizlik voqealari auditi: ActiveSupport::Notifications orqali xavfsizlik SIEM loglari",
        "desc": "Muvaffaqiyatsiz loginlar, parolni o'zgartirishlar va shubhali so'rovlar yuz berganda xavfsizlik bo'limining SIEM monitoring tizimiga voqea hodisalarini (Security Events) uzatish kerak.",
        "req": "`ActiveSupport::Notifications.instrument` va `subscribe` orqali xavfsizlik auditi jurnali (Audit Trail).",
        "code": """# app/services/security_event_broadcaster.rb
class SecurityEventBroadcaster
  def self.log_security_event(event_name, payload = {})
    ActiveSupport::Notifications.instrument(\"security.\#{event_name}\", payload.merge(timestamp: Time.now.utc))
  end
end

# config/initializers/security_notifications.rb
ActiveSupport::Notifications.subscribe(/security\\./) do |name, start, finish, id, payload|
  # SIEM formatidagi log yozuvi
  Rails.logger.warn(\"[SECURITY EVENT] Event: \#{name} | User: \#{payload[:user_id]} | IP: \#{payload[:ip]} | Details: \#{payload.inspect}\")
end""",
        "expl": "`ActiveSupport::Notifications` hodisaga asoslangan (Event-Driven) arxitekturani ta'minlaydi. Xavfsizlik auditi asosiy biznes mantiqqa ta'sir qilmasdan alohida obunachi orqali SIEM yoki Kafka tizimlariga oqimli uzatiladi."
    },
    {
        "id": 1200,
        "title": "To'liq korporativ Rails xavfsizlik himoya qalqoni (Comprehensive Security Shield)",
        "desc": "Tizimning barcha xavfsizlik mexanizmlarini (WAF qoidalari, kalitlar holati, shifrlash zanjiri, zaifliklar va audit holati) bitta markaziy xavfsizlik boshqaruv panelida tekshirish va tasdiqlash.",
        "req": "Barcha xavfsizlik holatlarini birlashtiruvchi sinov shlyuzi, to'liq mudofaa zanjiri tahlili.",
        "code": """# lib/security_shield_health.rb
class SecurityShieldHealth
  def self.audit_complete_system
    status = {
      credentials_encrypted: Rails.application.encrypted('config/credentials.yml.enc').key.present?,
      ssl_enforced: Rails.application.config.force_ssl,
      csrf_protection: ActionController::Base.allow_forgery_protection,
      session_httponly: Rails.application.config.session_options[:httponly],
      session_secure: Rails.application.config.session_options[:secure],
      rack_attack_enabled: defined?(Rack::Attack).present?
    }

    all_secure = status.values.all?
    puts \"\\n=== KHORAZMIY AI RAILS XAVFSIZLIK QALQONI AUDITI ===\"
    status.each do |feature, enabled|
      puts \" * \#{feature}: \#{enabled ? 'HIMOYALANGAN' : 'DIQQAT: ZAIF'}\"
    end
    puts \"Yakuniy Xulosa: \#{all_secure ? 'TIZIM 100% XAVFSIZ' : 'ZUDLIK BILAN SOZLANG'}\"
    all_secure
  end
end""",
        "expl": "Ushbu xavfsizlik qalqoni korxona miqyosidagi Rails ilovalarining to'liq xavfsizlik holatini tasdiqlaydi. Kriptografiya, autentifikatsiya, tarmoq filtrlari va audit jurnallari yagona xavfsizlik ekotizimini hosil qiladi."
    }
]
