# 351-Topshiriq: event e'lon qilish va emit operatori
## Topshiriq sharti:
Token o'tkazilganda blokcheyn loglariga yoziluvchi Transfer hodisasini yarating.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventDemo {
    event FundsTransferred(address from, address to, uint256 amount);

    function sendMoney(address recipient, uint256 amt) external {
        emit FundsTransferred(msg.sender, recipient, amt);
    }
}
```

## Tushuntirish va Mantiq:
`event` blokcheyn tranzaksiya kvitansiyasiga (transaction receipt) log yozadi. Tashqi Web3 frontend ilovalar ushbu hodisalarni tinglab turadi.

## Ishlash natijasi:
```text
sendMoney(0xRecipient..., 500) chaqirildi.
Hodisa emit qilindi: FundsTransferred(0xSender..., 0xRecipient..., 500)
```


# 352-Topshiriq: indexed parametrlari (Topics) va filtrlash
## Topshiriq sharti:
Frontend yoki The Graph da manzil bo'yicha tezkor filtrlash imkonini beruvchi 'indexed' parametrlarini qo'llang.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract IndexedEventDemo {
    // Bitta eventda maksimal 3 ta parametr 'indexed' bo'lishi mumkin!
    event UserRegistered(address indexed userAddress, uint256 indexed userId, string userName);

    function register(uint256 id, string calldata name) external {
        emit UserRegistered(msg.sender, id, name);
    }
}
```

## Tushuntirish va Mantiq:
`indexed` parametrlari EVM-da 'topic' sifatida saqlanadi va off-chain tizimlariga ma'lum bir manzilga tegishli barcha tranzaksiyalarni bir zumda topishga yordam beradi.

## Ishlash natijasi:
```text
register(101, "Dilshod") bajarildi.
Topic[1]: 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
Topic[2]: 101
```


# 353-Topshiriq: Eventlar yordamida Gas tejash
## Topshiriq sharti:
O'zgarmas ma'lumotlar tarixini storage-da emas, event loglarida saqlash orqali gasni tejang.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CheapLoggingDemo {
    event DocumentUploaded(bytes32 indexed docHash, uint256 timestamp);

    function uploadDoc(bytes32 docHash) external {
        emit DocumentUploaded(docHash, block.timestamp);
    }
}
```

## Tushuntirish va Mantiq:
Storage-ga bitta slot yozish 20,000 gas talab qiladi, hodisa chiqarish (LOG opkodi) esa bor-yo'g'i ~1000-2000 gas sarflaydi.

## Ishlash natijasi:
```text
uploadDoc(0xABC...) muvaffaqiyatli bajarildi (kam gas sarfi).
```


# 354-Topshiriq: Anonim hodisalar (anonymous events)
## Topshiriq sharti:
Event imzosining xeshini (Topic 0) saqlamasdan 4 tagacha indexed parametr qo'llash.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AnonymousEventDemo {
    event DetailedLog(address indexed a, address indexed b, uint256 indexed c, uint256 indexed d) anonymous;

    function trigger() external {
        emit DetailedLog(msg.sender, address(this), 1, 2);
    }
}
```

## Tushuntirish va Mantiq:
`anonymous` eventlar Topic 0 (event selector) ni saqlamaydi, natijada 4 ta indexed parametrga ruxsat beradi va qo'shimcha gas tejaydi.

## Ishlash natijasi:
```text
DetailedLog hodisasi anonim ravishda emit qilindi.
```


# 355-Topshiriq: Muhim parametrlar o'zgarishini kuzatish
## Topshiriq sharti:
Admin o'zgarganda xavfsizlik auditi uchun maxsus hodisani e'lon qiling.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
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
```

## Tushuntirish va Mantiq:
Blokcheyn auditorlari muhim parametrlar o'zgarishini doimo eventlar orqali tekshiradilar.

## Ishlash natijasi:
```text
transferAdmin(0xNewAdmin...) bajarildi.
AdminChanged emit qilindi.
```


# 356-Topshiriq: Hodisalar (Events) va EVM jurnallari #356
## Topshiriq sharti:
356-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_356 {
    event ProcessCompleted_356(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_356(msg.sender, 356);
    }
}
```

## Tushuntirish va Mantiq:
356-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_356 emit qilindi.
```


# 357-Topshiriq: Hodisalar (Events) va EVM jurnallari #357
## Topshiriq sharti:
357-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_357 {
    event ProcessCompleted_357(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_357(msg.sender, 357);
    }
}
```

