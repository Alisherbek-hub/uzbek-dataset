# 801-Topshiriq: Sinf deklaratsiyasi va metodlar

## Topshiriq sharti:
Oddiy Car sinfini e'lon qiling, uning maydonlari (brand, speed) va harakatlanish metodini yozing.

## Yechim (JS yoki TS kodi):
```typescript
class Car {
    brand: string;
    speed: number;

    constructor(brand: string, speed: number = 0) {
        this.brand = brand;
        this.speed = speed;
    }

    accelerate(amount: number): void {
        this.speed += amount;
        console.log(`${this.brand} tezligi oshdi: ${this.speed} km/soat`);
    }
}

const myCar = new Car("Chevrolet", 60);
myCar.accelerate(20);
```

## Tushuntirish va Mantiq:
TypeScript da sinf maydonlari aniq tiplar bilan e'lon qilinadi va constructor orqali boshlang'ich qiymat beriladi.

## Ishlash natijasi:
```text
Chevrolet tezligi oshdi: 80 km/soat
```


# 802-Topshiriq: Kirish modifikatorlari: public (sukut bo'yicha)

## Topshiriq sharti:
Ommaviy xossa va metodlarga tashqi koddan to'g'ridan-to'g'ri murojaat qilish.

## Yechim (JS yoki TS kodi):
```typescript
class Book {
    public title: string;
    public author: string;

    constructor(title: string, author: string) {
        this.title = title;
        this.author = author;
    }

    public getDetails(): string {
        return `"${this.title}" - ${this.author}`;
    }
}

const book = new Book("O'tkan kunlar", "Abdulla Qodiriy");
console.log(book.title);
console.log(book.getDetails());
```

## Tushuntirish va Mantiq:
Sinf a'zolari oldiga hech narsa yozilmasa, ular sukut bo'yicha 'public' hisoblanadi va istalgan joydan murojaat qilish mumkin.

## Ishlash natijasi:
```text
O'tkan kunlar
"O'tkan kunlar" - Abdulla Qodiriy
```


# 803-Topshiriq: Kirish modifikatorlari: private

## Topshiriq sharti:
Bank hisobidagi balansni tashqi o'zgartirishlardan 'private' yordamida himoyalash.

## Yechim (JS yoki TS kodi):
```typescript
class BankAccount {
    private balance: number = 0;

    deposit(amount: number): void {
        if (amount > 0) {
            this.balance += amount;
            console.log(`Balansga ${amount} qo'shildi.`);
        }
    }

    getBalance(): number {
        return this.balance;
    }
}

const acc = new BankAccount();
acc.deposit(500);
// acc.balance; // Xatolik: balance xususiy (private) maydon!
console.log("Joriy balans:", acc.getBalance());
```

## Tushuntirish va Mantiq:
private modifikatori xossa yoki metodga faqat o'sha sinfning o'zidan murojaat qilishga ruxsat beradi, bu inkapsulyatsiyaning asosi hisoblanadi.

## Ishlash natijasi:
```text
Balansga 500 qo'shildi.
Joriy balans: 500
```


# 804-Topshiriq: Kirish modifikatorlari: protected

## Topshiriq sharti:
Ota sinfdagi 'protected' maydonga faqat voris (merosxo'r) sinf ichidan kirish.

## Yechim (JS yoki TS kodi):
```typescript
class Employee {
    protected baseSalary: number;

    constructor(baseSalary: number) {
        this.baseSalary = baseSalary;
    }
}

class Manager extends Employee {
    private bonus: number;

    constructor(baseSalary: number, bonus: number) {
        super(baseSalary);
        this.bonus = bonus;
    }

    getTotalCompensation(): number {
        return this.baseSalary + this.bonus; // baseSalary protected bo'lgani uchun ochiq
    }
}

const mgr = new Manager(4000, 1500);
console.log("Menejer umumiy oyligi:", mgr.getTotalCompensation());
```

## Tushuntirish va Mantiq:
protected modifikatori sinf a'zolarini tashqaridan yashiradi, biroq 'extends' qilingan voris sinflar ichida bevosita foydalanish imkonini beradi.

## Ishlash natijasi:
```text
Menejer umumiy oyligi: 5500
```


# 805-Topshiriq: ECMAScript private maydonlari (#field) vs TS private

## Topshiriq sharti:
Haqiqiy runtime darajasidagi `#field` xavfsizligi va TypeScript kompilyatsiya darajasidagi `private` farqi.

## Yechim (JS yoki TS kodi):
```typescript
class SecureVault {
    #secretKey: string = "X-SECURE-KEY-99";
    private tsSecret: string = "TS-ONLY-PRIVATE";

    getSecretPreview(): string {
        return `ECMA: ${this.#secretKey.slice(0, 4)}... | TS: ${this.tsSecret.slice(0, 4)}...`;
    }
}

const vault = new SecureVault();
console.log(vault.getSecretPreview());
// (vault as any).tsSecret -> JS da ishlaydi
// (vault as any)["#secretKey"] -> Ishlamaydi, haqiqiy JavaScript darajasida xususiy!
```

## Tushuntirish va Mantiq:
#prefiksli maydonlar ECMAScript xususiy maydonlari bo'lib, ular runtime darajasida (hattoki 'as any' bilan ham) tashqaridan o'qib bo'lmaydigan qilib qattiq himoyalangan.

## Ishlash natijasi:
```text
ECMA: X-SE... | TS: TS-O...
```


# 806-Topshiriq: Parameter Properties - Konstruktorda qisqa e'lon qilish

## Topshiriq sharti:
Konstruktor parametrlariga public/private/protected berish orqali sinf maydonlarini bir qatorda yaratish.

## Yechim (JS yoki TS kodi):
```typescript
class UserProfile {
    constructor(
        public readonly id: number,
        public username: string,
        private email: string
    ) {}

    getEmail(): string {
        return this.email;
    }
}

const user = new UserProfile(1, "dilshod", "dilshod@dev.uz");
console.log(`ID: ${user.id}, Username: ${user.username}, Email: ${user.getEmail()}`);
```

## Tushuntirish va Mantiq:
Konstruktor argumentlari oldiga kirish modifikatori yoki readonly qo'yilganda, TypeScript avtomatik ravishda shu nomdagi maydonni e'lon qiladi va qiymatni biriktiradi.

## Ishlash natijasi:
```text
ID: 1, Username: dilshod, Email: dilshod@dev.uz
```


# 807-Topshiriq: readonly maydonlar sinfda

## Topshiriq sharti:
Faqat konstruktorda qiymat beriladigan va keyinchalik o'zgartirib bo'lmaydigan maydonlar.

## Yechim (JS yoki TS kodi):
```typescript
class ServerConfig {
    readonly createdAt: Date = new Date();
    readonly host: string;

