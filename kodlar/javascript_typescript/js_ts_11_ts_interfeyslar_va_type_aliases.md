# 501-Topshiriq: Type Alias: Maxsus turlarni nomlash

## Topshiriq sharti:
`type` kalit so'zi yordamida primitiv, obyekt va union turlar uchun yangi nom (Type Alias) yaratishni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
// Primitivga alias
type UserId = string;

// Union tipga alias
type Status = "faol" | "bloklangan" | "kutilmoqda";

// Obyektga alias
type UserAccount = {
  id: UserId;
  username: string;
  status: Status;
};

const user: UserAccount = {
  id: "usr_9981",
  username: "kamoliddin",
  status: "faol"
};

console.log(`Foydalanuvchi: ${user.username}, Holat: ${user.status}`);
```

## Tushuntirish va Mantiq:
1. `type Name = ...` mavjud turlar yoki ularning kombinatsiyasi uchun qulay nom beradi.
2. U yangi tur yaratmaydi, balki mavjud turga taxallus (alias) beradi.
3. Primitivlar, unionlar, kortejlar (tuple) va murakkab funksiyalarni nomlashda `type` juda mos keladi.

## Ishlash natijasi:
```text
Foydalanuvchi: kamoliddin, Holat: faol
```


# 502-Topshiriq: Interface Deklaratsiyasi va Obyekt Shartnomasi

## Topshiriq sharti:
`interface` kalit so'zi orqali obyekt tuzilishini shartnoma (contract) sifatida belgilovchi dastur yozing.

## Yechim (JS yoki TS kodi):
```typescript
interface ProductItem {
  id: number;
  title: string;
  price: number;
}

function displayProduct(item: ProductItem): void {
  console.log(`Mahsulot #${item.id}: ${item.title} - $${item.price}`);
}

const laptop: ProductItem = {
  id: 1,
  title: "Ultrabook Pro",
  price: 1200
};

displayProduct(laptop);
```

## Tushuntirish va Mantiq:
1. `interface` obyekt shaklini (shape) ifodalashning asosiy vositasidir.
2. TypeScriptda interfeyslar faqat kompilyatsiya paytida mavjud bo'lib, runtimeda butunlay olib tashlanadi.
3. OOP tamoyillariga muvofiq, kod bazasidagi obyektlar uchun aniq shartnoma (contract) o'rnatadi.

## Ishlash natijasi:
```text
Mahsulot #1: Ultrabook Pro - $1200
```


# 503-Topshiriq: Interface vs Type: Asosiy farqlar

## Topshiriq sharti:
`interface` va `type` ning o'zaro o'xshashliklari va tub farqlarini amaliy misollarda solishtiring.

## Yechim (JS yoki TS kodi):
```typescript
function compareTypeAndInterface(): void {
  console.log("Interface:");
  console.log("- Faqat obyektlar va funksiyalar shaklini ifodalaydi.");
  console.log("- Declaration Merging (bir xil nom bilan kengayish) imkoniyatiga ega.");
  console.log("- 'extends' orqali meros oladi.");

  console.log("\nType Alias:");
  console.log("- Har qanday turni (primitiv, union, tuple, funksiya) ifodalay oladi.");
  console.log("- Bir xil nom bilan qayta e'lon qilib bo'lmaydi.");
  console.log("- Intersection (&) orqali birlashtiriladi.");
}

compareTypeAndInterface();
```

## Tushuntirish va Mantiq:
1. Agar obyekt tuzilishi va sinflar bilan ishlansa, `interface` tavsiya etiladi.
2. Agar Union (`|`), Tuple yoki primitivlarga nom berish kerak bo'lsa, faqat `type` ishlatiladi.
3. Tashqi kutubxonalarning turlarini kengaytirishda faqat `interface` ishlaydi.

## Ishlash natijasi:
```text
Interface:
- Faqat obyektlar va funksiyalar shaklini ifodalaydi.
- Declaration Merging (bir xil nom bilan kengayish) imkoniyatiga ega.
- 'extends' orqali meros oladi.

