# 601-Topshiriq: Funksiya parametr va qaytish tiplarini aniqlash

## Topshiriq sharti:
Ikki sonni qo'shuvchi oddiy funksiya yarating va uning parametrlari hamda qaytish qiymati tipini number sifatida belgilang.

## Yechim (JS yoki TS kodi):
```typescript
function add(a: number, b: number): number {
    return a + b;
}

const res: number = add(15, 25);
console.log(`Yig'indi: ${res}`);
```

## Tushuntirish va Mantiq:
TypeScript da funksiya parametrlari va uning natijasi qaytish tipi (return type) aniq ko'rsatiladi. Bu xato tiplar berilishining oldini oladi.

## Ishlash natijasi:
```text
Yig'indi: 40
```


# 602-Topshiriq: Ixtiyoriy parametrlar (Optional Parameters)

## Topshiriq sharti:
Foydalanuvchi ismi va ixtiyoriy unvonini qabul qilib, salomlashish matnini qaytaruvchi funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
function greet(name: string, title?: string): string {
    if (title) {
        return `Assalomu alaykum, ${title} ${name}!`;
    }
    return `Salom, ${name}!`;
}

console.log(greet("Ali"));
console.log(greet("Vali", "Muhandis"));
```

## Tushuntirish va Mantiq:
Parametr nomidan keyin '?' belgisi qo'yilsa, u ixtiyoriy parametr hisoblanadi va uning tipi avtomatik 'type | undefined' bo'ladi. Ixtiyoriy parametrlar majburiy parametrlardan keyin kelishi shart.

## Ishlash natijasi:
```text
Salom, Ali!
Assalomu alaykum, Muhandis Vali!
```


# 603-Topshiriq: Standart qiymatli parametrlar (Default Parameters)

## Topshiriq sharti:
Xarid summasiga chegirma hisoblovchi funksiya yozing. Chegirma foizi berilmasa, sukut bo'yicha 5% deb olinsin.

## Yechim (JS yoki TS kodi):
```typescript
function calculateDiscount(price: number, discountPercent: number = 5): number {
    return price - (price * discountPercent) / 100;
}

console.log(calculateDiscount(100));
console.log(calculateDiscount(100, 20));
```

## Tushuntirish va Mantiq:
Standart qiymat berilganda TypeScript uning tipini avtomatik chiqaradi (type inference). Bunday parametrlar ixtiyoriy hisoblanadi.

## Ishlash natijasi:
```text
95
80
```


# 604-Topshiriq: Rest parametrlari (Rest Parameters) typing

## Topshiriq sharti:
Ixtiyoriy sondagi sonlarni qabul qilib, ularning o'rtacha qiymatini hisoblovchi funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
function average(...scores: number[]): number {
    if (scores.length === 0) return 0;
    const sum = scores.reduce((acc, curr) => acc + curr, 0);
    return sum / scores.length;
}

console.log(average(10, 20, 30, 40));
console.log(average(85, 90, 95));
```

## Tushuntirish va Mantiq:
Rest parametrlar (...args) massiv ko'rinishida yoziladi va ularga aniq massiv tipi (masalan, number[]) biriktiriladi.

## Ishlash natijasi:
```text
25
90
```


# 605-Topshiriq: Rest parametrlarida Tuple qo'llash

## Topshiriq sharti:
Birinchi elementi string (buyruq nomi), ikkinchi va uchinchi elementlari esa number bo'lgan aniq o'lchamli rest parametrli funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
function executeCommand(...args: [string, number, number]): void {
    const [action, x, y] = args;
    console.log(`Harakat: ${action}, Koordinatalar: (${x}, ${y})`);
}

executeCommand("MOVE_TO", 100, 250);
```

## Tushuntirish va Mantiq:
Rest parametrlarga tuple tipi berilsa, funksiya argumentlari soni va har bir pozitsiyadagi tipi qat'iy nazorat qilinadi.

## Ishlash natijasi:
```text
Harakat: MOVE_TO, Koordinatalar: (100, 250)
```


# 606-Topshiriq: Funksiya tipi taxallusi (Function Type Alias)

## Topshiriq sharti:
Matematik operatsiya uchun funksiya tipi taxallusi (MathOperation) yarating va uni amalga oshiring.

## Yechim (JS yoki TS kodi):
```typescript
type MathOperation = (x: number, y: number) => number;

const multiply: MathOperation = (a, b) => a * b;
const subtract: MathOperation = (a, b) => a - b;

console.log(`Ko'paytirish: ${multiply(6, 7)}`);
console.log(`Ayirish: ${subtract(20, 8)}`);
```

## Tushuntirish va Mantiq:
type MathOperation = (x: number, y: number) => number; ko'rinishidagi deklaratsiya funksiya qabul qiluvchi parametrlar va qaytuvchi qiymat qolipini yaratadi.

## Ishlash natijasi:
```text
Ko'paytirish: 42
Ayirish: 12
```


# 607-Topshiriq: Interfeys yordamida funksiya tipini e'lon qilish (Call Signature)

## Topshiriq sharti:
String qabul qilib boolean qaytaruvchi StringValidator interfeysini e'lon qiling va elektron pochtani tekshiruvchi funksiya yarating.

## Yechim (JS yoki TS kodi):
```typescript
interface StringValidator {
    (input: string): boolean;
}

const emailValidator: StringValidator = (email) => {
    return email.includes("@") && email.includes(".");
};

console.log(`alisher@gmail.com: ${emailValidator("alisher@gmail.com")}`);
console.log(`not-an-email: ${emailValidator("not-an-email")}`);
```

## Tushuntirish va Mantiq:
Interfeys ichida nom berilmagan metod qolipi (input: string): boolean shaklida yozilsa, bu 'Call Signature' deyiladi va interfeys funksiya tipiga aylanadi.

## Ishlash natijasi:
```text
alisher@gmail.com: true
not-an-email: false
```


# 608-Topshiriq: Gibrid tipli funksiyalar (Hybrid Types)

## Topshiriq sharti:
Ham funksiya sifatida chaqiriladigan, ham o'zining xossasi va metodlariga ega hisoblagich (counter) obyekt-funksiyasini tipini belgilang.

## Yechim (JS yoki TS kodi):
```typescript
interface Counter {
    (): number;
    count: number;
    reset(): void;
}

