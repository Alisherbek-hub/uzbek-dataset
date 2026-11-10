# 201-Topshiriq: Object Literal va Shorthand Property Notation

## Topshiriq sharti:
O'zgaruvchilar nomidan foydalanib obyekt yaratishda qisqartirilgan xususiyatlar (shorthand properties) sintaksisini qo'llang.

## Yechim (JS yoki TS kodi):
```typescript
function buildUserProfile(name: string, age: number, role: string) {
  const createdAt = new Date().toISOString().split("T")[0];

  // Eski: { name: name, age: age, role: role, createdAt: createdAt }
  // Zamonaviy Shorthand notation:
  return {
    name,
    age,
    role,
    createdAt
  };
}

const user = buildUserProfile("Rustam", 28, "Dasturchi");
console.log("Foydalanuvchi obyekti:", user);
```

## Tushuntirish va Mantiq:
1. Agar obyekt kalitining nomi o'zgaruvchi nomi bilan bir xil bo'lsa, uni ikki marta takrorlash (`name: name`) shart emas.
2. `name, age, role` deb yozish ES6 shorthand xususiyati bo'lib, kodni ancha toza va ixcham qiladi.
3. Funksiyadan obyekt qaytarishda yoki API ga so'rov jo'natishda eng ko'p qo'llaniladi.

## Ishlash natijasi:
```text
Foydalanuvchi obyekti: { name: 'Rustam', age: 28, role: 'Dasturchi', createdAt: '2026-11-08' }
```


# 202-Topshiriq: Computed Property Names: Dinamik hisoblangan kalitlar

## Topshiriq sharti:
Obyekt e'lon qilinayotgan paytda to'rtburchak qavslar `[expression]` yordamida dinamik kalit nomlarini hosil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function createPrefixConfig(prefix: string, keyName: string, value: any) {
  const timestamp = Date.now();

  return {
    // Dinamik kalit nomi
    [`${prefix}_${keyName}`]: value,
    [`meta_${timestamp}`]: "Avtomatik generatsiya qilindi"
  };
}

const conf = createPrefixConfig("app", "environment", "production");
console.log("Yaratilgan dinamik konfiguratsiya:");
console.log(conf);
```

## Tushuntirish va Mantiq:
1. Computed Property Names (hisoblangan kalitlar) obyekt literalining ichida `[ifoda]` ko'rinishida yoziladi.
2. Qavs ichidagi ifoda runtime da baholanadi va uning natijasi obyekt kalitiga aylanadi.
3. Redux reducerlarida action tiplari bo'yicha dinamik state yangilashda juda qulay.

## Ishlash natijasi:
```text
Yaratilgan dinamik konfiguratsiya:
{
  app_environment: 'production',
  meta_1794119400000: 'Avtomatik generatsiya qilindi'
}
```


# 203-Topshiriq: Obyekt xususiyatlariga kirish: Nuqta (.) vs Qavs ([])

## Topshiriq sharti:
Nuqta va to'rtburchak qavslar orqali obyekt xususiyatlariga kirish farqlarini (bo'sh joyli kalitlar, o'zgaruvchilar orqali kirish) ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function testPropertyAccess(): void {
  const book: Record<string, any> = {
    title: "O'tkan kunlar",
    author: "Abdulla Qodiriy",
    "chop etilgan yili": 1925,
    "1st_edition": true
  };

  // 1. Nuqta orqali (faqat qonuniy identifikatorlar uchun)
  console.log("Sarlavha:", book.title);

  // 2. Qavs orqali (bo'sh joy, maxsus belgilar yoki raqam bilan boshlangan kalitlar)
  console.log("Yili:", book["chop etilgan yili"]);
  console.log("1-nashr:", book["1st_edition"]);

  // 3. O'zgaruvchi orqali kirish
  const fieldToRead = "author";
  console.log("O'zgaruvchi orqali muallif:", book[fieldToRead]);
}

testPropertyAccess();
```

## Tushuntirish va Mantiq:
1. Nuqta (`obj.property`) oddiy, raqam bilan boshlanmagan va probelsiz kalitlar uchun qulaydir.
2. Qavs (`obj['chop etilgan yili']`) probelli, tireli yoki maxsus belgili har qanday kalitni o'qish imkonini beradi.
3. Agar kalit nomi o'zgaruvchida saqlansa, faqat qavs `obj[varName]` orqali murojaat qilinadi.

## Ishlash natijasi:
```text
Sarlavha: O'tkan kunlar
Yili: 1925
1-nashr: true
O'zgaruvchi orqali muallif: Abdulla Qodiriy
```


# 204-Topshiriq: Object.keys(), Object.values() va Object.entries()

## Topshiriq sharti:
Obyektning kalitlari, qiymatlari va [kalit, qiymat] juftliklarini massiv shaklida oluvchi metodlarni qo'llang.

## Yechim (JS yoki TS kodi):
```typescript
function inspectObjectProperties(): void {
  const exchangeRates = {
    USD: 12800,
    EUR: 13900,
    RUB: 135
  };

  console.log("1. Kalitlar (Object.keys):", Object.keys(exchangeRates));
  console.log("2. Qiymatlar (Object.values):", Object.values(exchangeRates));

  console.log("\n3. Juftliklar (Object.entries):");
  for (const [currency, rate] of Object.entries(exchangeRates)) {
    console.log(`- 1 ${currency} = ${rate} so'm`);
  }
}

inspectObjectProperties();
```

## Tushuntirish va Mantiq:
1. `Object.keys(obj)` faqat obyektning o'ziga tegishli sanaladigan kalitlari massivini qaytaradi.
2. `Object.values(obj)` barcha xususiyatlarning qiymatlari massivini qaytaradi.
3. `Object.entries(obj)` esa har bir xususiyat uchun `[key, value]` ko'rinishidagi massivlar massivini beradi, bu `for...of` bilan birgalikda aylanib chiqish uchun eng qulay usuldir.

## Ishlash natijasi:
```text
1. Kalitlar (Object.keys): [ 'USD', 'EUR', 'RUB' ]
2. Qiymatlar (Object.values): [ 12800, 13900, 135 ]

3. Juftliklar (Object.entries):
- 1 USD = 12800 so'm
- 1 EUR = 13900 so'm
- 1 RUB = 135 so'm
```


# 205-Topshiriq: Object.fromEntries(): Massiv yoki Map dan obyekt yasash

## Topshiriq sharti:
Obyekt qiymatlarini 2 barobar oshirib, yana yangi obyektga aylantirish uchun `Object.entries` va `Object.fromEntries` ni birga qo'llang.

## Yechim (JS yoki TS kodi):
```typescript
function doublePrices(prices: Record<string, number>): Record<string, number> {
  // 1. Obyektdan juftliklar massivi olamiz
  const entries = Object.entries(prices);

  // 2. Massiv ustida amallar bajaramiz
  const transformed = entries.map(([item, price]) => [item, price * 2]);

  // 3. Qaytadan obyektga o'giramiz
  return Object.fromEntries(transformed);
}

const productPrices = { non: 3000, sut: 8000, gobi: 60000 };
const doubled = doublePrices(productPrices);

console.log("Asl narxlar:", productPrices);
console.log("Ikki barobar oshirilgan:", doubled);
```

## Tushuntirish va Mantiq:
1. `Object.fromEntries(entries)` - bu `Object.entries()` ning teskarisi bo'lib, `[key, value]` ko'rinishidagi massiv yoki `Map` dan obyekt hosil qiladi.
2. Bu obyektlarni xuddi massivlar kabi `map()`, `filter()` orqali transformatsiya qilishning eng nafis va standart usulidir.

## Ishlash natijasi:
```text
Asl narxlar: { non: 3000, sut: 8000, gobi: 60000 }
Ikki barobar oshirilgan: { non: 6000, sut: 16000, gobi: 120000 }
```


# 206-Topshiriq: Massiv destrukturizatsiyasi va elementlarni tashlab ketish

## Topshiriq sharti:
Massivdan birinchi, ikkinchi elementlarni olish, keraksizlarini tashlab ketish (ignoring elements) va rest operatorini qo'llashni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function testArrayDestructuring(): void {
  const scores = [100, 95, 88, 72, 60, 45];

  // 1-o'rin, 2-o'rin, 3-o'rinni tashlab ketamiz (bo'sh vergul), qolganlari rest massiviga
  const [first, second, , fourth, ...others] = scores;

  console.log("1-o'rin (Oltin):", first);
  console.log("2-o'rin (Kumush):", second);
  console.log("4-o'rin:", fourth);
  console.log("Qolgan ishtirokchilar:", others);
}

testArrayDestructuring();
```

## Tushuntirish va Mantiq:
1. Massiv destrukturizatsiyasida o'zgaruvchilar to'rtburchak qavs `[a, b]` ichida yoziladi va elementlar ularning indekslari (tartibi) bo'yicha taqsimlanadi.
2. Keraksiz elementlarni bo'sh vergul `, ,` orqali tashlab ketish mumkin.
3. `...others` rest sintaksisi qolgan barcha elementlarni yangi massivga yig'adi.

## Ishlash natijasi:
```text
1-o'rin (Oltin): 100
2-o'rin (Kumush): 95
4-o'rin: 72
Qolgan ishtirokchilar: [ 60, 45 ]
```


# 207-Topshiriq: Obyekt destrukturizatsiyasi va O'zgaruvchilarni qayta nomlash (Aliasing)

## Topshiriq sharti:
Obyektdan ma'lumotlarni chiqarib olishda mavjud kalit nomini yangi nom bilan o'zlashtirishni (`{ key: alias }`) ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
interface ApiResponse {
  data_id: number;
  user_full_name: string;
  is_verified: boolean;
}

function processResponse(response: ApiResponse): void {
  // data_id -> id ga, user_full_name -> fullName ga, is_verified -> verified ga nomlanadi
  const { data_id: id, user_full_name: fullName, is_verified: verified } = response;

  console.log("Formatlangan ma'lumot:");
  console.log(`ID: ${id}, Ism: ${fullName}, Tasdiqlangan: ${verified}`);
}

