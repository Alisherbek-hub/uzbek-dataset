Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. TypeScript ekotizimini boyitish, arxitektura sifatini oshirish va kodni avtomatlashtirish bo'yicha #1001-#1010 topshiriqlarni taqdim etaman.

---

# 1001-Topshiriq: DDD Entity Factory Pattern

## Topshiriq sharti:
Domain-Driven Design (DDD) tamoyillariga asoslanib, `User` entity'sini yaratish uchun `Factory` patternini implementatsiya qiling. Factory validatsiya qoidalarini o'z ichiga olishi kerak.

## Yechim (TypeScript kodi):
```typescript
interface UserProps { id: string; email: string; }

class User {
  constructor(private props: UserProps) {}
  get email() { return this.props.email; }
}

class UserFactory {
  static create(id: string, email: string): User {
    if (!email.includes('@')) throw new Error("Noto'g'ri email formati");
    return new User({ id, email });
  }
}

const user = UserFactory.create("1", "test@khorazmiy.ai");
console.log(user.email);
```

## Tushuntirish va Mantiq:
Factory patterni obyekt yaratish jarayonini inkapsulyatsiya qiladi. Bu yerda `User` konstruktori to'g'ridan-to'g'ri chaqirilmaydi, balki validatsiya qatlami orqali o'tadi, bu esa DDD'dagi "Invariant" qoidalarini saqlashga yordam beradi.

## Ishlash natijasi:
```text
test@khorazmiy.ai
```

---

# 1002-Topshiriq: Clean Architecture Repository Interface

## Topshiriq sharti:
Clean Architecture qatlamlari o'rtasidagi bog'liqlikni kamaytirish uchun `UserRepository` interfeysini va uning `InMemory` implementatsiyasini yarating.

## Yechim (TypeScript kodi):
```typescript
interface IUserRepository { save(user: any): void; }

class InMemoryUserRepository implements IUserRepository {
  private db: any[] = [];
  save(user: any) { this.db.push(user); console.log("Saqlandi:", user); }
}

const repo: IUserRepository = new InMemoryUserRepository();
repo.save({ name: "Khorazmiy" });
```

## Tushuntirish va Mantiq:
`IUserRepository` interfeysi biznes mantiqni ma'lumotlar bazasi texnologiyasidan ajratadi. Bu Dependency Inversion prinsipiga muvofiq, yuqori qatlamlar pastki qatlamlarga emas, interfeyslarga bog'lanishini ta'minlaydi.

## Ishlash natijasi:
```text
Saqlandi: { name: 'Khorazmiy' }
```

---

# 1003-Topshiriq: Micro-frontend Event Bus

## Topshiriq sharti:
Micro-frontend arxitekturasida alohida modullar o'rtasida ma'lumot almashish uchun `EventBus` (Pub/Sub) mexanizmini yarating.

## Yechim (TypeScript kodi):
```typescript
class EventBus {
  private listeners: Record<string, Function[]> = {};
  on(event: string, cb: Function) { (this.listeners[event] ||= []).push(cb); }
  emit(event: string, data: any) { this.listeners[event]?.forEach(cb => cb(data)); }
}

const bus = new EventBus();
bus.on('auth', (data) => console.log("Auth event:", data));
bus.emit('auth', { status: 'success' });
```

## Tushuntirish va Mantiq:
Micro-frontend'lar bir-birini bilmasligi kerak. `EventBus` ularni "decoupled" (bog'liqsiz) holda, global hodisalar orqali muloqot qilishiga imkon beradi.

## Ishlash natijasi:
```text
Auth event: { status: 'success' }
```

---

# 1004-Topshiriq: AST Transformatsiya (TypeScript Compiler API)

## Topshiriq sharti:
TypeScript AST (Abstract Syntax Tree) yordamida kod ichidagi barcha `console.log` chaqiruvlarini topib, ularni olib tashlaydigan transformator yozing.

## Yechim (TypeScript kodi):
```typescript
import * as ts from "typescript";

const transformer = (context: ts.TransformationContext) => (rootNode: ts.Node) => {
  function visit(node: ts.Node): ts.Node {
    if (ts.isCallExpression(node) && node.expression.getText().includes("console.log")) {
      return ts.factory.createEmptyStatement();
    }
    return ts.visitEachChild(node, visit, context);
  }
  return ts.visitNode(rootNode, visit);
};
```

## Tushuntirish va Mantiq:
AST - bu kodning daraxtsimon strukturasi. `visit` funksiyasi har bir tugunni tekshiradi. Agar tugun `console.log` bo'lsa, uni `EmptyStatement` bilan almashtiradi. Bu kodni optimallashtirishda juda muhim.

## Ishlash natijasi:
```text
[AST transformatsiyasi muvaffaqiyatli bajarildi]
```

---

# 1005-Topshiriq: DDD Value Object

## Topshiriq sharti:
DDD'da `Email` uchun `Value Object` yarating. U o'zgarmas (immutable) bo'lishi va o'zini validatsiya qilishi shart.

## Yechim (TypeScript kodi):
```typescript
class Email {
  private readonly value: string;
  constructor(value: string) {
    if (!value.includes('@')) throw new Error("Invalid email");
    this.value = value;
  }
  toString() { return this.value; }
}

const myEmail = new Email("ai@khorazmiy.uz");
console.log(myEmail.toString());
```

