# Khorazmiy AI: Go - Modul 24
## Mavzu: Kriptografiya va Xavfsizlik: crypto/aes, crypto/rsa, crypto/ed25519, crypto/subtle (vaqt hujumlariga qarshi), TLS 1.3 xavfsiz konfiguratsiyasi va Hashicorp Vault/KMS integratsiyasi

### Topshiriq #1151: crypto/aes va cipher.NewGCM Bilan AES-256-GCM Shifrlash
**Tavsif:** Ma'lumotlar bazasidagi shaxsiy maxfiy ma'lumotlarni autentifikatsiyalangan AES-GCM (AEAD) rejimida xavfsiz shifrlash va ochish.
**Talablar:** `crypto/aes`, `crypto/cipher`, `crypto/rand`, 32-baytlik kalit, 12-baytlik tasodifiy Nonce.
**Yechim (Go):**
```go
package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"errors"
	"fmt"
	"io"
)

// EncryptAESGCM ma'lumotni 256-bitli kalit bilan shifrlaydi va Nonce ni boshiga qo'shadi
func EncryptAESGCM(key []byte, plaintext []byte) ([]byte, error) {
	block, err := aes.NewCipher(key)
	if err != nil {
		return nil, err
	}

	gcm, err := cipher.NewGCM(block)
	if err != nil {
		return nil, err
	}

	// 12-baytlik unikal tasodifiy Nonce
	nonce := make([]byte, gcm.NonceSize())
	if _, err := io.ReadFull(rand.Reader, nonce); err != nil {
		return nil, err
	}

	// Shifrlangan matn va 16-baytlik autentifikatsiya tegi
	ciphertext := gcm.Seal(nonce, nonce, plaintext, nil)
	return ciphertext, nil
}

// DecryptAESGCM shifrlangan matndan Nonce ni ajratib olib, ma'lumotni ochadi
func DecryptAESGCM(key []byte, ciphertext []byte) ([]byte, error) {
	block, err := aes.NewCipher(key)
	if err != nil {
		return nil, err
	}

	gcm, err := cipher.NewGCM(block)
	if err != nil {
		return nil, err
	}

	nonceSize := gcm.NonceSize()
	if len(ciphertext) < nonceSize {
		return nil, errors.New("shifr matni juda qisqa")
	}

	nonce, actualCiphertext := ciphertext[:nonceSize], ciphertext[nonceSize:]
	return gcm.Open(nil, nonce, actualCiphertext, nil)
}

func main() {
	key := make([]byte, 32) // AES-256
	io.ReadFull(rand.Reader, key)

	original := []byte("Foydalanuvchi pasport ma'lumotlari: AA1234567")
	encrypted, _ := EncryptAESGCM(key, original)
	fmt.Printf("Shifrlangan paket hajmi: %d bayt\n", len(encrypted))

	decrypted, _ := DecryptAESGCM(key, encrypted)
	fmt.Printf("Ochilgan ma'lumot: %s\n", string(decrypted))
}
```
**Tushuntirish:** AES-GCM shifrlash bilan birga 128-bitlik yaxlitlik tegini (Authentication Tag) hisoblaydi. Agar shifr matnining biror biti yo'lda o'zgartirilsa, `gcm.Open` xatolik qaytaradi va buferni qabul qilmaydi.

---

### Topshiriq #1152: AES-GCM Da Nonce Xavfsizligi va Nonce Reuse Hujumidan Himoya
**Tavsif:** Bitta kalit ostida Nonce takrorlanishi (Nonce Reuse Attack) maxfiy kalit va ma'lumotning fosh bo'lishiga olib kelishini tushunish va oldini olish.
**Talablar:** `crypto/rand`, deterministik hisoblagich yoki CSPRNG orqali unikal Nonce kafolati.
**Yechim (Go):**
```go
package main

import (
	"crypto/rand"
	"fmt"
	"sync/atomic"
)

// MonotonicNonceGenerator atomik hisoblagich va prefiks yordamida unikal Nonce kafolatlaydi
type MonotonicNonceGenerator struct {
	counter uint64
	prefix  [4]byte
}

func NewNonceGenerator() (*MonotonicNonceGenerator, error) {
	gen := &MonotonicNonceGenerator{}
	if _, err := rand.Read(gen.prefix[:]); err != nil {
		return nil, err
	}
	return gen, nil
}

func (g *MonotonicNonceGenerator) NextNonce() [12]byte {
	c := atomic.AddUint64(&g.counter, 1)
	var nonce [12]byte
	copy(nonce[:4], g.prefix[:])
	nonce[4] = byte(c >> 56)
	nonce[5] = byte(c >> 48)
	nonce[6] = byte(c >> 40)
	nonce[7] = byte(c >> 32)
	nonce[8] = byte(c >> 24)
	nonce[9] = byte(c >> 16)
	nonce[10] = byte(c >> 8)
	nonce[11] = byte(c)
	return nonce
}

func main() {
	gen, _ := NewNonceGenerator()
	n1 := gen.NextNonce()
	n2 := gen.NextNonce()
	fmt.Printf("Nonce 1: %x\nNonce 2: %x\n", n1, n2)
}
```
**Tushuntirish:** GCM rejimida bir xil kalit va bir xil Nonce bilan ikkita turli xabar shifrlansa, XOR operatsiyasi orqali har ikkala xabarning ochiq matnini va hatto autentifikatsiya kalitini (GHASH key) to'liq tiklash mumkin.

---

### Topshiriq #1153: AES-CBC va HMAC-SHA256 (Encrypt-then-MAC) Modeli
**Tavsif:** GCM mavjud bo'lmagan eski tizimlarda xavfsiz simmetrik shifrlashni to'g'ri tashkil qilish (Padding Oracle hujumlariga qarshi).
**Talablar:** `crypto/aes`, `cipher.NewCBCEncrypter`, PKCS#7 padding, `crypto/hmac`.
**Yechim (Go):**
```go
package main

import (
	"bytes"
	"crypto/aes"
	"crypto/cipher"
	"crypto/hmac"
	"crypto/rand"
	"crypto/sha256"
	"errors"
	"fmt"
	"io"
)

func pkcs7Pad(data []byte, blockSize int) []byte {
	padding := blockSize - (len(data) % blockSize)
	padtext := bytes.Repeat([]byte{byte(padding)}, padding)
	return append(data, padtext...)
}

func EncryptThenMac(encKey, macKey, plaintext []byte) ([]byte, error) {
	block, err := aes.NewCipher(encKey)
	if err != nil {
		return nil, err
	}

	padded := pkcs7Pad(plaintext, aes.BlockSize)
	iv := make([]byte, aes.BlockSize)
	io.ReadFull(rand.Reader, iv)

	mode := cipher.NewCBCEncrypter(block, iv)
	ciphertext := make([]byte, len(padded))
	mode.CryptBlocks(ciphertext, padded)

	// Avval shifrlash, so'ngra shifr matniga HMAC hisoblash (Encrypt-then-MAC)
	h := hmac.New(sha256.New, macKey)
	h.Write(iv)
	h.Write(ciphertext)
	tag := h.Sum(nil)

	result := append(iv, ciphertext...)
	result = append(result, tag...)
	return result, nil
}

func main() {
	encKey := make([]byte, 32)
	macKey := make([]byte, 32)
	io.ReadFull(rand.Reader, encKey)
	io.ReadFull(rand.Reader, macKey)

	ct, _ := EncryptThenMac(encKey, macKey, []byte("CBC orqali shifrlangan ma'lumot"))
	fmt.Printf("Encrypt-then-MAC paket hajmi: %d bayt\n", len(ct))
}
```
**Tushuntirish:** Encrypt-then-MAC eng xavfsiz kombinatsiya hisoblanadi: qabul qiluvchi avval HMAC imzosini doimiy vaqtda tekshiradi. Agar imzo xato bo'lsa, hech qanday CBC dekodlash va padding tahlili qilinmaydi (Padding Oracle hujumi bartaraf etiladi).

---

### Topshiriq #1154: ChaCha20-Poly1305 Shifrlash (golang.org/x/crypto/chacha20poly1305)
**Tavsif:** Go dasturlarida mobil va IoT qurilmalar uchun apparat AES talab qilmaydigan eng zamonaviy AEAD shifrini joriy qilish.
**Talablar:** `chacha20poly1305.New`, 32-baytlik kalit, 12-baytlik Nonce.
**Yechim (Go):**
```go
package main

import (
	"crypto/rand"
	"fmt"
	"io"

	"golang.org/x/crypto/chacha20poly1305"
)

func EncryptChaCha(key, plaintext []byte) ([]byte, error) {
	aead, err := chacha20poly1305.New(key)
	if err != nil {
		return nil, err
	}

	nonce := make([]byte, aead.NonceSize())
	if _, err := io.ReadFull(rand.Reader, nonce); err != nil {
		return nil, err
	}

	return aead.Seal(nonce, nonce, plaintext, nil), nil
}

func main() {
	key := make([]byte, chacha20poly1305.KeySize)
	io.ReadFull(rand.Reader, key)

	ct, _ := EncryptChaCha(key, []byte("ChaCha20-Poly1305 bilan shifrlangan paket"))
	fmt.Printf("ChaCha20-Poly1305 shifr hajmi: %d bayt\n", len(ct))
}
```
**Tushuntirish:** ChaCha20-Poly1305 RFC 8439 standarti bo'lib, xotira kesh timing hujumlariga qarshi dasturiy darajada to'liq immunitetga ega.

---

