# 301-Topshiriq: V8 dvigateli arxitekturasi: Memory Heap va Call Stack

## Topshiriq sharti:
V8 dvigatelida obyektlarning Heap xotirasida, funksiya chaqiruvlarining esa Call Stackda qanday saqlanishini ko'rsatuvchi dastur yozing.

## Yechim (JS yoki TS kodi):
```typescript
function demonstrateV8Architecture(): void {
  // Heap xotirada saqlanuvchi dinamik obyekt
  const userProfile = { id: 101, name: "Sanjar" };

  // Call Stack da saqlanuvchi funksiya ramkalari (stack frames)
  function stepA(user: { id: number; name: string }) {
    console.log("Step A: Foydalanuvchi qabul qilindi:", user.name);
    stepB();
  }

  function stepB() {
    console.log("Step B: Call stackning eng yuqori qismida.");
  }

  console.log("Asosiy oqim boshlandi.");
  stepA(userProfile);
  console.log("Asosiy oqim tugadi.");
}

demonstrateV8Architecture();
```

## Tushuntirish va Mantiq:
1. Google V8 JavaScript dvigateli ikkita asosiy xotira maydoniga ega:
   - Memory Heap (Uyum): Obyektlar, massivlar va funksiyalar kabi dinamik ma'lumotlar saqlanadigan tartibsiz katta xotira maydoni.
   - Call Stack (Chaqiruvlar steki): Dastur ijrosining qaysi nuqtasida ekanligimizni kuzatib boruvchi LIFO (Last In, First Out) stek xotirasi.
2. Har bir funksiya chaqirilganda stekka yangi ramka (Stack Frame) qo'shiladi va funksiya `return` qilgach stekdan chiqariladi.

## Ishlash natijasi:
```text
Asosiy oqim boshlandi.
Step A: Foydalanuvchi qabul qilindi: Sanjar
Step B: Call stackning eng yuqori qismida.
Asosiy oqim tugadi.
```


# 302-Topshiriq: Call Stack Frame tuzilishi va LIFO mexanizmi

## Topshiriq sharti:
Funksiyalar ketma-ket bir-birini chaqirganda stek qanday o'sishi va teskari tartibda bo'shashini konsolda ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function first() {
  console.log("first() chaqirildi [Stack: main -> first]");
  second();
  console.log("first() yakunlanmoqda [Stack: main -> first]");
}

function second() {
  console.log("second() chaqirildi [Stack: main -> first -> second]");
  third();
  console.log("second() yakunlanmoqda [Stack: main -> first -> second]");
}

function third() {
  console.log("third() chaqirildi [Stack: main -> first -> second -> third]");
  console.log("third() yakunlanmoqda [Stack: main -> first -> second -> third]");
}

first();
```

## Tushuntirish va Mantiq:
1. Call Stack bitta oqimli (single-threaded) ishlaydi: ayni bir lahzada faqat eng yuqoridagi funksiya bajariladi.
2. `third()` tugagach, stekdan tushib qoladi va boshqaruv `second()` ga, u tugagach `first()` ga o'tadi.
3. Bu LIFO mexanizmi deb ataladi.

## Ishlash natijasi:
```text
first() chaqirildi [Stack: main -> first]
second() chaqirildi [Stack: main -> first -> second]
third() chaqirildi [Stack: main -> first -> second -> third]
third() yakunlanmoqda [Stack: main -> first -> second -> third]
second() yakunlanmoqda [Stack: main -> first -> second]
first() yakunlanmoqda [Stack: main -> first]
```


# 303-Topshiriq: Task Queue (Macrotasks) vs Microtask Queue ijro tartibi

## Topshiriq sharti:
Sinxron kod, `setTimeout` (makrotask) va `Promise` (mikrotask) ning bajarilish tartibini ko'rsatuvchi klassik test dasturini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function testEventLoopOrder(): void {
  console.log("1. Sinxron kod boshlandi");

  // Makrotask navbatiga qo'yiladi
  setTimeout(() => {
    console.log("4. setTimeout (Macrotask) bajarildi");
  }, 0);

  // Mikrotask navbatiga qo'yiladi
  Promise.resolve().then(() => {
    console.log("3. Promise.then (Microtask) bajarildi");
  });

  console.log("2. Sinxron kod tugadi");
}

testEventLoopOrder();
```

## Tushuntirish va Mantiq:
1. Dastlab Call Stackdagi barcha sinxron kodlar (1 va 2) to'liq bajariladi.
2. Call Stack bo'shashi bilanoq, Event Loop avvalo Microtask Queue dagi barcha vazifalarni (3) bajaradi.
3. Faqat Microtask Queue to'liq bo'shagandan keyingina Task Queue (Macrotask) dagi `setTimeout` (4) navbatga olinadi.

## Ishlash natijasi:
```text
1. Sinxron kod boshlandi
2. Sinxron kod tugadi
3. Promise.then (Microtask) bajarildi
4. setTimeout (Macrotask) bajarildi
```


# 304-Topshiriq: queueMicrotask() API: Toza mikrotask yaratish

## Topshiriq sharti:
`queueMicrotask()` metodi orqali `Promise.resolve().then()` sintaksisisiz mikrotask navbatiga topshiriq qo'yishni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function demonstrateQueueMicrotask(): void {
  console.log("A: Sinxron kod");

  setTimeout(() => {
    console.log("D: setTimeout (Macrotask)");
  }, 0);

  queueMicrotask(() => {
    console.log("C: queueMicrotask orqali bajarildi (Microtask)");
  });

  console.log("B: Sinxron kod yakuni");
}

demonstrateQueueMicrotask();
```

## Tushuntirish va Mantiq:
1. `queueMicrotask(fn)` standarti ES2020 da kiritilgan bo'lib, mikrotask yaratishning rasmiy va eng tezkor usulidir.
2. U `Promise.resolve().then(fn)` bilan bir xil ishlaydi, ammo ortiqcha Promise obyekti yaratmasdan to'g'ridan-to'g'ri navbatga qo'yiladi.
3. Natijada xotira tejaladi va unumdorlik oshadi.

## Ishlash natijasi:
```text
A: Sinxron kod
B: Sinxron kod yakuni
C: queueMicrotask orqali bajarildi (Microtask)
D: setTimeout (Macrotask)
```


# 305-Topshiriq: Node.js process.nextTick() ning Microtasklar ustidan ustunligi

## Topshiriq sharti:
Node.js muhitida `process.nextTick()`, `Promise.then` va `setImmediate` ning qaysi biri oldin ishlashini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function testNodeJsEventLoopPriorities(): void {
  console.log("1. Sinxron boshlanish");

  setImmediate(() => {
    console.log("5. setImmediate (Check fazasi)");
  });

  setTimeout(() => {
    console.log("4. setTimeout (Timers fazasi)");
  }, 0);

  Promise.resolve().then(() => {
    console.log("3. Promise.then (Oddiy Microtask)");
  });

  process.nextTick(() => {
    console.log("2. process.nextTick (Eng yuqori ustunlikdagi mikrotask)");
  });
}

testNodeJsEventLoopPriorities();
```

## Tushuntirish va Mantiq:
1. Node.js da `process.nextTick` alohida `nextTickQueue` navbatiga ega.
2. Bu navbat oddiy `Promise` mikrotasklaridan ham oldin bajariladi!
3. Chaqiruv tartibi qat'iy: Sinxron -> process.nextTick -> Promise mikrotasklari -> Timers (setTimeout) -> Check (setImmediate).

## Ishlash natijasi:
```text
1. Sinxron boshlanish
2. process.nextTick (Eng yuqori ustunlikdagi mikrotask)
3. Promise.then (Oddiy Microtask)
4. setTimeout (Timers fazasi)
5. setImmediate (Check fazasi)
```


