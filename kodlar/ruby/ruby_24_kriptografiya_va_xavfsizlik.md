# Khorazmiy AI: Ruby - Modul 24
## Mavzu: Kriptografiya va Rails Xavfsizligi: OpenSSL, ActiveSupport::MessageEncryptor, Rails credentials (master.key), Devise/Argon2, CSRF himoyasi, Arel SQL injection audit va Rack::Attack rate limiting


---

### Topshiriq #1151: OpenSSL::Cipher AES-256-GCM autentifikatsiyalangan shifrlash (Auth Tag va IV)
**Tavsif:** Bank va maxfiy ma'lumotlarni saqlashda nafaqat maxfiylik (shifrlash), balki ma'lumotlarning soxtalashtirilmaganligini (yaxlitlik) kafolatlovchi AES-256-GCM rejimini joriy etish talab qilinadi.
**Talablar:** `OpenSSL::Cipher.new('aes-256-gcm')` dan foydalanish, 12 baytlik tasodifiy IV, 16 baytlik autentifikatsiya tegi (auth_tag) va ixtiyoriy bog'langan ma'lumotlar (auth_data).
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
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
end
```
**Tushuntirish:** AES-256-GCM autentifikatsiyalangan shifrlash (AEAD) rejimida ishlaydi. Oddiy CBC rejimlaridan farqli ravishda, GCM apparat darajasida (Intel AES-NI) tezlashadi va alohida HMAC talab qilmasdan bitta o'tishda kriptografik yaxlitlikni tekshiradi. `auth_tag` soxtalashtirish hujumlaridan (bit-flipping attacks) 100% himoya qiladi.


---

### Topshiriq #1152: OpenSSL::PKey::RSA 4096-bit kalitlar generatsiyasi, OAEP shifrlash va PSS raqamli imzo
**Tavsif:** Katta tashkilotlararo shartnomalar va litsenziyalarni asimmetrik kriptografiya orqali tasdiqlash uchun RSA-4096 kalitlarini yaratish va PSS (Probabilistic Signature Scheme) orqali imzolash kerak.
**Talablar:** `OpenSSL::PKey::RSA.new(4096)`, OAEP to'ldirish (padding) bilan shifrlash va PSS tuzilmasi bilan imzo qo'yish.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
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
end
```
**Tushuntirish:** RSA PKCS#1 v1.5 eski padding sxemasi Bleichenbacher hujumlariga zaif hisoblanadi. Zamonaviy xavfsizlik standartlarida shifrlash uchun faqat OAEP (Optimal Asymmetric Encryption Padding), imzolash uchun esa PSS (Probabilistic Signature Scheme) talab qilinadi.


---

### Topshiriq #1153: OpenSSL::Digest va HMAC-SHA256 yordamida webhook yaxlitligini tekshirish (Timing-safe comparison)
**Tavsif:** Stripe, GitHub yoki Click to'lov tizimlaridan kelayotgan webhook so'rovlarining soxtalashtirilmaganligini ularning sarlavhasidagi HMAC imzosi orqali xavfsiz tasdiqlash lozim.
**Talablar:** `OpenSSL::HMAC.hexdigest('sha256', secret, payload)`, vaqtga bog'liq bo'lmagan `Rack::Utils.secure_compare` tekshiruvi.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
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
end
```
**Tushuntirish:** Oddiy `==` operatori satrlarni belgilab solishtiradi va birinchi mos kelmagan belgidayoq to'xtaydi. Tajovuzkorlar serverning javob berish vaqtini mikrosekundlarda o'lchab (Timing Attack), to'g'ri baytlarni bittalab topishi mumkin. `Rack::Utils.secure_compare` har doim butun satrni to'liq tekshirib, xuddi bir xil vaqt sarflaydi.


---

### Topshiriq #1154: OpenSSL::PKCS5 PBKDF2 va Scrypt orqali parollarni kalitga aylantirish (Key Derivation)
**Tavsif:** Foydalanuvchi kiritgan matnli paroldan shifrlash kalitlarini (AES-256 uchun 32 bayt) yaratishda lug'at hujumlariga qarshi PBKDF2 yoki Scrypt funksiyalaridan foydalanish lozim.
**Talablar:** `OpenSSL::PKCS5.pbkdf2_hmac` dan foydalanish, 600 000 iteratsiya (OWASP tavsiyasi), 16 baytlik kriptografik tuz (salt).
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
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
end
```
**Tushuntirish:** Parolni to'g'ridan-to'g'ri AES kaliti sifatida ishlatish xavflidir, chunki inson o'ylab topgan parollarning entropiyasi juda past bo'ladi. PBKDF2 (Password-Based Key Derivation Function 2) 600 000 marta xeshlash orqali GPU va ASIC uskunalari yordamida parollarni ommaviy sindirish (Brute-Force) narxini yuz minglab dollarga oshiradi.


---

### Topshiriq #1155: OpenSSL::X509 sertifikatlarini tekshirish, CA zanjirini audit qilish va Certificate Pinning
**Tavsif:** Mikroxizmatlar orasidagi mTLS ulanishlarida tashqi server taqdim etgan SSL sertifikatining amal qilish muddati, emitent zanjiri (CA) va SPKI barmoq izini (Pinning) tekshirish zarur.
**Talablar:** `OpenSSL::X509::Certificate`, `OpenSSL::X509::Store` bilan zanjirni tasdiqlash, ommaviy kalit xeshini (SHA-256 pin) tekshirish.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
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
end
```
**Tushuntirish:** Certificate Pinning (Sertifikatni mahkamlash) Man-in-the-Middle (MITM) hujumlaridan eng ishonchli qalqondir. Agar tajovuzkor soxta CA sertifikatini operatsion tizimga o'rnatib olsa ham, SPKI xeshi mos kelmagani sababli ulanish darhol to'xtatiladi.


---

### Topshiriq #1156: Ed25519 elliptik egri chiziq imzolari Ruby da
**Tavsif:** Tezkor blokcheyn tranzaksiyalari yoki mikrosekundlik xavfsizlik tokenlarini imzolashda RSA ga nisbatan ancha ixcham va 10 barobar tez ishlaydigan Ed25519 (EdDSA) algoritmini qo'llash kerak.
**Talablar:** `OpenSSL::PKey` orqali Ed25519 kalitlarini hosil qilish, imzo chekish va tasdiqlash.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
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
end
```
**Tushuntirish:** Ed25519 - zamonaviy kriptografiyaning oltin standartidir. Uning kalitlari atigi 32 bayt, imzosi esa 64 bayt bo'ladi. RSA kabi tasodifiy sonlar generatoridagi nuqsonlar orqali xususiy kalitning sizib chiqishiga (side-channel attacks) nisbatan matematik himoyaga ega.


---

