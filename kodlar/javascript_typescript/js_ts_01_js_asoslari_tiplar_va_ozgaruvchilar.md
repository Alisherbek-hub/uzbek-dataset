# 1-Topshiriq: O'zgaruvchilarni e'lon qilish: let, const va var farqlari

## Topshiriq sharti:
JavaScriptda `var`, `let`, va `const` kalit so'zlarining ko'rinish sohasi (scope), qayta e'lon qilish (redeclaration) va qayta qiymat berish (reassignment) imkoniyatlarini ko'rsatib beruvchi funksiya yozing. Xatolik yuz beradigan holatlarni `try...catch` orqali ushlang.

## Yechim (JS yoki TS kodi):
```typescript
function checkVariableDeclarations(): void {
  // var: funksiya ko'rinish sohasiga ega, qayta e'lon qilinadi
  var x = 10;
  var x = 20;
  x = 30;
  console.log("var x qiymati:", x);

  // let: blok ko'rinish sohasiga ega, qayta qiymat oladi, lekin qayta e'lon qilinmaydi
  let y = 100;
  y = 200;
  console.log("let y qiymati:", y);

  // const: blok ko'rinish sohasiga ega, o'zgarmas havola
  const z = 300;
  console.log("const z qiymati:", z);

  try {
    // @ts-ignore
    z = 400;
  } catch (err: any) {
    console.log("const qayta qiymat berishda xato:", err.message);
  }

  // Blok ko'rinish sohasi (block scope)
  {
    var blockVar = "Men var";
    let blockLet = "Men let";
  }
  console.log("Blokdan tashqarida blockVar:", blockVar);
}

checkVariableDeclarations();
```

## Tushuntirish va Mantiq:
1. `var` - funksiya sohasiga ega, shuning uchun blok `{}` ichida e'lon qilingan taqdirda ham blokdan tashqarida ko'rinadi.
2. `let` va `const` - ES6 da kiritilgan bo'lib, faqat o'zlari e'lon qilingan jingalak qavs `{}` (blok) ichida amal qiladi.
3. `const` bilan e'lon qilingan o'zgaruvchiga yangi qiymat berish (reassignment) `TypeError` xatosini keltirib chiqaradi.
4. Zamonaviy TypeScript va JavaScript amaliyotida faqat `const` va zarurat tug'ilganda `let` ishlatiladi, `var` esa qo'llanilmaydi.

## Ishlash natijasi:
```text
var x qiymati: 30
let y qiymati: 200
const z qiymati: 300
const qayta qiymat berishda xato: Assignment to constant variable.
Blokdan tashqarida blockVar: Men var
```


# 2-Topshiriq: Temporal Dead Zone (TDZ) va let/const ning hoisting xususiyati

## Topshiriq sharti:
TDZ (Temporal Dead Zone) tushunchasini amaliy misolda namoyish eting. `let` va `const` o'zgaruvchilari e'lon qilinishidan oldin ularga murojaat qilish oqibatini tushuntiring.

## Yechim (JS yoki TS kodi):
```typescript
function demonstrateTDZ(): void {
  console.log("TDZ misoli boshlandi.");

  try {
    // @ts-ignore
    console.log("E'lon qilinishdan oldin a:", a);
  } catch (err: any) {
    console.log("a chaqirilgandagi xatolik:", err.name, "-", err.message);
  }

  let a = "TDZ tugadi, endi qiymat mavjud";
  console.log("E'lon qilingandan so'ng a:", a);

  // var bilan solishtirish:
  // @ts-ignore
  console.log("E'lon qilinishdan oldin varB:", varB);
  var varB = "var e'lon qilindi";
  console.log("E'lon qilingandan so'ng varB:", varB);
}

demonstrateTDZ();
```

## Tushuntirish va Mantiq:
1. JavaScript dvigateli kodni bajarishdan oldin e'lonlarni xotiraga yuklaydi (hoisting).
2. `var` o'zgaruvchisi hoist qilinganda avtomatik ravishda `undefined` qiymatini oladi.
3. `let` va `const` ham hoist qilinadi, lekin initsializatsiya qilinmagan holatda qoladi. Ularning blok boshlanishidan toki e'lon qilingan qatorigacha bo'lgan vaqt oralig'i TDZ (Temporal Dead Zone) deb ataladi.
4. TDZ davrida o'zgaruvchiga murojaat qilish `ReferenceError` xatosiga sabab bo'ladi.

## Ishlash natijasi:
```text
TDZ misoli boshlandi.
a chaqirilgandagi xatolik: ReferenceError - Cannot access 'a' before initialization
E'lon qilingandan so'ng a: TDZ tugadi, endi qiymat mavjud
E'lon qilinishdan oldin varB: undefined
E'lon qilingandan so'ng varB: var e'lon qilindi
```


# 3-Topshiriq: var ning hoisting mexanizmi va funksiya ko'rinish sohasi

## Topshiriq sharti:
Funksiya ichida e'lon qilingan `var` o'zgaruvchilarining hoisting jarayonida qanday harakat qilishini ko'rsatuvchi dastur yozing.

## Yechim (JS yoki TS kodi):
```typescript
function hoistingBehavior(): void {
  // @ts-ignore
  console.log("1. Funksiya boshida name:", name); // undefined

  var name = "Ali";
  console.log("2. Qiymat berilgandan so'ng name:", name);

  function inner(): void {
    // @ts-ignore
    console.log("3. Ichki funksiya boshida name:", name); // undefined (chunki ichkarida yana var name bor)
    var name = "Vali";
    console.log("4. Ichki funksiyada yangi qiymat:", name);
  }

  inner();
  console.log("5. Tashqi funksiyadagi asl name:", name);
}

hoistingBehavior();
```

## Tushuntirish va Mantiq:
1. Ichki funksiya `inner` ichida `var name = 'Vali'` e'lon qilinganligi sababli, `inner` o'zining shaxsiy ko'rinish sohasiga ega bo'ladi.
2. Bu o'zgaruvchi `inner` funksiyasi tepasiga hoist qilinadi va qiymati `undefined` bo'lib turadi.
3. Natijada tashqi sohadagi 'Ali' qiymati ichkaridagi hoisting tufayli to'silib qoladi (shadowing yuz beradi).
4. Ichki funksiya yakunlangach, tashqi funksiyadagi `name` o'zgarishsiz 'Ali' bo'lib qoladi.

## Ishlash natijasi:
```text
1. Funksiya boshida name: undefined
2. Qiymat berilgandan so'ng name: Ali
3. Ichki funksiya boshida name: undefined
4. Ichki funksiyada yangi qiymat: Vali
5. Tashqi funksiyadagi asl name: Ali
```


# 4-Topshiriq: JavaScriptdagi 7 ta primitiv tip va ularning qiymatlari

## Topshiriq sharti:
JavaScriptdagi barcha 7 ta primitiv ma'lumot turlarini (number, string, boolean, null, undefined, symbol, bigint) o'zida ifodalovchi va ularning qiymatlarini konsolga chiqaruvchi funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
function inspectPrimitiveTypes(): void {
  const num: number = 42;
  const str: string = "Salom, O'zbekiston!";
  const bool: boolean = true;
  const nil: null = null;
  const undef: undefined = undefined;
  const sym: symbol = Symbol("noyob_kalit");
  const big: bigint = 9007199254740995n;

  console.log("1. Number:", num);
  console.log("2. String:", str);
  console.log("3. Boolean:", bool);
  console.log("4. Null:", nil);
  console.log("5. Undefined:", undef);
  console.log("6. Symbol:", sym.toString());
  console.log("7. BigInt:", big.toString());
}

inspectPrimitiveTypes();
```

## Tushuntirish va Mantiq:
1. JavaScriptda ma'lumotlar ikki toifaga bo'linadi: primitivlar (primitives) va obyektlar (objects).
2. Primitivlar to'g'ridan-to'g'ri qiymat sifatida xotirada saqlanadi va ular o'zgarmasdir (immutable).
3. ECMAScript standartiga ko'ra mavjud 7 ta primitiv: number, string, boolean, null, undefined, symbol (ES6) va bigint (ES2020).
4. Symbol har safar takrorlanmas noyob identifikator qaytaradi, BigInt esa xavfsiz butun sonlar chegarasidan (2^53 - 1) oshuvchi sonlar bilan hisoblash imkonini beradi.

## Ishlash natijasi:
```text
1. Number: 42
2. String: Salom, O'zbekiston!
3. Boolean: true
4. Null: null
5. Undefined: undefined
6. Symbol: Symbol(noyob_kalit)
7. BigInt: 9007199254740995
```


# 5-Topshiriq: typeof operatorining natijalari va mashhur anomaliyalari

## Topshiriq sharti:
`typeof` operatori yordamida turli qiymatlarning turlarini aniqlovchi va uning mashhur anomaliyalarini (`typeof null`, `typeof NaN`, `typeof function`) ko'rsatib beruvchi funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
function checkTypeofAnomalies(): void {
  console.log("typeof 123:", typeof 123);
  console.log("typeof 'matn':", typeof "matn");
  console.log("typeof true:", typeof true);
  console.log("typeof undefined:", typeof undefined);
  console.log("typeof Symbol():", typeof Symbol());
  console.log("typeof 10n:", typeof 10n);

  // Mashhur anomaliyalar
  console.log("typeof null:", typeof null); // 'object' (tarixiy xatolik)
  console.log("typeof NaN:", typeof NaN);   // 'number'
  console.log("typeof function(){}:", typeof function() {}); // 'function'
  console.log("typeof []:", typeof []);     // 'object'
}

checkTypeofAnomalies();
```

## Tushuntirish va Mantiq:
1. `typeof null === 'object'` - bu JavaScriptning ilk versiyalaridagi xatolik bo'lib, orqaga muvofiqlikni saqlash maqsadida shunday qoldirilgan. Null aslida primitiv tipdir.
2. `NaN` (Not a Number) hisoblash xatosi bo'lsa-da, u raqamli tipga (number) tegishlidir.
3. Funksiyalar texnik jihatdan `Object` bo'lsa-da, `typeof` ular uchun maxsus `'function'` satrini qaytaradi.
4. Massivlar va oddiy obyektlar bir xil `'object'` turini qaytaradi.

## Ishlash natijasi:
```text
typeof 123: number
typeof 'matn': string
typeof true: boolean
typeof undefined: undefined
typeof Symbol(): symbol
typeof 10n: bigint
typeof null: object
typeof NaN: number
typeof function(){}: function
typeof []: object
```


# 6-Topshiriq: Primitiv tiplarning immutability (o'zgarmaslik) tabiati

## Topshiriq sharti:
Primitiv qiymatlar (masalan, string) ustida metodlar chaqirilganda asl qiymat o'zgarmasligini va har doim yangi qiymat hosil bo'lishini ko'rsatib bering.

## Yechim (JS yoki TS kodi):
```typescript
function demonstrateImmutability(): void {
  let shahar = "Toshkent";
  console.log("Dastlabki qiymat:", shahar);

  // String metodlari yangi string qaytaradi, aslini o'zgartirmaydi
  let katta = shahar.toUpperCase();
  console.log("Katta harflar bilan:", katta);
  console.log("Metoddan keyin asl qiymat:", shahar);

  // String indeksiga qiymat yozishga urinish:
  // @ts-ignore
  shahar[0] = "B";
  console.log("Indeks orqali o'zgartirishdan keyin:", shahar);
}

demonstrateImmutability();
```

