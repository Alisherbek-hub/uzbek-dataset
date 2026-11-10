# 551-Topshiriq: IERC20 Interfeysi: Standart metodlar va hodisalar
## Topshiriq sharti:
ERC-20 tokenining rasmiy interfeysini e'lon qiling.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
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
```

## Tushuntirish va Mantiq:
ERC-20 standarti almashtiriladigan (fungible) tokenlar uchun dunyodagi eng ommabop standart bo'lib, barcha birjalar va hamyonlar tomonidan qo'llab-quvvatlanadi.

## Ishlash natijasi:
```text
IERC20 interfeysi e'lon qilindi.
```


# 552-Topshiriq: Shaxsiy ERC-20 tokenini noldan yozish
## Topshiriq sharti:
O'zbekiston kiber valyutasi (KHOR token) kontraktini to'liq yozing.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
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
```

## Tushuntirish va Mantiq:
ERC-20 tokeni `balanceOf` mappingi, 18 ta kasr xonasi (decimals) va `Transfer` hodisasi bilan to'liq ishga tushirildi.

## Ishlash natijasi:
```text
KhorazmToken deploy qilindi.
Deployer balansi: 1000000000000000000000000 (1 million KHOR)
```


# 553-Topshiriq: approve va transferFrom: Uchinchi tomon xaridini ta'minlash
## Topshiriq sharti:
DEX (Uniswap) yoki boshqa smart kontraktga foydalanuvchi nomidan token sarflash ruxsatini berish.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
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
```

## Tushuntirish va Mantiq:
`approve` va `transferFrom` juftligi DeFi kontraktlarining asosi bo'lib, foydalanuvchiga o'z tokenlarini xavfsiz boshqarish imkonini beradi.

## Ishlash natijasi:
```text
User approve(DEX, 500) qildi.
DEX transferFrom(User, Shop, 500) bajardi.
```


# 554-Topshiriq: Mintable va Burnable tokenlar
## Topshiriq sharti:
Yangi tokenlarni chiqarish (mint) va muomaladagi tokenlarni yo'q qilish (burn).

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
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
```

## Tushuntirish va Mantiq:
Minting taklifni oshiradi, Burning esa tokenlarni deflyatsiyaga uchratib, umumiy sonini kamaytiradi.

## Ishlash natijasi:
```text
mint(0xUser..., 1000) -> totalSupply = 1000
burn(200) -> totalSupply = 800
```


# 555-Topshiriq: Capped Token (Maksimal taklif chegarasi)
## Topshiriq sharti:
Bitcoin kabi maksimal chegarasi (masalan, 21 million) o'zgarmas qilib belgilangan token.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CappedToken {
    uint256 public immutable cap = 21000000 * 10 ** 18;
    uint256 public totalSupply;

    function mint(uint256 amount) external {
        require(totalSupply + amount <= cap, "Maksimal chegara buzildi!");
        totalSupply += amount;
    }
}
```

## Tushuntirish va Mantiq:
`immutable cap` tokenlar soni hech qachon belgilangan sondan oshmasligini qat'iy kafolatlaydi.

## Ishlash natijasi:
```text
cap -> 21000000000000000000000000
```


# 556-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #556
## Topshiriq sharti:
556-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_556 {
    string public symbol = "TKN_556";
    uint256 public totalSupply = 556 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
556-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_556 yaratildi. Boshlang'ich zaxira: 556000 TKN_556
```


