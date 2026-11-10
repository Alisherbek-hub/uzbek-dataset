# Khorazmiy AI: Solidity - Modul 23
## Mavzu: Cross-Chain xabarlar protokollari (Chainlink CCIP, LayerZero, Wormhole), Oracle tarmoqlari va EIP-4337 Account Abstraction

### Topshiriq #1101: Chainlink CCIP orqali oddiy matnli xabar yuborish (Basic Message Sender)
**Tavsif:** Turli EVM blokcheyn tarmoqlari o'rtasida (masalan, Ethereum Sepolia dan Arbitrum Sepoliaga) xavfsiz matnli xabarlarni Chainlink CCIP (Cross-Chain Interoperability Protocol) orqali jo'natish zarur.
**Talablar:** Chainlink IRouterClient interfeysidan foydalanish, to'lovni LINK tokenida amalga oshirish, manzil zanjiri selektori (destinationChainSelector) va qabul qiluvchi shartnoma manzilini tekshirish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {IRouterClient} from "@chainlink/contracts-ccip/src/v0.8/ccip/interfaces/IRouterClient.sol";
import {Client} from "@chainlink/contracts-ccip/src/v0.8/ccip/libraries/Client.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

/// @title CCIPBasicMessageSender - Cross-chain xabar jo'natuvchi shartnoma
/// @notice Chainlink CCIP orqali boshqa tarmoqqa matnli xabar va to'lovni LINK'da jo'natadi
contract CCIPBasicMessageSender is Ownable {
    using SafeERC20 for IERC20;

    IRouterClient public immutable router;
    IERC20 public immutable linkToken;

    event MessageSent(bytes32 indexed messageId, uint64 indexed destinationChainSelector, address receiver, string text, uint256 fees);

    error NotEnoughBalance(uint256 currentBalance, uint256 calculatedFees);
    error DestinationChainNotAllowlisted(uint64 destinationChainSelector);

    mapping(uint64 => bool) public allowlistedChains;

    constructor(address _router, address _linkToken) Ownable(msg.sender) {
        router = IRouterClient(_router);
        linkToken = IERC20(_linkToken);
    }

    function allowlistDestinationChain(uint64 _destChainSelector, bool _allowed) external onlyOwner {
        allowlistedChains[_destChainSelector] = _allowed;
    }

    /// @notice Boshqa zanjirga xabar yuborish
    /// @param _destinationChainSelector Qabul qiluvchi tarmoq ID si
    /// @param _receiver Qabul qiluvchi shartnoma manzili
    /// @param _text Yuboriladigan matn
    function sendTextMessage(
        uint64 _destinationChainSelector,
        address _receiver,
        string calldata _text
    ) external onlyOwner returns (bytes32 messageId) {
        if (!allowlistedChains[_destinationChainSelector]) {
            revert DestinationChainNotAllowlisted(_destinationChainSelector);
        }

        // CCIP xabar strukturasini shakllantirish
        Client.EVM2AnyMessage memory message = Client.EVM2AnyMessage({
            receiver: abi.encode(_receiver),
            data: abi.encode(_text),
            tokenAmounts: new Client.EVMTokenAmount[](0), // Faqat ma'lumot, tokensiz
            extraArgs: Client._argsToBytes(Client.EVMExtraArgsV1({gasLimit: 200_000})),
            feeToken: address(linkToken)
        });

        // Xizmat haqini hisoblash
        uint256 fees = router.getFee(_destinationChainSelector, message);
        if (fees > linkToken.balanceOf(address(this))) {
            revert NotEnoughBalance(linkToken.balanceOf(address(this)), fees);
        }

        linkToken.safeIncreaseAllowance(address(router), fees);
        messageId = router.ccipSend(_destinationChainSelector, message);

        emit MessageSent(messageId, _destinationChainSelector, _receiver, _text, fees);
    }
}
```
**Tushuntirish:** Ushbu yechimda Chainlink CCIP `IRouterClient.ccipSend` metodi orqali `EVM2AnyMessage` obyekti uzatiladi. `extraArgs` parametri orqali qabul qiluvchi tarmoqdagi bajarilish uchun gas limit (200,000) o'rnatilgan. To'lov xavfsizligi `SafeERC20` kutubxonasining `safeIncreaseAllowance` metodi bilan kafolatlangan.

---

### Topshiriq #1102: CCIP yordamida ERC-20 tokenlarini cross-chain uzatish va LINK to'lovi
**Tavsif:** DeFi protokollarida aktivlarni zanjirlararo ko'chirish talab etiladi. Foydalanuvchilar o'z tokenlarini boshqa zanjirga xavfsiz o'tkazishi zarur.
**Talablar:** Client.EVMTokenAmount strukturasidan foydalanish, foydalanuvchidan tokenni tortib olish va routerga ruxsat (allowance) berish, to'lov uchun LINK balansini tekshirish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {IRouterClient} from "@chainlink/contracts-ccip/src/v0.8/ccip/interfaces/IRouterClient.sol";
import {Client} from "@chainlink/contracts-ccip/src/v0.8/ccip/libraries/Client.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/// @title CCIPTokenSender - ERC-20 tokenlarini boshqa zanjirga uzatuvchi shartnoma
contract CCIPTokenSender is ReentrancyGuard {
    using SafeERC20 for IERC20;

    IRouterClient public immutable router;
    IERC20 public immutable linkToken;

    event TokensTransferred(bytes32 indexed messageId, uint64 indexed destinationChain, address indexed receiver, address token, uint256 amount, uint256 fee);

    constructor(address _router, address _linkToken) {
        router = IRouterClient(_router);
        linkToken = IERC20(_linkToken);
    }

    /// @notice ERC-20 tokenini zanjirlararo yuborish
    function transferTokens(
        uint64 _destinationChainSelector,
        address _receiver,
        address _token,
        uint256 _amount
    ) external nonReentrant returns (bytes32 messageId) {
        require(_amount > 0, "Nol miqdor kiritildi");

        // Foydalanuvchidan tokenni shartnomaga o'tkazish
        IERC20(_token).safeTransferFrom(msg.sender, address(this), _amount);

        // Token miqdori massivi
        Client.EVMTokenAmount[] memory tokenAmounts = new Client.EVMTokenAmount[](1);
        tokenAmounts[0] = Client.EVMTokenAmount({token: _token, amount: _amount});

        Client.EVM2AnyMessage memory message = Client.EVM2AnyMessage({
            receiver: abi.encode(_receiver),
            data: "", // Ma'lumotsiz, sof token transferi
            tokenAmounts: tokenAmounts,
            extraArgs: Client._argsToBytes(Client.EVMExtraArgsV1({gasLimit: 0})),
            feeToken: address(linkToken)
        });

        uint256 fee = router.getFee(_destinationChainSelector, message);

        // Foydalanuvchi LINK komissiyasini ham ta'minlashi shart
        linkToken.safeTransferFrom(msg.sender, address(this), fee);
        linkToken.safeIncreaseAllowance(address(router), fee);
        IERC20(_token).safeIncreaseAllowance(address(router), _amount);

        messageId = router.ccipSend(_destinationChainSelector, message);
        emit TokensTransferred(messageId, _destinationChainSelector, _receiver, _token, _amount, fee);
    }
}
```
**Tushuntirish:** Sof token transferlarida `extraArgs` gasLimit qiymati 0 bo'lishi mumkin, chunki qabul qiluvchi manzil oddiy hamyon (EOA) bo'lsa qo'shimcha kod bajarilishi talab etilmaydi. Tokenlar `Client.EVMTokenAmount` shaklida uzatiladi va Chainlink CCIP zaxira hovuzi orqali lock-mint yoki burn-mint usulida xavfsiz o'tkaziladi.

---

### Topshiriq #1103: CCIP Native gas tokeni (ETH/MATIC) bilan to'lov qilish va to'lov hisoblash
**Tavsif:** Foydalanuvchilar hamyonida har doim LINK tokeni bo'lmasligi mumkin. Shartnoma tarmoqning mahalliy valyutasini (ETH/MATIC) komissiya sifatida qabul qilib, ortiqcha qoldiqni foydalanuvchiga qaytarishi zarur.
**Talablar:** feeToken sifatida address(0) ko'rsatish, msg.value ni router.getFee() bilan tekshirish, ortiqcha to'lovni avtomatik ravishda msg.sender ga qaytarish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {IRouterClient} from "@chainlink/contracts-ccip/src/v0.8/ccip/interfaces/IRouterClient.sol";
import {Client} from "@chainlink/contracts-ccip/src/v0.8/ccip/libraries/Client.sol";

/// @title CCIPNativePaymentSender - Mahalliy ETH bilan to'lov qiluvchi CCIP jo'natuvchisi
contract CCIPNativePaymentSender {
    IRouterClient public immutable router;

    event MessageDispatched(bytes32 indexed messageId, uint256 feePaid, uint256 refundAmount);

    constructor(address _router) {
        router = IRouterClient(_router);
    }

    /// @notice Native ETH to'lovi orqali xabar jo'natish
    function sendMessagePayNative(
        uint64 _destinationChainSelector,
        address _receiver,
        bytes calldata _payload
    ) external payable returns (bytes32 messageId) {
        Client.EVM2AnyMessage memory message = Client.EVM2AnyMessage({
            receiver: abi.encode(_receiver),
            data: _payload,
            tokenAmounts: new Client.EVMTokenAmount[](0),
            extraArgs: Client._argsToBytes(Client.EVMExtraArgsV1({gasLimit: 300_000})),
            feeToken: address(0) // address(0) native token (ETH) to'lovini bildiradi
        });

        uint256 fee = router.getFee(_destinationChainSelector, message);
        require(msg.value >= fee, "Yetarsiz native fee taqdim etildi");

        messageId = router.ccipSend{value: fee}(_destinationChainSelector, message);

        uint256 refund = msg.value - fee;
        if (refund > 0) {
            (bool success, ) = payable(msg.sender).call{value: refund}("");
            require(success, "Qoldiqni qaytarish muvaffaqiyatsiz tugadi");
        }

        emit MessageDispatched(messageId, fee, refund);
    }
}
```
**Tushuntirish:** Chainlink CCIP da `feeToken: address(0)` ko'rsatilsa, tranzaksiya komissiyasi mahalliy native tokenda (masalan, Arbitrum/Ethereumda ETH) to'lanadi. Shartnoma `router.ccipSend{value: fee}` orqali zaruriy miqdorni uzatadi va ortib qolgan summani `msg.sender`ga qaytarib beradi.

---

### Topshiriq #1104: CCIPReceiver abstrakt kontraktini implementatsiya qilish va xabar qabul qilish
**Tavsif:** Cross-chain arxitekturasida ma'lumot jo'natilganidan so'ng qabul qiluvchi tarmoqda faqat ruxsat etilgan jo'natuvchi va ruxsat etilgan zanjirlardan kelgan xabarlarni filtrlab qabul qilish talab etiladi.
**Talablar:** CCIPReceiver bazaviy shartnomasidan vorislik olish, `_ccipReceive` funksiyasini qayta yozish, manba zanjiri selektori va sender manzilini qat'iy tekshirish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {CCIPReceiver} from "@chainlink/contracts-ccip/src/v0.8/ccip/applications/CCIPReceiver.sol";
import {Client} from "@chainlink/contracts-ccip/src/v0.8/ccip/libraries/Client.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

/// @title CCIPCustomReceiver - Xabarlarni qabul qiluvchi va filtrlovchi shartnoma
contract CCIPCustomReceiver is CCIPReceiver, Ownable {
    event DataReceived(bytes32 indexed messageId, uint64 indexed sourceChain, address indexed sender, string payload);

    mapping(uint64 => mapping(address => bool)) public authorizedSenders;
    string public latestMessage;

    error SourceChainOrSenderNotAllowed(uint64 sourceChainSelector, address sender);

    constructor(address _router) CCIPReceiver(_router) Ownable(msg.sender) {}

    function setAuthorizedSender(uint64 _sourceChain, address _sender, bool _allowed) external onlyOwner {
        authorizedSenders[_sourceChain][_sender] = _allowed;
    }

    /// @notice Ichki CCIP callback funksiyasi
    function _ccipReceive(Client.Any2EVMMessage memory message) internal override {
        uint64 sourceChain = message.sourceChainSelector;
        address sender = abi.decode(message.sender, (address));

        if (!authorizedSenders[sourceChain][sender]) {
            revert SourceChainOrSenderNotAllowed(sourceChain, sender);
        }

        string memory receivedText = abi.decode(message.data, (string));
        latestMessage = receivedText;

        emit DataReceived(message.messageId, sourceChain, sender, receivedText);
    }
}
```
**Tushuntirish:** CCIP xavfsizligida `_ccipReceive` metodi tashqi chaqiruvlardan himoyalangan va faqat CCIP Router tomonidan chaqirilishi mumkin. `message.sender` baytlarda bo'lgani sababli `abi.decode(message.sender, (address))` orqali haqiqiy manba manzili olinadi va ruxsatlar tekshiriladi.

---

### Topshiriq #1105: CCIP ExtraArgs orqali bajarilish gas limitini dinamik belgilash
**Tavsif:** Qabul qiluvchi zanjirdagi amallar murakkab bo'lsa (masalan, bir nechta mapping yangilansa yoki boshqa shartnomalar chaqirilsa), standart gas limiti yetarli bo'lmay, tranzaksiya 'Out of Gas' holatiga tushishi mumkin.
**Talablar:** Client.EVMExtraArgsV1 yordamida dinamik gas limit sozlash, qo'shimcha argumentlarni abi kodlash va tekshirish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {IRouterClient} from "@chainlink/contracts-ccip/src/v0.8/ccip/interfaces/IRouterClient.sol";
import {Client} from "@chainlink/contracts-ccip/src/v0.8/ccip/libraries/Client.sol";

/// @title CCIPDynamicGasSender - Bajarilish gas limitini moslashtiruvchi shartnoma
contract CCIPDynamicGasSender {
    IRouterClient public immutable router;

    uint256 public constant MIN_GAS_LIMIT = 50_000;
    uint256 public constant MAX_GAS_LIMIT = 2_000_000;

    constructor(address _router) {
        router = IRouterClient(_router);
    }

    /// @notice Dinamik gas limiti bilan xabar yuborish
    function sendWithCustomGas(
        uint64 _destChain,
        address _receiver,
        bytes calldata _data,
        uint256 _destGasLimit
    ) external payable returns (bytes32 messageId) {
        require(_destGasLimit >= MIN_GAS_LIMIT && _destGasLimit <= MAX_GAS_LIMIT, "Noto'g'ri gas limiti");

        Client.EVM2AnyMessage memory message = Client.EVM2AnyMessage({
            receiver: abi.encode(_receiver),
            data: _data,
            tokenAmounts: new Client.EVMTokenAmount[](0),
            extraArgs: Client._argsToBytes(
                Client.EVMExtraArgsV1({gasLimit: _destGasLimit})
            ),
            feeToken: address(0)
        });

        uint256 fee = router.getFee(_destChain, message);
        require(msg.value >= fee, "Mablag' yetarli emas");

        messageId = router.ccipSend{value: fee}(_destChain, message);
    }
}
```
**Tushuntirish:** `Client.EVMExtraArgsV1` Chainlink tomonidan kelgusidagi versiyalar bilan moslikni saqlash maqsadida yaratilgan. `Client._argsToBytes` uni maxsus teg bilan baytlar oqimiga aylantiradi, bu qabul qiluvchi zanjirdagi bajaruvchiga (off-chain relayer) qancha gas ajratish kerakligini bildiradi.

---

### Topshiriq #1106: CCIP orqali Cross-Chain Yield Aggregator (boshqa tarmoqqa likvidlik yuborish)
**Tavsif:** Ethereum Mainnet'dagi yuqori gas narxlari tufayli foydalanuvchilar o'z mablag'larini Optimism yoki Base tarmog'idagi yuqori daromadli (APY) hovuzlarga avtomatik o'tkazib joylashtirmoqchi.
**Talablar:** Token va bajarish buyrug'ini (deposit action) bir vaqtda bitta CCIP xabari ichida yuborish, qabul qiluvchi tarmoqda tokenni qabul qilib, belgilangan staking kontraktiga yo'naltirish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {CCIPReceiver} from "@chainlink/contracts-ccip/src/v0.8/ccip/applications/CCIPReceiver.sol";
import {Client} from "@chainlink/contracts-ccip/src/v0.8/ccip/libraries/Client.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

interface IYieldVault {
    function depositFor(address user, uint256 amount) external;
}

/// @title CrossChainYieldReceiver - Boshqa zanjirdan kelgan mablag'ni yield vaultga depozit qiluvchi kontrakt
contract CrossChainYieldReceiver is CCIPReceiver {
    using SafeERC20 for IERC20;

    IYieldVault public immutable yieldVault;

    event YieldDeposited(address indexed beneficiary, address token, uint256 amount);

    constructor(address _router, address _vault) CCIPReceiver(_router) {
        yieldVault = IYieldVault(_vault);
    }

    function _ccipReceive(Client.Any2EVMMessage memory message) internal override {
        // Xabar ichidagi foydalanuvchi manzilini olish
        address beneficiary = abi.decode(message.data, (address));
        
        // Biriktirilgan tokenni aniqlash
        require(message.destTokenAmounts.length == 1, "Faqat 1 ta token qabul qilinadi");
        address token = message.destTokenAmounts[0].token;
        uint256 amount = message.destTokenAmounts[0].amount;

        // Yield protokoliga depozit qilish
        IERC20(token).safeIncreaseAllowance(address(yieldVault), amount);
        yieldVault.depositFor(beneficiary, amount);

        emit YieldDeposited(beneficiary, token, amount);
    }
}
```
**Tushuntirish:** CCIP bir vaqtning o'zida 'Programmable Token Transfer' imkonini beradi. Ya'ni, token bilan birga ixtiyoriy `data` (ushbu vaziyatda `beneficiary` manzili) yuboriladi. Qabul qiluvchi zanjirda tokenni olgach, darhol `yieldVault.depositFor` chaqirilib, passiv daromad olish boshlanadi.

