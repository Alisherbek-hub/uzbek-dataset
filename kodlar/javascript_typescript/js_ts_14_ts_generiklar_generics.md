# 651-Topshiriq: Generik funksiya - Kirish (Identity Function)

## Topshiriq sharti:
O'ziga uzatilgan har qanday tipdagi qiymatni aynan o'sha tipda qaytaruvchi identity funksiyasini generik yordamida yozing.

## Yechim (JS yoki TS kodi):
```typescript
function identity<T>(arg: T): T {
    return arg;
}

const strOutput = identity<string>("Salom Dunyo");
const numOutput = identity(42); // Type inference orqali T avtomatik number

console.log("Satr natija:", strOutput);
console.log("Son natija:", numOutput);
```

## Tushuntirish va Mantiq:
Generiklar (<T>) funksiyaga argument berilayotganda tipni parametr sifatida qabul qilish imkonini beradi. 'any' dan farqli o'laroq, kiruvchi va chiquvchi tiplar o'rtasidagi bog'liqlik to'liq saqlanib qoladi.

## Ishlash natijasi:
```text
Satr natija: Salom Dunyo
Son natija: 42
```


# 652-Topshiriq: Generik massivlar bilan ishlash

## Topshiriq sharti:
Har qanday tipdagi massivning birinchi elementini qaytaruvchi getFirstElement generik funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function getFirstElement<T>(arr: T[]): T | undefined {
    return arr.length > 0 ? arr[0] : undefined;
}

const nums = [100, 200, 300];
const names = ["Aziz", "Malika", "Jasur"];

console.log("Birinchi son:", getFirstElement(nums));
console.log("Birinchi ism:", getFirstElement(names));
```

## Tushuntirish va Mantiq:
arr: T[] (yoki Array<T>) sintaksisi berilgan massiv elementlari tipi T ekanini va funksiya T yoki undefined qaytarishini kafolatlaydi.

## Ishlash natijasi:
```text
Birinchi son: 100
Birinchi ism: Aziz
```


# 653-Topshiriq: Ikkita generik parametrli funksiya (Multiple Generics)

## Topshiriq sharti:
Ikkita har xil tipdagi qiymatni qabul qilib, ularni juftlik (tuple) sifatida qaytaruvchi makePair funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function makePair<T, U>(first: T, second: U): [T, U] {
    return [first, second];
}

const pair1 = makePair("Foydalanuvchi_ID", 10042);
const pair2 = makePair(true, ["ruxsat_1", "ruxsat_2"]);

console.log("Juftlik 1:", pair1);
console.log("Juftlik 2:", pair2);
```

## Tushuntirish va Mantiq:
<T, U> kabi bir nechta harflar orqali ikki yoki undan ortiq mustaqil tiplar parametr sifatida qabul qilinadi va tuple ko'rinishida qaytariladi.

## Ishlash natijasi:
```text
Juftlik 1: [ 'Foydalanuvchi_ID', 10042 ]
Juftlik 2: [ true, [ 'ruxsat_1', 'ruxsat_2' ] ]
```


# 654-Topshiriq: Generik Interfeys (Generic Interface)

## Topshiriq sharti:
Backenddan keladigan server javoblari uchun generik ApiResponse interfeysini e'lon qiling va unga mos obyekt yarating.

## Yechim (JS yoki TS kodi):
```typescript
interface ApiResponse<T> {
    status: number;
    success: boolean;
    data: T;
}

interface User {
    id: number;
    username: string;
}

const response: ApiResponse<User> = {
    status: 200,
    success: true,
    data: { id: 1, username: "admin_ali" }
};

console.log(`Foydalanuvchi: ${response.data.username}, Holat: ${response.status}`);
```

## Tushuntirish va Mantiq:
ApiResponse<T> interfeysi data maydonining tipini dinamik qilish imkonini beradi. Shunda User, Product yoki ro'yxat uchun alohida interfeyslar yozish shart bo'lmaydi.

## Ishlash natijasi:
```text
Foydalanuvchi: admin_ali, Holat: 200
```


# 655-Topshiriq: Generik Repository interfeysi

## Topshiriq sharti:
CRUD operatsiyalari uchun standart generik Repository interfeysini e'lon qiling va uni in-memory ro'yxat bilan amalga oshiring.

## Yechim (JS yoki TS kodi):
```typescript
interface Repository<T> {
    add(item: T): void;
    getAll(): T[];
}

interface Product {
    id: number;
    title: string;
}

class ProductRepository implements Repository<Product> {
    private items: Product[] = [];

    add(item: Product): void {
        this.items.push(item);
    }

    getAll(): Product[] {
        return this.items;
    }
}

const repo = new ProductRepository();
repo.add({ id: 101, title: "Noutbuk" });
console.log("Mahsulotlar:", repo.getAll());
```

## Tushuntirish va Mantiq:
Repository<T> dizayn namunasi turli ma'lumotlar modellari uchun yagona standart abstraksiya yaratishda generik interfeyslardan unumli foydalanadi.

## Ishlash natijasi:
```text
Mahsulotlar: [ { id: 101, title: 'Noutbuk' } ]
```


# 656-Topshiriq: Generik Sinf (Generic Class)

## Topshiriq sharti:
Ixtiyoriy tipdagi bitta qiymatni xavfsiz saqlovchi va oluvchi Box<T> generik sinfini yozing.

## Yechim (JS yoki TS kodi):
```typescript
class Box<T> {
    private content: T;

    constructor(initialContent: T) {
        this.content = initialContent;
    }

    getContent(): T {
        return this.content;
    }

    setContent(newContent: T): void {
        this.content = newContent;
    }
}

const stringBox = new Box<string>("Sirli matn");
console.log("Quti ichi:", stringBox.getContent());

const numberBox = new Box<number>(999);
console.log("Son quti ichi:", numberBox.getContent());
```

## Tushuntirish va Mantiq:
class Box<T> sinfi istalgan ma'lumot turi bilan ishlay oladi. Konstruktor orqali uzatilgan qiymatdan kelib chiqib, TS o'zgaruvchi tipini avtomatik taniydi.

## Ishlash natijasi:
```text
Quti ichi: Sirli matn
Son quti ichi: 999
```


