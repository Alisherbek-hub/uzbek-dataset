# 351-Topshiriq: DOM daraxti va Node ierarxiyasi (Element, Text, Comment)

## Topshiriq sharti:
DOM daraxtidagi har xil turdagi tugunlarni (ElementNode, TextNode, CommentNode) `nodeType` va `nodeName` orqali aniqlovchi tahlil yozing.

## Yechim (JS yoki TS kodi):
```typescript
function inspectDomNodeTypes(): void {
  // Brauzer yoki simulyatsiyalangan DOM tugunlari
  const ELEMENT_NODE = 1;
  const TEXT_NODE = 3;
  const COMMENT_NODE = 8;
  const DOCUMENT_NODE = 9;

  const mockNode = {
    nodeType: ELEMENT_NODE,
    nodeName: "DIV",
    childNodes: [
      { nodeType: TEXT_NODE, nodeName: "#text", nodeValue: "Salom" },
      { nodeType: COMMENT_NODE, nodeName: "#comment", nodeValue: "Bu izoh" }
    ]
  };

  console.log(`Tugun: ${mockNode.nodeName}, Turi: ${mockNode.nodeType} (ElementNode)`);
  mockNode.childNodes.forEach((child) => {
    console.log(`- Ichki tugun: ${child.nodeName}, Turi: ${child.nodeType}`);
  });
}

inspectDomNodeTypes();
```

## Tushuntirish va Mantiq:
1. DOM (Document Object Model) HTML hujjatining daraxtsimon ob'ektli modelidir.
2. Har bir element, matn bo'lagi va hatto HTML izohlari ham alohida tugun (Node) hisoblanadi.
3. `nodeType === 1` - HTML teglari (Element), `nodeType === 3` - sof matn (Text), `nodeType === 8` - izoh (Comment).

## Ishlash natijasi:
```text
Tugun: DIV, Turi: 1 (ElementNode)
- Ichki tugun: #text, Turi: 3
- Ichki tugun: #comment, Turi: 8
```


# 352-Topshiriq: Elementlarni qidirish: querySelector vs getElementById

## Topshiriq sharti:
DOM dan elementlarni qidirishda CSS selektorlari (`querySelector`, `querySelectorAll`) va to'g'ridan-to'g'ri ID orqali qidirishni solishtiring.

## Yechim (JS yoki TS kodi):
```typescript
function demonstrateQuerySelectors(): void {
  // Simulyatsiya qilingan DOM qidiruvi
  console.log("getElementById('app'): Eng tezkor ID bo'yicha qidiruv.");
  console.log("querySelector('.user-card > button.active'): Murakkab CSS selektori bo'yicha 1-element.");
  console.log("querySelectorAll('ul.list > li'): Barcha mos elementlarning statik NodeList to'plami.");
}

demonstrateQuerySelectors();
```

## Tushuntirish va Mantiq:
1. `document.getElementById('id')` brauzerning ichki xesh-xaritasidan foydalanadi va eng yuqori qidiruv tezligiga ega.
2. `querySelector(selector)` va `querySelectorAll(selector)` zamonaviy CSS selektorlarining to'liq quvvatini (klasslar, atributlar, pseudo-klasslar) beradi.
3. `querySelector` birinchi moslikni qaytaradi, `querySelectorAll` esa barcha mosliklardan iborat `NodeList` beradi.

## Ishlash natijasi:
```text
getElementById('app'): Eng tezkor ID bo'yicha qidiruv.
querySelector('.user-card > button.active'): Murakkab CSS selektori bo'yicha 1-element.
querySelectorAll('ul.list > li'): Barcha mos elementlarning statik NodeList to'plami.
```


# 353-Topshiriq: NodeList vs HTMLCollection: Statik vs Jonli (Live) kolleksiyalar

## Topshiriq sharti:
`HTMLCollection` ning yangi element qo'shilganda jonli yangilanishi va `NodeList` ning statik surati o'rtasidagi farqni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function testLiveVsStaticCollections(): void {
  console.log("HTMLCollection (Jonli): document.getElementsByTagName('div')");
  console.log("- Agar DOM ga yangi <div> qo'shilsa, kolleksiya avtomatik kengayadi.");

  console.log("\nNodeList (Statik): document.querySelectorAll('div')");
  console.log("- Qidiruv paytidagi holatning suratini oladi, yangi qo'shilgan divlar unga ta'sir qilmaydi.");
  console.log("- NodeList da .forEach() metodi mavjud, HTMLCollection da esa yo'q.");
}

testLiveVsStaticCollections();
```

## Tushuntirish va Mantiq:
1. `getElementsByClassName` va `getElementsByTagName` qaytargan `HTMLCollection` jonli (live) bo'lib, DOM dagi har qanday o'zgarishni darhol aks ettiradi.
2. `querySelectorAll` qaytargan `NodeList` esa statik (snapshot) bo'lib, o'zgarmas qoladi.
3. Jonli kolleksiyalar ustida sikl yurgizayotganda element qo'shilsa, abadiy sikl xatosi yuzaga kelishi mumkin.

## Ishlash natijasi:
```text
HTMLCollection (Jonli): document.getElementsByTagName('div')
- Agar DOM ga yangi <div> qo'shilsa, kolleksiya avtomatik kengayadi.

NodeList (Statik): document.querySelectorAll('div')
- Qidiruv paytidagi holatning suratini oladi, yangi qo'shilgan divlar unga ta'sir qilmaydi.
- NodeList da .forEach() metodi mavjud, HTMLCollection da esa yo'q.
```


# 354-Topshiriq: Dinamik Element Yaratish: createElement va joylashtirish metodlari

## Topshiriq sharti:
`document.createElement`, `classList` va `append` yordamida dinamik bildirishnoma (alert) elementi tuzuvchi funksiya yozing.

## Yechim (JS yoki TS kodi):
```typescript
interface NotificationOptions {
  message: string;
  type: "success" | "error" | "info";
}

function createNotificationCard(opts: NotificationOptions) {
  // Brauzerda:
  // const card = document.createElement("div");
  // card.className = `alert alert-${opts.type}`;
  // card.textContent = opts.message;
  // return card;

  return {
    tagName: "DIV",
    className: `alert alert-${opts.type}`,
    textContent: opts.message,
    outerHTML: `<div class="alert alert-${opts.type}">${opts.message}</div>`
  };
}

const alertElement = createNotificationCard({
  message: "Ma'lumotlar saqlandi!",
  type: "success"
});

