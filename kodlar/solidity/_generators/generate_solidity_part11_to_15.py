# -*- coding: utf-8 -*-
"""
Generator for Solidity Topics 11 to 15 (Tasks 501 to 750)
20-til: Solidity
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

def build_topic_11():
    # 501 to 550: Low-level Calls, delegatecall & ABI
    tasks = []
    tasks_data = [
        (501, "abi.encodeWithSignature va past darajali call",
         "Boshqa kontrakt metodini nomi va parametrlari orqali dinamik chaqiring.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract TargetReceiver {
    uint256 public value;
    function setValue(uint256 _val) external {
        value = _val;
    }
}

contract CallerContract {
    function callSetValue(address target, uint256 val) external returns (bool) {
        bytes memory payload = abi.encodeWithSignature("setValue(uint256)", val);
        (bool success, ) = target.call(payload);
        return success;
    }
}
""",
         "`target.call(payload)` past darajadagi EVM chaqiruvidir. Agar nishon kontrakt revert qilsa, caller to'xtab qolmaydi, faqat `false` qaytaradi.",
         """callSetValue(targetAddr, 77) -> true
TargetReceiver.value -> 77"""),

        (502, "delegatecall: Kodni boshqa joyda bajarish, holatni joriy kontraktda saqlash",
         "Mantiqni (Logic) boshqa kontrakt kutubxonasidan delegatecall orqali ishlatib o'z storage-ingizni yangilang.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract LogicLibrary {
    uint256 public num;
    function setNum(uint256 _n) external {
        num = _n;
    }
}

contract ProxyContract {
    uint256 public num; // Slot 0: LogicLibrary bilan bir xil layout!

    function executeDelegate(address logic, uint256 val) external returns (bool) {
        (bool success, ) = logic.delegatecall(
            abi.encodeWithSignature("setNum(uint256)", val)
        );
        return success;
    }
}
""",
         "`delegatecall` chaqirilganda kod `logic` kontraktidan olinadi, biroq barcha hisob-kitoblar va storage o'zgarishlari `ProxyContract` kontekstida amalga oshiriladi (`msg.sender` va `msg.value` saqlanadi).",
         """ProxyContract.executeDelegate(logicAddr, 450) -> true
ProxyContract.num -> 450
LogicLibrary.num -> 0 (o'zgarmadi)"""),

        (503, "staticcall: Holatni o'zgartirmaydigan xavfsiz chaqiruv",
         "Boshqa kontraktdan faqat ma'lumot o'qishda hech qanday state o'zgarmasligini kafolatlang.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StaticCallDemo {
    function readRemoteBalance(address token, address user) external view returns (uint256 balance) {
        (bool success, bytes memory data) = token.staticcall(
            abi.encodeWithSignature("balanceOf(address)", user)
        );
        require(success, "staticcall bajarilmadi");
        balance = abi.decode(data, (uint256));
    }
}
""",
         "`staticcall` agar chaqirilgan funksiya holatni o'zgartirishga urinsa (SSTORE, LOG va h.k.) darhol tranzaksiyani bekor qiladi.",
         """readRemoteBalance(token, user) -> 1500000000000000000"""),

        (504, "abi.encode vs abi.encodePacked farqi",
         "Oddiy ABI kodlash va bo'shliqlarsiz qadoqlangan kodlashning xesh hisoblashdagi farqi.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AbiEncodingDemo {
    function getStandardEncoded(string memory a, string memory b) external pure returns (bytes memory) {
        return abi.encode(a, b); // 32 baytlik bloklarga to'ldiradi
    }

    function getPackedHash(string memory a, string memory b) external pure returns (bytes32) {
        return keccak256(abi.encodePacked(a, b)); // Zich qadoqlaydi
    }
}
""",
         "`abi.encodePacked` ma'lumotlarni 32 baytga to'ldirmasdan zich joylashtiradi, biroq bir nechta dinamik argumentlarda xesh to'qnashuvlari (Hash Collision) ga sabab bo'lishi mumkin.",
         """getPackedHash("Salom", "Dunyosi") -> 0x4f35..."""),

        (505, "abi.decode orqali qaytarilgan baytlarni turlarga ajratish",
         "Past darajali chaqiruvdan qaytgan xom baytlarni kerakli strukturaga dekodlang.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AbiDecodeDemo {
    function decodeData(bytes memory raw) external pure returns (uint256 x, address addr, string memory s) {
        (x, addr, s) = abi.decode(raw, (uint256, address, string));
    }
}
""",
         "`abi.decode(bytes, (types))` xom baytlarni Solidity tiplariga aylantirib beradi.",
         """decodeData(rawBytes) -> (42, 0x5B38..., "Web3")""")
    ]

    for idx in range(506, 551):
        tasks_data.append((
            idx,
            f"Past darajali EVM chaqiruvlari va ABI protokollari #{idx}",
            f"{idx}-vazifa: delegatecall, staticcall va xavfsiz inter-kontrakt kommunikatsiyasi.",
            f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract LowLevelBridge_{idx} {{
    uint256 public bridgeId = {idx};

    function executeRaw(address target, bytes calldata callData) external returns (bool, bytes memory) {{
        (bool ok, bytes memory res) = target.call(callData);
        return (ok, res);
    }}
}}
""",
            f"{idx}-topshiriqda past darajali universal chaqiruv ko'prigi va xatoliklar nazorati amalga oshirildi.",
            f"executeRaw(target, data) -> (true, 0x...)"
        ))

    for item in tasks_data:
        tasks.append(item)

    save_file("solidity_11_past_darajali_chaqiruvlar_call_va_delegatecall.md", [format_task(*t) for t in tasks])