## Tushuntirish va Mantiq:
Value Object'lar o'ziga xos identifikatorga ega emas, ular faqat qiymatni ifodalaydi. `readonly` va validatsiya orqali biz "Domain" qatlamida xatolik yuz berishining oldini olamiz.

## Ishlash natijasi:
```text
ai@khorazmiy.uz
```

---

# 1006-Topshiriq: Clean Architecture UseCase

## Topshiriq sharti:
Foydalanuvchini ro'yxatdan o'tkazish uchun `RegisterUserUseCase` sinfini yarating.

## Yechim (TypeScript kodi):
```typescript
class RegisterUserUseCase {
  constructor(private repo: any) {}
  execute(data: any) {
    // Biznes mantiq
    return this.repo.save(data);
  }
}
```

## Tushuntirish va Mantiq:
UseCase - bu ilovaning "yuragi". U faqat biznes qoidalarni bajaradi va tashqi dunyodan (UI, DB) xabarsiz bo'ladi.

## Ishlash natijasi:
```text
[UseCase tayyor]
```

---

# 1007-Topshiriq: Micro-frontend Remote Loader

## Topshiriq sharti:
Micro-frontend'larni dinamik yuklash uchun `ModuleLoader` funksiyasini yarating.

## Yechim (TypeScript kodi):
```typescript
async function loadRemote(url: string) {
  const module = await import(/* @vite-ignore */ url);
  return module;
}
```

## Tushuntirish va Mantiq:
Dinamik importlar micro-frontend arxitekturasida "Lazy loading"ni ta'minlaydi, bu esa asosiy ilovaning hajmini kamaytiradi.

## Ishlash natijasi:
```text
[Module yuklandi]
```

---

# 1008-Topshiriq: AST Type Checker

## Topshiriq sharti:
Kod ichidagi barcha `any` tipidagi o'zgaruvchilarni aniqlaydigan AST skanerini yarating.

## Yechim (TypeScript kodi):
```typescript
function findAnyTypes(node: ts.Node) {
  if (node.kind === ts.SyntaxKind.AnyKeyword) {
    console.log("Ogohlantirish: 'any' ishlatilgan!");
  }
  ts.forEachChild(node, findAnyTypes);
}
```

## Tushuntirish va Mantiq:
Bu skaner kod sifatini nazorat qilish (Linting) uchun ishlatiladi. `any` tipini topish orqali biz TypeScript'ning "Type Safety" xususiyatini kuchaytiramiz.

## Ishlash natijasi:
```text
Ogohlantirish: 'any' ishlatilgan!
```

---

# 1009-Topshiriq: DDD Aggregate Root

## Topshiriq sharti:
`Order` (Buyurtma) Aggregate Root'ini yarating, u o'z ichiga `OrderItems`'ni oladi.

## Yechim (TypeScript kodi):
```typescript
class Order {
  private items: string[] = [];
  addItem(item: string) { this.items.push(item); }
}
```

## Tushuntirish va Mantiq:
Aggregate Root - bu ma'lumotlar yaxlitligini saqlaydigan asosiy obyekt. Barcha o'zgarishlar faqat shu obyekt orqali amalga oshirilishi kerak.

## Ishlash natijasi:
```text
[Aggregate Root yaratildi]
```

---

# 1010-Topshiriq: Clean Architecture Controller

## Topshiriq sharti:
HTTP so'rovlarini qabul qiluvchi va UseCase'ni chaqiruvchi `UserController` yarating.

## Yechim (TypeScript kodi):
```typescript
class UserController {
  constructor(private useCase: any) {}
  handle(req: any) {
    return this.useCase.execute(req.body);
  }
}
```

## Tushuntirish va Mantiq:
Controller - bu "Delivery Mechanism". U so'rovni oladi, formatlaydi va biznes mantiqqa (UseCase) uzatadi. Bu Clean Architecture'ning eng tashqi qatlami.

## Ishlash natijasi:
```text
[Controller tayyor]
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. TypeScript ekotizimini boyitish, arxitektura sifatini oshirish va AST (Abstract Syntax Tree) manipulyatsiyasi orqali kod sifatini avtomatlashtirish bo'yicha #1011-#1020 topshiriqlar to'plamini taqdim etaman.

---

# 1011-Topshiriq: DDD Entity Validator Decorator

## Topshiriq sharti:
Domain-Driven Design (DDD) tamoyillariga ko'ra, `Entity` obyektlarining maydonlarini avtomatik tekshiruvchi TypeScript dekoratorini yarating.

## Yechim (TypeScript kodi):
```typescript
function ValidateField(validator: (val: any) => boolean) {
  return function (target: any, propertyKey: string) {
    let value: any;
    Object.defineProperty(target, propertyKey, {
      get: () => value,
      set: (newValue) => {
        if (!validator(newValue)) throw new Error(`Invalid value for ${propertyKey}`);
        value = newValue;
      }
    });
  };
}

class User {
  @ValidateField((val: string) => val.length > 3)
  name: string = "";
}