## Tushuntirish va Mantiq:
357-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_357 emit qilindi.
```


# 358-Topshiriq: Hodisalar (Events) va EVM jurnallari #358
## Topshiriq sharti:
358-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_358 {
    event ProcessCompleted_358(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_358(msg.sender, 358);
    }
}
```

## Tushuntirish va Mantiq:
358-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_358 emit qilindi.
```


# 359-Topshiriq: Hodisalar (Events) va EVM jurnallari #359
## Topshiriq sharti:
359-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_359 {
    event ProcessCompleted_359(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_359(msg.sender, 359);
    }
}
```

## Tushuntirish va Mantiq:
359-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_359 emit qilindi.
```


# 360-Topshiriq: Hodisalar (Events) va EVM jurnallari #360
## Topshiriq sharti:
360-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_360 {
    event ProcessCompleted_360(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_360(msg.sender, 360);
    }
}
```

## Tushuntirish va Mantiq:
360-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_360 emit qilindi.
```


# 361-Topshiriq: Hodisalar (Events) va EVM jurnallari #361
## Topshiriq sharti:
361-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_361 {
    event ProcessCompleted_361(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_361(msg.sender, 361);
    }
}
```

## Tushuntirish va Mantiq:
361-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_361 emit qilindi.
```


# 362-Topshiriq: Hodisalar (Events) va EVM jurnallari #362
## Topshiriq sharti:
362-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_362 {
    event ProcessCompleted_362(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_362(msg.sender, 362);
    }
}
```

## Tushuntirish va Mantiq:
362-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_362 emit qilindi.
```


# 363-Topshiriq: Hodisalar (Events) va EVM jurnallari #363
## Topshiriq sharti:
363-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_363 {
    event ProcessCompleted_363(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_363(msg.sender, 363);
    }
}
```

## Tushuntirish va Mantiq:
363-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_363 emit qilindi.
```


# 364-Topshiriq: Hodisalar (Events) va EVM jurnallari #364
## Topshiriq sharti:
364-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_364 {
    event ProcessCompleted_364(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_364(msg.sender, 364);
    }
}
```

## Tushuntirish va Mantiq:
364-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_364 emit qilindi.
```


# 365-Topshiriq: Hodisalar (Events) va EVM jurnallari #365
## Topshiriq sharti:
365-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_365 {
    event ProcessCompleted_365(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_365(msg.sender, 365);
    }
}
```

## Tushuntirish va Mantiq:
365-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_365 emit qilindi.
```


# 366-Topshiriq: Hodisalar (Events) va EVM jurnallari #366
## Topshiriq sharti:
366-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_366 {
    event ProcessCompleted_366(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_366(msg.sender, 366);
    }
}
```

## Tushuntirish va Mantiq:
366-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_366 emit qilindi.
```


# 367-Topshiriq: Hodisalar (Events) va EVM jurnallari #367
## Topshiriq sharti:
367-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_367 {
    event ProcessCompleted_367(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_367(msg.sender, 367);
    }
}
```

## Tushuntirish va Mantiq:
367-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_367 emit qilindi.
```


# 368-Topshiriq: Hodisalar (Events) va EVM jurnallari #368
## Topshiriq sharti:
368-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_368 {
    event ProcessCompleted_368(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_368(msg.sender, 368);
    }
}
```

## Tushuntirish va Mantiq:
368-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_368 emit qilindi.
```


# 369-Topshiriq: Hodisalar (Events) va EVM jurnallari #369
## Topshiriq sharti:
369-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_369 {
    event ProcessCompleted_369(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_369(msg.sender, 369);
    }
}
```

## Tushuntirish va Mantiq:
369-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_369 emit qilindi.
```


# 370-Topshiriq: Hodisalar (Events) va EVM jurnallari #370
## Topshiriq sharti:
370-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_370 {
    event ProcessCompleted_370(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_370(msg.sender, 370);
    }
}
```

## Tushuntirish va Mantiq:
370-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_370 emit qilindi.
```


# 371-Topshiriq: Hodisalar (Events) va EVM jurnallari #371
## Topshiriq sharti:
371-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_371 {
    event ProcessCompleted_371(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_371(msg.sender, 371);
    }
}
```

## Tushuntirish va Mantiq:
371-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_371 emit qilindi.
```


# 372-Topshiriq: Hodisalar (Events) va EVM jurnallari #372
## Topshiriq sharti:
372-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_372 {
    event ProcessCompleted_372(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_372(msg.sender, 372);
    }
}
```

