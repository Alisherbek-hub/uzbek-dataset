# Khorazmiy AI: JavaScript & TypeScript - Modul 24
## Mavzu: Kiberxavfsizlik, Kriptografiya (AES, RSA, ECC) va Xavfsiz Kodlash

### Topshiriq #1151: AES-256-GCM yordamida ma'lumotlarni shifrlash
**Tavsif:** Foydalanuvchi ma'lumotlarini bazada saqlashdan oldin ularni AES-256-GCM algoritmi bilan shifrlash. GCM rejimi yaxlitlikni (integrity) tekshirish imkonini beradi.
**Talablar:** `crypto` modulidan foydalanish, 32 baytli kalit va 12 baytli IV (Initialization Vector) ishlatish.
**Yechim (JavaScript & TypeScript):**
```typescript
import crypto from 'crypto';

const algorithm = 'aes-256-gcm';
const key = crypto.randomBytes(32); // 256 bitli kalit

function encrypt(text: string): { iv: string, encryptedData: string, authTag: string } {
    const iv = crypto.randomBytes(12);
    const cipher = crypto.createCipheriv(algorithm, key, iv);
    let encrypted = cipher.update(text, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    return {
        iv: iv.toString('hex'),
        encryptedData: encrypted,
        authTag: cipher.getAuthTag().toString('hex')
    };
}
```
**Tushuntirish:** GCM rejimi "Authenticated Encryption" hisoblanadi. `authTag` ma'lumotlar o'zgartirilmaganligini kafolatlaydi, bu kiberxavfsizlikda standart hisoblanadi.

### Topshiriq #1152: RSA kalit juftligini generatsiya qilish
**Tavsif:** Server va mijoz o'rtasida xavfsiz almashinuv uchun RSA-4096 kalitlarini yaratish.
**Talablar:** 4096 bit uzunlik, PEM formatida eksport qilish.
**Yechim (JavaScript & TypeScript):**
```typescript
import { generateKeyPairSync } from 'crypto';

const { publicKey, privateKey } = generateKeyPairSync('rsa', {
    modulusLength: 4096,
    publicKeyEncoding: { type: 'spki', format: 'pem' },
    privateKeyEncoding: { type: 'pkcs8', format: 'pem' }
});

console.log("Ochiq kalit:", publicKey);
```
**Tushuntirish:** 4096 bit hozirgi kunda kvant hujumlariga nisbatan yuqori chidamlilikni ta'minlaydi. `pkcs8` formati zamonaviy tizimlar uchun standartdir.

### Topshiriq #1153: SHA-256 bilan parol xeshlash (Salted)
**Tavsif:** Parollarni bazada ochiq holda saqlamaslik uchun `scrypt` algoritmi bilan xeshlash.
**Talablar:** Har bir foydalanuvchi uchun noyob tuz (salt) ishlatish.
**Yechim (JavaScript & TypeScript):**
```typescript
import crypto from 'crypto';

function hashPassword(password: string): string {
    const salt = crypto.randomBytes(16).toString('hex');
    const hash = crypto.scryptSync(password, salt, 64).toString('hex');
    return `${salt}:${hash}`;
}
```
**Tushuntirish:** `scrypt` xotira talab qiluvchi funksiya bo'lib, "Brute-force" hujumlarini sezilarli darajada sekinlashtiradi.

### Topshiriq #1154: ECC (Elliptic Curve Cryptography) imzosi
**Tavsif:** Ma'lumotlarning haqiqiyligini tasdiqlash uchun ECDSA imzosini yaratish.
**Talablar:** `secp256k1` egri chizig'idan foydalanish.
**Yechim (JavaScript & TypeScript):**
```typescript
import { createSign, createVerify } from 'crypto';

const { privateKey, publicKey } = crypto.generateKeyPairSync('ec', { namedCurve: 'secp256k1' });

const sign = createSign('SHA256');
sign.update('Xabar matni');
const signature = sign.sign(privateKey, 'hex');
```
**Tushuntirish:** ECC RSA'ga qaraganda kichikroq kalit o'lchami bilan yuqori xavfsizlik darajasini ta'minlaydi, bu resursi cheklangan qurilmalar uchun optimaldir.

### Topshiriq #1155: XSS (Cross-Site Scripting) oldini olish uchun sanitizatsiya
**Tavsif:** Foydalanuvchi kiritgan ma'lumotlarni HTML-in'yektsiyalardan tozalash.
**Talablar:** Maxsus belgilarni (`<`, `>`, `&`) HTML entitilarga o'girish.
**Yechim (JavaScript & TypeScript):**
```typescript
function sanitize(str: string): string {
    const map: Record<string, string> = {
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#x27;'
    };
    return str.replace(/[&<>"']/g, (m) => map[m]);
}
```
**Tushuntirish:** Bu oddiy, ammo samarali usul. Real loyihalarda `DOMPurify` kabi kutubxonalar tavsiya etiladi.

