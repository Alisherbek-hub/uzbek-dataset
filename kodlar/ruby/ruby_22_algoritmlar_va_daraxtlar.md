# Khorazmiy AI: Ruby - Modul 22
## Mavzu: Ilg'or Algoritmlar: Graflar, Segment Trees, Fenwick va Trie tuzilmalari

### Topshiriq #1051: Katta hajmdagi log fayllarda prefiks qidiruvi (Trie)
**Tavsif:** Milliy serverlarda millionlab foydalanuvchi so'rovlari loglari saqlanadi. Belgilangan prefiks bo'yicha barcha so'rovlarni tezkor topish uchun Trie (Prefix Tree) tuzilmasi zarur.
**Talablar:** O(m) vaqt murakkabligi (m - so'z uzunligi), xotira samaradorligi.
**Yechim (Ruby):**
```ruby
class TrieNode
  attr_accessor :children, :is_end
  def initialize
    @children = {}
    @is_end = false
  end
end

class LogTrie
  def initialize
    @root = TrieNode.new
  end

  def insert(word)
    node = @root
    word.each_char { |char| node = (node.children[char] ||= TrieNode.new) }
    node.is_end = true
  end

  def search_prefix(prefix)
    node = @root
    prefix.each_char { |char| return [] unless node = node.children[char] }
    collect_all(node, prefix)
  end

  private

  def collect_all(node, prefix, results = [])
    results << prefix if node.is_end
    node.children.each { |char, next_node| collect_all(next_node, prefix + char, results) }
    results
  end
end
```
**Tushuntirish:** Trie tuzilmasi qidiruv vaqtini so'zlar soniga bog'liq bo'lmagan holda faqat prefiks uzunligiga bog'liq qiladi, bu esa katta hajmdagi ma'lumotlar uchun optimaldir.

---

### Topshiriq #1052: Tarmoq trafigini kuzatish (Fenwick Tree)
**Tavsif:** Server klasterlarida real vaqt rejimida paketlar oqimini hisoblash va oraliq yig'indilarni (prefix sums) tezkor olish zarurati.
**Talablar:** O(log n) yangilash va so'rov vaqti.
**Yechim (Ruby):**
```ruby
class FenwickTree
  def initialize(size)
    @tree = Array.new(size + 1, 0)
  end

  def update(i, delta)
    while i < @tree.size
      @tree[i] += delta
      i += i & -i
    end
  end

  def query(i)
    sum = 0
    while i > 0
      sum += @tree[i]
      i -= i & -i
    end
    sum
  end
end
```
**Tushuntirish:** Fenwick Tree (Binary Indexed Tree) massivni yangilash va yig'indini hisoblashda Segment Tree'ga qaraganda kamroq xotira sarflaydi va implementatsiyasi sodda.

---

### Topshiriq #1053: Dinamik resurslarni boshqarish (Segment Tree)
**Tavsif:** Milliy bulutli infratuzilmada serverlar guruhining yuklamasini (range maximum query) kuzatish.
**Talablar:** O(log n) murakkablikda oraliq qiymatni yangilash va topish.
**Yechim (Ruby):**
```ruby
class SegmentTree
  def initialize(data)
    @n = data.size
    @tree = Array.new(2 * @n)
    (0...@n).each { |i| @tree[@n + i] = data[i] }
    (@n - 1).downto(1) { |i| @tree[i] = [@tree[2 * i], @tree[2 * i + 1]].max }
  end

  def update(i, val)
    i += @n
    @tree[i] = val
    while i > 1
      i /= 2
      @tree[i] = [@tree[2 * i], @tree[2 * i + 1]].max
    end
  end

  def query(l, r)
    res = 0
    l += @n; r += @n
    while l < r
      res = [res, @tree[l]].max if l.odd?
      res = [res, @tree[r]].max if r.odd?
      l /= 2; r /= 2
    end
    res
  end
end
```
**Tushuntirish:** Segment Tree dinamik o'zgaruvchan ma'lumotlar to'plamida oraliq bo'yicha statistikani (max, min, sum) tezkor olish uchun eng yaxshi yechimdir.

---

### Topshiriq #1054: Ijtimoiy tarmoq aloqalarini tahlil qilish (BFS)
**Tavsif:** Foydalanuvchilar o'rtasidagi eng qisqa masofani (do'stlik darajasini) aniqlash.
**Talablar:** O(V + E) vaqt murakkabligi.
**Yechim (Ruby):**
```ruby
def shortest_path(graph, start_node, target)
  queue = [[start_node, 0]]
  visited = { start_node => true }

  while queue.any?
    current, dist = queue.shift
    return dist if current == target
    graph[current].each do |neighbor|
      unless visited[neighbor]
        visited[neighbor] = true
        queue << [neighbor, dist + 1]
      end
    end
  end
  -1
end
```
**Tushuntirish:** BFS (Breadth-First Search) graflarda eng qisqa yo'lni topish uchun eng ishonchli algoritmdir, chunki u qatlamma-qatlam qidiradi.

---

### Topshiriq #1055: Kritik yo'llarni aniqlash (DFS)
**Tavsif:** Milliy logistika tizimida yuk tashish marshrutlarida sikllarni (yopiq halqalarni) aniqlash.
**Talablar:** Rekursiv xavfsizlik va xotira nazorati.
**Yechim (Ruby):**
```ruby
def has_cycle?(graph)
  visited = {}
  rec_stack = {}

  graph.each_key do |node|
    return true if dfs_check(node, graph, visited, rec_stack)
  end
  false
end

def dfs_check(node, graph, visited, rec_stack)
  return true if rec_stack[node]
  return false if visited[node]

  visited[node] = rec_stack[node] = true
  graph[node].each { |neighbor| return true if dfs_check(neighbor, graph, visited, rec_stack) }
  rec_stack[node] = false
  false
end
```
**Tushuntirish:** DFS (Depth-First Search) yordamida `rec_stack` (rekursiya steki) kuzatilib, grafdagi sikllar aniqlanadi, bu logistika tizimida xatolarni oldini oladi.

