# 151-Topshiriq: Function Declaration vs Function Expression

## Topshiriq sharti:
Funksiya deklaratsiyasi (`function foo() {}`) va funksiya ifodasi (`const foo = function() {}`) o'rtasidagi farqlarni va hoisting ta'sirini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function testFunctionCreation(): void {
  // 1. Function Declaration e'lon qilinishidan oldin bemalol chaqiriladi (hoisting tufayli)
  console.log("Declaratsiyadan oldin chaqiruv:", declaredFunc());

  function declaredFunc(): string {
    return "Men Function Declarationman!";
  }

  // 2. Function Expression esa o'zgaruvchi qoidasiga bo'ysunadi (TDZ / hoisting yo'q)
  try {
    // @ts-ignore
    console.log("Expressiondan oldin:", expressedFunc());
  } catch (err: any) {
    console.log("Xatolik ushlandi:", err.name);
  }

  const expressedFunc = function(): string {
    return "Men Function Expressionman!";
  };

  console.log("E'lon qilingandan so'ng chaqiruv:", expressedFunc());
}

testFunctionCreation();
```

## Tushuntirish va Mantiq:
1. `Function Declaration` butun tanasi bilan birga ko'rinish sohasining eng yuqorisiga ko'tariladi (hoisting), shu bois uni faylning istalgan joyidan chaqirish mumkin.
2. `Function Expression` esa o'zgaruvchiga funksiya o'zlashtirishdir. U faqat kod ijrosi shu qatorga yetib kelgandagina xotirada yaratiladi.
3. Zamonaviy TypeScriptda ko'proq ifodalar (`const fn = () => {}`) ishlatiladi, chunki ular o'zgarmaslikni ta'minlaydi va tasodifiy qayta yozilishdan saqlaydi.

## Ishlash natijasi:
```text
Declaratsiyadan oldin chaqiruv: Men Function Declarationman!
Xatolik ushlandi: ReferenceError
E'lon qilingandan so'ng chaqiruv: Men Function Expressionman!
```


# 152-Topshiriq: Funksiya deklaratsiyasining to'liq hoisting bo'lish xususiyati

## Topshiriq sharti:
Bir nechta o'zaro bir-birini chaqiruvchi deklaratsiyalangan funksiyalarning qanday tartibda yozilishidan qat'iy nazar ishlashini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function runMutuallyRecursive(): void {
  console.log("4 juftmi:", isEven(4));
  console.log("5 juftmi:", isEven(5));

  // Funksiyalar pastda e'lon qilingan bo'lsa ham ishlayveradi
  function isEven(n: number): boolean {
    if (n === 0) return true;
    return isOdd(n - 1);
  }

  function isOdd(n: number): boolean {
    if (n === 0) return false;
    return isEven(n - 1);
  }
}

runMutuallyRecursive();
```

## Tushuntirish va Mantiq:
1. Bir-biriga bog'liq (mutually recursive) funksiyalarni yozishda hoisting juda qulay.
2. Dvigatel birinchi bosqichda (Creation phase) barcha funksiya deklaratsiyalarini xotiraga yuklab oladi.
3. Ikkinchi bosqichda (Execution phase) kod bajariladi, shuning uchun chaqiruv tartibi xatolik bermaydi.

## Ishlash natijasi:
```text
4 juftmi: true
5 juftmi: false
```


# 153-Topshiriq: Arrow funksiyalar (Strelkali funksiyalar) va ixcham sintaksis

## Topshiriq sharti:
Arrow funksiyalarning qisqa return sintaksisi (`() => expr`) va obyekt qaytarishda qavs bilan o'rash (`() => ({})`) qoidasini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function testArrowSyntax(): void {
  // Bitta parametr va bitta ifoda: jingalak qavssiz va return siz
  const square = (x: number) => x * x;
  console.log("square(6):", square(6));

  // Obyekt qaytarishda qavs () bilan o'rash shart, aks holda blok deb o'ylaydi
  const createUser = (id: number, username: string) => ({
    id,
    username,
    createdAt: "2026-11-08"
  });

  const newUser = createUser(101, "jasur_dev");
  console.log("Yaratilgan foydalanuvchi:", newUser);
}

testArrowSyntax();
```

## Tushuntirish va Mantiq:
1. Arrow funksiyalar ES6 da kiritilgan bo'lib, funksiyalarni ixcham yozish imkonini beradi.
2. Agar bitta ifoda bo'lsa, `{}` va `return` so'zlarini tashlab ketish mumkin (implicit return).
3. Obyekt literalini qaytarishda jingalak qavs funksiya bloki bilan adashtirilmasligi uchun obyekt yumaloq qavsga olinadi: `({ a: 1 })`.

## Ishlash natijasi:
```text
square(6): 36
Yaratilgan foydalanuvchi: { id: 101, username: 'jasur_dev', createdAt: '2026-11-08' }
```


# 154-Topshiriq: Arrow funksiyalarda leksik 'this' va an'anaviy funksiyadan farqi

## Topshiriq sharti:
Obyekt metodlari ichidagi timer callbacklarida an'anaviy funksiya `this` ni yo'qotishini va arrow funksiya leksik `this` orqali muammoni qanday yechishini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
class Counter {
  count = 0;

  startWithArrow(): void {
    // Arrow funksiya o'zining shaxsiy 'this' iga ega emas, balki tashqi klass 'this' ini oladi
    const increment = () => {
      this.count++;
      console.log("Arrow orqali count:", this.count);
    };
    increment();
  }

  startWithTraditional(): void {
    const that = this; // Qadimgi noqulay usul
    function traditional(this: any) {
      // Bu yerda this Counter obyekti emas, balki global yoki undefined bo'ladi!
      that.count++;
      console.log("Tashqi that orqali count:", that.count);
    }
    traditional();
  }
}

const c = new Counter();
c.startWithArrow();
c.startWithTraditional();
```

## Tushuntirish va Mantiq:
1. Oddiy funksiyalarda `this` qanday e'lon qilinganiga emas, balki qanday chaqirilganiga bog'liq bo'ladi (dinamik binding).
2. Arrow funksiyalarda esa `this` mutlaqo mavjud emas: u o'zi e'lon qilingan tashqi leksik kontekstdan `this` ni oladi (lexical this).
3. Shu bois event listenerlar va callbacklarda `this` kontekstini yo'qotmaslik uchun arrow funksiyalar eng ideal tanlovdir.

## Ishlash natijasi:
```text
Arrow orqali count: 1
Tashqi that orqali count: 2
```


# 155-Topshiriq: Arrow funksiyalarning cheklovlari: arguments yo'qligi va konstruktor bo'lolmasligi

## Topshiriq sharti:
Arrow funksiyalarda `arguments` obyekti yo'qligini va ularni `new` orqali chaqirib bo'lmasligini isbotlang.

## Yechim (JS yoki TS kodi):
```typescript
function testArrowRestrictions(): void {
  const normalFn = function() {
    return arguments.length;
  };
  console.log("Oddiy funksiyada arguments.length:", normalFn(1, 2, 3));

  const arrowFn = (...args: any[]) => {
    // Arrow funksiyada arguments yo'q, uning o'rniga rest parametrlar ishlatiladi
    return args.length;
  };
  console.log("Arrow funksiyada rest args.length:", arrowFn(1, 2, 3));

  // new bilan chaqirishga urinish
  try {
    // @ts-ignore
    const instance = new arrowFn();
  } catch (err: any) {
    console.log("new arrowFn() xatoligi:", err.name);
  }
}

testArrowRestrictions();
```

## Tushuntirish va Mantiq:
1. Arrow funksiyalar o'zining shaxsiy `arguments` obyektiga ega emas. Ular tashqi sohadagi `arguments` ni ko'rishi mumkin, shuning uchun rest `...args` ishlatiladi.
2. Arrow funksiyalarda `[[Construct]]` ichki metodi va `prototype` xususiyati bo'lmaydi.
3. Shu sababli ularni `new` kalit so'zi bilan konstruktor sifatida chaqirib bo'lmaydi (TypeError tashlaydi).

## Ishlash natijasi:
```text
Oddiy funksiyada arguments.length: 3
Arrow funksiyada rest args.length: 3
new arrowFn() xatoligi: TypeError
```


# 156-Topshiriq: Standart (Default) parametrlar va ularning baholanish vaqti

## Topshiriq sharti:
Funksiyaning default parametrlari har bir chaqiruv paytida yangitdan hisoblanishini (dinamik evaluation) namoyish eting.

## Yechim (JS yoki TS kodi):
```typescript
let callCounter = 0;
function getDefaultId(): number {
  return ++callCounter;
}

function registerUser(name: string, id: number = getDefaultId()): void {
  console.log(`Foydalanuvchi: ${name}, ID: ${id}`);
}

registerUser("Ali");
registerUser("Vali");
registerUser("Sami", 999); // Berilgan qiymat getDefaultId ni chaqirmaydi
registerUser("Gani");
```

## Tushuntirish va Mantiq:
1. Python kabi tillardan farqli ravishda, JavaScriptda default parametrlar funksiya e'lon qilinganda emas, balki funksiya chaqirilgan vaqtda (runtime) baholanadi.
2. Agar parametr uchun argument uzatilsa yoki `undefined` dan boshqa qiymat berilsa, default funksiya umuman chaqirilmaydi.
3. Bu har safar yangi sana, yangi ID yoki yangi bo'sh massiv hosil qilishda xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
Foydalanuvchi: Ali, ID: 1
Foydalanuvchi: Vali, ID: 2
Foydalanuvchi: Sami, ID: 999
Foydalanuvchi: Gani, ID: 3
```


# 157-Topshiriq: Default parametrlar oldingi parametrlarga murojaat qilishi

## Topshiriq sharti:
Keyingi standart parametr oldingi parametr qiymatiga asoslanib hisoblanishini ko'rsatuvchi to'rtburchak yuzi va perimetri funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function createBox(width: number, height: number = width, label: string = `${width}x${height}`): void {
  console.log(`Quti: Kenglik = ${width}, Balandlik = ${height}, Belgisi = '${label}'`);
}

createBox(10); // Kvadrat (height = width = 10)
createBox(20, 30); // To'rtburchak
createBox(15, 15, "Maxsus Quti");
```

## Tushuntirish va Mantiq:
1. Default parametrlar chapdan o'ngga qarab o'z ko'rinish sohasida (parameter scope) initsializatsiya qilinadi.
2. Shuning uchun o'ng tomonda turgan parametr o'zidan chapda joylashgan ixtiyoriy parametr qiymatini o'qiy oladi.
3. Biroq teskarisi mumkin emas (`width = height` deb yozilsa TDZ xatosi yuzaga keladi).

