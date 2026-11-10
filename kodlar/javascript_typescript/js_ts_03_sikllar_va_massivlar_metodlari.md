# 101-Topshiriq: Klassik for sikli: Initsializatsiya, shart va inkrement

## Topshiriq sharti:
Klassik `for` sikli yordamida 1 dan N gacha bo'lgan juft sonlarning kvadratlari yig'indisini hisoblovchi funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
function sumEvenSquares(n: number): number {
  let total = 0;
  for (let i = 2; i <= n; i += 2) {
    total += i * i;
  }
  return total;
}

const n = 10;
// 2^2 + 4^2 + 6^2 + 8^2 + 10^2 = 4 + 16 + 36 + 64 + 100 = 220
console.log(`1 dan ${n} gacha juft sonlar kvadratlari yig'indisi:`, sumEvenSquares(n));
```

## Tushuntirish va Mantiq:
1. Klassik `for (init; condition; step)` sikli eng yuqori hisoblash tezligiga ega.
2. Inkrement qadamini `i += 2` qilib belgilash orqali faqat juft sonlar bo'ylab harakatlaniladi va ortiqcha `if` tekshiruvlaridan saqlanadi.
3. Sikl o'zgaruvchisi `let i` blok sohasiga ega bo'lib, sikl tugashi bilan xotiradan bo'shaydi.

## Ishlash natijasi:
```text
1 dan 10 gacha juft sonlar kvadratlari yig'indisi: 220
```


# 102-Topshiriq: while sikli: Takrorlanishlar soni oldindan ma'lum bo'lmaganda

## Topshiriq sharti:
Berilgan sonni raqamlari teskari tartibda yozilgan yangi songa aylantiruvchi (masalan: 12345 -> 54321) funksiyani `while` sikli orqali yozing.

## Yechim (JS yoki TS kodi):
```typescript
function reverseNumber(num: number): number {
  let reversed = 0;
  let remaining = Math.abs(num);

  while (remaining > 0) {
    const lastDigit = remaining % 10;
    reversed = reversed * 10 + lastDigit;
    remaining = Math.floor(remaining / 10);
  }

  return num < 0 ? -reversed : reversed;
}

console.log("12345 teskarisi:", reverseNumber(12345));
console.log("-9876 teskarisi:", reverseNumber(-9876));
```

## Tushuntirish va Mantiq:
1. `while (shart)` takrorlanishlar soni noma'lum bo'lgan, ammo ma'lum bir mantiqiy to'xtash sharti mavjud bo'lgan jarayonlar uchun eng mos keladi.
2. `% 10` sonning oxirgi raqamini ajratib oladi, `Math.floor(x / 10)` esa oxirgi raqamni o'chiradi.
3. Sikl har bir qadamda o'zgaruvchini to'xtash shartiga yaqinlashtirib borishi shart, aks holda abadiy sikl (infinite loop) yuzaga keladi.

## Ishlash natijasi:
```text
12345 teskarisi: 54321
-9876 teskarisi: -6789
```


# 103-Topshiriq: do...while sikli: Kamida bir marta bajarilish kafolati

## Topshiriq sharti:
`do...while` siklidan foydalanib foydalanuvchining PIN kodini tekshiruvchi simulyatsiya qiling (kamida 1 marta tekshirilsin).

## Yechim (JS yoki TS kodi):
```typescript
function simulatePinEntry(correctPin: string, attempts: string[]): void {
  let attemptIndex = 0;
  let isGranted = false;
  let pin: string;

  do {
    pin = attempts[attemptIndex];
    console.log(`PIN kiritildi: ${pin}`);
    if (pin === correctPin) {
      isGranted = true;
      break;
    }
    attemptIndex++;
  } while (attemptIndex < attempts.length);

  console.log("Ruxsat holati:", isGranted ? "Muvaffaqiyatli kirildi" : "Bloklandi");
}

simulatePinEntry("7788", ["1111", "2222", "7788"]);
```

## Tushuntirish va Mantiq:
1. `do...while` siklida shart blok tanasi bajarilgandan so'ng tekshiriladi (`post-condition loop`).
2. Shu sababli sikl tanasi shart boshidanoq yolg'on bo'lgan taqdirda ham kamida bir marta albatta ishlaydi.
3. Foydalanuvchidan ma'lumot so'rash, o'yinlarda navbatni boshlash kabi jarayonlarda qulay.

## Ishlash natijasi:
```text
PIN kiritildi: 1111
PIN kiritildi: 2222
PIN kiritildi: 7788
Ruxsat holati: Muvaffaqiyatli kirildi
```


# 104-Topshiriq: break va continue: Sikl oqimini aniq boshqarish

## Topshiriq sharti:
1 dan 20 gacha bo'lgan sonlar ichidan 3 ga karrali sonlarni tashlab o'tuvchi (`continue`) va yig'indi 50 dan oshganda siklni to'xtatuvchi (`break`) dastur yozing.

## Yechim (JS yoki TS kodi):
```typescript
function testBreakAndContinue(): void {
  let sum = 0;
  console.log("Sikl boshlandi:");

  for (let i = 1; i <= 20; i++) {
    if (i % 3 === 0) {
      // 3 ga karrali sonlarni hisobga olmaymiz
      continue;
    }

    sum += i;
    console.log(`Qo'shildi: ${i}, Joriy yig'indi: ${sum}`);

    if (sum >= 50) {
      console.log(`Chegara yetdi (${sum} >= 50), sikl to'xtatildi.`);
      break;
    }
  }

  console.log("Yakuniy yig'indi:", sum);
}

testBreakAndContinue();
```

## Tushuntirish va Mantiq:
1. `continue` joriy iteratsiyani shu joyda yakunlaydi va siklning keyingi qadamiga o'tadi.
2. `break` esa butun siklni zudlik bilan to'xtatadi va boshqaruvni sikldan keyingi qatorga o'tkazadi.
3. Ular yordamida keraksiz amallarni chetlab o'tish va ortiqcha hisob-kitoblarni oldini olish mumkin.

## Ishlash natijasi:
```text
Sikl boshlandi:
Qo'shildi: 1, Joriy yig'indi: 1
Qo'shildi: 2, Joriy yig'indi: 3
Qo'shildi: 4, Joriy yig'indi: 7
Qo'shildi: 5, Joriy yig'indi: 12
Qo'shildi: 7, Joriy yig'indi: 19
Qo'shildi: 8, Joriy yig'indi: 27
Qo'shildi: 10, Joriy yig'indi: 37
Qo'shildi: 11, Joriy yig'indi: 48
Qo'shildi: 13, Joriy yig'indi: 61
Chegara yetdi (61 >= 50), sikl to'xtatildi.
Yakuniy yig'indi: 61
```


# 105-Topshiriq: Labeled Statements: Ichma-ich sikllarni tashqaridan boshqarish

## Topshiriq sharti:
Ikki o'lchovli matritsadan berilgan elementni qidirishda, element topilgach tashqi sikl bilan birga butun qidiruvni yorliq (label) orqali to'xtatuvchi kod yozing.

## Yechim (JS yoki TS kodi):
```typescript
function searchMatrix(matrix: number[][], target: number): [number, number] | null {
  let foundPosition: [number, number] | null = null;

  // Tashqi sikl uchun yorliq (label) e'lon qilinadi
  outerLoop: for (let r = 0; r < matrix.length; r++) {
    for (let c = 0; c < matrix[r].length; c++) {
      if (matrix[r][c] === target) {
        foundPosition = [r, c];
        console.log(`Topildi: ${target} [qator: ${r}, ustun: ${c}]`);
        break outerLoop; // To'g'ridan-to'g'ri tashqi sikldan chiqib ketamiz!
      }
    }
  }

  return foundPosition;
}

const grid = [
  [10, 20, 30],
  [40, 50, 60],
  [70, 80, 90]
];

searchMatrix(grid, 50);
```

## Tushuntirish va Mantiq:
1. Standart `break` faqat o'zi joylashgan ichki siklni to'xtatadi.
2. Yoriqlar (`labelName: for (...)`) orqali har qanday kiritilgan siklni bevosita tashqi darajasidan to'xtatish (`break labelName`) yoki keyingi iteratsiyasiga o'tish (`continue labelName`) mumkin.
3. Matritsalar, graf va daraxt algoritmlarida bayroqli o'zgaruvchilarsiz (boolean flag) toza yechim beradi.

## Ishlash natijasi:
```text
Topildi: 50 [qator: 1, ustun: 1]
```


# 106-Topshiriq: for...of sikli: Iterable tuzilmalar bo'ylab qulay iteratsiya

## Topshiriq sharti:
`for...of` siklidan foydalanib massiv, satr va `Map` to'plamlari bo'ylab elementlarni qiymati bo'yicha aylanib chiquvchi dastur yozing.

## Yechim (JS yoki TS kodi):
```typescript
function testForOf(): void {
  // Massiv
  const cities = ["Toshkent", "Buxoro", "Samarqand"];
  console.log("--- Shaharlar ---");
  for (const city of cities) {
    console.log("Shahar:", city);
  }

  // Satr
  console.log("\n--- Harflar ---");
  for (const char of "Salom") {
    console.log("Harf:", char);
  }

  // Map to'plami
  console.log("\n--- Lug'at ---");
  const currencyMap = new Map<string, number>([
    ["USD", 12800],
    ["EUR", 13900]
  ]);
  for (const [curr, rate] of currencyMap) {
    console.log(`${curr} kursi: ${rate} UZS`);
  }
}

testForOf();
```

## Tushuntirish va Mantiq:
1. `for...of` ES6 da kiritilgan bo'lib, `Symbol.iterator` ga ega barcha iterable ma'lumotlar tuzilmalarini to'g'ridan-to'g'ri qiymatlari bo'yicha aylanadi.
2. Klassik indekslar bilan ishlash mashaqqatini yo'qotadi va `break`, `continue`, `return` buyruqlarini to'liq qo'llab-quvvatlaydi.
3. Massivlar, Map, Set, TypedArray va generatorlar bilan mukammal ishlaydi.

## Ishlash natijasi:
```text
--- Shaharlar ---
Shahar: Toshkent
Shahar: Buxoro
Shahar: Samarqand

