# Khorazmiy AI: JavaScript & TypeScript - Modul 22
## Mavzu: Ilg'or Algoritmlar: Graflar, Segment Trees, Fenwick va Trie tuzilmalari

### Topshiriq #1051: Tarmoq topologiyasida eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Katta hajmdagi serverlararo aloqa tarmog'ida ma'lumotlar paketini eng kam kechikish bilan yetkazish.
**Talablar:** O(E log V) murakkablik, xotira xavfsizligi va Priority Queue ishlatish.
**Yechim (TypeScript):**
```typescript
class PriorityQueue<T> {
  private heap: { node: T; priority: number }[] = [];
  enqueue(node: T, priority: number) { this.heap.push({ node, priority }); this.heap.sort((a, b) => a.priority - b.priority); }
  dequeue() { return this.heap.shift()?.node; }
  isEmpty() { return this.heap.length === 0; }
}

function findShortestPath(graph: Map<string, { node: string, weight: number }[]>, start: string): Map<string, number> {
  const distances = new Map<string, number>();
  const pq = new PriorityQueue<string>();
  distances.set(start, 0);
  pq.enqueue(start, 0);

  while (!pq.isEmpty()) {
    const u = pq.dequeue()!;
    for (const edge of graph.get(u) || []) {
      const alt = distances.get(u)! + edge.weight;
      if (alt < (distances.get(edge.node) ?? Infinity)) {
        distances.set(edge.node, alt);
        pq.enqueue(edge.node, alt);
      }
    }
  }
  return distances;
}
```
**Tushuntirish:** Dijkstra algoritmi tarmoq kechikishlarini minimallashtirish uchun eng samarali yechimdir.

### Topshiriq #1052: Segment Tree yordamida dinamik diapazon yig'indisi
**Tavsif:** Real vaqt rejimida moliyaviy tranzaksiyalar oqimida ma'lum vaqt oralig'idagi umumiy summani hisoblash.
**Talablar:** O(log N) yangilash va so'rov vaqti.
**Yechim (JavaScript):**
```javascript
class SegmentTree {
  constructor(data) {
    this.n = data.length;
    this.tree = new Array(2 * this.n);
    for (let i = 0; i < this.n; i++) this.tree[this.n + i] = data[i];
    for (let i = this.n - 1; i > 0; i--) this.tree[i] = this.tree[2 * i] + this.tree[2 * i + 1];
  }
  update(i, val) {
    for (this.tree[i += this.n] = val; i > 1; i >>= 1) this.tree[i >> 1] = this.tree[i] + this.tree[i ^ 1];
  }
  query(l, r) {
    let res = 0;
    for (l += this.n, r += this.n; l < r; l >>= 1, r >>= 1) {
      if (l & 1) res += this.tree[l++];
      if (r & 1) res += this.tree[--r];
    }
    return res;
  }
}
```
**Tushuntirish:** Segment Tree katta massivlarda tezkor qism yig'indilarni olish imkonini beradi.

### Topshiriq #1053: Fenwick Tree (Binary Indexed Tree) bilan chastota tahlili
**Tavsif:** Log fayllarida hodisalar chastotasini hisoblash va prefiks yig'indilarni tezkor yangilash.
**Talablar:** O(log N) murakkablik, kam xotira sarfi.
**Yechim (TypeScript):**
```typescript
class FenwickTree {
  private tree: number[];
  constructor(size: number) { this.tree = new Array(size + 1).fill(0); }
  update(i: number, delta: number) {
    for (; i < this.tree.length; i += i & -i) this.tree[i] += delta;
  }
  query(i: number): number {
    let sum = 0;
    for (; i > 0; i -= i & -i) sum += this.tree[i];
    return sum;
  }
}
```
**Tushuntirish:** Fenwick Tree Segment Tree'ga qaraganda kamroq xotira talab qiladi va implementatsiyasi sodda.

### Topshiriq #1054: Trie (Prefix Tree) yordamida avtomatik to'ldirish
**Tavsif:** Foydalanuvchi so'rovlarini tezkor qidirish va taklif etish tizimi.
**Talablar:** O(L) qidiruv vaqti, bu yerda L - so'z uzunligi.
**Yechim (JavaScript):**
```javascript
class TrieNode {
  constructor() { this.children = {}; this.isEndOfWord = false; }
}
class Trie {
  constructor() { this.root = new TrieNode(); }
  insert(word) {
    let node = this.root;
    for (const char of word) {
      if (!node.children[char]) node.children[char] = new TrieNode();
      node = node.children[char];
    }
    node.isEndOfWord = true;
  }
  search(word) {
    let node = this.root;
    for (const char of word) {
      if (!node.children[char]) return false;
      node = node.children[char];
    }
    return node.isEndOfWord;
  }
}
```
**Tushuntirish:** Trie tuzilmasi lug'at qidiruvlarida eng yuqori unumdorlikni ta'minlaydi.

### Topshiriq #1055: Graflarda sikllarni aniqlash (DFS)
**Tavsif:** Tizim bog'liqliklarida (dependency graph) o'zaro bog'liqlik (deadlock) xavfini aniqlash.
**Talablar:** O(V + E) vaqt murakkabligi.
**Yechim (TypeScript):**
```typescript
function hasCycle(graph: Map<number, number[]>): boolean {
  const visited = new Set<number>();
  const recStack = new Set<number>();
  const dfs = (node: number): boolean => {
    visited.add(node); recStack.add(node);
    for (const neighbor of graph.get(node) || []) {
      if (!visited.has(neighbor) && dfs(neighbor)) return true;
      else if (recStack.has(neighbor)) return true;
    }
    recStack.delete(node);
    return false;
  };
  for (const node of graph.keys()) if (!visited.has(node) && dfs(node)) return true;
  return false;
}
```
**Tushuntirish:** Rekursiv stek (recStack) yordamida sikllarni aniqlash tizim barqarorligi uchun muhim.

### Topshiriq #1056: Kenglik bo'yicha qidiruv (BFS) - Eng qisqa yo'l
**Tavsif:** Ijtimoiy tarmoqlarda ikki foydalanuvchi orasidagi masofani (darajani) aniqlash.
**Talablar:** Unweighted graflarda optimal yechim.
**Yechim (JavaScript):**
```javascript
function getShortestDistance(graph, start, target) {
  let queue = [[start, 0]];
  let visited = new Set([start]);
  while (queue.length > 0) {
    let [node, dist] = queue.shift();
    if (node === target) return dist;
    for (let neighbor of graph[node] || []) {
      if (!visited.has(neighbor)) {
        visited.add(neighbor);
        queue.push([neighbor, dist + 1]);
      }
    }
  }
  return -1;
}
```
**Tushuntirish:** BFS qatlamma-qatlam qidirgani uchun unweighted graflarda eng qisqa yo'lni kafolatlaydi.

