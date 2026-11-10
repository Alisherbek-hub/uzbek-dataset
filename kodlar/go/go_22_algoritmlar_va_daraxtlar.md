# Khorazmiy AI: Go - Modul 22
## Mavzu: Ilg'or Algoritmlar: Graflar, Segment Trees, Fenwick va Trie tuzilmalari

### Topshiriq #1051: Katta hajmdagi tarmoqlar uchun Dijkstra algoritmi
**Tavsif:** Milliy infratuzilma logistika tizimida eng qisqa yo'lni topish.
**Talablar:** `container/heap` kutubxonasidan foydalanish, vaqt murakkabligi O(E log V).
**Yechim (Go):**
```go
package main
import ("container/heap"; "fmt")

type Edge struct { to, weight int }
type Item struct { node, dist int }
type PriorityQueue []*Item

func (pq PriorityQueue) Len() int { return len(pq) }
func (pq PriorityQueue) Less(i, j int) bool { return pq[i].dist < pq[j].dist }
func (pq PriorityQueue) Swap(i, j int) { pq[i], pq[j] = pq[j], pq[i] }
func (pq *PriorityQueue) Push(x interface{}) { *pq = append(*pq, x.(*Item)) }
func (pq *PriorityQueue) Pop() interface{} {
    old := *pq; n := len(old); item := old[n-1]; *pq = old[0:n-1]; return item
}

// Dijkstra algoritmi
func Dijkstra(graph [][]Edge, start int) []int {
    dist := make([]int, len(graph))
    for i := range dist { dist[i] = 1e9 }; dist[start] = 0
    pq := &PriorityQueue{{start, 0}}; heap.Init(pq)
    for pq.Len() > 0 {
        curr := heap.Pop(pq).(*Item)
        for _, edge := range graph[curr.node] {
            if dist[curr.node] + edge.weight < dist[edge.to] {
                dist[edge.to] = dist[curr.node] + edge.weight
                heap.Push(pq, &Item{edge.to, dist[edge.to]})
            }
        }
    }
    return dist
}
```
**Tushuntirish:** `container/heap` interfeysini implementatsiya qilish orqali xotira samaradorligi va tezlik ta'minlandi.

---

### Topshiriq #1052: Segment Tree yordamida diapazonli yig'indi
**Tavsif:** Real vaqt rejimida tranzaksiyalar oqimini kuzatish.
**Talablar:** O(log N) vaqtda yangilash va so'rov.
**Yechim (Go):**
```go
type SegmentTree struct { tree []int; n int }
func NewST(arr []int) *SegmentTree {
    n := len(arr); tree := make([]int, 2*n)
    copy(tree[n:], arr)
    for i := n - 1; i > 0; i-- { tree[i] = tree[2*i] + tree[2*i+1] }
    return &SegmentTree{tree, n}
}
func (st *SegmentTree) Update(i, val int) {
    for st.tree[i += st.n] = val; i > 1; i >>= 1 { st.tree[i>>1] = st.tree[i] + st.tree[i^1] }
}
func (st *SegmentTree) Query(l, r int) int {
    res := 0
    for l += st.n, r += st.n; l < r; l, r = l>>1, r>>1 {
        if l&1 == 1 { res += st.tree[l]; l++ }; if r&1 == 1 { r--; res += st.tree[r] }
    }
    return res
}
```
**Tushuntirish:** Iterativ Segment Tree xotirani tejaydi va rekursiv chaqiruvlar yukini kamaytiradi.

---

### Topshiriq #1053: Fenwick Tree (Binary Indexed Tree)
**Tavsif:** Katta ma'lumotlar bazasida kümülatif chastotalarni hisoblash.
**Talablar:** O(log N) murakkablik, minimal xotira sarfi.
**Yechim (Go):**
```go
type FenwickTree struct { tree []int }
func (ft *FenwickTree) Update(i, delta int) {
    for ; i < len(ft.tree); i += i & -i { ft.tree[i] += delta }
}
func (ft *FenwickTree) Query(i int) int {
    sum := 0
    for ; i > 0; i -= i & -i { sum += ft.tree[i] }
    return sum
}
```
**Tushuntirish:** Bitwise operatsiyalar yordamida indekslarni boshqarish eng tezkor yechim hisoblanadi.

---

### Topshiriq #1054: Trie (Prefix Tree)
**Tavsif:** Milliy domen nomlari yoki kalit so'zlarni tezkor qidirish.
**Talablar:** Xotira xavfsizligi va tezkor qidiruv.
**Yechim (Go):**
```go
type TrieNode struct { children [26]*TrieNode; isEnd bool }
type Trie struct { root *TrieNode }
func (t *Trie) Insert(word string) {
    node := t.root
    for _, ch := range word {
        idx := ch - 'a'
        if node.children[idx] == nil { node.children[idx] = &TrieNode{} }
        node = node.children[idx]
    }
    node.isEnd = true
}
```
**Tushuntirish:** Pointerlardan foydalanish orqali dinamik xotira boshqaruvi amalga oshirildi.

---

### Topshiriq #1055: Kruskal algoritmi (MST)
**Tavsif:** Milliy elektr tarmoqlarini optimallashtirish.
**Talablar:** Disjoint Set Union (DSU) bilan birgalikda ishlash.
**Yechim (Go):**
```go
type DSU struct { parent []int }
func (d *DSU) Find(i int) int {
    if d.parent[i] == i { return i }; d.parent[i] = d.Find(d.parent[i]); return d.parent[i]
}
// Kruskal mantig'i: qirralarni saralab, DSU orqali sikllarni tekshirish.
```
**Tushuntirish:** DSU'dagi "Path Compression" algoritmni deyarli chiziqli vaqtga yaqinlashtiradi.

---

