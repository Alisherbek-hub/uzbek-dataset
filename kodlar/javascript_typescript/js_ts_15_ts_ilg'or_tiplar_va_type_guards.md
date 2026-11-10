# 701-Topshiriq: typeof Type Guard bilan tiplarni toraytirish (Narrowing)

## Topshiriq sharti:
Kiruvchi qiymat string yoki number bo'lishi mumkin bo'lgan holatda typeof orqali har biriga mos ishlov bering.

## Yechim (JS yoki TS kodi):
```typescript
function processValue(val: string | number): string {
    if (typeof val === "string") {
        return `Satr uzunligi: ${val.length}`;
    } else {
        return `Sonning kvadrati: ${val * val}`;
    }
}

console.log(processValue("Alisher"));
console.log(processValue(8));
```

## Tushuntirish va Mantiq:
JavaScriptning typeof operatori if sharti ichida ishlatilganda, TypeScript kompilyatori shart blokida tipni string yoki number ekanligini avtomatik toraytiradi (narrowing).

## Ishlash natijasi:
```text
Satr uzunligi: 7
Sonning kvadrati: 64
```


# 702-Topshiriq: instanceof Type Guard bilan obyekt klassini tekshirish

## Topshiriq sharti:
Date yoki RegExp obyektini qabul qilib, uning klassiga qarab turlicha amal bajaruvchi funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
function inspectObject(obj: Date | RegExp): void {
    if (obj instanceof Date) {
        console.log(`Sana yili: ${obj.getFullYear()}`);
    } else {
        console.log(`Muntazam ifoda andozasi: ${obj.source}`);
    }
}

inspectObject(new Date(2025, 0, 1));
inspectObject(/^[a-z]+$/i);
```

## Tushuntirish va Mantiq:
instanceof operatori obyektning prototip zanjirini tekshiradi va TypeScript uning qaysi sinf instansiyasi ekanligini aniq biladi.

## Ishlash natijasi:
```text
Sana yili: 2025
Muntazam ifoda andozasi: ^[a-z]+$
```


# 703-Topshiriq: in operatori bilan xossalar orqali toraytirish

## Topshiriq sharti:
Admin va User interfeyslaridan biriga tegishli obyektni uning 'role' xossasi bor-yo'qligiga qarab aniqlang.

## Yechim (JS yoki TS kodi):
```typescript
interface User {
    id: number;
    username: string;
}

interface Admin extends User {
    role: "admin" | "superadmin";
    permissions: string[];
}

function handleAccount(account: User | Admin): void {
    if ("role" in account) {
        console.log(`Admin roli: ${account.role}, Ruxsatlar: ${account.permissions.length}`);
    } else {
        console.log(`Oddiy foydalanuvchi: ${account.username}`);
    }
}

handleAccount({ id: 1, username: "bekzod" });
handleAccount({ id: 2, username: "super_ali", role: "admin", permissions: ["ALL"] });
```

## Tushuntirish va Mantiq:
'property' in obj tekshiruvi berilgan xossaga ega bo'lgan interfeysni ajratishda juda qulay Type Guard vazifasini bajaradi.

## Ishlash natijasi:
```text
Oddiy foydalanuvchi: bekzod
Admin roli: admin, Ruxsatlar: 1
```


# 704-Topshiriq: Foydalanuvchi tomonidan yaratilgan Type Guard (is operatori)

## Topshiriq sharti:
Berilgan noma'lum qiymat Dog interfeysiga mosligini tekshiruvchi maxsus isDog funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
interface Dog {
    bark(): void;
}

function isDog(pet: any): pet is Dog {
    return pet !== null && typeof pet === "object" && typeof pet.bark === "function";
}

const animal: any = { bark: () => console.log("Vov-vov!") };

if (isDog(animal)) {
    animal.bark(); // TS bu yerda animal ni Dog deb hisoblaydi
}
```

## Tushuntirish va Mantiq:
pet is Dog qaytaruvchi funksiya Type Predicate deyiladi. Agar funksiya true qaytarsa, TypeScript chaqiruvchi blok ichida animal tipini aniq Dog deb taniydi.

## Ishlash natijasi:
```text
Vov-vov!
```


# 705-Topshiriq: Massivni filtrlashda Type Guard qo'llash

## Topshiriq sharti:
(string | null | undefined) elementlardan iborat massivdan faqat toza stringlarni ajratib oluvchi type guard yozing.

## Yechim (JS yoki TS kodi):
```typescript
function isNonNullableString(val: string | null | undefined): val is string {
    return typeof val === "string";
}

const rawList = ["Toshkent", null, "Samarqand", undefined, "Xiva"];
const cleanList: string[] = rawList.filter(isNonNullableString);

console.log("Toza shaharlar ro'yxati:", cleanList);
```

## Tushuntirish va Mantiq:
filter(isNonNullableString) dan so'ng natija massivining tipi (string | null | undefined)[] dan string[] ga avtomatik torayadi.

## Ishlash natijasi:
```text
Toza shaharlar ro'yxati: [ 'Toshkent', 'Samarqand', 'Xiva' ]
```


# 706-Topshiriq: Ajratilgan birlashmalar (Discriminated Unions)

## Topshiriq sharti:
Kvadrat, Doira va To'g'ri to'rtburchak uchun kind literal xossasiga ega shakllar birlashmasini tuzing va yuzini hisoblang.

## Yechim (JS yoki TS kodi):
```typescript
interface Circle { kind: "circle"; radius: number; }
interface Square { kind: "square"; side: number; }
interface Rectangle { kind: "rectangle"; width: number; height: number; }

type Shape = Circle | Square | Rectangle;

function getArea(shape: Shape): number {
    switch (shape.kind) {
        case "circle": return Math.PI * shape.radius ** 2;
        case "square": return shape.side * shape.side;
        case "rectangle": return shape.width * shape.height;
    }
}

console.log("Kvadrat yuzi:", getArea({ kind: "square", side: 5 }));
console.log("To'rtburchak yuzi:", getArea({ kind: "rectangle", width: 4, height: 6 }));
```

