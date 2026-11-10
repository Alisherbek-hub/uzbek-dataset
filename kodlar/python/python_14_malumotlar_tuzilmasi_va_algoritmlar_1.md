# Python Dasturlash Tili — 14-Qism: Ma'lumotlar Tuzilmasi va Algoritmlar (1-Qism)
## (651-700 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam poydevor algoritmlar, ma'lumotlar tuzilmalari va texnik intervyu masalalarini qamrab oladi:
* Chiziqli va ikkilik qidiruv, binary search chegaralari;
* Saralash algoritmlari: Bubble, Selection, Insertion, Merge, Quick, Counting Sort;
* Ikki ko'rsatkich (Two Pointers) va Siljuvchi darcha (Sliding Window) usullari;
* Bog'langan ro'yxatlar (Singly, Doubly Linked Lists), Floyd sikl detektori;
* Stek (Stack LIFO), Navbat (Queue FIFO), Monotonik stek va LRU Cache;
* Bit manipulatsiyalari va Prefix Sum optimizatsiyalari;

---

# 651-Topshiriq: Chiziqli qidiruv (Linear Search) va O(n) murakkablik

## Topshiriq sharti:
Massivdan berilgan elementning indeksini topuvchi chiziqli qidiruv funksiyasini yozing.

## Yechim (Python kodi):
```python
def linear_search(arr, nishon):
    for i, qiymat in enumerate(arr):
        if qiymat == nishon:
            return i
    return -1

sonlar = [14, 25, 8, 42, 19, 56]
print("42 indeksi:", linear_search(sonlar, 42))
print("100 indeksi:", linear_search(sonlar, 100))
```

## Tushuntirish va Mantiq:
1. Chiziqli qidiruv saralanmagan massivlarda barcha elementlarni birma-bir ko'rib chiqadi. Vaqt murakkabligi: O(n).

## Ishlash natijasi:
```text
Chiqish: 42 indeksi: 3, 100 indeksi: -1
```

---

# 652-Topshiriq: Ikkilik qidiruv (Binary Search) va O(log n)

## Topshiriq sharti:
Saralangan massivda elementni O(log n) vaqtda topuvchi ikkilik qidiruv algoritmini yozing.

## Yechim (Python kodi):
```python
def binary_search(arr, nishon):
    chap, ong = 0, len(arr) - 1
    while chap <= ong:
        orta = (chap + ong) // 2
        if arr[orta] == nishon:
            return orta
        elif arr[orta] < nishon:
            chap = orta + 1
        else:
            ong = orta - 1
    return -1

saralangan = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
print("23 indeksi:", binary_search(saralangan, 23))
print("15 indeksi:", binary_search(saralangan, 15))
```

## Tushuntirish va Mantiq:
1. Ikkilik qidiruv har qadamda qidiruv sohasini 2 barobarga qisqartiradi. Shart: massiv oldindan saralangan bo'lishi shart.

## Ishlash natijasi:
```text
Chiqish: 23 indeksi: 5, 15 indeksi: -1
```

---

# 653-Topshiriq: Ikkilik qidiruv: bisect_left (Lower Bound)

## Topshiriq sharti:
Massivda nishon qiymatidan kichik bo'lmagan birinchi element indeksini toping.

## Yechim (Python kodi):
```python
def lower_bound(arr, nishon):
    chap, ong = 0, len(arr)
    while chap < ong:
        orta = (chap + ong) // 2
        if arr[orta] < nishon:
            chap = orta + 1
        else:
            ong = orta
    return chap

sonlar = [1, 2, 4, 4, 4, 6, 8]
print("4 ning lower bound:", lower_bound(sonlar, 4))
print("5 ning lower bound:", lower_bound(sonlar, 5))
```

## Tushuntirish va Mantiq:
1. `lower_bound` elementni tartibni buzmasdan qo'yish mumkin bo'lgan eng chap indeksni beradi.

## Ishlash natijasi:
```text
Chiqish: 4 ning lower bound: 2, 5 ning lower bound: 5
```

---

# 654-Topshiriq: Pufaksimon saralash (Bubble Sort)

## Topshiriq sharti:
Qo'shni elementlarni solishtirib o'rin almashtiruvchi pufaksimon saralash algoritmini amalga oshiring.

## Yechim (Python kodi):
```python
def bubble_sort(arr):
    n = len(arr)
    massiv = arr.copy()
    for i in range(n):
        almashdi = False
        for j in range(0, n - i - 1):
            if massiv[j] > massiv[j + 1]:
                massiv[j], massiv[j + 1] = massiv[j + 1], massiv[j]
                almashdi = True
        if not almashdi:
            break
    return massiv

print(bubble_sort([64, 34, 25, 12, 22, 11, 90]))
```

## Tushuntirish va Mantiq:
1. Agar biror o'tishda hech qanday almashish yuz bermasa, massiv saralangan hisoblanadi va sikl muddatidan oldin to'xtaydi.

## Ishlash natijasi:
```text
Chiqish: [11, 12, 22, 25, 34, 64, 90]
```

---

# 655-Topshiriq: Tanlash orqali saralash (Selection Sort)

## Topshiriq sharti:
Har bir qadamda qolgan qismning eng kichik elementini topib boshiga joylashtiring.

## Yechim (Python kodi):
```python
def selection_sort(arr):
    massiv = arr.copy()
    n = len(massiv)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if massiv[j] < massiv[min_idx]:
                min_idx = j
        massiv[i], massiv[min_idx] = massiv[min_idx], massiv[i]
    return massiv

print(selection_sort([29, 10, 14, 37, 13]))
```

## Tushuntirish va Mantiq:
1. Selection sort almashishlar sonini minimal (aniq n ta) saqlaydi, ammo taqqoslashlar soni har doim O(n^2) bo'ladi.

## Ishlash natijasi:
```text
Chiqish: [10, 13, 14, 29, 37]
```

---

# 656-Topshiriq: Qo'yish orqali saralash (Insertion Sort)

## Topshiriq sharti:
Karta o'yinidagi kabi har bir yangi elementni saralangan qismga to'g'ri o'rniga joylang.

## Yechim (Python kodi):
```python
def insertion_sort(arr):
    massiv = arr.copy()
    for i in range(1, len(massiv)):
        kalit = massiv[i]
        j = i - 1
        while j >= 0 and massiv[j] > kalit:
            massiv[j + 1] = massiv[j]
            j -= 1
        massiv[j + 1] = kalit
    return massiv

print(insertion_sort([12, 11, 13, 5, 6]))
```

## Tushuntirish va Mantiq:
1. Insertion sort kichik yoki deyarli saralangan massivlarda juda tez (O(n)) ishlaydi.