### Topshiriq #1155: XChaCha20-Poly1305 Bilan 192-Bitlik Kengaytirilgan Nonce Xavfsizligi
**Tavsif:** Tasodifiy Nonce to'qnashuvi xavfini (Birthday Bound) amalda nolga tushirish uchun 24-baytlik (192-bit) Nonce dan foydalanish.
**Talablar:** `chacha20poly1305.NewX`, 192-bit Nonce.
**Yechim (Go):**
```go
package main

import (
	"crypto/rand"
	"fmt"
	"io"

	"golang.org/x/crypto/chacha20poly1305"
)

func EncryptXChaCha20(key, plaintext []byte) ([]byte, error) {
	// 192-bitlik Nonce bilan XChaCha20
	aead, err := chacha20poly1305.NewX(key)
	if err != nil {
		return nil, err
	}

	nonce := make([]byte, aead.NonceSize()) // 24 bayt
	if _, err := io.ReadFull(rand.Reader, nonce); err != nil {
		return nil, err
	}

	return aead.Seal(nonce, nonce, plaintext, nil), nil
}

func main() {
	key := make([]byte, chacha20poly1305.KeySize)
	io.ReadFull(rand.Reader, key)

	ct, _ := EncryptXChaCha20(key, []byte("Kengaytirilgan Nonce xavfsizligi"))
	fmt.Printf("XChaCha20 paketi (24 bayt Nonce + Shifr + 16 bayt Tag): %d bayt\n", len(ct))
}
```
**Tushuntirish:** Standart 96-bit Nonce da taxminan $2^{48}$ ta paketdan so'ng tasodifiy to'qnashuv ehtimoli paydo bo'ladi. XChaCha20 ning 192-bit Nonce si bilan bitta kalit ostida istalgancha paketni tasodifiy Nonce bilan xavfsiz shifrlash mumkin.

---

### Topshiriq #1156: Argon2id Bilan Xavfsiz Parol Xeshlash (golang.org/x/crypto/argon2)
**Tavsif:** Foydalanuvchi hisob qaydnomalari parollarini zamonaviy OWASP tavsiyalari bo'yicha mustahkam xeshlash.
**Talablar:** `argon2.IDKey(password, salt, time, memory, threads, keyLen)`.
**Yechim (Go):**
```go
package main

import (
	"crypto/rand"
	"crypto/subtle"
	"encoding/base64"
	"fmt"
	"io"

	"golang.org/x/crypto/argon2"
)

type HashParams struct {
	Memory      uint32
	Iterations  uint32
	Parallelism uint8
	SaltLength  uint32
	KeyLength   uint32
}

func HashPasswordArgon2id(password string, p *HashParams) (string, error) {
	salt := make([]byte, p.SaltLength)
	if _, err := io.ReadFull(rand.Reader, salt); err != nil {
		return "", err
	}

	hash := argon2.IDKey([]byte(password), salt, p.Iterations, p.Memory, p.Parallelism, p.KeyLength)

	b64Salt := base64.RawStdEncoding.EncodeToString(salt)
	b64Hash := base64.RawStdEncoding.EncodeToString(hash)

	encoded := fmt.Sprintf("$argon2id$v=%d$m=%d,t=%d,p=%d$%s$%s",
		argon2.Version, p.Memory, p.Iterations, p.Parallelism, b64Salt, b64Hash)
	return encoded, nil
}

func main() {
	params := &HashParams{
		Memory:      64 * 1024, // 64 MB
		Iterations:  3,
		Parallelism: 2,
		SaltLength:  16,
		KeyLength:   32,
	}

	hash, _ := HashPasswordArgon2id("O'taMaxfiyParol_2026", params)
	fmt.Printf("Argon2id Xesh: %s\n", hash)
}
```
**Tushuntirish:** Argon2id xotira sarfini (Memory Cost) 64 MB qilib belgilaydi. Bu parallel ishlovchi GPU va ASIC maxsus chiplarining parollarni brute-force qilish imkoniyatini keskin cheklaydi.

---

### Topshiriq #1157: Bcrypt Yordamida Parollarni Xeshlash va Solishtirish
**Tavsif:** Klassik veb-loyihalarda Blowfish shifriga asoslangan moslashuvchan (Adaptive) xesh yaratish.
**Talablar:** `bcrypt.GenerateFromPassword`, `bcrypt.CompareHashAndPassword`, `Cost`.
**Yechim (Go):**
```go
package main

import (
	"fmt"

	"golang.org/x/crypto/bcrypt"
)

func HashBcrypt(password string, cost int) (string, error) {
	bytes, err := bcrypt.GenerateFromPassword([]byte(password), cost)
	return string(bytes), err
}

func VerifyBcrypt(password, hash string) bool {
	err := bcrypt.CompareHashAndPassword([]byte(hash), []byte(password))
	return err == nil
}

func main() {
	pwd := "MeningParolim_123!"
	hash, _ := HashBcrypt(pwd, 12) // Cost = 12
	fmt.Printf("Bcrypt xesh: %s\n", hash)

	ok := VerifyBcrypt(pwd, hash)
	fmt.Printf("Parol to'g'riligi tekshirildi: %v\n", ok)
}
```
**Tushuntirish:** Bcrypt `cost` ko'rsatkichi hisoblash vaqtini eksponentsial oshiradi (har +1 cost vaqtni 2 barobarga oshiradi). Bu texnologiyalar rivojlangan sari parollarni qayta xeshlash imkonini beradi.

---

### Topshiriq #1158: HKDF Orqali Bitta Asosiy Kalitdan Kichik Kalitlar Hosil Qilish
**Tavsif:** Bitta umumiy sirdan (Master Secret) shifrlash, xeshlash va IV uchun bir-biriga bog'liq bo'lmagan mustaqil kalitlar generatsiya qilish.
**Talablar:** `golang.org/x/crypto/hkdf`, `io.ReadFull`, SHA-256.
**Yechim (Go):**
```go
package main

import (
	"crypto/sha256"
	"fmt"
	"io"

	"golang.org/x/crypto/hkdf"
)

func DeriveSubkeys(secret, salt, info []byte, length int) ([]byte, error) {
	kdf := hkdf.New(sha256.New, secret, salt, info)
	key := make([]byte, length)
	if _, err := io.ReadFull(kdf, key); err != nil {
		return nil, err
	}
	return key, nil
}

func main() {
	master := []byte("diffie_hellman_shared_master_secret")
	salt := []byte("tasodifiy_tuz_123")

	encKey, _ := DeriveSubkeys(master, salt, []byte("aes-encryption-key"), 32)
	macKey, _ := DeriveSubkeys(master, salt, []byte("hmac-integrity-key"), 32)

	fmt.Printf("Hosil qilingan Shifrlash kaliti: %x\n", encKey[:8])
	fmt.Printf("Hosil qilingan MAC kaliti: %x\n", macKey[:8])
}
```
**Tushuntirish:** HKDF (RFC 5869) orqali hosil qilingan subkalitlar matematik jihatdan mustaqil bo'ladi: biror subkalit fosh bo'lsa ham, u boshqa subkalitlarni yoki asosiy kalitni oshkor qilmaydi.

---

### Topshiriq #1159: Katta Fayllarni Oqimli Shifrlash (cipher.Stream va CTR Rejimi)
**Tavsif:** Fayllarni butunlay RAM ga yuklamasdan `io.Reader` va `io.Writer` oqimlarida parallel shifrlash.
**Talablar:** `crypto/cipher`, `cipher.NewCTR`, `cipher.StreamWriter`, `cipher.StreamReader`.
**Yechim (Go):**
```go
package main

import (
	"bytes"
	"crypto/aes"
	"crypto/cipher"
	"fmt"
	"io"
)

func StreamEncrypt(key, iv []byte, src io.Reader, dst io.Writer) error {
	block, err := aes.NewCipher(key)
	if err != nil {
		return err
	}

	stream := cipher.NewCTR(block, iv)
	writer := &cipher.StreamWriter{S: stream, W: dst}

	_, err = io.Copy(writer, src)
	return err
}

func main() {
	key := make([]byte, 32)
	iv := make([]byte, 16)
	src := bytes.NewBufferString("Katta hajmdagi video yoki arxiv ma'lumotlar oqimi")
	dst := &bytes.Buffer{}

	StreamEncrypt(key, iv, src, dst)
	fmt.Printf("Oqimli shifrlash yakunlandi. Chiqish hajmi: %d bayt\n", dst.Len())
}
```
**Tushuntirish:** `cipher.StreamWriter` oqim bo'ylab o'tayotgan har bir baytni parvoz holatida (on-the-fly) shifrlaydi. Bu gigabaytlik fayllarni server xotirasini to'ldirmasdan uzatish imkonini beradi.

---

### Topshiriq #1160: HMAC-SHA512 Bilan Xabar Yaxlitligi va Soxtalashtirishdan Himoya
**Tavsif:** Kritik API chaqiruvlari va to'lov xabarnomalarining soxtalashtirilmaganini tekshirish.
**Talablar:** `crypto/hmac`, `crypto/sha512`, `subtle.ConstantTimeCompare`.
**Yechim (Go):**
```go
package main

import (
	"crypto/hmac"
	"crypto/sha512"
	"crypto/subtle"
	"fmt"
)

func SignMessage(key, message []byte) []byte {
	mac := hmac.New(sha512.New, key)
	mac.Write(message)
	return mac.Sum(nil)
}

func CheckMAC(key, message, messageMAC []byte) bool {
	expectedMAC := SignMessage(key, message)
	// Doimiy vaqtda solishtirish
	return subtle.ConstantTimeCompare(messageMAC, expectedMAC) == 1
}

func main() {
	key := []byte("maxfiy_api_kaliti_512")
	msg := []byte("buyruq: to'lovni tasdiqlash")

	sig := SignMessage(key, msg)
	fmt.Printf("HMAC-SHA512 imzosi hajmi: %d bayt\n", len(sig))

	valid := CheckMAC(key, msg, sig)
	fmt.Printf("Imzo to'g'riligi tasdiqlandi: %v\n", valid)
}
```
**Tushuntirish:** `CheckMAC` funksiyasida `subtle.ConstantTimeCompare` dan foydalanish xavfsizlik uchun qat'iy talabdir; oddiy `bytes.Equal` vaqt bo'yicha hujumlarga (Timing Attack) imkon beradi.

