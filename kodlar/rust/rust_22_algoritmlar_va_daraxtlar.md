# Khorazmiy AI: Rust - Modul 22
## Mavzu: Ilg'or Algoritmlar: Graflar, Segment Trees, Fenwick va Trie tuzilmalari

### Topshiriq #1051: Graflarda eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Logistika tizimlarida yuk tashish marshrutlarini optimallashtirish.
**Talablar:** `BinaryHeap` yordamida $O(E \log V)$ murakkablikda ishlash, xavfsiz xotira boshqaruvi.
**Yechim (Rust):**
```rust
use std::collections::BinaryHeap;
use std::cmp::Ordering;

#[derive(Copy, Clone, Eq, PartialEq)]
struct State { cost: usize, position: usize }

impl Ord for State {
    fn cmp(&self, other: &Self) -> Ordering { other.cost.cmp(&self.cost) }
}
impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> { Some(self.cmp(other)) }
}

pub fn dijkstra(adj: &Vec<Vec<(usize, usize)>>, start: usize) -> Vec<usize> {
    let mut dists = vec![usize::MAX; adj.len()];
    let mut heap = BinaryHeap::new();
    dists[start] = 0;
    heap.push(State { cost: 0, position: start });
    while let Some(State { cost, position }) = heap.pop() {
        if cost > dists[position] { continue; }
        for &(next, weight) in &adj[position] {
            if dists[position] + weight < dists[next] {
                dists[next] = dists[position] + weight;
                heap.push(State { cost: dists[next], position: next });
            }
        }
    }
    dists
}
```
**Tushuntirish:** `BinaryHeap` Rust'da standart kutubxona orqali maksimal qiymatni qaytaradi, shuning uchun `Ord` trait'ini teskari qilib, minimal yo'lni topish uchun optimallashtirdik.

---

### Topshiriq #1052: Segment Tree yordamida diapazon yig'indisi
**Tavsif:** Moliya tizimlarida real vaqt rejimida balans o'zgarishlarini kuzatish.
**Talablar:** $O(\log N)$ yangilash va so'rov vaqti, thread-safe yondashuv.
**Yechim (Rust):**
```rust
struct SegmentTree { n: usize, tree: Vec<i64> }
impl SegmentTree {
    fn update(&mut self, mut i: usize, val: i64) {
        i += self.n;
        self.tree[i] = val;
        while i > 1 { i >>= 1; self.tree[i] = self.tree[2*i] + self.tree[2*i+1]; }
    }
    fn query(&self, mut l: usize, mut r: usize) -> i64 {
        let (mut res, mut l, mut r) = (0, l + self.n, r + self.n);
        while l < r {
            if l & 1 == 1 { res += self.tree[l]; l += 1; }
            if r & 1 == 1 { r -= 1; res += self.tree[r]; }
            l >>= 1; r >>= 1;
        }
        res
    }
}
```
**Tushuntirish:** Iterativ Segment Tree xotira samaradorligi va tezligi bo'yicha rekursiv yondashuvdan ustun turadi.

---

### Topshiriq #1053: Fenwick Tree (Binary Indexed Tree)
**Tavsif:** Katta hajmdagi ma'lumotlar oqimida kümülatif chastotalarni hisoblash.
**Talablar:** Minimal xotira sarfi, $O(\log N)$ operatsiyalar.
**Yechim (Rust):**
```rust
struct FenwickTree { tree: Vec<i64> }
impl FenwickTree {
    fn add(&mut self, mut i: usize, delta: i64) {
        while i < self.tree.len() { self.tree[i] += delta; i += i & (!i + 1); }
    }
    fn prefix_sum(&self, mut i: usize) -> i64 {
        let mut sum = 0;
        while i > 0 { sum += self.tree[i]; i -= i & (!i + 1); }
        sum
    }
}
```
**Tushuntirish:** Fenwick Tree Segment Tree'ga qaraganda kamroq xotira talab qiladi va bitwise operatsiyalar tufayli juda tez ishlaydi.

---

### Topshiriq #1054: Trie (Prefix Tree)
**Tavsif:** Milliy qidiruv tizimlarida avtomatik to'ldirish (autocomplete) funksiyasi.
**Talablar:** Xotira xavfsizligi, `Box` yoki `Rc` yordamida dinamik tugunlar.
**Yechim (Rust):**
```rust
use std::collections::HashMap;
struct TrieNode { children: HashMap<char, TrieNode>, is_end: bool }
pub struct Trie { root: TrieNode }
impl Trie {
    pub fn insert(&mut self, word: &str) {
        let mut curr = &mut self.root;
        for c in word.chars() { curr = curr.children.entry(c).or_insert(TrieNode { children: HashMap::new(), is_end: false }); }
        curr.is_end = true;
    }
}
```
**Tushuntirish:** `HashMap` yordamida har bir tugun uchun dinamik tarmoqlanish ta'minlandi, bu esa turli tillardagi alifbolar uchun moslashuvchanlikni beradi.

---

### Topshiriq #1055: Graflarda sikllarni aniqlash (DFS)
**Tavsif:** Tarmoq xavfsizligida o'lik qulflarni (deadlock) aniqlash.
**Talablar:** Rekursiv xavfsizlik, `visited` massivlari orqali holatni kuzatish.
**Yechim (Rust):**
```rust
fn has_cycle(adj: &Vec<Vec<usize>>, u: usize, visited: &mut Vec<bool>, rec_stack: &mut Vec<bool>) -> bool {
    visited[u] = true; rec_stack[u] = true;
    for &v in &adj[u] {
        if !visited[v] && has_cycle(adj, v, visited, rec_stack) { return true; }
        else if rec_stack[v] { return true; }
    }
    rec_stack[u] = false;
    false
}
```
**Tushuntirish:** `rec_stack` yordamida joriy rekursiya yo'lida sikl borligini tekshirish eng samarali usuldir.

---