### Topshiriq #1156: JWT (JSON Web Token) xavfsiz imzolash
**Tavsif:** Foydalanuvchi sessiyasini boshqarish uchun HMAC SHA-256 bilan token yaratish.
**Talablar:** Token muddati (exp) va maxfiy kalit (secret) ishlatish.
**Yechim (JavaScript & TypeScript):**
```typescript
import jwt from 'jsonwebtoken';

const secret = process.env.JWT_SECRET || 'super-maxfiy-kalit';
const token = jwt.sign({ userId: 123 }, secret, { expiresIn: '1h' });
```
**Tushuntirish:** Token muddati cheklangan bo'lishi kerak. `process.env` orqali kalitni saqlash xavfsizlikning birinchi qoidasidir.

### Topshiriq #1157: SQL In'yektsiyani oldini olish (Parameterized Queries)
**Tavsif:** Ma'lumotlar bazasi so'rovlarida foydalanuvchi kiritmalarini xavfsiz bog'lash.
**Talablar:** `pg` (PostgreSQL) kutubxonasi yordamida parametrlangan so'rovlar.
**Yechim (JavaScript & TypeScript):**
```typescript
// Yomon: "SELECT * FROM users WHERE id = " + id;
// Yaxshi:
const query = 'SELECT * FROM users WHERE id = $1';
const values = [userId];
await client.query(query, values);
```
**Tushuntirish:** Parametrlangan so'rovlar SQL kodini ma'lumotdan ajratib beradi, bu in'yektsiya hujumlarini imkonsiz qiladi.

### Topshiriq #1158: CSRF (Cross-Site Request Forgery) himoyasi
**Tavsif:** So'rovlar bilan birga yuboriladigan CSRF tokenni tekshirish.
**Talablar:** Har bir sessiya uchun noyob token generatsiya qilish.
**Yechim (JavaScript & TypeScript):**
```typescript
import crypto from 'crypto';

const csrfToken = crypto.randomBytes(32).toString('hex');
// Tokenni cookie yoki header orqali yuborish va serverda solishtirish
```
**Tushuntirish:** CSRF tokenni tekshirish orqali server so'rovning haqiqiy foydalanuvchi tomonidan yuborilganligini tasdiqlaydi.

### Topshiriq #1159: HTTP Header xavfsizligi (Helmet)
**Tavsif:** Express ilovasida xavfsizlik sarlavhalarini avtomatik sozlash.
**Talablar:** `helmet` kutubxonasidan foydalanish.
**Yechim (JavaScript & TypeScript):**
```typescript
import express from 'express';
import helmet from 'helmet';

const app = express();
app.use(helmet()); // Barcha xavfsizlik sarlavhalarini o'rnatadi
```
**Tushuntirish:** `Helmet` Content-Security-Policy (CSP) kabi sarlavhalarni o'rnatib, brauzer asosidagi hujumlarni bloklaydi.

### Topshiriq #1160: Rate Limiting (Brute-force himoyasi)
**Tavsif:** API endpointlariga ketma-ket so'rovlar yuborilishini cheklash.
**Talablar:** `express-rate-limit` yordamida IP bo'yicha cheklov.
**Yechim (JavaScript & TypeScript):**
```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 daqiqa
    max: 100 // IP uchun maksimal 100 so'rov
});
app.use('/api/', limiter);
```
**Tushuntirish:** Bu DDoS va Brute-force hujumlarini yumshatishning eng samarali usulidir.

---

### Topshiriq #1161: AES-256-GCM yordamida ma'lumotlarni shifrlash
**Tavsif:** Foydalanuvchi ma'lumotlarini bazada xavfsiz saqlash uchun autentifikatsiyalangan shifrlash (AEAD) usulini qo'llash.
**Talablar:** `crypto` modulidan foydalanish, IV (Initialization Vector) unikalligi va Auth Tag tekshiruvi.
**Yechim (JavaScript & TypeScript):**
```typescript
import { createCipheriv, createDecipheriv, randomBytes } from 'crypto';

const algorithm = 'aes-256-gcm';
const key = randomBytes(32); // 256 bitli kalit

export function encrypt(text: string, iv: Buffer): { encrypted: string, tag: string } {
    const cipher = createCipheriv(algorithm, key, iv);
    let encrypted = cipher.update(text, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    return { encrypted, tag: cipher.getAuthTag().toString('hex') };
}
```
**Tushuntirish:** GCM rejimi shifrlash bilan birga ma'lumot yaxlitligini ham tekshiradi, bu esa "bit-flipping" hujumlaridan himoya qiladi.

### Topshiriq #1162: RSA yordamida raqamli imzo yaratish
**Tavsif:** Tranzaksiyalarni tasdiqlash uchun xususiy kalit (private key) yordamida imzo qo'yish.
**Talablar:** `SHA-256` xesh funksiyasi va `RSA-PSS` to'ldirish (padding) sxemasi.
**Yechim (JavaScript & TypeScript):**
```typescript
import { sign } from 'crypto';

function signData(data: string, privateKey: string): string {
    return sign("sha256", Buffer.from(data), {
        key: privateKey,
        padding: 6 // RSA_PKCS1_PSS_PADDING
    }).toString('base64');
}
```
**Tushuntirish:** PSS (Probabilistic Signature Scheme) an'anaviy PKCS#1 v1.5 ga qaraganda xavfsizroq va matematik jihatdan isbotlangan.

