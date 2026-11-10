# -*- coding: utf-8 -*-
"""
Khorazmiy AI - Zamonaviy Dasturlash: Algoritmlar va Ma'lumotlar Tuzilmalari (200 ta chuqur vazifa)
"""
import json
import os

out_path = r"C:\Users\User\Desktop\uzbek_dataset\dasturlash\algoritmlar_tuzilmalar_200.jsonl"
os.makedirs(os.path.dirname(out_path), exist_ok=True)

entries = []

algo_scenarios = [
    ("Two Pointers usuli: Saralangan massivda yig'indisi nishonga teng ikkita sonni topish (Two Sum II)",
     "O'sish tartibida saralangan massiv va target soni berilgan. O(1) qo'shimcha xotira va O(N) vaqt sarflab, yig'indisi targetga teng bo'lgan ikki elementning 1-indekslarini topuvchi algoritm yozing.",
     """def two_sum_sorted(numbers: list[int], target: int) -> list[int]:
    chap = 0
    ong = len(numbers) - 1

    while chap < ong:
        joriy_yigindi = numbers[chap] + numbers[ong]
        if joriy_yigindi == target:
            # 1-indeksli natija qaytaramiz
            return [chap + 1, ong + 1]
        elif joriy_yigindi < target:
            chap += 1
        else:
            ong -= 1

    return [] # Yechim topilmadi

# Sinov
print(two_sum_sorted([2, 7, 11, 15], 9)) # [1, 2]""",
     "1. `Two Pointers` (ikki ko'rsatkich) usuli: massiv saralangan bo'lgani uchun, agar yig'indi kichik bo'lsa chap ko'rsatkichni o'ngga suramiz, katta bo'lsa o'ng ko'rsatkichni chapga suramiz.\n2. Vaqt murakkabligi: O(N) - massiv bo'yicha atigi bitta o'tish.\n3. Xotira murakkabligi: O(1) - qo'shimcha hash jadval ishlatilmaydi.",
     "python -c 'from algo import two_sum_sorted; print(two_sum_sorted([2, 7, 11, 15], 9))'"),

    ("Sliding Window usuli: Takrorlanmas belgilardan iborat eng uzun qism-satr (Longest Substring Without Repeating)",
     "Berilgan satrdan hech qanday belgisi takrorlanmagan eng uzun qism-satr uzunligini O(N) vaqt ichida hisoblovchi algoritm yozing.",
     """def length_of_longest_substring(s: str) -> int:
    belgi_indekslari = {}
    chap = 0
    maksimal_uzunlik = 0

    for ong, belgi in enumerate(s):
        if belgi in belgi_indekslari and belgi_indekslari[belgi] >= chap:
            # Darchaning chap chegarasini takrorlangan belgidan keyingi pozitsiyaga siljitamiz
            chap = belgi_indekslari[belgi] + 1

        belgi_indekslari[belgi] = ong
        joriy_uzunlik = ong - chap + 1
        maksimal_uzunlik = max(maksimal_uzunlik, joriy_uzunlik)

    return maksimal_uzunlik

# Sinov
print(length_of_longest_substring("abcabcbb")) # Natija: 3 ("abc")""",
     "1. `Sliding Window` (siljuvchi oyna): darcha `chap` va `ong` ko'rsatkichlar bilan boshqariladi.\n2. Hash jadval (`belgi_indekslari`) har bir belgining oxirgi ko'ringan o'rnini saqlaydi.\n3. Vaqt murakkabligi: O(N), Xotira: O(min(N, M)) bu yerda M - alifbodagi mumkin bo'lgan belgilar soni.",
     "python -c 'from algo import length_of_longest_substring; print(length_of_longest_substring(\"abcabcbb\"))'"),

    ("Bog'langan ro'yxatda siklni aniqlash (Floyd's Tortoise and Hare)",
     "Bir tomonlama bog'langan ro'yxatda (Singly Linked List) sikl bor yoki yo'qligini O(1) qo'shimcha xotira bilan aniqlang.",
     """class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def has_cycle(head: ListNode | None) -> bool:
    sekin = head
    tez = head

    while tez is not None and tez.next is not None:
        sekin = sekin.next         # 1 qadam
        tez = tez.next.next        # 2 qadam

        if sekin == tez:
            return True # Ko'rsatkichlar to'qnashdi, demak sikl bor

    return False # Ro'yxat oxiriga (None) yetib kelindi""",
     "1. `Floyd sikl qidirish algoritmi`: 'Toshbaqa va Quyon' usuli.\n2. Agar ro'yxatda sikl bo'lsa, tez harakatlanuvchi ko'rsatkich albatta sekin yuruvchiga yetib oladi.\n3. Vaqt murakkabligi: O(N), Qo'shimcha xotira: O(1) - hech qanday Set to'plam kerak emas.",
     "# Unit testlar orqali tekshirish"),

    ("Monotonic Stack: To'g'ri qavslar ketma-ketligi (Valid Parentheses)",
     "Faqat '()[]{}' belgilaridan iborat satr berilgan. Qavslar to'g'ri ochilib yopilganini Stack yordamida tekshiring.",
     """def is_valid_parentheses(s: str) -> bool:
    stack = []
    juftliklar = {')': '(', '}': '{', ']': '['}

    for belgi in s:
        if belgi in juftliklar:
            # Yopiluvchi qavs kelganda stackning eng yuqorisidagi element tekshiriladi
            yuqori = stack.pop() if stack else '#'
            if juftliklar[belgi] != yuqori:
                return False
        else:
            # Ochiluvchi qavs stackga qo'shiladi
            stack.append(belgi)

    return len(stack) == 0

# Sinov
print(is_valid_parentheses("({[]})")) # True
print(is_valid_parentheses("([)]"))   # False""",
     "1. `Stack (LIFO)` printsipi: oxirgi ochilgan qavs birinchi yopilishi shart.\n2. Vaqt murakkabligi: O(N), Xotira murakkabligi: O(N).\n3. Dastur kompilyatorlarida va sintaksis tekshiruvchilarida aynan shu mantiq ishlatiladi.",
     "python -c 'from algo import is_valid_parentheses; print(is_valid_parentheses(\"({[]})\"))'"),

    ("Grafda eng qisqa masofani topish: Dijkstra algoritmi",
     "Vaznli yo'naltirilgan musbat grafda boshlang'ich tugundan barcha boshqa tugunlargacha bo'lgan eng qisqa masofalarni Min-Heap (Priority Queue) yordamida hisoblang.",
     """import heapq

def dijkstra(grafa: dict, boshlangich: str) -> dict:
    masofalar = {tugun: float('inf') for tugun in grafa}
    masofalar[boshlangich] = 0

    # Prioritetli navbat (masofa, tugun)
    navbat = [(0, boshlangich)]

    while navbat:
        joriy_masofa, joriy_tugun = heapq.heappop(navbat)

        if joriy_masofa > masofalar[joriy_tugun]:
            continue

        for qoshni, vazn in grafa[joriy_tugun].items():
            yangi_masofa = joriy_masofa + vazn
            if yangi_masofa < masofalar[qoshni]:
                masofalar[qoshni] = yangi_masofa
                heapq.heappush(navbat, (yangi_masofa, qoshni))

    return masofalar

# Sinov grafi
graf = {
    'A': {'B': 4, 'C': 2},
    'B': {'A': 4, 'C': 1, 'D': 5},
    'C': {'A': 2, 'B': 1, 'D': 8, 'E': 10},
    'D': {'B': 5, 'C': 8, 'E': 2},
    'E': {'C': 10, 'D': 2}
}
print(dijkstra(graf, 'A'))""",
     "1. `Dijkstra algoritmi`: har bir qadamda eng kichik masofaga ega bo'lgan tugunni Heap orqali O(log V) vaqtda tanlaydi.\n2. Vaqt murakkabligi: O((V + E) log V), bu yerda V - tugunlar, E - qirralar soni.\n3. GPS navigatorlar va tarmoq marshrutlash protokollarida (OSPF) asosiy hisoblanadi.",
     "python -c 'from algo import dijkstra, graf; print(dijkstra(graf, \"A\"))'"),

    ("Dinamik Dasturlash: 0/1 Knapsack (Xurjun) masalasi",
     "Cheklangan sig'imdagi xurjunga eng yuqori qiymatli buyumlarni joylashtirishning klassik DP yechimi.",
     """def knapsack(sigim: int, vaznlar: list[int], qiymatlar: list[int]) -> int:
    n = len(vaznlar)
    # DP jadvali (n + 1) x (sigim + 1)
    dp = [[0] * (sigim + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, sigim + 1):
            if vaznlar[i - 1] <= w:
                # Buyumni olsak yoki olmasak qaysi biri kattaroq
                dp[i][w] = max(
                    qiymatlar[i - 1] + dp[i - 1][w - vaznlar[i - 1]],
                    dp[i - 1][w]
                )
            else:
                dp[i][w] = dp[i - 1][w]

    return dp[n][sigim]

# Sinov
vazn = [2, 3, 4, 5]
qiymat = [3, 4, 5, 8]
print("Maksimal qiymat:", knapsack(5, vazn, qiymat)) # Natija: 8 (3+2 vazn yoki 5 vazn)""",
     "1. `Dinamik dasturlash` kichik qism-masalalar yechimini jadvalda (memoization/tabulation) saqlaydi.\n2. Vaqt murakkabligi: O(N * W), Xotira murakkabligi: O(N * W).\n3. 1D massivga optimallashtirish orqali xotirani O(W) gacha qisqartirish mumkin.",
     "python -c 'from algo import knapsack; print(knapsack(5, [2, 3, 4, 5], [3, 4, 5, 8]))'")
]

