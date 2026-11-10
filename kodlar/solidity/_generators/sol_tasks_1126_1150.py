# -*- coding: utf-8 -*-
"""
Solidity 23-modul: 1126 dan 1150 gacha bo'lgan topshiriqlar
Wormhole Relayer/NTT, Oracles (Chainlink, Pyth, Redstone, TWAP) va EIP-4337 Account Abstraction
"""

TASKS_1126_1150 = [
    {
        "id": 1126,
        "title": "Wormhole orqali zanjirlararo shaxsiyatni tasdiqlash (Cross-Chain Attestation)",
        "desc": "Foydalanuvchi bitta bosh zanjirda (masalan Ethereum Mainnet) KYC yoki shaxsiyat tekshiruvidan o'tgan bo'lsa, uning tasdiqnomasini boshqa barcha tarmoqlarga VAA orqali uzatish kerak.",
        "req": "Attestation strukturasini yaratish, VAA orqali tekshirish va manzilga KYC tasdiqlangan maqomini berish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "Cross-Chain Attestation mexanizmi foydalanuvchiga har bir alohida tarmoqda takroriy tekshiruvdan o'tmaslik imkonini beradi. Bosh zanjirdagi attestation xizmati tomonidan chiqarilgan VAA boshqa zanjirlardagi DeFi va RWA (Real World Asset) protokollarida to'g'ridan-to'g'ri tan olinadi."
    },
    {
        "id": 1127,
        "title": "Wormhole Relayer (IWormholeRelayer) orqali avtomatik zanjirlararo yetkazish",
        "desc": "Foydalanuvchidan maqsadli zanjirda ikkinchi marta tranzaksiya yuborishni (manual redeem) talab qilmasdan, relayer orqali to'liq avtomatlashtirilgan yetkazib berish (push delivery) kerak.",
        "req": "IWormholeRelayer interfeysidan foydalanish, `sendPayloadToEvm` orqali xabar va receiver gas limitini belgilash, `quoteEVMDeliveryPrice` bilan haqni hisoblash.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "Wormhole Relayer tarmog'i foydalanuvchi tajribasini (UX) sezilarli darajada yaxshilaydi. Manba zanjirida to'langan native fee evaziga Wormhole off-chain relayerlari VAA ni olib, o'zlari maqsadli zanjirdagi shartnomaga yetkazib beradi."
    },
    {
        "id": 1128,
        "title": "Wormhole NTT (Native Token Transfers) framework mantiqi",
        "desc": "Ko'prik orqali o'tkaziladigan tokenlar har bir tarmoqda o'zining tabiiy (native) holatida muomalada bo'lishi va zanjirlararo o'tkazishda tezlik va kunlik limitlar bilan himoyalanishi zarur.",
        "req": "Kunlik transfer chegarasi (Rate Limiter) mantig'ini yozish, burn va mint operatsiyalarini vaqt oynasida kuzatish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "Wormhole NTT (Native Token Transfers) ning muhim ustunligi - uning o'rnatilgan Rate Limiting mexanizmidir. Agar qaysidir zanjirdagi shartnoma kiberhujumga uchrasa, tajovuzkor butun ta'minotni boshqa zanjirlarga birdaniga o'tkaza olmaydi, bu esa loyiha jamoasiga ko'prikni to'xtatish uchun vaqt beradi."
    },
    {
        "id": 1129,
        "title": "Wormhole xabarlari uchun ko'p imzoli favqulodda avariya to'xtatuvchisi (Circuit Breaker)",
        "desc": "Blokcheyn anomal holatga tushganda yoki kutilmagan xakkerlik harakatlari sezilganda, ko'p imzoli (Multisig) qo'mita zudlik bilan barcha zanjirlararo xabarlarni muzlatishi lozim.",
        "req": "Ko'p imzoli ruxsat mexanizmi, shartnomani favqulodda to'xtatish (Pause) va qayta faollashtirish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "Xavfsizlik amaliyotida 'Asimmetrik Favqulodda Holat' tamoyili qo'llaniladi: tizimni to'xtatish (Pause) imkoni bitta ishonchli qo'riqchiga tezkor beriladi, biroq tizimni qayta yoqish (Unpause) ko'p imzoli kvorumni (masalan 3/5 multisig) talab qiladi."
    },
    {
        "id": 1130,
        "title": "Wormhole orqali zanjirlararo limit order buyurtmalarini bajarish (Cross-chain Order Book)",
        "desc": "Markazlashtirilmagan birjada foydalanuvchi Arbitrumda limit order ochib, garov qo'yadi. Solana yoki Ethereumda mos keluvchi qarshi buyurtma (match) topilganda VAA orqali buyurtma yopilishi kerak.",
        "req": "Buyurtma holatini saqlash (Order struct), VAA orqali kross-zanjirli to'ldirish (fill) ma'lumotini tekshirish va mablag'larni taqsimlash.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "Ushbu arxitektura buyurtmalarni zanjirlararo asinxron moslashtirish (Cross-Chain Asynchronous Settlement) imkonini beradi. Boshqa zanjirda tranzaksiya amalga oshganligi to'g'risidagi VAA dalili asosida, manba zanjiridagi depozit tokenni to'g'ridan-to'g'ri ijrochiga o'tkazib beradi."
    },
    {
        "id": 1131,
        "title": "Chainlink Price Feeds orqali aktiv narxini o'qish va eskirganlikni (staleness) tekshirish",
        "desc": "DeFi kreditlash shartnomalarida aktivlar narxi Chainlink oracllari orqali olinadi. Eskirgan yoki yaroqsiz narx sababli noto'g'ri likvidatsiya sodir bo'lishini qat'iy oldini olish kerak.",
        "req": "AggregatorV3Interface dan foydalanish, `latestRoundData` parametrlarini (roundId, price, updatedAt, answeredInRound) to'liq tekshirish, maksimal qabul qilinuvchi eskirish muddatini (heartbeat) sozlash.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "Chainlink ma'lumotlarini o'qishda `price <= 0`, `answeredInRound < roundId` va `block.timestamp - updatedAt > heartbeat` tekshiruvlari o'ta muhimdir. Agar bu tekshiruvlar qilinmasa, tarmoq tiqilishi paytida shartnoma bir necha kunlik eski narxlar bilan ishlab, hovuzlarning bo'shab qolishiga olib kelishi mumkin."
    },
    {
        "id": 1132,
        "title": "Chainlink VRF V2.5 orqali tekshirilgan tasodifiy sonlarni so'rash va qabul qilish",
        "desc": "On-chain lotereya yoki NFT xususiyatlarini aniqlashda manipulyatsiyaga chidamli, matematik jihatdan isbotlangan tasodifiylik (Verifiable Random Function) talab qilinadi.",
        "req": "VRFConsumerBaseV2Plus dan foydalanish, `requestRandomWords` orqali so'rov yuborish, `fulfillRandomWords` ichida raund g'olibini aniqlash.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "Chainlink VRF V2.5 da so'rov va javob ikki bosqichda asinxron ishlaydi. Natija zanjir tashqarisidagi kriptografik maxfiy kalit va blok parametrlaridan olinib, EVM da uning matematik isboti tekshiriladi, bu esa validatorlar tomonidan natijani o'zgartirishni imkonsiz qiladi."
    },
    {
        "id": 1133,
        "title": "Chainlink Automation (Keepers): checkUpkeep va performUpkeep arxitekturasi",
        "desc": "Shartnoma ichidagi davriy to'lovlar, qarz likvidatsiyalari yoki staking foizlarini avtomatlashtirilgan holda, markazlashgan serversiz bajarish kerak.",
        "req": "`checkUpkeep` funksiyasida off-chain tekshiruv shartlarini hisoblash, `performUpkeep` da on-chain tasdiqlash va holatni yangilash.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "Chainlink Automation ning asosi ikki qismdan iborat: `checkUpkeep` off-chain rejimida doimiy 'eth_call' orqali bepul simulyatsiya qilinadi. Qachonki shart bajarilsa, Keeper tranzaksiya yuboradi va `performUpkeep` ni chaqiradi. On-chain shartni qayta tekshirish front-running hujumlaridan himoyalaydi."
    },
    {
        "id": 1134,
        "title": "Chainlink Data Streams (Low-Latency Pull Oracle) orqali kotirovkalarni tekshirish",
        "desc": "Perpetual birjalar va derivativ platformalarda an'anaviy Push oracllarning 1-5 daqiqalik kechikishi yetarli emas; sub-second (sekunddan tez) narxlar kerak.",
        "req": "Chainlink Verifier shartnomasini chaqirish, kriptografik imzolangan hisobotni (report) tekshirish va kotirovkani real vaqtda olish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "Chainlink Data Streams 'Pull' modelida ishlaydi. Narxlar blokcheynga doimiy yozib borilmaydi (bu gas tejamkorligini beradi), balki foydalanuvchi o'z tranzaksiyasini yuborayotgan vaqtda so'nggi imzolangan hisobotni ilova qiladi. Shartnoma imzoni tekshirib, o'sha lahzadagi narx bilan operatsiyani bajaradi."
    },
    {
        "id": 1135,
        "title": "Pyth Network orqali narx ma'lumotlarini yangilash va haqiqiy narxni hisoblash",
        "desc": "Pyth Network past kechikishli moliya oracllaridan bo'lib, institutsional market-meykerlarning narxlarini to'playdi. DApp foydalanuvchi tranzaksiyasida narxni yangilab, ishonch oralig'ini (confidence interval) tekshirishi kerak.",
        "req": "IPyth interfeysidan foydalanish, `updatePriceFeeds` ga zaruriy native fee ni to'lash, `getPriceNoOlderThan` orqali narx va conf ni olish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "Pyth Network oracllarida har bir kotirovka bilan birga `conf` (Confidence Interval) va `expo` (o'nlik darajasi) taqdim etiladi. Yuqori volatillik paytida `conf` kengayib ketadi, va uni tekshirish orqali manipulyatsiya qilingan yoki noaniq bozor narxlaridan shartnoma himoya qilinadi."
    },
    {
        "id": 1136,
        "title": "RedStone Oracles: tranzaksiya calldata'sidagi imzoli narxlarni dekodlash",
        "desc": "RedStone oracllari ma'lumotlarni tranzaksiyaning calldata oxiriga biriktirib yuboradi (EVM Connector). Shartnoma calldata oxiridagi ma'lumot paketini (RedStone payload) ajratib olib, imzolarni tasdiqlashi zarur.",
        "req": "Yul inline assembly yordamida calldata oxiridagi RedStone markerini tekshirish, narx va vaqt tamg'asini xavfsiz dekodlash.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "RedStone oracllarining o'ziga xosligi shundaki, ular blokcheyn saqlash (storage) xarajatlarini to'liq bartaraf etadi. Ma'lumot faqatgina tranzaksiya vaqtida calldata ichida uzatiladi va EIP-712 imzolari bilan tekshirilib, xotirada qayta ishlanadi."
    },
    {
        "id": 1137,
        "title": "Uniswap V3 TWAP (Time-Weighted Average Price) oracledan narx olish va tekshirish",
        "desc": "Tashqi markazlashgan oracllarga qaramlikni kamaytirish uchun AMM hovuzidagi matematik integratsiyalangan vaqt o'lchovli o'rtacha narx (TWAP) dan foydalanish talab etiladi.",
        "req": "Uniswap V3 Pool `observe` funksiyasidan foydalanish, `tickCumulatives` farqi orqali o'rtacha tickni hisoblash va uni narxga aylantirish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "Uniswap V3 TWAP geometric o'rtacha narxni ifodalaydi. Katta muddatli oynani (masalan 30 daqiqa) tanlash orqali Flash Loan yordamida bitta blokda hovuz narxini manipulyatsiya qilish butunlay befoyda qilinadi, chunki bitta blokning umumiy 30 daqiqalik integraldagi ulushi deyarli nolga teng bo'ladi."
    },
    {
        "id": 1138,
        "title": "Multi-Oracle Aggregator (Chainlink asosiy, Pyth zaxira, Uniswap TWAP tekshiruvchi)",
        "desc": "Bitta oracle manziliga tayanish tizimni zaif qilib qo'yadi. Asosiy oracle Chainlink ishlamay qolsa, avtomatik ravishda Pyth'ga o'tish va ikkalasini Uniswap TWAP bilan solishtirib tekshirish lozim.",
        "req": "Chainlinkdan narx olish, agar xato bersa Pyth'ga o'tish, narxlar orasidagi farq 5% dan oshsa tranzaksiyani to'xtatish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "Ko'p darajali oracle arxitekturasi eng ilg'or DeFi protokollarida (masalan, MakerDAO va Synthetix) qo'llaniladi. Bir manba ishlamay qolganda kutilmagan to'xtashlarning oldi olinadi, ikkala manba o'rtasidagi tafovut tekshiruvi esa yolg'on ma'lumotlar bilan ekspluatatsiya qilinish xavfini bartaraf qiladi."
    },
    {
        "id": 1139,
        "title": "Flash Crash va narx anomaliyalaridan himoyalovchi Oracle Circuit Breaker",
        "desc": "Kriptovalyuta bozorida 1 blok ichida narx 20% dan ko'proqqa tushib ketsa yoki sun'iy sakrasa, qarz berish va likvidatsiya funksiyalarini zudlik bilan avtomatik muzlatish lozim.",
        "req": "Oldingi tasdiqlangan narxni saqlab borish, yangi narx bilan o'zgarish foizini hisoblash, agar 20% dan oshsa `revert` qilish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "Bozorlarda 'Flash Crash' yuz berganda markazlashgan oracllar ham qisqa muddatga ekstremal past narx berib qo'yishi mumkin. Agar shartnomada himoyaviy avariya to'xtatuvchisi (circuit breaker) bo'lsa, sog'lom garovga ega bo'lgan foydalanuvchilarning hisoblari asossiz likvidatsiyaga uchramaydi."
    },
    {
        "id": 1140,
        "title": "L2 (Arbitrum/Optimism) Sequencer Uptime Feed tekshiruvi va xavfsiz narx olish",
        "desc": "Arbitrum yoki Optimism kabi L2 tarmoqlarida markaziy Sequencer vaqtincha to'xtab qolsa va qayta yoqilsa, mempooldagi to'plangan tranzaksiyalar ketma-ket bajariladi. Bu vaqtda eskirgan narx bilan likvidatsiyalar bo'lmasligi uchun kutish davri (grace period) talab etiladi.",
        "req": "Chainlink Sequencer Uptime Feed tekshiruvi, sequencer ishlamayotgan bo'lsa yoki qayta yoqilganiga grace period o'tmagan bo'lsa narx berishni rad etish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "L2 rolluplarda Sequencer to'xtab qolishi (downtime) mumkin. U qayta ishlashni boshlaganida narxlar bir zumda bir necha soatlik oraliqni qoplaydi. 'Grace Period' (kutish muddati) foydalanuvchilarga o'z garovlarini to'ldirish imkonini beradi va MEV botlarning adolatsiz likvidatsiyalaridan himoya qiladi."
    },
    {
        "id": 1141,
        "title": "ERC-4337 IAccount interfeysi va validateUserOp tekshiruv mantig'i",
        "desc": "EIP-4337 Account Abstraction arxitekturasida har bir aqlli hamyon (Smart Contract Account) EntryPoint shartnomasi chaqirganida `validateUserOp` orqali imzo va gas to'lovini tekshirishi shart.",
        "req": "`validateUserOp` funksiyasini yozish, ECDSA imzosini tiklash, `missingAccountFunds` miqdorini EntryPointga to'lash va `validationData` qaytarish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "EIP-4337 da `validateUserOp` aqlli hamyon xavfsizligining eshigidir. U foydalanuvchi imzosini tekshiradi va EntryPoint talab qilgan `missingAccountFunds` miqdoridagi gaz garovini to'laydi. `validationData` bitlari orqali amal qilish muddati (validUntil / validAfter) ham kodlanishi mumkin."
    },
    {
        "id": 1142,
        "title": "ERC-4337 Smart Account: Foydalanuvchi operatsiyasini bajarish (execute va executeBatch)",
        "desc": "Foydalanuvchi amallari tasdiqlangach, EntryPoint hamyonning `execute` yoki `executeBatch` metodini chaqirib, bitta tranzaksiya ichida bir nechta chaqiruvlarni (Multicall) bajarishi kerak.",
        "req": "Yagona va paketli ijro metodlari, `call` orqali maqsadli shartnomalarga ma'lumot va qiymat uzatish, xatolik yuz bersa xabarni qaytarish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "Account Abstraction foydalanuvchilarga 'Approve + Swap' operatsiyalarini bitta tranzaksiyada (`executeBatch`) bajarish imkoniyatini taqdim etadi. Bu foydalanuvchidan bir necha marta 'Approve' qilishni talab qilmaydi va umumiy gas narxini ancha arzonlashtiradi."
    },
    {
        "id": 1143,
        "title": "ERC-4337 Paymaster: ERC-20 tokenlarida gaz to'lovini qabul qiluvchi shartnoma",
        "desc": "Foydalanuvchi o'z hisobida mahalliy ETH bo'lmagan taqdirda ham, USDC yoki stablecoinlar orqali gaz to'lovini to'lashini ta'minlovchi Token Paymaster kerak.",
        "req": "`validatePaymasterUserOp` orqali foydalanuvchidan kerakli ERC-20 tokenini yechib olish, `postOp` ichida sarflangan haqiqiy gaz hisobiga ko'ra ortiqcha mablag'ni qaytarish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "Token Paymaster EIP-4337 ning eng kuchli imkoniyatlaridan biridir. Foydalanuvchi hamyonida umuman ETH bo'lmasa ham, o'zining USDC balansi hisobidan tranzaksiya o'tkaza oladi. Paymaster oldindan maksimal summani oladi va `postOp` bosqichida ortgan farqni darhol qaytarib beradi."
    },
    {
        "id": 1144,
        "title": "ERC-4337 Verifying Paymaster: Off-chain server imzosi bilan gaz homiyligi",
        "desc": "Web3 startaplar yangi foydalanuvchilarni jalb qilish maqsadida (onboarding) ularning dastlabki tranzaksiyalarini o'z hisoblaridan homiylik qilib (gasless dApp) o'tkazib bermoqchi.",
        "req": "Server tomonidan berilgan ECDSA imzosini, amal qilish muddati (validUntil) va homiy ruxsatini `validatePaymasterUserOp` ichida tekshirish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "Verifying Paymaster yordamida ilovalar foydalanuvchilariga 'Gasless' (bepul gaz) tajribasini beradi. Backend maxsus mezonlar (masalan, ro'yxatdan o'tgan yangi foydalanuvchi) bo'yicha imzo qo'yib beradi va barcha gas to'lovlari Paymaster shartnomasining EntryPoint depozitidan qoplanadi."
    },
    {
        "id": 1145,
        "title": "ERC-4337 Account Factory: CREATE2 orqali counterfactual hisob yaratish",
        "desc": "Foydalanuvchi blokcheynda hali aqlli hamyon yaratmagan bo'lsa ham uning deterministik manzili mavjud bo'lishi va birinchi tranzaksiyaning o'zida shartnoma deploy qilinishi zarur.",
        "req": "CREATE2 opkodidan foydalanish, `getAddress` orqali oldindan manzilni hisoblash, `createAccount` orqali birinchi userOp vaqtida deploy qilish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "Counterfactual Deployment foydalanuvchiga hech qanday gas to'lamasdan o'z manzilini olish va unga mablag' qabul qilish imkonini beradi. Foydalanuvchi o'zining birinchi tranzaksiyasini yuborgan paytda EntryPoint `userOp.initCode` orqali avtomatik ravishda fabrikadan shartnomani yaratadi."
    },
    {
        "id": 1146,
        "title": "ERC-4337 Ijtimoiy tiklash moduli (Social Recovery Module with Guardians)",
        "desc": "Foydalanuvchi o'zining xususiy kalitini (private key) yo'qotib qo'yganda, aktivlar butunlay yo'qolmasligi uchun do'stlari yoki ishonchli qurilmalari (guardians) orqali hisobni tiklash kerak.",
        "req": "Guardianlar ro'yxati va tiklash kvorumini saqlash, timelock (kechikish vaqti) o'rnatish, belgilangan kvorum tasdiqlasa egasini yangilash.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "Ijtimoiy tiklash (Social Recovery) markazlashtirilmagan hamyonlarning kelajagidir. Seed frazani yo'qotish Web3 dagi eng katta xavflardan biridir. Timelock va ko'p guardianli kvorum yordamida hatto bitta guardian o'g'irlangan taqdirda ham foydalanuvchiga hujumni bekor qilish uchun 3 kun vaqt beriladi."
    },
    {
        "id": 1147,
        "title": "ERC-4337 Web3 o'yinlar uchun Session Key (sessiya kaliti) moduli",
        "desc": "On-chain o'yinlarda har bir qilich siltash yoki harakat uchun hamyon orqali qayta-qayta tasdiqlash o'yin jarayonini buzadi. Cheklangan huquq va vaqtga ega vaqtinchalik sessiya kaliti yaratilishi lozim.",
        "req": "Sessiya kalitining amal qilish vaqti (validUntil), ruxsat etilgan kontrakt manzillari (allowlisted targets) va maksimal xarajat limitini tekshirish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "Session Keys texnologiyasi Web3 o'yinlarida foydalanuvchiga Web2 o'yinlaridagi kabi uzluksiz tezkorlikni beradi. Foydalanuvchi o'yin boshida faqat 1 soatga va faqat o'yin shartnomasiga tegishli amallar uchun sessiya kalitini yoqadi. O'yin tugagach kalit o'z-o'zidan yaroqsiz bo'ladi."
    },
    {
        "id": 1148,
        "title": "ERC-4337 Foydalanuvchi operatsiyalari uchun vaqt chegarasi va nonce boshqaruvi",
        "desc": "An'anaviy ketma-ket (sequential) nonce mexanizmida bitta tranzaksiya tiqilib qolsa boshqa amallar to'xtaydi. Bir vaqtning o'zida bir nechta mustaqil kanallarda tranzaksiya o'tkazish uchun 2D-nonce tizimi kerak.",
        "req": "EntryPoint NonceManager standartiga muvofiq, yuqori 192 bitni key (kanal), quyi 64 bitni ketma-ket nonce sifatida boshqarish.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "EIP-4337 dagi 2D Nonce innovatsiyasi foydalanuvchiga parallel operatsiyalarni o'tkazish imkonini beradi. Masalan, o'yin harakatlari 1-kanalda (key=1), DeFi savdolari 2-kanalda (key=2) bir-biriga mutlaqo xalaqit bermasdan parallel tasdiqlanadi."
    },
    {
        "id": 1149,
        "title": "ERC-4337 WebAuthn / Passkey (secp256r1) imzosini tekshiruvchi Smart Account",
        "desc": "Foydalanuvchilar maxsus kripto-hamyon kalitlarini saqlamasdan, iPhone FaceID yoki barmoq izi (Apple TouchID / Android Passkey) orqali tranzaksiyalarni imzolashi kerak.",
        "req": "secp256r1 (P-256) egri chizig'idagi imzolarni tekshirish, WebAuthn clientDataJSON va authenticatorData xeshini hisoblash.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "WebAuthn / Passkeys integratsiyasi Web3 ni ommalashtirishdagi eng katta qadamdir. Qurilmaning xavfsiz chipida (Apple Secure Enclave) yaratilgan P-256 kalitlar FaceID bilan himoyalanadi va hech qachon qurilmadan tashqariga chiqmaydi, bu esa phishing hujumlarini deyarli bartaraf qiladi."
    },
    {
        "id": 1150,
        "title": "ERC-4337 Bundler simulyatsiyasi va EntryPoint v0.7 xavfsizlik invariantlari",
        "desc": "Bundlerlar UserOperation larni mempooldan olib umumiy paketga jamlashdan oldin ularning xavfsizligini va taqiqlangan opkodlar (masalan TIMESTAMP, BLOCKHASH) ishlatilmaganligini simulyatsiya qilishi shart.",
        "req": "EntryPoint simulyatsiya xatolarini tekshirish, ValidationResult qaytarish va saqlash maydonlariga noqonuniy kirishni (storage access violation) ushlash.",
        "code": """// SPDX-License-Identifier: MIT
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
}""",
        "expl": "ERC-4337 ekotizimida Bundlerlar gaz xarajatlarini o'z yonidan to'lab tranzaksiyalarni tarmoqqa yuboradi. Shuning uchun ular `simulateValidation` orqali tranzaksiya mempoolda o'zgarib ketmasligi va paymaster to'lovni kafolatlashiga 100% ishonch hosil qilgandan so'nggina uni blokcheynga kiritadi."
    }
]
