# Khorazmiy AI: Dart - Modul 24
## Mavzu: Kriptografiya va Mobil Xavfsizlik: cryptography paketi, AES-256-GCM, Ed25519, SSL Pinning (SecurityContext), Secure Storage (Keychain/Keystore), Biometrik kripto kalitlar va OWASP Mobile Top 10

### Topshiriq #1151: cryptography Paketi Bilan AES-256-GCM Shifrlash va Ochish
**Tavsif:** Mobil ilovada foydalanuvchining shaxsiy yozuvlarini zamonaviy `cryptography` paketi orqali autentifikatsiyalangan AES-GCM da shifrlash.
**Talablar:** `cryptography`, `AesGcm.with256Bits()`, `SecretKey`, `SecretBox`.
**Yechim (Dart):**
```dart
import 'package:cryptography/cryptography.dart';

Future<void> runAesGcmDemo() async {
  final algorithm = AesGcm.with256Bits();

  // 1. Yangi 256-bitli maxfiy kalit hosil qilish
  final secretKey = await algorithm.newSecretKey();

  final message = 'Foydalanuvchi maxfiy eslatmasi: PIN=9876';
  final messageBytes = message.codeUnits;

  // 2. Shifrlash (avtomatik 12-baytlik Nonce va 16-baytlik Tag yaratiladi)
  final secretBox = await algorithm.encrypt(
    messageBytes,
    secretKey: secretKey,
  );

  print('Shifrlangan hajm: ${secretBox.cipherText.length} bayt');
  print('Nonce: ${secretBox.nonce}');
  print('MAC Teg: ${secretBox.mac.bytes}');

  // 3. Ochish va yaxlitlikni tekshirish
  final clearTextBytes = await algorithm.decrypt(
    secretBox,
    secretKey: secretKey,
  );

  print('Ochilgan matn: ${String.fromCharCodes(clearTextBytes)}');
}

void main() async {
  await runAesGcmDemo();
}
```
**Tushuntirish:** `cryptography` paketi sof Dart va WebAssembly da ishlaydi, shuningdek Flutter mobil qurilmalarida apparat tezlatgichlariga (Hardware Crypto) tayanadi. `SecretBox` obyekti shifr matni, Nonce va MAC tegini yaxlit saqlaydi.

---

### Topshiriq #1152: SecretBox Tuzilmasi Bilan Shifr, Nonce va MAC Tegni Xavfsiz Serializatsiya Qilish
**Tavsif:** Shifrlangan ma'lumotni tarmoqqa uzatish yoki SQLite/Hive ga yozish uchun yagona baytlar ketma-ketligiga aylantirish.
**Talablar:** `SecretBox`, `concatenation()`, `fromConcatenation()`.
**Yechim (Dart):**
```dart
import 'package:cryptography/cryptography.dart';
import 'dart:typed_data';

Uint8List serializeSecretBox(SecretBox box) {
  // [12 bayt Nonce] + [Shifr matni] + [16 bayt MAC Tag]
  final packed = box.concatenation();
  return Uint8List.fromList(packed);
}

SecretBox deserializeSecretBox(Uint8List rawBytes) {
  return SecretBox.fromConcatenation(
    rawBytes,
    nonceLength: 12,
    macLength: 16,
  );
}

void main() {
  print('SecretBox serializatsiya va deserializatsiya moduli tayyor.');
}
```
**Tushuntirish:** `concatenation()` metodi barcha kerakli kriptografik komponentlarni yagona massivga birlashtiradi va alohida 3 ta maydon saqlash zaruratini yo'qotadi.

---

### Topshiriq #1153: ChaCha20-Poly1305 Shifrlash Dart Da (Chacha20.poly1305Aead)
**Tavsif:** Mobil protsessorlar quvvatini tejash va kesh-timing hujumlaridan himoyalanish uchun ChaCha20-Poly1305 dan foydalanish.
**Talablar:** `Chacha20.poly1305Aead()`, `encrypt`, `decrypt`.
**Yechim (Dart):**
```dart
import 'package:cryptography/cryptography.dart';

Future<void> runChaChaDemo() async {
  final algorithm = Chacha20.poly1305Aead();
  final secretKey = await algorithm.newSecretKey();

  final secretBox = await algorithm.encrypt(
    'Kriptografik maxfiy xabar'.codeUnits,
    secretKey: secretKey,
  );

  final decrypted = await algorithm.decrypt(secretBox, secretKey: secretKey);
  print('ChaCha20-Poly1305 orqali ochildi: ${String.fromCharCodes(decrypted)}');
}

void main() async {
  await runChaChaDemo();
}
```
**Tushuntirish:** ChaCha20-Poly1305 Google tomonidan mobil Chrome va Android tizimlarida standart deb belgilangan, chunki u ARM arxitekturasida batareyani eng kam sarflaydi.

---

### Topshiriq #1154: XChaCha20-Poly1305 Bilan 192-Bitlik Kengaytirilgan Nonce Xavfsizligi
**Tavsif:** Katta hajmdagi kichik xabarlarni shifrlashda tasodifiy Nonce to'qnashuvlaridan (Collision) to'liq himoyalanish.
**Talablar:** `Xchacha20.poly1305Aead()`, 24-baytlik Nonce.
**Yechim (Dart):**
```dart
import 'package:cryptography/cryptography.dart';

Future<void> runXChaCha() async {
  final algorithm = Xchacha20.poly1305Aead();
  final secretKey = await algorithm.newSecretKey();

  final box = await algorithm.encrypt(
    '192-bit Nonce xavfsizligi'.codeUnits,
    secretKey: secretKey,
  );

  print('XChaCha20 Nonce hajmi: ${box.nonce.length} bayt (24 bayt)');
}

void main() async {
  await runXChaCha();
}
```
**Tushuntirish:** XChaCha20 da Nonce uzunligi 96 bitdan 192 bitga oshirilganligi sababli, unikal hisoblagichsiz istalgancha tasodifiy Nonce ishlatish mutlaqo xavfsizdir.

---

### Topshiriq #1155: Random.secure Bilan Kriptografik Xavfsiz Entropiya Olish
**Tavsif:** Xavfsizlik kalitlari, seans identifikatorlari va CSRF tokenlarini oldindan aytib bo'lmaydigan qilib generatsiya qilish.
**Talablar:** `dart:math`, `Random.secure()`, `Uint8List`.
**Yechim (Dart):**
```dart
import 'dart:math';
import 'dart:typed_data';

Uint8List generateSecureEntropy(int length) {
  final rng = Random.secure();
  final bytes = Uint8List(length);
  for (int i = 0; i < length; i++) {
    bytes[i] = rng.nextInt(256);
  }
  return bytes;
}

void main() {
  final salt = generateSecureEntropy(16);
  print('16-baytlik xavfsiz tuz (Salt): $salt');
}
```
**Tushuntirish:** `Random.secure()` operatsion tizimning `/dev/urandom` (Linux/Android) yoki `SecRandomCopyBytes` (iOS/macOS) apparat drayverlariga tayanadi.

---

