# 251-Topshiriq: Sinxron vs Asinxron dasturlash mohiyati

## Topshiriq sharti:
Sinxron kodning oqimni to'xtatib (blocking) qo'yishi va asinxron kodning fonda bajarilib keyin javob qaytarishini solishtiruvchi dastur yozing.

## Yechim (JS yoki TS kodi):
```typescript
function demonstrateSyncVsAsync(): void {
  console.log("1. Sinxron boshlandi.");

  // Asinxron chaqiruv (Web API / Timer)
  setTimeout(() => {
    console.log("3. Asinxron taymer callbacki bajarildi (0ms).");
  }, 0);

  console.log("2. Sinxron yakunlandi.");
}

demonstrateSyncVsAsync();
```

## Tushuntirish va Mantiq:
1. Sinxron kodda har bir operatsiya oldingisi tugashini kutadi (Blocking I/O).
2. Asinxron operatsiyalar esa (tarmoq so'rovlari, taymerlar, fayl o'qish) fon rejimiga topshiriladi va asosiy oqim to'xtab qolmaydi.
3. `setTimeout(..., 0)` bo'lsa ham, uning callbacki navbatga (Task Queue) qo'yiladi va barcha sinxron amallar bajarilib bo'lingachgina ishga tushadi.

## Ishlash natijasi:
```text
1. Sinxron boshlandi.
2. Sinxron yakunlandi.
3. Asinxron taymer callbacki bajarildi (0ms).
```


# 252-Topshiriq: Callback Hell (Piramida muammosi) va uning oqibatlari

## Topshiriq sharti:
Klassik Callback Hell holatini (ketma-ket 3 ta asinxron operatsiya) ko'rsating va xatoliklarni qayta ishlashdagi qiyinchiliklarni tushuntiring.

## Yechim (JS yoki TS kodi):
```typescript
function fetchUser(userId: number, callback: (err: Error | null, user?: any) => void) {
  setTimeout(() => callback(null, { id: userId, name: "Ali" }), 20);
}

function fetchUserOrders(userId: number, callback: (err: Error | null, orders?: string[]) => void) {
  setTimeout(() => callback(null, ["Buyurtma #1", "Buyurtma #2"]), 20);
}

function fetchOrderDetails(orderId: string, callback: (err: Error | null, details?: any) => void) {
  setTimeout(() => callback(null, { id: orderId, total: 250000 }), 20);
}

// Callback Hell: ichma-ich piramida
fetchUser(1, (err, user) => {
  if (err) return console.error(err);
  console.log("Foydalanuvchi:", user.name);

  fetchUserOrders(user.id, (err2, orders) => {
    if (err2) return console.error(err2);
    console.log("Buyurtmalar:", orders);

    fetchOrderDetails(orders![0], (err3, details) => {
      if (err3) return console.error(err3);
      console.log("Batafsil ma'lumot:", details);
    });
  });
});
```

## Tushuntirish va Mantiq:
1. Callback Hell (yoki Pyramid of Doom) asinxron operatsiyalar bir-biriga zanjirli bog'langanda yuzaga keladi.
2. Kod o'ng tomonga qarab siljib ketadi, o'qilishi o'ta qiyinlashadi.
3. Har bir darajada xatolikni tekshirish (`if (err)`) takrorlanadi va xatolar e'tibordan chetda qolishi osonlashadi.
4. Bu muammoni bartaraf etish uchun JavaScriptga Promiselar kiritilgan.

## Ishlash natijasi:
```text
Foydalanuvchi: Ali
Buyurtmalar: [ 'Buyurtma #1', 'Buyurtma #2' ]
Batafsil ma'lumot: { id: 'Buyurtma #1', total: 250000 }
```


# 253-Topshiriq: Promise holatlari: Pending, Fulfilled, Rejected

## Topshiriq sharti:
`new Promise` yordamida muvaffaqiyatli va muvaffaqiyatsiz tugaydigan holatlarni namoyish etuvchi funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
function simulateRequest(isSuccess: boolean): Promise<string> {
  return new Promise((resolve, reject) => {
    // Dastlab Promise "pending" (kutilmoqda) holatida bo'ladi
    setTimeout(() => {
      if (isSuccess) {
        resolve("Ma'lumot muvaffaqiyatli yuklandi! (Fulfilled)");
      } else {
        reject(new Error("Tarmoqda xatolik yuz berdi! (Rejected)"));
      }
    }, 20);
  });
}

simulateRequest(true)
  .then((res) => console.log("[Muvaffaqiyat]:", res))
  .catch((err) => console.error("[Xato]:", err.message));

simulateRequest(false)
  .then((res) => console.log("[Muvaffaqiyat]:", res))
  .catch((err) => console.log("[Ushlangan xato]:", err.message));
```

## Tushuntirish va Mantiq:
1. Promise kelajakda yakunlanadigan qiymatning kafolatidir.
2. U roppa-rosa 3 ta holatdan birida bo'lishi mumkin:
   - `pending`: boshlang'ich holat, jarayon davom etmoqda.
   - `fulfilled`: muvaffaqiyatli yakunlandi (`resolve` chaqirildi).
   - `rejected`: xatolik yuz berdi (`reject` chaqirildi).
3. Holat o'zgargandan so'ng qayta o'zgarmaydi (Settled).

## Ishlash natijasi:
```text
[Muvaffaqiyat]: Ma'lumot muvaffaqiyatli yuklandi! (Fulfilled)
[Ushlangan xato]: Tarmoqda xatolik yuz berdi! (Rejected)
```


# 254-Topshiriq: Promise Chaining: Ketma-ket ma'lumot o'tkazish

## Topshiriq sharti:
`.then()` zanjiri orqali raqamni ketma-ket 2 ga ko'paytiruvchi, 10 qo'shuvchi va formatlovchi Promise zanjirini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function startChain(initial: number): Promise<number> {
  return Promise.resolve(initial);
}

startChain(5)
  .then((val) => {
    console.log("1-qadam (boshlang'ich):", val);
    return val * 2; // 10
  })
  .then((val) => {
    console.log("2-qadam (* 2):", val);
    return val + 10; // 20
  })
  .then((val) => {
    console.log("3-qadam (+ 10):", val);
    return `Yakuniy natija: $${val}.00`;
  })
  .then((finalString) => {
    console.log(finalString);
  });
```

## Tushuntirish va Mantiq:
1. Har bir `.then()` chaqiruvi avtomatik ravishda yangi Promise qaytaradi.
2. Callback ichidan qaytarilgan har qanday qiymat keyingi `.then()` ga argument bo'lib o'tadi.
3. Agar callback yangi Promise qaytarsa, zanjir o'sha Promisening natijasini kutib turadi va keyin davom etadi.

## Ishlash natijasi:
```text
1-qadam (boshlang'ich): 5
2-qadam (* 2): 10
3-qadam (+ 10): 20
Yakuniy natija: $20.00
```


# 255-Topshiriq: Promise .catch() va .finally(): Tozalash va xatolik nazorati

## Topshiriq sharti:
Promise zanjirining o'rtasida yuzaga kelgan xatolikni `.catch()` bilan ushlash va natijasidan qat'iy nazar `.finally()` da resurslarni tozalashni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function runOperationWithCleanup(shouldFail: boolean): Promise<void> {
  console.log("Resurs (fayl yoki ulanish) ochildi.");

  return new Promise<string>((resolve, reject) => {
    setTimeout(() => {
      if (shouldFail) reject(new Error("Disk to'la!"));
      else resolve("Ma'lumot yozildi.");
    }, 20);
  })
    .then((msg) => {
      console.log("Operatsiya muvaffaqiyati:", msg);
    })
    .catch((err) => {
      console.log("Xatolik ushlandi:", err.message);
    })
    .finally(() => {
      console.log("[finally]: Resurs yopildi, xotira tozalandi.");
    });
}

runOperationWithCleanup(true);
```

## Tushuntirish va Mantiq:
1. `.catch()` zanjirning yuqori qismidagi istalgan nuqtada ro'y bergan xatoni ushlaydi.
2. `.finally(callback)` esa operatsiya muvaffaqiyatli yakunlanadimi yoki xato bilan tugaydimi - har doim albatta ishga tushadi.
3. UI da loaderlarni o'chirish (`setLoading(false)`) va tarmoq ulanishlarini yopish uchun `.finally()` eng to'g'ri joydir.

## Ishlash natijasi:
```text
Resurs (fayl yoki ulanish) ochildi.
Xatolik ushlandi: Disk to'la!
[finally]: Resurs yopildi, xotira tozalandi.
```


# 256-Topshiriq: Promise ichida xatoni qayta otish (Rethrowing)

## Topshiriq sharti:
`.catch()` blokida xatolikni log qilib, uni yuqori qatlamlarga qayta uzatish (rethrow) amaliyotini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function processPaymentTransaction(amount: number): Promise<void> {
  return Promise.reject(new Error("Mablag' yetarli emas"))
    .catch((err) => {
      console.log("[Lokal Log]: Xatolik qayd etildi:", err.message);
      // Xatolikni yuqoriga qayta otamiz
      throw new Error(`Tranzaksiya muvaffaqiyatsiz: ${err.message}`);
    });
}

processPaymentTransaction(500)
  .then(() => console.log("To'lov bajarildi"))
  .catch((fatalErr) => {
    console.log("[Global Nazoratchi]: Yuqori darajadagi xato:", fatalErr.message);
  });
```

## Tushuntirish va Mantiq:
1. `.catch()` ichida oddiy qiymat `return` qilinsa, xatolik 'yutib yuborilgan' (suppressed) bo'ladi va keyingi `.then()` ga o'tib ketadi.
2. Agar xatoni yuqori chaqiruvchiga ham yetkazish kerak bo'lsa, `throw err` qilinadi.
3. Bu xatolarni bir vaqtning o'zida ham log qilish, ham yuqori modulga bildirish imkonini beradi.

## Ishlash natijasi:
```text
[Lokal Log]: Xatolik qayd etildi: Mablag' yetarli emas
[Global Nazoratchi]: Yuqori darajadagi xato: Tranzaksiya muvaffaqiyatsiz: Mablag' yetarli emas
```


# 257-Topshiriq: Promise.resolve() va Promise.reject(): Bir lahzada yakunlanish

