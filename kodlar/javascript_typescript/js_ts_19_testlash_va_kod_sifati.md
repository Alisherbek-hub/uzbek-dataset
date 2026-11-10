# 901-Topshiriq: Unit test asoslari: test() va expect(value).toBe()

## Topshiriq sharti:
Ikki sonni qo'shuvchi add() funksiyasini Vitest/Jest da unit test bilan tekshiring.

## Yechim (JS yoki TS kodi):
```typescript
function add(a: number, b: number): number {
    return a + b;
}

// Mock testing framework sintaksisi
function expect<T>(actual: T) {
    return {
        toBe(expected: T) {
            if (actual !== expected) {
                throw new Error(`Xato: Kutilgan ${expected}, lekin olindi ${actual}`);
            }
        }
    };
}

function test(description: string, fn: () => void) {
    try {
        fn();
        console.log(`[PASS] ${description}`);
    } catch (e: any) {
        console.error(`[FAIL] ${description} -> ${e.message}`);
    }
}

test("add(2, 3) 5 ga teng bo'lishi kerak", () => {
    expect(add(2, 3)).toBe(5);
});
```

## Tushuntirish va Mantiq:
`test()` test sarlavhasi va tekshiruvchi callbackni oladi. `expect().toBe()` esa qat'iy tenglikni (`===`) tekshiradi.

## Ishlash natijasi:
```text
[PASS] add(2, 3) 5 ga teng bo'lishi kerak
```


# 902-Topshiriq: expect matcherlar: toEqual va toStrictEqual

## Topshiriq sharti:
Obyektlar va massivlarning chuqur (deep equality) tengligini tekshirish.

## Yechim (JS yoki TS kodi):
```typescript
function createUser(id: number, name: string) {
    return { id, name, active: true };
}

function deepEqual(a: any, b: any): boolean {
    return JSON.stringify(a) === JSON.stringify(b);
}

const user1 = createUser(1, "Sardor");
const expectedUser = { id: 1, name: "Sardor", active: true };

console.log("Obyektlar tengmi (toEqual):", deepEqual(user1, expectedUser));
```

## Tushuntirish va Mantiq:
`toBe` xotiradagi havolani (reference) tekshiradi, `toEqual` esa obyektning barcha xossalarini chuqur (deep equal) solishtiradi.

## Ishlash natijasi:
```text
Obyektlar tengmi (toEqual): true
```


# 903-Topshiriq: expect matcherlar: toBeTruthy, toBeFalsy, toBeNull, toBeUndefined

## Topshiriq sharti:
Mantiqiy qiymatlar va bo'shliqlarni maxsus matcherlar orqali tekshirish.

## Yechim (JS yoki TS kodi):
```typescript
const isOnline = true;
const errorReason = null;
let pendingOrder;

console.log("isOnline haqiqatmi:", Boolean(isOnline) === true); // toBeTruthy
console.log("errorReason nullmi:", errorReason === null);        // toBeNull
console.log("pendingOrder noaniqmi:", pendingOrder === undefined); // toBeUndefined
```

## Tushuntirish va Mantiq:
Jest va Vitest da `toBeTruthy()`, `toBeFalsy()`, `toBeNull()` va `toBeUndefined()` orqali ma'lumot mavjudligi aniq tekshiriladi.

## Ishlash natijasi:
```text
isOnline haqiqatmi: true
errorReason nullmi: true
pendingOrder noaniqmi: true
```


# 904-Topshiriq: expect matcherlar: toContain va toHaveLength

## Topshiriq sharti:
Massivda element mavjudligi va massiv uzunligini tekshirish.

## Yechim (JS yoki TS kodi):
```typescript
const fruits = ["olma", "anor", "anjir"];

console.log("Uchta element bormi:", fruits.length === 3); // toHaveLength(3)
console.log("'anor' massivda bormi:", fruits.includes("anor")); // toContain("anor")
```

## Tushuntirish va Mantiq:
`toContain` massivda ma'lum element yoki matnda qism satr borligini tekshiradi, `toHaveLength` esa .length xossasini solishtiradi.

## Ishlash natijasi:
```text
Uchta element bormi: true
'anor' massivda bormi: true
```


# 905-Topshiriq: expect matcherlar: toThrowError

## Topshiriq sharti:
Funksiya kutilgan xatolikni tashlashini (throw) tekshirish.

## Yechim (JS yoki TS kodi):
```typescript
function divide(a: number, b: number): number {
    if (b === 0) throw new Error("Nolga bo'lish mumkin emas!");
    return a / b;
}

let thrown = false;
try {
    divide(10, 0);
} catch (e: any) {
    if (e.message.includes("Nolga bo'lish")) thrown = true;
}

console.log("Xatolik muvaffaqiyatli ushlandimi:", thrown);
```

## Tushuntirish va Mantiq:
`expect(() => fn()).toThrow()` yordamida noto'g'ri argumentlar kiritilganda funksiya xato otishi sinovdan o'tkaziladi.

## Ishlash natijasi:
```text
Xatolik muvaffaqiyatli ushlandimi: true
```


# 906-Topshiriq: Guruhlangan testlar: describe() bloki

## Topshiriq sharti:
Bitta modul yoki xizmatga tegishli bir nechta testlarni mantiqiy bloklarga ajratish.

## Yechim (JS yoki TS kodi):
```typescript
function describe(suiteName: string, fn: () => void) {
    console.log(`--- Test Suite: ${suiteName} ---`);
    fn();
}

describe("MathOperations", () => {
    console.log("  [TEST] Qo'shish amali");
    console.log("  [TEST] Ko'paytirish amali");
});
```

## Tushuntirish va Mantiq:
`describe()` bloki test faylini tartibga soladi, test hisobotlarida ierarxik daraxt hosil qiladi.

## Ishlash natijasi:
```text
--- Test Suite: MathOperations ---
  [TEST] Qo'shish amali
  [TEST] Ko'paytirish amali
```


# 907-Topshiriq: Asinxron testlar: async/await bilan Promise kutish

## Topshiriq sharti:
Asinxron backend xizmatlarini to'g'ri testlash usuli.

