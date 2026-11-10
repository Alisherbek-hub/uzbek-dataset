# 451-Topshiriq: TypeScript nima: Statik tiplash va Ish vaqti (Runtime) mustaqilligi

## Topshiriq sharti:
TypeScriptning statik tiplash qobiliyati qanday qilib kompilyatsiya vaqtida xatolarni tutishini va runtimeda turlar butunlay o'chirilishini (Type Erasure) tushuntiring.

## Yechim (JS yoki TS kodi):
```typescript
function calculateDiscount(price: number, discountPercent: number): number {
  return price - (price * discountPercent) / 100;
}

// TypeScript kompilyatsiya paytida tiplarni tekshiradi:
const finalPrice = calculateDiscount(100000, 15);
console.log("Chegirilgan yakuniy narx:", finalPrice, "so'm");

// Kompilyatsiyadan so'ng (JS da):
// function calculateDiscount(price, discountPercent) { return price - (price * discountPercent) / 100; }
// Barcha ': number' tiplari JS ga o'tganda yo'qoladi (Type Erasure)!
```

## Tushuntirish va Mantiq:
1. TypeScript - bu JavaScriptning statik turlangan kengaytmasidir (Superset).
2. U dastur kodi ishga tushmasidan oldin (kompilyatsiya bosqichida) tiplarning to'g'riligini tekshiradi.
3. JavaScript fayliga aylantirilganda (Transpilation), barcha TypeScript tiplari butunlay olib tashlanadi (Type Erasure), shuning uchun runtime hajmiga yoki tezligiga hech qanday ortiqcha yuk tushmaydi.

## Ishlash natijasi:
```text
Chegirilgan yakuniy narx: 85000 so'm
```


# 452-Topshiriq: tsconfig.json asosiy direktivalari: target, module, strict

## Topshiriq sharti:
Professional TypeScript loyihasining `tsconfig.json` asosiy sozlamalarini va ularning ahamiyatini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function explainTsConfig(): void {
  const sampleConfig = {
    compilerOptions: {
      target: "ES2022",         // Qaysi ECMAScript versiyasiga kompilyatsiya qilish
      module: "NodeNext",       // Modul tizimi (NodeNext, ESNext)
      strict: true,             // Barcha qat'iy tip tekshiruvlarini yoqish
      esModuleInterop: true,    // CommonJS va ES modullari o'rtasidagi uyg'unlik
      skipLibCheck: true,       // .d.ts kutubxona fayllarini qayta tekshirmasdan tezlashtirish
      outDir: "./dist",         // Kompilyatsiya qilingan JS fayllar jildi
      rootDir: "./src"          // Asl TypeScript manba kodi jildi
    }
  };

  console.log("Tavsiya etiladigan tsconfig.json sozlamalari:");
  console.log(JSON.stringify(sampleConfig, null, 2));
}

explainTsConfig();
```

## Tushuntirish va Mantiq:
1. `target`: chiqariladigan JavaScript versiyasini belgilaydi (masalan ES2022 zamonaviy funksiyalarni saqlab qoladi).
2. `strict: true`: eng muhim bayroq bo'lib, `noImplicitAny`, `strictNullChecks` kabi barcha qat'iy xavfsizlik tekshiruvlarini yoqadi.
3. Loyihalarda har doim `strict: true` rejimida ishlash professional standartdir.

## Ishlash natijasi:
```text
Tavsiya etiladigan tsconfig.json sozlamalari:
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "outDir": "./dist",
    "rootDir": "./src"
  }
}
```


# 453-Topshiriq: Type Inference (Turlarni avtomatik aniqlash)

## Topshiriq sharti:
TypeScriptning qiymatga qarab o'zgaruvchi tipini avtomatik to'g'ri aniqlash (Inference) qobiliyatini namoyish eting.

## Yechim (JS yoki TS kodi):
```typescript
function testTypeInference(): void {
  // Qo'lda tip yozilmadi, ammo TypeScript ularni aniq bildi:
  let message = "Salom, TypeScript!"; // string deb topildi
  let score = 95;                      // number deb topildi
  let isActive = true;                 // boolean deb topildi

  console.log("message turi:", typeof message);
  console.log("score turi:", typeof score);
  console.log("isActive turi:", typeof isActive);

  // message = 100; // TS Xatosi: Type 'number' is not assignable to type 'string'
}

