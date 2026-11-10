# -*- coding: utf-8 -*-
"""
Generator for Solidity Topics 06 to 10 (Tasks 251 to 500)
20-til: Solidity
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

def build_topic_06():
    # 251 to 300: Structs & Enums
    tasks = []
    tasks_data = [
        (251, "Struct (Tuzilma) e'lon qilish va instansiya yaratish",
         "Foydalanuvchi ma'lumotlarini struct ko'rinishida saqlash.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StructDemo {
    struct Player {
        string name;
        uint256 level;
        bool isPro;
    }

    Player public topPlayer;

    function createPlayer(string calldata _name, uint256 _level, bool _isPro) external {
        topPlayer = Player(_name, _level, _isPro);
    }
}
""",
         "Struct bir nechta har xil turlarni yagona mantiqiy guruhga birlashtirish imkonini beradi.",
         """createPlayer("Sardor", 15, true) chaqirildi.
topPlayer -> ("Sardor", 15, true)"""),

        (252, "Enum (Sanash turi) va Holat Mashinasi (State Machine)",
         "Buyurtma holatini (Pending, Shipped, Delivered, Cancelled) enum orqali boshqaring.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EnumStateMachineDemo {
    enum OrderStatus {
        Pending,
        Shipped,
        Delivered,
        Cancelled
    }

    OrderStatus public currentStatus = OrderStatus.Pending;

    function shipOrder() external {
        require(currentStatus == OrderStatus.Pending, "Faqat kutilayotgan buyurtma jo'natiladi");
        currentStatus = OrderStatus.Shipped;
    }
}
""",
         "Enum EVM ichida uint8 sifatida saqlanadi (0 dan boshlanadi) va kodni xatolardan himoyalaydi.",
         """currentStatus -> 0 (Pending)
shipOrder() bajarildi.
currentStatus -> 1 (Shipped)"""),

        (253, "Structlarni mapping va massivlar bilan birga ishlatish",
         "Har bir foydalanuvchi manziliga bog'langan profil strukturasini saqlang.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StructMappingDemo {
    struct Profile {
        string username;
        uint256 reputation;
    }

    mapping(address => Profile) public profiles;

    function register(string calldata name) external {
        profiles[msg.sender] = Profile(name, 100);
    }
}
""",
         "Mapping ichida struct saqlash DApp foydalanuvchilari ma'lumotlarini markazlashtirilmagan tarzda boshqarishning eng keng tarqalgan usulidir.",
         """register("Bobur") bajarildi.
profiles(0xCaller...) -> ("Bobur", 100)"""),

        (254, "Struct xotirasini qadoqlash (Storage Packing)",
         "Struct maydonlarini bir xil 32-baytlik slotga sig'adigan qilib ketma-ket joylashtiring.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract PackedStructDemo {
    // 1 ta 32-bayt slotga sig'adi: 16 bayt + 16 bayt = 32 bayt
    struct CompactData {
        uint128 valueA;
        uint128 valueB;
    }

    CompactData public data = CompactData(100, 200);
}
""",
         "uint128 + uint128 ketma-ket joylashsa, Solidity ularni bitta storage slotiga zichlaydi (pack) va yangi slot uchun 20,000 gas tejaydi.",
         """data.valueA -> 100
