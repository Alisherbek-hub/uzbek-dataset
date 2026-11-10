# 51-Topshiriq: Arifmetik operatorlar va darajaga ko'tarish (**)

## Topshiriq sharti:
JavaScriptda arifmetik amallar (+, -, *, /, %, **) va Math.pow o'rniga ES2016 ning daraja operatorini (`**`) qo'llab murakkab ifodalarni hisoblovchi funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
function calculateFormulas(radius: number, power: number): void {
  const pi = 3.14159;
  // Aylana yuzi: S = pi * r^2
  const area = pi * (radius ** 2);
  console.log(`Radius ${radius} bo'lgan doira yuzi:`, area.toFixed(2));

  // Katta darajalar: 2^10
  const twoPower = 2 ** power;
  console.log(`2 ning ${power}-darajasi:`, twoPower);

  // Darajalar ketma-ketligi o'ngdan chapga hisoblanadi: 2 ** 3 ** 2 = 2 ** 9 = 512
  const rightAssociative = 2 ** 3 ** 2;
  console.log("2 ** 3 ** 2 (o'ngdan chapga):", rightAssociative);
}

calculateFormulas(5, 10);
```

## Tushuntirish va Mantiq:
1. ES2016 (ES7) da kiritilgan `**` operatori `Math.pow()` funksiyasining qisqa va qulay sintaktik shaklidir.
2. `**` operatori o'ngdan chapga (right-associative) bajariladi, ya'ni `2 ** 3 ** 2` ifodasi `2 ** (3 ** 2) = 2 ** 9 = 512` tarzida hisoblanadi.
3. Manfiy sonlarni darajaga ko'tarishda qavs qo'yish shart: `(-2) ** 2 = 4`, aks holda sintaktik xato beradi.

## Ishlash natijasi:
```text
Radius 5 bo'lgan doira yuzi: 78.54
2 ning 10-darajasi: 1024
2 ** 3 ** 2 (o'ngdan chapga): 512
```


# 52-Topshiriq: Unar plyus (+) va unar minus (-): Tip o'zgartirish va ishora almashtirish

## Topshiriq sharti:
Unar plyus va minus operatorlari orqali satrlarni sonlarga aylantirish va sonlarning ishorasini o'zgartirish amallarini namoyish eting.

## Yechim (JS yoki TS kodi):
```typescript
function testUnaryOperators(): void {
  const priceStr = "450.50";
  const quantityStr = "3";

  // Unar plyus satrni tezkor raqamga aylantiradi
  const price = +priceStr;
  const quantity = +quantityStr;
  const total = price * quantity;

  console.log("Unar plyus orqali jami summa:", total);
  console.log("typeof +priceStr:", typeof price);

  // Unar minus qiymatni manfiyga aylantiradi yoki songa o'girib ishorasini o'zgartiradi
  const discount = -50;
  console.log("-discount (qarama-qarshi ishora):", -discount);
  console.log("-'100':", -"100");
}

testUnaryOperators();
```

## Tushuntirish va Mantiq:
1. Unar plyus (`+x`) `Number(x)` bilan aynan bir xil ishlaydi, ammo sintaktik jihatdan ancha qisqa va tezkor.
2. Unar minus (`-x`) esa qiymatni songa aylantiradi va uning arifmetik ishorasini teskarisiga o'zgartiradi.
3. Agar satrda noaniq belgilar bo'lsa, natija `NaN` bo'ladi.

## Ishlash natijasi:
```text
Unar plyus orqali jami summa: 1351.5
typeof +priceStr: number
-discount (qarama-qarshi ishora): 50
-'100': -100
```


# 53-Topshiriq: Prefiks (++x) va Postfiks (x++) inkrement/dekrement farqi

## Topshiriq sharti:
Prefiks (`++a`) va postfiks (`b++`) inkrementlarining ifoda ichida beradigan qiymatlari va o'zgaruvchiga ta'sirini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function compareIncrements(): void {
  let a = 5;
  let b = 5;

  // Prefiks: avval qiymat oshiriladi, so'ng ifodaga qaytariladi
  const prefixResult = ++a;
  console.log(`Prefiks: a = ${a}, ifoda natijasi = ${prefixResult}`);

  // Postfiks: avval joriy qiymat qaytariladi, so'ng o'zgaruvchi oshiriladi
  const postfixResult = b++;
  console.log(`Postfiks: b = ${b}, ifoda natijasi = ${postfixResult}`);

  // Murakkab ifodada
  let c = 10;
  const complex = c++ + ++c;
  // c++ -> 10 beradi, c=11 bo'ladi. Keyin ++c -> c=12 bo'ladi, 12 beradi. 10 + 12 = 22
  console.log(`Murakkab hisob (c++ + ++c): ${complex}, yakuniy c: ${c}`);
}

compareIncrements();
```

## Tushuntirish va Mantiq:
1. `++x` (prefiks) qiymatni darhol 1 ga oshiradi va yangilangan qiymatni qaytaradi.
2. `x++` (postfiks) o'zgaruvchining joriy qiymatini ifodaga beradi, ammo xotirada uni 1 ga oshirib qo'yadi.
3. Murakkab arifmetik ifodalarda postfiks va prefikslarni aralashtirib yozish kodning o'qilishini qiyinlashtiradi, shuning uchun ularni alohida qatorda yozish eng yaxshi amaliyotdir.

## Ishlash natijasi:
```text
Prefiks: a = 6, ifoda natijasi = 6
Postfiks: b = 6, ifoda natijasi = 5
Murakkab hisob (c++ + ++c): 22, yakuniy c: 12
```


# 54-Topshiriq: Mantiqiy VA (&&) va Short-Circuit (Qisqa tutashuv) baholash

## Topshiriq sharti:
`&&` operatorining birinchi uchragan Falsy qiymatni qaytarishi (short-circuit) orqali shartli chaqiruvlarni xavfsiz amalga oshirishni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function testLogicalAnd(): void {
  const user = {
    isLoggedIn: true,
    profile: {
      name: "Sherzod",
      email: "sherzod@example.com"
    }
  };

  // Faqat login qilgan bo'lsa profil nomini olamiz
  const profileName = user.isLoggedIn && user.profile.name;
  console.log("Profil nomi:", profileName);

  // Short-circuit: birinchi falsy da to'xtaydi va keyingi qismni bajarmaydi
  let executed = false;
  const shouldNotRun = () => {
    executed = true;
    return "Ishladi";
  };

  const check = false && shouldNotRun();
  console.log("Natija:", check, "| Funksiya chaqirildimi:", executed);
}

testLogicalAnd();
```

## Tushuntirish va Mantiq:
1. Mantiqiy VA (`&&`) chapdan o'ngga qarab qiymatlarni tekshiradi.
2. Agar birorta Falsy qiymat uchrasa, darhol o'sha Falsy qiymatni qaytaradi va o'ng tomondagi ifodalarni umuman hisoblamaydi (short-circuit).
3. Agar hamma qiymat Truthy bo'lsa, eng oxirgi qiymat qaytariladi.
4. Bu xususiyat shartli render qilishda va null-pointer xatolaridan saqlanishda keng qo'llaniladi.

## Ishlash natijasi:
```text
Profil nomi: Sherzod
Natija: false | Funksiya chaqirildimi: false
```


# 55-Topshiriq: Mantiqiy YOKI (||) va Boshlang'ich (Default) qiymat belgilash

## Topshiriq sharti:
`||` operatori orqali o'zgaruvchilarga zaxira (fallback) qiymat berish va uning 0 yoki bo'sh satr bilan ishlashdagi kamchiligini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function setupConfig(customTimeout?: number, customTitle?: string): void {
  // || birinchi Truthy qiymatni qaytaradi
  const timeout = customTimeout || 5000;
  const title = customTitle || "Bosh sahifa";

  console.log(`Timeout: ${timeout}ms, Sarlavha: '${title}'`);
}

function demonstrateLogicalOr(): void {
  console.log("1. Argumentlar berilmaganda:");
  setupConfig();

  console.log("2. 0 va bo'sh satr berilganda (|| ning muammosi):");
  setupConfig(0, ""); // 0 va "" falsy bo'lgani uchun default qiymatga o'tib ketadi!
}

demonstrateLogicalOr();
```

## Tushuntirish va Mantiq:
1. Mantiqiy YOKI (`||`) birinchi uchragan Truthy qiymatni qaytaradi. Agar hamma qiymat Falsy bo'lsa, eng oxirgi Falsy qiymat qaytadi.
2. Qadimdan bu usul default parametrlar berishda ishlatilgan.
3. Biroq `0`, `""` (bo'sh satr) yoki `false` kabi qonuniy qiymatlar kiritilganda `||` ularni xato deb hisoblab, zaxira qiymatni tanlaydi.
4. Bu muammoni bartaraf etish uchun ES2020 da Nullish Coalescing (`??`) kiritilgan.

## Ishlash natijasi:
```text
1. Argumentlar berilmaganda:
Timeout: 5000ms, Sarlavha: 'Bosh sahifa'
2. 0 va bo'sh satr berilganda (|| ning muammosi):
Timeout: 5000ms, Sarlavha: 'Bosh sahifa'
```


# 56-Topshiriq: Mantiqiy EMAS (!) va Double Negation (!!) orqali Booleanga o'tkazish

## Topshiriq sharti:
`!` va `!!` operatorlari yordamida obyektlar, satrlar va sonlarni sof `boolean` turiga xavfsiz o'tkazish funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function checkUserAccess(token: string | null, role?: string): boolean {
  // !! qiymatning mavjudligini qat'iy true/false ga o'tkazadi
  const hasToken = !!token;
  const isAdmin = !!(role && role === "admin");

  console.log(`hasToken: ${hasToken}, isAdmin: ${isAdmin}`);
  return hasToken && isAdmin;
}

function demonstrateDoubleNegation(): void {
  console.log("!!'salom':", !!"salom");
  console.log("!!'':", !!"");
  console.log("!!0:", !!0);
  console.log("!!100:", !!100);
  console.log("!!null:", !!null);
  console.log("!!undefined:", !!undefined);

  console.log("Kirish ruxsati:", checkUserAccess("jwt_token_123", "admin"));
}

demonstrateDoubleNegation();
```

## Tushuntirish va Mantiq:
1. Birinchi inkor (`!x`) qiymatni boolean turiga o'giradi va uni teskari qiladi (truthy -> false, falsy -> true).
2. Ikkinchi inkor (`!!x`) yana teskarisiga o'giradi, natijada qiymatning asl rostlik darajasi sof `boolean` (`true` yoki `false`) qiymat sifatida saqlanib qoladi.
3. Bu usul `Boolean(x)` funksiyasining qisqa va qulay ekvivalentidir.

## Ishlash natijasi:
```text
!!'salom': true
!!'': false
!!0: false
!!100: true
!!null: false
!!undefined: false
hasToken: true, isAdmin: true
Kirish ruxsati: true
```


# 57-Topshiriq: Nullish Coalescing (??) va || o'rtasidagi tub farq

## Topshiriq sharti:
`??` (Nullish Coalescing) operatori yordamida `null` va `undefined` bilan `0` va `""` kabi qonuniy qiymatlarni to'g'ri ajratuvchi konfiguratsiya yuklagichini yozing.

## Yechim (JS yoki TS kodi):
```typescript
interface AppConfig {
  port?: number;
  appName?: string;
  debugMode?: boolean;
}

function initApp(options: AppConfig): void {
  // ?? faqat null va undefined bo'lgandagina zaxira qiymatga o'tadi
  const port = options.port ?? 3000;
  const appName = options.appName ?? "Standart Ilova";
  const debug = options.debugMode ?? true;

  console.log(`Ilova: '${appName}', Port: ${port}, Debug: ${debug}`);
}

function testNullishCoalescing(): void {
  // port 0 (qonuniy port), appName bo'sh satr, debug esa ataylab false
  initApp({ port: 0, appName: "", debugMode: false });
}

testNullishCoalescing();
```

## Tushuntirish va Mantiq:
1. `||` operatori har qanday Falsy qiymatda (`0`, `""`, `false`, `NaN`, `null`, `undefined`) zaxiraga o'tadi.
2. `??` (Nullish Coalescing) esa FAQAT VA FAQAT chap tomon `null` yoki `undefined` bo'lgandagina o'ng tomonga o'tadi.
3. Agar qiymat `0`, `""` yoki `false` bo'lsa, `??` ularni qonuniy qiymat deb hisoblaydi va saqlab qoladi.
4. Bu parametrlar va konfiguratsiyalarda kutilmagan buzilishlarning oldini oladi.

## Ishlash natijasi:
```text
Ilova: '', Port: 0, Debug: false
```


# 58-Topshiriq: Nullish Coalescing Assignment (??=) operatori

## Topshiriq sharti:
ES2021 da kiritilgan `??=` operatori yordamida obyektdagi faqat `null` yoki `undefined` bo'lgan maydonlarga qiymat biriktirishni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
interface UserProfile {
  username: string;
  theme?: string | null;
  visits?: number;
}

function populateDefaults(user: UserProfile): void {
  // Agar theme null yoki undefined bo'lsa 'dark' qilinadi
  user.theme ??= "dark";
  // Agar visits null yoki undefined bo'lsa 1 qilinadi
  user.visits ??= 1;
}

const user1: UserProfile = { username: "aziza", theme: null, visits: 0 };
populateDefaults(user1);

console.log("Foydalanuvchi profili:");
console.log(`Username: ${user1.username}, Theme: ${user1.theme}, Visits: ${user1.visits}`);
```

## Tushuntirish va Mantiq:
1. `x ??= y` ifodasi `x ?? (x = y)` ma'nosini bildiradi.
2. Agar `x` allaqachon `null` yoki `undefined` bo'lmagan qiymatga ega bo'lsa (masalan `visits: 0`), unga yangi qiymat o'zlashtirilmaydi.
3. Bu usul bo'sh maydonlarni default qiymatlar bilan to'ldirishda juda ixcham va toza sintaksis beradi.

## Ishlash natijasi:
```text
Foydalanuvchi profili:
Username: aziza, Theme: dark, Visits: 0
```


# 59-Topshiriq: Logical OR Assignment (||=) va Logical AND Assignment (&&=)

## Topshiriq sharti:
`||=` va `&&=` operatorlarining qanday ishlashini va ularning holat yangilashdagi qulayligini namoyish eting.

## Yechim (JS yoki TS kodi):
```typescript
function testLogicalAssignments(): void {
  // ||= : Agar falsy bo'lsa, yangi qiymat oladi
  let message = "";
  message ||= "Standart xabar";
  console.log("||= natijasi:", message);

  let existingTitle = "Mavjud Sarlavha";
  existingTitle ||= "Yangi Sarlavha";
  console.log("Mavjud sarlavha ||= keyin:", existingTitle);

  // &&= : Agar truthy bo'lsa, yangi qiymat bilan yangilanadi
  let userSession: any = { active: true };
  userSession &&= { active: false, terminatedAt: "2026-11-08" };
  console.log("&&= natijasi:", userSession);

  let emptySession: any = null;
  emptySession &&= { active: true };
  console.log("emptySession &&= keyin:", emptySession);
}

testLogicalAssignments();
```

## Tushuntirish va Mantiq:
1. `x ||= y`: faqat `x` falsy bo'lgandagina `x = y` o'zlashtirishini amalga oshiradi.
2. `x &&= y`: faqat `x` truthy bo'lgandagina `x = y` o'zlashtirishini amalga oshiradi.
3. Ushbu mantiqiy o'zlashtirish operatorlari ES2021 da kiritilgan bo'lib, ortiqcha `if` shartlarisiz qiymat berishni soddalashtiradi.

## Ishlash natijasi:
```text
||= natijasi: Standart xabar
Mavjud sarlavha ||= keyin: Mavjud Sarlavha
&&= natijasi: { active: false, terminatedAt: '2026-11-08' }
emptySession &&= keyin: null
```


# 60-Topshiriq: Optional Chaining (?.) - Chuqur obyekt zanjirlariga xavfsiz murojaat

## Topshiriq sharti:
Chuqur kiritilgan (nested) obyektlarda mavjud bo'lmagan xususiyatlarga murojaat qilishda `TypeError` oldini olish uchun `?.` operatorini qo'llang.

## Yechim (JS yoki TS kodi):
```typescript
interface Company {
  name: string;
  address?: {
    city?: string;
    geo?: {
      lat: number;
      lng: number;
    };
  };
}

function printGeoLocation(company: Company): void {
  // An'anaviy usul: company && company.address && company.address.geo && company.address.geo.lat
  // Zamonaviy usul: Optional Chaining (?.)
  const latitude = company.address?.geo?.lat ?? 0;
  const longitude = company.address?.geo?.lng ?? 0;

  console.log(`${company.name} koordinatalari: lat = ${latitude}, lng = ${longitude}`);
}

const c1: Company = {
  name: "Tech Corp",
  address: { city: "Toshkent", geo: { lat: 41.2995, lng: 69.2401 } }
};

const c2: Company = {
  name: "StartUp Soft"
  // address yo'q
};

printGeoLocation(c1);
printGeoLocation(c2);
```

## Tushuntirish va Mantiq:
1. Agar zanjirning biron bir bo'g'ini `null` yoki `undefined` bo'lsa, `?.` amali butun ifodani darhol to'xtatadi va xatolik tashlamasdan `undefined` qaytaradi.
2. Nullish coalescing (`??`) bilan birga qo'llanganda, zanjir uzilsa ham standart default qiymatni osongina qaytarish mumkin.
3. Bu backenddan to'liq kelmagan API javoblarini qayta ishlashda eng muhim vositadir.

## Ishlash natijasi:
```text
Tech Corp koordinatalari: lat = 41.2995, lng = 69.2401
StartUp Soft koordinatalari: lat = 0, lng = 0
```


# 61-Topshiriq: Optional Chaining massiv indekslari bilan (arr?.[index])

## Topshiriq sharti:
Massivlar mavjud bo'lmasligi yoki indeks chegaradan tashqarida bo'lishi mumkin bo'lgan holatlarda `?.[]` sintaksisidan foydalanishni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function getFirstItem(data: { items?: string[] } | null): string {
  // data bo'lmasligi yoki data.items bo'lmasligi mumkin
  const first = data?.items?.[0] ?? "Element topilmadi";
  return first;
}