### Topshiriq #1163: ECC (Elliptic Curve Cryptography) kalit juftligini generatsiya qilish
**Tavsif:** Resurs tejamkor va yuqori xavfsizlik darajasiga ega bo'lgan `secp256k1` egri chizig'idan foydalanish.
**Talablar:** Asinxron kalit generatsiyasi va xotira boshqaruvi.
**Yechim (JavaScript & TypeScript):**
```typescript
import { generateKeyPairSync } from 'crypto';

const { publicKey, privateKey } = generateKeyPairSync('ec', {
    namedCurve: 'secp256k1',
    publicKeyEncoding: { type: 'spki', format: 'pem' },
    privateKeyEncoding: { type: 'pkcs8', format: 'pem' }
});
```
**Tushuntirish:** ECC kichikroq kalit o'lchami bilan RSA ga nisbatan yuqoriroq xavfsizlikni ta'minlaydi, bu mobil qurilmalar uchun optimaldir.

### Topshiriq #1164: Xavfsiz parol xeshlash (Argon2id)
**Tavsif:** Foydalanuvchi parollarini bazada saqlashda "Brute-force" hujumlariga qarshi himoya.
**Talablar:** `argon2` kutubxonasi, tuz (salt) va xotira chegaralari.
**Yechim (JavaScript & TypeScript):**
```typescript
import * as argon2 from 'argon2';

async function hashPassword(password: string): Promise<string> {
    return await argon2.hash(password, {
        type: argon2.argon2id,
        memoryCost: 2 ** 16, // 64MB
        timeCost: 3
    });
}
```
**Tushuntirish:** Argon2id hozirgi kunda eng xavfsiz xeshlash algoritmi hisoblanadi, chunki u GPU hujumlariga va yon kanal (side-channel) hujumlariga chidamli.

### Topshiriq #1165: JWT (JSON Web Token) xavfsizligini ta'minlash
**Tavsif:** Tokenlarni `HS256` o'rniga `RS256` (asimetrik) bilan imzolash.
**Talablar:** Token muddati (exp) va auditor (aud) maydonlarini tekshirish.
**Yechim (JavaScript & TypeScript):**
```typescript
import jwt from 'jsonwebtoken';

const token = jwt.sign({ sub: 'user123' }, privateKey, { 
    algorithm: 'RS256', 
    expiresIn: '1h' 
});
```
**Tushuntirish:** Asimetrik imzolash serverning xususiy kalitini oshkor qilmasdan tokenlarni tekshirish imkonini beradi.

### Topshiriq #1166: XSS (Cross-Site Scripting) dan himoya qilish
**Tavsif:** Foydalanuvchi kiritgan ma'lumotlarni HTML kontekstida tozalash.
**Talablar:** `dompurify` kutubxonasi va `jsdom` muhiti.
**Yechim (JavaScript & TypeScript):**
```typescript
import createDOMPurify from 'dompurify';
import { JSDOM } from 'jsdom';

const window = new JSDOM('').window;
const DOMPurify = createDOMPurify(window);

const cleanHTML = DOMPurify.sanitize(userInput);
```
**Tushuntirish:** XSS hujumlari brauzerda zararli skriptlarni ishga tushiradi; `sanitize` funksiyasi xavfli teglarni (script, onerror) olib tashlaydi.

### Topshiriq #1167: SQL Injection'ga qarshi parametrlangan so'rovlar
**Tavsif:** Ma'lumotlar bazasiga to'g'ridan-to'g'ri string qo'shishning oldini olish.
**Talablar:** `pg` (PostgreSQL) kutubxonasi va `parameterized queries`.
**Yechim (JavaScript & TypeScript):**
```typescript
const query = 'SELECT * FROM users WHERE email = $1';
const values = [userEmail];
const res = await client.query(query, values);
```
**Tushuntirish:** Parametrlangan so'rovlar SQL buyruqlarini ma'lumotlardan ajratib turadi, bu esa SQL Injection hujumlarini imkonsiz qiladi.

### Topshiriq #1168: Xavfsiz tasodifiy sonlar generatsiyasi
**Tavsif:** Kriptografik operatsiyalar uchun bashorat qilib bo'lmaydigan sonlar yaratish.
**Talablar:** `Math.random()` dan foydalanmaslik, `crypto.getRandomValues`.
**Yechim (JavaScript & TypeScript):**
```typescript
import { randomBytes } from 'crypto';

function generateSecureToken(length: number): string {
    return randomBytes(length).toString('hex');
}
```
**Tushuntirish:** `Math.random()` psevdo-tasodifiy bo'lib, uni bashorat qilish oson. `crypto` moduli esa operatsion tizimning entropiyasidan foydalanadi.

### Topshiriq #1169: HTTP Header xavfsizligi (Helmet.js)
**Tavsif:** Express ilovasida xavfsizlik sarlavhalarini avtomatik sozlash.
**Talablar:** `Content-Security-Policy`, `X-Content-Type-Options`.
**Yechim (JavaScript & TypeScript):**
```typescript
import helmet from 'helmet';
import express from 'express';

const app = express();
app.use(helmet()); // Barcha xavfsizlik sarlavhalarini o'rnatadi
```
**Tushuntirish:** Helmet brauzerga saytni qanday xavfsiz ko'rsatish kerakligini aytuvchi HTTP sarlavhalarini (CSP, HSTS) avtomatik qo'shadi.