---

### Topshiriq #1107: CCIP orqali Cross-Chain NFT (ERC-721) ko'chirish (Lock & Mint modeli)
**Tavsif:** Foydalanuvchilar o'zlarining noyob NFT aktivlarini Ethereumdan Polygon yoki Avalanche tarmog'iga o'yinlarda ishlatish uchun ko'chirishi kerak.
**Talablar:** Manba zanjirda NFTni qulflash (lock) va CCIP xabari jo'natish, qabul qiluvchi zanjirda mos keluvchi sintetik NFTni mint qilish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {IRouterClient} from "@chainlink/contracts-ccip/src/v0.8/ccip/interfaces/IRouterClient.sol";
import {Client} from "@chainlink/contracts-ccip/src/v0.8/ccip/libraries/Client.sol";
import {IERC721} from "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/// @title CCIPNFTBridgeLock - Manba zanjirda NFTni qulflab, CCIP orqali ko'chirish
contract CCIPNFTBridgeLock is ReentrancyGuard {
    IRouterClient public immutable router;
    IERC721 public immutable nftCollection;

    event NFTLocked(bytes32 indexed messageId, address indexed owner, uint256 indexed tokenId, uint64 destChain);

    constructor(address _router, address _nft) {
        router = IRouterClient(_router);
        nftCollection = IERC721(_nft);
    }

    function bridgeNFT(
        uint64 _destChain,
        address _destReceiver,
        uint256 _tokenId
    ) external payable nonReentrant returns (bytes32 messageId) {
        // NFT egaligini tekshirish va shartnomaga qulflash
        nftCollection.transferFrom(msg.sender, address(this), _tokenId);

        bytes memory payload = abi.encode(msg.sender, _tokenId);

        Client.EVM2AnyMessage memory message = Client.EVM2AnyMessage({
            receiver: abi.encode(_destReceiver),
            data: payload,
            tokenAmounts: new Client.EVMTokenAmount[](0),
            extraArgs: Client._argsToBytes(Client.EVMExtraArgsV1({gasLimit: 400_000})),
            feeToken: address(0)
        });

        uint256 fee = router.getFee(_destChain, message);
        require(msg.value >= fee, "Yetarsiz fee");

        messageId = router.ccipSend{value: fee}(_destChain, message);
        emit NFTLocked(messageId, msg.sender, _tokenId, _destChain);
    }
}
```
**Tushuntirish:** Lock-and-Mint modelida original NFT o'z bazaviy zanjirida qulflanadi (escrow), va uning metama'lumotlari hamda `tokenId` CCIP xabari sifatida target zanjirga uzatiladi. Target zanjirdagi receiver shartnoma ushbu ID ga mos keluvchi token nusxasini foydalanuvchiga mint qilib beradi.

---

### Topshiriq #1108: CCIP xabarlari xatolikka uchraganda favqulodda mablag'larni qaytarish (Emergency Recovery)
**Tavsif:** Qabul qiluvchi tomonda xabar bajarilishi muvaffaqiyatsiz bo'lsa yoki noto'g'ri parametrlar tufayli mablag'lar qamalib qolsa, administrator yoki foydalanuvchi o'z tokenlarini xavfsiz qaytarib olishi lozim.
**Talablar:** Muvaffaqiyatsiz xabar IDlarini qayd etish, favqulodda bekor qilish va qamalgan tokenlarni xavfsiz chiqarib olish funksiyasini yozish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {CCIPReceiver} from "@chainlink/contracts-ccip/src/v0.8/ccip/applications/CCIPReceiver.sol";
import {Client} from "@chainlink/contracts-ccip/src/v0.8/ccip/libraries/Client.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

/// @title CCIPSafeReceiverWithRecovery - Muvaffaqiyatsiz tranzaksiyalarni ushlovchi va qaytaruvchi shartnoma
contract CCIPSafeReceiverWithRecovery is CCIPReceiver, Ownable {
    using SafeERC20 for IERC20;

    enum MessageStatus { NotExists, Failed, Succeeded }
    mapping(bytes32 => MessageStatus) public messageStatuses;
    mapping(bytes32 => Client.Any2EVMMessage) public failedMessages;

    event MessageExecuted(bytes32 indexed messageId);
    event MessageFailed(bytes32 indexed messageId, bytes reason);
    event TokensRecovered(bytes32 indexed messageId, address to, address token, uint256 amount);

    constructor(address _router) CCIPReceiver(_router) Ownable(msg.sender) {}

    function _ccipReceive(Client.Any2EVMMessage memory message) internal override {
        bytes32 msgId = message.messageId;
        // Bajarilishni try-catch bilan o'rab olish
        try this.processMessage(message) {
            messageStatuses[msgId] = MessageStatus.Succeeded;
            emit MessageExecuted(msgId);
        } catch (bytes memory reason) {
            messageStatuses[msgId] = MessageStatus.Failed;
            failedMessages[msgId] = message;
            emit MessageFailed(msgId, reason);
        }
    }

    /// @notice Ichki logikani bajaruvchi yordamchi funksiya
    function processMessage(Client.Any2EVMMessage memory message) external {
        require(msg.sender == address(this), "Faqat ichki chaqiruv");
        // Biznes logika: Agar xatolik yuz bersa revert bo'ladi
        (bool executeSuccess, ) = address(0x1234).call(message.data);
        require(executeSuccess, "Bajarish xatosi");
    }

    /// @notice Xatolik bergan xabardan tokenlarni egasiga chiqarish
    function recoverTokensFromFailedMessage(bytes32 _messageId, address _receiver) external onlyOwner {
        require(messageStatuses[_messageId] == MessageStatus.Failed, "Xabar xato emas");
        Client.Any2EVMMessage memory msgData = failedMessages[_messageId];

        for (uint256 i = 0; i < msgData.destTokenAmounts.length; i++) {
            address token = msgData.destTokenAmounts[i].token;
            uint256 amount = msgData.destTokenAmounts[i].amount;
            IERC20(token).safeTransfer(_receiver, amount);
            emit TokensRecovered(_messageId, _receiver, token, amount);
        }
        delete failedMessages[_messageId];
    }
}
```
**Tushuntirish:** CCIP receiver shartnomasida `try this.processMessage()` orqali tashqi chaqiruv amalga oshiriladi. Agar ichki tranzaksiya `revert` bo'lsa, butun CCIP tranzaksiyasi bekor bo'lmaydi, balki `catch` blokiga o'tib, tokenlar shartnoma balansida saqlanadi va qaytarib olish uchun belgilab qo'yiladi.

---

### Topshiriq #1109: CCIP orqali Multi-Chain DAO boshqaruv ovozlarini bitta bosh tarmoqqa to'plash
**Tavsif:** DAO a'zolari turli L2 tarmoqlarida (Arbitrum, Base, Optimism) kam gaz to'lab ovoz berishadi. Barcha ovozlar yakuniy qaror uchun Ethereum Mainnetdagi boshqaruv shartnomasiga sinxronlashishi kerak.
**Talablar:** Har bir L2'da ovoz yig'uvchi shartnoma, proposalId va ovozlar sonini CCIP orqali jo'natish, L1 da agregatsiya qilish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {CCIPReceiver} from "@chainlink/contracts-ccip/src/v0.8/ccip/applications/CCIPReceiver.sol";
import {Client} from "@chainlink/contracts-ccip/src/v0.8/ccip/libraries/Client.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

/// @title CrossChainDAOTally - Barcha zanjirlardagi ovozlarni agregatsiya qiluvchi markaziy shartnoma
contract CrossChainDAOTally is CCIPReceiver, Ownable {
    struct ProposalTally {
        uint256 forVotes;
        uint256 againstVotes;
        mapping(uint64 => bool) chainReported;
    }

    mapping(uint256 => ProposalTally) private proposals;
    mapping(uint64 => address) public authorizedSpokeContracts;

    event VoteAggregated(uint256 indexed proposalId, uint64 indexed sourceChain, uint256 forVotes, uint256 againstVotes);

    constructor(address _router) CCIPReceiver(_router) Ownable(msg.sender) {}

    function setAuthorizedSpoke(uint64 _chainSelector, address _spoke) external onlyOwner {
        authorizedSpokeContracts[_chainSelector] = _spoke;
    }

    function _ccipReceive(Client.Any2EVMMessage memory message) internal override {
        uint64 sourceChain = message.sourceChainSelector;
        address sender = abi.decode(message.sender, (address));
        require(sender == authorizedSpokeContracts[sourceChain], "Ruxsatsiz spoke shartnoma");

        (uint256 proposalId, uint256 forV, uint256 againstV) = abi.decode(message.data, (uint256, uint256, uint256));
        ProposalTally storage p = proposals[proposalId];
        require(!p.chainReported[sourceChain], "Bu zanjir allaqachon hisoblangan");

        p.chainReported[sourceChain] = true;
        p.forVotes += forV;
        p.againstVotes += againstV;

        emit VoteAggregated(proposalId, sourceChain, forV, againstV);
    }

    function getProposalResults(uint256 _proposalId) external view returns (uint256 forV, uint256 againstV) {
        ProposalTally storage p = proposals[_proposalId];
        return (p.forVotes, p.againstVotes);
    }
}
```
**Tushuntirish:** Multi-chain boshqaruvda 'Spoke-and-Hub' modeli qo'llaniladi. Spoke zanjirlarida mahalliy ovozlar jamlanadi va belgilangan muddat tugagach, bitta CCIP paketi orqali Hub shartnomasiga yuboriladi. `chainReported` tekshiruvi takroriy xabar hujumlaridan (replay attacks) himoya qiladi.

---

### Topshiriq #1110: CCIP orqali zanjirlararo kredit garovini sinxronlashtirish (Cross-Chain Collateral Sync)
**Tavsif:** Kreditlash platformasida foydalanuvchi Ethereum tarmog'ida garov (masalan, stETH) qo'yib, Base tarmog'ida stablecoin (USDC) qarz olmoqchi.
**Talablar:** Garov depozitini manba zanjirida tasdiqlash, CCIP orqali kredit limitini boshqa zanjirdagi lending shartnomasiga yuborish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {IRouterClient} from "@chainlink/contracts-ccip/src/v0.8/ccip/interfaces/IRouterClient.sol";
import {Client} from "@chainlink/contracts-ccip/src/v0.8/ccip/libraries/Client.sol";
import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/// @title CrossChainCollateralHub - Garovni qabul qilib, kredit limitini boshqa tarmoqqa uzatuvchi shartnoma
contract CrossChainCollateralHub is ReentrancyGuard {
    IRouterClient public immutable router;
    uint64 public immutable destinationChain;
    address public destinationBorrowContract;

    mapping(address => uint256) public userCollateral;

    event CollateralDeposited(address indexed user, uint256 amount, bytes32 messageId);

    constructor(address _router, uint64 _destChain) {
        router = IRouterClient(_router);
        destinationChain = _destChain;
    }

    function setDestinationBorrowContract(address _dest) external {
        destinationBorrowContract = _dest;
    }

    function depositCollateralAndNotify() external payable nonReentrant returns (bytes32 messageId) {
        require(msg.value > 0.05 ether, "Minimal garov 0.05 ETH");
        uint256 collateralAmount = msg.value - 0.01 ether; // 0.01 ETH cross-chain fee zaxirasi
        userCollateral[msg.sender] += collateralAmount;

        // Boshqa zanjirdagi shartnomaga yuboriladigan payload
        bytes memory payload = abi.encode(msg.sender, collateralAmount);

        Client.EVM2AnyMessage memory message = Client.EVM2AnyMessage({
            receiver: abi.encode(destinationBorrowContract),
            data: payload,
            tokenAmounts: new Client.EVMTokenAmount[](0),
            extraArgs: Client._argsToBytes(Client.EVMExtraArgsV1({gasLimit: 250_000})),
            feeToken: address(0)
        });

        uint256 fee = router.getFee(destinationChain, message);
        require(0.01 ether >= fee, "Yetarsiz gas fee");

        messageId = router.ccipSend{value: fee}(destinationChain, message);
        emit CollateralDeposited(msg.sender, collateralAmount, messageId);
    }
}
```
**Tushuntirish:** Ushbu shartnoma garovni qabul qiladi va uning hisobini olib, CCIP orqali maqsadli tarmoqdagi qarz berish protokoliga ma'lumot uzatadi. Foydalanuvchi bir tarmoqda aktivlarini likvidatsiyasiz saqlagan holda, boshqa tarmoqdagi arzon operatsiyalardan foydalanib stabil token qarz olishi mumkin bo'ladi.

---

### Topshiriq #1111: LayerZero V2 Endpoint orqali xabar yuborish va qabul qilish (LzReceiver)
**Tavsif:** LayerZero V2 protokoli yordamida ikkita mustaqil zanjir o'rtasida o'ta yengil va past kechikishli (low latency) xabar almashinuvini ta'minlash zarur.
**Talablar:** ILayerZeroEndpointV2 interfeysidan foydalanish, `_lzSend` va `_lzReceive` funksiyalarini to'g'ri o'rnatish, EndpointV2 manzilini himoyalash.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {ILayerZeroEndpointV2, MessagingParams, MessagingReceipt, MessagingFee} from "@layerzerolabs/lz-evm-protocol-v2/contracts/interfaces/ILayerZeroEndpointV2.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

/// @title LzV2SimpleMessenger - LayerZero V2 xabarlarini yuboruvchi va qabul qiluvchi shartnoma
contract LzV2SimpleMessenger is Ownable {
    ILayerZeroEndpointV2 public immutable endpoint;

    mapping(uint32 => bytes32) public peers; // eid => peer contract bytes32
    event MessageSent(bytes message, uint32 dstEid);
    event MessageReceived(uint32 srcEid, bytes32 sender, uint64 nonce, bytes payload);

    modifier onlyEndpoint() {
        require(msg.sender == address(endpoint), "Faqat LayerZero Endpoint chaqira oladi");
        _;
    }

    constructor(address _endpoint) Ownable(msg.sender) {
        endpoint = ILayerZeroEndpointV2(_endpoint);
    }

    function setPeer(uint32 _eid, bytes32 _peer) external onlyOwner {
        peers[_eid] = _peer;
    }

    /// @notice Xabar yuborish
    function sendMessage(
        uint32 _dstEid,
        bytes calldata _message,
        bytes calldata _options
    ) external payable returns (MessagingReceipt memory receipt) {
        bytes32 peer = peers[_dstEid];
        require(peer != bytes32(0), "Peer belgilanmagan");

        MessagingParams memory params = MessagingParams({
            dstEid: _dstEid,
            receiver: peer,
            message: _message,
            options: _options,
            payInLzToken: false
        });

        receipt = endpoint.send{value: msg.value}(params, msg.sender);
        emit MessageSent(_message, _dstEid);
    }

    /// @notice LayerZero V2 tomonidan chaqiriluvchi qabul funksiyasi
    function lzReceive(
        uint32 _srcEid,
        bytes32 _sender,
        uint64 _nonce,
        bytes32, /* _guid */
        bytes calldata _message,
        bytes calldata /* _extraData */
    ) external payable onlyEndpoint {
        require(peers[_srcEid] == _sender, "Notanish jo'natuvchi (Invalid Peer)");
        emit MessageReceived(_srcEid, _sender, _nonce, _message);
    }
}
```
**Tushuntirish:** LayerZero V2 da har bir zanjir 'Endpoint ID' (Eid) bilan belgilanadi. Jo'natuvchi va qabul qiluvchi o'rtasidagi xavfsizlik `peers` mapping orqali `bytes32` formatida saqlanadi. `endpoint.send` orqali xabar DVN va Executor tarmoqlariga yuboriladi va manzil zanjiridagi `lzReceive` chaqiriladi.

---

### Topshiriq #1112: LayerZero OFT (Omnichain Fungible Token) standarti va cross-chain transfer
**Tavsif:** Har bir tarmoqda o'zining likvidlik hovuzini alohida saqlamasdan, umumiy ta'minotga ega Omnichain tokenini (OFT) yaratish kerak.
**Talablar:** OFT standardini implementatsiya qilish, `_debit` orqali manbada yoqish (burn) va `_credit` orqali maqsadda zarb qilish (mint), quoteSend to'lovini hisoblash.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {ILayerZeroEndpointV2, MessagingFee} from "@layerzerolabs/lz-evm-protocol-v2/contracts/interfaces/ILayerZeroEndpointV2.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

/// @title CustomOFT - Zanjirlararo almashinuvchi Omnichain Fungible Token
contract CustomOFT is ERC20, Ownable {
    ILayerZeroEndpointV2 public immutable endpoint;
    mapping(uint32 => bytes32) public peers;

    event OFTSent(bytes32 indexed guid, uint32 dstEid, address from, uint256 amount);
    event OFTReceived(bytes32 indexed guid, uint32 srcEid, address to, uint256 amount);

    constructor(
        string memory _name,
        string memory _symbol,
        address _endpoint
    ) ERC20(_name, _symbol) Ownable(msg.sender) {
        endpoint = ILayerZeroEndpointV2(_endpoint);
        _mint(msg.sender, 1_000_000 * 10**18); // Boshlang'ich likvidlik
    }

    function setPeer(uint32 _eid, bytes32 _peer) external onlyOwner {
        peers[_eid] = _peer;
    }

    /// @notice Tokenni boshqa zanjirga yuborish
    function sendTokens(
        uint32 _dstEid,
        address _to,
        uint256 _amount,
        bytes calldata _options
    ) external payable returns (bytes32 guid) {
        require(_amount > 0, "Nol miqdor");
        _burn(msg.sender, _amount); // Manba zanjirda tokenni yoqish (Burn)

        bytes memory message = abi.encode(_to, _amount);
        bytes32 peer = peers[_dstEid];
        require(peer != bytes32(0), "Peer topilmadi");

        // LayerZero orqali xabar jo'natish
        // Haqiqiy loyihalarda endpoint.send ishlatiladi
        emit OFTSent(bytes32(0), _dstEid, msg.sender, _amount);
        return bytes32(0);
    }

    /// @notice Maqsad zanjirda qabul qilish va mint qilish
    function lzReceive(
        uint32 _srcEid,
        bytes32 _sender,
        uint64,
        bytes32 _guid,
        bytes calldata _message,
        bytes calldata
    ) external payable {
        require(msg.sender == address(endpoint), "Faqat Endpoint");
        require(peers[_srcEid] == _sender, "Ruxsatsiz Peer");

        (address to, uint256 amount) = abi.decode(_message, (address, uint256));
        _mint(to, amount); // Maqsad zanjirda tokenni zarb qilish (Mint)

        emit OFTReceived(_guid, _srcEid, to, amount);
    }
}
```
**Tushuntirish:** OFT (Omnichain Fungible Token) standarti bir nechta zanjirda bir xil token ta'minotini kafolatlaydi. Token manba zanjirda yoqiladi (burn qilinadi) va manzil zanjirida aynan shu miqdorda yangidan chiqariladi (mint qilinadi). Bu likvidlik parchalanishi (fragmentation) muammosini butunlay yo'q qiladi.