function createCounter(): Counter {
    const fn = (() => ++fn.count) as Counter;
    fn.count = 0;
    fn.reset = () => { fn.count = 0; };
    return fn;
}

const c = createCounter();
console.log(c());
console.log(c());
c.reset();
console.log(c());
```

## Tushuntirish va Mantiq:
JavaScriptda funksiyalar obyekt bo'lgani uchun, TS da Call signature va oddiy xossalar birgalikda e'lon qilinishi mumkin (Hybrid Type).

## Ishlash natijasi:
```text
1
2
1
```


# 609-Topshiriq: void qaytaruvchi funksiyalar

## Topshiriq sharti:
Hech qanday qiymat qaytarmaydigan, faqat konsolga log yozuvchi xabar tizimini yarating.

## Yechim (JS yoki TS kodi):
```typescript
function logNotification(message: string, level: "INFO" | "WARN" | "ERROR"): void {
    console.log(`[${level}] ${message}`);
}

logNotification("Tizim ishga tushdi", "INFO");
logNotification("Xotira kam qoldi", "WARN");
```

## Tushuntirish va Mantiq:
void tipi funksiya hech qanday qiymat qaytarmasligini (yoki return; bilan bo'sh qaytishini) bildiradi.

## Ishlash natijasi:
```text
[INFO] Tizim ishga tushdi
[WARN] Xotira kam qoldi
```


# 610-Topshiriq: never tipi bilan tugallanmaydigan funksiyalar

## Topshiriq sharti:
Xatolik yuz berganda istisno (exception) tashlovchi yordamchi funksiyani yozing va never qaytish tipini bering.

## Yechim (JS yoki TS kodi):
```typescript
function raiseError(message: string): never {
    throw new Error(`Kritik xatolik: ${message}`);
}

try {
    raiseError("Ma'lumotlar bazasiga ulanib bo'lmadi");
} catch (e: any) {
    console.log(e.message);
}
```

## Tushuntirish va Mantiq:
never tipi funksiya hech qachon muvaffaqiyatli yakuniga yetmasligini (istisno tashlaydi yoki cheksiz siklda qoladi) ifodalaydi.

## Ishlash natijasi:
```text
Kritik xatolik: Ma'lumotlar bazasiga ulanib bo'lmadi
```


# 611-Topshiriq: Destrukturizatsiya qilingan parametrlar tipi

## Topshiriq sharti:
Foydalanuvchi ma'lumotlari obyektini argument sifatida qabul qilib, uni funksiya parametrining o'zida destrukturizatsiya qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface UserProfile {
    id: number;
    username: string;
    isActive: boolean;
}

function displayUser({ id, username, isActive }: UserProfile): void {
    console.log(`Foydalanuvchi #${id}: ${username} [${isActive ? "Faol" : "Nofaol"}]`);
}

displayUser({ id: 101, username: "bekzod_dev", isActive: true });
```

## Tushuntirish va Mantiq:
Obyekt parametrlarini ({ a, b }: Type) ko'rinishida destrukturizatsiya qilishda tiplash o'ng tomondagi obyekt tipiga biriktiriladi.

## Ishlash natijasi:
```text
Foydalanuvchi #101: bekzod_dev [Faol]
```


# 612-Topshiriq: Funksiya ortiqcha yuklash (Function Overloading) - Kirish

## Topshiriq sharti:
Agar string kelsa so'zlar sonini (number), agar massiv kelsa elementlar sonini (number) qaytaruvchi oddiy overload funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
function getCount(input: string): number;
function getCount(input: any[]): number;
function getCount(input: string | any[]): number {
    if (typeof input === "string") {
        return input.trim().split(/\s+/).length;
    }
    return input.length;
}

console.log("Matn so'zlari:", getCount("Salom dunyo TypeScript"));
console.log("Massiv elementlari:", getCount([10, 20, 30, 40, 50]));
```

## Tushuntirish va Mantiq:
Function overloading: bir nechta overload imzosi (signatures) e'lon qilinadi, so'ngra bitta umumiy implementatsiya funksiyasi yoziladi. Tashqi kod faqat overload imzolarini ko'radi.

## Ishlash natijasi:
```text
Matn so'zlari: 3
Massiv elementlari: 5
```


# 613-Topshiriq: Argumentlar soniga ko'ra ortiqcha yuklash

## Topshiriq sharti:
Bitta argument berilsa doira yuzini, ikkita argument berilsa to'g'ri to'rtburchak yuzini hisoblovchi area() funksiyasini overload qiling.

## Yechim (JS yoki TS kodi):
```typescript
function calculateArea(radius: number): number;
function calculateArea(width: number, height: number): number;
function calculateArea(a: number, b?: number): number {
    if (b !== undefined) {
        return a * b; // To'rtburchak
    }
    return Math.PI * a * a; // Doira
}

console.log("Doira yuzi (r=5):", calculateArea(5).toFixed(2));
console.log("To'rtburchak yuzi (w=4, h=6):", calculateArea(4, 6));
```

## Tushuntirish va Mantiq:
Argumentlar soni turlicha bo'lgan holatlarda, implementatsiya imzosi barcha variantlarni qamrab olishi kerak (b?: number).

## Ishlash natijasi:
```text
Doira yuzi (r=5): 78.54
To'rtburchak yuzi (w=4, h=6): 24
```


# 614-Topshiriq: Parametr tipiga bog'liq har xil qaytish tipi (Overload Return Types)