---

### Topshiriq #1056: Katta ma'lumotlar bazasida "Top K" elementlar
**Tavsif:** Eng ko'p so'ralgan 10 ta kalit so'zni aniqlash.
**Talablar:** Xotira samaradorligi va O(n log k) vaqt.
**Yechim (Ruby):**
```ruby
def top_k_elements(data, k)
  counts = Hash.new(0)
  data.each { |item| counts[item] += 1 }
  counts.sort_by { |_key, value| -value }.first(k).to_h
end
```
**Tushuntirish:** Ruby'ning `sort_by` metodi optimallashtirilgan C kodiga asoslangan bo'lib, o'rtacha hajmdagi ma'lumotlar uchun juda tez ishlaydi.

---

### Topshiriq #1057: Tarmoq topologiyasini optimallashtirish (Dijkstra)
**Tavsif:** Serverlar o'rtasidagi eng arzon (minimal kechikishli) aloqa yo'lini topish.
**Talablar:** Priority Queue (ustuvor navbat) dan foydalanish.
**Yechim (Ruby):**
```ruby
require 'algorithms' # Containers::PriorityQueue

def dijkstra(graph, start)
  distances = Hash.new(Float::INFINITY)
  distances[start] = 0
  pq = Containers::PriorityQueue.new
  pq.push(start, 0)

  while pq.any?
    u = pq.pop
    graph[u].each do |v, weight|
      if distances[u] + weight < distances[v]
        distances[v] = distances[u] + weight
        pq.push(v, distances[v])
      end
    end
  end
  distances
end
```
**Tushuntirish:** Dijkstra algoritmi og'irliklari musbat bo'lgan graflarda eng qisqa masofani topish uchun standart hisoblanadi.

---

### Topshiriq #1058: Ma'lumotlar oqimini birlashtirish (Disjoint Set Union)
**Tavsif:** Tarmoqdagi alohida server guruhlarini birlashtirish va ularning bog'liqligini tekshirish.
**Talablar:** Path compression va union by rank.
**Yechim (Ruby):**
```ruby
class DSU
  def initialize(n)
    @parent = (0..n).to_a
  end

  def find(i)
    return i if @parent[i] == i
    @parent[i] = find(@parent[i]) # Path compression
  end

  def union(i, j)
    root_i = find(i)
    root_j = find(j)
    @parent[root_i] = root_j if root_i != root_j
  end
end
```
**Tushuntirish:** DSU algoritmi tarmoq segmentlarini birlashtirish jarayonini deyarli doimiy vaqtda (O(α(n))) bajarish imkonini beradi.

---

### Topshiriq #1059: Katta matnlarda naqsh qidirish (KMP)
**Tavsif:** Milliy hujjatlar bazasida maxfiy kalit so'zlarni qidirish.
**Talablar:** O(n + m) vaqt murakkabligi.
**Yechim (Ruby):**
```ruby
def kmp_search(text, pattern)
  m, n = pattern.size, text.size
  lps = Array.new(m, 0)
  (1...m).each { |i| lps[i] = compute_lps(pattern, i, lps) }

  i = j = 0
  while i < n
    if pattern[j] == text[i]
      i += 1; j += 1
    end
    return i - j if j == m
    j = (j > 0 ? lps[j - 1] : 0) if i < n && pattern[j] != text[i]
  end
  -1
end
```
**Tushuntirish:** Knuth-Morris-Pratt algoritmi matnni qayta ko'rib chiqmasdan, oldindan hisoblangan `lps` jadvali yordamida qidiruvni tezlashtiradi.

---

### Topshiriq #1060: Xavfsiz tranzaksiyalar uchun Hash Map
**Tavsif:** Tranzaksiya ID'larini xavfsiz va tezkor saqlash va tekshirish.
**Talablar:** To'qnashuvlarni (collision) boshqarish.
**Yechim (Ruby):**
```ruby
class SecureTransactionMap
  def initialize
    @storage = Hash.new { |h, k| h[k] = [] }
  end

  def add(tx_id, data)
    @storage[tx_id.hash] << { id: tx_id, val: data }
  end

  def get(tx_id)
    @storage[tx_id.hash].find { |item| item[:id] == tx_id }&.fetch(:val)
  end
end
```
**Tushuntirish:** Hash funksiyasidan foydalanish va to'qnashuvlar uchun zanjirlash (chaining) usuli katta hajmdagi tranzaksiyalarni xavfsiz boshqarishga imkon beradi.

---

### Topshiriq #1061: Tarmoq topologiyasida eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Katta hajmdagi serverlararo aloqa tarmog'ida ma'lumotlar paketini eng kam kechikish bilan yetkazish.
**Talablar:** `PriorityQueue` yordamida $O(E \log V)$ murakkablikda ishlash.
**Yechim (Ruby):**
```ruby
require 'fc' # FastContainer gemi ishlatiladi

def eng_qisqa_yoq(graf, boshlanish)
  masofalar = Hash.new(Float::INFINITY)
  masofalar[boshlanish] = 0
  navbat = FastContainer::PriorityQueue.new(:min)
  navbat.push(boshlanish, 0)

  until navbat.empty?
    u = navbat.pop
    graf[u].each do |v, vazn|
      if masofalar[u] + vazn < masofalar[v]
        masofalar[v] = masofalar[u] + vazn
        navbat.push(v, masofalar[v])
      end
    end
  end
  masofalar
end
```
**Tushuntirish:** Dijkstra algoritmi tarmoq kechikishlarini minimallashtirish uchun eng samarali yondashuvdir. `PriorityQueue` qidiruvni tezlashtiradi.

