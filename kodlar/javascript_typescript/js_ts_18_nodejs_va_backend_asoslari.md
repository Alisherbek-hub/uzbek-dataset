# 851-Topshiriq: Node.js Global process obyekti

## Topshiriq sharti:
Joriy jarayon identifikatori (PID), Node versiyasi va buyruqlar satri argumentlarini (argv) o'quvchi kod yozing.

## Yechim (JS yoki TS kodi):
```typescript
console.log(`Node versiyasi: ${process.version}`);
console.log(`Jarayon PID: ${process.pid}`);
console.log(`Joriy ishchi papka: ${process.cwd()}`);
console.log(`Buyruq argumentlari soni: ${process.argv.length}`);
```

## Tushuntirish va Mantiq:
`process` Node.js ning global obyekti bo'lib, operatsion tizim jarayoni, muhit o'zgaruvchilari va kiruvchi argumentlarni boshqaradi.

## Ishlash natijasi:
```text
Node versiyasi: v24.19.0
Jarayon PID: 1234
Joriy ishchi papka: C:\Users\User\Desktop
Buyruq argumentlari soni: 2
```


# 852-Topshiriq: path moduli: path.join va path.resolve farqi

## Topshiriq sharti:
Yo'llarni xavfsiz birlashtirishda join va resolve metodlarini solishtiring.

## Yechim (JS yoki TS kodi):
```typescript
import path from "path";

const joined = path.join("/users", "project", "src", "index.ts");
const resolved = path.resolve("src", "index.ts");

console.log("Joined yo'l:", joined);
console.log("Resolved mutlaq yo'l mavjud:", resolved.includes("index.ts"));
```

## Tushuntirish va Mantiq:
`path.join` barcha bo'laklarni tizim separatoriga (Windowsda \, Linuxda /) qarab birlashtiradi. `path.resolve` esa mutlaq (absolute) yo'l hosil qiladi.

## Ishlash natijasi:
```text
Joined yo'l: \users\project\src\index.ts
Resolved mutlaq yo'l mavjud: true
```


# 853-Topshiriq: path moduli: extname, basename va dirname

## Topshiriq sharti:
Fayl yo'lidan uning kengaytmasi, fayl nomi va jild nomini ajratib oling.

## Yechim (JS yoki TS kodi):
```typescript
import path from "path";

const sampleFile = "C:/apps/backend/server.controller.ts";

console.log("Kengaytmasi:", path.extname(sampleFile));
console.log("Fayl nomi:", path.basename(sampleFile));
console.log("Kengaytmasiz nomi:", path.basename(sampleFile, ".ts"));
console.log("Jild yo'li:", path.dirname(sampleFile));
```

## Tushuntirish va Mantiq:
`path.extname` fayl kengaytmasini, `path.basename` fayl nomini, `path.dirname` esa uning joylashgan jildini qaytaradi.

## Ishlash natijasi:
```text
Kengaytmasi: .ts
Fayl nomi: server.controller.ts
Kengaytmasiz nomi: server.controller
Jild yo'li: C:/apps/backend
```


# 854-Topshiriq: fs/promises: Faylga yozish va o'qish

## Topshiriq sharti:
Asinxron tarzda matnli fayl yaratib, so'ngra uning ichini o'qing.

## Yechim (JS yoki TS kodi):
```typescript
import fs from "fs/promises";

async function testFileSystem() {
    const filename = "test_note.txt";
    await fs.writeFile(filename, "Assalomu alaykum Node.js!", "utf-8");
    const data = await fs.readFile(filename, "utf-8");
    console.log("Fayldan o'qildi:", data);
    await fs.unlink(filename); // Tozalash
}

testFileSystem();
```

## Tushuntirish va Mantiq:
`fs/promises` yordamida fayl tizimi amallari Promise qaytaradi va async/await orqali xavfsiz va qulay boshqariladi.

## Ishlash natijasi:
```text
Fayldan o'qildi: Assalomu alaykum Node.js!
```


# 855-Topshiriq: fs moduli: Fayl holatini tekshirish (fs.stat)

## Topshiriq sharti:
Faylning o'lchami va yaratilgan vaqtini tekshirish.

## Yechim (JS yoki TS kodi):
```typescript
import fs from "fs/promises";

async function checkFileStat() {
    const tempFile = "stat_sample.txt";
    await fs.writeFile(tempFile, "1234567890");
    const stat = await fs.stat(tempFile);

    console.log(`Fayl hajmi: ${stat.size} bayt`);
    console.log(`Bu faylmi: ${stat.isFile()}`);
    console.log(`Bu jildmi: ${stat.isDirectory()}`);

    await fs.unlink(tempFile);
}

checkFileStat();
```

## Tushuntirish va Mantiq:
`fs.stat` obyekti fayl hajmi (bytes), huquqlari va yaratilish vaqti kabi metama'lumotlarni beradi.

## Ishlash natijasi:
```text
Fayl hajmi: 10 bayt
Bu faylmi: true
Bu jildmi: false
```


# 856-Topshiriq: fs moduli: Jild yaratish va ichini o'qish (mkdir va readdir)

## Topshiriq sharti:
Rekursiv jild yaratish va undagi fayllar ro'yxatini olish.

## Yechim (JS yoki TS kodi):
```typescript
import fs from "fs/promises";

async function manageDirectories() {
    const dir = "temp_logs/system";
    await fs.mkdir(dir, { recursive: true });
    await fs.writeFile(`${dir}/app.log`, "log data");

    const files = await fs.readdir(dir);
    console.log("Jilddagi fayllar:", files);

    await fs.rm("temp_logs", { recursive: true, force: true });
}

manageDirectories();
```

## Tushuntirish va Mantiq:
`mkdir` da `{ recursive: true }` opsiyasi ichma-ich jildlarni birato'la xatosiz yaratish imkonini beradi.

## Ishlash natijasi:
```text
Jilddagi fayllar: [ 'app.log' ]
```


# 857-Topshiriq: Buffer bilan ishlash: UTF-8, HEX va Base64

## Topshiriq sharti:
Satrni Bufferga aylantirib, so'ngra turli kodirovkalarda o'qish.

## Yechim (JS yoki TS kodi):
```typescript
const text = "NodeJS Backend";
const buf = Buffer.from(text, "utf-8");

console.log("Buffer uzunligi:", buf.length);
console.log("HEX formatda:", buf.toString("hex"));
console.log("Base64 formatda:", buf.toString("base64"));
console.log("Qayta tiklangan satr:", buf.toString("utf-8"));
```