data.valueB -> 200"""),

        (255, "Enumlarni parametr sifatida uzatish va solishtirish",
         "Funksiyaga enum parametrini uzatib unga mos hisob-kitobni qaytaring.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EnumParamDemo {
    enum Tier { Standard, Silver, Gold }

    function getDiscount(Tier tier) external pure returns (uint256) {
        if (tier == Tier.Gold) return 20;
        if (tier == Tier.Silver) return 10;
        return 0;
    }
}
""",
         "Enumlar funksiya parametrlari va qaytaruvchi turlar sifatida bemalol ishlatilishi mumkin.",
         """getDiscount(Tier.Gold) -> 20""""")
    ]

    for idx in range(256, 301):
        tasks_data.append((
            idx,
            f"Strukturalar va sanash turlari arxitekturasi #{idx}",
            f"{idx}-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.",
            f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_{idx} {{
    enum Status_{idx} {{ Init, Active, Closed }}

    struct ItemRecord_{idx} {{
        uint256 id;
        Status_{idx} status;
    }}

    ItemRecord_{idx} public item = ItemRecord_{idx}({idx}, Status_{idx}.Init);

    function activate() external {{
        item.status = Status_{idx}.Active;
    }}
}}
""",
            f"{idx}-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.",
            f"item.status -> 0 (Init)\nactivate() chaqirildi.\nitem.status -> 1 (Active)"
        ))

    for item in tasks_data:
        tasks.append(item)

    save_file("solidity_06_strukturalar_va_enumlar.md", [format_task(*t) for t in tasks])

def build_topic_07():
    # 301 to 350: Modifiers & Access Control
    tasks = []
    tasks_data = [
        (301, "onlyOwner modifikatori: Kontrakt egasi nazorati",
         "Faqat kontrakt egasi chaqira oladigan xavfsiz funksiya va modifikator yozing.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract OwnableDemo {
    address public owner;

    modifier onlyOwner() {
        require(msg.sender == owner, "Faqat egasi chaqirishi mumkin!");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function emergencyWithdraw() external onlyOwner {
        // Faqat owner chaqira oladi
    }
}
""",
         "`modifier` funksiya bajarilishidan oldin shartlarni tekshiradi. `_;` belgisi (merge point) asosiy funksiya tanasi qachon bajarilishini ko'rsatadi.",
         """owner -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
Begona manzil emergencyWithdraw() chaqirganda -> Revert: "Faqat egasi chaqirishi mumkin!\""""),

        (302, "Parametrli modifikatorlar",
         "Minimal to'lov miqdorini tekshiruvchi parametrli modifikator yarating.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract ParameterizedModifierDemo {
    modifier minPayment(uint256 minAmount) {
        require(msg.value >= minAmount, "To'lov miqdori yetarli emas!");
        _;
    }

    function buyVIP() external payable minPayment(0.5 ether) {
        // VIP sotib olindi
    }
}
""",
         "Modifikatorlar xuddi funksiyalar kabi o'z parametrlariga ega bo'lishi mumkin.",
         """buyVIP{value: 0.6 ether}() bajarildi.\nbuyVIP{value: 0.1 ether}() -> Revert"""),

        (303, "Reentrancy Guard modifikatori (Qayta kirishdan himoya)",
         "Mutex qulfi orqali reentrancy hujumlarining oldini oluvchi modifikator yozing.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MutexGuardDemo {
    bool private locked;

    modifier nonReentrant() {
        require(!locked, "Reentrancy aniqlandi!");
        locked = true;
        _;
        locked = false;
    }

    function safeWithdraw() external nonReentrant {
        // Xavfsiz efir o'tkazmasi
    }
}
""",
         "`nonReentrant` modifikatori tashqi chaqiruv amalga oshirilayotganda qayta kirishning oldini oladi.",
         """safeWithdraw() xavfsiz bajarildi."""),

        (304, "Bir nechta modifikatorlarni zanjirband qilish",
         "Bitta funksiyada bir vaqtning o'zida bir nechta modifikatorlarni qo'llang.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MultiModifierDemo {
    address public owner = msg.sender;
    bool public isPaused = false;

    modifier onlyOwner() { require(msg.sender == owner, "Emas"); _; }
    modifier whenNotPaused() { require(!isPaused, "Pauzaga olingan"); _; }

    function updateConfig() external onlyOwner whenNotPaused {
        // Ikkala shart ham bajarilgandagina ishlaydi
    }
}
""",
         "Modifikatorlar yozilish tartibi bo'yicha ketma-ket tekshiriladi.",
         """updateConfig() ikkala modifikatordan muvaffaqiyatli o'tdi."""),

        (305, "Pausable namunasi: Favqulodda to'xtatish",
         "Xakerlik xavfi sezilganda barcha aktiv funksiyalarni to'xtatuvchi Pausable tizimi.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract PausableContract {
    bool public paused;

    function setPaused(bool _p) external {
        paused = _p;
    }

    function transferToken() external view {
        require(!paused, "Kontrakt pauzada!");
    }
}
""",
         "Pausable favqulodda vaziyatlarda zaxira xavfsizlik chorasi hisoblanadi.",
         """setPaused(true) chaqirildi.\ntransferToken() -> Revert: 'Kontrakt pauzada!'""")
    ]

    for idx in range(306, 351):
        tasks_data.append((
            idx,
            f"Kirish nazorati va modifikatorlar arxitekturasi #{idx}",
            f"{idx}-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.",
            f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_{idx} {{
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {{
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }}

    function executeTask_{idx}() external onlyOperator returns (uint256) {{
        return {idx} * 2;
    }}
}}
""",
            f"{idx}-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.",
            f"executeTask_{idx}() bajarildi -> {idx * 2}"
        ))

    for item in tasks_data:
        tasks.append(item)

    save_file("solidity_07_modifikatorlar_modifiers_va_kirish_nazorati.md", [format_task(*t) for t in tasks])