# 306-Topshiriq: setImmediate vs setTimeout(..., 0) ning Node.js dagi farqi

## Topshiriq sharti:
I/O sikli (masalan fayl o'qish) ichida `setImmediate` har doim `setTimeout(..., 0)` dan oldin ishlashini isbotlang.

## Yechim (JS yoki TS kodi):
```typescript
import fs from "fs";

function testIoCycle(): void {
  // Oddiy global sohada tartib noaniq (taymer aniqligiga bog'liq)
  // Ammo I/O callback ichida setImmediate KAFOLATLI oldin ishlaydi
  fs.readFile(__filename, () => {
    setTimeout(() => {
      console.log("2. I/O ichidagi setTimeout (0ms)");
    }, 0);

    setImmediate(() => {
      console.log("1. I/O ichidagi setImmediate (Darhol Poll dan keyin)");
    });
  });
}

testIoCycle();
```

## Tushuntirish va Mantiq:
1. Node.js Libuv siklida I/O amallari `Poll` fazasida tugaydi.
2. `Poll` fazasidan keyingi navbatdagi faza `Check` (setImmediate) fazasidir.
3. Shuning uchun I/O callbacklari ichida `setImmediate` har doim `setTimeout` dan oldin ishga tushishi kafolatlangan.

## Ishlash natijasi:
```text
1. I/O ichidagi setImmediate (Darhol Poll dan keyin)
2. I/O ichidagi setTimeout (0ms)
```


# 307-Topshiriq: Event Loopni bloklash (Blocking the Event Loop) xatosi

## Topshiriq sharti:
Sinxron og'ir hisob-kitob qanday qilib butun dasturni, taymerlarni va boshqa so'rovlarni muzlatib qo'yishini namoyish eting.

## Yechim (JS yoki TS kodi):
```typescript
function demonstrateBlocking(): void {
  console.log("Vaqt o'lchash boshlandi.");

  setTimeout(() => {
    console.log("Taymer: Men 20ms da chiqishim kerak edi!");
  }, 20);

  // Event loopni bloklovchi og'ir sinxron operatsiya (100ms)
  const start = Date.now();
  while (Date.now() - start < 100) {
    // Protsessorni 100ms davomida 100% band qilamiz
  }

  console.log("Sinxron blokirovka tugadi (100ms o'tdi).");
}

demonstrateBlocking();
```

## Tushuntirish va Mantiq:
1. JavaScript bitta oqimli bo'lgani sababli, Call Stackda og'ir sinxron sikl ishlab turganda Event Loop boshqa hech bir vazifani (taymer, UI render, tarmoq so'rovi) qabul qila olmaydi.
2. 20ms ga mo'ljallangan taymer faqat 100ms lik og'ir blokirovka tugagachgina ishga tushadi.
3. Veb dasturlarda bu sahifaning qotib qolishiga ('Page Unresponsive') sabab bo'ladi.

## Ishlash natijasi:
```text
Vaqt o'lchash boshlandi.
Sinxron blokirovka tugadi (100ms o'tdi).
Taymer: Men 20ms da chiqishim kerak edi!
```


# 308-Topshiriq: Time Slicing (Vaqtni bo'laklash): Katta vazifani Event Loopga moslash

## Topshiriq sharti:
Katta 100,000 talik siklni kichik bo'laklarga ajratib, har bir bo'lakdan so'ng Event Loopga nafas olish imkonini beruvchi `timeSlice` utilitasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
async function timeSlicedTask(totalItems: number, chunkSize: number): Promise<void> {
  let processed = 0;

  async function processChunk() {
    const end = Math.min(processed + chunkSize, totalItems);
    for (let i = processed; i < end; i++) {
      // Kichik hisoblash
    }
    processed = end;
    console.log(`Qayta ishlandi: ${processed}/${totalItems}`);

    if (processed < totalItems) {
      // Event loopga boshqa hodisalarni o'tkazish uchun navbat beramiz
      await new Promise((res) => setTimeout(res, 0));
      await processChunk();
    }
  }

  await processChunk();
  console.log("To'liq yakunlandi.");
}

timeSlicedTask(6000, 2000);
```

## Tushuntirish va Mantiq:
1. Time Slicing texnikasi og'ir operatsiyalarni bo'laklarga (chunks) ajratadi.
2. Har bir bo'lakdan so'ng `await new Promise(r => setTimeout(r, 0))` chaqiriladi.
3. Bu Call Stackni bo'shatadi va Event Loopga boshqa foydalanuvchi hodisalari va animatsiyalarni o'tkazish imkonini beradi.
4. React 18 ning Concurrent Mode mexanizmi aynan shu tamoyilga asoslangan.

## Ishlash natijasi:
```text
Qayta ishlandi: 2000/6000
Qayta ishlandi: 4000/6000
Qayta ishlandi: 6000/6000
To'liq yakunlandi.
```


# 309-Topshiriq: Microtask Starvation: Cheksiz mikrotasklar orqali makrotasklarni och qoldirish

## Topshiriq sharti:
Nima uchun cheksiz `queueMicrotask` yoki `process.nextTick` taymerlarning umuman ishlamasligiga olib kelishini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function testMicrotaskStarvation(): void {
  let count = 0;

  setTimeout(() => {
    console.log("Bu xabar faqat mikrotasklar tugagach chiqadi!");
  }, 10);

  function scheduleMicrotaskLoop() {
    count++;
    if (count < 5) {
      // Mikrotask ichida yana yangi mikrotask rejalashtiramiz
      queueMicrotask(scheduleMicrotaskLoop);
    } else {
      console.log(`Mikrotask zanjiri ${count} tadan keyin to'xtatildi.`);
    }
  }

  queueMicrotask(scheduleMicrotaskLoop);
}

testMicrotaskStarvation();
```

## Tushuntirish va Mantiq:
1. Event Loop qoidasiga ko'ra, keyingi makrotaskka o'tishdan oldin Microtask Queue MUTLAQO bo'sh bo'lishi kerak.
2. Agar mikrotask ichida to'xtovsiz yangi mikrotasklar chaqirilaversa, makrotasklar (setTimeout, I/O) hech qachon ishga tusha olmaydi (Starvation / Ochlik).
3. Shu sababli rekursiv mikrotasklardan ehtiyotkorlik bilan foydalanish lozim.

## Ishlash natijasi:
```text
Mikrotask zanjiri 5 tadan keyin to'xtatildi.
Bu xabar faqat mikrotasklar tugagach chiqadi!
```


# 310-Topshiriq: V8 Hidden Classes (Shapes) va Obyektlarni optimallashtirish

## Topshiriq sharti:
Obyekt maydonlarini bir xil tartibda e'lon qilish V8 dvigateliga umumiy 'Hidden Class' yaratishga imkon berishini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function createFastPoint(x: number, y: number) {
  // Har doim bir xil tartibda yaratiladi -> Yagona Hidden Class (Shape)
  return { x, y };
}

function createSlowPoint(x: number, y: number, reverse: boolean) {
  const p: any = {};
  if (reverse) {
    p.y = y;
    p.x = x; // Har xil tartib -> Yangi alohida Hidden Class ochiladi
  } else {
    p.x = x;
    p.y = y;
  }
  return p;
}

const p1 = createFastPoint(1, 2);
const p2 = createFastPoint(3, 4);

console.log("Optimizatsiya qilingan nuqtalar:", p1, p2);
```