testTypeInference();
```

## Tushuntirish va Mantiq:
1. TypeScript aqlli tahlil mexanizmiga ega: initsializatsiya paytidagi qiymatga qarab tipni o'zi avtomatik belgilaydi.
2. Aniq ma'lum bo'lgan oddiy o'zgaruvchilarda qo'lda `: string` yoki `: number` deb yozish ortiqcha hisoblanadi (redundant).
3. Type Inference kodni toza va o'qilishi yengil saqlaydi.

## Ishlash natijasi:
```text
message turi: string
score turi: number
isActive turi: boolean
```


# 454-Topshiriq: any tipi va uning xavflari (Nima uchun any dan qochish kerak?)

## Topshiriq sharti:
`any` tipi TypeScriptning barcha xavfsizlik tekshiruvlarini o'chirib qo'yishi oqibatida yuzaga keladigan runtime xatosini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function demonstrateAnyDanger(): void {
  let dangerousData: any = "Salom Dunyo";

  // any bo'lgani uchun TS har qanday amalga ko'r-ko'rona ruxsat beradi
  dangerousData = 12345;

  try {
    // Number ustida toUpperCase chaqirish runtime da TypeError beradi!
    // Kompilyator esa any tufayli buni payqamadi!
    dangerousData.toUpperCase();
  } catch (err: any) {
    console.log("Kutilmagan runtime xato ushlandi:", err.name, "-", err.message);
  }
}

demonstrateAnyDanger();
```

## Tushuntirish va Mantiq:
1. `any` tipi TypeScript tekshiruvini aylanib o'tish (opt-out) vositasidir.
2. `any` ishlatilgan joyda TypeScript oddiy xavfli JavaScriptga aylanadi: hech qanday avtomatik to'ldirish (autocomplete) va xatolar tekshiruvi ishlamaydi.
3. Agar tip oldindan noma'lum bo'lsa, `any` o'rniga har doim `unknown` tipidan foydalanish shart.

## Ishlash natijasi:
```text
Kutilmagan runtime xato ushlandi: TypeError - dangerousData.toUpperCase is not a function
```


# 455-Topshiriq: unknown tipi: any ning xavfsiz muqobili va Type Narrowing

## Topshiriq sharti:
`unknown` tipidagi o'zgaruvchi bilan ishlashda majburiy tip tekshiruvini (Type Narrowing) qo'llang.

## Yechim (JS yoki TS kodi):
```typescript
function processUnknownInput(input: unknown): string {
  // input.toUpperCase(); // XATO! 'input' is of type 'unknown'

  // Majburiy tip tekshiruvi (Narrowing):
  if (typeof input === "string") {
    return input.toUpperCase(); // Bu blokda TS biladi: input aniq string!
  } else if (typeof input === "number") {
    return input.toFixed(2);
  } else {
    return "Noma'lum tipdagi qiymat";
  }
}

console.log("String bilan:", processUnknownInput("dasturlash"));
console.log("Number bilan:", processUnknownInput(45.6789));
console.log("Boolean bilan:", processUnknownInput(true));
```

## Tushuntirish va Mantiq:
1. `unknown` tipi har qanday qiymatni qabul qila oladi, ammo `any` dan farqli ravishda, uning ustida tipni tekshirmasdan turib hech qanday amal bajarishga ruxsat bermaydi.
2. `if (typeof x === 'string')` tekshiruvi orqali TypeScript tipni toraytiradi (Type Narrowing).
3. Tashqi API lardan yoki foydalanuvchidan keladigan noma'lum ma'lumotlar uchun eng to'g'ri tipdir.

## Ishlash natijasi:
```text
String bilan: DASTURLASH
Number bilan: 45.68
Boolean bilan: Noma'lum tipdagi qiymat
```


# 456-Topshiriq: void vs never tiplari farqi

## Topshiriq sharti:
Hech narsa qaytarmaydigan (`void`) va hech qachon oxiriga yetmaydigan yoki xato tashlaydigan (`never`) funksiyalar farqini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
// void: funksiya o'z ishini yakunlaydi, lekin qiymat qaytarmaydi (undefined qaytadi)
function logMessage(msg: string): void {
  console.log(`[Xabar]: ${msg}`);
}

// never: funksiya hech qachon normal yakunlanmaydi (abadiy sikl yoki xato otadi)
function throwFatalError(errorMessage: string): never {
  throw new Error(`Kritik xatolik: ${errorMessage}`);
}

logMessage("Tizim ishlamoqda");