# 657-Topshiriq: Generik Stack ma'lumotlar tuzilmasi

## Topshiriq sharti:
LIFO (Last In First Out) tamoyiliga asoslangan generik Stack sinfini yarating.

## Yechim (JS yoki TS kodi):
```typescript
class Stack<T> {
    private elements: T[] = [];

    push(item: T): void {
        this.elements.push(item);
    }

    pop(): T | undefined {
        return this.elements.pop();
    }

    size(): number {
        return this.elements.length;
    }
}

const numberStack = new Stack<number>();
numberStack.push(10);
numberStack.push(20);
console.log("Pop qilingan:", numberStack.pop());
console.log("Qolgan o'lcham:", numberStack.size());
```

## Tushuntirish va Mantiq:
Stack<T> har qanday ma'lumot turidagi elementlarni ketma-ket to'plash va oxirgisini chiqarib olishda to'liq tiplash xavfsizligini kafolatlaydi.

## Ishlash natijasi:
```text
Pop qilingan: 20
Qolgan o'lcham: 1
```


# 658-Topshiriq: Generik Queue (Navbat) ma'lumotlar tuzilmasi

## Topshiriq sharti:
FIFO (First In First Out) tamoyili bo'yicha ishlovchi generik Queue sinfini yarating.

## Yechim (JS yoki TS kodi):
```typescript
class Queue<T> {
    private items: T[] = [];

    enqueue(item: T): void {
        this.items.push(item);
    }

    dequeue(): T | undefined {
        return this.items.shift();
    }

    isEmpty(): boolean {
        return this.items.length === 0;
    }
}

const taskQueue = new Queue<string>();
taskQueue.enqueue("Vazifa_A");
taskQueue.enqueue("Vazifa_B");
console.log("Bajarilmoqda:", taskQueue.dequeue());
console.log("Navbat bo'shmi:", taskQueue.isEmpty());
```

## Tushuntirish va Mantiq:
Queue<T> navbati har qanday tipdagi topshiriqlarni bir xil tartibda boshqarish uchun generic tip xavfsizligidan foydalanadi.

## Ishlash natijasi:
```text
Bajarilmoqda: Vazifa_A
Navbat bo'shmi: false
```


# 659-Topshiriq: Generik cheklovlar (Generic Constraints - extends)

## Topshiriq sharti:
Parametr sifatida faqat .length xossasiga ega bo'lgan tiplarni qabul qiluvchi funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
interface HasLength {
    length: number;
}

function logLength<T extends HasLength>(item: T): T {
    console.log(`Element uzunligi: ${item.length}`);
    return item;
}

logLength("Salom TypeScript");
logLength([1, 2, 3, 4]);
logLength({ length: 42, title: "Kitob" });
```

## Tushuntirish va Mantiq:
T extends HasLength ifodasi T tipining kamida HasLength interfeysi talablariga javob berishini shart qilib qo'yadi. Agar length xossasi bo'lmagan tip (masalan, number) berilsa, kompilyator xato beradi.

## Ishlash natijasi:
```text
Element uzunligi: 16
Element uzunligi: 4
Element uzunligi: 42
```


# 660-Topshiriq: ID bo'yicha generik obyekt cheklovi

## Topshiriq sharti:
Har qanday id raqamiga ega obyektlar massividan qidiruvchi findEntityById funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
interface BaseEntity {
    id: number;
}

function findEntityById<T extends BaseEntity>(items: T[], id: number): T | undefined {
    return items.find(entity => entity.id === id);
}

const users = [{ id: 1, name: "Ali" }, { id: 2, name: "Vali" }];
const found = findEntityById(users, 2);
console.log("Topildi:", found?.name);
```

## Tushuntirish va Mantiq:
T extends BaseEntity cheklovi orqali funksiya kiruvchi obyektlarning boshqa har qanday xossalarini saqlab qolgan holda ularda id mavjudligiga tayanadi.

## Ishlash natijasi:
```text
Topildi: Vali
```


# 661-Topshiriq: keyof operatori bilan generik cheklov

## Topshiriq sharti:
Obyekt va uning kalitini qabul qilib, o'sha kalitdagi qiymatni qaytaruvchi getProperty funksiyasini tiplash.

## Yechim (JS yoki TS kodi):
```typescript
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
    return obj[key];
}

const car = { make: "Chevrolet", model: "Cobalt", year: 2024 };
const make = getProperty(car, "make");
const year = getProperty(car, "year");

console.log(`Avtomobil: ${make}, Yili: ${year}`);
```

## Tushuntirish va Mantiq:
K extends keyof T sintaksisi kalit faqat T obyektida mavjud bo'lgan xossalar bo'lishini talab qiladi, qaytish tipi esa T[K] (Indexed Access Type) bo'ladi.

## Ishlash natijasi:
```text
Avtomobil: Chevrolet, Yili: 2024
```


# 662-Topshiriq: Obyekt xossasini yangilovchi generik funksiya

## Topshiriq sharti:
Obyekt, uning kaliti va faqat o'sha kalit tipiga mos keluvchi yangi qiymatni qabul qiluvchi setProperty funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function setProperty<T, K extends keyof T>(obj: T, key: K, value: T[K]): void {
    obj[key] = value;
}

const settings = { theme: "dark", autoSave: true, maxTabs: 10 };
setProperty(settings, "theme", "light");
setProperty(settings, "maxTabs", 15);

console.log("Yangilangan sozlamalar:", settings);
```

## Tushuntirish va Mantiq:
value parametriga T[K] tipi berilishi sababli, agar theme kalitiga boolean yoki son berishga urinilsa, kompilyator xato ko'rsatadi.

## Ishlash natijasi:
```text
Yangilangan sozlamalar: { theme: 'light', autoSave: true, maxTabs: 15 }
```


# 663-Topshiriq: Sukut bo'yicha beriladigan generik tiplar (Default Generic Types)

## Topshiriq sharti:
Agar tip belgilanmasa string deb hisoblaydigan Container generik sinfini e'lon qiling.

## Yechim (JS yoki TS kodi):
```typescript
class Container<T = string> {
    private val: T;