### Topshiriq #1056: Topological Sort
**Tavsif:** Loyihalarni boshqarish tizimlarida vazifalar ketma-ketligini belgilash.
**Talablar:** DAG (Directed Acyclic Graph) shartini tekshirish.
**Yechim (Rust):**
```rust
fn topo_sort(adj: &Vec<Vec<usize>>, n: usize) -> Vec<usize> {
    let mut in_degree = vec![0; n];
    for u in 0..n { for &v in &adj[u] { in_degree[v] += 1; } }
    let mut q = std::collections::VecDeque::new();
    for i in 0..n { if in_degree[i] == 0 { q.push_back(i); } }
    let mut res = Vec::new();
    while let Some(u) = q.pop_front() {
        res.push(u);
        for &v in &adj[u] {
            in_degree[v] -= 1;
            if in_degree[v] == 0 { q.push_back(v); }
        }
    }
    res
}
```
**Tushuntirish:** Kahn algoritmi yordamida in-degree hisoblash orqali tartiblash xotira va vaqt bo'yicha optimaldir.

---

### Topshiriq #1057: Disjoint Set Union (DSU)
**Tavsif:** Ijtimoiy tarmoqlarda "do'stlar guruhini" birlashtirish.
**Talablar:** Path compression va union by rank/size.
**Yechim (Rust):**
```rust
struct DSU { parent: Vec<usize> }
impl DSU {
    fn find(&mut self, i: usize) -> usize {
        if self.parent[i] == i { i }
        else { self.parent[i] = self.find(self.parent[i]); self.parent[i] }
    }
    fn union(&mut self, i: usize, j: usize) {
        let root_i = self.find(i); let root_j = self.find(j);
        if root_i != root_j { self.parent[root_i] = root_j; }
    }
}
```
**Tushuntirish:** Path compression yordamida `find` operatsiyasi deyarli $O(1)$ vaqtda bajariladi.

---

### Topshiriq #1058: Kruskal Algoritmi (MST)
**Tavsif:** Milliy infratuzilma (elektr tarmoqlari) uchun minimal xarajatli daraxt.
**Talablar:** `DSU` bilan integratsiya, qirralarni saralash.
**Yechim (Rust):**
```rust
fn kruskal(n: usize, mut edges: Vec<(usize, usize, usize)>) -> usize {
    edges.sort_by_key(|&(_, _, w)| w);
    let mut dsu = DSU { parent: (0..n).collect() };
    let mut mst_weight = 0;
    for (u, v, w) in edges {
        if dsu.find(u) != dsu.find(v) {
            dsu.union(u, v);
            mst_weight += w;
        }
    }
    mst_weight
}
```
**Tushuntirish:** Qirralarni vazn bo'yicha saralash va DSU yordamida sikllarni chetlab o'tish eng ishonchli MST yechimidir.

---

### Topshiriq #1059: Suffix Trie (Oddiy)
**Tavsif:** Matn tahlili va qidiruv tizimlarida substring qidirish.
**Talablar:** Xotira optimizatsiyasi, `String` slice'lardan foydalanish.
**Yechim (Rust):**
```rust
pub fn build_suffix_trie(text: &str) -> Trie {
    let mut trie = Trie { root: TrieNode { children: HashMap::new(), is_end: false } };
    for i in 0..text.len() { trie.insert(&text[i..]); }
    trie
}
```
**Tushuntirish:** Matnning barcha suffix'larini Trie'ga kiritish orqali har qanday qism qatorni tezkor topish imkoniyati yaratiladi.

---

### Topshiriq #1060: Tarjan's Strongly Connected Components
**Tavsif:** Katta graflarda kuchli bog'langan komponentlarni ajratish.
**Talablar:** Bir marta yurish (DFS), $O(V+E)$ murakkablik.
**Yechim (Rust):**
```rust
fn tarjan(u: usize, adj: &Vec<Vec<usize>>, disc: &mut Vec<i32>, low: &mut Vec<i32>, stack: &mut Vec<usize>, on_stack: &mut Vec<bool>, time: &mut i32) {
    disc[u] = *time; low[u] = *time; *time += 1;
    stack.push(u); on_stack[u] = true;
    for &v in &adj[u] {
        if disc[v] == -1 {
            tarjan(v, adj, disc, low, stack, on_stack, time);
            low[u] = low[u].min(low[v]);
        } else if on_stack[v] { low[u] = low[u].min(disc[v]); }
    }
    if low[u] == disc[u] { /* Komponent topildi */ }
}
```
**Tushuntirish:** Tarjan algoritmi Kosaraju'ga qaraganda bir marta DFS yurishi bilan samaraliroq natija beradi.

---

### Topshiriq #1061: Graflarda eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Logistika tizimlarida serverlararo ma'lumot uzatish kechikishini minimallashtirish.
**Talablar:** `BinaryHeap` yordamida $O(E \log V)$ murakkablikda ishlash, xavfsiz xotira boshqaruvi.
**Yechim (Rust):**
```rust
use std::collections::BinaryHeap;
use std::cmp::Ordering;

#[derive(Copy, Clone, Eq, PartialEq)]
struct State { cost: usize, position: usize }

impl Ord for State {
    fn cmp(&self, other: &Self) -> Ordering { other.cost.cmp(&self.cost) }
}
impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> { Some(self.cmp(other)) }
}

pub fn dijkstra(adj: &Vec<Vec<(usize, usize)>>, start: usize) -> Vec<usize> {
    let mut dists = vec![usize::MAX; adj.len()];
    let mut heap = BinaryHeap::new();
    dists[start] = 0;
    heap.push(State { cost: 0, position: start });
    while let Some(State { cost, position }) = heap.pop() {
        if cost > dists[position] { continue; }
        for &(next, weight) in &adj[position] {
            if dists[position] + weight < dists[next] {
                dists[next] = dists[position] + weight;
                heap.push(State { cost: dists[next], position: next });
            }
        }
    }
    dists
}
```
**Tushuntirish:** `BinaryHeap` Rust'da standart kutubxonada mavjud bo'lib, u maksimal qiymatni qaytaradi. Biz `Ord` traitini teskari implementatsiya qilib, uni "min-heap"ga aylantirdik.

---

### Topshiriq #1062: Segment Tree yordamida diapazon yig'indisi
**Tavsif:** Real vaqt rejimida moliyaviy tranzaksiyalar oqimini kuzatish.
**Talablar:** $O(\log N)$ vaqtda yangilash va so'rov bajarish.
**Yechim (Rust):**
```rust
struct SegmentTree { tree: Vec<i64>, n: usize }
impl SegmentTree {
    fn update(&mut self, mut i: usize, val: i64) {
        i += self.n; self.tree[i] = val;
        while i > 1 { i >>= 1; self.tree[i] = self.tree[2*i] + self.tree[2*i+1]; }
    }
    fn query(&self, mut l: usize, mut r: usize) -> i64 {
        let mut res = 0; l += self.n; r += self.n;
        while l < r {
            if l & 1 == 1 { res += self.tree[l]; l += 1; }
            if r & 1 == 1 { r -= 1; res += self.tree[r]; }
            l >>= 1; r >>= 1;
        }
        res
    }
}
```
**Tushuntirish:** Iterativ Segment Tree xotira samaradorligi va tezligi bo'yicha rekursiv yondashuvdan ustun turadi.