    constructor(host: string) {
        this.host = host;
    }
}

const conf = new ServerConfig("api.uzcloud.uz");
console.log("Xost:", conf.host);
// conf.host = "other"; // Xatolik: faqat o'qish mumkin!
```

## Tushuntirish va Mantiq:
readonly maydonlar obyekt tuzilgandan so'ng qayta yozilmasligini kafolatlaydi.

## Ishlash natijasi:
```text
Xost: api.uzcloud.uz
```


# 808-Topshiriq: Getters va Setters (get va set aksessorlari)

## Topshiriq sharti:
Haroratni Selsiy bo'yicha saqlab, Farengeyt bo'yicha getter va setter orqali o'qish va yangilash.

## Yechim (JS yoki TS kodi):
```typescript
class Temperature {
    private _celsius: number = 0;

    get celsius(): number {
        return this._celsius;
    }

    set celsius(val: number) {
        if (val < -273.15) throw new Error("Mutlaq noldan past bo'lishi mumkin emas!");
        this._celsius = val;
    }

    get fahrenheit(): number {
        return this._celsius * 1.8 + 32;
    }

    set fahrenheit(val: number) {
        this.celsius = (val - 32) / 1.8;
    }
}

const temp = new Temperature();
temp.celsius = 25;
console.log(`Selsiy: ${temp.celsius}°C, Farengeyt: ${temp.fahrenheit}°F`);
temp.fahrenheit = 68;
console.log(`Farengeytdan keyin Selsiy: ${temp.celsius}°C`);
```

## Tushuntirish va Mantiq:
get va set metodlari xossaga murojaat qilinganda maxsus mantiq, validatsiya yoki hisob-kitobni bajarish imkonini beradi.

## Ishlash natijasi:
```text
Selsiy: 25°C, Farengeyt: 77°F
Farengeytdan keyin Selsiy: 20°C
```


# 809-Topshiriq: Sinf merosxo'rligi (extends va super)

## Topshiriq sharti:
Asosiy Animal sinfidan meros oluvchi Dog sinfini yozing.

## Yechim (JS yoki TS kodi):
```typescript
class Animal {
    constructor(public name: string) {}

    makeSound(): void {
        console.log(`${this.name} ovoz chiqardi.`);
    }
}

class Dog extends Animal {
    constructor(name: string, public breed: string) {
        super(name); // Ota sinf konstruktorini chaqirish shart
    }

    makeSound(): void {
        console.log(`${this.name} (${this.breed}) vovilladi!`);
    }
}

const dog = new Dog("Bo'rikalla", "Ov iti");
dog.makeSound();
```

## Tushuntirish va Mantiq:
Voris sinf ota sinf konstruktorini super(...) orqali chaqirishi va ota sinf metodlarini override qilishi mumkin.

## Ishlash natijasi:
```text
Bo'rikalla (Ov iti) vovilladi!
```


# 810-Topshiriq: Metodni qayta aniqlash (Method Overriding) va super.method()

## Topshiriq sharti:
Ota sinf metodining natijasiga qo'shimcha mantiq qo'shib qaytarish.

## Yechim (JS yoki TS kodi):
```typescript
class Printer {
    print(content: string): void {
        console.log(`[ODDIY CHOP ETISH]: ${content}`);
    }
}

class ColorPrinter extends Printer {
    print(content: string): void {
        console.log("Rangli kartrij tayyorlandi...");
        super.print(content);
        console.log("Ranglar quritildi.");
    }
}

const cp = new ColorPrinter();
cp.print("Shartnoma.pdf");
```

## Tushuntirish va Mantiq:
super.metod() orqali voris sinf ota sinfning asl metodini to'g'ridan-to'g'ri chaqirib, uning ustiga qo'shimcha xatti-harakat qo'shishi mumkin.

## Ishlash natijasi:
```text
Rangli kartrij tayyorlandi...
[ODDIY CHOP ETISH]: Shartnoma.pdf
Ranglar quritildi.
```


# 811-Topshiriq: Abstrakt sinflar (Abstract Classes)

## Topshiriq sharti:
O'zidan bevosita obyekt yaratib bo'lmaydigan, faqat meros olish uchun mo'ljallangan abstrakt sinf.

## Yechim (JS yoki TS kodi):
```typescript
abstract class Shape {
    constructor(public color: string) {}

    abstract getArea(): number; // Vorislar amalga oshirishi shart

    describe(): void {
        console.log(`Rangi: ${this.color}, Yuzi: ${this.getArea()}`);
    }
}

class Rectangle extends Shape {
    constructor(color: string, private w: number, private h: number) {
        super(color);
    }

    getArea(): number {
        return this.w * this.h;
    }
}

const rect = new Rectangle("Yashil", 5, 10);
rect.describe();
```

## Tushuntirish va Mantiq:
abstract class yangi instansiya hosil qilishni (new Shape) taqiqlaydi va voris sinflarga umumiy xatti-harakatlar va andozalarni taqdim etadi.

## Ishlash natijasi:
```text
Rangi: Yashil, Yuzi: 50
```


# 812-Topshiriq: Interfeysni amalga oshirish (implements)

## Topshiriq sharti:
Sinf interfeysda e'lon qilingan barcha talablarni to'liq bajarishi kerakligini ta'minlash.

## Yechim (JS yoki TS kodi):
```typescript
interface Serializable {
    serialize(): string;
}

class UserRecord implements Serializable {
    constructor(public id: number, public name: string) {}

    serialize(): string {
        return JSON.stringify({ id: this.id, name: this.name });
    }
}

const rec = new UserRecord(101, "Jamshid");
console.log("Seriyalangan:", rec.serialize());
```

## Tushuntirish va Mantiq:
implements kalit so'zi sinfning belgilangan interfeys shartnomasi (contract) bo'yicha to'liq tuzilganligini kompilyatsiya vaqtida tekshiradi.

## Ishlash natijasi:
```text
Seriyalangan: {"id":101,"name":"Jamshid"}
```


# 813-Topshiriq: Bir nechta interfeyslarni amalga oshirish

## Topshiriq sharti:
Sinf bir vaqtning o'zida ham Logger, ham Notifier interfeyslarini bajarishi.

## Yechim (JS yoki TS kodi):
```typescript
interface Logger {
    log(msg: string): void;
}

interface Notifier {
    sendAlert(text: string): void;
}

class SystemAlertManager implements Logger, Notifier {
    log(msg: string): void {
        console.log(`LOG: ${msg}`);
    }

    sendAlert(text: string): void {
        console.log(`ALERT: ${text}`);
    }
}

