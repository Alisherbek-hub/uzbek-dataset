# 751-Topshiriq: Partial<T> - Profilni qisman yangilash

## Topshiriq sharti:
Foydalanuvchi ma'lumotlarini qisman tahrirlash (update) funksiyasida Partial<User> utility tipini qo'llang.

## Yechim (JS yoki TS kodi):
```typescript
interface User {
    id: number;
    name: string;
    email: string;
    age: number;
}

function updateUser(user: User, fieldsToUpdate: Partial<User>): User {
    return { ...user, ...fieldsToUpdate };
}

const originalUser: User = { id: 1, name: "Farxod", email: "farxod@uz.dev", age: 24 };
const updated = updateUser(originalUser, { age: 25 });

console.log("Yangilangan foydalanuvchi:", updated);
```

## Tushuntirish va Mantiq:
Partial<T> berilgan T interfeysining barcha maydonlarini ixtiyoriy (optional: ?) qiladi. Bu PATCH/Update so'rovlarida qisman ma'lumot uzatish uchun juda qulay.

## Ishlash natijasi:
```text
Yangilangan foydalanuvchi: { id: 1, name: 'Farxod', email: 'farxod@uz.dev', age: 25 }
```


# 752-Topshiriq: Required<T> - Ixtiyoriy maydonlarni majburiy qilish

## Topshiriq sharti:
Ixtiyoriy sozlamalar berilgan konfiguratsiya obyektini Required<T> orqali to'liq to'ldirilgan holga keltiring.

## Yechim (JS yoki TS kodi):
```typescript
interface AppConfig {
    host: string;
    port?: number;
    ssl?: boolean;
}

const fullConfig: Required<AppConfig> = {
    host: "localhost",
    port: 8080,
    ssl: true
};

console.log(`Server: ${fullConfig.host}:${fullConfig.port}, SSL: ${fullConfig.ssl}`);
```

## Tushuntirish va Mantiq:
Required<T> barcha '?' belgilarini olib tashlaydi va har bir xossa bo'lishini shart qilib qo'yadi.

## Ishlash natijasi:
```text
Server: localhost:8080, SSL: true
```


# 753-Topshiriq: Readonly<T> - O'zgarmas (Immutable) obyekt

## Topshiriq sharti:
Obyekt maydonlarini o'zgartirishdan himoyalovchi Readonly<T> utility tipini qo'llang.

## Yechim (JS yoki TS kodi):
```typescript
interface Point {
    x: number;
    y: number;
}

const origin: Readonly<Point> = { x: 0, y: 0 };

// origin.x = 10; // Xatolik: x faqat o'qish uchun!
console.log(`Nuqta koordinatalari: (${origin.x}, ${origin.y})`);
```

## Tushuntirish va Mantiq:
Readonly<T> obyektdagi barcha xossalarga readonly modifikatorini qo'shadi, bu qiymatni qayta yozishni taqiqlaydi.

## Ishlash natijasi:
```text
Nuqta koordinatalari: (0, 0)
```


# 754-Topshiriq: Record<K, T> - Lug'at va Xaritalar tuzish

## Topshiriq sharti:
Foydalanuvchi rollari bo'yicha sahifalarga ruxsat beruvchi lug'atni Record orqali yarating.

## Yechim (JS yoki TS kodi):
```typescript
type Role = "admin" | "manager" | "guest";

interface AccessPolicy {
    canEdit: boolean;
    canDelete: boolean;
}

const rolePermissions: Record<Role, AccessPolicy> = {
    admin: { canEdit: true, canDelete: true },
    manager: { canEdit: true, canDelete: false },
    guest: { canEdit: false, canDelete: false }
};

console.log("Admin ruxsati:", rolePermissions.admin);
console.log("Mehmon ruxsati:", rolePermissions.guest);
```

## Tushuntirish va Mantiq:
Record<K, T> kalitlari K to'plamiga va qiymatlari T tipiga ega bo'lgan lug'at (key-value) obyektini hosil qiladi.

## Ishlash natijasi:
```text
Admin ruxsati: { canEdit: true, canDelete: true }
Mehmon ruxsati: { canEdit: false, canDelete: false }
```


# 755-Topshiriq: Pick<T, K> - Kerakli xossalarni tanlab olish

## Topshiriq sharti:
Katta Product interfeysidan faqat id va title maydonlarini Pick orqali ajratib oling.

## Yechim (JS yoki TS kodi):
```typescript
interface Product {
    id: number;
    title: string;
    price: number;
    description: string;
    inStock: boolean;
}

type ProductSummary = Pick<Product, "id" | "title">;

const summary: ProductSummary = {
    id: 101,
    title: "Smartfon"
};

console.log("Mahsulot qisqacha ma'lumoti:", summary);
```

## Tushuntirish va Mantiq:
Pick<T, K> mavjud interfeysdan faqat ko'rsatilgan K kalitlarini ajratib olib yangi kichikroq tip yasaydi.

## Ishlash natijasi:
```text
Mahsulot qisqacha ma'lumoti: { id: 101, title: 'Smartfon' }
```


# 756-Topshiriq: Omit<T, K> - Keraksiz maydonlarni olib tashlash

## Topshiriq sharti:
Foydalanuvchi obyektidan maxfiy parol va token maydonlarini Omit orqali chiqarib tashlang.

## Yechim (JS yoki TS kodi):
```typescript
interface FullUser {
    id: number;
    username: string;
    passwordHash: string;
    sessionToken: string;
}

type PublicUser = Omit<FullUser, "passwordHash" | "sessionToken">;

const publicProfile: PublicUser = {
    id: 1,
    username: "islombek"
};

console.log("Ochiq profil:", publicProfile);
```

## Tushuntirish va Mantiq:
Omit<T, K> T interfeysidan K kalitlarini butunlay olib tashlaydi va xavfsiz ochiq modellarni shakllantirishda ishlatiladi.

## Ishlash natijasi:
```text
Ochiq profil: { id: 1, username: 'islombek' }
```