### Topshiriq #1057: Union-Find (Disjoint Set Union)
**Tavsif:** Tarmoq segmentlarini birlashtirish va ularning bog'liqligini tekshirish.
**Talablar:** Path compression va union by rank optimizatsiyasi.
**Yechim (TypeScript):**
```typescript
class DSU {
  private parent: number[];
  constructor(n: number) { this.parent = Array.from({ length: n }, (_, i) => i); }
  find(i: number): number {
    if (this.parent[i] === i) return i;
    return this.parent[i] = this.find(this.parent[i]);
  }
  union(i: number, j: number) {
    const rootI = this.find(i), rootJ = this.find(j);
    if (rootI !== rootJ) this.parent[rootI] = rootJ;
  }
}
```
**Tushuntirish:** DSU tarmoq komponentlarini boshqarishda deyarli doimiy vaqtda ishlaydi.

### Topshiriq #1058: Topological Sort (Kahn's Algorithm)
**Tavsif:** Vazifalarni bajarish tartibini (task scheduling) aniqlash.
**Talablar:** O(V + E) murakkablik, siklsiz graflar uchun.
**Yechim (JavaScript):**
```javascript
function topologicalSort(numNodes, edges) {
  let inDegree = new Array(numNodes).fill(0);
  let adj = Array.from({ length: numNodes }, () => []);
  edges.forEach(([u, v]) => { adj[u].push(v); inDegree[v]++; });
  let queue = inDegree.map((d, i) => d === 0 ? i : -1).filter(i => i !== -1);
  let result = [];
  while (queue.length) {
    let u = queue.shift(); result.push(u);
    adj[u].forEach(v => { if (--inDegree[v] === 0) queue.push(v); });
  }
  return result;
}
```
**Tushuntirish:** Kahn algoritmi vazifalar ketma-ketligini aniqlashda eng ishonchli usuldir.

### Topshiriq #1059: Trie bilan "Longest Common Prefix"
**Tavsif:** Katta ma'lumotlar to'plamida umumiy prefikslarni topish.
**Talablar:** Xotira samaradorligi va tezkor qidiruv.
**Yechim (TypeScript):**
```typescript
function longestCommonPrefix(strs: string[]): string {
  if (!strs.length) return "";
  let prefix = strs[0];
  for (let i = 1; i < strs.length; i++) {
    while (strs[i].indexOf(prefix) !== 0) {
      prefix = prefix.substring(0, prefix.length - 1);
      if (!prefix) return "";
    }
  }
  return prefix;
}
```
**Tushuntirish:** Trie yondashuvi katta hajmdagi stringlar to'plamida prefiksni aniqlashni optimallashtiradi.

### Topshiriq #1060: Segment Tree Lazy Propagation
**Tavsif:** Katta massivda diapazon bo'yicha qiymatlarni yangilash va so'rash.
**Talablar:** O(log N) murakkablik, "Lazy" yangilash mexanizmi.
**Yechim (JavaScript):**
```javascript
class LazySegmentTree {
  constructor(size) {
    this.n = size;
    this.tree = new Array(4 * size).fill(0);
    this.lazy = new Array(4 * size).fill(0);
  }
  updateRange(node, start, end, l, r, val) {
    if (this.lazy[node] !== 0) {
      this.tree[node] += (end - start + 1) * this.lazy[node];
      if (start !== end) { this.lazy[2 * node] += this.lazy[node]; this.lazy[2 * node + 1] += this.lazy[node]; }
      this.lazy[node] = 0;
    }
    if (start > end || start > r || end < l) return;
    if (start >= l && end <= r) {
      this.tree[node] += (end - start + 1) * val;
      if (start !== end) { this.lazy[2 * node] += val; this.lazy[2 * node + 1] += val; }
      return;
    }
    let mid = Math.floor((start + end) / 2);
    this.updateRange(2 * node, start, mid, l, r, val);
    this.updateRange(2 * node + 1, mid + 1, end, l, r, val);
    this.tree[node] = this.tree[2 * node] + this.tree[2 * node + 1];
  }
}
```
**Tushuntirish:** Lazy propagation diapazon bo'yicha o'zgarishlarni kechiktirib, ishlash tezligini keskin oshiradi.

---

### Topshiriq #1061: Tarmoq topologiyasida eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Katta hajmdagi serverlararo aloqa tarmog'ida ma'lumotlar paketini eng kam kechikish (latency) bilan yetkazib berish.
**Talablar:** O(E log V) murakkablik, Priority Queue (Min-Heap) ishlatilishi shart.
**Yechim (TypeScript):**
```typescript
class PriorityQueue {
    private heap: [number, number][] = [];
    push(val: [number, number]) { this.heap.push(val); this.heap.sort((a, b) => a[1] - b[1]); }
    pop() { return this.heap.shift(); }
    isEmpty() { return this.heap.length === 0; }
}

function findShortestPath(graph: Map<number, [number, number][]>, start: number): number[] {
    const distances = new Array(graph.size).fill(Infinity);
    const pq = new PriorityQueue();
    distances[start] = 0;
    pq.push([start, 0]);

    while (!pq.isEmpty()) {
        const [u, dist] = pq.pop()!;
        for (const [v, weight] of graph.get(u) || []) {
            if (distances[u] + weight < distances[v]) {
                distances[v] = distances[u] + weight;
                pq.push([v, distances[v]]);
            }
        }
    }
    return distances;
}
```
**Tushuntirish:** Dijkstra algoritmi tarmoq kechikishlarini minimallashtirishda standart hisoblanadi. Min-Heap yordamida eng kichik masofali tugunni tanlash optimallikni ta'minlaydi.

---