const manager = new SystemAlertManager();
manager.log("Tizim tekshiruvi");
manager.sendAlert("Disk to'ldi");
```

## Tushuntirish va Mantiq:
TypeScript sinflari faqat bitta ota sinfdan meros olishi (single inheritance) mumkin, lekin cheksiz ko'p interfeyslarni implements qila oladi.

## Ishlash natijasi:
```text
LOG: Tizim tekshiruvi
ALERT: Disk to'ldi
```


# 814-Topshiriq: Statik xossalar va metodlar (static)

## Topshiriq sharti:
Sinf instansiyasini yaratmasdan to'g'ridan-to'g'ri sinf nomidan chaqiriladigan a'zolar.

## Yechim (JS yoki TS kodi):
```typescript
class MathUtility {
    static readonly PI = 3.14159;

    static circleArea(radius: number): number {
        return this.PI * radius * radius;
    }
}

console.log("PI qiymati:", MathUtility.PI);
console.log("Doira yuzi (r=3):", MathUtility.circleArea(3));
```

## Tushuntirish va Mantiq:
static bilan belgilangan metod va maydonlar alohida obyektga emas, balki sinf funksiyasining o'ziga biriktiriladi.

## Ishlash natijasi:
```text
PI qiymati: 3.14159
Doira yuzi (r=3): 28.27431
```


# 815-Topshiriq: Statik inisializatsiya bloklari (Static Blocks)

## Topshiriq sharti:
Sinf birinchi marta yuklanganda murakkab statik konfiguratsiyani ishga tushirish.

## Yechim (JS yoki TS kodi):
```typescript
class AppDatabase {
    static connectionString: string;

    static {
        const env = "prod";
        if (env === "prod") {
            AppDatabase.connectionString = "postgres://prod-db:5432/main";
        } else {
            AppDatabase.connectionString = "postgres://localhost:5432/test";
        }
    }
}

console.log("Baza manzili:", AppDatabase.connectionString);
```

## Tushuntirish va Mantiq:
static { ... } bloki sinf e'lon qilinganda bir marta ishlaydi va statik xususiy maydonlarni ham sozlash imkonini beradi.

## Ishlash natijasi:
```text
Baza manzili: postgres://prod-db:5432/main
```


# 816-Topshiriq: Singleton dizayn naqshi

## Topshiriq sharti:
Butun ilova davomida yagona instansiyaga ega bo'lgan AppConfig sinfini yozing.

## Yechim (JS yoki TS kodi):
```typescript
class AppConfig {
    private static instance: AppConfig | null = null;
    public appName = "Yagona Ilova";

    private constructor() {} // Tashqaridan new qilib bo'lmaydi

    public static getInstance(): AppConfig {
        if (!AppConfig.instance) {
            AppConfig.instance = new AppConfig();
        }
        return AppConfig.instance;
    }
}

const c1 = AppConfig.getInstance();
const c2 = AppConfig.getInstance();

console.log("Ikkala instansiya tengmi:", c1 === c2);
```

## Tushuntirish va Mantiq:
private constructor va static getInstance metodi Singleton naqshining yadrosi bo'lib, butun dasturda yagona obyekt nusxasini kafolatlaydi.

## Ishlash natijasi:
```text
Ikkala instansiya tengmi: true
```


# 817-Topshiriq: Generic Sinf (Generic Class) OOP da

## Topshiriq sharti:
Xotirada ma'lumotlarni saqlovchi generic Key-Value omborini sinf yordamida yarating.

## Yechim (JS yoki TS kodi):
```typescript
class KeyValueStore<K extends string | number, V> {
    private store = new Map<K, V>();

    set(key: K, value: V): void {
        this.store.set(key, value);
    }

    get(key: K): V | undefined {
        return this.store.get(key);
    }
}

const kv = new KeyValueStore<string, { role: string }>();
kv.set("user_10", { role: "moderator" });
console.log("Foydalanuvchi ma'lumoti:", kv.get("user_10"));
```

## Tushuntirish va Mantiq:
Generic sinflar turli xil ma'lumotlar bilan xavfsiz ishlovchi qayta ishlatiluvchi komponentlar qurishda asosiy vositadir.

## Ishlash natijasi:
```text
Foydalanuvchi ma'lumoti: { role: 'moderator' }
```


# 818-Topshiriq: Sinf metodlarida ortiqcha yuklash (Overloading)

## Topshiriq sharti:
Sinf ichida bir nechta parametr turlari bilan chaqiriladigan metod yozing.

## Yechim (JS yoki TS kodi):
```typescript
class MessageFormatter {
    format(text: string): string;
    format(id: number, text: string): string;
    format(arg1: string | number, arg2?: string): string {
        if (typeof arg1 === "number" && arg2 !== undefined) {
            return `[ID: ${arg1}] ${arg2}`;
        }
        return `[LOG] ${arg1}`;
    }
}

const fmt = new MessageFormatter();
console.log(fmt.format("Tizim faol"));
console.log(fmt.format(105, "Buyurtma yaratildi"));
```

## Tushuntirish va Mantiq:
Sinf metodlari ham oddiy funksiyalar kabi bir nechta overload imzolariga ega bo'lishi mumkin.

## Ishlash natijasi:
```text
[LOG] Tizim faol
[ID: 105] Buyurtma yaratildi
```


# 819-Topshiriq: Fluent Interface (Zanjirli chaqiruv) va `this` qaytarish

## Topshiriq sharti:
So'rov parametrlarini zanjir usulida shakllantiruvchi RequestBuilder sinfini yozing.

## Yechim (JS yoki TS kodi):
```typescript
class RequestBuilder {
    private url: string = "";
    private method: string = "GET";

    setUrl(url: string): this {
        this.url = url;
        return this;
    }

    setMethod(method: string): this {
        this.method = method;
        return this;
    }

    send(): string {
        return `So'rov jo'natildi: ${this.method} -> ${this.url}`;
    }
}

const req = new RequestBuilder()
    .setUrl("https://api.example.com/data")
    .setMethod("POST")
    .send();

console.log(req);
```

## Tushuntirish va Mantiq:
Metoddan 'this' qaytarish zanjirli (fluent) chaqiruv uslubini yaratadi va voris sinflarda ham to'g'ri tipni saqlab qoladi.

## Ishlash natijasi:
```text
So'rov jo'natildi: POST -> https://api.example.com/data
```


# 820-Topshiriq: Sinfda this Type Guard (this is VorisSinf)

## Topshiriq sharti:
Sinf metodida joriy obyektning qaysi voris sinf ekanligini `this is` orqali tekshirish.

## Yechim (JS yoki TS kodi):
```typescript
class FileSystemNode {
    constructor(public name: string) {}

    isDirectory(): this is DirectoryNode {
        return this instanceof DirectoryNode;
    }
}