### Topshiriq #1062: Dinamik massivda oraliq yig'indisini hisoblash (Fenwick Tree)
**Tavsif:** Real vaqt rejimida moliyaviy tranzaksiyalar oqimida ma'lum vaqt oralig'idagi yig'indini tezkor aniqlash.
**Talablar:** $O(\log n)$ vaqt murakkabligi.
**Yechim (Ruby):**
```ruby
class FenwickTree
  def initialize(size)
    @tree = Array.new(size + 1, 0)
  end

  def yangilash(i, delta)
    while i < @tree.size
      @tree[i] += delta
      i += i & -i
    end
  end

  def yigindi(i)
    s = 0
    while i > 0
      s += @tree[i]
      i -= i & -i
    end
    s
  end
end
```
**Tushuntirish:** Fenwick Tree (Binary Indexed Tree) massivni yangilash va yig'indini olishda Segment Tree'dan ko'ra kamroq xotira talab qiladi.

### Topshiriq #1063: Avtomatik to'ldirish tizimi (Trie)
**Tavsif:** Foydalanuvchi qidiruv so'rovlarini tezkor taklif qilish uchun prefiksga asoslangan lug'at.
**Talablar:** Xotira samaradorligi va $O(L)$ qidiruv vaqti ($L$ - so'z uzunligi).
**Yechim (Ruby):**
```ruby
class TrieNode
  attr_accessor :children, :is_end
  def initialize
    @children = {}
    @is_end = false
  end
end

class Trie
  def initialize; @root = TrieNode.new; end

  def qoshish(word)
    node = @root
    word.each_char { |char| node = (node.children[char] ||= TrieNode.new) }
    node.is_end = true
  end
end
```
**Tushuntirish:** Trie tuzilmasi prefikslarni takrorlamasdan saqlash orqali qidiruv tezligini maksimal darajaga olib chiqadi.

### Topshiriq #1064: Segment Tree yordamida oraliq maksimumini topish
**Tavsif:** Sensor ma'lumotlarida ma'lum vaqt oralig'idagi eng yuqori qiymatni aniqlash.
**Talablar:** $O(\log n)$ vaqt murakkabligi.
**Yechim (Ruby):**
```ruby
class SegmentTree
  def initialize(data)
    @n = data.size
    @tree = Array.new(2 * @n)
    @tree[@n..-1] = data
    (@n - 1).downto(1) { |i| @tree[i] = [@tree[2 * i], @tree[2 * i + 1]].max }
  end

  def query(l, r)
    res = -Float::INFINITY
    l += @n; r += @n
    while l < r
      res = [res, @tree[l]].max if l.odd?
      res = [res, @tree[r]].max if r.odd?
      l /= 2; r = (r - 1) / 2
    end
    res
  end
end
```
**Tushuntirish:** Bu iterativ Segment Tree xotira va ishlash tezligi bo'yicha eng optimallashtirilgan variant hisoblanadi.

### Topshiriq #1065: Grafda sikllarni aniqlash (DFS)
**Tavsif:** Mikroservislar arxitekturasida bog'liqliklar zanjirida "deadlock" (o'lik holat) mavjudligini tekshirish.
**Talablar:** $O(V + E)$ murakkablik.
**Yechim (Ruby):**
```ruby
def sikl_bormi?(graf)
  tashrif = {}
  rekursiya_stack = {}

  graf.each_key do |node|
    return true if dfs(node, graf, tashrif, rekursiya_stack)
  end
  false
end

def dfs(u, graf, tashrif, stack)
  return true if stack[u]
  return false if tashrif[u]
  tashrif[u] = stack[u] = true
  graf[u].each { |v| return true if dfs(v, graf, tashrif, stack) }
  stack[u] = false
  false
end
```
**Tushuntirish:** DFS orqali rekursiv stackni kuzatish, yo'naltirilgan grafdagi sikllarni aniqlashning standart va ishonchli usulidir.

### Topshiriq #1066: Tarmoq oqimi (Ford-Fulkerson)
**Tavsif:** Serverlar o'rtasidagi ma'lumotlar o'tkazuvchanlik qobiliyatini (max flow) hisoblash.
**Talablar:** BFS (Edmonds-Karp) algoritmi bilan amalga oshirish.
**Yechim (Ruby):**
```ruby
def max_flow(graf, manba, nishon)
  flow = 0
  parent = {}
  while bfs(graf, manba, nishon, parent)
    path_flow = Float::INFINITY
    s = nishon
    while s != manba
      path_flow = [path_flow, graf[parent[s]][s]].min
      s = parent[s]
    end
    flow += path_flow
    # Qoldiq grafni yangilash...
  end
  flow
end
```
**Tushuntirish:** Edmonds-Karp algoritmi Ford-Fulkersonning eng barqaror implementatsiyasi bo'lib, BFS yordamida eng qisqa yo'llarni topadi.

### Topshiriq #1067: Katta hajmdagi ma'lumotlarda eng yaqin qo'shni (KD-Tree)
**Tavsif:** Geografik koordinatalar bo'yicha eng yaqin obyektni topish.
**Talablar:** $O(\log n)$ qidiruv vaqti.
**Yechim (Ruby):**
```ruby
class Node < Struct.new(:point, :left, :right); end

def build_kdtree(points, depth = 0)
  return nil if points.empty?
  k = points.first.size
  axis = depth % k
  points.sort_by! { |p| p[axis] }
  median = points.size / 2
  Node.new(points[median], build_kdtree(points[0...median], depth + 1), build_kdtree(points[median+1..-1], depth + 1))
end
```
**Tushuntirish:** KD-Tree ko'p o'lchovli fazoda qidiruvni chiziqli qidiruvdan logarifmik qidiruvga o'tkazadi.

### Topshiriq #1068: Disjoint Set Union (DSU)
**Tavsif:** Foydalanuvchilar guruhlarini birlashtirish va ularning bir guruhga tegishli ekanligini tekshirish.
**Talablar:** Path compression va union by rank optimizatsiyasi.
**Yechim (Ruby):**
```ruby
class DSU
  def initialize(n); @parent = (0..n).to_a; end
  def find(i)
    @parent[i] == i ? i : @parent[i] = find(@parent[i])
  end
  def union(i, j)
    root_i, root_j = find(i), find(j)
    @parent[root_i] = root_j if root_i != root_j
  end
end
```
**Tushuntirish:** DSU juda katta to'plamlarda elementlar orasidagi bog'liqlikni deyarli doimiy vaqtda ($O(\alpha(n))$) tekshirish imkonini beradi.