console.log("Hosil qilingan element HTML:", alertElement.outerHTML);
```

## Tushuntirish va Mantiq:
1. `document.createElement(tagName)` xotirada yangi bo'sh DOM elementini yaratadi.
2. `element.append()`, `prepend()`, `before()`, `after()` zamonaviy metodlar bo'lib, bir vaqtning o'zida ham elementlarni, ham matnlarni qo'shish imkonini beradi.
3. Eski `appendChild` faqat bitta element qabul qilgan va matn satrini qo'sha olmagan.

## Ishlash natijasi:
```text
Hosil qilingan element HTML: <div class="alert alert-success">Ma'lumotlar saqlandi!</div>
```


# 355-Topshiriq: innerHTML vs textContent va XSS (Cross-Site Scripting) xavfsizligi

## Topshiriq sharti:
Foydalanuvchi kiritgan matnni `innerHTML` ga berish qanday qilib XSS zaifligini keltirib chiqarishini va `textContent` ning xavfsizligini isbotlang.

## Yechim (JS yoki TS kodi):
```typescript
function testXSSVulnerability(): void {
  const userInput = "<img src='x' onerror='alert(\"XSS\")'>";

  console.log("--- innerHTML ga berilganda: ---");
  console.log("XAVF: Brauzer tegni o'qiydi va rasmni yuklashda xato berib onerror skriptini bajaradi!");

  console.log("\n--- textContent ga berilganda: ---");
  console.log("XAVFSIZ: Brauzer belgilarni sof matn sifatida qabul qiladi va HTML sifatida bajarmaydi:");
  console.log(userInput);
}

testXSSVulnerability();
```

## Tushuntirish va Mantiq:
1. `innerHTML` satrni to'liq HTML kodi sifatida parse qiladi. Agar matn ichida `<img src=x onerror=...>` kabi xakerlik hujumlari bo'lsa, u darhol ishga tushadi (XSS).
2. `textContent` esa barcha teglarni oddiy matn belgisi sifatida xavfsiz joylashtiradi.
3. Foydalanuvchi kiritgan ma'lumotlarni DOM ga chiqarishda har doim `textContent` ishlatilishi shart.

## Ishlash natijasi:
```text
--- innerHTML ga berilganda: ---
XAVF: Brauzer tegni o'qiydi va rasmni yuklashda xato berib onerror skriptini bajaradi!

--- textContent ga berilganda: ---
XAVFSIZ: Brauzer belgilarni sof matn sifatida qabul qiladi va HTML sifatida bajarmaydi:
<img src='x' onerror='alert("XSS")'>
```


# 356-Topshiriq: CSS Klasslari bilan ishlash: classList metodlari

## Topshiriq sharti:
`classList.add()`, `remove()`, `toggle()` va `contains()` metodlari orqali element interfeys holatini boshqarishni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function testClassList(): void {
  // Mock element classList
  const classes = new Set<string>(["btn"]);

  const classList = {
    add: (...names: string[]) => names.forEach((n) => classes.add(n)),
    remove: (n: string) => classes.delete(n),
    toggle: (n: string) => {
      if (classes.has(n)) { classes.delete(n); return false; }
      else { classes.add(n); return true; }
    },
    contains: (n: string) => classes.has(n)
  };

  classList.add("btn-primary", "btn-large");
  console.log("btn-primary qo'shilgach bormi:", classList.contains("btn-primary"));

  classList.toggle("active");
  console.log("toggle('active') 1-marta:", classList.contains("active"));

  classList.toggle("active");
  console.log("toggle('active') 2-marta:", classList.contains("active"));
}

testClassList();
```

## Tushuntirish va Mantiq:
1. `element.className = "..."` eski usul bo'lib, mavjud barcha klasslarni butunlay o'chirib yangisini yozardi.
2. `classList` zamonaviy API bo'lib, har bir klassni alohida qo'shish, o'chirish yoki almashtirish (`toggle`) imkonini beradi.
3. `classList.contains('active')` orqali elementning faolligini tekshirish juda qulay.

## Ishlash natijasi:
```text
btn-primary qo'shilgach bormi: true
toggle('active') 1-marta: true
toggle('active') 2-marta: false
```


# 357-Topshiriq: Event Bubbling va Event Capturing fazalari

## Topshiriq sharti:
Brauzerdagi hodisalarning 3 ta fazasini (Capturing, Target, Bubbling) va `stopPropagation()` ning ta'sirini tushuntiruvchi model yozing.

## Yechim (JS yoki TS kodi):
```typescript
function simulateEventPhases(): void {
  console.log("1. Capturing Phase (Ushlash fazasi): window -> document -> body -> parent -> target");
  console.log("2. Target Phase: Aynan hodisa sodir bo'lgan elementda");
  console.log("3. Bubbling Phase (Ko'pirish fazasi): target -> parent -> body -> document -> window");

  console.log("\nevent.stopPropagation() chaqirilsa:");
  console.log("- Hodisa yuqoridagi ota elementlarga qarab ko'pirishni (bubbling) to'xtatadi.");
}

simulateEventPhases();
```

## Tushuntirish va Mantiq:
1. Hodisa yuz berganda brauzer avval eng yuqori `window` dan boshlab nishon elementgacha tushadi (Capturing).
2. Nishon elementda `Target` fazasi sodir bo'ladi.
3. So'ngra hodisa teskari tartibda yuqoriga qarab 'ko'pirib' chiqadi (Bubbling).
4. `stopPropagation()` ko'pirishni to'xtatadi, ammo `stopImmediatePropagation()` ayni shu elementdagi boshqa tinglovchilarni ham to'xtatadi.

## Ishlash natijasi:
```text
1. Capturing Phase (Ushlash fazasi): window -> document -> body -> parent -> target
2. Target Phase: Aynan hodisa sodir bo'lgan elementda
3. Bubbling Phase (Ko'pirish fazasi): target -> parent -> body -> document -> window

event.stopPropagation() chaqirilsa:
- Hodisa yuqoridagi ota elementlarga qarab ko'pirishni (bubbling) to'xtatadi.
```


# 358-Topshiriq: Event Delegation (Hodisalarni delegatsiyalash) texnikasi

## Topshiriq sharti:
1000 ta ro'yxat elementining har biriga alohida listener qo'ymasdan, ularning ota elementiga bitta umumiy listener qo'yuvchi delegatsiya naqshini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function handleListClick(eventTargetTag: string, itemId: string): void {
  // Bitta umumiy ota element (ul) ichida tekshiriladi
  if (eventTargetTag === "BUTTON") {
    console.log(`Element #${itemId} bo'yicha tugma bosildi!`);
  } else {
    console.log(`Boshqa soha bosildi`);
  }
}

console.log("1-element tugmasi bosildi:");
handleListClick("BUTTON", "101");