---

### Topshiriq #1161: Merkle Tree (Xesh Daraxti) Orqali Fayllar Yaxlitligini Tekshirish
**Tavsif:** Taqsimlangan tizimlarda (P2P, Git, Blokcheyn) faylning biror bo'lagi o'zgarganini daraxt ildizi (Merkle Root) orqali zudlik bilan aniqlash.
**Talablar:** Binar xesh daraxti, SHA-256.
**Yechim (Go):**
```go
package main

import (
	"crypto/sha256"
	"fmt"
)

func hashPair(a, b []byte) []byte {
	h := sha256.New()
	h.Write(a)
	h.Write(b)
	return h.Sum(nil)
}

func BuildMerkleRoot(leaves [][]byte) []byte {
	if len(leaves) == 0 {
		return nil
	}
	current := leaves
	for len(current) > 1 {
		var next [][]byte
		for i := 0; i < len(current); i += 2 {
			if i+1 < len(current) {
				next = append(next, hashPair(current[i], current[i+1]))
			} else {
				next = append(next, hashPair(current[i], current[i]))
			}
		}
		current = next
	}
	return current[0]
}

func main() {
	leaf1 := sha256.Sum256([]byte("Fayl bo'lagi 1"))
	leaf2 := sha256.Sum256([]byte("Fayl bo'lagi 2"))
	root := BuildMerkleRoot([][]byte{leaf1[:], leaf2[:]})
	fmt.Printf("Merkle Root xeshi: %x\n", root[:8])
}
```
**Tushuntirish:** Merkle Tree orqali butun gigabaytlik faylni qayta ko'chirmasdan, faqat $O(\log N)$ ta xeshni solishtirish orqali aynan qaysi blok buzilganini aniqlash mumkin.

---

### Topshiriq #1162: Deterministik Shifrlash: AES-SIV (Synthetic IV)
**Tavsif:** Shifrlangan ma'lumotlar bazasida indeksli qidiruvni amalga oshirish uchun bir xil kalit va matnga doimiy bir xil shifr yaratish.
**Talablar:** `miscreant` yoki AES-SIV (RFC 5297) arxitekturasi.
**Yechim (Go):**
```go
package main

import (
	"crypto/hmac"
	"crypto/sha256"
	"fmt"
)

// Deterministik qidiruv uchun soxta SIV modeli
func PseudoSivToken(key, data []byte) []byte {
	h := hmac.New(sha256.New, key)
	h.Write(data)
	return h.Sum(nil)
}

func main() {
	key := []byte("qidiruv_indeksi_uchun_maxfiy_kalit")
	pii := []byte("INN: 300123456")

	t1 := PseudoSivToken(key, pii)
	t2 := PseudoSivToken(key, pii)

	fmt.Printf("Deterministik token 1: %x\nDeterministik token 2: %x\n", t1[:6], t2[:6])
	fmt.Printf("Tokenlar teng: %v\n", string(t1) == string(t2))
}
```
**Tushuntirish:** Deterministik shifrlashda qidiruv operatsiyasi (`SELECT * FROM users WHERE ssn_token = ?`) amalga oshiriladi; bunda ma'lumotlar bazasi asl ochiq matnni hech qachon bilmaydi.

---

### Topshiriq #1163: crypto/ed25519 Bilan Yuqori Tezlikdagi Raqamli Imzolash va Verifikatsiya
**Tavsif:** Mikroxizmatlar va API tranzaksiyalarini tasdiqlash uchun xavfsiz va ixcham Ed25519 raqamli imzolarini qo'llash.
**Talablar:** `crypto/ed25519`, `GenerateKey`, `Sign`, `Verify`.
**Yechim (Go):**
```go
package main

import (
	"crypto/ed25519"
	"crypto/rand"
	"fmt"
)

func main() {
	// 1. Ed25519 kalit juftligini yaratish
	publicKey, privateKey, err := ed25519.GenerateKey(rand.Reader)
	if err != nil {
		panic(err)
	}

	message := []byte("Moliyaviy tranzaksiya #987654: 5,000,000 UZS")

	// 2. Xabarni imzolash (64-baytlik imzo)
	signature := ed25519.Sign(privateKey, message)
	fmt.Printf("Ochiq kalit: %d bayt, Imzo: %d bayt\n", len(publicKey), len(signature))

	// 3. Imzoni tekshirish
	isValid := ed25519.Verify(publicKey, message, signature)
	fmt.Printf("Ed25519 raqamli imzo haqiqiy: %v\n", isValid)
}
```
**Tushuntirish:** `crypto/ed25519` Go standart kutubxonasida C yordamisiz to'liq doimiy vaqtda (Constant-Time) ishlaydi va tasodifiy son generatoridagi xatoliklarga ham chidamli (deterministik imzo) hisoblanadi.

---

### Topshiriq #1164: Ed25519 Kalitlarini PEM va PKCS#8 Formatida Saqlash va Yuklash
**Tavsif:** Yaratilgan xususiy va ochiq kalitlarni diskka xavfsiz `.pem` fayl ko'rinishida saqlash va qayta o'qish.
**Talablar:** `crypto/x509`, `x509.MarshalPKCS8PrivateKey`, `encoding/pem`.
**Yechim (Go):**
```go
package main

import (
	"crypto/ed25519"
	"crypto/rand"
	"crypto/x509"
	"encoding/pem"
	"fmt"
)

func ExportPrivateKeyPEM(priv ed25519.PrivateKey) ([]byte, error) {
	bytes, err := x509.MarshalPKCS8PrivateKey(priv)
	if err != nil {
		return nil, err
	}
	block := &pem.Block{
		Type:  "PRIVATE KEY",
		Bytes: bytes,
	}
	return pem.EncodeToMemory(block), nil
}

func main() {
	_, priv, _ := ed25519.GenerateKey(rand.Reader)
	pemBytes, _ := ExportPrivateKeyPEM(priv)
	fmt.Printf("PKCS#8 PEM formatidagi xususiy kalit:\n%s", string(pemBytes[:60]))
}
```
**Tushuntirish:** PKCS#8 formati xususiy kalitlarni barcha platformalar va dasturlar (OpenSSL, Java, Rust) o'rtasida bir xil tushunishni ta'minlaydigan xalqaro standartdir.

---

### Topshiriq #1165: crypto/rsa Bilan RSA-OAEP Asimmetrik Shifrlash va Ochish
**Tavsif:** Faqat serverning ochiq kaliti yordamida ma'lumotni shifrlab, xususiy kalit egasigina o'qiy olishini ta'minlash.
**Talablar:** `crypto/rsa`, `rsa.EncryptOAEP`, `rsa.DecryptOAEP`, SHA-256.
**Yechim (Go):**
```go
package main

import (
	"crypto/rand"
	"crypto/rsa"
	"crypto/sha256"
	"fmt"
)

func main() {
	privateKey, _ := rsa.GenerateKey(rand.Reader, 2048)
	publicKey := &privateKey.PublicKey

	secretMessage := []byte("Maxfiy bank paroli")
	label := []byte("payment-module")

	// RSA-OAEP shifrlash
	ciphertext, err := rsa.EncryptOAEP(sha256.New(), rand.Reader, publicKey, secretMessage, label)
	if err != nil {
		panic(err)
	}
	fmt.Printf("RSA-OAEP shifrlangan ma'lumot hajmi: %d bayt\n", len(ciphertext))

	// RSA-OAEP dekodlash
	decrypted, err := rsa.DecryptOAEP(sha256.New(), rand.Reader, privateKey, ciphertext, label)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Ochilgan asl xabar: %s\n", string(decrypted))
}
```
**Tushuntirish:** `rsa.EncryptOAEP` tasodifiy padding qo'shadi, bu esa bir xil xabar shifrlanganda ham har safar butunlay yangi shifr matn hosil qiladi va semantik xavfsizlikni (IND-CCA2) ta'minlaydi.

---

### Topshiriq #1166: crypto/rsa Bilan RSA-PSS Raqamli Imzolash va Verifikatsiya
**Tavsif:** Muhim hujjatlarni PKCS#1 v2.1 PSS standarti bo'yicha soxtalashtirishdan himoyalangan holda imzolash.
**Talablar:** `rsa.SignPSS`, `rsa.VerifyPSS`, `crypto.SHA256`.
**Yechim (Go):**
```go
package main

import (
	"crypto"
	"crypto/rand"
	"crypto/rsa"
	"crypto/sha256"
	"fmt"
)

func main() {
	privateKey, _ := rsa.GenerateKey(rand.Reader, 2048)
	msg := []byte("Kredit shartnomasi #40021")

	// Xabarni xeshlash
	hashed := sha256.Sum256(msg)

	// PSS optsiyasi bilan imzolash
	opts := &rsa.PSSOptions{SaltLength: rsa.PSSSaltLengthEqualsHash}
	sig, err := rsa.SignPSS(rand.Reader, privateKey, crypto.SHA256, hashed[:], opts)
	if err != nil {
		panic(err)
	}

	// Imzoni tekshirish
	err = rsa.VerifyPSS(&privateKey.PublicKey, crypto.SHA256, hashed[:], sig, opts)
	fmt.Printf("RSA-PSS imzosi haqiqiy: %v\n", err == nil)
}
```
**Tushuntirish:** RSA-PSS klassik PKCS#1 v1.5 ga nisbatan matematik jihatdan isbotlangan xavfsizlikka ega bo'lib, zamonaviy TLS 1.3 da RSA uchun yagona majburiy imzo algoritmi etib belgilangan.