### Topshiriq #1170: Rate Limiting (Hujumlarni cheklash)
**Tavsif:** API ga bo'lgan "Brute-force" yoki DDoS hujumlarini oldini olish.
**Talablar:** `express-rate-limit` kutubxonasi va IP asosida cheklash.
**Yechim (JavaScript & TypeScript):**
```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 daqiqa
    max: 100 // IP boshiga 100 ta so'rov
});
app.use('/api/', limiter);
```
**Tushuntirish:** Rate limiting server resurslarini himoya qiladi va botlar orqali amalga oshiriladigan avtomatlashtirilgan hujumlarni sekinlashtiradi.

---

### Topshiriq #1171: AES-256-GCM yordamida ma'lumotlarni shifrlash
**Tavsif:** Foydalanuvchi maxfiy ma'lumotlarini (tokenlar, shaxsiy ma'lumotlar) ma'lumotlar bazasida xavfsiz saqlash uchun AES-256-GCM algoritmini qo'llash.
**Talablar:** `crypto` modulidan foydalanish, IV (Initialization Vector) va Auth Tag'ni saqlash, xavfsiz kalit boshqaruvi.
**Yechim (JavaScript & TypeScript):**
```typescript
import { createCipheriv, createDecipheriv, randomBytes } from 'crypto';

const ALGORITHM = 'aes-256-gcm';
const KEY = randomBytes(32); // 256 bitli kalit

export function encrypt(text: string): string {
  const iv = randomBytes(12); // GCM uchun tavsiya etilgan IV uzunligi
  const cipher = createCipheriv(ALGORITHM, KEY, iv);
  const encrypted = Buffer.concat([cipher.update(text, 'utf8'), cipher.final()]);
  const tag = cipher.getAuthTag();
  return Buffer.concat([iv, tag, encrypted]).toString('base64');
}
```
**Tushuntirish:** GCM (Galois/Counter Mode) nafaqat maxfiylikni, balki ma'lumotlarning yaxlitligini (integrity) ham ta'minlaydi. Auth Tag orqali ma'lumot o'zgartirilgan bo'lsa, dekodlash jarayonida xatolik yuz beradi.

---

### Topshiriq #1172: RSA yordamida kalitlar almashinuvi
**Tavsif:** Mijoz va server o'rtasida simmetrik kalitni xavfsiz uzatish uchun RSA asimmetrik shifrlashdan foydalanish.
**Talablar:** `publicEncrypt` va `privateDecrypt` metodlarini qo'llash, OAEP padding'dan foydalanish.
**Yechim (JavaScript & TypeScript):**
```typescript
import { publicEncrypt, privateDecrypt, generateKeyPairSync } from 'crypto';

const { publicKey, privateKey } = generateKeyPairSync('rsa', { modulusLength: 2048 });

const secretKey = "super-maxfiy-kalit";
const encrypted = publicEncrypt({ key: publicKey, padding: 1 }, Buffer.from(secretKey));
const decrypted = privateDecrypt({ key: privateKey, padding: 1 }, encrypted);
```
**Tushuntirish:** RSA-OAEP zamonaviy standart hisoblanadi. Padding uchun `RSA_PKCS1_OAEP_PADDING` ishlatish hujumlardan (padding oracle attacks) himoya qiladi.

---

### Topshiriq #1173: ECC (Elliptic Curve Cryptography) imzosi
**Tavsif:** Tranzaksiyalar yoki API so'rovlarining haqiqiyligini tekshirish uchun ECDSA raqamli imzosini yaratish.
**Talablar:** `secp256k1` egri chizig'idan foydalanish, xabarni imzolash va tekshirish.
**Yechim (JavaScript & TypeScript):**
```typescript
import { createSign, createVerify, generateKeyPairSync } from 'crypto';

const { publicKey, privateKey } = generateKeyPairSync('ec', { namedCurve: 'secp256k1' });

const data = "Tranzaksiya ma'lumoti #101";
const signer = createSign('SHA256');
signer.update(data);
const signature = signer.sign(privateKey, 'hex');

const verifier = createVerify('SHA256');
verifier.update(data);
const isValid = verifier.verify(publicKey, signature, 'hex');
```
**Tushuntirish:** ECC RSA'ga qaraganda kichikroq kalit o'lchami bilan yuqori xavfsizlik darajasini ta'minlaydi, bu esa resurslarni tejaydi.

---

