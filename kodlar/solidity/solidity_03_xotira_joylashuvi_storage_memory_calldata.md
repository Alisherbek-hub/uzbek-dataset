# 101-Topshiriq: EVM Xotira joylashuvi: Storage vs Memory ko'rsatkichlari
## Topshiriq sharti:
Storage ko'rsatkichi orqali holat o'zgaruvchisini to'g'ridan-to'g'ri o'zgartirish va memory orqali vaqtinchalik nusxa olish.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
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
```

## Tushuntirish va Mantiq:
'storage' o'zgaruvchilariga havola yaratilganda ko'rsatkich hosil bo'ladi va o'zgarishlar doimiy saqlanadi. 'memory' esa vaqtinchalik nusxa oladi.

## Ishlash natijasi:
```text
admin.name -> "Ali"
updateStorage("Vali") chaqirildi.
admin.name -> "Vali"
testMemoryCopy("Sami") -> "Sami"
admin.name -> "Vali" (o'zgarmasdan qoldi)
```


# 102-Topshiriq: calldata xotirasi va Gas tejash
## Topshiriq sharti:
O'zgarmas tashqi argumentlar uchun calldata ishlatish orqali xotiraga nusxalash xarajatlarini tejash.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CalldataDemo {
    function sumNumbers(uint256[] calldata numbers) external pure returns (uint256 total) {
        for (uint256 i = 0; i < numbers.length; i++) {
            total += numbers[i];
        }
    }
}
```

## Tushuntirish va Mantiq:
'calldata' tashqi tranzaksiyadan kelgan o'zgarmas baytlardir. Uni 'memory' ga ko'chirish shart bo'lmagani sababli juda ko'p gas tejaladi.

## Ishlash natijasi:
```text
sumNumbers([10, 20, 30, 40]) -> 100
```


# 103-Topshiriq: Xotirada dinamik massiv yaratish: new uint256[](size)
## Topshiriq sharti:
Memory qatlamida o'lchami qat'iy dinamik massiv yaratish.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
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
```

## Tushuntirish va Mantiq:
Memory massivlari `.push()` metodiga ega emas, ularning hajmi `new type[](size)` orqali avvaldan aniq belgilanishi shart.

## Ishlash natijasi:
```text
generateEvenNumbers(3) -> [2, 4, 6]
```


# 104-Topshiriq: Storage slotlari va 32-baytlik so'zlar
## Topshiriq sharti:
Holat o'zgaruvchilarining 32-baytlik storage slotlarida ketma-ket joylashuvi tahlili.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StorageLayoutDemo {
    uint256 public slot0 = 100; // Slot 0 da (32 bayt)
    uint256 public slot1 = 200; // Slot 1 da (32 bayt)

    function getSlotValues() external view returns (uint256, uint256) {
        return (slot0, slot1);
    }
}
```

## Tushuntirish va Mantiq:
EVM storage-ni $2^{256}$ ta har biri 32 baytdan iborat slotlar xaritasi sifatida boshqaradi.

## Ishlash natijasi:
```text
getSlotValues() -> (100, 200)
```


# 105-Topshiriq: Storage to Memory nusxalashdagi gas xarajatlari
## Topshiriq sharti:
Katta massivlarni storage-dan memory-ga o'qishda ehtiyotkorlik choralari.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract GasComparisonDemo {
    uint256[] public storedNumbers = [1, 2, 3, 4, 5];

    function readFromStorageDirectly() external view returns (uint256) {
        return storedNumbers[0];
    }
}
```

## Tushuntirish va Mantiq:
Katta massivlarni butunlay memory-ga yuklash kvadratik xotira kengayishiga (memory expansion cost) olib kelishi mumkin.

## Ishlash natijasi:
```text
readFromStorageDirectly() -> 1
```


# 106-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #106
## Topshiriq sharti:
106-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_106 {
    uint256 public dataPoint = 106;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 2 : 106;
    }
}
```

## Tushuntirish va Mantiq:
106-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 20
```


# 107-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #107
## Topshiriq sharti:
107-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_107 {
    uint256 public dataPoint = 107;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 3 : 107;
    }
}
```

## Tushuntirish va Mantiq:
107-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 30
```


# 108-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #108
## Topshiriq sharti:
108-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_108 {
    uint256 public dataPoint = 108;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 4 : 108;
    }
}
```

## Tushuntirish va Mantiq:
108-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 40
```


# 109-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #109
## Topshiriq sharti:
109-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_109 {
    uint256 public dataPoint = 109;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 5 : 109;
    }
}
```

