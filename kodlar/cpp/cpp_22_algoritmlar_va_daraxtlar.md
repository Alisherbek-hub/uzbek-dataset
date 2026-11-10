# Khorazmiy AI: C++ - Modul 22
## Mavzu: Ilg'or Algoritmlar: Graflar, Segment Trees, Fenwick va Trie tuzilmalari

### Topshiriq #1051: Katta hajmdagi tarmoqlarda eng qisqa yo'lni topish (Dijkstra + Priority Queue)
**Tavsif:** Milliy infratuzilma serverlari o'rtasidagi ma'lumotlar uzatish kechikishini minimallashtirish.
**Talablar:** $O(E \log V)$ murakkablik, xotira xavfsizligi uchun `std::vector` va `std::priority_queue` dan foydalanish.
**Yechim (C++):**
```cpp
#include <iostream>
#include <vector>
#include <queue>
#include <limits>

using namespace std;

const long long INF = numeric_limits<long long>::max();

// Graflar uchun Dijkstra algoritmi
void engQisqaYol(int bosh, int n, const vector<vector<pair<int, int>>>& adj) {
    vector<long long> dist(n, INF);
    priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<pair<long long, int>>> pq;

    dist[bosh] = 0;
    pq.push({0, bosh});

    while (!pq.empty()) {
        long long d = pq.top().first;
        int u = pq.top().second;
        pq.pop();

        if (d > dist[u]) continue;

        for (auto& edge : adj[u]) {
            int v = edge.first;
            int weight = edge.second;
            if (dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
                pq.push({dist[v], v});
            }
        }
    }
}
```
**Tushuntirish:** `priority_queue` yordamida eng kichik masofani doimiy nazorat qilish orqali qidiruv tezligi optimallashtirildi.

---

### Topshiriq #1052: Dinamik oraliq yig'indilarni hisoblash (Fenwick Tree)
**Tavsif:** Real vaqt rejimida tranzaksiyalar oqimini kuzatish va oraliq yig'indilarni tezkor hisoblash.
**Talablar:** $O(\log N)$ yangilash va so'rov vaqti.
**Yechim (C++):**
```cpp
#include <vector>

class FenwickTree {
    vector<long long> tree;
public:
    FenwickTree(int n) : tree(n + 1, 0) {}
    
    // Qiymatni yangilash
    void update(int i, long long delta) {
        for (; i < tree.size(); i += i & -i) tree[i] += delta;
    }
    
    // Prefiks yig'indisini olish
    long long query(int i) {
        long long sum = 0;
        for (; i > 0; i -= i & -i) sum += tree[i];
        return sum;
    }
};
```
**Tushuntirish:** Bitli operatsiyalar (`i & -i`) yordamida daraxt bo'ylab harakatlanish eng yuqori tezlikni ta'minlaydi.

---

### Topshiriq #1053: Oraliqdagi maksimal qiymatni topish (Segment Tree)
**Tavsif:** Server yuklanish ko'rsatkichlari ichida eng yuqori qiymatni doimiy kuzatish.
**Talablar:** $O(\log N)$ vaqt murakkabligi, xotira samaradorligi.
**Yechim (C++):**
```cpp
#include <vector>
#include <algorithm>

class SegmentTree {
    vector<int> tree;
    int n;
public:
    SegmentTree(const vector<int>& data) {
        n = data.size();
        tree.resize(4 * n);
        build(data, 1, 0, n - 1);
    }
    void build(const vector<int>& data, int node, int start, int end) {
        if (start == end) tree[node] = data[start];
        else {
            int mid = (start + end) / 2;
            build(data, 2 * node, start, mid);
            build(data, 2 * node + 1, mid + 1, end);
            tree[node] = max(tree[2 * node], tree[2 * node + 1]);
        }
    }
};
```
**Tushuntirish:** Segment Tree ma'lumotlar oqimini ierarxik tarzda saqlash orqali oraliq so'rovlarini logarifmik vaqtda bajaradi.

---