## Topshiriq sharti:
Kiruvchi qiymat string bo'lsa JSON obyektini qaytarsin, agar obyekt bo'lsa JSON string qaytarsin.

## Yechim (JS yoki TS kodi):
```typescript
function transformData(val: string): Record<string, any>;
function transformData(val: Record<string, any>): string;
function transformData(val: string | Record<string, any>): any {
    if (typeof val === "string") {
        return JSON.parse(val);
    }
    return JSON.stringify(val);
}

const obj = transformData('{"name": "Rustam", "age": 28}');
console.log("Obyekt nomi:", obj.name);

const str = transformData({ status: "OK", code: 200 });
console.log("JSON satr:", str);
```

## Tushuntirish va Mantiq:
Overload imzolari yordamida kirish parametri string bo'lsa qaytish tipi Record<string, any>, obyekt bo'lsa qaytish tipi string ekanligi kompilyator darajasida aniq kafolatlanadi.

## Ishlash natijasi:
```text
Obyekt nomi: Rustam
JSON satr: {"status":"OK","code":200}
```


# 615-Topshiriq: Sana formatlashda funksiya ortiqcha yuklash

## Topshiriq sharti:
Date obyekti yoki Unix timestamp (number) qabul qilib, formatlangan sana matnini qaytaruvchi formatDate funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function formatDate(date: Date): string;
function formatDate(timestamp: number): string;
function formatDate(input: Date | number): string {
    const d = typeof input === "number" ? new Date(input) : input;
    return d.toISOString().split("T")[0];
}

console.log(formatDate(new Date(2025, 5, 15)));
console.log(formatDate(1750000000000));
```

## Tushuntirish va Mantiq:
Turlicha kirish formatlarini qabul qilib, yagona mantiqqa birlashtirishda overload imzolari kodni juda toza va xavfsiz qiladi.

## Ishlash natijasi:
```text
2025-06-15
2025-06-15
```


# 616-Topshiriq: Obyekt metodlarida ortiqcha yuklash

## Topshiriq sharti:
DataStore sinfi metodida get() chaqirilsa butun obyektni, get(key) chaqirilsa aniq qiymatni qaytaruvchi metod yozing.

## Yechim (JS yoki TS kodi):
```typescript
class DataStore {
    private data: Record<string, string> = { lang: "TypeScript", framework: "NodeJS" };

    public get(): Record<string, string>;
    public get(key: string): string | undefined;
    public get(key?: string): any {
        if (key !== undefined) {
            return this.data[key];
        }
        return { ...this.data };
    }
}

const store = new DataStore();
console.log("Barcha ma'lumotlar:", store.get());
console.log("Til:", store.get("lang"));
```

## Tushuntirish va Mantiq:
Sinf metodlarida ham function overloading xuddi oddiy funksiyalar kabi public/private metod imzolari bilan amalga oshiriladi.

## Ishlash natijasi:
```text
Barcha ma'lumotlar: { lang: 'TypeScript', framework: 'NodeJS' }
Til: TypeScript
```


# 617-Topshiriq: this parametrini aniq tiplash (Explicit 'this')

## Topshiriq sharti:
Obyekt kontekstiga tayanuvchi funksiyada 'this' ning tipini birinchi parametr sifatida ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
interface UserContext {
    id: number;
    login: string;
}

function showIdentity(this: UserContext, greeting: string): void {
    console.log(`${greeting}, ${this.login} (ID: ${this.id})`);
}

const userObj: UserContext = { id: 77, login: "johndoe" };
showIdentity.call(userObj, "Xush kelibsiz");
```

## Tushuntirish va Mantiq:
TypeScript da funksiyaning birinchi parametri 'this: Type' deb yozilsa, bu oddiy argument emas, balki chaqiruv paytidagi 'this' kontekstining tipini belgilaydi. Kompilyatsiya natijasida u olib tashlanadi.

## Ishlash natijasi:
```text
Xush kelibsiz, johndoe (ID: 77)
```


# 618-Topshiriq: Callback funksiyalarida this tiplash

## Topshiriq sharti:
DOM elementiga o'xshash tugma bosilganda ishlaydigan hodisa callbackida this qaysi tugmaga tegishli ekanini tekshiring.

## Yechim (JS yoki TS kodi):
```typescript
interface CustomButton {
    label: string;
    onClick(this: CustomButton, eventName: string): void;
}

const submitBtn: CustomButton = {
    label: "Yuborish",
    onClick(this: CustomButton, eventName: string) {
        console.log(`Tugma '${this.label}' hodisasi: ${eventName}`);
    }
};

submitBtn.onClick("click");
```

## Tushuntirish va Mantiq:
Hodisalar (events) va callbacklarda 'this' ning to'g'ri bog'langanligini ta'minlash uchun 'this' parametri kompilyator tekshiruvini kuchaytiradi.

## Ishlash natijasi:
```text
Tugma 'Yuborish' hodisasi: click
```


# 619-Topshiriq: Asinxron funksiyalar va Promise qaytish tipi

## Topshiriq sharti:
Foydalanuvchi ID si bo'yicha ma'lumot olib keluvchi asinxron funksiya yozing va qaytish tipini Promise<UserData> qilib belgilang.

## Yechim (JS yoki TS kodi):
```typescript
interface UserData {
    id: number;
    name: string;
}

async function fetchUser(id: number): Promise<UserData> {
    return { id, name: `Foydalanuvchi_${id}` };
}

fetchUser(42).then(user => console.log(`Olingan user: ${user.name}`));
```

## Tushuntirish va Mantiq:
async funksiyalar har doim Promise qaytaradi. Uning ichidagi qiymat esa Promise<T> generigi orqali o'raladi.

## Ishlash natijasi:
```text
Olingan user: Foydalanuvchi_42
```


# 620-Topshiriq: Callback tipida void ning nozik jihati

## Topshiriq sharti:
Natija qaytarishi taqiqlanmagan, lekin chaqiruvchi kod e'tiborsiz qoldiradigan void qaytaruvchi callback yozing.

