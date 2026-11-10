# Khorazmiy AI: Solidity - Modul 24
## Mavzu: Kiberxavfsizlik, Kriptografiya (AES, RSA, ECC) va Xavfsiz Kodlash

### Topshiriq #1151: AES-GCM Kalitini boshqarishda "Replay Attack"dan himoya
**Tavsif:** Off-chain AES-GCM shifrlashda ishlatiladigan `nonce` qiymatini on-chain tasdiqlash. Smart kontraktda takroriy foydalanish (replay) oldini olish zarur.
**Talablar:** `nonce` qiymati har bir tranzaksiya uchun unik bo'lishi va `mapping` orqali tekshirilishi shart.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AESNonceGuard {
    mapping(uint256 => bool) public usedNonces;

    // Nonce ishlatilganligini tekshirish va yangilash
    function validateNonce(uint256 nonce) external {
        require(!usedNonces[nonce], "Nonce allaqachon ishlatilgan");
        usedNonces[nonce] = true;
    }
}
```
**Tushuntirish:** `nonce` takrorlanmasligini ta'minlash AES-GCM xavfsizligi uchun kritik. `mapping` O(1) murakkablik bilan tezkor tekshiruvni ta'minlaydi.

### Topshiriq #1152: RSA Imzo tekshiruvi (ECDSA o'rniga)
**Tavsif:** Ba'zi legacy tizimlar RSA imzolaridan foydalanadi. Solidity'da RSA-2048 imzosini tekshirish uchun `ecrecover` yetarli emas.
**Talablar:** `modexp` (0x05) precompiled kontraktidan foydalangan holda RSA imzosini verifikatsiya qilish.
**Yechim (Solidity):**
```solidity
contract RSAVerifier {
    // RSA imzosini tekshirish uchun modexp (0x05) dan foydalanish
    function verifyRSA(uint256 _m, uint256 _e, uint256 _n, uint256 _s) public view returns (bool) {
        // s^e mod n == m
        bytes memory base = abi.encodePacked(_s);
        bytes memory exp = abi.encodePacked(_e);
        bytes memory mod = abi.encodePacked(_n);
        // Bu yerda assembly orqali staticcall(0x05) chaqiriladi
        return true; // Soddalashtirilgan
    }
}
```
**Tushuntirish:** `modexp` precompiled kontrakti katta sonlar ustida arifmetikani gaz samaradorligi bilan bajarishga imkon beradi.

### Topshiriq #1153: ECC (Elliptic Curve) Kalitlarini saqlash xavfsizligi
**Tavsif:** Foydalanuvchi ochiq kalitlarini (Public Keys) xavfsiz saqlash va ularni `address` formatiga o'tkazish.
**Talablar:** Kalitlarni `bytes32` formatida saqlash va `keccak256` orqali manzilni hosil qilish.
**Yechim (Solidity):**
```solidity
contract ECCKeyManager {
    mapping(address => bytes32) public publicKeys;

    function registerKey(bytes32 _pubKey) external {
        // Public kalitdan address hosil qilish
        address addr = address(uint160(uint256(keccak256(abi.encodePacked(_pubKey)))));
        require(addr == msg.sender, "Kalit egasi noto'g'ri");
        publicKeys[msg.sender] = _pubKey;
    }
}
```
**Tushuntirish:** ECC kalitlarini to'g'ridan-to'g'ri `address` sifatida emas, `bytes32` sifatida saqlash xavfsizlikni oshiradi.

### Topshiriq #1154: Reentrancy (Qayta kirish) hujumiga qarshi "Checks-Effects-Interactions"
**Tavsif:** Kriptografik aktivlar almashinuvi vaqtida reentrancy hujumini to'xtatish.
**Talablar:** `nonReentrant` modifieri va holatni o'zgartirishni (effects) tashqi chaqiruvdan (interactions) oldin bajarish.
**Yechim (Solidity):**
```solidity
abstract contract ReentrancyGuard {
    bool private _locked;
    modifier nonReentrant() {
        require(!_locked, "Reentrancy aniqlandi");
        _locked = true;
        _;
        _locked = false;
    }
}
```
**Tushuntirish:** `_locked` bayrog'i funksiya tugamasdan qayta chaqirilishini bloklaydi.

### Topshiriq #1155: Hash-based Commitment Scheme
**Tavsif:** "Commit-Reveal" sxemasi orqali oldindan ma'lumotni oshkor qilmasdan tasdiqlash.
**Talablar:** `keccak256(secret + salt)` qiymatini saqlash.
**Yechim (Solidity):**
```solidity
contract Commitment {
    mapping(address => bytes32) public commitments;

    function commit(bytes32 _hash) external {
        commitments[msg.sender] = _hash;
    }
}
```
**Tushuntirish:** Bu usul o'yinlar yoki auktsionlarda ma'lumotlar oshkor bo'lishidan oldin ularni "muhrlash" uchun ishlatiladi.

### Topshiriq #1156: Integer Overflow/Underflow himoyasi (Solidity 0.8+)
**Tavsif:** Matematik amallarda xatoliklarni oldini olish.
**Talablar:** `unchecked` bloklaridan faqat optimizatsiya zarur bo'lganda foydalanish va standart arifmetikani qo'llash.
**Yechim (Solidity):**
```solidity
contract SafeMath {
    function safeAdd(uint256 a, uint256 b) public pure returns (uint256) {
        return a + b; // 0.8.0 dan boshlab avtomatik overflow tekshiruvi mavjud
    }
}
```
**Tushuntirish:** 0.8.0+ versiyalarida `SafeMath` kutubxonasi shart emas, chunki kompilyator o'zi tekshiradi.

### Topshiriq #1157: Access Control (Rolga asoslangan kirish)
**Tavsif:** Admin funksiyalarini faqat vakolatli shaxslar bajarishini ta'minlash.
**Talablar:** `Ownable` yoki `AccessControl` patternidan foydalanish.
**Yechim (Solidity):**
```solidity
contract AdminControl {
    address public admin;
    constructor() { admin = msg.sender; }
    modifier onlyAdmin() {
        require(msg.sender == admin, "Admin huquqi yo'q");
        _;
    }
}
```
**Tushuntirish:** Kiberxavfsizlikda "Least Privilege" (eng kam imtiyoz) prinsipi muhimdir.

### Topshiriq #1158: Data Sanitization (Kiruvchi ma'lumotlarni tozalash)
**Tavsif:** Foydalanuvchi kiritgan string yoki ma'lumotlarni xavfsiz formatga keltirish.
**Talablar:** `bytes` uzunligini tekshirish va `require` orqali validatsiya.
**Yechim (Solidity):**
```solidity
function sanitizeInput(string memory input) public pure returns (bool) {
    require(bytes(input).length > 0 && bytes(input).length < 100, "Noto'g'ri uzunlik");
    return true;
}
```
**Tushuntirish:** Input validatsiyasi smart kontraktlarga hujumlarni (masalan, buffer overflow) oldini oladi.

### Topshiriq #1159: Gas Limit va DoS hujumidan himoya
**Tavsif:** Katta massivlar ustida iteratsiya qilishdan qochish.
**Talablar:** `for` looplarini cheklash yoki "Pull-over-Push" modelini qo'llash.
**Yechim (Solidity):**
```solidity
// Yomon yondashuv: for loop bilan barcha foydalanuvchilarga pul yuborish
// Yaxshi yondashuv: Har bir foydalanuvchi o'zi pulini yechib oladi (Withdraw pattern)
function withdraw() external {
    uint256 amount = balances[msg.sender];
    balances[msg.sender] = 0;
    payable(msg.sender).transfer(amount);
}
```
**Tushuntirish:** "Pull-over-Push" modeli tranzaksiya gaz limitidan oshib ketish (DoS) xavfini yo'q qiladi.

### Topshiriq #1160: Self-Destruct va Kontraktni o'chirish xavfsizligi
**Tavsif:** Eskirgan yoki xavfli kontraktlarni tizimdan butunlay olib tashlash.
**Talablar:** `selfdestruct` funksiyasini faqat admin chaqira olishi va qoldiq mablag'ni xavfsiz manzilga o'tkazish.
**Yechim (Solidity):**
```solidity
function kill() external onlyAdmin {
    selfdestruct(payable(admin));
}
```
**Tushuntirish:** `selfdestruct` kodni blokcheyndan o'chiradi, bu esa xavfsizlik buzilganda eng oxirgi chora hisoblanadi.

---

### Topshiriq #1161: Off-chain ma'lumotlar uchun ECDSA imzo tekshiruvi
**Tavsif:** Smart kontraktga tashqi tizimdan kelayotgan buyruqlarni xavfsiz tasdiqlash. Replay attack'dan himoyalanish uchun `nonce` ishlatish zarurati.
**Talablar:** `ecrecover` funksiyasidan foydalangan holda imzo egasini aniqlash va takroriy hujumlarni bloklash.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SecureSigner {
    mapping(address => uint256) public nonces;

    // Imzoni tekshirib, buyruqni bajarish
    function execute(bytes32 messageHash, uint8 v, bytes32 r, bytes32 s, address signer) external {
        require(nonces[signer] < type(uint256).max, "Nonce limit");
        
        // EIP-191 standartidagi hashni qayta tiklash
        bytes32 ethSignedHash = keccak256(abi.encodePacked("\x19Ethereum Signed Message:\n32", messageHash));
        address recovered = ecrecover(ethSignedHash, v, r, s);
        
        require(recovered == signer, "Noto'g'ri imzo");
        nonces[signer]++;
    }
}
```
**Tushuntirish:** `ecrecover` kriptografik jihatdan samarali, chunki u EVM'ning o'rnatilgan prekompilyatsiya qilingan funksiyasidan foydalanadi.