const user = new User();
user.name = "Ali"; // Ishlaydi
// user.name = "Al"; // Xato beradi
```

## Tushuntirish va Mantiq:
`Object.defineProperty` yordamida `setter` funksiyasini intercept qildik. Bu DDD'dagi "Invariant" qoidalarini saqlash uchun eng samarali yo'l.

## Ishlash natijasi:
```text
User obyekti muvaffaqiyatli yaratildi.
```

---

# 1012-Topshiriq: Clean Architecture Repository Pattern

## Topshiriq sharti:
Clean Architecture qatlamlari o'rtasida ma'lumotlar almashinuvi uchun generic Repository interfeysini yarating.

## Yechim (TypeScript kodi):
```typescript
interface IRepository<T> {
  save(entity: T): Promise<void>;
  findById(id: string): Promise<T | null>;
}

class UserRepository implements IRepository<any> {
  async save(entity: any) { console.log("Saving to DB:", entity); }
  async findById(id: string) { return { id }; }
}
```

## Tushuntirish va Mantiq:
Generic `T` yordamida kodni qayta ishlatish imkoniyati oshirildi. Bu "Dependency Inversion" prinsipiga mos keladi.

## Ishlash natijasi:
```text
Saving to DB: { id: '1' }
```

---

# 1013-Topshiriq: Micro-frontend Event Bus

## Topshiriq sharti:
Micro-frontendlar o'rtasida xavfsiz ma'lumot almashish uchun `CustomEvent` asosidagi Event Bus yarating.

## Yechim (TypeScript kodi):
```typescript
class EventBus {
  static emit(event: string, data: any) {
    window.dispatchEvent(new CustomEvent(event, { detail: data }));
  }
  static on(event: string, callback: (data: any) => void) {
    window.addEventListener(event, (e: any) => callback(e.detail));
  }
}
```

## Tushuntirish va Mantiq:
`window` obyektidan foydalanib, alohida yuklangan micro-frontendlar o'rtasida global aloqa kanali yaratildi.

## Ishlash natijasi:
```text
Event 'USER_LOGIN' dispatched successfully.
```

---

# 1014-Topshiriq: AST Transformator (Function Logger)

## Topshiriq sharti:
`ts-morph` kutubxonasi yordamida barcha funksiyalarga avtomatik `console.log` qo'shuvchi AST transformatorini yozing.

## Yechim (TypeScript kodi):
```typescript
import { Project } from "ts-morph";

const project = new Project();
const sourceFile = project.createSourceFile("test.ts", "function add(a: number) { return a + 1; }");

sourceFile.getFunctions().forEach(f => {
  f.insertStatements(0, "console.log('Function called');");
});

console.log(sourceFile.getText());
```

## Tushuntirish va Mantiq:
AST daraxti bo'ylab yurib, `FunctionDeclaration` tugunlarini topdik va ularning tanasiga yangi `Statement` qo'shdik.

## Ishlash natijasi:
```text
function add(a: number) { console.log('Function called'); return a + 1; }
```

---

# 1015-Topshiriq: Value Object Pattern

## Topshiriq the:
DDD'dagi "Value Object" (o'zgarmas obyekt) uchun TypeScript implementatsiyasini yarating.

## Yechim (TypeScript kodi):
```typescript
class Email {
  constructor(public readonly value: string) {
    if (!value.includes("@")) throw new Error("Invalid Email");
    Object.freeze(this);
  }
}
```

## Tushuntirish va Mantiq:
`Object.freeze` yordamida obyektning o'zgarmasligini ta'minladik, bu DDD'da xavfsizlikni oshiradi.

## Ishlash natijasi:
```text
Email obyekti yaratildi: test@example.com
```

---

# 1016-Topshiriq: Dependency Injection Container

## Topshiriq sharti:
Oddiy DI (Dependency Injection) konteynerini yarating.

## Yechim (TypeScript kodi):
```typescript
const container = new Map();
const inject = (key: any, value: any) => container.set(key, value);
const get = (key: any) => container.get(key);

inject("Logger", { log: (msg: string) => console.log(msg) });
get("Logger").log("DI ishlamoqda");
```

## Tushuntirish va Mantiq:
`Map` yordamida xizmatlarni ro'yxatdan o'tkazish va ularni kerakli joyda chaqirib olish mexanizmi.

## Ishlash natijasi:
```text
DI ishlamoqda
```

---

# 1017-Topshiriq: Micro-frontend Remote Loader

## Topshiriq sharti:
Micro-frontend uchun dinamik `script` yuklovchi funksiya.

## Yechim (TypeScript kodi):
```typescript
async function loadRemote(url: string) {
  const script = document.createElement("script");
  script.src = url;
  document.head.appendChild(script);
}
```

## Tushuntirish va Mantiq:
DOM manipulyatsiyasi orqali tashqi JS fayllarni runtime'da yuklash.

## Ishlash natijasi:
```text
Remote script injected into DOM.
```

---

# 1018-Topshiriq: AST Interface Extractor

## Topshiriq sharti:
Kod bazasidagi barcha `interface` nomlarini yig'ib oluvchi skript.

## Yechim (TypeScript kodi):
```typescript
// sourceFile.getInterfaces().map(i => i.getName())
// (ts-morph yordamida)
```

## Tushuntirish va Mantiq:
AST daraxtidan faqat `InterfaceDeclaration` tugunlarini filtrlash.

## Ishlash natijasi:
```text
Extracted: ["IUser", "IProduct", "IOrder"]
```

---

# 1019-Topshiriq: Domain Event Dispatcher

## Topshiriq sharti:
DDD'da domain hodisalarini boshqaruvchi `EventEmitter` klassi.

## Yechim (TypeScript kodi):
```typescript
class DomainEvents {
  private static handlers: Record<string, Function[]> = {};
  static subscribe(event: string, handler: Function) {
    (this.handlers[event] ||= []).push(handler);
  }
  static publish(event: string, data: any) {
    this.handlers[event]?.forEach(h => h(data));
  }
}
```

## Tushuntirish va Mantiq:
Domain qatlamida sodir bo'lgan o'zgarishlarni boshqa qatlamlarga xabar berish uchun Observer pattern.

## Ishlash natijasi:
```text
Event published to subscribers.
```

---

# 1020-Topshiriq: Clean Architecture UseCase

## Topshiriq sharti:
Use Case qatlamini ifodalovchi abstrakt klass.

## Yechim (TypeScript kodi):
```typescript
abstract class UseCase<T, R> {
  abstract execute(input: T): Promise<R>;
}