## Tushuntirish va Mantiq:
Barcha variantlarda bir xil nomli literal xossa (masalan, kind) mavjud bo'lsa, bu Discriminated (Tagged) Union deyiladi va switch/case da mukammal ishlaydi.

## Ishlash natijasi:
```text
Kvadrat yuzi: 25
To'rtburchak yuzi: 24
```


# 707-Topshiriq: Discriminated Unions bilan Redux Action Pattern

## Topshiriq sharti:
Redux uslubidagi Action tiplari va reducerni xavfsiz boshqarish.

## Yechim (JS yoki TS kodi):
```typescript
type Action =
    | { type: "LOGIN"; payload: { userId: number } }
    | { type: "LOGOUT" }
    | { type: "UPDATE_STATUS"; payload: { statusText: string } };

function appReducer(state: { loggedIn: boolean; status: string }, action: Action) {
    switch (action.type) {
        case "LOGIN":
            return { loggedIn: true, status: `User #${action.payload.userId} faol` };
        case "LOGOUT":
            return { loggedIn: false, status: "Chiqilgan" };
        case "UPDATE_STATUS":
            return { ...state, status: action.payload.statusText };
    }
}

const st1 = appReducer({ loggedIn: false, status: "" }, { type: "LOGIN", payload: { userId: 42 } });
console.log("Yangi holat:", st1);
```

## Tushuntirish va Mantiq:
action.type ga qarab action.payload mavjudligi va uning tipi avtomatik ravishda to'g'ri aniqlanadi.

## Ishlash natijasi:
```text
Yangi holat: { loggedIn: true, status: 'User #42 faol' }
```


# 708-Topshiriq: Exhaustive Checking va `never` tipi

## Topshiriq sharti:
Switch blokida barcha holatlar tekshirilganligini kompilyatsiya darajasida kafolatlang.

## Yechim (JS yoki TS kodi):
```typescript
type NetworkState = "IDLE" | "LOADING" | "SUCCESS" | "FAILED";

function handleNetwork(state: NetworkState): string {
    switch (state) {
        case "IDLE": return "Kutilmoqda...";
        case "LOADING": return "Yuklanmoqda...";
        case "SUCCESS": return "Muvaffaqiyatli yakunlandi!";
        case "FAILED": return "Xatolik yuz berdi!";
        default: {
            const _exhaustiveCheck: never = state;
            return _exhaustiveCheck;
        }
    }
}

console.log(handleNetwork("SUCCESS"));
```

## Tushuntirish va Mantiq:
Agar NetworkState ga yangi qiymat qo'shilsa va switch da unutilsa, TypeScript `_exhaustiveCheck: never = state` satrida qat'iy kompilyatsiya xatosi beradi.

## Ishlash natijasi:
```text
Muvaffaqiyatli yakunlandi!
```


# 709-Topshiriq: keyof operatori - Kalitlar birlashmasi

## Topshiriq sharti:
Foydalanuvchi interfeysining kalitlaridan iborat union tip yasang.

## Yechim (JS yoki TS kodi):
```typescript
interface Car {
    brand: string;
    model: string;
    year: number;
}

type CarKey = keyof Car; // "brand" | "model" | "year"

const validKey: CarKey = "brand";
console.log("Tanlangan kalit:", validKey);
```

## Tushuntirish va Mantiq:
keyof Car berilgan Car tipining barcha ochiq kalitlari nomlarini literal stringlar birlashmasi ('brand' | 'model' | 'year') sifatida qaytaradi.

## Ishlash natijasi:
```text
Tanlangan kalit: brand
```


# 710-Topshiriq: typeof operatori tiplar olamida

## Topshiriq sharti:
Mavjud obyekt konstantasidan uning tipini typeof orqali chiqarib oling.

## Yechim (JS yoki TS kodi):
```typescript
const defaultSystemConfig = {
    host: "127.0.0.1",
    port: 8080,
    secure: false,
    tags: ["system", "core"]
};

type AppConfigType = typeof defaultSystemConfig;

const customConfig: AppConfigType = {
    host: "api.mycloud.uz",
    port: 443,
    secure: true,
    tags: ["production"]
};

console.log(`Xost: ${customConfig.host}, Port: ${customConfig.port}`);
```

## Tushuntirish va Mantiq:
TypeScript da 'typeof' o'zgaruvchi yoki konstanta ustiga qo'yilsa, uning strukturasidan avtomatik tip hosil qiladi.

## Ishlash natijasi:
```text
Xost: api.mycloud.uz, Port: 443
```


# 711-Topshiriq: keyof typeof birikmasi

## Topshiriq sharti:
Konstanta obyektining barcha kalitlari unionini olish.

## Yechim (JS yoki TS kodi):
```typescript
const COLORS = {
    PRIMARY: "#007bff",
    SUCCESS: "#28a745",
    DANGER: "#dc3545"
} as const;

type ColorKey = keyof typeof COLORS; // "PRIMARY" | "SUCCESS" | "DANGER"
type ColorValue = typeof COLORS[ColorKey]; // "#007bff" | "#28a745" | "#dc3545"

const selectedColor: ColorValue = COLORS.SUCCESS;
console.log("Tanlangan rang kodi:", selectedColor);
```

## Tushuntirish va Mantiq:
keyof typeof obyekt kalitlarini, typeof obj[keyof typeof obj] esa obyekt qiymatlarini literal tiplar sifatida ajratib olish imkonini beradi.

## Ishlash natijasi:
```text
Tanlangan rang kodi: #28a745
```


# 712-Topshiriq: Indexed Access Types (Indekslangan kirish tiplari)

## Topshiriq sharti:
Murakkab obyekt ichidagi aniq bir xossaning tipini T['key'] orqali ajratib oling.

## Yechim (JS yoki TS kodi):
```typescript
interface UserProfile {
    id: number;
    personal: {
        firstName: string;
        lastName: string;
        contacts: {
            email: string;
            phone: string;
        };
    };
}