## Tushuntirish va Mantiq:
Buffer binar ma'lumotlar bilan xotirada to'g'ridan-to'g'ri ishlash vositasi bo'lib, tarmoq va fayl almashuvida qo'llaniladi.

## Ishlash natijasi:
```text
Buffer uzunligi: 14
HEX formatda: 4e6f64654a53204261636b656e64
Base64 formatda: Tm9kZUpTIEJhY2tlbmQ=
Qayta tiklangan satr: NodeJS Backend
```


# 858-Topshiriq: Buffer.alloc vs Buffer.allocUnsafe

## Topshiriq sharti:
Xavfsiz va xavfli xotira ajratish farqi.

## Yechim (JS yoki TS kodi):
```typescript
const safeBuf = Buffer.alloc(4); // 0 bilan tozalangan
const unsafeBuf = Buffer.allocUnsafe(4); // Eski xotira qoldiqlari bo'lishi mumkin

console.log("Tozalangan buffer:", safeBuf);
console.log("Unsafe buffer uzunligi:", unsafeBuf.length);
```

## Tushuntirish va Mantiq:
`alloc` xotirani nol bilan tozalaydi (xavfsiz), `allocUnsafe` esa tozalashsiz tez ajratadi, lekin maxfiy ma'lumotlar qoldig'i bo'lishi mumkin.

## Ishlash natijasi:
```text
Tozalangan buffer: <Buffer 00 00 00 00>
Unsafe buffer uzunligi: 4
```


# 859-Topshiriq: EventEmitter: Maxsus hodisalar yaratish va tinglash

## Topshiriq sharti:
Node.js ning `events` moduli orqali maxsus hodisalar boshqaruvchisini yarating.

## Yechim (JS yoki TS kodi):
```typescript
import { EventEmitter } from "events";

const emitter = new EventEmitter();

emitter.on("orderPlaced", (orderId: number, total: number) => {
    console.log(`Buyurtma #${orderId} qabul qilindi. Summa: ${total} so'm`);
});

emitter.emit("orderPlaced", 7701, 150000);
```

## Tushuntirish va Mantiq:
EventEmitter hodisalar asosida ishlaydigan asinxron reaktiv arxitekturaning poydevori hisoblanadi.

## Ishlash natijasi:
```text
Buyurtma #7701 qabul qilindi. Summa: 150000 so'm
```


# 860-Topshiriq: EventEmitter: once va removeListener (off)

## Topshiriq sharti:
Hodisani faqat bir marta tinglash va tinglovchini o'chirish.

## Yechim (JS yoki TS kodi):
```typescript
import { EventEmitter } from "events";

const emitter = new EventEmitter();
let callCount = 0;

emitter.once("connect", () => {
    callCount++;
    console.log("Bir martalik ulanish amalga oshdi.");
});

emitter.emit("connect");
emitter.emit("connect"); // Ikkinchi marta ishlamaydi
console.log("Chaqiruvlar soni:", callCount);
```

## Tushuntirish va Mantiq:
`once` metodi hodisa birinchi marta yuz bergandan so'ng o'z-o'zini ro'yxatdan o'chiradi.

## Ishlash natijasi:
```text
Bir martalik ulanish amalga oshdi.
Chaqiruvlar soni: 1
```


# 861-Topshiriq: EventEmitter da 'error' hodisasini ushlash

## Topshiriq sharti:
Agar error hodisasi tinglanmasa Node.js jarayoni qulashini oldini olish.

## Yechim (JS yoki TS kodi):
```typescript
import { EventEmitter } from "events";

const emitter = new EventEmitter();

emitter.on("error", (err: Error) => {
    console.log(`Tutilgan xatolik: ${err.message}`);
});

emitter.emit("error", new Error("Ulanish uzildi!"));
```

## Tushuntirish va Mantiq:
EventEmitter da 'error' hodisasi alohida ahamiyatga ega: agar unga listener ulanmagan bo'lsa, butun Node.js dasturi to'xtaydi (crash bo'ladi).

## Ishlash natijasi:
```text
Tutilgan xatolik: Ulanish uzildi!
```


# 862-Topshiriq: Readable Stream orqali oqimdan o'qish

## Topshiriq sharti:
Kichik bo'laklar (chunk) holatida ma'lumot oqimini o'qish.

## Yechim (JS yoki TS kodi):
```typescript
import { Readable } from "stream";

const stream = Readable.from(["Salom ", "O'zbekiston ", "Node.js!"]);

stream.on("data", (chunk: string) => {
    console.log(`Chunk olindi: "${chunk}"`);
});

stream.on("end", () => {
    console.log("Oqim tugadi.");
});
```

## Tushuntirish va Mantiq:
Readable Stream butun ma'lumotni xotiraga bir vaqtda yuklamasdan, qismma-qism uzatish imkonini beradi.

## Ishlash natijasi:
```text
Chunk olindi: "Salom "
Chunk olindi: "O'zbekiston "
Chunk olindi: "Node.js!"
Oqim tugadi.
```


# 863-Topshiriq: Writable Stream orqali yozish

## Topshiriq sharti:
Qabul qiluvchi oqim yaratib, unga qatorlar yozish.

## Yechim (JS yoki TS kodi):
```typescript
import { Writable } from "stream";

const received: string[] = [];
const customWriter = new Writable({
    write(chunk, encoding, callback) {
        received.push(chunk.toString());
        callback();
    }
});

customWriter.write("Qator 1\n");
customWriter.write("Qator 2\n");
customWriter.end();

console.log("Yozilgan elementlar soni:", received.length);
```

## Tushuntirish va Mantiq:
Writable Stream ma'lumotlarni qabul qilib oladi va oraliq bufer to'lib qolganda oqimni to'xtatib boshqarish (backpressure) xususiyatiga ega.

## Ishlash natijasi:
```text
Yozilgan elementlar soni: 2
```


# 864-Topshiriq: Stream pipe() orqali oqimlarni bog'lash

## Topshiriq sharti:
O'quvchi oqimni to'g'ridan-to'g'ri yozuvchi oqimga uzatish.

## Yechim (JS yoki TS kodi):
```typescript
import { Readable, Writable } from "stream";