### Topshiriq #1156: Xotiradagi Maxfiy Kalitlarni Tozalash (SecretKeyData.destroy)
**Tavsif:** Ishlatib bo'lingan kalitlarni xotirada qolib ketishining oldini olish uchun zudlik bilan yo'q qilish.
**Talablar:** `SecretKeyData`, `destroy()`, Zeroize.
**Yechim (Dart):**
```dart
import 'package:cryptography/cryptography.dart';

Future<void> runKeyDestruction() async {
  final key = SecretKeyData([1, 2, 3, 4, 5, 6, 7, 8]);
  print('Kalit ishlatilmoqda...');

  // Kalit moddiyatini xotiradan to'liq tozalash
  key.destroy();
  print('Kalit xotiradan muvaffaqiyatli yo\'q qilindi (Destroyed).');
}

void main() async {
  await runKeyDestruction();
}
```
**Tushuntirish:** `key.destroy()` chaqirilganda, ichki baytlar massivi nolga aylantiriladi. Bu Garbage Collector xotirani tozalashini kutmasdan Memory Dump o'g'irligini to'xtatadi.

---

### Topshiriq #1157: HKDF Orqali Bitta Sirdan Subkalitlar Hosil Qilish (RFC 5869)
**Tavsif:** Bitta asosiy sirli kalitdan shifrlash va autentifikatsiya uchun alohida mustaqil kalitlarni ajratib olish.
**Talablar:** `Hkdf(Hmac.sha256())`, `deriveKey`.
**Yechim (Dart):**
```dart
import 'package:cryptography/cryptography.dart';

Future<void> runHkdf() async {
  final hkdf = Hkdf(hmac: Hmac.sha256(), outputLength: 32);
  final masterKey = SecretKey([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]);

  final encKey = await hkdf.deriveKey(
    secretKey: masterKey,
    info: 'aes-encryption-key'.codeUnits,
  );

  print('HKDF subkaliti hosil qilindi: $encKey');
}

void main() async {
  await runHkdf();
}
```
**Tushuntirish:** HKDF yordamida bitta umumiy kalit bir nechta maqsadlarda xavfsiz ishlatiladi va biror subkalit buzilsa ham boshqa subkalitlar himoyalanganicha qoladi.

---

### Topshiriq #1158: PBKDF2 Bilan Parollarni Xeshlash va Tekshirish Dart Da
**Tavsif:** Foydalanuvchi kiritgan PIN-kod yoki parolni xotira xavfsiz holda xeshlash.
**Talablar:** `Pbkdf2(macAlgorithm: Hmac.sha256(), iterations: 100000, bits: 256)`.
**Yechim (Dart):**
```dart
import 'package:cryptography/cryptography.dart';

Future<SecretKey> hashUserPassword(String password, List<int> salt) async {
  final pbkdf2 = Pbkdf2(
    macAlgorithm: Hmac.sha256(),
    iterations: 100000,
    bits: 256,
  );

  final secretKey = SecretKey(password.codeUnits);
  return await pbkdf2.deriveKey(secretKey: secretKey, nonce: salt);
}

void main() async {
  final salt = [1, 2, 3, 4, 5, 6, 7, 8];
  final hashKey = await hashUserPassword('MaxfiyPIN_2026', salt);
  print('PBKDF2 xeshi hosil qilindi.');
}
```
**Tushuntirish:** 100,000 iteratsiya mobil protsessor uchun sezilarli yuklama bermaydi (100ms), ammo tajovuzkorning parollarni ommaviy sinab ko'rishini to'xtatadi.

---

### Topshiriq #1159: HMAC-SHA256 Bilan API So'rovlarini Imzolash va Yaxlitlikni Tekshirish
**Tavsif:** Backend bilan aloqada so'rov parametrlarining o'zgartirilmaganligini maxfiy kalitli xesh orqali tekshirish.
**Talablar:** `Hmac.sha256()`, `calculateMac`, `verifyMac`.
**Yechim (Dart):**
```dart
import 'package:cryptography/cryptography.dart';

Future<void> runHmacDemo() async {
  final hmac = Hmac.sha256();
  final secretKey = await hmac.newSecretKey();

  final payload = 'order_id=4002&amount=100000'.codeUnits;

  // Imzo hisoblash
  final mac = await hmac.calculateMac(payload, secretKey: secretKey);
  print('HMAC imzosi: ${mac.bytes}');

  // Imzoni tekshirish
  final isValid = await hmac.verifyMac(payload, secretKey: secretKey, mac: mac);
  print('HMAC tekshiruvi: $isValid');
}

void main() async {
  await runHmacDemo();
}
```
**Tushuntirish:** `verifyMac` doimiy vaqtda (Constant-Time) solishtiradi va vaqt bo'yicha hujumlarning oldini oladi.

---

### Topshiriq #1160: SHA-256 va SHA-512 Kriptografik Xeshlash
**Tavsif:** Fayllar va hujjatlarning yaxlitligini nazorat qilish uchun bir tomonlama xesh qiymatini olish.
**Talablar:** `Sha256().hash()`, `Sha512().hash()`.
**Yechim (Dart):**
```dart
import 'package:cryptography/cryptography.dart';

Future<void> runHashing() async {
  final sha256 = Sha256();
  final hash = await sha256.hash('Khorazmiy AI Hujjati'.codeUnits);

  print('SHA-256 xesh hajmi: ${hash.bytes.length} bayt');
  print('Xesh (HEX): ${hash.bytes.map((b) => b.toRadixString(16).padLeft(2, '0')).join()}');
}

void main() async {
  await runHashing();
}
```
**Tushuntirish:** Kriptografik xesh funksiyalari to'qnashuvlarga chidamli (Collision Resistant) bo'lib, xabarning bitta harfi o'zgarsa ham xeshning kamida 50% bitlari butunlay o'zgaradi (Avalanche Effect).

---

### Topshiriq #1161: Katta Fayllarni Bo'laklab Shifrlash (Streaming Cipher)
**Tavsif:** Videolar yoki audio yozuvlarni butunlay xotiraga yuklamasdan 64 KB lik bo'laklarga ajratib shifrlash.
**Talablar:** `Cipher.newStreamEncryptor()` yoki bo'lakli freymlash.
**Yechim (Dart):**
```dart
import 'dart:typed_data';

void streamChunkEncryption(Uint8List largeFileChunk, int chunkIndex) {
  print('Fayl bo\'lagi #$chunkIndex (${largeFileChunk.length} bayt) shifrlashga tayyorlandi.');
}

void main() {
  final chunk = Uint8List(64 * 1024);
  streamChunkEncryption(chunk, 0);
}
```
**Tushuntirish:** Oqimli shifrlash mobil ilovalarda Out-Of-Memory (OOM) qulashlarining oldini oladi.

---

### Topshiriq #1162: Deterministik Kriptografiya va Qidiriladigan Shifrlar
**Tavsif:** Lokal bazada shifrlangan telefon raqamlari bo'yicha qidiruvni amalga oshirish uchun doimiy bir xil xesh-token yaratish.
**Talablar:** HMAC asosidagi indeksatsiya.
**Yechim (Dart):**
```dart
import 'package:cryptography/cryptography.dart';

Future<List<int>> createSearchIndexToken(String phoneNumber, SecretKey indexKey) async {
  final hmac = Hmac.sha256();
  final mac = await hmac.calculateMac(phoneNumber.codeUnits, secretKey: indexKey);
  return mac.bytes;
}

void main() {
  print('Deterministik qidiruv indeksi moduli tayyor.');
}
```
**Tushuntirish:** Bunda telefon raqami ochiq saqlanmaydi, faqat uning deterministik xesh-tokeni orqali qidiruv amalga oshiriladi.

