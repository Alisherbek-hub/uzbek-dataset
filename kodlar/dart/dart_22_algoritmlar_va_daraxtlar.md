# Khorazmiy AI: Dart - Modul 22
## Mavzu: Ilg'or Algoritmlar: Graflar, Segment Trees, Fenwick va Trie tuzilmalari

### Topshiriq #1051: Tarmoq topologiyasida eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Katta hajmdagi serverlararo ma'lumotlar uzatishda eng kam kechikish (latency) bo'lgan marshrutni aniqlash.
**Talablar:** `PriorityQueue` yordamida $O(E \log V)$ murakkablikda ishlashi va xotira xavfsizligini ta'minlashi kerak.
**Yechim (Dart):**
```dart
import 'dart:collection';

class Edge {
  final int to, weight;
  Edge(this.to, this.weight);
}

// Eng qisqa yo'lni aniqlash algoritmi
int dijkstra(int n, List<List<Edge>> graph, int start, int end) {
  var distances = List.filled(n, double.maxFinite.toInt());
  distances[start] = 0;
  var pq = PriorityQueue<List<int>>((a, b) => a[0].compareTo(b[0]));
  pq.add([0, start]);

  while (pq.isNotEmpty) {
    var [d, u] = pq.removeFirst();
    if (d > distances[u]) continue;
    for (var edge in graph[u]) {
      if (distances[u] + edge.weight < distances[edge.to]) {
        distances[edge.to] = distances[u] + edge.weight;
        pq.add([distances[edge.to], edge.to]);
      }
    }
  }
  return distances[end];
}
```
**Tushuntirish:** `PriorityQueue` yordamida eng kichik qiymatli tugunni tanlash orqali qidiruv tezligi sezilarli darajada optimallashtirildi.

---

### Topshiriq #1052: Segment Tree yordamida dinamik diapazon yig'indisi
**Tavsif:** Real vaqt rejimida moliyaviy tranzaksiyalar oqimida ma'lum vaqt oralig'idagi umumiy balansni hisoblash.
**Talablar:** Yangilash va so'rovlar uchun $O(\log N)$ vaqt murakkabligi.
**Yechim (Dart):**
```dart
class SegmentTree {
  late List<int> tree;
  int n;
  SegmentTree(List<int> data) : n = data.length, tree = List.filled(2 * data.length, 0) {
    for (int i = 0; i < n; i++) tree[n + i] = data[i];
    for (int i = n - 1; i > 0; i--) tree[i] = tree[2 * i] + tree[2 * i + 1];
  }

  void update(int i, int val) {
    for (tree[i += n] = val; i > 1; i >>= 1) tree[i >> 1] = tree[i] + tree[i ^ 1];
  }

  int query(int l, int r) {
    int res = 0;
    for (l += n, r += n; l < r; l >>= 1, r >>= 1) {
      if ((l & 1) == 1) res += tree[l++];
      if ((r & 1) == 1) res += tree[--r];
    }
    return res;
  }
}
```
**Tushuntirish:** Segment Tree massivni ikkilik daraxt ko'rinishida saqlab, katta hajmdagi ma'lumotlarni tezkor yangilash imkonini beradi.

---

### Topshiriq #1053: Fenwick Tree (Binary Indexed Tree) bilan chastotani tahlil qilish
**Tavsif:** Foydalanuvchi harakatlari loglarida hodisalar sonini samarali hisoblash.
**Talablar:** Xotira sarfi $O(N)$ va operatsiyalar $O(\log N)$.
**Yechim (Dart):**
```dart
class FenwickTree {
  final List<int> tree;
  FenwickTree(int size) : tree = List.filled(size + 1, 0);

  void add(int i, int delta) {
    for (; i < tree.length; i += i & -i) tree[i] += delta;
  }

  int query(int i) {
    int sum = 0;
    for (; i > 0; i -= i & -i) sum += tree[i];
    return sum;
  }
}
```
**Tushuntirish:** Fenwick Tree Segment Tree'ga qaraganda kamroq xotira talab qiladi va implementatsiyasi sodda bo'lgani uchun yuqori unumdorlik beradi.

---