--- Harflar ---
Harf: S
Harf: a
Harf: l
Harf: o
Harf: m

--- Lug'at ---
USD kursi: 12800 UZS
EUR kursi: 13900 UZS
```


# 107-Topshiriq: for...in sikli va Prototip zanjiridagi xususiyatlardan saqlanish

## Topshiriq sharti:
`for...in` siklida obyektning prototipidan meros bo'lib o'tgan xususiyatlar chiqib ketishini ko'rsating va `Object.hasOwn()` orqali faqat o'ziga tegishli kalitlarni filtrlang.

## Yechim (JS yoki TS kodi):
```typescript
function inspectObjectKeys(): void {
  const parent = { inheritedProp: "Meros qolgan qiymat" };
  const child = Object.create(parent);
  child.ownProp1 = "Shaxsiy qiymat 1";
  child.ownProp2 = "Shaxsiy qiymat 2";

  console.log("--- Barcha kalitlar (for...in): ---");
  for (const key in child) {
    console.log("Topilgan kalit:", key);
  }

  console.log("\n--- Faqat shaxsiy kalitlar (Object.hasOwn): ---");
  for (const key in child) {
    if (Object.hasOwn(child, key)) {
      console.log("Shaxsiy kalit:", key, "->", child[key]);
    }
  }
}

inspectObjectKeys();
```

## Tushuntirish va Mantiq:
1. `for...in` obyektning barcha sanaladigan (enumerable) xususiyatlarini, shu jumladan prototip zanjiridagi xususiyatlarni ham aylanadi.
2. Massivlar ustida `for...in` ishlatish xavflidir, chunki indekslar tartibi kafolatlanmaydi va satr (`'0'`, `'1'`) ko'rinishida olinadi.
3. Obyektning faqat o'ziga tegishli xususiyatlarini olish uchun ES2022 ning `Object.hasOwn(obj, key)` yoki `Object.keys(obj)` ishlatiladi.

## Ishlash natijasi:
```text
--- Barcha kalitlar (for...in): ---
Topilgan kalit: ownProp1
Topilgan kalit: ownProp2
Topilgan kalit: inheritedProp

--- Faqat shaxsiy kalitlar (Object.hasOwn): ---
Shaxsiy kalit: ownProp1 -> Shaxsiy qiymat 1
Shaxsiy kalit: ownProp2 -> Shaxsiy qiymat 2
```


# 108-Topshiriq: Massiv yaratish usullari: Literal [], new Array() va Array.of()

## Topshiriq sharti:
Massiv yaratishning uchta usulini solishtiring va `new Array(5)` ning nima uchun bitta element emas, balki 5 ta bo'sh katak yaratishini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function compareArrayCreation(): void {
  // 1. Array literal (eng tavsiya etiladigan)
  const a1 = [5];
  console.log("a1 ([5]):", a1, "uzunligi:", a1.length);

  // 2. new Array(5) - diqqat! 5 elementli bo'sh massiv yaratadi
  const a2 = new Array(5);
  console.log("a2 (new Array(5)):", a2, "uzunligi:", a2.length);

  // 3. Array.of(5) - doimo berilgan argumentlardan iborat massiv tuzadi
  const a3 = Array.of(5);
  console.log("a3 (Array.of(5)):", a3, "uzunligi:", a3.length);

  const a4 = Array.of(1, 2, 3);
  console.log("a4 (Array.of(1, 2, 3)):", a4);
}

compareArrayCreation();
```

