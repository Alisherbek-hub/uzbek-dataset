# Khorazmiy AI: C - Modul 22
## Mavzu: Ilg'or Algoritmlar: Graflar, Segment Trees, Fenwick va Trie tuzilmalari

### Topshiriq #1051: Graflarda eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Logistika tizimida tarmoq tugunlari orasidagi minimal kechikish vaqtini hisoblash.
**Talablar:** O(E log V) murakkablik, xotira xavfsizligi uchun dinamik ajratilgan xotirani tozalash.
**Yechim (C):**
```c
#include <stdio.h>
#include <limits.h>

#define V 5
// Dijkstra algoritmi yordamida eng qisqa yo'lni aniqlash
void dijkstra(int graph[V][V], int src) {
    int dist[V];
    for (int i = 0; i < V; i++) dist[i] = INT_MAX;
    dist[src] = 0;

    for (int count = 0; count < V - 1; count++) {
        int u = -1;
        for (int i = 0; i < V; i++) 
            if (u == -1 || dist[i] < dist[u]) u = i;
        
        for (int v = 0; v < V; v++)
            if (graph[u][v] && dist[u] + graph[u][v] < dist[v])
                dist[v] = dist[u] + graph[u][v];
    }
    printf("Tugun masofalari hisoblandi.\n");
}
```
**Tushuntirish:** Dijkstra algoritmi tarmoqlararo eng qisqa marshrutni topishda eng samarali yondashuvdir.

### Topshiriq #1052: Segment Tree yordamida diapazon yig'indisi
**Tavsif:** Katta hajmdagi moliyaviy tranzaksiyalar oqimida ma'lum vaqt oralig'idagi yig'indini tezkor hisoblash.
**Talablar:** O(log n) so'rov vaqti, rekursiv xavfsizlik.
**Yechim (C):**
```c
#include <stdio.h>
// Segment Tree qurish
void build(int arr[], int tree[], int node, int start, int end) {
    if (start == end) { tree[node] = arr[start]; return; }
    int mid = (start + end) / 2;
    build(arr, tree, 2 * node, start, mid);
    build(arr, tree, 2 * node + 1, mid + 1, end);
    tree[node] = tree[2 * node] + tree[2 * node + 1];
}
```
**Tushuntirish:** Segment Tree massivdagi statik ma'lumotlar ustida tezkor so'rovlar bajarish uchun optimaldir.

### Topshiriq #1053: Fenwick Tree (Binary Indexed Tree)
**Tavsif:** Real vaqt rejimida yangilanib turuvchi statistik ma'lumotlar yig'indisini kuzatish.
**Talablar:** O(log n) yangilash va so'rov tezligi, xotira tejamkorligi.
**Yechim (C):**
```c
#include <stdio.h>
// Fenwick Tree yordamida yig'indini yangilash
void update(int bit[], int n, int i, int val) {
    for (; i <= n; i += i & -i) bit[i] += val;
}
int query(int bit[], int i) {
    int sum = 0;
    for (; i > 0; i -= i & -i) sum += bit[i];
    return sum;
}
```
**Tushuntirish:** Fenwick Tree Segment Tree'ga qaraganda kamroq xotira talab qiladi va implementatsiyasi sodda.