type ContactInfo = UserProfile["personal"]["contacts"];

const contact: ContactInfo = {
    email: "alisher@uzbek.dev",
    phone: "+998712000000"
};

console.log("Aloqa:", contact.email);
```

## Tushuntirish va Mantiq:
UserProfile['personal']['contacts'] sintaksisi murakkab ichki tiplarni alohida e'lon qilmasdan to'g'ridan-to'g'ri o'qib olish imkonini beradi.

## Ishlash natijasi:
```text
Aloqa: alisher@uzbek.dev
```


# 713-Topshiriq: Tuple elementlarini Indexed Access orqali olish (T[number])

## Topshiriq sharti:
Massiv yoki tupledagi barcha mumkin bo'lgan elementlar tipini chiqarish.

## Yechim (JS yoki TS kodi):
```typescript
const roles = ["admin", "editor", "viewer"] as const;
type Role = typeof roles[number]; // "admin" | "editor" | "viewer"

const userRole: Role = "editor";
console.log("Foydalanuvchi roli:", userRole);
```

## Tushuntirish va Mantiq:
typeof roles[number] massivning raqamli indeksi bo'yicha qiymatlarini yig'ib, literal union tipga aylantiradi.

## Ishlash natijasi:
```text
Foydalanuvchi roli: editor
```


# 714-Topshiriq: Mapped Types asoslari

## Topshiriq sharti:
Interfeysdagi barcha maydonlarni boolean tipiga o'zgartiruvchi Mapped Type yarating.

## Yechim (JS yoki TS kodi):
```typescript
interface FeatureFlags {
    darkMode: boolean;
    betaFeatures: boolean;
    analytics: boolean;
}

type FlagsActive<T> = {
    [K in keyof T]: boolean;
};

interface AppSettings {
    theme: string;
    retries: number;
}

const statusCheck: FlagsActive<AppSettings> = {
    theme: true,
    retries: false
};

console.log("Sozlamalar holati:", statusCheck);
```

## Tushuntirish va Mantiq:
[K in keyof T] sintaksisi T tipidagi har bir kalit bo'yicha aylanib chiqib, yangi tip strukturasini hosil qiladi.

## Ishlash natijasi:
```text
Sozlamalar holati: { theme: true, retries: false }
```


# 715-Topshiriq: Mapped Types: -readonly modifikatori

## Topshiriq sharti:
Obyektdagi barcha readonly xossalarni o'zgaruvchan (mutable) qilish.

## Yechim (JS yoki TS kodi):
```typescript
interface ImmutableUser {
    readonly id: number;
    readonly username: string;
}

type Mutable<T> = {
    -readonly [K in keyof T]: T[K];
};

const user: Mutable<ImmutableUser> = { id: 1, username: "akmal" };
user.username = "akmal_yangi";

console.log("O'zgartirilgan ism:", user.username);
```

## Tushuntirish va Mantiq:
-readonly prefiksi kalitdan readonly cheklovini olib tashlaydi va uni oddiy o'zgartiriladigan xossaga aylantiradi.

## Ishlash natijasi:
```text
O'zgartirilgan ism: akmal_yangi
```


# 716-Topshiriq: Mapped Types: -? modifikatori (Required)

## Topshiriq sharti:
Barcha ixtiyoriy (?) maydonlarni majburiy holatga keltiruvchi maxsus Concrete turi.

## Yechim (JS yoki TS kodi):
```typescript
interface OptionalConfig {
    host?: string;
    port?: number;
    timeout?: number;
}

type Concrete<T> = {
    [K in keyof T]-?: T[K];
};

const finalConfig: Concrete<OptionalConfig> = {
    host: "localhost",
    port: 3000,
    timeout: 5000
};

console.log("Majburiy port:", finalConfig.port);
```

## Tushuntirish va Mantiq:
-? modifikatori barcha ixtiyoriy xossalardagi ? belgisini olib tashlaydi, bu TypeScript dagi o'rnatilgan Required<T> ga teng.

## Ishlash natijasi:
```text
Majburiy port: 3000
```


# 717-Topshiriq: Key Remapping in Mapped Types (as kalit so'zi)

## Topshiriq sharti:
Har bir maydon uchun getX() nomli getterlar interfeysini avtomatik yasash.

## Yechim (JS yoki TS kodi):
```typescript
interface Person {
    name: string;
    age: number;
}