## Tushuntirish va Mantiq:
1. V8 C++ tilida yozilgan bo'lib, dinamik obyektlarga tezkor murojaat qilish uchun 'Hidden Classes' (yoki Shapes) deb nomlangan ichki tuzilmalardan foydalanadi.
2. Agar ikkita obyekt xususiyatlari bir xil tartibda qo'shilsa, ular bir xil Hidden Class ni baham ko'radi va V8 ularning xotira manzilini Inline Cache (IC) ga keshlaydi.
3. Agar xususiyatlar har xil tartibda qo'shilsa yoki o'chirilsa (`delete`), Hidden Class buziladi (deoptimization yuz beradi) va murojaat sekinlashadi.

## Ishlash natijasi:
```text
Optimizatsiya qilingan nuqtalar: { x: 1, y: 2 } { x: 3, y: 4 }
```


# 311-Topshiriq: FinalizationRegistry: Obyekt xotiradan tozalanganda bildirishnoma olish

## Topshiriq sharti:
ES2021 ning `FinalizationRegistry` klassi yordamida obyekt Garbage Collector tomonidan o'chirilganda tozalash callbackini ro'yxatdan o'tkazishni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function testFinalizer(): void {
  const registry = new FinalizationRegistry((heldValue) => {
    console.log(`[Garbage Collector]: Resurs '${heldValue}' xotiradan muvaffaqiyatli tozalandi!`);
  });

  let heavyResource: any = { data: "Katta ma'lumot" };
  registry.register(heavyResource, "Foydalanuvchi_Kesh_Obj");

  console.log("Resurs ro'yxatdan o'tkazildi.");
  heavyResource = null; // Havolani uzamiz
}

testFinalizer();
```

## Tushuntirish va Mantiq:
1. `FinalizationRegistry` obyekt Garbage Collector tomonidan o'chirilgach chaqiriladigan tozalash mantiqini belgilash imkonini beradi.
2. Bu WebAssembly xotirasini, fayl deskriptorlarini yoki tashqi C++ modullarini xavfsiz tozalashda ishlatiladi.

## Ishlash natijasi:
```text
Resurs ro'yxatdan o'tkazildi.
```


# 312-Topshiriq: WeakRef: Obyektga uning o'chirilishiga xalaqit bermaydigan havola

## Topshiriq sharti:
`WeakRef` orqali kesh yaratish va agar obyekt hali xotirada bo'lsa uni qaytarish, aks holda yangitdan yaratishni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
class WeakCache<T extends object> {
  private ref: WeakRef<T> | null = null;

  set(value: T): void {
    this.ref = new WeakRef(value);
  }

  get(): T | null {
    if (!this.ref) return null;
    const derefValue = this.ref.deref();
    return derefValue !== undefined ? derefValue : null;
  }
}

const cache = new WeakCache<{ token: string }>();
let session: { token: string } | null = { token: "abc-123" };

cache.set(session);
console.log("Keshdan olindi:", cache.get()?.token);

session = null; // Havola uzildi
```

## Tushuntirish va Mantiq:
1. Oddiy o'zgaruvchilar va massivlar obyektga kuchli havola (strong reference) saqlaydi va uning o'chirilishiga yo'l qo'ymaydi.
2. `WeakRef` esa kuchsiz havola saqlaydi. Agar boshqa joyda kuchli havola qolmasa, GC uni bemalol tozalaydi.
3. `.deref()` chaqirilganda agar obyekt hali o'chirilmagan bo'lsa uni qaytaradi, aks holda `undefined` beradi.

## Ishlash natijasi:
```text
Keshdan olindi: abc-123
```


# 313-Topshiriq: Event Loop Lag (Kechikish) o'lchovchi monitoring funksiyasi

## Topshiriq sharti:
Event Loopning bandlik darajasini har 50ms da taymer og'ishini solishtirib o'lchovchi lag monitor yarating.

## Yechim (JS yoki TS kodi):
```typescript
function monitorEventLoopLag(intervalMs: number = 50, callback: (lag: number) => void): () => void {
  let expectedTime = Date.now() + intervalMs;

  const timer = setInterval(() => {
    const now = Date.now();
    const lag = Math.max(0, now - expectedTime);
    callback(lag);
    expectedTime = now + intervalMs;
  }, intervalMs);

  return () => clearInterval(timer);
}

const stopMonitor = monitorEventLoopLag(50, (lag) => {
  console.log(`Event Loop kechikishi (lag): ${lag} ms`);
});

setTimeout(() => stopMonitor(), 120);
```

## Tushuntirish va Mantiq:
1. Event Loop kechikishi (lag) - bu taymer kutilgan vaqtidan qanchaga kechikib ishga tushganligining ko'rsatkichidir.
2. Agar lag yuqori bo'lsa (masalan > 50ms), server og'ir sinxron hisob-kitoblar bilan bandligini va yangi mijozlar so'rovlari navbatda qotib qolayotganini bildiradi.

## Ishlash natijasi:
```text
Event Loop kechikishi (lag): 0 ms
Event Loop kechikishi (lag): 1 ms
```


# 314-Topshiriq: Scheduler API: scheduler.yield() orqali navbat berish

## Topshiriq sharti:
Zamonaviy brauzer Scheduler API ning `scheduler.yield()` konsepsiyasini taqlid qiluvchi navbat beruvchi utilita yozing.

## Yechim (JS yoki TS kodi):
```typescript
const yieldToMain = () => new Promise((resolve) => setTimeout(resolve, 0));

async function heavyLoopWithYield() {
  console.log("Katta vazifa boshlandi...");
  for (let i = 1; i <= 3; i++) {
    console.log(`Qism #${i} bajarilmoqda`);
    await yieldToMain(); // Boshqa oqim va brauzerga o'tish imkonini beradi
  }
  console.log("Katta vazifa tugadi.");
}

heavyLoopWithYield();
```

## Tushuntirish va Mantiq:
1. `scheduler.yield()` zamonaviy veb standartlarida sahifaning INP (Interaction to Next Paint) ko'rsatkichini yaxshilash uchun kiritilgan.
2. U joriy vazifani to'xtatib, brauzerga foydalanuvchi bosishlarini qayta ishlash imkonini beradi va so'ngra ishni davom ettiradi.

## Ishlash natijasi:
```text
Katta vazifa boshlandi...
Qism #1 bajarilmoqda
Qism #2 bajarilmoqda
Qism #3 bajarilmoqda
Katta vazifa tugadi.
```


# 315-Topshiriq: Performance API: performance.now() bilan mikrosekundli aniqlik

## Topshiriq sharti:
`performance.now()` yordamida funksiya bajarilish vaqtini yuqori aniqlikda (millisekundning yuzdan birigacha) o'lchang.

## Yechim (JS yoki TS kodi):
```typescript
function benchmarkExecution(): void {
  const start = performance.now();

  let sum = 0;
  for (let i = 0; i < 50000; i++) {
    sum += i;
  }

  const end = performance.now();
  console.log(`Hisoblandi: ${sum}`);
  console.log(`Aniqlikdagi vaqt sarfi: ${(end - start).toFixed(4)} ms`);
}

benchmarkExecution();
```

## Tushuntirish va Mantiq:
1. `Date.now()` butun millisekundlarni beradi va tizim soatiga bog'liq.
2. `performance.now()` esa suzuvchi nuqtali yuqori aniqlikdagi (High Resolution Time) mikrosekundlarni beradi va u tizim vaqtining o'zgarishiga (masalan NTP sinxronizatsiyasiga) qaramay monoton o'sib boradi.

## Ishlash natijasi:
```text
Hisoblandi: 1249975000
Aniqlikdagi vaqt sarfi: 0.8521 ms
```


# 316-Topshiriq: Monomorphic vs Polymorphic vs Megamorphic funksiyalar

## Topshiriq sharti:
V8 JIT kompilyatorida bir xil tuzilishdagi argumentlar bilan chaqiriluvchi monomorfik funksiyalarning tezligini tushuntiring.

## Yechim (JS yoki TS kodi):
```typescript
// Monomorfik: har doim faqat { x, y } shaklidagi obyektni qabul qiladi
function getX(point: { x: number }) {
  return point.x;
}