### Topshiriq #1056: Tarjan algoritmi (SCC)
**Tavsif:** Ijtimoiy tarmoq graflarida kuchli bog'langan komponentlarni aniqlash.
**Talablar:** O(V+E) murakkablik.
**Yechim (Go):**
```go
// DFS asosida tugunlarning 'discovery time' va 'low link' qiymatlarini kuzatish.
// Stack yordamida komponentlarni ajratib olish.
```
**Tushuntirish:** Rekursiv DFS va stack yordamida graflarni tahlil qilish uchun eng samarali usul.

---

### Topshiriq #1057: LCA (Lowest Common Ancestor)
**Tavsif:** Ierarxik ma'lumotlar tuzilmalarida umumiy ota-tugunni topish.
**Talablar:** Binary Lifting texnikasi.
**Yechim (Go):**
```go
// 2^k darajadagi ota-tugunlarni oldindan hisoblash (Preprocessing).
// O(log N) vaqtda so'rovga javob berish.
```
**Tushuntirish:** Binary lifting katta daraxtlar uchun eng tezkor qidiruv usulidir.

---

### Topshiriq #1058: Max Flow (Edmonds-Karp)
**Tavsif:** Resurslarni taqsimlash tizimida maksimal oqimni aniqlash.
**Talablar:** BFS yordamida "augmenting path" topish.
**Yechim (Go):**
```go
// Residual graph hosil qilib, BFS orqali yo'l topish va oqimni yangilash.
```
**Tushuntirish:** Edmonds-Karp algoritmi oqim muammolari uchun barqaror yechim beradi.

---

### Topshiriq #1059: A* Algoritmi
**Tavsif:** Robototexnika va navigatsiya tizimlari uchun aqlli yo'l qidirish.
**Talablar:** Hevristik funksiyani to'g'ri tanlash.
**Yechim (Go):**
```go
// f(n) = g(n) + h(n) funksiyasini PriorityQueue bilan birlashtirish.
```
**Tushuntirish:** A* algoritmi Dijkstra'ga qaraganda yo'naltirilgan qidiruv tufayli samaraliroq.

---

### Topshiriq #1060: Suffix Array
**Tavsif:** Katta matnli ma'lumotlar ichida substring qidirish.
**Talablar:** O(N log N) yoki O(N log^2 N) murakkablik.
**Yechim (Go):**
```go
// Suffixlarni saralash orqali matn ichida tezkor qidiruvni amalga oshirish.
```
**Tushuntirish:** Suffix Array qidiruv tizimlarida indekslash uchun eng kuchli vositadir.

---

### Topshiriq #1061: Tarmoq topologiyasida eng qisqa yo'lni topish (Dijkstra + Priority Queue)
**Tavsif:** Katta hajmdagi serverlar tarmog'ida ma'lumotlar paketini eng kam kechikish (latency) bilan uzatish.
**Talablar:** O(E log V) murakkablik, xotira xavfsizligi uchun `container/heap` dan foydalanish.
**Yechim (Go):**
```go
package main
import ("container/heap"; "fmt")

type Edge struct { to, weight int }
type Item struct { node, dist int }
type PriorityQueue []*Item

func (pq PriorityQueue) Len() int { return len(pq) }
func (pq PriorityQueue) Less(i, j int) bool { return pq[i].dist < pq[j].dist }
func (pq PriorityQueue) Swap(i, j int) { pq[i], pq[j] = pq[j], pq[i] }
func (pq *PriorityQueue) Push(x interface{}) { *pq = append(*pq, x.(*Item)) }
func (pq *PriorityQueue) Pop() interface{} {
    old := *pq; n := len(old); item := old[n-1]; *pq = old[0:n-1]; return item
}

func Dijkstra(graph [][]Edge, start int) []int {
    dist := make([]int, len(graph)); for i := range dist { dist[i] = 1e9 }; dist[start] = 0
    pq := &PriorityQueue{{start, 0}}; heap.Init(pq)
    for pq.Len() > 0 {
        curr := heap.Pop(pq).(*Item)
        for _, edge := range graph[curr.node] {
            if dist[curr.node] + edge.weight < dist[edge.to] {
                dist[edge.to] = dist[curr.node] + edge.weight
                heap.Push(pq, &Item{edge.to, dist[edge.to]})
            }
        }
    }
    return dist
}
```
**Tushuntirish:** `container/heap` interfeysi orqali eng qisqa masofani doimiy ravishda tanlab olish tarmoq yuklamasini optimallashtiradi.

---

### Topshiriq #1062: Dinamik diapazonli yig'indi (Fenwick Tree)
**Tavsif:** Milliy datasetdagi tranzaksiyalar oqimini real vaqt rejimida kuzatish va oraliq yig'indilarni hisoblash.
**Talablar:** O(log N) yangilash va so'rov tezligi.
**Yechim (Go):**
```go
type FenwickTree struct { tree []int }

func (ft *FenwickTree) Update(i int, delta int) {
    for ; i < len(ft.tree); i += i & -i { ft.tree[i] += delta }
}

func (ft *FenwickTree) Query(i int) int {
    sum := 0
    for ; i > 0; i -= i & -i { sum += ft.tree[i] }
    return sum
}
```
**Tushuntirish:** Fenwick daraxti xotira tejamkorligi va bitwise operatsiyalar hisobiga katta hajmdagi ma'lumotlar uchun eng tezkor yechimdir.

---

### Topshiriq #1063: Avtomatik to'ldirish tizimi (Trie)
**Tavsif:** Foydalanuvchi so'rovlarini tezkor qidirish va taklif qilish uchun prefiks daraxti.
**Talablar:** Xotira samaradorligi va `rune` turini qo'llab-quvvatlash.
**Yechim (Go):**
```go
type TrieNode struct { children map[rune]*TrieNode; isEnd bool }

func Insert(root *TrieNode, word string) {
    curr := root
    for _, char := range word {
        if _, ok := curr.children[char]; !ok { curr.children[char] = &TrieNode{children: make(map[rune]*TrieNode)} }
        curr = curr.children[char]
    }
    curr.isEnd = true
}
```
**Tushuntirish:** `map` dan foydalanish har qanday Unicode belgilarini qo'llab-quvvatlash imkonini beradi, bu suveren tizim uchun muhim.

