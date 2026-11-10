# Khorazmiy AI: Swift - Modul 22
## Mavzu: Ilg'or Algoritmlar: Graflar, Segment Trees, Fenwick va Trie tuzilmalari

### Topshiriq #1051: Tarmoq Kechikishini Minimallashtirish (Dijkstra)
**Tavsif:** Katta hajmdagi ma'lumotlar markazlari o'rtasidagi eng qisqa yo'lni topish.
**Talablar:** O(E log V) murakkablik, xotira xavfsizligi.
**Yechim (Swift):**
```swift
import Foundation

struct Edge { let to: Int; let weight: Int }

func findShortestPath(n: Int, graph: [[Edge]], start: Int) -> [Int] {
    var distances = Array(repeating: Int.max, count: n)
    distances[start] = 0
    var pq = [(0, start)] // Oddiy navbat, ishlab chiqarishda PriorityQueue ishlatiladi
    
    while !pq.isEmpty {
        pq.sort { $0.0 < $1.0 }
        let (d, u) = pq.removeFirst()
        if d > distances[u] { continue }
        for edge in graph[u] {
            if distances[u] + edge.weight < distances[edge.to] {
                distances[edge.to] = distances[u] + edge.weight
                pq.append((distances[edge.to], edge.to))
            }
        }
    }
    return distances
}
```
**Tushuntirish:** Dijkstra algoritmi tarmoq topologiyasida paketlar yo'nalishini optimallashtirish uchun eng ishonchli yondashuvdir.

### Topshiriq #1052: Real-time Statistik Yangilanish (Fenwick Tree)
**Tavsif:** Foydalanuvchi faolligini doimiy kuzatish va oraliq yig'indilarni hisoblash.
**Talablar:** O(log N) yangilanish va so'rov vaqti.
**Yechim (Swift):**
```swift
class FenwickTree {
    private var tree: [Int]
    init(size: Int) { tree = Array(repeating: 0, count: size + 1) }
    
    func update(index: Int, delta: Int) {
        var i = index + 1
        while i < tree.count { tree[i] += delta; i += i & -i }
    }
    
    func query(index: Int) -> Int {
        var i = index + 1, sum = 0
        while i > 0 { sum += tree[i]; i -= i & -i }
        return sum
    }
}
```
**Tushuntirish:** Fenwick Tree (Binary Indexed Tree) xotira tejamkorligi va tezligi tufayli real vaqt rejimida analitika uchun ideal.

### Topshiriq #1053: Dinamik Oraliq So'rovlari (Segment Tree)
**Tavsif:** Katta massivdagi ma'lumotlar uchun diapazon bo'yicha maksimum qiymatni topish.
**Talablar:** O(log N) murakkablik, thread-safe yondashuv.
**Yechim (Swift):**
```swift
class SegmentTree {
    private var tree: [Int]
    private let n: Int
    init(data: [Int]) {
        n = data.count
        tree = Array(repeating: 0, count: 2 * n)
        for i in 0..<n { tree[n + i] = data[i] }
        for i in stride(from: n - 1, through: 1, by: -1) { tree[i] = max(tree[2*i], tree[2*i+1]) }
    }
    func query(l: Int, r: Int) -> Int {
        var res = 0, left = l + n, right = r + n
        while left < right {
            if left % 2 == 1 { res = max(res, tree[left]); left += 1 }
            if right % 2 == 1 { right -= 1; res = max(res, tree[right]) }
            left /= 2; right /= 2
        }
        return res
    }
}
```
**Tushuntirish:** Segment Tree o'zgaruvchan ma'lumotlar to'plamida tezkor diapazon so'rovlarini bajarishga imkon beradi.

### Topshiriq #1054: Avtomatik To'ldirish Tizimi (Trie)
**Tavsif:** Lug'at bazasidan so'zlarni tezkor izlash va taklif qilish.
**Talablar:** O(L) qidiruv vaqti, bu yerda L - so'z uzunligi.
**Yechim (Swift):**
```swift
class TrieNode {
    var children: [Character: TrieNode] = [:]
    var isEndOfWord = false
}

class Trie {
    let root = TrieNode()
    func insert(_ word: String) {
        var curr = root
        for char in word {
            if curr.children[char] == nil { curr.children[char] = TrieNode() }
            curr = curr.children[char]!
        }
        curr.isEndOfWord = true
    }
}
```
**Trie:** Trie ma'lumotlar strukturasi prefiksga asoslangan qidiruvlarda hash-mapdan ko'ra samaraliroq xotira boshqaruvini ta'minlaydi.

### Topshiriq #1055: Tarmoq Komponentlarini Aniqlash (Union-Find)
**Tavsif:** Tarmoqdagi bog'liq bo'lmagan klasterlarni aniqlash.
**Talablar:** Path compression va union by rank texnikalari.
**Yechim (Swift):**
```swift
class DSU {
    var parent: [Int]
    init(n: Int) { parent = Array(0..<n) }
    func find(_ i: Int) -> Int {
        if parent[i] == i { return i }
        parent[i] = find(parent[i]) // Path compression
        return parent[i]
    }
    func union(_ i: Int, _ j: Int) {
        let rootI = find(i), rootJ = find(j)
        if rootI != rootJ { parent[rootI] = rootJ }
    }
}
```
**Tushuntirish:** DSU algoritmi katta tarmoqlarda elementlarning bir-biriga bog'liqligini tekshirishda eng yuqori unumdorlikni beradi.

### Topshiriq #1056: Topologik Saralash (Kahn Algoritmi)
**Tavsif:** Vazifalarni bajarilish ketma-ketligini (dependency) aniqlash.
**Talablar:** O(V + E) vaqt murakkabligi.
**Yechim (Swift):**
```swift
func topologicalSort(n: Int, adj: [[Int]], inDegree: inout [Int]) -> [Int] {
    var queue = [Int](), result = [Int]()
    for i in 0..<n where inDegree[i] == 0 { queue.append(i) }
    while !queue.isEmpty {
        let u = queue.removeFirst()
        result.append(u)
        for v in adj[u] {
            inDegree[v] -= 1
            if inDegree[v] == 0 { queue.append(v) }
        }
    }
    return result
}
```
**Tushuntirish:** Loyiha menejmenti tizimlarida vazifalar bog'liqligini (DAG) hal qilish uchun eng samarali usul.