## Yechim (JS yoki TS kodi):
```typescript
type ActionCallback = () => void;

function doSomething(cb: ActionCallback): void {
    cb();
}

// Funksiya son qaytarsa ham void tipli callback ga mos tushadi
const res = doSomething(() => 12345);
console.log("doSomething muvaffaqiyatli bajarildi");
```

## Tushuntirish va Mantiq:
TypeScript da callback funksiya uchun '() => void' ko'rsatilsa, callback har qanday qiymat qaytarsa ham qabul qilinadi, lekin uning qaytargan qiymatidan foydalanishga yo'l qo'yilmaydi.

## Ishlash natijasi:
```text
doSomething muvaffaqiyatli bajarildi
```


# 621-Topshiriq: Constructor Signature (Yaratuvchi imzo)

## Topshiriq sharti:
new operatori bilan yangi obyekt yaratuvchi konstruktor funksiya qolipini interfeysda e'lon qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface ClockConstructor {
    new (hour: number, minute: number): ClockInterface;
}

interface ClockInterface {
    tick(): void;
}

class DigitalClock implements ClockInterface {
    constructor(private h: number, private m: number) {}
    tick() {
        console.log(`Soat urdi: ${this.h}:${this.m}`);
    }
}

function createClock(ctor: ClockConstructor, h: number, m: number): ClockInterface {
    return new ctor(h, m);
}

const clock = createClock(DigitalClock, 12, 30);
clock.tick();
```

## Tushuntirish va Mantiq:
new (params): ReturnType ko'rinishi Constructor Signature deb ataladi va fabrika funksiyalarida sinflarni parametr sifatida uzatishda ishlatiladi.

## Ishlash natijasi:
```text
Soat urdi: 12:30
```


# 622-Topshiriq: Higher-Order Function (Yuqori tartibli funksiya) tiplash

## Topshiriq sharti:
Boshqa funksiyani o'rab olib, uning bajarilish vaqtini o'lchovchi benchmark HOF funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function withLogging<T extends (...args: any[]) => any>(fn: T): T {
    return ((...args: any[]) => {
        console.log(`Funksiya chaqirildi, argumentlar:`, args);
        return fn(...args);
    }) as T;
}

const sum = (a: number, b: number) => a + b;
const loggedSum = withLogging(sum);
console.log("Natija:", loggedSum(10, 20));
```

## Tushuntirish va Mantiq:
Yuqori tartibli funksiyalar parametr sifatida funksiya qabul qiladi yoki yangi funksiya qaytaradi. Parametrlarni to'g'ri o'tkazish uchun generic va rest parametrlardan foydalaniladi.

## Ishlash natijasi:
```text
Funksiya chaqirildi, argumentlar: [ 10, 20 ]
Natija: 30
```


# 623-Topshiriq: Currying (Karrilash) funksiyasini tiplash

## Topshiriq sharti:
Ikki bosqichli curried ko'paytirish funksiyasini yozing va uning tiplarini to'liq ifodalang.

## Yechim (JS yoki TS kodi):
```typescript
type CurriedMultiply = (a: number) => (b: number) => number;

const multiplyBy: CurriedMultiply = (a) => (b) => a * b;

const double = multiplyBy(2);
const triple = multiplyBy(3);

console.log(`2 * 5 = ${double(5)}`);
console.log(`3 * 5 = ${triple(5)}`);
```

## Tushuntirish va Mantiq:
Currying bir vaqtning o'zida barcha argumentlarni emas, ketma-ket har bir chaqiruvda bittadan parametr oluvchi zanjirli funksiyalar tizimidir.

## Ishlash natijasi:
```text
2 * 5 = 10
3 * 5 = 15
```


# 624-Topshiriq: Generator funksiyalari (Generator typing)

## Topshiriq sharti:
Sonlar ketma-ketligini generatsiya qiluvchi generator funksiya yarating va uning Generator tip parametrlarini bering.

## Yechim (JS yoki TS kodi):
```typescript
function* numberRange(start: number, end: number): Generator<number, void, unknown> {
    for (let i = start; i <= end; i++) {
        yield i;
    }
}

const gen = numberRange(1, 4);
for (const val of gen) {
    console.log(`Hosil qilingan son: ${val}`);
}
```

## Tushuntirish va Mantiq:
Generator<TYield, TReturn, TNext> interfeysida: TYield - yield qilinadigan qiymat tipi, TReturn - funksiya oxirida return qilinadigan qiymat tipi, TNext - next() orqali ichkariga uzatiladigan qiymat tipi.

## Ishlash natijasi:
```text
Hosil qilingan son: 1
Hosil qilingan son: 2
Hosil qilingan son: 3
Hosil qilingan son: 4
```


# 625-Topshiriq: Async Generator funksiyalari

## Topshiriq sharti:
Asinxron kechikish bilan ma'lumot uzatuvchi AsyncGenerator yozing.

## Yechim (JS yoki TS kodi):
```typescript
async function* asyncStream(): AsyncGenerator<string, void, unknown> {
    yield "Birinchi xabar";
    yield "Ikkinchi xabar";
}

async function run() {
    for await (const msg of asyncStream()) {
        console.log(`Oqimdan keldi: ${msg}`);
    }
}

run();
```

## Tushuntirish va Mantiq:
AsyncGenerator<TYield, TReturn, TNext> asinxron ma'lumotlar oqimini for await (... of ...) siklida ketma-ket o'qish imkonini beradi.

## Ishlash natijasi:
```text
Oqimdan keldi: Birinchi xabar
Oqimdan keldi: Ikkinchi xabar
```


# 626-Topshiriq: Polimorfik this qaytarish (Fluent API)

## Topshiriq sharti:
Zanjirli metodlar chaqiruvi (method chaining) uchun 'this' qaytaruvchi Calculator sinfini yozing.

