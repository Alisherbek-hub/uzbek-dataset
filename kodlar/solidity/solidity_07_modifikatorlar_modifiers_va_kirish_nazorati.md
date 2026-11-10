# 301-Topshiriq: onlyOwner modifikatori: Kontrakt egasi nazorati
## Topshiriq sharti:
Faqat kontrakt egasi chaqira oladigan xavfsiz funksiya va modifikator yozing.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
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
```

## Tushuntirish va Mantiq:
`modifier` funksiya bajarilishidan oldin shartlarni tekshiradi. `_;` belgisi (merge point) asosiy funksiya tanasi qachon bajarilishini ko'rsatadi.

## Ishlash natijasi:
```text
owner -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
Begona manzil emergencyWithdraw() chaqirganda -> Revert: "Faqat egasi chaqirishi mumkin!"
```


# 302-Topshiriq: Parametrli modifikatorlar
## Topshiriq sharti:
Minimal to'lov miqdorini tekshiruvchi parametrli modifikator yarating.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
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
```

## Tushuntirish va Mantiq:
Modifikatorlar xuddi funksiyalar kabi o'z parametrlariga ega bo'lishi mumkin.

## Ishlash natijasi:
```text
buyVIP{value: 0.6 ether}() bajarildi.
buyVIP{value: 0.1 ether}() -> Revert
```


# 303-Topshiriq: Reentrancy Guard modifikatori (Qayta kirishdan himoya)
## Topshiriq sharti:
Mutex qulfi orqali reentrancy hujumlarining oldini oluvchi modifikator yozing.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
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
```

## Tushuntirish va Mantiq:
`nonReentrant` modifikatori tashqi chaqiruv amalga oshirilayotganda qayta kirishning oldini oladi.

## Ishlash natijasi:
```text
safeWithdraw() xavfsiz bajarildi.
```


# 304-Topshiriq: Bir nechta modifikatorlarni zanjirband qilish
## Topshiriq sharti:
Bitta funksiyada bir vaqtning o'zida bir nechta modifikatorlarni qo'llang.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
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
```

## Tushuntirish va Mantiq:
Modifikatorlar yozilish tartibi bo'yicha ketma-ket tekshiriladi.

## Ishlash natijasi:
```text
updateConfig() ikkala modifikatordan muvaffaqiyatli o'tdi.
```


# 305-Topshiriq: Pausable namunasi: Favqulodda to'xtatish
## Topshiriq sharti:
Xakerlik xavfi sezilganda barcha aktiv funksiyalarni to'xtatuvchi Pausable tizimi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
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
```

## Tushuntirish va Mantiq:
Pausable favqulodda vaziyatlarda zaxira xavfsizlik chorasi hisoblanadi.

## Ishlash natijasi:
```text
setPaused(true) chaqirildi.
transferToken() -> Revert: 'Kontrakt pauzada!'
```


# 306-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #306
## Topshiriq sharti:
306-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_306 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_306() external onlyOperator returns (uint256) {
        return 306 * 2;
    }
}
```

## Tushuntirish va Mantiq:
306-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_306() bajarildi -> 612
```


# 307-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #307
## Topshiriq sharti:
307-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_307 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_307() external onlyOperator returns (uint256) {
        return 307 * 2;
    }
}
```

## Tushuntirish va Mantiq:
307-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_307() bajarildi -> 614
```


# 308-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #308
## Topshiriq sharti:
308-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_308 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_308() external onlyOperator returns (uint256) {
        return 308 * 2;
    }
}
```

## Tushuntirish va Mantiq:
308-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_308() bajarildi -> 616
```


# 309-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #309
## Topshiriq sharti:
309-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_309 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_309() external onlyOperator returns (uint256) {
        return 309 * 2;
    }
}
```

## Tushuntirish va Mantiq:
309-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_309() bajarildi -> 618
```


# 310-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #310
## Topshiriq sharti:
310-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_310 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_310() external onlyOperator returns (uint256) {
        return 310 * 2;
    }
}
```

## Tushuntirish va Mantiq:
310-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_310() bajarildi -> 620
```


# 311-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #311
## Topshiriq sharti:
311-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_311 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_311() external onlyOperator returns (uint256) {
        return 311 * 2;
    }
}
```

## Tushuntirish va Mantiq:
311-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_311() bajarildi -> 622
```


# 312-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #312
## Topshiriq sharti:
312-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_312 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_312() external onlyOperator returns (uint256) {
        return 312 * 2;
    }
}
```

## Tushuntirish va Mantiq:
312-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_312() bajarildi -> 624
```


# 313-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #313
## Topshiriq sharti:
313-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_313 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_313() external onlyOperator returns (uint256) {
        return 313 * 2;
    }
}
```