class DirectoryNode extends FileSystemNode {
    public children: FileSystemNode[] = [];
}

const node: FileSystemNode = new DirectoryNode("src");
if (node.isDirectory()) {
    console.log(`Jild nomi: ${node.name}, Ichki fayllar soni: ${node.children.length}`);
}
```

## Tushuntirish va Mantiq:
this is DirectoryNode predikati 'node.isDirectory()' tekshirilgandan so'ng, if ichida node tipini DirectoryNode ga avtomatik toraytiradi.

## Ishlash natijasi:
```text
Jild nomi: src, Ichki fayllar soni: 0
```


# 821-Topshiriq: Factory Method Pattern (Fabrika metodi)

## Topshiriq sharti:
Turli xil bildirishnoma jo'natuvchi obyektlarni yaratuvchi fabrika sinfini yozing.

## Yechim (JS yoki TS kodi):
```typescript
interface NotificationSender {
    send(message: string): void;
}

class EmailSender implements NotificationSender {
    send(m: string) { console.log(`Email yuborildi: ${m}`); }
}

class SmsSender implements NotificationSender {
    send(m: string) { console.log(`SMS yuborildi: ${m}`); }
}

class NotificationFactory {
    static create(type: "email" | "sms"): NotificationSender {
        if (type === "email") return new EmailSender();
        return new SmsSender();
    }
}

const notifier = NotificationFactory.create("sms");
notifier.send("Tasdiqlash kodi: 1234");
```

## Tushuntirish va Mantiq:
Fabrika metodi obyekt yaratish mantiqini mijoz kodidan ajratib, dasturni yangi tiplar bilan kengaytirishni osonlashtiradi.

## Ishlash natijasi:
```text
SMS yuborildi: Tasdiqlash kodi: 1234
```


# 822-Topshiriq: Strategy Pattern (Strategiya naqshi)

## Topshiriq sharti:
To'lovlarni amalga oshirishda to'lov usulini (Payme, Click) dinamik almashtirish.

## Yechim (JS yoki TS kodi):
```typescript
interface PaymentStrategy {
    pay(amount: number): void;
}

class ClickPayment implements PaymentStrategy {
    pay(amount: number) { console.log(`Click orqali to'landi: ${amount} so'm`); }
}

class PaymePayment implements PaymentStrategy {
    pay(amount: number) { console.log(`Payme orqali to'landi: ${amount} so'm`); }
}

class CheckoutService {
    constructor(private strategy: PaymentStrategy) {}

    setStrategy(s: PaymentStrategy) { this.strategy = s; }

    completeOrder(amount: number) { this.strategy.pay(amount); }
}

const checkout = new CheckoutService(new ClickPayment());
checkout.completeOrder(50000);
checkout.setStrategy(new PaymePayment());
checkout.completeOrder(75000);
```

## Tushuntirish va Mantiq:
Strategy naqshi algoritmni alohida sinfga chiqarib, uni runtime paytida erkin almashtirish imkonini beradi.

## Ishlash natijasi:
```text
Click orqali to'landi: 50000 so'm
Payme orqali to'landi: 75000 so'm
```


# 823-Topshiriq: Observer / Pub-Sub pattern sinflar bilan

## Topshiriq sharti:
Obunachilarga yangiliklar kelganda xabar beruvchi NewsChannel sinfini yozing.

## Yechim (JS yoki TS kodi):
```typescript
interface Subscriber {
    update(news: string): void;
}

class NewsAgency {
    private subscribers: Subscriber[] = [];

    subscribe(s: Subscriber): void {
        this.subscribers.push(s);
    }

    notify(news: string): void {
        this.subscribers.forEach(s => s.update(news));
    }
}

class NewsReader implements Subscriber {
    constructor(private name: string) {}
    update(news: string) {
        console.log(`${this.name} yangilikni o'qidi: "${news}"`);
    }
}

const agency = new NewsAgency();
const reader1 = new NewsReader("Olim");
const reader2 = new NewsReader("Kamola");

agency.subscribe(reader1);
agency.subscribe(reader2);
agency.notify("TypeScript 5.0 taqdim etildi!");
```

## Tushuntirish va Mantiq:
Observer naqshi obyektlar o'rtasida bir-ko'p bog'liqlik o'rnatib, bitta obyekt o'zgarganda qolganlariga xabar tarqatadi.

## Ishlash natijasi:
```text
Olim yangilikni o'qidi: "TypeScript 5.0 taqdim etildi!"
Kamola yangilikni o'qidi: "TypeScript 5.0 taqdim etildi!"
```


# 824-Topshiriq: Adapter Pattern (Adapter naqshi)

## Topshiriq sharti:
Eski API interfeysini yangi zamonaviy interfeysga moslashtiruvchi adapter sinfi.

## Yechim (JS yoki TS kodi):
```typescript
// Eski xizmat
class LegacyPaymentGateway {
    makePayment(cents: number): void {
        console.log(`Eski tizimda to'landi: ${cents / 100} dollar`);
    }
}

// Yangi interfeys
interface ModernPayment {
    payDollars(dollars: number): void;
}

// Adapter
class PaymentAdapter implements ModernPayment {
    constructor(private legacy: LegacyPaymentGateway) {}

    payDollars(dollars: number): void {
        const cents = dollars * 100;
        this.legacy.makePayment(cents);
    }
}

const legacy = new LegacyPaymentGateway();
const modern: ModernPayment = new PaymentAdapter(legacy);
modern.payDollars(25);
```

## Tushuntirish va Mantiq:
Adapter naqshi mos kelmaydigan ikki interfeysni bir-biri bilan birgalikda ishlashiga imkon yaratadi.

## Ishlash natijasi:
```text
Eski tizimda to'landi: 25 dollar
```


# 825-Topshiriq: Template Method Pattern abstrakt sinf bilan

## Topshiriq sharti:
Algoritm skeletini belgilab, aniq qadamlarni voris sinflarga qoldiruvchi DataMiner abstrakt sinfi.

## Yechim (JS yoki TS kodi):
```typescript
abstract class DataMiner {
    // Shabloni metod (Template Method)
    public mine(path: string): void {
        this.openFile(path);
        this.extractData();
        this.closeFile();
    }

    protected openFile(path: string): void {
        console.log(`Fayl ochildi: ${path}`);
    }

    protected abstract extractData(): void;

    protected closeFile(): void {
        console.log("Fayl yopildi.");
    }
}

class PdfDataMiner extends DataMiner {
    protected extractData(): void {
        console.log("PDF dan matn va rasmlar ajratib olindi.");
    }
}