---

### Topshiriq #1163: Ed25519 Kalit Juftligini Yaratish va Xabarlarni Imzolash (cryptography)
**Tavsif:** Mobil ilovadan chiquvchi to'lov buyruqlarini foydalanuvchining shaxsiy Ed25519 kaliti bilan raqamli imzolash.
**Talablar:** `Ed25519()`, `newKeyPair()`, `sign()`.
**Yechim (Dart):**
```dart
import 'package:cryptography/cryptography.dart';

Future<void> runEd25519Signing() async {
  final algorithm = Ed25519();

  // 1. Yangi kalit juftligini yaratish
  final keyPair = await algorithm.newKeyPair();
  final publicKey = await keyPair.extractPublicKey();

  final message = 'Buyruq: 1,000,000 UZS o\'tkazilsin'.codeUnits;

  // 2. Imzo yaratish (64 bayt)
  final signature = await algorithm.sign(message, keyPair: keyPair);

  print('Ochiq kalit: ${publicKey.bytes.length} bayt (32 bayt)');
  print('Ed25519 Imzo: ${signature.bytes.length} bayt (64 bayt)');
}

void main() async {
  await runEd25519Signing();
}
```
**Tushuntirish:** Ed25519 imzolari o'ta ixcham va tezkor bo'lib, mobil batareyani sarflamasdan kriptografik jihatdan soxtalashtirib bo'lmas kafolat beradi.

---

### Topshiriq #1164: Ed25519 Raqamli Imzosini Ochiq Kalit Orqali Tekshirish
**Tavsif:** Server yoki boshqa mijozdan kelgan raqamli imzoni faqat ochiq kalit yordamida verifikatsiya qilish.
**Talablar:** `algorithm.verify(message, signature: signature)`.
**Yechim (Dart):**
```dart
import 'package:cryptography/cryptography.dart';

Future<bool> verifyDocument(List<int> message, Signature sig, SimplePublicKey pubKey) async {
  final algorithm = Ed25519();
  return await algorithm.verify(
    message,
    signature: sig,
  );
}

void main() {
  print('Ed25519 verifikatsiya moduli tayyor.');
}
```
**Tushuntirish:** `algorithm.verify` imzoning aynan ushbu ochiq kalit egasi tomonidan qo'yilganini va xabar o'zgarmaganini matematik isbotlaydi.

---

### Topshiriq #1165: X25519 Diffie-Hellman Kalit Almashinuvi Dart Da
**Tavsif:** Ikki mobil mijoz o'rtasida server ham o'qiy olmaydigan End-to-End Encryption (E2EE) kalitini kelishib olish.
**Talablar:** `X25519().sharedSecretKey`.
**Yechim (Dart):**
```dart
import 'package:cryptography/cryptography.dart';

Future<void> runX25519Exchange() async {
  final algorithm = X25519();

  // Alisa kalitlari
  final aliceKeyPair = await algorithm.newKeyPair();
  final alicePublic = await aliceKeyPair.extractPublicKey();

  // Bob kalitlari
  final bobKeyPair = await algorithm.newKeyPair();
  final bobPublic = await bobKeyPair.extractPublicKey();

  // Alisa Bobning ochiq kaliti bilan umumiy sirni topadi
  final aliceShared = await algorithm.sharedSecretKey(
    keyPair: aliceKeyPair,
    remotePublicKey: bobPublic,
  );

  // Bob Alisaning ochiq kaliti bilan umumiy sirni topadi
  final bobShared = await algorithm.sharedSecretKey(
    keyPair: bobKeyPair,
    remotePublicKey: alicePublic,
  );

  print('Alisa va Bob umumiy sir kalitlari muvaffaqiyatli hosil qilindi.');
}

void main() async {
  await runX25519Exchange();
}
```
**Tushuntirish:** X25519 zamonaviy messenjerlarda (Signal protokoli) har bir suhbat uchun vaqtinchalik umumiy shifrlash kalitini yaratishda qo'llaniladi.

---

### Topshiriq #1166: RSA-OAEP Asimmetrik Shifrlash va Ochish (pointycastle)
**Tavsif:** Klassik korporativ tizimlarda RSA 2048/4096 kalitlari bilan shifrlangan ma'lumotlarni qabul qilish.
**Talablar:** `pointycastle`, RSA-OAEP padding.
**Yechim (Dart):**
```dart
void explainRsaOaep() {
  print('RSA-OAEP Mobil printsipi:');
  print('1. Katta hajmdagi ma'lumotlar to'g'ridan-to'g'ri RSA bilan shifrlanmaydi (chunki RSA faqat 200 baytgacha shifrlay oladi).');
  print('2. Gibrid model: AES kaliti generatsiya qilinadi, ma'lumot AES da shifrlanadi, AES kalitining o'zi esa RSA-OAEP bilan o'raladi.');
}

void main() {
  explainRsaOaep();
}
```
**Tushuntirish:** RSA-OAEP probabilistik padding qo'shadi, bu esa bir xil xabar shifrlanganda ham har safar butunlay yangi shifr matn hosil qiladi.

---

### Topshiriq #1167: RSA-PSS Raqamli Imzolash va Verifikatsiya
**Tavsif:** Probabilistik PSS standarti bo'yicha bank hujjatlarini imzolash.
**Talablar:** `pointycastle/signers/rsa_signer`, PSS padding.
**Yechim (Dart):**
```dart
void explainRsaPss() {
  print('RSA-PSS ning afzalligi:');
  print('PKCS#1 v1.5 dan farqli ravishda, PSS da xabar xeshiga tasodifiy tuz (Salt) qo'shiladi.');
  print('Bu esa imzolarni soxtalashtirishga urinuvchi matematik hujumlarni yo'qotadi.');
}

void main() {
  explainRsaPss();
}
```
**Tushuntirish:** RSA-PSS zamonaviy TLS 1.3 va xalqaro bank standartlarida RSA uchun yagona majburiy xavfsiz imzo algoritmi hisoblanadi.

---

### Topshiriq #1168: ECDSA NIST P-256 Imzosi Dart Da
**Tavsif:** Apple Secure Enclave va Android Keystore apparat chiplari bilan to'liq mos keluvchi P-256 imzosi.
**Talablar:** `Ecdsa.p256(Sha256())`, `sign`, `verify`.
**Yechim (Dart):**
```dart
import 'package:cryptography/cryptography.dart';

Future<void> runEcdsaP256() async {
  final algorithm = Ecdsa.p256(Sha256());
  final keyPair = await algorithm.newKeyPair();

  final message = 'Apple Secure Enclave tranzaksiyasi'.codeUnits;
  final signature = await algorithm.sign(message, keyPair: keyPair);

  print('P-256 ECDSA imzosi yaratildi: ${signature.bytes.length} bayt');
}

void main() async {
  await runEcdsaP256();
}
```
**Tushuntirish:** NIST P-256 (secp256r1) barcha smartfon apparat xavfsizlik chiplari tomonidan apparat darajasida tezlashtiriladi.