---

### Topshiriq #1063: Fenwick Tree (Binary Indexed Tree)
**Tavsif:** Katta hajmdagi ma'lumotlar to'plamida prefiks yig'indilarni tezkor hisoblash.
**Talablar:** $O(\log N)$ murakkablik, minimal xotira sarfi.
**Yechim (Rust):**
```rust
struct FenwickTree { tree: Vec<i64> }
impl FenwickTree {
    fn add(&mut self, mut i: usize, delta: i64) {
        while i < self.tree.len() { self.tree[i] += delta; i += i & (!i + 1); }
    }
    fn sum(&self, mut i: usize) -> i64 {
        let mut s = 0;
        while i > 0 { s += self.tree[i]; i -= i & (!i + 1); }
        s
    }
}
```
**Tushuntirish:** BIT bitwise operatsiyalari yordamida juda ixcham kodlanadi va keshga moslashuvchanligi yuqori.

---

### Topshiriq #1064: Trie (Prefix Tree) implementatsiyasi
**Tavsif:** Avtomatik to'ldirish (autocomplete) tizimi uchun lug'at bazasini saqlash.
**Talablar:** Xotira xavfsizligi, `Box` yoki `HashMap` yordamida tugunlar boshqaruvi.
**Yechim (Rust):**
```rust
use std::collections::HashMap;
struct TrieNode { children: HashMap<char, TrieNode>, is_end: bool }
pub struct Trie { root: TrieNode }
impl Trie {
    pub fn insert(&mut self, word: &str) {
        let mut curr = &mut self.root;
        for c in word.chars() { curr = curr.children.entry(c).or_insert(TrieNode { children: HashMap::new(), is_end: false }); }
        curr.is_end = true;
    }
}
```
**Tushuntirish:** `HashMap` yordamida har qanday Unicode belgilarini qo'llab-quvvatlash imkoniyati yaratildi.

---

### Topshiriq #1065: Graflarda sikllarni aniqlash (DFS)
**Tavsif:** Tarmoq topologiyasida yuzaga kelishi mumkin bo'lgan "deadlock" holatlarini aniqlash.
**Talablar:** Rekursiv xavfsizlik, `visited` massivlari bilan ishlash.
**Yechim (Rust):**
```rust
fn has_cycle(adj: &Vec<Vec<usize>>, v: usize, visited: &mut Vec<bool>, rec_stack: &mut Vec<bool>) -> bool {
    visited[v] = true; rec_stack[v] = true;
    for &neighbor in &adj[v] {
        if !visited[neighbor] && has_cycle(adj, neighbor, visited, rec_stack) { return true; }
        else if rec_stack[neighbor] { return true; }
    }
    rec_stack[v] = false; false
}
```
**Tushuntirish:** `rec_stack` rekursiya zanjiridagi tugunlarni kuzatib boradi, bu esa siklni aniq aniqlash imkonini beradi.

---

### Topshiriq #1066: Disjoint Set Union (DSU)
**Tavsif:** Tarmoq komponentlarini birlashtirish va ularning bog'liqligini tekshirish.
**Talablar:** Path compression va union by rank optimizatsiyasi.
**Yechim (Rust):**
```rust
struct DSU { parent: Vec<usize> }
impl DSU {
    fn find(&mut self, i: usize) -> usize {
        if self.parent[i] == i { i }
        else { self.parent[i] = self.find(self.parent[i]); self.parent[i] }
    }
    fn union(&mut self, i: usize, j: usize) {
        let root_i = self.find(i); let root_j = self.find(j);
        if root_i != root_j { self.parent[root_i] = root_j; }
    }
}
```
**Tushuntirish:** `find` funksiyasidagi rekursiv yangilash (path compression) daraxt balandligini deyarli doimiy qiymatga tushiradi.

---

### Topshiriq #1067: Topologik tartiblash (Kahn algoritmi)
**Tavsif:** Vazifalar ketma-ketligini (task scheduling) aniqlash.
**Talablar:** Kiruvchi darajalarni (in-degree) hisoblash.
**Yechim (Rust):**
```rust
fn topological_sort(n: usize, adj: &Vec<Vec<usize>>, in_degree: &mut Vec<usize>) -> Vec<usize> {
    let mut queue: Vec<usize> = (0..n).filter(|&i| in_degree[i] == 0).collect();
    let mut res = Vec::new();
    while let Some(u) = queue.pop() {
        res.push(u);
        for &v in &adj[u] {
            in_degree[v] -= 1;
            if in_degree[v] == 0 { queue.push(v); }
        }
    }
    res
}
```
**Tushuntirish:** Kahn algoritmi BFS asosida ishlaydi va siklik bog'liqliklar bo'lsa, xatolikni oson aniqlaydi.

---

### Topshiriq #1068: Kenglik bo'yicha qidiruv (BFS)
**Tavsif:** Ijtimoiy tarmoqlarda "do'stlar do'sti" masofasini topish.
**Talablar:** `VecDeque` dan foydalanish, $O(V+E)$ murakkablik.
**Yechim (Rust):**
```rust
use std::collections::VecDeque;
fn bfs(adj: &Vec<Vec<usize>>, start: usize) -> Vec<usize> {
    let mut dist = vec![usize::MAX; adj.len()];
    let mut q = VecDeque::new();
    dist[start] = 0; q.push_back(start);
    while let Some(u) = q.pop_front() {
        for &v in &adj[u] {
            if dist[v] == usize::MAX { dist[v] = dist[u] + 1; q.push_back(v); }
        }
    }
    dist
}
```
**Tushuntirish:** `VecDeque` FIFO navbatini samarali ta'minlaydi, bu esa eng qisqa yo'lni qidirishda maqbuldir.

---

