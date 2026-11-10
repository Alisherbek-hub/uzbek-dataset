# Khorazmiy AI: R - Modul 22
## Mavzu: Ilg'or Algoritmlar: Graflar, Segment Trees, Fenwick va Trie tuzilmalari

### Topshiriq #1051: Graflarda eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Milliy logistika tarmog'ida shaharlararo yuk tashish xarajatlarini minimallashtirish.
**Talablar:** $O(E \log V)$ murakkablik, xotira xavfsizligi.
**Yechim (R):**
```r
library(igraph)
# Shaharlararo bog'liqlik grafigini yaratish
edges <- c(1,2, 10, 2,3, 5, 1,3, 20)
g <- graph(edges, directed = TRUE)
E(g)$weight <- c(10, 5, 20)

# Dijkstra algoritmi yordamida 1-tugundan 3-tugungacha eng qisqa yo'l
path <- shortest_paths(g, from = 1, to = 3, weights = E(g)$weight)
print(path$vpath)
```
**Tushuntirish:** `igraph` kutubxonasi C++ asosida yozilgan bo'lib, katta hajmdagi ma'lumotlar uchun eng tezkor yechim hisoblanadi.

### Topshiriq #1052: Segment Tree yordamida diapazon yig'indisi
**Tavsif:** Real vaqt rejimida milliy iqtisodiy ko'rsatkichlarning dinamik o'zgarishini kuzatish.
**Talablar:** $O(\log N)$ yangilash va so'rov vaqti.
**Yechim (R):**
```r
# Segment Tree funksiyasi
update_tree <- function(tree, idx, val, n) {
  idx <- idx + n
  tree[idx] <- val
  while (idx > 1) {
    idx <- idx %/% 2
    tree[idx] <- tree[2*idx] + tree[2*idx+1]
  }
  return(tree)
}
# 8 elementli daraxt uchun misol
n <- 8
tree <- numeric(2 * n)
tree <- update_tree(tree, 3, 15, n)
```
**Tushuntirish:** Segment Tree massivdagi o'zgarishlarni tezkor qayta ishlash uchun eng samarali tuzilmadir.

### Topshiriq #1053: Fenwick Tree (Binary Indexed Tree)
**Tavsif:** Katta hajmdagi tranzaksiyalar oqimida kümülatif yig'indilarni hisoblash.
**Talablar:** $O(\log N)$ murakkablik, minimal xotira sarfi.
**Yechim (R):**
```r
update_bit <- function(bit, idx, val) {
  while(idx <= length(bit)) {
    bit[idx] <- bit[idx] + val
    idx <- idx + (idx & -idx)
  }
  return(bit)
}
bit <- numeric(10)
bit <- update_bit(bit, 3, 5)
```
**Tushuntirish:** Fenwick Tree Segment Tree'ga qaraganda kamroq xotira talab qiladi va implementatsiyasi sodda.