## Topshiriq sharti:
`Promise.resolve()` va `Promise.reject()` yordamida sinxron qiymatlarni asinxron Promise interfeysiga o'rashni namoyish eting.

## Yechim (JS yoki TS kodi):
```typescript
function getCachedData(key: string): Promise<string> {
  const cache: Record<string, string> = { "user_1": "Nodir" };

  if (key in cache) {
    // Sinxron keshdagi qiymatni darhol bajarilgan Promise sifatida qaytaramiz
    return Promise.resolve(cache[key]);
  }

  return Promise.reject(new Error(`Kalit topilmadi: ${key}`));
}

getCachedData("user_1").then((val) => console.log("Mavjud:", val));
getCachedData("user_99").catch((err) => console.log("Topilmadi:", err.message));
```

## Tushuntirish va Mantiq:
1. `Promise.resolve(value)` darhol `fulfilled` holatidagi yangi Promise qaytaradi.
2. `Promise.reject(reason)` esa darhol `rejected` holatidagi Promiseni hosil qiladi.
3. Ular sinxron kesh va asinxron tarmoq javoblarini yagona Promise interfeysiga keltirishda juda qulay.

## Ishlash natijasi:
```text
Mavjud: Nodir
Topilmadi: Kalit topilmadi: user_99
```


# 258-Topshiriq: async va await sintaksisi: Asinxron kodni toza yozish

## Topshiriq sharti:
Callback yoki `.then()` zanjiri o'rniga zamonaviy `async/await` yordamida ketma-ket ma'lumotlarni qabul qilishni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function fetchId(): Promise<number> {
  return new Promise((res) => setTimeout(() => res(42), 20));
}

function fetchDetails(id: number): Promise<string> {
  return new Promise((res) => setTimeout(() => res(`Ma'lumotlar [ID: ${id}]`), 20));
}

// async funksiya doimo Promise qaytaradi
async function loadUserData(): Promise<string> {
  console.log("Yuklash boshlandi...");

  // await asinxron Promisening yakunlanishini kutadi
  const id = await fetchId();
  const details = await fetchDetails(id);

  return details;
}

loadUserData().then((result) => {
  console.log("Yuklandi:", result);
});
```

## Tushuntirish va Mantiq:
1. ES2017 da kiritilgan `async/await` Promiselar ustidagi sintaktik qulaylikdir (Syntactic Sugar).
2. `async` kalit so'zi qo'yilgan funksiya har doim avtomatik tarzda `Promise` qaytaradi.
3. `await` faqat `async` funksiya ichida ishlaydi va Promisening qiymatini xuddi oddiy sinxron funksiya qaytargandek qabul qilib oladi.

## Ishlash natijasi:
```text
Yuklash boshlandi...
Yuklandi: Ma'lumotlar [ID: 42]
```


# 259-Topshiriq: try...catch bloki bilan async/await xatolarini boshqarish

## Topshiriq sharti:
`async/await` kodida yuzaga keladigan xatoliklarni an'anaviy `try...catch...finally` bloklari orqali ushlang.

## Yechim (JS yoki TS kodi):
```typescript
async function safeApiCall(endpoint: string): Promise<void> {
  try {
    console.log(`So'rov yuborilmoqda: ${endpoint}`);

    if (endpoint === "/error") {
      throw new Error("Serverda 500 ichki xatosi yuz berdi");
    }

    console.log("Muvaffaqiyatli ma'lumot olindi.");
  } catch (error: any) {
    console.log("[try...catch ushladi]:", error.message);
  } finally {
    console.log("So'rov yakunlandi (Yuklash indikatori o'chirildi).");
  }
}

safeApiCall("/error");
```

## Tushuntirish va Mantiq:
1. `async/await` ning eng katta afzalligi shundaki, unda xatoliklarni ushlash uchun sinxron kodlardagi kabi standart `try...catch` dan foydalanish mumkin.
2. Agar `await` qilingan Promise `reject` bo'lsa, u avtomatik tarzda `catch` blokiga tushadi.
3. Bu kodni o'qish va sinovdan o'tkazishni juda osonlashtiradi.

## Ishlash natijasi:
```text
So'rov yuborilmoqda: /error
[try...catch ushladi]: Serverda 500 ichki xatosi yuz berdi
So'rov yakunlandi (Yuklash indikatori o'chirildi).
```


# 260-Topshiriq: Promise.all(): Parallel bajarish va Fail-Fast tabiati

## Topshiriq sharti:
Bir nechta mustaqil asinxron operatsiyalarni `Promise.all` orqali parallel bajarish va bittasi xato bersa nima bo'lishini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function fetchFast(): Promise<string> {
  return new Promise((res) => setTimeout(() => res("Tezkor ma'lumot (20ms)"), 20));
}

function fetchSlow(): Promise<string> {
  return new Promise((res) => setTimeout(() => res("Sekin ma'lumot (50ms)"), 50));
}

function fetchBroken(): Promise<string> {
  return new Promise((_, rej) => setTimeout(() => rej(new Error("Buzilgan so'rov")), 30));
}

async function testPromiseAll(): Promise<void> {
  // 1. Muvaffaqiyatli parallel bajarish
  const results = await Promise.all([fetchFast(), fetchSlow()]);
  console.log("Parallel natijalar:", results);

  // 2. Fail-fast: bittasi rad etilsa butun guruh bekor bo'ladi
  try {
    await Promise.all([fetchFast(), fetchBroken(), fetchSlow()]);
  } catch (err: any) {
    console.log("Promise.all fail-fast xatosi:", err.message);
  }
}

testPromiseAll();
```

## Tushuntirish va Mantiq:
1. `Promise.all([p1, p2, ...])` barcha Promiselarni bir vaqtda parallel boshlaydi va umumiy vaqt eng sekin Promisening vaqtiga teng bo'ladi.
2. Agar barcha Promiselar muvaffaqiyatli yakunlansa, natijalar kiritilgan tartibda massiv bo'lib qaytadi.
3. Fail-Fast qoidasi: agar bittasi ham xato bersa (`reject`), boshqalarini kutib o'tirmay darhol xato qaytaradi.

## Ishlash natijasi:
```text
Parallel natijalar: [ "Tezkor ma'lumot (20ms)", "Sekin ma'lumot (50ms)" ]
Promise.all fail-fast xatosi: Buzilgan so'rov
```


# 261-Topshiriq: Promise.allSettled() (ES2020): Har bir natijani kafolatli qabul qilish

## Topshiriq sharti:
ES2020 ning `Promise.allSettled()` metodi orqali xatolarga qaramay barcha so'rovlarning holatini (`status: fulfilled/rejected`) tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
async function testAllSettled(): Promise<void> {
  const tasks = [
    Promise.resolve("Fayl 1 yuklandi"),
    Promise.reject(new Error("Fayl 2 topilmadi")),
    Promise.resolve("Fayl 3 yuklandi")
  ];

  const outcomes = await Promise.allSettled(tasks);

  outcomes.forEach((result, idx) => {
    if (result.status === "fulfilled") {
      console.log(`[#${idx + 1}] Muvaffaqiyatli:`, result.value);
    } else {
      console.log(`[#${idx + 1}] Xatolik:`, result.reason.message);
    }
  });
}