## Ishlash natijasi:
```text
Quti: Kenglik = 10, Balandlik = 10, Belgisi = '10x10'
Quti: Kenglik = 20, Balandlik = 30, Belgisi = '20x30'
Quti: Kenglik = 15, Balandlik = 15, Belgisi = 'Maxsus Quti'
```


# 158-Topshiriq: Rest parametrlar (...args): Moslashuvchan argumentlar soni

## Topshiriq sharti:
Ixtiyoriy sondagi raqamlarni qabul qilib ularning o'rtacha arifmetigini hisoblovchi funksiyani rest parametrlar orqali yozing.

## Yechim (JS yoki TS kodi):
```typescript
function calculateAverage(prefix: string, ...numbers: number[]): string {
  if (numbers.length === 0) return `${prefix}: 0`;

  const sum = numbers.reduce((acc, curr) => acc + curr, 0);
  const avg = sum / numbers.length;
  return `${prefix}: ${avg.toFixed(2)}`;
}

console.log(calculateAverage("Test 1", 10, 20, 30));
console.log(calculateAverage("Test 2", 5, 15, 25, 35, 45));
console.log(calculateAverage("Bo'sh"));
```

## Tushuntirish va Mantiq:
1. Rest operatori (`...numbers`) barcha qolgan argumentlarni bitta haqiqiy massivga yig'adi.
2. Funksiya parametrlarida rest faqat eng oxirgi o'rinda turishi shart (`(a, ...b)` to'g'ri, ammo `(...a, b)` sintaktik xato).
3. Qadimgi `arguments` dan farqli ravishda, u haqiqiy `Array` nusxasi bo'lib, unga barcha metodlar (`reduce`, `map`, `filter`) bevosita ishlaydi.

## Ishlash natijasi:
```text
Test 1: 20.00
Test 2: 25.00
Bo'sh: 0
```


# 159-Topshiriq: Rest parametrlar vs Eski 'arguments' obyekti

## Topshiriq sharti:
Eski `arguments` obyekti nima uchun qulay emasligini va rest parametrlarga o'tish afzalliklarini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function compareRestAndArguments(this: any, ...modernArgs: number[]): void {
  // arguments - bu massivsimon (array-like) obyekt, unda massiv metodlari yo'q!
  // @ts-ignore
  console.log("arguments turi:", typeof arguments, "| Array.isArray:", Array.isArray(arguments));

  // arguments da map yoki reduce chaqirish uchun avval uni massivga o'tkazish kerak bo'lgan
  // @ts-ignore
  const legacyArray = Array.prototype.slice.call(arguments);
  console.log("Eski usulda massivga o'tkazish:", legacyArray);

  // Rest parametr esa tayyor massiv:
  console.log("modernArgs turi:", typeof modernArgs, "| Array.isArray:", Array.isArray(modernArgs));
  console.log("Zamonaviy to'g'ridan-to'g'ri map:", modernArgs.map((x) => x * 10));
}

compareRestAndArguments(1, 2, 3);
```

## Tushuntirish va Mantiq:
1. `arguments` faqat `length` va raqamli indekslarga ega massivsimon obyektdir (`Array.isArray(arguments) === false`).
2. Unda `map`, `filter` kabi zamonaviy funksiyalar mavjud emas, ularni ishlatish uchun `Array.from()` yoki `slice.call()` kerak bo'lardi.
3. Rest parametrlar toza, turlashtirilgan va qulay massiv yaratadi.

## Ishlash natijasi:
```text
arguments turi: object | Array.isArray: false
Eski usulda massivga o'tkazish: [ 1, 2, 3 ]
modernArgs turi: object | Array.isArray: true
Zamonaviy to'g'ridan-to'g'ri map: [ 10, 20, 30 ]
```


# 160-Topshiriq: Spread operatori funksiya argumentlarida: fn(...items)

## Topshiriq sharti:
Massivdagi ma'lumotlarni alohida argumentlar sifatida qabul qiluvchi funksiyaga spread operatori yordamida uzatishni namoyish eting.

## Yechim (JS yoki TS kodi):
```typescript
function sendEmail(to: string, subject: string, priority: number): void {
  console.log(`Xat yuborildi: Kimga: ${to} | Mavzu: '${subject}' | Muhimlik: ${priority}`);
}

const emailDetails: [string, string, number] = ["support@startup.uz", "Tizim yangilanishi", 1];

// Funksiyaga massivni yoyib (spread) yuboramiz
sendEmail(...emailDetails);
```

## Tushuntirish va Mantiq:
1. Spread operatori (`...arr`) funksiya chaqirilayotganda massivni alohida argumentlar ketma-ketligiga yoyib beradi.
2. Bu `fn.apply(null, arr)` qadimgi usulining ancha sodda va o'qilishi oson muqobilidir.
3. TypeScript tuple turlari bilan birlashganda funksiya parametrlarining turlarini qat'iy tekshiradi.

## Ishlash natijasi:
```text
Xat yuborildi: Kimga: support@startup.uz | Mavzu: 'Tizim yangilanishi' | Muhimlik: 1
```


# 161-Topshiriq: Function.prototype.call: Kontekstni qo'lda belgilab chaqirish

## Topshiriq sharti:
`call` metodi orqali obyekt metodini boshqa begona obyekt ustida bajarishni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
interface UserIdentity {
  name: string;
  role: string;
}

function introduce(this: UserIdentity, greeting: string): void {
  console.log(`${greeting}, men ${this.name}, lavozimim: ${this.role}`);
}

const admin = { name: "Farhod", role: "Bosh administrator" };
const guest = { name: "Mehmon_01", role: "Tashrif buyuruvchi" };

// introduce funksiyasini turli obyektlar kontekstida chaqiramiz
introduce.call(admin, "Assalomu alaykum");
introduce.call(guest, "Xush kelibsiz");
```

## Tushuntirish va Mantiq:
1. `fn.call(thisArg, arg1, arg2, ...)` funksiyani birinchi argumentda ko'rsatilgan `this` konteksti bilan zudlik bilan ishga tushiradi.
2. Qolgan argumentlar vergul bilan alohida beriladi.
3. Bu biror obyekt metodini boshqa obyektga 'qarzga berish' (method borrowing) imkonini beradi.

## Ishlash natijasi:
```text
Assalomu alaykum, men Farhod, lavozimim: Bosh administrator
Xush kelibsiz, men Mehmon_01, lavozimim: Tashrif buyuruvchi
```


# 162-Topshiriq: Function.prototype.apply: Argumentlar massivi bilan chaqirish

## Topshiriq sharti:
`apply` metodi orqali parametrlar soni oldindan noma'lum bo'lgan massivni funksiyaga uzatishni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function formatReport(this: { title: string }, ...sections: string[]): void {
  console.log(`=== ${this.title} ===`);
  sections.forEach((sec, idx) => {
    console.log(`${idx + 1}. ${sec}`);
  });
}

const reportContext = { title: "Choraklik Moliya Hisoboti" };
const sectionList = ["Kirimlar tahlili", "Chiqimlar balansi", "Soliq to'lovlari"];

// apply ikkinchi parametr sifatida argumentlar massivini oladi
formatReport.apply(reportContext, sectionList);
```

## Tushuntirish va Mantiq:
1. `fn.apply(thisArg, [argsArray])` xuddi `call` kabi ishlaydi, faqat argumentlarni massiv ko'rinishida qabul qiladi.
2. Zamonaviy JavaScriptda spread operatori paydo bo'lgach (`fn.call(thisArg, ...sectionList)`), `apply` ga bo'lgan ehtiyoj kamaydi, ammo u mavjud kod bazalarida muhim o'rin tutadi.

## Ishlash natijasi:
```text
=== Choraklik Moliya Hisoboti ===
1. Kirimlar tahlili
2. Chiqimlar balansi
3. Soliq to'lovlari
```


# 163-Topshiriq: Function.prototype.bind: Doimiy kontekstga ega yangi funksiya yaratish

## Topshiriq sharti:
`bind` metodi orqali obyektdan ajratib olingan metodning `this` kontekstini saqlab qoluvchi yangi funksiya hosil qiling.

## Yechim (JS yoki TS kodi):
```typescript
class UserSessionManager {
  constructor(public activeUser: string) {}

  printSession(): void {
    console.log("Faol sessiya egasi:", this.activeUser);
  }
}

const manager = new UserSessionManager("Dilnoza");

// Kontekstni yo'qotish xavfi:
const detachedMethod = manager.printSession;
try {
  detachedMethod(); // Xatolik yoki undefined
} catch (err: any) {
  console.log("Kontekstsiz chaqiruvda xatolik:", err.name);
}

// bind orqali xavfsiz bog'lash
const boundMethod = manager.printSession.bind(manager);
boundMethod(); // Mukammal ishlaydi!
```

## Tushuntirish va Mantiq:
1. `bind(thisArg, ...args)` funksiyani darhol bajarmaydi.
2. Buning o'rniga u `this` konteksti belgilangan obyektga doimiy qilib biriktirilgan (bound) yangi funksiya qaytaradi.
3. Yangi funksiya keyinchalik qayerda va qanday chaqirilishidan qat'iy nazar o'zining `this` ini yo'qotmaydi.
4. Bu hodisalar tinglovchilari (event listeners) va setTimeout bilan ishlashda eng ishonchli usuldir.

## Ishlash natijasi:
```text
Kontekstsiz chaqiruvda xatolik: TypeError
Faol sessiya egasi: Dilnoza
```


# 164-Topshiriq: Partial Application (Qisman qo'llash) bind orqali

## Topshiriq sharti:
`bind` yordamida funksiyaning dastlabki argumentlarini oldindan biriktirib yangi ixtisoslashgan funksiya hosil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function multiply(a: number, b: number): number {
  return a * b;
}

// 'this' muhim emas (null), lekin 1-argument 2 ga teng qilib 'qotirildi'
const double = multiply.bind(null, 2);
// 1-argument 10 ga teng qilib qotirildi
const multiplyByTen = multiply.bind(null, 10);

console.log("double(5):", double(5)); // 2 * 5 = 10
console.log("double(12):", double(12)); // 2 * 12 = 24
console.log("multiplyByTen(7):", multiplyByTen(7)); // 10 * 7 = 70
```

