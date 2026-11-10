# 51-Topshiriq: Funksiya ko'rinishi: public vs external
## Topshiriq sharti:
public va external funksiyalarning gas narxi va chaqirilish joylari farqini ko'rsating.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
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
```

## Tushuntirish va Mantiq:
'external' funksiyalar faqat kontrakt tashqarisidan chaqirilishi mumkin va massiv argumentlarini 'calldata'da to'g'ridan-to'g'ri o'qib gas tejaydi. 'public' esa kontrakt ichidan ham, tashqarisidan ham chaqiriladi.

## Ishlash natijasi:
```text
publicFunction() -> 777
externalFunction([1, 2, 3, 4]) -> 4
```


# 52-Topshiriq: Funksiya ko'rinishi: internal vs private
## Topshiriq sharti:
Merosxo'rlar uchun ochiq (internal) va faqat joriy kontrakt ichida yopiq (private) metodlarni loyihalang.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
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
```

## Tushuntirish va Mantiq:
'private' funksiyalar hatto undan meros olgan bolalar kontraktlariga ham ko'rinmaydi. 'internal' esa joriy va barcha merosxo'r kontraktlar ichida bemalol chaqiriladi.

## Ishlash natijasi:
```text
execute(5) -> 20
```


# 53-Topshiriq: Holat mutabilligi: pure funksiyalar
## Topshiriq sharti:
Blokcheyn holatini umuman o'qimaydigan va o'zgartirmaydigan sof matematik funksiya yozing.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract PureDemo {
    function multiply(uint256 x, uint256 y) external pure returns (uint256) {
        return x * y;
    }
}
```

## Tushuntirish va Mantiq:
'pure' funksiyalar storage o'zgaruvchilarini ham, global 'msg.sender'/'block.timestamp' kabi parametrlarni ham o'qimaydi. Faqat kiritilgan parametrlar ustida amallar bajaradi.

## Ishlash natijasi:
```text
multiply(7, 8) -> 56
```


# 54-Topshiriq: Holat mutabilligi: view funksiyalar
## Topshiriq sharti:
Holat o'zgaruvchilarini faqat o'qiydigan, lekin hech qanday holatni o'zgartirmaydigan funksiya tuzing.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract ViewDemo {
    uint256 public score = 100;

    function getScorePlus(uint256 bonus) external view returns (uint256) {
        return score + bonus;
    }
}
```

## Tushuntirish va Mantiq:
'view' funksiyalar holatni o'qiy oladi, biroq hech narsani o'zgartira olmaydi. Tashqi chaqiruvlarda (eth_call) 'view' va 'pure' funksiyalar nol gas sarflaydi.

## Ishlash natijasi:
```text
getScorePlus(25) -> 125
```


# 55-Topshiriq: Ko'p qiymat qaytarish (Multiple Return Values)
## Topshiriq sharti:
Bitta chaqiruvda nomlangan bir nechta natijalarni qaytaruvchi funksiya yozing.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MultiReturnDemo {
    function calculate(uint256 a, uint256 b) external pure returns (uint256 sum, uint256 diff, uint256 prod) {
        sum = a + b;
        diff = a > b ? a - b : b - a;
        prod = a * b;
    }
}
```

## Tushuntirish va Mantiq:
Solidity-da funksiyalar `returns (type1 name1, type2 name2)` orqali bir vaqtning o'zida bir nechta qiymat qaytara oladi.

## Ishlash natijasi:
```text
calculate(10, 4) -> (sum: 14, diff: 6, prod: 40)
```


# 56-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #56
## Topshiriq sharti:
56-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_56 {
    uint256 public rate = 56;

    function process_56(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 0;
    }
}
```

## Tushuntirish va Mantiq:
56-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_56(10) -> 560
```


# 57-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #57
## Topshiriq sharti:
57-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_57 {
    uint256 public rate = 57;

    function process_57(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 1;
    }
}
```

## Tushuntirish va Mantiq:
57-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_57(10) -> 571
```


# 58-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #58
## Topshiriq sharti:
58-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_58 {
    uint256 public rate = 58;

    function process_58(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 2;
    }
}
```

## Tushuntirish va Mantiq:
58-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_58(10) -> 582
```


# 59-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #59
## Topshiriq sharti:
59-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_59 {
    uint256 public rate = 59;

    function process_59(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 3;
    }
}
```

## Tushuntirish va Mantiq:
59-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_59(10) -> 593
```


# 60-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #60
## Topshiriq sharti:
60-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_60 {
    uint256 public rate = 60;

    function process_60(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 4;
    }
}
```

## Tushuntirish va Mantiq:
60-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_60(10) -> 604
```


# 61-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #61
## Topshiriq sharti:
61-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_61 {
    uint256 public rate = 61;

    function process_61(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 5;
    }
}
```