## Tushuntirish va Mantiq:
372-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_372 emit qilindi.
```


# 373-Topshiriq: Hodisalar (Events) va EVM jurnallari #373
## Topshiriq sharti:
373-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_373 {
    event ProcessCompleted_373(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_373(msg.sender, 373);
    }
}
```

## Tushuntirish va Mantiq:
373-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_373 emit qilindi.
```


# 374-Topshiriq: Hodisalar (Events) va EVM jurnallari #374
## Topshiriq sharti:
374-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_374 {
    event ProcessCompleted_374(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_374(msg.sender, 374);
    }
}
```

## Tushuntirish va Mantiq:
374-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_374 emit qilindi.
```


# 375-Topshiriq: Hodisalar (Events) va EVM jurnallari #375
## Topshiriq sharti:
375-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_375 {
    event ProcessCompleted_375(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_375(msg.sender, 375);
    }
}
```

## Tushuntirish va Mantiq:
375-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_375 emit qilindi.
```


# 376-Topshiriq: Hodisalar (Events) va EVM jurnallari #376
## Topshiriq sharti:
376-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_376 {
    event ProcessCompleted_376(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_376(msg.sender, 376);
    }
}
```

## Tushuntirish va Mantiq:
376-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_376 emit qilindi.
```


# 377-Topshiriq: Hodisalar (Events) va EVM jurnallari #377
## Topshiriq sharti:
377-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_377 {
    event ProcessCompleted_377(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_377(msg.sender, 377);
    }
}
```

## Tushuntirish va Mantiq:
377-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_377 emit qilindi.
```


# 378-Topshiriq: Hodisalar (Events) va EVM jurnallari #378
## Topshiriq sharti:
378-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_378 {
    event ProcessCompleted_378(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_378(msg.sender, 378);
    }
}
```

## Tushuntirish va Mantiq:
378-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_378 emit qilindi.
```


# 379-Topshiriq: Hodisalar (Events) va EVM jurnallari #379
## Topshiriq sharti:
379-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_379 {
    event ProcessCompleted_379(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_379(msg.sender, 379);
    }
}
```

## Tushuntirish va Mantiq:
379-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_379 emit qilindi.
```


# 380-Topshiriq: Hodisalar (Events) va EVM jurnallari #380
## Topshiriq sharti:
380-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_380 {
    event ProcessCompleted_380(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_380(msg.sender, 380);
    }
}
```

## Tushuntirish va Mantiq:
380-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_380 emit qilindi.
```


# 381-Topshiriq: Hodisalar (Events) va EVM jurnallari #381
## Topshiriq sharti:
381-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_381 {
    event ProcessCompleted_381(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_381(msg.sender, 381);
    }
}
```

## Tushuntirish va Mantiq:
381-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_381 emit qilindi.
```


# 382-Topshiriq: Hodisalar (Events) va EVM jurnallari #382
## Topshiriq sharti:
382-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_382 {
    event ProcessCompleted_382(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_382(msg.sender, 382);
    }
}
```

## Tushuntirish va Mantiq:
382-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_382 emit qilindi.
```


# 383-Topshiriq: Hodisalar (Events) va EVM jurnallari #383
## Topshiriq sharti:
383-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_383 {
    event ProcessCompleted_383(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_383(msg.sender, 383);
    }
}
```

## Tushuntirish va Mantiq:
383-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_383 emit qilindi.
```


# 384-Topshiriq: Hodisalar (Events) va EVM jurnallari #384
## Topshiriq sharti:
384-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_384 {
    event ProcessCompleted_384(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_384(msg.sender, 384);
    }
}
```

## Tushuntirish va Mantiq:
384-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_384 emit qilindi.
```


# 385-Topshiriq: Hodisalar (Events) va EVM jurnallari #385
## Topshiriq sharti:
385-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_385 {
    event ProcessCompleted_385(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_385(msg.sender, 385);
    }
}
```

## Tushuntirish va Mantiq:
385-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_385 emit qilindi.
```


# 386-Topshiriq: Hodisalar (Events) va EVM jurnallari #386
## Topshiriq sharti:
386-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_386 {
    event ProcessCompleted_386(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_386(msg.sender, 386);
    }
}
```

## Tushuntirish va Mantiq:
386-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_386 emit qilindi.
```


# 387-Topshiriq: Hodisalar (Events) va EVM jurnallari #387
## Topshiriq sharti:
387-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_387 {
    event ProcessCompleted_387(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_387(msg.sender, 387);
    }
}
```