## Tushuntirish va Mantiq:
1. `bind` nafaqat `this` ni, balki argumentlarni ham oldindan biriktirish imkoniyatiga ega.
2. Bu jarayon funksional dasturlashda Partial Application (qisman parametrli funksiya yaratish) deb ataladi.
3. Keng qamrovli umumiy funksiyalardan tor doiradagi maxsus funksiyalar yasashda juda qulay.

## Ishlash natijasi:
```text
double(5): 10
double(12): 24
multiplyByTen(7): 70
```


# 165-Topshiriq: Lexical Scope va Scope Chain (Ko'rinish sohalari zanjiri)

## Topshiriq sharti:
Ichma-ich kiritilgan funksiyalarning tashqi sohalardagi o'zgaruvchilarni qanday qidirib topishini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
const globalLevel = "Global daraja";

function levelOne(): void {
  const outerLevel = "1-daraja";

  function levelTwo(): void {
    const innerLevel = "2-daraja";

    function levelThree(): void {
      // Dvigatel o'zgaruvchini avval levelThree dan, so'ng levelTwo, levelOne va nihoyat globaldan qidiradi
      console.log(`Qidiruv natijasi:\n- ${innerLevel}\n- ${outerLevel}\n- ${globalLevel}`);
    }

    levelThree();
  }

  levelTwo();
}

levelOne();
```

## Tushuntirish va Mantiq:
1. JavaScriptda ko'rinish sohasi leksik (statik) xarakterga ega: soha funksiyaning qayerda chaqirilganiga emas, aynan kodning qayerida yozilganiga qarab belgilanadi.
2. Har bir ichki soha o'zining tashqi ota sohalariga kirish huquqiga ega bo'lib, bu Scope Chain (zanjir) deb ataladi.
3. Tashqi soha esa hech qachon ichki sohadagi o'zgaruvchilarni ko'ra olmaydi.

## Ishlash natijasi:
```text
Qidiruv natijasi:
- 2-daraja
- 1-daraja
- Global daraja
```


# 166-Topshiriq: Variable Shadowing (O'zgaruvchini soyalash)

## Topshiriq sharti:
Ichki sohadagi o'zgaruvchi tashqi sohadagi bir xil nomli o'zgaruvchini qanday qilib to'sib qo'yishini namoyish eting.

## Yechim (JS yoki TS kodi):
```typescript
let role = "Foydalanuvchi";

function authenticate(): void {
  // Tashqi role soyalanadi
  let role = "Moderator";
  console.log("Funksiya ichida role:", role);

  if (true) {
    let role = "SuperAdmin";
    console.log("Blok ichida role:", role);
  }

  console.log("Blokdan keyin funksiya ichida:", role);
}

authenticate();
console.log("Global miqyosda role:", role);
```

## Tushuntirish va Mantiq:
1. Bir xil nomli o'zgaruvchi ichki sohada qayta e'lon qilinsa, dvigatel eng yaqin sohadagi o'zgaruvchini oladi. Bu 'Variable Shadowing' deyiladi.
2. Ichki soha tugashi bilanoq tashqi sohadagi asl qiymat o'z kuchini qayta tiklaydi.
3. Soyalash tasodifiy mantiqiy xatolarga olib kelmasligi uchun imkon qadar o'zgaruvchilarga betakror nomlar berish tavsiya qilinadi.

## Ishlash natijasi:
```text
Funksiya ichida role: Moderator
Blok ichida role: SuperAdmin
Blokdan keyin funksiya ichida: Moderator
Global miqyosda role: Foydalanuvchi
```


# 167-Topshiriq: Closure (Yopiq soha): Asosiy tushuncha va xotirada saqlanish

## Topshiriq sharti:
Tashqi funksiya bajarilib bo'lgandan keyin ham uning o'zgaruvchilarini xotirada eslab qoluvchi klassik Closure yaratishni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function makeGreeting(greetingWord: string) {
  // greetingWord tashqi funksiya leksik muhitida saqlanadi
  return function(userName: string): string {
    return `${greetingWord}, ${userName}!`;
  };
}

// Tashqi funksiya bajarildi va tugadi
const uzbekGreeter = makeGreeting("Assalomu alaykum");
const englishGreeter = makeGreeting("Hello");

// Ammo ichki funksiya o'zgaruvchini eslab qolgan:
console.log(uzbekGreeter("Anvar"));
console.log(uzbekGreeter("Shahlo"));
console.log(englishGreeter("John"));
```

## Tushuntirish va Mantiq:
1. Closure (yopiq soha) - bu funksiya va u e'lon qilingan paytdagi leksik muhitning (Lexical Environment) birikmasidir.
2. Tashqi funksiya o'z ishini tugatib, call stackdan chiqib ketsa ham, ichki funksiya uning o'zgaruvchilariga havola saqlab qoladi.
3. Garbage Collector bu o'zgaruvchilarni o'chirmaydi, chunki ularga hali ham faol havola mavjud.

## Ishlash natijasi:
```text
Assalomu alaykum, Anvar!
Assalomu alaykum, Shahlo!
Hello, John!
```


# 168-Topshiriq: Closure orqali Private State (Xususiy holat) va Inkapsulyatsiya

## Topshiriq sharti:
Closure yordamida tashqaridan to'g'ridan-to'g'ri o'zgartirib bo'lmaydigan xavfsiz hisoblagich (Counter) obyektini yarating.

## Yechim (JS yoki TS kodi):
```typescript
function createSecureCounter(initialValue: number = 0) {
  // privateValue tashqaridan to'g'ridan-to'g'ri ko'rinmaydi
  let privateValue = initialValue;

  return {
    increment(): number {
      privateValue += 1;
      return privateValue;
    },
    decrement(): number {
      privateValue -= 1;
      return privateValue;
    },
    getValue(): number {
      return privateValue;
    }
  };
}

const counterA = createSecureCounter(10);
console.log("increment:", counterA.increment());
console.log("increment:", counterA.increment());
console.log("decrement:", counterA.decrement());
console.log("Joriy qiymat:", counterA.getValue());

// To'g'ridan-to'g'ri o'zgartirishga urinish
// @ts-ignore
console.log("Tashqaridan privateValue:", counterA.privateValue); // undefined
```

## Tushuntirish va Mantiq:
1. JavaScriptda ES klasslarining private maydonlari (`#field`) paydo bo'lgunga qadar inkapsulyatsiya faqat closure yordamida amalga oshirilgan.
2. `privateValue` o'zgaruvchisi faqat `increment`, `decrement` va `getValue` metodlari orqaligina o'zgarishi mumkin.
3. Bu holat ma'lumotlarning buzilishi va ruxsatsiz o'zgartirilishidan to'liq himoya qiladi.

## Ishlash natijasi:
```text
increment: 11
increment: 12
decrement: 11
Joriy qiymat: 11
Tashqaridan privateValue: undefined
```


# 169-Topshiriq: Closure va Sikl: var vs let ning asinxron callbacklardagi mashhur xatosi

## Topshiriq sharti:
`for` siklida `var` va `let` bilan `setTimeout` chaqirilganda qanday natijalar bo'lishini va sababini tushuntirib bering.

## Yechim (JS yoki TS kodi):
```typescript
function testLoopClosure(): void {
  console.log("--- var bilan (bitta umumiy o'zgaruvchi) ---");
  for (var i = 0; i < 3; i++) {
    // Har bir callback bitta umumiy 'i' ga havola qiladi
    setTimeout(() => {
      console.log("var i natijasi:", i);
    }, 10);
  }

  console.log("--- let bilan (har bir qadamda yangi blok sohasi) ---");
  for (let j = 0; j < 3; j++) {
    // 'let' har bir iteratsiya uchun yangi soha va alohida closure yaratadi
    setTimeout(() => {
      console.log("let j natijasi:", j);
    }, 20);
  }
}

testLoopClosure();
```

## Tushuntirish va Mantiq:
1. `var` funksiya sohasiga ega bo'lgani sababli, butun sikl uchun yagona bitta `i` o'zgaruvchisi mavjud bo'ladi. Sikl tugaganda uning qiymati `3` bo'ladi va asinxron callbacklar ishlaganda barchasi `3` ni ko'radi.
2. `let` esa blok sohasiga ega: har bir iteratsiyada yangi o'zgaruvchi katakchasi yaratiladi va callback o'sha qadamdagi qiymatni (`0`, `1`, `2`) o'z closuriga muhrlab oladi.
3. Bu JavaScript bo'yicha intervyularda eng ko'p so'raladigan savollardan biridir.

## Ishlash natijasi:
```text
--- var bilan (bitta umumiy o'zgaruvchi) ---
--- let bilan (har bir qadamda yangi blok sohasi) ---
var i natijasi: 3
var i natijasi: 3
var i natijasi: 3
let j natijasi: 0
let j natijasi: 1
let j natijasi: 2
```


# 170-Topshiriq: IIFE (Immediately Invoked Function Expression) va Modulli dasturlash

## Topshiriq sharti:
IIFE sintaksisi yordamida global sohani ifloslantirmasdan bir martalik initsializatsiya modulini yarating.

## Yechim (JS yoki TS kodi):
```typescript
const DatabaseModule = (function() {
  // Xususiy o'zgaruvchilar va konfiguratsiya
  const connectionString = "postgres://admin:secret@localhost:5432/main_db";
  let isConnected = false;

  function log(msg: string) {
    console.log(`[DB Log]: ${msg}`);
  }

  // Ommaviy API qaytariladi
  return {
    connect() {
      isConnected = true;
      log("Baza bilan aloqa o'rnatildi.");
    },
    status() {
      return isConnected ? "Ulanish faol" : "Ulanmagan";
    }
  };
})();

console.log("Dastlabki holat:", DatabaseModule.status());
DatabaseModule.connect();
console.log("Keyingi holat:", DatabaseModule.status());
```

## Tushuntirish va Mantiq:
1. IIFE `(function() { ... })()` e'lon qilinishi bilanoq darhol ishga tushadigan funksiya ifodasidir.
2. U o'z ichida mustaqil soha yaratadi, undagi o'zgaruvchilar global nomlar fazosini (global namespace) ifloslantirmaydi.
3. ES modullari (`import`/`export`) paydo bo'lishidan oldin kutubxonalar (masalan, jQuery) aynan IIFE Module Pattern orqali qurilgan.

## Ishlash natijasi:
```text
Dastlabki holat: Ulanmagan
[DB Log]: Baza bilan aloqa o'rnatildi.
Keyingi holat: Ulanish faol
```


# 171-Topshiriq: Memoization naqshi: Hisoblash natijalarini keshlovchi closure

## Topshiriq sharti:
Murakkab matematik hisoblash natijalarini keshlab oluvchi universal `memoize` funksiyasini closure orqali yozing.

