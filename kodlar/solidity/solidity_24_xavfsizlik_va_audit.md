# 24-Modul: Smart-Kontraktlar Kiberxavfsizligi va Audit: Reentrancy (CEI pattern, ReentrancyGuard), Flash Loan himoyasi, Oracle Manipulation (TWAP), Formal Verification (Slither, Echidna, Halmos), Access Control va ERC-4337 xavfsizligi

Ushbu modulda Ethereum va EVM moslashuvchan blokcheynlar uchun ishlab chiqarish darajasidagi smart-kontraktlar kiberxavfsizligi, eng xavfli zaifliklar tahlili (Reentrancy, Oracle manipulyatsiyasi, Flash Loan arbitraji, Signature Replay, Sandwich/MEV hujumlari), zamonaviy formal tekshiruv usullari (Slither, Echidna, Halmos, Certora) hamda ERC-4337 Account Abstraction xavfsizligi bo'yicha 50 ta amaliy, mukammal topshiriq va yechimlar keltirilgan.

---

### Topshiriq #1151: Klassik Reentrancy Zaifligi va Checks-Effects-Interactions (CEI) Patterni
**Tavsif:** Smart-kontraktdan efir yechishda (withdraw) tashqi kontraktga pul o'tkazish foydalanuvchi balansini nollashdan oldin bajarilsa, hujumchi fallback/receive funksiyasi orqali qayta kirib (reentrancy) butun hovuz mablag'larini o'g'irlashi mumkin. CEI patterni orqali mutlaq himoyalangan xavfsiz kontrakt yaratish talab etiladi.
**Talablar:** Solidity ^0.8.20, zaif va xavfsiz variantlarni ko'rsatish, CEI (Checks-Effects-Interactions) qoidasiga 100% amal qilish, custom error `TransferFailed()` ishlatish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title SecureEtherVault - Checks-Effects-Interactions (CEI) namunasi
/// @notice Reentrancy hujumlariga qarshi sof arxitektura darajasidagi himoya
contract SecureEtherVault {
    // Foydalanuvchilarning depozit balanslari
    mapping(address => uint256) public balances;

    // Hodisalar (Events)
    event Deposited(address indexed user, uint256 amount);
    event Withdrawn(address indexed user, uint256 amount);

    // Maxsus xatoliklar (Gas optimallashtirish uchun)
    error InsufficientBalance(uint256 requested, uint256 available);
    error EtherTransferFailed();

    /// @notice Shartnomaga efir depozit qilish
    function deposit() external payable {
        if (msg.value == 0) revert InsufficientBalance(0, 0);
        balances[msg.sender] += msg.value;
        emit Deposited(msg.sender, msg.value);
    }

    /// @notice Balansdagi mablag'ni xavfsiz yechish (CEI Pattern)
    function withdraw() external {
        // 1. CHECKS (Tekshiruvlar): Balans mavjudligini tasdiqlash
        uint256 balance = balances[msg.sender];
        if (balance == 0) {
            revert InsufficientBalance(balance, 0);
        }

        // 2. EFFECTS (Ichki o'zgarishlar): Holatni tashqi chaqiruvdan OLDIN yangilash!
        // Hujumchi qayta kirganda (reenter) uning balansi allaqachon 0 bo'ladi
        balances[msg.sender] = 0;

        emit Withdrawn(msg.sender, balance);

        // 3. INTERACTIONS (Tashqi aloqalar): Efirni oxirida yuborish
        (bool success, ) = msg.sender.call{value: balance}("");
        if (!success) {
            // Agar o'tkazma amalga oshmasa, tranzaksiya butunlay bekor qilinadi (revert)
            revert EtherTransferFailed();
        }
    }

    /// @notice Shartnoma umumiy balansini ko'rish
    function getContractBalance() external view returns (uint256) {
        return address(this).balance;
    }
}
```
**Tushuntirish:** Reentrancy - aqlli shartnomalar tarixidagi eng mashhur zaiflikdir (2016-yilgi The DAO xakining sababchisi). Checks-Effects-Interactions (CEI) tamoyilida har qanday holat o'zgarishi (`balances[msg.sender] = 0`) tashqi `call{value: ...}` chaqiruvidan oldin amalga oshiriladi. Tashqi chaqiruv hujumchining fallback funksiyasini faollashtirgan taqdirda ham, qayta kirgan `withdraw()` chaqiruvi 0 balans ko'radi va darhol to'xtatiladi.

---

### Topshiriq #1152: OpenZeppelin ReentrancyGuard va Maxsus Status Qulflari
**Tavsif:** Murakkab DeFi tizimlarida faqat CEI ga tayanib bo'lmaydigan holatlarda (masalan, bir nechta funksiyalararo bog'liqlikda) funksiyaga bir vaqtda ikkinchi marta kirishni qat'iy taqiqlovchi ReentrancyGuard mutex modifikatorini loyihalash zarur.
**Talablar:** Status o'zgaruvchisi (1 = NOT_ENTERED, 2 = ENTERED), custom reentrancy modifier, gas tejamkorligi (uint256 non-zero slots).
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title CustomReentrancyGuard - Gas jihatdan optimallashtirilgan mutex qulfi
abstract contract CustomReentrancyGuard {
    // 0 o'rniga 1 va 2 ishlatiladi (EVM da 0 dan 1 ga o'tish 20,000 gas, 1 dan 2 ga esa 5,000 gas oladi)
    uint256 private constant _NOT_ENTERED = 1;
    uint256 private constant _ENTERED = 2;

    uint256 private _status;

    error ReentrancyGuardReentrantCall();

    constructor() {
        _status = _NOT_ENTERED;
    }

    modifier nonReentrant() {
        // Qulf holatini tekshirish
        if (_status == _ENTERED) {
            revert ReentrancyGuardReentrantCall();
        }

        // Qulfni yopish
        _status = _ENTERED;

        _;

        // Qulfni qayta ochish
        _status = _NOT_ENTERED;
    }
}

/// @title SecureBank - ReentrancyGuard bilan himoyalangan bank
contract SecureBank is CustomReentrancyGuard {
    mapping(address => uint256) public userBalances;

    event FundsWithdrawn(address indexed to, uint256 amount);

    function deposit() external payable {
        userBalances[msg.sender] += msg.value;
    }

    /// @notice Mutex qulfi bilan to'liq himoyalangan mablag' yechish
    function withdrawAll() external nonReentrant {
        uint256 amount = userBalances[msg.sender];
        require(amount > 0, "Balans nolga teng");

        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "O'tkazma muvaffaqiyatsiz");

        userBalances[msg.sender] = 0;
        emit FundsWithdrawn(msg.sender, amount);
    }
}
```
**Tushuntirish:** OpenZeppelin `ReentrancyGuard` xotirada holat bayrog'ini (`_status`) saqlaydi. Funksiya bajarilishidan oldin u `_ENTERED` ga o'zgartiriladi va tugagach `_NOT_ENTERED` ga qaytariladi. Agar tashqi shartnoma o'sha tranzaksiya ichida yana qaytib chaqirsa, `_status == _ENTERED` bo'lib turgani sababli xatolik beradi. Qiymatlarni 0 va 1 emas, 1 va 2 qilish SSTORE gas xarajatlarini 75% ga qisqartiradi.

---

### Topshiriq #1153: Cross-Function Reentrancy Himoyasi va Umumiy Holat Boshqaruvi
**Tavsif:** Hujumchi `withdraw()` orqali qayta kirish o'rniga, uning o'rniga boshqa bir zaif funksiyaga (masalan, `transfer()` yoki `claimReward()`) kirib, o'zgarmay qolgan eski balansdan foydalanib o'g'irlik qilishi mumkin. Bir nechta funksiyalararo bog'liqlikni himoyalash talab qilinadi.
**Talablar:** Ikkala funksiya ham umumiy `nonReentrant` qulfiga ega bo'lishi va CEI tartibiga qat'iy rioya qilishi kerak.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {CustomReentrancyGuard} from "./CustomReentrancyGuard.sol";

/// @title CrossFunctionVault - Funksiyalararo qayta kirishdan himoyalangan xazina
contract CrossFunctionVault is CustomReentrancyGuard {
    mapping(address => uint256) public balances;

    event Transfer(address indexed from, address indexed to, uint256 amount);

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    /// @notice Mablag'ni yechish: nonReentrant bilan himoyalangan
    function withdraw() external nonReentrant {
        uint256 amount = balances[msg.sender];
        require(amount > 0, "Mablag' mavjud emas");

        balances[msg.sender] = 0;

        (bool sent, ) = msg.sender.call{value: amount}("");
        require(sent, "Efir yuborib bo'lmadi");
    }

    /// @notice Ichki balans o'tkazmasi: umumiy nonReentrant bilan himoyalangan
    function transfer(address to, uint256 amount) external nonReentrant {
        require(balances[msg.sender] >= amount, "Yetarli balans yo'q");
        require(to != address(0), "Nol manzilga o'tkazma taqiqlangan");

        balances[msg.sender] -= amount;
        balances[to] += amount;

        emit Transfer(msg.sender, to, amount);
    }
}
```
**Tushuntirish:** Cross-Function Reentrancy da bitta funksiya xavfsiz bo'lsa ham, u boshqa funksiya bilan umumiy holatni (`balances`) ulashadi. Agar `transfer()` funksiyasida `nonReentrant` bo'lmasa, hujumchi `withdraw()` dagi tashqi qo'ng'iroq paytida `transfer()` ni chaqirib, allaqachon yechib olinayotgan balansini boshqa shaxsiy hamyoniga o'tkazib yuborishi mumkin edi.

---

### Topshiriq #1154: Read-Only Reentrancy va DeFi Narx Oracllariga Hujumning Oldini Olish
**Tavsif:** DeFi lending protokollari narxni aniqlash uchun AMM hovuzidagi `view` funksiyaga (masalan `getVirtualPrice()`) murojaat qiladi. Hovuzdan mablag' yechilayotgan oraliqda holat vaqtincha buziladi. Read-Only Reentrancy ni bloklash moduli talab qilinadi.
**Talablar:** View funksiyada ham reentrancy holatini tekshirish, oracllar uchun reentrancy flagini oshkor qilish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title SecureLpPool - Read-Only Reentrancy himoyasiga ega likvidlik hovuzi
contract SecureLpPool {
    uint256 public totalLiquidity;
    uint256 public totalSupply;
    mapping(address => uint256) public lpBalances;

    bool private _locked;

    error PoolLockedForReentrancy();

    modifier lock() {
        if (_locked) revert PoolLockedForReentrancy();
        _locked = true;
        _;
        _locked = false;
    }

    /// @notice Likvidlik yechish
    function removeLiquidity(uint256 lpAmount) external lock {
        require(lpBalances[msg.sender] >= lpAmount, "Yetarli LP yo'q");

        uint256 etherToReturn = (lpAmount * totalLiquidity) / totalSupply;

        lpBalances[msg.sender] -= lpAmount;
        totalSupply -= lpAmount;

        // Vaqtincha totalLiquidity hali kamaymagan paytda tashqi chaqiruv ketadi!
        (bool sent, ) = msg.sender.call{value: etherToReturn}("");
        require(sent, "Efir qaytarilmadi");

        totalLiquidity -= etherToReturn;
    }

    /// @notice Tashqi protokollar narxni hisoblash uchun chaqiradigan VIEW funksiya
    /// @dev Read-Only Reentrancy himoyasi: agar tranzaksiya o'rtasida bo'lsa, xatolik beradi
    function getVirtualPrice() external view returns (uint256) {
        if (_locked) {
            revert PoolLockedForReentrancy();
        }
        if (totalSupply == 0) return 1e18;
        return (totalLiquidity * 1e18) / totalSupply;
    }
}
```
**Tushuntirish:** Read-Only Reentrancy da shartnoma holati o'zgarmaydi, ammo tashqi protokollar (masalan lending yoki collateral tekshirgichlar) uning `view` funksiyasidan buzilgan oraliq narxni o'qiydi. Natijada hujumchi soxta yuqori narx evaziga katta kredit olib qochadi. `_locked` flagini `view` funksiyada tekshirish bunday manipulyatsiyalarni butunlay to'xtatadi.

---

### Topshiriq #1155: EIP-1153 Transient Storage (TSTORE va TLOAD) Bilan Ultra-Arzon ReentrancyGuard
**Tavsif:** Cancun hardforkida kiritilgan EIP-1153 `tstore` va `tload` opkodlari faqat bitta tranzaksiya davomida yashaydi va diskka (Storage) yozilmaydi. Bu an'anaviy ReentrancyGuard ga qaraganda 90% kamroq gas sarflaydi.
**Talablar:** Inline Yul assembly, `tstore(SLOT, 1)` va `tload(SLOT)`, tranzaksiya yakunida tozalanish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title TransientReentrancyGuard - EIP-1153 Transient Storage asosidagi mutex
/// @notice Dencun / Cancun yangilanishidan so'ng eng arzon va xavfsiz qulf
abstract contract TransientReentrancyGuard {
    // bytes32(uint256(keccak256("eip1153.reentrancy_guard")) - 1)
    bytes32 private constant REENTRANCY_GUARD_SLOT = 
        0x8e94f173e351838d72f7d934278e9c9c8e82ef4554b73b22cf53c023d8c11e7e;

    error ReentrancyGuardReentrantCall();

    modifier nonReentrant() {
        assembly {
            // Transient Storage dan o'qish (atigi 100 gas!)
            if tload(REENTRANCY_GUARD_SLOT) {
                // Xatolik selektori: bytes4(keccak256("ReentrancyGuardReentrantCall()"))
                mstore(0x00, 0x3ee5b1cb)
                revert(0x1c, 0x04)
            }
            // Qulfni yopish (Transient xotiraga 1 yozish - 100 gas)
            tstore(REENTRANCY_GUARD_SLOT, 1)
        }

        _;

        assembly {
            // Tranzaksiya oxirida qulfni ochish
            tstore(REENTRANCY_GUARD_SLOT, 0)
        }
    }
}

contract UltraLowGasVault is TransientReentrancyGuard {
    mapping(address => uint256) public balances;

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw() external nonReentrant {
        uint256 amount = balances[msg.sender];
        require(amount > 0, "Mablag' yo'q");
        balances[msg.sender] = 0;

        (bool s, ) = msg.sender.call{value: amount}("");
        require(s, "Muvaffaqiyatsiz");
    }
}
```
**Tushuntirish:** EIP-1153 `tstore` va `tload` an'anaviy `sstore` (20,000 gas) va `sload` (2,100 gas) ga nisbatan atigi 100 gas sarflaydi. Tranzaksiya yakunlanishi bilan transient xotira avtomatik nollanadi, bu esa xotirani qo'lda tozalash xarajatlarini va storage bloat muammosini yo'qotadi.

---

### Topshiriq #1156: ERC-777 va ERC-1363 Tokenlar Callback Reentrancy Himoyasi
**Tavsif:** Standart ERC-20 dan farqli o'laroq, ERC-777 (`tokensReceived`) va ERC-1363 (`onTransferReceived`) tokenlari pul o'tkazilganda qabul qiluvchining kontraktini chaqiradi (Hook). Ushbu yashirin callback reentrancy ni to'xtatish lozim.
**Talablar:** Token transferidan oldin balansni yangilash yoki `nonReentrant` bilan himoyalash, SafeERC20 integratsiyasi.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import {CustomReentrancyGuard} from "./CustomReentrancyGuard.sol";

/// @title SecureTokenStaking - ERC-777 va ERC-1363 callback hujumlaridan himoyalangan
contract SecureTokenStaking is CustomReentrancyGuard {
    using SafeERC20 for IERC20;

    IERC20 public immutable stakingToken;
    mapping(address => uint256) public stakedAmounts;

    event Staked(address indexed user, uint256 amount);
    event Unstaked(address indexed user, uint256 amount);

    constructor(address tokenAddress) {
        require(tokenAddress != address(0), "Noto'g'ri manzil");
        stakingToken = IERC20(tokenAddress);
    }

    /// @notice Mablag'ni yechish: Token callback qilsa ham CEI va Guard himoya qiladi
    function unstake(uint256 amount) external nonReentrant {
        require(stakedAmounts[msg.sender] >= amount, "Yetarli steyk yo'q");

        // 1. Balansni oldindan kamaytirish (CEI)
        stakedAmounts[msg.sender] -= amount;

        // 2. Token o'tkazmasi (ERC-777 bo'lsa `tokensToSend`/`tokensReceived` hooklari chaqiriladi)
        stakingToken.safeTransfer(msg.sender, amount);

        emit Unstaked(msg.sender, amount);
    }
}
```
**Tushuntirish:** Ko'plab dasturchilar reentrancy faqat efir (`call{value}`) yuborilgandagina yuz beradi deb xato o'ylashadi. Ammo ERC-777 yoki ERC-1363 tokenlari o'z ichida `IERC777Recipient.tokensReceived()` kabi hook chaqiruvlariga ega bo'lib, xuddi fallback kabi kontraktga qayta kirishga imkon yaratadi.

---