## Yechim (JS yoki TS kodi):
```typescript
class Calculator {
    private value: number = 0;

    add(n: number): this {
        this.value += n;
        return this;
    }

    multiply(n: number): this {
        this.value *= n;
        return this;
    }

    getResult(): number {
        return this.value;
    }
}

const res = new Calculator().add(5).multiply(4).getResult();
console.log(`Natija: ${res}`);
```

## Tushuntirish va Mantiq:
Qaytish tipi sifatida 'this' ko'rsatilsa, voris sinflarda ham meros olingan metodlar chaqirilganda aynan o'sha voris sinf tipini saqlab qoladi (polymorphic this).

## Ishlash natijasi:
```text
Natija: 20
```


# 627-Topshiriq: Assertion Signatures (asserts x is T)

## Topshiriq sharti:
Berilgan parametr string ekanligini tasdiqlovchi va bo'lmasa xato tashlovchi maxsus assert funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
function assertIsString(val: any): asserts val is string {
    if (typeof val !== "string") {
        throw new Error("Qiymat satr bo'lishi shart!");
    }
}

const mystery: any = "Salom TypeScript";
assertIsString(mystery);
// Bu joydan boshlab kompilyator mystery ning string ekanligini biladi
console.log("Satr uzunligi:", mystery.length);
```

## Tushuntirish va Mantiq:
asserts val is T deklaratsiyasi funksiya bajarilgandan so'ng, ushbu o'zgaruvchi shu tipga ega ekanligini kompilyatorga qat'iy uqtiradi.

## Ishlash natijasi:
```text
Satr uzunligi: 16
```


# 628-Topshiriq: Oddiy shartli Assertion (asserts condition)

## Topshiriq sharti:
Shart bajarilmaganda xato beruvchi assert funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function customAssert(condition: boolean, msg: string): asserts condition {
    if (!condition) {
        throw new Error(`Tekshiruv xatosi: ${msg}`);
    }
}

const age: number = 18;
customAssert(age >= 18, "Yosh kamida 18 bo'lishi kerak");
console.log("Tekshiruvdan o'tdi!");
```

## Tushuntirish va Mantiq:
asserts condition sintaksisi shart qanoatlantirilmasa keyingi kod satriga o'tmasligini kompilyator tahlilchisiga ma'lum qiladi.

## Ishlash natijasi:
```text
Tekshiruvdan o'tdi!
```


# 629-Topshiriq: Ortiqcha yuklash: DOM element qidirish namunasi

## Topshiriq sharti:
ID bo'yicha HTML element yoki canvas qidiruvchi metod kabi, kalit so'zga qarab tegishli tip qaytaruvchi overload yozing.

## Yechim (JS yoki TS kodi):
```typescript
type ElementTypeMap = {
    div: { tag: "div"; html: string };
    button: { tag: "button"; disabled: boolean };
};

function createElement<K extends keyof ElementTypeMap>(tag: K): ElementTypeMap[K] {
    if (tag === "div") return { tag: "div", html: "" } as ElementTypeMap[K];
    return { tag: "button", disabled: false } as ElementTypeMap[K];
}

const div = createElement("div");
console.log("Yaratildi:", div.tag);
```

## Tushuntirish va Mantiq:
Generik va xaritalangan tiplar (mapped types) orqali parametr qiymatiga qarab aniq tipni xavfsiz qaytarish mumkin.

## Ishlash natijasi:
```text
Yaratildi: div
```


# 630-Topshiriq: Overload tartibining ahamiyati

## Topshiriq sharti:
Aniqroq overload imzolari har doim umumiyroq imzodan oldin turishi kerakligini kod misolida ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function processVal(x: "urgent"): string;
function processVal(x: string): string;
function processVal(x: string): string {
    if (x === "urgent") return "SHOSHILINCH AMAL";
    return `Oddiy amal: ${x}`;
}

console.log(processVal("urgent"));
console.log(processVal("standard"));
```

## Tushuntirish va Mantiq:
TypeScript overload imzolarini yuqoridan pastga qarab tekshiradi. Agar umumiy string imzosi literal 'urgent' dan oldin qo'yilsa, aniqroq imzo hech qachon ishlamaydi.

## Ishlash natijasi:
```text
SHOSHILINCH AMAL
Oddiy amal: standard
```


# 631-Topshiriq: Funksiya parametri sifatida callback bilan xatolik boshqaruvi

## Topshiriq sharti:
Node.js uslubidagi error-first callback (err: Error | null, data?: string) parametrini tiplash.

## Yechim (JS yoki TS kodi):
```typescript
type NodeCallback = (err: Error | null, result?: string) => void;

function readFileMock(path: string, callback: NodeCallback): void {
    if (path === "valid.txt") {
        callback(null, "Fayl muvaffaqiyatli o'qildi!");
    } else {
        callback(new Error("Fayl topilmadi"));
    }
}

readFileMock("valid.txt", (err, data) => {
    if (err) console.error(err.message);
    else console.log(data);
});
```

## Tushuntirish va Mantiq:
Node.js uslubidagi asinxron callbacklarda birinchi parametr Error yoki null, ikkinchi parametr esa natija bo'lishi standart amaliyotdir.

## Ishlash natijasi:
```text
Fayl muvaffaqiyatli o'qildi!
```


# 632-Topshiriq: Funksiya imzolarida ReadonlyArray parametri

## Topshiriq sharti:
Massivni o'zgartirmasdan faqat o'quvchi xavfsiz funksiya parametrlari.

## Yechim (JS yoki TS kodi):
```typescript
function sumReadOnly(numbers: readonly number[]): number {
    return numbers.reduce((acc, curr) => acc + curr, 0);
}

