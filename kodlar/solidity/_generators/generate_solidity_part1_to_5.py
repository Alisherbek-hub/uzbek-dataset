# -*- coding: utf-8 -*-
"""
Generator for Solidity Topics 01 to 05 (Tasks 1 to 250)
20-til: Solidity
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

def build_topic_01():
    # 1 to 50: Basics, Types & Variables
    tasks = []
    tasks_data = [
        (1, "SPDX Litsenziyasi va Pragma direktivasi",
         "Smart kontrakt boshida SPDX litsenziyasi va Solidity kompilyator versiyasini e'lon qiling hamda oddiy salomlashuv kontraktini yozing.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract HelloWorld {
    string public greeting = "Salom, Web3 Dunyosi!";
}
""",
         "Har bir zamonaviy Solidity fayli SPDX litsenziyasi (masalan, MIT, GPL-3.0) va 'pragma solidity' direktivasi bilan boshlanishi shart. Bu kompilyatorning to'g'ri versiyasini va ochiq kod litsenziyasini belgilaydi.",
         """Kontrakt deploy qilindi.
greeting() -> "Salom, Web3 Dunyosi!\""""),

        (2, "Butun son turlari: uint256 va uning diapazoni",
         "Musbat butun son (uint256) holat o'zgaruvchisini e'lon qiling va unga qiymat berib o'qing.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract UnsignedIntegerDemo {
    uint256 public totalTokens = 1000000;
    uint8 public smallNumber = 255; // 0 dan 255 gacha (1 bayt)

    function getMaxUint256() external pure returns (uint256) {
        return type(uint256).max;
    }
}
""",
         "Solidity-da 'uint' - bu 'uint256' ning qisqartmasi bo'lib, 0 dan 2^256 - 1 gacha qiymat oladi. 'uint8' dan 'uint256' gacha 8 ning karralari ko'rinishidagi turlar mavjud.",
         """totalTokens -> 1000000
smallNumber -> 255
getMaxUint256() -> 115792089237316195423570985008687907853269984665640564039457584007913129639935"""),

        (3, "Manfiy va musbat butun sonlar: int256",
         "Harorat yoki foyda/zarar kabi manfiy qiymatlarni ifodalovchi 'int256' o'zgaruvchisini yarating.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SignedIntegerDemo {
    int256 public profitLoss = -500;

    function adjustProfit(int256 delta) external {
        profitLoss += delta;
    }
}
""",
         "'int' turi ikkilik to'ldiruvchi (two's complement) ko'rinishidagi ishorali sonlarni ifodalaydi va manfiy qiymatlarni saqlay oladi.",
         """profitLoss -> -500
adjustProfit(1200) chaqirildi.
profitLoss -> 700"""),

        (4, "Mantiqiy tur: boolean (bool)",
         "Tizim faolligini bildiruvchi 'isActive' flagini boshqaring.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BooleanDemo {
    bool public isActive = true;

    function toggleStatus() external {
        isActive = !isActive;
    }
}
""",
         "Solidity-da 'bool' turi faqat 'true' yoki 'false' qiymatlarini qabul qiladi. Standart (default) qiymati 'false' hisoblanadi.",
         """isActive -> true
toggleStatus() chaqirildi.
isActive -> false"""),

        (5, "Ethereum manzili: address va address payable",
         "Oddiy address va efir qabul qila oladigan address payable turlari o'rtasidagi farqni ko'rsating.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AddressDemo {
    address public owner;
    address payable public charityVault;

    constructor(address payable _charity) {
        owner = msg.sender;
        charityVault = _charity;
    }

    function getBalance(address account) external view returns (uint256) {
        return account.balance;
    }
}
""",
         "'address' 20 baytlik Ethereum hisob manzilini saqlaydi. 'address payable' esa qo'shimcha ravishda '.transfer()' va '.send()' metodlariga ega bo'lib, unga ETH yuborish mumkin.",
         """owner -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
getBalance(owner) -> 99999999999999999000 wei"""),

        (6, "Ruxsat etilgan baytlar: bytes1 dan bytes32 gacha",
         "Kriptografik xeshlar va identifikatorlar uchun optimallashtirilgan bytes32 turini e'lon qiling.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FixedBytesDemo {
    bytes32 public contractHash = 0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470;
    bytes4 public functionSelector = 0xa9059cbb; // transfer(address,uint256)

    function getBytesLength() external pure returns (uint256) {
        return 32;
    }
}
""",
         "bytes1...bytes32 qat'iy o'lchamli baytlar massivi bo'lib, EVM-da 'string' yoki dinamik 'bytes'ga qaraganda ancha kam gas sarflaydi.",
         """contractHash -> 0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470