const miner = new PdfDataMiner();
miner.mine("document.pdf");
```

## Tushuntirish va Mantiq:
Template Method umumiy qadamlar ketma-ketligini o'zgarmas qilib belgilaydi, faqat o'zgaruvchan qadamlarni vorislar ixtiyoriga topshiradi.

## Ishlash natijasi:
```text
Fayl ochildi: document.pdf
PDF dan matn va rasmlar ajratib olindi.
Fayl yopildi.
```


# 826-Topshiriq: Command Pattern (Buyruq naqshi)

## Topshiriq sharti:
Amallarni obyekt ko'rinishida saqlash va bajarish (Undo/Execute).

## Yechim (JS yoki TS kodi):
```typescript
interface Command {
    execute(): void;
    undo(): void;
}

class Light {
    turnOn() { console.log("Chiroq yondi"); }
    turnOff() { console.log("Chiroq o'chdi"); }
}

class LightOnCommand implements Command {
    constructor(private light: Light) {}
    execute() { this.light.turnOn(); }
    undo() { this.light.turnOff(); }
}

const bulb = new Light();
const cmd = new LightOnCommand(bulb);

cmd.execute();
cmd.undo();
```

## Tushuntirish va Mantiq:
Command naqshi so'rovlarni obyekt sifatida o'rab oladi, bu esa operatsiyalarni navbatga qo'yish, qaytarish (undo) va log qilish imkonini beradi.

## Ishlash natijasi:
```text
Chiroq yondi
Chiroq o'chdi
```


# 827-Topshiriq: Mixins (Miksinkalar) - Konstruktor turi va kengaytirish

## Topshiriq sharti:
Sinfga qo'shimcha timestamp xossasini beruvchi Mixin funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
type Constructor<T = {}> = new (...args: any[]) => T;

function Timestamped<TBase extends Constructor>(Base: TBase) {
    return class extends Base {
        timestamp = new Date();
    };
}

class SimpleUser {
    constructor(public name: string) {}
}

const TimestampedUser = Timestamped(SimpleUser);
const user = new TimestampedUser("Nodira");

console.log(`Foydalanuvchi: ${user.name}, Vaqt mavjud: ${user.timestamp instanceof Date}`);
```

## Tushuntirish va Mantiq:
Mixins yordamida bir nechta mustaqil funksionalliklarni sinflarga kompozitsiya orqali aralashtirish mumkin.

## Ishlash natijasi:
```text
Foydalanuvchi: Nodira, Vaqt mavjud: true
```


# 828-Topshiriq: Faoliyat logini qo'shuvchi Activable Mixin

## Topshiriq sharti:
Sinfga isActivated holatini beruvchi miksinka yarating.

## Yechim (JS yoki TS kodi):
```typescript
type AnyConstructor = new (...args: any[]) => any;

function Activatable<TBase extends AnyConstructor>(Base: TBase) {
    return class extends Base {
        isActive: boolean = false;
        activate() { this.isActive = true; }
        deactivate() { this.isActive = false; }
    };
}

class Device {
    constructor(public model: string) {}
}

const SmartDevice = Activatable(Device);
const dev = new SmartDevice("Sensor_X");
dev.activate();

console.log(`${dev.model} faolmi: ${dev.isActive}`);
```

## Tushuntirish va Mantiq:
Mixin naqshi ko'p karra merosxo'rlik (multiple inheritance) bo'lmagan tillarda funksiyalarni qayta ishlatishning qulay usulidir.

## Ishlash natijasi:
```text
Sensor_X faolmi: true
```


# 829-Topshiriq: Sinflarda implements va extends ni birgalikda qo'llash

## Topshiriq sharti:
Ota sinfdan meros olib, qo'shimcha ravishda interfeysni amalga oshirish.

## Yechim (JS yoki TS kodi):
```typescript
class BaseEntity {
    constructor(public id: number) {}
}

interface Auditable {
    getAuditLog(): string;
}

class OrderEntity extends BaseEntity implements Auditable {
    constructor(id: number, public total: number) {
        super(id);
    }

    getAuditLog(): string {
        return `Order #${this.id} jami: ${this.total}`;
    }
}

const ord = new OrderEntity(701, 120000);
console.log(ord.getAuditLog());
```

## Tushuntirish va Mantiq:
Sinf bir vaqtning o'zida 'extends Base' va 'implements Interface' qoidalariga rioya qilishi mumkin.

## Ishlash natijasi:
```text
Order #701 jami: 120000
```


# 830-Topshiriq: Sinf tipi va Konstruktor funksiya tipi farqi

## Topshiriq sharti:
`typeof MyClass` bilan `MyClass` o'rtasidagi farqni kodda ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
class Member {
    static role = "standart";
    constructor(public name: string) {}
}

// Member tipi - bu instansiya tipi (name maydoni bor)
const m: Member = new Member("Jasurbek");

// typeof Member - bu konstruktor funksiyaning o'zi (statik role maydoni bor)
const MemberCtor: typeof Member = Member;
console.log("Statik rol:", MemberCtor.role);
console.log("Instansiya ismi:", m.name);
```

## Tushuntirish va Mantiq:
TypeScript da sinf e'lon qilinganda ikkita tip yaratiladi: instansiya tipi (Member) va statik konstruktor tipi (typeof Member).

## Ishlash natijasi:
```text
Statik rol: standart
Instansiya ismi: Jasurbek
```


# 831-Topshiriq: Polimorfizm va Dinamik Dispatch (Dynamic Dispatch)

## Topshiriq sharti:
Ota tipdagi massiv orqali turli voris sinflar metodlarini bir xil chaqirish.

## Yechim (JS yoki TS kodi):
```typescript
abstract class NotificationChannel {
    abstract deliver(msg: string): void;
}

class TelegramChannel extends NotificationChannel {
    deliver(msg: string) { console.log(`Telegram botdan: ${msg}`); }
}

class PushChannel extends NotificationChannel {
    deliver(msg: string) { console.log(`Push bildirishnoma: ${msg}`); }
}

const channels: NotificationChannel[] = [new TelegramChannel(), new PushChannel()];
channels.forEach(ch => ch.deliver("Yangi xabaringiz bor!"));
```

## Tushuntirish va Mantiq:
Polimorfizm orqali umumiy NotificationChannel interfeysi ostida turli sinflar o'ziga xos mantiqni bajaradi.

## Ishlash natijasi:
```text
Telegram botdan: Yangi xabaringiz bor!
Push bildirishnoma: Yangi xabaringiz bor!
```


# 832-Topshiriq: Composite Pattern (Ierarxik daraxt tuzish)

## Topshiriq sharti:
Bitta element va elementlar guruhini bir xil interfeys bilan boshqarish.