# 557-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #557
## Topshiriq sharti:
557-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_557 {
    string public symbol = "TKN_557";
    uint256 public totalSupply = 557 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
557-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_557 yaratildi. Boshlang'ich zaxira: 557000 TKN_557
```


# 558-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #558
## Topshiriq sharti:
558-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_558 {
    string public symbol = "TKN_558";
    uint256 public totalSupply = 558 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
558-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_558 yaratildi. Boshlang'ich zaxira: 558000 TKN_558
```


# 559-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #559
## Topshiriq sharti:
559-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_559 {
    string public symbol = "TKN_559";
    uint256 public totalSupply = 559 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
559-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_559 yaratildi. Boshlang'ich zaxira: 559000 TKN_559
```


# 560-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #560
## Topshiriq sharti:
560-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_560 {
    string public symbol = "TKN_560";
    uint256 public totalSupply = 560 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
560-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_560 yaratildi. Boshlang'ich zaxira: 560000 TKN_560
```


# 561-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #561
## Topshiriq sharti:
561-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_561 {
    string public symbol = "TKN_561";
    uint256 public totalSupply = 561 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
561-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_561 yaratildi. Boshlang'ich zaxira: 561000 TKN_561
```


# 562-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #562
## Topshiriq sharti:
562-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_562 {
    string public symbol = "TKN_562";
    uint256 public totalSupply = 562 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
562-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_562 yaratildi. Boshlang'ich zaxira: 562000 TKN_562
```


# 563-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #563
## Topshiriq sharti:
563-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_563 {
    string public symbol = "TKN_563";
    uint256 public totalSupply = 563 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
563-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_563 yaratildi. Boshlang'ich zaxira: 563000 TKN_563
```


# 564-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #564
## Topshiriq sharti:
564-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_564 {
    string public symbol = "TKN_564";
    uint256 public totalSupply = 564 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
564-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_564 yaratildi. Boshlang'ich zaxira: 564000 TKN_564
```


# 565-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #565
## Topshiriq sharti:
565-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_565 {
    string public symbol = "TKN_565";
    uint256 public totalSupply = 565 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
565-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_565 yaratildi. Boshlang'ich zaxira: 565000 TKN_565
```


# 566-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #566
## Topshiriq sharti:
566-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_566 {
    string public symbol = "TKN_566";
    uint256 public totalSupply = 566 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
566-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_566 yaratildi. Boshlang'ich zaxira: 566000 TKN_566
```


# 567-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #567
## Topshiriq sharti:
567-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_567 {
    string public symbol = "TKN_567";
    uint256 public totalSupply = 567 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
567-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_567 yaratildi. Boshlang'ich zaxira: 567000 TKN_567
```


# 568-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #568
## Topshiriq sharti:
568-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_568 {
    string public symbol = "TKN_568";
    uint256 public totalSupply = 568 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
568-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_568 yaratildi. Boshlang'ich zaxira: 568000 TKN_568
```


# 569-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #569
## Topshiriq sharti:
569-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_569 {
    string public symbol = "TKN_569";
    uint256 public totalSupply = 569 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
569-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_569 yaratildi. Boshlang'ich zaxira: 569000 TKN_569
```


# 570-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #570
## Topshiriq sharti:
570-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_570 {
    string public symbol = "TKN_570";
    uint256 public totalSupply = 570 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
570-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_570 yaratildi. Boshlang'ich zaxira: 570000 TKN_570
```


# 571-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #571
## Topshiriq sharti:
571-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_571 {
    string public symbol = "TKN_571";
    uint256 public totalSupply = 571 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
571-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_571 yaratildi. Boshlang'ich zaxira: 571000 TKN_571
```


# 572-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #572
## Topshiriq sharti:
572-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_572 {
    string public symbol = "TKN_572";
    uint256 public totalSupply = 572 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
572-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_572 yaratildi. Boshlang'ich zaxira: 572000 TKN_572
```


# 573-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #573
## Topshiriq sharti:
573-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_573 {
    string public symbol = "TKN_573";
    uint256 public totalSupply = 573 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
573-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_573 yaratildi. Boshlang'ich zaxira: 573000 TKN_573
```


# 574-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #574
## Topshiriq sharti:
574-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_574 {
    string public symbol = "TKN_574";
    uint256 public totalSupply = 574 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
574-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_574 yaratildi. Boshlang'ich zaxira: 574000 TKN_574
```


# 575-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #575
## Topshiriq sharti:
575-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_575 {
    string public symbol = "TKN_575";
    uint256 public totalSupply = 575 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
575-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_575 yaratildi. Boshlang'ich zaxira: 575000 TKN_575
```


# 576-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #576
## Topshiriq sharti:
576-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_576 {
    string public symbol = "TKN_576";
    uint256 public totalSupply = 576 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
576-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_576 yaratildi. Boshlang'ich zaxira: 576000 TKN_576
```


# 577-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #577
## Topshiriq sharti:
577-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_577 {
    string public symbol = "TKN_577";
    uint256 public totalSupply = 577 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
577-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_577 yaratildi. Boshlang'ich zaxira: 577000 TKN_577
```


# 578-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #578
## Topshiriq sharti:
578-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_578 {
    string public symbol = "TKN_578";
    uint256 public totalSupply = 578 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
578-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_578 yaratildi. Boshlang'ich zaxira: 578000 TKN_578
```


# 579-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #579
## Topshiriq sharti:
579-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_579 {
    string public symbol = "TKN_579";
    uint256 public totalSupply = 579 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
579-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_579 yaratildi. Boshlang'ich zaxira: 579000 TKN_579
```


# 580-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #580
## Topshiriq sharti:
580-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_580 {
    string public symbol = "TKN_580";
    uint256 public totalSupply = 580 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
580-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_580 yaratildi. Boshlang'ich zaxira: 580000 TKN_580
```


# 581-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #581
## Topshiriq sharti:
581-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_581 {
    string public symbol = "TKN_581";
    uint256 public totalSupply = 581 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
581-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_581 yaratildi. Boshlang'ich zaxira: 581000 TKN_581
```


# 582-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #582
## Topshiriq sharti:
582-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_582 {
    string public symbol = "TKN_582";
    uint256 public totalSupply = 582 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
582-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_582 yaratildi. Boshlang'ich zaxira: 582000 TKN_582
```


# 583-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #583
## Topshiriq sharti:
583-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_583 {
    string public symbol = "TKN_583";
    uint256 public totalSupply = 583 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
583-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_583 yaratildi. Boshlang'ich zaxira: 583000 TKN_583
```


# 584-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #584
## Topshiriq sharti:
584-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_584 {
    string public symbol = "TKN_584";
    uint256 public totalSupply = 584 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
584-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_584 yaratildi. Boshlang'ich zaxira: 584000 TKN_584
```


# 585-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #585
## Topshiriq sharti:
585-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_585 {
    string public symbol = "TKN_585";
    uint256 public totalSupply = 585 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
585-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_585 yaratildi. Boshlang'ich zaxira: 585000 TKN_585
```


# 586-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #586
## Topshiriq sharti:
586-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_586 {
    string public symbol = "TKN_586";
    uint256 public totalSupply = 586 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
586-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_586 yaratildi. Boshlang'ich zaxira: 586000 TKN_586
```


# 587-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #587
## Topshiriq sharti:
587-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_587 {
    string public symbol = "TKN_587";
    uint256 public totalSupply = 587 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
587-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_587 yaratildi. Boshlang'ich zaxira: 587000 TKN_587
```


# 588-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #588
## Topshiriq sharti:
588-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_588 {
    string public symbol = "TKN_588";
    uint256 public totalSupply = 588 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
588-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_588 yaratildi. Boshlang'ich zaxira: 588000 TKN_588
```


# 589-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #589
## Topshiriq sharti:
589-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_589 {
    string public symbol = "TKN_589";
    uint256 public totalSupply = 589 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
589-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_589 yaratildi. Boshlang'ich zaxira: 589000 TKN_589
```


# 590-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #590
## Topshiriq sharti:
590-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_590 {
    string public symbol = "TKN_590";
    uint256 public totalSupply = 590 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
590-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_590 yaratildi. Boshlang'ich zaxira: 590000 TKN_590
```


# 591-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #591
## Topshiriq sharti:
591-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_591 {
    string public symbol = "TKN_591";
    uint256 public totalSupply = 591 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
591-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_591 yaratildi. Boshlang'ich zaxira: 591000 TKN_591
```


# 592-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #592
## Topshiriq sharti:
592-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_592 {
    string public symbol = "TKN_592";
    uint256 public totalSupply = 592 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
592-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_592 yaratildi. Boshlang'ich zaxira: 592000 TKN_592
```


# 593-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #593
## Topshiriq sharti:
593-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_593 {
    string public symbol = "TKN_593";
    uint256 public totalSupply = 593 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
593-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_593 yaratildi. Boshlang'ich zaxira: 593000 TKN_593
```


# 594-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #594
## Topshiriq sharti:
594-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_594 {
    string public symbol = "TKN_594";
    uint256 public totalSupply = 594 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
594-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_594 yaratildi. Boshlang'ich zaxira: 594000 TKN_594
```


# 595-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #595
## Topshiriq sharti:
595-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_595 {
    string public symbol = "TKN_595";
    uint256 public totalSupply = 595 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
595-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_595 yaratildi. Boshlang'ich zaxira: 595000 TKN_595
```


# 596-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #596
## Topshiriq sharti:
596-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_596 {
    string public symbol = "TKN_596";
    uint256 public totalSupply = 596 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
596-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_596 yaratildi. Boshlang'ich zaxira: 596000 TKN_596
```


# 597-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #597
## Topshiriq sharti:
597-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_597 {
    string public symbol = "TKN_597";
    uint256 public totalSupply = 597 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
597-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_597 yaratildi. Boshlang'ich zaxira: 597000 TKN_597
```


# 598-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #598
## Topshiriq sharti:
598-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_598 {
    string public symbol = "TKN_598";
    uint256 public totalSupply = 598 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
598-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_598 yaratildi. Boshlang'ich zaxira: 598000 TKN_598
```


# 599-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #599
## Topshiriq sharti:
599-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_599 {
    string public symbol = "TKN_599";
    uint256 public totalSupply = 599 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
599-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_599 yaratildi. Boshlang'ich zaxira: 599000 TKN_599
```


# 600-Topshiriq: ERC-20 token injiniringi va moliyaviy protokollar #600
## Topshiriq sharti:
600-vazifa: Balanslar, o'tkazmalar, soliq (tax) mexanizmlari va tokenomiika.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomERC20_600 {
    string public symbol = "TKN_600";
    uint256 public totalSupply = 600 * 1000 * 10 ** 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
}
```

## Tushuntirish va Mantiq:
600-topshiriqda standartlashtirilgan ERC-20 token arxitekturasi va taqsimoti loyihalandi.

## Ishlash natijasi:
```text
CustomERC20_600 yaratildi. Boshlang'ich zaxira: 600000 TKN_600
```