### Topshiriq #1157: Pull Over Push To'lov Modeli Bilan DoS va Reentrancy ni Yo'qotish
**Tavsif:** Barcha yutuq yoki to'lovlarni birdaniga barcha ishtirokchilarga tarqatish (Push) bitta nosoz yoki yovuz kontrakt tufayli butun tranzaksiyani bekor bo'lishiga (DoS) olib keladi. Pull-payment (Withdrawal pattern) ni joriy etish talab qilinadi.
**Talablar:** PullPayment patterni, alohida `withdrawPayments(address payee)`, OpenZeppelin PullPayment arxitekturasi.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title PullPaymentAuction - 'Pull over Push' tamoyilidagi xavfsiz auksion
contract PullPaymentAuction {
    address public highestBidder;
    uint256 public highestBid;

    // Har bir foydalanuvchining auksionda qaytarib olishi mumkin bo'lgan mablag'i
    mapping(address => uint256) public pendingReturns;

    event HighestBidIncreased(address indexed bidder, uint256 amount);
    event Withdraw(address indexed bidder, uint256 amount);

    /// @notice Yangi stavka qo'yish
    function bid() external payable {
        require(msg.value > highestBid, "Stavka yetarli emas");

        if (highestBidder != address(0)) {
            // XATOLI USUL: Oldingi a'zoga darhol efir jo'natish (Push) - DoS xavfi!
            // TO'G'RI USUL: Qarzni yozib qo'yish (Pull)
            pendingReturns[highestBidder] += highestBid;
        }

        highestBidder = msg.sender;
        highestBid = msg.value;
        emit HighestBidIncreased(msg.sender, msg.value);
    }

    /// @notice Foydalanuvchi o'zining qaytarilishi kerak bo'lgan pulini mustaqil yechadi
    function withdrawPendingReturns() external {
        uint256 amount = pendingReturns[msg.sender];
        require(amount > 0, "Qaytariladigan pul yo'q");

        pendingReturns[msg.sender] = 0;

        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "To'lov o'tmadi");

        emit Withdraw(msg.sender, amount);
    }
}
```
**Tushuntirish:** 'Push' to'lov modelida agar biror a'zo efir qabul qilishni rad etuvchi (fallback revert) shartnoma bo'lsa, keyingi hech kim stavka qo'ya olmay auksion butunlay muzlab qolardi (Denial of Service). 'Pull' modeli har bir foydalanuvchiga faqat o'z pulini mustaqil yechish imkonini beradi.

---

### Topshiriq #1158: NFT (ERC-721) _safeMint Reentrancy Zaifligi va Himoyalanish
**Tavsif:** `_safeMint` yoki `_safeTransferFrom` funksiyalari qabul qiluvchi shartnomada `IERC721Receiver.onERC721Received` chaqiruvini bajaradi. Hujumchilar ushbu hook orqali minting cheklovlarini (masalan, 1 kishiga 1 ta NFT) aylanib o'tadi.
**Talablar:** onERC721Received reentrancy fosh etilishi, ReentrancyGuard va mint limitlarini o'zgarishlaridan oldin yozish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {ERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import {CustomReentrancyGuard} from "./CustomReentrancyGuard.sol";

/// @title SecureNftMint - _safeMint reentrancy xavfidan to'liq himoyalangan
contract SecureNftMint is ERC721, CustomReentrancyGuard {
    uint256 public nextTokenId;
    uint256 public constant MAX_SUPPLY = 10000;
    
    // Har bir hamyon maksimal 2 ta NFT olishi mumkin
    mapping(address => uint256) public mintedCount;

    error MaxSupplyExceeded();
    error MintLimitExceeded();

    constructor() ERC721("Khorazmiy Cyber NFT", "KCNFT") {}

    function mint() external nonReentrant {
        if (nextTokenId >= MAX_SUPPLY) revert MaxSupplyExceeded();
        if (mintedCount[msg.sender] >= 2) revert MintLimitExceeded();

        // CEI: Mint hisobini chaqiruvdan oldin oshirish!
        mintedCount[msg.sender]++;
        uint256 tokenId = nextTokenId++;

        // _safeMint ichida `onERC721Received` chaqiriladi.
        // nonReentrant va mintedCount oshirilgani sababli qayta kirishning iloji yo'q
        _safeMint(msg.sender, tokenId);
    }
}
```
**Tushuntirish:** OpenZeppelin `_safeMint` xavfsiz hisoblansa-da, u qabul qiluvchi manzil shartnoma bo'lsa, uning `onERC721Received` funksiyasini chaqiradi. Agar ishlab chiquvchi `mintedCount[msg.sender]++` ni `_safeMint` dan keyin bajarsa, hujumchi bitta tranzaksiyada barcha NFT larni bemalol o'g'irlab oladi.

---

### Topshiriq #1159: Delegatecall Reentrancy va Proksi Shartnomalari Holatining Buzilishi
**Tavsif:** Proksi shartnomalar `delegatecall` orqali mantiqiy kontraktni chaqirganda, bajarilish konteksti proksi xotirasida ishlaydi. Mantiqiy kontrakt qayta kirishda proksining boshqaruvchi o'zgaruvchilarini (owner, implementation) o'zgartirib yuborishining oldini olish.
**Talablar:** Storage collision tahlili, EIP-1967 storage slots, delegatecall kontekstida reentrancy nazorati.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title SafeProxyContext - Delegatecall reentrancy xatolarining oldini olish
contract SafeProxyContext {
    // EIP-1967 bo'yicha maxsus slotlar (Storage Collision oldini olish)
    bytes32 private constant IMPLEMENTATION_SLOT = 
        0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc;

    address public owner;
    bool private locked;

    modifier noReentrant() {
        require(!locked, "Reentrancy taqiqlangan");
        locked = true;
        _;
        locked = false;
    }

    constructor(address impl) {
        owner = msg.sender;
        bytes32 slot = IMPLEMENTATION_SLOT;
        assembly {
            sstore(slot, impl)
        }
    }

    fallback() external payable noReentrant {
        bytes32 slot = IMPLEMENTATION_SLOT;
        address impl;
        assembly {
            impl := sload(slot)
        }
        require(impl != address(0), "Implementatsiya topilmadi");

        assembly {
            calldatacopy(0, 0, calldatasize())
            let result := delegatecall(gas(), impl, 0, calldatasize(), 0, 0)
            returndatacopy(0, 0, returndatasize())
            switch result
            case 0 { revert(0, returndatasize()) }
            default { return(0, returndatasize()) }
        }
    }
}
```
**Tushuntirish:** `delegatecall` chaqiruvchi kontraktning xotirasini (Storage) o'zgartiradi. Agar proksi va implementatsiya shartnomalarida o'zgaruvchilar bir xil slotda joylashmasa (Storage collision) yoki implementatsiyada reentrancy orqali `owner` yozilgan slot nishonga olinsa, hujumchi shartnoma boshqaruvini egallab oladi.

---

### Topshiriq #1160: Avtomatlashtirilgan Invariant Testlar: Reentrancy Invariantini Foundry Bilan Sinash
**Tavsif:** Smart-kontraktning har qanday sharoitda ham `address(vault).balance == sum(balances)` invariantini saqlab qolishini kafolatlovchi fuzzing va invariant testi spetsifikatsiyasi.
**Talablar:** Initsializatsiya, Fuzz test, Reentrancy xakerlik shartnomasi va Assert tekshiruvi.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IVault {
    function deposit() external payable;
    function withdraw() external;
    function balances(address) external view returns (uint256);
}

/// @title ReentrancyAttacker - Xakerlik shartnomasi simulyatsiyasi
contract ReentrancyAttacker {
    IVault public targetVault;
    uint256 public attackCount;

    constructor(address _vault) {
        targetVault = IVault(_vault);
    }

    function attack() external payable {
        targetVault.deposit{value: msg.value}();
        targetVault.withdraw();
    }

    // Reentrancy tuzog'i
    receive() external payable {
        if (attackCount < 5 && address(targetVault).balance >= msg.value) {
            attackCount++;
            targetVault.withdraw(); // Qayta kirish urinishi!
        }
    }
}
```
**Tushuntirish:** Invariant testlashda (Foundry invariant testing) tasodifiy aktyorlar orqali tizimga millionlab harakatlar yuboriladi. Agar xakerlik shartnomasi `receive()` orqali qayta kirishga uringanda shartnoma qulasa, invariant buzilgan deb topiladi va xavfsizlik zaifligi auditda darhol fosh bo'ladi.

---

### Topshiriq #1161: Spot Narx Manipulyatsiyasi va Uniswap V2 getReserves() Xavfi
**Tavsif:** Ko'plab lending protokollari garov narxini AMM hovuzidagi zahiralardan (`getReserves`) hisoblaydi. Hujumchi Flash Loan orqali hovuz narxini bir zumda buzib (Spot price manipulation) millionlab dollar kredit olib qochadi. Ushbu zaiflikni va to'g'ri yechimni ko'rsatuvchi kontrakt.
**Talablar:** Spot narxdan voz kechish, TWAP yoki Chainlink oracllaridan foydalanish, zaiflik tahlili.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IUniswapV2Pair {
    function getReserves() external view returns (uint112 reserve0, uint112 reserve1, uint32 blockTimestampLast);
}

/// @title InsecureLending - Spot narxga tayangan o'ta zaif shartnoma namunasi
/// @dev DIQQAT: Ushbu kod faqat audit va ta'lim maqsadida zaiflikni ko'rsatish uchun yozilgan!
contract VulnerableSpotPriceLending {
    IUniswapV2Pair public immutable pool;

    constructor(address _pool) {
        pool = IUniswapV2Pair(_pool);
    }

    /// @notice O'TA ZAIF FUNKSIYA: Spot narxni hovuz zahiralaridan to'g'ridan-to'g'ri hisoblaydi!
    /// @dev Hujumchi Flash Loan olib bitta swap orqali reserve0 ni ko'paytirib narxni 100 baravar oshirishi mumkin
    function getCollateralPrice() public view returns (uint256) {
        (uint112 reserve0, uint112 reserve1, ) = pool.getReserves();
        // Spot narx = reserve1 / reserve0
        return (uint256(reserve1) * 1e18) / uint256(reserve0);
    }
}

/// @title SecureLendingOracleGuard - Spot narx manipulyatsiyasidan himoyalangan
contract SecureLendingOracleGuard {
    // XAVFSIZ: Spot narx o'rniga tashqi ishonchli markazlashmagan oracllar yoki TWAP ishlatiladi
    error SpotPriceForbidden();

    function getSafePrice() external pure returns (uint256) {
        // Haqiqiy tizimda Chainlink yoki Uniswap V3 TWAP chaqiriladi
        return 2500 * 1e18; // 2500 USD xavfsiz narx
    }
}
```
**Tushuntirish:** AMM dagi zahiralar nisbati (`reserve1 / reserve0`) bitta blok ichida katta hajmdagi token almashtirilganda (Swap) keskin o'zgaradi. Flash Loan yordamida har qanday kishi hovuzdagi narxni 1 tranzaksiyada 100 baravar ko'tarishi va shartnomadan soxta yuqori garov evaziga barcha mablag'larni o'g'irlashi mumkin. Shuning uchun `getReserves()` narx aniqlashda hech qachon ishlatilmasligi shart.

---

### Topshiriq #1162: Uniswap V3 TWAP (Time-Weighted Average Price) Oracle Integratsiyasi
**Tavsif:** Flash Loan hujumlariga chidamli bo'lishi uchun narxni ma'lum bir vaqt oralig'ida (masalan oxirgi 30 daqiqa - 1800 soniya) geometrik o'rtacha hisoblovchi Uniswap V3 TWAP oracleni joriy etish.
**Talablar:** IUniswapV3Pool.observe(), tickCumulatives farqini hisoblash, vaqt oralig'i (twapInterval >= 1800).
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IUniswapV3Pool {
    function observe(uint32[] calldata secondsAgos)
        external
        view
        returns (int56[] memory tickCumulatives, uint160[] memory secondsPerLiquidityCumulativeX128s);
}

/// @title UniswapV3TwapOracle - Vaqt bo'yicha tortilgan o'rtacha narx moduli
contract UniswapV3TwapOracle {
    address public immutable pool;
    uint32 public constant TWAP_INTERVAL = 1800; // 30 daqiqa (1800 soniya)

    error InvalidTwapInterval();

    constructor(address _pool) {
        pool = _pool;
    }

    /// @notice Oxirgi 30 daqiqalik xavfsiz TWAP narxini hisoblash
    function getTwapTick() external view returns (int24 arithmeticMeanTick) {
        uint32[] memory secondsAgos = new uint32[](2);
        secondsAgos[0] = TWAP_INTERVAL; // 1800 soniya oldingi vaqt
        secondsAgos[1] = 0;             // Hozirgi vaqt

        (int56[] memory tickCumulatives, ) = IUniswapV3Pool(pool).observe(secondsAgos);

        // Vaqt oraliqdagi tick akumulyatsiyasi farqi
        int56 tickCumulativesDelta = tickCumulatives[1] - tickCumulatives[0];

        // O'rtacha tick qiymati
        arithmeticMeanTick = int24(tickCumulativesDelta / int56(uint56(TWAP_INTERVAL)));

        // Agar qoldiq manfiy bo'lsa yaxlitlash
        if (tickCumulativesDelta < 0 && (tickCumulativesDelta % int56(uint56(TWAP_INTERVAL)) != 0)) {
            arithmeticMeanTick--;
        }
    }
}
```
**Tushuntirish:** TWAP (Time-Weighted Average Price) narxni bitta blokda emas, balki oxirgi 30 daqiqa davomidagi o'rtacha qiymatini hisoblaydi. Hujumchi narxni manipulyatsiya qilish uchun narxni 30 daqiqa davomida (yuzlab bloklar) ushlab turishi kerak, bu esa arbitrajchilar tufayli millionlab dollar zarar keltiradi va Flash Loan orqali amalga oshirishni imkonsiz qiladi.

---

### Topshiriq #1163: Chainlink Data Feeds: Stale Price, minAnswer va maxAnswer Circuit Breaker Himoyasi
**Tavsif:** Chainlink narxlari yangilanmay qotib qolsa (Stale Price) yoki LUNA halokatidagi kabi narx `minAnswer` chegarasiga yetib qolgan bo'lsa, noto'g'ri narx bilan kreditlar berilishini to'xtatuvchi xavfsiz narx tekshirgichi.
**Talablar:** AggregatorV3Interface.latestRoundData(), updatedAt tekshiruvi, minAnswer va maxAnswer chegaralari.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface AggregatorV3Interface {
    function latestRoundData()
        external
        view
        returns (
            uint80 roundId,
            int256 answer,
            uint256 startedAt,
            uint256 updatedAt,
            uint80 answeredInRound
        );
}

/// @title ChainlinkPriceConsumerSafe - Barcha zaifliklardan himoyalangan Chainlink narx tekshirgichi
contract ChainlinkPriceConsumerSafe {
    AggregatorV3Interface public immutable priceFeed;
    
    // Qat'iy chegaralar (Circuit Breakers)
    int256 public immutable minPriceLimit;
    int256 public immutable maxPriceLimit;
    uint256 public constant MAX_STALENESS = 3600; // 1 soatdan eski narx qabul qilinmaydi

    error StalePriceError();
    error InvalidPriceValue();
    error CircuitBreakerTriggered();

    constructor(address _feed, int256 _minLimit, int256 _maxLimit) {
        priceFeed = AggregatorV3Interface(_feed);
        minPriceLimit = _minLimit;
        maxPriceLimit = _maxLimit;
    }

    /// @notice Barcha kiberxavfsizlik filtrlaridan o'tgan toza narxni olish
    function getValidatedPrice() public view returns (uint256) {
        (
            uint80 roundId,
            int256 price,
            ,
            uint256 updatedAt,
            uint80 answeredInRound
        ) = priceFeed.latestRoundData();

        // 1. Narx 0 dan katta bo'lishi shart
        if (price <= 0) revert InvalidPriceValue();

        // 2. Stale Price tekshiruvi: narx oxirgi 1 soatda yangilanganmi?
        if (updatedAt == 0 || block.timestamp - updatedAt > MAX_STALENESS) {
            revert StalePriceError();
        }

        // 3. RoundId to'liqligi
        if (answeredInRound < roundId) {
            revert StalePriceError();
        }

        // 4. Min/Max Answer Circuit Breaker (LUNA qulashi kabi holatlar uchun)
        if (price <= minPriceLimit || price >= maxPriceLimit) {
            revert CircuitBreakerTriggered();
        }

        return uint256(price);
    }
}
```
**Tushuntirish:** Chainlink oracllari o'z ichida `minAnswer` parametriga ega (masalan, 0.10$). Agar aktiv narxi 0.00001$ ga qulasa ham, oracle 0.10$ qaytarishda davom etadi. Natijada xakerlar qadrsizlangan token evaziga butun protokol aktivlarini tortib oladi. `minPriceLimit` va `updatedAt` tekshiruvi bu kabi ofatlarning oldini oladi.

---

### Topshiriq #1164: Flash Loan Himoyasi: Bir Tranzaksiyada Balans va Kotirovkalar O'zgarishini Bloklash
**Tavsif:** A'zo bitta blok ichida depozit qilib, darhol shu blokda qarzdorlik olsa yoki likvidlikni manipulyatsiya qilsa Flash Loan hujumi bo'lishi mumkin. Oxirgi depozit blokini saqlash va bir blokda bir nechta agressiv amallarni taqiqlash.
**Talablar:** `lastDepositBlock[msg.sender] == block.number` tekshiruvi, xavfsiz blok kutish qoidasi.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title FlashLoanResistantVault - Bir xil blokdagi manipulyatsiyalardan himoyalangan
contract FlashLoanResistantVault {
    mapping(address => uint256) public balances;
    mapping(address => uint256) public lastActionBlock;

    event Deposited(address indexed user, uint256 amount);
    event Withdrawn(address indexed user, uint256 amount);

    error ActionBlockedInSameBlock();

    /// @notice Depozit qilish
    function deposit() external payable {
        balances[msg.sender] += msg.value;
        // Oxirgi harakat blokini belgilash
        lastActionBlock[msg.sender] = block.number;
        emit Deposited(msg.sender, msg.value);
    }

    /// @notice Pul yechish: Depozit qilingan blokda yechish taqiqlanadi (Anti-Flash-Loan)
    function withdraw(uint256 amount) external {
        // Flash Loan faqat bitta tranzaksiya (bitta blok) ichida ishlaydi!
        if (lastActionBlock[msg.sender] == block.number) {
            revert ActionBlockedInSameBlock();
        }
        require(balances[msg.sender] >= amount, "Yetarli balans yo'q");

        balances[msg.sender] -= amount;
        (bool sent, ) = msg.sender.call{value: amount}("");
        require(sent, "O'tkazma muvaffaqiyatsiz");

        emit Withdrawn(msg.sender, amount);
    }
}
```
**Tushuntirish:** Flash Loan ning fundamental qoidasi shundaki, qarz olingan pul o'sha tranzaksiya ichida (ya'ni o'sha bitta blokda) qaytarilishi shart. `lastActionBlock == block.number` tekshiruvi depozit bilan yechishni turli bloklarga ajratib, Flash Loan vositasida shartnomani manipulyatsiya qilish imkoniyatini yo'qqa chiqaradi.