## Yechim (JS yoki TS kodi):
```typescript
interface Graphic {
    draw(): void;
}

class Dot implements Graphic {
    constructor(private x: number, private y: number) {}
    draw() { console.log(`Nuqta chizildi: (${this.x}, ${this.y})`); }
}

class CompoundGraphic implements Graphic {
    private children: Graphic[] = [];

    add(child: Graphic) { this.children.push(child); }

    draw() {
        console.log("Guruh chizilmoqda:");
        this.children.forEach(c => c.draw());
    }
}

const group = new CompoundGraphic();
group.add(new Dot(1, 2));
group.add(new Dot(5, 8));
group.draw();
```

## Tushuntirish va Mantiq:
Composite naqshi daraxtsimon tuzilmalarda bitta obyekt va butun novdani bir xil metod orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Guruh chizilmoqda:
Nuqta chizildi: (1, 2)
Nuqta chizildi: (5, 8)
```


# 833-Topshiriq: Dependency Inversion Principle (DIP)

## Topshiriq sharti:
Yuqori darajadagi modul quyi modulga emas, abstraksiyaga (interfeysga) bog'lanishi.

## Yechim (JS yoki TS kodi):
```typescript
interface MessageService {
    sendMessage(to: string, message: string): void;
}

class EmailService implements MessageService {
    sendMessage(to: string, message: string) {
        console.log(`Email jo'natildi -> ${to}: ${message}`);
    }
}

class OrderNotificationManager {
    constructor(private service: MessageService) {} // Konkret sinfga emas, interfeysga bog'liq

    notifyUser(userId: string) {
        this.service.sendMessage(userId, "Buyurtmangiz yo'lga chiqdi!");
    }
}

const manager = new OrderNotificationManager(new EmailService());
manager.notifyUser("user@uz.dev");
```

## Tushuntirish va Mantiq:
DIP tamoyiliga ko'ra sinflar to'g'ridan-to'g'ri bir-biriga bog'lanmasdan, umumiy interfeyslar orqali bog'lanadi (Loose Coupling).

## Ishlash natijasi:
```text
Email jo'natildi -> user@uz.dev: Buyurtmangiz yo'lga chiqdi!
```


# 834-Topshiriq: Open-Closed Principle (OCP)

## Topshiriq sharti:
Mavjud kodni o'zgartirmasdan, yangi voris sinflar qo'shish orqali yangi funksionallik kiritish.

## Yechim (JS yoki TS kodi):
```typescript
abstract class DiscountCalculator {
    abstract calculate(amount: number): number;
}

class RegularCustomerDiscount extends DiscountCalculator {
    calculate(amount: number): number { return amount * 0.95; } // 5%
}

class VipCustomerDiscount extends DiscountCalculator {
    calculate(amount: number): number { return amount * 0.80; } // 20%
}

function processPayment(calc: DiscountCalculator, total: number): void {
    console.log(`Chegirmali narx: ${calc.calculate(total)}`);
}

processPayment(new VipCustomerDiscount(), 1000);
```

## Tushuntirish va Mantiq:
Yangi chegirma turi qo'shilganda processPayment funksiyasini tahrirlash shart emas, faqat yangi sinf e'lon qilinadi.

## Ishlash natijasi:
```text
Chegirmali narx: 800
```


# 835-Topshiriq: Liskov Substitution Principle (LSP)

## Topshiriq sharti:
Voris sinf ota sinf kutayotgan joyda dastur mantig'ini buzmasdan to'liq ishlay olishi.

## Yechim (JS yoki TS kodi):
```typescript
class Bird {
    fly(): string { return "Qush uchmoqda"; }
}

class Eagle extends Bird {
    fly(): string { return "Burgut baland parvoz qilmoqda"; }
}

function makeBirdFly(bird: Bird) {
    console.log(bird.fly());
}

makeBirdFly(new Bird());
makeBirdFly(new Eagle());
```

## Tushuntirish va Mantiq:
LSP qoidasiga binoan voris sinf ota sinfning shartnomalariga to'liq rioya qilishi lozim.

## Ishlash natijasi:
```text
Qush uchmoqda
Burgut baland parvoz qilmoqda
```


# 836-Topshiriq: Interface Segregation Principle (ISP)

## Topshiriq sharti:
Katta umumiy interfeys o'rniga kichik, ixtisoslashgan interfeyslar tuzish.

## Yechim (JS yoki TS kodi):
```typescript
interface PrinterInterface {
    printDoc(): void;
}

interface ScannerInterface {
    scanDoc(): void;
}

class SimplePrinter implements PrinterInterface {
    printDoc() { console.log("Hujjat chop etildi."); }
}

class AllInOneMachine implements PrinterInterface, ScannerInterface {
    printDoc() { console.log("MFU chop etdi."); }
    scanDoc() { console.log("MFU skaner qildi."); }
}

const printer = new SimplePrinter();
printer.printDoc();
```

## Tushuntirish va Mantiq:
ISP mijozlarni o'zlari ishlatmaydigan metodlarga bog'lanishga majburlamaslikni talab qiladi.

## Ishlash natijasi:
```text
Hujjat chop etildi.
```


# 837-Topshiriq: Single Responsibility Principle (SRP)

## Topshiriq sharti:
Sinf faqat bitta aniq vazifaga javobgar bo'lishi lozim.

## Yechim (JS yoki TS kodi):
```typescript
class UserData {
    constructor(public id: number, public name: string) {}
}

class UserRepository {
    save(user: UserData) {
        console.log(`Foydalanuvchi #${user.id} bazaga yozildi.`);
    }
}

class UserEmailer {
    sendWelcome(user: UserData) {
        console.log(`${user.name} ga xush kelibsiz xati yuborildi.`);
    }
}

const u = new UserData(1, "Mansur");
new UserRepository().save(u);
new UserEmailer().sendWelcome(u);
```

## Tushuntirish va Mantiq:
SRP ga binoan ma'lumot saqlash va xat yuborish mantiqlari alohida sinflarga ajratiladi.

## Ishlash natijasi:
```text
Foydalanuvchi #1 bazaga yozildi.
Mansur ga xush kelibsiz xati yuborildi.
```


# 838-Topshiriq: Repository Pattern TypeScript OOP da

## Topshiriq sharti:
Xotirada (In-memory) ma'lumotlarni saqlash va qidirish ombori.

## Yechim (JS yoki TS kodi):
```typescript
interface IRepository<T> {
    findById(id: number): T | undefined;
    save(entity: T): void;
}

interface Customer {
    id: number;
    fullName: string;
}

class CustomerRepository implements IRepository<Customer> {
    private db = new Map<number, Customer>();

    findById(id: number): Customer | undefined {
        return this.db.get(id);
    }

    save(customer: Customer): void {
        this.db.set(customer.id, customer);
        console.log(`Mijoz saqlandi: ${customer.fullName}`);
    }
}