### Topshiriq #1062: Dinamik oraliq yig'indisi (Fenwick Tree)
**Tavsif:** Real vaqt rejimida moliyaviy tranzaksiyalar oqimini kuzatish va ma'lum oraliqdagi yig'indini tezkor hisoblash.
**Talablar:** O(log N) yangilash va so'rov vaqti.
**Yechim (JavaScript):**
```javascript
class FenwickTree {
    constructor(size) { this.tree = new Array(size + 1).fill(0); }
    update(i, delta) {
        for (; i < this.tree.length; i += i & -i) this.tree[i] += delta;
    }
    query(i) {
        let sum = 0;
        for (; i > 0; i -= i & -i) sum += this.tree[i];
        return sum;
    }
}
```
**Tushuntirish:** Fenwick Tree (Binary Indexed Tree) massivni yangilash va yig'indini hisoblashda Segment Tree'ga qaraganda kamroq xotira talab qiladi.

---

### Topshiriq #1063: Avtomatik to'ldirish tizimi (Trie)
**Tavsif:** Foydalanuvchi qidiruv maydoniga yozayotganda so'zlarni tezkor taklif qilish.
**Talablar:** Prefiks bo'yicha qidiruv O(L) vaqtda bajarilishi kerak (L - so'z uzunligi).
**Yechim (TypeScript):**
```typescript
class TrieNode {
    children: Map<string, TrieNode> = new Map();
    isEndOfWord: boolean = false;
}

class Trie {
    root = new TrieNode();
    insert(word: string) {
        let node = this.root;
        for (const char of word) {
            if (!node.children.has(char)) node.children.set(char, new TrieNode());
            node = node.children.get(char)!;
        }
        node.isEndOfWord = true;
    }
}
```
**Tushuntirish:** Trie tuzilmasi prefiks asosidagi qidiruv uchun eng samarali yechim bo'lib, lug'at hajmi qanchalik katta bo'lmasin, qidiruv tezligi faqat so'z uzunligiga bog'liq.

---

### Topshiriq #1064: Segment Tree yordamida Range Minimum Query (RMQ)
**Tavsif:** Sensor ma'lumotlari qatorida ma'lum vaqt oralig'idagi eng past qiymatni aniqlash.
**Talablar:** O(log N) vaqt murakkabligi, xotira samaradorligi.
**Yechim (JavaScript):**
```javascript
class SegmentTree {
    constructor(data) {
        this.n = data.length;
        this.tree = new Array(2 * this.n);
        for (let i = 0; i < this.n; i++) this.tree[this.n + i] = data[i];
        for (let i = this.n - 1; i > 0; i--) this.tree[i] = Math.min(this.tree[2 * i], this.tree[2 * i + 1]);
    }
    query(l, r) {
        let res = Infinity;
        for (l += this.n, r += this.n; l < r; l >>= 1, r >>= 1) {
            if (l & 1) res = Math.min(res, this.tree[l++]);
            if (r & 1) res = Math.min(res, this.tree[--r]);
        }
        return res;
    }
}
```
**Tushuntirish:** Segment Tree statik yoki dinamik ma'lumotlar to'plamida oraliq funksiyalarini (min, max, sum) bajarish uchun eng mos tuzilmadir.

---

### Topshiriq #1065: Graflarda sikllarni aniqlash (DFS)
**Tavsif:** Mikroxizmatlar arxitekturasida bog'liqliklar (dependency) orasida o'zaro bog'liqlik (deadlock) borligini tekshirish.
**Talablar:** O(V + E) vaqt murakkabligi, rekursiv xavfsizlik.
**Yechim (TypeScript):**
```typescript
function hasCycle(graph: Map<number, number[]>): boolean {
    const visited = new Set<number>();
    const recStack = new Set<number>();

    function dfs(node: number): boolean {
        visited.add(node);
        recStack.add(node);
        for (const neighbor of graph.get(node) || []) {
            if (!visited.has(neighbor) && dfs(neighbor)) return true;
            else if (recStack.has(neighbor)) return true;
        }
        recStack.delete(node);
        return false;
    }
    return Array.from(graph.keys()).some(node => !visited.has(node) && dfs(node));
}
```
**Tushuntirish:** Rekursiv stek (recStack) yordamida yo'naltirilgan grafdagi sikllarni aniqlash tizim barqarorligini ta'minlaydi.

---

### Topshiriq #1066: Trie yordamida IP-manzilni qidirish
**Tavsif:** Firewall tizimida IP-manzillarni prefiks bo'yicha bloklash yoki ruxsat berish.
**Talablar:** Bitwise operatsiyalar bilan ishlash, yuqori tezlik.
**Yechim (JavaScript):**
```javascript
class IPTrie {
    constructor() { this.root = {}; }
    insert(ip) {
        let node = this.root;
        for (let bit of ip) {
            if (!node[bit]) node[bit] = {};
            node = node[bit];
        }
        node.isEnd = true;
    }
}
```
**Tushuntirish:** IP manzillar ikkilik ko'rinishda Trie'ga joylashtirilsa, subnet maskalarni tekshirish juda tez amalga oshiriladi.

---

### Topshiriq #1067: Tarmoq oqimi (Max Flow - Edmonds-Karp)
**Tavsif:** Serverlar o'rtasida ma'lumot uzatish quvvatini (bandwidth) maksimal darajaga yetkazish.
**Talablar:** BFS algoritmi yordamida yo'l topish.
**Yechim (TypeScript):**
```typescript
function maxFlow(capacity: number[][], source: number, sink: number): number {
    let flow = 0;
    const parent = new Array(capacity.length);
    while (bfs(capacity, source, sink, parent)) {
        let pathFlow = Infinity;
        for (let v = sink; v !== source; v = parent[v]) pathFlow = Math.min(pathFlow, capacity[parent[v]][v]);
        for (let v = sink; v !== source; v = parent[v]) {
            capacity[parent[v]][v] -= pathFlow;
            capacity[v][parent[v]] += pathFlow;
        }
        flow += pathFlow;
    }
    return flow;
}
```
**Tushuntirish:** Edmonds-Karp algoritmi tarmoq o'tkazuvchanligini optimallashtirish uchun eng ishonchli yechimdir.

---

### Topshiriq #1068: Fenwick Tree bilan 2D massiv so'rovi
**Tavsif:** Tasvirni qayta ishlashda (image processing) piksel hududlari yig'indisini hisoblash.
**Talablar:** O(log N * log M) murakkablik.
**Yechim (JavaScript):**
```javascript
class FenwickTree2D {
    constructor(n, m) { this.tree = Array.from({length: n+1}, () => new Array(m+1).fill(0)); }
    update(r, c, val) {
        for (let i = r; i < this.tree.length; i += i & -i)
            for (let j = c; j < this.tree[0].length; j += j & -j) this.tree[i][j] += val;
    }
}
```
**Tushuntirish:** 2D Fenwick Tree matritsadagi sub-hududlar ustida operatsiyalarni bajarish uchun eng ixcham tuzilmadir.