### Topshiriq #1057: Eng Kichik Qamrovchi Daraxt (Kruskal)
**Tavsif:** Serverlararo aloqa xarajatlarini minimallashtirib, barchasini bog'lash.
**Talablar:** DSU bilan integratsiya, O(E log E).
**Yechim (Swift):**
```swift
struct Edge { let u: Int, v: Int, weight: Int }
func kruskal(n: Int, edges: [Edge]) -> Int {
    let sortedEdges = edges.sorted { $0.weight < $1.weight }
    let dsu = DSU(n: n)
    var mstWeight = 0
    for edge in sortedEdges {
        if dsu.find(edge.u) != dsu.find(edge.v) {
            dsu.union(edge.u, edge.v)
            mstWeight += edge.weight
        }
    }
    return mstWeight
}
```
**Tushuntirish:** Kruskal algoritmi tarmoq infratuzilmasini qurishda xarajatlarni minimal darajada ushlab turish uchun ishlatiladi.

### Topshiriq #1058: Bipartite Grafni Tekshirish (BFS)
**Tavsif:** Foydalanuvchilarni ikki guruhga (masalan, "do'stlar" va "dushmanlar") ajratish.
**Talablar:** O(V + E) murakkablik, 2-rangli bo'yash.
**Yechim (Swift):**
```swift
func isBipartite(n: Int, graph: [[Int]]) -> Bool {
    var colors = Array(repeating: -1, count: n)
    for i in 0..<n where colors[i] == -1 {
        var queue = [i]; colors[i] = 0
        while !queue.isEmpty {
            let u = queue.removeFirst()
            for v in graph[u] {
                if colors[v] == -1 { colors[v] = 1 - colors[u]; queue.append(v) }
                else if colors[v] == colors[u] { return false }
            }
        }
    }
    return true
}
```
**Tushuntirish:** BFS yordamida grafni ikki qismga ajratish ijtimoiy tarmoq tahlilida juda muhim.

### Topshiriq #1059: Eng Uzun Umumiy Prefiks (Trie)
**Tavsif:** Katta ma'lumotlar bazasidagi so'zlar orasidagi umumiy prefiksni topish.
**Talablar:** Xotira samaradorligi, O(N*L).
**Yechim (Swift):**
```swift
func longestCommonPrefix(strs: [String]) -> String {
    guard let first = strs.first else { return "" }
    var prefix = ""
    for (i, char) in first.enumerated() {
        for s in strs {
            if i >= s.count || s[s.index(s.startIndex, offsetBy: i)] != char { return prefix }
        }
        prefix.append(char)
    }
    return prefix
}
```
**Tushuntirish:** Trie tuzilmasi bilan birgalikda bu yondashuv katta lug'atlarda qidiruvni tezlashtiradi.

### Topshiriq #1060: Tarmoq Oqimini Hisoblash (Ford-Fulkerson)
**Tavsif:** Serverlar o'rtasidagi maksimal ma'lumot o'tkazuvchanlik qobiliyatini aniqlash.
**Talablar:** DFS/BFS qidiruvlari bilan integratsiya.
**Yechim (Swift):**
```swift
func maxFlow(capacity: [[Int]], source: Int, sink: Int) -> Int {
    var flow = 0, parent = Array(repeating: -1, count: capacity.count)
    while let path = bfs(capacity, source, sink, &parent) {
        var pathFlow = Int.max
        var s = sink
        while s != source { pathFlow = min(pathFlow, capacity[parent[s]][s]); s = parent[s] }
        flow += pathFlow
        var v = sink
        while v != source { let u = parent[v]; capacity[u][v] -= pathFlow; capacity[v][u] += pathFlow; v = u }
    }
    return flow
}
```
**Tushuntirish:** Maksimal oqim algoritmi tarmoq yuklamasini muvozanatlash va o'tkazuvchanlikni maksimal darajaga chiqarish uchun zarurdir.

---

### Topshiriq #1061: Tarmoq topologiyasida eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Katta hajmdagi serverlararo ma'lumotlar uzatish tarmog'ida kechikishni (latency) minimallashtirish.
**Talablar:** `PriorityQueue` yordamida $O(E \log V)$ murakkablikda ishlash.
**Yechim (Swift):**
```swift
struct Edge { let to: Int; let weight: Int }

func dijkstra(graph: [[Edge]], start: Int) -> [Int] {
    var distances = Array(repeating: Int.max, count: graph.count)
    distances[start] = 0
    var pq = [(dist: 0, node: start)] // Oddiy navbat, real loyihada Heap ishlating
    
    while !pq.isEmpty {
        let (d, u) = pq.removeFirst()
        if d > distances[u] { continue }
        for edge in graph[u] {
            if distances[u] + edge.weight < distances[edge.to] {
                distances[edge.to] = distances[u] + edge.weight
                pq.append((distances[edge.to], edge.to))
            }
        }
    }
    return distances
}
```
**Tushuntirish:** Dijkstra algoritmi tarmoq kechikishlarini hisoblashda eng samarali yondashuvdir. `PriorityQueue`dan foydalanish katta graflarda ishlash tezligini keskin oshiradi.

### Topshiriq #1062: Segment Tree yordamida dinamik diapazon yig'indisi
**Tavsif:** Real vaqt rejimida moliyaviy tranzaksiyalar oqimida ma'lum vaqt oralig'idagi umumiy summani hisoblash.
**Talablar:** Yangilash va so'rovlar uchun $O(\log N)$ vaqt murakkabligi.
**Yechim (Swift):**
```swift
class SegmentTree {
    var tree: [Int]
    let n: Int
    init(_ data: [Int]) {
        n = data.count
        tree = Array(repeating: 0, count: 2 * n)
        for i in 0..<n { tree[n + i] = data[i] }
        for i in stride(from: n - 1, through: 1, by: -1) { tree[i] = tree[2 * i] + tree[2 * i + 1] }
    }
    func update(_ i: Int, _ val: Int) {
        var idx = i + n; tree[idx] = val
        while idx > 1 { idx /= 2; tree[idx] = tree[2 * idx] + tree[2 * idx + 1] }
    }
}
```
**Tushuntirish:** Segment Tree massivdagi elementlar tez-tez o'zgarib turganda yig'indini hisoblash uchun eng optimal tuzilmadir.