    constructor(initial: T) {
        this.val = initial;
    }

    get(): T {
        return this.val;
    }
}

const defaultContainer = new Container("Sukut bo'yicha satr");
const numContainer = new Container<number>(100);

console.log(defaultContainer.get());
console.log(numContainer.get());
```

## Tushuntirish va Mantiq:
<T = string> sintaksisi orqali generik parametr ko'rsatilmaganda avtomatik ravishda standart tip sifatida string olinishi belgilanadi.

## Ishlash natijasi:
```text
Sukut bo'yicha satr
100
```


# 664-Topshiriq: Sahifalash (Pagination) uchun sukutli generik interfeys

## Topshiriq sharti:
Elementlar ro'yxati va sahifalash metama'lumotlarini o'zida saqlovchi PaginatedResult interfeysini yozing.

## Yechim (JS yoki TS kodi):
```typescript
interface PaginatedResult<T = Record<string, any>> {
    items: T[];
    total: number;
    page: number;
    pageSize: number;
}

const userPage: PaginatedResult<{ id: number; name: string }> = {
    items: [{ id: 1, name: "Anvar" }],
    total: 1,
    page: 1,
    pageSize: 10
};

console.log(`Sahifadagi elementlar soni: ${userPage.items.length}`);
```

## Tushuntirish va Mantiq:
PaginatedResult<T = Record<string, any>> yordamida backend API lari uchun qaytuvchi ma'lumotlar tuzilmasini standartlashtirish mumkin.

## Ishlash natijasi:
```text
Sahifadagi elementlar soni: 1
```


# 665-Topshiriq: Generik Factory naqshi (Constructor type bilan)

## Topshiriq sharti:
Sinf konstruktorini qabul qilib, uning yangi instansiyasini hosil qiluvchi createInstance generik funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
class OrderService {
    public status = "OrderService faol";
}

function createInstance<T>(Cls: new () => T): T {
    return new Cls();
}

const service = createInstance(OrderService);
console.log(service.status);
```

## Tushuntirish va Mantiq:
new () => T konstruktor imzosidir. Bu orqali createInstance ixtiyoriy sinfni qabul qilib, uning to'g'ri tiplangan obyektini qaytara oladi.

## Ishlash natijasi:
```text
OrderService faol
```


# 666-Topshiriq: Generik Promise bilan asinxron API qidiruvi

## Topshiriq sharti:
JSON qabul qilib oluvchi soxta asinxron fetchApi generik funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
interface WeatherData {
    city: string;
    temp: number;
}

async function fetchMockApi<T>(data: T): Promise<T> {
    return Promise.resolve(data);
}

async function run() {
    const weather = await fetchMockApi<WeatherData>({ city: "Toshkent", temp: 22 });
    console.log(`Shahar: ${weather.city}, Harorat: ${weather.temp}°C`);
}

run();
```

## Tushuntirish va Mantiq:
Promise<T> qaytaruvchi asinxron funksiyalar chaqiruvchi kodga await qilingan qiymat aynan T tipi ekanini bildiradi.

## Ishlash natijasi:
```text
Shahar: Toshkent, Harorat: 22°C
```


# 667-Topshiriq: Generik Custom Filter funksiyasi

## Topshiriq sharti:
Array.prototype.filter ga o'xshash generik customFilter funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function customFilter<T>(arr: T[], predicate: (item: T) => boolean): T[] {
    const result: T[] = [];
    for (const el of arr) {
        if (predicate(el)) {
            result.push(el);
        }
    }
    return result;
}

const numbers = [1, 2, 3, 4, 5, 6];
const evens = customFilter(numbers, n => n % 2 === 0);
console.log("Juft sonlar:", evens);
```

## Tushuntirish va Mantiq:
predicate: (item: T) => boolean argumenti massiv elementlari tipi T ekanini biladi va qaytgan natija T[] massivi bo'ladi.

## Ishlash natijasi:
```text
Juft sonlar: [ 2, 4, 6 ]
```


# 668-Topshiriq: Generik Custom Map funksiyasi

## Topshiriq sharti:
Array.prototype.map kabi T tipidagi massivni U tipidagi yangi massivga aylantiruvchi customMap generik funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function customMap<T, U>(arr: T[], transform: (item: T) => U): U[] {
    const res: U[] = [];
    for (const el of arr) {
        res.push(transform(el));
    }
    return res;
}

const nums = [1, 2, 3];
const strLengths = customMap(nums, n => `Element #${n}`);
console.log("O'zgartirilgan massiv:", strLengths);
```

## Tushuntirish va Mantiq:
<T, U> yordamida kiruvchi element tipi T va chiquvchi element tipi U o'zaro ajratiladi.

## Ishlash natijasi:
```text
O'zgartirilgan massiv: [ 'Element #1', 'Element #2', 'Element #3' ]
```


# 669-Topshiriq: Generik Custom Reduce funksiyasi

## Topshiriq sharti:
Array.prototype.reduce ning soddalashtirilgan generik implementatsiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function customReduce<T, U>(arr: T[], reducer: (acc: U, curr: T) => U, initialValue: U): U {
    let acc = initialValue;
    for (const el of arr) {
        acc = reducer(acc, el);
    }
    return acc;
}

const words = ["TypeScript", "generiklari", "kuchli"];
const totalLength = customReduce(words, (acc, word) => acc + word.length, 0);
console.log("Umumiy belgilar soni:", totalLength);
```

## Tushuntirish va Mantiq:
customReduce<T, U> da akkumulyator tipi U bo'lib, T elementlari birin-ketin unga qo'shiladi.

## Ishlash natijasi:
```text
Umumiy belgilar soni: 28
```


# 670-Topshiriq: Generik Tuple o'rnini almashtirish (Swap)

## Topshiriq sharti:
Juftlikning birinchi va ikkinchi elementlarini teskari qilib beruvchi swap generik funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function swap<T, U>(tuple: [T, U]): [U, T] {
    return [tuple[1], tuple[0]];
}

const original: [number, string] = [200, "OK"];
const swapped = swap(original);