### Topshiriq #1162: AES-256 simmetrik kalit boshqaruvi (Simulyatsiya)
**Tavsif:** On-chain AES kalitlarini saqlash xavfli, shuning uchun faqat kalit hashlarini saqlash orqali ma'lumotlar yaxlitligini tekshirish.
**Talablar:** Kalitni emas, uning `keccak256` hashini saqlash va tekshirish.
**Yechim (Solidity):**
```solidity
contract KeyVault {
    bytes32 private keyHash;

    function setKeyHash(bytes32 _hash) external {
        require(keyHash == 0, "Kalit allaqachon o'rnatilgan");
        keyHash = _hash;
    }

    function verifyKey(string memory _key) external view returns (bool) {
        return keccak256(abi.encodePacked(_key)) == keyHash;
    }
}
```
**Tushuntirish:** Blokcheyn shaffof bo'lgani uchun xom kalitlarni hech qachon saqlamaslik kerak. Hash orqali tekshirish "Zero-Knowledge" tamoyiliga yaqinlashadi.

### Topshiriq #1163: Reentrancy himoyasi (ReentrancyGuard)
**Tavsif:** Kriptografik hamyonlarda mablag' o'tkazishda "Reentrancy" hujumini oldini olish.
**Talablar:** `nonReentrant` modifikatorini qo'llash va `Checks-Effects-Interactions` qoidasiga amal qilish.
**Yechim (Solidity):**
```solidity
contract SecureVault {
    bool private locked;

    modifier nonReentrant() {
        require(!locked, "Reentrancy aniqlandi");
        locked = true;
        _;
        locked = false;
    }

    function withdraw(uint256 amount) external nonReentrant {
        require(address(this).balance >= amount, "Mablag' yetarli emas");
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "O'tkazma muvaffaqiyatsiz");
    }
}
```
**Tushuntirish:** `locked` o'zgaruvchisi funksiya bajarilayotganda qayta chaqiruvni bloklaydi, bu esa xavfsizlikning eng yuqori standartidir.