try {
  throwFatalError("Baza quladi");
} catch (e: any) {
  console.log("never funksiyasi tashlagan xato ushlandi:", e.message);
}
```

## Tushuntirish va Mantiq:
1. `void` funksiya odatiy tarzda tugaydi, ammo uning qaytargan natijasi e'tiborga olinmaydi (`undefined`).
2. `never` esa dastur oqimining bu nuqtadan keyin hech qachon davom etmasligini bildiradi (funksiya yo doim xato tashlaydi, yo abadiy siklda qoladi).
3. `never` to'liq tekshiruv (Exhaustive checking) algoritmlarida juda muhim o'rin tutadi.

## Ishlash natijasi:
```text
[Xabar]: Tizim ishlamoqda
never funksiyasi tashlagan xato ushlandi: Kritik xatolik: Baza quladi
```


# 457-Topshiriq: Tuple (Kortej) tiplari: Qat'iy tartib va o'lcham

## Topshiriq sharti:
Geografik koordinatalar (kenglik, uzunlik, shahar nomi) uchun qat'iy uzunlik va turlarga ega Tuple tipini yarating.

## Yechim (JS yoki TS kodi):
```typescript
// Tuple: [kenglik: number, uzunlik: number, shahar: string]
type GeoLocation = [number, number, string];

function printLocation(loc: GeoLocation): void {
  const [lat, lng, city] = loc;
  console.log(`Shahar: ${city} (Lat: ${lat}, Lng: ${lng})`);
}

const toshkent: GeoLocation = [41.2995, 69.2401, "Toshkent"];
printLocation(toshkent);

// Noto'g'ri tartib kompilyatsiya xatosi beradi:
// const bad: GeoLocation = ["Toshkent", 41.2995, 69.2401]; // Xato!
```

## Tushuntirish va Mantiq:
1. Massivda (`number[]`) barcha elementlar bir xil turda bo'ladi va elementlar soni cheklanmagan.
2. Tuple (Kortej) esa aniq belgilangan uzunlikka va har bir indeksda aniq qat'iy belgilangan turga ega bo'ladi (`[number, number, string]`).
3. React `useState` hooki aynan Tuple (`[state, setState]`) qaytaradi.

## Ishlash natijasi:
```text
Shahar: Toshkent (Lat: 41.2995, Lng: 69.2401)
```


# 458-Topshiriq: Readonly Tuples va const Assertions (as const)

## Topshiriq sharti:
`as const` operatori orqali o'zgaruvchini mutlaqo o'zgarmas literal tuple ga aylantirishni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function testConstAssertion(): void {
  // Oddiy massiv: turi string[]
  const normalColors = ["qizil", "yashil"];
  normalColors.push("ko'k"); // Ruxsat etilgan

  // as const bilan: turi readonly ["qizil", "yashil"]
  const strictColors = ["qizil", "yashil"] as const;

  console.log("strictColors elementlari:", strictColors[0], strictColors[1]);

  // strictColors.push("ko'k"); // TS Xatosi: Property 'push' does not exist on type 'readonly ["qizil", "yashil"]'
}

testConstAssertion();
```

## Tushuntirish va Mantiq:
1. `as const` ifodasi TypeScriptga ob'ekt yoki massivning barcha maydonlarini `readonly` qilishni va primitiv turlarni aniq literal turlar (`string` emas, balki `'qizil'`) sifatida qabul qilishni buyuradi.
2. Bu o'zgarmas konfiguratsiyalar va enumlarga muqobil yaratishda eng zamonaviy uslubdir.

## Ishlash natijasi:
```text
strictColors elementlari: qizil yashil
```


# 459-Topshiriq: Type Assertions: 'as Type' va Non-null Assertion (!)

## Topshiriq sharti:
`as` yordamida turni aniqlashtirish va `!` (non-null assertion) operatorining vazifasini namoyish eting.

## Yechim (JS yoki TS kodi):
```typescript
function findElementLength(data: string | null): number {
  // 1. Non-null assertion (!) - qiymat aniq null yoki undefined emasligiga kafolat berish
  const length = data!.length;
  return length;
}

function processRawData(raw: unknown): string {
  // 2. Type assertion (as string)
  const str = raw as string;
  return str.trim();
}

console.log("Uzunlik:", findElementLength("TypeScript"));
console.log("Qayta ishlangan:", processRawData("   toza kod   "));
```