console.log("Asl tuple:", original);
console.log("Almashtirilgan:", swapped);
```

## Tushuntirish va Mantiq:
Generiklar tuple pozitsiyalarini to'liq saqlaydi: [number, string] kirsa, [string, number] chiqishi kafolatlanadi.

## Ishlash natijasi:
```text
Asl tuple: [ 200, 'OK' ]
Almashtirilgan: [ 'OK', 200 ]
```


# 671-Topshiriq: Generik Sinflarda merosxo'rlik

## Topshiriq sharti:
Entity<TId> umumiy asosiy sinfidan meros oluvchi UserEntity sinfini yozing.

## Yechim (JS yoki TS kodi):
```typescript
abstract class Entity<TId> {
    constructor(public id: TId) {}
}

class UserEntity extends Entity<number> {
    constructor(id: number, public name: string) {
        super(id);
    }
}

const user = new UserEntity(101, "Sardor");
console.log(`Foydalanuvchi ID: ${user.id}, Ism: ${user.name}`);
```

## Tushuntirish va Mantiq:
Voris sinf ota sinfning generik parametrini aniq tip bilan to'ldirishi (Entity<number>) yoki o'zi ham generik bo'lib qolishi mumkin.

## Ishlash natijasi:
```text
Foydalanuvchi ID: 101, Ism: Sardor
```


# 672-Topshiriq: Generik Interfeyslar merosxo'rligi

## Topshiriq sharti:
BasePayload<T> interfeysini kengaytiruvchi EventPayload<T, M> interfeysini yarating.

## Yechim (JS yoki TS kodi):
```typescript
interface BasePayload<T> {
    data: T;
    timestamp: number;
}

interface EventPayload<T, M> extends BasePayload<T> {
    meta: M;
    eventName: string;
}

const auditEvent: EventPayload<{ action: string }, { ip: string }> = {
    eventName: "USER_LOGIN",
    data: { action: "login" },
    timestamp: Date.now(),
    meta: { ip: "192.168.1.1" }
};

console.log("Hodisa nomi:", auditEvent.eventName);
```

## Tushuntirish va Mantiq:
Interfeyslarni extends qilishda generik parametrlar uzatiladi va yangi generik parametrlar qo'shilishi mumkin.

## Ishlash natijasi:
```text
Hodisa nomi: USER_LOGIN
```


# 673-Topshiriq: Generik cheklovda Union Type qo'llash

## Topshiriq sharti:
Faqat string yoki number tiplarini qabul qiluvchi generik funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
function stringifyVal<T extends string | number>(val: T): string {
    return String(val);
}

console.log("Satr:", stringifyVal("Matn"));
console.log("Son:", stringifyVal(12345));
```

## Tushuntirish va Mantiq:
T extends string | number cheklovi orqali funksiyaga boolean yoki obyekt kabi boshqa tiplarni kiritish taqiqlanadi.

## Ishlash natijasi:
```text
Satr: Matn
Son: 12345
```


# 674-Topshiriq: Generik Record yaratuvchi yordamchi funksiya

## Topshiriq sharti:
Kalitlar massivi va dastlabki qiymatni qabul qilib, Record hosil qiluvchi createRecord funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function createRecord<K extends string | number, V>(keys: K[], initialVal: V): Record<K, V> {
    const map = {} as Record<K, V>;
    for (const k of keys) {
        map[k] = initialVal;
    }
    return map;
}

const statusMap = createRecord(["online", "offline", "busy"], 0);
console.log("Xarita:", statusMap);
```

## Tushuntirish va Mantiq:
K extends string | number cheklovi Record kalitlari bo'lishi mumkin bo'lgan yaroqli turlarni ta'minlaydi.

## Ishlash natijasi:
```text
Xarita: { online: 0, offline: 0, busy: 0 }
```


# 675-Topshiriq: Generik Bog'langan Ro'yxat (Linked List) tuguni

## Topshiriq sharti:
Keyingi tugunga havola qiluvchi ListNode<T> generik sinfini yarating.

## Yechim (JS yoki TS kodi):
```typescript
class ListNode<T> {
    public value: T;
    public next: ListNode<T> | null = null;

    constructor(val: T) {
        this.value = val;
    }
}

const head = new ListNode<string>("Toshkent");
head.next = new ListNode<string>("Samarqand");
head.next.next = new ListNode<string>("Buxoro");

console.log(`Marshrut: ${head.value} -> ${head.next.value} -> ${head.next.next.value}`);
```

## Tushuntirish va Mantiq:
ListNode<T> rekursiv generik tuzilma bo'lib, o'z tipidagi keyingi tugunni saqlaydi.

## Ishlash natijasi:
```text
Marshrut: Toshkent -> Samarqand -> Buxoro
```


# 676-Topshiriq: Generik Hodisalar boshqaruvchisi (Typed Event Bus)

## Topshiriq sharti:
Hodisalar xaritasiga asoslangan tiplangan EventBus sinfini yarating.

## Yechim (JS yoki TS kodi):
```typescript
type EventMap = {
    login: { userId: number };
    logout: { timestamp: number };
};

class TypedEventBus<T extends Record<string, any>> {
    private handlers: { [K in keyof T]?: ((data: T[K]) => void)[] } = {};

    on<K extends keyof T>(event: K, handler: (data: T[K]) => void): void {
        if (!this.handlers[event]) this.handlers[event] = [];
        this.handlers[event]!.push(handler);
    }

    emit<K extends keyof T>(event: K, data: T[K]): void {
        this.handlers[event]?.forEach(h => h(data));
    }
}

const bus = new TypedEventBus<EventMap>();
bus.on("login", (data) => console.log(`Foydalanuvchi kirdi: ID=${data.userId}`));
bus.emit("login", { userId: 555 });
```

## Tushuntirish va Mantiq:
T extends Record<string, any> va K extends keyof T orqali hodisa nomi bilan unga uzatiladigan argument tipi bir-biriga 100% mos bo'lishi shart qilinadi.

## Ishlash natijasi:
```text
Foydalanuvchi kirdi: ID=555
```


# 677-Topshiriq: Generik Deep Clone yordamchisi

## Topshiriq sharti:
Obyektni chuqur nusxalovchi va original tipni qaytaruvchi generik funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
function deepClone<T>(obj: T): T {
    return JSON.parse(JSON.stringify(obj));
}

interface Config {
    env: string;
    retries: number;
}

const conf: Config = { env: "prod", retries: 3 };
const copy = deepClone(conf);
copy.retries = 5;

console.log(`Original: ${conf.retries}, Nusxa: ${copy.retries}`);
```