# 757-Topshiriq: Exclude<T, U> - Birlashmadan tiplarni chiqarib tashlash

## Topshiriq sharti:
Barcha ruxsatlar unionidan xavfli huquqlarni Exclude orqali o'chirib tashlang.

## Yechim (JS yoki TS kodi):
```typescript
type Action = "view" | "create" | "update" | "delete" | "drop_database";

type SafeAction = Exclude<Action, "delete" | "drop_database">;

const currentAction: SafeAction = "create";
console.log("Xavfsiz amal:", currentAction);
```

## Tushuntirish va Mantiq:
Exclude<T, U> shartli tip bo'lib, T union a'zolaridan U ga mos keluvchi barcha variantlarni chiqarib tashlaydi.

## Ishlash natijasi:
```text
Xavfsiz amal: create
```


# 758-Topshiriq: Extract<T, U> - Mos keluvchi a'zolarni ajratib olish

## Topshiriq sharti:
Aralash union tiplaridan faqat funksiya yoki string bo'lganlarini Extract orqali oling.

## Yechim (JS yoki TS kodi):
```typescript
type MixedEvents = "click" | "hover" | (() => void) | number;

type EventNames = Extract<MixedEvents, string>;

const eventName: EventNames = "click";
console.log("Hodisa nomi:", eventName);
```

## Tushuntirish va Mantiq:
Extract<T, U> faqat U tipiga mos tushadigan a'zolarni qoldiradi, qolganlarini chiqarib tashlaydi.

## Ishlash natijasi:
```text
Hodisa nomi: click
```


# 759-Topshiriq: NonNullable<T> - null va undefined ni yo'qotish

## Topshiriq sharti:
Bo'sh bo'lishi mumkin bo'lgan tipdan null va undefined ni tozalang.

## Yechim (JS yoki TS kodi):
```typescript
type MaybeName = string | null | undefined;
type DefiniteName = NonNullable<MaybeName>;

const clientName: DefiniteName = "Sherzod";
console.log("Mijoz ismi:", clientName);
```

## Tushuntirish va Mantiq:
NonNullable<T> barcha null va undefined qiymatlarini chiqarib tashlaydi va qiymat kafolatlangan bo'lishini ta'minlaydi.

## Ishlash natijasi:
```text
Mijoz ismi: Sherzod
```


# 760-Topshiriq: ReturnType<T> - Funksiya qaytish qiymati tipi

## Topshiriq sharti:
Funksiya chaqirilganda hosil bo'ladigan obyekt tipini ReturnType yordamida oling.

## Yechim (JS yoki TS kodi):
```typescript
function buildReport() {
    return {
        timestamp: Date.now(),
        totalSales: 154000,
        status: "APPROVED" as const
    };
}

type ReportData = ReturnType<typeof buildReport>;

const report: ReportData = {
    timestamp: 1710000000000,
    totalSales: 200000,
    status: "APPROVED"
};

console.log(`Hisobot savdosi: ${report.totalSales}`);
```

## Tushuntirish va Mantiq:
ReturnType<typeof fn> funksiyaning qaytarish qiymati tipini avtomatik chiqarib beradi, natijada har safar alohida interfeys yozish shart bo'lmaydi.

## Ishlash natijasi:
```text
Hisobot savdosi: 200000
```


# 761-Topshiriq: Parameters<T> - Argumentlar tuple tipi

## Topshiriq sharti:
Funksiya qabul qiladigan parametrlarning aniq tiplarini Parameters yordamida oling.

## Yechim (JS yoki TS kodi):
```typescript
function registerStudent(name: string, age: number, isEnrolled: boolean) {
    return { name, age, isEnrolled };
}

type RegisterArgs = Parameters<typeof registerStudent>; // [string, number, boolean]

const studentArgs: RegisterArgs = ["Diyorbek", 21, true];
const student = registerStudent(...studentArgs);

console.log("Ro'yxatga olindi:", student);
```

## Tushuntirish va Mantiq:
Parameters<T> funksiya argumentlarini tuple ko'rinishida beradi, bu wrapper va dekoratorlar yozishda juda foydalidir.

## Ishlash natijasi:
```text
Ro'yxatga olindi: { name: 'Diyorbek', age: 21, isEnrolled: true }
```


# 762-Topshiriq: ConstructorParameters<T> - Sinf konstruktori parametrlari

## Topshiriq sharti:
Sinf konstruktoriga uzatiladigan argumentlarni ConstructorParameters orqali oling.

## Yechim (JS yoki TS kodi):
```typescript
class DatabaseConnection {
    constructor(public host: string, public port: number) {}
}

type ConnParams = ConstructorParameters<typeof DatabaseConnection>; // [string, number]

const dbParams: ConnParams = ["192.168.1.100", 5432];
const db = new DatabaseConnection(...dbParams);

console.log(`DB ulandi: ${db.host}:${db.port}`);
```

## Tushuntirish va Mantiq:
ConstructorParameters<typeof Class> sinf konstruktori qabul qiladigan argumentlar to'plamini tuple sifatida taqdim etadi.

## Ishlash natijasi:
```text
DB ulandi: 192.168.1.100:5432
```


# 763-Topshiriq: InstanceType<T> - Sinf instansiyasi tipi

## Topshiriq sharti:
Konstruktor funksiyasidan hosil bo'luvchi obyekt tipini InstanceType bilan oling.

## Yechim (JS yoki TS kodi):
```typescript
class ApiManager {
    public endpoint = "https://api.domain.uz";
    fetchData() {
        return "ma'lumot";
    }
}

type ApiManagerInstance = InstanceType<typeof ApiManager>;

function runApi(manager: ApiManagerInstance) {
    console.log("Endpoint:", manager.endpoint);
}

runApi(new ApiManager());
```

## Tushuntirish va Mantiq:
InstanceType<typeof Class> sinf konstruktori ishlab chiqaradigan obyektning aniq tipini ifodalaydi.

## Ishlash natijasi:
```text
Endpoint: https://api.domain.uz
```


# 764-Topshiriq: Awaited<T> - Promise qiymatini ochish