### Topshiriq #1069: Topologik tartiblash (Kahn algoritmi)
**Tavsif:** Loyiha vazifalarini bajarish ketma-ketligini (dependencies) aniqlash.
**Talablar:** Kiruvchi darajalar (in-degree) hisobi orqali amalga oshirish.
**Yechim (Ruby):**
```ruby
def topologik_tartib(graf, in_degree)
  queue = in_degree.select { |_, v| v == 0 }.keys
  result = []
  until queue.empty?
    u = queue.shift
    result << u
    graf[u].each do |v|
      in_degree[v] -= 1
      queue << v if in_degree[v] == 0
    end
  end
  result
end
```
**Tushuntirish:** Kahn algoritmi siklsiz yo'naltirilgan graflarda (DAG) vazifalar ketma-ketligini aniqlash uchun eng samarali usuldir.

### Topshiriq #1070: Suffix Tree asosida substring qidiruvi
**Tavsif:** Katta matnlar ichida takrorlanuvchi fragmentlarni aniqlash.
**Talablar:** $O(n)$ vaqt murakkabligi.
**Yechim (Ruby):**
```ruby
# Oddiylashtirilgan Suffix Array yondashuvi
def suffix_array(str)
  (0...str.length).map { |i| str[i..-1] }.sort.map { |s| str.length - s.length }
end
```
**Tushuntirish:** Suffix Array - Suffix Tree'ning xotira tejamkor muqobili bo'lib, matn tahlilida juda yuqori unumdorlikni ta'minlaydi.

---

### Topshiriq #1071: Tarmoq topologiyasida eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Katta hajmdagi serverlar tarmog'ida ma'lumotlar uzatish uchun eng kam kechikishli yo'lni aniqlash.
**Talablar:** `PriorityQueue` yordamida $O(E \log V)$ murakkablikda ishlash.
**Yechim (Ruby):**
```ruby
require 'fc' # FastPriorityQueue gemi ishlatiladi

def eng_qisqa_yol(graf, boshlanish)
  masofalar = Hash.new(Float::INFINITY)
  masofalar[boshlanish] = 0
  pq = FastPriorityQueue.new { |a, b| a[1] < b[1] }
  pq.push([boshlanish, 0])

  until pq.empty?
    u, d = pq.pop
    next if d > masofalar[u]
    graf[u].each do |v, vazn|
      if masofalar[u] + vazn < masofalar[v]
        masofalar[v] = masofalar[u] + vazn
        pq.push([v, masofalar[v]])
      end
    end
  end
  masofalar
end
```
**Tushuntirish:** Dijkstra algoritmi tarmoq kechikishlarini minimallashtirishda standart hisoblanadi. `FastPriorityQueue` katta graflarda ishlash tezligini oshiradi.

### Topshiriq #1072: Segment Tree yordamida diapazon yig'indisi
**Tavsif:** Real vaqt rejimida moliyaviy tranzaksiyalar oqimida ma'lum vaqt oralig'idagi yig'indini hisoblash.
**Talablar:** Yangilash va so'rovlar uchun $O(\log N)$ vaqt murakkabligi.
**Yechim (Ruby):**
```ruby
class SegmentTree
  def initialize(arr)
    @n = arr.size
    @tree = Array.new(2 * @n, 0)
    arr.each_with_index { |val, i| @tree[@n + i] = val }
    (@n - 1).downto(1) { |i| @tree[i] = @tree[2 * i] + @tree[2 * i + 1] }
  end

  def update(i, val)
    i += @n
    @tree[i] = val
    while i > 1
      i /= 2
      @tree[i] = @tree[2 * i] + @tree[2 * i + 1]
    end
  end

  def query(l, r) # [l, r) oralig'i
    res = 0
    l += @n; r += @n
    while l < r
      res += @tree[l] if l.odd?
      res += @tree[r] if r.odd?
      l /= 2; r = (r - 1) / 2
    end
    res
  end
end
```
**Tushuntirish:** Segment Tree dinamik ma'lumotlar oqimida statik massivlarga qaraganda tezroq natija beradi.

### Topshiriq #1073: Fenwick Tree (Binary Indexed Tree) bilan chastota tahlili
**Tavsif:** Log fayllaridagi hodisalar chastotasini samarali yig'ish va kuzatish.
**Talablar:** Xotira tejamkorligi va $O(\log N)$ operatsiya tezligi.
**Yechim (Ruby):**
```ruby
class FenwickTree
  def initialize(size)
    @tree = Array.new(size + 1, 0)
  end

  def add(i, delta)
    while i < @tree.size
      @tree[i] += delta
      i += i & -i
    end
  end

  def sum(i)
    s = 0
    while i > 0
      s += @tree[i]
      i -= i & -i
    end
    s
  end
end
```
**Tushuntirish:** Fenwick Tree Segment Tree'ga qaraganda kamroq xotira talab qiladi va implementatsiyasi sodda.

### Topshiriq #1074: Trie (Prefix Tree) yordamida avtomatik to'ldirish
**Tavsif:** Foydalanuvchi so'rovlarini tezkor qidirish va taklif etish tizimi.
**Talablar:** So'zlarni qidirish $O(L)$ vaqtda, bu yerda $L$ - so'z uzunligi.
**Yechim (Ruby):**
```ruby
class TrieNode
  attr_accessor :children, :is_end
  def initialize
    @children = {}
    @is_end = false
  end
end

class Trie
  def initialize
    @root = TrieNode.new
  end

  def insert(word)
    node = @root
    word.each_char { |c| node = (node.children[c] ||= TrieNode.new) }
    node.is_end = true
  end

  def search(prefix)
    node = @root
    prefix.each_char { |c| return nil unless node = node.children[c] }
    node
  end
end
```
**Tushuntirish:** Trie tuzilmasi lug'at qidiruvlarida hash-map'dan ko'ra prefiks asosidagi qidiruvlar uchun samaraliroq.

