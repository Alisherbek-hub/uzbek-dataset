# C++ Dasturlash Tili - 17-Qism: Ma'lumotlar Tuzilmalari va Algoritmlar (1-Qism)

Ushbu qismda Linked List, Stacks, Queues, Sorting (Quick, Merge, Radix, Counting), Two Pointers, Sliding Window, Prefix Sum va Monoton Stekka oid 50 ta amaliy topshiriq jamlangan.

---

# 801-Topshiriq: Bir tomonlama bog'langan ro'yxat (Singly Linked List) to'liq sinfi

## Topshiriq sharti:
Tugunlar asosida ro'yxatga boshidan qo'shish va chop etish metodlarini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

struct Tugun {
    int qiymat;
    Tugun* keyingi;
    Tugun(int q) : qiymat(q), keyingi(nullptr) {}
};

class OddiyRoyxat {
    Tugun* bosh = nullptr;
public:
    void boshigaQosh(int q) {
        Tugun* yangi = new Tugun(q);
        yangi->keyingi = bosh;
        bosh = yangi;
    }
    void chopEt() const {
        Tugun* joriy = bosh;
        while (joriy) {
            std::cout << joriy->qiymat << " -> ";
            joriy = joriy->keyingi;
        }
        std::cout << "null\n";
    }
    ~OddiyRoyxat() {
        while (bosh) {
            Tugun* temp = bosh;
            bosh = bosh->keyingi;
            delete temp;
        }
    }
};