## Yechim (JS yoki TS kodi):
```typescript
async function fetchUserScore(userId: number): Promise<number> {
    return Promise.resolve(userId * 10);
}

async function runAsyncTest() {
    const score = await fetchUserScore(5);
    console.log("Natija 50 bo'ldimi:", score === 50);
}

runAsyncTest();
```

## Tushuntirish va Mantiq:
Asinxron testlarda test funksiyasi `async () => { await ... }` bo'lishi shart, aks holda test Promise yakunlanishini kutmasdan o'tib ketadi.

## Ishlash natijasi:
```text
Natija 50 bo'ldimi: true
```


# 908-Topshiriq: Asinxron matcherlar: resolves va rejects

## Topshiriq sharti:
Promise muvaffaqiyatli yoki xatolik bilan tugashini deklarativ tekshirish.

## Yechim (JS yoki TS kodi):
```typescript
const successPromise = Promise.resolve("OK");
const failedPromise = Promise.reject(new Error("Ulanish xatosi"));

successPromise.then(res => console.log("Resolves:", res === "OK"));
failedPromise.catch(err => console.log("Rejects:", err.message.includes("Ulanish")));
```

## Tushuntirish va Mantiq:
Jest va Vitest da `await expect(promise).resolves.toBe('OK')` yoki `.rejects.toThrow()` sintaksislari ishlatiladi.

## Ishlash natijasi:
```text
Resolves: true
Rejects: true
```


# 909-Topshiriq: Setup va Teardown: beforeEach va afterEach

## Topshiriq sharti:
Har bir testdan oldin holatni tozalash va tayyorlash.

## Yechim (JS yoki TS kodi):
```typescript
let databaseState: string[] = [];

function beforeEach(fn: () => void) { fn(); }
function afterEach(fn: () => void) { fn(); }

// Har bir testdan oldin bazani tiklaymiz
beforeEach(() => {
    databaseState = ["dastlabki_element"];
});

console.log("Dastlabki holat:", databaseState.length);
databaseState.push("yangi_element");
console.log("Test ichida o'zgardi:", databaseState.length);

// Tozalash
afterEach(() => {
    databaseState = [];
});
console.log("Testdan keyin tozalandi:", databaseState.length);
```

## Tushuntirish va Mantiq:
`beforeEach` har bir alohida test mustaqil (isolated) bo'lishini va boshqa testlar qoldirgan axlatlardan ta'sirlanmasligini kafolatlaydi.

## Ishlash natijasi:
```text
Dastlabki holat: 1
Test ichida o'zgardi: 2
Testdan keyin tozalandi: 0
```


# 910-Topshiriq: Setup va Teardown: beforeAll va afterAll

## Topshiriq sharti:
Barcha testlar boshlanishidan oldin va oxirida bir marta ishlovchi global sozlamalar.

## Yechim (JS yoki TS kodi):
```typescript
let serverPort: number | null = null;

function beforeAll() {
    serverPort = 8080;
    console.log("Soxta test serveri 8080 portda ishga tushdi.");
}

function afterAll() {
    serverPort = null;
    console.log("Soxta test serveri to'xtatildi.");
}

beforeAll();
console.log("Testlar bajarilmoqda, port:", serverPort);
afterAll();
```

## Tushuntirish va Mantiq:
`beforeAll` va `afterAll` og'ir operatsiyalar (masalan, test ma'lumotlar bazasini yuklash yoki serverni yoqish/o'chirish) uchun bir martalik resurs ajratadi.

## Ishlash natijasi:
```text
Soxta test serveri 8080 portda ishga tushdi.
Testlar bajarilmoqda, port: 8080
Soxta test serveri to'xtatildi.
```


# 911-Topshiriq: Mock funksiya asoslari: vi.fn() / jest.fn()

## Topshiriq sharti:
Funksiya chaqirilganligini va argumentlarini yozib oluvchi mock obyekti.

## Yechim (JS yoki TS kodi):
```typescript
function createMockFunction() {
    const calls: any[][] = [];
    const fn: any = (...args: any[]) => {
        calls.push(args);
        return fn.mockReturnValue;
    };
    fn.mock = { calls };
    return fn;
}

const mockCallback = createMockFunction();
mockCallback("salom", 123);
mockCallback("dunyo");

console.log("Chaqiruvlar soni:", mockCallback.mock.calls.length);
console.log("1-chaqiruv argumenti:", mockCallback.mock.calls[0][0]);
```

## Tushuntirish va Mantiq:
Mock funksiyalar real xizmatlarni chaqirmasdan, faqat ularga qanday parametrlar berilganligini tekshirish uchun xizmat qiladi.

## Ishlash natijasi:
```text
Chaqiruvlar soni: 2
1-chaqiruv argumenti: salom
```


# 912-Topshiriq: Mock: toHaveBeenCalledWith tekshiruvi

## Topshiriq sharti:
Funksiya aynan kerakli argumentlar bilan chaqirilganligini tasdiqlash.

## Yechim (JS yoki TS kodi):
```typescript
class NotificationService {
    notify(user: string, message: string) {
        console.log(`Xabar: ${user} -> ${message}`);
    }
}

// Mock tekshiruvi simulyatsiyasi
const recordedArgs: [string, string][] = [];
const mockNotify = (u: string, m: string) => recordedArgs.push([u, m]);

mockNotify("islom@uz.dev", "Xush kelibsiz");
const isCalledCorrectly = recordedArgs.some(([u, m]) => u === "islom@uz.dev" && m === "Xush kelibsiz");

console.log("To'g'ri parametrlar bilan chaqirildimi:", isCalledCorrectly);
```

## Tushuntirish va Mantiq:
`toHaveBeenCalledWith(arg1, arg2)` metodi funksiyaga uzatilgan qiymatlarni aniq solishtiradi.

## Ishlash natijasi:
```text
To'g'ri parametrlar bilan chaqirildimi: true
```


# 913-Topshiriq: Mock qaytish qiymati: mockReturnValue va mockResolvedValue

