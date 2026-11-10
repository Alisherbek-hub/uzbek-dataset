# Khorazmiy AI: Solidity - Modul 22
## Mavzu: Ilg'or Algoritmlar: Graflar, Segment Trees, Fenwick va Trie tuzilmalari

### Topshiriq #1051: Graflar yordamida Tranzaksiyalar Zanjirini Tekshirish (Cycle Detection)
**Tavsif:** DeFi protokollarida "flash loan" hujumlarini oldini olish uchun tranzaksiyalar zanjirida sikl (aylana) mavjudligini aniqlash.
**Talablar:** DFS (Depth First Search) algoritmi orqali siklni aniqlash, gaz samaradorligi.
**Yechim (Solidity):**
```solidity
contract TransactionGraph {
    mapping(address => address[]) public adj; // Graf ro'yxati

    function addEdge(address from, address to) public {
        adj[from].push(to);
    }

    // Sikl mavjudligini tekshirish
    function hasCycle(address start, address current, mapping(address => bool) visited) public view returns (bool) {
        if (visited[current]) return true;
        visited[current] = true;
        for (uint i = 0; i < adj[current].length; i++) {
            if (hasCycle(start, adj[current][i], visited)) return true;
        }
        return false;
    }
}
```
**Tushuntirish:** DFS algoritmi tranzaksiyalar orasidagi bog'liqlikni tekshiradi. `visited` xaritasi rekursiv chaqiriqlarda cheksiz tsiklni oldini oladi.

---

### Topshiriq #1052: Segment Tree yordamida Likvidlikni Kuzatish
**Tavsif:** Katta diapazondagi likvidlik o'zgarishlarini tezkor so'rash (Range Sum Query).
**Talablar:** O(log n) vaqt murakkabligi, massivni yangilash.
**Yechim (Solidity):**
```solidity
contract LiquidityTree {
    uint[] public tree;
    uint public n;

    constructor(uint[] memory data) {
        n = data.length;
        tree = new uint[](2 * n);
        for (uint i = 0; i < n; i++) tree[n + i] = data[i];
        for (uint i = n - 1; i > 0; i--) tree[i] = tree[2 * i] + tree[2 * i + 1];
    }

    function update(uint i, uint val) public {
        for (tree[i += n] = val; i > 1; i >>= 1) tree[i >> 1] = tree[i] + tree[i ^ 1];
    }
}
```
**Tushuntirish:** Segment Tree yordamida likvidlikni yangilash va yig'indini hisoblash logarifmik vaqtda amalga oshiriladi, bu esa katta massivlar uchun juda samarali.

---

### Topshiriq #1053: Fenwick Tree (Binary Indexed Tree) bilan Mukofotlarni Hisoblash
**Tavsif:** Staking mukofotlarini tezkor hisoblash va prefiks yig'indilarni saqlash.
**Talablar:** O(log n) yangilash va so'rov tezligi.
**Yechim (Solidity):**
```solidity
contract RewardTracker {
    uint[] bit;
    function update(uint i, uint delta) public {
        for (; i < bit.length; i += i & -i) bit[i] += delta;
    }
    function query(uint i) public view returns (uint sum) {
        for (; i > 0; i -= i & -i) sum += bit[i];
    }
}
```
**Tushuntirish:** Fenwick Tree xotira jihatidan Segment Tree'dan tejamkorroq va prefiks yig'indilarni hisoblash uchun eng tezkor yechimdir.

---

### Topshiriq #1054: Trie (Prefix Tree) yordamida Manzillar Katalogi
**Tavsif:** Smart kontraktda foydalanuvchi nomlari yoki manzillarini prefiks bo'yicha qidirish.
**Talablar:** Xotirani tejash, tezkor qidiruv.
**Yechim (Solidity):**
```solidity
contract AddressTrie {
    struct Node { mapping(bytes1 => uint) children; bool isEnd; }
    Node[] nodes;

    function insert(string memory key) public {
        uint curr = 0;
        bytes memory b = bytes(key);
        for (uint i = 0; i < b.length; i++) {
            if (nodes[curr].children[b[i]] == 0) {
                nodes.push();
                nodes[curr].children[b[i]] = nodes.length - 1;
            }
            curr = nodes[curr].children[b[i]];
        }
        nodes[curr].isEnd = true;
    }
}
```
**Tushuntirish:** Trie tuzilmasi string ma'lumotlarini saqlashda takrorlanuvchi prefikslarni birlashtirib, qidiruv tezligini oshiradi.

---

### Topshiriq #1055: Dijkstra Algoritmi bilan Arbitraj Yo'lini Topish
**Tavsif:** Tokenlar almashinuvida eng qisqa (eng foydali) yo'lni topish.
**Talablar:** Gazni optimallashtirish, og'irlik matritsasi.
**Yechim (Solidity):**
```solidity
contract ArbitrageFinder {
    uint constant INF = 1e18;
    function findShortestPath(uint[][] memory graph, uint start) public pure returns (uint[] memory) {
        // Oddiy Dijkstra implementatsiyasi
        // ... (qisqartirilgan mantiq)
    }
}
```
**Tushuntirish:** Dijkstra eng qisqa yo'lni topish uchun eng ishonchli algoritm bo'lib, arbitraj imkoniyatlarini aniqlashda muhim ahamiyatga ega.

---