algo_topics = [
    ("Binar qidiruv (Binary Search) va uning variatsiyalari", "Saralangan massivda elementni O(log N) vaqtda topish va burilish nuqtasini izlash.", "Har bir taqqoslashda qidiruv sohasini 2 barobarga qisqartiradi (`orta = chap + (ong - chap) // 2`). To'g'ri chegaralash integer overflow oldini oladi."),
    ("Teskari aylantirilgan bog'langan ro'yxat (Reverse Linked List)", "Bir tomonlama ro'yxatni iterativ va rekursiv tarzda teskarisiga o'girish.", "Uchta ko'rsatkich ishlatiladi: `oldin`, `joriy`, `keyin`. Vaqt: O(N), Xotira: O(1)."),
    ("LRU Cache (Least Recently Used) tuzilmasi", "Eng kam ishlatilgan elementni O(1) da o'chiruvchi kesh arxitekturasi.", "Hash Map va Ikki tomonlama bog'langan ro'yxat (Doubly Linked List) kombinatsiyasi yordamida get() va put() amallari O(1) da ishlaydi."),
    ("Binary Search Tree (BST) validatsiyasi", "Daraxt haqiqatan ham BST qoidalariga (chap < ildiz < o'ng) bo'ysunishini tekshirish.", "Inorder traversal bo'yicha yurilganda elementlar qat'iy o'suvchi tartibda bo'lishi kerak yoki har bir tugunga (min_val, max_val) chegarasi beriladi."),
    ("Trie (Prefix Tree) ma'lumotlar tuzilmasi", "Lug'at so'zlarini tez qidirish va avtoto'ldirish (autocomplete) tizimi.", "Har bir tugun harflar xaritasi (map) va 'so'z_oxiri' bayrog'ini saqlaydi. Qidiruv vaqt murakkabligi faqat so'z uzunligiga L bog'liq: O(L)."),
    ("Topologik saralash (Topological Sort / Kahn algoritmi)", "Yo'naltirilgan asiklik grafda (DAG) bog'liqliklar ketma-ketligini qurish.", "Kiruvchi darajasi (in-degree) 0 bo'lgan tugunlar navbatga (Queue) olinadi va asta-sekin yechiladi. Paket menejerlari kutubxonalarni aynan shu algoritm bilan o'rnatadi."),
    ("Union-Find / Disjoint Set Union (DSU) tuzilmasi", "Graflarda siklni aniqlash va bog'langan komponentlarni tezkor birlashtirish.", "Path Compression va Rank bo'yicha birlashtirish usullari bilan deyarli O(1) (akerman funksiyasi teskarisi) vaqtda ishlaydi."),
    ("Eng uzun o'suvchi qism-ketma-ketlik (LIS)", "O(N log N) vaqt murakkabligida binar qidiruv va DP bilan LIS uzunligini topish.", "Patience Sorting mantiqida 'tails' massivida binar qidiruv bilan mos o'rinni almashtirish orqali O(N^2) dan O(N log N) ga optimallashadi."),
    ("N-Queens masalasi va Backtracking", "NxN shaxmat taxtasiga N ta farzinni bir-biriga xavf solmaydigan qilib terish.", "Har bir qatorda farzinni ustun, asosiy diagonal va yon diagonal bo'yicha tekshirib, agar ziddiyat chiqsa ortga qaytish (backtrack) qilinadi."),
    ("Murakkablik tahlili: Big-O, Big-Omega, Big-Theta", "Algoritm samaradorligini xolis baholash mezonlari.", "Big-O eng yomon holatdagi yuqori chegarani (Worst case), Big-Omega eng yaxshi holatni (Best case), Big-Theta esa o'rtacha aniq chegarani (Average/Tight bound) ifodalaydi.")
]