---

### Topshiriq #1069: Kruskal algoritmi (Minimum Spanning Tree)
**Tavsif:** Shaharlararo optik tolali tarmoqni eng kam xarajat bilan ulash.
**Talablar:** Disjoint Set Union (DSU) ishlatilishi shart.
**Yechim (TypeScript):**
```typescript
class DSU {
    parent: number[];
    constructor(n: number) { this.parent = Array.from({length: n}, (_, i) => i); }
    find(i: number): number { return this.parent[i] === i ? i : (this.parent[i] = this.find(this.parent[i])); }
    union(i: number, j: number) { this.parent[this.find(i)] = this.find(j); }
}
```
**Tushuntirish:** Kruskal algoritmi DSU bilan birgalikda tarmoq infratuzilmasini qurishda xarajatlarni minimallashtirish uchun ishlatiladi.

---

### Topshiriq #1070: Segment Tree bilan Lazy Propagation
**Tavsif:** Katta massivda oraliq qiymatlarini ommaviy yangilash (masalan, narxlarni foizli o'zgartirish).
**Talablar:** O(log N) yangilash vaqti.
**Yechim (JavaScript):**
```javascript
class LazySegmentTree {
    updateRange(node, start, end, l, r, val) {
        if (this.lazy[node] !== 0) {
            this.tree[node] += (end - start + 1) * this.lazy[node];
            if (start !== end) { this.lazy[2*node] += this.lazy[node]; this.lazy[2*node+1] += this.lazy[node]; }
            this.lazy[node] = 0;
        }
        // Qo'shimcha mantiq...
    }
}
```
**Tushuntirish:** Lazy propagation oraliq yangilash operatsiyalarini kechiktirib, samaradorlikni keskin oshiradi.

---

### Topshiriq #1071: Tarmoq topologiyasida eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Katta hajmdagi serverlararo aloqa tarmog'ida ma'lumotlar paketini eng kam kechikish (latency) bilan yetkazish.
**Talablar:** `PriorityQueue` yordamida $O(E \log V)$ murakkablikda ishlash, xavfsiz tugunlar validatsiyasi.
**Yechim (TypeScript):**
```typescript
class Graph {
  adj: Map<number, { node: number; weight: number }[]> = new Map();
  addEdge(u: number, v: number, w: number) {
    if (!this.adj.has(u)) this.adj.set(u, []);
    this.adj.get(u)!.push({ node: v, weight: w });
  }
  // Dijkstra algoritmi
  findShortestPath(start: number, end: number): number {
    const dists = new Map<number, number>();
    const pq = [[0, start]]; // Oddiy navbat, ishlab chiqarishda Binary Heap tavsiya etiladi
    dists.set(start, 0);
    while (pq.length > 0) {
      pq.sort((a, b) => a[0] - b[0]);
      const [d, u] = pq.shift()!;
      if (u === end) return d;
      for (const edge of this.adj.get(u) || []) {
        const newDist = d + edge.weight;
        if (newDist < (dists.get(edge.node) ?? Infinity)) {
          dists.set(edge.node, newDist);
          pq.push([newDist, edge.node]);
        }
      }
    }
    return -1;
  }
}
```
**Tushuntirish:** Dijkstra algoritmi tarmoq kechikishlarini minimallashtirish uchun eng samarali yechimdir.

### Topshiriq #1072: Dinamik massivda diapazon yig'indisini hisoblash (Fenwick Tree)
**Tavsif:** Moliya tizimlarida real vaqt rejimida tranzaksiyalar yig'indisini kuzatish.
**Talablar:** Yangilash va so'rovlar uchun $O(\log N)$ vaqt murakkabligi.
**Yechim (JavaScript):**
```javascript
class FenwickTree {
  constructor(size) { this.tree = new Array(size + 1).fill(0); }
  update(i, delta) {
    for (; i < this.tree.length; i += i & -i) this.tree[i] += delta;
  }
  query(i) {
    let sum = 0;
    for (; i > 0; i -= i & -i) sum += this.tree[i];
    return sum;
  }
}
```
**Tushuntirish:** Fenwick Tree (Binary Indexed Tree) xotira tejamkorligi va tezligi tufayli yuqori yuklamali tizimlar uchun ideal.

### Topshiriq #1073: Avtomatik to'ldirish tizimi (Trie)
**Tavsif:** Foydalanuvchi qidiruv so'rovlarini tezkor bashorat qilish.
**Talablar:** Prefiks bo'yicha qidiruv $O(L)$ vaqtda (L - so'z uzunligi).
**Yechim (TypeScript):**
```typescript
class TrieNode {
  children: Map<string, TrieNode> = new Map();
  isEndOfWord: boolean = false;
}
class Trie {
  root = new TrieNode();
  insert(word: string) {
    let node = this.root;
    for (const char of word) {
      if (!node.children.has(char)) node.children.set(char, new TrieNode());
      node = node.children.get(char)!;
    }
    node.isEndOfWord = true;
  }
}
```
**Tushuntirish:** Trie tuzilmasi lug'at qidiruvini chiziqli vaqtda amalga oshirish imkonini beradi.

### Topshiriq #1074: Diapazon bo'yicha eng katta qiymatni topish (Segment Tree)
**Tavsif:** Sensor ma'lumotlari oqimida eng yuqori ko'rsatkichni aniqlash.
**Talablar:** $O(\log N)$ vaqt murakkabligi, xotira xavfsizligi.
**Yechim (JavaScript):**
```javascript
class SegmentTree {
  constructor(data) {
    this.n = data.length;
    this.tree = new Array(2 * this.n);
    for (let i = 0; i < this.n; i++) this.tree[this.n + i] = data[i];
    for (let i = this.n - 1; i > 0; i--) this.tree[i] = Math.max(this.tree[2 * i], this.tree[2 * i + 1]);
  }
  query(l, r) {
    let res = -Infinity;
    for (l += this.n, r += this.n; l < r; l >>= 1, r >>= 1) {
      if (l & 1) res = Math.max(res, this.tree[l++]);
      if (r & 1) res = Math.max(res, this.tree[--r]);
    }
    return res;
  }
}
```
**Tushuntirish:** Segment Tree statik va dinamik diapazon so'rovlari uchun eng tezkor ma'lumotlar strukturasi hisoblanadi.