### Topshiriq #1157: Diffie-Hellman (ECDH) orqali umumiy maxfiy kalit almashinuvi
**Tavsif:** Ikkita mustaqil server ochiq tarmoq orqali o'zaro bog'langanda, hech qanday oldindan kelishilgan maxfiy parolsiz umumiy simmetrik kalit (Shared Secret) hosil qilishi kerak.
**Talablar:** Elliptik egri chiziqli Diffie-Hellman (`prime256v1` yoki `X25519`), `derive_key` orqali ikkala tomonda bir xil maxfiy kalitni hisoblash.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
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
end
```
**Tushuntirish:** Diffie-Hellman algoritmi kriptografiyaning eng go'zal yutuqlaridan biridir. Tomonlar faqat o'zlarining ochiq kalitlarini tarmoq orqali almashadilar. Hatto barcha trafikni yozib olib turgan xakker ham xususiy kalitlarga ega bo'lmagani sababli umumiy kalitni tiklay olmaydi.


---

### Topshiriq #1158: XChaCha20-Poly1305 shifrlash algoritmi
**Tavsif:** AES apparat tezlatkichiga (AES-NI) ega bo'lmagan mobil yoki ARM serverlarda AES sekin ishlaydi va kesh hujumlariga moyil bo'ladi. Uning o'rniga zamonaviy oqimli XChaCha20-Poly1305 shifrlashini qo'llash lozim.
**Talablar:** `OpenSSL::Cipher.new('chacha20-poly1305')`, 32 baytlik kalit, 12 yoki 24 baytlik nonce bilan AEAD shifrlash.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
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
end
```
**Tushuntirish:** ChaCha20-Poly1305 algoritmi Daniel J. Bernstein tomonidan yaratilgan bo'lib, Google tomonidan barcha Android va Chromium qurilmalarida TLS 1.3 standarti sifatida qabul qilingan. U toza arifmetik amallar (ARX: Add-Rotate-Xor) bilan ishlagani sababli kesh vaqti o'lchov hujumlariga mutlaqo chidamli.


---

### Topshiriq #1159: Kriptografik xavfsiz tasodifiy tokenlar: SecureRandom (hex, base64, urlsafe, random_number)
**Tavsif:** Parolni tiklash tokenlari, API kalitlar va sessiya identifikatorlarini yaratishda standart `rand` funksiyasidan foydalanish xavfsizlik halokatiga olib keladi.
**Talablar:** `securerandom` dan foydalanish, CSPRNG (Cryptographically Secure Pseudo-Random Number Generator), turli formatlardagi tokenlar va entropiya tahlili.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
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
end
```
**Tushuntirish:** Standart `rand()` psevdo-tasodifiy generator bo'lib, LCG yoki Mersenne Twister algoritmidan foydalanadi. Uning ichki holatini atigi 624 ta ketma-ket chiqarilgan son orqali to'liq taxmin qilish mumkin. `SecureRandom` esa to'g'ridan-to'g'ri OS yadrosining `/dev/urandom` entropiya hovuzidan oziqlanadi.


---

### Topshiriq #1160: Xavfsiz xotirani tozalash: Maxfiy kalitlarni Ruby RAM dan o'chirish (Memory Zeroing)
**Tavsif:** Kriptografik amallardan so'ng, xususiy kalitlar va parollar Ruby Garbage Collector tozalaguniga qadar operativ xotirada (RAM) ochiq qolib ketadi va Memory Dump hujumlarida o'g'irlanishi mumkin.
**Talablar:** Ruby satrlari xotirasini nolga tenglashtirish (`string.clear` yoki FFI orqali `memset`), xavfsiz tozalash bloki.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true

class MemoryWiper
  # Maxfiy ma'lumot bilan xavfsiz ishlash bloki
  def self.with_sensitive_string(secret_data)
    yield secret_data
  ensure
    # Satr baytlarini nol bilan to'ldirish
    if secret_data.is_a?(String) && !secret_data.frozen?
      # Xotirani jismoniy tozalash
      secret_data.replace('\0' * secret_data.bytesize)
      secret_data.clear
    end
  end
end
```
**Tushuntirish:** Xotirani tozalash (Memory Zeroing) yuqori darajadagi xavfsizlik auditi talabidir. Server kutilmaganda Core Dump hosil qilganida yoki xotira sizib chiqishi (Heartbleed uslubidagi) yuz berganda, maxfiy kalitlar darhol tozalab tashlangan bo'lsa, xakker faqat nollarni qo'lga kiritadi.


---

### Topshiriq #1161: ActiveSupport::MessageEncryptor va ActiveSupport::KeyGenerator bilan ma'lumotlarni shifrlash
**Tavsif:** Rails ilovasida foydalanuvchilarning pasport raqamlari yoki kredit karta ma'lumotlarini bazaga yozishdan oldin Rails ning standart shifrlash vositalari yordamida himoyalash kerak.
**Talablar:** `ActiveSupport::KeyGenerator`, salt yordamida kalit ajratish va `ActiveSupport::MessageEncryptor` orqali shifrlash/deshifrlash.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
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
    warn '[XAVFSIZLIK XATOSI] Ma\'lumot soxtalashtirilgan yoki kalit noto\'g\'ri!'
    nil
  end
end
```
**Tushuntirish:** `ActiveSupport::MessageEncryptor` Rails ekotizimining eng qulay va sinovdan o'tgan shifrlagichidir. U avtomatik tarzda serializatsiya, IV generatsiyasi va yaxlitlik imzosini bitta ixcham satrga jamlaydi.


---

### Topshiriq #1162: ActiveSupport::MessageVerifier orqali imzolangan xavfsiz cookie va tokenlar
**Tavsif:** Foydalanuvchiga yuboriladigan ma'lumotni shifrlash shart bo'lmasa-da, foydalanuvchi uning qiymatini (masalan `user_id=42` ni `user_id=1` ga) o'zgartirmasligini kafolatlovchi raqamli imzo talab etiladi.
**Talablar:** `ActiveSupport::MessageVerifier` dan foydalanish, xabarni imzolash, muddati o'tishini (`purpose` va `expires_in`) tekshirish.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
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
end
```
**Tushuntirish:** `MessageVerifier` HMACSha256 yordamida ochiq ma'lumotga raqamli tamg'a qo'yadi. Agar tajovuzkor hatto bitta bitni o'zgartirsa yoki tokenning amal qilish muddati (`expires_in`) o'tib ketsa, `verified` usuli darhol `nil` qaytaradi.


---