## Topshiriq sharti:
Promise yoki ichma-ich Promise ichidagi yakuniy qiymat turini Awaited orqali oling.

## Yechim (JS yoki TS kodi):
```typescript
type AsyncNumber = Promise<number>;
type UnwrappedNumber = Awaited<AsyncNumber>; // number

type DeepPromise = Promise<Promise<string[]>>;
type UnwrappedDeep = Awaited<DeepPromise>; // string[]

const list: UnwrappedDeep = ["TS", "ES6", "Node"];
console.log("Awaited natija:", list);
```

## Tushuntirish va Mantiq:
Awaited<T> TypeScript 4.5 da joriy qilingan bo'lib, Promise zanjirlarini rekursiv yechib, yakuniy natijaviy tipni aniqlaydi.

## Ishlash natijasi:
```text
Awaited natija: [ 'TS', 'ES6', 'Node' ]
```


# 765-Topshiriq: ThisParameterType<T> - 'this' kontekstini olish

## Topshiriq sharti:
Funksiyaning 'this' parametrida belgilangan tipni ajratib oling.

## Yechim (JS yoki TS kodi):
```typescript
function greetCustomer(this: { storeName: string }, message: string) {
    console.log(`${this.storeName}: ${message}`);
}

type GreetThis = ThisParameterType<typeof greetCustomer>;

const store: GreetThis = { storeName: "Supermarket 'Baraka'" };
greetCustomer.call(store, "Xush kelibsiz!");
```

## Tushuntirish va Mantiq:
ThisParameterType funksiyadagi 'this: Context' parametrining aniq tipini sug'urib oladi.

## Ishlash natijasi:
```text
Supermarket 'Baraka': Xush kelibsiz!
```


# 766-Topshiriq: OmitThisParameter<T> - 'this' parametrini olib tashlash

## Topshiriq sharti:
Funksiya imzosidan 'this' parametrini olib tashlab, oddiy chaqiriladigan funksiya tipiga aylantirish.

## Yechim (JS yoki TS kodi):
```typescript
function logger(this: { prefix: string }, text: string): void {
    console.log(`${this.prefix} ${text}`);
}

const boundLogger: OmitThisParameter<typeof logger> = logger.bind({ prefix: "[TIZIM]:" });
boundLogger("Xizmat qayta yuklandi.");
```

## Tushuntirish va Mantiq:
OmitThisParameter funksiya oldindan bind qilingandan keyin uning tipidan this talabini olib tashlashda qo'llaniladi.

## Ishlash natijasi:
```text
[TIZIM]: Xizmat qayta yuklandi.
```


# 767-Topshiriq: ThisType<T> - Kontekstual this ni belgilash

## Topshiriq sharti:
Metodlar obyekti ichida 'this' qaysi holatga ishora qilishini ThisType bilan ta'minlang.

## Yechim (JS yoki TS kodi):
```typescript
interface State {
    count: number;
}

interface Methods {
    increment(): void;
    decrement(): void;
}

const component: { state: State; methods: Methods & ThisType<State & Methods> } = {
    state: { count: 0 },
    methods: {
        increment() {
            this.count++;
        },
        decrement() {
            this.count--;
        }
    }
};

component.methods.increment.call(component.state);
console.log("Count:", component.state.count);
```

## Tushuntirish va Mantiq:
ThisType<T> marker tipi bo'lib, obyekt metodlari ichidagi this ni T tipiga tenglashtiradi (Vue.js Options API arxitekturasida keng qo'llaniladi).

## Ishlash natijasi:
```text
Count: 1
```


# 768-Topshiriq: Pick va Omit birikmasi bilan maydon turini yangilash (Override)

## Topshiriq sharti:
Obyektdagi mavjud 'id: number' maydonini 'id: string' ga almashtiruvchi yangi tip yasang.

## Yechim (JS yoki TS kodi):
```typescript
interface Article {
    id: number;
    title: string;
    body: string;
}

type StringIdArticle = Omit<Article, "id"> & { id: string };

const doc: StringIdArticle = {
    id: "art_uuid_9941",
    title: "TypeScript Utility Types",
    body: "Utility tiplar kodni ixchamlashtiradi."
};

console.log(`Maqola ID: ${doc.id}, Nomi: ${doc.title}`);
```

## Tushuntirish va Mantiq:
Omit<T, K> & { K: NewType } usuli mavjud interfeysdagi biror maydonning tipini o'zgartirish (override) uchun eng standart va toza uslubdir.

## Ishlash natijasi:
```text
Maqola ID: art_uuid_9941, Nomi: TypeScript Utility Types
```


# 769-Topshiriq: RequireAtLeastOne custom utility tipi

## Topshiriq sharti:
Obyektda berilgan kalitlardan kamida bittasi majburiy bo'lishini talab qiluvchi utility tipini yozing.

## Yechim (JS yoki TS kodi):
```typescript
type RequireAtLeastOne<T, Keys extends keyof T = keyof T> =
    Pick<T, Exclude<keyof T, Keys>> &
    {
        [K in Keys]-?: Required<Pick<T, K>> & Partial<Pick<T, Exclude<Keys, K>>>
    }[Keys];

interface ContactOptions {
    email?: string;
    phone?: string;
    telegram?: string;
}

type ValidContact = RequireAtLeastOne<ContactOptions>;

const c1: ValidContact = { email: "ali@pochta.uz" };
const c2: ValidContact = { phone: "+998901234567", telegram: "@ali_dev" };

console.log("Aloqa 1:", c1);
console.log("Aloqa 2:", c2);
```

## Tushuntirish va Mantiq:
RequireAtLeastOne kamida bitta aloqa vositasi kiritilishi shart bo'lgan formalar uchun kuchli tiplash imkonini beradi.

## Ishlash natijasi:
```text
Aloqa 1: { email: 'ali@pochta.uz' }
Aloqa 2: { phone: '+998901234567', telegram: '@ali_dev' }
```


# 770-Topshiriq: ValueOf<T> custom utility tipi

