# 1-Topshiriq: SPDX Litsenziyasi va Pragma direktivasi
## Topshiriq sharti:
Smart kontrakt boshida SPDX litsenziyasi va Solidity kompilyator versiyasini e'lon qiling hamda oddiy salomlashuv kontraktini yozing.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract HelloWorld {
    string public greeting = "Salom, Web3 Dunyosi!";
}
```

## Tushuntirish va Mantiq:
Har bir zamonaviy Solidity fayli SPDX litsenziyasi (masalan, MIT, GPL-3.0) va 'pragma solidity' direktivasi bilan boshlanishi shart. Bu kompilyatorning to'g'ri versiyasini va ochiq kod litsenziyasini belgilaydi.

## Ishlash natijasi:
```text
Kontrakt deploy qilindi.
greeting() -> "Salom, Web3 Dunyosi!"
```


# 2-Topshiriq: Butun son turlari: uint256 va uning diapazoni
## Topshiriq sharti:
Musbat butun son (uint256) holat o'zgaruvchisini e'lon qiling va unga qiymat berib o'qing.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract UnsignedIntegerDemo {
    uint256 public totalTokens = 1000000;
    uint8 public smallNumber = 255; // 0 dan 255 gacha (1 bayt)

    function getMaxUint256() external pure returns (uint256) {
        return type(uint256).max;
    }
}
```

## Tushuntirish va Mantiq:
Solidity-da 'uint' - bu 'uint256' ning qisqartmasi bo'lib, 0 dan 2^256 - 1 gacha qiymat oladi. 'uint8' dan 'uint256' gacha 8 ning karralari ko'rinishidagi turlar mavjud.

## Ishlash natijasi:
```text
totalTokens -> 1000000
smallNumber -> 255
getMaxUint256() -> 115792089237316195423570985008687907853269984665640564039457584007913129639935
```


# 3-Topshiriq: Manfiy va musbat butun sonlar: int256
## Topshiriq sharti:
Harorat yoki foyda/zarar kabi manfiy qiymatlarni ifodalovchi 'int256' o'zgaruvchisini yarating.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SignedIntegerDemo {
    int256 public profitLoss = -500;

    function adjustProfit(int256 delta) external {
        profitLoss += delta;
    }
}
```

## Tushuntirish va Mantiq:
'int' turi ikkilik to'ldiruvchi (two's complement) ko'rinishidagi ishorali sonlarni ifodalaydi va manfiy qiymatlarni saqlay oladi.

## Ishlash natijasi:
```text
profitLoss -> -500
adjustProfit(1200) chaqirildi.
profitLoss -> 700
```


# 4-Topshiriq: Mantiqiy tur: boolean (bool)
## Topshiriq sharti:
Tizim faolligini bildiruvchi 'isActive' flagini boshqaring.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BooleanDemo {
    bool public isActive = true;

    function toggleStatus() external {
        isActive = !isActive;
    }
}
```

## Tushuntirish va Mantiq:
Solidity-da 'bool' turi faqat 'true' yoki 'false' qiymatlarini qabul qiladi. Standart (default) qiymati 'false' hisoblanadi.

## Ishlash natijasi:
```text
isActive -> true
toggleStatus() chaqirildi.
isActive -> false
```


# 5-Topshiriq: Ethereum manzili: address va address payable
## Topshiriq sharti:
Oddiy address va efir qabul qila oladigan address payable turlari o'rtasidagi farqni ko'rsating.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
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
```

## Tushuntirish va Mantiq:
'address' 20 baytlik Ethereum hisob manzilini saqlaydi. 'address payable' esa qo'shimcha ravishda '.transfer()' va '.send()' metodlariga ega bo'lib, unga ETH yuborish mumkin.

## Ishlash natijasi:
```text
owner -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
getBalance(owner) -> 99999999999999999000 wei
```


# 6-Topshiriq: Ruxsat etilgan baytlar: bytes1 dan bytes32 gacha
## Topshiriq sharti:
Kriptografik xeshlar va identifikatorlar uchun optimallashtirilgan bytes32 turini e'lon qiling.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FixedBytesDemo {
    bytes32 public contractHash = 0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470;
    bytes4 public functionSelector = 0xa9059cbb; // transfer(address,uint256)

    function getBytesLength() external pure returns (uint256) {
        return 32;
    }
}
```