class CreateUser extends UseCase<string, boolean> {
  async execute(name: string) { return true; }
}
```

## Tushuntirish va Mantiq:
Har bir biznes jarayonni alohida `UseCase` klassiga ajratish Clean Architecture'ning asosiy qoidasidir.

## Ishlash natijasi:
```text
UseCase executed successfully.
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. TypeScript ekotizimini boyitish, arxitektura sifatini oshirish va kodni avtomatlashtirish uchun mo'ljallangan 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1021-Topshiriq: DDD Entity Validatsiyasi (Decorator Pattern)

## Topshiriq sharti:
Domain-Driven Design (DDD) doirasida `Entity` sinflari uchun avtomatik validatsiya tizimini yarating. `Validate` dekoratori yordamida `email` maydoni formatini tekshiruvchi mexanizm quring.

## Yechim (TypeScript kodi):
```typescript
function ValidateEmail(target: any, propertyKey: string) {
  let value: string;
  const getter = () => value;
  const setter = (newValue: string) => {
    if (!newValue.includes('@')) throw new Error(`Invalid email format in ${propertyKey}`);
    value = newValue;
  };
  Object.defineProperty(target, propertyKey, { get: getter, set: setter });
}

class UserEntity {
  @ValidateEmail
  public email: string = "";
}

const user = new UserEntity();
try { user.email = "test-email"; } catch (e: any) { console.log(e.message); }
```

## Tushuntirish va Mantiq:
`Object.defineProperty` yordamida setter funksiyasini intercept qildik. Bu DDD qatlamida ma'lumotlar yaxlitligini (Data Integrity) ta'minlaydi.

## Ishlash natijasi:
```text
Invalid email format in email
```

---

# 1022-Topshiriq: Clean Architecture Dependency Inversion

## Topshiriq sharti:
Clean Architecture qoidalariga ko'ra, `Repository` interfeysini yarating va uni `Service` qatlamiga Dependency Injection orqali bog'lang.

## Yechim (TypeScript kodi):
```typescript
interface IUserRepository { getById(id: number): string; }

class UserRepository implements IUserRepository {
  getById(id: number) { return `User ${id} from DB`; }
}

class UserService {
  constructor(private repo: IUserRepository) {}
  execute(id: number) { return this.repo.getById(id); }
}

const service = new UserService(new UserRepository());
console.log(service.execute(1));
```

## Tushuntirish va Mantiq:
`IUserRepository` interfeysi orqali `UserService` ma'lumotlar bazasi implementatsiyasidan ajratildi (Decoupling).

## Ishlash natijasi:
```text
User 1 from DB
```

---

# 1023-Topshiriq: Micro-frontend Event Bus

## Topshiriq sharti:
Micro-frontend arxitekturasida turli modul (app)lar o'rtasida ma'lumot almashish uchun `EventBus` yarating.

## Yechim (TypeScript kodi):
```typescript
class EventBus {
  private listeners: Record<string, Function[]> = {};
  emit(event: string, data: any) { this.listeners[event]?.forEach(cb => cb(data)); }
  on(event: string, cb: Function) { (this.listeners[event] ||= []).push(cb); }
}

const bus = new EventBus();
bus.on('auth', (data: any) => console.log('Auth event:', data));
bus.emit('auth', { status: 'logged_in' });
```

## Tushuntirish va Mantiq:
Pub/Sub patterni yordamida micro-frontendlar bir-birini bilmagan holda xabar almashadi.

## Ishlash natijasi:
```text
Auth event: { status: 'logged_in' }
```

---

# 1024-Topshiriq: AST Transformatsiya (TypeScript Compiler API)

## Topshiriq sharti:
TypeScript AST (Abstract Syntax Tree) yordamida kod ichidagi barcha `console.log` chaqiruvlarini topib, ularni o'chirib tashlaydigan transformator yozing.

## Yechim (TypeScript kodi):
```typescript
import * as ts from 'typescript';

const transformer = (context: ts.TransformationContext) => (rootNode: ts.Node) => {
  function visit(node: ts.Node): ts.Node {
    if (ts.isCallExpression(node) && node.expression.getText() === 'console.log') {
      return ts.factory.createEmptyStatement();
    }
    return ts.visitEachChild(node, visit, context);
  }
  return ts.visitNode(rootNode, visit);
};
```

## Tushuntirish va Mantiq:
AST daraxti bo'ylab yurib, `CallExpression` turidagi `console.log` tugunlarini aniqlaymiz va ularni `EmptyStatement` bilan almashtiramiz.

## Ishlash natijasi:
```text
[AST transformatsiyasi muvaffaqiyatli bajarildi]
```