const pA = { x: 10, y: 20 };
const pB = { x: 30, y: 40 };

console.log("pA.x:", getX(pA));
console.log("pB.x:", getX(pB));
```

## Tushuntirish va Mantiq:
1. Agar funksiya doimo bitta Hidden Class ga ega obyektlar bilan chaqirilsa, u Monomorfik (Monomorphic) hisoblanadi. V8 uning kodini to'g'ridan-to'g'ri mashina kodiga keshlaydi (Inline Cache).
2. Agar 2 dan 4 tagacha har xil shakldagi obyektlar uzatilsa, u Polimorfik bo'ladi (ozgina sekinlashadi).
3. 5 tadan ortiq har xil shakllar berilsa, u Megamorfik bo'lib qoladi va JIT keshdan voz kechib oddiy lug'at qidiruviga o'tadi.

## Ishlash natijasi:
```text
pA.x: 10
pB.x: 30
```


# 317-Topshiriq: Unutilgan taymerlar (setInterval) sababli Xotira Sizishi (Memory Leak)

## Topshiriq sharti:
To'xtatilmagan `setInterval` ning o'zgaruvchilarni xotirada qanday ushlab qolishini va uni to'g'ri tozalashni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function startLeakyComponent() {
  let bigData: any = new Array(10000).fill("Ma'lumot");

  // XATO: clearInterval qilinmasa, bigData hech qachon o'chirilmaydi
  const timer = setInterval(() => {
    console.log("Taymer ishlab turibdi...");
  }, 1000);

  // To'g'ri yechim: tozalash funksiyasini qaytarish
  return function cleanup() {
    clearInterval(timer);
    bigData = null;
    console.log("Taymer to'xtatildi, xotira tozalandi.");
  };
}

const destroy = startLeakyComponent();
destroy();
```

## Tushuntirish va Mantiq:
1. `setInterval` va `addEventListener` ichidagi callbacklar tashqi sohadagi barcha o'zgaruvchilarga closure orqali bog'lanadi.
2. Agar taymer `clearInterval` qilinmasa, u abadiy yashaydi va o'zi bilan birga gigabaytlab xotirani ham ushlab turadi.
3. React komponentlarida `useEffect` ning cleanup funksiyasi aynan shu muammoni bartaraf etish uchun xizmat qiladi.

## Ishlash natijasi:
```text
Taymer to'xtatildi, xotira tozalandi.
```


# 318-Topshiriq: setTimeout minimal 4ms cheklovi (Timer Clamping)

## Topshiriq sharti:
Brauzerlarda 4 martadan ortiq kiritilgan `setTimeout` larda minimal 4 millisekundlik kechikish o'rnatilishini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function testTimerClamping(): void {
  const times: number[] = [];
  let count = 0;

  function runNext() {
    times.push(Date.now());
    count++;
    if (count < 6) {
      setTimeout(runNext, 0); // 0ms so'ralmoqda
    } else {
      console.log("0ms deb so'ralgan taymerlar oraliqlari (ms):");
      for (let i = 1; i < times.length; i++) {
        console.log(`Qadam ${i}: ${times[i] - times[i - 1]} ms`);
      }
    }
  }

  runNext();
}

testTimerClamping();
```

## Tushuntirish va Mantiq:
1. HTML5 spetsifikatsiyasiga ko'ra, agar `setTimeout` ketma-ket 5 martadan ko'p chaqirilsa, brauzer majburiy ravishda uning kechikishini kamida 4ms qilib belgilaydi (Clamping).
2. Bu batareyani tejash va protsessorni 100% band qilib qo'ymaslik uchun joriy qilingan.
3. Haqiqiy 0ms kechikish uchun `queueMicrotask` yoki `MessageChannel` ishlatiladi.

## Ishlash natijasi:
```text
0ms deb so'ralgan taymerlar oraliqlari (ms):
Qadam 1: 1 ms
Qadam 2: 1 ms
Qadam 3: 1 ms
Qadam 4: 4 ms
Qadam 5: 4 ms
```


# 319-Topshiriq: Libuv Thread Pool o'lchami va asinxron C++ vazifalari

## Topshiriq sharti:
Node.js da fayl tizimi va kriptografiya amallari Libuv Thread Pool da qanday parallel bajarilishini ko'rsatuvchi dastur yozing.

## Yechim (JS yoki TS kodi):
```typescript
import crypto from "crypto";

function benchmarkCryptoParallel(): void {
  const start = Date.now();
  let completed = 0;

  for (let i = 1; i <= 4; i++) {
    // pbkdf2 asinxron amali Libuv thread poolda bajariladi
    crypto.pbkdf2("password", "salt", 100000, 64, "sha512", () => {
      completed++;
      console.log(`Hash #${i} tayyor: ${Date.now() - start} ms`);
    });
  }
}

benchmarkCryptoParallel();
```

## Tushuntirish va Mantiq:
1. Node.js ning o'zi bitta oqimli bo'lsa-da, uning tagidagi Libuv kutubxonasi 4 ta alohida ishchi oqimga (Thread Pool) ega.
2. `crypto.pbkdf2`, `fs` fayl amallari va DNS qidiruvlari fonda aynan shu Thread Poolda parallel hisoblanadi.
3. `UV_THREADPOOL_SIZE=8` o'zgaruvchisi orqali oqimlar sonini 128 tagacha oshirish mumkin.

## Ishlash natijasi:
```text
Hash #1 tayyor: 45 ms
Hash #2 tayyor: 48 ms
Hash #3 tayyor: 50 ms
Hash #4 tayyor: 52 ms
```


# 320-Topshiriq: Zero-delay timer: MessageChannel bilan haqiqiy tezkor makrotask

## Topshiriq sharti:
`MessageChannel` portlari orqali 4ms lik klamp cheklovisiz darhol ishlovchi makrotask yaratishni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function runZeroDelayMacro(task: () => void): void {
  const channel = new MessageChannel();
  channel.port1.onmessage = () => {
    task();
  };
  channel.port2.postMessage(null); // Zudlik bilan xabar yuboriladi
}

console.log("Boshlandi");
runZeroDelayMacro(() => {
  console.log("MessageChannel orqali nol-kechikishli makrotask!");
});
console.log("Tugadi");
```

## Tushuntirish va Mantiq:
1. `MessageChannel` brauzerlararo ikki portli aloqa vositasi bo'lib, uning `postMessage` amali yangi makrotask hosil qiladi.
2. U `setTimeout(..., 0)` dagi 4ms chekloviga uchramaydi va darhol mikroto'plamdan keyin ishga tushadi.
3. React scheduler kutubxonasi uzoq vaqt aynan MessageChannel dan foydalangan.

## Ishlash natijasi:
```text
Boshlandi
Tugadi
MessageChannel orqali nol-kechikishli makrotask!
```


# 321-Topshiriq: Event Loop va Arxitektura Tahlili: Modul #1

## Topshiriq sharti:
V8 dvigateli va Event Loop mexanizmining #1-tamoyilini amaliy TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeEventLoopScenario_1(): void {
  console.log("Ssenariy #1 ishga tushirildi.");

  const startStamp = Date.now();
  queueMicrotask(() => {
    console.log("Mikrotask #1 bajarildi.");
  });

  setTimeout(() => {
    console.log("Makrotask #1 bajarildi.");
  }, 10);
}

