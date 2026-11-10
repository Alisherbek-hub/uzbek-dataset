# Khorazmiy AI: PHP - Modul 22
## Mavzu: Ilg'or Algoritmlar: Graflar, Segment Trees, Fenwick va Trie tuzilmalari

### Topshiriq #1051: Graflarda eng qisqa yo'lni topish (Dijkstra algoritmi)
**Tavsif:** Logistika tizimlarida serverlararo ma'lumot uzatishning eng maqbul yo'nalishini aniqlash.
**Talablar:** $O(E \log V)$ murakkablik, xotira xavfsizligi va `SplPriorityQueue` dan foydalanish.
**Yechim (PHP):**
```php
function dijkstra($graph, $start) {
    $distances = array_fill_keys(array_keys($graph), INF);
    $distances[$start] = 0;
    $pq = new SplPriorityQueue();
    $pq->insert($start, 0);

    while (!$pq->isEmpty()) {
        $u = $pq->extract();
        foreach ($graph[$u] as $v => $weight) {
            if ($distances[$u] + $weight < $distances[$v]) {
                $distances[$v] = $distances[$u] + $weight;
                $pq->insert($v, -$distances[$v]);
            }
        }
    }
    return $distances;
}
```
**Tushuntirish:** `SplPriorityQueue` PHP'ning ichki optimallashtirilgan tuzilmasi bo'lib, katta graflarda massivni qayta saralashdan ko'ra samaraliroq ishlaydi.

---

### Topshiriq #1052: Segment Tree yordamida diapazon yig'indisini hisoblash
**Tavsif:** Moliya tizimlarida ma'lum vaqt oralig'idagi tranzaksiyalar yig'indisini real vaqtda yangilash.
**Talablar:** $O(\log N)$ vaqt murakkabligi, ma'lumotlar yaxlitligi.
**Yechim (PHP):**
```php
class SegmentTree {
    private $tree;
    private $n;
    public function __construct($data) {
        $this->n = count($data);
        $this->tree = array_fill(0, 2 * $this->n, 0);
        for ($i = 0; $i < $this->n; $i++) $this->tree[$this->n + $i] = $data[$i];
        for ($i = $this->n - 1; $i > 0; $i--) $this->tree[$i] = $this->tree[2*$i] + $this->tree[2*$i+1];
    }
    public function update($i, $val) {
        for ($this->tree[$i += $this->n] = $val; $i > 1; $i >>= 1) 
            $this->tree[$i >> 1] = $this->tree[$i] + $this->tree[$i^1];
    }
}
```
**Tushuntirish:** Iterativ Segment Tree rekursiv yondashuvga qaraganda xotirani tejaydi va stack overflow xavfini yo'q qiladi.

---

### Topshiriq #1053: Fenwick Tree (Binary Indexed Tree)
**Tavsif:** Katta hajmdagi log fayllarida kümülatif chastotalarni hisoblash.
**Talablar:** Minimal xotira sarfi, $O(\log N)$ operatsiyalar.
**Yechim (PHP):**
```php
class FenwickTree {
    private $tree;
    public function __construct($n) { $this->tree = array_fill(0, $n + 1, 0); }
    public function update($i, $delta) {
        for (; $i < count($this->tree); $i += $i & -$i) $this->tree[$i] += $delta;
    }
    public function query($i) {
        $sum = 0;
        for (; $i > 0; $i -= $i & -$i) $sum += $this->tree[$i];
        return $sum;
    }
}
```
**Tushuntirish:** Fenwick Tree segment tree'ga qaraganda ixchamroq va bitwise operatsiyalar tufayli juda tez ishlaydi.

---