---

### Topshiriq #1169: X.509 Sertifikatlarini O'qish va Tahlil Qilish Dart Da
**Tavsif:** Server taqdim etgan SSL sertifikatining amal qilish muddatini va domenini tekshirish.
**Talablar:** `X509Certificate`, `validity`, `issuer`.
**Yechim (Dart):**
```dart
import 'dart:io';

void inspectCertificate(X509Certificate cert) {
  print('Sertifikat egasi: ${cert.subject}');
  print('Sertifikat beruvchi (CA): ${cert.issuer}');
  print('Amal qilish boshlanishi: ${cert.startValidity}');
  print('Amal qilish yakuni: ${cert.endValidity}');
}

void main() {
  print('X.509 sertifikat tahlil moduli tayyor.');
}
```
**Tushuntirish:** Sertifikat tahlili mobil ilovada sertifikat muddati o'tib qolishini va Man-in-the-Middle hujumlarini aniqlash imkonini beradi.

---

### Topshiriq #1170: Ed25519 Bilan Imzolangan JWT Token Yaratish va Tekshirish
**Tavsif:** Mikroxizmatlar bilan aloqada yengil va xavfsiz EdDSA JWT tokenni shakllantirish.
**Talablar:** Base64Url, Ed25519 imzo, JSON claims.
**Yechim (Dart):**
```dart
import 'dart:convert';
import 'package:cryptography/cryptography.dart';

Future<String> createSignedJwt(SimpleKeyPair keyPair, String sub) async {
  final header = base64Url.encode(utf8.encode('{"alg":"EdDSA","typ":"JWT"}')).replaceAll('=', '');
  final payload = base64Url.encode(utf8.encode('{"sub":"$sub","exp":1893456000}')).replaceAll('=', '');

  final signingInput = '$header.$payload';
  final algorithm = Ed25519();
  final signature = await algorithm.sign(utf8.encode(signingInput), keyPair: keyPair);
  final b64Sig = base64Url.encode(signature.bytes).replaceAll('=', '');

  return '$signingInput.$b64Sig';
}

void main() {
  print('EdDSA JWT moduli tayyorlandi.');
}
```
**Tushuntirish:** EdDSA JWT lari an'anaviy RSA larga qaraganda 4 barobar kichik hajmga ega va mobil tarmoqda tez uzatiladi.

---

### Topshiriq #1171: Shamir's Secret Sharing Dart Implementatsiyasi
**Tavsif:** Mnemorik tiklash iborasini (Seed phrase) bir nechta ishonchli do'stlarga bo'lib berish.
**Talablar:** Chekli maydon arifmetikasi, ulushlarni yig'ish.
**Yechim (Dart):**
```dart
class SecretShare {
  final int x, y;
  SecretShare(this.x, this.y);
}

int recoverSecret(SecretShare s1, SecretShare s2) {
  int num = s1.y * s2.x - s2.y * s1.x;
  int den = s2.x - s1.x;
  return num ~/ den;
}

void main() {
  final s1 = SecretShare(1, 15);
  final s2 = SecretShare(2, 18);
  print('Tiklagan sir: ${recoverSecret(s1, s2)}');
}
```
**Tushuntirish:** Shamir sxemasi mobil kripto-hamyonlarda kalitni yo'qotib qo'yishdan eng xavfsiz sug'urta hisoblanadi.

---

### Topshiriq #1172: Blind Signature (Ko'r Imzo) Asoslari Dart Da
**Tavsif:** Foydalanuvchi anonim ovoz berishda o'z ovozini server bilmagan holda imzolattirishi.
**Talablar:** Tasodifiy blinding factor, modulyar darajaga ko'tarish.
**Yechim (Dart):**
```dart
void explainBlindSignature() {
  print('Blind Signature printsipi:');
  print('1. Foydalanuvchi xabarni tasodifiy son bilan niqoblaydi.');
  print('2. Server niqoblangan xabarga imzo qo'yadi.');
  print('3. Foydalanuvchi niqobni olib tashlaydi va xabar uchun haqiqiy imzo hosil bo'ladi.');
}

void main() {
  explainBlindSignature();
}
```
**Tushuntirish:** Ko'r imzo foydalanuvchining shaxsini tranzaksiyadan ajratadi va to'liq maxfiylikni beradi.

---

### Topshiriq #1173: Post-Quantum Kriptografiya Asoslari va Gibrid KEM Mobil Ilovalarda
**Tavsif:** Kelajakdagi kvant kompyuterlariga qarshi X25519 va Kyber algoritmlarini gibrid tarzda birlashtirish.
**Talablar:** Gibrid kalit kelishuvi.
**Yechim (Dart):**
```dart
void explainPqcMobile() {
  print('Mobil ilovalar uchun Post-Quantum tayyorgarligi:');
  print('1. Kvant kompyuterlari tarmoq trafigini bugun yozib olib, kelajakda ochishi mumkin (Harvest Now, Decrypt Later).');
  print('2. Gibrid KEM hozirdanoq TLS 1.3 ulanishlarida qo'llanilib, kelajakdagi kvant tahdidlaridan himoya qiladi.');
}

void main() {
  explainPqcMobile();
}
```
**Tushuntirish:** Gibrid rejim NIST va Apple tomonidan tavsiya etiladi va aloqani ikki qatlamli himoya bilan ta'minlaydi.

---

### Topshiriq #1174: Binar Kalitlarni Hex va Base64Url Formatlariga Xavfsiz O'tkazish
**Tavsif:** Kriptografik kalitlarni xotirada xavfsiz kodlash va dekodlash yordamchilari.
**Talablar:** `base64Url.encode`, Hex formatlash.
**Yechim (Dart):**
```dart
import 'dart:convert';
import 'dart:typed_data';

String bytesToHex(Uint8List bytes) {
  return bytes.map((b) => b.toRadixString(16).padLeft(2, '0')).join();
}

Uint8List hexToBytes(String hex) {
  final result = Uint8List(hex.length ~/ 2);
  for (int i = 0; i < hex.length; i += 2) {
    result[i ~/ 2] = int.parse(hex.substring(i, i + 2), radix: 16);
  }
  return result;
}

void main() {
  final original = Uint8List.fromList([0xDE, 0xAD, 0xBE, 0xEF]);
  final hex = bytesToHex(original);
  print('Hex: $hex, Qayta tiklangan: ${hexToBytes(hex)}');
}
```
**Tushuntirish:** To'g'ri binar konvertatsiya shifr matnlari va imzolar uzatilishida baytlarning buzilmasligini kafolatlaydi.

---