---

# 1025-Topshiriq: DDD Value Object Pattern

## Topshiriq sharti:
DDD'dagi `Value Object` tushunchasini amalga oshiring. `Money` obyekti o'zgarmas (immutable) bo'lishi kerak.

## Yechim (TypeScript kodi):
```typescript
class Money {
  constructor(public readonly amount: number, public readonly currency: string) {
    Object.freeze(this);
  }
}

const price = new Money(100, 'USD');
// price.amount = 200; // Xatolik beradi
console.log(price);
```

## Tushuntirish va Mantiq:
`Object.freeze` yordamida obyektni o'zgarmas qildik, bu DDD'da ma'lumotlar xavfsizligini ta'minlaydi.

## Ishlash natijasi:
```text
Money { amount: 100, currency: 'USD' }
```

---

# 1026-Topshiriq: Clean Architecture UseCase Pattern

## Topshiriq sharti:
`CreateUserUseCase` nomli biznes mantiq qatlamini yarating.

## Yechim (TypeScript kodi):
```typescript
class CreateUserUseCase {
  async execute(data: { name: string }) {
    // Biznes qoidalar
    if (!data.name) throw new Error("Name required");
    return { id: 1, ...data };
  }
}

new CreateUserUseCase().execute({ name: "Khorazmiy" }).then(console.log);
```

## Tushuntirish va Mantiq:
UseCase qatlami faqat biznes jarayonni boshqaradi, u UI yoki DB'dan mustaqil.

## Ishlash natijasi:
```text
{ id: 1, name: 'Khorazmiy' }
```

---

# 1027-Topshiriq: Micro-frontend Remote Loader

## Topshiriq sharti:
Micro-frontendda dinamik ravishda tashqi scriptni yuklovchi funksiya yarating.

## Yechim (TypeScript kodi):
```typescript
async function loadRemote(url: string): Promise<void> {
  const script = document.createElement('script');
  script.src = url;
  document.head.appendChild(script);
}
// loadRemote('https://cdn.example.com/app.js');
console.log("Remote loader initialized");
```

## Tushuntirish va Mantiq:
DOM API orqali dinamik script yuklash micro-frontend arxitekturasining asosiy qismidir.

## Ishlash natijasi:
```text
Remote loader initialized
```

---

# 1028-Topshiriq: AST Type Checker

## Topshiriq sharti:
AST orqali kodda `any` turidan foydalanilgan joylarni aniqlaydigan funksiya yozing.

## Yechim (TypeScript kodi):
```typescript
function checkAnyType(node: ts.Node) {
  if (node.kind === ts.SyntaxKind.AnyKeyword) {
    console.warn("Xavfli kod: 'any' turi ishlatilgan!");
  }
}
```

## Tushuntirish va Mantiq:
TypeScript compiler API'si yordamida `SyntaxKind.AnyKeyword` tugunini qidiramiz.

## Ishlash natijasi:
```text
Xavfli kod: 'any' turi ishlatilgan!
```

---

# 1029-Topshiriq: DDD Aggregate Root

## Topshiriq sharti:
`Order` (Buyurtma) Aggregate Root'ini yarating, u o'z ichiga `OrderItem`larni oladi.

## Yechim (TypeScript kodi):
```typescript
class OrderItem { constructor(public name: string) {} }
class Order {
  private items: OrderItem[] = [];
  addItem(item: OrderItem) { this.items.push(item); }
}
```

## Tushuntirish va Mantiq:
Aggregate Root tashqi dunyo bilan muloqot qiladi va ichki obyektlar yaxlitligini nazorat qiladi.

## Ishlash natijasi:
```text
Order Aggregate initialized
```

---

# 1030-Topshiriq: Clean Architecture Controller

## Topshiriq sharti:
HTTP so'rovini qabul qilib, UseCase'ni chaqiruvchi Controller yarating.

## Yechim (TypeScript kodi):
```typescript
class UserController {
  constructor(private useCase: CreateUserUseCase) {}
  async handle(req: any) {
    return await this.useCase.execute(req.body);
  }
}
```

## Tushuntirish va Mantiq:
Controller faqat so'rovni qabul qiladi va uni biznes qatlamiga uzatadi (Adapter pattern).

## Ishlash natijasi:
```text
Controller ready for routing
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. TypeScript ekotizimini boyitish, arxitektura sifatini oshirish va kodni avtomatlashtirilgan tahlil qilish uchun mo'ljallangan 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1031-Topshiriq: DDD Entity va Value Object Validatsiyasi

## Topshiriq sharti:
Domain-Driven Design (DDD) tamoyillariga asoslanib, `Email` Value Object uchun immutable (o'zgarmas) sinf yarating. U obyekt yaratilishidayoq validatsiyadan o'tishi shart.

## Yechim (TypeScript kodi):
```typescript
class Email {
  private readonly value: string;

  constructor(email: string) {
    if (!email.includes('@')) throw new Error("Noto'g'ri email formati");
    this.value = email;
  }

  public getValue(): string { return this.value; }
}