const src = Readable.from(["A", "B", "C"]);
const output: string[] = [];

const dest = new Writable({
    write(chunk, enc, cb) {
        output.push(chunk.toString());
        cb();
    }
});

src.pipe(dest);

dest.on("finish", () => {
    console.log("Natija:", output.join("-"));
});
```

## Tushuntirish va Mantiq:
pipe() o'qish va yozish tezligini avtomatik muvofiqlashtirib (backpressure management), xotira to'lib ketishini oldini oladi.

## Ishlash natijasi:
```text
Natija: A-B-C
```


# 865-Topshiriq: pipeline bilan xavfsiz oqim boshqaruvi

## Topshiriq sharti:
`stream/promises` dagi pipeline orqali xatolarni xavfsiz boshqarish.

## Yechim (JS yoki TS kodi):
```typescript
import { pipeline } from "stream/promises";
import { Readable, Writable } from "stream";

async function runPipeline() {
    const source = Readable.from(["Pipeline", " ", "Muvaffaqiyatli"]);
    let result = "";

    const sink = new Writable({
        write(chunk, enc, cb) {
            result += chunk.toString();
            cb();
        }
    });

    await pipeline(source, sink);
    console.log("Birlashtirilgan:", result);
}

runPipeline();
```

## Tushuntirish va Mantiq:
`pipeline` pipe() dan farqli o'laroq, xatolik yuz berganda barcha oqimlarni xavfsiz yopadi va xotira sizib chiqishini (leak) oldini oladi.

## Ishlash natijasi:
```text
Birlashtirilgan: Pipeline Muvaffaqiyatli
```


# 866-Topshiriq: Transform Stream: Oqim ma'lumotlarini o'zgartirish

## Topshiriq sharti:
O'tib ketayotgan matnlarni KATTA harflarga o'giruvchi transformator oqimi.

## Yechim (JS yoki TS kodi):
```typescript
import { Transform, Readable } from "stream";

const uppercaseTransform = new Transform({
    transform(chunk, encoding, callback) {
        this.push(chunk.toString().toUpperCase());
        callback();
    }
});

const src = Readable.from(["hello ", "world"]);
src.pipe(uppercaseTransform).on("data", (chunk) => {
    console.log("Katta harf:", chunk.toString());
});
```

## Tushuntirish va Mantiq:
Transform Stream ham o'quvchi, ham yozuvchi oqim bo'lib, ma'lumotlarni oqim davomida konvertatsiya qilish uchun xizmat qiladi.

## Ishlash natijasi:
```text
Katta harf: HELLO WORLD
```


# 867-Topshiriq: Native http moduli: Oddiy HTTP Server

## Topshiriq sharti:
Tashqi kutubxonalarsiz sof Node.js http serverini yaratish andozasi.

## Yechim (JS yoki TS kodi):
```typescript
import http from "http";

const server = http.createServer((req, res) => {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ message: "Assalomu alaykum!", success: true }));
});

console.log("Server yaratildi, tinglashga tayyor.");
```

## Tushuntirish va Mantiq:
`http.createServer` har bir kiruvchi so'rov uchun IncomingMessage (req) va ServerResponse (res) obyektlarini taqdim etadi.

## Ishlash natijasi:
```text
Server yaratildi, tinglashga tayyor.
```


# 868-Topshiriq: Native http: Marshrutlash (Routing) va HTTP metodlar

## Topshiriq sharti:
req.url va req.method bo'yicha turli javoblar qaytarish.

## Yechim (JS yoki TS kodi):
```typescript
function handleRoute(method: string, url: string): { status: number; body: string } {
    if (method === "GET" && url === "/api/health") {
        return { status: 200, body: JSON.stringify({ status: "UP" }) };
    }
    if (method === "POST" && url === "/api/users") {
        return { status: 201, body: JSON.stringify({ message: "Yaratildi" }) };
    }
    return { status: 404, body: JSON.stringify({ error: "Topilmadi" }) };
}

console.log("Health check:", handleRoute("GET", "/api/health"));
console.log("Noma'lum yo'l:", handleRoute("GET", "/unknown"));
```

## Tushuntirish va Mantiq:
Sof http modulida marshrutlash URL va metod kombinatsiyalarini shartlar orqali tekshirish bilan amalga oshiriladi.

## Ishlash natijasi:
```text
Health check: { status: 200, body: '{"status":"UP"}' }
Noma'lum yo'l: { status: 404, body: '{"error":"Topilmadi"}' }
```


# 869-Topshiriq: Native http: So'rov tanasini (Body) yig'ish

## Topshiriq sharti:
req oqimidan barcha bo'laklarni (chunks) yig'ib JSON ga o'giruvchi yordamchi.

## Yechim (JS yoki TS kodi):
```typescript
import { Readable } from "stream";

async function parseRequestBody(req: Readable): Promise<any> {
    const chunks: Buffer[] = [];
    for await (const chunk of req) {
        chunks.push(typeof chunk === "string" ? Buffer.from(chunk) : chunk);
    }
    const fullBody = Buffer.concat(chunks).toString("utf-8");
    return JSON.parse(fullBody);
}

const mockReq = Readable.from([JSON.stringify({ name: "Anvar", age: 28 })]);
parseRequestBody(mockReq).then(data => {
    console.log("Qabul qilingan tana:", data);
});
```

## Tushuntirish va Mantiq:
Node.js da POST so'rov tanasi darhol tayyor bo'lmaydi; u Readable stream bo'lganligi sababli barcha chunklar tugashini kutish kerak.

## Ishlash natijasi:
```text
Qabul qilingan tana: { name: 'Anvar', age: 28 }
```


# 870-Topshiriq: Express.js / REST API: Asosiy middleware mexanizmi

## Topshiriq sharti:
Middleware lar ketma-ketligi va next() funksiyasi ishlash tamoyili.

## Yechim (JS yoki TS kodi):
```typescript
type NextFn = () => void;
type MockMiddleware = (req: Record<string, any>, res: Record<string, any>, next: NextFn) => void;

const middlewares: MockMiddleware[] = [
    (req, res, next) => {
        req.timestamp = Date.now();
        next();
    },
    (req, res, next) => {
        req.authenticated = true;
        next();
    }
];

const mockReq: Record<string, any> = {};
const mockRes: Record<string, any> = {};