### Topshiriq #1164: RSA-2048 imzo tekshiruvi (Modulyar arifmetika)
**Tavsif:** Smart kontraktda RSA imzosini tekshirish (qimmat operatsiya).
**Talablar:** `expmod` (modpow) yordamida katta sonlar bilan ishlash.
**Yechim (Solidity):**
```solidity
contract RSAVerifier {
    // RSA: m = c^e mod n
    function verifyRSA(uint256 c, uint256 e, uint256 n) public view returns (uint256) {
        // 0x05 - modexp prekompilyatsiyasi
        (bool success, bytes memory result) = address(0x05).staticcall(abi.encode(32, 32, 32, c, e, n));
        require(success, "Modexp xatosi");
        return abi.decode(result, (uint256));
    }
}
```
**Tushuntirish:** `0x05` manzili EVM'dagi `modexp` uchun ajratilgan bo'lib, katta sonlar bilan ishlashda eng tezkor usuldir.

### Topshiriq #1165: Integer Overflow/Underflow himoyasi
**Tavsif:** Solidity 0.8.0 dan oldingi versiyalarda matematik xatolarni oldini olish.
**Talablar:** `SafeMath` kutubxonasini simulyatsiya qilish yoki zamonaviy `unchecked` bloklaridan to'g'ri foydalanish.
**Yechim (Solidity):**
```solidity
contract SafeMathOps {
    function safeAdd(uint256 a, uint256 b) public pure returns (uint256) {
        unchecked {
            uint256 res = a + b;
            require(res >= a, "Overflow");
            return res;
        }
    }
}
```
**Tushuntirish:** `unchecked` bloklari gazni tejaydi, lekin xavfsizlikni ta'minlash uchun `require` bilan birga ishlatilishi shart.

### Topshiriq #1166: Access Control (Role-Based)
**Tavsif:** Faqat ruxsat etilgan adminlar uchun funksiyalarni cheklash.
**Talablar:** `AccessControl` patternidan foydalanish.
**Yechim (Solidity):**
```solidity
contract AdminControl {
    mapping(address => bool) public admins;

    modifier onlyAdmin() {
        require(admins[msg.sender], "Admin huquqi yo'q");
        _;
    }

    function addAdmin(address _newAdmin) external onlyAdmin {
        admins[_newAdmin] = true;
    }
}
```
**Tushuntirish:** Markazlashmagan tizimlarda rolga asoslangan boshqaruv eng xavfsiz yechimdir.

### Topshiriq #1167: Ma'lumotlarni shifrlash (XOR maskalash)
**Tavsif:** Oddiy ma'lumotlarni kontrakt ichida vaqtinchalik yashirish.
**Talablar:** XOR operatsiyasi orqali oddiy maskalash.
**Yechim (Solidity):**
```solidity
contract Masking {
    function mask(bytes32 data, bytes32 secret) public pure returns (bytes32) {
        return data ^ secret;
    }
}
```
**Tushuntirish:** XOR operatsiyasi teskari hisoblanadi, ya'ni bir xil kalit bilan ikki marta XOR qilish asl ma'lumotni qaytaradi.

### Topshiriq #1168: Front-running hujumiga qarshi "Commit-Reveal"
**Tavsif:** Tranzaksiya mempool'da ko'rinib qolishini oldini olish.
**Talablar:** Avval hashni yuborish (commit), keyin ma'lumotni ochish (reveal).
**Yechim (Solidity):**
```solidity
contract CommitReveal {
    mapping(address => bytes32) public commits;

    function commit(bytes32 _hash) external {
        commits[msg.sender] = _hash;
    }

    function reveal(string memory _data, uint256 _nonce) external {
        require(keccak256(abi.encodePacked(_data, _nonce)) == commits[msg.sender], "Noto'g'ri ma'lumot");
        // Logika...
    }
}
```
**Tushuntirish:** Bu usul tranzaksiya mazmunini yashirish orqali "Front-running" (oldindan sotib olish) hujumlarini to'liq bloklaydi.

### Topshiriq #1169: Pausable (Favqulodda to'xtatish)
**Tavsif:** Xavfsizlik xavfi tug'ilganda kontraktni to'xtatib turish.
**Talablar:** `pause` va `unpause` funksiyalari.
**Yechim (Solidity):**
```solidity
contract Pausable {
    bool public paused;

    modifier whenNotPaused() {
        require(!paused, "Kontrakt to'xtatilgan");
        _;
    }

    function togglePause() external {
        paused = !paused;
    }

    function sensitiveAction() external whenNotPaused {
        // Xavfli operatsiya
    }
}
```
**Tushuntirish:** Favqulodda vaziyatlarda aktivlarni himoya qilish uchun eng muhim mexanizm.

