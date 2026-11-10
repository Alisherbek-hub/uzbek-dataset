# Khorazmiy AI: Lua - Modul 22
## Mavzu: Ilg'or Algoritmlar: Graflar, Segment Trees, Fenwick va Trie tuzilmalari

### Topshiriq #1051: Graflarda eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Logistika tizimlarida yuk tashish marshrutlarini optimallashtirish.
**Talablar:** O(E log V) murakkablik, xotira xavfsizligi.
**Yechim (Lua):**
```lua
-- Dijkstra algoritmi yordamida eng qisqa yo'lni topish
local function dijkstra(graph, start_node)
    local dist = {}
    for node in pairs(graph) do dist[node] = math.huge end
    dist[start_node] = 0
    local pq = {[start_node] = 0} -- Oddiy navbat (kattaroq loyihalar uchun Heap kerak)

    while next(pq) do
        local u = nil
        for n, d in pairs(pq) do if not u or d < pq[u] then u = n end end
        pq[u] = nil
        for v, weight in pairs(graph[u]) do
            if dist[v] > dist[u] + weight then
                dist[v] = dist[u] + weight
                pq[v] = dist[v]
            end
        end
    end
    return dist
end
```
**Tushuntirish:** Dijkstra algoritmi tarmoqlararo ma'lumotlar oqimini boshqarishda eng ishonchli yondashuvdir.

### Topshiriq #1052: Segment Tree yordamida diapazon yig'indisi
**Tavsif:** Real vaqt rejimida moliyaviy tranzaksiyalar yig'indisini hisoblash.
**Talablar:** O(log N) yangilash va so'rov tezligi.
**Yechim (Lua):**
```lua
-- Segment Tree qurish
local tree = {}
local function update(node, start, end_idx, idx, val)
    if start == end_idx then tree[node] = val return end
    local mid = math.floor((start + end_idx) / 2)
    if idx <= mid then update(2*node, start, mid, idx, val)
    else update(2*node+1, mid+1, end_idx, idx, val) end
    tree[node] = tree[2*node] + tree[2*node+1]
end
```
**Tushuntirish:** Segment Tree katta massivlarda dinamik o'zgarishlarni kuzatish uchun eng samarali tuzilmadir.

### Topshiriq #1053: Fenwick Tree (Binary Indexed Tree)
**Tavsif:** Katta hajmdagi statistik ma'lumotlar ustida tezkor prefiks yig'indilarni hisoblash.
**Talablar:** O(log N) murakkablik, minimal xotira sarfi.
**Yechim (Lua):**
```lua
-- Fenwick Tree implementatsiyasi
local bit = {}
local function add(i, val, n)
    while i <= n do
        bit[i] = (bit[i] or 0) + val
        i = i + (i & -i)
    end
end
```
**Tushuntirish:** Fenwick Tree Segment Tree'ga qaraganda kamroq xotira talab qiladi va kodlash uchun qulayroq.