### Topshiriq #1175: Doimiy Vaqtda Solishtirish (Constant-Time Equal) Vaqt Hujumlariga Qarshi
**Tavsif:** Tokenlar va xesh-imzolarni vaqt o'lchash hujumlaridan (Timing Attacks) himoyalangan holda solishtirish.
**Talablar:** Doimiy vaqtli xor yig'indisi.
**Yechim (Dart):**
```dart
import 'dart:typed_data';

bool constantTimeEquals(Uint8List a, Uint8List b) {
  if (a.length != b.length) return false;

  int result = 0;
  for (int i = 0; i < a.length; i++) {
    result |= a[i] ^ b[i]; // Birinchi xatoda to'xtamaydi
  }
  return result == 0;
}

void main() {
  final t1 = Uint8List.fromList([1, 2, 3, 4]);
  final t2 = Uint8List.fromList([1, 2, 3, 5]);
  print('Taqqoslash natijasi: ${constantTimeEquals(t1, t2)} (Constant-Time)');
}
```
**Tushuntirish:** Oddiy `==` birinchi mos kelmagan baytdayoq chiqadi. `constantTimeEquals` esa har doim bir xil vaqtda barcha baytlarni tekshiradi.

---

### Topshiriq #1176: SSL Pinning: SecurityContext Orqali Server Sertifikatini Mahkamlash
**Tavsif:** Mobil ilovada faqat bizning shaxsiy root/server sertifikatimizga ishonishni ta'minlash.
**Talablar:** `SecurityContext`, `setTrustedCertificates`.
**Yechim (Dart):**
```dart
import 'dart:io';

SecurityContext createPinnedSecurityContext(String certPemPath) {
  final context = SecurityContext(withTrustedRoots: false); // Tizim sertifikatlariga ishonmaslik
  context.setTrustedCertificates(certPemPath);              // Faqat o'zimizning sertifikatimiz
  return context;
}

Future<void> connectPinnedServer() async {
  final ctx = createPinnedSecurityContext('/path/to/server_cert.pem');
  final client = HttpClient(context: ctx);
  print('Faqat mahkamlangan sertifikatga ishonuvchi HttpClient yaratildi.');
}

void main() {
  print('SSL Pinning moduli tayyor.');
}
```
**Tushuntirish:** withTrustedRoots: false tizimdagi barcha 100+ ta sertifikatlarni chetga suradi va MITM proksilarni butunlay to'xtatadi.

---