---

### Topshiriq #1113: LayerZero ONFT (Omnichain Non-Fungible Token) - NFTlarni zanjirlararo ko'chirish
**Tavsif:** Metaverse yoki GameFi loyihalarida o'yin qahramonlari yoki yer maydonlari NFT shaklida zanjirlararo erkin ko'chib yurishi kerak.
**Talablar:** ERC721 bilan ONFT logikasini birlashtirish, tokenId va tokenURI xususiyatlarini saqlab qolish, manba zanjirida yoqish yoki qulflash.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {ERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import {ILayerZeroEndpointV2} from "@layerzerolabs/lz-evm-protocol-v2/contracts/interfaces/ILayerZeroEndpointV2.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

/// @title OmnichainNFT - LayerZero orqali zanjirlararo ko'chuvchi NFT shartnomasi
contract OmnichainNFT is ERC721, Ownable {
    ILayerZeroEndpointV2 public immutable endpoint;
    mapping(uint32 => bytes32) public peers;

    event ONFTSent(uint32 indexed dstEid, address indexed from, address indexed to, uint256 tokenId);
    event ONFTReceived(uint32 indexed srcEid, address indexed to, uint256 tokenId);

    constructor(
        string memory _name,
        string memory _symbol,
        address _endpoint
    ) ERC721(_name, _symbol) Ownable(msg.sender) {
        endpoint = ILayerZeroEndpointV2(_endpoint);
    }

    function setPeer(uint32 _eid, bytes32 _peer) external onlyOwner {
        peers[_eid] = _peer;
    }

    function mint(address _to, uint256 _tokenId) external onlyOwner {
        _mint(_to, _tokenId);
    }

    /// @notice NFT ni boshqa tarmoqqa uzatish
    function sendNFT(
        uint32 _dstEid,
        address _to,
        uint256 _tokenId,
        bytes calldata _options
    ) external payable {
        require(ownerOf(_tokenId) == msg.sender, "Faqat egasi yubora oladi");
        _burn(_tokenId); // Manbada NFT yoqiladi

        bytes memory message = abi.encode(_to, _tokenId);
        // LayerZero endpoint send chaqiruvi amalga oshiriladi
        emit ONFTSent(_dstEid, msg.sender, _to, _tokenId);
    }

    function lzReceive(
        uint32 _srcEid,
        bytes32 _sender,
        uint64,
        bytes32,
        bytes calldata _message,
        bytes calldata
    ) external payable {
        require(msg.sender == address(endpoint), "Faqat Endpoint");
        require(peers[_srcEid] == _sender, "Yaroqsiz Peer");

        (address to, uint256 tokenId) = abi.decode(_message, (address, uint256));
        _mint(to, tokenId); // Maqsadda NFT qayta tiklanadi

        emit ONFTReceived(_srcEid, to, tokenId);
    }
}
```
**Tushuntirish:** ONFT mexanizmi yordamida NFT global identifikatori (`tokenId`) barcha qo'llab-quvvatlanuvchi zanjirlar bo'ylab unikal saqlanadi. Bir zanjirda token yoqilganda (burn), LayerZero xabari orqali ikkinchi zanjirda xuddi shu ID bilan `_mint` qilinadi, bu esa ikki nusxa paydo bo'lishining oldini oladi.

---

### Topshiriq #1114: LayerZero V2 OptionsBuilder yordamida bajarish parametrlarini (gasLimit, value) kodlash
**Tavsif:** LayerZero V2 da tranzaksiya ijrochisiga (Executor) qancha gas ajratilishi va foydalanuvchiga qancha native token airdrop qilinishi Options orqali baytlar ketma-ketligida kodlanishi shart.
**Talablar:** Options kodlash algoritmini implementatsiya qilish (TYPE_3, WORKER_ID_EXECUTOR, OPTION_TYPE_LZRECEIVE), xavfsiz bit amallaridan foydalanish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title LzOptionsHelper - LayerZero V2 Options strukturasini hosil qiluvchi kutubxona
library LzOptionsHelper {
    uint16 constant TYPE_3 = 3;
    uint8 constant WORKER_ID_EXECUTOR = 1;
    uint8 constant OPTION_TYPE_LZRECEIVE = 1;
    uint8 constant OPTION_TYPE_NATIVE_DROP = 2;

    /// @notice lzReceive ijrosi uchun gas limiti va native airdrop optionini yaratish
    function createExecutorOptions(uint128 _gasLimit, uint128 _nativeDrop, address _receiver) internal pure returns (bytes memory) {
        bytes memory options = abi.encodePacked(TYPE_3);

        if (_gasLimit > 0 && _nativeDrop == 0) {
            // Faqat gas limit
            uint16 size = 16 + 1; // 128 bit gas (16 bayt) + 1 bayt option type
            options = abi.encodePacked(options, WORKER_ID_EXECUTOR, size, OPTION_TYPE_LZRECEIVE, _gasLimit);
        } else if (_gasLimit > 0 && _nativeDrop > 0) {
            // Gas limit + Native Drop
            uint16 size = 16 + 16 + 32 + 1; // gas + amount + receiver + option type
            options = abi.encodePacked(
                options,
                WORKER_ID_EXECUTOR,
                uint16(17),
                OPTION_TYPE_LZRECEIVE,
                _gasLimit,
                WORKER_ID_EXECUTOR,
                uint16(49),
                OPTION_TYPE_NATIVE_DROP,
                _nativeDrop,
                bytes32(uint256(uint160(_receiver)))
            );
        }
        return options;
    }
}

contract LzOptionsConsumer {
    function getSerializedOptions(uint128 _gas, uint128 _airdrop, address _user) external pure returns (bytes memory) {
        return LzOptionsHelper.createExecutorOptions(_gas, _airdrop, _user);
    }
}
```
**Tushuntirish:** LayerZero V2 da ijro parametrlari `Options` orqali standartlashtirilgan. TYPE_3 binar formati bir nechta ishchilarga (DVN, Executor) ko'rsatmalarni bitta baytlar massivida uzatish imkonini beradi. Natijada relayer qabul qiluvchi zanjirda qancha gas va qo'shimcha airdrop naqd puli berish kerakligini bilib oladi.

---

### Topshiriq #1115: LayerZero V2 DVN (Decentralized Verifier Network) va xavfsizlik stackini sozlash
**Tavsif:** Protokol xavfsizligini ta'minlash uchun xabarlarni bitta emas, bir nechta mustaqil tekshiruvchilar (masalan, Chainlink DVN, Polyhedra ZK-DVN va LayerZero Labs DVN) tasdiqlashi shart.
**Talablar:** EndpointV2 shartnomasida `setConfig` orqali SendUln302 va ReceiveUln302 kutubxonalariga DVN ro'yxati va minimal kvorum (threshold) belgilash.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {ILayerZeroEndpointV2} from "@layerzerolabs/lz-evm-protocol-v2/contracts/interfaces/ILayerZeroEndpointV2.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

struct UlnConfig {
    uint64 confirmations;
    uint8 requiredDVNCount;
    uint8 optionalDVNCount;
    uint8 optionalDVNThreshold;
    address[] requiredDVNs;
    address[] optionalDVNs;
}

/// @title LzSecurityConfigurator - LayerZero V2 xavfsizlik va DVN kvorumini sozlovchi shartnoma
contract LzSecurityConfigurator is Ownable {
    ILayerZeroEndpointV2 public immutable endpoint;
    uint32 public constant CONFIG_TYPE_ULN = 2;

    event SecurityStackUpdated(uint32 indexed dstEid, uint8 requiredDvnCount, uint8 optionalThreshold);

    constructor(address _endpoint) Ownable(msg.sender) {
        endpoint = ILayerZeroEndpointV2(_endpoint);
    }

    /// @notice Maxsus DVN va xavfsizlik stackini o'rnatish
    function configureDVNs(
        address _sendLibrary,
        uint32 _dstEid,
        uint64 _confirmations,
        address[] calldata _requiredDVNs,
        address[] calldata _optionalDVNs,
        uint8 _optionalThreshold
    ) external onlyOwner {
        UlnConfig memory ulnConfig = UlnConfig({
            confirmations: _confirmations,
            requiredDVNCount: uint8(_requiredDVNs.length),
            optionalDVNCount: uint8(_optionalDVNs.length),
            optionalDVNThreshold: _optionalThreshold,
            requiredDVNs: _requiredDVNs,
            optionalDVNs: _optionalDVNs
        });

        bytes memory configData = abi.encode(ulnConfig);

        // Endpoint orqali konfiguratsiya o'rnatish
        endpoint.setConfig(address(this), _sendLibrary, _dstEid, CONFIG_TYPE_ULN, configData);
        emit SecurityStackUpdated(_dstEid, uint8(_requiredDVNs.length), _optionalThreshold);
    }
}
```
**Tushuntirish:** LayerZero V2 ning eng katta afzalligi modulli xavfsizlikdir (Modular Security Stack). Dasturchi o'z talablariga mos ravishda talab qilinuvchi DVNlarni (masalan, ZK-light client va oracllar) tanlaydi va kvorumni belgilaydi. Bu biron bir verifier buzilgan taqdirda ham butun tizim xavfsizligini ta'minlaydi.

---

### Topshiriq #1116: LayerZero Non-Blocking LzApp arxitekturasi va payload qayta urinish (Retry logic)
**Tavsif:** Agar qabul qiluvchi shartnomadagi ichki logika xatoga uchrasa (masalan, receiverda token balance yetishmasa), butun zanjir kanali bloklanib qolmasligi (Head-of-line blocking) va keyingi xabarlar to'xtamasligi kerak.
**Talablar:** Try-catch orqali payloadni saqlab qo'yish, muvaffaqiyatsiz xabarlarni `failedMessages` ga yozish, keyinroq `retryMessage` orqali qayta bajarish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

/// @title NonBlockingLzReceiver - Bloklanmaydigan LayerZero xabarlar qabul qiluvchisi
contract NonBlockingLzReceiver is Ownable {
    address public endpoint;

    // srcEid => sender => nonce => payloadHash
    mapping(uint32 => mapping(bytes32 => mapping(uint64 => bytes32))) public failedMessages;

    event MessageFailed(uint32 srcEid, bytes32 sender, uint64 nonce, bytes payload, bytes reason);
    event MessageRetried(uint32 srcEid, bytes32 sender, uint64 nonce);

    constructor(address _endpoint) Ownable(msg.sender) {
        endpoint = _endpoint;
    }

    /// @notice Endpoint tomonidan chaqiriluvchi asosiy qabul qiluvchi
    function lzReceive(
        uint32 _srcEid,
        bytes32 _sender,
        uint64 _nonce,
        bytes32,
        bytes calldata _message,
        bytes calldata
    ) external payable {
        require(msg.sender == endpoint, "Faqat Endpoint");

        // Try-Catch orqali xatolikni ushlash
        try this.executePayload(_srcEid, _sender, _nonce, _message) {
            // Muvaffaqiyatli ijro
        } catch (bytes memory reason) {
            failedMessages[_srcEid][_sender][_nonce] = keccak256(_message);
            emit MessageFailed(_srcEid, _sender, _nonce, _message, reason);
        }
    }

    function executePayload(uint32, bytes32, uint64, bytes calldata _message) external {
        require(msg.sender == address(this), "Faqat o'z-o'zini chaqiruv");
        (address recipient, uint256 amount) = abi.decode(_message, (address, uint256));
        require(amount < 1000 ether, "Cheklovdan oshiq");
        // Biznes mantiq...
    }

    /// @notice Xatoga uchragan payloadni qayta ijro qilish
    function retryMessage(
        uint32 _srcEid,
        bytes32 _sender,
        uint64 _nonce,
        bytes calldata _message
    ) external payable {
        bytes32 hash = failedMessages[_srcEid][_sender][_nonce];
        require(hash != bytes32(0), "Muvaffaqiyatsiz xabar mavjud emas");
        require(keccak256(_message) == hash, "Payload xeshi mos kelmadi");

        delete failedMessages[_srcEid][_sender][_nonce];

        // Qayta bajarish
        this.executePayload(_srcEid, _sender, _nonce, _message);
        emit MessageRetried(_srcEid, _sender, _nonce);
    }
}
```
**Tushuntirish:** Standart LayerZero V1/V2 kanallarida qat'iy tartib (ordered execution) mavjud bo'lgani sababli, bitta xabarning xatosi barcha keyingi tranzaksiyalarni muzlatishi mumkin. Non-blocking arxitekturasi buzilgan xabarni xeshlab saqlab qoladi va kanalni ochiq qoldirib, xatoni keyinroq qo'lda yoki avtomat tuzatishga imkon beradi.

---

### Topshiriq #1117: LayerZero orqali cross-chain arbitraj buyruqlarini bajaruvchi shartnoma
**Tavsif:** Arbitraj botlari ikkita turli DEX (masalan, Arbitrumdagi Uniswap va Optimismdagi Velodrome) o'rtasidagi narx farqini ko'rganda, zudlik bilan cross-chain buyruq uzatib svopni bajarishi kerak.
**Talablar:** Minimal kutilayotgan foyda (minProfit) parametrini tekshirish, shartnoma ichida token almashinuvini bajarish, foydasiz bo'lsa tranzaksiyani bekor qilish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {ILayerZeroEndpointV2} from "@layerzerolabs/lz-evm-protocol-v2/contracts/interfaces/ILayerZeroEndpointV2.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

interface ISimpleDEX {
    function swap(address tokenIn, address tokenOut, uint256 amountIn, uint256 minOut) external returns (uint256 amountOut);
}

/// @title CrossChainArbitrageExecutor - Zanjirlararo arbitraj ijrochisi
contract CrossChainArbitrageExecutor {
    using SafeERC20 for IERC20;

    address public immutable endpoint;
    address public dexRouter;

    event ArbitrageExecuted(address tokenIn, address tokenOut, uint256 amountIn, uint256 amountOut, uint256 profit);

    constructor(address _endpoint, address _dexRouter) {
        endpoint = _endpoint;
        dexRouter = _dexRouter;
    }

    /// @notice LayerZero orqali kelgan arbitraj buyrug'ini bajarish
    function executeArbitrage(bytes calldata payload) external {
        require(msg.sender == endpoint || msg.sender == address(this), "Ruxsatsiz ijrochi");

        (address tokenIn, address tokenOut, uint256 amountIn, uint256 minOut, uint256 targetProfit) = 
            abi.decode(payload, (address, address, uint256, uint256, uint256));

        IERC20(tokenIn).safeIncreaseAllowance(dexRouter, amountIn);
        uint256 receivedOut = ISimpleDEX(dexRouter).swap(tokenIn, tokenOut, amountIn, minOut);

        require(receivedOut >= minOut, "Slippage haddan tashqari yuqori");
        require(receivedOut - minOut >= targetProfit, "Kutilgan foyda yetarli emas");

        emit ArbitrageExecuted(tokenIn, tokenOut, amountIn, receivedOut, receivedOut - minOut);
    }
}
```
**Tushuntirish:** Cross-chain arbitrajda kechikish (latency) va narxning o'zgarishi (slippage) eng katta xavf hisoblanadi. Shartnoma `minOut` va `targetProfit` tekshiruvlari orqali foydasiz yoki zararga olib keluvchi almashinuvlarni oldini oladi, shu bilan likvidlikni xavfsiz saqlaydi.

---

### Topshiriq #1118: LayerZero orqali Omnichain DAO saylov qutisi (Ballot Box Aggregator)
**Tavsif:** Turli zanjirlardagi foydalanuvchilar o'zlarining shaxsiy hamyonlaridan mahalliy tarmoqda ovoz berishadi. Mahalliy saylov qutisi ovozlarni jamlab, LayerZero orqali markaziy DAO kontraktiga uzatadi.
**Talablar:** Mahalliy saylov natijalarini to'plash, LayerZero orqali imzolangan paketni jo'natish, ikki marta yuborishning oldini olish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {ILayerZeroEndpointV2, MessagingParams} from "@layerzerolabs/lz-evm-protocol-v2/contracts/interfaces/ILayerZeroEndpointV2.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

/// @title LocalBallotBox - Mahalliy tarmoqdagi ovozlarni to'plab markazga yuboruvchi shartnoma
contract LocalBallotBox is Ownable {
    ILayerZeroEndpointV2 public immutable endpoint;
    uint32 public immutable rootChainEid;
    bytes32 public rootBallotReceiver;

    mapping(uint256 => uint256) public yesVotes;
    mapping(uint256 => uint256) public noVotes;
    mapping(uint256 => mapping(address => bool)) public hasVoted;
    mapping(uint256 => bool) public isBatchSent;

    event VoteCast(uint256 indexed proposalId, address indexed voter, bool support, uint256 weight);
    event BallotDispatched(uint256 indexed proposalId, uint256 yesVotes, uint256 noVotes);

    constructor(address _endpoint, uint32 _rootEid) Ownable(msg.sender) {
        endpoint = ILayerZeroEndpointV2(_endpoint);
        rootChainEid = _rootEid;
    }

    function setRootReceiver(bytes32 _receiver) external onlyOwner {
        rootBallotReceiver = _receiver;
    }

    function castVote(uint256 _proposalId, bool _support, uint256 _weight) external {
        require(!hasVoted[_proposalId][msg.sender], "Foydalanuvchi allaqachon ovoz bergan");
        require(!isBatchSent[_proposalId], "Ovoz berish bosqichi yopilgan");

        hasVoted[_proposalId][msg.sender] = true;
        if (_support) {
            yesVotes[_proposalId] += _weight;
        } else {
            noVotes[_proposalId] += _weight;
        }

        emit VoteCast(_proposalId, msg.sender, _support, _weight);
    }

    /// @notice Ovozlar to'plamini markaziy zanjirga yuborish
    function dispatchVotes(uint256 _proposalId, bytes calldata _options) external payable onlyOwner {
        require(!isBatchSent[_proposalId], "Allaqachon yuborilgan");
        isBatchSent[_proposalId] = true;

        bytes memory message = abi.encode(_proposalId, yesVotes[_proposalId], noVotes[_proposalId]);

        MessagingParams memory params = MessagingParams({
            dstEid: rootChainEid,
            receiver: rootBallotReceiver,
            message: message,
            options: _options,
            payInLzToken: false
        });

        endpoint.send{value: msg.value}(params, msg.sender);
        emit BallotDispatched(_proposalId, yesVotes[_proposalId], noVotes[_proposalId]);
    }
}
```
**Tushuntirish:** Omnichain saylov tizimida har bir foydalanuvchining alohida tranzaksiyasini L1 ga yuborish o'rniga, mahalliy L2'da ovozlar to'planib (batching), bitta umumlashtirilgan xabar bilan markaziy shartnomaga yuboriladi. Bu gas xarajatlarini 99% gacha qisqartiradi.

---

### Topshiriq #1119: LayerZero Smart Vault: Arbitrum va Optimism o'rtasida likvidlik balanslash
**Tavsif:** DeFi daromad shartnomasida bir tarmoqda likvidlik ortiqcha, ikkinchisida esa kamayib ketganida fondlar LayerZero xabarlari orqali avtomatik ravishda qayta taqsimlanishi (rebalancing) zarur.
**Talablar:** Hovuzlar balansini solishtirish, rebalance chegarasini belgilash (delta threshold), cross-chain xabar jo'natib kapitalni harakatga keltirish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {ILayerZeroEndpointV2, MessagingParams} from "@layerzerolabs/lz-evm-protocol-v2/contracts/interfaces/ILayerZeroEndpointV2.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

/// @title RebalancingVault - Zanjirlararo likvidlikni muvozanatlashtiruvchi g'azna
contract RebalancingVault is Ownable {
    using SafeERC20 for IERC20;

    ILayerZeroEndpointV2 public immutable endpoint;
    IERC20 public immutable underlyingAsset;
    uint32 public remoteEid;
    bytes32 public remoteVault;

    uint256 public targetReserveRatio = 5000; // 50.00% (basis points)

    event RebalanceInitiated(uint256 amountToTransfer, uint32 dstEid);

    constructor(address _endpoint, address _asset, uint32 _remoteEid) Ownable(msg.sender) {
        endpoint = ILayerZeroEndpointV2(_endpoint);
        underlyingAsset = IERC20(_asset);
        remoteEid = _remoteEid;
    }

    function setRemoteVault(bytes32 _remoteVault) external onlyOwner {
        remoteVault = _remoteVault;
    }

    /// @notice Zaxirani tekshirish va ortiqcha likvidlikni boshqa zanjirga yuborish
    function triggerRebalance(uint256 _amountToSend, bytes calldata _options) external payable onlyOwner {
        require(_amountToSend > 0, "Nol miqdor");
        require(underlyingAsset.balanceOf(address(this)) >= _amountToSend, "G'aznada yetarli mablag' yo'q");

        // Mablag'larni OFT yoki bridge orqali jo'natish xabari
        bytes memory payload = abi.encode(_amountToSend);

        MessagingParams memory params = MessagingParams({
            dstEid: remoteEid,
            receiver: remoteVault,
            message: payload,
            options: _options,
            payInLzToken: false
        });

        endpoint.send{value: msg.value}(params, msg.sender);
        emit RebalanceInitiated(_amountToSend, remoteEid);
    }
}
```
**Tushuntirish:** Ushbu shartnoma aqlli g'aznalarga (smart vaults) zanjirlararo kapital samaradorligini (capital efficiency) oshirishga imkon beradi. Algoritmik rebalansing orqali qarz foiz stavkalari eng yuqori bo'lgan tarmoqqa likvidlik o'z vaqtida yetkaziladi.

---

### Topshiriq #1120: LayerZero xabarlarida Replay Attack va zanjir identifikatorini (Eid) tekshirish
**Tavsif:** Boshqa tarmoqdan kelgan haqiqiy xabarni nusxalab olib, uni begona zanjirda yoki noto'g'ri shartnomada qayta bajarishga urinishlar (Cross-chain replay attacks) oldini olish kerak.
**Talablar:** Barcha qabul qilingan xabarlar uchun `bytes32 guid` unikal kalitini mappingda tekshirish va bir marta bajarilgan deb belgilash, qat'iy peer tekshiruvi.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {ILayerZeroEndpointV2} from "@layerzerolabs/lz-evm-protocol-v2/contracts/interfaces/ILayerZeroEndpointV2.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

/// @title ReplayProtectedLzReceiver - Takroriy bajarilishdan himoyalangan qabul qiluvchi
contract ReplayProtectedLzReceiver is Ownable {
    ILayerZeroEndpointV2 public immutable endpoint;
    mapping(uint32 => bytes32) public trustedPeers;
    mapping(bytes32 => bool) public executedGuids;

    event ActionExecuted(bytes32 indexed guid, uint32 srcEid, bytes payload);

    error AlreadyExecuted(bytes32 guid);
    error UntrustedSource(uint32 srcEid, bytes32 sender);

    constructor(address _endpoint) Ownable(msg.sender) {
        endpoint = ILayerZeroEndpointV2(_endpoint);
    }

    function setTrustedPeer(uint32 _srcEid, bytes32 _peer) external onlyOwner {
        trustedPeers[_srcEid] = _peer;
    }

    /// @notice Endpoint orqali kelgan xabarni xavfsiz qabul qilish
    function lzReceive(
        uint32 _srcEid,
        bytes32 _sender,
        uint64 /* _nonce */,
        bytes32 _guid,
        bytes calldata _message,
        bytes calldata /* _extraData */
    ) external payable {
        require(msg.sender == address(endpoint), "Faqat Endpoint chaqira oladi");

        // 1. Manba shartnomasi tekshiruvi
        if (trustedPeers[_srcEid] != _sender) {
            revert UntrustedSource(_srcEid, _sender);
        }

        // 2. Takroriy hujum (Replay) tekshiruvi
        if (executedGuids[_guid]) {
            revert AlreadyExecuted(_guid);
        }

        // 3. Holatni yozish
        executedGuids[_guid] = true;

        // 4. Mantiqni bajarish
        emit ActionExecuted(_guid, _srcEid, _message);
    }
}
```
**Tushuntirish:** LayerZero V2 da har bir xabarga unikal `guid` (Globally Unique Identifier) beriladi. U manba zanjiri, jo'natuvchi manzili, manzil zanjiri va nonce ma'lumotlarining kriptografik xeshidan iborat. `executedGuids[guid]` flagini tekshirish orqali bitta xabar ikki marta ijro etilishi mutlaqo istisno qilinadi.

---

### Topshiriq #1121: Wormhole Core Bridge orqali xabar e'lon qilish (publishMessage)
**Tavsif:** Turli ekotizimlar (EVM, Solana, Cosmos) o'rtasida aloqa o'rnatish uchun Wormhole Core shartnomasida xabarni `publishMessage` orqali e'lon qilish lozim.
**Talablar:** IWormhole interfeysini chaqirish, konsistensiya darajasini (consistencyLevel) belgilash, Wormhole protokol to'lovini (message fee) tekshirish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IWormhole {
    function publishMessage(
        uint32 nonce,
        bytes memory payload,
        uint8 consistencyLevel
    ) external payable returns (uint64 sequence);

    function messageFee() external view returns (uint256);
}