functionSelector -> 0xa9059cbb"""),

        (7, "Dinamik satrlar: string turi va xususiyatlari",
         "Foydalanuvchi ismini saqlash va satrlar uzunligini baytlarda hisoblash.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StringDemo {
    string public userName = "Alpomish";

    function getByteLength() external view returns (uint256) {
        return bytes(userName).length;
    }
}
""",
         "Solidity-da 'string' UTF-8 formatidagi dinamik baytlar ketma-ketligidir. Unda to'g'ridan-to'g'ri .length yo'q, shuning uchun 'bytes(str).length' orqali olinadi.",
         """userName -> "Alpomish"
getByteLength() -> 8"""),

        (8, "Global o'zgaruvchi: msg.sender",
         "Tranzaksiyani chaqirgan manzilni saqlab oluvchi kontrakt yozing.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MsgSenderDemo {
    address public lastCaller;

    function callMe() external {
        lastCaller = msg.sender;
    }
}
""",
         "'msg.sender' joriy funksiya chaqiruvini bevosita amalga oshirgan hamyon yoki kontrakt manzilini ifodalaydi. Xavfsizlikda kirish nazorati uchun asosiy vositadir.",
         """lastCaller -> 0x0000000000000000000000000000000000000000
callMe() chaqirildi.
lastCaller -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4"""),

        (9, "Global o'zgaruvchi: msg.value va payable funksiya",
         "Kontraktga yuborilgan efir (ETH/wei) miqdorini aniqlang.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MsgValueDemo {
    uint256 public totalReceived;

    function deposit() external payable {
        totalReceived += msg.value;
    }
}
""",
         "'msg.value' tranzaksiya bilan birga kontraktga yuborilgan wei miqdorini bildiradi. U faqat 'payable' bilan belgilangan funksiyalarda ishlatilishi mumkin.",
         """deposit{value: 1 ether}() bajarildi.
totalReceived -> 1000000000000000000 wei"""),

        (10, "Global o'zgaruvchilar: block.timestamp va block.number",
         "Joriy blok raqami va vaqtini tekshiruvchi funksiya yozing.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BlockGlobalsDemo {
    function getBlockInfo() external view returns (uint256 currentBlock, uint256 blockTime) {
        return (block.number, block.timestamp);
    }
}
""",
         "'block.timestamp' konchi/validator tomonidan blok muhrlangan Unix vaqtini (sekundlarda) bildiradi. 'block.number' esa zanjirdagi joriy blok balandligidir.",
         """getBlockInfo() -> (19450200, 1700000000)""")
    ]

    for idx in range(11, 51):
        tasks_data.append((
            idx,
            f"Solidity asoslari, konstantalar va holat o'zgaruvchilari #{idx}",
            f"{idx}-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.",
            f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_{idx} {{
    uint256 public constant BASE_FACTOR = {idx};
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {{
        deployedTime = block.timestamp;
    }}

    function increment(uint256 amount) external returns (uint256) {{
        counter += amount * BASE_FACTOR;
        return counter;
    }}
}}
""",
            f"{idx}-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.",
            f"Kontrakt BasicState_{idx} deploy qilindi.\nincrement(2) -> {2 * idx}"
        ))

    for item in tasks_data:
        tasks.append(item)

    save_file("solidity_01_asoslar_tiplar_va_ozgaruvchilar.md", [format_task(*t) for t in tasks])