## Ishlash natijasi:
```text
Chiqish: [5, 6, 11, 12, 13]
```

---

# 657-Topshiriq: Birlashtirish orqali saralash (Merge Sort) — O(n log n)

## Topshiriq sharti:
Bo'lib tashla va hukmronlik qil (Divide and Conquer) tamoyiliga asoslangan Merge Sort algoritmini yozing.

## Yechim (Python kodi):
```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    orta = len(arr) // 2
    chap = merge_sort(arr[:orta])
    ong = merge_sort(arr[orta:])
    
    # Birlashtirish (Merge)
    natija = []
    i = j = 0
    while i < len(chap) and j < len(ong):
        if chap[i] <= ong[j]:
            natija.append(chap[i])
            i += 1
        else:
            natija.append(ong[j])
            j += 1
    natija.extend(chap[i:])
    natija.extend(ong[j:])
    return natija

print(merge_sort([38, 27, 43, 3, 9, 82, 10]))
```

## Tushuntirish va Mantiq:
1. Merge sort barqaror (stable) saralash bo'lib, har doim O(n log n) kafolatlangan vaqt talab qiladi.

## Ishlash natijasi:
```text
Chiqish: [3, 9, 10, 27, 38, 43, 82]
```

---

# 658-Topshiriq: Tezkor saralash (Quick Sort)

## Topshiriq sharti:
Tayanch element (Pivot) tanlab, undan kichik va kattalarga ajratuvchi Quick Sort algoritmini tuzing.

## Yechim (Python kodi):
```python
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    kichik = [x for x in arr if x < pivot]
    teng = [x for x in arr if x == pivot]
    katta = [x for x in arr if x > pivot]
    return quick_sort(kichik) + teng + quick_sort(katta)

print(quick_sort([10, 80, 30, 90, 40, 50, 70]))
```

## Tushuntirish va Mantiq:
1. O'rtacha hisobda O(n log n) ishlaydi va amaliyotda kesh xotirasi bilan ishlash qulayligi tufayli eng tez saralashlardan biridir.

## Ishlash natijasi:
```text
Chiqish: [10, 30, 40, 50, 70, 80, 90]
```

---

# 659-Topshiriq: Sanash orqali saralash (Counting Sort) — O(n + k)

## Topshiriq sharti:
Elementlar qiymat diapazoni cheklangan bo'lgan butun sonlar massivini chiziqli vaqtda saralang.

## Yechim (Python kodi):
```python
def counting_sort(arr):
    if not arr: return []
    max_val = max(arr)
    hisob = [0] * (max_val + 1)
    for x in arr:
        hisob[x] += 1
    saralangan = []
    for son, marta in enumerate(hisob):
        saralangan.extend([son] * marta)
    return saralangan

print(counting_sort([4, 2, 2, 8, 3, 3, 1]))
```

## Tushuntirish va Mantiq:
1. Taqqoslashga asoslanmagan saralash bo'lib, maksimal qiymat k kichik bo'lganda O(n+k) da ishlaydi.

## Ishlash natijasi:
```text
Chiqish: [1, 2, 2, 3, 3, 4, 8]
```

---

# 660-Topshiriq: Ikki ko'rsatkich: Saralangan massivda Two Sum

## Topshiriq sharti:
Saralangan massivda yig'indisi nishonga teng bo'lgan ikki son indeksini O(n) vaqtda toping.

## Yechim (Python kodi):
```python
def two_sum_sorted(arr, target):
    chap = 0
    ong = len(arr) - 1
    while chap < ong:
        jami = arr[chap] + arr[ong]
        if jami == target:
            return (chap, ong)
        elif jami < target:
            chap += 1
        else:
            ong -= 1
    return None

print(two_sum_sorted([2, 7, 11, 15, 18], 22))
```