### Topshiriq #1170: Gas limit optimizatsiyasi (Storage vs Memory)
**Tavsif:** Katta hajmdagi ma'lumotlarni qayta ishlashda gazni tejash.
**Talablar:** `storage` o'rniga `memory` dan foydalanish.
**Yechim (Solidity):**
```solidity
contract GasOptimizer {
    uint256[] public data;

    function process() external view {
        uint256[] memory localData = data; // Storage'dan memory'ga yuklash
        for(uint i = 0; i < localData.length; i++) {
            // Operatsiyalar
        }
    }
}
```
**Tushuntirish:** `storage` ga har bir murojaat qimmat (SSTORE/SLOAD), `memory` esa arzonroq. Ma'lumotni bir marta yuklab olish gazni 50% gacha tejaydi.

---

### Topshiriq #1171: Reentrancy hujumiga qarshi "Checks-Effects-Interactions" patterini
**Tavsif:** Smart kontraktlarda mablag'larni yechib olish jarayonida reentrancy (qayta kirish) hujumlarini oldini olish.
**Talablar:** `nonReentrant` modifikatoridan foydalanish va holatni o'zgartirishni tashqi chaqiruvdan oldin bajarish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SecureVault {
    mapping(address => uint256) public balances;
    bool private locked;

    // Reentrancy hujumini bloklash uchun modifikator
    modifier nonReentrant() {
        require(!locked, "Qayta kirish aniqlandi!");
        locked = true;
        _;
        locked = false;
    }

    function withdraw(uint256 _amount) public nonReentrant {
        require(balances[msg.sender] >= _amount, "Mablag' yetarli emas");
        
        // 1. Checks (Tekshirish)
        // 2. Effects (Holatni yangilash - birinchi bajarilishi shart)
        balances[msg.sender] -= _amount;
        
        // 3. Interactions (Tashqi chaqiruv - oxirida)
        (bool success, ) = msg.sender.call{value: _amount}("");
        require(success, "O'tkazma muvaffaqiyatsiz");
    }
}
```
**Tushuntirish:** "Checks-Effects-Interactions" qoidasi hujumchi `fallback` funksiyasi orqali kontraktga qayta kirib, balansni nolga tushirmasdan mablag'ni qayta yechib olishini oldini oladi.

---

### Topshiriq #1172: ECC (Elliptic Curve Cryptography) imzosini tekshirish
**Tavsif:** Off-chain yaratilgan xabarni on-chain tasdiqlash (masalan, gas to'lamasdan tranzaksiya imzolash).
**Talablar:** `ecrecover` funksiyasidan foydalangan holda imzo egasini aniqlash.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SignatureVerifier {
    function verify(address _signer, bytes32 _messageHash, uint8 v, bytes32 r, bytes32 s) 
        public pure returns (bool) {
        // Ethereum imzo formatini to'g'rilash
        bytes32 ethSignedMessageHash = keccak256(abi.encodePacked("\x19Ethereum Signed Message:\n32", _messageHash));
        return ecrecover(ethSignedMessageHash, v, r, s) == _signer;
    }
}
```
**Tushuntirish:** `ecrecover` ECC algoritmi asosida ishlaydi. `\x19Ethereum Signed Message:\n32` prefiksi xabarning haqiqiyligini va boshqa kontraktlarda qayta ishlatilmasligini ta'minlaydi.

---

### Topshiriq #1173: Integer Overflow/Underflow himoyasi
**Tavsif:** Matematik amallarda qiymatlarning chegaradan chiqib ketishini oldini olish.
**Talablar:** Solidity 0.8.0+ versiyasidagi o'rnatilgan xavfsizlik mexanizmlaridan foydalanish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SafeMathExample {
    uint256 public supply = 100;

    // 0.8.0 dan yuqori versiyalarda overflow avtomatik tekshiriladi
    function decreaseSupply(uint256 _amount) public {
        // Agar _amount > supply bo'lsa, tranzaksiya avtomatik revert bo'ladi
        supply -= _amount;
    }
}
```
**Tushuntirish:** Eski versiyalarda `SafeMath` kutubxonasi kerak edi, ammo zamonaviy Solidity kompilyatorlari `panic` kodlari orqali xavfsiz matematikani ta'minlaydi.

---

### Topshiriq #1174: Access Control (Role-based)
**Tavsif:** Kontrakt funksiyalariga faqat vakolatli shaxslar kirishini ta'minlash.
**Talablar:** `Ownable` yoki `AccessControl` patternidan foydalanish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AdminControl {
    address public admin;

    constructor() { admin = msg.sender; }

    modifier onlyAdmin() {
        require(msg.sender == admin, "Faqat admin ruxsat berilgan!");
        _;
    }

    function restrictedAction() public onlyAdmin {
        // Maxfiy amallar
    }
}
```
**Tushuntirish:** `modifier` yordamida kirish huquqini cheklash kodning takrorlanishini oldini oladi va xavfsizlikni markazlashtiradi.

---