processResponse({
  data_id: 4501,
  user_full_name: "Aziz Bekzodov",
  is_verified: true
});
```

## Tushuntirish va Mantiq:
1. Obyekt destrukturizatsiyasida `{ key: newName }` sintaksisi orqali obyektdagi xususiyatni boshqa o'zgaruvchi nomi bilan qabul qilish mumkin (aliasing).
2. Bu backend API dan kelgan `snake_case` formatidagi kalitlarni frontenddagi `camelCase` standartiga o'tkazishda juda foydali.
3. O'zgaruvchi nomi o'zgarsa ham, asl obyektdagi ma'lumot o'zgarmaydi.

## Ishlash natijasi:
```text
Formatlangan ma'lumot:
ID: 4501, Ism: Aziz Bekzodov, Tasdiqlangan: true
```


# 208-Topshiriq: Destrukturizatsiyada standart (default) qiymatlar

## Topshiriq sharti:
Obyektda xususiyat mavjud bo'lmaganda yoki uning qiymati `undefined` bo'lganda default qiymatlar berilishini namoyish eting.

## Yechim (JS yoki TS kodi):
```typescript
interface ThemeSettings {
  mode?: "light" | "dark";
  fontSize?: number;
  animationsEnabled?: boolean;
}

function applyTheme(settings: ThemeSettings): void {
  // Agar xususiyat undefined bo'lsa default qiymat olinadi
  const {
    mode = "dark",
    fontSize = 14,
    animationsEnabled = true
  } = settings;

  console.log(`Mavzu sozlamalari:\n- Rejim: ${mode}\n- Shrift: ${fontSize}px\n- Animatsiyalar: ${animationsEnabled}`);
}

console.log("1. Qisman sozlamalar:");
applyTheme({ fontSize: 16 });

console.log("\n2. Bo'sh sozlamalar:");
applyTheme({});
```

## Tushuntirish va Mantiq:
1. Destrukturizatsiyada `{ prop = defaultValue }` ko'rinishida standart qiymat beriladi.
2. Standart qiymat FAQAT xususiyat `undefined` bo'lgandagina ishga tushadi. Agar qiymat `null` bo'lsa, `null` qabul qilinadi.
3. Yangi qayta nomlash bilan birga ham ishlatilishi mumkin: `{ prop: alias = defaultValue }`.

## Ishlash natijasi:
```text
1. Qisman sozlamalar:
Mavzu sozlamalari:
- Rejim: dark
- Shrift: 16px
- Animatsiyalar: true

2. Bo'sh sozlamalar:
Mavzu sozlamalari:
- Rejim: dark
- Shrift: 14px
- Animatsiyalar: true
```


# 209-Topshiriq: Chuqur kiritilgan (Nested) destrukturizatsiya

## Topshiriq sharti:
Chuqur kiritilgan murakkab API javobidan kerakli maydonlarni bitta ifodada ajratib olishni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
const apiData = {
  status: 200,
  payload: {
    user: {
      profile: {
        firstName: "Madina",
        contacts: {
          telegram: "@madina_dev"
        }
      }
    }
  }
};

// Chuqur destrukturizatsiya
const {
  payload: {
    user: {
      profile: {
        firstName,
        contacts: { telegram }
      }
    }
  }
} = apiData;

console.log(`Foydalanuvchi: ${firstName}, Telegram: ${telegram}`);
```

## Tushuntirish va Mantiq:
1. Jingalak qavslarni ichma-ich yozish orqali eng quyi darajadagi obyekt maydonlariga ham to'g'ridan-to'g'ri o'zgaruvchi sifatida kirish mumkin.
2. Eslatma: agar oraliq obyektlardan biri (masalan `profile` yoki `contacts`) `undefined` bo'lsa, butun ifoda `TypeError` tashlaydi.
3. Shu sababli oraliq obyektlar yo'q bo'lishi ehtimoli bo'lsa, default bo'sh obyekt `{}` berish tavsiya qilinadi: `{ contacts: { telegram } = {} }`.

## Ishlash natijasi:
```text
Foydalanuvchi: Madina, Telegram: @madina_dev
```


# 210-Topshiriq: Destrukturizatsiyada Rest operatori: Qolgan xususiyatlarni ajratish

## Topshiriq sharti:
Obyektdan maxfiy yoki keraksiz maydonlarni ajratib olib, qolgan hamma maydonlarni yangi obyektga to'plang.

## Yechim (JS yoki TS kodi):
```typescript
interface UserRecord {
  id: number;
  passwordHash: string;
  salt: string;
  name: string;
  email: string;
}

function sanitizeUser(user: UserRecord) {
  // passwordHash va salt alohida o'zgaruvchiga olinadi, qolgani safeProfile ga o'tadi
  const { passwordHash, salt, ...safeProfile } = user;

  return safeProfile;
}

const rawUser: UserRecord = {
  id: 1,
  name: "Jasur",
  email: "jasur@mail.uz",
  passwordHash: "a8f5f167f44f4964e6c998dee827110c",
  salt: "secret_salt_99"
};

const clientSafeData = sanitizeUser(rawUser);
console.log("Mijozga yuboriladigan xavfsiz profil:", clientSafeData);
```

## Tushuntirish va Mantiq:
1. Destrukturizatsiyadagi rest operatori (`...rest`) ko'rsatilmagan barcha qolgan xususiyatlardan iborat yangi obyekt yaratadi.
2. Bu `delete user.passwordHash` mutatsiyasidan ancha xavfsiz va toza, chunki asl obyekt butunlay o'zgarmas qoladi.
3. Backendda maxfiy ma'lumotlarni mijozga yuborishdan oldin tozalashda asosiy usuldir.

## Ishlash natijasi:
```text
Mijozga yuboriladigan xavfsiz profil: { id: 1, name: 'Jasur', email: 'jasur@mail.uz' }
```


# 211-Topshiriq: O'zgaruvchilar qiymatini destrukturizatsiya orqali almashtirish (Swap)

## Topshiriq sharti:
Uchinchi vaqtinchalik o'zgaruvchisiz ikkita o'zgaruvchi qiymatini massiv destrukturizatsiyasi orqali almashtiring.

## Yechim (JS yoki TS kodi):
```typescript
function swapVariables(): void {
  let primaryColor = "Qizil";
  let secondaryColor = "Ko'k";

  console.log(`Dastlabki: primary = '${primaryColor}', secondary = '${secondaryColor}'`);

  // Bitta qatorda almashtirish
  [primaryColor, secondaryColor] = [secondaryColor, primaryColor];

  console.log(`Almashtirilgach: primary = '${primaryColor}', secondary = '${secondaryColor}'`);
}

swapVariables();
```

## Tushuntirish va Mantiq:
1. `[a, b] = [b, a]` ifodasi o'ng tomonda yangi vaqtinchalik 2 elementli massiv tuzadi va chap tomondagi destrukturizatsiya orqali ularni yangi o'zgaruvchilarga taqsimlaydi.
2. Qo'shimcha `temp` o'zgaruvchisiga hojat qolmaydi.
3. Saralash algoritmlarida (QuickSort, BubbleSort) elementlar o'rnini almashtirishda keng qo'llaniladi.

## Ishlash natijasi:
```text
Dastlabki: primary = 'Qizil', secondary = 'Ko'k'
Almashtirilgach: primary = 'Ko'k', secondary = 'Qizil'
```


# 212-Topshiriq: RegExp mosliklarini destrukturizatsiya qilish

## Topshiriq sharti:
Muntazam ifodadagi guruhlarni (capturing groups) to'g'ridan-to'g'ri massiv destrukturizatsiyasi orqali o'zgaruvchilarga ajrating.

## Yechim (JS yoki TS kodi):
```typescript
function parseDateString(dateStr: string): void {
  // YIL-OY-KUN formati: (\d{4})-(\d{2})-(\d{2})
  const regex = /^(\d{4})-(\d{2})-(\d{2})$/;
  const match = dateStr.match(regex);

  if (!match) {
    console.log("Noto'g'ri sana formati");
    return;
  }

  // match[0] to'liq satr, qolganlari guruhlar
  const [, year, month, day] = match;

  console.log(`Ajratildi: Yil = ${year}, Oy = ${month}, Kun = ${day}`);
}

parseDateString("2026-11-08");
```

## Tushuntirish va Mantiq:
1. `str.match(regex)` birinchi elementda to'liq moslikni (`match[0]`), keyingi indekslarda esa qavs ichidagi guruhlarni qaytaradi.
        2. `[, year, month, day]` destrukturizatsiyasi 0-indeksni tashlab o'tib, to'g'ridan-to'g'ri guruhlarni o'zgaruvchilarga biriktiradi.
        3. Matnlarni parse qilishda eng qisqa va qulay usuldir.

## Ishlash natijasi:
```text
Ajratildi: Yil = 2026, Oy = 11, Kun = 08
```


# 213-Topshiriq: Object.assign() va Obyektlarni birlashtirish

## Topshiriq sharti:
`Object.assign()` orqali bir nechta obyektdan bitta nishon (target) obyektga xususiyatlarni ko'chirishni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function testObjectAssign(): void {
  const target = { a: 1 };
  const source1 = { b: 2 };
  const source2 = { c: 3, a: 99 }; // a kalitini ezib yuboradi

  // Yangi bo'sh obyektga nusxalaymiz
  const combined = Object.assign({}, target, source1, source2);

  console.log("Birlashtirilgan obyekt:", combined);
  console.log("Asl target (o'zgarmadi):", target);

  // Agar birinchi argument target ning o'zi bo'lsa, u mutatsiyaga uchraydi:
  Object.assign(target, source1);
  console.log("Mutatsiyaga uchragan target:", target);
}

