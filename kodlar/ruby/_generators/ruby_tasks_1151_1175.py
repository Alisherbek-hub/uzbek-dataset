# -*- coding: utf-8 -*-
"""
Ruby 24-modul: 1151 dan 1175 gacha bo'lgan topshiriqlar
Kriptografiya, OpenSSL, ActiveSupport va Rails 7+ Shifrlash
"""

TASKS_1151_1175 = [
    {
        "id": 1151,
        "title": "OpenSSL::Cipher AES-256-GCM autentifikatsiyalangan shifrlash (Auth Tag va IV)",
        "desc": "Bank va maxfiy ma'lumotlarni saqlashda nafaqat maxfiylik (shifrlash), balki ma'lumotlarning soxtalashtirilmaganligini (yaxlitlik) kafolatlovchi AES-256-GCM rejimini joriy etish talab qilinadi.",
        "req": "`OpenSSL::Cipher.new('aes-256-gcm')` dan foydalanish, 12 baytlik tasodifiy IV, 16 baytlik autentifikatsiya tegi (auth_tag) va ixtiyoriy bog'langan ma'lumotlar (auth_data).",
        "code": """# frozen_string_literal: true
require 'openssl'
require 'base64'

class AesGcmVault
  CIPHER_TYPE = 'aes-256-gcm'

  def self.encrypt(plaintext, key, auth_data = '')
    cipher = OpenSSL::Cipher.new(CIPHER_TYPE)
    cipher.encrypt
    cipher.key = key

    # GCM uchun optimal 96-bitlik (12 bayt) tasodifiy IV
    iv = OpenSSL::Random.random_bytes(12)
    cipher.iv = iv
    cipher.auth_data = auth_data unless auth_data.empty?

    ciphertext = cipher.update(plaintext) + cipher.final
    auth_tag = cipher.auth_tag # 16 baytlik yaxlitlik tegi

    {
      ciphertext: Base64.strict_encode64(ciphertext),
      iv: Base64.strict_encode64(iv),
      auth_tag: Base64.strict_encode64(auth_tag)
    }
  end

  def self.decrypt(encrypted_data, key, auth_data = '')
    decipher = OpenSSL::Cipher.new(CIPHER_TYPE)
    decipher.decrypt
    decipher.key = key
    decipher.iv = Base64.strict_decode64(encrypted_data[:iv])
    decipher.auth_tag = Base64.strict_decode64(encrypted_data[:auth_tag])
    decipher.auth_data = auth_data unless auth_data.empty?

    # Agar ma'lumot yoki teg o'zgartirilgan bo'lsa OpenSSL::Cipher::CipherError tashlanadi
    decipher.update(Base64.strict_decode64(encrypted_data[:ciphertext])) + decipher.final
  end
end""",
        "expl": "AES-256-GCM autentifikatsiyalangan shifrlash (AEAD) rejimida ishlaydi. Oddiy CBC rejimlaridan farqli ravishda, GCM apparat darajasida (Intel AES-NI) tezlashadi va alohida HMAC talab qilmasdan bitta o'tishda kriptografik yaxlitlikni tekshiradi. `auth_tag` soxtalashtirish hujumlaridan (bit-flipping attacks) 100% himoya qiladi."
    },
    {
        "id": 1152,
        "title": "OpenSSL::PKey::RSA 4096-bit kalitlar generatsiyasi, OAEP shifrlash va PSS raqamli imzo",
        "desc": "Katta tashkilotlararo shartnomalar va litsenziyalarni asimmetrik kriptografiya orqali tasdiqlash uchun RSA-4096 kalitlarini yaratish va PSS (Probabilistic Signature Scheme) orqali imzolash kerak.",
        "req": "`OpenSSL::PKey::RSA.new(4096)`, OAEP to'ldirish (padding) bilan shifrlash va PSS tuzilmasi bilan imzo qo'yish.",
        "code": """# frozen_string_literal: true
require 'openssl'
require 'base64'

class RsaSecurityEngine
  def self.generate_keypair
    key = OpenSSL::PKey::RSA.new(4096)
    [key.to_pem, key.public_key.to_pem]
  end

  # Optimal Asymmetric Encryption Padding (OAEP)
  def self.encrypt_oaep(plaintext, public_key_pem)
    pub_key = OpenSSL::PKey::RSA.new(public_key_pem)
    encrypted = pub_key.public_encrypt(plaintext, OpenSSL::PKey::RSA::PKCS1_OAEP_PADDING)
    Base64.strict_encode64(encrypted)
  end

  def self.decrypt_oaep(ciphertext_b64, private_key_pem)
    priv_key = OpenSSL::PKey::RSA.new(private_key_pem)
    raw = Base64.strict_decode64(ciphertext_b64)
    priv_key.private_decrypt(raw, OpenSSL::PKey::RSA::PKCS1_OAEP_PADDING)
  end

  # SHA-256 va PSS bilan raqamli imzo
  def self.sign_document(data, private_key_pem)
    priv_key = OpenSSL::PKey::RSA.new(private_key_pem)
    signature = priv_key.sign_pss('SHA256', data, salt_length: :max, mgf1_hash: 'SHA256')
    Base64.strict_encode64(signature)
  end

  def self.verify_document(data, signature_b64, public_key_pem)
    pub_key = OpenSSL::PKey::RSA.new(public_key_pem)
    sig = Base64.strict_decode64(signature_b64)
    pub_key.verify_pss('SHA256', sig, data, salt_length: :max, mgf1_hash: 'SHA256')
  end
end""",
        "expl": "RSA PKCS#1 v1.5 eski padding sxemasi Bleichenbacher hujumlariga zaif hisoblanadi. Zamonaviy xavfsizlik standartlarida shifrlash uchun faqat OAEP (Optimal Asymmetric Encryption Padding), imzolash uchun esa PSS (Probabilistic Signature Scheme) talab qilinadi."
    },
    {
        "id": 1153,
        "title": "OpenSSL::Digest va HMAC-SHA256 yordamida webhook yaxlitligini tekshirish (Timing-safe comparison)",
        "desc": "Stripe, GitHub yoki Click to'lov tizimlaridan kelayotgan webhook so'rovlarining soxtalashtirilmaganligini ularning sarlavhasidagi HMAC imzosi orqali xavfsiz tasdiqlash lozim.",
        "req": "`OpenSSL::HMAC.hexdigest('sha256', secret, payload)`, vaqtga bog'liq bo'lmagan `Rack::Utils.secure_compare` tekshiruvi.",
        "code": """# frozen_string_literal: true
require 'openssl'
require 'rack/utils'

class WebhookSignatureValidator
  def self.verify!(payload, received_signature, secret_key)
    raise ArgumentError, 'Imzo taqdim etilmadi' if received_signature.nil? || received_signature.empty?

    # HMAC-SHA256 hisoblash
    expected_signature = OpenSSL::HMAC.hexdigest('SHA256', secret_key, payload)

    # Timing Attack (vaqt o'lchov hujumi) ga qarshi tenglik tekshiruvi
    is_valid = Rack::Utils.secure_compare(expected_signature, received_signature)

    raise SecurityError, 'Webhook imzosi mos kelmadi!' unless is_valid

    true
  end
end""",
        "expl": "Oddiy `==` operatori satrlarni belgilab solishtiradi va birinchi mos kelmagan belgidayoq to'xtaydi. Tajovuzkorlar serverning javob berish vaqtini mikrosekundlarda o'lchab (Timing Attack), to'g'ri baytlarni bittalab topishi mumkin. `Rack::Utils.secure_compare` har doim butun satrni to'liq tekshirib, xuddi bir xil vaqt sarflaydi."
    },
    {
        "id": 1154,
        "title": "OpenSSL::PKCS5 PBKDF2 va Scrypt orqali parollarni kalitga aylantirish (Key Derivation)",
        "desc": "Foydalanuvchi kiritgan matnli paroldan shifrlash kalitlarini (AES-256 uchun 32 bayt) yaratishda lug'at hujumlariga qarshi PBKDF2 yoki Scrypt funksiyalaridan foydalanish lozim.",
        "req": "`OpenSSL::PKCS5.pbkdf2_hmac` dan foydalanish, 600 000 iteratsiya (OWASP tavsiyasi), 16 baytlik kriptografik tuz (salt).",
        "code": """# frozen_string_literal: true
require 'openssl'

class KeyDerivationVault
  ITERATIONS = 600_000 # 2026-yil OWASP tavsiyasi
  KEY_LENGTH = 32      # 256 bit

  def self.derive_key(password, salt = nil)
    # Agar tuz berilmasa, 16 baytlik tasodifiy tuz yaratish
    salt ||= OpenSSL::Random.random_bytes(16)

    derived_key = OpenSSL::PKCS5.pbkdf2_hmac(
      password,
      salt,
      ITERATIONS,
      KEY_LENGTH,
      OpenSSL::Digest.new('SHA256')
    )

    {
      key: derived_key,
      salt: salt,
      iterations: ITERATIONS
    }
  end
end""",
        "expl": "Parolni to'g'ridan-to'g'ri AES kaliti sifatida ishlatish xavflidir, chunki inson o'ylab topgan parollarning entropiyasi juda past bo'ladi. PBKDF2 (Password-Based Key Derivation Function 2) 600 000 marta xeshlash orqali GPU va ASIC uskunalari yordamida parollarni ommaviy sindirish (Brute-Force) narxini yuz minglab dollarga oshiradi."
    },
    {
        "id": 1155,
        "title": "OpenSSL::X509 sertifikatlarini tekshirish, CA zanjirini audit qilish va Certificate Pinning",
        "desc": "Mikroxizmatlar orasidagi mTLS ulanishlarida tashqi server taqdim etgan SSL sertifikatining amal qilish muddati, emitent zanjiri (CA) va SPKI barmoq izini (Pinning) tekshirish zarur.",
        "req": "`OpenSSL::X509::Certificate`, `OpenSSL::X509::Store` bilan zanjirni tasdiqlash, ommaviy kalit xeshini (SHA-256 pin) tekshirish.",
        "code": """# frozen_string_literal: true
require 'openssl'

class CertificateAuditor
  def self.verify_certificate_chain(cert_pem, root_ca_pem)
    cert = OpenSSL::X509::Certificate.new(cert_pem)
    root_ca = OpenSSL::X509::Certificate.new(root_ca_pem)

    store = OpenSSL::X509::Store.new
    store.add_cert(root_ca)

    # 1. Muddati o'tmaganligini tekshirish
    now = Time.now
    return false if now < cert.not_before || now > cert.not_after

    # 2. CA zanjirini tasdiqlash
    store.verify(cert)
  end

  def self.matches_pin?(cert_pem, expected_spki_sha256)
    cert = OpenSSL::X509::Certificate.new(cert_pem)
    # Subject Public Key Info (SPKI) xeshini olish
    public_key_der = cert.public_key.to_der
    spki_hash = OpenSSL::Digest::SHA256.hexdigest(public_key_der)

    Rack::Utils.secure_compare(spki_hash, expected_spki_sha256)
  end
end""",
        "expl": "Certificate Pinning (Sertifikatni mahkamlash) Man-in-the-Middle (MITM) hujumlaridan eng ishonchli qalqondir. Agar tajovuzkor soxta CA sertifikatini operatsion tizimga o'rnatib olsa ham, SPKI xeshi mos kelmagani sababli ulanish darhol to'xtatiladi."
    },
    {
        "id": 1156,
        "title": "Ed25519 elliptik egri chiziq imzolari Ruby da",
        "desc": "Tezkor blokcheyn tranzaksiyalari yoki mikrosekundlik xavfsizlik tokenlarini imzolashda RSA ga nisbatan ancha ixcham va 10 barobar tez ishlaydigan Ed25519 (EdDSA) algoritmini qo'llash kerak.",
        "req": "`OpenSSL::PKey` orqali Ed25519 kalitlarini hosil qilish, imzo chekish va tasdiqlash.",
        "code": """# frozen_string_literal: true
require 'openssl'
require 'base64'

class Ed25519Signer
  def self.generate_keypair
    key = OpenSSL::PKey.generate_key('ED25519')
    {
      private_pem: key.private_to_pem,
      public_pem: key.public_to_pem
    }
  end

  def self.sign(message, private_pem)
    key = OpenSSL::PKey.read(private_pem)
    signature = key.sign(nil, message) # Ed25519 o'z ichida xeshlashni birlashtirgan
    Base64.strict_encode64(signature)
  end

  def self.verify(message, signature_b64, public_pem)
    key = OpenSSL::PKey.read(public_pem)
    raw_sig = Base64.strict_decode64(signature_b64)
    key.verify(nil, raw_sig, message)
  end
end""",
        "expl": "Ed25519 - zamonaviy kriptografiyaning oltin standartidir. Uning kalitlari atigi 32 bayt, imzosi esa 64 bayt bo'ladi. RSA kabi tasodifiy sonlar generatoridagi nuqsonlar orqali xususiy kalitning sizib chiqishiga (side-channel attacks) nisbatan matematik himoyaga ega."
    },
    {
        "id": 1157,
        "title": "Diffie-Hellman (ECDH) orqali umumiy maxfiy kalit almashinuvi",
        "desc": "Ikkita mustaqil server ochiq tarmoq orqali o'zaro bog'langanda, hech qanday oldindan kelishilgan maxfiy parolsiz umumiy simmetrik kalit (Shared Secret) hosil qilishi kerak.",
        "req": "Elliptik egri chiziqli Diffie-Hellman (`prime256v1` yoki `X25519`), `derive_key` orqali ikkala tomonda bir xil maxfiy kalitni hisoblash.",
        "code": """# frozen_string_literal: true
require 'openssl'

class EcdhKeyExchange
  def self.create_peer
    # X25519 zamonaviy Diffie-Hellman egri chizig'i
    OpenSSL::PKey.generate_key('X25519')
  end

  def self.compute_shared_secret(my_private_key, other_public_key_pem)
    other_pub = OpenSSL::PKey.read(other_public_key_pem)
    # Diffie-Hellman matematik formulasi: (a * B) == (b * A)
    my_private_key.derive(other_pub)
  end
end""",
        "expl": "Diffie-Hellman algoritmi kriptografiyaning eng go'zal yutuqlaridan biridir. Tomonlar faqat o'zlarining ochiq kalitlarini tarmoq orqali almashadilar. Hatto barcha trafikni yozib olib turgan xakker ham xususiy kalitlarga ega bo'lmagani sababli umumiy kalitni tiklay olmaydi."
    },
    {
        "id": 1158,
        "title": "XChaCha20-Poly1305 shifrlash algoritmi",
        "desc": "AES apparat tezlatkichiga (AES-NI) ega bo'lmagan mobil yoki ARM serverlarda AES sekin ishlaydi va kesh hujumlariga moyil bo'ladi. Uning o'rniga zamonaviy oqimli XChaCha20-Poly1305 shifrlashini qo'llash lozim.",
        "req": "`OpenSSL::Cipher.new('chacha20-poly1305')`, 32 baytlik kalit, 12 yoki 24 baytlik nonce bilan AEAD shifrlash.",
        "code": """# frozen_string_literal: true
require 'openssl'
require 'base64'

class ChaChaCipher
  ALGORITHM = 'chacha20-poly1305'

  def self.encrypt(plaintext, key)
    cipher = OpenSSL::Cipher.new(ALGORITHM)
    cipher.encrypt
    cipher.key = key
    iv = OpenSSL::Random.random_bytes(12)
    cipher.iv = iv

    ciphertext = cipher.update(plaintext) + cipher.final
    tag = cipher.auth_tag

    {
      ciphertext: Base64.strict_encode64(ciphertext),
      iv: Base64.strict_encode64(iv),
      tag: Base64.strict_encode64(tag)
    }
  end

  def self.decrypt(data, key)
    decipher = OpenSSL::Cipher.new(ALGORITHM)
    decipher.decrypt
    decipher.key = key
    decipher.iv = Base64.strict_decode64(data[:iv])
    decipher.auth_tag = Base64.strict_decode64(data[:tag])

    decipher.update(Base64.strict_decode64(data[:ciphertext])) + decipher.final
  end
end""",
        "expl": "ChaCha20-Poly1305 algoritmi Daniel J. Bernstein tomonidan yaratilgan bo'lib, Google tomonidan barcha Android va Chromium qurilmalarida TLS 1.3 standarti sifatida qabul qilingan. U toza arifmetik amallar (ARX: Add-Rotate-Xor) bilan ishlagani sababli kesh vaqti o'lchov hujumlariga mutlaqo chidamli."
    },
    {
        "id": 1159,
        "title": "Kriptografik xavfsiz tasodifiy tokenlar: SecureRandom (hex, base64, urlsafe, random_number)",
        "desc": "Parolni tiklash tokenlari, API kalitlar va sessiya identifikatorlarini yaratishda standart `rand` funksiyasidan foydalanish xavfsizlik halokatiga olib keladi.",
        "req": "`securerandom` dan foydalanish, CSPRNG (Cryptographically Secure Pseudo-Random Number Generator), turli formatlardagi tokenlar va entropiya tahlili.",
        "code": """# frozen_string_literal: true
require 'securerandom'

class SecureTokenGenerator
  # API kalitlar uchun 256-bitli xavfsiz HEX
  def self.generate_api_key
    "ak_live_#{SecureRandom.hex(32)}"
  end

  # URL larda xavfsiz o'tuvchi token (parolni tiklash havolalari uchun)
  def self.generate_reset_token
    SecureRandom.urlsafe_base64(32)
  end

  # 6 xonali SMS kodlari uchun kriptografik xavfsiz son
  def self.generate_otp_code
    # rand(100000..999999) o'rniga
    SecureRandom.random_number(900_000) + 100_000
  end
end""",
        "expl": "Standart `rand()` psevdo-tasodifiy generator bo'lib, LCG yoki Mersenne Twister algoritmidan foydalanadi. Uning ichki holatini atigi 624 ta ketma-ket chiqarilgan son orqali to'liq taxmin qilish mumkin. `SecureRandom` esa to'g'ridan-to'g'ri OS yadrosining `/dev/urandom` entropiya hovuzidan oziqlanadi."
    },
    {
        "id": 1160,
        "title": "Xavfsiz xotirani tozalash: Maxfiy kalitlarni Ruby RAM dan o'chirish (Memory Zeroing)",
        "desc": "Kriptografik amallardan so'ng, xususiy kalitlar va parollar Ruby Garbage Collector tozalaguniga qadar operativ xotirada (RAM) ochiq qolib ketadi va Memory Dump hujumlarida o'g'irlanishi mumkin.",
        "req": "Ruby satrlari xotirasini nolga tenglashtirish (`string.clear` yoki FFI orqali `memset`), xavfsiz tozalash bloki.",
        "code": """# frozen_string_literal: true

class MemoryWiper
  # Maxfiy ma'lumot bilan xavfsiz ishlash bloki
  def self.with_sensitive_string(secret_data)
    yield secret_data
  ensure
    # Satr baytlarini nol bilan to'ldirish
    if secret_data.is_a?(String) && !secret_data.frozen?
      # Xotirani jismoniy tozalash
      secret_data.replace('\\0' * secret_data.bytesize)
      secret_data.clear
    end
  end
end""",
        "expl": "Xotirani tozalash (Memory Zeroing) yuqori darajadagi xavfsizlik auditi talabidir. Server kutilmaganda Core Dump hosil qilganida yoki xotira sizib chiqishi (Heartbleed uslubidagi) yuz berganda, maxfiy kalitlar darhol tozalab tashlangan bo'lsa, xakker faqat nollarni qo'lga kiritadi."
    },
    {
        "id": 1161,
        "title": "ActiveSupport::MessageEncryptor va ActiveSupport::KeyGenerator bilan ma'lumotlarni shifrlash",
        "desc": "Rails ilovasida foydalanuvchilarning pasport raqamlari yoki kredit karta ma'lumotlarini bazaga yozishdan oldin Rails ning standart shifrlash vositalari yordamida himoyalash kerak.",
        "req": "`ActiveSupport::KeyGenerator`, salt yordamida kalit ajratish va `ActiveSupport::MessageEncryptor` orqali shifrlash/deshifrlash.",
        "code": """# frozen_string_literal: true
require 'active_support'

class RailsDataEncryptor
  def initialize(master_secret)
    # Master kalitdan maxsus tuz bilan 32 baytlik kalit hosil qilish
    key_generator = ActiveSupport::KeyGenerator.new(master_secret)
    secret_key = key_generator.generate_key('khorazmiy_db_salt', 32)
    @encryptor = ActiveSupport::MessageEncryptor.new(secret_key, cipher: 'aes-256-gcm')
  end

  def encrypt_data(clear_text)
    @encryptor.encrypt_and_sign(clear_text)
  end

  def decrypt_data(encrypted_payload)
    @encryptor.decrypt_and_verify(encrypted_payload)
  rescue ActiveSupport::MessageEncryptor::InvalidMessage
    warn '[XAVFSIZLIK XATOSI] Ma\\'lumot soxtalashtirilgan yoki kalit noto\\'g\\'ri!'
    nil
  end
end""",
        "expl": "`ActiveSupport::MessageEncryptor` Rails ekotizimining eng qulay va sinovdan o'tgan shifrlagichidir. U avtomatik tarzda serializatsiya, IV generatsiyasi va yaxlitlik imzosini bitta ixcham satrga jamlaydi."
    },
    {
        "id": 1162,
        "title": "ActiveSupport::MessageVerifier orqali imzolangan xavfsiz cookie va tokenlar",
        "desc": "Foydalanuvchiga yuboriladigan ma'lumotni shifrlash shart bo'lmasa-da, foydalanuvchi uning qiymatini (masalan `user_id=42` ni `user_id=1` ga) o'zgartirmasligini kafolatlovchi raqamli imzo talab etiladi.",
        "req": "`ActiveSupport::MessageVerifier` dan foydalanish, xabarni imzolash, muddati o'tishini (`purpose` va `expires_in`) tekshirish.",
        "code": """# frozen_string_literal: true
require 'active_support'

class SecureStateVerifier
  def initialize(app_secret)
    @verifier = ActiveSupport::MessageVerifier.new(app_secret, digest: 'SHA256')
  end

  def sign_user_state(user_id, lifetime_seconds = 3600)
    @verifier.generate(
      { user_id: user_id },
      purpose: :user_session,
      expires_in: lifetime_seconds
    )
  end

  def verify_user_state(signed_token)
    @verifier.verified(signed_token, purpose: :user_session)
  end
end""",
        "expl": "`MessageVerifier` HMACSha256 yordamida ochiq ma'lumotga raqamli tamg'a qo'yadi. Agar tajovuzkor hatto bitta bitni o'zgartirsa yoki tokenning amal qilish muddati (`expires_in`) o'tib ketsa, `verified` usuli darhol `nil` qaytaradi."
    },
    {
        "id": 1163,
        "title": "Rails 7+ ActiveRecord Encryption (Deterministic va Non-deterministic maydonlar)",
        "desc": "Rails 7 dan boshlab ma'lumotlar bazasi ustunlarini (masalan foydalanuvchi elektron pochtasi va telefon raqami) shaffof shifrlash imkoniyati yaratildi. Email bo'yicha qidirish imkonini saqlab qolish uchun Deterministic shifrlash talab etiladi.",
        "req": "`encrypts :field`, deterministik shifrlash (`deterministic: true`) va no-deterministik xavfsiz shifrlash.",
        "code": """# app/models/user.rb
class User < ApplicationRecord
  # Deterministic: Bir xil email har doim bir xil shifrlangan qiymat beradi
  # Bu User.find_by(email: params[:email]) qilish imkonini beradi
  encrypts :email, deterministic: true

  # Non-deterministic (standart): Har safar yangi tasodifiy IV ishlatiladi
  # Qidirish talab qilinmaydigan o'ta maxfiy maydonlar uchun (masalan pasport seriyasi)
  encrypts :passport_number
  encrypts :home_address
end""",
        "expl": "ActiveRecord Encryption Rails 7 ning inqilobiy xususiyatidir. Dasturchi kodida hech narsa o'zgarmaydi: `user.email` oddiy stringdek o'qiladi va yoziladi, lekin ma'lumotlar bazasi diskida (PostgreSQL/MySQL) ma'lumotlar to'liq AES-GCM bilan shifrlangan bo'ladi. Agar DB backup o'g'irlansa ham ma'lumotlar xavfsiz qoladi."
    },
    {
        "id": 1164,
        "title": "Rails 7+ ActiveRecord Encryption da kalitlarni yangilash (Key Rotation)",
        "desc": "Tashkilot xavfsizlik qoidalariga ko'ra shifrlash kalitlari har 1 yilda yangilanishi lozim. Eski kalit bilan shifrlangan ma'lumotlarni yo'qotmasdan yangi kalitga ko'chirish kerak.",
        "req": "`config.active_record.encryption.previous_keys` sozlamasi, background job orqali qayta shifrlash (Key Rotation Task).",
        "code": """# config/application.rb
# config.active_record.encryption.primary_key = ENV['NEW_PRIMARY_KEY']
# config.active_record.encryption.previous_keys = [ENV['OLD_PRIMARY_KEY_2025']]

# lib/tasks/rotate_keys.rake
class KeyRotator
  def self.rotate_all_users
    User.find_each do |user|
      # Eski kalit bilan o'qiladi va xotirada ochiladi
      decrypted_email = user.email
      decrypted_passport = user.passport_number

      # Yangi kalit bilan qayta yoziladi
      user.email = decrypted_email
      user.passport_number = decrypted_passport
      user.save!
    end
    puts "[KEY ROTATION] Barcha foydalanuvchilar yangi 2026-yil kalitiga o'tkazildi!"
  end
end""",
        "expl": "Rails `previous_keys` orqali bir vaqtning o'zida bir nechta avlod kalitlarini qo'llab-quvvatlaydi. O'qish paytida Rails avval asosiy kalitni sinab ko'radi, agar ocholmasa ketma-ket oldingi kalitlar bilan ochadi. Bu kalitlarni tizimni to'xtatmasdan (Zero-Downtime) yangilashga imkon beradi."
    },
    {
        "id": 1165,
        "title": "Rails Credentials tizimi: master.key, credentials.yml.enc va multi-environment shifrlash",
        "desc": "Ma'lumotlar bazasi parollari, to'lov API kalitlari va JWT sirlarini Git repozitoriysiga ochiq yuklamasdan, Rails ning o'rnatilgan shifrlangan konfiguratsiya tizimida saqlash lozim.",
        "req": "`config/credentials.yml.enc` va `config/master.key` boshqaruvi, muhitlar bo'yicha alohida fayllar (`production.yml.enc`).",
        "code": """# frozen_string_literal: true

class CredentialsReader
  def self.fetch_payment_secret
    # Rails.application.credentials orqali xavfsiz o'qish
    payment_key = Rails.application.credentials.dig(:stripe, :secret_key)

    raise SecurityError, 'Stripe maxfiy kaliti credentials ichida topilmadi!' if payment_key.nil?

    payment_key
  end

  def self.audit_credentials_present!
    required_keys = %i[secret_key_base database_password aws_secret]
    required_keys.each do |key|
      val = Rails.application.credentials[key]
      warn "[DIQQAT] #{key} konfiguratsiyasi bo'sh!" if val.nil?
    end
  end
end""",
        "expl": "Rails Credentials shifrlangan YAML fayldir. Dasturchilar `config/credentials.yml.enc` faylini Git ga bemalol push qilishlari mumkin, chunki uni ochish uchun `config/master.key` (yoki `RAILS_MASTER_KEY` muhit o'zgaruvchisi) kerak bo'ladi. Kalitsiz faylni dunyodagi hech bir superkompyuter ocha olmaydi."
    },
    {
        "id": 1166,
        "title": "Rails EncryptedConfiguration ichki mexanizmi va kalit yo'qolishida avariya choralari",
        "desc": "Rails ning ichki shifrlash konfiguratsiyasi (`ActiveSupport::EncryptedConfiguration`) qanday ishlashini dasturiy darajada tushunish va xavfsiz boshqarish talab etiladi.",
        "req": "`ActiveSupport::EncryptedConfiguration.new` orqali shaxsiy shifrlangan fayllarni ochish va tahrirlash.",
        "code": """# frozen_string_literal: true
require 'active_support/encrypted_configuration'

class CustomEncryptedStore
  def self.load_custom_secrets(config_path, key_path)
    encrypted_config = ActiveSupport::EncryptedConfiguration.new(
      config_path: config_path,
      key_path: key_path,
      env_key: 'MY_CUSTOM_SECRET_KEY',
      raise_if_missing_key: true
    )

    # Shifrlangan YAML ni ochish
    decrypted_hash = encrypted_config.config
    puts "[CONFIG] Yuklangan xavfsiz kalitlar soni: #{decrypted_hash.keys.size}"
    decrypted_hash
  end
end""",
        "expl": "`EncryptedConfiguration` mustaqil klass bo'lib, undan nafaqat Rails ichida, balki har qanday maxsus loyihada ixtiyoriy konfiguratsiya fayllarini AES-256-GCM bilan shifrlab saqlash uchun foydalanish mumkin."
    },
    {
        "id": 1167,
        "title": "ActiveSupport::SecurityUtils.secure_compare orqali Timing Attack himoyasi",
        "desc": "Parollar, API tokenlar yoki sessiya ma'lumotlarini tekshirishda vaqt o'lchov hujumlarini (Timing Attacks) to'liq istisno qiluvchi usulni qo'llash kerak.",
        "req": "`ActiveSupport::SecurityUtils.secure_compare(a, b)` dan foydalanish, uzunliklar har xil bo'lganda ham vaqt barqarorligini ta'minlash.",
        "code": """# frozen_string_literal: true
require 'active_support/security_utils'

class SafeTokenComparator
  def self.authenticate_api_token(submitted_token, stored_token)
    return false if submitted_token.nil? || stored_token.nil?

    # Doimiy vaqt davomida solishtirish (Constant-Time Comparison)
    ActiveSupport::SecurityUtils.secure_compare(submitted_token, stored_token)
  end
end""",
        "expl": "`secure_compare` baytlarni XOR (`^`) amali orqali solishtiradi va butun massivni oxirigacha tekshirib chiqadi. Bu protsessorning tarmoqlanishini (branch prediction) chetlab o'tib, barcha so'rovlar uchun bir xil CPU taktlarini ta'minlaydi."
    },
    {
        "id": 1168,
        "title": "Rails Session shifrlash va cookie xavfsizlik flaglari (Secure, HttpOnly, SameSite)",
        "desc": "Foydalanuvchi sessiya ma'lumotlarini saqlovchi cookie fayllari XSS hujumlarida JavaScript orqali o'g'irlanmasligi va HTTPS orqali himoyalanishi shart.",
        "req": "`config.session_store` sozlamalari, `httponly: true`, `secure: true`, `same_site: :lax` parametrlarini qat'iy o'rnatish.",
        "code": """# config/initializers/session_store.rb
Rails.application.config.session_store :cookie_store,
  key: '_khorazmiy_enterprise_session',
  expire_after: 14.days,
  secure: Rails.env.production?, # Faqat HTTPS orqali uzatiladi
  httponly: true,                # JavaScript (document.cookie) o'qiy olmaydi (XSS himoyasi)
  same_site: :lax                # CSRF hujumlarining 90% ini to'xtatadi""",
        "expl": "`HttpOnly` bayrog'i XSS ekspluatatsiyasida sessiya o'g'irlanishini (Session Hijacking) imkonsiz qiladi. `SameSite=Lax` esa uchinchi tomon saytlaridan kelayotgan POST so'rovlarida cookie yuborilishini bloklab, CSRF dan kuchli himoya yaratadi."
    },
    {
        "id": 1169,
        "title": "Rails da vaqtga bog'langan xavfsiz tokenlar (ActiveSupport::Duration bilan expire)",
        "desc": "Parolni tiklash yoki elektron pochtani tasdiqlash uchun yuboriladigan havolalar faqat 15 daqiqa amal qilishi va muddat o'tgach avtomatik yaroqsiz bo'lishi kerak.",
        "req": "`has_secure_token` yoki `generate_token_for` (Rails 7.1+ standarti) orqali vaqtli tokenlar yaratish.",
        "code": """# app/models/user.rb
class User < ApplicationRecord
  # Rails 7.1+ ning o'rnatilgan vaqtli token mexanizmi
  generates_token_for :password_reset, expires_in: 15.minutes do
    # Agar parol xeshi o'zgarsa, eski token avtomatik yaroqsiz bo'ladi
    password_salt&.last(10)
  end

  generates_token_for :email_confirmation, expires_in: 24.hours
end""",
        "expl": "Rails 7.1 dagi `generates_token_for` ma'lumotlar bazasida qo'shimcha token ustunlarini ochmasdan ishlaydi. Token o'z ichiga ma'lumotlar xeshini va muddatni oladi. Foydalanuvchi parolini o'zgartirishi bilanoq uning barcha oldingi parolni tiklash tokenlari bir zumda o'z kuchini yo'qotadi."
    },
    {
        "id": 1170,
        "title": "Maxfiy konfiguratsiyalarni muhit o'zgaruvchilari orqali xavfsiz ineksiya qilish (Dotenv vs Vault)",
        "desc": "Kubernetes yoki Docker konteynerlarida ilovani ishga tushirishda maxfiy kalitlarni fayllarga yozmasdan, HashiCorp Vault yoki tizim muhitidan (ENV) xavfsiz yuklash lozim.",
        "req": "ENV o'zgaruvchilarini tekshirish (`ENV.fetch`), bo'sh bo'lsa serverni ishga tushirmaslik (Fail-Fast printsipi).",
        "code": """# config/initializers/env_audit.rb
class StrictEnvironment
  REQUIRED_VARS = %w[
    DATABASE_URL
    REDIS_URL
    RAILS_MASTER_KEY
  ].freeze

  def self.validate!
    missing = REQUIRED_VARS.reject { |var| ENV[var].present? }

    if missing.any?
      abort "[KRITIK XAVFSIZLIK XATOSI] Muhit o'zgaruvchilari yetishmayapti: #{missing.join(', ')}! Server to'xtatildi."
    end
  end
end

StrictEnvironment.validate! if Rails.env.production?""",
        "expl": "Fail-Fast tamoyili: Agar ishlab chiqarish muhitida biron bir kritik xavfsizlik o'zgaruvchisi kiritilmagan bo'lsa, server jimjitlikda sukut bo'yicha (fallback) zaif kalitlar bilan ishga tushmasligi, balki zudlik bilan xato bilan to'xtashi shart."
    },
    {
        "id": 1171,
        "title": "Argon2id parollarni xeshlash algoritmi (argon2 gem) va Bcrypt bilan solishtirish",
        "desc": "Bcrypt algoritmi xotira talab qilmaydi va GPU klasterlarida tez sindirilishi mumkin. Password Hashing Competition g'olibi bo'lgan xotira-qattiq (memory-hard) Argon2id algoritmini joriy etish kerak.",
        "req": "`argon2` gemi, `Argon2::Password.create`, t_cost (vaqt), m_cost (xotira - masalan 64MB) parametrlarini sozlash.",
        "code": """# frozen_string_literal: true
require 'argon2'

class ModernPasswordHasher
  # Argon2id: Side-channel va GPU hujumlariga qarshi gibrid algoritm
  def self.hash_password(raw_password)
    hasher = Argon2::Password.new(
      t_cost: 3,        # 3 iteratsiya
      m_cost: 16,       # 2^16 KB = 64 MB operativ xotira talabi
      p_cost: 4         # 4 parallel oqim
    )
    hasher.create(raw_password)
  end

  def self.verify_password(raw_password, password_hash)
    Argon2::Password.verify_password(raw_password, password_hash)
  rescue Argon2::Errors::VerificationError
    false
  end
end""",
        "expl": "Argon2id ning eng katta kuchi uning xotira talabchanligidadir (`m_cost`). Bitta parolni tekshirish uchun 64 MB xotira kerak bo'lsa, xakker o'zining GPU kartasida parallel ravishda millionlab parollarni tekshira olmaydi, chunki video karta xotirasi darhol to'lib qoladi."
    },
    {
        "id": 1172,
        "title": "Devise autentifikatsiyasida xavfsizlik sozlamalari (Lockable, Trackable, Paranoid rejim)",
        "desc": "Foydalanuvchi hisoblarini himoyalashda 5 ta noto'g'ri urinishdan so'ng hisobni qulflash (Lockable) va tajovuzkorga qaysi email mavjudligini bildirmaslik (Paranoid mode) talab qilinadi.",
        "req": "Devise konfiguratsiyasi: `config.lock_strategy = :failed_attempts`, `config.maximum_attempts = 5`, `config.paranoid = true`.",
        "code": """# config/initializers/devise.rb
Devise.setup do |config|
  # Paranoid Mode: Foydalanuvchi mavjud yoki yo'qligini bildirmaslik (User Enumeration himoyasi)
  config.paranoid = true

  # Lockable: 5 marta xato kiritilsa hisobni bloklash
  config.lock_strategy = :failed_attempts
  config.maximum_attempts = 5
  config.unlock_keys = [:email]
  config.unlock_strategy = :both # Email havola yoki 1 soatdan keyin ochiladi
  config.unlock_in = 1.hour

  # Parol xeshlash xarajatini oshirish
  config.stretches = Rails.env.test? ? 1 : 12

  # Sessiyani eslatib qolish muddati
  config.remember_for = 2.weeks
end""",
        "expl": "`config.paranoid = true` kiberxavfsizlikda 'User Enumeration' hujumlarining oldini oladi. Tizim foydalanuvchi bor bo'lsa ham, yo'q bo'lsa ham bir xil: 'Agar hisob mavjud bo'lsa, sizga ko'rsatma yuborildi' degan javobni qaytaradi."
    },
    {
        "id": 1173,
        "title": "Ikki bosqichli autentifikatsiya (2FA / TOTP: RFC 6238) rotp gemi bilan",
        "desc": "Google Authenticator yoki 1Password orqali har 30 soniyada o'zgaruvchi 6 xonali bir martalik kodlar (Time-Based One-Time Password) tizimini Rails ga integratsiya qilish lozim.",
        "req": "`rotp` gemi, `ROTP::TOTP.new`, QR-kod havolasi (`provisioning_uri`), vaqt driftini hisobga oluvchi tasdiqlash (`verify(code, drift_behind: 15)`).",
        "code": """# frozen_string_literal: true
require 'rotp'

class TwoFactorAuthManager
  def self.generate_secret
    ROTP::Base32.random # 160-bitlik xavfsiz Base32 maxfiy kalit
  end

  def self.build_qr_uri(secret, user_email, issuer = 'Khorazmiy AI')
    totp = ROTP::TOTP.new(secret, issuer: issuer)
    totp.provisioning_uri(user_email)
  end

  def self.verify_code(secret, user_code)
    totp = ROTP::TOTP.new(secret)
    # drift_behind: 30 soniyalik vaqt og'ishini hisobga olish
    totp.verify(user_code, drift_behind: 15, drift_ahead: 15)
  end
end""",
        "expl": "RFC 6238 standarti bo'yicha TOTP hozirgi Unix vaqtini 30 soniyalik darchalarga bo'ladi va maxfiy kalit bilan HMAC-SHA1 hisoblaydi. `drift_behind` foydalanuvchi telefonidagi soat server soatidan bir necha soniya orqada qolganda ham kodni to'g'ri qabul qilish imkonini beradi."
    },
    {
        "id": 1174,
        "title": "WebAuthn / FIDO2 Passkeys autentifikatsiyasini Rails da joriy qilish",
        "desc": "Parolsiz dunyoga o'tish: foydalanuvchi brauzeridagi Apple TouchID, FaceID yoki Windows Hello biometrik kalitlari bilan tizimga kirishini ta'minlash kerak.",
        "req": "`webauthn` gemi, Challenge yaratish, Attestation va Assertion obyektlarini tekshirish.",
        "code": """# app/controllers/webauthn_sessions_controller.rb
class WebauthnSessionsController < ApplicationController
  def create_challenge
    options = WebAuthn::Credential.options_for_get(
      allow_credentials: current_user.passkeys.pluck(:external_id)
    )
    session[:webauthn_challenge] = options.challenge
    render json: options
  end

  def verify_passkey
    webauthn_credential = WebAuthn::Credential.from_get(params[:credential])

    # Saqlangan ochiq kalit bo'yicha imzoni tekshirish
    passkey = current_user.passkeys.find_by(external_id: webauthn_credential.id)

    webauthn_credential.verify(
      session[:webauthn_challenge],
      public_key: passkey.public_key,
      sign_count: passkey.sign_count
    )

    passkey.update!(sign_count: webauthn_credential.sign_count)
    session[:user_id] = current_user.id
    render json: { status: 'Xavfsiz kirdi' }
  end
end""",
        "expl": "Passkeys (FIDO2) phishing hujumlarini 100% bartaraf etadi. Brauzer autentifikatsiya paytida domen nomini tekshiradi, shu sababli hatto foydalanuvchi soxta (klonlangan) phishing saytiga kirsa ham, FaceID unga kalitni bermaydi."
    },
    {
        "id": 1175,
        "title": "Parol murakkabligi va zxcvbn algoritmi orqali zaif parollarni tekshirish",
        "desc": "Foydalanuvchilar 'Parol123!' kabi sodda parollar qo'yishining oldini olish uchun parollarning haqiqiy entropiyasini Dropbox ning `zxcvbn` algoritmi bilan baholash lozim.",
        "req": "Entropiya balli (0 dan 4 gacha), lug'atlar va ketma-ketliklarni aniqlash, ball < 3 bo'lsa parolni rad etish.",
        "code": """# app/validators/strong_password_validator.rb
require 'zxcvbn'

class StrongPasswordValidator < ActiveModel::EachValidator
  MIN_SCORE = 3 # 0: Juda zaif, 1: Zaif, 2: O'rta, 3: Kuchli, 4: O'ta xavfsiz

  def validate_each(record, attribute, value)
    return if value.blank?

    tester = Zxcvbn::Tester.new
    # Foydalanuvchi ismi va emailini lug'at sifatida kiritish
    user_inputs = [record.try(:name), record.try(:email)].compact
    result = tester.test(value, user_inputs)

    if result.score < MIN_SCORE
      feedback = result.feedback.suggestions.join('. ')
      warning = result.feedback.warning
      record.errors.add(attribute, "juda zaif! #{warning}. #{feedback}")
    end
  end
end""",
        "expl": "An'anaviy qoidalar (1 ta katta harf, 1 ta belgi) xavfsizlik bermaydi, chunki odamlar shunchaki 'Password123!' yozadi. `zxcvbn` esa fazoviy entropiyani hisoblaydi, klaviaturadagi ketma-ketliklarni (qwerty), mashhur ismlarni va sanalarni tahlil qilib, real himoyani ta'minlaydi."
    }
]