## Tushuntirish va Mantiq:
deepClone<T> qabul qilgan obyekt tipini qaytarish orqali nusxalangan ma'lumot ustida tiplash imkoniyatlarini yo'qotmaydi.

## Ishlash natijasi:
```text
Original: 3, Nusxa: 5
```


# 678-Topshiriq: Generik Builder naqshi (Query Builder)

## Topshiriq sharti:
Obyekt uchun filtrlash shartlarini zanjirli qo'shuvchi Builder sinfini yarating.

## Yechim (JS yoki TS kodi):
```typescript
class QueryBuilder<T> {
    private filters: Partial<T> = {};

    where<K extends keyof T>(key: K, value: T[K]): this {
        this.filters[key] = value;
        return this;
    }

    build(): Partial<T> {
        return this.filters;
    }
}

interface UserFilter {
    age: number;
    role: string;
    active: boolean;
}

const query = new QueryBuilder<UserFilter>()
    .where("role", "admin")
    .where("active", true)
    .build();

console.log("Qurilgan so'rov filtri:", query);
```

## Tushuntirish va Mantiq:
QueryBuilder<T> da K extends keyof T va T[K] tufayli noo'rin filtr maydoni yoki noto'g'ri qiymat kiritilishi mumkin emas.

## Ishlash natijasi:
```text
Qurilgan so'rov filtri: { role: 'admin', active: true }
```


# 679-Topshiriq: Generik State Store (Redux uslubida)

## Topshiriq sharti:
Holatni saqlovchi va listenerlarga xabar beruvchi generik Store sinfini yozing.

## Yechim (JS yoki TS kodi):
```typescript
class Store<T> {
    private state: T;
    private listeners: ((s: T) => void)[] = [];

    constructor(initial: T) {
        this.state = initial;
    }

    getState(): T {
        return this.state;
    }

    setState(newState: T): void {
        this.state = newState;
        this.listeners.forEach(l => l(this.state));
    }

    subscribe(listener: (s: T) => void): () => void {
        this.listeners.push(listener);
        return () => {
            this.listeners = this.listeners.filter(l => l !== listener);
        };
    }
}

const countStore = new Store<number>(0);
countStore.subscribe(val => console.log("Yangi holat:", val));
countStore.setState(1);
countStore.setState(5);
```

## Tushuntirish va Mantiq:
Store<T> har qanday murakkab state obyektini xavfsiz boshqarishda generik tiplardan foydalanadi.

## Ishlash natijasi:
```text
Yangi holat: 1
Yangi holat: 5
```


# 680-Topshiriq: Bir nechta interfeys bilan cheklangan generik

## Topshiriq sharti:
Ham id ga, ham name ga ega bo'lgan tiplarni qabul qiluvchi funksiya.

## Yechim (JS yoki TS kodi):
```typescript
interface WithId { id: number; }
interface WithName { name: string; }

function displayIdentity<T extends WithId & WithName>(entity: T): void {
    console.log(`ID: ${entity.id}, Nomi: ${entity.name}`);
}

const product = { id: 7, name: "Monitor", price: 250 };
displayIdentity(product);
```

## Tushuntirish va Mantiq:
T extends WithId & WithName ifodasi T tipi bir vaqtning o'zida ikkala interfeys shartlarini qondirishi lozimligini bildiradi.

## Ishlash natijasi:
```text
ID: 7, Nomi: Monitor
```


# 681-Topshiriq: Generik Rest parametrlari bilan to'plash

## Topshiriq sharti:
Ixtiyoriy sondagi bir xil tipdagi qiymatlarni bitta massivga o'rovchi generik funksiya.

## Yechim (JS yoki TS kodi):
```typescript
function collect<T>(...items: T[]): T[] {
    return items;
}

const strArr = collect("A", "B", "C");
const numArr = collect(1, 2, 3, 4);

console.log("Satrlar:", strArr);
console.log("Sonlar:", numArr);
```

## Tushuntirish va Mantiq:
...items: T[] barcha uzatilgan argumentlar yagona umumiy T tipiga ega bo'lishini ta'minlaydi.

## Ishlash natijasi:
```text
Satrlar: [ 'A', 'B', 'C' ]
Sonlar: [ 1, 2, 3, 4 ]
```


# 682-Topshiriq: Generik Memoize (Keshlash) wrapperi

## Topshiriq sharti:
Bitta argumentli har qanday funksiyaning natijasini keshlovchi generik funksiya.

## Yechim (JS yoki TS kodi):
```typescript
function memoize<TArg, TResult>(fn: (arg: TArg) => TResult): (arg: TArg) => TResult {
    const cache = new Map<TArg, TResult>();
    return (arg: TArg): TResult => {
        if (cache.has(arg)) {
            console.log(`[Keshdan olindi: ${arg}]`);
            return cache.get(arg)!;
        }
        const res = fn(arg);
        cache.set(arg, res);
        return res;
    };
}

const square = (n: number) => n * n;
const memoizedSquare = memoize(square);

console.log("Natija 1:", memoizedSquare(5));
console.log("Natija 2:", memoizedSquare(5));
```

## Tushuntirish va Mantiq:
memoize<TArg, TResult> original funksiya parametr va qaytish tiplarini to'liq saqlab qoladi.

## Ishlash natijasi:
```text
Natija 1: 25
[Keshdan olindi: 5]
Natija 2: 25
```


# 683-Topshiriq: Generik Result / Either tipi (Muvaffaqiyat yoki Xato)

## Topshiriq sharti:
Try-catch siz xatolarni xavfsiz boshqarish uchun Rust uslubidagi Result generik turini yarating.