## Topshiriq sharti:
Obyektning barcha mumkin bo'lgan qiymatlari birlashmasini oluvchi ValueOf tipini yozing.

## Yechim (JS yoki TS kodi):
```typescript
type ValueOf<T> = T[keyof T];

interface ThemeColors {
    background: "#ffffff";
    text: "#000000";
    accent: "#ff5722";
}

type AppColor = ValueOf<ThemeColors>; // "#ffffff" | "#000000" | "#ff5722"

const myColor: AppColor = "#ff5722";
console.log("Ilova rangi:", myColor);
```

## Tushuntirish va Mantiq:
ValueOf<T> sintaksisi T[keyof T] orqali obyekt ichidagi har bir xossaning qiymatini union shaklida birlashtirib beradi.

## Ishlash natijasi:
```text
Ilova rangi: #ff5722
```


# 771-Topshiriq: Mutable<T> - Readonly ni olib tashlash

## Topshiriq sharti:
Readonly xossalarni yana o'zgaruvchan qilish uchun -readonly modifikatorli utility tip yozing.

## Yechim (JS yoki TS kodi):
```typescript
type Mutable<T> = {
    -readonly [P in keyof T]: T[P];
};

interface ImmutableConfig {
    readonly mode: string;
    readonly debug: boolean;
}

const liveConfig: Mutable<ImmutableConfig> = { mode: "development", debug: false };
liveConfig.mode = "production";
liveConfig.debug = true;

console.log("Yangilangan sozlama:", liveConfig);
```

## Tushuntirish va Mantiq:
Mutable<T> obyektdan barcha readonly xususiyatlarni olib tashlaydi.

## Ishlash natijasi:
```text
Yangilangan sozlama: { mode: 'production', debug: true }
```


# 772-Topshiriq: Nullable<T> va NullableFields<T>

## Topshiriq sharti:
Obyekt maydonlariga null qiymat qabul qilish imkoniyatini beruvchi utility tiplar.

## Yechim (JS yoki TS kodi):
```typescript
type Nullable<T> = T | null;
type NullableFields<T> = {
    [K in keyof T]: Nullable<T[K]>;
};

interface Invoice {
    id: number;
    amount: number;
    paidAt: Date;
}

const draftInvoice: NullableFields<Invoice> = {
    id: 1001,
    amount: null,
    paidAt: null
};

console.log("Qoralama faktura:", draftInvoice);
```

## Tushuntirish va Mantiq:
Baza yoki formadan kelayotgan bo'sh qiymatlarni ifodalash uchun NullableFields juda qo'l keladi.

## Ishlash natijasi:
```text
Qoralama faktura: { id: 1001, amount: null, paidAt: null }
```


# 773-Topshiriq: StrictUnion (XOR) amaliyoti

## Topshiriq sharti:
Ikki interfeysdan birini tanlaganda ikkinchisining xossalari qat'iy taqiqlanishi (XOR).

## Yechim (JS yoki TS kodi):
```typescript
type Without<T, U> = { [P in Exclude<keyof T, keyof U>]?: never };
type XOR<T, U> = (T | U) extends object ? (Without<T, U> & U) | (Without<U, T> & T) : T | U;

interface EmailAuth { email: string; }
interface PhoneAuth { phone: string; }

type AuthOption = XOR<EmailAuth, PhoneAuth>;

const validAuth1: AuthOption = { email: "user@domain.com" };
const validAuth2: AuthOption = { phone: "+998900000000" };

console.log("Auth 1:", validAuth1);
console.log("Auth 2:", validAuth2);
```

## Tushuntirish va Mantiq:
XOR (Exclusive OR) har ikkala parametr bir vaqtda kiritilishining oldini oladi va faqat bittasini majburiy qiladi.

## Ishlash natijasi:
```text
Auth 1: { email: 'user@domain.com' }
Auth 2: { phone: '+998900000000' }
```


# 774-Topshiriq: Record kalitlarini Enum orqali cheklash

## Topshiriq sharti:
Enum qiymatlarini Record kaliti sifatida ishlatish.

## Yechim (JS yoki TS kodi):
```typescript
enum HttpStatus {
    OK = 200,
    NOT_FOUND = 404,
    SERVER_ERROR = 500
}

const statusMessages: Record<HttpStatus, string> = {
    [HttpStatus.OK]: "Muvaffaqiyatli",
    [HttpStatus.NOT_FOUND]: "Topilmadi",
    [HttpStatus.SERVER_ERROR]: "Serverda xatolik"
};

console.log(`404 xabari: ${statusMessages[HttpStatus.NOT_FOUND]}`);
```

## Tushuntirish va Mantiq:
Record<Enum, Value> enumning har bir a'zosi lug'atda qatnashishini shart qilib qo'yadi.

## Ishlash natijasi:
```text
404 xabari: Topilmadi
```


# 775-Topshiriq: Pick yordamida DTO (Data Transfer Object) yaratish

## Topshiriq sharti:
Foydalanuvchi ro'yxatdan o'tishi uchun kerak bo'ladigan CreateUserDto ni Pick orqali yasang.

## Yechim (JS yoki TS kodi):
```typescript
interface UserEntity {
    id: number;
    name: string;
    email: string;
    createdAt: Date;
    updatedAt: Date;
}

type CreateUserDto = Pick<UserEntity, "name" | "email">;

const newUser: CreateUserDto = {
    name: "Murod",
    email: "murod@pochta.uz"
};

console.log("Yangi DTO:", newUser);
```

## Tushuntirish va Mantiq:
Ma'lumotlar bazasi modelidan serverga kiruvchi DTO larni Pick orqali tezkor va xatosiz yaratish mumkin.

## Ishlash natijasi:
```text
Yangi DTO: { name: 'Murod', email: 'murod@pochta.uz' }
```


# 776-Topshiriq: FunctionKeys<T> - Faqat funksiya kalitlarini ajratish

## Topshiriq sharti:
Obyektdan faqat metodlarning nomlarini ajratib oluvchi utility tip.