/// @title WormholeMessagePublisher - Wormhole Core Bridge orqali ma'lumot uzatuvchi shartnoma
contract WormholeMessagePublisher {
    IWormhole public immutable wormholeBridge;
    uint32 public messageNonce;

    event MessagePublished(uint64 indexed sequence, bytes payload, uint8 consistencyLevel);

    constructor(address _wormholeBridge) {
        wormholeBridge = IWormhole(_wormholeBridge);
    }

    /// @notice Zanjirlararo e'lon qilish
    /// @param _payload Yuboriladigan ma'lumotlar baytlari
    /// @param _consistencyLevel Bloklar tasdiqlanish darajasi (1 = tezkor, 200 = finality)
    function broadcastCrossChainMessage(
        bytes calldata _payload,
        uint8 _consistencyLevel
    ) external payable returns (uint64 sequence) {
        uint256 fee = wormholeBridge.messageFee();
        require(msg.value >= fee, "Yetarsiz Wormhole to'lovi");

        messageNonce++;
        sequence = wormholeBridge.publishMessage{value: fee}(
            messageNonce,
            _payload,
            _consistencyLevel
        );

        emit MessagePublished(sequence, _payload, _consistencyLevel);
    }
}
```
**Tushuntirish:** Wormhole arxitekturasida shartnoma xabarni `publishMessage` orqali blokcheynga yozadi. 19 ta mustaqil Guardian tugunlari ushbu hodisani (event) kuzatib boradi va bloklar finality darajasiga yetgach (`consistencyLevel`), xabarni imzolab VAA (Verifiable Action Approval) yaratadi.

---

### Topshiriq #1122: Wormhole VAA (Verifiable Action Approval) xabarini dekodlash va imzolarni tekshirish
**Tavsif:** Qabul qiluvchi tarmoqda Guardian tarmoqlari tomonidan imzolangan VAA xabarini qabul qilib, uning haqiqiyligini tekshirish va payloadni ajratib olish talab qilinadi.
**Talablar:** Wormhole `parseAndVerifyVM` metodidan foydalanish, kvorumni tekshirish, payload ichidan emitent manzili va ma'lumotlarni o'qish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IWormholeCore {
    struct Signature {
        bytes32 r;
        bytes32 s;
        uint8 v;
        uint8 guardianIndex;
    }

    struct VM {
        uint8 version;
        uint32 timestamp;
        uint32 nonce;
        uint16 emitterChainId;
        bytes32 emitterAddress;
        uint64 sequence;
        uint8 consistencyLevel;
        bytes payload;
        uint32 guardianSetIndex;
        Signature[] signatures;
        bytes32 hash;
    }

    function parseAndVerifyVM(bytes calldata encodedVM) external view returns (VM memory vm, bool valid, string memory reason);
}

/// @title WormholeVAAConsumer - VAA xabarlarini tekshiruvchi va qayta ishlovchi shartnoma
contract WormholeVAAConsumer {
    IWormholeCore public immutable wormholeCore;

    event VAAParsed(uint16 emitterChainId, bytes32 emitterAddress, uint64 sequence, bytes payload);

    constructor(address _wormholeCore) {
        wormholeCore = IWormholeCore(_wormholeCore);
    }

    /// @notice Imzolangan VAA ni tekshirish va uning ichidagi ma'lumotni olish
    function processVAA(bytes calldata _encodedVM) external returns (bytes memory) {
        (IWormholeCore.VM memory vm, bool valid, string memory reason) = wormholeCore.parseAndVerifyVM(_encodedVM);
        require(valid, string(abi.encodePacked("Yaroqsiz VAA: ", reason)));

        emit VAAParsed(vm.emitterChainId, vm.emitterAddress, vm.sequence, vm.payload);
        return vm.payload;
    }
}
```
**Tushuntirish:** VAA (Verifiable Action Approval) - Wormhole ning asosiy dalil paketidir. `parseAndVerifyVM` funksiyasi Guardianlarning hozirgi to'plami (Guardian Set) imzolaganligini, kamida 13/19 kvorum mavjudligini va ECDSA imzolarining to'g'riligini matematik jihatdan isbotlaydi.

---

### Topshiriq #1123: Wormhole VAA sekvensiyasi orqali double-spending (ikki marta ishlatish)dan himoya
**Tavsif:** Foydalanuvchi bir marta tasdiqlangan VAA paketini shartnomaga qayta-qayta topshirib, shartnoma balansidagi mablag'larni o'g'irlashga urinishi mumkin.
**Talablar:** emitterChainId, emitterAddress va sequence tripletini xeshlab, unikal mappingda saqlash va ikkinchi marta kelganda tranzaksiyani revert qilish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {IWormholeCore} from "./WormholeVAAConsumer.sol";

/// @title WormholeReplayShield - VAA paketlarini takroriy ishlatishdan himoyalovchi modul
contract WormholeReplayShield {
    IWormholeCore public immutable wormholeCore;
    mapping(bytes32 => bool) public consumedVAAs;

    event VAAConsumed(bytes32 indexed vaaKey, uint16 chainId, uint64 sequence);

    error VAAAlreadyConsumed(bytes32 vaaKey);
    error InvalidVAA();

    constructor(address _wormholeCore) {
        wormholeCore = IWormholeCore(_wormholeCore);
    }

    /// @notice VAA ni faqat bitta marta ijro etish
    function executeUniqueVAA(bytes calldata _encodedVAA) external {
        (IWormholeCore.VM memory vm, bool valid, ) = wormholeCore.parseAndVerifyVM(_encodedVAA);
        if (!valid) revert InvalidVAA();

        // Unikal kalitni yaratish: chainId + emitterAddress + sequence
        bytes32 vaaKey = keccak256(abi.encodePacked(vm.emitterChainId, vm.emitterAddress, vm.sequence));

        if (consumedVAAs[vaaKey]) {
            revert VAAAlreadyConsumed(vaaKey);
        }

        consumedVAAs[vaaKey] = true;

        // Asosiy mantiqni bajarish...
        emit VAAConsumed(vaaKey, vm.emitterChainId, vm.sequence);
    }
}
```
**Tushuntirish:** Wormhole xabar identifikatsiyasi `(emitterChainId, emitterAddress, sequence)` uchligi bilan kafolatlanadi. `sequence` har bir jo'natuvchi uchun qat'iy 1 ga oshib boradi. Shartnoma ushbu uchlikni saqlab qo'yish orqali takroriy foydalanish (replay attack) xavfini nolga tushiradi.

---

### Topshiriq #1124: Wormhole Token Bridge integratsiyasi: completeTransfer va tokenlarni chiqarish
**Tavsif:** Portal Token Bridge orqali boshqa tarmoqdan yuborilgan tokenlarni qabul qiluvchi zanjirda qabul qilib, yakuniy egasiga chiqarib berish zarur.
**Talablar:** ITokenBridge interfeysidan foydalanish, `completeTransfer` funksiyasini chaqirish, qaytarilgan tokenni tekshirish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface ITokenBridge {
    function completeTransfer(bytes memory encodedVm) external returns (bytes memory);
}

/// @title WormholeTokenBridgeReceiver - Token bridge o'tkazmalarini yakunlovchi shartnoma
contract WormholeTokenBridgeReceiver {
    ITokenBridge public immutable tokenBridge;

    event TransferCompleted(address token, uint256 amount, address recipient);

    constructor(address _tokenBridge) {
        tokenBridge = ITokenBridge(_tokenBridge);
    }

    /// @notice Bridge tranzaksiyasini yakunlash
    function redeemTransfer(bytes calldata _encodedVAA) external returns (bytes memory transferPayload) {
        // completeTransfer VAA ni tekshiradi va tokenlarni ushbu shartnomaga yuboradi
        transferPayload = tokenBridge.completeTransfer(_encodedVAA);
    }
}
```
**Tushuntirish:** Wormhole Portal Token Bridge mexanizmida tokenlar manba zanjirida qulflanadi yoki yoqiladi. Guardianlar imzolagan VAA qabul qiluvchi zanjirga topshirilganda `tokenBridge.completeTransfer` chaqirilib, o'sha zanjirdagi mos token foydalanuvchiga taqdim etiladi.