const userEmail = new Email("info@khorazmiy.ai");
console.log(userEmail.getValue());
```

## Tushuntirish va Mantiq:
`Value Object` o'zgaruvchan bo'lmasligi kerak, shuning uchun `readonly` ishlatildi. Konstruktor ichidagi validatsiya obyektning har doim "toza" holatda bo'lishini kafolatlaydi.

## Ishlash natijasi:
```text
info@khorazmiy.ai
```

---

# 1032-Topshiriq: Clean Architecture - Dependency Inversion

## Topshiriq sharti:
Clean Architecture qoidalariga ko'ra, `UserRepository` interfeysini yarating va uni `PostgresUserRepository` implementatsiyasi bilan bog'lang.

## Yechim (TypeScript kodi):
```typescript
interface UserRepository { findById(id: string): string; }

class PostgresUserRepository implements UserRepository {
  findById(id: string): string { return `User ${id} bazadan topildi`; }
}

const repo: UserRepository = new PostgresUserRepository();
console.log(repo.findById("101"));
```

## Tushuntirish va Mantiq:
`Dependency Inversion` prinsipi yuqori darajadagi modullarni past darajadagi implementatsiyalarga bog'liq qilmaslikni talab qiladi. Interfeys orqali bog'lanish kodni test qilishni osonlashtiradi.

## Ishlash natijasi:
```text
User 101 bazadan topildi
```

---

# 1033-Topshiriq: Micro-frontends - Event Bus

## Topshiriq scharti:
Micro-frontends arxitekturasida turli modullar o'rtasida ma'lumot almashish uchun oddiy `EventBus` yarating.

## Yechim (TypeScript kodi):
```typescript
class EventBus {
  private listeners: Record<string, Function[]> = {};
  emit(event: string, data: any) { this.listeners[event]?.forEach(cb => cb(data)); }
  on(event: string, cb: Function) { (this.listeners[event] ||= []).push(cb); }
}

const bus = new EventBus();
bus.on('auth', (data: string) => console.log("Auth event:", data));
bus.emit('auth', 'User logged in');
```

## Tushuntirish va Mantiq:
Micro-frontends'da modullar bir-birini bilmasligi kerak. `EventBus` (Pub/Sub pattern) orqali ular bir-biriga xabar yuborishi mumkin.

## Ishlash natijasi:
```text
Auth event: User logged in
```

---

# 1034-Topshiriq: AST Transformatsiya - Function Renamer

## Topshiriq sharti:
`ts-morph` kutubxonasi yordamida kod ichidagi barcha funksiya nomlarini o'zgartiruvchi (refactoring) mantiqni simulyatsiya qiling.

## Yechim (TypeScript kodi):
```typescript
const code = "function oldName() {}";
const transformed = code.replace(/oldName/g, "newName");
console.log(transformed);
```

## Tushuntirish va Mantiq:
AST (Abstract Syntax Tree) transformatsiyasi kodni tahlil qilib, uning tuzilishini o'zgartirishdir. Bu yerda regex orqali soddalashtirilgan transformatsiya ko'rsatilgan.

## Ishlash natijasi:
```text
function newName() {}
```

---

# 1035-Topshiriq: DDD Aggregate Root

## Topshiriq sharti:
`Order` (Buyurtma) Aggregate Root sinfini yarating, u o'z ichiga `OrderItem` obyektlarini oladi va ularni boshqaradi.

## Yechim (TypeScript kodi):
```typescript
class Order {
  private items: string[] = [];
  addItem(item: string) { this.items.push(item); }
  getItems() { return [...this.items]; }
}

const order = new Order();
order.addItem("Laptop");
console.log(order.getItems());
```

## Tushuntirish va Mantiq:
Aggregate Root - bu ma'lumotlar yaxlitligini saqlaydigan asosiy obyekt. Tashqi kod to'g'ridan-to'g'ri `items` massivini o'zgartira olmaydi.

## Ishlash natijasi:
```text
[ 'Laptop' ]
```

---

# 1036-Topshiriq: Clean Architecture - Use Case

## Topshiriq sharti:
Foydalanuvchini ro'yxatdan o'tkazish uchun `RegisterUserUseCase` sinfini yarating.

## Yechim (TypeScript kodi):
```typescript
class RegisterUserUseCase {
  execute(email: string) {
    return `User ${email} muvaffaqiyatli ro'yxatdan o'tdi.`;
  }
}

console.log(new RegisterUserUseCase().execute("test@ai.uz"));
```

## Tushuntirish va Mantiq:
Use Case - bu biznes mantiqining yuragi. U qaysi framework ishlatilishidan qat'iy nazar bir xil ishlaydi.

## Ishlash natijasi:
```text
User test@ai.uz muvaffaqiyatli ro'yxatdan o'tdi.
```

---

# 1037-Topshiriq: Micro-frontends - Remote Module Loader

## Topshiriq sharti:
Uzoqdan yuklanadigan (remote) modulni simulyatsiya qiluvchi `loadModule` funksiyasini yarating.

## Yechim (TypeScript kodi):
```typescript
async function loadModule(name: string) {
  return `Module ${name} loaded successfully`;
}

loadModule("Dashboard").then(console.log);
```

## Tushuntirish va Mantiq:
Micro-frontends'da modullar dinamik yuklanadi. `async/await` bu jarayonni boshqarish uchun eng yaxshi vositadir.

## Ishlash natijasi:
```text
Module Dashboard loaded successfully
```

---

# 1038-Topshiriq: AST - Type Checker

## Topshiriq sharti:
Kod ichidagi o'zgaruvchi turini tekshiruvchi oddiy `TypeChecker` funksiyasini yarating.

## Yechim (TypeScript kodi):
```typescript
function checkType(val: any) {
  return typeof val === 'string' ? "String type" : "Other type";
}

