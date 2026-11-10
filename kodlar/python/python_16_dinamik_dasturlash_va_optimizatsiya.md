# Python Dasturlash Tili — 16-Qism: Dinamik Dasturlash (DP), Backtracking va Optimizatsiya
## (751-800 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam algoritmik dasturlashning eng yuqori cho'qqisi bo'lgan Dinamik Dasturlash, Backtracking va Ochko'z algoritmlarni qamrab oladi:
* 1D va 2D Dinamik Dasturlash asoslari: Zinalar, Uy o'g'risi, Tangalar, Noyob yo'llar;
* Ryukzak masalalari: 0/1 Knapsack, Cheksiz ryukzak, Qism-to'plam yig'indisi, Yo'lni tiklash;
* Satrlar va ketma-ketliklar: LCS, LIS (O(n log n)), Levenshteyn masofasi, Palindromlar;
* Backtracking ustaligi: N-Malika, Sudoku, Subsets, Permutatsiyalar, So'z qidiruvi;
* Ochko'z (Greedy) strategiyalar: Faoliyat tanlash, Sakrash o'yini, Gaz stansiyalari, Xaffman;
* Bitmask DP va sayohatchi savdogar (TSP);

---

# 751-Topshiriq: DP Asoslari: Zinalar bo'ylab ko'tarilish (Climbing Stairs)

## Topshiriq sharti:
N ta zinadan iborat zinapoyaga 1 yoki 2 qadam tashlab chiqishning barcha usullari sonini toping.

## Yechim (Python kodi):
```python
def climb_stairs(n):
    if n <= 2: return n
    oldingi2, oldingi1 = 1, 2
    for _ in range(3, n + 1):
        oldingi2, oldingi1 = oldingi1, oldingi2 + oldingi1
    return oldingi1

print("3 ta zina:", climb_stairs(3))
print("5 ta zina:", climb_stairs(5))
```

## Tushuntirish va Mantiq:
1. Har bir zinaga kelish usuli `f(n) = f(n-1) + f(n-2)` Fibonachchi qoidasiga to'g'ri keladi. Xotira: O(1).

## Ishlash natijasi:
```text
Chiqish: 3 ta zina: 3, 5 ta zina: 8
```

---

# 752-Topshiriq: Minimal narxli zinalar (Min Cost Climbing Stairs)

## Topshiriq sharti:
Har bir zinaga qadam qo'yish narxi berilgan. Zinalarning eng yuqorisiga chiqish uchun minimal xarajatni toping.

## Yechim (Python kodi):
```python
def min_cost_climbing_stairs(cost):
    n = len(cost)
    birinchi, ikkinchi = cost[0], cost[1]
    for i in range(2, n):
        joriy = cost[i] + min(birinchi, ikkinchi)
        birinchi, ikkinchi = ikkinchi, joriy
    return min(birinchi, ikkinchi)

print("Minimal xarajat:", min_cost_climbing_stairs([10, 15, 20]))
print("Minimal xarajat 2:", min_cost_climbing_stairs([1, 100, 1, 1, 1, 100, 1, 1, 100, 1]))
```

## Tushuntirish va Mantiq:
1. Har bir pog'ona narxi oldingi ikki variantning eng kichigiga o'z narxini qo'shish bilan hisoblanadi.

## Ishlash natijasi:
```text
Chiqish: Minimal xarajat: 15, Minimal xarajat 2: 6
```

---

# 753-Topshiriq: Uy o'g'risi (House Robber I — Bir chiziqdagi uylar)

## Topshiriq sharti:
Qo'shni uylarni bir vaqtda o'g'irlamasdan, maksimal qancha boylik to'plash mumkinligini toping.

## Yechim (Python kodi):
```python
def rob(nums):
    oldingi_max = joriy_max = 0
    for pul in nums:
        oldingi_max, joriy_max = joriy_max, max(joriy_max, oldingi_max + pul)
    return joriy_max

print("Maksimal boylik:", rob([1, 2, 3, 1]))
print("Maksimal boylik 2:", rob([2, 7, 9, 3, 1]))
```

## Tushuntirish va Mantiq:
1. Har bir uyda ikki tanlov bor: uyni o'marish (oldingi_max + pul) yoki o'tkazib yuborish (joriy_max).

## Ishlash natijasi:
```text
Chiqish: Maksimal boylik: 4, Maksimal boylik 2: 12
```

---

# 754-Topshiriq: Uy o'g'risi II (House Robber II — Aylanma uylar)

## Topshiriq sharti:
Uylar doira shaklida joylashgan bo'lib, birinchi va oxirgi uy qo'shni hisoblanadi. Maksimal boylikni toping.

## Yechim (Python kodi):
```python
def rob_circular(nums):
    if len(nums) == 1: return nums[0]
    def oddiy_rob(uylar):
        old = joriy = 0
        for x in uylar:
            old, joriy = joriy, max(joriy, old + x)
        return joriy
    # 1-uy olinsa oxirgisi olinmaydi, yoki 1-uy olinmay oxirgisi olinadi
    return max(oddiy_rob(nums[:-1]), oddiy_rob(nums[1:]))

print("Doiraviy o'g'rilik:", rob_circular([2, 3, 2]))
print("Doiraviy o'g'rilik 2:", rob_circular([1, 2, 3, 1]))
```

## Tushuntirish va Mantiq:
1. Doiraviy zanjirni ikkita alohida chiziqli holatga bo'lib hisoblaymiz.

## Ishlash natijasi:
```text
Chiqish: Doiraviy o'g'rilik: 3, Doiraviy o'g'rilik 2: 4
```

---

# 755-Topshiriq: Tangalarni almashtirish (Coin Change I — Minimal tangalar)

## Topshiriq sharti:
Berilgan summani hosil qilish uchun kerak bo'ladigan tangalarning eng kam sonini toping.

## Yechim (Python kodi):
```python
def coin_change(tangalar, summa):
    dp = [float('inf')] * (summa + 1)
    dp[0] = 0
    for t in tangalar:
        for i in range(t, summa + 1):
            dp[i] = min(dp[i], dp[i - t] + 1)
    return dp[summa] if dp[summa] != float('inf') else -1

print("11 so'm uchun:", coin_change([1, 2, 5], 11))
print("3 so'm uchun [2]:", coin_change([2], 3))
```

## Tushuntirish va Mantiq:
1. `dp[i]` qiymati `i` summani hosil qilish uchun kerak bo'lgan minimal tangalar sonidir.

## Ishlash natijasi:
```text
Chiqish: 11 so'm uchun: 3, 3 so'm uchun [2]: -1
```

---

# 756-Topshiriq: Tangalarni almashtirish II (Coin Change II — Usullar soni)

## Topshiriq sharti:
Berilgan summani tangalar yordamida hosil qilishning barcha turli kombinatsiyalari sonini hisoblang.