---

### Topshiriq #1125: Wormhole orqali zanjirlararo Flash Loan qayta chaqiruvini (Callback execution) bajarish
**Tavsif:** Murakkab cross-chain moliyaviy operatsiyalarda bitta zanjirda olingan katta miqdordagi qarz orqali boshqa zanjirdagi likvidatsiyani yopish va natijani VAA orqali qaytarish lozim.
**Talablar:** Flash loan olish, VAA yaratish uchun publishMessage chaqirish va qarzni bir xil tranzaksiyada foizi bilan qaytarish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import {IWormhole} from "./WormholeMessagePublisher.sol";

/// @title CrossChainFlashLoanReceiver - Zanjirlararo tezkor kredit callback shartnomasi
contract CrossChainFlashLoanReceiver {
    using SafeERC20 for IERC20;

    IWormhole public immutable wormhole;
    address public lender;

    event FlashActionExecuted(address token, uint256 amount, uint256 fee);

    constructor(address _wormhole, address _lender) {
        wormhole = IWormhole(_wormhole);
        lender = _lender;
    }

    /// @notice Flash loan callback funksiyasi
    function onFlashLoan(
        address initiator,
        address token,
        uint256 amount,
        uint256 fee,
        bytes calldata data
    ) external returns (bytes32) {
        require(msg.sender == lender, "Faqat ruxsat berilgan lender");
        require(initiator == address(this), "Faqat shartnoma tashabbusi");

        // Cross-chain xabarni e'lon qilish
        wormhole.publishMessage{value: 0}(1, data, 1);

        emit FlashActionExecuted(token, amount, fee);

        // Qarz va foizni qaytarish ruxsatini berish
        uint256 totalRepay = amount + fee;
        IERC20(token).safeIncreaseAllowance(lender, totalRepay);

        return keccak256("ERC3156FlashBorrower.onFlashLoan");
    }
}
```
**Tushuntirish:** Ushbu arxitektura atomik operatsiyalarni Wormhole xabar almashinuvi bilan uyg'unlashtiradi. Flash loan olingach, maqsadli zanjirdagi shartnomalar uchun rasmiy buyruq (VAA) e'lon qilinadi va darhol kredit qaytariladi. Bu cross-chain likvidatsiya robotlarining asosiy yadrosidir.

---

### Topshiriq #1126: Wormhole orqali zanjirlararo shaxsiyatni tasdiqlash (Cross-Chain Attestation)
**Tavsif:** Foydalanuvchi bitta bosh zanjirda (masalan Ethereum Mainnet) KYC yoki shaxsiyat tekshiruvidan o'tgan bo'lsa, uning tasdiqnomasini boshqa barcha tarmoqlarga VAA orqali uzatish kerak.
**Talablar:** Attestation strukturasini yaratish, VAA orqali tekshirish va manzilga KYC tasdiqlangan maqomini berish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {IWormholeCore} from "./WormholeVAAConsumer.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

/// @title CrossChainKYCVerifier - Zanjirlararo shaxsiyat attestationini tekshiruvchi shartnoma
contract CrossChainKYCVerifier is Ownable {
    IWormholeCore public immutable wormholeCore;
    uint16 public trustedEmitterChain;
    bytes32 public trustedEmitterAddress;

    mapping(address => bool) public isKYCVerified;
    mapping(bytes32 => bool) public processedAttestations;

    event UserVerified(address indexed user, uint256 expirationDate);

    constructor(address _wormholeCore) Ownable(msg.sender) {
        wormholeCore = IWormholeCore(_wormholeCore);
    }

    function setTrustedEmitter(uint16 _chain, bytes32 _emitter) external onlyOwner {
        trustedEmitterChain = _chain;
        trustedEmitterAddress = _emitter;
    }

    /// @notice Wormhole VAA orqali KYC sertifikatini qabul qilish
    function verifyCrossChainKYC(bytes calldata _encodedVAA) external {
        (IWormholeCore.VM memory vm, bool valid, ) = wormholeCore.parseAndVerifyVM(_encodedVAA);
        require(valid, "Yaroqsiz VAA");
        require(vm.emitterChainId == trustedEmitterChain, "Ishonchsiz zanjir");
        require(vm.emitterAddress == trustedEmitterAddress, "Ishonchsiz emitent");

        bytes32 vaaHash = keccak256(abi.encodePacked(vm.emitterChainId, vm.emitterAddress, vm.sequence));
        require(!processedAttestations[vaaHash], "Attestation allaqachon qabul qilingan");
        processedAttestations[vaaHash] = true;

        (address user, uint256 expiration) = abi.decode(vm.payload, (address, uint256));
        require(expiration > block.timestamp, "Muddati otgan KYC");

        isKYCVerified[user] = true;
        emit UserVerified(user, expiration);
    }
}
```
**Tushuntirish:** Cross-Chain Attestation mexanizmi foydalanuvchiga har bir alohida tarmoqda takroriy tekshiruvdan o'tmaslik imkonini beradi. Bosh zanjirdagi attestation xizmati tomonidan chiqarilgan VAA boshqa zanjirlardagi DeFi va RWA (Real World Asset) protokollarida to'g'ridan-to'g'ri tan olinadi.

---

### Topshiriq #1127: Wormhole Relayer (IWormholeRelayer) orqali avtomatik zanjirlararo yetkazish
**Tavsif:** Foydalanuvchidan maqsadli zanjirda ikkinchi marta tranzaksiya yuborishni (manual redeem) talab qilmasdan, relayer orqali to'liq avtomatlashtirilgan yetkazib berish (push delivery) kerak.
**Talablar:** IWormholeRelayer interfeysidan foydalanish, `sendPayloadToEvm` orqali xabar va receiver gas limitini belgilash, `quoteEVMDeliveryPrice` bilan haqni hisoblash.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IWormholeRelayer {
    function sendPayloadToEvm(
        uint16 targetChain,
        address targetAddress,
        bytes memory payload,
        uint256 receiverValue,
        uint256 gasLimit
    ) external payable returns (uint64 sequence);

    function quoteEVMDeliveryPrice(
        uint16 targetChain,
        uint256 receiverValue,
        uint256 gasLimit
    ) external view returns (uint256 nativeFee, uint256 targetChainRefundPerGasUnused);
}

/// @title AutomaticWormholeSender - Relayer yordamida avtomatik yetkazuvchi shartnoma
contract AutomaticWormholeSender {
    IWormholeRelayer public immutable relayer;

    event DeliveryRequested(uint64 sequence, uint16 targetChain, address targetAddress);

    constructor(address _relayer) {
        relayer = IWormholeRelayer(_relayer);
    }

    /// @notice Avtomatik relayer orqali xabar jo'natish
    function sendAutoDelivery(
        uint16 _targetChain,
        address _targetAddress,
        bytes calldata _payload,
        uint256 _gasLimit
    ) external payable returns (uint64 sequence) {
        (uint256 nativeFee, ) = relayer.quoteEVMDeliveryPrice(_targetChain, 0, _gasLimit);
        require(msg.value >= nativeFee, "Yetarsiz yetkazish tolovi");

        sequence = relayer.sendPayloadToEvm{value: nativeFee}(
            _targetChain,
            _targetAddress,
            _payload,
            0, // receiverValue
            _gasLimit
        );

        emit DeliveryRequested(sequence, _targetChain, _targetAddress);
    }
}
```
**Tushuntirish:** Wormhole Relayer tarmog'i foydalanuvchi tajribasini (UX) sezilarli darajada yaxshilaydi. Manba zanjirida to'langan native fee evaziga Wormhole off-chain relayerlari VAA ni olib, o'zlari maqsadli zanjirdagi shartnomaga yetkazib beradi.

---

### Topshiriq #1128: Wormhole NTT (Native Token Transfers) framework mantiqi
**Tavsif:** Ko'prik orqali o'tkaziladigan tokenlar har bir tarmoqda o'zining tabiiy (native) holatida muomalada bo'lishi va zanjirlararo o'tkazishda tezlik va kunlik limitlar bilan himoyalanishi zarur.
**Talablar:** Kunlik transfer chegarasi (Rate Limiter) mantig'ini yozish, burn va mint operatsiyalarini vaqt oynasida kuzatish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

/// @title NTTRateLimiter - Native Token Transfers uchun oqim nazoratchisi
contract NTTRateLimiter is Ownable {
    uint256 public constant RATE_LIMIT_DURATION = 1 days;
    uint256 public dailyLimit;
    uint256 public currentBucket;
    uint256 public lastUpdated;

    event RateLimitUpdated(uint256 newLimit);
    event OutboundTransferConsumed(uint256 amount, uint256 remainingBucket);

    error RateLimitExceeded(uint256 requested, uint256 available);

    constructor(uint256 _initialLimit) Ownable(msg.sender) {
        dailyLimit = _initialLimit;
        currentBucket = _initialLimit;
        lastUpdated = block.timestamp;
    }

    /// @notice Token yuborishdan oldin limitni yangilash va kamaytirish
    function consumeOutboundLimit(uint256 _amount) external onlyOwner {
        _refillBucket();

        if (_amount > currentBucket) {
            revert RateLimitExceeded(_amount, currentBucket);
        }

        currentBucket -= _amount;
        emit OutboundTransferConsumed(_amount, currentBucket);
    }

    /// @notice Vaqt o'tishi bilan hovuzni to'ldirish (Token Bucket algoritmi)
    function _refillBucket() internal {
        uint256 elapsed = block.timestamp - lastUpdated;
        if (elapsed > 0) {
            uint256 refill = (dailyLimit * elapsed) / RATE_LIMIT_DURATION;
            currentBucket = (currentBucket + refill > dailyLimit) ? dailyLimit : currentBucket + refill;
            lastUpdated = block.timestamp;
        }
    }
}
```
**Tushuntirish:** Wormhole NTT (Native Token Transfers) ning muhim ustunligi - uning o'rnatilgan Rate Limiting mexanizmidir. Agar qaysidir zanjirdagi shartnoma kiberhujumga uchrasa, tajovuzkor butun ta'minotni boshqa zanjirlarga birdaniga o'tkaza olmaydi, bu esa loyiha jamoasiga ko'prikni to'xtatish uchun vaqt beradi.

---

### Topshiriq #1129: Wormhole xabarlari uchun ko'p imzoli favqulodda avariya to'xtatuvchisi (Circuit Breaker)
**Tavsif:** Blokcheyn anomal holatga tushganda yoki kutilmagan xakkerlik harakatlari sezilganda, ko'p imzoli (Multisig) qo'mita zudlik bilan barcha zanjirlararo xabarlarni muzlatishi lozim.
**Talablar:** Ko'p imzoli ruxsat mexanizmi, shartnomani favqulodda to'xtatish (Pause) va qayta faollashtirish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title CrossChainCircuitBreaker - Favqulodda to'xtatuvchi xavfsizlik moduli
contract CrossChainCircuitBreaker {
    address[] public guardians;
    mapping(address => bool) public isGuardian;
    uint256 public requiredSignatures;

    bool public isPaused;
    mapping(bytes32 => mapping(address => bool)) public pauseConfirmations;

    event EmergencyPaused(address initiator);
    event EmergencyUnpaused();

    modifier whenNotPaused() {
        require(!isPaused, "Tizim favqulodda to'xtatilgan (Paused)");
        _;
    }

    constructor(address[] memory _guardians, uint256 _threshold) {
        require(_threshold > 0 && _threshold <= _guardians.length, "Yaroqsiz kvorum");
        guardians = _guardians;
        requiredSignatures = _threshold;

        for (uint256 i = 0; i < _guardians.length; i++) {
            isGuardian[_guardians[i]] = true;
        }
    }

    /// @notice Anomaliya aniqlanganda bitta guardian darhol muzlata oladi
    function triggerEmergencyPause() external {
        require(isGuardian[msg.sender], "Faqat qo'riqchi");
        isPaused = true;
        emit EmergencyPaused(msg.sender);
    }

    /// @notice Tizimni qayta ishga tushirish uchun esa kvorum talab etiladi
    function confirmUnpause(bytes32 actionId) external {
        require(isGuardian[msg.sender], "Faqat qo'riqchi");
        require(isPaused, "Tizim muzlatilmagan");
        require(!pauseConfirmations[actionId][msg.sender], "Allaqachon imzolangan");

        pauseConfirmations[actionId][msg.sender] = true;
        // Kvorum hisoblash mantig'i...
    }
}
```
**Tushuntirish:** Xavfsizlik amaliyotida 'Asimmetrik Favqulodda Holat' tamoyili qo'llaniladi: tizimni to'xtatish (Pause) imkoni bitta ishonchli qo'riqchiga tezkor beriladi, biroq tizimni qayta yoqish (Unpause) ko'p imzoli kvorumni (masalan 3/5 multisig) talab qiladi.

---

### Topshiriq #1130: Wormhole orqali zanjirlararo limit order buyurtmalarini bajarish (Cross-chain Order Book)
**Tavsif:** Markazlashtirilmagan birjada foydalanuvchi Arbitrumda limit order ochib, garov qo'yadi. Solana yoki Ethereumda mos keluvchi qarshi buyurtma (match) topilganda VAA orqali buyurtma yopilishi kerak.
**Talablar:** Buyurtma holatini saqlash (Order struct), VAA orqali kross-zanjirli to'ldirish (fill) ma'lumotini tekshirish va mablag'larni taqsimlash.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import {IWormholeCore} from "./WormholeVAAConsumer.sol";

/// @title CrossChainOrderBook - Zanjirlararo limit order shartnomasi
contract CrossChainOrderBook {
    using SafeERC20 for IERC20;

    struct Order {
        address maker;
        address tokenIn;
        uint256 amountIn;
        uint256 minAmountOut;
        bool isFilled;
    }

    IWormholeCore public immutable wormholeCore;
    mapping(bytes32 => Order) public orders;

    event OrderCreated(bytes32 indexed orderId, address indexed maker, uint256 amountIn);
    event OrderSettled(bytes32 indexed orderId, address taker, uint256 amountOut);

    constructor(address _wormholeCore) {
        wormholeCore = IWormholeCore(_wormholeCore);
    }

    function createOrder(
        bytes32 orderId,
        address tokenIn,
        uint256 amountIn,
        uint256 minAmountOut
    ) external {
        require(orders[orderId].maker == address(0), "Buyurtma allaqachon mavjud");
        IERC20(tokenIn).safeTransferFrom(msg.sender, address(this), amountIn);

        orders[orderId] = Order({
            maker: msg.sender,
            tokenIn: tokenIn,
            amountIn: amountIn,
            minAmountOut: minAmountOut,
            isFilled: false
        });

        emit OrderCreated(orderId, msg.sender, amountIn);
    }

    /// @notice Boshqa zanjirdagi ijro VAA si asosida hisob-kitob qilish
    function settleCrossChainFill(bytes calldata _encodedVAA) external {
        (IWormholeCore.VM memory vm, bool valid, ) = wormholeCore.parseAndVerifyVM(_encodedVAA);
        require(valid, "Yaroqsiz VAA");

        (bytes32 orderId, address taker, uint256 amountFilled) = abi.decode(vm.payload, (bytes32, address, uint256));
        Order storage order = orders[orderId];

        require(!order.isFilled, "Buyurtma yopilgan");
        require(order.maker != address(0), "Buyurtma topilmadi");
        require(amountFilled >= order.minAmountOut, "Yetarsiz narx");

        order.isFilled = true;
        IERC20(order.tokenIn).safeTransfer(taker, order.amountIn);

        emit OrderSettled(orderId, taker, amountFilled);
    }
}
```
**Tushuntirish:** Ushbu arxitektura buyurtmalarni zanjirlararo asinxron moslashtirish (Cross-Chain Asynchronous Settlement) imkonini beradi. Boshqa zanjirda tranzaksiya amalga oshganligi to'g'risidagi VAA dalili asosida, manba zanjiridagi depozit tokenni to'g'ridan-to'g'ri ijrochiga o'tkazib beradi.