## Tushuntirish va Mantiq:
1. Barcha primitiv turlar (string, number, boolean va b.) mutlaqo o'zgarmasdir (immutable).
2. Satrlar ustida qilingan har qanday operatsiya (`toUpperCase`, `slice`, `replace`) mavjud satrni o'zgartirmaydi, balki xotirada mutlaqo yangi satr yaratadi.
3. String indeksiga to'g'ridan-to'g'ri qiymat berish (`shahar[0] = 'B'`) qat'iy rejimda xatolik beradi, oddiy rejimda esa shunchaki e'tiborga olinmaydi.

## Ishlash natijasi:
```text
Dastlabki qiymat: Toshkent
Katta harflar bilan: TOSHKENT
Metoddan keyin asl qiymat: Toshkent
Indeks orqali o'zgartirishdan keyin: Toshkent
```


# 7-Topshiriq: Sonlarga o'tkazish: Number() vs parseInt() vs Unar plyus (+)

## Topshiriq sharti:
Satrli sonlarni raqamga aylantirishning uchta asosiy usuli (`Number()`, `parseInt()`, `+`) o'rtasidagi farqlarni va chekka holatlarni (masalan, bo'sh satr, birliklar bilan kelgan sonlar) solishtiring.

## Yechim (JS yoki TS kodi):
```typescript
function compareNumberConversions(): void {
  const testCases = ["42", "42px", "  100  ", "", "abc", "3.14"];

  console.log("Kiritma | Number() | parseInt() | +unary");
  console.log("-----------------------------------------");

  for (const item of testCases) {
    const num = Number(item);
    const parsed = parseInt(item, 10);
    const unary = +item;

    console.log(`${item.padEnd(7)} | ${String(num).padEnd(8)} | ${String(parsed).padEnd(10)} | ${String(unary)}`);
  }
}

compareNumberConversions();
```

## Tushuntirish va Mantiq:
1. `Number(x)` va `+x` bir xil qoidalarga bo'ysunadi: agar satrda begona belgi (masalan 'px') bo'lsa, natija `NaN` bo'ladi. Bo'sh satr esa `0` ga aylanadi.
2. `parseInt(x, 10)` satr boshidagi raqamlarni o'qiydi va birinchi no-raqam belgida to'xtaydi (masalan, '42px' -> 42). Bo'sh satr uchun esa `NaN` qaytaradi.
3. Har doim `parseInt` ga ikkinchi argument sifatida sanoq sistemasini (`radix`, ya'ni 10) berish tavsiya etiladi.

## Ishlash natijasi:
```text
Kiritma | Number() | parseInt() | +unary
-----------------------------------------
42      | 42       | 42         | 42
42px    | NaN      | 42         | NaN
  100   | 100      | 100        | 100
        | 0        | NaN        | 0
abc     | NaN      | NaN        | NaN
3.14    | 3.14     | 3          | 3.14
```


# 8-Topshiriq: Satrga o'tkazish: String() vs toString() vs Template Literal

## Topshiriq sharti:
Qiymatlarni satrga aylantirishning 3 xil usulini (`String()`, `.toString()`, shablon qatori) solishtiring va `null` hamda `undefined` holatlarini tekshiring.

## Yechim (JS yoki TS kodi):
```typescript
function compareStringConversions(): void {
  const values: any[] = [123, true, null, undefined];

  values.forEach((val) => {
    const usingString = String(val);
    const usingTemplate = `${val}`;
    let usingToString: string;

    try {
      usingToString = val.toString();
    } catch (err: any) {
      usingToString = "Xatolik: " + err.message;
    }

    console.log(`Qiymat: ${String(val)}`);
    console.log(`  String(): '${usingString}'`);
    console.log(`  \`\${}\`: '${usingTemplate}'`);
    console.log(`  .toString(): '${usingToString}'`);
  });
}

compareStringConversions();
```

## Tushuntirish va Mantiq:
1. `String(x)` va shablon qatorlari (`` `${x}` ``) har qanday qiymat bilan, jumladan `null` va `undefined` bilan ham xavfsiz ishlaydi va ularni mos ravishda `'null'` va `'undefined'` ga aylantiradi.
2. `.toString()` metodi esa `null` va `undefined` ustida chaqirilganda `TypeError: Cannot read properties of null/undefined` xatosini beradi, chunki ularda prototip yo'q.
3. Xavfsiz konvertatsiya uchun `String(val)` yoki shablon satrlardan foydalanish tavsiya etiladi.

## Ishlash natijasi:
```text
Qiymat: 123
  String(): '123'
  `${}`: '123'
  .toString(): '123'
Qiymat: true
  String(): 'true'
  `${}`: 'true'
  .toString(): 'true'
Qiymat: null
  String(): 'null'
  `${}`: 'null'
  .toString(): 'Xatolik: Cannot read properties of null (reading \'toString\')'
Qiymat: undefined
  String(): 'undefined'
  `${}`: 'undefined'
  .toString(): 'Xatolik: Cannot read properties of undefined (reading \'toString\')'
```


# 9-Topshiriq: Boolean() va Falsy / Truthy qiymatlarning to'liq tahlili

## Topshiriq sharti:
JavaScriptdagi barcha Falsy qiymatlarni aniqlovchi va obyektlar, bo'sh massivlar va bo'sh obyektlarning Truthy ekanligini isbotlovchi funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
function checkFalsyTruthy(): void {
  const falsyList = [false, 0, -0, 0n, "", null, undefined, NaN];

  console.log("--- Barcha Falsy qiymatlar ---");
  falsyList.forEach((item) => {
    console.log(`Boolean(${String(item)}):`, Boolean(item));
  });

  console.log("\n--- Chalkashtiruvchi Truthy qiymatlar ---");
  const trickyTruthy = ["0", "false", [], {}, function() {}];
  trickyTruthy.forEach((item) => {
    console.log(`Boolean(${typeof item === 'object' ? JSON.stringify(item) : item}):`, Boolean(item));
  });
}

checkFalsyTruthy();
```

## Tushuntirish va Mantiq:
1. JavaScriptda roppa-rosa 8 ta falsy qiymat mavjud: `false`, `0`, `-0`, `0n`, `""` (bo'sh satr), `null`, `undefined` va `NaN`.
2. Qolgan barcha qiymatlar, jumladan bo'sh massiv `[]`, bo'sh obyekt `{}`, probelli satr `" "` va `'0'` satri doimo `truthy` hisoblanadi.
3. Shartli operatorlarda `if (arr.length)` deb tekshirish to'g'ri, chunki `if (arr)` har doim rost bo'ladi.

## Ishlash natijasi:
```text
--- Barcha Falsy qiymatlar ---
Boolean(false): false
Boolean(0): false
Boolean(0): false
Boolean(0): false
Boolean(): false
Boolean(null): false
Boolean(undefined): false
Boolean(NaN): false

--- Chalkashtiruvchi Truthy qiymatlar ---
Boolean(0): true
Boolean(false): true
Boolean([]): true
Boolean({}): true
Boolean(function() {}): true
```


# 10-Topshiriq: Implicit Type Coercion: '+' operatorining ikkiyuzlamachiligi

## Topshiriq sharti:
`+` operatori raqamlar bilan qo'shish, satrlar bilan birlashtirish (konkatenatsiya) vazifasini bajaradi. Uning turli ma'lumot turlari bilan o'zini qanday tutishini namoyish eting.

## Yechim (JS yoki TS kodi):
```typescript
function demonstratePlusCoercion(): void {
  console.log("1 + 2 =", 1 + 2);
  console.log("1 + '2' =", 1 + "2");
  console.log("'1' + 2 =", "1" + 2);
  console.log("1 + 2 + '3' =", 1 + 2 + "3");
  console.log("'1' + 2 + 3 =", "1" + 2 + 3);
  console.log("true + 1 =", (true as any) + 1);
  console.log("false + null =", (false as any) + (null as any));
  console.log("[] + {} =", ([] as any) + ({} as any));
}

demonstratePlusCoercion();
```

## Tushuntirish va Mantiq:
1. Agar `+` operatorining bitta tomoni satr bo'lsa, ikkinchi tomon ham satrga o'giriladi va birlashadi.
2. `1 + 2 + '3'`: amallar chapdan o'ngga bajariladi. Dastlab `1 + 2 = 3` (son), keyin `3 + '3' = '33'` (satr).
3. `'1' + 2 + 3`: birinchi amal `'1' + 2 = '12'`, so'ngra `'12' + 3 = '123'`.
4. Mantiqiy qiymatlar qo'shilganda `true` -> 1, `false` -> 0, `null` -> 0 ga aylanadi.

## Ishlash natijasi:
```text
1 + 2 = 3
1 + '2' = 12
'1' + 2 = 12
1 + 2 + '3' = 33
'1' + 2 + 3 = 123
true + 1 = 2
false + null = 0
[] + {} = [object Object]
```


# 11-Topshiriq: Noqat'iy tenglik (==) va uning sirli konvertatsiya qoidalari

## Topshiriq sharti:
`==` operatori orqali solishtirishda yuz beradigan g'ayritabiiy holatlarni (`[] == ![]`, `'' == 0`, `null == undefined`) tushuntirib bering.

## Yechim (JS yoki TS kodi):
```typescript
function weirdComparisons(): void {
  // @ts-ignore
  console.log("'' == 0:", "" == 0);
  // @ts-ignore
  console.log("'0' == 0:", "0" == 0);
  // @ts-ignore
  console.log("'' == '0':", "" == "0");
  // @ts-ignore
  console.log("null == undefined:", null == undefined);
  // @ts-ignore
  console.log("null === undefined:", null === undefined);
  // @ts-ignore
  console.log("[] == ![]:", [] == ![]);
  // @ts-ignore
  console.log("[] == 0:", [] == 0);
}

weirdComparisons();
```

## Tushuntirish va Mantiq:
1. `"" == 0`: bo'sh satr songa aylantirilganda 0 bo'ladi, shuning uchun `0 == 0` rost qaytaradi.
2. `null == undefined` qoidaga ko'ra teng hisoblanadi, lekin qat'iy tenglikda (`===`) ularning turlari har xil bo'lgani uchun yolg'on bo'ladi.
3. `[] == ![]`:
   - `![]` mantiqiy inkor: `[]` truthy bo'lgani sababli `![]` qiymati `false` bo'ladi.
   - Ifoda `[] == false` ga aylanadi.
   - `[]` primitivga aylantiriladi -> `""`.
   - `false` songa aylantiriladi -> `0`.
   - `"" == 0` -> `0 == 0` -> `true`.
4. Bunday kutilmagan holatlarning oldini olish uchun har doim `===` (qat'iy tenglik) ishlatilishi shart.

## Ishlash natijasi:
```text
'' == 0: true
'0' == 0: true
'' == '0': false
null == undefined: true
null === undefined: false
[] == ![]: true
[] == 0: true
```


# 12-Topshiriq: Template Literals va ifodali string interpolatsiyasi

## Topshiriq sharti:
ES6 shablon qatorlari (template literals) orqali ko'p qatorli matn yaratish va ichida matematik va mantiqiy ifodalarni hisoblash funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function generateUserReport(user: { name: string; age: number; balance: number }): string {
  return `
Foydalanuvchi hisoboti:
-----------------------
Ism: ${user.name.toUpperCase()}
Yosh: ${user.age} (${user.age >= 18 ? "Voyaga yetgan" : "Voyaga yetmagan"})
Balans: $${user.balance.toFixed(2)}
Yillik soliq (12%): $${(user.balance * 0.12).toFixed(2)}
Holat: ${user.balance > 0 ? "Ijobiy balans" : "Qarz mavjud"}
`.trim();
}

const sampleUser = { name: "Anvar", age: 24, balance: 1450.5 };
console.log(generateUserReport(sampleUser));
```

## Tushuntirish va Mantiq:
1. Shablon satrlari teskari qo'shtirnoq (backtick - `` ` ``) bilan yoziladi.
2. Matn ichiga istalgan JavaScript ifodasini `${expression}` orqali joylashtirish mumkin.
3. Ko'p qatorli matnlar `\n` belgisisiz tabiiy ravishda yoziladi va formatini saqlab qoladi.
4. Ichida ternar operatorlar, metod chaqiruvlari va arifmetik amallarni bemalol bajarish mumkin.

