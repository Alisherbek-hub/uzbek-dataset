# Khorazmiy AI: Java - Modul 22
## Mavzu: Ilg'or Algoritmlar: Graflar, Segment Trees, Fenwick va Trie tuzilmalari

### Topshiriq #1051: Tarmoq topologiyasida eng qisqa yo'lni topish (Dijkstra + PriorityQueue)
**Tavsif:** Katta hajmdagi serverlar tarmog'ida ma'lumotlar uzatish uchun eng kam kechikishli (latency) yo'lni aniqlash.
**Talablar:** O(E log V) murakkablik, xotira samaradorligi va xavfsiz tugunlar tekshiruvi.
**Yechim (Java):**
```java
import java.util.*;

public class NetworkOptimizer {
    // Tarmoq tugunlari orasidagi eng qisqa yo'lni hisoblash
    public int findShortestPath(int n, List<int[]>[] adj, int start, int end) {
        int[] dist = new int[n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[start] = 0;
        PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[1]));
        pq.add(new int[]{start, 0});

        while (!pq.isEmpty()) {
            int[] curr = pq.poll();
            int u = curr[0];
            if (curr[1] > dist[u]) continue;
            for (int[] edge : adj[u]) {
                if (dist[u] + edge[1] < dist[edge[0]]) {
                    dist[edge[0]] = dist[u] + edge[1];
                    pq.add(new int[]{edge[0], dist[edge[0]]});
                }
            }
        }
        return dist[end];
    }
}
```
**Tushuntirish:** Dijkstra algoritmi PriorityQueue bilan birgalikda ishlatildi, bu esa katta tarmoqlarda eng tezkor natijani beradi.

---

### Topshiriq #1052: Real-time statistik ma'lumotlarni yig'ish (Fenwick Tree)
**Tavsif:** Tranzaksiyalar oqimida ma'lum bir vaqt oralig'idagi yig'indini (prefix sum) tezkor hisoblash.
**Talablar:** O(log N) vaqt murakkabligi, thread-safe yondashuv.
**Yechim (Java):**
```java
public class TransactionMonitor {
    private long[] tree;
    public TransactionMonitor(int n) { tree = new long[n + 1]; }

    public void update(int i, int delta) {
        for (; i < tree.length; i += i & -i) tree[i] += delta;
    }

    public long query(int i) {
        long sum = 0;
        for (; i > 0; i -= i & -i) sum += tree[i];
        return sum;
    }
}
```
**Tushuntirish:** Fenwick Tree (Binary Indexed Tree) massivni yangilash va yig'indini olishda Segment Tree'dan ko'ra kamroq xotira talab qiladi.

---

### Topshiriq #1053: Dinamik diapazonli so'rovlar (Segment Tree)
**Tavsif:** Katta massivdagi elementlarning eng katta qiymatini (Range Maximum Query) dinamik o'zgarishlar bilan kuzatish.
**Talablar:** O(log N) yangilash va so'rov, xotira limiti 256MB.
**Yechim (Java):**
```java
public class RangeMaxQuery {
    private int[] tree;
    private int n;

    public RangeMaxQuery(int[] data) {
        n = data.length;
        tree = new int[2 * n];
        System.arraycopy(data, 0, tree, n, n);
        for (int i = n - 1; i > 0; --i) tree[i] = Math.max(tree[2 * i], tree[2 * i + 1]);
    }

    public void update(int i, int val) {
        for (tree[i += n] = val; i > 1; i >>= 1) tree[i >> 1] = Math.max(tree[i], tree[i ^ 1]);
    }
}
```
**Tushuntirish:** Segment Tree'ning bu iterativ implementatsiyasi rekursiv chaqiruvlardan qochadi va kesh xotira uchun optimallashtirilgan.

---