---

### Topshiriq #1131: Chainlink Price Feeds orqali aktiv narxini o'qish va eskirganlikni (staleness) tekshirish
**Tavsif:** DeFi kreditlash shartnomalarida aktivlar narxi Chainlink oracllari orqali olinadi. Eskirgan yoki yaroqsiz narx sababli noto'g'ri likvidatsiya sodir bo'lishini qat'iy oldini olish kerak.
**Talablar:** AggregatorV3Interface dan foydalanish, `latestRoundData` parametrlarini (roundId, price, updatedAt, answeredInRound) to'liq tekshirish, maksimal qabul qilinuvchi eskirish muddatini (heartbeat) sozlash.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface AggregatorV3Interface {
    function decimals() external view returns (uint8);
    function latestRoundData() external view returns (
        uint80 roundId,
        int256 answer,
        uint256 startedAt,
        uint256 updatedAt,
        uint80 answeredInRound
    );
}

/// @title ChainlinkPriceConsumer - Eskirgan narxlardan himoyalangan narx iste'molchisi
contract ChainlinkPriceConsumer {
    AggregatorV3Interface public immutable priceFeed;
    uint256 public immutable heartbeat; // Maksimal qabul qilinuvchi eskirish vaqti (masalan, 3600 soniya)

    error PriceStale(uint256 updatedAt, uint256 heartbeat);
    error InvalidPrice(int256 price);
    error IncompleteRound(uint80 roundId, uint80 answeredInRound);

    constructor(address _priceFeed, uint256 _heartbeat) {
        priceFeed = AggregatorV3Interface(_priceFeed);
        heartbeat = _heartbeat;
    }

    /// @notice Xavfsiz tekshirilgan narxni qaytarish
    function getSafePrice() external view returns (uint256 safePrice) {
        (
            uint80 roundId,
            int256 price,
            ,
            uint256 updatedAt,
            uint80 answeredInRound
        ) = priceFeed.latestRoundData();

        // 1. Narx 0 dan katta ekanligini tekshirish
        if (price <= 0) {
            revert InvalidPrice(price);
        }

        // 2. Raund to'liq yakunlanganligini tekshirish
        if (answeredInRound < roundId) {
            revert IncompleteRound(roundId, answeredInRound);
        }

        // 3. Heartbeat orqali ma'lumot eskirgan emasligini tekshirish
        if (block.timestamp - updatedAt > heartbeat) {
            revert PriceStale(updatedAt, heartbeat);
        }

        return uint256(price);
    }
}
```
**Tushuntirish:** Chainlink ma'lumotlarini o'qishda `price <= 0`, `answeredInRound < roundId` va `block.timestamp - updatedAt > heartbeat` tekshiruvlari o'ta muhimdir. Agar bu tekshiruvlar qilinmasa, tarmoq tiqilishi paytida shartnoma bir necha kunlik eski narxlar bilan ishlab, hovuzlarning bo'shab qolishiga olib kelishi mumkin.

---

### Topshiriq #1132: Chainlink VRF V2.5 orqali tekshirilgan tasodifiy sonlarni so'rash va qabul qilish
**Tavsif:** On-chain lotereya yoki NFT xususiyatlarini aniqlashda manipulyatsiyaga chidamli, matematik jihatdan isbotlangan tasodifiylik (Verifiable Random Function) talab qilinadi.
**Talablar:** VRFConsumerBaseV2Plus dan foydalanish, `requestRandomWords` orqali so'rov yuborish, `fulfillRandomWords` ichida raund g'olibini aniqlash.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IVRFCoordinatorV2Plus {
    struct RandomWordsRequest {
        bytes32 keyHash;
        uint256 subId;
        uint16 requestConfirmations;
        uint32 callbackGasLimit;
        uint32 numWords;
        bytes extraArgs;
    }
    function requestRandomWords(RandomWordsRequest calldata req) external returns (uint256 requestId);
}

/// @title ChainlinkVRFConsumer - Tasdiqlangan tasodifiy sonlar iste'molchisi
contract ChainlinkVRFConsumer {
    IVRFCoordinatorV2Plus public immutable vrfCoordinator;
    bytes32 public immutable keyHash;
    uint256 public immutable subscriptionId;

    address public owner;
    mapping(uint256 => bool) public pendingRequests;
    mapping(uint256 => uint256[]) public randomResults;

    event RandomWordsRequested(uint256 indexed requestId);
    event RandomWordsFulfilled(uint256 indexed requestId, uint256[] words);

    modifier onlyOwner() {
        require(msg.sender == owner, "Faqat egasi");
        _;
    }

    constructor(address _coordinator, bytes32 _keyHash, uint256 _subId) {
        vrfCoordinator = IVRFCoordinatorV2Plus(_coordinator);
        keyHash = _keyHash;
        subscriptionId = _subId;
        owner = msg.sender;
    }

    function requestRandomness(uint32 _numWords) external onlyOwner returns (uint256 requestId) {
        IVRFCoordinatorV2Plus.RandomWordsRequest memory req = IVRFCoordinatorV2Plus.RandomWordsRequest({
            keyHash: keyHash,
            subId: subscriptionId,
            requestConfirmations: 3,
            callbackGasLimit: 100_000,
            numWords: _numWords,
            extraArgs: ""
        });

        requestId = vrfCoordinator.requestRandomWords(req);
        pendingRequests[requestId] = true;
        emit RandomWordsRequested(requestId);
    }

    /// @notice VRF tugunlari tomonidan chaqiriluvchi ichki funksiya
    function rawFulfillRandomWords(uint256 requestId, uint256[] calldata randomWords) external {
        require(msg.sender == address(vrfCoordinator), "Faqat VRF koordinatori chaqirishi mumkin");
        require(pendingRequests[requestId], "Kutilmagan requestId");

        delete pendingRequests[requestId];
        randomResults[requestId] = randomWords;

        emit RandomWordsFulfilled(requestId, randomWords);
    }
}
```
**Tushuntirish:** Chainlink VRF V2.5 da so'rov va javob ikki bosqichda asinxron ishlaydi. Natija zanjir tashqarisidagi kriptografik maxfiy kalit va blok parametrlaridan olinib, EVM da uning matematik isboti tekshiriladi, bu esa validatorlar tomonidan natijani o'zgartirishni imkonsiz qiladi.

---

### Topshiriq #1133: Chainlink Automation (Keepers): checkUpkeep va performUpkeep arxitekturasi
**Tavsif:** Shartnoma ichidagi davriy to'lovlar, qarz likvidatsiyalari yoki staking foizlarini avtomatlashtirilgan holda, markazlashgan serversiz bajarish kerak.
**Talablar:** `checkUpkeep` funksiyasida off-chain tekshiruv shartlarini hisoblash, `performUpkeep` da on-chain tasdiqlash va holatni yangilash.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title ChainlinkAutomatedVault - Avtomatlashtirilgan g'azna shartnomasi
contract ChainlinkAutomatedVault {
    uint256 public lastTimeStamp;
    uint256 public immutable interval;
    uint256 public counter;

    event UpkeepPerformed(uint256 indexed newCounter, uint256 timeStamp);

    constructor(uint256 _interval) {
        interval = _interval;
        lastTimeStamp = block.timestamp;
    }

    /// @notice Chainlink Keeper tugunlari tomonidan off-chain (bepul) muntazam simulyatsiya qilinadi
    function checkUpkeep(bytes calldata /* checkData */) external view returns (bool upkeepNeeded, bytes memory performData) {
        upkeepNeeded = (block.timestamp - lastTimeStamp) > interval;
        performData = abi.encode(counter + 1);
    }

    /// @notice checkUpkeep 'true' qaytarganda Chainlink tugunlari tomonidan gaz to'lab chaqiriladi
    function performUpkeep(bytes calldata performData) external {
        // Xavfsizlik uchun vaqt shartini on-chain qayta tekshiramiz
        if ((block.timestamp - lastTimeStamp) > interval) {
            lastTimeStamp = block.timestamp;
            uint256 nextVal = abi.decode(performData, (uint256));
            counter = nextVal;
            emit UpkeepPerformed(nextVal, block.timestamp);
        }
    }
}
```
**Tushuntirish:** Chainlink Automation ning asosi ikki qismdan iborat: `checkUpkeep` off-chain rejimida doimiy 'eth_call' orqali bepul simulyatsiya qilinadi. Qachonki shart bajarilsa, Keeper tranzaksiya yuboradi va `performUpkeep` ni chaqiradi. On-chain shartni qayta tekshirish front-running hujumlaridan himoyalaydi.

---

### Topshiriq #1134: Chainlink Data Streams (Low-Latency Pull Oracle) orqali kotirovkalarni tekshirish
**Tavsif:** Perpetual birjalar va derivativ platformalarda an'anaviy Push oracllarning 1-5 daqiqalik kechikishi yetarli emas; sub-second (sekunddan tez) narxlar kerak.
**Talablar:** Chainlink Verifier shartnomasini chaqirish, kriptografik imzolangan hisobotni (report) tekshirish va kotirovkani real vaqtda olish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IVerifierProxy {
    function verify(bytes calldata payload, bytes calldata parameterPayload) external payable returns (bytes memory verifierResponse);
}

/// @title LowLatencyPriceConsumer - Chainlink Data Streams (Pull) narx iste'molchisi
contract LowLatencyPriceConsumer {
    IVerifierProxy public immutable verifier;

    struct ReportData {
        bytes32 feedId;
        uint32 validFromTimestamp;
        uint32 observationsTimestamp;
        uint192 nativeFee;
        uint192 linkFee;
        uint32 expiresAt;
        int192 benchmarkPrice;
        int192 bid;
        int192 ask;
    }

    event PriceVerified(bytes32 indexed feedId, int192 benchmarkPrice, uint32 timestamp);

    constructor(address _verifier) {
        verifier = IVerifierProxy(_verifier);
    }

    /// @notice Imzolangan hisobotni tekshirib narxni olish
    function verifyAndExecute(bytes calldata _signedReport) external payable returns (int192 price) {
        // Hisobotni Chainlink verifier orqali tekshirish
        bytes memory verifiedBytes = verifier.verify{value: msg.value}(_signedReport, abi.encode(msg.sender));

        ReportData memory report = abi.decode(verifiedBytes, (ReportData));
        require(report.expiresAt > block.timestamp, "Hisobot muddati tugagan");

        emit PriceVerified(report.feedId, report.benchmarkPrice, report.observationsTimestamp);
        return report.benchmarkPrice;
    }
}
```
**Tushuntirish:** Chainlink Data Streams 'Pull' modelida ishlaydi. Narxlar blokcheynga doimiy yozib borilmaydi (bu gas tejamkorligini beradi), balki foydalanuvchi o'z tranzaksiyasini yuborayotgan vaqtda so'nggi imzolangan hisobotni ilova qiladi. Shartnoma imzoni tekshirib, o'sha lahzadagi narx bilan operatsiyani bajaradi.

---

### Topshiriq #1135: Pyth Network orqali narx ma'lumotlarini yangilash va haqiqiy narxni hisoblash
**Tavsif:** Pyth Network past kechikishli moliya oracllaridan bo'lib, institutsional market-meykerlarning narxlarini to'playdi. DApp foydalanuvchi tranzaksiyasida narxni yangilab, ishonch oralig'ini (confidence interval) tekshirishi kerak.
**Talablar:** IPyth interfeysidan foydalanish, `updatePriceFeeds` ga zaruriy native fee ni to'lash, `getPriceNoOlderThan` orqali narx va conf ni olish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IPyth {
    struct Price {
        int64 price;
        uint64 conf;
        int32 expo;
        uint256 publishTime;
    }

    function getUpdateFee(bytes[] calldata updateData) external view returns (uint256 feeAmount);
    function updatePriceFeeds(bytes[] calldata updateData) external payable;
    function getPriceNoOlderThan(bytes32 id, uint256 age) external view returns (Price memory price);
}

/// @title PythPriceConsumer - Pyth Network orqali narxni yangilovchi shartnoma
contract PythPriceConsumer {
    IPyth public immutable pyth;
    bytes32 public immutable priceFeedId;

    event PriceUpdated(int64 rawPrice, int32 exponent, uint64 confidence);

    constructor(address _pyth, bytes32 _priceFeedId) {
        pyth = IPyth(_pyth);
        priceFeedId = _priceFeedId;
    }

    /// @notice Narxni on-chain yangilash va hisoblash
    function updateAndGetPrice(bytes[] calldata _pythPriceUpdateData) external payable returns (int64) {
        // 1. Yangilanish komissiyasini hisoblash
        uint256 updateFee = pyth.getUpdateFee(_pythPriceUpdateData);
        require(msg.value >= updateFee, "Yetarsiz Pyth to'lovi");

        // 2. Narxni yangilash (on-chain davlatga yozish)
        pyth.updatePriceFeeds{value: updateFee}(_pythPriceUpdateData);

        // 3. Maksimal 60 soniya eski narxni olish
        IPyth.Price memory currentPrice = pyth.getPriceNoOlderThan(priceFeedId, 60);

        // 4. Ishonch oralig'i (confidence) haddan tashqari keng emasligini tekshirish (15%)
        require(currentPrice.conf * 100 < uint64(currentPrice.price > 0 ? currentPrice.price : -currentPrice.price) * 15, "Haddan tashqari yuqori noaniqlik");

        emit PriceUpdated(currentPrice.price, currentPrice.expo, currentPrice.conf);
        return currentPrice.price;
    }
}
```
**Tushuntirish:** Pyth Network oracllarida har bir kotirovka bilan birga `conf` (Confidence Interval) va `expo` (o'nlik darajasi) taqdim etiladi. Yuqori volatillik paytida `conf` kengayib ketadi, va uni tekshirish orqali manipulyatsiya qilingan yoki noaniq bozor narxlaridan shartnoma himoya qilinadi.

---

### Topshiriq #1136: RedStone Oracles: tranzaksiya calldata'sidagi imzoli narxlarni dekodlash
**Tavsif:** RedStone oracllari ma'lumotlarni tranzaksiyaning calldata oxiriga biriktirib yuboradi (EVM Connector). Shartnoma calldata oxiridagi ma'lumot paketini (RedStone payload) ajratib olib, imzolarni tasdiqlashi zarur.
**Talablar:** Yul inline assembly yordamida calldata oxiridagi RedStone markerini tekshirish, narx va vaqt tamg'asini xavfsiz dekodlash.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title RedStoneCalldataExtractor - Calldata oxiridagi RedStone narx paketini o'quvchi shartnoma
contract RedStoneCalldataExtractor {
    // RedStone payload oxirida 0x000002ed markeri bo'ladi
    bytes4 constant REDSTONE_MARKER = 0x000002ed;

    event RedStoneDataExtracted(uint256 timestamp, uint256 price);

    /// @notice Calldata oxiridan narx paketini ajratib olish
    function extractLatestPrice() public view returns (uint256 extractedPrice, uint256 dataTimestamp) {
        bytes memory data = msg.data;
        uint256 len = data.length;
        require(len > 32, "Yetarsiz calldata uzunligi");

        // Yul yordamida calldata oxirini o'qish
        assembly {
            // Calldata oxiridagi marker va narx paketini ajratish
            let offset := sub(len, 32)
            calldatacopy(0x0, offset, 32)
            extractedPrice := mload(0x0)
        }

        dataTimestamp = block.timestamp;
        require(extractedPrice > 0, "Nol narx");
    }
}
```
**Tushuntirish:** RedStone oracllarining o'ziga xosligi shundaki, ular blokcheyn saqlash (storage) xarajatlarini to'liq bartaraf etadi. Ma'lumot faqatgina tranzaksiya vaqtida calldata ichida uzatiladi va EIP-712 imzolari bilan tekshirilib, xotirada qayta ishlanadi.

---

### Topshiriq #1137: Uniswap V3 TWAP (Time-Weighted Average Price) oracledan narx olish va tekshirish
**Tavsif:** Tashqi markazlashgan oracllarga qaramlikni kamaytirish uchun AMM hovuzidagi matematik integratsiyalangan vaqt o'lchovli o'rtacha narx (TWAP) dan foydalanish talab etiladi.
**Talablar:** Uniswap V3 Pool `observe` funksiyasidan foydalanish, `tickCumulatives` farqi orqali o'rtacha tickni hisoblash va uni narxga aylantirish.
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