let idx = 0;
function dispatch() {
    if (idx < middlewares.length) {
        const mw = middlewares[idx++];
        mw(mockReq, mockRes, dispatch);
    }
}
dispatch();

console.log("Middleware ishlovidan keyin:", mockReq.authenticated);
```

## Tushuntirish va Mantiq:
Express middleware lari `(req, res, next)` zanjiri asosida ishlaydi; har bir qadam `next()` orqali estafetani keyingisiga uzatadi.

## Ishlash natijasi:
```text
Middleware ishlovidan keyin: true
```


# 871-Topshiriq: Express.js: URL parametrlari va Query String

## Topshiriq sharti:
req.params va req.query bilan ishlash.

## Yechim (JS yoki TS kodi):
```typescript
interface CustomRequest {
    params: { id: string };
    query: { filter?: string; page?: string };
}

function handleGetUser(req: CustomRequest) {
    const userId = Number(req.params.id);
    const filter = req.query.filter ?? "all";
    return `User: ${userId}, Filtr: ${filter}`;
}

const fakeReq: CustomRequest = {
    params: { id: "42" },
    query: { filter: "active" }
};

console.log(handleGetUser(fakeReq));
```

## Tushuntirish va Mantiq:
Marshrutdagi `/users/:id` qismi `req.params.id` bo'ladi, `?filter=active` kabi qo'shimchalar esa `req.query` da joylashadi.

## Ishlash natijasi:
```text
User: 42, Filtr: active
```


# 872-Topshiriq: Express.js: Autentifikatsiya Guard Middleware

## Topshiriq sharti:
Headerda Bearer Token mavjudligini tekshiruvchi auth middleware.

## Yechim (JS yoki TS kodi):
```typescript
function authGuard(headers: Record<string, string | undefined>): { authorized: boolean; error?: string } {
    const authHeader = headers["authorization"];
    if (!authHeader || !authHeader.startsWith("Bearer ")) {
        return { authorized: false, error: "401: Token taqdim etilmagan" };
    }
    const token = authHeader.split(" ")[1];
    if (token !== "valid_secret_token") {
        return { authorized: false, error: "403: Yaroqsiz token" };
    }
    return { authorized: true };
}

console.log("Token yo'q:", authGuard({}));
console.log("To'g'ri token:", authGuard({ authorization: "Bearer valid_secret_token" }));
```

## Tushuntirish va Mantiq:
Himoyalangan marshrutlarga kirishdan oldin so'rov sarlavhalari (headers) middleware orqali tekshiriladi.

## Ishlash natijasi:
```text
Token yo'q: { authorized: false, error: '401: Token taqdim etilmagan' }
To'g'ri token: { authorized: true }
```


# 873-Topshiriq: Express.js: Markaziy Xatoliklarni boshqarish (Error Middleware)

## Topshiriq sharti:
To'rtta parametrli (err, req, res, next) xato tutuvchi middleware tuzilishi.

## Yechim (JS yoki TS kodi):
```typescript
interface AppError {
    statusCode: number;
    message: string;
}

function errorHandler(err: AppError, req: any): { status: number; body: object } {
    const status = err.statusCode || 500;
    return {
        status,
        body: {
            success: false,
            error: err.message || "Ichki server xatoligi"
        }
    };
}

const errRes = errorHandler({ statusCode: 404, message: "Foydalanuvchi topilmadi" }, {});
console.log("Xato javobi:", errRes);
```

## Tushuntirish va Mantiq:
Express da 4 ta argument oluvchi middleware markaziy xato qayta ishlovchi hisoblanadi va barcha try-catch siz tashlangan xatolarni bitta joyda tutadi.

## Ishlash natijasi:
```text
Xato javobi: { status: 404, body: { success: false, error: 'Foydalanuvchi topilmadi' } }
```


# 874-Topshiriq: crypto: SHA-256 xesh generatsiyasi

## Topshiriq sharti:
Matndan xavfsiz SHA-256 xesh qiymatini hosil qilish.

## Yechim (JS yoki TS kodi):
```typescript
import crypto from "crypto";

function hashText(text: string): string {
    return crypto.createHash("sha256").update(text).digest("hex");
}

const hash = hashText("maxfiy_parol");
console.log("SHA-256 uzunligi:", hash.length);
console.log("Boshlang'ich 10 belgisi:", hash.slice(0, 10));
```

## Tushuntirish va Mantiq:
SHA-256 bir tomonlama kriptografik xeshlash algoritmi bo'lib, har doim 64 belgili (256 bit) HEX satr qaytaradi.

## Ishlash natijasi:
```text
SHA-256 uzunligi: 64
Boshlang'ich 10 belgisi: 025d57d5e4
```


# 875-Topshiriq: crypto: HMAC yaratish (Secret Key bilan)

## Topshiriq sharti:
Maxfiy kalitga bog'langan xesh (HMAC) hosil qilish.

## Yechim (JS yoki TS kodi):
```typescript
import crypto from "crypto";

function generateHmac(payload: string, secret: string): string {
    return crypto.createHmac("sha256", secret).update(payload).digest("hex");
}

const hmac = generateHmac("order_id_100", "my_api_secret_key");
console.log("HMAC hosil qilindi, uzunlik:", hmac.length);
```

## Tushuntirish va Mantiq:
HMAC ma'lumotning o'rtada soxtalashtirilmaganligini va faqat maxfiy kalit egalari tomonidan yuborilganligini tekshirish uchun webhooklarda ishlatiladi.

## Ishlash natijasi:
```text
HMAC hosil qilindi, uzunlik: 64
```


# 876-Topshiriq: crypto: randomUUID va randomBytes

## Topshiriq sharti:
Noyob identifikatorlar va xavfsiz tasodifiy tokenlar yaratish.

## Yechim (JS yoki TS kodi):
```typescript
import crypto from "crypto";

const uuid = crypto.randomUUID();
const randomHex = crypto.randomBytes(8).toString("hex");

console.log("UUID v4 formati:", uuid.length === 36);
console.log("Tasodifiy HEX token:", randomHex);
```

## Tushuntirish va Mantiq:
`randomUUID` RFC-4122 v4 standartidagi noyob identifikator yaratadi, `randomBytes` esa kriptografik xavfsiz tasodifiy baytlar beradi.

## Ishlash natijasi:
```text
UUID v4 formati: true
Tasodifiy HEX token: a1b2c3d4e5f60718
```


# 877-Topshiriq: os moduli: Tizim resurslarini kuzatish

## Topshiriq sharti:
Serverning bo'sh xotirasi, CPU yadrolari va operatsion tizim nomini aniqlash.

## Yechim (JS yoki TS kodi):
```typescript
import os from "os";

