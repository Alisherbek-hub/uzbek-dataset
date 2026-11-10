# 601-Topshiriq: IERC721 Interfeysi va NFT arxitekturasi
## Topshiriq sharti:
Noyob raqamli san'at va aktivlar uchun rasmiy ERC-721 interfeysini e'lon qiling.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IERC721 {
    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);
    event Approval(address indexed owner, address indexed approved, uint256 indexed tokenId);

    function balanceOf(address owner) external view returns (uint256);
    function ownerOf(uint256 tokenId) external view returns (address);
    function safeTransferFrom(address from, address to, uint256 tokenId) external;
}
```

## Tushuntirish va Mantiq:
ERC-721 standarti har bir tokenning noyob `tokenId` identifikatoriga ega bo'lishini va takrorlanmasligini ta'minlaydi.

## Ishlash natijasi:
```text
IERC721 e'lon qilindi.
```


# 602-Topshiriq: Shaxsiy ERC-721 NFT kontraktini noldan yozish
## Topshiriq sharti:
O'zbek madaniy merosi NFT kolleksiyasi kontraktini loyihalang.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
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
```

## Tushuntirish va Mantiq:
NFT larda har bir `tokenId` aniq bitta egaga (`_owners[tokenId]`) tegishli bo'ladi.

## Ishlash natijasi:
```text
HeritageNFT deploy qilindi.
mint(0xArtist..., 1) bajarildi.
ownerOf(1) -> 0xArtist...
```


# 603-Topshiriq: tokenURI va JSON Metadata formati
## Topshiriq sharti:
IPFS tarmog'idagi rasm va ma'lumotlar bilan bog'lovchi tokenURI funksiyasini yozing.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
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
```

## Tushuntirish va Mantiq:
`tokenURI(tokenId)` OpenSea yoki Rarible kabi bozorlarga NFT tasviri, nomi va xususiyatlarini (attributes) yuklab ko'rsatish imkonini beradi.

## Ishlash natijasi:
```text
tokenURI(1) -> "ipfs://QmXoy.../token_1.json"
```


# 604-Topshiriq: safeTransferFrom va IERC721Receiver xavfsizligi
## Topshiriq sharti:
Smart kontrakt manziliga NFT yuborilganda aktivlar abadiy qulflanib qolmasligini kafolatlang.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
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
```

## Tushuntirish va Mantiq:
`safeTransferFrom` qabul qiluvchi kontraktning `onERC721Received` interfeysini tekshiradi va NFT yo'qolib ketishining oldini oladi.

## Ishlash natijasi:
```text
Receiver tekshirildi -> Xavfsiz.
```


# 605-Topshiriq: Royalti standarti: EIP-2981
## Topshiriq sharti:
NFT ikkilamchi bozorda har safar qayta sotilganda muallifga foiz to'lanishini ta'minlang.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract RoyaltyDemo {
    address public artist = msg.sender;
    uint96 public royaltyBasisPoints = 500; // 5% (500 / 10000)

    function royaltyInfo(uint256, uint256 salePrice) external view returns (address receiver, uint256 royaltyAmount) {
        receiver = artist;
        royaltyAmount = (salePrice * royaltyBasisPoints) / 10000;
    }
}
```

## Tushuntirish va Mantiq:
EIP-2981 standarti barcha NFT bozorlariga bir xil qoidada mualliflik gonorarini to'lash imkonini yaratadi.

## Ishlash natijasi:
```text
royaltyInfo(1, 10 ether) -> (0xArtist..., 0.5 ether)
```


# 606-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #606
## Topshiriq sharti:
606-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_606 {
    string public constant COLLECTION_TAG = "COL_606";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
606-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_606 deploy qilindi.
mintItem(606) bajarildi.
```


