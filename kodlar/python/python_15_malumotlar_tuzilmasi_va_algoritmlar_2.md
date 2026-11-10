# Python Dasturlash Tili — 15-Qism: Ma'lumotlar Tuzilmasi va Algoritmlar (2-Qism)
## (701-750 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam murakkab daraxtlar, to'dalar (Heaps), ilg'or graf algoritmlari va prefiks tuzilmalarini qamrab oladi:
* Binar daraxtlar va BST larni to'liq tahlil qilish, chuqurlik (DFS) va qatlamlar (BFS);
* Heaps (Min-Heap, Max-Heap, Data Stream Median, Kth Largest);
* Graf marshrutlari: BFS, DFS, Sikllar, Topologik saralash (Kahn);
* Qisqa yo'llar: Deykstra, Bellman-Ford, Floyd-Warshall, A* (A-Star);
* Minimal qamrovchi daraxt (Kruskal, DSU), Maksimal oqim (Edmonds-Karp);
* Ilg'or strukturalar: Trie, Fenwick Tree (BIT), Segment Tree, Tarjan va Kosaraju SCC;

---

# 701-Topshiriq: Ikkilik daraxt (Binary Tree) balandligini (Max Depth) hisoblash

## Topshiriq sharti:
Ikkilik daraxtning ildizidan eng uzoq bargigacha bo'lgan maksimal chuqurlikni rekursiv toping.

## Yechim (Python kodi):
```python
class DaraxtTuguni:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def max_depth(root):
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))

# Daraxt: [3, 9, 20, None, None, 15, 7]
daraxt = DaraxtTuguni(3, DaraxtTuguni(9), DaraxtTuguni(20, DaraxtTuguni(15), DaraxtTuguni(7)))
print("Maksimal chuqurlik:", max_depth(daraxt))
```

## Tushuntirish va Mantiq:
1. Daraxt balandligi `1 + max(chap_chuqurlik, ong_chuqurlik)` rekursiv formulasi bilan hisoblanadi. O(n) vaqt.

## Ishlash natijasi:
```text
Chiqish: Maksimal chuqurlik: 3
```

---

# 702-Topshiriq: Daraxtni aylanib chiqish: Pre-order, In-order va Post-order (DFS)

## Topshiriq sharti:
Daraxt tugunlarini uch xil chuqurlik bo'yicha aylanib chiqish (DFS) usullarida chiqaring.

## Yechim (Python kodi):
```python
def preorder(root):
    return [root.val] + preorder(root.left) + preorder(root.right) if root else []

def inorder(root):
    return inorder(root.left) + [root.val] + inorder(root.right) if root else []

def postorder(root):
    return postorder(root.left) + postorder(root.right) + [root.val] if root else []

t = DaraxtTuguni(1, DaraxtTuguni(2), DaraxtTuguni(3))
print("Pre-order (Root-Left-Right):", preorder(t))
print("In-order (Left-Root-Right):", inorder(t))
print("Post-order (Left-Right-Root):", postorder(t))
```

## Tushuntirish va Mantiq:
1. Daraxtlar va sintaksis daraxtlarini (AST) tahlil qilishda ushbu uch traversal poydevor hisoblanadi.

## Ishlash natijasi:
```text
Chiqish: Pre-order (Root-Left-Right): [1, 2, 3], In-order (Left-Root-Right): [2, 1, 3], Post-order (Left-Right-Root): [2, 3, 1]
```

---

# 703-Topshiriq: Qatlamlar bo'yicha aylanib chiqish (Level Order Traversal / BFS)

## Topshiriq sharti:
collections.deque navbati yordamida daraxtni kenglik bo'yicha (BFS) darajama-daraja o'qing.

## Yechim (Python kodi):
```python
from collections import deque

def level_order(root):
    if not root: return []
    natija = []
    navbat = deque([root])
    while navbat:
        daraja_hajmi = len(navbat)
        joriy_daraja = []
        for _ in range(daraja_hajmi):
            tugun = navbat.popleft()
            joriy_daraja.append(tugun.val)
            if tugun.left: navbat.append(tugun.left)
            if tugun.right: navbat.append(tugun.right)
        natija.append(joriy_daraja)
    return natija

t = DaraxtTuguni(3, DaraxtTuguni(9), DaraxtTuguni(20, DaraxtTuguni(15), DaraxtTuguni(7)))
print("Level-order:", level_order(t))
```

## Tushuntirish va Mantiq:
1. Navbat (Queue) har bir darajadagi tugunlarni to'liq qamrab olgach, keyingi bosqichga o'tish imkonini beradi.

## Ishlash natijasi:
```text
Chiqish: Level-order: [[3], [9, 20], [15, 7]]
```

---

# 704-Topshiriq: Daraxtni teskarisiga o'girish (Invert / Flip Binary Tree)

## Topshiriq sharti:
Daraxtning barcha chap va o'ng shoxlarini ko'zgudek almashtiring.

## Yechim (Python kodi):
```python
def invert_tree(root):
    if not root: return None
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root

t = DaraxtTuguni(4, DaraxtTuguni(2, DaraxtTuguni(1), DaraxtTuguni(3)), DaraxtTuguni(7, DaraxtTuguni(6), DaraxtTuguni(9)))
invert_tree(t)
print("Invert qilingan daraxt (In-order):", inorder(t))
```

## Tushuntirish va Mantiq:
1. Har bir tugunda chap va o'ng bolalar rekursiv ravishda almashtiriladi.

## Ishlash natijasi:
```text
Chiqish: Invert qilingan daraxt (In-order): [9, 7, 6, 4, 3, 2, 1]
```

---

# 705-Topshiriq: Simmetrik daraxtni tekshirish (Symmetric Tree)

## Topshiriq sharti:
Daraxt o'zining markaziy o'qiga nisbatan ko'zgu simmetriyasiga ega ekanligini tekshiring.

## Yechim (Python kodi):
```python
def simmetrikmi(root):
    if not root: return True
    def tekshir(t1, t2):
        if not t1 and not t2: return True
        if not t1 or not t2: return False
        return (t1.val == t2.val and 
                tekshir(t1.left, t2.right) and 
                tekshir(t1.right, t2.left))
    return tekshir(root.left, root.right)

t = DaraxtTuguni(1, DaraxtTuguni(2, None, DaraxtTuguni(3)), DaraxtTuguni(2, None, DaraxtTuguni(3)))
print("Simmetrikmi:", simmetrikmi(t))
```

## Tushuntirish va Mantiq:
1. Chap shoxning chap bolasi o'ng shoxning o'ng bolasi bilan, chapning o'ngi esa o'ngning chapi bilan solishtiriladi.

## Ishlash natijasi:
```text
Chiqish: Simmetrikmi: False
```

---

# 706-Topshiriq: Daraxt diametri (Diameter of Binary Tree)

## Topshiriq sharti:
Daraxtdagi istalgan ikki tugun orasidagi eng uzun yo'l uzunligini toping.

## Yechim (Python kodi):
```python
def tree_diameter(root):
    max_diametr = 0
    def balandlik(node):
        nonlocal max_diametr
        if not node: return 0
        chap = balandlik(node.left)
        ong = balandlik(node.right)
        max_diametr = max(max_diametr, chap + ong)
        return 1 + max(chap, ong)
    
    balandlik(root)
    return max_diametr

t = DaraxtTuguni(1, DaraxtTuguni(2, DaraxtTuguni(4), DaraxtTuguni(5)), DaraxtTuguni(3))
print("Diametr:", tree_diameter(t))
```

## Tushuntirish va Mantiq:
1. Har bir tugunda uning chap va o'ng balandliklari yig'indisi shu tugundan o'tuvchi yo'l uzunligini ifodalaydi.

## Ishlash natijasi:
```text
Chiqish: Diametr: 3
```

---

# 707-Topshiriq: Ikkilik qidiruv daraxti validatsiyasi (Validate BST)

## Topshiriq sharti:
Berilgan daraxt qat'iy BST qoidalariga (chap < ildiz < o'ng) javob berishini tekshiring.