## Tushuntirish va Mantiq:
bytes1...bytes32 qat'iy o'lchamli baytlar massivi bo'lib, EVM-da 'string' yoki dinamik 'bytes'ga qaraganda ancha kam gas sarflaydi.

## Ishlash natijasi:
```text
contractHash -> 0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470
functionSelector -> 0xa9059cbb
```


# 7-Topshiriq: Dinamik satrlar: string turi va xususiyatlari
## Topshiriq sharti:
Foydalanuvchi ismini saqlash va satrlar uzunligini baytlarda hisoblash.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StringDemo {
    string public userName = "Alpomish";

    function getByteLength() external view returns (uint256) {
        return bytes(userName).length;
    }
}
```

## Tushuntirish va Mantiq:
Solidity-da 'string' UTF-8 formatidagi dinamik baytlar ketma-ketligidir. Unda to'g'ridan-to'g'ri .length yo'q, shuning uchun 'bytes(str).length' orqali olinadi.

## Ishlash natijasi:
```text
userName -> "Alpomish"
getByteLength() -> 8
```


# 8-Topshiriq: Global o'zgaruvchi: msg.sender
## Topshiriq sharti:
Tranzaksiyani chaqirgan manzilni saqlab oluvchi kontrakt yozing.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MsgSenderDemo {
    address public lastCaller;

    function callMe() external {
        lastCaller = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
'msg.sender' joriy funksiya chaqiruvini bevosita amalga oshirgan hamyon yoki kontrakt manzilini ifodalaydi. Xavfsizlikda kirish nazorati uchun asosiy vositadir.

## Ishlash natijasi:
```text
lastCaller -> 0x0000000000000000000000000000000000000000
callMe() chaqirildi.
lastCaller -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 9-Topshiriq: Global o'zgaruvchi: msg.value va payable funksiya
## Topshiriq sharti:
Kontraktga yuborilgan efir (ETH/wei) miqdorini aniqlang.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MsgValueDemo {
    uint256 public totalReceived;

    function deposit() external payable {
        totalReceived += msg.value;
    }
}
```

## Tushuntirish va Mantiq:
'msg.value' tranzaksiya bilan birga kontraktga yuborilgan wei miqdorini bildiradi. U faqat 'payable' bilan belgilangan funksiyalarda ishlatilishi mumkin.

## Ishlash natijasi:
```text
deposit{value: 1 ether}() bajarildi.
totalReceived -> 1000000000000000000 wei
```


# 10-Topshiriq: Global o'zgaruvchilar: block.timestamp va block.number
## Topshiriq sharti:
Joriy blok raqami va vaqtini tekshiruvchi funksiya yozing.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BlockGlobalsDemo {
    function getBlockInfo() external view returns (uint256 currentBlock, uint256 blockTime) {
        return (block.number, block.timestamp);
    }
}
```

## Tushuntirish va Mantiq:
'block.timestamp' konchi/validator tomonidan blok muhrlangan Unix vaqtini (sekundlarda) bildiradi. 'block.number' esa zanjirdagi joriy blok balandligidir.

## Ishlash natijasi:
```text
getBlockInfo() -> (19450200, 1700000000)
```