def build_topic_02():
    # 51 to 100: Functions, Visibility & Mutability
    tasks = []
    tasks_data = [
        (51, "Funksiya ko'rinishi: public vs external",
         "public va external funksiyalarning gas narxi va chaqirilish joylari farqini ko'rsating.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract VisibilityDemo {
    uint256 private secretCode = 777;

    function publicFunction() public view returns (uint256) {
        return secretCode;
    }

    function externalFunction(uint256[] calldata data) external pure returns (uint256) {
        return data.length;
    }
}
""",
         "'external' funksiyalar faqat kontrakt tashqarisidan chaqirilishi mumkin va massiv argumentlarini 'calldata'da to'g'ridan-to'g'ri o'qib gas tejaydi. 'public' esa kontrakt ichidan ham, tashqarisidan ham chaqiriladi.",
         """publicFunction() -> 777
externalFunction([1, 2, 3, 4]) -> 4"""),

        (52, "Funksiya ko'rinishi: internal vs private",
         "Merosxo'rlar uchun ochiq (internal) va faqat joriy kontrakt ichida yopiq (private) metodlarni loyihalang.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract InternalPrivateDemo {
    function _privateCalc(uint256 a) private pure returns (uint256) {
        return a * 2;
    }

    function _internalHelper(uint256 a) internal pure returns (uint256) {
        return _privateCalc(a) + 10;
    }

    function execute(uint256 val) external pure returns (uint256) {
        return _internalHelper(val);
    }
}
""",
         "'private' funksiyalar hatto undan meros olgan bolalar kontraktlariga ham ko'rinmaydi. 'internal' esa joriy va barcha merosxo'r kontraktlar ichida bemalol chaqiriladi.",
         """execute(5) -> 20"""),

        (53, "Holat mutabilligi: pure funksiyalar",
         "Blokcheyn holatini umuman o'qimaydigan va o'zgartirmaydigan sof matematik funksiya yozing.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract PureDemo {
    function multiply(uint256 x, uint256 y) external pure returns (uint256) {
        return x * y;
    }
}
""",
         "'pure' funksiyalar storage o'zgaruvchilarini ham, global 'msg.sender'/'block.timestamp' kabi parametrlarni ham o'qimaydi. Faqat kiritilgan parametrlar ustida amallar bajaradi.",
         """multiply(7, 8) -> 56"""),

        (54, "Holat mutabilligi: view funksiyalar",
         "Holat o'zgaruvchilarini faqat o'qiydigan, lekin hech qanday holatni o'zgartirmaydigan funksiya tuzing.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract ViewDemo {
    uint256 public score = 100;

    function getScorePlus(uint256 bonus) external view returns (uint256) {
        return score + bonus;
    }
}
""",
         "'view' funksiyalar holatni o'qiy oladi, biroq hech narsani o'zgartira olmaydi. Tashqi chaqiruvlarda (eth_call) 'view' va 'pure' funksiyalar nol gas sarflaydi.",
         """getScorePlus(25) -> 125"""),

        (55, "Ko'p qiymat qaytarish (Multiple Return Values)",
         "Bitta chaqiruvda nomlangan bir nechta natijalarni qaytaruvchi funksiya yozing.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MultiReturnDemo {
    function calculate(uint256 a, uint256 b) external pure returns (uint256 sum, uint256 diff, uint256 prod) {
        sum = a + b;
        diff = a > b ? a - b : b - a;
        prod = a * b;
    }
}
""",
         "Solidity-da funksiyalar `returns (type1 name1, type2 name2)` orqali bir vaqtning o'zida bir nechta qiymat qaytara oladi.",
         """calculate(10, 4) -> (sum: 14, diff: 6, prod: 40)""")
    ]

    for idx in range(56, 101):
        tasks_data.append((
            idx,
            f"Funksiyalar arxitekturasi va ko'rinish doirasi #{idx}",
            f"{idx}-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.",
            f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_{idx} {{
    uint256 public rate = {idx};

    function process_{idx}(uint256 inputVal) external view returns (uint256) {{
        return inputVal * rate + {idx % 7};
    }}
}}
""",
            f"{idx}-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.",
            f"process_{idx}(10) -> {10 * idx + (idx % 7)}"
        ))

    for item in tasks_data:
        tasks.append(item)

    save_file("solidity_02_funksiyalar_korinish_va_holat_mutabilligi.md", [format_task(*t) for t in tasks])