## Yechim (JS yoki TS kodi):
```typescript
function memoize<T extends (...args: any[]) => any>(fn: T): T {
  const cache = new Map<string, ReturnType<T>>();

  return function(this: any, ...args: any[]): ReturnType<T> {
    const key = JSON.stringify(args);

    if (cache.has(key)) {
      console.log(`[Keshdan olindi] Kalit: ${key}`);
      return cache.get(key)!;
    }

    console.log(`[Yangi hisoblash] Kalit: ${key}`);
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  } as T;
}

const slowMultiplier = (a: number, b: number) => a * b;
const memoizedMultiply = memoize(slowMultiplier);

console.log("1-chaqiruv:", memoizedMultiply(5, 10));
console.log("2-chaqiruv:", memoizedMultiply(5, 10)); // Keshdan olinadi
console.log("3-chaqiruv:", memoizedMultiply(2, 4));
```

## Tushuntirish va Mantiq:
1. Memoization funksional dasturlashdagi eng muhim optimallashtirish naqshlaridan biridir.
2. Funksiyaning ichki `cache` xaritasi closure da saqlanadi va tashqaridan unga to'g'ridan-to'g'ri kirib bo'lmaydi.
3. Agar ayni bir xil argumentlar yana uzatilsa, og'ir hisoblash qayta bajarilmasdan keshdagi tayyor natija qaytariladi.

## Ishlash natijasi:
```text
[Yangi hisoblash] Kalit: [5,10]
1-chaqiruv: 50
[Keshdan olindi] Kalit: [5,10]
2-chaqiruv: 50
[Yangi hisoblash] Kalit: [2,4]
3-chaqiruv: 8
```


# 172-Topshiriq: Fibonachchi ketma-ketligini Memoization orqali tezkor hisoblash

## Topshiriq sharti:
Rekursiv Fibonachchi funksiyasining `O(2^N)` murakkabligini memoization yordamida `O(N)` ga tushiring.

## Yechim (JS yoki TS kodi):
```typescript
function getFibonacciMemo() {
  const memo: Record<number, number> = { 0: 0, 1: 1 };

  function fib(n: number): number {
    if (n in memo) {
      return memo[n];
    }
    memo[n] = fib(n - 1) + fib(n - 2);
    return memo[n];
  }

  return fib;
}

const fastFib = getFibonacciMemo();

console.log("fib(10):", fastFib(10));
console.log("fib(40):", fastFib(40));
```

## Tushuntirish va Mantiq:
1. Oddiy rekursiv Fibonachchi juda ko'p bir xil oraliq qadamlarni takroran hisoblaydi va `O(2^N)` ko'rsatkichli vaqt oladi (`fib(40)` soniyalab qotib qoladi).
2. Closure dagi `memo` lug'ati orqali har bir son faqat bir marta hisoblanadi.
3. Natijada vaqt sarfi chiziqli `O(N)` ga tushadi va `fib(40)` darhol mikrosekundda hisoblanadi.

## Ishlash natijasi:
```text
fib(10): 55
fib(40): 102334155
```


# 173-Topshiriq: Currying (Karring): Funksiyani zanjirli chaqiruvga aylantirish

## Topshiriq sharti:
Uchta sonni qo'shuvchi oddiy funksiyani `add(a)(b)(c)` ko'rinishida chaqiriladigan karring qilingan shaklga keltiring.

## Yechim (JS yoki TS kodi):
```typescript
// Oddiy funksiya: add(1, 2, 3)
// Karring qilingan: add(1)(2)(3)
function curryAdd(a: number) {
  return function(b: number) {
    return function(c: number) {
      return a + b + c;
    };
  };
}

// Qisqa arrow shakli
const arrowCurry = (a: number) => (b: number) => (c: number) => a + b + c;

console.log("curryAdd(1)(2)(3):", curryAdd(1)(2)(3));
console.log("arrowCurry(10)(20)(30):", arrowCurry(10)(20)(30));

// Bosqichma-bosqich qo'llash
const add10 = arrowCurry(10);
const add10And20 = add10(20);
console.log("add10And20(5):", add10And20(5));
```

## Tushuntirish va Mantiq:
1. Karring (Currying) ko'p parametrli funksiyani har safar faqat bitta parametr qabul qiluvchi zanjirli funksiyalarga ajratish usulidir.
2. Har bir qadamda yangi closure hosil bo'ladi va o'zgaruvchilar yakuniy natijaga qadar saqlanib boradi.
3. Bu uslub konfiguratsiyalarni bosqichma-bosqich boyitishda va funksiyalarni qayta ishlatishda juda qo'l keladi.

## Ishlash natijasi:
```text
curryAdd(1)(2)(3): 6
arrowCurry(10)(20)(30): 60
add10And20(5): 35
```


# 174-Topshiriq: Universal Curry yordamchi funksiyasini yozish

## Topshiriq sharti:
Har qanday ixtiyoriy ko'p argumentli funksiyani avtomatik karring qiluvchi universal `curry(fn)` utilitasini yarating.

## Yechim (JS yoki TS kodi):
```typescript
function autoCurry(fn: Function) {
  return function curried(this: any, ...args: any[]): any {
    // Agar yetarli argumentlar to'plangan bo'lsa, asl funksiyani chaqiramiz
    if (args.length >= fn.length) {
      return fn.apply(this, args);
    }
    // Aks holda qolgan argumentlarni to'plash uchun yangi funksiya qaytaramiz
    return function(this: any, ...nextArgs: any[]) {
      return curried.apply(this, args.concat(nextArgs));
    };
  };
}

function calculateVolume(length: number, width: number, height: number): number {
  return length * width * height;
}

const curriedVolume = autoCurry(calculateVolume);

console.log("1. Bir vaqtda:", curriedVolume(2, 3, 4));
console.log("2. Alohida:", curriedVolume(2)(3)(4));
console.log("3. Aralash:", curriedVolume(2, 3)(4));
```

## Tushuntirish va Mantiq:
1. `fn.length` funksiya kutayotgan parametrlar sonini (arilligini) bildiradi.
2. Agar qabul qilingan `args.length >= fn.length` bo'lsa, barcha argumentlar yetarli deb topilib, funksiya bajariladi.
3. Agar kam bo'lsa, rekursiv ravishda argumentlarni yig'ishda davom etadi. Bu Ramda va Lodash kutubxonalarining asosiy tamoyilidir.

## Ishlash natijasi:
```text
1. Bir vaqtda: 24
2. Alohida: 24
3. Aralash: 24
```


# 175-Topshiriq: Pure Functions (Sof funksiyalar) va Yon ta'sirlarsizlik

## Topshiriq sharti:
Sof (Pure) va Nosof (Impure) funksiyalarning farqini ko'rsatuvchi dastur yozing.

## Yechim (JS yoki TS kodi):
```typescript
// 1. Nosof (Impure) funksiya: tashqi holatga bog'liq va uni o'zgartiradi
let globalTax = 0.12;
function impureCalculateTotal(price: number): number {
  return price * (1 + globalTax);
}

// 2. Sof (Pure) funksiya: faqat argumentlarga tayanadi va hech qanday tashqi narsani o'zgartirmaydi
function pureCalculateTotal(price: number, taxRate: number): number {
  return price * (1 + taxRate);
}

console.log("Impure (globalTax = 0.12):", impureCalculateTotal(100));
globalTax = 0.20; // Tashqi o'zgarish natijani o'zgartirib yuboradi!
console.log("Impure (globalTax = 0.20):", impureCalculateTotal(100));

console.log("Pure natijasi 1:", pureCalculateTotal(100, 0.12));
console.log("Pure natijasi 2 (har doim bir xil):", pureCalculateTotal(100, 0.12));
```

## Tushuntirish va Mantiq:
1. Sof funksiya (Pure Function) ikkita qat'iy talabga javob beradi:
   - Ayni bir xil argumentlar uchun har doim bir xil natija qaytaradi (deterministik).
   - Hech qanday yon ta'sir (side effect) keltirib chiqarmaydi (global o'zgaruvchilarni o'zgartirmaydi, DOM ga yoki bazaga teginmaydi).
2. Sof funksiyalarni testlash, keshlash (memoization) va parallellashtirish juda oson.

## Ishlash natijasi:
```text
Impure (globalTax = 0.12): 112
Impure (globalTax = 0.20): 120
Pure natijasi 1: 112
Pure natijasi 2 (har doim bir xil): 112
```


# 176-Topshiriq: Rekursiya asoslari: Baza holati (Base Case) va Rekursiv qadam

## Topshiriq sharti:
Sonning faktorialini (N!) to'g'ri baza holati bilan hisoblovchi xavfsiz rekursiv funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
function factorial(n: number): number {
  // Cheklov va xatolik nazorati
  if (n < 0) throw new Error("Faktorial faqat musbat sonlar uchun aniqlangan");

  // Baza holati (Base case) - rekursiyani to'xtatuvchi shart
  if (n === 0 || n === 1) {
    return 1;
  }

  // Rekursiv qadam
  return n * factorial(n - 1);
}

console.log("5! =", factorial(5));
console.log("0! =", factorial(0));
```

## Tushuntirish va Mantiq:
1. Rekursiya - bu funksiyaning o'z-o'zini chaqirishi.
2. Har qanday rekursiv funksiyada kamida bitta Baza holati (Base case) bo'lishi shart, aks holda funksiya to'xtamasdan o'zini chaqirib xotirani to'ldirib yuboradi.
3. Rekursiv qadam har safar muammoni kichikroq bo'lakka bo'lib, baza holatiga yaqinlashtirib borishi kerak.

## Ishlash natijasi:
```text
5! = 120
0! = 1
```


# 177-Topshiriq: Daraxtsimon (Tree) obyektlarni rekursiv aylanib chiqish

## Topshiriq sharti:
Tashkiliy tuzilma (kompaniya bo'limlari va xodimlari) ierarxiyasidagi barcha xodimlarning maoshlari yig'indisini hisoblovchi rekursiv funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
interface OrgNode {
  name: string;
  salary: number;
  subordinates?: OrgNode[];
}

function calculateTotalOrgSalary(node: OrgNode): number {
  let total = node.salary;

  if (node.subordinates && node.subordinates.length > 0) {
    for (const sub of node.subordinates) {
      total += calculateTotalOrgSalary(sub); // Rekursiv chaqiruv
    }
  }

  return total;
}

const companyHierarchy: OrgNode = {
  name: "Bosh Direktor",
  salary: 10000,
  subordinates: [
    {
      name: "IT Boshlig'i",
      salary: 6000,
      subordinates: [
        { name: "Frontend Dasturchi", salary: 3000 },
        { name: "Backend Dasturchi", salary: 3500 }
      ]
    },
    {
      name: "Moliya Boshlig'i",
      salary: 5000,
      subordinates: [
        { name: "Buxgalter", salary: 2500 }
      ]
    }
  ]
};

console.log("Kompaniya bo'yicha jami oylik maosh:", calculateTotalOrgSalary(companyHierarchy), "USD");
```