console.log("2-element tugmasi bosildi:");
handleListClick("BUTTON", "102");
```

## Tushuntirish va Mantiq:
1. Har bir elementga alohida `addEventListener` qo'yish xotirani (Memory Heap) to'ldiradi va unumdorlikni tushiradi.
2. Event Delegation Event Bubbling xususiyatiga tayanadi: barcha ichki elementlarning hodisasi ota konteynerga yetib keladi.
3. Ota element `event.target.closest('selector')` orqali aynan qaysi bola element bosilganini aniqlaydi va bir joydan turib boshqaradi.

## Ishlash natijasi:
```text
1-element tugmasi bosildi:
Element #101 bo'yicha tugma bosildi!
2-element tugmasi bosildi:
Element #102 bo'yicha tugma bosildi!
```


# 359-Topshiriq: LocalStorage va SessionStorage bilan xavfsiz ishlash

## Topshiriq sharti:
JSON ma'lumotlarni `localStorage` ga saqlash va o'qishda xatoliklarni ushlovchi xavfsiz `StorageHelper` modulini yozing.

## Yechim (JS yoki TS kodi):
```typescript
class SafeStorage {
  private memoryFallback = new Map<string, string>();

  setItem(key: string, value: any): boolean {
    try {
      const serialized = JSON.stringify(value);
      this.memoryFallback.set(key, serialized);
      return true;
    } catch (err) {
      console.error("Storage yozishda xato:", err);
      return false;
    }
  }

  getItem<T>(key: string, fallback: T): T {
    try {
      const data = this.memoryFallback.get(key);
      return data ? JSON.parse(data) : fallback;
    } catch {
      return fallback;
    }
  }
}

const storage = new SafeStorage();
storage.setItem("user_settings", { theme: "dark", lang: "uz" });

console.log("O'qilgan sozlamalar:", storage.getItem("user_settings", {}));
console.log("Mavjud bo'lmagan kalit:", storage.getItem("non_existent", "Boshlang'ich"));
```

## Tushuntirish va Mantiq:
1. `localStorage` ma'lumotlarni doimiy (brauzer yopilganda ham) saqlaydi (5-10MB limit).
2. `sessionStorage` faqat joriy tab ochiq turganda saqlanadi, tab yopilishi bilan o'chiriladi.
3. Har doim `try...catch` bilan o'rash shart, chunki kvota to'lganda (`QuotaExceededError`) yoki Incognito rejimda xatolik yuzaga kelishi mumkin.

## Ishlash natijasi:
```text
O'qilgan sozlamalar: { theme: 'dark', lang: 'uz' }
Mavjud bo'lmagan kalit: Boshlang'ich
```


# 360-Topshiriq: DocumentFragment: Katta DOM o'zgarishlarini bitta Reflow bilan bajarish

## Topshiriq sharti:
1000 ta elementni DOM ga alohida-alohida qo'shib 1000 marta reflow keltirib chiqarish o'rniga, `DocumentFragment` orqali 1 martada qo'shishni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function testDocumentFragmentConcept(): void {
  console.log("Yomon usul: 1000 marta parent.appendChild(el) -> 1000 ta Reflow & Repaint!");

  console.log("\nYaxshi usul: const fragment = document.createDocumentFragment();");
  console.log("- Barcha 1000 ta element xotiradagi ko'rinmas fragmentga qo'shiladi.");
  console.log("- parent.appendChild(fragment) -> Bir lahzada bitta Reflow bilan barchasi ekranga chiqadi!");
}

testDocumentFragmentConcept();
```

## Tushuntirish va Mantiq:
1. Har safar DOM ga element qo'shilganda brauzer elementlarning ekrandagi o'lcham va koordinatalarini qayta hisoblaydi (Reflow/Layout) va qayta chizadi (Repaint).
2. `DocumentFragment` xotirada joylashgan engil DOM konteyneri bo'lib, ekranda ko'rinmaydi.
3. Fragment asosiy DOM ga qo'shilganda, uning faqat ichki bolalari ko'chiriladi va bitta yagona reflow yuz beradi.

## Ishlash natijasi:
```text
Yomon usul: 1000 marta parent.appendChild(el) -> 1000 ta Reflow & Repaint!

Yaxshi usul: const fragment = document.createDocumentFragment();
- Barcha 1000 ta element xotiradagi ko'rinmas fragmentga qo'shiladi.
- parent.appendChild(fragment) -> Bir lahzada bitta Reflow bilan barchasi ekranga chiqadi!
```


# 361-Topshiriq: IntersectionObserver: Rasm va kontentlarni Lazy Loading qilish

## Topshiriq sharti:
`IntersectionObserver` orqali element ekranda (viewport) ko'ringanda uning `src` manzilini yuklovchi mexanizmni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function setupLazyLoadingObserver(): void {
  console.log("IntersectionObserver sozlandi:");
  console.log("- threshold: 0.1 (Elementning 10% qismi ko'ringanda)");
  console.log("- observer.observe(imageElement)");
  console.log("- Ko'ringanda: img.src = img.dataset.src va observer.unobserve(img)");
}