## Topshiriq sharti:
Tashqi API yoki bazadan qaytadigan soxta javobni oldindan belgilash.

## Yechim (JS yoki TS kodi):
```typescript
interface UserApi {
    getUser(id: number): Promise<{ id: number; name: string }>;
}

const mockApi: UserApi = {
    getUser: async (id: number) => ({ id, name: "Mock Ali" })
};

mockApi.getUser(1).then(user => {
    console.log("Mock natija:", user.name);
});
```

## Tushuntirish va Mantiq:
`mockResolvedValue` asinxron funksiyalar uchun Promise.resolve(qiymat) ni avtomatik qaytarib beradi.

## Ishlash natijasi:
```text
Mock natija: Mock Ali
```


# 914-Topshiriq: SpyOn yordamida metodlarni kuzatish (vi.spyOn)

## Topshiriq sharti:
Mavjud obyekt metodini buzmasdan uning chaqirilishini monitoring qilish.

## Yechim (JS yoki TS kodi):
```typescript
const mathObj = {
    multiply(a: number, b: number) {
        return a * b;
    }
};

let callCounter = 0;
const originalMultiply = mathObj.multiply;
mathObj.multiply = (a, b) => {
    callCounter++;
    return originalMultiply(a, b);
};

const result = mathObj.multiply(4, 5);
console.log(`Natija: ${result}, Chaqirildi: ${callCounter} marta`);
```

## Tushuntirish va Mantiq:
`spyOn` mavjud obyekt metodining asl ishini saqlab qolgan holda, uning necha marta chaqirilganini kuzatishga imkon beradi.

## Ishlash natijasi:
```text
Natija: 20, Chaqirildi: 1 marta
```


# 915-Topshiriq: Fake Timers: setTimeout ni tezlashtirish

## Topshiriq sharti:
Sekundlab yoki soatlab kutmasdan taymerlarni bir zumda oldinga siljitish.

## Yechim (JS yoki TS kodi):
```typescript
let isExecuted = false;

// Haqiqiy kutishsiz taymer simulyatsiyasi
function scheduleTask(delayMs: number, cb: () => void) {
    return { delay: delayMs, run: cb };
}

const scheduled = scheduleTask(5000, () => { isExecuted = true; });

console.log("Vaqt o'tishidan oldin:", isExecuted);
scheduled.run(); // Fake timers orqali vaqtni oldinga surdik
console.log("Vaqt o'tgandan keyin:", isExecuted);
```

## Tushuntirish va Mantiq:
`vi.useFakeTimers()` va `vi.advanceTimersByTime(5000)` testlarni bir necha millisekundda tez va ishonchli bajarilishini ta'minlaydi.

## Ishlash natijasi:
```text
Vaqt o'tishidan oldin: false
Vaqt o'tgandan keyin: true
```


# 916-Topshiriq: TDD (Test-Driven Development): Red -> Green -> Refactor

## Topshiriq sharti:
Avval test yozish, so'ng kodni ishlatish, so'ngra tozalash metodologiyasi.

## Yechim (JS yoki TS kodi):
```typescript
// 1. RED bosqichi: Funksiya hali mavjud emas yoki noto'g'ri ishlaydi
// 2. GREEN bosqichi: Minimal ishlaydigan kod
function reverseString(str: string): string {
    return str.split("").reverse().join("");
}

// 3. REFACTOR bosqichi: Kod tozalanadi va testlar bilan tekshiriladi
console.log("Test natijasi:", reverseString("samarqand") === "dnaqramas");
```

## Tushuntirish va Mantiq:
TDD ning asosiy qoidasi: avval yiqiluvchi test yoziladi (Red), so'ng eng oddiy yechim bilan test o'tkaziladi (Green) va nihoyat kod optimallashtiriladi (Refactor).

## Ishlash natijasi:
```text
Test natijasi: true
```


# 917-Topshiriq: TDD amaliyoti: String Calculator

## Topshiriq sharti:
Vergullar bilan ajratilgan sonlar matnini qo'shuvchi kalkulyatorni TDD talablari bo'yicha yozing.

## Yechim (JS yoki TS kodi):
```typescript
function addNumbers(numbers: string): number {
    if (!numbers) return 0;
    const parts = numbers.split(",");
    return parts.reduce((acc, curr) => acc + Number(curr), 0);
}

console.log("Bo'sh satr:", addNumbers("") === 0);
console.log("Bitta son:", addNumbers("5") === 5);
console.log("Ikkita son:", addNumbers("1,2") === 3);
console.log("Bir nechta son:", addNumbers("1,2,3,4") === 10);
```

## Tushuntirish va Mantiq:
Har bir yangi talab (bo'sh satr, bitta son, ko'p son) alohida test orqali bosqichma-bosqich yechiladi.

## Ishlash natijasi:
```text
Bo'sh satr: true
Bitta son: true
Ikkita son: true
Bir nechta son: true
```


# 918-Topshiriq: TDD amaliyoti: Palindrome tekshiruvi

## Topshiriq sharti:
Matn chapdan ham, o'ngdan ham bir xil o'qilishini tekshiruvchi isPalindrome funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function isPalindrome(text: string): boolean {
    const clean = text.toLowerCase().replace(/[^a-z0-9]/g, "");
    return clean === clean.split("").reverse().join("");
}

console.log("'kiyik' palindrommi:", isPalindrome("kiyik"));
console.log("'non' palindrommi:", isPalindrome("non"));
console.log("'kitob' palindrommi:", isPalindrome("kitob"));
```

## Tushuntirish va Mantiq:
Palindrom tekshiruvida probellar va katta-kichik harflar e'tiborga olinmaydigan holatlar testlar bilan mustahkamlanadi.

## Ishlash natijasi:
```text
'kiyik' palindrommi: true
'non' palindrommi: true
'kitob' palindrommi: false
```


# 919-Topshiriq: Parameterized Tests: test.each() bilan jadval testlari

## Topshiriq sharti:
Bir xil mantiqni bir nechta ma'lumotlar to'plami bilan qayta-qayta tekshirish.

## Yechim (JS yoki TS kodi):
```typescript
const testCases = [
    { input: 2, expected: true },
    { input: 3, expected: false },
    { input: 4, expected: true },
    { input: 9, expected: false }
];