### Topshiriq #1063: Fenwick Tree (Binary Indexed Tree) bilan chastotani tahlil qilish
**Tavsif:** Foydalanuvchi harakatlari loglarida hodisalar chastotasini hisoblash.
**Talablar:** Xotira tejamkorligi va $O(\log N)$ operatsiya tezligi.
**Yechim (Swift):**
```swift
class FenwickTree {
    var tree: [Int]
    init(size: Int) { tree = Array(repeating: 0, count: size + 1) }
    func add(index: Int, val: Int) {
        var i = index
        while i < tree.count { tree[i] += val; i += i & (-i) }
    }
    func query(index: Int) -> Int {
        var i = index, sum = 0
        while i > 0 { sum += tree[i]; i -= i & (-i) }
        return sum
    }
}
```
**Tushuntirish:** Fenwick Tree Segment Tree'ga qaraganda kamroq xotira talab qiladi va implementatsiyasi sodda, bu esa yuqori yuklamali tizimlar uchun juda mos.

### Topshiriq #1064: Trie (Prefix Tree) bilan avtomatik to'ldirish tizimi
**Tavsif:** Foydalanuvchi qidiruv so'rovlarini tezkor avtomatik to'ldirish (Autocomplete).
**Talablar:** So'rovlarni $O(L)$ vaqtda izlash, bu yerda $L$ - so'z uzunligi.
**Yechim (Swift):**
```swift
class TrieNode {
    var children = [Character: TrieNode]()
    var isEndOfWord = false
}

class Trie {
    let root = TrieNode()
    func insert(_ word: String) {
        var current = root
        for char in word {
            if current.children[char] == nil { current.children[char] = TrieNode() }
            current = current.children[char]!
        }
        current.isEndOfWord = true
    }
}
```
**Tavsif:** Trie tuzilmasi prefiks asosidagi qidiruvlar uchun eng tezkor yechimdir, chunki u qidiruv vaqtini so'zlar soniga emas, balki so'z uzunligiga bog'laydi.

### Topshiriq #1065: Grafda sikllarni aniqlash (DFS)
**Tavsif:** Mikroxizmatlar bog'liqliklarida (dependency) o'zaro bog'liqlik (circular dependency) xatolarini aniqlash.
**Talablar:** Rekursiv yondashuv va xotira xavfsizligi.
**Yechim (Swift):**
```swift
func hasCycle(graph: [[Int]]) -> Bool {
    var visited = Array(repeating: false, count: graph.count)
    var recStack = Array(repeating: false, count: graph.count)
    
    func dfs(_ u: Int) -> Bool {
        visited[u] = true; recStack[u] = true
        for v in graph[u] {
            if !visited[v] && dfs(v) { return true }
            else if recStack[v] { return true }
        }
        recStack[u] = false; return false
    }
    return (0..<graph.count).contains { !visited[$0] && dfs($0) }
}
```
**Tushuntirish:** `recStack` yordamida biz joriy rekursiya yo'lida takrorlanish borligini tekshiramiz, bu tizim barqarorligi uchun muhim.

### Topshiriq #1066: Kruskal algoritmi bilan minimal qamrovchi daraxt (MST)
**Tavsif:** Shaharlararo optik tolali tarmoqni eng kam xarajat bilan ulash.
**Talablar:** Disjoint Set Union (DSU) yordamida samaradorlik.
**Yechim (Swift):**
```swift
struct Edge { let u: Int, v: Int, weight: Int }
func kruskal(edges: [Edge], n: Int) -> Int {
    var parent = Array(0..<n)
    func find(_ i: Int) -> Int { return parent[i] == i ? i : find(parent[i]) }
    let sortedEdges = edges.sorted { $0.weight < $1.weight }
    var mstWeight = 0
    for edge in sortedEdges {
        let rootU = find(edge.u), rootV = find(edge.v)
        if rootU != rootV { parent[rootU] = rootV; mstWeight += edge.weight }
    }
    return mstWeight
}
```
**Tushuntirish:** Kruskal algoritmi tarmoq infratuzilmasini optimallashtirishda eng kam resurs sarflab maksimal qamrovga erishish uchun ishlatiladi.

### Topshiriq #1067: Tarjan algoritmi bilan kuchli bog'langan komponentlar (SCC)
**Tavsif:** Ijtimoiy tarmoqlarda o'zaro ta'sir guruhlarini aniqlash.
**Talablar:** Bir martalik DFS o'tish bilan $O(V+E)$ murakkablik.
**Yechim (Swift):**
```swift
// Tarjan algoritmi yordamida SCC aniqlash
var timer = 0, disc = [Int](), low = [Int](), stack = [Int]()
// ... (DFS logikasi bilan SCC guruhlarini ajratish)
```
**Tushuntirish:** Tarjan algoritmi graflardagi klasterlarni aniqlashda eng samarali hisoblanadi, chunki u barcha komponentlarni bitta DFS o'tishida topadi.

### Topshiriq #1068: Segment Tree bilan Range Minimum Query (RMQ)
**Tavsif:** Sensor ma'lumotlarida ma'lum vaqt oralig'idagi minimal qiymatni aniqlash.
**Talablar:** $O(\log N)$ vaqtda so'rovlarni qayta ishlash.
**Yechim (Swift):**
```swift
func queryMin(_ l: Int, _ r: Int, _ tree: [Int], _ n: Int) -> Int {
    var res = Int.max, left = l + n, right = r + n
    while left < right {
        if left % 2 == 1 { res = min(res, tree[left]); left += 1 }
        if right % 2 == 1 { right -= 1; res = min(res, tree[right]) }
        left /= 2; right /= 2
    }
    return res
}
```
**Tushuntirish:** RMQ muammosi real vaqtda monitoring tizimlarida anomaliyalarni (minimal qiymatlarni) tezkor aniqlash uchun zarur.

### Topshiriq #1069: Trie yordamida IP-manzillar prefiksini izlash
**Tavsif:** Tarmoq xavfsizligida IP-manzillarni blokirovka qilish ro'yxatini (blacklist) tezkor tekshirish.
**Talablar:** Bit darajasida qidiruv va yuqori tezlik.
**Yechim (Swift):**
```swift
class IPTrieNode { var children = [0: IPTrieNode(), 1: IPTrieNode()]; var isBlocked = false }
// IP manzilni 32-bitli binar ko'rinishda Trie'ga kiritish va izlash
```
**Tushuntirish:** IP-manzillarni Trie'da saqlash, millionlab qoidalarni millisekundlarda tekshirish imkonini beradi.