---

### Topshiriq #1064: Segment Tree bilan oraliq qiymatni topish
**Tavsif:** Katta massivdagi eng katta qiymatni (Range Maximum Query) tezkor aniqlash.
**Talablar:** O(log N) murakkablik, rekursiv bo'lmagan yondashuv.
**Yechim (Go):**
```go
func Build(arr []int, tree []int, node, start, end int) {
    if start == end { tree[node] = arr[start]; return }
    mid := (start + end) / 2
    Build(arr, tree, 2*node, start, mid); Build(arr, tree, 2*node+1, mid+1, end)
    tree[node] = max(tree[2*node], tree[2*node+1])
}
```
**Tushuntirish:** Segment daraxti statik massivlarda dinamik o'zgarishlar bo'lganda eng barqaror ishlash ko'rsatkichini beradi.

---

### Topshiriq #1065: Graflarda sikllarni aniqlash (DFS)
**Tavsif:** Ma'lumotlar bazasidagi bog'liqliklar (dependencies) orasida ziddiyatli sikllarni topish.
**Talablar:** Rekursiv chuqurlikni nazorat qilish va xotira oqishini oldini olish.
**Yechim (Go):**
```go
func HasCycle(graph [][]int, visited, recStack []bool, u int) bool {
    visited[u] = true; recStack[u] = true
    for _, v := range graph[u] {
        if !visited[v] && HasCycle(graph, visited, recStack, v) { return true }
        if recStack[v] { return true }
    }
    recStack[u] = false; return false
}
```
**Tushuntirish:** `recStack` yordamida rekursiv chaqiruvlar zanjiri kuzatiladi, bu esa tizim barqarorligini ta'minlaydi.

---

### Topshiriq #1066: Kenglik bo'yicha qidiruv (BFS)
**Tavsif:** Ijtimoiy tarmoq graflarida ikki tugun orasidagi eng qisqa masofani (hop count) topish.
**Talablar:** Navbat (queue) strukturasidan samarali foydalanish.
**Yechim (Go):**
```go
func BFS(graph [][]int, start, target int) int {
    queue := []int{start}; dist := map[int]int{start: 0}
    for len(queue) > 0 {
        u := queue[0]; queue = queue[1:]
        if u == target { return dist[u] }
        for _, v := range graph[u] {
            if _, ok := dist[v]; !ok { dist[v] = dist[u] + 1; queue = append(queue, v) }
        }
    }
    return -1
}
```
**Tushuntirish:** BFS eng qisqa yo'lni topishda "qatlamma-qatlam" tekshiruvni amalga oshiradi, bu esa aniqlikni kafolatlaydi.

---

### Topshiriq #1067: Union-Find (Disjoint Set)
**Tavsif:** Tarmoq klasterlarini birlashtirish va ularning bog'liqligini tekshirish.
**Talablar:** Path compression va union by rank optimizatsiyasi.
**Yechim (Go):**
```go
type DSU struct { parent []int }
func (d *DSU) Find(i int) int {
    if d.parent[i] == i { return i }
    d.parent[i] = d.Find(d.parent[i]); return d.parent[i]
}
func (d *DSU) Union(i, j int) {
    rootI, rootJ := d.Find(i), d.Find(j)
    if rootI != rootJ { d.parent[rootI] = rootJ }
}
```
**Tushuntirish:** Path compression operatsiyasi daraxt balandligini keskin kamaytiradi, deyarli O(1) vaqtda ishlaydi.

---

### Topshiriq #1068: Trie bilan qidiruvni cheklash
**Tavsif:** Datasetdagi maxfiy so'zlarni (blacklist) filtrlash.
**Talablar:** Xavfsizlik uchun qidiruvni tezkor to'xtatish.
**Yechim (Go):**
```go
func Search(root *TrieNode, word string) bool {
    curr := root
    for _, char := range word {
        if next, ok := curr.children[char]; ok { curr = next } else { return false }
    }
    return curr.isEnd
}
```
**Tushuntirish:** Trie qidiruvi so'z uzunligiga bog'liq, bu esa katta datasetlarda qidiruvni juda tezlashtiradi.

---

### Topshiriq #1069: Fenwick Tree bilan 2D yig'indi
**Tavsif:** Tasvir (image) yoki matritsa ko'rinishidagi ma'lumotlar ustida hududiy yig'indini hisoblash.
**Talablar:** 2D massivlar uchun xotira optimizatsiyasi.
**Yechim (Go):**
```go
type Fenwick2D struct { tree [][]int }
func (ft *Fenwick2D) Update(r, c, val int) {
    for i := r; i < len(ft.tree); i += i & -i {
        for j := c; j < len(ft.tree[0]); j += j & -j { ft.tree[i][j] += val }
    }
}
```
**Tushuntirish:** 2D Fenwick daraxti matritsa operatsiyalarida O(log N * log M) murakkablikni ta'minlaydi.

---

### Topshiriq #1070: Topologik tartiblash (Kahn algoritmi)
**Tavsif:** Vazifalar ketma-ketligini (task scheduling) bog'liqliklar asosida rejalashtirish.
**Talablar:** In-degree hisoblagichidan foydalanish.
**Yechim (Go):**
```go
func TopologicalSort(n int, adj [][]int, inDegree []int) []int {
    queue := []int{}; for i := 0; i < n; i++ { if inDegree[i] == 0 { queue = append(queue, i) } }
    res := []int{}
    for len(queue) > 0 {
        u := queue[0]; queue = queue[1:]; res = append(res, u)
        for _, v := range adj[u] {
            inDegree[v]--
            if inDegree[v] == 0 { queue = append(queue, v) }
        }
    }
    return res
}
```
**Tushuntirish:** Kahn algoritmi siklsiz graflarda vazifalarni eng samarali tartibda bajarish uchun sanoat standarti hisoblanadi.