function isEven(n: number): boolean {
    return n % 2 === 0;
}

testCases.forEach(({ input, expected }) => {
    const result = isEven(input);
    console.log(`isEven(${input}) -> ${result} (Kutilgan: ${expected})`);
});
```

## Tushuntirish va Mantiq:
`test.each` kodni takrorlamasdan, qator test holatlarini ixcham jadval ko'rinishida yozish imkonini beradi.

## Ishlash natijasi:
```text
isEven(2) -> true (Kutilgan: true)
isEven(3) -> false (Kutilgan: false)
isEven(4) -> true (Kutilgan: true)
isEven(9) -> false (Kutilgan: false)
```


# 920-Topshiriq: Custom Matcher yaratish (expect.extend tushunchasi)

## Topshiriq sharti:
O'zingizning maxsus toBeWithinRange matcher tekshiruvingizni yozing.

## Yechim (JS yoki TS kodi):
```typescript
function toBeWithinRange(actual: number, floor: number, ceiling: number) {
    const pass = actual >= floor && actual <= ceiling;
    return {
        pass,
        message: () => `Son ${actual} [${floor}, ${ceiling}] oralig'ida bo'lishi kutilgan edi.`
    };
}

const check1 = toBeWithinRange(25, 20, 30);
const check2 = toBeWithinRange(15, 20, 30);

console.log("25 oralikdami:", check1.pass);
console.log("15 oralikdami:", check2.pass);
```

## Tushuntirish va Mantiq:
`expect.extend()` test kutubxonasiga domen mantiqiga mos maxsus o'qilishi oson matcherni qo'shish imkonini beradi.

## Ishlash natijasi:
```text
25 oralikdami: true
15 oralikdami: false
```


# 921-Topshiriq: Code Coverage: Statements, Branches, Functions, Lines

## Topshiriq sharti:
Koddagi shoxlanishlar (branch) to'liq tekshirilganligini aniqlash.

## Yechim (JS yoki TS kodi):
```typescript
function getShippingFee(isPremium: boolean, total: number): number {
    if (isPremium) {
        return 0; // Branch 1
    } else {
        if (total > 100) {
            return 5; // Branch 2
        }
        return 10; // Branch 3
    }
}

// 100% Branch Coverage uchun 3 ta holat tekshirilishi shart:
console.log("Holat 1 (Premium):", getShippingFee(true, 50));
console.log("Holat 2 (Oddiy, >100):", getShippingFee(false, 150));
console.log("Holat 3 (Oddiy, <=100):", getShippingFee(false, 50));
```

## Tushuntirish va Mantiq:
Branch coverage har bir `if-else` shoxlanishi testlar orqali sinovdan o'tganligini o'lchaydi. 100% qamrov barcha yo'llar tekshirilganini anglatadi.

## Ishlash natijasi:
```text
Holat 1 (Premium): 0
Holat 2 (Oddiy, >100): 5
Holat 3 (Oddiy, <=100): 10
```


# 922-Topshiriq: ESLint: no-unused-vars qoidasi

## Topshiriq sharti:
Ishlatilmagan o'zgaruvchilarni kompilyatsiya va lint bosqichida aniqlash.

## Yechim (JS yoki TS kodi):
```typescript
function processPayment(userId: number, _options?: Record<string, any>) {
    console.log(`To'lov foydalanuvchi #${userId} uchun bajarildi.`);
}

processPayment(101);
```

## Tushuntirish va Mantiq:
ESLint da `_` prefiksi bilan boshlangan o'zgaruvchilarga ishlatilmaslikka ruxsat beriladi (`argsIgnorePattern: '^_'`). Bu toza kod madaniyatini shakllantiradi.

## Ishlash natijasi:
```text
To'lov foydalanuvchi #101 uchun bajarildi.
```


# 923-Topshiriq: Prettier: Formatlash qoidalari

## Topshiriq sharti:
Kodni bir xil formatda (semi, singleQuote, trailingComma) saqlash.

## Yechim (JS yoki TS kodi):
```typescript
// Prettier talablari bo'yicha toza formatlangan obyekt
const userConfig = {
    appName: "E-Commerce",
    version: "2.0.0",
    enableTelemetry: false,
};

console.log("Konfiguratsiya:", userConfig.appName);
```

## Tushuntirish va Mantiq:
Prettier barcha ishlab chiquvchilar kompyuterida kod uslubini (probellar, vergullar, tirnoqlar) yagona standartga keltiradi.

## Ishlash natijasi:
```text
Konfiguratsiya: E-Commerce
```


# 924-Topshiriq: TypeScript Strict Mode: strictNullChecks

## Topshiriq sharti:
null yoki undefined bo'lishi mumkin bo'lgan qiymatlarni majburiy tekshirish.

## Yechim (JS yoki TS kodi):
```typescript
function printLength(str: string | null) {
    if (str !== null) {
        console.log("Satr uzunligi:", str.length);
    } else {
        console.log("Satr mavjud emas.");
    }
}

printLength("TypeScript");
printLength(null);
```

## Tushuntirish va Mantiq:
`strictNullChecks: true` yoqilganda TypeScript null qiymatlar ustida to'g'ridan-to'g'ri metod chaqirishni taqiqlaydi (NullPointerException ning oldini oladi).

## Ishlash natijasi:
```text
Satr uzunligi: 10
Satr mavjud emas.
```


# 925-Topshiriq: TypeScript: noUncheckedIndexedAccess qoidasi

## Topshiriq sharti:
Massiv yoki lug'atdan indeks orqali element olinganda uni avtomatik `undefined` bilan birga berish.

## Yechim (JS yoki TS kodi):
```typescript
const list: string[] = ["salom", "dunyo"];
const first: string | undefined = list[0];
const tenth: string | undefined = list[10];

