# 251-Topshiriq: Struct (Tuzilma) e'lon qilish va instansiya yaratish
## Topshiriq sharti:
Foydalanuvchi ma'lumotlarini struct ko'rinishida saqlash.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
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
```

## Tushuntirish va Mantiq:
Struct bir nechta har xil turlarni yagona mantiqiy guruhga birlashtirish imkonini beradi.

## Ishlash natijasi:
```text
createPlayer("Sardor", 15, true) chaqirildi.
topPlayer -> ("Sardor", 15, true)
```


# 252-Topshiriq: Enum (Sanash turi) va Holat Mashinasi (State Machine)
## Topshiriq sharti:
Buyurtma holatini (Pending, Shipped, Delivered, Cancelled) enum orqali boshqaring.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
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
```

## Tushuntirish va Mantiq:
Enum EVM ichida uint8 sifatida saqlanadi (0 dan boshlanadi) va kodni xatolardan himoyalaydi.

## Ishlash natijasi:
```text
currentStatus -> 0 (Pending)
shipOrder() bajarildi.
currentStatus -> 1 (Shipped)
```


# 253-Topshiriq: Structlarni mapping va massivlar bilan birga ishlatish
## Topshiriq sharti:
Har bir foydalanuvchi manziliga bog'langan profil strukturasini saqlang.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
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
```

## Tushuntirish va Mantiq:
Mapping ichida struct saqlash DApp foydalanuvchilari ma'lumotlarini markazlashtirilmagan tarzda boshqarishning eng keng tarqalgan usulidir.

## Ishlash natijasi:
```text
register("Bobur") bajarildi.
profiles(0xCaller...) -> ("Bobur", 100)
```


# 254-Topshiriq: Struct xotirasini qadoqlash (Storage Packing)
## Topshiriq sharti:
Struct maydonlarini bir xil 32-baytlik slotga sig'adigan qilib ketma-ket joylashtiring.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract PackedStructDemo {
    // 1 ta 32-bayt slotga sig'adi: 16 bayt + 16 bayt = 32 bayt
    struct CompactData {
        uint128 valueA;
        uint128 valueB;
    }

    CompactData public data = CompactData(100, 200);
}
```

## Tushuntirish va Mantiq:
uint128 + uint128 ketma-ket joylashsa, Solidity ularni bitta storage slotiga zichlaydi (pack) va yangi slot uchun 20,000 gas tejaydi.

## Ishlash natijasi:
```text
data.valueA -> 100
data.valueB -> 200
```


# 255-Topshiriq: Enumlarni parametr sifatida uzatish va solishtirish
## Topshiriq sharti:
Funksiyaga enum parametrini uzatib unga mos hisob-kitobni qaytaring.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EnumParamDemo {
    enum Tier { Standard, Silver, Gold }

    function getDiscount(Tier tier) external pure returns (uint256) {
        if (tier == Tier.Gold) return 20;
        if (tier == Tier.Silver) return 10;
        return 0;
    }
}
```

## Tushuntirish va Mantiq:
Enumlar funksiya parametrlari va qaytaruvchi turlar sifatida bemalol ishlatilishi mumkin.

## Ishlash natijasi:
```text
getDiscount(Tier.Gold) -> 20
```


# 256-Topshiriq: Strukturalar va sanash turlari arxitekturasi #256
## Topshiriq sharti:
256-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_256 {
    enum Status_256 { Init, Active, Closed }

    struct ItemRecord_256 {
        uint256 id;
        Status_256 status;
    }

    ItemRecord_256 public item = ItemRecord_256(256, Status_256.Init);

    function activate() external {
        item.status = Status_256.Active;
    }
}
```

## Tushuntirish va Mantiq:
256-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 257-Topshiriq: Strukturalar va sanash turlari arxitekturasi #257
## Topshiriq sharti:
257-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_257 {
    enum Status_257 { Init, Active, Closed }

    struct ItemRecord_257 {
        uint256 id;
        Status_257 status;
    }

    ItemRecord_257 public item = ItemRecord_257(257, Status_257.Init);

    function activate() external {
        item.status = Status_257.Active;
    }
}
```

## Tushuntirish va Mantiq:
257-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 258-Topshiriq: Strukturalar va sanash turlari arxitekturasi #258
## Topshiriq sharti:
258-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_258 {
    enum Status_258 { Init, Active, Closed }

    struct ItemRecord_258 {
        uint256 id;
        Status_258 status;
    }

    ItemRecord_258 public item = ItemRecord_258(258, Status_258.Init);

    function activate() external {
        item.status = Status_258.Active;
    }
}
```