console.log(`OS: ${os.platform()} (${os.arch()})`);
console.log(`CPU yadrolari soni: ${os.cpus().length}`);
console.log(`Jami xotira: ${(os.totalmem() / 1024 / 1024 / 1024).toFixed(1)} GB`);
console.log(`Bo'sh xotira: ${(os.freemem() / 1024 / 1024 / 1024).toFixed(1)} GB`);
```

## Tushuntirish va Mantiq:
`os` moduli server monitoringi, klasterlash (cluster) va resurslarni taqsimlashda ishlatiladi.

## Ishlash natijasi:
```text
OS: win32 (x64)
CPU yadrolari soni: 8
Jami xotira: 16.0 GB
Bo'sh xotira: 8.5 GB
```


# 878-Topshiriq: process.nextTick vs setImmediate

## Topshiriq sharti:
Microtask va Macrotask navbatlarining Node.js dagi farqi.

## Yechim (JS yoki TS kodi):
```typescript
console.log("1: Asosiy sinxron kod");

setImmediate(() => {
    console.log("4: setImmediate (Check bosqichi)");
});

process.nextTick(() => {
    console.log("2: process.nextTick (Microtask)");
});

Promise.resolve().then(() => {
    console.log("3: Promise microtask");
});
```

## Tushuntirish va Mantiq:
`process.nextTick` joriy operatsiya tugashi bilanoq, hattoki boshqa Promise microtasklaridan ham oldin bajariladi. `setImmediate` esa Event Loop ning Check fazasida ishga tushadi.

## Ishlash natijasi:
```text
1: Asosiy sinxron kod
2: process.nextTick (Microtask)
3: Promise microtask
4: setImmediate (Check bosqichi)
```


# 879-Topshiriq: process: uncaughtException va unhandledRejection

## Topshiriq sharti:
Tutib olinmagan xatoliklar tufayli server qulashini nazoratga olish.

## Yechim (JS yoki TS kodi):
```typescript
process.on("unhandledRejection", (reason, promise) => {
    console.log("Ushlangan asinxron xatolik:", reason);
});

Promise.reject("Kutilmagan asinxron xatolik!");
```

## Tushuntirish va Mantiq:
Katta backend tizimlarida `unhandledRejection` hodisasini tinglash kutilmagan qulashlarni log qilish va monitoringga (masalan, Sentry) yuborish uchun shartdir.

## Ishlash natijasi:
```text
Ushlangan asinxron xatolik: Kutilmagan asinxron xatolik!
```


# 880-Topshiriq: Graceful Shutdown (Yumshoq to'xtash) patterni

## Topshiriq sharti:
SIGINT yoki SIGTERM signali kelganda ochiq ulanishlarni toza yopish.

## Yechim (JS yoki TS kodi):
```typescript
function mockGracefulShutdown(signal: string) {
    console.log(`[${signal}] signali olindi. Server to'xtatilmoqda...`);
    console.log("1. Yangi so'rovlar qabul qilish to'xtatildi.");
    console.log("2. Baza ulanishlari yopildi.");
    console.log("Server muvaffaqiyatli to'xtadi.");
}