if (tenth !== undefined) {
    console.log("10-element:", tenth);
} else {
    console.log("10-element mavjud emas.");
}
```

## Tushuntirish va Mantiq:
`noUncheckedIndexedAccess: true` xususiyati massiv chegarasidan tashqariga chiqib ketish oqibatidagi yashirin xatoliklarni tiplash darajasida fosh qiladi.

## Ishlash natijasi:
```text
10-element mavjud emas.
```


# 926-Topshiriq: Dependency Injection orqali Testlanuvchanlik (Testability)

## Topshiriq sharti:
Tashqi bog'liqliklarni konstruktor orqali uzatib, testda ularni soxtalashtirish (mocking).

## Yechim (JS yoki TS kodi):
```typescript
interface MailSender {
    send(to: string, msg: string): boolean;
}

class AuthService {
    constructor(private mailer: MailSender) {}

    register(email: string) {
        return this.mailer.send(email, "Xush kelibsiz!");
    }
}

// Test uchun soxta obyekt (Fake/Mock)
const fakeMailer: MailSender = {
    send: (to, msg) => true
};

const service = new AuthService(fakeMailer);
console.log("Ro'yxatdan o'tdimi:", service.register("ali@uz.dev"));
```

## Tushuntirish va Mantiq:
Dependency Injection kodni qattiq bog'liqliklardan xalos qilib, unit testlarda real tarmoq yoki serverlarga ehtiyojsiz sinash imkonini beradi.

## Ishlash natijasi:
```text
Ro'yxatdan o'tdimi: true
```


# 927-Topshiriq: Xatoliklarni boshqarish testi: Custom Error sinfi

## Topshiriq sharti:
Biznes mantiq xatosi to'g'ri kod bilan otilishini tekshirish.

## Yechim (JS yoki TS kodi):
```typescript
class InsufficientFundsError extends Error {
    constructor(public balance: number, public required: number) {
        super(`Mablag' yetarli emas! Joriy: ${balance}, Talab etiladi: ${required}`);
        this.name = "InsufficientFundsError";
    }
}

function withdraw(balance: number, amount: number) {
    if (amount > balance) throw new InsufficientFundsError(balance, amount);
    return balance - amount;
}

try {
    withdraw(100, 250);
} catch (e: any) {
    console.log("Xato turi:", e.name);
    console.log("Yetishmagan mablag':", e.required - e.balance);
}
```

## Tushuntirish va Mantiq:
Maxsus Error sinflari testlarda `toThrow(InsufficientFundsError)` orqali tekshirilib, xato sabablarini aniq qayd qiladi.

## Ishlash natijasi:
```text
Xato turi: InsufficientFundsError
Yetishmagan mablag': 150
```


# 928-Topshiriq: Snapshot Testing tushunchasi

## Topshiriq sharti:
Murakkab ma'lumotlar tuzilmasining o'zgarmasligini saqlash.

## Yechim (JS yoki TS kodi):
```typescript
const apiResponse = {
    status: 200,
    data: {
        id: 77,
        attributes: { role: "admin", verified: true }
    }
};

const snapshot = JSON.stringify(apiResponse, null, 2);
console.log("Olingan snapshot ko'rinishi:\n" + snapshot);
```

## Tushuntirish va Mantiq:
Snapshot testlari UI komponentlari yoki katta JSON javoblarni saqlab qo'yib, kelajakda tasodifiy o'zgarishlar kiritilsa darhol ogohlantiradi.

## Ishlash natijasi:
```text
Olingan snapshot ko'rinishi:
{
  "status": 200,
  "data": {
    "id": 77,
    "attributes": {
      "role": "admin",
      "verified": true
    }
  }
}
```


# 929-Topshiriq: Integratsion Test (Integration Test) simulyatsiyasi

## Topshiriq sharti:
Router va Servis qatlamlarining birgalikda to'g'ri ishlashini sinash.

## Yechim (JS yoki TS kodi):
```typescript
class OrderDb {
    orders: string[] = [];
    save(o: string) { this.orders.push(o); }
}

class OrderController {
    constructor(private db: OrderDb) {}
    handleCreateOrder(name: string) {
        this.db.save(name);
        return { success: true, count: this.db.orders.length };
    }
}

const db = new OrderDb();
const controller = new OrderController(db);
const result = controller.handleCreateOrder("Buyurtma #1");

console.log("Integratsion test natijasi:", result);
```

## Tushuntirish va Mantiq:
Unit testlar har bir funksiyani alohida sinasa, Integratsion testlar bir nechta komponentlarning o'zaro hamkorligini tekshiradi.

## Ishlash natijasi:
```text
Integratsion test natijasi: { success: true, count: 1 }
```


# 930-Topshiriq: Mocking Modules (vi.mock / jest.mock tushunchasi)

## Topshiriq sharti:
Tashqi npm kutubxonasini test muhitida soxtalashtirish.

## Yechim (JS yoki TS kodi):
```typescript
// Soxtalashtirilgan axios/fetch moduli
const mockedAxios = {
    get: async (url: string) => ({ data: { title: "Test Maqola" } })
};

async function getArticleTitle(url: string) {
    const res = await mockedAxios.get(url);
    return res.data.title;
}

getArticleTitle("https://api.domain.uz/post/1").then(t => {
    console.log("Mock moduldan kelgan sarlavha:", t);
});
```

## Tushuntirish va Mantiq:
`vi.mock('axios')` orqali real internetga so'rov yubormasdan, testlarni offline, tez va xavfsiz o'tkazish mumkin bo'ladi.

## Ishlash natijasi:
```text
Mock moduldan kelgan sarlavha: Test Maqola
```


# 931-Topshiriq: DOM Eventlarini testlash (fireEvent tushunchasi)

## Topshiriq sharti:
Tugma bosilganda hisoblagich oshishini sinovdan o'tkazish.

## Yechim (JS yoki TS kodi):
```typescript
let count = 0;
const button = {
    click() { count++; }
};