### Topshiriq #1054: Trie (Prefix Tree) implementatsiyasi
**Tavsif:** Foydalanuvchi so'rovlarini avtomatik to'ldirish (autocomplete) tizimi.
**Talablar:** String qidiruvida $O(L)$ murakkablik (L - so'z uzunligi).
**Yechim (PHP):**
```php
class TrieNode {
    public $children = [];
    public $isEndOfWord = false;
}
class Trie {
    private $root;
    public function __construct() { $this->root = new TrieNode(); }
    public function insert($word) {
        $curr = $this->root;
        foreach (str_split($word) as $char) {
            if (!isset($curr->children[$char])) $curr->children[$char] = new TrieNode();
            $curr = $curr->children[$char];
        }
        $curr->isEndOfWord = true;
    }
}
```
**Tushuntirish:** Trie tuzilmasi lug'at bazalarida takrorlanuvchi prefikslarni saqlashni optimallashtiradi, bu esa xotirani tejaydi.

---

### Topshiriq #1055: Graflarda sikllarni aniqlash (DFS)
**Tavsif:** Mikroxizmatlar arxitekturasida bog'liqliklar (dependencies) orasida halqali bog'liqlik (circular dependency) yo'qligini tekshirish.
**Talablar:** Rekursiv xavfsizlik, $O(V+E)$ murakkablik.
**Yechim (PHP):**
```php
function hasCycle($graph, $node, &$visited, &$recStack) {
    $visited[$node] = true;
    $recStack[$node] = true;
    foreach ($graph[$node] as $neighbor) {
        if (!$visited[$neighbor] && hasCycle($graph, $neighbor, $visited, $recStack)) return true;
        if (isset($recStack[$neighbor])) return true;
    }
    unset($recStack[$node]);
    return false;
}
```
**Tushuntirish:** `recStack` (rekursiya steki) orqali biz joriy yo'lda qayta tashrif buyurilgan tugunni aniqlaymiz, bu siklni aniqlashning eng ishonchli usuli.

---

### Topshiriq #1056: Topological Sort (Kahn algoritmi)
**Tavsif:** Vazifalarni bajarish tartibini (task scheduling) aniqlash.
**Talablar:** Kiruvchi darajalarni (in-degree) hisoblash orqali tartiblash.
**Yechim (PHP):**
```php
function topologicalSort($graph, $inDegree) {
    $queue = new SplQueue();
    foreach ($inDegree as $node => $degree) if ($degree === 0) $queue->enqueue($node);
    $result = [];
    while (!$queue->isEmpty()) {
        $u = $queue->dequeue();
        $result[] = $u;
        foreach ($graph[$u] as $v) {
            if (--$inDegree[$v] === 0) $queue->enqueue($v);
        }
    }
    return $result;
}
```
**Tushuntirish:** Kahn algoritmi BFS asosida ishlaydi va DAG (Directed Acyclic Graph) uchun eng samarali yechimdir.

---

### Topshiriq #1057: Disjoint Set Union (DSU)
**Tavsif:** Tarmoq segmentlarini birlashtirish va ularning bog'liqligini tezkor tekshirish.
**Talablar:** Path compression va union by rank texnikalari.
**Yechim (PHP):**
```php
class DSU {
    private $parent;
    public function __construct($n) { $this->parent = range(0, $n); }
    public function find($i) {
        if ($this->parent[$i] == $i) return $i;
        return $this->parent[$i] = $this->find($this->parent[$i]);
    }
    public function union($i, $j) {
        $rootI = $this->find($i);
        $rootJ = $this->find($j);
        if ($rootI != $rootJ) $this->parent[$rootI] = $rootJ;
    }
}
```
**Tushuntirish:** `find` funksiyasidagi path compression operatsiyasi daraxt balandligini doimiy ravishda pasaytirib, deyarli $O(1)$ tezlikni ta'minlaydi.

---

### Topshiriq #1058: Kruskal algoritmi (MST)
**Tavsif:** Minimal xarajat bilan serverlar tarmog'ini ulash.
**Talablar:** DSU dan foydalanish, qirralarni vazn bo'yicha saralash.
**Yechim (PHP):**
```php
function kruskal($edges, $n) {
    usort($edges, fn($a, $b) => $a[2] <=> $b[2]);
    $dsu = new DSU($n);
    $mst = [];
    foreach ($edges as $edge) {
        if ($dsu->find($edge[0]) != $dsu->find($edge[1])) {
            $dsu->union($edge[0], $edge[1]);
            $mst[] = $edge;
        }
    }
    return $mst;
}
```
**Tushuntirish:** Kruskal algoritmi tarmoq infratuzilmasini loyihalashda eng kam resurs sarflab, barcha tugunlarni bog'lash uchun eng yaxshi tanlovdir.

---

### Topshiriq #1059: Trie bilan so'zlar sonini hisoblash
**Tavsif:** Katta matnlar ichida ma'lum prefiksga ega so'zlar sonini tezkor aniqlash.
**Talablar:** Trie tugunlarida `count` atributini saqlash.
**Yechim (PHP):**
```php
class TrieNode {
    public $children = [];
    public $count = 0; // Prefiks orqali o'tuvchi so'zlar soni
}
// insert funksiyasida har bir tugun uchun $curr->count++ qo'shiladi
function countPrefix($root, $prefix) {
    $curr = $root;
    foreach (str_split($prefix) as $char) {
        if (!isset($curr->children[$char])) return 0;
        $curr = $curr->children[$char];
    }
    return $curr->count;
}
```
**Tushuntirish:** Har bir tugunda `count` saqlash qidiruv vaqtini $O(1)$ ga yaqinlashtiradi, chunki natija oldindan hisoblab qo'yilgan bo'ladi.

---

### Topshiriq #1060: Segment Tree (Lazy Propagation)
**Tavsif:** Diapazon bo'yicha yangilash (range update) operatsiyalarini optimallashtirish.
**Talablar:** $O(\log N)$ murakkablik, "Lazy" qiymatlarni saqlash.
**Yechim (PHP):**
```php
// Lazy propagation uchun qo'shimcha $lazy massivi ishlatiladi
function updateRange(&$tree, &$lazy, $node, $start, $end, $l, $r, $val) {
    if ($lazy[$node] != 0) {
        $tree[$node] += ($end - $start + 1) * $lazy[$node];
        if ($start != $end) {
            $lazy[2*$node] += $lazy[$node];
            $lazy[2*$node+1] += $lazy[$node];
        }
        $lazy[$node] = 0;
    }
    // ... qolgan mantiq diapazonni yangilash uchun
}
```
**Tushuntirish:** Lazy propagation operatsiyalarni kechiktirish orqali katta diapazonlarni bir vaqtning o'zida yangilash imkonini beradi, bu esa tizim unumdorligini keskin oshiradi.

---

### Topshiriq #1061: Trie yordamida avtomatik to'ldirish tizimi
**Tavsif:** Katta hajmdagi PHP funksiyalar nomlari bazasidan prefiks bo'yicha qidiruvni tezlashtirish.
**Talablar:** Qidiruv vaqti O(L) bo'lishi kerak (L - qidirilayotgan so'z uzunligi).
**Yechim (PHP):**
```php
class TrieNode {
    public $children = [];
    public $isEndOfWord = false;
}

class Trie {
    private $root;
    public function __construct() { $this->root = new TrieNode(); }

    public function insert($word) {
        $curr = $this->root;
        foreach (str_split($word) as $char) {
            if (!isset($curr->children[$char])) $curr->children[$char] = new TrieNode();
            $curr = $curr->children[$char];
        }
        $curr->isEndOfWord = true;
    }
}
```
**Tushuntirish:** Trie tuzilmasi satrli qidiruvlarda hash-mapdan ko'ra xotira tejamkor va prefiks qidiruv uchun optimal hisoblanadi.

### Topshiriq #1062: Fenwick Tree yordamida reytinglar yig'indisi
**Tavsif:** Foydalanuvchilarning dinamik o'zgaruvchan reytinglari yig'indisini hisoblash.
**Talablar:** Yangilash va so'rovlar O(log N) murakkablikda bo'lishi shart.
**Yechim (PHP):**
```php
class FenwickTree {
    private $tree = [];
    public function update($i, $delta, $n) {
        for (; $i <= $n; $i += $i & -$i) $this->tree[$i] = ($this->tree[$i] ?? 0) + $delta;
    }
    public function query($i) {
        $sum = 0;
        for (; $i > 0; $i -= $i & -$i) $sum += $this->tree[$i] ?? 0;
        return $sum;
    }
}
```
**Tushuntirish:** Fenwick Tree (Binary Indexed Tree) massivdagi prefiks yig'indilarni juda tez hisoblash imkonini beradi.

### Topshiriq #1063: Segment Tree bilan intervaldagi maksimal qiymat
**Tavsif:** Server yuklanish statistikasi (interval) ichidagi eng yuqori qiymatni topish.
**Talablar:** O(log N) vaqtda interval so'rovlarini bajarish.
**Yechim (PHP):**
```php
class SegmentTree {
    private $tree = [];
    public function build($arr, $node, $start, $end) {
        if ($start == $end) $this->tree[$node] = $arr[$start];
        else {
            $mid = (int)(($start + $end) / 2);
            $this->build($arr, 2*$node, $start, $mid);
            $this->build($arr, 2*$node+1, $mid+1, $end);
            $this->tree[$node] = max($this->tree[2*$node], $this->tree[2*$node+1]);
        }
    }
}
```
**Tushuntirish:** Segment Tree statik ma'lumotlar ustida interval so'rovlarini bajarish uchun eng samarali tuzilmadir.

