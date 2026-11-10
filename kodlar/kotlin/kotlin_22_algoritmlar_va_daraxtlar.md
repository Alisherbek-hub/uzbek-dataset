# Khorazmiy AI: Kotlin - Modul 22
## Mavzu: Ilg'or Algoritmlar: Graflar, Segment Trees, Fenwick va Trie tuzilmalari

### Topshiriq #1051: Tarmoq topologiyasida eng qisqa yo'lni aniqlash (Dijkstra)
**Tavsif:** Katta hajmdagi serverlar tarmog'ida ma'lumotlar uzatish uchun eng kam kechikishli (latency) yo'lni topish.
**Talablar:** `PriorityQueue` yordamida $O(E \log V)$ murakkablikda ishlash, xavfsizlik uchun `null` xavfsizligini ta'minlash.
**Yechim (Kotlin):**
```kotlin
import java.util.PriorityQueue

data class Edge(val to: Int, val weight: Int)

fun findShortestPath(n: Int, graph: Array<MutableList<Edge>>, start: Int): IntArray {
    val dist = IntArray(n) { Int.MAX_VALUE }
    dist[start] = 0
    val pq = PriorityQueue<Pair<Int, Int>>(compareBy { it.second })
    pq.add(start to 0)

    while (pq.isNotEmpty()) {
        val (u, d) = pq.poll()
        if (d > dist[u]) continue
        for (edge in graph[u]) {
            if (dist[u] + edge.weight < dist[edge.to]) {
                dist[edge.to] = dist[u] + edge.weight
                pq.add(edge.to to dist[edge.to])
            }
        }
    }
    return dist
}
```
**Tushuntirish:** `PriorityQueue` yordamida eng kichik masofali tugunni tanlash orqali Dijkstra algoritmi optimallashtirildi.

### Topshiriq #1052: Segment Tree yordamida dinamik diapazon yig'indisi
**Tavsif:** Real vaqt rejimida o'zgaruvchan moliyaviy tranzaksiyalar qatorida ma'lum oraliqdagi yig'indini hisoblash.
**Talablar:** Yangilash va so'rov uchun $O(\log N)$ vaqt murakkabligi.
**Yechim (Kotlin):**
```kotlin
class SegmentTree(val size: Int, val data: IntArray) {
    private val tree = IntArray(4 * size)
    
    fun update(node: Int, start: Int, end: Int, idx: Int, value: Int) {
        if (start == end) { tree[node] = value; return }
        val mid = (start + end) / 2
        if (idx <= mid) update(2 * node, start, mid, idx, value)
        else update(2 * node + 1, mid + 1, end, idx, value)
        tree[node] = tree[2 * node] + tree[2 * node + 1]
    }

    fun query(node: Int, start: Int, end: Int, l: Int, r: Int): Int {
        if (r < start || end < l) return 0
        if (l <= start && end <= r) return tree[node]
        val mid = (start + end) / 2
        return query(2 * node, start, mid, l, r) + query(2 * node + 1, mid + 1, end, l, r)
    }
}
```
**Tushuntirish:** Segment Tree massivni daraxt ko'rinishida ifodalab, diapazonli so'rovlarni logarifmik vaqtda bajarish imkonini beradi.

### Topshiriq #1053: Fenwick Tree (Binary Indexed Tree) bilan tezkor statistikalar
**Tavsif:** Katta hajmdagi log fayllarida tez-tez o'zgarib turadigan qiymatlar uchun prefiks yig'indilarni hisoblash.
**Talablar:** Xotira tejamkorligi va $O(\log N)$ ishlash tezligi.
**Yechim (Kotlin):**
```kotlin
class FenwickTree(val size: Int) {
    private val tree = IntArray(size + 1)

    fun add(idx: Int, delta: Int) {
        var i = idx
        while (i <= size) { tree[i] += delta; i += i and -i }
    }

    fun query(idx: Int): Int {
        var i = idx; var sum = 0
        while (i > 0) { sum += tree[i]; i -= i and -i }
        return sum
    }
}
```
**Tushuntirish:** Fenwick Tree Segment Tree'ga qaraganda kamroq xotira talab qiladi va implementatsiyasi sodda.

### Topshiriq #1054: Trie (Prefix Tree) yordamida avtomatik to'ldirish
**Tavsif:** Foydalanuvchi kiritayotgan so'zlarni milliy lug'at bazasidan tezkor qidirish.
**Talablar:** So'zlarni qidirish $O(L)$ vaqtda (L - so'z uzunligi).
**Yechim (Kotlin):**
```kotlin
class TrieNode {
    val children = mutableMapOf<Char, TrieNode>()
    var isEndOfWord = false
}

class Trie {
    private val root = TrieNode()

    fun insert(word: String) {
        var curr = root
        for (char in word) curr = curr.children.getOrPut(char) { TrieNode() }
        curr.isEndOfWord = true
    }
}
```
**Tushuntirish:** Trie tuzilmasi so'zlarni prefikslar bo'yicha guruhlab, qidiruvni maksimal tezlashtiradi.

### Topshiriq #1055: Graflarda sikllarni aniqlash (DFS)
**Tavsif:** Tizim bog'liqliklarida (dependencies) yuzaga kelishi mumkin bo'lgan o'zaro bog'liqlik (deadlock) xavfini aniqlash.
**Talablar:** Rekursiv yondashuv va `visited` holatlarini kuzatish.
**Yechim (Kotlin):**
```kotlin
fun hasCycle(n: Int, adj: Array<MutableList<Int>>): Boolean {
    val visited = IntArray(n) // 0: unvisited, 1: visiting, 2: visited
    fun dfs(u: Int): Boolean {
        visited[u] = 1
        for (v in adj[u]) {
            if (visited[v] == 1) return true
            if (visited[v] == 0 && dfs(v)) return true
        }
        visited[u] = 2
        return false
    }
    return (0 until n).any { visited[it] == 0 && dfs(it) }
}
```
**Tushuntirish:** DFS orqali tugunlarning holatini kuzatish orqali yo'naltirilgan graflarda sikl borligini aniqlash mumkin.

### Topshiriq #1056: Kenglik bo'yicha qidiruv (BFS) - Eng qisqa yo'l
**Tavsif:** Og'irlanmagan graflarda (masalan, ijtimoiy tarmoq do'stlik aloqalari) ikki tugun orasidagi eng qisqa masofani topish.
**Talablar:** `Queue` ma'lumotlar tuzilmasidan foydalanish.
**Yechim (Kotlin):**
```kotlin
import java.util.LinkedList

fun bfsShortestPath(n: Int, adj: Array<MutableList<Int>>, start: Int, target: Int): Int {
    val dist = IntArray(n) { -1 }
    val queue = LinkedList<Int>()
    dist[start] = 0
    queue.add(start)
    while (queue.isNotEmpty()) {
        val u = queue.poll()
        if (u == target) return dist[u]
        for (v in adj[u]) {
            if (dist[v] == -1) {
                dist[v] = dist[u] + 1
                queue.add(v)
            }
        }
    }
    return -1
}
```
**Tushuntirish:** BFS qatlamma-qatlam qidirganligi sababli, og'irlanmagan graflarda eng qisqa yo'lni kafolatlaydi.