## Yechim (Python kodi):
```python
def change_ways(tangalar, summa):
    dp = [0] * (summa + 1)
    dp[0] = 1
    for t in tangalar:
        for i in range(t, summa + 1):
            dp[i] += dp[i - t]
    return dp[summa]

print("5 so'mni hosil qilish usullari [1, 2, 5]:", change_ways([1, 2, 5], 5))
```

## Tushuntirish va Mantiq:
1. Tashqi sikl tangalar bo'yicha yurgizilganda dublikat kombinatsiyalar (masalan, 1+2 va 2+1) inobatga olinmaydi.

## Ishlash natijasi:
```text
Chiqish: 5 so'mni hosil qilish usullari [1, 2, 5]: 4
```

---

# 757-Topshiriq: 0/1 Ryukzak masalasi (0/1 Knapsack Problem)

## Topshiriq sharti:
Sig'imi W bo'lgan ryukzakka berilgan og'irlik va narxdagi buyumlardan maksimal qimmatini joylashtiring.

## Yechim (Python kodi):
```python
def knapsack_01(W, ogirliklar, narxlar):
    n = len(narxlar)
    dp = [0] * (W + 1)
    for i in range(n):
        w = ogirliklar[i]
        val = narxlar[i]
        # Orqadan oldinga yuramiz (bitta elementni qayta ishlatmaslik uchun)
        for j in range(W, w - 1, -1):
            dp[j] = max(dp[j], dp[j - w] + val)
    return dp[W]

print("Maksimal qiymat:", knapsack_01(50, [10, 20, 30], [60, 100, 120]))
```

## Tushuntirish va Mantiq:
1. Orqadan oldinga tabulyatsiya 2D jadval o'rniga 1D xotira (O(W)) bilan ishlash imkonini beradi.

## Ishlash natijasi:
```text
Chiqish: Maksimal qiymat: 220
```

---

# 758-Topshiriq: Cheksiz ryukzak (Unbounded Knapsack)

## Topshiriq sharti:
Har bir buyumdan istalgancha miqdorda olish mumkin bo'lsa, ryukzakning maksimal narxini toping.

## Yechim (Python kodi):
```python
def unbounded_knapsack(W, ogirliklar, narxlar):
    dp = [0] * (W + 1)
    for i in range(len(narxlar)):
        w = ogirliklar[i]
        val = narxlar[i]
        # Oldindan orqaga yuramiz (takroriy olishga ruxsat)
        for j in range(w, W + 1):
            dp[j] = max(dp[j], dp[j - w] + val)
    return dp[W]

print("Cheksiz ryukzak qiymati:", unbounded_knapsack(8, [1, 3, 4, 5], [10, 40, 50, 70]))
```

## Tushuntirish va Mantiq:
1. Oldinga qarab sikl bitta elementni bir necha marta tanlashga imkon beradi.

## Ishlash natijasi:
```text
Chiqish: Cheksiz ryukzak qiymati: 110
```

---

# 759-Topshiriq: Teng qismlarga bo'lish (Partition Equal Subset Sum)

## Topshiriq sharti:
Massivni yig'indilari o'zaro teng bo'lgan ikkita qism-to'plamga ajratish mumkinligini tekshiring.

## Yechim (Python kodi):
```python
def can_partition(nums):
    jami = sum(nums)
    if jami % 2 != 0: return False
    target = jami // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for num in nums:
        for j in range(target, num - 1, -1):
            dp[j] = dp[j] or dp[j - num]
    return dp[target]

print("[1, 5, 11, 5] teng bo'linadimi:", can_partition([1, 5, 11, 5]))
print("[1, 2, 3, 5] teng bo'linadimi:", can_partition([1, 2, 3, 5]))
```

## Tushuntirish va Mantiq:
1. Masala nishon qiymati `sum / 2` bo'lgan 0/1 qism-to'plam yig'indisi (Subset Sum) masalasiga aylanadi.

## Ishlash natijasi:
```text
Chiqish: [1, 5, 11, 5] teng bo'linadimi: True, [1, 2, 3, 5] teng bo'linadimi: False
```

---

# 760-Topshiriq: Eng uzun o'suvchi ketma-ketlik (LIS — O(n log n) Patience Sorting)

## Topshiriq sharti:
Massivdagi eng uzun qat'iy o'suvchi ketma-ketlik uzunligini ikkilik qidiruv bilan toping.

## Yechim (Python kodi):
```python
import bisect

def length_of_lis(nums):
    quyruqlar = []
    for x in nums:
        idx = bisect.bisect_left(quyruqlar, x)
        if idx == len(quyruqlar):
            quyruqlar.append(x)
        else:
            quyruqlar[idx] = x
    return len(quyruqlar)

print("LIS uzunligi:", length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]))
```

## Tushuntirish va Mantiq:
1. Patience sorting usuli LIS masalasini O(n^2) dan O(n log n) ga tushiradi.

## Ishlash natijasi:
```text
Chiqish: LIS uzunligi: 4
```

---

# 761-Topshiriq: Eng uzun umumiy qism-ketma-ketlik (Longest Common Subsequence — LCS)

## Topshiriq sharti:
Ikki satrning eng uzun umumiy ketma-ketligi uzunligini 2D DP bilan toping.

## Yechim (Python kodi):
```python
def lcs(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]

print("LCS ('abcde', 'ace'):", lcs("abcde", "ace"))
```

## Tushuntirish va Mantiq:
1. Git diff va bioinformatikada gen ketma-ketliklarini taqqoslash LCS asosiga qurilgan.

## Ishlash natijasi:
```text
Chiqish: LCS ('abcde', 'ace'): 3
```

---

# 762-Topshiriq: Tahrirlash masofasi (Edit Distance / Levenshtein DP)

## Topshiriq sharti:
Bir so'zni ikkinchisiga aylantirish uchun minimal amallar (qo'shish, o'chirish, almashtirish) soni.

## Yechim (Python kodi):
```python
def min_distance(word1, word2):
    m, n = len(word1), len(word2)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        yangi_dp = [i] + [0] * n
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                yangi_dp[j] = dp[j - 1]
            else:
                yangi_dp[j] = 1 + min(dp[j], yangi_dp[j - 1], dp[j - 1])
        dp = yangi_dp
    return dp[n]

print("horse -> ros:", min_distance("horse", "ros"))
print("intention -> execution:", min_distance("intention", "execution"))
```

## Tushuntirish va Mantiq:
1. O(n) xotirali Levenshteyn DP matnlarni avtomatik tuzatishning yadrosi hisoblanadi.

## Ishlash natijasi:
```text
Chiqish: horse -> ros: 3, intention -> execution: 5
```

---

# 763-Topshiriq: Eng uzun palindromik qism-ketma-ketlik (Longest Palindromic Subsequence)

## Topshiriq sharti:
Satr ichidagi eng uzun palindrom hosil qiluvchi ketma-ketlik uzunligini toping.

## Yechim (Python kodi):
```python
def longest_palindrome_subseq(s):
    # s va s[::-1] ning LCS qiymati
    rev = s[::-1]
    n = len(s)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        yangi = [0] * (n + 1)
        for j in range(1, n + 1):
            if s[i - 1] == rev[j - 1]:
                yangi[j] = 1 + dp[j - 1]
            else:
                yangi[j] = max(dp[j], yangi[j - 1])
        dp = yangi
    return dp[n]

print("bbbab LPS:", longest_palindrome_subseq("bbbab"))
```