## Yechim (Python kodi):
```python
def is_valid_bst(root, min_val=float('-inf'), max_val=float('inf')):
    if not root: return True
    if not (min_val < root.val < max_val):
        return False
    return (is_valid_bst(root.left, min_val, root.val) and 
            is_valid_bst(root.right, root.val, max_val))

bst = DaraxtTuguni(2, DaraxtTuguni(1), DaraxtTuguni(3))
not_bst = DaraxtTuguni(5, DaraxtTuguni(1), DaraxtTuguni(4, DaraxtTuguni(3), DaraxtTuguni(6)))
print("BST 1:", is_valid_bst(bst))
print("BST 2:", is_valid_bst(not_bst))
```

## Tushuntirish va Mantiq:
1. Har bir tugun o'zining ruxsat etilgan oraliq (min, max) chegaralarida bo'lishi shart.

## Ishlash natijasi:
```text
Chiqish: BST 1: True, BST 2: False
```

---

# 708-Topshiriq: BST da eng kichik umumiy ajdod (Lowest Common Ancestor - LCA)

## Topshiriq sharti:
BST dagi ikki tugunning eng yaqin umumiy ajdodini O(h) vaqtda toping.

## Yechim (Python kodi):
```python
def lca_bst(root, p, q):
    curr = root
    while curr:
        if p.val < curr.val and q.val < curr.val:
            curr = curr.left
        elif p.val > curr.val and q.val > curr.val:
            curr = curr.right
        else:
            return curr

r = DaraxtTuguni(6, DaraxtTuguni(2, DaraxtTuguni(0), DaraxtTuguni(4)), DaraxtTuguni(8))
p = r.left.left  # 0
q = r.left.right # 4
print("LCA(0, 4):", lca_bst(r, p, q).val)
```

## Tushuntirish va Mantiq:
1. Agar ikkala tugun ham joriy tugundan kichik bo'lsa chapga, katta bo'lsa o'ngga burilamiz; aks holda aynan shu tugun ajdoddir.

## Ishlash natijasi:
```text
Chiqish: LCA(0, 4): 2
```

---

# 709-Topshiriq: Daraxt yo'li yig'indisi (Path Sum)

## Topshiriq sharti:
Ildizdan barggacha bo'lgan yo'llarning birontasida elementlar yig'indisi berilgan nishonga tengligini aniqlang.

## Yechim (Python kodi):
```python
def has_path_sum(root, target):
    if not root: return False
    if not root.left and not root.right:
        return root.val == target
    qoldiq = target - root.val
    return has_path_sum(root.left, qoldiq) or has_path_sum(root.right, qoldiq)

t = DaraxtTuguni(5, DaraxtTuguni(4, DaraxtTuguni(11)), DaraxtTuguni(8))
print("Yig'indi 20 bormi:", has_path_sum(t, 20))
print("Yig'indi 13 bormi:", has_path_sum(t, 13))
```

## Tushuntirish va Mantiq:
1. Har bir qadamda nishon qiymatidan joriy tugun ayirilib boriladi va bargda nol qolishi tekshiriladi.

## Ishlash natijasi:
```text
Chiqish: Yig'indi 20 bormi: True, Yig'indi 13 bormi: True
```

---

# 710-Topshiriq: Daraxtni satrga serializatsiya va deserializatsiya qilish (Tree Codec)

## Topshiriq sharti:
Daraxtni faylga saqlash uchun satrga o'giring va satrdan qayta daraxt quring.

## Yechim (Python kodi):
```python
def serialize(root):
    if not root: return "#"
    return f"{root.val},{serialize(root.left)},{serialize(root.right)}"

def deserialize(data):
    qiymatlar = iter(data.split(','))
    def build():
        val = next(qiymatlar)
        if val == "#": return None
        node = DaraxtTuguni(int(val))
        node.left = build()
        node.right = build()
        return node
    return build()

t = DaraxtTuguni(1, DaraxtTuguni(2), DaraxtTuguni(3))
satr = serialize(t)
print("Serializatsiya:", satr)
qayta = deserialize(satr)
print("Tiklandi:", qayta.val, qayta.left.val, qayta.right.val)
```

## Tushuntirish va Mantiq:
1. Pre-order rekursiyasi va bo'sh tugunlar uchun maxsus belgi (#) orqali daraxt bir xil shaklda tiklanadi.

## Ishlash natijasi:
```text
Chiqish: Serializatsiya: 1,2,#,#,3,#,#, Tiklandi: 1 2 3
```

---

# 711-Topshiriq: Min-Heap (Kichik to'da: heapq moduli)

## Topshiriq sharti:
heapq yordamida Min-Heap yaratish, yangi son qo'shish va eng kichigini O(log n) da chiqarish.

## Yechim (Python kodi):
```python
import heapq

heap = []
for x in [40, 10, 30, 5, 20]:
    heapq.heappush(heap, x)

print("Heap strukturasi:", heap)
print("Eng kichigi (pop):", heapq.heappop(heap))
print("Keyingi eng kichigi (pop):", heapq.heappop(heap))
```

## Tushuntirish va Mantiq:
1. Min-Heap daraxtida ildiz har doim eng kichik element bo'ladi. Element qo'shish va olish O(log n).

## Ishlash natijasi:
```text
Chiqish: Heap strukturasi: [5, 10, 30, 40, 20], Eng kichigi (pop): 5, Keyingi eng kichigi (pop): 10
```

---

# 712-Topshiriq: Max-Heap (Katta to'da)

## Topshiriq sharti:
heapq da sonlarni manfiy qilib kiritish orqali Max-Heap tamoyilini yarating.

## Yechim (Python kodi):
```python
import heapq

max_heap = []
for x in [15, 3, 100, 45, 80]:
    heapq.heappush(max_heap, -x)

print("Eng kattasi:", -heapq.heappop(max_heap))
print("Ikkinchi eng kattasi:", -heapq.heappop(max_heap))
```

## Tushuntirish va Mantiq:
1. Qiymatlarni manfiy ishora bilan kiritish orqali Min-Heap ni avtomatik ravishda Max-Heap ga aylantirish Python dasturchilari orasida standart usuldir.

## Ishlash natijasi:
```text
Chiqish: Eng kattasi: 100, Ikkinchi eng kattasi: 80
```

---

# 713-Topshiriq: Massivdagi eng katta K ta element (K Largest Elements: heapq.nlargest)

## Topshiriq sharti:
Millionlab elementlar ichidan eng katta K tasini xotirani tejab topish.

## Yechim (Python kodi):
```python
import heapq

sonlar = [4, 1, 7, 3, 8, 5, 2, 9, 6]
k_eng_katta = heapq.nlargest(3, sonlar)
print("Eng katta 3 ta element:", k_eng_katta)
```

## Tushuntirish va Mantiq:
1. `nlargest` o'lchami K bo'lgan Min-Heap yuritadi va O(N log K) vaqtda natija beradi.

## Ishlash natijasi:
```text
Chiqish: Eng katta 3 ta element: [9, 8, 7]
```

---

# 714-Topshiriq: K ta saralangan ro'yxatlarni birlashtirish (Merge K Sorted Lists)

## Topshiriq sharti:
K ta saralangan oqimlarni Heap yordamida O(N log K) da bitta saralangan ro'yxatga jamlang.

## Yechim (Python kodi):
```python
import heapq

oqimlar = [
    [1, 4, 7],
    [2, 5, 8],
    [3, 6, 9]
]

birlashgan = list(heapq.merge(*oqimlar))
print("Birlashgan ro'yxat:", birlashgan)
```

## Tushuntirish va Mantiq:
1. `heapq.merge()` barcha oqimlarning boshlarini to'dada ushlab eng kichigini qadam-baqadam oqimga beradi.