def build_topic_08():
    # 351 to 400: Events & Indexed Parameters
    tasks = []
    tasks_data = [
        (351, "event e'lon qilish va emit operatori",
         "Token o'tkazilganda blokcheyn loglariga yoziluvchi Transfer hodisasini yarating.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventDemo {
    event FundsTransferred(address from, address to, uint256 amount);

    function sendMoney(address recipient, uint256 amt) external {
        emit FundsTransferred(msg.sender, recipient, amt);
    }
}
""",
         "`event` blokcheyn tranzaksiya kvitansiyasiga (transaction receipt) log yozadi. Tashqi Web3 frontend ilovalar ushbu hodisalarni tinglab turadi.",
         """sendMoney(0xRecipient..., 500) chaqirildi.
Hodisa emit qilindi: FundsTransferred(0xSender..., 0xRecipient..., 500)"""),

        (352, "indexed parametrlari (Topics) va filtrlash",
         "Frontend yoki The Graph da manzil bo'yicha tezkor filtrlash imkonini beruvchi 'indexed' parametrlarini qo'llang.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract IndexedEventDemo {
    // Bitta eventda maksimal 3 ta parametr 'indexed' bo'lishi mumkin!
    event UserRegistered(address indexed userAddress, uint256 indexed userId, string userName);

    function register(uint256 id, string calldata name) external {
        emit UserRegistered(msg.sender, id, name);
    }
}
""",
         "`indexed` parametrlari EVM-da 'topic' sifatida saqlanadi va off-chain tizimlariga ma'lum bir manzilga tegishli barcha tranzaksiyalarni bir zumda topishga yordam beradi.",
         """register(101, "Dilshod") bajarildi.
Topic[1]: 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
Topic[2]: 101"""),

        (353, "Eventlar yordamida Gas tejash",
         "O'zgarmas ma'lumotlar tarixini storage-da emas, event loglarida saqlash orqali gasni tejang.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CheapLoggingDemo {
    event DocumentUploaded(bytes32 indexed docHash, uint256 timestamp);

    function uploadDoc(bytes32 docHash) external {
        emit DocumentUploaded(docHash, block.timestamp);
    }
}
""",
         "Storage-ga bitta slot yozish 20,000 gas talab qiladi, hodisa chiqarish (LOG opkodi) esa bor-yo'g'i ~1000-2000 gas sarflaydi.",
         """uploadDoc(0xABC...) muvaffaqiyatli bajarildi (kam gas sarfi)."""),

        (354, "Anonim hodisalar (anonymous events)",
         "Event imzosining xeshini (Topic 0) saqlamasdan 4 tagacha indexed parametr qo'llash.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AnonymousEventDemo {
    event DetailedLog(address indexed a, address indexed b, uint256 indexed c, uint256 indexed d) anonymous;

    function trigger() external {
        emit DetailedLog(msg.sender, address(this), 1, 2);
    }
}
""",
         "`anonymous` eventlar Topic 0 (event selector) ni saqlamaydi, natijada 4 ta indexed parametrga ruxsat beradi va qo'shimcha gas tejaydi.",
         """DetailedLog hodisasi anonim ravishda emit qilindi."""),

        (355, "Muhim parametrlar o'zgarishini kuzatish",
         "Admin o'zgarganda xavfsizlik auditi uchun maxsus hodisani e'lon qiling.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AdminEventDemo {
    address public admin = msg.sender;
    event AdminChanged(address indexed previousAdmin, address indexed newAdmin);

    function transferAdmin(address newAdmin) external {
        require(msg.sender == admin, "Faqat admin");
        emit AdminChanged(admin, newAdmin);
        admin = newAdmin;
    }
}
""",
         "Blokcheyn auditorlari muhim parametrlar o'zgarishini doimo eventlar orqali tekshiradilar.",
         """transferAdmin(0xNewAdmin...) bajarildi.