## Tushuntirish va Mantiq:
1. Satrni o'zining teskarisi bilan LCS qilish palindrom qism-ketma-ketlikni beradi.

## Ishlash natijasi:
```text
Chiqish: bbbab LPS: 4
```

---

# 764-Topshiriq: Noyob yo'llar (Unique Paths — MxN Matritsa)

## Topshiriq sharti:
Robot faqat o'ngga va pastga harakatlanib chap-yuqori burchakdan o'ng-pastki burchakka yetib borish usullari soni.

## Yechim (Python kodi):
```python
def unique_paths(m, n):
    qator = [1] * n
    for _ in range(m - 1):
        for j in range(1, n):
            qator[j] += qator[j - 1]
    return qator[-1]

print("3x7 maydon yo'llari soni:", unique_paths(3, 7))
```

## Tushuntirish va Mantiq:
1. Kombinatorika va DP orqali `dp[j] = dp[j] + dp[j-1]` bir o'lchamli massivda hisoblanadi.

## Ishlash natijasi:
```text
Chiqish: 3x7 maydon yo'llari soni: 28
```

---

# 765-Topshiriq: Minimal yo'l yig'indisi (Minimum Path Sum)

## Topshiriq sharti:
MxN matritsadagi sonlar orqali o'tib eng kichik yig'indili yo'lni toping.

## Yechim (Python kodi):
```python
def min_path_sum(grid):
    m, n = len(grid), len(grid[0])
    dp = [float('inf')] * (n + 1)
    dp[1] = 0
    for row in grid:
        for j in range(n):
            dp[j + 1] = min(dp[j + 1], dp[j]) + row[j]
    return dp[n]

m = [
    [1, 3, 1],
    [1, 5, 1],
    [4, 2, 1]
]
print("Minimal yo'l yig'indisi:", min_path_sum(m))
```

## Tushuntirish va Mantiq:
1. Har bir katak yuqoridan yoki chapdan kelishi mumkin bo'lgan minimal narxni tanlaydi.

## Ishlash natijasi:
```text
Chiqish: Minimal yo'l yig'indisi: 7
```

---

# 766-Topshiriq: So'zlarni sindirish (Word Break I)

## Topshiriq sharti:
Satrni lug'atdagi so'zlarga bo'laklab chiqish mumkinligini DP orqali aniqlang.

## Yechim (Python kodi):
```python
def word_break(s, word_dict):
    sozlar = set(word_dict)
    dp = [False] * (len(s) + 1)
    dp[0] = True
    for i in range(1, len(s) + 1):
        for j in range(i):
            if dp[j] and s[j:i] in sozlar:
                dp[i] = True
                break
    return dp[len(s)]

print(word_break("leetcode", ["leet", "code"]))
print(word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]))
```

## Tushuntirish va Mantiq:
1. Agar `s[0:j]` bo'linsa va `s[j:i]` lug'atda bo'lsa, demak `s[0:i]` ham bo'linadi.

## Ishlash natijasi:
```text
Chiqish: True, False
```

---

# 767-Topshiriq: Uchburchak yo'li minimal yig'indisi (Triangle DP)

## Topshiriq sharti:
Uchburchak shaklidagi sonlar piramidasining tepasidan pastiga minimal yig'indini pastdan yuqoriga hisoblang.

## Yechim (Python kodi):
```python
def minimum_total(triangle):
    dp = triangle[-1].copy()
    for qator in range(len(triangle) - 2, -1, -1):
        for i in range(len(triangle[qator])):
            dp[i] = triangle[qator][i] + min(dp[i], dp[i + 1])
    return dp[0]

uchburchak = [
    [2],
    [3, 4],
    [6, 5, 7],
    [4, 1, 8, 3]
]
print("Piramida minimal yo'li:", minimum_total(uchburchak))
```

## Tushuntirish va Mantiq:
1. Pastdan yuqoriga (Bottom-Up) hisoblash chekka chegaralarni tekshirishni yo'qotadi va juda toza chiqadi.

## Ishlash natijasi:
```text
Chiqish: Piramida minimal yo'li: 11
```

---

# 768-Topshiriq: Matritsalarni zanjirli ko'paytirish (Matrix Chain Multiplication)

## Topshiriq sharti:
N ta matritsani ko'paytirishda skalyar ko'paytirishlar sonini minimallashtiruvchi qavslar tartibini toping.

## Yechim (Python kodi):
```python
def matrix_chain_order(p):
    n = len(p) - 1
    dp = [[0] * n for _ in range(n)]
    for L in range(2, n + 1):
        for i in range(n - L + 1):
            j = i + L - 1
            dp[i][j] = float('inf')
            for k in range(i, j):
                narx = dp[i][k] + dp[k + 1][j] + p[i] * p[k + 1] * p[j + 1]
                dp[i][j] = min(dp[i][j], narx)
    return dp[0][n - 1]

print("Minimal amallar:", matrix_chain_order([10, 20, 30, 40, 30]))
```

## Tushuntirish va Mantiq:
1. Oraliqlar bo'yicha dinamik dasturlash (Interval DP) orqali optimal qavslar yig'indisi topiladi.

## Ishlash natijasi:
```text
Chiqish: Minimal amallar: 30000
```

---

# 769-Topshiriq: Bitmask DP: Sayohatchi savdogar masalasi (TSP — Travelling Salesperson Problem)

## Topshiriq sharti:
N ta shaharni aylanib qaytishning eng qisqa marshrutini Bitmask DP bilan O(N^2 * 2^N) da hisoblang.

## Yechim (Python kodi):
```python
def tsp(masofalar):
    n = len(masofalar)
    memo = {}
    def qidiruv(mask, u):
        if mask == (1 << n) - 1:
            return masofalar[u][0]
        if (mask, u) in memo:
            return memo[(mask, u)]
        res = float('inf')
        for v in range(n):
            if not (mask & (1 << v)):
                res = min(res, masofalar[u][v] + qidiruv(mask | (1 << v), v))
        memo[(mask, u)] = res
        return res

    return qidiruv(1, 0)

dist = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]
print("TSP minimal masofa:", tsp(dist))
```

## Tushuntirish va Mantiq:
1. Bitmask yordamida tashrif buyurilgan shaharlar to'plami bitta butun sonning bitlarida ixcham saqlanadi.

## Ishlash natijasi:
```text
Chiqish: TSP minimal masofa: 80
```

---

# 770-Topshiriq: Backtracking: Barcha qism-to'plamlar (Subsets I)

## Topshiriq sharti:
N ta elementdan iborat massivning barcha mumkin bo'lgan 2^N ta qism-to'plamlarini hosil qiling.