### Topshiriq #1174: Xavfsiz parol xeshlash (Argon2)
**Tavsif:** Foydalanuvchi parollarini bazada saqlash uchun eng xavfsiz xesh funksiyasini qo'llash.
**Talablar:** `argon2` kutubxonasidan foydalanish, salt va cost faktorlarini sozlash.
**Yechim (JavaScript & TypeScript):**
```typescript
import * as argon2 from 'argon2';

async function hashPassword(password: string): Promise<string> {
  return await argon2.hash(password, {
    type: argon2.argon2id,
    memoryCost: 2 ** 16, // 64MB
    timeCost: 3,
    parallelism: 1
  });
}
```
**Tushuntirish:** Argon2id - bu GPU hujumlariga va yon kanal (side-channel) hujumlariga chidamli bo'lgan zamonaviy standart.

---

### Topshiriq #1175: XSS (Cross-Site Scripting) oldini olish
**Tavsif:** Foydalanuvchi kiritgan ma'lumotlarni HTML sahifada xavfsiz ko'rsatish.
**Talablar:** Maxsus belgilarni (tags) escape qilish, DOM-based XSS'ni bloklash.
**Yechim (JavaScript & TypeScript):**
```typescript
function escapeHTML(str: string): string {
  const map: Record<string, string> = {
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
  };
  return str.replace(/[&<>"']/g, (m) => map[m]);
}
```
**Tushuntirish:** Brauzer interpretatorini aldashning oldini olish uchun barcha maxsus belgilarni HTML entity'larga aylantirish shart.

---

### Topshiriq #1176: SQL Injection'dan himoya
**Tavsif:** Ma'lumotlar bazasiga so'rov yuborishda foydalanuvchi kiritgan ma'lumotlarni tozalash.
**Talablar:** Parametrlashtirilgan so'rovlardan (Prepared Statements) foydalanish.
**Yechim (JavaScript & TypeScript):**
```typescript
// Yomon yondashuv: "SELECT * FROM users WHERE id = " + id;
// Yaxshi yondashuv (pg kutubxonasi misolida):
const query = 'SELECT * FROM users WHERE username = $1';
const values = [userInput];
await client.query(query, values);
```
**Tushuntirish:** Parametrlashtirilgan so'rovlar SQL kodini ma'lumotdan ajratib turadi, bu esa SQLi hujumlarini imkonsiz qiladi.

---

### Topshiriq #1177: JWT (JSON Web Token) xavfsizligi
**Tavsif:** Tokenlarni imzolashda kuchli algoritmlardan foydalanish va `none` algoritmini bloklash.
**Talablar:** `jsonwebtoken` kutubxonasi, `HS256` yoki `RS256` ishlatish.
**Yechim (JavaScript & TypeScript):**
```typescript
import jwt from 'jsonwebtoken';

const token = jwt.sign({ userId: 123 }, process.env.JWT_SECRET!, {
  algorithm: 'HS256',
  expiresIn: '1h'
});
```
**Tushuntirish:** Token muddati (exp) va kuchli maxfiy kalit (secret) JWT xavfsizligining asosidir.

---

### Topshiriq #1178: Rate Limiting (Brute-force hujumiga qarshi)
**Tavsif:** API so'rovlar sonini cheklash orqali tizimni DDoS va Brute-force hujumlaridan himoya qilish.
**Talablar:** `express-rate-limit` middleware'idan foydalanish.
**Yechim (JavaScript & TypeScript):**
```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 daqiqa
  max: 100, // IP manziliga 100 ta so'rov
  message: "Juda ko'p so'rov yuborildi, kuting."
});
```
**Tushuntirish:** Bu yondashuv server resurslarini himoya qiladi va avtomatlashtirilgan hujumlarni sekinlashtiradi.

---

### Topshiriq #1179: HTTP Header xavfsizligi (Helmet)
**Tavsif:** HTTP javob sarlavhalarini sozlash orqali brauzer xavfsizligini kuchaytirish.
**Talablar:** `helmet` middleware'ini qo'llash.
**Yechim (JavaScript & TypeScript):**
```typescript
import helmet from 'helmet';
import express from 'express';

const app = express();
app.use(helmet()); // Xavfsizlik sarlavhalarini avtomatik qo'shadi
```
**Tushuntirish:** `Helmet` CSP (Content Security Policy), HSTS va boshqa sarlavhalarni sozlab, Clickjacking va XSS hujumlarini kamaytiradi.

---

### Topshiriq #1180: Environment Variables xavfsizligi
**Tavsif:** Maxfiy kalitlarni kod ichida saqlamaslik va ularni `.env` faylidan yuklash.
**Talablar:** `dotenv` kutubxonasi, kodni commit qilmaslik.
**Yechim (JavaScript & TypeScript):**
```typescript
import 'dotenv/config';

const DB_PASSWORD = process.env.DB_PASSWORD;
if (!DB_PASSWORD) {
  throw new Error("XAVF: DB_PASSWORD aniqlanmadi!");
}
```
**Tushuntirish:** Kodni versiya boshqaruv tizimiga (Git) yuklaganda maxfiy ma'lumotlar sizib chiqishining oldini olish uchun `.env` fayli `.gitignore` ga qo'shilishi shart.

---