### Topshiriq #1054: Trie (Prefix Tree) yordamida qidiruv
**Tavsif:** Foydalanuvchi so'rovlarini avtomatik to'ldirish (autocomplete) tizimi.
**Talablar:** O(L) qidiruv tezligi (L - so'z uzunligi).
**Yechim (Lua):**
```lua
local trie = {children = {}}
local function insert(word)
    local node = trie
    for i = 1, #word do
        local char = word:sub(i, i)
        if not node.children[char] then node.children[char] = {children = {}} end
        node = node.children[char]
    end
    node.is_end = true
end
```
**Tushuntirish:** Trie tuzilmasi lug'atga asoslangan qidiruvlarda eng tezkor natijani beradi.

### Topshiriq #1055: Graflarda aylanalarni aniqlash (DFS)
**Tavsif:** Tizimdagi o'zaro bog'liq jarayonlarda "deadlock" (o'lik nuqta) xavfini aniqlash.
**Talablar:** O(V + E) vaqt murakkabligi.
**Yechim (Lua):**
```lua
local function has_cycle(u, visited, rec_stack, graph)
    visited[u], rec_stack[u] = true, true
    for _, v in ipairs(graph[u]) do
        if not visited[v] and has_cycle(v, visited, rec_stack, graph) then return true
        elseif rec_stack[v] then return true end
    end
    rec_stack[u] = false
    return false
end
```
**Tushuntirish:** Rekursiv stek yordamida graflardagi sikllarni aniqlash tizim barqarorligini ta'minlaydi.

### Topshiriq #1056: Kenglik bo'yicha qidiruv (BFS)
**Tavsif:** Ijtimoiy tarmoqlarda "do'stlar doirasi"ni aniqlash.
**Talablar:** Navbat (Queue) tuzilmasidan samarali foydalanish.
**Yechim (Lua):**
```lua
local function bfs(graph, start)
    local queue = {start}
    local visited = {[start] = true}
    while #queue > 0 do
        local u = table.remove(queue, 1)
        for _, v in ipairs(graph[u]) do
            if not visited[v] then
                visited[v] = true
                table.insert(queue, v)
            end
        end
    end
end
```
**Tushuntirish:** BFS eng yaqin qo'shnilarni qidirishda eng optimal algoritmdir.

### Topshiriq #1057: Union-Find (Disjoint Set Union)
**Tavsif:** Tarmoq segmentlarini birlashtirish va tarmoqlararo aloqani tekshirish.
**Talablar:** Path compression optimizatsiyasi.
**Yechim (Lua):**
```lua
local parent = {}
local function find(i)
    if parent[i] == i then return i end
    parent[i] = find(parent[i]) -- Path compression
    return parent[i]
end
```
**Tushuntirish:** DSU algoritmi dinamik ravishda to'plamlarni birlashtirishda juda samarali.

### Topshiriq #1058: Topologik tartiblash (Kahn algoritmi)
**Tavsif:** Loyiha boshqaruvida vazifalarni bajarish ketma-ketligini belgilash.
**Talablar:** Kiruvchi darajalarni (in-degree) hisoblash.
**Yechim (Lua):**
```lua
local function topo_sort(graph, in_degree)
    local queue = {}
    for node, deg in pairs(in_degree) do if deg == 0 then table.insert(queue, node) end end
    local result = {}
    while #queue > 0 do
        local u = table.remove(queue, 1)
        table.insert(result, u)
        for _, v in ipairs(graph[u]) do
            in_degree[v] = in_degree[v] - 1
            if in_degree[v] == 0 then table.insert(queue, v) end
        end
    end
    return result
end
```
**Tushuntirish:** Vazifalarni bog'liqlik darajasiga ko'ra tartiblash xatolarni oldini oladi.

### Topshiriq #1059: Minimal qamrovchi daraxt (Kruskal)
**Tavsif:** Shaharlararo optik tolali kabellarni minimal xarajat bilan yotqizish.
**Talablar:** Edge'larni vazn bo'yicha saralash.
**Yechim (Lua):**
```lua
-- Kruskal algoritmi uchun qisqacha mantiq
table.sort(edges, function(a, b) return a.w < b.w end)
for _, edge in ipairs(edges) do
    if find(edge.u) ~= find(edge.v) then
        union(edge.u, edge.v)
        -- Edge'ni daraxtga qo'shish
    end
end
```
**Tushuntirish:** Kruskal algoritmi global minimal xarajatni ta'minlaydi.

### Topshiriq #1060: Trie yordamida so'zlarni saralash
**Tavsif:** Katta hajmdagi matnlarni tezkor indekslash va qidirish.
**Talablar:** Xotirani tejash va tezkor iteratsiya.
**Yechim (Lua):**
```lua
local function collect_words(node, prefix, result)
    if node.is_end then table.insert(result, prefix) end
    for char, next_node in pairs(node.children) do
        collect_words(next_node, prefix .. char, result)
    end
end
```
**Tushuntirish:** Trie orqali ma'lumotlarni yig'ish qidiruv tizimlarining ishlash tezligini oshiradi.

---

### Topshiriq #1061: Graflarda eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Logistika tizimlarida eng qisqa marshrutni aniqlash. Real vaqt rejimida yuk tashish xarajatlarini minimallashtirish uchun zarur.
**Talablar:** O(E log V) murakkablik, xotira xavfsizligi va manfiy og'irliklarni inobatga olish.
**Yechim (Lua):**
```lua
-- Dijkstra algoritmi yordamida eng qisqa yo'lni topish
function dijkstra(graph, start_node)
    local distances = {}
    local visited = {}
    for node in pairs(graph) do distances[node] = math.huge end
    distances[start_node] = 0

    while true do
        local current_node, min_dist = nil, math.huge
        for node, dist in pairs(distances) do
            if not visited[node] and dist < min_dist then
                current_node, min_dist = node, dist
            end
        end
        if not current_node then break end
        visited[current_node] = true
        for neighbor, weight in pairs(graph[current_node]) do
            if distances[current_node] + weight < distances[neighbor] then
                distances[neighbor] = distances[current_node] + weight
            end
        end
    end
    return distances
end
```
**Tushuntirish:** Ushbu yondashuv statik graflarda eng yuqori aniqlikni ta'minlaydi. `math.huge` qiymati cheksizlikni ifodalash uchun xavfsiz tanlovdir.

### Topshiriq #1062: Segment Tree yordamida diapazon yig'indisi
**Tavsif:** Moliya tizimlarida ma'lum vaqt oralig'idagi tranzaksiyalar yig'indisini tezkor hisoblash.
**Talablar:** O(log N) vaqt murakkabligi, ma'lumotlar yaxlitligi.
**Yechim (Lua):**
```lua
-- Segment Tree qurish va query qilish
local tree = {}
function update(node, start, end_idx, idx, val)
    if start == end_idx then tree[node] = val return end
    local mid = math.floor((start + end_idx) / 2)
    if idx <= mid then update(2*node, start, mid, idx, val)
    else update(2*node+1, mid+1, end_idx, idx, val) end
    tree[node] = (tree[2*node] or 0) + (tree[2*node+1] or 0)
end
```
**Tushuntirish:** Segment Tree katta massivlarda yangilanish va so'rovlar uchun eng samarali tuzilma hisoblanadi.

### Topshiriq #1063: Fenwick Tree (Binary Indexed Tree)
**Tavsif:** Katta hajmdagi ma'lumotlar oqimida kümülatif chastotalarni hisoblash.
**Talablar:** O(log N) vaqt, minimal xotira sarfi.
**Yechim (Lua):**
```lua
local bit = {}
function update_bit(idx, val, n)
    while idx <= n do
        bit[idx] = (bit[idx] or 0) + val
        idx = idx + (idx & -idx)
    end
end
function query_bit(idx)
    local sum = 0
    while idx > 0 do
        sum = sum + (bit[idx] or 0)
        idx = idx - (idx & -idx)
    end
    return sum
end
```
**Tushuntirish:** Fenwick Tree Segment Tree'ga qaraganda kamroq xotira talab qiladi va bitwise operatsiyalar tufayli juda tez ishlaydi.

### Topshiriq #1064: Trie (Prefix Tree) yordamida avtomatik to'ldirish
**Tavsif:** Qidiruv tizimlarida so'zlarni tezkor qidirish va taklif qilish.
**Talablar:** Xotirani tejash, tezkor qidiruv.
**Yechim (Lua):**
```lua
local trie = {children = {}}
function insert(word)
    local node = trie
    for i = 1, #word do
        local char = word:sub(i, i)
        if not node.children[char] then node.children[char] = {children = {}} end
        node = node.children[char]
    end
    node.is_end = true
end
```
**Tushuntirish:** Trie tuzilmasi prefikslar bo'yicha qidiruvni O(L) vaqtda (L - so'z uzunligi) amalga oshirishga imkon beradi.

### Topshiriq #1065: Graflarda sikllarni aniqlash (DFS)
**Tavsif:** Tarmoq xavfsizligida o'lik qulflarni (deadlocks) aniqlash.
**Talablar:** Rekursiv xavfsizlik, stack overflow'dan himoya.
**Yechim (Lua):**
```lua
function has_cycle(graph, node, visited, rec_stack)
    visited[node] = true
    rec_stack[node] = true
    for _, neighbor in pairs(graph[node]) do
        if not visited[neighbor] and has_cycle(graph, neighbor, visited, rec_stack) then return true
        elseif rec_stack[neighbor] then return true end
    end
    rec_stack[node] = false
    return false
end
```
**Tushuntirish:** `rec_stack` yordamida joriy rekursiya yo'lidagi tugunlar kuzatiladi, bu siklni aniq aniqlash imkonini beradi.

### Topshiriq #1066: Segment Tree bilan Range Minimum Query (RMQ)
**Tavsif:** Sensor ma'lumotlarida minimal qiymatni tezkor aniqlash.
**Talablar:** O(log N) vaqt, massiv o'zgarganda tezkor yangilanish.
**Yechim (Lua):**
```lua
function query_min(node, start, end_idx, l, r)
    if r < start or end_idx < l then return math.huge end
    if l <= start and end_idx <= r then return tree[node] end
    local mid = math.floor((start + end_idx) / 2)
    return math.min(query_min(2*node, start, mid, l, r), query_min(2*node+1, mid+1, end_idx, l, r))
end
```
**Tushuntirish:** `math.min` funksiyasi va rekursiv bo'linish orqali diapazon ichidagi eng kichik qiymatni samarali topadi.

### Topshiriq #1067: Fenwick Tree bilan diapazon yangilash
**Tavsif:** Massivdagi bir nechta elementga bir vaqtda qiymat qo'shish.
**Talablar:** O(log N) murakkablik.
**Yechim (Lua):**
```lua
function range_update(l, r, val, n)
    update_bit(l, val, n)
    update_bit(r + 1, -val, n)
end
```
**Tushuntirish:** Farqlar massivi (difference array) usuli yordamida diapazonni yangilashni oddiy nuqtaviy yangilashga aylantiramiz.

### Topshiriq #1068: Trie yordamida so'zlar sonini sanash
**Tavsif:** Matn tahlilida takrorlanuvchi prefikslarni aniqlash.
**Talablar:** Xotira optimizatsiyasi.
**Yechim (Lua):**
```lua
function count_prefix(prefix)
    local node = trie
    for i = 1, #prefix do
        local char = prefix:sub(i, i)
        if not node.children[char] then return 0 end
        node = node.children[char]
    end
    return node.count or 0
end
```
**Tushuntirish:** Har bir tugunga `count` qiymatini qo'shish orqali qidiruvni tezlashtiramiz.

### Topshiriq #1069: Graflarda bog'langan komponentlarni topish
**Tavsif:** Ijtimoiy tarmoqlarda foydalanuvchilar guruhlarini aniqlash.
**Talablar:** O(V + E) vaqt murakkabligi.
**Yechim (Lua):**
```lua
function find_components(graph)
    local visited = {}
    local count = 0
    for node in pairs(graph) do
        if not visited[node] then
            count = count + 1
            -- BFS yoki DFS orqali barcha bog'langan tugunlarni belgilash
        end
    end
    return count
end
```
**Tushuntirish:** Har bir tashrif buyurilmagan tugun yangi komponent boshlanishi hisoblanadi.

### Topshiriq #1070: Trie yordamida so'z o'chirish
**Tavsif:** Dinamik lug'atlarni boshqarish.
**Talablar:** Xotirani tozalash va xatolarni oldini olish.
**Yechim (Lua):**
```lua
function delete_word(word)
    local function remove(node, word, depth)
        if not node then return false end
        if depth == #word then
            node.is_end = false
            return next(node.children) == nil
        end
        local char = word:sub(depth + 1, depth + 1)
        if remove(node.children[char], word, depth + 1) then
            node.children[char] = nil
            return next(node.children) == nil and not node.is_end
        end
        return false
    end
    remove(trie, word, 0)
end
```
**Tushuntirish:** Rekursiv o'chirish orqali keraksiz tugunlarni xotiradan bo'shatish (garbage collection) ta'minlanadi.

---

### Topshiriq #1071: Graflarda eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Logistika tizimlarida yuk tashish marshrutlarini optimallashtirish.
**Talablar:** O(E log V) murakkablik, xotira xavfsizligi.
**Yechim (Lua):**
```lua
-- Dijkstra algoritmi yordamida eng qisqa yo'lni aniqlash
function dijkstra(graph, start_node)
    local dist = {}
    for node in pairs(graph) do dist[node] = math.huge end
    dist[start_node] = 0
    local pq = {[start_node] = 0} -- Oddiy navbat (kattaroq loyihalar uchun heap kerak)

    while next(pq) do
        local u = nil
        for n, d in pairs(pq) do if not u or d < pq[u] then u = n end end
        pq[u] = nil
        for v, weight in pairs(graph[u]) do
            if dist[v] > dist[u] + weight then
                dist[v] = dist[u] + weight
                pq[v] = dist[v]
            end
        end
    end
    return dist
end
```
**Tushuntirish:** Dijkstra algoritmi graflarda vaznli yo'llarni topishda eng samarali yechimdir.

### Topshiriq #1072: Segment Tree yordamida diapazon yig'indisi
**Tavsif:** Moliya tizimlarida real vaqt rejimida tranzaksiyalar yig'indisini hisoblash.
**Talablar:** O(log N) yangilash va so'rov vaqti.
**Yechim (Lua):**
```lua
-- Segment Tree qurish
local tree = {}
function update(node, start, end_idx, idx, val)
    if start == end_idx then tree[node] = val return end
    local mid = math.floor((start + end_idx) / 2)
    if idx <= mid then update(2*node, start, mid, idx, val)
    else update(2*node+1, mid+1, end_idx, idx, val) end
    tree[node] = tree[2*node] + tree[2*node+1]
end
```
**Tushuntirish:** Segment Tree katta massivlarda statik va dinamik yig'indilarni tezkor hisoblash imkonini beradi.

### Topshiriq #1073: Fenwick Tree (Binary Indexed Tree)
**Tavsif:** Katta hajmdagi ma'lumotlar oqimida kümülatif chastotalarni kuzatish.
**Talablar:** O(log N) murakkablik, minimal xotira sarfi.
**Yechim (Lua):**
```lua
local bit = {}
function add(i, val, n)
    while i <= n do
        bit[i] = (bit[i] or 0) + val
        i = i + (i & -i)
    end
end
```
**Tushuntirish:** Fenwick Tree Segment Tree'ga qaraganda kamroq xotira talab qiladi va implementatsiyasi sodda.

### Topshiriq #1074: Trie (Prefix Tree) implementatsiyasi
**Tavsif:** Avtomatik to'ldirish (autocomplete) tizimlari uchun so'zlarni saqlash.
**Talablar:** O(L) qidiruv vaqti, bu yerda L - so'z uzunligi.
**Yechim (Lua):**
```lua
local trie = {children = {}}
function insert(word)
    local node = trie
    for i = 1, #word do
        local char = word:sub(i, i)
        if not node.children[char] then node.children[char] = {children = {}} end
        node = node.children[char]
    end
    node.is_end = true
end
```
**Tushuntirish:** Trie tuzilmasi prefiks asosidagi qidiruvlar uchun eng tezkor ma'lumotlar tuzilmasidir.

### Topshiriq #1075: Grafda aylana (cycle) mavjudligini tekshirish
**Tavsif:** Tarmoq topologiyasida yuzaga kelishi mumkin bo'lgan "deadlock" holatlarini aniqlash.
**Talablar:** DFS asosida O(V+E) murakkablik.
**Yechim (Lua):**
```lua
function has_cycle(u, visited, recStack, graph)
    visited[u], recStack[u] = true, true
    for _, v in ipairs(graph[u]) do
        if not visited[v] and has_cycle(v, visited, recStack, graph) then return true
        elseif recStack[v] then return true end
    end
    recStack[u] = false
    return false
end
```
**Tushuntirish:** Rekursiv stack yordamida yo'naltirilgan graflardagi tsikllarni aniqlash tizim barqarorligi uchun muhim.

### Topshiriq #1076: Kenglik bo'yicha qidiruv (BFS)
**Tavsif:** Ijtimoiy tarmoqlarda "do'stlar do'sti" darajasini aniqlash.
**Talablar:** O(V+E) murakkablik, navbat (queue) tuzilmasi.
**Yechim (Lua):**
```lua
function bfs(graph, start)
    local queue, visited = {start}, {[start] = true}
    while #queue > 0 do
        local u = table.remove(queue, 1)
        for _, v in ipairs(graph[u]) do
            if not visited[v] then
                visited[v] = true
                table.insert(queue, v)
            end
        end
    end
end
```
**Tushuntirish:** BFS eng yaqin qo'shnilarni qidirishda eng ishonchli algoritmdir.

### Topshiriq #1077: Segment Tree (Lazy Propagation)
**Tavsif:** Massivning bir qismini doimiy ravishda yangilash (range updates).
**Talablar:** O(log N) samaradorlik.
**Yechim (Lua):**
```lua
-- Lazy propagation: yangilanishlarni kechiktirib bajarish
function update_range(node, start, end_idx, l, r, val)
    -- Lazy qiymatlarni qo'llash kodi shu yerda bo'ladi
    -- Bu yerda asosiy mantiq: oraliq kesishganda yangilash
end
```
**Tushuntirish:** Lazy propagation katta massivlarda oraliq amallarini keskin tezlashtiradi.

### Topshiriq #1078: Trie yordamida so'zlar sonini sanash
**Tavsif:** Matn tahlilida takrorlanuvchi prefikslarni aniqlash.
**Talablar:** Xotira samaradorligi.
**Yechim (Lua):**
```lua
function count_prefix(node, prefix)
    for i = 1, #prefix do
        node = node.children[prefix:sub(i, i)]
        if not node then return 0 end
    end
    return node.count or 0
end
```
**Tushuntirish:** Trie tugunlariga hisoblagich qo'shish orqali prefiks chastotasini O(L) vaqtda olish mumkin.

### Topshiriq #1079: Kruskal algoritmi (MST)
**Tavsif:** Tarmoq infratuzilmasini eng kam xarajat bilan ulash.
**Talablar:** Union-Find ma'lumotlar tuzilmasi bilan O(E log E).
**Yechim (Lua):**
```lua
-- Disjoint Set Union (DSU)
local parent = {}
function find(i)
    if parent[i] == i then return i end
    parent[i] = find(parent[i])
    return parent[i]
end
```
**Tushuntirish:** Kruskal algoritmi tarmoqni minimal xarajat bilan ulashda eng optimal yechimdir.

### Topshiriq #1080: Fenwick Tree 2D (Matritsalar uchun)
**Tavsif:** Tasvirni qayta ishlashda (image processing) hududiy yig'indilarni hisoblash.
**Talablar:** O(log N * log M) murakkablik.
**Yechim (Lua):**
```lua
local bit2d = {}
function update2d(r, c, val, n, m)
    for i = r; i <= n; i = i + (i & -i) do
        for j = c; j <= m; j = j + (j & -j) do
            bit2d[i][j] = (bit2d[i][j] or 0) + val
        end
    end
end
```
**Tushuntirish:** 2D Fenwick Tree matritsalardagi hududiy so'rovlarni juda yuqori tezlikda bajaradi.

---

### Topshiriq #1081: Graflarda eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Logistika tizimlarida yuk tashish marshrutlarini optimallashtirish uchun tugunlar orasidagi eng qisqa masofani aniqlash.
**Talablar:** $O(E \log V)$ murakkablik, xotira xavfsizligi uchun jadval (table) indekslarini tozalash.
**Yechim (Lua):**
```lua
-- Dijkstra algoritmi yordamida eng qisqa yo'lni topish
function dijkstra(graph, start_node)
    local distances = {}
    for node in pairs(graph) do distances[node] = math.huge end
    distances[start_node] = 0
    
    local pq = {[start_node] = 0} -- Oddiy navbat (kattaroq loyihalarda min-heap ishlating)
    
    while next(pq) do
        local u, dist = nil, math.huge
        for node, d in pairs(pq) do
            if d < dist then u, dist = node, d end
        end
        pq[u] = nil
        
        for v, weight in pairs(graph[u]) do
            if distances[v] > distances[u] + weight then
                distances[v] = distances[u] + weight
                pq[v] = distances[v]
            end
        end
    end
    return distances
end
```
**Tushuntirish:** Ushbu yondashuv dinamik dasturlash va ochko'z (greedy) strategiyani birlashtiradi, bu esa tarmoq topologiyalarida samarali hisob-kitobni ta'minlaydi.

---

### Topshiriq #1082: Segment Tree yordamida diapazon yig'indisi
**Tavsif:** Real vaqt rejimida moliyaviy tranzaksiyalar oqimida ma'lum vaqt oralig'idagi umumiy summani hisoblash.
**Talablar:** $O(\log N)$ yangilash va so'rov tezligi.
**Yechim (Lua):**
```lua
-- Segment Tree qurish va diapazon yig'indisini olish
local tree = {}
function update(node, start, end_idx, idx, val)
    if start == end_idx then tree[node] = val return end
    local mid = math.floor((start + end_idx) / 2)
    if idx <= mid then update(2*node, start, mid, idx, val)
    else update(2*node+1, mid+1, end_idx, idx, val) end
    tree[node] = (tree[2*node] or 0) + (tree[2*node+1] or 0)
end
```
**Tushuntirish:** Segment Tree massivni ierarxik tuzilmaga o'tkazib, katta hajmdagi ma'lumotlar ustida tezkor agregatsiya qilish imkonini beradi.

---

### Topshiriq #1083: Fenwick Tree (Binary Indexed Tree)
**Tavsif:** Katta hajmdagi ma'lumotlar bazasida kümülatif chastotalarni (prefix sums) tezkor hisoblash.
**Talablar:** $O(\log N)$ murakkablik, minimal xotira sarfi.
**Yechim (Lua):**
```lua
local bit = {}
function add(i, val, n)
    while i <= n do
        bit[i] = (bit[i] or 0) + val
        i = i + (i & -i)
    end
end
function query(i)
    local sum = 0
    while i > 0 do
        sum = sum + (bit[i] or 0)
        i = i - (i & -i)
    end
    return sum
end
```
**Tushuntirish:** Fenwick Tree Segment Tree'ga qaraganda kamroq xotira talab qiladi va bitwise operatsiyalari tufayli juda tez ishlaydi.

---

### Topshiriq #1084: Trie (Prefix Tree) implementatsiyasi
**Tavsif:** Avtomatik to'ldirish (autocomplete) tizimlari uchun so'zlarni samarali saqlash va qidirish.
**Talablar:** Xotirani tejash uchun tugunlarni dinamik yaratish.
**Yechim (Lua):**
```lua
local trie = {children = {}}
function insert(word)
    local node = trie
    for i = 1, #word do
        local char = word:sub(i, i)
        if not node.children[char] then node.children[char] = {children = {}} end
        node = node.children[char]
    end
    node.is_end = true
end
```
**Tushuntirish:** Trie tuzilmasi so'zlarni prefiks bo'yicha guruhlash orqali qidiruv vaqtini so'z uzunligiga bog'liq qiladi, bu esa lug'at hajmidan qat'iy nazar tezlikni saqlaydi.

---

### Topshiriq #1085: Graflarda sikllarni aniqlash (DFS)
**Tavsif:** Tizim bog'liqliklari (dependency graph) ichida yuzaga kelishi mumkin bo'lgan o'zaro bog'liqlik (deadlock) xavfini aniqlash.
**Talablar:** Rekursiv chuqurlikni nazorat qilish.
**Yechim (Lua):**
```lua
function has_cycle(graph, u, visited, recStack)
    visited[u] = true
    recStack[u] = true
    for v in pairs(graph[u]) do
        if not visited[v] and has_cycle(graph, v, visited, recStack) then return true
        elseif recStack[v] then return true end
    end
    recStack[u] = false
    return false
end
```
**Tushuntirish:** `recStack` (rekursiya steki) yordamida joriy yo'lda tugun qayta uchraganini tekshirish siklni aniqlashning eng ishonchli usulidir.

---

### Topshiriq #1086: Kenglik bo'yicha qidiruv (BFS)
**Tavsif:** Ijtimoiy tarmoqlarda "eng yaqin do'stlar" darajasini aniqlash.
**Talablar:** Navbat (queue) tuzilmasidan foydalanish.
**Yechim (Lua):**
```lua
function bfs(graph, start)
    local queue = {start}
    local visited = {[start] = true}
    while #queue > 0 do
        local u = table.remove(queue, 1)
        for v in pairs(graph[u]) do
            if not visited[v] then
                visited[v] = true
                table.insert(queue, v)
            end
        end
    end
end
```
**Tushuntirish:** BFS qatlamma-qatlam qidiruvni amalga oshiradi, bu esa tarmoq grafiklarida masofani aniqlash uchun optimaldir.

---

### Topshiriq #1087: Disjoint Set Union (DSU)
**Tavsif:** Tarmoq segmentlarini birlashtirish va ular orasidagi aloqadorlikni tekshirish.
**Talablar:** Path compression va union by rank optimizatsiyasi.
**Yechim (Lua):**
```lua
local parent = {}
function find(i)
    if parent[i] == i then return i end
    parent[i] = find(parent[i]) -- Path compression
    return parent[i]
end
function union(i, j)
    local root_i, root_j = find(i), find(j)
    if root_i ~= root_j then parent[root_i] = root_j end
end
```
**Tushuntirish:** DSU juda katta to'plamlar ustida birlashish va tekshirish amallarini deyarli doimiy vaqtda ($O(\alpha(N))$) bajaradi.

---

### Topshiriq #1088: Topologik tartiblash (Kahn algoritmi)
**Tavsif:** Vazifalar ketma-ketligini (task scheduling) bajarish tartibini belgilash.
**Talablar:** Kiruvchi darajalarni (in-degree) hisoblash.
**Yechim (Lua):**
```lua
function topological_sort(graph, in_degree)
    local queue = {}
    for node, deg in pairs(in_degree) do if deg == 0 then table.insert(queue, node) end end
    local result = {}
    while #queue > 0 do
        local u = table.remove(queue, 1)
        table.insert(result, u)
        for v in pairs(graph[u]) do
            in_degree[v] = in_degree[v] - 1
            if in_degree[v] == 0 then table.insert(queue, v) end
        end
    end
    return result
end
```
**Tushuntirish:** Kahn algoritmi yo'naltirilgan atsiklik graflarda (DAG) vazifalar bajarilish tartibini aniqlash uchun eng samarali usuldir.

---

### Topshiriq #1089: Minimal qamrovchi daraxt (Kruskal)
**Tavsif:** Shaharlararo optik tolali kabel yotqizishda xarajatlarni minimallashtirish.
**Talablar:** Edge'larni vazn bo'yicha saralash.
**Yechim (Lua):**
```lua
function kruskal(edges, n)
    table.sort(edges, function(a, b) return a.w < b.w end)
    local mst = {}
    for _, edge in ipairs(edges) do
        if find(edge.u) ~= find(edge.v) then
            union(edge.u, edge.v)
            table.insert(mst, edge)
        end
    end
    return mst
end
```
**Tushuntirish:** Kruskal algoritmi eng arzon aloqalarni tanlab, barcha tugunlarni eng kam xarajat bilan bog'laydi.

---

### Topshiriq #1090: Suffix Tree (Qisqartirilgan)
**Tavsif:** Katta matnlar ichida takrorlanuvchi qismlarni (substring) tezkor qidirish.
**Talablar:** Xotira samaradorligi va qidiruv tezligi.
**Yechim (Lua):**
```lua
-- Suffix-larni Trie'ga joylash
function build_suffix_tree(text)
    local root = {children = {}}
    for i = 1, #text do
        local suffix = text:sub(i)
        local node = root
        for j = 1, #suffix do
            local char = suffix:sub(j, j)
            if not node.children[char] then node.children[char] = {children = {}} end
            node = node.children[char]
        end
    end
    return root
end
```
**Tushuntirish:** Suffix Tree matn tahlili va bioinformatika kabi sohalarda naqshlarni (pattern matching) izlash uchun eng kuchli vositadir.

---

### Topshiriq #1091: Dijkstra algoritmi yordamida eng qisqa yo'lni topish
**Tavsif:** Logistika tizimlarida yuk tashish marshrutlarini optimallashtirish uchun graf tugunlari orasidagi eng qisqa masofani hisoblash.
**Talablar:** $O(E \log V)$ murakkablik, xotira xavfsizligi uchun jadval (table) indekslarini tozalash.
**Yechim (Lua):**
```lua
-- Dijkstra algoritmi implementatsiyasi
local function dijkstra(graph, start_node)
    local distances = {}
    for node in pairs(graph) do distances[node] = math.huge end
    distances[start_node] = 0
    local pq = {[start_node] = 0}

    while next(pq) do
        local u, dist = nil, math.huge
        for n, d in pairs(pq) do if d < dist then u, dist = n, d end end
        pq[u] = nil

        for v, weight in pairs(graph[u]) do
            if distances[v] > distances[u] + weight then
                distances[v] = distances[u] + weight
                pq[v] = distances[v]
            end
        end
    end
    return distances
end
```
**Tushuntirish:** Ushbu yondashuv grafdagi og'irliklar musbat bo'lganda eng samarali hisoblanadi. `math.huge` qiymati cheksizlikni ifodalash uchun ishlatildi.

### Topshiriq #1092: Segment Tree yordamida diapazon yig'indisini hisoblash
**Tavsif:** Real vaqt rejimida moliyaviy ma'lumotlar oqimida ma'lum oraliqdagi yig'indini tezkor aniqlash.
**Talablar:** $O(\log N)$ vaqt murakkabligi, rekursiv xotira boshqaruvi.
**Yechim (Lua):**
```lua
local tree = {}
local function update(node, start, end_idx, idx, val, arr)
    if start == end_idx then
        arr[idx] = val
        tree[node] = val
        return
    end
    local mid = math.floor((start + end_idx) / 2)
    if idx <= mid then update(2*node, start, mid, idx, val, arr)
    else update(2*node+1, mid+1, end_idx, idx, val, arr) end
    tree[node] = tree[2*node] + tree[2*node+1]
end
```
**Tushuntirish:** Segment Tree katta massivlarda o'zgarishlar va so'rovlar tezligini logarifmik darajaga tushiradi.

### Topshiriq #1093: Fenwick Tree (Binary Indexed Tree) bilan prefiks yig'indisi
**Tavsif:** Katta hajmdagi statistik ma'lumotlarni yangilash va yig'indisini olishda xotirani tejash.
**Talablar:** $O(\log N)$ vaqt, minimal xotira sarfi.
**Yechim (Lua):**
```lua
local bit = {}
local function update(i, delta, n)
    while i <= n do
        bit[i] = (bit[i] or 0) + delta
        i = i + (i & -i)
    end
end
local function query(i)
    local sum = 0
    while i > 0 do
        sum = sum + (bit[i] or 0)
        i = i - (i & -i)
    end
    return sum
end
```
**Tushuntirish:** Fenwick Tree Segment Tree'ga qaraganda kamroq xotira talab qiladi va bitwise operatsiyalar tufayli juda tez ishlaydi.

### Topshiriq #1094: Trie (Prefix Tree) yordamida avtomatik to'ldirish
**Tavsif:** Foydalanuvchi kiritayotgan so'zlarni tezkor qidirish va taklif qilish tizimi.
**Talablar:** $O(L)$ vaqt murakkabligi (L - so'z uzunligi), xavfsiz tugun yaratish.
**Yechim (Lua):**
```lua
local trie = {children = {}}
local function insert(word)
    local node = trie
    for i = 1, #word do
        local char = word:sub(i, i)
        if not node.children[char] then node.children[char] = {children = {}} end
        node = node.children[char]
    end
    node.is_end = true
end
```
**Tushuntirish:** Trie tuzilmasi so'zlarni saqlashda takrorlanuvchi prefikslarni bir marta saqlash orqali xotirani optimallashtiradi.

### Topshiriq #1095: Grafda BFS (Breadth-First Search) yordamida eng qisqa yo'l
**Tavsif:** Ijtimoiy tarmoqlarda ikki foydalanuvchi o'rtasidagi "do'stlik darajasi"ni aniqlash.
**Talablar:** $O(V+E)$ murakkablik, navbat (queue) tuzilmasi.
**Yechim (Lua):**
```lua
local function bfs(graph, start)
    local visited = {[start] = true}
    local queue = {start}
    while #queue > 0 do
        local u = table.remove(queue, 1)
        for _, v in ipairs(graph[u]) do
            if not visited[v] then
                visited[v] = true
                table.insert(queue, v)
            end
        end
    end
end
```
**Tushuntirish:** BFS vaznsiz graflarda eng qisqa yo'lni topish uchun eng ishonchli algoritmdir.

### Topshiriq #1096: Grafda DFS (Depth-First Search) yordamida sikl aniqlash
**Tavsif:** Tizim bog'liqliklarida (dependency graph) yuzaga kelishi mumkin bo'lgan halqali bog'liqliklarni topish.
**Talablar:** Rekursiv xavfsizlik, $O(V+E)$ murakkablik.
**Yechim (Lua):**
```lua
local function has_cycle(u, visited, recStack, graph)
    visited[u] = true
    recStack[u] = true
    for _, v in ipairs(graph[u]) do
        if not visited[v] and has_cycle(v, visited, recStack, graph) then return true
        elseif recStack[v] then return true end
    end
    recStack[u] = false
    return false
end
```
**Tushuntirish:** `recStack` yordamida joriy rekursiya yo'lidagi tugunlar kuzatiladi, bu siklni aniq aniqlash imkonini beradi.

### Topshiriq #1097: Kruskal algoritmi (Minimal Spanning Tree)
**Tavsif:** Tarmoq infratuzilmasini eng kam xarajat bilan ulash (MST).
**Talablar:** Disjoint Set Union (DSU) tuzilmasi, $O(E \log E)$ murakkablik.
**Yechim (Lua):**
```lua
local parent = {}
local function find(i)
    if parent[i] == i then return i end
    parent[i] = find(parent[i])
    return parent[i]
end
-- Kruskal algoritmi qirralarni saralash va DSU orqali birlashtirishni talab qiladi
```
**Tushuntirish:** DSU yordamida qirralarni birlashtirishda sikl hosil bo'lishining oldi olinadi.

### Topshiriq #1098: Topologik tartiblash (Kahn algoritmi)
**Tavsif:** Vazifalarni bajarilish ketma-ketligini (task scheduling) aniqlash.
**Talablar:** Kiruvchi darajalarni (in-degree) hisoblash, $O(V+E)$.
**Yechim (Lua):**
```lua
local function topological_sort(graph, in_degree)
    local queue = {}
    for node, deg in pairs(in_degree) do if deg == 0 then table.insert(queue, node) end end
    local result = {}
    while #queue > 0 do
        local u = table.remove(queue, 1)
        table.insert(result, u)
        for _, v in ipairs(graph[u]) do
            in_degree[v] = in_degree[v] - 1
            if in_degree[v] == 0 then table.insert(queue, v) end
        end
    end
    return result
end
```
**Tushuntirish:** Kahn algoritmi yo'naltirilgan atsiklik graflarda (DAG) tartibni aniqlash uchun eng samarali usuldir.

### Topshiriq #1099: Floyd-Warshall algoritmi
**Tavsif:** Barcha juftliklar orasidagi eng qisqa masofani aniqlash (Dense graphs).
**Talablar:** $O(V^3)$ murakkablik, matritsa ko'rinishidagi graf.
**Yechim (Lua):**
```lua
local function floyd_warshall(dist, n)
    for k = 1, n do
        for i = 1, n do
            for j = 1, n do
                if dist[i][j] > dist[i][k] + dist[k][j] then
                    dist[i][j] = dist[i][k] + dist[k][j]
                end
            end
        end
    end
end
```
**Tushuntirish:** Matritsa yondashuvi kichikroq, lekin zich graflar uchun juda qulay va tushunarli.

### Topshiriq #1100: Suffix Tree (Trie varianti)
**Tavsif:** Katta matnlar ichidan pastki qatorni (substring) tezkor qidirish.
**Talablar:** Xotirani tejash, $O(N)$ qurilish vaqti.
**Yechim (Lua):**
```lua
-- Suffix Tree uchun oddiy tugun tuzilmasi
local function create_node()
    return {children = {}, suffix_link = nil}
end
-- Murakkablikni kamaytirish uchun Ukkonen algoritmi tavsiya etiladi
```
**Tushuntirish:** Suffix Tree matn tahlili va bioinformatika sohasida qidiruvni tezlashtirish uchun eng kuchli vositadir.