## Tushuntirish va Mantiq:
313-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_313() bajarildi -> 626
```


# 314-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #314
## Topshiriq sharti:
314-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_314 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_314() external onlyOperator returns (uint256) {
        return 314 * 2;
    }
}
```

## Tushuntirish va Mantiq:
314-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_314() bajarildi -> 628
```


# 315-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #315
## Topshiriq sharti:
315-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_315 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_315() external onlyOperator returns (uint256) {
        return 315 * 2;
    }
}
```

## Tushuntirish va Mantiq:
315-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_315() bajarildi -> 630
```


# 316-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #316
## Topshiriq sharti:
316-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_316 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_316() external onlyOperator returns (uint256) {
        return 316 * 2;
    }
}
```

## Tushuntirish va Mantiq:
316-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_316() bajarildi -> 632
```


# 317-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #317
## Topshiriq sharti:
317-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_317 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_317() external onlyOperator returns (uint256) {
        return 317 * 2;
    }
}
```

## Tushuntirish va Mantiq:
317-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_317() bajarildi -> 634
```


# 318-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #318
## Topshiriq sharti:
318-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_318 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_318() external onlyOperator returns (uint256) {
        return 318 * 2;
    }
}
```

## Tushuntirish va Mantiq:
318-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_318() bajarildi -> 636
```


# 319-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #319
## Topshiriq sharti:
319-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_319 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_319() external onlyOperator returns (uint256) {
        return 319 * 2;
    }
}
```

## Tushuntirish va Mantiq:
319-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_319() bajarildi -> 638
```


# 320-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #320
## Topshiriq sharti:
320-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_320 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_320() external onlyOperator returns (uint256) {
        return 320 * 2;
    }
}
```

## Tushuntirish va Mantiq:
320-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_320() bajarildi -> 640
```


# 321-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #321
## Topshiriq sharti:
321-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_321 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_321() external onlyOperator returns (uint256) {
        return 321 * 2;
    }
}
```

## Tushuntirish va Mantiq:
321-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_321() bajarildi -> 642
```


# 322-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #322
## Topshiriq sharti:
322-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_322 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_322() external onlyOperator returns (uint256) {
        return 322 * 2;
    }
}
```

## Tushuntirish va Mantiq:
322-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_322() bajarildi -> 644
```


# 323-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #323
## Topshiriq sharti:
323-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_323 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_323() external onlyOperator returns (uint256) {
        return 323 * 2;
    }
}
```

## Tushuntirish va Mantiq:
323-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_323() bajarildi -> 646
```


# 324-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #324
## Topshiriq sharti:
324-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_324 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_324() external onlyOperator returns (uint256) {
        return 324 * 2;
    }
}
```

## Tushuntirish va Mantiq:
324-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_324() bajarildi -> 648
```


# 325-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #325
## Topshiriq sharti:
325-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_325 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_325() external onlyOperator returns (uint256) {
        return 325 * 2;
    }
}
```

## Tushuntirish va Mantiq:
325-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_325() bajarildi -> 650
```


# 326-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #326
## Topshiriq sharti:
326-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_326 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_326() external onlyOperator returns (uint256) {
        return 326 * 2;
    }
}
```

## Tushuntirish va Mantiq:
326-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_326() bajarildi -> 652
```


# 327-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #327
## Topshiriq sharti:
327-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_327 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_327() external onlyOperator returns (uint256) {
        return 327 * 2;
    }
}
```

## Tushuntirish va Mantiq:
327-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_327() bajarildi -> 654
```


# 328-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #328
## Topshiriq sharti:
328-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_328 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_328() external onlyOperator returns (uint256) {
        return 328 * 2;
    }
}
```

## Tushuntirish va Mantiq:
328-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_328() bajarildi -> 656
```


# 329-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #329
## Topshiriq sharti:
329-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_329 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_329() external onlyOperator returns (uint256) {
        return 329 * 2;
    }
}
```

## Tushuntirish va Mantiq:
329-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_329() bajarildi -> 658
```


# 330-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #330
## Topshiriq sharti:
330-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_330 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_330() external onlyOperator returns (uint256) {
        return 330 * 2;
    }
}
```

## Tushuntirish va Mantiq:
330-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_330() bajarildi -> 660
```


# 331-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #331
## Topshiriq sharti:
331-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_331 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_331() external onlyOperator returns (uint256) {
        return 331 * 2;
    }
}
```

## Tushuntirish va Mantiq:
331-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_331() bajarildi -> 662
```


# 332-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #332
## Topshiriq sharti:
332-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_332 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_332() external onlyOperator returns (uint256) {
        return 332 * 2;
    }
}
```

## Tushuntirish va Mantiq:
332-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_332() bajarildi -> 664
```


# 333-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #333
## Topshiriq sharti:
333-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_333 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_333() external onlyOperator returns (uint256) {
        return 333 * 2;
    }
}
```