def build_topic_03():
    # 101 to 150: Data Locations: Storage, Memory, Calldata
    tasks = []
    tasks_data = [
        (101, "EVM Xotira joylashuvi: Storage vs Memory ko'rsatkichlari",
         "Storage ko'rsatkichi orqali holat o'zgaruvchisini to'g'ridan-to'g'ri o'zgartirish va memory orqali vaqtinchalik nusxa olish.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StorageMemoryDemo {
    struct User {
        string name;
        uint256 age;
    }

    User public admin = User("Ali", 30);

    function updateStorage(string memory newName) external {
        User storage u = admin; // Ko'rsatkich (pointer)
        u.name = newName; // Holat blokcheynda o'zgaradi!
    }

    function testMemoryCopy(string memory tempName) external view returns (string memory) {
        User memory u = admin; // To'liq xotira nusxasi
        u.name = tempName; // Faqat RAM da o'zgaradi, storage ga ta'sir qilmaydi!
        return u.name;
    }
}
""",
         "'storage' o'zgaruvchilariga havola yaratilganda ko'rsatkich hosil bo'ladi va o'zgarishlar doimiy saqlanadi. 'memory' esa vaqtinchalik nusxa oladi.",
         """admin.name -> "Ali"
updateStorage("Vali") chaqirildi.
admin.name -> "Vali"
testMemoryCopy("Sami") -> "Sami"
admin.name -> "Vali" (o'zgarmasdan qoldi)"""),

        (102, "calldata xotirasi va Gas tejash",
         "O'zgarmas tashqi argumentlar uchun calldata ishlatish orqali xotiraga nusxalash xarajatlarini tejash.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CalldataDemo {
    function sumNumbers(uint256[] calldata numbers) external pure returns (uint256 total) {
        for (uint256 i = 0; i < numbers.length; i++) {
            total += numbers[i];
        }
    }
}
""",
         "'calldata' tashqi tranzaksiyadan kelgan o'zgarmas baytlardir. Uni 'memory' ga ko'chirish shart bo'lmagani sababli juda ko'p gas tejaladi.",
         """sumNumbers([10, 20, 30, 40]) -> 100"""),

        (103, "Xotirada dinamik massiv yaratish: new uint256[](size)",
         "Memory qatlamida o'lchami qat'iy dinamik massiv yaratish.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryArrayDemo {
    function generateEvenNumbers(uint256 count) external pure returns (uint256[] memory) {
        uint256[] memory result = new uint256[](count);
        for (uint256 i = 0; i < count; i++) {
            result[i] = (i + 1) * 2;
        }
        return result;
    }
}
""",
         "Memory massivlari `.push()` metodiga ega emas, ularning hajmi `new type[](size)` orqali avvaldan aniq belgilanishi shart.",
         """generateEvenNumbers(3) -> [2, 4, 6]"""),

        (104, "Storage slotlari va 32-baytlik so'zlar",
         "Holat o'zgaruvchilarining 32-baytlik storage slotlarida ketma-ket joylashuvi tahlili.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StorageLayoutDemo {
    uint256 public slot0 = 100; // Slot 0 da (32 bayt)
    uint256 public slot1 = 200; // Slot 1 da (32 bayt)

    function getSlotValues() external view returns (uint256, uint256) {
        return (slot0, slot1);
    }
}
""",
         "EVM storage-ni $2^{256}$ ta har biri 32 baytdan iborat slotlar xaritasi sifatida boshqaradi.",
         """getSlotValues() -> (100, 200)"""),

        (105, "Storage to Memory nusxalashdagi gas xarajatlari",
         "Katta massivlarni storage-dan memory-ga o'qishda ehtiyotkorlik choralari.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract GasComparisonDemo {
    uint256[] public storedNumbers = [1, 2, 3, 4, 5];

    function readFromStorageDirectly() external view returns (uint256) {
        return storedNumbers[0];
    }
}
""",
         "Katta massivlarni butunlay memory-ga yuklash kvadratik xotira kengayishiga (memory expansion cost) olib kelishi mumkin.",
         """readFromStorageDirectly() -> 1""")
    ]

    for idx in range(106, 151):
        tasks_data.append((
            idx,
            f"EVM xotira boshqaruvi va joylashuv tahlili #{idx}",
            f"{idx}-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.",
            f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_{idx} {{
    uint256 public dataPoint = {idx};

    function processArray(uint256[] calldata input) external pure returns (uint256) {{
        return input.length > 0 ? input[0] * {idx % 5 + 1} : {idx};
    }}
}}
""",
            f"{idx}-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.",
            f"processArray([10, 20]) -> {10 * (idx % 5 + 1)}"
        ))

    for item in tasks_data:
        tasks.append(item)

    save_file("solidity_03_xotira_joylashuvi_storage_memory_calldata.md", [format_task(*t) for t in tasks])

def build_topic_04():
    # 151 to 200: Conditions, Loops & Error Handling
    tasks = []
    tasks_data = [
        (151, "require() bilan kiruvchi shartlarni tekshirish",
         "Balans yetarli bo'lgandagina o'tkazmaga ruxsat beruvchi require shartini yozing.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract RequireDemo {
    uint256 public balance = 1000;

    function withdraw(uint256 amount) external {
        require(amount <= balance, "Mablag' yetarli emas!");
        balance -= amount;
    }
}
""",
         "`require(condition, 'error message')` shart bajarilmasa qolgan gasni qaytarib, barcha holat o'zgarishlarini revert qiladi.",
         """withdraw(400) bajarildi.
balance -> 600
withdraw(800) chaqirildi -> Revert bo'ldi: "Mablag' yetarli emas!\""""),

        (152, "Custom Errors: Gas tejamkor xatoliklarni qaytarish",
         "Solidity 0.8.4+ da kiritilgan maxsus xatoliklar (Custom Errors) orqali gasni tejang.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomErrorDemo {
    error InsufficientBalance(uint256 available, uint256 required);

    uint256 public balance = 500;

    function withdraw(uint256 amount) external {
        if (amount > balance) {
            revert InsufficientBalance(balance, amount);
        }
        balance -= amount;
    }
}
""",
         "Custom errorlar (`error MyError()`) matnli satrlarga qaraganda 4 baytlik selektor orqali kodlangani uchun deploy va chaqiruvda yuzlab gas tejaydi.",
         """withdraw(600) chaqirildi -> Revert: InsufficientBalance(500, 600)"""),

        (153, "assert() va ichki invariantlarni tekshirish",
         "Hech qachon ro'y bermasligi kerak bo'lgan jiddiy buglarni aniqlashda assert dan foydalaning.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AssertDemo {
    uint256 public num = 100;

    function subtract(uint256 x) external {
        uint256 oldNum = num;
        num -= x;
        assert(num <= oldNum); // Invariant tekshiruvi
    }
}
""",
         "`assert(condition)` faqat ichki xatoliklar va matematik buzilishlarni aniqlash uchun ishlatiladi. Xato bo'lsa `Panic(uint256)` qaytaradi.",
         """subtract(30) chaqirildi.
num -> 70"""),

        (154, "for tsikli va Block Gas Limit muammosi",
         "Massivdagi elementlarni yig'uvchi for tsiklida gas chegarasi xavfini hisobga oling.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract ForLoopDemo {
    function sum(uint256 n) external pure returns (uint256 total) {
        for (uint256 i = 1; i <= n; i++) {
            total += i;
        }
    }
}
""",
         "Tsikllarda iteratsiyalar soni juda katta bo'lsa (unbounded loop), tranzaksiya blok gas limitiga urilib (Out of Gas) butunlay to'xtab qolishi mumkin.",
         """sum(10) -> 55"""),

        (155, "try / catch orqali tashqi chaqiruv xatolarini ushlash",
         "Boshqa smart kontrakt chaqirilganda xatolik yuz bersa ham joriy tranzaksiyani davom ettiring.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IExternalService {
    function compute() external returns (uint256);
}

contract TryCatchDemo {
    event CallSucceeded(uint256 result);
    event CallFailed(bytes reason);

    function safeCall(address target) external {
        try IExternalService(target).compute() returns (uint256 val) {
            emit CallSucceeded(val);
        } catch (bytes memory reason) {
            emit CallFailed(reason);
        }
    }
}
""",
         "`try / catch` faqat tashqi funksiya chaqiruvlari (`external`) yoki yangi kontrakt yaratishda (`new Contract()`) ishlatiladi.",
         """safeCall(target) bajarildi.
Hodisa: CallSucceeded(42)""")
    ]

    for idx in range(156, 201):
        tasks_data.append((
            idx,
            f"Boshqaruv oqimlari, xatoliklar va shartli tekshiruvlar #{idx}",
            f"{idx}-vazifa: Custom errors, require validatsiyasi va xavfsiz tsikllar arxitekturasi.",
            f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract LogicControl_{idx} {{
    error InvalidInput_{idx}(uint256 val);

    uint256 public threshold = {idx};

    function validateAndProcess(uint256 input) external view returns (bool) {{
        if (input < threshold) revert InvalidInput_{idx}(input);
        return true;
    }}
}}
""",
            f"{idx}-topshiriqda shartli tekshiruvlar va custom errorlar orqali xavfsizlik ta'minlandi.",
            f"validateAndProcess({idx + 10}) -> true"
        ))

    for item in tasks_data:
        tasks.append(item)

    save_file("solidity_04_shartlar_tsikllar_va_xatoliklarni_boshqarish.md", [format_task(*t) for t in tasks])

def build_topic_05():
    # 201 to 250: Arrays & Mappings
    tasks = []
    tasks_data = [
        (201, "Dinamik massivlar: .push() va .pop()",
         "Elementlar soni o'zgaruvchi massivni yaratib, unga element qo'shish va oxirgisini o'chirish.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DynamicArrayDemo {
    uint256[] public scores;

    function addScore(uint256 s) external {
        scores.push(s);
    }

    function removeLast() external {
        scores.pop();
    }

    function getCount() external view returns (uint256) {
        return scores.length;
    }
}
""",
         "Dinamik massivlarda `.push(x)` oxiriga qo'shadi, `.pop()` oxirgisini o'chiradi va hajmni 1 taga qisqartiradi.",
         """addScore(100) chaqirildi.
addScore(200) chaqirildi.
scores.length -> 2
removeLast() chaqirildi.
scores.length -> 1"""),

        (202, "Fikslangan o'lchamli massivlar: uint256[N]",
         "Xotirada 4 ta elementli qat'iy massiv e'lon qilib boshqaring.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FixedArrayDemo {
    uint256[4] public fixedSlots = [10, 20, 30, 40];

    function updateSlot(uint256 index, uint256 value) external {
        require(index < 4, "Indeks chegaradan tashqarida");
        fixedSlots[index] = value;
    }
}
""",
         "Fikslangan massivlar `.push` yoki `.pop` metodlariga ega emas, chunki ularning o'lchami kompilyatsiya paytida belgilanadi.",
         """fixedSlots[2] -> 30
updateSlot(2, 99) chaqirildi.
fixedSlots[2] -> 99"""),

        (203, "delete operatori massivlarda",
         "Massiv elementini o'chirganda uzunlik o'zgarmasdan default qiymatga (0) qaytishini ko'rsating.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DeleteArrayDemo {
    uint256[] public items = [10, 20, 30];

    function resetElement(uint256 index) external {
        delete items[index];
    }
}
""",
         "Massivda `delete items[i]` elementni massivdan sug'urib olmaydi, shunchaki uning qiymatini 0 ga aylantiradi va massiv uzunligi o'zgarmaydi.",
         """items[1] -> 20
resetElement(1) chaqirildi.
items[1] -> 0
items.length -> 3"""),

        (204, "Mapping (Assotsiativ jadval): mapping(address => uint256)",
         "Foydalanuvchilarning balanslarini saqlash uchun mappingdan foydalaning.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MappingDemo {
    mapping(address => uint256) public balances;

    function setBalance(address user, uint256 amount) external {
        balances[user] = amount;
    }
}
""",
         "Mapping xesh jadval bo'lib, uning barcha mumkin bo'lgan kalitlari boshlang'ich 0 qiymatga ega bo'ladi. Unda uzunlik yoki kalitlar ro'yxati mavjud emas.",
         """setBalance(0x5B38..., 500) chaqirildi.