const myNums: number[] = [1, 2, 3, 4, 5];
console.log("Yig'indi:", sumReadOnly(myNums));
```

## Tushuntirish va Mantiq:
readonly number[] parametri berilsa, funksiya tanasi ichida push, pop kabi o'zgartiruvchi operatsiyalar chaqirilishi kompilyatsiya xatosini beradi.

## Ishlash natijasi:
```text
Yig'indi: 15
```


# 633-Topshiriq: Generic Constraints funksiya parametrida

## Topshiriq sharti:
Faqat length xossasiga ega obyektlarni qabul qiluvchi generik funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
interface HasLength {
    length: number;
}

function printLength<T extends HasLength>(item: T): void {
    console.log(`Uzunlik: ${item.length}`);
}

printLength("Salom");
printLength([10, 20, 30]);
printLength({ length: 99, info: "Custom" });
```

## Tushuntirish va Mantiq:
T extends HasLength cheklovi (constraint) argument sifatida faqat length xossasiga ega turlarni uzatishni ta'minlaydi.

## Ishlash natijasi:
```text
Uzunlik: 5
Uzunlik: 3
Uzunlik: 99
```


# 634-Topshiriq: Funksiyalar kompozitsiyasi (Compose) tipi

## Topshiriq sharti:
Ikki funksiyani bitta funksiyaga birlashtiruvchi compose funksiyasini tiplash.

## Yechim (JS yoki TS kodi):
```typescript
function compose<A, B, C>(f: (b: B) => C, g: (a: A) => B): (a: A) => C {
    return (a: A) => f(g(a));
}

const addTwo = (x: number) => x + 2;
const numToStr = (x: number) => `Son: ${x}`;

const addAndStringify = compose(numToStr, addTwo);
console.log(addAndStringify(10));
```

## Tushuntirish va Mantiq:
compose(f, g)(x) matematika dagi f(g(x)) ga teng. TS da generiklar A, B, C orqali oraliq va yakuniy tiplar qat'iy tekshiriladi.

## Ishlash natijasi:
```text
Son: 12
```


# 635-Topshiriq: Parametrlar ro'yxatida nomlangan tuple (Named Tuple Members)

## Topshiriq sharti:
Funksiya parametrlarini named tuple orqali o'qishli va tushunarli qilish.

## Yechim (JS yoki TS kodi):
```typescript
type UserCoordinates = [latitude: number, longitude: number, altitude?: number];

function locateUser(...coords: UserCoordinates): void {
    const [lat, lng, alt] = coords;
    console.log(`Kenglik: ${lat}, Uzunlik: ${lng}, Balandlik: ${alt ?? 0}m`);
}

locateUser(41.2995, 69.2401);
```

## Tushuntirish va Mantiq:
Named tuple a'zolari parametrlar ro'yxatida IDE avtoto'ldirishida parametr nomlari sifatida ko'rinib, kod o'qilishini yaxshilaydi.

## Ishlash natijasi:
```text
Kenglik: 41.2995, Uzunlik: 69.2401, Balandlik: 0m
```


# 636-Topshiriq: Overload bilan sozlamalar obyekti va oddiy qiymat qabul qilish

## Topshiriq sharti:
Birinchi variantda to'g'ridan-to'g'ri string, ikkinchi variantda esa options obyekti oluvchi overload yozing.

## Yechim (JS yoki TS kodi):
```typescript
interface LogConfig {
    msg: string;
    prefix: string;
}

function systemLog(msg: string): void;
function systemLog(config: LogConfig): void;
function systemLog(arg: string | LogConfig): void {
    if (typeof arg === "string") {
        console.log(`[LOG]: ${arg}`);
    } else {
        console.log(`[${arg.prefix}]: ${arg.msg}`);
    }
}

systemLog("Oddiy ogohlantirish");
systemLog({ msg: "To'lov amalga oshdi", prefix: "PAYMENT" });
```

## Tushuntirish va Mantiq:
Overload orqali qulay chaqiruv usullarini yaratish mumkin: oddiy holatda tezkor parametr, murakkab holatda konfiguratsiya obyekti.

## Ishlash natijasi:
```text
[LOG]: Oddiy ogohlantirish
[PAYMENT]: To'lov amalga oshdi
```


# 637-Topshiriq: Funksiya xossasiga ega bo'lgan funksiyalar (Callable Object)

## Topshiriq sharti:
O'zining versiya raqami bor funksiya interfeysini tuzing.

## Yechim (JS yoki TS kodi):
```typescript
interface AppVersionFn {
    (): string;
    version: string;
}

const getAppName: AppVersionFn = Object.assign(
    () => "MySuperApp",
    { version: "2.1.0" }
);

console.log(`${getAppName()} v${getAppName.version}`);
```

## Tushuntirish va Mantiq:
Object.assign yordamida funksiyaga statik xossa biriktirilib, AppVersionFn interfeysiga mos keltiriladi.

## Ishlash natijasi:
```text
MySuperApp v2.1.0
```


# 638-Topshiriq: Ortiqcha yuklash: Massivni filtrlash yoki bitta element topish

## Topshiriq sharti:
Boolean ikkinchi parametriga qarab yoki butun massiv yoki faqat birinchi mos elementni qaytaruvchi overload.

## Yechim (JS yoki TS kodi):
```typescript
function searchItems(query: string, single: true): string | undefined;
function searchItems(query: string, single?: false): string[];
function searchItems(query: string, single: boolean = false): any {
    const list = ["apple", "apricot", "banana", "avocado"];
    const matched = list.filter(item => item.startsWith(query));
    return single ? matched[0] : matched;
}

const one = searchItems("a", true);
const all = searchItems("a");
console.log("Bitta:", one);
console.log("Barchasi:", all);
```

## Tushuntirish va Mantiq:
Literal boolean tiplari (single: true va single?: false) orqali qaytish tipini bitta element yoki massivga o'zgartirish mumkin.

## Ishlash natijasi:
```text
Bitta: apple
Barchasi: [ 'apple', 'apricot', 'avocado' ]
```


# 639-Topshiriq: Debounce funksiyasini tiplash

## Topshiriq sharti:
Ixtiyoriy funksiyani kechiktiruvchi debounce wrapper funksiyasi tipini yarating.