### Topshiriq #1064: Grafda eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Tarmoq tugunlari o'rtasidagi eng kam kechikishli marshrutni aniqlash.
**Talablar:** Og'irligi manfiy bo'lmagan qirralar uchun optimallash.
**Yechim (PHP):**
```php
function dijkstra($graph, $start) {
    $dist = array_fill_keys(array_keys($graph), INF);
    $dist[$start] = 0;
    $pq = new SplPriorityQueue();
    $pq->insert($start, 0);
    while (!$pq->isEmpty()) {
        $u = $pq->extract();
        foreach ($graph[$u] as $v => $weight) {
            if ($dist[$u] + $weight < $dist[$v]) {
                $dist[$v] = $dist[$u] + $weight;
                $pq->insert($v, -$dist[$v]);
            }
        }
    }
    return $dist;
}
```
**Tushuntirish:** `SplPriorityQueue` dan foydalanish Dijkstra algoritmini PHPda O(E log V) murakkablikda ishlashini ta'minlaydi.

### Topshiriq #1065: Topologik tartiblash (Kahn algoritmi)
**Tavsif:** PHP paketlarining bog'liqliklarini (dependencies) to'g'ri o'rnatish tartibini aniqlash.
**Talablar:** Acyclic (tsiklsiz) graf bo'lishi shart.
**Yechim (PHP):**
```php
function topologicalSort($graph, $inDegree) {
    $queue = new SplQueue();
    foreach ($inDegree as $node => $deg) if ($deg === 0) $queue->enqueue($node);
    $result = [];
    while (!$queue->isEmpty()) {
        $u = $queue->dequeue();
        $result[] = $u;
        foreach ($graph[$u] as $v) if (--$inDegree[$v] === 0) $queue->enqueue($v);
    }
    return $result;
}
```
**Tushuntirish:** Kahn algoritmi bog'liqliklar zanjirini aniqlashda eng ishonchli yondashuvdir.

### Topshiriq #1066: Grafda tsiklni aniqlash (DFS)
**Tavsif:** Tizimdagi o'zaro bog'liqliklarda yuzaga kelishi mumkin bo'lgan "deadlock"larni aniqlash.
**Talablar:** Rekursiv yondashuv va xotira nazorati.
**Yechim (PHP):**
```php
function hasCycle($node, $graph, &$visited, &$recStack) {
    $visited[$node] = true;
    $recStack[$node] = true;
    foreach ($graph[$node] as $neighbor) {
        if (!isset($visited[$neighbor]) && hasCycle($neighbor, $graph, $visited, $recStack)) return true;
        elseif (isset($recStack[$neighbor])) return true;
    }
    unset($recStack[$node]);
    return false;
}
```
**Tushuntirish:** `recStack` (rekursiya steki) yordamida yo'naltirilgan grafdagi tsikllarni O(V+E) vaqtda aniqlash mumkin.

### Topshiriq #1067: Fenwick Tree bilan 2D maydonni yangilash
**Tavsif:** 2D koordinata tizimidagi (masalan, ekran pikseli) qiymatlarni tezkor yangilash.
**Talablar:** 2D Fenwick Tree (Binary Indexed Tree) implementatsiyasi.
**Yechim (PHP):**
```php
class FenwickTree2D {
    private $tree = [];
    public function update($x, $y, $val, $n) {
        for ($i = $x; $i <= $n; $i += $i & -$i)
            for ($j = $y; $j <= $n; $j += $j & -$j)
                $this->tree[$i][$j] = ($this->tree[$i][$j] ?? 0) + $val;
    }
}
```
**Tushuntirish:** 2D Fenwick Tree matritsali ma'lumotlar ustida qator va ustun yig'indilarini hisoblashda juda tezkor.

### Topshiriq #1068: Trie bilan IP manzillar filtri
**Tavsif:** Qora ro'yxatdagi IP manzillar prefikslarini tezkor tekshirish.
**Talablar:** Bit darajasida qidiruvni amalga oshirish.
**Yechim (PHP):**
```php
// IP ni bitlar ketma-ketligiga aylantirib Trie ga joylash
function insertIP($root, $ipBinary) {
    $curr = $root;
    foreach (str_split($ipBinary) as $bit) {
        if (!isset($curr[$bit])) $curr[$bit] = [];
        $curr = &$curr[$bit];
    }
    $curr['#'] = true; // Tugash belgisi
}
```
**Tushuntirish:** IP manzillarni Trie daraxtiga bitma-bit joylash, CIDR bloklarini tekshirishni O(32) vaqtda bajaradi.

### Topshiriq #1069: Segment Tree (Lazy Propagation)
**Tavsif:** Katta massivdagi intervalni bir vaqtda yangilash (Range Update).
**Talablar:** Yangilash vaqti O(log N) bo'lishi kerak.
**Yechim (PHP):**
```php
// Lazy propagation - kechiktirilgan yangilash texnikasi
function updateRange($node, $start, $end, $l, $r, $val) {
    if ($this->lazy[$node] != 0) {
        $this->tree[$node] += ($end - $start + 1) * $this->lazy[$node];
        if ($start != $end) {
            $this->lazy[2*$node] += $this->lazy[$node];
            $this->lazy[2*$node+1] += $this->lazy[$node];
        }
        $this->lazy[$node] = 0;
    }
    // ... qolgan mantiq
}
```
**Tushuntirish:** Lazy propagation massivning katta qismini bir vaqtda yangilashda samaradorlikni keskin oshiradi.