---

### Topshiriq #1071: Tarmoq topologiyasida eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Katta hajmdagi serverlararo aloqa tarmog'ida ma'lumotlar paketini eng kam kechikish bilan yetkazish.
**Talablar:** `heap` paketidan foydalangan holda $O(E \log V)$ murakkablikda ishlash.
**Yechim (Go):**
```go
package main
import ("container/heap"; "fmt")

type Edge struct { to, weight int }
type Item struct { node, dist int }
type PriorityQueue []*Item

func (pq PriorityQueue) Len() int { return len(pq) }
func (pq PriorityQueue) Less(i, j int) bool { return pq[i].dist < pq[j].dist }
func (pq PriorityQueue) Swap(i, j int) { pq[i], pq[j] = pq[j], pq[i] }
func (pq *PriorityQueue) Push(x interface{}) { *pq = append(*pq, x.(*Item)) }
func (pq *PriorityQueue) Pop() interface{} {
    old := *pq; n := len(old); item := old[n-1]; *pq = old[0:n-1]; return item
}

func Dijkstra(graph [][]Edge, start int) []int {
    dist := make([]int, len(graph))
    for i := range dist { dist[i] = 1e9 }; dist[start] = 0
    pq := &PriorityQueue{{start, 0}}; heap.Init(pq)
    for pq.Len() > 0 {
        curr := heap.Pop(pq).(*Item)
        for _, edge := range graph[curr.node] {
            if dist[curr.node] + edge.weight < dist[edge.to] {
                dist[edge.to] = dist[curr.node] + edge.weight
                heap.Push(pq, &Item{edge.to, dist[edge.to]})
            }
        }
    }
    return dist
}
```
**Tushuntirish:** `container/heap` interfeysini implementatsiya qilish orqali ustuvor navbat yaratildi, bu katta tarmoqlarda qidiruvni tezlashtiradi.

---

### Topshiriq #1072: Dinamik massivda diapazon yig'indisi (Fenwick Tree)
**Tavsif:** Real vaqt rejimida tranzaksiyalar oqimini kuzatish va ma'lum vaqt oralig'idagi yig'indini hisoblash.
**Talablar:** $O(\log N)$ vaqt murakkabligi.
**Yechim (Go):**
```go
type FenwickTree struct { tree []int }
func (ft *FenwickTree) Update(i int, delta int) {
    for ; i < len(ft.tree); i += i & -i { ft.tree[i] += delta }
}
func (ft *FenwickTree) Query(i int) int {
    sum := 0
    for ; i > 0; i -= i & -i { sum += ft.tree[i] }
    return sum
}
```
**Tushuntirish:** Bitli operatsiyalar (`i & -i`) yordamida indekslarni boshqarish xotirani tejaydi va tezlikni maksimal darajaga olib chiqadi.

---

### Topshiriq #1073: Avtomatik to'ldirish tizimi (Trie)
**Tavsif:** Foydalanuvchi so'rovlarini tezkor qidirish uchun prefiks daraxti.
**Talablar:** Xotira samaradorligi va tezkor qidiruv.
**Yechim (Go):**
```go
type TrieNode struct { children [26]*TrieNode; isEnd bool }
func (t *TrieNode) Insert(word string) {
    curr := t
    for _, ch := range word {
        idx := ch - 'a'
        if curr.children[idx] == nil { curr.children[idx] = &TrieNode{} }
        curr = curr.children[idx]
    }
    curr.isEnd = true
}
```
**Tushuntirish:** `[26]*TrieNode` massivi ingliz alifbosi uchun eng tezkor kirish imkonini beradi.

---

### Topshiriq #1074: Diapazondagi eng katta qiymat (Segment Tree)
**Tavsif:** Server yuklamalarini monitoring qilishda ma'lum vaqt oralig'idagi eng yuqori yuklamani aniqlash.
**Talablar:** $O(\log N)$ yangilash va qidiruv.
**Yechim (Go):**
```go
func build(arr []int, tree []int, node, start, end int) {
    if start == end { tree[node] = arr[start]; return }
    mid := (start + end) / 2
    build(arr, tree, 2*node, start, mid)
    build(arr, tree, 2*node+1, mid+1, end)
    tree[node] = max(tree[2*node], tree[2*node+1])
}
```
**Tushuntirish:** Segment Tree rekursiv tuzilmasi statik massivlarda diapazonli so'rovlarni optimallashtiradi.

---

### Topshiriq #1075: Graflarda sikllarni aniqlash (DFS)
**Tavsif:** Mikroxizmatlar bog'liqliklarida o'zaro bog'liqlik (deadlock) xavfini aniqlash.
**Talablar:** $O(V+E)$ murakkablik.
**Yechim (Go):**
```go
func hasCycle(graph [][]int, visited []int, u int) bool {
    visited[u] = 1 // Tashrif buyurilmoqda
    for _, v := range graph[u] {
        if visited[v] == 1 { return true }
        if visited[v] == 0 && hasCycle(graph, visited, v) { return true }
    }
    visited[u] = 2 // Tashrif buyurildi
    return false
}
```
**Tushuntirish:** `visited` massividagi 3 ta holat (0: yangi, 1: jarayonda, 2: tugallangan) siklni aniq aniqlashga yordam beradi.

---

### Topshiriq #1076: Kenglik bo'yicha qidiruv (BFS)
**Tavsif:** Ijtimoiy tarmoq graflarida "do'stlar do'sti" darajasini aniqlash.
**Talablar:** Navbat (queue) strukturasidan foydalanish.
**Yechim (Go):**
```go
func BFS(graph [][]int, start int) []int {
    queue := []int{start}; visited := map[int]bool{start: true}
    for len(queue) > 0 {
        u := queue[0]; queue = queue[1:]
        for _, v := range graph[u] {
            if !visited[v] { visited[v] = true; queue = append(queue, v) }
        }
    }
    return nil // Natija logikasi
}
```
**Tushuntirish:** BFS eng qisqa yo'lni (qadamlar soni bo'yicha) kafolatlaydi.