### Topshiriq #1057: Union-Find (Disjoint Set Union)
**Tavsif:** Tarmoq segmentlarini birlashtirish va ular orasidagi bog'liqlikni tekshirish.
**Talablar:** `Path Compression` va `Union by Rank` optimizatsiyalari.
**Yechim (Kotlin):**
```kotlin
class DSU(n: Int) {
    private val parent = IntArray(n) { it }
    fun find(i: Int): Int {
        if (parent[i] == i) return i
        parent[i] = find(parent[i]) // Path compression
        return parent[i]
    }
    fun union(i: Int, j: Int) {
        val rootI = find(i); val rootJ = find(j)
        if (rootI != rootJ) parent[rootI] = rootJ
    }
}
```
**Tushuntirish:** DSU operatsiyalari deyarli doimiy vaqtda ($O(\alpha(N))$) ishlaydi, bu esa katta tarmoqlarni boshqarishda juda samarali.

### Topshiriq #1058: Kruskal algoritmi (Minimum Spanning Tree)
**Tavsif:** Tarmoq infratuzilmasini eng kam xarajat bilan bog'lash.
**Talablar:** Edge'larni vazn bo'yicha saralash va DSU'dan foydalanish.
**Yechim (Kotlin):**
```kotlin
data class Edge(val u: Int, val v: Int, val weight: Int)

fun kruskal(n: Int, edges: MutableList<Edge>): Int {
    edges.sortBy { it.weight }
    val dsu = DSU(n)
    var mstWeight = 0
    for (edge in edges) {
        if (dsu.find(edge.u) != dsu.find(edge.v)) {
            dsu.union(edge.u, edge.v)
            mstWeight += edge.weight
        }
    }
    return mstWeight
}
```
**Tushuntirish:** Kruskal algoritmi eng arzon aloqalarni tanlab, minimal bog'langan daraxtni quradi.

### Topshiriq #1059: Trie bilan so'zlarni o'chirish va xotirani boshqarish
**Tavsif:** Lug'at bazasidan so'zlarni xavfsiz o'chirish va foydalanilmayotgan tugunlarni tozalash.
**Talablar:** Rekursiv o'chirish va xotira sizib chiqishining oldini olish.
**Yechim (Kotlin):**
```kotlin
fun delete(node: TrieNode, word: String, depth: Int): Boolean {
    if (depth == word.length) {
        node.isEndOfWord = false
        return node.children.isEmpty()
    }
    val char = word[depth]
    val child = node.children[char] ?: return false
    if (delete(child, word, depth + 1)) {
        node.children.remove(char)
        return node.children.isEmpty() && !node.isEndOfWord
    }
    return false
}
```
**Tushuntirish:** Rekursiv yondashuv orqali ortiqcha tugunlar o'chiriladi, bu esa Trie hajmini optimallashtiradi.

### Topshiriq #1060: Segment Tree bilan diapazonni yangilash (Lazy Propagation)
**Tavsif:** Katta massivda diapazon bo'yicha qiymatlarni o'zgartirish va yig'indini olish.
**Talablar:** $O(\log N)$ murakkablikda diapazonni yangilash.
**Yechim (Kotlin):**
```kotlin
class LazySegmentTree(val n: Int) {
    private val tree = LongArray(4 * n)
    private val lazy = LongArray(4 * n)

    private fun push(node: Int, start: Int, end: Int) {
        if (lazy[node] != 0L) {
            tree[node] += (end - start + 1) * lazy[node]
            if (start != end) {
                lazy[2 * node] += lazy[node]
                lazy[2 * node + 1] += lazy[node]
            }
            lazy[node] = 0
        }
    }
    // Update va Query funksiyalari push() ni chaqirishi kerak
}
```
**Tushuntirish:** Lazy Propagation o'zgarishlarni vaqtincha saqlab, faqat kerak bo'lganda qo'llaydi, bu esa ishlash tezligini keskin oshiradi.

---

### Topshiriq #1061: Tarmoq topologiyasida eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Katta hajmdagi serverlararo ma'lumotlar uzatish tarmog'ida kechikishni minimallashtirish uchun eng qisqa yo'lni aniqlash.
**Talablar:** `PriorityQueue` yordamida $O(E \log V)$ murakkablikda ishlash, xavfsizlik uchun `null` xavfsizligini ta'minlash.
**Yechim (Kotlin):**
```kotlin
import java.util.*

fun findShortestPath(graph: Map<Int, List<Pair<Int, Int>>>, start: Int): Map<Int, Int> {
    val distances = mutableMapOf<Int, Int>().withDefault { Int.MAX_VALUE }
    val pq = PriorityQueue<Pair<Int, Int>>(compareBy { it.second })
    
    distances[start] = 0
    pq.add(start to 0)
    
    while (pq.isNotEmpty()) {
        val (u, d) = pq.poll()
        if (d > (distances[u] ?: Int.MAX_VALUE)) continue
        
        graph[u]?.forEach { (v, weight) ->
            if ((distances[u] ?: Int.MAX_VALUE) + weight < (distances[v] ?: Int.MAX_VALUE)) {
                distances[v] = (distances[u] ?: 0) + weight
                pq.add(v to distances[v]!!)
            }
        }
    }
    return distances
}
```
**Tushuntirish:** Dijkstra algoritmi tarmoq kechikishlarini hisoblashda eng samarali yondashuvdir. `PriorityQueue` operatsiyalarni logarifmik vaqtda bajarish imkonini beradi.

---

### Topshiriq #1062: Dinamik diapazonli yig'indini hisoblash (Fenwick Tree)
**Tavsif:** Real vaqt rejimida tranzaksiyalar oqimining ma'lum oraliqdagi yig'indisini tezkor hisoblash.
**Talablar:** Yangilash va so'rovlar uchun $O(\log N)$ vaqt murakkabligi.
**Yechim (Kotlin):**
```kotlin
class FenwickTree(val size: Int) {
    private val tree = IntArray(size + 1)

    fun update(i: Int, delta: Int) {
        var idx = i + 1
        while (idx <= size) {
            tree[idx] += delta
            idx += idx and -idx
        }
    }

    fun query(i: Int): Int {
        var idx = i + 1
        var sum = 0
        while (idx > 0) {
            sum += tree[idx]
            idx -= idx and -idx
        }
        return sum
    }
}
```
**Tushuntirish:** Fenwick Tree (Binary Indexed Tree) xotira tejamkorligi va tezligi bilan Segment Tree'dan ustun turadi, ayniqsa prefiks yig'indilari uchun.