const repo = new CustomerRepository();
repo.save({ id: 5, fullName: "Sanjar Qodirov" });
console.log("Topildi:", repo.findById(5)?.fullName);
```

## Tushuntirish va Mantiq:
Repository naqshi ma'lumotlar qatlamini domen mantiqidan to'liq ajratadi.

## Ishlash natijasi:
```text
Mijoz saqlandi: Sanjar Qodirov
Topildi: Sanjar Qodirov
```


# 839-Topshiriq: Value Object (O'zgarmas Qiymat Obyekti) patterni

## Topshiriq sharti:
Identifikatori bo'lmagan, qiymatlari tengligi bilan belgilanuvchi o'zgarmas Money sinfi.

## Yechim (JS yoki TS kodi):
```typescript
class Money {
    constructor(readonly amount: number, readonly currency: string) {
        if (amount < 0) throw new Error("Miqdor manfiy bo'la olmaydi!");
        Object.freeze(this);
    }

    equals(other: Money): boolean {
        return this.amount === other.amount && this.currency === other.currency;
    }

    add(other: Money): Money {
        if (this.currency !== other.currency) throw new Error("Valyutalar bir xil bo'lishi shart!");
        return new Money(this.amount + other.amount, this.currency);
    }
}

const m1 = new Money(100, "UZS");
const m2 = new Money(50, "UZS");
const sum = m1.add(m2);

console.log(`Jami: ${sum.amount} ${sum.currency}`);
```

## Tushuntirish va Mantiq:
Value Object o'zining ichki qiymatlari bilan aniqlanadi va yangi operatsiya har doim yangi obyekt qaytaradi.

## Ishlash natijasi:
```text
Jami: 150 UZS
```


# 840-Topshiriq: Aggregate Root patterni (DDD asoslari)

## Topshiriq sharti:
Buyurtma va uning ichki qismlarini yaxlit boshqaruvchi Order aggregati.

## Yechim (JS yoki TS kodi):
```typescript
class OrderLine {
    constructor(public product: string, public price: number) {}
}

class OrderAggregate {
    private items: OrderLine[] = [];

    addLine(product: string, price: number): void {
        this.items.push(new OrderLine(product, price));
    }

    calculateTotal(): number {
        return this.items.reduce((sum, item) => sum + item.price, 0);
    }

    getItemCount(): number {
        return this.items.length;
    }
}

const order = new OrderAggregate();
order.addLine("Kitob", 45000);
order.addLine("Ruchka", 5000);
console.log(`Mahsulotlar: ${order.getItemCount()}, Jami: ${order.calculateTotal()} so'm`);
```

## Tushuntirish va Mantiq:
Aggregate Root barcha ichki bog'liq obyektlarni yagona chegara ichida nazorat qiladi.

## Ishlash natijasi:
```text
Mahsulotlar: 2, Jami: 50000 so'm
```


# 841-Topshiriq: Domain Event generatsiya qiluvchi Entity sinfi

## Topshiriq sharti:
Obyekt holati o'zgarganda ichki hodisalarni to'plovchi asosiy Entity sinfi.

## Yechim (JS yoki TS kodi):
```typescript
class BaseDomainEntity {
    private domainEvents: string[] = [];

    protected addEvent(event: string): void {
        this.domainEvents.push(event);
    }

    public pullEvents(): string[] {
        const events = [...this.domainEvents];
        this.domainEvents = [];
        return events;
    }
}

class UserAccountEntity extends BaseDomainEntity {
    changePassword() {
        this.addEvent("PASSWORD_CHANGED");
    }
}

const acc = new UserAccountEntity();
acc.changePassword();
console.log("Hodisalar:", acc.pullEvents());
```

## Tushuntirish va Mantiq:
Domain Events sinf ichidagi muhim biznes hodisalarini qayd qilib, tashqi tizimlarga uzatishda ishlatiladi.

## Ishlash natijasi:
```text
Hodisalar: [ 'PASSWORD_CHANGED' ]
```


# 842-Topshiriq: Sinfda Symbol.iterator implementatsiyasi (Iterable sinf)

## Topshiriq sharti:
for...of siklida to'g'ridan-to'g'ri aylanish mumkin bo'lgan Team sinfini yozing.

## Yechim (JS yoki TS kodi):
```typescript
class Team {
    constructor(private members: string[]) {}

    *[Symbol.iterator](): Iterator<string> {
        for (const member of this.members) {
            yield member;
        }
    }
}

const devTeam = new Team(["Ali", "Vali", "G'ani"]);
for (const dev of devTeam) {
    console.log(`Jamoa a'zosi: ${dev}`);
}
```

## Tushuntirish va Mantiq:
*[Symbol.iterator]() metodi sinfga Iterable interfeysini beradi va uni for...of orqali aylantirish imkonini beradi.

## Ishlash natijasi:
```text
Jamoa a'zosi: Ali
Jamoa a'zosi: Vali
Jamoa a'zosi: G'ani
```


# 843-Topshiriq: Sinfda Symbol.asyncIterator implementatsiyasi

## Topshiriq sharti:
for await...of siklida asinxron ma'lumotlarni o'quvchi sinf.

## Yechim (JS yoki TS kodi):
```typescript
class AsyncDataStream {
    constructor(private count: number) {}

    async *[Symbol.asyncIterator](): AsyncIterator<number> {
        for (let i = 1; i <= this.count; i++) {
            yield i;
        }
    }
}

async function run() {
    const stream = new AsyncDataStream(3);
    for await (const val of stream) {
        console.log(`Olingan asinxron qiymat: ${val}`);
    }
}

run();
```

## Tushuntirish va Mantiq:
Symbol.asyncIterator asinxron oqimlarni ketma-ket for await orqali o'qish uchun sinfga integratsiya qilinadi.

## Ishlash natijasi:
```text
Olingan asinxron qiymat: 1
Olingan asinxron qiymat: 2
Olingan asinxron qiymat: 3
```


# 844-Topshiriq: Sinf ichida xususiy metodlar va yordamchi funksiyalar

## Topshiriq sharti:
Tashqaridan ko'rinmaydigan murakkab algoritmni private metodga yashirish.

## Yechim (JS yoki TS kodi):
```typescript
class EncryptionService {
    public encrypt(text: string): string {
        const salt = this.generateSalt();
        return `${salt}_${text}_enc`;
    }

    private generateSalt(): string {
        return "salt_xyz";
    }
}

const enc = new EncryptionService();
console.log("Shifrlangan:", enc.encrypt("Salom"));
```

## Tushuntirish va Mantiq:
Xususiy metodlar faqat sinf ichidagi boshqa ommaviy metodlarga yordam berish uchun ajratiladi.

## Ishlash natijasi:
```text
Shifrlangan: salt_xyz_Salom_enc
```


# 845-Topshiriq: Sinf parametrlarida default qiymatlar bilan destrukturizatsiya

## Topshiriq sharti:
Konstruktorga options obyekti uzatilganda qulay boshlang'ich qiymatlar berish.

## Yechim (JS yoki TS kodi):
```typescript
interface WindowOptions {
    width?: number;
    height?: number;
    title?: string;
}