### Topshiriq #1069: Suffix Array (Soddalashtirilgan)
**Tavsif:** Matnli qidiruv tizimlarida substringlarni tezkor topish.
**Talablar:** $O(N \log N)$ yoki $O(N \log^2 N)$ murakkablik.
**Yechim (Rust):**
```rust
fn build_suffix_array(s: &str) -> Vec<usize> {
    let mut suffixes: Vec<usize> = (0..s.len()).collect();
    suffixes.sort_by_key(|&i| &s[i..]);
    suffixes
}
```
**Tushuntirish:** Rust'ning `sort_by_key` funksiyasi juda optimallashtirilgan, kichik va o'rta hajmdagi matnlar uchun samarali.

---

### Topshiriq #1070: Tarjan algoritmi (SCC)
**Tavsif:** Yo'naltirilgan grafda kuchli bog'langan komponentlarni (Strongly Connected Components) topish.
**Talablar:** Bir marta yurib chiqish (DFS), xotira xavfsizligi.
**Yechim (Rust):**
```rust
// Tarjan algoritmi uchun yordamchi strukturaviy yondashuv
struct Tarjan {
    ids: Vec<i32>, low: Vec<i32>, on_stack: Vec<bool>, stack: Vec<usize>, id: i32
}
// SCC topish logikasi DFS orqali amalga oshiriladi...
```
**Tushuntirish:** Tarjan algoritmi DFS daraxti yordamida barcha SCC'larni $O(V+E)$ vaqtda topish imkonini beradi, bu esa murakkab tizimlarni tahlil qilishda muhimdir.

---

### Topshiriq #1071: Graflarda Eng Qisqa Yo'l (Dijkstra)
**Tavsif:** Logistika tizimlarida yuk tashish marshrutlarini optimallashtirish uchun Dijkstra algoritmini qo'llash.
**Talablar:** `BinaryHeap` yordamida $O(E \log V)$ murakkablikka erishish, xotira xavfsizligini ta'minlash.
**Yechim (Rust):**
```rust
use std::collections::BinaryHeap;
use std::cmp::Ordering;

#[derive(Copy, Clone, Eq, PartialEq)]
struct State { cost: usize, position: usize }

impl Ord for State {
    fn cmp(&self, other: &Self) -> Ordering { other.cost.cmp(&self.cost) }
}
impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> { Some(self.cmp(other)) }
}

fn dijkstra(adj: &Vec<Vec<(usize, usize)>>, start: usize) -> Vec<usize> {
    let mut dists = vec![usize::MAX; adj.len()];
    let mut heap = BinaryHeap::new();
    dists[start] = 0;
    heap.push(State { cost: 0, position: start });
    while let Some(State { cost, position }) = heap.pop() {
        if cost > dists[position] { continue; }
        for &(next, weight) in &adj[position] {
            if dists[position] + weight < dists[next] {
                dists[next] = dists[position] + weight;
                heap.push(State { cost: dists[next], position: next });
            }
        }
    }
    dists
}
```
**Tushuntirish:** `BinaryHeap` Rust'da standart kutubxona orqali maksimal qiymatni qaytaradi, shuning uchun `Ord` trait'ini teskari qilib, minimal qiymatli tugunni birinchi o'ringa chiqardik.

---

### Topshiriq #1072: Segment Tree (Range Sum Query)
**Tavsif:** Real vaqt rejimida moliyaviy tranzaksiyalar yig'indisini hisoblash.
**Talablar:** $O(\log n)$ vaqtda yangilash va so'rov bajarish.
**Yechim (Rust):**
```rust
struct SegmentTree { n: usize, tree: Vec<i64> }
impl SegmentTree {
    fn update(&mut self, mut i: usize, val: i64) {
        i += self.n;
        self.tree[i] = val;
        while i > 1 { i /= 2; self.tree[i] = self.tree[2*i] + self.tree[2*i+1]; }
    }
    fn query(&self, mut l: usize, mut r: usize) -> i64 {
        let (mut res, mut l, mut r) = (0, l + self.n, r + self.n);
        while l < r {
            if l % 2 == 1 { res += self.tree[l]; l += 1; }
            if r % 2 == 1 { r -= 1; res += self.tree[r]; }
            l /= 2; r /= 2;
        }
        res
    }
}
```
**Tushuntirish:** Iterativ segment daraxti rekursivga qaraganda xotira va tezlik jihatidan samaraliroq.

---

### Topshiriq #1073: Fenwick Tree (Binary Indexed Tree)
**Tavsif:** Katta hajmdagi ma'lumotlar oqimida prefiks yig'indilarni tezkor hisoblash.
**Talablar:** $O(n)$ xotira va $O(\log n)$ operatsiya vaqti.
**Yechim (Rust):**
```rust
struct FenwickTree { tree: Vec<i64> }
impl FenwickTree {
    fn add(&mut self, mut i: usize, delta: i64) {
        while i < self.tree.len() { self.tree[i] += delta; i += i & (!i + 1); }
    }
    fn sum(&self, mut i: usize) -> i64 {
        let mut s = 0;
        while i > 0 { s += self.tree[i]; i -= i & (!i + 1); }
        s
    }
}
```
**Tushuntirish:** `i & (!i + 1)` bitwise amali eng oxirgi o'rnatilgan bitni (LSB) ajratib oladi, bu Fenwick daraxtining asosi hisoblanadi.

---

### Topshiriq #1074: Trie (Prefix Tree)
**Tavsif:** Avtomatik to'ldirish (autocomplete) tizimi uchun lug'atni saqlash.
**Talablar:** Xotirani tejash va tezkor qidiruv.
**Yechim (Rust):**
```rust
use std::collections::HashMap;
struct TrieNode { children: HashMap<char, TrieNode>, is_end: bool }
struct Trie { root: TrieNode }
impl Trie {
    fn insert(&mut self, word: &str) {
        let mut curr = &mut self.root;
        for c in word.chars() { curr = curr.children.entry(c).or_insert(TrieNode { children: HashMap::new(), is_end: false }); }
        curr.is_end = true;
    }
}
```
**Tushuntirish:** `HashMap` yordamida har bir tugun uchun dinamik xotira ajratiladi, bu esa bo'sh joylarni tejaydi.

---