---

### Topshiriq #1063: Avtomatik to'ldirish tizimi (Trie)
**Tavsif:** Foydalanuvchi so'rovlarini tezkor qidirish va taklif etish uchun lug'at bazasini boshqarish.
**Talablar:** Prefix qidiruvda $O(L)$ vaqt murakkabligi (L - so'z uzunligi).
**Yechim (Kotlin):**
```kotlin
class TrieNode {
    val children = mutableMapOf<Char, TrieNode>()
    var isEndOfWord = false
}

class Trie {
    private val root = TrieNode()

    fun insert(word: String) {
        var current = root
        for (char in word) {
            current = current.children.getOrPut(char) { TrieNode() }
        }
        current.isEndOfWord = true
    }

    fun search(prefix: String): Boolean {
        var current = root
        for (char in prefix) {
            current = current.children[char] ?: return false
        }
        return true
    }
}
```
**Tushuntirish:** Trie tuzilmasi matnli qidiruv tizimlarida xotirani optimallashtirish va prefix qidiruvni tezlashtirish uchun standart hisoblanadi.

---

### Topshiriq #1064: Segment Tree yordamida Range Minimum Query (RMQ)
**Tavsif:** Katta massivlardagi eng kichik qiymatni dinamik yangilanishlar bilan topish.
**Talablar:** $O(\log N)$ vaqtda yangilash va qidirish.
**Yechim (Kotlin):**
```kotlin
class SegmentTree(val data: IntArray) {
    private val n = data.size
    private val tree = IntArray(2 * n)

    init {
        for (i in 0 until n) tree[n + i] = data[i]
        for (i in n - 1 downTo 1) tree[i] = minOf(tree[2 * i], tree[2 * i + 1])
    }

    fun update(i: Int, value: Int) {
        var pos = i + n
        tree[pos] = value
        while (pos > 1) {
            pos /= 2
            tree[pos] = minOf(tree[2 * pos], tree[2 * pos + 1])
        }
    }

    fun query(l: Int, r: Int): Int {
        var res = Int.MAX_VALUE
        var left = l + n; var right = r + n
        while (left < right) {
            if (left % 2 == 1) res = minOf(res, tree[left++])
            if (right % 2 == 1) res = minOf(res, tree[--right])
            left /= 2; right /= 2
        }
        return res
    }
}
```
**Tushuntirish:** Iterativ Segment Tree rekursiv yondashuvga qaraganda xotira va tezlik jihatidan ancha samaraliroq.

---

### Topshiriq #1065: Grafda sikllarni aniqlash (DFS)
**Tavsif:** Tizim bog'liqliklari (dependencies) orasida o'zaro bog'liqlik (deadlock) borligini tekshirish.
**Talablar:** $O(V + E)$ vaqt murakkabligi.
**Yechim (Kotlin):**
```kotlin
fun hasCycle(graph: Map<Int, List<Int>>, nodes: Int): Boolean {
    val visited = mutableSetOf<Int>()
    val recStack = mutableSetOf<Int>()

    fun dfs(u: Int): Boolean {
        visited.add(u)
        recStack.add(u)
        for (v in graph[u] ?: emptyList()) {
            if (v !in visited && dfs(v)) return true
            else if (v in recStack) return true
        }
        recStack.remove(u)
        return false
    }

    return (0 until nodes).any { it !in visited && dfs(it) }
}
```
**Tushuntirish:** Rekursiv stek (recStack) yordamida yo'naltirilgan grafdagi sikllarni aniqlash tizim xavfsizligi uchun muhimdir.

---

### Topshiriq #1066: Kenglik bo'yicha qidiruv (BFS) - Eng qisqa yo'l
**Tavsif:** Ijtimoiy tarmoq graflarida ikki foydalanuvchi orasidagi masofani (degrees of separation) topish.
**Talablar:** $O(V + E)$ vaqt murakkabligi.
**Yechim (Kotlin):**
```kotlin
fun bfsShortestPath(graph: Map<Int, List<Int>>, start: Int, target: Int): Int {
    val queue: Queue<Pair<Int, Int>> = LinkedList()
    val visited = mutableSetOf<Int>()
    
    queue.add(start to 0)
    visited.add(start)
    
    while (queue.isNotEmpty()) {
        val (u, dist) = queue.poll()
        if (u == target) return dist
        
        graph[u]?.forEach { v ->
            if (v !in visited) {
                visited.add(v)
                queue.add(v to dist + 1)
            }
        }
    }
    return -1
}
```
**Tushuntirish:** BFS vaznsiz graflarda eng qisqa yo'lni topish uchun eng optimal algoritmdir.

---

### Topshiriq #1067: Union-Find (Disjoint Set Union)
**Tavsif:** Tarmoq segmentlarini birlashtirish va ularning bog'liqligini tekshirish.
**Talablar:** Path compression va union by rank yordamida deyarli doimiy vaqt murakkabligi.
**Yechim (Kotlin):**
```kotlin
class DSU(n: Int) {
    private val parent = IntArray(n) { it }
    
    fun find(i: Int): Int {
        if (parent[i] == i) return i
        parent[i] = find(parent[i]) // Path compression
        return parent[i]
    }
    
    fun union(i: Int, j: Int) {
        val rootI = find(i)
        val rootJ = find(j)
        if (rootI != rootJ) parent[rootI] = rootJ
    }
}
```
**Tushuntirish:** DSU tarmoq komponentlarini boshqarishda juda tez va samarali vositadir.

---

### Topshiriq #1068: Topological Sort (Kahn's Algorithm)
**Tavsif:** Vazifalarni bajarish tartibini (task scheduling) ularning bog'liqliklari asosida belgilash.
**Talablar:** $O(V + E)$ vaqt murakkabligi.
**Yechim (Kotlin):**
```kotlin
fun topologicalSort(nodes: Int, adj: Map<Int, List<Int>>): List<Int> {
    val inDegree = IntArray(nodes)
    adj.values.flatten().forEach { inDegree[it]++ }
    val queue: Queue<Int> = LinkedList()
    (0 until nodes).filter { inDegree[it] == 0 }.forEach { queue.add(it) }
    
    val result = mutableListOf<Int>()
    while (queue.isNotEmpty()) {
        val u = queue.poll()
        result.add(u)
        adj[u]?.forEach { v ->
            inDegree[v]--
            if (inDegree[v] == 0) queue.add(v)
        }
    }
    return result
}
```
**Tushuntirish:** Kahn algoritmi siklsiz yo'naltirilgan graflar (DAG) uchun eng ishonchli tartiblash usulidir.

---

### Topshiriq #1069: Trie yordamida so'zlar sonini sanash
**Tavsif:** Katta matnlar to'plamida ma'lum bir so'zning necha marta takrorlanganligini aniqlash.
**Talablar:** Xotirani tejash va tezkor qidiruv.
**Yechim (Kotlin):**
```kotlin
class CountTrieNode {
    val children = mutableMapOf<Char, CountTrieNode>()
    var count = 0
}

fun insertAndCount(root: CountTrieNode, word: String) {
    var curr = root
    for (char in word) {
        curr = curr.children.getOrPut(char) { CountTrieNode() }
    }
    curr.count++
}
```
**Tushuntirish:** Trie tugunlariga `count` maydonini qo'shish orqali qidiruv va sanash jarayonini bir vaqtning o'zida amalga oshirish mumkin.

---

### Topshiriq #1070: Segment Tree (Lazy Propagation)
**Tavsif:** Massivning bir qismini yangilash (range update) va yig'indini so'rash (range query).
**Talablar:** $O(\log N)$ vaqt murakkabligi.
**Yechim (Kotlin):**
```kotlin
class LazySegmentTree(val n: Int) {
    private val tree = LongArray(4 * n)
    private val lazy = LongArray(4 * n)

    fun updateRange(node: Int, start: Int, end: Int, l: Int, r: Int, diff: Long) {
        if (lazy[node] != 0L) {
            tree[node] += (end - start + 1) * lazy[node]
            if (start != end) {
                lazy[2 * node] += lazy[node]
                lazy[2 * node + 1] += lazy[node]
            }
            lazy[node] = 0
        }
        if (start > end || start > r || end < l) return
        if (start >= l && end <= r) {
            tree[node] += (end - start + 1) * diff
            if (start != end) {
                lazy[2 * node] += diff
                lazy[2 * node + 1] += diff
            }
            return
        }
        val mid = (start + end) / 2
        updateRange(2 * node, start, mid, l, r, diff)
        updateRange(2 * node + 1, mid + 1, end, l, r, diff)
        tree[node] = tree[2 * node] + tree[2 * node + 1]
    }
}
```
**Tushuntirish:** Lazy propagation katta massivlarda oraliq yangilanishlarni kechiktirib bajarish orqali unumdorlikni keskin oshiradi.

---

### Topshiriq #1071: Tarmoq trafigini kuzatish (Segment Tree)
**Tavsif:** Katta hajmdagi serverlar klasterida real vaqt rejimida ma'lum diapazondagi trafik yig'indisini hisoblash.
**Talablar:** O(log n) vaqt murakkabligi, xavfsiz xotira boshqaruvi.
**Yechim (Kotlin):**
```kotlin
class SegmentTree(val size: Int) {
    private val tree = LongArray(2 * size)

    // Trafik qiymatini yangilash
    fun update(index: Int, value: Long) {
        var i = index + size
        tree[i] = value
        while (i > 1) {
            tree[i shr 1] = tree[i] + tree[i xor 1]
            i = i shr 1
        }
    }

    // [l, r) diapazondagi yig'indini olish
    fun query(l: Int, r: Int): Long {
        var res = 0L
        var left = l + size
        var right = r + size
        while (left < right) {
            if (left and 1 == 1) res += tree[left++]
            if (right and 1 == 1) res += tree[--right]
            left = left shr 1
            right = right shr 1
        }
        return res
    }
}
```
**Tushuntirish:** Segment Tree tanlandi, chunki u nuqtali yangilash va diapazonli so'rovlar uchun eng samarali statik tuzilmadir.

### Topshiriq #1072: Foydalanuvchi so'rovlarini tezkor qidirish (Trie)
**Tavsif:** Milliy qidiruv tizimida prefiks asosida so'zlarni avtomatik to'ldirish.
**Talablar:** Xotirani tejash, O(L) qidiruv vaqti (L - so'z uzunligi).
**Yechim (Kotlin):**
```kotlin
class TrieNode {
    val children = mutableMapOf<Char, TrieNode>()
    var isEndOfWord = false
}

class AutoComplete {
    private val root = TrieNode()

    fun insert(word: String) {
        var current = root
        for (char in word) {
            current = current.children.getOrPut(char) { TrieNode() }
        }
        current.isEndOfWord = true
    }

    fun searchPrefix(prefix: String): Boolean {
        var current = root
        for (char in prefix) {
            current = current.children[char] ?: return false
        }
        return true
    }
}
```
**Tushuntirish:** Trie tuzilmasi prefiks qidiruvida hash-mapga qaraganda xotira va tezlik jihatidan optimaldir.

### Topshiriq #1073: Kümülatif statistikani hisoblash (Fenwick Tree)
**Tavsif:** Bank tranzaksiyalarini real vaqtda kuzatish va prefiks yig'indilarni hisoblash.
**Talablar:** Minimal xotira sarfi, O(log n) murakkablik.
**Yechim (Kotlin):**
```kotlin
class FenwickTree(val size: Int) {
    private val tree = LongArray(size + 1)

    fun add(index: Int, delta: Long) {
        var i = index + 1
        while (i <= size) {
            tree[i] += delta
            i += i and -i
        }
    }

    fun query(index: Int): Long {
        var i = index + 1
        var sum = 0L
        while (i > 0) {
            sum += tree[i]
            i -= i and -i
        }
        return sum
    }
}
```
**Tushuntirish:** Fenwick Tree (Binary Indexed Tree) Segment Tree'ga qaraganda kamroq xotira talab qiladi va implementatsiyasi sodda.

### Topshiriq #1074: Tarmoq topologiyasini tahlil qilish (BFS)
**Tavsif:** Serverlar o'rtasidagi eng qisqa aloqa yo'lini topish.
**Talablar:** O(V + E) vaqt murakkabligi, xavfsiz graf traversali.
**Yechim (Kotlin):**
```kotlin
fun findShortestPath(graph: Map<Int, List<Int>>, start: Int, target: Int): Int {
    val queue = ArrayDeque<Pair<Int, Int>>()
    val visited = mutableSetOf<Int>()
    queue.add(start to 0)
    visited.add(start)

    while (queue.isNotEmpty()) {
        val (current, dist) = queue.removeFirst()
        if (current == target) return dist
        for (neighbor in graph[current] ?: emptyList()) {
            if (neighbor !in visited) {
                visited.add(neighbor)
                queue.add(neighbor to dist + 1)
            }
        }
    }
    return -1
}
```
**Tushuntirish:** BFS (Breadth-First Search) vaznsiz graflarda eng qisqa yo'lni topish uchun eng ishonchli algoritmdir.

### Topshiriq #1075: Kritik resurslarni aniqlash (Tarjan's Algorithm)
**Tavsif:** Tarmoqdagi "bottleneck" (tiqilinch) nuqtalarni aniqlash.
**Talablar:** O(V + E) vaqt murakkabligi, rekursiv xavfsizlik.
**Yechim (Kotlin):**
```kotlin
class BridgeFinder(val n: Int, val adj: Array<MutableList<Int>>) {
    private var timer = 0
    private val tin = IntArray(n) { -1 }
    private val low = IntArray(n) { -1 }

    fun findBridges(u: Int, p: Int = -1) {
        tin[u] = timer; low[u] = timer++
        for (v in adj[u]) {
            if (v == p) continue
            if (tin[v] != -1) low[u] = minOf(low[u], tin[v])
            else {
                findBridges(v, u)
                low[u] = minOf(low[u], low[v])
                if (low[v] > tin[u]) println("Ko'prik topildi: $u - $v")
            }
        }
    }
}
```
**Tushuntirish:** Tarjan algoritmi grafdagi kritik bog'lanishlarni bitta o'tishda aniqlash imkonini beradi.

### Topshiriq #1076: Katta ma'lumotlar oqimida medianani topish (Two Heaps)
**Tavsif:** Real vaqtda kelayotgan raqamli oqimning medianasini hisoblash.
**Talablar:** O(log n) kiritish, O(1) olish.
**Yechim (Kotlin):**
```kotlin
import java.util.PriorityQueue

class MedianFinder {
    private val small = PriorityQueue<Int>(compareByDescending { it })
    private val large = PriorityQueue<Int>()

    fun addNum(num: Int) {
        small.add(num)
        large.add(small.poll())
        if (small.size < large.size) small.add(large.poll())
    }

    fun findMedian(): Double = if (small.size > large.size) small.peek().toDouble() 
                               else (small.peek() + large.peek()) / 2.0
}
```
**Tushuntirish:** Ikkita PriorityQueue (Min-Heap va Max-Heap) yordamida medianani doimiy nazorat qilish mumkin.

### Topshiriq #1077: Vazifalarni rejalashtirish (Topological Sort)
**Tavsif:** Bir-biriga bog'liq bo'lgan mikroservislarni ishga tushirish tartibini aniqlash.
**Talablar:** Sikllarni aniqlash, O(V + E) murakkablik.
**Yechim (Kotlin):**
```kotlin
fun topologicalSort(n: Int, adj: Array<MutableList<Int>>): List<Int> {
    val inDegree = IntArray(n)
    adj.forEach { list -> list.forEach { inDegree[it]++ } }
    val queue = ArrayDeque<Int>().apply { addAll(inDegree.indices.filter { inDegree[it] == 0 }) }
    val result = mutableListOf<Int>()

    while (queue.isNotEmpty()) {
        val u = queue.removeFirst()
        result.add(u)
        for (v in adj[u]) {
            if (--inDegree[v] == 0) queue.add(v)
        }
    }
    return result
}
```
**Tushuntirish:** Kahn algoritmi (BFS asosida) siklsiz graflarda tartibni aniqlash uchun eng samarali yechimdir.

### Topshiriq #1078: Minimal xarajatli tarmoq (Kruskal's Algorithm)
**Tavsif:** Serverlarni minimal kabel sarfi bilan ulash.
**Talablar:** Disjoint Set Union (DSU) ishlatish, O(E log E).
**Yechim (Kotlin):**
```kotlin
class DSU(n: Int) {
    val parent = IntArray(n) { it }
    fun find(i: Int): Int = if (parent[i] == i) i else find(parent[i].also { parent[i] = find(parent[i]) })
    fun union(i: Int, j: Int) { val rootI = find(i); if (rootI != find(j)) parent[rootI] = find(j) }
}
```
**Tushuntirish:** DSU path compression bilan birgalikda Kruskal algoritmini juda tezkor qiladi.

### Topshiriq #1079: Katta matn ichida naqsh qidirish (KMP)
**Tavsif:** Log fayllar ichida zararli kod fragmentlarini qidirish.
**Talablar:** O(N + M) vaqt murakkabligi.
**Yechim (Kotlin):**
```kotlin
fun kmpSearch(text: String, pattern: String): List<Int> {
    val lps = IntArray(pattern.length)
    var len = 0
    for (i in 1 until pattern.length) {
        while (len > 0 && pattern[i] != pattern[len]) len = lps[len - 1]
        if (pattern[i] == pattern[len]) lps[i] = ++len
    }
    val matches = mutableListOf<Int>()
    var j = 0
    for (i in text.indices) {
        while (j > 0 && text[i] != pattern[j]) j = lps[j - 1]
        if (text[i] == pattern[j]) j++
        if (j == pattern.length) { matches.add(i - j + 1); j = lps[j - 1] }
    }
    return matches
}
```
**Tushuntirish:** Knuth-Morris-Pratt algoritmi qidiruv jarayonida ortiqcha orqaga qaytishlarni oldini oladi.

### Topshiriq #1080: Eng uzun umumiy prefiks (Trie/Array)
**Tavsif:** Foydalanuvchi nomlari ro'yxatidan umumiy prefiksni ajratib olish.
**Talablar:** O(S) vaqt murakkabligi (S - barcha belgilar yig'indisi).
**Yechim (Kotlin):**
```kotlin
fun longestCommonPrefix(strs: Array<String>): String {
    if (strs.isEmpty()) return ""
    var prefix = strs[0]
    for (i in 1 until strs.size) {
        while (strs[i].indexOf(prefix) != 0) {
            prefix = prefix.substring(0, prefix.length - 1)
            if (prefix.isEmpty()) return ""
        }
    }
    return prefix
}
```
**Tushuntirish:** Gorizontal skanerlash usuli eng kam xotira sarfi bilan umumiy prefiksni topishga imkon beradi.

---

### Topshiriq #1081: Tarmoq topologiyasida eng qisqa yo'lni aniqlash (Dijkstra + PriorityQueue)
**Tavsif:** Katta hajmdagi serverlar tarmog'ida ma'lumotlar paketini eng kam kechikish bilan uzatish.
**Talablar:** Vaqt murakkabligi O(E log V), xotira xavfsizligi uchun `Long` tipidagi masofalardan foydalanish.
**Yechim (Kotlin):**
```kotlin
import java.util.*

fun dijkstra(graph: Array<MutableList<Pair<Int, Int>>>, start: Int): LongArray {
    val dist = LongArray(graph.size) { Long.MAX_VALUE }
    dist[start] = 0
    val pq = PriorityQueue<Pair<Long, Int>>(compareBy { it.first })
    pq.add(0L to start)

    while (pq.isNotEmpty()) {
        val (d, u) = pq.poll()
        if (d > dist[u]) continue
        for ((v, weight) in graph[u]) {
            if (dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight
                pq.add(dist[v] to v)
            }
        }
    }
    return dist
}
```
**Tushuntirish:** `PriorityQueue` yordamida eng qisqa masofani tanlash algoritmi tarmoq kechikishlarini minimallashtirish uchun eng samarali yondashuvdir.

### Topshiriq #1082: Dinamik massivda oraliq yig'indisini hisoblash (Fenwick Tree)
**Tavsif:** Real vaqt rejimida moliyaviy tranzaksiyalar oqimida ma'lum vaqt oralig'idagi jami summani tezkor aniqlash.
**Talablar:** O(log N) vaqt murakkabligi, indeks xavfsizligi.
**Yechim (Kotlin):**
```kotlin
class FenwickTree(val size: Int) {
    private val tree = LongArray(size + 1)

    fun update(i: Int, delta: Long) {
        var idx = i + 1
        while (idx <= size) {
            tree[idx] += delta
            idx += idx and -idx
        }
    }

    fun query(i: Int): Long {
        var idx = i + 1
        var sum = 0L
        while (idx > 0) {
            sum += tree[idx]
            idx -= idx and -idx
        }
        return sum
    }
}
```
**Tushuntirish:** Fenwick Tree (Binary Indexed Tree) massivni yangilash va yig'indini olishda Segment Tree'ga qaraganda kamroq xotira sarflaydi.

### Topshiriq #1083: Katta hajmdagi matnlar ichidan prefiks qidirish (Trie)
**Tavsif:** Foydalanuvchi so'rovlarini avtomatik to'ldirish (Autocomplete) tizimi uchun lug'at bazasi.
**Talablar:** O(L) qidiruv tezligi (L - so'z uzunligi), xotirani tejash uchun `Map` dan foydalanish.
**Yechim (Kotlin):**
```kotlin
class TrieNode {
    val children = mutableMapOf<Char, TrieNode>()
    var isEndOfWord = false
}

class Trie {
    private val root = TrieNode()

    fun insert(word: String) {
        var current = root
        for (char in word) {
            current = current.children.getOrPut(char) { TrieNode() }
        }
        current.isEndOfWord = true
    }

    fun search(prefix: String): Boolean {
        var current = root
        for (char in prefix) {
            current = current.children[char] ?: return false
        }
        return true
    }
}
```
**Tushuntirish:** Trie tuzilmasi prefikslarni saqlashda takrorlanuvchi qismlarni birlashtirib, qidiruvni chiziqli vaqtda amalga oshiradi.

### Topshiriq #1084: Oraliqdagi eng katta qiymatni topish (Segment Tree)
**Tavsif:** Sensor ma'lumotlari oqimida ma'lum vaqt oralig'idagi maksimal qiymatni (masalan, harorat pikini) aniqlash.
**Talablar:** O(log N) yangilash va so'rov, rekursiv bo'lmagan implementatsiya imkoniyati.
**Yechim (Kotlin):**
```kotlin
class SegmentTree(val n: Int, val data: IntArray) {
    private val tree = IntArray(2 * n)

    init {
        for (i in 0 until n) tree[n + i] = data[i]
        for (i in n - 1 downTo 1) tree[i] = maxOf(tree[2 * i], tree[2 * i + 1])
    }

    fun query(l: Int, r: Int): Int {
        var res = Int.MIN_VALUE
        var left = l + n
        var right = r + n
        while (left < right) {
            if (left % 2 == 1) res = maxOf(res, tree[left++])
            if (right % 2 == 1) res = maxOf(res, tree[--right])
            left /= 2; right /= 2
        }
        return res
    }
}
```
**Tushuntirish:** Iterativ Segment Tree xotira va tezlik jihatidan rekursiv yondashuvdan ustunroqdir.

### Topshiriq #1085: Grafda bog'langan komponentlarni aniqlash (Disjoint Set Union)
**Tavsif:** Ijtimoiy tarmoqlarda do'stlar guruhini (klasterlarni) aniqlash.
**Talablar:** Path compression va union by rank texnikalari, deyarli doimiy vaqt murakkabligi.
**Yechim (Kotlin):**
```kotlin
class DSU(n: Int) {
    private val parent = IntArray(n) { it }
    
    fun find(i: Int): Int {
        if (parent[i] == i) return i
        parent[i] = find(parent[i]) // Path compression
        return parent[i]
    }

    fun union(i: Int, j: Int) {
        val rootI = find(i)
        val rootJ = find(j)
        if (rootI != rootJ) parent[rootI] = rootJ
    }
}
```
**Tushuntirish:** DSU algoritmi katta tarmoqlarda obyektlar o'rtasidagi aloqadorlikni tekshirish uchun eng tezkor vositadir.

### Topshiriq #1086: Grafda sikllarni aniqlash (Kahn algoritmi)
**Tavsif:** Ish jarayonlarini (workflow) rejalashtirishda bog'liqliklar orasida sikl mavjudligini tekshirish.
**Talablar:** Topologik tartiblash, O(V + E) murakkablik.
**Yechim (Kotlin):**
```kotlin
fun hasCycle(n: Int, adj: Array<MutableList<Int>>): Boolean {
    val inDegree = IntArray(n)
    for (u in 0 until n) for (v in adj[u]) inDegree[v]++
    val queue: Queue<Int> = LinkedList()
    for (i in 0 until n) if (inDegree[i] == 0) queue.add(i)
    
    var count = 0
    while (queue.isNotEmpty()) {
        val u = queue.poll()
        count++
        for (v in adj[u]) if (--inDegree[v] == 0) queue.add(v)
    }
    return count != n
}
```
**Tushuntirish:** Kahn algoritmi nafaqat topologik tartiblashni, balki grafdagi ziddiyatli bog'liqliklarni (sikllarni) aniqlash uchun ham xizmat qiladi.

### Topshiriq #1087: Ikki tomonlama grafda maksimal oqim (Edmonds-Karp)
**Tavsif:** Logistika tizimida omborlardan do'konlarga yuk tashish imkoniyatini optimallashtirish.
**Talablar:** BFS asosidagi oqimni oshirish, xavfsiz oqim chegaralari.
**Yechim (Kotlin):**
```kotlin
fun bfs(capacity: Array<IntArray>, source: Int, sink: Int, parent: IntArray): Int {
    parent.fill(-1)
    parent[source] = source
    val queue: Queue<Pair<Int, Int>> = LinkedList()
    queue.add(source to Int.MAX_VALUE)
    
    while (queue.isNotEmpty()) {
        val (u, flow) = queue.poll()
        for (v in capacity.indices) {
            if (parent[v] == -1 && capacity[u][v] > 0) {
                parent[v] = u
                val newFlow = minOf(flow, capacity[u][v])
                if (v == sink) return newFlow
                queue.add(v to newFlow)
            }
        }
    }
    return 0
}
```
**Tushuntirish:** Edmonds-Karp algoritmi Ford-Fulkersonning barqaror versiyasi bo'lib, BFS yordamida eng qisqa yo'llarni tanlaydi.

### Topshiriq #1088: Trie yordamida so'zlar chastotasini hisoblash
**Tavsif:** Katta matnlar bazasida so'zlarning uchrash sonini tezkor aniqlash.
**Talablar:** O(N) vaqt, har bir tugunda `count` o'zgaruvchisi.
**Yechim (Kotlin):**
```kotlin
class FrequencyTrie {
    class Node {
        val children = mutableMapOf<Char, Node>()
        var count = 0
    }
    val root = Node()
    
    fun insert(word: String) {
        var curr = root
        for (char in word) curr = curr.children.getOrPut(char) { Node() }
        curr.count++
    }
}
```
**Tushuntirish:** Trie tugunlariga `count` qo'shish orqali qidiruv va statistikani bir vaqtning o'zida amalga oshirish mumkin.

### Topshiriq #1089: Segment Tree yordamida Lazy Propagation
**Tavsif:** Katta massivda oraliq bo'yicha qiymatlarni yangilash (Range Update).
**Talablar:** O(log N) yangilash, "Lazy" (kechiktirilgan) yangilash texnikasi.
**Yechim (Kotlin):**
```kotlin
class LazySegmentTree(val n: Int) {
    private val tree = LongArray(4 * n)
    private val lazy = LongArray(4 * n)

    fun update(node: Int, start: Int, end: Int, l: Int, r: Int, diff: Long) {
        if (lazy[node] != 0L) {
            tree[node] += (end - start + 1) * lazy[node]
            if (start != end) {
                lazy[2 * node] += lazy[node]
                lazy[2 * node + 1] += lazy[node]
            }
            lazy[node] = 0
        }
        // ... (Update logikasi davom etadi)
    }
}
```
**Tushuntirish:** Lazy propagation butun oraliqni bir vaqtda yangilash uchun zarur bo'lgan samarali texnikadir.

### Topshiriq #1090: Grafda eng yaqin umumiy ota (LCA - Lowest Common Ancestor)
**Tavsif:** Ierarxik tuzilmalarda (masalan, fayl tizimi yoki tashkiliy tuzilma) ikki tugun o'rtasidagi eng yaqin umumiy ota-tugunni topish.
**Talablar:** Binary Lifting texnikasi, O(log N) so'rov tezligi.
**Yechim (Kotlin):**
```kotlin
class LCA(val n: Int, val adj: Array<MutableList<Int>>) {
    private val LOG = 20
    private val up = Array(n) { IntArray(LOG) }
    private val depth = IntArray(n)

    fun dfs(u: Int, p: Int, d: Int) {
        depth[u] = d
        up[u][0] = p
        for (i in 1 until LOG) up[u][i] = up[up[u][i - 1]][i - 1]
        for (v in adj[u]) if (v != p) dfs(v, u, d + 1)
    }
    // LCA so'rovi uchun binary lifting logikasi...
}
```
**Tushuntirish:** Binary lifting yordamida LCA topish katta daraxt tuzilmalarida eng tezkor usul hisoblanadi.

---

### Topshiriq #1091: Tarmoq topologiyasida eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Katta hajmdagi serverlararo aloqa tarmog'ida ma'lumot uzatish kechikishini minimallashtirish.
**Talablar:** O(E log V) murakkablik, xotira xavfsizligi uchun `PriorityQueue` dan foydalanish.
**Yechim (Kotlin):**
```kotlin
import java.util.*

fun dijkstra(graph: Map<Int, List<Pair<Int, Int>>>, start: Int): IntArray {
    val distances = IntArray(graph.size) { Int.MAX_VALUE }
    distances[start] = 0
    val pq = PriorityQueue<Pair<Int, Int>>(compareBy { it.second })
    pq.add(start to 0)

    while (pq.isNotEmpty()) {
        val (u, dist) = pq.poll()
        if (dist > distances[u]) continue
        graph[u]?.forEach { (v, weight) ->
            if (distances[u] + weight < distances[v]) {
                distances[v] = distances[u] + weight
                pq.add(v to distances[v])
            }
        }
    }
    return distances
}
```
**Tushuntirish:** Dijkstra algoritmi tarmoq kechikishlarini hisoblashda eng samarali yondashuvdir. `PriorityQueue` yordamida eng kichik masofali tugunni tanlash vaqtni tejaydi.

### Topshiriq #1092: Segment Tree yordamida diapazon yig'indisini hisoblash
**Tavsif:** Real vaqt rejimida moliya tizimlarida tranzaksiyalar yig'indisini tezkor yangilash va so'rash.
**Talablar:** Yangilash va so'rov uchun O(log N) murakkablik.
**Yechim (Kotlin):**
```kotlin
class SegmentTree(val size: Int) {
    private val tree = LongArray(2 * size)

    fun update(i: Int, value: Long) {
        var idx = i + size
        tree[idx] = value
        while (idx > 1) {
            tree[idx shr 1] = tree[idx] + tree[idx xor 1]
            idx = idx shr 1
        }
    }

    fun query(l: Int, r: Int): Long {
        var res = 0L
        var left = l + size; var right = r + size
        while (left < right) {
            if (left and 1 == 1) res += tree[left++]
            if (right and 1 == 1) res += tree[--right]
            left = left shr 1; right = right shr 1
        }
        return res
    }
}
```
**Tushuntirish:** Segment Tree massivdagi o'zgarishlarni tezkor qayta ishlash uchun optimaldir. Bitwise operatsiyalar (`shr`, `xor`) ishlash tezligini oshiradi.

### Topshiriq #1093: Fenwick Tree (Binary Indexed Tree) bilan chastota tahlili
**Tavsif:** Katta log fayllarida hodisalar chastotasini hisoblash.
**Talablar:** Xotira samaradorligi va O(log N) tezlik.
**Yechim (Kotlin):**
```kotlin
class FenwickTree(val size: Int) {
    private val tree = LongArray(size + 1)

    fun add(i: Int, delta: Long) {
        var idx = i + 1
        while (idx <= size) {
            tree[idx] += delta
            idx += idx and -idx
        }
    }

    fun prefixSum(i: Int): Long {
        var idx = i + 1; var sum = 0L
        while (idx > 0) {
            sum += tree[idx]
            idx -= idx and -idx
        }
        return sum
    }
}
```
**Tushuntirish:** Fenwick Tree Segment Tree ga nisbatan kamroq xotira talab qiladi va implementatsiyasi sodda, bu esa yuqori yuklamali tizimlar uchun mos.

### Topshiriq #1094: Trie (Prefix Tree) yordamida avtomatik to'ldirish
**Tavsif:** Foydalanuvchi so'rovlarini tezkor qidirish va taklif qilish tizimi.
**Talablar:** Harflar bo'yicha qidiruvda O(L) murakkablik (L - so'z uzunligi).
**Yechim (Kotlin):**
```kotlin
class TrieNode {
    val children = mutableMapOf<Char, TrieNode>()
    var isEndOfWord = false
}

class Trie {
    val root = TrieNode()
    fun insert(word: String) {
        var curr = root
        for (ch in word) curr = curr.children.getOrPut(ch) { TrieNode() }
        curr.isEndOfWord = true
    }
}
```
**Tavsif:** Trie tuzilmasi lug'at qidiruvlarida va avtomatik to'ldirishda eng yuqori samaradorlikni ta'minlaydi.

### Topshiriq #1095: Graflarda sikllarni aniqlash (DFS)
**Tavsif:** Mikroxizmatlar bog'liqliklarida o'zaro bog'liqlik (deadlock) xavfini aniqlash.
**Talablar:** O(V + E) vaqt murakkabligi.
**Yechim (Kotlin):**
```kotlin
fun hasCycle(graph: Map<Int, List<Int>>, visited: MutableSet<Int>, recStack: MutableSet<Int>, node: Int): Boolean {
    visited.add(node); recStack.add(node)
    for (neighbor in graph[node] ?: emptyList()) {
        if (neighbor !in visited && hasCycle(graph, visited, recStack, neighbor)) return true
        else if (neighbor in recStack) return true
    }
    recStack.remove(node)
    return false
}
```
**Tushuntirish:** Rekursiv stek yordamida graflardagi sikllarni aniqlash tizim barqarorligi uchun muhimdir.

### Topshiriq #1096: Union-Find (Disjoint Set Union)
**Tavsif:** Tarmoq segmentlarini birlashtirish va ularning bog'liqligini tekshirish.
**Talablar:** Path compression va union by rank optimizatsiyasi.
**Yechim (Kotlin):**
```kotlin
class DSU(n: Int) {
    private val parent = IntArray(n) { it }
    fun find(i: Int): Int {
        if (parent[i] == i) return i
        parent[i] = find(parent[i]) // Path compression
        return parent[i]
    }
    fun union(i: Int, j: Int) {
        val rootI = find(i); val rootJ = find(j)
        if (rootI != rootJ) parent[rootI] = rootJ
    }
}
```
**Tushuntirish:** DSU dinamik guruhlash muammolarini deyarli doimiy vaqtda hal qiladi.

### Topshiriq #1097: Topologik tartiblash (Kahn algoritmi)
**Tavsif:** Loyiha vazifalari (task dependency) ketma-ketligini aniqlash.
**Talablar:** O(V + E) murakkablik.
**Yechim (Kotlin):**
```kotlin
fun topologicalSort(n: Int, adj: Map<Int, List<Int>>, inDegree: IntArray): List<Int> {
    val queue: Queue<Int> = LinkedList<Int>()
    for (i in 0 until n) if (inDegree[i] == 0) queue.add(i)
    val result = mutableListOf<Int>()
    while (queue.isNotEmpty()) {
        val u = queue.poll(); result.add(u)
        for (v in adj[u] ?: emptyList()) {
            if (--inDegree[v] == 0) queue.add(v)
        }
    }
    return result
}
```
**Tushuntirish:** Kahn algoritmi vazifalar orasidagi bog'liqlikni tartiblashda eng ishonchli usuldir.

### Topshiriq #1098: Eng yaqin umumiy ota (LCA)
**Tavsif:** Ierarxik ma'lumotlar bazasida (kategoriyalar daraxti) umumiy ota tugunni topish.
**Talablar:** Binary lifting yordamida O(log N) so'rov tezligi.
**Yechim (Kotlin):**
```kotlin
// Binary lifting uchun oldindan hisoblash (qisqartirilgan)
fun getLCA(u: Int, v: Int, depth: IntArray, up: Array<IntArray>): Int {
    var a = u; var b = v
    if (depth[a] < depth[b]) a = b.also { b = a }
    // ... (depth tenglashtirish va binary lifting logikasi)
    return a 
}
```
**Tushuntirish:** Binary lifting katta daraxtlarda LCA ni tezkor topish uchun sanoat standarti hisoblanadi.

### Topshiriq #1099: Tarjan algoritmi (SCC)
**Tavsif:** Kuchli bog'langan komponentlarni (Strongly Connected Components) aniqlash.
**Talablar:** Bir martalik DFS yurishi bilan O(V + E).
**Yechim (Kotlin):**
```kotlin
// Tarjan algoritmi yordamida SCC topish
fun tarjan(u: Int, disc: IntArray, low: IntArray, stack: Stack<Int>, onStack: BooleanArray) {
    disc[u] = timer; low[u] = timer; timer++
    stack.push(u); onStack[u] = true
    // ... (qo'shni tugunlar bo'ylab DFS va low-link yangilash)
}
```
**Tushuntirish:** Tarjan algoritmi murakkab graflarni qismlarga ajratishda eng samarali yondashuvdir.

### Topshiriq #1100: Kenglik bo'yicha qidiruv (BFS) - Eng qisqa yo'l
**Tavsif:** Unweighted (vaznsiz) graflarda eng qisqa yo'lni topish.
**Talablar:** O(V + E) murakkablik va xotira xavfsizligi.
**Yechim (Kotlin):**
```kotlin
fun bfs(graph: Map<Int, List<Int>>, start: Int, target: Int): Int {
    val queue: Queue<Pair<Int, Int>> = LinkedList()
    queue.add(start to 0)
    val visited = mutableSetOf(start)
    while (queue.isNotEmpty()) {
        val (curr, dist) = queue.poll()
        if (curr == target) return dist
        for (neighbor in graph[curr] ?: emptyList()) {
            if (neighbor !in visited) {
                visited.add(neighbor)
                queue.add(neighbor to dist + 1)
            }
        }
    }
    return -1
}
```
**Tushuntirish:** BFS vaznsiz graflarda eng qisqa yo'lni topish uchun eng optimal va xavfsiz algoritmdir.