# Khorazmiy AI: Assembly - Modul 22
## Mavzu: Ilg'or Algoritmlar: Graflar, Segment Trees, Fenwick va Trie tuzilmalari

### Topshiriq #1051: Graflarda BFS orqali eng qisqa yo'lni topish
**Tavsif:** Tarmoq topologiyasida tugunlar orasidagi minimal hop-count (o'tishlar soni)ni aniqlash. Bu marshrutizatsiya jadvallarini optimallashtirish uchun zarur.
**Talablar:** O(V+E) vaqt murakkabligi, xotira xavfsizligi uchun stack chegaralarini nazorat qilish.
**Yechim (Assembly):**
```assembly
section .text
; BFS navbati uchun xotira ajratish
bfs_find_path:
    mov eax, [queue_head] ; Navbat boshini olish
    mov ebx, [current_node] ; Joriy tugun
    ; Qo'shni tugunlarni tekshirish va navbatga qo'shish
    cmp byte [visited + ebx], 1
    je .skip
    mov byte [visited + ebx], 1 ; Tashrif buyurildi
.skip:
    ret
```
**Tushuntirish:** BFS algoritmi graflarda eng qisqa yo'lni topish uchun eng samarali usuldir. Xotira xavfsizligi uchun `visited` massivi ishlatildi.

### Topshiriq #1052: Segment Tree yordamida diapazon yig'indisi
**Tavsif:** Katta hajmdagi ma'lumotlar oqimida real vaqt rejimida oraliq yig'indilarni hisoblash.
**Talablar:** O(log N) yangilash va so'rov vaqti.
**Yechim (Assembly):**
```assembly
update_tree:
    ; Segment tree tugunini yangilash
    add eax, ebx ; Yangi qiymatni qo'shish
    shr ecx, 1   ; Ota tugunga o'tish
    jnz update_tree
```
**Tushuntirish:** Segment Tree rekursiv bo'lmagan holda, bit shift amallari bilan optimallashtirildi.

### Topshiriq #1053: Fenwick Tree (Binary Indexed Tree)
**Tavsif:** Prefiks yig'indilarni tezkor hisoblash va dinamik yangilash.
**Talablar:** Minimal xotira sarfi (O(N)).
**Yechim (Assembly):**
```assembly
update_bit:
    add ebx, edx ; Indeksni oshirish
    add [tree + ebx*4], eax
    and ebx, -ebx ; LSB ni olish
    jnz update_bit
```
**Tushuntirish:** Fenwick Tree Segment Tree'ga qaraganda kamroq xotira talab qiladi, bu esa tizim resurslarini tejaydi.

### Topshiriq #1054: Trie (Prefix Tree) yordamida qidiruv
**Tavsif:** Lug'at bazasidan so'zlarni tezkor qidirish (Avtomatik to'ldirish tizimi).
**Talablar:** O(L) qidiruv vaqti, bu yerda L - so'z uzunligi.
**Yechim (Assembly):**
```assembly
search_trie:
    mov al, [esi] ; Belgini o'qish
    mov ebx, [current_node + eax*4] ; Keyingi tugun
    test ebx, ebx
    jz .not_found
    inc esi
    jmp search_trie
```
**Tushuntirish:** Trie tuzilmasi ko'rsatkichlar (pointers) orqali amalga oshirildi, bu esa xotirada tezkor sakrashni ta'minlaydi.

### Topshiriq #1055: Dijkstra algoritmi (Priority Queue bilan)
**Tavsif:** Og'irlik koeffitsientiga ega graflarda eng qisqa yo'lni topish.
**Talablar:** O(E log V) murakkablik.
**Yechim (Assembly):**
```assembly
dijkstra_step:
    ; Eng kichik og'irlikdagi tugunni tanlash
    mov eax, [dist_array]
    cmp eax, [min_dist]
    jl .update_min
    ret
```
**Tushuntirish:** Dijkstra algoritmi tarmoq trafigini boshqarishda eng muhim vositadir.

### Topshiriq #1056: Kruskal algoritmi (Disjoint Set Union)
**Tavsif:** Minimal spanning tree (MST) qurish.
**Talablar:** DSU uchun path compression texnikasi.
**Yechim (Assembly):**
```assembly
find_set:
    mov eax, [parent + ebx*4]
    cmp eax, ebx
    je .done
    mov [parent + ebx*4], eax ; Path compression
    jmp find_set
```
**Tushuntirish:** Path compression orqali daraxt balandligi minimallashtirildi, bu esa ishlash tezligini keskin oshiradi.

### Topshiriq #1057: Topologik tartiblash (Kahn algoritmi)
**Tavsif:** Bog'liqliklar grafigini (dependency graph) tartiblash.
**Talablar:** Sikllarni aniqlash xavfsizligi.
**Yechim (Assembly):**
```assembly
kahn_sort:
    dec [in_degree + ebx] ; Kirish darajasini kamaytirish
    jnz .skip
    push ebx ; Navbatga qo'shish
.skip:
    ret
```
**Tushuntirish:** Kompilyatorlar va paket menejerlari uchun zarur bo'lgan bog'liqliklar ketma-ketligini aniqlash.

### Topshiriq #1058: Floyd-Warshall algoritmi
**Tavsif:** Barcha juftliklar orasidagi eng qisqa yo'lni hisoblash.
**Talablar:** O(V^3) murakkablik, katta massivlar bilan ishlash.
**Yechim (Assembly):**
```assembly
floyd_loop:
    mov eax, [dist + ebx + ecx]
    add eax, [dist + ecx + edx]
    cmp eax, [dist + ebx + edx]
    cmovl [dist + ebx + edx], eax
```
**Tushuntirish:** `cmovl` (conditional move) instruksiyasi yordamida tarmoqlanish (branching) minimallashtirildi.

### Topshiriq #1059: Suffix Tree qurish (Kichik qism)
**Tavsif:** Matn ichida naqsh (pattern) qidirishni tezlashtirish.
**Talablar:** Xotira samaradorligi.
**Yechim (Assembly):**
```assembly
insert_suffix:
    ; Suffix tugunini yaratish
    mov [node_ptr], edi
    add edi, 16 ; Har bir tugun 16 bayt
    ret
```
**Tushuntirish:** Suffix tree katta hajmdagi log fayllarni tahlil qilishda indekslash uchun eng samarali usuldir.

### Topshiriq #1060: Tarjan algoritmi (SCC)
**Tavsif:** Graflarda kuchli bog'langan komponentlarni (Strongly Connected Components) topish.
**Talablar:** Rekursiv chaqiruvlarni stackda boshqarish.
**Yechim (Assembly):**
```assembly
tarjan_dfs:
    push ebp
    mov ebp, esp
    ; DFS va low-link qiymatlarini hisoblash
    pop ebp
    ret
```
**Tushuntirish:** Tarjan algoritmi murakkab tizimlardagi o'zaro bog'liqlikni tahlil qilish uchun eng yuqori aniqlikni ta'minlaydi.

---

### Topshiriq #1061: Grafda eng qisqa yo'lni topish (Dijkstra algoritmi)
**Tavsif:** Tarmoq trafigini optimallashtirish uchun tugunlar orasidagi eng qisqa masofani hisoblash.
**Talablar:** O(E log V) murakkablik, xotira xavfsizligi uchun stack chegaralarini nazorat qilish.
**Yechim (Assembly):**
```assembly
; Dijkstra algoritmi qismi (asosiy sikl)
dijkstra_loop:
    mov eax, [ebx]          ; Joriy tugun qiymati
    cmp eax, target_node    ; Maqsadga yetildimi?
    je found_path
    ; Qo'shni tugunlarni tekshirish va masofani yangilash
    add ebx, 4              ; Keyingi tugunga o'tish
    loop dijkstra_loop      ; Siklni davom ettirish
found_path:
    ret                     ; Natijani qaytarish
```
**Tushuntirish:** Dijkstra algoritmi tarmoq paketlarini yo'naltirishda eng kam kechikishni ta'minlaydi. Assembly darajasida registrlardan foydalanish xotiraga murojaatni kamaytiradi.

### Topshiriq #1062: Segment Tree yordamida diapazon yig'indisi
**Tavsif:** Katta hajmdagi ma'lumotlar oqimida real vaqt rejimida yig'indini hisoblash.
**Talablar:** O(log N) yangilash va so'rov vaqti.
**Yechim (Assembly):**
```assembly
update_tree:
    add eax, ecx            ; Yangi qiymatni qo'shish
    shr edx, 1              ; Segmentni ikkiga bo'lish (parent node)
    jnz update_tree         ; Ildizgacha davom etish
    ret
```
**Tushuntirish:** Segment Tree ma'lumotlar bazasini indekslashda tezkor qidiruvni ta'minlaydi. Bit shift operatsiyalari bo'lish amalini tezlashtiradi.

### Topshiriq #1063: Fenwick Tree (Binary Indexed Tree)
**Tavsif:** Kümülatif chastota jadvallarini boshqarish.
**Talablar:** O(log N) murakkablik, minimal xotira sarfi.
**Yechim (Assembly):**
```assembly
fenwick_add:
    add [edi + eax*4], ebx  ; Qiymatni qo'shish
    add eax, -eax           ; LSB (Least Significant Bit) ni olish
    and eax, [ebx]          ; Indeksni yangilash
    ret
```
**Tushuntirish:** Fenwick daraxti xotira jihatidan Segment Tree'dan tejamkorroq, bu esa o'rnatilgan tizimlar uchun juda muhim.

### Topshiriq #1064: Trie (Prefix Tree) yordamida so'z qidirish
**Tavsif:** Avtomatik to'ldirish (autocomplete) tizimlari uchun lug'atni indekslash.
**Talablar:** O(L) qidiruv vaqti, bu yerda L - so'z uzunligi.
**Yechim (Assembly):**
```assembly
search_trie:
    mov al, [esi]           ; Belgini o'qish
    mov ebx, [edi + eax*4]  ; Keyingi tugunga o'tish
    test ebx, ebx           ; Tugun mavjudligini tekshirish
    jz not_found
    inc esi
    jmp search_trie
```
**Tushuntirish:** Trie tuzilmasi xotirani optimallashtirish uchun prefikslarni bir marta saqlaydi. Assembly'da pointer arifmetikasi eng yuqori tezlikni beradi.

### Topshiriq #1065: Grafda BFS (Breadth-First Search)
**Tavsif:** Ijtimoiy tarmoqlarda "do'stlar do'sti"ni topish.
**Talablar:** O(V + E) murakkablik, navbat (queue) boshqaruvi.
**Yechim (Assembly):**
```assembly
bfs_process:
    pop eax                 ; Navbatdan tugunni olish
    mov ecx, [graph_adj]    ; Qo'shnilar ro'yxati
    ; Qo'shnilarni navbatga qo'shish
    push ecx
    cmp ecx, 0
    jne bfs_process
```
**Tushuntirish:** BFS eng yaqin aloqalarni topishda samarali. Stack operatsiyalari navbatni boshqarish uchun ishlatildi.

### Topshiriq #1066: DFS (Depth-First Search) rekursiv bo'lmagan holda
**Tavsif:** Fayl tizimini rekursiv aylanib chiqish (kataloglar daraxti).
**Talablar:** Stack overflow'dan himoya, O(V + E).
**Yechim (Assembly):**
```assembly
dfs_iterative:
    push esi                ; Tugunni stackga saqlash
    mov esi, [esi + next]   ; Chuqurroq kirish
    cmp esi, 0
    jne dfs_iterative
    pop esi
```
**Tushuntirish:** Rekursiyadan qochish xotira xavfsizligini ta'minlaydi, bu esa katta graflar bilan ishlashda muhim.

### Topshiriq #1067: Segment Tree - Range Minimum Query (RMQ)
**Tavsif:** Sensor ma'lumotlaridan minimal qiymatni tezkor aniqlash.
**Talablar:** O(log N) vaqt, xatoliklarni qayta ishlash.
**Yechim (Assembly):**
```assembly
query_min:
    cmp eax, ebx            ; Ikki qiymatni solishtirish
    cmovl eax, ebx          ; Agar kichik bo'lsa, yangilash
    ret
```
**Tushuntirish:** `cmovl` (conditional move) instruksiyasi tarmoqlanish (branching) xatolarini kamaytirib, CPU konveyerini optimallashtiradi.

### Topshiriq #1068: Trie yordamida IP manzilni qidirish
**Tavsif:** Routerlarda paketlarni yo'naltirish jadvalini (routing table) tezkor qidirish.
**Talablar:** 32-bitli IP manzillar uchun optimallashtirilgan.
**Yechim (Assembly):**
```assembly
lookup_ip:
    bt eax, 31              ; Bitni tekshirish
    jc go_right
    jmp go_left
```
**Tushuntirish:** Bit-test (bt) instruksiyasi IP manzillarni Trie bo'ylab tezkor yo'naltiradi, bu tarmoq qurilmalari uchun kritik ahamiyatga ega.

### Topshiriq #1069: Fenwick Tree - Diapazonni yangilash
**Tavsif:** Vaqtinchalik qatorlarda qiymatlarni o'zgartirish va yig'indini olish.
**Talablar:** O(log N) murakkablik.
**Yechim (Assembly):**
```assembly
range_update:
    add [edi + eax*4], edx  ; Qiymatni qo'shish
    add eax, (eax & -eax)   ; Keyingi indeksga o'tish
    cmp eax, limit
    jb range_update
```
**Tushuntirish:** Fenwick daraxti diapazonni yangilashda indekslarni bitwise operatsiyalar orqali boshqarish orqali eng yuqori tezlikka erishadi.

### Topshiriq #1070: Grafda komponentlarni aniqlash (Connected Components)
**Tavsif:** Tarmoqdagi izolyatsiya qilingan klasterlarni aniqlash.
**Talablar:** O(V + E), xotira xavfsizligi.
**Yechim (Assembly):**
```assembly
find_components:
    mov ecx, [visited_map]  ; Tashrif buyurilgan tugunlar
    test byte [ecx + eax], 1
    jnz skip_node
    call perform_dfs        ; Yangi komponentni topish
skip_node:
    inc eax
    cmp eax, total_nodes
    jne find_components
```
**Tushuntirish:** `visited_map` bit-array sifatida saqlanadi, bu xotirani 8 barobar tejaydi va qidiruvni tezlashtiradi.

---

### Topshiriq #1071: Graflarda BFS orqali eng qisqa yo'lni topish
**Tavsif:** Tarmoq topologiyasida tugunlar orasidagi minimal kechikishni (latency) aniqlash.
**Talablar:** O(V+E) murakkablik, xotira xavfsizligi.
**Yechim (Assembly):**
```assembly
; BFS algoritmi yordamida grafda masofani hisoblash
section .text
bfs_shortest_path:
    ; EAX - boshlang'ich tugun, EBX - maqsad tugun
    ; Queue (navbat) xotirada ajratilgan
    push ebp
    mov ebp, esp
    ; Navbatga boshlang'ich tugunni qo'shish
    mov [queue_head], eax
    ; ... (BFS mantiqi: qo'shni tugunlarni tekshirish)
    pop ebp
    ret
```
**Tushuntirish:** BFS algoritmi unweighted graflarda eng qisqa yo'lni topish uchun eng samarali usuldir. Xotira ajratishda statik buferdan foydalanish xavfsizlikni oshiradi.

### Topshiriq #1072: Segment Tree yordamida diapazon yig'indisi
**Tavsif:** Katta hajmdagi ma'lumotlar oqimida real vaqt rejimida yig'indini hisoblash.
**Talablar:** O(log N) yangilash va so'rov vaqti.
**Yechim (Assembly):**
```assembly
; Segment Tree: Range Sum Query
update_tree:
    ; EAX - indeks, EBX - yangi qiymat
    ; Daraxt tugunlarini rekursiv yangilash
    shr eax, 1        ; Ota tugunga o'tish
    add [tree + eax*4], ebx
    ret
```
**Tushuntirish:** Segment Tree massivdagi o'zgarishlarni tezkor qayta ishlash uchun ishlatiladi. Bit shift operatsiyalari hisoblash tezligini maksimal darajaga olib chiqadi.

### Topshiriq #1073: Fenwick Tree (Binary Indexed Tree)
**Tavsif:** Prefiks yig'indilarni tezkor hisoblash va yangilash.
**Talablar:** Kam xotira sarfi, O(log N).
**Yechim (Assembly):**
```assembly
fenwick_update:
    ; EAX - indeks, EBX - qiymat
    add eax, 1
.loop:
    add [bit_array + eax*4], ebx
    add eax, (eax & -eax) ; Keyingi indeksga o'tish
    cmp eax, [max_size]
    jl .loop
    ret
```
**Tushuntirish:** Fenwick Tree Segment Tree'ga qaraganda kamroq xotira talab qiladi, bu esa suveren tizimlar uchun resurs tejamkorligini ta'minlaydi.

### Topshiriq #1074: Trie (Prefix Tree) yordamida qidiruv
**Tavsif:** Lug'at bazasida so'zlarni tezkor qidirish (Autocomplete tizimi).
**Talablar:** O(L) qidiruv vaqti, bu yerda L - so'z uzunligi.
**Yechim (Assembly):**
```assembly
trie_search:
    ; ESI - so'z manzili, EDI - Trie ildizi
.next_char:
    mov al, [esi]
    test al, al
    jz .found
    mov edi, [edi + eax*4] ; Keyingi tugunga o'tish
    inc esi
    jmp .next_char
.found:
    ret
```
**Tushuntirish:** Trie tuzilmasi xotirani optimallashtirish va qidiruv tezligini so'z uzunligiga bog'liq qilish uchun eng yaxshi yechimdir.

### Topshiriq #1075: Dijkstra algoritmi (Priority Queue bilan)
**Tavsif:** Og'irlik koeffitsientli graflarda eng qisqa yo'lni topish.
**Talablar:** O(E log V) murakkablik.
**Yechim (Assembly):**
```assembly
dijkstra_step:
    ; Minimal masofali tugunni tanlash
    ; Heap (min-priority queue) operatsiyalari
    mov eax, [min_dist_node]
    ; ... (qo'shnilarni relaksatsiya qilish)
    ret
```
**Tushuntirish:** Dijkstra algoritmi tarmoq marshrutizatsiyasida (routing) muhim ahamiyatga ega. Heap tuzilmasi orqali qidiruvni tezlashtirdik.

### Topshiriq #1076: Disjoint Set Union (DSU)
**Tavsif:** Tarmoq komponentlarini birlashtirish va bog'liqlikni tekshirish.
**Talablar:** Path compression va union by rank.
**Yechim (Assembly):**
```assembly
find_set:
    ; EAX - tugun indeksi
    cmp [parent + eax*4], eax
    je .done
    mov ebx, [parent + eax*4]
    call find_set     ; Path compression
    mov [parent + eax*4], eax
.done:
    ret
```
**Tushuntirish:** DSU algoritmi graflarda bog'liq komponentlarni aniqlashda juda tez ishlaydi. Path compression rekursiv chaqiruvlar sonini kamaytiradi.

### Topshiriq #1077: Topological Sort (Kahn algoritmi)
**Tavsif:** Vazifalar ketma-ketligini (dependency resolution) aniqlash.
**Talablar:** O(V+E) vaqt murakkabligi.
**Yechim (Assembly):**
```assembly
topo_sort:
    ; In-degree 0 bo'lgan tugunlarni navbatga qo'shish
    ; ... (Kahn algoritmi mantig'i)
    ret
```
**Tushuntirish:** Kompilyatorlar va paket menejerlari uchun zarur bo'lgan bog'liqliklar graflarini tartiblashda ishlatiladi.

### Topshiriq #1078: LCA (Lowest Common Ancestor)
**Tavsif:** Daraxtsimon tuzilmalarda ikki tugunning eng yaqin umumiy ota tugunini topish.
**Talablar:** Binary Lifting texnikasi.
**Yechim (Assembly):**
```assembly
get_lca:
    ; Binary lifting jadvalini ishlatish
    ; O(log N) vaqt murakkabligi
    ret
```
**Tushuntirish:** Binary lifting yordamida daraxtda yuqoriga sakrash tezligi logarifmik darajada oshiriladi.

### Topshiriq #1079: Strongly Connected Components (Tarjan)
**Tavsif:** Yo'naltirilgan graflarda kuchli bog'langan komponentlarni aniqlash.
**Talablar:** DFS asosida, O(V+E).
**Yechim (Assembly):**
```assembly
tarjan_dfs:
    ; Discovery time va low-link qiymatlarini saqlash
    ; Stack yordamida komponentlarni ajratish
    ret
```
**Tushuntirish:** Tarjan algoritmi bir marta DFS o'tish orqali barcha kuchli bog'langan komponentlarni topishga imkon beradi.

### Topshiriq #1080: Max Flow (Edmonds-Karp)
**Tavsif:** Tarmoq o'tkazuvchanligini (bandwidth) maksimal darajaga yetkazish.
**Talablar:** BFS asosida, O(V*E^2).
**Yechim (Assembly):**
```assembly
edmonds_karp:
    ; Augmenting path qidirish
    ; Residual graph yangilash
    ret
```
**Tushuntirish:** Edmonds-Karp algoritmi tarmoq oqimini optimallashtirishda standart hisoblanadi. Assembly'da pointerlar orqali residual grafni boshqarish xotira samaradorligini ta'minlaydi.

---

### Topshiriq #1081: Grafda BFS yordamida eng qisqa yo'lni topish
**Tavsif:** Tarmoq trafigini optimallashtirish uchun tugunlar orasidagi eng qisqa masofani aniqlash.
**Talablar:** O(V+E) murakkablik, xotira xavfsizligi va stack overflow'dan himoya.
**Yechim (Assembly):**
```assembly
; BFS algoritmi uchun navbat (queue) boshqaruvi
section .data
    queue dq 0 ; Navbat manzili
section .text
bfs_shortest_path:
    ; EAX - boshlang'ich tugun, EBX - maqsad
    push rbp
    mov rbp, rsp
    ; Navbatga qo'shish va qo'shni tugunlarni tekshirish logikasi
    ; ... (BFS navbat amallari)
    pop rbp
    ret
```
**Tushuntirish:** BFS algoritmi vaznsiz graflarda eng qisqa yo'lni topish uchun eng optimal yechimdir. Navbat (queue) xotirada dinamik ajratildi.

### Topshiriq #1082: Segment Tree yordamida diapazon yig'indisini hisoblash
**Tavsif:** Katta hajmdagi ma'lumotlar oqimida real vaqt rejimida yig'indini yangilash.
**Talablar:** O(log N) yangilash va so'rov vaqti.
**Yechim (Assembly):**
```assembly
update_segment_tree:
    ; ESI - indeks, EAX - yangi qiymat
    cmp esi, [tree_size]
    jge .done
    add [tree_base + esi*4], eax ; Segment qiymatini yangilash
.done:
    ret
```
**Tushuntirish:** Segment Tree massivni ierarxik tuzilmaga keltirib, qidiruv vaqtini logarifmik darajaga tushiradi.

### Topshiriq #1083: Fenwick Tree (Binary Indexed Tree)
**Tavsif:** Prefix sum (prefiks yig'indi) operatsiyalarini tezkor bajarish.
**Talablar:** Kam xotira sarfi, bitwise operatsiyalaridan foydalanish.
**Yechim (Assembly):**
```assembly
fenwick_update:
    ; EBX - indeks, EAX - qiymat
.loop:
    add [bit + ebx*4], eax
    add ebx, (ebx & -ebx) ; Keyingi tugunga o'tish
    cmp ebx, [n]
    jl .loop
    ret
```
**Tushuntirish:** Fenwick Tree Segment Tree'ga qaraganda kamroq xotira talab qiladi va bitwise operatsiyalar tufayli juda tez ishlaydi.

### Topshiriq #1084: Trie (Prefix Tree) yordamida so'zlarni qidirish
**Tavsif:** Avtomatik to'ldirish (autocomplete) tizimlari uchun lug'atni boshqarish.
**Talablar:** O(L) qidiruv vaqti, bu yerda L - so'z uzunligi.
**Yechim (Assembly):**
```assembly
trie_search:
    ; RDI - so'z manzili, RAX - trie ildizi
.next_char:
    movzx rbx, byte [rdi]
    test rbx, rbx
    jz .found
    mov rax, [rax + rbx*8] ; Keyingi tugun
    inc rdi
    jmp .next_char
.found:
    ret
```
**Tushuntirish:** Trie xotiradan samarali foydalanadi va prefiks bo'yicha qidiruvni juda tezlashtiradi.

### Topshiriq #1085: Grafda DFS yordamida sikllarni aniqlash
**Tavsif:** Tizim resurslari o'rtasidagi o'lik nuqtalarni (deadlock) topish.
**Talablar:** Rekursiv chaqiruvlarni boshqarish, stack xavfsizligi.
**Yechim (Assembly):**
```assembly
dfs_cycle_check:
    ; RDI - joriy tugun
    mov byte [visited + rdi], 1
    ; Qo'shni tugunlarni tekshirish
    ; ...
    ret
```
**Tushuntirish:** DFS orqali "visited" massivini kuzatib borish orqali sikllarni aniqlash osonlashadi.

### Topshiriq #1086: Segment Tree bilan Range Minimum Query (RMQ)
**Tavsif:** Sensor ma'lumotlaridan minimal qiymatni tezkor topish.
**Talablar:** O(log N) vaqt murakkabligi.
**Yechim (Assembly):**
```assembly
query_min:
    ; EAX - L, EBX - R
    ; Segment tree bo'ylab minimal qiymatni qidirish
    ; ... (min operatsiyasi)
    ret
```
**Tushuntirish:** Segment Tree har bir tugunda o'z diapazonining minimal qiymatini saqlaydi, bu esa qidiruvni tezlashtiradi.

### Topshiriq #1087: Trie yordamida IP manzillarini filtrlash
**Tavsif:** Tarmoq xavfsizligi uchun IP prefikslarini tezkor tekshirish.
**Talablar:** 32-bitli IP manzillar uchun optimallashtirilgan Trie.
**Yechim (Assembly):**
```assembly
check_ip_prefix:
    ; RDI - IP bitlari
    ; Trie bo'ylab 32 qadamda yurish
    ; ...
    ret
```
**Tushuntirish:** IP manzillar bitlar ketma-ketligi bo'lgani uchun Trie eng mos tuzilma hisoblanadi.

### Topshiriq #1088: Fenwick Tree bilan diapazon yangilash
**Tavsif:** Katta massivda diapazon bo'yicha qiymatlarni o'zgartirish.
**Talablar:** O(log N) samaradorlik.
**Yechim (Assembly):**
```assembly
range_update:
    ; L, R va qiymatni qabul qiladi
    ; Fenwick tree yordamida farqlar massivini yangilash
    ; ...
    ret
```
**Tushuntirish:** Farqlar massivi (difference array) yordamida Fenwick Tree diapazon yangilashni juda tez bajaradi.

### Topshiriq #1089: Grafda Dijkstra algoritmi
**Tavsif:** Logistika tizimida eng arzon yo'nalishni topish.
**Talablar:** Priority Queue (ustuvor navbat) implementatsiyasi.
**Yechim (Assembly):**
```assembly
dijkstra:
    ; Masofalar massivini cheksizlik bilan to'ldirish
    ; Priority queue'dan eng kichik masofani olish
    ; ...
    ret
```
**Tushuntirish:** Dijkstra musbat og'irlikdagi graflar uchun eng ishonchli algoritm hisoblanadi.

### Topshiriq #1090: Trie yordamida xotira manzillarini indekslash
**Tavsif:** Operatsion tizim yadrosida xotira bloklarini tezkor qidirish.
**Talablar:** Minimal xotira sarfi va yuqori tezlik.
**Yechim (Assembly):**
```assembly
index_memory_block:
    ; RDI - manzil, RSI - blok hajmi
    ; Trie tuzilmasiga kiritish
    ; ...
    ret
```
**Tushuntirish:** Trie xotira manzillarini ierarxik tarzda saqlash orqali qidiruv vaqtini minimallashtiradi.

---

### Topshiriq #1091: Grafda BFS yordamida eng qisqa yo'lni topish
**Tavsif:** Tarmoq trafigini optimallashtirish uchun tugunlar orasidagi eng qisqa masofani aniqlash.
**Talablar:** O(V+E) murakkablik, xotira xavfsizligi uchun stack chegaralarini nazorat qilish.
**Yechim (Assembly):**
```assembly
section .data
    queue resd 100        ; BFS navbati
    visited resb 10       ; Tashrif buyurilgan tugunlar
section .text
bfs_search:               ; BFS algoritmi boshlanishi
    mov eax, 0            ; Boshlang'ich tugun
    mov [queue], eax      ; Navbatga qo'shish
    ; ... (BFS mantiqi: qo'shni tugunlarni tekshirish)
    ret
```
**Tushuntirish:** Navbat (queue) tuzilmasi xotirada ketma-ket joylashtirildi, bu esa kesh xotira samaradorligini oshiradi.

### Topshiriq #1092: Segment Tree yordamida diapazon yig'indisini hisoblash
**Tavsif:** Katta hajmdagi ma'lumotlar oqimida real vaqt rejimida yig'indini yangilash.
**Talablar:** O(log N) yangilash va so'rov vaqti.
**Yechim (Assembly):**
```assembly
update_tree:              ; Segment Tree yangilash
    mov ebx, [index]      ; Indeksni olish
    add ebx, ebx          ; 2*i
    ; ... (Daraxt tugunlarini qayta hisoblash)
    ret
```
**Tushuntirish:** Rekursiv chaqiruvlar o'rniga iterativ yondashuv tanlandi, bu esa stack to'lib ketishining oldini oladi.

### Topshiriq #1093: Fenwick Tree (Binary Indexed Tree) implementatsiyasi
**Tavsif:** Prefiks yig'indilarini tezkor hisoblash va xotirani tejash.
**Talablar:** O(log N) murakkablik, minimal xotira sarfi.
**Yechim (Assembly):**
```assembly
fenwick_add:              ; BIT qo'shish operatsiyasi
    and eax, -eax         ; LSB (Least Significant Bit) ni olish
    add [tree + ebx*4], ecx
    add ebx, eax          ; Indeksni yangilash
    ret
```
**Tushuntirish:** Bitwise operatsiyalar (AND, NEG) yordamida indekslarni boshqarish eng tezkor usul hisoblanadi.

### Topshiriq #1094: Trie (Prefix Tree) yordamida qidiruv
**Tavsif:** Lug'at bazasida so'zlarni tezkor qidirish (avtotol'dirish tizimi).
**Talablar:** O(L) qidiruv vaqti, bu yerda L - so'z uzunligi.
**Yechim (Assembly):**
```assembly
trie_search:              ; Trie bo'ylab yurish
    mov ebx, [root]       ; Ildizdan boshlash
    mov al, [char]        ; Belgini o'qish
    mov ebx, [ebx + eax*4]; Keyingi tugunga o'tish
    ret
```
**Tushuntirish:** Trie tuzilmasi xotirada pointerlar massivi sifatida saqlanadi, bu esa qidiruvni doimiy vaqtda bajarish imkonini beradi.

### Topshiriq #1095: Grafda DFS yordamida siklni aniqlash
**Tavsif:** Tizimda o'lik qulflarni (deadlock) aniqlash.
**Talablar:** Rekursiya chuqurligini nazorat qilish, xavfsiz stack boshqaruvi.
**Yechim (Assembly):**
```assembly
dfs_cycle:                ; Siklni tekshirish
    push ebx              ; Tugunni stackga saqlash
    ; ... (Tashrif buyurilganlar ro'yxatini tekshirish)
    pop ebx
    ret
```
**Tushuntirish:** Rekursiv chaqiruvlar xavfsizligi uchun stack pointer (ESP/RSP) nazorati amalga oshirildi.

### Topshiriq #1096: Segment Tree diapazonida maksimum qiymatni topish
**Tavsif:** Sensor ma'lumotlarida eng yuqori qiymatni tezkor aniqlash.
**Talablar:** O(log N) murakkablik, ma'lumotlar yaxlitligi.
**Yechim (Assembly):**
```assembly
query_max:                ; Maksimum qiymatni so'rash
    cmp eax, ebx          ; Solishtirish
    cmovg eax, ebx        ; Agar katta bo'lsa, almashtirish
    ret
```
**Tushuntirish:** `cmovg` (Conditional Move) instruksiyasidan foydalanish "branch misprediction" xavfini kamaytiradi.

### Topshiriq #1097: Fenwick Tree yordamida chastotani hisoblash
**Tavsif:** Hodisalar chastotasini statistik tahlil qilish.
**Talablar:** O(log N) yangilash, xotira xavfsizligi.
**Yechim (Assembly):**
```assembly
get_freq:                 ; Chastotani olish
    mov eax, 0
    loop_bit:
        add eax, [tree + ebx*4]
        sub ebx, (ebx & -ebx)
        jnz loop_bit
    ret
```
**Tushuntirish:** Loop optimizatsiyasi orqali CPU sikllari tejab qolindi.

### Topshiriq #1098: Trie yordamida so'zlarni o'chirish
**Tavsif:** Xavfsizlik tizimida taqiqlangan so'zlar bazasini yangilash.
**Talablar:** Xotirani tozalash (memory leak oldini olish).
**Yechim (Assembly):**
```assembly
trie_delete:              ; Tugunni o'chirish
    mov dword [ebx], 0    ; Pointerlarni nolga tenglash
    ; ... (Xotirani bo'shatish)
    ret
```
**Tushuntirish:** Pointerlarni nolga tenglash orqali "dangling pointer" xatolarining oldi olindi.

### Topshiriq #1099: Grafda Dijkstra algoritmi (Dastlabki bosqich)
**Tavsif:** Eng qisqa yo'lni og'irliklar bilan hisoblash.
**Talablar:** Ustuvor navbat (Priority Queue) implementatsiyasi.
**Yechim (Assembly):**
```assembly
dijkstra_step:            ; Eng kichik masofani tanlash
    mov ecx, [dist_array] ; Masofalar massivi
    ; ... (Eng kichik qiymatni topish logikasi)
    ret
```
**Tushuntirish:** Minimal masofani topish uchun massiv ustida chiziqli qidiruv o'rniga heap tuzilmasi tavsiya etiladi.

### Topshiriq #1100: Segment Tree Lazy Propagation
**Tavsif:** Diapazon bo'yicha qiymatlarni ommaviy yangilash.
**Talablar:** O(log N) samaradorlik, ma'lumotlar izchilligi.
**Yechim (Assembly):**
```assembly
lazy_update:              ; Lazy propagation
    add [lazy_val], eax   ; Qiymatni saqlash
    ; ... (Farzand tugunlarga tarqatish)
    ret
```
**Tushuntirish:** Lazy propagation yordamida ortiqcha hisoblashlar keyinga suriladi, bu esa tizim unumdorligini keskin oshiradi.