## Yechim (JS yoki TS kodi):
```typescript
type FunctionKeys<T> = {
    [K in keyof T]: T[K] extends (...args: any[]) => any ? K : never;
}[keyof T];

class Player {
    score: number = 0;
    name: string = "Player1";
    play(): void {}
    pause(): void {}
}

type PlayerMethods = FunctionKeys<Player>; // "play" | "pause"

const m: PlayerMethods = "play";
console.log("Metod nomi:", m);
```

## Tushuntirish va Mantiq:
FunctionKeys metodlarni dinamik chaqirish yoki avtomatlashtirishda faqat funksiyalarni tanlash imkonini beradi.

## Ishlash natijasi:
```text
Metod nomi: play
```


# 777-Topshiriq: NonFunctionKeys<T> - Faqat ma'lumot kalitlarini ajratish

## Topshiriq sharti:
Sinfdan faqat ma'lumot maydonlarini ajratib oluvchi utility tip.

## Yechim (JS yoki TS kodi):
```typescript
type NonFunctionKeys<T> = {
    [K in keyof T]: T[K] extends (...args: any[]) => any ? never : K;
}[keyof T];

class Vehicle {
    speed: number = 60;
    color: string = "qora";
    drive() {}
    stop() {}
}

type VehicleProperties = NonFunctionKeys<Vehicle>; // "speed" | "color"

const prop: VehicleProperties = "speed";
console.log("Xossa nomi:", prop);
```

## Tushuntirish va Mantiq:
NonFunctionKeys sinfdan holat (state) ma'lumotlarini ajratib olish va saqlashda qo'llaniladi.

## Ishlash natijasi:
```text
Xossa nomi: speed
```


# 778-Topshiriq: OptionalKeys<T> - Faqat ixtiyoriy kalitlarni topish

## Topshiriq sharti:
Qaysi maydonlar ixtiyoriy ekanligini aniqlovchi utility tip.

## Yechim (JS yoki TS kodi):
```typescript
type OptionalKeys<T> = {
    [K in keyof T]-?: {} extends Pick<T, K> ? K : never;
}[keyof T];

interface Profile {
    id: number;
    bio?: string;
    avatarUrl?: string;
}

type OptionalProfileFields = OptionalKeys<Profile>; // "bio" | "avatarUrl"

const optField: OptionalProfileFields = "bio";
console.log("Ixtiyoriy maydon:", optField);
```

## Tushuntirish va Mantiq:
{} extends Pick<T, K> tekshiruvi orqali maydon ixtiyoriy bo'lsa kalit saqlanadi, majburiy bo'lsa never ga aylanadi.

## Ishlash natijasi:
```text
Ixtiyoriy maydon: bio
```


# 779-Topshiriq: RequiredKeys<T> - Faqat majburiy kalitlarni topish

## Topshiriq sharti:
Interfeysdagi majburiy maydonlarni ajratib oluvchi utility tip.

## Yechim (JS yoki TS kodi):
```typescript
type RequiredKeys<T> = {
    [K in keyof T]-?: {} extends Pick<T, K> ? never : K;
}[keyof T];

interface ServerConfig {
    host: string;
    port: number;
    debug?: boolean;
}

type ReqFields = RequiredKeys<ServerConfig>; // "host" | "port"

const req: ReqFields = "host";
console.log("Majburiy maydon:", req);
```

## Tushuntirish va Mantiq:
RequiredKeys obyektning qaysi parametrlari to'ldirilishi shart ekanligini dasturiy tekshirishda ishlatiladi.

## Ishlash natijasi:
```text
Majburiy maydon: host
```


# 780-Topshiriq: PickByValue<T, ValueType> utility tipi

## Topshiriq sharti:
Faqat ma'lum qiymat tipiga mos xossalarni tanlab oluvchi utility tip.

## Yechim (JS yoki TS kodi):
```typescript
type PickByValue<T, V> = Pick<T, {
    [K in keyof T]: T[K] extends V ? K : never;
}[keyof T]>;

interface Stats {
    views: number;
    likes: number;
    title: string;
    isTrending: boolean;
}

type NumericStats = PickByValue<Stats, number>; // { views: number; likes: number; }

const stats: NumericStats = { views: 1200, likes: 450 };
console.log("Raqamli statistika:", stats);
```

## Tushuntirish va Mantiq:
PickByValue obyektdan bir xil turdagi barcha xossalarni birato'la ajratib olish imkonini beradi.

## Ishlash natijasi:
```text
Raqamli statistika: { views: 1200, likes: 450 }
```


# 781-Topshiriq: OmitByValue<T, ValueType> utility tipi

## Topshiriq sharti:
Ma'lum qiymat tipidagi barcha xossalarni chiqarib tashlovchi utility tip.

## Yechim (JS yoki TS kodi):
```typescript
type OmitByValue<T, V> = Pick<T, {
    [K in keyof T]: T[K] extends V ? never : K;
}[keyof T]>;

interface MetaItem {
    id: number;
    title: string;
    description: string;
    archived: boolean;
}

type NonStringMeta = OmitByValue<MetaItem, string>; // { id: number; archived: boolean; }

const item: NonStringMeta = { id: 1, archived: false };
console.log("Satr bo'lmagan xossalar:", item);
```

## Tushuntirish va Mantiq:
OmitByValue ma'lum turdagi maydonlarni (masalan, funksiyalar yoki booleans) filtrlab tashlashda qo'llaniladi.

## Ishlash natijasi:
```text
Satr bo'lmagan xossalar: { id: 1, archived: false }
```


# 782-Topshiriq: Merge<T, U> - Ikki obyektni o'zaro ustunlik bilan birlashtirish

## Topshiriq sharti:
U dagi maydonlar T dagi bir xil nomli maydonlarni almashtiruvchi (override qiluvchi) Merge tipi.