## Tushuntirish va Mantiq:
109-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 50
```


# 110-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #110
## Topshiriq sharti:
110-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_110 {
    uint256 public dataPoint = 110;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 1 : 110;
    }
}
```

## Tushuntirish va Mantiq:
110-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 10
```


# 111-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #111
## Topshiriq sharti:
111-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_111 {
    uint256 public dataPoint = 111;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 2 : 111;
    }
}
```

## Tushuntirish va Mantiq:
111-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 20
```


# 112-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #112
## Topshiriq sharti:
112-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_112 {
    uint256 public dataPoint = 112;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 3 : 112;
    }
}
```

## Tushuntirish va Mantiq:
112-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 30
```


# 113-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #113
## Topshiriq sharti:
113-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_113 {
    uint256 public dataPoint = 113;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 4 : 113;
    }
}
```

## Tushuntirish va Mantiq:
113-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 40
```


# 114-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #114
## Topshiriq sharti:
114-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_114 {
    uint256 public dataPoint = 114;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 5 : 114;
    }
}
```

## Tushuntirish va Mantiq:
114-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 50
```


# 115-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #115
## Topshiriq sharti:
115-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_115 {
    uint256 public dataPoint = 115;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 1 : 115;
    }
}
```

## Tushuntirish va Mantiq:
115-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 10
```


# 116-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #116
## Topshiriq sharti:
116-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_116 {
    uint256 public dataPoint = 116;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 2 : 116;
    }
}
```

## Tushuntirish va Mantiq:
116-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 20
```


# 117-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #117
## Topshiriq sharti:
117-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_117 {
    uint256 public dataPoint = 117;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 3 : 117;
    }
}
```

## Tushuntirish va Mantiq:
117-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 30
```


# 118-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #118
## Topshiriq sharti:
118-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_118 {
    uint256 public dataPoint = 118;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 4 : 118;
    }
}
```

## Tushuntirish va Mantiq:
118-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 40
```


# 119-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #119
## Topshiriq sharti:
119-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_119 {
    uint256 public dataPoint = 119;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 5 : 119;
    }
}
```

## Tushuntirish va Mantiq:
119-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 50
```


# 120-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #120
## Topshiriq sharti:
120-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_120 {
    uint256 public dataPoint = 120;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 1 : 120;
    }
}
```

## Tushuntirish va Mantiq:
120-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 10
```


# 121-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #121
## Topshiriq sharti:
121-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_121 {
    uint256 public dataPoint = 121;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 2 : 121;
    }
}
```

## Tushuntirish va Mantiq:
121-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 20
```


# 122-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #122
## Topshiriq sharti:
122-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_122 {
    uint256 public dataPoint = 122;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 3 : 122;
    }
}
```

## Tushuntirish va Mantiq:
122-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 30
```


# 123-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #123
## Topshiriq sharti:
123-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_123 {
    uint256 public dataPoint = 123;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 4 : 123;
    }
}
```

## Tushuntirish va Mantiq:
123-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 40
```


# 124-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #124
## Topshiriq sharti:
124-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_124 {
    uint256 public dataPoint = 124;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 5 : 124;
    }
}
```

## Tushuntirish va Mantiq:
124-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 50
```


# 125-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #125
## Topshiriq sharti:
125-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_125 {
    uint256 public dataPoint = 125;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 1 : 125;
    }
}
```

## Tushuntirish va Mantiq:
125-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 10
```


# 126-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #126
## Topshiriq sharti:
126-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_126 {
    uint256 public dataPoint = 126;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 2 : 126;
    }
}
```

## Tushuntirish va Mantiq:
126-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 20
```


# 127-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #127
## Topshiriq sharti:
127-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_127 {
    uint256 public dataPoint = 127;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 3 : 127;
    }
}
```

## Tushuntirish va Mantiq:
127-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 30
```


# 128-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #128
## Topshiriq sharti:
128-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_128 {
    uint256 public dataPoint = 128;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 4 : 128;
    }
}
```

## Tushuntirish va Mantiq:
128-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 40
```


# 129-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #129
## Topshiriq sharti:
129-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_129 {
    uint256 public dataPoint = 129;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 5 : 129;
    }
}
```

## Tushuntirish va Mantiq:
129-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 50
```


# 130-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #130
## Topshiriq sharti:
130-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_130 {
    uint256 public dataPoint = 130;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 1 : 130;
    }
}
```

## Tushuntirish va Mantiq:
130-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 10
```


# 131-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #131
## Topshiriq sharti:
131-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_131 {
    uint256 public dataPoint = 131;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 2 : 131;
    }
}
```