### Topshiriq #1163: Rails 7+ ActiveRecord Encryption (Deterministic va Non-deterministic maydonlar)
**Tavsif:** Rails 7 dan boshlab ma'lumotlar bazasi ustunlarini (masalan foydalanuvchi elektron pochtasi va telefon raqami) shaffof shifrlash imkoniyati yaratildi. Email bo'yicha qidirish imkonini saqlab qolish uchun Deterministic shifrlash talab etiladi.
**Talablar:** `encrypts :field`, deterministik shifrlash (`deterministic: true`) va no-deterministik xavfsiz shifrlash.
**Yechim (Ruby):**
```ruby
# app/models/user.rb
class User < ApplicationRecord
  # Deterministic: Bir xil email har doim bir xil shifrlangan qiymat beradi
  # Bu User.find_by(email: params[:email]) qilish imkonini beradi
  encrypts :email, deterministic: true

  # Non-deterministic (standart): Har safar yangi tasodifiy IV ishlatiladi
  # Qidirish talab qilinmaydigan o'ta maxfiy maydonlar uchun (masalan pasport seriyasi)
  encrypts :passport_number
  encrypts :home_address
end
```
**Tushuntirish:** ActiveRecord Encryption Rails 7 ning inqilobiy xususiyatidir. Dasturchi kodida hech narsa o'zgarmaydi: `user.email` oddiy stringdek o'qiladi va yoziladi, lekin ma'lumotlar bazasi diskida (PostgreSQL/MySQL) ma'lumotlar to'liq AES-GCM bilan shifrlangan bo'ladi. Agar DB backup o'g'irlansa ham ma'lumotlar xavfsiz qoladi.


---

### Topshiriq #1164: Rails 7+ ActiveRecord Encryption da kalitlarni yangilash (Key Rotation)
**Tavsif:** Tashkilot xavfsizlik qoidalariga ko'ra shifrlash kalitlari har 1 yilda yangilanishi lozim. Eski kalit bilan shifrlangan ma'lumotlarni yo'qotmasdan yangi kalitga ko'chirish kerak.
**Talablar:** `config.active_record.encryption.previous_keys` sozlamasi, background job orqali qayta shifrlash (Key Rotation Task).
**Yechim (Ruby):**
```ruby
# config/application.rb
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
end
```
**Tushuntirish:** Rails `previous_keys` orqali bir vaqtning o'zida bir nechta avlod kalitlarini qo'llab-quvvatlaydi. O'qish paytida Rails avval asosiy kalitni sinab ko'radi, agar ocholmasa ketma-ket oldingi kalitlar bilan ochadi. Bu kalitlarni tizimni to'xtatmasdan (Zero-Downtime) yangilashga imkon beradi.


---

### Topshiriq #1165: Rails Credentials tizimi: master.key, credentials.yml.enc va multi-environment shifrlash
**Tavsif:** Ma'lumotlar bazasi parollari, to'lov API kalitlari va JWT sirlarini Git repozitoriysiga ochiq yuklamasdan, Rails ning o'rnatilgan shifrlangan konfiguratsiya tizimida saqlash lozim.
**Talablar:** `config/credentials.yml.enc` va `config/master.key` boshqaruvi, muhitlar bo'yicha alohida fayllar (`production.yml.enc`).
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true

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
end
```
**Tushuntirish:** Rails Credentials shifrlangan YAML fayldir. Dasturchilar `config/credentials.yml.enc` faylini Git ga bemalol push qilishlari mumkin, chunki uni ochish uchun `config/master.key` (yoki `RAILS_MASTER_KEY` muhit o'zgaruvchisi) kerak bo'ladi. Kalitsiz faylni dunyodagi hech bir superkompyuter ocha olmaydi.


---

### Topshiriq #1166: Rails EncryptedConfiguration ichki mexanizmi va kalit yo'qolishida avariya choralari
**Tavsif:** Rails ning ichki shifrlash konfiguratsiyasi (`ActiveSupport::EncryptedConfiguration`) qanday ishlashini dasturiy darajada tushunish va xavfsiz boshqarish talab etiladi.
**Talablar:** `ActiveSupport::EncryptedConfiguration.new` orqali shaxsiy shifrlangan fayllarni ochish va tahrirlash.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
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
end
```
**Tushuntirish:** `EncryptedConfiguration` mustaqil klass bo'lib, undan nafaqat Rails ichida, balki har qanday maxsus loyihada ixtiyoriy konfiguratsiya fayllarini AES-256-GCM bilan shifrlab saqlash uchun foydalanish mumkin.


---

### Topshiriq #1167: ActiveSupport::SecurityUtils.secure_compare orqali Timing Attack himoyasi
**Tavsif:** Parollar, API tokenlar yoki sessiya ma'lumotlarini tekshirishda vaqt o'lchov hujumlarini (Timing Attacks) to'liq istisno qiluvchi usulni qo'llash kerak.
**Talablar:** `ActiveSupport::SecurityUtils.secure_compare(a, b)` dan foydalanish, uzunliklar har xil bo'lganda ham vaqt barqarorligini ta'minlash.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
require 'active_support/security_utils'

class SafeTokenComparator
  def self.authenticate_api_token(submitted_token, stored_token)
    return false if submitted_token.nil? || stored_token.nil?

    # Doimiy vaqt davomida solishtirish (Constant-Time Comparison)
    ActiveSupport::SecurityUtils.secure_compare(submitted_token, stored_token)
  end
end
```
**Tushuntirish:** `secure_compare` baytlarni XOR (`^`) amali orqali solishtiradi va butun massivni oxirigacha tekshirib chiqadi. Bu protsessorning tarmoqlanishini (branch prediction) chetlab o'tib, barcha so'rovlar uchun bir xil CPU taktlarini ta'minlaydi.


---

### Topshiriq #1168: Rails Session shifrlash va cookie xavfsizlik flaglari (Secure, HttpOnly, SameSite)
**Tavsif:** Foydalanuvchi sessiya ma'lumotlarini saqlovchi cookie fayllari XSS hujumlarida JavaScript orqali o'g'irlanmasligi va HTTPS orqali himoyalanishi shart.
**Talablar:** `config.session_store` sozlamalari, `httponly: true`, `secure: true`, `same_site: :lax` parametrlarini qat'iy o'rnatish.
**Yechim (Ruby):**
```ruby
# config/initializers/session_store.rb
Rails.application.config.session_store :cookie_store,
  key: '_khorazmiy_enterprise_session',
  expire_after: 14.days,
  secure: Rails.env.production?, # Faqat HTTPS orqali uzatiladi
  httponly: true,                # JavaScript (document.cookie) o'qiy olmaydi (XSS himoyasi)
  same_site: :lax                # CSRF hujumlarining 90% ini to'xtatadi
```
**Tushuntirish:** `HttpOnly` bayrog'i XSS ekspluatatsiyasida sessiya o'g'irlanishini (Session Hijacking) imkonsiz qiladi. `SameSite=Lax` esa uchinchi tomon saytlaridan kelayotgan POST so'rovlarida cookie yuborilishini bloklab, CSRF dan kuchli himoya yaratadi.


---

### Topshiriq #1169: Rails da vaqtga bog'langan xavfsiz tokenlar (ActiveSupport::Duration bilan expire)
**Tavsif:** Parolni tiklash yoki elektron pochtani tasdiqlash uchun yuboriladigan havolalar faqat 15 daqiqa amal qilishi va muddat o'tgach avtomatik yaroqsiz bo'lishi kerak.
**Talablar:** `has_secure_token` yoki `generate_token_for` (Rails 7.1+ standarti) orqali vaqtli tokenlar yaratish.
**Yechim (Ruby):**
```ruby
# app/models/user.rb
class User < ApplicationRecord
  # Rails 7.1+ ning o'rnatilgan vaqtli token mexanizmi
  generates_token_for :password_reset, expires_in: 15.minutes do
    # Agar parol xeshi o'zgarsa, eski token avtomatik yaroqsiz bo'ladi
    password_salt&.last(10)
  end

  generates_token_for :email_confirmation, expires_in: 24.hours