### Topshiriq #1075: Graflarda sikllarni aniqlash (DFS)
**Tavsif:** Mikroxizmatlar bog'liqliklarida (dependency) o'zaro bog'liqlik (deadlock) xavfini aniqlash.
**Talablar:** $O(V+E)$ vaqt murakkabligi, rekursiv chuqurlikni nazorat qilish.
**Yechim (TypeScript):**
```typescript
function hasCycle(graph: Map<number, number[]>): boolean {
  const visited = new Set<number>();
  const recStack = new Set<number>();
  const dfs = (node: number): boolean => {
    visited.add(node);
    recStack.add(node);
    for (const neighbor of graph.get(node) || []) {
      if (!visited.has(neighbor) && dfs(neighbor)) return true;
      else if (recStack.has(neighbor)) return true;
    }
    recStack.delete(node);
    return false;
  };
  return false; // Loop orqali barcha tugunlar tekshiriladi
}
```
**Tushuntirish:** DFS orqali rekursiv stekni kuzatish sikllarni aniqlashning standart usulidir.

### Topshiriq #1076: Kenglik bo'yicha qidiruv (BFS)
**Tavsif:** Ijtimoiy tarmoqlarda "do'stlik darajasi"ni (degree of separation) aniqlash.
**Talablar:** Eng qisqa yo'lni topish, xotira sarfini optimallashtirish.
**Yechim (JavaScript):**
```javascript
function bfs(graph, start, target) {
  const queue = [[start, 0]];
  const visited = new Set([start]);
  while (queue.length > 0) {
    const [node, dist] = queue.shift();
    if (node === target) return dist;
    for (const neighbor of graph[node]) {
      if (!visited.has(neighbor)) {
        visited.add(neighbor);
        queue.push([neighbor, dist + 1]);
      }
    }
  }
  return -1;
}
```
**Tushuntirish:** BFS vaznsiz graflarda eng qisqa yo'lni topish uchun eng ishonchli algoritmdir.

### Topshiriq #1077: Trie yordamida so'zlar chastotasini hisoblash
**Tavsif:** Katta matnlar bazasida so'zlarning takrorlanishini hisoblash.
**Talablar:** Xotirani tejash uchun Trie tugunlarida `count` maydonini saqlash.
**Yechim (TypeScript):**
```typescript
class FreqTrieNode {
  children: Map<string, FreqTrieNode> = new Map();
  count: number = 0;
}
// Insert va getCount funksiyalari bilan amalga oshiriladi
```
**Tushuntirish:** Trie tuzilmasi so'zlarni prefiks bo'yicha guruhlab, qidiruvni tezlashtiradi.

### Topshiriq #1078: Fenwick Tree yordamida 2D massivni yangilash
**Tavsif:** Tasvirni qayta ishlashda (image processing) piksel qiymatlarini tezkor o'zgartirish.
**Talablar:** $O(\log N \cdot \log M)$ vaqt murakkabligi.
**Yechim (JavaScript):**
```javascript
// 2D Fenwick Tree implementatsiyasi
class FenwickTree2D {
  constructor(rows, cols) { this.tree = Array.from({length: rows+1}, () => new Array(cols+1).fill(0)); }
  update(r, c, val) {
    for (let i = r; i < this.tree.length; i += i & -i)
      for (let j = c; j < this.tree[0].length; j += j & -j) this.tree[i][j] += val;
  }
}
```
**Tushuntirish:** 2D Fenwick Tree matritsali ma'lumotlar ustida tezkor operatsiyalar bajarish uchun juda samarali.

### Topshiriq #1079: Topologik tartiblash (Kahn algoritmi)
**Tavsif:** Loyiha vazifalarini bajarish ketma-ketligini (task scheduling) aniqlash.
**Talablar:** Sikllarni aniqlash va tartibni qaytarish.
**Yechim (TypeScript):**
```typescript
function topologicalSort(numTasks: number, adj: number[][]): number[] {
  const inDegree = new Array(numTasks).fill(0);
  adj.forEach(neighbors => neighbors.forEach(v => inDegree[v]++));
  const queue = inDegree.map((d, i) => d === 0 ? i : -1).filter(i => i !== -1);
  const result: number[] = [];
  while (queue.length) {
    const u = queue.shift()!;
    result.push(u);
    adj[u].forEach(v => { if (--inDegree[v] === 0) queue.push(v); });
  }
  return result;
}
```
**Tushuntirish:** Kahn algoritmi vazifalar o'rtasidagi bog'liqlikni chiziqli vaqtda hal qiladi.

### Topshiriq #1080: Segment Tree Lazy Propagation
**Tavsif:** Katta vaqt intervallarida o'zgaruvchan ma'lumotlar bazasini yangilash.
**Talablar:** $O(\log N)$ vaqtda diapazonni yangilash.
**Yechim (JavaScript):**
```javascript
// Lazy propagation bilan Segment Tree
class LazySegmentTree {
  // Yangilash vaqtida qiymatlarni kechiktirib (lazy) hisoblash
  updateRange(node, start, end, l, r, val) {
    if (this.lazy[node] !== 0) {
      this.tree[node] += (end - start + 1) * this.lazy[node];
      if (start !== end) {
        this.lazy[2 * node] += this.lazy[node];
        this.lazy[2 * node + 1] += this.lazy[node];
      }
      this.lazy[node] = 0;
    }
    // ... qolgan mantiq
  }
}
```
**Tushuntirish:** Lazy propagation katta diapazonlarni bir vaqtning o'zida yangilash uchun eng maqbul optimizatsiya usulidir.

---