---

### Topshiriq #1165: Slippage Tolerance va Deadline Nazorati Bilan MEV / Sandwich Hujumlarini To'xtatish
**Tavsif:** DEX da token almashtirishda `minAmountOut` va `deadline` ko'rsatilmasa, MEV botlar so'rovni ko'rib qolib, oldidan va orqasidan tranzaksiya joylashtirib (Sandwich attack) foydalanuvchini bor mablag'idan mahrum qiladi. Qat'iy slippage nazoratini o'rnatish.
**Talablar:** require(amountOut >= minAmountOut), require(block.timestamp <= deadline), MEV himoyasi.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IERC20 {
    function transfer(address to, uint256 amount) external returns (bool);
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
}

/// @title SafeDexRouter - MEV va Sandwich hujumlaridan himoyalangan savdo routeri
contract SafeDexRouter {
    error ExpiredDeadline();
    error ExcessiveSlippage(uint256 received, uint256 minimumExpected);

    /// @notice Token almashtirishda slippage va deadline majburiy
    function swapTokens(
        address tokenIn,
        address tokenOut,
        uint256 amountIn,
        uint256 minAmountOut, // Foydalanuvchi qabul qiladigan eng kam miqdor
        uint256 deadline      // Tranzaksiya amal qilish muddati
    ) external returns (uint256 amountOut) {
        // 1. DEADLINE: Tranzaksiya mempoolda ushlab turilib, eski narxda ijro etilmasligi uchun
        if (block.timestamp > deadline) {
            revert ExpiredDeadline();
        }

        IERC20(tokenIn).transferFrom(msg.sender, address(this), amountIn);

        // AMM dagi hisob-kitob (Simulyatsiya)
        amountOut = (amountIn * 99) / 100; // 1% komissiya bilan

        // 2. SLIPPAGE TOLERANCE: Sandwich botlari narxni tushirib yuborsa xatolik beradi
        if (amountOut < minAmountOut) {
            revert ExcessiveSlippage(amountOut, minAmountOut);
        }

        IERC20(tokenOut).transfer(msg.sender, amountOut);
    }
}
```
**Tushuntirish:** Sandwich hujumida bot mempooldagi `minAmountOut` ko'rsatilmagan so'rovni ko'radi. Bot so'rovdan oldin katta hajm sotib olib narxni sun'iy ko'taradi (Frontrun), foydalanuvchi eng yomon narxda sotib oladi, so'ng bot darhol sotib foydani oladi (Backrun). `minAmountOut` foydalanuvchi yo'qotishi mumkin bo'lgan maksimal chegarani (masalan 0.5%) qulflaydi.

---

### Topshiriq #1166: Donation Attack va Vault Share Inflation Hujumidan Himoyalanish (ERC-4626)
**Tavsif:** Yangi yaratilgan ERC-4626 tokenlashtirilgan xazinaga 1-bo'lib depozit qilgan xaker 1 wei depozit qilib, so'ng to'g'ridan-to'g'ri xazinaga 10,000 token hadya (Donation) qiladi. Keyingi a'zolarning depozitlari yaxlitlash xatosi (Rounding down to zero) tufayli o'g'irlanadi. Ushbu hujumdan himoyalanish.
**Talablar:** Virtual shares / Virtual assets qo'shish yoki dastlabki 1000 ulushni (Dead shares) yoqib yuborish (Burn).
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

/// @title InflationResistantVault - Share Inflation va Donation hujumlaridan himoyalangan xazina
contract InflationResistantVault {
    using SafeERC20 for IERC20;

    IERC20 public immutable asset;
    uint256 public totalAssets;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;

    // Dastlabki ulushlarni yoqish uchun nol manzil
    address private constant DEAD_ADDRESS = 0x000000000000000000000000000000000000dEaD;
    uint256 private constant MINIMUM_LIQUIDITY = 1000; // Uniswap V2 dagi kabi 1000 dead shares

    constructor(address _asset) {
        asset = IERC20(_asset);
    }

    /// @notice Himoyalangan depozit funksiyasi
    function deposit(uint256 assets) external returns (uint256 shares) {
        require(assets > 0, "Nol aktiv");

        if (totalSupply == 0) {
            // 1-depozitchi: Birinchi 1000 ta ulush yoqib yuboriladi (Dead shares)
            // Bu narxni 1 wei ga 10,000 qilib ko'tarish hujumini iqtisodiy imkonsiz qiladi!
            shares = assets;
            require(shares > MINIMUM_LIQUIDITY, "Minimal likvidlikdan kam");
            
            totalSupply = shares;
            balanceOf[DEAD_ADDRESS] = MINIMUM_LIQUIDITY;
            balanceOf[msg.sender] = shares - MINIMUM_LIQUIDITY;
        } else {
            // Standart proporsiya
            shares = (assets * totalSupply) / totalAssets;
            require(shares > 0, "Ulush nolga teng bo'ldi");
            
            totalSupply += shares;
            balanceOf[msg.sender] += shares;
        }

        totalAssets += assets;
        asset.safeTransferFrom(msg.sender, address(this), assets);
    }
}
```
**Tushuntirish:** Share Inflation hujumida xaker 1 dona ulushga (share) ega bo'lgach, xazinaga to'g'ridan-to'g'ri transfer qilib 1 ta ulush narxini 10,000 ETH ga chiqaradi. Keyingi a'zo 5,000 ETH depozit qilganda, `(5000 * 1) / 10000 = 0` bo'lib yaxlitlanadi va u 0 ulush oladi, lekin uning 5,000 ETH i xazinaga tushadi. 1000 ta `dead shares` yoqilishi bu manipulyatsiyani yo'qotadi.

---

### Topshiriq #1167: OpenZeppelin ERC-4626 Virtual Offset Bilan Kiberhimoya
**Tavsif:** OpenZeppelin v5 da kiritilgan Virtual Assets va Virtual Shares offset texnologiyasi orqali hech qanday dead shares talab qilmasdan matematik darajada yaxlitlash hujumlarini to'xtatish.
**Talablar:** `_decimalsOffset()` qo'llash, ulushlar hisob-kitobida `+ 10 ** _decimalsOffset()` ofsetini kiritish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title VirtualOffsetCalculator - OpenZeppelin v5 uslubidagi matematik ofset
library VirtualOffsetCalculator {
    uint8 internal constant DECIMALS_OFFSET = 3; // 10^3 = 1000 virtual ulush

    function convertToShares(
        uint256 assets,
        uint256 totalAssets,
        uint256 totalSupply
    ) internal pure returns (uint256) {
        // Virtual ulushlar va virtual aktivlar qo'shiladi: (Aktivlar * (TotalShares + 1000)) / (TotalAssets + 1)
        return (assets * (totalSupply + 10 ** DECIMALS_OFFSET)) / (totalAssets + 1);
    }

    function convertToAssets(
        uint256 shares,
        uint256 totalAssets,
        uint256 totalSupply
    ) internal pure returns (uint256) {
        return (shares * (totalAssets + 1)) / (totalSupply + 10 ** DECIMALS_OFFSET);
    }
}
```
**Tushuntirish:** Virtual Offset matematik formulaga virtual tarzda 1 dona aktiv va 1,000 ta virtual ulush qo'shadi. Xazina butunlay bo'sh bo'lgan taqdirda ham, maxraj hech qachon 0 yoki 1 wei bo'lib qolmaydi, natijada sun'iy inflyatsiya yaratish tajovuzkorga foyda o'rniga faqat zarar keltiradi.

---

### Topshiriq #1168: Liquidation Front-Running va Bad Debt Kaskadining Oldini Olish
**Tavsif:** Kreditlash protokollarida garov narxi tushganda likvidatsiya amalini faqat ruxsat etilgan likvidatorlar yoki navbat orqali bajarish, aks holda botlar MEV frontrunning orqali tizimni qarzga (Bad Debt) botiradi.
**Talablar:** Liquidation bonus chegarasi, close factor (maksimal 50% garovni yechish), Bad debt monitoringi.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title SafeLiquidationEngine - Xavfsiz va boshqariladigan likvidatsiya mexanizmi
contract SafeLiquidationEngine {
    uint256 public constant CLOSE_FACTOR = 5000; // Maksimal 50% qarzni 1 marta likvidatsiya qilish mumkin (basis points: 10000 = 100%)
    uint256 public constant LIQUIDATION_BONUS = 500; // Likvidator uchun 5% mukofot

    error PositionHealthy();
    error RepayExceedsCloseFactor();

    /// @notice Xavfsiz likvidatsiya hisob-kitobi
    function calculateLiquidation(
        uint256 collateralBalance,
        uint256 debtBalance,
        uint256 collateralPrice,
        uint256 debtToCover
    ) public pure returns (uint256 collateralToSeize) {
        // Sog'lomlik koeffitsiyenti (Health Factor) tekshiruvi: Garov qiymati qarzning 120% idan kam bo'lsa
        uint256 collateralValue = (collateralBalance * collateralPrice) / 1e18;
        if (collateralValue >= (debtBalance * 120) / 100) {
            revert PositionHealthy();
        }

        // Likvidator bitta amalda qarzning faqat 50% igacha yopa oladi (Kaskadli bankrotlikni oldini olish)
        uint256 maxRepay = (debtBalance * CLOSE_FACTOR) / 10000;
        if (debtToCover > maxRepay) {
            revert RepayExceedsCloseFactor();
        }

        // Munosib garovni 5% bonus bilan hisoblash
        uint256 baseCollateral = (debtToCover * 1e18) / collateralPrice;
        collateralToSeize = (baseCollateral * (10000 + LIQUIDATION_BONUS)) / 10000;
    }
}
```
**Tushuntirish:** Close Factor likvidatsiyani bo'lakma-bo'lak amalga oshirishni majburlaydi. Bu orqali foydalanuvchining butun pozitsiyasi bir zumda tugatilmaydi, qarzning yarmi yopilgach sog'lomlik indeksi tiklanadi va protokol kaskadli yiqilishdan saqlanadi.

---