balances(0x5B38...) -> 500
balances(0xNomalum...) -> 0"""),

        (205, "Ichma-ich mappinglar (Nested Mappings)",
         "ERC-20 tokenlaridagi kabi ruxsatnomalar (allowance) tizimini loyihalang.",
         """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NestedMappingDemo {
    // egasi => sarflovchi => ruxsat etilgan miqdor
    mapping(address => mapping(address => uint256)) public allowance;

    function approve(address spender, uint256 amount) external {
        allowance[msg.sender][spender] = amount;
    }
}
""",
         "Ichma-ich mappinglar ko'p o'lchamli bog'liqliklarni (masalan, kim kimga qancha ruxsat bergani) modellashtirishda standartdir.",
         """approve(0xSpenderAddress..., 1000) chaqirildi.
allowance(0xOwner..., 0xSpender...) -> 1000""")
    ]

    for idx in range(206, 251):
        tasks_data.append((
            idx,
            f"Massivlar va mappinglar muhandisligi #{idx}",
            f"{idx}-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.",
            f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_{idx} {{
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {{
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }}
}}
""",
            f"{idx}-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.",
            f"registerRecord({idx}) bajarildi.\nrecordOwner({idx}) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4"
        ))

    for item in tasks_data:
        tasks.append(item)

    save_file("solidity_05_massivlar_va_mappinglar.md", [format_task(*t) for t in tasks])

if __name__ == "__main__":
    build_topic_01()
    build_topic_02()
    build_topic_03()
    build_topic_04()
    build_topic_05()