### Topshiriq #1070: Fenwick Tree bilan 2D maydon yig'indisi
**Tavsif:** Tasvirni qayta ishlashda (image processing) piksel hududlari yig'indisini hisoblash.
**Talablar:** 2D massivda samarali yangilash va so'rov.
**Yechim (Swift):**
```swift
class FenwickTree2D {
    var tree: [[Int]]
    init(n: Int, m: Int) { tree = Array(repeating: Array(repeating: 0, count: m + 1), count: n + 1) }
    func update(r: Int, c: Int, val: Int) {
        var i = r
        while i < tree.count {
            var j = c
            while j < tree[0].count { tree[i][j] += val; j += j & (-j) }
            i += i & (-i)
        }
    }
}
```
**Tushuntirish:** 2D Fenwick Tree tasvir yoki matritsa ko'rinishidagi ma'lumotlar ustida hududiy operatsiyalarni bajarishda eng ixcham va tezkor yechimdir.

---

### Topshiriq #1071: Tarmoq topologiyasida eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Katta hajmdagi serverlar tarmog'ida ma'lumotlar uzatish uchun eng kam kechikishli (latency) yo'lni aniqlash.
**Talablar:** O(E log V) murakkablik, xotira xavfsizligi uchun `PriorityQueue`dan foydalanish.
**Yechim (Swift):**
```swift
struct Edge { let to: Int; let weight: Int }

func findShortestPath(n: Int, adj: [[Edge]], start: Int) -> [Int] {
    var dist = Array(repeating: Int.max, count: n)
    dist[start] = 0
    var pq = [(Int, Int)]() // (node, weight)
    pq.append((start, 0))
    
    while !pq.isEmpty {
        pq.sort { $0.1 < $1.1 }
        let (u, d) = pq.removeFirst()
        if d > dist[u] { continue }
        for edge in adj[u] {
            if dist[u] + edge.weight < dist[edge.to] {
                dist[edge.to] = dist[u] + edge.weight
                pq.append((edge.to, dist[edge.to]))
            }
        }
    }
    return dist
}
```
**Tushuntirish:** Dijkstra algoritmi tarmoq kechikishlarini minimallashtirishda eng samarali yechim hisoblanadi.

### Topshiriq #1072: Dinamik massivda oraliq yig'indisini hisoblash (Fenwick Tree)
**Tavsif:** Real vaqt rejimida moliyaviy tranzaksiyalar oqimida ma'lum vaqt oralig'idagi umumiy summani tezkor hisoblash.
**Talablar:** O(log N) yangilash va so'rov vaqti.
**Yechim (Swift):**
```swift
class FenwickTree {
    private var tree: [Int]
    init(size: Int) { tree = Array(repeating: 0, count: size + 1) }
    
    func update(index: Int, delta: Int) {
        var i = index + 1
        while i < tree.count { tree[i] += delta; i += i & -i }
    }
    
    func query(index: Int) -> Int {
        var i = index + 1, sum = 0
        while i > 0 { sum += tree[i]; i -= i & -i }
        return sum
    }
}
```
**Tushuntirish:** Fenwick Tree (Binary Indexed Tree) xotira tejamkorligi va tezligi bo'yicha Segment Tree'dan ustunroqdir.

### Topshiriq #1073: Avtomatik to'ldirish tizimi (Trie)
**Tavsif:** Foydalanuvchi kiritayotgan so'zlarni milliy lug'at bazasi asosida tezkor bashorat qilish.
**Talablar:** Prefiks bo'yicha qidiruv, O(L) murakkablik (L - so'z uzunligi).
**Yechim (Swift):**
```swift
class TrieNode {
    var children = [Character: TrieNode]()
    var isEndOfWord = false
}

class Trie {
    let root = TrieNode()
    func insert(_ word: String) {
        var curr = root
        for char in word {
            if curr.children[char] == nil { curr.children[char] = TrieNode() }
            curr = curr.children[char]!
        }
        curr.isEndOfWord = true
    }
}
```
**Tushuntirish:** Trie tuzilmasi katta hajmdagi matnli ma'lumotlarni qidirishda xesh-jadvallarga qaraganda samaraliroq.

### Topshiriq #1074: Segment Tree yordamida oraliq maksimumini topish
**Tavsif:** Sensor ma'lumotlari oqimida ma'lum vaqt oralig'idagi eng yuqori qiymatni aniqlash.
**Talablar:** O(log N) qidiruv, xavfsiz indekslash.
**Yechim (Swift):**
```swift
class SegmentTree {
    var tree: [Int]
    let n: Int
    init(_ data: [Int]) {
        n = data.count
        tree = Array(repeating: 0, count: 2 * n)
        for i in 0..<n { tree[n + i] = data[i] }
        for i in stride(from: n - 1, through: 1, by: -1) { tree[i] = max(tree[2 * i], tree[2 * i + 1]) }
    }
    func query(l: Int, r: Int) -> Int {
        var res = 0, left = l + n, right = r + n
        while left < right {
            if left % 2 == 1 { res = max(res, tree[left]); left += 1 }
            if right % 2 == 1 { right -= 1; res = max(res, tree[right]) }
            left /= 2; right /= 2
        }
        return res
    }
}
```
**Tushuntirish:** Segment Tree statik massivlarda oraliq so'rovlarini bajarish uchun eng optimal strukturadir.