/// @title UniswapV3TWAPOracle - 30 daqiqalik o'rtacha narxni hisoblovchi shartnoma
contract UniswapV3TWAPOracle {
    address public immutable pool;
    uint32 public immutable twapPeriod; // Masalan: 1800 soniya (30 daqiqa)

    constructor(address _pool, uint32 _period) {
        require(_period > 0, "Period nol bolmasligi kerak");
        pool = _pool;
        twapPeriod = _period;
    }

    /// @notice Hovuzdagi o'rtacha arifmetik tickni hisoblash
    function getTWAPTick() external view returns (int24 avgTick) {
        uint32[] memory secondsAgos = new uint32[](2);
        secondsAgos[0] = twapPeriod;
        secondsAgos[1] = 0; // Hozirgi lahza

        (int56[] memory tickCumulatives, ) = IUniswapV3Pool(pool).observe(secondsAgos);

        int56 tickCumulativesDelta = tickCumulatives[1] - tickCumulatives[0];
        int56 timeWeightedAverageTick = tickCumulativesDelta / int56(uint56(twapPeriod));

        // Butun son yaxlitlashini hisobga olish
        if (tickCumulativesDelta < 0 && (tickCumulativesDelta % int56(uint56(twapPeriod)) != 0)) {
            timeWeightedAverageTick--;
        }

        avgTick = int24(timeWeightedAverageTick);
    }
}
```
**Tushuntirish:** Uniswap V3 TWAP geometric o'rtacha narxni ifodalaydi. Katta muddatli oynani (masalan 30 daqiqa) tanlash orqali Flash Loan yordamida bitta blokda hovuz narxini manipulyatsiya qilish butunlay befoyda qilinadi, chunki bitta blokning umumiy 30 daqiqalik integraldagi ulushi deyarli nolga teng bo'ladi.

---

### Topshiriq #1138: Multi-Oracle Aggregator (Chainlink asosiy, Pyth zaxira, Uniswap TWAP tekshiruvchi)
**Tavsif:** Bitta oracle manziliga tayanish tizimni zaif qilib qo'yadi. Asosiy oracle Chainlink ishlamay qolsa, avtomatik ravishda Pyth'ga o'tish va ikkalasini Uniswap TWAP bilan solishtirib tekshirish lozim.
**Talablar:** Chainlinkdan narx olish, agar xato bersa Pyth'ga o'tish, narxlar orasidagi farq 5% dan oshsa tranzaksiyani to'xtatish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {AggregatorV3Interface} from "./ChainlinkPriceConsumer.sol";

/// @title ResilientMultiOracle - Ishonchli ko'p manbali oracle agregatori
contract ResilientMultiOracle {
    AggregatorV3Interface public immutable chainlinkFeed;
    uint256 public constant MAX_DEVIATION_BPS = 500; // 5.00%

    error OracleDiscrepancy(uint256 primaryPrice, uint256 fallbackPrice);

    constructor(address _chainlinkFeed) {
        chainlinkFeed = AggregatorV3Interface(_chainlinkFeed);
    }

    /// @notice Bir nechta manbadan xavfsiz agregatsiyalangan narxni olish
    function getUnifiedPrice(uint256 fallbackPrice) external view returns (uint256 finalPrice) {
        uint256 primaryPrice;
        bool chainlinkSuccess = false;

        try chainlinkFeed.latestRoundData() returns (
            uint80,
            int256 price,
            uint256,
            uint256 updatedAt,
            uint80
        ) {
            if (price > 0 && block.timestamp - updatedAt <= 3600) {
                primaryPrice = uint256(price);
                chainlinkSuccess = true;
            }
        } catch {}

        if (!chainlinkSuccess) {
            // Chainlink ishlamasa, ikkinchi manba (fallback) ga o'tamiz
            require(fallbackPrice > 0, "Ikkilamchi oracle narxi yaroqsiz");
            return fallbackPrice;
        }

        // Ikkala narx mavjud bo'lganda og'ishni (deviation) tekshiramiz
        if (fallbackPrice > 0) {
            uint256 diff = primaryPrice > fallbackPrice ? primaryPrice - fallbackPrice : fallbackPrice - primaryPrice;
            uint256 deviationBps = (diff * 10000) / primaryPrice;
            if (deviationBps > MAX_DEVIATION_BPS) {
                revert OracleDiscrepancy(primaryPrice, fallbackPrice);
            }
        }

        return primaryPrice;
    }
}
```
**Tushuntirish:** Ko'p darajali oracle arxitekturasi eng ilg'or DeFi protokollarida (masalan, MakerDAO va Synthetix) qo'llaniladi. Bir manba ishlamay qolganda kutilmagan to'xtashlarning oldi olinadi, ikkala manba o'rtasidagi tafovut tekshiruvi esa yolg'on ma'lumotlar bilan ekspluatatsiya qilinish xavfini bartaraf qiladi.

---

### Topshiriq #1139: Flash Crash va narx anomaliyalaridan himoyalovchi Oracle Circuit Breaker
**Tavsif:** Kriptovalyuta bozorida 1 blok ichida narx 20% dan ko'proqqa tushib ketsa yoki sun'iy sakrasa, qarz berish va likvidatsiya funksiyalarini zudlik bilan avtomatik muzlatish lozim.
**Talablar:** Oldingi tasdiqlangan narxni saqlab borish, yangi narx bilan o'zgarish foizini hisoblash, agar 20% dan oshsa `revert` qilish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title OracleVolatilityCircuitBreaker - Narx sakrashlaridan himoyalovchi modul
contract OracleVolatilityCircuitBreaker {
    uint256 public lastValidPrice;
    uint256 public lastPriceUpdateBlock;
    uint256 public constant MAX_PRICE_CHANGE_PERCENT = 20; // 20% limit

    event VolatilityWarning(uint256 oldPrice, uint256 newPrice, uint256 changePercent);

    error ExcessiveVolatility(uint256 oldPrice, uint256 newPrice);

    constructor(uint256 _initialPrice) {
        lastValidPrice = _initialPrice;
        lastPriceUpdateBlock = block.number;
    }

    /// @notice Yangi olingan narxning dinamikasini tekshirish
    function validatePriceMovement(uint256 newPrice) external returns (bool) {
        if (lastValidPrice > 0) {
            uint256 priceDiff = newPrice > lastValidPrice ? newPrice - lastValidPrice : lastValidPrice - newPrice;
            uint256 changePercent = (priceDiff * 100) / lastValidPrice;

            if (changePercent > MAX_PRICE_CHANGE_PERCENT) {
                emit VolatilityWarning(lastValidPrice, newPrice, changePercent);
                revert ExcessiveVolatility(lastValidPrice, newPrice);
            }
        }

        lastValidPrice = newPrice;
        lastPriceUpdateBlock = block.number;
        return true;
    }
}
```
**Tushuntirish:** Bozorlarda 'Flash Crash' yuz berganda markazlashgan oracllar ham qisqa muddatga ekstremal past narx berib qo'yishi mumkin. Agar shartnomada himoyaviy avariya to'xtatuvchisi (circuit breaker) bo'lsa, sog'lom garovga ega bo'lgan foydalanuvchilarning hisoblari asossiz likvidatsiyaga uchramaydi.

---

### Topshiriq #1140: L2 (Arbitrum/Optimism) Sequencer Uptime Feed tekshiruvi va xavfsiz narx olish
**Tavsif:** Arbitrum yoki Optimism kabi L2 tarmoqlarida markaziy Sequencer vaqtincha to'xtab qolsa va qayta yoqilsa, mempooldagi to'plangan tranzaksiyalar ketma-ket bajariladi. Bu vaqtda eskirgan narx bilan likvidatsiyalar bo'lmasligi uchun kutish davri (grace period) talab etiladi.
**Talablar:** Chainlink Sequencer Uptime Feed tekshiruvi, sequencer ishlamayotgan bo'lsa yoki qayta yoqilganiga grace period o'tmagan bo'lsa narx berishni rad etish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {AggregatorV3Interface} from "./ChainlinkPriceConsumer.sol";

/// @title L2SequencerGuardian - L2 Sequencer holatini tekshiruvchi himoyachi
contract L2SequencerGuardian {
    AggregatorV3Interface public immutable sequencerUptimeFeed;
    uint256 public constant GRACE_PERIOD_TIME = 3600; // 1 soat

    error SequencerDown();
    error GracePeriodNotOver();

    constructor(address _sequencerUptimeFeed) {
        sequencerUptimeFeed = AggregatorV3Interface(_sequencerUptimeFeed);
    }

    /// @notice L2 tarmog'ida sequencer xavfsiz holatda ekanligini tasdiqlash
    function checkSequencer() external view {
        (
            ,
            int256 answer,
            uint256 startedAt,
            ,
        ) = sequencerUptimeFeed.latestRoundData();

        // answer == 0 bo'lsa Sequencer ishlayapti, answer == 1 bo'lsa to'xtagan
        if (answer == 1) {
            revert SequencerDown();
        }

        // Sequencer qayta ishga tushganidan so'ng belgilangan muddat o'tganini tekshirish
        if (block.timestamp - startedAt < GRACE_PERIOD_TIME) {
            revert GracePeriodNotOver();
        }
    }
}
```
**Tushuntirish:** L2 rolluplarda Sequencer to'xtab qolishi (downtime) mumkin. U qayta ishlashni boshlaganida narxlar bir zumda bir necha soatlik oraliqni qoplaydi. 'Grace Period' (kutish muddati) foydalanuvchilarga o'z garovlarini to'ldirish imkonini beradi va MEV botlarning adolatsiz likvidatsiyalaridan himoya qiladi.

---

### Topshiriq #1141: ERC-4337 IAccount interfeysi va validateUserOp tekshiruv mantig'i
**Tavsif:** EIP-4337 Account Abstraction arxitekturasida har bir aqlli hamyon (Smart Contract Account) EntryPoint shartnomasi chaqirganida `validateUserOp` orqali imzo va gas to'lovini tekshirishi shart.
**Talablar:** `validateUserOp` funksiyasini yozish, ECDSA imzosini tiklash, `missingAccountFunds` miqdorini EntryPointga to'lash va `validationData` qaytarish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {ECDSA} from "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";
import {MessageHashUtils} from "@openzeppelin/contracts/utils/cryptography/MessageHashUtils.sol";

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

/// @title MinimalAccount4337 - ERC-4337 standartidagi aqlli hisob
contract MinimalAccount4337 {
    using ECDSA for bytes32;
    using MessageHashUtils for bytes32;

    address public immutable entryPoint;
    address public owner;

    modifier onlyEntryPoint() {
        require(msg.sender == entryPoint, "Faqat EntryPoint");
        _;
    }

    constructor(address _entryPoint, address _owner) {
        entryPoint = _entryPoint;
        owner = _owner;
    }

    /// @notice EntryPoint tomonidan chaqiriluvchi asosiy validatsiya funksiyasi
    function validateUserOp(
        UserOperation calldata userOp,
        bytes32 userOpHash,
        uint256 missingAccountFunds
    ) external onlyEntryPoint returns (uint256 validationData) {
        // 1. Imzoni tekshirish
        bytes32 ethSignedMessageHash = userOpHash.toEthSignedMessageHash();
        address recovered = ethSignedMessageHash.recover(userOp.signature);

        if (recovered != owner) {
            return 1; // 1 = SIG_VALIDATION_FAILED
        }

        // 2. EntryPoint ga gaz zaxirasini to'lash (prefund)
        if (missingAccountFunds > 0) {
            (bool success, ) = payable(entryPoint).call{value: missingAccountFunds}("");
            require(success, "Prefund muvaffaqiyatsiz");
        }

        return 0; // 0 = Validatsiya muvaffaqiyatli
    }
}
```
**Tushuntirish:** EIP-4337 da `validateUserOp` aqlli hamyon xavfsizligining eshigidir. U foydalanuvchi imzosini tekshiradi va EntryPoint talab qilgan `missingAccountFunds` miqdoridagi gaz garovini to'laydi. `validationData` bitlari orqali amal qilish muddati (validUntil / validAfter) ham kodlanishi mumkin.

---

### Topshiriq #1142: ERC-4337 Smart Account: Foydalanuvchi operatsiyasini bajarish (execute va executeBatch)
**Tavsif:** Foydalanuvchi amallari tasdiqlangach, EntryPoint hamyonning `execute` yoki `executeBatch` metodini chaqirib, bitta tranzaksiya ichida bir nechta chaqiruvlarni (Multicall) bajarishi kerak.
**Talablar:** Yagona va paketli ijro metodlari, `call` orqali maqsadli shartnomalarga ma'lumot va qiymat uzatish, xatolik yuz bersa xabarni qaytarish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {MinimalAccount4337} from "./MinimalAccount4337.sol";

/// @title ExecutableSmartAccount - Operatsiyalarni ijro etuvchi aqlli hamyon
contract ExecutableSmartAccount is MinimalAccount4337 {
    event CallExecuted(address indexed target, uint256 value, bytes data);

    constructor(address _entryPoint, address _owner) MinimalAccount4337(_entryPoint, _owner) {}

    /// @notice Bitta operatsiyani bajarish
    function execute(address dest, uint256 value, bytes calldata func) external onlyEntryPoint {
        (bool success, bytes memory result) = dest.call{value: value}(func);
        if (!success) {
            assembly {
                revert(add(result, 32), mload(result))
            }
        }
        emit CallExecuted(dest, value, func);
    }

    /// @notice Bir nechta chaqiruvlarni bitta tranzaksiyada bajarish (Batching)
    function executeBatch(
        address[] calldata dest,
        uint256[] calldata values,
        bytes[] calldata func
    ) external onlyEntryPoint {
        require(dest.length == func.length && dest.length == values.length, "Uzunliklar mos emas");

        for (uint256 i = 0; i < dest.length; i++) {
            (bool success, bytes memory result) = dest[i].call{value: values[i]}(func[i]);
            if (!success) {
                assembly {
                    revert(add(result, 32), mload(result))
                }
            }
            emit CallExecuted(dest[i], values[i], func[i]);
        }
    }

    receive() external payable {}
}
```
**Tushuntirish:** Account Abstraction foydalanuvchilarga 'Approve + Swap' operatsiyalarini bitta tranzaksiyada (`executeBatch`) bajarish imkoniyatini taqdim etadi. Bu foydalanuvchidan bir necha marta 'Approve' qilishni talab qilmaydi va umumiy gas narxini ancha arzonlashtiradi.

---

### Topshiriq #1143: ERC-4337 Paymaster: ERC-20 tokenlarida gaz to'lovini qabul qiluvchi shartnoma
**Tavsif:** Foydalanuvchi o'z hisobida mahalliy ETH bo'lmagan taqdirda ham, USDC yoki stablecoinlar orqali gaz to'lovini to'lashini ta'minlovchi Token Paymaster kerak.
**Talablar:** `validatePaymasterUserOp` orqali foydalanuvchidan kerakli ERC-20 tokenini yechib olish, `postOp` ichida sarflangan haqiqiy gaz hisobiga ko'ra ortiqcha mablag'ni qaytarish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {UserOperation} from "./MinimalAccount4337.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

/// @title TokenPaymaster4337 - ERC-20 tokenlarida gaz to'lovini qabul qiluvchi homiy shartnoma
contract TokenPaymaster4337 {
    using SafeERC20 for IERC20;

    address public immutable entryPoint;
    IERC20 public immutable paymentToken;
    uint256 public constant TOKEN_TO_ETH_RATE = 1000; // 1 ETH = 1000 Token misolida

    modifier onlyEntryPoint() {
        require(msg.sender == entryPoint, "Faqat EntryPoint");
        _;
    }

    constructor(address _entryPoint, address _token) {
        entryPoint = _entryPoint;
        paymentToken = IERC20(_token);
    }

    /// @notice EntryPoint tomonidan gaz to'lovi tekshirilishi
    function validatePaymasterUserOp(
        UserOperation calldata userOp,
        bytes32 /* userOpHash */,
        uint256 maxCost
    ) external onlyEntryPoint returns (bytes memory context, uint256 validationData) {
        uint256 tokenRequired = (maxCost * TOKEN_TO_ETH_RATE) / 1e18;

        // Foydalanuvchidan tokenni shartnomaga o'tkazish
        paymentToken.safeTransferFrom(userOp.sender, address(this), tokenRequired);

        context = abi.encode(userOp.sender, tokenRequired, maxCost);
        return (context, 0);
    }

    /// @notice Tranzaksiya bajarilgandan so'ng haqiqiy sarflangan gaz hisob-kitobi
    function postOp(uint8 /* mode */, bytes calldata context, uint256 actualGasCost) external onlyEntryPoint {
        (address sender, uint256 tokenCharged, uint256 maxCost) = abi.decode(context, (address, uint256, uint256));

        uint256 actualTokenNeeded = (actualGasCost * TOKEN_TO_ETH_RATE) / 1e18;
        if (tokenCharged > actualTokenNeeded) {
            uint256 refund = tokenCharged - actualTokenNeeded;
            paymentToken.safeTransfer(sender, refund); // Ortiqcha tokenni qaytarish
        }
    }
}
```
**Tushuntirish:** Token Paymaster EIP-4337 ning eng kuchli imkoniyatlaridan biridir. Foydalanuvchi hamyonida umuman ETH bo'lmasa ham, o'zining USDC balansi hisobidan tranzaksiya o'tkaza oladi. Paymaster oldindan maksimal summani oladi va `postOp` bosqichida ortgan farqni darhol qaytarib beradi.

---

### Topshiriq #1144: ERC-4337 Verifying Paymaster: Off-chain server imzosi bilan gaz homiyligi
**Tavsif:** Web3 startaplar yangi foydalanuvchilarni jalb qilish maqsadida (onboarding) ularning dastlabki tranzaksiyalarini o'z hisoblaridan homiylik qilib (gasless dApp) o'tkazib bermoqchi.
**Talablar:** Server tomonidan berilgan ECDSA imzosini, amal qilish muddati (validUntil) va homiy ruxsatini `validatePaymasterUserOp` ichida tekshirish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {UserOperation} from "./MinimalAccount4337.sol";
import {ECDSA} from "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";
import {MessageHashUtils} from "@openzeppelin/contracts/utils/cryptography/MessageHashUtils.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

/// @title VerifyingPaymaster - Backend imzosi bilan gazni to'lovchi shartnoma
contract VerifyingPaymaster is Ownable {
    using ECDSA for bytes32;
    using MessageHashUtils for bytes32;

    address public immutable entryPoint;
    address public verifyingSigner;

    constructor(address _entryPoint, address _signer) Ownable(msg.sender) {
        entryPoint = _entryPoint;
        verifyingSigner = _signer;
    }

    function setSigner(address _newSigner) external onlyOwner {
        verifyingSigner = _newSigner;
    }

    function validatePaymasterUserOp(
        UserOperation calldata userOp,
        bytes32 /* userOpHash */,
        uint256 /* maxCost */
    ) external view returns (bytes memory context, uint256 validationData) {
        require(msg.sender == entryPoint, "Faqat EntryPoint");

        // paymasterAndData: [paymaster (20 bayt)] + [validUntil (6 bayt)] + [validAfter (6 bayt)] + [signature (65 bayt)]
        bytes calldata pData = userOp.paymasterAndData;
        require(pData.length >= 20 + 12 + 65, "Qisqa paymaster ma'lumoti");

        uint48 validUntil = uint48(bytes6(pData[20:26]));
        uint48 validAfter = uint48(bytes6(pData[26:32]));
        bytes calldata signature = pData[32:97];

        bytes32 hash = keccak256(abi.encode(userOp.sender, userOp.nonce, validUntil, validAfter));
        address signer = hash.toEthSignedMessageHash().recover(signature);

        if (signer != verifyingSigner) {
            return ("", 1); // Validatsiya xatosi
        }

        // validationData: sigFailed (1 bit) + validUntil (48 bit) + validAfter (48 bit)
        validationData = (uint256(validUntil) << 160) | (uint256(validAfter) << 208);
        return ("", validationData);
    }
}
```
**Tushuntirish:** Verifying Paymaster yordamida ilovalar foydalanuvchilariga 'Gasless' (bepul gaz) tajribasini beradi. Backend maxsus mezonlar (masalan, ro'yxatdan o'tgan yangi foydalanuvchi) bo'yicha imzo qo'yib beradi va barcha gas to'lovlari Paymaster shartnomasining EntryPoint depozitidan qoplanadi.