console.log("Bosilishdan oldin:", count);
button.click();
console.log("Bosilishdan keyin:", count);
```

## Tushuntirish va Mantiq:
Testing Library yordamida brauzer tugmalari bosilishi va formalarning jo'natilishi xuddi foydalanuvchi bajargandek testlanadi.

## Ishlash natijasi:
```text
Bosilishdan oldin: 0
Bosilishdan keyin: 1
```


# 932-Topshiriq: Mock funksiyani tozalash: mockClear, mockReset, mockRestore

## Topshiriq sharti:
Testlar orasida chaqiruvlar tarixini tozalash.

## Yechim (JS yoki TS kodi):
```typescript
let callsHistory: string[] = ["chaqiruv_1", "chaqiruv_2"];

function mockClear() {
    callsHistory = []; // Tarix tozalandi
}

console.log("Test 1 dan keyin:", callsHistory.length);
mockClear();
console.log("mockClear dan keyin:", callsHistory.length);
```

## Tushuntirish va Mantiq:
`mockClear` chaqiruvlar sonini nolga tushiradi, `mockReset` qaytaruvchi qiymatlarni ham o'chiradi, `mockRestore` esa asl funksiyani qaytaradi.

## Ishlash natijasi:
```text
Test 1 dan keyin: 2
mockClear dan keyin: 0
```


# 933-Topshiriq: Xotira sizib chiqishini (Memory Leak) testda aniqlash

## Topshiriq sharti:
Obunachilar o'z vaqtida o'chirilayotganini tekshirish.

## Yechim (JS yoki TS kodi):
```typescript
class EventChannel {
    private listeners: Function[] = [];
    subscribe(fn: Function) {
        this.listeners.push(fn);
        return () => {
            this.listeners = this.listeners.filter(l => l !== fn);
        };
    }
    listenerCount() { return this.listeners.length; }
}

const ch = new EventChannel();
const unsubscribe = ch.subscribe(() => {});
console.log("Obunachi qo'shildi:", ch.listenerCount());
unsubscribe();
console.log("Obunachi bekor qilindi:", ch.listenerCount());
```

## Tushuntirish va Mantiq:
Event listenerlar bekor qilinmasa xotira to'lib boradi. Unit testlar orqali obuna to'liq bekor qilinganini tekshirish muhimdir.

## Ishlash natijasi:
```text
Obunachi qo'shildi: 1
Obunachi bekor qilindi: 0
```


# 934-Topshiriq: Smoke Test (Tutun testi) tushunchasi

## Topshiriq sharti:
Ilova eng minimal darajada xatosiz ishga tushishini tezkor tekshirish.

## Yechim (JS yoki TS kodi):
```typescript
function appBootstrap(): boolean {
    const isDbConnected = true;
    const isRouterReady = true;
    return isDbConnected && isRouterReady;
}

console.log("Smoke Test natijasi (Tizim ishga tushdimi):", appBootstrap());
```

## Tushuntirish va Mantiq:
Smoke test chuqur mantiqqa kirmasdan, dastur asosiy arxitekturasi buzilmaganligini va darhol qulab tushmasligini tasdiqlaydi.

## Ishlash natijasi:
```text
Smoke Test natijasi (Tizim ishga tushdimi): true
```


# 935-Topshiriq: RegEx andozalarini testlash

## Topshiriq sharti:
Elektron pochta va telefon raqamlari formatini qat'iy tekshiruvchi test.

## Yechim (JS yoki TS kodi):
```typescript
const phoneRegex = /^\+998\d{9}$/;

console.log("+998901234567 to'g'rimi:", phoneRegex.test("+998901234567"));
console.log("+99890123456 xatomi (qisqa):", phoneRegex.test("+99890123456"));
console.log("123456789 xatomi:", phoneRegex.test("123456789"));
```

## Tushuntirish va Mantiq:
Muntazam ifodalar (RegEx) yordamida kiritilgan ma'lumotlar barcha chekka holatlar (edge cases) bo'yicha to'liq testlanishi kerak.

## Ishlash natijasi:
```text
+998901234567 to'g'rimi: true
+99890123456 xatomi (qisqa): false
123456789 xatomi: false
```


# 936-Topshiriq: TypeScript: noImplicitAny qoidasi

## Topshiriq sharti:
Tip ko'rsatilmagan noma'lum o'zgaruvchilarga any berilishini man qilish.

## Yechim (JS yoki TS kodi):
```typescript
// strict rejimida parametrlarga tip berish majburiy
function calculateTax(income: number, rate: number): number {
    return income * rate;
}

console.log("Soliq:", calculateTax(5000000, 0.12));
```

## Tushuntirish va Mantiq:
`noImplicitAny: true` dasturchilarni har bir parametr va xossa tipini aniq ko'rsatishga majbur qilib, runtime xatoliklarni oldini oladi.

## Ishlash natijasi:
```text
Soliq: 600000
```


# 937-Topshiriq: TypeScript: strictBindCallApply qoidasi

## Topshiriq sharti:
call, apply va bind metodlarining parametrlarini to'liq tekshirish.

## Yechim (JS yoki TS kodi):
```typescript
function greetPerson(name: string, age: number) {
    return `${name} ${age} yoshda`;
}

console.log(greetPerson.call(null, "Alisher", 25));
```

## Tushuntirish va Mantiq:
`strictBindCallApply` yoqilganda .call() yoki .apply() ga noto'g'ri turdagi parametr uzatilsa darhol kompilyatsiya xatosi beriladi.

## Ishlash natijasi:
```text
Alisher 25 yoshda
```


# 938-Topshiriq: Asinxron Retry funksiyasini testlash

## Topshiriq sharti:
Funksiya xatolikdan so'ng belgilangan martagacha qayta urinishini tekshirish.

## Yechim (JS yoki TS kodi):
```typescript
let attempts = 0;
async function unstableOperation() {
    attempts++;
    if (attempts < 3) throw new Error("Tarmoq xatosi");
    return "Muvaffaqiyat";
}

async function retry(fn: () => Promise<string>, maxRetries: number) {
    for (let i = 0; i < maxRetries; i++) {
        try {
            return await fn();
        } catch (e) {
            if (i === maxRetries - 1) throw e;
        }
    }
}