### Topshiriq #1075: Graflarda sikllarni aniqlash (DFS)
**Tavsif:** Mikroxizmatlar arxitekturasida o'zaro bog'liqliklar (dependency) orasida "deadlock" (o'lik qulf) mavjudligini tekshirish.
**Talablar:** Rekursiv xavfsizlik, O(V + E) murakkablik.
**Yechim (Swift):**
```swift
func hasCycle(n: Int, adj: [[Int]]) -> Bool {
    var visited = Array(repeating: 0, count: n) // 0: unvisited, 1: visiting, 2: visited
    func dfs(_ u: Int) -> Bool {
        visited[u] = 1
        for v in adj[u] {
            if visited[v] == 1 { return true }
            if visited[v] == 0 && dfs(v) { return true }
        }
        visited[u] = 2
        return false
    }
    for i in 0..<n where visited[i] == 0 { if dfs(i) { return true } }
    return false
}
```
**Tushuntirish:** DFS orqali "visiting" holatini kuzatish sikllarni aniqlashning standart va ishonchli usulidir.

### Topshiriq #1076: Kenglik bo'yicha qidiruv (BFS) - Eng qisqa yo'l
**Tavsif:** Ijtimoiy tarmoq graflarida ikki foydalanuvchi orasidagi eng qisqa "do'stlik" masofasini topish.
**Talablar:** Navbat (Queue) tuzilmasidan foydalanish, xotira samaradorligi.
**Yechim (Swift):**
```swift
func shortestPathBFS(adj: [[Int]], start: Int, target: Int) -> Int {
    var queue = [(start, 0)]
    var visited = Set([start])
    while !queue.isEmpty {
        let (u, dist) = queue.removeFirst()
        if u == target { return dist }
        for v in adj[u] where !visited.contains(v) {
            visited.insert(v)
            queue.append((v, dist + 1))
        }
    }
    return -1
}
```
**Tushuntirish:** BFS vaznsiz graflarda eng qisqa yo'lni kafolatlaydi.

### Topshiriq #1077: Trie yordamida so'zlar sonini sanash
**Tavsif:** Katta hujjatlar to'plamida ma'lum prefiksga ega bo'lgan so'zlar chastotasini aniqlash.
**Talablar:** Har bir tugunda `count` o'zgaruvchisini saqlash.
**Yechim (Swift):**
```swift
class CountTrieNode {
    var children = [Character: CountTrieNode]()
    var count = 0
}
// Insert vaqtida har bir tugun count'ini oshirish kifoya.
```
**Tushuntirish:** Trie tugunlarida `count` saqlash prefiks bo'yicha qidiruvni O(1) ga yaqinlashtiradi.

### Topshiriq #1078: Topologik tartiblash (Kahn algoritmi)
**Tavsif:** Loyiha vazifalari (tasks) orasidagi bog'liqliklar ketma-ketligini aniqlash.
**Talablar:** Kirish darajasi (in-degree) hisobi, O(V + E).
**Yechim (Swift):**
```swift
func topologicalSort(n: Int, adj: [[Int]], inDegree: inout [Int]) -> [Int] {
    var queue = [Int](), result = [Int]()
    for i in 0..<n where inDegree[i] == 0 { queue.append(i) }
    while !queue.isEmpty {
        let u = queue.removeFirst(); result.append(u)
        for v in adj[u] {
            inDegree[v] -= 1
            if inDegree[v] == 0 { queue.append(v) }
        }
    }
    return result
}
```
**Tushuntirish:** Kahn algoritmi vazifalarni bajarish tartibini aniqlashda eng intuitiv yondashuvdir.

### Topshiriq #1079: Fenwick Tree yordamida inversiyalarni sanash
**Tavsif:** Katta massivdagi tartibsizlik darajasini (inversion count) aniqlash.
**Talablar:** O(N log N) murakkablik.
**Yechim (Swift):**
```swift
func countInversions(arr: [Int]) -> Int {
    let ft = FenwickTree(size: arr.count + 1)
    var count = 0
    for i in stride(from: arr.count - 1, through: 0, by: -1) {
        count += ft.query(index: arr[i] - 1)
        ft.update(index: arr[i], delta: 1)
    }
    return count
}
```
**Tushuntirish:** Fenwick Tree yordamida inversiyalarni sanash Merge Sort'dan ko'ra kod jihatidan qisqaroq va tezroq ishlaydi.

### Topshiriq #1080: Minimal qamrovchi daraxt (Kruskal)
**Tavsif:** Shaharlararo optik tolali tarmoqni eng kam xarajat bilan ulash.
**Talablar:** Disjoint Set Union (DSU) strukturasi, O(E log E).
**Yechim (Swift):**
```swift
class DSU {
    var parent: [Int]
    init(n: Int) { parent = Array(0..<n) }
    func find(_ i: Int) -> Int {
        if parent[i] == i { return i }
        parent[i] = find(parent[i]); return parent[i]
    }
    func union(_ i: Int, _ j: Int) { parent[find(i)] = find(j) }
}
```
**Tushuntirish:** Kruskal algoritmi DSU bilan birgalikda eng samarali minimal qamrovchi daraxtni hosil qiladi.

---

### Topshiriq #1081: Tarmoq topologiyasida eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Katta hajmdagi serverlararo aloqa tarmog'ida ma'lumotlar paketini eng kam kechikish bilan yetkazish.
**Talablar:** O(E log V) murakkablik, xotira xavfsizligi uchun `PriorityQueue`dan foydalanish.
**Yechim (Swift):**
```swift
struct Edge { let to: Int; let weight: Int }

func dijkstra(graph: [[Edge]], start: Int) -> [Int] {
    var distances = Array(repeating: Int.max, count: graph.count)
    distances[start] = 0
    var pq = [(dist: Int, node: Int)]() // Oddiy navbat, ishlab chiqarishda Heap ishlatiladi
    
    while !pq.isEmpty {
        let (d, u) = pq.removeFirst()
        if d > distances[u] { continue }
        for edge in graph[u] {
            if distances[u] + edge.weight < distances[edge.to] {
                distances[edge.to] = distances[u] + edge.weight
                pq.append((distances[edge.to], edge.to))
            }
        }
    }
    return distances
}
```
**Tushuntirish:** Dijkstra algoritmi tarmoq kechikishlarini minimallashtirishda eng samarali yechimdir.

### Topshiriq #1082: Dinamik oraliq yig'indisi (Fenwick Tree)
**Tavsif:** Moliya tizimida real vaqt rejimida tranzaksiyalar yig'indisini hisoblash.
**Talablar:** O(log N) yangilash va so'rov vaqti.
**Yechim (Swift):**
```swift
class FenwickTree {
    private var tree: [Int]
    init(size: Int) { tree = Array(repeating: 0, count: size + 1) }
    
    func update(index: Int, delta: Int) {
        var i = index
        while i < tree.count { tree[i] += delta; i += i & (-i) }
    }
    
    func query(index: Int) -> Int {
        var i = index, sum = 0
        while i > 0 { sum += tree[i]; i -= i & (-i) }
        return sum
    }
}
```
**Tushuntirish:** Fenwick Tree (Binary Indexed Tree) massivni tez yangilash va yig'indini olish uchun eng ixcham tuzilmadir.

### Topshiriq #1083: Prefix qidiruv tizimi (Trie)
**Tavsif:** Foydalanuvchi kiritayotgan so'zlarni avtomatik to'ldirish (Autocomplete) xizmati.
**Talablar:** Xotira samaradorligi va tezkor qidiruv.
**Yechim (Swift):**
```swift
class TrieNode {
    var children = [Character: TrieNode]()
    var isEndOfWord = false
}

class Trie {
    let root = TrieNode()
    func insert(_ word: String) {
        var current = root
        for char in word {
            if current.children[char] == nil { current.children[char] = TrieNode() }
            current = current.children[char]!
        }
        current.isEndOfWord = true
    }
}
```
**Tushuntirish:** Trie tuzilmasi lug'at qidiruvini O(L) vaqtda (L - so'z uzunligi) bajaradi, bu esa katta lug'atlar uchun optimaldir.