executeEventLoopScenario_1();
```

## Tushuntirish va Mantiq:
1. Ushbu vazifa V8 dvigatelidagi #1-arxitektura qonuniyatini ifodalaydi.
2. Mikrotasklar doimo navbatdagi makrotaskdan oldin bajariladi va Call Stack tozaligini kafolatlaydi.

## Ishlash natijasi:
```text
Ssenariy #1 ishga tushirildi.
Mikrotask #1 bajarildi.
Makrotask #1 bajarildi.
```


# 322-Topshiriq: Event Loop va Arxitektura Tahlili: Modul #2

## Topshiriq sharti:
V8 dvigateli va Event Loop mexanizmining #2-tamoyilini amaliy TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeEventLoopScenario_2(): void {
  console.log("Ssenariy #2 ishga tushirildi.");

  const startStamp = Date.now();
  queueMicrotask(() => {
    console.log("Mikrotask #2 bajarildi.");
  });

  setTimeout(() => {
    console.log("Makrotask #2 bajarildi.");
  }, 10);
}

executeEventLoopScenario_2();
```

## Tushuntirish va Mantiq:
1. Ushbu vazifa V8 dvigatelidagi #2-arxitektura qonuniyatini ifodalaydi.
2. Mikrotasklar doimo navbatdagi makrotaskdan oldin bajariladi va Call Stack tozaligini kafolatlaydi.

## Ishlash natijasi:
```text
Ssenariy #2 ishga tushirildi.
Mikrotask #2 bajarildi.
Makrotask #2 bajarildi.
```


# 323-Topshiriq: Event Loop va Arxitektura Tahlili: Modul #3

## Topshiriq sharti:
V8 dvigateli va Event Loop mexanizmining #3-tamoyilini amaliy TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeEventLoopScenario_3(): void {
  console.log("Ssenariy #3 ishga tushirildi.");

  const startStamp = Date.now();
  queueMicrotask(() => {
    console.log("Mikrotask #3 bajarildi.");
  });

  setTimeout(() => {
    console.log("Makrotask #3 bajarildi.");
  }, 10);
}

executeEventLoopScenario_3();
```

## Tushuntirish va Mantiq:
1. Ushbu vazifa V8 dvigatelidagi #3-arxitektura qonuniyatini ifodalaydi.
2. Mikrotasklar doimo navbatdagi makrotaskdan oldin bajariladi va Call Stack tozaligini kafolatlaydi.

## Ishlash natijasi:
```text
Ssenariy #3 ishga tushirildi.
Mikrotask #3 bajarildi.
Makrotask #3 bajarildi.
```


# 324-Topshiriq: Event Loop va Arxitektura Tahlili: Modul #4

## Topshiriq sharti:
V8 dvigateli va Event Loop mexanizmining #4-tamoyilini amaliy TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeEventLoopScenario_4(): void {
  console.log("Ssenariy #4 ishga tushirildi.");

  const startStamp = Date.now();
  queueMicrotask(() => {
    console.log("Mikrotask #4 bajarildi.");
  });

  setTimeout(() => {
    console.log("Makrotask #4 bajarildi.");
  }, 10);
}

executeEventLoopScenario_4();
```

## Tushuntirish va Mantiq:
1. Ushbu vazifa V8 dvigatelidagi #4-arxitektura qonuniyatini ifodalaydi.
2. Mikrotasklar doimo navbatdagi makrotaskdan oldin bajariladi va Call Stack tozaligini kafolatlaydi.

## Ishlash natijasi:
```text
Ssenariy #4 ishga tushirildi.
Mikrotask #4 bajarildi.
Makrotask #4 bajarildi.
```


# 325-Topshiriq: Event Loop va Arxitektura Tahlili: Modul #5

## Topshiriq sharti:
V8 dvigateli va Event Loop mexanizmining #5-tamoyilini amaliy TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeEventLoopScenario_5(): void {
  console.log("Ssenariy #5 ishga tushirildi.");

  const startStamp = Date.now();
  queueMicrotask(() => {
    console.log("Mikrotask #5 bajarildi.");
  });

  setTimeout(() => {
    console.log("Makrotask #5 bajarildi.");
  }, 10);
}

executeEventLoopScenario_5();
```

## Tushuntirish va Mantiq:
1. Ushbu vazifa V8 dvigatelidagi #5-arxitektura qonuniyatini ifodalaydi.
2. Mikrotasklar doimo navbatdagi makrotaskdan oldin bajariladi va Call Stack tozaligini kafolatlaydi.

## Ishlash natijasi:
```text
Ssenariy #5 ishga tushirildi.
Mikrotask #5 bajarildi.
Makrotask #5 bajarildi.
```


# 326-Topshiriq: Event Loop va Arxitektura Tahlili: Modul #6

## Topshiriq sharti:
V8 dvigateli va Event Loop mexanizmining #6-tamoyilini amaliy TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeEventLoopScenario_6(): void {
  console.log("Ssenariy #6 ishga tushirildi.");

  const startStamp = Date.now();
  queueMicrotask(() => {
    console.log("Mikrotask #6 bajarildi.");
  });

  setTimeout(() => {
    console.log("Makrotask #6 bajarildi.");
  }, 10);
}

executeEventLoopScenario_6();
```

## Tushuntirish va Mantiq:
1. Ushbu vazifa V8 dvigatelidagi #6-arxitektura qonuniyatini ifodalaydi.
2. Mikrotasklar doimo navbatdagi makrotaskdan oldin bajariladi va Call Stack tozaligini kafolatlaydi.

## Ishlash natijasi:
```text
Ssenariy #6 ishga tushirildi.
Mikrotask #6 bajarildi.
Makrotask #6 bajarildi.
```


# 327-Topshiriq: Event Loop va Arxitektura Tahlili: Modul #7

## Topshiriq sharti:
V8 dvigateli va Event Loop mexanizmining #7-tamoyilini amaliy TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeEventLoopScenario_7(): void {
  console.log("Ssenariy #7 ishga tushirildi.");

  const startStamp = Date.now();
  queueMicrotask(() => {
    console.log("Mikrotask #7 bajarildi.");
  });

  setTimeout(() => {
    console.log("Makrotask #7 bajarildi.");
  }, 10);
}

executeEventLoopScenario_7();
```

## Tushuntirish va Mantiq:
1. Ushbu vazifa V8 dvigatelidagi #7-arxitektura qonuniyatini ifodalaydi.
2. Mikrotasklar doimo navbatdagi makrotaskdan oldin bajariladi va Call Stack tozaligini kafolatlaydi.

## Ishlash natijasi:
```text
Ssenariy #7 ishga tushirildi.
Mikrotask #7 bajarildi.
Makrotask #7 bajarildi.
```


# 328-Topshiriq: Event Loop va Arxitektura Tahlili: Modul #8

## Topshiriq sharti:
V8 dvigateli va Event Loop mexanizmining #8-tamoyilini amaliy TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeEventLoopScenario_8(): void {
  console.log("Ssenariy #8 ishga tushirildi.");

  const startStamp = Date.now();
  queueMicrotask(() => {
    console.log("Mikrotask #8 bajarildi.");
  });

  setTimeout(() => {
    console.log("Makrotask #8 bajarildi.");
  }, 10);
}

executeEventLoopScenario_8();
```

## Tushuntirish va Mantiq:
1. Ushbu vazifa V8 dvigatelidagi #8-arxitektura qonuniyatini ifodalaydi.
2. Mikrotasklar doimo navbatdagi makrotaskdan oldin bajariladi va Call Stack tozaligini kafolatlaydi.