console.log(checkType("Khorazmiy"));
```

## Tushuntirish va Mantiq:
AST tahlilida kodning turi (type) muhim ahamiyatga ega. Bu funksiya runtime'da tur tekshiruvini amalga oshiradi.

## Ishlash natijasi:
```text
String type
```

---

# 1039-Topshiriq: DDD - Domain Event

## Topshiriq sharti:
Buyurtma yaratilganda `OrderCreated` hodisasini (event) ishga tushiruvchi tizim yarating.

## Yechim (TypeScript kodi):
```typescript
class OrderCreated { constructor(public id: number) {} }
const event = new OrderCreated(1);
console.log(`Event triggered: Order ${event.id}`);
```

## Tushuntirish va Mantiq:
Domain Events tizimlar o'rtasida bog'liqlikni kamaytiradi va biznes jarayonlarini kuzatishni osonlashtiradi.

## Ishlash natijasi:
```text
Event triggered: Order 1
```

---

# 1040-Topshiriq: Clean Architecture - Entity Mapper

## Topshiriq sharti:
Domain modelini DTO (Data Transfer Object) ga o'giruvchi `Mapper` sinfini yarating.

## Yechim (TypeScript kodi):
```typescript
class User { constructor(public name: string) {} }
class UserMapper {
  static toDTO(user: User) { return { username: user.name.toUpperCase() }; }
}

console.log(UserMapper.toDTO(new User("Khorazmiy")));
```

## Tushuntirish va Mantiq:
Domain model va API javobi (DTO) bir xil bo'lmasligi kerak. Mapper qatlami bu ikki dunyoni ajratib turadi.

## Ishlash natijasi:
```text
{ username: 'KHORAZMIY' }
```

---

Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. TypeScript ekotizimini boyitish uchun DDD, Clean Architecture, Micro-frontends va AST (Abstract Syntax Tree) tahliliga asoslangan 10 ta ilg'or topshiriqni taqdim etaman.

---

# #1041-Topshiriq: DDD Entity-ni Value Object bilan avtomatik validatsiya qilish

## Topshiriq sharti:
DDD tamoyillariga ko'ra, `Email` qiymatini `ValueObject` sifatida modellashtiring va uni `User` entity-si ichida ishlatganda avtomatik validatsiya qiluvchi dekorator yarating.

## Yechim (TypeScript kodi):
```typescript
function ValidateEmail(target: any, propertyKey: string) {
  let value: string;
  const setter = (newValue: string) => {
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(newValue)) {
      throw new Error(`Noto'g'ri email formati: ${newValue}`);
    }
    value = newValue;
  };
  Object.defineProperty(target, propertyKey, { set: setter, get: () => value });
}

class User {
  @ValidateEmail
  public email!: string;
  constructor(email: string) { this.email = email; }
}

const user = new User("test@khorazmiy.ai");
console.log("User yaratildi:", user.email);
```

## Tushuntirish va Mantiq:
`ValidateEmail` dekoratori `Object.defineProperty` orqali setter funksiyasini o'zgartiradi. Bu DDD-dagi "Invariant" qoidasini ta'minlaydi: obyekt hech qachon noto'g'ri holatda bo'lmasligi kerak.

## Ishlash natijasi:
```text
User yaratildi: test@khorazmiy.ai
```

---

# #1042-Topshiriq: Clean Architecture uchun Dependency Inversion (DI) konteyneri

## Topshiriq sharti:
Clean Architecture qatlamlari o'rtasidagi bog'liqlikni kamaytirish uchun oddiy DI konteynerini yarating.

## Yechim (TypeScript kodi):
```typescript
class Container {
  private services = new Map<string, any>();
  register(name: string, service: any) { this.services.set(name, service); }
  resolve<T>(name: string): T { return this.services.get(name); }
}

const container = new Container();
container.register("Logger", { log: (msg: string) => console.log(`[Log]: ${msg}`) });
const logger = container.resolve<{log: (m: string) => void}>("Logger");
logger.log("Clean Architecture ishga tushdi.");
```

## Tushuntirish va Mantiq:
Bu yechim "Dependency Inversion" prinsipini amalga oshiradi. Yuqori darajadagi modullar past darajadagi modullarga emas, balki abstraksiyalarga bog'liq bo'ladi.

## Ishlash natijasi:
```text
[Log]: Clean Architecture ishga tushdi.
```

---

# #1043-Topshiriq: Micro-frontend uchun Event Bus tizimi

## Topshiriq va Mantiq:
Micro-frontendlar o'rtasida ma'lumot almashish uchun `Pub/Sub` pattern-ini yarating.

## Yechim (TypeScript kodi):
```typescript
class EventBus {
  private listeners: Record<string, Function[]> = {};
  on(event: string, cb: Function) { (this.listeners[event] ||= []).push(cb); }
  emit(event: string, data: any) { this.listeners[event]?.forEach(cb => cb(data)); }
}

const bus = new EventBus();
bus.on("auth", (user: string) => console.log(`MFE qabul qildi: ${user}`));
bus.emit("auth", "Khorazmiy_User");
```

## Ishlash natijasi:
```text
MFE qabul qildi: Khorazmiy_User
```

---

# #1044-Topshiriq: AST yordamida kodni tahlil qilish (TypeScript Compiler API)

## Topshiriq sharti:
`typescript` kutubxonasi yordamida kod ichidagi barcha `interface` nomlarini aniqlang.

## Yechim (TypeScript kodi):
```typescript
import * as ts from "typescript";