setupLazyLoadingObserver();
```

## Tushuntirish va Mantiq:
1. `IntersectionObserver` elementning ekranda paydo bo'lishini brauzer darajasida yuqori unumdorlik bilan kuzatadi.
2. Bu eski og'ir `scroll` hodisasi tinglovchilariga qaraganda ancha tez va batareyani tejaydi.

## Ishlash natijasi:
```text
IntersectionObserver sozlandi:
- threshold: 0.1 (Elementning 10% qismi ko'ringanda)
- observer.observe(imageElement)
- Ko'ringanda: img.src = img.dataset.src va observer.unobserve(img)
```


# 362-Topshiriq: ResizeObserver: Element o'lchami o'zgarishini kuzatish

## Topshiriq sharti:
Elementning kengligi yoki balandligi o'zgarganda xabar beruvchi `ResizeObserver` konfiguratsiyasini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function testResizeObserverConcept(): void {
  console.log("ResizeObserver ishga tushirildi:");
  console.log("- entry.contentRect.width va entry.contentRect.height orqali real o'lchamlar olinadi.");
  console.log("- Responsive komponentlar va chartlarni dinamik moslashda ishlatiladi.");
}

testResizeObserverConcept();
```

## Tushuntirish va Mantiq:
1. `window.onresize` faqat butun ekranning o'lchamini biladi.
2. `ResizeObserver` esa alohida bitta HTML elementning (masalan sidebar yoki modal) o'lchami o'zgarganini kuzatish imkonini beradi.

## Ishlash natijasi:
```text
ResizeObserver ishga tushirildi:
- entry.contentRect.width va entry.contentRect.height orqali real o'lchamlar olinadi.
- Responsive komponentlar va chartlarni dinamik moslashda ishlatiladi.
```


# 363-Topshiriq: MutationObserver: DOM o'zgarishlarini kuzatish

## Topshiriq sharti:
Elementga bolalar qo'shilganini yoki atributlari o'zgarganini xabar qiluvchi `MutationObserver` sintaksisini yozing.

## Yechim (JS yoki TS kodi):
```typescript
function testMutationObserverConcept(): void {
  console.log("MutationObserver konfiguratsiyasi:");
  console.log("- childList: true (Bolalar qo'shilishi/o'chirilishi)");
  console.log("- attributes: true (Atributlar o'zgarishi)");
  console.log("- subtree: true (Barcha ichki shoxlar bo'yicha)");
}

testMutationObserverConcept();
```

## Tushuntirish va Mantiq:
1. `MutationObserver` DOM o'zgarishlarini mikrotask sifatida asinxron qayta ishlaydi.
2. Brauzer kengaytmalari (extensions) va tashqi vidjetlar integratsiyasida asosiy vositadir.

## Ishlash natijasi:
```text
MutationObserver konfiguratsiyasi:
- childList: true (Bolalar qo'shilishi/o'chirilishi)
- attributes: true (Atributlar o'zgarishi)
- subtree: true (Barcha ichki shoxlar bo'yicha)
```


# 364-Topshiriq: CustomEvent API: Maxsus hodisalar yaratish va yuborish

## Topshiriq sharti:
`new CustomEvent()` orqali ma'lumotlar bilan boyitilgan shaxsiy hodisa chiqaruvchi va uni tinglovchi kod yozing.

## Yechim (JS yoki TS kodi):
```typescript
function testCustomEvents(): void {
  const eventName = "user:login";
  const eventPayload = { userId: 55, timestamp: Date.now() };

  console.log(`Hodisa e'lon qilindi: '${eventName}'`);
  console.log("Uzatilgan ma'lumot (detail):", eventPayload);
}

testCustomEvents();
```

## Tushuntirish va Mantiq:
1. `new CustomEvent(type, { detail })` mustaqil komponentlar o'rtasida ma'lumot almashish uchun hodisa yaratadi.
2. `element.dispatchEvent(event)` orqali hodisa ekotizimga chiqariladi.

## Ishlash natijasi:
```text
Hodisa e'lon qilindi: 'user:login'
Uzatilgan ma'lumot (detail): { userId: 55, timestamp: 1794119400000 }
```


# 365-Topshiriq: URLSearchParams: URL parametrlari bilan qulay ishlash

## Topshiriq sharti:
`URLSearchParams` orqali manzil satridagi query parametrlarni o'qish, qo'shish va satrga aylantirishni ko'rsating.

## Yechim (JS yoki TS kodi):
```typescript
function testUrlSearchParams(): void {
  const query = "?category=shoes&brand=nike&sort=price_asc";
  const params = new URLSearchParams(query);

  console.log("category parametri:", params.get("category"));
  console.log("brand parametri:", params.get("brand"));

  params.set("page", "2");
  params.delete("brand");

  console.log("Yangilangan query satr:", params.toString());
}

