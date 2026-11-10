# Khorazmiy AI: C# - Modul 22
## Mavzu: Ilg'or Algoritmlar: Graflar, Segment Trees, Fenwick va Trie tuzilmalari

### Topshiriq #1051: Katta hajmdagi tarmoqlar uchun Dijkstra algoritmi
**Tavsif:** Milliy infratuzilma logistika tizimida eng qisqa yo'lni aniqlash.
**Talablar:** O(E log V) murakkablik, xotira xavfsizligi uchun PriorityQueue dan foydalanish.
**Yechim (C#):**
```csharp
using System;
using System.Collections.Generic;

public class GraphOptimizer {
    public static long GetShortestPath(List<(int to, int weight)>[] adj, int start, int end, int n) {
        long[] dist = new long[n];
        Array.Fill(dist, long.MaxValue);
        dist[start] = 0;
        var pq = new PriorityQueue<int, long>();
        pq.Enqueue(start, 0);

        while (pq.Count > 0) {
            pq.TryDequeue(out int u, out long d);
            if (d > dist[u]) continue;
            foreach (var edge in adj[u]) {
                if (dist[u] + edge.weight < dist[edge.to]) {
                    dist[edge.to] = dist[u] + edge.weight;
                    pq.Enqueue(edge.to, dist[edge.to]);
                }
            }
        }
        return dist[end];
    }
}
```
**Tushuntirish:** `PriorityQueue` yordamida eng qisqa masofani samarali qidirish ta'minlandi, bu katta graflarda ishlash uchun optimaldir.

### Topshiriq #1052: Segment Tree yordamida diapazon yig'indisi
**Tavsif:** Real vaqt rejimida moliyaviy tranzaksiyalar yig'indisini hisoblash.
**Talablar:** O(log N) yangilash va so'rov vaqti.
**Yechim (C#):**
```csharp
public class SegmentTree {
    private long[] tree;
    private int n;
    public SegmentTree(int[] data) {
        n = data.Length;
        tree = new long[2 * n];
        for (int i = 0; i < n; i++) tree[n + i] = data[i];
        for (int i = n - 1; i > 0; i--) tree[i] = tree[2 * i] + tree[2 * i + 1];
    }
    public void Update(int i, int val) {
        for (tree[i += n] = val; i > 1; i >>= 1) tree[i >> 1] = tree[i] + tree[i ^ 1];
    }
}
```
**Tushuntirish:** Iterativ Segment Tree xotirani tejaydi va rekursiv chaqiruvlarsiz tezroq ishlaydi.

### Topshiriq #1053: Fenwick Tree (Binary Indexed Tree)
**Tavsif:** Katta massivlarda prefiks yig'indilarni tezkor hisoblash.
**Talablar:** O(log N) murakkablik, minimal xotira sarfi.
**Yechim (C#):**
```csharp
public class FenwickTree {
    private int[] bit;
    public FenwickTree(int n) => bit = new int[n + 1];
    public void Add(int i, int val) {
        for (; i < bit.Length; i += i & -i) bit[i] += val;
    }
    public int Query(int i) {
        int sum = 0;
        for (; i > 0; i -= i & -i) sum += bit[i];
        return sum;
    }
}
```
**Tushuntirish:** BIT tuzilmasi Segment Tree'ga qaraganda kamroq xotira talab qiladi va implementatsiyasi sodda.

### Topshiriq #1054: Trie (Prefix Tree) yordamida qidiruv
**Tavsif:** Milliy lug'at tizimida so'zlarni avtomatik to'ldirish (autocomplete).
**Talablar:** O(L) qidiruv vaqti, bu yerda L - so'z uzunligi.
**Yechim (C#):**
```csharp
public class TrieNode {
    public Dictionary<char, TrieNode> Children = new();
    public bool IsEndOfWord;
}
public class Trie {
    private readonly TrieNode root = new();
    public void Insert(string word) {
        var curr = root;
        foreach (var c in word) {
            if (!curr.Children.ContainsKey(c)) curr.Children[c] = new TrieNode();
            curr = curr.Children[c];
        }
        curr.IsEndOfWord = true;
    }
}
```
**Tushuntirish:** Lug'at bazasini xotirada samarali saqlash va prefiks bo'yicha qidirish uchun eng yaxshi yechim.

### Topshiriq #1055: Grafda bog'langan komponentlarni topish (DFS)
**Tavsif:** Ijtimoiy tarmoq foydalanuvchilari guruhlarini aniqlash.
**Talablar:** O(V + E) vaqt murakkabligi.
**Yechim (C#):**
```csharp
public void FindComponents(List<int>[] adj, int n) {
    bool[] visited = new bool[n];
    for (int i = 0; i < n; i++) {
        if (!visited[i]) {
            DFS(i, adj, visited);
            // Yangi komponent topildi
        }
    }
}
private void DFS(int u, List<int>[] adj, bool[] visited) {
    visited[u] = true;
    foreach (var v in adj[u]) if (!visited[v]) DFS(v, adj, visited);
}
```
**Tushuntirish:** Rekursiv DFS yondashuvi grafdagi barcha bog'langan tugunlarni aniqlash uchun eng toza yechimdir.

### Topshiriq #1056: Lazy Propagation bilan Segment Tree
**Tavsif:** Diapazon bo'yicha qiymatlarni yangilash (Range Update).
**Talablar:** O(log N) murakkablik.
**Yechim (C#):**
```csharp
// Lazy propagation uchun qisman kod
private void UpdateRange(int node, int start, int end, int l, int r, int val) {
    if (lazy[node] != 0) {
        tree[node] += (end - start + 1) * lazy[node];
        if (start != end) { lazy[2 * node] += lazy[node]; lazy[2 * node + 1] += lazy[node]; }
        lazy[node] = 0;
    }
    // ... qolgan mantiq
}
```
**Tushuntirish:** Lazy propagation katta massivlarda diapazonli operatsiyalarni keskin tezlashtiradi.

### Topshiriq #1057: Topologik tartiblash (Kahn algoritmi)
**Tavsif:** Loyiha vazifalari ketma-ketligini (Dependency resolution) aniqlash.
**Talablar:** O(V + E) murakkablik, sikllarni aniqlash.
**Yechim (C#):**
```csharp
public List<int> TopologicalSort(int n, List<int>[] adj, int[] inDegree) {
    var queue = new Queue<int>();
    for (int i = 0; i < n; i++) if (inDegree[i] == 0) queue.Enqueue(i);
    var result = new List<int>();
    while (queue.Count > 0) {
        int u = queue.Dequeue();
        result.Add(u);
        foreach (var v in adj[u]) if (--inDegree[v] == 0) queue.Enqueue(v);
    }
    return result;
}
```
**Tushuntirish:** Kahn algoritmi sikllarni aniqlash va vazifalarni tartiblash uchun eng ishonchli usuldir.

### Topshiriq #1058: Trie yordamida XOR maksimal qiymatni topish
**Tavsif:** Kriptografik kalitlar to'plamida XOR operatsiyasi uchun eng katta qiymatni topish.
**Talablar:** O(N * 32) murakkablik.
**Yechim (C#):**
```csharp
// Trie tugunlarida bitlarni saqlash orqali XOR yechimi
public void Insert(int num) {
    var curr = root;
    for (int i = 31; i >= 0; i--) {
        int bit = (num >> i) & 1;
        if (curr.Children[bit] == null) curr.Children[bit] = new TrieNode();
        curr = curr.Children[bit];
    }
}
```
**Tushuntirish:** Bit darajasida Trie ishlatish murakkab qidiruv muammolarini chiziqli vaqtda hal qiladi.

### Topshiriq #1059: Kruskal algoritmi (MST)
**Tavsif:** Milliy elektr tarmoqlarini eng kam xarajat bilan ulash.
**Talablar:** Disjoint Set Union (DSU) dan foydalanish.
**Yechim (C#):**
```csharp
public class DSU {
    int[] parent;
    public DSU(int n) { parent = Enumerable.Range(0, n).ToArray(); }
    public int Find(int i) => parent[i] == i ? i : (parent[i] = Find(parent[i]));
    public bool Union(int i, int j) {
        int rootI = Find(i), rootJ = Find(j);
        if (rootI != rootJ) { parent[rootI] = rootJ; return true; }
        return false;
    }
}
```
**Tushuntirish:** DSU bilan Kruskal algoritmi minimal qamrovchi daraxtni (MST) qurish uchun eng samarali usuldir.

### Topshiriq #1060: Bellman-Ford algoritmi
**Tavsif:** Salbiy vaznli qirralar mavjud bo'lgan moliyaviy tarmoqlarda eng qisqa yo'lni topish.
**Talablar:** O(V * E) murakkablik, salbiy sikllarni aniqlash.
**Yechim (C#):**
```csharp
public bool BellmanFord(int n, List<(int u, int v, int w)> edges, int start) {
    long[] dist = new long[n];
    Array.Fill(dist, int.MaxValue);
    dist[start] = 0;
    for (int i = 0; i < n - 1; i++)
        foreach (var e in edges)
            if (dist[e.u] + e.w < dist[e.v]) dist[e.v] = dist[e.u] + e.w;
    // Salbiy siklni tekshirish
    foreach (var e in edges) if (dist[e.u] + e.w < dist[e.v]) return false;
    return true;
}
```
**Tushuntirish:** Dijkstra ishlamaydigan holatlarda, Bellman-Ford salbiy sikllarni aniqlash orqali tizim barqarorligini ta'minlaydi.

---

### Topshiriq #1061: Tarmoq trafigini optimallashtirish (Dijkstra)
**Tavsif:** Katta ma'lumotlar markazlari o'rtasidagi eng qisqa marshrutni topish. Real vaqt rejimida paketlar yo'nalishini aniqlash uchun zarur.
**Talablar:** O(E log V) murakkablik, xotira xavfsizligi uchun `PriorityQueue` dan foydalanish.
**Yechim (C#):**
```csharp
using System;
using System.Collections.Generic;

public class NetworkOptimizer {
    public static int GetShortestPath(int n, List<(int to, int weight)>[] adj, int start, int end) {
        int[] dist = new int[n];
        Array.Fill(dist, int.MaxValue);
        dist[start] = 0;
        var pq = new PriorityQueue<int, int>();
        pq.Enqueue(start, 0);

        while (pq.Count > 0) {
            int u = pq.Dequeue();
            foreach (var edge in adj[u]) {
                if (dist[u] + edge.weight < dist[edge.to]) {
                    dist[edge.to] = dist[u] + edge.weight;
                    pq.Enqueue(edge.to, dist[edge.to]);
                }
            }
        }
        return dist[end];
    }
}
```
**Tushuntirish:** Dijkstra algoritmi `PriorityQueue` bilan birgalikda eng samarali yo'lni topishda minimal vaqt sarflaydi.

---

### Topshiriq #1062: Dinamik diapazonli yig'indilarni hisoblash (Fenwick Tree)
**Tavsif:** Moliya tizimlarida tranzaksiyalar oqimini real vaqtda kuzatish.
**Talablar:** O(log N) yangilash va so'rov tezligi.
**Yechim (C#):**
```csharp
public class FenwickTree {
    private long[] tree;
    public FenwickTree(int n) => tree = new long[n + 1];

    public void Update(int i, long delta) {
        for (; i < tree.Length; i += i & -i) tree[i] += delta;
    }

    public long Query(int i) {
        long sum = 0;
        for (; i > 0; i -= i & -i) sum += tree[i];
        return sum;
    }
}
```
**Tushuntirish:** Fenwick Tree (Binary Indexed Tree) xotira tejamkorligi va tezligi bo'yicha Segment Tree dan ustunroqdir.

---

### Topshiriq #1063: Katta hajmli matnlarni qidirish (Trie)
**Tavsif:** Milliy qidiruv tizimlarida avtomatik to'ldirish (autocomplete) funksiyasini amalga oshirish.
**Talablar:** Prefiks bo'yicha qidiruv O(L) murakkablikda bo'lishi kerak.
**Yechim (C#):**
```csharp
public class TrieNode {
    public Dictionary<char, TrieNode> Children = new();
    public bool IsEndOfWord;
}

public class Trie {
    private readonly TrieNode root = new();
    public void Insert(string word) {
        var curr = root;
        foreach (var c in word) {
            if (!curr.Children.ContainsKey(c)) curr.Children[c] = new TrieNode();
            curr = curr.Children[c];
        }
        curr.IsEndOfWord = true;
    }
}
```
**Tushuntirish:** Trie tuzilmasi lug'at hajmi katta bo'lganda qidiruvni eksponensial tezlashtiradi.

---

### Topshiriq #1064: Intervaldagi eng katta qiymatni topish (Segment Tree)
**Tavsif:** Sensor ma'lumotlari oqimida eng yuqori ko'rsatkichlarni (peak) aniqlash.
**Talablar:** O(log N) murakkablik, thread-safe yondashuv.
**Yechim (C#):**
```csharp
public class SegmentTree {
    private int[] tree;
    private int n;
    public SegmentTree(int[] data) {
        n = data.Length;
        tree = new int[2 * n];
        for (int i = 0; i < n; i++) tree[n + i] = data[i];
        for (int i = n - 1; i > 0; i--) tree[i] = Math.Max(tree[2 * i], tree[2 * i + 1]);
    }
    public int Query(int l, int r) {
        int res = 0;
        for (l += n, r += n; l < r; l >>= 1, r >>= 1) {
            if ((l & 1) == 1) res = Math.Max(res, tree[l++]);
            if ((r & 1) == 1) res = Math.Max(res, tree[--r]);
        }
        return res;
    }
}
```
**Tushuntirish:** Iterativ Segment Tree rekursiv yondashuvga qaraganda kamroq stack xotira sarflaydi.

---

### Topshiriq #1065: Tarmoq komponentlarini aniqlash (DFS/BFS)
**Tavsif:** Ijtimoiy tarmoqlarda foydalanuvchilar guruhlarini (klasterlarni) aniqlash.
**Talablar:** O(V + E) murakkablik, rekursiya chuqurligini nazorat qilish.
**Yechim (C#):**
```csharp
public void FindComponents(List<int>[] adj, int n) {
    bool[] visited = new bool[n];
    for (int i = 0; i < n; i++) {
        if (!visited[i]) {
            // BFS yordamida komponentni topish
            var q = new Queue<int>();
            q.Enqueue(i);
            visited[i] = true;
            while (q.Count > 0) {
                int u = q.Dequeue();
                foreach (var v in adj[u]) if (!visited[v]) { visited[v] = true; q.Enqueue(v); }
            }
        }
    }
}
```
**Tushuntirish:** BFS xotira xavfsizligi nuqtai nazaridan chuqur graflar uchun DFS dan xavfsizroqdir.

---

### Topshiriq #1066: Eng yaqin qo'shni (K-D Tree asoslari)
**Tavsif:** Geolokatsiya tizimlarida eng yaqin obyektlarni topish.
**Talablar:** Ko'p o'lchovli fazoda qidiruv samaradorligini ta'minlash.
**Yechim (C#):**
```csharp
public class KDNode {
    public double[] Point;
    public KDNode Left, Right;
    public KDNode(double[] p) => Point = p;
}
// K-D Tree qidiruv mantig'i nuqtalarni fazoviy bo'lish uchun ishlatiladi.
```
**Tushuntirish:** K-D Tree fazoviy ma'lumotlarni indekslash uchun eng optimal yechimdir.

---

### Topshiriq #1067: Tranzaksiyalar zanjirini tekshirish (Union-Find)
**Tavsif:** Bank tizimlarida shubhali hisoblar o'rtasidagi bog'liqlikni aniqlash.
**Talablar:** Path compression va union by rank texnikasi.
**Yechim (C#):**
```csharp
public class UnionFind {
    private int[] parent;
    public UnionFind(int n) {
        parent = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
    }
    public int Find(int i) => parent[i] == i ? i : (parent[i] = Find(parent[i]));
    public void Union(int i, int j) {
        int rootI = Find(i), rootJ = Find(j);
        if (rootI != rootJ) parent[rootI] = rootJ;
    }
}
```
**Tushuntirish:** Path compression operatsiyani deyarli O(1) ga yaqinlashtiradi.

---

### Topshiriq #1068: Katta hajmli ma'lumotlar oqimida medianani topish
**Tavsif:** IoT qurilmalari oqimida o'rtacha qiymatni real vaqtda hisoblash.
**Talablar:** Ikki tomonlama PriorityQueue (Min-Max heap).
**Yechim (C#):**
```csharp
public class MedianFinder {
    private PriorityQueue<int, int> minHeap = new();
    private PriorityQueue<int, int> maxHeap = new(Comparer<int>.Create((a, b) => b.CompareTo(a)));
    
    public void AddNum(int num) {
        maxHeap.Enqueue(num, num);
        minHeap.Enqueue(maxHeap.Dequeue(), maxHeap.Count);
        if (minHeap.Count > maxHeap.Count) maxHeap.Enqueue(minHeap.Dequeue(), minHeap.Count);
    }
}
```
**Tushuntirish:** Ikkita heap yordamida medianani O(log N) da topish mumkin.

---

### Topshiriq #1069: Topologik tartiblash (Kahn algoritmi)
**Tavsif:** Loyihalarni boshqarish tizimida vazifalar ketma-ketligini (dependency) aniqlash.
**Talablar:** Sikllarni aniqlash va O(V + E) murakkablik.
**Yechim (C#):**
```csharp
public List<int> TopologicalSort(int n, List<int>[] adj, int[] inDegree) {
    var queue = new Queue<int>();
    for (int i = 0; i < n; i++) if (inDegree[i] == 0) queue.Enqueue(i);
    var result = new List<int>();
    while (queue.Count > 0) {
        int u = queue.Dequeue();
        result.Add(u);
        foreach (var v in adj[u]) if (--inDegree[v] == 0) queue.Enqueue(v);
    }
    return result;
}
```
**Tushuntirish:** Kahn algoritmi vazifalar o'rtasidagi bog'liqlikni aniq tartiblaydi.

---

### Topshiriq #1070: Minimal qamrovchi daraxt (Kruskal)
**Tavsif:** Milliy elektr tarmoqlarini eng kam xarajat bilan ulash.
**Talablar:** Disjoint Set Union (DSU) bilan integratsiya.
**Yechim (C#):**
```csharp
public class Edge : IComparable<Edge> {
    public int U, V, Weight;
    public int CompareTo(Edge other) => Weight.CompareTo(other.Weight);
}
// Kruskal algoritmi qirralarni saralab, DSU orqali siklsiz daraxt quradi.
```
**Tushuntirish:** Kruskal algoritmi tarmoq infratuzilmasini optimallashtirishda eng ishonchli usul hisoblanadi.

---

### Topshiriq #1071: Tarmoq topologiyasida Dijkstra algoritmi
**Tavsif:** Katta hajmdagi serverlar tarmog'ida paketlarni eng qisqa yo'l bilan uzatish.
**Talablar:** O(E log V) murakkablik, xavfsizlik uchun yo'naltirilgan graflardan foydalanish.
**Yechim (C#):**
```csharp
using System;
using System.Collections.Generic;

public class NetworkRouter {
    // Dijkstra algoritmi yordamida eng qisqa yo'lni topish
    public static int GetShortestPath(int n, List<(int to, int weight)>[] adj, int start) {
        int[] dist = new int[n];
        Array.Fill(dist, int.MaxValue);
        dist[start] = 0;
        var pq = new SortedSet<(int d, int node)>();
        pq.Add((0, start));

        while (pq.Count > 0) {
            var (d, u) = pq.Min;
            pq.Remove(pq.Min);
            foreach (var edge in adj[u]) {
                if (dist[u] + edge.weight < dist[edge.to]) {
                    pq.Remove((dist[edge.to], edge.to));
                    dist[edge.to] = dist[u] + edge.weight;
                    pq.Add((dist[edge.to], edge.to));
                }
            }
        }
        return dist[n - 1];
    }
}
```
**Tushuntirish:** `SortedSet` yordamida ustuvor navbat (Priority Queue) simulyatsiya qilindi, bu katta tarmoqlarda ishlash tezligini oshiradi.

---

### Topshiriq #1072: Segment Tree orqali diapazon yig'indisi
**Tavsif:** Moliya tizimida ma'lum vaqt oralig'idagi tranzaksiyalar yig'indisini tezkor hisoblash.
**Talablar:** O(log N) yangilash va so'rov vaqti.
**Yechim (C#):**
```csharp
public class SegmentTree {
    private long[] tree;
    private int n;
    public SegmentTree(long[] data) {
        n = data.Length;
        tree = new long[2 * n];
        for (int i = 0; i < n; i++) tree[n + i] = data[i];
        for (int i = n - 1; i > 0; i--) tree[i] = tree[2 * i] + tree[2 * i + 1];
    }
    public void Update(int i, long val) {
        for (tree[i += n] = val; i > 1; i >>= 1) tree[i >> 1] = tree[i] + tree[i ^ 1];
    }
    public long Query(int l, int r) {
        long res = 0;
        for (l += n, r += n; l < r; l >>= 1, r >>= 1) {
            if ((l & 1) == 1) res += tree[l++];
            if ((r & 1) == 1) res += tree[--r];
        }
        return res;
    }
}
```
**Tushuntirish:** Iterativ Segment Tree xotirani tejaydi va rekursiv chaqiruvlarsiz yuqori unumdorlikni ta'minlaydi.

---

### Topshiriq #1073: Fenwick Tree (Binary Indexed Tree)
**Tavsif:** Katta massivlarda tezkor prefiks yig'indilarini hisoblash va yangilash.
**Talablar:** O(log N) murakkablik, minimal xotira sarfi.
**Yechim (C#):**
```csharp
public class FenwickTree {
    private int[] tree;
    public FenwickTree(int n) => tree = new int[n + 1];
    public void Update(int i, int delta) {
        for (; i < tree.Length; i += i & -i) tree[i] += delta;
    }
    public int Query(int i) {
        int sum = 0;
        for (; i > 0; i -= i & -i) sum += tree[i];
        return sum;
    }
}
```
**Tushuntirish:** BIT (Fenwick) Segment Tree'ga qaraganda kamroq xotira talab qiladi, bu esa katta datasetlarda samarali.

---

### Topshiriq #1074: Trie (Prefix Tree) yordamida avtomatik to'ldirish
**Tavsif:** Foydalanuvchi qidiruv so'rovlarini tezkor taklif qilish tizimi.
**Talablar:** O(L) qidiruv vaqti, bu yerda L - so'z uzunligi.
**Yechim (C#):**
```csharp
public class TrieNode {
    public Dictionary<char, TrieNode> Children = new();
    public bool IsEndOfWord;
}
public class Trie {
    private readonly TrieNode root = new();
    public void Insert(string word) {
        var curr = root;
        foreach (var c in word) {
            if (!curr.Children.ContainsKey(c)) curr.Children[c] = new TrieNode();
            curr = curr.Children[c];
        }
        curr.IsEndOfWord = true;
    }
}
```
**Tushuntirish:** `Dictionary` dan foydalanish xotirani dinamik boshqarish va tezkor qidiruvni ta'minlaydi.

---

### Topshiriq #1075: Grafda bog'langan komponentlarni topish (DFS)
**Tavsif:** Ijtimoiy tarmoqlarda "do'stlar guruhini" aniqlash.
**Talablar:** O(V + E) murakkablik, rekursiv xavfsizlik.
**Yechim (C#):**
```csharp
public void FindComponents(List<int>[] adj, int n) {
    bool[] visited = new bool[n];
    for (int i = 0; i < n; i++) {
        if (!visited[i]) {
            DFS(i, adj, visited);
            Console.WriteLine("Yangi komponent topildi.");
        }
    }
}
private void DFS(int u, List<int>[] adj, bool[] visited) {
    visited[u] = true;
    foreach (var v in adj[u]) if (!visited[v]) DFS(v, adj, visited);
}
```
**Tushuntirish:** DFS algoritmi grafning barcha bog'langan qismlarini to'liq qamrab olish uchun eng optimal yondashuvdir.

---

### Topshiriq #1076: Kruskal algoritmi (MST)
**Tavsif:** Shaharlararo optik tolali kabel yotqizishda minimal xarajatli tarmoqni loyihalash.
**Talablar:** Disjoint Set Union (DSU) bilan integratsiya.
**Yechim (C#):**
```csharp
public class DSU {
    int[] parent;
    public DSU(int n) { parent = new int[n]; for(int i=0; i<n; i++) parent[i] = i; }
    public int Find(int i) => parent[i] == i ? i : (parent[i] = Find(parent[i]));
    public void Union(int i, int j) { int rootI = Find(i); int rootJ = Find(j); if(rootI != rootJ) parent[rootI] = rootJ; }
}
```
**Tushuntirish:** DSU (Union-Find) Kruskal algoritmini tezlashtirish uchun zarur bo'lgan eng muhim yordamchi tuzilmadir.

---

### Topshiriq #1077: KMP (Knuth-Morris-Pratt) satr qidiruvi
**Tavsif:** Katta matnlar ichidan maxfiy kodlarni qidirish.
**Talablar:** O(N + M) vaqt murakkabligi.
**Yechim (C#):**
```csharp
public int[] ComputeLPS(string pattern) {
    int[] lps = new int[pattern.Length];
    for (int i = 1, len = 0; i < pattern.Length; ) {
        if (pattern[i] == pattern[len]) lps[i++] = ++len;
        else if (len != 0) len = lps[len - 1];
        else lps[i++] = 0;
    }
    return lps;
}
```
**Tushuntirish:** LPS massivi qidiruv jarayonida ortiqcha solishtirishlarni oldini oladi, bu esa katta hajmdagi ma'lumotlarda juda muhim.

---

### Topshiriq #1078: Bellman-Ford algoritmi
**Tavsif:** Salbiy og'irlikdagi qirralar mavjud bo'lgan moliyaviy tranzaksiya graflarida eng qisqa yo'lni topish.
**Talablar:** Salbiy sikllarni aniqlash qobiliyati.
**Yechim (C#):**
```csharp
public bool BellmanFord(int n, List<(int u, int v, int w)> edges, int start) {
    long[] dist = new long[n];
    Array.Fill(dist, int.MaxValue);
    dist[start] = 0;
    for (int i = 0; i < n - 1; i++)
        foreach (var e in edges)
            if (dist[e.u] != int.MaxValue && dist[e.u] + e.w < dist[e.v]) dist[e.v] = dist[e.u] + e.w;
    // Salbiy siklni tekshirish
    foreach (var e in edges) if (dist[e.u] + e.w < dist[e.v]) return false;
    return true;
}
```
**Tushuntirish:** Dijkstra salbiy og'irliklarda ishlamaydi, Bellman-Ford esa bu muammoni hal qiladi.

---

### Topshiriq #1079: Topological Sort (Kahn algoritmi)
**Tavsif:** Loyiha vazifalarini bajarish ketma-ketligini (dependency) aniqlash.
**Talablar:** O(V + E) murakkablik.
**Yechim (C#):**
```csharp
public List<int> TopoSort(int n, List<int>[] adj, int[] inDegree) {
    var queue = new Queue<int>();
    for (int i = 0; i < n; i++) if (inDegree[i] == 0) queue.Enqueue(i);
    var result = new List<int>();
    while (queue.Count > 0) {
        int u = queue.Dequeue();
        result.Add(u);
        foreach (var v in adj[u]) if (--inDegree[v] == 0) queue.Enqueue(v);
    }
    return result;
}
```
**Tushuntirish:** Kahn algoritmi DAG (Directed Acyclic Graph) tuzilmalarida vazifalarni tartiblash uchun eng xavfsiz va samarali usuldir.

---

### Topshiriq #1080: Suffix Trie (Qisqartirilgan)
**Tavsif:** Katta genom yoki matnlar ichida takrorlanuvchi qismlarni qidirish.
**Talablar:** Xotirani tejash va tezkor indekslash.
**Yechim (C#):**
```csharp
public class SuffixTrie {
    private TrieNode root = new();
    public void Build(string text) {
        for (int i = 0; i < text.Length; i++) {
            var curr = root;
            for (int j = i; j < text.Length; j++) {
                if (!curr.Children.ContainsKey(text[j])) curr.Children[text[j]] = new TrieNode();
                curr = curr.Children[text[j]];
            }
        }
    }
}
```
**Tushuntirish:** Suffix Trie ma'lumotlar bazasida "substring search" operatsiyalarini O(M) vaqtda bajarish imkonini beradi.

---

### Topshiriq #1081: Graflarda eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Logistika tizimida shaharlararo eng qisqa masofani aniqlash.
**Talablar:** O(E log V) murakkablik, PriorityQueue dan foydalanish.
**Yechim (C#):**
```csharp
using System;
using System.Collections.Generic;

public class Dijkstra {
    public static void FindShortestPath(List<(int to, int weight)>[] graph, int start) {
        int n = graph.Length;
        int[] dist = new int[n];
        Array.Fill(dist, int.MaxValue);
        dist[start] = 0;
        var pq = new PriorityQueue<int, int>();
        pq.Enqueue(start, 0);

        while (pq.Count > 0) {
            int u = pq.Dequeue();
            foreach (var edge in graph[u]) {
                if (dist[u] + edge.weight < dist[edge.to]) {
                    dist[edge.to] = dist[u] + edge.weight;
                    pq.Enqueue(edge.to, dist[edge.to]);
                }
            }
        }
    }
}
```
**Tushuntirish:** PriorityQueue yordamida eng kam xarajatli tugunni tanlash orqali vaqt murakkabligini optimallashtirdik.

### Topshiriq #1082: Segment Tree yordamida diapazon yig'indisi
**Tavsif:** Moliya tizimida ma'lum vaqt oralig'idagi tranzaksiyalar yig'indisini tezkor hisoblash.
**Talablar:** O(log N) yangilash va so'rov vaqti.
**Yechim (C#):**
```csharp
public class SegmentTree {
    private int[] tree;
    private int n;
    public SegmentTree(int[] arr) {
        n = arr.Length;
        tree = new int[2 * n];
        for (int i = 0; i < n; i++) tree[n + i] = arr[i];
        for (int i = n - 1; i > 0; i--) tree[i] = tree[2 * i] + tree[2 * i + 1];
    }
    public int Query(int l, int r) {
        int sum = 0;
        for (l += n, r += n; l < r; l >>= 1, r >>= 1) {
            if ((l & 1) == 1) sum += tree[l++];
            if ((r & 1) == 1) sum += tree[--r];
        }
        return sum;
    }
}
```
**Tushuntirish:** Iterativ Segment Tree xotira samaradorligi va tezlik bo'yicha eng optimal yechimdir.

### Topshiriq #1083: Fenwick Tree (Binary Indexed Tree)
**Tavsif:** Katta hajmdagi ma'lumotlar oqimida kümülatif chastotalarni hisoblash.
**Talablar:** O(log N) murakkablik, minimal xotira sarfi.
**Yechim (C#):**
```csharp
public class FenwickTree {
    private int[] bit;
    public FenwickTree(int n) => bit = new int[n + 1];
    public void Update(int i, int val) {
        for (; i < bit.Length; i += i & -i) bit[i] += val;
    }
    public int Query(int i) {
        int sum = 0;
        for (; i > 0; i -= i & -i) sum += bit[i];
        return sum;
    }
}
```
**Tushuntirish:** Bitwise operatsiyalar yordamida indekslarni boshqarish Fenwick Tree'ni juda tezkor qiladi.

### Topshiriq #1084: Trie (Prefix Tree) implementatsiyasi
**Tavsif:** Milliy qidiruv tizimida so'zlarni avtomatik to'ldirish (Autocomplete).
**Talablar:** O(L) qidiruv vaqti, bu yerda L - so'z uzunligi.
**Yechim (C#):**
```csharp
public class TrieNode {
    public Dictionary<char, TrieNode> Children = new();
    public bool IsEndOfWord;
}
public class Trie {
    private readonly TrieNode root = new();
    public void Insert(string word) {
        var curr = root;
        foreach (var ch in word) {
            if (!curr.Children.ContainsKey(ch)) curr.Children[ch] = new TrieNode();
            curr = curr.Children[ch];
        }
        curr.IsEndOfWord = true;
    }
}
```
**Tavsif:** Trie tuzilmasi prefikslarni saqlashda xotirani tejash va qidiruvni tezlashtirish uchun eng yaxshi tanlovdir.

### Topshiriq #1085: Graflarda siklni aniqlash (DFS)
**Tavsif:** Tarmoq topologiyasida bog'liqliklar zanjirini (deadlock) aniqlash.
**Talablar:** O(V + E) murakkablik, rekursiv xavfsizlik.
**Yechim (C#):**
```csharp
public bool HasCycle(List<int>[] adj, int u, bool[] visited, bool[] recStack) {
    visited[u] = true;
    recStack[u] = true;
    foreach (var v in adj[u]) {
        if (!visited[v] && HasCycle(adj, v, visited, recStack)) return true;
        else if (recStack[v]) return true;
    }
    recStack[u] = false;
    return false;
}
```
**Tushuntirish:** `recStack` yordamida joriy rekursiya yo'lida tugun mavjudligini tekshirish siklni aniqlashning standart usulidir.

### Topshiriq #1086: Union-Find (Disjoint Set Union)
**Tavsif:** Ijtimoiy tarmoqlarda do'stlik guruhlarini (klasterlarni) birlashtirish.
**Talablar:** Path compression va union by rank optimizatsiyasi.
**Yechim (C#):**
```csharp
public class DSU {
    int[] parent;
    public DSU(int n) {
        parent = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
    }
    public int Find(int i) {
        if (parent[i] == i) return i;
        return parent[i] = Find(parent[i]); // Path compression
    }
    public void Union(int i, int j) {
        int rootI = Find(i);
        int rootJ = Find(j);
        if (rootI != rootJ) parent[rootI] = rootJ;
    }
}
```
**Tushuntirish:** Path compression operatsiyasi daraxt balandligini minimal darajada ushlab turadi.

### Topshiriq #1087: Topological Sort (Kahn algoritmi)
**Tavsif:** Loyiha vazifalarini bajarish ketma-ketligini (Dependency Resolution) aniqlash.
**Talablar:** O(V + E) murakkablik, in-degree hisobi.
**Yechim (C#):**
```csharp
public List<int> TopoSort(int n, List<int>[] adj, int[] inDegree) {
    var queue = new Queue<int>();
    for (int i = 0; i < n; i++) if (inDegree[i] == 0) queue.Enqueue(i);
    var result = new List<int>();
    while (queue.Count > 0) {
        int u = queue.Dequeue();
        result.Add(u);
        foreach (var v in adj[u]) if (--inDegree[v] == 0) queue.Enqueue(v);
    }
    return result;
}
```
**Tushuntirish:** Kahn algoritmi siklsiz yo'naltirilgan graflar (DAG) uchun eng samarali tartiblash usulidir.

### Topshiriq #1088: Segment Tree bilan Lazy Propagation
**Tavsif:** Katta diapazondagi qiymatlarni bir vaqtda yangilash (Range Update).
**Talablar:** O(log N) murakkablik.
**Yechim (C#):**
```csharp
// Qisman ko'rinish: Yangilash jarayonida 'lazy' massivdan foydalanish
private void UpdateRange(int node, int start, int end, int l, int r, int val) {
    if (lazy[node] != 0) {
        tree[node] += (end - start + 1) * lazy[node];
        if (start != end) { lazy[2 * node] += lazy[node]; lazy[2 * node + 1] += lazy[node]; }
        lazy[node] = 0;
    }
    // ... rekursiv mantiq
}
```
**Tushuntirish:** Lazy propagation keraksiz hisoblashlarni keyinga qoldirib, ishlash tezligini keskin oshiradi.

### Topshiriq #1089: Trie yordamida eng uzun umumiy prefiks
**Tavsif:** Katta lug'at bazasidan so'zlar guruhining umumiy qismini topish.
**Talablar:** Xotira xavfsizligi va tezkor qidiruv.
**Yechim (C#):**
```csharp
public string FindLongestPrefix(string[] words) {
    var root = new TrieNode();
    foreach (var w in words) Insert(w);
    // Trie bo'ylab faqat bitta bolasi bor tugunlarni yurib chiqish
    // ...
    return prefix;
}
```
**Tushuntirish:** Trie tuzilmasi prefiks muammolarini chiziqli vaqtda hal qilishga imkon beradi.

### Topshiriq #1090: Kruskal algoritmi (Minimum Spanning Tree)
**Tavsif:** Milliy aloqa tarmoqlarini eng kam xarajat bilan bog'lash.
**Talablar:** Edge sorting va DSU integratsiyasi.
**Yechim (C#):**
```csharp
public int Kruskal(int n, List<(int u, int v, int weight)> edges) {
    edges.Sort((a, b) => a.weight.CompareTo(b.weight));
    var dsu = new DSU(n);
    int mstWeight = 0;
    foreach (var edge in edges) {
        if (dsu.Find(edge.u) != dsu.Find(edge.v)) {
            dsu.Union(edge.u, edge.v);
            mstWeight += edge.weight;
        }
    }
    return mstWeight;
}
```
**Tushuntirish:** Qirralarni vazn bo'yicha saralash va DSU dan foydalanish MST muammosini eng samarali yechish usulidir.

---

### Topshiriq #1091: Tarmoq Latentligini Minimallashtirish (Dijkstra)
**Tavsif:** Katta hajmdagi serverlar tarmog'ida ma'lumotlar uzatish uchun eng qisqa yo'lni topish.
**Talablar:** O(E log V) murakkablik, xotira xavfsizligi uchun `PriorityQueue` dan foydalanish.
**Yechim (C#):**
```csharp
public class NetworkOptimizer {
    public int GetShortestPath(int n, List<(int to, int weight)>[] adj, int start) {
        int[] dist = Enumerable.Repeat(int.MaxValue, n).ToArray();
        dist[start] = 0;
        var pq = new PriorityQueue<int, int>();
        pq.Enqueue(start, 0);

        while (pq.Count > 0) {
            int u = pq.Dequeue();
            foreach (var edge in adj[u]) {
                if (dist[u] + edge.weight < dist[edge.to]) {
                    dist[edge.to] = dist[u] + edge.weight;
                    pq.Enqueue(edge.to, dist[edge.to]);
                }
            }
        }
        return dist.Max(); // Eng uzoq tugungacha bo'lgan masofa
    }
}
```
**Tushuntirish:** Dijkstra algoritmi `PriorityQueue` bilan birgalikda eng samarali yo'lni topishda minimal vaqt sarflaydi.

### Topshiriq #1092: Dinamik Diapazon Summasini Hisoblash (Segment Tree)
**Tavsif:** Real vaqt rejimida moliyaviy tranzaksiyalar oqimini kuzatish.
**Talablar:** Yangilash va so'rovlar uchun O(log N) vaqt murakkabligi.
**Yechim (C#):**
```csharp
public class SegmentTree {
    private long[] tree;
    private int n;
    public SegmentTree(long[] arr) {
        n = arr.Length;
        tree = new long[2 * n];
        for (int i = 0; i < n; i++) tree[n + i] = arr[i];
        for (int i = n - 1; i > 0; i--) tree[i] = tree[2 * i] + tree[2 * i + 1];
    }
    public void Update(int i, long val) {
        for (tree[i += n] = val; i > 1; i >>= 1) tree[i >> 1] = tree[i] + tree[i ^ 1];
    }
}
```
**Tushuntirish:** Segment Tree massivdagi o'zgarishlarni tezkor qayta ishlash uchun eng optimal tuzilmadir.

### Topshiriq #1093: Prefiks Summalarni Tezkor Yangilash (Fenwick Tree)
**Tavsif:** Foydalanuvchi faolligini tahlil qilishda kümülatif statistikani yuritish.
**Talablar:** Kam xotira sarfi, O(log N) operatsiya tezligi.
**Yechim (C#):**
```csharp
public class FenwickTree {
    private int[] bit;
    public FenwickTree(int n) => bit = new int[n + 1];
    public void Update(int i, int delta) {
        for (; i < bit.Length; i += i & -i) bit[i] += delta;
    }
    public int Query(int i) {
        int sum = 0;
        for (; i > 0; i -= i & -i) sum += bit[i];
        return sum;
    }
}
```
**Tushuntirish:** Fenwick Tree (BIT) Segment Tree'ga qaraganda kamroq xotira talab qiladi va implementatsiyasi sodda.

### Topshiriq #1094: Avtomatik To'ldirish Tizimi (Trie)
**Tavsif:** Milliy qidiruv tizimida so'rovlarni tezkor bashorat qilish.
**Talablar:** So'zlarni izlashda O(L) murakkablik (L - so'z uzunligi).
**Yechim (C#):**
```csharp
public class TrieNode {
    public Dictionary<char, TrieNode> Children = new();
    public bool IsEndOfWord;
}
public class Trie {
    private readonly TrieNode root = new();
    public void Insert(string word) {
        var curr = root;
        foreach (var ch in word) {
            if (!curr.Children.ContainsKey(ch)) curr.Children[ch] = new TrieNode();
            curr = curr.Children[ch];
        }
        curr.IsEndOfWord = true;
    }
}
```
**Tushuntirish:** Trie tuzilmasi prefikslar bo'yicha qidiruvni o'ta tezlashtiradi, bu esa avtomatik to'ldirish uchun ideal.

### Topshiriq #1095: Tarmoq Komponentlarini Aniqlash (Union-Find)
**Tavsif:** Ijtimoiy tarmoqlarda do'stlar guruhini (klasterlarni) aniqlash.
**Talablar:** Path compression va union by rank texnikasi.
**Yechim (C#):**
```csharp
public class DSU {
    private int[] parent;
    public DSU(int n) {
        parent = Enumerable.Range(0, n).ToArray();
    }
    public int Find(int i) {
        if (parent[i] == i) return i;
        return parent[i] = Find(parent[i]); // Path compression
    }
    public void Union(int i, int j) {
        int rootI = Find(i), rootJ = Find(j);
        if (rootI != rootJ) parent[rootI] = rootJ;
    }
}
```
**Tushuntirish:** DSU algoritmi katta hajmdagi bog'liqliklarni boshqarishda deyarli doimiy vaqtda ishlaydi.

### Topshiriq #1096: Eng Katta Umumiy Prefiks (Trie Optimization)
**Tavsif:** Fayl tizimidagi yo'llarni optimallashtirish va qisqartirish.
**Talablar:** Xotirani tejash uchun `Dictionary` o'rniga massivdan foydalanish.
**Yechim (C#):**
```csharp
public class FastTrie {
    private class Node { public int[] next = new int[26]; }
    private List<Node> nodes = new() { new Node() };
    public void Insert(string s) {
        int curr = 0;
        foreach (var c in s) {
            int idx = c - 'a';
            if (nodes[curr].next[idx] == 0) {
                nodes[curr].next[idx] = nodes.Count;
                nodes.Add(new Node());
            }
            curr = nodes[curr].next[idx];
        }
    }
}
```
**Tushuntirish:** Massiv asosidagi Trie xotirani boshqarishda `Dictionary`ga qaraganda tezroq ishlaydi.

### Topshiriq #1097: Minimal Qamrovchi Daraxt (Kruskal)
**Tavsif:** Milliy infratuzilma (elektr tarmoqlari) uchun eng arzon ulanish sxemasi.
**Talablar:** Edge listni saralash va DSU integratsiyasi.
**Yechim (C#):**
```csharp
public class Kruskal {
    public int GetMST(int n, List<(int u, int v, int w)> edges) {
        edges.Sort((a, b) => a.w.CompareTo(b.w));
        var dsu = new DSU(n);
        int cost = 0;
        foreach (var edge in edges) {
            if (dsu.Find(edge.u) != dsu.Find(edge.v)) {
                dsu.Union(edge.u, edge.v);
                cost += edge.w;
            }
        }
        return cost;
    }
}
```
**Tushuntirish:** Kruskal algoritmi tarmoq xarajatlarini minimallashtirish uchun eng ishonchli yondashuvdir.

### Topshiriq #1098: Range Minimum Query (Sparse Table)
**Tavsif:** Sensor ma'lumotlarida eng past ko'rsatkichni statik diapazonda topish.
**Talablar:** O(1) so'rov vaqti, O(N log N) oldindan ishlov berish.
**Yechim (C#):**
```csharp
public class SparseTable {
    private int[,] st;
    public SparseTable(int[] arr) {
        int n = arr.Length, k = (int)Math.Log2(n) + 1;
        st = new int[n, k];
        for (int i = 0; i < n; i++) st[i, 0] = arr[i];
        for (int j = 1; j < k; j++)
            for (int i = 0; i + (1 << j) <= n; i++)
                st[i, j] = Math.Min(st[i, j - 1], st[i + (1 << (j - 1)), j - 1]);
    }
}
```
**Tushuntirish:** Sparse Table statik ma'lumotlar uchun eng tezkor qidiruv usulidir.

### Topshiriq #1099: Topologik Saralash (Kahn's Algorithm)
**Tavsif:** Milliy loyihalarda vazifalar ketma-ketligini (Dependency) belgilash.
**Talablar:** Sikllarni aniqlash va O(V+E) murakkablik.
**Yechim (C#):**
```csharp
public List<int> TopologicalSort(int n, List<int>[] adj, int[] inDegree) {
    var queue = new Queue<int>(Enumerable.Range(0, n).Where(i => inDegree[i] == 0));
    var result = new List<int>();
    while (queue.Count > 0) {
        int u = queue.Dequeue();
        result.Add(u);
        foreach (var v in adj[u]) if (--inDegree[v] == 0) queue.Enqueue(v);
    }
    return result;
}
```
**Tushuntirish:** Kahn algoritmi vazifalar o'rtasidagi bog'liqlikni vizualizatsiya qilish va tartiblash uchun juda samarali.

### Topshiriq #1100: Kenglik bo'yicha qidiruv (BFS)
**Tavsif:** Katta graflarda eng yaqin qo'shni tugunlarni topish.
**Talablar:** Xotira xavfsizligi va `HashSet` orqali tashrif buyurilgan tugunlarni kuzatish.
**Yechim (C#):**
```csharp
public void BFS(List<int>[] adj, int start) {
    var visited = new HashSet<int>();
    var queue = new Queue<int>();
    queue.Enqueue(start);
    visited.Add(start);
    while (queue.Count > 0) {
        int u = queue.Dequeue();
        foreach (var v in adj[u]) {
            if (visited.Add(v)) queue.Enqueue(v);
        }
    }
}
```
**Tushuntirish:** BFS graflarni bosqichma-bosqich o'rganish uchun eng barqaror va tushunarli algoritmdir.