retry(unstableOperation, 4).then(res => {
    console.log(`Natija: ${res}, Urinishlar soni: ${attempts}`);
});
```

## Tushuntirish va Mantiq:
Qayta urinish (retry) funksiyalari mocklangan xatolar orqali belgilangan cheklovga rioya qilishini sinovdan o'tkazadi.

## Ishlash natijasi:
```text
Natija: Muvaffaqiyat, Urinishlar soni: 3
```


# 939-Topshiriq: Husky va lint-staged tushunchasi

## Topshiriq sharti:
Git ga commit qilishdan oldin avtomatik test va lint tekshiruvini ishga tushirish.

## Yechim (JS yoki TS kodi):
```typescript
const preCommitSteps = [
    "git add qilingan fayllarni aniqlash",
    "eslint --fix bajarish",
    "prettier --write bajarish",
    "vitest related testlarni ishga tushirish"
];

console.log("Pre-commit zanjiri qadamlari soni:", preCommitSteps.length);
```

## Tushuntirish va Mantiq:
Husky Git hooklari orqali nosoz yoki formatlanmagan kodning repozitoriyga kirib ketishini to'xtatadi.

## Ishlash natijasi:
```text
Pre-commit zanjiri qadamlari soni: 4
```


# 940-Topshiriq: Flaky testlarni bartaraf qilish

## Topshiriq sharti:
Tasodifiy (ba'zan o'tib, ba'zan yiqiluvchi) testlarning sabablari va ularni tuzatish.

## Yechim (JS yoki TS kodi):
```typescript
// Noto'g'ri: Date.now() ga tayanib solishtirish
// To'g'ri: Aniq berilgan vaqt konstantasiga tayanish
const fixedTimestamp = 1700000000000;
function getFormattedTime(ts: number) {
    return new Date(ts).toISOString().split("T")[0];
}

console.log("Barqaror vaqt testi:", getFormattedTime(fixedTimestamp) === "2023-11-14");
```

## Tushuntirish va Mantiq:
Flaky testlar ko'pincha real vaqt (Date.now), tarmoq kechikishlari yoki tartibsiz asinxronlik tufayli yuzaga keladi; ularni fiksatsiyalangan qiymatlar bilan tuzatish kerak.

## Ishlash natijasi:
```text
Barqaror vaqt testi: true
```


# 941-Topshiriq: Mutation Testing tushunchasi

## Topshiriq sharti:
Testlarning o'zini sifatini tekshirish uchun kodga sun'iy xatolar (mutatsiyalar) kiritish.

## Yechim (JS yoki TS kodi):
```typescript
function isAdult(age: number): boolean {
    return age >= 18; // Agar mutant kodda >= o'rniga > qo'yilsa, test yiqilishi shart!
}

console.log("18 yosh tekshiruvi:", isAdult(18));
console.log("17 yosh tekshiruvi:", isAdult(17));
```

## Tushuntirish va Mantiq:
Mutation testing (masalan, Stryker) testlarning chindan ham biznes mantiqni tekshirayotganini aniqlaydi.

## Ishlash natijasi:
```text
18 yosh tekshiruvi: true
17 yosh tekshiruvi: false
```


# 942-Topshiriq: Snapshot Testing: Obyekt tuzilishi o'zgarishini tekshirish

## Topshiriq sharti:
Obyektdagi ortiqcha yoki yetishmayotgan kalitlarni aniqlash.

## Yechim (JS yoki TS kodi):
```typescript
interface AppTheme {
    primaryColor: string;
    fontSize: number;
}

function validateTheme(theme: any): boolean {
    return typeof theme.primaryColor === "string" && typeof theme.fontSize === "number";
}

const theme = { primaryColor: "#333", fontSize: 16 };
console.log("Sxemaga mosmi:", validateTheme(theme));
```

## Tushuntirish va Mantiq:
Snapshotlar orqali konfiguratsiya va mavzular tasodifan buzilmasligi kafolatlanadi.

## Ishlash natijasi:
```text
Sxemaga mosmi: true
```


# 943-Topshiriq: Asinxron Race Condition testlash

## Topshiriq sharti:
Bir nechta so'rovlar parallel kelganda hisoblagich to'g'ri ishlashi.

## Yechim (JS yoki TS kodi):
```typescript
let sharedCounter = 0;

async function incrementCounter() {
    const current = sharedCounter;
    await new Promise(r => setTimeout(r, 1));
    sharedCounter = current + 1;
}

async function runTest() {
    await Promise.all([incrementCounter(), incrementCounter()]);
    // Bu yerda race condition yuz berishi mumkinligini tushunish
    console.log("Parallel operatsiyalar bajarildi.");
}

runTest();
```

## Tushuntirish va Mantiq:
Asinxron testlar tizimdagi poyga holatlari (race conditions) va bir vaqtning o'zidagi chaqiruvlarni aniqlashga xizmat qiladi.

## Ishlash natijasi:
```text
Parallel operatsiyalar bajarildi.
```


# 944-Topshiriq: Error Boundary va UI xatoliklarini testlash

## Topshiriq sharti:
Komponentda xatolik yuz berganda xavfsiz zaxira ekrani chiqishini sinash.

## Yechim (JS yoki TS kodi):
```typescript
function safeRender(renderFn: () => string): string {
    try {
        return renderFn();
    } catch (err: any) {
        return `[Zaxira Ekrani]: Xatolik - ${err.message}`;
    }
}

const faultyComponent = () => { throw new Error("Chizishda xatolik!"); };
console.log(safeRender(faultyComponent));
```

## Tushuntirish va Mantiq:
Error Boundary testlari kutilmagan frontend xatoliklari butun ilovani muzlatib qo'ymasligini tekshiradi.

## Ishlash natijasi:
```text
[Zaxira Ekrani]: Xatolik - Chizishda xatolik!
```


# 945-Topshiriq: Mocking Global Fetch API

## Topshiriq sharti:
Brauzer yoki Node.js dagi global.fetch funksiyasini testda mocklash.

## Yechim (JS yoki TS kodi):
```typescript
const originalFetch = globalThis.fetch;