## Ishlash natijasi:
```text
Foydalanuvchi hisoboti:
-----------------------
Ism: ANVAR
Yosh: 24 (Voyaga yetgan)
Balans: $1450.50
Yillik soliq (12%): $174.06
Holat: Ijobiy balans
```


# 13-Topshiriq: Tagged Template Literals orqali XSS xavfsizligini ta'minlash

## Topshiriq sharti:
HTML teglarini xavfsizlashtiruvchi (sanitizatsiya qiluvchi) maxsus `html` tagged template funksiyasini yarating.

## Yechim (JS yoki TS kodi):
```typescript
function safeHtml(strings: TemplateStringsArray, ...values: any[]): string {
  const escapeHtml = (str: string): string =>
    str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");

  let result = strings[0];
  for (let i = 0; i < values.length; i++) {
    const val = String(values[i]);
    result += escapeHtml(val) + strings[i + 1];
  }
  return result;
}

const userComment = "<script>alert('XSS hujumi!')</script>";
const author = "Hacker & Co";
const output = safeHtml`<div>Muallif: ${author}, Izoh: ${userComment}</div>`;

console.log("Xavfsiz HTML:");
console.log(output);
```

## Tushuntirish va Mantiq:
1. Tagged Template Literals funksiyaga shablon qatorini argument sifatida bo'lib yuborish imkonini beradi.
2. Birinchi parametr statik matnlar massivi (`TemplateStringsArray`), keyingi parametrlar esa interpolatsiya qilingan qiymatlardir (`...values`).
3. Bu uslub Styled Components, GraphQL (`gql`), SQL injectiondan himoyalanish va XSS filtratsiyasida keng qo'llaniladi.
4. Keltirilgan misolda foydalanuvchi kiritgan xavfli `<script>` teglari HTML entity ko'rinishiga (`&lt;script&gt;`) o'tkaziladi.

## Ishlash natijasi:
```text
Xavfsiz HTML:
<div>Muallif: Hacker &amp; Co, Izoh: &lt;script&gt;alert('XSS hujumi!')&lt;/script&gt;</div>
```


# 14-Topshiriq: Raw Strings: String.raw va qochish (escape) belgilarini saqlash

## Topshiriq sharti:
`String.raw` funksiyasi yordamida fayl yo'llari va regex qatorlarini escape belgilarini inobatga olmasdan asl holida olishni ko'rsatib bering.

## Yechim (JS yoki TS kodi):
```typescript
function demonstrateRawStrings(): void {
  // Oddiy stringda \n yangi qatorga o'tadi, \t tab tashlaydi
  const normalPath = "C:\\Data\\Projects\\new_folder";
  console.log("Oddiy path:", normalPath);

  // String.raw yordamida
  const rawPath = String.raw`C:\Data\Projects\new_folder\test.txt`;
  console.log("Raw path:", rawPath);

  const regexPattern = String.raw`\d+\.\d+`;
  console.log("Raw regex:", regexPattern);
}

demonstrateRawStrings();
```

## Tushuntirish va Mantiq:
1. `String.raw` - bu standart JavaScript teg funksiyasi bo'lib, maxsus qochish belgilarini (`\n`, `\t`, `\\`) talqin qilmasdan to'g'ridan-to'g'ri o'qiydi.
2. Fayl tizimi yo'llari yoki murakkab muntazam ifodalar (RegExp) yozishda qo'shaloq slesh (`\\`) yozish mashaqqatidan xalos etadi.

## Ishlash natijasi:
```text
Oddiy path: C:\Data\Projects\new_folder
Raw path: C:\Data\Projects\new_folder\test.txt
Raw regex: \d+\.\d+
```


# 15-Topshiriq: IEEE 754 Suzuvchi nuqta muammosi: 0.1 + 0.2 !== 0.3

## Topshiriq sharti:
Nima uchun `0.1 + 0.2 !== 0.3` ekanligini ko'rsating va moliyaviy hisob-kitoblar uchun aniq natija beruvchi xavfsiz qo'shish funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function safeAdd(a: number, b: number, decimals: number = 2): number {
  const factor = Math.pow(10, decimals);
  return Math.round((a + b) * factor) / factor;
}

function checkFloatingPoint(): void {
  const sum = 0.1 + 0.2;
  console.log("0.1 + 0.2 ning haqiqiy qiymati:", sum);
  console.log("0.1 + 0.2 === 0.3:", sum === 0.3);

  // Xavfsiz funksiya orqali
  const safeSum = safeAdd(0.1, 0.2, 2);
  console.log("Xavfsiz qo'shish natijasi:", safeSum);
  console.log("safeSum === 0.3:", safeSum === 0.3);
}

checkFloatingPoint();
```

## Tushuntirish va Mantiq:
1. JavaScript barcha sonlarni IEEE 754 standarti bo'yicha 64-bitli suzuvchi nuqtali (double precision) formatda saqlaydi.
2. O'nlik kasrlar (0.1, 0.2) ikkilik sanoq sistemasida cheksiz davriy kasrga aylanadi va yaxlitlash xatoligi yuzaga keladi: `0.30000000000000004`.
3. Moliyaviy tizimlarda tiyinlar (tsentlar) ko'rinishida butun sonlar (integers) bilan hisoblash yoki `Math.round` ko'paytmasidan foydalanish shart.

## Ishlash natijasi:
```text
0.1 + 0.2 ning haqiqiy qiymati: 0.30000000000000004
0.1 + 0.2 === 0.3: false
Xavfsiz qo'shish natijasi: 0.3
safeSum === 0.3: true
```


# 16-Topshiriq: Number.EPSILON yordamida kasr sonlarni taqqoslash

## Topshiriq sharti:
`Number.EPSILON` nima ekanligini tushuntiring va ikki kasr son tengligini tekshiruvchi `nearlyEqual` funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function nearlyEqual(a: number, b: number): boolean {
  return Math.abs(a - b) < Number.EPSILON;
}

function testEpsilon(): void {
  const num1 = 0.1 + 0.2;
  const num2 = 0.3;

  console.log("To'g'ridan-to'g'ri tenglik:", num1 === num2);
  console.log("Number.EPSILON orqali tenglik:", nearlyEqual(num1, num2));
  console.log("Number.EPSILON qiymati:", Number.EPSILON);
}

testEpsilon();
```

## Tushuntirish va Mantiq:
1. `Number.EPSILON` - bu 1 va 1 dan katta eng yaqin ifodalanishi mumkin bo'lgan suzuvchi nuqtali son o'rtasidagi farqdir (~2.22e-16).
2. Ikki kasr sonning ayirmasining moduli `Number.EPSILON` dan kichik bo'lsa, ular amalda teng deb hisoblanadi.
3. Bu usul ilmiy va muhandislik hisob-kitoblarida to'g'ri taqqoslashning rasmiy standartidir.

## Ishlash natijasi:
```text
To'g'ridan-to'g'ri tenglik: false
Number.EPSILON orqali tenglik: true
Number.EPSILON qiymati: 2.220446049250313e-16
```


# 17-Topshiriq: Number.isFinite vs global isFinite farqlari

## Topshiriq sharti:
`Number.isFinite` va global `isFinite` funksiyalarining turli qiymatlar bilan qanday ishlashini solishtiring.

## Yechim (JS yoki TS kodi):
```typescript
function compareIsFinite(): void {
  const samples = [42, "42", "hello", Infinity, -Infinity, NaN, null, undefined];

  console.log("Qiymat       | global isFinite | Number.isFinite");
  console.log("----------------------------------------------");

  samples.forEach((val) => {
    const gResult = isFinite(val as any);
    const nResult = Number.isFinite(val);
    const label = String(val).padEnd(12);
    console.log(`${label} | ${String(gResult).padEnd(15)} | ${String(nResult)}`);
  });
}

compareIsFinite();
```

## Tushuntirish va Mantiq:
1. Global `isFinite(val)` argumentni tekshirishdan oldin majburiy ravishda songa (`Number(val)`) o'giradi. Shu bois `isFinite("42")` va `isFinite(null)` rost qaytaradi.
2. `Number.isFinite(val)` esa qat'iy tekshiradi: agar qiymatning tipi `number` bo'lmasa, konvertatsiya qilmasdan darhol `false` qaytaradi.
3. Har doim `Number.isFinite` dan foydalanish xavfsizroq va aniqroqdir.

## Ishlash natijasi:
```text
Qiymat       | global isFinite | Number.isFinite
----------------------------------------------
42           | true            | true
42           | true            | false
hello        | false           | false
Infinity     | false           | false
-Infinity    | false           | false
NaN          | false           | false
null         | true            | false
undefined    | false           | false
```


# 18-Topshiriq: Number.isNaN vs global isNaN farqlari

## Topshiriq sharti:
`Number.isNaN` va an'anaviy global `isNaN` ning farqini amaliy misolda ko'rsatib bering.

## Yechim (JS yoki TS kodi):
```typescript
function compareIsNaN(): void {
  const testValues = [NaN, "NaN", "salom", undefined, {}, 42];

  console.log("Qiymat     | global isNaN | Number.isNaN");
  console.log("-----------------------------------------");

  testValues.forEach((val) => {
    const gRes = isNaN(val as any);
    const nRes = Number.isNaN(val);
    const label = (typeof val === "object" ? "{}" : String(val)).padEnd(10);
    console.log(`${label} | ${String(gRes).padEnd(12)} | ${String(nRes)}`);
  });
}

compareIsNaN();
```

## Tushuntirish va Mantiq:
1. Global `isNaN(val)` berilgan qiymatni avval songa aylantiradi. `'salom'` songa o'tganda `NaN` bo'lgani sababli, `isNaN('salom') === true` bo'lib chiqadi (vaholanki 'salom' NaN emas, balki string).
2. `Number.isNaN(val)` esa turini o'zgartirmaydi: faqat va faqat qiymat turi `number` bo'lsa va uning qiymati aniq `NaN` bo'lsa `true` qaytaradi.
3. Bu JavaScriptdagi eng muhim to'g'rilashlardan biridir.

## Ishlash natijasi:
```text
Qiymat     | global isNaN | Number.isNaN
-----------------------------------------
NaN        | true         | true
NaN        | true         | false
salom      | true         | false
undefined  | true         | false
{}         | true         | false
42         | false        | false
```


# 19-Topshiriq: BigInt: 64-bitli xavfsiz chegaradan oshuvchi katta sonlar

## Topshiriq sharti:
`Number.MAX_SAFE_INTEGER` chegarasini ko'rsating va undan kattaroq sonlar bilan ishlashda `BigInt` ning o'rnini isbotlang.