## Tushuntirish va Mantiq:
258-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 259-Topshiriq: Strukturalar va sanash turlari arxitekturasi #259
## Topshiriq sharti:
259-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_259 {
    enum Status_259 { Init, Active, Closed }

    struct ItemRecord_259 {
        uint256 id;
        Status_259 status;
    }

    ItemRecord_259 public item = ItemRecord_259(259, Status_259.Init);

    function activate() external {
        item.status = Status_259.Active;
    }
}
```

## Tushuntirish va Mantiq:
259-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 260-Topshiriq: Strukturalar va sanash turlari arxitekturasi #260
## Topshiriq sharti:
260-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_260 {
    enum Status_260 { Init, Active, Closed }

    struct ItemRecord_260 {
        uint256 id;
        Status_260 status;
    }

    ItemRecord_260 public item = ItemRecord_260(260, Status_260.Init);

    function activate() external {
        item.status = Status_260.Active;
    }
}
```

## Tushuntirish va Mantiq:
260-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 261-Topshiriq: Strukturalar va sanash turlari arxitekturasi #261
## Topshiriq sharti:
261-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_261 {
    enum Status_261 { Init, Active, Closed }

    struct ItemRecord_261 {
        uint256 id;
        Status_261 status;
    }

    ItemRecord_261 public item = ItemRecord_261(261, Status_261.Init);

    function activate() external {
        item.status = Status_261.Active;
    }
}
```

## Tushuntirish va Mantiq:
261-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 262-Topshiriq: Strukturalar va sanash turlari arxitekturasi #262
## Topshiriq sharti:
262-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_262 {
    enum Status_262 { Init, Active, Closed }

    struct ItemRecord_262 {
        uint256 id;
        Status_262 status;
    }

    ItemRecord_262 public item = ItemRecord_262(262, Status_262.Init);

    function activate() external {
        item.status = Status_262.Active;
    }
}
```

## Tushuntirish va Mantiq:
262-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 263-Topshiriq: Strukturalar va sanash turlari arxitekturasi #263
## Topshiriq sharti:
263-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_263 {
    enum Status_263 { Init, Active, Closed }

    struct ItemRecord_263 {
        uint256 id;
        Status_263 status;
    }

    ItemRecord_263 public item = ItemRecord_263(263, Status_263.Init);

    function activate() external {
        item.status = Status_263.Active;
    }
}
```

## Tushuntirish va Mantiq:
263-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 264-Topshiriq: Strukturalar va sanash turlari arxitekturasi #264
## Topshiriq sharti:
264-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_264 {
    enum Status_264 { Init, Active, Closed }

    struct ItemRecord_264 {
        uint256 id;
        Status_264 status;
    }

    ItemRecord_264 public item = ItemRecord_264(264, Status_264.Init);

    function activate() external {
        item.status = Status_264.Active;
    }
}
```

## Tushuntirish va Mantiq:
264-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 265-Topshiriq: Strukturalar va sanash turlari arxitekturasi #265
## Topshiriq sharti:
265-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_265 {
    enum Status_265 { Init, Active, Closed }

    struct ItemRecord_265 {
        uint256 id;
        Status_265 status;
    }

    ItemRecord_265 public item = ItemRecord_265(265, Status_265.Init);

    function activate() external {
        item.status = Status_265.Active;
    }
}
```

## Tushuntirish va Mantiq:
265-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 266-Topshiriq: Strukturalar va sanash turlari arxitekturasi #266
## Topshiriq sharti:
266-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_266 {
    enum Status_266 { Init, Active, Closed }

    struct ItemRecord_266 {
        uint256 id;
        Status_266 status;
    }

    ItemRecord_266 public item = ItemRecord_266(266, Status_266.Init);

    function activate() external {
        item.status = Status_266.Active;
    }
}
```