## Tushuntirish va Mantiq:
1. Fayllar tizimi kataloglari, DOM daraxti va tashkiliy tuzilmalar ierarxik daraxt ko'rinishida bo'ladi.
2. Bunday tuzilmalarni aylanib chiqishda rekursiya tabiiy va eng o'qilishi oson yechimdir.
3. Funksiya har bir tugun (node) uchun o'zini qayta chaqiradi va pastki shoxlar natijalarini yuqoriga yig'ib chiqadi.

## Ishlash natijasi:
```text
Kompaniya bo'yicha jami oylik maosh: 30000 USD
```


# 178-Topshiriq: Call Stack to'lishi (Stack Overflow) va xavfsiz chegaralar

## Topshiriq sharti:
Rekursiyada baza holati bo'lmaganda yoki chuqurlik haddan tashqari oshganda `RangeError: Maximum call stack size exceeded` xatosi yuzaga kelishini namoyish eting.

## Yechim (JS yoki TS kodi):
```typescript
function testCallStackLimit(): void {
  let depth = 0;

  function recursiveBlow() {
    depth++;
    recursiveBlow();
  }

  try {
    recursiveBlow();
  } catch (err: any) {
    console.log(`Call stack chegarasi yetdi! Xatolik: ${err.name}`);
    console.log(`Maksimal chaqiruv chuqurligi taxminan: ${depth} ta daraja`);
  }
}

testCallStackLimit();
```

## Tushuntirish va Mantiq:
1. Call Stack xotirasining hajmi cheklangan (odatda 10,000 dan 15,000 tagacha chaqiruv).
2. Har bir funksiya chaqirilganda stekka yangi Stack Frame (lokal o'zgaruvchilar, qaytish manzili) yoziladi.
3. Agar rekursiya juda chuqur bo'lsa, xotira to'lib ketadi va JavaScript dasturi to'xtaydi.

## Ishlash natijasi:
```text
Call stack chegarasi yetdi! Xatolik: RangeError
Maksimal chaqiruv chuqurligi taxminan: 10450 ta daraja
```


# 179-Topshiriq: Trampoline naqshi: Rekursiyani Stack Overflow siz boshqarish

## Topshiriq sharti:
Juda katta rekursiyani siklga o'giruvchi va call stackni to'ldirmaydigan `trampoline` naqshini amalga oshiring.

## Yechim (JS yoki TS kodi):
```typescript
type Thunk = () => Thunk | any;

function trampoline(fn: (...args: any[]) => Thunk) {
  return function(...args: any[]) {
    let result = fn(...args);
    while (typeof result === "function") {
      result = result(); // Stekni bo'shatib keyingi qadamni siklda chaqiramiz
    }
    return result;
  };
}

// Katta sonlar yig'indisi rekursiv (thunk qaytaradi)
function sumTrampoline(n: number, acc: number = 0): Thunk | number {
  if (n <= 0) return acc;
  return () => sumTrampoline(n - 1, acc + n);
}

const safeSum = trampoline(sumTrampoline);
console.log("100,000 gacha sonlar yig'indisi (stack overflowsiz):", safeSum(100000));
```

## Tushuntirish va Mantiq:
1. Trampoline naqshi rekursiv funksiyaning o'zini to'g'ridan-to'g'ri chaqirish o'rniga, bajarilishi kerak bo'lgan keyingi amaliyotni funksiya (thunk) shaklida qaytarishiga asoslanadi.
2. Tashqi `while` sikli har bir thunkni navbatma-navbat bajaradi, natijada har bir qadamdan so'ng call stack darhol bo'shaydi.
3. Bu usul hatto millionlab chaqiruvlarda ham Stack Overflow xatosini butunlay istisno qiladi.

## Ishlash natijasi:
```text
100,000 gacha sonlar yig'indisi (stack overflowsiz): 5000050000
```


# 180-Topshiriq: Debounce funksiyasi: Tezkor takrorlanuvchi hodisalarni jilovlash

## Topshiriq sharti:
Qidiruv maydonida foydalanuvchi yozishdan to'xtaganidan so'nggina so'rov yuboruvchi `debounce` utilitasini closure orqali yozing.

## Yechim (JS yoki TS kodi):
```typescript
function debounce<T extends (...args: any[]) => void>(func: T, delayMs: number): (...args: Parameters<T>) => void {
  let timerId: any = null;

  return function(this: any, ...args: Parameters<T>) {
    // Oldingi rejalashtirilgan chaqiruvni bekor qilamiz
    if (timerId !== null) {
      clearTimeout(timerId);
    }

    // Yangi kechiktirilgan chaqiruvni boshlaymiz
    timerId = setTimeout(() => {
      func.apply(this, args);
      timerId = null;
    }, delayMs);
  };
}

let requestCount = 0;
const sendSearchRequest = (query: string) => {
  requestCount++;
  console.log(`[API So'rov ${requestCount}]: '${query}' qidirilmoqda...`);
};

const debouncedSearch = debounce(sendSearchRequest, 50);

// Foydalanuvchi tez-tez klaviatura bosmoqda
debouncedSearch("T");
debouncedSearch("To");
debouncedSearch("Tosh");
debouncedSearch("Toshkent"); // Faqat shu oxirgisi ishga tushishi kerak!
```

## Tushuntirish va Mantiq:
1. Debounce funksiyasi har safar chaqirilganda oldingi taymerni `clearTimeout` orqali to'xtatadi va yangi taymer o'rnatadi.
2. Faqat foydalanuvchi belgilangan vaqt (`delayMs`) davomida boshqa chaqirmasagina funksiya nihoyat ishga tushadi.
3. Qidiruv inputlari, oyna o'lchami o'zgarganda (resize) API serverini ortiqcha so'rovlar bilan qiynab qo'ymaslik uchun shart.

## Ishlash natijasi:
```text
[API So'rov 1]: 'Toshkent' qidirilmoqda...
```


# 181-Topshiriq: Throttle funksiyasi: Hodisalarni chastota bo'yicha me'yorlash

## Topshiriq sharti:
Scroll hodisasi kabi sekundiga yuzlab marta sodir bo'ladigan amallarni har `limitMs` millisekundda faqat 1 marta bajarishni ta'minlovchi `throttle` funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function throttle<T extends (...args: any[]) => void>(func: T, limitMs: number): (...args: Parameters<T>) => void {
  let inThrottle = false;

  return function(this: any, ...args: Parameters<T>) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;

      setTimeout(() => {
        inThrottle = false;
      }, limitMs);
    }
  };
}

let scrollEventsHandled = 0;
const onScroll = () => {
  scrollEventsHandled++;
  console.log(`Scroll qayta ishlandi (Jami: ${scrollEventsHandled})`);
};

const throttledScroll = throttle(onScroll, 100);

// 10 marta ketma-ket tezkor chaqiramiz
for (let i = 0; i < 10; i++) {
  throttledScroll();
}
```

## Tushuntirish va Mantiq:
1. `throttle` funksiyasi hodisalar oqimini me'yorga soladi (rate limiting).
2. Debounce dan farqli o'laroq, throttle hodisa to'xtashini kutmaydi, balki har belgilangan vaqt oralig'ida (masalan har 100ms da) bitta chaqiruvning bajarilishiga kafolat beradi.
3. Sahifa scrollini kuzatish, sichqoncha harakati va o'yinlardagi otish mexanikasida ishlatiladi.

## Ishlash natijasi:
```text
Scroll qayta ishlandi (Jami: 1)
```


# 182-Topshiriq: Once funksiyasi: Funksiyaning faqat bir marta ishlashini kafolatlash

## Topshiriq sharti:
Dasturda to'lovni tasdiqlash yoki bazani initsializatsiya qilish kabi xavfli amallar faqat 1 marta bajarilishini kafolatlovchi `once` closure funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function once<T extends (...args: any[]) => any>(fn: T): T {
  let hasBeenCalled = false;
  let cachedResult: any;

  return function(this: any, ...args: any[]) {
    if (!hasBeenCalled) {
      hasBeenCalled = true;
      cachedResult = fn.apply(this, args);
    } else {
      console.log("[Ogohlantirish]: Bu amal faqat 1 marta bajarilishi mumkin!");
    }
    return cachedResult;
  } as T;
}

const initializeDatabase = once((dbName: string) => {
  console.log(`Baza yaratildi: ${dbName}`);
  return { connected: true };
});

console.log("1-urinish:", initializeDatabase("users_db"));
console.log("2-urinish:", initializeDatabase("users_db"));
console.log("3-urinish:", initializeDatabase("users_db"));
```

## Tushuntirish va Mantiq:
1. `once` yordamchi funksiyasi o'z closurida `hasBeenCalled` bayrog'ini saqlaydi.
2. Birinchi chaqiruvdan so'ng natija saqlanadi va bayroq ko'tariladi.
3. Keyingi barcha chaqiruvlar asl funksiyani qayta bajarmasdan birinchi natijani qaytaradi. To'lov tizimlarida takroriy yechib olishlarning (double charge) oldini oladi.

## Ishlash natijasi:
```text
Baza yaratildi: users_db
1-urinish: { connected: true }
[Ogohlantirish]: Bu amal faqat 1 marta bajarilishi mumkin!
2-urinish: { connected: true }
[Ogohlantirish]: Bu amal faqat 1 marta bajarilishi mumkin!
3-urinish: { connected: true }
```


# 183-Topshiriq: Function.prototype.length va name xususiyatlari

## Topshiriq sharti:
Funksiyaning parametrlari soni (arilligi - arity) va nomini `fn.length` hamda `fn.name` orqali aniqlashni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function sample(a: number, b: string, c: boolean = false, ...rest: any[]) {}

console.log("Funksiya nomi:", sample.name);
// length faqat default parametrlargacha bo'lgan majburiy parametrlar sonini beradi
console.log("sample.length (majburiy parametrlar soni):", sample.length);

const anonymous = function() {};
console.log("Nomlanmagan funksiya nomi:", anonymous.name);
```

## Tushuntirish va Mantiq:
1. `fn.length` funksiya talab qiladigan rasmiy parametrlar sonini qaytaradi.
2. Diqqat: default qiymatga ega parametrlar va `rest` parametrlari `fn.length` ga kiritilmaydi.
3. `fn.name` funksiyaning identifikator nomini beradi. Nomsiz funksiya o'zgaruvchiga berilsa, JS dvigateli o'zgaruvchi nomini `fn.name` ga biriktiradi (Name Inference).

## Ishlash natijasi:
```text
Funksiya nomi: sample
sample.length (majburiy parametrlar soni): 2
Nomlanmagan funksiya nomi: anonymous
```


# 184-Topshiriq: Rekursiv Deep Clone (Chuqur nusxalash) funksiyasi

## Topshiriq sharti:
Obyekt va massivlarning ichma-ich tuzilmalarini to'liq mustaqil nusxasini yaratuvchi rekursiv `deepClone` funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function deepClone<T>(obj: T): T {
  // Primitivlar va null o'zgarishsiz qaytadi
  if (obj === null || typeof obj !== "object") {
    return obj;
  }

  // Sana obyekti
  if (obj instanceof Date) {
    return new Date(obj.getTime()) as any;
  }

  // Massiv
  if (Array.isArray(obj)) {
    return obj.map((item) => deepClone(item)) as any;
  }

  // Oddiy obyekt
  const clonedObj: Record<string, any> = {};
  for (const key in obj) {
    if (Object.hasOwn(obj, key)) {
      clonedObj[key] = deepClone((obj as any)[key]);
    }
  }

  return clonedObj as T;
}