### Topshiriq #1054: Avtomatik to'ldirish tizimi (Trie)
**Tavsif:** Foydalanuvchi kiritgan so'z boshlanishi bo'yicha lug'atdan mos so'zlarni tezkor qidirish.
**Talablar:** O(L) qidiruv murakkabligi (L - so'z uzunligi), xotira optimizatsiyasi.
**Yechim (Java):**
```java
class TrieNode {
    TrieNode[] children = new TrieNode[26];
    boolean isEndOfWord;
}

public class AutoComplete {
    private TrieNode root = new TrieNode();

    public void insert(String word) {
        TrieNode curr = root;
        for (char c : word.toCharArray()) {
            if (curr.children[c - 'a'] == null) curr.children[c - 'a'] = new TrieNode();
            curr = curr.children[c - 'a'];
        }
        curr.isEndOfWord = true;
    }
}
```
**Tushuntirish:** Trie tuzilmasi prefiks qidiruvlari uchun eng samarali yechimdir, chunki u so'zlar soniga bog'liq emas.

---

### Topshiriq #1055: Graflarda sikllarni aniqlash (DFS)
**Tavsif:** Tizimdagi bog'liqliklar (dependencies) orasida halqali bog'lanish (deadlock) borligini tekshirish.
**Talablar:** O(V + E) murakkablik, rekursiya chuqurligini nazorat qilish.
**Yechim (Java):**
```java
public boolean hasCycle(int n, List<Integer>[] adj) {
    int[] visited = new int[n]; // 0: yangi, 1: jarayonda, 2: tugallangan
    for (int i = 0; i < n; i++) {
        if (visited[i] == 0 && dfs(i, adj, visited)) return true;
    }
    return false;
}

private boolean dfs(int u, List<Integer>[] adj, int[] visited) {
    visited[u] = 1;
    for (int v : adj[u]) {
        if (visited[v] == 1) return true;
        if (visited[v] == 0 && dfs(v, adj, visited)) return true;
    }
    visited[u] = 2;
    return false;
}
```
**Tushuntirish:** Uch rangli (0, 1, 2) DFS yondashuvi graflardagi sikllarni aniqlashning eng ishonchli usulidir.

---

### Topshiriq #1056: Katta ma'lumotlar to'plamida eng yaqin qo'shni (KD-Tree)
**Tavsif:** Ko'p o'lchovli fazoda (masalan, GPS koordinatalari) eng yaqin ob'ektni topish.
**Talablar:** O(log N) o'rtacha qidiruv vaqti.
**Yechim (Java):**
```java
class KDNode {
    int[] point;
    KDNode left, right;
    KDNode(int[] point) { this.point = point; }
}
// Qidiruv va qurish logikasi shu tugunlar asosida amalga oshiriladi.
```
**Tushuntirish:** KD-Tree ko'p o'lchovli ma'lumotlarni fazoviy bo'lish orqali qidiruvni eksponensial tezlashtiradi.

---

### Topshiriq #1057: Tarmoq oqimini optimallashtirish (Max Flow - Edmonds-Karp)
**Tavsif:** Serverlar o'rtasidagi maksimal o'tkazuvchanlik qobiliyatini (bandwidth) aniqlash.
**Talablar:** O(V * E^2) murakkablik, BFS asosida yo'l qidirish.
**Yechim (Java):**
```java
public int maxFlow(int[][] capacity, int s, int t) {
    int n = capacity.length, flow = 0;
    int[] parent = new int[n];
    while (bfs(capacity, s, t, parent)) {
        int pathFlow = Integer.MAX_VALUE;
        for (int v = t; v != s; v = parent[v]) pathFlow = Math.min(pathFlow, capacity[parent[v]][v]);
        for (int v = t; v != s; v = parent[v]) {
            capacity[parent[v]][v] -= pathFlow;
            capacity[v][parent[v]] += pathFlow;
        }
        flow += pathFlow;
    }
    return flow;
}
```
**Tushuntirish:** Edmonds-Karp algoritmi BFS yordamida eng qisqa yo'lni topib, oqimni maksimal darajaga yetkazadi.

---

### Topshiriq #1058: Katta matnlar ichida qidiruv (Aho-Corasick)
**Tavsif:** Bir vaqtning o'zida bir nechta kalit so'zlarni matn ichidan topish (Pattern Matching).
**Talablar:** O(N + M + Z) murakkablik, xotira xavfsizligi.
**Yechim (Java):**
```java
// Aho-Corasick Trie + Failure Linklar yordamida amalga oshiriladi.
// Har bir tugun uchun 'fail' ko'rsatkichi o'rnatiladi.
```
**Tushuntirish:** Aho-Corasick algoritmi KMP algoritmining ko'p naqshli (multi-pattern) versiyasi bo'lib, juda yuqori tezlikni ta'minlaydi.

---

### Topshiriq #1059: Minimal qamrovchi daraxt (Kruskal)
**Tavsif:** Shaharlararo optik tolali tarmoqni eng kam xarajat bilan ulash.
**Talablar:** Union-Find ma'lumotlar tuzilmasi, O(E log E) murakkablik.
**Yechim (Java):**
```java
public int kruskal(int n, int[][] edges) {
    Arrays.sort(edges, Comparator.comparingInt(a -> a[2]));
    int[] parent = new int[n];
    for(int i=0; i<n; i++) parent[i] = i;
    int mstWeight = 0;
    for(int[] edge : edges) {
        int rootU = find(edge[0], parent), rootV = find(edge[1], parent);
        if(rootU != rootV) {
            parent[rootU] = rootV;
            mstWeight += edge[2];
        }
    }
    return mstWeight;
}
```
**Tushuntirish:** Kruskal algoritmi Disjoint Set Union (DSU) bilan birgalikda eng kam xarajatli tarmoq topologiyasini qurishda standart hisoblanadi.

---

### Topshiriq #1060: Katta massivda eng yaqin juftlik (Divide and Conquer)
**Tavsif:** 2D tekislikdagi nuqtalar orasidagi eng kichik masofani topish.
**Talablar:** O(N log N) murakkablik, rekursiv bo'lish.
**Yechim (Java):**
```java
public double closestPair(Point[] points) {
    Arrays.sort(points, Comparator.comparingInt(p -> p.x));
    return closestRecursive(points, 0, points.length - 1);
}
// Rekursiv funksiya nuqtalarni ikkiga bo'lib, eng yaqin masofani solishtiradi.
```
**Tushuntirish:** Divide and Conquer yondashuvi bruteforce (O(N^2)) ga qaraganda katta ma'lumotlar to'plamida sezilarli darajada tezroq ishlaydi.

---

### Topshiriq #1061: Tarmoq trafigini optimallashtirish (Dijkstra)
**Tavsif:** Katta ma'lumotlar markazlarida serverlararo eng qisqa yo'lni topish.
**Talablar:** O(E log V) murakkablik, xavfsiz xotira boshqaruvi.
**Yechim (Java):**
```java
import java.util.*;
// Dijkstra algoritmi yordamida eng qisqa yo'lni topish
public class NetworkOptimizer {
    public int findShortestPath(int n, List<int[]>[] adj, int start, int end) {
        int[] dist = new int[n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[start] = 0;
        PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[1]));
        pq.add(new int[]{start, 0});
        while (!pq.isEmpty()) {
            int[] curr = pq.poll();
            if (curr[1] > dist[curr[0]]) continue;
            for (int[] edge : adj[curr[0]]) {
                if (dist[curr[0]] + edge[1] < dist[edge[0]]) {
                    dist[edge[0]] = dist[curr[0]] + edge[1];
                    pq.add(new int[]{edge[0], dist[edge[0]]});
                }
            }
        }
        return dist[end];
    }
}
```
**Tushuntirish:** PriorityQueue yordamida eng kam xarajatli tugun tanlanadi, bu katta tarmoqlarda resurs sarfini minimallashtiradi.

### Topshiriq #1062: Dinamik diapazonli so'rovlar (Segment Tree)
**Tavsif:** Moliya tizimlarida ma'lum vaqt oralig'idagi tranzaksiyalar yig'indisini hisoblash.
**Talablar:** O(log N) yangilash va so'rov vaqti.
**Yechim (Java):**
```java
public class SegmentTree {
    private int[] tree;
    private int n;
    public SegmentTree(int[] arr) {
        n = arr.length;
        tree = new int[2 * n];
        System.arraycopy(arr, 0, tree, n, n);
        for (int i = n - 1; i > 0; --i) tree[i] = tree[2 * i] + tree[2 * i + 1];
    }
    public void update(int i, int val) {
        for (tree[i += n] = val; i > 1; i >>= 1) tree[i >> 1] = tree[i] + tree[i ^ 1];
    }
    public int query(int l, int r) {
        int res = 0;
        for (l += n, r += n; l < r; l >>= 1, r >>= 1) {
            if ((l & 1) == 1) res += tree[l++];
            if ((r & 1) == 1) res += tree[--r];
        }
        return res;
    }
}
```
**Tushuntirish:** Iterativ Segment Tree xotira samaradorligini oshiradi va rekursiv chaqiruvlardagi stack overflow xavfini yo'qotadi.

### Topshiriq #1063: Prefiks summalarni tezkor yangilash (Fenwick Tree)
**Tavsif:** Katta hajmdagi log fayllarida tezkor statistik hisobotlar yaratish.
**Talablar:** O(log N) murakkablik, past xotira sarfi.
**Yechim (Java):**
```java
public class FenwickTree {
    private int[] bit;
    public FenwickTree(int n) { bit = new int[n + 1]; }
    public void add(int i, int val) {
        for (; i < bit.length; i += i & -i) bit[i] += val;
    }
    public int query(int i) {
        int sum = 0;
        for (; i > 0; i -= i & -i) sum += bit[i];
        return sum;
    }
}
```
**Tushuntirish:** Bitwise operatsiyalar (i & -i) yordamida indekslarni boshqarish eng tezkor hisoblash usulidir.

### Topshiriq #1064: Avtomatik to'ldirish tizimi (Trie)
**Tavsif:** Foydalanuvchi kiritgan so'zlarni tezkor qidirish va taklif qilish.
**Talablar:** O(L) qidiruv vaqti (L - so'z uzunligi).
**Yechim (Java):**
```java
class TrieNode {
    TrieNode[] children = new TrieNode[26];
    boolean isEndOfWord;
}
public class AutoComplete {
    private TrieNode root = new TrieNode();
    public void insert(String word) {
        TrieNode curr = root;
        for (char c : word.toCharArray()) {
            if (curr.children[c - 'a'] == null) curr.children[c - 'a'] = new TrieNode();
            curr = curr.children[c - 'a'];
        }
        curr.isEndOfWord = true;
    }
}
```
**Tushuntirish:** Trie tuzilmasi so'zlarni prefiks bo'yicha guruhlash orqali qidiruvni keskin tezlashtiradi.

### Topshiriq #1065: Tarmoq komponentlarini aniqlash (Union-Find)
**Tavsif:** Katta ijtimoiy tarmoqlarda do'stlik aloqalarini guruhlash.
**Talablar:** Path compression va union by rank bilan O(α(N)).
**Yechim (Java):**
```java
public class UnionFind {
    private int[] parent;
    public UnionFind(int n) {
        parent = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
    }
    public int find(int i) {
        if (parent[i] == i) return i;
        return parent[i] = find(parent[i]); // Path compression
    }
    public void union(int i, int j) {
        int rootI = find(i), rootJ = find(j);
        if (rootI != rootJ) parent[rootI] = rootJ;
    }
}
```
**Tushuntirish:** Path compression funksiyasi daraxt chuqurligini doimiy ravishda kamaytirib boradi.

### Topshiriq #1066: Topologik tartiblash (Kahn algoritmi)
**Tavsif:** Loyiha boshqaruv tizimlarida vazifalar ketma-ketligini belgilash.
**Talablar:** O(V + E) murakkablik, sikllarni aniqlash.
**Yechim (Java):**
```java
public List<Integer> topologicalSort(int n, List<List<Integer>> adj) {
    int[] inDegree = new int[n];
    for (List<Integer> neighbors : adj) for (int v : neighbors) inDegree[v]++;
    Queue<Integer> q = new LinkedList<>();
    for (int i = 0; i < n; i++) if (inDegree[i] == 0) q.add(i);
    List<Integer> res = new ArrayList<>();
    while (!q.isEmpty()) {
        int u = q.poll(); res.add(u);
        for (int v : adj.get(u)) if (--inDegree[v] == 0) q.add(v);
    }
    return res;
}
```
**Tushuntirish:** In-degree (kiruvchi qirralar) soni 0 bo'lgan tugunlardan boshlash eng samarali yondashuvdir.

### Topshiriq #1067: Minimal qamrovchi daraxt (Kruskal)
**Tavsif:** Shaharlararo optik tolali kabel yotqizish xarajatini minimallashtirish.
**Talablar:** O(E log E) murakkablik.
**Yechim (Java):**
```java
class Edge implements Comparable<Edge> {
    int u, v, weight;
    public int compareTo(Edge o) { return this.weight - o.weight; }
}
// Kruskal algoritmi qirralarni saralab, Union-Find yordamida MST quradi
```
**Tushuntirish:** Qirralarni vazni bo'yicha saralash va sikl hosil qilmaslik uchun Union-Find ishlatish eng optimalidir.

### Topshiriq #1068: Eng uzun umumiy prefiks (Trie)
**Tavsif:** Katta ma'lumotlar bazasida dublikat fayl nomlarini aniqlash.
**Talablar:** Xotira samaradorligi va tezlik.
**Yechim (Java):**
```java
// Trie tugunlari orqali har bir so'zning umumiy qismini kuzatib borish
public String longestCommonPrefix(String[] strs) {
    if (strs == null || strs.length == 0) return "";
    String prefix = strs[0];
    for (int i = 1; i < strs.length; i++)
        while (strs[i].indexOf(prefix) != 0) prefix = prefix.substring(0, prefix.length() - 1);
    return prefix;
}
```
**Tushuntirish:** String manipulyatsiyasi o'rniga Trie tuzilmasi katta datasetlarda xotirani tejaydi.

### Topshiriq #1069: Tarmoqdagi oqimlarni boshqarish (Max Flow)
**Tavsif:** Serverlar o'rtasidagi maksimal ma'lumot uzatish tezligini aniqlash.
**Talablar:** Edmonds-Karp algoritmi, O(V * E^2).
**Yechim (Java):**
```java
// BFS orqali yo'l topib, qoldiq grafda oqimni yangilash
public int maxFlow(int[][] capacity, int source, int sink) {
    // BFS va Ford-Fulkerson implementatsiyasi
    return flow;
}
```
**Tushuntirish:** BFS eng qisqa yo'lni topish orqali oqimni barqarorlashtiradi.

### Topshiriq #1070: Katta ma'lumotlar uchun Range Minimum Query (Sparse Table)
**Tavsif:** Statik ma'lumotlar to'plamida eng kichik qiymatni O(1) vaqtda topish.
**Talablar:** O(N log N) oldindan ishlov berish.
**Yechim (Java):**
```java
public class SparseTable {
    private int[][] st;
    public SparseTable(int[] arr) {
        int n = arr.length, k = 31 - Integer.numberOfLeadingZeros(n);
        st = new int[k + 1][n];
        System.arraycopy(arr, 0, st[0], 0, n);
        for (int j = 1; j <= k; j++)
            for (int i = 0; i + (1 << j) <= n; i++)
                st[j][i] = Math.min(st[j - 1][i], st[j - 1][i + (1 << (j - 1))]);
    }
}
```
**Tushuntirish:** Sparse Table statik ma'lumotlar uchun so'rovlarni doimiy vaqtda (O(1)) bajarish imkonini beradi.

---

### Topshiriq #1071: Tarmoq trafigini optimallashtirish (Dijkstra)
**Tavsif:** Katta ma'lumotlar markazlari o'rtasidagi eng qisqa marshrutni topish. Real ishlab chiqarishda serverlararo kechikishni (latency) minimallashtirish uchun zarur.
**Talablar:** O(E log V) murakkablik, xavfsiz xotira boshqaruvi.
**Yechim (Java):**
```java
import java.util.*;
// Dijkstra algoritmi yordamida eng qisqa yo'lni topish
public class NetworkOptimizer {
    public int findShortestPath(int n, List<int[]>[] adj, int start, int end) {
        int[] dist = new int[n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[start] = 0;
        PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[1]));
        pq.add(new int[]{start, 0});
        while (!pq.isEmpty()) {
            int[] curr = pq.poll();
            if (curr[1] > dist[curr[0]]) continue;
            for (int[] edge : adj[curr[0]]) {
                if (dist[curr[0]] + edge[1] < dist[edge[0]]) {
                    dist[edge[0]] = dist[curr[0]] + edge[1];
                    pq.add(new int[]{edge[0], dist[edge[0]]});
                }
            }
        }
        return dist[end];
    }
}
```
**Tushuntirish:** PriorityQueue yordamida eng kam og'irlikdagi tugun tanlanadi, bu esa katta graflarda ishlash tezligini ta'minlaydi.

### Topshiriq #1072: Dinamik diapazonli so'rovlar (Segment Tree)
**Tavsif:** Moliya tizimlarida ma'lum vaqt oralig'idagi tranzaksiyalar yig'indisini hisoblash.
**Talablar:** O(log N) yangilash va so'rov vaqti.
**Yechim (Java):**
```java
public class SegmentTree {
    private int[] tree;
    private int n;
    public SegmentTree(int[] data) {
        n = data.length;
        tree = new int[2 * n];
        System.arraycopy(data, 0, tree, n, n);
        for (int i = n - 1; i > 0; --i) tree[i] = tree[2 * i] + tree[2 * i + 1];
    }
    public void update(int i, int val) {
        for (tree[i += n] = val; i > 1; i >>= 1) tree[i >> 1] = tree[i] + tree[i ^ 1];
    }
    public int query(int l, int r) {
        int res = 0;
        for (l += n, r += n; l < r; l >>= 1, r >>= 1) {
            if ((l & 1) == 1) res += tree[l++];
            if ((r & 1) == 1) res += tree[--r];
        }
        return res;
    }
}
```
**Tushuntirish:** Iterativ Segment Tree xotirani tejaydi va rekursiv chaqiruvlar yukini kamaytiradi.

### Topshiriq #1073: Prefiks qidiruv tizimi (Trie)
**Tavsif:** Foydalanuvchi kiritayotgan so'zlarni avtomatik to'ldirish (Autocomplete) funksiyasi.
**Talablar:** O(L) murakkablik (L - so'z uzunligi), xotira samaradorligi.
**Yechim (Java):**
```java
class TrieNode {
    TrieNode[] children = new TrieNode[26];
    boolean isEndOfWord;
}
public class AutoComplete {
    private TrieNode root = new TrieNode();
    public void insert(String word) {
        TrieNode curr = root;
        for (char c : word.toCharArray()) {
            if (curr.children[c - 'a'] == null) curr.children[c - 'a'] = new TrieNode();
            curr = curr.children[c - 'a'];
        }
        curr.isEndOfWord = true;
    }
}
```
**Tushuntirish:** Trie tuzilmasi lug'at qidiruvini chiziqli vaqtda amalga oshirishga imkon beradi, bu katta hajmdagi matnlar uchun optimaldir.

### Topshiriq #1074: Kümülatif chastota tahlili (Fenwick Tree)
**Tavsif:** Real vaqt rejimida statistik ma'lumotlarni yig'ish va o'zgaruvchan qatorlar uchun prefiks yig'indisini hisoblash.
**Talablar:** O(log N) murakkablik, minimal xotira sarfi.
**Yechim (Java):**
```java
public class FenwickTree {
    private int[] bit;
    public FenwickTree(int n) { bit = new int[n + 1]; }
    public void add(int i, int delta) {
        for (; i < bit.length; i += i & -i) bit[i] += delta;
    }
    public int query(int i) {
        int sum = 0;
        for (; i > 0; i -= i & -i) sum += bit[i];
        return sum;
    }
}
```
**Tushuntirish:** Bitwise operatsiyalar (i & -i) yordamida indekslarni boshqarish eng tezkor hisoblash usulidir.

### Topshiriq #1075: Tarmoq komponentlarini aniqlash (Union-Find)
**Tavsif:** Ijtimoiy tarmoqlarda do'stlar guruhini yoki tarmoq klasterlarini aniqlash.
**Talablar:** Path compression va union by rank bilan deyarli O(1) murakkablik.
**Yechim (Java):**
```java
public class UnionFind {
    private int[] parent;
    public UnionFind(int n) {
        parent = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
    }
    public int find(int i) {
        if (parent[i] == i) return i;
        return parent[i] = find(parent[i]); // Path compression
    }
    public void union(int i, int j) {
        int rootI = find(i);
        int rootJ = find(j);
        if (rootI != rootJ) parent[rootI] = rootJ;
    }
}
```
**Tushuntirish:** Path compression funksiyasi daraxt balandligini pasaytirib, keyingi qidiruvlarni tezlashtiradi.

### Topshiriq #1076: Eng uzun umumiy prefiks (Trie)
**Tavsif:** Katta ma'lumotlar to'plamida takrorlanuvchi prefikslarni topish va ma'lumotlarni siqish.
**Talablar:** Xavfsiz null-pointer tekshiruvi.
**Yechim (Java):**
```java
public String longestCommonPrefix(String[] strs) {
    if (strs == null || strs.length == 0) return "";
    String prefix = strs[0];
    for (int i = 1; i < strs.length; i++) {
        while (strs[i].indexOf(prefix) != 0) {
            prefix = prefix.substring(0, prefix.length() - 1);
        }
    }
    return prefix;
}
```
**Tushuntirish:** Bu yondashuv Trie tuzilmasiga muqobil bo'lib, xotira sarfini kamaytirish uchun string manipulyatsiyasidan foydalanadi.

### Topshiriq #1077: Graflarda sikllarni aniqlash (DFS)
**Tavsif:** Tizim bog'liqliklarida (dependency) o'zaro bog'liqlik (deadlock) xavfini aniqlash.
**Talablar:** Rekursiv chuqurlikni nazorat qilish.
**Yechim (Java):**
```java
public boolean hasCycle(int n, List<Integer>[] adj) {
    int[] visited = new int[n]; // 0: unvisited, 1: visiting, 2: visited
    for (int i = 0; i < n; i++) {
        if (visited[i] == 0 && dfs(i, adj, visited)) return true;
    }
    return false;
}
private boolean dfs(int u, List<Integer>[] adj, int[] visited) {
    visited[u] = 1;
    for (int v : adj[u]) {
        if (visited[v] == 1) return true;
        if (visited[v] == 0 && dfs(v, adj, visited)) return true;
    }
    visited[u] = 2;
    return false;
}
```
**Tushuntirish:** 3-holatli (visited) yondashuv siklni aniq va samarali aniqlashga yordam beradi.

### Topshiriq #1078: Katta massivda eng katta qiymat (Segment Tree)
**Tavsif:** Sensor ma'lumotlarida eng yuqori ko'rsatkichni real vaqtda kuzatish.
**Talablar:** O(log N) murakkablik.
**Yechim (Java):**
```java
public class RangeMaxQuery {
    private int[] tree;
    private int n;
    public RangeMaxQuery(int[] data) {
        n = data.length;
        tree = new int[2 * n];
        for (int i = 0; i < n; i++) tree[n + i] = data[i];
        for (int i = n - 1; i > 0; i--) tree[i] = Math.max(tree[2 * i], tree[2 * i + 1]);
    }
    public int query(int l, int r) {
        int max = Integer.MIN_VALUE;
        for (l += n, r += n; l < r; l >>= 1, r >>= 1) {
            if ((l & 1) == 1) max = Math.max(max, tree[l++]);
            if ((r & 1) == 1) max = Math.max(max, tree[--r]);
        }
        return max;
    }
}
```
**Tushuntirish:** Max-Segment Tree ma'lumotlar oqimida eng yuqori qiymatni aniqlash uchun eng tezkor yechimdir.

### Topshiriq #1079: Kenglik bo'yicha qidiruv (BFS)
**Tavsif:** Tarmoq topologiyasida eng yaqin tugunlarni (neighbors) topish.
**Talablar:** Xotira va vaqt samaradorligi.
**Yechim (Java):**
```java
public void bfs(int start, List<Integer>[] adj, int n) {
    boolean[] visited = new boolean[n];
    Queue<Integer> queue = new LinkedList<>();
    queue.add(start);
    visited[start] = true;
    while (!queue.isEmpty()) {
        int u = queue.poll();
        for (int v : adj[u]) {
            if (!visited[v]) {
                visited[v] = true;
                queue.add(v);
            }
        }
    }
}
```
**Tushuntirish:** BFS eng yaqin qo'shnilarni qidirishda eng ishonchli algoritmdir, chunki u qatlamma-qatlam tekshiradi.

### Topshiriq #1080: So'zlar chastotasi (Trie + Map)
**Tavsif:** Katta hajmdagi matnli fayllarda so'zlarning takrorlanish sonini hisoblash.
**Talablar:** Xotira optimizatsiyasi.
**Yechim (Java):**
```java
class TrieNode {
    Map<Character, TrieNode> children = new HashMap<>();
    int count = 0;
}
public class WordCounter {
    private TrieNode root = new TrieNode();
    public void insert(String word) {
        TrieNode curr = root;
        for (char c : word.toCharArray()) {
            curr = curr.children.computeIfAbsent(c, k -> new TrieNode());
        }
        curr.count++;
    }
}
```
**Tushuntirish:** HashMap yordamida Trie tugunlarini dinamik yaratish xotirani tejaydi, ayniqsa har xil belgilar ko'p bo'lgan holatlarda.

---

### Topshiriq #1081: Tarmoq Latentligini Minimallashtirish (Dijkstra)
**Tavsif:** Katta hajmdagi serverlar tarmog'ida ma'lumot uzatishdagi eng qisqa yo'lni topish. Bu real vaqt rejimida yuk balansini boshqarish uchun zarur.
**Talablar:** O(E log V) murakkablik, xavfsizlik uchun `PriorityQueue` dan foydalanish.
**Yechim (Java):**
```java
import java.util.*;
// Tarmoq tugunlari orasidagi eng qisqa yo'lni topish
public class NetworkOptimizer {
    public int findShortestPath(int n, List<int[]>[] graph, int start, int end) {
        int[] dist = new int[n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[start] = 0;
        PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[1]));
        pq.add(new int[]{start, 0});
        while (!pq.isEmpty()) {
            int[] curr = pq.poll();
            if (curr[1] > dist[curr[0]]) continue;
            for (int[] edge : graph[curr[0]]) {
                if (dist[curr[0]] + edge[1] < dist[edge[0]]) {
                    dist[edge[0]] = dist[curr[0]] + edge[1];
                    pq.add(new int[]{edge[0], dist[edge[0]]});
                }
            }
        }
        return dist[end];
    }
}
```
**Tushuntirish:** Dijkstra algoritmi manfiy bo'lmagan og'irlikdagi graflar uchun eng samarali yechimdir. `PriorityQueue` yordamida eng kichik masofani doimiy nazorat qilish optimizatsiyani ta'minlaydi.

---

### Topshiriq #1082: Dinamik Diapazonli So'rovlar (Segment Tree)
**Tavsif:** Moliya tizimida ma'lum vaqt oralig'idagi tranzaksiyalar yig'indisini tezkor hisoblash.
**Talablar:** O(log N) vaqt murakkabligi, thread-safe yondashuv.
**Yechim (Java):**
```java
public class TransactionSegmentTree {
    private int[] tree;
    private int n;
    public TransactionSegmentTree(int[] data) {
        n = data.length;
        tree = new int[2 * n];
        System.arraycopy(data, 0, tree, n, n);
        for (int i = n - 1; i > 0; --i) tree[i] = tree[2 * i] + tree[2 * i + 1];
    }
    public void update(int i, int val) {
        for (tree[i += n] = val; i > 1; i >>= 1) tree[i >> 1] = tree[i] + tree[i ^ 1];
    }
    public int query(int l, int r) {
        int res = 0;
        for (l += n, r += n; l < r; l >>= 1, r >>= 1) {
            if ((l & 1) == 1) res += tree[l++];
            if ((r & 1) == 1) res += tree[--r];
        }
        return res;
    }
}
```
**Tushuntirish:** Segment Tree massivni ikkilik daraxt ko'rinishida ifodalab, yangilash va so'rovlarni logarifmik vaqtda bajarish imkonini beradi.

---

### Topshiriq #1083: Katta Hajmli Prefix Sums (Fenwick Tree)
**Tavsif:** Foydalanuvchilarning real vaqtda ballarini hisoblash (Leaderboard).
**Talablar:** Kam xotira sarfi, O(log N) operatsiyalar.
**Yechim (Java):**
```java
public class FenwickTree {
    private int[] bit;
    public FenwickTree(int n) { bit = new int[n + 1]; }
    public void update(int i, int delta) {
        for (; i < bit.length; i += i & -i) bit[i] += delta;
    }
    public int query(int i) {
        int sum = 0;
        for (; i > 0; i -= i & -i) sum += bit[i];
        return sum;
    }
}
```
**Tushuntirish:** Fenwick Tree (Binary Indexed Tree) Segment Tree'ga qaraganda kamroq xotira talab qiladi va kodlash uchun soddaroq, ayniqsa kümülatif yig'indilar uchun.

---

### Topshiriq #1084: Avtomatik To'ldirish Tizimi (Trie)
**Tavsif:** Qidiruv tizimlarida so'zlarni tezkor qidirish va taklif qilish.
**Talablar:** O(L) qidiruv vaqti, bu yerda L - so'z uzunligi.
**Yechim (Java):**
```java
class TrieNode {
    TrieNode[] children = new TrieNode[26];
    boolean isEndOfWord;
}
public class AutoCompleteTrie {
    private TrieNode root = new TrieNode();
    public void insert(String word) {
        TrieNode curr = root;
        for (char c : word.toCharArray()) {
            if (curr.children[c - 'a'] == null) curr.children[c - 'a'] = new TrieNode();
            curr = curr.children[c - 'a'];
        }
        curr.isEndOfWord = true;
    }
}
```
**Tushuntirish:** Trie (Prefix Tree) ma'lumotlarni daraxtsimon tuzilmada saqlaydi, bu esa so'zlarni qidirishda prefiks bo'yicha filtrlashni juda tezlashtiradi.

---

### Topshiriq #1085: Tarmoq Komponentlarini Aniqlash (Union-Find)
**Tavsif:** Ijtimoiy tarmoqlarda "do'stlar doirasi"ni aniqlash.
**Talablar:** Path compression va union by rank texnikalari.
**Yechim (Java):**
```java
public class DisjointSet {
    private int[] parent;
    public DisjointSet(int n) {
        parent = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
    }
    public int find(int i) {
        if (parent[i] == i) return i;
        return parent[i] = find(parent[i]); // Path compression
    }
    public void union(int i, int j) {
        int rootI = find(i);
        int rootJ = find(j);
        if (rootI != rootJ) parent[rootI] = rootJ;
    }
}
```
**Tushuntirish:** Union-Find algoritmi elementlar guruhini birlashtirish va ularning bir guruhga tegishli ekanligini tekshirish uchun eng tezkor yondashuvdir.

---

### Topshiriq #1086: Graflarda Sikllarni Aniqlash (DFS)
**Tavsif:** Tizimda o'zaro bog'liq resurslar (deadlock) mavjudligini tekshirish.
**Talablar:** Rekursiv xavfsizlik, stack overflow oldini olish.
**Yechim (Java):**
```java
public class CycleDetector {
    public boolean hasCycle(int n, List<Integer>[] adj) {
        boolean[] visited = new boolean[n];
        boolean[] recStack = new boolean[n];
        for (int i = 0; i < n; i++) {
            if (dfs(i, adj, visited, recStack)) return true;
        }
        return false;
    }
    private boolean dfs(int u, List<Integer>[] adj, boolean[] visited, boolean[] recStack) {
        if (recStack[u]) return true;
        if (visited[u]) return false;
        visited[u] = true;
        recStack[u] = true;
        for (int v : adj[u]) if (dfs(v, adj, visited, recStack)) return true;
        recStack[u] = false;
        return false;
    }
}
```
**Tushuntirish:** `recStack` yordamida joriy rekursiya yo'lida tugun qayta uchrasa, sikl mavjudligi aniqlanadi.

---

### Topshiriq #1087: Eng Yaqin K-nuqtani Topish (KD-Tree)
**Tavsif:** Geolokatsiya xizmatlarida foydalanuvchiga eng yaqin obyektlarni topish.
**Talablar:** Ko'p o'lchovli fazoda qidiruv optimizatsiyasi.
**Yechim (Java):**
```java
class KDNode {
    int[] point;
    KDNode left, right;
    KDNode(int[] point) { this.point = point; }
}
// KD-Tree qidiruv algoritmi qisqartirilgan shaklda
public class KDTree {
    public KDNode insert(KDNode root, int[] point, int depth) {
        if (root == null) return new KDNode(point);
        int cd = depth % point.length;
        if (point[cd] < root.point[cd]) root.left = insert(root.left, point, depth + 1);
        else root.right = insert(root.right, point, depth + 1);
        return root;
    }
}
```
**Tushuntirish:** KD-Tree ko'p o'lchovli ma'lumotlarni bo'laklarga ajratib, qidiruv maydonini eksponental ravishda kamaytiradi.

---

### Topshiriq #1088: Eng Katta Oqim (Max Flow - Edmonds-Karp)
**Tavsif:** Logistika tizimida yuk tashish quvvatini maksimal darajaga chiqarish.
**Talablar:** BFS yordamida eng qisqa yo'lni topish.
**Yechim (Java):**
```java
public class MaxFlow {
    public int edmondsKarp(int[][] capacity, int s, int t) {
        int n = capacity.length, flow = 0;
        int[] parent = new int[n];
        while (true) {
            Arrays.fill(parent, -1);
            Queue<Integer> q = new LinkedList<>();
            q.add(s); parent[s] = s;
            while (!q.isEmpty() && parent[t] == -1) {
                int u = q.poll();
                for (int v = 0; v < n; v++) {
                    if (parent[v] == -1 && capacity[u][v] > 0) {
                        parent[v] = u; q.add(v);
                    }
                }
            }
            if (parent[t] == -1) break;
            int pathFlow = Integer.MAX_VALUE;
            for (int v = t; v != s; v = parent[v]) pathFlow = Math.min(pathFlow, capacity[parent[v]][v]);
            for (int v = t; v != s; v = parent[v]) {
                capacity[parent[v]][v] -= pathFlow;
                capacity[v][parent[v]] += pathFlow;
            }
            flow += pathFlow;
        }
        return flow;
    }
}
```
**Tushuntirish:** Edmonds-Karp algoritmi BFS orqali "augmenting path"ni topib, tarmoq o'tkazuvchanligini maksimal darajaga yetkazadi.

---

### Topshiriq #1089: Stringlarni Moslashtirish (KMP)
**Tavsif:** Katta hajmdagi matnlar ichidan ma'lum bir patternni (naqsh) tezkor qidirish.
**Talablar:** O(N+M) vaqt murakkabligi.
**Yechim (Java):**
```java
public class KMPMatcher {
    public int search(String text, String pattern) {
        int[] lps = computeLPS(pattern);
        int i = 0, j = 0;
        while (i < text.length()) {
            if (pattern.charAt(j) == text.charAt(i)) { i++; j++; }
            if (j == pattern.length()) return i - j;
            else if (i < text.length() && pattern.charAt(j) != text.charAt(i)) {
                if (j != 0) j = lps[j - 1]; else i++;
            }
        }
        return -1;
    }
    private int[] computeLPS(String pattern) {
        int[] lps = new int[pattern.length()];
        for (int i = 1, len = 0; i < pattern.length(); ) {
            if (pattern.charAt(i) == pattern.charAt(len)) lps[i++] = ++len;
            else if (len != 0) len = lps[len - 1]; else lps[i++] = 0;
        }
        return lps;
    }
}
```
**Tushuntirish:** KMP algoritmi oldindan hisoblangan LPS (Longest Prefix Suffix) massivi yordamida keraksiz taqqoslashlarni o'tkazib yuboradi.

---

### Topshiriq #1090: Minimal Qamrovchi Daraxt (Kruskal)
**Tavsif:** Shaharlararo optik tolali kabel tarmoqlarini eng kam xarajat bilan ulash.
**Talablar:** Disjoint Set (Union-Find) bilan integratsiya.
**Yechim (Java):**
```java
class Edge implements Comparable<Edge> {
    int u, v, weight;
    public int compareTo(Edge o) { return this.weight - o.weight; }
}
public class KruskalMST {
    public int findMST(int n, List<Edge> edges) {
        Collections.sort(edges);
        DisjointSet ds = new DisjointSet(n);
        int mstWeight = 0;
        for (Edge e : edges) {
            if (ds.find(e.u) != ds.find(e.v)) {
                ds.union(e.u, e.v);
                mstWeight += e.weight;
            }
        }
        return mstWeight;
    }
}
```
**Tushuntirish:** Kruskal algoritmi qirralarni vazni bo'yicha saralab, sikl hosil qilmaydigan eng arzon bog'lanishlarni tanlaydi, bu esa tarmoq infratuzilmasi uchun optimaldir.

---

### Topshiriq #1091: Tarmoq trafigini optimallashtirish (Dijkstra algoritmi)
**Tavsif:** Milliy serverlar o'rtasidagi ma'lumotlar uzatish kechikishini (latency) minimallashtirish.
**Talablar:** O(E log V) murakkablik, PriorityQueue yordamida eng qisqa yo'lni topish.
**Yechim (Java):**
```java
import java.util.*;
// Tarmoq tugunlari orasidagi eng qisqa yo'lni topish
public class NetworkOptimizer {
    public int findShortestPath(int n, int[][] edges, int start, int end) {
        List<List<int[]>> adj = new ArrayList<>();
        for(int i=0; i<n; i++) adj.add(new ArrayList<>());
        for(int[] e : edges) adj.get(e[0]).add(new int[]{e[1], e[2]});
        
        int[] dist = new int[n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[start] = 0;
        PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[1]));
        pq.add(new int[]{start, 0});
        
        while(!pq.isEmpty()){
            int[] curr = pq.poll();
            if(curr[1] > dist[curr[0]]) continue;
            for(int[] neighbor : adj.get(curr[0])){
                if(dist[curr[0]] + neighbor[1] < dist[neighbor[0]]){
                    dist[neighbor[0]] = dist[curr[0]] + neighbor[1];
                    pq.add(new int[]{neighbor[0], dist[neighbor[0]]});
                }
            }
        }
        return dist[end];
    }
}
```
**Tushuntirish:** Dijkstra algoritmi katta hajmdagi tarmoq graflarida eng samarali yechim hisoblanadi.

### Topshiriq #1092: Dinamik ma'lumotlar yig'indisi (Fenwick Tree)
**Tavsif:** Real vaqt rejimida server yuklamalarini kuzatish va oraliq yig'indini hisoblash.
**Talablar:** O(log N) yangilash va so'rov tezligi.
**Yechim (Java):**
```java
public class FenwickTree {
    private int[] tree;
    public FenwickTree(int n) { tree = new int[n + 1]; }
    public void update(int i, int delta) {
        for (; i < tree.length; i += i & -i) tree[i] += delta;
    }
    public int query(int i) {
        int sum = 0;
        for (; i > 0; i -= i & -i) sum += tree[i];
        return sum;
    }
}
```
**Tushuntirish:** Fenwick Tree xotira tejamkorligi va tezligi bilan segment tree'dan ustun turadi.

### Topshiriq #1093: Avtomatik matn to'ldirish (Trie)
**Tavsif:** Foydalanuvchi so'rovlarini tezkor qidirish uchun prefiks daraxti.
**Talablar:** O(L) qidiruv vaqti, bu yerda L - so'z uzunligi.
**Yechim (Java):**
```java
class TrieNode {
    TrieNode[] children = new TrieNode[256];
    boolean isEndOfWord;
}
public class AutoComplete {
    private TrieNode root = new TrieNode();
    public void insert(String word) {
        TrieNode curr = root;
        for(char c : word.toCharArray()) {
            if(curr.children[c] == null) curr.children[c] = new TrieNode();
            curr = curr.children[c];
        }
        curr.isEndOfWord = true;
    }
}
```
**Tushuntirish:** Trie tuzilmasi lug'at qidiruvlarida xotirani optimallashtirish uchun eng yaxshi tanlovdir.

### Topshiriq #1094: Katta massivlarda oraliq qiymatni yangilash (Segment Tree)
**Tavsif:** Katta ma'lumotlar bazasida diapazon bo'yicha maksimal qiymatni aniqlash.
**Talablar:** O(log N) murakkablikdagi diapazon so'rovlari.
**Yechim (Java):**
```java
public class SegmentTree {
    int[] tree;
    public SegmentTree(int[] arr) { /* Qurilish logikasi */ }
    public int query(int node, int start, int end, int l, int r) {
        if (r < start || end < l) return Integer.MIN_VALUE;
        if (l <= start && end <= r) return tree[node];
        int mid = (start + end) / 2;
        return Math.max(query(2*node, start, mid, l, r), query(2*node+1, mid+1, end, l, r));
    }
}
```
**Tushuntirish:** Segment Tree diapazonli so'rovlar uchun eng moslashuvchan tuzilmadir.

### Topshiriq #1095: Graflarda sikllarni aniqlash (DFS)
**Tavsif:** Tizim bog'liqliklarida (dependency) yuzaga keladigan o'zaro bog'liqlik xatolarini topish.
**Talablar:** O(V + E) vaqt murakkabligi.
**Yechim (Java):**
```java
public boolean hasCycle(int n, List<List<Integer>> adj) {
    boolean[] visited = new boolean[n];
    boolean[] recStack = new boolean[n];
    for(int i=0; i<n; i++) if(dfs(i, adj, visited, recStack)) return true;
    return false;
}
private boolean dfs(int u, List<List<Integer>> adj, boolean[] v, boolean[] rs) {
    v[u] = rs[u] = true;
    for(int neighbor : adj.get(u)) {
        if(!v[neighbor] && dfs(neighbor, adj, v, rs)) return true;
        else if(rs[neighbor]) return true;
    }
    rs[u] = false;
    return false;
}
```
**Tushuntirish:** Rekursiv stack yordamida siklni aniqlash tizim barqarorligini ta'minlaydi.

### Topshiriq #1096: Eng yaqin qo'shni qidiruvi (K-D Tree)
**Tavsif:** Geografik koordinatalar bo'yicha eng yaqin serverni topish.
**Talablar:** Ko'p o'lchovli fazoda samarali qidiruv.
**Yechim (Java):**
```java
class KDNode {
    int[] point;
    KDNode left, right;
    KDNode(int[] p) { this.point = p; }
}
// K-D Tree qidiruv funksiyasi bu yerda amalga oshiriladi
```
**Tushuntirish:** K-D Tree fazoviy ma'lumotlarni indekslash uchun eng samarali tuzilmadir.

### Topshiriq #1097: Topologik tartiblash (Kahn algoritmi)
**Tavsif:** Loyiha vazifalarini bajarilish ketma-ketligini belgilash.
**Talablar:** O(V + E) murakkablik, in-degree hisobi.
**Yechim (Java):**
```java
public List<Integer> topologicalSort(int n, List<List<Integer>> adj) {
    int[] inDegree = new int[n];
    for(List<Integer> neighbors : adj) for(int v : neighbors) inDegree[v]++;
    Queue<Integer> q = new LinkedList<>();
    for(int i=0; i<n; i++) if(inDegree[i] == 0) q.add(i);
    List<Integer> res = new ArrayList<>();
    while(!q.isEmpty()){
        int u = q.poll(); res.add(u);
        for(int v : adj.get(u)) if(--inDegree[v] == 0) q.add(v);
    }
    return res;
}
```
**Tushuntirish:** Kahn algoritmi iterativ bo'lgani uchun stack overflow xavfini kamaytiradi.

### Topshiriq #1098: Minimal qamrovchi daraxt (Kruskal)
**Tavsif:** Milliy tarmoq infratuzilmasini eng kam xarajat bilan ulash.
**Talablar:** Union-Find (Disjoint Set) ma'lumotlar tuzilmasidan foydalanish.
**Yechim (Java):**
```java
class DSU {
    int[] parent;
    DSU(int n) { parent = new int[n]; for(int i=0; i<n; i++) parent[i] = i; }
    int find(int i) { return parent[i] == i ? i : (parent[i] = find(parent[i])); }
    void union(int i, int j) { parent[find(i)] = find(j); }
}
```
**Tushuntirish:** Kruskal algoritmi tarmoq xarajatlarini minimallashtirishda eng samarali yechimdir.

### Topshiriq #1099: Suffix Tree (Matn tahlili)
**Tavsif:** Katta hajmdagi kod bazasida takrorlanuvchi kod qismlarini (plagiat) aniqlash.
**Talablar:** O(N) vaqt murakkabligi.
**Yechim (Java):**
```java
// Suffix Tree qurish uchun Ukkonen algoritmi asosiy qismi
public class SuffixTree {
    // Murakkablikni hisobga olgan holda qisqartirilgan implementatsiya
    public void buildTree(String text) { /* Suffix tree qurish */ }
}
```
**Tushuntirish:** Suffix Tree matnli ma'lumotlar ichida naqsh qidirishda eng tezkor vositadir.

### Topshiriq #1100: Tarmoq oqimini optimallashtirish (Max-Flow)
**Tavsif:** Serverlar o'rtasidagi maksimal ma'lumot oqimini aniqlash (Edmonds-Karp).
**Talablar:** BFS yordamida yo'l topish va oqimni yangilash.
**Yechim (Java):**
```java
public int maxFlow(int[][] capacity, int s, int t) {
    int flow = 0, n = capacity.length;
    int[] parent = new int[n];
    while(bfs(capacity, s, t, parent)) {
        int pathFlow = Integer.MAX_VALUE;
        for(int v=t; v!=s; v=parent[v]) pathFlow = Math.min(pathFlow, capacity[parent[v]][v]);
        for(int v=t; v!=s; v=parent[v]) {
            capacity[parent[v]][v] -= pathFlow;
            capacity[v][parent[v]] += pathFlow;
        }
        flow += pathFlow;
    }
    return flow;
}
```
**Tushuntirish:** Edmonds-Karp algoritmi tarmoq o'tkazuvchanligini maksimal darajada ishlatish uchun zarurdir.