## Yechim (JS yoki TS kodi):
```typescript
type Merge<T, U> = Omit<T, keyof U> & U;

interface BaseProps {
    id: number;
    color: string;
    size: number;
}

interface CustomProps {
    color: { r: number; g: number; b: number }; // color o'zgardi
    label: string; // yangi maydon
}

type FinalProps = Merge<BaseProps, CustomProps>;

const props: FinalProps = {
    id: 1,
    size: 24,
    color: { r: 255, g: 0, b: 0 },
    label: "Tugma"
};

console.log("Birlashtirilgan xossalar:", props);
```

## Tushuntirish va Mantiq:
Merge<T, U> tipi komponentlar xossalarini (props) kengaytirishda eski maydonlarni yangi tur bilan almashtirish uchun idealdir.

## Ishlash natijasi:
```text
Birlashtirilgan xossalar: { id: 1, size: 24, color: { r: 255, g: 0, b: 0 }, label: 'Tugma' }
```


# 783-Topshiriq: ReadonlyKeys<T> va WritableKeys<T>

## Topshiriq sharti:
Obyektdagi qaysi kalitlar readonly ekanligini aniqlash.

## Yechim (JS yoki TS kodi):
```typescript
type IfEquals<X, Y, A = X, B = never> =
    (<T>() => T extends X ? 1 : 2) extends (<T>() => T extends Y ? 1 : 2) ? A : B;

type ReadonlyKeys<T> = {
    [P in keyof T]-?: IfEquals<{ [Q in P]: T[P] }, { -readonly [Q in P]: T[P] }, never, P>
}[keyof T];

interface Account {
    readonly id: number;
    username: string;
}

type ReadonlyFields = ReadonlyKeys<Account>; // "id"

const readField: ReadonlyFields = "id";
console.log("Faqat o'qiladigan kalit:", readField);
```

## Tushuntirish va Mantiq:
IfEquals yordamida readonly va mutable xossalar o'rtasidagi farq tekshirilib, faqat readonly maydonlar topiladi.

## Ishlash natijasi:
```text
Faqat o'qiladigan kalit: id
```


# 784-Topshiriq: DeepReadonly bilan ichma-ich konfiguratsiyani himoyalash

## Topshiriq sharti:
Barcha ichki obyektlarni ham o'zgarmas qilish.

## Yechim (JS yoki TS kodi):
```typescript
type DeepReadonly<T> = {
    readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P];
};

const appSettings: DeepReadonly<{ server: { host: string; port: number } }> = {
    server: { host: "127.0.0.1", port: 3000 }
};

console.log("Xost:", appSettings.server.host);
```

## Tushuntirish va Mantiq:
DeepReadonly rekursiv bo'lib, har qanday chuqurlikdagi obyektning tasodifiy o'zgartirilishini man etadi.

## Ishlash natijasi:
```text
Xost: 127.0.0.1
```


# 785-Topshiriq: DeepPartial bilan qisman konfiguratsiya qabul qilish

## Topshiriq sharti:
Har qanday ichki obyektning biror qismini yangilash.

## Yechim (JS yoki TS kodi):
```typescript
type DeepPartial<T> = {
    [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

interface FullConfig {
    theme: {
        dark: boolean;
        colors: {
            primary: string;
            secondary: string;
        };
    };
}

const partialConf: DeepPartial<FullConfig> = {
    theme: {
        colors: {
            primary: "#ff0000"
        }
    }
};

console.log("Rang:", partialConf.theme?.colors?.primary);
```

## Tushuntirish va Mantiq:
DeepPartial konfiguratsiya fayllari va sozlamalarni yangilashda keng qo'llaniladi.

## Ishlash natijasi:
```text
Rang: #ff0000
```


# 786-Topshiriq: TupleToUnion utility tipi

## Topshiriq sharti:
Tuple massividan union tip hosil qilish.

## Yechim (JS yoki TS kodi):
```typescript
type TupleToUnion<T extends any[]> = T[number];

type StatusList = ["pending", "in_progress", "done"];
type TaskStatus = TupleToUnion<StatusList>; // "pending" | "in_progress" | "done"

const task: TaskStatus = "in_progress";
console.log("Vazifa holati:", task);
```

## Tushuntirish va Mantiq:
T[number] indeksi massiv yoki tuple elementlarining barcha variantlarini birlashtiradi.

## Ishlash natijasi:
```text
Vazifa holati: in_progress
```


# 787-Topshiriq: UnionToIntersection yordamida obyektlarni birlashtirish

## Topshiriq sharti:
Bir nechta obyekt interfeyslarining unionini yagona kesishma tipga aylantirish.

## Yechim (JS yoki TS kodi):
```typescript
type UnionToIntersection<U> =
    (U extends any ? (k: U) => void : never) extends ((k: infer I) => void) ? I : never;

type U = { name: string } | { age: number } | { city: string };
type Intersected = UnionToIntersection<U>; // { name: string } & { age: number } & { city: string }

const fullObj: Intersected = { name: "Botir", age: 30, city: "Samarqand" };
console.log("To'liq obyekt:", fullObj);
```

## Tushuntirish va Mantiq:
UnionToIntersection shartli tiplar va funksiya parametrlari kontravariantligi orqali ishlaydi.

## Ishlash natijasi:
```text
To'liq obyekt: { name: 'Botir', age: 30, city: 'Samarqand' }
```


# 788-Topshiriq: Awaited bilan asinxron ma'lumotlar oqimini to'g'ri tiplash

## Topshiriq sharti:
Asinxron funksiyaning natijasini olish va uni parametr sifatida ishlatish.

## Yechim (JS yoki TS kodi):
```typescript
async function fetchServerStatus() {
    return {
        online: true,
        load: 0.42,
        activeConnections: 120
    };
}

type ServerStatus = Awaited<ReturnType<typeof fetchServerStatus>>;

function renderStatus(status: ServerStatus) {
    console.log(`Server online: ${status.online}, Yuklama: ${status.load}`);
}

fetchServerStatus().then(renderStatus);
```

## Tushuntirish va Mantiq:
Awaited<ReturnType<typeof fn>> asinxron funksiyaning Promise ichidagi yakuniy obyekt turini chiqaradi.