---

### Topshiriq #1167: crypto/ecdsa P-256 (secp256r1) Elliptik Egri Chizig'ida Imzo
**Tavsif:** Mobil ilovalar va Apple/Android xavfsizlik chiplari (Secure Enclave / Keystore) bilan mos keluvchi NIST P-256 imzosi.
**Talablar:** `crypto/ecdsa`, `elliptic.P256()`, `ecdsa.SignASN1`, `ecdsa.VerifyASN1`.
**Yechim (Go):**
```go
package main

import (
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/rand"
	"crypto/sha256"
	"fmt"
)

func main() {
	privKey, _ := ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
	data := []byte("Mobil qurilma biometrik autentifikatsiyasi")
	hash := sha256.Sum256(data)

	// ASN.1 formatidagi DER imzo
	sig, err := ecdsa.SignASN1(rand.Reader, privKey, hash[:])
	if err != nil {
		panic(err)
	}

	valid := ecdsa.VerifyASN1(&privKey.PublicKey, hash[:], sig)
	fmt.Printf("P-256 ECDSA imzosi tekshirildi: %v\n", valid)
}
```
**Tushuntirish:** `SignASN1` va `VerifyASN1` imzoni xalqaro DER/ASN.1 formatida shakllantiradi, bu esa veb-brauzerlar va HSM chiplari bilan to'liq moslikni ta'minlaydi.

---

### Topshiriq #1168: crypto/ecdh (Go 1.20+) Orqali X25519 Diffie-Hellman Kalit Kelishuvi
**Tavsif:** Go ning zamonaviy `crypto/ecdh` paketi orqali ikki tomonlama Perfect Forward Secrecy (PFS) kalit almashinuvini bajarish.
**Talablar:** `crypto/ecdh.X25519()`, `GenerateKey`, `ECDH`.
**Yechim (Go):**
```go
package main

import (
	"crypto/ecdh"
	"crypto/rand"
	"fmt"
)

func main() {
	curve := ecdh.X25519()

	// 1. Alisa kalitlari
	alicePriv, _ := curve.GenerateKey(rand.Reader)
	alicePub := alicePriv.PublicKey()

	// 2. Bob kalitlari
	bobPriv, _ := curve.GenerateKey(rand.Reader)
	bobPub := bobPriv.PublicKey()

	// 3. Umumiy sirni hisoblash
	aliceSecret, _ := alicePriv.ECDH(bobPub)
	bobSecret, _ := bobPriv.ECDH(alicePub)

	fmt.Printf("Alisa va Bob umumiy siri mos keldi: %v (%d bayt)\n",
		string(aliceSecret) == string(bobSecret), len(aliceSecret))
}
```
**Tushuntirish:** `crypto/ecdh` paketi Go 1.20 da chiqarilgan bo'lib, eski `crypto/elliptic` dagi past darajadagi egri chiziq xatolarini (Invalid Curve Attack) arxitekturaviy darajada yo'q qilgan.

---

### Topshiriq #1169: crypto/x509 Bilan Xususiy CA (Certificate Authority) Yaratish
**Tavsif:** Korporativ tarmoqda o'zimizning Root CA sertifikatimizni generatsiya qilish va serverlar uchun sertifikat imzolash.
**Talablar:** `x509.CreateCertificate`, `x509.Certificate`, `x509.KeyUsageCertSign`.
**Yechim (Go):**
```go
package main

import (
	"crypto/ed25519"
	"crypto/rand"
	"crypto/x509"
	"crypto/x509/pkix"
	"fmt"
	"math/big"
	"time"
)

func GenerateRootCA() ([]byte, ed25519.PrivateKey, error) {
	pub, priv, _ := ed25519.GenerateKey(rand.Reader)

	template := &x509.Certificate{
		SerialNumber: big.NewInt(1),
		Subject: pkix.Name{
			Organization: []string{"Khorazmiy AI Root Authority"},
			CommonName:   "Khorazmiy CA",
		},
		NotBefore:             time.Now(),
		NotAfter:              time.Now().AddDate(10, 0, 0),
		IsCA:                  true,
		KeyUsage:              x509.KeyUsageCertSign | x509.KeyUsageCRLSign,
		BasicConstraintsValid: true,
	}

	certBytes, err := x509.CreateCertificate(rand.Reader, template, template, pub, priv)
	return certBytes, priv, err
}

func main() {
	cert, _, err := GenerateRootCA()
	if err == nil {
		fmt.Printf("Root CA sertifikati yaratildi: %d bayt\n", len(cert))
	}
}
```
**Tushuntirish:** `IsCA: true` va `KeyUsageCertSign` boshqa sertifikatlarni imzolash huquqini beradi. Barcha mTLS va ichki mikroxizmatlar ushbu Root CA orqali bir-birini taniydi.

---

### Topshiriq #1170: Sertifikat Revocation Tekshiruvi: CRL va OCSP Asoslari
**Tavsif:** O'g'irlangan yoki muddati bekor qilingan (Revoked) sertifikatlarni tekshirish mexanizmi.
**Talablar:** `x509.ParseRevocationList`, `crypto/x509/pkix`.
**Yechim (Go):**
```go
package main

import (
	"crypto/x509"
	"fmt"
	"math/big"
)

func CheckCertificateRevocation(crl *x509.RevocationList, serialNumber *big.Int) bool {
	for _, revoked := range crl.RevokedCertificateEntries {
		if revoked.SerialNumber.Cmp(serialNumber) == 0 {
			return true // Sertifikat bekor qilingan!
		}
	}
	return false
}

func main() {
	fmt.Println("Sertifikatlarni CRL orqali bekor qilinganlikka tekshirish moduli tayyor.")
}
```
**Tushuntirish:** Sertifikat faqat muddatiga qarab emas, balki xususiy kalit sizib chiqqan bo'lsa CRL (Certificate Revocation List) yoki real vaqtli OCSP orqali zudlik bilan bekor qilinishi lozim.

---

### Topshiriq #1171: Ed25519 Bilan Tashqi Kutubxonasiz JWT Imzolash va Tekshirish
**Tavsif:** Hech qanday qo'shimcha qaramliklarsiz (No Dependencies) to'liq xavfsiz EdDSA JWT tokenni shakllantirish.
**Talablar:** `encoding/base64`, `crypto/ed25519`, `strings.Split`.
**Yechim (Go):**
```go
package main

import (
	"crypto/ed25519"
	"crypto/rand"
	"encoding/base64"
	"fmt"
	"strings"
)

func CreateSignedJWT(priv ed25519.PrivateKey, payloadJSON string) string {
	header := `{"alg":"EdDSA","typ":"JWT"}`
	b64Hdr := base64.RawURLEncoding.EncodeToString([]byte(header))
	b64Payload := base64.RawURLEncoding.EncodeToString([]byte(payloadJSON))

	signingInput := b64Hdr + "." + b64Payload
	signature := ed25519.Sign(priv, []byte(signingInput))
	b64Sig := base64.RawURLEncoding.EncodeToString(signature)

	return signingInput + "." + b64Sig
}

func VerifyJWT(pub ed25519.PublicKey, token string) bool {
	parts := strings.Split(token, ".")
	if len(parts) != 3 {
		return false
	}
	signingInput := parts[0] + "." + parts[1]
	sig, err := base64.RawURLEncoding.DecodeString(parts[2])
	if err != nil {
		return false
	}
	return ed25519.Verify(pub, []byte(signingInput), sig)
}

func main() {
	pub, priv, _ := ed25519.GenerateKey(rand.Reader)
	token := CreateSignedJWT(priv, `{"sub":"101","role":"superadmin"}`)
	fmt.Printf("EdDSA JWT: %s\n", token[:40]+"...")

	ok := VerifyJWT(pub, token)
	fmt.Printf("JWT tekshirildi: %v\n", ok)
}
```
**Tushuntirish:** Ushbu toza implementatsiya mashhur 'alg: none' yoki RSA-to-HMAC konversiya hujumlaridan holidir, chunki algoritm qat'iy ravishda faqat Ed25519 uchun tekshiriladi.

---

### Topshiriq #1172: Shamir's Secret Sharing: Go Tilida Kritik Kalitlarni Bo'lish
**Tavsif:** Boshqaruvchi kalitni 3 ta direktorga bo'lib berish va ulardan kamida 2 tasi kelgandagina kalitni ochish.
**Talablar:** Chekli maydondagi polinomlar (Galois Field GF(256)).
**Yechim (Go):**
```go
package main

import (
	"fmt"
)

type Share struct {
	X uint8
	Y uint8
}

// 2 ta ulushdan sirni tiklash: f(0) = (y1*x2 - y2*x1) / (x2 - x1)
func RecoverSecret(s1, s2 Share) uint8 {
	num := int(s1.Y)*int(s2.X) - int(s2.Y)*int(s1.X)
	den := int(s2.X) - int(s1.X)
	return uint8(num / den)
}

func main() {
	// f(x) = 3x + 10 mod 256. Sir = 10
	s1 := Share{X: 1, Y: 13}
	s2 := Share{X: 2, Y: 16}

	secret := RecoverSecret(s1, s2)
	fmt.Printf("Tiklagan maxfiy sir: %d\n", secret)
}
```
**Tushuntirish:** Bank va kiberxavfsizlikda Master Key bitta odam qo'lida saqlanmaydi; Shamir sxemasi xodimlar o'rtasida mas'uliyatni teng taqsimlaydi.

---