# 11-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #11
## Topshiriq sharti:
11-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_11 {
    uint256 public constant BASE_FACTOR = 11;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
11-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_11 deploy qilindi.
increment(2) -> 22
```


# 12-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #12
## Topshiriq sharti:
12-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_12 {
    uint256 public constant BASE_FACTOR = 12;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
12-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_12 deploy qilindi.
increment(2) -> 24
```


# 13-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #13
## Topshiriq sharti:
13-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_13 {
    uint256 public constant BASE_FACTOR = 13;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
13-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_13 deploy qilindi.
increment(2) -> 26
```


# 14-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #14
## Topshiriq sharti:
14-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_14 {
    uint256 public constant BASE_FACTOR = 14;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
14-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_14 deploy qilindi.
increment(2) -> 28
```


# 15-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #15
## Topshiriq sharti:
15-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_15 {
    uint256 public constant BASE_FACTOR = 15;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
15-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_15 deploy qilindi.
increment(2) -> 30
```


# 16-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #16
## Topshiriq sharti:
16-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_16 {
    uint256 public constant BASE_FACTOR = 16;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
16-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_16 deploy qilindi.
increment(2) -> 32
```


# 17-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #17
## Topshiriq sharti:
17-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_17 {
    uint256 public constant BASE_FACTOR = 17;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
17-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_17 deploy qilindi.
increment(2) -> 34
```


# 18-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #18
## Topshiriq sharti:
18-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_18 {
    uint256 public constant BASE_FACTOR = 18;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
18-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_18 deploy qilindi.
increment(2) -> 36
```


# 19-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #19
## Topshiriq sharti:
19-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_19 {
    uint256 public constant BASE_FACTOR = 19;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
19-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_19 deploy qilindi.
increment(2) -> 38
```


# 20-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #20
## Topshiriq sharti:
20-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_20 {
    uint256 public constant BASE_FACTOR = 20;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
20-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_20 deploy qilindi.
increment(2) -> 40
```


# 21-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #21
## Topshiriq sharti:
21-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_21 {
    uint256 public constant BASE_FACTOR = 21;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
21-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_21 deploy qilindi.
increment(2) -> 42
```


# 22-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #22
## Topshiriq sharti:
22-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_22 {
    uint256 public constant BASE_FACTOR = 22;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
22-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_22 deploy qilindi.
increment(2) -> 44
```


# 23-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #23
## Topshiriq sharti:
23-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_23 {
    uint256 public constant BASE_FACTOR = 23;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
23-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_23 deploy qilindi.
increment(2) -> 46
```


# 24-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #24
## Topshiriq sharti:
24-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_24 {
    uint256 public constant BASE_FACTOR = 24;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
24-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_24 deploy qilindi.
increment(2) -> 48
```


# 25-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #25
## Topshiriq sharti:
25-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_25 {
    uint256 public constant BASE_FACTOR = 25;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
25-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_25 deploy qilindi.
increment(2) -> 50
```


# 26-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #26
## Topshiriq sharti:
26-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_26 {
    uint256 public constant BASE_FACTOR = 26;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
26-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_26 deploy qilindi.
increment(2) -> 52
```


# 27-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #27
## Topshiriq sharti:
27-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_27 {
    uint256 public constant BASE_FACTOR = 27;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
27-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_27 deploy qilindi.
increment(2) -> 54
```


# 28-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #28
## Topshiriq sharti:
28-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_28 {
    uint256 public constant BASE_FACTOR = 28;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
28-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_28 deploy qilindi.
increment(2) -> 56
```


# 29-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #29
## Topshiriq sharti:
29-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_29 {
    uint256 public constant BASE_FACTOR = 29;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
29-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_29 deploy qilindi.
increment(2) -> 58
```


# 30-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #30
## Topshiriq sharti:
30-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_30 {
    uint256 public constant BASE_FACTOR = 30;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
30-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_30 deploy qilindi.
increment(2) -> 60
```


# 31-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #31
## Topshiriq sharti:
31-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_31 {
    uint256 public constant BASE_FACTOR = 31;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
31-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_31 deploy qilindi.
increment(2) -> 62
```


# 32-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #32
## Topshiriq sharti:
32-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_32 {
    uint256 public constant BASE_FACTOR = 32;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
32-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_32 deploy qilindi.
increment(2) -> 64
```


# 33-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #33
## Topshiriq sharti:
33-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_33 {
    uint256 public constant BASE_FACTOR = 33;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
33-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_33 deploy qilindi.
increment(2) -> 66
```


# 34-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #34
## Topshiriq sharti:
34-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_34 {
    uint256 public constant BASE_FACTOR = 34;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
34-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_34 deploy qilindi.
increment(2) -> 68
```


# 35-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #35
## Topshiriq sharti:
35-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_35 {
    uint256 public constant BASE_FACTOR = 35;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
35-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_35 deploy qilindi.
increment(2) -> 70
```


# 36-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #36
## Topshiriq sharti:
36-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_36 {
    uint256 public constant BASE_FACTOR = 36;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
36-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_36 deploy qilindi.
increment(2) -> 72
```


# 37-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #37
## Topshiriq sharti:
37-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_37 {
    uint256 public constant BASE_FACTOR = 37;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
37-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_37 deploy qilindi.
increment(2) -> 74
```


# 38-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #38
## Topshiriq sharti:
38-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_38 {
    uint256 public constant BASE_FACTOR = 38;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
38-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_38 deploy qilindi.
increment(2) -> 76
```


# 39-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #39
## Topshiriq sharti:
39-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_39 {
    uint256 public constant BASE_FACTOR = 39;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
39-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_39 deploy qilindi.
increment(2) -> 78
```


# 40-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #40
## Topshiriq sharti:
40-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_40 {
    uint256 public constant BASE_FACTOR = 40;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
40-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_40 deploy qilindi.
increment(2) -> 80
```


# 41-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #41
## Topshiriq sharti:
41-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_41 {
    uint256 public constant BASE_FACTOR = 41;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
41-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_41 deploy qilindi.
increment(2) -> 82
```


# 42-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #42
## Topshiriq sharti:
42-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_42 {
    uint256 public constant BASE_FACTOR = 42;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
42-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_42 deploy qilindi.
increment(2) -> 84
```


# 43-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #43
## Topshiriq sharti:
43-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_43 {
    uint256 public constant BASE_FACTOR = 43;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
43-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_43 deploy qilindi.
increment(2) -> 86
```


# 44-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #44
## Topshiriq sharti:
44-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_44 {
    uint256 public constant BASE_FACTOR = 44;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
44-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_44 deploy qilindi.
increment(2) -> 88
```


# 45-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #45
## Topshiriq sharti:
45-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_45 {
    uint256 public constant BASE_FACTOR = 45;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
45-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_45 deploy qilindi.
increment(2) -> 90
```


# 46-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #46
## Topshiriq sharti:
46-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_46 {
    uint256 public constant BASE_FACTOR = 46;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
46-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_46 deploy qilindi.
increment(2) -> 92
```


# 47-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #47
## Topshiriq sharti:
47-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_47 {
    uint256 public constant BASE_FACTOR = 47;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
47-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_47 deploy qilindi.
increment(2) -> 94
```


# 48-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #48
## Topshiriq sharti:
48-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_48 {
    uint256 public constant BASE_FACTOR = 48;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
48-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_48 deploy qilindi.
increment(2) -> 96
```


# 49-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #49
## Topshiriq sharti:
49-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_49 {
    uint256 public constant BASE_FACTOR = 49;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
49-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_49 deploy qilindi.
increment(2) -> 98
```


# 50-Topshiriq: Solidity asoslari, konstantalar va holat o'zgaruvchilari #50
## Topshiriq sharti:
50-vazifa: Konstantalar (constant/immutable), xotira qoidalari va xavfsiz arifmetika amaliyoti.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicState_50 {
    uint256 public constant BASE_FACTOR = 50;
    uint256 public immutable deployedTime;
    uint256 public counter;

    constructor() {
        deployedTime = block.timestamp;
    }

    function increment(uint256 amount) external returns (uint256) {
        counter += amount * BASE_FACTOR;
        return counter;
    }
}
```

## Tushuntirish va Mantiq:
50-topshiriqda 'constant' va 'immutable' kalit so'zlari yordamida gas tejamkorligi va holat boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
Kontrakt BasicState_50 deploy qilindi.
increment(2) -> 100
```