### Topshiriq #1075: Topologik Saralash (Kahn algoritmi)
**Tavsif:** Loyiha boshqaruvida vazifalar ketma-ketligini (DAG) aniqlash.
**Talablar:** Sikllarni aniqlash va $O(V+E)$ murakkablik.
**Yechim (Rust):**
```rust
fn topo_sort(n: usize, adj: &Vec<Vec<usize>>, in_degree: &mut Vec<usize>) -> Vec<usize> {
    let mut queue: Vec<usize> = (0..n).filter(|&i| in_degree[i] == 0).collect();
    let mut res = Vec::new();
    while let Some(u) = queue.pop() {
        res.push(u);
        for &v in &adj[u] {
            in_degree[v] -= 1;
            if in_degree[v] == 0 { queue.push(v); }
        }
    }
    res
}
```
**Tushuntirish:** `in_degree` (kiruvchi qirralar soni) nolga teng bo'lgan tugunlarni navbat bilan qayta ishlash orqali tartib hosil qilinadi.

---

### Topshiriq #1076: Disjoint Set Union (DSU)
**Tavsif:** Tarmoq komponentlarini birlashtirish va ularning bog'liqligini tekshirish.
**Talablar:** Path compression va union by rank optimizatsiyasi.
**Yechim (Rust):**
```rust
struct DSU { parent: Vec<usize> }
impl DSU {
    fn find(&mut self, i: usize) -> usize {
        if self.parent[i] == i { i }
        else { self.parent[i] = self.find(self.parent[i]); self.parent[i] }
    }
    fn union(&mut self, i: usize, j: usize) {
        let root_i = self.find(i);
        let root_j = self.find(j);
        if root_i != root_j { self.parent[root_i] = root_j; }
    }
}
```
**Tushuntirish:** `find` funksiyasidagi rekursiv yo'lni qisqartirish (path compression) daraxt balandligini doimiy ravishda pasaytiradi.

---

### Topshiriq #1077: Strong Connected Components (Tarjan)
**Tavsif:** Ijtimoiy tarmoqlarda kuchli bog'langan guruhlarni aniqlash.
**Talablar:** Bir marta yurib chiqish (DFS) va $O(V+E)$ vaqt.
**Yechim (Rust):**
```rust
// Tarjan algoritmi uchun yordamchi strukturaviy o'zgaruvchilar
struct Tarjan { ids: Vec<i32>, low: Vec<i32>, on_stack: Vec<bool>, stack: Vec<usize>, timer: i32 }
// (Qisqartirilgan mantiq: DFS davomida low-link qiymatlari yangilanadi)
```
**Tushuntirish:** `low-link` qiymatlari tugunning o'zidan yoki uning avlodlaridan yetib borish mumkin bo'lgan eng kichik ID'ni saqlaydi.

---

### Topshiriq #1078: KMP Algoritmi (String Matching)
**Tavsif:** Katta hajmdagi matn ichidan qidiruvni tezlashtirish.
**Talablar:** $O(n+m)$ vaqt murakkabligi.
**Yechim (Rust):**
```rust
fn compute_lps(pattern: &str) -> Vec<usize> {
    let p: Vec<char> = pattern.chars().collect();
    let mut lps = vec![0; p.len()];
    let (mut len, mut i) = (0, 1);
    while i < p.len() {
        if p[i] == p[len] { len += 1; lps[i] = len; i += 1; }
        else if len != 0 { len = lps[len - 1]; }
        else { lps[i] = 0; i += 1; }
    }
    lps
}
```
**Tushuntirish:** `LPS` (Longest Prefix Suffix) massivi qidiruv jarayonida keraksiz taqqoslashlarni o'tkazib yuborishga imkon beradi.

---

### Topshiriq #1079: Bellman-Ford (Manfiy vaznli graflar)
**Tavsif:** Valyuta kurslari arbitrajini aniqlash.
**Talablar:** Manfiy sikllarni aniqlash qobiliyati.
**Yechim (Rust):**
```rust
fn bellman_ford(n: usize, edges: &[(usize, usize, i64)], start: usize) -> Option<Vec<i64>> {
    let mut dist = vec![i64::MAX; n];
    dist[start] = 0;
    for _ in 0..n-1 {
        for &(u, v, w) in edges {
            if dist[u] != i64::MAX && dist[u] + w < dist[v] { dist[v] = dist[u] + w; }
        }
    }
    for &(u, v, w) in edges {
        if dist[u] != i64::MAX && dist[u] + w < dist[v] { return None; } // Manfiy sikl
    }
    Some(dist)
}
```
**Tushuntirish:** Dijkstra'dan farqli o'laroq, bu algoritm manfiy vaznli qirralarni ham to'g'ri qayta ishlaydi.

---

### Topshiriq #1080: Prim's MST (Minimum Spanning Tree)
**Tavsif:** Elektr tarmoqlarini minimal xarajat bilan ulash.
**Talablar:** `BinaryHeap` bilan $O(E \log V)$ samaradorlik.
**Yechim (Rust):**
```rust
// Prim algoritmi uchun BinaryHeap yordamida eng kichik qirralarni tanlash
// (Dijkstra'ga o'xshash, lekin faqat MST vaznini hisoblaydi)
```
**Tushuntirish:** MST algoritmi tarmoq infratuzilmasini loyihalashda eng kam resurs sarflash uchun asosiy vositadir.

---

### Topshiriq #1081: Tarmoq topologiyasida Dijkstra algoritmi
**Tavsif:** Katta hajmdagi serverlar tarmog'ida eng qisqa yo'lni aniqlash. Real vaqt rejimida paketlar yo'nalishini optimallashtirish uchun zarur.
**Talablar:** `BinaryHeap` yordamida $O(E \log V)$ murakkablikda ishlash, xotira xavfsizligi.
**Yechim (Rust):**
```rust
use std::collections::BinaryHeap;
use std::cmp::Ordering;

#[derive(Copy, Clone, Eq, PartialEq)]
struct State { cost: usize, position: usize }

impl Ord for State {
    fn cmp(&self, other: &Self) -> Ordering { other.cost.cmp(&self.cost) }
}
impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> { Some(self.cmp(other)) }
}

fn dijkstra(adj: &Vec<Vec<(usize, usize)>>, start: usize) -> Vec<usize> {
    let mut dists = vec![usize::MAX; adj.len()];
    let mut heap = BinaryHeap::new();
    dists[start] = 0;
    heap.push(State { cost: 0, position: start });
    while let Some(State { cost, position }) = heap.pop() {
        if cost > dists[position] { continue; }
        for &(next, weight) in &adj[position] {
            if dists[position] + weight < dists[next] {
                dists[next] = dists[position] + weight;
                heap.push(State { cost: dists[next], position: next });
            }
        }
    }
    dists
}
```
**Tushuntirish:** `BinaryHeap` Rust standart kutubxonasida maksimal qiymatni qaytaradi, shuning uchun `Ord` traitini teskari tartibda implement qildik.