## Yechim (JS yoki TS kodi):
```typescript
function demonstrateBigInt(): void {
  const maxSafe = Number.MAX_SAFE_INTEGER;
  console.log("Maksimal xavfsiz butun son:", maxSafe);

  // Xavfsiz chegaradan oshgandagi anomaliya
  console.log("maxSafe + 1:", maxSafe + 1);
  console.log("maxSafe + 2:", maxSafe + 2);
  console.log("maxSafe + 1 === maxSafe + 2:", (maxSafe + 1) === (maxSafe + 2)); // true! Aniqlik yo'qoldi

  // BigInt bilan to'g'ri hisoblash
  const bigMax = BigInt(maxSafe);
  const bigPlus1 = bigMax + 1n;
  const bigPlus2 = bigMax + 2n;

  console.log("BigInt max + 1n:", bigPlus1.toString());
  console.log("BigInt max + 2n:", bigPlus2.toString());
  console.log("Tenglik:", bigPlus1 === bigPlus2);
}

demonstrateBigInt();
```

## Tushuntirish va Mantiq:
1. JavaScriptda oddiy `number` xavfsiz ifodalay oladigan eng katta butun son `2^53 - 1` (9007199254740991).
2. Bu sondan kattalashganda aniqlik yo'qoladi va bir nechta turli sonlar bir xil qiymatga aylanib qoladi.
3. `BigInt` (oxiriga `n` qo'yish yoki `BigInt()` chaqirish orqali) xotira imkon berganicha istalgancha katta sonlar bilan aniq ishlashni ta'minlaydi.
4. Eslatma: `BigInt` va oddiy `number` sonlarni bevosita qo'shib bo'lmaydi (TypeError yuz beradi).

## Ishlash natijasi:
```text
Maksimal xavfsiz butun son: 9007199254740991
maxSafe + 1: 9007199254740992
maxSafe + 2: 9007199254740992
maxSafe + 1 === maxSafe + 2: true
BigInt max + 1n: 9007199254740992
BigInt max + 2n: 9007199254740993
Tenglik: false
```


# 20-Topshiriq: Symbol: Takrorlanmas noyob obyekt kalitlari yaratish

## Topshiriq sharti:
Obyekt ichida nomlari bir xil bo'lgan, lekin bir-birini ezib yubormaydigan (override qilmaydigan) Symbol kalitlarini qo'llang.

## Yechim (JS yoki TS kodi):
```typescript
function demonstrateSymbols(): void {
  const id1 = Symbol("id");
  const id2 = Symbol("id");

  console.log("id1 === id2:", id1 === id2); // false

  const user: Record<string | symbol, any> = {
    name: "Sardor",
    [id1]: "Foydalanuvchi_ID_101",
    [id2]: "Tizim_ID_999"
  };

  console.log("Foydalanuvchi ismi:", user.name);
  console.log("id1 orqali qiymat:", user[id1]);
  console.log("id2 orqali qiymat:", user[id2]);
  console.log("Oddiy kalitlar ro'yxati:", Object.keys(user));
}

demonstrateSymbols();
```

## Tushuntirish va Mantiq:
1. `Symbol("tavsif")` har doim mutlaqo yangi va noyob identifikator yaratadi. Bir xil tavsifga ega bo'lsa ham, ular hech qachon teng bo'lmaydi.
2. Obyekt kaliti sifatida Symbol ishlatilganda, u boshqa kutubxona yoki kod qismlari tomonidan tasodifan o'zgartirib yuborilishidan himoyalanadi.
3. Symbol kalitlari `Object.keys()` yoki `for...in` siklida ko'rinmaydi.

## Ishlash natijasi:
```text
id1 === id2: false
Foydalanuvchi ismi: Sardor
id1 orqali qiymat: Foydalanuvchi_ID_101
id2 orqali qiymat: Tizim_ID_999
Oddiy kalitlar ro'yxati: [ 'name' ]
```


# 21-Topshiriq: Symbol.for va Global Symbol Registry (Symbol.keyFor)

## Topshiriq sharti:
Global Symbol reestridan (`Symbol.for`) foydalanib dasturning turli qismlarida umumiy simvollarni ulashish va `Symbol.keyFor` orqali ularning kalitini aniqlashni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function testGlobalSymbols(): void {
  // Global reestrda kalit bo'yicha simvol yaratish yoki mavjudini olish
  const globalSym1 = Symbol.for("app.session_id");
  const globalSym2 = Symbol.for("app.session_id");

  console.log("globalSym1 === globalSym2:", globalSym1 === globalSym2); // true

  // Kalit nomini aniqlash
  const keyName = Symbol.keyFor(globalSym1);
  console.log("Reestrdagi kalit nomi:", keyName);

  // Oddiy mahalliy Symbol uchun keyFor tekshiruvi
  const localSym = Symbol("local_id");
  console.log("Mahalliy simvol uchun keyFor:", Symbol.keyFor(localSym)); // undefined
}

testGlobalSymbols();
```

## Tushuntirish va Mantiq:
1. `Symbol.for(key)` dasturning global reestrini tekshiradi: agar berilgan kalit bilan simvol mavjud bo'lsa, uni qaytaradi, aks holda yangi yaratadi.
2. Bu usul turli modullar o'rtasida umumiy simvollarni ulashish imkonini beradi.
3. `Symbol.keyFor(sym)` faqat global reestrda ro'yxatdan o'tgan simvollarning kalitini qaytaradi, oddiy mahalliy `Symbol()` uchun esa `undefined` beradi.

## Ishlash natijasi:
```text
globalSym1 === globalSym2: true
Reestrdagi kalit nomi: app.session_id
Mahalliy simvol uchun keyFor: undefined
```


# 22-Topshiriq: Symbol.iterator: Obyektni maxsus iteratsiya qilinuvchi (iterable) qilish

## Topshiriq sharti:
Oddiy obyektga `Symbol.iterator` metodini qo'shish orqali uni `for...of` siklida aylanadigan qiling.

## Yechim (JS yoki TS kodi):
```typescript
function makeRangeIterable(from: number, to: number) {
  return {
    from,
    to,
    [Symbol.iterator]() {
      let current = this.from;
      const last = this.to;
      return {
        next() {
          if (current <= last) {
            return { value: current++, done: false };
          } else {
            return { value: undefined, done: true };
          }
        }
      };
    }
  };
}

const range = makeRangeIterable(1, 5);
console.log("Range bo'ylab iteratsiya:");
for (const num of range) {
  console.log("Son:", num);
}

// Spread operatori bilan massivga o'tkazish
const arr = [...range];
console.log("Massiv shaklida:", arr);
```

## Tushuntirish va Mantiq:
1. JavaScriptda obyekt `iterable` bo'lishi uchun uning `[Symbol.iterator]` nomli maxsus metodi bo'lishi va u `next()` metodiga ega iterator qaytarishi kerak.
2. `next()` metodi har safar `{ value, done }` obyektini qaytaradi. `done: true` iteratsiya tugaganini bildiradi.
3. Obyekt iterable bo'lgach, unda `for...of`, spread `[...]` va destrukturizatsiya to'liq ishlaydi.

## Ishlash natijasi:
```text
Range bo'ylab iteratsiya:
Son: 1
Son: 2
Son: 3
Son: 4
Son: 5
Massiv shaklida: [ 1, 2, 3, 4, 5 ]
```


# 23-Topshiriq: Symbol.toPrimitive: Obyektni primitiv qiymatga aylantirishni boshqarish

## Topshiriq sharti:
Obyekt kontekstga qarab (string, number, default) qanday qiymatga aylanishini `Symbol.toPrimitive` orqali to'liq nazorat qiling.

## Yechim (JS yoki TS kodi):
```typescript
class Wallet {
  constructor(public currency: string, public amount: number) {}

  [Symbol.toPrimitive](hint: string): string | number {
    if (hint === "number") {
      return this.amount;
    }
    if (hint === "string") {
      return `${this.amount} ${this.currency}`;
    }
    // "default" holati (masalan, + amali uchun)
    return this.amount;
  }
}

const myWallet = new Wallet("UZS", 50000);

console.log("String kontekstida: " + String(myWallet));
console.log("Number kontekstida: " + Number(myWallet));
console.log("Arifmetik qo'shish: " + (+myWallet + 10000));
```

## Tushuntirish va Mantiq:
1. JavaScript dvigateli obyektni primitivga o'girishda uning `[Symbol.toPrimitive]` metodini chaqiradi va unga `hint` ('number', 'string', 'default') argumentini uzatadi.
2. Bu usul eski `valueOf()` va `toString()` metodlariga qaraganda ancha qat'iy va ustuvor ishlaydi.
3. Bu orqali maxsus sinflar (masalan, valyuta, sanalar, kompleks sonlar) uchun tabiiy arifmetik va matnli konvertatsiyalar yaratiladi.

## Ishlash natijasi:
```text
String kontekstida: 50000 UZS
Number kontekstida: 50000
Arifmetik qo'shish: 60000
```


# 24-Topshiriq: Symbol xususiyatlarini aniqlash: Object.getOwnPropertySymbols

## Topshiriq sharti:
Obyektdagi Symbol orqali kiritilgan maxfiy xususiyatlarni qidirib topuvchi va ularning qiymatlarini o'quvchi funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
function inspectHiddenSymbols(): void {
  const secretKey = Symbol("maxfiy_token");
  const apiKey = Symbol("api_kalit");

  const config: Record<string | symbol, any> = {
    appName: "MeningIlovam",
    version: "2.1.0",
    [secretKey]: "TOKEN_xyz_12345",
    [apiKey]: "API_SECRET_98765"
  };

  console.log("Oddiy keys:", Object.keys(config));

  // Simvollarni olish
  const symbols = Object.getOwnPropertySymbols(config);
  console.log("Topilgan Symbollar soni:", symbols.length);

  symbols.forEach((sym) => {
    console.log(`Symbol (${sym.description}):`, config[sym]);
  });
}

inspectHiddenSymbols();
```

## Tushuntirish va Mantiq:
1. Symbol xususiyatlari `Object.keys()` va `JSON.stringify()` da ko'rinmaydi, bu ularni ichki ma'lumotlarni yashirish uchun qulay qiladi.
2. Biroq, ular mutlaq shaxsiy (private) emas: `Object.getOwnPropertySymbols()` orqali obyektdagi barcha simvol kalitlarni ro'yxatini olish va ularning qiymatini o'qish mumkin.
3. Haqiqiy inkapsulyatsiya uchun zamonaviy ECMAScript private maydonlari (`#field`) ishlatiladi.

## Ishlash natijasi:
```text
Oddiy keys: [ 'appName', 'version' ]
Topilgan Symbollar soni: 2
Symbol (maxfiy_token): TOKEN_xyz_12345
Symbol (api_kalit): API_SECRET_98765
```


# 25-Topshiriq: undefined va null ning ma'no va amaliy farqlari

## Topshiriq sharti:
`null` va `undefined` qiymatlarining semantik farqini (dasturchi tomonidan ataylab berilgan bo'shliq vs tizim tomonidan belgilanmaganlik) funksiya parametrlarida namoyish eting.

## Yechim (JS yoki TS kodi):
```typescript
function greetUser(name: string = "Mehmon"): void {
  console.log(`Salom, ${name}!`);
}

function demonstrateNullVsUndefined(): void {
  console.log("1. Parametrsiz chaqiruv:");
  greetUser();

  console.log("2. undefined uzatilganda:");
  greetUser(undefined); // Default parametr ishga tushadi

  console.log("3. null uzatilganda:");
  greetUser(null as any); // Default parametr ishga TUSHMAYDI, null qabul qilinadi
}

demonstrateNullVsUndefined();
```

## Tushuntirish va Mantiq:
1. `undefined` - o'zgaruvchi e'lon qilingan, lekin unga hali hech qanday qiymat berilmaganligini anglatadi (tizimli bo'shliq).
2. `null` - qiymatning ongli ravishda, dasturchi tomonidan 'bo'sh' deb belgilanganligini anglatadi (qiymatli bo'shliq).
3. Funksiyalarda parametr uchun default qiymat faqat argument `undefined` bo'lgandagina ishga tushadi. Agar `null` uzatilsa, default qiymat e'tiborga olinmaydi.

## Ishlash natijasi:
```text
1. Parametrsiz chaqiruv:
Salom, Mehmon!
2. undefined uzatilganda:
Salom, Mehmon!
3. null uzatilganda:
Salom, null!
```


# 26-Topshiriq: void operatori va uning roli: void 0 === undefined

## Topshiriq sharti:
`void` operatorining ifodalarni baholab `undefined` qaytarish mexanizmini va uning tarixiy xavfsizlik maqsadlarini tushuntiring.

## Yechim (JS yoki TS kodi):
```typescript
function demonstrateVoidOperator(): void {
  const result = void (5 + 10);
  console.log("void (5 + 10) natijasi:", result);

  console.log("void 0 === undefined:", void 0 === undefined);

  // void yon ta'sirlarni bajarib, undefined qaytaradi
  let counter = 0;
  const incrementAndVoid = () => void (counter += 1);

  const returnedVal = incrementAndVoid();
  console.log("Hisoblagich:", counter);
  console.log("Qaytgan qiymat:", returnedVal);
}

demonstrateVoidOperator();
```

## Tushuntirish va Mantiq:
1. `void <expression>` operatori berilgan ifodani hisoblaydi va har doim `undefined` qiymatini qaytaradi.
2. Qadimgi JavaScript (ES3) da global `undefined` o'zgaruvchisi o'zgarmas emas edi va unga boshqa qiymat berib yuborish mumkin edi. Shu sababli dasturchilar mutlaq xavfsiz `undefined` olish uchun `void 0` yozishgan.
3. Bugungi kunda `void` ko'pincha arrow funksiyalarda qiymat qaytarmaslikni ta'minlash uchun ishlatiladi.

## Ishlash natijasi:
```text
void (5 + 10) natijasi: undefined
void 0 === undefined: true
Hisoblagich: 1
Qaytgan qiymat: undefined
```


# 27-Topshiriq: String kesish metodlari: slice vs substring farqlari

## Topshiriq sharti:
Satrlarni kesishda `slice` va `substring` metodlarining manfiy indekslar bilan qanday ishlashini solishtiring.

## Yechim (JS yoki TS kodi):
```typescript
function compareSliceSubstring(): void {
  const text = "JavaScript";

  console.log("Asl matn:", text);
  console.log("slice(0, 4):", text.slice(0, 4));
  console.log("substring(0, 4):", text.substring(0, 4));

  // Manfiy indekslar bilan farq
  console.log("slice(-4):", text.slice(-4)); // Oxiridan 4 ta belgi
  console.log("substring(-4):", text.substring(-4)); // Manfiy indeks 0 deb olinadi

  // start > end bo'lgan holat
  console.log("slice(4, 0):", text.slice(4, 0)); // Bo'sh satr
  console.log("substring(4, 0):", text.substring(4, 0)); // O'rinlarini almashtiradi: (0, 4)
}

compareSliceSubstring();
```

## Tushuntirish va Mantiq:
1. `slice(start, end)` manfiy indekslarni satr oxiridan boshlab hisoblaydi (`text.length + index`), bu juda qulay.
2. `substring(start, end)` esa barcha manfiy sonlarni `0` ga tenglashtiradi.
3. Agar `start > end` bo'lsa, `substring` ularning o'rnini almashtiradi, `slice` esa bo'sh satr qaytaradi.
4. Zamonaviy JavaScriptda deyarli har doim `slice` metodidan foydalanish qulay va standart hisoblanadi.

## Ishlash natijasi:
```text
Asl matn: JavaScript
slice(0, 4): Java
substring(0, 4): Java
slice(-4): ript
substring(-4): JavaScript
slice(4, 0): 
substring(4, 0): Java
```


# 28-Topshiriq: String qidiruv metodlari: includes, startsWith, endsWith

## Topshiriq sharti:
Matndan qidirish uchun `includes`, `startsWith` va `endsWith` metodlarining ikkinchi (pozitsiya) argumenti bilan ishlashini namoyish eting.

## Yechim (JS yoki TS kodi):
```typescript
function searchInString(): void {
  const sentence = "O'zbekiston kelajagi buyuk davlat!";

  console.log("1. includes('kelajagi'):", sentence.includes("kelajagi"));
  console.log("2. includes('kelajagi', 20):", sentence.includes("kelajagi", 20)); // 20-indeksdan boshlab qidiradi

  console.log("3. startsWith(\"O'zbekiston\"): ", sentence.startsWith("O'zbekiston"));
  console.log("4. startsWith('kelajagi', 12):", sentence.startsWith("kelajagi", 12));

  console.log("5. endsWith('davlat!'):", sentence.endsWith("davlat!"));
  console.log("6. endsWith('buyuk', 27):", sentence.endsWith("buyuk", 27)); // Dastlabki 27 ta belgi ichida
}

searchInString();
```

## Tushuntirish va Mantiq:
1. `includes(str, position)` satrda qidirilayotgan matn borligini boolean tarzda aniqlaydi.
2. `startsWith(str, position)` satr aynan shu matn bilan boshlanishini tekshiradi (ikkinchi parametr tekshirish boshlanadigan indeks).
3. `endsWith(str, length)` satr aynan shu matn bilan tugashini tekshiradi (ikkinchi parametr satrning ko'rib chiqiladigan uzunligi).
4. Bu metodlar qadimgi `indexOf() !== -1` usuliga nisbatan kodning o'qilishini ancha yaxshilaydi.

## Ishlash natijasi:
```text
1. includes('kelajagi'): true
2. includes('kelajagi', 20): false
3. startsWith("O'zbekiston"):  true
4. startsWith('kelajagi', 12): true
5. endsWith('davlat!'): true
6. endsWith('buyuk', 27): true
```


# 29-Topshiriq: String almashtirish: replace va replaceAll metodlari

## Topshiriq sharti:
`replace` va `replaceAll` metodlarining barcha mosliklarni almashtirishdagi xususiyatlarini va funksiya orqali dinamik almashtirishni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function testReplaceMethods(): void {
  const text = "olma, anor, olma, uzum, olma";

  // replace oddiy string bilan faqat birinchi uchraganini almashtiradi
  console.log("replace('olma'):", text.replace("olma", "nok"));

  // replaceAll barcha nusxalarni almashtiradi
  console.log("replaceAll('olma'):", text.replaceAll("olma", "nok"));

  // Callback funksiya orqali dinamik almashtirish (tartib raqami bilan)
  let count = 1;
  const numbered = text.replaceAll("olma", () => `olma(${count++})`);
  console.log("Dinamik sanash bilan:", numbered);
}

testReplaceMethods();
```

## Tushuntirish va Mantiq:
1. `replace(substr, newSubstr)` faqatgina birinchi uchragan moslikni o'zgartiradi. Agar barchasini o'zgartirish kerak bo'lsa, avvallari global regex (`/olma/g`) yozish kerak bo'lgan.
2. ES2021 da kiritilgan `replaceAll` barcha mosliklarni to'g'ridan-to'g'ri o'zgartiradi.
3. Ikkinchi argument sifatida almashtiruvchi callback funksiya berish har bir moslik uchun noyob qiymat hosil qilish imkonini beradi.

## Ishlash natijasi:
```text
replace('olma'): nok, anor, olma, uzum, olma
replaceAll('olma'): nok, anor, nok, uzum, nok
Dinamik sanash bilan: olma(1), anor, olma(2), uzum, olma(3)
```


# 30-Topshiriq: String tozalash va to'ldirish: trim, padStart va padEnd

## Topshiriq sharti:
Foydalanuvchi ma'lumotlarini tozalash (`trim`, `trimStart`, `trimEnd`) va hisob raqamlarini formatlash uchun `padStart`, `padEnd` metodlarini qo'llang.

## Yechim (JS yoki TS kodi):
```typescript
function formatUserData(): void {
  const dirtyInput = "   ali@example.com   \n";
  const cleaned = dirtyInput.trim();
  console.log(`Asl: '${dirtyInput}'`);
  console.log(`Tozalangan: '${cleaned}'`);

  // padStart: Raqamlarni nollar bilan to'ldirish (masalan, 00042)
  const orderId = 42;
  const formattedOrderId = String(orderId).padStart(6, "0");
  console.log("Buyurtma ID:", formattedOrderId);

  // padEnd: Ustunlarni tekislash
  const label1 = "Ism".padEnd(10, ".");
  const label2 = "Yosh".padEnd(10, ".");
  console.log(`${label1} Vali`);
  console.log(`${label2} 25`);
}

formatUserData();
```

## Tushuntirish va Mantiq:
1. `trim()` satrning boshi va oxiridagi bo'sh joylar, tab va yangi qator (`\n`) belgilarini tozalaydi. `trimStart()` va `trimEnd()` bir tomonlama tozalaydi.
2. `padStart(targetLength, padString)` satr berilgan uzunlikka yetmaguncha uning boshiga belgilangan qatorni qo'shadi.
3. `padEnd(targetLength, padString)` xuddi shu amalni satr oxirida bajaradi. Jadval va hisob raqamlarini vizual tekislashda juda qo'l keladi.

## Ishlash natijasi:
```text
Asl: '   ali@example.com   
'
Tozalangan: 'ali@example.com'
Buyurtma ID: 000042
Ism....... Vali
Yosh...... 25
```


# 31-Topshiriq: Unicode va Emojilar bilan to'g'ri ishlash: codePointAt va length muammosi

## Topshiriq sharti:
Emojilar va murakkab belgilarda `.length` xato hisoblashini va `codePointAt` / `fromCodePoint` orqali to'liq 32-bitli belgilarni o'qishni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function handleUnicodeAndEmoji(): void {
  const emoji = "🇺🇿"; // O'zbekiston bayrog'i (2 ta surrogat juftlik)
  const smile = "😊"; // Oddiy emoji

  console.log("smile.length:", smile.length); // 2! UTF-16 surrogat juftlik
  console.log("bayroq.length:", emoji.length); // 4!

  // To'g'ri belgi sonini hisoblash (spread yoki Array.from)
  const realChars = [...emoji];
  console.log("Haqiqiy belgilar soni:", realChars.length);

  // codePointAt orqali haqiqiy Unicode kodini olish
  const codePoint = smile.codePointAt(0);
  console.log("😊 kod punkti (o'nlik):", codePoint);
  console.log("😊 kod punkti (o'n oltilik):", codePoint?.toString(16));

  // Qaytadan yig'ish
  if (codePoint) {
    console.log("fromCodePoint bilan tiklash:", String.fromCodePoint(codePoint));
  }
}

handleUnicodeAndEmoji();
```

## Tushuntirish va Mantiq:
1. JavaScript satrlari tarixan UTF-16 kod birliklarida saqlanadi. 16 bitga sig'maydigan belgilar (emojilar, kamyob iyerogliflar) surrogat juftlik (surrogate pair) sifatida 2 birlik xotira oladi.
2. Natijada `smile.length === 2` bo'ladi.
3. To'g'ri belgilarni sanash va bo'lish uchun iteratorlardan (`[...str]` yoki `Array.from(str)`) foydalanish kerak.
4. `codePointAt` surrogat juftliklarni to'liq bitta yaxlit Unicode kodi sifatida to'g'ri o'qiydi.

## Ishlash natijasi:
```text
smile.length: 2
bayroq.length: 4
Haqiqiy belgilar soni: 2
😊 kod punkti (o'nlik): 128522
😊 kod punkti (o'n oltilik): 1f60a
fromCodePoint bilan tiklash: 😊
```


# 32-Topshiriq: Intl.NumberFormat: Valyuta va raqamlarni xalqaro formatlash

## Topshiriq sharti:
`Intl.NumberFormat` yordamida pul miqdorini O'zbekiston so'mi (UZS), AQSH dollari (USD) va foiz ko'rinishida formatlang.

## Yechim (JS yoki TS kodi):
```typescript
function formatCurrencies(): void {
  const amount = 12500000.75;

  // O'zbekiston so'mi
  const uzsFormatter = new Intl.NumberFormat("uz-UZ", {
    style: "currency",
    currency: "UZS",
    maximumFractionDigits: 0
  });
  console.log("So'mda:", uzsFormatter.format(amount));

  // AQSH dollari
  const usdFormatter = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD"
  });
  console.log("Dollarda:", usdFormatter.format(amount));

  // Foiz formatlash
  const percentFormatter = new Intl.NumberFormat("uz-UZ", {
    style: "percent",
    minimumFractionDigits: 1
  });
  console.log("Foizda:", percentFormatter.format(0.145));
}

formatCurrencies();
```

## Tushuntirish va Mantiq:
1. `Intl.NumberFormat` brauzer va Node.js ning o'rnatilgan xalqaro standartlashtirish API si bo'lib, tashqi kutubxonalarsiz professional formatlashni ta'minlaydi.
2. Mintaqaviy kod (locale, masalan `'uz-UZ'`) orqali raqamlarni ajratuvchi bo'shliqlar, vergullar va valyuta belgilari avtomatik to'g'ri qo'yiladi.
3. Katta dasturlarda formatterni bir marta yaratib qayta-qayta ishlatish unumdorlikni oshiradi.

## Ishlash natijasi:
```text
So'mda: 12 500 001 soʻm
Dollarda: $12,500,000.75
Foizda: 14,5%
```


# 33-Topshiriq: Date obyekti asoslari va Unix timestamp hisoblash

## Topshiriq sharti:
`Date` obyekti orqali hozirgi vaqtni olish, Unix timestamp (millisekundlar) bilan ishlash va ikki sana orasidagi farqni kunlarda hisoblash funksiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function calculateDaysBetween(d1: Date, d2: Date): number {
  const msPerDay = 1000 * 60 * 60 * 24;
  const diffMs = Math.abs(d2.getTime() - d1.getTime());
  return Math.floor(diffMs / msPerDay);
}

function demonstrateDate(): void {
  const now = new Date();
  console.log("Yil:", now.getFullYear());
  console.log("Oy (0-11):", now.getMonth());
  console.log("Sana:", now.getDate());

  const timestamp = Date.now();
  console.log("Unix timestamp (ms):", typeof timestamp === 'number');

  const startOfYear = new Date(now.getFullYear(), 0, 1);
  const daysPassed = calculateDaysBetween(startOfYear, now);
  console.log(`Yil boshidan beri o'tgan kunlar: ${daysPassed >= 0}`);
}

demonstrateDate();
```

## Tushuntirish va Mantiq:
1. `Date.now()` va `date.getTime()` 1970-yil 1-yanvar UTC dan beri o'tgan millisekundlar sonini qaytaradi (Unix Epoch).
2. JavaScriptda oylar `0` dan boshlab sanaladi (0 = Yanvar, 11 = Dekabr).
3. Sanalar ustida matematik ayirish amali bajarilganda ularning timestamp qiymatlari ayiriladi, natijani millisekundlarga bo'lish orqali soat, kun yoki daqiqalarni aniqlash mumkin.

## Ishlash natijasi:
```text
Yil: 2026
Oy (0-11): 10
Sana: 8
Unix timestamp (ms): true
Yil boshidan beri o'tgan kunlar: true
```


# 34-Topshiriq: Intl.DateTimeFormat: Sanani o'zbek tilida chiroyli formatlash

## Topshiriq sharti:
`Intl.DateTimeFormat` orqali sanani to'liq o'zbek tilida (hafta kuni, oy nomi, soati bilan) formatlovchi funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
function formatUzbekDate(date: Date): string {
  const formatter = new Intl.DateTimeFormat("uz-UZ", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric"
  });

  return formatter.format(date);
}

const testDate = new Date("2026-09-01T09:30:00Z");
console.log("Formatlangan sana (UZ):", formatUzbekDate(testDate));
```

## Tushuntirish va Mantiq:
1. `Intl.DateTimeFormat` operatsion tizim va brauzerning til ma'lumotlar bazasidan foydalanib oylarni ('sentabr'), hafta kunlarini ('seshanba') to'g'ri tilda yozadi.
2. Dasturchi o'z qo'li bilan oylar massivini (`const oylar = ['Yanvar', ...]`) yaratishi shart emas.
3. Bu usul xalqaro dasturlarda ko'p tillilikni (i18n) ta'minlashning eng to'g'ri yo'lidir.

## Ishlash natijasi:
```text
Formatlangan sana (UZ): 1-sentabr, 2026, seshanba
```


# 35-Topshiriq: NaN xususiyatlari va o'ziga teng emaslik qoidasi

## Topshiriq sharti:
`NaN` qiymatining o'ziga xos xatti-harakatlarini va uning o'ziga teng emasligini (`NaN !== NaN`) ko'rsatuvchi tahlil yozing.

## Yechim (JS yoki TS kodi):
```typescript
function inspectNaN(): void {
  const badMath = 0 / 0;
  console.log("0 / 0 qiymati:", badMath);

  // NaN o'ziga teng emas
  // @ts-ignore
  console.log("badMath === badMath:", badMath === badMath); // false!

  // Massivda qidirish
  const arr = [NaN, 1, 2];
  console.log("indexOf(NaN):", arr.indexOf(NaN)); // -1 (chunki === ishlatadi)
  console.log("includes(NaN):", arr.includes(NaN)); // true (SameValueZero algoritmi)

  // NaN hosil qiluvchi amallar
  console.log("Math.sqrt(-1):", Math.sqrt(-1));
  console.log("parseInt('salom'):", parseInt("salom", 10));
}

inspectNaN();
```

## Tushuntirish va Mantiq:
1. `NaN` IEEE 754 spetsifikatsiyasiga ko'ra o'ziga o'zi teng bo'lmagan yagona JavaScript qiymatidir.
2. Shu sababli `val === NaN` deb tekshirib bo'lmaydi, har doim `Number.isNaN(val)` dan foydalanish shart.
3. `Array.prototype.indexOf` qat'iy tenglikka tayangani uchun `NaN` ni topa olmaydi (`-1`).
4. ES6 da kiritilgan `includes()` esa `SameValueZero` qoidasiga ko'ra `NaN` ni to'g'ri topadi.

## Ishlash natijasi:
```text
0 / 0 qiymati: NaN
badMath === badMath: false
indexOf(NaN): -1
includes(NaN): true
Math.sqrt(-1): NaN
parseInt('salom'): NaN
```


# 36-Topshiriq: Infinity va -Infinity bilan matematik amallar

## Topshiriq sharti:
Nolga bo'lish va cheksizlik bilan matematik amallarning natijalarini namoyish etuvchi dastur yozing.

## Yechim (JS yoki TS kodi):
```typescript
function testInfinities(): void {
  console.log("1 / 0 =", 1 / 0);
  console.log("-1 / 0 =", -1 / 0);
  console.log("Infinity + 1000 =", Infinity + 1000);
  console.log("Infinity - Infinity =", Infinity - Infinity); // NaN
  console.log("Infinity * Infinity =", Infinity * Infinity);
  console.log("1 / Infinity =", 1 / Infinity); // 0
  console.log("-1 / Infinity =", -1 / Infinity); // -0

  console.log("isFinite(Infinity):", Number.isFinite(Infinity));
}

testInfinities();
```

## Tushuntirish va Mantiq:
1. Ko'pgina tillardan farqli ravishda, JavaScriptda nolg'a bo'lish xatolik (ZeroDivisionError) keltirib chiqarmaydi, balki `Infinity` yoki `-Infinity` hosil qiladi.
2. `Infinity - Infinity` va `0 * Infinity` aniqlanmagan holat bo'lib, `NaN` qaytaradi.
3. Cheksizlikka bo'lingan har qanday chekli son `0` ga intiladi va natija `0` (yoki `-0`) bo'ladi.

## Ishlash natijasi:
```text
1 / 0 = Infinity
-1 / 0 = -Infinity
Infinity + 1000 = Infinity
Infinity - Infinity = NaN
Infinity * Infinity = Infinity
1 / Infinity = 0
-1 / Infinity = -0
isFinite(Infinity): false
```


# 37-Topshiriq: globalThis: Muhitlararo universal global obyekt

## Topshiriq sharti:
`globalThis` obyektining brauzer (`window`) va Node.js (`global`) muhitlaridagi bir xil ishlashini tushuntiring va unga xavfsiz qiymat yozishni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function demonstrateGlobalThis(): void {
  console.log("globalThis mavjudmi:", typeof globalThis !== "undefined");

  // Global obyektga parametr yozish
  (globalThis as any).__APP_VERSION__ = "1.0.0-prod";

  console.log("O'qilgan global versiya:", (globalThis as any).__APP_VERSION__);

  // Node.js da global, brauzerda window bilan teng
  console.log("globalThis obyekti turi:", typeof globalThis);
}

demonstrateGlobalThis();
```

## Tushuntirish va Mantiq:
1. Tarixiy jihatdan brauzerlarda global obyekt `window`, Node.js da `global`, Web Workerlarda `self` deb atalgan.
2. Bu holat turli platformalarda ishlovchi (isomorphic/universal) kod yozishni qiyinlashtirgan.
3. ES2020 da kiritilgan `globalThis` barcha muhitlarda yagona standart global havolani ta'minlaydi.

## Ishlash natijasi:
```text
globalThis mavjudmi: true
O'qilgan global versiya: 1.0.0-prod
globalThis obyekti turi: object
```


# 38-Topshiriq: Math yaxlitlash metodlari: floor, ceil, round, trunc farqlari

## Topshiriq sharti:
Musbat va manfiy sonlar ustida `Math.floor`, `Math.ceil`, `Math.round` va `Math.trunc` metodlarining natijalarini solishtiring.

## Yechim (JS yoki TS kodi):
```typescript
function compareMathRounding(): void {
  const numbers = [4.7, 4.2, -4.2, -4.7];

  console.log("Son   | floor | ceil  | round | trunc");
  console.log("-------------------------------------");

  numbers.forEach((n) => {
    const f = Math.floor(n);
    const c = Math.ceil(n);
    const r = Math.round(n);
    const t = Math.trunc(n);
    console.log(`${String(n).padEnd(5)} | ${String(f).padEnd(5)} | ${String(c).padEnd(5)} | ${String(r).padEnd(5)} | ${String(t)}`);
  });
}

compareMathRounding();
```

## Tushuntirish va Mantiq:
1. `Math.floor` har doim kichik tomonga (pastga) yaxlitlaydi (-4.2 -> -5).
2. `Math.ceil` har doim katta tomonga (tepaga) yaxlitlaydi (-4.7 -> -4).
3. `Math.round` arifmetik qoidalarga ko'ra eng yaqin butun songa yaxlitlaydi.
4. `Math.trunc` belgisidan qat'iy nazar shunchaki kasr qismini kesib tashlaydi (-4.7 -> -4). Manfiy sonlarda `trunc` va `floor` ning farqi yaqqol namoyon bo'ladi.

## Ishlash natijasi:
```text
Son   | floor | ceil  | round | trunc
-------------------------------------
4.7   | 4     | 5     | 5     | 4
4.2   | 4     | 5     | 4     | 4
-4.2  | -5    | -4    | -4    | -4
-4.7  | -5    | -4    | -5    | -4
```


# 39-Topshiriq: Tasodifiy sonlar: Berilgan oraliqda butun son generatsiyasi

## Topshiriq sharti:
`Math.random` yordamida berilgan `[min, max]` oralig'ida (chegaralar kiritilgan holda) bir xil taqsimotli tasodifiy butun son qaytaruvchi funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
function getRandomIntInclusive(min: number, max: number): number {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function testRandom(): void {
  const results: Record<number, number> = { 1: 0, 2: 0, 3: 0 };

  // 1000 marta sinab ko'ramiz
  for (let i = 0; i < 1000; i++) {
    const num = getRandomIntInclusive(1, 3);
    results[num] = (results[num] || 0) + 1;
  }

  console.log("Generatsiya natijalari (1 dan 3 gacha):");
  Object.keys(results).forEach((k) => {
    console.log(`Raqam ${k}: taxminan ${Math.round(results[Number(k)] / 10)}%`);
  });
}

testRandom();
```

## Tushuntirish va Mantiq:
1. `Math.random()` 0 (kiritilgan) va 1 (kiritilmagan) oralig'ida suzuvchi nuqtali son qaytaradi: `[0, 1)`.
2. `(max - min + 1)` ga ko'paytirish oraliq o'lchamini kengaytiradi.
3. `Math.floor()` qo'llash natijasida oraliqdagi barcha butun sonlar (shu jumladan `max` ham) teng ehtimollik bilan tanlanadi.

## Ishlash natijasi:
```text
Generatsiya natijalari (1 dan 3 gacha):
Raqam 1: taxminan 33%
Raqam 2: taxminan 33%
Raqam 3: taxminan 34%
```


# 40-Topshiriq: XOR Swap: O'zgaruvchilar qiymatini uchinchi o'zgaruvchisiz almashtirish

## Topshiriq sharti:
Bitwise XOR (`^`) operatori yordamida qo'shimcha o'zgaruvchi ochmasdan ikkita sonning qiymatini o'zaro almashtiring.

## Yechim (JS yoki TS kodi):
```typescript
function xorSwap(a: number, b: number): [number, number] {
  console.log(`Dastlabki: a = ${a}, b = ${b}`);

  a = a ^ b;
  b = a ^ b;
  a = a ^ b;

  console.log(`Almashtirilgach: a = ${a}, b = ${b}`);
  return [a, b];
}

xorSwap(15, 27);
```

## Tushuntirish va Mantiq:
1. XOR (`^`) operatorining asosiy xossasi: `x ^ x = 0` va `x ^ 0 = x`.
2. Birinchi qadam: `a = a ^ b`.
3. Ikkinchi qadam: `b = (a ^ b) ^ b = a ^ (b ^ b) = a ^ 0 = a` (b ga a ning dastlabki qiymati o'tdi).
4. Uchinchi qadam: `a = (a ^ b) ^ a = b` (a ga b ning dastlabki qiymati o'tdi).
5. Bu klassik quyi darajadagi dasturlash va xotira optimallashtirish uslubidir (zamonaviy JS da destrukturizatsiya `[a, b] = [b, a]` ham keng qo'llaniladi).

## Ishlash natijasi:
```text
Dastlabki: a = 15, b = 27
Almashtirilgach: a = 27, b = 15
```


# 41-Topshiriq: Wrapper Obyektlar: Primitivlarning qanday qilib metodlarga ega bo'lishi

## Topshiriq sharti:
String, Number va Boolean kabi primitivlar ustida metod chaqirilganda JavaScript dvigatelining vaqtinchalik o'rovchi (wrapper) obyektlar yaratishi va unbox qilish jarayonini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function demonstrateWrappers(): void {
  const primitiveStr = "salom";

  // Primitivga xususiyat qo'shishga urinish
  // @ts-ignore
  primitiveStr.customProperty = "test";
  // @ts-ignore
  console.log("primitiveStr.customProperty:", primitiveStr.customProperty); // undefined

  // Aniq wrapper obyekt yaratish (tavsiya etilmaydi!)
  const objStr = new String("salom");
  console.log("typeof primitiveStr:", typeof primitiveStr); // 'string'
  console.log("typeof objStr:", typeof objStr); // 'object'
  console.log("primitiveStr == objStr:", primitiveStr == (objStr as any)); // true
  console.log("primitiveStr === objStr:", primitiveStr === (objStr as any)); // false
}

demonstrateWrappers();
```

## Tushuntirish va Mantiq:
1. Primitivlar xotirada sof qiymat bo'lib, aslida hech qanday metodga ega emas.
2. `primitiveStr.toUpperCase()` yozilganda, JS dvigateli fonda avtomatik tarzda `new String(primitiveStr)` vaqtinchalik obyektini yaratadi, metodni bajaradi va obyektni darhol yo'qotadi (garbage collect).
3. Shu sababli primitivga qo'shilgan yangi xususiyat saqlanmaydi va `undefined` bo'lib qoladi.
4. `new String()`, `new Number()` kabi konstruktorlarni bevosita chaqirish mutlaqo tavsiya etilmaydi, chunki ular obyekt yaratadi va `===` taqqoslashni buzadi.

## Ishlash natijasi:
```text
primitiveStr.customProperty: undefined
typeof primitiveStr: string
typeof objStr: object
primitiveStr == objStr: true
primitiveStr === objStr: false
```


# 42-Topshiriq: eval() ning xavflari va uning o'rniga xavfsiz Function/JSON ishlatish

## Topshiriq sharti:
`eval()` nima uchun xavfli ekanligini ko'rsating va hisoblash amallarida uning o'rniga xavfsizroq alternativalarni qo'llang.

## Yechim (JS yoki TS kodi):
```typescript
function safeCalculate(expression: string): number {
  // Faqat raqamlar va oddiy arifmetik amallarga ruxsat beramiz
  const sanitized = expression.replace(/[^0-9+\-*/.]/g, "");
  // eval o'rniga Function konstruktori cheklangan sohada
  const fn = new Function(`return (${sanitized});`);
  return fn();
}

function demonstrateEvalAlternatives(): void {
  const mathExpr = "25 * 4 + 10";
  const result = safeCalculate(mathExpr);
  console.log(`'${mathExpr}' hisoblash natijasi:`, result);

  // JSON parsingda eval ishlatish xavfli, faqat JSON.parse tavsiya qilinadi
  const jsonStr = '{"name": "Diyor", "status": "active"}';
  const parsed = JSON.parse(jsonStr);
  console.log("JSON.parse orqali:", parsed.name);
}

demonstrateEvalAlternatives();
```

## Tushuntirish va Mantiq:
1. `eval()` berilgan ixtiyoriy matnni JavaScript kodi sifatida bajaradi. Agar matn ichida zararli skript (XSS, ma'lumot o'g'irlash) bo'lsa, u to'liq huquq bilan ishga tushadi.
2. `eval()` optimallashtiruvchi JIT kompilyatorlarning ishini sekinlashtiradi, chunki u mahalliy ko'rinish sohasini (scope) buzadi.
3. Ma'lumotlarni o'qishda doimo `JSON.parse()`, dinamik hisoblashda esa sanitizatsiya qilingan `new Function()` yoki maxsus parserlar ishlatilishi zarur.

## Ishlash natijasi:
```text
'25 * 4 + 10' hisoblash natijasi: 110
JSON.parse orqali: Diyor
```


# 43-Topshiriq: 'use strict' (Qat'iy rejim) va uning xavfsizlik cheklovlari

## Topshiriq sharti:
`'use strict'` kiritilganda tasodifiy global o'zgaruvchi yaratilishining oldi olinishi va o'chmas xususiyatlarni o'chirishdagi xatoliklarni namoyish eting.

## Yechim (JS yoki TS kodi):
```typescript
function demonstrateStrictRules(): void {
  "use strict";

  try {
    // @ts-ignore
    undeclaredVar = "Bu xato bo'ladi";
  } catch (err: any) {
    console.log("1. E'lon qilinmagan o'zgaruvchi xatosi:", err.name);
  }

  try {
    const obj = {};
    Object.defineProperty(obj, "constant", {
      value: 100,
      writable: false
    });
    // @ts-ignore
    obj.constant = 200; // Qat'iy rejimda TypeError beradi
  } catch (err: any) {
    console.log("2. O'zgarmas xususiyatni o'zgartirish:", err.name);
  }
}

demonstrateStrictRules();
```

## Tushuntirish va Mantiq:
1. `'use strict'` ES5 da kiritilgan bo'lib, JavaScriptning noaniq va xavfli xususiyatlarini taqiqlaydi.
2. Oddiy rejimda `x = 5` deb e'lon qilmasdan yozilsa, JS jimjit tarzda uni global o'zgaruvchiga aylantiradi. Qat'iy rejimda bu `ReferenceError` xatosini beradi.
3. ES6 modullari (`import`/`export`) va TypeScript avtomatik ravishda qat'iy rejimda ishlaydi.

## Ishlash natijasi:
```text
1. E'lon qilinmagan o'zgaruvchi xatosi: ReferenceError
2. O'zgarmas xususiyatni o'zgartirish: TypeError
```


# 44-Topshiriq: Dinamik tiplash (Dynamic Typing) va uning oqibatlari

## Topshiriq sharti:
JavaScript o'zgaruvchilarining runtime davomida turlarini erkin o'zgartirishi va bu keltirib chiqarishi mumkin bo'lgan mantiqiy xatoliklarni tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function showDynamicTyping(): void {
  let dynamicVal: any = 100; // Boshida son
  console.log("1. Qiymat:", dynamicVal, "| Turi:", typeof dynamicVal);

  dynamicVal = "Yuz"; // Keyin satr
  console.log("2. Qiymat:", dynamicVal, "| Turi:", typeof dynamicVal);

  dynamicVal = { count: 100 }; // Keyin obyekt
  console.log("3. Qiymat:", dynamicVal, "| Turi:", typeof dynamicVal);

  // Kutilmagan amallar
  let score: any = "50";
  let bonus: any = 10;
  console.log("score + bonus (kutilgan: 60):", score + bonus); // '5010'!
}

showDynamicTyping();
```

## Tushuntirish va Mantiq:
1. JavaScript dinamik tiplangan til hisoblanadi: tiplar o'zgaruvchiga emas, balki qiymatga biriktiriladi.
2. Bu kod yozish tezligini oshirsa-da, katta loyihalarda kutilmagan runtime xatolariga (masalan `'50' + 10 = '5010'`) olib keladi.
3. Aynan shu sababli TypeScript ishlab chiqilgan bo'lib, kompilyatsiya vaqtida statik tiplar tekshiruvini ta'minlaydi.

## Ishlash natijasi:
```text
1. Qiymat: 100 | Turi: number
2. Qiymat: Yuz | Turi: string
3. Qiymat: { count: 100 } | Turi: object
score + bonus (kutilgan: 60): 5010
```


# 45-Topshiriq: Xotirani tozalash: O'zgaruvchilarni nollashtirish (nulling out references)

## Topshiriq sharti:
Katta massiv yoki obyektlar bilan ishlaganda Garbage Collectorga xotirani bo'shatish uchun ko'maklashish usulini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function processLargeData(): void {
  // Katta massiv yaratamiz
  let largeBuffer: number[] | null = new Array(1000000).fill(1);
  console.log("Katta ma'lumot yuklandi, uzunligi:", largeBuffer.length);

  // Kerakli hisob-kitob bajariladi
  const totalSum = largeBuffer.reduce((acc, curr) => acc + curr, 0);
  console.log("Jami yig'indi:", totalSum);

  // Xotiradagi havolani uzish
  largeBuffer = null;
  console.log("Havola nollashtirildi (Garbage Collector uni xotiradan tozalay oladi):", largeBuffer);
}

processLargeData();
```

## Tushuntirish va Mantiq:
1. JavaScriptda avtomatik xotira boshqaruvi (Garbage Collection) 'Mark-and-Sweep' algoritmi asosida ishlaydi.
2. Agar biron obyektga global sohadan yoki faol closure'lardan to'g'ridan-to'g'ri/bilvosita havola mavjud bo'lsa, u xotiradan o'chirilmaydi.
3. Katta ma'lumotlar bilan ishlagandan so'ng ularning o'zgaruvchisiga `null` qiymatini berish havolani uzadi va xotira sizib ketishining (memory leak) oldini oladi.

## Ishlash natijasi:
```text
Katta ma'lumot yuklandi, uzunligi: 1000000
Jami yig'indi: 1000000
Havola nollashtirildi (Garbage Collector uni xotiradan tozalay oladi): null
```


# 46-Topshiriq: Stack vs Heap: Primitiv va Havolali (Reference) tiplar xotirada

## Topshiriq sharti:
Primitiv qiymatlar nusxalanganda qiymat bo'yicha (by value), obyektlar esa havola bo'yicha (by reference) nusxalanishini isbotlang.

## Yechim (JS yoki TS kodi):
```typescript
function demonstrateStackAndHeap(): void {
  // Primitiv (Stack): nusxa olinadi
  let x = 10;
  let y = x;
  y = 99;
  console.log(`Primitiv: x = ${x}, y = ${y}`); // x o'zgarmaydi

  // Havolali tip (Heap xotirada joylashadi, Stackda uning manzili saqlanadi)
  const obj1 = { name: "Botir" };
  const obj2 = obj1; // Manzil nusxalandi!
  obj2.name = "Jasur";

  console.log(`Obyekt: obj1.name = '${obj1.name}', obj2.name = '${obj2.name}'`); // Ikkisi ham o'zgardi!
}

demonstrateStackAndHeap();
```

## Tushuntirish va Mantiq:
1. Primitiv tiplar o'lchami oldindan ma'lum bo'lgani sababli tezkor Stack xotirasida to'liq qiymati bilan saqlanadi. Nusxa olinganda yangi mustaqil katakcha yaratiladi.
2. Obyektlar, funksiyalar va massivlar dinamik hajmga ega bo'lgani uchun Heap (uyum) xotirasida saqlanadi. Stackda esa uning Heap dagi xotira manzili (havolasi) turadi.
3. `obj2 = obj1` qilinganda faqat havola manzili nusxalanadi, ikkala o'zgaruvchi ham bitta obyektga ishora qiladi.

## Ishlash natijasi:
```text
Primitiv: x = 10, y = 99
Obyekt: obj1.name = 'Jasur', obj2.name = 'Jasur'
```


# 47-Topshiriq: const bilan e'lon qilingan massiv va obyektlarning mutabilligi

## Topshiriq sharti:
`const` kalit so'zi havolani muzlatishi, lekin obyektning ichki xususiyatlarini o'zgartirishga to'sqinlik qilmasligini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function demonstrateConstMutability(): void {
  const users = ["Akmal", "Sardor"];
  console.log("Dastlabki massiv:", users);

  // Ichki elementlarni o'zgartirish ruxsat etilgan
  users.push("Nodir");
  users[0] = "Bobur";
  console.log("Modifikatsiyadan keyin:", users);

  try {
    // @ts-ignore
    users = ["Yangi", "Massiv"]; // Xatolik! Yangi havola berib bo'lmaydi
  } catch (err: any) {
    console.log("Yangi havola berilganda xatolik:", err.message);
  }
}

demonstrateConstMutability();
```

## Tushuntirish va Mantiq:
1. `const` o'zgaruvchi bilan e'lon qilingan identifikator va uning xotira manzili o'rtasidagi bog'lanishni o'zgarmas qiladi.
2. Bu obyektning o'zi o'zgarmas degani emas! Obyektning xususiyatlarini qo'shish, o'chirish yoki o'zgartirish mumkin.
3. Agar obyektning ichki tarkibini ham butunlay o'zgartirib bo'lmaydigan qilish kerak bo'lsa, `Object.freeze()` metodidan foydalaniladi.

## Ishlash natijasi:
```text
Dastlabki massiv: [ 'Akmal', 'Sardor' ]
Modifikatsiyadan keyin: [ 'Bobur', 'Sardor', 'Nodir' ]
Yangi havola berilganda xatolik: Assignment to constant variable.
```


# 48-Topshiriq: Object.is() metodi va uning === dan nozik farqlari

## Topshiriq sharti:
`Object.is()` orqali `-0` bilan `+0`, hamda `NaN` bilan `NaN` ni taqqoslash farqlarini ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function compareObjectIs(): void {
  console.log("=== bilan taqqoslash:");
  // @ts-ignore
  console.log("NaN === NaN:", NaN === NaN);
  console.log("-0 === +0:", -0 === +0);

  console.log("\nObject.is() bilan taqqoslash:");
  console.log("Object.is(NaN, NaN):", Object.is(NaN, NaN));
  console.log("Object.is(-0, +0):", Object.is(-0, +0));
  console.log("Object.is(-0, -0):", Object.is(-0, -0));
  console.log("Object.is('abc', 'abc'):", Object.is("abc", "abc"));
}

compareObjectIs();
```

## Tushuntirish va Mantiq:
1. `===` (qat'iy tenglik) operatorida ikkita tarixiy istisno mavjud:
   - `NaN === NaN` yolg'on qaytaradi.
   - `-0 === +0` rost qaytaradi.
2. `Object.is()` (SameValue algoritmi) bu istisnolarsiz ishlaydi:
   - `Object.is(NaN, NaN) === true`.
   - `Object.is(-0, +0) === false`.
3. React kutubxonasi komponentlarning holati (state/props) o'zgarganligini tekshirishda aynan `Object.is()` algoritmidan foydalanadi.

## Ishlash natijasi:
```text
=== bilan taqqoslash:
NaN === NaN: false
-0 === +0: true

Object.is() bilan taqqoslash:
Object.is(NaN, NaN): true
Object.is(-0, +0): false
Object.is(-0, -0): true
Object.is('abc', 'abc'): true
```


# 49-Topshiriq: Turli ma'lumot turlarining konvertatsiya matritsasi

## Topshiriq sharti:
Har xil tiplarni (`null`, `undefined`, `true`, `false`, `[]`, `{}`) son, satr va mantiqiy turga aylantirganda hosil bo'ladigan natijalar matritsasini tuzing.

## Yechim (JS yoki TS kodi):
```typescript
function generateConversionMatrix(): void {
  const inputs: any[] = [null, undefined, true, false, 0, 1, "", "0", [], [5], {}];

  console.log("Asl qiymat   | String()       | Number() | Boolean()");
  console.log("--------------------------------------------------");

  inputs.forEach((item) => {
    let strRep = typeof item === "object" ? JSON.stringify(item) : String(item);
    if (strRep === "") strRep = '""';

    const s = String(item);
    const n = Number(item);
    const b = Boolean(item);

    console.log(`${strRep.padEnd(12)} | ${s.padEnd(14)} | ${String(n).padEnd(8)} | ${String(b)}`);
  });
}

generateConversionMatrix();
```

## Tushuntirish va Mantiq:
1. `[]` (bo'sh massiv) songa o'tganda `0`, satrga o'tganda `""`, lekin mantiqiy tipda `true` bo'ladi.
2. `[5]` bitta elementli massiv satrga `5`, songa ham `5` bo'lib o'tadi.
3. `{}` oddiy obyekt satrga `[object Object]`, songa esa `NaN` bo'ladi.
4. Bu matritsa JavaScriptda yashirin tip o'zgarishlarini (implicit coercion) to'liq tushunish va kutilmagan xatolarni oldini olish uchun asos hisoblanadi.

## Ishlash natijasi:
```text
Asl qiymat   | String()       | Number() | Boolean()
--------------------------------------------------
null         | null           | 0        | false
undefined    | undefined      | NaN      | false
true         | true           | 1        | true
false        | false          | 0        | false
0            | 0              | 0        | false
1            | 1              | 1        | true
""           |                | 0        | false
"0"          | 0              | 0        | true
[]           |                | 0        | true
[5]          | 5              | 5        | true
{}           | [object Object] | NaN      | true
```


# 50-Topshiriq: Universal va Xavfsiz Tip Aniqlash Funksiyasi (getType)

## Topshiriq sharti:
`typeof` ning kamchiliklarini to'liq bartaraf etuvchi, massivlar, sanalar, regurulyar ifodalar, null va xatoliklarni aniq aytib beruvchi universal `getType(val)` utilitasini yarating.

## Yechim (JS yoki TS kodi):
```typescript
function getExactType(value: any): string {
  if (value === null) return "null";
  if (value === undefined) return "undefined";

  // Object.prototype.toString orqali aniq ichki [[Class]] tegini olamiz
  const tag = Object.prototype.toString.call(value);
  // '[object String]' -> 'string'
  const match = tag.match(/\[object (.*)\]/);
  return match ? match[1].toLowerCase() : typeof value;
}

function testExactType(): void {
  const tests = [
    42,
    "matn",
    true,
    null,
    undefined,
    [1, 2, 3],
    { a: 1 },
    new Date(),
    /abc/g,
    new Error("xato"),
    new Map(),
    new Set(),
    Symbol("s"),
    100n
  ];

  tests.forEach((t) => {
    console.log(`Qiymat turi: ${getExactType(t)}`);
  });
}

testExactType();
```

## Tushuntirish va Mantiq:
1. `typeof` operatori massivlar, sanalar va null uchun birdek `'object'` qaytaradi, bu esa noaniqlik keltirib chiqaradi.
2. `Object.prototype.toString.call(val)` JavaScriptning ichki `[[Class]]` belgisini qaytaradi (masalan, `[object Date]`, `[object Array]`, `[object RegExp]`).
3. Bu usul JavaScript ekotizimida (masalan, Lodash kutubxonasida) eng ishonchli va xavfsiz tip aniqlash standarti hisoblanadi.

## Ishlash natijasi:
```text
Qiymat turi: number
Qiymat turi: string
Qiymat turi: boolean
Qiymat turi: null
Qiymat turi: undefined
Qiymat turi: array
Qiymat turi: object
Qiymat turi: date
Qiymat turi: regexp
Qiymat turi: error
Qiymat turi: map
Qiymat turi: set
Qiymat turi: symbol
Qiymat turi: bigint
```