### Topshiriq #1181: AES-GCM yordamida ma'lumotlarni shifrlash
**Tavsif:** Foydalanuvchi ma'lumotlarini bazada xavfsiz saqlash uchun AES-256-GCM algoritmidan foydalanish.
**Talablar:** `crypto` modulidan foydalanish, IV (Initialization Vector) har safar noyob bo'lishi shart.
**Yechim (JavaScript & TypeScript):**
```typescript
import { randomBytes, createCipheriv, createDecipheriv } from 'crypto';

const algorithm = 'aes-256-gcm';
const key = randomBytes(32); // 256 bitli kalit

export function encrypt(text: string): { iv: string, encryptedData: string, authTag: string } {
    const iv = randomBytes(12);
    const cipher = createCipheriv(algorithm, key, iv);
    let encrypted = cipher.update(text, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    return { iv: iv.toString('hex'), encryptedData: encrypted, authTag: cipher.getAuthTag().toString('hex') };
}
```
**Tushuntirish:** GCM rejimi ma'lumotlarning maxfiyligi bilan birga yaxlitligini (integrity) ham ta'minlaydi.

### Topshiriq #1182: RSA kalit juftligini generatsiya qilish
**Tavsif:** JWT tokenlari yoki xabarlarni imzolash uchun RSA-4096 kalitlarini yaratish.
**Talablar:** Asinxron generatsiya, xavfsizlik uchun 4096 bit uzunlik.
**Yechim (JavaScript & TypeScript):**
```typescript
import { generateKeyPairSync } from 'crypto';

const { publicKey, privateKey } = generateKeyPairSync('rsa', {
    modulusLength: 4096,
    publicKeyEncoding: { type: 'spki', format: 'pem' },
    privateKeyEncoding: { type: 'pkcs8', format: 'pem' }
});
console.log("Kalitlar muvaffaqiyatli yaratildi.");
```
**Tushuntirish:** 4096 bit hozirgi kunda standart hisoblanadi va brute-force hujumlariga chidamli.

### Topshiriq #1183: Xavfsiz parol xeshlash (Argon2)
**Tavsif:** Parollarni bazada saqlashdan oldin ularni "salt" va "hash" qilish.
**Talablar:** `argon2` kutubxonasi, yuqori xavfsizlik parametrlari.
**Yechim (JavaScript & TypeScript):**
```typescript
import * as argon2 from 'argon2';

async function hashPassword(password: string): Promise<string> {
    // Argon2id eng xavfsiz variant hisoblanadi
    return await argon2.hash(password, { type: argon2.argon2id });
}
```
**Tushuntirish:** Argon2id GPU hujumlariga qarshi eng samarali xesh funksiyasidir.

### Topshiriq #1184: XSS (Cross-Site Scripting) oldini olish
**Tavsif:** Foydalanuvchi kiritgan ma'lumotlarni tozalash (sanitization).
**Talablar:** HTML teglarini tozalash, `dompurify` kutubxonasi.
**Yechim (JavaScript & TypeScript):**
```typescript
import createDOMPurify from 'dompurify';
import { JSDOM } from 'jsdom';

const window = new JSDOM('').window;
const DOMPurify = createDOMPurify(window);

const cleanInput = (dirty: string) => DOMPurify.sanitize(dirty);
```
**Tushuntirish:** XSS hujumlarini oldini olish uchun har qanday kiritilgan ma'lumotni render qilishdan oldin tozalash shart.

### Topshiriq #1185: ECC (Elliptic Curve Cryptography) imzo
**Tavsif:** ECC yordamida raqamli imzo yaratish.
**Talablar:** `secp256k1` egri chizig'idan foydalanish.
**Yechim (JavaScript & TypeScript):**
```typescript
import { sign, createHash } from 'crypto';

const data = "Muhim hujjat";
const hash = createHash('sha256').update(data).digest();
// privateKey yordamida imzolash
const signature = sign('sha256', hash, { key: privateKey, dsaEncoding: 'ieee-p1363' });
```
**Tushuntirish:** ECC RSA ga qaraganda kichikroq kalitlar bilan yuqori xavfsizlikni ta'minlaydi.

### Topshiriq #1186: SQL Injection himoyasi
**Tavsif:** Parametrlashtirilgan so'rovlar orqali SQL injeksiyani bloklash.
**Talablar:** `pg` yoki `mysql2` kutubxonalarida tayyor so'rovlardan foydalanish.
**Yechim (JavaScript & TypeScript):**
```typescript
const query = 'SELECT * FROM users WHERE email = $1';
const values = ['user@example.com'];
// pool.query(query, values) - bu yerda $1 xavfsiz joylashtiriladi
```
**Tushuntirish:** SQL so'roviga o'zgaruvchilarni to'g'ridan-to'g'ri qo'shish xavfli, parametrlashtirish esa ma'lumotlarni ajratib turadi.

### Topshiriq #1187: JWT (JSON Web Token) xavfsizligi
**Tavsif:** Tokenlarni `httpOnly` va `secure` cookie'larda saqlash.
**Talablar:** Token muddati (exp) va imzolash algoritmi (HS256).
**Yechim (JavaScript & TypeScript):**
```typescript
import jwt from 'jsonwebtoken';

const token = jwt.sign({ userId: 123 }, process.env.JWT_SECRET!, { expiresIn: '1h' });
// Cookie'ga yozish
res.cookie('token', token, { httpOnly: true, secure: true, sameSite: 'strict' });
```
**Tushuntirish:** `httpOnly` flagi JavaScript orqali tokenni o'g'irlashni imkonsiz qiladi.