console.log("1. To'liq ma'lumot:", getFirstItem({ items: ["Olma", "Nok"] }));
console.log("2. Bo'sh massiv:", getFirstItem({ items: [] }));
console.log("3. items maydoni yo'q:", getFirstItem({}));
console.log("4. null uzatilganda:", getFirstItem(null));
```

## Tushuntirish va Mantiq:
1. `obj?.[prop]` yoki `arr?.[index]` sintaksisi dinamik kalitlar va massiv indekslari uchun optional chaining imkoniyatini beradi.
2. Agar massiv yoki obyekt `null` yoki `undefined` bo'lsa, indeksga kirishda xato yuz bermaydi, balki xavfsiz `undefined` qaytadi.
3. Bo'sh massiv `[]` uchun `[0]` indeksi tabiiy ravishda `undefined` beradi.

## Ishlash natijasi:
```text
1. To'liq ma'lumot: Olma
2. Bo'sh massiv: Element topilmadi
3. items maydoni yo'q: Element topilmadi
4. null uzatilganda: Element topilmadi
```


# 62-Topshiriq: Optional Chaining funksiya chaqiruvlari bilan (obj.method?.())

## Topshiriq sharti:
Obyektdagi callback funksiyalari mavjud bo'lmasligi mumkin bo'lgan holatda `fn?.()` sintaksisi orqali ularni xavfsiz chaqiring.

## Yechim (JS yoki TS kodi):
```typescript
interface EventHandler {
  onSuccess?: (msg: string) => void;
  onError?: (err: Error) => void;
}

function executeTask(actionName: string, handlers?: EventHandler): void {
  console.log(`Vazifa bajarilmoqda: ${actionName}`);

  // Callback funksiya berilgan bo'lsagina ishga tushadi
  handlers?.onSuccess?.(`${actionName} muvaffaqiyatli yakunlandi!`);
}

// 1. Handlers umuman berilmagan
executeTask("Fayl yuklash");