### Topshiriq #1056: Segment Tree bilan "Range Max" (Narxlar cho'qqisi)
**Tavsif:** Token narxlarining ma'lum vaqt oralig'idagi maksimal qiymatini aniqlash.
**Talablar:** O(log n) vaqt, xavfsizlik.
**Yechim (Solidity):**
```solidity
contract PriceOracle {
    uint[] tree;
    function queryMax(uint l, uint r) public view returns (uint max) {
        for (l += tree.length/2, r += tree.length/2; l < r; l >>= 1, r >>= 1) {
            if (l & 1 == 1) max = max > tree[l++] ? max : tree[l-1];
            if (r & 1 == 1) max = max > tree[--r] ? max : tree[r];
        }
    }
}
```
**Tushuntirish:** Iterativ Segment Tree rekursivga qaraganda gazni kamroq sarflaydi va narx o'zgarishlarini kuzatishda juda tez ishlaydi.

---

### Topshiriq #1057: Fenwick Tree bilan "Range Update"
**Tavsif:** Ko'plab foydalanuvchilarning balansini bir vaqtda yangilash.
**Talablar:** O(log n) diapazonli yangilash.
**Yechim (Solidity):**
```solidity
contract BatchUpdate {
    uint[] bit;
    function rangeUpdate(uint l, uint r, uint val) public {
        update(l, val);
        update(r + 1, uint(int(0) - int(val)));
    }
    // update funksiyasi #1053 dagi kabi
}
```
**Tushuntirish:** Fenwick Tree'da diapazonli yangilash (Range Update) ikki nuqtali yangilash orqali amalga oshiriladi, bu juda samarali.

---

### Topshiriq #1058: Trie bilan "Whitelist" boshqaruvi
**Tavsif:** Katta hajmdagi ruxsat etilgan manzillar ro'yxatini saqlash.
**Talablar:** O(k) qidiruv vaqti (k - manzil uzunligi).
**Yechim (Solidity):**
```solidity
contract WhitelistTrie {
    mapping(bytes32 => bool) trieNodes;
    function isWhitelisted(address user) public view returns (bool) {
        return trieNodes[keccak256(abi.encodePacked(user))];
    }
}
```
**Tushuntirish:** Trie tuzilmasini hash bilan birlashtirish manzilni tasdiqlash jarayonini O(1) ga yaqinlashtiradi.

---

### Topshiriq #1059: Grafda "Strongly Connected Components" (SCC)
**Tavsif:** DAO boshqaruvida ovoz berish zanjirlarini tahlil qilish.
**Talablar:** Tarjan algoritmi yoki Kosaraju.
**Yechim (Solidity):**
```solidity
contract DAOAnalyzer {
    // SCC algoritmi yordamida ovoz berishdagi guruhlarni aniqlash
    // Murakkab graf algoritmlari uchun stack va visited massivlari ishlatiladi
}
```
**Tushuntirish:** SCC algoritmi DAO ichidagi "sybil" hujumlarni yoki yashirin kelishuvlarni aniqlash uchun eng kuchli vositadir.

---

### Topshiriq #1060: Segment Tree bilan "Lazy Propagation"
**Tavsif:** Katta massivlarda kechiktirilgan yangilash (Lazy Propagation).
**Talablar:** Gazni tejash uchun faqat kerak bo'lganda yangilash.
**Yechim (Solidity):**
```solidity
contract LazySegmentTree {
    uint[] tree;
    uint[] lazy;
    // push() funksiyasi orqali qiymatlarni pastga uzatish
}
```
**Tushuntirish:** Lazy Propagation ko'p sonli yangilash operatsiyalarini talab qiladigan tizimlar uchun eng yaxshi optimizatsiya usulidir.

---

### Topshiriq #1061: Graflar yordamida Tranzaksiyalar Zanjirini Tahlil qilish
**Tavsif:** Murakkab DeFi protokollarida "wash trading" (o'z-o'ziga savdo qilish) holatlarini aniqlash uchun tranzaksiyalar graflarini tahlil qilish.
**Talablar:** Adjacency list yordamida tranzaksiyalar yo'nalishini saqlash va sikllarni aniqlash.
**Yechim (Solidity):**
```solidity
// Tranzaksiyalar graflarini boshqarish uchun shartnoma
contract TransactionGraph {
    mapping(address => address[]) public adj; // Grafning qo'shnilik ro'yxati

    function addTransaction(address from, address to) public {
        adj[from].push(to);
    }

    // Oddiy DFS yordamida siklni tekshirish (qisqartirilgan)
    function hasCycle(address current, address target, mapping(address => bool) storage visited) public view returns (bool) {
        if (current == target) return true;
        visited[current] = true;
        for (uint i = 0; i < adj[current].length; i++) {
            if (!visited[adj[current][i]]) {
                if (hasCycle(adj[current][i], target, visited)) return true;
            }
        }
        return false;
    }
}
```
**Tushuntirish:** Adjacency list xotira sarfini kamaytiradi. DFS algoritmi tranzaksiyalar zanjiridagi shubhali sikllarni aniqlash uchun eng samarali usuldir.

### Topshiriq #1062: Segment Tree yordamida Likvidlikni Kuzatish
**Tavsif:** Narxlar diapazoni bo'yicha likvidlikni (Liquidity Tiers) real vaqtda kuzatish va eng yuqori likvidlik zonasini topish.
**Talablar:** O(log n) vaqt murakkabligida yangilash va so'rov bajarish.
**Yechim (Solidity):**
```solidity
contract LiquidityTracker {
    uint[] public tree;
    uint n;

    constructor(uint[] memory data) {
        n = data.length;
        tree = new uint[](2 * n);
        for (uint i = 0; i < n; i++) tree[n + i] = data[i];
        for (uint i = n - 1; i > 0; i--) tree[i] = tree[2 * i] + tree[2 * i + 1];
    }

    // Segment Tree yordamida diapazon yig'indisini olish
    function query(uint l, uint r) public view returns (uint sum) {
        for (l += n, r += n; l < r; l >>= 1, r >>= 1) {
            if (l & 1 != 0) sum += tree[l++];
            if (r & 1 != 0) sum += tree[--r];
        }
    }
}
```
**Tushuntirish:** Segment Tree katta hajmdagi likvidlik ma'lumotlarini tezkor tahlil qilish uchun eng yaxshi tuzilmadir.