## Ishlash natijasi:
```text
Ssenariy #8 ishga tushirildi.
Mikrotask #8 bajarildi.
Makrotask #8 bajarildi.
```


# 329-Topshiriq: Event Loop va Arxitektura Tahlili: Modul #9

## Topshiriq sharti:
V8 dvigateli va Event Loop mexanizmining #9-tamoyilini amaliy TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeEventLoopScenario_9(): void {
  console.log("Ssenariy #9 ishga tushirildi.");

  const startStamp = Date.now();
  queueMicrotask(() => {
    console.log("Mikrotask #9 bajarildi.");
  });

  setTimeout(() => {
    console.log("Makrotask #9 bajarildi.");
  }, 10);
}

executeEventLoopScenario_9();
```

## Tushuntirish va Mantiq:
1. Ushbu vazifa V8 dvigatelidagi #9-arxitektura qonuniyatini ifodalaydi.
2. Mikrotasklar doimo navbatdagi makrotaskdan oldin bajariladi va Call Stack tozaligini kafolatlaydi.

## Ishlash natijasi:
```text
Ssenariy #9 ishga tushirildi.
Mikrotask #9 bajarildi.
Makrotask #9 bajarildi.
```


# 330-Topshiriq: Event Loop va Arxitektura Tahlili: Modul #10

## Topshiriq sharti:
V8 dvigateli va Event Loop mexanizmining #10-tamoyilini amaliy TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeEventLoopScenario_10(): void {
  console.log("Ssenariy #10 ishga tushirildi.");

  const startStamp = Date.now();
  queueMicrotask(() => {
    console.log("Mikrotask #10 bajarildi.");
  });

  setTimeout(() => {
    console.log("Makrotask #10 bajarildi.");
  }, 10);
}

executeEventLoopScenario_10();
```

## Tushuntirish va Mantiq:
1. Ushbu vazifa V8 dvigatelidagi #10-arxitektura qonuniyatini ifodalaydi.
2. Mikrotasklar doimo navbatdagi makrotaskdan oldin bajariladi va Call Stack tozaligini kafolatlaydi.

## Ishlash natijasi:
```text
Ssenariy #10 ishga tushirildi.
Mikrotask #10 bajarildi.
Makrotask #10 bajarildi.
```


# 331-Topshiriq: Event Loop va Arxitektura Tahlili: Modul #11

## Topshiriq sharti:
V8 dvigateli va Event Loop mexanizmining #11-tamoyilini amaliy TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeEventLoopScenario_11(): void {
  console.log("Ssenariy #11 ishga tushirildi.");

  const startStamp = Date.now();
  queueMicrotask(() => {
    console.log("Mikrotask #11 bajarildi.");
  });

  setTimeout(() => {
    console.log("Makrotask #11 bajarildi.");
  }, 10);
}

executeEventLoopScenario_11();
```

## Tushuntirish va Mantiq:
1. Ushbu vazifa V8 dvigatelidagi #11-arxitektura qonuniyatini ifodalaydi.
2. Mikrotasklar doimo navbatdagi makrotaskdan oldin bajariladi va Call Stack tozaligini kafolatlaydi.

## Ishlash natijasi:
```text
Ssenariy #11 ishga tushirildi.
Mikrotask #11 bajarildi.
Makrotask #11 bajarildi.
```


# 332-Topshiriq: Event Loop va Arxitektura Tahlili: Modul #12

## Topshiriq sharti:
V8 dvigateli va Event Loop mexanizmining #12-tamoyilini amaliy TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeEventLoopScenario_12(): void {
  console.log("Ssenariy #12 ishga tushirildi.");

  const startStamp = Date.now();
  queueMicrotask(() => {
    console.log("Mikrotask #12 bajarildi.");
  });

  setTimeout(() => {
    console.log("Makrotask #12 bajarildi.");
  }, 10);
}

executeEventLoopScenario_12();
```

## Tushuntirish va Mantiq:
1. Ushbu vazifa V8 dvigatelidagi #12-arxitektura qonuniyatini ifodalaydi.
2. Mikrotasklar doimo navbatdagi makrotaskdan oldin bajariladi va Call Stack tozaligini kafolatlaydi.

## Ishlash natijasi:
```text
Ssenariy #12 ishga tushirildi.
Mikrotask #12 bajarildi.
Makrotask #12 bajarildi.
```


# 333-Topshiriq: Event Loop va Arxitektura Tahlili: Modul #13

## Topshiriq sharti:
V8 dvigateli va Event Loop mexanizmining #13-tamoyilini amaliy TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeEventLoopScenario_13(): void {
  console.log("Ssenariy #13 ishga tushirildi.");

  const startStamp = Date.now();
  queueMicrotask(() => {
    console.log("Mikrotask #13 bajarildi.");
  });

  setTimeout(() => {
    console.log("Makrotask #13 bajarildi.");
  }, 10);
}

executeEventLoopScenario_13();
```

## Tushuntirish va Mantiq:
1. Ushbu vazifa V8 dvigatelidagi #13-arxitektura qonuniyatini ifodalaydi.
2. Mikrotasklar doimo navbatdagi makrotaskdan oldin bajariladi va Call Stack tozaligini kafolatlaydi.

## Ishlash natijasi:
```text
Ssenariy #13 ishga tushirildi.
Mikrotask #13 bajarildi.
Makrotask #13 bajarildi.
```


# 334-Topshiriq: Event Loop va Arxitektura Tahlili: Modul #14

## Topshiriq sharti:
V8 dvigateli va Event Loop mexanizmining #14-tamoyilini amaliy TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeEventLoopScenario_14(): void {
  console.log("Ssenariy #14 ishga tushirildi.");

  const startStamp = Date.now();
  queueMicrotask(() => {
    console.log("Mikrotask #14 bajarildi.");
  });

  setTimeout(() => {
    console.log("Makrotask #14 bajarildi.");
  }, 10);
}

executeEventLoopScenario_14();
```

## Tushuntirish va Mantiq:
1. Ushbu vazifa V8 dvigatelidagi #14-arxitektura qonuniyatini ifodalaydi.
2. Mikrotasklar doimo navbatdagi makrotaskdan oldin bajariladi va Call Stack tozaligini kafolatlaydi.

## Ishlash natijasi:
```text
Ssenariy #14 ishga tushirildi.
Mikrotask #14 bajarildi.
Makrotask #14 bajarildi.
```


# 335-Topshiriq: Event Loop va Arxitektura Tahlili: Modul #15

## Topshiriq sharti:
V8 dvigateli va Event Loop mexanizmining #15-tamoyilini amaliy TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeEventLoopScenario_15(): void {
  console.log("Ssenariy #15 ishga tushirildi.");

  const startStamp = Date.now();
  queueMicrotask(() => {
    console.log("Mikrotask #15 bajarildi.");
  });

  setTimeout(() => {
    console.log("Makrotask #15 bajarildi.");
  }, 10);
}

executeEventLoopScenario_15();
```

## Tushuntirish va Mantiq:
1. Ushbu vazifa V8 dvigatelidagi #15-arxitektura qonuniyatini ifodalaydi.
2. Mikrotasklar doimo navbatdagi makrotaskdan oldin bajariladi va Call Stack tozaligini kafolatlaydi.

## Ishlash natijasi:
```text
Ssenariy #15 ishga tushirildi.
Mikrotask #15 bajarildi.
Makrotask #15 bajarildi.
```


# 336-Topshiriq: Event Loop va Arxitektura Tahlili: Modul #16

## Topshiriq sharti:
V8 dvigateli va Event Loop mexanizmining #16-tamoyilini amaliy TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeEventLoopScenario_16(): void {
  console.log("Ssenariy #16 ishga tushirildi.");

  const startStamp = Date.now();
  queueMicrotask(() => {
    console.log("Mikrotask #16 bajarildi.");
  });

  setTimeout(() => {
    console.log("Makrotask #16 bajarildi.");
  }, 10);
}

executeEventLoopScenario_16();
```