// 2. Handlers berilgan
executeTask("Ma'lumotlar bazasini yangilash", {
  onSuccess: (msg) => console.log("Xabar olindi:", msg)
});
```

## Tushuntirish va Mantiq:
1. `obj.callback?.(args)` agar `callback` mavjud bo'lmasa yoki funksiya bo'lmasa, uni chaqirmaydi va hech qanday xato chiqarmaydi.
2. Bu usul `if (obj && typeof obj.callback === 'function') obj.callback(args)` tekshiruvini bitta chiroyli qatorga almashtiradi.
3. Event listenerlar va opsional parametrli modullarda nihoyatda samarali.

## Ishlash natijasi:
```text
Vazifa bajarilmoqda: Fayl yuklash
Vazifa bajarilmoqda: Ma'lumotlar bazasini yangilash
Xabar olindi: Ma'lumotlar bazasini yangilash muvaffaqiyatli yakunlandi!
```


# 63-Topshiriq: Ternary operator (? :) bilan shartli qiymat tanlash

## Topshiriq sharti:
Ternar operator yordamida buyurtma summasiga qarab yetkazib berish narxini hisoblovchi ixcham funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
function calculateDelivery(orderTotal: number): number {
  // Agar buyurtma 100,000 so'm yoki undan ko'p bo'lsa bepul (0), aks holda 15,000 so'm
  const deliveryFee = orderTotal >= 100000 ? 0 : 15000;
  return deliveryFee;
}

const order1 = 85000;
const order2 = 120000;

console.log(`${order1} so'm uchun yetkazib berish: ${calculateDelivery(order1)} so'm`);
console.log(`${order2} so'm uchun yetkazib berish: ${calculateDelivery(order2)} so'm`);
```

## Tushuntirish va Mantiq:
1. Ternary operator (`shart ? rost_ifoda : yolg'on_ifoda`) JavaScriptdagi yagona 3 ta operand qabul qiluvchi operatordir.
2. `if...else` dan farqli ravishda u buyruq (statement) emas, balki ifoda (expression) hisoblanadi, ya'ni to'g'ridan-to'g'ri o'zgaruvchiga o'zlashtirilishi yoki `return` qilinishi mumkin.
3. Oddiy ikki tomonlama tanlovlar uchun eng ixcham yechimdir.

## Ishlash natijasi:
```text
85000 so'm uchun yetkazib berish: 15000 so'm
120000 so'm uchun yetkazib berish: 0 so'm
```


# 64-Topshiriq: Zanjirli ternary operator (Nested Ternary): Baholash shkalasi

## Topshiriq sharti:
Talabaning imtihon balliga qarab uning darajasini (A, B, C, D, F) qaytaruvchi zanjirli ternar ifodasini yozing va uning formatlanish qoidalarini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function getGrade(score: number): string {
  // Toza va ustun shaklida formatlangan zanjirli ternar
  return score >= 90
    ? "A (A'lo)"
    : score >= 80
    ? "B (Yaxshi)"
    : score >= 70
    ? "C (Qoniqarli)"
    : score >= 60
    ? "D (Yetarli)"
    : "F (Qoniqarsiz)";
}