type Getters<T> = {
    [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

const personService: Getters<Person> = {
    getName: () => "Nodir",
    getAge: () => 25
};

console.log(`Ism: ${personService.getName()}, Yoshi: ${personService.getAge()}`);
```

## Tushuntirish va Mantiq:
[K in keyof T as `get${Capitalize<string & K>}`] sintaksisi kalit nomini yangi shablon asosida o'zgartiradi (Key Remapping).

## Ishlash natijasi:
```text
Ism: Nodir, Yoshi: 25
```


# 718-Topshiriq: Key Remapping bilan kalitlarni filtrlash (never bilan)

## Topshiriq sharti:
Faqat string tipidagi maydonlarni ajratib oluvchi Mapped Type yarating.

## Yechim (JS yoki TS kodi):
```typescript
interface MixedData {
    id: number;
    title: string;
    active: boolean;
    description: string;
}

type OnlyStringKeys<T> = {
    [K in keyof T as T[K] extends string ? K : never]: T[K];
};

type StringOnly = OnlyStringKeys<MixedData>; // { title: string; description: string; }

const textData: StringOnly = {
    title: "Mavzu",
    description: "Batafsil ma'lumot"
};

console.log("Matnli ma'lumot:", textData);
```

## Tushuntirish va Mantiq:
as shartida 'never' qaytarilsa, o'sha kalit yangi generatsiya qilingan tipdan butunlay olib tashlanadi.

## Ishlash natijasi:
```text
Matnli ma'lumot: { title: 'Mavzu', description: 'Batafsil ma\'lumot' }
```


# 719-Topshiriq: Shartli Tiplar (Conditional Types) - Kirish

## Topshiriq sharti:
Agar tip boolean bo'lsa 'HA_YOQ', aks holda 'BOSHQA' literalini qaytaruvchi IsBoolean tipini yozing.

## Yechim (JS yoki TS kodi):
```typescript
type IsBoolean<T> = T extends boolean ? "HA_YOQ" : "BOSHQA";

type T1 = IsBoolean<true>;     // "HA_YOQ"
type T2 = IsBoolean<string>;   // "BOSHQA"

const v1: T1 = "HA_YOQ";
const v2: T2 = "BOSHQA";

console.log(`T1: ${v1}, T2: ${v2}`);
```

## Tushuntirish va Mantiq:
T extends U ? X : Y sintaksisi tiplar darajasidagi ternary operator (uchlik shart) bo'lib, T ning U ga mosligiga qarab boshqa tip tanlaydi.

## Ishlash natijasi:
```text
T1: HA_YOQ, T2: BOSHQA
```


# 720-Topshiriq: Distributive Conditional Types

## Topshiriq sharti:
Union tip berilganda shartli tip har bir elementga alohida qo'llanishini namoyish qiling.

## Yechim (JS yoki TS kodi):
```typescript
type ToArray<T> = T extends any ? T[] : never;

type StrOrNumArr = ToArray<string | number>; // string[] | number[]

const sArr: StrOrNumArr = ["A", "B"];
const nArr: StrOrNumArr = [1, 2, 3];

console.log("Massivlar muvaffaqiyatli tiplandi.");
```

## Tushuntirish va Mantiq:
Agar shartli tip generic parametri bevosita yalang'och (naked) T bo'lsa, u union a'zolariga avtomatik tarqaladi (distribute bo'ladi). Shunda ToArray<A | B> => ToArray<A> | ToArray<B>.

## Ishlash natijasi:
```text
Massivlar muvaffaqiyatli tiplandi.
```


# 721-Topshiriq: Distributivity ni to'xtatish ([T] sintaksisi)

## Topshiriq sharti:
Union tip berilganda ham uni bo'lib yubormasdan yaxlit massiv (string | number)[] yasash.

## Yechim (JS yoki TS kodi):
```typescript
type ToNonDistributiveArray<T> = [T] extends [any] ? T[] : never;

type CombinedArray = ToNonDistributiveArray<string | number>; // (string | number)[]

const mixed: CombinedArray = ["Salom", 42, "Dunyo"];
console.log("Aralash massiv:", mixed);
```

## Tushuntirish va Mantiq:
[T] extends [any] ko'rinishida kvadrat qavsga o'ralganda, TypeScript tarqalishni (distribution) to'xtatadi va butun unionni yagona tip sifatida ko'radi.

## Ishlash natijasi:
```text
Aralash massiv: [ 'Salom', 42, 'Dunyo' ]
```


# 722-Topshiriq: infer kalit so'zi bilan Shartli Tipda tipni chiqarib olish

## Topshiriq sharti:
Massiv ichidagi element turini infer orqali ajratib oluvchi ElementType tipini yozing.

## Yechim (JS yoki TS kodi):
```typescript
type ElementType<T> = T extends (infer U)[] ? U : T;

type Nums = ElementType<number[]>; // number
type Single = ElementType<string>;   // string

const n: Nums = 123;
const s: Single = "Matn";

console.log(`Nums: ${typeof n}, Single: ${typeof s}`);
```

## Tushuntirish va Mantiq:
infer U shartli tip ichida yangi tip o'zgaruvchisini joriy qiladi va TypeScript uni kiruvchi ma'lumotdan avtomatik hisoblab chiqaradi.

## Ishlash natijasi:
```text
Nums: number, Single: string
```


# 723-Topshiriq: infer yordamida funksiyaning qaytish tipini aniqlash

## Topshiriq sharti:
O'zingizning MyReturnType tipingizni infer bilan yozing.

## Yechim (JS yoki TS kodi):
```typescript
type MyReturnType<T> = T extends (...args: any[]) => infer R ? R : never;

function getUser() {
    return { id: 10, name: "Sanjar" };
}

type UserResult = MyReturnType<typeof getUser>;

const user: UserResult = { id: 10, name: "Sanjar" };
console.log(`Foydalanuvchi: ${user.name}`);
```

## Tushuntirish va Mantiq:
T extends (...args: any[]) => infer R ifodasi funksiyaning natijasini R deb belgilab, o'sha R ni qaytaradi. Bu TypeScript ning o'rnatilgan ReturnType utility tipining ishlash mexanizmidir.

## Ishlash natijasi:
```text
Foydalanuvchi: Sanjar
```


# 724-Topshiriq: infer yordamida funksiya parametrlarini aniqlash

## Topshiriq sharti:
Funksiya parametrlarini tuple sifatida ajratib oluvchi MyParameters turini yozing.

## Yechim (JS yoki TS kodi):
```typescript
type MyParameters<T> = T extends (...args: infer P) => any ? P : never;

function saveSettings(key: string, value: number, isPermanent: boolean): void {}

type SaveParams = MyParameters<typeof saveSettings>; // [string, number, boolean]

const testParams: SaveParams = ["theme", 1, true];
console.log("Parametrlar:", testParams);
```

## Tushuntirish va Mantiq:
infer P rest parametrlari o'rniga qo'yilganda barcha argumentlar tiplari tartiblangan tuple sifatida olinadi.

## Ishlash natijasi:
```text
Parametrlar: [ 'theme', 1, true ]
```


# 725-Topshiriq: infer yordamida Promise ichidagi tipni ajratish

## Topshiriq sharti:
Promise<T> ichidagi T tipini sug'urib oluvchi MyAwaited turini yozing.

## Yechim (JS yoki TS kodi):
```typescript
type MyAwaited<T> = T extends Promise<infer U> ? MyAwaited<U> : T;

type Resolved1 = MyAwaited<Promise<string>>;         // string
type Resolved2 = MyAwaited<Promise<Promise<number>>>; // number (rekursiv)

const val: Resolved1 = "Tayyor natija";
console.log(val);
```

## Tushuntirish va Mantiq:
Rekursiv MyAwaited<U> Promise ichma-ich o'ralgan bo'lsa ham uning eng tubidagi haqiqiy qiymat tipini topib beradi.

## Ishlash natijasi:
```text
Tayyor natija
```


# 726-Topshiriq: Template Literal Types - Matnli andozalar

## Topshiriq sharti:
Hodisa nomi va harakat turini birlashtiruvchi andozali satr tipini tuzing.

## Yechim (JS yoki TS kodi):
```typescript
type Scope = "user" | "order" | "invoice";
type Action = "created" | "updated" | "deleted";

type AuditEvent = `${Scope}:${Action}`;

const ev1: AuditEvent = "user:created";
const ev2: AuditEvent = "order:updated";

console.log("Hodisa 1:", ev1);
console.log("Hodisa 2:", ev2);
```

## Tushuntirish va Mantiq:
Template literal types (`${Scope}:${Action}`) ikkita union a'zolarini ko'paytirib, jami 9 ta kombinatsiyadan iborat qat'iy tiplar to'plamini hosil qiladi.

## Ishlash natijasi:
```text
Hodisa 1: user:created
Hodisa 2: order:updated
```


# 727-Topshiriq: String manipulyatsiya tiplari (Uppercase, Lowercase, Capitalize)

## Topshiriq sharti:
TypeScript ning o'rnatilgan satr modifikatorlari bilan ishlash.

## Yechim (JS yoki TS kodi):
```typescript
type Greeting = "salom dunyo";

type Loud = Uppercase<Greeting>;       // "SALOM DUNYO"
type Quiet = Lowercase<Loud>;           // "salom dunyo"
type TitleCase = Capitalize<Greeting>;  // "Salom dunyo"

const l: Loud = "SALOM DUNYO";
const t: TitleCase = "Salom dunyo";

console.log(`${l} | ${t}`);
```

## Tushuntirish va Mantiq:
Uppercase, Lowercase, Capitalize, Uncapitalize kabi ichki tiplar satr literal tiplarini kompilyatsiya darajasida o'zgartiradi.

## Ishlash natijasi:
```text
SALOM DUNYO | Salom dunyo
```


# 728-Topshiriq: Template Literal Types bilan CSS xossalari tiplash

## Topshiriq sharti:
Padding yoki margin qiymatlari uchun px va rem birliklarini talab qiluvchi o'lcham tipini yozing.

## Yechim (JS yoki TS kodi):
```typescript
type CssUnit = "px" | "rem" | "%";
type CssValue = `${number}${CssUnit}` | "auto";

function setMargin(val: CssValue) {
    console.log(`Margin o'rnatildi: ${val}`);
}

setMargin("16px");
setMargin("2.5rem");
setMargin("auto");
```

## Tushuntirish va Mantiq:
`${number}${CssUnit}` sintaksisi oldida ixtiyoriy son va orqasidan ruxsat etilgan birlik kelishini qat'iy tekshiradi.

## Ishlash natijasi:
```text
Margin o'rnatildi: 16px
Margin o'rnatildi: 2.5rem
Margin o'rnatildi: auto
```


# 729-Topshiriq: Recursive Flatten turi

## Topshiriq sharti:
Ixtiyoriy chuqurlikdagi massivlarni bitta darajali yassi massiv tipiga aylantiruvchi Flatten tipini yozing.

## Yechim (JS yoki TS kodi):
```typescript
type Flatten<T> = T extends (infer U)[] ? Flatten<U> : T;

type NestedArray = number[][][];
type Flat = Flatten<NestedArray>; // number

const singleNum: Flat = 42;
console.log("Yassi element tipi:", typeof singleNum);
```

## Tushuntirish va Mantiq:
Rekursiv Flatten shartli turi massiv ichida massiv qolmaguniga qadar infer U bilan ochib boradi.

## Ishlash natijasi:
```text
Yassi element tipi: number
```


# 730-Topshiriq: Brand Types (Nominal Typing) - Kirish

## Topshiriq sharti:
Primitive string va number larni tasodifiy chalkashtirib yubormaslik uchun maxsus Brand (tamg'a) tipini yarating.

## Yechim (JS yoki TS kodi):
```typescript
type Brand<K, T> = K & { readonly __brand: T };

type UserId = Brand<number, "UserId">;
type OrderId = Brand<number, "OrderId">;

function createUserId(id: number): UserId {
    return id as UserId;
}

function createOrderId(id: number): OrderId {
    return id as OrderId;
}

const uId = createUserId(101);
const oId = createOrderId(5001);

function shipOrder(userId: UserId, orderId: OrderId) {
    console.log(`Foydalanuvchi #${userId} uchun Buyurtma #${orderId} jo'natildi.`);
}

shipOrder(uId, oId);
```

## Tushuntirish va Mantiq:
TypeScript strukturaviy tiplash tizimiga ega bo'lgani uchun barcha sonlarni bir xil deb biladi. Brand Types yordamida UserId va OrderId larni bir-biriga noo'rin berib yuborishning oldi olinadi.

## Ishlash natijasi:
```text
Foydalanuvchi #101 uchun Buyurtma #5001 jo'natildi.
```


# 731-Topshiriq: Valyutalar xavfsizligi uchun Brand Types

## Topshiriq sharti:
USD va EUR valyutalarini bir-biriga noto'g'ri qo'shib yubormaslik uchun brendlash.

## Yechim (JS yoki TS kodi):
```typescript
type USD = number & { readonly __currency: "USD" };
type EUR = number & { readonly __currency: "EUR" };

const makeUSD = (n: number) => n as USD;
const makeEUR = (n: number) => n as EUR;

function payInUSD(amount: USD) {
    console.log(`To'lov: $${amount}`);
}

const myDollars = makeUSD(150);
payInUSD(myDollars);
```

## Tushuntirish va Mantiq:
Brand Types dasturda hisob-kitob xatolarini (masalan, valyutalarni konvertatsiyasiz aralashtirib yuborish) kompilyator tekshiruvidayoq to'xtatadi.

## Ishlash natijasi:
```text
To'lov: $150
```


# 732-Topshiriq: satisfies operatori (TS 4.9+) - Asosiy vazifasi

## Topshiriq sharti:
Obyektning berilgan tipga mosligini tekshirib, lekin uning aniq literal tiplarini yo'qotmaslik.

## Yechim (JS yoki TS kodi):
```typescript
type RGB = [red: number, green: number, blue: number];
type Color = string | RGB;

const palette = {
    primary: "red",
    secondary: [0, 255, 0],
} satisfies Record<string, Color>;

// palette.primary ning satr ekanligi aniq saqlanib qolgan
console.log("Katta harfda:", palette.primary.toUpperCase());
// palette.secondary ning massiv ekanligi saqlangan
console.log("Yashil kanal:", palette.secondary[1]);
```

## Tushuntirish va Mantiq:
`satisfies` operatori obyektni Record<string, Color> ga mosligini tasdiqlaydi, lekin ': Record<string, Color>' kabi kengaytirib (widen qilib) yubormaydi, natijada .toUpperCase() xatosiz ishlaydi.

## Ishlash natijasi:
```text
Katta harfda: RED
Yashil kanal: 255
```


# 733-Topshiriq: satisfies bilan xossalarni qat'iy tekshirish

## Topshiriq sharti:
Konfiguratsiyada imlo xatoliklarini aniqlash va aniq xossalarni saqlab qolish.

## Yechim (JS yoki TS kodi):
```typescript
type RouteConfig = {
    path: string;
    authRequired: boolean;
};

const routes = {
    home: { path: "/", authRequired: false },
    dashboard: { path: "/dashboard", authRequired: true }
} satisfies Record<string, RouteConfig>;

console.log("Dashboard yo'li:", routes.dashboard.path);
```

## Tushuntirish va Mantiq:
satisfies orqali routes.dashboard to'liq taniladi va avtoto'ldirishda routes.profile kabi yo'q xossalar chiqmaydi.

## Ishlash natijasi:
```text
Dashboard yo'li: /dashboard
```


# 734-Topshiriq: DeepPartial rekursiv turi

## Topshiriq sharti:
Obyektning barcha ichma-ich xossalarini ixtiyoriy (?) qiluvchi DeepPartial tipini yarating.

## Yechim (JS yoki TS kodi):
```typescript
type DeepPartial<T> = {
    [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

interface ComplexSettings {
    database: {
        host: string;
        credentials: {
            user: string;
            pass: string;
        };
    };
}

const partialUpdate: DeepPartial<ComplexSettings> = {
    database: {
        credentials: {
            user: "super_admin"
        }
    }
};

console.log("Qisman yangilanish:", partialUpdate.database?.credentials?.user);
```

## Tushuntirish va Mantiq:
DeepPartial rekursiv mapped type bo'lib, eng chuqur obyekt ichidagi xossalarni ham xavfsiz qisman yangilash imkonini beradi.

## Ishlash natijasi:
```text
Qisman yangilanish: super_admin
```


# 735-Topshiriq: DeepRequired rekursiv turi

## Topshiriq sharti:
Barcha ichma-ich ixtiyoriy maydonlarni majburiy qiluvchi DeepRequired turi.

## Yechim (JS yoki TS kodi):
```typescript
type DeepRequired<T> = {
    [P in keyof T]-?: T[P] extends object ? DeepRequired<T[P]> : T[P];
};

interface ConfigDraft {
    server?: {
        port?: number;
    };
}

const readyConfig: DeepRequired<ConfigDraft> = {
    server: {
        port: 8080
    }
};

console.log("Tayyor port:", readyConfig.server.port);
```

## Tushuntirish va Mantiq:
DeepRequired har bir qatlamdagi -? modifikatori yordamida to'liq to'ldirilgan obyekt tuzilishini talab qiladi.

## Ishlash natijasi:
```text
Tayyor port: 8080
```


# 736-Topshiriq: Tuple uzunligini tip darajasida hisoblash

## Topshiriq sharti:
Tuple tipining length xossasi orqali uning elementlar sonini literal raqam sifatida olish.

## Yechim (JS yoki TS kodi):
```typescript
type Length<T extends any[]> = T["length"];

type ThreeItems = Length<["A", "B", "C"]>; // 3
type ZeroItems = Length<[]>;              // 0

const count: ThreeItems = 3;
console.log("Elementlar soni:", count);
```

## Tushuntirish va Mantiq:
Tuple tiplarida 'length' xossasi oddiy number emas, balki qat'iy sonli literal tip (masalan, 3) bo'ladi.

## Ishlash natijasi:
```text
Elementlar soni: 3
```


# 737-Topshiriq: Tuple boshini ajratish (Head va Tail infer)

## Topshiriq sharti:
Tuple ning birinchi elementi va qolgan qismini infer orqali ajratuvchi tiplar yozing.

## Yechim (JS yoki TS kodi):
```typescript
type Head<T extends any[]> = T extends [infer H, ...any[]] ? H : never;
type Tail<T extends any[]> = T extends [any, ...infer Rest] ? Rest : [];

type MyTuple = [string, number, boolean];
type First = Head<MyTuple>; // string
type Others = Tail<MyTuple>; // [number, boolean]

const f: First = "Bosh element";
const o: Others = [100, true];

console.log(f, o);
```

## Tushuntirish va Mantiq:
infer H va ...infer Rest sintaksisi massivlarni destrukturizatsiya qilish kabi tiplar darajasida qismlarga ajratish imkonini beradi.

## Ishlash natijasi:
```text
Bosh element [ 100, true ]
```


# 738-Topshiriq: Obyekt yo'lini nuqtali satr sifatida olish (Dot Notation Path)

## Topshiriq sharti:
Ichma-ich xossalarga kirish yo'llarini (masalan, 'user.address.city') template literal types bilan ifodalash.

## Yechim (JS yoki TS kodi):
```typescript
type Paths<T> = T extends object ? {
    [K in keyof T]: `${string & K}` | `${string & K}.${Paths<T[K]>}`
}[keyof T] : never;

interface Schema {
    user: {
        name: string;
        address: {
            city: string;
        };
    };
}

type ValidPath = Paths<Schema>;

const p1: ValidPath = "user";
const p2: ValidPath = "user.name";
const p3: ValidPath = "user.address.city";

console.log("To'g'ri yo'llar:", p1, p2, p3);
```

## Tushuntirish va Mantiq:
Paths<T> rekursiv shablon turi lodash get yoki form validation kutubxonalarida xavfsiz chuqur kalitlarni yozishda ishlatiladi.

## Ishlash natijasi:
```text
To'g'ri yo'llar: user user.name user.address.city
```


# 739-Topshiriq: Type Guard yordamida API xatoliklarini farqlash

## Topshiriq sharti:
Serverdan kelgan javob Oddiy xatolikmi yoki Validatsiya xatoligimi ekanini tekshiruvchi guard.

## Yechim (JS yoki TS kodi):
```typescript
interface SimpleError {
    message: string;
}

interface ValidationError {
    message: string;
    fields: Record<string, string[]>;
}

function isValidationError(err: SimpleError | ValidationError): err is ValidationError {
    return "fields" in err;
}

function handleErr(err: SimpleError | ValidationError) {
    if (isValidationError(err)) {
        console.log("Maydon xatolari:", Object.keys(err.fields));
    } else {
        console.log("Umumiy xato:", err.message);
    }
}

handleErr({ message: "Xato", fields: { email: ["Noto'g'ri format"] } });
```

## Tushuntirish va Mantiq:
Dastur davomida murakkab xato tuzilmalarini to'g'ri ushlab qayta ishlash uchun type guardlar eng toza yechimdir.

## Ishlash natijasi:
```text
Maydon xatolari: [ 'email' ]
```


# 740-Topshiriq: Opaque Types yordamida parollarni himoyalash

## Topshiriq sharti:
Oddiy string bilan shifrlangan yoki toza parolni aralashtirib yubormaslik.

## Yechim (JS yoki TS kodi):
```typescript
type HashedPassword = string & { readonly __type: unique symbol };

function hashPassword(plain: string): HashedPassword {
    return `sha256_${plain}_secret` as HashedPassword;
}

function saveToDatabase(login: string, pass: HashedPassword) {
    console.log(`Foydalanuvchi ${login} saqlandi, hash: ${pass}`);
}

const pwd = hashPassword("maxfiy123");
saveToDatabase("alisher", pwd);
```

## Tushuntirish va Mantiq:
unique symbol bilan brand yaratilganda, boshqa fayldan uni soxtalashtirish (spoofing) imkonsiz bo'ladi.

## Ishlash natijasi:
```text
Foydalanuvchi alisher saqlandi, hash: sha256_maxfiy123_secret
```


# 741-Topshiriq: Literal Type Narrowing bilan Oddiy Holat Mashinasi (FSM)

## Topshiriq sharti:
Cheklangan holatlar va o'tishlarni qat'iy tiplash.

## Yechim (JS yoki TS kodi):
```typescript
type MachineState =
    | { status: "IDLE" }
    | { status: "PENDING"; startedAt: number }
    | { status: "COMPLETED"; result: string };

function renderMachine(state: MachineState): string {
    switch (state.status) {
        case "IDLE": return "Tizim bo'sh turibdi";
        case "PENDING": return `Ishlamoqda: ${state.startedAt}`;
        case "COMPLETED": return `Natija: ${state.result}`;
    }
}

console.log(renderMachine({ status: "COMPLETED", result: "OK" }));
```

## Tushuntirish va Mantiq:
Har bir holatga faqat o'sha holat uchun xos ma'lumotlar biriktiriladi (masalan, result faqat COMPLETED da bor).

## Ishlash natijasi:
```text
Natija: OK
```


# 742-Topshiriq: Const Type Parameters (TypeScript 5.0+)

## Topshiriq sharti:
Funksiya chaqirilganda 'as const' yozmasdan avtomatik literal tipni ushlab qolish.

## Yechim (JS yoki TS kodi):
```typescript
function createRoutes<const T extends readonly string[]>(routes: T): T {
    return routes;
}

const r = createRoutes(["/home", "/about", "/contact"]);
// r ning tipi string[] emas, readonly ["/home", "/about", "/contact"]
console.log("Yo'nalishlar:", r);
```

## Tushuntirish va Mantiq:
<const T> sintaksisi TypeScript 5.0 da kiritilgan bo'lib, funksiyaga uzatilgan massiv va obyektlarni avtomatik readonly literal sifatida taniydi.

## Ishlash natijasi:
```text
Yo'nalishlar: [ '/home', '/about', '/contact' ]
```


# 743-Topshiriq: Shartli tiplarda Union qismlarini chiqarib tashlash (Exclude qolipi)

## Topshiriq sharti:
T extends U ? never : T mantiqini qo'lda amalga oshirish.

## Yechim (JS yoki TS kodi):
```typescript
type CustomExclude<T, U> = T extends U ? never : T;

type Available = "read" | "write" | "delete" | "execute";
type SafePermissions = CustomExclude<Available, "delete">; // "read" | "write" | "execute"

const p: SafePermissions = "write";
console.log("Xavfsiz ruxsat:", p);
```

## Tushuntirish va Mantiq:
Tarqalish (distribution) tufayli 'delete' o'z o'rnida never ga aylanadi va birlashmadan avtomatik tushib qoladi.

## Ishlash natijasi:
```text
Xavfsiz ruxsat: write
```


# 744-Topshiriq: Shartli tiplarda Umumiy qismlarni ajratish (Extract qolipi)

## Topshiriq sharti:
T extends U ? T : never orqali umumiy a'zolarni olish.

## Yechim (JS yoki TS kodi):
```typescript
type CustomExtract<T, U> = T extends U ? T : never;

type ActionTypes = "click" | "hover" | "scroll" | 100 | 200;
type StringActions = CustomExtract<ActionTypes, string>; // "click" | "hover" | "scroll"

const act: StringActions = "click";
console.log("Satrli amal:", act);
```

## Tushuntirish va Mantiq:
Faqat berilgan U tipiga mos tushuvchi elementlargina qoldiriladi.

## Ishlash natijasi:
```text
Satrli amal: click
```


# 745-Topshiriq: NonNullable qo'lda amalga oshirish

## Topshiriq sharti:
T dan null va undefined ni tozalovchi shartli tip.

## Yechim (JS yoki TS kodi):
```typescript
type CustomNonNullable<T> = T extends null | undefined ? never : T;

type RawInput = string | number | null | undefined;
type ValidInput = CustomNonNullable<RawInput>; // string | number

const inp: ValidInput = "Ma'lumot mavjud";
console.log("Tozalangan kirish:", inp);
```

## Tushuntirish va Mantiq:
null | undefined tekshiruvidan o'tmagan qismlar never ga aylanadi va faqat yaroqli tiplar qoladi.

## Ishlash natijasi:
```text
Tozalangan kirish: Ma'lumot mavjud
```


# 746-Topshiriq: Tuple ni Teskari qilish (Reverse Tuple)

## Topshiriq sharti:
Rekursiv infer yordamida tuple elementlari tartibini teskari qilish.

## Yechim (JS yoki TS kodi):
```typescript
type Reverse<T extends any[]> = T extends [infer First, ...infer Rest]
    ? [...Reverse<Rest>, First]
    : [];

type Normal = [number, string, boolean];
type Inverted = Reverse<Normal>; // [boolean, string, number]

const inv: Inverted = [true, "salom", 99];
console.log("Teskari tuple:", inv);
```

## Tushuntirish va Mantiq:
Rekursiv shartli tiplar dasturlashdagi oddiy rekursiya kabi ishlaydi: boshidagi elementni sug'urib, qolganini yana o'ziga uzatadi.

## Ishlash natijasi:
```text
Teskari tuple: [ true, 'salom', 99 ]
```


# 747-Topshiriq: Obyekt qiymatlari bo'yicha filtrlash

## Topshiriq sharti:
Faqat funksiya bo'lgan metodlarni ajratuvchi FunctionPropertyNames tipi.

## Yechim (JS yoki TS kodi):
```typescript
interface DocumentService {
    title: string;
    pages: number;
    print(): void;
    exportPdf(): boolean;
}

type FunctionPropertyNames<T> = {
    [K in keyof T]: T[K] extends (...args: any[]) => any ? K : never;
}[keyof T];

type DocumentMethods = FunctionPropertyNames<DocumentService>; // "print" | "exportPdf"

const method: DocumentMethods = "print";
console.log("Tanlangan metod:", method);
```

## Tushuntirish va Mantiq:
T[K] extends Function tekshiruvi orqali faqat metodlar kalitlarini ajratib oluvchi kuchli pattern.

## Ishlash natijasi:
```text
Tanlangan metod: print
```


# 748-Topshiriq: Deep Readonly massivlar bilan birga

## Topshiriq sharti:
Massivlarni ham readonly ga aylantiruvchi mukammal DeepReadonly.

## Yechim (JS yoki TS kodi):
```typescript
type DeepReadonlyFull<T> = T extends (infer U)[]
    ? ReadonlyArray<DeepReadonlyFull<U>>
    : T extends object
    ? { readonly [K in keyof T]: DeepReadonlyFull<T[K]> }
    : T;

const systemData: DeepReadonlyFull<{ tags: string[]; meta: { id: number } }> = {
    tags: ["prod", "db"],
    meta: { id: 7 }
};

console.log("Tizim tegi:", systemData.tags[0]);
```

## Tushuntirish va Mantiq:
Massivlar uchun ReadonlyArray<U> ga o'tkazish push/pop kabi o'zgartirishlarni to'liq bloklaydi.

## Ishlash natijasi:
```text
Tizim tegi: prod
```


# 749-Topshiriq: Union To Intersection tushunchasi (Funksiya parametrlari kontravariantligi orqali)

## Topshiriq sharti:
Birlashma tipni kesishma tipga aylantiruvchi ilg'or shartli tip.

## Yechim (JS yoki TS kodi):
```typescript
type UnionToIntersection<U> =
    (U extends any ? (k: U) => void : never) extends ((k: infer I) => void) ? I : never;

type TUnion = { a: string } | { b: number };
type TIntersect = UnionToIntersection<TUnion>; // { a: string } & { b: number }

const combined: TIntersect = { a: "test", b: 100 };
console.log("Birlashgan obyekt:", combined.a, combined.b);
```

## Tushuntirish va Mantiq:
Funksiya parametrlari kontravariant bo'lganligi sababli, bir nechta funksiyalar birlashmasining parametri ularning kesishmasiga aylanadi.

## Ishlash natijasi:
```text
Birlashgan obyekt: test 100
```


# 750-Topshiriq: Tip darajasidagi Tuplega element qo'shish (Append / Prepend)

## Topshiriq sharti:
Tuple boshiga yoki oxiriga yangi tip elementini qo'shuvchi generik tiplar.

## Yechim (JS yoki TS kodi):
```typescript
type Push<T extends any[], V> = [...T, V];
type Unshift<T extends any[], V> = [V, ...T];

type BaseTuple = [number, string];
type Pushed = Push<BaseTuple, boolean>; // [number, string, boolean]
type Unshifted = Unshift<BaseTuple, symbol>; // [symbol, number, string]

const ex1: Pushed = [1, "salom", true];
console.log("Oxiriga qo'shilgan tuple:", ex1);
```

## Tushuntirish va Mantiq:
Spread operatori tuple tiplar ustida ham to'liq ishlaydi va yangi o'zgarmas tuple strukturalarini hosil qiladi.

## Ishlash natijasi:
```text
Oxiriga qo'shilgan tuple: [ 1, 'salom', true ]
```