### Topshiriq #1084: Oraliqdagi eng katta qiymat (Segment Tree)
**Tavsif:** Sensor ma'lumotlari oqimida ma'lum vaqt oralig'idagi maksimal qiymatni aniqlash.
**Talablar:** O(log N) murakkablikdagi so'rovlar.
**Yechim (Swift):**
```swift
class SegmentTree {
    var tree: [Int]
    let n: Int
    init(_ data: [Int]) {
        n = data.count
        tree = Array(repeating: 0, count: 2 * n)
        for i in 0..<n { tree[n + i] = data[i] }
        for i in (1..<n).reversed() { tree[i] = max(tree[2 * i], tree[2 * i + 1]) }
    }
    
    func query(l: Int, r: Int) -> Int {
        var res = 0, left = l + n, right = r + n
        while left < right {
            if left % 2 == 1 { res = max(res, tree[left]); left += 1 }
            if right % 2 == 1 { right -= 1; res = max(res, tree[right]) }
            left /= 2; right /= 2
        }
        return res
    }
}
```
**Tushuntirish:** Segment Tree statik va dinamik oraliq so'rovlari uchun eng moslashuvchan tuzilmadir.

### Topshiriq #1085: Grafda sikllarni aniqlash (DFS)
**Tavsif:** Tizim bog'liqliklarida (dependency graph) o'zaro bog'liqlik (deadlock) xavfini aniqlash.
**Talablar:** Rekursiv xavfsizlik va O(V+E) vaqt.
**Yechim (Swift):**
```swift
func hasCycle(graph: [[Int]]) -> Bool {
    var visited = Array(repeating: false, count: graph.count)
    var recStack = Array(repeating: false, count: graph.count)
    
    func dfs(_ u: Int) -> Bool {
        visited[u] = true; recStack[u] = true
        for v in graph[u] {
            if !visited[v] && dfs(v) { return true }
            else if recStack[v] { return true }
        }
        recStack[u] = false
        return false
    }
    return (0..<graph.count).contains { !visited[$0] && dfs($0) }
}
```
**Tushuntirish:** DFS orqali rekursiv stekni kuzatish orqali sikllarni aniqlash tizim barqarorligini ta'minlaydi.

### Topshiriq #1086: Kenglik bo'yicha qidiruv (BFS)
**Tavsif:** Ijtimoiy tarmoqda ikki foydalanuvchi o'rtasidagi eng qisqa "do'stlik" masofasini topish.
**Talablar:** Navbat (Queue) yordamida xotirani boshqarish.
**Yechim (Swift):**
```swift
func bfs(graph: [[Int]], start: Int, target: Int) -> Int {
    var queue = [(start, 0)]
    var visited = Set([start])
    
    while !queue.isEmpty {
        let (u, dist) = queue.removeFirst()
        if u == target { return dist }
        for v in graph[u] {
            if !visited.contains(v) {
                visited.insert(v); queue.append((v, dist + 1))
            }
        }
    }
    return -1
}
```
**Tushuntirish:** BFS eng qisqa yo'lni topish uchun eng ishonchli algoritmdir.

### Topshiriq #1087: Topologik tartiblash (Kahn algoritmi)
**Tavsif:** Loyiha vazifalarini bajarilish ketma-ketligini (task scheduling) belgilash.
**Talablar:** Kiruvchi darajalar (in-degree) hisobi.
**Yechim (Swift):**
```swift
func topologicalSort(n: Int, edges: [[Int]]) -> [Int] {
    var inDegree = Array(repeating: 0, count: n)
    var adj = Array(repeating: [Int](), count: n)
    for e in edges { adj[e[0]].append(e[1]); inDegree[e[1]] += 1 }
    
    var queue = (0..<n).filter { inDegree[$0] == 0 }
    var result = [Int]()
    
    while !queue.isEmpty {
        let u = queue.removeFirst(); result.append(u)
        for v in adj[u] {
            inDegree[v] -= 1
            if inDegree[v] == 0 { queue.append(v) }
        }
    }
    return result
}
```
**Tushuntirish:** Kahn algoritmi vazifalar o'rtasidagi bog'liqlikni tartiblash uchun eng samarali yondashuvdir.

### Topshiriq #1088: Union-Find (Disjoint Set)
**Tavsif:** Tarmoq segmentlari birlashganligini tekshirish (Network Connectivity).
**Talablar:** Path compression va union by rank optimizatsiyasi.
**Yechim (Swift):**
```swift
class UnionFind {
    var parent: [Int]
    init(_ n: Int) { parent = Array(0..<n) }
    
    func find(_ i: Int) -> Int {
        if parent[i] == i { return i }
        parent[i] = find(parent[i]) // Path compression
        return parent[i]
    }
    
    func union(_ i: Int, _ j: Int) {
        let rootI = find(i), rootJ = find(j)
        if rootI != rootJ { parent[rootI] = rootJ }
    }
}
```
**Tushuntirish:** Union-Find algoritmi tarmoq komponentlarini dinamik birlashtirishda O(α(N)) vaqt murakkabligini beradi.