## Tushuntirish va Mantiq:
266-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 267-Topshiriq: Strukturalar va sanash turlari arxitekturasi #267
## Topshiriq sharti:
267-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_267 {
    enum Status_267 { Init, Active, Closed }

    struct ItemRecord_267 {
        uint256 id;
        Status_267 status;
    }

    ItemRecord_267 public item = ItemRecord_267(267, Status_267.Init);

    function activate() external {
        item.status = Status_267.Active;
    }
}
```

## Tushuntirish va Mantiq:
267-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 268-Topshiriq: Strukturalar va sanash turlari arxitekturasi #268
## Topshiriq sharti:
268-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_268 {
    enum Status_268 { Init, Active, Closed }

    struct ItemRecord_268 {
        uint256 id;
        Status_268 status;
    }

    ItemRecord_268 public item = ItemRecord_268(268, Status_268.Init);

    function activate() external {
        item.status = Status_268.Active;
    }
}
```

## Tushuntirish va Mantiq:
268-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 269-Topshiriq: Strukturalar va sanash turlari arxitekturasi #269
## Topshiriq sharti:
269-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_269 {
    enum Status_269 { Init, Active, Closed }

    struct ItemRecord_269 {
        uint256 id;
        Status_269 status;
    }

    ItemRecord_269 public item = ItemRecord_269(269, Status_269.Init);

    function activate() external {
        item.status = Status_269.Active;
    }
}
```

## Tushuntirish va Mantiq:
269-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 270-Topshiriq: Strukturalar va sanash turlari arxitekturasi #270
## Topshiriq sharti:
270-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_270 {
    enum Status_270 { Init, Active, Closed }

    struct ItemRecord_270 {
        uint256 id;
        Status_270 status;
    }

    ItemRecord_270 public item = ItemRecord_270(270, Status_270.Init);

    function activate() external {
        item.status = Status_270.Active;
    }
}
```

## Tushuntirish va Mantiq:
270-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 271-Topshiriq: Strukturalar va sanash turlari arxitekturasi #271
## Topshiriq sharti:
271-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_271 {
    enum Status_271 { Init, Active, Closed }

    struct ItemRecord_271 {
        uint256 id;
        Status_271 status;
    }

    ItemRecord_271 public item = ItemRecord_271(271, Status_271.Init);

    function activate() external {
        item.status = Status_271.Active;
    }
}
```

## Tushuntirish va Mantiq:
271-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 272-Topshiriq: Strukturalar va sanash turlari arxitekturasi #272
## Topshiriq sharti:
272-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_272 {
    enum Status_272 { Init, Active, Closed }

    struct ItemRecord_272 {
        uint256 id;
        Status_272 status;
    }

    ItemRecord_272 public item = ItemRecord_272(272, Status_272.Init);

    function activate() external {
        item.status = Status_272.Active;
    }
}
```

## Tushuntirish va Mantiq:
272-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 273-Topshiriq: Strukturalar va sanash turlari arxitekturasi #273
## Topshiriq sharti:
273-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_273 {
    enum Status_273 { Init, Active, Closed }

    struct ItemRecord_273 {
        uint256 id;
        Status_273 status;
    }

    ItemRecord_273 public item = ItemRecord_273(273, Status_273.Init);

    function activate() external {
        item.status = Status_273.Active;
    }
}
```

## Tushuntirish va Mantiq:
273-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 274-Topshiriq: Strukturalar va sanash turlari arxitekturasi #274
## Topshiriq sharti:
274-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_274 {
    enum Status_274 { Init, Active, Closed }

    struct ItemRecord_274 {
        uint256 id;
        Status_274 status;
    }

    ItemRecord_274 public item = ItemRecord_274(274, Status_274.Init);

    function activate() external {
        item.status = Status_274.Active;
    }
}
```

