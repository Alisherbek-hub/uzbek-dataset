# Khorazmiy AI: Python - Modul 22
## Mavzu: Ilg'or Algoritmlar: Graflar, Segment Trees, Fenwick va Trie tuzilmalari

### Topshiriq #1051: Tarmoq topologiyasida qisqa yo'lni topish (Dijkstra)
**Tavsif:** Katta hajmdagi ma'lumotlar markazlari o'rtasidagi kechikishni (latency) minimallashtirish uchun eng qisqa yo'lni aniqlash.
**Talablar:** $O(E \log V)$ murakkablik, xotira xavfsizligi va `heapq` kutubxonasidan foydalanish.
**Yechim (Python):**
```python
import heapq

def eng_qisqa_yoq(graf, boshlangich, maqsad):
    # Masofalarni cheksizlik bilan belgilash
    masofalar = {tugun: float('inf') for tugun in graf}
    masofalar[boshlangich] = 0
    navbat = [(0, boshlangich)]
    
    while navbat:
        joriy_masofa, joriy_tugun = heapq.heappop(navbat)
        
        if joriy_masofa > masofalar[joriy_tugun]:
            continue
            
        for qoshni, vazn in graf[joriy_tugun].items():
            masofa = joriy_masofa + vazn
            if masofa < masofalar[qoshni]:
                masofalar[qoshni] = masofa
                heapq.heappush(navbat, (masofa, qoshni))
    return masofalar[maqsad]
```
**Tushuntirish:** Dijkstra algoritmi ustuvor navbat (priority queue) yordamida eng samarali yo'lni topadi, bu real vaqt rejimida tarmoq yuklamasini boshqarish uchun eng maqbul yechimdir.

### Topshiriq #1052: Dinamik diapazonli yig'indini hisoblash (Segment Tree)
**Tavsif:** Moliya tizimlarida ma'lum vaqt oralig'idagi tranzaksiyalar yig'indisini tezkor hisoblash.
**Talablar:** $O(\log N)$ yangilash va so'rov vaqti.
**Yechim (Python):**
```python
class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (2 * self.n)
        for i in range(self.n): self.tree[self.n + i] = data[i]
        for i in range(self.n - 1, 0, -1): self.tree[i] = self.tree[2*i] + self.tree[2*i+1]

    def yangilash(self, i, qiymat):
        i += self.n
        self.tree[i] = qiymat
        while i > 1:
            i //= 2
            self.tree[i] = self.tree[2*i] + self.tree[2*i+1]
```
**Tushuntirish:** Segment Tree massivdagi o'zgarishlarni tezkor qayta ishlash va oraliq yig'indilarni logarifmik vaqtda topish imkonini beradi.