end
```
**Tushuntirish:** Rails 7.1 dagi `generates_token_for` ma'lumotlar bazasida qo'shimcha token ustunlarini ochmasdan ishlaydi. Token o'z ichiga ma'lumotlar xeshini va muddatni oladi. Foydalanuvchi parolini o'zgartirishi bilanoq uning barcha oldingi parolni tiklash tokenlari bir zumda o'z kuchini yo'qotadi.


---

### Topshiriq #1170: Maxfiy konfiguratsiyalarni muhit o'zgaruvchilari orqali xavfsiz ineksiya qilish (Dotenv vs Vault)
**Tavsif:** Kubernetes yoki Docker konteynerlarida ilovani ishga tushirishda maxfiy kalitlarni fayllarga yozmasdan, HashiCorp Vault yoki tizim muhitidan (ENV) xavfsiz yuklash lozim.
**Talablar:** ENV o'zgaruvchilarini tekshirish (`ENV.fetch`), bo'sh bo'lsa serverni ishga tushirmaslik (Fail-Fast printsipi).
**Yechim (Ruby):**
```ruby
# config/initializers/env_audit.rb
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

StrictEnvironment.validate! if Rails.env.production?
```
**Tushuntirish:** Fail-Fast tamoyili: Agar ishlab chiqarish muhitida biron bir kritik xavfsizlik o'zgaruvchisi kiritilmagan bo'lsa, server jimjitlikda sukut bo'yicha (fallback) zaif kalitlar bilan ishga tushmasligi, balki zudlik bilan xato bilan to'xtashi shart.


---

### Topshiriq #1171: Argon2id parollarni xeshlash algoritmi (argon2 gem) va Bcrypt bilan solishtirish
**Tavsif:** Bcrypt algoritmi xotira talab qilmaydi va GPU klasterlarida tez sindirilishi mumkin. Password Hashing Competition g'olibi bo'lgan xotira-qattiq (memory-hard) Argon2id algoritmini joriy etish kerak.
**Talablar:** `argon2` gemi, `Argon2::Password.create`, t_cost (vaqt), m_cost (xotira - masalan 64MB) parametrlarini sozlash.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
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
end
```
**Tushuntirish:** Argon2id ning eng katta kuchi uning xotira talabchanligidadir (`m_cost`). Bitta parolni tekshirish uchun 64 MB xotira kerak bo'lsa, xakker o'zining GPU kartasida parallel ravishda millionlab parollarni tekshira olmaydi, chunki video karta xotirasi darhol to'lib qoladi.


---

### Topshiriq #1172: Devise autentifikatsiyasida xavfsizlik sozlamalari (Lockable, Trackable, Paranoid rejim)
**Tavsif:** Foydalanuvchi hisoblarini himoyalashda 5 ta noto'g'ri urinishdan so'ng hisobni qulflash (Lockable) va tajovuzkorga qaysi email mavjudligini bildirmaslik (Paranoid mode) talab qilinadi.
**Talablar:** Devise konfiguratsiyasi: `config.lock_strategy = :failed_attempts`, `config.maximum_attempts = 5`, `config.paranoid = true`.
**Yechim (Ruby):**
```ruby
# config/initializers/devise.rb
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
end
```
**Tushuntirish:** `config.paranoid = true` kiberxavfsizlikda 'User Enumeration' hujumlarining oldini oladi. Tizim foydalanuvchi bor bo'lsa ham, yo'q bo'lsa ham bir xil: 'Agar hisob mavjud bo'lsa, sizga ko'rsatma yuborildi' degan javobni qaytaradi.


---

### Topshiriq #1173: Ikki bosqichli autentifikatsiya (2FA / TOTP: RFC 6238) rotp gemi bilan
**Tavsif:** Google Authenticator yoki 1Password orqali har 30 soniyada o'zgaruvchi 6 xonali bir martalik kodlar (Time-Based One-Time Password) tizimini Rails ga integratsiya qilish lozim.
**Talablar:** `rotp` gemi, `ROTP::TOTP.new`, QR-kod havolasi (`provisioning_uri`), vaqt driftini hisobga oluvchi tasdiqlash (`verify(code, drift_behind: 15)`).
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
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
end
```
**Tushuntirish:** RFC 6238 standarti bo'yicha TOTP hozirgi Unix vaqtini 30 soniyalik darchalarga bo'ladi va maxfiy kalit bilan HMAC-SHA1 hisoblaydi. `drift_behind` foydalanuvchi telefonidagi soat server soatidan bir necha soniya orqada qolganda ham kodni to'g'ri qabul qilish imkonini beradi.


---

### Topshiriq #1174: WebAuthn / FIDO2 Passkeys autentifikatsiyasini Rails da joriy qilish
**Tavsif:** Parolsiz dunyoga o'tish: foydalanuvchi brauzeridagi Apple TouchID, FaceID yoki Windows Hello biometrik kalitlari bilan tizimga kirishini ta'minlash kerak.
**Talablar:** `webauthn` gemi, Challenge yaratish, Attestation va Assertion obyektlarini tekshirish.
**Yechim (Ruby):**
```ruby
# app/controllers/webauthn_sessions_controller.rb
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
end
```
**Tushuntirish:** Passkeys (FIDO2) phishing hujumlarini 100% bartaraf etadi. Brauzer autentifikatsiya paytida domen nomini tekshiradi, shu sababli hatto foydalanuvchi soxta (klonlangan) phishing saytiga kirsa ham, FaceID unga kalitni bermaydi.


---

### Topshiriq #1175: Parol murakkabligi va zxcvbn algoritmi orqali zaif parollarni tekshirish
**Tavsif:** Foydalanuvchilar 'Parol123!' kabi sodda parollar qo'yishining oldini olish uchun parollarning haqiqiy entropiyasini Dropbox ning `zxcvbn` algoritmi bilan baholash lozim.
**Talablar:** Entropiya balli (0 dan 4 gacha), lug'atlar va ketma-ketliklarni aniqlash, ball < 3 bo'lsa parolni rad etish.
**Yechim (Ruby):**
```ruby
# app/validators/strong_password_validator.rb
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
end
```
**Tushuntirish:** An'anaviy qoidalar (1 ta katta harf, 1 ta belgi) xavfsizlik bermaydi, chunki odamlar shunchaki 'Password123!' yozadi. `zxcvbn` esa fazoviy entropiyani hisoblaydi, klaviaturadagi ketma-ketliklarni (qwerty), mashhur ismlarni va sanalarni tahlil qilib, real himoyani ta'minlaydi.


---

### Topshiriq #1176: Sessiyalarni o'g'irlashdan himoyalash: Session Fixation va Session Regeneration
**Tavsif:** Foydalanuvchi tizimga kirishidan oldin unga berilgan sessiya ID sini saqlab qolib, keyinchalik uning hisobiga kirib olish (Session Fixation) xavfini yo'qotish kerak.
**Talablar:** Login vaqtida `reset_session` metodini chaqirish, yangi sessiya ID yaratish va eski ma'lumotlarni tozalash.
**Yechim (Ruby):**
```ruby
# app/controllers/sessions_controller.rb
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
end
```
**Tushuntirish:** Session Fixation hujumida xakker qurbonga o'zi bilgan sessiya ID sini (masalan URL yoki cookie orqali) beradi. Agar login paytida `reset_session` chaqirilmasa, foydalanuvchi tizimga kirgach ham xuddi shu ID faol qoladi va xakker foydalanuvchi hisobiga kirib oladi.


---

### Topshiriq #1177: Brute-Force hujumlaridan himoyalanish: hisobni avtomatik bloklash va ogohlantirish
**Tavsif:** Parollarni avtomatlashtirilgan robotlar bilan sinab ko'rishni to'xtatish uchun ketma-ket muvaffaqiyatsiz urinishlarni hisoblab boruvchi va IP/foydalanuvchini bloklovchi modul kerak.
**Talablar:** Redis yordamida muvaffaqiyatsiz urinishlarni hisoblash, 5 tadan oshsa bloklash va xavfsizlik xabarini yuborish.
**Yechim (Ruby):**
```ruby
# app/services/login_attempt_tracker.rb
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
end
```
**Tushuntirish:** Redis da `failed_logins` hisoblagichini TTL bilan saqlash ma'lumotlar bazasiga ortiqcha yuklama bermasdan, daqiqasiga o'n minglab hujumlarni osonlik bilan filtrlaydi.


---

### Topshiriq #1178: JWT (JSON Web Token) xavfsiz imzolash va Asimmetrik (RS256) validatsiya
**Tavsif:** Mikroxizmatlar arxitekturasida barcha xizmatlarga umumiy sirni (HMAC shared secret) tarqatmaslik uchun autentifikatsiya serveri JWT ni xususiy kalit bilan imzolashi, qolgan servislar esa faqat ochiq kalit bilan tekshirishi lozim.
**Talablar:** `jwt` gemi, RS256 algoritmi, `iss`, `aud`, `exp` claims parametrlarini qat'iy tekshirish.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
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
end
```
**Tushuntirish:** RS256 asimmetrik shifrlash usuli bo'lib, ommaviy kalitni istalgan tashqi mikroxizmat yoki frontendga berish xavfsizdir. Agar biron bir mikroxizmat buzib kirilsa ham, u yangi soxta JWT yarata olmaydi, chunki xususiy kalit faqat markaziy autentifikatsiya serverida saqlanadi.