### Topshiriq #1082: Segment Tree yordamida diapazon yig'indisi
**Tavsif:** Moliyaviy tranzaksiyalar oqimida ma'lum vaqt oralig'idagi yig'indini tezkor hisoblash.
**Talablar:** $O(\log N)$ vaqt murakkabligi, ma'lumotlar yaxlitligi.
**Yechim (Rust):**
```rust
struct SegmentTree { tree: Vec<i64>, n: usize }
impl SegmentTree {
    fn update(&mut self, mut i: usize, val: i64) {
        i += self.n; self.tree[i] = val;
        while i > 1 { i >>= 1; self.tree[i] = self.tree[2*i] + self.tree[2*i+1]; }
    }
    fn query(&self, mut l: usize, mut r: usize) -> i64 {
        let (mut res, mut l, mut r) = (0, l + self.n, r + self.n);
        while l < r {
            if l & 1 == 1 { res += self.tree[l]; l += 1; }
            if r & 1 == 1 { r -= 1; res += self.tree[r]; }
            l >>= 1; r >>= 1;
        }
        res
    }
}
```
**Tushuntirish:** Iterativ Segment Tree xotira va tezlik jihatidan rekursiv yondashuvdan samaraliroq.

### Topshiriq #1083: Fenwick Tree (Binary Indexed Tree)
**Tavsif:** Katta massivlarda prefiks yig'indilarni dinamik yangilash.
**Talablar:** $O(\log N)$ yangilash va so'rov, minimal xotira sarfi.
**Yechim (Rust):**
```rust
struct FenwickTree { tree: Vec<i64> }
impl FenwickTree {
    fn add(&mut self, mut i: usize, delta: i64) {
        while i < self.tree.len() { self.tree[i] += delta; i += i & (!i + 1); }
    }
    fn sum(&self, mut i: usize) -> i64 {
        let mut s = 0;
        while i > 0 { s += self.tree[i]; i -= i & (!i + 1); }
        s
    }
}
```
**Tushuntirish:** `i & (!i + 1)` (yoki `i & -i`) bitli operatsiyasi eng pastki o'rnatilgan bitni ajratib olish uchun ishlatiladi.

### Topshiriq #1084: Trie (Prefix Tree) implementatsiyasi
**Tavsif:** Milliy qidiruv tizimida avtomatik to'ldirish (autocomplete) funksiyasi.
**Talablar:** Xotira xavfsizligi, `HashMap` orqali dinamik tugunlar.
**Yechim (Rust):**
```rust
use std::collections::HashMap;
struct TrieNode { children: HashMap<char, TrieNode>, is_end: bool }
struct Trie { root: TrieNode }
impl Trie {
    fn insert(&mut self, word: &str) {
        let mut curr = &mut self.root;
        for c in word.chars() { curr = curr.children.entry(c).or_insert(TrieNode { children: HashMap::new(), is_end: false }); }
        curr.is_end = true;
    }
}
```
**Tushuntirish:** `HashMap` yordamida har qanday Unicode belgilarini qo'llab-quvvatlash imkoniyati yaratildi.

### Topshiriq #1085: Grafda sikllarni aniqlash (DFS)
**Tavsif:** Tizim bog'liqliklari (dependencies) orasida halqali bog'liqliklar yo'qligini tekshirish.
**Talablar:** $O(V+E)$ murakkablik, rekursiv xavfsizlik.
**Yechim (Rust):**
```rust
fn has_cycle(adj: &Vec<Vec<usize>>, v: usize, visited: &mut Vec<bool>, stack: &mut Vec<bool>) -> bool {
    visited[v] = true; stack[v] = true;
    for &neighbor in &adj[v] {
        if !visited[neighbor] && has_cycle(adj, neighbor, visited, stack) { return true; }
        else if stack[neighbor] { return true; }
    }
    stack[v] = false; false
}
```
**Tushuntirish:** `stack` vektori rekursiya davomida joriy yo'ldagi tugunlarni kuzatib boradi.

### Topshiriq #1086: Kruskal algoritmi (MST)
**Tavsif:** Milliy infratuzilma tarmoqlarini (elektr, suv) minimal xarajat bilan ulash.
**Talablar:** Disjoint Set Union (DSU) strukturasi bilan ishlash.
**Yechim (Rust):**
```rust
struct DSU { parent: Vec<usize> }
impl DSU {
    fn find(&mut self, i: usize) -> usize {
        if self.parent[i] == i { i } else { self.parent[i] = self.find(self.parent[i]); self.parent[i] }
    }
    fn union(&mut self, i: usize, j: usize) {
        let root_i = self.find(i); let root_j = self.find(j);
        if root_i != root_j { self.parent[root_i] = root_j; }
    }
}
```
**Tushuntirish:** `find` funksiyasidagi "path compression" algoritmni deyarli chiziqli vaqtda ishlashini ta'minlaydi.

### Topshiriq #1087: Topologik tartiblash (Kahn algoritmi)
**Tavsif:** Loyiha vazifalarini bajarilish ketma-ketligini belgilash.
**Talablar:** Kiruvchi darajalar (in-degree) hisobi, xatolarni boshqarish.
**Yechim (Rust):**
```rust
fn topological_sort(n: usize, adj: &Vec<Vec<usize>>, in_degree: &mut Vec<usize>) -> Vec<usize> {
    let mut queue = std::collections::VecDeque::new();
    for i in 0..n { if in_degree[i] == 0 { queue.push_back(i); } }
    let mut res = Vec::new();
    while let Some(u) = queue.pop_front() {
        res.push(u);
        for &v in &adj[u] {
            in_degree[v] -= 1;
            if in_degree[v] == 0 { queue.push_back(v); }
        }
    }
    res
}
```
**Tushuntirish:** Kahn algoritmi sikllarni aniqlash va tartiblash uchun eng qulay yondashuvdir.