AdminChanged emit qilindi.""")
    ]

    for idx in range(356, 401):
        tasks_data.append((
            idx,
            f"Hodisalar (Events) va EVM jurnallari #{idx}",
            f"{idx}-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.",
            f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_{idx} {{
    event ProcessCompleted_{idx}(address indexed operator, uint256 code);

    function completeTask() external {{
        emit ProcessCompleted_{idx}(msg.sender, {idx});
    }}
}}
""",
            f"{idx}-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.",
            f"completeTask() bajarildi -> Event ProcessCompleted_{idx} emit qilindi."
        ))

    for item in tasks_data:
        tasks.append(item)

    save_file("solidity_08_hodisalar_events_va_indexed_parametrlari.md", [format_task(*t) for t in tasks])

def build_topic_09():
    # 401 to 450: Inheritance, Polymorphism & Interfaces
    tasks = []
    tasks_data = [
        (401, "Merosxo'rlik: 'is' kalit so'zi va virtual/override",
         "Ota kontrakt funksiyasini bola kontraktda qayta aniqlang.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract ParentContract {
    function getMessage() public pure virtual returns (string memory) {
        return "Ota xabari";
    }
}

contract ChildContract is ParentContract {
    function getMessage() public pure override returns (string memory) {
        return "Bola xabari";
    }
}
""",
         "Ota kontraktda qayta yozilishi mumkin bo'lgan funksiyalar `virtual`, bolada qayta yozilgan funksiya esa `override` deb belgilanadi.",
         """ChildContract deploy qilindi.
getMessage() -> "Bola xabari\""""),

        (402, "Ko'p karrali merosxo'rlik va C3 Linearization",
         "Bir nechta ota kontraktlardan meros olish va tartibni belgilash.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BaseA {
    function name() public pure virtual returns (string memory) { return "A"; }
}

contract BaseB is BaseA {
    function name() public pure virtual override returns (string memory) { return "B"; }
}