## Tushuntirish va Mantiq:
61-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_61(10) -> 615
```


# 62-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #62
## Topshiriq sharti:
62-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_62 {
    uint256 public rate = 62;

    function process_62(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 6;
    }
}
```

## Tushuntirish va Mantiq:
62-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_62(10) -> 626
```


# 63-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #63
## Topshiriq sharti:
63-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_63 {
    uint256 public rate = 63;

    function process_63(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 0;
    }
}
```

## Tushuntirish va Mantiq:
63-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_63(10) -> 630
```


# 64-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #64
## Topshiriq sharti:
64-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_64 {
    uint256 public rate = 64;

    function process_64(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 1;
    }
}
```

## Tushuntirish va Mantiq:
64-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_64(10) -> 641
```


# 65-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #65
## Topshiriq sharti:
65-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_65 {
    uint256 public rate = 65;

    function process_65(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 2;
    }
}
```

## Tushuntirish va Mantiq:
65-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_65(10) -> 652
```


# 66-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #66
## Topshiriq sharti:
66-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_66 {
    uint256 public rate = 66;

    function process_66(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 3;
    }
}
```

## Tushuntirish va Mantiq:
66-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_66(10) -> 663
```


# 67-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #67
## Topshiriq sharti:
67-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_67 {
    uint256 public rate = 67;

    function process_67(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 4;
    }
}
```

## Tushuntirish va Mantiq:
67-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_67(10) -> 674
```


# 68-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #68
## Topshiriq sharti:
68-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_68 {
    uint256 public rate = 68;

    function process_68(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 5;
    }
}
```

## Tushuntirish va Mantiq:
68-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_68(10) -> 685
```


# 69-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #69
## Topshiriq sharti:
69-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_69 {
    uint256 public rate = 69;

    function process_69(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 6;
    }
}
```

## Tushuntirish va Mantiq:
69-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_69(10) -> 696
```


# 70-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #70
## Topshiriq sharti:
70-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_70 {
    uint256 public rate = 70;

    function process_70(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 0;
    }
}
```

## Tushuntirish va Mantiq:
70-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_70(10) -> 700
```


# 71-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #71
## Topshiriq sharti:
71-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_71 {
    uint256 public rate = 71;

    function process_71(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 1;
    }
}
```

## Tushuntirish va Mantiq:
71-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_71(10) -> 711
```


# 72-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #72
## Topshiriq sharti:
72-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_72 {
    uint256 public rate = 72;

    function process_72(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 2;
    }
}
```

## Tushuntirish va Mantiq:
72-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_72(10) -> 722
```


# 73-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #73
## Topshiriq sharti:
73-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_73 {
    uint256 public rate = 73;

    function process_73(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 3;
    }
}
```

## Tushuntirish va Mantiq:
73-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_73(10) -> 733
```


# 74-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #74
## Topshiriq sharti:
74-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_74 {
    uint256 public rate = 74;

    function process_74(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 4;
    }
}
```

## Tushuntirish va Mantiq:
74-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_74(10) -> 744
```


# 75-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #75
## Topshiriq sharti:
75-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_75 {
    uint256 public rate = 75;

    function process_75(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 5;
    }
}
```

## Tushuntirish va Mantiq:
75-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_75(10) -> 755
```


# 76-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #76
## Topshiriq sharti:
76-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_76 {
    uint256 public rate = 76;

    function process_76(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 6;
    }
}
```

## Tushuntirish va Mantiq:
76-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_76(10) -> 766
```


# 77-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #77
## Topshiriq sharti:
77-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_77 {
    uint256 public rate = 77;

    function process_77(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 0;
    }
}
```

## Tushuntirish va Mantiq:
77-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_77(10) -> 770
```


# 78-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #78
## Topshiriq sharti:
78-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_78 {
    uint256 public rate = 78;

    function process_78(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 1;
    }
}
```

## Tushuntirish va Mantiq:
78-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_78(10) -> 781
```


# 79-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #79
## Topshiriq sharti:
79-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_79 {
    uint256 public rate = 79;

    function process_79(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 2;
    }
}
```

## Tushuntirish va Mantiq:
79-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_79(10) -> 792
```


# 80-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #80
## Topshiriq sharti:
80-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_80 {
    uint256 public rate = 80;

    function process_80(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 3;
    }
}
```

## Tushuntirish va Mantiq:
80-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_80(10) -> 803
```


# 81-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #81
## Topshiriq sharti:
81-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_81 {
    uint256 public rate = 81;

    function process_81(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 4;
    }
}
```