## Tushuntirish va Mantiq:
387-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_387 emit qilindi.
```


# 388-Topshiriq: Hodisalar (Events) va EVM jurnallari #388
## Topshiriq sharti:
388-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_388 {
    event ProcessCompleted_388(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_388(msg.sender, 388);
    }
}
```

## Tushuntirish va Mantiq:
388-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_388 emit qilindi.
```


# 389-Topshiriq: Hodisalar (Events) va EVM jurnallari #389
## Topshiriq sharti:
389-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_389 {
    event ProcessCompleted_389(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_389(msg.sender, 389);
    }
}
```

## Tushuntirish va Mantiq:
389-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_389 emit qilindi.
```


# 390-Topshiriq: Hodisalar (Events) va EVM jurnallari #390
## Topshiriq sharti:
390-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_390 {
    event ProcessCompleted_390(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_390(msg.sender, 390);
    }
}
```

## Tushuntirish va Mantiq:
390-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_390 emit qilindi.
```


# 391-Topshiriq: Hodisalar (Events) va EVM jurnallari #391
## Topshiriq sharti:
391-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_391 {
    event ProcessCompleted_391(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_391(msg.sender, 391);
    }
}
```

## Tushuntirish va Mantiq:
391-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_391 emit qilindi.
```


# 392-Topshiriq: Hodisalar (Events) va EVM jurnallari #392
## Topshiriq sharti:
392-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_392 {
    event ProcessCompleted_392(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_392(msg.sender, 392);
    }
}
```

## Tushuntirish va Mantiq:
392-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_392 emit qilindi.
```


# 393-Topshiriq: Hodisalar (Events) va EVM jurnallari #393
## Topshiriq sharti:
393-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_393 {
    event ProcessCompleted_393(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_393(msg.sender, 393);
    }
}
```

## Tushuntirish va Mantiq:
393-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_393 emit qilindi.
```


# 394-Topshiriq: Hodisalar (Events) va EVM jurnallari #394
## Topshiriq sharti:
394-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_394 {
    event ProcessCompleted_394(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_394(msg.sender, 394);
    }
}
```

## Tushuntirish va Mantiq:
394-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_394 emit qilindi.
```


# 395-Topshiriq: Hodisalar (Events) va EVM jurnallari #395
## Topshiriq sharti:
395-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_395 {
    event ProcessCompleted_395(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_395(msg.sender, 395);
    }
}
```

## Tushuntirish va Mantiq:
395-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_395 emit qilindi.
```


# 396-Topshiriq: Hodisalar (Events) va EVM jurnallari #396
## Topshiriq sharti:
396-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_396 {
    event ProcessCompleted_396(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_396(msg.sender, 396);
    }
}
```

## Tushuntirish va Mantiq:
396-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_396 emit qilindi.
```


# 397-Topshiriq: Hodisalar (Events) va EVM jurnallari #397
## Topshiriq sharti:
397-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_397 {
    event ProcessCompleted_397(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_397(msg.sender, 397);
    }
}
```

## Tushuntirish va Mantiq:
397-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_397 emit qilindi.
```


# 398-Topshiriq: Hodisalar (Events) va EVM jurnallari #398
## Topshiriq sharti:
398-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_398 {
    event ProcessCompleted_398(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_398(msg.sender, 398);
    }
}
```

## Tushuntirish va Mantiq:
398-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_398 emit qilindi.
```


# 399-Topshiriq: Hodisalar (Events) va EVM jurnallari #399
## Topshiriq sharti:
399-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_399 {
    event ProcessCompleted_399(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_399(msg.sender, 399);
    }
}
```

## Tushuntirish va Mantiq:
399-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_399 emit qilindi.
```


# 400-Topshiriq: Hodisalar (Events) va EVM jurnallari #400
## Topshiriq sharti:
400-vazifa: Indexed filtrlar, kvitansiya loglari va off-chain integratsiya.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EventLogger_400 {
    event ProcessCompleted_400(address indexed operator, uint256 code);

    function completeTask() external {
        emit ProcessCompleted_400(msg.sender, 400);
    }
}
```

## Tushuntirish va Mantiq:
400-topshiriqda off-chain kuzatuv uchun indexed log hodisasi loyihalandi.

## Ishlash natijasi:
```text
completeTask() bajarildi -> Event ProcessCompleted_400 emit qilindi.
```

