# 201-Topshiriq: Dinamik massivlar: .push() va .pop()
## Topshiriq sharti:
Elementlar soni o'zgaruvchi massivni yaratib, unga element qo'shish va oxirgisini o'chirish.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
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
```

## Tushuntirish va Mantiq:
Dinamik massivlarda `.push(x)` oxiriga qo'shadi, `.pop()` oxirgisini o'chiradi va hajmni 1 taga qisqartiradi.

## Ishlash natijasi:
```text
addScore(100) chaqirildi.
addScore(200) chaqirildi.
scores.length -> 2
removeLast() chaqirildi.
scores.length -> 1
```


# 202-Topshiriq: Fikslangan o'lchamli massivlar: uint256[N]
## Topshiriq sharti:
Xotirada 4 ta elementli qat'iy massiv e'lon qilib boshqaring.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FixedArrayDemo {
    uint256[4] public fixedSlots = [10, 20, 30, 40];

    function updateSlot(uint256 index, uint256 value) external {
        require(index < 4, "Indeks chegaradan tashqarida");
        fixedSlots[index] = value;
    }
}
```

## Tushuntirish va Mantiq:
Fikslangan massivlar `.push` yoki `.pop` metodlariga ega emas, chunki ularning o'lchami kompilyatsiya paytida belgilanadi.

## Ishlash natijasi:
```text
fixedSlots[2] -> 30
updateSlot(2, 99) chaqirildi.
fixedSlots[2] -> 99
```


# 203-Topshiriq: delete operatori massivlarda
## Topshiriq sharti:
Massiv elementini o'chirganda uzunlik o'zgarmasdan default qiymatga (0) qaytishini ko'rsating.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DeleteArrayDemo {
    uint256[] public items = [10, 20, 30];

    function resetElement(uint256 index) external {
        delete items[index];
    }
}
```

## Tushuntirish va Mantiq:
Massivda `delete items[i]` elementni massivdan sug'urib olmaydi, shunchaki uning qiymatini 0 ga aylantiradi va massiv uzunligi o'zgarmaydi.

## Ishlash natijasi:
```text
items[1] -> 20
resetElement(1) chaqirildi.
items[1] -> 0
items.length -> 3
```


# 204-Topshiriq: Mapping (Assotsiativ jadval): mapping(address => uint256)
## Topshiriq sharti:
Foydalanuvchilarning balanslarini saqlash uchun mappingdan foydalaning.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MappingDemo {
    mapping(address => uint256) public balances;

    function setBalance(address user, uint256 amount) external {
        balances[user] = amount;
    }
}
```

## Tushuntirish va Mantiq:
Mapping xesh jadval bo'lib, uning barcha mumkin bo'lgan kalitlari boshlang'ich 0 qiymatga ega bo'ladi. Unda uzunlik yoki kalitlar ro'yxati mavjud emas.

## Ishlash natijasi:
```text
setBalance(0x5B38..., 500) chaqirildi.
balances(0x5B38...) -> 500
balances(0xNomalum...) -> 0
```