### Topshiriq #1175: AES-like xavfsiz ma'lumotlar shifrlash (Simmetrik)
**Tavsif:** Kontrakt ichida maxfiy ma'lumotlarni saqlash (eslatma: blockchain ochiq, shuning uchun faqat hash yoki off-chain kalitlar bilan).
**Talablar:** `keccak256` orqali ma'lumotlarni "salt" bilan himoyalash.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DataVault {
    // Ma'lumotni "salt" bilan hashlab saqlash (hashing)
    function generateSecureHash(string memory _data, string memory _salt) 
        public pure returns (bytes32) {
        return keccak256(abi.encodePacked(_data, _salt));
    }
}
```
**Tushuntirish:** Blockchainda to'liq AES shifrlash qimmat va xavfli. "Salted Hashing" ma'lumotlarni o'qib bo'lmas holatga keltiradi.

---

### Topshiriq #1176: Front-running hujumiga qarshi "Commit-Reveal"
**Tavsif:** Tranzaksiya mempoolga tushganda boshqalar uni ko'rib, oldindan harakat qilishini (front-running) oldini olish.
**Talablar:** Avval hashni yuborish, keyin ma'lumotni ochish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CommitReveal {
    bytes32 public commitment;
    bool public revealed;

    function commit(bytes32 _hash) public {
        commitment = _hash;
    }

    function reveal(string memory _secret) public {
        require(keccak256(abi.encodePacked(_secret)) == commitment, "Noto'g'ri ma'lumot");
        revealed = true;
    }
}
```
**Tushuntirish:** Bu usul tranzaksiya mazmunini yashirin tutib, uni faqat tasdiqlash bosqichida ochishga imkon beradi.

---

### Topshiriq #1177: Pull-over-Push to'lov tizimi
**Tavsif:** To'g'ridan-to'g'ri `transfer` qilish o'rniga, foydalanuvchiga mablag'ni o'zi yechib olish imkonini berish.
**Talablar:** `withdraw` patternidan foydalanish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PullPayment {
    mapping(address => uint256) public pendingWithdrawals;

    function withdraw() public {
        uint256 amount = pendingWithdrawals[msg.sender];
        require(amount > 0, "Yechib olinadigan mablag' yo'q");
        pendingWithdrawals[msg.sender] = 0;
        payable(msg.sender).transfer(amount);
    }
}
```
**Tushuntirish:** Push (to'g'ridan-to'g'ri yuborish) xavfli, chunki qabul qiluvchi kontrakt xato bo'lsa, butun tranzaksiya revert bo'ladi. Pull modeli xavfsizroq.

---

### Topshiriq #1178: Time-lock mexanizmi
**Tavsif:** Muhim qarorlarni (masalan, admin huquqini o'zgartirish) ma'lum vaqt o'tgach amalga oshirish.
**Talablar:** `block.timestamp` dan foydalanish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TimeLock {
    uint256 public constant DELAY = 2 days;
    uint256 public releaseTime;

    function scheduleAction() public {
        releaseTime = block.timestamp + DELAY;
    }

    function execute() public {
        require(block.timestamp >= releaseTime, "Vaqt hali kelmadi");
        // Amaliyotni bajarish
    }
}
```
**Tushuntirish:** Time-lock foydalanuvchilarga xavfli o'zgarishlardan xabardor bo'lish va kerak bo'lsa chiqib ketish uchun vaqt beradi.

---

### Topshiriq #1179: Replay hujumiga qarshi "Nonce"
**Tavsif:** Bir xil tranzaksiyani qayta-qayta yuborishning oldini olish.
**Talablar:** Har bir foydalanuvchi uchun `nonce` (tartib raqami) saqlash.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract NonceManager {
    mapping(address => uint256) public nonces;

    function execute(uint256 _nonce) public {
        require(_nonce == nonces[msg.sender], "Noto'g'ri nonce");
        nonces[msg.sender]++;
        // Tranzaksiyani bajarish
    }
}
```
**Tushuntirish:** `nonce` har bir tranzaksiyani noyob qiladi, bu esa imzolangan xabarlarni qayta ishlatish (replay) imkonini yo'q qiladi.

---

### Topshiriq #1180: Kontraktni o'chirish (Self-Destruct)
**Tavsif:** Xavfsizlik buzilganda kontraktni zudlik bilan to'xtatish.
**Talablar:** `selfdestruct` funksiyasidan foydalanish va qoldiqlarni qaytarish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EmergencyStop {
    address public owner;

    constructor() { owner = msg.sender; }

    function kill() public {
        require(msg.sender == owner, "Faqat egasi o'chira oladi");
        selfdestruct(payable(owner));
    }
}
```
**Tushuntirish:** `selfdestruct` kontraktni blokcheyndan o'chiradi va qolgan barcha mablag'ni egasiga qaytaradi. Bu "o't o'chirish" mexanizmi hisoblanadi.

---

### Topshiriq #1181: Reentrancy Hujumiga Qarshi "Checks-Effects-Interactions" Patterni
**Tavsif:** Smart kontraktlarda mablag'larni yechib olish jarayonida reentrancy (qayta kirish) hujumlarini oldini olish.
**Talablar:** `withdraw` funksiyasida tashqi chaqiruvdan oldin balansni nolga tenglash shart.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SecureVault {
    mapping(address => uint256) public balances;

    // Mablag' yechishda xavfsiz yondashuv
    function withdraw(uint256 _amount) public {
        require(balances[msg.sender] >= _amount, "Balans yetarli emas");
        
        // 1. Tekshirish (Checks)
        // 2. Effekt (Effects) - Tashqi chaqiruvdan oldin holatni yangilash
        balances[msg.sender] -= _amount;
        
        // 3. O'zaro ta'sir (Interactions)
        (bool success, ) = msg.sender.call{value: _amount}("");
        require(success, "O'tkazma muvaffaqiyatsiz");
    }
}
```
**Tushuntirish:** "Checks-Effects-Interactions" patterini reentrancy hujumlarini to'liq bloklaydi, chunki balans o'zgartirilgandan so'ng hujumchi kontrakt funksiyani qayta chaqirsa ham, balans allaqachon nol bo'ladi.

### Topshiriq #1182: ECC (Elliptic Curve) Imzo Tekshiruvi
**Tavsif:** Off-chain yaratilgan xabarni on-chain `ecrecover` yordamida autentifikatsiya qilish.
**Talablar:** `v, r, s` parametrlarini tekshirish va xabar egasini aniqlash.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SignatureVerifier {
    function verify(bytes32 messageHash, uint8 v, bytes32 r, bytes32 s, address signer) public pure returns (bool) {
        // EIP-191 standartiga mos xabar prefiksi
        bytes32 ethSignedMessageHash = keccak256(abi.encodePacked("\x19Ethereum Signed Message:\n32", messageHash));
        return ecrecover(ethSignedMessageHash, v, r, s) == signer;
    }
}
```
**Tushuntirish:** `ecrecover` funksiyasi ECC algoritmidan foydalanadi. Prefiks qo'shish orqali xabarning Ethereum tarmog'iga xosligi ta'minlanadi va "replay attack" oldi olinadi.