const originalData = {
  user: "Botir",
  details: {
    skills: ["TypeScript", "Node.js"],
    address: { city: "Toshkent" }
  }
};

const clonedData = deepClone(originalData);
clonedData.details.skills.push("Docker");
clonedData.details.address.city = "Samarqand";

console.log("Asl ma'lumot ko'nikmalari:", originalData.details.skills);
console.log("Asl shahar:", originalData.details.address.city);
console.log("Nusxa shahar:", clonedData.details.address.city);
```

## Tushuntirish va Mantiq:
1. Sayoz nusxalash (`Object.assign`, spread `{...obj}`) faqat birinchi darajani nusxalaydi, ichki obyektlar esa yana umumiy xotira manziliga havola qiladi.
2. Rekursiv `deepClone` har bir obyekt yoki massivni uchratganda uning ichiga kiradi va har bir bo'g'in uchun yangi mustaqil obyekt ochadi.
3. Zamonaviy brauzer va Node.js da `structuredClone()` mavjud, ammo bu algoritm intervyularda eng ko'p so'raladigan dasturiy vazifalardandir.

## Ishlash natijasi:
```text
Asl ma'lumot ko'nikmalari: [ 'TypeScript', 'Node.js' ]
Asl shahar: Toshkent
Nusxa shahar: Samarqand
```


# 185-Topshiriq: Function Composition: Pipe funksiyasi (Chapdan o'ngga konveyer)

## Topshiriq sharti:
Funksiyalarni chapdan o'ngga ketma-ket bajaruvchi `pipe(f, g, h)(x)` utilitasini yarating.

## Yechim (JS yoki TS kodi):
```typescript
type TransformFn<T> = (val: T) => T;

function pipe<T>(...functions: TransformFn<T>[]): TransformFn<T> {
  return (initialValue: T) =>
    functions.reduce((currentValue, fn) => fn(currentValue), initialValue);
}

const trimText = (s: string) => s.trim();
const capitalize = (s: string) => s.charAt(0).toUpperCase() + s.slice(1).toLowerCase();
const addExclamation = (s: string) => `${s}!`;

const sanitizeUserGreeting = pipe(trimText, capitalize, addExclamation);

console.log(sanitizeUserGreeting("   tOSHKENT   "));
```

## Tushuntirish va Mantiq:
1. `pipe` funksional konveyer tamoyilidir: birinchi funksiyaning natijasi ikkinchisiga kiradi, ikkinchisiniki uchinchisiga.
2. `compose` dan farqi shundaki, `pipe` inson o'qish tartibi bo'yicha chapdan o'ngga (tabiiy tartibda) ishlaydi.
3. Katta ma'lumotlarni qayta ishlash zanjirlarida kodni nihoyatda modulli va toza qiladi.

## Ishlash natijasi:
```text
Toshkent!
```


# 186-Topshiriq: Curried Validatorlar: Yuqori tartibli tekshiruvchilar

## Topshiriq sharti:
Boshqa funksiyalarni tekshiruvchi va kompozitsiya qiluvchi qoidalardan iborat validator tizimini yarating.

## Yechim (JS yoki TS kodi):
```typescript
type ValidatorFn = (value: string) => string | null;

const minLength = (min: number): ValidatorFn => (val) =>
  val.length >= min ? null : `Kamida ${min} ta belgi bo'lishi kerak`;