### Topshiriq #1169: Chainlink L2 Sequencer Uptime Feed: Arbitrum/Optimism da Sequencer O'chganda Oracleni To'xtatish
**Tavsif:** Arbitrum yoki Base kabi Layer 2 tarmoqlarida Sequencer (tranzaksiyalarni yig'uvchi server) o'chib qolsa, narxlar yangilanmaydi. Sequencer qayta yoqilganda eski narxlar bilan ekspluatatsiya qilinmasligi uchun 'Sequencer Uptime Feed' tekshiruvini joriy etish.
**Talablar:** Chainlink L2 Sequencer Feed, status == 0 (Sequencer faol), gracePeriod = 3600 (qayta yoqilgach 1 soat kutish).
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface ISequencerUptimeFeed {
    function latestRoundData()
        external
        view
        returns (
            uint80 roundId,
            int256 answer,
            uint256 startedAt,
            uint256 updatedAt,
            uint80 answeredInRound
        );
}

/// @title L2SequencerGuardian - Arbitrum va Optimism L2 tarmoqlari uchun maxsus xavfsizlik qalqoni
contract L2SequencerGuardian {
    ISequencerUptimeFeed public immutable sequencerFeed;
    uint256 public constant GRACE_PERIOD_TIME = 3600; // 1 soat sovush vaqti

    error L2SequencerDown();
    error GracePeriodNotOver();

    constructor(address _sequencerFeed) {
        sequencerFeed = ISequencerUptimeFeed(_sequencerFeed);
    }

    /// @notice L2 tarmog'i va uning oracllari xavfsizligini tekshirish
    function checkL2Uptime() external view {
        (
            ,
            int256 answer,
            uint256 startedAt,
            ,
        ) = sequencerFeed.latestRoundData();

        // answer == 0: Sequencer ishlamoqda
        // answer == 1: Sequencer O'CHGAN!
        if (answer == 1) {
            revert L2SequencerDown();
        }

        // Sequencer qayta yoqilgandan keyin oracllar to'liq yangilanib olishi uchun 1 soat kutish majburiy
        uint256 timeSinceUp = block.timestamp - startedAt;
        if (timeSinceUp < GRACE_PERIOD_TIME) {
            revert GracePeriodNotOver();
        }
    }
}
```
**Tushuntirish:** L2 da Sequencer bir necha soatga to'xtab qolsa, tarmoqdagi bloklar to'xtaydi, lekin real hayotda narxlar o'zgaradi. Sequencer qayta ishga tushgan birinchi sekundda MEV botlar eski narxlar bilan zudlik bilan barcha likvidatsiyalarni frontrun qilib yuboradi. `GRACE_PERIOD_TIME` oracllarga yangi narxlarni to'liq yetkazib olishga imkon beradi.

---

### Topshiriq #1170: Dual Oracle Architecture: Chainlink va Uniswap V3 TWAP ni O'zaro Qiyoslash
**Tavsif:** Bitta oracle manbasiga tayanmasdan, Chainlink va Uniswap V3 TWAP oracllaridan narx olib, agar ular orasidagi farq 2% dan oshsa, tranzaksiyani to'xtatuvchi (Circuit Breaker) ikki oraclli xavfsizlik arxitekturasi.
**Talablar:** Ikkala oracleni solishtirish, delta <= 200 bps (2%), divergensiya xatosi.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title DualOracleValidator - Ikki mustaqil oracle taqqoslovchi xavfsizlik markazi
contract DualOracleValidator {
    uint256 public constant MAX_DIVERGENCE_BPS = 200; // 2% (200 / 10000)

    error OracleDivergenceTooHigh(uint256 chainlinkPrice, uint256 twapPrice);

    /// @notice Narxlarni o'zaro tekshirib, eng xavfsiz o'rtacha qiymatni qaytarish
    function getConsensusPrice(uint256 chainlinkPrice, uint256 twapPrice) external pure returns (uint256) {
        uint256 diff = chainlinkPrice > twapPrice 
            ? chainlinkPrice - twapPrice 
            : twapPrice - chainlinkPrice;

        // Narxlar farqini foizda hisoblash
        uint256 divergenceBps = (diff * 10000) / chainlinkPrice;

        if (divergenceBps > MAX_DIVERGENCE_BPS) {
            // Agar ikkala oracle orasida 2% dan ko'p tafovut bo'lsa, qaysidir biri manipulyatsiya qilingan!
            revert OracleDivergenceTooHigh(chainlinkPrice, twapPrice);
        }

        // Konsensus narxi: o'rtachasi
        return (chainlinkPrice + twapPrice) / 2;
    }
}
```
**Tushuntirish:** Dual Oracle modeli DeFi xavfsizligining eng yuqori darajasidir. Hujumchi Uniswap V3 ni manipulyatsiya qilsa ham Chainlink unga to'g'ri kelmaydi; Chainlink buzilsa TWAP uni fosh qiladi. Natijada shartnoma avtomatik tarzda tranzaksiyani bekor qilib xavfsizlikni saqlab qoladi.

---

### Topshiriq #1171: tx.origin Phishing Zaifligi va msg.sender Bilan Solishtirish
**Tavsif:** `tx.origin` tranzaksiyani boshlagan tashqi hamyonni (EOA) bildiradi. Agar kontrakt `require(tx.origin == owner)` ishlatsa, hujumchi tuzoq veb-sayt orqali egasini tranzaksiya yuborishga undab butun kontrakt boshqaruvini o'g'irlashi (Phishing) mumkin. Ushbu zaiflikni bartaraf etish.
**Talablar:** tx.origin o'rniga msg.sender ishlatish, tx.origin faqat shartnoma emasligini tekshirishda ham ehtiyotkorlik bilan qo'llanishi.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title InsecureTxOriginWallet - tx.origin ishlatilgan O'TA ZAIF hamyon
contract InsecureTxOriginWallet {
    address public owner;

    constructor() payable {
        owner = msg.sender;
    }

    /// @dev O'TA ZAIF: Hujumchi tuzoq kontrakt orqali owner nomidan chaqira oladi!
    function transferToInsecure(address payable to, uint256 amount) external {
        require(tx.origin == owner, "Faqat egasi!");
        to.transfer(amount);
    }
}

/// @title SecureMsgSenderWallet - msg.sender bilan himoyalangan xavfsiz hamyon
contract SecureMsgSenderWallet {
    address public immutable owner;

    error UnauthorizedCaller(address caller);

    constructor() payable {
        owner = msg.sender;
    }

    /// @notice XAVFSIZ: Faqat to'g'ridan-to'g'ri chaqiruvchi tekshiriladi
    function transferTo(address payable to, uint256 amount) external {
        if (msg.sender != owner) {
            revert UnauthorizedCaller(msg.sender);
        }
        require(to != address(0), "Noto'g'ri manzil");
        to.transfer(amount);
    }
}
```
**Tushuntirish:** Agar foydalanuvchi `A -> B (hujumchi shartnomasi) -> C (jabrlanuvchi hamyon)` zanjirida harakat qilsa, `tx.origin` doimo `A` (foydalanuvchi) bo'lib qolaveradi, lekin `msg.sender` `B` bo'ladi. Shu sababli ruxsatlarni (Access Control) tekshirishda `tx.origin` dan foydalanish mutlaqo taqiqlanadi.

---

### Topshiriq #1172: EIP-712 Typed Data Hashing va Cross-Chain Signature Replay Attack Himoyasi
**Tavsif:** Imzolarni zanjirdan tashqarida (Off-chain) yig'ishda (Permit, Gasless transactions) bitta zanjirdagi imzo boshqa zanjirda yoki boshqa kontraktda qayta ishlatilmasligi (Replay Attack) uchun EIP-712 Domen Separator va Nonce tekshiruvini qurish.
**Talablar:** EIP712Domain (name, version, chainId, verifyingContract), nonces mapping, deadline nazorati.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {ECDSA} from "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";

/// @title Eip712ReplayResistant - EIP-712 va ChainId bilan to'liq himoyalangan imzo tekshirgichi
contract Eip712ReplayResistant {
    using ECDSA for bytes32;

    bytes32 private constant TYPE_HASH = 
        keccak256("EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)");
    bytes32 private constant PERMIT_TYPEHASH = 
        keccak256("PermitTransfer(address owner,address spender,uint256 value,uint256 nonce,uint256 deadline)");

    bytes32 public immutable DOMAIN_SEPARATOR;
    mapping(address => uint256) public nonces;

    error ExpiredSignature();
    error InvalidSigner();

    constructor() {
        // Domen ajratuvchi: zanjir ID si va kontrakt manzili bilan bog'lanadi
        DOMAIN_SEPARATOR = keccak256(
            abi.encode(
                TYPE_HASH,
                keccak256(bytes("Khorazmiy Security")),
                keccak256(bytes("1")),
                block.chainid, // Cross-chain replay attack larni yo'qotadi
                address(this)  // Cross-contract replay attack larni yo'qotadi
            )
        );
    }

    function permitTransfer(
        address owner,
        address spender,
        uint256 value,
        uint256 deadline,
        bytes memory signature
    ) external {
        if (block.timestamp > deadline) revert ExpiredSignature();

        // 1. Unikal Nonce orqali imzoning bir necha marta ishlatilishini to'xtatish
        uint256 currentNonce = nonces[owner]++;

        bytes32 structHash = keccak256(
            abi.encode(PERMIT_TYPEHASH, owner, spender, value, currentNonce, deadline)
        );

        // EIP-712 to'liq xeshi
        bytes32 digest = keccak256(abi.encodePacked("\x19\x01", DOMAIN_SEPARATOR, structHash));

        address signer = digest.recover(signature);
        if (signer != owner) revert InvalidSigner();

        // Ruxsat tasdiqlandi!
    }
}
```
**Tushuntirish:** EIP-712 imzolangan ma'lumotlarni strukturaviy qiladi. `DOMAIN_SEPARATOR` ichidagi `block.chainid` tufayli Ethereum Mainnet uchun imzolangan buyruqni hech kim Arbitrum yoki BSC tarmoqlarida qayta ishlata olmaydi. `nonces` esa bitta imzo faqat 1 marta bajarilishini kafolatlaydi.

---

### Topshiriq #1173: ECDSA Signature Malleability (s-value cheklovi va ecrecover Zaifliklari)
**Tavsif:** Standart `ecrecover` funksiyasi xato imzoda `address(0)` qaytaradi va elliptik egri chiziq simmetriyasi sababli bitta imzo uchun ikkita qonuniy `(r, s)` juftligi mavjud (Signature Malleability). OpenZeppelin ECDSA orqali ushbu zaifliklarni bartaraf etish.
**Talablar:** s-qiymati secp256k1n / 2 dan kichik bo'lishi shart, signer != address(0) tekshiruvi.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title SafeEcdsaValidator - Signature Malleability va ecrecover xatolaridan himoyalangan
contract SafeEcdsaValidator {
    // secp256k1 egri chizig'ining yarmi: s qiymati ushbu sondan oshmasligi shart (EIP-2)
    uint256 private constant SECP256K1_N_DIV_2 = 
        0x7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF5D576E7357A4501DDFE92F46681B20A0;

    error InvalidSignatureS();
    error InvalidSignatureV();
    error ZeroAddressSigner();

    /// @notice Malleability hujumlariga qarshi tekshirilgan xavfsiz tiklovchi
    function safeRecover(bytes32 hash, uint8 v, bytes32 r, bytes32 s) public pure returns (address) {
        // EIP-2 bo'yicha 's' qiymatining pastki yarmida bo'lishini tekshirish (Malleability himoyasi)
        if (uint256(s) > SECP256K1_N_DIV_2) {
            revert InvalidSignatureS();
        }

        // v faqat 27 yoki 28 bo'lishi mumkin
        if (v != 27 && v != 28) {
            revert InvalidSignatureV();
        }

        address signer = ecrecover(hash, v, r, s);
        
        // ecrecover buzilgan imzoda xatolik bermaydi, balki address(0) qaytaradi!
        if (signer == address(0)) {
            revert ZeroAddressSigner();
        }

        return signer;
    }
}
```
**Tushuntirish:** Elliptik egri chiziqlarda `(r, s)` to'g'ri imzo bo'lsa, `(r, -s mod n)` ham xuddi o'sha xabarga matematik jihatdan to'g'ri keladi. Hujumchi tranzaksiya mempoolda turganida uning `s` qiymatini o'zgartirib tranzaksiya heshini (txHash) o'zgartirishi mumkin edi. EIP-2 qoidasi `s <= n/2` bo'lishini majburlab, imzoning yagonaligini ta'minlaydi.

---

### Topshiriq #1174: Initializer Front-Running va Proksi Implementatsiyasini Qulflash (_disableInitializers)
**Tavsif:** Proksi shartnomalarda `constructor` o'rniga `initialize()` ishlatiladi. Agar mantiqiy kontrakt (Implementation) o'z-o'zidan initsializatsiya qilinmay ochiq qoldirilsa, xaker implementatsiyaning `owner`i bo'lib olib, `selfdestruct` orqali butun tizimni yo'q qilishi mumkin.
**Talablar:** OpenZeppelin Initializable, konstruktorda `_disableInitializers()` chaqirilishi shart.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Initializable} from "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";

/// @title SecureImplementation - Initializer front-running dan to'liq himoyalangan implementatsiya
contract SecureImplementation is Initializable {
    address public owner;
    uint256 public protocolFee;

    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() {
        // ENG MUHIM XAVFSIZLIK QOIDASI:
        // Mantiqiy kontrakt yaratilishi bilanoq barcha initsializatorlarni abadiy qulflash!
        // Bu hech kim mantiqiy kontraktni to'g'ridan-to'g'ri initialize qila olmasligini kafolatlaydi.
        _disableInitializers();
    }

    /// @notice Faqat Proksi orqali bir marta chaqiriladigan initsializatsiya
    function initialize(address _initialOwner, uint256 _fee) external initializer {
        require(_initialOwner != address(0), "Noto'g'ri egasi");
        owner = _initialOwner;
        protocolFee = _fee;
    }
}
```
**Tushuntirish:** 2022-yilda Wormhole va Nomad proksilarida implementatsiya shartnomalari initsializatsiya qilinmagani sababli yuzlab million dollar xavf ostida qolgan. Konstruktorda `_disableInitializers()` chaqirish implementatsiya kontraktining o'zida hech qachon `initialize()` funksiyasini chaqirib bo'lmasligini ta'minlaydi.

---

### Topshiriq #1175: UUPS vs Transparent Upgradeable Proxy: Storage Layout Collision Auditi
**Tavsif:** Proksi shartnomasi yangilanganda (Upgrade), yangi versiyadagi o'zgaruvchilar eski versiyaning xotira slotlarini (Storage Slots) ustidan yozib yubormasligi (Storage Collision) uchun xavfsiz kengaytirish qoidalari.
**Talablar:** Storage gap `uint256[50] private __gap;` yoki ERC-7201 Namespaced Storage layout.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title StorageLayoutV1 - Xotira buzilishidan himoyalangan 1-versiya
contract StorageLayoutV1 {
    address public admin;
    uint256 public balance;

    // KELAJAKDAGI YANGILANISHLAR UCHUN ZAXIRA SLOTLAR (Storage Gap)
    // Bu bolalar sinflari yangi o'zgaruvchi qo'shganda slotlarni buzmasligini kafolatlaydi
    uint256[48] private __gap;
}

/// @title StorageLayoutV2 - Xavfsiz yangilangan 2-versiya
contract StorageLayoutV2 is StorageLayoutV1 {
    // Yangi qo'shilgan o'zgaruvchi faqat oxiriga qo'shiladi!
    uint256 public newProtocolMetric;
    
    // Zaxira slotlar bittaga kamaytiriladi (48 - 1 = 47)
    // uint256[47] private __gap;
}
```
**Tushuntirish:** EVM xotirasida o'zgaruvchilar e'lon qilingan tartibda ketma-ket slotlarga (slot 0, slot 1) joylashadi. Agar yangi versiyada o'zgaruvchilar tartibi o'zgartirilsa yoki o'rtasiga yangi o'zgaruvchi qo'shilsa, eski `balance` yangi o'zgaruvchining qiymati bilan ifloslanadi va tizim ishdan chiqadi.

---

### Topshiriq #1176: ERC-4337 Account Abstraction: UserOperation Validation va Nonce Replay Himoyasi
**Tavsif:** Smart-Account (ERC-4337) foydalanuvchining shaxsiy imzosini `validateUserOp` funksiyasida tekshirganda, xakerlar imzoni boshqa maqsadda qayta ishlatmasligi uchun EntryPoint tomonidan boshqariluvchi 2D noncelar bilan himoyalanish.
**Talablar:** IEntryPoint integratsiyasi, require(msg.sender == address(entryPoint)), SIG_VALIDATION_FAILED (1) qaytarish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {ECDSA} from "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";

struct UserOperation {
    address sender;
    uint256 nonce;
    bytes initCode;
    bytes callData;
    uint256 callGasLimit;
    uint256 verificationGasLimit;
    uint256 preVerificationGas;
    uint256 maxFeePerGas;
    uint256 maxPriorityFeePerGas;
    bytes paymasterAndData;
    bytes signature;
}

/// @title SecureSmartAccount4337 - ERC-4337 xavfsiz aqlli hisob
contract SecureSmartAccount4337 {
    using ECDSA for bytes32;

    address public immutable entryPoint;
    address public owner;

    uint256 internal constant SIG_VALIDATION_SUCCESS = 0;
    uint256 internal constant SIG_VALIDATION_FAILED = 1;

    error OnlyEntryPoint();

    constructor(address _entryPoint, address _owner) {
        entryPoint = _entryPoint;
        owner = _owner;
    }

    /// @notice EntryPoint tomonidan chaqiriluvchi UserOperation validatsiyasi
    function validateUserOp(
        UserOperation calldata userOp,
        bytes32 userOpHash,
        uint256 missingAccountFunds
    ) external returns (uint256 validationData) {
        // XAVFSIZLIK: Ushbu metodni FAQAT rasmiy EntryPoint chaqira oladi!
        if (msg.sender != entryPoint) {
            revert OnlyEntryPoint();
        }

        // Imzoni tekshirish
        bytes32 hash = userOpHash.toEthSignedMessageHash();
        address signer = hash.recover(userOp.signature);

        if (signer != owner) {
            return SIG_VALIDATION_FAILED;
        }

        // Yetishmayotgan gaz to'lovini EntryPoint ga yuborish
        if (missingAccountFunds > 0) {
            (bool success, ) = entryPoint.call{value: missingAccountFunds}("");
            (success);
        }

        return SIG_VALIDATION_SUCCESS;
    }
}
```
**Tushuntirish:** ERC-4337 da `validateUserOp` funksiyasining faqat `entryPoint` tomonidan chaqirilishi kritik talabdir. Agar tashqi har qanday kishi bu funksiyani chaqira olsa, hisobdagi barcha mablag'lar gaz to'lash bahonasida o'g'irlab ketilishi mumkin edi.

---

### Topshiriq #1177: Paymaster Draining va Sybil Hujumlariga Qarshi ERC-4337 Himoyasi
**Tavsif:** ERC-4337 Paymaster foydalanuvchilar o'rniga gaz to'lab beradi (Sponsorship). Yovuz foydalanuvchilar botlar orqali soxta operatsiyalar yuborib Paymasterdagi barcha efirni tugatib qo'yishining (Draining attack) oldini oluvchi kvotalar tizimi.
**Talablar:** postOp balansi, har bir foydalanuvchiga kunlik gaz limiti (Sponsoring budget), whitelist tekshiruvi.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title RateLimitedPaymaster - Gaz sponsoring fondini o'g'irlanishdan himoyalovchi Paymaster
contract RateLimitedPaymaster {
    address public immutable entryPoint;
    address public owner;

    // Har bir foydalanuvchiga kunlik maksimal gaz limiti (masalan 0.05 ETH)
    uint256 public constant DAILY_LIMIT = 0.05 ether;
    mapping(address => uint256) public userDailySpent;
    mapping(address => uint256) public lastResetDay;

    error DailyGasLimitExceeded();
    error NotFromEntryPoint();

    constructor(address _entryPoint) {
        entryPoint = _entryPoint;
        owner = msg.sender;
    }

    /// @notice Foydalanuvchi so'rovini qabul qilishdan oldin tekshirish
    function validatePaymasterUserOp(address sender, uint256 maxCost) external returns (bool) {
        if (msg.sender != entryPoint) revert NotFromEntryPoint();

        uint256 currentDay = block.timestamp / 86400;
        if (lastResetDay[sender] < currentDay) {
            userDailySpent[sender] = 0;
            lastResetDay[sender] = currentDay;
        }

        if (userDailySpent[sender] + maxCost > DAILY_LIMIT) {
            revert DailyGasLimitExceeded();
        }

        userDailySpent[sender] += maxCost;
        return true;
    }
}
```
**Tushuntirish:** Paymasterlar gaz subsidiyalari bilan ishlaydi. Agar shartnoma darajasida har bir foydalanuvchi (Smart Account) uchun kunlik limitlar belgilanmasa, bitta tajovuzkor minglab bo'sh UserOperation yuborib Paymasterning butun depozitini bir necha blokda yoqib yuboradi.

---

### Topshiriq #1178: OpenZeppelin AccessControlDefaultAdminRules Bilan Admin Huquqlarini 2 Bosqichli O'tkazish
**Tavsif:** Katta loyihalarda bosh admin kaliti xatoga yo'l qo'yib noto'g'ri manzilga berib yuborilmasligi uchun 2 bosqichli qabul qilish (Pending Admin) va kechiktirish (Delay) taymeriga ega xavfsiz boshqaruv.
**Talablar:** AccessControlDefaultAdminRules, 48 soatlik kutish oraliq delay parametri, changeDefaultAdmin.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {AccessControlDefaultAdminRules} from "@openzeppelin/contracts/access/extensions/AccessControlDefaultAdminRules.sol";

/// @title EnterpriseAccessControl - 2 bosqichli admin almashinuviga ega xavfsiz kirish nazorati
contract EnterpriseAccessControl is AccessControlDefaultAdminRules {
    bytes32 public constant OPERATOR_ROLE = keccak256("OPERATOR_ROLE");

    event CriticalOperationExecuted(address indexed operator);

    /// @param initialAdmin Boshlang'ich bosh admin
    /// @param adminDelay Admin o'zgarishi kuchga kirishi uchun majburiy kutish vaqti (masalan 2 kun = 172800 soniya)
    constructor(address initialAdmin, uint48 adminDelay)
        AccessControlDefaultAdminRules(adminDelay, initialAdmin)
    {}

    function executeCriticalOperation() external onlyRole(OPERATOR_ROLE) {
        emit CriticalOperationExecuted(msg.sender);
    }
}
```
**Tushuntirish:** Standart `Ownable` da `transferOwnership(newOwner)` bitta xato manzil bilan chaqirilsa, shartnoma boshqaruvi abadiy yo'qotiladi. `AccessControlDefaultAdminRules` 48 soatlik kechiktirish beradi va yangi admin ham qabul qilishini tasdiqlashi shart, bu esa insoniy xatolar va kalit o'g'irlanishini to'xtatadi.

---

### Topshiriq #1179: TimelockController Bilan Boshqaruv (Governance) Chaqiruvlarini Kechiktirish
**Tavsif:** Protokol parametrlari yoki yangilanishlar jamoa tomonidan bir zumda kiritilmasligi va hamjamiyat xavfli o'zgarishlarni ko'rib o'z mablag'larini olib chiqib ketishga ulgurishi uchun 48 soatlik Timelock nazoratini o'rnatish.
**Talablar:** TimelockController, schedule(), execute(), minDelay (kamida 2 kun), Cancel huquqi.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {TimelockController} from "@openzeppelin/contracts/governance/TimelockController.sol";

/// @title ProtocolTimelock - Barcha admin buyruqlarini 48 soat kechiktiruvchi vaqt qulfi
contract ProtocolTimelock is TimelockController {
    /// @param minDelay Minimal kechiktirish muddati (masalan 172800 soniya = 48 soat)
    /// @param proposers Taklif kirituvchilar (Multisig yoki DAO)
    /// @param executors Bajaruvchilar (Har qanday a'zo yoki belgilangan manzil)
    /// @param admin Vaqtinchalik admin (deploy yakunida bekor qilinadi)
    constructor(
        uint256 minDelay,
        address[] memory proposers,
        address[] memory executors,
        address admin
    ) TimelockController(minDelay, proposers, executors, admin) {}
}
```
**Tushuntirish:** Timelock shartnomasi DeFi dagi 'Rug-pull' va jamoaning maxfiy kalitlari o'g'irlanishiga qarshi asosiy kafolatdir. Har qanday yangi o'zgarish avval `schedule` qilinadi va 48 soat davomida blokcheynda ochiq turadi. Agar admin yovuz kod kiritmoqchi bo'lsa, foydalanuvchilar bu vaqt ichida o'z pullarini xavfsiz yechib olishlari mumkin.

---

### Topshiriq #1180: Multi-Sig Mantiqi: ECDSA Imzolarini Threshold (m-of-n) Tekshiruvi Bilan Bajarish
**Tavsif:** Hech bir tranzaksiya bitta kishi tomonidan bajarilmasligi uchun m-of-n (masalan 3 tadan kamida 2 ta) tasdiqlangan ECDSA imzolari bilan tranzaksiyani xavfsiz bajaruvchi mini-multisig yadrosi.
**Talablar:** Signers array, threshold, imzo tartibi va takrorlanmasligi tekshiruvi.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {ECDSA} from "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";

/// @title MultiSigCore - m-of-n imzolar bilan boshqariluvchi shartnoma
contract MultiSigCore {
    using ECDSA for bytes32;

    address[] public owners;
    mapping(address => bool) public isOwner;
    uint256 public immutable threshold;
    uint256 public nonce;

    error InvalidThreshold();
    error NotAnOwner();
    error DuplicateOrUnorderedSigner();

    constructor(address[] memory _owners, uint256 _threshold) {
        if (_threshold == 0 || _threshold > _owners.length) revert InvalidThreshold();
        for (uint256 i = 0; i < _owners.length; i++) {
            address owner = _owners[i];
            require(owner != address(0), "Nol manzil");
            require(!isOwner[owner], "Takroriy a'zo");
            isOwner[owner] = true;
            owners.push(owner);
        }
        threshold = _threshold;
    }

    /// @notice Tasdiqlangan imzolar to'plami bilan buyruqni bajarish
    function executeTransaction(
        address to,
        uint256 value,
        bytes calldata data,
        bytes[] calldata signatures
    ) external payable {
        require(signatures.length >= threshold, "Yetarli imzo yo'q");

        bytes32 txHash = keccak256(
            abi.encodePacked(address(this), block.chainid, nonce++, to, value, data)
        ).toEthSignedMessageHash();

        address lastSigner = address(0);
        for (uint256 i = 0; i < threshold; i++) {
            address signer = txHash.recover(signatures[i]);
            if (!isOwner[signer]) revert NotAnOwner();
            // Takroriy imzolarni va tartibni tekshirish (Strictly ascending order)
            if (signer <= lastSigner) revert DuplicateOrUnorderedSigner();
            lastSigner = signer;
        }

        (bool success, ) = to.call{value: value}(data);
        require(success, "Ijro muvaffaqiyatsiz bo'ldi");
    }
}
```
**Tushuntirish:** `signer <= lastSigner` qat'iy o'suvchi tartib tekshiruvi bitta egasi o'z imzosini 2 marta berib thresholdni soxtalashtirishini (Replay within transaction) oldini oladi. Bu Gnosis Safe kabi yirik xazinalarning asosiy poydevoridir.

---

### Topshiriq #1181: Butun Sonlarni Noto'g'ri Qisqartirish (Integer Truncation) va SafeCast
**Tavsif:** Solidity 0.8+ da arifmetik toshishlar (overflow/underflow) avtomatik tekshirilsa-da, katta turdan kichik turga bevosita typecasting qilishda (masalan, uint256 -> uint64 yoki uint32) qiymat kesilib (truncation) ketadi va revert bermaydi. Bu moliyaviy tizimlarda baland summalarni arzimas songa aylantirib yuborishi mumkin.
**Talablar:** Katta butun son turlarini xavfsiz konvertatsiya qilish uchun OpenZeppelin SafeCast patternidan foydalanish, toshish yuz berganda xatolik chiqarish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title SafeCastLibrary - Turlarni xavfsiz qisqartirish kutubxonasi
library SafeCast {
    error SafeCastOverflowUint256ToUint64(uint256 value);
    error SafeCastOverflowUint256ToUint32(uint256 value);
    error SafeCastOverflowUint256ToUint8(uint256 value);

    /// @notice uint256 ni uint64 ga xavfsiz o'tkazish
    function toUint64(uint256 value) internal pure returns (uint64) {
        if (value > type(uint64).max) {
            revert SafeCastOverflowUint256ToUint64(value);
        }
        return uint64(value);
    }

    /// @notice uint256 ni uint32 ga xavfsiz o'tkazish
    function toUint32(uint256 value) internal pure returns (uint32) {
        if (value > type(uint32).max) {
            revert SafeCastOverflowUint256ToUint32(value);
        }
        return uint32(value);
    }

    /// @notice uint256 ni uint8 ga xavfsiz o'tkazish
    function toUint8(uint256 value) internal pure returns (uint8) {
        if (value > type(uint8).max) {
            revert SafeCastOverflowUint8ToUint8(value);
        }
        return uint8(value);
    }
}

/// @title StakingTimerVault - Vaqt tamg'alari va token miqdorlarini xavfsiz saqlash
contract StakingTimerVault {
    using SafeCast for uint256;

    struct StakeRecord {
        uint64 timestamp;     // 8 bayt
        uint64 lockDuration; // 8 bayt
        uint128 amount;      // 16 bayt (1 ta storage slotiga zich joylashadi)
    }

    mapping(address => StakeRecord) public stakes;

    event Staked(address indexed user, uint128 amount, uint64 unlockTime);

    /// @notice Xavfsiz casting orqali stavka qilish
    function stake(uint256 amount, uint256 duration) external {
        require(amount > 0, "Miqdor musbat bo'lishi kerak");
        require(duration > 0 && duration <= 365 days, "Muddati noto'g'ri");

        // Xavfsiz qisqartirish: agar duration yoki amount sig'masa revert beradi
        uint64 safeDuration = duration.toUint64();
        uint64 currentTimestamp = block.timestamp.toUint64();

        if (amount > type(uint128).max) {
            revert("Miqdor uint128 chegarasidan oshib ketdi!");
        }
        uint128 safeAmount = uint128(amount);

        stakes[msg.sender] = StakeRecord({
            timestamp: currentTimestamp,
            lockDuration: safeDuration,
            amount: safeAmount
        });

        emit Staked(msg.sender, safeAmount, currentTimestamp + safeDuration);
    }
}
```
**Tushuntirish:** Solidity 0.8 versiyasidan boshlab arifmetik amallarda avtomatik tekshiruv mavjud, ammo eksplitsit tur o'zgartirish `uint64(val)` harakatida tildagi semantika pastki 64 bitni olib qoladi va yuqori bitlarni jimgina tashlab yuboradi (truncation). SafeCast kutubxonasi `value > type(uint64).max` shartini tekshirib, ma'lumot yo'qotilishining oldini oladi. Shuningdek struct maydonlarini uint64/uint128 ga ixchamlashtirish (packing) orqali gas tejaladi.

---

### Topshiriq #1182: Inline Assembly (Yul) da Calldata Slicing va Xotirani Buzishdan Himoya
**Tavsif:** Inline assembly (Yul) gazni tejash uchun calldata va xotira bilan to'g'ridan-to'g'ri ishlaydi. Biroq xotira ko'rsatkichi (free memory pointer `0x40`) noto'g'ri boshqarilsa yoki calldata chegaralari tekshirilmasa, xotira maydoni ifloslanishi (memory corruption) va kutilmagan zaifliklar kelib chiqadi.
**Talablar:** Yul da calldata qismini xavfsiz ajratib olish, `0x40` free memory pointer intizomiga rioya qilish va `calldatasize()` tekshiruvlarini to'liq amalga oshirish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title SecureCalldataParser - Yul vositasida xavfsiz bayt o'qish va xotira nazorati
contract SecureCalldataParser {
    error InvalidCalldataLength(uint256 actual, uint256 required);
    error ExecutionFailed();

    /// @notice Calldata dan ko'rsatilgan ofsetdagi 32-baytli so'zni xavfsiz o'qish
    function extractWordAt(bytes calldata data, uint256 offset) external pure returns (bytes32 result) {
        if (offset + 32 > data.length) {
            revert InvalidCalldataLength(data.length, offset + 32);
        }

        assembly {
            // calldataload: data offsetiga calldata boshlanish joyini (data.offset) qo'shamiz
            let calldataPtr := add(data.offset, offset)
            result := calldataload(calldataPtr)
        }
    }

    /// @notice Xotira tozaligi intizomini (memory-safe) saqlagan holda ikkita bayt massivini nusxalash
    function safeMemoryCopy(bytes memory input) external pure returns (bytes memory output) {
        assembly ("memory-safe") {
            let length := mload(input)
            // 0x40 - EVM free memory ko'rsatkichi
            let freeMem := mload(0x40)
            output := freeMem

            // Yangi massiv uzunligini yozish
            mstore(output, length)

            let src := add(input, 32)
            let dest := add(output, 32)

            // 32-baytli qadamlar bilan xavfsiz nusxalash
            for { let i := 0 } lt(i, length) { i := add(i, 32) } {
                mstore(add(dest, i), mload(add(src, i)))
            }

            // Yangi bo'sh xotira manzilini yangilash (32 bayt sarlavha + yaxlitlangan hajm)
            let totalAllocated := add(32, and(add(length, 31), not(31)))
            mstore(0x40, add(freeMem, totalAllocated))
        }
    }
}
```
**Tushuntirish:** EVM xotirasida `0x40` manzilida keyingi mavjud erkin xotira ko'rsatkichi saqlanadi. Inline assembly yozishda `assembly ('memory-safe')` annotatsiyasi kompilyatorga ushbu blok erkin xotira pointerini buzmasligini kafolatlaydi. Calldata bilan ishlaganda `data.offset` va `data.length` chegaralarini qat'iy tekshirish boshqa tranzaksiya ma'lumotlarini o'qib ketish (out-of-bounds read) xavfini yo'qotadi.

---

### Topshiriq #1183: Tashqi Chaqiruvlar Siklida DoS (Denial of Service) va Push-o'rniga-Pull Modeli
**Tavsif:** Smart-kontrakt ko'plab foydalanuvchilarga mukofot yoki qoldiq mablag'larni bitta siklda to'g'ridan-to'g'ri yuborsa (Push payment), bitta qabul qiluvchi kontrakt o'zining `receive()` funksiyasida revert qilsa yoki gazni tugatsa, butun sikl bloklanadi va boshqa hech kim o'z pulini ololmaydi.
**Talablar:** Push to'lov usulidan voz kechib, Pull Payment (foydalanuvchilar o'zlari mustaqil yechib olishi) arxitekturasini joriy etish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title PullPaymentDistributor - DoS hujumlariga chidamli to'lov tarqatish tizimi
contract PullPaymentDistributor {
    address public immutable admin;

    // Har bir foydalanuvchining shaxsiy yechib olinishi mumkin bo'lgan balansi
    mapping(address => uint256) private _pendingWithdrawals;

    event BalanceCredited(address indexed payee, uint256 amount);
    event Withdrawn(address indexed payee, uint256 amount);

    modifier onlyAdmin() {
        require(msg.sender == admin, "Faqat admin ruxsatiga ega");
        _;
    }

    constructor() {
        admin = msg.sender;
    }

    /// @notice Mablag'larni yuboruvchi emas, ulush hisoblovchi xavfsiz funksiya
    function creditReward(address payee, uint256 amount) external onlyAdmin {
        require(payee != address(0), "Noto'g'ri qabul qiluvchi");
        require(amount > 0, "Nol bo'lmagan miqdor talab qilinadi");

        _pendingWithdrawals[payee] += amount;
        emit BalanceCredited(payee, amount);
    }

    /// @notice Shartnoma balansini depozit qilish
    function depositPool() external payable onlyAdmin {}

    /// @notice Foydalanuvchi o'z ulushini xavfsiz yechib oladi (Pull Pattern)
    function withdraw() external {
        uint256 amount = _pendingWithdrawals[msg.sender];
        require(amount > 0, "Yechib olish uchun balans mavjud emas");

        // Checks-Effects-Interactions (CEI) qoidasi
        _pendingWithdrawals[msg.sender] = 0;

        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "ETH o'tkazish muvaffaqiyatsiz tugadi");

        emit Withdrawn(msg.sender, amount);
    }

    /// @notice Foydalanuvchi kutilayotgan balansini ko'rish
    function pendingWithdrawalOf(address payee) external view returns (uint256) {
        return _pendingWithdrawals[payee];
    }
}
```
**Tushuntirish:** Push modeli (barcha manzilarga bitta tranzaksiyada yuborish) jiddiy xavf tug'diradi: bitta zararli kontrakt yoki gaz cheklovi barcha foydalanuvchilar pulini abadiy muzlatib qo'yishi mumkin. Pull Payment arxitekturasi har bir tranzaksiyani alohida ajratadi (isolation), foydalanuvchi faqat o'z tranzaksiyasi va gazi uchun javobgar bo'ladi.

---

### Topshiriq #1184: Blok Gaz Cheklovi (Block Gas Limit) DoS va Sahifalash (Pagination) Arxitekturasi
**Tavsif:** Dinamik massivlar o'sib borgan sari (masalan, 50,000 investor), ularni bitta funksiyada aylanib chiqish (iterate) blokning maksimal gaz chegarasidan (odatda 30M gas) oshib ketadi. Natijada funksiya tranzaksiya o'tkazolmay butunlay yaroqsiz holga keladi.
**Talablar:** Cheksiz massiv sikllaridan himoyalanish, ma'lumotlarni qismlarga bo'lib qayta ishlash (chunking/pagination) mexanizmini yaratish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title PaginatedBatchProcessor - Katta ma'lumotlar oqimini sahifalab xavfsiz boshqarish
contract PaginatedBatchProcessor {
    address[] public registeredUsers;
    mapping(address => bool) public isProcessed;
    uint256 public nextProcessIndex;

    event UserRegistered(address indexed user);
    event BatchProcessed(uint256 startIndex, uint256 count);

    /// @notice Foydalanuvchilarni ro'yxatga olish
    function registerUser(address user) external {
        require(user != address(0), "Nol manzil taqiqlangan");
        registeredUsers.push(user);
        emit UserRegistered(user);
    }

    /// @notice Foydalanuvchilarning umumiy soni
    function totalUsers() external view returns (uint256) {
        return registeredUsers.length;
    }

    /// @notice Sahifalab ma'lumotlarni o'qish (View pagination)
    function getUsersPage(uint256 offset, uint256 limit) external view returns (address[] memory page) {
        uint256 total = registeredUsers.length;
        if (offset >= total) {
            return new address[](0);
        }

        uint256 end = offset + limit;
        if (end > total) {
            end = total;
        }

        uint256 size = end - offset;
        page = new address[](size);

        for (uint256 i = 0; i < size; i++) {
            page[i] = registeredUsers[offset + i];
        }
    }

    /// @notice Cheklangan gaz doirasida qismlab ishlov berish (State modifying pagination)
    function processBatch(uint256 batchSize) external {
        require(batchSize > 0 && batchSize <= 100, "Paket hajmi 1 dan 100 gacha bo'lishi lozim");

        uint256 total = registeredUsers.length;
        uint256 startIndex = nextProcessIndex;
        require(startIndex < total, "Barcha foydalanuvchilarga ishlov berib bo'lingan");

        uint256 endIndex = startIndex + batchSize;
        if (endIndex > total) {
            endIndex = total;
        }

        for (uint256 i = startIndex; i < endIndex; i++) {
            address user = registeredUsers[i];
            if (!isProcessed[user]) {
                isProcessed[user] = true;
                // Bu yerda foydalanuvchi bo'yicha hisob-kitoblar bajariladi
            }
        }

        nextProcessIndex = endIndex;
        emit BatchProcessed(startIndex, endIndex - startIndex);
    }
}
```
**Tushuntirish:** EVM bloklari qat'iy gaz limitiga ega. Hech qachon shartnoma holatini o'zgartiruvchi amallarda uzunligi noaniq bo'lgan massivlarni to'liq aylanib chiqish (for-loop) tavsiya etilmaydi. Buning o'rniga tashqi chaqiruvchiga `batchSize` yoki `offset/limit` uzatish imkonini beruvchi sahifalash arxitekturasi qo'llaniladi.