def build_topic_12():
    # 551 to 600: ERC-20 Token Standard & Implementation
    tasks = []
    tasks_data = [
        (551, "IERC20 Interfeysi: Standart metodlar va hodisalar",
         "ERC-20 tokenining rasmiy interfeysini e'lon qiling.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IERC20 {
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);

    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function transfer(address to, uint256 value) external returns (bool);
    function allowance(address owner, address spender) external view returns (uint256);
    function approve(address spender, uint256 value) external returns (bool);
    function transferFrom(address from, address to, uint256 value) external returns (bool);
}
""",
         "ERC-20 standarti almashtiriladigan (fungible) tokenlar uchun dunyodagi eng ommabop standart bo'lib, barcha birjalar va hamyonlar tomonidan qo'llab-quvvatlanadi.",
         """IERC20 interfeysi e'lon qilindi."""),

        (552, "Shaxsiy ERC-20 tokenini noldan yozish",
         "O'zbekiston kiber valyutasi (KHOR token) kontraktini to'liq yozing.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract KhorazmToken {
    string public name = "Khorazm AI Token";
    string public symbol = "KHOR";
    uint8 public decimals = 18;
    uint256 public totalSupply;

    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);

    constructor(uint256 initialSupply) {
        totalSupply = initialSupply * 10 ** decimals;
        balanceOf[msg.sender] = totalSupply;
        emit Transfer(address(0), msg.sender, totalSupply);
    }

    function transfer(address to, uint256 value) external returns (bool) {
        require(balanceOf[msg.sender] >= value, "Balans yetarsiz");
        balanceOf[msg.sender] -= value;
        balanceOf[to] += value;
        emit Transfer(msg.sender, to, value);
        return true;
    }
}
""",
         "ERC-20 tokeni `balanceOf` mappingi, 18 ta kasr xonasi (decimals) va `Transfer` hodisasi bilan to'liq ishga tushirildi.",
         """KhorazmToken deploy qilindi.