## Yechim (Python kodi):
```python
def subsets(nums):
    natija = []
    def backtrack(boshlanish, yo_l):
        natija.append(list(yo_l))
        for i in range(boshlanish, len(nums)):
            yo_l.append(nums[i])
            backtrack(i + 1, yo_l)
            yo_l.pop() # Orqaga qaytish
    backtrack(0, [])
    return natija

print("Subsets [1, 2, 3] soni:", len(subsets([1, 2, 3])))
```

## Tushuntirish va Mantiq:
1. Backtracking orqali har bir shox o'rganilib, element qo'shiladi va qaytishda `pop()` qilinadi.

## Ishlash natijasi:
```text
Chiqish: Subsets [1, 2, 3] soni: 8
```

---

# 771-Topshiriq: Backtracking: Dublikatli qism-to'plamlar (Subsets II)

## Topshiriq sharti:
Takrorlanuvchi elementlar qatnashgan massivdan barcha noyob qism-to'plamlarni oling.

## Yechim (Python kodi):
```python
def subsets_with_dup(nums):
    nums.sort()
    natija = []
    def backtrack(start, path):
        natija.append(list(path))
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()
    backtrack(0, [])
    return natija

print("Noyob qism-to'plamlar [1, 2, 2]:", subsets_with_dup([1, 2, 2]))
```

## Tushuntirish va Mantiq:
1. Saralash va `nums[i] == nums[i-1]` sharti bitta darajada bir xil elementlarni takrorlanishidan saqlaydi.

## Ishlash natijasi:
```text
Chiqish: Noyob qism-to'plamlar [1, 2, 2]: [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]
```

---

# 772-Topshiriq: Backtracking: Permutatsiyalar (Permutations)

## Topshiriq sharti:
Elementlarning barcha N! ta mumkin bo'lgan o'rin almashtirishlarini chiqaring.

## Yechim (Python kodi):
```python
def permute(nums):
    natija = []
    def backtrack(bosh):
        if bosh == len(nums):
            natija.append(list(nums))
            return
        for i in range(bosh, len(nums)):
            nums[bosh], nums[i] = nums[i], nums[bosh]
            backtrack(bosh + 1)
            nums[bosh], nums[i] = nums[i], nums[bosh] # Qaytarish
    backtrack(0)
    return natija

print("Permutatsiyalar [1, 2, 3]:", permute([1, 2, 3]))
```

## Tushuntirish va Mantiq:
1. Elementlarni o'rnini almashtirib (swap) rekursiyaga kirish va qaytgach qayta almashtirish xotirani tejaydi.

## Ishlash natijasi:
```text
Chiqish: Permutatsiyalar [1, 2, 3]: [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 2, 1], [3, 1, 2]]
```

---

# 773-Topshiriq: Backtracking: Kombinatsiya yig'indisi (Combination Sum)

## Topshiriq sharti:
Elementlarni cheksiz takrorlash mumkin bo'lgan holda yig'indisi nishonga teng bo'lgan kombinatsiyalarni toping.

## Yechim (Python kodi):
```python
def combination_sum(candidates, target):
    natija = []
    def backtrack(start, qoldiq, path):
        if qoldiq == 0:
            natija.append(list(path))
            return
        for i in range(start, len(candidates)):
            if candidates[i] <= qoldiq:
                path.append(candidates[i])
                backtrack(i, qoldiq - candidates[i], path) # i qayta ishlatiladi
                path.pop()
    backtrack(0, target, [])
    return natija

print("Yig'indisi 7 bo'lganlar [2, 3, 6, 7]:", combination_sum([2, 3, 6, 7], 7))
```

## Tushuntirish va Mantiq:
1. Rekursiya indeksini `i` sifatida uzatish orqali bitta elementni bir necha bor tanlash ta'minlanadi.

## Ishlash natijasi:
```text
Chiqish: Yig'indisi 7 bo'lganlar [2, 3, 6, 7]: [[2, 2, 3], [7]]
```

---

# 774-Topshiriq: Backtracking: N-Malika masalasi (N-Queens)

## Topshiriq sharti:
NxN shaxmat taxtasiga N ta malikani bir-biriga xavf solmaydigan qilib joylashtirish usullari.

## Yechim (Python kodi):
```python
def solve_n_queens(n):
    ustunlar = set()
    musbat_diag = set() # (r + c)
    manfiy_diag = set() # (r - c)
    natijalar = 0

    def backtrack(r):
        nonlocal natijalar
        if r == n:
            natijalar += 1
            return
        for c in range(n):
            if c in ustunlar or (r + c) in musbat_diag or (r - c) in manfiy_diag:
                continue
            ustunlar.add(c); musbat_diag.add(r + c); manfiy_diag.add(r - c)
            backtrack(r + 1)
            ustunlar.remove(c); musbat_diag.remove(r + c); manfiy_diag.remove(r - c)

    backtrack(0)
    return natijalar

print("4-malika yechimlari soni:", solve_n_queens(4))
print("8-malika yechimlari soni:", solve_n_queens(8))
```

## Tushuntirish va Mantiq:
1. Diagonallar `r + c` va `r - c` to'plamlari orqali O(1) vaqtda tekshiriladi.

## Ishlash natijasi:
```text
Chiqish: 4-malika yechimlari soni: 2, 8-malika yechimlari soni: 92
```

---

# 775-Topshiriq: Backtracking: Sudoku Solver

## Topshiriq sharti:
9x9 katakli Sudoku boshqotirmasini to'liq yechuvchi algoritm.

## Yechim (Python kodi):
```python
def solve_sudoku(board):
    def mosmi(r, c, val):
        for i in range(9):
            if board[r][i] == val or board[i][c] == val: return False
            if board[3*(r//3) + i//3][3*(c//3) + i%3] == val: return False
        return True

    def yech():
        for r in range(9):
            for c in range(9):
                if board[r][c] == '.':
                    for ch in '123456789':
                        if mosmi(r, c, ch):
                            board[r][c] = ch
                            if yech(): return True
                            board[r][c] = '.'
                    return False
        return True

    yech()
    return board

board = [['5','3','.','.','7','.','.','.','.']] + [['.']*9 for _ in range(8)]
solve_sudoku(board)
print("1-qator yechimi:", board[0])
```

## Tushuntirish va Mantiq:
1. Har bir bo'sh katakka 1 dan 9 gacha nomzodlarni qo'yib tekshirish va ziddiyat bo'lsa orqaga qaytish.

## Ishlash natijasi:
```text
Chiqish: 1-qator yechimi: ['5', '3', '1', '2', '7', '4', '6', '8', '9']
```

---

# 776-Topshiriq: Backtracking: Matritsada so'z qidirish (Word Search)

## Topshiriq sharti:
2D harflar jadvalidan berilgan so'zni qo'shni kataklar orqali yig'ish mumkinligini aniqlang.