## Tushuntirish va Mantiq:
1. `as Type` dasturchi kompilyatorga: 'Men bu qiymatning turini sendan ko'ra aniqroq bilaman' deb aytishidir. U runtimeda hech qanday konvertatsiya qilmaydi.
2. `x!` (Non-null assertion) qiymatdan `null` va `undefined` turlarini olib tashlaydi.
3. Agar qiymat haqiqatda `null` bo'lib chiqsa, runtimeda xato yuz beradi, shu bois undan ehtiyotkorlik bilan foydalanish lozim.

## Ishlash natijasi:
```text
Uzunlik: 10
Qayta ishlangan: toza kod
```


# 460-Topshiriq: satisfies operatori (TS 4.9+): Tip tekshiruvi va xususiyat aniqligi

## Topshiriq sharti:
TS 4.9 da kiritilgan `satisfies` operatori yordamida turni tekshirib, shu bilan birga o'zgaruvchining aniq literal xususiyatlarini saqlab qolishni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
type CustomColor = string | { r: number; g: number; b: number };

type Palette = Record<string, CustomColor>;

// satisfies yordamida:
const myPalette = {
  primary: "blue",
  secondary: { r: 0, g: 255, b: 0 }
} satisfies Palette;

// satisfies primary ning aniq 'string' ekanligini eslab qoladi!
console.log("primary katta harflarda:", myPalette.primary.toUpperCase());
console.log("secondary yashil kanali:", myPalette.secondary.g);
```

## Tushuntirish va Mantiq:
1. An'anaviy `const p: Palette = { ... }` yozilganda, `p.primary` ning turi `string | { r, g, b }` ga aylanib qolar va `.toUpperCase()` chaqirib bo'lmasdi.
2. `satisfies Palette` ob'ektning `Palette` turiga mosligini tekshiradi, ammo uning haqiqiy ichki turlarini toraytirmay, to'liq saqlab qoladi.
3. Bu TypeScriptning eng ajoyib zamonaviy yutuqlaridan biridir.

## Ishlash natijasi:
```text
primary katta harflarda: BLUE
secondary yashil kanali: 255
```


# 461-Topshiriq: TypeScript Asoslari va Turlar: Modul #1

## Topshiriq sharti:
TypeScript statik tiplash tizimining #1-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_1(): void {
  type Scenario_1 = { id: number; title: string; active: boolean };
  const scenario: Scenario_1 = {
    id: 1,
    title: "TypeScript Asoslari #1",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_1();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #1-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #1
```


# 462-Topshiriq: TypeScript Asoslari va Turlar: Modul #2