## Ishlash natijasi:
```text
Server online: true, Yuklama: 0.42
```


# 789-Topshiriq: Omit yordamida User modelidan parolni yashirgan PublicUser tipi yasash

## Topshiriq sharti:
Ma'lumotlar bazasi foydalanuvchi modelini xavfsiz ommaviy API javobiga aylantirish.

## Yechim (JS yoki TS kodi):
```typescript
interface UserDbModel {
    id: number;
    username: string;
    email: string;
    passwordHash: string;
    refreshToken: string;
}

type SafeUserResponse = Omit<UserDbModel, "passwordHash" | "refreshToken">;

function sanitizeUser(user: UserDbModel): SafeUserResponse {
    const { passwordHash, refreshToken, ...safe } = user;
    return safe;
}

const dbUser: UserDbModel = {
    id: 1,
    username: "islom_coder",
    email: "islom@coder.uz",
    passwordHash: "hash_xyz_123",
    refreshToken: "token_abc"
};

console.log("Xavfsiz foydalanuvchi:", sanitizeUser(dbUser));
```

## Tushuntirish va Mantiq:
Omit xavfsizlik nuqtai nazaridan maxfiy maydonlarning tashqi dunyoga sizib chiqishini tiplar darajasida bloklaydi.

## Ishlash natijasi:
```text
Xavfsiz foydalanuvchi: { id: 1, username: 'islom_coder', email: 'islom@coder.uz' }
```


# 790-Topshiriq: Parameters bilan middleware funksiyalarini zanjirlash

## Topshiriq sharti:
Middleware qabul qiluvchi parametrlarni avtomatik ko'chirish.

## Yechim (JS yoki TS kodi):
```typescript
type RequestHandler = (req: { path: string; user?: string }, res: { send(body: string): void }) => void;

function logMiddleware(handler: RequestHandler): (...args: Parameters<RequestHandler>) => void {
    return (req, res) => {
        console.log(`So'rov keldi: ${req.path}`);
        handler(req, res);
    };
}

const myHandler: RequestHandler = (req, res) => res.send("OK");
const wrapped = logMiddleware(myHandler);
wrapped({ path: "/api/users" }, { send: (s) => console.log(s) });
```

## Tushuntirish va Mantiq:
Parameters<RequestHandler> orqali middleware original funksiya bilan 100% bir xil argumentlarni qabul qilishi ta'minlanadi.

## Ishlash natijasi:
```text
So'rov keldi: /api/users
OK
```


# 791-Topshiriq: ReturnType bilan Redux Action Creator natijasini tiplash

## Topshiriq sharti:
Redux action creator funksiyasining qaytargan action obyektini tiplash.

## Yechim (JS yoki TS kodi):
```typescript
const setFilter = (filterName: string) => ({
    type: "SET_FILTER" as const,
    payload: filterName
});

type SetFilterAction = ReturnType<typeof setFilter>;

const action: SetFilterAction = setFilter("active");
console.log("Action turi:", action.type, "Payload:", action.payload);
```

## Tushuntirish va Mantiq:
ReturnType<typeof setFilter> action yaratuvchi funksiyalardan Action tiplarini qo'lda yozmasdan avtomatik olish imkonini beradi.

## Ishlash natijasi:
```text
Action turi: SET_FILTER Payload: active
```


# 792-Topshiriq: ConstructorParameters bilan universal instansiya yaratuvchi fabrika

## Topshiriq sharti:
Har qanday sinf uchun konstruktor parametrlarini saqlagan holda fabrika funksiya yozish.

## Yechim (JS yoki TS kodi):
```typescript
class LoggerService {
    constructor(private appName: string, private level: number) {}
    log(msg: string) {
        console.log(`[${this.appName} Lvl:${this.level}] ${msg}`);
    }
}

function createService<T extends new (...args: any[]) => any>(
    Cls: T,
    ...args: ConstructorParameters<T>
): InstanceType<T> {
    return new Cls(...args);
}

const logger = createService(LoggerService, "E-Bozor", 1);
logger.log("Xizmat faollashdi.");
```

## Tushuntirish va Mantiq:
ConstructorParameters va InstanceType birgalikda to'liq tiplangan Factory funksiyalarini yaratishga imkon beradi.

## Ishlash natijasi:
```text
[E-Bozor Lvl:1] Xizmat faollashdi.
```


# 793-Topshiriq: String bo'lmagan xossalarni Omit qilish

## Topshiriq sharti:
Faqat satrli xossalardan iborat obyekt tipini yasash.

## Yechim (JS yoki TS kodi):
```typescript
interface Mixed {
    id: number;
    name: string;
    address: string;
    isActive: boolean;
}

type OnlyStringProps<T> = Pick<T, {
    [K in keyof T]: T[K] extends string ? K : never;
}[keyof T]>;

const strOnly: OnlyStringProps<Mixed> = {
    name: "Toshkent",
    address: "Amir Temur ko'chasi"
};

console.log("Faqat satrlar:", strOnly);
```

## Tushuntirish va Mantiq:
Ushbu naqsh formalar va matnli filtrlash komponentlarida ma'lumotlarni saralashda qo'llaniladi.

## Ishlash natijasi:
```text
Faqat satrlar: { name: 'Toshkent', address: 'Amir Temur ko\'chasi' }
```


# 794-Topshiriq: Readonly<Record<string, string>> - O'zgarmas konfiguratsiya lug'ati

## Topshiriq sharti:
Tashqaridan hech qanday o'zgartirish kiritib bo'lmaydigan xaritalangan lug'at.

## Yechim (JS yoki TS kodi):
```typescript
const ENV_VARS: Readonly<Record<string, string>> = {
    NODE_ENV: "production",
    API_URL: "https://api.domain.uz"
};