### Topshiriq #1089: Trie yordamida so'zlar sonini sanash
**Tavsif:** Katta matnlar bazasida ma'lum prefiksga ega so'zlar sonini tezkor aniqlash.
**Talablar:** Trie tugunlarida `count` parametrini saqlash.
**Yechim (Swift):**
```swift
class CountTrieNode {
    var children = [Character: CountTrieNode]()
    var count = 0
}

func insertAndCount(_ root: CountTrieNode, _ word: String) {
    var curr = root
    for char in word {
        if curr.children[char] == nil { curr.children[char] = CountTrieNode() }
        curr = curr.children[char]!
        curr.count += 1
    }
}
```
**Tushuntirish:** Har bir tugunda `count` saqlash qidiruv vaqtini O(1) ga yaqinlashtiradi.

### Topshiriq #1090: Eng yaqin umumiy ota (LCA)
**Tavsif:** Daraxtsimon ierarxik tizimlarda (masalan, fayl tizimi) ikki tugun o'rtasidagi umumiy ota tugunni topish.
**Talablar:** O(log N) vaqt murakkabligi.
**Yechim (Swift):**
```swift
// Binary Lifting usuli uchun asosiy funksiya
func getLCA(u: Int, v: Int, depth: [Int], parent: [[Int]]) -> Int {
    var (u, v) = (u, v)
    if depth[u] < depth[v] { swap(&u, &v) }
    // Chuqurlikni tenglashtirish
    for i in (0..<20).reversed() {
        if depth[u] - (1 << i) >= depth[v] { u = parent[u][i] }
    }
    if u == v { return u }
    // Ota tugunlarni qidirish
    for i in (0..<20).reversed() {
        if parent[u][i] != parent[v][i] {
            u = parent[u][i]; v = parent[v][i]
        }
    }
    return parent[u][0]
}
```
**Tushuntirish:** Binary Lifting yordamida LCA qidiruvi katta daraxtlar uchun eng tezkor yechim hisoblanadi.

---

### Topshiriq #1091: Tarmoq topologiyasida eng qisqa yo'lni aniqlash (Dijkstra)
**Tavsif:** Katta hajmdagi serverlar tarmog'ida ma'lumotlar paketini eng kam kechikish bilan yetkazish.
**Talablar:** O(E log V) murakkablik, xotira xavfsizligi.
**Yechim (Swift):**
```swift
import Foundation

struct Edge { let to: Int; let weight: Int }

func dijkstra(graph: [[Edge]], start: Int) -> [Int] {
    var dist = Array(repeating: Int.max, count: graph.count)
    dist[start] = 0
    var pq = [(dist: 0, node: start)] // Oddiy navbat, real loyihada Heap ishlatiladi
    
    while !pq.isEmpty {
        let (d, u) = pq.removeFirst()
        if d > dist[u] { continue }
        for edge in graph[u] {
            if dist[u] + edge.weight < dist[edge.to] {
                dist[edge.to] = dist[u] + edge.weight
                pq.append((dist[edge.to], edge.to))
            }
        }
        pq.sort { $0.dist < $1.dist }
    }
    return dist
}
```
**Tushuntirish:** Dijkstra algoritmi tarmoq marshrutizatsiyasida standart hisoblanadi. `dist` massivi orqali masofalar nazorat qilinadi.

### Topshiriq #1092: Dinamik massivda diapazon yig'indisini hisoblash (Fenwick Tree)
**Tavsif:** Real vaqt rejimida moliyaviy tranzaksiyalar oqimini yig'indisini kuzatish.
**Talablar:** O(log N) yangilash va so'rov vaqti.
**Yechim (Swift):**
```swift
class FenwickTree {
    private var tree: [Int]
    init(size: Int) { tree = Array(repeating: 0, count: size + 1) }
    
    func update(index: Int, delta: Int) {
        var i = index + 1
        while i < tree.count { tree[i] += delta; i += i & (-i) }
    }
    
    func query(index: Int) -> Int {
        var i = index + 1, sum = 0
        while i > 0 { sum += tree[i]; i -= i & (-i) }
        return sum
    }
}
```
**Tushuntirish:** Fenwick Tree (Binary Indexed Tree) xotira tejamkorligi va tezligi bilan katta ma'lumotlar to'plamida samarali.

### Topshiriq #1093: Diapazon bo'yicha eng katta qiymatni topish (Segment Tree)
**Tavsif:** Sensor ma'lumotlarida ma'lum vaqt oralig'idagi eng yuqori ko'rsatkichni aniqlash.
**Talablar:** O(log N) so'rov vaqti, rekursiv bo'lmagan implementatsiya afzal.
**Yechim (Swift):**
```swift
class SegmentTree {
    private var tree: [Int], n: Int
    init(data: [Int]) {
        n = data.count; tree = Array(repeating: 0, count: 2 * n)
        for i in 0..<n { tree[n + i] = data[i] }
        for i in stride(from: n - 1, through: 1, by: -1) { tree[i] = max(tree[2*i], tree[2*i+1]) }
    }
    func query(l: Int, r: Int) -> Int {
        var res = 0, left = l + n, right = r + n
        while left < right {
            if left % 2 == 1 { res = max(res, tree[left]); left += 1 }
            if right % 2 == 1 { right -= 1; res = max(res, tree[right]) }
            left /= 2; right /= 2
        }
        return res
    }
}
```
**Tushuntirish:** Iterativ Segment Tree xotira va vaqt bo'yicha rekursiv yondashuvdan ustun turadi.

### Topshiriq #1094: Avtomatik to'ldirish tizimi (Trie)
**Tavsif:** Foydalanuvchi kiritayotgan so'zlarni tezkor qidirish va taklif etish.
**Talablar:** O(L) qidiruv vaqti, bu yerda L - so'z uzunligi.
**Yechim (Swift):**
```swift
class TrieNode {
    var children: [Character: TrieNode] = [:]
    var isEndOfWord = false
}

class Trie {
    let root = TrieNode()
    func insert(_ word: String) {
        var curr = root
        for char in word {
            if curr.children[char] == nil { curr.children[char] = TrieNode() }
            curr = curr.children[char]!
        }
        curr.isEndOfWord = true
    }
}
```
**Tushuntirish:** Trie tuzilmasi prefikslar bo'yicha qidiruvda eng yuqori samaradorlikni ta'minlaydi.