testObjectAssign();
```

## Tushuntirish va Mantiq:
1. `Object.assign(target, ...sources)` barcha manba obyektlarning sanaladigan xususiyatlarini `target` obyektiga ko'chiradi va `target` ni qaytaradi.
2. Agar bir xil kalit bir nechta manbada uchrasa, eng oxirgi manbaning qiymati oldingilarini ezib yuboradi (override).
3. Doimo birinchi parametr sifatida `{}` berish asl obyektlarning mutatsiyaga uchrashining oldini oladi.

## Ishlash natijasi:
```text
Birlashtirilgan obyekt: { a: 99, b: 2, c: 3 }
Asl target (o'zgarmadi): { a: 1 }
Mutatsiyaga uchragan target: { a: 1, b: 2 }
```


# 214-Topshiriq: Spread operatori bilan obyektlarni yangilash (Object Spread)

## Topshiriq sharti:
Obyekt spread operatori (`{ ...obj, updatedProp: val }`) yordamida holatni (state) o'zgarmas tarzda yangilashni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
interface AppState {
  theme: string;
  notifications: boolean;
  user: { name: string };
}

function updateState(prevState: AppState, updates: Partial<AppState>): AppState {
  return {
    ...prevState,
    ...updates
  };
}

const initialState: AppState = {
  theme: "light",
  notifications: true,
  user: { name: "Anvar" }
};

const nextState = updateState(initialState, { theme: "dark" });

console.log("Dastlabki holat:", initialState);
console.log("Yangilangan holat:", nextState);
console.log("Tenglik (alohida havolalar):", initialState === nextState); // false
```

## Tushuntirish va Mantiq:
1. Object spread (`{ ...obj }`) ES2018 da kiritilgan bo'lib, `Object.assign({}, obj)` ga qaraganda qisqaroq va deklarativdir.
2. Keyingi ko'rsatilgan xususiyatlar oldingilarini yangilaydi.
3. React va Redux da komponent holatini (state) immutabil boshqarishning poydevori hisoblanadi.

## Ishlash natijasi:
```text
Dastlabki holat: { theme: 'light', notifications: true, user: { name: 'Anvar' } }
Yangilangan holat: { theme: 'dark', notifications: true, user: { name: 'Anvar' } }
Tenglik (alohida havolalar): false
```


# 215-Topshiriq: structuredClone(): Zamonaviy rasmiy chuqur nusxalash

## Topshiriq sharti:
`structuredClone()` metodi yordamida murakkab siklik havolalar (circular references), Date va Map larni to'liq klonlashni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function testStructuredClone(): void {
  const original: any = {
    date: new Date(),
    numbers: new Set([1, 2, 3]),
    map: new Map([["key", "value"]]),
    nested: { count: 42 }
  };

  // Siklik havola qo'shamiz (JSON.stringify buni eplay olmay xato beradi)
  original.self = original;

  // structuredClone to'liq chuqur nusxa oladi
  const clone = structuredClone(original);

  console.log("Klon muvaffaqiyatli yaratildi:", clone !== original);
  console.log("Ichki nested obyekt teng emas:", clone.nested !== original.nested);
  console.log("clone.date turi:", clone.date instanceof Date);
  console.log("Siklik havola to'g'ri tiklandi:", clone.self === clone);
}

testStructuredClone();
```

## Tushuntirish va Mantiq:
1. Tarixiy jihatdan dasturchilar `JSON.parse(JSON.stringify(obj))` usulidan foydalanishgan, ammo u `Date` ni stringga aylantirib qo'yadi, `Map`, `Set`, `undefined` larni yo'qotadi va siklik havolalarda (`circular reference`) dasturni to'xtatadi.
2. `structuredClone(val)` HTML5 spetsifikatsiyasiga kiritilgan va barcha zamonaviy brauzerlar hamda Node.js da o'rnatilgan rasmiy chuqur nusxalash mexanizmidir.
3. U deyarli barcha murakkab tuzilmalarni aniq saqlab qoladi.

## Ishlash natijasi:
```text
Klon muvaffaqiyatli yaratildi: true
Ichki nested obyekt teng emas: true
clone.date turi: true
Siklik havola to'g'ri tiklandi: true
```


# 216-Topshiriq: Object.freeze(): Obyektni muzlatish va sayozlik cheklovi

## Topshiriq sharti:
`Object.freeze()` orqali obyektni muzlatish va uning ichidagi kiritilgan (nested) obyektlar muzlamasdan qolishini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function testObjectFreeze(): void {
  const config = {
    appName: "MeningIlovam",
    db: {
      host: "localhost"
    }
  };

  Object.freeze(config);

  // 1. Yuqori darajani o'zgartirishga urinish
  try {
    // @ts-ignore
    config.appName = "BoshqaNom";
  } catch (err: any) {
    console.log("appName o'zgarmadi:", err.message);
  }

  // 2. Sayozlik (Shallow) muammosi: ichki obyekt muzlamagan!
  config.db.host = "production.db.uz";
  console.log("Ichki db.host o'zgarib ketdi:", config.db.host);
}

testObjectFreeze();
```

## Tushuntirish va Mantiq:
1. `Object.freeze(obj)` obyektni sayoz (shallow) muzlatadi: yangi xususiyat qo'shib bo'lmaydi, mavjudlarini o'chirib yoki qiymatini o'zgartirib bo'lmaydi.
2. Biroq, agar xususiyat qiymati boshqa obyekt bo'lsa, u obyekt muzlatilmagan bo'ladi.
3. Haqiqiy to'liq o'zgarmaslik uchun Deep Freeze algoritmi talab etiladi.

## Ishlash natijasi:
```text
appName o'zgarmadi: Cannot assign to read only property 'appName' of object '#<Object>'
Ichki db.host o'zgarib ketdi: production.db.uz
```


# 217-Topshiriq: Deep Freeze: Barcha ichki obyektlarni rekursiv muzlatish

## Topshiriq sharti:
Ixtiyoriy chuqurlikdagi ichki obyektlarni ham to'liq muzlatuvchi rekursiv `deepFreeze` funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function deepFreeze<T extends object>(obj: T): Readonly<T> {
  // Avval o'zini muzlatamiz
  Object.freeze(obj);

  // Barcha xususiyatlarni ko'rib chiqamiz
  Object.getOwnPropertyNames(obj).forEach((prop) => {
    const val = (obj as any)[prop];
    if (val !== null && (typeof val === "object" || typeof val === "function") && !Object.isFrozen(val)) {
      deepFreeze(val); // Rekursiv muzlatish
    }
  });

  return obj;
}

const secureConfig = deepFreeze({
  server: {
    ip: "192.168.1.1",
    ports: [80, 443]
  }
});

try {
  // @ts-ignore
  secureConfig.server.ports.push(8080);
} catch (err: any) {
  console.log("Ichki massiv ham muzlatilgan:", err.message);
}
```

## Tushuntirish va Mantiq:
1. Rekursiv `deepFreeze` funksiyasi obyektning barcha xususiyatlarini aylanib chiqadi.
2. Agar xususiyat obyekt bo'lsa va hali muzlatilmagan bo'lsa (`!Object.isFrozen(val)`), unga yana `deepFreeze` chaqiradi.
3. Natijada massivlar, ichki obyektlar va sozlamalar butunlay o'zgarmas holatga keladi.

## Ishlash natijasi:
```text
Ichki massiv ham muzlatilgan: Cannot add property 2, object is not extensible
```


# 218-Topshiriq: Object.seal(): Obyektni muhrlash

## Topshiriq sharti:
`Object.seal()` va `Object.freeze()` o'rtasidagi farqni (mavjud qiymatlarni o'zgartirish ruxsat etilganligi) amalda ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function testObjectSeal(): void {
  const character = {
    name: "Javohir",
    health: 100
  };

  Object.seal(character);

  // 1. Mavjud xususiyatni o'zgartirish mumkin!
  character.health = 85;
  console.log("Mavjud xususiyat yangilandi:", character.health);

  // 2. Yangi xususiyat qo'shish mumkin emas
  try {
    // @ts-ignore
    character.mana = 50;
  } catch (err: any) {
    console.log("Yangi xususiyat qo'shilmadi:", err.message);
  }

  // 3. Mavjud xususiyatni o'chirib ham bo'lmaydi
  // @ts-ignore
  delete character.health;
  console.log("O'chirishdan keyin health:", character.health);
}

testObjectSeal();
```

## Tushuntirish va Mantiq:
1. `Object.seal()` obyektni muhrlaydi: mavjud xususiyatlarning `configurable` xususiyatini `false` qiladi.
2. Natijada obyektdan xususiyatlarni o'chirish (`delete`) yoki yangilarini qo'shish taqiqlanadi.
3. Ammo `freeze` dan farqli ravishda, agar xususiyat `writable: true` bo'lsa, uning qiymatini o'zgartirishga ruxsat beriladi.

## Ishlash natijasi:
```text
Mavjud xususiyat yangilandi: 85
Yangi xususiyat qo'shilmadi: Cannot add property mana, object is not extensible
O'chirishdan keyin health: 85
```


# 219-Topshiriq: Object.preventExtensions() va kengaytirishni taqiqlash

## Topshiriq sharti:
Obyektga yangi xususiyatlar qo'shilishini cheklovchi `Object.preventExtensions()` metodini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function testPreventExtensions(): void {
  const settings = { theme: "light" };

  console.log("Kengaytirilishi mumkinmi:", Object.isExtensible(settings)); // true

  Object.preventExtensions(settings);
  console.log("preventExtensions dan keyin:", Object.isExtensible(settings)); // false

  try {
    // @ts-ignore
    settings.lang = "uz";
  } catch (err: any) {
    console.log("Yangi kalit qo'shishda xatolik:", err.message);
  }

  // Mavjud xususiyatni o'chirish mumkin!
  delete (settings as any).theme;
  console.log("Xususiyat o'chirilgach obyekt:", settings);
}

testPreventExtensions();
```

## Tushuntirish va Mantiq:
1. `Object.preventExtensions()` eng yumshoq cheklov darajasi hisoblanadi: faqat yangi kalitlar qo'shilishini to'xtatadi.
2. Mavjud kalitlarni o'zgartirish yoki hatto o'chirib tashlash (`delete`) mumkin.
3. Obyektning kengaytiruvchanligini `Object.isExtensible(obj)` orqali tekshirish mumkin.

## Ishlash natijasi:
```text
Kengaytirilishi mumkinmi: true
preventExtensions dan keyin: false
Yangi kalit qo'shishda xatolik: Cannot add property lang, object is not extensible
Xususiyat o'chirilgach obyekt: {}
```


# 220-Topshiriq: Property Descriptors: writable, enumerable, configurable

## Topshiriq sharti:
`Object.defineProperty()` orqali konsolda ko'rinmaydigan (non-enumerable) va qayta yozilmaydigan maxfiy xususiyat yarating.

## Yechim (JS yoki TS kodi):
```typescript
function testPropertyDescriptors(): void {
  const user = { username: "akrom" };

  // Maxsus identifikator xususiyatini o'rnatamiz
  Object.defineProperty(user, "internalId", {
    value: "SEC_998811",
    writable: false,     // Qiymatni o'zgartirib bo'lmaydi
    enumerable: false,   // Object.keys yoki for...in da ko'rinmaydi
    configurable: false  // Xususiyatni o'chirib yoki qayta sozlab bo'lmaydi
  });

  console.log("Object.keys(user):", Object.keys(user)); // Faqat 'username' chiqadi
  console.log("To'g'ridan-to'g'ri o'qish:", (user as any).internalId);

  // Deskriptorni tekshiramiz
  const desc = Object.getOwnPropertyDescriptor(user, "internalId");
  console.log("internalId deskriptori:", desc);
}