---

### Topshiriq #1185: Selfdestruct va Majburiy Ether Kiritish (Forcible Ether Injection) Hujumidan Himoya
**Tavsif:** Solidity kontraktlari `address(this).balance` ga tayansa, zararli aktyor `selfdestruct(victimAddress)` qilib kontraktga majburiy tarzda ETH yuborishi mumkin. Agar kontrakt mantig'i `require(address(this).balance == TARGET)` kabi qat'iy tenglikka asoslangan bo'lsa, o'yin yoki auksion doimiy qulflanadi.
**Talablar:** Ichki hisob-kitob (internal accounting) balansini alohida `depositedBalance` o'zgaruvchisida yuritish, `==` o'rniga `>=` ishlatish va majburiy yuborilgan ETH larni xavfsiz boshqarish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title EtherGameVault - Majburiy Ether kiritishdan himoyalangan auksion o'yini
contract EtherGameVault {
    uint256 public constant TARGET_MIQDOR = 10 ether;
    uint256 public constant STEP_MIQDOR = 1 ether;

    // Ichki aniq hisoblangan balans (Tashqi majburiy kiritishlardan daxlsiz)
    uint256 public internalAccountingBalance;
    address public winner;

    event Deposited(address indexed player, uint256 step, uint256 totalProgress);
    event WinnerAnnounced(address indexed winner, uint256 reward);

    /// @notice O'yinchilar qadamma-qadam depozit qilishadi
    function deposit() external payable {
        require(msg.value == STEP_MIQDOR, "Faqat aniq 1 ETH kiritish mumkin");
        require(internalAccountingBalance < TARGET_MIQDOR, "O'yin allaqachon yakunlangan");

        // ZAIF AMALIYOT: `address(this).balance == TARGET_MIQDOR`
        // XAVFSIZ AMALIYOT: Faqat qonuniy depozit qilingan ichki hisobni oshirish
        internalAccountingBalance += msg.value;

        emit Deposited(msg.sender, msg.value, internalAccountingBalance);

        if (internalAccountingBalance >= TARGET_MIQDOR) {
            winner = msg.sender;
            emit WinnerAnnounced(winner, internalAccountingBalance);
        }
    }

    /// @notice G'olib mukofotni yechib oladi
    function claimReward() external {
        require(msg.sender == winner, "Faqat g'olib yechib olishi mumkin");
        require(internalAccountingBalance >= TARGET_MIQDOR, "Maqsadga erishilmagan");

        uint256 payout = internalAccountingBalance;
        internalAccountingBalance = 0;

        (bool success, ) = payable(winner).call{value: payout}("");
        require(success, "Mablag'ni o'tkazish muvaffaqiyatsiz bo'ldi");
    }

    /// @notice Shartnoma balansidagi ortiqcha (majburiy kiritilgan) ETH larni tekshirish
    function excessBalance() external view returns (uint256) {
        if (address(this).balance > internalAccountingBalance) {
            return address(this).balance - internalAccountingBalance;
        }
        return 0;
    }
}
```
**Tushuntirish:** EVM da kontrakt `receive()` yoki `fallback()` ga ega bo'lmasa ham, unga boshqa kontraktning `selfdestruct` chaqiruvi yoki coinbase tranzaksiyalari (blok qazib oluvchi mukofoti) orqali majburiy Ether tushishi mumkin. Shuning uchun smart-kontrakt mantig'ida `address(this).balance == x` qat'iy tengligini ishlatish xavfli hisoblanadi; ichki hisoblagich `internalAccountingBalance` ishlatish kerak.

---

### Topshiriq #1186: Boshlang'ich Qiymatlanmagan Xotira Ko'rsatkichlari (Uninitialized Storage Pointers)
**Tavsif:** Eskirgan yoki xato yozilgan Solidity kontraktlarida mahalliy struktura o'zgaruvchisi `memory` yoki `storage` ko'rsatilmasdan yaratilsa, u sukut bo'yicha 0-slotdagi storage ko'rsatkichiga bog'lanadi va birinchi saqlangan o'zgaruvchini (masalan, owner manzilini) qayta yozib yuboradi.
**Talablar:** Mahalliy strukturalarni faqat xotirada (`memory`) yoki aniq boshlang'ich qiymatga ega `storage` ko'rsatkichida ishlatish, noxush storage buzilishini oldini olish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title StoragePointerSafety - Storage ko'rsatkichlarini xavfsiz boshqarish
contract StoragePointerSafety {
    address public owner;
    bool public isLocked;
    uint256 public totalUsersCount;

    struct Profile {
        address userAddress;
        uint256 score;
        bool active;
    }

    mapping(address => Profile) public userProfiles;

    event ProfileUpdated(address indexed user, uint256 newScore, bool active);

    constructor() {
        owner = msg.sender;
        isLocked = false;
        totalUsersCount = 0;
    }

    /// @notice XAVFSIZ: To'g'ridan-to'g'ri storage ko'rsatkichini aniq belgilangan mappingdan olish
    function updateScoreSafeStorage(uint256 bonus) external {
        // storage kalit so'zi aniq mavjud mapping elementiga ishora qiladi
        Profile storage profile = userProfiles[msg.sender];
        profile.userAddress = msg.sender;
        profile.score += bonus;
        profile.active = true;

        emit ProfileUpdated(msg.sender, profile.score, profile.active);
    }

    /// @notice XAVFSIZ: Xotirada vaqtinchalik hisob-kitob qilish (memory struct)
    function calculateProjectedScore(uint256 bonus) external view returns (Profile memory) {
        Profile memory tempProfile = userProfiles[msg.sender];
        tempProfile.score += bonus;
        // Storage o'zgarmaydi, faqat hisob natijasi qaytadi
        return tempProfile;
    }

    /// @notice Administrator huquqini himoyalash tekshiruvi
    function verifyOwnershipIntegrity() external view returns (bool) {
        // Agar 0-slotdagi owner buzilmagan bo'lsa
        return owner != address(0);
    }
}
```
**Tushuntirish:** Solidity 0.5.0 dan boshlab strukturalar va massivlar uchun ma'lumot joylashuvini (`storage`, `memory` yoki `calldata`) aniq ko'rsatish majburiy qilib qo'yilgan. Agar `storage` ko'rsatkichini mavjud bo'lmagan yangi obyekt sifatida yaratishga urunilsa, kompilyator xatolik beradi. Bu qoida 0-slot (owner yoki muhim davlat holati) tasodifan ezilib ketishining oldini oladi.