# 607-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #607
## Topshiriq sharti:
607-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_607 {
    string public constant COLLECTION_TAG = "COL_607";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
607-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_607 deploy qilindi.
mintItem(607) bajarildi.
```


# 608-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #608
## Topshiriq sharti:
608-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_608 {
    string public constant COLLECTION_TAG = "COL_608";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
608-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_608 deploy qilindi.
mintItem(608) bajarildi.
```


# 609-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #609
## Topshiriq sharti:
609-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_609 {
    string public constant COLLECTION_TAG = "COL_609";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
609-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_609 deploy qilindi.
mintItem(609) bajarildi.
```


# 610-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #610
## Topshiriq sharti:
610-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_610 {
    string public constant COLLECTION_TAG = "COL_610";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
610-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_610 deploy qilindi.
mintItem(610) bajarildi.
```


# 611-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #611
## Topshiriq sharti:
611-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_611 {
    string public constant COLLECTION_TAG = "COL_611";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
611-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_611 deploy qilindi.
mintItem(611) bajarildi.
```


# 612-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #612
## Topshiriq sharti:
612-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_612 {
    string public constant COLLECTION_TAG = "COL_612";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
612-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_612 deploy qilindi.
mintItem(612) bajarildi.
```


# 613-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #613
## Topshiriq sharti:
613-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_613 {
    string public constant COLLECTION_TAG = "COL_613";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
613-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_613 deploy qilindi.
mintItem(613) bajarildi.
```


# 614-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #614
## Topshiriq sharti:
614-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_614 {
    string public constant COLLECTION_TAG = "COL_614";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
614-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_614 deploy qilindi.
mintItem(614) bajarildi.
```


# 615-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #615
## Topshiriq sharti:
615-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_615 {
    string public constant COLLECTION_TAG = "COL_615";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
615-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_615 deploy qilindi.
mintItem(615) bajarildi.
```


# 616-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #616
## Topshiriq sharti:
616-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_616 {
    string public constant COLLECTION_TAG = "COL_616";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
616-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_616 deploy qilindi.
mintItem(616) bajarildi.
```


# 617-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #617
## Topshiriq sharti:
617-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_617 {
    string public constant COLLECTION_TAG = "COL_617";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
617-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_617 deploy qilindi.
mintItem(617) bajarildi.
```


# 618-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #618
## Topshiriq sharti:
618-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_618 {
    string public constant COLLECTION_TAG = "COL_618";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
618-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_618 deploy qilindi.
mintItem(618) bajarildi.
```


# 619-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #619
## Topshiriq sharti:
619-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_619 {
    string public constant COLLECTION_TAG = "COL_619";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
619-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_619 deploy qilindi.
mintItem(619) bajarildi.
```


# 620-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #620
## Topshiriq sharti:
620-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_620 {
    string public constant COLLECTION_TAG = "COL_620";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
620-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_620 deploy qilindi.
mintItem(620) bajarildi.
```


# 621-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #621
## Topshiriq sharti:
621-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_621 {
    string public constant COLLECTION_TAG = "COL_621";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
621-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_621 deploy qilindi.
mintItem(621) bajarildi.
```


# 622-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #622
## Topshiriq sharti:
622-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_622 {
    string public constant COLLECTION_TAG = "COL_622";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
622-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_622 deploy qilindi.
mintItem(622) bajarildi.
```


# 623-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #623
## Topshiriq sharti:
623-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_623 {
    string public constant COLLECTION_TAG = "COL_623";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
623-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_623 deploy qilindi.
mintItem(623) bajarildi.
```


# 624-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #624
## Topshiriq sharti:
624-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_624 {
    string public constant COLLECTION_TAG = "COL_624";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
624-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_624 deploy qilindi.
mintItem(624) bajarildi.
```


# 625-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #625
## Topshiriq sharti:
625-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_625 {
    string public constant COLLECTION_TAG = "COL_625";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
625-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_625 deploy qilindi.
mintItem(625) bajarildi.
```


# 626-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #626
## Topshiriq sharti:
626-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_626 {
    string public constant COLLECTION_TAG = "COL_626";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
626-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_626 deploy qilindi.
mintItem(626) bajarildi.
```


# 627-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #627
## Topshiriq sharti:
627-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_627 {
    string public constant COLLECTION_TAG = "COL_627";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
627-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_627 deploy qilindi.
mintItem(627) bajarildi.
```


# 628-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #628
## Topshiriq sharti:
628-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_628 {
    string public constant COLLECTION_TAG = "COL_628";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
628-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_628 deploy qilindi.
mintItem(628) bajarildi.
```


# 629-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #629
## Topshiriq sharti:
629-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_629 {
    string public constant COLLECTION_TAG = "COL_629";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
629-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_629 deploy qilindi.
mintItem(629) bajarildi.
```


# 630-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #630
## Topshiriq sharti:
630-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_630 {
    string public constant COLLECTION_TAG = "COL_630";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
630-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_630 deploy qilindi.
mintItem(630) bajarildi.
```


# 631-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #631
## Topshiriq sharti:
631-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_631 {
    string public constant COLLECTION_TAG = "COL_631";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
631-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_631 deploy qilindi.
mintItem(631) bajarildi.
```


# 632-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #632
## Topshiriq sharti:
632-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_632 {
    string public constant COLLECTION_TAG = "COL_632";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
632-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_632 deploy qilindi.
mintItem(632) bajarildi.
```


# 633-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #633
## Topshiriq sharti:
633-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_633 {
    string public constant COLLECTION_TAG = "COL_633";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
633-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_633 deploy qilindi.
mintItem(633) bajarildi.
```


# 634-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #634
## Topshiriq sharti:
634-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_634 {
    string public constant COLLECTION_TAG = "COL_634";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
634-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_634 deploy qilindi.
mintItem(634) bajarildi.
```


# 635-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #635
## Topshiriq sharti:
635-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_635 {
    string public constant COLLECTION_TAG = "COL_635";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
635-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_635 deploy qilindi.
mintItem(635) bajarildi.
```


# 636-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #636
## Topshiriq sharti:
636-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_636 {
    string public constant COLLECTION_TAG = "COL_636";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
636-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_636 deploy qilindi.
mintItem(636) bajarildi.
```


# 637-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #637
## Topshiriq sharti:
637-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_637 {
    string public constant COLLECTION_TAG = "COL_637";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
637-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_637 deploy qilindi.
mintItem(637) bajarildi.
```


# 638-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #638
## Topshiriq sharti:
638-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_638 {
    string public constant COLLECTION_TAG = "COL_638";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
638-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_638 deploy qilindi.
mintItem(638) bajarildi.
```


# 639-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #639
## Topshiriq sharti:
639-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_639 {
    string public constant COLLECTION_TAG = "COL_639";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
639-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_639 deploy qilindi.
mintItem(639) bajarildi.
```


# 640-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #640
## Topshiriq sharti:
640-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_640 {
    string public constant COLLECTION_TAG = "COL_640";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
640-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_640 deploy qilindi.
mintItem(640) bajarildi.
```


# 641-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #641
## Topshiriq sharti:
641-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_641 {
    string public constant COLLECTION_TAG = "COL_641";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
641-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_641 deploy qilindi.
mintItem(641) bajarildi.
```


# 642-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #642
## Topshiriq sharti:
642-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_642 {
    string public constant COLLECTION_TAG = "COL_642";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
642-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_642 deploy qilindi.
mintItem(642) bajarildi.
```


# 643-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #643
## Topshiriq sharti:
643-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_643 {
    string public constant COLLECTION_TAG = "COL_643";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
643-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_643 deploy qilindi.
mintItem(643) bajarildi.
```


# 644-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #644
## Topshiriq sharti:
644-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_644 {
    string public constant COLLECTION_TAG = "COL_644";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
644-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_644 deploy qilindi.
mintItem(644) bajarildi.
```


# 645-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #645
## Topshiriq sharti:
645-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_645 {
    string public constant COLLECTION_TAG = "COL_645";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
645-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_645 deploy qilindi.
mintItem(645) bajarildi.
```


# 646-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #646
## Topshiriq sharti:
646-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_646 {
    string public constant COLLECTION_TAG = "COL_646";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
646-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_646 deploy qilindi.
mintItem(646) bajarildi.
```


# 647-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #647
## Topshiriq sharti:
647-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_647 {
    string public constant COLLECTION_TAG = "COL_647";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
647-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_647 deploy qilindi.
mintItem(647) bajarildi.
```


# 648-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #648
## Topshiriq sharti:
648-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_648 {
    string public constant COLLECTION_TAG = "COL_648";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
648-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_648 deploy qilindi.
mintItem(648) bajarildi.
```


# 649-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #649
## Topshiriq sharti:
649-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_649 {
    string public constant COLLECTION_TAG = "COL_649";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
649-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_649 deploy qilindi.
mintItem(649) bajarildi.
```


# 650-Topshiriq: ERC-721 NFT muhandisligi va auksionlar #650
## Topshiriq sharti:
650-vazifa: Noyob tokenlar identifikatsiyasi, egalik huquqi va metadata boshqaruvi.

## Yechim (Solidity kodi):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NFTCollection_650 {
    string public constant COLLECTION_TAG = "COL_650";
    mapping(uint256 => address) public ownerOf;

    function mintItem(uint256 id) external {
        ownerOf[id] = msg.sender;
    }
}
```

## Tushuntirish va Mantiq:
650-topshiriqda noyob raqamli tokenlar egaligi va kolleksiya strukturasi yaratildi.

## Ishlash natijasi:
```text
NFTCollection_650 deploy qilindi.
mintItem(650) bajarildi.
```