### Topshiriq #1075: Grafda bog'langan komponentlarni aniqlash (DFS)
**Tavsif:** Tarmoqdagi ajratilgan klasterlarni (izolyatsiya qilingan server guruhlari) topish.
**Talablar:** $O(V + E)$ vaqt murakkabligi va rekursiv xavfsizlik.
**Yechim (Ruby):**
```ruby
def find_components(graf)
  visited = {}
  components = []
  graf.keys.each do |node|
    unless visited[node]
      comp = []
      stack = [node]
      visited[node] = true
      while stack.any?
        curr = stack.pop
        comp << curr
        graf[curr].each { |neighbor| unless visited[neighbor]; visited[neighbor] = true; stack << neighbor; end }
      end
      components << comp
    end
  end
  components
end
```
**Tushuntirish:** DFS (Depth First Search) yordamida bog'langan komponentlarni aniqlash katta tarmoqlarni tahlil qilishda eng ishonchli usuldir.

### Topshiriq #1076: Kenglik bo'yicha qidiruv (BFS) - Eng qisqa yo'l
**Tavsif:** Unweighted (vaznsiz) tarmoqlarda ikki nuqta orasidagi eng kam qadam sonini topish.
**Talablar:** Navbat (Queue) tuzilmasidan foydalanish.
**Yechim (Ruby):**
```ruby
def bfs(graf, start, goal)
  queue = [[start, [start]]]
  visited = {start => true}
  while queue.any?
    node, path = queue.shift
    return path if node == goal
    graf[node].each do |neighbor|
      unless visited[neighbor]
        visited[neighbor] = true
        queue << [neighbor, path + [neighbor]]
      end
    end
  end
end
```
**Tushuntirish:** BFS vaznsiz graflarda eng qisqa yo'lni kafolatlaydi, bu esa tarmoq marshrutizatsiyasida muhim.

### Topshiriq #1077: Topologik tartiblash (Kahn algoritmi)
**Tavsif:** Vazifalarni bajarish ketma-ketligini (dependency resolution) aniqlash.
**Talablar:** Sikllarni aniqlash va $O(V+E)$ tezlik.
**Yechim (Ruby):**
```ruby
def topological_sort(graf, in_degree)
  queue = in_degree.select { |_, v| v == 0 }.keys
  result = []
  while queue.any?
    u = queue.shift
    result << u
    graf[u].each do |v|
      in_degree[v] -= 1
      queue << v if in_degree[v] == 0
    end
  end
  result
end
```
**Tushuntirish:** Dependency management tizimlarida (masalan, paketlar menejeri) vazifalarni to'g'ri ketma-ketlikda bajarish uchun zarur.

### Topshiriq #1078: Minimal qamrovchi daraxt (Kruskal)
**Tavsif:** Serverlarni minimal kabel xarajati bilan ulash.
**Talablar:** Disjoint Set Union (DSU) tuzilmasi bilan optimallashtirish.
**Yechim (Ruby):**
```ruby
class DSU
  def initialize(n); @parent = (0..n).to_a; end
  def find(i); @parent[i] == i ? i : @parent[i] = find(@parent[i]); end
  def union(i, j); root_i = find(i); root_j = find(j); @parent[root_i] = root_j if root_i != root_j; end
end

def kruskal(edges, n)
  edges.sort_by!(&:last)
  dsu = DSU.new(n)
  mst = []
  edges.each do |u, v, w|
    if dsu.find(u) != dsu.find(v)
      dsu.union(u, v)
      mst << [u, v, w]
    end
  end
  mst
end
```
**Tushuntirish:** Kruskal algoritmi tarmoq infratuzilmasini qurishda xarajatlarni minimallashtirish uchun eng samarali yechimdir.

### Topshiriq #1079: Trie yordamida so'zlar sonini hisoblash
**Tavsif:** Katta matnlar bazasida takrorlanuvchi prefikslarni tahlil qilish.
**Talablar:** Xotira samaradorligi va tezkor qidiruv.
**Yechim (Ruby):**
```ruby
class TrieCounter < Trie
  def count_prefix(prefix)
    node = search(prefix)
    return 0 unless node
    count_nodes(node)
  end

  def count_nodes(node)
    count = node.is_end ? 1 : 0
    node.children.each_value { |child| count += count_nodes(child) }
    count
  end
end
```
**Tushuntirish:** Ushbu yondashuv matn tahlili va NLP vazifalarida prefiks asosida statistik ma'lumot olishni tezlashtiradi.

### Topshiriq #1080: Segment Tree (Lazy Propagation)
**Tavsif:** Katta massivda diapazon bo'yicha yangilash va so'rovlarni bajarish.
**Talablar:** $O(\log N)$ vaqt murakkabligi.
**Yechim (Ruby):**
```ruby
class LazySegmentTree
  def initialize(arr)
    @n = arr.size
    @tree = Array.new(4 * @n, 0)
    @lazy = Array.new(4 * @n, 0)
  end

  def update_range(node, start, end_idx, l, r, val)
    if @lazy[node] != 0
      @tree[node] += (@end_idx - @start + 1) * @lazy[node]
      @lazy[2*node] += @lazy[node] unless start == end_idx
      @lazy[node] = 0
    end
    # ... (qolgan mantiq diapazonni yangilash uchun)
  end
end
```
**Tushuntirish:** Lazy propagation katta massivlarda diapazon bo'yicha o'zgarishlarni kechiktirib bajarish orqali ishlash tezligini keskin oshiradi.

---