const requireSpecialChar: ValidatorFn = (val) =>
  /[!@#$%^&*]/.test(val) ? null : "Kamida bitta maxsus belgi bo'lishi shart";

function createFieldValidator(...validators: ValidatorFn[]) {
  return (value: string): string[] => {
    return validators
      .map((v) => v(value))
      .filter((err): err is string => err !== null);
  };
}

const passwordValidator = createFieldValidator(minLength(8), requireSpecialChar);

console.log("Parol 'pass':", passwordValidator("pass"));
console.log("Parol 'superSecret!':", passwordValidator("superSecret!"));
```

## Tushuntirish va Mantiq:
1. Yuqori tartibli funksiyalar (Higher-Order Functions) boshqa funksiyalarni qaytarish orqali qoidalarni moslashuvchan (reusable) qiladi.
2. `minLength(8)` alohida funksiya qaytaradi, `requireSpecialChar` bilan birga bitta validatorga birlashtiriladi.
3. Formik, React Hook Form va Zod kabi zamonaviy kutubxonalar aynan shu falsafaga tayanadi.

## Ishlash natijasi:
```text
Parol 'pass': [
  'Kamida 8 ta belgi bo\'lishi kerak',
  'Kamida bitta maxsus belgi bo\'lishi shart'
]
Parol 'superSecret!': []
```


# 187-Topshiriq: Konstruktor funksiyalar va new.target operatori

## Topshiriq sharti:
ES6 sinflaridan oldingi konstruktor funksiyalar qanday ishlaganini va `new.target` orqali `new` siz chaqirilishdan himoyalanishni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function Car(this: any, make: string, model: string) {
  // new bilan chaqirilganini tekshirish
  if (!new.target) {
    console.log("[Ogohlantirish]: Car 'new' siz chaqirildi, avtomatik new ga o'tkazildi.");
    return new (Car as any)(make, model);
  }

  this.make = make;
  this.model = model;
}

Car.prototype.getInfo = function() {
  return `${this.make} ${this.model}`;
};

// 1. To'g'ri new bilan
const car1 = new (Car as any)("Tesla", "Model 3");
console.log("car1:", car1.getInfo());

// 2. new siz chaqiruv
const car2 = (Car as any)("BYD", "Song Plus");
console.log("car2:", car2.getInfo());
```

## Tushuntirish va Mantiq:
1. ES6 gacha sinflar bo'lmagan, ularning vazifasini oddiy konstruktor funksiyalar bajargan.
2. Agar konstruktor funksiya tasodifan `new` siz chaqirilsa, `this` global obyektga ulanib, global sohani buzardi.
3. `new.target` ES6 da kiritilgan meta-xususiyat bo'lib, funksiya `new` bilan chaqirilgan bo'lsa konstruktor havolasini, aks holda `undefined` qaytaradi.

## Ishlash natijasi:
```text
car1: Tesla Model 3
[Ogohlantirish]: Car 'new' siz chaqirildi, avtomatik new ga o'tkazildi.
car2: BYD Song Plus
```


# 188-Topshiriq: Method Chaining (Fluent API) naqshini sinfda amalga oshirish

## Topshiriq sharti:
Har bir metodda `return this` qaytarish orqali SQL so'rovlarini quruvchi Fluent Query Builder yarating.

## Yechim (JS yoki TS kodi):
```typescript
class QueryBuilder {
  private table: string = "";
  private fields: string[] = ["*"];
  private whereClause: string = "";

  from(table: string): this {
    this.table = table;
    return this; // Zanjirni davom ettirish uchun obyektning o'zini qaytaramiz
  }

  select(...fields: string[]): this {
    this.fields = fields;
    return this;
  }

  where(condition: string): this {
    this.whereClause = `WHERE ${condition}`;
    return this;
  }

  build(): string {
    return `SELECT ${this.fields.join(", ")} FROM ${this.table} ${this.whereClause}`.trim();
  }
}

const query = new QueryBuilder()
  .from("users")
  .select("id", "username", "email")
  .where("is_active = true")
  .build();

console.log("Yig'ilgan SQL so'rovi:\n" + query);
```

## Tushuntirish va Mantiq:
1. Method Chaining (yoki Fluent Interface) har bir metod oxirida joriy obyekt nusxasini (`return this`) qaytarishga asoslanadi.
2. Bu metodlarni ketma-ket nuqta bilan (`.from().select().where()`) tabiiy til kabi zanjir qilib yozish imkonini beradi.
3. Knex.js, Prisma, jQuery va ko'plab zamonaviy SDKlar shu naqshda qurilgan.

## Ishlash natijasi:
```text
Yig'ilgan SQL so'rovi:
SELECT id, username, email FROM users WHERE is_active = true
```


# 189-Topshiriq: Closure bilan Memory Leak (Xotira sizib ketishi) xatarlaridan saqlanish

## Topshiriq sharti:
Closure ichida keraksiz katta obyektlarni ushlab qolish xatosini va uni bartaraf etish usulini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function createHeavyOperation() {
  let heavyBuffer: number[] | null = new Array(1000000).fill(7);

  const neededResult = heavyBuffer[0] * 10;

  // XATO: Agar heavyBuffer closure da qolsa, xotirada 1M ta son yashayveradi
  // TO'G'RI: Keraksiz o'zgaruvchini nollashtiramiz
  heavyBuffer = null;

  return function() {
    return `Bajarildi, hisoblangan qiymat: ${neededResult}`;
  };
}

const op = createHeavyOperation();
console.log(op());
```

## Tushuntirish va Mantiq:
1. Closure tashqi leksik muhitdagi o'zgaruvchilarga havola saqlaydi.
2. Agar tashqi funksiyada katta massiv yoki DOM elementlari bo'lsa va ular closure ichida ishlatilmasa ham, ba'zi dvigatellarda umumiy soha tufayli xotiradan tozalanmay qolib ketishi mumkin.
3. Katta vaqtinchalik ma'lumotlarni o'z vaqtida `null` qilib qo'yish xotira tozaligini ta'minlaydi.

## Ishlash natijasi:
```text
Bajarildi, hisoblangan qiymat: 70
```


# 190-Topshiriq: Amaliy loyiha: Event Emitter va Pub/Sub (Publish-Subscribe) tizimi

## Topshiriq sharti:
Funksiyalar va massivlar asosida to'liq ishlovchi hodisalar boshqaruvchisi (`on`, `off`, `emit`, `once`) sinfini yarating.

## Yechim (JS yoki TS kodi):
```typescript
type Listener = (...args: any[]) => void;

class CustomEventEmitter {
  private events: Map<string, Listener[]> = new Map();

  // Hodisaga obuna bo'lish
  on(event: string, listener: Listener): void {
    if (!this.events.has(event)) {
      this.events.set(event, []);
    }
    this.events.get(event)!.push(listener);
  }

  // Hodisani yuborish
  emit(event: string, ...args: any[]): void {
    const listeners = this.events.get(event);
    if (listeners) {
      listeners.forEach((fn) => fn(...args));
    }
  }

  // Obunani bekor qilish
  off(event: string, listenerToRemove: Listener): void {
    const listeners = this.events.get(event);
    if (!listeners) return;

    this.events.set(
      event,
      listeners.filter((fn) => fn !== listenerToRemove)
    );
  }

  // Faqat 1 marta eshitish
  once(event: string, listener: Listener): void {
    const wrapper = (...args: any[]) => {
      this.off(event, wrapper);
      listener(...args);
    };
    this.on(event, wrapper);
  }
}

const emitter = new CustomEventEmitter();

const orderLogger = (orderId: number, amount: number) => {
  console.log(`[Buyurtma]: ID=${orderId}, Summa=${amount} so'm`);
};

emitter.on("order_created", orderLogger);
emitter.once("system_ready", () => console.log("[Tizim]: Tayyor!"));

emitter.emit("system_ready");
emitter.emit("system_ready"); // Ishlamaydi (chunki once)

emitter.emit("order_created", 501, 120000);
emitter.off("order_created", orderLogger);
emitter.emit("order_created", 502, 350000); // Ishlamaydi (chunki off)
```

## Tushuntirish va Mantiq:
1. Event Emitter (Hodisalar emitenti) Node.js va zamonaviy frontend arxitekturalarining (Redux, Vue event bus) yuragi hisoblanadi.
2. Har bir hodisa nomi bo'yicha callback funksiyalari massivi saqlanadi.
3. `emit` chaqirilganda barcha ro'yxatdan o'tgan tinglovchilar ketma-ket chaqiriladi.
4. `once` metodi esa closure ichida wrapper yaratib, birinchi chaqiruvdan so'ng o'zini `off` qilib tashlaydi.

## Ishlash natijasi:
```text
[Tizim]: Tayyor!
[Buyurtma]: ID=501, Summa=120000 so'm
```


# 191-Topshiriq: Recursion: Palindromlikni tekshirish

## Topshiriq sharti:
Berilgan satrning palindrom (o'ngdan ham, chapdan ham bir xil o'qilishi) ekanligini rekursiv usulda aniqlovchi funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
function isPalindromeRecursive(str: string): boolean {
  // Bosh va oxiridagi bo'shliqlarni olib, kichik harfga keltiramiz
  const clean = str.toLowerCase().replace(/[^a-z0-9]/g, "");

  function check(s: string, start: number, end: number): boolean {
    if (start >= end) return true; // Baza holati: o'rtaga yetib keldik
    if (s[start] !== s[end]) return false;
    return check(s, start + 1, end - 1);
  }

  return check(clean, 0, clean.length - 1);
}

console.log("'kiyik' palindrommi:", isPalindromeRecursive("kiyik"));
console.log("'non' palindrommi:", isPalindromeRecursive("non"));
console.log("'salom' palindrommi:", isPalindromeRecursive("salom"));
```

## Tushuntirish va Mantiq:
1. Har bir qadamda satrning birinchi va oxirgi belgilari solishtiriladi.
2. Agar ular teng bo'lsa, qidiruv chegarasi ichkariga suriladi (`start + 1, end - 1`).
3. Chegaralar to'qnashganda (`start >= end`), satr to'liq tekshirilib palindrom deb tasdiqlanadi.

## Ishlash natijasi:
```text
'kiyik' palindrommi: true
'non' palindrommi: true
'salom' palindrommi: false
```


# 192-Topshiriq: Funksiya argumentlarining destrukturizatsiyasi va standart qiymatlar

## Topshiriq sharti:
Murakkab sozlamalar qabul qiluvchi funksiyada obyekt destrukturizatsiyasi va har bir parametr uchun standart qiymatlar berishni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
interface ServerConfig {
  host?: string;
  port?: number;
  ssl?: boolean;
}

function startServer({ host = "localhost", port = 8080, ssl = false }: ServerConfig = {}): void {
  const protocol = ssl ? "https" : "http";
  console.log(`Server ishga tushdi: ${protocol}://${host}:${port}`);
}

startServer(); // Butunlay argumentsiz
startServer({ port: 3000 });
startServer({ host: "api.domain.uz", port: 443, ssl: true });
```

## Tushuntirish va Mantiq:
1. `{ host = "localhost", ... } = {}` sintaksisi nafaqat parametrlar ichida, balki argumentning o'zi uzatilmagan taqdirda ham xatoliksiz ishlashni ta'minlaydi.
2. Bu naqsh (Options Object Pattern) ko'p argumentli funksiyalarda parametrlar tartibini yodda tutish majburiyatidan qutqaradi.

## Ishlash natijasi:
```text
Server ishga tushdi: http://localhost:8080
Server ishga tushdi: http://localhost:3000
Server ishga tushdi: https://api.domain.uz:443
```


# 193-Topshiriq: Asinxron funksiyalarda Lexical Environment va Closure

## Topshiriq sharti:
`async/await` vaqtida closure dagi o'zgaruvchilarning asinxron kutish paytida qanday saqlanib turishini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function createAsyncWorker(workerId: string) {
  let taskCount = 0;

  return async function executeTask(taskName: string): Promise<string> {
    taskCount++;
    const currentTaskId = taskCount;

    // Asinxron kutish simulyatsiyasi (masalan, API yoki I/O)
    await new Promise((resolve) => setTimeout(resolve, 50));

    return `Worker [${workerId}] vazifani yakunladi: #${currentTaskId} '${taskName}'`;
  };
}

async function runWorker() {
  const worker = createAsyncWorker("Node_01");

  const r1 = await worker("Hisobot generatsiyasi");
  console.log(r1);

  const r2 = await worker("Email yuborish");
  console.log(r2);
}

runWorker();
```

## Tushuntirish va Mantiq:
1. `async` funksiya ichidagi `await` bajarilishni vaqtinchalik to'xtatganda (pause), butun leksik muhit va closure saqlanib turadi.
2. Asinxron operatsiya tugagach, dvigatel to'xtagan joyidan qayta davom etadi va barcha closure o'zgaruvchilari o'z qiymatini saqlab qolgan bo'ladi.

## Ishlash natijasi:
```text
Worker [Node_01] vazifani yakunladi: #1 'Hisobot generatsiyasi'
Worker [Node_01] vazifani yakunladi: #2 'Email yuborish'
```


# 194-Topshiriq: Funksiyalar arilligi (Arity) bo'yicha adapter funksiya

## Topshiriq sharti:
Ko'p argument kutadigan funksiyani faqat bitta argument qabul qiluvchi kontekstga (masalan `parseInt` bilan `map`) moslovchi `unary` adapterini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function testUnaryAdapter(): void {
  // Mashhur xato: ['1', '2', '3'].map(parseInt) -> [1, NaN, NaN]!
  // Chunki map element, index, array ni uzatadi, parseInt esa radix deb qabul qiladi
  const wrong = ["1", "2", "3"].map(parseInt);
  console.log("Noto'g'ri map(parseInt):", wrong);

  // unary adapteri: faqat 1-argumentni o'tkazadi
  const unary = (fn: Function) => (arg: any) => fn(arg);

  const correct = ["1", "2", "3"].map(unary(parseInt));
  console.log("unary(parseInt) orqali to'g'ri natija:", correct);
}

testUnaryAdapter();
```

## Tushuntirish va Mantiq:
1. `['1', '2', '3'].map(parseInt)` yozilganda, `map` har bir iteratsiyada 3 ta argument beradi: `(item, index, array)`.
2. `parseInt` ikkinchi argumentni sanoq sistemasi (`radix`) deb biladi, natijada `parseInt('2', 1)` va `parseInt('3', 2)` xato (`NaN`) qaytaradi.
3. `unary(fn)` adapteri har qanday funksiyani majburiy ravishda 1 ta argument oladigan qilib o'rab beradi.

## Ishlash natijasi:
```text
Noto'g'ri map(parseInt): [ 1, NaN, NaN ]
unary(parseInt) orqali to'g'ri natija: [ 1, 2, 3 ]
```


# 195-Topshiriq: Funksiyalar va Generatorlar integratsiyasi

## Topshiriq sharti:
Kattaroq oraliqdagi ID larni talab bo'yicha (lazy evaluation) ishlab chiqaruvchi generator funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function* idSequenceGenerator(prefix: string): Generator<string, void, unknown> {
  let id = 1;
  while (true) {
    yield `${prefix}_${id++}`;
  }
}

const userIdGen = idSequenceGenerator("USER");