### Topshiriq #1070: Grafda bog'langan komponentlarni topish (BFS)
**Tavsif:** Tarmoq ichidagi izolyatsiya qilingan klasterlarni aniqlash.
**Talablar:** O(V+E) murakkablik va xotira samaradorligi.
**Yechim (PHP):**
```php
function findComponents($graph) {
    $visited = [];
    $count = 0;
    foreach (array_keys($graph) as $node) {
        if (!isset($visited[$node])) {
            $count++;
            $queue = new SplQueue();
            $queue->enqueue($node);
            $visited[$node] = true;
            while (!$queue->isEmpty()) {
                $u = $queue->dequeue();
                foreach ($graph[$u] as $v) if (!isset($visited[$v])) { $visited[$v] = true; $queue->enqueue($v); }
            }
        }
    }
    return $count;
}
```
**Tushuntirish:** BFS (Breadth-First Search) yordamida grafdagi barcha bog'langan komponentlarni aniqlash tizim xavfsizligini tekshirishda muhimdir.

---

### Topshiriq #1071: Graflarda eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Logistika tizimlarida serverlararo ma'lumot uzatish marshrutini optimallashtirish.
**Talablar:** O(E log V) murakkablik, xotira xavfsizligi uchun `SplPriorityQueue` dan foydalanish.
**Yechim (PHP):**
```php
function dijkstra($graph, $start) {
    $distances = array_fill_keys(array_keys($graph), INF);
    $distances[$start] = 0;
    $pq = new SplPriorityQueue();
    $pq->insert($start, 0);

    while (!$pq->isEmpty()) {
        $u = $pq->extract();
        foreach ($graph[$u] as $v => $weight) {
            if ($distances[$u] + $weight < $distances[$v]) {
                $distances[$v] = $distances[$u] + $weight;
                $pq->insert($v, -$distances[$v]); // Min-heap uchun manfiy qiymat
            }
        }
    }
    return $distances;
}
```
**Tushuntirish:** `SplPriorityQueue` PHP'ning ichki kutubxonasi bo'lib, katta hajmdagi graflarda massivlarni qayta saralashdan ko'ra tezroq ishlaydi.

### Topshiriq #1072: Segment Tree yordamida diapazon yig'indisi
**Tavsif:** Moliya tizimlarida real vaqt rejimida tranzaksiyalar yig'indisini hisoblash.
**Talablar:** O(log N) yangilash va so'rov vaqti.
**Yechim (PHP):**
```php
class SegmentTree {
    private $tree = [];
    private $n;

    public function __construct($data) {
        $this->n = count($data);
        $this->tree = array_fill(0, 2 * $this->n, 0);
        for ($i = 0; $i < $this->n; $i++) $this->tree[$this->n + $i] = $data[$i];
        for ($i = $this->n - 1; $i > 0; $i--) $this->tree[$i] = $this->tree[2 * $i] + $this->tree[2 * $i + 1];
    }

    public function query($l, $r) {
        $res = 0;
        for ($l += $this->n, $r += $this->n; $l < $r; $l >>= 1, $r >>= 1) {
            if ($l & 1) $res += $this->tree[$l++];
            if ($r & 1) $res += $this->tree[--$r];
        }
        return $res;
    }
}
```
**Tushuntirish:** Iterativ Segment Tree rekursiv yondashuvga qaraganda xotirani tejaydi va stack overflow xavfini yo'qotadi.

### Topshiriq #1073: Fenwick Tree (Binary Indexed Tree)
**Tavsif:** Katta hajmdagi log fayllarida chastotani hisoblash.
**Talablar:** O(log N) murakkablik, minimal xotira sarfi.
**Yechim (PHP):**
```php
class FenwickTree {
    private $tree;
    public function __construct($n) { $this->tree = array_fill(0, $n + 1, 0); }
    public function update($i, $delta) {
        for (; $i < count($this->tree); $i += $i & -$i) $this->tree[$i] += $delta;
    }
    public function query($i) {
        $sum = 0;
        for (; $i > 0; $i -= $i & -$i) $sum += $this->tree[$i];
        return $sum;
    }
}
```
**Tushuntirish:** Fenwick Tree segment tree'ga qaraganda kamroq xotira talab qiladi va bitwise operatsiyalar tufayli juda tez ishlaydi.

### Topshiriq #1074: Trie (Prefix Tree) implementatsiyasi
**Tavsif:** Foydalanuvchi so'rovlari uchun "avtomatik to'ldirish" (autocomplete) tizimi.
**Talablar:** Xotirani samarali boshqarish, o'zgaruvchan uzunlikdagi stringlar bilan ishlash.
**Yechim (PHP):**
```php
class TrieNode {
    public $children = [];
    public $isEndOfWord = false;
}

class Trie {
    private $root;
    public function __construct() { $this->root = new TrieNode(); }
    public function insert($word) {
        $curr = $this->root;
        foreach (str_split($word) as $char) {
            if (!isset($curr->children[$char])) $curr->children[$char] = new TrieNode();
            $curr = $curr->children[$char];
        }
        $curr->isEndOfWord = true;
    }
}
```
**Tushuntirish:** Trie tuzilmasi so'zlarni qidirishda O(L) (L - so'z uzunligi) vaqt sarflaydi, bu esa lug'at hajmidan qat'iy nazar tezlikni ta'minlaydi.

### Topshiriq #1075: Graflarda siklni aniqlash (DFS)
**Tavsif:** Mikroxizmatlar bog'liqliklarida (dependency) "deadlock" holatlarini oldini olish.
**Talablar:** Rekursiv chuqurlikni nazorat qilish.
**Yechim (PHP):**
```php
function hasCycle($graph, $node, &$visited, &$recStack) {
    $visited[$node] = true;
    $recStack[$node] = true;
    foreach ($graph[$node] as $neighbor) {
        if (!isset($visited[$neighbor]) && hasCycle($graph, $neighbor, $visited, $recStack)) return true;
        if (isset($recStack[$neighbor])) return true;
    }
    unset($recStack[$node]);
    return false;
}
```
**Tushuntirish:** `recStack` (recursion stack) orqali biz joriy yo'lda tugun qayta uchraganini aniqlaymiz, bu siklni aniqlashning eng ishonchli usuli.

### Topshiriq #1076: Topological Sort (Kahn algoritmi)
**Tavsif:** Vazifalarni bajarish tartibini (task scheduling) belgilash.
**Talablar:** O(V+E) vaqt murakkabligi.
**Yechim (PHP):**
```php
function topologicalSort($graph, $inDegree) {
    $queue = new SplQueue();
    foreach ($inDegree as $node => $degree) if ($degree === 0) $queue->enqueue($node);
    $result = [];
    while (!$queue->isEmpty()) {
        $u = $queue->dequeue();
        $result[] = $u;
        foreach ($graph[$u] as $v) {
            if (--$inDegree[$v] === 0) $queue->enqueue($v);
        }
    }
    return $result;
}
```
**Tushuntirish:** Kahn algoritmi graflardagi bog'liqliklar ketma-ketligini aniqlash uchun eng samarali yondashuvdir.