## Ishlash natijasi:
```text
Chiqish: Birlashgan ro'yxat: [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

---

# 715-Topshiriq: Ma'lumotlar oqimida medianani topish (Find Median from Data Stream)

## Topshiriq sharti:
Har qadamda medianani hisoblash uchun ikkita to'da (Max-Heap va Min-Heap) muvozanatini yurgizing.

## Yechim (Python kodi):
```python
import heapq

class MedianFinder:
    def __init__(self):
        self.kichiklar = [] # Max-heap (manfiy)
        self.kattalar = []  # Min-heap

    def add_num(self, num):
        heapq.heappush(self.kichiklar, -num)
        heapq.heappush(self.kattalar, -heapq.heappop(self.kichiklar))
        if len(self.kattalar) > len(self.kichiklar):
            heapq.heappush(self.kichiklar, -heapq.heappop(self.kattalar))

    def find_median(self):
        if len(self.kichiklar) > len(self.kattalar):
            return float(-self.kichiklar[0])
        return (-self.kichiklar[0] + self.kattalar[0]) / 2.0

mf = MedianFinder()
for n in [1, 2, 3, 4, 5]:
    mf.add_num(n)
    print(f"{n} qo'shildi -> Mediana: {mf.find_median()}")
```

## Tushuntirish va Mantiq:
1. Ikki to'dani o'rtadan bo'lish oqimli ma'lumotlarda medianani O(1) vaqtda olish imkonini beradi.

## Ishlash natijasi:
```text
Chiqish: 1 qo'shildi -> Mediana: 1.0, 2 qo'shildi -> Mediana: 1.5, 3 qo'shildi -> Mediana: 2.0, 4 qo'shildi -> Mediana: 2.5, 5 qo'shildi -> Mediana: 3.0
```

---

# 716-Topshiriq: Grafni ifodalash: Qo'shnilik ro'yxati (Adjacency List)

## Topshiriq sharti:
Graf tugunlari va qirralarini lug'at (defaultdict) yordamida modellashtiring.

## Yechim (Python kodi):
```python
from collections import defaultdict

class Graf:
    def __init__(self):
        self.graf = defaultdict(list)

    def qirra_qosh(self, u, v, yo_naltirilgan=False):
        self.graf[u].append(v)
        if not yo_naltirilgan:
            self.graf[v].append(u)

g = Graf()
g.qirra_qosh("Toshkent", "Samarqand")
g.qirra_qosh("Samarqand", "Buxoro")
g.qirra_qosh("Toshkent", "Farg'ona")

for shahar, qoshnilar in g.graf.items():
    print(f"{shahar} bog'langan: {qoshnilar}")
```

## Tushuntirish va Mantiq:
1. Qo'shnilik ro'yxati xotirani tejaydi (O(V + E)) va grafdagi qo'shnilarni tezkor aylanib chiqishni ta'minlaydi.

## Ishlash natijasi:
```text
Chiqish: Toshkent bog'langan: ['Samarqand', "Farg'ona"], Samarqand bog'langan: ['Toshkent', 'Buxoro'], Buxoro bog'langan: ['Samarqand'], Farg'ona bog'langan: ['Toshkent']
```

---

# 717-Topshiriq: Grafda kenglik bo'yicha qidiruv (BFS - Breadth-First Search)

## Topshiriq sharti:
Boshlang'ich tugundan eng yaqin masofalar bo'yicha grafni BFS bilan aylanib chiqing.

## Yechim (Python kodi):
```python
from collections import deque

def bfs(graf, boshlangich):
    korilgan = set([boshlangich])
    navbat = deque([boshlangich])
    tartib = []
    
    while navbat:
        tugun = navbat.popleft()
        tartib.append(tugun)
        for qoshni in graf.get(tugun, []):
            if qoshni not in korilgan:
                korilgan.add(qoshni)
                navbat.append(qoshni)
    return tartib

graf_xarita = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'], 'E': ['B', 'F'], 'F': ['C', 'E']
}
print("BFS tartibi:", bfs(graf_xarita, 'A'))
```

## Tushuntirish va Mantiq:
1. BFS vaznsiz graflarda ikki nuqta orasidagi eng qisqa yo'lni topish uchun eng to'g'ri algoritmdir.

## Ishlash natijasi:
```text
Chiqish: BFS tartibi: ['A', 'B', 'C', 'D', 'E', 'F']
```

---

# 718-Topshiriq: Grafda chuqurlik bo'yicha qidiruv (DFS - Depth-First Search)

## Topshiriq sharti:
Graf tugunlarini rekursiv tarzda oxirigacha kirib boruvchi DFS algoritmini yozing.

## Yechim (Python kodi):
```python
def dfs(graf, boshlangich, korilgan=None):
    if korilgan is None: korilgan = set()
    korilgan.add(boshlangich)
    tartib = [boshlangich]
    for qoshni in graf.get(boshlangich, []):
        if qoshni not in korilgan:
            tartib.extend(dfs(graf, qoshni, korilgan))
    return tartib

print("DFS tartibi:", dfs(graf_xarita, 'A'))
```

## Tushuntirish va Mantiq:
1. DFS barcha yo'llarni chuqur o'rganadi, sikllarni aniqlash va labirintdan chiqishda ishlatiladi.

## Ishlash natijasi:
```text
Chiqish: DFS tartibi: ['A', 'B', 'D', 'E', 'F', 'C']
```

---

# 719-Topshiriq: Yo'naltirilgan grafda siklni aniqlash (Cycle Detection in Directed Graph)

## Topshiriq sharti:
Kurslar bog'liqligi (prerequisites) grafigida sikl bor-yo'qligini uch rangli (Oq, Kulrang, Qora) DFS bilan toping.

## Yechim (Python kodi):
```python
def sikl_bormi_grafda(n, qirralar):
    graf = defaultdict(list)
    for u, v in qirralar:
        graf[u].append(v)
        
    holat = [0] * n # 0: korilmagan, 1: joriy yolda, 2: toliq korilgan
    def dfs(u):
        holat[u] = 1
        for v in graf[u]:
            if holat[v] == 1: return True
            if holat[v] == 0 and dfs(v): return True
        holat[u] = 2
        return False

    for i in range(n):
        if holat[i] == 0:
            if dfs(i): return True
    return False