### Topshiriq #1081: Tarmoq topologiyasida eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Katta hajmdagi serverlararo aloqa tarmog'ida ma'lumotlar paketini eng kam kechikish bilan uzatish uchun eng qisqa yo'lni aniqlash.
**Talablar:** O(E log V) murakkablik, xotira xavfsizligi va manfiy bo'lmagan og'irliklar bilan ishlash.
**Yechim (TypeScript):**
```typescript
class Graph {
  adj: Map<number, { node: number, weight: number }[]> = new Map();
  addEdge(u: number, v: number, w: number) {
    if (!this.adj.has(u)) this.adj.set(u, []);
    this.adj.get(u)!.push({ node: v, weight: w });
  }
  dijkstra(start: number): Map<number, number> {
    const dists = new Map<number, number>();
    const pq = [{ node: start, dist: 0 }];
    dists.set(start, 0);
    while (pq.length > 0) {
      pq.sort((a, b) => a.dist - b.dist);
      const { node, dist } = pq.shift()!;
      for (const edge of this.adj.get(node) || []) {
        const newDist = dist + edge.weight;
        if (newDist < (dists.get(edge.node) ?? Infinity)) {
          dists.set(edge.node, newDist);
          pq.push({ node: edge.node, dist: newDist });
        }
      }
    }
    return dists;
  }
}
```
**Tushuntirish:** Dijkstra algoritmi tarmoq kechikishlarini minimallashtirish uchun eng samarali yondashuvdir.

### Topshiriq #1082: Dinamik oraliq yig'indisi (Fenwick Tree)
**Tavsif:** Real vaqt rejimida moliyaviy tranzaksiyalar oqimida ma'lum vaqt oralig'idagi yig'indini tezkor hisoblash.
**Talablar:** O(log N) yangilash va so'rov tezligi.
**Yechim (JavaScript):**
```javascript
class FenwickTree {
  constructor(size) { this.tree = new Array(size + 1).fill(0); }
  update(i, delta) {
    for (; i < this.tree.length; i += i & -i) this.tree[i] += delta;
  }
  query(i) {
    let sum = 0;
    for (; i > 0; i -= i & -i) sum += this.tree[i];
    return sum;
  }
}
```
**Tushuntirish:** Fenwick Tree (Binary Indexed Tree) xotira tejamkorligi va tezligi tufayli yuqori chastotali moliya tizimlarida qo'llaniladi.

### Topshiriq #1083: Avtomatik to'ldirish tizimi (Trie)
**Tavsif:** Foydalanuvchi qidiruv so'rovlarini tezkor avtomatik to'ldirish uchun lug'at bazasini saqlash.
**Talablar:** Prefiks bo'yicha qidiruv O(L) murakkablikda (L - so'z uzunligi).
**Yechim (TypeScript):**
```typescript
class TrieNode {
  children: Map<string, TrieNode> = new Map();
  isEnd: boolean = false;
}
class Trie {
  root = new TrieNode();
  insert(word: string) {
    let node = this.root;
    for (const char of word) {
      if (!node.children.has(char)) node.children.set(char, new TrieNode());
      node = node.children.get(char)!;
    }
    node.isEnd = true;
  }
}
```
**Tushuntirish:** Trie tuzilmasi prefiks qidiruvlari uchun eng optimal xotira va vaqt samaradorligini ta'minlaydi.

### Topshiriq #1084: Oraliqdagi maksimal qiymat (Segment Tree)
**Tavsif:** Sensor ma'lumotlari massivida ma'lum vaqt oralig'idagi eng yuqori haroratni aniqlash.
**Talablar:** O(log N) murakkablikdagi diapazonli so'rovlar.
**Yechim (JavaScript):**
```javascript
class SegmentTree {
  constructor(data) {
    this.n = data.length;
    this.tree = new Array(2 * this.n);
    for (let i = 0; i < this.n; i++) this.tree[this.n + i] = data[i];
    for (let i = this.n - 1; i > 0; i--) this.tree[i] = Math.max(this.tree[2 * i], this.tree[2 * i + 1]);
  }
  query(l, r) {
    let res = -Infinity;
    for (l += this.n, r += this.n; l < r; l >>= 1, r >>= 1) {
      if (l & 1) res = Math.max(res, this.tree[l++]);
      if (r & 1) res = Math.max(res, this.tree[--r]);
    }
    return res;
  }
}
```
**Tushuntirish:** Segment Tree statik va dinamik massivlarda diapazonli so'rovlar uchun eng mos keladi.

### Topshiriq #1085: Grafda bog'liqlik komponentlarini topish (DFS)
**Tavsif:** Ijtimoiy tarmoq foydalanuvchilari orasidagi o'zaro bog'liq guruhlarni (klasterlarni) aniqlash.
**Talablar:** O(V + E) murakkablik, rekursiv xavfsizlik.
**Yechim (TypeScript):**
```typescript
function findComponents(adj: Map<number, number[]>): number {
  const visited = new Set<number>();
  let count = 0;
  for (const node of adj.keys()) {
    if (!visited.has(node)) {
      count++;
      const stack = [node];
      while (stack.length) {
        const curr = stack.pop()!;
        if (!visited.has(curr)) {
          visited.add(curr);
          adj.get(curr)?.forEach(neighbor => stack.push(neighbor));
        }
      }
    }
  }
  return count;
}
```
**Tushuntirish:** DFS (Depth First Search) iterativ yondashuvi stack overflow xavfini oldini oladi va katta graflarda barqaror ishlaydi.

### Topshiriq #1086: Kengaytirilgan Trie (Autocomplete with frequency)
**Tavsif:** Qidiruv so'rovlarini chastotasiga ko'ra saralab ko'rsatish.
**Talablar:** Har bir tugunda chastota hisoblagichini saqlash.
**Yechim (JavaScript):**
```javascript
class TrieNode {
  constructor() { this.children = {}; this.freq = 0; }
}
// Qo'shimcha mantiq: insert paytida freq ni oshirish va qidiruvda saralash.
```
**Tushuntirish:** Chastota ma'lumotlarini Trie tugunlarida saqlash qidiruv natijalarini foydalanuvchi uchun moslashtirishga yordam beradi.

### Topshiriq #1087: Minimal qamrovchi daraxt (Kruskal)
**Tavsif:** Shaharlararo optik tolali kabel yotqizishda eng kam xarajatli tarmoqni loyihalash.
**Talablar:** Disjoint Set Union (DSU) yordamida O(E log E) murakkablik.
**Yechim (TypeScript):**
```typescript
class DSU {
  parent: number[];
  constructor(n: number) { this.parent = Array.from({length: n}, (_, i) => i); }
  find(i: number): number { return this.parent[i] === i ? i : (this.parent[i] = this.find(this.parent[i])); }
  union(i: number, j: number) { this.parent[this.find(i)] = this.find(j); }
}
```
**Tushuntirish:** Kruskal algoritmi DSU bilan birgalikda tarmoq infratuzilmasini optimallashtirishda eng samarali hisoblanadi.