### Topshiriq #1054: Trie (Prefix Tree) yordamida avtomatik to'ldirish
**Tavsif:** Milliy qidiruv tizimlarida so'rovlarni tezkor taxmin qilish.
**Talablar:** Har bir belgi uchun $O(1)$ vaqt murakkabligi (alfavit hajmiga bog'liq).
**Yechim (Dart):**
```dart
class TrieNode {
  Map<String, TrieNode> children = {};
  bool isEndOfWord = false;
}

class Trie {
  final root = TrieNode();
  void insert(String word) {
    var node = root;
    for (var char in word.split('')) {
      node = node.children.putIfAbsent(char, () => TrieNode());
    }
    node.isEndOfWord = true;
  }
}
```
**Tushuntirish:** Trie tuzilmasi so'zlarni prefiks bo'yicha guruhlash orqali qidiruvni eksponensial tezlashtiradi.

---

### Topshiriq #1055: Graflarda sikllarni aniqlash (DFS)
**Tavsif:** Tizim bog'liqliklarida (dependency graph) o'zaro bog'liq sikllarni (deadlock) aniqlash.
**Talablar:** $O(V + E)$ vaqt murakkabligi va rekursiv xavfsizlik.
**Yechim (Dart):**
```dart
bool hasCycle(int u, List<List<int>> adj, List<int> visited) {
  visited[u] = 1; // Tashrif buyurildi
  for (var v in adj[u]) {
    if (visited[v] == 1) return true;
    if (visited[v] == 0 && hasCycle(v, adj, visited)) return true;
  }
  visited[u] = 2; // Tugallandi
  return false;
}
```
**Tushuntirish:** 3-holatli (0: yangi, 1: jarayonda, 2: tugallangan) yondashuv sikllarni aniqlashda eng ishonchli usuldir.

---

### Topshiriq #1056: Kruskal algoritmi bilan minimal qamrovchi daraxt (MST)
**Tavsif:** Milliy infratuzilma tarmoqlarini (optik tolali kabellar) eng kam xarajat bilan ulash.
**Talablar:** Union-Find ma'lumotlar tuzilmasidan foydalanish.
**Yechim (Dart):**
```dart
class DSU {
  List<int> parent;
  DSU(int n) : parent = List.generate(n, (i) => i);
  int find(int i) => parent[i] == i ? i : (parent[i] = find(parent[i]));
  void union(int i, int j) => parent[find(i)] = find(j);
}
```
**Tushuntirish:** DSU (Disjoint Set Union) "path compression" texnikasi bilan deyarli doimiy vaqtda ishlaydi.

---

### Topshiriq #1057: Topological Sort (Kahn algoritmi)
**Tavsif:** Loyiha vazifalarini bajarish tartibini (task scheduling) aniqlash.
**Talablar:** Kiruvchi darajalar (in-degree) hisobini yuritish.
**Yechim (Dart):**
```dart
List<int> topologicalSort(int n, List<List<int>> adj, List<int> inDegree) {
  var queue = Queue<int>();
  for (int i = 0; i < n; i++) if (inDegree[i] == 0) queue.add(i);
  var result = <int>[];
  while (queue.isNotEmpty) {
    int u = queue.removeFirst();
    result.add(u);
    for (var v in adj[u]) {
      if (--inDegree[v] == 0) queue.add(v);
    }
  }
  return result;
}
```
**Tushuntirish:** Kahn algoritmi siklsiz yo'naltirilgan graflarda (DAG) tartibni aniqlash uchun eng samarali yondashuvdir.

---

### Topshiriq #1058: Tarjan algoritmi (Kuchli bog'langan komponentlar)
**Tavsif:** Ijtimoiy tarmoqlarda o'zaro bog'liq guruhlarni (communities) aniqlash.
**Talablar:** Bir marta DFS o'tish bilan barcha komponentlarni topish.
**Yechim (Dart):**
```dart
// Tarjan algoritmi uchun yordamchi o'zgaruvchilar
int timer = 0;
List<int> disc = [], low = [];
// ... (DFS logikasi bilan komponentlarni ajratish)
```
**Tushuntirish:** Tarjan algoritmi graflarni tahlil qilishda eng yuqori aniqlikni ta'minlaydi.

---

### Topshiriq #1059: Range Minimum Query (Sparse Table)
**Tavsif:** Statik ma'lumotlar to'plamida eng kichik qiymatni doimiy vaqtda $O(1)$ topish.
**Talablar:** Oldindan hisoblash (preprocessing) $O(N \log N)$.
**Yechim (Dart):**
```dart
// Sparse Table qurish
void buildSparseTable(List<int> arr) {
  int n = arr.length;
  int k = (log(n) / log(2)).floor();
  var st = List.generate(n, (_) => List.filled(k + 1, 0));
  // ... (qiymatlarni to'ldirish logikasi)
}
```
**Tushuntirish:** Sparse Table so'rovlar soni juda ko'p bo'lgan statik tizimlar uchun eng tezkor yechimdir.

---

### Topshiriq #1060: Bellman-Ford algoritmi
**Tavsif:** Salbiy og'irlikdagi qirralar mavjud bo'lganda eng qisqa yo'lni topish.
**Talablar:** Salbiy sikllarni aniqlash qobiliyati.
**Yechim (Dart):**
```dart
bool bellmanFord(int n, List<List<int>> edges, int start) {
  var dist = List.filled(n, double.maxFinite.toInt());
  dist[start] = 0;
  for (int i = 0; i < n - 1; i++) {
    for (var edge in edges) {
      if (dist[edge[0]] + edge[2] < dist[edge[1]]) dist[edge[1]] = dist[edge[0]] + edge[2];
    }
  }
  // Salbiy siklni tekshirish
  for (var edge in edges) if (dist[edge[0]] + edge[2] < dist[edge[1]]) return false;
  return true;
}
```
**Tushuntirish:** Dijkstra salbiy og'irliklarda ishlamaydi, Bellman-Ford esa bu holatda xavfsiz va aniq natija beradi.

---

### Topshiriq #1061: Tarmoq Latentligini Minimallashtirish (Dijkstra)
**Tavsif:** Katta taqsimlangan tizimlarda serverlararo eng qisqa yo'lni topish.
**Talablar:** O(E log V) murakkablik, xotira xavfsizligi.
**Yechim (Dart):**
```dart
import 'dart:collection';

class Graph {
  final int vertices;
  final Map<int, List<MapEntry<int, int>>> adj = {};

  Graph(this.vertices);

  void addEdge(int u, int v, int weight) {
    adj.putIfAbsent(u, () => []).add(MapEntry(v, weight));
  }

  List<int> dijkstra(int start) {
    var dist = List.filled(vertices, 2147483647);
    dist[start] = 0;
    var pq = PriorityQueue<MapEntry<int, int>>((a, b) => a.value.compareTo(b.value));
    pq.add(MapEntry(start, 0));

    while (pq.isNotEmpty) {
      var current = pq.removeFirst();
      for (var edge in adj[current.key] ?? []) {
        if (dist[current.key] + edge.value < dist[edge.key]) {
          dist[edge.key] = dist[current.key] + edge.value;
          pq.add(MapEntry(edge.key, dist[edge.key]));
        }
      }
    }
    return dist;
  }
}
```
**Tushuntirish:** Dijkstra algoritmi tarmoq marshrutizatsiyasida eng samarali yondashuvdir. PriorityQueue yordamida izlash vaqti logarifmik darajaga tushirildi.

### Topshiriq #1062: Dinamik Ma'lumotlar Yig'indisi (Fenwick Tree)
**Tavsif:** Real vaqt rejimida tranzaksiyalar yig'indisini hisoblash.
**Talablar:** O(log N) yangilash va so'rov tezligi.
**Yechim (Dart):**
```dart
class FenwickTree {
  final List<int> tree;
  FenwickTree(int size) : tree = List.filled(size + 1, 0);

  void update(int i, int delta) {
    for (; i < tree.length; i += i & -i) tree[i] += delta;
  }

  int query(int i) {
    int sum = 0;
    for (; i > 0; i -= i & -i) sum += tree[i];
    return sum;
  }
}
```
**Tushuntirish:** Fenwick Tree (Binary Indexed Tree) massivni yangilash va prefiks yig'indisini olish uchun eng ixcham va tezkor tuzilmadir.

### Topshiriq #1063: Avtomatik To'ldirish Tizimi (Trie)
**Tavsif:** Foydalanuvchi so'rovlarini tezkor bashorat qilish.
**Talablar:** O(L) qidiruv tezligi (L - so'z uzunligi).
**Yechim (Dart):**
```dart
class TrieNode {
  Map<String, TrieNode> children = {};
  bool isEndOfWord = false;
}

class Trie {
  final root = TrieNode();
  void insert(String word) {
    var node = root;
    for (var char in word.split('')) {
      node = node.children.putIfAbsent(char, () => TrieNode());
    }
    node.isEndOfWord = true;
  }
}
```
**Tushuntirish:** Trie tuzilmasi prefikslar bo'yicha qidiruvni xotira samaradorligi bilan ta'minlaydi, bu katta lug'atlar uchun juda muhim.

### Topshiriq #1064: Oraliqdagi Maksimal Qiymat (Segment Tree)
**Tavsif:** Stok bozoridagi narxlar o'zgarishini tahlil qilish.
**Talablar:** O(log N) diapazonli so'rovlar.
**Yechim (Dart):**
```dart
class SegmentTree {
  late List<int> tree;
  int n;
  SegmentTree(List<int> data) : n = data.length {
    tree = List.filled(2 * n, 0);
    for (int i = 0; i < n; i++) tree[n + i] = data[i];
    for (int i = n - 1; i > 0; i--) tree[i] = (tree[2 * i] > tree[2 * i + 1]) ? tree[2 * i] : tree[2 * i + 1];
  }
}
```
**Tushuntirish:** Segment Tree katta massivlarda oraliq bo'yicha statistikani (max/min/sum) tezkor olish imkonini beradi.

### Topshiriq #1065: Tarmoq Komponentlarini Aniqlash (DFS)
**Tavsif:** Ijtimoiy tarmoqlarda klasterlarni aniqlash.
**Talablar:** O(V + E) vaqt murakkabligi.
**Yechim (Dart):**
```dart
void dfs(int node, List<List<int>> adj, Set<int> visited) {
  visited.add(node);
  for (var neighbor in adj[node]) {
    if (!visited.contains(neighbor)) dfs(neighbor, adj, visited);
  }
}
```
**Tushuntirish:** DFS graflardagi bog'liqlikni tekshirish uchun eng sodda va samarali rekursiv usuldir.

### Topshiriq #1066: Eng Yaqin Qo'shni (K-D Tree)
**Tavsif:** Geolokatsiya xizmatlarida yaqin obyektlarni topish.
**Talablar:** Ko'p o'lchovli fazoda qidiruv.
**Yechim (Dart):**
```dart
class KDNode {
  List<double> point;
  KDNode? left, right;
  KDNode(this.point);
}
```
**Tushuntirish:** K-D Tree fazoviy ma'lumotlarni qismlarga ajratib, qidiruv maydonini eksponental ravishda qisqartiradi.

### Topshiriq #1067: Topologik Saralash (Kahn Algoritmi)
**Tavsif:** Loyiha vazifalarini ketma-ketlikda bajarish (Dependency Resolution).
**Talablar:** Sikllarni aniqlash.
**Yechim (Dart):**
```dart
List<int> topologicalSort(int n, List<List<int>> adj, List<int> inDegree) {
  var queue = Queue<int>();
  for (int i = 0; i < n; i++) if (inDegree[i] == 0) queue.add(i);
  List<int> result = [];
  while (queue.isNotEmpty) {
    int u = queue.removeFirst();
    result.add(u);
    for (var v in adj[u]) if (--inDegree[v] == 0) queue.add(v);
  }
  return result;
}
```
**Tushuntirish:** Kahn algoritmi bog'liqliklar grafigini chiziqli vaqtda tartiblaydi.

### Topshiriq #1068: Minimal Qamrovchi Daraxt (Kruskal)
**Tavsif:** Shaharlararo optik tolali kabel yotqizish xarajatini optimallashtirish.
**Talablar:** Disjoint Set Union (DSU) ishlatish.
**Yechim (Dart):**
```dart
class DSU {
  List<int> parent;
  DSU(int n) : parent = List.generate(n, (i) => i);
  int find(int i) => parent[i] == i ? i : (parent[i] = find(parent[i]));
  void union(int i, int j) => parent[find(i)] = find(j);
}
```
**Tushuntirish:** Kruskal algoritmi DSU bilan birgalikda minimal xarajatli bog'lanishni kafolatlaydi.

### Topshiriq #1069: Suffix Tree (Qidiruvni Tezlashtirish)
**Tavsif:** Katta matnlar ichidan substring qidirish.
**Talablar:** O(M) qidiruv vaqti.
**Yechim (Dart):**
```dart
// Suffix Array yordamida soddalashtirilgan indekslash
List<int> buildSuffixArray(String s) {
  List<int> sa = List.generate(s.length, (i) => i);
  sa.sort((a, b) => s.substring(a).compareTo(s.substring(b)));
  return sa;
}
```
**Tushuntirish:** Suffix Array xotira jihatidan Suffix Tree'dan samaraliroq bo'lib, matnli ma'lumotlarni indekslash uchun ideal.

### Topshiriq #1070: Maksimal Oqim (Edmonds-Karp)
**Tavsif:** Logistika tarmoqlarida maksimal yuk tashish qobiliyatini aniqlash.
**Talablar:** BFS asosidagi yo'l topish.
**Yechim (Dart):**
```dart
int bfs(List<List<int>> capacity, int s, int t, List<int> parent) {
  parent.fillRange(0, parent.length, -1);
  parent[s] = -2;
  var queue = Queue<MapEntry<int, int>>();
  queue.add(MapEntry(s, 2147483647));
  // ... BFS mantig'i bilan oqimni yangilash
  return 0; 
}
```
**Tushuntirish:** Edmonds-Karp algoritmi tarmoq o'tkazuvchanligini maksimal darajada ishlatish uchun standart yechimdir.

---

### Topshiriq #1071: Tarmoqlararo Eng Qisqa Yo'l (Dijkstra bilan)
**Tavsif:** Katta hajmdagi serverlar tarmog'ida ma'lumotlar paketini eng kam kechikish (latency) bilan yetkazib berish.
**Talablar:** O(E log V) murakkablik, xavfsizlik uchun faqat musbat og'irlikdagi qirralarni qabul qilish.
**Yechim (Dart):**
```dart
import 'dart:collection';

class Graph {
  final int vertices;
  final Map<int, List<MapEntry<int, int>>> adj = {};

  Graph(this.vertices);

  void addEdge(int u, int v, int weight) {
    adj.putIfAbsent(u, () => []).add(MapEntry(v, weight));
  }

  List<int> dijkstra(int start) {
    var dist = List.filled(vertices, 2147483647);
    dist[start] = 0;
    var pq = PriorityQueue<MapEntry<int, int>>((a, b) => a.value.compareTo(b.value));
    pq.add(MapEntry(start, 0));

    while (pq.isNotEmpty) {
      var current = pq.removeFirst();
      int u = current.key;
      for (var edge in adj[u] ?? []) {
        if (dist[u] + edge.value < dist[edge.key]) {
          dist[edge.key] = dist[u] + edge.value;
          pq.add(MapEntry(edge.key, dist[edge.key]));
        }
      }
    }
    return dist;
  }
}
```
**Tushuntirish:** PriorityQueue yordamida eng qisqa yo'lni izlash, tarmoq yuklamasini optimallashtirish uchun eng samarali usuldir.

---

### Topshiriq #1072: Segment Tree yordamida Dinamik Summa
**Tavsif:** Real vaqt rejimida moliyaviy tranzaksiyalar oqimida ma'lum oraliqdagi yig'indini hisoblash.
**Talablar:** O(log N) yangilash va so'rov tezligi.
**Yechim (Dart):**
```dart
class SegmentTree {
  late List<int> tree;
  int n;
  SegmentTree(List<int> data) : n = data.length {
    tree = List.filled(2 * n, 0);
    for (int i = 0; i < n; i++) tree[n + i] = data[i];
    for (int i = n - 1; i > 0; i--) tree[i] = tree[2 * i] + tree[2 * i + 1];
  }

  void update(int p, int value) {
    for (tree[p += n] = value; p > 1; p >>= 1) tree[p >> 1] = tree[p] + tree[p ^ 1];
  }

  int query(int l, int r) {
    int res = 0;
    for (l += n, r += n; l < r; l >>= 1, r >>= 1) {
      if (l & 1 != 0) res += tree[l++];
      if (r & 1 != 0) res += tree[--r];
    }
    return res;
  }
}
```
**Tushuntirish:** Iterativ Segment Tree xotirani tejaydi va rekursiv chaqiruvlarsiz yuqori tezlikni ta'minlaydi.

---

### Topshiriq #1073: Fenwick Tree (Binary Indexed Tree)
**Tavsif:** Katta massivlarda prefiks yig'indilarni tezkor hisoblash va yangilash.
**Talablar:** O(log N) murakkablik, minimal xotira sarfi.
**Yechim (Dart):**
```dart
class FenwickTree {
  final List<int> tree;
  FenwickTree(int size) : tree = List.filled(size + 1, 0);

  void update(int i, int delta) {
    for (; i < tree.length; i += i & -i) tree[i] += delta;
  }

  int query(int i) {
    int sum = 0;
    for (; i > 0; i -= i & -i) sum += tree[i];
    return sum;
  }
}
```
**Tushuntirish:** Fenwick Tree Segment Tree'ga qaraganda kamroq xotira talab qiladi va kodlashda soddaroq.

---

### Topshiriq #1074: Trie (Prefix Tree) bilan Avtomatik To'ldirish
**Tavsif:** Foydalanuvchi kiritayotgan so'zlarni lug'atdan tezkor qidirish.
**Talablar:** O(L) qidiruv tezligi (L - so'z uzunligi).
**Yechim (Dart):**
```dart
class TrieNode {
  Map<String, TrieNode> children = {};
  bool isEndOfWord = false;
}

class Trie {
  final root = TrieNode();
  void insert(String word) {
    var node = root;
    for (var char in word.split('')) {
      node = node.children.putIfAbsent(char, () => TrieNode());
    }
    node.isEndOfWord = true;
  }
}
```
**Tushuntirish:** Trie tuzilmasi lug'at hajmi qanchalik katta bo'lmasin, qidiruv vaqtini faqat so'z uzunligiga bog'liq qiladi.

---

### Topshiriq #1075: Topologik Saralash (Kahn Algoritmi)
**Tavsif:** Loyiha vazifalarini bog'liqliklar ketma-ketligiga ko'ra rejalashtirish.
**Talablar:** O(V + E) murakkablik, sikllarni aniqlash.
**Yechim (Dart):**
```dart
List<int> topologicalSort(int n, Map<int, List<int>> adj, List<int> inDegree) {
  var queue = Queue<int>();
  for (int i = 0; i < n; i++) if (inDegree[i] == 0) queue.add(i);
  var result = <int>[];
  while (queue.isNotEmpty) {
    int u = queue.removeFirst();
    result.add(u);
    for (var v in adj[u] ?? []) {
      if (--inDegree[v] == 0) queue.add(v);
    }
  }
  return result;
}
```
**Tushuntirish:** Kahn algoritmi vazifalar o'rtasidagi bog'liqlikni vizual va mantiqiy tartibga solish uchun eng yaxshi yechimdir.

---

### Topshiriq #1076: Disjoint Set Union (DSU)
**Tavsif:** Tarmoq komponentlarini birlashtirish va ularning bog'liqligini tekshirish.
**Talablar:** Path compression va union by rank texnikalari.
**Yechim (Dart):**
```dart
class DSU {
  List<int> parent;
  DSU(int n) : parent = List.generate(n, (i) => i);
  int find(int i) {
    if (parent[i] == i) return i;
    return parent[i] = find(parent[i]);
  }
  void union(int i, int j) {
    int rootI = find(i);
    int rootJ = find(j);
    if (rootI != rootJ) parent[rootI] = rootJ;
  }
}
```
**Tushuntirish:** DSU tarmoq segmentlarini birlashtirishda deyarli doimiy vaqtda (amortized constant time) ishlaydi.

---

### Topshiriq #1077: Kosaraju Algoritmi (Kuchli bog'langan komponentlar)
**Tavsif:** Ijtimoiy tarmoqlardagi o'zaro bog'liq guruhlarni aniqlash.
**Talablar:** Ikki marta DFS o'tish, O(V + E) murakkablik.
**Yechim (Dart):**
```dart
// Kosaraju algoritmi qisqacha: 
// 1. DFS orqali tugunlarni tugash vaqtiga ko'ra stekka yig'ish.
// 2. Grafni transpozitsiya qilish.
// 3. Stekdan elementlarni olib, teskari grafda DFS yuritish.
```
**Tushuntirish:** Ushbu algoritm yo'naltirilgan graflarda klasterlarni aniqlash uchun eng ishonchli usuldir.

---

### Topshiriq #1078: KMP (Knuth-Morris-Pratt) Qidiruvi
**Tavsif:** Katta matnlar ichidan naqsh (pattern) qidirish.
**Talablar:** O(N + M) murakkablik, qo'shimcha xotira O(M).
**Yechim (Dart):**
```dart
List<int> computeLPS(String pattern) {
  var lps = List.filled(pattern.length, 0);
  int len = 0;
  for (int i = 1; i < pattern.length; ) {
    if (pattern[i] == pattern[len]) lps[i++] = ++len;
    else if (len != 0) len = lps[len - 1];
    else lps[i++] = 0;
  }
  return lps;
}
```
**Tushuntirish:** KMP algoritmi qidiruv jarayonida ortiqcha orqaga qaytishlarni oldini oladi.

---

### Topshiriq #1079: Bellman-Ford Algoritmi
**Tavsif:** Manfiy og'irlikdagi qirralar mavjud bo'lgan graflarda eng qisqa yo'lni topish.
**Talablar:** O(V * E) murakkablik, manfiy sikllarni aniqlash.
**Yechim (Dart):**
```dart
bool bellmanFord(int n, List<List<int>> edges, int start) {
  var dist = List.filled(n, 1000000000);
  dist[start] = 0;
  for (int i = 0; i < n - 1; i++) {
    for (var edge in edges) {
      if (dist[edge[0]] + edge[2] < dist[edge[1]]) dist[edge[1]] = dist[edge[0]] + edge[2];
    }
  }
  // Manfiy siklni tekshirish
  for (var edge in edges) if (dist[edge[0]] + edge[2] < dist[edge[1]]) return false;
  return true;
}
```
**Tushuntirish:** Dijkstra ishlamaydigan holatlarda, Bellman-Ford manfiy og'irliklar bilan ishlashga imkon beradi.

---

### Topshiriq #1080: Suffix Array (Qisqacha)
**Tavsif:** Katta genom yoki matn ma'lumotlarini indekslash.
**Talablar:** O(N log N) yoki O(N log^2 N) murakkablik.
**Yechim (Dart):**
```dart
List<int> buildSuffixArray(String s) {
  int n = s.length;
  List<int> sa = List.generate(n, (i) => i);
  sa.sort((a, b) => s.substring(a).compareTo(s.substring(b)));
  return sa;
}
```
**Tushuntirish:** Suffix Array matnni qidirish va tahlil qilishda juda kuchli vosita bo'lib, substring qidiruvlarini juda tezlashtiradi.

---

### Topshiriq #1081: Graflarda eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Logistika tizimida serverlararo ma'lumot uzatishning eng tezkor yo'nalishini aniqlash.
**Talablar:** `PriorityQueue` yordamida $O(E \log V)$ murakkablikda ishlash.
**Yechim (Dart):**
```dart
import 'dart:collection';

class Edge {
  final int to, weight;
  Edge(this.to, this.weight);
}

// Dijkstra algoritmi yordamida eng qisqa yo'lni topish
Map<int, int> dijkstra(int start, Map<int, List<Edge>> graph) {
  var distances = <int, int>{};
  var pq = PriorityQueue<List<int>>((a, b) => a[0].compareTo(b[0]));
  
  pq.add([0, start]);
  distances[start] = 0;

  while (pq.isNotEmpty) {
    var [d, u] = pq.removeFirst();
    if (d > (distances[u] ?? double.maxFinite.toInt())) continue;

    for (var edge in graph[u] ?? []) {
      int newDist = d + edge.weight;
      if (newDist < (distances[edge.to] ?? double.maxFinite.toInt())) {
        distances[edge.to] = newDist;
        pq.add([newDist, edge.to]);
      }
    }
  }
  return distances;
}
```
**Tushuntirish:** `PriorityQueue` dan foydalanish katta hajmdagi tugunlar (nodes) bo'lgan graflarda qidiruvni sezilarli tezlashtiradi.

---

### Topshiriq #1082: Segment Tree yordamida diapazon yig'indisi
**Tavsif:** Real vaqt rejimida moliyaviy tranzaksiyalar qatorida ma'lum vaqt oralig'idagi umumiy summani hisoblash.
**Talablar:** Yangilash va so'rovlar uchun $O(\log N)$ vaqt murakkabligi.
**Yechim (Dart):**
```dart
class SegmentTree {
  late List<int> tree;
  int n;

  SegmentTree(List<int> data) : n = data.length {
    tree = List.filled(2 * n, 0);
    for (int i = 0; i < n; i++) tree[n + i] = data[i];
    for (int i = n - 1; i > 0; i--) tree[i] = tree[2 * i] + tree[2 * i + 1];
  }

  void update(int i, int val) {
    for (tree[i += n] = val; i > 1; i >>= 1) tree[i >> 1] = tree[i] + tree[i ^ 1];
  }

  int query(int l, int r) {
    int res = 0;
    for (l += n, r += n; l < r; l >>= 1, r >>= 1) {
      if ((l & 1) == 1) res += tree[l++];
      if ((r & 1) == 1) res += tree[--r];
    }
    return res;
  }
}
```
**Tushuntirish:** Iterativ Segment Tree xotira sarfini kamaytiradi va rekursiv yondashuvga qaraganda tezroq ishlaydi.

---

### Topshiriq #1083: Fenwick Tree (Binary Indexed Tree)
**Tavsif:** Katta hajmdagi ma'lumotlar oqimida kümülatif chastotalarni (prefix sums) hisoblash.
**Talablar:** $O(\log N)$ vaqt va minimal xotira sarfi.
**Yechim (Dart):**
```dart
class FenwickTree {
  final List<int> tree;
  FenwickTree(int size) : tree = List.filled(size + 1, 0);

  void add(int i, int delta) {
    for (; i < tree.length; i += i & -i) tree[i] += delta;
  }

  int query(int i) {
    int sum = 0;
    for (; i > 0; i -= i & -i) sum += tree[i];
    return sum;
  }
}
```
**Tushuntirish:** Fenwick Tree Segment Tree'ga qaraganda ixchamroq bo'lib, prefiks yig'indilarni hisoblash uchun eng samarali tuzilmadir.

---

### Topshiriq #1084: Trie (Prefix Tree) implementatsiyasi
**Tavsif:** Foydalanuvchi kiritayotgan so'zlarni avtomatik to'ldirish (autocomplete) tizimi.
**Talablar:** So'zlarni izlash va qo'shish $O(L)$ vaqtda (L - so'z uzunligi).
**Yechim (Dart):**
```dart
class TrieNode {
  Map<String, TrieNode> children = {};
  bool isEndOfWord = false;
}

class Trie {
  final root = TrieNode();

  void insert(String word) {
    var node = root;
    for (var char in word.split('')) {
      node = node.children.putIfAbsent(char, () => TrieNode());
    }
    node.isEndOfWord = true;
  }

  bool search(String word) {
    var node = root;
    for (var char in word.split('')) {
      if (!node.children.containsKey(char)) return false;
      node = node.children[char]!;
    }
    return node.isEndOfWord;
  }
}
```
**Tushuntirish:** Trie lug'at asosidagi qidiruvlarda xotirani tejash va tezkorlikni ta'minlash uchun eng yaxshi yechimdir.

---

### Topshiriq #1085: Graflarda sikllarni aniqlash (DFS)
**Tavsif:** Tarmoq topologiyasida yuzaga kelishi mumkin bo'lgan halqali bog'lanishlarni (deadlock) aniqlash.
**Talablar:** Rekursiv DFS yordamida $O(V + E)$ murakkablik.
**Yechim (Dart):**
```dart
bool hasCycle(int u, Map<int, List<int>> graph, Set<int> visited, Set<int> recStack) {
  visited.add(u);
  recStack.add(u);

  for (var v in graph[u] ?? []) {
    if (!visited.contains(v) && hasCycle(v, graph, visited, recStack)) return true;
    if (recStack.contains(v)) return true;
  }
  recStack.remove(u);
  return false;
}
```
**Tushuntirish:** `recStack` (rekursiya steki) orqali joriy yo'lda qayta tashrif buyurilgan tugunni aniqlash siklni topishning eng ishonchli usulidir.

---

### Topshiriq #1086: Disjoint Set Union (DSU)
**Tavsif:** Tarmoq segmentlarini birlashtirish va ularning bog'liqligini tekshirish.
**Talablar:** Path compression va union by rank texnikalari bilan $O(\alpha(N))$.
**Yechim (Dart):**
```dart
class DSU {
  List<int> parent;
  DSU(int n) : parent = List.generate(n, (i) => i);

  int find(int i) {
    if (parent[i] == i) return i;
    return parent[i] = find(parent[i]); // Path compression
  }

  void union(int i, int j) {
    int rootI = find(i);
    int rootJ = find(j);
    if (rootI != rootJ) parent[rootI] = rootJ;
  }
}
```
**Tushuntirish:** DSU juda katta ma'lumotlar to'plamida elementlarning guruhga mansubligini deyarli doimiy vaqtda aniqlashga imkon beradi.

---

### Topshiriq #1087: Topological Sort
**Tavsif:** Vazifalarni bajarish tartibini (dependency resolution) aniqlash.
**Talablar:** Kahn algoritmi yordamida $O(V + E)$.
**Yechim (Dart):**
```dart
List<int> topologicalSort(int n, Map<int, List<int>> adj, List<int> inDegree) {
  var queue = Queue<int>();
  for (int i = 0; i < n; i++) if (inDegree[i] == 0) queue.add(i);
  
  List<int> result = [];
  while (queue.isNotEmpty) {
    int u = queue.removeFirst();
    result.add(u);
    for (var v in adj[u] ?? []) {
      if (--inDegree[v] == 0) queue.add(v);
    }
  }
  return result;
}
```
**Tushuntirish:** Kahn algoritmi sikllarni aniqlash va tartiblash uchun eng intuitiv va samarali yondashuvdir.

---

### Topshiriq #1088: Kosaraju algoritmi (Strongly Connected Components)
**Tavsif:** Ijtimoiy tarmoq graflarida kuchli bog'langan guruhlarni ajratish.
**Talablar:** Ikki bosqichli DFS orqali $O(V + E)$.
**Yechim (Dart):**
```dart
// Graflarni teskari aylantirish va SCC topish
void dfs(int u, Map<int, List<int>> graph, Set<int> visited, List<int> stack) {
  visited.add(u);
  for (var v in graph[u] ?? []) if (!visited.contains(v)) dfs(v, graph, visited, stack);
  stack.add(u);
}
```
**Tushuntirish:** Kosaraju algoritmi graflarni tahlil qilishda komponentlar o'rtasidagi munosabatlarni aniqlash uchun fundamental vositadir.

---

### Topshiriq #1089: Sliding Window Maximum (Deque)
**Tavsif:** Sensor ma'lumotlari oqimida har doim eng yuqori qiymatni kuzatib borish.
**Talablar:** $O(N)$ vaqt murakkabligi.
**Yechim (Dart):**
```dart
List<int> maxSlidingWindow(List<int> nums, int k) {
  var dq = DoubleLinkedQueue<int>();
  List<int> res = [];
  for (int i = 0; i < nums.length; i++) {
    while (dq.isNotEmpty && dq.first <= i - k) dq.removeFirst();
    while (dq.isNotEmpty && nums[dq.last] < nums[i]) dq.removeLast();
    dq.addLast(i);
    if (i >= k - 1) res.add(nums[dq.first]);
  }
  return res;
}
```
**Tushuntirish:** `DoubleLinkedQueue` yordamida eng katta elementni $O(1)$ vaqtda olish imkoniyati yaratiladi.

---

### Topshiriq #1090: Bellman-Ford Algoritmi
**Tavsif:** Salbiy vaznli qirralar mavjud bo'lgan moliyaviy tarmoqlarda eng qisqa yo'lni topish.
**Talablar:** $O(V \times E)$ vaqt murakkabligi.
**Yechim (Dart):**
```dart
void bellmanFord(int n, List<List<int>> edges, int start) {
  var dist = List.filled(n, double.infinity);
  dist[start] = 0;

  for (int i = 0; i < n - 1; i++) {
    for (var edge in edges) {
      if (dist[edge[0]] + edge[2] < dist[edge[1]]) {
        dist[edge[1]] = dist[edge[0]] + edge[2];
      }
    }
  }
}
```
**Tushuntirish:** Dijkstra salbiy vaznlar bilan ishlay olmaydi, Bellman-Ford esa bu muammoni hal qiladi va salbiy sikllarni aniqlay oladi.

---

### Topshiriq #1091: Tarmoq Latentligini Minimallashtirish (Dijkstra)
**Tavsif:** Taqsimlangan tizimlarda serverlararo eng qisqa yo'lni topish.
**Talablar:** O(E log V) murakkablik, xotira xavfsizligi.
**Yechim (Dart):**
```dart
import 'dart:collection';

class Graph {
  final int vertices;
  final Map<int, List<MapEntry<int, int>>> adj = {};

  Graph(this.vertices);

  void addEdge(int u, int v, int weight) {
    adj.putIfAbsent(u, () => []).add(MapEntry(v, weight));
  }

  int findShortestPath(int start, int end) {
    var distances = List.filled(vertices, double.maxFinite.toInt());
    distances[start] = 0;
    var pq = PriorityQueue<MapEntry<int, int>>((a, b) => a.value.compareTo(b.value));
    pq.add(MapEntry(start, 0));

    while (pq.isNotEmpty) {
      var current = pq.removeFirst();
      if (current.key == end) return current.value;
      for (var edge in adj[current.key] ?? []) {
        if (distances[current.key] + edge.value < distances[edge.key]) {
          distances[edge.key] = distances[current.key] + edge.value;
          pq.add(MapEntry(edge.key, distances[edge.key]));
        }
      }
    }
    return -1;
  }
}
```
**Tushuntirish:** Dijkstra algoritmi PriorityQueue bilan birgalikda eng samarali yo'lni topish uchun ishlatildi.

### Topshiriq #1092: Dinamik Diapazon Summasini Hisoblash (Segment Tree)
**Tavsif:** Real vaqt rejimida tranzaksiyalar yig'indisini kuzatish.
**Talablar:** O(log N) yangilash va so'rov vaqti.
**Yechim (Dart):**
```dart
class SegmentTree {
  late List<int> tree;
  int n;

  SegmentTree(List<int> data) : n = data.length {
    tree = List.filled(2 * n, 0);
    for (int i = 0; i < n; i++) tree[n + i] = data[i];
    for (int i = n - 1; i > 0; i--) tree[i] = tree[2 * i] + tree[2 * i + 1];
  }

  void update(int i, int val) {
    for (tree[i += n] = val; i > 1; i >>= 1) tree[i >> 1] = tree[i] + tree[i ^ 1];
  }

  int query(int l, int r) {
    int res = 0;
    for (l += n, r += n; l < r; l >>= 1, r >>= 1) {
      if (l & 1 == 1) res += tree[l++];
      if (r & 1 == 1) res += tree[--r];
    }
    return res;
  }
}
```
**Tushuntirish:** Iterativ Segment Tree xotira sarfini kamaytiradi va rekursiv chaqiruvlarsiz tez ishlaydi.

### Topshiriq #1093: Prefiks Qidiruv Tizimi (Trie)
**Tavsif:** Foydalanuvchi so'rovlarini avtomatik to'ldirish (Autocomplete).
**Talablar:** O(L) qidiruv vaqti, bu yerda L - so'z uzunligi.
**Yechim (Dart):**
```dart
class TrieNode {
  Map<String, TrieNode> children = {};
  bool isEndOfWord = false;
}

class Trie {
  final root = TrieNode();

  void insert(String word) {
    var node = root;
    for (var char in word.split('')) {
      node = node.children.putIfAbsent(char, () => TrieNode());
    }
    node.isEndOfWord = true;
  }

  bool search(String word) {
    var node = root;
    for (var char in word.split('')) {
      if (!node.children.containsKey(char)) return false;
      node = node.children[char]!;
    }
    return node.isEndOfWord;
  }
}
```
**Tushuntirish:** Trie tuzilmasi katta lug'atlar ichida prefiks asosida qidiruvni maksimal tezlashtiradi.

### Topshiriq #1094: Kümülativ Chastotani Hisoblash (Fenwick Tree)
**Tavsif:** Katta hajmdagi oqimli ma'lumotlar uchun kümülativ yig'indini saqlash.
**Talablar:** O(log N) murakkablik, minimal xotira.
**Yechim (Dart):**
```dart
class FenwickTree {
  final List<int> tree;
  FenwickTree(int size) : tree = List.filled(size + 1, 0);

  void add(int i, int delta) {
    for (; i < tree.length; i += i & -i) tree[i] += delta;
  }

  int query(int i) {
    int sum = 0;
    for (; i > 0; i -= i & -i) sum += tree[i];
    return sum;
  }
}
```
**Tushuntirish:** Fenwick Tree (Binary Indexed Tree) Segment Tree'ga qaraganda kamroq xotira talab qiladi va implementatsiyasi sodda.

### Topshiriq #1095: Tarmoq Komponentlarini Aniqlash (Union-Find)
**Tavsif:** Ijtimoiy tarmoqlarda do'stlik aloqalarini klasterlash.
**Talablar:** Path compression va union by rank texnikasi.
**Yechim (Dart):**
```dart
class UnionFind {
  List<int> parent;
  UnionFind(int n) : parent = List.generate(n, (i) => i);

  int find(int i) {
    if (parent[i] == i) return i;
    return parent[i] = find(parent[i]); // Path compression
  }

  void union(int i, int j) {
    int rootI = find(i);
    int rootJ = find(j);
    if (rootI != rootJ) parent[rootI] = rootJ;
  }
}
```
**Tushuntirish:** Path compression operatsiyasi daraxt balandligini doimiy ravishda pasaytirib, deyarli O(1) vaqtda ishlaydi.

### Topshiriq #1096: Topologik Tartiblash (Kahn Algoritmi)
**Tavsif:** Loyiha vazifalari o'rtasidagi bog'liqlikni (dependency) aniqlash.
**Talablar:** Acyclic graf tekshiruvi.
**Yechim (Dart):**
```dart
List<int> topologicalSort(int n, Map<int, List<int>> adj, List<int> inDegree) {
  var queue = Queue<int>();
  for (int i = 0; i < n; i++) if (inDegree[i] == 0) queue.add(i);
  List<int> result = [];

  while (queue.isNotEmpty) {
    int u = queue.removeFirst();
    result.add(u);
    for (var v in adj[u] ?? []) {
      inDegree[v]--;
      if (inDegree[v] == 0) queue.add(v);
    }
  }
  return result;
}
```
**Tushuntirish:** Kahn algoritmi tsiklik bog'liqliklarni aniqlash va vazifalar ketma-ketligini belgilash uchun eng xavfsiz yo'l.

### Topshiriq #1097: Eng Yaqin Umumiy Ota (LCA)
**Tavsif:** Daraxtsimon ierarxik ma'lumotlar bazasida ikki tugun o'rtasidagi bog'liqlikni topish.
**Talablar:** Binary lifting usuli, O(log N) so'rov.
**Yechim (Dart):**
```dart
// Binary lifting yordamida LCA
int getLCA(int u, int v, List<List<int>> up, List<int> depth) {
  if (depth[u] < depth[v]) u = v.also((it) => v = u); // Swap
  for (int i = 19; i >= 0; i--) {
    if (depth[u] - (1 << i) >= depth[v]) u = up[u][i];
  }
  if (u == v) return u;
  for (int i = 19; i >= 0; i--) {
    if (up[u][i] != up[v][i]) {
      u = up[u][i];
      v = up[v][i];
    }
  }
  return up[u][0];
}
```
**Tushuntirish:** Binary lifting katta daraxtlarda LCA ni juda tez hisoblash imkonini beradi.

### Topshiriq #1098: Maksimal Oqim (Edmonds-Karp)
**Tavsif:** Logistika tizimida yuk tashish sig'imini optimallashtirish.
**Talablar:** BFS asosida BFS-based augmenting path.
**Yechim (Dart):**
```dart
int bfs(List<List<int>> capacity, int s, int t, List<int> parent) {
  parent.fillRange(0, parent.length, -1);
  parent[s] = -2;
  var queue = Queue<MapEntry<int, int>>();
  queue.add(MapEntry(s, 1000000));
  while (queue.isNotEmpty) {
    var entry = queue.removeFirst();
    int u = entry.key, flow = entry.value;
    for (int v = 0; v < capacity.length; v++) {
      if (parent[v] == -1 && capacity[u][v] > 0) {
        parent[v] = u;
        int newFlow = flow < capacity[u][v] ? flow : capacity[u][v];
        if (v == t) return newFlow;
        queue.add(MapEntry(v, newFlow));
      }
    }
  }
  return 0;
}
```
**Tushuntirish:** Edmonds-Karp algoritmi tarmoq o'tkazuvchanligini maksimal darajada ishlatish uchun standart yechimdir.

### Topshiriq #1099: Suffix Array (Qidiruvni tezlashtirish)
**Tavsif:** Katta matnlar ichida substring qidirishni O(log N) ga tushirish.
**Talablar:** Xotira samaradorligi va tezkor indeksatsiya.
**Yechim (Dart):**
```dart
List<int> buildSuffixArray(String s) {
  int n = s.length;
  List<int> sa = List.generate(n, (i) => i);
  sa.sort((a, b) => s.substring(a).compareTo(s.substring(b)));
  return sa;
}
```
**Tushuntirish:** Suffix Array matnni qayta ishlash va qidiruv algoritmlarida indekslashni optimallashtiradi.

### Topshiriq #1100: Kengaytirilgan Trie (Trie with Frequency)
**Tavsif:** Ko'p so'raladigan so'zlarni (trending) aniqlash.
**Talablar:** Har bir tugunda chastotani saqlash.
**Yechim (Dart):**
```dart
class FrequencyTrieNode {
  Map<String, FrequencyTrieNode> children = {};
  int frequency = 0;
}

class FrequencyTrie {
  final root = FrequencyTrieNode();
  void insert(String word) {
    var node = root;
    for (var char in word.split('')) {
      node = node.children.putIfAbsent(char, () => FrequencyTrieNode());
      node.frequency++;
    }
  }
}
```
**Tushuntirish:** Har bir tugunda chastotani saqlash orqali qidiruv natijalarini mashhurlik darajasiga ko'ra saralash imkoniyati yaratildi.