## Yechim (JS yoki TS kodi):
```typescript
function debounce<T extends (...args: any[]) => void>(fn: T, delay: number): (...args: Parameters<T>) => void {
    let timeoutId: any;
    return (...args: Parameters<T>) => {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
            fn(...args);
        }, delay);
    };
}

const sendLog = (text: string, code: number) => {
    console.log(`Log jo'natildi: ${text} (${code})`);
};

const debouncedSend = debounce(sendLog, 100);
debouncedSend("Test xabar", 200);
```

## Tushuntirish va Mantiq:
Parameters<T> utility tipi yordamida original funksiyaning barcha argument tiplari saqlab qolinadi.

## Ishlash natijasi:
```text
Log jo'natildi: Test xabar (200)
```


# 640-Topshiriq: Throttle funksiyasini tiplash

## Topshiriq sharti:
Funksiya chaqiruvlari oralig'ini cheklovchi throttle tipi yaratish.

## Yechim (JS yoki TS kodi):
```typescript
function throttle<T extends (...args: any[]) => void>(fn: T, limit: number): (...args: Parameters<T>) => void {
    let inThrottle = false;
    return (...args: Parameters<T>) => {
        if (!inThrottle) {
            fn(...args);
            inThrottle = true;
            setTimeout(() => { inThrottle = false; }, limit);
        }
    };
}

const onScroll = (pos: number) => console.log(`Skroll: ${pos}`);
const throttledScroll = throttle(onScroll, 200);
throttledScroll(100);
throttledScroll(120);
```

## Tushuntirish va Mantiq:
Throttle yordamida funksiya belgilangan vaqt ichida ko'pi bilan bir marta chaqiriladi, uning argumentlari Parameters<T> bilan to'liq tiplanadi.

## Ishlash natijasi:
```text
Skroll: 100
```


# 641-Topshiriq: Sinf konstruktorini overload qilish

## Topshiriq sharti:
Point sinfida yoki koordinata raqamlari yoki boshqa Point obyektini nusxalash orqali yaratish.

## Yechim (JS yoki TS kodi):
```typescript
class Point {
    public x: number;
    public y: number;

    constructor(x: number, y: number);
    constructor(other: Point);
    constructor(arg1: number | Point, arg2?: number) {
        if (typeof arg1 === "object") {
            this.x = arg1.x;
            this.y = arg1.y;
        } else {
            this.x = arg1;
            this.y = arg2 ?? 0;
        }
    }
}

const p1 = new Point(10, 20);
const p2 = new Point(p1);
console.log(`p1: (${p1.x}, ${p1.y}), p2: (${p2.x}, ${p2.y})`);
```

## Tushuntirish va Mantiq:
Sinf konstruktori ham xuddi funksiyalar kabi bir nechta overload imzolariga ega bo'lishi mumkin.

## Ishlash natijasi:
```text
p1: (10, 20), p2: (10, 20)
```


# 642-Topshiriq: Never qaytaruvchi exhaustive check funksiyasi

## Topshiriq sharti:
Switch blokida barcha holatlar tekshirilganligini kafolatlovchi assertNever funksiyasi.

## Yechim (JS yoki TS kodi):
```typescript
type TrafficLight = "RED" | "YELLOW" | "GREEN";

function assertNever(x: never): never {
    throw new Error(`Kutilmagan qiymat: ${x}`);
}

function getAction(light: TrafficLight): string {
    switch (light) {
        case "RED": return "To'xtang";
        case "YELLOW": return "Tayyorlaning";
        case "GREEN": return "Harakatlaning";
        default: return assertNever(light);
    }
}

console.log(getAction("GREEN"));
```

## Tushuntirish va Mantiq:
Agar TrafficLight ga yangi qiymat (masalan, 'BLUE') qo'shilsa-yu, switch da u tekshirilmasa, default dagi assertNever(light) kompilyatsiya xatosini beradi.

## Ishlash natijasi:
```text
Harakatlaning
```


# 643-Topshiriq: Funksiyalarda Index Signature bilan parametrlar

## Topshiriq sharti:
Noma'lum nomli qo'shimcha parametrlarga ega konfiguratsiya funksiyasini tiplash.

## Yechim (JS yoki TS kodi):
```typescript
interface DynamicOptions {
    name: string;
    [key: string]: any;
}

function initPlugin(options: DynamicOptions): void {
    console.log(`Plagin: ${options.name}`);
    if (options.timeout) {
        console.log(`Timeout: ${options.timeout}ms`);
    }
}

initPlugin({ name: "AuthPlugin", timeout: 5000, debug: true });
```

## Tushuntirish va Mantiq:
Index signature [key: string]: any funksiya parametrida nomi oldindan noma'lum bo'lgan dinamik kalitlarni qabul qilishga imkon beradi.

## Ishlash natijasi:
```text
Plagin: AuthPlugin
Timeout: 5000ms
```


# 644-Topshiriq: Funksiya tiplarida kovariantlik va kontravariantlik

## Topshiriq sharti:
Callback parametrlarining mosligi (function assignability).

## Yechim (JS yoki TS kodi):
```typescript
class Animal { name = "Animal"; }
class Dog extends Animal { breed = "Alabay"; }

type AnimalHandler = (a: Animal) => void;
type DogHandler = (d: Dog) => void;

let handleDog: DogHandler;
let handleAnimal: AnimalHandler = (a: Animal) => console.log(a.name);