## Tushuntirish va Mantiq:
274-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 275-Topshiriq: Strukturalar va sanash turlari arxitekturasi #275
## Topshiriq sharti:
275-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_275 {
    enum Status_275 { Init, Active, Closed }

    struct ItemRecord_275 {
        uint256 id;
        Status_275 status;
    }

    ItemRecord_275 public item = ItemRecord_275(275, Status_275.Init);

    function activate() external {
        item.status = Status_275.Active;
    }
}
```

## Tushuntirish va Mantiq:
275-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 276-Topshiriq: Strukturalar va sanash turlari arxitekturasi #276
## Topshiriq sharti:
276-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_276 {
    enum Status_276 { Init, Active, Closed }

    struct ItemRecord_276 {
        uint256 id;
        Status_276 status;
    }

    ItemRecord_276 public item = ItemRecord_276(276, Status_276.Init);

    function activate() external {
        item.status = Status_276.Active;
    }
}
```

## Tushuntirish va Mantiq:
276-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 277-Topshiriq: Strukturalar va sanash turlari arxitekturasi #277
## Topshiriq sharti:
277-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_277 {
    enum Status_277 { Init, Active, Closed }

    struct ItemRecord_277 {
        uint256 id;
        Status_277 status;
    }

    ItemRecord_277 public item = ItemRecord_277(277, Status_277.Init);

    function activate() external {
        item.status = Status_277.Active;
    }
}
```

## Tushuntirish va Mantiq:
277-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 278-Topshiriq: Strukturalar va sanash turlari arxitekturasi #278
## Topshiriq sharti:
278-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_278 {
    enum Status_278 { Init, Active, Closed }

    struct ItemRecord_278 {
        uint256 id;
        Status_278 status;
    }

    ItemRecord_278 public item = ItemRecord_278(278, Status_278.Init);

    function activate() external {
        item.status = Status_278.Active;
    }
}
```

## Tushuntirish va Mantiq:
278-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 279-Topshiriq: Strukturalar va sanash turlari arxitekturasi #279
## Topshiriq sharti:
279-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_279 {
    enum Status_279 { Init, Active, Closed }

    struct ItemRecord_279 {
        uint256 id;
        Status_279 status;
    }

    ItemRecord_279 public item = ItemRecord_279(279, Status_279.Init);

    function activate() external {
        item.status = Status_279.Active;
    }
}
```

## Tushuntirish va Mantiq:
279-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 280-Topshiriq: Strukturalar va sanash turlari arxitekturasi #280
## Topshiriq sharti:
280-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_280 {
    enum Status_280 { Init, Active, Closed }

    struct ItemRecord_280 {
        uint256 id;
        Status_280 status;
    }

    ItemRecord_280 public item = ItemRecord_280(280, Status_280.Init);

    function activate() external {
        item.status = Status_280.Active;
    }
}
```

## Tushuntirish va Mantiq:
280-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 281-Topshiriq: Strukturalar va sanash turlari arxitekturasi #281
## Topshiriq sharti:
281-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_281 {
    enum Status_281 { Init, Active, Closed }

    struct ItemRecord_281 {
        uint256 id;
        Status_281 status;
    }

    ItemRecord_281 public item = ItemRecord_281(281, Status_281.Init);

    function activate() external {
        item.status = Status_281.Active;
    }
}
```

## Tushuntirish va Mantiq:
281-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 282-Topshiriq: Strukturalar va sanash turlari arxitekturasi #282
## Topshiriq sharti:
282-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_282 {
    enum Status_282 { Init, Active, Closed }

    struct ItemRecord_282 {
        uint256 id;
        Status_282 status;
    }

    ItemRecord_282 public item = ItemRecord_282(282, Status_282.Init);

    function activate() external {
        item.status = Status_282.Active;
    }
}
```

## Tushuntirish va Mantiq:
282-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 283-Topshiriq: Strukturalar va sanash turlari arxitekturasi #283
## Topshiriq sharti:
283-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_283 {
    enum Status_283 { Init, Active, Closed }

    struct ItemRecord_283 {
        uint256 id;
        Status_283 status;
    }

    ItemRecord_283 public item = ItemRecord_283(283, Status_283.Init);

    function activate() external {
        item.status = Status_283.Active;
    }
}
```

## Tushuntirish va Mantiq:
283-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 284-Topshiriq: Strukturalar va sanash turlari arxitekturasi #284
## Topshiriq sharti:
284-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_284 {
    enum Status_284 { Init, Active, Closed }

    struct ItemRecord_284 {
        uint256 id;
        Status_284 status;
    }

    ItemRecord_284 public item = ItemRecord_284(284, Status_284.Init);

    function activate() external {
        item.status = Status_284.Active;
    }
}
```