testPropertyDescriptors();
```

## Tushuntirish va Mantiq:
1. Har bir JavaScript obyekt xususiyati orqasida maxsus Xususiyat Deskriptori (Property Descriptor) yotadi.
2. `value`: haqiqiy saqlangan qiymat.
3. `writable`: `false` bo'lsa yangi qiymat berish taqiqlanadi.
4. `enumerable`: `false` bo'lsa sikllarda va `JSON.stringify` da yashiriladi.
5. `configurable`: `false` bo'lsa xususiyatni o'chirish yoki uning deskriptorini o'zgartirish taqiqlanadi.

## Ishlash natijasi:
```text
Object.keys(user): [ 'username' ]
To'g'ridan-to'g'ri o'qish: SEC_998811
internalId deskriptori: {
  value: 'SEC_998811',
  writable: false,
  enumerable: false,
  configurable: false
}
```


# 221-Topshiriq: Getter va Setter: Validatsiya va himoyalangan xususiyatlar

## Topshiriq sharti:
Getter (`get`) va Setter (`set`) yordamida foydalanuvchi yoshi faqat 0 va 120 oralig'ida bo'lishini ta'minlovchi xavfsiz obyekt yarating.

## Yechim (JS yoki TS kodi):
```typescript
class UserAccount {
  private _age: number = 18;

  get age(): number {
    return this._age;
  }

  set age(newAge: number) {
    if (newAge < 0 || newAge > 120) {
      console.log(`Xato: Yosh noto'g'ri (${newAge}). O'zgartirilmadi.`);
      return;
    }
    this._age = newAge;
    console.log(`Yosh muvaffaqiyatli yangilandi: ${this._age}`);
  }
}

const account = new UserAccount();
console.log("Dastlabki yosh:", account.age);

account.age = 25; // Setter ishlaydi
account.age = -5; // Noto'g'ri yosh, rad etiladi
account.age = 150; // Noto'g'ri yosh, rad etiladi

console.log("Yakuniy yosh:", account.age);
```

## Tushuntirish va Mantiq:
1. Getter (`get prop()`) xususiyat o'qilganda avtomatik chaqiriladigan funksiyadir.
2. Setter (`set prop(val)`) xususiyatga qiymat berilganda (`obj.prop = val`) ishga tushadi va qiymatni tekshirish, formatlash imkonini beradi.
3. Bu OOP ning inkapsulyatsiya tamoyilini chiroyli sintaksis bilan ta'minlaydi.

## Ishlash natijasi:
```text
Dastlabki yosh: 18
Yosh muvaffaqiyatli yangilandi: 25
Xato: Yosh noto'g'ri (-5). O'zgartirilmadi.
Xato: Yosh noto'g'ri (150). O'zgartirilmadi.
Yakuniy yosh: 25
```


# 222-Topshiriq: Prototip zanjiri (Prototype Chain) va Merosxo'rlik

## Topshiriq sharti:
Obyekt o'zida mavjud bo'lmagan xususiyatni o'zining prototipidan qanday qidirib topishini ko'rsatuvchi dastur yozing.

## Yechim (JS yoki TS kodi):
```typescript
function testPrototypeChain(): void {
  const vehicle = {
    hasWheels: true,
    move() {
      return "Harakatlanmoqda...";
    }
  };

  // vehicle ni prototip qilib car yaratamiz
  const car = Object.create(vehicle);
  car.brand = "Chevrolet";

  console.log("car.brand (o'ziniki):", car.brand);
  console.log("car.hasWheels (prototipdan):", car.hasWheels);
  console.log("car.move() (prototip metod):", car.move());

  console.log("car ning prototipi vehicle mi:", Object.getPrototypeOf(car) === vehicle);
}

testPrototypeChain();
```

## Tushuntirish va Mantiq:
1. JavaScript sinflariga asoslangan emas, balki prototiplarga asoslangan tildir (Prototypal Inheritance).
2. Har bir obyekt yashirin `[[Prototype]]` havolasiga ega bo'ladi.
3. Biror xususiyat chaqirilganda, dvigatel avval obyektning o'zini tekshiradi, topolmasa uning prototipiga, so'ng prototipning prototipiga (toki `Object.prototype` gacha) qarab zanjir bo'yicha ko'tariladi.

## Ishlash natijasi:
```text
car.brand (o'ziniki): Chevrolet
car.hasWheels (prototipdan): true
car.move() (prototip metod): Harakatlanmoqda...
car ning prototipi vehicle mi: true
```


# 223-Topshiriq: Object.create(null): Sof xotira xaritasi (Clean Dictionary)

## Topshiriq sharti:
`Object.create(null)` yordamida hech qanday prototipga (hatto `toString`, `valueOf` ga ham) ega bo'lmagan sof lug'at yaratishni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function testNullPrototype(): void {
  // Oddiy obyekt Object.prototype dan meros oladi
  const normalObj: any = {};
  console.log("'toString' oddiy obyektdami:", "toString" in normalObj); // true

  // Prototipsiz toza lug'at
  const cleanDict: any = Object.create(null);
  console.log("'toString' cleanDict dami:", "toString" in cleanDict); // false!

  cleanDict["apple"] = "olma";
  cleanDict["banana"] = "banan";

  console.log("cleanDict['apple']:", cleanDict["apple"]);
  console.log("cleanDict prototipi:", Object.getPrototypeOf(cleanDict)); // null
}

testNullPrototype();
```

## Tushuntirish va Mantiq:
1. Oddiy `{}` obyekti `Object.prototype` dagi o'nlab metodlarni (`toString`, `hasOwnProperty`, `constructor`) o'z ichiga oladi.
2. Bu foydalanuvchi kiritgan ixtiyoriy kalitlarni saqlashda xavfli bo'lishi mumkin (masalan, foydalanuvchi 'toString' degan kalit kiritsa, xatolik yuzaga kelishi mumkin).
3. `Object.create(null)` hech qanday prototip zanjiriga ega bo'lmagan, 100% sof kalit-qiymat xaritasi yaratadi.

## Ishlash natijasi:
```text
'toString' oddiy obyektdami: true
'toString' cleanDict dami: false
cleanDict['apple']: olma
cleanDict prototipi: null
```


# 224-Topshiriq: Object.hasOwn() vs hasOwnProperty(): Xavfsiz kalit tekshiruvi

## Topshiriq sharti:
ES2022 ning `Object.hasOwn()` metodi nima uchun eski `obj.hasOwnProperty()` dan ustun ekanligini isbotlang.

## Yechim (JS yoki TS kodi):
```typescript
function testHasOwnSafety(): void {
  // 1. Obyekt hasOwnProperty xususiyatini o'zi qayta yozib olgan bo'lsa:
  const trickyObj = {
    name: "Ali",
    hasOwnProperty: () => false // Zararli yoki tasodifiy override
  };

  // @ts-ignore
  console.log("trickyObj.hasOwnProperty('name'):", trickyObj.hasOwnProperty("name")); // false (aldanib qoldik!)
  console.log("Object.hasOwn(trickyObj, 'name'):", Object.hasOwn(trickyObj, "name")); // true (to'g'ri!)

  // 2. Prototipsiz obyektdagi holat:
  const nullProtoObj: any = Object.create(null);
  nullProtoObj.id = 100;

  try {
    nullProtoObj.hasOwnProperty("id"); // TypeError! Chunki hasOwnProperty yo'q
  } catch (err: any) {
    console.log("nullProtoObj.hasOwnProperty xatosi:", err.name);
  }

  console.log("Object.hasOwn(nullProtoObj, 'id'):", Object.hasOwn(nullProtoObj, "id")); // true!
}

testHasOwnSafety();
```

## Tushuntirish va Mantiq:
1. `obj.hasOwnProperty()` xususiyatini obyektning o'zida qayta yozib yuborish mumkin yoki `Object.create(null)` da u mavjud bo'lmaydi.
2. Shu bois avvallari `Object.prototype.hasOwnProperty.call(obj, prop)` deb yozishga to'g'ri kelgan.
3. ES2022 da kiritilgan statik `Object.hasOwn(obj, prop)` har qanday obyekt bilan mutlaq xavfsiz ishlaydi.

## Ishlash natijasi:
```text
trickyObj.hasOwnProperty('name'): false
Object.hasOwn(trickyObj, 'name'): true
nullProtoObj.hasOwnProperty xatosi: TypeError
Object.hasOwn(nullProtoObj, 'id'): true
```


# 225-Topshiriq: Object.getPrototypeOf() va getOwnPropertyNames()

## Topshiriq sharti:
Obyektning prototipini o'qish va uning barcha (ko'rinadigan va yashirin) xususiyatlar nomlarini ro'yxatga olishni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function inspectObjectReflection(): void {
  const base = { baseRole: "user" };
  const admin = Object.create(base);
  admin.name = "Alisher";

  Object.defineProperty(admin, "hiddenSecret", {
    value: "12345",
    enumerable: false
  });

  console.log("1. Object.keys (faqat sanaladigan):", Object.keys(admin));
  console.log("2. getOwnPropertyNames (yashirinlari ham):", Object.getOwnPropertyNames(admin));
  console.log("3. getPrototypeOf:", Object.getPrototypeOf(admin));
}

inspectObjectReflection();
```

## Tushuntirish va Mantiq:
1. `Object.keys()` faqat `enumerable: true` bo'lgan shaxsiy kalitlarni qaytaradi.
2. `Object.getOwnPropertyNames()` esa sanaladigan hamda sanalmaydigan (`enumerable: false`) barcha shaxsiy kalitlarni olib beradi.
3. `Object.getPrototypeOf()` obyektdan uning ota prototipiga xavfsiz havolani qaytaradi.

## Ishlash natijasi:
```text
1. Object.keys (faqat sanaladigan): [ 'name' ]
2. getOwnPropertyNames (yashirinlari ham): [ 'name', 'hiddenSecret' ]
3. getPrototypeOf: { baseRole: 'user' }
```


# 226-Topshiriq: WeakMap: Obyektlar uchun xotira sizishisiz ma'lumotlar saqlash

## Topshiriq sharti:
`WeakMap` yordamida DOM elementlari yoki obyektlar xotiradan o'chirilganda avtomatik tozalanuvchi metadata omborini yarating.

## Yechim (JS yoki TS kodi):
```typescript
function testWeakMap(): void {
  const metaStore = new WeakMap<object, { visitCount: number }>();

  let userObject: any = { id: 1, name: "Botir" };

  // Obyektga metadata biriktiramiz
  metaStore.set(userObject, { visitCount: 5 });

  console.log("Obyekt bo'yicha metadata:", metaStore.get(userObject));
  console.log("metaStore da bormi:", metaStore.has(userObject));

  // userObject xotiradan o'chirilsa:
  userObject = null;
  // Garbage Collector userObject ni xotiradan tozalaganda, WeakMap dagi ma'lumot ham avtomatik o'chiriladi!
  console.log("Havola nollashtirildi, xotira sizishi yo'q.");
}