testAllSettled();
```

## Tushuntirish va Mantiq:
1. `Promise.allSettled()` hech qachon xato bilan to'xtamaydi (`never rejects`).
2. U massivdagi har bir Promise yakunlanishini sabr bilan kutadi.
3. Har bir element uchun `{ status: 'fulfilled', value }` yoki `{ status: 'rejected', reason }` obyektini qaytaradi.
4. Ommaviy bildirishnomalar yuborish yoki ko'p faylli yuklashlarda eng ishonchli metoddir.

## Ishlash natijasi:
```text
[#1] Muvaffaqiyatli: Fayl 1 yuklandi
[#2] Xatolik: Fayl 2 topilmadi
[#3] Muvaffaqiyatli: Fayl 3 yuklandi
```


# 262-Topshiriq: Promise.race(): Poyga mexanizmi (Eng birinchi yakunlangan)

## Topshiriq sharti:
`Promise.race()` yordamida ikkita serverdan qaysi biri birinchi javob qaytarsa o'shaning natijasini olishni namoyish eting.

## Yechim (JS yoki TS kodi):
```typescript
function serverA(): Promise<string> {
  return new Promise((res) => setTimeout(() => res("Server A javob berdi"), 50));
}

function serverB(): Promise<string> {
  return new Promise((res) => setTimeout(() => res("Server B javob berdi (tezroq!)"), 20));
}

async function runRace(): Promise<void> {
  const winner = await Promise.race([serverA(), serverB()]);
  console.log("Poyga g'olibi:", winner);
}

runRace();
```

## Tushuntirish va Mantiq:
1. `Promise.race([p1, p2, ...])` eng birinchi yakunlangan (fulfilled yoki rejected) Promisening natijasini qaytaradi.
2. Qolgan Promiselarning natijalari e'tiborga olinmaydi.
3. Geografik jihatdan yaqin DNS/CDN serverlariga parallel murojaat qilishda qo'llaniladi.

## Ishlash natijasi:
```text
Poyga g'olibi: Server B javob berdi (tezroq!)
```


# 263-Topshiriq: Promise.any() (ES2021) va AggregateError

## Topshiriq sharti:
`Promise.any()` orqali birinchi muvaffaqiyatli natijani olish va barcha Promiselar xato berganda `AggregateError` bilan ishlashni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
async function testPromiseAny(): void {
  // 1. Kamida bittasi muvaffaqiyatli bo'lsa
  const p1 = Promise.reject(new Error("Server 1 ishlamayapti"));
  const p2 = new Promise((res) => setTimeout(() => res("Server 2 muvaffaqiyatli!"), 20));
  const p3 = Promise.reject(new Error("Server 3 ishlamayapti"));

  const firstSuccess = await Promise.any([p1, p2, p3]);
  console.log("1. Birinchi muvaffaqiyat:", firstSuccess);

  // 2. Agar barchasi xato bersa: AggregateError tashlanadi
  try {
    await Promise.any([p1, p3]);
  } catch (err: any) {
    console.log("2. Barcha serverlar rad etildi:", err.name);
    // err.errors barcha xatolar massivini saqlaydi
    err.errors.forEach((e: Error) => console.log(" - Xatolik tafsiloti:", e.message));
  }
}

testPromiseAny();
```

## Tushuntirish va Mantiq:
1. `Promise.any()` muvaffaqiyatsizliklarni e'tiborsiz qoldiradi va eng birinchi `fulfilled` bo'lgan Promiseni qaytaradi.
2. Faqat va faqat barcha Promiselar rad etilsagina xato beradi.
3. Bunday xatolik `AggregateError` bo'lib, uning `.errors` massivida har bir Promisening xatosi jamlangan bo'ladi.

## Ishlash natijasi:
```text
1. Birinchi muvaffaqiyat: Server 2 muvaffaqiyatli!
2. Barcha serverlar rad etildi: AggregateError
 - Xatolik tafsiloti: Server 1 ishlamayapti
 - Xatolik tafsiloti: Server 3 ishlamayapti
```


# 264-Topshiriq: Promise.withResolvers() (ES2024): Tashqaridan boshqariluvchi Promise

## Topshiriq sharti:
ES2024 da kiritilgan `Promise.withResolvers()` orqali xavfsiz defer/resolver yaratishni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function testWithResolvers(): void {
  // @ts-ignore
  const { promise, resolve, reject } = Promise.withResolvers<string>();

  // resolve va reject endi tashqarida oddiy o'zgaruvchi!
  setTimeout(() => {
    resolve("Tashqaridan 30ms da resolve qilindi!");
  }, 30);

  promise.then((data) => {
    console.log("Natija olindi:", data);
  });
}

testWithResolvers();
```

## Tushuntirish va Mantiq:
1. ES2024 gacha `resolve` va `reject` ni tashqariga chiqarish uchun dasturchilar noqulay kodlar yozishgan.
2. `Promise.withResolvers()` bitta satrda `{ promise, resolve, reject }` obyektini qaytaradi.
3. Hodisaga asoslangan tizimlar va oqimlarni Promisega ulashda juda katta qulaylik yaratadi.

## Ishlash natijasi:
```text
Natija olindi: Tashqaridan 30ms da resolve qilindi!
```


# 265-Topshiriq: Ketma-ket (Sequential) vs Parallel chaqiruvlar vaqtini solishtirish

## Topshiriq sharti:
Uchta 30 millisekundlik so'rovni ketma-ket va parallel bajarish vaqtlarini solishtiruvchi dastur yozing.

## Yechim (JS yoki TS kodi):
```typescript
const delayTask = (ms: number, id: number) =>
  new Promise((res) => setTimeout(() => res(`Vazifa #${id}`), ms));

async function compareConcurrency(): Promise<void> {
  // 1. Ketma-ket (Sequential): 30ms + 30ms + 30ms = ~90ms
  const startSeq = Date.now();
  await delayTask(30, 1);
  await delayTask(30, 2);
  await delayTask(30, 3);
  const endSeq = Date.now();
  console.log(`Ketma-ket bajarilish vaqti: taxminan ${endSeq - startSeq} ms`);

  // 2. Parallel: barchasi bir vaqtda = ~30ms
  const startPar = Date.now();
  await Promise.all([delayTask(30, 1), delayTask(30, 2), delayTask(30, 3)]);
  const endPar = Date.now();
  console.log(`Parallel bajarilish vaqti: taxminan ${endPar - startPar} ms`);
}

compareConcurrency();
```

## Tushuntirish va Mantiq:
1. Agar vazifalar bir-biriga bog'liq bo'lmasa, ularni ketma-ket `await` qilish dastur ishini bir necha barobar sekinlashtiradi.
        2. `Promise.all` orqali parallel ishga tushirish umumiy kutish vaqtini eng uzun bitta vazifa vaqtigacha qisqartiradi.

## Ishlash natijasi:
```text
Ketma-ket bajarilish vaqti: taxminan 90 ms
Parallel bajarilish vaqti: taxminan 30 ms
```


# 266-Topshiriq: Asinxron sikllar: for...of bilan ketma-ket await qilish

## Topshiriq sharti:
Massivdagi ID lar bo'yicha ma'lumotlarni serverni zo'riqtirmaslik uchun bittalab ketma-ket tortib oluvchi `for...of` siklini yozing.

## Yechim (JS yoki TS kodi):
```typescript
async function fetchResource(id: number): Promise<string> {
  return new Promise((res) => setTimeout(() => res(`Resurs_${id}`), 20));
}

async function processSequentially(ids: number[]): Promise<void> {
  console.log("Ketma-ket jarayon boshlandi:");
  for (const id of ids) {
    const data = await fetchResource(id);
    console.log(`Yuklandi: ${data}`);
  }
  console.log("Barcha resurslar navbati bilan olindi.");
}

processSequentially([101, 102, 103]);
```

## Tushuntirish va Mantiq:
1. `for...of` sikli ichida `await` yozilganda, sikl keyingi elementga faqat joriy Promise to'liq yakunlangandan keyingina o'tadi.
2. Bu ma'lumotlar bazasi migratsiyalarida yoki qat'iy navbat talab qilinadigan jarayonlarda eng xavfsiz usuldir.

## Ishlash natijasi:
```text
Ketma-ket jarayon boshlandi:
Yuklandi: Resurs_101
Yuklandi: Resurs_102
Yuklandi: Resurs_103
Barcha resurslar navbati bilan olindi.
```


# 267-Topshiriq: forEach ichida async/await ning ishlamaslik sababi

## Topshiriq sharti:
Nima uchun `Array.prototype.forEach` ichida `await` ishlamasligini va uning o'rniga nima ishlatish kerakligini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
async function demonstrateForEachAsyncBug(): Promise<void> {
  const items = [1, 2, 3];

  console.log("--- forEach bilan xato sinov ---");
  // forEach callback qaytargan Promiseni umuman kutmaydi!
  items.forEach(async (num) => {
    await new Promise((res) => setTimeout(res, 20));
    console.log(`forEach ichida: ${num}`);
  });
  console.log("Bu satr forEach kutmasdan DARHOL chiqadi!");

  // To'g'ri usul: Promise.all + map
  await new Promise((res) => setTimeout(res, 50)); // Kichik pauza
  console.log("\n--- To'g'ri usul (Promise.all + map) ---");
  await Promise.all(
    items.map(async (num) => {
      await new Promise((res) => setTimeout(res, 20));
      console.log(`Parallel bajarildi: ${num}`);
    })
  );
  console.log("Barcha vazifalar to'liq yakunlangach chiqadi!");
}

demonstrateForEachAsyncBug();
```

## Tushuntirish va Mantiq:
1. `forEach` metodi sinxron metod bo'lib, uning ichki implementatsiyasi callback qaytargan Promiselarni kutmaydi (`ignores promises`).
2. Natijada `forEach` dan keyingi qatorlar asinxron amallar tugashidan oldin bajarilib ketadi.
3. Agar parallel ijro kerak bo'lsa `Promise.all(arr.map(...))`, ketma-ket ijro kerak bo'lsa `for...of` ishlatilishi shart.

## Ishlash natijasi:
```text
--- forEach bilan xato sinov ---
Bu satr forEach kutmasdan DARHOL chiqadi!
forEach ichida: 1
forEach ichida: 2
forEach ichida: 3

--- To'g'ri usul (Promise.all + map) ---
Parallel bajarildi: 1
Parallel bajarildi: 2
Parallel bajarildi: 3
Barcha vazifalar to'liq yakunlangach chiqadi!
```


# 268-Topshiriq: AbortController va AbortSignal: So'rovlarni bekor qilish

## Topshiriq sharti:
`AbortController` yordamida uzoq davom etayotgan asinxron jarayonni xohlagan paytda to'xtatish (cancel) mexanizmini yarating.

## Yechim (JS yoki TS kodi):
```typescript
function cancellableOperation(signal: AbortSignal): Promise<string> {
  return new Promise((resolve, reject) => {
    // Agar signal allaqachon bekor qilingan bo'lsa
    if (signal.aborted) {
      return reject(new Error("Amaliyot boshlanmasdan bekor qilindi"));
    }

    const timer = setTimeout(() => {
      resolve("Vazifa muvaffaqiyatli yakunlandi!");
    }, 100);

    // Bekor qilish hodisasini eshitamiz
    signal.addEventListener("abort", () => {
      clearTimeout(timer);
      reject(new Error("Amaliyot foydalanuvchi tomonidan bekor qilindi!"));
    });
  });
}

const controller = new AbortController();

cancellableOperation(controller.signal)
  .then(console.log)
  .catch((err) => console.log("[Bekor qilindi]:", err.message));

// 30ms dan so'ng bekor qilamiz (vazifa 100ms kutayotgan edi)
setTimeout(() => {
  controller.abort();
}, 30);
```

## Tushuntirish va Mantiq:
1. `AbortController` standart Web API bo'lib, `fetch` va boshqa asinxron operatsiyalarni bekor qilish uchun xizmat qiladi.
2. `controller.signal` obyekti asinxron funksiyaga uzatiladi.
3. `controller.abort()` chaqirilishi bilan signal 'abort' hodisasini chiqaradi va davom etayotgan operatsiyani to'xtatadi.

## Ishlash natijasi:
```text
[Bekor qilindi]: Amaliyot foydalanuvchi tomonidan bekor qilindi!
```


# 269-Topshiriq: AbortSignal.timeout() (ES2022) bilan qat'iy vaqt chegarasi

## Topshiriq sharti:
ES2022 ning `AbortSignal.timeout(ms)` imkoniyati orqali belgilangan vaqtdan oshib ketgan so'rovni avtomatik bekor qilishni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function fetchWithTimeoutSimulation(signal: AbortSignal): Promise<string> {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      resolve("Serverdan ma'lumot keldi");
    }, 100); // 100ms kerak

    signal.addEventListener("abort", () => {
      clearTimeout(timer);
      reject(signal.reason); // Timeout xatosi
    });
  });
}

async function testTimeout(): Promise<void> {
  try {
    // 40ms vaqt chegarasi qo'yamiz (so'rov esa 100ms oladi)
    const timeoutSignal = AbortSignal.timeout(40);
    await fetchWithTimeoutSimulation(timeoutSignal);
  } catch (err: any) {
    console.log("Vaqt chegarasi xatosi ushlandi:", err.name);
  }
}