## Yechim (JS yoki TS kodi):
```typescript
type Result<T, E = Error> =
    | { success: true; value: T }
    | { success: false; error: E };

function safeParseInt(str: string): Result<number, string> {
    const n = Number(str);
    if (isNaN(n)) {
        return { success: false, error: "Yaroqsiz son satri" };
    }
    return { success: true, value: n };
}

const res1 = safeParseInt("123");
const res2 = safeParseInt("abc");

if (res1.success) console.log("Son qiymati:", res1.value);
if (!res2.success) console.log("Xatolik:", res2.error);
```

## Tushuntirish va Mantiq:
Result<T, E> discriminated union bo'lib, success boolean qiymatiga qarab value yoki error maydonlarini tiplaydi.

## Ishlash natijasi:
```text
Son qiymati: 123
Xatolik: Yaroqsiz son satri
```


# 684-Topshiriq: Generik Option / Maybe tipi

## Topshiriq sharti:
Qiymat mavjud yoki mavjud emasligini ifodalovchi Option generik turi.

## Yechim (JS yoki TS kodi):
```typescript
type Option<T> = { hasValue: true; value: T } | { hasValue: false };

function findEven(nums: number[]): Option<number> {
    const found = nums.find(x => x % 2 === 0);
    if (found !== undefined) {
        return { hasValue: true, value: found };
    }
    return { hasValue: false };
}

const opt = findEven([1, 3, 6, 7]);
if (opt.hasValue) {
    console.log("Topilgan juft son:", opt.value);
}
```

## Tushuntirish va Mantiq:
Option<T> orqali null yoki undefined bilan bog'liq kutilmagan Runtime xatoliklarning oldi olinadi.

## Ishlash natijasi:
```text
Topilgan juft son: 6
```


# 685-Topshiriq: Generik Validatsiya interfeysi

## Topshiriq sharti:
Har qanday ma'lumot turini tekshiruvchi generik Validator interfeysini e'lon qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface Validator<T> {
    validate(val: T): { isValid: boolean; errors: string[] };
}

const emailValidator: Validator<string> = {
    validate(email: string) {
        const errors: string[] = [];
        if (!email.includes("@")) errors.push("@ belgisi yo'q");
        return { isValid: errors.length === 0, errors };
    }
};

console.log(emailValidator.validate("test@sayt.uz"));
console.log(emailValidator.validate("not-an-email"));
```

## Tushuntirish va Mantiq:
Validator<T> formalar, API payloadlari va domen obyektlarini tekshirishda umumiy qolip yaratadi.

## Ishlash natijasi:
```text
{ isValid: true, errors: [] }
{ isValid: false, errors: [ '@ belgisi yo\'q' ] }
```


# 686-Topshiriq: Generik LRU (Least Recently Used) kesh namunasi

## Topshiriq sharti:
Hajmi cheklangan LRU kesh sinfini generik kalit va qiymatlar bilan yozing.

## Yechim (JS yoki TS kodi):
```typescript
class SimpleLRU<K, V> {
    private cache = new Map<K, V>();

    constructor(private limit: number) {}

    get(key: K): V | undefined {
        if (!this.cache.has(key)) return undefined;
        const val = this.cache.get(key)!;
        this.cache.delete(key);
        this.cache.set(key, val);
        return val;
    }

    set(key: K, val: V): void {
        if (this.cache.has(key)) {
            this.cache.delete(key);
        } else if (this.cache.size >= this.limit) {
            const firstKey = this.cache.keys().next().value;
            if (firstKey !== undefined) this.cache.delete(firstKey);
        }
        this.cache.set(key, val);
    }
}

const lru = new SimpleLRU<string, number>(2);
lru.set("a", 1);
lru.set("b", 2);
lru.set("c", 3); // "a" o'chib ketadi
console.log("a mavjudmi:", lru.get("a"));
console.log("b mavjudmi:", lru.get("b"));
```

## Tushuntirish va Mantiq:
SimpleLRU<K, V> Map orqali buyurtmalarni boshqaradi va generiklar tufayli kalit hamda qiymatlar aniq tiplanadi.

## Ishlash natijasi:
```text
a mavjudmi: undefined
b mavjudmi: 2
```


# 687-Topshiriq: Generik Daraxt (Tree Node) tuzilmasi

## Topshiriq sharti:
Ierarxik tuzilma uchun TreeNode<T> generik interfeysini yarating.

## Yechim (JS yoki TS kodi):
```typescript
interface TreeNode<T> {
    value: T;
    children?: TreeNode<T>[];
}

const orgChart: TreeNode<string> = {
    value: "Bosh direktor",
    children: [
        { value: "Texnik direktor", children: [{ value: "Dasturchi" }] },
        { value: "Moliya direktori" }
    ]
};

console.log(`Kompaniya rahbari: ${orgChart.value}, Birinchi bola: ${orgChart.children?.[0].value}`);
```

## Tushuntirish va Mantiq:
TreeNode<T> rekursiv generik tuzilma orqali ixtiyoriy chuqurlikdagi daraxtsimon ma'lumotlarni tasvirlaydi.

## Ishlash natijasi:
```text
Kompaniya rahbari: Bosh direktor, Birinchi bola: Texnik direktor
```


# 688-Topshiriq: Generik Funksiyada `this` tipi bilan generic bog'lanish

## Topshiriq sharti:
Sinf metodida joriy obyektni o'zini qaytaruvchi generik shablon.

## Yechim (JS yoki TS kodi):
```typescript
class FluentEntity {
    protected props: Record<string, any> = {};

    setProp<K extends string, V>(this: any, key: K, val: V) {
        this.props[key] = val;
        return this;
    }

    getProps() {
        return this.props;
    }
}

const fe = new FluentEntity().setProp("color", "red").setProp("speed", 100);
console.log(fe.getProps());
```

## Tushuntirish va Mantiq:
this bilan generiklar birgalikda chaqiruv zanjirida metodlar o'z obyekti xususiyatlarini saqlab qolishini ta'minlaydi.

## Ishlash natijasi:
```text
{ color: 'red', speed: 100 }
```


# 689-Topshiriq: Generik Obyektlarni birlashtirish (mergeObjects)

## Topshiriq sharti:
Ikkita obyektni xavfsiz birlashtirib, ularning tipi T & U kesishmasi (intersection) bo'lgan obyekt qaytaruvchi funksiya.

## Yechim (JS yoki TS kodi):
```typescript
function mergeObjects<T, U>(obj1: T, obj2: U): T & U {
    return { ...obj1, ...obj2 };
}