testWeakMap();
```

## Tushuntirish va Mantiq:
1. `WeakMap` kalitlari faqat obyektlar bo'lishi mumkin.
2. WeakMap kalit bo'lgan obyektlarga kuchsiz (weak) havola saqlaydi: agar obyektga dasturning boshqa joyida havola qolmasa, u Garbage Collector tomonidan xotiradan o'chiriladi.
3. WeakMap o'lchamini (`size`) bilib bo'lmaydi va uni aylanib (`iterate`) chiqib bo'lmaydi.

## Ishlash natijasi:
```text
Obyekt bo'yicha metadata: { visitCount: 5 }
metaStore da bormi: true
Havola nollashtirildi, xotira sizishi yo'q.
```


# 227-Topshiriq: WeakSet: Obyektlar to'plami va teglash mexanizmi

## Topshiriq sharti:
Obyektlarning qayta ishlangani yoki ruxsat etilganligini `WeakSet` orqali belgilovchi xavfsiz tizim yarating.

## Yechim (JS yoki TS kodi):
```typescript
function testWeakSet(): void {
  const processedItems = new WeakSet<object>();

  function processOnce(item: object): void {
    if (processedItems.has(item)) {
      console.log("Bu obyekt allaqachon qayta ishlangan! Qayta bajarilmaydi.");
      return;
    }

    console.log("Obyekt ilk bor muvaffaqiyatli qayta ishlandi.");
    processedItems.add(item);
  }

  const taskA = { task: "A" };
  processOnce(taskA);
  processOnce(taskA); // Qayta chaqiruv rad etiladi
}

testWeakSet();
```

## Tushuntirish va Mantiq:
1. `WeakSet` faqat obyektlarni saqlaydi va ularga kuchsiz havola bilan birikadi.
2. Obyekt boshqa joyda kerak bo'lmay qolsa, u avtomatik ravishda WeakSet dan ham yo'qoladi.
3. Obyektlarni teglash (marking) yoki ularni 'faqat bir marta' tekshirishda juda samarali.

## Ishlash natijasi:
```text
Obyekt ilk bor muvaffaqiyatli qayta ishlandi.
Bu obyekt allaqachon qayta ishlangan! Qayta bajarilmaydi.
```


# 228-Topshiriq: JSON.stringify Replacer: Obyektni tanlab formatlash

## Topshiriq sharti:
`JSON.stringify` ning ikkinchi `replacer` parametri yordamida obyekt ichidagi parollarni yashirish yoki faqat kerakli maydonlarni qoldirishni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function serializeUser(): void {
  const account = {
    id: 101,
    name: "Sherzod",
    password: "secret_password_123",
    salary: 5000000,
    role: "manager"
  };

  // 1. Faqat oq ro'yxatdagi (whitelist) maydonlarni chiqarish
  const jsonWhitelist = JSON.stringify(account, ["id", "name", "role"], 2);
  console.log("Oq ro'yxat bilan JSON:\n" + jsonWhitelist);

  // 2. Callback replacer orqali parollarni maskalash
  const jsonMasked = JSON.stringify(account, (key, value) => {
    if (key === "password") return "********";
    return value;
  });
  console.log("\nMaskalangan JSON:\n" + jsonMasked);
}

serializeUser();
```

## Tushuntirish va Mantiq:
1. `JSON.stringify(obj, replacer, space)` juda kuchli sozlash imkoniyatlariga ega.
2. `replacer` massiv bo'lsa, faqat shu massivdagi kalitlar serializatsiya qilinadi.
3. `replacer` funksiya bo'lsa, har bir kalit-qiymat uchun chaqiriladi va nozik ma'lumotlarni o'zgartirish yoki filtrlab tashlash imkonini beradi.

## Ishlash natijasi:
```text
Oq ro'yxat bilan JSON:
{
  "id": 101,
  "name": "Sherzod",
  "role": "manager"
}

Maskalangan JSON:
{"id":101,"name":"Sherzod","password":"********","salary":5000000,"role":"manager"}
```


# 229-Topshiriq: JSON.parse Reviver: Sanalarni avtomatik Date obyektiga aylantirish

## Topshiriq sharti:
JSON satrdan obyekt o'qiyotganda sana formatidagi satrlarni avtomatik ravishda haqiqiy `Date` obyektiga aylantiruvchi `reviver` funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function parseWithDates(jsonString: string) {
  const dateFormatRegex = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/;

  return JSON.parse(jsonString, (key, value) => {
    if (typeof value === "string" && dateFormatRegex.test(value)) {
      return new Date(value);
    }
    return value;
  });
}

const jsonPayload = '{"title":"Uchrashuv","createdAt":"2026-11-08T10:00:00.000Z"}';
const parsed = parseWithDates(jsonPayload);

console.log("parsed.title:", parsed.title);
console.log("parsed.createdAt turi:", typeof parsed.createdAt);
console.log("parsed.createdAt Date obyekti ekanligi:", parsed.createdAt instanceof Date);
console.log("Yil:", parsed.createdAt.getFullYear());
```

## Tushuntirish va Mantiq:
1. Standart `JSON.parse` barcha sanalarni oddiy `string` sifatida qoldiradi, bu esa keyinchalik sana metodlarini chaqirishda xato beradi.
2. `reviver` funksiyasi har bir qiymatni tekshiradi va ISO 8601 sana formatiga mos kelsa, uni to'g'ridan-to'g'ri `new Date(val)` ga aylantirib qaytaradi.

## Ishlash natijasi:
```text
parsed.title: Uchrashuv
parsed.createdAt turi: object
parsed.createdAt Date obyekti ekanligi: true
Yil: 2026
```


# 230-Topshiriq: toJSON() Maxsus Metodi: Obyekt serializatsiyasini o'zi boshqarishi

## Topshiriq sharti:
Obyektda `toJSON()` metodini yaratish orqali uning `JSON.stringify` chaqirilganda qanday formatda chiqishini to'liq nazorat qiling.

## Yechim (JS yoki TS kodi):
```typescript
class SecretUser {
  constructor(public id: number, public name: string, private pin: string) {}

  // JSON.stringify avtomatik ushbu metodni qidiradi
  toJSON() {
    return {
      userId: this.id,
      displayName: this.name.toUpperCase(),
      hasPin: Boolean(this.pin)
      // pin ning o'zi sir tutiladi!
    };
  }
}

const securePerson = new SecretUser(77, "Sardor", "4455");
console.log("JSON.stringify natijasi:\n" + JSON.stringify(securePerson, null, 2));
```

## Tushuntirish va Mantiq:
1. Agar obyektda `toJSON()` metodi mavjud bo'lsa, `JSON.stringify()` odatiy xususiyatlarni emas, aynan shu metod qaytargan qiymatni satrga o'giradi.
2. `Date` obyekti o'zining `toJSON()` metodiga ega bo'lgani uchun JSON da ISO satr ko'rinishida chiqadi.
3. Sinflar va ma'lumotlar modellarida xavfsiz DTO yaratishda juda qo'l keladi.

## Ishlash natijasi:
```text
JSON.stringify natijasi:
{
  "userId": 77,
  "displayName": "SARDOR",
  "hasPin": true
}
```


# 231-Topshiriq: Obyekt kalitlarining saralanish tartibi (Property Order)

## Topshiriq sharti:
JavaScript dvigateli obyekt kalitlarini (raqamli indekslar, satrlar, simvollar) qanday qat'iy tartibda saralashini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function testPropertyOrder(): void {
  const obj: any = {};

  obj["b"] = "Satr b";
  obj[2] = "Raqam 2";
  obj[1] = "Raqam 1";
  obj["a"] = "Satr a";
  const sym = Symbol("s");
  obj[sym] = "Simvol";

  console.log("Object.keys tartibi:", Object.keys(obj));
  console.log("Reflect.ownKeys (barchasi):", Reflect.ownKeys(obj));
}

testPropertyOrder();
```

## Tushuntirish va Mantiq:
1. ECMAScript spetsifikatsiyasiga ko'ra obyekt kalitlari quyidagi qat'iy tartibda aylanadi:
   - Butun musbat sonli kalitlar (`0, 1, 2...`) har doim o'sish tartibida saralanadi (qo'shilgan vaqtidan qat'iy nazar).
   - Oddiy satrli kalitlar aynan kiritilgan (xronologik) tartibida chiqadi.
   - Symbol kalitlari eng oxirida joylashadi.
2. Bu qoida barcha zamonaviy dvigatellarda kafolatlangan.

## Ishlash natijasi:
```text
Object.keys tartibi: [ '1', '2', 'b', 'a' ]
Reflect.ownKeys (barchasi): [ '1', '2', 'b', 'a', Symbol(s) ]
```


# 232-Topshiriq: Invert Object: Kalitlar va qiymatlarni o'zaro almashtirish

## Topshiriq sharti:
Obyektning kalitlari va qiymatlarini o'zaro almashtiruvchi (invert) utilita funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function invertObject<K extends string | number, V extends string | number>(
  obj: Record<K, V>
): Record<V, K> {
  const result: any = {};
  for (const [key, value] of Object.entries(obj)) {
    result[value] = key;
  }
  return result;
}

const statusCodes = {
  SUCCESS: 200,
  NOT_FOUND: 404,
  SERVER_ERROR: 500
};