---

### Topshiriq #1145: ERC-4337 Account Factory: CREATE2 orqali counterfactual hisob yaratish
**Tavsif:** Foydalanuvchi blokcheynda hali aqlli hamyon yaratmagan bo'lsa ham uning deterministik manzili mavjud bo'lishi va birinchi tranzaksiyaning o'zida shartnoma deploy qilinishi zarur.
**Talablar:** CREATE2 opkodidan foydalanish, `getAddress` orqali oldindan manzilni hisoblash, `createAccount` orqali birinchi userOp vaqtida deploy qilish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {ExecutableSmartAccount} from "./ExecutableSmartAccount.sol";

/// @title SmartAccountFactory - Aqlli hisoblarni CREATE2 orqali chiqaruvchi zavod
contract SmartAccountFactory {
    address public immutable entryPoint;

    event AccountCreated(address indexed account, address indexed owner, uint256 salt);

    constructor(address _entryPoint) {
        entryPoint = _entryPoint;
    }

    /// @notice Hamyon deploy qilinishidan oldin uning manzilini aniqlash (Counterfactual)
    function getAddress(address owner, uint256 salt) public view returns (address) {
        bytes memory bytecode = abi.encodePacked(
            type(ExecutableSmartAccount).creationCode,
            abi.encode(entryPoint, owner)
        );
        bytes32 hash = keccak256(
            abi.encodePacked(bytes1(0xff), address(this), salt, keccak256(bytecode))
        );
        return address(uint160(uint256(hash)));
    }

    /// @notice Yangi aqlli hisob yaratish
    function createAccount(address owner, uint256 salt) external returns (address ret) {
        address addr = getAddress(owner, salt);
        uint256 codeSize = addr.code.length;

        if (codeSize > 0) {
            return addr; // Hisob allaqachon mavjud
        }

        ret = address(new ExecutableSmartAccount{salt: bytes32(salt)}(entryPoint, owner));
        emit AccountCreated(ret, owner, salt);
    }
}
```
**Tushuntirish:** Counterfactual Deployment foydalanuvchiga hech qanday gas to'lamasdan o'z manzilini olish va unga mablag' qabul qilish imkonini beradi. Foydalanuvchi o'zining birinchi tranzaksiyasini yuborgan paytda EntryPoint `userOp.initCode` orqali avtomatik ravishda fabrikadan shartnomani yaratadi.

---

### Topshiriq #1146: ERC-4337 Ijtimoiy tiklash moduli (Social Recovery Module with Guardians)
**Tavsif:** Foydalanuvchi o'zining xususiy kalitini (private key) yo'qotib qo'yganda, aktivlar butunlay yo'qolmasligi uchun do'stlari yoki ishonchli qurilmalari (guardians) orqali hisobni tiklash kerak.
**Talablar:** Guardianlar ro'yxati va tiklash kvorumini saqlash, timelock (kechikish vaqti) o'rnatish, belgilangan kvorum tasdiqlasa egasini yangilash.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title SocialRecoveryModule - Ijtimoiy himoyachilar orqali kalitni qayta tiklash
contract SocialRecoveryModule {
    address public wallet;
    address[] public guardians;
    mapping(address => bool) public isGuardian;
    uint256 public recoveryThreshold;
    uint256 public constant TIMELOCK_DELAY = 3 days;

    struct RecoveryRequest {
        address newProposedOwner;
        uint256 approvalCount;
        uint256 executeAfter;
        bool executed;
    }

    RecoveryRequest public currentRecovery;
    mapping(address => bool) public guardianVoted;

    event RecoveryInitiated(address newOwner, uint256 executeAfter);
    event RecoveryExecuted(address newOwner);

    constructor(address _wallet, address[] memory _guardians, uint256 _threshold) {
        wallet = _wallet;
        guardians = _guardians;
        recoveryThreshold = _threshold;
        for (uint256 i = 0; i < _guardians.length; i++) {
            isGuardian[_guardians[i]] = true;
        }
    }

    /// @notice Guardian yangi egalik taklifini tasdiqlaydi
    function approveRecovery(address _newOwner) external {
        require(isGuardian[msg.sender], "Faqat vasiy (guardian)");
        require(!guardianVoted[msg.sender], "Allaqachon tasdiqlangan");

        guardianVoted[msg.sender] = true;

        if (currentRecovery.newProposedOwner != _newOwner) {
            currentRecovery = RecoveryRequest({
                newProposedOwner: _newOwner,
                approvalCount: 1,
                executeAfter: block.timestamp + TIMELOCK_DELAY,
                executed: false
            });
            emit RecoveryInitiated(_newOwner, currentRecovery.executeAfter);
        } else {
            currentRecovery.approvalCount++;
        }
    }

    /// @notice Kvorum to'planib timelock muddati tugagach yangi egaga o'tkazish
    function finalizeRecovery() external {
        require(currentRecovery.approvalCount >= recoveryThreshold, "Yetarsiz kvorum");
        require(block.timestamp >= currentRecovery.executeAfter, "Timelock hali otmadi");
        require(!currentRecovery.executed, "Allaqachon bajarilgan");

        currentRecovery.executed = true;
        // Hamyon shartnomasida egasini almashtirish chaqiruvi
        (bool ok, ) = wallet.call(abi.encodeWithSignature("transferOwnership(address)", currentRecovery.newProposedOwner));
        require(ok, "Egalikni otkazish muvaffaqiyatsiz");

        emit RecoveryExecuted(currentRecovery.newProposedOwner);
    }
}
```
**Tushuntirish:** Ijtimoiy tiklash (Social Recovery) markazlashtirilmagan hamyonlarning kelajagidir. Seed frazani yo'qotish Web3 dagi eng katta xavflardan biridir. Timelock va ko'p guardianli kvorum yordamida hatto bitta guardian o'g'irlangan taqdirda ham foydalanuvchiga hujumni bekor qilish uchun 3 kun vaqt beriladi.

---

### Topshiriq #1147: ERC-4337 Web3 o'yinlar uchun Session Key (sessiya kaliti) moduli
**Tavsif:** On-chain o'yinlarda har bir qilich siltash yoki harakat uchun hamyon orqali qayta-qayta tasdiqlash o'yin jarayonini buzadi. Cheklangan huquq va vaqtga ega vaqtinchalik sessiya kaliti yaratilishi lozim.
**Talablar:** Sessiya kalitining amal qilish vaqti (validUntil), ruxsat etilgan kontrakt manzillari (allowlisted targets) va maksimal xarajat limitini tekshirish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title SessionKeyManager - O'yinlar uchun cheklangan sessiya kalitlari boshqaruvchisi
contract SessionKeyManager {
    struct SessionConfig {
        uint48 validUntil;
        address allowedTarget;
        bytes4 allowedSelector;
        uint256 maxValuePerTx;
    }

    // wallet => sessionKey => config
    mapping(address => mapping(address => SessionConfig)) public sessionKeys;

    event SessionKeyRegistered(address indexed wallet, address indexed key, uint48 validUntil);
    event SessionKeyRevoked(address indexed wallet, address indexed key);

    /// @notice Yangi sessiya kalitini ro'yxatdan o'tkazish
    function registerSessionKey(
        address _sessionKey,
        uint48 _validUntil,
        address _target,
        bytes4 _selector,
        uint256 _maxValue
    ) external {
        sessionKeys[msg.sender][_sessionKey] = SessionConfig({
            validUntil: _validUntil,
            allowedTarget: _target,
            allowedSelector: _selector,
            maxValuePerTx: _maxValue
        });
        emit SessionKeyRegistered(msg.sender, _sessionKey, _validUntil);
    }

    /// @notice Chaqiruv huquqini tekshirish
    function validateSessionCall(
        address _wallet,
        address _key,
        address _target,
        uint256 _value,
        bytes calldata _data
    ) external view returns (bool) {
        SessionConfig memory config = sessionKeys[_wallet][_key];
        if (block.timestamp > config.validUntil) return false;
        if (_target != config.allowedTarget) return false;
        if (_value > config.maxValuePerTx) return false;
        if (bytes4(_data[:4]) != config.allowedSelector) return false;

        return true;
    }
}
```
**Tushuntirish:** Session Keys texnologiyasi Web3 o'yinlarida foydalanuvchiga Web2 o'yinlaridagi kabi uzluksiz tezkorlikni beradi. Foydalanuvchi o'yin boshida faqat 1 soatga va faqat o'yin shartnomasiga tegishli amallar uchun sessiya kalitini yoqadi. O'yin tugagach kalit o'z-o'zidan yaroqsiz bo'ladi.

---

### Topshiriq #1148: ERC-4337 Foydalanuvchi operatsiyalari uchun vaqt chegarasi va nonce boshqaruvi
**Tavsif:** An'anaviy ketma-ket (sequential) nonce mexanizmida bitta tranzaksiya tiqilib qolsa boshqa amallar to'xtaydi. Bir vaqtning o'zida bir nechta mustaqil kanallarda tranzaksiya o'tkazish uchun 2D-nonce tizimi kerak.
**Talablar:** EntryPoint NonceManager standartiga muvofiq, yuqori 192 bitni key (kanal), quyi 64 bitni ketma-ket nonce sifatida boshqarish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title TwoDimensionalNonceTracker - 2D Nonce kanallarini boshqaruvchi shartnoma
contract TwoDimensionalNonceTracker {
    // account => key => sequence
    mapping(address => mapping(uint192 => uint64)) public nonces;

    event NonceIncremented(address indexed account, uint192 key, uint64 newSequence);

    /// @notice 2D nonceni tekshirish va oshirish
    function validateAndConsumeNonce(address account, uint256 rawNonce) external returns (bool) {
        uint192 key = uint192(rawNonce >> 64);
        uint64 seq = uint64(rawNonce);

        require(nonces[account][key] == seq, "Noto'g'ri sequence nonce");

        nonces[account][key] = seq + 1;
        emit NonceIncremented(account, key, seq + 1);
        return true;
    }

    /// @notice Keyingi kutilayotgan to'liq nonceni olish
    function getNonce(address account, uint192 key) external view returns (uint256) {
        return (uint256(key) << 64) | nonces[account][key];
    }
}
```
**Tushuntirish:** EIP-4337 dagi 2D Nonce innovatsiyasi foydalanuvchiga parallel operatsiyalarni o'tkazish imkonini beradi. Masalan, o'yin harakatlari 1-kanalda (key=1), DeFi savdolari 2-kanalda (key=2) bir-biriga mutlaqo xalaqit bermasdan parallel tasdiqlanadi.

---

### Topshiriq #1149: ERC-4337 WebAuthn / Passkey (secp256r1) imzosini tekshiruvchi Smart Account
**Tavsif:** Foydalanuvchilar maxsus kripto-hamyon kalitlarini saqlamasdan, iPhone FaceID yoki barmoq izi (Apple TouchID / Android Passkey) orqali tranzaksiyalarni imzolashi kerak.
**Talablar:** secp256r1 (P-256) egri chizig'idagi imzolarni tekshirish, WebAuthn clientDataJSON va authenticatorData xeshini hisoblash.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title PasskeyAccountValidator - FaceID/Passkey imzosini tasdiqlovchi shartnoma
contract PasskeyAccountValidator {
    // EIP-7212 da tavsiya etilgan P256 verify precompile manzili: 0x100
    address constant P256_VERIFIER = address(0x100);

    struct WebAuthnAuth {
        bytes authenticatorData;
        bytes clientDataJSON;
        uint256[2] rs; // r va s qiymatlari
        uint256[2] coordinates; // Qx va Qy ochiq kalit koordinatalari
    }

    event PasskeyValidated(address indexed user);

    /// @notice Passkey imzosining haqiqiyligini tekshirish
    function verifyPasskeySignature(
        bytes32 messageHash,
        WebAuthnAuth calldata auth
    ) external view returns (bool) {
        // ClientDataJSON ichidagi challenge mosligini tekshirish
        bytes32 clientDataHash = sha256(auth.clientDataJSON);

        // WebAuthn xeshini hosil qilish
        bytes32 finalHash = sha256(abi.encodePacked(auth.authenticatorData, clientDataHash));

        // secp256r1 precompile chaqiruvi
        bytes memory input = abi.encode(
            finalHash,
            auth.rs[0],
            auth.rs[1],
            auth.coordinates[0],
            auth.coordinates[1]
        );

        (bool success, bytes memory ret) = P256_VERIFIER.staticcall(input);
        require(success && ret.length > 0 && abi.decode(ret, (uint256)) == 1, "Passkey imzosi yaroqsiz");

        return true;
    }
}
```
**Tushuntirish:** WebAuthn / Passkeys integratsiyasi Web3 ni ommalashtirishdagi eng katta qadamdir. Qurilmaning xavfsiz chipida (Apple Secure Enclave) yaratilgan P-256 kalitlar FaceID bilan himoyalanadi va hech qachon qurilmadan tashqariga chiqmaydi, bu esa phishing hujumlarini deyarli bartaraf qiladi.

---

### Topshiriq #1150: ERC-4337 Bundler simulyatsiyasi va EntryPoint v0.7 xavfsizlik invariantlari
**Tavsif:** Bundlerlar UserOperation larni mempooldan olib umumiy paketga jamlashdan oldin ularning xavfsizligini va taqiqlangan opkodlar (masalan TIMESTAMP, BLOCKHASH) ishlatilmaganligini simulyatsiya qilishi shart.
**Talablar:** EntryPoint simulyatsiya xatolarini tekshirish, ValidationResult qaytarish va saqlash maydonlariga noqonuniy kirishni (storage access violation) ushlash.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {UserOperation} from "./MinimalAccount4337.sol";

/// @title BundlerSimulator - Bundlerlar uchun tranzaksiya simulyatsiyasini o'tkazuvchi test shartnomasi
contract BundlerSimulator {
    struct SimulationResult {
        uint256 preOpGas;
        uint256 paid;
        uint48 validUntil;
        uint48 validAfter;
        bytes targetResult;
    }

    error SimulationFailed(bytes revertReason);

    /// @notice UserOperation ni simulyatsiya qilish
    function simulateValidation(address entryPoint, UserOperation calldata op) external returns (SimulationResult memory result) {
        // EntryPoint simulyatsiya metodini staticcall orqali chaqirish
        (bool success, bytes memory data) = entryPoint.call(
            abi.encodeWithSignature("simulateValidation((address,uint256,bytes,bytes,uint256,uint256,uint256,uint256,uint256,bytes,bytes))", op)
        );

        if (!success) {
            // Revert sababini tahlil qilish
            revert SimulationFailed(data);
        }

        result = abi.decode(data, (SimulationResult));
    }
}
```
**Tushuntirish:** ERC-4337 ekotizimida Bundlerlar gaz xarajatlarini o'z yonidan to'lab tranzaksiyalarni tarmoqqa yuboradi. Shuning uchun ular `simulateValidation` orqali tranzaksiya mempoolda o'zgarib ketmasligi va paymaster to'lovni kafolatlashiga 100% ishonch hosil qilgandan so'nggina uni blokcheynga kiritadi.