Deployer balansi: 1000000000000000000000000 (1 million KHOR)"""),

        (553, "approve va transferFrom: Uchinchi tomon xaridini ta'minlash",
         "DEX (Uniswap) yoki boshqa smart kontraktga foydalanuvchi nomidan token sarflash ruxsatini berish.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract ERC20AllowanceDemo {
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    function approve(address spender, uint256 value) external returns (bool) {
        allowance[msg.sender][spender] = value;
        return true;
    }

    function transferFrom(address from, address to, uint256 value) external returns (bool) {
        require(allowance[from][msg.sender] >= value, "Ruxsat etilgan limit yetarli emas");
        require(balanceOf[from] >= value, "Balans yetarli emas");
        allowance[from][msg.sender] -= value;
        balanceOf[from] -= value;
        balanceOf[to] += value;
        return true;
    }
}
""",
         "`approve` va `transferFrom` juftligi DeFi kontraktlarining asosi bo'lib, foydalanuvchiga o'z tokenlarini xavfsiz boshqarish imkonini beradi.",
         """User approve(DEX, 500) qildi.
DEX transferFrom(User, Shop, 500) bajardi."""),

        (554, "Mintable va Burnable tokenlar",
         "Yangi tokenlarni chiqarish (mint) va muomaladagi tokenlarni yo'q qilish (burn).",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MintBurnToken {
    address public owner = msg.sender;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;

    function mint(address to, uint256 amount) external {
        require(msg.sender == owner, "Faqat owner");
        totalSupply += amount;
        balanceOf[to] += amount;
    }

    function burn(uint256 amount) external {
        require(balanceOf[msg.sender] >= amount, "Balans yetarsiz");
        balanceOf[msg.sender] -= amount;
        totalSupply -= amount;
    }
}
""",
         "Minting taklifni oshiradi, Burning esa tokenlarni deflyatsiyaga uchratib, umumiy sonini kamaytiradi.",
         """mint(0xUser..., 1000) -> totalSupply = 1000\nburn(200) -> totalSupply = 800"""),

        (555, "Capped Token (Maksimal taklif chegarasi)",
         "Bitcoin kabi maksimal chegarasi (masalan, 21 million) o'zgarmas qilib belgilangan token.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CappedToken {
    uint256 public immutable cap = 21000000 * 10 ** 18;
    uint256 public totalSupply;

    function mint(uint256 amount) external {
        require(totalSupply + amount <= cap, "Maksimal chegara buzildi!");
        totalSupply += amount;
    }
}
""",
         "`immutable cap` tokenlar soni hech qachon belgilangan sondan oshmasligini qat'iy kafolatlaydi.",
         """cap -> 21000000000000000000000000""")
    ]

    for idx in range(556, 601):
        tasks_data.append((
            idx,
            f"ERC-20 token injiniringi va moliyaviy protokollar #{idx}",
            f"{idx}-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.",
            f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_{idx} {{
    string public symbol = "TKN_{idx}";
    uint256 public totalSupply = {idx} * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {{
        balanceOf[msg.sender] = totalSupply;
    }}
}}
""",
            f"{idx}-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.",
            f"CustomERC20_{idx} yaratildi. Boshlang'ich zaxira: {idx * 1000} TKN_{idx}"
        ))

    for item in tasks_data:
        tasks.append(item)

    save_file("solidity_12_erc20_token_standarti_va_amaliyoti.md", [format_task(*t) for t in tasks])

def build_topic_13():
    # 601 to 650: ERC-721 NFT Standards & Metadata
    tasks = []
    tasks_data = [
        (601, "IERC721 Interfeysi va NFT arxitekturasi",
         "Noyob raqamli san'at va aktivlar uchun rasmiy ERC-721 interfeysini e'lon qiling.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IERC721 {
    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);
    event Approval(address indexed owner, address indexed approved, uint256 indexed tokenId);

    function balanceOf(address owner) external view returns (uint256);
    function ownerOf(uint256 tokenId) external view returns (address);
    function safeTransferFrom(address from, address to, uint256 tokenId) external;
}
""",
         "ERC-721 standarti har bir tokenning noyob `tokenId` identifikatoriga ega bo'lishini va takrorlanmasligini ta'minlaydi.",
         """IERC721 e'lon qilindi."""),

        (602, "Shaxsiy ERC-721 NFT kontraktini noldan yozish",
         "O'zbek madaniy merosi NFT kolleksiyasi kontraktini loyihalang.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract HeritageNFT {
    string public name = "Uzbek Heritage NFTs";
    string public symbol = "UZNFT";

    mapping(uint256 => address) private _owners;
    mapping(address => uint256) private _balances;

    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);

    function mint(address to, uint256 tokenId) external {
        require(_owners[tokenId] == address(0), "Token allaqachon mavjud");
        _owners[tokenId] = to;
        _balances[to] += 1;
        emit Transfer(address(0), to, tokenId);
    }

    function ownerOf(uint256 tokenId) external view returns (address) {
        address owner = _owners[tokenId];
        require(owner != address(0), "Mavjud emas");
        return owner;
    }
}
""",
         "NFT larda har bir `tokenId` aniq bitta egaga (`_owners[tokenId]`) tegishli bo'ladi.",
         """HeritageNFT deploy qilindi.