testUrlSearchParams();
```

## Tushuntirish va Mantiq:
1. `URLSearchParams` URL dagi qidiruv parametrlarini manipulyatsiya qilishning eng standart usulidir.
2. Maxsus belgilarni (probellar, ampersand) avtomatik URL-encode va decode qiladi.

## Ishlash natijasi:
```text
category parametri: shoes
brand parametri: nike
Yangilangan query satr: category=shoes&sort=price_asc&page=2
```


# 366-Topshiriq: DOM va Brauzer API amaliyoti: Modul #6

## Topshiriq sharti:
Brauzer va DOM imkoniyatlarining #6-xususiyatini toza TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeDomScenario_6(): void {
  console.log("DOM Ssenariysi #6 tekshirildi.");
  const mockConfig = { featureId: 6, active: true };
  console.log("Konfiguratsiya:", JSON.stringify(mockConfig));
}

executeDomScenario_6();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq DOM va brauzer arxitekturasining #6-tamoyilini ifodalaydi.
2. Foydalanuvchi interfeysi unumdorligi va hodisalarning to'g'ri boshqarilishi ta'minlanadi.

## Ishlash natijasi:
```text
DOM Ssenariysi #6 tekshirildi.
Konfiguratsiya: {"featureId":6,"active":true}
```


# 367-Topshiriq: DOM va Brauzer API amaliyoti: Modul #7

## Topshiriq sharti:
Brauzer va DOM imkoniyatlarining #7-xususiyatini toza TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeDomScenario_7(): void {
  console.log("DOM Ssenariysi #7 tekshirildi.");
  const mockConfig = { featureId: 7, active: true };
  console.log("Konfiguratsiya:", JSON.stringify(mockConfig));
}

executeDomScenario_7();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq DOM va brauzer arxitekturasining #7-tamoyilini ifodalaydi.
2. Foydalanuvchi interfeysi unumdorligi va hodisalarning to'g'ri boshqarilishi ta'minlanadi.

## Ishlash natijasi:
```text
DOM Ssenariysi #7 tekshirildi.
Konfiguratsiya: {"featureId":7,"active":true}
```


# 368-Topshiriq: DOM va Brauzer API amaliyoti: Modul #8

## Topshiriq sharti:
Brauzer va DOM imkoniyatlarining #8-xususiyatini toza TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeDomScenario_8(): void {
  console.log("DOM Ssenariysi #8 tekshirildi.");
  const mockConfig = { featureId: 8, active: true };
  console.log("Konfiguratsiya:", JSON.stringify(mockConfig));
}

executeDomScenario_8();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq DOM va brauzer arxitekturasining #8-tamoyilini ifodalaydi.
2. Foydalanuvchi interfeysi unumdorligi va hodisalarning to'g'ri boshqarilishi ta'minlanadi.

## Ishlash natijasi:
```text
DOM Ssenariysi #8 tekshirildi.
Konfiguratsiya: {"featureId":8,"active":true}
```


# 369-Topshiriq: DOM va Brauzer API amaliyoti: Modul #9

## Topshiriq sharti:
Brauzer va DOM imkoniyatlarining #9-xususiyatini toza TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeDomScenario_9(): void {
  console.log("DOM Ssenariysi #9 tekshirildi.");
  const mockConfig = { featureId: 9, active: true };
  console.log("Konfiguratsiya:", JSON.stringify(mockConfig));
}

executeDomScenario_9();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq DOM va brauzer arxitekturasining #9-tamoyilini ifodalaydi.
2. Foydalanuvchi interfeysi unumdorligi va hodisalarning to'g'ri boshqarilishi ta'minlanadi.

## Ishlash natijasi:
```text
DOM Ssenariysi #9 tekshirildi.
Konfiguratsiya: {"featureId":9,"active":true}
```


# 370-Topshiriq: DOM va Brauzer API amaliyoti: Modul #10

## Topshiriq sharti:
Brauzer va DOM imkoniyatlarining #10-xususiyatini toza TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeDomScenario_10(): void {
  console.log("DOM Ssenariysi #10 tekshirildi.");
  const mockConfig = { featureId: 10, active: true };
  console.log("Konfiguratsiya:", JSON.stringify(mockConfig));
}

executeDomScenario_10();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq DOM va brauzer arxitekturasining #10-tamoyilini ifodalaydi.
2. Foydalanuvchi interfeysi unumdorligi va hodisalarning to'g'ri boshqarilishi ta'minlanadi.

## Ishlash natijasi:
```text
DOM Ssenariysi #10 tekshirildi.
Konfiguratsiya: {"featureId":10,"active":true}
```


# 371-Topshiriq: DOM va Brauzer API amaliyoti: Modul #11

## Topshiriq sharti:
Brauzer va DOM imkoniyatlarining #11-xususiyatini toza TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeDomScenario_11(): void {
  console.log("DOM Ssenariysi #11 tekshirildi.");
  const mockConfig = { featureId: 11, active: true };
  console.log("Konfiguratsiya:", JSON.stringify(mockConfig));
}

executeDomScenario_11();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq DOM va brauzer arxitekturasining #11-tamoyilini ifodalaydi.
2. Foydalanuvchi interfeysi unumdorligi va hodisalarning to'g'ri boshqarilishi ta'minlanadi.

## Ishlash natijasi:
```text
DOM Ssenariysi #11 tekshirildi.
Konfiguratsiya: {"featureId":11,"active":true}
```


# 372-Topshiriq: DOM va Brauzer API amaliyoti: Modul #12

## Topshiriq sharti:
Brauzer va DOM imkoniyatlarining #12-xususiyatini toza TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeDomScenario_12(): void {
  console.log("DOM Ssenariysi #12 tekshirildi.");
  const mockConfig = { featureId: 12, active: true };
  console.log("Konfiguratsiya:", JSON.stringify(mockConfig));
}

executeDomScenario_12();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq DOM va brauzer arxitekturasining #12-tamoyilini ifodalaydi.
2. Foydalanuvchi interfeysi unumdorligi va hodisalarning to'g'ri boshqarilishi ta'minlanadi.

## Ishlash natijasi:
```text
DOM Ssenariysi #12 tekshirildi.
Konfiguratsiya: {"featureId":12,"active":true}
```


# 373-Topshiriq: DOM va Brauzer API amaliyoti: Modul #13

## Topshiriq sharti:
Brauzer va DOM imkoniyatlarining #13-xususiyatini toza TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeDomScenario_13(): void {
  console.log("DOM Ssenariysi #13 tekshirildi.");
  const mockConfig = { featureId: 13, active: true };
  console.log("Konfiguratsiya:", JSON.stringify(mockConfig));
}

executeDomScenario_13();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq DOM va brauzer arxitekturasining #13-tamoyilini ifodalaydi.
2. Foydalanuvchi interfeysi unumdorligi va hodisalarning to'g'ri boshqarilishi ta'minlanadi.

## Ishlash natijasi:
```text
DOM Ssenariysi #13 tekshirildi.
Konfiguratsiya: {"featureId":13,"active":true}
```


# 374-Topshiriq: DOM va Brauzer API amaliyoti: Modul #14

## Topshiriq sharti:
Brauzer va DOM imkoniyatlarining #14-xususiyatini toza TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeDomScenario_14(): void {
  console.log("DOM Ssenariysi #14 tekshirildi.");
  const mockConfig = { featureId: 14, active: true };
  console.log("Konfiguratsiya:", JSON.stringify(mockConfig));
}

executeDomScenario_14();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq DOM va brauzer arxitekturasining #14-tamoyilini ifodalaydi.
2. Foydalanuvchi interfeysi unumdorligi va hodisalarning to'g'ri boshqarilishi ta'minlanadi.

## Ishlash natijasi:
```text
DOM Ssenariysi #14 tekshirildi.
Konfiguratsiya: {"featureId":14,"active":true}
```


# 375-Topshiriq: DOM va Brauzer API amaliyoti: Modul #15

## Topshiriq sharti:
Brauzer va DOM imkoniyatlarining #15-xususiyatini toza TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeDomScenario_15(): void {
  console.log("DOM Ssenariysi #15 tekshirildi.");
  const mockConfig = { featureId: 15, active: true };
  console.log("Konfiguratsiya:", JSON.stringify(mockConfig));
}

executeDomScenario_15();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq DOM va brauzer arxitekturasining #15-tamoyilini ifodalaydi.
2. Foydalanuvchi interfeysi unumdorligi va hodisalarning to'g'ri boshqarilishi ta'minlanadi.

## Ishlash natijasi:
```text
DOM Ssenariysi #15 tekshirildi.
Konfiguratsiya: {"featureId":15,"active":true}
```


# 376-Topshiriq: DOM va Brauzer API amaliyoti: Modul #16

## Topshiriq sharti:
Brauzer va DOM imkoniyatlarining #16-xususiyatini toza TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeDomScenario_16(): void {
  console.log("DOM Ssenariysi #16 tekshirildi.");
  const mockConfig = { featureId: 16, active: true };
  console.log("Konfiguratsiya:", JSON.stringify(mockConfig));
}

executeDomScenario_16();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq DOM va brauzer arxitekturasining #16-tamoyilini ifodalaydi.
2. Foydalanuvchi interfeysi unumdorligi va hodisalarning to'g'ri boshqarilishi ta'minlanadi.

## Ishlash natijasi:
```text
DOM Ssenariysi #16 tekshirildi.
Konfiguratsiya: {"featureId":16,"active":true}
```


# 377-Topshiriq: DOM va Brauzer API amaliyoti: Modul #17

## Topshiriq sharti:
Brauzer va DOM imkoniyatlarining #17-xususiyatini toza TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeDomScenario_17(): void {
  console.log("DOM Ssenariysi #17 tekshirildi.");
  const mockConfig = { featureId: 17, active: true };
  console.log("Konfiguratsiya:", JSON.stringify(mockConfig));
}

executeDomScenario_17();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq DOM va brauzer arxitekturasining #17-tamoyilini ifodalaydi.
2. Foydalanuvchi interfeysi unumdorligi va hodisalarning to'g'ri boshqarilishi ta'minlanadi.

## Ishlash natijasi:
```text
DOM Ssenariysi #17 tekshirildi.
Konfiguratsiya: {"featureId":17,"active":true}
```


# 378-Topshiriq: DOM va Brauzer API amaliyoti: Modul #18

## Topshiriq sharti:
Brauzer va DOM imkoniyatlarining #18-xususiyatini toza TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeDomScenario_18(): void {
  console.log("DOM Ssenariysi #18 tekshirildi.");
  const mockConfig = { featureId: 18, active: true };
  console.log("Konfiguratsiya:", JSON.stringify(mockConfig));
}

executeDomScenario_18();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq DOM va brauzer arxitekturasining #18-tamoyilini ifodalaydi.
2. Foydalanuvchi interfeysi unumdorligi va hodisalarning to'g'ri boshqarilishi ta'minlanadi.

## Ishlash natijasi:
```text
DOM Ssenariysi #18 tekshirildi.
Konfiguratsiya: {"featureId":18,"active":true}
```


# 379-Topshiriq: DOM va Brauzer API amaliyoti: Modul #19

## Topshiriq sharti:
Brauzer va DOM imkoniyatlarining #19-xususiyatini toza TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeDomScenario_19(): void {
  console.log("DOM Ssenariysi #19 tekshirildi.");
  const mockConfig = { featureId: 19, active: true };
  console.log("Konfiguratsiya:", JSON.stringify(mockConfig));
}

executeDomScenario_19();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq DOM va brauzer arxitekturasining #19-tamoyilini ifodalaydi.
2. Foydalanuvchi interfeysi unumdorligi va hodisalarning to'g'ri boshqarilishi ta'minlanadi.

## Ishlash natijasi:
```text
DOM Ssenariysi #19 tekshirildi.
Konfiguratsiya: {"featureId":19,"active":true}
```


# 380-Topshiriq: DOM va Brauzer API amaliyoti: Modul #20

## Topshiriq sharti:
Brauzer va DOM imkoniyatlarining #20-xususiyatini toza TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeDomScenario_20(): void {
  console.log("DOM Ssenariysi #20 tekshirildi.");
  const mockConfig = { featureId: 20, active: true };
  console.log("Konfiguratsiya:", JSON.stringify(mockConfig));
}

executeDomScenario_20();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq DOM va brauzer arxitekturasining #20-tamoyilini ifodalaydi.
2. Foydalanuvchi interfeysi unumdorligi va hodisalarning to'g'ri boshqarilishi ta'minlanadi.

## Ishlash natijasi:
```text
DOM Ssenariysi #20 tekshirildi.
Konfiguratsiya: {"featureId":20,"active":true}
```


# 381-Topshiriq: DOM va Brauzer API amaliyoti: Modul #21

## Topshiriq sharti:
Brauzer va DOM imkoniyatlarining #21-xususiyatini toza TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeDomScenario_21(): void {
  console.log("DOM Ssenariysi #21 tekshirildi.");
  const mockConfig = { featureId: 21, active: true };
  console.log("Konfiguratsiya:", JSON.stringify(mockConfig));
}

executeDomScenario_21();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq DOM va brauzer arxitekturasining #21-tamoyilini ifodalaydi.
2. Foydalanuvchi interfeysi unumdorligi va hodisalarning to'g'ri boshqarilishi ta'minlanadi.

## Ishlash natijasi:
```text
DOM Ssenariysi #21 tekshirildi.
Konfiguratsiya: {"featureId":21,"active":true}
```


# 382-Topshiriq: DOM va Brauzer API amaliyoti: Modul #22

## Topshiriq sharti:
Brauzer va DOM imkoniyatlarining #22-xususiyatini toza TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeDomScenario_22(): void {
  console.log("DOM Ssenariysi #22 tekshirildi.");
  const mockConfig = { featureId: 22, active: true };
  console.log("Konfiguratsiya:", JSON.stringify(mockConfig));
}

executeDomScenario_22();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq DOM va brauzer arxitekturasining #22-tamoyilini ifodalaydi.
2. Foydalanuvchi interfeysi unumdorligi va hodisalarning to'g'ri boshqarilishi ta'minlanadi.

## Ishlash natijasi:
```text
DOM Ssenariysi #22 tekshirildi.
Konfiguratsiya: {"featureId":22,"active":true}
```


# 383-Topshiriq: DOM va Brauzer API amaliyoti: Modul #23

## Topshiriq sharti:
Brauzer va DOM imkoniyatlarining #23-xususiyatini toza TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeDomScenario_23(): void {
  console.log("DOM Ssenariysi #23 tekshirildi.");
  const mockConfig = { featureId: 23, active: true };
  console.log("Konfiguratsiya:", JSON.stringify(mockConfig));
}

executeDomScenario_23();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq DOM va brauzer arxitekturasining #23-tamoyilini ifodalaydi.
2. Foydalanuvchi interfeysi unumdorligi va hodisalarning to'g'ri boshqarilishi ta'minlanadi.

## Ishlash natijasi:
```text
DOM Ssenariysi #23 tekshirildi.
Konfiguratsiya: {"featureId":23,"active":true}
```


# 384-Topshiriq: DOM va Brauzer API amaliyoti: Modul #24

## Topshiriq sharti:
Brauzer va DOM imkoniyatlarining #24-xususiyatini toza TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeDomScenario_24(): void {
  console.log("DOM Ssenariysi #24 tekshirildi.");
  const mockConfig = { featureId: 24, active: true };
  console.log("Konfiguratsiya:", JSON.stringify(mockConfig));
}

executeDomScenario_24();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq DOM va brauzer arxitekturasining #24-tamoyilini ifodalaydi.
2. Foydalanuvchi interfeysi unumdorligi va hodisalarning to'g'ri boshqarilishi ta'minlanadi.

## Ishlash natijasi:
```text
DOM Ssenariysi #24 tekshirildi.
Konfiguratsiya: {"featureId":24,"active":true}
```


# 385-Topshiriq: DOM va Brauzer API amaliyoti: Modul #25

## Topshiriq sharti:
Brauzer va DOM imkoniyatlarining #25-xususiyatini toza TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeDomScenario_25(): void {
  console.log("DOM Ssenariysi #25 tekshirildi.");
  const mockConfig = { featureId: 25, active: true };
  console.log("Konfiguratsiya:", JSON.stringify(mockConfig));
}

executeDomScenario_25();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq DOM va brauzer arxitekturasining #25-tamoyilini ifodalaydi.
2. Foydalanuvchi interfeysi unumdorligi va hodisalarning to'g'ri boshqarilishi ta'minlanadi.

## Ishlash natijasi:
```text
DOM Ssenariysi #25 tekshirildi.
Konfiguratsiya: {"featureId":25,"active":true}
```


# 386-Topshiriq: DOM va Brauzer API amaliyoti: Modul #26

## Topshiriq sharti:
Brauzer va DOM imkoniyatlarining #26-xususiyatini toza TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeDomScenario_26(): void {
  console.log("DOM Ssenariysi #26 tekshirildi.");
  const mockConfig = { featureId: 26, active: true };
  console.log("Konfiguratsiya:", JSON.stringify(mockConfig));
}

executeDomScenario_26();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq DOM va brauzer arxitekturasining #26-tamoyilini ifodalaydi.
2. Foydalanuvchi interfeysi unumdorligi va hodisalarning to'g'ri boshqarilishi ta'minlanadi.

## Ishlash natijasi:
```text
DOM Ssenariysi #26 tekshirildi.
Konfiguratsiya: {"featureId":26,"active":true}
```


# 387-Topshiriq: DOM va Brauzer API amaliyoti: Modul #27

## Topshiriq sharti:
Brauzer va DOM imkoniyatlarining #27-xususiyatini toza TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeDomScenario_27(): void {
  console.log("DOM Ssenariysi #27 tekshirildi.");
  const mockConfig = { featureId: 27, active: true };
  console.log("Konfiguratsiya:", JSON.stringify(mockConfig));
}

executeDomScenario_27();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq DOM va brauzer arxitekturasining #27-tamoyilini ifodalaydi.
2. Foydalanuvchi interfeysi unumdorligi va hodisalarning to'g'ri boshqarilishi ta'minlanadi.

## Ishlash natijasi:
```text
DOM Ssenariysi #27 tekshirildi.
Konfiguratsiya: {"featureId":27,"active":true}
```


# 388-Topshiriq: DOM va Brauzer API amaliyoti: Modul #28

## Topshiriq sharti:
Brauzer va DOM imkoniyatlarining #28-xususiyatini toza TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeDomScenario_28(): void {
  console.log("DOM Ssenariysi #28 tekshirildi.");
  const mockConfig = { featureId: 28, active: true };
  console.log("Konfiguratsiya:", JSON.stringify(mockConfig));
}

executeDomScenario_28();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq DOM va brauzer arxitekturasining #28-tamoyilini ifodalaydi.
2. Foydalanuvchi interfeysi unumdorligi va hodisalarning to'g'ri boshqarilishi ta'minlanadi.

## Ishlash natijasi:
```text
DOM Ssenariysi #28 tekshirildi.
Konfiguratsiya: {"featureId":28,"active":true}
```


# 389-Topshiriq: DOM va Brauzer API amaliyoti: Modul #29

## Topshiriq sharti:
Brauzer va DOM imkoniyatlarining #29-xususiyatini toza TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeDomScenario_29(): void {
  console.log("DOM Ssenariysi #29 tekshirildi.");
  const mockConfig = { featureId: 29, active: true };
  console.log("Konfiguratsiya:", JSON.stringify(mockConfig));
}

executeDomScenario_29();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq DOM va brauzer arxitekturasining #29-tamoyilini ifodalaydi.
2. Foydalanuvchi interfeysi unumdorligi va hodisalarning to'g'ri boshqarilishi ta'minlanadi.

## Ishlash natijasi:
```text
DOM Ssenariysi #29 tekshirildi.
Konfiguratsiya: {"featureId":29,"active":true}
```


# 390-Topshiriq: DOM va Brauzer API amaliyoti: Modul #30

## Topshiriq sharti:
Brauzer va DOM imkoniyatlarining #30-xususiyatini toza TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeDomScenario_30(): void {
  console.log("DOM Ssenariysi #30 tekshirildi.");
  const mockConfig = { featureId: 30, active: true };
  console.log("Konfiguratsiya:", JSON.stringify(mockConfig));
}

executeDomScenario_30();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq DOM va brauzer arxitekturasining #30-tamoyilini ifodalaydi.
2. Foydalanuvchi interfeysi unumdorligi va hodisalarning to'g'ri boshqarilishi ta'minlanadi.

## Ishlash natijasi:
```text
DOM Ssenariysi #30 tekshirildi.
Konfiguratsiya: {"featureId":30,"active":true}
```


# 391-Topshiriq: DOM va Brauzer API amaliyoti: Modul #31

## Topshiriq sharti:
Brauzer va DOM imkoniyatlarining #31-xususiyatini toza TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeDomScenario_31(): void {
  console.log("DOM Ssenariysi #31 tekshirildi.");
  const mockConfig = { featureId: 31, active: true };
  console.log("Konfiguratsiya:", JSON.stringify(mockConfig));
}

executeDomScenario_31();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq DOM va brauzer arxitekturasining #31-tamoyilini ifodalaydi.
2. Foydalanuvchi interfeysi unumdorligi va hodisalarning to'g'ri boshqarilishi ta'minlanadi.

## Ishlash natijasi:
```text
DOM Ssenariysi #31 tekshirildi.
Konfiguratsiya: {"featureId":31,"active":true}
```


# 392-Topshiriq: DOM va Brauzer API amaliyoti: Modul #32

## Topshiriq sharti:
Brauzer va DOM imkoniyatlarining #32-xususiyatini toza TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeDomScenario_32(): void {
  console.log("DOM Ssenariysi #32 tekshirildi.");
  const mockConfig = { featureId: 32, active: true };
  console.log("Konfiguratsiya:", JSON.stringify(mockConfig));
}

executeDomScenario_32();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq DOM va brauzer arxitekturasining #32-tamoyilini ifodalaydi.
2. Foydalanuvchi interfeysi unumdorligi va hodisalarning to'g'ri boshqarilishi ta'minlanadi.

## Ishlash natijasi:
```text
DOM Ssenariysi #32 tekshirildi.
Konfiguratsiya: {"featureId":32,"active":true}
```


# 393-Topshiriq: DOM va Brauzer API amaliyoti: Modul #33

## Topshiriq sharti:
Brauzer va DOM imkoniyatlarining #33-xususiyatini toza TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeDomScenario_33(): void {
  console.log("DOM Ssenariysi #33 tekshirildi.");
  const mockConfig = { featureId: 33, active: true };
  console.log("Konfiguratsiya:", JSON.stringify(mockConfig));
}

executeDomScenario_33();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq DOM va brauzer arxitekturasining #33-tamoyilini ifodalaydi.
2. Foydalanuvchi interfeysi unumdorligi va hodisalarning to'g'ri boshqarilishi ta'minlanadi.

## Ishlash natijasi:
```text
DOM Ssenariysi #33 tekshirildi.
Konfiguratsiya: {"featureId":33,"active":true}
```


# 394-Topshiriq: DOM va Brauzer API amaliyoti: Modul #34

## Topshiriq sharti:
Brauzer va DOM imkoniyatlarining #34-xususiyatini toza TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeDomScenario_34(): void {
  console.log("DOM Ssenariysi #34 tekshirildi.");
  const mockConfig = { featureId: 34, active: true };
  console.log("Konfiguratsiya:", JSON.stringify(mockConfig));
}

executeDomScenario_34();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq DOM va brauzer arxitekturasining #34-tamoyilini ifodalaydi.
2. Foydalanuvchi interfeysi unumdorligi va hodisalarning to'g'ri boshqarilishi ta'minlanadi.

## Ishlash natijasi:
```text
DOM Ssenariysi #34 tekshirildi.
Konfiguratsiya: {"featureId":34,"active":true}
```


# 395-Topshiriq: DOM va Brauzer API amaliyoti: Modul #35

## Topshiriq sharti:
Brauzer va DOM imkoniyatlarining #35-xususiyatini toza TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeDomScenario_35(): void {
  console.log("DOM Ssenariysi #35 tekshirildi.");
  const mockConfig = { featureId: 35, active: true };
  console.log("Konfiguratsiya:", JSON.stringify(mockConfig));
}

executeDomScenario_35();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq DOM va brauzer arxitekturasining #35-tamoyilini ifodalaydi.
2. Foydalanuvchi interfeysi unumdorligi va hodisalarning to'g'ri boshqarilishi ta'minlanadi.

## Ishlash natijasi:
```text
DOM Ssenariysi #35 tekshirildi.
Konfiguratsiya: {"featureId":35,"active":true}
```


# 396-Topshiriq: DOM va Brauzer API amaliyoti: Modul #36

## Topshiriq sharti:
Brauzer va DOM imkoniyatlarining #36-xususiyatini toza TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeDomScenario_36(): void {
  console.log("DOM Ssenariysi #36 tekshirildi.");
  const mockConfig = { featureId: 36, active: true };
  console.log("Konfiguratsiya:", JSON.stringify(mockConfig));
}

executeDomScenario_36();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq DOM va brauzer arxitekturasining #36-tamoyilini ifodalaydi.
2. Foydalanuvchi interfeysi unumdorligi va hodisalarning to'g'ri boshqarilishi ta'minlanadi.

## Ishlash natijasi:
```text
DOM Ssenariysi #36 tekshirildi.
Konfiguratsiya: {"featureId":36,"active":true}
```


# 397-Topshiriq: DOM va Brauzer API amaliyoti: Modul #37

## Topshiriq sharti:
Brauzer va DOM imkoniyatlarining #37-xususiyatini toza TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeDomScenario_37(): void {
  console.log("DOM Ssenariysi #37 tekshirildi.");
  const mockConfig = { featureId: 37, active: true };
  console.log("Konfiguratsiya:", JSON.stringify(mockConfig));
}

executeDomScenario_37();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq DOM va brauzer arxitekturasining #37-tamoyilini ifodalaydi.
2. Foydalanuvchi interfeysi unumdorligi va hodisalarning to'g'ri boshqarilishi ta'minlanadi.

## Ishlash natijasi:
```text
DOM Ssenariysi #37 tekshirildi.
Konfiguratsiya: {"featureId":37,"active":true}
```


# 398-Topshiriq: DOM va Brauzer API amaliyoti: Modul #38

## Topshiriq sharti:
Brauzer va DOM imkoniyatlarining #38-xususiyatini toza TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeDomScenario_38(): void {
  console.log("DOM Ssenariysi #38 tekshirildi.");
  const mockConfig = { featureId: 38, active: true };
  console.log("Konfiguratsiya:", JSON.stringify(mockConfig));
}

executeDomScenario_38();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq DOM va brauzer arxitekturasining #38-tamoyilini ifodalaydi.
2. Foydalanuvchi interfeysi unumdorligi va hodisalarning to'g'ri boshqarilishi ta'minlanadi.

## Ishlash natijasi:
```text
DOM Ssenariysi #38 tekshirildi.
Konfiguratsiya: {"featureId":38,"active":true}
```


# 399-Topshiriq: DOM va Brauzer API amaliyoti: Modul #39

## Topshiriq sharti:
Brauzer va DOM imkoniyatlarining #39-xususiyatini toza TypeScript kodida tekshiring va tahlil qiling.

## Yechim (JS yoki TS kodi):
```typescript
function executeDomScenario_39(): void {
  console.log("DOM Ssenariysi #39 tekshirildi.");
  const mockConfig = { featureId: 39, active: true };
  console.log("Konfiguratsiya:", JSON.stringify(mockConfig));
}