### Topshiriq #1077: Tarjan algoritmi (Strongly Connected Components)
**Tavsif:** Ijtimoiy tarmoqlarda o'zaro bog'liq guruhlarni aniqlash.
**Talablar:** Bir marta o'tish (single pass) bilan aniqlash.
**Yechim (PHP):**
```php
// Tarjan algoritmi uchun yordamchi o'zgaruvchilar
$index = 0; $stack = []; $indices = []; $lowlink = []; $onStack = [];

function strongConnect($v, $graph) {
    global $index, $stack, $indices, $lowlink, $onStack;
    $indices[$v] = $lowlink[$v] = $index++;
    $stack[] = $v; $onStack[$v] = true;

    foreach ($graph[$v] as $w) {
        if (!isset($indices[$w])) {
            strongConnect($w, $graph);
            $lowlink[$v] = min($lowlink[$v], $lowlink[$w]);
        } elseif ($onStack[$w]) {
            $lowlink[$v] = min($lowlink[$v], $indices[$w]);
        }
    }
}
```
**Tushuntirish:** Tarjan algoritmi graflardagi kuchli bog'langan komponentlarni O(V+E) vaqtda topadi, bu katta ma'lumotlar bazalarida klasterlash uchun juda muhim.

### Topshiriq #1078: Minimum Spanning Tree (Kruskal)
**Tavsif:** Tarmoq infratuzilmasini qurishda minimal xarajatli kabel yotqizish.
**Talablar:** Disjoint Set Union (DSU) tuzilmasidan foydalanish.
**Yechim (PHP):**
```php
class DSU {
    private $parent;
    public function __construct($n) { $this->parent = range(0, $n); }
    public function find($i) { return ($this->parent[$i] == $i) ? $i : ($this->parent[$i] = $this->find($this->parent[$i])); }
    public function union($i, $j) { $this->parent[$this->find($i)] = $this->find($j); }
}
```
**Tushuntirish:** DSU orqali biz "path compression" texnikasini qo'llaymiz, bu esa operatsiyalarni deyarli doimiy (constant) vaqtda bajarishga imkon beradi.

### Topshiriq #1079: Longest Common Prefix (Trie yordamida)
**Tavsif:** Katta hajmdagi fayl nomlari orasida umumiy prefiksni topish.
**Talablar:** Xotirani tejash va tezkor qidiruv.
**Yechim (PHP):**
```php
function findLCP($words) {
    $root = new TrieNode();
    foreach ($words as $word) {
        $curr = $root;
        foreach (str_split($word) as $char) {
            if (!isset($curr->children[$char])) $curr->children[$char] = new TrieNode();
            $curr = $curr->children[$char];
        }
    }
    // Trie bo'ylab faqat bitta farzandi bor tugunlarni yurib chiqish
    // ... (qisqartirilgan mantiq)
}
```
**Tushuntirish:** Trie tuzilmasi prefikslarni ierarxik saqlaydi, bu esa stringlarni solishtirishdan ko'ra samaraliroqdir.

### Topshiriq #1080: Range Minimum Query (Sparse Table)
**Tavsif:** Statik ma'lumotlar to'plamida eng kichik qiymatni tezkor topish.
**Talablar:** O(1) so'rov vaqti.
**Yechim (PHP):**
```php
class SparseTable {
    private $st = [];
    public function __construct($arr) {
        $n = count($arr);
        $k = floor(log($n, 2));
        for ($i = 0; $i < $n; $i++) $this->st[$i][0] = $arr[$i];
        for ($j = 1; $j <= $k; $j++)
            for ($i = 0; $i + (1 << $j) <= $n; $i++)
                $this->st[$i][$j] = min($this->st[$i][$j-1], $this->st[$i + (1 << ($j-1))][$j-1]);
    }
    public function query($l, $r) {
        $j = floor(log($r - $l + 1, 2));
        return min($this->st[$l][$j], $this->st[$r - (1 << $j) + 1][$j]);
    }
}
```
**Tushuntirish:** Sparse Table statik massivlar uchun RMQ muammosini O(1) vaqtda yechadi, bu esa real vaqtda tahlil tizimlari uchun juda muhim.

---

### Topshiriq #1081: Trie yordamida avtomatik to'ldirish (Autocomplete) tizimi
**Tavsif:** Katta hajmdagi foydalanuvchi so'rovlarini tezkor qidirish va taklif qilish uchun Trie (Prefix Tree) ma'lumotlar tuzilmasini implementatsiya qilish.
**Talablar:** Qidiruv tezligi O(L) bo'lishi kerak (L - so'z uzunligi). Xotira samaradorligi muhim.
**Yechim (PHP):**
```php
class TrieNode {
    public $children = [];
    public $isEndOfWord = false;
}

class AutocompleteTrie {
    private $root;

    public function __construct() { $this->root = new TrieNode(); }

    public function insert(string $word) {
        $curr = $this->root;
        foreach (str_split($word) as $char) {
            if (!isset($curr->children[$char])) $curr->children[$char] = new TrieNode();
            $curr = $curr->children[$char];
        }
        $curr->isEndOfWord = true;
    }

    public function searchPrefix(string $prefix): array {
        $curr = $this->root;
        foreach (str_split($prefix) as $char) {
            if (!isset($curr->children[$char])) return [];
            $curr = $curr->children[$char];
        }
        return $this->collectAll($curr, $prefix);
    }

    private function collectAll($node, $prefix): array {
        $results = [];
        if ($node->isEndOfWord) $results[] = $prefix;
        foreach ($node->children as $char => $child) {
            $results = array_merge($results, $this->collectAll($child, $prefix . $char));
        }
        return $results;
    }
}
```
**Tushuntirish:** Trie tuzilmasi prefiks bo'yicha qidiruvda massivni to'liq skanerlashdan ko'ra ancha tezroq ishlaydi, bu esa yuqori yuklamali tizimlar uchun optimaldir.

---