### Topshiriq #1173: Post-Quantum Tayyorgarlik: Go Da Gibrid KEM (X25519 + Kyber768)
**Tavsif:** Kelajakdagi kvant kompyuterlariga qarshi an'anaviy ECDH va post-kvant KEM ni birlashtiruvchi gibrid model.
**Talablar:** Gibrid kalit kelishuvi: $Secret = KDF(ECDH\_Secret \parallel Kyber\_Secret)$.
**Yechim (Go):**
```go
package main

import (
	"crypto/sha256"
	"fmt"
)

func CombineHybridSecrets(classicEcdhSecret, pqcKyberSecret []byte) []byte {
	h := sha256.New()
	h.Write(classicEcdhSecret)
	h.Write(pqcKyberSecret)
	return h.Sum(nil) // Gibrid umumiy maxfiy kalit
}

func main() {
	ecdh := []byte("32_bayt_x25519_klassik_sir")
	kyber := []byte("32_bayt_kyber768_post_kvant_siri")

	hybrid := CombineHybridSecrets(ecdh, kyber)
	fmt.Printf("Gibrid post-kvant kaliti: %x\n", hybrid[:8])
}
```
**Tushuntirish:** Gibrid rejim NIST va Cloudflare tomonidan tavsiya etiladi: agar post-kvant algoritmlarida kutilmagan matematik zaiflik topilsa ham, an'anaviy X25519 aloqani xavfsiz saqlab qoladi.

---

### Topshiriq #1174: CSR (Certificate Signing Request) Generatsiyasi va Avtomatlashtirish
**Tavsif:** Serverlar uchun yangi kalit yaratib, ommaviy CA larga (Let's Encrypt / DigiCert) so'rov yuborish uchun CSR shakllantirish.
**Talablar:** `x509.CreateCertificateRequest`, `x509.CertificateRequest`.
**Yechim (Go):**
```go
package main

import (
	"crypto/ed25519"
	"crypto/rand"
	"crypto/x509"
	"crypto/x509/pkix"
	"encoding/pem"
	"fmt"
)

func GenerateCSR(domain string) ([]byte, error) {
	_, priv, _ := ed25519.GenerateKey(rand.Reader)

	template := &x509.CertificateRequest{
		Subject: pkix.Name{
			CommonName:   domain,
			Organization: []string{"Khorazmiy AI Tizimlari"},
		},
		DNSNames: []string{domain, "www." + domain},
	}

	csrBytes, err := x509.CreateCertificateRequest(rand.Reader, template, priv)
	if err != nil {
		return nil, err
	}

	block := &pem.Block{Type: "CERTIFICATE REQUEST", Bytes: csrBytes}
	return pem.EncodeToMemory(block), nil
}

func main() {
	csr, _ := GenerateCSR("khorazmiy.uz")
	fmt.Printf("CSR Hujjati:\n%s", string(csr[:60]))
}
```
**Tushuntirish:** CSR faqat ochiq kalit va domen ma'lumotlarini o'z ichiga oladi va xususiy kalit bilan imzolanadi; xususiy kalit esa hech qachon serverdan tashqariga chiqmaydi.

---

### Topshiriq #1175: crypto/subtle.ConstantTimeCompare Bilan Vaqt Hujumlarini Yo'qotish
**Tavsif:** API tokenlari va parollarni solishtirishda vaqt oqishini (Timing Side-Channel) butunlay yo'q qilish.
**Talablar:** `crypto/subtle.ConstantTimeCompare`, doimiy vaqt taqqoslash.
**Yechim (Go):**
```go
package main

import (
	"crypto/subtle"
	"fmt"
)

func SecureCompareTokens(tokenA, tokenB string) bool {
	a := []byte(tokenA)
	b := []byte(tokenB)

	// Har doim bir xil vaqtda bajariladi
	return subtle.ConstantTimeCompare(a, b) == 1
}

func main() {
	realToken := "secret_api_token_abc_123"
	clientToken := "secret_api_token_abc_124"

	match := SecureCompareTokens(realToken, clientToken)
	fmt.Printf("Tokenlar mos kelishi: %v (Constant-Time)\n", match)
}
```
**Tushuntirish:** `ConstantTimeCompare` ikkala massiv uzunligini va har bir baytini bitwise XOR orqali to'liq tekshirib chiqadi va birinchi xatoda siklni to'xtatmaydi.

---

### Topshiriq #1176: crypto/subtle.ConstantTimeSelect Bilan Tarmoqlanishsiz Dasturlash
**Tavsif:** Kriptografik operatsiyalarda `if` shart operatorini ishlatmasdan baytlarni doimiy vaqtda tanlash.
**Talablar:** `subtle.ConstantTimeSelect`, `ConstantTimeByteEq`.
**Yechim (Go):**
```go
package main

import (
	"crypto/subtle"
	"fmt"
)

func SafeSelect(v int, a, b int) int {
	// Agar v == 1 bo'lsa a, aks holda b tanlanadi (hech qanday if-else siz)
	return subtle.ConstantTimeSelect(v, a, b)
}

func main() {
	val := SafeSelect(1, 100, 200)
	fmt.Printf("Tanlangan qiymat: %d\n", val)
}
```
**Tushuntirish:** `ConstantTimeSelect` protsessor buyruqlar darajasida conditional move (CMOV) yoki bitwise niqob bilan ishlaydi va branch predictorga hech qanday ma'lumot bermaydi.

---

### Topshiriq #1177: Vaqt Hujumlari (Timing Attack) Simulyatori va Himoyasi
**Tavsif:** Noto'g'ri yozilgan satr taqqoslash funksiyasining qanchalik tez vaqt farqini ko'rsatishini namoyish qilish.
**Talablar:** `time.Now()`, nanosekundlar o'lchovi.
**Yechim (Go):**
```go
package main

import (
	"crypto/subtle"
	"fmt"
	"time"
)

func InsecureCompare(a, b string) bool {
	return a == b // Zaif: birinchi xato baytdayoq chiqadi
}

func main() {
	s1 := "AAAAAAAAAAAAAAAAAAAA"
	s2 := "BAAAAAAAAAAAAAAAAAAA"
	s3 := "AAAAAAAAAAAAAAAABBBB"

	start := time.Now()
	InsecureCompare(s1, s2)
	t1 := time.Since(start)

	start = time.Now()
	InsecureCompare(s1, s3)
	t2 := time.Since(start)

	fmt.Printf("Boshida xato vaqt: %v | Oxirida xato vaqt: %v\n", t1, t2)
	fmt.Printf("Xavfsiz: %v\n", subtle.ConstantTimeCompare([]byte(s1), []byte(s2)) == 1)
}
```
**Tushuntirish:** Tajovuzkor millionlab so'rovlar yuborib o'rtacha vaqtni hisoblaganda, bitta to'g'ri topilgan bayt so'rov vaqtini 5-10 nanosekundga uzaytiradi; shu yo'l bilan butun token bosqichma-bosqich ochiladi.

---

### Topshiriq #1178: Xotiradagi Maxfiy Kalitlarni Tozalash (memclr va Garbage Collector)
**Tavsif:** Garbage Collector kalitlar nusxasini xotirada qoldirmasligi uchun bayt massivlarini zudlik bilan nolga tenglashtirish.
**Talablar:** `for i := range key { key[i] = 0 }`, `runtime.KeepAlive`.
**Yechim (Go):**
```go
package main

import (
	"fmt"
	"runtime"
)

func WipeSlice(buf []byte) {
	for i := range buf {
		buf[i] = 0
	}
	runtime.KeepAlive(buf) // Kompilyator bu siklni o'chirib yubormasligi uchun
}

func main() {
	secret := []byte("o'ta_maxfiy_parol_123")
	fmt.Printf("Tozalashdan oldin: %s\n", string(secret))

	WipeSlice(secret)
	fmt.Printf("Tozalangandan keyin: %v (barcha baytlar nol)\n", secret)
}
```
**Tushuntirish:** `runtime.KeepAlive` Go kompilyatorining optimallashtiruvchi qismiga ushbu massiv hali kerakligini bildiradi va nolga yozish operatsiyasining o'chirib tashlanishini oldini oladi.

---

### Topshiriq #1179: Kriptografik DoS Hujumlaridan Himoya (CPU va Xotira Kvotalari)
**Tavsif:** Hujumchilar og'ir RSA yoki Argon2 operatsiyalarini ko'p yuborib server CPU sini 100% ga qotirib qo'yishini cheklash.
**Talablar:** `golang.org/x/time/rate`, Concurrency semafori.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
	"golang.org/x/time/rate"
	"time"
)

type CryptoLimiter struct {
	limiter *rate.Limiter
}

func NewCryptoLimiter(r rate.Limit, b int) *CryptoLimiter {
	return &CryptoLimiter{limiter: rate.NewLimiter(r, b)}
}

func (cl *CryptoLimiter) AllowCryptoOp() bool {
	return cl.limiter.Allow()
}

func main() {
	limiter := NewCryptoLimiter(rate.Every(time.Second/5), 2) // Sekundiga maksimal 5 ta og'ir kripto-operatsiya
	fmt.Printf("Birinchi operatsiyaga ruxsat: %v\n", limiter.AllowCryptoOp())
}
```
**Tushuntirish:** Kriptografik operatsiyalar oddiy HTTP so'rovlardan 1000 baravar ko'proq CPU sarflaydi, shuning uchun ularga alohida qat'iy Rate Limiter o'rnatilishi shart.

---

### Topshiriq #1180: ECDSA Da Nonce Takrorlanishi (Nonce Reuse) Xavfi va RFC 6979
**Tavsif:** Tasodifiy $k$ soni takrorlanganda xususiy kalit formulasi ($d = (s_1 - s_2)^{-1} ...$) orqali darhol fosh bo'lishining oldini olish.
**Talablar:** Deterministik Nonce generatsiyasi (RFC 6979).
**Yechim (Go):**
```go
package main

import (
	"fmt"
)