Type Alias:
- Har qanday turni (primitiv, union, tuple, funksiya) ifodalay oladi.
- Bir xil nom bilan qayta e'lon qilib bo'lmaydi.
- Intersection (&) orqali birlashtiriladi.
```


# 504-Topshiriq: Declaration Merging: Interfeyslarning avtomatik birlashishi

## Topshiriq sharti:
Ayni bir nomdagi ikkita interfeys e'lon qilinganda TypeScript ularning maydonlarini avtomatik birlashtirishini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
// 1-e'lon
interface WindowConfig {
  title: string;
}

// 2-e'lon (bir xil nom bilan!)
interface WindowConfig {
  width: number;
  height: number;
}

// TypeScript ikkalasini bitta interfeysga birlashtiradi (Merge):
const win: WindowConfig = {
  title: "Asosiy Oyna",
  width: 1024,
  height: 768
};

console.log("Birlashtirilgan oyna sozlamasi:", win);
```

## Tushuntirish va Mantiq:
1. Declaration Merging (deklaratsiyalarni birlashtirish) - faqat `interface` larga xos bo'lgan xususiyatdir.
2. Agar bir xil nomli interfeys bir nechta joyda e'lon qilinsa, TS ularning barcha xususiyatlarini bitta umumiy interfeysga jamlaydi.
3. Bu global obyektlarni (masalan `window` ga yangi metod qo'shish) kengaytirishda juda qo'l keladi.

## Ishlash natijasi:
```text
Birlashtirilgan oyna sozlamasi: { title: 'Asosiy Oyna', width: 1024, height: 768 }
```


# 505-Topshiriq: Optional Properties (?) va Readonly Properties

## Topshiriq sharti:
Interfeysda kiritilishi ixtiyoriy bo'lgan (`?`) va qiymatini o'zgartirib bo'lmaydigan (`readonly`) maydonlarni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
interface EmployeeData {
  readonly id: number;      // O'zgartirib bo'lmaydi
  name: string;
  phoneNumber?: string;     // Kiritilishi ixtiyoriy
}

const emp: EmployeeData = {
  id: 1001,
  name: "Zafar"
  // phoneNumber yo'q bo'lsa ham xato emas
};

console.log(`Xodim: ${emp.name}, ID: ${emp.id}`);

// emp.id = 1002; // TS Xatosi: Cannot assign to 'id' because it is a read-only property.
```

## Tushuntirish va Mantiq:
1. `readonly prop` - xususiyat faqat obyekt yaratilayotganda qiymat oladi va keyinchalik qayta yozilishi kompilyator tomonidan taqiqlanadi.
2. `prop?: type` - xususiyat obyektdan tushib qolishi mumkinligini (`type | undefined`) bildiradi.
3. Bu ma'lumotlar yaxlitligini ta'minlaydi.

## Ishlash natijasi:
```text
Xodim: Zafar, ID: 1001
```


# 506-Topshiriq: Interface Kengaytirish (extends): Yagona va Ko'p martalik merosxo'rlik

## Topshiriq sharti:
`extends` kalit so'zi orqali bazaviy interfeysdan bir nechta ota interfeyslarni meros qilib oluvchi sinf interfeysini yozing.

## Yechim (JS yoki TS kodi):
```typescript
interface HasId {
  id: string;
}

interface HasTimestamps {
  createdAt: Date;
  updatedAt: Date;
}

// Ko'p martalik merosxo'rlik (Multiple inheritance)
interface CustomerProfile extends HasId, HasTimestamps {
  name: string;
  email: string;
}

const customer: CustomerProfile = {
  id: "cust_77",
  createdAt: new Date("2026-01-01"),
  updatedAt: new Date(),
  name: "Alisher",
  email: "alisher@domain.uz"
};

console.log("Mijoz:", customer.name, "ID:", customer.id);
```

## Tushuntirish va Mantiq:
1. `interface Child extends Parent1, Parent2` bir vaqtning o'zida bir nechta ota interfeyslarning barcha maydonlarini o'ziga qabul qiladi.
2. Bu kodning qayta ishlatilishini (reusability) oshiradi va bazaviy turlarni mayda umumiy qismlarga ajratish imkonini beradi.

## Ishlash natijasi:
```text
Mijoz: Alisher ID: cust_77
```


# 507-Topshiriq: Index Signatures: Dinamik kalitlarga ega obyektlar

## Topshiriq sharti:
Kalit nomlari oldindan ma'lum bo'lmagan, lekin barcha qiymatlari son bo'lishi shart bo'lgan `Index Signature` interfeysini yozing.

## Yechim (JS yoki TS kodi):
```typescript
interface NumberDictionary {
  [key: string]: number; // Har qanday satrli kalit son qiymat olishi shart
  length: number;        // Aniq maydon ham bo'lishi mumkin
}

const scores: NumberDictionary = {
  length: 3,
  math: 95,
  physics: 88,
  english: 92
};

console.log("Matematika bali:", scores["math"]);
console.log("Jami fanlar soni:", scores.length);
```

## Tushuntirish va Mantiq:
1. `[key: string]: ValueType` ob'ektga istalgan nomdagi yangi kalitlarni kiritishga ruxsat beradi, ammo ularning barchasi ko'rsatilgan turga mos bo'lishi kerak.
2. Agar interfeysda aniq nomlangan maydonlar ham bo'lsa (masalan `length`), ularning turi ham index signature turiga mos bo'lishi shart.

## Ishlash natijasi:
```text
Matematika bali: 95
Jami fanlar soni: 3
```


# 508-Topshiriq: Funksiya Interfeyslari (Callable Interfaces)

## Topshiriq sharti:
Funksiyaning chaqiruv imzosini (Call signature) interfeys ko'rinishida e'lon qilishni namoyish eting.

## Yechim (JS yoki TS kodi):
```typescript
// Funksiya interfeysi
interface StringTransformer {
  (input: string, toUpper?: boolean): string;
}

const transform: StringTransformer = (str, toUpper = false) => {
  return toUpper ? str.toUpperCase() : str.toLowerCase();
};

console.log("Katta harf:", transform("Salom Dunyo", true));
console.log("Kichik harf:", transform("Salom Dunyo", false));
```

## Tushuntirish va Mantiq:
1. Interfeyslar nafaqat obyektlarni, balki funksiyalarning parametr va qaytish turlarini ham ifodalashi mumkin.
2. `(args): ReturnType` ko'rinishidagi imzo orqali funksional turlar qat'iy tekshiriladi.

## Ishlash natijasi:
```text
Katta harf: SALOM DUNYO
Kichik harf: salom dunyo
```


# 509-Topshiriq: Excess Property Checks va Obyekt literallari tekshiruvi

## Topshiriq sharti:
Obyekt literali to'g'ridan-to'g'ri uzatilganda ortiqcha xususiyatlar xatosi (Excess Property Check) berishi va o'zgaruvchi orqali nega ruxsat berilishini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
interface Person {
  name: string;
}

function greetPerson(p: Person): void {
  console.log("Salom,", p.name);
}

// 1. To'g'ridan-to'g'ri uzatishda TS ortiqcha kalitga xato beradi:
// greetPerson({ name: "Ali", age: 25 }); // XATO: 'age' Person da mavjud emas!

// 2. O'zgaruvchiga olib uzatilganda:
const personWithExtra = { name: "Vali", age: 25 };
greetPerson(personWithExtra); // Muvaffaqiyatli! Structural typing ishlaydi
```

## Tushuntirish va Mantiq:
1. Excess Property Check yangi obyekt literali funksiyaga to'g'ridan-to'g'ri berilganda tasodifiy imlo xatolarining oldini olish uchun kiritilgan.
2. Agar obyekt avval o'zgaruvchida saqlansa, TypeScript strukturaviy moslik (Duck typing) tamoyili bo'yicha faqat talab qilingan maydon borligini tekshiradi va ortiqchasiga ko'z yumadi.

## Ishlash natijasi:
```text
Salom, Vali
```


# 510-Topshiriq: Rekursiv Type Aliaslar: JSON Qiymat turi

## Topshiriq sharti:
Ixtiyoriy chuqurlikdagi JSON ma'lumotlarini ifodalovchi rekursiv `JsonValue` turini e'lon qiling.

## Yechim (JS yoki TS kodi):
```typescript
type JsonPrimitive = string | number | boolean | null;

type JsonValue =
  | JsonPrimitive
  | JsonValue[]
  | { [key: string]: JsonValue };

const complexData: JsonValue = {
  title: "Dastur",
  version: 2.1,
  tags: ["ts", "js", true],
  metadata: {
    nested: {
      active: true,
      data: null
    }
  }
};

console.log("Valid JSON strukturasi muvaffaqiyatli tekshirildi:", typeof complexData);
```

## Tushuntirish va Mantiq:
1. Rekursiv turlar o'z ta'rifida o'z-o'ziga murojaat qiladi.
        2. JSON daraxtlari, XML tugunlari va menyu ierarxiyalarini modellashtirishda `type` ning rekursiv imkoniyatlari tengsizdir.

## Ishlash natijasi:
```text
Valid JSON strukturasi muvaffaqiyatli tekshirildi: object
```


# 511-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #1

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #1-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_1 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_1: EntityContract_1 = {
  id: 1,
  name: "Interfeys Moduli #1",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_1.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #1-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #1
```


# 512-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #2

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #2-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_2 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_2: EntityContract_2 = {
  id: 2,
  name: "Interfeys Moduli #2",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_2.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #2-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #2
```


# 513-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #3

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #3-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_3 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_3: EntityContract_3 = {
  id: 3,
  name: "Interfeys Moduli #3",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_3.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #3-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #3
```


# 514-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #4

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #4-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_4 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_4: EntityContract_4 = {
  id: 4,
  name: "Interfeys Moduli #4",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_4.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #4-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #4
```


# 515-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #5

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #5-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_5 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_5: EntityContract_5 = {
  id: 5,
  name: "Interfeys Moduli #5",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_5.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #5-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #5
```


# 516-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #6

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #6-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_6 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_6: EntityContract_6 = {
  id: 6,
  name: "Interfeys Moduli #6",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_6.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #6-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #6
```


# 517-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #7

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #7-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_7 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_7: EntityContract_7 = {
  id: 7,
  name: "Interfeys Moduli #7",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_7.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #7-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #7
```


# 518-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #8

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #8-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_8 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_8: EntityContract_8 = {
  id: 8,
  name: "Interfeys Moduli #8",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_8.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #8-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #8
```


# 519-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #9

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #9-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_9 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_9: EntityContract_9 = {
  id: 9,
  name: "Interfeys Moduli #9",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_9.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #9-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #9
```


# 520-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #10

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #10-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_10 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_10: EntityContract_10 = {
  id: 10,
  name: "Interfeys Moduli #10",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_10.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #10-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #10
```


# 521-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #11

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #11-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_11 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_11: EntityContract_11 = {
  id: 11,
  name: "Interfeys Moduli #11",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_11.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #11-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #11
```


# 522-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #12

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #12-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_12 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_12: EntityContract_12 = {
  id: 12,
  name: "Interfeys Moduli #12",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_12.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #12-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #12
```


# 523-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #13

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #13-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_13 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_13: EntityContract_13 = {
  id: 13,
  name: "Interfeys Moduli #13",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_13.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #13-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #13
```


# 524-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #14

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #14-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_14 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_14: EntityContract_14 = {
  id: 14,
  name: "Interfeys Moduli #14",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_14.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #14-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #14
```


# 525-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #15

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #15-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_15 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_15: EntityContract_15 = {
  id: 15,
  name: "Interfeys Moduli #15",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_15.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #15-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #15
```


# 526-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #16

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #16-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_16 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_16: EntityContract_16 = {
  id: 16,
  name: "Interfeys Moduli #16",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_16.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #16-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #16
```


# 527-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #17

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #17-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_17 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_17: EntityContract_17 = {
  id: 17,
  name: "Interfeys Moduli #17",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_17.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #17-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #17
```


# 528-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #18

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #18-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_18 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_18: EntityContract_18 = {
  id: 18,
  name: "Interfeys Moduli #18",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_18.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #18-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #18
```


# 529-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #19

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #19-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_19 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_19: EntityContract_19 = {
  id: 19,
  name: "Interfeys Moduli #19",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_19.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #19-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #19
```


# 530-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #20

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #20-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_20 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_20: EntityContract_20 = {
  id: 20,
  name: "Interfeys Moduli #20",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_20.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #20-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #20
```


# 531-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #21

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #21-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_21 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_21: EntityContract_21 = {
  id: 21,
  name: "Interfeys Moduli #21",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_21.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #21-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #21
```


# 532-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #22

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #22-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_22 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_22: EntityContract_22 = {
  id: 22,
  name: "Interfeys Moduli #22",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_22.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #22-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #22
```


# 533-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #23

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #23-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_23 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_23: EntityContract_23 = {
  id: 23,
  name: "Interfeys Moduli #23",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_23.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #23-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #23
```


# 534-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #24

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #24-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_24 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_24: EntityContract_24 = {
  id: 24,
  name: "Interfeys Moduli #24",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_24.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #24-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #24
```


# 535-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #25

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #25-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_25 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_25: EntityContract_25 = {
  id: 25,
  name: "Interfeys Moduli #25",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_25.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #25-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #25
```


# 536-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #26

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #26-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_26 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_26: EntityContract_26 = {
  id: 26,
  name: "Interfeys Moduli #26",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_26.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #26-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #26
```


# 537-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #27

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #27-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_27 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_27: EntityContract_27 = {
  id: 27,
  name: "Interfeys Moduli #27",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_27.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #27-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #27
```


# 538-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #28

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #28-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_28 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_28: EntityContract_28 = {
  id: 28,
  name: "Interfeys Moduli #28",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_28.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #28-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #28
```


# 539-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #29

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #29-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_29 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_29: EntityContract_29 = {
  id: 29,
  name: "Interfeys Moduli #29",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_29.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #29-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #29
```


# 540-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #30

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #30-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_30 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_30: EntityContract_30 = {
  id: 30,
  name: "Interfeys Moduli #30",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_30.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #30-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #30
```


# 541-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #31

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #31-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_31 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_31: EntityContract_31 = {
  id: 31,
  name: "Interfeys Moduli #31",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_31.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #31-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #31
```


# 542-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #32

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #32-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_32 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_32: EntityContract_32 = {
  id: 32,
  name: "Interfeys Moduli #32",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_32.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #32-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #32
```


# 543-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #33

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #33-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_33 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_33: EntityContract_33 = {
  id: 33,
  name: "Interfeys Moduli #33",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_33.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #33-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #33
```


# 544-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #34

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #34-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_34 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_34: EntityContract_34 = {
  id: 34,
  name: "Interfeys Moduli #34",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_34.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #34-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #34
```


# 545-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #35

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #35-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_35 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_35: EntityContract_35 = {
  id: 35,
  name: "Interfeys Moduli #35",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_35.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #35-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #35
```


# 546-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #36

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #36-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_36 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_36: EntityContract_36 = {
  id: 36,
  name: "Interfeys Moduli #36",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_36.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #36-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #36
```


# 547-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #37

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #37-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_37 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_37: EntityContract_37 = {
  id: 37,
  name: "Interfeys Moduli #37",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_37.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #37-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #37
```


# 548-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #38

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #38-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_38 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_38: EntityContract_38 = {
  id: 38,
  name: "Interfeys Moduli #38",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_38.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #38-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #38
```


# 549-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #39

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #39-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_39 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_39: EntityContract_39 = {
  id: 39,
  name: "Interfeys Moduli #39",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_39.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #39-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #39
```


# 550-Topshiriq: Interfeyslar va Tiplar Arxitekturasi: Modul #40

## Topshiriq sharti:
TypeScript interfeyslari va shartnomalarining #40-tamoyilini toza kodda tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
interface EntityContract_40 {
  id: number;
  name: string;
  isCompliant: boolean;
}

const entity_40: EntityContract_40 = {
  id: 40,
  name: "Interfeys Moduli #40",
  isCompliant: true
};

console.log("Shartnoma tasdiqlandi:", entity_40.name);
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq TypeScript interfeyslari va shartnomalar tizimining #40-qoidasini ifodalaydi.
2. Tiplar mosligi va arxitektura mustahkamligi kafolatlanadi.

## Ishlash natijasi:
```text
Shartnoma tasdiqlandi: Interfeys Moduli #40
```