## Tushuntirish va Mantiq:
1. `[]` (massiv literali) eng qulay, tezkor va xavfsiz massiv yaratish usulidir.
2. `new Array(n)` agar bitta raqam argument olsa, `n` uzunlikdagi siyrak (sparse, bo'sh katakli) massiv hosil qiladi. Bir nechta argument olsa (`new Array(1, 2)`), ulardan massiv tuzadi.
3. `Array.of()` esa argumentlar sonidan qat'iy nazar har doim uzatilgan qiymatlardan iborat massiv yaratadi.

## Ishlash natijasi:
```text
a1 ([5]): [ 5 ] uzunligi: 1
a2 (new Array(5)): [ <5 empty items> ] uzunligi: 5
a3 (Array.of(5)): [ 5 ] uzunligi: 1
a4 (Array.of(1, 2, 3)): [ 1, 2, 3 ]
```


# 109-Topshiriq: Array.from(): Massivsimon obyektlar va mapping funksiyasi

## Topshiriq sharti:
`Array.from()` orqali 1 dan N gacha bo'lgan sonlar massivini bitta qatorda generatsiya qilishni va ikkinchi mapFn argumentini qo'llashni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function generateRange(start: number, end: number, step: number = 1): number[] {
  const length = Math.floor((end - start) / step) + 1;
  return Array.from({ length }, (_, index) => start + index * step);
}

function testArrayFrom(): void {
  // 1 dan 5 gacha sonlar
  const r1 = generateRange(1, 5);
  console.log("1 dan 5 gacha:", r1);

  // 10 dan 50 gacha 10 qadam bilan
  const r2 = generateRange(10, 50, 10);
  console.log("10 dan 50 gacha (step 10):", r2);

  // Set to'plamidan massiv yaratish
  const uniqueSet = new Set(["olma", "nok", "olma"]);
  const fromSet = Array.from(uniqueSet);
  console.log("Set dan olingan massiv:", fromSet);
}

testArrayFrom();
```

## Tushuntirish va Mantiq:
1. `Array.from(arrayLike, mapFn)` massivsimon (masalan, `{ length: 5 }`, NodeList, `arguments`) yoki iterable tuzilmalarni haqiqiy massivga aylantiradi.
2. Ikkinchi argument sifatida `mapFn` qabul qiladi, bu esa oraliq massiv yaratmasdan to'g'ridan-to'g'ri o'zgartirish kiritish imkonini beradi.
3. Raqamli oraliqlar (ranges) yaratishda eng nafis funksional usuldir.

## Ishlash natijasi:
```text
1 dan 5 gacha: [ 1, 2, 3, 4, 5 ]
10 dan 50 gacha (step 10): [ 10, 20, 30, 40, 50 ]
Set dan olingan massiv: [ 'olma', 'nok' ]
```


# 110-Topshiriq: Stack (LIFO) amallari: Array.prototype.push va pop

## Topshiriq sharti:
Massiv yordamida Stack (oxirgi kirgan - birinchi chiqadi) ma'lumot tuzilmasi sinfini (`push`, `pop`, `peek`, `isEmpty`) yarating.

## Yechim (JS yoki TS kodi):
```typescript
class Stack<T> {
  private items: T[] = [];

  push(element: T): void {
    this.items.push(element);
  }

  pop(): T | undefined {
    return this.items.pop();
  }

  peek(): T | undefined {
    return this.items[this.items.length - 1];
  }

  isEmpty(): boolean {
    return this.items.length === 0;
  }

  size(): number {
    return this.items.length;
  }
}

const historyStack = new Stack<string>();
historyStack.push("sahifa_1");
historyStack.push("sahifa_2");
historyStack.push("sahifa_3");

console.log("Tepada turgan sahifa:", historyStack.peek());
console.log("Orqaga qaytildi (pop):", historyStack.pop());
console.log("Hozirgi faol sahifa:", historyStack.peek());
console.log("Stack hajmi:", historyStack.size());
```

## Tushuntirish va Mantiq:
1. `push()` massiv oxiriga element qo'shadi va unumdorligi `O(1)` amortizatsiyalangan vaqtga ega.
2. `pop()` massivning eng oxirgi elementini olib tashlaydi va qaytaradi (`O(1)`).
3. Stack LIFO (Last In First Out) prinsipi bo'yicha ishlaydi va brauzer tarixi (Back tugmasi), undo/redo tizimlarining asosidir.

## Ishlash natijasi:
```text
Tepada turgan sahifa: sahifa_3
Orqaga qaytildi (pop): sahifa_3
Hozirgi faol sahifa: sahifa_2
Stack hajmi: 2
```


# 111-Topshiriq: Queue (FIFO) amallari: unshift va shift hamda unumdorlik tahlili

## Topshiriq sharti:
Massiv boshiga element qo'shish (`unshift`) va boshidan olish (`shift`) amallari nima uchun `O(N)` vaqt olishini ko'rsatib bering.

## Yechim (JS yoki TS kodi):
```typescript
function demonstrateQueue(): void {
  const queue: string[] = [];

  // Navbatga qo'shish (oxiriga)
  queue.push("Mijoz 1");
  queue.push("Mijoz 2");
  queue.push("Mijoz 3");
  console.log("Boshlang'ich navbat:", queue);

  // Navbatdan chiqarish (boshidan - shift)
  const served = queue.shift();
  console.log("Xizmat ko'rsatildi:", served);
  console.log("Qolgan navbat:", queue);

  // Boshiga yangi element qo'shish (unshift)
  queue.unshift("Shoshilinch VIP mijoz");
  console.log("VIP qo'shilgach navbat:", queue);
}

demonstrateQueue();
```

## Tushuntirish va Mantiq:
1. `shift()` va `unshift()` massivning boshidagi indekslar bilan ishlaydi.
2. 0-indeks o'chirilganda yoki qo'shilganda massivdagi qolgan barcha keyingi elementlar xotirada bitta pozitsiyaga siljishi (re-indexing) kerak bo'ladi.
3. Shu sababli bu amallarning murakkabligi `O(N)` dir. Katta hajmdagi navbatlar (Queue) uchun bog'langan ro'yxatlar (LinkedList) yoki Circular Buffer ishlatish tavsiya etiladi.

## Ishlash natijasi:
```text
Boshlang'ich navbat: [ 'Mijoz 1', 'Mijoz 2', 'Mijoz 3' ]
Xizmat ko'rsatildi: Mijoz 1
Qolgan navbat: [ 'Mijoz 2', 'Mijoz 3' ]
VIP qo'shilgach navbat: [ 'Shoshilinch VIP mijoz', 'Mijoz 2', 'Mijoz 3' ]
```


# 112-Topshiriq: Array.prototype.map(): Transformatsiya va Immutability

## Topshiriq sharti:
Mahsulotlar massividagi narxlarni soliq (12%) bilan qayta hisoblab, yangi o'zgarmas massiv qaytaruvchi toza funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
interface Product {
  id: number;
  name: string;
  price: number;
}

function applyTax(products: Product[], taxRate: number = 0.12) {
  // Asl massiv va obyektlarni o'zgartirmay (immutability) yangi massiv qaytaramiz
  return products.map((item) => ({
    ...item,
    priceWithTax: Math.round(item.price * (1 + taxRate))
  }));
}

const originalProducts: Product[] = [
  { id: 1, name: "Noutbuk", price: 8000000 },
  { id: 2, name: "Smartfon", price: 3500000 }
];

const taxedProducts = applyTax(originalProducts);

console.log("Asl mahsulotlar (o'zgarmagan):", originalProducts[0].price);
console.log("Soliqli mahsulotlar:", taxedProducts[0].priceWithTax);
```

## Tushuntirish va Mantiq:
1. `map()` funksiyasi asl massivni o'zgartirmaydi (pure function) va har doim bir xil uzunlikdagi yangi massiv qaytaradi.
        2. Har bir element uchun berilgan callback funksiya bajariladi.
        3. Obyektlar massivini o'zgartirganda spread `{ ...item }` orqali yangi obyekt nusxasini yaratish juda muhim, aks holda asl obyektlar o'zgarib ketishi (mutation) mumkin.

## Ishlash natijasi:
```text
Asl mahsulotlar (o'zgarmagan): 8000000
Soliqli mahsulotlar: 8960000
```


# 113-Topshiriq: Array.prototype.filter(): Shart bo'yicha saralash

## Topshiriq sharti:
Foydalanuvchilar ro'yxatidan faqat faol va yoshi 18 dan katta bo'lganlarni saralab oluvchi funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
interface User {
  id: number;
  name: string;
  age: number;
  isActive: boolean;
}

function filterEligibleUsers(users: User[]): User[] {
  return users.filter((u) => u.isActive && u.age >= 18);
}

const userList: User[] = [
  { id: 1, name: "Olim", age: 22, isActive: true },
  { id: 2, name: "Zuhra", age: 16, isActive: true },
  { id: 3, name: "Rustam", age: 30, isActive: false },
  { id: 4, name: "Nodira", age: 19, isActive: true }
];

const eligible = filterEligibleUsers(userList);
console.log("Mos foydalanuvchilar:", eligible.map((u) => u.name));
```

## Tushuntirish va Mantiq:
1. `filter()` massivning har bir elementini ko'rib chiqadi va callback `true` qaytargan elementlardangina iborat yangi massiv hosil qiladi.
2. Agar birorta element mos kelmasa, xato bermaydi, balki bo'sh massiv `[]` qaytaradi.
3. Asl massivga hech qanday ta'sir o'tkazmaydi.

## Ishlash natijasi:
```text
Mos foydalanuvchilar: [ 'Olim', 'Nodira' ]
```


# 114-Topshiriq: Array.prototype.reduce(): Massivni yagona qiymatga yig'ish

## Topshiriq sharti:
Savatchadagi mahsulotlarning narxlari va miqdorini hisobga olib jami xarid summasini `reduce` orqali hisoblang.

## Yechim (JS yoki TS kodi):
```typescript
interface CartItem {
  title: string;
  price: number;
  quantity: number;
}

function calculateGrandTotal(cart: CartItem[]): number {
  return cart.reduce((accumulator, item) => {
    return accumulator + item.price * item.quantity;
  }, 0); // Boshlang'ich qiymat: 0
}

const myCart: CartItem[] = [
  { title: "Kitob", price: 45000, quantity: 2 },
  { title: "Daftar", price: 5000, quantity: 10 },
  { title: "Ruchka", price: 3000, quantity: 5 }
];

console.log("Savatchaning jami summasi:", calculateGrandTotal(myCart), "so'm");
```

## Tushuntirish va Mantiq:
1. `reduce(callback, initialValue)` JavaScriptdagi eng qudratli massiv metodidir.
2. Callback 4 ta parametr oladi: `accumulator` (yig'uvchi), `currentValue` (joriy element), `currentIndex`, `array`.
3. Doimo `initialValue` berish shart (masalan `0`), aks holda bo'sh massivda `reduce` chaqirilsa `TypeError: Reduce of empty array with no initial value` yuzaga keladi.

## Ishlash natijasi:
```text
Savatchaning jami summasi: 155000 so'm
```


# 115-Topshiriq: reduce orqali elementlarni toifalar bo'yicha guruhlash (Grouping)

## Topshiriq sharti:
`reduce` metodi orqali xodimlar ro'yxatini ularning bo'limi (department) bo'yicha guruhlovchi funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
interface Employee {
  name: string;
  department: string;
  salary: number;
}

function groupByDepartment(employees: Employee[]): Record<string, Employee[]> {
  return employees.reduce((acc, emp) => {
    const dept = emp.department;
    if (!acc[dept]) {
      acc[dept] = [];
    }
    acc[dept].push(emp);
    return acc;
  }, {} as Record<string, Employee[]>);
}

const staff: Employee[] = [
  { name: "Sardor", department: "IT", salary: 2000 },
  { name: "Malika", department: "Marketing", salary: 1500 },
  { name: "Jasur", department: "IT", salary: 2500 },
  { name: "Nilufar", department: "HR", salary: 1400 }
];

const grouped = groupByDepartment(staff);
console.log("IT bo'limi xodimlari:", grouped["IT"].map((e) => e.name));
console.log("Barcha bo'limlar:", Object.keys(grouped));
```

## Tushuntirish va Mantiq:
1. `reduce` nafaqat sonlarni yig'ish, balki massivni obyektga, Map ga yoki boshqa ixtiyoriy tuzilmaga o'girish imkonini beradi.
2. Boshlang'ich qiymat sifatida bo'sh obyekt `{}` beriladi va har bir iteratsiyada mos kalit bo'yicha massiv to'ldirib boriladi.
3. Bu backendda SQL dagi `GROUP BY` amalining mijoz yoki Node.js tomonidagi mukammal analogidir.

## Ishlash natijasi:
```text
IT bo'limi xodimlari: [ 'Sardor', 'Jasur' ]
Barcha bo'limlar: [ 'IT', 'Marketing', 'HR' ]
```


# 116-Topshiriq: Array.prototype.reduceRight(): O'ngdan chapga funksiyalar kompozitsiyasi

## Topshiriq sharti:
`reduceRight` yordamida funksiyalarni o'ngdan chapga qarab zanjirli bajaruvchi `compose` funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
type MathFunc = (x: number) => number;

function compose(...funcs: MathFunc[]): MathFunc {
  return (initialValue: number) =>
    funcs.reduceRight((acc, fn) => fn(acc), initialValue);
}

const addFive: MathFunc = (x) => x + 5;
const double: MathFunc = (x) => x * 2;
const square: MathFunc = (x) => x * x;

// compose(square, double, addFive)(3):
// 1-qadam: addFive(3) = 8
// 2-qadam: double(8) = 16
// 3-qadam: square(16) = 256
const pipeline = compose(square, double, addFive);
console.log("Kompozitsiya natijasi:", pipeline(3));
```

## Tushuntirish va Mantiq:
1. `reduceRight()` xuddi `reduce` kabi ishlaydi, faqat massiv oxiridan boshiga qarab (o'ngdan chapga) harakatlanadi.
2. Funksional dasturlashda `compose(f, g, h)(x) === f(g(h(x)))` formulasini amalga oshirishda asosiy vosita hisoblanadi.
3. Agar chapdan o'ngga tartib kerak bo'lsa, `pipe` funksiyasi va oddiy `reduce` ishlatiladi.

## Ishlash natijasi:
```text
Kompozitsiya natijasi: 256
```


# 117-Topshiriq: Array.prototype.find() va findIndex(): Qidiruv mexanizmi

## Topshiriq sharti:
ID bo'yicha foydalanuvchini va uning massivdagi indeksini topuvchi funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
interface UserItem {
  id: number;
  login: string;
}

const db: UserItem[] = [
  { id: 101, login: "coder_uz" },
  { id: 102, login: "dev_pro" },
  { id: 103, login: "ninja_ts" }
];

function findUserById(id: number) {
  const user = db.find((u) => u.id === id);
  const index = db.findIndex((u) => u.id === id);

  return { user, index };
}

console.log("ID 102 qidiruvi:", findUserById(102));
console.log("ID 999 qidiruvi:", findUserById(999));
```

## Tushuntirish va Mantiq:
1. `find()` shartni qanoatlantirgan birinchi elementning o'zini qaytaradi, topa olmasa `undefined` beradi.
2. `findIndex()` esa o'sha elementning indeksini qaytaradi, topa olmasa `-1` beradi.
3. Ikkala metod ham elementni topishi bilanoq siklni to'xtatadi (short-circuit), butun massivni behuda aylanmaydi.

## Ishlash natijasi:
```text
ID 102 qidiruvi: { user: { id: 102, login: 'dev_pro' }, index: 1 }
ID 999 qidiruvi: { user: undefined, index: -1 }
```


# 118-Topshiriq: findLast() va findLastIndex() (ES2023): Oxiridan qidirish

## Topshiriq sharti:
ES2023 da kiritilgan `findLast` va `findLastIndex` orqali tranzaksiyalar ro'yxatidan eng so'nggi chiqim amaliyotini toping.

## Yechim (JS yoki TS kodi):
```typescript
interface Transaction {
  id: number;
  type: "income" | "expense";
  amount: number;
}

const transactions: Transaction[] = [
  { id: 1, type: "income", amount: 1000 },
  { id: 2, type: "expense", amount: 200 },
  { id: 3, type: "income", amount: 500 },
  { id: 4, type: "expense", amount: 150 }, // Eng oxirgi chiqim
  { id: 5, type: "income", amount: 300 }
];

// @ts-ignore
const lastExpense = transactions.findLast((t) => t.type === "expense");
// @ts-ignore
const lastExpenseIndex = transactions.findLastIndex((t) => t.type === "expense");

console.log("Eng oxirgi chiqim:", lastExpense);
console.log("Uning indeksi:", lastExpenseIndex);
```

## Tushuntirish va Mantiq:
1. ES2023 gacha massiv oxiridan qidirish uchun massivni `reverse()` qilish kerak edi, bu esa asl massivni buzgan yoki ortiqcha xotira olgan.
2. `findLast` va `findLastIndex` massivni o'zgartirmasdan to'g'ridan-to'g'ri oxiridan boshlab tekshiradi va birinchi uchragan moslikda to'xtaydi.
3. Loglar va vaqt bo'yicha tartiblangan hodisalarni tahlil qilishda juda qulay.

## Ishlash natijasi:
```text
Eng oxirgi chiqim: { id: 4, type: 'expense', amount: 150 }
Uning indeksi: 3
```


# 119-Topshiriq: Array.prototype.some(): Kamida bitta moslikni tekshirish

## Topshiriq sharti:
Foydalanuvchilar orasida kamida bitta admin huquqiga ega shaxs borligini `some` orqali tekshiruvchi funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
function hasAdmin(roles: string[]): boolean {
  return roles.some((r) => r === "admin" || r === "superadmin");
}

console.log("['user', 'editor', 'admin']:", hasAdmin(["user", "editor", "admin"]));
console.log("['user', 'guest']:", hasAdmin(["user", "guest"]));
console.log("[] (bo'sh massiv):", hasAdmin([]));
```

## Tushuntirish va Mantiq:
1. `some()` agar massivda kamida bitta element callback shartiga mos kelsa `true`, aks holda `false` qaytaradi.
2. Birinchi `true` natijasini topishi bilanoq tekshirishni to'xtatadi.
3. Bo'sh massiv uchun har doim `false` qaytaradi.

## Ishlash natijasi:
```text
['user', 'editor', 'admin']: true
['user', 'guest']: false
[] (bo'sh massiv): false
```


# 120-Topshiriq: Array.prototype.every(): Barcha elementlarning mosligini tekshirish

## Topshiriq sharti:
Barcha kiritilgan baholarning o'tish chegarasidan (60 ball) yuqoriligini `every` yordamida tekshiring.

## Yechim (JS yoki TS kodi):
```typescript
function isClassPassing(scores: number[], passingThreshold: number = 60): boolean {
  return scores.every((sc) => sc >= passingThreshold);
}

console.log("[65, 80, 92, 74]:", isClassPassing([65, 80, 92, 74]));
console.log("[70, 58, 90]:", isClassPassing([70, 58, 90]));
console.log("[] (bo'sh massiv):", isClassPassing([]));
```

## Tushuntirish va Mantiq:
1. `every()` faqat va faqat barcha elementlar shartga mos kelgandagina `true` qaytaradi.
2. Agar bitta element ham mos kelmasa, darhol `false` qaytaradi va to'xtaydi.
3. Bo'sh massiv uchun `every` har doim `true` qaytaradi (Vacuous truth matematik qoidasi).

## Ishlash natijasi:
```text
[65, 80, 92, 74]: true
[70, 58, 90]: false
[] (bo'sh massiv): true
```


# 121-Topshiriq: Array.prototype.includes(): Primitivlar va NaN ni topish

## Topshiriq sharti:
`includes()` va `indexOf()` ning `NaN` qiymatini qidirishdagi farqini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function testIncludes(): void {
  const list = [10, NaN, 30, "salom"];

  console.log("list.includes(NaN):", list.includes(NaN)); // true!
  console.log("list.indexOf(NaN):", list.indexOf(NaN));   // -1! (chunki === bilan topolmaydi)

  console.log("list.includes(30, 2):", list.includes(30, 2)); // 2-indeksdan boshlab qidiradi
  console.log("list.includes(30, 3):", list.includes(30, 3));
}

testIncludes();
```

## Tushuntirish va Mantiq:
1. `includes()` ES2016 da qo'shilgan bo'lib, `SameValueZero` taqqoslash algoritmidan foydalanadi.
2. Bu algoritm `NaN` ni o'ziga teng deb biladi, natijada `includes(NaN) === true` bo'ladi.
3. `indexOf()` esa qat'iy tenglikka (`===`) asoslangani sababli `NaN` ni hech qachon topa olmaydi.

## Ishlash natijasi:
```text
list.includes(NaN): true
list.indexOf(NaN): -1
list.includes(30, 2): true
list.includes(30, 3): false
```


# 122-Topshiriq: Array.prototype.indexOf() va lastIndexOf(): Indekslarni aniqlash

## Topshiriq sharti:
Massivda bir necha marta takrorlangan elementning birinchi va oxirgi uchrash joyini aniqlang.

## Yechim (JS yoki TS kodi):
```typescript
function findOccurrences(): void {
  const letters = ["a", "b", "c", "d", "b", "e", "b"];

  console.log("'b' birinchi uchrashi:", letters.indexOf("b"));
  console.log("'b' oxirgi uchrashi:", letters.lastIndexOf("b"));
  console.log("'z' qidiruvi:", letters.indexOf("z"));
}

findOccurrences();
```

## Tushuntirish va Mantiq:
1. `indexOf(elem, fromIndex)` chapdan boshlab element indeksini qidiradi.
2. `lastIndexOf(elem, fromIndex)` esa o'ngdan (oxiridan) boshlab qidiradi.
3. Element topilmasa ikkalasi ham `-1` qaytaradi.

## Ishlash natijasi:
```text
'b' birinchi uchrashi: 1
'b' oxirgi uchrashi: 6
'z' qidiruvi: -1
```


# 123-Topshiriq: Array.prototype.slice(): Xavfsiz kesib olish (Shallow Copy)

## Topshiriq sharti:
`slice` metodi yordamida sahifalash (pagination) funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function paginate<T>(items: T[], page: number, pageSize: number): T[] {
  const startIndex = (page - 1) * pageSize;
  const endIndex = startIndex + pageSize;
  return items.slice(startIndex, endIndex);
}

const allData = ["A", "B", "C", "D", "E", "F", "G", "H"];

console.log("1-sahifa (3 tadan):", paginate(allData, 1, 3));
console.log("2-sahifa (3 tadan):", paginate(allData, 2, 3));
console.log("3-sahifa (3 tadan):", paginate(allData, 3, 3));
```

## Tushuntirish va Mantiq:
1. `slice(start, end)` asl massivni o'zgartirmasdan uning belgilangan oraliqdagi sayoz nusxasini (shallow copy) qaytaradi.
2. `end` indeksi oraliqqa kirmaydi (`[start, end)`).
3. Pagination mantiqida `(page - 1) * pageSize` formulasini qo'llash eng qulay usuldir.

## Ishlash natijasi:
```text
1-sahifa (3 tadan): [ 'A', 'B', 'C' ]
2-sahifa (3 tadan): [ 'D', 'E', 'F' ]
3-sahifa (3 tadan): [ 'G', 'H' ]
```


# 124-Topshiriq: Array.prototype.splice(): Mutatsion tahrirlash

## Topshiriq sharti:
`splice` yordamida massivning o'rtasidan elementlarni o'chirish, yangilarini qo'shish va almashtirish amallarini namoyish eting.

## Yechim (JS yoki TS kodi):
```typescript
function testSplice(): void {
  const months = ["Yanvar", "Fevral", "Aprel", "May"];

  // 'Mart' tushib qolgan: 2-indeksga 0 ta o'chirib 'Mart' qo'shamiz
  months.splice(2, 0, "Mart");
  console.log("Mart qo'shilgach:", months);

  // 1-indeksdan boshlab 1 ta elementni o'chiramiz
  const removed = months.splice(1, 1);
  console.log("O'chirib olingan:", removed);
  console.log("Qolgan oylar:", months);

  // Almashtirish: 0-indeksdagi element o'rniga boshqasini qo'yish
  months.splice(0, 1, "Dekabr");
  console.log("Almashtirilgach:", months);
}

testSplice();
```

## Tushuntirish va Mantiq:
1. `splice(start, deleteCount, ...items)` massivni to'g'ridan-to'g'ri o'zgartiruvchi (mutatsion) metoddir.
2. U o'chirilgan elementlardan iborat yangi massiv qaytaradi.
3. Elementlarni biron bir pozitsiyaga kiritish yoki bir vaqtning o'zida almashtirish imkonini beradi.

## Ishlash natijasi:
```text
Mart qo'shilgach: [ 'Yanvar', 'Fevral', 'Mart', 'Aprel', 'May' ]
O'chirib olingan: [ 'Fevral' ]
Qolgan oylar: [ 'Yanvar', 'Mart', 'Aprel', 'May' ]
Almashtirilgach: [ 'Dekabr', 'Mart', 'Aprel', 'May' ]
```


# 125-Topshiriq: concat() vs Spread operator ([...arr]) birlashtirishda

## Topshiriq sharti:
Massivlarni birlashtirishda `concat` va zamonaviy spread `[...]` operatorini solishtiring.

## Yechim (JS yoki TS kodi):
```typescript
function testArrayMerging(): void {
  const part1 = [1, 2];
  const part2 = [3, 4];
  const extra = 5;

  // concat orqali
  const resConcat = part1.concat(part2, extra);
  console.log("concat natijasi:", resConcat);

  // Spread orqali (zamonaviy va qulay)
  const resSpread = [...part1, ...part2, extra];
  console.log("spread natijasi:", resSpread);
}

testArrayMerging();
```

## Tushuntirish va Mantiq:
1. `concat` va spread ikkalasi ham asl massivlarni o'zgartirmaydi va yangi massiv hosil qiladi.
2. Spread sintaksisi (`[...a, ...b]`) ancha ko'rgazmali bo'lib, o'rtaga yoki chetlariga yangi elementlarni osongina qo'shish imkonini beradi.
3. Zamonaviy TypeScript va React dasturlashida spread operatori de-fakto standart hisoblanadi.

## Ishlash natijasi:
```text
concat natijasi: [ 1, 2, 3, 4, 5 ]
spread natijasi: [ 1, 2, 3, 4, 5 ]
```


# 126-Topshiriq: Array.prototype.flat(): Chuqur massivlarni tekislash

## Topshiriq sharti:
Kiritilgan chuqur (nested) ko'p o'lchovli massivlarni `flat(depth)` va `flat(Infinity)` orqali tekis holatga keltiring.

## Yechim (JS yoki TS kodi):
```typescript
function testFlat(): void {
  const nested = [1, [2, [3, [4, 5]]]];

  console.log("Asl massiv:", JSON.stringify(nested));
  console.log("flat(1):", nested.flat(1));
  console.log("flat(2):", nested.flat(2));
  console.log("flat(Infinity):", nested.flat(Infinity));

  // Bo'sh kataklarni (holes) tozalash
  const sparse = [1, 2, , 4, , 5];
  console.log("Siyrak massiv flat(0):", sparse.flat(0));
}

testFlat();
```

## Tushuntirish va Mantiq:
1. `flat(depth)` massiv ichidagi ichki massivlarni berilgan chuqurlik darajasi bo'yicha yuqoriga chiqaradi (tekislaydi).
        2. `flat(Infinity)` har qanday darajadagi chuqurlikdagi massivni bir o'lchovli tekis massivga aylantiradi.
        3. Shuningdek, massivdagi bo'sh teshiklarni (empty slots) avtomatik ravishda olib tashlaydi.

## Ishlash natijasi:
```text
Asl massiv: [1,[2,[3,[4,5]]]]
flat(1): [ 1, 2, [ 3, [ 4, 5 ] ] ]
flat(2): [ 1, 2, 3, [ 4, 5 ] ]
flat(Infinity): [ 1, 2, 3, 4, 5 ]
Siyrak massiv flat(0): [ 1, 2, 4, 5 ]
```


# 127-Topshiriq: Array.prototype.flatMap(): Xaritalash va tekislash kombinatsiyasi

## Topshiriq sharti:
Jumlalardan iborat massivni so'zlarga ajratish va ularni bitta tekis massivga yig'ish uchun `flatMap` metodini qo'llang.

## Yechim (JS yoki TS kodi):
```typescript
function extractWords(sentences: string[]): string[] {
  // map qilib so'ng flat(1) qilish o'rniga bitta amalda flatMap
  return sentences.flatMap((s) => s.split(" "));
}

const lines = ["Salom dunyo", "JavaScript va TypeScript", "Ajoyib dasturlash"];
const words = extractWords(lines);

console.log("Barcha ajratilgan so'zlar:", words);
```

## Tushuntirish va Mantiq:
1. `flatMap(callback)` har bir element ustida `map` bajaradi va natijani 1 daraja tekislaydi (`flat(1)`).
2. `arr.map(...).flat()` ga nisbatan unumdorroq ishlaydi, chunki oraliq massiv yaratmaydi.
3. Shuningdek, callback ichidan `[]` qaytarish orqali elementlarni olib tashlash (1-to-0) yoki bir nechta element qaytarish (1-to-N) mumkin.

## Ishlash natijasi:
```text
Barcha ajratilgan so'zlar: [ 'Salom', 'dunyo', 'JavaScript', 'va', 'TypeScript', 'Ajoyib', 'dasturlash' ]
```


# 128-Topshiriq: Array.prototype.sort(): Sonlarni to'g'ri saralash va comparator

## Topshiriq sharti:
`sort()` ning default leksikografik saralash xatosini (`[10, 2, 5]` -> `[10, 2, 5]`) ko'rsating va to'g'ri raqamli comparator yozing.

## Yechim (JS yoki TS kodi):
```typescript
function testSortingNumbers(): void {
  const numbers = [25, 8, 100, 4, 1, 50];

  // Noto'g'ri: parametrsiz sort string sifatida saralaydi ('100' < '25')
  const wrongSort = [...numbers].sort();
  console.log("Noto'g'ri (string) saralash:", wrongSort);

  // To'g'ri: solishtiruvchi funksiya (a - b)
  const ascending = [...numbers].sort((a, b) => a - b);
  console.log("O'sish tartibida:", ascending);

  // Kamayish tartibida (b - a)
  const descending = [...numbers].sort((a, b) => b - a);
  console.log("Kamayish tartibida:", descending);
}

testSortingNumbers();
```

## Tushuntirish va Mantiq:
1. `sort()` parametri ko'rsatilmasa elementlarni satrga aylantirib, ularning Unicode kodlari bo'yicha saralaydi (shuning uchun `'100' < '25'`).
2. Raqamlarni to'g'ri saralash uchun `(a, b) => a - b` taqqoslash funksiyasi (comparator) berilishi shart:
   - Agar `a - b < 0` bo'lsa, `a` oldin keladi.
   - Agar `a - b > 0` bo'lsa, `b` oldin keladi.
3. Eslatma: `sort()` asl massivni to'g'ridan-to'g'ri o'zgartiradi (mutatsion).

## Ishlash natijasi:
```text
Noto'g'ri (string) saralash: [ 1, 100, 25, 4, 50, 8 ]
O'sish tartibida: [ 1, 4, 8, 25, 50, 100 ]
Kamayish tartibida: [ 100, 50, 25, 8, 4, 1 ]
```


# 129-Topshiriq: Obyektlar massivini bir nechta xususiyatlar bo'yicha saralash

## Topshiriq sharti:
Talabalar ro'yxatini avval fakultet bo'yicha alifbo tartibida, fakultet teng bo'lsa ball bo'yicha kamayish tartibida saralovchi funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
interface Student {
  name: string;
  faculty: string;
  score: number;
}

function sortStudents(students: Student[]): Student[] {
  return [...students].sort((a, b) => {
    // 1. Fakultet bo'yicha taqqoslash (localeCompare)
    const facultyDiff = a.faculty.localeCompare(b.faculty);
    if (facultyDiff !== 0) {
      return facultyDiff;
    }

    // 2. Ball bo'yicha kamayish tartibida
    return b.score - a.score;
  });
}

const list: Student[] = [
  { name: "Anvar", faculty: "Kiberxavfsizlik", score: 85 },
  { name: "Shahnoza", faculty: "Dasturlash", score: 95 },
  { name: "Bobur", faculty: "Kiberxavfsizlik", score: 92 },
  { name: "Zafar", faculty: "Dasturlash", score: 88 }
];

const sorted = sortStudents(list);
sorted.forEach((s) => {
  console.log(`${s.faculty} | ${s.name} | Ball: ${s.score}`);
});
```

## Tushuntirish va Mantiq:
1. Bir nechta maydonlar bo'yicha saralashda dastlab birinchi shart tekshiriladi; agar farq `0` bo'lmasa, o'sha natija qaytariladi.
2. Agar birinchi shart teng bo'lsa (`facultyDiff === 0`), keyingi shartga (ballga) o'tiladi.
3. Matnlarni milliy alifbo qoidalariga ko'ra to'g'ri solishtirish uchun `a.localeCompare(b)` ishlatiladi.

## Ishlash natijasi:
```text
Dasturlash | Shahnoza | Ball: 95
Dasturlash | Zafar | Ball: 88
Kiberxavfsizlik | Bobur | Ball: 92
Kiberxavfsizlik | Anvar | Ball: 85
```


# 130-Topshiriq: Array.prototype.reverse(): Massivni teskari o'girish va mutatsiya

## Topshiriq sharti:
`reverse()` metodining asl massivni o'zgartirishini ko'rsating va massivni o'zgartirmasdan teskari nusxa olish usullarini solishtiring.

## Yechim (JS yoki TS kodi):
```typescript
function testReverse(): void {
  const original = [1, 2, 3, 4, 5];

  // slice() yoki spread qilib so'ng reverse qilish
  const reversedCopy = [...original].reverse();

  console.log("Teskari nusxa:", reversedCopy);
  console.log("Asl massiv (buzilmadi):", original);

  // Asl massivda to'g'ridan-to'g'ri chaqirish
  original.reverse();
  console.log("Asl massiv mutatsiyaga uchradi:", original);
}

testReverse();
```

## Tushuntirish va Mantiq:
1. `reverse()` metodi massiv elementlarini o'z joyida teskari qilib qo'yadi va asl massivni o'zgartiradi.
2. Dasturda kutilmagan yon ta'sirlarning oldini olish uchun avval nusxa olish `[...arr].reverse()` kerak.
3. ES2023 da bu muammo yangi `toReversed()` metodi orqali rasman hal qilingan.

## Ishlash natijasi:
```text
Teskari nusxa: [ 5, 4, 3, 2, 1 ]
Asl massiv (buzilmadi): [ 1, 2, 3, 4, 5 ]
Asl massiv mutatsiyaga uchradi: [ 5, 4, 3, 2, 1 ]
```


# 131-Topshiriq: ES2023 Immutatsion metodlar: toSorted, toReversed va toSpliced

## Topshiriq sharti:
ES2023 da kiritilgan o'zgarmas (immutable) `toSorted()`, `toReversed()` va `toSpliced()` metodlarining ishlashini namoyish eting.

## Yechim (JS yoki TS kodi):
```typescript
function testES2023ImmutableArray(): void {
  const nums = [30, 10, 50, 20, 40];

  // @ts-ignore
  const sorted = nums.toSorted((a, b) => a - b);
  // @ts-ignore
  const reversed = nums.toReversed();
  // @ts-ignore
  const spliced = nums.toSpliced(1, 2, 999);

  console.log("Asl massiv (o'zgarmagan):", nums);
  console.log("toSorted():", sorted);
  console.log("toReversed():", reversed);
  console.log("toSpliced():", spliced);
}

testES2023ImmutableArray();
```

## Tushuntirish va Mantiq:
1. ES2023 standartida massivlarning barcha asosiy mutatsion metodlariga xavfsiz immutatsion muqobillar kiritildi.
2. `toSorted()`, `toReversed()`, `toSpliced()` asl massivga tegmasdan to'g'ridan-to'g'ri yangi massiv nusxasini qaytaradi.
3. Bu Redux, React va funksional dasturlashda nusxa olish (`[...arr]`) kodlarini qisqartiradi.

## Ishlash natijasi:
```text
Asl massiv (o'zgarmagan): [ 30, 10, 50, 20, 40 ]
toSorted(): [ 10, 20, 30, 40, 50 ]
toReversed(): [ 40, 20, 50, 10, 30 ]
toSpliced(): [ 30, 999, 20, 40 ]
```


# 132-Topshiriq: ES2023 with() metodi: Elementni almashtirib yangi nusxa olish

## Topshiriq sharti:
Massivning ma'lum indeksidagi qiymatini asl massivni o'zgartirmasdan almashtiruvchi `arr.with(index, value)` metodini qo'llang.

## Yechim (JS yoki TS kodi):
```typescript
function testWithMethod(): void {
  const letters = ["a", "b", "c", "d"];

  // 2-indeksdagi 'c' ni 'Z' ga almashtirib yangi massiv olamiz
  // @ts-ignore
  const updated = letters.with(2, "Z");

  // Manfiy indeks ham mumkin (-1 oxirgi element)
  // @ts-ignore
  const lastUpdated = letters.with(-1, "OXIRGI");

  console.log("Asl massiv:", letters);
  console.log("with(2, 'Z'):", updated);
  console.log("with(-1, 'OXIRGI'):", lastUpdated);
}

testWithMethod();
```

## Tushuntirish va Mantiq:
1. `with(index, value)` metodi massivning nusxasini oladi va ko'rsatilgan indeksdagi qiymatni yangisiga almashtiradi.
2. Manfiy indekslarni ham qo'llab-quvvatlaydi (`-1` = oxirgi element).
3. Bu usul React holatini yangilashda (`setList(list.with(i, newVal))`) juda toza va qulay sintaksis beradi.

## Ishlash natijasi:
```text
Asl massiv: [ 'a', 'b', 'c', 'd' ]
with(2, 'Z'): [ 'a', 'b', 'Z', 'd' ]
with(-1, 'OXIRGI'): [ 'a', 'b', 'c', 'OXIRGI' ]
```


# 133-Topshiriq: Object.groupBy() va Map.groupBy() (ES2024)

## Topshiriq sharti:
ES2024 standartidagi o'rnatilgan `Object.groupBy()` va `Map.groupBy()` metodlari orqali ma'lumotlarni oson guruhlashni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
interface CarItem {
  model: string;
  type: "sedan" | "suv" | "hatchback";
}

const cars: CarItem[] = [
  { model: "Malibu", type: "sedan" },
  { model: "Tracker", type: "suv" },
  { model: "Lacetti", type: "sedan" },
  { model: "Tahoe", type: "suv" }
];

// @ts-ignore
const groupedCars = Object.groupBy(cars, (car) => car.type);

console.log("Guruhlangan avtomobillar:");
console.log("Sedanlar:", groupedCars.sedan?.map((c: any) => c.model));
console.log("SUVlar:", groupedCars.suv?.map((c: any) => c.model));
```

## Tushuntirish va Mantiq:
1. ES2024 gacha ma'lumotlarni guruhlash uchun qiyin `reduce()` kodlari yozilar yoki Lodash kutubxonasiga murojaat qilinar edi.
2. `Object.groupBy(iterable, callback)` endi tilning o'zida mavjud bo'lib, eng optimal tezlikda ob'ekt kalitlari bo'yicha guruhlaydi.
3. `Map.groupBy()` esa ixtiyoriy ob'ektlar kalit bo'lgan holatda `Map` to'plami qaytaradi.

## Ishlash natijasi:
```text
Guruhlangan avtomobillar:
Sedanlar: [ 'Malibu', 'Lacetti' ]
SUVlar: [ 'Tracker', 'Tahoe' ]
```


# 134-Topshiriq: Massivdan takrorlangan elementlarni tozalash (Unique Elements)

## Topshiriq sharti:
Massivdan dublikatlarni tozalashning ikki usulini (`new Set` va `filter()`) unumdorlik va qulaylik bo'yicha solishtiring.

## Yechim (JS yoki TS kodi):
```typescript
function testRemoveDuplicates(): void {
  const numbers = [1, 2, 2, 3, 4, 4, 4, 5, 1];

  // 1. Set orqali (eng tez O(N))
  const uniqueViaSet = [...new Set(numbers)];
  console.log("Set orqali tozalangan:", uniqueViaSet);

  // 2. filter va indexOf orqali (O(N^2))
  const uniqueViaFilter = numbers.filter((val, index, arr) => arr.indexOf(val) === index);
  console.log("filter orqali tozalangan:", uniqueViaFilter);
}

testRemoveDuplicates();
```

## Tushuntirish va Mantiq:
1. `[...new Set(arr)]` takrorlanmas qiymatlar to'plamini (Set) tuzadi va spread orqali yana massivga qaytaradi. Uning vaqt murakkabligi `O(N)` bo'lib, eng samarali yo'ldir.
2. `filter((v, i, a) => a.indexOf(v) === i)` har bir elementning massivdagi birinchi uchragan indeksini tekshiradi. Har qadamda `indexOf` ishlagani sababli u `O(N^2)` vaqt oladi va katta massivlarda sekin ishlaydi.

## Ishlash natijasi:
```text
Set orqali tozalangan: [ 1, 2, 3, 4, 5 ]
filter orqali tozalangan: [ 1, 2, 3, 4, 5 ]
```


# 135-Topshiriq: Ikki massivning kesishmasi (Array Intersection)

## Topshiriq sharti:
Ikkita massivning umumiy elementlarini (kesishmasini) `Set` yordamida `O(N + M)` vaqtda topuvchi funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
function arrayIntersection<T>(arr1: T[], arr2: T[]): T[] {
  const set2 = new Set(arr2);
  // Faqat set2 da bor elementlarni olamiz va natijani ham unikal qilamiz
  return [...new Set(arr1.filter((item) => set2.has(item)))];
}

const listA = [1, 2, 3, 4, 5, 3];
const listB = [3, 4, 5, 6, 7];

console.log("Kesishma:", arrayIntersection(listA, listB));
```

## Tushuntirish va Mantiq:
1. Ikkinchi massiv `Set` ga o'tkazilganda `set.has()` tekshiruvi `O(1)` vaqt oladi.
2. Bu orqali ikki massivning kesishmasi `O(N * M)` emas, balki chiziqli `O(N + M)` tezlikda topiladi.
3. Huquqlar (permissions) va umumiy teglar bilan ishlashda eng ko'p qo'llaniladigan funksiyalardan biridir.

## Ishlash natijasi:
```text
Kesishma: [ 3, 4, 5 ]
```


# 136-Topshiriq: Ikki massivning farqi (Array Difference)

## Topshiriq sharti:
Birinchi massivda bor, lekin ikkinchi massivda mavjud bo'lmagan elementlarni aniqlovchi `arrayDifference` funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function arrayDifference<T>(source: T[], exclude: T[]): T[] {
  const excludeSet = new Set(exclude);
  return source.filter((item) => !excludeSet.has(item));
}

const allPermissions = ["read", "write", "delete", "export", "share"];
const userPermissions = ["read", "share"];

const missingPermissions = arrayDifference(allPermissions, userPermissions);
console.log("Foydalanuvchida yo'q huquqlar:", missingPermissions);
```

## Tushuntirish va Mantiq:
1. Massivlar farqi (A \ B) to'plamlar nazariyasining klassik amali hisoblanadi.
2. `Set.prototype.has()` orqali tekshirish tezkor bo'lib, ruxsatlar auditida, bazadagi o'zgarishlarni solishtirishda keng qo'llaniladi.

## Ishlash natijasi:
```text
Foydalanuvchida yo'q huquqlar: [ 'write', 'delete', 'export' ]
```


# 137-Topshiriq: Fisher-Yates Shuffle: Massiv elementlarini xolis tasodifiy aralashtirish

## Topshiriq sharti:
Nima uchun `sort(() => Math.random() - 0.5)` noto'g'ri ekanligini va Fisher-Yates algoritmi orqali massivni xolis aralashtirishni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function shuffleFisherYates<T>(array: T[]): T[] {
  const arr = [...array];
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    // Destructuring orqali qiymatlarni almashtirish (swap)
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

const deck = [1, 2, 3, 4, 5, 6, 7, 8];
console.log("Aralashtirilgan massiv:", shuffleFisherYates(deck));
console.log("Yana aralashtirilgan:", shuffleFisherYates(deck));
```

## Tushuntirish va Mantiq:
1. `arr.sort(() => Math.random() - 0.5)` usuli qat'iy matematik taqsimot bermaydi va ba'zi elementlar o'z o'rnida qolib ketish ehtimoli yuqori bo'ladi.
2. Fisher-Yates (yoki Knuth) algoritmi massiv oxiridan boshlab har bir elementni o'zidan oldingi tasodifiy element bilan almashtiradi.
3. Bu algoritm `O(N)` vaqt oladi va har bir permutatsiyaning yuzaga kelish ehtimolini teng (1/N!) ta'minlaydi.

## Ishlash natijasi:
```text
Aralashtirilgan massiv: [ 4, 7, 1, 8, 2, 5, 3, 6 ]
Yana aralashtirilgan: [ 2, 8, 3, 6, 1, 4, 7, 5 ]
```


# 138-Topshiriq: Array.prototype.fill(): Massivni standart qiymatlar bilan to'ldirish

## Topshiriq sharti:
`fill` metodining xususiyatlarini va obyektlar bilan to'ldirganda bitta manzil nusxalanishi xavfini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function testFill(): void {
  // Primitivlar bilan to'ldirish: xavfsiz
  const zeroArray = new Array(5).fill(0);
  console.log("Nollar massivi:", zeroArray);

  // Obyekt bilan to'ldirishdagi XAVF:
  const badMatrix = new Array(3).fill([]);
  badMatrix[0].push("xato");
  console.log("Xato: barcha qatorlar bitta massivga bog'langan:", badMatrix);

  // To'g'ri usul: Array.from
  const correctMatrix = Array.from({ length: 3 }, () => []);
  correctMatrix[0].push("to'g'ri");
  console.log("To'g'ri: har bir qator alohida mustaqil massiv:", correctMatrix);
}

testFill();
```

## Tushuntirish va Mantiq:
1. `fill(val, start, end)` massivning katakchalarini berilgan qiymat bilan to'ldiradi.
2. Agar `val` obyekt yoki massiv bo'lsa, xotiradagi ayni bir xil havola barcha kataklarga ko'chiriladi. Ularning birini o'zgartirsangiz, barchasi o'zgaradi!
3. Obyektlar yoki ichki massivlar bilan to'ldirishda har doim `Array.from({ length }, () => ({}))` usulidan foydalanish shart.

## Ishlash natijasi:
```text
Nollar massivi: [ 0, 0, 0, 0, 0 ]
Xato: barcha qatorlar bitta massivga bog'langan: [ [ 'xato' ], [ 'xato' ], [ 'xato' ] ]
To'g'ri: har bir qator alohida mustaqil massiv: [ [ 'to\'g\'ri' ], [], [] ]
```


# 139-Topshiriq: Ko'p o'lchovli matritsalar yaratish va diagonallar yig'indisini hisoblash

## Topshiriq sharti:
N x N o'lchamdagi kvadrat matritsaning asosiy va yordamchi diagonallaridagi sonlar yig'indisini hisoblovchi funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
function sumDiagonals(matrix: number[][]): { main: number; secondary: number } {
  const n = matrix.length;
  let main = 0;
  let secondary = 0;

  for (let i = 0; i < n; i++) {
    main += matrix[i][i];
    secondary += matrix[i][n - 1 - i];
  }

  return { main, secondary };
}

const squareGrid = [
  [1, 2, 3],
  [4, 5, 6],
  [7, 8, 9]
];

const diagSums = sumDiagonals(squareGrid);
console.log("Asosiy diagonal yig'indisi (1+5+9):", diagSums.main);
console.log("Yordamchi diagonal yig'indisi (3+5+7):", diagSums.secondary);
```

## Tushuntirish va Mantiq:
1. Kvadrat matritsada asosiy diagonal elementlari `[i][i]` koordinatalarida joylashadi.
2. Yordamchi diagonal elementlari esa `[i][n - 1 - i]` koordinatalariga to'g'ri keladi.
3. Bitta `for` sikli orqali ikkala diagonalni parallel hisoblash unumdorlikni `O(N)` qiladi.

## Ishlash natijasi:
```text
Asosiy diagonal yig'indisi (1+5+9): 15
Yordamchi diagonal yig'indisi (3+5+7): 15
```


# 140-Topshiriq: Chunking: Massivni belgilangan o'lchamdagi bo'laklarga ajratish

## Topshiriq sharti:
Katta massivni `chunkSize` o'lchamli kichik massivlar guruhiga bo'lib beruvchi `chunkArray` utilitasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function chunkArray<T>(array: T[], size: number): T[][] {
  const result: T[][] = [];
  for (let i = 0; i < array.length; i += size) {
    result.push(array.slice(i, i + size));
  }
  return result;
}

const elements = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

console.log("3 tadan bo'lingan:", chunkArray(elements, 3));
console.log("4 tadan bo'lingan:", chunkArray(elements, 4));
```

## Tushuntirish va Mantiq:
1. Massivni bo'laklarga ajratish (chunking) ma'lumotlarni paketlab (batching) yuborishda, UI da panjarali (grid) ko'rinishda joylashtirishda zarur bo'ladi.
2. `i += size` qadami va `slice(i, i + size)` kombinatsiyasi orqali har safar yangi qism kesib olinadi.
3. Oxirgi qism to'liq to'lmasa ham `slice` xatosiz boricha qismini qaytaradi.

## Ishlash natijasi:
```text
3 tadan bo'lingan: [ [ 1, 2, 3 ], [ 4, 5, 6 ], [ 7, 8, 9 ], [ 10 ] ]
4 tadan bo'lingan: [ [ 1, 2, 3, 4 ], [ 5, 6, 7, 8 ], [ 9, 10 ] ]
```


# 141-Topshiriq: Massivda eng katta va eng kichik qiymatni topish

## Topshiriq sharti:
`Math.max` va `Math.min` ning spread operatori bilan ishlashini va katta massivlarda `Maximum call stack size exceeded` xatosining oldini olishni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function findMinMaxSafe(numbers: number[]): { min: number; max: number } {
  if (numbers.length === 0) {
    throw new Error("Massiv bo'sh bo'lishi mumkin emas");
  }

  // 100,000 dan ortiq elementlar uchun reduce xavfsiz (call stack to'lmaydi)
  return numbers.reduce(
    (acc, curr) => ({
      min: curr < acc.min ? curr : acc.min,
      max: curr > acc.max ? curr : acc.max
    }),
    { min: numbers[0], max: numbers[0] }
  );
}

const testNumbers = [45, 12, 89, -5, 120, 3];
console.log("Natija:", findMinMaxSafe(testNumbers));
```

## Tushuntirish va Mantiq:
1. Kichik massivlar uchun `Math.max(...arr)` juda qulay.
2. Biroq massivda 100,000 dan ortiq element bo'lsa, `Math.max(...arr)` argumentlar ro'yxatiga aylanganda `RangeError: Maximum call stack size exceeded` beradi.
3. Chiziqli `for` sikli yoki `reduce` xotira chegarasidan qat'iy nazar millionlab elementlar bilan ham xavfsiz ishlaydi.

## Ishlash natijasi:
```text
Natija: { min: -5, max: 120 }
```


# 142-Topshiriq: Zich (Dense) vs Siyrak (Sparse) massivlar farqi va teshiklar (holes)

## Topshiriq sharti:
Massivdagi `undefined` qiymati bilan 'bo'sh teshik' (hole) o'rtasidagi farqni va ularning `forEach` / `map` da qanday ishlashini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function testSparseArrays(): void {
  // Siyrak massiv (2-indeksda bo'sh joy bor)
  const sparse = [1, , 3];
  // Zich massiv (2-indeksda aniq undefined qiymati bor)
  const dense = [1, undefined, 3];

  console.log("sparse da '1' kaliti bormi:", 1 in sparse); // false!
  console.log("dense da '1' kaliti bormi:", 1 in dense);   // true!

  let sparseCount = 0;
  sparse.forEach(() => sparseCount++);
  console.log("sparse.forEach chaqirilish soni:", sparseCount); // 2! (bo'sh joy sakrab o'tiladi)

  let denseCount = 0;
  dense.forEach(() => denseCount++);
  console.log("dense.forEach chaqirilish soni:", denseCount);   // 3!
}

testSparseArrays();
```

## Tushuntirish va Mantiq:
1. JavaScriptda massivlar mohiyatan sonli kalitlarga ega obyektlardir.
2. Siyrak massivda (sparse array) indeks xotirada mavjud bo'lmaydi (`1 in sparse === false`).
3. Massiv metodlari (`forEach`, `map`, `filter`) bo'sh teshiklarni avtomatik tarzda tashlab o'tadi va ular uchun callback chaqirmaydi.
4. Aniq `undefined` berilgan zich massivda esa element mavjud deb hisoblanadi.

## Ishlash natijasi:
```text
sparse da '1' kaliti bormi: false
dense da '1' kaliti bormi: true
sparse.forEach chaqirilish soni: 2
dense.forEach chaqirilish soni: 3
```


# 143-Topshiriq: Array Iteratorlari: keys(), values() va entries()

## Topshiriq sharti:
`entries()` orqali massiv elementlari va ularning indekslarini `for...of` siklida bir vaqtda olishni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function testArrayIterators(): void {
  const colors = ["Qizil", "Yashil", "Ko'k"];

  console.log("--- entries() bilan aylanib chiqish ---");
  for (const [index, color] of colors.entries()) {
    console.log(`Indeks: ${index}, Rang: ${color}`);
  }

  console.log("\n--- keys() bilan ---");
  console.log([...colors.keys()]);

  console.log("\n--- values() bilan ---");
  console.log([...colors.values()]);
}

testArrayIterators();
```

## Tushuntirish va Mantiq:
1. `entries()` har bir iteratsiyada `[index, element]` juftligini qaytaruvchi iterator beradi.
2. Bu `for...of` siklida ham indeks, ham qiymat kerak bo'lgan holatda `forEach` o'rniga eng qulay va zamonaviy yechimdir.
3. `keys()` indekslar ketma-ketligini, `values()` esa qiymatlar ketma-ketligini qaytaradi.

## Ishlash natijasi:
```text
--- entries() bilan aylanib chiqish ---
Indeks: 0, Rang: Qizil
Indeks: 1, Rang: Yashil
Indeks: 2, Rang: Ko'k

--- keys() bilan ---
[ 0, 1, 2 ]

--- values() bilan ---
[ 'Qizil', 'Yashil', 'Ko\'k' ]
```


# 144-Topshiriq: Array.isArray() va Tip tekshiruvi xavfsizligi

## Topshiriq sharti:
Nima uchun `typeof arr === 'object'` yetarli emasligini va `Array.isArray()` ning ahamiyatini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function testArrayValidation(input: any): void {
  console.log(`Qiymat: ${JSON.stringify(input)}`);
  console.log("  typeof:", typeof input);
  console.log("  Array.isArray():", Array.isArray(input));
}

testArrayValidation([1, 2, 3]);
testArrayValidation({ a: 1 });
testArrayValidation(null);
```

## Tushuntirish va Mantiq:
1. `typeof [] === 'object'` va `typeof {} === 'object'` bir xil bo'lgani sababli `typeof` massivni ajratib berolmaydi.
2. `null` ham `typeof` bo'yicha `'object'` hisoblanadi.
3. `Array.isArray(x)` JavaScriptning eng aniq va rasmiy usuli bo'lib, hatto boshqa iframe yoki context'dan kelgan massivlarni ham to'g'ri aniqlaydi.

## Ishlash natijasi:
```text
Qiymat: [1,2,3]
  typeof: object
  Array.isArray(): true
Qiymat: {"a":1}
  typeof: object
  Array.isArray(): false
Qiymat: null
  typeof: object
  Array.isArray(): false
```


# 145-Topshiriq: Array.prototype.join(): Formatlash va birlashtirish

## Topshiriq sharti:
Massiv elementlarini ajratuvchi vergul va so'nggi element uchun 'va' so'zi bilan birlashtiruvchi formatlash funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function formatListNatural(items: string[]): string {
  if (items.length === 0) return "";
  if (items.length === 1) return items[0];
  if (items.length === 2) return items.join(" va ");

  const allExceptLast = items.slice(0, -1).join(", ");
  const last = items[items.length - 1];

  return `${allExceptLast} va ${last}`;
}

console.log(formatListNatural(["Olma"]));
console.log(formatListNatural(["Olma", "Nok"]));
console.log(formatListNatural(["Olma", "Nok", "Uzum", "Anor"]));
```

## Tushuntirish va Mantiq:
1. `join(separator)` massivning barcha elementlarini satrga o'girib, ko'rsatilgan ajratuvchi orqali bitta matnga yig'adi.
2. Tabiiy tilda ro'yxatlarni ifodalashda `slice(0, -1)` va `join(", ")` kombinatsiyasi xalqaro formatlash talablariga mos keladi.

## Ishlash natijasi:
```text
Olma
Olma va Nok
Olma, Nok, Uzum va Anor
```


# 146-Topshiriq: Sliding Window (Sirpanuvchi oyna) algoritmi

## Topshiriq sharti:
Berilgan `k` o'lchamli oynada qo'shni elementlarning maksimal yig'indisini `O(N)` vaqt murakkabligida topuvchi funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
function maxSubarraySum(nums: number[], k: number): number | null {
  if (nums.length < k) return null;

  let maxSum = 0;
  let currentWindowSum = 0;

  // Dastlabki k ta element yig'indisi
  for (let i = 0; i < k; i++) {
    currentWindowSum += nums[i];
  }
  maxSum = currentWindowSum;

  // Oynani o'ngga suramiz: yangi element qo'shiladi, eski element chiqariladi
  for (let i = k; i < nums.length; i++) {
    currentWindowSum += nums[i] - nums[i - k];
    maxSum = Math.max(maxSum, currentWindowSum);
  }

  return maxSum;
}

const arr = [2, 1, 5, 1, 3, 2];
console.log("3 ta ketma-ket elementning maksimal yig'indisi (5+1+3):", maxSubarraySum(arr, 3));
```

## Tushuntirish va Mantiq:
1. Har bir oraliq uchun yangidan yig'indi hisoblash `O(N * k)` vaqt olgan bo'lardi.
2. Sirpanuvchi oyna (Sliding window) texnikasida oldingi yig'indiga yangi kirgan element qo'shiladi va oynadan chiqib ketgan element ayirib tashlanadi.
3. Bu amallar `O(1)` bo'lib, umumiy algoritm chiziqli `O(N)` vaqtda yakunlanadi.

## Ishlash natijasi:
```text
3 ta ketma-ket elementning maksimal yig'indisi (5+1+3): 9
```


# 147-Topshiriq: Two Pointers (Ikki ko'rsatkich) texnikasi: Two Sum muammosi

## Topshiriq sharti:
O'sish tartibida saralangan massivda yig'indisi `target` ga teng bo'lgan ikki sonning indekslarini `O(N)` vaqt va `O(1)` xotirada toping.

## Yechim (JS yoki TS kodi):
```typescript
function twoSumSorted(numbers: number[], target: number): [number, number] | null {
  let left = 0;
  let right = numbers.length - 1;

  while (left < right) {
    const sum = numbers[left] + numbers[right];

    if (sum === target) {
      return [left, right];
    } else if (sum < target) {
      left++; // Yig'indini kattalashtirish uchun chap ko'rsatkich o'ngga suriladi
    } else {
      right--; // Yig'indini kichiklashtirish uchun o'ng ko'rsatkich chapga suriladi
    }
  }

  return null;
}

const sortedArr = [2, 7, 11, 15, 20];
const targetSum = 18; // 7 + 11
console.log(`Yig'indi ${targetSum} uchun indekslar:`, twoSumSorted(sortedArr, targetSum));
```

## Tushuntirish va Mantiq:
1. Massiv saralangan bo'lsa, ikkita ko'rsatkich (boshida va oxirida) yordamida `O(N)` vaqtda qidirish mumkin.
2. Yig'indi kichik bo'lsa `left++`, katta bo'lsa `right--` qilinadi.
3. Bu usul qo'shimcha xotira (`Set` yoki `Map`) talab qilmaydi: `O(1)` space complexity.

## Ishlash natijasi:
```text
Yig'indi 18 uchun indekslar: [ 1, 2 ]
```


# 148-Topshiriq: Method Chaining: filter -> map -> reduce konveyeri

## Topshiriq sharti:
Bir nechta massiv metodlarini zanjirli (chaining) bog'lash orqali faol foydalanuvchilarning o'rtacha yoshini bitta deklarativ ifodada hisoblang.

## Yechim (JS yoki TS kodi):
```typescript
interface Member {
  name: string;
  age: number;
  active: boolean;
}

function getAverageAgeOfActiveMembers(members: Member[]): number {
  const activeAges = members
    .filter((m) => m.active)
    .map((m) => m.age);

  if (activeAges.length === 0) return 0;

  const totalAge = activeAges.reduce((sum, age) => sum + age, 0);
  return Math.round(totalAge / activeAges.length);
}

const team: Member[] = [
  { name: "Ali", age: 25, active: true },
  { name: "Vali", age: 35, active: false },
  { name: "Hasan", age: 29, active: true },
  { name: "Husan", age: 32, active: true }
];

console.log("Faol a'zolar o'rtacha yoshi:", getAverageAgeOfActiveMembers(team));
```

## Tushuntirish va Mantiq:
1. Metodlar zanjiri (Method Chaining) deklarativ dasturlashning asosiy ustunidir: kod nima qilinayotganini aniq ifodalaydi.
2. Har bir metod yangi massiv qaytargani sababli keyingi metod bevosita unga ulanadi.
3. Katta massivlarda oraliq massivlar xotirasini tejash uchun bitta `reduce` ga birlashtirish ham mumkin.

## Ishlash natijasi:
```text
Faol a'zolar o'rtacha yoshi: 29
```


# 149-Topshiriq: Unumdorlik tahlili: for vs forEach vs map/reduce

## Topshiriq sharti:
1 millionta element ustida klassik `for` sikli va `reduce` metodining bajarilish vaqtini `performance.now()` orqali o'lchovchi tahlil yozing.

## Yechim (JS yoki TS kodi):
```typescript
function benchmarkLoops(): void {
  const size = 1000000;
  const numbers = new Array(size).fill(1);

  // 1. Klassik for sikli
  const t0 = Date.now();
  let sumFor = 0;
  for (let i = 0; i < numbers.length; i++) {
    sumFor += numbers[i];
  }
  const t1 = Date.now();
  console.log(`1. Klassik for: yig'indi = ${sumFor}, vaqt: ${t1 - t0} ms`);

  // 2. Array.prototype.reduce
  const t2 = Date.now();
  const sumReduce = numbers.reduce((acc, curr) => acc + curr, 0);
  const t3 = Date.now();
  console.log(`2. reduce metodi: yig'indi = ${sumReduce}, vaqt: ${t3 - t2} ms`);
}

benchmarkLoops();
```

## Tushuntirish va Mantiq:
1. Klassik `for` sikli V8 dvigatelida eng chuqur optimallashtiriladi va to'g'ridan-to'g'ri mashina kodiga yaqin ishlaydi.
2. `reduce` va `forEach` har bir elementda funksiya chaqiruvi (function call overhead) xarajatiga ega bo'lgani uchun ozgina ko'proq vaqt oladi.
3. Biroq zamonaviy JIT kompilyatorlar bu farqni sezilarli kamaytirgan, shuning uchun odatda o'qilishi oson va xavfsiz bo'lgan deklarativ metodlar afzal ko'riladi.

## Ishlash natijasi:
```text
1. Klassik for: yig'indi = 1000000, vaqt: 2 ms
2. reduce metodi: yig'indi = 1000000, vaqt: 6 ms
```


# 150-Topshiriq: Amaliy loyiha: Savatcha va Buyurtmalar Tahlilchisi (Sintez)

## Topshiriq sharti:
Barcha o'rganilgan massiv metodlarini (filter, map, reduce, sort, groupBy) o'zida mujassam etgan to'liq E-tijorat tahlil modulini yarating.

## Yechim (JS yoki TS kodi):
```typescript
interface OrderItem {
  id: string;
  category: "elektronika" | "kiyim" | "oziq-ovqat";
  name: string;
  price: number;
  quantity: number;
}

class CartAnalytics {
  constructor(private items: OrderItem[]) {}

  // 1. Jami summa
  getTotalValue(): number {
    return this.items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  }

  // 2. Kategoriya bo'yicha sarflangan mablag'
  getSpendingByCategory(): Record<string, number> {
    return this.items.reduce((acc, item) => {
      acc[item.category] = (acc[item.category] || 0) + item.price * item.quantity;
      return acc;
    }, {} as Record<string, number>);
  }

  // 3. Eng qimmatbaho mahsulotlar (Top N)
  getTopValuableItems(limit: number = 2): OrderItem[] {
    return [...this.items]
      .sort((a, b) => b.price * b.quantity - a.price * a.quantity)
      .slice(0, limit);
  }
}

const sampleOrders: OrderItem[] = [
  { id: "1", category: "elektronika", name: "Sichqoncha", price: 150000, quantity: 2 },
  { id: "2", category: "kiyim", name: "Kurtka", price: 600000, quantity: 1 },
  { id: "3", category: "elektronika", name: "Monitor", price: 2500000, quantity: 1 },
  { id: "4", category: "oziq-ovqat", name: "Qahva", price: 80000, quantity: 3 }
];

const analytics = new CartAnalytics(sampleOrders);

console.log("Jami xarid summasi:", analytics.getTotalValue(), "so'm");
console.log("Kategoriya bo'yicha tahlil:", analytics.getSpendingByCategory());
console.log("Top qimmat mahsulotlar:", analytics.getTopValuableItems(2).map((i) => i.name));
```

## Tushuntirish va Mantiq:
1. Ushbu vazifa massivlar va iteratsiyalar bo'limining barcha konseptlarini real biznes senariysida sintezlaydi.
2. `reduce` orqali yig'indilar va toifalar bo'yicha hisob-kitoblar amalga oshiriladi.
3. `sort` va `slice` kombinatsiyasi orqali eng yetakchi (top) ko'rsatkichlar xavfsiz ajratib olinadi.

## Ishlash natijasi:
```text
Jami xarid summasi: 3640000 so'm
Kategoriya bo'yicha tahlil: { elektronika: 2800000, kiyim: 600000, 'oziq-ovqat': 240000 }
Top qimmat mahsulotlar: [ 'Monitor', 'Kurtka' ]
```