[95, 82, 74, 61, 45].forEach((sc) => {
  console.log(`Ball ${sc}: ${getGrade(sc)}`);
});
```

## Tushuntirish va Mantiq:
1. Zanjirli ternar ifodalar bir nechta `if...else if...else` shartlarini ixcham shaklda ifodalash imkonini beradi.
2. Har bir shartni yangi qatordan chekinish (indentation) bilan yozish kodning o'qilishini yaxshilaydi.
3. Juda chuqur (5-6 tadan ortiq) zanjirlarda `switch` yoki lookup table ishlatish ma'qulroq.

## Ishlash natijasi:
```text
Ball 95: A (A'lo)
Ball 82: B (Yaxshi)
Ball 74: C (Qoniqarli)
Ball 61: D (Yetarli)
Ball 45: F (Qoniqarsiz)
```


# 65-Topshiriq: Qat'iy tenglik (===) va tengsizlik (!==) solishtirishlari

## Topshiriq sharti:
Har doim qat'iy tenglik operatorlaridan (`===`, `!==`) foydalanish zarurligini va ularning tip o'zgarishisiz ishlashini namoyish eting.

## Yechim (JS yoki TS kodi):
```typescript
function compareStrictness(val1: any, val2: any): void {
  // @ts-ignore
  const loose = val1 == val2;
  const strict = val1 === val2;

  console.log(`Solishtirish: ${JSON.stringify(val1)} va ${JSON.stringify(val2)}`);
  console.log(`  Noqat'iy (==) : ${loose}`);
  console.log(`  Qat'iy   (===): ${strict}`);
}

compareStrictness(0, false);
compareStrictness("42", 42);
compareStrictness(null, undefined);
```

## Tushuntirish va Mantiq:
1. `==` va `!=` taqqoslashdan oldin turli tiplarni bir-biriga aylantirishga urinadi (type coercion), bu esa kutilmagan mantiqiy xatolarni keltirib chiqaradi.
2. `===` va `!==` avvalo operandlarning turlarini tekshiradi: agar turlari har xil bo'lsa, konvertatsiya qilmasdan darhol `false` qaytaradi.
3. Zamonaviy TypeScript/JavaScript qoidalarida faqat `===` va `!==` dan foydalanish qat'iy tavsiya etiladi.

## Ishlash natijasi:
```text
Solishtirish: 0 va false
  Noqat'iy (==) : true
  Qat'iy   (===): false
Solishtirish: "42" va 42
  Noqat'iy (==) : true
  Qat'iy   (===): false
Solishtirish: null va undefined
  Noqat'iy (==) : true
  Qat'iy   (===): false
```


# 66-Topshiriq: Satrlarni leksikografik taqqoslash (Unicode bo'yicha alfavit tartibi)

## Topshiriq sharti:
Satrlarni `>`, `<`, `>=` operatorlari orqali solishtirishda Unicode kod nuqtalari va registr (katta/kichik harflar) ta'sirini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function compareStringsLexicographically(): void {
  console.log("'b' > 'a':", "b" > "a"); // true
  console.log("'olma' < 'uzum':", "olma" < "uzum"); // true

  // Katta va kichik harflar (Unicode: 'A' = 65, 'a' = 97)
  console.log("'A' > 'a':", "A" > "a"); // false, chunki 65 < 97
  console.log("'B' < 'a':", "B" < "a"); // true! Katta harflar kichiklardan 'kichik'

  // Satrli raqamlarni solishtirish
  console.log("'10' < '2':", "10" < "2"); // true! Chunki '1' belgisi '2' dan kichik!
}

compareStringsLexicographically();
```

## Tushuntirish va Mantiq:
1. JavaScriptda satrlar harfma-harf ularning UTF-16 kod qiymatlari (`charCodeAt`) bo'yicha taqqoslanadi.
2. Katta lotin harflari (A-Z) kichik lotin harflaridan (a-z) oldin keladi, shuning uchun `'Z' < 'a'` rost bo'ladi.
3. Raqamlardan iborat satrlar solishtirilganda son qiymati emas, birinchi harfi solishtiriladi (`'10' < '2' === true`). Shu sababli sonlarni solishtirishdan oldin `Number()` ga aylantirish shart.

## Ishlash natijasi:
```text
'b' > 'a': true
'olma' < 'uzum': true
'A' > 'a': false
'B' < 'a': true
'10' < '2': true
```


# 67-Topshiriq: Bitwise AND (&) va juft/toq sonni aniqlash

## Topshiriq sharti:
Bitwise AND (`&`) operatori orqali sonning toq yoki juft ekanligini eng tez usulda aniqlovchi funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
function isOddBitwise(num: number): boolean {
  // Sonning ikkilikdagi eng oxirgi biti 1 bo'lsa toq, 0 bo'lsa juft
  return (num & 1) === 1;
}

const numbersToTest = [4, 7, 18, 25, 0, -3];
numbersToTest.forEach((n) => {
  console.log(`${n} soni toqmi: ${isOddBitwise(n)}`);
});
```

## Tushuntirish va Mantiq:
1. Ikkilik sanoq sistemasida har qanday toq sonning eng quyi (oxirgi) biti `1` ga, juft sonlarniki esa `0` ga teng.
2. `num & 1` amali faqat shu oxirgi bitni tekshiradi, qolgan barcha bitlar `0` bo'lib qoladi.
3. Bu usul an'anaviy `num % 2 !== 0` qoldiq olish amaliga qaraganda protsessor darajasida tezroq ishlaydi va manfiy sonlar bilan ham aniq ishlaydi.

## Ishlash natijasi:
```text
4 soni toqmi: false
7 soni toqmi: true
18 soni toqmi: false
25 soni toqmi: true
0 soni toqmi: false
-3 soni toqmi: true
```


# 68-Topshiriq: Bitwise OR (|) va butun songa aylantirish

## Topshiriq sharti:
`| 0` operatori orqali musbat va manfiy suzuvchi nuqtali sonlarning kasr qismini tezkor olib tashlashni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function fastTruncate(val: number): number {
  return val | 0;
}

console.log("fastTruncate(4.99):", fastTruncate(4.99));
console.log("fastTruncate(4.01):", fastTruncate(4.01));
console.log("fastTruncate(-4.99):", fastTruncate(-4.99));
console.log("fastTruncate(-4.01):", fastTruncate(-4.01));
```

## Tushuntirish va Mantiq:
1. Bitwise operatorlar (`|`, `&`, `^`) operatsiyadan oldin o'z operandlarini 32-bitli butun sonlarga (int32) aylantiradi.
2. Natijada `val | 0` amali sonning kasr qismini nolga aylantirib, butun qismini qoldiradi.
3. Bu `Math.trunc()` funksiyasiga teng bo'lib, o'yinlar va grafik hisob-kitoblarda unumdorlikni oshirish uchun ishlatiladi.

## Ishlash natijasi:
```text
fastTruncate(4.99): 4
fastTruncate(4.01): 4
fastTruncate(-4.99): -4
fastTruncate(-4.01): -4
```


# 69-Topshiriq: Bitwise XOR (^) va Massivdagi yagona toq elementni topish

## Topshiriq sharti:
Massivdagi barcha elementlar juft marta (2 marta) takrorlangan, faqat bitta element 1 marta qatnashgan. Ushbu yagona elementni `O(N)` vaqt va `O(1)` xotirada XOR (`^`) yordamida toping.

## Yechim (JS yoki TS kodi):
```typescript
function findSingleNumber(nums: number[]): number {
  let unique = 0;
  for (const n of nums) {
    unique ^= n; // Bir xil sonlar bir-birini nolga aylantiradi: x ^ x = 0
  }
  return unique;
}

const data = [4, 1, 2, 1, 2, 99, 4];
const result = findSingleNumber(data);
console.log("Massivdagi yagona takrorlanmas element:", result);
```

## Tushuntirish va Mantiq:
1. XOR operatori assotsiativ va kommutativdir: tartib ahamiyatsiz.
2. `x ^ x = 0` (bir xil ikkita son bir-birini bekor qiladi).
3. `x ^ 0 = x` (har qanday sonning 0 bilan XOR amali o'sha sonni beradi).
4. Shunday qilib, barcha juft sonlar bir-birini nolga aylantiradi va faqat yagona qolgan toq son saqlanib qoladi.

## Ishlash natijasi:
```text
Massivdagi yagona takrorlanmas element: 99
```


# 70-Topshiriq: Bitwise NOT (~) va -1 indeksini tekshirish

## Topshiriq sharti:
Bitwise NOT (`~`) operatorining `-(n + 1)` formulasi asosida ishlashini va `indexOf` natijasini tekshirishdagi klassik rolini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function testBitwiseNot(): void {
  // ~n formulasi: -(n + 1)
  console.log("~0 =", ~0);   // -1
  console.log("~(-1) =", ~(-1)); // 0!
  console.log("~5 =", ~5);   // -6

  // indexOf bilan tekshirish: ~(-1) === 0 (falsy), boshqa har qanday indeks truthy bo'ladi
  const fruits = ["olma", "banan", "anor"];

  const searchItem = (item: string) => {
    const idx = fruits.indexOf(item);
    if (~idx) {
      console.log(`'${item}' topildi! Indeksi: ${idx}`);
    } else {
      console.log(`'${item}' ro'yxatda yo'q.`);
    }
  };

  searchItem("banan");
  searchItem("nok");
}

testBitwiseNot();
```

## Tushuntirish va Mantiq:
1. Bitwise NOT (`~`) barcha bitlarni teskarisiga aylantiradi (1 -> 0, 0 -> 1), bu arifmetik jihatdan `-(n + 1)` ga teng.
2. Agar `indexOf` elementni topolmasa `-1` qaytaradi. `~(-1)` esa `0` (ya'ni falsy) bo'ladi.
3. Element topilsa indeks >= 0 bo'ladi, `~indeks` manfiy son bo'lib, truthy qiymat beradi.
4. Zamonaviy kodda `includes()` ko'proq ishlatilsa-da, bu klassik usul kutubxonalar kodida tez-tez uchraydi.

## Ishlash natijasi:
```text
~0 = -1
~(-1) = 0
~5 = -6
'banan' topildi! Indeksi: 1
'nok' ro'yxatda yo'q.
```


# 71-Topshiriq: Bitwise siljitish (<<, >>, >>>) va 2 ga ko'paytirish/bo'lish

## Topshiriq sharti:
Chapga siljitish (`<<`) va o'ngga siljitish (`>>`, `>>>`) operatorlarining 2 ning darajalariga tezkor ko'paytirish va bo'lish xususiyatlarini namoyish eting.

## Yechim (JS yoki TS kodi):
```typescript
function demonstrateBitwiseShifts(): void {
  const n = 5;

  // Chapga 1 ta siljitish: n * 2^1 = 10
  console.log("5 << 1 =", n << 1);
  // Chapga 3 ta siljitish: n * 2^3 = 40
  console.log("5 << 3 =", n << 3);

  // Belgili o'ngga 1 ta siljitish: Math.floor(n / 2)
  console.log("40 >> 1 =", 40 >> 1);
  console.log("-40 >> 1 =", -40 >> 1);

  // Belgisiz o'ngga siljitish (>>>): manfiy sonni musbat katta songa aylantiradi
  console.log("-1 >>> 0 =", -1 >>> 0); // 32-bitli maksimal butun son (4294967295)
}

demonstrateBitwiseShifts();
```

## Tushuntirish va Mantiq:
1. `x << k` sonni ikkilik ko'rinishda `k` pozitsiyaga chapga suradi, bu `x * (2^k)` ga teng.
2. `x >> k` belgini (manfiy/musbatlikni) saqlagan holda o'ngga suradi, bu `Math.floor(x / (2^k))` ga teng.
3. `x >>> k` nol bilan to'ldiruvchi belgisiz o'ngga siljitish bo'lib, har qanday sonni musbat 32-bitli songa aylantiradi.

## Ishlash natijasi:
```text
5 << 1 = 10
5 << 3 = 40
40 >> 1 = 20
-40 >> 1 = -20
-1 >>> 0 = 4294967295
```


# 72-Topshiriq: Bitmask (Bayroqlar) tizimi: Foydalanuvchi huquqlarini boshqarish

## Topshiriq sharti:
Ikkilik bitmasklar yordamida foydalanuvchiga huquqlar (Read, Write, Execute, Admin) berish, huquqni tekshirish va o'chirish tizimini yarating.

## Yechim (JS yoki TS kodi):
```typescript
const PERMISSIONS = {
  READ: 1 << 0,    // 0001 (1)
  WRITE: 1 << 1,   // 0010 (2)
  EXECUTE: 1 << 2, // 0100 (4)
  ADMIN: 1 << 3    // 1000 (8)
};

function managePermissions(): void {
  // Huquqlarni birlashtirish (OR - |)
  let userRole = PERMISSIONS.READ | PERMISSIONS.WRITE;
  console.log("Boshlang'ich huquqlar kodi:", userRole);

  // Huquqni tekshirish (AND - &)
  const canRead = (userRole & PERMISSIONS.READ) !== 0;
  const canExecute = (userRole & PERMISSIONS.EXECUTE) !== 0;
  console.log("O'qiy oladimi:", canRead);
  console.log("Bajara oladimi:", canExecute);

  // Yangi huquq qo'shish
  userRole |= PERMISSIONS.EXECUTE;
  console.log("EXECUTE qo'shilgach tekshiruv:", (userRole & PERMISSIONS.EXECUTE) !== 0);

  // Huquqni bekor qilish (AND NOT - & ~)
  userRole &= ~PERMISSIONS.WRITE;
  console.log("WRITE o'chirilgach tekshiruv:", (userRole & PERMISSIONS.WRITE) !== 0);
}

managePermissions();
```

## Tushuntirish va Mantiq:
1. Bitmasklar bitta butun sonda bir nechta mantiqiy bayroqlarni (flags) ixcham saqlash imkonini beradi.
2. `|` (OR) yangi bayroq qo'shish uchun ishlatiladi.
3. `&` (AND) bayroq bor-yo'qligini tekshirish uchun ishlatiladi.
4. `& ~` (AND NOT) berilgan bayroqni o'chirish uchun ishlatiladi.
5. Bu Linux fayl tizimi huquqlari (chmod) va yuqori unumdor tizimlarning asosiy arxitekturasidir.

## Ishlash natijasi:
```text
Boshlang'ich huquqlar kodi: 3
O'qiy oladimi: true
Bajara oladimi: false
EXECUTE qo'shilgach tekshiruv: true
WRITE o'chirilgach tekshiruv: false
```


# 73-Topshiriq: switch...case operatori va qat'iy tenglik tekshiruvi

## Topshiriq sharti:
`switch...case` operatori ichida qat'iy tenglik (`===`) qoidasi amal qilishini ko'rsatuvchi dastur yozing.

## Yechim (JS yoki TS kodi):
```typescript
function testSwitchStrictness(input: any): void {
  switch (input) {
    case "10":
      console.log("Moslik topildi: Satr '10'");
      break;
    case 10:
      console.log("Moslik topildi: Raqam 10");
      break;
    default:
      console.log("Moslik topilmadi");
  }
}

console.log("Kirish raqam 10:");
testSwitchStrictness(10);

console.log("Kirish satr '10':");
testSwitchStrictness("10");
```

## Tushuntirish va Mantiq:
1. `switch (val)` operatori `case` qiymatlari bilan solishtirishda har doim qat'iy tenglikdan (`===`) foydalanadi.
2. Shuning uchun satr `'10'` bilan raqam `10` bir-biriga mos kelmaydi va o'zining mos branchiga tushadi.
3. Har bir `case` bloki oxiriga `break` qo'yilmasa, ijro keyingi case'larga o'tib ketadi (fallthrough).

## Ishlash natijasi:
```text
Kirish raqam 10:
Moslik topildi: Raqam 10
Kirish satr '10':
Moslik topildi: Satr '10'
```


# 74-Topshiriq: switch operatorida Fallthrough xususiyati va holatlarni guruhlash

## Topshiriq sharti:
`switch` blokidagi fallthrough imkoniyatidan foydalanib haftaning kunlarini ish kuni yoki dam olish kuniga ajratuvchi funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
function getDayType(dayNumber: number): string {
  let type: string;

  switch (dayNumber) {
    case 1:
    case 2:
    case 3:
    case 4:
    case 5:
      type = "Ish kuni";
      break;
    case 6:
    case 7:
      type = "Dam olish kuni";
      break;
    default:
      type = "Noto'g'ri hafta kuni";
  }

  return type;
}

[1, 3, 6, 7, 9].forEach((d) => {
  console.log(`${d}-kun: ${getDayType(d)}`);
});
```

## Tushuntirish va Mantiq:
1. Agar `case` blokida `break` yozilmasa, dastur keyingi `case` ga shart tekshirilmasdan to'g'ridan-to'g'ri o'tib ketadi. Bu xususiyat 'fallthrough' deb ataladi.
2. Fallthrough bir nechta turli qiymatlar uchun bir xil mantiqni bajarishda (guruhlashda) juda qulaydir.
3. Kutilmagan fallthrough xatolariga yo'l qo'ymaslik uchun ESLint qoidalarida har doim `break` yoki izoh talab qilinadi.

## Ishlash natijasi:
```text
1-kun: Ish kuni
3-kun: Ish kuni
6-kun: Dam olish kuni
7-kun: Dam olish kuni
9-kun: Noto'g'ri hafta kuni
```


# 75-Topshiriq: switch(true) naqshi: Murakkab oraliqlar va shartlarni tekshirish

## Topshiriq sharti:
An'anaviy qiymat tekshiruvi o'rniga `switch(true)` uslubi orqali sonli diapazonlarni tekshirish funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function categorizeTemperature(tempCelsius: number): string {
  // switch argumentiga true beriladi, case qismida esa mantiqiy ifodalar yoziladi
  switch (true) {
    case tempCelsius < 0:
      return "Qahraton sovuq";
    case tempCelsius >= 0 && tempCelsius < 15:
      return "Salqin havo";
    case tempCelsius >= 15 && tempCelsius < 30:
      return "Iliq va yoqimli";
    case tempCelsius >= 30:
      return "Jazirama issiq";
    default:
      return "Noma'lum harorat";
  }
}

[-5, 10, 22, 38].forEach((t) => {
  console.log(`${t}°C harorat: ${categorizeTemperature(t)}`);
});
```

## Tushuntirish va Mantiq:
1. `switch(true)` naqshida JavaScript birinchi `true` qaytargan `case` ifodasini qidiradi.
2. Bu uslub ko'plab `if...else if` shartlarini chiroyli va tartibli ustun ko'rinishida yozish imkonini beradi.
3. Murakkab oraliqlar (ranges) va bir nechta o'zgaruvchilarni solishtirishda qo'llaniladi.

## Ishlash natijasi:
```text
-5°C harorat: Qahraton sovuq
10°C harorat: Salqin havo
22°C harorat: Iliq va yoqimli
38°C harorat: Jazirama issiq
```


# 76-Topshiriq: Guard Clauses (Himoya shartlari) orqali chuqur if-else zanjirlarini yo'qotish

## Topshiriq sharti:
Kiritilgan chuqur (nested) `if-else` kodini Guard Clauses (erta qaytish - Early Return) texnikasi yordamida toza va o'qilishi oson holatga keltiring.

## Yechim (JS yoki TS kodi):
```typescript
interface PaymentRequest {
  userActive: boolean;
  amount: number;
  balance: number;
}

// Yomon uslub: chuqur if-else
// Yaxshi uslub: Guard clauses
function processPayment(req: PaymentRequest): string {
  if (!req.userActive) {
    return "Xato: Foydalanuvchi hisobi faol emas.";
  }

  if (req.amount <= 0) {
    return "Xato: To'lov summasi 0 dan katta bo'lishi kerak.";
  }

  if (req.balance < req.amount) {
    return "Xato: Hisobda mablag' yetarli emas.";
  }

  // Asosiy muvaffaqiyatli mantiq eng pastda erkin joylashadi
  const remaining = req.balance - req.amount;
  return `To'lov muvaffaqiyatli! Qoldiq: $${remaining}`;
}

console.log(processPayment({ userActive: false, amount: 100, balance: 500 }));
console.log(processPayment({ userActive: true, amount: -10, balance: 500 }));
console.log(processPayment({ userActive: true, amount: 600, balance: 500 }));
console.log(processPayment({ userActive: true, amount: 200, balance: 500 }));
```

## Tushuntirish va Mantiq:
1. Guard Clauses naqshi barcha xatolik va chekka holatlarni funksiya boshidayoq tekshirib, darhol `return` qiladi.
2. Bu kodning o'ng tomonga siljib ketishining ('Arrow Anti-pattern' yoki 'Pyramid of Doom') oldini oladi.
3. Asosiy biznes mantiq hech qanday `else` bloki ichiga olinmasdan, to'g'ridan-to'g'ri o'qiladi.

## Ishlash natijasi:
```text
Xato: Foydalanuvchi hisobi faol emas.
Xato: To'lov summasi 0 dan katta bo'lishi kerak.
Xato: Hisobda mablag' yetarli emas.
To'lov muvaffaqiyatli! Qoldiq: $300
```


# 77-Topshiriq: 'in' operatori: Xususiyat mavjudligini xavfsiz tekshirish

## Topshiriq sharti:
Obyektda xususiyat mavjudligini uning qiymati `undefined` bo'lgan holatda ham to'g'ri aniqlovchi `in` operatori misolini yozing.

## Yechim (JS yoki TS kodi):
```typescript
interface Car {
  make: string;
  model: string;
  year?: number;
  owner?: string | undefined;
}

const myCar: Car = {
  make: "Chevrolet",
  model: "Cobalt",
  owner: undefined // Kalit mavjud, lekin qiymati undefined
};

console.log("1. 'owner' in myCar:", "owner" in myCar); // true
console.log("2. myCar.owner !== undefined:", myCar.owner !== undefined); // false!

console.log("3. 'year' in myCar:", "year" in myCar); // false (kalit yo'q)
console.log("4. 'toString' in myCar:", "toString" in myCar); // true (prototipdan kelgan)
```

## Tushuntirish va Mantiq:
1. `key in obj` obyektdan yoki uning prototiplar zanjiridan kalitni qidiradi.
2. Agar kalit mavjud bo'lib, uning qiymati `undefined` bo'lsa ham, `in` operatori `true` qaytaradi.
3. To'g'ridan-to'g'ri `obj.key !== undefined` deb tekshirish kalit yo'qligi bilan qiymatning undefined ekanligini ajrata olmaydi.
4. Faqat obyektning o'ziga tegishli ekanligini bilish uchun `Object.hasOwn(obj, key)` ishlatiladi.

## Ishlash natijasi:
```text
1. 'owner' in myCar: true
2. myCar.owner !== undefined: false
3. 'year' in myCar: false
4. 'toString' in myCar: true
```


# 78-Topshiriq: 'instanceof' operatori: Prototip zanjirini tekshirish

## Topshiriq sharti:
`instanceof` operatori yordamida obyektning ma'lum bir sinf yoki konstruktor nusxasi ekanligini aniqlashni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
class Animal {
  constructor(public name: string) {}
}

class Dog extends Animal {
  bark() {
    return "Vov-vov";
  }
}

const rex = new Dog("Rex");

console.log("rex instanceof Dog:", rex instanceof Dog); // true
console.log("rex instanceof Animal:", rex instanceof Animal); // true (merosxo'rlik zanjirida bor)
console.log("rex instanceof Object:", rex instanceof Object); // true
console.log("rex instanceof Array:", (rex as any) instanceof Array); // false

// Maxsus xatoliklarni tekshirishda
try {
  throw new TypeError("Noto'g'ri ma'lumot turi");
} catch (err) {
  if (err instanceof TypeError) {
    console.log("Ushlangan xato aynan TypeError:", err.message);
  }
}
```

## Tushuntirish va Mantiq:
1. `instanceof` operatori o'ng tomondagi konstruktor funksiyaning `prototype` xususiyati chap tomondagi obyektning prototiplar zanjirida mavjudligini tekshiradi.
2. Merosxo'rlik zanjiridagi barcha ota sinflar uchun ham `true` qaytaradi.
3. Xatoliklarni qayta ishlashda (`catch (e) { if (e instanceof CustomError) ... }`) juda muhim vositadir.

## Ishlash natijasi:
```text
rex instanceof Dog: true
rex instanceof Animal: true
rex instanceof Object: true
rex instanceof Array: false
Ushlangan xato aynan TypeError: Noto'g'ri ma'lumot turi
```


# 79-Topshiriq: Operator Precedence (Operatorlar ustunligi) va hisoblash tartibi

## Topshiriq sharti:
Operatorlar ustunligi (arifmetik, solishtirish, mantiqiy) tufayli qavssiz yozilgan ifodaning kutilmagan natijasini va qavslar bilan to'g'rilashni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function testPrecedence(): void {
  // + operatori > dan ustun
  // 5 + 5 > 8 -> 10 > 8 -> true
  console.log("5 + 5 > 8 =", 5 + 5 > 8);

  // && operatori || dan ustun
  // true || false && false -> true || (false && false) -> true || false -> true
  const res1 = true || false && false;
  console.log("true || false && false =", res1);

  // Qavslar bilan tartibni o'zgartirish
  const res2 = (true || false) && false;
  console.log("(true || false) && false =", res2);
}

testPrecedence();
```

## Tushuntirish va Mantiq:
1. JavaScriptda har bir operator o'zining qat'iy ustuvorlik darajasiga (precedence) ega.
2. Mantiqiy `&&` operatori `||` operatoridan yuqoriroq ustunlikka ega (ko'paytirish qo'shishdan ustun bo'lgani kabi).
3. Murakkab shartlarda har doim qavslardan `()` foydalanish kutilmagan xatolarning oldini oladi va boshqa dasturchilarga mantiqni aniq ko'rsatadi.

## Ishlash natijasi:
```text
5 + 5 > 8 = true
true || false && false = true
(true || false) && false = false
```


# 80-Topshiriq: Vergul operatori (Comma Operator) va uning ketma-ket baholanishi

## Topshiriq sharti:
Vergul operatorining (`,`) chapdan o'ngga barcha ifodalarni bajarib, eng oxirgi ifoda qiymatini qaytarish xususiyatini namoyish eting.

## Yechim (JS yoki TS kodi):
```typescript
function demonstrateCommaOperator(): void {
  let x = 1;

  // Vergul operatori: (x += 1, x * 2)
  // 1-amal: x 1 ga oshadi (x=2), 2-amal: x * 2 hisoblanadi (4) va qaytariladi
  const result = (x += 1, x * 2);

  console.log("Oxirgi qaytgan natija:", result);
  console.log("x ning qiymati:", x);

  // for siklida bir nechta hisoblagichlarni yurgizish
  for (let i = 0, j = 10; i < j; i++, j--) {
    console.log(`i: ${i}, j: ${j}`);
  }
}

demonstrateCommaOperator();
```

## Tushuntirish va Mantiq:
1. Vergul operatori har bir ifodani chapdan o'ngga qarab bajaradi va eng oxirgi operand qiymatini qaytaradi.
2. Eng ko'p tarqalgan qonuniy qo'llanish joyi `for` sikllarining boshlang'ich va inkrement qismida bir nechta o'zgaruvchilarni parallel o'zgartirishdir.
3. Oddiy kodda undan me'yordan ortiq foydalanish tavsiya etilmaydi, chunki u kodni tushunishni qiyinlashtiradi.

## Ishlash natijasi:
```text
Oxirgi qaytgan natija: 4
x ning qiymati: 2
i: 0, j: 10
i: 1, j: 9
i: 2, j: 8
i: 3, j: 7
i: 4, j: 6
```


# 81-Topshiriq: 'delete' operatori: Xususiyatni o'chirish va uning massivdagi xavfi

## Topshiriq sharti:
`delete` operatori yordamida obyektdan maydonni o'chirish va nima uchun uni massiv elementlariga qo'llamaslik kerakligini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function testDeleteOperator(): void {
  // Obyektda:
  const user: Record<string, any> = { id: 1, secret: "12345", name: "Dilshod" };
  delete user.secret;
  console.log("Obyektdan secret o'chirildi:", user);

  // Massivda delete ishlatish XATOSI:
  const fruits = ["olma", "banan", "shaftoli"];
  delete fruits[1]; // banan o'chiriladi, lekin bo'shliq (empty slot) qoladi!

  console.log("delete dan keyin massiv:", fruits);
  console.log("Massiv uzunligi:", fruits.length); // Hali ham 3!
  console.log("fruits[1]:", fruits[1]); // undefined

  // To'g'ri usul: splice()
  const correctFruits = ["olma", "banan", "shaftoli"];
  correctFruits.splice(1, 1);
  console.log("splice() orqali to'g'ri o'chirilgan massiv:", correctFruits);
}

testDeleteOperator();
```

## Tushuntirish va Mantiq:
1. `delete obj.prop` obyektdan berilgan xususiyatni butunlay olib tashlaydi.
2. Massiv elementiga `delete arr[i]` qo'llanganda, element o'chiriladi, ammo massiv uzunligi (`length`) qisqarmaydi. U yerda 'bo'sh teshik' (sparse array) hosil bo'ladi.
3. Massivdan elementni xavfsiz o'chirish uchun `splice()`, `filter()` yoki `toSpliced()` ishlatilishi shart.

## Ishlash natijasi:
```text
Obyektdan secret o'chirildi: { id: 1, name: 'Dilshod' }
delete dan keyin massiv: [ 'olma', <1 empty item>, 'shaftoli' ]
Massiv uzunligi: 3
fruits[1]: undefined
splice() orqali to'g'ri o'chirilgan massiv: [ 'olma', 'shaftoli' ]
```


# 82-Topshiriq: Clamp funksiyasi: Math.min va Math.max orqali qiymatni chegaralash

## Topshiriq sharti:
Sonni berilgan minimal va maksimal oraliqda ushlab turuvchi `clamp` funksiyasini shartli operatorlar va Math metodlari orqali yozing.

## Yechim (JS yoki TS kodi):
```typescript
function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max);
}

function testClamp(): void {
  console.log("clamp(15, 0, 100):", clamp(15, 0, 100)); // Oraliqda
  console.log("clamp(-20, 0, 100):", clamp(-20, 0, 100)); // Minimumdan kichik -> 0 bo'ladi
  console.log("clamp(150, 0, 100):", clamp(150, 0, 100)); // Maksimumdan katta -> 100 bo'ladi
}

testClamp();
```

## Tushuntirish va Mantiq:
1. `clamp` funksiyasi qiymatni belgilangan chegaralar `[min, max]` ichida qat'iy cheklaydi.
2. `Math.max(value, min)` qiymatni minimumdan pastga tushmasligini kafolatlaydi.
3. `Math.min(..., max)` esa qiymatning maksimumdan oshib ketmasligini ta'minlaydi.
4. UI animatsiyalari, ovoz balandligi (0-100%) va scroll pozitsiyalarini hisoblashda keng qo'llaniladi.

## Ishlash natijasi:
```text
clamp(15, 0, 100): 15
clamp(-20, 0, 100): 0
clamp(150, 0, 100): 100
```


# 83-Topshiriq: Lookup Table (Qidiruv obyekti): Murakkab switch/if-else o'rniga

## Topshiriq sharti:
Ko'p tarmoqli `switch` o'rniga obyekt orqali holatlarni boshqaruvchi (Lookup Table) naqshini yozing.

## Yechim (JS yoki TS kodi):
```typescript
type Status = "pending" | "approved" | "rejected" | "cancelled";

function getStatusBadge(status: Status): string {
  // Lookup table: kalit - status, qiymat - natija
  const statusBadges: Record<Status, string> = {
    pending: "[KUTILMOQDA] - Sariq",
    approved: "[TASDIQLANDI] - Yashil",
    rejected: "[RAD ETILDI] - Qizil",
    cancelled: "[BEKOR QILINDI] - Kulrang"
  };

  return statusBadges[status] ?? "[NOMA'LUM]";
}

console.log(getStatusBadge("pending"));
console.log(getStatusBadge("approved"));
console.log(getStatusBadge("rejected"));
```

## Tushuntirish va Mantiq:
1. Lookup Table (lug'at) naqshi tarmoqlanishlarni ma'lumotlar tuzilmasiga (obyekt yoki Map) ko'chiradi.
2. Murakkab `switch` bloklariga nisbatan kod ancha qisqa, toza va deklarativ ko'rinishga ega bo'ladi.
3. Qidiruv tezligi `O(1)` bo'lib, yangi holatlarni qo'shish obyektga yangi kalit-qiymat kiritish kabi oson kechadi.

## Ishlash natijasi:
```text
[KUTILMOQDA] - Sariq
[TASDIQLANDI] - Yashil
[RAD ETILDI] - Qizil
```


# 84-Topshiriq: Early Return pattern bilan biznes mantiqni toza tashkil etish

## Topshiriq sharti:
Chegirma hisoblash tizimida Early Return patterni orqali tekshiruvlarni tartibli amalga oshiring.

## Yechim (JS yoki TS kodi):
```typescript
function calculateClientDiscount(yearsActive: number, totalSpent: number, isVip: boolean): number {
  if (isVip) {
    return 25; // VIP mijozlarga darhol 25% chegirma
  }

  if (yearsActive >= 5 && totalSpent > 10000) {
    return 20;
  }

  if (yearsActive >= 3 || totalSpent > 5000) {
    return 10;
  }

  if (totalSpent > 1000) {
    return 5;
  }

  return 0; // Standart mijoz
}

console.log("VIP mijoz chegirmasi:", calculateClientDiscount(1, 500, true), "%");
console.log("5 yillik faol mijoz chegirmasi:", calculateClientDiscount(5, 12000, false), "%");
console.log("Yangi mijoz chegirmasi:", calculateClientDiscount(1, 200, false), "%");
```

## Tushuntirish va Mantiq:
1. Early return kodning o'qilishini chiziqli qiladi: shart bajarildimi, darhol qiymat qaytadi va funksiya to'xtaydi.
2. Dasturchi keyingi satrlarni o'qiyotganda oldingi shartlar haqida bosh qotirishi shart bo'lmaydi.
3. Keraksiz `else` bloklari butunlay yo'qoladi.

## Ishlash natijasi:
```text
VIP mijoz chegirmasi: 25 %
5 yillik faol mijoz chegirmasi: 20 %
Yangi mijoz chegirmasi: 0 %
```


# 85-Topshiriq: Xatolik tekshiruvida Ternary vs if-else: Yon ta'sirlarni boshqarish

## Topshiriq sharti:
Qiymat qaytarishda ternar operatordan, yon ta'sirlar (side-effects, log chiqarish, fayl yozish) bo'lganda esa if-else dan foydalanish qoidasini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function handleAction(isValid: boolean): void {
  // 1. Toza qiymat olish uchun TERNARY juda mos:
  const statusText = isValid ? "Muvaffaqiyatli" : "Muvaffaqiyatsiz";
  console.log("Holat:", statusText);

  // 2. Yon ta'sirlar (bir nechta amallar) bo'lganda IF-ELSE ishlatiladi:
  if (isValid) {
    console.log("[Log]: Tranzaksiya tasdiqlandi.");
    console.log("[Audit]: Tizim yozuvi yangilandi.");
  } else {
    console.warn("[Ogohlantirish]: Kirish rad etildi.");
  }
}

handleAction(true);
handleAction(false);
```

## Tushuntirish va Mantiq:
1. Ternary operator faqat natijaviy qiymat kerak bo'lganda ishlatilishi kerak.
2. Ternar ichiga konsolga yozish yoki holatni o'zgartiruvchi ko'p qatorli amallarni joylashtirish anti-pattern hisoblanadi.
3. Yon ta'sirlar mavjud bo'lganda an'anaviy `if...else` bloklaridan foydalanish eng to'g'ri amaliyotdir.

## Ishlash natijasi:
```text
Holat: Muvaffaqiyatli
[Log]: Tranzaksiya tasdiqlandi.
[Audit]: Tizim yozuvi yangilandi.
Holat: Muvaffaqiyatsiz
[Ogohlantirish]: Kirish rad etildi.
```


# 86-Topshiriq: Array.prototype.includes orqali ko'p variantli shartlarni soddalashtirish

## Topshiriq sharti:
`if (status === 'a' || status === 'b' || status === 'c')` kabi uzun shartlarni `includes()` orqali tozalang.

## Yechim (JS yoki TS kodi):
```typescript
function isActionAllowed(action: string): boolean {
  const allowedActions = ["read", "write", "upload", "download"];

  // Uzun || o'rniga ixcham includes
  return allowedActions.includes(action.toLowerCase());
}

console.log("upload ruxsat etilganmi:", isActionAllowed("upload"));
console.log("delete ruxsat etilganmi:", isActionAllowed("delete"));
```

## Tushuntirish va Mantiq:
1. `[val1, val2, ...].includes(target)` usuli bir nechta `||` tekshiruvlarini bitta massivga jamlaydi.
2. Kod ancha toza ko'rinadi va yangi variantlarni qo'shish shunchaki massivga yangi satr kiritish orqali bajariladi.
3. Katta ro'yxatlar uchun `Set.prototype.has` ishlatilsa `O(1)` qidiruv tezligiga erishiladi.

## Ishlash natijasi:
```text
upload ruxsat etilganmi: true
delete ruxsat etilganmi: false
```


# 87-Topshiriq: Shartli obyekt xususiyatlarini spread orqali qo'shish

## Topshiriq sharti:
Mantiqiy `&&` va spread (`...`) operatori yordamida shart bajarilgandagina obyektdagi xususiyatni generatsiya qilishni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function buildUserPayload(name: string, isAdmin: boolean) {
  return {
    name,
    role: "user",
    // Agar isAdmin rost bo'lsa, permissions xususiyati obyektga qo'shiladi
    ...(isAdmin && { permissions: ["all"], sudo: true })
  };
}

console.log("Oddiy foydalanuvchi:", buildUserPayload("Bobur", false));
console.log("Admin foydalanuvchi:", buildUserPayload("Jamshid", true));
```

## Tushuntirish va Mantiq:
1. `...(condition && { prop: val })` usuli shartli obyekt tuzishning mashhur naqshidir.
2. Agar `condition` rost bo'lsa, `{ prop: val }` obyekti tarqatiladi (spread).
3. Agar `condition` yolg'on bo'lsa, `(false)` olinadi. Obyekt ichida `...false` hech qanday xususiyat qo'shmaydi va e'tiborga olinmaydi.

## Ishlash natijasi:
```text
Oddiy foydalanuvchi: { name: 'Bobur', role: 'user' }
Admin foydalanuvchi: { name: 'Jamshid', role: 'user', permissions: [ 'all' ], sudo: true }
```


# 88-Topshiriq: De Morgan qonunlari: Mantiqiy inkorlarni soddalashtirish

## Topshiriq sharti:
De Morgan qoidalarini (`!(A && B) === !A || !B` va `!(A || B) === !A && !B`) amaliy JavaScript shartida isbotlang.

## Yechim (JS yoki TS kodi):
```typescript
function verifyDeMorgan(a: boolean, b: boolean): void {
  // 1-qoida: !(A && B) === !A || !B
  const left1 = !(a && b);
  const right1 = !a || !b;

  // 2-qoida: !(A || B) === !A && !B
  const left2 = !(a || b);
  const right2 = !a && !b;

  console.log(`a = ${a}, b = ${b}:`);
  console.log(`  !(A && B) === !A || !B : ${left1 === right1}`);
  console.log(`  !(A || B) === !A && !B : ${left2 === right2}`);
}

verifyDeMorgan(true, false);
verifyDeMorgan(true, true);
verifyDeMorgan(false, false);
```

## Tushuntirish va Mantiq:
1. De Morgan qonunlari murakkab inkor qilingan shartlarni soddalashtirish va ularni o'qilishi oson ko'rinishga keltirish uchun asosdir.
2. Ko'pincha `if (!(isLogged && hasAccess))` ifodasi o'rniga `if (!isLogged || !hasAccess)` deb yozish inson ongiga ancha tez yetib boradi.

## Ishlash natijasi:
```text
a = true, b = false:
  !(A && B) === !A || !B : true
  !(A || B) === !A && !B : true
a = true, b = true:
  !(A && B) === !A || !B : true
  !(A || B) === !A && !B : true
a = false, b = false:
  !(A && B) === !A || !B : true
  !(A || B) === !A && !B : true
```


# 89-Topshiriq: Object.is vs ===: Chekka matematik holatlarni tekshirish

## Topshiriq sharti:
`Object.is()` yordamida `NaN` va `-0` bilan bog'liq hisob-kitoblar to'g'ri tekshirilishini ko'rsatuvchi moliyaviy nazorat funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function validateTransactionAmount(amount: number): boolean {
  // Agar miqdor NaN bo'lsa
  if (Object.is(amount, NaN)) {
    console.log("Xato: Miqdor raqam emas (NaN)");
    return false;
  }

  // -0 holatini tekshirish
  if (Object.is(amount, -0)) {
    console.log("Ogohlantirish: -0 kiritildi, 0 ga aylantiriladi");
  }

  return true;
}

validateTransactionAmount(NaN);
validateTransactionAmount(-0);
validateTransactionAmount(1500);
```

## Tushuntirish va Mantiq:
1. `===` operatori `NaN === NaN` uchun `false`, `-0 === +0` uchun `true` beradi.
2. `Object.is()` esa qiymatlarning fizik aynanligini (identity) xatosiz tekshiradi.
3. Keltirilgan misolda bu tekshiruvlar orqali tizimga yaroqsiz ma'lumotlar kirmasligi ta'minlanadi.

## Ishlash natijasi:
```text
Xato: Miqdor raqam emas (NaN)
Ogohlantirish: -0 kiritildi, 0 ga aylantiriladi
```


# 90-Topshiriq: Havola orqali taqqoslash: Obyekt va massivlarning tenglik sharti

## Topshiriq sharti:
Bir xil tarkibga ega ikki turli obyekt yoki massiv nima uchun `===` orqali teng bo'lmasligini va ularni chuqur taqqoslash usulini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function testReferenceEquality(): void {
  const arr1 = [1, 2, 3];
  const arr2 = [1, 2, 3];
  const arr3 = arr1;

  console.log("arr1 === arr2:", arr1 === arr2); // false (har xil xotira manzillari)
  console.log("arr1 === arr3:", arr1 === arr3); // true (bitta xotira manzili)

  // Oddiy obyektlarda
  const obj1 = { id: 10 };
  const obj2 = { id: 10 };
  console.log("obj1 === obj2:", obj1 === obj2); // false

  // Tarkibini taqqoslash (JSON orqali oddiy holatda)
  console.log("JSON tengligi:", JSON.stringify(obj1) === JSON.stringify(obj2));
}

testReferenceEquality();
```

## Tushuntirish va Mantiq:
1. JavaScriptda obyektlar va massivlar 'havola bo'yicha' (by reference) taqqoslanadi.
2. Ikki obyektning ichki qiymatlari 100% bir xil bo'lsa ham, ular xotirada alohida katakchalarda joylashgan bo'lsa `===` har doim `false` qaytaradi.
3. Faqat ikkala o'zgaruvchi xotiradagi ayni bir manzilga ishora qilsagina `true` bo'ladi.

## Ishlash natijasi:
```text
arr1 === arr2: false
arr1 === arr3: true
obj1 === obj2: false
JSON tengligi: true
```


# 91-Topshiriq: RegExp.prototype.test bilan shartli tekshiruv

## Topshiriq sharti:
Muntazam ifodaning `test()` metodi orqali O'zbekiston telefon raqamlari formatini (+998...) tekshiruvchi funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
function isValidUzbekPhone(phone: string): boolean {
  // +998 followed by 2 digits operator code and 7 digits number
  const regex = /^\+998(90|91|93|94|95|97|98|99|88|33)\d{7}$/;
  return regex.test(phone.trim());
}

const p1 = "+998901234567";
const p2 = "+99890123456"; // Kam raqam
const p3 = "+123456789012";

console.log(`${p1} to'g'rimi:`, isValidUzbekPhone(p1));
console.log(`${p2} to'g'rimi:`, isValidUzbekPhone(p2));
console.log(`${p3} to'g'rimi:`, isValidUzbekPhone(p3));
```

## Tushuntirish va Mantiq:
1. `regex.test(str)` metodi satr belgilangan naqshga mos kelsa `true`, aks holda `false` qaytaradi.
2. Bu shartli ifodalarda `str.match()` ga qaraganda ancha tez va xotirani kamroq sarflaydi, chunki u mosliklar massivini tuzmaydi.
3. Formalar va foydalanuvchi kiritmalarini validatsiya qilishda standart hisoblanadi.

## Ishlash natijasi:
```text
+998901234567 to'g'rimi: true
+99890123456 to'g'rimi: false
+123456789012 to'g'rimi: false
```


# 92-Topshiriq: Dinamik kalitlar orqali xususiyatlarga kirish va shartli filtrlash

## Topshiriq sharti:
Hisoblangan kalitlar (`obj[key]`) yordamida obyektni dinamik filtrlash funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function filterByProperty<T extends Record<string, any>>(list: T[], key: keyof T, expectedValue: any): T[] {
  return list.filter((item) => item[key] === expectedValue);
}

const users = [
  { id: 1, name: "Ali", role: "admin" },
  { id: 2, name: "Vali", role: "user" },
  { id: 3, name: "Gani", role: "admin" }
];

const admins = filterByProperty(users, "role", "admin");
console.log("Faqat adminlar:", admins.map((u) => u.name));
```

## Tushuntirish va Mantiq:
1. JavaScriptda xususiyat nomi oldindan ma'lum bo'lmaganda yoki o'zgaruvchida saqlanganda to'rtburchak qavslar `obj[prop]` orqali murojaat qilinadi.
2. TypeScriptning `keyof T` cheklovi kiritilgan kalitning haqiqatda obyektdagi mavjud xususiyat ekanligini kafolatlaydi.

## Ishlash natijasi:
```text
Faqat adminlar: [ 'Ali', 'Gani' ]
```


# 93-Topshiriq: isNil utilitasi: null va undefined qiymatlarini aniqlash

## Topshiriq sharti:
Qiymatning `null` yoki `undefined` ekanligini bitta qatorda noqat'iy tenglik yordamida aniqlaydigan utilita yozing.

## Yechim (JS yoki TS kodi):
```typescript
function isNil(value: any): value is null | undefined {
  // null == undefined true qaytaradi, boshqa hech narsa null ga teng emas
  return value == null;
}

console.log("isNil(null):", isNil(null));
console.log("isNil(undefined):", isNil(undefined));
console.log("isNil(0):", isNil(0));
console.log("isNil(''):", isNil(""));
console.log("isNil(false):", isNil(false));
```

## Tushuntirish va Mantiq:
1. Bu `==` operatorining kamdan-kam qonuniy va foydali qo'llanilish holatlaridan biridir.
2. `val == null` ifodasi `val === null || val === undefined` ifodasining to'liq ekvivalentidir.
3. `0`, `""` va `false` kabi falsy qiymatlar uchun esa `false` qaytaradi, bu aynan kerakli natijadir.

## Ishlash natijasi:
```text
isNil(null): true
isNil(undefined): true
isNil(0): false
isNil(''): false
isNil(false): false
```


# 94-Topshiriq: Array.prototype.filter(Boolean) orqali Falsy qiymatlarni tozalash

## Topshiriq sharti:
Massivdan barcha falsy elementlarni (`0`, `""`, `null`, `undefined`, `NaN`, `false`) tozalash usulini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function compactArray<T>(arr: (T | null | undefined | false | "" | 0)[]): T[] {
  // Boolean konstruktorini callback sifatida uzatish
  return arr.filter(Boolean) as T[];
}

const rawList = ["Toshkent", "", null, "Samarqand", undefined, 0, "Buxoro", false];
const cleanList = compactArray(rawList);

console.log("Tozalangan ro'yxat:", cleanList);
```

## Tushuntirish va Mantiq:
1. `filter(Boolean)` yozilganda, massivning har bir elementi `Boolean(item)` funksiyasiga uzatiladi.
2. Faqat Truthy bo'lgan elementlar yangi massivga o'tadi, barcha Falsy qiymatlar elanib qoladi.
3. Bu usul qisqa, tushunarli va juda samarali hisoblanadi.

## Ishlash natijasi:
```text
Tozalangan ro'yxat: [ 'Toshkent', 'Samarqand', 'Buxoro' ]
```


# 95-Topshiriq: Bitwise Truncation (~~x): Qo'shaloq inkor orqali butun son olish

## Topshiriq sharti:
`~~` (qo'shaloq bitwise NOT) operatori orqali musbat va manfiy suzuvchi nuqtali sonlarni butun songa aylantirishni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function doubleTildeTruncate(val: number): number {
  return ~~val;
}

console.log("~~9.85 =", doubleTildeTruncate(9.85));
console.log("~~(-9.85) =", doubleTildeTruncate(-9.85));
console.log("~~0.001 =", doubleTildeTruncate(0.001));
```

## Tushuntirish va Mantiq:
1. Birinchi `~` sonni 32-bitli butun songa o'girib bitlarini teskarisiga aylantiradi (`-(x + 1)`).
2. Ikkinchi `~` yana teskarisiga aylantiradi, natijada sonning belgisi va butun qismi saqlanadi, kasr qismi esa yo'qoladi.
3. Bu `Math.trunc(x)` ning tezkor alternatividir.

## Ishlash natijasi:
```text
~~9.85 = 9
~~(-9.85) = -9
~~0.001 = 0
```


# 96-Topshiriq: Shartli funksiya chaqiruvi (Conditional Function Invocation)

## Topshiriq sharti:
Shartga qarab mos funksiyani tanlash va uni darhol chaqirish naqshini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function exportData(format: "json" | "csv", data: any[]): string {
  const jsonExporter = (d: any[]) => JSON.stringify(d);
  const csvExporter = (d: any[]) => d.map((row) => Object.values(row).join(",")).join("\n");

  // Shartga qarab funksiyani tanlash va chaqirish
  const exporter = format === "json" ? jsonExporter : csvExporter;
  return exporter(data);
}

const sampleData = [{ name: "Anvar", age: 25 }, { name: "Zuhra", age: 22 }];

console.log("JSON eksport:\n" + exportData("json", sampleData));
console.log("\nCSV eksport:\n" + exportData("csv", sampleData));
```

## Tushuntirish va Mantiq:
1. JavaScriptda funksiyalar birinchi darajali fuqarolardir (First-Class Citizens): ularni o'zgaruvchilarga saqlash, ifodalarda tanlash va uzatish mumkin.
2. Shart orqali funksiyaning o'zini tanlab, so'ng argument bilan chaqirish ortiqcha if-else takrorlanishlaridan xalos etadi.

## Ishlash natijasi:
```text
JSON eksport:
[{"name":"Anvar","age":25},{"name":"Zuhra","age":22}]

CSV eksport:
Anvar,25
Zuhra,22
```


# 97-Topshiriq: Multiple Conditions: Har xil turdagi tekshiruvlarni to'g'ri birlashtirish

## Topshiriq sharti:
Foydalanuvchining yoshi, elektron pochtasi va to'lov holatini tekshiruvchi ko'p parametrli xavfsiz ifodani yozing.

## Yechim (JS yoki TS kodi):
```typescript
interface UserRegistration {
  email: string;
  age: number;
  hasPaid: boolean;
}

function canAccessPremiumContent(user: UserRegistration): boolean {
  const isAdult = user.age >= 18;
  const isEmailValid = user.email.includes("@") && user.email.endsWith(".uz");
  const isSubscribed = user.hasPaid === true;

  return isAdult && isEmailValid && isSubscribed;
}

const u1: UserRegistration = { email: "nodir@mail.uz", age: 20, hasPaid: true };
const u2: UserRegistration = { email: "kamol@gmail.com", age: 17, hasPaid: true };

console.log("u1 kirish huquqi:", canAccessPremiumContent(u1));
console.log("u2 kirish huquqi:", canAccessPremiumContent(u2));
```

## Tushuntirish va Mantiq:
1. Har bir mantiqiy qismni alohida nomlangan o'zgaruvchilarga (`isAdult`, `isEmailValid`) ajratish kodning tushunarliligini (readability) bir necha barobar oshiradi.
2. Bitta uzun va tushunarsiz `if (...)` satridan ko'ra, mantiqiy bo'laklarga ajratilgan ifodalar oson testlanadi va xatolar tez topiladi.

## Ishlash natijasi:
```text
u1 kirish huquqi: true
u2 kirish huquqi: false
```


# 98-Topshiriq: Number.isSafeInteger orqali hisoblash chegaralarini tekshirish

## Topshiriq sharti:
Katta sonlar bilan hisoblash operatsiyalarida aniqlik yo'qolmasligini kafolatlovchi shartli tekshiruv yozing.

## Yechim (JS yoki TS kodi):
```typescript
function safeMultiply(a: number, b: number): number | bigint {
  const product = a * b;

  if (Number.isSafeInteger(product)) {
    return product;
  } else {
    console.log("Ogohlantirish: Xavfsiz chegaradan oshdi! BigInt ga o'tilmoqda.");
    return BigInt(a) * BigInt(b);
  }
}

console.log("Oddiy ko'paytirish:", safeMultiply(1000, 2000));
console.log("Katta ko'paytirish:", safeMultiply(900719925, 20000000).toString());
```

## Tushuntirish va Mantiq:
1. `Number.isSafeInteger(n)` berilgan sonning `-(2^53 - 1)` va `2^53 - 1` oralig'idagi aniq butun son ekanligini tekshiradi.
2. Agar hisoblash natijasi bu chegaradan chiqib ketsa, an'anaviy `number` tipi aniqlikni yo'qotadi.
3. Shartli ravishda `BigInt` ga o'tish orqali hisoblash xatolarining oldi olinadi.

## Ishlash natijasi:
```text
Oddiy ko'paytirish: 2000000
Ogohlantirish: Xavfsiz chegaradan oshdi! BigInt ga o'tilmoqda.
Katta ko'paytirish: 18014398500000000
```


# 99-Topshiriq: Ternary operator orqali reaktiv holatni xavfsiz boshqarish

## Topshiriq sharti:
Foydalanuvchi hisobining holatiga qarab unga ruxsat etilgan funksiyalar ro'yxatini reaktiv qaytaruvchi ifodani yozing.

## Yechim (JS yoki TS kodi):
```typescript
type AccountTier = "free" | "pro" | "enterprise";

function getAvailableFeatures(tier: AccountTier): string[] {
  return tier === "enterprise"
    ? ["Cheksiz xotira", "24/7 Qo'llab-quvvatlash", "Maxsus API", "Shaxsiy menejer"]
    : tier === "pro"
    ? ["100GB xotira", "Tezkor yordam", "Standart API"]
    : ["5GB xotira", "Hamjamiyat yordami"];
}

console.log("Free imkoniyatlari:", getAvailableFeatures("free"));
console.log("Pro imkoniyatlari:", getAvailableFeatures("pro"));
```

## Tushuntirish va Mantiq:
1. Reaktiv UI arxitekturalarida (React, Vue) komponentlarning holati va xususiyatlari ko'pincha aynan shunday sof deklarativ funksiyalar orqali aniqlanadi.
2. Zanjirli ternar ifoda bu yerda har qanday tashqi o'zgaruvchilarsiz to'g'ridan-to'g'ri massivni qaytaradi.

## Ishlash natijasi:
```text
Free imkoniyatlari: [ '5GB xotira', 'Hamjamiyat yordami' ]
Pro imkoniyatlari: [ '100GB xotira', 'Tezkor yordam', 'Standart API' ]
```


# 100-Topshiriq: Kengaytirilgan autentifikatsiya va avtorizatsiya filtri: Barcha operatorlar integratsiyasi

## Topshiriq sharti:
Ushbu bo'limda o'rganilgan barcha asosiy operatorlarni (Optional Chaining `?.`, Nullish Coalescing `??`, Logical AND `&&`, Guard Clauses, Ternary, Qat'iy tenglik `===`) o'zida birlashtirgan to'liq xavfsizlik nazorati funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
interface UserSession {
  token?: string | null;
  account?: {
    isBanned?: boolean;
    role?: "user" | "moderator" | "admin";
    permissions?: number; // Bitmask
  };
}

const ADMIN_BIT = 1 << 3;

function authorizeRequest(session: UserSession | null, requiredRole?: string): { allowed: boolean; reason: string } {
  // 1. Guard clause: Sessiya mavjud emas yoki token yo'q
  if (!session?.token) {
    return { allowed: false, reason: "Autentifikatsiyadan o'tilmagan (token yo'q)." };
  }

  // 2. Bloklanganlikni tekshirish
  const isBanned = session.account?.isBanned ?? false;
  if (isBanned) {
    return { allowed: false, reason: "Hisob bloklangan." };
  }

  // 3. Rolni tekshirish
  const userRole = session.account?.role ?? "user";
  const userBits = session.account?.permissions ?? 0;
  const isSuperAdmin = (userBits & ADMIN_BIT) !== 0;

  const hasRole = requiredRole ? userRole === requiredRole || isSuperAdmin : true;

  return {
    allowed: hasRole,
    reason: hasRole ? "Muvaffaqiyatli ruxsat berildi." : `Ruxsat yetarli emas (${requiredRole} talab qilinadi).`
  };
}

const validAdmin: UserSession = {
  token: "valid_jwt_99",
  account: { isBanned: false, role: "admin", permissions: 8 }
};

const guestUser: UserSession = {
  token: null
};

console.log("Admin tekshiruvi:", authorizeRequest(validAdmin, "admin"));
console.log("Mehmon tekshiruvi:", authorizeRequest(guestUser));
```

## Tushuntirish va Mantiq:
1. Ushbu vazifa zamonaviy veb-arxitekturaning backend va API Gateway middleware qatlamida qo'llaniladigan avtorizatsiya mantiqini ifodalaydi.
2. `?.` xavfsiz chuqur o'qishni ta'minlaydi, `??` kutilmagan `null` qiymatlarni default qiymatlar bilan to'ldiradi.
3. Bitmask (`&`) va mantiqiy operatorlar kombinatsiyasi yuqori tezlik va xavfsizlikni kafolatlaydi.

## Ishlash natijasi:
```text
Admin tekshiruvi: { allowed: true, reason: 'Muvaffaqiyatli ruxsat berildi.' }
Mehmon tekshiruvi: { allowed: false, reason: 'Autentifikatsiyadan o\'tilmagan (token yo\'q).' }
```