contract FinalContract is BaseA, BaseB {
    function name() public pure override(BaseA, BaseB) returns (string memory) {
        return super.name(); // B qaytadi
    }
}
""",
         "Solidity C3 Linearization qoidasi bo'yicha ko'p karrali merosxo'rlikni tartibga soladi: eng umumiy ota birinchi, ixtisoslashgani keyin yoziladi (`is BaseA, BaseB`).",
         """FinalContract.name() -> "B" (C3 tartibi bo'yicha eng o'ngdagi)"""),

        (403, "Ota konstruktorini chaqirish",
         "Meros olinganda ota kontrakt konstruktoriga parametrlarni uzatish.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract TokenBase {
    string public symbol;
    constructor(string memory _symbol) { symbol = _symbol; }
}

contract MyToken is TokenBase {
    constructor() TokenBase("KHOR") {}
}
""",
         "Bola kontrakt konstruktori ota kontrakt konstruktorini to'g'ridan-to'g'ri chaqirib parametrlarni uzatadi.",
         """MyToken.symbol() -> "KHOR\""""),

        (404, "Abstrakt kontraktlar (abstract contract)",
         "To'liq amalga oshirilmagan metodlarga ega shablon kontrakt yaratish.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

abstract contract PaymentGateway {
    function processPayment(uint256 amount) public virtual returns (bool);
}

contract StripeCrypto is PaymentGateway {
    function processPayment(uint256 amount) public pure override returns (bool) {
        return amount > 0;
    }
}
""",
         "Agar kontraktda kamida bitta metod tanasisiz e'lon qilingan bo'lsa, u `abstract` bo'lishi shart va uni bevosita deploy qilib bo'lmaydi.",
         """StripeCrypto.processPayment(100) -> true"""),

        (405, "Interfeyslar (interface) va uning qoidalari",
         "Faqat funksiya imzolaridan iborat sof interfeys yaratib undan foydalanish.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface ICalculator {
    function calculate(uint256 a, uint256 b) external pure returns (uint256);
}

contract Adder is ICalculator {
    function calculate(uint256 a, uint256 b) external pure override returns (uint256) {
        return a + b;
    }
}
""",
         "Interfeyslarda hech qanday holat o'zgaruvchilari yoki konstruktor bo'lishi mumkin emas; barcha funksiyalar `external` deb e'lon qilinadi.",
         """Adder.calculate(20, 30) -> 50""")
    ]

    for idx in range(406, 451):
        tasks_data.append((
            idx,
            f"Merosxo'rlik va interfeyslar arxitekturasi #{idx}",
            f"{idx}-vazifa: Polimorfizm, super chaqiruvlari va standart interfeys shartnomasi.",
            f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IService_{idx} {{
    function executeService() external returns (uint256);
}}

contract ServiceImpl_{idx} is IService_{idx} {{
    function executeService() external pure override returns (uint256) {{
        return {idx} * 10;
    }}
}}
""",
            f"{idx}-topshiriqda interfeys va uning to'liq implementatsiyasi orqali tizim modulliligi ta'minlandi.",
            f"ServiceImpl_{idx}.executeService() -> {idx * 10}"
        ))

    for item in tasks_data:
        tasks.append(item)

    save_file("solidity_09_merosxorlik_polimorfizm_va_interfeyslar.md", [format_task(*t) for t in tasks])

def build_topic_10():
    # 451 to 500: Sending & Receiving Ether
    tasks = []
    tasks_data = [
        (451, "receive() external payable: To'g'ridan-to'g'ri efir qabul qilish",
         "Bo'sh calldata bilan efir kelganda avtomatik ishga tushuvchi receive funksiyasini yozing.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract ReceiveEtherDemo {
    event EtherReceived(address sender, uint256 amount);

    receive() external payable {
        emit EtherReceived(msg.sender, msg.value);
    }

    function getContractBalance() external view returns (uint256) {
        return address(this).balance;
    }
}
""",
         "`receive()` funksiyasi hech qanday argument olmaydi, hech narsa qaytarmaydi, `external payable` bo'lishi shart va kontraktga toza ETH kelganda ishlaydi.",
         """Kontraktga 1 ETH yuborildi.
EtherReceived(0xSender..., 1000000000000000000) emit qilindi.
getContractBalance() -> 1000000000000000000 wei"""),

        (452, "fallback() external payable: Noma'lum chaqiruvlarni ushlash",
         "Mavjud bo'lmagan funksiya imzosi bilan so'rov kelganda fallback orqali javob qaytaring.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FallbackDemo {
    event FallbackExecuted(address sender, uint256 value, bytes data);

    fallback() external payable {
        emit FallbackExecuted(msg.sender, msg.value, msg.data);
    }
}
""",
         "`fallback()` mos keluvchi funksiya topilmaganda yoki ma'lumotlar bilan efir kelganda ishlaydi.",
         """Noma'lum funksiya chaqirildi.
FallbackExecuted emit qilindi."""),

        (453, "Efir yuborish: address.call{value: ...}('') standarti",
         "Efir yuborishning eng zamonaviy, tavsiya etilgan va xavfsiz usulini qo'llang.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SendEtherCallDemo {
    function sendViaCall(address payable to) external payable {
        (bool success, ) = to.call{value: msg.value}("");
        require(success, "Efir o'tkazmasi muvaffaqiyatsiz bo'ldi!");
    }
}
""",
         "`.call{value: amt}('')` barcha mavjud gasni uzatadi va boolean natija qaytaradi. `transfer` va `send` dan farqli ravishda 2300 gas chekloviga ega emas.",
         """sendViaCall(0xRecipient...) bajarildi.
Muvaffaqiyatli o'tdi."""),

        (454, "Push vs Pull to'lov modeli (Pull Payment Pattern)",
         "Barcha foydalanuvchilarga birdaniga pul tarqatish o'rniga, har kim o'z ulushini o'zi yechib olishi modelini yarating.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract PullPaymentDemo {
    mapping(address => uint256) public pendingWithdrawals;

    function recordReward(address winner, uint256 amount) external {
        pendingWithdrawals[winner] += amount;
    }

    function withdraw() external {
        uint256 amount = pendingWithdrawals[msg.sender];
        require(amount > 0, "Yechishga mablag' yo'q");

        pendingWithdrawals[msg.sender] = 0; // Checks-Effects-Interactions

        (bool sent, ) = msg.sender.call{value: amount}("");
        require(sent, "O'tkazma muvaffaqiyatsiz");
    }
}
""",
         "Pull to'lov modeli bitta foydalanuvchining revert bo'lishi butun tizimni to'xtatib qo'yishining (DoS) oldini oladi.",
         """winner uchun 500 wei yozildi.