const identity = { name: "Shaxzod" };
const contact = { phone: "+998901234567" };

const person = mergeObjects(identity, contact);
console.log(`Ism: ${person.name}, Telefon: ${person.phone}`);
```

## Tushuntirish va Mantiq:
Qaytish tipi T & U ikki obyektning barcha xossalarini yagona yangi tipga birlashtiradi.

## Ishlash natijasi:
```text
Ism: Shaxzod, Telefon: +998901234567
```


# 690-Topshiriq: Generik Pluck funksiyasi

## Topshiriq sharti:
Obyektlar massividan bitta kalitga mos keluvchi qiymatlarni ajratib oluvchi pluck funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function pluck<T, K extends keyof T>(items: T[], key: K): T[K][] {
    return items.map(item => item[key]);
}

const books = [
    { title: "Alkimyogar", pages: 180 },
    { title: "Yulduzli tunlar", pages: 450 }
];

const titles = pluck(books, "title");
const pages = pluck(books, "pages");

console.log("Kitob nomlari:", titles);
console.log("Sahifalar:", pages);
```

## Tushuntirish va Mantiq:
pluck funksiyasi K extends keyof T cheklovi orqali mavjud bo'lmagan kalit berilishiga yo'l qo'ymaydi va natija T[K][] tipida bo'ladi.

## Ishlash natijasi:
```text
Kitob nomlari: [ 'Alkimyogar', 'Yulduzli tunlar' ]
Sahifalar: [ 180, 450 ]
```


# 691-Topshiriq: Generik Sinflarda statik a'zolar qoidasi

## Topshiriq sharti:
Nega sinfning generik parametri statik metodlarda to'g'ridan-to'g'ri ishlatilmasligini tushuntiruvchi misol.

## Yechim (JS yoki TS kodi):
```typescript
class GenericHolder<T> {
    constructor(public val: T) {}

    // Statik metod sinfning T sidan foydalana olmaydi, o'zining generik parametrini e'lon qilishi kerak
    static createDefault<U>(defaultValue: U): GenericHolder<U> {
        return new GenericHolder<U>(defaultValue);
    }
}

const holder = GenericHolder.createDefault<number>(42);
console.log("Statik metoddan qiymat:", holder.val);
```

## Tushuntirish va Mantiq:
Statik a'zolar sinf instansiyasiga emas, sinfning o'ziga tegishli bo'lgani uchun ular GenericHolder<T> ning T parametriga kira olmaydi. Shuning uchun statik metod o'zining <U> generigiga ega bo'lishi lozim.

## Ishlash natijasi:
```text
Statik metoddan qiymat: 42
```


# 692-Topshiriq: Generik Type Alias bilan chuqur o'qiladigan tiplar (DeepReadonly)

## Topshiriq sharti:
Obyektning barcha ichma-ich xossalarini readonly qiluvchi generik type alias.

## Yechim (JS yoki TS kodi):
```typescript
type DeepReadonly<T> = {
    readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P];
};

interface UserProfile {
    name: string;
    location: { city: string };
}

const user: DeepReadonly<UserProfile> = {
    name: "Akmal",
    location: { city: "Buxoro" }
};

console.log(`Shahar: ${user.location.city}`);
```

## Tushuntirish va Mantiq:
Rekursiv generik tiplar orqali istalgan qatlamdagi obyekt xossalarini faqat o'qiladigan qilish mumkin.

## Ishlash natijasi:
```text
Shahar: Buxoro
```


# 693-Topshiriq: Generik Batch Processor (To'plamli ishlov beruvchi)

## Topshiriq sharti:
Elementlarni ma'lum o'lchamdagi guruhlarga (chunk) bo'luvchi generik funksiya.

## Yechim (JS yoki TS kodi):
```typescript
function chunkArray<T>(items: T[], size: number): T[][] {
    const chunks: T[][] = [];
    for (let i = 0; i < items.length; i += size) {
        chunks.push(items.slice(i, i + size));
    }
    return chunks;
}

const list = [1, 2, 3, 4, 5, 6, 7];
const chunked = chunkArray(list, 3);
console.log("Bo'lingan guruhlar:", chunked);
```

## Tushuntirish va Mantiq:
chunkArray<T> har qanday massivni T[][] (massivlar massivi) ko'rinishida guruhlarga ajratadi.

## Ishlash natijasi:
```text
Bo'lingan guruhlar: [ [ 1, 2, 3 ], [ 4, 5, 6 ], [ 7 ] ]
```


# 694-Topshiriq: Generik CSV qatorlarini obyektlarga parse qiluvchi funksiya

## Topshiriq sharti:
CSV sarlavhalari va qatorlarini qabul qilib, obyektlar massiviga aylantiruvchi yordamchi.

## Yechim (JS yoki TS kodi):
```typescript
function parseCsvLine<T extends Record<string, string>>(headers: (keyof T)[], line: string): T {
    const values = line.split(",");
    const result = {} as T;
    headers.forEach((h, idx) => {
        result[h] = (values[idx] || "") as any;
    });
    return result;
}

interface StudentCsv {
    id: string;
    name: string;
    grade: string;
}

const headers: (keyof StudentCsv)[] = ["id", "name", "grade"];
const parsed = parseCsvLine<StudentCsv>(headers, "1,Farrux,A");
console.log("Talaba:", parsed);
```

## Tushuntirish va Mantiq:
CSV parse qilishda generiklar maydonlar nomlarini tiplash va natijaviy obyekt strukturasi aniqligini ta'minlashda yordam beradi.

## Ishlash natijasi:
```text
Talaba: { id: '1', name: 'Farrux', grade: 'A' }
```


# 695-Topshiriq: Generik Dependency Injection konteyneri

## Topshiriq sharti:
Xizmatlarni kalit (token) bo'yicha ro'yxatga oluvchi va qaytaruvchi Container sinfi.