### Topshiriq #1088: Lazy Propagation (Segment Tree)
**Tavsif:** Katta massivda oraliq qiymatlarini ommaviy yangilash (masalan, narxlarni 10% ga oshirish).
**Talablar:** O(log N) murakkablikdagi yangilash operatsiyasi.
**Yechim (JavaScript):**
```javascript
// Lazy array qo'shish orqali yangilanishlarni kechiktirib bajarish.
// Bu operatsiyalar sonini keskin kamaytiradi.
```
**Tushuntirish:** Lazy propagation katta hajmdagi ma'lumotlar to'plamida yozish operatsiyalarini optimallashtiradi.

### Topshiriq #1089: Topologik tartiblash (Kahn algoritmi)
**Tavsif:** Loyiha vazifalari orasidagi bog'liqlikni (dependency) hisobga olgan holda bajarilish ketma-ketligini aniqlash.
**Talablar:** O(V + E) murakkablik, sikllarni aniqlash.
**Yechim (TypeScript):**
```typescript
function topologicalSort(n: number, adj: number[][]): number[] {
  const inDegree = new Array(n).fill(0);
  adj.forEach(neighbors => neighbors.forEach(v => inDegree[v]++));
  const queue = inDegree.map((d, i) => d === 0 ? i : -1).filter(i => i !== -1);
  const result: number[] = [];
  while (queue.length) {
    const u = queue.shift()!;
    result.push(u);
    adj[u].forEach(v => { if (--inDegree[v] === 0) queue.push(v); });
  }
  return result;
}
```
**Tushuntirish:** Kahn algoritmi vazifalar ketma-ketligini aniqlashda eng xavfsiz va tushunarli yondashuvdir.

### Topshiriq #1090: Fenwick Tree 2D (Matritsalar uchun)
**Tavsif:** 2D tasvir (image) piksel qiymatlari yig'indisini tezkor hisoblash.
**Talablar:** O(log N * log M) murakkablik.
**Yechim (JavaScript):**
```javascript
class FenwickTree2D {
  constructor(n, m) { this.tree = Array.from({length: n+1}, () => new Array(m+1).fill(0)); }
  update(r, c, val) {
    for (let i = r; i < this.tree.length; i += i & -i)
      for (let j = c; j < this.tree[0].length; j += j & -j) this.tree[i][j] += val;
  }
}
```
**Tushuntirish:** 2D Fenwick Tree matritsali ma'lumotlar bilan ishlashda 2D segment tree'ga qaraganda xotira jihatidan ancha samarali.

---

### Topshiriq #1091: Tarmoq topologiyasida eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Katta hajmdagi serverlararo aloqa tarmog'ida ma'lumotlar paketini eng kam kechikish bilan yetkazish.
**Talablar:** `PriorityQueue` yordamida $O(E \log V)$ murakkablikda ishlash.
**Yechim (TypeScript):**
```typescript
class PriorityQueue {
  private heap: { node: number, dist: number }[] = [];
  push(val: { node: number, dist: number }) { this.heap.push(val); this.heap.sort((a, b) => a.dist - b.dist); }
  pop() { return this.heap.shift(); }
  isEmpty() { return this.heap.length === 0; }
}

function findShortestPath(graph: Map<number, {to: number, weight: number}[]>, start: number): number[] {
  const dists = new Array(1000).fill(Infinity);
  dists[start] = 0;
  const pq = new PriorityQueue();
  pq.push({ node: start, dist: 0 });
  while (!pq.isEmpty()) {
    const { node, dist } = pq.pop()!;
    for (const edge of graph.get(node) || []) {
      if (dists[node] + edge.weight < dists[edge.to]) {
        dists[edge.to] = dists[node] + edge.weight;
        pq.push({ node: edge.to, dist: dists[edge.to] });
      }
    }
  }
  return dists;
}
```
**Tushuntirish:** Dijkstra algoritmi tarmoq kechikishlarini minimallashtirish uchun eng samarali yechimdir.

### Topshiriq #1092: Dinamik oraliq yig'indisi (Segment Tree)
**Tavsif:** Moliya tizimida real vaqt rejimida tranzaksiyalar yig'indisini hisoblash.
**Talablar:** Yangilash va so'rovlar uchun $O(\log N)$ vaqt murakkabligi.
**Yechim (JavaScript):**
```javascript
class SegmentTree {
  constructor(arr) { this.n = arr.length; this.tree = new Array(2 * this.n); this.build(arr); }
  build(arr) { for (let i = 0; i < this.n; i++) this.tree[this.n + i] = arr[i];
    for (let i = this.n - 1; i > 0; i--) this.tree[i] = this.tree[2 * i] + this.tree[2 * i + 1]; }
  update(i, val) { for (this.tree[i += this.n] = val; i > 1; i >>= 1) this.tree[i >> 1] = this.tree[i] + this.tree[i ^ 1]; }
  query(l, r) { let res = 0; for (l += this.n, r += this.n; l < r; l >>= 1, r >>= 1) {
    if (l & 1) res += this.tree[l++]; if (r & 1) res += this.tree[--r]; } return res; }
}
```
**Tushuntirish:** Segment Tree massivdagi o'zgarishlarni tezkor kuzatish va oraliq yig'indilarni hisoblash uchun optimaldir.

### Topshiriq #1093: Fenwick Tree yordamida chastotali tahlil
**Tavsif:** Foydalanuvchi harakatlari ketma-ketligida voqealar chastotasini hisoblash.
**Talablar:** Xotira tejamkorligi va $O(\log N)$ operatsiyalar.
**Yechim (TypeScript):**
```typescript
class FenwickTree {
  private tree: number[];
  constructor(size: number) { this.tree = new Array(size + 1).fill(0); }
  update(i: number, delta: number) { for (; i < this.tree.length; i += i & -i) this.tree[i] += delta; }
  query(i: number): number { let sum = 0; for (; i > 0; i -= i & -i) sum += this.tree[i]; return sum; }
}
```
**Tushuntirish:** Fenwick Tree (Binary Indexed Tree) Segment Tree'ga qaraganda kamroq xotira talab qiladi va kodlash osonroq.