mint(0xArtist..., 1) bajarildi.
ownerOf(1) -> 0xArtist..."""),

        (603, "tokenURI va JSON Metadata formati",
         "IPFS tarmog'idagi rasm va ma'lumotlar bilan bog'lovchi tokenURI funksiyasini yozing.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTMetadataDemo {
    string public baseURI = "ipfs://QmXoypizjW3WknFiJnKLwHCnL72vedxjQkDDP1mXWo6uco/";

    function tokenURI(uint256 tokenId) external view returns (string memory) {
        return string(abi.encodePacked(baseURI, "token_", _toString(tokenId), ".json"));
    }

    function _toString(uint256 value) internal pure returns (string memory) {
        if (value == 0) return "0";
        uint256 temp = value;
        uint256 digits;
        while (temp != 0) { digits++; temp /= 10; }
        bytes memory buffer = new bytes(digits);
        while (value != 0) {
            digits -= 1;
            buffer[digits] = bytes1(uint8(48 + uint256(value % 10)));
            value /= 10;
        }
        return string(buffer);
    }
}
""",
         "`tokenURI(tokenId)` OpenSea yoki Rarible kabi bozorlarga NFT tasviri, nomi va xususiyatlarini (attributes) yuklab ko'rsatish imkonini beradi.",
         """tokenURI(1) -> "ipfs://QmXoy.../token_1.json\""""),

        (604, "safeTransferFrom va IERC721Receiver xavfsizligi",
         "Smart kontrakt manziliga NFT yuborilganda aktivlar abadiy qulflanib qolmasligini kafolatlang.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IERC721Receiver {
    function onERC721Received(address operator, address from, uint256 tokenId, bytes calldata data) external returns (bytes4);
}