---

### Topshiriq #1179: OAuth2 / OpenID Connect Single Sign-On (SSO) provayderi xavfsizligi
**Tavsif:** OmniAuth orqali Google, GitHub yoki Apple orqali kirishda CSRF va State tampering hujumlarining oldini olish lozim.
**Talablar:** `state` parametrini tekshirish, `origin` va `nonce` parametrlarini tasdiqlash.
**Yechim (Ruby):**
```ruby
# config/initializers/omniauth.rb
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
OmniAuth.config.allowed_request_methods = [:post]
```
**Tushuntirish:** OmniAuth da GET so'rovlari orqali login qilish xavflidir, chunki tajovuzkor `<img>` teglari orqali qurbonning hisobini o'z akkauntiga ulab qo'yishi mumkin. Faqat POST metodiga ruxsat berish va `state` parametrini tekshirish ushbu zaiflikni bartaraf qiladi.


---

### Topshiriq #1180: Maxfiy parollarni ma'lumotlar bazasidan qidirishsiz va xeshsiz saqlamaslik auditi
**Tavsif:** Ma'lumotlar bazasi zaxira nusxasi sizib chiqqanda ham hech bir parol yoki to'liq karta raqami ochiq holda ko'rinmasligi uchun model darajasida audit tekshiruvi kerak.
**Talablar:** Faqat `password_digest` saqlash, `has_secure_password` dan foydalanish, modelda ochiq parol atributlarini xotirada qoldirmaslik.
**Yechim (Ruby):**
```ruby
# app/models/user.rb
class User < ApplicationRecord
  # has_secure_password parolni ochiq holda saqlamaydi,
  # balki uni bcrypt bilan xeshlab password_digest ga yozadi
  has_secure_password

  validates :password, length: { minimum: 12 }, allow_nil: true

  # Bazaga tasodifan parolni ochiq yozishdan himoyalovchi callback
  before_validation do
    self.password = nil if password.blank?
  end
end
```
**Tushuntirish:** `has_secure_password` virtual `password` va `password_confirmation` atributlarini yaratadi. Validatsiyadan so'ng parollar darhol xeshlanadi va SQL bazasiga faqat `password_digest` boradi. Ochiq matn hech qachon diskka yozilmaydi.


---

### Topshiriq #1181: Rails CSRF himoyasi: protect_from_forgery with: :exception va Form Authenticity Token
**Tavsif:** Boshqa zararli saytlar foydalanuvchining nomidan soxta POST/DELETE so'rovlarini (masalan pul o'tkazish) yubormasligi (Cross-Site Request Forgery) uchun qat'iy token tekshiruvini yoqish kerak.
**Talablar:** `protect_from_forgery with: :exception`, har bir shaklda (form) `authenticity_token` kiritilishi va tekshirilishi.
**Yechim (Ruby):**
```ruby
# app/controllers/application_controller.rb
class ApplicationController < ActionController::Base
  # CSRF token mos kelmasa darhol Exception tashlash
  protect_from_forgery with: :exception

  # API kontrollerlari uchun null_session rejimiga o'tish
  # protect_from_forgery with: :null_session
end
```
**Tushuntirish:** Rails CSRF mexanizmi har bir foydalanuvchi sessiyasi uchun unikal kriptografik token yaratadi. Har bir HTML formaga yashirin `authenticity_token` maydoni kiritiladi. Brauzer POST qilganda, Rails tokenni dekodlab, sessiya kaliti bilan solishtiradi. Begona sayt bu tokenni o'qiy olmaydi (Same-Origin Policy tufayli).


---

### Topshiriq #1182: AJAX / Single Page Applications (SPA) uchun CSRF token almashinuvi
**Tavsif:** React, Vue yoki oddiy `fetch()` chaqiruvlarida Rails backendga JSON so'rovlar yuborilganda CSRF tokenini `X-CSRF-Token` sarlavhasi orqali xavfsiz uzatish lozim.
**Talablar:** HTML meta tegdan tokenni olish (`csrf_meta_tags`), har bir JavaScript so'roviga sarlavha qo'shish.
**Yechim (Ruby):**
```ruby
// app/javascript/packs/api_client.js
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
}
```
**Tushuntirish:** SPA ilovalarda Rails sahifani to'liq qayta render qilmaydi. Shuning uchun `csrf_meta_tags` orqali berilgan token JavaScript xotirasiga olinadi va har bir AJAX so'rovida `X-CSRF-Token` HTTP sarlavhasida uzatiladi.