// ENV_VARS["PORT"] = "3000"; // Kompilyatsiya xatosi beradi!
console.log("Muhit o'zgaruvchilari:", ENV_VARS.NODE_ENV);
```

## Tushuntirish va Mantiq:
Readonly bilan Record birikmasi global konfiguratsiya obyektlarining butunligini saqlaydi.

## Ishlash natijasi:
```text
Muhit o'zgaruvchilari: production
```


# 795-Topshiriq: StrictExtract va StrictExclude

## Topshiriq sharti:
Birlashmalardan aniq tiplarni ajratib olish va chiqarib tashlash amaliyoti.

## Yechim (JS yoki TS kodi):
```typescript
type HttpMethod = "GET" | "POST" | "PUT" | "DELETE" | "PATCH";

type ReadMethods = Extract<HttpMethod, "GET">;
type WriteMethods = Exclude<HttpMethod, "GET">;

const read: ReadMethods = "GET";
const write: WriteMethods = "POST";

console.log(`O'qish amali: ${read}, Yozish amali: ${write}`);
```

## Tushuntirish va Mantiq:
Extract va Exclude REST API usullarini huquqlar bo'yicha toifalashda juda aniq natija beradi.

## Ishlash natijasi:
```text
O'qish amali: GET, Yozish amali: POST
```


# 796-Topshiriq: Required va Partial kombinatsiyasi (Selected Partial)

## Topshiriq sharti:
Obyektdagi ma'lum maydonlarni ixtiyoriy, qolganlarini majburiy qilish.

## Yechim (JS yoki TS kodi):
```typescript
interface ArticleEntity {
    id: number;
    title: string;
    content: string;
    author: string;
}

type CreateArticleInput = Pick<ArticleEntity, "title" | "content"> & Partial<Pick<ArticleEntity, "author">>;

const art1: CreateArticleInput = { title: "Yangiliklar", content: "Matn..." };
const art2: CreateArticleInput = { title: "Maqola", content: "Matn...", author: "Ali" };

console.log("Maqola 1:", art1.title);
console.log("Maqola 2 muallifi:", art2.author);
```

## Tushuntirish va Mantiq:
Pick va Partial birikmasi orqali qaysi xossalar majburiy va qaysilari ixtiyoriy ekanligini erkin sozlash mumkin.

## Ishlash natijasi:
```text
Maqola 1: Yangiliklar
Maqola 2 muallifi: Ali
```


# 797-Topshiriq: Capitalize va Uncapitalize utility tiplari

## Topshiriq sharti:
Satrli literallarni bosh harfga yoki kichik harfga o'tkazish.

## Yechim (JS yoki TS kodi):
```typescript
type EventName = "click" | "change";
type HandlerName = `on${Capitalize<EventName>}`; // "onClick" | "onChange"

const handler: HandlerName = "onClick";
console.log("Hodisa tinglovchi nomi:", handler);
```

## Tushuntirish va Mantiq:
Capitalize hodisalar (event handlers) nomlarini avtomatik generatsiya qilishda keng qo'llaniladi.

## Ishlash natijasi:
```text
Hodisa tinglovchi nomi: onClick
```


# 798-Topshiriq: NonNullable bilan massiv elementlarini tozalash

## Topshiriq sharti:
Elementlari orasida null bo'lishi mumkin bo'lgan massivni NonNullable bilan tiplash.

## Yechim (JS yoki TS kodi):
```typescript
type NullableItems = (string | null | undefined)[];
type PureItem = NonNullable<NullableItems[number]>; // string

const pureValue: PureItem = "Toza matn";
console.log("Toza qiymat:", pureValue);
```

## Tushuntirish va Mantiq:
NonNullable massiv elementlari tipidan null va undefined ni olib tashlab, qat'iy ma'lumotlar bilan ishlashni ta'minlaydi.

## Ishlash natijasi:
```text
Toza qiymat: Toza matn
```


# 799-Topshiriq: Custom DeepMutable utility tipi

## Topshiriq sharti:
Ichma-ich barcha readonly xossalarni o'zgaruvchan qilish.

## Yechim (JS yoki TS kodi):
```typescript
type DeepMutable<T> = {
    -readonly [P in keyof T]: T[P] extends object ? DeepMutable<T[P]> : T[P];
};

interface LockedData {
    readonly meta: {
        readonly version: number;
    };
}

const editable: DeepMutable<LockedData> = {
    meta: { version: 1 }
};

editable.meta.version = 2;
console.log("O'zgartirilgan versiya:", editable.meta.version);
```

## Tushuntirish va Mantiq:
DeepMutable chuqur readonly obyektlarni tahrirlanadigan holatga keltiradi.

## Ishlash natijasi:
```text
O'zgartirilgan versiya: 2
```


# 800-Topshiriq: CRUD tizimi uchun to'liq Utility Tiplar majmuasi

## Topshiriq sharti:
Yagona Entity asosida CreateDto, UpdateDto va ResponseDto larni shakllantirish.

## Yechim (JS yoki TS kodi):
```typescript
interface UserEntity {
    id: number;
    username: string;
    email: string;
    passwordHash: string;
    createdAt: Date;
    updatedAt: Date;
}

// Yaratish uchun faqat username, email va parol kerak
type CreateUserDto = Pick<UserEntity, "username" | "email"> & { password: string };

// Yangilash uchun faqat username va email ixtiyoriy bo'lishi mumkin
type UpdateUserDto = Partial<Pick<UserEntity, "username" | "email">>;

// Ommaviy javobda parol va sanalardan tashqari qolganlar
type UserResponseDto = Omit<UserEntity, "passwordHash">;

const createPayload: CreateUserDto = {
    username: "islomjon",
    email: "islom@uz.dev",
    password: "secretPassword123"
};

const updatePayload: UpdateUserDto = {
    username: "islom_yangi"
};

console.log("Create DTO:", createPayload.username);
console.log("Update DTO:", updatePayload.username);
```

## Tushuntirish va Mantiq:
Enterprise arxitekturada yagona UserEntity interfeysidan Pick, Omit, Partial orqali barcha qatlamlar (API, Servis, DB) uchun DTO lar hosil qilinadi va kodning DRY tamoyiliga mos kelishi ta'minlanadi.

## Ishlash natijasi:
```text
Create DTO: islomjon
Update DTO: islom_yangi
```