## Yechim (Python kodi):
```python
def exist(board, word):
    m, n = len(board), len(board[0])
    def dfs(r, c, k):
        if k == len(word): return True
        if r < 0 or r >= m or c < 0 or c >= n or board[r][c] != word[k]: return False
        temp = board[r][c]
        board[r][c] = '#' # Niqoblash
        res = (dfs(r+1, c, k+1) or dfs(r-1, c, k+1) or 
               dfs(r, c+1, k+1) or dfs(r, c-1, k+1))
        board[r][c] = temp
        return res

    for i in range(m):
        for j in range(n):
            if dfs(i, j, 0): return True
    return False

grid = [['A','B','C','E'], ['S','F','C','S'], ['A','D','E','E']]
print("ABCCED bormi:", exist(grid, "ABCCED"))
print("ABCB bormi:", exist(grid, "ABCB"))
```

## Tushuntirish va Mantiq:
1. Katakni vaqtincha '#' qilish qayta kirishning oldini oladi va qo'shimcha xotira sarflamaydi.

## Ishlash natijasi:
```text
Chiqish: ABCCED bormi: True, ABCB bormi: False
```

---

# 777-Topshiriq: Ochko'z algoritmlar: Faoliyatni tanlash (Activity Selection Problem)

## Topshiriq sharti:
Vaqti kesishmaydigan maksimal miqdordagi dars yoki tadbirlarni tanlang.

## Yechim (Python kodi):
```python
def max_activities(tadbirlar):
    # tadbirlar: [(boshlanish, tugash), ...]
    tadbirlar.sort(key=lambda x: x[1]) # Tugash vaqti bo'yicha saralash
    tanlangan = [tadbirlar[0]]
    oxirgi_tugash = tadbirlar[0][1]
    for b, t in tadbirlar[1:]:
        if b >= oxirgi_tugash:
            tanlangan.append((b, t))
            oxirgi_tugash = t
    return tanlangan

print("Tanlangan faoliyatlar:", max_activities([(1, 4), (3, 5), (0, 6), (5, 7), (8, 9), (5, 9)]))
```

## Tushuntirish va Mantiq:
1. Eng ertaroq tugaydigan faoliyatni tanlash qolgan vaqt oralig'ini maksimal bo'sh qoldiradi.

## Ishlash natijasi:
```text
Chiqish: Tanlangan faoliyatlar: [(1, 4), (5, 7), (8, 9)]
```

---

# 778-Topshiriq: Ochko'z algoritmlar: Sakrash o'yini (Jump Game I)

## Topshiriq sharti:
Har bir katakdagi maksimal sakrash masofasi bilan oxirgi katakka yetib borish mumkinligini O(n) da toping.

## Yechim (Python kodi):
```python
def can_jump(nums):
    maksimal_yetish = 0
    for i, x in enumerate(nums):
        if i > maksimal_yetish:
            return False
        maksimal_yetish = max(maksimal_yetish, i + x)
    return True

print("[2, 3, 1, 1, 4] yetadimi:", can_jump([2, 3, 1, 1, 4]))
print("[3, 2, 1, 0, 4] yetadimi:", can_jump([3, 2, 1, 0, 4]))
```

## Tushuntirish va Mantiq:
1. Ochko'zlik bilan erishish mumkin bo'lgan maksimal ufq (Reach Horizon) doim yangilanib boradi.

## Ishlash natijasi:
```text
Chiqish: [2, 3, 1, 1, 4] yetadimi: True, [3, 2, 1, 0, 4] yetadimi: False
```

---

# 779-Topshiriq: Ochko'z algoritmlar: Sakrash o'yini II (Jump Game II — Minimal sakrashlar)

## Topshiriq sharti:
Oxirgi katakka yetib borish uchun talab qilinadigan minimal sakrashlar sonini toping.

## Yechim (Python kodi):
```python
def min_jumps(nums):
    sakrashlar = joriy_oxiri = eng_uzoq = 0
    for i in range(len(nums) - 1):
        eng_uzoq = max(eng_uzoq, i + nums[i])
        if i == joriy_oxiri:
            sakrashlar += 1
            joriy_oxiri = eng_uzoq
    return sakrashlar

print("Minimal sakrashlar:", min_jumps([2, 3, 1, 1, 4]))
```

## Tushuntirish va Mantiq:
1. Har safar joriy chegaraga yetganda sakrash amalga oshiriladi va yangi uzoq marra belgilanadi.

## Ishlash natijasi:
```text
Chiqish: Minimal sakrashlar: 2
```

---

# 780-Topshiriq: Ochko'z algoritmlar: Gaz stansiyalari (Gas Station Circuit)

## Topshiriq sharti:
Aylanma yo'ldagi gaz stansiyalaridan qaysi biridan boshlab butun yo'lni aylanib chiqish mumkinligini toping.

## Yechim (Python kodi):
```python
def can_complete_circuit(gas, cost):
    if sum(gas) < sum(cost): return -1
    jami_bak = start = 0
    for i in range(len(gas)):
        jami_bak += gas[i] - cost[i]
        if jami_bak < 0:
            start = i + 1
            jami_bak = 0
    return start

print("Boshlang'ich stansiya:", can_complete_circuit([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]))
```

## Tushuntirish va Mantiq:
1. Agar umumiy benzin xarajatdan ko'p bo'lsa, qat'iy yechim mavjud. Bak manfiy bo'lgan zahoti keyingi indeks yangi nomzod bo'ladi.

## Ishlash natijasi:
```text
Chiqish: Boshlang'ich stansiya: 3
```

---

# 781-Topshiriq: Ochko'z: Konfet tarqatish (Candy Distribution)

## Topshiriq sharti:
Reytingi yuqori bolalarga qo'shnisidan ko'p konfet berish sharti bilan minimal konfetlar sonini toping.

## Yechim (Python kodi):
```python
def candy(ratings):
    n = len(ratings)
    konfet = [1] * n
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            konfet[i] = konfet[i - 1] + 1
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            konfet[i] = max(konfet[i], konfet[i + 1] + 1)
    return sum(konfet)

print("Minimal konfetlar:", candy([1, 0, 2]))
print("Minimal konfetlar 2:", candy([1, 2, 2]))
```

## Tushuntirish va Mantiq:
1. Chapdan o'ngga va o'ngdan chapga ikki martalik o'tish bilan minimal optimal taqsimot kafolatlanadi.

## Ishlash natijasi:
```text
Chiqish: Minimal konfetlar: 5, Minimal konfetlar 2: 4
```

---

# 782-Topshiriq: DP: Bo'linuvchi qism-ketma-ketliklar soni (Number of Dice Rolls With Target Sum)

## Topshiriq sharti:
D ta zar tashlanganda ochkolar yig'indisi Target ga teng bo'lish usullari soni.

## Yechim (Python kodi):
```python
def num_rolls_to_target(d, f, target):
    dp = [0] * (target + 1)
    dp[0] = 1
    for _ in range(d):
        yangi = [0] * (target + 1)
        for i in range(1, target + 1):
            for k in range(1, min(f, i) + 1):
                yangi[i] += dp[i - k]
        dp = yangi
    return dp[target]

print("2 ta 6 qirrali zar bilan 7 hosil qilish:", num_rolls_to_target(2, 6, 7))
```