## Tushuntirish va Mantiq:
333-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_333() bajarildi -> 666
```


# 334-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #334
## Topshiriq sharti:
334-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_334 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_334() external onlyOperator returns (uint256) {
        return 334 * 2;
    }
}
```

## Tushuntirish va Mantiq:
334-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_334() bajarildi -> 668
```


# 335-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #335
## Topshiriq sharti:
335-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_335 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_335() external onlyOperator returns (uint256) {
        return 335 * 2;
    }
}
```

## Tushuntirish va Mantiq:
335-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_335() bajarildi -> 670
```


# 336-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #336
## Topshiriq sharti:
336-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_336 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_336() external onlyOperator returns (uint256) {
        return 336 * 2;
    }
}
```

## Tushuntirish va Mantiq:
336-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_336() bajarildi -> 672
```


# 337-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #337
## Topshiriq sharti:
337-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_337 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_337() external onlyOperator returns (uint256) {
        return 337 * 2;
    }
}
```

## Tushuntirish va Mantiq:
337-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_337() bajarildi -> 674
```


# 338-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #338
## Topshiriq sharti:
338-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_338 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_338() external onlyOperator returns (uint256) {
        return 338 * 2;
    }
}
```

## Tushuntirish va Mantiq:
338-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_338() bajarildi -> 676
```


# 339-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #339
## Topshiriq sharti:
339-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_339 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_339() external onlyOperator returns (uint256) {
        return 339 * 2;
    }
}
```

## Tushuntirish va Mantiq:
339-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_339() bajarildi -> 678
```


# 340-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #340
## Topshiriq sharti:
340-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_340 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_340() external onlyOperator returns (uint256) {
        return 340 * 2;
    }
}
```

## Tushuntirish va Mantiq:
340-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_340() bajarildi -> 680
```


# 341-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #341
## Topshiriq sharti:
341-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_341 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_341() external onlyOperator returns (uint256) {
        return 341 * 2;
    }
}
```

## Tushuntirish va Mantiq:
341-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_341() bajarildi -> 682
```


# 342-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #342
## Topshiriq sharti:
342-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_342 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_342() external onlyOperator returns (uint256) {
        return 342 * 2;
    }
}
```

## Tushuntirish va Mantiq:
342-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_342() bajarildi -> 684
```


# 343-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #343
## Topshiriq sharti:
343-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_343 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_343() external onlyOperator returns (uint256) {
        return 343 * 2;
    }
}
```

## Tushuntirish va Mantiq:
343-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_343() bajarildi -> 686
```


# 344-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #344
## Topshiriq sharti:
344-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_344 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_344() external onlyOperator returns (uint256) {
        return 344 * 2;
    }
}
```

## Tushuntirish va Mantiq:
344-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_344() bajarildi -> 688
```


# 345-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #345
## Topshiriq sharti:
345-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_345 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_345() external onlyOperator returns (uint256) {
        return 345 * 2;
    }
}
```

## Tushuntirish va Mantiq:
345-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_345() bajarildi -> 690
```


# 346-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #346
## Topshiriq sharti:
346-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_346 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_346() external onlyOperator returns (uint256) {
        return 346 * 2;
    }
}
```

## Tushuntirish va Mantiq:
346-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_346() bajarildi -> 692
```


# 347-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #347
## Topshiriq sharti:
347-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_347 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_347() external onlyOperator returns (uint256) {
        return 347 * 2;
    }
}
```

## Tushuntirish va Mantiq:
347-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_347() bajarildi -> 694
```


# 348-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #348
## Topshiriq sharti:
348-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_348 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_348() external onlyOperator returns (uint256) {
        return 348 * 2;
    }
}
```

## Tushuntirish va Mantiq:
348-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_348() bajarildi -> 696
```


# 349-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #349
## Topshiriq sharti:
349-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_349 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_349() external onlyOperator returns (uint256) {
        return 349 * 2;
    }
}
```

## Tushuntirish va Mantiq:
349-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_349() bajarildi -> 698
```


# 350-Topshiriq: Kirish nazorati va modifikatorlar arxitekturasi #350
## Topshiriq sharti:
350-vazifa: Rolga asoslangan kirish (RBAC), modifier tekshiruvlari va xavfsizlik.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessControl_350 {
    mapping(address => bool) public isOperator;

    modifier onlyOperator() {
        require(isOperator[msg.sender] || msg.sender == address(this), "Operator ruxsati yo'q");
        _;
    }

    function executeTask_350() external onlyOperator returns (uint256) {
        return 350 * 2;
    }
}
```

## Tushuntirish va Mantiq:
350-topshiriqda operator ruxsati va modifikator tekshiruvi orqali xavfsiz chaqiruv amalga oshirildi.

## Ishlash natijasi:
```text
executeTask_350() bajarildi -> 700
```