### Topshiriq #1188: Rate Limiting (Brute-force himoyasi)
**Tavsif:** API so'rovlar sonini cheklash.
**Talablar:** `express-rate-limit` kutubxonasi.
**Yechim (JavaScript & TypeScript):**
```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 daqiqa
    max: 100 // IP manziliga 100 ta so'rov
});
```
**Tushuntirish:** Bu DDoS va brute-force hujumlarini sezilarli darajada kamaytiradi.

### Topshiriq #1189: Xavfsiz tasodifiy sonlar generatsiyasi
**Tavsif:** Kriptografik jihatdan xavfsiz tasodifiy sonlar (CSPRNG).
**Talablar:** `Math.random()` ishlatmaslik (u xavfsiz emas).
**Yechim (JavaScript & TypeScript):**
```typescript
import { randomInt } from 'crypto';

const secureNumber = randomInt(0, 1000000);
console.log(secureNumber);
```
**Tushuntirish:** `Math.random()` deterministik, `crypto.randomInt` esa kriptografik xavfsizdir.

### Topshiriq #1190: Helmet.js bilan HTTP sarlavhalari
**Tavsif:** Veb-ilovaning HTTP sarlavhalarini xavfsiz sozlash.
**Talablar:** `helmet` kutubxonasi.
**Yechim (JavaScript & TypeScript):**
```typescript
import helmet from 'helmet';
import express from 'express';

const app = express();
app.use(helmet()); // Avtomatik xavfsiz sarlavhalar qo'shadi
```
**Tushuntirish:** Helmet CSP, X-Content-Type-Options kabi himoya sarlavhalarini avtomatik sozlaydi.

---

### Topshiriq #1191: AES-256-GCM yordamida ma'lumotlarni shifrlash
**Tavsif:** Foydalanuvchi maxfiy ma'lumotlarini (API kalitlari, tokenlar) bazada saqlashdan oldin xavfsiz shifrlash zarur. AES-GCM autentifikatsiyalangan shifrlashni ta'minlaydi.
**Talablar:** `crypto` modulidan foydalanish, 32 baytli kalit va 12 baytli IV (Initialization Vector) ishlatish.
**Yechim (JavaScript & TypeScript):**
```typescript
import { createCipheriv, randomBytes } from 'crypto';

const algorithm = 'aes-256-gcm';
const key = randomBytes(32); // 256 bitli kalit

function encryptData(text: string): { iv: string; encrypted: string; authTag: string } {
  const iv = randomBytes(12);
  const cipher = createCipheriv(algorithm, key, iv);
  let encrypted = cipher.update(text, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  return {
    iv: iv.toString('hex'),
    encrypted,
    authTag: cipher.getAuthTag().toString('hex')
  };
}
```
**Tushuntirish:** GCM rejimi ma'lumotlarning yaxlitligini (integrity) tekshirish uchun `authTag` yaratadi, bu esa ma'lumotlarning o'zgartirilmaganini kafolatlaydi.

### Topshiriq #1192: RSA yordamida kalit almashinuvi
**Tavsif:** Mijoz va server o'rtasida simmetrik kalitni xavfsiz uzatish uchun RSA asimmetrik shifrlashdan foydalanish.
**Talablar:** `publicEncrypt` va `privateDecrypt` metodlarini qo'llash.
**Yechim (JavaScript & TypeScript):**
```typescript
import { generateKeyPairSync, publicEncrypt, privateDecrypt } from 'crypto';

const { publicKey, privateKey } = generateKeyPairSync('rsa', { modulusLength: 2048 });

const secretKey = "maxfiy-kalit-123";
const encrypted = publicEncrypt(publicKey, Buffer.from(secretKey));
const decrypted = privateDecrypt(privateKey, encrypted).toString();
```
**Tushuntirish:** RSA katta ma'lumotlar uchun sekin, shuning uchun u faqat kichik kalitlarni uzatish uchun ishlatiladi.

### Topshiriq #1193: ECC (Elliptic Curve Cryptography) imzosi
**Tavsif:** Xabarning haqiqiyligini tekshirish uchun ECDSA raqamli imzosini yaratish.
**Talablar:** `secp256k1` egri chizig'idan foydalanish.
**Yechim (JavaScript & TypeScript):**
```typescript
import { createSign, createVerify, generateKeyPairSync } from 'crypto';

const { publicKey, privateKey } = generateKeyPairSync('ec', { namedCurve: 'secp256k1' });

const data = "Tranzaksiya ma'lumoti";
const sign = createSign('SHA256');
sign.update(data);
const signature = sign.sign(privateKey, 'hex');

const verify = createVerify('SHA256');
verify.update(data);
const isValid = verify.verify(publicKey, signature, 'hex');
```
**Tushuntirish:** ECC RSA'ga qaraganda kichikroq kalit o'lchami bilan yuqori xavfsizlikni ta'minlaydi, bu mobil qurilmalar uchun optimaldir.