## Tushuntirish va Mantiq:
1. Ehtimollar nazariyasi va o'yinlar mantiqida qatlamli DP usuli.

## Ishlash natijasi:
```text
Chiqish: 2 ta 6 qirrali zar bilan 7 hosil qilish: 6
```

---

# 783-Topshiriq: DP: Aktsiyalar savdosi (Best Time to Buy and Sell Stock with Cooldown)

## Topshiriq sharti:
Sotishdan keyin 1 kunlik tanaffus (cooldown) bo'lganda maksimal foydani hisoblang.

## Yechim (Python kodi):
```python
def max_profit_cooldown(prices):
    sold, held, reset = 0, -float('inf'), 0
    for p in prices:
        pre_sold = sold
        sold = held + p
        held = max(held, reset - p)
        reset = max(reset, pre_sold)
    return max(sold, reset)

print("Maksimal savdo foydasi:", max_profit_cooldown([1, 2, 3, 0, 2]))
```

## Tushuntirish va Mantiq:
1. Chekli holatlar mashinasi (State Machine DP) moliyaviy strategiyalarni optimallashtiradi.

## Ishlash natijasi:
```text
Chiqish: Maksimal savdo foydasi: 3
```

---

# 784-Topshiriq: DP: Aktsiyalar savdosi K marta (Buy and Sell Stock IV)

## Topshiriq sharti:
Ko'pi bilan K ta savdo amali bajarish orqali eng yuqori daromadni toping.

## Yechim (Python kodi):
```python
def max_profit_k(k, prices):
    if not prices or k == 0: return 0
    buy = [-float('inf')] * (k + 1)
    sell = [0] * (k + 1)
    for p in prices:
        for i in range(1, k + 1):
            buy[i] = max(buy[i], sell[i - 1] - p)
            sell[i] = max(sell[i], buy[i] + p)
    return sell[k]

print("2 marta savdo bilan maksimal foyda:", max_profit_k(2, [3, 2, 6, 5, 0, 3]))
```

## Tushuntirish va Mantiq:
1. K ta savdo bosqichi uchun dinamik o'tishlar massivi yuritiladi.

## Ishlash natijasi:
```text
Chiqish: 2 marta savdo bilan maksimal foyda: 7
```

---

# 785-Topshiriq: DP: Pufakchalarni yorish (Burst Balloons)

## Topshiriq sharti:
Pufakchalarni yorishdan hosil bo'ladigan tangalar miqdorini maksimallashtiring.

## Yechim (Python kodi):
```python
def max_coins(nums):
    arr = [1] + [x for x in nums if x > 0] + [1]
    n = len(arr)
    dp = [[0] * n for _ in range(n)]
    for L in range(2, n):
        for left in range(n - L):
            right = left + L
            for k in range(left + 1, right):
                dp[left][right] = max(dp[left][right],
                    arr[left] * arr[k] * arr[right] + dp[left][k] + dp[k][right])
    return dp[0][n - 1]

print("Maksimal tangalar:", max_coins([3, 1, 5, 8]))
```

## Tushuntirish va Mantiq:
1. Qaysi pufak eng oxirida yorilishini tanlash orqali intervalli DP quriladi.

## Ishlash natijasi:
```text
Chiqish: Maksimal tangalar: 167
```

---

# 786-Topshiriq: DP: Eng katta kvadrat maydoni (Maximal Square)

## Topshiriq sharti:
Faqat '1' lardan iborat eng katta kvadrat o'lchamini 2D matritsada toping.

## Yechim (Python kodi):
```python
def maximal_square(matrix):
    if not matrix: return 0
    m, n = len(matrix), len(matrix[0])
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    max_side = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if matrix[i - 1][j - 1] == '1':
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
                max_side = max(max_side, dp[i][j])
    return max_side * max_side

mat = [
    ['1', '0', '1', '0', '0'],
    ['1', '0', '1', '1', '1'],
    ['1', '1', '1', '1', '1'],
    ['1', '0', '0', '1', '0']
]
print("Maksimal kvadrat yuzi:", maximal_square(mat))
```

## Tushuntirish va Mantiq:
1. Har bir katakda uning chap, yuqori va diagonal qo'shnilarining eng kichigi olinadi.

## Ishlash natijasi:
```text
Chiqish: Maksimal kvadrat yuzi: 4
```

---

# 787-Topshiriq: Ochko'z: Vaznli intervallarni rejalashtirish (Weighted Interval Scheduling)

## Topshiriq sharti:
Har bir oraliqning o'z qiymati (vazni) bo'lganda, DP + Binary Search bilan maksimal qiymatni toping.

## Yechim (Python kodi):
```python
import bisect

def job_scheduling(jobs):
    # jobs: [(start, end, profit), ...]
    jobs.sort(key=lambda x: x[1])
    dp = [(0, 0)] # (tugash_vaqti, jami_profit)
    for s, e, p in jobs:
        idx = bisect.bisect_right(dp, (s, float('inf'))) - 1
        yangi_profit = dp[idx][1] + p
        if yangi_profit > dp[-1][1]:
            dp.append((e, yangi_profit))
    return dp[-1][1]

ishlar = [(1, 2, 50), (3, 5, 20), (6, 19, 100), (2, 100, 200)]
print("Maksimal ish daromadi:", job_scheduling(ishlar))
```

## Tushuntirish va Mantiq:
1. Ikkilik qidiruv bilan kesishmaydigan eng yaqin oraliqni O(log n) da topib DP yangilanadi.

## Ishlash natijasi:
```text
Chiqish: Maksimal ish daromadi: 250
```

---

# 788-Topshiriq: Backtracking: Palindrom bo'laklarga ajratish (Palindrome Partitioning)

## Topshiriq sharti:
Satrni har bir bo'lagi palindrom bo'ladigan barcha usullarda kesing.

## Yechim (Python kodi):
```python
def partition_palindrome(s):
    natija = []
    def is_pal(sub): return sub == sub[::-1]
    def backtrack(start, path):
        if start == len(s):
            natija.append(list(path))
            return
        for end in range(start + 1, len(s) + 1):
            bolak = s[start:end]
            if is_pal(bolak):
                path.append(bolak)
                backtrack(end, path)
                path.pop()
    backtrack(0, [])
    return natija

print("aab bo'laklari:", partition_palindrome("aab"))
```

## Tushuntirish va Mantiq:
1. Rekursiya barcha mumkin bo'lgan palindrom qirqimlarni chuqur o'rganadi.

## Ishlash natijasi:
```text
Chiqish: aab bo'laklari: [['a', 'a', 'b'], ['aa', 'b']]
```

---

# 789-Topshiriq: DP: So'z masofasi (Interleaving String)

## Topshiriq sharti:
Ikkita satr harflarini aralashtirib uchinchi satrni hosil qilish mumkinligini aniqlang.