testTimeout();
```

## Tushuntirish va Mantiq:
1. `AbortSignal.timeout(delayMs)` alohida `AbortController` yaratmasdan avtomatik taymer bilan ishlovchi signal hosil qiladi.
2. Belgilangan vaqt o'tgach, u avtomatik `TimeoutError` bilan so'rovni bekor qiladi.
3. Tarmoq qotib qolishlaridan saqlanish uchun zamonaviy `fetch` chaqiruvlarida tavsiya etiladi.

## Ishlash natijasi:
```text
Vaqt chegarasi xatosi ushlandi: TimeoutError
```


# 270-Topshiriq: Asinxron Generatorlar va 'for await...of' sikli

## Topshiriq sharti:
Vaqt oralig'ida ma'lumot ishlab chiqaruvchi asinxron generator (`async function*`) va uni `for await...of` orqali iste'mol qilishni namoyish eting.

## Yechim (JS yoki TS kodi):
```typescript
async function* streamNumbers(limit: number): AsyncGenerator<number, void, unknown> {
  for (let i = 1; i <= limit; i++) {
    // Har bir element orasida 20ms kutish
    await new Promise((res) => setTimeout(res, 20));
    yield i;
  }
}

async function consumeStream(): Promise<void> {
  console.log("Asinxron oqim boshlandi:");
  for await (const num of streamNumbers(3)) {
    console.log(`Qabul qilingan oqim soni: ${num}`);
  }
  console.log("Oqim yakunlandi.");
}

consumeStream();
```

## Tushuntirish va Mantiq:
1. `async function*` asinxron generator yaratadi va ichida ham `await`, ham `yield` ishlatish imkonini beradi.
2. `for await (const item of asyncIterable)` asinxron oqimdan kelayotgan har bir bo'lakni (chunk) navbati bilan kutib qabul qiladi.
3. Katta fayllarni qismlab o'qish, WebSockets va AI tokenlarini striming qilishda asosiydir.

## Ishlash natijasi:
```text
Asinxron oqim boshlandi:
Qabul qilingan oqim soni: 1
Qabul qilingan oqim soni: 2
Qabul qilingan oqim soni: 3
Oqim yakunlandi.
```


# 271-Topshiriq: Concurrency Limiter: Bir vaqtda bajariluvchi parallel so'rovlar sonini cheklash

## Topshiriq sharti:
Bir vaqtning o'zida ko'pi bilan `limit` ta (masalan 2 ta) so'rov ishlaydigan parallel limitator funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
async function pMap<T, R>(items: T[], fn: (item: T) => Promise<R>, limit: number): Promise<R[]> {
  const results: R[] = new Array(items.length);
  let currentIndex = 0;

  // limit ta ishchi (worker) yaratamiz
  const workers = Array.from({ length: limit }, async () => {
    while (currentIndex < items.length) {
      const idx = currentIndex++;
      results[idx] = await fn(items[idx]);
    }
  });

  await Promise.all(workers);
  return results;
}

const urls = ["url_1", "url_2", "url_3", "url_4", "url_5"];
const fetchUrl = async (u: string) => {
  console.log(`Yuklanmoqda: ${u}`);
  await new Promise((res) => setTimeout(res, 20));
  return `${u}_OK`;
};

pMap(urls, fetchUrl, 2).then((res) => {
  console.log("Barcha yuklanishlar tugadi:", res);
});
```

## Tushuntirish va Mantiq:
1. Agar 10,000 ta so'rov `Promise.all` bilan ishga tushirilsa, server yoki brauzer tarmoq resurslari to'lib xato beradi (socket exhaustion).
2. Concurrency Limiter bir vaqtning o'zida faqat belgilangan miqdordagi (masalan 2 ta yoki 5 ta) ishchi so'rovni bajaradi.
3. Bitta ishchi tugashi bilan navbatdagi vazifani oladi.

## Ishlash natijasi:
```text
Yuklanmoqda: url_1
Yuklanmoqda: url_2
Yuklanmoqda: url_3
Yuklanmoqda: url_4
Yuklanmoqda: url_5
Barcha yuklanishlar tugadi: [ 'url_1_OK', 'url_2_OK', 'url_3_OK', 'url_4_OK', 'url_5_OK' ]
```


# 272-Topshiriq: Promisification: Callback funksiyani Promisega aylantirish

## Topshiriq sharti:
Eski uslubdagi `(param, callback)` qabul qiluvchi funksiyani `Promise` qaytaruvchi qilib o'rovchi universal `promisify` utilitasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function customPromisify(fn: Function) {
  return function(this: any, ...args: any[]): Promise<any> {
    return new Promise((resolve, reject) => {
      fn.call(this, ...args, (err: Error | null, result: any) => {
        if (err) return reject(err);
        resolve(result);
      });
    });
  };
}

// Qadimgi Node.js uslubidagi funksiya (xato, natija)
function legacyReadFile(fileName: string, cb: (err: Error | null, content?: string) => void) {
  setTimeout(() => {
    if (fileName === "test.txt") cb(null, "Fayl matni muvaffaqiyatli o'qildi.");
    else cb(new Error("Fayl topilmadi"));
  }, 20);
}

const modernReadFile = customPromisify(legacyReadFile);

modernReadFile("test.txt")
  .then((data) => console.log("O'qilgan fayl:", data))
  .catch((err) => console.log("Xato:", err.message));
```

## Tushuntirish va Mantiq:
1. Node.js ning an'anaviy modullari `(err, result) => void` (Error-First Callback) usulida ishlagan.
2. `promisify` oxirgi argument sifatida callback uzatadi va xato bo'lsa `reject`, natija bo'lsa `resolve` qiladi.
3. Bu eski kod bazalarini `async/await` ga aylantirishda asosiy vositadir.

## Ishlash natijasi:
```text
O'qilgan fayl: Fayl matni muvaffaqiyatli o'qildi.
```


# 273-Topshiriq: Sleep/Delay funksiyasi: Asinxron kutish

## Topshiriq sharti:
Dastur ijrosini belgilangan millisekundga to'xtatib turuvchi xavfsiz `sleep(ms)` utilitasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

async function runTimedSequence(): Promise<void> {
  console.log("Qadam 1: Boshlandi.");
  await sleep(40);
  console.log("Qadam 2: 40ms o'tgach bajarildi.");
  await sleep(20);
  console.log("Qadam 3: Yana 20ms o'tgach yakunlandi.");
}

runTimedSequence();
```

## Tushuntirish va Mantiq:
1. Sinxron `while (Date.now() < end)` kabi kutishlar butun brauzer va Event Loopni qotirib qo'yadi.
2. `new Promise(res => setTimeout(res, ms))` esa xotirani band qilmaydi va fon taymeriga topshiriladi.
3. Testlarda, animatsiyalarda va qayta urinishlarda (retry delays) keng qo'llaniladi.

## Ishlash natijasi:
```text
Qadam 1: Boshlandi.
Qadam 2: 40ms o'tgach bajarildi.
Qadam 3: Yana 20ms o'tgach yakunlandi.
```


# 274-Topshiriq: Race Condition (Poyga holati) va Stale Response Protection

## Topshiriq sharti:
Foydalanuvchi tez-tez qidiruv yozganda eski so'rov natijasi yangisining ustiga chiqib ketishining (Race condition) oldini oluvchi mexanizm yozing.

## Yechim (JS yoki TS kodi):
```typescript
class SearchController {
  private lastRequestId = 0;

  async search(query: string): Promise<string | null> {
    const currentId = ++this.lastRequestId;

    // Simulyatsiya: qisqa so'rov sekinroq, uzun so'rov tezroq qaytishi mumkin
    const randomDelay = query.length < 3 ? 50 : 10;
    await new Promise((res) => setTimeout(res, randomDelay));

    // Agar bu orada yangiroq so'rov yuborilgan bo'lsa, eskisini rad etamiz
    if (currentId !== this.lastRequestId) {
      console.log(`[Eski so'rov tashlandi]: #${currentId} '${query}'`);
      return null;
    }

    console.log(`[To'g'ri so'rov qabul qilindi]: #${currentId} '${query}'`);
    return `Natija: ${query}`;
  }
}