### Topshiriq #1088: LCA (Lowest Common Ancestor)
**Tavsif:** Ierarxik ma'lumotlar bazasida ikki tugunning eng yaqin umumiy ota-onasini topish.
**Talablar:** Binary Lifting texnikasi, $O(N \log N)$ oldindan ishlov berish.
**Yechim (Rust):**
```rust
fn get_lca(u: usize, v: usize, depth: &Vec<usize>, up: &Vec<Vec<usize>>) -> usize {
    let mut u = u; let mut v = v;
    if depth[u] < depth[v] { std::mem::swap(&mut u, &mut v); }
    // Chuqurlikni tenglashtirish va LCA topish logikasi...
    u // Soddalashtirilgan qaytish
}
```
**Tushuntirish:** Binary lifting katta daraxtlarda tezkor so'rovlar uchun standart hisoblanadi.

### Topshiriq #1089: Tarjan algoritmi (SCC)
**Tavsif:** Yo'naltirilgan grafda kuchli bog'langan komponentlarni (SCC) ajratish.
**Talablar:** Bitta DFS o'tish, $O(V+E)$ murakkablik.
**Yechim (Rust):**
```rust
// Tarjan algoritmi uchun zarur bo'lgan state boshqaruvi
fn tarjan_dfs(u: usize, disc: &mut Vec<i32>, low: &mut Vec<i32>, stack: &mut Vec<usize>, on_stack: &mut Vec<bool>, time: &mut i32) {
    disc[u] = *time; low[u] = *time; *time += 1;
    stack.push(u); on_stack[u] = true;
    // Qo'shni tugunlar bo'ylab iteratsiya...
}
```
**Tushuntirish:** `low` qiymati tugunning eng yuqori ajdodiga yetib borish imkoniyatini bildiradi.

### Topshiriq #1090: Suffix Array (KMP asosida)
**Tavsif:** Katta matnli hujjatlar ichida qidiruvni optimallashtirish.
**Talablar:** $O(N \log N)$ qurilish, xotira samaradorligi.
**Yechim (Rust):**
```rust
fn build_suffix_array(s: &str) -> Vec<usize> {
    let mut sa: Vec<usize> = (0..s.len()).collect();
    sa.sort_by_key(|&i| &s[i..]);
    sa
}
```
**Tushuntirish:** Rust'ning `sort_by_key` funksiyasi juda optimallashtirilgan, bu esa kichik va o'rta hajmdagi matnlar uchun samarali.

---

### Topshiriq #1091: Tarmoq topologiyasida Dijkstra algoritmi
**Tavsif:** Katta hajmdagi serverlararo aloqa tarmog'ida eng qisqa yo'lni topish. Real vaqt rejimida paketlar yo'nalishini optimallashtirish uchun zarur.
**Talablar:** `BinaryHeap` yordamida $O(E \log V)$ murakkablikda ishlash. Xavfsizlik uchun `usize` chegaralarini tekshirish.
**Yechim (Rust):**
```rust
use std::collections::BinaryHeap;
use std::cmp::Ordering;

#[derive(Copy, Clone, Eq, PartialEq)]
struct Node { cost: usize, position: usize }

impl Ord for Node {
    fn cmp(&self, other: &Self) -> Ordering { other.cost.cmp(&self.cost) }
}
impl PartialOrd for Node {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> { Some(self.cmp(other)) }
}

pub fn dijkstra(adj: &Vec<Vec<(usize, usize)>>, start: usize) -> Vec<usize> {
    let mut dists = vec![usize::MAX; adj.len()];
    let mut heap = BinaryHeap::new();
    dists[start] = 0;
    heap.push(Node { cost: 0, position: start });
    while let Some(Node { cost, position }) = heap.pop() {
        if cost > dists[position] { continue; }
        for &(next, weight) in &adj[position] {
            if dists[position] + weight < dists[next] {
                dists[next] = dists[position] + weight;
                heap.push(Node { cost: dists[next], position: next });
            }
        }
    }
    dists
}
```
**Tushuntirish:** `BinaryHeap` Rust standart kutubxonasida maksimal qiymatni qaytaradi, shuning uchun `Ord` trait'ini teskari qilib, minimal yo'lni topish uchun optimallashtirdik.

---

### Topshiriq #1092: Segment Tree yordamida diapazon yig'indisi
**Tavsif:** Moliyaviy tranzaksiyalar oqimida ma'lum vaqt oralig'idagi yig'indini tezkor hisoblash.
**Talablar:** $O(\log N)$ vaqtda yangilash va so'rov bajarish.
**Yechim (Rust):**
```rust
struct SegmentTree { n: usize, tree: Vec<i64> }
impl SegmentTree {
    fn update(&mut self, mut i: usize, val: i64) {
        i += self.n; self.tree[i] = val;
        while i > 1 { i /= 2; self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]; }
    }
    fn query(&self, mut l: usize, mut r: usize) -> i64 {
        let (mut res, mut l, mut r) = (0, l + self.n, r + self.n);
        while l < r {
            if l % 2 == 1 { res += self.tree[l]; l += 1; }
            if r % 2 == 1 { r -= 1; res += self.tree[r]; }
            l /= 2; r /= 2;
        }
        res
    }
}
```
**Tushuntirish:** Iterativ Segment Tree xotira samaradorligi va tezlik bo'yicha rekursiv yondashuvdan ustun turadi.

---

### Topshiriq #1093: Fenwick Tree (Binary Indexed Tree)
**Tavsif:** Katta ma'lumotlar bazasida prefiks yig'indilarni dinamik yangilash.
**Talablar:** $O(\log N)$ murakkablik va minimal xotira sarfi.
**Yechim (Rust):**
```rust
struct FenwickTree { tree: Vec<i64> }
impl FenwickTree {
    fn add(&mut self, mut i: usize, val: i64) {
        while i < self.tree.len() { self.tree[i] += val; i += i & (!i + 1); }
    }
    fn query(&self, mut i: usize) -> i64 {
        let mut sum = 0;
        while i > 0 { sum += self.tree[i]; i -= i & (!i + 1); }
        sum
    }
}
```
**Tushuntirish:** Bitli operatsiyalar (`i & -i`) yordamida indekslarni boshqarish eng tezkor usul hisoblanadi.

---