# 205-Topshiriq: Ichma-ich mappinglar (Nested Mappings)
## Topshiriq sharti:
ERC-20 tokenlaridagi kabi ruxsatnomalar (allowance) tizimini loyihalang.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NestedMappingDemo {
    // egasi => sarflovchi => ruxsat etilgan miqdor
    mapping(address => mapping(address => uint256)) public allowance;

    function approve(address spender, uint256 amount) external {
        allowance[msg.sender][spender] = amount;
    }
}
```

## Tushuntirish va Mantiq:
Ichma-ich mappinglar ko'p o'lchamli bog'liqliklarni (masalan, kim kimga qancha ruxsat bergani) modellashtirishda standartdir.

## Ishlash natijasi:
```text
approve(0xSpenderAddress..., 1000) chaqirildi.
allowance(0xOwner..., 0xSpender...) -> 1000
```


# 206-Topshiriq: Massivlar va mappinglar muhandisligi #206
## Topshiriq sharti:
206-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_206 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
206-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(206) bajarildi.
recordOwner(206) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 207-Topshiriq: Massivlar va mappinglar muhandisligi #207
## Topshiriq sharti:
207-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_207 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
207-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(207) bajarildi.
recordOwner(207) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 208-Topshiriq: Massivlar va mappinglar muhandisligi #208
## Topshiriq sharti:
208-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_208 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
208-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(208) bajarildi.
recordOwner(208) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 209-Topshiriq: Massivlar va mappinglar muhandisligi #209
## Topshiriq sharti:
209-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_209 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
209-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(209) bajarildi.
recordOwner(209) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 210-Topshiriq: Massivlar va mappinglar muhandisligi #210
## Topshiriq sharti:
210-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_210 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
210-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(210) bajarildi.
recordOwner(210) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 211-Topshiriq: Massivlar va mappinglar muhandisligi #211
## Topshiriq sharti:
211-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_211 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
211-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(211) bajarildi.
recordOwner(211) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 212-Topshiriq: Massivlar va mappinglar muhandisligi #212
## Topshiriq sharti:
212-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_212 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
212-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(212) bajarildi.
recordOwner(212) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 213-Topshiriq: Massivlar va mappinglar muhandisligi #213
## Topshiriq sharti:
213-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_213 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
213-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(213) bajarildi.
recordOwner(213) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 214-Topshiriq: Massivlar va mappinglar muhandisligi #214
## Topshiriq sharti:
214-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_214 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
214-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(214) bajarildi.
recordOwner(214) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 215-Topshiriq: Massivlar va mappinglar muhandisligi #215
## Topshiriq sharti:
215-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_215 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
215-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(215) bajarildi.
recordOwner(215) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 216-Topshiriq: Massivlar va mappinglar muhandisligi #216
## Topshiriq sharti:
216-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_216 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
216-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(216) bajarildi.
recordOwner(216) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 217-Topshiriq: Massivlar va mappinglar muhandisligi #217
## Topshiriq sharti:
217-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_217 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
217-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(217) bajarildi.
recordOwner(217) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 218-Topshiriq: Massivlar va mappinglar muhandisligi #218
## Topshiriq sharti:
218-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_218 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
218-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(218) bajarildi.
recordOwner(218) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 219-Topshiriq: Massivlar va mappinglar muhandisligi #219
## Topshiriq sharti:
219-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_219 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
219-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(219) bajarildi.
recordOwner(219) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 220-Topshiriq: Massivlar va mappinglar muhandisligi #220
## Topshiriq sharti:
220-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_220 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
220-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(220) bajarildi.
recordOwner(220) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 221-Topshiriq: Massivlar va mappinglar muhandisligi #221
## Topshiriq sharti:
221-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_221 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
221-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(221) bajarildi.
recordOwner(221) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 222-Topshiriq: Massivlar va mappinglar muhandisligi #222
## Topshiriq sharti:
222-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_222 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
222-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(222) bajarildi.
recordOwner(222) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 223-Topshiriq: Massivlar va mappinglar muhandisligi #223
## Topshiriq sharti:
223-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_223 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
223-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(223) bajarildi.
recordOwner(223) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 224-Topshiriq: Massivlar va mappinglar muhandisligi #224
## Topshiriq sharti:
224-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_224 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
224-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(224) bajarildi.
recordOwner(224) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 225-Topshiriq: Massivlar va mappinglar muhandisligi #225
## Topshiriq sharti:
225-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_225 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
225-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(225) bajarildi.
recordOwner(225) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 226-Topshiriq: Massivlar va mappinglar muhandisligi #226
## Topshiriq sharti:
226-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_226 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
226-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(226) bajarildi.
recordOwner(226) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 227-Topshiriq: Massivlar va mappinglar muhandisligi #227
## Topshiriq sharti:
227-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_227 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
227-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(227) bajarildi.
recordOwner(227) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 228-Topshiriq: Massivlar va mappinglar muhandisligi #228
## Topshiriq sharti:
228-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_228 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
228-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(228) bajarildi.
recordOwner(228) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 229-Topshiriq: Massivlar va mappinglar muhandisligi #229
## Topshiriq sharti:
229-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_229 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
229-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(229) bajarildi.
recordOwner(229) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 230-Topshiriq: Massivlar va mappinglar muhandisligi #230
## Topshiriq sharti:
230-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_230 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
230-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(230) bajarildi.
recordOwner(230) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 231-Topshiriq: Massivlar va mappinglar muhandisligi #231
## Topshiriq sharti:
231-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_231 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
231-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(231) bajarildi.
recordOwner(231) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 232-Topshiriq: Massivlar va mappinglar muhandisligi #232
## Topshiriq sharti:
232-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_232 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
232-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(232) bajarildi.
recordOwner(232) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 233-Topshiriq: Massivlar va mappinglar muhandisligi #233
## Topshiriq sharti:
233-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_233 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
233-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(233) bajarildi.
recordOwner(233) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 234-Topshiriq: Massivlar va mappinglar muhandisligi #234
## Topshiriq sharti:
234-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_234 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
234-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(234) bajarildi.
recordOwner(234) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 235-Topshiriq: Massivlar va mappinglar muhandisligi #235
## Topshiriq sharti:
235-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_235 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
235-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(235) bajarildi.
recordOwner(235) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 236-Topshiriq: Massivlar va mappinglar muhandisligi #236
## Topshiriq sharti:
236-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_236 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
236-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(236) bajarildi.
recordOwner(236) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 237-Topshiriq: Massivlar va mappinglar muhandisligi #237
## Topshiriq sharti:
237-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_237 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
237-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(237) bajarildi.
recordOwner(237) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 238-Topshiriq: Massivlar va mappinglar muhandisligi #238
## Topshiriq sharti:
238-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_238 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
238-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(238) bajarildi.
recordOwner(238) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 239-Topshiriq: Massivlar va mappinglar muhandisligi #239
## Topshiriq sharti:
239-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_239 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
239-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(239) bajarildi.
recordOwner(239) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 240-Topshiriq: Massivlar va mappinglar muhandisligi #240
## Topshiriq sharti:
240-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_240 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
240-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(240) bajarildi.
recordOwner(240) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 241-Topshiriq: Massivlar va mappinglar muhandisligi #241
## Topshiriq sharti:
241-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_241 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
241-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(241) bajarildi.
recordOwner(241) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 242-Topshiriq: Massivlar va mappinglar muhandisligi #242
## Topshiriq sharti:
242-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_242 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
242-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(242) bajarildi.
recordOwner(242) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 243-Topshiriq: Massivlar va mappinglar muhandisligi #243
## Topshiriq sharti:
243-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_243 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
243-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(243) bajarildi.
recordOwner(243) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 244-Topshiriq: Massivlar va mappinglar muhandisligi #244
## Topshiriq sharti:
244-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_244 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
244-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(244) bajarildi.
recordOwner(244) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 245-Topshiriq: Massivlar va mappinglar muhandisligi #245
## Topshiriq sharti:
245-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_245 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
245-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(245) bajarildi.
recordOwner(245) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 246-Topshiriq: Massivlar va mappinglar muhandisligi #246
## Topshiriq sharti:
246-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_246 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
246-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(246) bajarildi.
recordOwner(246) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 247-Topshiriq: Massivlar va mappinglar muhandisligi #247
## Topshiriq sharti:
247-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_247 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
247-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(247) bajarildi.
recordOwner(247) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 248-Topshiriq: Massivlar va mappinglar muhandisligi #248
## Topshiriq sharti:
248-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_248 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
248-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(248) bajarildi.
recordOwner(248) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 249-Topshiriq: Massivlar va mappinglar muhandisligi #249
## Topshiriq sharti:
249-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_249 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
249-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(249) bajarildi.
recordOwner(249) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```


# 250-Topshiriq: Massivlar va mappinglar muhandisligi #250
## Topshiriq sharti:
250-vazifa: Xotira zichligi, kalit-qiymat tuzilmalari va ma'lumotlar agregatsiyasi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStore_250 {
    mapping(uint256 => address) public recordOwner;
    uint256[] public recordIds;

    function registerRecord(uint256 id) external {
        recordOwner[id] = msg.sender;
        recordIds.push(id);
    }
}
```

## Tushuntirish va Mantiq:
250-topshiriqda mapping va massiv birgalikda qo'llanilib, kalitlar bo'yicha iteratsiya qilish imkoni yaratildi.

## Ishlash natijasi:
```text
registerRecord(250) bajarildi.
recordOwner(250) -> 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
```