### Topshiriq #1054: Trie (Prefix Tree) yordamida qidiruv
**Tavsif:** Milliy domenlar bazasida kalit so'zlarni tezkor qidirish.
**Talablar:** $O(L)$ qidiruv vaqti (L - so'z uzunligi).
**Yechim (R):**
```r
# Trie tuzilmasini listlar orqali ifodalash
trie <- list()
insert_trie <- function(trie, word) {
  node <- trie
  for (char in strsplit(word, "")[[1]]) {
    if (is.null(node[[char]])) node[[char]] <- list()
    node <- node[[char]]
  }
  node$end <- TRUE
  return(trie)
}
```
**Tushuntirish:** Trie tuzilmasi matnli ma'lumotlarni indekslashda xotirani tejash va tezlikni oshirish uchun optimaldir.

### Topshiriq #1055: Graflarda bog'langan komponentlarni aniqlash
**Tavsif:** Milliy elektr tarmoqlarining uzluksizligini tekshirish.
**Talablar:** $O(V+E)$ murakkablik.
**Yechim (R):**
```r
library(igraph)
g <- erdos.renyi.game(100, 0.05)
components <- components(g)
print(components$no) # Komponentlar soni
```
**Tushuntirish:** Tarmoqning uzilish nuqtalarini aniqlash uchun `components` funksiyasi eng ishonchli usuldir.

### Topshiriq #1056: Range Minimum Query (RMQ)
**Tavsif:** Sensor ma'lumotlarida minimal qiymatni tezkor aniqlash.
**Talablar:** $O(1)$ so'rov vaqti (oldindan ishlov berish bilan).
**Yechim (R):**
```r
# Sparse Table yondashuvi
data <- c(5, 2, 8, 1, 9)
n <- length(data)
st <- matrix(0, nrow = n, ncol = floor(log2(n)) + 1)
st[,1] <- data
# Sparse table to'ldirish logikasi...
```
**Tushuntirish:** RMQ statik ma'lumotlar to'plamida minimal qiymatni doimiy vaqtda topish imkonini beradi.

### Topshiriq #1057: Trie yordamida avto-to'ldirish
**Tavsif:** Foydalanuvchi so'rovlarini bashorat qilish tizimi.
**Talablar:** Xotira samaradorligi va tezkor javob.
**Yechim (R):**
```r
# Trie qidiruv funksiyasi
search_trie <- function(trie, prefix) {
  node <- trie
  for (char in strsplit(prefix, "")[[1]]) {
    if (is.null(node[[char]])) return(FALSE)
    node <- node[[char]]
  }
  return(TRUE)
}
```
**Tushuntirish:** Prefix qidiruvi foydalanuvchi tajribasini yaxshilash uchun eng tezkor algoritmdir.

### Topshiriq #1058: Topologik tartiblash (Kahn algoritmi)
**Tavsif:** Milliy loyihalarni amalga oshirish ketma-ketligini belgilash.
**Talablar:** Sikllarni aniqlash va tartiblash.
**Yechim (R):**
```r
library(igraph)
g <- graph(c(1,2, 2,3, 3,4))
topo_order <- topo_sort(g)
print(topo_order)
```
**Tushuntirish:** Loyiha boshqaruvida vazifalar o'rtasidagi bog'liqlikni vizuallashtirish va tartiblash uchun zarur.

### Topshiriq #1059: Fenwick Tree 2D
**Tavsif:** Geografik hududlar (matritsa) bo'yicha resurslarni taqsimlash.
**Talablar:** 2D maydonda yig'indini tez hisoblash.
**Yechim (R):**
```r
# 2D BIT uchun asosiy funksiya
update_bit2d <- function(bit2d, r, c, val) {
  i <- r
  while(i <= nrow(bit2d)) {
    j <- c
    while(j <= ncol(bit2d)) {
      bit2d[i, j] <- bit2d[i, j] + val
      j <- j + (j & -j)
    }
    i <- i + (i & -i)
  }
  return(bit2d)
}
```
**Tushuntirish:** 2D Fenwick Tree fazoviy ma'lumotlar tahlilida juda samarali.

### Topshiriq #1060: Minimum Spanning Tree (Prim)
**Tavsif:** Milliy infratuzilma (yo'l, quvur) qurilishida xarajatlarni minimallashtirish.
**Talablar:** $O(E \log V)$ murakkablik.
**Yechim (R):**
```r
library(igraph)
g <- make_full_graph(5)
E(g)$weight <- runif(10)
mst <- mst(g)
plot(mst)
```
**Tushuntirish:** Prim algoritmi tarmoqni eng kam xarajat bilan bog'lash uchun standart hisoblanadi.

---

### Topshiriq #1061: Graflarda eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Milliy logistika tarmog'ida shaharlararo yuk tashish xarajatlarini minimallashtirish.
**Talablar:** $O(E \log V)$ murakkablik, xotira xavfsizligi.
**Yechim (R):**
```r
library(igraph)
# Shaharlararo bog'liqlik grafigini yaratish
edges <- c("Toshkent", "Samarqand", 10, "Samarqand", "Buxoro", 15, "Toshkent", "Buxoro", 30)
g <- graph(edges = edges, directed = FALSE)
E(g)$weight <- c(10, 15, 30)

# Dijkstra algoritmi yordamida eng qisqa yo'lni topish
shortest_path <- distances(g, v = "Toshkent", to = "Buxoro", weights = E(g)$weight)
print(paste("Eng qisqa masofa:", shortest_path))
```
**Tushuntirish:** `igraph` kutubxonasi C++ asosida yozilgan bo'lib, katta hajmdagi tarmoqlar uchun eng yuqori unumdorlikni ta'minlaydi.

### Topshiriq #1062: Segment Tree yordamida diapazon yig'indisi
**Tavsif:** Real vaqt rejimida milliy iqtisodiy ko'rsatkichlar o'zgarishini kuzatish.
**Talablar:** $O(\log n)$ yangilash va so'rov vaqti.
**Yechim (R):**
```r
# Segment Tree funksiyasi
build_tree <- function(arr, node, start, end, tree) {
  if(start == end) { tree[node] <- arr[start]; return(tree) }
  mid <- (start + end) %/% 2
  tree <- build_tree(arr, 2*node, start, mid, tree)
  tree <- build_tree(arr, 2*node+1, mid+1, end, tree)
  tree[node] <- tree[2*node] + tree[2*node+1]
  return(tree)
}
data <- c(1, 3, 5, 7, 9, 11)
tree <- numeric(4 * length(data))
tree <- build_tree(data, 1, 1, length(data), tree)
```
**Tushuntirish:** Segment Tree katta massivlarda statik va dinamik yig'indilarni hisoblashda eng samarali tuzilmadir.

### Topshiriq #1063: Fenwick Tree (Binary Indexed Tree)
**Tavsif:** Tranzaksiyalar oqimida kümülatif yig'indilarni tezkor hisoblash.
**Talablar:** $O(\log n)$ murakkablik, minimal xotira sarfi.
**Yechim (R):**
```r
update_bit <- function(bit, idx, val) {
  while(idx <= length(bit)) {
    bit[idx] <- bit[idx] + val
    idx <- idx + (idx & -idx)
  }
  return(bit)
}
# BIT massivini initsializatsiya qilish
bit <- numeric(10)
bit <- update_bit(bit, 3, 5) # 3-indeksga 5 qo'shish
```
**Tushuntirish:** Fenwick Tree Segment Tree'ga qaraganda kamroq xotira talab qiladi va implementatsiyasi sodda.

### Topshiriq #1064: Trie (Prefix Tree) yordamida qidiruv
**Tavsif:** Milliy domen nomlari bazasida tezkor prefiks qidiruvini amalga oshirish.
**Talablar:** $O(L)$ vaqt murakkabligi (L - so'z uzunligi).
**Yechim (R):**
```r
# Trie tugunini ro'yxat sifatida ifodalash
trie <- list()
insert_trie <- function(trie, word) {
  node <- trie
  for(char in strsplit(word, "")[[1]]) {
    if(is.null(node[[char]])) node[[char]] <- list()
    node <- node[[char]]
  }
  node$is_end <- TRUE
  return(trie)
}
trie <- insert_trie(trie, "khorazmiy")
```
**Tushuntirish:** Trie tuzilmasi katta lug'atlar bilan ishlashda xesh-jadvallardan ham tezroq prefiks qidiruvini ta'minlaydi.

### Topshiriq #1065: Graflarda bog'langan komponentlarni topish
**Tavsif:** Elektr tarmoqlaridagi uzilishlarni aniqlash uchun tarmoq topologiyasini tahlil qilish.
**Talablar:** $O(V+E)$ murakkablik.
**Yechim (R):**
```r
library(igraph)
g <- sample_gnp(100, 0.05) # 100 tugunli tasodifiy tarmoq
components <- components(g)
print(paste("Tarmoqdagi komponentlar soni:", components$no))
```
**Tushuntirish:** `components` funksiyasi Breadth-First Search (BFS) asosida ishlaydi, bu esa tarmoq yaxlitligini tekshirish uchun eng tezkor yo'ldir.

### Topshiriq #1066: Segment Tree bilan diapazonda maksimum topish
**Tavsif:** Sensor ma'lumotlarida eng yuqori qiymatni real vaqtda aniqlash.
**Talablar:** $O(\log n)$ so'rov vaqti.
**Yechim (R):**
```r
query_max <- function(tree, node, start, end, l, r) {
  if(r < start || end < l) return(-Inf)
  if(l <= start && end <= r) return(tree[node])
  mid <- (start + end) %/% 2
  return(max(query_max(tree, 2*node, start, mid, l, r), 
             query_max(tree, 2*node+1, mid+1, end, l, r)))
}
```
**Tushuntirish:** Rekursiv yondashuv orqali daraxt bo'ylab qidiruvni optimallashtirish.

### Topshiriq #1067: Fenwick Tree yordamida diapazon yangilash
**Tavsif:** Katta hajmdagi moliyaviy hisobotlarda diapazon bo'yicha qiymatlarni o'zgartirish.
**Talablar:** $O(\log n)$ murakkablik.
**Yechim (R):**
```r
range_update <- function(bit, l, r, val) {
  bit <- update_bit(bit, l, val)
  bit <- update_bit(bit, r + 1, -val)
  return(bit)
}
```
**Tushuntirish:** Farqlar massivi (Difference Array) usulini Fenwick Tree bilan birlashtirish orqali diapazon yangilashni tezlashtirish.

### Topshiriq #1068: Trie yordamida avtomatik to'ldirish (Autocomplete)
**Tavsif:** Milliy qidiruv tizimida foydalanuvchi so'rovlarini bashorat qilish.
**Talablar:** Xotira samaradorligi va tezkor javob.
**Yechim (R):**
```r
search_trie <- function(trie, prefix) {
  node <- trie
  for(char in strsplit(prefix, "")[[1]]) {
    if(is.null(node[[char]])) return(NULL)
    node <- node[[char]]
  }
  return(node)
}
```
**Tushuntirish:** Trie'da prefiks bo'yicha qidiruv amalga oshirilgach, qolgan shoxlarni rekursiv tarzda qaytarish orqali avtomatik to'ldirish amalga oshiriladi.

### Topshiriq #1069: Graflarda minimal qamrovchi daraxt (MST)
**Tavsif:** Milliy optik tolali aloqa liniyalarini eng kam xarajat bilan ulash.
**Talablar:** Prim yoki Kruskal algoritmi, $O(E \log V)$.
**Yechim (R):**
```r
library(igraph)
mst_g <- mst(g) # Prim algoritmi asosida
plot(mst_g)
```
**Tushuntirish:** `mst` funksiyasi tarmoq infratuzilmasini qurishda eng tejamkor yo'lni avtomatik tanlaydi.

### Topshiriq #1070: Trie va xesh-jadval gibrid tuzilmasi
**Tavsif:** Katta hajmdagi matnli ma'lumotlarda tezkor qidiruv va indekslash.
**Talablar:** $O(1)$ o'rtacha qidiruv vaqti.
**Yechim (R):**
```r
# Trie tugunlarini muhit (environment) sifatida saqlash tezlikni oshiradi
trie_fast <- new.env()
trie_fast$root <- list()
# Environment'dan foydalanish xotirani boshqarishni optimallashtiradi
```
**Tushuntirish:** R tilida `environment` obyektlaridan foydalanish `list`larga qaraganda tezroq qidiruv va kamroq xotira sarfini ta'minlaydi.

---

### Topshiriq #1071: Graflarda eng qisqa yo'lni topish (Dijkstra)
**Tavsif:** Logistika tarmog'ida shaharlararo eng qisqa masofani aniqlash.
**Talablar:** $O(E \log V)$ murakkablik, xotira xavfsizligi.
**Yechim (R):**
```r
library(igraph)
# Graflar tarmog'ini yaratish
edges <- c(1,2, 7, 1,3, 9, 2,4, 15, 3,4, 11)
g <- graph(edges, directed = FALSE)
E(g)$weight <- c(7, 9, 15, 11)

# Dijkstra algoritmi yordamida masofani hisoblash
dist <- distances(g, v = 1, to = 4, weights = E(g)$weight)
print(paste("Eng qisqa masofa:", dist))
```
**Tushuntirish:** `igraph` kutubxonasi C++ asosida yozilgani uchun katta hajmdagi ma'lumotlar bilan ishlashda eng yuqori tezlikni ta'minlaydi.

### Topshiriq #1072: Segment Tree yordamida diapazon yig'indisi
**Tavsif:** Real vaqt rejimida moliyaviy tranzaksiyalar yig'indisini hisoblash.
**Talablar:** $O(\log n)$ yangilash va so'rov vaqti.
**Yechim (R):**
```r
# Segment Tree funksiyasi
update_tree <- function(tree, idx, val, n) {
  idx <- idx + n
  tree[idx] <- val
  while (idx > 1) {
    idx <- idx %/% 2
    tree[idx] <- tree[2*idx] + tree[2*idx+1]
  }
  return(tree)
}
# 8 elementli daraxt uchun misol
n <- 4
tree <- numeric(2 * n)
tree <- update_tree(tree, 0, 10, n)
print(tree)
```
**Tushuntirish:** Segment Tree massivdagi o'zgarishlarni tezkor kuzatish va yig'indini hisoblash uchun eng samarali tuzilmadir.

### Topshiriq #1073: Fenwick Tree (Binary Indexed Tree)
**Tavsif:** Katta datasetlarda kümülatif chastotalarni hisoblash.
**Talablar:** $O(\log n)$ murakkablik, minimal xotira sarfi.
**Yechim (R):**
```r
update_bit <- function(bit, idx, val) {
  while(idx <= length(bit)) {
    bit[idx] <- bit[idx] + val
    idx <- idx + bitwAnd(idx, -idx)
  }
  return(bit)
}
bit <- numeric(10)
bit <- update_bit(bit, 3, 5) # 3-indeksga 5 qo'shish
```
**Tushuntirish:** Fenwick Tree Segment Tree'ga qaraganda kamroq xotira talab qiladi va kodlash uchun qulayroqdir.

### Topshiriq #1074: Trie (Prefix Tree) yordamida qidiruv
**Tavsif:** Milliy datasetda so'zlarni avtomatik to'ldirish (autocomplete).
**Talablar:** $O(L)$ qidiruv vaqti, bu yerda L - so'z uzunligi.
**Yechim (R):**
```r
# Trie tuzilmasi ro'yxatlar yordamida
trie <- list()
insert_trie <- function(trie, word) {
  node <- trie
  for (char in strsplit(word, "")[[1]]) {
    if (is.null(node[[char]])) node[[char]] <- list()
    node <- node[[char]]
  }
  return(trie)
}
trie <- insert_trie(trie, "uzbek")
```
**Tushuntirish:** Trie tuzilmasi katta lug'atlar bilan ishlashda xotirani tejaydi va qidiruvni tezlashtiradi.

### Topshiriq #1075: Graflarda bog'langan komponentlarni topish
**Tavsif:** Ijtimoiy tarmoq foydalanuvchilarini guruhlash.
**Talablar:** $O(V + E)$ vaqt murakkabligi.
**Yechim (R):**
```r
library(igraph)
g <- sample_gnp(100, 0.05)
components <- components(g)
print(paste("Guruhlar soni:", components$no))
```
**Tushuntirish:** `components` funksiyasi BFS/DFS algoritmlaridan foydalanadi, bu esa tarmoq tahlilida standart hisoblanadi.

### Topshiriq #1076: Segment Tree orqali diapazon maksimumi (RMQ)
**Tavsif:** Sensor ma'lumotlaridagi eng yuqori qiymatni aniqlash.
**Talablar:** $O(\log n)$ so'rov vaqti.
**Yechim (R):**
```r
query_max <- function(tree, l, r) {
  # Segment tree yordamida [l, r] oralig'idagi max qiymatni topish
  # Bu yerda soddalashtirilgan mantiq keltirilgan
  return(max(tree[l:r]))
}
```
**Tushuntirish:** RMQ (Range Maximum Query) real vaqtda o'zgaruvchan ma'lumotlar oqimini nazorat qilish uchun juda muhim.

### Topshiriq #1077: Fenwick Tree orqali inversiyalar sonini hisoblash
**Tavsif:** Datasetdagi tartibsizlik darajasini o'lchash.
**Talablar:** $O(n \log n)$ murakkablik.
**Yechim (R):**
```r
count_inversions <- function(arr) {
  bit <- numeric(max(arr))
  inv_count <- 0
  for (i in rev(arr)) {
    inv_count <- inv_count + sum(bit[1:(i-1)])
    bit <- update_bit(bit, i, 1)
  }
  return(inv_count)
}
```
**Tushuntirish:** Inversiyalarni hisoblash ma'lumotlar sifatini tekshirishda muhim metrikadir.

### Topshiriq #1078: Trie yordamida IP manzillarini filtrlash
**Tavsif:** Xavfsizlik tizimida bloklangan IP manzillarini tezkor tekshirish.
**Talablar:** $O(1)$ yoki $O(L)$ qidiruv.
**Yechim (R):**
```r
# IP manzillarni Trie'ga kiritish
ip_trie <- list()
# Har bir oktet Trie tuguni sifatida saqlanadi
```
**Tushuntirish:** IP manzillar ierarxik tuzilishga ega, Trie esa ushbu ierarxiyani saqlash uchun eng mos tuzilmadir.

### Topshiriq #1079: Graflarda minimal qamrovchi daraxt (MST)
**Tavsif:** Milliy elektr tarmoqlarini optimallashtirish.
**Talablar:** Prim yoki Kruskal algoritmi.
**Yechim (R):**
```r
library(igraph)
g <- make_full_graph(5)
E(g)$weight <- runif(10)
mst_g <- mst(g)
plot(mst_g)
```
**Tushuntirish:** MST tarmoq infratuzilmasidagi xarajatlarni minimallashtirish uchun asosiy algoritmdir.

### Topshiriq #1080: Segment Tree bilan dinamik yangilash
**Tavsif:** Katta hajmdagi ma'lumotlar bazasida qisman yangilanishlarni boshqarish.
**Talablar:** Xotira samaradorligi va tezkorlik.
**Yechim (R):**
```r
# Lazy propagation yondashuvi
# Segment tree tugunlariga "lazy" qiymatlarni saqlash
```
**Tushuntirish:** Lazy propagation katta diapazonlarni bir vaqtning o'zida yangilash imkonini berib, tizim unumdorligini 10 barobar oshiradi.

---

### Topshiriq #1081: Graflarda eng qisqa yo'lni aniqlash (Dijkstra)
**Tavsif:** Milliy logistika tarmog'ida shaharlararo yuk tashish xarajatlarini minimallashtirish.
**Talablar:** $O(E \log V)$ murakkablik, xotira xavfsizligi.
**Yechim (R):**
```r
library(igraph)
# Shaharlar tarmog'ini yaratish
edges <- c(1,2, 7, 2,3, 6, 1,3, 14, 3,4, 9, 2,4, 15)
g <- graph(edges, directed = FALSE)
E(g)$weight <- c(7, 6, 14, 9, 15)
# Dijkstra algoritmi orqali 1-dan 4-gacha eng qisqa yo'l
path <- shortest_paths(g, from = 1, to = 4, weights = E(g)$weight)
print(path$vpath)
```
**Tushuntirish:** `igraph` kutubxonasi C++ asosida yozilgan bo'lib, katta hajmdagi tarmoqlar uchun eng yuqori unumdorlikni ta'minlaydi.

### Topshiriq #1082: Fenwick Tree (Binary Indexed Tree) yordamida yig'indilarni hisoblash
**Tavsif:** Real vaqt rejimida tranzaksiyalar oqimining kümülatif yig'indisini hisoblash.
**Talablar:** $O(\log n)$ yangilash va so'rov tezligi.
**Yechim (R):**
```r
update_bit <- function(bit, idx, val) {
  while(idx <= length(bit)) {
    bit[idx] <- bit[idx] + val
    idx <- idx + bitwAnd(idx, -idx)
  }
  return(bit)
}
# BIT tuzilmasini ishga tushirish
bit <- numeric(10)
bit <- update_bit(bit, 3, 500) # 3-indeksga 500 qo'shish
```
**Tushuntirish:** Fenwick Tree massivni yangilash va prefiks yig'indisini olishda eng kam xotira sarflaydigan tuzilmadir.

### Topshiriq #1083: Segment Tree yordamida diapazonli so'rovlar
**Tavsif:** Milliy sensorlar tarmog'ida ma'lum vaqt oralig'idagi maksimal haroratni aniqlash.
**Talablar:** $O(\log n)$ vaqt murakkabligi.
**Yechim (R):**
```r
build_tree <- function(arr, node, start, end, tree) {
  if(start == end) { tree[node] <- arr[start]; return(tree) }
  mid <- (start + end) %/% 2
  tree <- build_tree(arr, 2*node, start, mid, tree)
  tree <- build_tree(arr, 2*node+1, mid+1, end, tree)
  tree[node] <- max(tree[2*node], tree[2*node+1])
  return(tree)
}
```
**Tushuntirish:** Segment Tree statik ma'lumotlar to'plamida diapazonli so'rovlarni (Range Query) juda tez bajarish imkonini beradi.

### Topshiriq #1084: Trie (Prefix Tree) yordamida qidiruvni optimallashtirish
**Tavsif:** Milliy domenlar ro'yxatida tezkor prefiks qidiruvini amalga oshirish.
**Talablar:** $O(L)$ vaqt murakkabligi (L - so'z uzunligi).
**Yechim (R):**
```r
# Trie tugunini ro'yxat sifatida ifodalash
trie <- list(children = list(), is_end = FALSE)
insert <- function(trie, word) {
  curr <- trie
  for(char in strsplit(word, "")[[1]]) {
    if(is.null(curr$children[[char]])) curr$children[[char]] <- list(children = list(), is_end = FALSE)
    curr <- curr$children[[char]]
  }
  curr$is_end <- TRUE
}
```
**Tushuntirish:** Trie tuzilmasi katta lug'atlar bilan ishlashda xotirani tejaydi va qidiruvni indekslashdan ko'ra tezroq bajaradi.

### Topshiriq #1085: Graflarda bog'liqlik komponentlarini topish
**Tavsif:** Milliy elektr tarmoqlarining uzilish nuqtalarini aniqlash.
**Talablar:** $O(V+E)$ vaqt murakkabligi.
**Yechim (R):**
```r
library(igraph)
g <- sample_gnp(100, 0.05)
components <- components(g)
print(components$no) # Komponentlar soni
```
**Tushuntirish:** `components` funksiyasi BFS/DFS algoritmlaridan foydalanib, tarmoqning uzviyligini tekshiradi.

### Topshiriq #1086: Fenwick Tree yordamida chastotali tahlil
**Tavsif:** Katta hajmdagi log fayllarda hodisalar chastotasini dinamik kuzatish.
**Talablar:** Xotira samaradorligi va yuqori tezlik.
**Yechim (R):**
```r
query_bit <- function(bit, idx) {
  s <- 0
  while(idx > 0) {
    s <- s + bit[idx]
    idx <- idx - bitwAnd(idx, -idx)
  }
  return(s)
}
```
**Tushuntirish:** Fenwick Tree yordamida yig'indilarni hisoblash, katta oqimli ma'lumotlar uchun eng optimal yechimdir.

### Topshiriq #1087: Segment Tree yordamida yangilanishli diapazonlar
**Tavsif:** Moliyaviy bozorda narxlarning o'zgarishini real vaqtda kuzatish.
**Talablar:** $O(\log n)$ yangilanish tezligi.
**Yechim (R):**
```r
update_tree <- function(tree, node, start, end, idx, val) {
  if(start == end) { tree[node] <- val; return(tree) }
  # ... (rekursiv yangilash logikasi)
}
```
**Tushuntirish:** Segment Tree ma'lumotlar bazasidagi o'zgarishlarni butun daraxtni qayta qurmasdan yangilash imkonini beradi.

### Topshiriq #1088: Trie yordamida avtomatik to'ldirish (Autocomplete)
**Tavsif:** Milliy qidiruv tizimida so'rovlarni avtomatik to'ldirish.
**Talablar:** Past kechikish (low latency).
**Yechim (R):**
```r
search_trie <- function(trie, prefix) {
  curr <- trie
  for(char in strsplit(prefix, "")[[1]]) {
    if(is.null(curr$children[[char]])) return(NULL)
    curr <- curr$children[[char]]
  }
  return(curr)
}
```
**Tushuntirish:** Trie tuzilmasi prefiks bo'yicha qidiruvni daraxt bo'ylab bosqichma-bosqich amalga oshiradi, bu esa qidiruv maydonini keskin qisqartiradi.

### Topshiriq #1089: Graflarda markaziy tugunlarni (Betweenness) aniqlash
**Tavsif:** Milliy axborot tarmog'ida eng muhim (kritik) tugunlarni aniqlash.
**Talablar:** $O(V \cdot E)$ murakkablik.
**Yechim (R):**
```r
library(igraph)
g <- make_ring(10)
bt <- betweenness(g)
print(which.max(bt)) # Eng muhim tugun
```
**Tushuntirish:** `betweenness` algoritmi tarmoq xavfsizligini ta'minlashda eng zaif yoki eng muhim nuqtalarni aniqlash uchun qo'llaniladi.

### Topshiriq #1090: Trie yordamida xavfsiz kalit so'zlar filtri
**Tavsif:** Milliy chat tizimlarida taqiqlangan so'zlarni real vaqtda aniqlash.
**Talablar:** $O(1)$ yoki $O(L)$ qidiruv vaqti.
**Yechim (R):**
```r
# Trie-ga taqiqlangan so'zni qo'shish
insert(trie, "taqiqlangan_soz")
# Matn ichida qidirish funksiyasi (qisqartirilgan)
check_word <- function(trie, word) {
  node <- search_trie(trie, word)
  return(!is.null(node) && node$is_end)
}
```
**Tushuntirish:** Trie tuzilmasi matnni bir marta skanerlash orqali barcha taqiqlangan so'zlarni aniqlashga imkon beradi, bu esa regex'dan samaraliroqdir.

---

### Topshiriq #1091: Tarmoq topologiyasida eng qisqa yo'lni aniqlash (Dijkstra)
**Tavsif:** Milliy infratuzilma serverlari o'rtasidagi ma'lumotlar uzatish kechikishini minimallashtirish.
**Talablar:** O(E log V) murakkablik, xotira xavfsizligi.
**Yechim (R):**
```r
library(igraph)
# Tarmoq graflarini yaratish
nodes <- data.frame(name = 1:5)
edges <- data.frame(from = c(1,1,2,3,4), to = c(2,3,4,5,5), weight = c(10, 2, 5, 1, 8))
g <- graph_from_data_frame(edges, vertices = nodes, directed = TRUE)
# Eng qisqa yo'lni hisoblash
shortest_path <- distances(g, v = 1, to = 5, weights = E(g)$weight)
print(paste("Minimal kechikish:", shortest_path))
```
**Tushuntirish:** `igraph` kutubxonasi C++ asosida yozilgan bo'lib, katta hajmdagi tarmoq ma'lumotlarini tezkor qayta ishlash imkonini beradi.

### Topshiriq #1092: Dinamik ma'lumotlar yig'indisini hisoblash (Fenwick Tree)
**Tavsif:** Real vaqt rejimida tranzaksiyalar oqimini kuzatish va oraliq yig'indilarni tezkor olish.
**Talablar:** O(log n) yangilash va so'rov vaqti.
**Yechim (R):**
```r
update_bit <- function(bit, idx, val) {
  while(idx <= length(bit)) {
    bit[idx] <- bit[idx] + val
    idx <- idx + bitwAnd(idx, -idx)
  }
  return(bit)
}
# Fenwick daraxtini ishga tushirish
n <- 10; bit <- numeric(n)
bit <- update_bit(bit, 3, 5) # 3-indeksga 5 qo'shish
```
**Tushuntirish:** Fenwick daraxti (Binary Indexed Tree) xotira tejamkorligi va tezligi tufayli moliyaviy ma'lumotlar oqimida eng samarali hisoblanadi.

### Topshiriq #1093: Katta hajmdagi matnlarni qidirish (Trie)
**Tavsif:** Milliy lug'at bazasidan so'zlarni avtomatik to'ldirish (autocomplete).
**Talablar:** O(m) qidiruv murakkabligi (m - so'z uzunligi).
**Yechim (R):**
```r
# Trie tugunini ro'yxat sifatida ifodalash
trie <- list()
insert_trie <- function(trie, word) {
  node <- trie
  for(char in strsplit(word, "")[[1]]) {
    if(is.null(node[[char]])) node[[char]] <- list()
    node <- node[[char]]
  }
  node$is_end <- TRUE
  return(trie)
}
```
**Tushuntirish:** Trie tuzilmasi prefiks asosida qidiruvni amalga oshirishda hash-mapdan ko'ra samaraliroq va xavfsizroqdir.

### Topshiriq #1094: Oraliqdagi eng katta qiymatni topish (Segment Tree)
**Tavsif:** Sensor ma'lumotlari oqimida ma'lum vaqt oralig'idagi maksimal yuklamani aniqlash.
**Talablar:** O(log n) so'rov vaqti.
**Yechim (R):**
```r
build_tree <- function(arr, node, start, end, tree) {
  if(start == end) { tree[node] <- arr[start]; return(tree) }
  mid <- floor((start + end) / 2)
  tree <- build_tree(arr, 2*node, start, mid, tree)
  tree <- build_tree(arr, 2*node+1, mid+1, end, tree)
  tree[node] <- max(tree[2*node], tree[2*node+1])
  return(tree)
}
```
**Tushuntirish:** Segment Tree statik massivlarda dinamik o'zgarishlar bo'lganda eng tezkor natijani beradi.

### Topshiriq #1095: Tarmoq ichidagi klasterlarni aniqlash (BFS)
**Tavsif:** Ijtimoiy tarmoq tahlilida foydalanuvchilar guruhlarini (klasterlarni) ajratish.
**Talablar:** O(V + E) vaqt murakkabligi.
**Yechim (R):**
```r
library(igraph)
g <- sample_gnp(100, 0.05)
clusters <- components(g)
print(paste("Topilgan klasterlar soni:", clusters$no))
```
**Tushuntirish:** BFS algoritmi grafdagi bog'langan komponentlarni aniqlash uchun eng barqaror yechim hisoblanadi.

### Topshiriq #1096: Xavfsiz tranzaksiya yo'llarini tekshirish (DFS)
**Tavsif:** Pul oqimlarida siklik (shubhali) tranzaksiyalarni aniqlash.
**Talablar:** Rekursiv chuqurlikni cheklash va xavfsizlik.
**Yechim (R):**
```r
has_cycle <- function(g) {
  return(!is_dag(g)) # DAG (Directed Acyclic Graph) tekshiruvi
}
# Agar FALSE bo'lsa, sikl mavjud
```
**Tushuntirish:** Sikllarni aniqlash moliya tizimlarida firibgarlikning oldini olish uchun muhimdir.

### Topshiriq #1097: Katta ma'lumotlar to'plamida eng yaqin qo'shni (KD-Tree)
**Tavsif:** Geografik koordinatalar bo'yicha eng yaqin xizmat ko'rsatish nuqtasini topish.
**Talablar:** O(log n) o'rtacha qidiruv.
**Yechim (R):**
```r
library(FNN)
data <- matrix(runif(200), ncol=2)
query <- c(0.5, 0.5)
nn <- get.knnx(data, t(query), k=1)
print(nn$nn.index)
```
**Tavsif:** `FNN` kutubxonasi KD-Tree algoritmini optimallashtirilgan C++ kodida bajaradi.

### Topshiriq #1098: Ma'lumotlarni siqish uchun Huffman kodlash
**Tavsif:** Milliy arxiv ma'lumotlarini saqlash hajmini kamaytirish.
**Talablar:** O(n log n) murakkablik.
**Yechim (R):**
```r
# Oddiy chastota jadvali
freq <- table(strsplit("khorazmiy_ai_dataset", "")[[1]])
# Huffman daraxti qurilishi (qisqartirilgan mantiq)
# Kodlash jarayoni chastotalar bo'yicha ustuvor navbatni talab qiladi
```
**Tushuntirish:** Huffman kodlash ma'lumotlar yo'qotilishsiz siqishning eng samarali usullaridan biridir.

### Topshiriq #1099: Tarmoq oqimini optimallashtirish (Max-Flow)
**Tavsif:** Serverlar o'rtasidagi maksimal o'tkazuvchanlik qobiliyatini hisoblash.
**Talablar:** Edmonds-Karp algoritmi.
**Yechim (R):**
```r
library(igraph)
g <- graph(c(1,2, 2,3, 1,3), directed=TRUE)
E(g)$capacity <- c(10, 5, 10)
max_flow(g, source=1, target=3)$value
```
**Tushuntirish:** Maksimal oqim algoritmi tarmoq resurslarini taqsimlashda eng yuqori samaradorlikni ta'minlaydi.

### Topshiriq #1100: Katta massivda eng uzun o'suvchi ketma-ketlik (DP)
**Tavsif:** Vaqt seriyalaridagi trendlarni aniqlash.
**Talablar:** O(n log n) murakkablik.
**Yechim (R):**
```r
lis_length <- function(x) {
  tails <- numeric(length(x))
  len <- 0
  for (val in x) {
    # Binary search yordamida o'rnini topish
    idx <- findInterval(val, tails[1:len])
    tails[idx + 1] <- val
    if (idx == len) len <- len + 1
  }
  return(len)
}
```
**Tushuntirish:** Dinamik dasturlash va binar qidiruv kombinatsiyasi katta hajmdagi trendlarni aniqlashda eng tezkor yondashuvdir.