### Topshiriq #1082: Segment Tree yordamida diapazon yig'indisini hisoblash
**Tavsif:** Moliyaviy tranzaksiyalar jadvalida ma'lum vaqt oralig'idagi yig'indini real vaqt rejimida hisoblash.
**Talablar:** Yangilash va so'rovlar uchun O(log N) murakkablik.
**Yechim (PHP):**
```php
class SegmentTree {
    private $tree, $n;

    public function __construct($data) {
        $this->n = count($data);
        $this->tree = array_fill(0, 2 * $this->n, 0);
        for ($i = 0; $i < $this->n; $i++) $this->tree[$this->n + $i] = $data[$i];
        for ($i = $this->n - 1; $i > 0; $i--) $this->tree[$i] = $this->tree[2 * $i] + $this->tree[2 * $i + 1];
    }

    public function update($i, $val) {
        for ($this->tree[$i += $this->n] = $val; $i > 1; $i >>= 1) 
            $this->tree[$i >> 1] = $this->tree[$i] + $this->tree[$i ^ 1];
    }

    public function query($l, $r) {
        $res = 0;
        for ($l += $this->n, $r += $this->n; $l < $r; $l >>= 1, $r >>= 1) {
            if ($l & 1) $res += $this->tree[$l++];
            if ($r & 1) $res += $this->tree[--$r];
        }
        return $res;
    }
}
```
**Tushuntirish:** Segment Tree dinamik ma'lumotlar to'plamida interval so'rovlarini bajarish uchun eng samarali tuzilmalardan biridir.

---

### Topshiriq #1083: Fenwick Tree (Binary Indexed Tree) bilan chastotani kuzatish
**Tavsif:** Katta hajmdagi log fayllarda hodisalar chastotasini hisoblash va prefiks yig'indilarni tezkor olish.
**Talablar:** O(log N) murakkablik va minimal xotira sarfi.
**Yechim (PHP):**
```php
class FenwickTree {
    private $tree;
    public function __construct($n) { $this->tree = array_fill(0, $n + 1, 0); }

    public function add($i, $delta) {
        for (; $i < count($this->tree); $i += $i & -$i) $this->tree[$i] += $delta;
    }

    public function query($i) {
        $sum = 0;
        for (; $i > 0; $i -= $i & -$i) $sum += $this->tree[$i];
        return $sum;
    }
}
```
**Tushuntirish:** Fenwick Tree Segment Tree'ga qaraganda kamroq xotira talab qiladi va implementatsiyasi soddaroq, bu esa yuqori chastotali hisob-kitoblar uchun juda mos.

---

### Topshiriq #1084: Grafda eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Logistika tizimida serverlar yoki tarmoq tugunlari orasidagi eng qisqa aloqa yo'lini aniqlash.
**Talablar:** O(E log V) murakkablik, xavfsiz va xatosiz ishlash.
**Yechim (PHP):**
```php
function dijkstra($graph, $start) {
    $dist = array_fill_keys(array_keys($graph), INF);
    $dist[$start] = 0;
    $pq = new SplPriorityQueue();
    $pq->insert($start, 0);

    while (!$pq->isEmpty()) {
        $u = $pq->extract();
        foreach ($graph[$u] as $v => $weight) {
            if ($dist[$u] + $weight < $dist[$v]) {
                $dist[$v] = $dist[$u] + $weight;
                $pq->insert($v, -$dist[$v]);
            }
        }
    }
    return $dist;
}
```
**Tushuntirish:** `SplPriorityQueue` PHP'ning o'rnatilgan samarali navbat tuzilmasi bo'lib, Dijkstra algoritmi uchun eng maqbul tanlovdir.

---

### Topshiriq #1085: Grafda sikllarni aniqlash (DFS)
**Tavsif:** Mikroservislar arxitekturasida bog'liqliklar (dependency) zanjirida sikllar mavjudligini tekshirish.
**Talablar:** Rekursiv yondashuv, O(V + E) vaqt murakkabligi.
**Yechim (PHP):**
```php
function hasCycle($graph, $node, &$visited, &$recStack) {
    $visited[$node] = true;
    $recStack[$node] = true;

    foreach ($graph[$node] as $neighbor) {
        if (!isset($visited[$neighbor]) && hasCycle($graph, $neighbor, $visited, $recStack)) return true;
        elseif (isset($recStack[$neighbor])) return true;
    }
    unset($recStack[$node]);
    return false;
}
```
**Tushuntirish:** `recStack` (rekursiya stek) yordamida joriy yo'lda tugun qayta uchraganini tekshirish siklni aniqlashning eng ishonchli usulidir.

---

### Topshiriq #1086: Topologik saralash (Kahn algoritmi)
**Tavsif:** Vazifalar ketma-ketligini (Task scheduling) bajarish tartibini belgilash.
**Talablar:** O(V + E) murakkablik, siklsiz graflar uchun.
**Yechim (PHP):**
```php
function topologicalSort($graph, $inDegree) {
    $queue = new SplQueue();
    foreach ($inDegree as $node => $deg) if ($deg === 0) $queue->enqueue($node);
    $result = [];
    while (!$queue->isEmpty()) {
        $u = $queue->dequeue();
        $result[] = $u;
        foreach ($graph[$u] as $v) {
            if (--$inDegree[$v] === 0) $queue->enqueue($v);
        }
    }
    return $result;
}
```
**Tushuntirish:** Kahn algoritmi tugunlarning kirish darajasiga (in-degree) asoslanib, vazifalarni to'g'ri tartibda bajarishni ta'minlaydi.

---

### Topshiriq #1087: Disjoint Set Union (DSU)
**Tavsif:** Tarmoqdagi tugunlarning bir-biriga bog'liqligini (connectivity) boshqarish.
**Talablar:** Path compression va union by rank texnikalaridan foydalanish.
**Yechim (PHP):**
```php
class DSU {
    private $parent;
    public function __construct($n) { $this->parent = range(0, $n); }
    public function find($i) {
        if ($this->parent[$i] == $i) return $i;
        return $this->parent[$i] = $this->find($this->parent[$i]);
    }
    public function union($i, $j) {
        $rootI = $this->find($i); $rootJ = $this->find($j);
        if ($rootI != $rootJ) $this->parent[$rootI] = $rootJ;
    }
}
```
**Tushuntirish:** Path compression yordamida `find` operatsiyasi deyarli doimiy vaqtda (amortized O(1)) ishlaydi.

---