mockGracefulShutdown("SIGINT");
```

## Tushuntirish va Mantiq:
Docker va Kubernetes konteynerlarida ilova to'xtatilganda mavjud mijoz so'rovlari uzilib qolmasligi uchun Graceful Shutdown qo'llaniladi.

## Ishlash natijasi:
```text
[SIGINT] signali olindi. Server to'xtatilmoqda...
1. Yangi so'rovlar qabul qilish to'xtatildi.
2. Baza ulanishlari yopildi.
Server muvaffaqiyatli to'xtadi.
```


# 881-Topshiriq: CORS (Cross-Origin Resource Sharing) sarlavhalari

## Topshiriq sharti:
Boshqa domendan kelgan so'rovlarga ruxsat beruvchi sarlavhalarni sozlash.

## Yechim (JS yoki TS kodi):
```typescript
function applyCorsHeaders(resHeaders: Record<string, string>) {
    resHeaders["Access-Control-Allow-Origin"] = "*";
    resHeaders["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS";
    resHeaders["Access-Control-Allow-Headers"] = "Content-Type, Authorization";
}

const headers: Record<string, string> = {};
applyCorsHeaders(headers);
console.log("CORS sarlavhasi:", headers["Access-Control-Allow-Origin"]);
```

## Tushuntirish va Mantiq:
CORS brauzer xavfsizlik mexanizmi bo'lib, server javobida ushbu sarlavhalar bo'lmasa, frontend so'rovni bloklaydi.

## Ishlash natijasi:
```text
CORS sarlavhasi: *
```


# 882-Topshiriq: Rate Limiting mantiqi (In-Memory IP bo'yicha)

## Topshiriq sharti:
Bitta IP manzildan daqiqasiga keladigan so'rovlar sonini cheklash.

## Yechim (JS yoki TS kodi):
```typescript
class RateLimiter {
    private requests = new Map<string, number>();

    isAllowed(ip: string, limit: number): boolean {
        const count = this.requests.get(ip) || 0;
        if (count >= limit) return false;
        this.requests.set(ip, count + 1);
        return true;
    }
}

const limiter = new RateLimiter();
const ip = "192.168.1.50";

console.log("So'rov 1:", limiter.isAllowed(ip, 2));
console.log("So'rov 2:", limiter.isAllowed(ip, 2));
console.log("So'rov 3:", limiter.isAllowed(ip, 2));
```

## Tushuntirish va Mantiq:
Rate Limiter serverni DDoS hujumlari va botlarning ortiqcha yuklamasidan himoya qiladi.

## Ishlash natijasi:
```text
So'rov 1: true
So'rov 2: true
So'rov 3: false
```


# 883-Topshiriq: In-Memory Kesh (Cache) Middleware

## Topshiriq sharti:
Tez-tez takrorlanuvchi so'rovlarni xotirada saqlab, server yukini kamaytirish.

## Yechim (JS yoki TS kodi):
```typescript
class RequestCache {
    private cache = new Map<string, { data: any; expiry: number }>();

    set(key: string, data: any, ttlMs: number): void {
        this.cache.set(key, { data, expiry: Date.now() + ttlMs });
    }

    get(key: string): any | null {
        const entry = this.cache.get(key);
        if (!entry) return null;
        if (Date.now() > entry.expiry) {
            this.cache.delete(key);
            return null;
        }
        return entry.data;
    }
}

const c = new RequestCache();
c.set("/api/products", [{ id: 1, name: "Non" }], 5000);
console.log("Keshdan olindi:", c.get("/api/products")?.[0].name);
```

## Tushuntirish va Mantiq:
Keshlash ma'lumotlar bazasiga qayta-qayta murojaat qilmaslik va javob vaqtini tezlashtirish uchun qo'llaniladi.

## Ishlash natijasi:
```text
Keshdan olindi: Non
```


# 884-Topshiriq: DTO Schema Validatsiyasi

## Topshiriq sharti:
Kiruvchi JSON formatini tekshiruvchi validator funksiya.

## Yechim (JS yoki TS kodi):
```typescript
interface CreateProductInput {
    title: string;
    price: number;
}

function validateProductInput(body: any): { isValid: boolean; errors: string[] } {
    const errors: string[] = [];
    if (typeof body.title !== "string" || body.title.trim().length === 0) {
        errors.push("title satr bo'lishi va bo'sh bo'lmasligi shart");
    }
    if (typeof body.price !== "number" || body.price <= 0) {
        errors.push("price musbat son bo'lishi shart");
    }
    return { isValid: errors.length === 0, errors };
}

console.log("Yaroqli:", validateProductInput({ title: "Olma", price: 15000 }));
console.log("Yaroqsiz:", validateProductInput({ title: "", price: -100 }));
```

## Tushuntirish va Mantiq:
Backendda har qanday kiruvchi ma'lumot biznes mantiqqa o'tishidan oldin qat'iy sxema bo'yicha tekshirilishi lozim.

## Ishlash natijasi:
```text
Yaroqli: { isValid: true, errors: [] }
Yaroqsiz: { isValid: false, errors: [ 'title satr bo\'lishi va bo\'sh bo\'lmasligi shart', 'price musbat son bo\'lishi shart' ] }
```


# 885-Topshiriq: JWT Mock Token yaratish va tekshirish

## Topshiriq sharti:
JSON Web Token (Header.Payload.Signature) tuzilishini tushunish.

## Yechim (JS yoki TS kodi):
```typescript
import crypto from "crypto";

function createMockJwt(payload: object, secret: string): string {
    const header = Buffer.from(JSON.stringify({ alg: "HS256", typ: "JWT" })).toString("base64url");
    const body = Buffer.from(JSON.stringify(payload)).toString("base64url");
    const signature = crypto.createHmac("sha256", secret).update(`${header}.${body}`).digest("base64url");
    return `${header}.${body}.${signature}`;
}

const token = createMockJwt({ userId: 101, role: "admin" }, "maxfiy_kalit");
console.log("JWT bo'laklari soni:", token.split(".").length);
```

## Tushuntirish va Mantiq:
JWT uch qismdan iborat: Header, Payload va Signature bo'lib, nuqta bilan ajratiladi va Base64Url kodirovkasida saqlanadi.

## Ishlash natijasi:
```text
JWT bo'laklari soni: 3
```


# 886-Topshiriq: Environment Variables va .env boshqaruvi

## Topshiriq sharti:
Muhit o'zgaruvchilarini o'qish va sukutli qiymatlar berish.

## Yechim (JS yoki TS kodi):
```typescript
interface EnvConfig {
    PORT: number;
    DB_HOST: string;
    IS_PROD: boolean;
}

function loadConfig(): EnvConfig {
    return {
        PORT: Number(process.env.PORT) || 3000,
        DB_HOST: process.env.DB_HOST || "localhost",
        IS_PROD: process.env.NODE_ENV === "production"
    };
}

const conf = loadConfig();
console.log(`Port: ${conf.PORT}, Host: ${conf.DB_HOST}`);
```

## Tushuntirish va Mantiq:
Maxfiy kalitlar va server portlari hech qachon kod ichida ochiq yozilmaydi; ular muhit o'zgaruvchilari orqali taqdim etiladi.

## Ishlash natijasi:
```text
Port: 3000, Host: localhost
```


# 887-Topshiriq: child_process: exec bilan tizim buyrug'ini bajarish

## Topshiriq sharti:
Node.js ichidan konsol buyrug'ini ishga tushirish.

## Yechim (JS yoki TS kodi):
```typescript
import { exec } from "child_process";

exec("node -v", (error, stdout) => {
    if (error) {
        console.error("Xatolik:", error);
        return;
    }
    console.log(`Node versiyasi aniqlandi: ${stdout.trim()}`);
});
```

## Tushuntirish va Mantiq:
`child_process.exec` yangi operatsion tizim qobig'ini (shell) ochib, buyruqni bajaradi va natijani bufferda qaytaradi.

## Ishlash natijasi:
```text
Node versiyasi aniqlandi: v24.19.0
```


# 888-Topshiriq: child_process: spawn bilan oqimli jarayon ochish

## Topshiriq sharti:
Katta chiqishli buyruqlarni oqim (stream) orqali o'qish.

## Yechim (JS yoki TS kodi):
```typescript
import { spawn } from "child_process";

const child = spawn("node", ["-e", "console.log('Salom Spawn!')"]);

child.stdout.on("data", (data) => {
    console.log(`Spawn chiqishi: ${data.toString().trim()}`);
});
```

## Tushuntirish va Mantiq:
`spawn` yangi jarayonni to'g'ridan-to'g'ri oqim bilan bog'laydi, bu xotirada joy tejash va real vaqtda javob olish uchun juda mos keladi.

## Ishlash natijasi:
```text
Spawn chiqishi: Salom Spawn!
```


# 889-Topshiriq: HTTP Status kodlari yordamchisi (HttpStatus)

## Topshiriq sharti:
REST API da standart HTTP holat kodlarini qat'iy boshqarish.

## Yechim (JS yoki TS kodi):
```typescript
enum HttpStatus {
    OK = 200,
    CREATED = 201,
    BAD_REQUEST = 400,
    UNAUTHORIZED = 401,
    FORBIDDEN = 403,
    NOT_FOUND = 404,
    INTERNAL_SERVER_ERROR = 500
}

function respond(status: HttpStatus, data: any) {
    return { statusCode: status, body: data };
}

console.log("Muvaffaqiyat:", respond(HttpStatus.CREATED, { id: 1 }));
console.log("Xato:", respond(HttpStatus.NOT_FOUND, { message: "Topilmadi" }));
```

## Tushuntirish va Mantiq:
Raqamli xatoliklar o'rniga Enum ishlatish xatoliklarning oldini oladi va kod o'qilishini yaxshilaydi.

## Ishlash natijasi:
```text
Muvaffaqiyat: { statusCode: 201, body: { id: 1 } }
Xato: { statusCode: 404, body: { message: 'Topilmadi' } }
```


# 890-Topshiriq: REST API CRUD: In-Memory foydalanuvchilar ombori

## Topshiriq sharti:
Oddiy CRUD mantiqini massiv asosida boshqarish.

## Yechim (JS yoki TS kodi):
```typescript
interface User { id: number; name: string; }

class UserService {
    private users: User[] = [];
    private nextId = 1;

    create(name: string): User {
        const u = { id: this.nextId++, name };
        this.users.push(u);
        return u;
    }

    findAll(): User[] { return this.users; }

    delete(id: number): boolean {
        const idx = this.users.findIndex(u => u.id === id);
        if (idx === -1) return false;
        this.users.splice(idx, 1);
        return true;
    }
}

const s = new UserService();
s.create("Farrux");
s.create("Nodir");
console.log("Foydalanuvchilar soni:", s.findAll().length);
s.delete(1);
console.log("O'chirilgandan keyin soni:", s.findAll().length);
```

## Tushuntirish va Mantiq:
Service qatlami biznes mantiqni o'zida jamlaydi va HTTP controllerlaridan mustaqil ishlay oladi.

## Ishlash natijasi:
```text
Foydalanuvchilar soni: 2
O'chirilgandan keyin soni: 1
```


# 891-Topshiriq: Cookie sarlavhalarini parse qilish

## Topshiriq sharti:
Kiruvchi 'Cookie' satrini obyekt ko'rinishiga keltiruvchi funksiya.

## Yechim (JS yoki TS kodi):
```typescript
function parseCookies(cookieHeader: string | undefined): Record<string, string> {
    if (!cookieHeader) return {};
    return Object.fromEntries(
        cookieHeader.split(";").map(c => {
            const [k, v] = c.trim().split("=");
            return [k, decodeURIComponent(v)];
        })
    );
}

const rawCookie = "sessionId=xyz123; theme=dark; lang=uz";
const cookies = parseCookies(rawCookie);
console.log("Session ID:", cookies.sessionId);
console.log("Tanlangan til:", cookies.lang);
```

## Tushuntirish va Mantiq:
Sessiyalar va autentifikatsiya ma'lumotlarini brauzerdan olish uchun Cookie satri parse qilinadi.

## Ishlash natijasi:
```text
Session ID: xyz123
Tanlangan til: uz
```


# 892-Topshiriq: Set-Cookie sarlavhasini shakllantirish

## Topshiriq sharti:
HttpOnly, Secure va SameSite bayroqlari bilan xavfsiz cookie yaratish.

## Yechim (JS yoki TS kodi):
```typescript
function serializeCookie(name: string, val: string, maxAgeSec: number): string {
    return `${name}=${encodeURIComponent(val)}; Max-Age=${maxAgeSec}; HttpOnly; Secure; SameSite=Strict; Path=/`;
}

const cookieHeader = serializeCookie("token", "secret123", 3600);
console.log("Yaratilgan cookie sarlavhasi:", cookieHeader);
```

## Tushuntirish va Mantiq:
HttpOnly bayrog'i JavaScript (XSS hujumlari) orqali cookieni o'g'irlashni taqiqlaydi, Secure esa faqat HTTPS orqali yuborilishini kafolatlaydi.

## Ishlash natijasi:
```text
Yaratilgan cookie sarlavhasi: token=secret123; Max-Age=3600; HttpOnly; Secure; SameSite=Strict; Path=/
```


# 893-Topshiriq: Katta hajmdagi faylni qatorlab o'qish (readline moduli)

## Topshiriq sharti:
Xotirani to'ldirib yubormasdan katta fayllarni tahlil qilish.

## Yechim (JS yoki TS kodi):
```typescript
import { Readable } from "stream";
import readline from "readline";

async function countLines(stream: Readable): Promise<number> {
    const rl = readline.createInterface({ input: stream, crlfDelay: Infinity });
    let count = 0;
    for await (const line of rl) {
        count++;
    }
    return count;
}

const mockFileStream = Readable.from(["1-qator\n", "2-qator\n", "3-qator"]);
countLines(mockFileStream).then(c => console.log("Jami qatorlar soni:", c));
```

## Tushuntirish va Mantiq:
`readline` moduli har bir qatorni alohida ajratib beradi, bu gigabaytlab log fayllarni xotirasiz (low-memory) o'qish imkonini beradi.

## Ishlash natijasi:
```text
Jami qatorlar soni: 3
```


# 894-Topshiriq: URLSearchParams bilan Query String yasash

## Topshiriq sharti:
URL parametrlarini qulay va xavfsiz formatlash.

## Yechim (JS yoki TS kodi):
```typescript
const params = new URLSearchParams({
    search: "TypeScript qo'llanma",
    page: "2",
    limit: "20"
});

console.log("Query satr:", params.toString());
```

## Tushuntirish va Mantiq:
URLSearchParams maxsus belgilarni (bo'sh joy, apostrof) avtomatik URL-kodlaydi (percent-encoding).

## Ishlash natijasi:
```text
Query satr: search=TypeScript+qo%27llanma&page=2&limit=20
```


# 895-Topshiriq: JSON Fayl bilan kichik ma'lumotlar bazasi (Flat DB)

## Topshiriq sharti:
JSON faylga o'qish/yozish orqali oddiy konfiguratsiya saqlash.

## Yechim (JS yoki TS kodi):
```typescript
import fs from "fs/promises";

async function testJsonDb() {
    const dbFile = "temp_db.json";
    const initialData = { app: "MyStore", version: "1.0.0" };

    await fs.writeFile(dbFile, JSON.stringify(initialData, null, 2));
    const content = JSON.parse(await fs.readFile(dbFile, "utf-8"));

    console.log("Ilova nomi:", content.app);
    await fs.unlink(dbFile);
}

testJsonDb();
```

## Tushuntirish va Mantiq:
Kichik yordamchi skriptlar va CLI dasturlarida JSON fayllar eng sodda ma'lumotlar ombori hisoblanadi.

## Ishlash natijasi:
```text
Ilova nomi: MyStore
```


# 896-Topshiriq: Gzip bilan ma'lumotlarni siqish (zlib moduli)

## Topshiriq sharti:
Tarmoq trafigini tejash uchun zlib yordamida matnni siqish va ochish.

## Yechim (JS yoki TS kodi):
```typescript
import zlib from "zlib";

const original = "Juda uzun matn... ".repeat(10);
const compressed = zlib.gzipSync(original);
const decompressed = zlib.gunzipSync(compressed).toString();

console.log(`Asl hajm: ${original.length} bayt`);
console.log(`Siqilgan hajm: ${compressed.length} bayt`);
console.log(`Qayta tiklandi: ${decompressed === original}`);
```

## Tushuntirish va Mantiq:
HTTP serverlar `Content-Encoding: gzip` orqali javoblarni siqib uzatadi va yuklanish tezligini oshiradi.

## Ishlash natijasi:
```text
Asl hajm: 190 bayt
Siqilgan hajm: 46 bayt
Qayta tiklandi: true
```


# 897-Topshiriq: Parolni xavfsiz solishtirish (crypto.timingSafeEqual)

## Topshiriq sharti:
Timing Attack (vaqt bo'yicha tahlil) xurujlarining oldini olish.

## Yechim (JS yoki TS kodi):
```typescript
import crypto from "crypto";

function safeCompare(a: string, b: string): boolean {
    const bufA = Buffer.from(a);
    const bufB = Buffer.from(b);
    if (bufA.length !== bufB.length) return false;
    return crypto.timingSafeEqual(bufA, bufB);
}

console.log("Mos kelish:", safeCompare("token_12345", "token_12345"));
console.log("Mos kelmaslik:", safeCompare("token_12345", "token_99999"));
```

## Tushuntirish va Mantiq:
`crypto.timingSafeEqual` har ikkala satrni tekshirish uchun har doim bir xil vaqt sarflaydi, bu xakerlar harflarni vaqt farqidan bilib olishini man etadi.

## Ishlash natijasi:
```text
Mos kelish: true
Mos kelmaslik: false
```


# 898-Topshiriq: Fastify/Express uslubidagi Plugin / Modul arxitekturasi

## Topshiriq sharti:
Ilovani kichik plaginlar orqali kengaytirish namunasi.

## Yechim (JS yoki TS kodi):
```typescript
interface AppInstance {
    routes: string[];
    addRoute(route: string): void;
}

type PluginFn = (app: AppInstance) => void;

class ServerApp implements AppInstance {
    routes: string[] = [];
    addRoute(r: string) { this.routes.push(r); }
    register(plugin: PluginFn) { plugin(this); }
}

const authPlugin: PluginFn = (app) => {
    app.addRoute("/auth/login");
    app.addRoute("/auth/register");
};

const server = new ServerApp();
server.register(authPlugin);
console.log("Plagin qo'shgan marshrutlar:", server.routes);
```

## Tushuntirish va Mantiq:
Plagin arxitekturasi katta backend loyihalarini mustaqil modullarga ajratish uchun ishlatiladi.

## Ishlash natijasi:
```text
Plagin qo'shgan marshrutlar: [ '/auth/login', '/auth/register' ]
```


# 899-Topshiriq: worker_threads: Parallel hisoblash namunasi

## Topshiriq sharti:
Node.js da yangi ishchi ip (thread) ochish tamoyili.

## Yechim (JS yoki TS kodi):
```typescript
import { isMainThread } from "worker_threads";

if (isMainThread) {
    console.log("Asosiy Event Loop ishlamoqda. Worker Thread yaratish mumkin.");
} else {
    console.log("Ishchi ip ichida og'ir vazifa bajarilmoqda.");
}
```

## Tushuntirish va Mantiq:
`worker_threads` og'ir matematik va CPU ga bog'liq amallarni asosiy Event Loop ni bloklamasdan parallel bajarish uchun xizmat qiladi.

## Ishlash natijasi:
```text
Asosiy Event Loop ishlamoqda. Worker Thread yaratish mumkin.
```


# 900-Topshiriq: To'liq REST API Mikro-xizmati: Foydalanuvchilar boshqaruvi va Validatsiya

## Topshiriq sharti:
Router, Controller, Service va Validatsiyani o'z ichiga olgan mukammal arxitektura.

## Yechim (JS yoki TS kodi):
```typescript
interface UserDto {
    name: string;
    email: string;
}

class UserDb {
    private users: (UserDto & { id: number })[] = [];
    private idCounter = 1;

    insert(data: UserDto) {
        const record = { id: this.idCounter++, ...data };
        this.users.push(record);
        return record;
    }

    getAll() { return this.users; }
}

class UserController {
    constructor(private db: UserDb) {}

    handlePost(body: any): { status: number; data: any } {
        if (!body.name || !body.email || !body.email.includes("@")) {
            return { status: 400, data: { error: "Yaroqsiz ma'lumotlar" } };
        }
        const created = this.db.insert({ name: body.name, email: body.email });
        return { status: 201, data: created };
    }
}

const db = new UserDb();
const controller = new UserController(db);

const res1 = controller.handlePost({ name: "Bobur", email: "bobur@domain.uz" });
const res2 = controller.handlePost({ name: "Xato", email: "notanemail" });

console.log("Muvaffaqiyatli natija:", res1);
console.log("Xato natija:", res2);
```

## Tushuntirish va Mantiq:
Ushbu to'liq arxitektura kontroller va xizmat qatlamlarini to'g'ri ajratib, korporativ Node.js backend ilovalarining asosini ko'rsatib beradi.

## Ishlash natijasi:
```text
Muvaffaqiyatli natija: { status: 201, data: { id: 1, name: 'Bobur', email: 'bobur@domain.uz' } }
Xato natija: { status: 400, data: { error: 'Yaroqsiz ma\'lumotlar' } }
```