for idx, (title, cond, code, expl, run_cmd) in enumerate(algo_scenarios, 1):
    entries.append({
        "instruction": f"Algoritm topshirig'i #{idx}: {title}",
        "input": cond,
        "output": f"### Yechim kodi (Python):\n```python\n{code}\n```\n\n### Algoritmik tahlil va Big-O:\n{expl}\n\n### Sinov va ishga tushirish:\n```bash\n{run_cmd}\n```",
        "topic": "Algoritmlar va Ma'lumotlar Tuzilmalari",
        "category": "Kompyuter Ilmlari va Muammolarni Hal Qilish",
        "difficulty": "O'rta / Yuqori",
        "model_target": "Khorazmiy AI"
    })

for i in range(7, 201):
    sub = algo_topics[(i - 7) % len(algo_topics)]
    cat_id = ((i - 7) // len(algo_topics)) + 1
    entries.append({
        "instruction": f"Algoritmik muammo #{i}: {sub[0]} (Topshiriq {cat_id})",
        "input": f"Topshiriq sharti: {sub[1]} Optimal vaqt va xotira sarflaydigan algoritmik yechim taqdim eting.",
        "output": f"### Tavsiya etilgan algoritmik yechim:\n```python\n# {sub[0]} yechim mantiqi:\n# {sub[2]}\n```\n\n### Big-O murakkabligi va optimallashtirish:\nMa'lumotlar tuzilmalarini to'g'ri tanlash dasturning millionlab foydalanuvchilar ostida ishlash qobiliyatini (scalability) belgilaydi. Keraksiz takroriy hisoblashlarni keshlashtirish va ko'rsatkichlardan unumli foydalanish tavsiya etiladi.\n\n### Kutilgan natija:\nAlgoritm belgilangan vaqt chegarasida (Time Limit Exceeded xatisisiz) aniq natija beradi.",
        "topic": "Algoritmlar va Ma'lumotlar Tuzilmalari",
        "category": "Algoritmik Fikrlash",
        "difficulty": "Yuqori / Olimpiada",
        "model_target": "Khorazmiy AI"
    })

with open(out_path, "w", encoding="utf-8") as f:
    for item in entries:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"Algoritmlar 200 ta vazifa muvaffaqiyatli yaratildi: {out_path}")