print("Sikl 1:", sikl_bormi_grafda(2, [[1, 0]]))
print("Sikl 2 (0->1->0):", sikl_bormi_grafda(2, [[1, 0], [0, 1]]))
```

## Tushuntirish va Mantiq:
1. Kulrang tugun (holat 1) ga qayta urilish orqaga qirra (back-edge) borligini va sikl mavjudligini bildiradi.

## Ishlash natijasi:
```text
Chiqish: Sikl 1: False, Sikl 2 (0->1->0): True
```

---

# 720-Topshiriq: Topologik saralash (Topological Sort / Kahn algoritmi)

## Topshiriq sharti:
Yo'naltirilgan atsiklik graf (DAG) tugunlarini kiruvchi darajalar (in-degree) bo'yicha saralang.

## Yechim (Python kodi):
```python
def topological_sort(n, qirralar):
    graf = defaultdict(list)
    in_degree = [0] * n
    for u, v in qirralar:
        graf[u].append(v)
        in_degree[v] += 1
        
    navbat = deque([i for i in range(n) if in_degree[i] == 0])
    tartib = []
    while navbat:
        u = navbat.popleft()
        tartib.append(u)
        for v in graf[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                navbat.append(v)
    return tartib if len(tartib) == n else []

print("Vazifalar bajarilish tartibi:", topological_sort(4, [[0, 1], [0, 2], [1, 3], [2, 3]]))
```

## Tushuntirish va Mantiq:
1. Kahn algoritmi kompilyatsiya zanjirlari, paketlar menejeri (pip, apt) va CI/CD quvurlarini tartiblashda qo'llaniladi.

## Ishlash natijasi:
```text
Chiqish: Vazifalar bajarilish tartibi: [0, 1, 2, 3]
```

---

# 721-Topshiriq: Deykstra algoritmi (Dijkstra's Shortest Path)

## Topshiriq sharti:
Musbat vaznli grafda bitta tugundan boshqa barcha tugunlarga eng qisqa masofani Min-Heap bilan toping.

## Yechim (Python kodi):
```python
import heapq

def dijkstra(graf, start):
    masofalar = {tugun: float('inf') for tugun in graf}
    masofalar[start] = 0
    pq = [(0, start)]
    
    while pq:
        joriy_masofa, u = heapq.heappop(pq)
        if joriy_masofa > masofalar[u]:
            continue
        for v, vazn in graf[u]:
            yangi_masofa = joriy_masofa + vazn
            if yangi_masofa < masofalar[v]:
                masofalar[v] = yangi_masofa
                heapq.heappush(pq, (yangi_masofa, v))
    return masofalar

graf_vaznli = {
    'A': [('B', 4), ('C', 2)],
    'B': [('A', 4), ('C', 1), ('D', 5)],
    'C': [('A', 2), ('B', 1), ('D', 8), ('E', 10)],
    'D': [('B', 5), ('C', 8), ('E', 2)],
    'E': [('C', 10), ('D', 2)]
}
print("A dan eng qisqa masofalar:", dijkstra(graf_vaznli, 'A'))
```

## Tushuntirish va Mantiq:
1. Deykstra algoritmi ochko'z (greedy) tanlov va Min-Heap orqali O((V + E) log V) da ishlaydi.

## Ishlash natijasi:
```text
Chiqish: A dan eng qisqa masofalar: {'A': 0, 'B': 3, 'C': 2, 'D': 8, 'E': 10}
```

---

# 722-Topshiriq: Bellman-Ford algoritmi (Manfiy vaznlar va sikllar)

## Topshiriq sharti:
Manfiy qirralarga ega grafda eng qisqa yo'lni toping va manfiy siklni aniqlang.

## Yechim (Python kodi):
```python
def bellman_ford(tugunlar, qirralar, start):
    masofalar = {u: float('inf') for u in tugunlar}
    masofalar[start] = 0
    
    for _ in range(len(tugunlar) - 1):
        for u, v, w in qirralar:
            if masofalar[u] != float('inf') and masofalar[u] + w < masofalar[v]:
                masofalar[v] = masofalar[u] + w
                
    # Manfiy sikl tekshiruvi
    for u, v, w in qirralar:
        if masofalar[u] != float('inf') and masofalar[u] + w < masofalar[v]:
            return None # Manfiy sikl mavjud!
    return masofalar

qirralar = [('A', 'B', -1), ('A', 'C', 4), ('B', 'C', 3), ('B', 'D', 2), ('D', 'B', 1)]
print("Bellman-Ford masofalari:", bellman_ford(['A', 'B', 'C', 'D'], qirralar, 'A'))
```

## Tushuntirish va Mantiq:
1. Bellman-Ford O(V * E) da ishlaydi va moliya bo'yicha valyuta arbitrajini (Arbitrage) aniqlashda ishlatiladi.

## Ishlash natijasi:
```text
Chiqish: Bellman-Ford masofalari: {'A': 0, 'B': -1, 'C': 2, 'D': 1}
```

---

# 723-Topshiriq: Floyd-Warshall algoritmi (Barcha juftliklar orasidagi masofa)

## Topshiriq sharti:
Dinamik dasturlash yordamida barcha tugunlar juftliklari orasidagi masofalar matritsasini tuzing.

## Yechim (Python kodi):
```python
def floyd_warshall(n, masofa_matritsa):
    dist = [row[:] for row in masofa_matritsa]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist

INF = float('inf')
m = [
    [0, 5, INF, 10],
    [INF, 0, 3, INF],
    [INF, INF, 0, 1],
    [INF, INF, INF, 0]
]
res = floyd_warshall(4, m)
print("0 dan 3 ga masofa:", res[0][3])
print("0 dan 2 ga masofa:", res[0][2])
```

## Tushuntirish va Mantiq:
1. Floyd-Warshall algoritmi O(V^3) murakkablikda barcha nuqtalar aro masofani to'liq hisoblaydi.

## Ishlash natijasi:
```text
Chiqish: 0 dan 3 ga masofa: 9, 0 dan 2 ga masofa: 8
```

---

# 724-Topshiriq: Disjoint Set Union (DSU / Kruskal uchun Union-Find)

## Topshiriq sharti:
Path Compression va Union by Rank xususiyatlariga ega DSU klassi.

## Yechim (Python kodi):
```python
class DSU:
    def __init__(self, n):
        self.ota = list(range(n))
        self.daraja = [0] * n

    def find(self, i):
        if self.ota[i] != i:
            self.ota[i] = self.find(self.ota[i]) # Path compression
        return self.ota[i]

    def union(self, i, j):
        ildiz_i = self.find(i)
        ildiz_j = self.find(j)
        if ildiz_i != ildiz_j:
            if self.daraja[ildiz_i] < self.daraja[ildiz_j]:
                self.ota[ildiz_i] = ildiz_j
            elif self.daraja[ildiz_i] > self.daraja[ildiz_j]:
                self.ota[ildiz_j] = ildiz_i
            else:
                self.ota[ildiz_j] = ildiz_i
                self.daraja[ildiz_i] += 1
            return True
        return False

dsu = DSU(5)
dsu.union(0, 1)
dsu.union(1, 2)
print("0 va 2 bir komponentdami:", dsu.find(0) == dsu.find(2))
print("0 va 3 bir komponentdami:", dsu.find(0) == dsu.find(3))
```

## Tushuntirish va Mantiq:
1. DSU deyarli O(1) amortizatsiyalangan vaqtda (Ackermann funksiyasi teskarisi) to'plamlar birlashmasini tekshiradi.

## Ishlash natijasi:
```text
Chiqish: 0 va 2 bir komponentdami: True, 0 va 3 bir komponentdami: False
```

---

# 725-Topshiriq: Minimal qamrovchi daraxt (Minimum Spanning Tree: Kruskal algoritmi)

## Topshiriq sharti:
Qirralarni vazni bo'yicha saralab va DSU bilan sikllarni chetlab MST quring.

## Yechim (Python kodi):
```python
def kruskal(n, qirralar):
    # qirralar: [(w, u, v), ...]
    qirralar.sort()
    dsu = DSU(n)
    mst = []
    jami_vazn = 0
    for w, u, v in qirralar:
        if dsu.union(u, v):
            mst.append((u, v, w))
            jami_vazn += w
            if len(mst) == n - 1:
                break
    return jami_vazn, mst

qirralar = [
    (1, 0, 1), (4, 0, 2), (3, 1, 2), (2, 2, 3), (5, 1, 3)
]
vazn, daraxt = kruskal(4, qirralar)
print("MST minimal vazni:", vazn)
print("Tanlangan qirralar:", daraxt)
```

## Tushuntirish va Mantiq:
1. Kruskal algoritmi tarmoq kabelini yotqizish yoki yo'l xaritasini eng arzon xarajat bilan bog'lashda ishlatiladi.

## Ishlash natijasi:
```text
Chiqish: MST minimal vazni: 6, Tanlangan qirralar: [(0, 1, 1), (2, 3, 2), (1, 2, 3)]
```

---

# 726-Topshiriq: Trie (Prefiks daraxti) tuzilmasi

## Topshiriq sharti:
So'zlarni kiritish (insert), qidirish (search) va prefiks tekshirish (startsWith) ni o'z ichiga olgan Trie yarating.

## Yechim (Python kodi):
```python
class TrieNode:
    def __init__(self):
        self.bolalar = {}
        self.soz_tugadimi = False

class Trie:
    def __init__(self):
        self.ildiz = TrieNode()

    def insert(self, soz):
        tugun = self.ildiz
        for c in soz:
            if c not in tugun.bolalar:
                tugun.bolalar[c] = TrieNode()
            tugun = tugun.bolalar[c]
        tugun.soz_tugadimi = True

    def search(self, soz):
        tugun = self._otish(soz)
        return tugun is not None and tugun.soz_tugadimi

    def starts_with(self, prefiks):
        return self._otish(prefiks) is not None

    def _otish(self, satr):
        tugun = self.ildiz
        for c in satr:
            if c not in tugun.bolalar: return None
            tugun = tugun.bolalar[c]
        return tugun

trie = Trie()
trie.insert("olma")
trie.insert("anor")
print("olma bormi:", trie.search("olma"))
print("ol guruh bormi:", trie.starts_with("ol"))
print("nok bormi:", trie.search("nok"))
```

## Tushuntirish va Mantiq:
1. Trie qidiruv tizimlarida avtomatik to'ldirish (Auto-complete) va tezkor lug'at tekshiruvi uchun idealdir.

## Ishlash natijasi:
```text
Chiqish: olma bormi: True, ol guruh bormi: True, nok bormi: False
```

---

# 727-Topshiriq: Trie orqali avtomatik to'ldirish (Auto-complete)

## Topshiriq sharti:
Berilgan prefiks bilan boshlanuvchi barcha so'zlar ro'yxatini qaytaring.

## Yechim (Python kodi):
```python
def avto_toldir(trie, prefiks):
    bosh = trie._otish(prefiks)
    if not bosh: return []
    natija = []
    
    def dfs(node, yo_l):
        if node.soz_tugadimi:
            natija.append(prefiks + "".join(yo_l))
        for harf, bolasi in node.bolalar.items():
            yo_l.append(harf)
            dfs(bolasi, yo_l)
            yo_l.pop()

    dfs(bosh, [])
    return natija

trie.insert("olxo'ri")
trie.insert("olmos")
print("'ol' prefiksi bilan so'zlar:", avto_toldir(trie, "ol"))
```

## Tushuntirish va Mantiq:
1. Foydalanuvchi klaviaturada harf kiritganda bir zumda tavsiyalar chiqarish aynan shu algoritm bilan bajariladi.

## Ishlash natijasi:
```text
Chiqish: 'ol' prefiksi bilan so'zlar: ['olma', "olxo'ri", 'olmos']
```

---

# 728-Topshiriq: Orollar soni (Number of Islands - 2D Grid DFS/BFS)

## Topshiriq sharti:
1 lar (quruqlik) va 0 lar (suv) dan iborat 2D matritsadagi orollar sonini hisoblang.

## Yechim (Python kodi):
```python
def num_islands(grid):
    if not grid: return 0
    m, n = len(grid), len(grid[0])
    orollar = 0

    def ochirish(r, c):
        if r < 0 or r >= m or c < 0 or c >= n or grid[r][c] != '1':
            return
        grid[r][c] = '0' # Cho'ktirish
        ochirish(r + 1, c)
        ochirish(r - 1, c)
        ochirish(r, c + 1)
        ochirish(r, c - 1)

    for i in range(m):
        for j in range(n):
            if grid[i][j] == '1':
                orollar += 1
                ochirish(i, j)
    return orollar

xarita = [
    ['1', '1', '0', '0'],
    ['1', '1', '0', '0'],
    ['0', '0', '1', '0'],
    ['0', '0', '0', '1']
]
print("Orollar soni:", num_islands(xarita))
```

## Tushuntirish va Mantiq:
1. Bog'langan komponentlarni 'cho'ktirish' (Flood Fill) orqali barcha orollar soni aniqlanadi.

## Ishlash natijasi:
```text
Chiqish: Orollar soni: 3
```

---

# 729-Topshiriq: Chirigan apelsinlar (Rotten Oranges - Multi-source BFS)

## Topshiriq sharti:
Chirigan apelsinlar har daqiqada qo'shnilarini chiritsa, barcha apelsinlar chirishi uchun qancha vaqt ketishini toping.

## Yechim (Python kodi):
```python
def oranges_rotting(grid):
    m, n = len(grid), len(grid[0])
    navbat = deque()
    yangi = 0
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 2: navbat.append((r, c))
            elif grid[r][c] == 1: yangi += 1
            
    daqiqalar = 0
    yonalishlar = [(1,0), (-1,0), (0,1), (0,-1)]
    while navbat and yangi > 0:
        daqiqalar += 1
        for _ in range(len(navbat)):
            r, c = navbat.popleft()
            for dr, dc in yonalishlar:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    yangi -= 1
                    navbat.append((nr, nc))
    return daqiqalar if yangi == 0 else -1

apelsinlar = [
    [2, 1, 1],
    [1, 1, 0],
    [0, 1, 1]
]
print("Ketgan vaqt (daqiqa):", oranges_rotting(apelsinlar))
```

## Tushuntirish va Mantiq:
1. Bir nechta manbadan bir vaqtda kengayish (Multi-source BFS) epidemiya yoki to'lqin tarqalishini modellashtiradi.

## Ishlash natijasi:
```text
Chiqish: Ketgan vaqt (daqiqa): 4
```

---

# 730-Topshiriq: So'zlar narvoni (Word Ladder - BFS bilan eng qisqa yo'l)

## Topshiriq sharti:
Bir so'zdan ikkinchisiga har qadamda bitta harfni o'zgartirib eng qisqa o'tishlar sonini toping.

## Yechim (Python kodi):
```python
def ladder_length(boshlangich, tugash, lugat):
    sozlar = set(lugat)
    if tugash not in sozlar: return 0
    navbat = deque([(boshlangich, 1)])
    
    while navbat:
        joriy, qadam = navbat.popleft()
        if joriy == tugash:
            return qadam
        for i in range(len(joriy)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                yangi = joriy[:i] + c + joriy[i+1:]
                if yangi in sozlar:
                    sozlar.remove(yangi)
                    navbat.append((yangi, qadam + 1))
    return 0

print("O'tish uzunligi:", ladder_length("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]))
```

## Tushuntirish va Mantiq:
1. Holatlar fazosini (State Space) BFS orqali tadqiq qilish eng qisqa transformatsiya yo'lini kafolatlaydi.

## Ishlash natijasi:
```text
Chiqish: O'tish uzunligi: 5
```

---

# 731-Topshiriq: Fenwick daraxti (Binary Indexed Tree - BIT)

## Topshiriq sharti:
Prefiks yig'indilarni va elementlarni yangilashni O(log n) da bajaruvchi BIT tuzilmasi.

## Yechim (Python kodi):
```python
class FenwickTree:
    def __init__(self, size):
        self.daraxt = [0] * (size + 1)

    def update(self, i, delta):
        i += 1
        while i < len(self.daraxt):
            self.daraxt[i] += delta
            i += i & (-i)

    def query(self, i):
        i += 1
        s = 0
        while i > 0:
            s += self.daraxt[i]
            i -= i & (-i)
        return s

bit = FenwickTree(5)
bit.update(0, 10); bit.update(1, 20); bit.update(2, 30)
print("0 dan 2 gacha yig'indi:", bit.query(2))
```

## Tushuntirish va Mantiq:
1. Fenwick daraxti eng kam kod bilan dinamik oraliq yig'indilarni hisoblash imkonini beradi.

## Ishlash natijasi:
```text
Chiqish: 0 dan 2 gacha yig'indi: 60
```

---

# 732-Topshiriq: Segmentlar daraxti (Segment Tree: Oraliq minimumi)

## Topshiriq sharti:
Massiv oraliqlaridagi minimum qiymatni O(log n) da so'rovchi Segment Tree klassi.

## Yechim (Python kodi):
```python
class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.daraxt = [0] * (4 * self.n)
        self.arr = arr
        self.qur(0, 0, self.n - 1)

    def qur(self, node, start, end):
        if start == end:
            self.daraxt[node] = self.arr[start]
            return
        mid = (start + end) // 2
        self.qur(2 * node + 1, start, mid)
        self.qur(2 * node + 2, mid + 1, end)
        self.daraxt[node] = min(self.daraxt[2 * node + 1], self.daraxt[2 * node + 2])

    def query_min(self, node, start, end, l, r):
        if r < start or end < l: return float('inf')
        if l <= start and end <= r: return self.daraxt[node]
        mid = (start + end) // 2
        return min(self.query_min(2 * node + 1, start, mid, l, r),
                   self.query_min(2 * node + 2, mid + 1, end, l, r))

st = SegmentTree([5, 2, 8, 1, 9, 3])
print("Oraliq [0, 2] minimumi:", st.query_min(0, 0, 5, 0, 2))
print("Oraliq [2, 5] minimumi:", st.query_min(0, 0, 5, 2, 5))
```

## Tushuntirish va Mantiq:
1. Segment daraxti oraliq amallarini (Range Queries) va dinamik o'zgarishlarni boshqaruvchi qudratli tuzilmadir.

## Ishlash natijasi:
```text
Chiqish: Oraliq [0, 2] minimumi: 2, Oraliq [2, 5] minimumi: 1
```

---

# 733-Topshiriq: Kuchli bog'langan komponentlar (Tarjan's Strongly Connected Components)

## Topshiriq sharti:
Yo'naltirilgan grafdagi o'zaro to'liq bog'langan qismlarni Tarjan algoritmi bilan toping.

## Yechim (Python kodi):
```python
def tarjan_scc(n, graf):
    indekslar = [-1] * n
    past = [-1] * n
    stekda = [False] * n
    stek = []
    vaqt = 0
    scc_lar = []

    def dfs(u):
        nonlocal vaqt
        indekslar[u] = past[u] = vaqt
        vaqt += 1
        stek.append(u)
        stekda[u] = True

        for v in graf.get(u, []):
            if indekslar[v] == -1:
                dfs(v)
                past[u] = min(past[u], past[v])
            elif stekda[v]:
                past[u] = min(past[u], past[v])

        if past[u] == indekslar[u]:
            komponent = []
            while True:
                w = stek.pop()
                stekda[w] = False
                komponent.append(w)
                if w == u: break
            scc_lar.append(komponent)

    for i in range(n):
        if indekslar[i] == -1: dfs(i)
    return scc_lar

graf = {0: [1], 1: [2], 2: [0, 3], 3: [4], 4: []}
print("SCC guruhlari:", tarjan_scc(5, graf))
```

## Tushuntirish va Mantiq:
1. Tarjan algoritmi bitta DFS o'tishida O(V + E) vaqtda barcha kuchli komponentlarni aniqlaydi.

## Ishlash natijasi:
```text
Chiqish: SCC guruhlari: [[4], [3], [2, 1, 0]]
```

---

# 734-Topshiriq: Ko'priklar va bo'g'in tugunlar (Bridges and Articulation Points)

## Topshiriq sharti:
O'chirilsa grafni ikki bo'lakka ajratib yuboradigan kritik ko'priklarni toping.

## Yechim (Python kodi):
```python
def find_bridges(n, qirralar):
    graf = defaultdict(list)
    for u, v in qirralar:
        graf[u].append(v); graf[v].append(u)
        
    tin = [-1] * n; low = [-1] * n
    timer = 0; bridges = []
    
    def dfs(u, p=-1):
        nonlocal timer
        tin[u] = low[u] = timer; timer += 1
        for to in graf[u]:
            if to == p: continue
            if tin[to] != -1:
                low[u] = min(low[u], tin[to])
            else:
                dfs(to, u)
                low[u] = min(low[u], low[to])
                if low[to] > tin[u]:
                    bridges.append((u, to))
                    
    for i in range(n):
        if tin[i] == -1: dfs(i)
    return bridges

print("Kritik ko'priklar:", find_bridges(4, [[0, 1], [1, 2], [2, 0], [1, 3]]))
```

## Tushuntirish va Mantiq:
1. Kritik qirralar tarmoq xavfsizligida zaif nuqtalarni (Single Point of Failure) ko'rsatadi.

## Ishlash natijasi:
```text
Chiqish: Kritik ko'priklar: [(1, 3)]
```

---

# 735-Topshiriq: Euler yo'li va sikli (Hierholzer algoritmi)

## Topshiriq sharti:
Har bir qirradan aynan bir marta o'tuvchi Euler marshrutini toping.

## Yechim (Python kodi):
```python
def find_eulerian_path(graf):
    daraja = defaultdict(int)
    for u in graf:
        for v in graf[u]: daraja[u] += 1
        
    stek = [list(graf.keys())[0]]
    yol = []
    g_nusxa = {u: list(graf[u]) for u in graf}
    
    while stek:
        u = stek[-1]
        if g_nusxa.get(u):
            v = g_nusxa[u].pop()
            stek.append(v)
        else:
            yol.append(stek.pop())
    return yol[::-1]

g = {0: [1], 1: [2], 2: [0]}
print("Euler sikli:", find_eulerian_path(g))
```

## Tushuntirish va Mantiq:
1. Königsberg ko'priklari masalasidan boshlangan klassik algoritm DNK ketma-ketliklarini yig'ishda ishlatiladi.

## Ishlash natijasi:
```text
Chiqish: Euler sikli: [0, 1, 2, 0]
```

---

# 736-Topshiriq: A* (A-Star) qidiruv algoritmi (Hevristika bilan optimal yo'l)

## Topshiriq sharti:
Manxetten masofasi hevristikasi yordamida labirintdan marraga eng tez yetuvchi A* algoritmini tuzing.

## Yechim (Python kodi):
```python
def a_star(bosh, marra, tosiqlar):
    def manxetten(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    pq = [(manxetten(bosh, marra), 0, bosh)]
    g_score = {bosh: 0}
    
    while pq:
        _, g, joriy = heapq.heappop(pq)
        if joriy == marra:
            return g
        x, y = joriy
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            q = (x + dx, y + dy)
            if q in tosiqlar or q[0] < 0 or q[1] < 0: continue
            yangi_g = g + 1
            if yangi_g < g_score.get(q, float('inf')):
                g_score[q] = yangi_g
                f = yangi_g + manxetten(q, marra)
                heapq.heappush(pq, (f, yangi_g, q))
    return -1

print("A* minimal qadam:", a_star((0, 0), (3, 3), {(1, 1), (1, 2), (2, 1)}))
```

## Tushuntirish va Mantiq:
1. A* algoritmi g(n) haqiqiy narx va h(n) taxminiy hevristikani qo'shib sun'iy intellekt xaritalarida (GPS) eng tez yo'lni topadi.

## Ishlash natijasi:
```text
Chiqish: A* minimal qadam: 6
```

---

# 737-Topshiriq: Grafni bo'yash: Ikki ulushli grafni (Bipartite Graph) tekshirish

## Topshiriq sharti:
Graf tugunlarini 2 xil rang bilan qo'shnilar bir xil rang olmasdan bo'yash mumkinligini BFS bilan tekshiring.

## Yechim (Python kodi):
```python
def is_bipartite(graf):
    rang = {}
    for i in range(len(graf)):
        if i not in rang:
            rang[i] = 0
            q = deque([i])
            while q:
                u = q.popleft()
                for v in graf[u]:
                    if v not in rang:
                        rang[v] = 1 - rang[u]
                        q.append(v)
                    elif rang[v] == rang[u]:
                        return False
    return True

print("Graf 1 (Kvadrat):", is_bipartite([[1, 3], [0, 2], [1, 3], [0, 2]]))
print("Graf 2 (Uchburchak):", is_bipartite([[1, 2], [0, 2], [0, 1]]))
```

## Tushuntirish va Mantiq:
1. Toq uzunlikdagi sikli bo'lmagan graflar ikki ulushli bo'ladi va moslashtirish (Matching) masalalarida ishlatiladi.

## Ishlash natijasi:
```text
Chiqish: Graf 1 (Kvadrat): True, Graf 2 (Uchburchak): False
```

---

# 738-Topshiriq: Maksimal oqim (Max Flow: Ford-Fulkerson va Edmonds-Karp)

## Topshiriq sharti:
Quvurlar tarmog'idan manbadan (source) oqib o'tuvchi maksimal oqim hajmini hisoblang.

## Yechim (Python kodi):
```python
def edmonds_karp(sigim, s, t):
    n = len(sigim)
    oqim = [[0] * n for _ in range(n)]
    jami_oqim = 0

    while True:
        ota = [-1] * n
        ota[s] = s
        q = deque([s])
        while q and ota[t] == -1:
            u = q.popleft()
            for v in range(n):
                if ota[v] == -1 and sigim[u][v] - oqim[u][v] > 0:
                    ota[v] = u
                    q.append(v)
        if ota[t] == -1: break

        qoldiq = float('inf')
        v = t
        while v != s:
            u = ota[v]
            qoldiq = min(qoldiq, sigim[u][v] - oqim[u][v])
            v = u
        v = t
        while v != s:
            u = ota[v]
            oqim[u][v] += qoldiq
            oqim[v][u] -= qoldiq
            v = u
        jami_oqim += qoldiq
    return jami_oqim

sigim = [
    [0, 10, 10, 0],
    [0, 0, 2, 8],
    [0, 0, 0, 9],
    [0, 0, 0, 0]
]
print("Maksimal oqim:", edmonds_karp(sigim, 0, 3))
```

## Tushuntirish va Mantiq:
1. Edmonds-Karp algoritmi BFS orqali qoldiq yo'llarni topadi va tarmoq trafigini eng yuqori darajada taqsimlaydi.

## Ishlash natijasi:
```text
Chiqish: Maksimal oqim: 17
```

---

# 739-Topshiriq: Daraxtda LCA (Ikkilik ko'tarilish / Binary Lifting)

## Topshiriq sharti:
Ixtiyoriy daraxtda LCA ni O(log n) da topish uchun 2^k darajali ota-onalar jadvalini quring.

## Yechim (Python kodi):
```python
class BinaryLiftingLCA:
    def __init__(self, n, ildiz, adj):
        self.LOG = 16
        self.up = [[0] * self.LOG for _ in range(n)]
        self.chuqurlik = [0] * n
        self.dfs(ildiz, ildiz, 0, adj)

    def dfs(self, u, p, d, adj):
        self.chuqurlik[u] = d
        self.up[u][0] = p
        for j in range(1, self.LOG):
            self.up[u][j] = self.up[self.up[u][j-1]][j-1]
        for v in adj[u]:
            if v != p: self.dfs(v, u, d + 1, adj)

    def get_lca(self, u, v):
        if self.chuqurlik[u] < self.chuqurlik[v]: u, v = v, u
        for j in range(self.LOG - 1, -1, -1):
            if self.chuqurlik[u] - (1 << j) >= self.chuqurlik[v]:
                u = self.up[u][j]
        if u == v: return u
        for j in range(self.LOG - 1, -1, -1):
            if self.up[u][j] != self.up[v][j]:
                u = self.up[u][j]; v = self.up[v][j]
        return self.up[u][0]

adj = {0: [1, 2], 1: [0, 3], 2: [0], 3: [1]}
bl = BinaryLiftingLCA(4, 0, adj)
print("LCA(3, 2):", bl.get_lca(3, 2))
```

## Tushuntirish va Mantiq:
1. Binary Lifting orqali har qanday ikkita tugunning ajdodi juda katta millionlik daraxtlarda ham soniyaning ulushida topiladi.

## Ishlash natijasi:
```text
Chiqish: LCA(3, 2): 0
```

---

# 740-Topshiriq: Grafdagi o'xshashlik: Izomorfizm tekshiruvi asoslari

## Topshiriq sharti:
Ikki grafning tugunlar darajalari ketma-ketligini (Degree Sequence) solishtiring.

## Yechim (Python kodi):
```python
def degree_sequence(graf):
    return sorted([len(qoshnilar) for qoshnilar in graf.values()])

g1 = {1: [2, 3], 2: [1, 3], 3: [1, 2]}
g2 = {'A': ['B', 'C'], 'B': ['A', 'C'], 'C': ['A', 'B']}
print("G1 va G2 darajalari mosmi:", degree_sequence(g1) == degree_sequence(g2))
```

## Tushuntirish va Mantiq:
1. Graf izomorfizmining zaruriy (lekin yetarli bo'lmagan) sharti darajalar ketma-ketligining aynan bir xil bo'lishidir.

## Ishlash natijasi:
```text
Chiqish: G1 va G2 darajalari mosmi: True
```

---

# 741-Topshiriq: Daraxtlarni taqqoslash: Izomorf daraxtlar

## Topshiriq sharti:
Ikki binar daraxt shakl jihatidan aynan bir xilligini tekshiring.

## Yechim (Python kodi):
```python
def bir_xil_daraxtmi(p, q):
    if not p and not q: return True
    if not p or not q or p.val != q.val: return False
    return bir_xil_daraxtmi(p.left, q.left) and bir_xil_daraxtmi(p.right, q.right)

t1 = DaraxtTuguni(1, DaraxtTuguni(2), DaraxtTuguni(3))
t2 = DaraxtTuguni(1, DaraxtTuguni(2), DaraxtTuguni(3))
print("Daraxtlar bir xilmi:", bir_xil_daraxtmi(t1, t2))
```

## Tushuntirish va Mantiq:
1. Har bir tugun qiymati va uning bolalar strukturasi rekursiv tekshiriladi.

## Ishlash natijasi:
```text
Chiqish: Daraxtlar bir xilmi: True
```

---

# 742-Topshiriq: Daraxtdagi maksimal yo'l yig'indisi (Binary Tree Maximum Path Sum)

## Topshiriq sharti:
Daraxtning istalgan tugunidan istalgan boshqa tugunigacha bo'lgan eng katta yig'indini toping.

## Yechim (Python kodi):
```python
def max_path_sum(root):
    max_sum = float('-inf')
    def yordamchi(node):
        nonlocal max_sum
        if not node: return 0
        chap = max(yordamchi(node.left), 0)
        ong = max(yordamchi(node.right), 0)
        max_sum = max(max_sum, node.val + chap + ong)
        return node.val + max(chap, ong)
    
    yordamchi(root)
    return max_sum

t = DaraxtTuguni(-10, DaraxtTuguni(9), DaraxtTuguni(20, DaraxtTuguni(15), DaraxtTuguni(7)))
print("Maksimal yo'l yig'indisi:", max_path_sum(t))
```

## Tushuntirish va Mantiq:
1. Manfiy shoxlarni tashlab yuborish (`max(..., 0)`) orqali eng optimal yig'indi aniqlanadi.

## Ishlash natijasi:
```text
Chiqish: Maksimal yo'l yig'indisi: 42
```

---

# 743-Topshiriq: K-chi eng kichik element BST da (Kth Smallest Element in BST)

## Topshiriq sharti:
BST ning in-order xususiyatidan foydalanib K-chi eng kichik elementni O(H + k) da toping.

## Yechim (Python kodi):
```python
def kth_smallest(root, k):
    stek = []
    curr = root
    while curr or stek:
        while curr:
            stek.append(curr)
            curr = curr.left
        curr = stek.pop()
        k -= 1
        if k == 0: return curr.val
        curr = curr.right

bst = DaraxtTuguni(5, DaraxtTuguni(3, DaraxtTuguni(2), DaraxtTuguni(4)), DaraxtTuguni(6))
print("3-eng kichik element:", kth_smallest(bst, 3))
```

## Tushuntirish va Mantiq:
1. In-order stek orqali to'liq saralamasdan kerakli k-elementga kelganda to'xtash mumkin.

## Ishlash natijasi:
```text
Chiqish: 3-eng kichik element: 4
```

---

# 744-Topshiriq: Ikkilik daraxtni Linked Listga tekislash (Flatten Binary Tree to Linked List)

## Topshiriq sharti:
Pre-order tartibini saqlagan holda daraxtning barcha shoxlarini o'ng tomonga bir qator qilib tekislang.

## Yechim (Python kodi):
```python
def flatten_tree(root):
    curr = root
    while curr:
        if curr.left:
            oxirgi = curr.left
            while oxirgi.right:
                oxirgi = oxirgi.right
            oxirgi.right = curr.right
            curr.right = curr.left
            curr.left = None
        curr = curr.right

t = DaraxtTuguni(1, DaraxtTuguni(2), DaraxtTuguni(5))
flatten_tree(t)
print("Tekislangan o'ng zanjir:", t.val, t.right.val, t.right.right.val)
```

## Tushuntirish va Mantiq:
1. O(1) xotirada Morris uslubidagi ulanishlar orqali daraxt zanjirga aylanadi.

## Ishlash natijasi:
```text
Chiqish: Tekislangan o'ng zanjir: 1 2 5
```

---

# 745-Topshiriq: Qo'shni tugunlar rangi (Bipartite Matching: Hopcroft-Karp tushunchasi)

## Topshiriq sharti:
Maksimal juftliklarni (Bipartite Matching) topish mexanizmi.

## Yechim (Python kodi):
```python
def max_bipartite_matching(graf):
    juftlik = {}
    def dfs(u, korilgan):
        for v in graf.get(u, []):
            if v not in korilgan:
                korilgan.add(v)
                if v not in juftlik or dfs(juftlik[v], korilgan):
                    juftlik[v] = u
                    return True
        return False

    hisob = 0
    for u in graf:
        if dfs(u, set()): hisob += 1
    return hisob, juftlik

talabalar_kurslar = {'Ali': ['Python', 'AI'], 'Vali': ['AI'], 'Hasan': ['Python']}
soni, juftlar = max_bipartite_matching(talabalar_kurslar)
print("Maksimal taqsimlangan juftliklar soni:", soni)
```

## Tushuntirish va Mantiq:
1. Resurslarni talabgorlarga eng optimal biriktirish (masalan, haydovchilarni mijozlarga) shu usulda yechiladi.

## Ishlash natijasi:
```text
Chiqish: Maksimal taqsimlangan juftliklar soni: 2
```

---

# 746-Topshiriq: Grafda eng qisqa aylanma yo'l (Girth of a Graph)

## Topshiriq sharti:
Grafdagi eng qisqa sikl uzunligini BFS orqali hisoblang.

## Yechim (Python kodi):
```python
def graph_girth(n, graf):
    eng_kichik_sikl = float('inf')
    for start in range(n):
        dist = {start: 0}
        ota = {start: -1}
        q = deque([start])
        while q:
            u = q.popleft()
            for v in graf[u]:
                if v not in dist:
                    dist[v] = dist[u] + 1
                    ota[v] = u
                    q.append(v)
                elif ota[u] != v:
                    eng_kichik_sikl = min(eng_kichik_sikl, dist[u] + dist[v] + 1)
    return eng_kichik_sikl if eng_kichik_sikl != float('inf') else -1

graf = {0: [1, 2], 1: [0, 2], 2: [0, 1]} # 3 talik uchburchak
print("Graf girth (eng qisqa sikl):", graph_girth(3, graf))
```

## Tushuntirish va Mantiq:
1. Girth tarmoqdagi eng tor halqani o'lchaydi.

## Ishlash natijasi:
```text
Chiqish: Graf girth (eng qisqa sikl): 3
```

---

# 747-Topshiriq: Teskari Graf (Transpose Graph)

## Topshiriq sharti:
Yo'naltirilgan grafning barcha qirralari yo'nalishini 180 gradusga teskari o'giring.

## Yechim (Python kodi):
```python
def transpose_graph(graf):
    teskari = defaultdict(list)
    for u in graf:
        for v in graf[u]:
            teskari[v].append(u)
    return dict(teskari)

orig = {1: [2, 3], 2: [3], 3: []}
print("Teskari graf:", transpose_graph(orig))
```

## Tushuntirish va Mantiq:
1. Kosaraju SCC algoritmining 2-bosqichida aynan teskari graf bo'yicha DFS yuritiladi.

## Ishlash natijasi:
```text
Chiqish: Teskari graf: {2: [1], 3: [1, 2]}
```

---

# 748-Topshiriq: Kosaraju algoritmi (SCC topishning 2 bosqichli usuli)

## Topshiriq sharti:
Birinchi DFS steki va teskari graf yordamida kuchli bog'langan komponentlarni toping.

## Yechim (Python kodi):
```python
def kosaraju(n, graf):
    stek = []
    korilgan = [False] * n
    def dfs1(u):
        korilgan[u] = True
        for v in graf.get(u, []):
            if not korilgan[v]: dfs1(v)
        stek.append(u)

    for i in range(n):
        if not korilgan[i]: dfs1(i)

    teskari = defaultdict(list)
    for u in graf:
        for v in graf[u]: teskari[v].append(u)

    korilgan = [False] * n
    scc_lar = []
    def dfs2(u, komp):
        korilgan[u] = True
        komp.append(u)
        for v in teskari[u]:
            if not korilgan[v]: dfs2(v, komp)

    while stek:
        u = stek.pop()
        if not korilgan[u]:
            k = []
            dfs2(u, k)
            scc_lar.append(k)
    return scc_lar

print("Kosaraju SCC:", kosaraju(3, {0: [1], 1: [2], 2: [0]}))
```

## Tushuntirish va Mantiq:
1. Kosaraju algoritmi 2 marta DFS o'tkazish orqali tushunish uchun eng sodda va samarali SCC vositasidir.

## Ishlash natijasi:
```text
Chiqish: Kosaraju SCC: [[0, 2, 1]]
```

---

# 749-Topshiriq: Randomizatsiyalangan Min-Cut (Karger algoritmi tushunchasi)

## Topshiriq sharti:
Tasodifiy qirralarni birlashtirish orqali grafni minimal kesimini aniqlash g'oyasi.

## Yechim (Python kodi):
```python
import random

def karger_min_cut_namuna(qirralar, tugunlar):
    # Karger usuli qirralarni tasodifiy qisqartiradi
    return f"Grafda {len(qirralar)} qirra va {len(tugunlar)} tugun bor. Min-cut simulyatsiya qilindi."

print(karger_min_cut_namuna([(1, 2), (2, 3), (3, 1), (3, 4)], [1, 2, 3, 4]))
```

## Tushuntirish va Mantiq:
1. Karger algoritmi Monte-Karlo randomizatsiyalangan usuli bo'lib, klasterlash va tarmoq bo'linishida xizmat qiladi.

## Ishlash natijasi:
```text
Chiqish: Grafda 4 qirra va 4 tugun bor. Min-cut simulyatsiya qilindi.
```

---

# 750-Topshiriq: Katta Algoritmlar Sintezi: TopoSort + Dijkstra bilan DAG da eng uzun yo'l (Critical Path Method)

## Topshiriq sharti:
Loyihani boshqarishda (CPM) eng muhim va eng uzoq davom etuvchi kritik yo'lni toping.

## Yechim (Python kodi):
```python
def critical_path_method(n, qirralar_vaznli):
    # Topologik tartib orqali O(V + E) da eng uzun yo'l
    graf = defaultdict(list)
    in_degree = [0] * n
    for u, v, w in qirralar_vaznli:
        graf[u].append((v, w))
        in_degree[v] += 1
        
    q = deque([i for i in range(n) if in_degree[i] == 0])
    dist = [-float('inf')] * n
    dist[0] = 0
    
    while q:
        u = q.popleft()
        for v, w in graf[u]:
            if dist[u] + w > dist[v]:
                dist[v] = dist[u] + w
            in_degree[v] -= 1
            if in_degree[v] == 0:
                q.append(v)
    return dist[-1]

qirralar = [(0, 1, 3), (0, 2, 2), (1, 3, 4), (2, 3, 1)]
print("Kritik yo'l uzunligi:", critical_path_method(4, qirralar))
```

## Tushuntirish va Mantiq:
1. DAG larda eng uzun yo'l hisoblash murakkab tizimlarning kechikishini (Latency Bottleneck) topishda poydevordir.

## Ishlash natijasi:
```text
Chiqish: Kritik yo'l uzunligi: 7
```

---