// AnimalHandler funksiyasini DogHandler ga biriktirish mumkin (kontravariantlik)
handleDog = handleAnimal;
handleDog(new Dog());
```

## Tushuntirish va Mantiq:
TypeScript da funksiya parametrlari kontravariant (strictFunctionTypes yoqilganda), ya'ni kengroq tip qabul qiluvchi funksiya torroq tip kutayotgan joyga berilishi mumkin.

## Ishlash natijasi:
```text
Animal
```


# 645-Topshiriq: Overload bilan Promise va Callback rejimini qo'llab-quvvatlash

## Topshiriq sharti:
Agar callback berilsa void qaytarsin, berilmasa Promise qaytarsin.

## Yechim (JS yoki TS kodi):
```typescript
function fetchData(id: number): Promise<string>;
function fetchData(id: number, cb: (res: string) => void): void;
function fetchData(id: number, cb?: (res: string) => void): Promise<string> | void {
    const data = `Ma'lumot_${id}`;
    if (cb) {
        cb(data);
        return;
    }
    return Promise.resolve(data);
}

fetchData(10, (res) => console.log(`Callback natijasi: ${res}`));
fetchData(20).then(res => console.log(`Promise natijasi: ${res}`));
```

## Tushuntirish va Mantiq:
Ushbu naqsh kutubxonalarda keng tarqalgan: foydalanuvchi xohlasa callback, xohlasa async/await orqali Promise bilan ishlashi mumkin.

## Ishlash natijasi:
```text
Callback natijasi: Ma'lumot_10
Promise natijasi: Ma'lumot_20
```


# 646-Topshiriq: Funksiya qaytish qiymatida Type Predicate (is)

## Topshiriq sharti:
Obyekt Person ekanligini aniqlovchi funksiya va uning qaytish tipi.

## Yechim (JS yoki TS kodi):
```typescript
interface Person {
    name: string;
    age: number;
}

function isPerson(obj: any): obj is Person {
    return typeof obj === "object" && obj !== null && "name" in obj && "age" in obj;
}

const item: unknown = { name: "Bobur", age: 30 };
if (isPerson(item)) {
    console.log(`Shaxs nomi: ${item.name}, yoshi: ${item.age}`);
}
```

## Tushuntirish va Mantiq:
obj is Person qaytaruvchi funksiyalar Type Guard deb ataladi va if blokida tiplarni avtomatik toraytiradi (narrowing).

## Ishlash natijasi:
```text
Shaxs nomi: Bobur, yoshi: 30
```


# 647-Topshiriq: Ortiqcha yuklash: JSON ma'lumot parse qilish

## Topshiriq sharti:
Turli sxemalar uchun turlicha parse natijalari qaytaruvchi overload funksiya.

## Yechim (JS yoki TS kodi):
```typescript
function parseConfig(type: "database"): { host: string; port: number };
function parseConfig(type: "app"): { appName: string; version: string };
function parseConfig(type: string): any {
    if (type === "database") return { host: "localhost", port: 5432 };
    return { appName: "DemoApp", version: "1.0.0" };
}

const dbConfig = parseConfig("database");
console.log(`DB Port: ${dbConfig.port}`);
```

## Tushuntirish va Mantiq:
Literal stringlar bilan overload imzolarini berish orqali kalit so'ziga qarab qat'iy tipdagi konfiguratsiya obyektlarini olish mumkin.

## Ishlash natijasi:
```text
DB Port: 5432
```


# 648-Topshiriq: Funksiyalarda Uncurrying namunasi

## Topshiriq sharti:
Karrilangan funksiyani yana oddiy ikki parametrli funksiyaga aylantiruvchi yordamchi.

## Yechim (JS yoki TS kodi):
```typescript
function uncurry<A, B, C>(fn: (a: A) => (b: B) => C): (a: A, b: B) => C {
    return (a: A, b: B) => fn(a)(b);
}

const curriedSum = (x: number) => (y: number) => x + y;
const normalSum = uncurry(curriedSum);

console.log("Oddiy chaqiruv:", normalSum(15, 25));
```

## Tushuntirish va Mantiq:
Uncurry operatsiyasi ko'p bosqichli funksiyani bitta chaqiruvga ega funksiyaga o'zgartiradi va uning tiplari generiklar bilan xavfsiz bog'lanadi.

## Ishlash natijasi:
```text
Oddiy chaqiruv: 40
```


# 649-Topshiriq: Method Shorthand va Property funksiya sintaksisi farqi

## Topshiriq sharti:
Interfeysda metod yozishning ikki xil sintaksisi va ularning tiplar tekshiruvidagi farqi.

## Yechim (JS yoki TS kodi):
```typescript
interface ServiceA {
    // Method shorthand - bivariant tekshiriladi
    process(input: string | number): void;
}

interface ServiceB {
    // Property syntax - qat'iy kontravariant tekshiriladi
    process: (input: string | number) => void;
}

console.log("Metod va property imzolash qoidalari o'rganildi.");
```

## Tushuntirish va Mantiq:
TypeScript da metod sintaksisi m(x: T): void standart bivariantlikka ruxsat beradi, biroq xossa sintaksisi m: (x: T) => void strictFunctionTypes ostida to'liq xavfsiz parametr tiplashni ta'minlaydi.

## Ishlash natijasi:
```text
Metod va property imzolash qoidalari o'rganildi.
```


# 650-Topshiriq: Funksiyalarni quvur zanjiri (Pipe) yordamida ketma-ket bajarish

## Topshiriq sharti:
Berilgan son ustida ketma-ket 3 ta funksiyani bajaruvchi typed pipe funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function pipe<T1, T2, T3, T4>(
    initial: T1,
    f1: (x: T1) => T2,
    f2: (x: T2) => T3,
    f3: (x: T3) => T4
): T4 {
    return f3(f2(f1(initial)));
}

const result = pipe(
    5,
    x => x * 2,       // 10
    x => `Son: ${x}`, // "Son: 10"
    s => s.toUpperCase() // "SON: 10"
);

console.log("Yakuniy natija:", result);
```

## Tushuntirish va Mantiq:
pipe funksiyasi har bir bosqichning qaytish qiymatini keyingi bosqichning kirishiga uzatadi va generiklar T1->T2->T3->T4 orqali zanjirning yaxlitligini nazorat qiladi.

## Ishlash natijasi:
```text
Yakuniy natija: SON: 10
```