## Yechim (Python kodi):
```python
def is_interleave(s1, s2, s3):
    if len(s1) + len(s2) != len(s3): return False
    dp = [True] * (len(s2) + 1)
    for j in range(1, len(s2) + 1):
        dp[j] = dp[j - 1] and s2[j - 1] == s3[j - 1]
    for i in range(1, len(s1) + 1):
        dp[0] = dp[0] and s1[i - 1] == s3[i - 1]
        for j in range(1, len(s2) + 1):
            dp[j] = (dp[j] and s1[i - 1] == s3[i + j - 1]) or (dp[j - 1] and s2[j - 1] == s3[i + j - 1])
    return dp[-1]

print("Mosmi:", is_interleave("aabcc", "dbbca", "aadbbcbcac"))
```

## Tushuntirish va Mantiq:
1. 2D DP panjarasida yurib har ikki satrdan navbatma-navbat harflar olinishi tekshiriladi.

## Ishlash natijasi:
```text
Chiqish: Mosmi: True
```

---

# 790-Topshiriq: DP: Raqamli Dinamik Dasturlash (Digit DP tushunchasi)

## Topshiriq sharti:
1 dan N gacha bo'lgan sonlar orasida ma'lum raqam (masalan, 1 raqami) necha marta qatnashganini hisoblang.

## Yechim (Python kodi):
```python
def count_digit_one(n):
    hisob = 0
    i = 1
    while i <= n:
        divider = i * 10
        hisob += (n // divider) * i + min(max(n % divider - i + 1, 0), i)
        i *= 10
    return hisob

print("13 gacha '1' lar soni:", count_digit_one(13))
print("100 gacha '1' lar soni:", count_digit_one(100))
```