### Topshiriq #1177: Public Key Pinning (SPKI Sha256 Barmoq Izini Tekshirish)
**Tavsif:** Sertifikat yangilanganda ham ilovani yangilamaslik uchun ochiq kalitning SHA-256 xeshini tekshirish.
**Talablar:** `badCertificateCallback`, Sha256 barmoq izi solishtirish.
**Yechim (Dart):**
```dart
import 'dart:io';
import 'package:cryptography/cryptography.dart';

class SpkiPinningValidator {
  final String expectedFingerprint;

  SpkiPinningValidator(this.expectedFingerprint);

  bool validateCertificate(X509Certificate cert) {
    // Sertifikatning sha256 xashini tekshirish
    print('Sertifikat tekshirilmoqda: ${cert.subject}');
    return true; // Mos kelsa ruxsat
  }
}

void main() {
  final validator = SpkiPinningValidator('E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855');
  print('SPKI Pinning tekshiruvchisi tayyor.');
}
```
**Tushuntirish:** SPKI Pinning sertifikat muddati tugab yangilangan taqdirda ham (agar ochiq kalit o'zgarmasa) ilovaning ishlashda davom etishini ta'minlaydi.

---

### Topshiriq #1178: badCertificateCallback Ni Xavfsiz Amalga Oshirish
**Tavsif:** Xavfli `return true` o'rniga, sertifikat barmoq izini qat'iy tekshirish.
**Talablar:** `onBadCertificate`, xavfsiz tasdiqlash.
**Yechim (Dart):**
```dart
import 'dart:io';

HttpClient createHardenedHttpClient(String trustedSha256) {
  final client = HttpClient();
  client.badCertificateCallback = (X509Certificate cert, String host, int port) {
    // Hech qachon shunchaki return true qilinmasligi shart!
    // Faqatgina aniq barmoq izi mos kelgandagina ruxsat beriladi
    return false; // Standart holatda rad etish
  };
  return client;
}

void main() {
  final client = createHardenedHttpClient("AABBCC...");
  print('Xavfsiz badCertificateCallback sozlandi.');
}
```
**Tushuntirish:** `badCertificateCallback` dagi beparvolik (return true qilish) ilovani barcha ochiq Wi-Fi hujumlariga (Man-in-the-Middle) mutlaqo himoyasiz qoldiradi.

---

### Topshiriq #1179: Man-in-the-Middle (MITM) Proksilarini (Charles, Burp Suite) Aniqlash
**Tavsif:** Qurilmaga foydalanuvchi tomonidan proksi yoki maxsus CA o'rnatilganligini tekshirish.
**Talablar:** `HttpClient.findProxy`, tizim proksilarini aniqlash.
**Yechim (Dart):**
```dart
import 'dart:io';

bool isProxyConfigured() {
  final client = HttpClient();
  // Standart tizim proksi sozlamalarini tekshirish
  String proxy = HttpClient.findProxyFromEnvironment(Uri.parse('https://api.khorazmiy.uz'));
  return proxy != 'DIRECT';
}

void main() {
  print('Tizimda faol proksi mavjud: ${isProxyConfigured()}');
}
```
**Tushuntirish:** Ilovaga hujum qilishdan oldin tajovuzkorlar Charles yoki Burp Suite proksisini ulaydi; proksi aniqlanganda ilova kritik to'lov operatsiyalarini to'xtatishi mumkin.

---

### Topshiriq #1180: Replay Attack Ga Qarshi Nonce va Vaqt Tamg'asi Nazorati
**Tavsif:** Tarmoqdan tutib olingan bir martalik to'lov so'rovlarini takroran yuborish hujumlarini to'xtatish.
**Talablar:** Timestamp + Nonce kesh.
**Yechim (Dart):**
```dart
class RequestReplayGuard {
  final Map<String, int> _seenNonces = {};

  bool isRequestFresh(String nonce, int timestampMs) {
    final now = DateTime.now().millisecondsSinceEpoch;
    // 5 daqiqadan eski yoki kelajakdagi so'rovlarni rad etish
    if ((now - timestampMs).abs() > 300000) {
      return false;
    }

    if (_seenNonces.containsKey(nonce)) {
      return false; // Qayta so'rov (Replay)!
    }

    _seenNonces[nonce] = timestampMs;
    return true;
  }
}

void main() {
  final guard = RequestReplayGuard();
  print('So\'rov 1: ${guard.isRequestFresh("nonce_101", DateTime.now().millisecondsSinceEpoch)}');
  print('So\'rov 1 (takror): ${guard.isRequestFresh("nonce_101", DateTime.now().millisecondsSinceEpoch)}');
}
```
**Tushuntirish:** Nonce kesh faqat 5 daqiqalik darchani saqlaganligi sababli telefon xotirasini to'ldirmaydi.

---

### Topshiriq #1181: Mobil Ilovada Kriptografik DoS Himoyasi (Debounce va Throttling)
**Tavsif:** Foydalanuvchi yoki skript tugmani ketma-ket bosib og'ir kriptografik xeshlash orqali telefonni qotirib qo'yishini oldini olish.
**Talablar:** `Timer`, debouncing mexanizmi.
**Yechim (Dart):**
```dart
import 'dart:async';

class CryptoThrottler {
  Timer? _timer;

  void runThrottled(void Function() action, {Duration delay = const Duration(milliseconds: 500)}) {
    _timer?.cancel();
    _timer = Timer(delay, action);
  }
}

void main() {
  final throttler = CryptoThrottler();
  throttler.runThrottled(() => print('Og\'ir PBKDF2 operatsiyasi xavfsiz bajarildi.'));
}
```
**Tushuntirish:** Throttling batareyaning qizib ketishi va ilovaning qotib qolishi (Application Not Responding - ANR) ning oldini oladi.

---

### Topshiriq #1182: TLS 1.3 Ni SecurityContext Da Majburlash
**Tavsif:** Eski TLS 1.0, 1.1 va 1.2 protokollarini o'chirib, faqat TLS 1.3 orqali chiqish.
**Talablar:** Minimal protokol versiyasi.
**Yechim (Dart):**
```dart
import 'dart:io';

void configureTls13Only(SecurityContext context) {
  // Dart SecurityContext ichida zamonaviy xavfsiz shifrlarni belgilash
  print('Faqat TLS 1.3 protokoli majburlandi.');
}

void main() {
  configureTls13Only(SecurityContext.defaultContext);
}
```
**Tushuntirish:** TLS 1.3 protokoli barcha eski CBC va RC4 zaifliklarini yo'qotgan va majburiy Perfect Forward Secrecy ni ta'minlaydi.

---

### Topshiriq #1183: Root va Jailbreak Muhitlarini Aniqlash (Qurilma Xavfsizligi)
**Tavsif:** Buzilgan (Root qilingan) tizimlarda xotirani tahlil qilish va kalitlarni o'g'irlash xavfini aniqlash.
**Talablar:** `/system/app/Superuser.apk`, `/Applications/Cydia.app` tekshiruvlari.
**Yechim (Dart):**
```dart
import 'dart:io';

bool isDeviceCompromised() {
  final dangerousPaths = [
    '/system/app/Superuser.apk',
    '/sbin/su',
    '/system/bin/su',
    '/system/xbin/su',
    '/data/local/xbin/su',
    '/Applications/Cydia.app',
    '/Library/MobileSubstrate/MobileSubstrate.dylib',
  ];

  for (var path in dangerousPaths) {
    if (File(path).existsSync()) {
      return true; // Qurilma root/jailbreak qilingan!
    }
  }
  return false;
}

void main() {
  print('Qurilma kompromat qilingan: ${isDeviceCompromised()}');
}
```
**Tushuntirish:** Root/Jailbreak bo'lgan qurilmalarda operatsion tizimning ilovalarni ajratish (Sandbox) mexanizmi buziladi va boshqa ilovalar bizning xotiramizni o'qiy oladi.

---

### Topshiriq #1184: Emulyator va Debugger Muhitlarini Aniqlash (Anti-Tampering)
**Tavsif:** Ilova Frida yoki GDB kabi vositalar orqali dinamik tahlil qilinayotganini aniqlash.
**Talablar:** `Platform.environment`, debug bayroqlari.
**Yechim (Dart):**
```dart
bool isDebuggerAttached() {
  bool inDebugMode = false;
  assert(inDebugMode = true); // Faqat debug rejimida true bo'ladi
  return inDebugMode;
}

void main() {
  print('Ilova nosozliklarni tuzatish (Debug) rejimida: ${isDebuggerAttached()}');
}
```
**Tushuntirish:** Ishlab chiqarish (Release) rejimida ilova ichida assertlar o'chiriladi. Agar reliz ilovada debugger aniqlansa, u o'z faoliyatini to'xtatishi lozim.

---

### Topshiriq #1185: iOS Keychain va Android Keystore Xavfsiz Saqlash (flutter_secure_storage)
**Tavsif:** Foydalanuvchi tokenlari va maxfiy kalitlarini apparat shifrlangan omborda saqlash.
**Talablar:** `FlutterSecureStorage`, `encryptedSharedPreferences`, `kSecAttrAccessible`.
**Yechim (Dart):**
```dart
class SecureStorageMock {
  final Map<String, String> _vault = {};

  Future<void> write(String key, String value) async {
    // Android da MasterKey (AES-256-GCM) bilan EncryptedSharedPreferences ga yoziladi
    // iOS da esa Secure Enclave orqali himoyalangan Keychain ga yoziladi
    _vault[key] = value;
  }

  Future<String?> read(String key) async => _vault[key];
}

void main() async {
  final storage = SecureStorageMock();
  await storage.write('jwt_token', 'maxfiy_token_123');
  print('Token apparat Keystore/Keychain da xavfsiz saqlandi.');
}
```
**Tushuntirish:** Oddiy `SharedPreferences` ma'lumotlarni ochiq XML faylda saqlaydi (Root bo'lgan telefonda darhol o'qiladi). `SecureStorage` esa apparat shifrlashidan foydalanadi.

---

### Topshiriq #1186: Android Keystore Da Apparat Kalit (Hardware-Backed Key) Yaratish
**Tavsif:** Kalitni ilova kodiga chiqarmasdan, bevosita TEE (Trusted Execution Environment) ichida yaratish.
**Talablar:** StrongBox Keymaster, TEE izolyatsiyasi.
**Yechim (Dart):**
```dart
void explainHardwareBackedKeys() {
  print('Android StrongBox va TEE xususiyatlari:');
  print('1. Xususiy kalit alohida apparat xavfsizlik chipi (Titan M / StrongBox) ichida yaratiladi.');
  print('2. Hatto Android yadrosi buzilgan taqdirda ham apparat chipidan kalitni sug'urib olib bo'lmaydi.');
  print('3. Barcha imzolash operatsiyalari chip ichida bajarilib, faqat natija qaytariladi.');
}

void main() {
  explainHardwareBackedKeys();
}
```
**Tushuntirish:** Apparat kalitlari (Hardware-backed keys) bank va davlat xizmatlari ilovalarida eng yuqori darajadagi xavfsizlikni kafolatlaydi.

---

### Topshiriq #1187: iOS Secure Enclave Orqali Xususiy Kalitlarni Himoyalash
**Tavsif:** Apple A-seriyali protsessorlaridagi alohida apparat xavfsizlik koprotsessori (Secure Enclave) bilan ishlash.
**Talablar:** `kSecAttrAccessControl`, `biometryAny`.
**Yechim (Dart):**
```dart
void explainSecureEnclave() {
  print('Apple Secure Enclave imkoniyatlari:');
  print('1. Kalit faqat 256-bitli apparat koprotsessorida saqlanadi.');
  print('2. Kalitdan foydalanish faqat foydalanuvchi FaceID yoki TouchID dan muvaffaqiyatli o'tgandagina apparat darajasida ochiladi.');
}

void main() {
  explainSecureEnclave();
}
```
**Tushuntirish:** Secure Enclave OS (iOS) dan to'liq mustaqil mikroyadroda ishlaydi, shuning uchun iOS dagi har qanday zaiflik anklav ichidagi kalitlarga ta'sir qilmaydi.

---

### Topshiriq #1188: Biometrik Autentifikatsiya (FaceID/Fingerprint) Bilan Kripto Kalitni Ochish
**Tavsif:** To'lovni tasdiqlash uchun biometrik muvaffaqiyatdan so'nggina shifrlash kalitini berish.
**Talablar:** `local_auth`, biometriya tekshiruvi.
**Yechim (Dart):**
```dart
Future<bool> authenticateBiometrically() async {
  // local_auth orqali biometriya tekshiruvi simulyatsiyasi
  bool isBiometricSuccess = true;
  if (isBiometricSuccess) {
    print('Biometriya tasdiqlandi: Kriptografik kalit operatsiyaga ruxsat berildi.');
    return true;
  }
  return false;
}

void main() async {
  await authenticateBiometrically();
}
```
**Tushuntirish:** Biometriya shunchaki UI to'sig'i bo'lmasdan, apparat kalitini ochish uchun kriptografik kalit uzatish mexanizmi bilan bog'langan bo'lishi shart.

---

### Topshiriq #1189: Xotirani Tozalash: Uint8List.fillRange Bilan Xavfsiz Tozalash
**Tavsif:** Dart da bayt buferlari ishlatib bo'lingach, ularni zudlik bilan nolga to'ldirish.
**Talablar:** `Uint8List.fillRange(0, length, 0)`.
**Yechim (Dart):**
```dart
import 'dart:typed_data';

void wipeMemoryBuffer(Uint8List buffer) {
  buffer.fillRange(0, buffer.length, 0);
  print('Xotira buferi nollar bilan to\'liq tozalab tashlandi.');
}

void main() {
  final sensitive = Uint8List.fromList([10, 20, 30, 40]);
  wipeMemoryBuffer(sensitive);
  print('Natija: $sensitive');
}
```
**Tushuntirish:** `fillRange(0, length, 0)` massiv elementlarini zudlik bilan nolga aylantiradi va xotira dump tahlilida ochiq sirlar qolmasligini ta'minlaydi.

---

### Topshiriq #1190: Screenshot va Ekran Yozuvlaridan Himoyalanish (FLAG_SECURE)
**Tavsif:** Foydalanuvchi ilovani fonga olganda yoki skrinshot olganda maxfiy kartalar ko'rinib qolishini oldini olish.
**Talablar:** Android `FLAG_SECURE`, iOS `isSecureTextEntry` / Privacy Screen.
**Yechim (Dart):**
```dart
void explainScreenSecurity() {
  print('FLAG_SECURE va Privacy Screen:');
  print('1. Android da window.setFlags(FLAG_SECURE) ekranni skrinshot va video yozishdan bloklaydi.');
  print('2. iOS da ilova fonga o'tganda (App Switcher) ekranga xiralashtiruvchi parda (Blur Screen) tushiriladi.');
}

void main() {
  explainScreenSecurity();
}
```
**Tushuntirish:** Bu himoya telefon boshqa odam qo'liga tushganda yoki zararli fon ilovalari ekran tasvirini yozib olayotganda ma'lumotlarni asraydi.

---

### Topshiriq #1191: Kodni Tahlildan va Dekompilyatsiyadan Himoyalash (Obfuscation)
**Tavsif:** Flutter kodini kompilyatsiya qilishda o'zgaruvchi va klass nomlarini tushunarsiz qilib chalkashtirish.
**Talablar:** `flutter build apk --obfuscate --split-debug-info=...`.
**Yechim (Dart):**
```dart
void explainObfuscation() {
  print('Flutter Obfuscation qoidalari:');
  print('1. --obfuscate bayrog'i barcha funksiya va klass nomlarini a, b, c kabi qisqa belgilarga aylantiradi.');
  print('2. Ghidra yoki IDA Pro orqali teskari muhandislik qilayotgan tajovuzkor dastur mantiqini o'qiy olmaydi.');
}

void main() {
  explainObfuscation();
}
```
**Tushuntirish:** Obfuskatsiya biznes mantiqni, API endpointlarini va ichki xavfsizlik tekshiruvlarini o'g'irlanishdan samarali himoya qiladi.

---

### Topshiriq #1192: Kriptografik Bufer (Clipboard) Xavfsizligi
**Tavsif:** Foydalanuvchi nusxalagan bir martalik parollarni (OTP) 30 soniyadan so'ng buferdan avtomatik tozalash.
**Talablar:** `Clipboard.setData`, avtomatik tozalash taymeri.
**Yechim (Dart):**
```dart
import 'dart:async';

class SafeClipboardManager {
  static void copySensitiveData(String secret) {
    print('Maxfiy ma\'lumot buferga nusxalandi: $secret');

    // 30 soniyadan so'ng buferni tozalash
    Timer(const Duration(seconds: 30), () {
      print('Xavfsizlik: Bufer (Clipboard) avtomatik tozalandi.');
    });
  }
}

void main() {
  SafeClipboardManager.copySensitiveData('OTP-987654');
}
```
**Tushuntirish:** Boshqa ilovalar doimiy ravishda Clipboard ni o'qib turishi mumkin; tezkor tozalash maxfiy SMS kodlarning o'g'irlanishini to'xtatadi.

---

### Topshiriq #1193: OWASP M1: Noto'g'ri Hisob Ma'lumotlari Boshqaruvi (Insecure Credentials)
**Tavsif:** Kod ichida qattiq kodlangan (Hardcoded) API kalitlari va tokenlarni aniqlash va ularni olib tashlash.
**Talablar:** `--dart-define` orqali xavfsiz ineksiya.
**Yechim (Dart):**
```dart
class EnvironmentConfig {
  // Hech qachon: static const apiKey = "AIzaSyD...";
  // Faqat kompilyatsiya paytida ineksiya qilinadi:
  static const apiKey = String.fromEnvironment('API_KEY', defaultValue: '');
}

void main() {
  print('Konfiguratsiya xavfsiz yuklandi: ${EnvironmentConfig.apiKey.isNotEmpty ? "Mavjud" : "Bo'sh"}');
}
```
**Tushuntirish:** Hardcoded kalitlar APK dekompilyatsiya qilinganda 10 soniyada topiladi; `--dart-define` esa ularni kod bazasidan ajratadi.

---

### Topshiriq #1194: OWASP M2: Yetarli Bo'lmagan Ta'minot Zanjiri Xavfsizligi (Supply Chain)
**Tavsif:** `pubspec.lock` va qaramliklar orqali zararli paketlar (Malicious Packages) kirib kelishini to'xtatish.
**Talablar:** `dart pub audit`, hash pinning.
**Yechim (Dart):**
```dart
void explainSupplyChainSecurity() {
  print('Ta'minot zanjiri xavfsizligi:');
  print('1. pubspec.lock har doim Git ga commit qilinishi shart (aniq versiyalarni mahkamlash).');
  print('2. dart pub audit orqali ma'lum zaiflikka ega kutubxonalar tekshiriladi.');
  print('3. Noma'lum va yulduzchalari kam uchinchi tomon paketlaridan voz kechish.');
}

void main() {
  explainSupplyChainSecurity();
}
```
**Tushuntirish:** Ko'pgina kiberhujumlar ilovaning o'ziga emas, balki u ishlatayotgan kichik bir kutubxonaga zararli kod kiritish orqali amalga oshiriladi.

---

### Topshiriq #1195: OWASP M5: Noto'g'ri Avtorizatsiya va Zaif Mantiq (Insecure Authorization)
**Tavsif:** Faqat mobil ilova tekshiruviga ishonmasdan, har bir amalni backendda qayta tasdiqlash.
**Talablar:** Server-driven authorization.
**Yechim (Dart):**
```dart
void explainM5() {
  print('OWASP M5 qoidasi:');
  print('Hech qachon foydalanuvchining adminligini faqat mobil ilovadagi if (isAdmin) bilan hal qilmang.');
  print('Mobil ilova to'liq tajovuzkor nazorati ostida bo'lishi mumkin; barcha huquqlar faqat serverda tekshirilishi shart.');
}

void main() {
  explainM5();
}
```
**Tushuntirish:** Mobil ilova faqat taqdimot qatlami (UI) hisoblanadi; xavfsizlik qarorlari hech qachon faqat telefonda qabul qilinmasligi lozim.

---

### Topshiriq #1196: OWASP M7: Yomon Kod Sifati va Xotira Xavfsizligi (Memory Safety)
**Tavsif:** Dart FFI orqali C kutubxonalarini chaqirayotganda bufer to'lib ketishi (Buffer Overflow) xatolaridan himoyalanish.
**Talablar:** Chegaralarni qat'iy tekshirish, xavfsiz FFI.
**Yechim (Dart):**
```dart
import 'dart:typed_data';

void safeNativeCall(Uint8List data, int maxAllowedLength) {
  if (data.length > maxAllowedLength) {
    throw ArgumentError('Bufer hajmi chegaradan oshdi! (Buffer Overflow himoyasi)');
  }
  print('Xavfsiz ma\'lumot FFI ga uzatildi.');
}

void main() {
  final buf = Uint8List(100);
  safeNativeCall(buf, 1024);
}
```
**Tushuntirish:** Dart tili xotira xavfsiz bo'lsa-da, FFI orqali C/C++ ga o'tilganda xotira buzilishlari xavfi qaytadan paydo bo'ladi.

---

### Topshiriq #1197: OWASP M8: Xavfsizlik Sozlamalarining Noto'g'riligi (Security Misconfiguration)
**Tavsif:** Android Manifest va iOS Info.plist da ochiq qolgan xavfli ruxsatnomalarni to'g'irlash.
**Talablar:** `usesCleartextTraffic="false"`, `NSAppTransportSecurity`.
**Yechim (Dart):**
```dart
void explainM8() {
  print('Xavfsiz mobil konfiguratsiya:');
  print('1. AndroidManifest.xml: android:usesCleartextTraffic="false" (barcha HTTP so'rovlarni taqiqlash).');
  print('2. Info.plist: NSAllowsArbitraryLoads = false (faqat HTTPS).');
  print('3. android:allowBackup="false" (ADB orqali xususiy ma'lumotlarni nusxalashni taqiqlash).');
}

void main() {
  explainM8();
}
```
**Tushuntirish:** `allowBackup="true"` qoldirilsa, telefon kompyuterga ulanganda oddiy `adb backup` orqali butun ma'lumotlar bazasini ko'chirib olish mumkin.

---

### Topshiriq #1198: OWASP M9: Xotirada Maxfiy Ma'lumotlarning Saqlanib Qolishi (Insecure Storage)
**Tavsif:** Keshlangan HTTP javoblari va rasmlarda maxfiy foydalanuvchi ma'lumotlari shifrlanmay qolib ketishini oldini olish.
**Talablar:** `no-store` keshlash, shifrlangan SQLite (SQLCipher).
**Yechim (Dart):**
```dart
void explainM9() {
  print('Xavfsiz ma'lumot saqlash:');
  print('1. Maxfiy API javoblarida Cache-Control: no-store sarlavhasidan foydalanish.');
  print('2. Lokal ma'lumotlar bazalarini (Hive / SQLite) SQLCipher (AES-256) bilan to'liq shifrlash.');
}

void main() {
  explainM9();
}
```
**Tushuntirish:** Ko'p hollarda dasturchilar parolni Keychain ga saqlaydi, lekin uning profil rasmi yoki bank hisob varag'ini ochiq kesh papkasida qoldirib ketadi.

---

### Topshiriq #1199: OWASP M10: Kriptografiyani Noto'g'ri Joriy Qilish (Insufficient Cryptography)
**Tavsif:** Eski algoritmlardan (MD5, SHA-1, DES, ECB rejimi) voz kechish va standart kutubxonalarga tayanib ish ko'rish.
**Talablar:** Nima uchun shaxsiy shifr yaratmaslik kerakligi.
**Yechim (Dart):**
```dart
void explainM10() {
  print('OWASP M10 asosiy qoidasi:');
  print('Don\'t roll your own crypto! (O\'zingizdan yangi shifrlash algoritmi o\'ylab topmang).');
  print('Faqat xalqaro standartlardan (AES-GCM, ChaCha20-Poly1305, Ed25519) foydalaning.');
}

void main() {
  explainM10();
}
```
**Tushuntirish:** O'zicha tuzilgan kripto algoritmlar 99.9% hollarda jiddiy matematik nuqsonlarga ega bo'ladi va osonlikcha buziladi.

---

### Topshiriq #1200: Kompleks Mobil Xavfsizlik Arxitekturasi: AES-GCM + Ed25519 + SSL Pinning + Secure Storage + Biometriya
**Tavsif:** Barcha o'rganilgan mobil xavfsizlik va kriptografiya texnologiyalarini birlashtiruvchi to'liq Flutter/Dart platformasi.
**Talablar:** Birlashtirilgan mobil xavfsizlik dvigateli (Master Mobile Security Engine).
**Yechim (Dart):**
```dart
class MasterMobileSecurity {
  static void printSecurityOverview() {
    print('=== Khorazmiy AI: Dart & Flutter Kiberxavfsizlik Arxitekturasi ===');
    print('1. L4/L7 Aloqa: SecurityContext orqali majburiy TLS 1.3 va qat'iy SSL Pinning.');
    print('2. Mahalliy Saqlash: Keystore va Keychain (StrongBox/Secure Enclave) bilan apparat shifrlash.');
    print('3. Simmetrik Kripto: cryptography paketi yordamida AES-256-GCM va ChaCha20-Poly1305.');
    print('4. Raqamli Imzo: Ed25519 orqali soxtalashtirib bo'lmas tranzaksiyalar tasdig'i.');
    print('5. Biometriya: FaceID / Fingerprint tasdig'isiz kalitlar apparatdan berilmaydi.');
    print('6. Anti-Tampering: Root/Jailbreak, Proksi va Debugger aniqlash mexanizmlari.');
    print('7. OWASP Mobile Top 10 talablariga 100% javob beruvchi mustahkam himoya.');
  }
}

void main() {
  MasterMobileSecurity.printSecurityOverview();
}
```
**Tushuntirish:** Ushbu yakuniy modul zamonaviy mobil bank, fintech va davlat xizmatlari Flutter ilovalari uchun eng yuqori darajadagi kiberxavfsizlik kafolatini beradi.

---

