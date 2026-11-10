# Solidity: Mukammal Ensiklopediya va Fundamental Qo'llanma
**Loyiha:** Khorazmiy AI — O'zbek Tilidagi Katta Dasturlash Dataseti  
**Muallif:** Khorazmiy AI Blockchain & Smart Contract Specialist  
**Versiya:** Solidity 0.8.20+ / EVM Shanghai & Cancun (2026-yil holatiga)  
**Qamrovi:** Ethereum Virtual Machine (EVM) arxitekturasi, Smart kontraktlar, Xotira modeli (Storage, Memory, Calldata, Stack), ERC-20, ERC-721, ERC-1155 standartlari, Upgradeable proksi kontraktlar (UUPS, Transparent), DeFi primitivlari (AMM, Staking, Flash Loans), Gas optimizatsiyasi (Gas Golfing), Kriptografik tekshiruvlar (Merkle Trees, ECDSA) va Smart kontraktlar xavfsizligi (Hujumlar va ulardan himoyalanish).

---

## Mundarija
1. [Kirish va Blokcheyn hamda Ethereum Falsafasi](#1-kirish-va-blokcheyn-hamda-ethereum-falsafasi)
2. [EVM (Ethereum Virtual Machine) Arxitekturasi va Opkodlar](#2-evm-ethereum-virtual-machine-arxitekturasi-va-opkodlar)
3. [Xotira Modeli: Storage, Memory, Calldata va Stack](#3-xotira-modeli-storage-memory-calldata-va-stack)
4. [Solidity Sintaksisi, Tiplar Tizimi va Global O'zgaruvchilar](#4-solidity-sintaksisi-tiplar-tizimi-va-global-ozgaruvchilar)
5. [Funksiyalar, Ko'rinish Doiralari va Holat Mutabilligi](#5-funksiyalar-korinish-doiralari-va-holat-mutabilligi)
6. [Kirish Nazorati (Access Control) va Modifikatorlar](#6-kirish-nazorati-access-control-va-modifikatorlar)
7. [Merosxo'rlik, Polimorfizm va Interfeyslar](#7-merosxorlik-polimorfizm-va-interfeyslar)
8. [Efir Qabul Qilish va Yuborish: receive, fallback, call vs transfer](#8-efir-qabul-qilish-va-yuborish-receive-fallback-call-vs-transfer)
9. [Token Standartlari: ERC-20, ERC-721 va ERC-1155](#9-token-standartlari-erc-20-erc-721-va-erc-1155)
10. [Yangilanuvchi Kontraktlar (Upgradeable Proxies)](#10-yangilanuvchi-kontraktlar-upgradeable-proxies)
11. [DeFi Muhandisligi: Staking, AMM va Flash Loans](#11-defi-muhandisligi-staking-amm-va-flash-loans)
12. [Smart Kontraktlar Xavfsizligi va Eng Xavfli Zaifliklar](#12-smart-kontraktlar-xavfsizligi-va-eng-xavfli-zaifliklar)
13. [Gas Optimizatsiyasi San'ati (Gas Golfing)](#13-gas-optimizatsiyasi-sanati-gas-golfing)
14. [Inline Assembly va Yul Tili](#14-inline-assembly-va-yul-tili)
15. [Kriptografiya, Oracllar va EIP Standartlari](#15-kriptografiya-oracllar-va-eip-standartlari)

---

## 1. Kirish va Blokcheyn hamda Ethereum Falsafasi

Ethereum — bu taqsimlangan holat mashinasi (Decentralized State Machine) bo'lib, uning holatini o'zgartiruvchi ko'rsatmalar smart kontraktlar (aqlli shartnomalar) orqali bajariladi. Solidity tili Gavin Wood boshchiligidagi Ethereum asoschilari tomonidan 2014-yilda ishlab chiqilgan bo'lib, bugungi kunda EVM asosidagi barcha tarmoqlarda (Ethereum, Polygon, Arbitrum, Optimism, BNB Chain, Avalanche) eng asosiy dasturlash tili hisoblanadi.

### Smart Kontraktlarning Muhim Xususiyatlari:
- **Determinizm (Deterministic Execution):** Bir xil boshlang'ich holat va bir xil tranzaksiya barcha nodlarda 100% bir xil natija berishi shart. Shuning uchun EVM-da tasodifiy sonlar (`random`) yoki tashqi internetga to'g'ridan-to'g'ri so'rov yuborish (HTTP) imkoni yo'q.
- **Turing-To'liqligi va Gas Konsepsiyasi:** EVM cheksiz tsikllar (infinite loops) orqali tarmoqni to'xtatib qo'yishdan saqlanish uchun har bir opkod bajarilishiga "Gas" to'lovini joriy qilgan. Agar hisoblash jarayonida foydalanuvchi taqdim etgan gas tugasa, barcha holat o'zgarishlari bekor qilinadi (`Out of Gas`).
- **O'zgarmaslik (Immutability):** Blokcheynga joylashtirilgan smart kontrakt kodini o'zgartirib bo'lmaydi (agar maxsus proksi andozasi ishlatilmagan bo'lsa).

---

## 2. EVM (Ethereum Virtual Machine) Arxitekturasi va Opkodlar

EVM — bu 256-bitli so'z uzunligiga (word size) ega bo'lgan kvazi-Turing to'liq stek mashinasidir (stack-based architecture):
- **Stek chuqurligi:** Maksimal 1024 ta element. Har bir element 256 bit (32 bayt).
- **Stack Too Deep xatosi:** Agar bitta funksiya ichida bir vaqtning o'zida 16 tadan ortiq lokal o'zgaruvchiga murojaat qilinsa, EVM ko'rsatmalari (`SWAP1` - `SWAP16`, `DUP1` - `DUP16`) yetishmay qoladi va kompilyatsiya xatosi ro'y beradi.
- **Opkodlar:** EVM baytkodi 1 baytlik ko'rsatmalardan iborat (`ADD` = 0x01, `SLOAD` = 0x54, `SSTORE` = 0x55, `REVERT` = 0xFD).

---

## 3. Xotira Modeli: Storage, Memory, Calldata va Stack

Solidity tilida xotiraning 4 ta asosiy qatlami mavjud:

| Xotira Qatlami | Saqlanish Joyi | Hayot Davomiyligi | Gas Narxi | Tavsifi |
|---|---|---|---|---|
| **Storage** | Blokcheyn Holat Daraxti (Merkle Patricia) | Doimiy (Persistent) | Juda qimmat (20,000 gas yangi slot) | Kontrakt holat o'zgaruvchilari saqlanadi. 32-baytlik slotlarga bo'linadi. |
| **Memory** | Nod RAM xotirasi | Faqat funksiya bajarilishi davomida | O'rtacha (Kengayish kvadratik qimmatlashadi) | Vaqtinchalik hisob-kitoblar va ob'ektlar uchun. |
| **Calldata** | Tranzaksiya kiruvchi xom baytlari | O'zgarmas (Read-only) | Eng arzon | External funksiyalarga kelgan argumentlar. Ko'chirilmaydi. |
| **Stack** | EVM hisoblash stegi | Opkod bajarilishi paytida | Minimal | Registr vazifasini o'taydi. |

---

## 4. Solidity Sintaksisi, Tiplar Tizimi va Global O'zgaruvchilar

Solidity statik tiplanadigan til bo'lib, uning sintaksisi C++ va JavaScript-ga yaqin:
- **`uint` va `int`**: `uint8` dan `uint256` gacha (8 ning karralari). Default `uint` = `uint256`.
- **`address`**: 20 baytlik Ethereum manzili. `address payable` esa efir (ETH) qabul qila oladi va `.transfer()`, `.send()` metodlariga ega.
- **Global ob'ektlar:**
  - `msg.sender`: Tranzaksiyani bevosita chaqirgan manzil.
  - `msg.value`: Kontraktga yuborilgan wei miqdori.
  - `block.timestamp`: Joriy blok vaqti (Unix sekundlarida).
  - `tx.origin`: Tranzaksiyani boshlagan tashqi hamyon (EOA). *Xavfsizlik nuqtai nazaridan kirish nazorati uchun ishlatilmasligi kerak!*

---

## 5. Funksiyalar, Ko'rinish Doiralari va Holat Mutabilligi

### Ko'rinish Doiralari (Visibility):
- `public`: Tashqaridan (tranzaksiya orqali) va kontrakt ichidan chaqirish mumkin.
- `external`: Faqat tashqaridan (tranzaksiya yoki boshqa kontrakt) chaqirish mumkin. Katta massiv argumentlar uchun gas tejaydi (calldata ishlatadi).
- `internal`: Faqat joriy kontrakt va undan meros olgan sinflar ichida chaqiriladi.
- `private`: Faqat ushbu kontrakt ichida chaqiriladi, merosxo'rlarga ko'rinmaydi.

### Holat Mutabilligi (State Mutability):
- `pure`: Hech qanday blockchain holatini o'qimaydi va o'zgartirmaydi (faqat kiritilgan argumentlar bilan hisoblash qiladi).
- `view`: Blockchain holatini faqat o'qiydi, lekin hech qanday holatni o'zgartirmaydi (gas tekin, agar tranzaksiya ichida bo'lmasa).
- Oddiy (non-payable): Holatni o'zgartiradi, lekin efir qabul qilmaydi.
- `payable`: Kontraktga efir (ETH) qabul qila oladi.

---

## 6. Kirish Nazorati (Access Control) va Modifikatorlar

Modifikatorlar (`modifier`) funksiya bajarilishidan oldin yoki keyin shartlarni tekshirish uchun xizmat qiladi:
- `_;` (merge point) — asosiy funksiya tanasi qachon bajarilishini belgilaydi.
- OpenZeppelin `Ownable` va `AccessControl` (RBAC — Role-Based Access Control) kutubxonalari orqali administrator, operator va minter rollarini xavfsiz boshqarish.

---

## 7. Merosxo'rlik, Polimorfizm va Interfeyslar

- `is` kalit so'zi orqali ko'p karrali merosxo'rlik (Multiple Inheritance) qo'llab-quvvatlanadi.
- **C3 Linearization:** Agar bir nechta ota kontraktlarda bir xil funksiya bo'lsa, Solidity ularni qat'iy tartibda birlashtiradi.
- `virtual` — qayta yozilishi mumkin bo'lgan funksiyalar.
- `override` — ota funksiyani qayta yozishni tasdiqlash.
- `interface` — funksiya tanasisiz faqat imzolar e'lon qilinadi, boshqa kontraktlar bilan integratsiya uchun shartnoma interfeysini shakllantiradi.

---

## 8. Efir Qabul Qilish va Yuborish: receive, fallback, call vs transfer

Kontraktga to'g'ridan-to'g'ri efir kelganda:
1. `receive() external payable`: Bo'sh `msg.data` bilan efir kelganda ishlaydi.
2. `fallback() external payable`: Mos keluvchi funksiya imzosi topilmaganda yoki ma'lumotlar bilan efir kelganda ishlaydi.

### Efir Yuborishning 3 Usuli:
- `addr.transfer(amount)`: 2300 gas limitiga ega, xato bo'lsa avtomatik revert bo'ladi (eskirgan va tavsiya etilmaydi).
- `addr.send(amount)`: 2300 gas, `bool success` qaytaradi.
- `(bool success, ) = addr.call{value: amount}("")`: Zamonaviy va tavsiya etiladigan standart usul. Barcha qolgan gasni uzatadi va reentrancy himoyasi bilan birga ishlatilishi shart!

---

## 9. Token Standartlari: ERC-20, ERC-721 va ERC-1155

- **ERC-20 (Fungible Tokens):** Almashtiriladigan tokenlar (USDT, UNI). Asosiy metodlari: `balanceOf`, `transfer`, `approve`, `transferFrom`, `allowance`.
- **ERC-721 (Non-Fungible Tokens - NFT):** Noyob raqamli aktivlar. Har bir token o'zining `tokenId` va `tokenURI` siga ega. Xavfsiz o'tkazma: `safeTransferFrom`.
- **ERC-1155 (Multi-Token Standard):** Bir vaqtning o'zida ham zambaraklar, ham qurollar, ham valyutani bitta kontraktda boshqarish. Batch operatsiyalari orqali 80% gacha gas tejash.

---

## 10. Yangilanuvchi Kontraktlar (Upgradeable Proxies)

Kontrakt kodi blokcheynda o'zgarmas bo'lgani sababli xatolarni tuzatish uchun **Proxy Pattern** ishlatiladi:
- **Proxy Kontrakt:** Foydalanuvchi bilan muloqot qiladi, barcha holat o'zgaruvchilarini (`Storage`) saqlaydi va barcha chaqiruvlarni `delegatecall` orqali mantiqiy kontraktga uzatadi.
- **Implementation Kontrakt:** Faqat kod mantiqini o'z ichiga oladi.
- **Modellar:** Transparent Proxy (ProxyAdmin boshqaruvida) va UUPS (Universal Upgradeable Proxy Standard - yanada yengil va arzon).
- **Muhim qoida:** Yangilanuvchi kontraktlarda konstruktor (`constructor`) ishlatilmaydi, uning o'rniga `initialize()` funksiyasi ishlatiladi!

---

## 11. DeFi Muhandisligi: Staking, AMM va Flash Loans

- **AMM (Automated Market Maker):** Uniswap v2 doimiy ko'paytma formulasiga asoslangan ($x \cdot y = k$). Likvidlik provayderlari (LP) pul kiritib LP tokenlar oladi va savdo komissiyalaridan daromad topadi.
- **Staking va Yield Farming:** Foydalanuvchilar o'z tokenlarini bloklab, sekundiga mutanosib mukofot hisoblaydi (Synthetics reward distribution algoritmi).
- **Flash Loans:** Hech qanday garovsiz millionlab dollar qarz olib, bitta tranzaksiya ichida qaytarish imkoni. Arbitraj va likvidatsiya uchun foydalaniladi.

---

## 12. Smart Kontraktlar Xavfsizligi va Eng Xavfli Zaifliklar

1. **Reentrancy (Qayta kirish hujumi):** Tashqi kontraktga pul o'tkazilganda nazorat hujumchiga o'tadi va u hisobdan yechish funksiyasini qayta-qayta chaqirib balansni bo'shatadi (The DAO xakerligi). Himoya: **Checks-Effects-Interactions** namunasi va `ReentrancyGuard` modifieri.
2. **Integer Overflow/Underflow:** Solidity 0.8+ versiyasidan boshlab avtomatik ravishda tekshiriladi va xato bo'lsa revert qilinadi.
3. **Tx.origin Phishing:** `tx.origin` orqali tekshirish hujumchi vositachi kontrakt yaratib o'g'irlik qilishiga sabab bo'ladi. Har doim `msg.sender` ishlatilishi shart.
4. **Front-running va MEV:** Mempooldagi tranzaksiyalarni ko'rib, yuqori gas to'lab oldinga o'tib ketish. Himoya: Commit-Reveal sxemalari.

---

## 13. Gas Optimizatsiyasi San'ati (Gas Golfing)

- **Storage Packing:** O'zgaruvchilarni bitta 32-bayt slotga sig'adigan qilib ketma-ket joylashtirish (`uint128 a; uint128 b;` bitta slot egallaydi).
- **Custom Errors:** `require(condition, "Uzoq xato matni")` o'rniga `if (!condition) revert MyError();` ishlatish.
- **Calldata vs Memory:** O'zgarmas tashqi massivlar uchun `calldata` tanlash.
- **O'zgarmas qiymatlar:** `constant` va `immutable` kalit so'zlari storage xotirasini band qilmaydi, to'g'ridan-to'g'ri baytkodga yoziladi.
- **Unchecked bloki:** Hech qachon overflow bo'lmaydigan for tsikli hisoblagichlarini `unchecked { ++i; }` qilish.

---

## 14. Inline Assembly va Yul Tili

Yul — bu EVM opkodlari ustiga qurilgan o'rta darajadagi dasturlash tili:
```solidity
assembly {
    let result := add(x, y)
    mstore(0x0, result)
    return(0x0, 0x20)
}
```
Yul orqali Solidity tekshiruvlarini chetlab o'tib, to'g'ridan-to'g'ri xotira bilan ishlash va maksimal darajada past gasli kontraktlar (masalan, Uniswap v4 yoki Seaport) yozish mumkin.

---

## 15. Kriptografiya, Oracllar va EIP Standartlari

- **ECDSA va ecrecover:** Off-chain imzolangan ruxsatnomalar (Gasless Permit - EIP-2612) orqali tranzaksiya to'lovini foydalanuvchi o'rniga relayer to'lashiga imkon berish.
- **Merkle Trees:** Millionlab foydalanuvchilarga token tarqatish (Airdrop) uchun xotirada faqat bitta 32 baytlik `rootHash` saqlanadi, har bir foydalanuvchi o'zining bargi va isbotini (proof) taqdim etadi ($O(\log N)$ tekshiruv).
- **Chainlink Oracllari:** Real dunyo narxlarini (BTC/USD, ETH/USD) va kriptografik tasodifiy sonlarni (Chainlink VRF) smart kontraktga yetkazib beruvchi markazlashmagan tarmoq.

---
*Ushbu qo'llanma O'zbekiston Web3 va Blokcheyn ekotizimi mutaxassislari, auditorlar va smart kontrakt muhandislari uchun fundamental ensiklopediya sifatida yaratildi.*