## Tushuntirish va Mantiq:
1. Ikki tomondan (chap va o'ng) markazga qarab siljish orqali O(n^2) li vazifani O(n) da hal qilish mumkin.

## Ishlash natijasi:
```text
Chiqish: (1, 3)
```

---

# 661-Topshiriq: Ikki ko'rsatkich: Nollarni massiv oxiriga siljitish (Move Zeroes)

## Topshiriq sharti:
Nol bo'lmagan elementlar tartibini saqlagan holda barcha 0 larni massiv oxiriga o'tkazing.

## Yechim (Python kodi):
```python
def nollarni_surish(arr):
    yozish_idx = 0
    for i in range(len(arr)):
        if arr[i] != 0:
            arr[yozish_idx], arr[i] = arr[i], arr[yozish_idx]
            yozish_idx += 1
    return arr

massiv = [0, 1, 0, 3, 12]
print(nollarni_surish(massiv))
```

## Tushuntirish va Mantiq:
1. Qo'shimcha xotira O(1) ishlatgan holda 'in-place' tartiblash amalga oshiriladi.

## Ishlash natijasi:
```text
Chiqish: [1, 3, 12, 0, 0]
```

---

# 662-Topshiriq: Ikki ko'rsatkich: Palindrom satrni tekshirish

## Topshiriq sharti:
Satr chapdan ham, o'ngdan ham bir xil o'qilishini probel va tinish belgilarisiz tekshiring.

## Yechim (Python kodi):
```python
def palindrommi(s):
    toza = [c.lower() for c in s if c.isalnum()]
    chap, ong = 0, len(toza) - 1
    while chap < ong:
        if toza[chap] != toza[ong]:
            return False
        chap += 1
        ong -= 1
    return True

print("kiyik ->", palindrommi("kiyik"))
print("A man, a plan, a canal: Panama ->", palindrommi("A man, a plan, a canal: Panama"))
print("salom ->", palindrommi("salom"))
```

## Tushuntirish va Mantiq:
1. Ikki ko'rsatkich bilan chetlardan o'rtaga qarab taqqoslash amalga oshiriladi.

## Ishlash natijasi:
```text
Chiqish: kiyik -> True, A man, a plan, a canal: Panama -> True, salom -> False
```

---

# 663-Topshiriq: Siljuvchi darcha: K o'lchamli eng katta yig'indili qism-massiv

## Topshiriq sharti:
K uzunlikdagi ketma-ket elementlarning maksimal yig'indisini O(n) vaqtda hisoblang.

## Yechim (Python kodi):
```python
def max_sum_subarray(arr, k):
    if len(arr) < k: return 0
    oyna_yigindisi = sum(arr[:k])
    max_yigindi = oyna_yigindisi
    
    for i in range(k, len(arr)):
        oyna_yigindisi += arr[i] - arr[i - k]
        max_yigindi = max(max_yigindi, oyna_yigindisi)
        
    return max_yigindi

print(max_sum_subarray([2, 1, 5, 1, 3, 2], 3))
```

## Tushuntirish va Mantiq:
1. Darchani har safar qaytadan hisoblamasdan, yangi elementni qo'shib, eskisinigini ayirib siljitiladi.

## Ishlash natijasi:
```text
Chiqish: 9
```

---

# 664-Topshiriq: Siljuvchi darcha: Takrorlanmas eng uzun qism-satr

## Topshiriq sharti:
Satr ichida belgilar takrorlanmagan eng uzun qism-satr uzunligini toping.

## Yechim (Python kodi):
```python
def eng_uzun_unikal_satr(s):
    belgilar = {}
    chap = 0
    max_uzunlik = 0
    
    for ong, c in enumerate(s):
        if c in belgilar and belgilar[c] >= chap:
            chap = belgilar[c] + 1
        belgilar[c] = ong
        max_uzunlik = max(max_uzunlik, ong - chap + 1)
        
    return max_uzunlik

print(eng_uzun_unikal_satr("abcabcbb"))
print(eng_uzun_unikal_satr("bbbbb"))
print(eng_uzun_unikal_satr("pwwkew"))
```

## Tushuntirish va Mantiq:
1. Dinamik oyna (Dynamic Sliding Window) chap chegarasini takrorlangan belgining oxirgi indeksidan keyinga siljitadi.

## Ishlash natijasi:
```text
Chiqish: 3, 1, 3
```

---

# 665-Topshiriq: Kadane algoritmi: Maksimal qism-massiv yig'indisi (Maximum Subarray)

## Topshiriq sharti:
Manfiy va musbat sonlar qatnashgan massivda eng katta uzluksiz yig'indini O(n) da toping.

## Yechim (Python kodi):
```python
def max_subarray_kadane(arr):
    joriy_yigindi = max_yigindi = arr[0]
    for x in arr[1:]:
        joriy_yigindi = max(x, joriy_yigindi + x)
        max_yigindi = max(max_yigindi, joriy_yigindi)
    return max_yigindi

print(max_subarray_kadane([-2, 1, -3, 4, -1, 2, 1, -5, 4]))
```

## Tushuntirish va Mantiq:
1. Kadane algoritmi har qadamda yig'indini noldan boshlash yoki davom ettirishni optimal tanlaydi.

## Ishlash natijasi:
```text
Chiqish: 6
```

---

# 666-Topshiriq: Prefix Sum massivlari va O(1) oraliq yig'indisi

## Topshiriq sharti:
Qator oraliqlari [L, R] yig'indisini bir zumda O(1) vaqtda hisoblovchi sinf yarating.

## Yechim (Python kodi):
```python
class RangeSum:
    def __init__(self, arr):
        self.pref = [0] * (len(arr) + 1)
        for i in range(len(arr)):
            self.pref[i + 1] = self.pref[i] + arr[i]

    def yigindi(self, chap, ong):
        # [chap, ong] indekslari oraliq yig'indisi
        return self.pref[ong + 1] - self.pref[chap]

rs = RangeSum([3, 1, 4, 1, 5, 9, 2])
print("Oraliq [1, 4] yig'indisi:", rs.yigindi(1, 4))
print("Oraliq [0, 2] yig'indisi:", rs.yigindi(0, 2))
```

## Tushuntirish va Mantiq:
1. Prefix Sum massivlarida `pref[R+1] - pref[L]` ayirmasi oraliq yig'indisini tezkor hisoblaydi.

## Ishlash natijasi:
```text
Chiqish: Oraliq [1, 4] yig'indisi: 11, Oraliq [0, 2] yig'indisi: 8
```

---

# 667-Topshiriq: Ko'pchilik elementi (Majority Element: Boyer-Moore Voting)

## Topshiriq sharti:
Massivda n/2 martadan ko'p qatnashgan dominant elementni O(1) xotira va O(n) vaqtda aniqlang.

## Yechim (Python kodi):
```python
def majority_element(arr):
    nomzod = None
    hisob = 0
    for x in arr:
        if hisob == 0:
            nomzod = x
        hisob += 1 if x == nomzod else -1
    return nomzod

print("Ko'pchilik elementi:", majority_element([2, 2, 1, 1, 1, 2, 2]))
```

## Tushuntirish va Mantiq:
1. Boyer-Moore ovoz berish algoritmi tengsizliklarni bekor qilish hisobiga eng ko'p qatnashgan elementni topadi.

## Ishlash natijasi:
```text
Chiqish: Ko'pchilik elementi: 2
```

---

# 668-Topshiriq: Bir tomonlama bog'langan ro'yxat (Singly Linked List) Node klassi

## Topshiriq sharti:
Linked List tuguni (Node) va yangi element qo'shish metodlarini yarating.

## Yechim (Python kodi):
```python
class Tugun:
    def __init__(self, qiymat):
        self.qiymat = qiymat
        self.keyingi = None

class BoglanganRoyxat:
    def __init__(self):
        self.bosh = None

    def qoshish(self, qiymat):
        yangi = Tugun(qiymat)
        if not self.bosh:
            self.bosh = yangi
            return
        joriy = self.bosh
        while joriy.keyingi:
            joriy = joriy.keyingi
        joriy.keyingi = yangi

    def chop_et(self):
        elementlar = []
        joriy = self.bosh
        while joriy:
            elementlar.append(str(joriy.qiymat))
            joriy = joriy.keyingi
        return " -> ".join(elementlar) + " -> None"

royxat = BoglanganRoyxat()
royxat.qoshish(10)
royxat.qoshish(20)
royxat.qoshish(30)
print(royxat.chop_et())
```

## Tushuntirish va Mantiq:
1. Linked List xotirada ketma-ket joylashmaydi, balki ko'rsatkichlar (pointers) orqali ulanadi.

## Ishlash natijasi:
```text
Chiqish: 10 -> 20 -> 30 -> None
```

---

# 669-Topshiriq: Bog'langan ro'yxatni teskarisiga o'girish (Reverse Linked List)

## Topshiriq sharti:
Linked List ko'rsatkichlarini teskarisiga o'giruvchi O(n) vaqt va O(1) xotirali funksiya yozing.

## Yechim (Python kodi):
```python
def reverse_list(bosh):
    oldingi = None
    joriy = bosh
    while joriy:
        keyingi = joriy.keyingi
        joriy.keyingi = oldingi
        oldingi = joriy
        joriy = keyingi
    return oldingi

# Bog'lanish: 1 -> 2 -> 3
t1 = Tugun(1); t2 = Tugun(2); t3 = Tugun(3)
t1.keyingi = t2; t2.keyingi = t3

yangi_bosh = reverse_list(t1)
res = []
while yangi_bosh:
    res.append(str(yangi_bosh.qiymat))
    yangi_bosh = yangi_bosh.keyingi
print(" -> ".join(res))
```

## Tushuntirish va Mantiq:
1. `oldingi`, `joriy`, `keyingi` ko'rsatkichlar yordamida ro'yxat iterativ tarzda teskarilanadi.

## Ishlash natijasi:
```text
Chiqish: 3 -> 2 -> 1
```

---

# 670-Topshiriq: Linked List siklini aniqlash (Floyd's Tortoise and Hare)

## Topshiriq sharti:
Ro'yxat ichida aylanma sikl (loop) bor-yo'qligini sekin va tez yuguruvchi ko'rsatkichlar bilan aniqlang.

## Yechim (Python kodi):
```python
def sikl_bormi(bosh):
    sekin = tez = bosh
    while tez and tez.keyingi:
        sekin = sekin.keyingi
        tez = tez.keyingi.keyingi
        if sekin == tez:
            return True
    return False

n1 = Tugun(1); n2 = Tugun(2); n3 = Tugun(3)
n1.keyingi = n2; n2.keyingi = n3; n3.keyingi = n2 # 2 ga qaytuvchi sikl
print("Sikl bormi:", sikl_bormi(n1))
```

## Tushuntirish va Mantiq:
1. Floyd sikl algoritmi: agar sikl bo'lsa, 2 qadam tashlovchi tez ko'rsatkich albatta 1 qadam tashlovchi sekinga yetib oladi.

## Ishlash natijasi:
```text
Chiqish: Sikl bormi: True
```

---

# 671-Topshiriq: Ikki saralangan Linked Listni birlashtirish (Merge Two Sorted Lists)

## Topshiriq sharti:
Saralangan ikki ro'yxatni bitta saralangan ro'yxatga birlashtiring.

## Yechim (Python kodi):
```python
def merge_two_lists(l1, l2):
    dummy = Tugun(0)
    quyruq = dummy
    while l1 and l2:
        if l1.qiymat <= l2.qiymat:
            quyruq.keyingi = l1
            l1 = l1.keyingi
        else:
            quyruq.keyingi = l2
            l2 = l2.keyingi
        quyruq = quyruq.keyingi
    quyruq.keyingi = l1 or l2
    return dummy.keyingi

# 1 -> 3 va 2 -> 4
a1, a2 = Tugun(1), Tugun(3); a1.keyingi = a2
b1, b2 = Tugun(2), Tugun(4); b1.keyingi = b2
bir = merge_two_lists(a1, b1)
natija = []
while bir:
    natija.append(str(bir.qiymat))
    bir = bir.keyingi
print(" -> ".join(natija))
```

## Tushuntirish va Mantiq:
1. Dummy node (soxta tugun) boshlang'ich chekka holatlarni boshqarishni juda osonlashtiradi.

## Ishlash natijasi:
```text
Chiqish: 1 -> 2 -> 3 -> 4
```

---

# 672-Topshiriq: Stek (Stack LIFO) tuzilmasi klassi

## Topshiriq sharti:
Ro'yxat asosida push, pop, peek va is_empty amallarini bajaruvchi Stek klassini yarating.

## Yechim (Python kodi):
```python
class Stek:
    def __init__(self):
        self._ombor = []

    def push(self, qiymat):
        self._ombor.append(qiymat)

    def pop(self):
        if self.is_empty():
            raise IndexError("Stek bo'sh!")
        return self._ombor.pop()

    def peek(self):
        return self._ombor[-1] if not self.is_empty() else None

    def is_empty(self):
        return len(self._ombor) == 0

s = Stek()
s.push("birinchi")
s.push("ikkinchi")
print("Tepada:", s.peek())
print("O'chirildi:", s.pop())
```

## Tushuntirish va Mantiq:
1. Stek LIFO (Last In First Out — oxirgi kirgan birinchi chiqadi) tamoyilida ishlaydi.

## Ishlash natijasi:
```text
Chiqish: Tepada: ikkinchi, O'chirildi: ikkinchi
```

---

# 673-Topshiriq: Qavslar balansini tekshirish (Valid Parentheses)

## Topshiriq sharti:
Satrdagi '()', '{}', '[]' qavslar to'g'ri ochilib yopilganligini Stek yordamida tekshiring.

## Yechim (Python kodi):
```python
def qavslar_togrimi(s):
    stek = []
    juftlar = {')': '(', '}': '{', ']': '['}
    for belgi in s:
        if belgi in "({[":
            stek.append(belgi)
        elif belgi in ")}]":
            if not stek or stek[-1] != juftlar[belgi]:
                return False
            stek.pop()
    return len(stek) == 0

print("()[]{} ->", qavslar_togrimi("()[]{}"))
print("([)] ->", qavslar_togrimi("([)]"))
print("{[]} ->", qavslar_togrimi("{[]}"))
```

## Tushuntirish va Mantiq:
1. Har bir yopiluvchi qavs stek tepasidagi mos ochiluvchi qavs bilan juftlashishi shart.

## Ishlash natijasi:
```text
Chiqish: ()[]{} -> True, ([)] -> False, {[]} -> True
```

---

# 674-Topshiriq: Postfix ifodani hisoblash (Reverse Polish Notation)

## Topshiriq sharti:
Teskari Polsha yozuvidagi matematik ifodani Stek bilan hisoblang (masalan: '2 1 + 3 *' = 9).

## Yechim (Python kodi):
```python
def hisobla_rpn(belgilar):
    stek = []
    amallar = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: int(a / b)
    }
    for b in belgilar:
        if b in amallar:
            o2 = stek.pop()
            o1 = stek.pop()
            stek.append(amallar[b](o1, o2))
        else:
            stek.append(int(b))
    return stek[0]

print("Natija:", hisobla_rpn(["2", "1", "+", "3", "*"]))
print("Natija 2:", hisobla_rpn(["4", "13", "5", "/", "+"]))
```

## Tushuntirish va Mantiq:
1. Kompyuterlar va kompilyatorlar arifmetik ifodalarni aynan RPN stek orqali hisoblaydi.

## Ishlash natijasi:
```text
Chiqish: Natija: 9, Natija 2: 6
```

---

# 675-Topshiriq: Min Stek (MinStack — O(1) vaqtda minimal element)

## Topshiriq sharti:
get_min() amalini doimiy O(1) vaqtda qaytaruvchi maxsus stek yarating.

## Yechim (Python kodi):
```python
class MinStack:
    def __init__(self):
        self.asosiy = []
        self.min_stek = []

    def push(self, val):
        self.asosiy.append(val)
        if not self.min_stek or val <= self.min_stek[-1]:
            self.min_stek.append(val)

    def pop(self):
        val = self.asosiy.pop()
        if val == self.min_stek[-1]:
            self.min_stek.pop()
        return val

    def get_min(self):
        return self.min_stek[-1]

ms = MinStack()
ms.push(-2); ms.push(0); ms.push(-3)
print("Min:", ms.get_min())
ms.pop()
print("Pop dan keyin min:", ms.get_min())
```

## Tushuntirish va Mantiq:
1. Yordamchi stek har bir darajadagi eng kichik qiymatni kuzatib boradi.

## Ishlash natijasi:
```text
Chiqish: Min: -3, Pop dan keyin min: -2
```

---

# 676-Topshiriq: Navbat (Queue FIFO: collections.deque)

## Topshiriq sharti:
Ikki tomonlama tezkor navbat (deque) yordamida FIFO mexanizmini yarating.

## Yechim (Python kodi):
```python
from collections import deque

navbat = deque()
navbat.append("1-mijoz")
navbat.append("2-mijoz")
navbat.append("3-mijoz")

print("Xizmat ko'rsatildi:", navbat.popleft())
print("Keyingi:", navbat[0])
print("Qolganlar:", list(navbat))
```

## Tushuntirish va Mantiq:
1. `deque.popleft()` O(1) vaqt oladi, oddiy `list.pop(0)` esa O(n) vaqt talab qiladi.

## Ishlash natijasi:
```text
Chiqish: Xizmat ko'rsatildi: 1-mijoz, Keyingi: 2-mijoz, Qolganlar: ['2-mijoz', '3-mijoz']
```

---

# 677-Topshiriq: Aylana navbat (Circular Queue)

## Topshiriq sharti:
Ruxsat etilgan qat'iy sig'imli aylana bufer tuzilmasini yarating.

## Yechim (Python kodi):
```python
class CircularQueue:
    def __init__(self, k):
        self.ombor = [None] * k
        self.k = k
        self.bosh = 0
        self.soni = 0

    def enQueue(self, val):
        if self.soni == self.k: return False
        idx = (self.bosh + self.soni) % self.k
        self.ombor[idx] = val
        self.soni += 1
        return True

    def deQueue(self):
        if self.soni == 0: return False
        self.bosh = (self.bosh + 1) % self.k
        self.soni -= 1
        return True

cq = CircularQueue(3)
cq.enQueue(10); cq.enQueue(20); cq.enQueue(30)
print("To'ldi:", not cq.enQueue(40))
cq.deQueue()
print("Yangi element kirdi:", cq.enQueue(40))
```

## Tushuntirish va Mantiq:
1. Aylana navbat audio drayverlar, tarmoq kartalari va buferlash tizimlarida xotirani qayta sarflamasdan ishlatiladi.

## Ishlash natijasi:
```text
Chiqish: To'ldi: True, Yangi element kirdi: True
```

---

# 678-Topshiriq: Monotonik Stek: Keyingi eng katta element (Next Greater Element)

## Topshiriq sharti:
Har bir element uchun undan keyin keluvchi birinchi eng katta qiymatni O(n) da toping.

## Yechim (Python kodi):
```python
def next_greater_element(arr):
    natija = [-1] * len(arr)
    stek = [] # Indekslarni saqlaydi
    for i, x in enumerate(arr):
        while stek and arr[stek[-1]] < x:
            idx = stek.pop()
            natija[idx] = x
        stek.append(i)
    return natija

print(next_greater_element([4, 5, 2, 25]))
```

## Tushuntirish va Mantiq:
1. Monotonik stek elementlar kamayish tartibida bo'lishini ta'minlaydi va har bir son uchun bir martadan stekka kiradi.

## Ishlash natijasi:
```text
Chiqish: [5, 25, 25, -1]
```

---

# 679-Topshiriq: Massivni K qadamga o'ngga aylantirish (Rotate Array)

## Topshiriq sharti:
Massivni O(1) qo'shimcha xotira bilan 3 marta teskarilash (Reverse) orqali aylantiring.

## Yechim (Python kodi):
```python
def rotate_array(nums, k):
    k %= len(nums)
    def reverse(i, j):
        while i < j:
            nums[i], nums[j] = nums[j], nums[i]
            i += 1; j -= 1
            
    reverse(0, len(nums) - 1)
    reverse(0, k - 1)
    reverse(k, len(nums) - 1)
    return nums

print(rotate_array([1, 2, 3, 4, 5, 6, 7], 3))
```

## Tushuntirish va Mantiq:
1. Butun massivni, keyin dastlabki k tani, keyin qolgan qismini teskarilash orqali massiv aylantiriladi.

## Ishlash natijasi:
```text
Chiqish: [5, 6, 7, 1, 2, 3, 4]
```

---

# 680-Topshiriq: Oraliqlar birlashmasi (Merge Intervals)

## Topshiriq sharti:
Ustma-ust tushgan vaqt yoki raqamlar oraliqlarini bitta yaxlit oraliqqa birlashtiring.

## Yechim (Python kodi):
```python
def merge_intervals(oraliqlar):
    oraliqlar.sort(key=lambda x: x[0])
    birlashgan = [oraliqlar[0]]
    for joriy in oraliqlar[1:]:
        oxirgi = birlashgan[-1]
        if joriy[0] <= oxirgi[1]:
            oxirgi[1] = max(oxirgi[1], joriy[1])
        else:
            birlashgan.append(joriy)
    return birlashgan

print(merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]))
```

## Tushuntirish va Mantiq:
1. Oraliqlarni boshlanish vaqti bo'yicha saralab, ularning kesishishini tekshirish eng optimal yechimdir.

## Ishlash natijasi:
```text
Chiqish: [[1, 6], [8, 10], [15, 18]]
```

---

# 681-Topshiriq: Matritsani soat mili bo'yicha 90 gradusga burish (Rotate Matrix)

## Topshiriq sharti:
NxN matritsani qo'shimcha xotirasiz transponirlash va teskarilash bilan 90 gradusga burish.

## Yechim (Python kodi):
```python
def rotate_matrix(m):
    n = len(m)
    # Transponirlash
    for i in range(n):
        for j in range(i, n):
            m[i][j], m[j][i] = m[j][i], m[i][j]
    # Har bir qatorni teskarilash
    for row in m:
        row.reverse()
    return m

matritsa = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print("Burilgan matritsa:", rotate_matrix(matritsa))
```

## Tushuntirish va Mantiq:
1. Matritsani transponirlab, so'ng qatorlarini teskarisiga o'girish uni 90° o'ngga aylantiradi.

## Ishlash natijasi:
```text
Chiqish: Burilgan matritsa: [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
```

---

# 682-Topshiriq: Spiral matritsani aylanib chiqish (Spiral Order)

## Topshiriq sharti:
MxN o'lchamli to'rtburchak matritsa elementlarini spiral shaklda ro'yxatga to'plang.

## Yechim (Python kodi):
```python
def spiral_order(matrix):
    res = []
    if not matrix: return res
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    
    while top <= bottom and left <= right:
        for j in range(left, right + 1): res.append(matrix[top][j])
        top += 1
        for i in range(top, bottom + 1): res.append(matrix[i][right])
        right -= 1
        if top <= bottom:
            for j in range(right, left - 1, -1): res.append(matrix[bottom][j])
            bottom -= 1
        if left <= right:
            for i in range(bottom, top - 1, -1): res.append(matrix[i][left])
            left += 1
    return res

m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(spiral_order(m))
```

## Tushuntirish va Mantiq:
1. To'rt chegara (top, bottom, left, right) ni bosqichma-bosqich qisqartirib borish spiral marshrutini hosil qiladi.

## Ishlash natijasi:
```text
Chiqish: [1, 2, 3, 6, 9, 8, 7, 4, 5]
```

---

# 683-Topshiriq: Suv saqlash sig'imi (Trapping Rain Water)

## Topshiriq sharti:
Ustunlar orasida to'planadigan yomg'ir suvi hajmini ikki ko'rsatkich bilan O(n) da hisoblang.

## Yechim (Python kodi):
```python
def trap_water(balandlik):
    chap, ong = 0, len(balandlik) - 1
    chap_max = ong_max = suv = 0
    while chap < ong:
        if balandlik[chap] < balandlik[ong]:
            if balandlik[chap] >= chap_max:
                chap_max = balandlik[chap]
            else:
                suv += chap_max - balandlik[chap]
            chap += 1
        else:
            if balandlik[ong] >= ong_max:
                ong_max = balandlik[ong]
            else:
                suv += ong_max - balandlik[ong]
            ong -= 1
    return suv

print("Suv hajmi:", trap_water([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))
```

## Tushuntirish va Mantiq:
1. Har bir ustundagi suv miqdori uning chap va o'ng tomonidagi maksimal balandliklarning kichigiga bog'liq.

## Ishlash natijasi:
```text
Chiqish: Suv hajmi: 6
```

---

# 684-Topshiriq: Eng katta to'g'ri to'rtburchak maydoni (Largest Rectangle in Histogram)

## Topshiriq sharti:
Gistogramma ustunlari ichidagi eng katta maydonni monotonik stek bilan O(n) da toping.

## Yechim (Python kodi):
```python
def largest_rectangle(heights):
    heights.append(0)
    stek = [-1]
    max_maydon = 0
    for i, h in enumerate(heights):
        while heights[stek[-1]] > h:
            balandlik = heights[stek.pop()]
            kenglik = i - stek[-1] - 1
            max_maydon = max(max_maydon, balandlik * kenglik)
        stek.append(i)
    return max_maydon

print("Maksimal maydon:", largest_rectangle([2, 1, 5, 6, 2, 3]))
```

## Tushuntirish va Mantiq:
1. Stek orqali har bir ustun qaysi chegaralargacha cho'zilishi mumkinligi O(n) vaqtda hisoblanadi.

## Ishlash natijasi:
```text
Chiqish: Maksimal maydon: 10
```

---

# 685-Topshiriq: Ikki tomonlama bog'langan ro'yxat (Doubly Linked List)

## Topshiriq sharti:
Oldingi va keyingi tugunlarga ko'rsatkichi bor Doubly Node klassi tuzilmasi.

## Yechim (Python kodi):
```python
class DNode:
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None

n1 = DNode(10)
n2 = DNode(20)
n1.next = n2
n2.prev = n1

print(f"Olg'a: {n1.val} -> {n1.next.val}")
print(f"Orqaga: {n2.val} -> {n2.prev.val}")
```

## Tushuntirish va Mantiq:
1. Ikki tomonlama bog'langan ro'yxat LRU Cache va murakkab operatsion tizim navbatlarining asosidir.

## Ishlash natijasi:
```text
Chiqish: Olg'a: 10 -> 20, Orqaga: 20 -> 10
```

---

# 686-Topshiriq: LRU Kesh (Least Recently Used Cache) tuzilmasi

## Topshiriq sharti:
Eng kam ishlatilgan elementlarni avtomatik o'chiruvchi LRU keshini OrderedDict orqali yarating.

## Yechim (Python kodi):
```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.ombor = OrderedDict()
        self.cap = capacity

    def get(self, key):
        if key not in self.ombor: return -1
        self.ombor.move_to_end(key)
        return self.ombor[key]

    def put(self, key, value):
        if key in self.ombor:
            self.ombor.move_to_end(key)
        self.ombor[key] = value
        if len(self.ombor) > self.cap:
            self.ombor.popitem(last=False)

lru = LRUCache(2)
lru.put(1, 100); lru.put(2, 200)
print("1 olindi:", lru.get(1))
lru.put(3, 300) # 2 o'chiriladi
print("2 mavjudmi:", lru.get(2))
```

## Tushuntirish va Mantiq:
1. O(1) o'qish va yozish imkoniyatiga ega bo'lgan LRU Kesh xotirani boshqarishda standartdir.

## Ishlash natijasi:
```text
Chiqish: 1 olindi: 100, 2 mavjudmi: -1
```

---

# 687-Topshiriq: LFU Kesh (Least Frequently Used) tushunchasi

## Topshiriq sharti:
Foydalanish chastotasi eng past bo'lgan elementlarni chiqaruvchi kesh arxitekturasi.

## Yechim (Python kodi):
```python
class LFUSimulyatsiya:
    def __init__(self, cap):
        self.cap = cap
        self.chastota = {}

    def foydalanildi(self, kalit):
        self.chastota[kalit] = self.chastota.get(kalit, 0) + 1

    def eng_kam(self):
        return min(self.chastota.items(), key=lambda x: x[1])[0]

lfu = LFUSimulyatsiya(3)
lfu.foydalanildi("A"); lfu.foydalanildi("A"); lfu.foydalanildi("B")
print("Eng kam foydalanilgan:", lfu.eng_kam())
```

## Tushuntirish va Mantiq:
1. LFU algoritmi uzoq muddatli ommaboplikni saqlab qoladi.

## Ishlash natijasi:
```text
Chiqish: Eng kam foydalanilgan: B
```

---

# 688-Topshiriq: Bit manipulatsiyasi: Yagona yolg'iz elementni topish (Single Number: XOR)

## Topshiriq sharti:
Massivda barcha sonlar juft bo'lib, faqat bittasi toq bo'lsa, uni O(1) xotirada XOR bilan toping.

## Yechim (Python kodi):
```python
def single_number(nums):
    yolgiz = 0
    for x in nums:
        yolgiz ^= x
    return yolgiz

print("Yolg'iz son:", single_number([4, 1, 2, 1, 2]))
```

## Tushuntirish va Mantiq:
1. `a ^ a = 0` va `a ^ 0 = a`. Barcha juft sonlar bir-birini yo'qotadi va faqat bitta yolg'iz qoladi.

## Ishlash natijasi:
```text
Chiqish: Yolg'iz son: 4
```

---

# 689-Topshiriq: Bit manipulatsiyasi: 2 ning darajasi ekanligini tekshirish

## Topshiriq sharti:
Son 2 ning darajasi (1, 2, 4, 8, 16...) ekanligini birgina `n & (n - 1)` biti amali bilan tekshiring.

## Yechim (Python kodi):
```python
def ikkining_darajasimi(n):
    return n > 0 and (n & (n - 1)) == 0

print("16 ->", ikkining_darajasimi(16))
print("18 ->", ikkining_darajasimi(18))
print("1 ->", ikkining_darajasimi(1))
```

## Tushuntirish va Mantiq:
1. 2 ning darajasidagi binar son faqat bitta '1' dan iborat. `n & (n - 1)` eng quyi 1 bitni o'chiradi.

## Ishlash natijasi:
```text
Chiqish: 16 -> True, 18 -> False, 1 -> True
```

---

# 690-Topshiriq: Bitlar sonini sanash (Hamming Weight / Population Count)

## Topshiriq sharti:
Butun sonning ikkilik ifodasidagi '1' lar sonini hisoblang.

## Yechim (Python kodi):
```python
def count_bits(n):
    hisob = 0
    while n:
        n &= (n - 1)
        hisob += 1
    return hisob

print("11 (1011b) bitlari soni:", count_bits(11))
print("128 (10000000b) bitlari soni:", count_bits(128))
```

## Tushuntirish va Mantiq:
1. Brian Kernighan algoritmi har siklda 1 ta '1' bitni yo'qotadi va amallar soni faqat mavjud birlar soniga teng bo'ladi.

## Ishlash natijasi:
```text
Chiqish: 11 (1011b) bitlari soni: 3, 128 (10000000b) bitlari soni: 1
```

---

# 691-Topshiriq: Hamming masofasi (Hamming Distance)

## Topshiriq sharti:
Ikki butun sonning ikkilik ko'rinishida farq qiluvchi bitlar sonini hisoblang.

## Yechim (Python kodi):
```python
def hamming_distance(x, y):
    xor = x ^ y
    hisob = 0
    while xor:
        xor &= (xor - 1)
        hisob += 1
    return hisob

print("1 va 4 orasidagi masofa:", hamming_distance(1, 4))
```

## Tushuntirish va Mantiq:
1. Kriptografiya va xatoliklarni tuzatish kodlarida (ECC) Hamming masofasi kalit ahamiyatga ega.

## Ishlash natijasi:
```text
Chiqish: 1 va 4 orasidagi masofa: 2
```

---

# 692-Topshiriq: Matritsada ikkilik qidiruv (Search a 2D Matrix)

## Topshiriq sharti:
Har bir qatori va ustuni saralangan matritsadan sonni O(log(m*n)) vaqtda toping.

## Yechim (Python kodi):
```python
def search_matrix(m, target):
    if not m or not m[0]: return False
    rows, cols = len(m), len(m[0])
    chap, ong = 0, rows * cols - 1
    while chap <= ong:
        orta = (chap + ong) // 2
        r, c = divmod(orta, cols)
        if m[r][c] == target:
            return True
        elif m[r][c] < target:
            chap = orta + 1
        else:
            ong = orta - 1
    return False

mat = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
print("3 mavjudmi:", search_matrix(mat, 3))
print("13 mavjudmi:", search_matrix(mat, 13))
```

## Tushuntirish va Mantiq:
1. 2D matritsani tekis 1D massiv sifatida tasavvur qilib ikkilik qidiruv qo'llaniladi.

## Ishlash natijasi:
```text
Chiqish: 3 mavjudmi: True, 13 mavjudmi: False
```

---

# 693-Topshiriq: Aylantirilgan saralangan massivda qidiruv (Search in Rotated Sorted Array)

## Topshiriq sharti:
Aylantirilgan massivda (masalan, [4, 5, 6, 7, 0, 1, 2]) nishonni O(log n) da toping.

## Yechim (Python kodi):
```python
def search_rotated(nums, target):
    l, r = 0, len(nums) - 1
    while l <= r:
        mid = (l + r) // 2
        if nums[mid] == target: return mid
        # Chap qism saralanganmi?
        if nums[l] <= nums[mid]:
            if nums[l] <= target < nums[mid]:
                r = mid - 1
            else:
                l = mid + 1
        else:
            if nums[mid] < target <= nums[r]:
                l = mid + 1
            else:
                r = mid - 1
    return -1

print("0 ning indeksi:", search_rotated([4, 5, 6, 7, 0, 1, 2], 0))
```

## Tushuntirish va Mantiq:
1. Kamida bir yarmi har doim qat'iy saralangan bo'ladi; qidiruv aynan shu yarimga qarab yo'naltiriladi.

## Ishlash natijasi:
```text
Chiqish: 0 ning indeksi: 4
```

---

# 694-Topshiriq: Kvadrat ildizni butun qismini ikkilik qidiruv bilan topish (int sqrt)

## Topshiriq sharti:
math kutubxonasiz sonning butun kvadrat ildizini O(log n) da toping.

## Yechim (Python kodi):
```python
def my_sqrt(x):
    if x < 2: return x
    chap, ong = 1, x // 2
    natija = 1
    while chap <= ong:
        orta = (chap + ong) // 2
        if orta * orta <= x:
            natija = orta
            chap = orta + 1
        else:
            ong = orta - 1
    return natija

print("8 ildizi:", my_sqrt(8))
print("16 ildizi:", my_sqrt(16))
```

## Tushuntirish va Mantiq:
1. Ikkilik qidiruv nafaqat massivlarda, balki monotonik matematik funksiyalarda ham qo'llaniladi.

## Ishlash natijasi:
```text
Chiqish: 8 ildizi: 2, 16 ildizi: 4
```

---

# 695-Topshiriq: Tezkor darajaga ko'tarish (Binary Exponentiation: Pow(x, n))

## Topshiriq sharti:
Sonni n-darajaga O(log n) qadamda ko'taruvchi rekursiv/iterativ algoritm.

## Yechim (Python kodi):
```python
def my_pow(x, n):
    if n < 0:
        x = 1 / x
        n = -n
    natija = 1
    joriy_kop = x
    while n > 0:
        if n % 2 == 1:
            natija *= joriy_kop
        joriy_kop *= joriy_kop
        n //= 2
    return natija

print("2^10 =", my_pow(2, 10))
print("2^-2 =", my_pow(2, -2))
```

## Tushuntirish va Mantiq:
1. Darajani ikkiga bo'lish orqali amallar soni 1000 dan 10 taga qisqaradi.

## Ishlash natijasi:
```text
Chiqish: 2^10 = 1024, 2^-2 = 0.25
```

---

# 696-Topshiriq: Eratosfen g'alviri (Sieve of Eratosthenes) — Tub sonlar

## Topshiriq sharti:
N gacha bo'lgan barcha tub sonlarni O(n log log n) da topuvchi klassik g'alvir.

## Yechim (Python kodi):
```python
def tub_sonlar_galviri(n):
    galvir = [True] * (n + 1)
    galvir[0] = galvir[1] = False
    for p in range(2, int(n**0.5) + 1):
        if galvir[p]:
            for i in range(p * p, n + 1, p):
                galvir[i] = False
    return [i for i, tub in enumerate(galvir) if tub]

print("30 gacha tub sonlar:", tub_sonlar_galviri(30))
```

## Tushuntirish va Mantiq:
1. Har bir tub sonning karralilarini chizib tashlash orqali eng samarali tub sonlar ro'yxati olinadi.

## Ishlash natijasi:
```text
Chiqish: 30 gacha tub sonlar: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
```

---

# 697-Topshiriq: EKUB va EKUK (Evklid algoritmi)

## Topshiriq sharti:
Eng katta umumiy bo'luvchi (EKUB) va eng kichik umumiy karrali (EKUK) ni topish.

## Yechim (Python kodi):
```python
def ekub(a, b):
    while b:
        a, b = b, a % b
    return a

def ekuk(a, b):
    return (a * b) // ekub(a, b)

print("EKUB(48, 18):", ekub(48, 18))
print("EKUK(48, 18):", ekuk(48, 18))
```

## Tushuntirish va Mantiq:
1. Evklid algoritmi qoldiqli bo'lish orqali logarifmik qadamda javob topadi.

## Ishlash natijasi:
```text
Chiqish: EKUB(48, 18): 6, EKUK(48, 18): 144
```

---

# 698-Topshiriq: Massivdagi K-chi eng katta element (QuickSelect)

## Topshiriq sharti:
Massivni to'liq saralamasdan o'rtacha O(n) vaqtda K-chi eng katta elementni toping.

## Yechim (Python kodi):
```python
import random

def quick_select(nums, k):
    pivot = random.choice(nums)
    kichik = [x for x in nums if x > pivot] # Katta elementlar
    teng = [x for x in nums if x == pivot]
    katta = [x for x in nums if x < pivot]
    
    if k <= len(kichik):
        return quick_select(kichik, k)
    elif k <= len(kichik) + len(teng):
        return pivot
    else:
        return quick_select(katta, k - len(kichik) - len(teng))

print("2-eng katta element:", quick_select([3, 2, 1, 5, 6, 4], 2))
```

## Tushuntirish va Mantiq:
1. QuickSelect faqat kerakli qismga chuqurlashadi va umumiy saralashdan (O(n log n)) tezroq ishlaydi.

## Ishlash natijasi:
```text
Chiqish: 2-eng katta element: 5
```

---

# 699-Topshiriq: Uchta son yig'indisi (3Sum) nolga teng bo'lgan uchliklar

## Topshiriq sharti:
Massivdan a + b + c = 0 bo'lgan barcha noyob uchliklarni O(n^2) da toping.

## Yechim (Python kodi):
```python
def three_sum(nums):
    nums.sort()
    natijalar = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]: continue
        l, r = i + 1, len(nums) - 1
        while l < r:
            jami = nums[i] + nums[l] + nums[r]
            if jami == 0:
                natijalar.append([nums[i], nums[l], nums[r]])
                while l < r and nums[l] == nums[l + 1]: l += 1
                while l < r and nums[r] == nums[r - 1]: r -= 1
                l += 1; r -= 1
            elif jami < 0:
                l += 1
            else:
                r -= 1
    return natijalar

print(three_sum([-1, 0, 1, 2, -1, -4]))
```

## Tushuntirish va Mantiq:
1. Saralash va ikki ko'rsatkich texnikasini birlashtirish orqali O(n^3) lik brute-force O(n^2) ga tushiriladi.

## Ishlash natijasi:
```text
Chiqish: [[-1, -1, 2], [-1, 0, 1]]
```

---

# 700-Topshiriq: Kompakt Binar Qidiruv Daraxti (Mini BST)

## Topshiriq sharti:
Qidiruv, qo'shish va tartiblangan (in-order) chiqarish amallarini o'z ichiga olgan sodda BST yarating.

## Yechim (Python kodi):
```python
class BSTNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

class MiniBST:
    def __init__(self):
        self.ildiz = None

    def insert(self, val):
        if not self.ildiz:
            self.ildiz = BSTNode(val)
        else:
            self._insert(self.ildiz, val)

    def _insert(self, node, val):
        if val < node.val:
            if not node.left: node.left = BSTNode(val)
            else: self._insert(node.left, val)
        else:
            if not node.right: node.right = BSTNode(val)
            else: self._insert(node.right, val)

    def in_order(self, node):
        return self.in_order(node.left) + [node.val] + self.in_order(node.right) if node else []

bst = MiniBST()
for x in [50, 30, 70, 20, 40, 60, 80]:
    bst.insert(x)

print("BST In-Order saralangan tartibi:", bst.in_order(bst.ildiz))
```

## Tushuntirish va Mantiq:
1. Binar qidiruv daraxtida har qanday chap tugun kichik, o'ng tugun esa katta bo'ladi. In-order aylanib chiqish avtomatik saralangan tartibni beradi.

## Ishlash natijasi:
```text
Chiqish: BST In-Order saralangan tartibi: [20, 30, 40, 50, 60, 70, 80]
```

---