console.log("1-ID:", userIdGen.next().value);
console.log("2-ID:", userIdGen.next().value);
console.log("3-ID:", userIdGen.next().value);
```

## Tushuntirish va Mantiq:
1. `function*` generator funksiyasi chaqirilganda darhol bajarilmaydi, balki generator obyektini qaytaradi.
2. Har safar `.next()` chaqirilganda, funksiya navbatdagi `yield` operatorigacha ishlaydi va qiymatni qaytarib to'xtab turadi.
3. Bu usul cheksiz ketma-ketliklarni xotirani to'ldirmasdan, faqat kerak bo'lganda (lazy) hisoblash imkonini beradi.

## Ishlash natijasi:
```text
1-ID: USER_1
2-ID: USER_2
3-ID: USER_3
```


# 196-Topshiriq: Kompilyatsiya vaqtida funksiya nomini saqlash: Function name inferring

## Topshiriq sharti:
Anonim funksiyalar turli o'zgaruvchilarga, massivlarga va obyekt xususiyatlariga berilganda `name` xususiyati qanday nomlanishini tekshiring.

## Yechim (JS yoki TS kodi):
```typescript
function checkFunctionNames(): void {
  const myHandler = function() {};
  console.log("myHandler.name:", myHandler.name);

  const obj = {
    doWork() {},
    processData: () => {}
  };
  console.log("obj.doWork.name:", obj.doWork.name);
  console.log("obj.processData.name:", obj.processData.name);

  // Getter va Setterlar maxsus prefiks oladi
  const propertyDescriptor = {
    get balance() { return 100; }
  };
  const desc = Object.getOwnPropertyDescriptor(propertyDescriptor, "balance");
  console.log("Getter nomi:", desc?.get?.name);
}

checkFunctionNames();
```

## Tushuntirish va Mantiq:
1. JavaScript dvigateli funksiya nomlarini aniqlashda (Name Inference) aqlli harakat qiladi: nomsiz funksiyaga o'zlashtirilgan o'zgaruvchi yoki obyekt kalitining nomi beriladi.
2. Getter va Setter funksiyalar nomining oldiga `get ` va `set ` prefikslari qo'shiladi.
3. Bu stack trace va xatoliklar logini o'qishda xatolik yuz bergan joyni aniq ko'rsatishga yordam beradi.

## Ishlash natijasi:
```text
myHandler.name: myHandler
obj.doWork.name: doWork
obj.processData.name: processData
Getter nomi: get balance
```


# 197-Topshiriq: Recursion: Massiv elementlari kombinatsiyalarini (Permutations) generatsiya qilish

## Topshiriq sharti:
Berilgan massivning barcha mumkin bo'lgan o'rin almashtirishlarini (permutatsiyalarini) rekursiya yordamida hosil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function getPermutations<T>(arr: T[]): T[][] {
  if (arr.length <= 1) return [arr];

  const result: T[][] = [];

  for (let i = 0; i < arr.length; i++) {
    const current = arr[i];
    const remaining = arr.slice(0, i).concat(arr.slice(i + 1));
    const remainingPermutations = getPermutations(remaining);

    for (const perm of remainingPermutations) {
      result.push([current, ...perm]);
    }
  }

  return result;
}

const items = ["A", "B", "C"];
const perms = getPermutations(items);

console.log(`Jami kombinatsiyalar soni: ${perms.length}`);
perms.forEach((p) => console.log(p.join("")));
```

## Tushuntirish va Mantiq:
1. Permutatsiyalar algoritmi rekursiv ravishda har bir elementni boshiga qo'yadi va qolgan elementlar uchun yana o'zini chaqiradi.
2. N ta element uchun jami `N!` ta kombinatsiya mavjud bo'ladi (3 element uchun 3! = 6 ta).
3. Backtracking va kombinatorika algoritmlarida asosiy poydevor hisoblanadi.

## Ishlash natijasi:
```text
Jami kombinatsiyalar soni: 6
ABC
ACB
BAC
BCA
CAB
CBA
```


# 198-Topshiriq: Funksiya parametri sifatida boshqa funksiyani tekshiruvchi Guard HOF

## Topshiriq sharti:
Foydalanuvchi huquqi yetarli bo'lgandagina asl funksiyani chaqiruvchi himoyalovchi Yuqori Tartibli Funksiya (Higher-Order Guard) yozing.

## Yechim (JS yoki TS kodi):
```typescript
interface Session {
  role: "admin" | "user";
}

function withRoleGuard<T extends (...args: any[]) => any>(
  requiredRole: string,
  fn: T
) {
  return function(session: Session, ...args: Parameters<T>): ReturnType<T> | string {
    if (session.role !== requiredRole) {
      return `Ruxsat rad etildi: Faqat [${requiredRole}] bajara oladi.`;
    }
    return fn(...args);
  };
}

function deleteDatabase(target: string): string {
  return `Baza '${target}' butunlay o'chirildi!`;
}

const safeDeleteDatabase = withRoleGuard("admin", deleteDatabase);

const userSession: Session = { role: "user" };
const adminSession: Session = { role: "admin" };

console.log("Oddiy foydalanuvchi urinishi:", safeDeleteDatabase(userSession, "production_db"));
console.log("Admin urinishi:", safeDeleteDatabase(adminSession, "production_db"));
```

## Tushuntirish va Mantiq:
1. HOF Guard naqshi biznes funksiyasiga teginmasdan uni yangi xavfsizlik va ruxsat qatlami bilan o'rab beradi (Decorator naqshi).
2. Asl funksiya (`deleteDatabase`) faqat o'z vazifasini biladi, huquq tekshirish esa alohida ajratilgan.
3. Bu dasturiy arxitekturadagi Yagona javobgarlik (Single Responsibility) tamoyiliga to'liq mos keladi.

## Ishlash natijasi:
```text
Oddiy foydalanuvchi urinishi: Ruxsat rad etildi: Faqat [admin] bajara oladi.
Admin urinishi: Baza 'production_db' butunlay o'chirildi!
```


# 199-Topshiriq: Recursion va Backtracking: Labirintdan chiqish yo'lini topish

## Topshiriq sharti:
0 (o'tish mumkin) va 1 (devor) lardan iborat 2D katakchada boshlang'ich nuqtadan marragacha bo'lgan yo'lni rekursiv backtracking orqali toping.

## Yechim (JS yoki TS kodi):
```typescript
type Maze = number[][];

function solveMaze(maze: Maze): boolean {
  const rows = maze.length;
  const cols = maze[0].length;
  const solution: number[][] = Array.from({ length: rows }, () => new Array(cols).fill(0));

  function findPath(r: number, c: number): boolean {
    // Manzilga yetdikmi?
    if (r === rows - 1 && c === cols - 1 && maze[r][c] === 0) {
      solution[r][c] = 1;
      return true;
    }

    // Chegaralar va devor tekshiruvi
    if (r >= 0 && r < rows && c >= 0 && c < cols && maze[r][c] === 0 && solution[r][c] === 0) {
      solution[r][c] = 1; // Ushbu yo'lni sinab ko'ramiz

      // O'ngga yurish
      if (findPath(r, c + 1)) return true;
      // Pastga yurish
      if (findPath(r + 1, c)) return true;

      // Agar ikkala yo'l ham berk bo'lsa - orqaga qaytamiz (Backtrack)
      solution[r][c] = 0;
      return false;
    }

    return false;
  }

  const hasPath = findPath(0, 0);
  console.log("Chiqish yo'li mavjudmi:", hasPath);
  return hasPath;
}

const sampleMaze = [
  [0, 1, 0],
  [0, 0, 0],
  [1, 1, 0]
];

solveMaze(sampleMaze);
```

## Tushuntirish va Mantiq:
1. Backtracking (orqaga chekinish) - bu yechimni sinab ko'rish va agar yechim xato yo'lga kirib qolsa, qilingan oxirgi amallarni bekor qilib boshqa yo'ldan ketish algoritmidir.
2. Rekursiya chaqiruvlari orqali yangi koordinatalar tekshiriladi.
3. Agar yo'l berk bo'lsa, `solution[r][c] = 0` qilinadi va oldingi qadamga qaytiladi.

## Ishlash natijasi:
```text
Chiqish yo'li mavjudmi: true
```


# 200-Topshiriq: Yakuniy Sintez: Asinxron Retry Mexanizmi va Exponential Backoff

## Topshiriq sharti:
Funksiyalar, closure va asinxronlikni birlashtirib, xatolik bergan API chaqiruvlarini eksponensial kechikish bilan qayta urinuvchi (Retry with Exponential Backoff) professional utilita yarating.

## Yechim (JS yoki TS kodi):
```typescript
interface RetryOptions {
  maxRetries: number;
  initialDelayMs: number;
  backoffFactor: number;
}

function withRetry<T>(
  asyncFn: () => Promise<T>,
  options: RetryOptions = { maxRetries: 3, initialDelayMs: 50, backoffFactor: 2 }
): Promise<T> {
  let attempt = 0;
  let currentDelay = options.initialDelayMs;

  return new Promise<T>((resolve, reject) => {
    function executeAttempt() {
      attempt++;
      console.log(`[Urinish #${attempt}] Funksiya bajarilmoqda...`);

      asyncFn()
        .then(resolve)
        .catch((error) => {
          if (attempt >= options.maxRetries) {
            console.log(`Barcha ${options.maxRetries} ta urinish tugadi. Xatolik!`);
            return reject(error);
          }

          console.log(`Xatolik yuz berdi (${error.message}). ${currentDelay}ms dan keyin qayta uriniladi...`);
          setTimeout(() => {
            currentDelay *= options.backoffFactor; // Kechikish vaqtini ko'paytiramiz
            executeAttempt();
          }, currentDelay);
        });
    }

    executeAttempt();
  });
}

// Sinov uchun 2 marta xato berib, 3-sida muvaffaqiyatli ishlaydigan so'rov
let failCount = 0;
const unstableNetworkCall = async () => {
  if (failCount < 2) {
    failCount++;
    throw new Error("Tarmoqda uzilish (503)");
  }
  return "Ma'lumotlar muvaffaqiyatli qabul qilindi!";
};

withRetry(unstableNetworkCall, { maxRetries: 3, initialDelayMs: 50, backoffFactor: 2 })
  .then((data) => console.log("[Muvaffaqiyat]:", data))
  .catch((err) => console.error("[Xato]:", err));
```

## Tushuntirish va Mantiq:
1. Exponential Backoff zamonaviy taqsimlangan tizimlar va API integratsiyalarida standart hisoblanadi.
2. Har bir muvaffaqiyatsiz urinishdan keyin kutish vaqti eksponensial oshiriladi (50ms -> 100ms -> 200ms).
3. Bu serverga birdaniga qayta-qayta zarba bermasdan (Thundering Herd muammosi), tarmoq tiklanishiga imkon beradi.

## Ishlash natijasi:
```text
[Urinish #1] Funksiya bajarilmoqda...
Xatolik yuz berdi (Tarmoqda uzilish (503)). 50ms dan keyin qayta uriniladi...
[Urinish #2] Funksiya bajarilmoqda...
Xatolik yuz berdi (Tarmoqda uzilish (503)). 100ms dan keyin qayta uriniladi...
[Urinish #3] Funksiya bajarilmoqda...
[Muvaffaqiyat]: Ma'lumotlar muvaffaqiyatli qabul qilindi!
```