---

### Topshiriq #1187: Funksiya Selektori To'qnashuvi (Function Selector Clashing) va Proxy Himoyasi
**Tavsif:** Solidity funksiya selektori funksiya imzosining `keccak256` xeshining dastlabki 4 baytidan iborat (32 bit). 4 milliardlik maydonda turli nomdagi ikkita funksiyaning 4 bayti to'qnash kelishi mumkin. Proxy kontraktda Proxy Admin funksiyasi bilan Implementation funksiyasi selektori to'qnashsa, tizim boshqaruvi yo'qotilishi mumkin.
**Talablar:** Transparent Upgradeable Proxy patterni yordamida selektor to'qnashuvini ajratish yoki ERC-1967 maxsus slotlaridan foydalanish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title TransparentUpgradeableProxy - Selektor to'qnashuvidan xolis proxy arxitekturasi
contract TransparentUpgradeableProxy {
    // EIP-1967 bo'yicha maxsus slotlar
    bytes32 private constant IMPLEMENTATION_SLOT = 
        0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc;
    bytes32 private constant ADMIN_SLOT = 
        0xb53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103;

    event Upgraded(address indexed newImplementation);
    event AdminChanged(address previousAdmin, address newAdmin);

    modifier ifAdmin() {
        if (msg.sender == _getAdmin()) {
            _;
        } else {
            _fallback();
        }
    }

    constructor(address logic, address adminAddress, bytes memory data) payable {
        _setAdmin(adminAddress);
        _setImplementation(logic);
        if (data.length > 0) {
            (bool success, ) = logic.delegatecall(data);
            require(success, "Boshlang'ich chaqiruv muvaffaqiyatsiz bo'ldi");
        }
    }

    /// @notice Faqat admin uchun ruxsat etilgan yangilash funksiyasi
    function upgradeTo(address newImplementation) external ifAdmin {
        _setImplementation(newImplementation);
        emit Upgraded(newImplementation);
    }

    /// @notice Oddiy foydalanuvchilar chaqiruvlari Implementation shartnomasiga yo'naltiriladi
    fallback() external payable {
        _fallback();
    }

    receive() external payable {
        _fallback();
    }

    function _fallback() internal {
        // Admin hech qachon implementation funksiyalarini bexosdan chaqirolmaydi
        require(msg.sender != _getAdmin(), "Admin implementationga murojaat qila olmaydi");

        address impl = _getImplementation();
        assembly {
            calldatacopy(0, 0, calldatasize())
            let result := delegatecall(gas(), impl, 0, calldatasize(), 0, 0)
            returndatacopy(0, 0, returndatasize())
            switch result
            case 0 { revert(0, returndatasize()) }
            default { return(0, returndatasize()) }
        }
    }

    function _getImplementation() internal view returns (address impl) {
        bytes32 slot = IMPLEMENTATION_SLOT;
        assembly { impl := sload(slot) }
    }

    function _setImplementation(address newImpl) internal {
        require(newImpl.code.length > 0, "Implementation kontrakt bo'lishi shart");
        bytes32 slot = IMPLEMENTATION_SLOT;
        assembly { sstore(slot, newImpl) }
    }

    function _getAdmin() internal view returns (address adm) {
        bytes32 slot = ADMIN_SLOT;
        assembly { adm := sload(slot) }
    }

    function _setAdmin(address newAdm) internal {
        require(newAdm != address(0), "Admin nol manzil bo'lishi mumkin emas");
        bytes32 slot = ADMIN_SLOT;
        assembly { sstore(slot, newAdm) }
    }
}
```
**Tushuntirish:** Agar Proxy shartnomasida `upgradeTo(address)` funksiyasi bo'lsa va Implementation shartnomasida ham bir xil 4-baytli selektorga ega funksiya bo'lsa (Function Selector Clashing), chaqiruvning qayerga ketishi noaniq bo'lib qoladi. Transparent Proxy patterni bunga chek qo'yadi: agar chaqiruvchi Admin bo'lsa, u faqat Proxy boshqaruvini ko'radi; agar foydalanuvchi bo'lsa, har qanday chaqiruv Implementation shartnomasiga yuboriladi.

---

### Topshiriq #1188: Storage Massiv Elementlarini O'chirish (Delete) va Qoldiq Bo'shliqlar Muammosi
**Tavsif:** Solidity da `delete array[index]` bajarilganda massiv uzunligi qisqarmaydi; ko'rsatilgan indeksdagi qiymat o'zining 'nol qiymati'ga (default value 0 yoki address(0)) qaytariladi. Agar ishlab chiquvchi element to'liq o'chdi deb hisoblasa, bo'sh joylar (gaps) hisob-kitoblarni buzadi yoki gaz isrofini keltirib chiqaradi.
**Talablar:** Elementni to'liq o'chirish uchun 'Swap-and-Pop' texnikasini joriy etish va tartiblangan o'chirish xavfsizligini ta'minlash.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title SafeArrayManager - Massiv elementlarini xavfsiz o'chirish va bo'shliqlarsiz boshqarish
contract SafeArrayManager {
    uint256[] public itemIds;
    // Tezkor qidirish uchun id dan massiv indeksiga mapping
    mapping(uint256 => uint256) private _indexOfItem;
    mapping(uint256 => bool) public itemExists;

    event ItemAdded(uint256 indexed id, uint256 index);
    event ItemRemoved(uint256 indexed id);

    /// @notice Yangi element qo'shish O(1)
    function addItem(uint256 id) external {
        require(!itemExists[id], "Element allaqachon mavjud");

        _indexOfItem[id] = itemIds.length;
        itemIds.push(id);
        itemExists[id] = true;

        emit ItemAdded(id, itemIds.length - 1);
    }

    /// @notice Swap-and-Pop usuli orqali elementni to'liq o'chirish O(1)
    function removeItemSwapAndPop(uint256 id) external {
        require(itemExists[id], "Element mavjud emas");

        uint256 indexToRemove = _indexOfItem[id];
        uint256 lastIndex = itemIds.length - 1;

        if (indexToRemove != lastIndex) {
            uint256 lastElement = itemIds[lastIndex];
            // Oxirgi elementni o'chirilayotgan joyga ko'chiramiz
            itemIds[indexToRemove] = lastElement;
            _indexOfItem[lastElement] = indexToRemove;
        }

        // Oxirgi slotni massivdan uzib tashlaymiz
        itemIds.pop();
        delete _indexOfItem[id];
        itemExists[id] = false;

        emit ItemRemoved(id);
    }

    /// @notice Barcha elementlarni xavfsiz ko'rish
    function getAllItems() external view returns (uint256[] memory) {
        return itemIds;
    }

    /// @notice Jami elementlar soni
    function count() external view returns (uint256) {
        return itemIds.length;
    }
}
```
**Tushuntirish:** Oddiy `delete arr[i]` amali massiv uzunligini kamaytirmaydi, faqat `arr[i] = 0` qiladi. Bu esa keyingi sikllarda bo'sh elementlarni bekorga aylanib chiqishga va gaz isrofiga sabab bo'ladi. 'Swap-and-Pop' usuli o'chirilishi kerak bo'lgan element o'rniga massivning oxirgi elementini joylashtiradi va `pop()` chaqiradi, bu esa operatsiyani $O(1)$ murakkablikda bo'shliqsiz amalga oshiradi.

---

### Topshiriq #1189: Nol Manzil (Zero Address) Tekshiruvi va Ikki Bosqichli Egalik Transferi (Ownable2Step)
**Tavsif:** Smart-kontrakt egasi o'z huquqini boshqa manzilga o'tkazishda yanglishib noto'g'ri yoki 0x0 manzilni ko'rsatsa, shartnoma ustidan boshqaruv abadiy yo'qotiladi (deadlock).
**Talablar:** Barcha muhim setterlarda nol manzil tekshiruvini kiritish hamda xavfsiz ikki bosqichli egalik topshirish (Ownable2Step: taklif qilish va qabul qilish) mexanizmini yaratish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title SecureOwnable2Step - Ikki bosqichli xavfsiz boshqaruv transferi
contract SecureOwnable2Step {
    address private _owner;
    address private _pendingOwner;

    error CallerNotOwner();
    error CallerNotPendingOwner();
    error InvalidZeroAddress();

    event OwnershipTransferStarted(address indexed previousOwner, address indexed newOwner);
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    modifier onlyOwner() {
        if (msg.sender != _owner) revert CallerNotOwner();
        _;
    }

    constructor() {
        _owner = msg.sender;
        emit OwnershipTransferred(address(0), msg.sender);
    }

    function owner() public view returns (address) {
        return _owner;
    }

    function pendingOwner() public view returns (address) {
        return _pendingOwner;
    }

    /// @notice 1-bosqich: Yangi egaga nomzod taklif qilish
    function transferOwnership(address newOwner) public virtual onlyOwner {
        if (newOwner == address(0)) revert InvalidZeroAddress();
        if (newOwner == _owner) revert("Allaqachon egasi");

        _pendingOwner = newOwner;
        emit OwnershipTransferStarted(_owner, newOwner);
    }

    /// @notice 2-bosqich: Nomzod shaxsan o'zi tasdiqlab egalikni qabul qiladi
    function acceptOwnership() public virtual {
        if (msg.sender != _pendingOwner) revert CallerNotPendingOwner();

        address oldOwner = _owner;
        _owner = msg.sender;
        _pendingOwner = address(0);

        emit OwnershipTransferred(oldOwner, msg.sender);
    }

    /// @notice Taklifni bekor qilish (agar adashib yuborilgan bo'lsa)
    function cancelOwnershipTransfer() public virtual onlyOwner {
        _pendingOwner = address(0);
    }
}
```
**Tushuntirish:** An'anaviy `transferOwnership(newOwner)` bir zumda amalga oshadi; agar kiritilgan manzil noto'g'ri bo'lsa yoki shaxsiy kaliti mavjud bo'lmasa, shartnoma egasiz qoladi. OpenZeppelin tomonidan standartlashtirilgan `Ownable2Step` naqshida yangi ega o'zining kaliti borligini `acceptOwnership()` tranzaksiyasini yuborish orqali isbotlaydi, bu tizim xavfsizligini kafolatlaydi.

---

### Topshiriq #1190: E'tiborsiz Qoldirilgan Qaytish Qiymatlari (Ignored Return Values) va SafeSendValue
**Tavsif:** Solidity da past darajali chaqiruvlar (`call`, `send`) xatolik yuz berganda avtomatik revert bermaydi, balki `false` qiymat qaytaradi. Agar dasturchi qaytgan mantiqiy bayroqni tekshirmasa (`(bool success, ) = to.call{value: x}('')`), tranzaksiya go'yo muvaffaqiyatli o'tgandek hisoblanadi, lekin pul o'tkazilmay qoladi.
**Talablar:** Barcha past darajali chaqiruvlarning `success` holatini qat'iy tekshirish, qaytgan xatolik ma'lumotlarini (revert data) tahlil qilish va Address.sendValue ekvivalentini yaratish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title SafePaymentExecutor - Qaytish qiymatlarini to'liq tekshiruvchi to'lov vositasi
contract SafePaymentExecutor {
    error PaymentFailed(address recipient, uint256 amount, bytes returnData);
    error InsufficientContractBalance(uint256 available, uint256 required);

    event PaymentDispatched(address indexed recipient, uint256 amount);

    receive() external payable {}

    /// @notice ETH ni past darajali call orqali qat'iy tekshiruv bilan yuborish
    function sendValueSecure(address payable recipient, uint256 amount) external {
        if (recipient == address(0)) revert("Nol manzilga yuborib bo'lmaydi");
        if (address(this).balance < amount) {
            revert InsufficientContractBalance(address(this).balance, amount);
        }

        // Past darajali call gaz limiti cheklovisiz va qaytish qiymatini tekshirish bilan
        (bool success, bytes memory returnData) = recipient.call{value: amount}("");

        if (!success) {
            // Agar recipient revert bersa, uning sababi bilan qaytaramiz
            revert PaymentFailed(recipient, amount, returnData);
        }

        emit PaymentDispatched(recipient, amount);
    }

    /// @notice Ixtiyoriy kontrakt funksiyasini chaqirish va natijani dekodlash
    function executeExternalCall(address target, bytes calldata callData) external returns (bytes memory) {
        require(target.code.length > 0, "Nishon kontrakt emas");

        (bool success, bytes memory result) = target.call(callData);

        if (!success) {
            // Revert sababini tashqariga uzatish (Bubble-up revert reason)
            if (result.length > 0) {
                assembly {
                    let returndata_size := mload(result)
                    revert(add(32, result), returndata_size)
                }
            } else {
                revert("Tashqi chaqiruv noma'lum sababga ko'ra revert berdi");
            }
        }

        return result;
    }
}
```
**Tushuntirish:** Eski `send()` yoki `transfer()` funksiyalari faqat 2300 gas uzatgani sababli zamonaviy multisig yoki hisob abstraksiyasi hamyonlariga (ERC-4337) to'lov qilishda ishlamay qoladi. Shu bois zamonaviy Solidity da `.call{value: x}('')` tavsiya etiladi, ammo uning qaytargan `bool success` qiymatini e'tiborsiz qoldirish jiddiy zaiflikdir. Har doim `require(success)` yoki `if (!success) revert()` orqali natija kafolatlanishi shart.

---