## Yechim (JS yoki TS kodi):
```typescript
class DIContainer {
    private services = new Map<string, any>();

    register<T>(key: string, service: T): void {
        this.services.set(key, service);
    }

    resolve<T>(key: string): T {
        const serv = this.services.get(key);
        if (!serv) throw new Error(`Xizmat topilmadi: ${key}`);
        return serv as T;
    }
}

const di = new DIContainer();
di.register<{ send(msg: string): void }>("mailer", {
    send: (m) => console.log(`Xat: ${m}`)
});

const mailer = di.resolve<{ send(msg: string): void }>("mailer");
mailer.send("Salom do'st!");
```

## Tushuntirish va Mantiq:
resolve<T> generik metodi konteynerdan olingan xizmatning barcha metodlari va xossalarini to'g'ri intellisense bilan ta'minlaydi.

## Ishlash natijasi:
```text
Xat: Salom do'st!
```


# 696-Topshiriq: Generik O'z-o'ziga bog'langan cheklov (F-Bounded Polymorphism)

## Topshiriq sharti:
O'z turiga teng yoki vorisi bo'lgan obyektlar bilan solishtiriladigan interfeys.

## Yechim (JS yoki TS kodi):
```typescript
interface Comparable<T> {
    compareTo(other: T): number;
}

class UserRank implements Comparable<UserRank> {
    constructor(public score: number) {}

    compareTo(other: UserRank): number {
        return this.score - other.score;
    }
}

function findMax<T extends Comparable<T>>(items: T[]): T | undefined {
    if (items.length === 0) return undefined;
    let max = items[0];
    for (let i = 1; i < items.length; i++) {
        if (items[i].compareTo(max) > 0) {
            max = items[i];
        }
    }
    return max;
}

const ranks = [new UserRank(10), new UserRank(50), new UserRank(30)];
console.log("Maksimal ball:", findMax(ranks)?.score);
```

## Tushuntirish va Mantiq:
T extends Comparable<T> namunasi generik tiplarda solishtirish mantiqini xavfsiz ifodalashda qo'llaniladi.

## Ishlash natijasi:
```text
Maksimal ball: 50
```


# 697-Topshiriq: Generik Shartli Tip bilan tekshirish (Conditional Types)

## Topshiriq sharti:
Agar tip massiv bo'lsa uning element tipini, aks holda tipning o'zini qaytaruvchi Unpack generigi.

## Yechim (JS yoki TS kodi):
```typescript
type Unpack<T> = T extends (infer U)[] ? U : T;

type A = Unpack<string[]>; // string
type B = Unpack<number>;   // number

const word: A = "TypeScript";
const num: B = 100;

console.log(`A: ${typeof word}, B: ${typeof num}`);
```

## Tushuntirish va Mantiq:
T extends (infer U)[] ? U : T shartli generik turi massiv ichidagi ichki element turini avtomatik ajratib oladi.

## Ishlash natijasi:
```text
A: string, B: number
```


# 698-Topshiriq: Generik Birlashma turi bo'yicha farqlash

## Topshiriq sharti:
Turli ma'lumot turlari bo'yicha diskriminant qiymatni ajratuvchi yordamchi.

## Yechim (JS yoki TS kodi):
```typescript
interface Square { kind: "square"; size: number; }
interface Circle { kind: "circle"; radius: number; }

type Shape = Square | Circle;

function getArea<T extends Shape>(shape: T): number {
    if (shape.kind === "square") {
        return shape.size * shape.size;
    }
    return Math.PI * shape.radius * shape.radius;
}

console.log("Kvadrat yuzi:", getArea({ kind: "square", size: 4 }));
console.log("Doira yuzi:", getArea({ kind: "circle", radius: 3 }).toFixed(2));
```

## Tushuntirish va Mantiq:
Discriminated union bilan generiklar birgalikda ishlaganda, obyektning kind maydoniga qarab boshqa xossalar avtomatik aniqlanadi.

## Ishlash natijasi:
```text
Kvadrat yuzi: 16
Doira yuzi: 28.27
```


# 699-Topshiriq: Generik Retry asinxron yordamchisi

## Topshiriq sharti:
Asinxron funksiyani berilgan urinishlar sonicha qayta bajaruvchi generik retry funksiyasi.

## Yechim (JS yoki TS kodi):
```typescript
async function retry<T>(fn: () => Promise<T>, attempts: number): Promise<T> {
    let lastError: any;
    for (let i = 0; i < attempts; i++) {
        try {
            return await fn();
        } catch (err) {
            lastError = err;
        }
    }
    throw lastError;
}

let counter = 0;
async function unreliableTask(): Promise<string> {
    counter++;
    if (counter < 2) throw new Error("Tarmoq xatosi");
    return "Muvaffaqiyat!";
}

retry(unreliableTask, 3).then(res => console.log("Natija:", res));
```

## Tushuntirish va Mantiq:
retry<T> asinxron operatsiyaning qaytish qiymati tipini Promise<T> sifatida to'liq kafolatlaydi.

## Ishlash natijasi:
```text
Natija: Muvaffaqiyat!
```


# 700-Topshiriq: Generik Konfiguratsiya boshqaruvchisi (ConfigManager)

## Topshiriq sharti:
Sozlamalar obyektini xavfsiz boshqaruvchi va faqat mavjud kalitlarni o'qish/yozish imkonini beruvchi sinf.

## Yechim (JS yoki TS kodi):
```typescript
class ConfigManager<T extends object> {
    constructor(private config: T) {}

    get<K extends keyof T>(key: K): T[K] {
        return this.config[key];
    }

    set<K extends keyof T>(key: K, value: T[K]): void {
        this.config[key] = value;
    }
}

interface AppSettings {
    port: number;
    host: string;
    debug: boolean;
}

const config = new ConfigManager<AppSettings>({ port: 3000, host: "localhost", debug: false });
config.set("port", 8080);
console.log(`Server ishlamoqda: http://${config.get("host")}:${config.get("port")}`);
```

## Tushuntirish va Mantiq:
ConfigManager<T> da K extends keyof T va T[K] generik cheklovlari noto'g'ri kalit yoki mos kelmaydigan qiymat berilishini dastur yozish vaqtidanoq butunlay bartaraf etadi.

## Ishlash natijasi:
```text
Server ishlamoqda: http://localhost:8080
```