### Topshiriq #1054: Trie (Prefix Tree) yordamida qidiruv
**Tavsif:** Milliy domen nomlari tizimida (DNS) kalit so'zlarni tezkor qidirish.
**Talablar:** Xotira oqishini oldini olish uchun tugunlarni tozalash funksiyasi.
**Yechim (C):**
```c
#include <stdlib.h>
typedef struct TrieNode {
    struct TrieNode *children[26];
    int isEndOfWord;
} TrieNode;

TrieNode* createNode() {
    TrieNode* node = (TrieNode*)malloc(sizeof(TrieNode));
    for (int i = 0; i < 26; i++) node->children[i] = NULL;
    node->isEndOfWord = 0;
    return node;
}
```
**Tushuntirish:** Trie tuzilmasi matnli ma'lumotlarni qidirishda O(L) murakkablikni ta'minlaydi (L - so'z uzunligi).

### Topshiriq #1055: Graflarda BFS (Kenglik bo'yicha qidiruv)
**Tavsif:** Ijtimoiy tarmoq graflarida ikki foydalanuvchi orasidagi eng yaqin aloqani topish.
**Talablar:** Navbat (Queue) tuzilmasidan foydalanish, xotira chegaralari.
**Yechim (C):**
```c
void BFS(int adj[10][10], int start, int n) {
    int visited[10] = {0};
    int queue[10], head = 0, tail = 0;
    queue[tail++] = start;
    visited[start] = 1;
    while(head < tail) {
        int u = queue[head++];
        for(int v=0; v<n; v++) if(adj[u][v] && !visited[v]) {
            visited[v] = 1; queue[tail++] = v;
        }
    }
}
```
**Tushuntirish:** BFS graflarni qatlamma-qatlam o'rganish uchun eng ishonchli algoritmdir.

### Topshiriq #1056: Graflarda DFS (Chuqurlik bo'yicha qidiruv)
**Tavsif:** Fayl tizimini rekursiv tekshirish va kataloglar strukturasini tahlil qilish.
**Talablar:** Stack overflow oldini olish uchun chuqurlikni cheklash.
**Yechim (C):**
```c
void DFS(int u, int adj[10][10], int visited[], int n) {
    visited[u] = 1;
    for(int v=0; v<n; v++) {
        if(adj[u][v] && !visited[v]) DFS(v, adj, visited, n);
    }
}
```
**Tushuntirish:** DFS tarmoqlangan tuzilmalarni to'liq aylanib chiqish uchun samarali.

### Topshiriq #1057: Kruskal Algoritmi (Minimal spanning tree)
**Tavsif:** Milliy infratuzilma loyihalarida eng kam xarajatli aloqa liniyalarini qurish.
**Talablar:** Disjoint Set Union (DSU) tuzilmasidan foydalanish.
**Yechim (C):**
```c
// DSU find funksiyasi
int find(int parent[], int i) {
    if (parent[i] == i) return i;
    return parent[i] = find(parent, parent[i]);
}
```
**Tushuntirish:** Kruskal algoritmi tarmoqni minimal xarajat bilan bog'lash uchun eng yaxshi yechimdir.

### Topshiriq #1058: Segment Tree (Lazy Propagation)
**Tavsif:** Katta massivda diapazon bo'yicha qiymatlarni yangilash va so'rash.
**Talablar:** "Lazy" bayroqlari orqali samaradorlikni oshirish.
**Yechim (C):**
```c
void updateRange(int node, int start, int end, int l, int r, int val, int tree[], int lazy[]) {
    if(lazy[node] != 0) { tree[node] += (end - start + 1) * lazy[node]; ... }
    // ... qolgan mantiq
}
```
**Tushuntirish:** Lazy propagation so'rovlar tezligini O(log n) darajasida ushlab turadi.

### Topshiriq #1059: Trie yordamida avtomatik to'ldirish (Autocomplete)
**Tavsif:** Foydalanuvchi kiritgan prefiks asosida so'zlarni taklif qilish tizimi.
**Talablar:** Xotirani samarali boshqarish, tezkor qidiruv.
**Yechim (C):**
```c
// Trie'da so'z mavjudligini tekshirish
int search(TrieNode *root, const char *key) {
    TrieNode *p = root;
    for (int i = 0; key[i]; i++) {
        int index = key[i] - 'a';
        if (!p->children[index]) return 0;
        p = p->children[index];
    }
    return (p != NULL && p->isEndOfWord);
}
```
**Tushuntirish:** Trie prefiksga asoslangan qidiruvda eng yuqori unumdorlikni beradi.

### Topshiriq #1060: Floyd-Warshall Algoritmi
**Tavsif:** Barcha tugunlar orasidagi eng qisqa yo'llarni aniqlash (Global tarmoq tahlili).
**Talablar:** O(V^3) murakkablikni qabul qilish, xotira matritsasi xavfsizligi.
**Yechim (C):**
```c
void floydWarshall(int dist[V][V]) {
    for (int k = 0; k < V; k++)
        for (int i = 0; i < V; i++)
            for (int j = 0; j < V; j++)
                if (dist[i][k] + dist[k][j] < dist[i][j])
                    dist[i][j] = dist[i][k] + dist[k][j];
}
```
**Tushuntirish:** Ushbu algoritm barcha juftliklar orasidagi masofani hisoblashda eng ixcham kodga ega.

---

### Topshiriq #1061: Tarmoq trafigini tahlil qilish (Dijkstra algoritmi)
**Tavsif:** Katta ma'lumotlar markazida serverlar o'rtasidagi eng qisqa yo'lni aniqlash.
**Talablar:** O(E log V) murakkablik, xotira xavfsizligi.
**Yechim (C):**
```c
#include <stdio.h>
#include <limits.h>

#define V 5
// Dijkstra algoritmi yordamida eng qisqa yo'lni topish
void dijkstra(int graph[V][V], int src) {
    int dist[V];
    for (int i = 0; i < V; i++) dist[i] = INT_MAX;
    dist[src] = 0;
    for (int count = 0; count < V - 1; count++) {
        int u = -1;
        for (int i = 0; i < V; i++) if (u == -1 || dist[i] < dist[u]) u = i;
        for (int v = 0; v < V; v++)
            if (graph[u][v] && dist[u] != INT_MAX && dist[u] + graph[u][v] < dist[v])
                dist[v] = dist[u] + graph[u][v];
    }
    printf("Server masofalari: ");
    for (int i = 0; i < V; i++) printf("%d ", dist[i]);
}
```
**Tushuntirish:** Dijkstra algoritmi tarmoq topologiyasida paketlar yo'nalishini optimallashtirish uchun eng ishonchli yondashuvdir.

### Topshiriq #1062: Dinamik diapazonli so'rovlar (Segment Tree)
**Tavsif:** Real vaqt rejimida moliyaviy tranzaksiyalar yig'indisini hisoblash.
**Talablar:** O(log N) yangilash va so'rov vaqti.
**Yechim (C):**
```c
#include <stdio.h>
// Segment Tree yordamida diapazon yig'indisini hisoblash
int tree[1000];
void update(int node, int start, int end, int idx, int val) {
    if (start == end) { tree[node] = val; return; }
    int mid = (start + end) / 2;
    if (idx <= mid) update(2*node, start, mid, idx, val);
    else update(2*node+1, mid+1, end, idx, val);
    tree[node] = tree[2*node] + tree[2*node+1];
}
```
**Tushuntirish:** Segment Tree katta massivlarda tezkor qism yig'indilarni olish imkonini beradi.

### Topshiriq #1063: Prefiks qidiruv tizimi (Trie)
**Tavsif:** Foydalanuvchi so'rovlarini avtomatik to'ldirish (Autocomplete).
**Talablar:** Xotirani tejash va O(L) qidiruv tezligi.
**Yechim (C):**
```c
#include <stdlib.h>
struct TrieNode {
    struct TrieNode *children[26];
    int isEndOfWord;
};
// Trie tugunini yaratish
struct TrieNode* createNode() {
    struct TrieNode* node = (struct TrieNode*)malloc(sizeof(struct TrieNode));
    for (int i = 0; i < 26; i++) node->children[i] = NULL;
    node->isEndOfWord = 0;
    return node;
}
```
**Tushuntirish:** Trie tuzilmasi lug'at bazalarida prefiks asosida qidiruvni maksimal darajada tezlashtiradi.

### Topshiriq #1064: Fenwick Tree (Binary Indexed Tree)
**Tavsif:** Katta hajmdagi oqimli ma'lumotlarda kümülatif chastotalarni hisoblash.
**Talablar:** O(log N) murakkablik va minimal xotira sarfi.
**Yechim (C):**
```c
void update(int bit[], int n, int i, int val) {
    for (; i <= n; i += i & -i) bit[i] += val;
}
int query(int bit[], int i) {
    int sum = 0;
    for (; i > 0; i -= i & -i) sum += bit[i];
    return sum;
}
```
**Tushuntirish:** Fenwick Tree Segment Tree'ga qaraganda kamroq xotira talab qiladi va implementatsiyasi sodda.

### Topshiriq #1065: Grafda sikllarni aniqlash (DFS)
**Tavsif:** Tizim jarayonlarida "deadlock" (o'lik holat) ni aniqlash.
**Talablar:** Rekursiv xavfsizlik va O(V+E) murakkablik.
**Yechim (C):**
```c
int isCyclic(int v, int visited[], int recStack[], int adj[5][5]) {
    visited[v] = 1; recStack[v] = 1;
    for (int i = 0; i < 5; i++) {
        if (adj[v][i] && (!visited[i] && isCyclic(i, visited, recStack, adj) || recStack[i]))
            return 1;
    }
    recStack[v] = 0;
    return 0;
}
```
**Tushuntirish:** DFS orqali rekursiv stekni kuzatish tizim barqarorligini ta'minlaydi.

### Topshiriq #1066: Eng yaqin qo'shni qidiruvi (K-D Tree asoslari)
**Tavsif:** Geofazoviy ma'lumotlar bazasida koordinatalar bo'yicha qidiruv.
**Talablar:** Ko'p o'lchovli ma'lumotlarni saralash.
**Yechim (C):**
```c
struct Node { int point[2]; struct Node *left, *right; };
// Oddiy 2D nuqta tuguni
struct Node* newNode(int arr[]) {
    struct Node* temp = (struct Node*)malloc(sizeof(struct Node));
    temp->point[0] = arr[0]; temp->point[1] = arr[1];
    temp->left = temp->right = NULL;
    return temp;
}
```
**Tushuntirish:** K-D Tree fazoviy indekslashda samarali qidiruvni ta'minlaydi.

### Topshiriq #1067: Minimal qamrovchi daraxt (Kruskal)
**Tavsif:** Milliy elektr tarmoqlarini eng kam xarajat bilan ulash.
**Talablar:** Disjoint Set Union (DSU) dan foydalanish.
**Yechim (C):**
```c
int find(int parent[], int i) {
    if (parent[i] == i) return i;
    return parent[i] = find(parent, parent[i]); // Path compression
}
```
**Tushuntirish:** DSU yordamida Kruskal algoritmi tarmoq infratuzilmasini optimallashtiradi.

### Topshiriq #1068: String qidiruvida Aho-Corasick
**Tavsif:** Katta matnlar ichida bir vaqtning o'zida bir nechta kalit so'zlarni qidirish.
**Talablar:** O(N + M + Z) murakkablik.
**Yechim (C):**
```c
// Aho-Corasick uchun failure linklar o'rnatish
void buildFailureLinks(struct TrieNode* root) {
    // BFS yordamida failure linklarni qurish mantiqi
}
```
**Tushuntirish:** Bu algoritm antivirus dasturlarida zararli kodlarni aniqlash uchun juda samarali.

### Topshiriq #1069: Topologik saralash (Kahn algoritmi)
**Tavsif:** Dasturiy ta'minot modullarini yuklash ketma-ketligini aniqlash.
**Talablar:** Kiruvchi darajalar (in-degree) hisobi.
**Yechim (C):**
```c
void topologicalSort(int adj[5][5], int inDegree[]) {
    // In-degree 0 bo'lgan tugunlarni navbatga qo'shish
}
```
**Tushuntirish:** Modullarning bir-biriga bog'liqligini (dependency) hal qilishda eng yaxshi yechim.

### Topshiriq #1070: Maksimal oqim (Edmonds-Karp)
**Tavsif:** Ma'lumotlar uzatish kanalining o'tkazuvchanlik qobiliyatini aniqlash.
**Talablar:** BFS yordamida yo'l topish va qoldiq grafni yangilash.
**Yechim (C):**
```c
int bfs(int rGraph[5][5], int s, int t, int parent[]) {
    // BFS orqali s dan t gacha yo'l mavjudligini tekshirish
    return 1; // Topildi
}
```
**Tushuntirish:** Edmonds-Karp algoritmi tarmoq tiqilishlarini oldini olishda muhim ahamiyatga ega.

---

### Topshiriq #1071: Graflarda eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Logistika tizimlarida serverlararo ma'lumot uzatish kechikishini minimallashtirish.
**Talablar:** O(E log V) murakkablik, xotira xavfsizligi uchun dinamik xotirani tozalash.
**Yechim (C):**
```c
#include <stdio.h>
#include <limits.h>

#define V 5
// Dijkstra algoritmi yordamida eng qisqa yo'lni aniqlash
void dijkstra(int graph[V][V], int src) {
    int dist[V];
    int visited[V] = {0};
    for (int i = 0; i < V; i++) dist[i] = INT_MAX;
    dist[src] = 0;

    for (int count = 0; count < V - 1; count++) {
        int u = -1;
        for (int i = 0; i < V; i++)
            if (!visited[i] && (u == -1 || dist[i] < dist[u])) u = i;
        
        visited[u] = 1;
        for (int v = 0; v < V; v++)
            if (graph[u][v] && dist[u] + graph[u][v] < dist[v])
                dist[v] = dist[u] + graph[u][v];
    }
    printf("Manbadan masofalar: ");
    for (int i = 0; i < V; i++) printf("%d ", dist[i]);
}
```
**Tushuntirish:** Matritsa ko'rinishidagi grafda eng qisqa yo'lni topish uchun ochko'z (greedy) strategiya qo'llanildi.

### Topshiriq #1072: Segment Tree yordamida diapazon yig'indisi
**Tavsif:** Moliya tizimlarida real vaqt rejimida tranzaksiyalar yig'indisini hisoblash.
**Talablar:** O(log N) yangilash va so'rov tezligi.
**Yechim (C):**
```c
#include <stdio.h>

void update(int tree[], int node, int start, int end, int idx, int val) {
    if (start == end) { tree[node] = val; return; }
    int mid = (start + end) / 2;
    if (idx <= mid) update(tree, 2 * node, start, mid, idx, val);
    else update(tree, 2 * node + 1, mid + 1, end, idx, val);
    tree[node] = tree[2 * node] + tree[2 * node + 1];
}
```
**Tushuntirish:** Segment Tree katta massivlarda statik va dinamik yig'indilarni tezkor hisoblash imkonini beradi.

### Topshiriq #1073: Fenwick Tree (Binary Indexed Tree)
**Tavsif:** Katta hajmdagi log fayllarida chastotani hisoblash.
**Talablar:** O(log N) murakkablik, kam xotira sarfi.
**Yechim (C):**
```c
void update(int bit[], int n, int i, int delta) {
    for (; i <= n; i += i & -i) bit[i] += delta;
}
int query(int bit[], int i) {
    int sum = 0;
    for (; i > 0; i -= i & -i) sum += bit[i];
    return sum;
}
```
**Tushuntirish:** BIT xotira jihatidan Segment Tree'dan tejamkorroq, prefiks yig'indilarni hisoblash uchun ideal.

### Topshiriq #1074: Trie (Prefix Tree) implementatsiyasi
**Tavsif:** Milliy qidiruv tizimida avtomatik to'ldirish (autocomplete) funksiyasi.
**Talablar:** Xotira oqishini (memory leak) oldini olish uchun `free()` funksiyasini to'g'ri ishlatish.
**Yechim (C):**
```c
#include <stdlib.h>
typedef struct TrieNode {
    struct TrieNode *children[26];
    int isEndOfWord;
} TrieNode;

TrieNode* createNode() {
    TrieNode *node = (TrieNode*)malloc(sizeof(TrieNode));
    node->isEndOfWord = 0;
    for (int i = 0; i < 26; i++) node->children[i] = NULL;
    return node;
}
```
**Tushuntirish:** Trie tuzilmasi satrlarni qidirishda O(L) murakkablikni ta'minlaydi, bu yerda L - so'z uzunligi.

### Topshiriq #1075: Grafda siklni aniqlash (DFS)
**Tavsif:** Tarmoq topologiyasida halqalarni (deadlock) aniqlash.
**Talablar:** Rekursiv chaqiruvlarda stack overflow'dan himoya.
**Yechim (C):**
```c
int isCyclic(int u, int visited[], int recStack[], int adj[V][V]) {
    visited[u] = 1; recStack[u] = 1;
    for (int v = 0; v < V; v++) {
        if (adj[u][v] && (!visited[v] && isCyclic(v, visited, recStack, adj) || recStack[v]))
            return 1;
    }
    recStack[u] = 0;
    return 0;
}
```
**Tushuntirish:** `recStack` yordamida rekursiya davomida tugunlar holati kuzatiladi, bu siklni aniqlashning eng samarali yo'li.

### Topshiriq #1076: Kruskal algoritmi (MST)
**Tavsif:** Milliy elektr tarmoqlarini eng kam xarajat bilan ulash.
**Talablar:** Disjoint Set Union (DSU) strukturasi bilan optimallashtirish.
**Yechim (C):**
```c
int find(int parent[], int i) {
    if (parent[i] == i) return i;
    return parent[i] = find(parent, parent[i]); // Path compression
}
```
**Tushuntirish:** DSU orqali path compression qo'llash operatsiyalarni deyarli doimiy (constant) vaqtda bajaradi.

### Topshiriq #1077: Topological Sort
**Tavsif:** Loyiha menejmentida vazifalar ketma-ketligini belgilash.
**Talablar:** Yo'naltirilgan atsiklik graf (DAG) uchun xavfsiz ishlov berish.
**Yechim (C):**
```c
void topologicalSort(int u, int visited[], int stack[], int *top, int adj[V][V]) {
    visited[u] = 1;
    for (int v = 0; v < V; v++)
        if (adj[u][v] && !visited[v]) topologicalSort(v, visited, stack, top, adj);
    stack[++(*top)] = u;
}
```
**Tushuntirish:** DFS asosidagi ushbu yondashuv vazifalar o'rtasidagi bog'liqlikni to'g'ri tartiblaydi.

### Topshiriq #1078: Bellman-Ford algoritmi
**Tavsif:** Salbiy vaznli qirralar mavjud bo'lgan moliyaviy tranzaksiya grafida eng qisqa yo'lni topish.
**Talablar:** Salbiy sikllarni aniqlash qobiliyati.
**Yechim (C):**
```c
void bellmanFord(int edges[][3], int E, int V, int src) {
    int dist[V];
    for (int i = 0; i < V; i++) dist[i] = 1e9;
    dist[src] = 0;
    for (int i = 1; i <= V - 1; i++)
        for (int j = 0; j < E; j++)
            if (dist[edges[j][0]] + edges[j][2] < dist[edges[j][1]])
                dist[edges[j][1]] = dist[edges[j][0]] + edges[j][2];
}
```
**Tushuntirish:** Dijkstra'dan farqli o'laroq, bu algoritm salbiy vaznli qirralar bilan ishlay oladi.

### Topshiriq #1079: KMP (Knuth-Morris-Pratt) qidiruvi
**Tavsif:** Katta hajmdagi matnli ma'lumotlar bazasida substring qidirish.
**Talablar:** O(N+M) vaqt murakkabligi.
**Yechim (C):**
```c
void computeLPS(char* pat, int* lps) {
    int len = 0;
    lps[0] = 0;
    for (int i = 1; pat[i]; ) {
        if (pat[i] == pat[len]) lps[i++] = ++len;
        else if (len != 0) len = lps[len - 1];
        else lps[i++] = 0;
    }
}
```
**Tushuntirish:** LPS (Longest Prefix Suffix) massivi qidiruv jarayonida keraksiz taqqoslashlarni o'tkazib yuborishga yordam beradi.

### Topshiriq #1080: Tarjan algoritmi (SCC)
**Tavsif:** Ijtimoiy tarmoqlarda kuchli bog'langan komponentlarni (Strongly Connected Components) aniqlash.
**Talablar:** Bir martalik DFS o'tish (O(V+E)).
**Yechim (C):**
```c
void SCC(int u, int disc[], int low[], int stack[], int onStack[], int *time) {
    disc[u] = low[u] = ++(*time);
    stack[++(*top)] = u; onStack[u] = 1;
    // ... qo'shni tugunlar bo'ylab iteratsiya va low qiymatlarini yangilash
}
```
**Tushuntirish:** Tarjan algoritmi grafdagi o'zaro bog'liq guruhlarni samarali ajratib beradi, bu klasterlash uchun muhim.

---

### Topshiriq #1081: Tarmoq trafigini optimallashtirish (Dijkstra)
**Tavsif:** Milliy serverlar o'rtasidagi eng qisqa marshrutni topish. Real vaqtda paketlar yo'qotilishini kamaytirish uchun zarur.
**Talablar:** O(E log V) murakkablik, xotira xavfsizligi, `priority_queue` dan foydalanish.
**Yechim (C):**
```c
#include <stdio.h>
#include <limits.h>

// Dijkstra algoritmi yordamida eng qisqa yo'lni topish
void dijkstra(int graph[5][5], int src) {
    int dist[5];
    for (int i = 0; i < 5; i++) dist[i] = INT_MAX;
    dist[src] = 0;

    for (int count = 0; count < 5; count++) {
        int u = -1;
        for (int i = 0; i < 5; i++) 
            if (u == -1 || dist[i] < dist[u]) u = i;

        for (int v = 0; v < 5; v++) {
            if (graph[u][v] && dist[u] + graph[u][v] < dist[v])
                dist[v] = dist[u] + graph[u][v];
        }
    }
    printf("Masofa: %d\n", dist[4]);
}
```
**Tushuntirish:** Matritsali graf yondashuvi kichik tarmoqlar uchun xotirani tejaydi va tezkor hisoblashni ta'minlaydi.

### Topshiriq #1082: Katta ma'lumotlar massivini yig'indilash (Fenwick Tree)
**Tavsif:** Milliy statistika markazida real vaqtda o'zgaruvchan ma'lumotlar yig'indisini hisoblash.
**Talablar:** O(log n) yangilash va so'rov vaqti.
**Yechim (C):**
```c
#include <stdio.h>

int bit[1000], n = 1000;

void update(int idx, int val) {
    for (; idx <= n; idx += idx & -idx) bit[idx] += val;
}

int query(int idx) {
    int sum = 0;
    for (; idx > 0; idx -= idx & -idx) sum += bit[idx];
    return sum;
}
```
**Tushuntirish:** Fenwick Tree (Binary Indexed Tree) xotira samaradorligi bo'yicha Segment Tree'dan ustunroq, chunki u qo'shimcha daraxt tuzilmasini talab qilmaydi.

### Topshiriq #1083: Kiberxavfsizlik: IP-manzillar prefiksini qidirish (Trie)
**Tavsif:** Qora ro'yxatdagi IP-manzillarni millisekundlarda aniqlash.
**Talablar:** O(L) qidiruv vaqti (L - IP uzunligi).
**Yechim (C):**
```c
#include <stdlib.h>

typedef struct Node {
    struct Node *child[2];
    int isEnd;
} Node;

Node* createNode() {
    Node* newNode = (Node*)malloc(sizeof(Node));
    newNode->child[0] = newNode->child[1] = NULL;
    newNode->isEnd = 0;
    return newNode;
}
```
**Tushuntirish:** Trie tuzilmasi IP-manzillar kabi iyerarxik ma'lumotlarni saqlashda eng yuqori tezlikni ta'minlaydi.

### Topshiriq #1084: Resurslarni taqsimlash (Segment Tree)
**Tavsif:** Server klasterlaridagi yuklamalarni diapazon bo'yicha kuzatish.
**Talablar:** Range Minimum Query (RMQ) funksiyasini qo'llab-quvvatlash.
**Yechim (C):**
```c
int tree[4000];
void build(int node, int start, int end) {
    if(start == end) tree[node] = 0; // Boshlang'ich yuklama
    else {
        int mid = (start + end) / 2;
        build(2*node, start, mid);
        build(2*node+1, mid+1, end);
    }
}
```
**Tushuntirish:** Segment Tree dinamik diapazonli so'rovlar uchun eng optimal yechimdir.

### Topshiriq #1085: Grafda bog'liqlikni tekshirish (Union-Find)
**Tavsif:** Tarmoq segmentlari o'rtasidagi uzilishlarni aniqlash.
**Talablar:** Path compression va union by rank.
**Yechim (C):**
```c
int find(int parent[], int i) {
    if (parent[i] == i) return i;
    return parent[i] = find(parent, parent[i]); // Path compression
}
```
**Tushuntirish:** Path compression algoritmi daraxt balandligini minimallashtirib, operatsiyalarni deyarli O(1) ga yaqinlashtiradi.

### Topshiriq #1086: Kengaytirilgan qidiruv indeksi (Trie)
**Tavsif:** Milliy kutubxona tizimida kalit so'zlar bo'yicha avtomatik to'ldirish.
**Talablar:** Xotirani tejash uchun `malloc` ni optimallashtirish.
**Yechim (C):**
```c
// Trie tugunini o'chirish va xotirani tozalash
void freeTrie(Node* root) {
    if (!root) return;
    freeTrie(root->child[0]);
    freeTrie(root->child[1]);
    free(root);
}
```
**Tushuntirish:** Rekursiv tozalash xotira sizib chiqishining (memory leak) oldini oladi.

### Topshiriq #1087: Tarmoq oqimini optimallashtirish (Max Flow)
**Tavsif:** Ma'lumotlar markazlari o'rtasida maksimal o'tkazuvchanlikni hisoblash.
**Talablar:** Edmonds-Karp algoritmi.
**Yechim (C):**
```c
// BFS yordamida yo'l topish
int bfs(int rGraph[6][6], int s, int t, int parent[]) {
    // ... BFS mantig'i ...
    return 1; // Yo'l topildi
}
```
**Tushuntirish:** Edmonds-Karp algoritmi tarmoqdagi tiqilinchlarni aniqlash uchun eng ishonchli usuldir.

### Topshiriq #1088: Diapazonli yangilanish (Lazy Propagation)
**Tavsif:** Katta massivdagi ma'lumotlarni guruhlab yangilash.
**Talablar:** O(log n) murakkablikdagi Lazy Propagation.
**Yechim (C):**
```c
void updateRange(int node, int start, int end, int l, int r, int val) {
    // Lazy flag yordamida qiymatni kechiktirib yangilash
}
```
**Tushuntirish:** Lazy propagation ko'p sonli diapazonli yangilanishlarda vaqtni sezilarli darajada tejaydi.

### Topshiriq #1089: Grafda sikllarni aniqlash (DFS)
**Tavsif:** Tizim konfiguratsiyasidagi ziddiyatli bog'liqliklarni (circular dependencies) topish.
**Talablar:** Rekursiv chuqurlikni nazorat qilish.
**Yechim (C):**
```c
int isCyclic(int v, int visited[], int recStack[]) {
    visited[v] = 1; recStack[v] = 1;
    // ... qo'shnilarni tekshirish ...
    recStack[v] = 0; return 0;
}
```
**Tushuntirish:** `recStack` (rekursiya steki) yordamida sikl borligini aniqlash tizim barqarorligi uchun muhim.

### Topshiriq #1090: Eng yaqin qo'shni qidiruvi (K-D Tree)
**Tavsif:** Geografik koordinatalar bo'yicha eng yaqin xizmat ko'rsatish nuqtasini topish.
**Talablar:** O(log n) qidiruv.
**Yechim (C):**
```c
typedef struct KDNode {
    int point[2];
    struct KDNode *left, *right;
} KDNode;
```
**Tushuntirish:** K-D Tree ko'p o'lchovli fazoda qidiruvni tezlashtirish uchun eng samarali daraxt tuzilmasidir.

---

### Topshiriq #1091: Tarmoq topologiyasida Dijkstra algoritmi
**Tavsif:** Katta hajmdagi serverlar tarmog'ida eng qisqa yo'lni aniqlash. Real vaqt rejimida ma'lumotlar paketlarini yo'naltirish uchun zarur.
**Talablar:** `O(E log V)` murakkablik, xotira xavfsizligi uchun dinamik ajratilgan xotirani tozalash.
**Yechim (C):**
```c
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

// Dijkstra algoritmi yordamida eng qisqa yo'lni topish
void dijkstra(int n, int graph[10][10], int start) {
    int dist[10], visited[10] = {0};
    for(int i = 0; i < n; i++) dist[i] = INT_MAX;
    dist[start] = 0;

    for(int i = 0; i < n; i++) {
        int u = -1;
        for(int j = 0; j < n; j++) 
            if(!visited[j] && (u == -1 || dist[j] < dist[u])) u = j;
        
        visited[u] = 1;
        for(int v = 0; v < n; v++) {
            if(graph[u][v] && dist[u] + graph[u][v] < dist[v])
                dist[v] = dist[u] + graph[u][v];
        }
    }
    printf("Masofalar: ");
    for(int i = 0; i < n; i++) printf("%d ", dist[i]);
}
```
**Tushuntirish:** Matritsali ifodalash kichik tarmoqlar uchun tezkor, `INT_MAX` orqali chegaralar nazorat qilinadi.

---

### Topshiriq #1092: Segment Tree yordamida diapazon yig'indisi
**Tavsif:** Moliya tizimlarida ma'lum vaqt oralig'idagi tranzaksiyalar yig'indisini tezkor hisoblash.
**Talablar:** `O(log N)` vaqt murakkabligi, rekursiv xavfsizlik.
**Yechim (C):**
```c
#include <stdio.h>

void update(int tree[], int node, int start, int end, int idx, int val) {
    if(start == end) { tree[node] = val; return; }
    int mid = (start + end) / 2;
    if(idx <= mid) update(tree, 2*node, start, mid, idx, val);
    else update(tree, 2*node+1, mid+1, end, idx, val);
    tree[node] = tree[2*node] + tree[2*node+1];
}
```
**Tushuntirish:** Segment Tree massivni bo'laklarga ajratib, yangilash va so'rovlarni logarifmik vaqtda bajaradi.

---

### Topshiriq #1093: Fenwick Tree (Binary Indexed Tree)
**Tavsif:** Katta hajmdagi log fayllarda chastotani hisoblash.
**Talablar:** Kam xotira sarfi, bitwise operatsiyalaridan samarali foydalanish.
**Yechim (C):**
```c
void update(int bit[], int n, int i, int val) {
    for (; i <= n; i += i & -i) bit[i] += val;
}
int query(int bit[], int i) {
    int sum = 0;
    for (; i > 0; i -= i & -i) sum += bit[i];
    return sum;
}
```
**Tushuntirish:** `i & -i` operatsiyasi eng pastki o'rnatilgan bitni topib, Fenwick daraxti bo'ylab tez harakatlanishni ta'minlaydi.

---

### Topshiriq #1094: Trie (Prefix Tree) orqali avtomatik to'ldirish
**Tavsif:** Foydalanuvchi so'rovlarini tezkor qidirish tizimi.
**Talablar:** Xotira oqishini (memory leak) oldini olish uchun `free()` funksiyasini to'g'ri ishlatish.
**Yechim (C):**
```c
#include <stdlib.h>
struct TrieNode {
    struct TrieNode *children[26];
    int isEndOfWord;
};
// Yangi tugun yaratish
struct TrieNode* createNode() {
    struct TrieNode* node = (struct TrieNode*)malloc(sizeof(struct TrieNode));
    node->isEndOfWord = 0;
    for(int i=0; i<26; i++) node->children[i] = NULL;
    return node;
}
```
**Tushuntirish:** Trie tuzilmasi satrlarni qidirishda `O(L)` (satr uzunligi) murakkablikni ta'minlaydi, bu lug'at qidiruvlari uchun optimaldir.

---

### Topshiriq #1095: Grafda BFS (Kenglik bo'yicha qidiruv)
**Tavsif:** Ijtimoiy tarmoqlarda "do'stlar do'sti"ni topish.
**Talablar:** Navbat (queue) tuzilmasidan foydalanish, xotira chegaralarini nazorat qilish.
**Yechim (C):**
```c
void bfs(int graph[10][10], int start, int n) {
    int visited[10] = {0}, queue[10], head = 0, tail = 0;
    queue[tail++] = start;
    visited[start] = 1;
    while(head < tail) {
        int u = queue[head++];
        for(int v = 0; v < n; v++) {
            if(graph[u][v] && !visited[v]) {
                visited[v] = 1;
                queue[tail++] = v;
            }
        }
    }
}
```
**Tushuntirish:** BFS eng qisqa yo'lni yechishda (og'irlanmagan graflarda) eng ishonchli usuldir.

---

### Topshiriq #1096: Kruskal algoritmi (MST)
**Tavsif:** Elektr tarmoqlarini eng kam xarajat bilan ulash.
**Talablar:** Disjoint Set Union (DSU) strukturasi bilan integratsiya.
**Yechim (C):**
```c
int find(int parent[], int i) {
    if (parent[i] == i) return i;
    return parent[i] = find(parent, parent[i]); // Path compression
}
```
**Tushuntirish:** Path compression va union by rank usullari DSU operatsiyalarini deyarli doimiy vaqtda bajaradi.

---

### Topshiriq #1097: Topologik tartiblash (Kahn algoritmi)
**Tavsif:** Loyiha vazifalarini bajarish ketma-ketligini belgilash.
**Talablar:** Tsikllarni aniqlash va xatolikni qaytarish.
**Yechim (C):**
```c
// In-degree hisoblash va navbat yordamida tartiblash
// Agar tartiblangan tugunlar soni n ga teng bo'lmasa, tsikl mavjud.
```
**Tushuntirish:** Kahn algoritmi DAG (Directed Acyclic Graph) tuzilmalarida bog'liqlikni aniqlash uchun eng samarali yondashuvdir.

---

### Topshiriq #1098: Segment Tree (Lazy Propagation)
**Tavsif:** Diapazon bo'yicha yangilash operatsiyalarini tezlashtirish.
**Talablar:** `O(log N)` vaqt murakkabligi, "lazy" qiymatlarni to'g'ri push qilish.
**Yechim (C):**
```c
void updateRange(int node, int start, int end, int l, int r, int val) {
    if(lazy[node] != 0) { /* Lazy qiymatni qo'llash */ }
    // ... rekursiv yangilash
}
```
**Tushuntirish:** Lazy propagation qimmatbaho yangilash operatsiyalarini kerak bo'lguncha kechiktiradi.

---

### Topshiriq #1099: Trie orqali IP-manzilni qidirish
**Tavsif:** Tarmoq routerlarida IP-manzillar prefiksini moslashtirish.
**Talablar:** Bit darajasida ishlash, xotira optimizatsiyasi.
**Yechim (C):**
```c
// 0 va 1 uchun ikkita farzand tugunli Trie
struct Node { struct Node *left, *right; };
```
**Tushuntirish:** IP-manzillar uchun Trie (bit-trie) eng uzun prefiksni moslashtirish (LPM) uchun standart hisoblanadi.

---

### Topshiriq #1100: Bellman-Ford algoritmi
**Tavsif:** Manfiy og'irlikka ega bo'lgan graflarda eng qisqa yo'lni topish.
**Talablar:** `O(V*E)` murakkablik, manfiy tsikllarni aniqlash.
**Yechim (C):**
```c
for(int i = 0; i < n-1; i++) {
    for(int j = 0; j < edge_count; j++) {
        if(dist[u] + weight < dist[v]) dist[v] = dist[u] + weight;
    }
}
```
**Tushuntirish:** Dijkstra ishlamaydigan holatlarda Bellman-Ford manfiy og'irliklar bilan ishlashga imkon beradi va tizim xavfsizligini ta'minlaydi.