### Topshiriq #1088: Trie yordamida IP-manzillar prefiksini qidirish
**Tavsif:** Firewall tizimlarida IP-manzillarni blokirovka qilish uchun prefiks qidirishni optimallashtirish.
**Talablar:** Bit darajasida ishlash, yuqori tezlik.
**Yechim (PHP):**
```php
class IPTrieNode { public $children = [0 => null, 1 => null]; public $isLeaf = false; }

class IPTrie {
    private $root;
    public function __construct() { $this->root = new IPTrieNode(); }
    public function insert($binaryIp) {
        $curr = $this->root;
        foreach (str_split($binaryIp) as $bit) {
            if (!$curr->children[$bit]) $curr->children[$bit] = new IPTrieNode();
            $curr = $curr->children[$bit];
        }
        $curr->isLeaf = true;
    }
}
```
**Tushuntirish:** IP-manzillarni ikkilik ko'rinishda Trie'ga joylash eng tezkor qidiruvni ta'minlaydi, bu esa tarmoq xavfsizligi uchun juda muhim.

---

### Topshiriq #1089: Grafda eng uzun yo'lni topish (DAG uchun)
**Tavsif:** Loyiha boshqaruvida "kritik yo'l" (Critical Path Method) ni aniqlash.
**Talablar:** Dinamik dasturlash va topologik saralash kombinatsiyasi.
**Yechim (PHP):**
```php
function longestPath($graph, $n) {
    $dist = array_fill(0, $n, -INF);
    $order = topologicalSort($graph, $inDegree); // Oldingi topshiriqdan
    $dist[$startNode] = 0;
    foreach ($order as $u) {
        foreach ($graph[$u] as $v => $weight) {
            if ($dist[$v] < $dist[$u] + $weight) $dist[$v] = $dist[$u] + $weight;
        }
    }
    return max($dist);
}
```
**Tushuntirish:** DAG (Directed Acyclic Graph) uchun eng uzun yo'l muammosi topologik tartibda DP yordamida O(V+E) vaqtda yechiladi.

---

### Topshiriq #1090: Fenwick Tree yordamida 2D diapazon yig'indisi
**Tavsif:** Tasvirni qayta ishlash yoki matritsali ma'lumotlar bazasida hududiy yig'indilarni tezkor hisoblash.
**Talablar:** O(log N * log M) murakkablik.
**Yechim (PHP):**
```php
class FenwickTree2D {
    private $tree;
    public function __construct($rows, $cols) { $this->tree = array_fill(0, $rows + 1, array_fill(0, $cols + 1, 0)); }

    public function update($r, $c, $val) {
        for ($i = $r; $i < count($this->tree); $i += $i & -$i)
            for ($j = $c; $j < count($this->tree[0]); $j += $j & -$j)
                $this->tree[$i][$j] += $val;
    }

    public function query($r, $c) {
        $sum = 0;
        for ($i = $r; $i > 0; $i -= $i & -$i)
            for ($j = $c; $j > 0; $j -= $j & -$j)
                $sum += $this->tree[$i][$j];
        return $sum;
    }
}
```
**Tushuntirish:** 2D Fenwick Tree ko'p o'lchovli ma'lumotlar massivlarida hududiy so'rovlarni bajarish uchun eng ixcham va samarali yechimdir.

---

### Topshiriq #1091: Graflarda eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Logistika tizimida serverlararo ma'lumot uzatish uchun eng kam kechikishli (latency) yo'lni aniqlash.
**Talablar:** O(E log V) murakkablik, `SplPriorityQueue` dan foydalanish.
**Yechim (PHP):**
```php
function dijkstra($graph, $start) {
    $distances = array_fill_keys(array_keys($graph), INF);
    $distances[$start] = 0;
    $pq = new SplPriorityQueue();
    $pq->insert($start, 0);

    while (!$pq->isEmpty()) {
        $u = $pq->extract();
        foreach ($graph[$u] as $v => $weight) {
            if ($distances[$u] + $weight < $distances[$v]) {
                $distances[$v] = $distances[$u] + $weight;
                $pq->insert($v, -$distances[$v]);
            }
        }
    }
    return $distances;
}
```
**Tushuntirish:** `SplPriorityQueue` PHP'ning o'rnatilgan samarali tuzilmasi bo'lib, katta hajmdagi graf tugunlarini qayta ishlashda xotirani tejaydi.

### Topshiriq #1092: Segment Tree yordamida diapazon yig'indisi
**Tavsif:** Moliya tizimida ma'lum vaqt oralig'idagi tranzaksiyalar yig'indisini real vaqtda hisoblash.
**Talablar:** Yangilash va so'rov uchun O(log N) murakkablik.
**Yechim (PHP):**
```php
class SegmentTree {
    private $tree;
    private $n;
    public function __construct($data) {
        $this->n = count($data);
        $this->tree = array_fill(0, 2 * $this->n, 0);
        for ($i = 0; $i < $this->n; $i++) $this->tree[$this->n + $i] = $data[$i];
        for ($i = $this->n - 1; $i > 0; $i--) $this->tree[$i] = $this->tree[2 * $i] + $this->tree[2 * $i + 1];
    }
    public function query($l, $r) {
        $res = 0;
        for ($l += $this->n, $r += $this->n; $l < $r; $l >>= 1, $r >>= 1) {
            if ($l & 1) $res += $this->tree[$l++];
            if ($r & 1) $res += $this->tree[--$r];
        }
        return $res;
    }
}
```
**Tushuntirish:** Iterativ Segment Tree rekursiv yondashuvga qaraganda tezroq ishlaydi va stack overflow xavfini yo'qotadi.

### Topshiriq #1093: Fenwick Tree (Binary Indexed Tree)
**Tavsif:** Katta ma'lumotlar bazasida kümülatif chastotalarni (frequency) hisoblash.
**Talablar:** Xotira samaradorligi va O(log N) tezlik.
**Yechim (PHP):**
```php
class FenwickTree {
    private $tree;
    public function __construct($n) { $this->tree = array_fill(0, $n + 1, 0); }
    public function update($i, $delta) {
        for (; $i < count($this->tree); $i += $i & -$i) $this->tree[$i] += $delta;
    }
    public function query($i) {
        $sum = 0;
        for (; $i > 0; $i -= $i & -$i) $sum += $this->tree[$i];
        return $sum;
    }
}
```
**Tushuntirish:** Fenwick Tree Segment Tree'ga nisbatan kamroq xotira talab qiladi, bu esa katta massivlar uchun ideal.