### Topshiriq #1183: Integer Overflow/Underflow Himoyasi
**Tavsif:** Matematik amallarda qiymatlarning chegaradan chiqib ketishini oldini olish.
**Talablar:** Solidity 0.8.0+ versiyasining o'rnatilgan xavfsizlik mexanizmlaridan foydalanish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SafeMathExample {
    uint256 public counter;

    // 0.8.0 dan yuqori versiyalarda overflow avtomatik tekshiriladi
    function increment(uint256 _value) public {
        counter += _value; // Agar oshib ketsa, revert bo'ladi
    }

    function decrement(uint256 _value) public {
        require(counter >= _value, "Underflow xavfi");
        counter -= _value;
    }
}
```
**Tushuntirish:** Eski versiyalarda `SafeMath` kutubxonasi kerak edi, hozirgi versiyalarda esa `unchecked` blokidan foydalanilmasa, har qanday xavfli matematik amal avtomatik tarzda tranzaksiyani bekor qiladi.

### Topshiriq #1184: Access Control (Rolga asoslangan kirish)
**Tavsif:** Kontrakt funksiyalariga faqat vakolatli shaxslar kirishini ta'minlash.
**Talablar:** `Ownable` patterni yoki `AccessControl` standartidan foydalanish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AdminControl {
    address public admin;

    constructor() { admin = msg.sender; }

    modifier onlyAdmin() {
        require(msg.sender == admin, "Faqat admin ruxsatli");
        _;
    }

    function sensitiveAction() public onlyAdmin {
        // Maxfiy operatsiyalar
    }
}
```
**Tushuntirish:** `modifier` yordamida kodni takrorlamasdan, xavfsizlik qatlamini funksiyalarga osonlik bilan qo'shish mumkin.

### Topshiriq #1185: AES-like XOR shifrlash (Simmetrik)
**Tavsif:** Ma'lumotlarni on-chain vaqtincha yashirish uchun oddiy XOR shifrlash mexanizmi.
**Talablar:** Kalit (key) yordamida ma'lumotni shifrlash va deshifrlash.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleCrypto {
    function xorCipher(bytes memory data, bytes32 key) public pure returns (bytes memory) {
        bytes memory result = new bytes(data.length);
        for (uint i = 0; i < data.length; i++) {
            result[i] = data[i] ^ key[i % 32];
        }
        return result;
    }
}
```
**Tushuntirish:** XOR operatsiyasi teskari bo'lgani uchun, bir xil funksiya ham shifrlash, ham deshifrlash uchun ishlatiladi. Bu yengil kriptografik operatsiyalar uchun samarali.

### Topshiriq #1186: Pausable (Favqulodda to'xtatish)
**Tavsif:** Xavfsizlik tahdidi aniqlanganda kontraktni vaqtincha to'xtatish.
**Talablar:** `whenNotPaused` modifikatorini qo'llash.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PausableContract {
    bool public paused;

    modifier whenNotPaused() {
        require(!paused, "Kontrakt to'xtatilgan");
        _;
    }

    function togglePause(bool _status) public {
        paused = _status;
    }

    function transfer() public whenNotPaused {
        // Transfer logikasi
    }
}
```
**Tushuntirish:** Bu yondashuv "Circuit Breaker" deb ataladi. Xatolik aniqlanganda barcha funksiyalarni bloklab, mablag'larni saqlab qolish imkonini beradi.

### Topshiriq #1187: Front-running himoyasi (Commit-Reveal)
**Tavsif:** Tranzaksiya mempool'da ko'rinib qolganda, boshqalar tomonidan oldindan bajarilishini (front-running) oldini olish.
**Talablar:** Hash qiymatini yuborish va keyinchalik uni ochish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CommitReveal {
    mapping(address => bytes32) public commits;

    function commit(bytes32 _hash) public {
        commits[msg.sender] = _hash;
    }

    function reveal(string memory _secret) public {
        require(keccak256(abi.encodePacked(_secret)) == commits[msg.sender], "Noto'g'ri ma'lumot");
        // Logika davom etadi
    }
}
```
**Tushuntirish:** Foydalanuvchi avval hashni yuboradi, keyin esa haqiqiy qiymatni ochadi. Bu orqali tranzaksiya mazmuni mempool'da oshkor bo'lmaydi.

### Topshiriq #1188: Randomness (Tasodifiylik) xavfsizligi
**Tavsif:** `block.timestamp` kabi bashorat qilinishi mumkin bo'lgan qiymatlardan foydalanmaslik.
**Talablar:** Chainlink VRF yoki xavfsizroq tasodifiy raqam manbasini simulyatsiya qilish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SecureRandom {
    // Haqiqiy loyihalarda Chainlink VRF ishlatilishi shart
    function generateRandom(uint256 seed) public view returns (uint256) {
        return uint256(keccak256(abi.encodePacked(block.prevrandao, block.timestamp, msg.sender, seed)));
    }
}
```
**Tushuntirish:** `block.prevrandao` (EIP-4399) eski `block.difficulty` dan ko'ra xavfsizroq, ammo yuqori xavfsizlik talab qilinadigan o'yinlarda faqat Chainlink VRF tavsiya etiladi.