class AppWindow {
    public width: number;
    public height: number;
    public title: string;

    constructor({ width = 800, height = 600, title = "Ilova oynasi" }: WindowOptions = {}) {
        this.width = width;
        this.height = height;
        this.title = title;
    }
}

const win = new AppWindow({ title: "Mening Oynam" });
console.log(`Oyna: "${win.title}", O'lcham: ${win.width}x${win.height}`);
```

## Tushuntirish va Mantiq:
Konstruktor parametrida destrukturizatsiya va sukutli qiymatlar birlashmasi obyektni juda moslashuvchan qiladi.

## Ishlash natijasi:
```text
Oyna: "Mening Oynam", O'lcham: 800x600
```


# 846-Topshiriq: Sinf xossalarida definite assignment assertion (!)

## Topshiriq sharti:
Konstruktordan tashqarida inisializatsiya qilinadigan maydonni belgilash.

## Yechim (JS yoki TS kodi):
```typescript
class DeferredComponent {
    name!: string; // ! belgisi kompilyatorga maydon albatta to'ldirilishini bildiradi

    init(name: string) {
        this.name = name;
    }

    display() {
        console.log(`Komponent: ${this.name}`);
    }
}

const comp = new DeferredComponent();
comp.init("Sidebar");
comp.display();
```

## Tushuntirish va Mantiq:
Definite assignment assertion (!) strictPropertyInitialization xatosini chetlab o'tish uchun ishlatiladi.

## Ishlash natijasi:
```text
Komponent: Sidebar
```


# 847-Topshiriq: Object.freeze bilan sinf instansiyasini to'liq muzlatish

## Topshiriq sharti:
Konstruktor oxirida obyektni muzlatib, xossalar qo'shish yoki o'zgartirishni man etish.

## Yechim (JS yoki TS kodi):
```typescript
class ImmutablePoint {
    public x: number;
    public y: number;

    constructor(x: number, y: number) {
        this.x = x;
        this.y = y;
        Object.freeze(this);
    }
}

const pt = new ImmutablePoint(10, 20);
console.log(`Nuqta: (${pt.x}, ${pt.y})`);
```

## Tushuntirish va Mantiq:
Object.freeze(this) nafaqat kompilyatsiya darajasida, balki runtime darajasida ham obyektning o'zgarmasligini ta'minlaydi.

## Ishlash natijasi:
```text
Nuqta: (10, 20)
```


# 848-Topshiriq: Abstrakt sinfda metod implementatsiyasi va abstrakt metod aralashmasi

## Topshiriq sharti:
Umumiy logikani o'zida saqlab, aniq formatlashni vorisga yuklash.

## Yechim (JS yoki TS kodi):
```typescript
abstract class BaseReport {
    generate(): string {
        const header = "=== HISOBOT BOSHI ===";
        const body = this.formatBody();
        const footer = "=== HISOBOT TUGADI ===";
        return `${header}\n${body}\n${footer}`;
    }

    protected abstract formatBody(): string;
}

class SalesReport extends BaseReport {
    protected formatBody(): string {
        return "Jami sotildi: 150 ta mahsulot";
    }
}

console.log(new SalesReport().generate());
```

## Tushuntirish va Mantiq:
Abstrakt sinflar to'liq abstrakt bo'lishi shart emas; ular tayyor metodlar bilan abstrakt metodlarni birlashtira oladi.

## Ishlash natijasi:
```text
=== HISOBOT BOSHI ===
Jami sotildi: 150 ta mahsulot
=== HISOBOT TUGADI ===
```


# 849-Topshiriq: Sinf vorisligida konstruktor parametrlari kengayishi

## Topshiriq sharti:
Voris sinf ota parametrlari ustiga o'zining yangi parametrlarini qabul qilishi.

## Yechim (JS yoki TS kodi):
```typescript
class VehicleBase {
    constructor(public readonly vin: string, public make: string) {}
}

class ElectricVehicle extends VehicleBase {
    constructor(vin: string, make: string, public batteryCapacityKWh: number) {
        super(vin, make);
    }
}

const ev = new ElectricVehicle("VIN_123456", "BYD", 72);
console.log(`Mashina: ${ev.make}, Batareya: ${ev.batteryCapacityKWh} kVt/soat`);
```

## Tushuntirish va Mantiq:
Voris sinf konstruktori ota sinfning barcha parametrlarini super(...) ga uzatadi va qo'shimcha yangi maydonlarni o'zida saqlaydi.

## Ishlash natijasi:
```text
Mashina: BYD, Batareya: 72 kVt/soat
```


# 850-Topshiriq: E-Commerce Buyurtmalar tizimi: To'liq OOP Arxitekturasi

## Topshiriq sharti:
Order, OrderItem, DiscountStrategy va PaymentGateway ni birlashtiruvchi to'liq domen modeli.

## Yechim (JS yoki TS kodi):
```typescript
interface DiscountStrategy {
    applyDiscount(amount: number): number;
}

class PercentageDiscount implements DiscountStrategy {
    constructor(private percent: number) {}
    applyDiscount(amount: number): number {
        return amount - (amount * this.percent) / 100;
    }
}

class OrderItem {
    constructor(public name: string, public price: number, public quantity: number) {}
    getTotal(): number {
        return this.price * this.quantity;
    }
}

class Order {
    private items: OrderItem[] = [];

    constructor(public id: number, private discountStrategy?: DiscountStrategy) {}

    addItem(item: OrderItem): void {
        this.items.push(item);
    }

    calculateTotal(): number {
        const subtotal = this.items.reduce((sum, item) => sum + item.getTotal(), 0);
        return this.discountStrategy ? this.discountStrategy.applyDiscount(subtotal) : subtotal;
    }
}

const order = new Order(1001, new PercentageDiscount(10)); // 10% chegirma
order.addItem(new OrderItem("Klaviatura", 300000, 1));
order.addItem(new OrderItem("Sichqoncha", 100000, 2));

console.log(`Buyurtma #${order.id} yakuniy summasi: ${order.calculateTotal()} so'm`);
```

## Tushuntirish va Mantiq:
Ushbu modelda Inkapsulyatsiya (private items), Abstraksiya (DiscountStrategy), Polimorfizm va Kompozitsiya to'liq birlashtirilgan.

## Ishlash natijasi:
```text
Buyurtma #1001 yakuniy summasi: 450000 so'm
```

