# HTML5 VA CSS3 MUKAMMAL ARXITEKTURA VA AMALIY ENSIKLOPEDIYASI

Ushbu qo'llanma zamonaviy veb-ishlab chiqishda HTML5 va CSS3 texnologiyalarining nazariy arxitekturasi, brauzer darajasidagi ishlash mexanizmlari, kaskad va selektorlar o'ziga xosligi, zamonaviy layout tizimlari (Flexbox, Grid, Subgrid), CSS metodologiyalari (BEM, ITCSS), veb unumdorligi (Web Performance & Core Web Vitals) hamda kirishlilik (Accessibility / WCAG) talablarini to'liq va tizimli qamrab olgan professional ensiklopedik qo'llanmadir.

---

## MUNDARIJA

1. [1-BOB: HTML5 Arxitekturasi, Standartlar va Semantik Tizim](#1-bob-html5-arxitekturasi-standartlar-va-semantik-tizim)
   - 1.1. Veb standartlari evolyutsiyasi (HTML4, XHTML va HTML5)
   - 1.2. DOM (Document Object Model) daraxti va parsing mexanizmi
   - 1.3. Semantik teglarning fundamental ahamiyati va taksonomiyasi
   - 1.4. Meta-ma'lumotlar, SEO, Open Graph va Viewport boshqaruvi
   - 1.5. Veb Kirishlilik (Accessibility / A11y) va WAI-ARIA standartlari
2. [2-BOB: Brauzer Renderlash Dvigatellari va Critical Rendering Path (CRP)](#2-bob-brauzer-renderlash-dvigatellari-va-critical-rendering-path-crp)
   - 2.1. Renderlash bosqichlari: HTML Parsing, CSSOM, Render Tree
   - 2.2. Layout (Reflow), Paint (Repaint) va Compositing
   - 2.3. Render-blocking resurslar va ularni bartaraf etish (async, defer, preload, preconnect)
   - 2.4. Uskunaviy tezlatish (Hardware Acceleration) va GPU qatlamlari
3. [3-BOB: CSS3 Kaskad, Meros va Specificity Nazariyasi](#3-bob-css3-kaskad-meros-va-specificity-nazariyasi)
   - 3.1. Kaskad (The Cascade) algoritmi va prioritetlar iyerarxiyasi
   - 3.2. Specificity (O'ziga xoslik) matematik hisoblash qoidalari
   - 3.3. Kaskad qatlamlari (`@layer`) arxitekturasi
   - 3.4. Merosxo'rlik (Inheritance) va uning qiymatlari (`inherit`, `initial`, `unset`, `revert`)
4. [4-BOB: Joylashuv (Layout) Modellari va Ularning Evolyutsiyasi](#4-bob-joylashuv-layout-modellari-va-ularning-evolyutsiyasi)
   - 4.1. Oddiy oqim (Normal Flow) va Box Model mexanikasi
   - 4.2. Joylashuv turlari (Static, Relative, Absolute, Fixed, Sticky) va Stacking Context (z-index)
   - 4.3. Flexbox arxitekturasi: O'qlar, Formatting Context va moslashuvchanlik matematikasi
   - 4.4. CSS Grid arxitekturasi: Ikki o'lchovli koordinata tizimi, Implicit vs Explicit, Subgrid
5. [5-BOB: Katta Loyihalarda CSS Arxitekturasi va Metodologiyalar](#5-bob-katta-loyihalarda-css-arxitekturasi-va-metodologiyalar)
   - 5.1. BEM (Block, Element, Modifier) metodologiyasi va nomlash qoidalari
   - 5.2. OOCSS, SMACSS va Utility-First yondashuvlar taqqoslovi
   - 5.3. ITCSS (Inverted Triangle CSS) fayllar strukturasi va komponentlar izolatsiyasi
6. [6-BOB: Zamonaviy CSS (Modern CSS Capabilities)](#6-bob-zamonaviy-css-modern-css-capabilities)
   - 6.1. CSS Maxsus O'zgaruvchilari (Custom Properties / CSS Variables)
   - 6.2. Ilg'or mantiqiy selektorlar: `:has()`, `:is()`, `:where()`, `:not()`, `:focus-visible`
   - 6.3. Native CSS Nesting spetsifikatsiyasi
   - 6.4. Matematik funksiyalar: `clamp()`, `min()`, `max()`, `calc()` va fluid dizayn
   - 6.5. Container Queries (`@container`) - Komponent darajasidagi responsivlik
7. [7-BOB: Responsiv Veb Dizayn va Multi-Device Strategiyalari](#7-bob-responsiv-veb-dizayn-va-multi-device-strategiyalari)
   - 7.1. Mobile-First va Desktop-First yondashuvlarining fundamental farqlari
   - 7.2. Breakpointlar strategiyasi va fluid o'lchamlar
   - 7.3. Moslashuvchan media: `<picture>`, `srcset`, zamonaviy formatlar (AVIF, WebP)
8. [8-BOB: Veb Unumdorligi (Web Performance) va Core Web Vitals](#8-bob-veb-unumdorligi-web-performance-va-core-web-vitals)
   - 8.1. Core Web Vitals metrikalari: LCP, INP, CLS va ularning CSS bilan bog'liqligi
   - 8.2. CSS kodini minifikatsiya qilish, PurgeCSS va kritikal CSS ajratish
   - 8.3. Veb shriftlar optimizatsiyasi: `@font-face`, `font-display: swap`, WOFF2
9. [9-BOB: Animatsiyalar, Mikro-Interaksiyalar va Foydalanuvchi Qulayligi](#9-bob-animatsiyalar-mikro-interaksiyalar-va-foydalanuvchi-qulayligi)
   - 9.1. Tranzitsiyalar va transformatsiyalar mexanikasi
   - 9.2. `@keyframes` animatsiyalari va unumdorlik (CPU vs GPU)
   - 9.3. Foydalanuvchi maxsus sozlamalari (`prefers-reduced-motion`, `prefers-color-scheme`)
10. [10-BOB: Professional Ishlab Chiqish Standartlari va Yakuniy Checklist](#10-bob-professional-ishlab-chiqish-standartlari-va-yakuniy-checklist)

---

## 1-BOB: HTML5 Arxitekturasi, Standartlar va Semantik Tizim

### 1.1. Veb Standartlari Evolyutsiyasi (HTML4, XHTML va HTML5)
Veb texnologiyalari rivojlanishida HTML bir nechta muhim bosqichlarni bosib o'tdi:
- **HTML 4.01 (1999)**: Veb sahifalarni vizual bezash va sodda gipermatn tuzish uchun mo'ljallangan edi. Unda ko'plab ko'rinish beruvchi teglar (`<font>`, `<center>`, `<b>`, `<i>`) mavjud bo'lib, strukturani dizayndan ajratish to'liq yo'lga qo'yilmagan edi.
- **XHTML 1.0 / 2.0 (2000-2004)**: W3C XML qoidalarini vebga kiritishga urindi. Har bir teg qat'iy yopilishi (`<br />`), atributlar qo'shtirnoqqa olinishi kerak edi. Har qanday sintaksis xatosi brauzerda "Yellow Screen of Death" (fatal xatolik) keltirib chiqarar edi. Bu real vebning moslashuvchan tabiati bilan to'qnash keldi.
- **HTML5 va WHATWG**: Apple, Mozilla va Opera muhandislari 2004-yilda WHATWG (Web Hypertext Application Technology Working Group) guruhini tuzib, pragmatik "Living Standard"ni ishlab chiqdilar. HTML5 quyidagi asosiy tamoyillarga tayandi:
  - **Moslashuvchanlik**: Mavjud veb-sahifalar buzilmasligi kerak (Backward compatibility).
  - **Ajratish**: Struktura (HTML), bezak (CSS) va xatti-harakat (JavaScript) qat'iy ajratildi.
  - **Multimediyani mahalliy qo'llab-quvvatlash**: Plaginlarsiz (Flash, Silverlight talab qilmasdan) `<video>`, `<audio>`, `<canvas>`, `<svg>` kiritildi.
  - **Semantik boylik**: Brauzer, qidiruv botlari va ekran o'quvchilarga sahifaning ichki ma'nosini tushunish imkoniyati berildi.

### 1.2. DOM Daraxti va Parsing Mexanizmi
Brauzer HTML hujjatni yuklab olganda quyidagi ketma-ketlikda DOM (Document Object Model) obyektlar modelini barpo etadi:
1. **Baytlar (Bytes)**: Tarmoqdan kelayotgan xom baytlar (`3C 68 74 6D 6C 3E...`).
2. **Belgilar (Characters)**: Baytlar belgilangan kodlash tizimi (odatda `UTF-8`) asosida matn belgilariga aylantiriladi.
3. **Tokenlar (Tokenization)**: Belgilar HTML standarti leksik qoidalari bo'yicha tokenlarga bo'linadi: `StartTag: html`, `StartTag: body`, `EndTag: html`.
4. **Tugunlar (Nodes)**: Tokenlar xususiyatlar va kontentga ega bo'lgan DOM obyektlariga (Element, Text, Comment) aylantiriladi.
5. **DOM Tree**: Tugunlar o'zaro ota-bola (parent-child) va qardoshlik (sibling) bog'liqliklari orqali yagona iyerarxik daraxtga birlashadi.

```
            [Document]
                |
             [html]
           /        \
       [head]      [body]
       /    \       /    \
   [meta] [title] [header] [main]
                    |        |
                   [h1]     [article]
```

### 1.3. Semantik Teglarning Fundamental Ahamiyati va Taksonomiyasi
Semantika — bu dasturlash elementining nafaqat vizual ko'rinishi, balki uning inson va mashina uchun ma'no-mazmunini anglatadi. Umumiy `<div>` va `<span>` teglaridan farqli o'laroq, semantik teglar sahifa strukturasini aniq belgilaydi:

| Semantik Teg | Mantiqiy Vazifasi | Ruxsat Berilgan Kontekst |
|---|---|---|
| `<header>` | Sahifa yoki bo'limning kirish qismi (logo, sarlavha, navigatsiya) | Sahifa boshida yoki `<article>`, `<section>` ichida |
| `<nav>` | Saytning asosiy navigatsion havolalar bloki | Asosiy menyular, sahifalash (pagination) |
| `<main>` | Sahifaning yagona, takrorlanmas asosiy mazmuni | Sahifada faqat BIR MARTA ishlatilishi shart |
| `<article>` | Mustaqil, alohida tarqatilishi mumkin bo'lgan kontent (maqola, post, sharh) | Blog post, yangilik xabari, mahsulot kartasi |
| `<section>` | Umumiy mavzuga ega bo'lgan mantiqiy blok (sarlavhasi bo'lishi shart) | Boblar, tematik bloklar, tab bo'limlari |
| `<aside>` | Asosiy kontentga bilvosita bog'liq yordamchi ma'lumot | Yon panel (sidebar), reklama, izohlar, muallif bio |
| `<footer>` | Mualliflik huquqi, aloqa ma'lumotlari, pastki havolalar | Sahifa oxirida yoki `<article>` so'ngida |
| `<figure>` / `<figcaption>` | Mustaqil tasvir, diagramma, kod parchasi va uning ostki izohi | Maqola illyustratsiyalari, jadvallar |
| `<time>` | Mashina o'qiy oladigan sana va vaqt | Sana va vaqt ko'rsatkichlari (`datetime="..."`) |

### 1.4. Meta-ma'lumotlar, SEO, Open Graph va Viewport Boshqaruvi
Brauzer va qidiruv tizimlari sahifani to'g'ri indekslashi va renderlashi uchun `<head>` qismidagi meta-teglar juda muhimdir:
- **Xarakterlar to'plami**: `<meta charset="UTF-8">` — Barcha tillardagi belgilarni to'g'ri ko'rsatishni ta'minlaydi.
- **Viewport**: `<meta name="viewport" content="width=device-width, initial-scale=1.0">` — Sahifa o'lchamini qurilma ekraniga moslashtirish uchun majburiy.
- **Qidiruv Tizimi Optimizatsiyasi (SEO)**:
  ```html
  <title>Zamonaviy Veb Texnologiyalari Ensiklopediyasi</title>
  <meta name="description" content="HTML5 va CSS3 arxitekturasi bo'yicha to'liq ta'limiy qo'llanma va professional spetsifikatsiya.">
  <link rel="canonical" href="https://example.uz/html-css-guide">
  ```
- **Open Graph (Ijtimoiy Tarmoqlar uchun)**: Facebook, Telegram, LinkedIn kabi tarmoqlarda link yuborilganda chiroyli preview kartasi paydo bo'lishini ta'minlaydi:
  ```html
  <meta property="og:title" content="HTML5 va CSS3 Mukammal Ensiklopediyasi">
  <meta property="og:description" content="Veb arxitekturasi va CSS metodologiyalari bo'yicha to'liq qo'llanma.">
  <meta property="og:image" content="https://example.uz/cover.jpg">
  <meta property="og:type" content="article">
  ```

### 1.5. Veb Kirishlilik (Accessibility / A11y) va WAI-ARIA Standartlari
Veb-saytlar jismoniy imkoniyati cheklangan (ko'rish, eshitish, harakatlanish imkoniyati past) insonlar uchun ham to'liq qulay bo'lishi shart:
1. **WCAG 2.1 printsiplari (POUR)**:
   - **Perceivable (Idrok etiladigan)**: Barcha vizual elementlarga matnli muqobillar (`alt="Tog' manzarasi"`).
   - **Operable (Boshqariladigan)**: Sichqonchasiz, faqat klaviatura (`Tab`, `Enter`, `Space`) orqali harakatlanish imkoniyati.
   - **Understandable (Tushunarli)**: Aniqlik, sodda til, kutilgan natija beruvchi interfeys.
   - **Robust (Mustahkam)**: Har xil brauzerlar va ekran o'quvchi (Screen Reader - NVDA, JAWS, VoiceOver) dasturlar bilan muvofiq ishlash.
2. **WAI-ARIA (Accessible Rich Internet Applications)**:
   - `aria-label="Qidirish"`: Ko'rinmas sarlavha berish.
   - `aria-expanded="false"`: Qatlam ochilgan yoki yopiqligi holati.
   - `aria-hidden="true"`: Dekorativ ikonkalar ekran o'quvchilarga o'qilmasligi uchun.
   - `role="dialog"`: Maxsus vidjetlarning semantik rolini ifodalash.

---

## 2-BOB: Brauzer Renderlash Dvigatellari va Critical Rendering Path (CRP)

### 2.1. Renderlash Bosqichlari: HTML Parsing, CSSOM, Render Tree
Brauzer (Blink, Gecko, WebKit) ekranga piksellarni chiqarish uchun bir necha qadamlarni amalga oshiradi:
1. **HTML Parsing -> DOM**: HTML matni DOM daraxtiga aylanadi.
2. **CSS Parsing -> CSSOM**: Yuklangan CSS qoidalari CSSOM (CSS Object Model) daraxtiga aylanadi. CSSOM kaskad va meros qoidalarini o'z ichiga oladi.
3. **Render Tree qurilishi**: DOM va CSSOM birlashtiriladi. Ekranda ko'rinmaydigan tugunlar (`<head>`, `<script>`, `display: none;` bo'lgan elementlar) Render Treega **kirmaydi**. Lekin `visibility: hidden;` elementlari o'rin egallagani uchun Render Treega kiradi.

### 2.2. Layout (Reflow), Paint (Repaint) va Compositing
1. **Layout (Reflow)**: Render Treedagi har bir elementning ekrandagi aniq geometrik koordinatalari (kengligi, balandligi, X va Y o'qidagi o'rni) hisoblanadi. Layout eng og'ir operatsiyalardan biridir.
2. **Paint (Repaint)**: Har bir elementning vizual piksellari chiziladi: ranglar, matnlar, chegaralar, soyalar.
3. **Compositing**: Chizilgan qatlamlar (Layers) GPU (Grafik Protsessor) yordamida birlashtirilib, ekranga yakuniy kadr sifatida uzatiladi.

```
[HTML] -> [DOM]    \
                   -> [Render Tree] -> [Layout (Reflow)] -> [Paint] -> [Composite]
[CSS]  -> [CSSOM]  /
```

> [!WARNING]
> Elementlarning `width`, `height`, `margin`, `padding`, `top`, `left` xususiyatlarini animatsiya qilish **Reflow**ni chaqiradi va CPUga katta yuk tushiradi. Animatsiyalarni doimo GPU tomonidan boshqariladigan `transform` (`translate3d`, `scale`) va `opacity` orqali bajarish kerak!

### 2.3. Render-blocking Resurslar va Ularni Bartaraf Etish
CSS render-blocking hisoblanadi: brauzer CSSOM to'liq qurilmaguncha sahifani ekranga chiqarmaydi (oq ekran turadi).
- **Skriptlar yuklanishi**: Oddiy `<script src="...">` HTML parsingni to'xtatadi.
- **`defer` atributi**: Skript fonda yuklanadi va HTML parsing to'liq tugagach, tartib bilan ishga tushadi (DOM kutuvchi skriptlar uchun eng yaxshi yechim).
- **`async` atributi**: Skript yuklanishi bilanoq darhol HTML parsingni to'xtatib ishga tushadi (tashqi tahlil tizimlari - Google Analytics uchun mos).
- **Resurs prioritizatsiyasi**:
  ```html
  <!-- DNS ulanishni oldindan o'rnatish -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <!-- Kritik resursni yuqori ustunlik bilan oldindan yuklash -->
  <link rel="preload" href="/fonts/inter.woff2" as="font" type="font/woff2" crossorigin>
  ```

### 2.4. Uskunaviy Tezlatish (Hardware Acceleration) va GPU Qatlamlari
Brauzer murakkab elementlarni alohida qatlamga (Compositing Layer) ajratishi mumkin. Buni faollashtirish:
```css
.card {
    will-change: transform, opacity;
    transform: translateZ(0); /* Qatlamni GPU xotirasiga yuklash */
}
```
`will-change` brauzerga qaysi xususiyat o'zgarishini oldindan bildiradi, bu orqali brauzer kadr tushib qolishini (jank) oldini oladi.

---

## 3-BOB: CSS3 Kaskad, Meros va Specificity Nazariyasi

### 3.1. Kaskad (The Cascade) Algoritmi
CSS (Cascading Style Sheets) nomi bejizga kaskad deb atalmagan. Bir elementga bir nechta qarama-qarshi uslublar berilganda, brauzer quyidagi ustunlik zanjiri bo'yicha g'olib qoidani aniqlaydi:
1. **Muhimlik va Manba (Importance & Origin)**:
   - Brauzer standart uslublari (User Agent Stylesheet).
   - Foydalanuvchi maxsus uslublari (User Stylesheet).
   - Muallif uslublari (Author Stylesheet - biz yozgan CSS).
   - Muallif `!important` uslublari.
   - Foydalanuvchi `!important` uslublari (Eng yuqori kuchga ega).
2. **Kaskad qatlamlari (`@layer`)**: Quyi qatlamlar yuqori qatlamlarga bo'ysunadi.
3. **Specificity (O'ziga xoslik darajasi)**: Selektorlarning kuchi.
4. **Kod Tartibi (Order of Appearance)**: Bir xil kuchga ega qoidalar ichida kodda oxirgi yozilgani g'olib chiqadi.

### 3.2. Specificity (O'ziga xoslik) Matematik Hisoblash Qoidalari
Specificity to'rtta qiymatdan iborat kortej ko'rinishida hisoblanadi: `(A, B, C, D)`:

- **A (Inline uslublar)**: HTML elementining `style="..."` atributi ichida yozilgan uslublar. Qiymati: `(1, 0, 0, 0)`.
- **B (ID selektorlar)**: Masalan `#header`, `#main-nav`. Qiymati: `(0, 1, 0, 0)`.
- **C (Class, Attribute, Pseudo-class)**: Masalan `.btn`, `[type="text"]`, `:hover`, `:nth-child(2)`. Qiymati: `(0, 0, 1, 0)`.
- **D (Element va Pseudo-element)**: Masalan `div`, `p`, `h1`, `::before`, `::after`. Qiymati: `(0, 0, 0, 1)`.

> [!NOTE]
> Universal selektor (`*`), kombinatorlar (`+`, `>`, `~`) va `:where()` psevdo-sinfi specificityga ta'sir qilmaydi `(0, 0, 0, 0)`.
> `:is()`, `:not()` va `:has()` esa argumentlari ichidagi eng og'ir selektor kuchini oladi.

#### Misollar taqqoslovi:
1. `nav ul li a` -> 4 ta element -> `(0, 0, 0, 4)`
2. `.nav-item .nav-link` -> 2 ta klass -> `(0, 0, 2, 0)` -> **G'olib (1-ga nisbatan)**
3. `#main-nav a:hover` -> 1 ta ID, 1 ta psevdo-klass, 1 ta element -> `(0, 1, 1, 1)` -> **G'olib (2-ga nisbatan)**

### 3.3. Kaskad Qatlamlari (`@layer`) Arxitekturasi
Zamonaviy CSSda selektorlar o'rtasidagi "urush" (specificity wars) muammosini hal qilish uchun `@layer` joriy etildi:
```css
@layer reset, base, components, utilities;

@layer utilities {
    .hidden { display: none; } /* Oxirgi qatlam har doim avvalgilardan ustun */
}

@layer components {
    .card { background: white; padding: 20px; }
}
```
`@layer` yordamida kutubxonalar va tashqi freymvorklar uslublarini o'z loyihangizdan ajratib, nazorat ostiga olish mumkin.

### 3.4. Merosxo'rlik (Inheritance)
Ba'zi CSS xususiyatlari ota elementdan bola elementlarga avtomatik meros bo'lib o'tadi (`color`, `font-family`, `line-height`), boshqalari esa o'tmaydi (`margin`, `padding`, `border`, `background`).
Maxsus qiymatlar:
- `inherit`: Xususiyatni ota elementdan majburiy meros qilib oladi.
- `initial`: Xususiyatni CSS spetsifikatsiyasidagi birlamchi holatiga qaytaradi.
- `unset`: Agar xususiyat meros bo'ladigan bo'lsa `inherit`, aks holda `initial` qiladi.
- `revert`: Brauzerning dastlabki standart uslubiga qaytaradi.

---

## 4-BOB: Joylashuv (Layout) Modellari va Ularning Evolyutsiyasi

### 4.1. Oddiy Oqim (Normal Flow) va Box Model Mexanikasi
Standart holatda blok elementlar tepadan pastga, inline elementlar esa chapdan o'ngga qarab oqadi.

**Box Model to'rtta konsentrik to'rtburchakdan iborat**:
1. **Content**: Matn yoki tasvir joylashgan maydon.
2. **Padding**: Kontent va chegara orasidagi ichki bo'shliq.
3. **Border**: Elementning chegarasi.
4. **Margin**: Element va unga qo'shni elementlar orasidagi tashqi masofa.

```
+---------------------------+
|          Margin           |
|  +---------------------+  |
|  |       Border        |  |
|  |  +---------------+  |  |
|  |  |    Padding    |  |  |
|  |  |  +---------+  |  |  |
|  |  |  | Content |  |  |  |
|  |  |  +---------+  |  |  |
|  |  +---------------+  |  |
|  +---------------------+  |
+---------------------------+
```

> [!IMPORTANT]
> **Standart `box-sizing: content-box` muammosi**: `width: 200px; padding: 20px; border: 5px solid;` bo'lganda, elementning real kengligi `200 + 40 + 10 = 250px` bo'ladi.
> **Zamonaviy yechim**: Loyihaning eng boshida quyidagi qoidani qo'yish shart:
> ```css
> *, *::before, *::after {
>     box-sizing: border-box;
> }
> ```
> Bu holda ko'rsatilgan `width: 200px` ichiga padding va border avtomatik kiritiladi.

### 4.2. Joylashuv Turlari (Positioning) va Stacking Context
- `static`: Standart oqim, `top/left/right/bottom/z-index` ta'sir qilmaydi.
- `relative`: Standart oqimdagi o'z o'rniga nisbatan siljiydi, uning dastlabki o'rni saqlanib qoladi.
- `absolute`: Eng yaqin `position: relative/absolute/fixed/sticky` bo'lgan ota konteynerga nisbatan siljiydi, oddiy oqimdan butunlay chiqib ketadi.
- `fixed`: Brauzer ko'rish maydoni (viewport)ga bog'lanadi, sahifa aylantirilganda (scroll) o'z joyida qoladi.
- `sticky`: Oddiy oqimda harakatlanadi, belgilangan chegaraga yetganda `fixed` kabi "yopishib" qoladi.

**Stacking Context (Qatlamlar z-index konteksti)**:
Elementlarning ustma-ust ko'rinish tartibini boshqaradi. Yangi stacking context quyidagi hollarda hosil bo'ladi:
- `position: relative/absolute` va `z-index` qiymati `auto` bo'lmaganda;
- `opacity < 1`;
- `transform`, `filter`, `perspective`, `clip-path` mavjud bo'lganda;
- `isolation: isolate;` qo'llanilganda.

### 4.3. Flexbox Arxitekturasi (1D Layout)
Flexbox elementlarni bitta o'q (yoki gorizontal, yoki vertikal) bo'ylab moslashuvchan taqsimlash uchun mo'ljallangan.
- **Asosiy o'q (Main Axis)**: `flex-direction: row` (standart) yoki `column`.
- **Ko'ndalang o'q (Cross Axis)**: Asosiy o'qqa perpendikulyar yo'nalish.
- **Tenglashtirish xususiyatlari**:
  - `justify-content`: Asosiy o'q bo'ylab elementlarni tarqatish (`flex-start`, `center`, `space-between`, `space-around`, `space-evenly`).
  - `align-items`: Ko'ndalang o'q bo'ylab qator ichida tekislash (`stretch`, `center`, `flex-start`, `flex-end`).
  - `align-content`: Ko'p qatorli o'ralishda (`flex-wrap: wrap`) butun qatorlarni tekislash.
- **Moslashuvchanlik matematikasi (Flex Item Properties)**:
  - `flex-grow: <number>`: Bo'sh qolgan joyni proporsional bo'lishib olish koeffitsiyenti.
  - `flex-shrink: <number>`: Joy yetmaganda elementning siqilish koeffitsiyenti.
  - `flex-basis: <length>`: Elementning boshlang'ich asosiy o'lchami.
  - Qisqartma: `flex: 1 1 auto;` yoki `flex: 0 0 250px;`.

### 4.4. CSS Grid Arxitekturasi (2D Layout)
CSS Grid bir vaqtning o'zida ham qatorlar, ham ustunlar bilan ishlash imkoniyatini beruvchi to'liq ikki o'lchovli koordinata tizimidir.
- **Fr birligi (Fractional unit)**: Bo'sh maydonning erkin ulushini ifodalaydi (`1fr 2fr 1fr`).
- **Funksiyalar**:
  - `repeat(auto-fit, minmax(280px, 1fr))`: Element soniga va ekran hajmiga qarab avtomatik moslashuvchi eng mashhur responsiv grid shabloni.
  - `gap: 20px`: Qator va ustunlar orasidagi masofa.
- **Grid Template Areas**: Sahifa dizaynini vizual kodlash imkoniyati:
  ```css
  .dashboard {
      display: grid;
      grid-template-columns: 260px 1fr;
      grid-template-rows: auto 1fr auto;
      grid-template-areas:
          "sidebar header"
          "sidebar main"
          "sidebar footer";
  }
  ```
- **Subgrid (`grid-template-columns: subgrid;`)**: Ichki elementlarning ota konteyner grid chiziqlariga to'liq bog'lanishini ta'minlaydi.

---

## 5-BOB: Katta Loyihalarda CSS Arxitekturasi va Metodologiyalar

### 5.1. BEM (Block, Element, Modifier) Metodologiyasi
Yandex tomonidan ishlab chiqilgan va dunyo standartiga aylangan eng mustahkam CSS metodologiyasi.

1. **Block (Blok)**: Mustaqil, alohida ma'noga ega bo'lgan tashqi komponent.
   - Masalan: `.card`, `.button`, `.nav`, `.modal`.
2. **Element (Element)**: Blokning ajralmas qismi bo'lib, undan tashqarida ma'noga ega emas. Ikki pastki chiziq bilan yoziladi `__`:
   - Masalan: `.card__title`, `.card__image`, `.card__button`.
3. **Modifier (Modifikator)**: Blok yoki elementning holatini, ko'rinishini yoki hajmini o'zgartiruvchi belgi. Ikki chiziqcha bilan yoziladi `--`:
   - Masalan: `.button--primary`, `.button--disabled`, `.card--highlighted`.

```html
<!-- BEM Namuna Strukturasi -->
<article class="card card--featured">
    <img class="card__thumbnail" src="photo.jpg" alt="...">
    <div class="card__body">
        <h3 class="card__title">CSS Arxitekturasi</h3>
        <p class="card__description">BEM orqali kodni modulli tashkil etish usuli.</p>
        <button class="card__btn card__btn--active">Batafsil</button>
    </div>
</article>
```

#### BEM Afzalliklari:
- Specificity har doim 1 ta klass darajasida saqlanadi `(0, 0, 1, 0)`.
- Kaskad ziddiyatlari va global nomlar to'qnashuvi butunlay bartaraf etiladi.
- Komponentlar mustaqil bo'lib, loyihaning istalgan joyiga oson ko'chiriladi.

### 5.2. OOCSS, SMACSS va Utility-First Yondashuvlar Taqqoslovi
- **OOCSS (Object-Oriented CSS)**: Strukturani ko'rinishdan ajratish (`.btn` + `.btn-blue`).
- **SMACSS (Scalable and Modular Architecture for CSS)**: CSSni 5 ta toifaga bo'ladi: Base, Layout, Module, State, Theme.
- **Utility-First (Tailwind CSS)**: Oldindan tayyorlangan kichik yordamchi sinflar (`flex`, `p-4`, `text-center`) orqali yangi CSS yozmasdan to'g'ridan-to'g'ri HTMLda interfeys qurish.

### 5.3. ITCSS (Inverted Triangle CSS) Arxitekturasi
Katta hajmdagi korporativ loyihalarda CSS fayllarini specificity va ko'lam o'sishi bo'yicha piramida shaklida tashkil etish:
1. **Settings**: Global o'zgaruvchilar, ranglar palitrasi, shrift o'lchamlari.
2. **Tools**: Miksinlar va funksiyalar.
3. **Generic**: CSS Reset va Normalize qoidalari.
4. **Elements**: Qizil chiziqsiz teglar (`h1`, `a`, `body`).
5. **Objects**: O'lcham va joylashuv skeletlari (Grid tizimi, Media obyekt).
6. **Components**: BEM bloklari (`.card`, `.btn`, `.navbar`).
7. **Utilities / Trumps**: Yuqori darajadagi yordamchi klasslar (`.u-text-center`, `!important` bilan).

---

## 6-BOB: Zamonaviy CSS (Modern CSS Capabilities)

### 6.1. CSS Maxsus O'zgaruvchilari (Custom Properties / CSS Variables)
CSS o'zgaruvchilari SASS o'zgaruvchilaridan farqli o'laroq brauzer xotirasida dinamik yashaydi va DOM daraxti bo'ylab meros oladi:
```css
:root {
    --primary-color: #3b82f6;
    --surface-bg: #ffffff;
    --text-color: #1e293b;
    --radius-sm: 8px;
    --font-heading: 'Inter', sans-serif;
}

[data-theme="dark"] {
    --surface-bg: #0f172a;
    --text-color: #f8fafc;
}

.button {
    background-color: var(--primary-color);
    border-radius: var(--radius-sm);
    color: #ffffff;
}
```

### 6.2. Ilg'or Mantiqiy Selektorlar
- **`:has()` (CSS Parent Selector)**: Farzandining holatiga qarab ota elementni uslublash.
  ```css
  /* Ichida xatolik bo'lgan inputni ushlab turgan form bloki */
  .form-group:has(input:invalid) {
      border-left: 4px solid #ef4444;
  }
  ```
- **`:is()` va `:where()`**: Selektorlar guruhini qisqartirish. `:is()` argumentidagi eng yuqori specificityni oladi, `:where()` esa har doim `0` specificityga ega bo'ladi.
- **`:focus-visible`**: Tugma sichqoncha bilan bosilganda noo'rin kontur (outline) chiqmasligi, lekin faqat klaviatura (`Tab`) orqali fokuslanganda yorqin kontur paydo bo'lishini ta'minlaydi.

### 6.3. Native CSS Nesting
Zamonaviy CSS endi SASS/SCSS o'rnatmasdan turib ichma-ich yozishni to'liq qo'llab-quvvatlaydi:
```css
.card {
    background-color: var(--surface-bg);
    padding: 24px;

    & .card__title {
        font-size: 1.5rem;
        margin-bottom: 12px;
    }

    &:hover {
        transform: translateY(-4px);
    }

    @media (max-width: 768px) {
        padding: 16px;
    }
}
```

### 6.4. Matematik Funksiyalar va Fluid Dizayn
- **`clamp(MIN, PREFERRED, MAX)`**: Ekran o'lchamiga qarab dinamik silliq o'zgaruvchi matn va o'lchamlar.
  ```css
  h1 {
      /* Minimal 2rem, maksimal 4rem, ekranga qarab 5vw */
      font-size: clamp(2rem, 5vw, 4rem);
  }
  ```
- **`min()` va `max()`**: Eng kichik yoki eng katta qiymatni tanlash.

### 6.5. Container Queries (`@container`)
Media Queries butun brauzer ekraniga (`viewport`) qaraydi. Container Queries esa komponent joylashtirilgan ota blokning kengligiga qaraydi:
```css
.sidebar {
    container-type: inline-size;
}

@container (max-width: 400px) {
    .card {
        flex-direction: column; /* Sidebar kichrayganda kartochka ustun holatiga o'tadi */
    }
}
```

---

## 7-BOB: Responsiv Veb Dizayn va Multi-Device Strategiyalari

### 7.1. Mobile-First vs Desktop-First
- **Mobile-First (Tavsiya etiladi)**: Birlamchi uslublar kichik ekranlar (mobil telefonlar) uchun yoziladi. Katta ekranlar uchun `min-width` orqali kengaytirib boriladi. Bu unumdorlikni oshiradi va ortiqcha kodlarni kamaytiradi.
- **Desktop-First**: Katta ekranlar uchun yozilib, `max-width` orqali qisqartirib boriladi.

### 7.2. Breakpointlar Standartlari
Qurilmalarga emas, balki kontentning buzilish nuqtalariga qarab breakpoint tanlash:
- `sm`: `640px` (Katta smartfonlar)
- `md`: `768px` (Planshetlar)
- `lg`: `1024px` (Noutbuklar va kichik monitorlar)
- `xl`: `1280px` (Desktop kompyuterlar)
- `2xl`: `1536px` (Ultra keng ekranlar)

### 7.3. Moslashuvchan Media Arxitekturasi
Tasvirlarni turli ekran zichligi (Retina 2x/3x) va qurilmalar uchun moslashtirish:
```html
<picture>
    <source srcset="hero-large.avif 1200w, hero-medium.avif 800w" type="image/avif">
    <source srcset="hero-large.webp 1200w, hero-medium.webp 800w" type="image/webp">
    <img src="hero-fallback.jpg" 
         alt="Loyiha taqdimoti" 
         loading="lazy" 
         decoding="async" 
         width="1200" 
         height="630">
</picture>
```
`width` va `height` atributlarini berish orqali rasm yuklanishidan oldin ekranda uning o'rni ajratiladi va **CLS (Cumulative Layout Shift)** oldi olinadi.

---

## 8-BOB: Veb Unumdorligi (Web Performance) va Core Web Vitals

### 8.1. Core Web Vitals Metrikalari
Google tomonidan veb-sayt foydalanuvchi tajribasini (UX) baholash uchun belgilangan asosiy metrikalar:
1. **LCP (Largest Contentful Paint)**: Sahifadagi eng katta kontent (katta banner, h1 sarlavha) ekranda paydo bo'lish vaqti. Maqsad: **< 2.5 soniya**.
2. **INP (Interaction to Next Paint)**: Foydalanuvchi sahifadagi tugma yoki elementni bosgandan so'ng brauzer yangi kadrni chizib berish tezligi. Maqsad: **< 200 ms**.
3. **CLS (Cumulative Layout Shift)**: Sahifa yuklanayotganda elementlarning to'satdan siljib ketish koeffitsiyenti. Maqsad: **< 0.1**.

### 8.2. CSS Kodini Optimizatsiya Qilish
- **Critical CSS Inlining**: Sahifaning "Above the Fold" (ekranning birinchi ko'rinadigan qismi) uslublarini to'g'ridan-to'g'ri `<style>` tegi ichida HTMLga joylash, qolgan qismini esa asinxron yuklash.
- **Ishlatilmaydigan CSSni tozalash (PurgeCSS / UnCSS)**: Ishlab chiqarish (Production) bosqichida loyihada ishlatilmagan selektorlarni yo'qotish orqali fayl hajmini 80-90% gacha qisqartirish.
- **Siqish (Compression)**: Server darajasida CSS fayllarni Gzip yoki Brotli algoritmi bilan siqib yuborish.

### 8.3. Veb Shriftlar Optimizatsiyasi
Noto'g'ri yuklangan shriftlar FOIT (Flash of Invisible Text) yoki FOUT (Flash of Unstyled Text) muammosini keltirib chiqaradi.
```css
@font-face {
    font-family: 'Geist';
    src: url('/fonts/geist-regular.woff2') format('woff2');
    font-weight: 400;
    font-style: normal;
    font-display: swap; /* Standart shrift darhol ko'rinadi, veb shrift yuklangach almashtiriladi */
}
```

---

## 9-BOB: Animatsiyalar, Mikro-Interaksiyalar va Foydalanuvchi Qulayligi

### 9.1. Tranzitsiyalar va Transformatsiyalar
Silliq o'tishlar interfeysni tirik va tushunarli qiladi:
- **`transition: property duration timing-function delay;`**
- `cubic-bezier(0.4, 0, 0.2, 1)`: Tabiiy tezlanish va sekinlashish egri chiziqlari.
- `transform`: `translateX()`, `translateY()`, `scale()`, `rotate()` — Layoutni buzmagan holda vizual o'zgarish beradi.

### 9.2. `@keyframes` va Animatsiyalar Mexanikasi
Murakkab ko'p bosqichli ssenariylar uchun:
```css
@keyframes pulseGlow {
    0% {
        transform: scale(1);
        box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.7);
    }
    70% {
        transform: scale(1.03);
        box-shadow: 0 0 0 16px rgba(59, 130, 246, 0);
    }
    100% {
        transform: scale(1);
        box-shadow: 0 0 0 0 rgba(59, 130, 246, 0);
    }
}

.glow-btn {
    animation: pulseGlow 2s infinite ease-in-out;
}
```

### 9.3. Foydalanuvchi Shaxsiy Sozlamalari (User Preferences)
Zamonaviy interfeys foydalanuvchining operatsion tizim sozlamalarini hurmat qilishi shart:
- **`prefers-reduced-motion`**: Vestibulyar apparati sezgir bo'lgan insonlar uchun ortiqcha harakatlarni to'xtatish:
  ```css
  @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after {
          animation-duration: 0.01ms !important;
          animation-iteration-count: 1 !important;
          transition-duration: 0.01ms !important;
          scroll-behavior: auto !important;
      }
  }
  ```
- **`prefers-color-scheme`**: Tizim darajasidagi Qorong'i / Yorug' rejimni avtomatik aniqlash.

---

## 10-BOB: Professional Ishlab Chiqish Standartlari va Yakuniy Checklist

Yuqori darajadagi professional veb-sahifani yakunlashdan oldin quyidagi tekshiruvlar ro'yxatidan o'tish tavsiya etiladi:

### HTML & Semantika Tekshiruvi:
- [ ] `<!DOCTYPE html>` e'lon qilingan va `<html lang="uz">` tili to'g'ri ko'rsatilgan.
- [ ] `<head>` ichida `<meta charset="UTF-8">` va moslashuvchan `<meta name="viewport">` mavjud.
- [ ] Sahifada faqat bitta `<h1>` va bitta `<main>` tegi ishlatilgan.
- [ ] Vizual barcha `<img>` teglari mazmunli `alt="..."` atributiga ega (dekorativ tasvirlarda `alt=""`).
- [ ] Formalarda barcha `<input>` elementlari `<label>` bilan uzviy bog'langan (`for="..."` va `id="..."`).
- [ ] Tugmalar `<button type="button|submit">`, boshqa sahifaga o'tishlar esa `<a href="...">` orqali yaratilgan (div yoki spanga onClick berilmagan).

### CSS & Arxitektura Tekshiruvi:
- [ ] Global darajada `*, *::before, *::after { box-sizing: border-box; }` kiritilgan.
- [ ] CSS selektorlari BEM qoidalari bo'yicha nomlangan, chuqur zanjirlar (`div > ul > li > a`) ishlatilmagan.
- [ ] O'zboshimchalik bilan `!important` va haddan tashqari yuqori `z-index: 999999` qo'llanilmagan.
- [ ] Ranglar, masofalar va shriftlar CSS maxsus o'zgaruvchilariga (`var(--...)`) ajratilgan.
- [ ] Matn va fon ranglari kontrasti WCAG AA standarti (kamida 4.5:1 nisbat) talablariga javob beradi.

### Responsivlik va Unumdorlik:
- [ ] Mobil ekranda (320px dan boshlab) gorizontal aylanma yo'lakcha (Horizontal Scrollbar) paydo bo'lmaydi.
- [ ] Shriftlar `font-display: swap` bilan yuklangan, og'ir formatlar (TTF, OTF) o'rniga WOFF2 ishlatilgan.
- [ ] Animatsiyalar faqat `transform` va `opacity` xususiyatlarida ishlaydi.
- [ ] `prefers-reduced-motion` media qoidasi orqali harakatga sezgir foydalanuvchilar holati hisobga olingan.

---

Ushbu ensiklopediya HTML va CSS bo'yicha tayyorlangan 1,000 ta amaliy topshiriqlar to'plami bilan to'liq uyg'unlikda ishlaydi hamda har qanday darajadagi dasturchi uchun fundamental va chuqur ma'lumot manbai hisoblanadi.