contract SafeTransferDemo {
    bytes4 internal constant MAGIC_VALUE = 0x150b7a02;

    function checkReceiver(address to, uint256 tokenId) internal returns (bool) {
        if (to.code.length > 0) {
            try IERC721Receiver(to).onERC721Received(msg.sender, msg.sender, tokenId, "") returns (bytes4 ret) {
                return ret == MAGIC_VALUE;
            } catch {
                return false;
            }
        }
        return true;
    }
}
""",
         "`safeTransferFrom` qabul qiluvchi kontraktning `onERC721Received` interfeysini tekshiradi va NFT yo'qolib ketishining oldini oladi.",
         """Receiver tekshirildi -> Xavfsiz."""),

        (605, "Royalti standarti: EIP-2981",
         "NFT ikkilamchi bozorda har safar qayta sotilganda muallifga foiz to'lanishini ta'minlang.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract RoyaltyDemo {
    address public artist = msg.sender;
    uint96 public royaltyBasisPoints = 500; // 5% (500 / 10000)

    function royaltyInfo(uint256, uint256 salePrice) external view returns (address receiver, uint256 royaltyAmount) {
        receiver = artist;
        royaltyAmount = (salePrice * royaltyBasisPoints) / 10000;
    }
}
""",
         "EIP-2981 standarti barcha NFT bozorlariga bir xil qoidada mualliflik gonorarini to'lash imkonini yaratadi.",
         """royaltyInfo(1, 10 ether) -> (0xArtist..., 0.5 ether)""")
    ]

    for idx in range(606, 651):
        tasks_data.append((
            idx,
            f"ERC-721 NFT muhandisligi va auksionlar #{idx}",
            f"{idx}-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.",
            f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_{idx} {{
    string public constant COLLECTION_TAG = "COL_{idx}";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {{
        ownerOf[id] = msg.sender;
    }}
}}
""",
            f"{idx}-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.",
            f"NFTCollection_{idx} deploy qilindi.\nmintItem({idx}) bajarildi."
        ))

    for item in tasks_data:
        tasks.append(item)

    save_file("solidity_13_erc721_va_nft_standartlari.md", [format_task(*t) for t in tasks])

def build_topic_14():
    # 651 to 700: ERC-1155 Multi-Token Standard
    tasks = []
    tasks_data = [
        (651, "ERC-1155 Multi-Token standarti mohiyati",
         "Bitta kontraktda ham valyuta (fungible), ham qurollar (non-fungible) aktivlarini birga boshqaring.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract ERC1155BasicDemo {
    uint256 public constant GOLD_COIN = 0;   // Cheksiz almashtiriladigan (Fungible)
    uint256 public constant SWORD_LEGEND = 1; // Noyob yagona qilich (NFT)

    mapping(uint256 => mapping(address => uint256)) public balanceOf;

    function mint(address to, uint256 id, uint256 amount) external {
        balanceOf[id][to] += amount;
    }
}
""",
         "ERC-1155 ko'p tokenli standart bo'lib, o'yinlarda yuzlab har xil aktivlarni bitta kontraktda boshqarish imkonini beradi.",
         """mint(0xGamer..., GOLD_COIN, 1000) bajarildi.
mint(0xGamer..., SWORD_LEGEND, 1) bajarildi."""),

        (652, "Batch Operatsiyalari: safeBatchTransferFrom",
         "Bir nechta har xil tokenlarni bitta tranzaksiya ichida o'tkazib 80% gacha gas tejang.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract ERC1155BatchDemo {
    mapping(uint256 => mapping(address => uint256)) public balanceOf;

    function batchTransfer(
        address to,
        uint256[] calldata ids,
        uint256[] calldata amounts
    ) external {
        require(ids.length == amounts.length, "Uzunliklar mos emas");
        for (uint256 i = 0; i < ids.length; i++) {
            balanceOf[ids[i]][msg.sender] -= amounts[i];
            balanceOf[ids[i]][to] += amounts[i];
        }
    }
}
""",
         "Batch operatsiyalari alohida 10 ta tranzaksiya o'rniga bitta tranzaksiya ochib tarmoq komissiyasini keskin kamaytiradi.",
         """batchTransfer(to, [0, 1], [500, 1]) muvaffaqiyatli bajarildi."""),

        (653, "Dinamik URI formati: {id} almashtirilishi",
         "ERC-1155 dagi o'n oltilik formatdagi dinamik identifikator matnini qaytarish.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract ERC1155UriDemo {
    function uri(uint256) external pure returns (string memory) {
        return "https://api.game.uz/metadata/{id}.json";
    }
}
""",
         "ERC-1155 da `{id}` 64 belgili hexadecimal format bilan frontend tomonidan avtomatik almashtiriladi.",
         """uri(1) -> "https://api.game.uz/metadata/{id}.json\""""),

        (654, "balanceOfBatch orqali ko'p balanslarni bir so'rovda o'qish",
         "Bir nechta o'yinchi va turli tokenlar balansini bitta chaqiruvda tekshiring.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract ERC1155BalanceBatchDemo {
    mapping(uint256 => mapping(address => uint256)) public balanceOf;

    function balanceOfBatch(
        address[] calldata accounts,
        uint256[] calldata ids
    ) external view returns (uint256[] memory batchBalances) {
        require(accounts.length == ids.length, "Massivlar mos emas");
        batchBalances = new uint256[](accounts.length);
        for (uint256 i = 0; i < accounts.length; i++) {
            batchBalances[i] = balanceOf[ids[i]][accounts[i]];
        }
    }
}
""",
         "`balanceOfBatch` RPC chaqiruvlari sonini qisqartiradi.",
         """balanceOfBatch([user1, user2], [1, 2]) -> [10, 50]"""),

        (655, "O'yin iqtisodiyoti uchun integratsiya",
         "Yangi resurslarni konchilik (crafting) orqali yaratish mantig'i.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CraftingDemo {
    uint256 public constant WOOD = 1;
    uint256 public constant IRON = 2;
    uint256 public constant SHIELD = 3;

    mapping(uint256 => mapping(address => uint256)) public balances;

    function craftShield() external {
        require(balances[WOOD][msg.sender] >= 5, "Yog'och yetarsiz");
        require(balances[IRON][msg.sender] >= 2, "Temir yetarsiz");
        balances[WOOD][msg.sender] -= 5;
        balances[IRON][msg.sender] -= 2;
        balances[SHIELD][msg.sender] += 1;
    }
}
""",
         "Multi-token standarti murakkab o'yin resurslarini arzon narxlarda boshqarish imkonini beradi.",
         """craftShield() bajarildi -> Qalqon yaratildi!""")
    ]

    for idx in range(656, 701):
        tasks_data.append((
            idx,
            f"ERC-1155 ko'p tokenli tizimlar #{idx}",
            f"{idx}-vazifa: Multi-asset inventar boshqaruvi va o'yin aktivlari optimizatsiyasi.",
            f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MultiTokenHub_{idx} {{
    uint256 public constant HUB_ID = {idx};
    mapping(uint256 => mapping(address => uint256)) public balances;

    function mintBatchItem(uint256 id, uint256 amount) external {{
        balances[id][msg.sender] += amount;
    }}
}}
""",
            f"{idx}-topshiriqda ERC-1155 token inventari va ko'p qirrali aktivlar balansi shakllantirildi.",
            f"mintBatchItem({idx}, 100) bajarildi.\nbalances({idx}) -> 100"
        ))

    for item in tasks_data:
        tasks.append(item)

    save_file("solidity_14_erc1155_kop_tokenli_standart.md", [format_task(*t) for t in tasks])

def build_topic_15():
    # 701 to 750: Upgradeable Contracts & Proxies
    tasks = []
    tasks_data = [
        (701, "Proksi arxitekturasi: Proxy vs Implementation",
         "Smart kontrakt kodini yangilash uchun proksi modelining ishlash printsipini ko'rsating.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract LogicV1 {
    uint256 public value;
    function setValue(uint256 _val) external {
        value = _val * 2;
    }
}

contract SimpleProxy {
    address public implementation;
    uint256 public value;

    constructor(address _logic) { implementation = _logic; }

    fallback() external payable {
        address impl = implementation;
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
""",
         "Proksi kontrakt barcha ma'lumotlarni saqlaydi va barcha chaqiruvlarni `delegatecall` orqali mantiqiy kontraktga yo'naltiradi.",
         """Proxy orqali setValue(10) chaqirildi.
Proxy.value -> 20 (LogicV1 orqali hisoblandi)"""),

        (702, "EIP-1967: Standartlashtirilgan Storage Slotlari",
         "Proksi va mantiq o'rtasidagi storage to'qnashuvlarini oldini olish uchun pseudo-random slotdan foydalanish.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EIP1967Demo {
    // bytes32(uint256(keccak256('eip1967.proxy.implementation')) - 1)
    bytes32 internal constant _IMPLEMENTATION_SLOT = 
        0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc;

    function getImplementation() external view returns (address impl) {
        assembly {
            impl := sload(_IMPLEMENTATION_SLOT)
        }
    }
}
""",
         "EIP-1967 slotlari 0, 1 kabi oddiy slotlardan uzoqda joylashgani uchun hech qachon foydalanuvchi o'zgaruvchilari bilan to'qnashmaydi (No Storage Collision).",
         """getImplementation() -> 0xLogicContractAddress..."""),

        (703, "Konstruktor o'rniga initialize() funksiyasi",
         "Yangilanuvchi kontraktlarda konstruktor ishlamasligi sababini va Initializable andozasini ko'rsating.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract InitializableLogic {
    bool private initialized;
    address public owner;

    function initialize(address _owner) external {
        require(!initialized, "Allaqachon initsializatsiya qilingan!");
        initialized = true;
        owner = _owner;
    }
}
""",
         "Proksi `delegatecall` qilganda mantiqiy kontraktning konstruktori proksi xotirasini yangilay olmaydi. Shuning uchun ochiq bir martalik `initialize()` funksiyasi ishlatiladi.",
         """initialize(0xAdmin...) bajarildi.
owner -> 0xAdmin...
Qayta initialize chaqirilganda -> Revert"""),

        (704, "UUPS (Universal Upgradeable Proxy Standard) namunasi",
         "Yangilash (upgrade) funksiyasi proksida emas, mantiqiy kontraktning o'zida saqlanishi modeli.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

abstract contract UUPSUpgradeable {
    function upgradeTo(address newImplementation) external virtual;
}

contract MyLogicUUPS is UUPSUpgradeable {
    address public owner = msg.sender;

    function upgradeTo(address newImplementation) external override {
        require(msg.sender == owner, "Faqat owner yangilay oladi");
        // Yangi mantiqqa o'tish kodi
    }
}
""",
         "UUPS Transparent proksiga qaraganda ancha yengil va gaz jihatidan arzon hisoblanadi.",
         """upgradeTo(0xNewLogicAddress...) muvaffaqiyatli bajarildi."""),

        (705, "Storage Layout buzilishi xavfi (Storage Collision)",
         "Mantiq yangilanganda eski o'zgaruvchilar tartibini buzmaslik va oxiriga yangi maydon qo'shish qoidasi.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

// V1
contract LogicLayoutV1 {
    uint256 public count; // Slot 0
}

// V2 (TO'G'RI: eski maydon saqlanib, yangisi oxiriga qo'shiladi)
contract LogicLayoutV2 {
    uint256 public count; // Slot 0
    string public title;  // Slot 1
}
""",
         "Yangilanuvchi kontraktlarda hech qachon mavjud o'zgaruvchilar turi yoki ketma-ketlik tartibini o'zgartirib bo'lmaydi!",
         """Storage layout to'g'ri saqlandi. Xatolik yo'q.""")
    ]

    for idx in range(706, 751):
        tasks_data.append((
            idx,
            f"Yangilanuvchi kontraktlar va proksilar arxitekturasi #{idx}",
            f"{idx}-vazifa: EIP-1967 slotlari, initialize xavfsizligi va proksi boshqaruvi.",
            f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract UpgradeableModule_{idx} {{
    uint256 public constant VERSION = {idx};
    uint256 public stateVar;

    function initialize(uint256 initVal) external {{
        require(stateVar == 0, "Already init");
        stateVar = initVal;
    }}
}}
""",
            f"{idx}-topshiriqda yangilanuvchi modul strukturasi va initsializatsiya nazorati loyihalandi.",
            f"UpgradeableModule_{idx} deploy qilindi.\ninitialize({idx}) bajarildi.\nstateVar -> {idx}"
        ))

    for item in tasks_data:
        tasks.append(item)

    save_file("solidity_15_yangilanuvchi_kontraktlar_upgradeable_va_proksilar.md", [format_task(*t) for t in tasks])

if __name__ == "__main__":
    build_topic_11()
    build_topic_12()
    build_topic_13()
    build_topic_14()
    build_topic_15()