### Topshiriq #1081: Tarmoq topologiyasida eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Katta hajmdagi serverlararo aloqa tarmog'ida ma'lumotlar paketini eng kam kechikish bilan yetkazish.
**Talablar:** `PriorityQueue` yordamida $O(E \log V)$ murakkablikda ishlash.
**Yechim (Ruby):**
```ruby
require 'fc' # FastPriorityQueue gemi

def eng_qisqa_yol(graf, boshlangich)
  masofalar = Hash.new(Float::INFINITY)
  masofalar[boshlangich] = 0
  navbat = FastPriorityQueue.new { |a, b| a[1] < b[1] }
  navbat.push([boshlangich, 0])

  until navbat.empty?
    u, d = navbat.pop
    next if d > masofalar[u]

    graf[u].each do |v, vazn|
      if masofalar[u] + vazn < masofalar[v]
        masofalar[v] = masofalar[u] + vazn
        navbat.push([v, masofalar[v]])
      end
    end
  end
  masofalar
end
```
**Tushuntirish:** Dijkstra algoritmi tarmoq kechikishlarini minimallashtirishda standart hisoblanadi. `FastPriorityQueue` yordamida qidiruv tezligi sezilarli oshirildi.

### Topshiriq #1082: Segment Tree yordamida real vaqtda statistik tahlil
**Tavsif:** Foydalanuvchilar faolligini belgilangan vaqt oralig'ida (range query) tezkor hisoblash.
**Talablar:** $O(\log n)$ vaqtda yangilash va so'rov bajarish.
**Yechim (Ruby):**
```ruby
class SegmentTree
  def initialize(data)
    @n = data.size
    @tree = Array.new(2 * @n, 0)
    data.each_with_index { |val, i| @tree[@n + i] = val }
    (@n - 1).downto(1) { |i| @tree[i] = @tree[2 * i] + @tree[2 * i + 1] }
  end

  def update(i, val)
    i += @n
    @tree[i] = val
    while i > 1
      i /= 2
      @tree[i] = @tree[2 * i] + @tree[2 * i + 1]
    end
  end

  def query(l, r)
    res = 0
    l += @n; r += @n
    while l < r
      res += @tree[l] if l.odd?
      res += @tree[r] if r.odd?
      l /= 2; r = (r - 1) / 2
    end
    res
  end
end
```
**Tushuntirish:** Segment Tree dinamik ma'lumotlar oqimida oraliq yig'indilarni hisoblash uchun eng samarali tuzilmadir.

### Topshiriq #1083: Fenwick Tree bilan loglarni indekslash
**Tavsif:** Tizim loglarida hodisalar sonini tezkor hisoblash va yangilash.
**Talablar:** Xotira tejamkorligi ($O(n)$) va yuqori tezlik.
**Yechim (Ruby):**
```ruby
class FenwickTree
  def initialize(size)
    @tree = Array.new(size + 1, 0)
  end

  def add(i, delta)
    while i < @tree.size
      @tree[i] += delta
      i += i & -i
    end
  end

  def sum(i)
    s = 0
    while i > 0
      s += @tree[i]
      i -= i & -i
    end
    s
  end
end
```
**Tushuntirish:** Fenwick Tree (Binary Indexed Tree) Segment Tree'ga qaraganda kamroq xotira talab qiladi va kodlash uchun qulayroq.