---

### Topshiriq #1183: Content Security Policy (CSP) konfiguratsiyasi Rails 7 da (content_security_policy.rb)
**Tavsif:** Xakker saytga zararli JavaScript kodini joylab ketgan taqdirda ham (XSS), brauzer begona domenlardan skriptlar yuklamasligi va inline skriptlarni bajarmasligi lozim.
**Talablar:** `Rails.application.config.content_security_policy` orqali `default-src 'self'`, `script_src`, `nonce_generator` sozlash.
**Yechim (Ruby):**
```ruby
# config/initializers/content_security_policy.rb
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
end
```
**Tushuntirish:** CSP (Content Security Policy) zamonaviy brauzer xavfsizligining eng kuchli himoyasidir. Agar sahifada hatto tajovuzkor kiritgan `<script>alert(1)</script>` tegi bo'lsa ham, unda to'g'ri `nonce` attributi bo'lmasa, brauzer skriptni ijro etishdan bosh tortadi.


---

### Topshiriq #1184: XSS (Cross-Site Scripting) himoyasi: ERB::Util.html_escape, sanitize va SafeBuffer
**Tavsif:** Foydalanuvchi sharhlarida va profillarida yozilgan HTML teglarni xavfsiz qabul qilish, zararli `<script>` va `onload=` hodisalarini filtrdan tozalash kerak.
**Talablar:** `sanitize` helperidan foydalanish, faqat ruxsat etilgan teglarni (`tags: %w[b i p]`) qoldirish, `raw` yoki `html_safe` ni ehtiyotkorlik bilan ishlatish.
**Yechim (Ruby):**
```ruby
# app/helpers/sanitization_helper.rb
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
end
```
**Tushuntirish:** Rails ERB shablonlari sukut bo'yicha barcha o'zgaruvchilarni avtomatik tarzda HTML-escape qiladi (`<` belgisi `&lt;` ga aylanadi). Dasturchi hech qachon tekshirilmagan foydalanuvchi ma'lumotlariga `.html_safe` yoki `raw()` qo'llamasligi shart, aks holda Stored XSS zaifligi ochiladi.


---

### Topshiriq #1185: SQL Injection va Arel: Xom SQL (find_by_sql, where("...")) zaifliklarini audit qilish
**Tavsif:** Foydalanuvchi kiritgan satrlarni to'g'ridan-to'g'ri SQL so'roviga birlashtirish (String Interpolation) orqali yuzaga keluvchi SQL Injection zaifligini bartaraf qilish lozim.
**Talablar:** Xom SQL satrlarini parametrlangan (Parameterized/Prepared Statements) so'rovlarga o'zgartirish, Arel orqali xavfsiz SQL generatsiyasi.
**Yechim (Ruby):**
```ruby
# app/services/secure_user_search.rb
class SecureUserSearch
  # XAVFLI (SQL Injection mavjud):
  # User.where("name LIKE '%#{params[:query]}%'") -- MUTLAQO MUMKIN EMAS!

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
end
```
**Tushuntirish:** Parametrlangan so'rovlarda ma'lumotlar bazasi drayveri kiruvchi ma'lumotlarni hech qachon SQL buyrug'i deb qabul qilmaydi, balki ularni faqatgina oddiy literallar sifatida qayta ishlaydi. Bu `OR 1=1` kabi barcha klassik SQL Injection hiylalarini bekor qiladi.


---

### Topshiriq #1186: Strong Parameters orqali Mass Assignment zaifliklarini bartaraf etish
**Tavsif:** Foydalanuvchi ro'yxatdan o'tayotganda HTTP so'rovi ichiga `admin: true` parametrini qo'shib yuborib o'zini admin qilib qo'yishining (Mass Assignment) oldini olish lozim.
**Talablar:** `params.require(:user).permit(...)` dan foydalanish, faqat ruxsat etilgan maydonlarni filtrdan o'tkazish.
**Yechim (Ruby):**
```ruby
# app/controllers/users_controller.rb
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
end
```
**Tushuntirish:** Strong Parameters Rails 4 dan boshlab majburiy qilingan. Agar so'rovda `permit` qilinmagan parametrlar kelsa, Rails ularni shunchaki e'tiborsiz qoldiradi va bazaga yozmaydi, bu esa ruxsatsiz huquqlarni oshirishni (Privilege Escalation) to'xtatadi.


---

### Topshiriq #1187: SSRF (Server-Side Request Forgery) himoyasi: Ichki IP diapazonlarini filtrlash
**Tavsif:** Ilova foydalanuvchi ko'rsatgan havola bo'yicha veb-sayt skrinshotini oladigan bo'lsa, xakker `http://169.254.169.254/latest/meta-data/` yoki `http://localhost:6379/` kiritib ichki tarmoqni skanerlashi mumkin.
**Talablar:** IP manzilni tekshirish, maxfiy/lokal IP diapazonlarini (`IPAddr.new('127.0.0.0/8')`, `10.0.0.0/8`, `169.254.0.0/16`) bloklash.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
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
end
```
**Tushuntirish:** SSRF bulutli tizimlarda (AWS, GCP) eng xavfli zaiflikdir. Xakker serverni o'zining nomidan ichki AWS Metadata servisiga murojaat qildirib, IAM xavfsizlik rollari va kalitlarini o'g'irlashi mumkin. Har bir tashqi so'rov oldidan IP diapazonlarini tekshirish shart.


---

### Topshiriq #1188: Clickjacking himoyasi va X-Frame-Options sarlavhasi
**Tavsif:** Tajovuzkor o'z saytiga shaffof `<iframe>` orqali bizning saytimizni joylashtirib, foydalanuvchini alqov orqali tugmalarni bosishga majburlashining (Clickjacking) oldini olish lozim.
**Talablar:** `X-Frame-Options: SAMEORIGIN` yoki `DENY` sarlavhasini o'rnatish, CSP `frame-ancestors 'self'` ni belgilash.
**Yechim (Ruby):**
```ruby
# config/initializers/security_headers.rb
Rails.application.config.action_dispatch.default_headers.merge!(
  # Clickjacking himoyasi
  'X-Frame-Options' => 'DENY', # Hech qaysi sayt saytimizni iframe ichiga joylay olmaydi

  # XSS filtri
  'X-XSS-Protection' => '1; mode=block',

  # Mime-turi mos kelmasa yuklamaslik
  'X-Content-Type-Options' => 'nosniff'
)
```
**Tushuntirish:** `X-Frame-Options: DENY` brauzerga ushbu saytni biron bir boshqa sahifaning `<iframe>` tegi ichida ko'rsatishni qat'iyan taqiqlaydi. Natijada foydalanuvchi aldov yo'li bilan maxfiy amallarni bajarishga jalb qilinmaydi.


---

### Topshiriq #1189: Fayl yuklash xavfsizligi: Mime-type spoofing va zararli SVG/Polyglot skriptlarni filtrlash
**Tavsif:** Foydalanuvchi rasm o'rniga ichiga `<script>` yashiringan soxta SVG yoki PHP/Ruby bajariluvchi skriptlarni (Polyglot files) yuklashining oldini olish kerak.
**Talablar:** `marcel` gemi orqali haqiqiy binar sehrli raqamlarni (Magic bytes) tekshirish, fayl kengaytmasi va uning ichki kontentini solishtirish.
**Yechim (Ruby):**
```ruby
# app/validators/secure_attachment_validator.rb
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
end
```
**Tushuntirish:** Fayl kengaytmasini `.jpg` deb nomlab qo'yish uning rasm ekanligini bildirmaydi. `Marcel` kutubxonasi faylning dastlabki baytlarini (Magic bytes, masalan PNG uchun `89 50 4E 47`) tekshirib, haqiqiy formatni aniqlaydi va zararli fayllarni bloklaydi.


---

### Topshiriq #1190: Ochiq qayta yo'naltirish (Open Redirect) zaifligini aniqlash va xavfsiz redirect_to
**Tavsif:** Saytda login qilingach `params[:return_to]` manziliga yo'naltirish mantig'i bo'lsa, xakker `?return_to=https://evil-phishing.com` berib foydalanuvchini soxta saytga o'g'irlashi mumkin.
**Talablar:** `redirect_to` funksiyasida `allow_other_host: false` (Rails 7 standarti) qo'llash yoki faqat ruxsat etilgan domenlarni oq ro'yxatda tekshirish.
**Yechim (Ruby):**
```ruby
# app/controllers/redirect_controller.rb
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
end
```
**Tushuntirish:** Open Redirect zaifligi ko'pincha phishing kampaniyalarida qo'llaniladi. Foydalanuvchi manzil satrida haqiqiy bank domenini ko'radi, ammo login qilgach soxta saytga sakrab o'tib ketadi. `allow_other_host: false` bu xavfni to'liq yo'qotadi.