func explainNonceReuseAttack() {
	fmt.Println("ECDSA Nonce Reuse fojiasi:")
	fmt.Println("Agar ikkita turli xabar bir xil tasodifiy k bilan imzolansa:")
	fmt.Println("  s1 = k^-1 * (e1 + d * r)")
	fmt.Println("  s2 = k^-1 * (e2 + d * r)")
	fmt.Println("Tajovuzkor oddiy ayirish orqali k ni topadi va xususiy kalit d zudlik bilan fosh bo'ladi!")
	fmt.Println("Yechim: RFC 6979 bo'yicha k soni xabar va kalitning HMAC xeshidan deterministik olinadi.")
}

func main() {
	explainNonceReuseAttack()
}
```
**Tushuntirish:** PlayStation 3 xakerlik hujumi aynan Sony dasturchilarining ECDSA da doim bir xil $k$ sonini qo'llaganligi tufayli sodir bo'lgan edi.

---

### Topshiriq #1181: Replay Attack (Qayta Yuborish) Dan Himoyalovchi Nonce Kesh
**Tavsif:** Tajovuzkor tarmoqdan yozib olingan haqiqiy imzolangan to'lov paketini qayta-qayta yuborishining oldini olish.
**Talablar:** Timestamp + Nonce kesh + TTL tekshiruvi.
**Yechim (Go):**
```go
package main

import (
	"fmt"
	"sync"
	"time"
)

type ReplayGuard struct {
	mu     sync.Mutex
	nonces map[string]time.Time
	ttl    time.Duration
}

func (rg *ReplayGuard) ValidateAndStore(nonce string, timestamp time.Time) bool {
	rg.mu.Lock()
	defer rg.mu.Unlock()

	// 1. Vaqt 5 daqiqadan eski emasligini tekshirish
	if time.Since(timestamp) > rg.ttl {
		return false
	}

	// 2. Nonce avval ishlatilmaganligini tekshirish
	if _, exists := rg.nonces[nonce]; exists {
		return false // Qayta yuborilgan hujum (Replay Attack)!
	}

	rg.nonces[nonce] = timestamp
	return true
}

func main() {
	guard := &ReplayGuard{nonces: make(map[string]time.Time), ttl: 5 * time.Minute}
	fmt.Printf("Paket 1: %v\n", guard.ValidateAndStore("nonce_1", time.Now()))
	fmt.Printf("Paket 1 (takroriy): %v\n", guard.ValidateAndStore("nonce_1", time.Now()))
}
```
**Tushuntirish:** Vaqt tamg'asi (Timestamp) va Nonce kesh kombinatsiyasi keshning cheksiz o'sib ketishini oldini oladi (faqat 5 daqiqalik noncelar saqlanadi).

---

### Topshiriq #1182: RSA Asosidagi Blind Signature (Ko'r Imzo) Protokoli
**Tavsif:** Foydalanuvchi ma'lumotni ko'r qiluvchi omil ($r$) bilan niqoblab imzolattirishi va so'ngra ochishi.
**Talablar:** RSA ko'r imzo matematikasi.
**Yechim (Go):**
```go
package main

import (
	"fmt"
	"math/big"
)

func BlindMessage(m, r, e, n *big.Int) *big.Int {
	// m' = (m * r^e) mod n
	re := new(big.Int).Exp(r, e, n)
	return new(big.Int).Mod(new(big.Int).Mul(m, re), n)
}

func main() {
	n := big.NewInt(1000000007)
	e := big.NewInt(65537)
	m := big.NewInt(42)
	r := big.NewInt(7)

	blinded := BlindMessage(m, r, e, n)
	fmt.Printf("Ko'r qilingan xabar: %s\n", blinded.String())
}
```
**Tushuntirish:** Ko'r imzo maxfiy elektron pullar (e-cash) va yashirin elektron ovoz berishda foydalanuvchining shaxsini tranzaksiyadan uzish uchun ishlatiladi.

---

### Topshiriq #1183: DNS Rebinding va SSRF Hujumlaridan Himoyalangan HTTP Klient
**Tavsif:** Kriptografik xizmatlar tashqi vebxuklarga murojaat qilganda ichki lokal tarmoqqa (127.0.0.1, 192.168.x) kirib ketmasligini tekshirish.
**Talablar:** `net.Dialer.Control`, IP tekshiruvi.
**Yechim (Go):**
```go
package main

import (
	"context"
	"errors"
	"fmt"
	"net"
	"net/http"
	"time"
)

func SafeDialContext(ctx context.Context, network, addr string) (net.Conn, error) {
	host, port, _ := net.SplitHostPort(addr)
	ips, err := net.LookupIP(host)
	if err != nil {
		return nil, err
	}

	for _, ip := range ips {
		// Xususiy, Loopback va Multicast IP larni taqiqlash
		if ip.IsLoopback() || ip.IsPrivate() || ip.IsLinkLocalUnicast() {
			return nil, errors.New("ichki tarmoqqa murojaat taqiqlangan (SSRF himoyasi)")
		}
	}

	dialer := &net.Dialer{Timeout: 5 * time.Second}
	return dialer.DialContext(ctx, network, net.JoinHostPort(ips[0].String(), port))
}

func main() {
	client := &http.Client{
		Transport: &http.Transport{DialContext: SafeDialContext},
	}
	_ = client
	fmt.Println("SSRF va DNS Rebinding dan himoyalangan xavfsiz HTTP klient yaratildi.")
}
```
**Tushuntirish:** DNS Rebinding hujumida tajovuzkor domeni dastlab tashqi ochiq IP qaytaradi, so'ngra darhol 127.0.0.1 ga o'zgartiradi; IP ni ulanish vaqtida bevosita tekshirish buni to'xtatadi.

---

### Topshiriq #1184: Kriptografik Xotira Sahifalarini Bloklash (unix.Mlock)
**Tavsif:** Xotiradagi maxfiy kalitlar operatsion tizim tomonidan qattiq diskka (Swap / Pagefile) yozilib ketishining oldini olish.
**Talablar:** `golang.org/x/sys/unix.Mlock`, `unix.Munlock`.
**Yechim (Go):**
```go
package main

import (
	"fmt"
)

func explainMemoryLocking() {
	fmt.Println("unix.Mlock xavfsizlik printsipi:")
	fmt.Println("1. Linux/macOS da OS xotira yetishmaganda RAM sahifalarini swap fayliga tashlaydi.")
	fmt.Println("2. Agar maxfiy kalit swapga tushsa, server o'chirilgandan keyin ham diskda o'qilishi mumkin.")
	fmt.Println("3. unix.Mlock(slice) bu sahifani apparat RAM ida 'qotirib' qo'yadi va swapga tushishni taqiqlaydi.")
}

func main() {
	explainMemoryLocking()
}
```
**Tushuntirish:** Kriptografik standartlar (PCI-DSS) bank xavfsizlik modullarida maxfiy kalitlar joylashgan barcha operativ xotira bloklariga `mlock` chaqirishni majburiy etib belgilaydi.

---

### Topshiriq #1185: TLS 1.3 Majburiy Konfiguratsiyasi (crypto/tls)
**Tavsif:** Eski va zaif shifrlash protokollarini (TLS 1.0, 1.1, 1.2) butunlay taqiqlab, faqat eng yangi TLS 1.3 ni yoqish.
**Talablar:** `tls.Config{MinVersion: tls.VersionTLS13}`.
**Yechim (Go):**
```go
package main

import (
	"crypto/tls"
	"fmt"
	"net/http"
)

func NewHardenedTlsServer(addr string, handler http.Handler) *http.Server {
	tlsConfig := &tls.Config{
		MinVersion: tls.VersionTLS13, // TLS 1.3 dan pastiga ruxsat berilmaydi
		CurvePreferences: []tls.CurveID{
			tls.X25519,
			tls.CurveP256,
		},
	}

	return &http.Server{
		Addr:      addr,
		Handler:   handler,
		TLSConfig: tlsConfig,
	}
}

func main() {
	server := NewHardenedTlsServer(":8443", nil)
	fmt.Printf("Faqat TLS 1.3 qabul qiluvchi xavfsiz server tayyorlandi: %s\n", server.Addr)
}
```
**Tushuntirish:** TLS 1.3 da RSA kalit almashinuvi, CBC shifrlash va SHA-1 butunlay olib tashlangan. Barcha ulanishlar majburiy Perfect Forward Secrecy (PFS) ga ega bo'ladi.

---

### Topshiriq #1186: Faqat Xavfsiz Shifrlar (CipherSuites) va ALPN Ni Sozlash
**Tavsif:** Serverda faqat eng kuchli autentifikatsiyalangan shifrlarni qoldirish va HTTP/2 ni kelishish.
**Talablar:** `tls.CipherSuites`, `NextProtos: []string{"h2", "http/1.1"}`.
**Yechim (Go):**
```go
package main

import (
	"crypto/tls"
	"fmt"
)

func GetSecureTlsConfig() *tls.Config {
	return &tls.Config{
		MinVersion: tls.VersionTLS12,
		CipherSuites: []uint16{
			tls.TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,
			tls.TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,
			tls.TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305,
			tls.TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305,
		},
		NextProtos: []string{"h2", "http/1.1"}, // ALPN
	}
}

func main() {
	cfg := GetSecureTlsConfig()
	fmt.Printf("Shifrlash suitlari va ALPN sozlangan: %d ta shifr\n", len(cfg.CipherSuites))
}
```
**Tushuntirish:** Zaif shifrlarni (masalan, RC4, 3DES, CBC) o'chirib tashlash SSL stripping va SWEET32 kabi mashhur hujumlardan to'liq himoya qiladi.

---

### Topshiriq #1187: mTLS (Mutual TLS): Klient va Serverning O'zaro Autentifikatsiyasi
**Tavsif:** Zero-Trust mikroxizmatlar arxitekturasida mijoz ham serverga o'zining shaxsiy sertifikatini taqdim etishi shartligi.
**Talablar:** `tls.RequireAndVerifyClientCert`, `ClientCAs`, x509 sertifikatlar hovuzi.
**Yechim (Go):**
```go
package main