const inverted = invertObject(statusCodes);
console.log("Teskari o'girilgan lug'at:");
console.log(inverted);
console.log("404 kodi nomi:", inverted[404]);
```

## Tushuntirish va Mantiq:
1. Lug'atni teskari qilish kodlarni ularning nomlariga tezkor tarjima qilishda (`O(1)` qidiruv) kerak bo'ladi.
2. `Object.entries()` orqali juftliklar aylanadi va `result[value] = key` o'rnatiladi.
3. Agar qiymatlar takrorlanuvchi bo'lsa, oxirgi kalit avvalgisini ezib yuborishi inobatga olinishi kerak.

## Ishlash natijasi:
```text
Teskari o'girilgan lug'at:
{ '200': 'SUCCESS', '404': 'NOT_FOUND', '500': 'SERVER_ERROR' }
404 kodi nomi: NOT_FOUND
```


# 233-Topshiriq: Deep Get: Matnli yo'l (Path) bo'yicha qiymatni xavfsiz o'qish

## Topshiriq sharti:
Lodash `get` metodi kabi `'user.profile.address.city'` ko'rinishidagi satrli yo'l orqali chuqur obyektdan qiymatni xavfsiz o'quvchi funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
function getDeepValue(obj: any, path: string, fallback: any = undefined): any {
  // 'a.b.c' yoki 'a[0].b' kabi yo'llarni bo'lib olamiz
  const keys = path.replace(/\[(\w+)\]/g, ".$1").split(".");

  let current = obj;
  for (const key of keys) {
    if (current === null || current === undefined) {
      return fallback;
    }
    current = current[key];
  }

  return current !== undefined ? current : fallback;
}

const companyData = {
  subsidiary: {
    departments: [
      { name: "IT", lead: "Ali" }
    ]
  }
};

console.log("Yo'l 'subsidiary.departments.0.lead':", getDeepValue(companyData, "subsidiary.departments.0.lead"));
console.log("Mavjud bo'lmagan yo'l:", getDeepValue(companyData, "subsidiary.ceo.name", "Noma'lum"));
```

## Tushuntirish va Mantiq:
1. Dinamik yo'llar orqali ma'lumot olish konfiguratsiya tizimlari va jadvallarda (table column bindings) asosiy vositadir.
2. Satr nuqtalar bo'yicha bo'linadi (`split('.')`) va obyekt bo'ylab siklda chuqurlashiladi.
3. Agar zanjirning biron joyida `null` yoki `undefined` uchrasa, xatolik bermasdan `fallback` qiymat qaytadi.

## Ishlash natijasi:
```text
Yo'l 'subsidiary.departments.0.lead': Ali
Mavjud bo'lmagan yo'l: Noma'lum
```


# 234-Topshiriq: Deep Set: Matnli yo'l (Path) bo'yicha qiymat yozish

## Topshiriq sharti:
Obyektda `'user.settings.theme'` yo'li bo'yicha, oraliq obyektlar mavjud bo'lmagan taqdirda ularni avtomatik ochib qiymat yozuvchi funksiya yarating.

## Yechim (JS yoki TS kodi):
```typescript
function setDeepValue(obj: any, path: string, value: any): void {
  const keys = path.split(".");
  let current = obj;

  for (let i = 0; i < keys.length - 1; i++) {
    const key = keys[i];
    if (!(key in current) || typeof current[key] !== "object" || current[key] === null) {
      current[key] = {}; // Oraliq obyektni avtomatik yaratamiz
    }
    current = current[key];
  }

  current[keys[keys.length - 1]] = value;
}

const myAppConfig: any = {};
setDeepValue(myAppConfig, "system.database.host", "127.0.0.1");
setDeepValue(myAppConfig, "system.database.port", 5432);

console.log("Yaratilgan chuqur obyekt:\n", JSON.stringify(myAppConfig, null, 2));
```

## Tushuntirish va Mantiq:
1. `setDeepValue` oraliq obyektlar mavjud bo'lmasa, ularni avtomatik tarzda `{}` qilib yaratib ketadi.
2. Eng oxirgi kalitga yetganda berilgan qiymatni o'zlashtiradi.
3. Konfiguratsiyalarni dinamik yig'ish va form-builder dasturlarida ajralmas vositadir.

## Ishlash natijasi:
```text
Yaratilgan chuqur obyekt:
 {
  "system": {
    "database": {
      "host": "127.0.0.1",
      "port": 5432
    }
  }
}
```


# 235-Topshiriq: Deep Merge: Ikki obyektni chuqur birlashtirish

## Topshiriq sharti:
Ikki obyektning ichki qatlamlarini bir-birini ezib yubormasdan rekursiv tarzda birlashtiruvchi `deepMerge` funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function deepMerge(target: any, source: any): any {
  const isObject = (item: any) => item && typeof item === "object" && !Array.isArray(item);

  const output = { ...target };

  if (isObject(target) && isObject(source)) {
    Object.keys(source).forEach((key) => {
      if (isObject(source[key])) {
        if (!(key in target)) {
          output[key] = source[key];
        } else {
          output[key] = deepMerge(target[key], source[key]); // Rekursiv birlashtirish
        }
      } else {
        output[key] = source[key];
      }
    });
  }

  return output;
}

const defaultOptions = {
  theme: "dark",
  ui: {
    sidebar: true,
    fontSize: 14
  }
};

const userOptions = {
  ui: {
    fontSize: 18 // sidebar yo'qolib ketmasligi kerak!
  }
};

const merged = deepMerge(defaultOptions, userOptions);
console.log("Deep Merge natijasi:\n", JSON.stringify(merged, null, 2));
```

## Tushuntirish va Mantiq:
1. Oddiy `Object.assign` yoki spread `{ ...defaultOptions, ...userOptions }` ishlatilganda `ui` obyekti butunlay yangisi bilan almashtirilib, `sidebar: true` yo'qolib ketgan bo'lardi.
2. `deepMerge` ichki obyektlarni ham ko'rib chiqadi va faqat o'zgargan maydonlarni yangilab, qolganlarini saqlab qoladi.

## Ishlash natijasi:
```text
Deep Merge natijasi:
 {
  "theme": "dark",
  "ui": {
    "sidebar": true,
    "fontSize": 18
  }
}
```


# 236-Topshiriq: Object Diff: Ikki obyekt orasidagi farqlarni aniqlash

## Topshiriq sharti:
Dastlabki va yangilangan obyektlarni solishtirib, qaysi kalitlar o'zgarganini qaytaruvchi `getObjectDiff` utilitasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function getObjectDiff(oldObj: Record<string, any>, newObj: Record<string, any>) {
  const diff: Record<string, { old: any; new: any }> = {};

  const allKeys = new Set([...Object.keys(oldObj), ...Object.keys(newObj)]);

  for (const key of allKeys) {
    if (oldObj[key] !== newObj[key]) {
      diff[key] = {
        old: oldObj[key],
        new: newObj[key]
      };
    }
  }

  return diff;
}

const before = { name: "Anvar", role: "user", status: "active" };
const after = { name: "Anvar", role: "admin", status: "active", verified: true };

console.log("Farqlar tahlili:");
console.log(getObjectDiff(before, after));
```

## Tushuntirish va Mantiq:
1. Obyektlar auditida (masalan, foydalanuvchi profilida qaysi maydonlar o'zgarganini log qilishda) diffing kerak bo'ladi.
2. Ikkala obyekt kalitlari `Set` orqali birlashtiriladi.
3. Qiymatlari teng bo'lmagan har bir kalit uchun eski va yangi qiymat yozib olinadi.

## Ishlash natijasi:
```text
Farqlar tahlili:
{
  role: { old: 'user', new: 'admin' },
  verified: { old: undefined, new: true }
}
```


# 237-Topshiriq: Proxy API: Obyekt ustidan to'liq nazorat va get/set tuzoqlari

## Topshiriq sharti:
`Proxy` obyekti yordamida mavjud bo'lmagan xususiyat o'qilganda ogohlantiruvchi va qiymat yozilganda tip tekshiruvchi himoyalovchi wrapper yarating.

## Yechim (JS yoki TS kodi):
```typescript
interface StrictUser {
  name: string;
  age: number;
}

function createStrictUser(target: StrictUser): StrictUser {
  return new Proxy(target, {
    get(obj: any, prop: string) {
      if (prop in obj) {
        return obj[prop];
      }
      throw new ReferenceError(`Xususiyat '${prop}' obyektdan topilmadi!`);
    },
    set(obj: any, prop: string, value: any) {
      if (prop === "age" && (typeof value !== "number" || value < 0)) {
        throw new TypeError("Yosh musbat raqam bo'lishi shart!");
      }
      obj[prop] = value;
      return true;
    }
  });
}

const u = createStrictUser({ name: "Bobur", age: 25 });
console.log("Ismi:", u.name);

try {
  // @ts-ignore
  console.log(u.email);
} catch (e: any) {
  console.log("Get tuzog'i ushladi:", e.message);
}

try {
  // @ts-ignore
  u.age = "yigirma";
} catch (e: any) {
  console.log("Set tuzog'i ushladi:", e.message);
}
```

## Tushuntirish va Mantiq:
1. `Proxy(target, handler)` - ECMAScriptning eng kuchli meta-dasturlash imkoniyatlaridan biridir.
2. `get` tuzog'i xususiyat o'qilishini ushlaydi, `set` esa qiymat yozilishini nazorat qiladi.
3. Vue 3 ning reaktiv tizimi (Reactivity System) aynan JavaScript Proxy lariga asoslangan.

## Ishlash natijasi:
```text
Ismi: Bobur
Get tuzog'i ushladi: Xususiyat 'email' obyektdan topilmadi!
Set tuzog'i ushladi: Yosh musbat raqam bo'lishi shart!
```


# 238-Topshiriq: Reflect API: Standart amallarni funksional bajarish

## Topshiriq sharti:
`Reflect.get`, `Reflect.set`, `Reflect.has` va `Reflect.deleteProperty` metodlarining qo'llanilishini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function testReflectAPI(): void {
  const car: any = { make: "Toyota", year: 2022 };

  // Reflect.has ('in' operatori o'rniga)
  console.log("Reflect.has(car, 'make'):", Reflect.has(car, "make"));

  // Reflect.set
  Reflect.set(car, "color", "Oq");
  console.log("Reflect.get(car, 'color'):", Reflect.get(car, "color"));

  // Reflect.deleteProperty ('delete' o'rniga)
  const isDeleted = Reflect.deleteProperty(car, "year");
  console.log("Muvaffaqiyatli o'chirildimi:", isDeleted);
  console.log("O'chirilgach obyekt:", car);
}

testReflectAPI();
```

## Tushuntirish va Mantiq:
1. `Reflect` - bu ichki JavaScript operatsiyalarini (masalan `obj.prop`, `delete obj.prop`) chaqiruvchi metodlarni o'zida jamlagan global obyektdir.
2. Proxy handlerlari ichida standart xatti-harakatni davom ettirish uchun har doim `Reflect` metodlari bilan birga ishlatiladi.
3. Amallar boolean natija qaytaradi, bu esa xatoliklarni xavfsiz boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Reflect.has(car, 'make'): true
Reflect.get(car, 'color'): Oq
Muvaffaqiyatli o'chirildimi: true
O'chirilgach obyekt: { make: 'Toyota', color: 'Oq' }
```