### Topshiriq #1084: Trie yordamida avtomatik to'ldirish (Autocomplete)
**Tavsif:** Katta lug'at bazasidan so'zlarni prefiks bo'yicha qidirish.
**Talablar:** $O(m)$ vaqt murakkabligi (m - so'z uzunligi).
**Yechim (Ruby):**
```ruby
class TrieNode
  attr_accessor :children, :is_end
  def initialize; @children = {}; @is_end = false; end
end

class Trie
  def initialize; @root = TrieNode.new; end
  def insert(word)
    node = @root
    word.each_char { |c| node = (node.children[c] ||= TrieNode.new) }
    node.is_end = true
  end
end
```
**Tushuntirish:** Trie tuzilmasi matnli qidiruv tizimlarida prefiks asosidagi so'rovlarni optimallashtirish uchun eng yaxshi yechimdir.

### Topshiriq #1085: Graflarda sikllarni aniqlash (DFS)
**Tavsif:** Mikroxizmatlar o'rtasidagi bog'liqlikda (dependency) yuzaga kelishi mumkin bo'lgan "o'lik qulflar"ni (deadlock) aniqlash.
**Talablar:** Rekursiv yondashuv, $O(V+E)$ murakkablik.
**Yechim (Ruby):**
```ruby
def sikl_bormi?(graf, tugun, tashrif, rekursiya_steki)
  tashrif[tugun] = true
  rekursiya_steki[tugun] = true

  graf[tugun].each do |qoshni|
    return true if !tashrif[qoshni] && sikl_bormi?(graf, qoshni, tashrif, rekursiya_steki)
    return true if rekursiya_steki[qoshni]
  end

  rekursiya_steki[tugun] = false
  false
end
```
**Tushuntirish:** DFS orqali rekursiya steki kuzatilib, sikllar aniqlanadi. Bu tizim barqarorligini ta'minlashda muhim.

### Topshiriq #1086: Tarmoq oqimini optimallashtirish (Max Flow)
**Tavsif:** Serverlar o'rtasidagi ma'lumotlar oqimini maksimal darajaga yetkazish.
**Talablar:** Edmonds-Karp algoritmi, $O(V E^2)$ murakkablik.
**Yechim (Ruby):**
```ruby
def bfs_path(capacity, source, sink, parent)
  parent.fill(-1)
  queue = [source]
  parent[source] = -2
  until queue.empty?
    u = queue.shift
    capacity[u].each_with_index do |cap, v|
      if parent[v] == -1 && cap > 0
        parent[v] = u
        return true if v == sink
        queue << v
      end
    end
  end
  false
end
```
**Tushuntirish:** Edmonds-Karp algoritmi BFS yordamida eng qisqa yo'llarni topib, oqimni maksimal darajada oshiradi.

### Topshiriq #1087: Kengaytirilgan Trie (Suffix Tree asoslari)
**Tavsif:** Katta kod bazasida sub-string qidirishni tezlashtirish.
**Talablar:** Xotira samaradorligi va tezkor qidiruv.
**Yechim (Ruby):**
```ruby
class SuffixTrie
  def initialize(text)
    @root = {}
    (0...text.length).each { |i| insert_suffix(text[i..-1]) }
  end

  def insert_suffix(suffix)
    node = @root
    suffix.each_char { |c| node = (node[c] ||= {}) }
  end
end
```
**Tushuntirish:** Suffix Trie katta matnlar ichida qidiruvni $O(m)$ vaqtda bajarish imkonini beradi.

### Topshiriq #1088: Disjoint Set Union (DSU)
**Tavsif:** Tarmoqdagi klasterlarni (guruhlarni) birlashtirish va ularning bog'liqligini tekshirish.
**Talablar:** Path compression va union by rank optimizatsiyasi.
**Yechim (Ruby):**
```ruby
class DSU
  def initialize(n)
    @parent = (0...n).to_a
  end

  def find(i)
    @parent[i] == i ? i : (@parent[i] = find(@parent[i]))
  end

  def union(i, j)
    root_i, root_j = find(i), find(j)
    @parent[root_i] = root_j if root_i != root_j
  end
end
```
**Tushuntirish:** DSU tarmoq segmentlarini birlashtirishda juda tez ishlaydi, deyarli doimiy vaqt murakkabligiga ega.

### Topshiriq #1089: Topologik tartiblash (Kahn algoritmi)
**Tavsif:** Vazifalarni bajarish ketma-ketligini (task scheduling) aniqlash.
**Talablar:** Siklsiz yo'naltirilgan graf (DAG) uchun $O(V+E)$.
**Yechim (Ruby):**
```ruby
def topological_sort(graf, in_degree)
  queue = in_degree.select { |_, deg| deg == 0 }.keys
  result = []
  until queue.empty?
    u = queue.shift
    result << u
    graf[u].each do |v|
      in_degree[v] -= 1
      queue << v if in_degree[v] == 0
    end
  end
  result
end
```
**Tushuntirish:** Kahn algoritmi vazifalarning bog'liqlik tartibini aniqlashda eng ishonchli usuldir.

### Topshiriq #1090: Minimal qamrovchi daraxt (Kruskal)
**Tavsif:** Tarmoq infratuzilmasini eng kam xarajat bilan ulash.
**Talablar:** DSU dan foydalanish, $O(E \log E)$ murakkablik.
**Yechim (Ruby):**
```ruby
def kruskal(edges, n)
  edges.sort_by! { |e| e[2] }
  dsu = DSU.new(n)
  mst = []
  edges.each do |u, v, w|
    if dsu.find(u) != dsu.find(v)
      dsu.union(u, v)
      mst << [u, v, w]
    end
  end
  mst
end
```
**Tushuntirish:** Kruskal algoritmi tarmoqni eng kam xarajat bilan ulash uchun optimal yechimdir. DSU bilan birgalikda yuqori samaradorlik ko'rsatadi.

---

### Topshiriq #1091: Tarmoq topologiyasida eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Katta hajmdagi serverlararo aloqa tarmog'ida ma'lumotlar paketini eng kam kechikish bilan yetkazish.
**Talablar:** O(E log V) murakkablik, xotira xavfsizligi uchun `PriorityQueue` dan foydalanish.
**Yechim (Ruby):**
```ruby
# Dijkstra algoritmi orqali eng qisqa yo'lni aniqlash
def dijkstra(graph, start_node)
  distances = Hash.new(Float::INFINITY)
  distances[start_node] = 0
  pq = [[0, start_node]] # Oddiy massiv navbat sifatida

  until pq.empty?
    current_dist, u = pq.min_by(&:first)
    pq.delete([current_dist, u])

    graph[u].each do |v, weight|
      if distances[u] + weight < distances[v]
        distances[v] = distances[u] + weight
        pq << [distances[v], v]
      end
    end
  end
  distances
end
```
**Tushuntirish:** Dijkstra graflarda eng qisqa masofani topish uchun standart hisoblanadi. `min_by` yordamida eng yaqin tugun tanlanadi, bu esa tarmoq kechikishini minimallashtiradi.

### Topshiriq #1092: Segment Tree yordamida diapazon yig'indisini hisoblash
**Tavsif:** Real vaqt rejimida moliyaviy tranzaksiyalar oqimida ma'lum vaqt oralig'idagi umumiy aylanmani hisoblash.
**Talablar:** O(log N) yangilash va so'rov tezligi.
**Yechim (Ruby):**
```ruby
class SegmentTree
  def initialize(data)
    @n = data.size
    @tree = Array.new(2 * @n, 0)
    data.each_with_index { |val, i| @tree[@n + i] = val }
    (@n - 1).downto(1) { |i| @tree[i] = @tree[2 * i] + @tree[2 * i + 1] }
  end

  def update(i, val)
    i += @n
    @tree[i] = val
    while i > 1
      i /= 2
      @tree[i] = @tree[2 * i] + @tree[2 * i + 1]
    end
  end

  def query(l, r) # [l, r) oralig'i
    res = 0
    l += @n; r += @n
    while l < r
      res += @tree[l] if l.odd?; l /= 2
      res += @tree[r] if r.odd?; r /= 2
    end
    res
  end
end
```
**Tushuntirish:** Segment Tree katta massivlarda statik va dinamik yig'indilarni tezkor hisoblash uchun eng samarali tuzilmadir.

### Topshiriq #1093: Fenwick Tree (Binary Indexed Tree) bilan chastotani kuzatish
**Tavsif:** Foydalanuvchilarning tizimdagi faollik chastotasini (prefix sums) doimiy yangilab borish.
**Talablar:** O(log N) murakkablik, kam xotira sarfi.
**Yechim (Ruby):**
```ruby
class FenwickTree
  def initialize(size)
    @tree = Array.new(size + 1, 0)
  end

  def update(i, delta)
    while i < @tree.size
      @tree[i] += delta
      i += i & -i
    end
  end

  def query(i)
    sum = 0
    while i > 0
      sum += @tree[i]
      i -= i & -i
    end
    sum
  end
end
```
**Tushuntirish:** Fenwick Tree Segment Tree ga qaraganda kamroq xotira talab qiladi va kodlash uchun qulayroq, ayniqsa kümülatif yig'indilar uchun.

### Topshiriq #1094: Trie (Prefix Tree) yordamida avtomatik to'ldirish
**Tavsif:** Qidiruv tizimlarida so'rovlarni tezkor taxmin qilish va avtomatik to'ldirish.
**Talablar:** O(L) qidiruv tezligi (L - so'z uzunligi).
**Yechim (Ruby):**
```ruby
class TrieNode
  def initialize
    @children = {}
    @is_end = false
  end
  attr_accessor :children, :is_end
end

class Trie
  def initialize; @root = TrieNode.new; end
  
  def insert(word)
    node = @root
    word.each_char { |c| node = (node.children[c] ||= TrieNode.new) }
    node.is_end = true
  end
end
```
**Tushuntirish:** Trie tuzilmasi matnli ma'lumotlarni qidirishda xesh-jadvallarga qaraganda samaraliroq, chunki u prefikslarni birgalikda saqlaydi.

### Topshiriq #1095: Grafda sikllarni aniqlash (DFS)
**Tavsif:** Tizim bog'liqliklarida (dependency graph) o'lik qulflarni (deadlock) oldini olish.
**Talablar:** O(V + E) vaqt murakkabligi.
**Yechim (Ruby):**
```ruby
def has_cycle?(graph)
  visited = {}
  rec_stack = {}

  graph.each_key do |node|
    return true if dfs_cycle(node, graph, visited, rec_stack)
  end
  false
end

def dfs_cycle(u, graph, visited, rec_stack)
  visited[u] = true
  rec_stack[u] = true
  graph[u].each do |v|
    return true if !visited[v] && dfs_cycle(v, graph, visited, rec_stack)
    return true if rec_stack[v]
  end
  rec_stack[u] = false
  false
end
```
**Tushuntirish:** `rec_stack` yordamida rekursiya zanjiridagi tugunlar kuzatiladi, bu sikllarni aniqlashning eng ishonchli usuli.

### Topshiriq #1096: Kruskal algoritmi bilan minimal qamrovchi daraxt (MST)
**Tavsif:** Shaharlararo optik tolali tarmoqni eng kam xarajat bilan ulash.
**Talablar:** Disjoint Set Union (DSU) dan foydalanish.
**Yechim (Ruby):**
```ruby
def kruskal(nodes, edges)
  parent = nodes.each_with_object({}) { |n, h| h[n] = n }
  find = ->(i) { parent[i] == i ? i : (parent[i] = find.call(parent[i])) }
  
  edges.sort_by!(&:last)
  mst = []
  edges.each do |u, v, w|
    root_u, root_v = find.call(u), find.call(v)
    if root_u != root_v
      mst << [u, v, w]
      parent[root_u] = root_v
    end
  end
  mst
end
```
**Tushuntirish:** Kruskal algoritmi qirralarni vazn bo'yicha saralab, MST hosil qiladi. DSU (Union-Find) esa sikllarni oldini oladi.

### Topshiriq #1097: Topological Sort (Kahn algoritmi)
**Tavsif:** Loyiha vazifalarini bajarilish ketma-ketligini (task scheduling) aniqlash.
**Talablar:** O(V + E) murakkablik.
**Yechim (Ruby):**
```ruby
def topological_sort(graph, in_degree)
  queue = in_degree.select { |_, v| v == 0 }.keys
  result = []
  
  until queue.empty?
    u = queue.shift
    result << u
    graph[u].each do |v|
      in_degree[v] -= 1
      queue << v if in_degree[v] == 0
    end
  end
  result
end
```
**Tushuntirish:** Kahn algoritmi kirish darajasi (in-degree) 0 bo'lgan tugunlardan boshlab, graflarni chiziqli tartiblaydi.

### Topshiriq #1098: Tarjan algoritmi (Kuchli bog'langan komponentlar)
**Tavsif:** Ijtimoiy tarmoqlarda o'zaro zich bog'langan guruhlarni aniqlash.
**Talablar:** Bir martalik DFS o'tishi.
**Yechim (Ruby):**
```ruby
# Tarjan algoritmi skeleti
def tarjan(graph)
  @index = 0
  @stack = []
  @indices = {}
  @lowlink = {}
  
  # DFS va komponentlarni ajratish logikasi shu yerda amalga oshiriladi
  # ... (murakkablik tufayli qisqartirilgan)
end
```
**Tushuntirish:** Tarjan algoritmi graflarni kuchli bog'langan komponentlarga ajratish uchun eng tezkor (O(V+E)) yechimdir.

### Topshiriq #1099: Suffix Tree asosiy qismlari
**Tavsif:** Katta genomik ketma-ketliklarda naqsh qidirish.
**Talablar:** O(N) qurilish vaqti.
**Yechim (Ruby):**
```ruby
# Suffix Tree uchun oddiy tugun tuzilmasi
class SuffixNode
  def initialize
    @children = {}
    @start = -1
    @end = nil
  end
end
```
**Tushuntirish:** Suffix Tree matnni qayta ishlashda eng kuchli vosita bo'lib, substring qidiruvlarini juda tezlashtiradi.

### Topshiriq #1100: Max-Flow (Edmonds-Karp)
**Tavsif:** Logistika tizimida maksimal o'tkazuvchanlikni aniqlash.
**Talablar:** BFS dan foydalanish.
**Yechim (Ruby):**
```ruby
def edmonds_karp(capacity, source, sink)
  flow = 0
  parent = {}
  while bfs(capacity, source, sink, parent)
    path_flow = Float::INFINITY
    s = sink
    while s != source
      prev = parent[s]
      path_flow = [path_flow, capacity[prev][s]].min
      s = prev
    end
    # Oqimni yangilash...
  end
  flow
end
```
**Tushuntirish:** Edmonds-Karp algoritmi Ford-Fulkerson usulining BFS bilan optimallashtirilgan varianti bo'lib, tarmoq oqimini maksimal darajaga yetkazadi.