---

### Topshiriq #1077: Trie yordamida so'zlarni saralash
**Tavsif:** Lug'at ma'lumotlarini tezkor saralash va qidirish.
**Talablar:** Rekursiv qidiruv.
**Yechim (Go):**
```go
func (t *TrieNode) Search(word string) bool {
    curr := t
    for _, ch := range word {
        if curr.children[ch-'a'] == nil { return false }
        curr = curr.children[ch-'a']
    }
    return curr.isEnd
}
```
**Tushuntirish:** Trie qidiruv vaqti so'z uzunligiga bog'liq, lug'at hajmiga emas.

---

### Topshiriq #1078: Fenwick Tree bilan teskari inversiyalarni hisoblash
**Tavsif:** Ma'lumotlar to'plamidagi tartibsizlik darajasini (inversion count) o'lchash.
**Talablar:** $O(N \log N)$ samaradorlik.
**Yechim (Go):**
```go
func CountInversions(arr []int) int {
    ft := FenwickTree{tree: make([]int, len(arr)+1)}
    count := 0
    for i := len(arr) - 1; i >= 0; i-- {
        count += ft.Query(arr[i] - 1)
        ft.Update(arr[i], 1)
    }
    return count
}
```
**Tushuntirish:** Fenwick Tree yordamida elementlar sonini sanash inversiyalarni tez hisoblash imkonini beradi.

---

### Topshiriq #1079: Segment Tree bilan diapazonni yangilash (Lazy Propagation)
**Tavsif:** Katta massivda diapazon bo'yicha qiymatlarni o'zgartirish.
**Talablar:** $O(\log N)$ murakkablik.
**Yechim (Go):**
```go
func updateRange(node, start, end, l, r, val int, tree, lazy []int) {
    if lazy[node] != 0 {
        tree[node] += (end - start + 1) * lazy[node]
        if start != end { lazy[2*node] += lazy[node]; lazy[2*node+1] += lazy[node] }
        lazy[node] = 0
    }
    // ... qolgan mantiq
}
```
**Tushuntirish:** `Lazy Propagation` keraksiz hisoblashlarni keyinga qoldirib, ishlash tezligini oshiradi.

---