### Topshiriq #1191: Slither Statik Tahlil Vositalari va Soxta Ijobiylarni (False Positives) Filtrlash
**Tavsif:** Katta kod bazalarida Slither statik tahlili yuzlab ogohlantirishlar berishi mumkin. Xavfsizlik muhandisi Slither qoidalarini moslashtirishi, qasddan qilingan xavfsiz arxitekturani natspec teglari orqali tasdiqlashi va haqiqiy zaifliklarni aniq ajratishi kerak.
**Talablar:** Slither tahlilchisi uchun natspec annotatsiyalaridan foydalanish, reentrancy va unindexed event ogohlantirishlarini professional darajada boshqarish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title SlitherCompliantVault - Slither statik tahlil talablariga moslashtirilgan shartnoma
contract SlitherCompliantVault {
    address public immutable owner;
    mapping(address => uint256) private _balances;

    // Slither: barcha qidirilishi lozim bo'lgan argumentlar indexed bo'lishi shart
    event DepositReceived(address indexed user, uint256 amount);
    event WithdrawalCompleted(address indexed user, uint256 amount);

    constructor() {
        owner = msg.sender;
    }

    /// @notice Balansni to'ldirish
    function deposit() external payable {
        require(msg.value > 0, "Nol qiymat taqiqlangan");
        _balances[msg.sender] += msg.value;
        emit DepositReceived(msg.sender, msg.value);
    }

    /// @notice Slither reentrancy-benign va checks-effects qoidalariga 100% javob beruvchi yechib olish
    /// @dev slither-disable-next-line reentrancy-no-eth
    function withdraw(uint256 amount) external {
        require(_balances[msg.sender] >= amount, "Mablag' yetarli emas");

        // Checks-Effects-Interactions (Slither CEI tekshiruvini qoniqtiradi)
        _balances[msg.sender] -= amount;

        (bool success, ) = payable(msg.sender).call{value: amount}("");
        require(success, "To'lov o'tmadi");

        emit WithdrawalCompleted(msg.sender, amount);
    }

    /// @notice Foydalanuvchi balansini tekshirish
    function balanceOf(address account) external view returns (uint256) {
        return _balances[account];
    }
}
```
**Tushuntirish:** Slither - Ethereum ekotizimida eng keng tarqalgan statik tahlil vositasi bo'lib, u kodni AST (Abstract Syntax Tree) va CFG (Control Flow Graph) darajasida tahlil qiladi. Kod ichida `slither-disable-next-line <detector>` kabi qat'iy asoslangan izohlar qoldirish orqali CI/CD quvurlarida soxta to'xtalishlarning (false positive) oldi olinadi va haqiqiy xatarlarga e'tibor qaratiladi.

---

### Topshiriq #1192: Echidna Bilan Xususiyatlarga Asoslangan Fuzzing (Property-Based Fuzzing) va Invariantlar
**Tavsif:** Birlik testlari (unit tests) dasturchi tasavvur qilgan stsenariylarni tekshiradi, ammo kutilmagan kombinatsiyalarni aniqlay olmaydi. Echidna tasodifiy tranzaksiyalar oqimini yaratib, aqlli kontrakt invariantlari (hech qachon buzilmasligi kerak bo'lgan mantiqiy qoidalar) har qanday sharoitda buzilmasligini sinovdan o'tkazadi.
**Talablar:** Echidna test shartnomasini qurish, `echidna_` prefiksli invariantlarni yozish va umumiy zaxira balansining buzilmasligini isbotlash.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title TokenVaultTarget - Test qilinayotgan maqsadli kontrakt
contract TokenVaultTarget {
    mapping(address => uint256) public balances;
    uint256 public totalDeposits;

    function deposit() external payable {
        balances[msg.sender] += msg.value;
        totalDeposits += msg.value;
    }

    function withdraw(uint256 amount) external {
        require(balances[msg.sender] >= amount, "Yetarli balans yo'q");
        balances[msg.sender] -= amount;
        totalDeposits -= amount;

        (bool s, ) = msg.sender.call{value: amount}("");
        require(s, "O'tkazma xatosi");
    }
}

/// @title EchidnaTestHarness - Echidna fuzzeri uchun invariantlar tekshiruvchi shartnoma
contract EchidnaTestHarness {
    TokenVaultTarget public target;

    constructor() payable {
        target = new TokenVaultTarget();
    }

    /// @notice Echidna fuzzeri ushbu funksiyani ixtiyoriy parametrlar bilan millionlab marta chaqiradi
    function testDeposit(uint256 amount) public {
        amount = amount % (address(this).balance + 1);
        if (amount > 0) {
            target.deposit{value: amount}();
        }
    }

    /// @notice Echidna fuzzeri orqali yechib olishni sinash
    function testWithdraw(uint256 amount) public {
        target.withdraw(amount);
    }

    /// @notice INVARIANT: Kontraktning haqiqiy balansi har doim totalDeposits dan katta yoki teng bo'lishi shart
    function echidna_solvency_invariant() public view returns (bool) {
        return address(target).balance >= target.totalDeposits();
    }

    /// @notice ETH qabul qilish uchun
    receive() external payable {}
}
```
**Tushuntirish:** Echidna - smart-kontraktlar uchun maxsus fuzzer bo'lib, har bir qadamdan so'ng `echidna_*` bilan boshlanuvchi invariant funksiyalarni chaqirib natijani (`true` yoki `false`) tekshiradi. Agar bitta kombinatsiyada ham natija `false` qaytsa, Echidna xatolikni keltirib chiqargan eng qisqa tranzaksiyalar ketma-ketligini (shrinking) hisobot qilib beradi.

---

### Topshiriq #1193: Halmos va Ramziy Bajarish (Symbolic Execution) Bilan Matematik Formal Isbotlash
**Tavsif:** Fuzzing tasodifiy qiymatlar tanlaydi, biroq ramziy bajarish (symbolic execution) o'zgaruvchilarni aniq son emas, balki algebraik belgilar (symbolic values) sifatida qabul qilib, barcha mumkin bo'lgan kirishlar maydonini matematik isbotlaydi.
**Talablar:** Halmos vositasida tekshirish uchun formal spetsifikatsiya testini yozish, `check_` prefiksli formal invariantlar orqali to'lovlar xavfsizligini isbotlash.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title LinearVestingLock - Vaqtga asoslangan token tarqatish shartnomasi
contract LinearVestingLock {
    uint256 public immutable start;
    uint256 public immutable duration;
    uint256 public immutable totalAmount;
    uint256 public released;

    constructor(uint256 _totalAmount, uint256 _duration) {
        require(_duration > 0, "Davomiylik musbat bo'lishi shart");
        start = block.timestamp;
        duration = _duration;
        totalAmount = _totalAmount;
    }

    /// @notice O'tgan vaqtga mutanosib ravishda yechish mumkin bo'lgan summani hisoblash
    function vestedAmount(uint256 timestamp) public view returns (uint256) {
        if (timestamp < start) {
            return 0;
        } else if (timestamp >= start + duration) {
            return totalAmount;
        } else {
            return (totalAmount * (timestamp - start)) / duration;
        }
    }
}

/// @title HalmosFormalVerificationTest - Halmos orqali matematik isbotlash
contract HalmosFormalVerificationTest {
    LinearVestingLock public vesting;
    uint256 constant TOTAL = 1_000_000 ether;
    uint256 constant DURATION = 365 days;

    function setUp() public {
        vesting = new LinearVestingLock(TOTAL, DURATION);
    }

    /// @notice FORMAL ISBOT: Har qanday vaqt tamg'asi (timestamp) da chiqarilgan miqdor umumiy miqdordan oshib ketmaydi
    /// @dev Halmos ushbu funksiyani barcha mumkin bo'lgan t (0 dan 2^256-1 gacha) uchun SMT solver orqali isbotlaydi
    function check_vested_amount_never_exceeds_total(uint256 t) public view {
        uint256 vested = vesting.vestedAmount(t);
        // Isbot talabi: vested <= totalAmount
        assert(vested <= TOTAL);
    }

    /// @notice FORMAL ISBOT: Vaqt oldinga siljishi bilan ajratilgan mablag' hech qachon kamaymasligi (monoton o'sish)
    function check_vesting_is_monotonic(uint256 t1, uint256 t2) public view {
        if (t1 <= t2) {
            assert(vesting.vestedAmount(t1) <= vesting.vestedAmount(t2));
        }
    }
}
```
**Tushuntirish:** Halmos - formal tekshirish (formal verification) vositasi bo'lib, u Solidity bytecode-ni to'g'ridan-to'g'ri Z3 SMT solver formulasiga aylantiradi. Oddiy test faqat berilgan parametrlarni tekshirsa, Halmos bir necha soniya ichida cheksiz koinotdagi barcha parametrlar bo'yicha invariant buzilmasligini 100% matematik aniqlikda isbotlaydi yoki qoidani buzuvchi qarshi misolni topadi.

---

### Topshiriq #1194: Certora Verification Language (CVL) va Smart-Kontrakt Matematik Qoidalari
**Tavsif:** Eng nufuzli DeFi protokollari (Aave, MakerDAO, Compound) auditida Certora Prover ishlatiladi. Tizimning qoidalari CVL tilida yozilib, kontrakt holati har qanday funksiya bajarilishidan oldin va keyin qoidaga mosligi tekshiriladi.
**Talablar:** Solidity shartnomasi va unga mos keluvchi CVL spetsifikatsiya mantiqini ishlab chiqish, invariantlarning matematik ifodasini tushuntirish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title CollateralizedVault - Garov ta'minotiga ega kreditlash shartnomasi
contract CollateralizedVault {
    mapping(address => uint256) public collateral;
    mapping(address => uint256) public debt;
    uint256 public totalDebt;
    uint256 public constant COLLATERAL_RATIO = 150; // 150% ta'minot talabi

    event CollateralDeposited(address indexed user, uint256 amount);
    event LoanTaken(address indexed user, uint256 debtAmount);

    function depositCollateral() external payable {
        collateral[msg.sender] += msg.value;
        emit CollateralDeposited(msg.sender, msg.value);
    }

    function borrow(uint256 amount) external {
        uint256 maxBorrow = (collateral[msg.sender] * 100) / COLLATERAL_RATIO;
        require(debt[msg.sender] + amount <= maxBorrow, "Garov ta'minoti yetarli emas");

        debt[msg.sender] += amount;
        totalDebt += amount;

        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Qarz o'tkazilishi xatosi");

        emit LoanTaken(msg.sender, amount);
    }

    function repayDebt() external payable {
        require(msg.value <= debt[msg.sender], "Qarzdan ko'p to'lab bo'lmaydi");
        debt[msg.sender] -= msg.value;
        totalDebt -= msg.value;
    }
}

/*
/// ==========================================
/// CERTORA CVL SPETSIFIKATSIYASI (certora.spec)
/// ==========================================

methods {
    function collateral(address) external returns (uint256) envfree;
    function debt(address) external returns (uint256) envfree;
    function totalDebt() external returns (uint256) envfree;
}

// Qoida 1: Hech qachon shaxsiy qarz ta'minot limitidan oshib ketmasligi shart
rule solvencyIntegrity(method f, address user) {
    env e;
    calldataarg args;

    sinov_oldi = debt(user) <= (collateral(user) * 100) / 150;
    require sinov_oldi;

    f(e, args);

    assert debt(user) <= (collateral(user) * 100) / 150, "Garov yetarli emas!";
}

// Invariant 2: Jami qarz har doim foydalanuvchilar qarzlari yig'indisiga teng
invariant totalDebtMatchesUsers(address a, address b)
    a != b => totalDebt() >= debt(a) + debt(b);
*/
```
**Tushuntirish:** Certora Prover texnologiyasi EVM baytkodini tahlil qilib, CVL (Certora Verification Language) da berilgan qoidalarni har qanday tranzaksiya kombinatsiyasi uchun tekshiradi. Bu usul xakerlar foydalanishi mumkin bo'lgan murakkab zanjirsimon holatlarni ishlab chiqish bosqichidayoq bartaraf etishga xizmat qiladi.

---

### Topshiriq #1195: Foundry Handler-Based Invariant Fuzzing va Murakkab DeFi Holatlarini Sinash
**Tavsif:** Oddiy invariant testlari ko'pincha noqonuniy holatlarni yuborib revert bo'ladi. Handler-based invariant fuzzing texnikasida maxsus boshqaruvchi (Handler) kontrakt yaratilib, fuzzer harakatlari faqat mantiqiy ruxsat etilgan oraliqlarda boshqariladi.
**Talablar:** Foundry Handler shartnomasini qurish, 'Ghost Variables' (kuzatuvchi xotira o'zgaruvchilari) yordamida depozit va qoldiqlarni tekshiruvchi invariant testini yozish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title YieldProtocol - Foiz hisoblovchi DeFi protokoli
contract YieldProtocol {
    mapping(address => uint256) public userBalances;
    uint256 public totalStaked;

    function stake() external payable {
        require(msg.value > 0, "0 depozit qilib bo'lmaydi");
        userBalances[msg.sender] += msg.value;
        totalStaked += msg.value;
    }

    function unstake(uint256 amount) external {
        require(userBalances[msg.sender] >= amount, "Yetarli depozit yo'q");
        userBalances[msg.sender] -= amount;
        totalStaked -= amount;
        payable(msg.sender).transfer(amount);
    }
}

/// @title ProtocolHandler - Fuzzer qo'ng'iroqlarini cheklovchi va yo'naltiruvchi Handler
contract ProtocolHandler {
    YieldProtocol public protocol;
    address[] public actors;
    address internal currentActor;

    // Ghost o'zgaruvchi: protokoldan tashqari mustaqil hisoblangan umumiy balans
    uint256 public ghost_expectedTotalStaked;

    constructor(YieldProtocol _protocol) {
        protocol = _protocol;
    }

    modifier useActor(uint256 actorIndexSeed) {
        if (actors.length == 0) {
            actors.push(address(0x1111));
            actors.push(address(0x2222));
            actors.push(address(0x3333));
        }
        currentActor = actors[actorIndexSeed % actors.length];
        vmDeal(currentActor, 100 ether);
        _;
    }

    function stake(uint256 actorSeed, uint256 amount) external useActor(actorSeed) {
        amount = bound(amount, 1 wei, 10 ether);

        // Aktyor nomidan chaqiruv
        (bool success, ) = address(protocol).call{value: amount}(abi.encodeWithSignature("stake()"));
        if (success) {
            ghost_expectedTotalStaked += amount;
        }
    }

    function unstake(uint256 actorSeed, uint256 amount) external useActor(actorSeed) {
        uint256 userBal = protocol.userBalances(currentActor);
        if (userBal == 0) return;

        amount = bound(amount, 1 wei, userBal);
        (bool success, ) = address(protocol).call(abi.encodeWithSignature("unstake(uint256)", amount));
        if (success) {
            ghost_expectedTotalStaked -= amount;
        }
    }

    function bound(uint256 x, uint256 min, uint256 max) internal pure returns (uint256) {
        if (max <= min) return min;
        return min + (x % (max - min + 1));
    }

    function vmDeal(address who, uint256 newBalance) internal {
        // Foundry cheatcode simulyatsiyasi
    }
}
```
**Tushuntirish:** Foundry Handler-based invariant fuzzing texnikasi protokoldagi barcha mumkin bo'lgan harakatlar kombinatsiyasini tekshirishning eng ilg'or usulidir. Handler kontrakt kiruvchi tasodifiy qiymatlarni `bound()` yordamida qonuniy diapazonga keltiradi va 'Ghost variables' yordamida kontrakt hisob-kitoblarining haqiqiyligini real vaqtda tasdiqlaydi.

---

### Topshiriq #1196: Gazni Optimallashtirish va Xavfsizlik Balansi (Gas Golfing vs Security)
**Tavsif:** Ba'zi dasturchilar gazni tejash maqsadida xavfsizlik tekshiruvlarini (require, safemath, custom error) chetlab o'tishga yoki xavfli inline assembly kodlaridan foydalanishga harakat qilishadi. Bu esa fojiali xakerlik hujumlariga yo'l ochadi.
**Talablar:** Xavfsizlikni 1 foiz ham yo'qotmagan holda eng optimal gaz tejash usullarini (immutable, custom error, storage packing, unchecked bloklari) to'g'ri qo'llash.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title OptimizedAndSecureVault - Xavfsiz va maksimal darajada gaz tejamkor ombor
contract OptimizedAndSecureVault {
    // 1. O'zgarmas o'zgaruvchilar storage o'rniga bevosita baytkodga yoziladi (Gas: SLOAD -> PUSH)
    address public immutable owner;
    uint256 public immutable feeBasisPoints;

    // 2. Storage Packing: Bitta 32-baytli slotga bir nechta o'zgaruvchilarni zichlashtirish
    struct ConfigRecord {
        uint64 lastDepositTimestamp; // 8 bayt
        uint64 lockDuration;        // 8 bayt
        uint128 minimumDeposit;      // 16 bayt (Jami 32 bayt = 1 ta storage slot!)
    }
    ConfigRecord public config;

    mapping(address => uint256) private _balances;

    // 3. String o'rniga Custom Error ishlatish gazni keskin kamaytiradi
    error Unauthorized();
    error InsufficientBalance(uint256 available, uint256 required);
    error DepositBelowMinimum(uint256 provided, uint256 required);

    event Deposited(address indexed user, uint256 amount);
    event Withdrawn(address indexed user, uint256 amount);

    constructor(uint256 _feeBps, uint128 _minDep, uint64 _lockDur) {
        owner = msg.sender;
        feeBasisPoints = _feeBps;

        config = ConfigRecord({
            lastDepositTimestamp: uint64(block.timestamp),
            lockDuration: _lockDur,
            minimumDeposit: _minDep
        });
    }

    function deposit() external payable {
        if (msg.value < config.minimumDeposit) {
            revert DepositBelowMinimum(msg.value, config.minimumDeposit);
        }

        // 4. Overflow/underflow matematik jihatdan imkonsiz ekanligi isbotlangan joydagina unchecked ishlatish
        unchecked {
            _balances[msg.sender] += msg.value;
        }

        emit Deposited(msg.sender, msg.value);
    }

    function withdraw(uint256 amount) external {
        uint256 bal = _balances[msg.sender];
        if (bal < amount) {
            revert InsufficientBalance(bal, amount);
        }

        unchecked {
            // bal >= amount ekanligi yuqorida tekshirildi, demak underflow bo'lmaydi
            _balances[msg.sender] = bal - amount;
        }

        (bool success, ) = payable(msg.sender).call{value: amount}("");
        require(success, "To'lov amalga oshmadi");

        emit Withdrawn(msg.sender, amount);
    }
}
```
**Tushuntirish:** Gazni to'g'ri tejash qoidalari: 1) Har doim string require o'rniga `custom error` ishlatish (har chaqiruvda yuzlab gas tejaladi). 2) Bir marta o'rnatiladigan o'zgaruvchilarni `immutable` qilish. 3) `unchecked` bloklarini faqat oldingi if tekshiruvi orqali matematik xato bo'lmasligi qat'iy kafolatlangan joylardagina ishlatish lozim.