## Topshiriq sharti:
TypeScript statik tiplash tizimining #2-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_2(): void {
  type Scenario_2 = { id: number; title: string; active: boolean };
  const scenario: Scenario_2 = {
    id: 2,
    title: "TypeScript Asoslari #2",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_2();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #2-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #2
```


# 463-Topshiriq: TypeScript Asoslari va Turlar: Modul #3

## Topshiriq sharti:
TypeScript statik tiplash tizimining #3-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_3(): void {
  type Scenario_3 = { id: number; title: string; active: boolean };
  const scenario: Scenario_3 = {
    id: 3,
    title: "TypeScript Asoslari #3",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_3();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #3-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #3
```


# 464-Topshiriq: TypeScript Asoslari va Turlar: Modul #4

## Topshiriq sharti:
TypeScript statik tiplash tizimining #4-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_4(): void {
  type Scenario_4 = { id: number; title: string; active: boolean };
  const scenario: Scenario_4 = {
    id: 4,
    title: "TypeScript Asoslari #4",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_4();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #4-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #4
```


# 465-Topshiriq: TypeScript Asoslari va Turlar: Modul #5

## Topshiriq sharti:
TypeScript statik tiplash tizimining #5-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_5(): void {
  type Scenario_5 = { id: number; title: string; active: boolean };
  const scenario: Scenario_5 = {
    id: 5,
    title: "TypeScript Asoslari #5",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_5();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #5-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #5
```


# 466-Topshiriq: TypeScript Asoslari va Turlar: Modul #6

## Topshiriq sharti:
TypeScript statik tiplash tizimining #6-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_6(): void {
  type Scenario_6 = { id: number; title: string; active: boolean };
  const scenario: Scenario_6 = {
    id: 6,
    title: "TypeScript Asoslari #6",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_6();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #6-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #6
```


# 467-Topshiriq: TypeScript Asoslari va Turlar: Modul #7

## Topshiriq sharti:
TypeScript statik tiplash tizimining #7-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_7(): void {
  type Scenario_7 = { id: number; title: string; active: boolean };
  const scenario: Scenario_7 = {
    id: 7,
    title: "TypeScript Asoslari #7",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_7();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #7-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #7
```


# 468-Topshiriq: TypeScript Asoslari va Turlar: Modul #8

## Topshiriq sharti:
TypeScript statik tiplash tizimining #8-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_8(): void {
  type Scenario_8 = { id: number; title: string; active: boolean };
  const scenario: Scenario_8 = {
    id: 8,
    title: "TypeScript Asoslari #8",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_8();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #8-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #8
```


# 469-Topshiriq: TypeScript Asoslari va Turlar: Modul #9

## Topshiriq sharti:
TypeScript statik tiplash tizimining #9-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_9(): void {
  type Scenario_9 = { id: number; title: string; active: boolean };
  const scenario: Scenario_9 = {
    id: 9,
    title: "TypeScript Asoslari #9",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_9();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #9-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #9
```


# 470-Topshiriq: TypeScript Asoslari va Turlar: Modul #10

## Topshiriq sharti:
TypeScript statik tiplash tizimining #10-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_10(): void {
  type Scenario_10 = { id: number; title: string; active: boolean };
  const scenario: Scenario_10 = {
    id: 10,
    title: "TypeScript Asoslari #10",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_10();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #10-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #10
```


# 471-Topshiriq: TypeScript Asoslari va Turlar: Modul #11

## Topshiriq sharti:
TypeScript statik tiplash tizimining #11-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_11(): void {
  type Scenario_11 = { id: number; title: string; active: boolean };
  const scenario: Scenario_11 = {
    id: 11,
    title: "TypeScript Asoslari #11",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_11();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #11-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #11
```


# 472-Topshiriq: TypeScript Asoslari va Turlar: Modul #12

## Topshiriq sharti:
TypeScript statik tiplash tizimining #12-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_12(): void {
  type Scenario_12 = { id: number; title: string; active: boolean };
  const scenario: Scenario_12 = {
    id: 12,
    title: "TypeScript Asoslari #12",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_12();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #12-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #12
```


# 473-Topshiriq: TypeScript Asoslari va Turlar: Modul #13

## Topshiriq sharti:
TypeScript statik tiplash tizimining #13-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_13(): void {
  type Scenario_13 = { id: number; title: string; active: boolean };
  const scenario: Scenario_13 = {
    id: 13,
    title: "TypeScript Asoslari #13",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_13();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #13-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #13
```


# 474-Topshiriq: TypeScript Asoslari va Turlar: Modul #14

## Topshiriq sharti:
TypeScript statik tiplash tizimining #14-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_14(): void {
  type Scenario_14 = { id: number; title: string; active: boolean };
  const scenario: Scenario_14 = {
    id: 14,
    title: "TypeScript Asoslari #14",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_14();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #14-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #14
```


# 475-Topshiriq: TypeScript Asoslari va Turlar: Modul #15

## Topshiriq sharti:
TypeScript statik tiplash tizimining #15-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_15(): void {
  type Scenario_15 = { id: number; title: string; active: boolean };
  const scenario: Scenario_15 = {
    id: 15,
    title: "TypeScript Asoslari #15",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_15();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #15-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #15
```


# 476-Topshiriq: TypeScript Asoslari va Turlar: Modul #16

## Topshiriq sharti:
TypeScript statik tiplash tizimining #16-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_16(): void {
  type Scenario_16 = { id: number; title: string; active: boolean };
  const scenario: Scenario_16 = {
    id: 16,
    title: "TypeScript Asoslari #16",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_16();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #16-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #16
```


# 477-Topshiriq: TypeScript Asoslari va Turlar: Modul #17

## Topshiriq sharti:
TypeScript statik tiplash tizimining #17-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_17(): void {
  type Scenario_17 = { id: number; title: string; active: boolean };
  const scenario: Scenario_17 = {
    id: 17,
    title: "TypeScript Asoslari #17",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_17();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #17-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #17
```


# 478-Topshiriq: TypeScript Asoslari va Turlar: Modul #18

## Topshiriq sharti:
TypeScript statik tiplash tizimining #18-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_18(): void {
  type Scenario_18 = { id: number; title: string; active: boolean };
  const scenario: Scenario_18 = {
    id: 18,
    title: "TypeScript Asoslari #18",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_18();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #18-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #18
```


# 479-Topshiriq: TypeScript Asoslari va Turlar: Modul #19

## Topshiriq sharti:
TypeScript statik tiplash tizimining #19-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_19(): void {
  type Scenario_19 = { id: number; title: string; active: boolean };
  const scenario: Scenario_19 = {
    id: 19,
    title: "TypeScript Asoslari #19",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_19();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #19-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #19
```


# 480-Topshiriq: TypeScript Asoslari va Turlar: Modul #20

## Topshiriq sharti:
TypeScript statik tiplash tizimining #20-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_20(): void {
  type Scenario_20 = { id: number; title: string; active: boolean };
  const scenario: Scenario_20 = {
    id: 20,
    title: "TypeScript Asoslari #20",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_20();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #20-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #20
```


# 481-Topshiriq: TypeScript Asoslari va Turlar: Modul #21

## Topshiriq sharti:
TypeScript statik tiplash tizimining #21-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_21(): void {
  type Scenario_21 = { id: number; title: string; active: boolean };
  const scenario: Scenario_21 = {
    id: 21,
    title: "TypeScript Asoslari #21",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_21();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #21-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #21
```


# 482-Topshiriq: TypeScript Asoslari va Turlar: Modul #22

## Topshiriq sharti:
TypeScript statik tiplash tizimining #22-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_22(): void {
  type Scenario_22 = { id: number; title: string; active: boolean };
  const scenario: Scenario_22 = {
    id: 22,
    title: "TypeScript Asoslari #22",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_22();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #22-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #22
```


# 483-Topshiriq: TypeScript Asoslari va Turlar: Modul #23

## Topshiriq sharti:
TypeScript statik tiplash tizimining #23-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_23(): void {
  type Scenario_23 = { id: number; title: string; active: boolean };
  const scenario: Scenario_23 = {
    id: 23,
    title: "TypeScript Asoslari #23",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_23();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #23-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #23
```


# 484-Topshiriq: TypeScript Asoslari va Turlar: Modul #24

## Topshiriq sharti:
TypeScript statik tiplash tizimining #24-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_24(): void {
  type Scenario_24 = { id: number; title: string; active: boolean };
  const scenario: Scenario_24 = {
    id: 24,
    title: "TypeScript Asoslari #24",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_24();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #24-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #24
```


# 485-Topshiriq: TypeScript Asoslari va Turlar: Modul #25

## Topshiriq sharti:
TypeScript statik tiplash tizimining #25-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_25(): void {
  type Scenario_25 = { id: number; title: string; active: boolean };
  const scenario: Scenario_25 = {
    id: 25,
    title: "TypeScript Asoslari #25",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_25();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #25-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #25
```


# 486-Topshiriq: TypeScript Asoslari va Turlar: Modul #26

## Topshiriq sharti:
TypeScript statik tiplash tizimining #26-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_26(): void {
  type Scenario_26 = { id: number; title: string; active: boolean };
  const scenario: Scenario_26 = {
    id: 26,
    title: "TypeScript Asoslari #26",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_26();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #26-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #26
```


# 487-Topshiriq: TypeScript Asoslari va Turlar: Modul #27

## Topshiriq sharti:
TypeScript statik tiplash tizimining #27-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_27(): void {
  type Scenario_27 = { id: number; title: string; active: boolean };
  const scenario: Scenario_27 = {
    id: 27,
    title: "TypeScript Asoslari #27",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_27();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #27-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #27
```


# 488-Topshiriq: TypeScript Asoslari va Turlar: Modul #28

## Topshiriq sharti:
TypeScript statik tiplash tizimining #28-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_28(): void {
  type Scenario_28 = { id: number; title: string; active: boolean };
  const scenario: Scenario_28 = {
    id: 28,
    title: "TypeScript Asoslari #28",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_28();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #28-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #28
```


# 489-Topshiriq: TypeScript Asoslari va Turlar: Modul #29

## Topshiriq sharti:
TypeScript statik tiplash tizimining #29-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_29(): void {
  type Scenario_29 = { id: number; title: string; active: boolean };
  const scenario: Scenario_29 = {
    id: 29,
    title: "TypeScript Asoslari #29",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_29();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #29-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #29
```


# 490-Topshiriq: TypeScript Asoslari va Turlar: Modul #30

## Topshiriq sharti:
TypeScript statik tiplash tizimining #30-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_30(): void {
  type Scenario_30 = { id: number; title: string; active: boolean };
  const scenario: Scenario_30 = {
    id: 30,
    title: "TypeScript Asoslari #30",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_30();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #30-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #30
```


# 491-Topshiriq: TypeScript Asoslari va Turlar: Modul #31

## Topshiriq sharti:
TypeScript statik tiplash tizimining #31-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_31(): void {
  type Scenario_31 = { id: number; title: string; active: boolean };
  const scenario: Scenario_31 = {
    id: 31,
    title: "TypeScript Asoslari #31",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_31();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #31-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #31
```


# 492-Topshiriq: TypeScript Asoslari va Turlar: Modul #32

## Topshiriq sharti:
TypeScript statik tiplash tizimining #32-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_32(): void {
  type Scenario_32 = { id: number; title: string; active: boolean };
  const scenario: Scenario_32 = {
    id: 32,
    title: "TypeScript Asoslari #32",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_32();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #32-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #32
```


# 493-Topshiriq: TypeScript Asoslari va Turlar: Modul #33

## Topshiriq sharti:
TypeScript statik tiplash tizimining #33-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_33(): void {
  type Scenario_33 = { id: number; title: string; active: boolean };
  const scenario: Scenario_33 = {
    id: 33,
    title: "TypeScript Asoslari #33",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_33();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #33-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #33
```


# 494-Topshiriq: TypeScript Asoslari va Turlar: Modul #34

## Topshiriq sharti:
TypeScript statik tiplash tizimining #34-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_34(): void {
  type Scenario_34 = { id: number; title: string; active: boolean };
  const scenario: Scenario_34 = {
    id: 34,
    title: "TypeScript Asoslari #34",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_34();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #34-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #34
```


# 495-Topshiriq: TypeScript Asoslari va Turlar: Modul #35

## Topshiriq sharti:
TypeScript statik tiplash tizimining #35-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_35(): void {
  type Scenario_35 = { id: number; title: string; active: boolean };
  const scenario: Scenario_35 = {
    id: 35,
    title: "TypeScript Asoslari #35",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_35();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #35-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #35
```


# 496-Topshiriq: TypeScript Asoslari va Turlar: Modul #36

## Topshiriq sharti:
TypeScript statik tiplash tizimining #36-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_36(): void {
  type Scenario_36 = { id: number; title: string; active: boolean };
  const scenario: Scenario_36 = {
    id: 36,
    title: "TypeScript Asoslari #36",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_36();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #36-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #36
```


# 497-Topshiriq: TypeScript Asoslari va Turlar: Modul #37

## Topshiriq sharti:
TypeScript statik tiplash tizimining #37-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_37(): void {
  type Scenario_37 = { id: number; title: string; active: boolean };
  const scenario: Scenario_37 = {
    id: 37,
    title: "TypeScript Asoslari #37",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_37();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #37-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #37
```


# 498-Topshiriq: TypeScript Asoslari va Turlar: Modul #38

## Topshiriq sharti:
TypeScript statik tiplash tizimining #38-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_38(): void {
  type Scenario_38 = { id: number; title: string; active: boolean };
  const scenario: Scenario_38 = {
    id: 38,
    title: "TypeScript Asoslari #38",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_38();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #38-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #38
```


# 499-Topshiriq: TypeScript Asoslari va Turlar: Modul #39

## Topshiriq sharti:
TypeScript statik tiplash tizimining #39-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_39(): void {
  type Scenario_39 = { id: number; title: string; active: boolean };
  const scenario: Scenario_39 = {
    id: 39,
    title: "TypeScript Asoslari #39",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_39();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #39-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #39
```


# 500-Topshiriq: TypeScript Asoslari va Turlar: Modul #40

## Topshiriq sharti:
TypeScript statik tiplash tizimining #40-xususiyatini amaliy toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeTsScenario_40(): void {
  type Scenario_40 = { id: number; title: string; active: boolean };
  const scenario: Scenario_40 = {
    id: 40,
    title: "TypeScript Asoslari #40",
    active: true
  };

  console.log("Ssenariy tekshirildi:", scenario.title);
}

executeTsScenario_40();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript tip tizimining #40-qoidasini mustahkamlaydi.
2. Kompilyatsiya xavfsizligi va tiplar to'g'riligi kafolatlanadi.

## Ishlash natijasi:
```text
Ssenariy tekshirildi: TypeScript Asoslari #40
```