## Tushuntirish va Mantiq:
284-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 285-Topshiriq: Strukturalar va sanash turlari arxitekturasi #285
## Topshiriq sharti:
285-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_285 {
    enum Status_285 { Init, Active, Closed }

    struct ItemRecord_285 {
        uint256 id;
        Status_285 status;
    }

    ItemRecord_285 public item = ItemRecord_285(285, Status_285.Init);

    function activate() external {
        item.status = Status_285.Active;
    }
}
```

## Tushuntirish va Mantiq:
285-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 286-Topshiriq: Strukturalar va sanash turlari arxitekturasi #286
## Topshiriq sharti:
286-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_286 {
    enum Status_286 { Init, Active, Closed }

    struct ItemRecord_286 {
        uint256 id;
        Status_286 status;
    }

    ItemRecord_286 public item = ItemRecord_286(286, Status_286.Init);

    function activate() external {
        item.status = Status_286.Active;
    }
}
```

## Tushuntirish va Mantiq:
286-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 287-Topshiriq: Strukturalar va sanash turlari arxitekturasi #287
## Topshiriq sharti:
287-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_287 {
    enum Status_287 { Init, Active, Closed }

    struct ItemRecord_287 {
        uint256 id;
        Status_287 status;
    }

    ItemRecord_287 public item = ItemRecord_287(287, Status_287.Init);

    function activate() external {
        item.status = Status_287.Active;
    }
}
```

## Tushuntirish va Mantiq:
287-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 288-Topshiriq: Strukturalar va sanash turlari arxitekturasi #288
## Topshiriq sharti:
288-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_288 {
    enum Status_288 { Init, Active, Closed }

    struct ItemRecord_288 {
        uint256 id;
        Status_288 status;
    }

    ItemRecord_288 public item = ItemRecord_288(288, Status_288.Init);

    function activate() external {
        item.status = Status_288.Active;
    }
}
```

## Tushuntirish va Mantiq:
288-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 289-Topshiriq: Strukturalar va sanash turlari arxitekturasi #289
## Topshiriq sharti:
289-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_289 {
    enum Status_289 { Init, Active, Closed }

    struct ItemRecord_289 {
        uint256 id;
        Status_289 status;
    }

    ItemRecord_289 public item = ItemRecord_289(289, Status_289.Init);

    function activate() external {
        item.status = Status_289.Active;
    }
}
```

## Tushuntirish va Mantiq:
289-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 290-Topshiriq: Strukturalar va sanash turlari arxitekturasi #290
## Topshiriq sharti:
290-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_290 {
    enum Status_290 { Init, Active, Closed }

    struct ItemRecord_290 {
        uint256 id;
        Status_290 status;
    }

    ItemRecord_290 public item = ItemRecord_290(290, Status_290.Init);

    function activate() external {
        item.status = Status_290.Active;
    }
}
```

## Tushuntirish va Mantiq:
290-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 291-Topshiriq: Strukturalar va sanash turlari arxitekturasi #291
## Topshiriq sharti:
291-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_291 {
    enum Status_291 { Init, Active, Closed }

    struct ItemRecord_291 {
        uint256 id;
        Status_291 status;
    }

    ItemRecord_291 public item = ItemRecord_291(291, Status_291.Init);

    function activate() external {
        item.status = Status_291.Active;
    }
}
```

## Tushuntirish va Mantiq:
291-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 292-Topshiriq: Strukturalar va sanash turlari arxitekturasi #292
## Topshiriq sharti:
292-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_292 {
    enum Status_292 { Init, Active, Closed }

    struct ItemRecord_292 {
        uint256 id;
        Status_292 status;
    }

    ItemRecord_292 public item = ItemRecord_292(292, Status_292.Init);

    function activate() external {
        item.status = Status_292.Active;
    }
}
```