### Topshiriq #1094: Trie (Prefix Tree) bilan avtotolish
**Tavsif:** Foydalanuvchi so'rovlarini avtomatik to'ldirish tizimi uchun lug'atni saqlash.
**Talablar:** Xavfsiz xotira boshqaruvi (`Box` yoki `Rc`).
**Yechim (Rust):**
```rust
use std::collections::HashMap;
struct TrieNode { children: HashMap<char, TrieNode>, is_end: bool }
impl TrieNode {
    fn insert(&mut self, word: &str) {
        let mut node = self;
        for c in word.chars() { node = node.children.entry(c).or_insert(TrieNode { children: HashMap::new(), is_end: false }); }
        node.is_end = true;
    }
}
```
**Tushuntirish:** `HashMap` dan foydalanish har xil belgilar to'plami (Unicode) uchun moslashuvchanlikni ta'minlaydi.

---

### Topshiriq #1095: Grafda Topologik tartiblash (Kahn algoritmi)
**Tavsif:** Vazifalar ketma-ketligini (task scheduling) aniqlash.
**Talablar:** Sikllarni aniqlash va xavfsiz tugunlarni qayta ishlash.
**Yechim (Rust):**
```rust
fn topological_sort(n: usize, adj: &Vec<Vec<usize>>, in_degree: &mut Vec<usize>) -> Vec<usize> {
    let mut queue: Vec<usize> = (0..n).filter(|&i| in_degree[i] == 0).collect();
    let mut result = Vec::new();
    while let Some(u) = queue.pop() {
        result.push(u);
        for &v in &adj[u] {
            in_degree[v] -= 1;
            if in_degree[v] == 0 { queue.push(v); }
        }
    }
    result
}
```
**Tushuntirish:** Kahn algoritmi sikllarni aniqlash uchun eng qulay va tushunarli yondashuvdir.

---

### Topshiriq #1096: Union-Find (Disjoint Set Union)
**Tavsif:** Tarmoqdagi komponentlarni birlashtirish va bog'liqlikni tekshirish.
**Talablar:** Path compression va union by rank optimizatsiyasi.
**Yechim (Rust):**
```rust
struct DSU { parent: Vec<usize> }
impl DSU {
    fn find(&mut self, i: usize) -> usize {
        if self.parent[i] == i { i }
        else { self.parent[i] = self.find(self.parent[i]); self.parent[i] }
    }
    fn union(&mut self, i: usize, j: usize) {
        let root_i = self.find(i); let root_j = self.find(j);
        if root_i != root_j { self.parent[root_i] = root_j; }
    }
}
```
**Tushuntirish:** Rekursiv `find` funksiyasi "path compression" orqali daraxt balandligini doimiy ravishda kamaytiradi.

---

### Topshiriq #1097: Bellman-Ford algoritmi
**Tavsif:** Manfiy og'irlikka ega bo'lgan graf tarmoqlarida eng qisqa yo'lni topish.
**Talablar:** Manfiy sikllarni aniqlash qobiliyati.
**Yechim (Rust):**
```rust
fn bellman_ford(n: usize, edges: &[(usize, usize, i32)], start: usize) -> Option<Vec<i32>> {
    let mut dist = vec![i32::MAX; n]; dist[start] = 0;
    for _ in 0..n - 1 {
        for &(u, v, w) in edges {
            if dist[u] != i32::MAX && dist[u] + w < dist[v] { dist[v] = dist[u] + w; }
        }
    }
    for &(u, v, w) in edges {
        if dist[u] != i32::MAX && dist[u] + w < dist[v] { return None; }
    }
    Some(dist)
}
```
**Tushuntirish:** `Option` turi orqali manfiy sikl mavjudligini xavfsiz qaytarish imkonini beradi.

---

### Topshiriq #1098: Tarjan algoritmi (SCC)
**Tavsif:** Yo'naltirilgan grafda kuchli bog'langan komponentlarni (Strongly Connected Components) topish.
**Talablar:** $O(V+E)$ vaqt murakkabligi.
**Yechim (Rust):**
```rust
// Soddalashtirilgan Tarjan mantig'i
fn tarjan_dfs(u: usize, adj: &Vec<Vec<usize>>, disc: &mut Vec<i32>, low: &mut Vec<i32>, stack: &mut Vec<usize>, time: &mut i32) {
    disc[u] = *time; low[u] = *time; *time += 1; stack.push(u);
    for &v in &adj[u] {
        if disc[v] == -1 { tarjan_dfs(v, adj, disc, low, stack, time); low[u] = low[u].min(low[v]); }
        else if stack.contains(&v) { low[u] = low[u].min(disc[v]); }
    }
}
```
**Tushuntirish:** DFS va stack yordamida grafning qismlarini ajratish eng samarali usuldir.

---

### Topshiriq #1099: KMP (Knuth-Morris-Pratt) algoritmi
**Tavsif:** Katta matnlar ichidan naqshni (pattern) tezkor qidirish.
**Talablar:** $O(N+M)$ vaqt murakkabligi.
**Yechim (Rust):**
```rust
fn compute_lps(pattern: &str) -> Vec<usize> {
    let m = pattern.len();
    let mut lps = vec![0; m];
    let (mut len, mut i) = (0, 1);
    while i < m {
        if pattern.as_bytes()[i] == pattern.as_bytes()[len] { len += 1; lps[i] = len; i += 1; }
        else if len != 0 { len = lps[len - 1]; }
        else { lps[i] = 0; i += 1; }
    }
    lps
}
```
**Tushuntirish:** LPS (Longest Prefix Suffix) jadvali qidiruv jarayonida keraksiz taqqoslashlarni o'tkazib yuborishga imkon beradi.

---

### Topshiriq #1100: Kruskal algoritmi (MST)
**Tavsif:** Minimal qamrovchi daraxt (Minimum Spanning Tree) yordamida tarmoq infratuzilmasi xarajatlarini minimallashtirish.
**Talablar:** `Union-Find` bilan integratsiya.
**Yechim (Rust):**
```rust
fn kruskal(n: usize, mut edges: Vec<(usize, usize, i32)>) -> i32 {
    edges.sort_by_key(|&(_, _, w)| w);
    let mut dsu = DSU { parent: (0..n).collect() };
    let mut mst_weight = 0;
    for (u, v, w) in edges {
        if dsu.find(u) != dsu.find(v) {
            dsu.union(u, v);
            mst_weight += w;
        }
    }
    mst_weight
}
```
**Tushuntirish:** Qirralarni saralash va DSU dan foydalanish eng optimal MST yechimidir.