---

### Topshiriq #1191: Rack::Attack orqali IP bo'yicha Rate Limiting (Throttle)
**Tavsif:** Har qanday bitta IP manzildan sekundiga 10 tadan ortiq yoki daqiqasiga 300 tadan ortiq so'rovlar kelganda ularga HTTP 429 Too Many Requests javobini qaytarish lozim.
**Talablar:** `Rack::Attack.throttle` sozlamasi, Redis kesh backend, limitdan oshganda maxsus JSON javob qaytarish.
**Yechim (Ruby):**
```ruby
# config/initializers/rack_attack.rb
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
      [{ error: 'Tezlik chegarasidan oshildi. Birozdan so\'ng qayta urining.' }.to_json]
    ]
  end
end
```
**Tushuntirish:** `Rack::Attack` Rails so'rovlar zanjirining eng boshida, Rack middleware darajasida ishlaydi. U so'rovlarni Controller yoki Ma'lumotlar bazasiga yetkazmasdanoq filtrlaydi, bu esa serverni DDoS hujumlarida yiqilishdan asraydi.


---

### Topshiriq #1192: Rack::Attack orqali soxta login urinishlarini cheklash (Fail2ban uslubida)
**Tavsif:** Bitta foydalanuvchi hisobiga yoki bitta IP dan login sahifasiga qilinayotgan ketma-ket urinishlarni 20 soniyada 5 tadan oshirmaslik lozim.
**Talablar:** Login POST marshrutini filtrlash (`req.path == '/login' && req.post?`), IP va email bo'yicha alohida darchalar o'rnatish.
**Yechim (Ruby):**
```ruby
# config/initializers/rack_attack_login.rb
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
end
```
**Tushuntirish:** Bitta tajovuzkor 1000 ta proksi IP orqali bitta maqsadli emailni sindirmoqchi bo'lishi mumkin. Email bo'yicha alohida keshli throttle qo'yish tarmoqlangan kiberhujumlarni ham to'xtata oladi.


---

### Topshiriq #1193: Rack::Attack orqali zararli skanerlar va User-Agentlarni bloklash (Blocklist)
**Tavsif:** Saytni skanerlayotgan avtomatik zaiflik qidiruvchilari (Nikto, SQLMap, WPScan) va `.php`, `.env` kabi fayllarni qidirayotgan robotlarni darhol bloklash talab etiladi.
**Talablar:** `Rack::Attack.blocklist` sozlamasi, User-Agent regex filtri va qidirilayotgan xavfli fayllar yo'li.
**Yechim (Ruby):**
```ruby
# config/initializers/rack_attack_blocklist.rb
class Rack::Attack
  # Xakerlik skanerlarini bloklash
  blocklist('block_malicious_user_agents') do |req|
    req.user_agent =~ /(nikto|sqlmap|wpscan|dirbuster|acunetix)/i
  end

  # PHP yoki muhit fayllarini qidirayotgan so'rovlarni darhol to'xtatish
  blocklist('block_probe_paths') do |req|
    req.path =~ /(\.php|wp-admin|\.env|\.git|phpmyadmin)/i
  end
end
```
**Tushuntirish:** Rails ilovasi PHP emas, ammo internetdagi botlar barcha saytlarni standart `.env` yoki `wp-admin` bo'yicha doimiy skanerlaydi. Ularni Rack darajasidayoq bloklab qo'yish loglarni toza saqlaydi va keraksiz yuklamani kamaytiradi.


---

### Topshiriq #1194: Brakeman statik xavfsizlik tahlilchisi (Static Analysis Security Testing) va ogohlantirishlar
**Tavsif:** Loyiha kod bazasida yashiringan zaifliklarni (SQLi, XSS, CSRF, Mass Assignment) avtomatlashtirilgan CI/CD konveyerida aniqlash uchun Brakeman tahlilini sozlash lozim.
**Talablar:** Brakeman konfiguratsiyasi (`config/brakeman.ignore`), xavflilik darajasi (Confidence: High/Medium) bo'yicha filtrlash va xatolik berilganda CI ni to'xtatish.
**Yechim (Ruby):**
```ruby
# lib/tasks/security_audit.rake
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
end
```
**Tushuntirish:** Brakeman dastur kodini ishga tushirmasdan (Static AST tahlil) o'rganadi. U Rails ning ichki konventsiyalarini chuqur tushunadi va ochiq qolgan `find_by_sql` yoki filtrlanmagan `redirect_to` parametrlarini sekunlar ichida topadi.


---