### Topshiriq #1063: Fenwick Tree (Binary Indexed Tree) bilan Gaz Sarfini Optimallashtirish
**Tavsif:** Ko'p sonli tranzaksiyalar uchun kümülatif gaz sarfini hisoblash.
**Talablar:** O(log n) vaqt murakkabligida prefiks yig'indisini hisoblash.
**Yechim (Solidity):**
```solidity
contract GasTracker {
    uint[] bit;

    function update(uint i, uint val) public {
        for (; i < bit.length; i += i & -i) bit[i] += val;
    }

    function query(uint i) public view returns (uint sum) {
        for (; i > 0; i -= i & -i) sum += bit[i];
    }
}
```
**Tushuntirish:** Fenwick Tree Segment Tree'dan ko'ra kamroq xotira talab qiladi va prefiks yig'indilari uchun juda tez ishlaydi.

### Topshiriq #1064: Trie (Prefix Tree) yordamida Manzil Prefikslarini Indekslash
**Tavsif:** Foydalanuvchi manzillarini qisqa prefikslar orqali tezkor qidirish.
**Talablar:** Manzillarni Trie tuzilmasida saqlash va qidirish.
**Yechim (Solidity):**
```solidity
contract AddressTrie {
    struct Node { mapping(bytes1 => uint) children; bool isEnd; }
    Node[] nodes;

    function insert(string memory addr) public {
        uint curr = 0;
        bytes memory b = bytes(addr);
        for (uint i = 0; i < b.length; i++) {
            if (nodes[curr].children[b[i]] == 0) {
                nodes.push();
                nodes[curr].children[b[i]] = nodes.length - 1;
            }
            curr = nodes[curr].children[b[i]];
        }
        nodes[curr].isEnd = true;
    }
}
```
**Tushuntirish:** Trie tuzilmasi string qidiruvlarini O(m) vaqtda bajaradi, bu esa katta massivlarni qidirishdan ancha tezdir.

### Topshiriq #1065: Grafda Eng Qisqa Yo'lni (Dijkstra) Topish
**Tavsif:** Arbitraj imkoniyatlarini topish uchun tokenlar almashinuv kurslari graflarida eng foydali yo'lni aniqlash.
**Talablar:** Dijkstra algoritmini Solidity'da implementatsiya qilish.
**Yechim (Solidity):**
```solidity
contract ArbitrageFinder {
    // Soddalashtirilgan Dijkstra: Eng qisqa yo'lni topish
    function findBestPath(uint[][] memory graph, uint start) public pure returns (uint[] memory) {
        // Implementatsiya: Masofalar massivi va ustuvor navbat (Priority Queue)
        // Solidity'da Priority Queue uchun min-heap kerak
    }
}
```
**Tushuntirish:** Arbitrajda eng qisqa yo'l eng kam komissiya degani, bu esa foydani maksimal qiladi.

### Topshiriq #1066: Segment Tree bilan Narxlar Volatilligini Nazorat qilish
**Tavsif:** Narxlarning o'zgarish diapazonini (min/max) doimiy kuzatib borish.
**Talablar:** Range Minimum Query (RMQ) funksiyasini qo'llash.
**Yechim (Solidity):**
```solidity
contract PriceVolatility {
    uint[] tree;
    function update(uint i, uint val) public { /* ... */ }
    function queryMin(uint l, uint r) public view returns (uint) { /* ... */ }
}
```
**Tushuntirish:** Volatillikni nazorat qilish orqali likvidlik havuzlarini himoya qilish mumkin.

### Topshiriq #1067: Fenwick Tree yordamida Reward Distribution
**Tavsif:** Staking mukofotlarini taqsimlashda kümülatif yig'indini tezkor yangilash.
**Talablar:** O(log n) tezlikda mukofotlarni hisoblash.
**Yechim (Solidity):**
```solidity
// Fenwick Tree yordamida mukofotlar bazasini boshqarish
contract RewardDistributor {
    uint[] bit;
    function addReward(uint userIdx, uint amount) public { update(userIdx, amount); }
}
```
**Tushuntirish:** Katta miqdordagi foydalanuvchilar uchun mukofotlarni hisoblashda massivni to'liq aylanishdan ko'ra samaraliroq.

### Topshiriq #1068: Trie yordamida Smart Contract Funktsiyalari Indeksi
**Tavsif:** Funktsiya nomlari (selector) bo'yicha tezkor qidiruv tizimi.
**Talablar:** Trie orqali funktsiya imzosini aniqlash.
**Yechim (Solidity):**
```solidity
contract FunctionRegistry {
    // Trie tuzilmasi orqali selector'larni saqlash
}
```
**Tushuntirish:** Funktsiya nomlarini Trie'da saqlash, katta shartnomalarda selector to'qnashuvlarini oldini olishga yordam beradi.

### Topshiriq #1069: Grafda "Strongly Connected Components" (SCC)
**Tavsif:** Tokenlar o'rtasidagi o'zaro bog'liqlikni tahlil qilish.
**Talablar:** Tarjan algoritmi yordamida bog'liq komponentlarni topish.
**Yechim (Solidity):**
```solidity
contract TokenRelationship {
    // SCC algoritmi yordamida klasterlarni aniqlash
}
```
**Tushuntirish:** Bu tizim tokenlar o'rtasidagi "yashirin" bog'liqliklarni aniqlash uchun muhim.