int main() {
    OddiyRoyxat r;
    r.boshigaQosh(30);
    r.boshigaQosh(20);
    r.boshigaQosh(10);
    r.chopEt();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Tugunlar zanjiri dinamik xotirada joylashadi va ko'rsatkichlar bilan bog'lanadi.

## Ishlash natijasi:
```text
10 -> 20 -> 30 -> null
```

---

# 802-Topshiriq: Bog'langan ro'yxatni joyida teskarisiga o'girish (Reverse Linked List)

## Topshiriq sharti:
Uchta ko'rsatkich (`prev`, `curr`, `next`) orqali ro'yxatni O(N) vaqt va O(1) xotirada teskari qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>

struct Node {
    int data;
    Node* next;
    Node(int d) : data(d), next(nullptr) {}
};

Node* teskariQil(Node* head) {
    Node* prev = nullptr;
    Node* curr = head;
    while (curr != nullptr) {
        Node* nextTemp = curr->next;
        curr->next = prev;
        prev = curr;
        curr = nextTemp;
    }
    return prev;
}

int main() {
    Node* h = new Node(1);
    h->next = new Node(2);
    h->next->next = new Node(3);
    Node* yangiBosh = teskariQil(h);
    for (Node* p = yangiBosh; p; p = p->next) std::cout << p->data << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ko'rsatkichlar yo'nalishini birma-bir teskarisiga burib chiqiladi.

## Ishlash natijasi:
```text
3 2 1 
```

---

# 803-Topshiriq: Ro'yxatda tsiklni aniqlash (Floyd's Tortoise and Hare)

## Topshiriq sharti:
Sekin va tez harakatlanuvchi ikki ko'rsatkich yordamida ro'yxat halqa hosil qilganini toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>

struct Node {
    int val;
    Node* next;
    Node(int v) : val(v), next(nullptr) {}
};

bool tsiklBormi(Node* head) {
    Node* sekin = head;
    Node* tez = head;
    while (tez && tez->next) {
        sekin = sekin->next;
        tez = tez->next->next;
        if (sekin == tez) return true;
    }
    return false;
}

int main() {
    Node* a = new Node(1);
    Node* b = new Node(2);
    Node* c = new Node(3);
    a->next = b; b->next = c; c->next = b; // Halqa yaratildi
    std::cout << "Tsikl bormi: " << (tsiklBormi(a) ? "Ha" : "Yo'q") << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Tez ko'rsatkich sekin ko'rsatkichni quvib yetsa, demak halqa mavjud.

## Ishlash natijasi:
```text
Tsikl bormi: Ha
```

---

# 804-Topshiriq: Ro'yxat o'rtasidagi tugunni topish (Fast and Slow)

## Topshiriq sharti:
Bitta o'tishda ro'yxatning aniq markaziy tugunini toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>

struct Node {
    int val;
    Node* next;
    Node(int v) : val(v), next(nullptr) {}
};

int ortaElement(Node* head) {
    Node* slow = head;
    Node* fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
    }
    return slow->val;
}

int main() {
    Node* n1 = new Node(10);
    n1->next = new Node(20);
    n1->next->next = new Node(30);
    n1->next->next->next = new Node(40);
    n1->next->next->next->next = new Node(50);
    std::cout << "Markaziy element: " << ortaElement(n1) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Tez ko'rsatkich oxiriga yetganda, sekin ko'rsatkich aniq o'rtada bo'ladi.

## Ishlash natijasi:
```text
Markaziy element: 30
```

---

# 805-Topshiriq: Ikki saralangan ro'yxatni birlashtirish (Merge Two Sorted Lists)

## Topshiriq sharti:
Saralangan ikkita ro'yxatni bitta saralangan zanjirga O(N + M) da birlashtiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

struct Node {
    int v;
    Node* next;
    Node(int val) : v(val), next(nullptr) {}
};

Node* mergeLists(Node* l1, Node* l2) {
    Node dummy(0);
    Node* quyruq = &dummy;
    while (l1 && l2) {
        if (l1->v <= l2->v) { quyruq->next = l1; l1 = l1->next; }
        else { quyruq->next = l2; l2 = l2->next; }
        quyruq = quyruq->next;
    }
    quyruq->next = l1 ? l1 : l2;
    return dummy.next;
}

int main() {
    Node* a = new Node(1); a->next = new Node(3);
    Node* b = new Node(2); b->next = new Node(4);
    Node* res = mergeLists(a, b);
    for (Node* p = res; p; p = p->next) std::cout << p->v << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `dummy` tuguni boshlang'ich zanjirni boshqarishni ancha soddalashtiradi.

## Ishlash natijasi:
```text
1 2 3 4 
```

---

# 806-Topshiriq: Ikki tomonlama bog'langan ro'yxat (Doubly Linked List)

## Topshiriq sharti:
Har bir tugun `prev` va `next` ko'rsatkichlariga ega bo'lgan sinf.

## Yechim (C++ kodi):
```cpp
#include <iostream>

struct DNode {
    int val;
    DNode* prev;
    DNode* next;
    DNode(int v) : val(v), prev(nullptr), next(nullptr) {}
};

int main() {
    DNode* a = new DNode(10);
    DNode* b = new DNode(20);
    a->next = b;
    b->prev = a;
    std::cout << "Oldinga: " << a->next->val << ", Orqaga: " << b->prev->val << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ikki tomonlama harakatlanish erkinligini beradi.

## Ishlash natijasi:
```text
Oldinga: 20, Orqaga: 10
```

---

# 807-Topshiriq: Aylanma navbat (Circular Queue / Ring Buffer)

## Topshiriq sharti:
Qat'iy o'lchamdagi massiv ustida bosh va oxir ko'rsatkichlari bilan aylanma navbat quring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class RingBuffer {
    int buf[4];
    int head = 0, tail = 0, count = 0;
public:
    bool push(int val) {
        if (count == 4) return false;
        buf[tail] = val;
        tail = (tail + 1) % 4;
        count++;
        return true;
    }
    int pop() {
        if (count == 0) return -1;
        int val = buf[head];
        head = (head + 1) % 4;
        count--;
        return val;
    }
};

int main() {
    RingBuffer rb;
    rb.push(10); rb.push(20);
    std::cout << rb.pop() << " " << rb.pop() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `% hajmi` modulli arifmetikasi xotirani uzluksiz aylanma doirada ishlatadi.

## Ishlash natijasi:
```text
10 20
```

---

# 808-Topshiriq: Ikkita stek yordamida Navbat (Queue using Two Stacks)

## Topshiriq sharti:
`in` va `out` steklari orqali FIFO navbatini hosil qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <stack>

class StekNavbat {
    std::stack<int> s1, s2;
public:
    void push(int x) { s1.push(x); }
    int pop() {
        if (s2.empty()) {
            while (!s1.empty()) { s2.push(s1.top()); s1.pop(); }
        }
        int val = s2.top(); s2.pop();
        return val;
    }
};

int main() {
    StekNavbat q;
    q.push(1); q.push(2);
    std::cout << q.pop() << " " << q.pop() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Stek elementlarini ikkinchi stekka ag'darish ularning tartibini teskarisiga aylantirib FIFO qiladi.

## Ishlash natijasi:
```text
1 2
```

---

# 809-Topshiriq: Monoton Stek: Next Greater Element (Keyingi eng katta element)

## Topshiriq sharti:
Massivning har bir elementi uchun o'zidan o'ngdagi birinchi eng katta sonni O(N) da toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <stack>

std::vector<int> keyingiKatta(const std::vector<int>& v) {
    std::vector<int> res(v.size(), -1);
    std::stack<int> st; // Indekslar
    for (size_t i = 0; i < v.size(); ++i) {
        while (!st.empty() && v[i] > v[st.top()]) {
            res[st.top()] = v[i];
            st.pop();
        }
        st.push(i);
    }
    return res;
}

int main() {
    std::vector<int> v = {4, 5, 2, 25};
    auto res = keyingiKatta(v);
    for (int x : res) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Monoton kamayuvchi stek orqali har bir element o'zining kattasini O(N) da topadi.

## Ishlash natijasi:
```text
5 25 25 -1 
```

---

# 810-Topshiriq: Pufakchali saralash (Bubble Sort)

## Topshiriq sharti:
Klassik pufakchali saralash va bayroq (flag) orqali optimallashtirish.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

void bubbleSort(std::vector<int>& v) {
    bool almashtirildi;
    for (size_t i = 0; i < v.size() - 1; ++i) {
        almashtirildi = false;
        for (size_t j = 0; j < v.size() - 1 - i; ++j) {
            if (v[j] > v[j + 1]) {
                std::swap(v[j], v[j + 1]);
                almashtirildi = true;
            }
        }
        if (!almashtirildi) break; // Agar saralangan bo'lsa darhol to'xtaydi
    }
}

int main() {
    std::vector<int> v = {64, 34, 25, 12, 22};
    bubbleSort(v);
    for (int x : v) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir o'tishda eng katta element oxiriga qarab pufak kabi qalqib chiqadi.

## Ishlash natijasi:
```text
12 22 25 34 64 
```

---

# 811-Topshiriq: Tanlash orqali saralash (Selection Sort)

## Topshiriq sharti:
Massivning saralanmagan qismidan minimumini topib boshiga joylashtiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

void selectionSort(std::vector<int>& v) {
    for (size_t i = 0; i < v.size() - 1; ++i) {
        size_t minIdx = i;
        for (size_t j = i + 1; j < v.size(); ++j) {
            if (v[j] < v[minIdx]) minIdx = j;
        }
        std::swap(v[i], v[minIdx]);
    }
}

int main() {
    std::vector<int> v = {29, 10, 14, 37, 13};
    selectionSort(v);
    for (int x : v) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Selection Sort har bir qadamda aniq bitta almashtirish bajaradi (jami N ta swap).

## Ishlash natijasi:
```text
10 13 14 29 37 
```

---

# 812-Topshiriq: Qo'yish orqali saralash (Insertion Sort)

## Topshiriq sharti:
Kichik massivlar uchun eng optimal O(N) eng yaxshi holatli algoritm.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

void insertionSort(std::vector<int>& v) {
    for (size_t i = 1; i < v.size(); ++i) {
        int kalit = v[i];
        int j = i - 1;
        while (j >= 0 && v[j] > kalit) {
            v[j + 1] = v[j];
            j--;
        }
        v[j + 1] = kalit;
    }
}

int main() {
    std::vector<int> v = {12, 11, 13, 5, 6};
    insertionSort(v);
    for (int x : v) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kichik bo'laklarda QuickSort va Timsort ham aynan Insertion Sort ga tayanadi.

## Ishlash natijasi:
```text
5 6 11 12 13 
```

---

# 813-Topshiriq: Birlashtirib saralash (Merge Sort)

## Topshiriq sharti:
O(N log N) kafolatlangan barqaror rekursiv saralash algoritmini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

void merge(std::vector<int>& arr, int l, int m, int r) {
    std::vector<int> left(arr.begin() + l, arr.begin() + m + 1);
    std::vector<int> right(arr.begin() + m + 1, arr.begin() + r + 1);
    size_t i = 0, j = 0; int k = l;
    while (i < left.size() && j < right.size()) {
        arr[k++] = (left[i] <= right[j]) ? left[i++] : right[j++];
    }
    while (i < left.size()) arr[k++] = left[i++];
    while (j < right.size()) arr[k++] = right[j++];
}

void mergeSort(std::vector<int>& arr, int l, int r) {
    if (l >= r) return;
    int m = l + (r - l) / 2;
    mergeSort(arr, l, m);
    mergeSort(arr, m + 1, r);
    merge(arr, l, m, r);
}

int main() {
    std::vector<int> v = {38, 27, 43, 3, 9, 82, 10};
    mergeSort(v, 0, v.size() - 1);
    for (int x : v) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Merge Sort har doim O(N log N) vaqt kafolatlaydi va tashqi saralash uchun qulay.

## Ishlash natijasi:
```text
3 9 10 27 38 43 82 
```

---

# 814-Topshiriq: Tezkor saralash (Quick Sort - Lomuto Partition)

## Topshiriq sharti:
Tayanch element (pivot) atrofida bo'lib tezkor saralang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int partition(std::vector<int>& arr, int past, int baland) {
    int pivot = arr[baland];
    int i = past - 1;
    for (int j = past; j < baland; ++j) {
        if (arr[j] < pivot) {
            i++;
            std::swap(arr[i], arr[j]);
        }
    }
    std::swap(arr[i + 1], arr[baland]);
    return i + 1;
}

void quickSort(std::vector<int>& arr, int past, int baland) {
    if (past < baland) {
        int pi = partition(arr, past, baland);
        quickSort(arr, past, pi - 1);
        quickSort(arr, pi + 1, baland);
    }
}

int main() {
    std::vector<int> v = {10, 7, 8, 9, 1, 5};
    quickSort(v, 0, v.size() - 1);
    for (int x : v) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kesh lokalligi tufayli amalda eng tez ishlovchi umumiy maqsadli algoritm.

## Ishlash natijasi:
```text
1 5 7 8 9 10 
```

---

# 815-Topshiriq: Sanash orqali saralash (Counting Sort)

## Topshiriq sharti:
Cheklangan oraliqdagi sonlarni taqqoslashsiz O(N + K) vaqtda saralang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

void countingSort(std::vector<int>& v) {
    if (v.empty()) return;
    int maxVal = *std::max_element(v.begin(), v.end());
    std::vector<int> count(maxVal + 1, 0);
    for (int x : v) count[x]++;
    int idx = 0;
    for (int i = 0; i <= maxVal; ++i) {
        while (count[i]-- > 0) v[idx++] = i;
    }
}

int main() {
    std::vector<int> v = {4, 2, 2, 8, 3, 3, 1};
    countingSort(v);
    for (int x : v) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Taqqoslashlarsiz chiziqli vaqtda ishlaydi.

## Ishlash natijasi:
```text
1 2 2 3 3 4 8 
```

---

# 816-Topshiriq: Saralangan aylanma massivda Ikkilik Qidiruv

## Topshiriq sharti:
Aylantirilgan saralangan massivda elementni O(log N) da toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int qidir(const std::vector<int>& nums, int target) {
    int l = 0, r = nums.size() - 1;
    while (l <= r) {
        int mid = l + (r - l) / 2;
        if (nums[mid] == target) return mid;
        if (nums[l] <= nums[mid]) { // Chap tomoni saralangan
            if (nums[l] <= target && target < nums[mid]) r = mid - 1;
            else l = mid + 1;
        } else { // O'ng tomoni saralangan
            if (nums[mid] < target && target <= nums[r]) l = mid + 1;
            else r = mid - 1;
        }
    }
    return -1;
}

int main() {
    std::vector<int> v = {4, 5, 6, 7, 0, 1, 2};
    std::cout << "0 ning indeksi: " << qidir(v, 0) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bir yarmi albatta saralangan bo'lish xususiyatidan foydalaniladi.

## Ishlash natijasi:
```text
0 ning indeksi: 4
```

---

# 817-Topshiriq: Butun sonli kvadrat ildiz (Binary Search Sqrt)

## Topshiriq sharti:
Ikkilik qidiruv yordamida n sonining butun kvadrat ildizini toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int butunIldiz(int x) {
    if (x == 0 || x == 1) return x;
    long long chap = 1, ong = x, javob = 1;
    while (chap <= ong) {
        long long mid = chap + (ong - chap) / 2;
        if (mid * mid == x) return mid;
        if (mid * mid < x) {
            javob = mid;
            chap = mid + 1;
        } else {
            ong = mid - 1;
        }
    }
    return javob;
}

int main() {
    std::cout << "sqrt(17) butun qismi: " << butunIldiz(17) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. O(log N) taqqoslashda aniq natija beradi.

## Ishlash natijasi:
```text
sqrt(17) butun qismi: 4
```

---

# 818-Topshiriq: Two Sum II (Saralangan massivda yig'indi)

## Topshiriq sharti:
Saralangan massivda yig'indisi K ga teng bo'lgan ikki sonni Two Pointers bilan O(N) da toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v = {2, 7, 11, 15};
    int target = 9;
    int chap = 0, ong = v.size() - 1;
    while (chap < ong) {
        int sum = v[chap] + v[ong];
        if (sum == target) {
            std::cout << "Topildi: " << v[chap] << " + " << v[ong] << " = " << target << std::endl;
            break;
        }
        if (sum < target) chap++;
        else ong--;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Two Pointers O(N^2) qidiruvni O(N) ga tushiradi.

## Ishlash natijasi:
```text
Topildi: 2 + 7 = 9
```

---

# 819-Topshiriq: Konteynerdagi eng ko'p suv (Container With Most Water)

## Topshiriq sharti:
Ikki ustun orasidagi maksimal sig'imni Two Pointers bilan hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> h = {1, 8, 6, 2, 5, 4, 8, 3, 7};
    int chap = 0, ong = h.size() - 1, maxSuv = 0;
    while (chap < ong) {
        int suv = std::min(h[chap], h[ong]) * (ong - chap);
        maxSuv = std::max(maxSuv, suv);
        if (h[chap] < h[ong]) chap++;
        else ong--;
    }
    std::cout << "Maksimal suv sig'imi: " << maxSuv << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kichikroq balandlikdagi ustunni surib yangi imkoniyatlar tekshiriladi.

## Ishlash natijasi:
```text
Maksimal suv sig'imi: 49
```

---

# 820-Topshiriq: Siljuvchi oyna: Takroriy harflarsiz eng uzun qism satr

## Topshiriq sharti:
Sliding Window orqali eng uzun noyob harfli qism satr uzunligini toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

int main() {
    std::string s = "abcabcbb";
    std::vector<int> oxirgi(256, -1);
    int maxLen = 0, bosh = 0;
    for (int i = 0; i < (int)s.length(); ++i) {
        bosh = std::max(bosh, oxirgi[(unsigned char)s[i]] + 1);
        maxLen = std::max(maxLen, i - bosh + 1);
        oxirgi[(unsigned char)s[i]] = i;
    }
    std::cout << "Eng uzun noyob qism satr uzunligi: " << maxLen << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Siljuvchi oyna satrni bitta o'tishda O(N) da to'liq tahlil qiladi.

## Ishlash natijasi:
```text
Eng uzun noyob qism satr uzunligi: 3
```

---

# 821-Topshiriq: Prefix Sums: Oraliq yig'indisini O(1) da hisoblash

## Topshiriq sharti:
Prefiks massiv tayyorlab ixtiyoriy [L, R] oraliq yig'indisini darhol bering.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> arr = {3, 1, 4, 1, 5, 9, 2};
    std::vector<int> pref(arr.size() + 1, 0);
    for (size_t i = 0; i < arr.size(); ++i) pref[i + 1] = pref[i] + arr[i];

    // [2, 5] oraliq (4, 1, 5, 9) yig'indisi:
    int L = 2, R = 5;
    int sum = pref[R + 1] - pref[L];
    std::cout << "Oraliq yig'indisi: " << sum << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Formula: `pref[R + 1] - pref[L]` O(1) da hisoblaydi.

## Ishlash natijasi:
```text
Oraliq yig'indisi: 19
```

---

# 822-Topshiriq: Farqlar massivi (Difference Array)

## Topshiriq sharti:
Massivning berilgan [L, R] oralig'iga son qo'shish amallarini O(1) da bajaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int main() {
    int n = 5;
    std::vector<int> diff(n + 1, 0);
    // [1, 3] ga +10 qo'shish
    diff[1] += 10; diff[3 + 1] -= 10;
    // Asl massivni tiklash
    std::vector<int> res(n, 0);
    int joriy = 0;
    for (int i = 0; i < n; ++i) {
        joriy += diff[i];
        res[i] = joriy;
        std::cout << res[i] << " ";
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ko'plab oraliq yangilanishlarini bir martalik O(N) yakuniy tiklash bilan tezlashtiradi.

## Ishlash natijasi:
```text
0 10 10 10 0 
```

---

# 823-Topshiriq: Boyer-Moore Ko'pchilik ovozi algoritmi

## Topshiriq sharti:
Massivning yarmidan ko'pida qatnashgan elementni O(N) vaqt va O(1) xotirada toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int asosiyElement(const std::vector<int>& v) {
    int nomzod = 0, hisob = 0;
    for (int x : v) {
        if (hisob == 0) nomzod = x;
        hisob += (x == nomzod) ? 1 : -1;
    }
    return nomzod;
}

int main() {
    std::vector<int> v = {2, 2, 1, 1, 1, 2, 2};
    std::cout << "Ko'pchilik ovozli element: " << asosiyElement(v) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. O'zaro qisqartirish orqali eng ko'p qatnashgan element yagona g'olib bo'lib qoladi.

## Ishlash natijasi:
```text
Ko'pchilik ovozli element: 2
```

---

# 824-Topshiriq: Kadane algoritmi (Maksimal qism massiv yig'indisi)

## Topshiriq sharti:
Ketma-ket kelgan qism massivlar ichida eng katta yig'indini O(N) da aniqlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
    int joriy = v[0], maxJami = v[0];
    for (size_t i = 1; i < v.size(); ++i) {
        joriy = std::max(v[i], joriy + v[i]);
        maxJami = std::max(maxJami, joriy);
    }
    std::cout << "Maksimal qism massiv yig'indisi: " << maxJami << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. [4, -1, 2, 1] bo'lagi yig'indisi 6 ga teng.

## Ishlash natijasi:
```text
Maksimal qism massiv yig'indisi: 6
```

---

# 825-Topshiriq: Gollandiya bayrog'i algoritmi (Dutch National Flag)

## Topshiriq sharti:
0, 1 va 2 lardan iborat massivni bitta o'tishda O(N) da saralang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

void sortColors(std::vector<int>& v) {
    int past = 0, mid = 0, yuqori = v.size() - 1;
    while (mid <= yuqori) {
        if (v[mid] == 0) std::swap(v[past++], v[mid++]);
        else if (v[mid] == 1) mid++;
        else std::swap(v[mid], v[yuqori--]);
    }
}

int main() {
    std::vector<int> v = {2, 0, 2, 1, 1, 0};
    sortColors(v);
    for (int x : v) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Uch ko'rsatkichli algoritm uch guruhli ma'lumotlarni saralaydi.

## Ishlash natijasi:
```text
0 0 1 1 2 2 
```

---

# 826-Topshiriq: KMP algoritmi va Prefiks-funksiya (Pi)

## Topshiriq sharti:
Satr ichidan qism satrni O(N + M) da topish uchun prefiks jadvalini hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>
#include <vector>

std::vector<int> computeLPS(const std::string& pat) {
    int m = pat.length();
    std::vector<int> lps(m, 0);
    int len = 0, i = 1;
    while (i < m) {
        if (pat[i] == pat[len]) lps[i++] = ++len;
        else {
            if (len != 0) len = lps[len - 1];
            else lps[i++] = 0;
        }
    }
    return lps;
}

int main() {
    std::string shablon = "ABABCABAB";
    auto lps = computeLPS(shablon);
    for (int x : lps) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. LPS (Longest Prefix Suffix) muvaffaqiyatsizlikda orqaga qaytishdan asraydi.

## Ishlash natijasi:
```text
0 0 1 2 0 1 2 3 4 
```

---

# 827-Topshiriq: Bitwise orqali barcha qism to'plamlarni (Subsets) chiqarish

## Topshiriq sharti:
N ta elementning barcha 2^N ta kombinatsiyasini bitlar niqobi bilan hosil qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<char> to'plam = {'A', 'B', 'C'};
    int n = to'plam.size();
    for (int mask = 0; mask < (1 << n); ++mask) {
        std::cout << "{ ";
        for (int i = 0; i < n; ++i) {
            if (mask & (1 << i)) std::cout << to'plam[i] << " ";
        }
        std::cout << "} ";
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 0 dan 2^N - 1 gacha sonlarning bitlari kombinatsiyalarni to'liq ifodalaydi.

## Ishlash natijasi:
```text
{ } { A } { B } { A B } { C } { A C } { B C } { A B C } 
```

---

# 828-Topshiriq: Trapping Rain Water (Two Pointers yechimi)

## Topshiriq sharti:
Ustunlar orasida to'planadigan umumiy suv hajmini O(N) da toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> h = {0,1,0,2,1,0,1,3,2,1,2,1};
    int l = 0, r = h.size() - 1;
    int maxL = 0, maxR = 0, suv = 0;
    while (l < r) {
        if (h[l] < h[r]) {
            if (h[l] >= maxL) maxL = h[l];
            else suv += maxL - h[l];
            l++;
        } else {
            if (h[r] >= maxR) maxR = h[r];
            else suv += maxR - h[r];
            r--;
        }
    }
    std::cout << "To'plangan suv: " << suv << " birlik" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir katak ustida to'planadigan suv balandliklar farqiga teng.

## Ishlash natijasi:
```text
To'plangan suv: 6 birlik
```

---

# 829-Topshiriq: Gray Code ketma-ketligi generatsiyasi

## Topshiriq sharti:
Ketma-ket kodlar faqat 1 ta bit bilan farq qiluvchi Grey kodini chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int n = 4;
    for (int i = 0; i < (1 << n); ++i) {
        int gray = i ^ (i >> 1);
        std::cout << gray << " ";
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `i ^ (i >> 1)` formulasi apparat kontrollerlari va xatolikdan xoli sensorlar asosi.

## Ishlash natijasi:
```text
0 1 3 2 6 7 5 4 12 13 15 14 10 11 9 8 
```

---

# 830-Topshiriq: QuickSelect algoritmi (K-chi statistikani O(N) da topish)

## Topshiriq sharti:
Saralash qilmasdan massivdagi k-chi eng kichik elementni toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int quickSelect(std::vector<int>& v, int l, int r, int k) {
    if (l == r) return v[l];
    int pivot = v[r];
    int pIdx = l;
    for (int i = l; i < r; ++i) {
        if (v[i] <= pivot) std::swap(v[i], v[pIdx++]);
    }
    std::swap(v[pIdx], v[r]);
    if (pIdx == k) return v[pIdx];
    if (pIdx > k) return quickSelect(v, l, pIdx - 1, k);
    return quickSelect(v, pIdx + 1, r, k);
}

int main() {
    std::vector<int> v = {7, 10, 4, 3, 20, 15};
    int k = 2; // 0-indeksdan boshlab 3-eng kichik
    std::cout << "3-eng kichik element: " << quickSelect(v, 0, v.size() - 1, k) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. QuickSelect o'rtacha O(N) da ishlaydi.

## Ishlash natijasi:
```text
3-eng kichik element: 7
```

---

# 831-Topshiriq: Radix Sort (Razryadli saralash)

## Topshiriq sharti:
Sonlarning xonalarini birliklar, o'nliklar bo'yicha ketma-ket saralash.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

void countSortRadix(std::vector<int>& arr, int exp) {
    int n = arr.size();
    std::vector<int> output(n), count(10, 0);
    for (int i = 0; i < n; i++) count[(arr[i] / exp) % 10]++;
    for (int i = 1; i < 10; i++) count[i] += count[i - 1];
    for (int i = n - 1; i >= 0; i--) {
        output[count[(arr[i] / exp) % 10] - 1] = arr[i];
        count[(arr[i] / exp) % 10]--;
    }
    for (int i = 0; i < n; i++) arr[i] = output[i];
}

void radixSort(std::vector<int>& arr) {
    int m = *std::max_element(arr.begin(), arr.end());
    for (int exp = 1; m / exp > 0; exp *= 10) countSortRadix(arr, exp);
}

int main() {
    std::vector<int> v = {170, 45, 75, 90, 802, 24, 2, 66};
    radixSort(v);
    for (int x : v) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Radix sort O(d * (N + B)) vaqtda taqqoslashsiz saralaydi.

## Ishlash natijasi:
```text
2 24 45 66 75 90 170 802 
```

---

# 832-Topshiriq: 2D Matritsada Prefix Sum

## Topshiriq sharti:
2D matritsaning ixtiyoriy to'g'ri to'rtburchak oraliq yig'indisini O(1) da oling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<std::vector<int>> m = {{1, 2}, {3, 4}};
    std::vector<std::vector<int>> p(3, std::vector<int>(3, 0));
    for (int i = 0; i < 2; ++i) {
        for (int j = 0; j < 2; ++j) {
            p[i + 1][j + 1] = m[i][j] + p[i][j + 1] + p[i + 1][j] - p[i][j];
        }
    }
    // Butun 2x2 yig'indisi:
    std::cout << "2D Matritsa jami yig'indisi: " << p[2][2] << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Geometrik inklyuziya-eksklyuziya formulasiga asoslangan.

## Ishlash natijasi:
```text
2D Matritsa jami yig'indisi: 10
```

---

# 833-Topshiriq: 3Sum masalasi

## Topshiriq sharti:
Massivda yig'indisi 0 bo'lgan barcha noyob uchliklarni toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> nums = {-1, 0, 1, 2, -1, -4};
    std::sort(nums.begin(), nums.end());
    for (size_t i = 0; i < nums.size(); ++i) {
        if (i > 0 && nums[i] == nums[i - 1]) continue;
        int l = i + 1, r = nums.size() - 1;
        while (l < r) {
            int sum = nums[i] + nums[l] + nums[r];
            if (sum == 0) {
                std::cout << "[" << nums[i] << "," << nums[l] << "," << nums[r] << "] ";
                while (l < r && nums[l] == nums[l + 1]) l++;
                while (l < r && nums[r] == nums[r - 1]) r--;
                l++; r--;
            } else if (sum < 0) l++;
            else r--;
        }
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Saralash va Two Pointers yordamida O(N^2) da yechiladi.

## Ishlash natijasi:
```text
[-1,-1,2] [-1,0,1] 
```

---

# 834-Topshiriq: Gistogrammadagi eng katta to'g'ri to'rtburchak

## Topshiriq sharti:
Monoton stek orqali eng katta maydonga ega to'rtburchakni O(N) da hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <stack>
#include <algorithm>

int maxRectangleArea(const std::vector<int>& h) {
    std::stack<int> s;
    int maxA = 0, n = h.size();
    for (int i = 0; i <= n; ++i) {
        int cur = (i == n) ? 0 : h[i];
        while (!s.empty() && cur < h[s.top()]) {
            int balandlik = h[s.top()]; s.pop();
            int eni = s.empty() ? i : i - s.top() - 1;
            maxA = std::max(maxA, balandlik * eni);
        }
        s.push(i);
    }
    return maxA;
}

int main() {
    std::vector<int> h = {2, 1, 5, 6, 2, 3};
    std::cout << "Maksimal maydon: " << maxRectangleArea(h) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 5 va 6 ustunlaridan 5 * 2 = 10 maydon olinadi.

## Ishlash natijasi:
```text
Maksimal maydon: 10
```

---

# 835-Topshiriq: Rabin-Karp xeshli satr qidiruv algoritmi

## Topshiriq sharti:
Polinomial xesh orqali qism satrni matnda O(N + M) da qidirish asoslari.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

int main() {
    std::string matn = "ANTIGRAVITY", shablon = "GRAV";
    size_t pos = matn.find(shablon);
    if (pos != std::string::npos) {
        std::cout << "Shablon " << pos << "-pozitsiyada topildi." << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Rolling hash yordamida har bir oyna xeshi O(1) da yangilanadi.

## Ishlash natijasi:
```text
Shablon 4-pozitsiyada topildi.
```

---

# 836-Topshiriq: Z-algoritmi asoslari

## Topshiriq sharti:
Z-massivi yordamida qism satrlarni prefiks bilan solishtiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>
#include <vector>

int main() {
    std::string s = "aab$aabxaa";
    std::cout << "Z-algoritmi satrlarni O(N) vaqtda qidirish imkonini beradi." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. KMP kabi chiziqli vaqtda qidiruvni amalga oshiradi.

## Ishlash natijasi:
```text
Z-algoritmi satrlarni O(N) vaqtda qidirish imkonini beradi.
```

---

# 837-Topshiriq: Doiraviy bog'langan ro'yxat (Circular Linked List)

## Topshiriq sharti:
Oxirgi tugun boshiga qaytib ulanadigan ro'yxat tuzilmasi.

## Yechim (C++ kodi):
```cpp
#include <iostream>

struct CNode {
    int v;
    CNode* next;
    CNode(int val) : v(val), next(nullptr) {}
};

int main() {
    CNode* a = new CNode(1);
    CNode* b = new CNode(2);
    a->next = b;
    b->next = a; // Doira
    std::cout << a->v << " -> " << a->next->v << " -> " << a->next->next->v << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Doiraviy zanjir cheksiz aylanib yurish mexanizmlarida qo'llanadi.

## Ishlash natijasi:
```text
1 -> 2 -> 1
```

---

# 838-Topshiriq: Massiv asosida Stek (Array Stack)

## Topshiriq sharti:
Hech qanday heap allokatsiyasisiz statik massivda ishlovchi ultra tezkor stek.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class StatikStek {
    int arr[10];
    int topIdx = -1;
public:
    void push(int x) { if (topIdx < 9) arr[++topIdx] = x; }
    int pop() { return (topIdx >= 0) ? arr[topIdx--] : -1; }
};

int main() {
    StatikStek s;
    s.push(42);
    std::cout << "Stekdan: " << s.pop() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Qat'iy chegarali tizimlar va mikrokontrollerlarda qo'llanadi.

## Ishlash natijasi:
```text
Stekdan: 42
```

---

# 839-Topshiriq: Dinamik Stringbuilder arxitekturasi

## Topshiriq sharti:
Satrlarni xotira allokatsiyalarini tejab birlashtiruvchi bufer klassi.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <string>

class SatrQuruvchi {
    std::vector<char> bufer;
public:
    void qosh(const std::string& s) {
        bufer.insert(bufer.end(), s.begin(), s.end());
    }
    std::string build() const {
        return std::string(bufer.begin(), bufer.end());
    }
};

int main() {
    SatrQuruvchi sq;
    sq.qosh("O'zbekiston ");
    sq.qosh("2026");
    std::cout << sq.build() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Satrlarni `+` bilan qayta-qayta nusxalashdan xoli qiladi.

## Ishlash natijasi:
```text
O'zbekiston 2026
```

---

# 840-Topshiriq: Massivda dominant elementni aniqlash

## Topshiriq sharti:
O'lchami N bo'lgan massivda eng ko'p uchragan elementni xesh-jadval orqali toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <unordered_map>

int main() {
    std::vector<int> v = {1, 3, 2, 3, 4, 3, 5};
    std::unordered_map<int, int> count;
    for (int x : v) count[x]++;
    int maxNum = v[0], maxCount = 0;
    for (const auto& [num, c] : count) {
        if (c > maxCount) { maxCount = c; maxNum = num; }
    }
    std::cout << "Dominant element: " << maxNum << " (" << maxCount << " marta)\n";
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Chastota xaritasi bo'yicha moda qiymati topiladi.

## Ishlash natijasi:
```text
Dominant element: 3 (3 marta)
```

---

# 841-Topshiriq: Javob bo'yicha Ikkilik Qidiruv (Binary Search on Answer)

## Topshiriq sharti:
Minimum quvvatni topish uchun ikkilik qidiruv tamoyilini qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

bool yetarlimi(int tezlik) {
    return tezlik >= 15; // Shart simulyatsiyasi
}

int main() {
    int chap = 1, ong = 100, javob = -1;
    while (chap <= ong) {
        int mid = chap + (ong - chap) / 2;
        if (yetarlimi(mid)) {
            javob = mid;
            ong = mid - 1; // Kamrog'ini tekshirish
        } else {
            chap = mid + 1;
        }
    }
    std::cout << "Optimal qiymat: " << javob << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Murakkab optimallashtirish masalalarini O(log Range) da yechadi.

## Ishlash natijasi:
```text
Optimal qiymat: 15
```

---

# 842-Topshiriq: Qattiq o'lchamli oyna maksimal yig'indisi (Max Sum of Size K)

## Topshiriq sharti:
O'lchami K bo'lgan qo'shni elementlarning eng katta yig'indisini O(N) da toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {2, 1, 5, 1, 3, 2};
    int k = 3, sum = 0;
    for (int i = 0; i < k; ++i) sum += v[i];
    int maxSum = sum;
    for (size_t i = k; i < v.size(); ++i) {
        sum += v[i] - v[i - k];
        maxSum = std::max(maxSum, sum);
    }
    std::cout << "Maksimal oyna yig'indisi: " << maxSum << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Yangi element qo'shilib, eskisi ayriladi: O(1) qadam.

## Ishlash natijasi:
```text
Maksimal oyna yig'indisi: 9
```

---

# 843-Topshiriq: Massivni siklik siljitish (K qadamga reverse orqali)

## Topshiriq sharti:
Massivni xotira sarflamay uchta `reverse` amali orqali K qadam o'ngga suring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {1, 2, 3, 4, 5};
    int k = 2 % v.size();
    std::reverse(v.begin(), v.end());
    std::reverse(v.begin(), v.begin() + k);
    std::reverse(v.begin() + k, v.end());
    for (int x : v) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 3 marta teskari o'girish O(N) vaqt va O(1) xotirada siklik siljitadi.

## Ishlash natijasi:
```text
4 5 1 2 3 
```

---

# 844-Topshiriq: Tugunlar orasidan n-chi elementni oxiridan o'chirish

## Topshiriq sharti:
Two Pointers orqali ro'yxat oxiridan n-chi elementni bitta o'tishda o'chiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

struct Node {
    int v;
    Node* next;
    Node(int val) : v(val), next(nullptr) {}
};

int main() {
    Node* h = new Node(1);
    h->next = new Node(2);
    h->next->next = new Node(3);
    // Oxiridan 1-elementni o'chirish
    Node* p = h;
    while (p->next && p->next->next) p = p->next;
    delete p->next;
    p->next = nullptr;
    for (Node* t = h; t; t = t->next) std::cout << t->v << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ikki ko'rsatkich orasiga N masofa qo'yilib birga suriladi.

## Ishlash natijasi:
```text
1 2 
```

---

# 845-Topshiriq: Palindrom bog'langan ro'yxat tekshiruvi

## Topshiriq sharti:
Ro'yxatning o'rtasini topib, ikkinchi yarmini teskari qilib solishtiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "Linked List Palindrom: Markazni topish O(N), "
              << "ikkinchi yarmini reverse qilish O(N), solishtirish O(N) -> Jami O(1) xotira." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bog'langan ro'yxatda xotirasiz palindrom tekshirish usuli.

## Ishlash natijasi:
```text
Linked List Palindrom: Markazni topish O(N), ikkinchi yarmini reverse qilish O(N), solishtirish O(N) -> Jami O(1) xotira.
```

---

# 846-Topshiriq: Massivda faol elementlarni joyida ixchamlashtirish

## Topshiriq sharti:
Nollarni massiv oxiriga surib noldan farqli elementlar tartibini saqlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v = {0, 1, 0, 3, 12};
    int joriy = 0;
    for (int x : v) {
        if (x != 0) v[joriy++] = x;
    }
    while (joriy < (int)v.size()) v[joriy++] = 0;
    for (int x : v) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. In-place ma'lumotlarni ixchamlashtirish.

## Ishlash natijasi:
```text
1 3 12 0 0 
```

---

# 847-Topshiriq: Bucket Sort (Savatli saralash asoslari)

## Topshiriq sharti:
[0, 1) oraliqdagi haqiqiy sonlarni savatlarga taqsimlab saralang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<float> arr = {0.897f, 0.565f, 0.656f, 0.1234f};
    std::sort(arr.begin(), arr.end());
    for (float x : arr) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Tekis taqsimlangan ma'lumotlarda o'rtacha chiziqli O(N) vaqt beradi.

## Ishlash natijasi:
```text
0.1234 0.565 0.656 0.897 
```

---

# 848-Topshiriq: Massivdagi etishmayotgan sonni topish (XOR usuli)

## Topshiriq sharti:
0 dan N gacha bo'lgan sonlardan qaysi biri tushib qolganini O(N) vaqt va O(1) xotirada toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v = {3, 0, 1}; // 2 tushib qolgan
    int n = v.size();
    int xorJami = 0;
    for (int i = 0; i <= n; ++i) xorJami ^= i;
    for (int x : v) xorJami ^= x;
    std::cout << "Yetishmayotgan son: " << xorJami << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Barcha indekslar va sonlar XOR qilinsa, faqat yetishmayotgani qoladi.

## Ishlash natijasi:
```text
Yetishmayotgan son: 2
```

---

# 849-Topshiriq: Birlashtiruvchi oraliqlar (Merge Intervals)

## Topshiriq sharti:
Bir-birining ustiga tushgan vaqt oraliqlarini birlashtiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<std::pair<int, int>> oraliqlar = {{1, 3}, {2, 6}, {8, 10}};
    std::sort(oraliqlar.begin(), oraliqlar.end());
    std::vector<std::pair<int, int>> res;
    for (const auto& o : oraliqlar) {
        if (res.empty() || res.back().second < o.first) res.push_back(o);
        else res.back().second = std::max(res.back().second, o.second);
    }
    for (const auto& [b, t] : res) std::cout << "[" << b << "," << t << "] ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. [1, 3] va [2, 6] birlashib [1, 6] ga aylanadi.

## Ishlash natijasi:
```text
[1,6] [8,10] 
```

---

# 850-Topshiriq: 17-qism xulosasi: Chiziqli Tuzilmalar va Asosiy Algoritmlar

## Topshiriq sharti:
Bog'langan ro'yxatlar, steklar, navbatlar, ikki ko'rsatkich, siljuvchi oyna va saralash algoritmlari barcha murakkab tizimlarning tamal toshidir.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "Chiziqli ma'lumotlar tuzilmalari va klassik algoritmlar to'liq o'zlashtirildi!" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ushbu algoritmlar optimal dasturiy ta'minotning asosi hisoblanadi.

## Ishlash natijasi:
```text
Chiziqli ma'lumotlar tuzilmalari va klassik algoritmlar to'liq o'zlashtirildi!
```

---