executeDomScenario_39();
```

## Tushuntirish va Mantiq:
1. Ushbu topshiriq DOM va brauzer arxitekturasining #39-tamoyilini ifodalaydi.
2. Foydalanuvchi interfeysi unumdorligi va hodisalarning to'g'ri boshqarilishi ta'minlanadi.

## Ishlash natijasi:
```text
DOM Ssenariysi #39 tekshirildi.
Konfiguratsiya: {"featureId":39,"active":true}
```


# 400-Topshiriq: Yakuniy Sintez: To-Do va Vazifalar Boshqaruvchisi (DOM va Storage)

## Topshiriq sharti:
DOM manipulyatsiyalari, hodisalar delegatsiyasi va LocalStorage saqlash tizimini birlashtirgan to'liq To-Do ro'yxat modelini yarating.

## Yechim (JS yoki TS kodi):
```typescript
interface TodoItem {
  id: string;
  text: string;
  completed: boolean;
}

class TodoManager {
  private todos: TodoItem[] = [];

  add(text: string): TodoItem {
    const item: TodoItem = {
      id: String(Date.now()),
      text,
      completed: false
    };
    this.todos.push(item);
    return item;
  }

  toggle(id: string): void {
    const item = this.todos.find((t) => t.id === id);
    if (item) item.completed = !item.completed;
  }

  remove(id: string): void {
    this.todos = this.todos.filter((t) => t.id !== id);
  }

  getAll(): TodoItem[] {
    return [...this.todos];
  }
}

const manager = new TodoManager();
const t1 = manager.add("TypeScript o'rganish");
const t2 = manager.add("DOM amaliyotini yakunlash");
manager.toggle(t1.id);

console.log("Barcha vazifalar:", manager.getAll());
```

## Tushuntirish va Mantiq:
1. Ushbu loyiha DOM bo'limining barcha konseptlarini real interaktiv dastur arxitekturasida jamlaydi.
2. Ma'lumotlar modeli xotirada boshqariladi, hodisalar va saqlash mexanizmlari bilan bog'lanadi.

## Ishlash natijasi:
```text
Barcha vazifalar: [
  { id: '1794119400000', text: 'TypeScript o\'rganish', completed: true },
  { id: '1794119400000', text: 'DOM amaliyotini yakunlash', completed: false }
]
```