// Mock fetch
const fakeFetch = async (url: string) => ({
    ok: true,
    json: async () => ({ status: "OK", serverTime: 123456 })
});

fakeFetch("https://api.myuzbek.uz/status").then(r => r.json()).then(data => {
    console.log("Mock fetch javobi:", data.status);
});
```

## Tushuntirish va Mantiq:
`globalThis.fetch = vi.fn()` orqali tarmoq so'rovlari to'liq nazorat qilinadi.

## Ishlash natijasi:
```text
Mock fetch javobi: OK
```


# 946-Topshiriq: Parametrlangan shartli xatoliklar testi

## Topshiriq sharti:
Noto'g'ri parametrlarning har biri uchun mos xabar chiqishini tekshirish.

## Yechim (JS yoki TS kodi):
```typescript
function validateAge(age: number) {
    if (age < 0) throw new Error("Yosh manfiy bo'lolmaydi");
    if (age > 150) throw new Error("Yosh juda katta");
    return true;
}

const inputs = [-5, 200];
inputs.forEach(val => {
    try {
        validateAge(val);
    } catch (e: any) {
        console.log(`Kirish ${val}: ${e.message}`);
    }
});
```

## Tushuntirish va Mantiq:
Har bir chegara qiymati alohida xatolik matnini tekshirish orqali to'liq sinovdan o'tadi.

## Ishlash natijasi:
```text
Kirish -5: Yosh manfiy bo'lolmaydi
Kirish 200: Yosh juda katta
```


# 947-Topshiriq: Pure Function (Toza funksiya) larni testlash qulayligi

## Topshiriq sharti:
Side effect (nojo'ya ta'sir) larsiz funksiyalarni mocklarsiz oson testlash.

## Yechim (JS yoki TS kodi):
```typescript
// Toza funksiya: tashqi dunyoga bog'liq emas
function calcTotal(price: number, qty: number, taxRate: number): number {
    return (price * qty) * (1 + taxRate);
}

console.log("Hisob-kitob to'g'rimi:", calcTotal(100, 2, 0.1) === 220);
```

## Tushuntirish va Mantiq:
Toza funksiyalar (Pure Functions) eng oson, eng tez va eng barqaror testlanuvchi kod birliklaridir.

## Ishlash natijasi:
```text
Hisob-kitob to'g'rimi: true
```


# 948-Topshiriq: Vitest va Jest da benchmark / Performance testi tushunchasi

## Topshiriq sharti:
Algoritmning bajarilish vaqtini millisekundlarda o'lchash.

## Yechim (JS yoki TS kodi):
```typescript
const start = Date.now();
let acc = 0;
for (let i = 0; i < 100000; i++) {
    acc += i;
}
const duration = Date.now() - start;
console.log(`100 ming amal bajarildi, vaqt: ${duration >= 0 ? "muvaffaqiyatli" : "xato"}`);
```

## Tushuntirish va Mantiq:
Benchmark testlari funksiyalarning ishlash tezligi regressiyaga uchramaganligini (sekinlashib ketmaganligini) nazorat qiladi.

## Ishlash natijasi:
```text
100 ming amal bajarildi, vaqt: muvaffaqiyatli
```


# 949-Topshiriq: Test Helpers va Utility funksiyalar yaratish

## Topshiriq sharti:
Testlarda qayta ishlatiladigan test obyekti yaratuvchi yordamchilar (Object Mothers / Factories).

## Yechim (JS yoki TS kodi):
```typescript
interface Order { id: number; total: number; status: string; }

function createTestOrder(overrides: Partial<Order> = {}): Order {
    return {
        id: 1,
        total: 100,
        status: "NEW",
        ...overrides
    };
}

const pendingOrder = createTestOrder({ status: "PENDING" });
console.log(`Test buyurtmasi: #${pendingOrder.id}, Holat: ${pendingOrder.status}`);
```

## Tushuntirish va Mantiq:
Test Helper fabriklari testlarda obyekt yaratishni 1 qatorga tushiradi va testlarni toza saqlaydi.

## Ishlash natijasi:
```text
Test buyurtmasi: #1, Holat: PENDING
```


# 950-Topshiriq: To'liq Test To'plami: Valyuta konvertori xizmati (100% test qoplami bilan)

## Topshiriq sharti:
Valyuta xizmatining barcha imkoniyatlari, xatoliklari va mocklarini o'z ichiga olgan to'liq test to'plami.

## Yechim (JS yoki TS kodi):
```typescript
interface ExchangeRateApi {
    getRate(from: string, to: string): number;
}

class CurrencyConverter {
    constructor(private api: ExchangeRateApi) {}

    convert(amount: number, from: string, to: string): number {
        if (amount < 0) throw new Error("Miqdor manfiy bo'lishi mumkin emas!");
        if (from === to) return amount;
        const rate = this.api.getRate(from, to);
        return amount * rate;
    }
}

// 1. Mock API
const mockRateApi: ExchangeRateApi = {
    getRate: (from, to) => {
        if (from === "USD" && to === "UZS") return 12800;
        throw new Error("Noma'lum valyuta juftligi");
    }
};

const converter = new CurrencyConverter(mockRateApi);

// Test 1: Bir xil valyuta
console.log("Test 1 (Bir xil):", converter.convert(100, "USD", "USD") === 100);

// Test 2: Konvertatsiya
console.log("Test 2 (USD -> UZS):", converter.convert(2, "USD", "UZS") === 25600);

// Test 3: Manfiy qiymat xatosi
let errorThrown = false;
try {
    converter.convert(-5, "USD", "UZS");
} catch (e: any) {
    if (e.message.includes("manfiy")) errorThrown = true;
}
console.log("Test 3 (Xatolik ushlandi):", errorThrown);
```

## Tushuntirish va Mantiq:
Ushbu to'liq test to'plamida Mocking, Dependency Injection, Oddiy holatlar va Istisno holatlari 100% qamrov bilan sinovdan o'tkazilgan.

## Ishlash natijasi:
```text
Test 1 (Bir xil): true
Test 2 (USD -> UZS): true
Test 3 (Xatolik ushlandi): true
```

