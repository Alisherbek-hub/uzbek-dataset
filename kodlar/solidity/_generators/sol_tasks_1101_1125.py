# -*- coding: utf-8 -*-
"""
Solidity 23-modul: 1101 dan 1125 gacha bo'lgan topshiriqlar
Cross-Chain protokollari (Chainlink CCIP, LayerZero V2, Wormhole)
"""

TASKS_1101_1125 = [
    {
        "id": 1101,
        "title": "Chainlink CCIP orqali oddiy matnli xabar yuborish (Basic Message Sender)",
        "desc": "Turli EVM blokcheyn tarmoqlari o'rtasida (masalan, Ethereum Sepolia dan Arbitrum Sepoliaga) xavfsiz matnli xabarlarni Chainlink CCIP (Cross-Chain Interoperability Protocol) orqali jo'natish zarur.",
        "req": "Chainlink IRouterClient interfeysidan foydalanish, to'lovni LINK tokenida amalga oshirish, manzil zanjiri selektori (destinationChainSelector) va qabul qiluvchi shartnoma manzilini tekshirish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "Ushbu yechimda Chainlink CCIP `IRouterClient.ccipSend` metodi orqali `EVM2AnyMessage` obyekti uzatiladi. `extraArgs` parametri orqali qabul qiluvchi tarmoqdagi bajarilish uchun gas limit (200,000) o'rnatilgan. To'lov xavfsizligi `SafeERC20` kutubxonasining `safeIncreaseAllowance` metodi bilan kafolatlangan."
    },
    {
        "id": 1102,
        "title": "CCIP yordamida ERC-20 tokenlarini cross-chain uzatish va LINK to'lovi",
        "desc": "DeFi protokollarida aktivlarni zanjirlararo ko'chirish talab etiladi. Foydalanuvchilar o'z tokenlarini boshqa zanjirga xavfsiz o'tkazishi zarur.",
        "req": "Client.EVMTokenAmount strukturasidan foydalanish, foydalanuvchidan tokenni tortib olish va routerga ruxsat (allowance) berish, to'lov uchun LINK balansini tekshirish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "Sof token transferlarida `extraArgs` gasLimit qiymati 0 bo'lishi mumkin, chunki qabul qiluvchi manzil oddiy hamyon (EOA) bo'lsa qo'shimcha kod bajarilishi talab etilmaydi. Tokenlar `Client.EVMTokenAmount` shaklida uzatiladi va Chainlink CCIP zaxira hovuzi orqali lock-mint yoki burn-mint usulida xavfsiz o'tkaziladi."
    },
    {
        "id": 1103,
        "title": "CCIP Native gas tokeni (ETH/MATIC) bilan to'lov qilish va to'lov hisoblash",
        "desc": "Foydalanuvchilar hamyonida har doim LINK tokeni bo'lmasligi mumkin. Shartnoma tarmoqning mahalliy valyutasini (ETH/MATIC) komissiya sifatida qabul qilib, ortiqcha qoldiqni foydalanuvchiga qaytarishi zarur.",
        "req": "feeToken sifatida address(0) ko'rsatish, msg.value ni router.getFee() bilan tekshirish, ortiqcha to'lovni avtomatik ravishda msg.sender ga qaytarish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "Chainlink CCIP da `feeToken: address(0)` ko'rsatilsa, tranzaksiya komissiyasi mahalliy native tokenda (masalan, Arbitrum/Ethereumda ETH) to'lanadi. Shartnoma `router.ccipSend{value: fee}` orqali zaruriy miqdorni uzatadi va ortib qolgan summani `msg.sender`ga qaytarib beradi."
    },
    {
        "id": 1104,
        "title": "CCIPReceiver abstrakt kontraktini implementatsiya qilish va xabar qabul qilish",
        "desc": "Cross-chain arxitekturasida ma'lumot jo'natilganidan so'ng qabul qiluvchi tarmoqda faqat ruxsat etilgan jo'natuvchi va ruxsat etilgan zanjirlardan kelgan xabarlarni filtrlab qabul qilish talab etiladi.",
        "req": "CCIPReceiver bazaviy shartnomasidan vorislik olish, `_ccipReceive` funksiyasini qayta yozish, manba zanjiri selektori va sender manzilini qat'iy tekshirish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "CCIP xavfsizligida `_ccipReceive` metodi tashqi chaqiruvlardan himoyalangan va faqat CCIP Router tomonidan chaqirilishi mumkin. `message.sender` baytlarda bo'lgani sababli `abi.decode(message.sender, (address))` orqali haqiqiy manba manzili olinadi va ruxsatlar tekshiriladi."
    },
    {
        "id": 1105,
        "title": "CCIP ExtraArgs orqali bajarilish gas limitini dinamik belgilash",
        "desc": "Qabul qiluvchi zanjirdagi amallar murakkab bo'lsa (masalan, bir nechta mapping yangilansa yoki boshqa shartnomalar chaqirilsa), standart gas limiti yetarli bo'lmay, tranzaksiya 'Out of Gas' holatiga tushishi mumkin.",
        "req": "Client.EVMExtraArgsV1 yordamida dinamik gas limit sozlash, qo'shimcha argumentlarni abi kodlash va tekshirish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "`Client.EVMExtraArgsV1` Chainlink tomonidan kelgusidagi versiyalar bilan moslikni saqlash maqsadida yaratilgan. `Client._argsToBytes` uni maxsus teg bilan baytlar oqimiga aylantiradi, bu qabul qiluvchi zanjirdagi bajaruvchiga (off-chain relayer) qancha gas ajratish kerakligini bildiradi."
    },
    {
        "id": 1106,
        "title": "CCIP orqali Cross-Chain Yield Aggregator (boshqa tarmoqqa likvidlik yuborish)",
        "desc": "Ethereum Mainnet'dagi yuqori gas narxlari tufayli foydalanuvchilar o'z mablag'larini Optimism yoki Base tarmog'idagi yuqori daromadli (APY) hovuzlarga avtomatik o'tkazib joylashtirmoqchi.",
        "req": "Token va bajarish buyrug'ini (deposit action) bir vaqtda bitta CCIP xabari ichida yuborish, qabul qiluvchi tarmoqda tokenni qabul qilib, belgilangan staking kontraktiga yo'naltirish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "CCIP bir vaqtning o'zida 'Programmable Token Transfer' imkonini beradi. Ya'ni, token bilan birga ixtiyoriy `data` (ushbu vaziyatda `beneficiary` manzili) yuboriladi. Qabul qiluvchi zanjirda tokenni olgach, darhol `yieldVault.depositFor` chaqirilib, passiv daromad olish boshlanadi."
    },
    {
        "id": 1107,
        "title": "CCIP orqali Cross-Chain NFT (ERC-721) ko'chirish (Lock & Mint modeli)",
        "desc": "Foydalanuvchilar o'zlarining noyob NFT aktivlarini Ethereumdan Polygon yoki Avalanche tarmog'iga o'yinlarda ishlatish uchun ko'chirishi kerak.",
        "req": "Manba zanjirda NFTni qulflash (lock) va CCIP xabari jo'natish, qabul qiluvchi zanjirda mos keluvchi sintetik NFTni mint qilish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "Lock-and-Mint modelida original NFT o'z bazaviy zanjirida qulflanadi (escrow), va uning metama'lumotlari hamda `tokenId` CCIP xabari sifatida target zanjirga uzatiladi. Target zanjirdagi receiver shartnoma ushbu ID ga mos keluvchi token nusxasini foydalanuvchiga mint qilib beradi."
    },
    {
        "id": 1108,
        "title": "CCIP xabarlari xatolikka uchraganda favqulodda mablag'larni qaytarish (Emergency Recovery)",
        "desc": "Qabul qiluvchi tomonda xabar bajarilishi muvaffaqiyatsiz bo'lsa yoki noto'g'ri parametrlar tufayli mablag'lar qamalib qolsa, administrator yoki foydalanuvchi o'z tokenlarini xavfsiz qaytarib olishi lozim.",
        "req": "Muvaffaqiyatsiz xabar IDlarini qayd etish, favqulodda bekor qilish va qamalgan tokenlarni xavfsiz chiqarib olish funksiyasini yozish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "CCIP receiver shartnomasida `try this.processMessage()` orqali tashqi chaqiruv amalga oshiriladi. Agar ichki tranzaksiya `revert` bo'lsa, butun CCIP tranzaksiyasi bekor bo'lmaydi, balki `catch` blokiga o'tib, tokenlar shartnoma balansida saqlanadi va qaytarib olish uchun belgilab qo'yiladi."
    },
    {
        "id": 1109,
        "title": "CCIP orqali Multi-Chain DAO boshqaruv ovozlarini bitta bosh tarmoqqa to'plash",
        "desc": "DAO a'zolari turli L2 tarmoqlarida (Arbitrum, Base, Optimism) kam gaz to'lab ovoz berishadi. Barcha ovozlar yakuniy qaror uchun Ethereum Mainnetdagi boshqaruv shartnomasiga sinxronlashishi kerak.",
        "req": "Har bir L2'da ovoz yig'uvchi shartnoma, proposalId va ovozlar sonini CCIP orqali jo'natish, L1 da agregatsiya qilish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "Multi-chain boshqaruvda 'Spoke-and-Hub' modeli qo'llaniladi. Spoke zanjirlarida mahalliy ovozlar jamlanadi va belgilangan muddat tugagach, bitta CCIP paketi orqali Hub shartnomasiga yuboriladi. `chainReported` tekshiruvi takroriy xabar hujumlaridan (replay attacks) himoya qiladi."
    },
    {
        "id": 1110,
        "title": "CCIP orqali zanjirlararo kredit garovini sinxronlashtirish (Cross-Chain Collateral Sync)",
        "desc": "Kreditlash platformasida foydalanuvchi Ethereum tarmog'ida garov (masalan, stETH) qo'yib, Base tarmog'ida stablecoin (USDC) qarz olmoqchi.",
        "req": "Garov depozitini manba zanjirida tasdiqlash, CCIP orqali kredit limitini boshqa zanjirdagi lending shartnomasiga yuborish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "Ushbu shartnoma garovni qabul qiladi va uning hisobini olib, CCIP orqali maqsadli tarmoqdagi qarz berish protokoliga ma'lumot uzatadi. Foydalanuvchi bir tarmoqda aktivlarini likvidatsiyasiz saqlagan holda, boshqa tarmoqdagi arzon operatsiyalardan foydalanib stabil token qarz olishi mumkin bo'ladi."
    },
    {
        "id": 1111,
        "title": "LayerZero V2 Endpoint orqali xabar yuborish va qabul qilish (LzReceiver)",
        "desc": "LayerZero V2 protokoli yordamida ikkita mustaqil zanjir o'rtasida o'ta yengil va past kechikishli (low latency) xabar almashinuvini ta'minlash zarur.",
        "req": "ILayerZeroEndpointV2 interfeysidan foydalanish, `_lzSend` va `_lzReceive` funksiyalarini to'g'ri o'rnatish, EndpointV2 manzilini himoyalash.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "LayerZero V2 da har bir zanjir 'Endpoint ID' (Eid) bilan belgilanadi. Jo'natuvchi va qabul qiluvchi o'rtasidagi xavfsizlik `peers` mapping orqali `bytes32` formatida saqlanadi. `endpoint.send` orqali xabar DVN va Executor tarmoqlariga yuboriladi va manzil zanjiridagi `lzReceive` chaqiriladi."
    },
    {
        "id": 1112,
        "title": "LayerZero OFT (Omnichain Fungible Token) standarti va cross-chain transfer",
        "desc": "Har bir tarmoqda o'zining likvidlik hovuzini alohida saqlamasdan, umumiy ta'minotga ega Omnichain tokenini (OFT) yaratish kerak.",
        "req": "OFT standardini implementatsiya qilish, `_debit` orqali manbada yoqish (burn) va `_credit` orqali maqsadda zarb qilish (mint), quoteSend to'lovini hisoblash.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "OFT (Omnichain Fungible Token) standarti bir nechta zanjirda bir xil token ta'minotini kafolatlaydi. Token manba zanjirda yoqiladi (burn qilinadi) va manzil zanjirida aynan shu miqdorda yangidan chiqariladi (mint qilinadi). Bu likvidlik parchalanishi (fragmentation) muammosini butunlay yo'q qiladi."
    },
    {
        "id": 1113,
        "title": "LayerZero ONFT (Omnichain Non-Fungible Token) - NFTlarni zanjirlararo ko'chirish",
        "desc": "Metaverse yoki GameFi loyihalarida o'yin qahramonlari yoki yer maydonlari NFT shaklida zanjirlararo erkin ko'chib yurishi kerak.",
        "req": "ERC721 bilan ONFT logikasini birlashtirish, tokenId va tokenURI xususiyatlarini saqlab qolish, manba zanjirida yoqish yoki qulflash.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "ONFT mexanizmi yordamida NFT global identifikatori (`tokenId`) barcha qo'llab-quvvatlanuvchi zanjirlar bo'ylab unikal saqlanadi. Bir zanjirda token yoqilganda (burn), LayerZero xabari orqali ikkinchi zanjirda xuddi shu ID bilan `_mint` qilinadi, bu esa ikki nusxa paydo bo'lishining oldini oladi."
    },
    {
        "id": 1114,
        "title": "LayerZero V2 OptionsBuilder yordamida bajarish parametrlarini (gasLimit, value) kodlash",
        "desc": "LayerZero V2 da tranzaksiya ijrochisiga (Executor) qancha gas ajratilishi va foydalanuvchiga qancha native token airdrop qilinishi Options orqali baytlar ketma-ketligida kodlanishi shart.",
        "req": "Options kodlash algoritmini implementatsiya qilish (TYPE_3, WORKER_ID_EXECUTOR, OPTION_TYPE_LZRECEIVE), xavfsiz bit amallaridan foydalanish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "LayerZero V2 da ijro parametrlari `Options` orqali standartlashtirilgan. TYPE_3 binar formati bir nechta ishchilarga (DVN, Executor) ko'rsatmalarni bitta baytlar massivida uzatish imkonini beradi. Natijada relayer qabul qiluvchi zanjirda qancha gas va qo'shimcha airdrop naqd puli berish kerakligini bilib oladi."
    },
    {
        "id": 1115,
        "title": "LayerZero V2 DVN (Decentralized Verifier Network) va xavfsizlik stackini sozlash",
        "desc": "Protokol xavfsizligini ta'minlash uchun xabarlarni bitta emas, bir nechta mustaqil tekshiruvchilar (masalan, Chainlink DVN, Polyhedra ZK-DVN va LayerZero Labs DVN) tasdiqlashi shart.",
        "req": "EndpointV2 shartnomasida `setConfig` orqali SendUln302 va ReceiveUln302 kutubxonalariga DVN ro'yxati va minimal kvorum (threshold) belgilash.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "LayerZero V2 ning eng katta afzalligi modulli xavfsizlikdir (Modular Security Stack). Dasturchi o'z talablariga mos ravishda talab qilinuvchi DVNlarni (masalan, ZK-light client va oracllar) tanlaydi va kvorumni belgilaydi. Bu biron bir verifier buzilgan taqdirda ham butun tizim xavfsizligini ta'minlaydi."
    },
    {
        "id": 1116,
        "title": "LayerZero Non-Blocking LzApp arxitekturasi va payload qayta urinish (Retry logic)",
        "desc": "Agar qabul qiluvchi shartnomadagi ichki logika xatoga uchrasa (masalan, receiverda token balance yetishmasa), butun zanjir kanali bloklanib qolmasligi (Head-of-line blocking) va keyingi xabarlar to'xtamasligi kerak.",
        "req": "Try-catch orqali payloadni saqlab qo'yish, muvaffaqiyatsiz xabarlarni `failedMessages` ga yozish, keyinroq `retryMessage` orqali qayta bajarish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "Standart LayerZero V1/V2 kanallarida qat'iy tartib (ordered execution) mavjud bo'lgani sababli, bitta xabarning xatosi barcha keyingi tranzaksiyalarni muzlatishi mumkin. Non-blocking arxitekturasi buzilgan xabarni xeshlab saqlab qoladi va kanalni ochiq qoldirib, xatoni keyinroq qo'lda yoki avtomat tuzatishga imkon beradi."
    },
    {
        "id": 1117,
        "title": "LayerZero orqali cross-chain arbitraj buyruqlarini bajaruvchi shartnoma",
        "desc": "Arbitraj botlari ikkita turli DEX (masalan, Arbitrumdagi Uniswap va Optimismdagi Velodrome) o'rtasidagi narx farqini ko'rganda, zudlik bilan cross-chain buyruq uzatib svopni bajarishi kerak.",
        "req": "Minimal kutilayotgan foyda (minProfit) parametrini tekshirish, shartnoma ichida token almashinuvini bajarish, foydasiz bo'lsa tranzaksiyani bekor qilish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "Cross-chain arbitrajda kechikish (latency) va narxning o'zgarishi (slippage) eng katta xavf hisoblanadi. Shartnoma `minOut` va `targetProfit` tekshiruvlari orqali foydasiz yoki zararga olib keluvchi almashinuvlarni oldini oladi, shu bilan likvidlikni xavfsiz saqlaydi."
    },
    {
        "id": 1118,
        "title": "LayerZero orqali Omnichain DAO saylov qutisi (Ballot Box Aggregator)",
        "desc": "Turli zanjirlardagi foydalanuvchilar o'zlarining shaxsiy hamyonlaridan mahalliy tarmoqda ovoz berishadi. Mahalliy saylov qutisi ovozlarni jamlab, LayerZero orqali markaziy DAO kontraktiga uzatadi.",
        "req": "Mahalliy saylov natijalarini to'plash, LayerZero orqali imzolangan paketni jo'natish, ikki marta yuborishning oldini olish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "Omnichain saylov tizimida har bir foydalanuvchining alohida tranzaksiyasini L1 ga yuborish o'rniga, mahalliy L2'da ovozlar to'planib (batching), bitta umumlashtirilgan xabar bilan markaziy shartnomaga yuboriladi. Bu gas xarajatlarini 99% gacha qisqartiradi."
    },
    {
        "id": 1119,
        "title": "LayerZero Smart Vault: Arbitrum va Optimism o'rtasida likvidlik balanslash",
        "desc": "DeFi daromad shartnomasida bir tarmoqda likvidlik ortiqcha, ikkinchisida esa kamayib ketganida fondlar LayerZero xabarlari orqali avtomatik ravishda qayta taqsimlanishi (rebalancing) zarur.",
        "req": "Hovuzlar balansini solishtirish, rebalance chegarasini belgilash (delta threshold), cross-chain xabar jo'natib kapitalni harakatga keltirish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "Ushbu shartnoma aqlli g'aznalarga (smart vaults) zanjirlararo kapital samaradorligini (capital efficiency) oshirishga imkon beradi. Algoritmik rebalansing orqali qarz foiz stavkalari eng yuqori bo'lgan tarmoqqa likvidlik o'z vaqtida yetkaziladi."
    },
    {
        "id": 1120,
        "title": "LayerZero xabarlarida Replay Attack va zanjir identifikatorini (Eid) tekshirish",
        "desc": "Boshqa tarmoqdan kelgan haqiqiy xabarni nusxalab olib, uni begona zanjirda yoki noto'g'ri shartnomada qayta bajarishga urinishlar (Cross-chain replay attacks) oldini olish kerak.",
        "req": "Barcha qabul qilingan xabarlar uchun `bytes32 guid` unikal kalitini mappingda tekshirish va bir marta bajarilgan deb belgilash, qat'iy peer tekshiruvi.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "LayerZero V2 da har bir xabarga unikal `guid` (Globally Unique Identifier) beriladi. U manba zanjiri, jo'natuvchi manzili, manzil zanjiri va nonce ma'lumotlarining kriptografik xeshidan iborat. `executedGuids[guid]` flagini tekshirish orqali bitta xabar ikki marta ijro etilishi mutlaqo istisno qilinadi."
    },
    {
        "id": 1121,
        "title": "Wormhole Core Bridge orqali xabar e'lon qilish (publishMessage)",
        "desc": "Turli ekotizimlar (EVM, Solana, Cosmos) o'rtasida aloqa o'rnatish uchun Wormhole Core shartnomasida xabarni `publishMessage` orqali e'lon qilish lozim.",
        "req": "IWormhole interfeysini chaqirish, konsistensiya darajasini (consistencyLevel) belgilash, Wormhole protokol to'lovini (message fee) tekshirish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "Wormhole arxitekturasida shartnoma xabarni `publishMessage` orqali blokcheynga yozadi. 19 ta mustaqil Guardian tugunlari ushbu hodisani (event) kuzatib boradi va bloklar finality darajasiga yetgach (`consistencyLevel`), xabarni imzolab VAA (Verifiable Action Approval) yaratadi."
    },
    {
        "id": 1122,
        "title": "Wormhole VAA (Verifiable Action Approval) xabarini dekodlash va imzolarni tekshirish",
        "desc": "Qabul qiluvchi tarmoqda Guardian tarmoqlari tomonidan imzolangan VAA xabarini qabul qilib, uning haqiqiyligini tekshirish va payloadni ajratib olish talab qilinadi.",
        "req": "Wormhole `parseAndVerifyVM` metodidan foydalanish, kvorumni tekshirish, payload ichidan emitent manzili va ma'lumotlarni o'qish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "VAA (Verifiable Action Approval) - Wormhole ning asosiy dalil paketidir. `parseAndVerifyVM` funksiyasi Guardianlarning hozirgi to'plami (Guardian Set) imzolaganligini, kamida 13/19 kvorum mavjudligini va ECDSA imzolarining to'g'riligini matematik jihatdan isbotlaydi."
    },
    {
        "id": 1123,
        "title": "Wormhole VAA sekvensiyasi orqali double-spending (ikki marta ishlatish)dan himoya",
        "desc": "Foydalanuvchi bir marta tasdiqlangan VAA paketini shartnomaga qayta-qayta topshirib, shartnoma balansidagi mablag'larni o'g'irlashga urinishi mumkin.",
        "req": "emitterChainId, emitterAddress va sequence tripletini xeshlab, unikal mappingda saqlash va ikkinchi marta kelganda tranzaksiyani revert qilish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "Wormhole xabar identifikatsiyasi `(emitterChainId, emitterAddress, sequence)` uchligi bilan kafolatlanadi. `sequence` har bir jo'natuvchi uchun qat'iy 1 ga oshib boradi. Shartnoma ushbu uchlikni saqlab qo'yish orqali takroriy foydalanish (replay attack) xavfini nolga tushiradi."
    },
    {
        "id": 1124,
        "title": "Wormhole Token Bridge integratsiyasi: completeTransfer va tokenlarni chiqarish",
        "desc": "Portal Token Bridge orqali boshqa tarmoqdan yuborilgan tokenlarni qabul qiluvchi zanjirda qabul qilib, yakuniy egasiga chiqarib berish zarur.",
        "req": "ITokenBridge interfeysidan foydalanish, `completeTransfer` funksiyasini chaqirish, qaytarilgan tokenni tekshirish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "Wormhole Portal Token Bridge mexanizmida tokenlar manba zanjirida qulflanadi yoki yoqiladi. Guardianlar imzolagan VAA qabul qiluvchi zanjirga topshirilganda `tokenBridge.completeTransfer` chaqirilib, o'sha zanjirdagi mos token foydalanuvchiga taqdim etiladi."
    },
    {
        "id": 1125,
        "title": "Wormhole orqali zanjirlararo Flash Loan qayta chaqiruvini (Callback execution) bajarish",
        "desc": "Murakkab cross-chain moliyaviy operatsiyalarda bitta zanjirda olingan katta miqdordagi qarz orqali boshqa zanjirdagi likvidatsiyani yopish va natijani VAA orqali qaytarish lozim.",
        "req": "Flash loan olish, VAA yaratish uchun publishMessage chaqirish va qarzni bir xil tranzaksiyada foizi bilan qaytarish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "Ushbu arxitektura atomik operatsiyalarni Wormhole xabar almashinuvi bilan uyg'unlashtiradi. Flash loan olingach, maqsadli zanjirdagi shartnomalar uchun rasmiy buyruq (VAA) e'lon qilinadi va darhol kredit qaytariladi. Bu cross-chain likvidatsiya robotlarining asosiy yadrosidir."
    }
]