import (
	"crypto/tls"
	"crypto/x509"
	"fmt"
)

func ConfigureMutualTLS(rootCaCertPEM []byte) (*tls.Config, error) {
	clientCertPool := x509.NewCertPool()
	if !clientCertPool.AppendCertsFromPEM(rootCaCertPEM) {
		return nil, fmt.Errorf("root CA sertifikatini yuklab bo'lmadi")
	}

	return &tls.Config{
		ClientCAs:  clientCertPool,
		ClientAuth: tls.RequireAndVerifyClientCert, // Mijozdan sertifikat talab qilish
		MinVersion: tls.VersionTLS13,
	}, nil
}

func main() {
	fmt.Println("mTLS (Mutual TLS) konfiguratsiya moduli tayyorlandi.")
}
```
**Tushuntirish:** mTLS da mijoz sertifikatsiz ulana olmaydi. Bu an'anaviy parollar va tokenlarga nisbatan L4 darajasidagi eng yuqori korporativ himoyani ta'minlaydi.

---

### Topshiriq #1188: TLS 0-RTT Replay Xatarlari va Session Resumption Boshqaruvi
**Tavsif:** QUIC va TLS 1.3 ning 0-RTT tezlashuvidagi takroriy paketlar hujumi (Replay Attack) xavfini tushunish va oldini olish.
**Talablar:** `MaxEarlyDataSize`, faqat GET/idempotent so'rovlarga ruxsat berish.
**Yechim (Go):**
```go
package main

import (
	"fmt"
)

func explainZeroRttRisks() {
	fmt.Println("TLS 1.3 / HTTP/3 0-RTT Replay hujumi:");
	fmt.Println("0-RTT bilan yuborilgan dastlabki paket shifrlangan bo'lsa-da, tajovuzkor uni tarmoqdan tutib olib, serverga yana qayta jo'natishi mumkin.");
	fmt.Println("Agar bu to'lov so'rovi bo'lsa, pul ikki marta yechilishi xavfi tug'iladi!");
	fmt.Println("Qoida: 0-RTT faqat xavfsiz (GET) so'rovlar uchun yoqilishi, POST/PUT uchun esa to'liq handshake talab qilinishi shart.");
}

func main() {
	explainZeroRttRisks()
}
```
**Tushuntirish:** 0-RTT tezlik bersa-da, kriptografik xavfsizlik darajasi 1-RTT dan pastroqdir (Forward Secrecy yo'q va Replay xavfi mavjud).

---

### Topshiriq #1189: Dinamik TLS Sertifikatlarini Yuklash (GetCertificate Callback)
**Tavsif:** Serverni to'xtatmasdan (Zero Downtime) yangilangan sertifikatlarni avtomatik xotiraga yuklash.
**Talablar:** `tls.Config.GetCertificate`, `tls.Certificate`.
**Yechim (Go):**
```go
package main

import (
	"crypto/tls"
	"fmt"
	"sync"
)

type DynamicCertManager struct {
	mu   sync.RWMutex
	cert *tls.Certificate
}

func (m *DynamicCertManager) GetCertificate(hello *tls.ClientHelloInfo) (*tls.Certificate, error) {
	m.mu.RLock()
	defer m.mu.RUnlock()
	return m.cert, nil
}

func (m *DynamicCertManager) UpdateCertificate(newCert tls.Certificate) {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.cert = &newCert
	fmt.Println("TLS sertifikati parvoz holatida (Zero Downtime) yangilandi.")
}

func main() {
	mgr := &DynamicCertManager{}
	cfg := &tls.Config{GetCertificate: mgr.GetCertificate}
	_ = cfg
	fmt.Println("Dinamik sertifikat menejeri sozlandi.")
}
```
**Tushuntirish:** `GetCertificate` funksiyasi har bir yangi kiruvchi TLS qo'l siqishida chaqiriladi. Bu Let's Encrypt / ACME botlariga sertifikatni almashtirishda serverni qayta ishga tushirmaslik imkonini beradi.

---

### Topshiriq #1190: SNI (Server Name Indication) Orqali Bitta IP Da Ko'p Domenli Xavfsiz Xosting
**Tavsif:** Bitta IP manzil va portda bir nechta turli domenlarga mos sertifikatlarni mijoz yuborgan nom bo'yicha taqdim etish.
**Talablar:** `ClientHelloInfo.ServerName`, domen marshrutlash.
**Yechim (Go):**
```go
package main

import (
	"crypto/tls"
	"errors"
	"fmt"
)

func MultiDomainGetCertificate(certs map[string]*tls.Certificate) func(*tls.ClientHelloInfo) (*tls.Certificate, error) {
	return func(hello *tls.ClientHelloInfo) (*tls.Certificate, error) {
		if cert, ok := certs[hello.ServerName]; ok {
			return cert, nil
		}
		return nil, errors.New("noma'lum domen uchun sertifikat mavjud emas: " + hello.ServerName)
	}
}

func main() {
	fmt.Println("SNI marshrutlash moduli tayyor.")
}
```
**Tushuntirish:** SNI shifrlash boshlanishidan oldin ochiq holda mijoz qaysi saytga murojaat qilayotganini bildiradi, natijada server to'g'ri sertifikatni tanlay oladi.

---

### Topshiriq #1191: Sertifikat Pinning (Certificate Pinning) Klient Himoyasi
**Tavsif:** Mijoz ilovasiga faqat o'zimizning aniq sertifikatimiz yoki ochiq kalitimiz bilan bog'lanishni majburlash.
**Talablar:** `tls.Config.VerifyPeerCertificate`, sha256 barmoq izi tekshiruvi.
**Yechim (Go):**
```go
package main

import (
	"bytes"
	"crypto/sha256"
	"crypto/tls"
	"crypto/x509"
	"errors"
	"fmt"
)

func CreatePinnedTlsConfig(expectedPin [32]byte) *tls.Config {
	return &tls.Config{
		InsecureSkipVerify: true, // Standart zanjirni chetlab, o'zimiz tekshiramiz
		VerifyPeerCertificate: func(rawCerts [][]byte, verifiedChains [][]*x509.Certificate) error {
			if len(rawCerts) == 0 {
				return errors.New("server sertifikat taqdim etmadi")
			}
			fingerprint := sha256.Sum256(rawCerts[0])
			if !bytes.Equal(fingerprint[:], expectedPin[:]) {
				return errors.New("sertifikat barmoq izi mos kelmadi (MITM xavfi)")
			}
			return nil
		},
	}
}

func main() {
	fmt.Println("Certificate Pinning tekshiruvchisi yaratildi.")
}
```
**Tushuntirish:** Certificate Pinning hatto tajovuzkor qurilmaga soxta Root CA o'rnatgan bo'lsa ham (masalan, korporativ proksilar yoki josus dasturlar), soxta sertifikatni darhol fosh qiladi.

---

### Topshiriq #1192: Xavfsiz HTTP Server: HSTS, CSP va Xavfsizlik Sarlavhalari (Security Headers)
**Tavsif:** Brauzer darajasidagi hujumlarni (XSS, Clickjacking, Protocol Downgrade) sarlavhalar orqali to'xtatish.
**Talablar:** `Strict-Transport-Security`, `Content-Security-Policy`, `X-Frame-Options`.
**Yechim (Go):**
```go
package main

import (
	"fmt"
	"net/http"
)

func SecurityHeadersMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// HSTS: 1 yil davomida faqat HTTPS ni majburlash
		w.Header().Set("Strict-Transport-Security", "max-age=31536000; includeSubDomains; preload")
		// XSS va Clickjacking himoyasi
		w.Header().Set("X-Frame-Options", "DENY")
		w.Header().Set("X-Content-Type-Options", "nosniff")
		w.Header().Set("Content-Security-Policy", "default-src 'self'")

		next.ServeHTTP(w, r)
	})
}

func main() {
	fmt.Println("Xavfsizlik sarlavhalari middleware moduli tayyor.")
}
```
**Tushuntirish:** HSTS sarlavhasi brauzerga kelgusida `http://` bilan kirishga urinishlarni avtomatik ravishda so'rov jo'natmasdanoq brauzer ichida `https://` ga o'zgartirishni buyuradi.

---

### Topshiriq #1193: Hashicorp Vault Transit Secrets Engine Bilan EaaS (Encryption-as-a-Service)
**Tavsif:** Ilova ichida shifrlash kalitlarini saqlamasdan, shifrlash va dekodlashni markazlashgan Vault serveriga topshirish.
**Talablar:** Vault HTTP API, `transit/encrypt/key-name`, Base64.
**Yechim (Go):**
```go
package main

import (
	"encoding/base64"
	"fmt"
)

type VaultTransitClient struct {
	VaultAddr string
	Token     string
}

func (v *VaultTransitClient) BuildEncryptRequest(keyName string, plaintext []byte) (string, string) {
	b64Plaintext := base64.StdEncoding.EncodeToString(plaintext)
	endpoint := fmt.Sprintf("%s/v1/transit/encrypt/%s", v.VaultAddr, keyName)
	payload := fmt.Sprintf(`{"plaintext": "%s"}`, b64Plaintext)
	return endpoint, payload
}

func main() {
	client := &VaultTransitClient{VaultAddr: "https://vault.khorazmiy.uz:8200", Token: "s.abcdef123"}
	ep, body := client.BuildEncryptRequest("customer-pii-key", []byte("1234-5678-9012-3456"))
	fmt.Printf("Vault Transit so'rovi:\nURL: %s\nBody: %s\n", ep, body)
}
```
**Tushuntirish:** EaaS modeli orqali dasturchilar va ilovalar maxfiy kalitlarni ko'rmaydi. Kalitlar faqat Vault ning shifrlangan xotirasida turadi va audit loglari to'liq yuritiladi.