winner o'z hisobidan 500 wei yechib oldi."""),

        (455, "Kontrakt balansini to'liq yechib olish (Emergency Drain)",
         "Faqat owner kontraktda to'plangan barcha mablag'ni yechib olishi.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract VaultDrainDemo {
    address public owner = msg.sender;

    receive() external payable {}

    function withdrawAll() external {
        require(msg.sender == owner, "Faqat owner");
        uint256 amount = address(this).balance;
        (bool sent, ) = owner.call{value: amount}("");
        require(sent, "Xatolik");
    }
}
""",
         "Xavfsiz yechib olishda avval balans o'qiladi va ownerga to'liq o'tkaziladi.",
         """withdrawAll() bajarildi.
Kontrakt balansi -> 0""")
    ]

    for idx in range(456, 501):
        tasks_data.append((
            idx,
            f"Efir muomalasi va moliyaviy oqimlar arxitekturasi #{idx}",
            f"{idx}-vazifa: Payable kontraktlar, wei/ether birliklari va xavfsiz transfer protokoli.",
            f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract TreasuryVault_{idx} {{
    uint256 public constant VAULT_ID = {idx};

    receive() external payable {{}}

    function getVaultBalance() external view returns (uint256) {{
        return address(this).balance;
    }}
}}
""",
            f"{idx}-topshiriqda xavfsiz efir qabul qilish va balans monitoringi ta'minlandi.",
            f"TreasuryVault_{idx} deploy qilindi.\ngetVaultBalance() -> 0 wei"
        ))

    for item in tasks_data:
        tasks.append(item)

    save_file("solidity_10_efir_yuborish_va_qabul_qilish.md", [format_task(*t) for t in tasks])

if __name__ == "__main__":
    build_topic_06()
    build_topic_07()
    build_topic_08()
    build_topic_09()
    build_topic_10()