### Topshiriq #1053: Prefiks qidiruv tizimi (Trie)
**Tavsif:** Foydalanuvchi kiritayotgan so'zlarni avtomatik to'ldirish (autocomplete) tizimi.
**Talablar:** Xotirani tejash va $O(L)$ qidiruv vaqti (L - so'z uzunligi).
**Yechim (Python):**
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def qoshish(self, word):
        node = self.root
        for char in word:
            node = node.children.setdefault(char, TrieNode())
        node.is_end = True
```
**Tushuntirish:** Trie daraxti prefikslarni saqlash uchun eng samarali tuzilma bo'lib, katta lug'atlarda qidiruvni keskin tezlashtiradi.

### Topshiriq #1054: Kümülatif chastotalarni boshqarish (Fenwick Tree)
**Tavsif:** Katta ma'lumotlar oqimida tezkor statistik hisobotlar yaratish.
**Talablar:** $O(\log N)$ murakkablik va minimal xotira sarfi.
**Yechim (Python):**
```python
class FenwickTree:
    def __init__(self, n):
        self.tree = [0] * (n + 1)

    def yangilash(self, i, delta):
        while i < len(self.tree):
            self.tree[i] += delta
            i += i & (-i)

    def yigindi(self, i):
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s
```
**Tushuntirish:** Fenwick Tree (Binary Indexed Tree) Segment Tree'ga qaraganda kamroq xotira talab qiladi va kodlash uchun qulayroqdir.

### Topshiriq #1055: Graflarda sikllarni aniqlash (DFS)
**Tavsif:** Tizim bog'liqliklarida (dependencies) yuzaga kelishi mumkin bo'lgan o'zaro blokirovkalarni (deadlock) aniqlash.
**Talablar:** Rekursiv xavfsizlik va $O(V+E)$ vaqt.
**Yechim (Python):**
```python
def sikl_bormi(graf):
    tashrif = set()
    rekursiya_steki = set()

    def dfs(tugun):
        tashrif.add(tugun)
        rekursiya_steki.add(tugun)
        for qoshni in graf.get(tugun, []):
            if qoshni not in tashrif:
                if dfs(qoshni): return True
            elif qoshni in rekursiya_steki: return True
        rekursiya_steki.remove(tugun)
        return False
    return any(dfs(t) for t in graf if t not in tashrif)
```
**Tushuntirish:** DFS orqali rekursiya steki kuzatiladi, bu esa yo'naltirilgan graflarda sikllarni aniqlashning standart usulidir.

### Topshiriq #1056: Eng yaqin umumiy ota (LCA)
**Tavsif:** Ierarxik ma'lumotlar bazasida (masalan, fayl tizimi) ikki tugun o'rtasidagi eng yaqin umumiy ota-tugunni topish.
**Talablar:** $O(N)$ oldindan ishlov berish.
**Yechim (Python):**
```python
def lca(root, p, q):
    if not root or root == p or root == q:
        return root
    chap = lca(root.left, p, q)
    ong = lca(root.right, p, q)
    if chap and ong: return root
    return chap if chap else ong
```
**Tushuntirish:** Rekursiv yondashuv daraxt tuzilmasini pastdan yuqoriga qarab tahlil qiladi, bu esa ierarxik qidiruv uchun juda samarali.

### Topshiriq #1057: Topologik tartiblash (Kahn algoritmi)
**Tavsif:** Vazifalarni bajarilish ketma-ketligini (task scheduling) belgilash.
**Talablar:** Kirish darajasi (in-degree) hisobi va $O(V+E)$.
**Yechim (Python):**
```python
from collections import deque

def topologik_tartib(graf, in_degree):
    navbat = deque([u for u in graf if in_degree[u] == 0])
    natija = []
    while navbat:
        u = navbat.popleft()
        natija.append(u)
        for v in graf[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0: navbat.append(v)
    return natija
```
**Tushuntirish:** Kahn algoritmi vazifalar o'rtasidagi bog'liqlikni buzmasdan chiziqli tartibni hosil qiladi.

### Topshiriq #1058: Minimal qamrovchi daraxt (Kruskal)
**Tavsif:** Shaharlararo optik tolali tarmoqni eng kam xarajat bilan ulash.
**Talablar:** Union-Find ma'lumotlar tuzilmasidan foydalanish.
**Yechim (Python):**
```python
def kruskal(tugunlar_soni, qirralar):
    qirralar.sort(key=lambda x: x[2])
    parent = list(range(tugunlar_soni))
    def find(i):
        if parent[i] == i: return i
        return find(parent[i])
    
    mst = []
    for u, v, w in qirralar:
        if find(u) != find(v):
            parent[find(u)] = find(v)
            mst.append((u, v, w))
    return mst
```
**Tushuntirish:** Kruskal algoritmi qirralarni vazn bo'yicha saralab, eng arzon tarmoqni qurish imkonini beradi.

### Topshiriq #1059: Kenglik bo'yicha qidiruv (BFS)
**Tavsif:** Ijtimoiy tarmoqlarda "do'stlar do'sti" darajasini aniqlash.
**Talablar:** $O(V+E)$ vaqt va xotira samaradorligi.
**Yechim (Python):**
```python
from collections import deque

def bfs_masofa(graf, start):
    masofalar = {start: 0}
    navbat = deque([start])
    while navbat:
        u = navbat.popleft()
        for v in graf[u]:
            if v not in masofalar:
                masofalar[v] = masofalar[u] + 1
                navbat.append(v)
    return masofalar
```
**Tushuntirish:** BFS qatlamma-qatlam qidiruvni amalga oshiradi, bu esa eng yaqin qo'shnilarni topishda eng ishonchli usuldir.

### Topshiriq #1060: Ikki qismli grafni tekshirish (Bipartite)
**Tavsif:** Foydalanuvchilarni ikki guruhga (masalan, mijoz va yetkazib beruvchi) bo'lish imkoniyatini tekshirish.
**Talablar:** Ranglash (coloring) usuli va $O(V+E)$.
**Yechim (Python):**
```python
def is_bipartite(graf):
    rang = {}
    for tugun in graf:
        if tugun not in rang:
            stack = [(tugun, 0)]
            rang[tugun] = 0
            while stack:
                u, c = stack.pop()
                for v in graf[u]:
                    if v not in rang:
                        rang[v] = 1 - c
                        stack.append((v, 1 - c))
                    elif rang[v] == c: return False
    return True
```
**Tushuntirish:** Grafni ikki rang bilan bo'yash orqali uning ikki qismli ekanligini tekshirish, tizimni segmentlarga ajratish uchun muhimdir.

---

### Topshiriq #1061: Tarmoq topologiyasida eng qisqa yo'lni aniqlash (Dijkstra)
**Tavsif:** Katta hajmdagi serverlar tarmog'ida ma'lumotlar paketini eng kam kechikish bilan uzatish.
**Talablar:** O(E log V) murakkablik, xotira xavfsizligi va `heapq` kutubxonasidan foydalanish.
**Yechim (Python):**
```python
import heapq

def eng_qisqa_yoq(graf, start):
    # Masofalarni cheksizlik bilan belgilash
    masofalar = {tugun: float('infinity') for tugun in graf}
    masofalar[start] = 0
    navbat = [(0, start)]
    
    while navbat:
        joriy_masofa, joriy_tugun = heapq.heappop(navbat)
        
        if joriy_masofa > masofalar[joriy_tugun]:
            continue
            
        for qoshni, vazn in graf[joriy_tugun].items():
            masofa = joriy_masofa + vazn
            if masofa < masofalar[qoshni]:
                masofalar[qoshni] = masofa
                heapq.heappush(navbat, (masofa, qoshni))
    return masofalar
```
**Tushuntirish:** Dijkstra algoritmi ustuvor navbat (priority queue) yordamida optimallashtirildi, bu esa katta tarmoqlarda tezkor ishlashni ta'minlaydi.

### Topshiriq #1062: Dinamik massivda oraliq yig'indisini hisoblash (Fenwick Tree)
**Tavsif:** Moliya tizimlarida real vaqt rejimida tranzaksiyalar yig'indisini kuzatish.
**Talablar:** O(log N) yangilash va so'rov vaqti.
**Yechim (Python):**
```python
class FenwickTree:
    def __init__(self, n):
        self.tree = [0] * (n + 1)
        
    def yangilash(self, i, delta):
        while i < len(self.tree):
            self.tree[i] += delta
            i += i & (-i)
            
    def yigindi(self, i):
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s
```
**Tushuntirish:** Fenwick Tree (Binary Indexed Tree) massivni yangilash va yig'indini olishda eng yuqori samaradorlikni beradi.

### Topshiriq #1063: Katta hajmdagi matnlarni qidirish (Trie)
**Tavsif:** Milliy qidiruv tizimida so'zlarni avtomatik to'ldirish (autocomplete) funksiyasi.
**Talablar:** Xotirani tejash va O(L) qidiruv vaqti (L - so'z uzunligi).
**Yechim (Python):**
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
        
    def qoshish(self, word):
        node = self.root
        for char in word:
            node = node.children.setdefault(char, TrieNode())
        node.is_end = True
```
**Tushuntirish:** Trie tuzilmasi prefikslarni saqlash uchun ideal bo'lib, millionlab so'zlar orasidan tezkor qidiruvni ta'minlaydi.

### Topshiriq #1064: Oraliqdagi eng katta qiymatni topish (Segment Tree)
**Tavsif:** Sensor ma'lumotlari oqimida ma'lum vaqt oralig'idagi eng yuqori ko'rsatkichni aniqlash.
**Talablar:** O(log N) so'rov vaqti, rekursiv bo'lmagan yondashuv tavsiya etiladi.
**Yechim (Python):**
```python
class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (2 * self.n)
        self.tree[self.n:] = data
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = max(self.tree[2*i], self.tree[2*i+1])
            
    def query(self, l, r):
        res = 0
        l += self.n; r += self.n
        while l < r:
            if l & 1: res = max(res, self.tree[l]); l += 1
            if r & 1: r -= 1; res = max(res, self.tree[r])
            l //= 2; r //= 2
        return res
```
**Tushuntirish:** Segment Tree massivdagi statik va dinamik oraliq so'rovlari uchun eng optimal yechimdir.

### Topshiriq #1065: Graflarda sikllarni aniqlash (DFS)
**Tavsif:** Mikroxizmatlar arxitekturasida bog'liqliklar (dependencies) orasida halqali bog'liqlik (circular dependency) yo'qligini tekshirish.
**Talablar:** O(V + E) murakkablik, rekursiya chuqurligini nazorat qilish.
**Yechim (Python):**
```python
def sikl_bormi(graf):
    tashrif = set()
    rekursiya_steki = set()
    
    def dfs(tugun):
        tashrif.add(tugun)
        rekursiya_steki.add(tugun)
        for qoshni in graf.get(tugun, []):
            if qoshni not in tashrif:
                if dfs(qoshni): return True
            elif qoshni in rekursiya_steki: return True
        rekursiya_steki.remove(tugun)
        return False
    
    return any(dfs(n) for n in graf if n not in tashrif)
```
**Tushuntirish:** DFS orqali "rekursiya steki"ni kuzatish orqali yo'naltirilgan graflarda sikllarni aniqlash xavfsiz va samarali.

### Topshiriq #1066: Kenglik bo'yicha qidiruv (BFS)
**Tavsif:** Ijtimoiy tarmoq graflarida ikki foydalanuvchi orasidagi eng qisqa "do'stlik" masofasini topish.
**Talablar:** Xotira samaradorligi, `collections.deque` dan foydalanish.
**Yechim (Python):**
```python
from collections import deque

def bfs_masofa(graf, start, goal):
    navbat = deque([(start, 0)])
    tashrif = {start}
    while navbat:
        tugun, masofa = navbat.popleft()
        if tugun == goal: return masofa
        for qoshni in graf.get(tugun, []):
            if qoshni not in tashrif:
                tashrif.add(qoshni)
                navbat.append((qoshni, masofa + 1))
    return -1
```
**Tushuntirish:** BFS eng qisqa yo'lni topishda (vaznsiz graflar uchun) eng ishonchli algoritmdir.

### Topshiriq #1067: Trie yordamida so'zlarni guruhlash
**Tavsif:** Katta hajmdagi lug'at ma'lumotlarini prefikslar bo'yicha tasniflash.
**Talablar:** O(N * L) murakkablik, ma'lumotlar yaxlitligi.
**Yechim (Python):**
```python
def guruhlash(sozlar):
    trie = {}
    for soz in sozlar:
        node = trie
        for char in soz:
            node = node.setdefault(char, {})
        node['#'] = True # Soz tugashi belgisi
    return trie
```
**Tushuntirish:** Trie lug'atni ierarxik ko'rinishda saqlash uchun eng ixcham tuzilma hisoblanadi.

### Topshiriq #1068: Fenwick Tree bilan oraliq yangilash
**Tavsif:** Katta hajmdagi massivda oraliq qiymatlarni ommaviy yangilash (Range Update).
**Talablar:** O(log N) operatsiya vaqti.
**Yechim (Python):**
```python
class FenwickRange:
    def __init__(self, n):
        self.bit = [0] * (n + 1)
        
    def update(self, i, val):
        while i < len(self.bit):
            self.bit[i] += val
            i += i & (-i)
            
    def range_update(self, l, r, val):
        self.update(l, val)
        self.update(r + 1, -val)
```
**Tushuntirish:** Farqlar massivi (difference array) yordamida Fenwick Tree'ni oraliq yangilash uchun moslashtirish.

### Topshiriq #1069: Minimal qamrovchi daraxt (Kruskal)
**Tavsif:** Shaharlararo optik tolali tarmoqni eng kam xarajat bilan ulash.
**Talablar:** Disjoint Set Union (DSU) tuzilmasidan foydalanish.
**Yechim (Python):**
```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
    def find(self, i):
        if self.parent[i] == i: return i
        return self.find(self.parent[i])
    def union(self, i, j):
        root_i, root_j = self.find(i), self.find(j)
        if root_i != root_j: self.parent[root_i] = root_j
```
**Tushuntirish:** Kruskal algoritmi DSU bilan birgalikda eng kam xarajatli tarmoq topologiyasini qurishda standart hisoblanadi.

### Topshiriq #1070: Segment Tree bilan oraliq yig'indini yangilash
**Tavsif:** Katta hajmdagi ma'lumotlar bazasida oraliq qiymatlarni tezkor o'zgartirish va o'qish.
**Talablar:** Lazy Propagation texnikasi, O(log N) murakkablik.
**Yechim (Python):**
```python
# Lazy propagation uchun asosiy mantiq
def push(self, v):
    if self.lazy[v] != 0:
        self.tree[2*v] += self.lazy[v]
        self.lazy[2*v] += self.lazy[v]
        self.tree[2*v+1] += self.lazy[v]
        self.lazy[2*v+1] += self.lazy[v]
        self.lazy[v] = 0
```
**Tushuntirish:** Lazy Propagation so'rovlar soni ko'p bo'lganda Segment Tree samaradorligini keskin oshiradi, chunki u yangilanishlarni faqat kerak bo'lganda amalga oshiradi.

---

### Topshiriq #1071: Tarmoq trafigini optimallashtirish (Dijkstra algoritmi)
**Tavsif:** Katta hajmdagi serverlar tarmog'ida paketlarni eng qisqa yo'l bilan uzatish. Real vaqt rejimida kechikishni kamaytirish uchun zarur.
**Talablar:** O(E log V) murakkablik, xatolarga chidamlilik.
**Yechim (Python):**
```python
import heapq

def eng_qisqa_yoq(graf, start):
    # Masofalarni cheksizlik bilan belgilash
    masofalar = {tugun: float('inf') for tugun in graf}
    masofalar[start] = 0
    navbat = [(0, start)]
    
    while navbat:
        hozirgi_masofa, u = heapq.heappop(navbat)
        
        if hozirgi_masofa > masofalar[u]: continue
        
        for v, vazn in graf[u].items():
            if masofalar[u] + vazn < masofalar[v]:
                masofalar[v] = masofalar[u] + vazn
                heapq.heappush(navbat, (masofalar[v], v))
    return masofalar
```
**Tushuntirish:** `heapq` (min-heap) yordamida eng qisqa yo'lni topish eng samarali usul hisoblanadi, bu katta tarmoqlarda resurs sarfini keskin kamaytiradi.

---

### Topshiriq #1072: Dinamik massivda oraliq yig'indisini hisoblash (Fenwick Tree)
**Tavsif:** Moliya tizimlarida tranzaksiyalar oqimini real vaqtda kuzatish va ma'lum oraliqdagi yig'indini tezkor aniqlash.
**Talablar:** O(log N) yangilash va so'rov vaqti.
**Yechim (Python):**
```python
class FenwickTree:
    def __init__(self, n):
        self.tree = [0] * (n + 1)
    
    def yangilash(self, i, delta):
        while i < len(self.tree):
            self.tree[i] += delta
            i += i & (-i)
            
    def yigindi(self, i):
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s
```
**Tushuntirish:** Fenwick Tree (Binary Indexed Tree) xotira tejamkorligi va tezligi bo'yicha Segment Tree'dan ustunroq, ayniqsa nuqtali yangilash talab qilinganda.

---

### Topshiriq #1073: Keng ko'lamli qidiruv tizimi (Trie)
**Tavsif:** Foydalanuvchi so'rovlarini avtomatik to'ldirish (autocomplete) tizimi uchun lug'at bazasini saqlash.
**Talablar:** Xotira samaradorligi va tezkor prefiks qidiruvi.
**Yechim (Python):**
```python
class TrieNode:
    def __init__(self):
        self.bolalar = {}
        self.oxiri = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
        
    def qoshish(self, soz):
        node = self.root
        for harf in soz:
            node = node.bolalar.setdefault(harf, TrieNode())
        node.oxiri = True
```
**Tushuntirish:** Trie tuzilmasi prefikslarni umumiy saqlash orqali katta lug'atlarda qidiruvni O(L) vaqtda (L - so'z uzunligi) amalga oshiradi.

---

### Topshiriq #1074: Segment Tree yordamida diapazonli maksimum (RMQ)
**Tavsif:** Sensor ma'lumotlari oqimida ma'lum vaqt oralig'idagi eng yuqori qiymatni aniqlash.
**Talablar:** O(log N) murakkablik, statik va dinamik ma'lumotlar uchun moslashuvchanlik.
**Yechim (Python):**
```python
class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (2 * self.n)
        for i in range(self.n): self.tree[self.n + i] = data[i]
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = max(self.tree[2*i], self.tree[2*i+1])
            
    def query(self, l, r):
        res = float('-inf')
        l += self.n; r += self.n
        while l < r:
            if l & 1: res = max(res, self.tree[l]); l += 1
            if r & 1: r -= 1; res = max(res, self.tree[r])
            l //= 2; r //= 2
        return res
```
**Tushuntirish:** Iterativ Segment Tree rekursiv yondashuvga qaraganda xotira va tezlik bo'yicha ancha samarali.

---

### Topshiriq #1075: Tarmoq topologiyasini aniqlash (DFS/BFS)
**Tavsif:** Murakkab mikroservislar arxitekturasida bog'liqliklar grafigini tekshirish (tsikllarni aniqlash).
**Talablar:** O(V + E) murakkablik, xavfsiz rekursiya chegarasi.
**Yechim (Python):**
```python
def tsikl_bormi(graf):
    tashrif = set()
    for tugun in list(graf):
        if tugun not in tashrif:
            stack = [(tugun, [tugun])]
            while stack:
                u, path = stack.pop()
                for v in graf.get(u, []):
                    if v in path: return True
                    if v not in tashrif:
                        tashrif.add(v)
                        stack.append((v, path + [v]))
    return False
```
**Tushuntirish:** Iterativ DFS yondashuvi Python'dagi rekursiya chegarasi (recursion limit) muammosini chetlab o'tadi va katta graflarda barqaror ishlaydi.

---

### Topshiriq #1076: Kengaytirilgan Trie (Autocomplete)
**Tavsif:** Foydalanuvchi yozayotgan so'zning davomini bashorat qilish uchun Trie'dan foydalanish.
**Talablar:** O(M) vaqt, bu yerda M - natijalar soni.
**Yechim (Python):**
```python
def prefiks_qidiruv(trie, prefiks):
    node = trie.root
    for char in prefiks:
        if char not in node.bolalar: return []
        node = node.bolalar[char]
    
    natijalar = []
    def dfs(n, path):
        if n.oxiri: natijalar.append(path)
        for char, next_node in n.bolalar.items():
            dfs(next_node, path + char)
    dfs(node, prefiks)
    return natijalar
```
**Tushuntirish:** DFS algoritmi Trie ichidagi barcha mos keluvchi so'zlarni yig'ib olish uchun eng qulay usuldir.

---

### Topshiriq #1077: Minimal qamrovchi daraxt (Kruskal algoritmi)
**Tavsif:** Shaharlararo optik tolali tarmoqni eng kam xarajat bilan ulash.
**Talablar:** Disjoint Set Union (DSU) yordamida samarali boshqarish.
**Yechim (Python):**
```python
def kruskal(n, qirralar):
    parent = list(range(n))
    def find(i):
        if parent[i] == i: return i
        parent[i] = find(parent[i]); return parent[i]
    
    qirralar.sort(key=lambda x: x[2])
    mst = []
    for u, v, w in qirralar:
        root_u, root_v = find(u), find(v)
        if root_u != root_v:
            parent[root_u] = root_v
            mst.append((u, v, w))
    return mst
```
**Tushuntirish:** DSU (Path Compression bilan) Kruskal algoritmini deyarli chiziqli vaqtda ishlashini ta'minlaydi.

---

### Topshiriq #1078: Fenwick Tree (2D)
**Tavsif:** Tasvirni qayta ishlashda (image processing) ma'lum hududlar yig'indisini tezkor hisoblash.
**Talablar:** O(log N * log M) murakkablik.
**Yechim (Python):**
```python
class FenwickTree2D:
    def __init__(self, n, m):
        self.tree = [[0] * (m + 1) for _ in range(n + 1)]
    
    def yangilash(self, r, c, val):
        i = r
        while i < len(self.tree):
            j = c
            while j < len(self.tree[0]):
                self.tree[i][j] += val
                j += j & (-j)
            i += i & (-i)
```
**Tushuntirish:** 2D Fenwick Tree matritsali ma'lumotlar ustida hududiy so'rovlarni (range queries) bajarish uchun eng optimallashgan tuzilmadir.

---

### Topshiriq #1079: Eng uzun umumiy prefiks (Trie)
**Tavsif:** Katta fayl tizimlarida umumiy yo'llarni (path) aniqlash va qisqartirish.
**Talablar:** O(N * L) vaqt, xotira optimallash.
**Yechim (Python):**
```python
def eng_uzun_prefiks(sozlar):
    if not sozlar: return ""
    trie = Trie()
    for s in sozlar: trie.qoshish(s)
    
    node = trie.root
    prefiks = ""
    while len(node.bolalar) == 1 and not node.oxiri:
        char = list(node.bolalar.keys())[0]
        prefiks += char
        node = node.bolalar[char]
    return prefiks
```
**Tushuntirish:** Trie tuzilmasi tarmoqlangan joyigacha bo'lgan qismni aniqlash orqali umumiy prefiksni tezkor topadi.

---

### Topshiriq #1080: Tarmoq oqimi (Ford-Fulkerson)
**Tavsif:** Logistika tizimida omborlar o'rtasidagi maksimal yuk tashish qobiliyatini aniqlash.
**Talablar:** O(E * f) murakkablik, bu yerda f - maksimal oqim.
**Yechim (Python):**
```python
def bfs_oqim(graf, s, t, parent):
    visited = {s}
    queue = [s]
    while queue:
        u = queue.pop(0)
        for v, cap in graf[u].items():
            if v not in visited and cap > 0:
                parent[v] = u
                visited.add(v)
                if v == t: return True
                queue.append(v)
    return False
```
**Tushuntirish:** Ford-Fulkerson algoritmi BFS (Edmonds-Karp) bilan birgalikda eng ishonchli maksimal oqimni topish usulidir.

---

### Topshiriq #1081: Tarmoq trafigini optimallashtirish (Dijkstra algoritmi)
**Tavsif:** Katta ma'lumotlar markazlari o'rtasidagi eng qisqa yo'lni topish. Real vaqt rejimida paketlar yo'nalishini belgilash uchun zarur.
**Talablar:** O(E log V) murakkablik, xotira xavfsizligi va Dijkstra algoritmi.
**Yechim (Python):**
```python
import heapq

def eng_qisqa_yoq(graf, boshlangich):
    # Masofalar jadvalini cheksizlik bilan to'ldirish
    masofalar = {tugun: float('inf') for tugun in graf}
    masofalar[boshlangich] = 0
    navbat = [(0, boshlangich)]
    
    while navbat:
        joriy_masofa, joriy_tugun = heapq.heappop(navbat)
        
        if joriy_masofa > masofalar[joriy_tugun]:
            continue
            
        for qoshni, vazn in graf[joriy_tugun].items():
            masofa = joriy_masofa + vazn
            if masofa < masofalar[qoshni]:
                masofalar[qoshni] = masofa
                heapq.heappush(navbat, (masofa, qoshni))
    return masofalar
```
**Tushuntirish:** `heapq` (min-heap) yordamida eng qisqa yo'lni izlash samaradorligi oshirildi, bu katta tarmoqlar uchun optimaldir.

---

### Topshiriq #1082: Dinamik massivda diapazon yig'indisi (Fenwick Tree)
**Tavsif:** Moliya tizimlarida tranzaksiyalar yig'indisini tezkor hisoblash.
**Talablar:** O(log N) yangilash va so'rov vaqti.
**Yechim (Python):**
```python
class FenwickTree:
    def __init__(self, n):
        self.tree = [0] * (n + 1)
    
    def yangilash(self, i, delta):
        while i < len(self.tree):
            self.tree[i] += delta
            i += i & (-i)
            
    def yigindi(self, i):
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s
```
**Tushuntirish:** Fenwick Tree (Binary Indexed Tree) massivni yangilash va yig'indini olishda eng tezkor tuzilmalardan biridir.

---

### Topshiriq #1083: So'zlarni tezkor qidirish (Trie - Prefiks daraxti)
**Tavsif:** Milliy qidiruv tizimlarida avtomatik to'ldirish (autocomplete) funksiyasi uchun.
**Talablar:** Xotirani tejash va O(L) qidiruv vaqti (L - so'z uzunligi).
**Yechim (Python):**
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def qoshish(self, word):
        node = self.root
        for char in word:
            node = node.children.setdefault(char, TrieNode())
        node.is_end = True
```
**Tushuntirish:** Trie tuzilmasi lug'at hajmi katta bo'lganda ham qidiruvni doimiy vaqtda bajarish imkonini beradi.

---

### Topshiriq #1084: Diapazon bo'yicha eng kichik qiymat (Segment Tree)
**Tavsif:** Sensor ma'lumotlari oqimida minimal qiymatni kuzatish.
**Talablar:** O(log N) murakkablikdagi so'rovlar.
**Yechim (Python):**
```python
class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (2 * self.n)
        for i in range(self.n): self.tree[self.n + i] = data[i]
        for i in range(self.n - 1, 0, -1): self.tree[i] = min(self.tree[2*i], self.tree[2*i+1])
    
    def query(self, l, r):
        l += self.n; r += self.n
        res = float('inf')
        while l < r:
            if l & 1: res = min(res, self.tree[l]); l += 1
            if r & 1: r -= 1; res = min(res, self.tree[r])
            l //= 2; r //= 2
        return res
```
**Tushuntirish:** Segment Tree statik va dinamik diapazon so'rovlari uchun eng mos keladigan tuzilmadir.

---

### Topshiriq #1085: Tarmoq komponentlarini aniqlash (Disjoint Set Union)
**Tavsif:** Ijtimoiy tarmoqlarda foydalanuvchilar guruhlarini (klasterlarni) birlashtirish.
**Talablar:** Path compression va union by rank texnikalari.
**Yechim (Python):**
```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
    def find(self, i):
        if self.parent[i] == i: return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]
    def union(self, i, j):
        root_i, root_j = self.find(i), self.find(j)
        if root_i != root_j: self.parent[root_i] = root_j
```
**Tushuntirish:** DSU algoritmi katta hajmdagi elementlar guruhini birlashtirishda deyarli chiziqli vaqt sarflaydi.

---

### Topshiriq #1086: Topologik tartiblash (Kahn algoritmi)
**Tavsif:** Loyiha boshqaruv tizimlarida vazifalar ketma-ketligini belgilash (DAG).
**Talablar:** O(V + E) murakkablik.
**Yechim (Python):**
```python
from collections import deque

def topologik_tartib(graf, in_degree):
    queue = deque([u for u in graf if in_degree[u] == 0])
    result = []
    while queue:
        u = queue.popleft()
        result.append(u)
        for v in graf[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0: queue.append(v)
    return result
```
**Tushuntirish:** Kahn algoritmi bog'liqliklar zanjirini aniqlashda eng ishonchli usul hisoblanadi.

---

### Topshiriq #1087: Eng katta umumiy prefiks (Trie)
**Tavsif:** Fayl tizimlarida yo'llarni qisqartirish va optimallashtirish.
**Talablar:** Xotira xavfsizligi va samarali qidiruv.
**Yechim (Python):**
```python
def eng_katta_prefiks(sozlar):
    if not sozlar: return ""
    trie = {}
    for soz in sozlar:
        node = trie
        for char in soz:
            node = node.setdefault(char, {})
        node['#'] = True
    
    prefiks = ""
    node = trie
    while len(node) == 1 and '#' not in node:
        char = list(node.keys())[0]
        prefiks += char
        node = node[char]
    return prefiks
```
**Tushuntirish:** Trie tuzilmasi yordamida umumiy prefikslarni aniqlash murakkablikni sezilarli darajada kamaytiradi.

---

### Topshiriq #1088: Tarmoq oqimi (Ford-Fulkerson)
**Tavsif:** Logistika tizimlarida maksimal yuk tashish hajmini hisoblash.
**Talablar:** O(E * f) murakkablik, bu yerda f - maksimal oqim.
**Yechim (Python):**
```python
def bfs(graf, s, t, parent):
    visited = {s}
    queue = [s]
    while queue:
        u = queue.pop(0)
        for v, cap in graf[u].items():
            if v not in visited and cap > 0:
                parent[v] = u
                visited.add(v)
                if v == t: return True
                queue.append(v)
    return False
```
**Tushuntirish:** Ford-Fulkerson algoritmi tarmoq o'tkazuvchanligini optimallashtirish uchun standart yechimdir.

---

### Topshiriq #1089: Katta massivda diapazon o'zgarishi (Difference Array)
**Tavsif:** Katta hajmdagi ma'lumotlar bazasida diapazon bo'yicha yangilanishlarni tezkor amalga oshirish.
**Talablar:** O(1) yangilash, O(N) yakuniy hisoblash.
**Yechim (Python):**
```python
def diapazon_yangilash(arr, l, r, val):
    # Farqlar massivini yaratish
    diff = [0] * (len(arr) + 1)
    diff[l] += val
    diff[r+1] -= val
    
    # Prefix sum orqali asl massivni tiklash
    current = 0
    for i in range(len(arr)):
        current += diff[i]
        arr[i] += current
    return arr
```
**Tushuntirish:** Difference array texnikasi ko'p sonli diapazon yangilanishlarini bitta o'tishda bajarish imkonini beradi.

---

### Topshiriq #1090: Graflarda sikllarni aniqlash (DFS)
**Tavsif:** Tizimlararo bog'liqliklarda (dependency) yuzaga kelishi mumkin bo'lgan "deadlock" holatlarini oldini olish.
**Talablar:** O(V + E) murakkablik, rekursiv xavfsizlik.
**Yechim (Python):**
```python
def sikl_bormi(graf):
    visited = set()
    rec_stack = set()
    
    def dfs(u):
        visited.add(u)
        rec_stack.add(u)
        for v in graf.get(u, []):
            if v not in visited:
                if dfs(v): return True
            elif v in rec_stack: return True
        rec_stack.remove(u)
        return False
        
    for node in list(graf.keys()):
        if node not in visited:
            if dfs(node): return True
    return False
```
**Tushuntirish:** DFS va rekursiv stek yordamida sikllarni aniqlash tizim barqarorligini ta'minlashda muhim ahamiyatga ega.

---

### Topshiriq #1091: Tarmoq trafigini optimallashtirish (Dijkstra)
**Tavsif:** Katta ma'lumotlar markazlari o'rtasidagi eng qisqa yo'lni topish. Real ishlab chiqarishda tarmoq kechikishini (latency) kamaytirish uchun zarur.
**Talablar:** O(E log V) murakkablik, xavfsiz tugunlar orqali o'tishni ta'minlash.
**Yechim (Python):**
```python
import heapq

def eng_qisqa_yoq(graf, start, end):
    # Masofalarni cheksiz deb belgilash
    masofalar = {tugun: float('inf') for tugun in graf}
    masofalar[start] = 0
    navbat = [(0, start)]
    
    while navbat:
        hozirgi_masofa, u = heapq.heappop(navbat)
        if hozirgi_masofa > masofalar[u]: continue
        for v, vazn in graf[u].items():
            if masofalar[u] + vazn < masofalar[v]:
                masofalar[v] = masofalar[u] + vazn
                heapq.heappush(navbat, (masofalar[v], v))
    return masofalar[end]
```
**Tushuntirish:** `heapq` (Priority Queue) yordamida eng qisqa yo'l samarali topiladi, bu katta hajmdagi tarmoq topologiyalari uchun eng maqbul yechimdir.

### Topshiriq #1092: Dinamik diapazonli yig'indi (Fenwick Tree)
**Tavsif:** Real vaqt rejimida moliyaviy tranzaksiyalar yig'indisini hisoblash.
**Talablar:** Yangilash va so'rov uchun O(log N) vaqt murakkabligi.
**Yechim (Python):**
```python
class FenwickTree:
    def __init__(self, n):
        self.tree = [0] * (n + 1)
    def yangilash(self, i, delta):
        while i < len(self.tree):
            self.tree[i] += delta
            i += i & (-i)
    def yigindi(self, i):
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s
```
**Tushuntirish:** Fenwick daraxti xotira tejamkorligi va tezkorligi bilan ajralib turadi, ayniqsa yuqori chastotali ma'lumotlar oqimida.

### Topshiriq #1093: Katta hajmdagi so'zlar bazasi (Trie)
**Tavsif:** Milliy til korpusida avtomatik to'ldirish (autocomplete) funksiyasini amalga oshirish.
**Talablar:** Prefiks bo'yicha qidiruv O(L) murakkablikda bo'lishi kerak.
**Yechim (Python):**
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    def insert(self, word):
        node = self.root
        for char in word:
            node = node.children.setdefault(char, TrieNode())
        node.is_end = True
```
**Tushuntirish:** Trie tuzilmasi lug'at bazalarida qidiruvni indekslashsiz ham juda tez bajarishga imkon beradi.

### Topshiriq #1094: Intervaldagi eng katta qiymat (Segment Tree)
**Tavsif:** Sensor ma'lumotlaridan ma'lum vaqt oralig'idagi maksimal qiymatni aniqlash.
**Talablar:** O(log N) vaqt murakkabligi, rekursiv bo'lmagan implementatsiya tavsiya etiladi.
**Yechim (Python):**
```python
class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (2 * self.n)
        self.tree[self.n:] = data
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = max(self.tree[2*i], self.tree[2*i+1])
    def query(self, l, r):
        res = 0
        l += self.n; r += self.n
        while l < r:
            if l & 1: res = max(res, self.tree[l]); l += 1
            if r & 1: r -= 1; res = max(res, self.tree[r])
            l //= 2; r //= 2
        return res
```
**Tushuntirish:** Segment Tree diapazonli so'rovlar uchun eng kuchli vosita bo'lib, xotirani 2N hajmda samarali ishlatadi.

### Topshiriq #1095: Tarmoqdagi halqalarni aniqlash (DFS)
**Tavsif:** Serverlar o'rtasidagi bog'liqlikda yuzaga kelishi mumkin bo'lgan "deadlock" (o'lik holat) ni aniqlash.
**Talablar:** O(V+E) murakkablik, rekursiv xavfsizlik.
**Yechim (Python):**
```python
def halqa_bormi(graf):
    tashrif = set()
    rekursiya_steki = set()
    def dfs(v):
        tashrif.add(v); rekursiya_steki.add(v)
        for neighbor in graf.get(v, []):
            if neighbor not in tashrif and dfs(neighbor): return True
            elif neighbor in rekursiya_steki: return True
        rekursiya_steki.remove(v)
        return False
    return any(dfs(node) for node in graf if node not in tashrif)
```
**Tushuntirish:** DFS orqali "rekursiya steki" ni kuzatish orqali yo'naltirilgan graflardagi sikllarni aniqlash eng ishonchli usuldir.

### Topshiriq #1096: Katta ma'lumotlar oqimida medianani topish (Heap)
**Tavsif:** Real vaqtda kelayotgan raqamli oqimning medianasini hisoblash.
**Talablar:** O(log N) qo'shish murakkabligi.
**Yechim (Python):**
```python
import heapq
class MedianFinder:
    def __init__(self):
        self.small = [] # Max-heap
        self.large = [] # Min-heap
    def add(self, num):
        heapq.heappush(self.small, -heapq.heappushpop(self.large, num))
        if len(self.large) < len(self.small):
            heapq.heappush(self.large, -heapq.heappop(self.small))
```
**Tushuntirish:** Ikki xil heap (min va max) dan foydalanish oqim ma'lumotlarini saralashsiz medianani topishga imkon beradi.

### Topshiriq #1097: Minimal qamrovchi daraxt (Kruskal)
**Tavsif:** Shaharlararo optik tolali tarmoqni eng kam xarajat bilan ulash.
**Talablar:** Union-Find ma'lumotlar tuzilmasidan foydalanish.
**Yechim (Python):**
```python
def kruskal(n, edges):
    parent = list(range(n))
    def find(i):
        if parent[i] == i: return i
        parent[i] = find(parent[i]); return parent[i]
    edges.sort(key=lambda x: x[2])
    mst = []
    for u, v, w in edges:
        root_u, root_v = find(u), find(v)
        if root_u != root_v:
            parent[root_u] = root_v
            mst.append((u, v, w))
    return mst
```
**Tushuntirish:** Kruskal algoritmi tarmoq infratuzilmasini optimallashtirishda eng kam xarajatli bog'lanishlarni topish uchun standart hisoblanadi.

### Topshiriq #1098: Topologik tartiblash (Kahn algoritmi)
**Tavsif:** Vazifalarni bajarish ketma-ketligini (dependency) aniqlash.
**Talablar:** O(V+E) murakkablik, sikllarni aniqlash.
**Yechim (Python):**
```python
from collections import deque
def topologik_tartib(n, graf, in_degree):
    queue = deque([i for i in range(n) if in_degree[i] == 0])
    result = []
    while queue:
        u = queue.popleft()
        result.append(u)
        for v in graf[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0: queue.append(v)
    return result
```
**Tushuntirish:** Kahn algoritmi vazifalar o'rtasidagi bog'liqlikni vizuallashtirish va bajarilish tartibini belgilashda juda samarali.

### Topshiriq #1099: Eng yaqin umumiy ota (LCA)
**Tavsif:** Ierarxik fayl tizimida ikki papka o'rtasidagi umumiy ildizni topish.
**Talablar:** O(log N) so'rov vaqti.
**Yechim (Python):**
```python
def get_lca(parent, depth, u, v):
    if depth[u] < depth[v]: u, v = v, u
    while depth[u] > depth[v]: u = parent[u]
    while u != v:
        u = parent[u]
        v = parent[v]
    return u
```
**Tushuntirish:** Daraxtsimon tuzilmalarda ota-tugunlar bo'ylab harakatlanish orqali ierarxik bog'liqliklarni tezkor aniqlash.

### Topshiriq #1100: Tarmoq oqimini maksimal darajaga chiqarish (Edmonds-Karp)
**Tavsif:** Logistika tizimida yuk tashish hajmini maksimal darajaga yetkazish.
**Talablar:** O(V * E^2) murakkablik, BFS dan foydalanish.
**Yechim (Python):**
```python
from collections import deque
def max_flow(capacity, source, sink):
    n = len(capacity)
    parent = [-1] * n
    max_f = 0
    while True:
        parent = [-1] * n
        queue = deque([source])
        while queue:
            u = queue.popleft()
            for v, cap in enumerate(capacity[u]):
                if parent[v] == -1 and cap > 0:
                    parent[v] = u; queue.append(v)
        if parent[sink] == -1: break
        path_flow = float('inf')
        s = sink
        while s != source:
            path_flow = min(path_flow, capacity[parent[s]][s])
            s = parent[s]
        max_f += path_flow
        v = sink
        while v != source:
            u = parent[v]
            capacity[u][v] -= path_flow
            capacity[v][u] += path_flow
            v = u
    return max_f
```
**Tushuntirish:** Edmonds-Karp algoritmi tarmoq o'tkazuvchanligini maksimal darajada ishlatish uchun eng ishonchli va barqaror yechimdir.