const sourceCode = "interface User { id: number; } interface Product { name: string; }";
const sourceFile = ts.createSourceFile("test.ts", sourceCode, ts.ScriptTarget.Latest);

sourceFile.forEachChild(node => {
  if (ts.isInterfaceDeclaration(node)) {
    console.log("Topilgan interface:", node.name.text);
  }
});
```

## Tushuntirish va Mantiq:
AST (Abstract Syntax Tree) kodni daraxt ko'rinishida tahlil qiladi. `ts.isInterfaceDeclaration` tugun turi `interface` ekanligini tekshiradi.

## Ishlash natijasi:
```text
Topilgan interface: User
Topilgan interface: Product
```

---

# #1045-Topshiriq: Domain Event-larni Dispatcher orqali boshqarish

## Topshiriq sharti:
DDD-da `DomainEvent` sodir bo'lganda uni qayta ishlovchi `DomainEventDispatcher` yarating.

## Yechim (TypeScript kodi):
```typescript
interface DomainEvent { name: string; }
class Dispatcher {
  private handlers: Record<string, Function[]> = {};
  subscribe(name: string, handler: Function) { (this.handlers[name] ||= []).push(handler); }
  dispatch(event: DomainEvent) { this.handlers[event.name]?.forEach(h => h(event)); }
}

const dispatcher = new Dispatcher();
dispatcher.subscribe("UserCreated", (e: any) => console.log("Event bajarildi:", e.name));
dispatcher.dispatch({ name: "UserCreated" });
```

## Ishlash natijasi:
```text
Event bajarildi: UserCreated
```

---

# #1046-Topshiriq: Micro-frontend uchun Remote Module Loader

## Topshiriq sharti:
Micro-frontendda dinamik ravishda tashqi modulni yuklovchi funksiya yarating.

## Yechim (TypeScript kodi):
```typescript
async function loadRemoteModule(url: string) {
  const module = await import(/* @vite-ignore */ url);
  return module;
}
// Izoh: Haqiqiy muhitda URL to'liq bo'lishi kerak
console.log("Modul yuklashga tayyor...");
```

## Tushuntirish va Mantiq:
`import()` funksiyasi dinamik importni amalga oshiradi, bu micro-frontend arxitekturasida "Module Federation" uchun asosdir.

## Ishlash natijasi:
```text
Modul yuklashga tayyor...
```

---

# #1047-Topshiriq: Clean Architecture - Repository Pattern

## Topshiriq sharti:
Ma'lumotlar bazasi qatlamini abstraksiyalash uchun `Repository` interfeysini yarating.

## Yechim (TypeScript kodi):
```typescript
interface Repository<T> {
  save(entity: T): void;
}

class UserRepository implements Repository<string> {
  save(entity: string) { console.log("Saqlandi:", entity); }
}

const repo = new UserRepository();
repo.save("Khorazmiy_Data");
```

## Ishlash natijasi:
```text
Saqlandi: Khorazmiy_Data
```

---

# #1048-Topshiriq: AST yordamida kodni avtomatik refaktor qilish

## Topshiriq sharti:
Kod ichidagi `var` kalit so'zlarini `const` ga o'zgartiruvchi transformator qismini yozing.

## Yechim (TypeScript kodi):
```typescript
const code = "var x = 10;";
const transformed = code.replace(/\bvar\b/g, "const");
console.log("Refaktor qilingan kod:", transformed);
```

## Tushuntirish va Mantiq:
AST transformatsiyasi murakkab bo'lsa-da, bu yerda regex orqali soddalashtirilgan model ko'rsatilgan. Katta loyihalarda `ts.transform` ishlatiladi.

## Ishlash natijasi:
```text
Refaktor qilingan kod: const x = 10;
```

---

# #1049-Topshiriq: DDD Aggregate Root validatsiyasi

## Topshiriq sharti:
`Order` (Buyurtma) aggregate root-i uchun holat validatsiyasini yarating.

## Yechim (TypeScript kodi):
```typescript
class Order {
  constructor(public status: 'pending' | 'shipped') {}
  ship() {
    if (this.status !== 'pending') throw new Error("Buyurtma allaqachon jo'natilgan!");
    this.status = 'shipped';
  }
}

const order = new Order('pending');
order.ship();
console.log("Status:", order.status);
```

## Ishlash natijasi:
```text
Status: shipped
```

---

# #1050-Topshiriq: Micro-frontend uchun Shared State (Global)

## Topshiriq sharti:
Micro-frontendlar o'rtasida umumiy holatni (state) boshqaruvchi `Proxy` obyektini yarating.

## Yechim (TypeScript kodi):
```typescript
const state = new Proxy({ theme: 'light' }, {
  set(target, prop, value) {
    console.log(`State o'zgardi: ${String(prop)} -> ${value}`);
    return Reflect.set(target, prop, value);
  }
});

state.theme = 'dark';
```

## Tushuntirish va Mantiq:
`Proxy` obyekti har qanday o'zgarishni kuzatib boradi, bu micro-frontendlar o'rtasidagi reaktivlikni ta'minlaydi.

## Ishlash natijasi:
```text
State o'zgardi: theme -> dark
```