## Tushuntirish va Mantiq:
292-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 293-Topshiriq: Strukturalar va sanash turlari arxitekturasi #293
## Topshiriq sharti:
293-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_293 {
    enum Status_293 { Init, Active, Closed }

    struct ItemRecord_293 {
        uint256 id;
        Status_293 status;
    }

    ItemRecord_293 public item = ItemRecord_293(293, Status_293.Init);

    function activate() external {
        item.status = Status_293.Active;
    }
}
```

## Tushuntirish va Mantiq:
293-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 294-Topshiriq: Strukturalar va sanash turlari arxitekturasi #294
## Topshiriq sharti:
294-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_294 {
    enum Status_294 { Init, Active, Closed }

    struct ItemRecord_294 {
        uint256 id;
        Status_294 status;
    }

    ItemRecord_294 public item = ItemRecord_294(294, Status_294.Init);

    function activate() external {
        item.status = Status_294.Active;
    }
}
```

## Tushuntirish va Mantiq:
294-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 295-Topshiriq: Strukturalar va sanash turlari arxitekturasi #295
## Topshiriq sharti:
295-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_295 {
    enum Status_295 { Init, Active, Closed }

    struct ItemRecord_295 {
        uint256 id;
        Status_295 status;
    }

    ItemRecord_295 public item = ItemRecord_295(295, Status_295.Init);

    function activate() external {
        item.status = Status_295.Active;
    }
}
```

## Tushuntirish va Mantiq:
295-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 296-Topshiriq: Strukturalar va sanash turlari arxitekturasi #296
## Topshiriq sharti:
296-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_296 {
    enum Status_296 { Init, Active, Closed }

    struct ItemRecord_296 {
        uint256 id;
        Status_296 status;
    }

    ItemRecord_296 public item = ItemRecord_296(296, Status_296.Init);

    function activate() external {
        item.status = Status_296.Active;
    }
}
```

## Tushuntirish va Mantiq:
296-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 297-Topshiriq: Strukturalar va sanash turlari arxitekturasi #297
## Topshiriq sharti:
297-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_297 {
    enum Status_297 { Init, Active, Closed }

    struct ItemRecord_297 {
        uint256 id;
        Status_297 status;
    }

    ItemRecord_297 public item = ItemRecord_297(297, Status_297.Init);

    function activate() external {
        item.status = Status_297.Active;
    }
}
```

## Tushuntirish va Mantiq:
297-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 298-Topshiriq: Strukturalar va sanash turlari arxitekturasi #298
## Topshiriq sharti:
298-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_298 {
    enum Status_298 { Init, Active, Closed }

    struct ItemRecord_298 {
        uint256 id;
        Status_298 status;
    }

    ItemRecord_298 public item = ItemRecord_298(298, Status_298.Init);

    function activate() external {
        item.status = Status_298.Active;
    }
}
```

## Tushuntirish va Mantiq:
298-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 299-Topshiriq: Strukturalar va sanash turlari arxitekturasi #299
## Topshiriq sharti:
299-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_299 {
    enum Status_299 { Init, Active, Closed }

    struct ItemRecord_299 {
        uint256 id;
        Status_299 status;
    }

    ItemRecord_299 public item = ItemRecord_299(299, Status_299.Init);

    function activate() external {
        item.status = Status_299.Active;
    }
}
```

## Tushuntirish va Mantiq:
299-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```


# 300-Topshiriq: Strukturalar va sanash turlari arxitekturasi #300
## Topshiriq sharti:
300-vazifa: Struct packing, holat o'zgarishlari va murakkab ma'lumot modellari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StateModel_300 {
    enum Status_300 { Init, Active, Closed }

    struct ItemRecord_300 {
        uint256 id;
        Status_300 status;
    }

    ItemRecord_300 public item = ItemRecord_300(300, Status_300.Init);

    function activate() external {
        item.status = Status_300.Active;
    }
}
```

## Tushuntirish va Mantiq:
300-topshiriqda enum va struct birgalikda ishlatilib xavfsiz holat mashinasi shakllantirildi.

## Ishlash natijasi:
```text
item.status -> 0 (Init)
activate() chaqirildi.
item.status -> 1 (Active)
```