# 239-Topshiriq: Proxy orqali Obyekt O'zgarishlarini Kuzatuvchi (Observer) tizim

## Topshiriq sharti:
Obyektning har qanday xususiyati o'zgarganda avtomatik ro'yxatdan o'tgan tinglovchini xabardor qiluvchi reaktiv Proxy yarating.

## Yechim (JS yoki TS kodi):
```typescript
function makeObservable<T extends object>(target: T, onChange: (prop: string, val: any) => void): T {
  return new Proxy(target, {
    set(obj, prop, value, receiver) {
      const success = Reflect.set(obj, prop, value, receiver);
      if (success) {
        onChange(String(prop), value);
      }
      return success;
    }
  });
}

const userProfile = { name: "Olim", status: "offline" };

const observableUser = makeObservable(userProfile, (prop, val) => {
  console.log(`[Reaktiv Hodisa]: '${prop}' xususiyati yangilandi -> ${val}`);
});

observableUser.status = "online";
observableUser.name = "Olimjon";
```

## Tushuntirish va Mantiq:
1. Ushbu naqsh zamonaviy frontend reaktiv kutubxonalarining (MobX, Vue) ishlash mexanizmidir.
2. Obyekt o'zgarganda `set` tuzog'i ishga tushadi va `Reflect.set` orqali haqiqiy o'zgarishni amalga oshirib, ro'yxatdagi `onChange` callbacklarini chaqiradi.
3. Dasturchi qo'lda hech qanday `render()` chaqirishi shart bo'lmaydi.

## Ishlash natijasi:
```text
[Reaktiv Hodisa]: 'status' xususiyati yangilandi -> online
[Reaktiv Hodisa]: 'name' xususiyati yangilandi -> Olimjon
```


# 240-Topshiriq: Amaliy loyiha: Mini Reaktiv Holat Ombori (Observable Store)

## Topshiriq sharti:
Proxy, Symbol, Object.freeze va Destructuring tamoyillarini birlashtirgan to'liq holat boshqaruvchisi (State Store) modulini yarating.

## Yechim (JS yoki TS kodi):
```typescript
type StateListener<T> = (state: Readonly<T>) => void;

class ReactiveStore<T extends object> {
  private _state: T;
  private listeners: Set<StateListener<T>> = new Set();

  constructor(initialState: T) {
    this._state = initialState;
  }

  // Holatni o'qish (faqat o'qish uchun)
  getState(): Readonly<T> {
    return Object.freeze({ ...this._state });
  }

  // Holatni xavfsiz yangilash
  setState(updater: Partial<T> | ((prev: T) => Partial<T>)): void {
    const changes = typeof updater === "function" ? updater(this._state) : updater;
    this._state = { ...this._state, ...changes };
    this.notify();
  }

  // Obuna bo'lish
  subscribe(listener: StateListener<T>): () => void {
    this.listeners.add(listener);
    // Unsubscribe funksiyasi qaytariladi
    return () => this.listeners.delete(listener);
  }

  private notify(): void {
    const readOnlyState = this.getState();
    this.listeners.forEach((fn) => fn(readOnlyState));
  }
}

interface AppStoreState {
  theme: "light" | "dark";
  cartCount: number;
}

const store = new ReactiveStore<AppStoreState>({
  theme: "light",
  cartCount: 0
});

// Obuna bo'lamiz
const unsubscribe = store.subscribe((state) => {
  console.log(`[Store Yangilandi]: Rejim: ${state.theme}, Savatchada: ${state.cartCount} ta`);
});

store.setState({ cartCount: 1 });
store.setState((prev) => ({ cartCount: prev.cartCount + 2, theme: "dark" }));

unsubscribe(); // Obuna bekor qilindi
store.setState({ cartCount: 10 }); // Xabar chiqmaydi
```

## Tushuntirish va Mantiq:
1. Ushbu loyiha obyektlar bo'limining barcha konseptlarini Redux/Zustand uslubidagi holat boshqaruvchisida mujassam etadi.
2. `getState()` da `Object.freeze` ishlatilishi tashqi kodning holatni to'g'ridan-to'g'ri buzishining oldini oladi.
3. `setState` funksional va ob'ektli yangilanishlarni qo'llab-quvvatlaydi hamda barcha tinglovchilarga avtomatik xabar beradi.

## Ishlash natijasi:
```text
[Store Yangilandi]: Rejim: light, Savatchada: 1 ta
[Store Yangilandi]: Rejim: dark, Savatchada: 3 ta
```


# 241-Topshiriq: Object.isFrozen, isSealed va isExtensible tekshiruvlari

## Topshiriq sharti:
Obyektning himoya darajasini (`isFrozen`, `isSealed`, `isExtensible`) aniqlovchi audit utilitasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function auditObjectSecurity(obj: object): void {
  console.log("Xavfsizlik darajasi tahlili:");
  console.log("- Kengaytirib bo'ladimi (isExtensible):", Object.isExtensible(obj));
  console.log("- Muhrlanganmi (isSealed):", Object.isSealed(obj));
  console.log("- Muzlatilganmi (isFrozen):", Object.isFrozen(obj));
}

const testObj = { id: 1 };
console.log("1. Oddiy obyekt:");
auditObjectSecurity(testObj);

Object.freeze(testObj);
console.log("\n2. Muzlatilgan obyekt:");
auditObjectSecurity(testObj);
```

## Tushuntirish va Mantiq:
1. `isExtensible`: yangi maydonlar qo'shish mumkinligini tekshiradi.
2. `isSealed`: yangi maydon qo'shib ham, mavjudlarini o'chirib ham bo'lmaydigan holatni bildiradi.
3. `isFrozen`: eng yuqori daraja bo'lib, o'zgartirish, qo'shish va o'chirish mutlaqo taqiqlanganligini bildiradi.

## Ishlash natijasi:
```text
1. Oddiy obyekt:
Xavfsizlik darajasi tahlili:
- Kengaytirib bo'ladimi (isExtensible): true
- Muhrlanganmi (isSealed): false
- Muzlatilganmi (isFrozen): false

2. Muzlatilgan obyekt:
Xavfsizlik darajasi tahlili:
- Kengaytirib bo'ladimi (isExtensible): false
- Muhrlanganmi (isSealed): true
- Muzlatilganmi (isFrozen): true
```


# 242-Topshiriq: Shallow Copy vs Deep Copy ning ichki obyektlaridagi xavfi

## Topshiriq sharti:
Obyekt spread qilinganda uning ichki massivlari bitta manzilga havola qilib qolishi oqibatida yuzaga keladigan xatolikni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function demonstrateShallowPitfall(): void {
  const originalUser = {
    name: "Akmal",
    skills: ["HTML", "CSS"]
  };

  // Sayoz nusxalash
  const copiedUser = { ...originalUser };
  copiedUser.name = "Sardor"; // Xavfsiz: primitiv mustaqil o'zgardi

  // Ichki massivga yangi ma'lumot qo'shamiz:
  copiedUser.skills.push("JavaScript");

  console.log("copiedUser ismi:", copiedUser.name);
  console.log("originalUser ismi:", originalUser.name);
  console.log("originalUser ko'nikmalari ham o'zgarib ketdi!:", originalUser.skills);
}

demonstrateShallowPitfall();
```

## Tushuntirish va Mantiq:
1. Spread `{ ...obj }` va `Object.assign` faqat birinchi darajali primitivlarni nusxalaydi.
2. Ichki obyektlar va massivlarning faqat xotiradagi manzili nusxalanadi.
3. Natijada `copiedUser.skills` ga kiritilgan o'zgarish `originalUser.skills` ni ham o'zgartiradi. Katta loyihalarda bu yashirin xatolarga sabab bo'ladi.

## Ishlash natijasi:
```text
copiedUser ismi: Sardor
originalUser ismi: Akmal
originalUser ko'nikmalari ham o'zgarib ketdi!: [ 'HTML', 'CSS', 'JavaScript' ]
```


# 243-Topshiriq: Dynamic Dispatch: Obyekt metodlari orqali strategiyalarni boshqarish

## Topshiriq sharti:
Strategy naqshini obyekt metodlari lug'ati orqali amalga oshirib turli to'lov tizimlarini qayta ishlang.

## Yechim (JS yoki TS kodi):
```typescript
type PaymentStrategy = (amount: number) => string;

const paymentHandlers: Record<string, PaymentStrategy> = {
  payme: (amount) => `Payme orqali ${amount} so'm to'landi.`,
  click: (amount) => `Click orqali ${amount} so'm to'landi.`,
  uzum: (amount) => `Uzum Bank orqali ${amount} so'm to'landi.`
};

function processClientPayment(gateway: string, amount: number): string {
  const handler = paymentHandlers[gateway];
  if (!handler) {
    throw new Error(`Noma'lum to'lov tizimi: ${gateway}`);
  }
  return handler(amount);
}

console.log(processClientPayment("payme", 50000));
console.log(processClientPayment("click", 120000));
```

## Tushuntirish va Mantiq:
1. Dynamic Dispatch (dinamik yo'naltirish) `if-else` shartlarisiz obyekt kalitlari orqali to'g'ri strategiyani tanlaydi.
2. Yangi to'lov tizimi qo'shish shunchaki `paymentHandlers` obyektiga yangi funksiya qo'shish bilan hal bo'ladi (Open/Closed Principle).

## Ishlash natijasi:
```text
Payme orqali 50000 so'm to'landi.
Click orqali 120000 so'm to'landi.
```


# 244-Topshiriq: Object.defineProperties(): Bir nechta xususiyatlarni bir vaqtda sozlash

## Topshiriq sharti:
`Object.defineProperties()` yordamida obyektga bir vaqtda bir nechta sozlamali xususiyatlar va hisoblanuvchi getterlarni biriktiring.

## Yechim (JS yoki TS kodi):
```typescript
function createPoint2D(x: number, y: number) {
  const point = {};

  Object.defineProperties(point, {
    x: { value: x, writable: false, enumerable: true },
    y: { value: y, writable: false, enumerable: true },
    distanceFromOrigin: {
      get() {
        return Math.hypot((this as any).x, (this as any).y);
      },
      enumerable: true
    }
  });

  return point;
}

const p = createPoint2D(3, 4);
console.log("Nuqta koordinatalari:", p);
console.log("Koordinata boshigacha masofa (hypot 3, 4):", (p as any).distanceFromOrigin);
```

## Tushuntirish va Mantiq:
1. `Object.defineProperties` bitta chaqiruvda bir nechta xususiyatlar deskriptorini o'rnatish imkonini beradi.
2. `distanceFromOrigin` getter sifatida o'rnatilgani uchun har safar o'qilganda dinamik hisoblanadi.
3. Koordinatalar `writable: false` bo'lgani sababli ularni tasodifan o'zgartirib bo'lmaydi.

## Ishlash natijasi:
```text
Nuqta koordinatalari: { x: 3, y: 4, distanceFromOrigin: 5 }
Koordinata boshigacha masofa (hypot 3, 4): 5
```


# 245-Topshiriq: Shartli destrukturizatsiya va xavfsiz qiymat olish

## Topshiriq sharti:
Obyekt bo'lishi yoki `null` bo'lishi mumkin bo'lgan javoblarni xavfsiz destrukturizatsiya qilish usulini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function getUserLocation(apiResponse: { data?: { coords?: { lat: number; lng: number } } } | null) {
  // Har bir pog'ona uchun fallback bo'sh obyekt beriladi
  const {
    data: {
      coords: { lat = 0, lng = 0 } = {}
    } = {}
  } = apiResponse || {};

  return { lat, lng };
}