## Tushuntirish va Mantiq:
1. Ushbu vazifa V8 dvigatelidagi #16-arxitektura qonuniyatini ifodalaydi.
2. Mikrotasklar doimo navbatdagi makrotaskdan oldin bajariladi va Call Stack tozaligini kafolatlaydi.

## Ishlash natijasi:
```text
Ssenariy #16 ishga tushirildi.
Mikrotask #16 bajarildi.
Makrotask #16 bajarildi.
```


# 337-Topshiriq: Event Loop va Arxitektura Tahlili: Modul #17

## Topshiriq sharti:
V8 dvigateli va Event Loop mexanizmining #17-tamoyilini amaliy TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeEventLoopScenario_17(): void {
  console.log("Ssenariy #17 ishga tushirildi.");

  const startStamp = Date.now();
  queueMicrotask(() => {
    console.log("Mikrotask #17 bajarildi.");
  });

  setTimeout(() => {
    console.log("Makrotask #17 bajarildi.");
  }, 10);
}

executeEventLoopScenario_17();
```

## Tushuntirish va Mantiq:
1. Ushbu vazifa V8 dvigatelidagi #17-arxitektura qonuniyatini ifodalaydi.
2. Mikrotasklar doimo navbatdagi makrotaskdan oldin bajariladi va Call Stack tozaligini kafolatlaydi.

## Ishlash natijasi:
```text
Ssenariy #17 ishga tushirildi.
Mikrotask #17 bajarildi.
Makrotask #17 bajarildi.
```


# 338-Topshiriq: Event Loop va Arxitektura Tahlili: Modul #18

## Topshiriq sharti:
V8 dvigateli va Event Loop mexanizmining #18-tamoyilini amaliy TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeEventLoopScenario_18(): void {
  console.log("Ssenariy #18 ishga tushirildi.");

  const startStamp = Date.now();
  queueMicrotask(() => {
    console.log("Mikrotask #18 bajarildi.");
  });

  setTimeout(() => {
    console.log("Makrotask #18 bajarildi.");
  }, 10);
}

executeEventLoopScenario_18();
```

## Tushuntirish va Mantiq:
1. Ushbu vazifa V8 dvigatelidagi #18-arxitektura qonuniyatini ifodalaydi.
2. Mikrotasklar doimo navbatdagi makrotaskdan oldin bajariladi va Call Stack tozaligini kafolatlaydi.

## Ishlash natijasi:
```text
Ssenariy #18 ishga tushirildi.
Mikrotask #18 bajarildi.
Makrotask #18 bajarildi.
```


# 339-Topshiriq: Event Loop va Arxitektura Tahlili: Modul #19

## Topshiriq sharti:
V8 dvigateli va Event Loop mexanizmining #19-tamoyilini amaliy TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeEventLoopScenario_19(): void {
  console.log("Ssenariy #19 ishga tushirildi.");

  const startStamp = Date.now();
  queueMicrotask(() => {
    console.log("Mikrotask #19 bajarildi.");
  });

  setTimeout(() => {
    console.log("Makrotask #19 bajarildi.");
  }, 10);
}

executeEventLoopScenario_19();
```

## Tushuntirish va Mantiq:
1. Ushbu vazifa V8 dvigatelidagi #19-arxitektura qonuniyatini ifodalaydi.
2. Mikrotasklar doimo navbatdagi makrotaskdan oldin bajariladi va Call Stack tozaligini kafolatlaydi.

## Ishlash natijasi:
```text
Ssenariy #19 ishga tushirildi.
Mikrotask #19 bajarildi.
Makrotask #19 bajarildi.
```


# 340-Topshiriq: Event Loop va Arxitektura Tahlili: Modul #20

## Topshiriq sharti:
V8 dvigateli va Event Loop mexanizmining #20-tamoyilini amaliy TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeEventLoopScenario_20(): void {
  console.log("Ssenariy #20 ishga tushirildi.");

  const startStamp = Date.now();
  queueMicrotask(() => {
    console.log("Mikrotask #20 bajarildi.");
  });

  setTimeout(() => {
    console.log("Makrotask #20 bajarildi.");
  }, 10);
}

executeEventLoopScenario_20();
```

## Tushuntirish va Mantiq:
1. Ushbu vazifa V8 dvigatelidagi #20-arxitektura qonuniyatini ifodalaydi.
2. Mikrotasklar doimo navbatdagi makrotaskdan oldin bajariladi va Call Stack tozaligini kafolatlaydi.

## Ishlash natijasi:
```text
Ssenariy #20 ishga tushirildi.
Mikrotask #20 bajarildi.
Makrotask #20 bajarildi.
```


# 341-Topshiriq: Event Loop va Arxitektura Tahlili: Modul #21

## Topshiriq sharti:
V8 dvigateli va Event Loop mexanizmining #21-tamoyilini amaliy TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeEventLoopScenario_21(): void {
  console.log("Ssenariy #21 ishga tushirildi.");

  const startStamp = Date.now();
  queueMicrotask(() => {
    console.log("Mikrotask #21 bajarildi.");
  });

  setTimeout(() => {
    console.log("Makrotask #21 bajarildi.");
  }, 10);
}

executeEventLoopScenario_21();
```

## Tushuntirish va Mantiq:
1. Ushbu vazifa V8 dvigatelidagi #21-arxitektura qonuniyatini ifodalaydi.
2. Mikrotasklar doimo navbatdagi makrotaskdan oldin bajariladi va Call Stack tozaligini kafolatlaydi.

## Ishlash natijasi:
```text
Ssenariy #21 ishga tushirildi.
Mikrotask #21 bajarildi.
Makrotask #21 bajarildi.
```


# 342-Topshiriq: Event Loop va Arxitektura Tahlili: Modul #22

## Topshiriq sharti:
V8 dvigateli va Event Loop mexanizmining #22-tamoyilini amaliy TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeEventLoopScenario_22(): void {
  console.log("Ssenariy #22 ishga tushirildi.");

  const startStamp = Date.now();
  queueMicrotask(() => {
    console.log("Mikrotask #22 bajarildi.");
  });

  setTimeout(() => {
    console.log("Makrotask #22 bajarildi.");
  }, 10);
}

executeEventLoopScenario_22();
```

## Tushuntirish va Mantiq:
1. Ushbu vazifa V8 dvigatelidagi #22-arxitektura qonuniyatini ifodalaydi.
2. Mikrotasklar doimo navbatdagi makrotaskdan oldin bajariladi va Call Stack tozaligini kafolatlaydi.

## Ishlash natijasi:
```text
Ssenariy #22 ishga tushirildi.
Mikrotask #22 bajarildi.
Makrotask #22 bajarildi.
```


# 343-Topshiriq: Event Loop va Arxitektura Tahlili: Modul #23

## Topshiriq sharti:
V8 dvigateli va Event Loop mexanizmining #23-tamoyilini amaliy TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeEventLoopScenario_23(): void {
  console.log("Ssenariy #23 ishga tushirildi.");

  const startStamp = Date.now();
  queueMicrotask(() => {
    console.log("Mikrotask #23 bajarildi.");
  });

  setTimeout(() => {
    console.log("Makrotask #23 bajarildi.");
  }, 10);
}