### Topshiriq #1094: Trie (Prefix Tree) bilan avtomatik to'ldirish
**Tavsif:** Qidiruv tizimlarida kalit so'zlarni tezkor taklif qilish.
**Talablar:** $O(L)$ vaqt murakkabligi (L - so'z uzunligi).
**Yechim (JavaScript):**
```javascript
class TrieNode { constructor() { this.children = {}; this.isEnd = false; } }
class Trie {
  constructor() { this.root = new TrieNode(); }
  insert(word) { let node = this.root; for (let char of word) {
    if (!node.children[char]) node.children[char] = new TrieNode(); node = node.children[char]; } node.isEnd = true; }
  search(prefix) { let node = this.root; for (let char of prefix) {
    if (!node.children[char]) return false; node = node.children[char]; } return true; }
}
```
**Tushuntirish:** Trie tuzilmasi prefiks asosida qidiruvni juda tez amalga oshiradi.

### Topshiriq #1095: Graflarda sikllarni aniqlash (DFS)
**Tavsif:** Tizim bog'liqliklarida (dependencies) halqali bog'liqliklar (deadlock) mavjudligini tekshirish.
**Talablar:** Rekursiv yondashuv, $O(V + E)$ murakkablik.
**Yechim (TypeScript):**
```typescript
function hasCycle(graph: Map<number, number[]>, visited: Set<number>, recStack: Set<number>, node: number): boolean {
  visited.add(node); recStack.add(node);
  for (const neighbor of graph.get(node) || []) {
    if (!visited.has(neighbor) && hasCycle(graph, visited, recStack, neighbor)) return true;
    else if (recStack.has(neighbor)) return true;
  }
  recStack.delete(node); return false;
}
```
**Tushuntirish:** `recStack` yordamida joriy rekursiya yo'lidagi tugunlarni kuzatish siklni aniqlashning standart usulidir.

### Topshiriq #1096: Katta ma'lumotlar to'plamida eng yaqin qo'shni (K-D Tree)
**Tavsif:** Geolokatsiya ma'lumotlari asosida eng yaqin obyektni topish.
**Talablar:** Ko'p o'lchovli fazoda qidiruvni optimallashtirish.
**Yechim (JavaScript):**
```javascript
class KDNode { constructor(point, axis) { this.point = point; this.left = null; this.right = null; this.axis = axis; } }
// K-D Tree qurish va qidirish logikasi (qisqartirilgan)
function buildKDTree(points, depth = 0) {
  if (points.length === 0) return null;
  const axis = depth % 2;
  points.sort((a, b) => a[axis] - b[axis]);
  const mid = Math.floor(points.length / 2);
  const node = new KDNode(points[mid], axis);
  node.left = buildKDTree(points.slice(0, mid), depth + 1);
  node.right = buildKDTree(points.slice(mid + 1), depth + 1);
  return node;
}
```
**Tushuntirish:** K-D Tree fazoviy ma'lumotlarni qidirishda chiziqli qidiruvdan $O(\log N)$ barobar tezroq ishlaydi.

### Topshiriq #1097: Tarmoq oqimini optimallashtirish (Ford-Fulkerson)
**Tavsif:** Logistika tarmog'ida maksimal yuk tashish qobiliyatini aniqlash.
**Talablar:** BFS (Edmonds-Karp) algoritmi bilan amalga oshirish.
**Yechim (TypeScript):**
```typescript
function bfs(capacity: number[][], source: number, sink: number, parent: number[]): boolean {
  const visited = new Array(capacity.length).fill(false);
  const queue = [source]; visited[source] = true;
  while (queue.length > 0) {
    const u = queue.shift()!;
    for (let v = 0; v < capacity.length; v++) {
      if (!visited[v] && capacity[u][v] > 0) {
        parent[v] = u; visited[v] = true; queue.push(v);
      }
    }
  }
  return visited[sink];
}
```
**Tushuntirish:** Edmonds-Karp algoritmi maksimal oqimni topishda barqarorlikni ta'minlaydi.

### Topshiriq #1098: Union-Find (Disjoint Set Union)
**Tavsif:** Ijtimoiy tarmoqlarda do'stlar guruhini (klasterlarni) birlashtirish.
**Talablar:** `Path Compression` va `Union by Rank` optimizatsiyasi.
**Yechim (JavaScript):**
```javascript
class DSU {
  constructor(n) { this.parent = Array.from({length: n}, (_, i) => i); }
  find(i) { if (this.parent[i] === i) return i; return this.parent[i] = this.find(this.parent[i]); }
  union(i, j) { let rootI = this.find(i); let rootJ = this.find(j); if (rootI !== rootJ) this.parent[rootI] = rootJ; }
}
```
**Tushuntirish:** `Path Compression` yordamida `find` operatsiyasi deyarli $O(1)$ vaqtda bajariladi.

### Topshiriq #1099: Trie yordamida IP-manzilni qidirish (Longest Prefix Match)
**Tavsif:** Routerlarda paketlarni yo'naltirish jadvalini optimallashtirish.
**Talablar:** Bit darajasida Trie tuzilmasidan foydalanish.
**Yechim (TypeScript):**
```typescript
class BitTrieNode { children: [BitTrieNode | null, BitTrieNode | null] = [null, null]; }
function insertIP(root: BitTrieNode, bits: string) {
  let curr = root;
  for (const bit of bits) {
    const b = parseInt(bit);
    if (!curr.children[b]) curr.children[b] = new BitTrieNode();
    curr = curr.children[b]!;
  }
}
```
**Tushuntirish:** IP marshrutlashda eng uzun prefiks mosligini topish uchun bitli Trie eng tezkor usuldir.

### Topshiriq #1100: Tarmoq markazini topish (Floyd-Warshall)
**Tavsif:** Shahar infratuzilmasida eng optimal markazni (barcha nuqtalarga masofa minimal) aniqlash.
**Talablar:** $O(V^3)$ murakkablikda barcha juftliklar uchun masofani hisoblash.
**Yechim (JavaScript):**
```javascript
function floydWarshall(graph) {
  const dist = graph.map(row => [...row]);
  const n = graph.length;
  for (let k = 0; k < n; k++) {
    for (let i = 0; i < n; i++) {
      for (let j = 0; j < n; j++) {
        if (dist[i][k] + dist[k][j] < dist[i][j]) dist[i][j] = dist[i][k] + dist[k][j];
      }
    }
  }
  return dist;
}
```
**Tushuntirish:** Floyd-Warshall kichik va o'rta o'lchamdagi graflarda barcha yo'llarni aniqlash uchun eng qulay algoritmdir.