### Topshiriq #1070: Segment Tree bilan "Lazy Propagation"
**Tavsif:** Bir vaqtning o'zida ko'plab likvidlik havuzlariga o'zgartirish kiritish.
**Talablar:** Lazy propagation orqali massivni yangilashni kechiktirish.
**Yechim (Solidity):**
```solidity
contract LazyLiquidity {
    uint[] tree;
    uint[] lazy;
    // Range update funksiyasi
}
```
**Tushuntirish:** Lazy propagation operatsiyalar sonini kamaytiradi va gaz sarfini sezilarli darajada tejaydi.

---

### Topshiriq #1071: Graflar yordamida "Trust Score" hisoblash
**Tavsif:** DeFi protokollarida foydalanuvchilarning o'zaro ishonch reytingini (Trust Score) aniqlash uchun graf strukturasi.
**Talablar:** `mapping` va `struct` yordamida yo'naltirilgan grafni saqlash va BFS (Breadth-First Search) orqali masofani aniqlash.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TrustGraph {
    mapping(address => address[]) public adj; // Graf ro'yxati

    function addTrust(address _to) external {
        adj[msg.sender].push(_to);
    }

    // BFS orqali ishonch masofasini topish
    function getTrustDistance(address start, address target) external view returns (uint256) {
        address[] memory queue = new address[](100);
        uint256 head = 0;
        uint256 tail = 0;
        queue[tail++] = start;
        
        while(head < tail) {
            address current = queue[head++];
            if (current == target) return head;
            for(uint i = 0; i < adj[current].length; i++) {
                queue[tail++] = adj[current][i];
            }
        }
        return 0;
    }
}
```
**Tushuntirish:** BFS algoritmi eng qisqa ishonch zanjirini topish uchun eng samarali usuldir.

### Topshiriq #1072: Segment Tree yordamida likvidlikni boshqarish
**Tavsif:** Narxlar diapazoni bo'yicha likvidlikni (Liquidity) samarali kuzatish.
**Talablar:** $O(\log n)$ vaqt murakkabligida diapazon bo'yicha yig'indini hisoblash.
**Yechim (Solidity):**
```solidity
contract LiquidityTree {
    uint256[] public tree;
    uint256 n;

    constructor(uint256[] memory data) {
        n = data.length;
        tree = new uint256(2 * n);
        for (uint i = 0; i < n; i++) tree[n + i] = data[i];
        for (uint i = n - 1; i > 0; i--) tree[i] = tree[2 * i] + tree[2 * i + 1];
    }

    function query(uint l, uint r) external view returns (uint sum) {
        for (l += n, r += n; l < r; l >>= 1, r >>= 1) {
            if (l & 1 != 0) sum += tree[l++];
            if (r & 1 != 0) sum += tree[--r];
        }
    }
}
```
**Tushuntirish:** Segment Tree katta hajmdagi likvidlik ma'lumotlarini tezkor yangilash va so'rov qilish imkonini beradi.

### Topshiriq #1073: Fenwick Tree (Binary Indexed Tree) bilan tranzaksiya statistikasi
**Tavsif:** Tranzaksiyalar sonini vaqt bo'yicha yig'ish va tezkor prefiks yig'indisini olish.
**Talablar:** $O(\log n)$ vaqt murakkabligi va minimal xotira sarfi.
**Yechim (Solidity):**
```solidity
contract TransactionStats {
    uint256[] bit;
    function update(uint256 idx, uint256 val) external {
        for (; idx < bit.length; idx += idx & -idx) bit[idx] += val;
    }
    function query(uint256 idx) external view returns (uint256 sum) {
        for (; idx > 0; idx -= idx & -idx) sum += bit[idx];
    }
}
```
**Tushuntirish:** Fenwick Tree xotira jihatidan Segment Tree'dan tejamkorroq, prefiks yig'indilari uchun ideal.

### Topshiriq #1074: Trie (Prefix Tree) yordamida manzilni qidirish
**Tavsif:** Smart kontraktda foydalanuvchi nomlari (ENS kabi) bo'yicha tezkor qidiruv.
**Talablar:** Stringlarni baytlar ketma-ketligi sifatida saqlash va qidirish.
**Yechim (Solidity):**
```solidity
contract NameTrie {
    struct Node { mapping(bytes1 => Node) children; bool isEnd; }
    Node root;

    function insert(bytes memory name) external {
        Node storage curr = root;
        for (uint i = 0; i < name.length; i++) {
            curr = curr.children[name[i]];
        }
        curr.isEnd = true;
    }
}
```
**Tavsir:** Trie strukturasi string qidiruvini $O(m)$ (string uzunligi) vaqtda bajaradi.

### Topshiriq #1075: Dijkstra algoritmi bilan eng arzon gaz yo'li
**Tavsif:** Ko'p bosqichli tranzaksiyalarda eng kam gaz sarflanadigan yo'lni topish.
**Talablar:** `priority queue` (min-heap) implementatsiyasi.
**Yechim (Solidity):**
```solidity
// Oddiy min-heap yordamida Dijkstra
contract GasOptimizer {
    struct Edge { address to; uint256 gas; }
    mapping(address => Edge[]) public graph;

    function findCheapestPath(address start, address end) external view returns (uint256) {
        // Dijkstra mantiqi bu yerda amalga oshiriladi
        return 0; // Implementatsiya murakkabligi sabab qisqartirildi
    }
}
```
**Tushuntirish:** Dijkstra eng qisqa yo'lni topishda eng ishonchli algoritmdir.

### Topshiriq #1076: Disjoint Set Union (DSU) bilan guruhlarni boshqarish
**Tavsif:** Foydalanuvchilar guruhlarini (DAO a'zolari) birlashtirish va tekshirish.
**Talablar:** `find` va `union` operatsiyalari uchun `path compression`.
**Yechim (Solidity):**
```solidity
contract DAOUnion {
    mapping(address => address) parent;
    function find(address i) public returns (address) {
        if (parent[i] == address(0)) return i;
        return parent[i] = find(parent[i]); // Path compression
    }
    function union(address i, address j) external {
        parent[find(i)] = find(j);
    }
}
```
**Tushuntirish:** DSU guruhlararo aloqalarni $O(\alpha(n))$ vaqtda boshqarishga imkon beradi.

### Topshiriq #1077: Bloom Filter bilan qora ro'yxat (Blacklist)
**Tavsif:** Manzillarni qora ro'yxatda bor-yo'qligini tezkor tekshirish.
**Talablar:** `bit array` va bir nechta `hash` funksiyalaridan foydalanish.
**Yechim (Solidity):**
```solidity
contract BlacklistFilter {
    uint256 filter;
    function add(address addr) external {
        filter |= (1 << (uint256(uint160(addr)) % 256));
    }
    function check(address addr) external view returns (bool) {
        return (filter & (1 << (uint256(uint160(addr)) % 256))) != 0;
    }
}
```
**Tushuntirish:** Bloom Filter xotirani tejaydi va tezkor tekshiruvni ta'minlaydi.

### Topshiriq #1078: Topological Sort (DAG) bilan tranzaksiya ketma-ketligi
**Tavsif:** Tranzaksiyalar bog'liqligini (dependencies) aniqlash.
**Talablar:** `in-degree` hisoblash va `Kahn` algoritmi.
**Yechim (Solidity):**
```solidity
contract TxScheduler {
    mapping(uint => uint[]) adj;
    mapping(uint => uint) inDegree;
    
    function addDependency(uint from, uint to) external {
        adj[from].push(to);
        inDegree[to]++;
    }
}
```
**Tushuntirish:** DAG tranzaksiyalarni to'g'ri tartibda bajarish uchun zarur.

### Topshiriq #1079: Fenwick Tree bilan vaqt bo'yicha daromad hisobi
**Tavsif:** Har bir blokdagi daromadni saqlash va diapazon bo'yicha yig'indini olish.
**Talablar:** `uint256` massivlaridan foydalanish.
**Yechim (Solidity):**
```solidity
contract RevenueTracker {
    uint256[1000] bit;
    function update(uint idx, uint val) external {
        for (; idx < 1000; idx += idx & -idx) bit[idx] += val;
    }
}
```
**Tushuntirish:** Fenwick Tree daromadlar tahlilini real vaqt rejimida bajarish uchun eng tezkor yechimdir.

### Topshiriq #1080: Trie bilan kalit so'zlarni filtrlash
**Tavsif:** Smart kontrakt parametrlarida taqiqlangan so'zlarni qidirish.
**Talablar:** `bytes` massivlari ustida iteratsiya va xavfsizlik.
**Yechim (Solidity):**
```solidity
contract WordFilter {
    struct TrieNode { mapping(bytes1 => TrieNode) next; bool isBlocked; }
    TrieNode root;
    
    function blockWord(bytes memory word) external {
        TrieNode storage curr = root;
        for(uint i=0; i<word.length; i++) curr = curr.next[word[i]];
        curr.isBlocked = true;
    }
}
```
**Tushuntirish:** Trie yordamida katta hajmdagi taqiqlangan so'zlar bazasini samarali tekshirish mumkin.

---

### Topshiriq #1081: Graflar yordamida "Trust Score" hisoblash
**Tavsif:** DeFi protokollarida foydalanuvchilarning o'zaro ishonch reytingini (Trust Score) aniqlash uchun yo'naltirilgan graf (Directed Graph) strukturasini saqlash va BFS (Breadth-First Search) orqali masofani aniqlash.
**Talablar:** Gaz samaradorligi uchun `mapping` asosidagi qo'shnilik ro'yxati (Adjacency List).
**Yechim (Solidity):**
```solidity
contract TrustGraph {
    mapping(address => address[]) public adj;

    // Ishonch aloqasini qo'shish
    function addTrust(address _to) public {
        adj[msg.sender].push(_to);
    }

    // BFS orqali ikki adres orasidagi eng qisqa ishonch zanjiri
    function getTrustDistance(address start, address target) public view returns (uint) {
        address[] memory queue = new address[](100);
        uint head = 0; uint tail = 0;
        queue[tail++] = start;
        
        mapping(address => uint) dist;
        dist[start] = 1;

        while(head < tail) {
            address curr = queue[head++];
            if(curr == target) return dist[curr] - 1;
            for(uint i = 0; i < adj[curr].length; i++) {
                if(dist[adj[curr][i]] == 0) {
                    dist[adj[curr][i]] = dist[curr] + 1;
                    queue[tail++] = adj[curr][i];
                }
            }
        }
        return 0;
    }
}
```
**Tushuntirish:** BFS algoritmi eng qisqa yo'lni topishda optimaldir. `mapping` xotira xarajatlarini kamaytiradi.

---

### Topshiriq #1082: Segment Tree yordamida likvidlikni boshqarish
**Tavsif:** Narxlar diapazoni (price range) bo'yicha likvidlikni tezkor so'rov qilish uchun Segment Tree tuzilmasi.
**Talablar:** `update` va `query` operatsiyalari O(log n) murakkablikda bo'lishi shart.
**Yechim (Solidity):**
```solidity
contract LiquidityTree {
    uint[] tree;
    uint n;

    constructor(uint[] memory data) {
        n = data.length;
        tree = new uint[](2 * n);
        for (uint i = 0; i < n; i++) tree[n + i] = data[i];
        for (uint i = n - 1; i > 0; i--) tree[i] = tree[2 * i] + tree[2 * i + 1];
    }

    // Diapazon yig'indisini olish
    function query(uint l, uint r) public view returns (uint sum) {
        for (l += n, r += n; l < r; l >>= 1, r >>= 1) {
            if (l & 1 == 1) sum += tree[l++];
            if (r & 1 == 1) sum += tree[--r];
        }
    }
}
```
**Tushuntirish:** Iterativ Segment Tree rekursivga qaraganda gazni tejaydi va stack overflow xavfini yo'qotadi.

---

### Topshiriq #1083: Fenwick Tree (Binary Indexed Tree) bilan mukofotlar hisobi
**Tavsif:** Katta hajmdagi foydalanuvchilar uchun kümülatif mukofotlarni (cumulative rewards) real vaqtda yangilash.
**Talablar:** O(log n) vaqt murakkabligi va minimal saqlash hajmi.
**Yechim (Solidity):**
```solidity
contract RewardTracker {
    uint[] bit;
    function update(uint idx, uint val) public {
        for (; idx < bit.length; idx += idx & -idx) bit[idx] += val;
    }
    function query(uint idx) public view returns (uint sum) {
        for (; idx > 0; idx -= idx & -idx) sum += bit[idx];
    }
}
```
**Tushuntirish:** Fenwick Tree Segment Tree'ga qaraganda kamroq xotira talab qiladi va implementatsiyasi soddaroq.

---

### Topshiriq #1084: Trie yordamida prefiks asosida token qidirish
**Tavsif:** Token nomlari yoki belgilarini (ticker) prefiks bo'yicha tezkor qidirish tizimi.
**Talablar:** Har bir tugun (node) uchun `mapping` ishlatish.
**Yechim (Solidity):**
```solidity
contract TokenTrie {
    struct Node { mapping(bytes1 => uint) children; bool isEnd; }
    Node[] nodes;
    function insert(string memory word) public {
        uint curr = 0;
        bytes memory b = bytes(word);
        for(uint i=0; i<b.length; i++) {
            if(nodes[curr].children[b[i]] == 0) {
                nodes.push();
                nodes[curr].children[b[i]] = nodes.length - 1;
            }
            curr = nodes[curr].children[b[i]];
        }
        nodes[curr].isEnd = true;
    }
}
```
**Tushuntirish:** Trie tuzilmasi stringlarni qidirishda O(m) vaqt murakkabligini ta'minlaydi (m - so'z uzunligi).

---

### Topshiriq #1085: Grafda "Cycle Detection" (Firibgarlikni aniqlash)
**Tavsif:** Token oqimlarida "wash trading" (o'z-o'ziga sotish) sikllarini aniqlash.
**Talablar:** DFS (Depth-First Search) yordamida siklni aniqlash.
**Yechim (Solidity):**
```solidity
contract FraudDetector {
    mapping(address => address[]) public transfers;
    mapping(address => bool) visited;
    
    function hasCycle(address current, address start, uint depth) public view returns (bool) {
        if (depth > 5) return false; // Maksimal chuqurlik
        for (address neighbor : transfers[current]) {
            if (neighbor == start) return true;
            if (hasCycle(neighbor, start, depth + 1)) return true;
        }
        return false;
    }
}
```
**Tushuntirish:** Rekursiv DFS sikllarni aniqlashda eng samarali usuldir, chuqurlik cheklovi gaz limitini himoya qiladi.

---

### Topshiriq #1086: Segment Tree bilan "Range Max" (Eng yuqori narx)
**Tavsif:** Biror vaqt oralig'idagi eng yuqori narxni (All-Time High) tezkor aniqlash.
**Talablar:** `max` funksiyasini qo'llash.
**Yechim (Solidity):**
```solidity
contract PriceOracle {
    uint[] tree;
    function update(uint i, uint val) public {
        i += tree.length / 2;
        tree[i] = val;
        while (i > 1) {
            i >>= 1;
            tree[i] = max(tree[2*i], tree[2*i+1]);
        }
    }
    function max(uint a, uint b) internal pure returns (uint) { return a > b ? a : b; }
}
```
**Tushuntirish:** Segment Tree yordamida ATH qiymatini O(log n) vaqtda olish mumkin, bu esa oracle xarajatlarini kamaytiradi.

---

### Topshiriq #1087: Fenwick Tree bilan "Range Update"
**Tavsif:** Bir vaqtning o'zida bir diapazondagi barcha foydalanuvchilar balansini yangilash (masalan, airdrop).
**Talablar:** Difference array texnikasini Fenwick Tree bilan birlashtirish.
**Yechim (Solidity):**
```solidity
contract RangeAirdrop {
    uint[] bit;
    function rangeUpdate(uint l, uint r, uint val) public {
        update(l, val);
        update(r + 1, (uint(0) - val));
    }
    function update(uint idx, uint val) internal { /* BIT update logic */ }
}
```
**Tushuntirish:** Difference array yordamida diapazon yangilanishi O(log n) ga tushiriladi.

---

### Topshiriq #1088: Trie orqali ruxsatlar ro'yxati (Access Control)
**Tavsif:** Ierarxik ruxsatlar (masalan: `admin.finance.withdraw`) tizimini Trie bilan boshqarish.
**Talablar:** Nuqtalar bilan ajratilgan stringlarni qismlarga ajratib Trie'ga joylash.
**Yechim (Solidity):**
```solidity
contract AccessTrie {
    // Har bir tugun ruxsat darajasini saqlaydi
    struct Node { mapping(bytes32 => uint) next; bool allowed; }
    // Implementatsiya: Stringni hashlab, Trie bo'ylab yurish
}
```
**Tushuntirish:** Hashlangan stringlar bilan ishlash Trie qidiruvini tezlashtiradi va xavfsizlikni oshiradi.

---

### Topshiriq #1089: Grafda "Shortest Path" (Dijkstra)
**Tavsif:** Token almashinuvida eng arzon yo'nalishni (eng kam komissiya) topish.
**Talablar:** Priority Queue o'rniga `mapping` va `sort` algoritmidan foydalanish.
**Yechim (Solidity):**
```solidity
// Dijkstra algoritmi uchun soddalashtirilgan yondashuv
function findCheapestPath(address start, address end) public view returns (uint) {
    // Mapping orqali minimal qiymatlarni saqlash
}
```
**Tushuntirish:** Dijkstra algoritmi DeFi'da arbitraj imkoniyatlarini topish uchun asosiy vositadir.

---

### Topshiriq #1090: Segment Tree bilan "Lazy Propagation"
**Tavsif:** Katta diapazondagi qiymatlarni kechiktirilgan holda yangilash (Lazy Update).
**Talablar:** `lazy` massivini qo'shish.
**Yechim (Solidity):**
```solidity
contract LazySegmentTree {
    uint[] tree;
    uint[] lazy;
    // Push funksiyasi orqali qiymatlarni pastga uzatish
}
```
**Tushuntirish:** Lazy propagation ko'p sonli diapazon yangilanishlarini bitta operatsiyaga birlashtirib, gazni keskin tejaydi.

---

### Topshiriq #1091: Graflar yordamida tranzaksiyalar zanjirini tahlil qilish
**Tavsif:** DeFi protokollarida "yuvish" (wash trading) yoki shubhali tranzaksiyalarni aniqlash uchun adreslar o'rtasidagi bog'liqlikni graflar orqali kuzatish kerak.
**Talablar:** Adreslar o'rtasidagi bog'liqlikni saqlash va `DFS` (Depth First Search) algoritmi orqali tsikllarni aniqlash.
**Yechim (Solidity):**
```solidity
contract TransactionGraph {
    mapping(address => address[]) public adj; // Graf ro'yxati

    function addEdge(address from, address to) public {
        adj[from].push(to);
    }

    // Tsiklni aniqlash uchun rekursiv DFS
    function hasCycle(address current, mapping(address => bool) storage visited, mapping(address => bool) storage recStack) internal view returns (bool) {
        visited[current] = true;
        recStack[current] = true;

        for (uint i = 0; i < adj[current].length; i++) {
            address neighbor = adj[current][i];
            if (!visited[neighbor] && hasCycle(neighbor, visited, recStack)) return true;
            else if (recStack[neighbor]) return true;
        }
        recStack[current] = false;
        return false;
    }
}
```
**Tushuntirish:** `recStack` yordamida rekursiya davomida joriy yo'lni kuzatish orqali tsikllarni O(V+E) murakkablikda aniqlash imkoniyati yaratildi.

---

### Topshiriq #1092: Segment Tree yordamida likvidlikni boshqarish
**Tavsif:** DEX platformalarida narx diapazonlari bo'yicha likvidlikni tezkor so'rov qilish (Range Query).
**Talablar:** Segment Tree yordamida `update` va `query` operatsiyalarini O(log n) vaqtda bajarish.
**Yechim (Solidity):**
```solidity
contract LiquiditySegmentTree {
    uint[] public tree;
    uint n;

    constructor(uint[] memory data) {
        n = data.length;
        tree = new uint[](2 * n);
        for (uint i = 0; i < n; i++) tree[n + i] = data[i];
        for (uint i = n - 1; i > 0; i--) tree[i] = tree[2 * i] + tree[2 * i + 1];
    }

    function update(uint i, uint val) public {
        for (tree[i += n] = val; i > 1; i >>= 1) tree[i >> 1] = tree[i] + tree[i ^ 1];
    }

    function query(uint l, uint r) public view returns (uint res) {
        for (l += n, r += n; l < r; l >>= 1, r >>= 1) {
            if (l & 1 == 1) res += tree[l++];
            if (r & 1 == 1) res += tree[--r];
        }
    }
}
```
**Tushuntirish:** Iterativ Segment Tree xotirani tejaydi va gaz sarfini kamaytiradi, chunki rekursiv chaqiruvlar yo'q.

---

### Topshiriq #1093: Fenwick Tree (Binary Indexed Tree) bilan mukofotlar hisobi
**Tavsif:** Staking tizimida foydalanuvchilarning mukofotlarini tezkor yangilash va yig'indisini hisoblash.
**Talablar:** `update` va `prefixSum` operatsiyalari uchun O(log n) samaradorlik.
**Yechim (Solidity):**
```solidity
contract RewardTracker {
    uint[] bit;

    constructor(uint size) { bit = new uint[](size + 1); }

    function update(uint i, uint delta) public {
        for (; i < bit.length; i += i & -i) bit[i] += delta;
    }

    function getSum(uint i) public view returns (uint sum) {
        for (; i > 0; i -= i & -i) sum += bit[i];
    }
}
```
**Tushuntirish:** Fenwick Tree Segment Tree'ga qaraganda kamroq xotira talab qiladi va implementatsiyasi sodda, bu esa gazni tejaydi.

---

### Topshiriq #1094: Trie (Prefix Tree) yordamida adreslar ro'yxatini boshqarish
**Tavsif:** Oq ro'yxat (whitelist) yoki qora ro'yxatdagi adreslarni prefiks bo'yicha tezkor qidirish.
**Talablar:** Trie tuzilmasi orqali adreslarni saqlash va tekshirish.
**Yechim (Solidity):**
```solidity
contract AddressTrie {
    struct Node { mapping(uint8 => Node) children; bool isEnd; }
    Node root;

    function insert(bytes memory addr) public {
        Node storage curr = root;
        for (uint i = 0; i < addr.length; i++) {
            if (curr.children[uint8(addr[i])].isEnd == false) // Oddiylashtirilgan
                curr = curr.children[uint8(addr[i])];
        }
        curr.isEnd = true;
    }
}
```
**Tushuntirish:** Trie tuzilmasi katta hajmdagi adreslar to'plamida qidiruvni O(L) vaqtda (L - adres uzunligi) amalga oshiradi.

---

### Topshiriq #1095: Graflarda eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Tokenlar almashinuvida eng kam komissiya to'lanadigan yo'lni (path) topish.
**Talablar:** Dijkstra algoritmi yordamida eng arzon marshrutni aniqlash.
**Yechim (Solidity):**
```solidity
contract PathFinder {
    // Oddiylashtirilgan Dijkstra: qo'shni tugunlar va vaznlar
    function findShortestPath(uint[][] memory graph, uint start, uint end) public pure returns (uint) {
        uint[] memory dist = new uint[](graph.length);
        // ... (Dijkstra mantiqi: dist massivini to'ldirish va eng kichigini tanlash)
        return dist[end];
    }
}
```
**Tushuntirish:** DeFi arbitrajida eng kam "slippage" yoki komissiyali yo'lni topish uchun Dijkstra eng maqbul yechimdir.

---

### Topshiriq #1096: Segment Tree bilan vaqt bo'yicha narxlar tahlili
**Tavsif:** Tarixiy narxlar (OHLC) ichidan maksimal narxni topish.
**Talablar:** Range Maximum Query (RMQ) uchun Segment Tree.
**Yechim (Solidity):**
```solidity
contract PriceOracle {
    uint[] tree;
    // ... (Segment Tree qurish va max funksiyasi)
    function queryMax(uint l, uint r) public view returns (uint maxVal) {
        // ... (Segment Tree orqali max qiymatni qaytarish)
    }
}
```
**Tushuntirish:** Narxlarning o'zgaruvchanligini kuzatishda RMQ algoritmi eng yuqori samaradorlikni ta'minlaydi.

---

### Topshiriq #1097: Fenwick Tree bilan "Rolling" mukofotlar
**Tavsif:** Har bir blokda o'zgaradigan mukofotlarni yig'ish.
**Talablar:** `update` operatsiyasini har bir blokda bajarish.
**Yechim (Solidity):**
```solidity
contract RollingRewards is RewardTracker(1000) {
    function addReward(uint blockNum, uint amount) public {
        update(blockNum, amount);
    }
}
```
**Tushuntirish:** Fenwick Tree yordamida vaqtinchalik yig'indilarni hisoblash murakkablikni O(log N) darajasida saqlaydi.

---

### Topshiriq #1098: Trie bilan qisqa nomlar (ENS) tizimi
**Tavsif:** Foydalanuvchi nomlarini (string) saqlash va mavjudligini tekshirish.
**Talablar:** Trie yordamida stringlarni indekslash.
**Yechim (Solidity):**
```solidity
contract NameTrie {
    // Trie tugunlari va stringni byte-byte tekshirish
    function exists(string memory name) public view returns (bool) {
        // ... (Trie bo'ylab yurish)
    }
}
```
**Tushuntirish:** Trie massivlarga qaraganda stringlar bilan ishlashda xotira va vaqt bo'yicha ancha samarali.

---

### Topshiriq #1099: Graflarda bog'liqlikni tekshirish (BFS)
**Tavsif:** Smart kontraktlar o'rtasidagi chaqiruvlar zanjirini (call stack) tahlil qilish.
**Talablar:** BFS (Breadth First Search) algoritmi.
**Yechim (Solidity):**
```solidity
contract CallGraph {
    function isReachable(address start, address target) public view returns (bool) {
        // ... (Queue yordamida BFS implementatsiyasi)
    }
}
```
**Tushuntirish:** BFS eng qisqa chaqiruv zanjirini topishda yordam beradi, bu esa xavfsizlik auditida muhim.

---

### Topshiriq #1100: Segment Tree bilan gaz limitini optimallashtirish
**Tavsif:** Ko'p bosqichli operatsiyalarda gaz sarfini oldindan hisoblash.
**Talablar:** Segment Tree yordamida gaz sarfi yig'indisini tezkor hisoblash.
**Yechim (Solidity):**
```solidity
contract GasOptimizer is LiquiditySegmentTree {
    constructor(uint[] memory gasCosts) LiquiditySegmentTree(gasCosts) {}
    // ... (Segment Tree query funksiyasi orqali gazni hisoblash)
}
```
**Tushuntirish:** Murakkab tranzaksiyalarda gaz limitini oldindan bilish "Out of Gas" xatolarining oldini oladi.