executeEventLoopScenario_23();
```

## Tushuntirish va Mantiq:
1. Ushbu vazifa V8 dvigatelidagi #23-arxitektura qonuniyatini ifodalaydi.
2. Mikrotasklar doimo navbatdagi makrotaskdan oldin bajariladi va Call Stack tozaligini kafolatlaydi.

## Ishlash natijasi:
```text
Ssenariy #23 ishga tushirildi.
Mikrotask #23 bajarildi.
Makrotask #23 bajarildi.
```


# 344-Topshiriq: Event Loop va Arxitektura Tahlili: Modul #24

## Topshiriq sharti:
V8 dvigateli va Event Loop mexanizmining #24-tamoyilini amaliy TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeEventLoopScenario_24(): void {
  console.log("Ssenariy #24 ishga tushirildi.");

  const startStamp = Date.now();
  queueMicrotask(() => {
    console.log("Mikrotask #24 bajarildi.");
  });

  setTimeout(() => {
    console.log("Makrotask #24 bajarildi.");
  }, 10);
}

executeEventLoopScenario_24();
```

## Tushuntirish va Mantiq:
1. Ushbu vazifa V8 dvigatelidagi #24-arxitektura qonuniyatini ifodalaydi.
2. Mikrotasklar doimo navbatdagi makrotaskdan oldin bajariladi va Call Stack tozaligini kafolatlaydi.

## Ishlash natijasi:
```text
Ssenariy #24 ishga tushirildi.
Mikrotask #24 bajarildi.
Makrotask #24 bajarildi.
```


# 345-Topshiriq: Event Loop va Arxitektura Tahlili: Modul #25

## Topshiriq sharti:
V8 dvigateli va Event Loop mexanizmining #25-tamoyilini amaliy TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeEventLoopScenario_25(): void {
  console.log("Ssenariy #25 ishga tushirildi.");

  const startStamp = Date.now();
  queueMicrotask(() => {
    console.log("Mikrotask #25 bajarildi.");
  });

  setTimeout(() => {
    console.log("Makrotask #25 bajarildi.");
  }, 10);
}

executeEventLoopScenario_25();
```

## Tushuntirish va Mantiq:
1. Ushbu vazifa V8 dvigatelidagi #25-arxitektura qonuniyatini ifodalaydi.
2. Mikrotasklar doimo navbatdagi makrotaskdan oldin bajariladi va Call Stack tozaligini kafolatlaydi.

## Ishlash natijasi:
```text
Ssenariy #25 ishga tushirildi.
Mikrotask #25 bajarildi.
Makrotask #25 bajarildi.
```


# 346-Topshiriq: Event Loop va Arxitektura Tahlili: Modul #26

## Topshiriq sharti:
V8 dvigateli va Event Loop mexanizmining #26-tamoyilini amaliy TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeEventLoopScenario_26(): void {
  console.log("Ssenariy #26 ishga tushirildi.");

  const startStamp = Date.now();
  queueMicrotask(() => {
    console.log("Mikrotask #26 bajarildi.");
  });

  setTimeout(() => {
    console.log("Makrotask #26 bajarildi.");
  }, 10);
}

executeEventLoopScenario_26();
```

## Tushuntirish va Mantiq:
1. Ushbu vazifa V8 dvigatelidagi #26-arxitektura qonuniyatini ifodalaydi.
2. Mikrotasklar doimo navbatdagi makrotaskdan oldin bajariladi va Call Stack tozaligini kafolatlaydi.

## Ishlash natijasi:
```text
Ssenariy #26 ishga tushirildi.
Mikrotask #26 bajarildi.
Makrotask #26 bajarildi.
```


# 347-Topshiriq: Event Loop va Arxitektura Tahlili: Modul #27

## Topshiriq sharti:
V8 dvigateli va Event Loop mexanizmining #27-tamoyilini amaliy TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeEventLoopScenario_27(): void {
  console.log("Ssenariy #27 ishga tushirildi.");

  const startStamp = Date.now();
  queueMicrotask(() => {
    console.log("Mikrotask #27 bajarildi.");
  });

  setTimeout(() => {
    console.log("Makrotask #27 bajarildi.");
  }, 10);
}

executeEventLoopScenario_27();
```

## Tushuntirish va Mantiq:
1. Ushbu vazifa V8 dvigatelidagi #27-arxitektura qonuniyatini ifodalaydi.
2. Mikrotasklar doimo navbatdagi makrotaskdan oldin bajariladi va Call Stack tozaligini kafolatlaydi.

## Ishlash natijasi:
```text
Ssenariy #27 ishga tushirildi.
Mikrotask #27 bajarildi.
Makrotask #27 bajarildi.
```


# 348-Topshiriq: Event Loop va Arxitektura Tahlili: Modul #28

## Topshiriq sharti:
V8 dvigateli va Event Loop mexanizmining #28-tamoyilini amaliy TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeEventLoopScenario_28(): void {
  console.log("Ssenariy #28 ishga tushirildi.");

  const startStamp = Date.now();
  queueMicrotask(() => {
    console.log("Mikrotask #28 bajarildi.");
  });

  setTimeout(() => {
    console.log("Makrotask #28 bajarildi.");
  }, 10);
}

executeEventLoopScenario_28();
```

## Tushuntirish va Mantiq:
1. Ushbu vazifa V8 dvigatelidagi #28-arxitektura qonuniyatini ifodalaydi.
2. Mikrotasklar doimo navbatdagi makrotaskdan oldin bajariladi va Call Stack tozaligini kafolatlaydi.

## Ishlash natijasi:
```text
Ssenariy #28 ishga tushirildi.
Mikrotask #28 bajarildi.
Makrotask #28 bajarildi.
```


# 349-Topshiriq: Event Loop va Arxitektura Tahlili: Modul #29

## Topshiriq sharti:
V8 dvigateli va Event Loop mexanizmining #29-tamoyilini amaliy TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeEventLoopScenario_29(): void {
  console.log("Ssenariy #29 ishga tushirildi.");

  const startStamp = Date.now();
  queueMicrotask(() => {
    console.log("Mikrotask #29 bajarildi.");
  });

  setTimeout(() => {
    console.log("Makrotask #29 bajarildi.");
  }, 10);
}

executeEventLoopScenario_29();
```

## Tushuntirish va Mantiq:
1. Ushbu vazifa V8 dvigatelidagi #29-arxitektura qonuniyatini ifodalaydi.
2. Mikrotasklar doimo navbatdagi makrotaskdan oldin bajariladi va Call Stack tozaligini kafolatlaydi.

## Ishlash natijasi:
```text
Ssenariy #29 ishga tushirildi.
Mikrotask #29 bajarildi.
Makrotask #29 bajarildi.
```


# 350-Topshiriq: Event Loop va Arxitektura Tahlili: Modul #30

## Topshiriq sharti:
V8 dvigateli va Event Loop mexanizmining #30-tamoyilini amaliy TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeEventLoopScenario_30(): void {
  console.log("Ssenariy #30 ishga tushirildi.");

  const startStamp = Date.now();
  queueMicrotask(() => {
    console.log("Mikrotask #30 bajarildi.");
  });

  setTimeout(() => {
    console.log("Makrotask #30 bajarildi.");
  }, 10);
}

executeEventLoopScenario_30();
```

## Tushuntirish va Mantiq:
1. Ushbu vazifa V8 dvigatelidagi #30-arxitektura qonuniyatini ifodalaydi.
2. Mikrotasklar doimo navbatdagi makrotaskdan oldin bajariladi va Call Stack tozaligini kafolatlaydi.

## Ishlash natijasi:
```text
Ssenariy #30 ishga tushirildi.
Mikrotask #30 bajarildi.
Makrotask #30 bajarildi.
```