### Topshiriq #1195: Bundler-audit orqali zaif Gem qaramliklarini (CVE) aniqlash va avtomat yangilash
**Tavsif:** Loyihaga ulangan Gem kutubxonalarida (masalan eski `actionview` yoki `nokogiri`) xalqaro kiberxavfsizlik zaifliklari (CVE) paydo bo'lganda darhol xabar topish kerak.
**Talablar:** `bundler-audit` kutubxonasi, zaifliklar bazasini yangilash (`bundle-audit update`) va skanerlash.
**Yechim (Ruby):**
```ruby
# lib/tasks/dependency_audit.rake
namespace :security do
  desc 'Gem qaramliklarini CVE zaifliklari bo\'yicha tekshirish'
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
end
```
**Tushuntirish:** Ko'plab yirik kiberhujumlar uchinchi tomon kutubxonalari (Supply Chain Attacks) orqali amalga oshadi. `bundler-audit` har kuni yangilanadigan Ruby Advisory Database bazasi bilan solishtirib, loyihani o'z vaqtida himoyalaydi.


---

### Topshiriq #1196: Sensitiv ma'lumotlarni loglardan filtrlash (config.filter_parameters)
**Tavsif:** Foydalanuvchining paroli, pasport seriyasi yoki plastik karta raqami server xatolikka uchraganda `log/production.log` fayliga ochiq matnda tushib qolmasligi shart.
**Talablar:** `config.filter_parameters` ro'yxatini kengaytirish, parollar va tokenlarni `[FILTERED]` bilan almashtirish.
**Yechim (Ruby):**
```ruby
# config/initializers/filter_parameter_logging.rb
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
]
```
**Tushuntirish:** Log fayllari ko'pincha tashqi monitoring tizimlariga (ELK, Datadog) yuboriladi va u yerda o'nlab ma'murlar va dasturchilar kirish huquqiga ega bo'ladi. Maxfiy parametrlarni Rails darajasida filtrlab yuborish ma'lumotlar o'g'irlanishini oldini oladi.


---

### Topshiriq #1197: CORS (Cross-Origin Resource Sharing) xavfsiz sozlamalari (rack-cors gem)
**Tavsif:** API shlyuziga boshqa domenlardan (masalan `evil-site.com`) ruxsatsiz so'rovlar yuborilishini to'xtatish uchun faqat ruxsat etilgan frontend domenlarini ko'rsatish lozim.
**Talablar:** `rack-cors` gemi, `origins` oq ro'yxati, `credentials: true` bilan faqat ishonchli domenlarga ruxsat berish.
**Yechim (Ruby):**
```ruby
# config/initializers/cors.rb
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
end
```
**Tushuntirish:** CORS da hech qachon `origins '*'` va `credentials: true` ni birgalikda ishlatmaslik kerak. Bu har qanday zararli saytga foydalanuvchining shaxsiy ma'lumotlarini brauzer orqali o'g'irlashiga ochiq eshik qoldiradi.


---

### Topshiriq #1198: Xavfsiz HTTP sarlavhalari (Strict-Transport-Security, Permissions-Policy)
**Tavsif:** Brauzerni faqat HTTPS orqali ishlashga majburlash (HSTS) va sahifada mikrofon yoki kameradan ruxsatsiz foydalanishni cheklash zarur.
**Talablar:** HSTS `max-age=63072000; includeSubDomains; preload`, `Permissions-Policy` sozlamalari.
**Yechim (Ruby):**
```ruby
# config/initializers/hsts_headers.rb
Rails.application.config.action_dispatch.default_headers.merge!(
  # HSTS: 2 yil davomida barcha subdomenlar bilan faqat HTTPS
  'Strict-Transport-Security' => 'max-age=63072000; includeSubDomains; preload',

  # Permissions Policy: Kamera, mikrofon va geolokatsiyani taqiqlash
  'Permissions-Policy' => 'camera=(), microphone=(), geolocation=()'
)
```
**Tushuntirish:** HSTS (HTTP Strict Transport Security) brauzerga saytga hech qachon oddiy `http://` orqali ulanmaslikni buyuradi. Bu SSL-Stripping hujumlarini (xakker HTTPS ni HTTP ga tushirib ma'lumotlarni o'g'irlashini) to'liq to'xtatadi.


---

### Topshiriq #1199: Kiberxavfsizlik voqealari auditi: ActiveSupport::Notifications orqali xavfsizlik SIEM loglari
**Tavsif:** Muvaffaqiyatsiz loginlar, parolni o'zgartirishlar va shubhali so'rovlar yuz berganda xavfsizlik bo'limining SIEM monitoring tizimiga voqea hodisalarini (Security Events) uzatish kerak.
**Talablar:** `ActiveSupport::Notifications.instrument` va `subscribe` orqali xavfsizlik auditi jurnali (Audit Trail).
**Yechim (Ruby):**
```ruby
# app/services/security_event_broadcaster.rb
class SecurityEventBroadcaster
  def self.log_security_event(event_name, payload = {})
    ActiveSupport::Notifications.instrument("security.\#{event_name}", payload.merge(timestamp: Time.now.utc))
  end
end

# config/initializers/security_notifications.rb
ActiveSupport::Notifications.subscribe(/security\./) do |name, start, finish, id, payload|
  # SIEM formatidagi log yozuvi
  Rails.logger.warn("[SECURITY EVENT] Event: \#{name} | User: \#{payload[:user_id]} | IP: \#{payload[:ip]} | Details: \#{payload.inspect}")
end
```
**Tushuntirish:** `ActiveSupport::Notifications` hodisaga asoslangan (Event-Driven) arxitekturani ta'minlaydi. Xavfsizlik auditi asosiy biznes mantiqqa ta'sir qilmasdan alohida obunachi orqali SIEM yoki Kafka tizimlariga oqimli uzatiladi.


---

### Topshiriq #1200: To'liq korporativ Rails xavfsizlik himoya qalqoni (Comprehensive Security Shield)
**Tavsif:** Tizimning barcha xavfsizlik mexanizmlarini (WAF qoidalari, kalitlar holati, shifrlash zanjiri, zaifliklar va audit holati) bitta markaziy xavfsizlik boshqaruv panelida tekshirish va tasdiqlash.
**Talablar:** Barcha xavfsizlik holatlarini birlashtiruvchi sinov shlyuzi, to'liq mudofaa zanjiri tahlili.
**Yechim (Ruby):**
```ruby
# lib/security_shield_health.rb
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
    puts "\n=== KHORAZMIY AI RAILS XAVFSIZLIK QALQONI AUDITI ==="
    status.each do |feature, enabled|
      puts " * \#{feature}: \#{enabled ? 'HIMOYALANGAN' : 'DIQQAT: ZAIF'}"
    end
    puts "Yakuniy Xulosa: \#{all_secure ? 'TIZIM 100% XAVFSIZ' : 'ZUDLIK BILAN SOZLANG'}"
    all_secure
  end
end
```
**Tushuntirish:** Ushbu xavfsizlik qalqoni korxona miqyosidagi Rails ilovalarining to'liq xavfsizlik holatini tasdiqlaydi. Kriptografiya, autentifikatsiya, tarmoq filtrlari va audit jurnallari yagona xavfsizlik ekotizimini hosil qiladi.