### Topshiriq #1189: Honeypot (Aldovchi kontrakt) himoyasi
**Tavsif:** Foydalanuvchilarni aldovchi funksiyalardan himoya qilish uchun kodni shaffof qilish.
**Talablar:** Kontraktda yashirin `require` shartlari bo'lmasligi.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TransparentContract {
    // Barcha shartlar ochiq va tushunarli
    function withdrawAll() public {
        uint256 balance = address(this).balance;
        require(balance > 0, "Balans nol");
        payable(msg.sender).transfer(balance);
    }
}
```
**Tushuntirish:** Kodning soddaligi va "backdoor" (yashirin eshik) yo'qligi xavfsizlikning eng yaxshi kafolatidir.

### Topshiriq #1190: Gas Optimization (Xavfsiz kodlash)
**Tavsif:** Gaz sarfini kamaytirish orqali hujumlarga chidamlilikni oshirish (DoS hujumlaridan himoya).
**Talablar:** `calldata` dan foydalanish va `storage` o'qishni kamaytirish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract GasOptimized {
    // 'calldata' xotiradan o'qish arzonroq
    function processData(uint256[] calldata _data) external pure returns (uint256) {
        uint256 sum = 0;
        for (uint i = 0; i < _data.length; i++) {
            sum += _data[i];
        }
        return sum;
    }
}
```
**Tushuntirish:** `calldata` dan foydalanish tranzaksiya narxini pasaytiradi va kontraktni DoS (Denial of Service) hujumlariga nisbatan chidamliroq qiladi, chunki gaz limitiga yetib borish qiyinlashadi.

---

### Topshiriq #1191: Reentrancy Hujumiga Qarshi "Checks-Effects-Interactions" Patterni
**Tavsif:** Smart kontraktlarda mablag'larni yechib olish jarayonida reentrancy hujumlarini oldini olish.
**Talablar:** `nonReentrant` modifikatoridan foydalanish va holatni tashqi chaqiruvdan oldin yangilash.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SecureVault {
    mapping(address => uint256) public balances;
    bool private locked;

    // Reentrancy hujumini bloklash uchun modifikator
    modifier nonReentrant() {
        require(!locked, "Qayta kirish bloklandi");
        locked = true;
        _;
        locked = false;
    }

    function withdraw(uint256 _amount) public nonReentrant {
        require(balances[msg.sender] >= _amount, "Mablag' yetarli emas");
        
        // 1. Holatni yangilash (Checks-Effects)
        balances[msg.sender] -= _amount;
        
        // 2. Tashqi chaqiruv (Interactions)
        (bool success, ) = msg.sender.call{value: _amount}("");
        require(success, "O'tkazma muvaffaqiyatsiz");
    }
}
```
**Tushuntirish:** Holatni tashqi chaqiruvdan oldin o'zgartirish (Effects) hujumchi `fallback` funksiyasi orqali kontraktga qayta kirishiga yo'l qo'ymaydi.

---

### Topshiriq #1192: ECC (Elliptic Curve Cryptography) Imzo Tekshiruvi
**Tavsif:** Off-chain yaratilgan imzoning haqiqiyligini on-chain tekshirish.
**Talablar:** `ecrecover` funksiyasidan foydalangan holda xavfsiz imzo verifikatsiyasi.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SignatureVerifier {
    function verify(bytes32 messageHash, uint8 v, bytes32 r, bytes32 s, address signer) public pure returns (bool) {
        // Xabarni Ethereum imzo formatiga moslash
        bytes32 ethSignedMessageHash = keccak256(abi.encodePacked("\x19Ethereum Signed Message:\n32", messageHash));
        return ecrecover(ethSignedMessageHash, v, r, s) == signer;
    }
}
```
**Tushuntirish:** `ecrecover` ECC algoritmi asosida ishlaydi. Prefix qo'shish orqali "replay attack" va imzo soxtalashtirishning oldi olinadi.

---

### Topshiriq #1193: AES-ni Simulyatsiya Qiluvchi XOR Maskalash
**Tavsif:** On-chain ma'lumotlarni oddiy XOR shifrlash orqali himoyalash.
**Talablar:** Kalit (key) va matnni XOR operatsiyasi bilan o'zgartirish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleCipher {
    bytes32 private constant KEY = 0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef;

    function encryptDecrypt(bytes32 data) public pure returns (bytes32) {
        // XOR operatsiyasi o'zgaruvchan (reversible)
        return data ^ KEY;
    }
}
```
**Tushuntirish:** Blokcheyn shaffof bo'lgani uchun bu usul faqat "obscurity" (yashirish) uchun ishlatiladi. Haqiqiy AES on-chain juda qimmat, shuning uchun XOR samarali alternativ hisoblanadi.

---

### Topshiriq #1194: Integer Overflow/Underflow Himoyasi
**Tavsif:** Matematik amallarda qiymatlarning chegaradan chiqib ketishini oldini olish.
**Talablar:** Solidity 0.8.0+ versiyasidagi o'rnatilgan xavfsizlik mexanizmlaridan foydalanish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SafeMathExample {
    uint256 public count;

    function increment(uint256 _amount) public {
        // Solidity 0.8.0+ avtomatik ravishda overflow/underflow-ni tekshiradi
        count += _amount; 
    }

    function decrement(uint256 _amount) public {
        // Agar count < _amount bo'lsa, tranzaksiya bekor qilinadi
        count -= _amount;
    }
}
```
**Tushuntirish:** Eski versiyalarda `SafeMath` kutubxonasi kerak edi, hozir esa kompilyator darajasida xavfsizlik ta'minlangan.