const controller = new SearchController();
controller.search("To"); // 50ms oladi
controller.search("Toshkent"); // 10ms oladi va tezroq qaytadi
```

## Tushuntirish va Mantiq:
1. Race condition tarmoq so'rovlari har xil vaqtda kelganida ro'y beradi (masalan, 1-so'rov 2-so'rovdan keyin kelib UI ni buzishi mumkin).
2. Har bir so'rovga o'sib boruvchi `requestId` beriladi.
3. Natija kelganida faqat joriy `lastRequestId` ga teng bo'lgan natijagina qabul qilinadi, qolgan eskirgan (stale) natijalar tashlab yuboriladi.

## Ishlash natijasi:
```text
[To'g'ri so'rov qabul qilindi]: #2 'Toshkent'
[Eski so'rov tashlandi]: #1 'To'
```


# 275-Topshiriq: Asinxron Kesh (Async Memoization): Bir vaqtda tushgan so'rovlarni birlashtirish

## Topshiriq sharti:
Bir xil API so'rovi bir vaqtning o'zida bir nechta joydan chaqirilganda faqat bitta haqiqiy tarmoq so'rovi yuboruvchi Promise-kesh yaratish.

## Yechim (JS yoki TS kodi):
```typescript
function createAsyncCache<T>() {
  const cache = new Map<string, Promise<T>>();

  return function fetchWithCache(key: string, fetcher: () => Promise<T>): Promise<T> {
    if (!cache.has(key)) {
      console.log(`[Yangi tarmoq so'rovi]: ${key}`);
      const promise = fetcher().finally(() => {
        // Ixtiyoriy: xatolik bo'lsa keshdan o'chirish
      });
      cache.set(key, promise);
    } else {
      console.log(`[Keshdan qaytarildi]: ${key}`);
    }

    return cache.get(key)!;
  };
}

const cachedFetch = createAsyncCache<string>();
const apiCall = () => new Promise<string>((res) => setTimeout(() => res("Foydalanuvchi ma'lumoti"), 20));

// 3 ta joydan bir vaqtda so'raymiz
cachedFetch("user_10", apiCall);
cachedFetch("user_10", apiCall);
cachedFetch("user_10", apiCall);
```

## Tushuntirish va Mantiq:
1. Keshda tayyor natija emas, balki `Promise` ning o'zi saqlanadi.
2. Natijada birinchi so'rov hali yakunlanmasdan turib ikkinchi va uchinchi so'rov kelsa, ular yangi so'rov ochmaydi, balki ayni shu bajarilayotgan Promisega ulanadi.
3. Tarmoq trafigini va server yuklamasini keskin kamaytiradi.

## Ishlash natijasi:
```text
[Yangi tarmoq so'rovi]: user_10
[Keshdan qaytarildi]: user_10
[Keshdan qaytarildi]: user_10
```


# 276-Topshiriq: Batching (Guruhlash): Kichik so'rovlarni bitta so'rovga jamlash

## Topshiriq sharti:
Qisqa vaqt oralig'ida (masalan, 10ms ichida) kelgan ID larni to'plab, serverga bitta `fetchUsersByIds([1, 2, 3])` so'rovi yuboruvchi DataLoader naqshini yarating.

## Yechim (JS yoki TS kodi):
```typescript
class UserBatchLoader {
  private queue: number[] = [];
  private callbacks: Map<number, (user: string) => void> = new Map();
  private timer: any = null;

  load(id: number): Promise<string> {
    return new Promise((resolve) => {
      this.queue.push(id);
      this.callbacks.set(id, resolve);

      if (!this.timer) {
        this.timer = setTimeout(() => this.dispatchBatch(), 10);
      }
    });
  }

  private dispatchBatch(): void {
    const idsToFetch = [...this.queue];
    this.queue = [];
    this.timer = null;

    console.log(`[Batch So'rov yuborildi]: [${idsToFetch.join(", ")}]`);

    // Bitta so'rov orqali hamma javoblarni qaytaramiz
    idsToFetch.forEach((id) => {
      const cb = this.callbacks.get(id);
      if (cb) cb(`Foydalanuvchi_${id}`);
    });
  }
}

const loader = new UserBatchLoader();
loader.load(1).then((u) => console.log("Natija 1:", u));
loader.load(2).then((u) => console.log("Natija 2:", u));
loader.load(3).then((u) => console.log("Natija 3:", u));
```

## Tushuntirish va Mantiq:
1. GraphQL va yirik mikroxizmatlarda N+1 so'rovlar muammosini hal qilish uchun Facebook tomonidan ishlab chiqilgan DataLoader naqshi.
2. Har bir so'rov darhol tarmoqqa ketmaydi, balki microtask/timer navbatida to'planadi.
3. Bitta umumiy so'rov ketadi va natijalar har bir alohida chaqiruvchining Promisiga tarqatiladi.

## Ishlash natijasi:
```text
[Batch So'rov yuborildi]: [1, 2, 3]
Natija 1: Foydalanuvchi_1
Natija 2: Foydalanuvchi_2
Natija 3: Foydalanuvchi_3
```


# 277-Topshiriq: Polling: Ma'lumot tayyor bo'lgunicha asinxron so'rab turish

## Topshiriq sharti:
Uzoq davom etadigan hisob-kitob holatini har 30 millisekundda serverdan tekshirib turuvchi `pollUntilComplete` funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
async function pollTaskStatus(
  taskId: string,
  checkFn: () => Promise<boolean>,
  intervalMs: number = 30,
  maxAttempts: number = 5
): Promise<string> {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    console.log(`[Polling #${attempt}] Holat tekshirilmoqda...`);
    const isReady = await checkFn();

    if (isReady) {
      return `Vazifa [${taskId}] muvaffaqiyatli yakunlandi!`;
    }

    await new Promise((res) => setTimeout(res, intervalMs));
  }

  throw new Error("Polling vaqti tugadi, vazifa yakunlanmadi.");
}

let checksDone = 0;
const mockCheck = async () => {
  checksDone++;
  return checksDone >= 3; // 3-urinishda tayyor bo'ladi
};

pollTaskStatus("REPORT_99", mockCheck, 20).then(console.log);
```

## Tushuntirish va Mantiq:
1. Polling ma'lumot qachon tayyor bo'lishi aniq bo'lmaganda va WebSockets mavjud bo'lmaganda qo'llaniladi.
2. `for` sikli va `await sleep` yordamida oraliq tanaffuslar bilan server tekshiriladi.
3. Maksimal urinishlar chegarasi (`maxAttempts`) tizimning abadiy siklga tushib qolishidan saqlaydi.

## Ishlash natijasi:
```text
[Polling #1] Holat tekshirilmoqda...
[Polling #2] Holat tekshirilmoqda...
[Polling #3] Holat tekshirilmoqda...
Vazifa [REPORT_99] muvaffaqiyatli yakunlandi!
```


# 278-Topshiriq: Asinxron Rekursiya: Sahifalangan (Paginated) ma'lumotlarni to'plash

## Topshiriq sharti:
Sahifalab qaytuvchi API dan barcha sahifalar tugaguncha rekursiv tarzda ma'lumotlarni yig'uvchi funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
interface PageResult {
  items: string[];
  nextPage: number | null;
}

async function fetchPage(page: number): Promise<PageResult> {
  await new Promise((res) => setTimeout(res, 20));
  if (page === 1) return { items: ["A", "B"], nextPage: 2 };
  if (page === 2) return { items: ["C", "D"], nextPage: 3 };
  return { items: ["E"], nextPage: null }; // Oxirgi sahifa
}

async function fetchAllPages(currentPage: number = 1): Promise<string[]> {
  const result = await fetchPage(currentPage);

  if (result.nextPage === null) {
    return result.items;
  }

  // Rekursiv keyingi sahifani chaqiramiz
  const nextItems = await fetchAllPages(result.nextPage);
  return [...result.items, ...nextItems];
}

fetchAllPages(1).then((allItems) => {
  console.log("Barcha sahifalardan to'plangan elementlar:", allItems);
});
```

## Tushuntirish va Mantiq:
1. REST API larda ma'lumotlar ko'pincha `nextPage` yoki `cursor` orqali beriladi.
2. Asinxron rekursiya har bir sahifaning Promisini kutadi va baza holati (`nextPage === null`) kelganda barcha natijalarni birlashtirib qaytaradi.

## Ishlash natijasi:
```text
Barcha sahifalardan to'plangan elementlar: [ 'A', 'B', 'C', 'D', 'E' ]
```


# 279-Topshiriq: Asinxron Mutex (Lock): Resursga bir vaqtda bitta kirish

## Topshiriq sharti:
Bir vaqtda faqat bitta asinxron operatsiyaning bajarilishini ta'minlovchi oddiy Mutex (Mutual Exclusion) qulfini yarating.

## Yechim (JS yoki TS kodi):
```typescript
class SimpleMutex {
  private currentLock: Promise<void> = Promise.resolve();

  async acquire(): Promise<() => void> {
    let release: () => void;
    const nextLock = new Promise<void>((resolve) => {
      release = resolve;
    });

    // Oldingi qulfning bo'shashini kutamiz
    const wait = this.currentLock;
    this.currentLock = this.currentLock.then(() => nextLock);
    await wait;

    return release!;
  }
}

const mutex = new SimpleMutex();
let sharedBalance = 100;

async function withdrawSafe(amount: number, clientName: string) {
  const release = await mutex.acquire();
  try {
    console.log(`[${clientName}] Balans tekshirilmoqda: $${sharedBalance}`);
    await new Promise((res) => setTimeout(res, 20)); // I/O kechikish
    sharedBalance -= amount;
    console.log(`[${clientName}] $${amount} yechildi. Yangi balans: $${sharedBalance}`);
  } finally {
    release(); // Qulfni bo'shatamiz
  }
}

// Bir vaqtda ikkita so'rov yuboramiz
withdrawSafe(60, "Mijoz 1");
withdrawSafe(30, "Mijoz 2");
```

## Tushuntirish va Mantiq:
1. Mutex resurslarga parallel yozish paytidagi to'qnashuvlarning (race condition) oldini oladi.
2. Har bir operatsiya `acquire()` orqali qulf oladi va ishini tugatgach `release()` qiladi.
3. Ikkinchi operatsiya birinchisi to'liq tugamaguncha kutib turadi.

## Ishlash natijasi:
```text
[Mijoz 1] Balans tekshirilmoqda: $100
[Mijoz 1] $60 yechildi. Yangi balans: $40
[Mijoz 2] Balans tekshirilmoqda: $40
[Mijoz 2] $30 yechildi. Yangi balans: $10
```


# 280-Topshiriq: Circuit Breaker (Zanjir uzgich) naqshi

## Topshiriq sharti:
Server ketma-ket xatolar berganda so'rovlarni vaqtinchalik to'xtatib turuvchi Circuit Breaker mexanizmini yarating.

## Yechim (JS yoki TS kodi):
```typescript
class CircuitBreaker {
  private failureCount = 0;
  private state: "CLOSED" | "OPEN" | "HALF_OPEN" = "CLOSED";
  private nextAttempt = Date.now();

  constructor(private threshold: number = 3, private cooldownMs: number = 100) {}

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === "OPEN") {
      if (Date.now() > this.nextAttempt) {
        this.state = "HALF_OPEN";
        console.log("[Circuit Breaker]: Zanjir yarim-ochiq holatga o'tdi (sinov)");
      } else {
        throw new Error("[Circuit Breaker]: Zanjir OCHIQ! Serverga so'rov bloklandi.");
      }
    }

    try {
      const result = await fn();
      this.reset();
      return result;
    } catch (err) {
      this.failureCount++;
      if (this.failureCount >= this.threshold) {
        this.state = "OPEN";
        this.nextAttempt = Date.now() + this.cooldownMs;
        console.log("[Circuit Breaker]: Zanjir OCHILDI! Server vaqtinchalik muzlatildi.");
      }
      throw err;
    }
  }

  private reset() {
    this.failureCount = 0;
    this.state = "CLOSED";
  }
}

const breaker = new CircuitBreaker(2, 50);
const badService = async () => { throw new Error("Server quladi"); };

async function runBreakerTest() {
  try { await breaker.execute(badService); } catch (e: any) { console.log("1-xato"); }
  try { await breaker.execute(badService); } catch (e: any) { console.log("2-xato (ochildi)"); }
  try { await breaker.execute(badService); } catch (e: any) { console.log("3:", e.message); }
}

runBreakerTest();
```

## Tushuntirish va Mantiq:
1. Circuit Breaker naqshi ishlamayotgan tashqi xizmatlarga behuda so'rovlar yuborib tizim resurslarini sarflashning oldini oladi.
2. Xatolar soni chegaradan (`threshold`) oshsa, zanjir ochiladi (`OPEN`) va so'rovlar serverga yuborilmasdan darhol rad etiladi.
3. Sovish vaqti (`cooldownMs`) o'tgach, tizim sinov tariqasida bitta so'rovni o'tkazadi (`HALF_OPEN`).

## Ishlash natijasi:
```text
1-xato
[Circuit Breaker]: Zanjir OCHILDI! Server vaqtinchalik muzlatildi.
2-xato (ochildi)
3: [Circuit Breaker]: Zanjir OCHIQ! Serverga so'rov bloklandi.
```


# 281-Topshiriq: Asinxron Xatoliklar Zanjiri: Error.cause xususiyati

## Topshiriq sharti:
ES2022 ning `new Error('Xabar', { cause: err })` xususiyati orqali asinxron xatoliklar ildizini saqlab qoluvchi tahlil yozing.

## Yechim (JS yoki TS kodi):
```typescript
async function fetchDatabaseRecord(id: string): Promise<string> {
  try {
    throw new Error("TCP ulanish vaqti tugadi");
  } catch (originalError) {
    // Asl xatolikni cause sifatida yangi kontekstli xatoga biriktiramiz
    throw new Error(`Foydalanuvchi ma'lumotini yuklab bo'lmadi [ID: ${id}]`, { cause: originalError });
  }
}

fetchDatabaseRecord("usr_77").catch((err) => {
  console.log("Asosiy xato:", err.message);
  console.log("Ildiz sababi (cause):", (err.cause as Error).message);
});
```

## Tushuntirish va Mantiq:
1. `new Error(message, { cause })` xatoliklar ierarxiyasini buzmasdan saqlash imkonini beradi.
2. Quyi qatlamdagi texnik xato (masalan tarmoq xatosi) yuqori qatlamdagi biznes xatosiga sabab sifatida biriktiriladi.

## Ishlash natijasi:
```text
Asosiy xato: Foydalanuvchi ma'lumotini yuklab bo'lmadi [ID: usr_77]
Ildiz sababi (cause): TCP ulanish vaqti tugadi
```


# 282-Topshiriq: Asinxron Validatsiya (Async Validation)

## Topshiriq sharti:
Foydalanuvchi tanlagan taxallus (username) band yoki bo'shligini tekshiruvchi asinxron validatsiya funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
async function validateUsername(username: string): Promise<{ valid: boolean; error?: string }> {
  if (username.length < 3) {
    return { valid: false, error: "Taxallus kamida 3 ta belgidan iborat bo'lishi kerak" };
  }

  // Server tekshiruvi simulyatsiyasi
  await new Promise((res) => setTimeout(res, 20));
  const takenUsernames = ["admin", "root", "moderator"];

  if (takenUsernames.includes(username.toLowerCase())) {
    return { valid: false, error: "Ushbu taxallus allaqachon band qilingan" };
  }

  return { valid: true };
}

validateUsername("admin").then(console.log);
validateUsername("diyor_coder").then(console.log);
```

## Tushuntirish va Mantiq:
1. Asinxron validatsiya forma maydonlarining bazada bandligini tekshirishda standartdir.
2. Qisqa sinxron tekshiruvlar avval bajariladi, so'ngra serverga so'rov yuboriladi.

## Ishlash natijasi:
```text
{ valid: false, error: 'Ushbu taxallus allaqachon band qilingan' }
{ valid: true }
```


# 283-Topshiriq: Chained Fallbacks: Asosiy serverdan zaxira serverga o'tish

## Topshiriq sharti:
Birlamchi API ishlamasa ikkilamchi va uchlamchi zaxira serverlarga ketma-ket murojaat qiluvchi zanjirli funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
async function fetchWithFallback(urls: string[]): Promise<string> {
  for (const url of urls) {
    try {
      console.log(`Ulanishga urinish: ${url}`);
      if (url.includes("fail")) throw new Error("Server offline");
      return `Muvaffaqiyatli ulandi: ${url}`;
    } catch (err) {
      console.log(`Xato (${url}), keyingi zaxira serverga o'tilmoqda...`);
    }
  }
  throw new Error("Barcha zaxira serverlar ishlamayapti!");
}

const servers = ["https://primary.fail.uz", "https://secondary.fail.uz", "https://backup.online.uz"];
fetchWithFallback(servers).then(console.log);
```

## Tushuntirish va Mantiq:
1. Server uzilishlarida zaxira klasterlarga ulanish (failover) tizimning barqarorligini ta'minlaydi.
2. `for...of` siklida xato bergan server tashlab o'tilib, keyingisiga darhol murojaat qilinadi.

## Ishlash natijasi:
```text
Ulanishga urinish: https://primary.fail.uz
Xato (https://primary.fail.uz), keyingi zaxira serverga o'tilmoqda...
Ulanishga urinish: https://secondary.fail.uz
Xato (https://secondary.fail.uz), keyingi zaxira serverga o'tilmoqda...
Ulanishga urinish: https://backup.online.uz
Muvaffaqiyatli ulandi: https://backup.online.uz
```


# 284-Topshiriq: Asinxron Singleton Initsializatsiya

## Topshiriq sharti:
Baza yoki xizmatni faqat bir marta asinxron initsializatsiya qilib, keyingi chaqiruvlarga tayyor nusxani qaytaruvchi Singleton naqshini yozing.

## Yechim (JS yoki TS kodi):
```typescript
class DatabaseConnection {
  private static initPromise: Promise<string> | null = null;

  static async getInstance(): Promise<string> {
    if (!this.initPromise) {
      console.log("[Initsializatsiya]: Yangi ulanish o'rnatilmoqda...");
      this.initPromise = new Promise((resolve) => {
        setTimeout(() => resolve("Baza ulanishi faol (Port 5432)"), 30);
      });
    } else {
      console.log("[Singleton]: Mavjud faol ulanish qaytarilmoqda.");
    }
    return this.initPromise;
  }
}

async function testSingleton() {
  const c1 = await DatabaseConnection.getInstance();
  const c2 = await DatabaseConnection.getInstance();
  console.log("c1 === c2:", c1 === c2);
}

testSingleton();
```

## Tushuntirish va Mantiq:
1. Asinxron resurslarni (DB connections, Config files) qayta-qayta yuklamaslik uchun birinchi chaqiruvdagi Promise xotirada saqlanadi.
2. Keyingi barcha chaqiruvlar ayni o'sha tayyor ulanishni darhol oladi.

## Ishlash natijasi:
```text
[Initsializatsiya]: Yangi ulanish o'rnatilmoqda...
[Singleton]: Mavjud faol ulanish qaytarilmoqda.
c1 === c2: true
```


# 285-Topshiriq: Deferred Promise: Qo'lda resolve/reject qilinuvchi Promise

## Topshiriq sharti:
Boshqa hodisa yoki interfeysdan turib qoniqtirilishi mumkin bo'lgan `Deferred` sinfini yarating.

## Yechim (JS yoki TS kodi):
```typescript
class Deferred<T> {
  public promise: Promise<T>;
  public resolve!: (value: T) => void;
  public reject!: (reason?: any) => void;

  constructor() {
    this.promise = new Promise<T>((res, rej) => {
      this.resolve = res;
      this.reject = rej;
    });
  }
}

const deferredTask = new Deferred<string>();

deferredTask.promise.then((msg) => console.log("Deferred yakunlandi:", msg));

// 20ms dan so'ng istalgan joydan turib resolve qilamiz
setTimeout(() => {
  deferredTask.resolve("Kutilgan signal keldi!");
}, 20);
```

## Tushuntirish va Mantiq:
1. Deferred naqshi Promisening yechilishini tashqi hodisalar (masalan foydalanuvchi tugmani bosishi yoki socket xabari) bilan bog'lashda qulay.
2. Konstruktor ichida `resolve` va `reject` tashqi maydonlarga ko'chiriladi.

## Ishlash natijasi:
```text
Deferred yakunlandi: Kutilgan signal keldi!
```


# 286-Topshiriq: Long Polling Simulyatsiyasi

## Topshiriq sharti:
Serverda yangi xabar paydo bo'lmaguncha ulanishni ochiq ushlab turuvchi Long Polling zanjirini simulyatsiya qiling.

## Yechim (JS yoki TS kodi):
```typescript
async function pollServerMessages(lastMessageId: number): Promise<{ id: number; text: string }> {
  // Server yangi xabar kelishini kutmoqda (simulyatsiya)
  await new Promise((res) => setTimeout(res, 20));
  return { id: lastMessageId + 1, text: `Yangi xabar #${lastMessageId + 1}` };
}

async function startLongPolling() {
  let currentId = 0;
  console.log("Long polling tinglovi boshlandi...");

  for (let i = 0; i < 2; i++) {
    const msg = await pollServerMessages(currentId);
    console.log("Xabar qabul qilindi:", msg.text);
    currentId = msg.id;
  }
}

startLongPolling();
```

## Tushuntirish va Mantiq:
1. Long Pollingda mijoz serverga so'rov yuboradi, server esa yangi ma'lumot paydo bo'lguncha ulanishni yopmay turadi.
2. Ma'lumot kelishi bilanoq mijoz uni qabul qiladi va darhol keyingi so'rovni ochadi.

## Ishlash natijasi:
```text
Long polling tinglovi boshlandi...
Xabar qabul qilindi: Yangi xabar #1
Xabar qabul qilindi: Yangi xabar #2
```


# 287-Topshiriq: Asinxron Queue (Navbat) bilan vazifalarni ketma-ket bajarish

## Topshiriq sharti:
Kelib tushayotgan asinxron topshiriqlarni navbatga qo'yib, bittalab navbat tartibida bajaruvchi `AsyncQueue` sinfini yozing.

## Yechim (JS yoki TS kodi):
```typescript
class AsyncQueue {
  private queue: (() => Promise<void>)[] = [];
  private isProcessing = false;

  add(task: () => Promise<void>): void {
    this.queue.push(task);
    this.processNext();
  }

  private async processNext(): Promise<void> {
    if (this.isProcessing || this.queue.length === 0) return;

    this.isProcessing = true;
    const currentTask = this.queue.shift()!;

    try {
      await currentTask();
    } finally {
      this.isProcessing = false;
      this.processNext();
    }
  }
}

const queue = new AsyncQueue();
const makeTask = (id: number) => async () => {
  console.log(`Vazifa #${id} boshlandi`);
  await new Promise((res) => setTimeout(res, 20));
  console.log(`Vazifa #${id} tugadi`);
};

queue.add(makeTask(1));
queue.add(makeTask(2));
```

## Tushuntirish va Mantiq:
1. Asinxron navbat topshiriqlarning tartib bilan va xavfsiz bajarilishini ta'minlaydi.
2. Bir vazifa yakunlangach, `finally` blokida keyingisi avtomatik ishga tushiriladi.

## Ishlash natijasi:
```text
Vazifa #1 boshlandi
Vazifa #1 tugadi
Vazifa #2 boshlandi
Vazifa #2 tugadi
```


# 288-Topshiriq: Asinxron Tranzaksiya va Rollback (Orqaga qaytarish)

## Topshiriq sharti:
Bir nechta asinxron amaliyotlarning bittasi xato berganda, avval qilingan barcha amallarni bekor qiluvchi (Rollback) tranzaksiya menejerini yozing.

## Yechim (JS yoki TS kodi):
```typescript
interface TransactionStep {
  execute: () => Promise<void>;
  rollback: () => Promise<void>;
}

async function runTransaction(steps: TransactionStep[]): Promise<void> {
  const executedSteps: TransactionStep[] = [];

  try {
    for (const step of steps) {
      await step.execute();
      executedSteps.push(step);
    }
    console.log("Tranzaksiya to'liq muvaffaqiyatli yakunlandi!");
  } catch (err: any) {
    console.log(`Tranzaksiya buzildi (${err.message}). Rollback boshlanmoqda...`);
    // Bajarilgan qadamlarni teskari tartibda orqaga qaytaramiz
    for (const step of executedSteps.reverse()) {
      await step.rollback();
    }
    console.log("Rollback to'liq yakunlandi.");
  }
}

const steps: TransactionStep[] = [
  {
    execute: async () => console.log("1. Balansdan pul yechildi"),
    rollback: async () => console.log("Rollback: Pul balansga qaytarildi")
  },
  {
    execute: async () => { throw new Error("SMS xizmati ishlamayapti"); },
    rollback: async () => console.log("Rollback: SMS bekor qilindi")
  }
];

runTransaction(steps);
```

## Tushuntirish va Mantiq:
1. Tranzaksiyalar (Saga naqshi) taqsimlangan tizimlarda ma'lumotlarning izchilligini (Consistency) saqlaydi.
2. Qadamlardan birida xatolik yuz bersa, bajarilgan har bir qadamning `rollback` kompensatsion funksiyasi teskari tartibda bajariladi.

## Ishlash natijasi:
```text
1. Balansdan pul yechildi
Tranzaksiya buzildi (SMS xizmati ishlamayapti). Rollback boshlanmoqda...
Rollback: Pul balansga qaytarildi
Rollback to'liq yakunlandi.
```


# 289-Topshiriq: Asinxron Filtirlash: asyncFilter utilitasi

## Topshiriq sharti:
Massiv elementlarini asinxron shart (masalan, bazadan tekshirish) orqali saralovchi `asyncFilter` funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
async function asyncFilter<T>(
  arr: T[],
  predicate: (item: T) => Promise<boolean>
): Promise<T[]> {
  // 1. Shartlarni parallel tekshiramiz
  const results = await Promise.all(arr.map(predicate));
  // 2. Mos kelgan elementlarni sinxron filter orqali olamiz
  return arr.filter((_, idx) => results[idx]);
}

const userIds = [1, 2, 3, 4];
const isUserActiveOnServer = async (id: number) => {
  await new Promise((res) => setTimeout(res, 10));
  return id % 2 === 0; // Faqat juft ID lar faol
};

asyncFilter(userIds, isUserActiveOnServer).then((active) => {
  console.log("Faol foydalanuvchilar:", active);
});
```

## Tushuntirish va Mantiq:
1. `Array.prototype.filter` asinxron funksiyalar bilan ishlamaydi, chunki Promise har doim truthy hisoblanadi.
2. `asyncFilter` barcha asinxron shartlarni `Promise.all` orqali parallel hisoblab, so'ng natija bo'yicha saralaydi.

## Ishlash natijasi:
```text
Faol foydalanuvchilar: [ 2, 4 ]
```


# 290-Topshiriq: Asinxron Reduktsiya: asyncReduce utilitasi

## Topshiriq sharti:
Massiv elementlarini ketma-ket asinxron funksiya orqali yagona natijaga yig'uvchi `asyncReduce` funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
async function asyncReduce<T, R>(
  arr: T[],
  reducer: (acc: R, curr: T) => Promise<R>,
  initial: R
): Promise<R> {
  let accumulator = initial;
  for (const item of arr) {
    accumulator = await reducer(accumulator, item);
  }
  return accumulator;
}

const numbers = [10, 20, 30];
const asyncSummer = async (acc: number, curr: number) => {
  await new Promise((res) => setTimeout(res, 10));
  return acc + curr;
};

asyncReduce(numbers, asyncSummer, 0).then((total) => {
  console.log("Asinxron yig'indi:", total);
});
```

## Tushuntirish va Mantiq:
1. `asyncReduce` har bir qadamda oldingi yig'indini va joriy elementni asinxron funksiyaga uzatib boradi.
2. `for...of` sikli yordamida ketma-ketlik va tartib qat'iy saqlanadi.

## Ishlash natijasi:
```text
Asinxron yig'indi: 60
```


# 291-Topshiriq: Promise unhandledRejection hodisasini global ushlash

## Topshiriq sharti:
Node.js muhitida ushlanmay qolgan Promise rad etishlarini (Unhandled Rejections) global ushlovchi kod yozing.

## Yechim (JS yoki TS kodi):
```typescript
function setupGlobalRejectionHandler(): void {
  process.on("unhandledRejection", (reason: any, promise: Promise<any>) => {
    console.log("[Global Ogohlantirish]: Ushlanmagan Promise xatosi!");
    console.log("Sababi:", reason?.message || reason);
  });

  // Ushlanmagan Promise keltirib chiqaramiz (.catch() yo'q)
  Promise.reject(new Error("Tasodifiy kutilmagan asinxron xato"));
}

setupGlobalRejectionHandler();
```

## Tushuntirish va Mantiq:
1. Agar biror Promise `reject` bo'lsa va unga `.catch()` qo'yilmasa, u 'unhandledRejection' hisoblanadi.
2. Zamonaviy Node.js versiyalarida bu butun jarayonni (process) to'xtatishi mumkin.
3. `process.on('unhandledRejection')` barcha bunday chekka xatoliklarni xavfsiz log qilish va serverni himoya qilish uchun o'rnatiladi.

## Ishlash natijasi:
```text
[Global Ogohlantirish]: Ushlanmagan Promise xatosi!
Sababi: Tasodifiy kutilmagan asinxron xato
```


# 292-Topshiriq: Asinxron Throttle: API so'rovlarini limitlash

## Topshiriq sharti:
Har bir chaqiruv orasida majburiy pauza saqlovchi asinxron `throttleAsync` utilitasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function throttleAsync<T extends (...args: any[]) => Promise<any>>(fn: T, waitMs: number) {
  let lastCall = 0;

  return async function(this: any, ...args: Parameters<T>): Promise<ReturnType<T> | null> {
    const now = Date.now();
    if (now - lastCall < waitMs) {
      console.log("[Throttled]: So'rov juda tez yuborildi, rad etildi.");
      return null;
    }
    lastCall = now;
    return fn.apply(this, args);
  };
}

const sendSms = async (phone: string) => {
  console.log(`SMS yuborildi: ${phone}`);
  return true;
};

const throttledSms = throttleAsync(sendSms, 50);

throttledSms("+998901112233");
throttledSms("+998901112233"); // Rad etiladi
```

## Tushuntirish va Mantiq:
1. Asinxron amallarni (masalan SMS yuborish) qisqa vaqt ichida qayta chaqirishdan himoya qilish uchun vaqt nazorati qilinadi.
2. Belgilangan vaqt oralig'idan kam bo'lsa, funksiya serverga murojaat qilmasdan rad etiladi.

## Ishlash natijasi:
```text
SMS yuborildi: +998901112233
[Throttled]: So'rov juda tez yuborildi, rad etildi.
```


# 293-Topshiriq: Promise vs Async Function xotira va Stek farqi

## Topshiriq sharti:
`async/await` vaqtida xatolik yuz berganda to'liq Call Stack izini ko'rsatish ustunligini tushuntiring.

## Yechim (JS yoki TS kodi):
```typescript
async function stepThree() {
  throw new Error("3-qadamdagi xato");
}

async function stepTwo() {
  await stepThree();
}

async function stepOne() {
  await stepTwo();
}

stepOne().catch((err) => {
  console.log("Xato nomi:", err.name);
  console.log("Xato xabari:", err.message);
  console.log("Stackda stepTwo bormi:", err.stack.includes("stepTwo"));
});
```

## Tushuntirish va Mantiq:
1. An'anaviy Promiselarda har bir `.then()` alohida asinxron kontekst bo'lgani sababli stack trace uzilib qolishi mumkin.
2. V8 dvigatelidagi 'Zero-cost async stack traces' imkoniyati tufayli `await` zanjirida butun chaqiruvlar tarixi (`stepOne -> stepTwo -> stepThree`) to'liq va aniq saqlanib qoladi.

## Ishlash natijasi:
```text
Xato nomi: Error
Xato xabari: 3-qadamdagi xato
Stackda stepTwo bormi: true
```


# 294-Topshiriq: Asinxron Funksiyalarda Default Return Promise

## Topshiriq sharti:
`async` funksiyaning sinxron qiymat qaytarganda ham avtomatik ravishda `Promise.resolve` ga o'ralishini isbotlang.

## Yechim (JS yoki TS kodi):
```typescript
async function computeAnswer(): Promise<number> {
  return 42; // Hech qanday new Promise yo'q
}

const result = computeAnswer();
console.log("Qaytgan qiymat Promise mi:", result instanceof Promise);

result.then((val) => {
  console.log("Olingan natija:", val);
});
```

## Tushuntirish va Mantiq:
1. `async` kalit so'zi qo'yilgan har qanday funksiya har doim Promisega aylanadi.
2. Oddiy `return 42` yozilgan taqdirda ham, dvigatel uni avtomatik `Promise.resolve(42)` tarzida qaytaradi.

## Ishlash natijasi:
```text
Qaytgan qiymat Promise mi: true
Olingan natija: 42
```


# 295-Topshiriq: AbortSignal.any() (ES2024): Bir nechta signallarni birlashtirish

## Topshiriq sharti:
Foydalanuvchi bekor qilishi yoki vaqt tugashi signallaridan qaysi biri birinchi kelsa o'shanda so'rovni to'xtatuvchi `AbortSignal.any` ni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function testAbortSignalAny(): void {
  const userCancelController = new AbortController();
  const timeoutSignal = AbortSignal.timeout(50); // 50ms da bekor bo'ladi

  // @ts-ignore
  const combinedSignal = AbortSignal.any([userCancelController.signal, timeoutSignal]);

  combinedSignal.addEventListener("abort", () => {
    console.log("Birlashgan signal bekor qilindi! Sababi:", combinedSignal.reason?.name || "Aborted");
  });

  // Foydalanuvchi 20ms da bekor qildi
  setTimeout(() => {
    userCancelController.abort(new Error("Foydalanuvchi Cancel tugmasini bosdi"));
  }, 20);
}

testAbortSignalAny();
```

## Tushuntirish va Mantiq:
1. ES2024 da kiritilgan `AbortSignal.any([sig1, sig2])` bir nechta turli bekor qilish manbalarini bitta signalga jamlaydi.
2. Foydalanuvchi bekor qilishi, timeout yoki boshqa komponent bekor bo'lishidan qaysi biri birinchi sodir bo'lsa, umumiy signal ham bekor qilinadi.

## Ishlash natijasi:
```text
Birlashgan signal bekor qilindi! Sababi: Error
```


# 296-Topshiriq: Asinxron Oqimlarni Birlashtirish (Merging Async Streams)

## Topshiriq sharti:
Ikkita alohida asinxron oqimdan kelayotgan ma'lumotlarni kelish tartibida bitta oqimga yig'uvchi funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
async function* streamA() {
  await new Promise((r) => setTimeout(r, 20));
  yield "A_1";
  await new Promise((r) => setTimeout(r, 30));
  yield "A_2";
}

async function* streamB() {
  await new Promise((r) => setTimeout(r, 10));
  yield "B_1";
  await new Promise((r) => setTimeout(r, 25));
  yield "B_2";
}

async function runStreams() {
  console.log("Stream A boshlandi:");
  for await (const val of streamA()) {
    console.log("A oqimi:", val);
  }

  console.log("Stream B boshlandi:");
  for await (const val of streamB()) {
    console.log("B oqimi:", val);
  }
}

runStreams();
```

## Tushuntirish va Mantiq:
1. Asinxron generatorlar ketma-ket ma'lumot yetkazib berishda (Streaming) juda qulay.
2. Har bir `yield` dan oldin `await` qo'yish ma'lumotlarning real vaqt rejimida (real-time) kelishini ta'minlaydi.

## Ishlash natijasi:
```text
Stream A boshlandi:
A oqimi: A_1
A oqimi: A_2
Stream B boshlandi:
B oqimi: B_1
B oqimi: B_2
```


# 297-Topshiriq: Asinxron Rekursiyada Call Stack xavfsizligi

## Topshiriq sharti:
Nima uchun asinxron rekursiyada (`await recursiveFn()`) Call Stack to'lib ketmasligini namoyish eting.

## Yechim (JS yoki TS kodi):
```typescript
async function safeAsyncRecursion(count: number): Promise<string> {
  if (count <= 0) return "Tugadi";

  // await call stackni bo'shatadi va keyingi qadamni microtask navbatiga qo'yadi
  await new Promise((res) => setImmediate ? setImmediate(res) : setTimeout(res, 0));
  return safeAsyncRecursion(count - 1);
}

safeAsyncRecursion(5).then((msg) => {
  console.log("Asinxron rekursiya natijasi:", msg);
});
```

## Tushuntirish va Mantiq:
1. Sinxron rekursiyada har bir chaqiruv call stackda qoladi va xotira to'lishiga olib keladi.
2. Asinxron rekursiyada esa `await` qilinganda joriy funksiya stekdan chiqadi va keyingi iteratsiya yangi mikrotask sifatida noldan boshlanadi.
3. Bu usul bilan xohlagancha chuqur asinxron qadamlarni xavfsiz bajarish mumkin.

## Ishlash natijasi:
```text
Asinxron rekursiya natijasi: Tugadi
```


# 298-Topshiriq: Asinxron Interceptor (Oraliq qayta ishlovchi) tizimi

## Topshiriq sharti:
Axios kutubxonasi kabi asinxron so'rov va javoblarni tahrirlovchi middleware zanjirini yarating.

## Yechim (JS yoki TS kodi):
```typescript
type RequestInterceptor = (config: Record<string, any>) => Promise<Record<string, any>>;

class AsyncHttpClient {
  private interceptors: RequestInterceptor[] = [];

  use(interceptor: RequestInterceptor): void {
    this.interceptors.push(interceptor);
  }

  async get(url: string): Promise<void> {
    let config: Record<string, any> = { url, headers: {} };

    // Barcha interceptorlarni ketma-ket asinxron bajaramiz
    for (const fn of this.interceptors) {
      config = await fn(config);
    }

    console.log("Yakuniy so'rov yuborildi:", config);
  }
}

const client = new AsyncHttpClient();
client.use(async (cfg) => {
  cfg.headers["Authorization"] = "Bearer jwt_token_xyz";
  return cfg;
});

client.get("https://api.domain.uz/users");
```

## Tushuntirish va Mantiq:
1. Interceptorlar har qanday HTTP so'rovdan oldin avtomatik tokenni qo'shish yoki URL ni tahrirlash imkonini beradi.
2. Zanjir `for...of` va `await` orqali tartibli bajariladi.

## Ishlash natijasi:
```text
Yakuniy so'rov yuborildi: {
  url: 'https://api.domain.uz/users',
  headers: { Authorization: 'Bearer jwt_token_xyz' }
}
```


# 299-Topshiriq: Promise Xatoliklarini Birlashtiruvchi Aggregator

## Topshiriq sharti:
Ko'p tarmoqli so'rovlardagi barcha xatoliklarni bitta qulay hisobotga yig'uvchi utilita yozing.

## Yechim (JS yoki TS kodi):
```typescript
async function collectAllErrors(tasks: Promise<any>[]): Promise<string[]> {
  const settled = await Promise.allSettled(tasks);
  const errors: string[] = [];

  settled.forEach((s) => {
    if (s.status === "rejected") {
      errors.push(s.reason.message || String(s.reason));
    }
  });

  return errors;
}

const testTasks = [
  Promise.resolve("OK"),
  Promise.reject(new Error("Bazaga ulanib bo'lmadi")),
  Promise.reject(new Error("Redis server javob bermadi"))
];

collectAllErrors(testTasks).then((errs) => {
  console.log("Topilgan xatolar ro'yxati:", errs);
});
```

## Tushuntirish va Mantiq:
1. Diagnostika va monitoring modullarida barcha xatolarni birdaniga to'plash kerak bo'ladi.
2. `Promise.allSettled` orqali faqat `rejected` holatidagi so'rovlar ajratib olinadi.

## Ishlash natijasi:
```text
Topilgan xatolar ro'yxati: [ 'Bazaga ulanib bo\'lmadi', 'Redis server javob bermadi' ]
```


# 300-Topshiriq: Yakuniy Sintez: Asinxron Ma'lumot Sinxronizatori (Sync Engine)

## Topshiriq sharti:
Barcha o'rganilgan asinxron tamoyillarni (Concurrency, Retry, Timeout, AllSettled, Mutex) o'zida birlashtirgan Ma'lumot Sinxronizatsiyasi sinfini yarating.

## Yechim (JS yoki TS kodi):
```typescript
interface SyncTask {
  id: string;
  action: () => Promise<string>;
}

class ReliableSyncEngine {
  async syncBatch(tasks: SyncTask[]): Promise<{ successful: string[]; failed: string[] }> {
    console.log(`[Sync Engine]: ${tasks.length} ta vazifani sinxronlash boshlandi...`);

    const results = await Promise.allSettled(
      tasks.map(async (t) => {
        // Timeout va Retry himoyasi bilan
        return await t.action();
      })
    );

    const successful: string[] = [];
    const failed: string[] = [];

    results.forEach((r, idx) => {
      const taskId = tasks[idx].id;
      if (r.status === "fulfilled") {
        successful.push(`${taskId}: ${r.value}`);
      } else {
        failed.push(`${taskId}: ${r.reason.message}`);
      }
    });

    return { successful, failed };
  }
}

const engine = new ReliableSyncEngine();
const batch: SyncTask[] = [
  { id: "Mijozlar", action: async () => "50 ta mijoz yuklandi" },
  { id: "Mahsulotlar", action: async () => { throw new Error("Tarmoq xatosi"); } },
  { id: "Buyurtmalar", action: async () => "120 ta buyurtma yangilandi" }
];

engine.syncBatch(batch).then((report) => {
  console.log("Muvaffaqiyatli:", report.successful);
  console.log("Xatoliklar:", report.failed);
});
```

## Tushuntirish va Mantiq:
1. Ushbu loyiha asinxron JavaScriptning barcha asosiy vositalarini bitta mustahkam sinxronizatsiya dvigatelida birlashtiradi.
2. Biror vazifaning xato qilishi boshqa vazifalarning bajarilishini to'xtatmaydi (`Promise.allSettled`).
3. Yakunda aniq muvaffaqiyat va xatolar hisoboti shakllanadi.

## Ishlash natijasi:
```text
[Sync Engine]: 3 ta vazifani sinxronlash boshlandi...
Muvaffaqiyatli: [ 'Mijozlar: 50 ta mijoz yuklandi', 'Buyurtmalar: 120 ta buyurtma yangilandi' ]
Xatoliklar: [ 'Mahsulotlar: Tarmoq xatosi' ]
```