### Topshiriq #1194: Xavfsiz parol xeshlash (Argon2id)
**Tavsif:** Parollarni bazada saqlashda oddiy xeshlar (MD5, SHA1) yetarli emas. Argon2id - eng xavfsiz standart.
**Talablar:** `argon2` kutubxonasidan foydalanish, tuz (salt) qo'shish.
**Yechim (JavaScript & TypeScript):**
```typescript
import * as argon2 from 'argon2';

async function hashPassword(password: string): Promise<string> {
  return await argon2.hash(password, {
    type: argon2.argon2id,
    memoryCost: 2 ** 16, // 64MB
    timeCost: 3
  });
}
```
**Tushuntirish:** Argon2id GPU hujumlariga va vaqtga asoslangan hujumlarga (side-channel) chidamli.

### Topshiriq #1195: XSS (Cross-Site Scripting) oldini olish
**Tavsif:** Foydalanuvchi kiritgan ma'lumotlarni HTML'ga chiqarishda xavfsiz kodlash.
**Talablar:** Maxsus belgilarni (`<`, `>`, `&`, `"`) HTML entitilarga o'girish.
**Yechim (JavaScript & TypeScript):**
```typescript
function escapeHTML(str: string): string {
  const map: Record<string, string> = {
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
  };
  return str.replace(/[&<>"']/g, (m) => map[m]);
}
```
**Tushuntirish:** Bu funksiya brauzerga kiritilgan ma'lumotni kod sifatida emas, balki oddiy matn sifatida qabul qilishni buyuradi.

### Topshiriq #1196: JWT (JSON Web Token) xavfsizligi
**Tavsif:** Tokenni imzolashda `HS256` o'rniga `RS256` dan foydalanish va `exp` (expire) vaqtini belgilash.
**Talablar:** `jsonwebtoken` kutubxonasi, private key bilan imzolash.
**Yechim (JavaScript & TypeScript):**
```typescript
import jwt from 'jsonwebtoken';

const privateKey = '---PRIVATE KEY---';
const token = jwt.sign({ userId: 123 }, privateKey, { 
  algorithm: 'RS256', 
  expiresIn: '1h' 
});
```
**Tushuntirish:** RS256 tokenning server tomonidan yaratilganligini tasdiqlash imkonini beradi, chunki faqat serverda maxfiy kalit mavjud.

### Topshiriq #1197: SQL Inyeksiya oldini olish
**Tavsif:** Ma'lumotlar bazasiga so'rov yuborishda parametrlangan so'rovlardan foydalanish.
**Talablar:** `pg` (PostgreSQL) kutubxonasi yordamida `prepared statements` ishlatish.
**Yechim (JavaScript & TypeScript):**
```typescript
const query = 'SELECT * FROM users WHERE email = $1';
const values = ['user@example.com'];
// So'rov bazaga xavfsiz yuboriladi
const res = await client.query(query, values);
```
**Tushuntirish:** Parametrlangan so'rovlar foydalanuvchi kiritgan ma'lumotni SQL buyrug'idan ajratib turadi, inyeksiya imkonini yo'q qiladi.

### Topshiriq #1198: CSRF (Cross-Site Request Forgery) himoyasi
**Tavsif:** So'rovlar bilan birga yuboriladigan tasodifiy token orqali hujumlarni bloklash.
**Talablar:** `csurf` middleware yoki maxsus header tekshiruvi.
**Yechim (JavaScript & TypeScript):**
```typescript
// Express middleware misoli
function csrfProtection(req, res, next) {
  const token = req.headers['x-csrf-token'];
  if (token !== req.session.csrfSecret) {
    return res.status(403).send('CSRF token xatosi');
  }
  next();
}
```
**Tushuntirish:** Token faqat haqiqiy mijozda bo'lganligi sababli, uchinchi tomon saytlari so'rovni soxtalashtira olmaydi.

### Topshiriq #1199: Rate Limiting (Brute-force himoyasi)
**Tavsif:** Bir IP manzildan kelayotgan so'rovlar sonini cheklash.
**Talablar:** `express-rate-limit` kutubxonasi, 15 daqiqada 100 ta so'rov.
**Yechim (JavaScript & TypeScript):**
```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  message: "Juda ko'p so'rov yuborildi, kuting."
});
```
**Tushuntirish:** Bu DDOS va brute-force hujumlarining oldini oladi, server resurslarini himoya qiladi.

### Topshiriq #1200: Helmet.js bilan HTTP Header xavfsizligi
**Tavsif:** HTTP javoblarida xavfsizlik sarlavhalarini (HSTS, CSP) avtomatik sozlash.
**Talablar:** `helmet` kutubxonasini Express ilovasiga ulash.
**Yechim (JavaScript & TypeScript):**
```typescript
import express from 'express';
import helmet from 'helmet';

const app = express();
app.use(helmet()); // Barcha asosiy xavfsizlik headerlarini o'rnatadi
```
**Tushuntirish:** Helmet `Content-Security-Policy` va `X-Frame-Options` kabi headerlarni sozlab, brauzer darajasidagi hujumlarni (Clickjacking, XSS) kamaytiradi.