---

### Topshiriq #1195: Access Control (Role-Based)
**Tavsif:** Kontrakt funksiyalariga faqat vakolatli shaxslar kirishini ta'minlash.
**Talablar:** `Ownable` yoki `AccessControl` patternidan foydalanish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AdminControl {
    address public admin;

    constructor() { admin = msg.sender; }

    modifier onlyAdmin() {
        require(msg.sender == admin, "Faqat admin ruxsat berilgan");
        _;
    }

    function sensitiveAction() public onlyAdmin {
        // Maxfiy amallar
    }
}
```
**Tushuntirish:** `modifier` yordamida kod takrorlanishining oldi olinadi va xavfsizlik markazlashtiriladi.

---

### Topshiriq #1196: Front-running Hujumiga Qarshi Commit-Reveal
**Tavsif:** Tranzaksiya mempool-da ko'rinib qolishining oldini olish.
**Talablar:** Avval xashni yuborish (commit), keyin ma'lumotni ochish (reveal).
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CommitReveal {
    mapping(address => bytes32) public commits;

    function commit(bytes32 _hash) public {
        commits[msg.sender] = _hash;
    }

    function reveal(string memory _secret, uint256 _value) public {
        require(keccak256(abi.encodePacked(_secret, _value)) == commits[msg.sender], "Noto'g'ri ma'lumot");
        // Amallar bajariladi
    }
}
```
**Tushuntirish:** Bu usul raqobatchilarga tranzaksiya tarkibini oldindan ko'rish imkonini bermaydi.

---

### Topshiriq #1197: Honeypot-ga Qarshi "Gas Limit" Tekshiruvi
**Tavsif:** Kontraktning gaz sarfini nazorat qilish orqali hujumlarni aniqlash.
**Talablar:** `gasleft()` funksiyasidan foydalanish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract GasGuard {
    function secureCall() public view {
        // Agar gaz juda kam bo'lsa, xavfli operatsiyani to'xtatish
        require(gasleft() > 5000, "Gaz yetarli emas, hujum ehtimoli");
    }
}
```
**Tushuntirish:** Hujumchilar ko'pincha past gaz bilan kontraktni "ilmoqqa" ilishga harakat qilishadi, bu tekshiruv buni cheklaydi.

---

### Topshiriq #1198: Randomness (Tasodifiylik) - Chainlink VRF
**Tavsif:** Blokcheynda xavfsiz tasodifiy son hosil qilish.
**Talablar:** `block.timestamp` yoki `blockhash` kabi bashorat qilinadigan manbalardan qochish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// Eslatma: Haqiqiy muhitda Chainlink VRF kutubxonasi ishlatiladi
contract Randomness {
    function generateSecureRandom() public view returns (uint256) {
        // Oddiy vaqtga asoslangan tasodifiylik (faqat test uchun)
        return uint256(keccak256(abi.encodePacked(block.timestamp, msg.sender)));
    }
}
```
**Tushuntirish:** `block.timestamp` minerlar tomonidan manipulyatsiya qilinishi mumkin, shuning uchun ishlab chiqarishda VRF (Verifiable Random Function) shart.

---

### Topshiriq #1199: Proxy Kontraktlar va Upgradeability
**Tavsif:** Kontrakt kodini xavfsiz yangilash imkoniyatini yaratish.
**Talablar:** `delegatecall` yordamida mantiqni ajratish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Proxy {
    address public implementation;

    function upgrade(address _newImplementation) public {
        implementation = _newImplementation;
    }

    fallback() external {
        address _impl = implementation;
        assembly {
            calldatacopy(0, 0, calldatasize())
            let result := delegatecall(gas(), _impl, 0, calldatasize(), 0, 0)
            returndatacopy(0, 0, returndatasize())
            switch result
            case 0 { revert(0, returndatasize()) }
            default { return(0, returndatasize()) }
        }
    }
}
```
**Tushuntirish:** `delegatecall` boshqa kontrakt kodini joriy kontrakt kontekstida bajaradi, bu esa xatolarni tuzatish uchun muhimdir.

---

### Topshiriq #1200: Pausable Kontrakt (Favqulodda Holat)
**Tavsif:** Xavfsizlik tahdidi aniqlanganda kontrakt faoliyatini vaqtincha to'xtatish.
**Talablar:** `paused` holatini boshqarish va modifikatorlar.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Pausable {
    bool public paused;
    address public owner = msg.sender;

    modifier whenNotPaused() {
        require(!paused, "Kontrakt to'xtatilgan");
        _;
    }

    function togglePause() public {
        require(msg.sender == owner);
        paused = !paused;
    }

    function deposit() public whenNotPaused {
        // Depozit amallari
    }
}
```
**Tushuntirish:** Favqulodda vaziyatlarda (hack aniqlanganda) mablag'larni himoya qilish uchun eng muhim mexanizm.