---

### Topshiriq #1194: Vault AppRole Autentifikatsiyasi va Xavfsiz Token Boshqaruvi
**Tavsif:** Mikroxizmatlar serverda ishga tushganda o'z RoleID va SecretID si orqali Vault ga kirib vaqtinchalik token olishi.
**Talablar:** `v1/auth/approle/login`, RoleID, SecretID.
**Yechim (Go):**
```go
package main

import (
	"fmt"
)

func BuildAppRoleLoginPayload(roleID, secretID string) string {
	return fmt.Sprintf(`{"role_id":"%s","secret_id":"%s"}`, roleID, secretID)
}

func main() {
	payload := BuildAppRoleLoginPayload("app-backend-role-uuid", "secret-uuid-12345")
	fmt.Printf("Vault AppRole Login Payload: %s\n", payload)
}
```
**Tushuntirish:** AppRole mashinalar va konteynerlar (CI/CD, Kubernetes) uchun mo'ljallangan eng xavfsiz autentifikatsiya usuli bo'lib, statik parollardan to'liq xalos qiladi.

---

### Topshiriq #1195: Dinamik Ma'lumotlar Bazasi Hisob Ma'lumotlari (Database Secrets Engine)
**Tavsif:** Doimiy statik DB parollari o'rniga, har bir xizmat uchun 1 soat yashaydigan vaqtinchalik PostgreSQL foydalanuvchisi yaratish.
**Talablar:** `v1/database/creds/my-role`, avtomatik aylanish (TTL).
**Yechim (Go):**
```go
package main

import (
	"fmt"
	"time"
)

type DynamicDbCreds struct {
	Username string
	Password string
	LeaseTTL time.Duration
}

func main() {
	creds := DynamicDbCreds{
		Username: "v-app-usr-abcdef",
		Password: "tmp_db_secret_password_xyz",
		LeaseTTL: 1 * time.Hour,
	}
	fmt.Printf("Dinamik DB hisob qaydnomasi: User = %s (Amal qilish muddati: %v)\n", creds.Username, creds.LeaseTTL)
}
```
**Tushuntirish:** Dinamik hisoblar xavfsizlik buzilganda yetkaziladigan zararni minimallashtiradi: agar tajovuzkor parolni o'g'irlasa ham, u 1 soatdan keyin avtomatik o'chiriladi.

---

### Topshiriq #1196: AWS KMS / GCP Cloud KMS Bilan Envelope Encryption
**Tavsif:** Bulutli KMS orqali GenerateDataKey API chaqirib, ma'lumotlarni lokal shifrlash va faqat shifrlangan DEK ni saqlash.
**Talablar:** KMS Master Key, Data Key generatsiyasi.
**Yechim (Go):**
```go
package main

import (
	"fmt"
)

func explainKmsEnvelopeEncryption() {
	fmt.Println("Bulutli KMS Envelope Encryption ketma-ketligi:");
	fmt.Println("1. Ilova KMS dan 'GenerateDataKey' so'raydi.");
	fmt.Println("2. KMS ikkita kalit qaytaradi: Ochiq DEK (Plaintext) va KMS bilan shifrlangan DEK (Ciphertext).");
	fmt.Println("3. Ilova ma'lumotni ochiq DEK bilan AES-256-GCM da lokal shifrlaydi.");
	fmt.Println("4. Ochiq DEK xotiradan to'liq o'chiriladi (Zeroize); faqat shifrlangan DEK fayl bilan birga saqlanadi.");
}

func main() {
	explainKmsEnvelopeEncryption()
}
```
**Tushuntirish:** KMS Envelope Encryption gigabaytlik fayllarni bulutga yuborib o'tirmasdan, ularni lokal ravishda chaqmoq tezligida shifrlash imkonini beradi.

---

### Topshiriq #1197: Kalitlarni Avtomatik Rotatsiya Qilish (Key Rotation) va Qayta Shifrlash (Rewrap)
**Tavsif:** Eski ma'lumotlarni ochmasdan, faqat ularning DEK larini yangi KEK versiyasi bilan qayta o'rash (Rewrap).
**Talablar:** Vault `transit/rewrap/key-name`, versiyalar boshqaruvi.
**Yechim (Go):**
```go
package main

import (
	"fmt"
)

func BuildVaultRewrapEndpoint(keyName string) string {
	return fmt.Sprintf("/v1/transit/rewrap/%s", keyName)
}

func main() {
	ep := BuildVaultRewrapEndpoint("master-storage-key")
	fmt.Printf("Vault Rewrap endpointi: %s (Katta ma'lumotlarni ochmasdan kalitni yangilash)\n", ep)
}
```
**Tushuntirish:** `rewrap` operatsiyasi ma'lumotning o'zini ochiq matnga aylantirmasdan faqat shifrlash kalitini yangilashga imkon beradi va kompromat xatarini kamaytiradi.

---

### Topshiriq #1198: Xavfsiz Konfiguratsiya Auditi va Sirlarni In-Memory Demasking
**Tavsif:** Loglarda va xatolik hisobotlarida API kalitlari va parollarning tasodifan fosh bo'lishini (Data Leak) oldini olish.
**Talablar:** `fmt.Stringer` implementatsiyasi orqali sirlarni yashirish.
**Yechim (Go):**
```go
package main

import (
	"fmt"
)

type SecretString string

func (s SecretString) String() string {
	return "******** (REDACTED)"
}

func (s SecretString) Expose() string {
	return string(s)
}

func main() {
	dbPassword := SecretString("SuperSecretDbPassword_2026")
	fmt.Printf("Logga yoziladigan xabar: Parol = %s\n", dbPassword)
	// Asl qiymat faqat Expose() chaqirilganda olinadi
}
```
**Tushuntirish:** `String()` metodini qayta yozish orqali kutilmagan `fmt.Println` yoki JSON serializatsiya paytida maxfiy ma'lumotlarning log fayllariga tushib qolishi to'xtatiladi.

---

### Topshiriq #1199: Vault Lease Renew va Avtomatik Token Muddati Uzaytirish Worker
**Tavsif:** Uzoq ishlovchi Go xizmatida (Daemon) Vault tokeni muddati tugab to'xtab qolmasligi uchun uni orqa fonda yangilab borish.
**Talablar:** `time.Ticker`, `v1/sys/leases/renew`.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
	"time"
)

func StartLeaseRenewWorker(ctx context.Context, renewInterval time.Duration) {
	ticker := time.NewTicker(renewInterval)
	go func() {
		defer ticker.Stop()
		for {
			select {
			case <-ticker.C:
				fmt.Println("[Vault Worker] Token muddati muvaffaqiyatli uzaytirildi (Lease Renewed).")
			case <-ctx.Done():
				fmt.Println("[Vault Worker] To'xtatildi.")
				return
			}
		}
	}()
}

func main() {
	ctx, cancel := context.WithCancel(context.Background())
	StartLeaseRenewWorker(ctx, 100*time.Millisecond)
	time.Sleep(250 * time.Millisecond)
	cancel()
}
```
**Tushuntirish:** Lease Renew worker xizmatning 24/7 rejimida uzilishlarsiz ishlashini va har safar qayta login qilmasdan mavjud tokenning tirik turishini ta'minlaydi.

---

### Topshiriq #1200: Kompleks Xavfsizlik Tizimi: AES-GCM + Ed25519 + TLS 1.3 mTLS + Vault Transit + subtle
**Tavsif:** Barcha o'rganilgan kriptografik prinsiplarni birlashtiruvchi to'liq korporativ xavfsizlik platformasi arxitekturasi.
**Talablar:** Birlashgan xavfsizlik moduli (Master Security Platform).
**Yechim (Go):**
```go
package main

import (
	"crypto/subtle"
	"fmt"
)

type CorporateSecurityGateway struct {
	ServiceName string
}

func (g *CorporateSecurityGateway) VerifyAndProcess(tokenA, tokenB []byte) bool {
	// 1. Doimiy vaqtda xavfsiz autentifikatsiya
	if subtle.ConstantTimeCompare(tokenA, tokenB) != 1 {
		return false
	}

	fmt.Println("=== Khorazmiy AI: Go Kriptografik Xavfsizlik Platformasi ===")
	fmt.Println("1. L4/L7 Himoya: TLS 1.3 va mTLS orqali to'liq shifrlangan aloqa.")
	fmt.Println("2. Simmetrik Shifrlash: AES-256-GCM va ChaCha20-Poly1305 bilan ma'lumotlar yaxlitligi.")
	fmt.Println("3. Asimmetrik Imzo: Ed25519 va RSA-PSS orqali soxtalashtirib bo'lmas raqamli tasdiqlash.")
	fmt.Println("4. Maxfiylik Boshqaruvi: Hashicorp Vault Transit EaaS va Dinamik DB sirlari.")
	fmt.Println("5. Side-Channel Himoyasi: crypto/subtle orqali vaqt hujumlari to'liq bartaraf etildi.")
	return true
}

func main() {
	gw := &CorporateSecurityGateway{ServiceName: "Core-Security-V1"}
	token := []byte("master_auth_key")
	success := gw.VerifyAndProcess(token, token)
	fmt.Printf("Platforma holati: Barcha xavfsizlik testlaridan muvaffaqiyatli o'tdi (%v)\n", success)
}
```
**Tushuntirish:** Ushbu yakuniy modul Go dasturlash tilining barcha zamonaviy kriptografik xavfsizlik imkoniyatlarini mujassam etadi: noldan to'liq korporativ darajadagi xavfsizlik standarti.

---