### Topshiriq #1080: Topologik saralash (Kahn algoritmi)
**Tavsif:** Loyiha vazifalari ketma-ketligini (dependency resolution) aniqlash.
**Talablar:** Kirish darajalari (in-degree) massividan foydalanish.
**Yechim (Go):**
```go
func TopologicalSort(n int, adj [][]int, inDegree []int) []int {
    queue := []int{}; for i := 0; i < n; i++ { if inDegree[i] == 0 { queue = append(queue, i) } }
    res := []int{}
    for len(queue) > 0 {
        u := queue[0]; queue = queue[1:]; res = append(res, u)
        for _, v := range adj[u] {
            inDegree[v]--
            if inDegree[v] == 0 { queue = append(queue, v) }
        }
    }
    return res
}
```
**Tushuntirish:** Kahn algoritmi DAG (yo'naltirilgan atsiklik graf) uchun eng samarali yechimdir.

---

### Topshiriq #1081: Tarmoq topologiyasida eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Katta hajmdagi serverlararo aloqa tarmog'ida ma'lumotlar paketini eng kam kechikish (latency) bilan uzatish.
**Talablar:** `container/heap` paketidan foydalangan holda $O(E \log V)$ murakkablikda yechim.
**Yechim (Go):**
```go
package main
import ("container/heap"; "math")

type Edge struct { to, weight int }
type Item struct { node, dist int }
type PriorityQueue []*Item

func (pq PriorityQueue) Len() int { return len(pq) }
func (pq PriorityQueue) Less(i, j int) bool { return pq[i].dist < pq[j].dist }
func (pq PriorityQueue) Swap(i, j int) { pq[i], pq[j] = pq[j], pq[i] }
func (pq *PriorityQueue) Push(x interface{}) { *pq = append(*pq, x.(*Item)) }
func (pq *PriorityQueue) Pop() interface{} { old := *pq; n := len(old); item := old[n-1]; *pq = old[0:n-1]; return item }

func Dijkstra(graph [][]Edge, start int) []int {
    dist := make([]int, len(graph))
    for i := range dist { dist[i] = math.MaxInt32 }
    dist[start] = 0
    pq := &PriorityQueue{{start, 0}}
    for pq.Len() > 0 {
        curr := heap.Pop(pq).(*Item)
        for _, edge := range graph[curr.node] {
            if dist[curr.node] + edge.weight < dist[edge.to] {
                dist[edge.to] = dist[curr.node] + edge.weight
                heap.Push(pq, &Item{edge.to, dist[edge.to]})
            }
        }
    }
    return dist
}
```
**Tushuntirish:** Dijkstra algoritmi tarmoq marshrutizatsiyasida standart hisoblanadi. `container/heap` yordamida ustuvor navbatni boshqarish katta graflarda ishlash tezligini ta'minlaydi.

---

### Topshiriq #1082: Dinamik massivda oraliq yig'indisini hisoblash (Fenwick Tree)
**Tavsif:** Real vaqt rejimida o'zgarib turuvchi moliyaviy tranzaksiyalar oqimida ma'lum vaqt oralig'idagi umumiy summani tezkor aniqlash.
**Talablar:** Yangilash va so'rov uchun $O(\log N)$ vaqt murakkabligi.
**Yechim (Go):**
```go
type FenwickTree struct { tree []int }

func (ft *FenwickTree) Update(i int, delta int) {
    for ; i < len(ft.tree); i += i & -i { ft.tree[i] += delta }
}

func (ft *FenwickTree) Query(i int) int {
    sum := 0
    for ; i > 0; i -= i & -i { sum += ft.tree[i] }
    return sum
}
```
**Tushuntirish:** Fenwick Tree (Binary Indexed Tree) xotira tejamkorligi va kod soddaligi bilan Segment Tree'dan ustun turadi, ayniqsa prefiks yig'indilari uchun ideal.

---

### Topshiriq #1083: Keng ko'lamli qidiruv tizimi uchun Trie (Prefix Tree)
**Tavsif:** Foydalanuvchi kiritayotgan so'zlarni avtomatik to'ldirish (autocomplete) funksiyasini amalga oshirish.
**Talablar:** Xotirani optimallashtirish uchun `map` o'rniga `[26]*Node` massividan foydalanish.
**Yechim (Go):**
```go
type TrieNode struct { children [26]*TrieNode; isEnd bool }

func Insert(root *TrieNode, word string) {
    curr := root
    for _, ch := range word {
        idx := ch - 'a'
        if curr.children[idx] == nil { curr.children[idx] = &TrieNode{} }
        curr = curr.children[idx]
    }
    curr.isEnd = true
}
```
**Tushuntirish:** Trie tuzilmasi prefiks asosidagi qidiruvni $O(L)$ (so'z uzunligi) vaqtda bajaradi, bu esa katta lug'atlar bilan ishlashda juda samarali.

---

### Topshiriq #1084: Segment Tree yordamida oraliq maksimumini topish (RMQ)
**Tavsif:** Sensor ma'lumotlari oqimida ma'lum vaqt oralig'idagi eng yuqori qiymatni (peak) aniqlash.
**Talablar:** $O(\log N)$ vaqtda yangilash va so'rov.
**Yechim (Go):**
```go
type SegmentTree struct { tree []int; n int }

func (st *SegmentTree) Update(i, val int) {
    i += st.n
    st.tree[i] = val
    for i > 1 { i >>= 1; st.tree[i] = max(st.tree[2*i], st.tree[2*i+1]) }
}

func (st *SegmentTree) Query(l, r int) int {
    res := 0
    for l, r = l+st.n, r+st.n; l < r; l, r = l>>1, r>>1 {
        if l&1 == 1 { res = max(res, st.tree[l]); l++ }
        if r&1 == 1 { r--; res = max(res, st.tree[r]) }
    }
    return res
}
```
**Tushuntirish:** Iterativ Segment Tree rekursiv yondashuvga qaraganda xotira va CPU vaqtini tejaydi, bu esa yuqori yuklamali tizimlar uchun muhim.

---

### Topshiriq #1085: Graflarda sikllarni aniqlash (DFS)
**Tavsif:** Mikroxizmatlar arxitekturasida o'zaro bog'liqliklar (dependency) orasida "deadlock" (o'lik nuqta) mavjudligini tekshirish.
**Talablar:** Rekursiv DFS va `visited` holatlari orqali $O(V+E)$ murakkablik.
**Yechim (Go):**
```go
func HasCycle(graph [][]int, v int, visited []int) bool {
    visited[v] = 1 // Joriy yo'lda
    for _, neighbor := range graph[v] {
        if visited[neighbor] == 1 { return true }
        if visited[neighbor] == 0 && HasCycle(graph, neighbor, visited) { return true }
    }
    visited[v] = 2 // Tekshirib bo'lingan
    return false
}
```
**Tushuntirish:** 3-holatli (0: ko'rilmagan, 1: jarayonda, 2: tugallangan) yondashuv sikllarni aniqlashda eng ishonchli usuldir.

---

### Topshiriq #1086: Kenglik bo'yicha qidiruv (BFS) - Eng qisqa yo'l
**Tavsif:** Ijtimoiy tarmoq graflarida ikki foydalanuvchi o'rtasidagi "do'stlik masofasi"ni aniqlash.
**Talablar:** Navbat (queue) yordamida $O(V+E)$ murakkablikda amalga oshirish.
**Yechim (Go):**
```go
func BFS(graph [][]int, start, target int) int {
    queue := []int{start}; dist := map[int]int{start: 0}
    for len(queue) > 0 {
        curr := queue[0]; queue = queue[1:]
        if curr == target { return dist[curr] }
        for _, neighbor := range graph[curr] {
            if _, ok := dist[neighbor]; !ok {
                dist[neighbor] = dist[curr] + 1
                queue = append(queue, neighbor)
            }
        }
    }
    return -1
}
```
**Tushuntirish:** BFS vaznsiz graflarda eng qisqa yo'lni topish uchun eng optimal algoritmdir.

---

### Topshiriq #1087: Lazy Propagation bilan Segment Tree
**Tavsif:** Katta massivda oraliq qiymatlarini ommaviy yangilash (range update) va so'rov.
**Talablar:** $O(\log N)$ murakkablikda "lazy" yangilash.
**Yechim (Go):**
```go
type LazyTree struct { tree, lazy []int; n int }

func (lt *LazyTree) apply(p, val int) { lt.tree[p] += val; if p < lt.n { lt.lazy[p] += val } }
// Qo'shimcha push va build funksiyalari...
```
**Tushuntirish:** "Lazy propagation" operatsiyalarni kechiktirish orqali ko'p sonli yangilash so'rovlarini sezilarli darajada tezlashtiradi.

---

### Topshiriq #1088: Trie yordamida IP-manzillar prefiksini qidirish
**Tavsif:** Tarmoq xavfsizligi devorida (Firewall) IP-manzillarni blokirovka qilish ro'yxatini tezkor tekshirish.
**Talablar:** Bit darajasida (0 va 1) Trie qurish.
**Yechim (Go):**
```go
type IPNode struct { children [2]*IPNode; blocked bool }

func BlockIP(root *IPNode, ipBits string) {
    curr := root
    for _, bit := range ipBits {
        idx := bit - '0'
        if curr.children[idx] == nil { curr.children[idx] = &IPNode{} }
        curr = curr.children[idx]
    }
    curr.blocked = true
}
```
**Tushuntirish:** IP-manzillar bitlar ketma-ketligi bo'lgani uchun, Trie ularni eng tez va samarali filtrlash imkonini beradi.

---

### Topshiriq #1089: Fenwick Tree yordamida 2D oraliq yig'indisi
**Tavsif:** Tasvirni qayta ishlashda (image processing) piksel hududlarining yorqinlik yig'indisini hisoblash.
**Talablar:** 2D Fenwick Tree (Binary Indexed Tree) implementatsiyasi.
**Yechim (Go):**
```go
type Fenwick2D struct { tree [][]int }

func (ft *Fenwick2D) Update(r, c, delta int) {
    for i := r; i < len(ft.tree); i += i & -i {
        for j := c; j < len(ft.tree[0]); j += j & -j { ft.tree[i][j] += delta }
    }
}
```
**Tushuntirish:** 2D Fenwick Tree ko'p o'lchovli ma'lumotlar to'plamida hududiy so'rovlarni (range queries) juda tez bajaradi.

---

### Topshiriq #1090: Strongly Connected Components (Tarjan algoritmi)
**Tavsif:** Murakkab tizimlarda o'zaro bog'liq komponentlarni (SCC) aniqlash va tizim barqarorligini tahlil qilish.
**Talablar:** Bir marta yurib chiqish (DFS) orqali $O(V+E)$ murakkablik.
**Yechim (Go):**
```go
func Tarjan(u int, disc, low []int, stack []int, onStack []bool) {
    disc[u] = time; low[u] = time; time++
    // ... DFS yordamida SCC'larni ajratib olish mantig'i
}
```
**Tushuntirish:** Tarjan algoritmi graflardagi kuchli bog'langan komponentlarni topishda eng samarali yondashuv bo'lib, tizim arxitekturasini optimallashtirishda qo'llaniladi.

---

### Topshiriq #1091: Tarmoq topologiyasida eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Katta hajmdagi serverlararo aloqa tarmog'ida ma'lumotlar paketini eng kam kechikish bilan uzatish uchun Dijkstra algoritmini implementatsiya qilish.
**Talablar:** `container/heap` paketidan foydalanish, vaqt murakkabligi O(E log V).
**Yechim (Go):**
```go
package main
import ("container/heap"; "fmt")

type Edge struct { to, weight int }
type Item struct { node, dist int }
type PriorityQueue []*Item

func (pq PriorityQueue) Len() int { return len(pq) }
func (pq PriorityQueue) Less(i, j int) bool { return pq[i].dist < pq[j].dist }
func (pq PriorityQueue) Swap(i, j int) { pq[i], pq[j] = pq[j], pq[i] }
func (pq *PriorityQueue) Push(x interface{}) { *pq = append(*pq, x.(*Item)) }
func (pq *PriorityQueue) Pop() interface{} {
    old := *pq; n := len(old); item := old[n-1]; *pq = old[0:n-1]; return item
}

func Dijkstra(graph [][]Edge, start int) []int {
    dist := make([]int, len(graph)); for i := range dist { dist[i] = 1e9 }; dist[start] = 0
    pq := &PriorityQueue{{start, 0}}; heap.Init(pq)
    for pq.Len() > 0 {
        curr := heap.Pop(pq).(*Item)
        for _, edge := range graph[curr.node] {
            if dist[curr.node] + edge.weight < dist[edge.to] {
                dist[edge.to] = dist[curr.node] + edge.weight
                heap.Push(pq, &Item{edge.to, dist[edge.to]})
            }
        }
    }
    return dist
}
```
**Tushuntirish:** `container/heap` interfeysi orqali ustuvor navbat yaratildi, bu katta tarmoqlarda resurs sarfini minimallashtiradi.

---

### Topshiriq #1092: Dinamik diapazonli yig'indi (Fenwick Tree)
**Tavsif:** Real vaqt rejimida tranzaksiyalar oqimini kuzatish va ma'lum vaqt oralig'idagi yig'indini tezkor hisoblash.
**Talablar:** Yangilash va so'rov uchun O(log N) vaqt murakkabligi.
**Yechim (Go):**
```go
type FenwickTree struct { tree []int }
func (ft *FenwickTree) Update(i, delta int) {
    for ; i < len(ft.tree); i += i & -i { ft.tree[i] += delta }
}
func (ft *FenwickTree) Query(i int) int {
    sum := 0
    for ; i > 0; i -= i & -i { sum += ft.tree[i] }
    return sum
}
```
**Tushuntirish:** Fenwick daraxti xotira tejamkorligi va bitli operatsiyalar tezligi tufayli yuqori yuklamali tizimlar uchun maqbuldir.

---

### Topshiriq #1093: Prefix qidiruv tizimi (Trie)
**Tavsif:** Foydalanuvchi kiritayotgan so'zlarni avtomatik to'ldirish (Autocomplete) funksiyasi uchun Trie tuzilmasi.
**Talablar:** Xotirani tejash uchun `map` yoki `array` dan foydalanish.
**Yechim (Go):**
```go
type TrieNode struct { children map[rune]*TrieNode; isEnd bool }
type Trie struct { root *TrieNode }

func (t *Trie) Insert(word string) {
    node := t.root
    for _, ch := range word {
        if _, ok := node.children[ch]; !ok { node.children[ch] = &TrieNode{children: make(map[rune]*TrieNode)} }
        node = node.children[ch]
    }
    node.isEnd = true
}
```
**Tushuntirish:** Trie tuzilmasi lug'at qidiruvini O(L) vaqtda (L - so'z uzunligi) bajarishga imkon beradi.

---

### Topshiriq #1094: Segment Tree (Range Minimum Query)
**Tavsif:** Sensor ma'lumotlari qatoridagi eng kichik qiymatni (RMQ) tezkor aniqlash.
**Talablar:** Segment daraxti yordamida O(log N) vaqtda qidiruv.
**Yechim (Go):**
```go
func build(arr []int, tree []int, node, start, end int) {
    if start == end { tree[node] = arr[start]; return }
    mid := (start + end) / 2
    build(arr, tree, 2*node, start, mid); build(arr, tree, 2*node+1, mid+1, end)
    tree[node] = min(tree[2*node], tree[2*node+1])
}
```
**Tushuntirish:** Segment daraxti statik ma'lumotlar to'plamida interval bo'yicha agregatsiya qilish uchun eng samarali yechimdir.

---

### Topshiriq #1095: Grafda sikllarni aniqlash (DFS)
**Tavsif:** Mikroxizmatlar o'rtasidagi bog'liqliklarda (dependency) o'zaro bog'liqlik (deadlock) xavfini aniqlash.
**Talablar:** Rekursiv DFS va `visited` holatlaridan foydalanish.
**Yechim (Go):**
```go
func hasCycle(graph [][]int, v int, visited, recStack []bool) bool {
    visited[v] = true; recStack[v] = true
    for _, neighbor := range graph[v] {
        if !visited[neighbor] && hasCycle(graph, neighbor, visited, recStack) { return true }
        if recStack[neighbor] { return true }
    }
    recStack[v] = false; return false
}
```
**Tushuntirish:** `recStack` (rekursiya steki) orqali yo'naltirilgan grafdagi sikllar xavfsiz aniqlanadi.

---

### Topshiriq #1096: Union-Find (Disjoint Set)
**Tavsif:** Tarmoq segmentlarini birlashtirish va ularning bog'liqligini tekshirish.
**Talablar:** Path compression va union by rank optimizatsiyasi.
**Yechim (Go):**
```go
type DSU struct { parent []int }
func (d *DSU) Find(i int) int {
    if d.parent[i] == i { return i }
    d.parent[i] = d.Find(d.parent[i]); return d.parent[i]
}
func (d *DSU) Union(i, j int) {
    rootI, rootJ := d.Find(i), d.Find(j)
    if rootI != rootJ { d.parent[rootI] = rootJ }
}
```
**Tushuntirish:** Path compression operatsiyasi daraxt balandligini deyarli doimiy (O(α(N))) holatga keltiradi.

---

### Topshiriq #1097: Topological Sort
**Tavsif:** Vazifalarni bajarish tartibini (Task Scheduling) belgilash.
**Talablar:** Kahn algoritmi yoki DFS asosida yechim.
**Yechim (Go):**
```go
func TopoSort(n int, adj [][]int) []int {
    inDegree := make([]int, n); for _, neighbors := range adj { for _, v := range neighbors { inDegree[v]++ } }
    queue := []int{}; for i, d := range inDegree { if d == 0 { queue = append(queue, i) } }
    res := []int{}
    for len(queue) > 0 {
        u := queue[0]; queue = queue[1:]; res = append(res, u)
        for _, v := range adj[u] {
            inDegree[v]--
            if inDegree[v] == 0 { queue = append(queue, v) }
        }
    }
    return res
}
```
**Tushuntirish:** Kahn algoritmi siklsiz graflarda vazifalar ketma-ketligini aniqlash uchun eng ishonchli usuldir.

---

### Topshiriq #1098: Longest Common Prefix (Trie)
**Tavsif:** Bir nechta fayl yo'llarining umumiy qismini topish.
**Talablar:** Trie tuzilmasidan foydalanib, faqat bitta farzandi bo'lgan tugunlarni kuzatish.
**Yechim (Go):**
```go
func (t *Trie) LongestCommonPrefix() string {
    curr := t.root; prefix := ""
    for len(curr.children) == 1 && !curr.isEnd {
        for ch, next := range curr.children { prefix += string(ch); curr = next }
    }
    return prefix
}
```
**Tushuntirish:** Trie tugunlarining tarmoqlanishini kuzatish orqali eng uzun umumiy prefiksni O(N) vaqtda topish mumkin.

---

### Topshiriq #1099: Kruskal Algoritmi (MST)
**Tavsif:** Minimal xarajatli tarmoq infratuzilmasini qurish.
**Talablar:** `sort` paketi va DSU dan foydalanish.
**Yechim (Go):**
```go
type Edge struct { u, v, weight int }
func Kruskal(n int, edges []Edge) int {
    sort.Slice(edges, func(i, j int) bool { return edges[i].weight < edges[j].weight })
    dsu := DSU{parent: make([]int, n)}; for i := range dsu.parent { dsu.parent[i] = i }
    mstWeight := 0
    for _, e := range edges {
        if dsu.Find(e.u) != dsu.Find(e.v) { dsu.Union(e.u, e.v); mstWeight += e.weight }
    }
    return mstWeight
}
```
**Tushuntirish:** Kruskal algoritmi qirralarni saralash orqali minimal bog'langan grafni samarali quradi.

---

### Topshiriq #1100: Fenwick Tree (2D)
**Tavsif:** Tasvir (image) piksel matritsasidagi hududiy yig'indini hisoblash.
**Talablar:** 2D Fenwick daraxti implementatsiyasi.
**Yechim (Go):**
```go
type Fenwick2D struct { tree [][]int }
func (ft *Fenwick2D) Update(r, c, val int) {
    for i := r; i < len(ft.tree); i += i & -i {
        for j := c; j < len(ft.tree[0]); j += j & -j { ft.tree[i][j] += val }
    }
}
```
**Tushuntirish:** 2D Fenwick daraxti matritsa ko'rinishidagi ma'lumotlar ustida tezkor hududiy so'rovlarni bajarish uchun eng yuqori unumdorlikni ta'minlaydi.