## Tushuntirish va Mantiq:
1. Raqamlar pozitsiyalari (birliklar, o'nliklar, yuzliklar) bo'yicha matematik qonuniyat bilan O(log10 N) da hisoblanadi.

## Ishlash natijasi:
```text
Chiqish: 13 gacha '1' lar soni: 6, 100 gacha '1' lar soni: 21
```

---

# 791-Topshiriq: DP: Shifrlangan xabarlar soni (Decode Ways)

## Topshiriq sharti:
'1'->'A', '2'->'B'...'26'->'Z' shifrini necha xil usulda dekodlash mumkinligini toping.

## Yechim (Python kodi):
```python
def num_decodings(s):
    if not s or s[0] == '0': return 0
    old2, old1 = 1, 1
    for i in range(1, len(s)):
        joriy = 0
        if s[i] != '0': joriy += old1
        if 10 <= int(s[i-1:i+1]) <= 26: joriy += old2
        old2, old1 = old1, joriy
    return old1

print("12 dekodlash usullari:", num_decodings("12"))
print("226 dekodlash usullari:", num_decodings("226"))
```

## Tushuntirish va Mantiq:
1. Har bir raqam bitta harf yoki oldingisi bilan birgalikda 10-26 oraliqdagi harf bo'lishi mumkin.

## Ishlash natijasi:
```text
Chiqish: 12 dekodlash usullari: 2, 226 dekodlash usullari: 3
```

---

# 792-Topshiriq: Backtracking: Graf rangi (Graph Coloring / M-Coloring)

## Topshiriq sharti:
Graf tugunlarini M ta rang bilan qo'shnilar bir xil rang olmasdan bo'yash.

## Yechim (Python kodi):
```python
def graph_m_coloring(graf, m):
    ranglar = {}
    tugunlar = list(graf.keys())
    
    def xavfsizmi(u, rang):
        for v in graf[u]:
            if ranglar.get(v) == rang: return False
        return True

    def backtrack(idx):
        if idx == len(tugunlar): return True
        u = tugunlar[idx]
        for c in range(1, m + 1):
            if xavfsizmi(u, c):
                ranglar[u] = c
                if backtrack(idx + 1): return True
                del ranglar[u]
        return False

    mumkin = backtrack(0)
    return mumkin, ranglar

g = {0: [1, 2], 1: [0, 2], 2: [0, 1]} # Uchburchak
mumkin, res = graph_m_coloring(g, 3)
print("3 rang bilan bo'yaladimi:", mumkin, res)
```

## Tushuntirish va Mantiq:
1. Xarita bo'yash va registrlarni taqsimlashda NP-to'liq masalalarni Backtracking bilan yechish.

## Ishlash natijasi:
```text
Chiqish: 3 rang bilan bo'yaladimi: True {0: 1, 1: 2, 2: 3}
```

---

# 793-Topshiriq: Backtracking: Gamilton sikli (Hamiltonian Cycle)

## Topshiriq sharti:
Grafning barcha tugunlariga aynan bir martadan tashrif buyuruvchi aylanma yo'lni toping.

## Yechim (Python kodi):
```python
def hamiltonian_cycle(graf):
    n = len(graf)
    yol = [0]
    def xavfsizmi(v, pos):
        if v not in graf[yol[pos - 1]]: return False
        if v in yol: return False
        return True

    def backtrack(pos):
        if pos == n:
            return yol[0] in graf[yol[-1]]
        for v in range(1, n):
            if xavfsizmi(v, pos):
                yol.append(v)
                if backtrack(pos + 1): return True
                yol.pop()
        return False

    return yol if backtrack(1) else None

g = {0: [1, 3], 1: [0, 2], 2: [1, 3], 3: [0, 2]}
print("Gamilton sikli:", hamiltonian_cycle(g))
```

## Tushuntirish va Mantiq:
1. Euler yo'lidan farqli ravishda barcha tugunlardan bir martadan o'tish qat'iy NP-murakkab masaladir.

## Ishlash natijasi:
```text
Chiqish: Gamilton sikli: [0, 1, 2, 3]
```

---

# 794-Topshiriq: DP: Daraxtda mustaqil to'plam (Maximum Independent Set on Tree)

## Topshiriq sharti:
Daraxtda qo'shni bo'lmagan tugunlarning maksimal sonini toping.

## Yechim (Python kodi):
```python
def max_independent_set(ildiz):
    def dfs(node):
        if not node: return 0, 0
        chap_ichida, chap_tashqari = dfs(node.left)
        ong_ichida, ong_tashqari = dfs(node.right)
        
        # Tugun tanlansa, bolalar tanlanmaydi
        ichida = 1 + chap_tashqari + ong_tashqari
        # Tugun tanlanmasa, bolalarning maksimumi olinadi
        tashqari = max(chap_ichida, chap_tashqari) + max(ong_ichida, ong_tashqari)
        return ichida, tashqari

    return max(dfs(ildiz))

t = DaraxtTuguni(1, DaraxtTuguni(2), DaraxtTuguni(3))
print("Daraxt mustaqil to'plam hajmi:", max_independent_set(t))
```

## Tushuntirish va Mantiq:
1. Daraxtlarda dinamik dasturlash (Tree DP) har doim barglardan ildizga qarab hisoblanadi.

## Ishlash natijasi:
```text
Chiqish: Daraxt mustaqil to'plam hajmi: 2
```

---

# 795-Topshiriq: DP: Prefiks va Qoldiqlar bilan K ga karrali qism-massivlar (Subarray Sums Divisible by K)

## Topshiriq sharti:
Yig'indisi K ga qoldiqsiz bo'linuvchi qism-massivlar sonini O(n) da hisoblang.

## Yechim (Python kodi):
```python
def subarrays_div_by_k(nums, k):
    qoldiqlar = {0: 1}
    joriy_yigindi = 0
    hisob = 0
    for x in nums:
        joriy_yigindi += x
        rem = joriy_yigindi % k
        hisob += qoldiqlar.get(rem, 0)
        qoldiqlar[rem] = qoldiqlar.get(rem, 0) + 1
    return hisob

print("5 ga bo'linuvchilar:", subarrays_div_by_k([4, 5, 0, -2, -3, 1], 5))
```

## Tushuntirish va Mantiq:
1. Modulli arifmetika va Hash Map orqali O(n^2) lik masala chiziqli O(n) ga keltiriladi.

## Ishlash natijasi:
```text
Chiqish: 5 ga bo'linuvchilar: 7
```

---

# 796-Topshiriq: DP: Xarid qilish narxi (Target Sum: +/- belgilarini qo'yish)

## Topshiriq sharti:
Massiv elementlari oldiga '+' yoki '-' qo'yib nishon qiymatni hosil qilish usullari soni.

## Yechim (Python kodi):
```python
def find_target_sum_ways(nums, target):
    jami = sum(nums)
    if (jami + target) % 2 != 0 or jami < abs(target): return 0
    P = (jami + target) // 2
    dp = [0] * (P + 1)
    dp[0] = 1
    for x in nums:
        for j in range(P, x - 1, -1):
            dp[j] += dp[j - x]
    return dp[P]

print("Yig'indi 3 hosil qilish usullari [1, 1, 1, 1, 1]:", find_target_sum_ways([1, 1, 1, 1, 1], 3))
```

## Tushuntirish va Mantiq:
1. Matematik soddalashtirish orqali masala 0/1 Knapsack usullar soniga o'giriladi.

## Ishlash natijasi:
```text
Chiqish: Yig'indi 3 hosil qilish usullari [1, 1, 1, 1, 1]: 5
```

---

# 797-Topshiriq: DP: Eng qimmatli mustaqil interval to'plami (Weighted Interval DP)

## Topshiriq sharti:
Intervallar orasidagi munosabatlarni qadamma-qadam keshlab boruvchi optimizator.

## Yechim (Python kodi):
```python
def max_profit_schedule(intervals):
    # intervals: [(start, end, val)]
    intervals.sort(key=lambda x: x[1])
    n = len(intervals)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        s, e, v = intervals[i - 1]
        dp[i] = max(dp[i - 1], v)
        for j in range(i - 1, 0, -1):
            if intervals[j - 1][1] <= s:
                dp[i] = max(dp[i], dp[j] + v)
                break
    return dp[n]

print("Maksimal qiymat:", max_profit_schedule([(1, 3, 20), (2, 5, 30), (4, 6, 50)]))
```

## Tushuntirish va Mantiq:
1. Tadbirlarni rejalashtirishda vaqt kesishuvlarini samarali boshqarish.

## Ishlash natijasi:
```text
Chiqish: Maksimal qiymat: 70
```

---

# 798-Topshiriq: DP: Binar daraxtlar soni (Unique Binary Search Trees — Catalan sonlari)

## Topshiriq sharti:
1 dan N gacha sonlardan nechta turli xil BST tuzish mumkinligini toping.

## Yechim (Python kodi):
```python
def num_trees(n):
    dp = [0] * (n + 1)
    dp[0] = dp[1] = 1
    for i in range(2, n + 1):
        for j in range(1, i + 1):
            dp[i] += dp[j - 1] * dp[i - j]
    return dp[n]

print("3 ta tugun bilan BST lar soni:", num_trees(3))
print("4 ta tugun bilan BST lar soni:", num_trees(4))
```

## Tushuntirish va Mantiq:
1. Catalan sonlari (Catalan Numbers): `C(n) = sum(C(i-1)*C(n-i))` formulasiga asoslangan.

## Ishlash natijasi:
```text
Chiqish: 3 ta tugun bilan BST lar soni: 5, 4 ta tugun bilan BST lar soni: 14
```

---

# 799-Topshiriq: Ochko'z: Birlashtirish narxi (Minimum Cost to Connect Sticks / Huffman Coding)

## Topshiriq sharti:
Tayoqchalarni eng kichiklarini doim birlashtirib borish orqali minimal umumiy narxni toping.

## Yechim (Python kodi):
```python
import heapq

def connect_sticks(sticks):
    heapq.heapify(sticks)
    jami_narx = 0
    while len(sticks) > 1:
        bir = heapq.heappop(sticks)
        ikki = heapq.heappop(sticks)
        yangi = bir + ikki
        jami_narx += yangi
        heapq.heappush(sticks, yangi)
    return jami_narx

print("Minimal birlashtirish xarajati:", connect_sticks([2, 4, 3]))
print("Minimal birlashtirish xarajati 2:", connect_sticks([1, 8, 3, 5]))
```

## Tushuntirish va Mantiq:
1. Huffman arxivi va fayllarni siqish aynan eng kam chastotali elementlarni Min-Heap bilan birlashtirishga asoslanadi.

## Ishlash natijasi:
```text
Chiqish: Minimal birlashtirish xarajati: 14, Minimal birlashtirish xarajati 2: 30
```

---

# 800-Topshiriq: Mukammal Optimizator: Dinamik Dasturlash va Backtracking integratsiyasi (Knapsack Path Reconstruction)

## Topshiriq sharti:
Nafaqat maksimal ryukzak qiymatini, balki tanlangan aynan qaysi buyumlar ekanligini to'liq tiklab bering.

## Yechim (Python kodi):
```python
def knapsack_reconstruct(W, ogirliklar, narxlar):
    n = len(narxlar)
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        w = ogirliklar[i - 1]
        v = narxlar[i - 1]
        for j in range(W + 1):
            if w <= j:
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - w] + v)
            else:
                dp[i][j] = dp[i - 1][j]
                
    # Yo'lni orqaga qarab tiklash (Backtracking)
    tanlanganlar = []
    j = W
    for i in range(n, 0, -1):
        if dp[i][j] != dp[i - 1][j]:
            tanlanganlar.append(i - 1)
            j -= ogirliklar[i - 1]
            
    return dp[n][W], tanlanganlar[::-1]

qiymat, buyumlar = knapsack_reconstruct(50, [10, 20, 30], [60, 100, 120])
print(f"Maksimal qiymat: {qiymat}, Tanlangan buyum indekslari: {buyumlar}")
```

## Tushuntirish va Mantiq:
1. DP jadvali asosida orqaga qarab yechimni tiklash (Path Reconstruction) sun'iy intellekt va resurs taqsimoti tizimlarida yakuniy natijani tushuntirib berishda (explainability) muhimdir.

## Ishlash natijasi:
```text
Chiqish: Maksimal qiymat: 220, Tanlangan buyum indekslari: [1, 2]
```

---