## Tushuntirish va Mantiq:
131-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 20
```


# 132-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #132
## Topshiriq sharti:
132-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_132 {
    uint256 public dataPoint = 132;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 3 : 132;
    }
}
```

## Tushuntirish va Mantiq:
132-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 30
```


# 133-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #133
## Topshiriq sharti:
133-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_133 {
    uint256 public dataPoint = 133;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 4 : 133;
    }
}
```

## Tushuntirish va Mantiq:
133-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 40
```


# 134-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #134
## Topshiriq sharti:
134-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_134 {
    uint256 public dataPoint = 134;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 5 : 134;
    }
}
```

## Tushuntirish va Mantiq:
134-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 50
```


# 135-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #135
## Topshiriq sharti:
135-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_135 {
    uint256 public dataPoint = 135;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 1 : 135;
    }
}
```

## Tushuntirish va Mantiq:
135-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 10
```


# 136-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #136
## Topshiriq sharti:
136-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_136 {
    uint256 public dataPoint = 136;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 2 : 136;
    }
}
```

## Tushuntirish va Mantiq:
136-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 20
```


# 137-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #137
## Topshiriq sharti:
137-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_137 {
    uint256 public dataPoint = 137;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 3 : 137;
    }
}
```

## Tushuntirish va Mantiq:
137-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 30
```


# 138-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #138
## Topshiriq sharti:
138-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_138 {
    uint256 public dataPoint = 138;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 4 : 138;
    }
}
```

## Tushuntirish va Mantiq:
138-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 40
```


# 139-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #139
## Topshiriq sharti:
139-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_139 {
    uint256 public dataPoint = 139;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 5 : 139;
    }
}
```

## Tushuntirish va Mantiq:
139-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 50
```


# 140-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #140
## Topshiriq sharti:
140-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_140 {
    uint256 public dataPoint = 140;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 1 : 140;
    }
}
```

## Tushuntirish va Mantiq:
140-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 10
```


# 141-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #141
## Topshiriq sharti:
141-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_141 {
    uint256 public dataPoint = 141;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 2 : 141;
    }
}
```

## Tushuntirish va Mantiq:
141-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 20
```


# 142-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #142
## Topshiriq sharti:
142-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_142 {
    uint256 public dataPoint = 142;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 3 : 142;
    }
}
```

## Tushuntirish va Mantiq:
142-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 30
```


# 143-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #143
## Topshiriq sharti:
143-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_143 {
    uint256 public dataPoint = 143;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 4 : 143;
    }
}
```

## Tushuntirish va Mantiq:
143-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 40
```


# 144-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #144
## Topshiriq sharti:
144-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_144 {
    uint256 public dataPoint = 144;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 5 : 144;
    }
}
```

## Tushuntirish va Mantiq:
144-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 50
```


# 145-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #145
## Topshiriq sharti:
145-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_145 {
    uint256 public dataPoint = 145;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 1 : 145;
    }
}
```

## Tushuntirish va Mantiq:
145-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 10
```


# 146-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #146
## Topshiriq sharti:
146-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_146 {
    uint256 public dataPoint = 146;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 2 : 146;
    }
}
```

## Tushuntirish va Mantiq:
146-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 20
```


# 147-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #147
## Topshiriq sharti:
147-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_147 {
    uint256 public dataPoint = 147;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 3 : 147;
    }
}
```

## Tushuntirish va Mantiq:
147-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 30
```


# 148-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #148
## Topshiriq sharti:
148-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_148 {
    uint256 public dataPoint = 148;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 4 : 148;
    }
}
```

## Tushuntirish va Mantiq:
148-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 40
```


# 149-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #149
## Topshiriq sharti:
149-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_149 {
    uint256 public dataPoint = 149;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 5 : 149;
    }
}
```

## Tushuntirish va Mantiq:
149-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 50
```


# 150-Topshiriq: EVM xotira boshqaruvi va joylashuv tahlili #150
## Topshiriq sharti:
150-vazifa: Storage slotlari, memory massivlar va calldata optimizatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MemoryStorage_150 {
    uint256 public dataPoint = 150;

    function processArray(uint256[] calldata input) external pure returns (uint256) {
        return input.length > 0 ? input[0] * 1 : 150;
    }
}
```

## Tushuntirish va Mantiq:
150-topshiriqda calldata yordamida gas tejash va xotira boshqaruvi ko'rsatildi.

## Ishlash natijasi:
```text
processArray([10, 20]) -> 10
```