## Tushuntirish va Mantiq:
81-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_81(10) -> 814
```


# 82-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #82
## Topshiriq sharti:
82-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_82 {
    uint256 public rate = 82;

    function process_82(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 5;
    }
}
```

## Tushuntirish va Mantiq:
82-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_82(10) -> 825
```


# 83-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #83
## Topshiriq sharti:
83-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_83 {
    uint256 public rate = 83;

    function process_83(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 6;
    }
}
```

## Tushuntirish va Mantiq:
83-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_83(10) -> 836
```


# 84-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #84
## Topshiriq sharti:
84-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_84 {
    uint256 public rate = 84;

    function process_84(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 0;
    }
}
```

## Tushuntirish va Mantiq:
84-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_84(10) -> 840
```


# 85-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #85
## Topshiriq sharti:
85-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_85 {
    uint256 public rate = 85;

    function process_85(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 1;
    }
}
```

## Tushuntirish va Mantiq:
85-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_85(10) -> 851
```


# 86-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #86
## Topshiriq sharti:
86-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_86 {
    uint256 public rate = 86;

    function process_86(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 2;
    }
}
```

## Tushuntirish va Mantiq:
86-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_86(10) -> 862
```


# 87-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #87
## Topshiriq sharti:
87-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_87 {
    uint256 public rate = 87;

    function process_87(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 3;
    }
}
```

## Tushuntirish va Mantiq:
87-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_87(10) -> 873
```


# 88-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #88
## Topshiriq sharti:
88-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_88 {
    uint256 public rate = 88;

    function process_88(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 4;
    }
}
```

## Tushuntirish va Mantiq:
88-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_88(10) -> 884
```


# 89-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #89
## Topshiriq sharti:
89-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_89 {
    uint256 public rate = 89;

    function process_89(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 5;
    }
}
```

## Tushuntirish va Mantiq:
89-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_89(10) -> 895
```


# 90-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #90
## Topshiriq sharti:
90-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_90 {
    uint256 public rate = 90;

    function process_90(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 6;
    }
}
```

## Tushuntirish va Mantiq:
90-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_90(10) -> 906
```


# 91-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #91
## Topshiriq sharti:
91-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_91 {
    uint256 public rate = 91;

    function process_91(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 0;
    }
}
```

## Tushuntirish va Mantiq:
91-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_91(10) -> 910
```


# 92-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #92
## Topshiriq sharti:
92-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_92 {
    uint256 public rate = 92;

    function process_92(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 1;
    }
}
```

## Tushuntirish va Mantiq:
92-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_92(10) -> 921
```


# 93-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #93
## Topshiriq sharti:
93-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_93 {
    uint256 public rate = 93;

    function process_93(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 2;
    }
}
```

## Tushuntirish va Mantiq:
93-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_93(10) -> 932
```


# 94-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #94
## Topshiriq sharti:
94-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_94 {
    uint256 public rate = 94;

    function process_94(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 3;
    }
}
```

## Tushuntirish va Mantiq:
94-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_94(10) -> 943
```


# 95-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #95
## Topshiriq sharti:
95-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_95 {
    uint256 public rate = 95;

    function process_95(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 4;
    }
}
```

## Tushuntirish va Mantiq:
95-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_95(10) -> 954
```


# 96-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #96
## Topshiriq sharti:
96-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_96 {
    uint256 public rate = 96;

    function process_96(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 5;
    }
}
```

## Tushuntirish va Mantiq:
96-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_96(10) -> 965
```


# 97-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #97
## Topshiriq sharti:
97-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_97 {
    uint256 public rate = 97;

    function process_97(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 6;
    }
}
```

## Tushuntirish va Mantiq:
97-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_97(10) -> 976
```


# 98-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #98
## Topshiriq sharti:
98-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_98 {
    uint256 public rate = 98;

    function process_98(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 0;
    }
}
```

## Tushuntirish va Mantiq:
98-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_98(10) -> 980
```


# 99-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #99
## Topshiriq sharti:
99-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_99 {
    uint256 public rate = 99;

    function process_99(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 1;
    }
}
```

## Tushuntirish va Mantiq:
99-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_99(10) -> 991
```


# 100-Topshiriq: Funksiyalar arxitekturasi va ko'rinish doirasi #100
## Topshiriq sharti:
100-vazifa: Getter metodlar, parametrlarni uzatish va EVM mutabilligi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FuncContract_100 {
    uint256 public rate = 100;

    function process_100(uint256 inputVal) external view returns (uint256) {
        return inputVal * rate + 2;
    }
}
```

## Tushuntirish va Mantiq:
100-topshiriqda view funksiyasi va holat mutabilligi qoidalari asosida toza interfeys yaratildi.

## Ishlash natijasi:
```text
process_100(10) -> 1002
```