### Topshiriq #1094: Trie (Prefix Tree) implementatsiyasi
**Tavsif:** Foydalanuvchi qidiruv so'rovlari uchun "avtomatik to'ldirish" (autocomplete) funksiyasi.
**Talablar:** So'zlarni tezkor qidirish va xotira optimizatsiyasi.
**Yechim (PHP):**
```php
class TrieNode {
    public $children = [];
    public $isEndOfWord = false;
}
class Trie {
    private $root;
    public function __construct() { $this->root = new TrieNode(); }
    public function insert($word) {
        $curr = $this->root;
        foreach (str_split($word) as $char) {
            if (!isset($curr->children[$char])) $curr->children[$char] = new TrieNode();
            $curr = $curr->children[$char];
        }
        $curr->isEndOfWord = true;
    }
}
```
**Tushuntirish:** Trie tuzilmasi lug'at hajmi katta bo'lganda qidiruvni O(L) vaqtda (L - so'z uzunligi) bajaradi.

### Topshiriq #1095: Graflarda siklni aniqlash (DFS)
**Tavsif:** Mikroservislar o'rtasidagi bog'liqliklarda (dependency) o'zaro bog'liqlik (deadlock) xavfini aniqlash.
**Talablar:** Rekursiv yondashuv va xavfsizlik tekshiruvi.
**Yechim (PHP):**
```php
function hasCycle($graph, $node, &$visited, &$recStack) {
    $visited[$node] = true;
    $recStack[$node] = true;
    foreach ($graph[$node] as $neighbor) {
        if (!$visited[$neighbor] && hasCycle($graph, $neighbor, $visited, $recStack)) return true;
        elseif ($recStack[$neighbor]) return true;
    }
    $recStack[$node] = false;
    return false;
}
```
**Tushuntirish:** `recStack` yordamida joriy rekursiya yo'lidagi tugunlar kuzatiladi, bu esa siklni aniq topish imkonini beradi.

### Topshiriq #1096: Topological Sort (Kahn algoritmi)
**Tavsif:** Vazifalarni bajarish tartibini (task scheduling) belgilash.
**Talablar:** Kiruvchi darajalar (in-degree) hisobi.
**Yechim (PHP):**
```php
function topoSort($graph, $inDegree) {
    $queue = new SplQueue();
    foreach ($inDegree as $node => $deg) if ($deg === 0) $queue->enqueue($node);
    $result = [];
    while (!$queue->isEmpty()) {
        $u = $queue->dequeue();
        $result[] = $u;
        foreach ($graph[$u] as $v) {
            if (--$inDegree[$v] === 0) $queue->enqueue($v);
        }
    }
    return $result;
}
```
**Tushuntirish:** Kahn algoritmi DAG (Directed Acyclic Graph) uchun eng samarali tartiblash usulidir.

### Topshiriq #1097: Disjoint Set Union (DSU)
**Tavsif:** Tarmoq segmentlarini birlashtirish va ular orasidagi aloqani tekshirish.
**Talablar:** Path compression va union by rank optimizatsiyasi.
**Yechim (PHP):**
```php
class DSU {
    private $parent;
    public function __construct($n) { $this->parent = range(0, $n); }
    public function find($i) {
        if ($this->parent[$i] == $i) return $i;
        return $this->parent[$i] = $this->find($this->parent[$i]);
    }
    public function union($i, $j) {
        $rootI = $this->find($i);
        $rootJ = $this->find($j);
        if ($rootI != $rootJ) $this->parent[$rootI] = $rootJ;
    }
}
```
**Tushuntirish:** Path compression `find` operatsiyasini deyarli doimiy vaqtda bajarishga imkon beradi.

### Topshiriq #1098: Tarjan algoritmi (SCC)
**Tavsif:** Ijtimoiy tarmoqlarda kuchli bog'langan komponentlarni (Strongly Connected Components) aniqlash.
**Talablar:** O(V+E) vaqt murakkabligi.
**Yechim (PHP):**
```php
// Tarjan algoritmi yordamida SCC ni topish
function tarjan($u, &$ids, &$low, &$onStack, &$stack, &$timer, $graph) {
    $ids[$u] = $low[$u] = ++$timer;
    $stack->push($u);
    $onStack[$u] = true;
    foreach ($graph[$u] as $v) {
        if ($ids[$v] == -1) {
            tarjan($v, $ids, $low, $onStack, $stack, $timer, $graph);
            $low[$u] = min($low[$u], $low[$v]);
        } elseif ($onStack[$v]) $low[$u] = min($low[$u], $ids[$v]);
    }
    // SCC aniqlanganda stackdan chiqarish...
}
```
**Tushuntirish:** Tarjan algoritmi bir marta DFS o'tish orqali barcha SCC'larni topadi, bu esa katta graflar uchun juda tez.

### Topshiriq #1099: Minimum Spanning Tree (Kruskal)
**Tavsif:** Shaharlararo optik tolali tarmoq qurishda eng kam xarajatli ulanishni topish.
**Talablar:** Edge listni saralash va DSU dan foydalanish.
**Yechim (PHP):**
```php
function kruskal($edges, $n) {
    usort($edges, fn($a, $b) => $a[2] <=> $b[2]);
    $dsu = new DSU($n);
    $mst = [];
    foreach ($edges as $edge) {
        if ($dsu->find($edge[0]) != $dsu->find($edge[1])) {
            $dsu->union($edge[0], $edge[1]);
            $mst[] = $edge;
        }
    }
    return $mst;
}
```
**Tushuntirish:** Kruskal algoritmi tarmoq infratuzilmasini optimallashtirishda eng ishonchli yondashuv hisoblanadi.

### Topshiriq #1100: Bellman-Ford algoritmi
**Tavsif:** Salbiy vaznli qirralar mavjud bo'lgan moliyaviy tranzaksiyalar graflarida eng qisqa yo'lni topish.
**Talablar:** Salbiy sikllarni aniqlash qobiliyati.
**Yechim (PHP):**
```php
function bellmanFord($edges, $n, $start) {
    $dist = array_fill(0, $n, INF);
    $dist[$start] = 0;
    for ($i = 0; $i < $n - 1; $i++) {
        foreach ($edges as $edge) {
            if ($dist[$edge[0]] + $edge[2] < $dist[$edge[1]]) 
                $dist[$edge[1]] = $dist[$edge[0]] + $edge[2];
        }
    }
    return $dist;
}
```
**Tushuntirish:** Dijkstra salbiy vaznlar bilan ishlay olmaydi, Bellman-Ford esa bu muammoni hal qiladi va tizim xavfsizligini ta'minlaydi.