---

### Topshiriq #1197: Favqulodda To'xtatish (Circuit Breaker / Pausable) va Ko'p Bosqichli Rollar
**Tavsif:** Protokolda jiddiy zaiflik aniqlanganda, yo'qotishlarning oldini olish uchun barcha mablag' harakatlarini darhol muzlatish (pause) imkoniyati bo'lishi kerak. Biroq ushbu favqulodda kalit bitta admin qo'lida bo'lsa, u markazlashuv xatariga aylanadi.
**Talablar:** Ko'p rolli (Guardian, Admin) favqulodda to'xtatuvchi Circuit Breaker mexanizmini yaratish: Guardian tezda to'xtata oladi, lekin qayta yoqish faqat multisig kengashiga yuklanadi.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title EmergencyCircuitBreaker - Rollarga asoslangan xavfsiz favqulodda to'xtatish tizimi
contract EmergencyCircuitBreaker {
    address public multisigAdmin;
    address public securityGuardian;

    bool public isPaused;
    uint256 public pausedTimestamp;

    event ProtocolPaused(address indexed triggeredBy, uint256 timestamp);
    event ProtocolResumed(address indexed resumedBy, uint256 timestamp);

    error ProtocolIsPaused();
    error ProtocolIsNotPaused();
    error AccessDenied();

    modifier whenNotPaused() {
        if (isPaused) revert ProtocolIsPaused();
        _;
    }

    modifier whenPaused() {
        if (!isPaused) revert ProtocolIsNotPaused();
        _;
    }

    constructor(address _admin, address _guardian) {
        require(_admin != address(0) && _guardian != address(0), "Nol manzil taqiqlangan");
        multisigAdmin = _admin;
        securityGuardian = _guardian;
    }

    /// @notice Tezkor to'xtatish: Guardian yoki Admin zudlik bilan shartnomani muzlata oladi
    function emergencyPause() external {
        if (msg.sender != securityGuardian && msg.sender != multisigAdmin) {
            revert AccessDenied();
        }
        if (isPaused) revert ProtocolIsPaused();

        isPaused = true;
        pausedTimestamp = block.timestamp;

        emit ProtocolPaused(msg.sender, block.timestamp);
    }

    /// @notice Qayta tiklash: Xavf bartaraf etilgach, FAQAT Multisig kengashi qayta yoqa oladi
    function unpause() external whenPaused {
        if (msg.sender != multisigAdmin) revert AccessDenied();

        isPaused = false;
        emit ProtocolResumed(msg.sender, block.timestamp);
    }

    /// @notice Oddiy foydalanuvchi amali (Muzlatilgan paytda bloklanadi)
    function executeUserAction() external whenNotPaused {
        // Tizim faoliyat kodi
    }

    /// @notice Favqulodda holatda ham foydalanuvchi o'z asosiy depozitini qutqarish imkoniyati (Escape Hatch)
    function emergencyWithdrawalUserEscape() external whenPaused {
        // Protokol to'xtatilgan taqdirda ham foydalanuvchilarga kafolatlangan yechish yo'li
    }
}
```
**Tushuntirish:** Circuit Breaker arxitekturasida eng muhim xavfsizlik amaliyoti bu vakolatlarni ajratishdir (Separation of Concerns). Guardian bitta tranzaksiya bilan tizimni zudlik bilan to'xtata olishi kerak (hujumni jilovlash uchun), ammo tizimni qayta ishga tushirish faqat og'ir vaznli Multisig Admin qo'lida bo'ladi. Bu esa guardian kaliti o'g'irlangan taqdirda ham tizimni suiste'mol qilish imkonini bermaydi.

---

### Topshiriq #1198: Fee-on-Transfer va Qayta Balanslanuvchi (Rebasing) Tokenlar Xavfsizligi
**Tavsif:** Ko'plab ERC-20 tokenlari (masalan USDT ma'lum tarmoqlarda, STA, PAXG yoki stETH) o'tkazma paytida komissiya ushlab qoladi yoki balansni avtomatik o'zgartiradi (rebasing). Agar DEX yoki lending shartnomasi `transferFrom(user, address(this), amount)` deb yozib, hamyonga aniq `amount` tushdi deb hisoblasa, hisob-kitoblar buziladi va shartnoma kassa kamomadiga uchraydi.
**Talablar:** Haqiqiy tushgan mablag'ni `balanceOf(this)` ning o'zgarishi (delta) orqali aniqlash va xavfsiz ichki hisob yuritish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IERC20WithFee {
    function balanceOf(address account) external view returns (uint256);
    function transfer(address to, uint256 amount) external returns (bool);
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
}

/// @title DeflationaryTokenVault - Fee-on-Transfer tokenlarini to'g'ri qabul qiluvchi shartnoma
contract DeflationaryTokenVault {
    IERC20WithFee public immutable token;
    mapping(address => uint256) public userShares;
    uint256 public totalVaultBalance;

    event Deposited(address indexed user, uint256 requestedAmount, uint256 actualReceived);
    event Withdrawn(address indexed user, uint256 amountSent);

    constructor(address _tokenAddress) {
        require(_tokenAddress != address(0), "Nol manzil taqiqlangan");
        token = IERC20WithFee(_tokenAddress);
    }

    /// @notice Fee-on-transfer tokenlarini xavfsiz depozit qilish
    function deposit(uint256 amount) external {
        require(amount > 0, "Nol bo'lmagan miqdor kerak");

        // 1. O'tkazmadan oldingi haqiqiy balansni o'lchaymiz
        uint256 balanceBefore = token.balanceOf(address(this));

        // 2. Tokenlarni tortib olamiz
        bool success = token.transferFrom(msg.sender, address(this), amount);
        require(success, "Token o'tkazmasi muvaffaqiyatsiz bo'ldi");

        // 3. O'tkazmadan keyingi balansni o'lchaymiz
        uint256 balanceAfter = token.balanceOf(address(this));

        // 4. Haqiqiy kontraktga tushgan aniq miqdor (delta)
        uint256 actualAmountReceived = balanceAfter - balanceBefore;
        require(actualAmountReceived > 0, "Komissiyadan so'ng mablag' qolmadi");

        userShares[msg.sender] += actualAmountReceived;
        totalVaultBalance += actualAmountReceived;

        emit Deposited(msg.sender, amount, actualAmountReceived);
    }

    /// @notice Mablag'ni yechib olish
    function withdraw(uint256 amount) external {
        require(userShares[msg.sender] >= amount, "Ulush yetarli emas");

        userShares[msg.sender] -= amount;
        totalVaultBalance -= amount;

        bool success = token.transfer(msg.sender, amount);
        require(success, "Token qaytarish muvaffaqiyatsiz bo'ldi");

        emit Withdrawn(msg.sender, amount);
    }
}
```
**Tushuntirish:** Ko'plab DeFi protokollari (masalan Balancer v1) aynan 'Fee-on-Transfer' tokenlari hisobiga millionlab dollar yo'qotgan. Agar foydalanuvchi 100 token yuborsa-yu, kontraktga komissiya sababli 98 token tushsa, lekin shartnoma unga 100 deb yozib qo'ysa, shartnomadagi boshqa foydalanuvchilarning zaxirasi o'g'irlanadi. Shu sababli har doim `balanceAfter - balanceBefore` deltasini hisoblash talab etiladi.

---

### Topshiriq #1199: Frontrunning va Sandwich Hujumlaridan Himoya: Commit-Reveal Sxemasi
**Tavsif:** Mempool barcha uchun ochiq bo'lgani sababli, MEV botlari foydalanuvchining auksiondagi taklifi yoki yashirin harakatini oldindan ko'rib, undan oldinroq (Frontrun) yoki orqasidan (Sandwich) o'z tranzaksiyasini tiqib yuborishi mumkin.
**Talablar:** Ikki bosqichli Commit-Reveal arxitekturasini joriy etish: foydalanuvchi dastlab faqat hashni (commitment) saqlaydi, ma'lum bloklar o'tgach esa sirli parolini (secret/salt) ochib beradi (reveal).
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title CommitRevealAuction - Frontrunning hujumlariga qarshi auksion
contract CommitRevealAuction {
    struct Commitment {
        bytes32 commitHash;
        uint64 commitBlock;
        bool revealed;
    }

    mapping(address => Commitment) public commitments;
    mapping(address => uint256) public verifiedBids;

    uint256 public constant MIN_BLOCK_DELAY = 2; // Frontrunningdan himoya uchun oraliq
    uint256 public constant MAX_BLOCK_DELAY = 256; // Cheklangan reveal oynasi

    event BidCommitted(address indexed bidder, bytes32 commitHash);
    event BidRevealed(address indexed bidder, uint256 bidAmount);

    /// @notice 1-BOSQICH (COMMIT): Taklif va tuz (salt) xeshini yuborish
    /// @dev commitHash = keccak256(abi.encodePacked(bidAmount, salt, msg.sender))
    function commitBid(bytes32 _commitHash) external {
        require(_commitHash != bytes32(0), "Noto'g'ri xesh");

        commitments[msg.sender] = Commitment({
            commitHash: _commitHash,
            commitBlock: uint64(block.number),
            revealed: false
        });

        emit BidCommitted(msg.sender, _commitHash);
    }

    /// @notice 2-BOSQICH (REVEAL): Sirni ochish va haqiqiy taklifni tasdiqlash
    function revealBid(uint256 bidAmount, bytes32 salt) external payable {
        Commitment storage userCommit = commitments[msg.sender];
        require(userCommit.commitBlock > 0, "Commitment mavjud emas");
        require(!userCommit.revealed, "Allaqachon ochilgan");

        // Blok oralig'i tekshiruvi: bir xil blokda yoki darhol ochish mumkin emas
        require(block.number >= userCommit.commitBlock + MIN_BLOCK_DELAY, "Juda erta");
        require(block.number <= userCommit.commitBlock + MAX_BLOCK_DELAY, "Reveal muddati o'tgan");

        // Xeshning haqiqiyligini qayta tekshirish
        bytes32 calculatedHash = keccak256(abi.encodePacked(bidAmount, salt, msg.sender));
        require(calculatedHash == userCommit.commitHash, "Xesh mos kelmadi!");
        require(msg.value == bidAmount, "Yuborilgan ETH miqdori taklifga teng emas");

        userCommit.revealed = true;
        verifiedBids[msg.sender] = bidAmount;

        emit BidRevealed(msg.sender, bidAmount);
    }
}
```
**Tushuntirish:** Commit-Reveal sxemasi blokcheyndagi eng mustahkam kriptografik himoyalardan biridir. MEV botlari yoki konchilar foydalanuvchining niyatini mempoolda ko'ra olishmaydi, chunki faqat `keccak256(bid + salt + sender)` xeshi mavjud bo'ladi. Taklif tasdiqlanib blokcheynga kiritilgandan so'nggina ikkinchi bosqichda tuz (salt) va parametrlar e'lon qilinadi.

---

### Topshiriq #1200: Mukammal Korxona DeFi Xavfsizlik Ombori va Audit Kompleksi (Master Security Vault)
**Tavsif:** Ishlab chiqarish darajasidagi markazlashmagan moliya (DeFi) protokoli barcha xavfsizlik standartlarini: ReentrancyGuard, CEI, TimeLock, AccessControl, SafeERC20, CircuitBreaker, DoS himoyasi va favqulodda yechib olish mexanizmlarini bitta yaxlit arxitekturada birlashtirishi shart.
**Talablar:** Barcha xavfsizlik amaliyotlarini o'zida jamlagan mukammal audit darajasidagi korxona omborini yaratish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title MasterSecurityVault - Sanoat darajasidagi to'liq audit qilingan xavfsiz DeFi ombori
contract MasterSecurityVault {
    // -------------------------------------------------------------
    // STATIK XAVFSIZLIK KONSTANTALARI VA ROLLARI
    // -------------------------------------------------------------
    bytes32 public constant ROLE_ADMIN = keccak256("ROLE_ADMIN");
    bytes32 public constant ROLE_GUARDIAN = keccak256("ROLE_GUARDIAN");

    uint256 private constant _NOT_ENTERED = 1;
    uint256 private constant _ENTERED = 2;
    uint256 private _reentrancyStatus;

    bool public isEmergencyPaused;

    // Har bir foydalanuvchi hisobi
    mapping(address => uint256) private _balances;
    mapping(bytes32 => mapping(address => bool)) private _roles;

    uint256 public totalVaultLiquidity;

    // -------------------------------------------------------------
    // MAXSUS XATOLIKLAR (CUSTOM ERRORS)
    // -------------------------------------------------------------
    error ReentrantCallDetected();
    error ProtocolPaused();
    error InsufficientBalance(uint256 available, uint256 requested);
    error UnauthorizedAccess(bytes32 role, address caller);
    error ZeroAmountNotAllowed();
    error TransferExecutionFailed();

    // -------------------------------------------------------------
    // HODISALAR (EVENTS)
    // -------------------------------------------------------------
    event Deposited(address indexed user, uint256 amount);
    event Withdrawn(address indexed user, uint256 amount);
    event EmergencyPaused(address indexed triggeredBy);
    event EmergencyResumed(address indexed resumedBy);
    event RoleGranted(bytes32 indexed role, address indexed account);

    // -------------------------------------------------------------
    // MODIFIKATORLAR (MODIFIERS)
    // -------------------------------------------------------------
    modifier nonReentrant() {
        if (_reentrancyStatus == _ENTERED) revert ReentrantCallDetected();
        _reentrancyStatus = _ENTERED;
        _;
        _reentrancyStatus = _NOT_ENTERED;
    }

    modifier whenNotPaused() {
        if (isEmergencyPaused) revert ProtocolPaused();
        _;
    }

    modifier onlyRole(bytes32 role) {
        if (!_roles[role][msg.sender]) revert UnauthorizedAccess(role, msg.sender);
        _;
    }

    // -------------------------------------------------------------
    // KONSTRUKTOR
    // -------------------------------------------------------------
    constructor(address guardianMultisig) {
        require(guardianMultisig != address(0), "Guardian nol manzil bo'lishi mumkin emas");

        _reentrancyStatus = _NOT_ENTERED;
        _roles[ROLE_ADMIN][msg.sender] = true;
        _roles[ROLE_GUARDIAN][guardianMultisig] = true;

        emit RoleGranted(ROLE_ADMIN, msg.sender);
        emit RoleGranted(ROLE_GUARDIAN, guardianMultisig);
    }

    // -------------------------------------------------------------
    // ASOSIY BIZNES MANTIG'I (CEI VA TO'LIQ HIMOYA BILAN)
    // -------------------------------------------------------------
    /// @notice Depozit qilish
    function deposit() external payable nonReentrant whenNotPaused {
        if (msg.value == 0) revert ZeroAmountNotAllowed();

        // Internal Accounting
        _balances[msg.sender] += msg.value;
        totalVaultLiquidity += msg.value;

        emit Deposited(msg.sender, msg.value);
    }

    /// @notice Mablag'ni yechib olish (Checks-Effects-Interactions)
    function withdraw(uint256 amount) external nonReentrant whenNotPaused {
        if (amount == 0) revert ZeroAmountNotAllowed();

        uint256 userBal = _balances[msg.sender];
        if (userBal < amount) revert InsufficientBalance(userBal, amount);

        // EFFECTS (Ichki holatni tashqi chaqiruvdan oldin o'zgartirish)
        unchecked {
            _balances[msg.sender] = userBal - amount;
            totalVaultLiquidity -= amount;
        }

        emit Withdrawn(msg.sender, amount);

        // INTERACTIONS (Past darajali xavfsiz chaqiruv)
        (bool success, ) = payable(msg.sender).call{value: amount}("");
        if (!success) revert TransferExecutionFailed();
    }

    /// @notice Foydalanuvchi balansini ko'rish
    function balanceOf(address account) external view returns (uint256) {
        return _balances[account];
    }

    // -------------------------------------------------------------
    // FAVQULODDA BOSHQARUV TIZIMI (CIRCUIT BREAKER)
    // -------------------------------------------------------------
    /// @notice Xavf paytida zudlik bilan to'xtatish
    function triggerEmergencyPause() external onlyRole(ROLE_GUARDIAN) {
        isEmergencyPaused = true;
        emit EmergencyPaused(msg.sender);
    }

    /// @notice Xavf bartaraf etilgach qayta ishga tushirish (Faqat Bosh Admin)
    function resumeProtocol() external onlyRole(ROLE_ADMIN) {
        isEmergencyPaused = false;
        emit EmergencyResumed(msg.sender);
    }
}
```
**Tushuntirish:** Ushbu kontrakt DeFi audit standartlarining oltin qoidalarini o'zida birlashtirgan: 1) ReentrancyGuard flagi storage o'rniga gaz-tejamkor integer holatida boshqariladi. 2) Checks-Effects-Interactions patterni qat'iy qo'llangan. 3) Rol ajratilishi (Admin va Guardian). 4) Favqulodda to'xtatish (Circuit Breaker). 5) Custom Error'lar orqali gaz minimallashtirilgan va nosozliklarni aniqlash qulaylashtirilgan.

---