console.log("1. To'liq ma'lumot:", getUserLocation({ data: { coords: { lat: 41.3, lng: 69.2 } } }));
console.log("2. Ma'lumot yo'q (null):", getUserLocation(null));
console.log("3. Bo'sh obyekt:", getUserLocation({}));
```

## Tushuntirish va Mantiq:
1. `{ data: { coords: { lat } = {} } = {} } = apiResponse || {}` sintaksisi har qanday bosqichda `null` yoki `undefined` kelishidan to'liq himoya qiladi.
2. Natijada hech qachon `TypeError: Cannot destructure property of undefined` xatosi ro'y bermaydi.

## Ishlash natijasi:
```text
1. To'liq ma'lumot: { lat: 41.3, lng: 69.2 }
2. Ma'lumot yo'q (null): { lat: 0, lng: 0 }
3. Bo'sh obyekt: { lat: 0, lng: 0 }
```


# 246-Topshiriq: Symbol.hasInstance bilan instanceof xulqini o'zgartirish

## Topshiriq sharti:
Klass yoki obyektga `Symbol.hasInstance` metodini qo'shish orqali uning `instanceof` tekshiruvini maxsus shart bo'yicha moslashtiring.

## Yechim (JS yoki TS kodi):
```typescript
class EvenNumberRange {
  static [Symbol.hasInstance](instance: any) {
    return typeof instance === "number" && instance % 2 === 0;
  }
}

console.log("4 instanceof EvenNumberRange:", 4 instanceof (EvenNumberRange as any));
console.log("7 instanceof EvenNumberRange:", 7 instanceof (EvenNumberRange as any));
console.log("'8' instanceof EvenNumberRange:", "8" instanceof (EvenNumberRange as any));
```

## Tushuntirish va Mantiq:
1. `Symbol.hasInstance` metodi `obj instanceof Constructor` operatorining ishlash mexanizmini to'liq o'zgartirish imkonini beradi.
2. Bu orqali prototip tekshiruvidan tashqari maxsus validatsiya qoidalarini (masalan, sonning juftligi) `instanceof` orqali ifodalash mumkin.

## Ishlash natijasi:
```text
4 instanceof EvenNumberRange: true
7 instanceof EvenNumberRange: false
'8' instanceof EvenNumberRange: false
```


# 247-Topshiriq: Obyekt xususiyatlarini massiv tartibida saralangan holda chiqarish

## Topshiriq sharti:
Obyekt maydonlarini alfavit tartibida saralab yangi tartiblangan obyekt hosil qiluvchi `sortObjectKeys` utilitasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function sortObjectKeys<T extends Record<string, any>>(obj: T): T {
  const sortedKeys = Object.keys(obj).sort();
  const result: any = {};

  sortedKeys.forEach((key) => {
    result[key] = obj[key];
  });

  return result;
}

const messy = { zebra: 1, apple: 2, orange: 3, banana: 4 };
const clean = sortObjectKeys(messy);

console.log("Saralangan obyekt kalitlari:", Object.keys(clean));
console.log("JSON ko'rinishi:\n" + JSON.stringify(clean));
```

## Tushuntirish va Mantiq:
1. Kriptografik imzo (HMAC) va API so'rovlarini xesh qilishda obyekt kalitlarining qat'iy alfavit tartibida bo'lishi shart (Deterministic JSON).
2. `Object.keys().sort()` orqali kalitlar tartiblanadi va yangi obyektga ketma-ket yoziladi.

## Ishlash natijasi:
```text
Saralangan obyekt kalitlari: [ 'apple', 'banana', 'orange', 'zebra' ]
JSON ko'rinishi:
{"apple":2,"banana":4,"orange":3,"zebra":1}
```


# 248-Topshiriq: Revocable Proxy: Bekor qilinishi mumkin bo'lgan vaqtinchalik kirish

## Topshiriq sharti:
`Proxy.revocable()` yordamida ma'lum vaqtdan so'ng bekor qilinadigan (ruxsat qaytarib olinadigan) xavfsiz obyekt havolasini yarating.

## Yechim (JS yoki TS kodi):
```typescript
function createTemporaryAccess(data: any) {
  // revoke funksiyasi bilan birga proxy qaytaradi
  const { proxy, revoke } = Proxy.revocable(data, {});

  return { proxy, revoke };
}

const secretDocument = { content: "Konfidentsial hisobot 2026" };
const { proxy, revoke } = createTemporaryAccess(secretDocument);

console.log("Ruxsat ochiq paytda:", proxy.content);

// Ruxsatni bekor qilamiz
revoke();

try {
  console.log("Ruxsat yopilgach:", proxy.content);
} catch (err: any) {
  console.log("Bekor qilingan Proxy xatosi:", err.name);
}
```

## Tushuntirish va Mantiq:
1. `Proxy.revocable()` oddiy proxydan farqli ravishda `{ proxy, revoke }` juftligini qaytaradi.
2. `revoke()` chaqirilishi bilan obyektdan barcha huquqlar olinadi va unga murojaat qilish `TypeError: Cannot perform 'get' on a proxy that has been revoked` beradi.
3. Xavfsizlik modullari va xotirani majburiy tozalashda juda muhimdir.

## Ishlash natijasi:
```text
Ruxsat ochiq paytda: Konfidentsial hisobot 2026
Bekor qilingan Proxy xatosi: TypeError
```


# 249-Topshiriq: Shartli Obyekt maydonlarini tozalash (Prune Nulls)

## Topshiriq sharti:
Obyektdagi barcha `null` va `undefined` qiymatli kalitlarni tozalab tashlovchi `pruneEmptyValues` utilitasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function pruneEmptyValues(obj: Record<string, any>): Record<string, any> {
  return Object.fromEntries(
    Object.entries(obj).filter(([_, value]) => value !== null && value !== undefined)
  );
}

const dirtyForm = {
  username: "shohruh",
  bio: "",
  website: null,
  avatarUrl: undefined,
  age: 26
};

const cleanForm = pruneEmptyValues(dirtyForm);
console.log("Tozalangan forma ma'lumotlari:", cleanForm);
```

## Tushuntirish va Mantiq:
1. `Object.entries()` va `filter()` kombinatsiyasi orqali qiymati `null` yoki `undefined` bo'lgan barcha juftliklar chiqarib tashlanadi.
2. `Object.fromEntries()` toza juftliklardan yangi ixcham obyekt yasaydi.
3. Backendga PATCH so'rovlari yuborishda faqat to'ldirilgan maydonlarni jo'natish uchun idealdir.

## Ishlash natijasi:
```text
Tozalangan forma ma'lumotlari: { username: 'shohruh', bio: '', age: 26 }
```


# 250-Topshiriq: Yakuniy Sintez: Validatsiyaga ega Immutable Entity sinfi

## Topshiriq sharti:
Ushbu bo'limdagi barcha obyekt tamoyillarini (Object.freeze, Descriptors, Getter/Setter, Private fields) birlashtirgan Bank Hisob raqami (BankAccount) Entity modelini yarating.

## Yechim (JS yoki TS kodi):
```typescript
class BankAccountEntity {
  readonly accountNumber: string;
  private _balance: number;
  private _history: string[] = [];

  constructor(accountNumber: string, initialDeposit: number) {
    if (initialDeposit < 0) {
      throw new Error("Boshlang'ich depozit manfiy bo'lishi mumkin emas");
    }
    this.accountNumber = accountNumber;
    this._balance = initialDeposit;
    this._history.push(`Hisob ochildi. Depozit: $${initialDeposit}`);
  }

  get balance(): number {
    return this._balance;
  }

  get history(): readonly string[] {
    // Tarix massivining o'zgarmas nusxasi qaytariladi
    return Object.freeze([...this._history]);
  }

  deposit(amount: number): void {
    if (amount <= 0) throw new Error("Miqdor 0 dan katta bo'lishi kerak");
    this._balance += amount;
    this._history.push(`Kirim: +$${amount} (Balans: $${this._balance})`);
  }

  withdraw(amount: number): void {
    if (amount <= 0) throw new Error("Miqdor 0 dan katta bo'lishi kerak");
    if (amount > this._balance) throw new Error("Mablag' yetarli emas");
    this._balance -= amount;
    this._history.push(`Chiqim: -$${amount} (Balans: $${this._balance})`);
  }
}

const myAccount = new BankAccountEntity("UZ9900112233", 500);
myAccount.deposit(200);
myAccount.withdraw(150);

console.log(`Hisob: ${myAccount.accountNumber}, Yakuniy balans: $${myAccount.balance}`);
console.log("Tranzaksiyalar tarixi:");
myAccount.history.forEach((h) => console.log("-", h));
```

## Tushuntirish va Mantiq:
1. BankAccountEntity klassi domen obyekti (Domain Entity) sifatida to'liq inkapsulyatsiya qilingan.
2. `accountNumber` o'zgarmas (`readonly`), `_balance` faqat `deposit` va `withdraw` metodlari orqali boshqariladi.
3. `history` getteri `Object.freeze` orqali qaytarilgani sababli, tashqi kod unga `push` qilib o'zgartira olmaydi.

## Ishlash natijasi:
```text
Hisob: UZ9900112233, Yakuniy balans: $550
Tranzaksiyalar tarixi:
- Hisob ochildi. Depozit: $500
- Kirim: +$200 (Balans: $700)
- Chiqim: -$150 (Balans: $550)
```