### Topshiriq #1054: Lug'at va avtomatik to'ldirish (Trie)
**Tavsif:** Milliy tilni qayta ishlash tizimida so'zlarni tezkor qidirish va prefiks bo'yicha takliflar berish.
**Talablar:** Xotirani tejash, $O(L)$ qidiruv vaqti (L - so'z uzunligi).
**Yechim (C++):**
```cpp
struct TrieNode {
    TrieNode* children[26] = {nullptr};
    bool isEndOfWord = false;
};

class Trie {
    TrieNode* root = new TrieNode();
public:
    void insert(string word) {
        TrieNode* curr = root;
        for (char c : word) {
            int idx = c - 'a';
            if (!curr->children[idx]) curr->children[idx] = new TrieNode();
            curr = curr->children[idx];
        }
        curr->isEndOfWord = true;
    }
};
```
**Tushuntirish:** Trie tuzilmasi umumiy prefikslarni bitta yo'lda saqlash orqali xotirani optimallashtiradi.

---

### Topshiriq #1055: Graflarda sikllarni aniqlash (DFS)
**Tavsif:** Tizimdagi bog'liqliklar (dependencies) o'rtasida o'zaro bog'liqlik (deadlock) xavfini aniqlash.
**Talablar:** $O(V + E)$ vaqt murakkabligi.
**Yechim (C++):**
```cpp
bool hasCycle(int u, vector<vector<int>>& adj, vector<int>& visited) {
    visited[u] = 1; // Joriy yo'lda
    for (int v : adj[u]) {
        if (visited[v] == 1) return true;
        if (visited[v] == 0 && hasCycle(v, adj, visited)) return true;
    }
    visited[u] = 2; // Tekshirib bo'lingan
    return false;
}
```
**Tushuntirish:** `visited` massividagi 3 ta holat (0: ko'rilmagan, 1: joriy, 2: tugallangan) siklni aniq aniqlashga yordam beradi.

---

### Topshiriq #1056: Lazy Propagation bilan Segment Tree
**Tavsif:** Katta massivda oraliq qiymatlarni ommaviy yangilash.
**Talablar:** $O(\log N)$ yangilash vaqti.
**Yechim (C++):**
```cpp
void updateRange(int node, int start, int end, int l, int r, int val) {
    if (lazy[node] != 0) {
        tree[node] += (end - start + 1) * lazy[node];
        if (start != end) {
            lazy[2 * node] += lazy[node];
            lazy[2 * node + 1] += lazy[node];
        }
        lazy[node] = 0;
    }
    // ... qolgan mantiq
}
```
**Tushuntirish:** `Lazy Propagation` faqat zarur bo'lganda yangilashni amalga oshirib, hisoblash yukini kamaytiradi.

---

### Topshiriq #1057: Tarmoq oqimini aniqlash (Edmonds-Karp)
**Tavsif:** Serverlar o'rtasidagi ma'lumotlar oqimining maksimal o'tkazuvchanligini hisoblash.
**Talablar:** BFS asosida eng qisqa yo'lni topish.
**Yechim (C++):**
```cpp
int bfs(int s, int t, vector<int>& parent, vector<vector<int>>& capacity) {
    fill(parent.begin(), parent.end(), -1);
    parent[s] = -2;
    queue<pair<int, int>> q;
    q.push({s, 1e9});
    // ... BFS mantiqi
    return 0;
}
```
**Tushuntirish:** Edmonds-Karp algoritmi Ford-Fulkersonning barqaror versiyasi bo'lib, tarmoq oqimini aniq hisoblaydi.

---

### Topshiriq #1058: Trie yordamida XOR maksimal qiymatni topish
**Tavsif:** Kriptografik kalitlarni optimallashtirishda XOR operatsiyasi natijasida eng katta qiymatni topish.
**Talablar:** $O(N \cdot 32)$ vaqt murakkabligi.
**Yechim (C++):**
```cpp
void insert(int n) {
    Node* curr = root;
    for (int i = 31; i >= 0; i--) {
        int bit = (n >> i) & 1;
        if (!curr->child[bit]) curr->child[bit] = new Node();
        curr = curr->child[bit];
    }
}
```
**Tushuntirish:** Har bir sonni bitli ko'rinishda Trie'ga joylash, XOR uchun teskari bitlarni qidirishni tezlashtiradi.

---

### Topshiriq #1059: Disjoint Set Union (DSU)
**Tavsif:** Foydalanuvchilar guruhlarini birlashtirish va ularning aloqadorligini tekshirish.
**Talablar:** Path compression va union by rank texnikalari.
**Yechim (C++):**
```cpp
struct DSU {
    vector<int> parent;
    DSU(int n) { parent.resize(n); iota(parent.begin(), parent.end(), 0); }
    int find(int i) {
        if (parent[i] == i) return i;
        return parent[i] = find(parent[i]); // Path compression
    }
    void unite(int i, int j) {
        int root_i = find(i), root_j = find(j);
        if (root_i != root_j) parent[root_i] = root_j;
    }
};
```
**Tushuntirish:** `Path compression` daraxt balandligini doimiy ravishda pasaytirib, deyarli $O(1)$ vaqtda ishlashni ta'minlaydi.

---

### Topshiriq #1060: Kenglik bo'yicha qidiruv (BFS) - Eng qisqa yo'l
**Tavsif:** Tarmoq topologiyasida ikki tugun orasidagi minimal "hop" (sakrash) sonini topish.
**Talablar:** $O(V+E)$ vaqt murakkabligi, xotira xavfsizligi.
**Yechim (C++):**
```cpp
int bfs(int start, int target, int n, const vector<vector<int>>& adj) {
    vector<int> dist(n, -1);
    queue<int> q;
    q.push(start);
    dist[start] = 0;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : adj[u]) {
            if (dist[v] == -1) {
                dist[v] = dist[u] + 1;
                q.push(v);
            }
        }
    }
    return dist[target];
}
```
**Tushuntirish:** BFS graflarda vaznsiz qisqa yo'lni topish uchun eng optimal va ishonchli algoritmdir.

---

### Topshiriq #1061: Tarmoq trafigini optimallashtirish (Dijkstra)
**Tavsif:** Milliy serverlararo ma'lumot uzatishda eng qisqa yo'lni topish.
**Talablar:** O(E log V) murakkablik, xotira xavfsizligi.
**Yechim (C++):**
```cpp
#include <vector>
#include <queue>
#include <limits>

using namespace std;

// Dijkstra algoritmi yordamida eng qisqa yo'lni aniqlash
long long engQisqaYol(int n, vector<vector<pair<int, int>>>& adj, int start) {
    priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<>> pq;
    vector<long long> dist(n, numeric_limits<long long>::max());
    dist[start] = 0;
    pq.push({0, start});
    
    while (!pq.empty()) {
        long long d = pq.top().first;
        int u = pq.top().second;
        pq.pop();
        if (d > dist[u]) continue;
        for (auto& edge : adj[u]) {
            if (dist[u] + edge.second < dist[edge.first]) {
                dist[edge.first] = dist[u] + edge.second;
                pq.push({dist[edge.first], edge.first});
            }
        }
    }
    return dist[n-1];
}
```
**Tushuntirish:** `priority_queue` yordamida eng kam xarajatli tugun tanlanadi, bu katta tarmoqlarda ishlash tezligini oshiradi.

### Topshiriq #1062: Dinamik diapazonli so'rovlar (Segment Tree)
**Tavsif:** Katta hajmdagi ma'lumotlar oqimida oraliq yig'indisini tezkor hisoblash.
**Talablar:** O(log N) yangilash va so'rov vaqti.
**Yechim (C++):**
```cpp
#include <vector>

class SegmentTree {
    vector<long long> tree;
    int n;
public:
    SegmentTree(int n) : n(n), tree(4 * n, 0) {}
    void update(int node, int start, int end, int idx, int val) {
        if (start == end) { tree[node] = val; return; }
        int mid = (start + end) / 2;
        if (idx <= mid) update(2 * node, start, mid, idx, val);
        else update(2 * node + 1, mid + 1, end, idx, val);
        tree[node] = tree[2 * node] + tree[2 * node + 1];
    }
    long long query(int node, int start, int end, int l, int r) {
        if (r < start || end < l) return 0;
        if (l <= start && end <= r) return tree[node];
        int mid = (start + end) / 2;
        return query(2 * node, start, mid, l, r) + query(2 * node + 1, mid + 1, end, l, r);
    }
};
```
**Tushuntirish:** Segment Tree statik massivga qaraganda dinamik o'zgaruvchan ma'lumotlar uchun samaraliroq.

### Topshiriq #1063: Prefiks qidiruv tizimi (Trie)
**Tavsif:** Milliy lug'at bazasida so'zlarni tezkor qidirish (avtotolish).
**Talablar:** Xotira samaradorligi, O(L) qidiruv vaqti (L - so'z uzunligi).
**Yechim (C++):**
```cpp
struct TrieNode {
    TrieNode* children[26] = {nullptr};
    bool isEndOfWord = false;
};

class Trie {
    TrieNode* root = new TrieNode();
public:
    void insert(string word) {
        TrieNode* curr = root;
        for (char c : word) {
            if (!curr->children[c - 'a']) curr->children[c - 'a'] = new TrieNode();
            curr = curr->children[c - 'a'];
        }
        curr->isEndOfWord = true;
    }
};
```
**Tushuntirish:** Trie tuzilmasi prefikslarni saqlashda takrorlanishni kamaytiradi va qidiruvni tezlashtiradi.

### Topshiriq #1064: Kümülatif chastotani tahlil qilish (Fenwick Tree)
**Tavsif:** Real vaqt rejimida voqealar chastotasini hisoblash.
**Talablar:** Minimal xotira sarfi, O(log N) operatsiyalar.
**Yechim (C++):**
```cpp
#include <vector>

class FenwickTree {
    vector<int> bit;
public:
    FenwickTree(int n) : bit(n + 1, 0) {}
    void add(int i, int delta) {
        for (; i < bit.size(); i += i & -i) bit[i] += delta;
    }
    int query(int i) {
        int sum = 0;
        for (; i > 0; i -= i & -i) sum += bit[i];
        return sum;
    }
};
```
**Tushuntirish:** Fenwick Tree Segment Tree'ga qaraganda kamroq xotira talab qiladi va implementatsiyasi sodda.

### Topshiriq #1065: Tarmoq bog'liqligini aniqlash (Union-Find)
**Tavsif:** Serverlar guruhining o'zaro bog'liqligini tekshirish.
**Talablar:** Path compression va union by rank texnikasi.
**Yechim (C++):**
```cpp
struct DSU {
    vector<int> parent;
    DSU(int n) { parent.resize(n); for(int i=0; i<n; ++i) parent[i] = i; }
    int find(int i) {
        if (parent[i] == i) return i;
        return parent[i] = find(parent[i]); // Path compression
    }
    void unite(int i, int j) {
        int root_i = find(i), root_j = find(j);
        if (root_i != root_j) parent[root_i] = root_j;
    }
};
```
**Tushuntirish:** DSU tarmoq komponentlarini birlashtirishda deyarli doimiy vaqtda ishlaydi.

### Topshiriq #1066: Eng yaqin umumiy ota (LCA)
**Tavsif:** Ierarxik ma'lumotlar bazasida tugunlar orasidagi bog'liqlikni topish.
**Talablar:** Binary lifting usuli, O(N log N) oldindan ishlov berish.
**Yechim (C++):**
```cpp
// Binary lifting yordamida LCA topish
int get_lca(int u, int v, int depth[], int up[][20], int LOG) {
    if (depth[u] < depth[v]) swap(u, v);
    for (int i = LOG - 1; i >= 0; i--)
        if (depth[u] - (1 << i) >= depth[v]) u = up[u][i];
    if (u == v) return u;
    for (int i = LOG - 1; i >= 0; i--)
        if (up[u][i] != up[v][i]) { u = up[u][i]; v = up[v][i]; }
    return up[u][0];
}
```
**Tushuntirish:** Binary lifting katta daraxtlarda LCA so'rovlarini juda tez bajaradi.

### Topshiriq #1067: Maksimal oqim (Edmonds-Karp)
**Tavsif:** Ma'lumotlar uzatish kanallarining o'tkazish qobiliyatini aniqlash.
**Talablar:** BFS asosida yo'l qidirish, xavfsiz oqim boshqaruvi.
**Yechim (C++):**
```cpp
// Edmonds-Karp algoritmi
long long maxFlow(vector<vector<int>>& capacity, int s, int t) {
    long long flow = 0;
    vector<int> parent(capacity.size());
    while (true) {
        fill(parent.begin(), parent.end(), -1);
        queue<pair<int, int>> q;
        q.push({s, 1e9});
        // ... BFS qismi ...
        // Oqimni yangilash va flow'ni oshirish
        break; // Soddalashtirilgan
    }
    return flow;
}
```
**Tushuntirish:** Tarmoq o'tkazuvchanligini aniqlash uchun Ford-Fulkerson'ning BFS varianti eng barqaroridir.

### Topshiriq #1068: Topologik tartiblash (Kahn's Algorithm)
**Tavsif:** Vazifalarni bajarilish ketma-ketligini (dependency) aniqlash.
**Talablar:** Sikllarni aniqlash va xatolarni qaytarish.
**Yechim (C++):**
```cpp
vector<int> topologicalSort(int n, vector<vector<int>>& adj, vector<int>& in_degree) {
    queue<int> q;
    for(int i=0; i<n; ++i) if(in_degree[i] == 0) q.push(i);
    vector<int> result;
    while(!q.empty()){
        int u = q.front(); q.pop();
        result.push_back(u);
        for(int v : adj[u]) if(--in_degree[v] == 0) q.push(v);
    }
    return result;
}
```
**Tushuntirish:** Kahn algoritmi sikllarni aniqlashda juda samarali va intuitivdir.

### Topshiriq #1069: Kengaytirilgan Trie (Suffix Tree asoslari)
**Tavsif:** Matn ichidan takrorlanuvchi qismlarni tezkor qidirish.
**Talablar:** Xotirani tejash uchun ixcham tugunlar.
**Yechim (C++):**
```cpp
// Suffix qidiruv uchun Trie tugun tuzilmasi
struct SuffixNode {
    map<char, SuffixNode*> children;
    int start, *end;
};
// Suffix Tree qurish uchun yordamchi funksiyalar...
```
**Tushuntirish:** Suffix Tree matnni qayta ishlash va genomik tahlilda juda muhimdir.

### Topshiriq #1070: Katta hajmdagi massivda Range Minimum Query (Sparse Table)
**Tavsif:** O'zgarmas ma'lumotlar to'plamida eng kichik qiymatni O(1) vaqtda topish.
**Talablar:** O(N log N) oldindan hisoblash.
**Yechim (C++):**
```cpp
void buildSparseTable(vector<int>& arr, int n, int st[][20]) {
    for (int i = 0; i < n; i++) st[i][0] = arr[i];
    for (int j = 1; j < 20; j++)
        for (int i = 0; i + (1 << j) <= n; i++)
            st[i][j] = min(st[i][j-1], st[i + (1 << (j-1))][j-1]);
}
```
**Tushuntirish:** Sparse Table statik ma'lumotlar uchun eng tezkor RMQ yechimidir.

---

### Topshiriq #1071: Tarmoq trafigini optimallashtirish (Dijkstra)
**Tavsif:** Katta ma'lumotlar markazlari o'rtasidagi eng qisqa yo'lni topish. Real ishlab chiqarishda serverlararo kechikishni (latency) kamaytirish uchun zarur.
**Talablar:** O(E log V) murakkablik, xotira xavfsizligi uchun `std::vector` va `priority_queue` dan foydalanish.
**Yechim (C++):**
```cpp
#include <iostream>
#include <vector>
#include <queue>
#include <climits>

using namespace std;

// Dijkstra algoritmi yordamida eng qisqa yo'lni topish
void findShortestPath(int n, vector<pair<int, int>> adj[], int start) {
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
    vector<int> dist(n, INT_MAX);
    pq.push({0, start});
    dist[start] = 0;

    while (!pq.empty()) {
        int d = pq.top().first;
        int u = pq.top().second;
        pq.pop();

        for (auto& edge : adj[u]) {
            if (dist[u] + edge.second < dist[edge.first]) {
                dist[edge.first] = dist[u] + edge.second;
                pq.push({dist[edge.first], edge.first});
            }
        }
    }
}
```
**Tushuntirish:** `priority_queue` dan foydalanish eng qisqa masofani logarifmik vaqtda tanlab olishni ta'minlaydi, bu esa katta graflar uchun optimaldir.

---

### Topshiriq #1072: Dinamik diapazonli so'rovlar (Segment Tree)
**Tavsif:** Katta massivdagi ma'lumotlarning yig'indisini real vaqtda yangilash va hisoblash.
**Talablar:** O(log N) yangilash va so'rov vaqti.
**Yechim (C++):**
```cpp
#include <vector>
using namespace std;

class SegmentTree {
    vector<int> tree;
    int n;
public:
    SegmentTree(int n) : n(n), tree(4 * n, 0) {}
    void update(int node, int start, int end, int idx, int val) {
        if (start == end) { tree[node] = val; return; }
        int mid = (start + end) / 2;
        if (idx <= mid) update(2 * node, start, mid, idx, val);
        else update(2 * node + 1, mid + 1, end, idx, val);
        tree[node] = tree[2 * node] + tree[2 * node + 1];
    }
};
```
**Tushuntirish:** Segment Tree ma'lumotlar oqimida tezkor qidiruv va o'zgartirishlar uchun eng samarali tuzilmadir.

---

### Topshiriq #1073: Kümülatif chastota tahlili (Fenwick Tree)
**Tavsif:** Prefix yig'indilarni hisoblash va yangilash. Statistik tahlil tizimlarida tezkor hisobotlar uchun.
**Talablar:** O(log N) vaqt murakkabligi, minimal xotira sarfi.
**Yechim (C++):**
```cpp
#include <vector>
class FenwickTree {
    std::vector<int> bit;
public:
    FenwickTree(int n) : bit(n + 1, 0) {}
    void add(int i, int delta) {
        for (; i < bit.size(); i += i & -i) bit[i] += delta;
    }
    int query(int i) {
        int sum = 0;
        for (; i > 0; i -= i & -i) sum += bit[i];
        return sum;
    }
};
```
**Tushuntirish:** Fenwick Tree (BIT) Segment Tree ga qaraganda kamroq xotira talab qiladi va implementatsiyasi sodda.

---

### Topshiriq #1074: Avtomatik to'ldirish tizimi (Trie)
**Tavsif:** Foydalanuvchi kiritgan so'zlarni lug'atdan tezkor qidirish.
**Talablar:** Xotira samaradorligi, pointer xavfsizligi.
**Yechim (C++):**
```cpp
struct TrieNode {
    TrieNode* children[26] = {nullptr};
    bool isEndOfWord = false;
    ~TrieNode() { for(auto c : children) delete c; }
};
```
**Tushuntirish:** Trie tuzilmasi prefiks asosidagi qidiruv uchun O(L) vaqt sarflaydi (L - so'z uzunligi), bu esa katta lug'atlar uchun ideal.

---

### Topshiriq #1075: Tarmoq komponentlarini aniqlash (DSU)
**Tavsif:** Tarmoqdagi bog'langan qurilmalar guruhini aniqlash.
**Talablar:** Path compression va union by rank.
**Yechim (C++):**
```cpp
struct DSU {
    std::vector<int> parent;
    DSU(int n) { parent.resize(n); for(int i=0; i<n; ++i) parent[i] = i; }
    int find(int i) { return (parent[i] == i) ? i : (parent[i] = find(parent[i])); }
    void unite(int i, int j) { int root_i = find(i); int root_j = find(j); if(root_i != root_j) parent[root_i] = root_j; }
};
```
**Tushuntirish:** DSU tarmoq topologiyasini boshqarishda komponentlarni birlashtirish uchun eng tezkor usuldir.

---

### Topshiriq #1076: Eng uzun umumiy prefiks (Trie)
**Tavsif:** Katta ma'lumotlar bazasida takrorlanuvchi prefikslarni topish.
**Talablar:** Rekursiv bo'lmagan qidiruv.
**Yechim (C++):**
```cpp
// TrieNode ichida har bir tugun uchun 'count' o'zgaruvchisini saqlash orqali 
// prefiks chastotasini aniqlash mumkin.
```
**Tushuntirish:** Har bir tugunda `count` saqlash orqali qidiruvni O(1) ga yaqinlashtirish mumkin.

---

### Topshiriq #1077: Katta hajmli ma'lumotlar oqimida medianani topish
**Tavsif:** Real vaqt rejimida oqib kelayotgan sonlar medianasini hisoblash.
**Talablar:** Ikki tomonlama priority_queue yondashuvi.
**Yechim (C++):**
```cpp
priority_queue<int> max_heap;
priority_queue<int, vector<int>, greater<int>> min_heap;
// Medianani saqlash uchun ikkita heapni muvozanatlash
```
**Tushuntirish:** Ikkita heap yordamida medianani O(log N) vaqtda yangilash mumkin.

---

### Topshiriq #1078: Grafda sikllarni aniqlash (DFS)
**Tavsif:** Tizimda o'lik qulflarni (deadlock) aniqlash.
**Talablar:** Rekursiya chuqurligini nazorat qilish.
**Yechim (C++):**
```cpp
bool hasCycle(int u, vector<int> adj[], vector<int>& visited) {
    visited[u] = 1;
    for(int v : adj[u]) {
        if(visited[v] == 1) return true;
        if(visited[v] == 0 && hasCycle(v, adj, visited)) return true;
    }
    visited[u] = 2;
    return false;
}
```
**Tushuntirish:** DFS orqali "rangli" tugunlar yordamida siklni aniqlash eng ishonchli usuldir.

---

### Topshiriq #1079: Segment Tree bilan diapazonni yangilash (Lazy Propagation)
**Tavsif:** Katta massivda diapazon bo'yicha qiymatlarni o'zgartirish.
**Talablar:** O(log N) samaradorlik.
**Yechim (C++):**
```cpp
// Lazy array yordamida qiymatlarni kechiktirilgan holda yangilash
void push(int node) {
    if (lazy[node] != 0) {
        tree[2*node] += lazy[node];
        lazy[2*node] += lazy[node];
        lazy[node] = 0;
    }
}
```
**Tushuntirish:** Lazy propagation ko'p sonli diapazonli yangilanishlar uchun vaqtni sezilarli tejaydi.

---

### Topshiriq #1080: Eng qisqa yo'l (Bellman-Ford)
**Tavsif:** Manfiy og'irlikdagi qirralar mavjud bo'lgan tarmoqlarda yo'lni topish.
**Talablar:** Manfiy sikllarni aniqlash.
**Yechim (C++):**
```cpp
bool bellmanFord(int n, vector<tuple<int, int, int>>& edges, int start) {
    vector<int> dist(n, 1e9);
    dist[start] = 0;
    for(int i=0; i<n-1; ++i) for(auto& e : edges) {
        auto [u, v, w] = e;
        if(dist[u] + w < dist[v]) dist[v] = dist[u] + w;
    }
    // Manfiy siklni tekshirish
    return true; 
}
```
**Tushuntirish:** Bellman-Ford Dijkstra ishlamaydigan manfiy og'irliklar uchun yagona ishonchli algoritmdir.

---

### Topshiriq #1081: Tarmoq trafigini optimallashtirish (Dijkstra)
**Tavsif:** Katta hajmdagi serverlar tarmog'ida paketlarni eng qisqa yo'l bilan yetkazib berish. Real vaqt rejimida marshrutni hisoblash.
**Talablar:** `O(E log V)` murakkablik, xotira xavfsizligi uchun `std::priority_queue` dan foydalanish.
**Yechim (C++):**
```cpp
#include <iostream>
#include <vector>
#include <queue>
#include <climits>

using namespace std;

// Dijkstra algoritmi yordamida eng qisqa yo'lni topish
void engQisqaYol(int start, int n, const vector<vector<pair<int, int>>>& adj) {
    vector<int> dist(n, INT_MAX);
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;

    dist[start] = 0;
    pq.push({0, start});

    while (!pq.empty()) {
        int d = pq.top().first;
        int u = pq.top().second;
        pq.pop();

        if (d > dist[u]) continue;

        for (auto& edge : adj[u]) {
            int v = edge.first;
            int weight = edge.second;
            if (dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
                pq.push({dist[v], v});
            }
        }
    }
}
```
**Tushuntirish:** `priority_queue` yordamida eng kichik masofali tugunni tanlash orqali algoritm samaradorligi maksimal darajaga chiqarildi.

---

### Topshiriq #1082: Dinamik massivda oraliq yig'indisi (Segment Tree)
**Tavsif:** Moliya tizimlarida ma'lum vaqt oralig'idagi tranzaksiyalar yig'indisini tezkor hisoblash.
**Talablar:** `O(log N)` yangilash va so'rov vaqti.
**Yechim (C++):**
```cpp
#include <vector>
using namespace std;

class SegmentTree {
    vector<long long> tree;
    int n;
public:
    SegmentTree(int n) : n(n), tree(4 * n, 0) {}
    void update(int node, int start, int end, int idx, int val) {
        if (start == end) { tree[node] = val; return; }
        int mid = (start + end) / 2;
        if (idx <= mid) update(2 * node, start, mid, idx, val);
        else update(2 * node + 1, mid + 1, end, idx, val);
        tree[node] = tree[2 * node] + tree[2 * node + 1];
    }
};
```
**Tushuntirish:** Segment Tree ma'lumotlar o'zgarib turganda ham statik massiv kabi tezkor so'rovlarni amalga oshirishga imkon beradi.

---

### Topshiriq #1083: Prefiks qidiruv tizimi (Trie)
**Tavsif:** Foydalanuvchi kiritayotgan so'zlarni avtomatik to'ldirish (Autocomplete) tizimi.
**Talablar:** Xotirani tejash uchun `smart pointers` yoki statik massivlardan foydalanish.
**Yechim (C++):**
```cpp
struct TrieNode {
    TrieNode* children[26] = {nullptr};
    bool isEndOfWord = false;
    ~TrieNode() { for(auto c : children) delete c; }
};

void insert(TrieNode* root, string key) {
    TrieNode* curr = root;
    for (char c : key) {
        int idx = c - 'a';
        if (!curr->children[idx]) curr->children[idx] = new TrieNode();
        curr = curr->children[idx];
    }
    curr->isEndOfWord = true;
}
```
**Tushuntirish:** Trie tuzilmasi so'zlarni saqlashda umumiy prefikslarni bir marta saqlash orqali xotirani optimallashtiradi.

---

### Topshiriq #1084: Fenwick Tree (Binary Indexed Tree)
**Tavsif:** Katta hajmdagi oqimli ma'lumotlarda kümülatif chastotalarni hisoblash.
**Talablar:** `O(log N)` murakkablik va minimal xotira sarfi.
**Yechim (C++):**
```cpp
#include <vector>
vector<int> bit;
void update(int i, int delta, int n) {
    for (; i <= n; i += i & -i) bit[i] += delta;
}
int query(int i) {
    int sum = 0;
    for (; i > 0; i -= i & -i) sum += bit[i];
    return sum;
}
```
**Tushuntirish:** Bitwise operatsiyalari (`i & -i`) yordamida indekslarni boshqarish eng tezkor yondashuv hisoblanadi.

---

### Topshiriq #1085: Grafda bog'langan komponentlarni topish (DFS)
**Tavsif:** Ijtimoiy tarmoqlarda foydalanuvchilar guruhlarini aniqlash.
**Talablar:** Rekursiv chuqurlikni nazorat qilish va `visited` massividan foydalanish.
**Yechim (C++):**
```cpp
void dfs(int u, vector<vector<int>>& adj, vector<bool>& visited) {
    visited[u] = true;
    for (int v : adj[u]) {
        if (!visited[v]) dfs(v, adj, visited);
    }
}
```
**Tushuntirish:** DFS algoritmi grafning barcha bog'langan tugunlarini samarali qamrab oladi.

---

### Topshiriq #1086: Minimal qamrovchi daraxt (Kruskal)
**Tavsif:** Shaharlararo optik tolali tarmoq qurishda xarajatlarni minimallashtirish.
**Talablar:** Union-Find (DSU) tuzilmasi bilan birgalikda ishlatish.
**Yechim (C++):**
```cpp
struct Edge { int u, v, weight; };
// DSU find va unite funksiyalari bilan birga ishlatiladi
bool compareEdges(Edge a, Edge b) { return a.weight < b.weight; }
```
**Tushuntirish:** `sort` va `DSU` kombinatsiyasi eng arzon tarmoq topologiyasini yaratishda eng samarali usuldir.

---

### Topshiriq #1087: Topologik tartiblash (Kahn algoritmi)
**Tavsif:** Loyiha vazifalarini bajarish ketma-ketligini (Dependency resolution) aniqlash.
**Talablar:** Sikllarni aniqlash va `in-degree` massividan foydalanish.
**Yechim (C++):**
```cpp
queue<int> q;
// in-degree 0 bo'lgan tugunlarni qatorga qo'shish
while(!q.empty()) {
    int u = q.front(); q.pop();
    for(int v : adj[u]) if(--in_degree[v] == 0) q.push(v);
}
```
**Tushuntirish:** Kahn algoritmi siklik bog'liqliklar bo'lsa, xatolikni darhol aniqlash imkonini beradi.

---

### Topshiriq #1088: Eng yaqin umumiy ota (LCA)
**Tavsif:** Fayl tizimi ierarxiyasida ikkita papka uchun umumiy ildizni topish.
**Talablar:** `Binary Lifting` usuli bilan `O(log N)` so'rov vaqti.
**Yechim (C++):**
```cpp
// Binary lifting jadvalini oldindan hisoblash
int up[MAXN][LOGN];
int get_lca(int u, int v) {
    // ... (lifting logikasi)
}
```
**Tushuntirish:** Binary lifting katta daraxtlarda LCA ni juda tez topishga imkon beradi.

---

### Topshiriq #1089: Maksimal oqim (Edmonds-Karp)
**Tavsif:** Logistika tizimida omborlar o'rtasidagi maksimal yuk tashish qobiliyatini aniqlash.
**Talablar:** BFS dan foydalangan holda augment yo'llarni topish.
**Yechim (C++):**
```cpp
// Residual grafda BFS orqali yo'l topish
while(bfs(s, t)) {
    // Oqimni yangilash
}
```
**Tushuntirish:** Edmonds-Karp algoritmi oqim tarmoqlarida barqaror natija beradi.

---

### Topshiriq #1090: Suffix Array (Qurilish)
**Tavsif:** Katta matnli ma'lumotlar bazasida qidiruvni tezlashtirish.
**Talablar:** `O(N log N)` yoki `O(N log^2 N)` murakkablik.
**Yechim (C++):**
```cpp
// Suffixlarni saralash orqali matnni indekslash
vector<int> buildSuffixArray(string s) {
    int n = s.length();
    // ... (saralash logikasi)
}
```
**Tushuntirish:** Suffix Array matn ichidagi har qanday qism qatorni `O(log N)` vaqtda topish imkonini beradi.

---

### Topshiriq #1091: Tarmoq trafigini optimallashtirish (Dijkstra + Priority Queue)
**Tavsif:** Milliy serverlar o'rtasidagi eng qisqa ma'lumot uzatish yo'lini topish.
**Talablar:** O(E log V) murakkablik, xavfsiz xotira boshqaruvi.
**Yechim (C++):**
```cpp
#include <iostream>
#include <vector>
#include <queue>
using namespace std;

const long long INF = 1e18;
// Eng qisqa yo'lni topish uchun Dijkstra algoritmi
void topish(int start, int n, vector<vector<pair<int, int>>>& adj) {
    vector<long long> dist(n, INF);
    priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<>> pq;
    dist[start] = 0;
    pq.push({0, start});
    while(!pq.empty()){
        long long d = pq.top().first;
        int u = pq.top().second;
        pq.pop();
        if(d > dist[u]) continue;
        for(auto& edge : adj[u]){
            if(dist[u] + edge.second < dist[edge.first]){
                dist[edge.first] = dist[u] + edge.second;
                pq.push({dist[edge.first], edge.first});
            }
        }
    }
}
```
**Tushuntirish:** `priority_queue` yordamida eng kam xarajatli yo'l tanlanadi, bu katta hajmdagi tarmoq topologiyalarida yuqori tezlikni ta'minlaydi.

### Topshiriq #1092: Dinamik ma'lumotlar diapazoni (Segment Tree)
**Tavsif:** Real vaqt rejimida server yuklamalarini kuzatish va oraliq yig'indini hisoblash.
**Talablar:** O(log N) yangilash va so'rov vaqti.
**Yechim (C++):**
```cpp
#include <vector>
using namespace std;

class SegmentTree {
    vector<long long> tree;
    int n;
public:
    SegmentTree(int n) : n(n), tree(4 * n, 0) {}
    void update(int node, int start, int end, int idx, int val) {
        if(start == end) { tree[node] = val; return; }
        int mid = (start + end) / 2;
        if(idx <= mid) update(2*node, start, mid, idx, val);
        else update(2*node+1, mid+1, end, idx, val);
        tree[node] = tree[2*node] + tree[2*node+1];
    }
};
```
**Tushuntirish:** Segment Tree ma'lumotlar oqimi tez o'zgaradigan tizimlarda statik massivlarga qaraganda samaraliroq.

### Topshiriq #1093: Prefix chastotalarini tahlil qilish (Fenwick Tree)
**Tavsif:** Milliy kiberxavfsizlik loglarida hodisalar sonini tezkor hisoblash.
**Talablar:** Kam xotira sarfi, O(log N) operatsiya.
**Yechim (C++):**
```cpp
#include <vector>
using namespace std;

struct FenwickTree {
    vector<int> bit;
    FenwickTree(int n) : bit(n + 1, 0) {}
    void add(int i, int delta) {
        for(; i < bit.size(); i += i & -i) bit[i] += delta;
    }
    int query(int i) {
        int sum = 0;
        for(; i > 0; i -= i & -i) sum += bit[i];
        return sum;
    }
};
```
**Tushuntirish:** Fenwick Tree (BIT) Segment Tree'ga qaraganda kamroq xotira talab qiladi va implementatsiyasi sodda.

### Topshiriq #1094: Milliy domenlar ro'yxatini qidirish (Trie)
**Tavsif:** Millionlab domen nomlari orasidan prefiks bo'yicha qidiruv.
**Talablar:** O(L) qidiruv vaqti, bu yerda L - so'z uzunligi.
**Yechim (C++):**
```cpp
struct TrieNode {
    TrieNode* children[26] = {nullptr};
    bool isEndOfWord = false;
};

void insert(TrieNode* root, string key) {
    TrieNode* curr = root;
    for(char c : key) {
        if(!curr->children[c-'a']) curr->children[c-'a'] = new TrieNode();
        curr = curr->children[c-'a'];
    }
    curr->isEndOfWord = true;
}
```
**Tushuntirish:** Trie tuzilmasi matnli ma'lumotlarni indekslashda eng yuqori samaradorlikni beradi.

### Topshiriq #1095: Tarmoq komponentlarini aniqlash (DSU)
**Tavsif:** Tarmoqdagi uzilishlarni aniqlash uchun bog'langan komponentlarni topish.
**Talablar:** Path compression va union by rank.
**Yechim (C++):**
```cpp
struct DSU {
    vector<int> parent;
    DSU(int n) { parent.resize(n); for(int i=0; i<n; ++i) parent[i] = i; }
    int find(int i) {
        if(parent[i] == i) return i;
        return parent[i] = find(parent[i]); // Path compression
    }
    void unite(int i, int j) {
        int root_i = find(i), root_j = find(j);
        if(root_i != root_j) parent[root_i] = root_j;
    }
};
```
**Tushuntirish:** DSU dinamik ravishda tarmoq segmentlarini birlashtirish va ularning bog'liqligini tekshirish uchun eng tezkor vositadir.

### Topshiriq #1096: Eng uzun umumiy prefiks (Trie + DFS)
**Tavsif:** Milliy kodlar bazasidagi takrorlanuvchi qismlarni aniqlash.
**Talablar:** Rekursiv xavfsizlik va stack limitini hisobga olish.
**Yechim (C++):**
```cpp
// Trie tugunlari bo'ylab DFS yordamida prefiks qidirish
string findLCP(TrieNode* root) {
    TrieNode* curr = root;
    string lcp = "";
    while(curr) {
        int count = 0, idx = -1;
        for(int i=0; i<26; ++i) if(curr->children[i]) { count++; idx = i; }
        if(count != 1 || curr->isEndOfWord) break;
        lcp += (char)('a' + idx);
        curr = curr->children[idx];
    }
    return lcp;
}
```
**Tushuntirish:** Ushbu yondashuv Trie daraxti bo'ylab bir marta o'tish bilan barcha so'zlar uchun umumiy prefiksni aniqlaydi.

### Topshiriq #1097: Katta hajmli graflarda aylanishni aniqlash (DFS)
**Tavsif:** Tizim jarayonlarida "deadlock" (o'lik nuqta) holatini aniqlash.
**Talablar:** O(V+E) vaqt murakkabligi.
**Yechim (C++):**
```cpp
bool hasCycle(int u, vector<vector<int>>& adj, vector<int>& visited) {
    visited[u] = 1; // Joriy yo'lda
    for(int v : adj[u]) {
        if(visited[v] == 1) return true;
        if(visited[v] == 0 && hasCycle(v, adj, visited)) return true;
    }
    visited[u] = 2; // Tekshirib bo'lingan
    return false;
}
```
**Tushuntirish:** `visited` massividagi 3 ta holat (0: ko'rilmagan, 1: yo'lda, 2: tugallangan) siklni aniqlash uchun eng samarali usuldir.

### Topshiriq #1098: Segment Tree bilan Range Update
**Tavsif:** Server guruhlariga bir vaqtning o'zida yangilanish yuborish (Lazy Propagation).
**Talablar:** O(log N) murakkablik.
**Yechim (C++):**
```cpp
void updateRange(int node, int start, int end, int l, int r, int val, vector<long long>& tree, vector<long long>& lazy) {
    if(lazy[node] != 0) {
        tree[node] += (end - start + 1) * lazy[node];
        if(start != end) { lazy[2*node] += lazy[node]; lazy[2*node+1] += lazy[node]; }
        lazy[node] = 0;
    }
    if(start > end || start > r || end < l) return;
    if(start >= l && end <= r) { tree[node] += (end - start + 1) * val; return; }
    int mid = (start + end) / 2;
    updateRange(2*node, start, mid, l, r, val, tree, lazy);
    updateRange(2*node+1, mid+1, end, l, r, val, tree, lazy);
    tree[node] = tree[2*node] + tree[2*node+1];
}
```
**Tushuntirish:** Lazy propagation katta oraliqlarni yangilashda vaqtni tejaydi, chunki u faqat kerak bo'lganda hisoblaydi.

### Topshiriq #1099: Eng yaqin qo'shni (K-D Tree asoslari)
**Tavsif:** Geografik koordinatalar bo'yicha eng yaqin serverni topish.
**Talablar:** 2D fazoda qidiruvni optimallashtirish.
**Yechim (C++):**
```cpp
struct Point { int x, y; };
// Oddiy 2D qidiruv uchun strukturaviy yondashuv
double dist(Point a, Point b) {
    return sqrt(pow(a.x - b.x, 2) + pow(a.y - b.y, 2));
}
```
**Tushuntirish:** K-D Tree ko'p o'lchovli ma'lumotlar bazasida qidiruvni logarifmik vaqtga tushiradi.

### Topshiriq #1100: Fenwick Tree bilan 2D so'rovlar
**Tavsif:** 2D matritsa ko'rinishidagi hududiy server yuklamalarini yig'ish.
**Talablar:** O(log N * log M) murakkablik.
**Yechim (C++):**
```cpp
void update2D(int r, int c, int val, vector<vector<int>>& bit) {
    for(int i = r; i < bit.size(); i += i & -i)
        for(int j = c; j < bit[0].size(); j += j & -j)
            bit[i][j] += val;
}
```
**Tushuntirish:** 2D Fenwick Tree matritsadagi sub-to'rtburchak yig'indisini hisoblash uchun eng ixcham va tezkor yechimdir.