### Topshiriq #1095: Graflarda sikllarni aniqlash (DFS)
**Tavsif:** Tizim bog'liqliklarida (dependency) yuzaga kelishi mumkin bo'lgan o'zaro bog'liqlik xatolarini topish.
**Talablar:** O(V + E) murakkablik.
**Yechim (Swift):**
```swift
func hasCycle(graph: [[Int]]) -> Bool {
    var visited = Array(repeating: false, count: graph.count)
    var recStack = Array(repeating: false, count: graph.count)
    
    func dfs(_ u: Int) -> Bool {
        visited[u] = true; recStack[u] = true
        for v in graph[u] {
            if !visited[v] && dfs(v) { return true }
            else if recStack[v] { return true }
        }
        recStack[u] = false; return false
    }
    return (0..<graph.count).contains { !visited[$0] && dfs($0) }
}
```
**Tushuntirish:** `recStack` yordamida rekursiya zanjiridagi tugunlar kuzatiladi, bu siklni aniqlash uchun kalit hisoblanadi.

### Topshiriq #1096: Minimal qamrovchi daraxt (Kruskal)
**Tavsif:** Shaharlararo optik tolali tarmoqni eng kam xarajat bilan ulash.
**Talablar:** Union-Find ma'lumotlar tuzilmasi bilan birlashtirish.
**Yechim (Swift):**
```swift
struct Edge { let u: Int, v: Int, weight: Int }
func kruskal(edges: [Edge], n: Int) -> Int {
    var parent = Array(0..<n), cost = 0
    func find(_ i: Int) -> Int { return parent[i] == i ? i : find(parent[i]) }
    let sortedEdges = edges.sorted { $0.weight < $1.weight }
    for edge in sortedEdges {
        let rootU = find(edge.u), rootV = find(edge.v)
        if rootU != rootV { parent[rootU] = rootV; cost += edge.weight }
    }
    return cost
}
```
**Tushuntirish:** Kruskal algoritmi tarmoq infratuzilmasini optimallashtirishda eng samarali yondashuvdir.

### Topshiriq #1097: Eng uzun umumiy prefiks (Trie)
**Tavsif:** Katta datasetdagi so'zlar ro'yxatidan umumiy prefiksni ajratib olish.
**Talablar:** Xotira samaradorligi va tezkor qidiruv.
**Yechim (Swift):**
```swift
func longestCommonPrefix(_ strs: [String]) -> String {
    guard let first = strs.first else { return "" }
    var prefix = ""
    for (i, char) in first.enumerated() {
        for s in strs.dropFirst() {
            if i >= s.count || s[s.index(s.startIndex, offsetBy: i)] != char { return prefix }
        }
        prefix.append(char)
    }
    return prefix
}
```
**Tushuntirish:** Bu yondashuv har bir belgini tekshirib, eng qisqa umumiy prefiksni O(N*M) vaqtda topadi.

### Topshiriq #1098: Topologik tartiblash (Kahn algoritmi)
**Tavsif:** Loyiha vazifalarini bajarilish tartibini (dependency) belgilash.
**Talablar:** O(V + E) murakkablik.
**Yechim (Swift):**
```swift
func topologicalSort(n: Int, adj: [[Int]], inDegree: inout [Int]) -> [Int] {
    var queue = (0..<n).filter { inDegree[$0] == 0 }, result = [Int]()
    while !queue.isEmpty {
        let u = queue.removeFirst(); result.append(u)
        for v in adj[u] {
            inDegree[v] -= 1
            if inDegree[v] == 0 { queue.append(v) }
        }
    }
    return result
}
```
**Tushuntirish:** Kahn algoritmi vazifalar ketma-ketligini aniqlashda eng ishonchli usuldir.

### Topshiriq #1099: Ikki qismli grafni tekshirish (Bipartite)
**Tavsif:** Foydalanuvchilar va resurslar o'rtasidagi bog'liqlikni ikki guruhga ajratish.
**Talablar:** BFS orqali ranglash (coloring).
**Yechim (Swift):**
```swift
func isBipartite(graph: [[Int]]) -> Bool {
    var colors = Array(repeating: -1, count: graph.count)
    for i in 0..<graph.count {
        if colors[i] == -1 {
            var queue = [i]; colors[i] = 0
            while !queue.isEmpty {
                let u = queue.removeFirst()
                for v in graph[u] {
                    if colors[v] == -1 { colors[v] = 1 - colors[u]; queue.append(v) }
                    else if colors[v] == colors[u] { return false }
                }
            }
        }
    }
    return true
}
```
**Tushuntirish:** BFS yordamida grafni ikki rangga bo'yash orqali uning ikki qismli ekanligini aniqlaymiz.

### Topshiriq #1100: Katta massivda diapazon yig'indisi (Segment Tree - Lazy Propagation)
**Tavsif:** Ma'lumotlar bazasida diapazon bo'yicha yangilash va so'rovlarni tezkor bajarish.
**Talablar:** O(log N) murakkablik, Lazy Propagation qo'llanilishi shart.
**Yechim (Swift):**
```swift
class LazySegmentTree {
    var tree: [Int], lazy: [Int], n: Int
    init(size: Int) { n = size; tree = Array(repeating: 0, count: 4 * n); lazy = Array(repeating: 0, count: 4 * n) }
    
    func update(l: Int, r: Int, val: Int, node: Int, start: Int, end: Int) {
        if lazy[node] != 0 { tree[node] += (end - start + 1) * lazy[node]; if start != end { lazy[2*node] += lazy[node]; lazy[2*node+1] += lazy[node] }; lazy[node] = 0 }
        if start > end || start > r || end < l { return }
        if start >= l && end <= r { tree[node] += (end - start + 1) * val; if start != end { lazy[2*node] += val; lazy[2*node+1] += val }; return }
        let mid = (start + end) / 2
        update(l: l, r: r, val: val, node: 2*node, start: start, end: mid)
        update(l: l, r: r, val: val, node: 2*node+1, start: mid+1, end: end)
        tree[node] = tree[2*node] + tree[2*node+1]
    }
}
```
**Tushuntirish:** Lazy Propagation katta massivlarda diapazon bo'yicha yangilashni sezilarli darajada tezlashtiradi.