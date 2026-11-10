# 18-Qism: Murakkab Ma'lumotlar Tuzilmalari va Ilg'or Algoritmlar (851-900)

Ushbu qismda C++ tilida daraxtlar (BST, AVL, Trie), graflar (BFS, DFS, Dijkstra, Bellman-Ford, Kruskal, Prim), dinamik dasturlash (DP), segmentlar daraxti, to'dalar (Heap) va murakkab algoritmlar noldan chuqur o'rganiladi.

# 851-Topshiriq: Ikkilik qidiruv daraxti (BST) - tugun qo'shish va inorder traversali
## Topshiriq sharti:
C++ da `TreeNode` strukturasini yarating. Ikkilik qidiruv daraxtiga (BST) elementlarni qo'shuvchi `insert` funksiyasini va daraxt elementlarini o'sish tartibida ekranga chiqaruvchi `inorder` rekursiv traversali yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

TreeNode* insert(TreeNode* root, int val) {
    if (root == nullptr) {
        return new TreeNode(val);
    }
    if (val < root->val) {
        root->left = insert(root->left, val);
    } else if (val > root->val) {
        root->right = insert(root->right, val);
    }
    return root;
}

void inorder(TreeNode* root) {
    if (root == nullptr) return;
    inorder(root->left);
    std::cout << root->val << " ";
    inorder(root->right);
}

int main() {
    TreeNode* root = nullptr;
    int values[] = {50, 30, 70, 20, 40, 60, 80};
    for (int v : values) {
        root = insert(root, v);
    }

    std::cout << "BST Inorder traversali (o'sish tartibida): ";
    inorder(root);
    std::cout << std::endl;

    return 0;
}
```

## Tushuntirish va Mantiq:
BST qoidasiga ko'ra chap shoxdagi har bir tugun ota tugundan kichik, o'ng shoxdagisi esa katta bo'ladi. Inorder (chap, ildiz, o'ng) traversali natijasida barcha elementlar o'sish tartibida tartiblanadi.

## Ishlash natijasi:
```text
BST Inorder traversali (o'sish tartibida): 20 30 40 50 60 70 80
```

# 852-Topshiriq: BST - qiymatni rekursiv va iterativ qidirish
## Topshiriq sharti:
BST ichida berilgan `val` qiymati mavjudligini tekshiruvchi ikkita usulni: `searchRecursive` va xotira stekini tejovchi `searchIterative` funksiyalarini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

TreeNode* insert(TreeNode* root, int val) {
    if (!root) return new TreeNode(val);
    if (val < root->val) root->left = insert(root->left, val);
    else if (val > root->val) root->right = insert(root->right, val);
    return root;
}

bool searchRecursive(TreeNode* root, int target) {
    if (root == nullptr) return false;
    if (root->val == target) return true;
    if (target < root->val) return searchRecursive(root->left, target);
    return searchRecursive(root->right, target);
}

bool searchIterative(TreeNode* root, int target) {
    TreeNode* curr = root;
    while (curr != nullptr) {
        if (curr->val == target) return true;
        if (target < curr->val) curr = curr->left;
        else curr = curr->right;
    }
    return false;
}

int main() {
    TreeNode* root = nullptr;
    int arr[] = {45, 12, 89, 5, 23, 72, 99};
    for (int x : arr) root = insert(root, x);

    std::cout << "Rekursiv 23 mavjudmi: " << (searchRecursive(root, 23) ? "Ha" : "Yo'q") << "\n";
    std::cout << "Iterativ 50 mavjudmi: " << (searchIterative(root, 50) ? "Ha" : "Yo'q") << "\n";
    std::cout << "Iterativ 89 mavjudmi: " << (searchIterative(root, 89) ? "Ha" : "Yo'q") << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
BST da qidirish vaqti muvozanatlangan daraxt uchun O(log N) ni tashkil etadi. Iterativ qidirish qo'shimcha rekursiya chaqiruv stekidan (call stack) foydalanmaydi, O(1) xotirada ishlaydi.

## Ishlash natijasi:
```text
Rekursiv 23 mavjudmi: Ha
Iterativ 50 mavjudmi: Yo'q
Iterativ 89 mavjudmi: Ha
```

# 853-Topshiriq: BST - minimal va maksimal qiymatlarni topish
## Topshiriq sharti:
BST daraxtidagi eng kichik (eng chapdagi) va eng katta (eng o'ngdagi) elementlarni qaytaruvchi `findMin` va `findMax` funksiyalarini amalga oshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <stdexcept>

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

TreeNode* insert(TreeNode* root, int val) {
    if (!root) return new TreeNode(val);
    if (val < root->val) root->left = insert(root->left, val);
    else if (val > root->val) root->right = insert(root->right, val);
    return root;
}

int findMin(TreeNode* root) {
    if (!root) throw std::runtime_error("Daraxt bo'sh!");
    TreeNode* curr = root;
    while (curr->left != nullptr) {
        curr = curr->left;
    }
    return curr->val;
}

int findMax(TreeNode* root) {
    if (!root) throw std::runtime_error("Daraxt bo'sh!");
    TreeNode* curr = root;
    while (curr->right != nullptr) {
        curr = curr->right;
    }
    return curr->val;
}

int main() {
    TreeNode* root = nullptr;
    int vals[] = {40, 20, 60, 10, 30, 50, 70, 5, 85};
    for (int v : vals) root = insert(root, v);

    std::cout << "Eng kichik qiymat: " << findMin(root) << std::endl;
    std::cout << "Eng katta qiymat: " << findMax(root) << std::endl;

    return 0;
}
```

## Tushuntirish va Mantiq:
BST ning xususiyatiga ko'ra eng kichik element doim chap shoxning eng oxirida, eng katta element esa o'ng shoxning eng oxirida joylashgan bo'ladi.

## Ishlash natijasi:
```text
Eng kichik qiymat: 5
Eng katta qiymat: 85
```

# 854-Topshiriq: BST - tugunni o'chirish (Delete Node)
## Topshiriq sharti:
BST dan tugunni o'chiruvchi `deleteNode` funksiyasini yarating. 3 ta holatni (farzandsiz, 1 ta farzandli, 2 ta farzandli - inorder successor bilan almashtirish) to'g'ri boshqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

TreeNode* insert(TreeNode* root, int val) {
    if (!root) return new TreeNode(val);
    if (val < root->val) root->left = insert(root->left, val);
    else if (val > root->val) root->right = insert(root->right, val);
    return root;
}

TreeNode* findMinNode(TreeNode* node) {
    TreeNode* curr = node;
    while (curr && curr->left != nullptr) curr = curr->left;
    return curr;
}

TreeNode* deleteNode(TreeNode* root, int key) {
    if (root == nullptr) return nullptr;

    if (key < root->val) {
        root->left = deleteNode(root->left, key);
    } else if (key > root->val) {
        root->right = deleteNode(root->right, key);
    } else {
        // 1-holat yoki 2-holat: 0 yoki 1 ta farzand
        if (root->left == nullptr) {
            TreeNode* temp = root->right;
            delete root;
            return temp;
        } else if (root->right == nullptr) {
            TreeNode* temp = root->left;
            delete root;
            return temp;
        }
        // 3-holat: 2 ta farzand - o'ng ost-daraxtdagi eng kichik tugunni (inorder successor) topamiz
        TreeNode* temp = findMinNode(root->right);
        root->val = temp->val;
        root->right = deleteNode(root->right, temp->val);
    }
    return root;
}

void inorder(TreeNode* root) {
    if (!root) return;
    inorder(root->left);
    std::cout << root->val << " ";
    inorder(root->right);
}

int main() {
    TreeNode* root = nullptr;
    int arr[] = {50, 30, 70, 20, 40, 60, 80};
    for (int x : arr) root = insert(root, x);

    std::cout << "Asl daraxt: ";
    inorder(root);
    std::cout << "\n";

    root = deleteNode(root, 20); // 0 ta farzand
    std::cout << "20 o'chirilgach: ";
    inorder(root);
    std::cout << "\n";

    root = deleteNode(root, 30); // 1 ta farzand
    std::cout << "30 o'chirilgach: ";
    inorder(root);
    std::cout << "\n";

    root = deleteNode(root, 50); // 2 ta farzand
    std::cout << "50 (ildiz) o'chirilgach: ";
    inorder(root);
    std::cout << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
Tugunni o'chirishda 2 ta farzandi bo'lsa, uning o'rniga o'ng shoxining eng kichik elementi (inorder successor) qo'yiladi va o'sha takrorlangan element o'ng shoxdan o'chiriladi.

## Ishlash natijasi:
```text
Asl daraxt: 20 30 40 50 60 70 80
20 o'chirilgach: 30 40 50 60 70 80
30 o'chirilgach: 40 50 60 70 80
50 (ildiz) o'chirilgach: 40 60 70 80
```

# 855-Topshiriq: BST balandligi va muvozanatini (isBalanced) hisoblash
## Topshiriq sharti:
Ikkilik daraxt balandligini hisoblovchi `height` funksiyasi va daraxt AVL qoidasiga ko'ra muvozanatlashganini (har bir tugun uchun chap va o'ng ost daraxt balandliklari farqi <= 1) tekshiruvchi `isBalanced` funksiyasini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <algorithm>
#include <cmath>

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

int checkHeight(TreeNode* root) {
    if (root == nullptr) return 0;

    int leftH = checkHeight(root->left);
    if (leftH == -1) return -1;

    int rightH = checkHeight(root->right);
    if (rightH == -1) return -1;

    if (std::abs(leftH - rightH) > 1) return -1;
    return std::max(leftH, rightH) + 1;
}

bool isBalanced(TreeNode* root) {
    return checkHeight(root) != -1;
}

int main() {
    TreeNode* root1 = new TreeNode(1);
    root1->left = new TreeNode(2);
    root1->right = new TreeNode(3);
    root1->left->left = new TreeNode(4);
    root1->left->right = new TreeNode(5);

    std::cout << "1-daraxt muvozanatlanganmi: " << (isBalanced(root1) ? "Ha" : "Yo'q") << "\n";

    TreeNode* root2 = new TreeNode(1);
    root2->left = new TreeNode(2);
    root2->left->left = new TreeNode(3);
    root2->left->left->left = new TreeNode(4);

    std::cout << "2-daraxt muvozanatlanganmi: " << (isBalanced(root2) ? "Ha" : "Yo'q") << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
Balandlikni pastdan yuqoriga O(N) vaqtda tekshirish eng optimal usuldir. Agar istalgan tugunda balandliklar farqi 1 dan katta bo'lsa, darhol -1 qaytarilib, daraxt nomutanosib deb belgilanadi.

## Ishlash natijasi:
```text
1-daraxt muvozanatlanganmi: Ha
2-daraxt muvozanatlanganmi: Yo'q
```

# 856-Topshiriq: AVL daraxti - chap va o'ng burilish (Rotations)
## Topshiriq sharti:
AVL daraxtida muvozanatni tiklash uchun ishlatiladigan `rotateRight` va `rotateLeft` operatsiyalarini va tugun balandligini yangilash mantiqini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <algorithm>

struct AVLNode {
    int val;
    AVLNode* left;
    AVLNode* right;
    int height;
    AVLNode(int k) : val(k), left(nullptr), right(nullptr), height(1) {}
};

int getHeight(AVLNode* n) {
    return n ? n->height : 0;
}

int getBalance(AVLNode* n) {
    return n ? getHeight(n->left) - getHeight(n->right) : 0;
}

AVLNode* rotateRight(AVLNode* y) {
    AVLNode* x = y->left;
    AVLNode* T2 = x->right;

    x->right = y;
    y->left = T2;

    y->height = std::max(getHeight(y->left), getHeight(y->right)) + 1;
    x->height = std::max(getHeight(x->left), getHeight(x->right)) + 1;

    return x;
}

AVLNode* rotateLeft(AVLNode* x) {
    AVLNode* y = x->right;
    AVLNode* T2 = y->left;

    y->left = x;
    x->right = T2;

    x->height = std::max(getHeight(x->left), getHeight(x->right)) + 1;
    y->height = std::max(getHeight(y->left), getHeight(y->right)) + 1;

    return y;
}

void inorder(AVLNode* root) {
    if (!root) return;
    inorder(root->left);
    std::cout << root->val << " ";
    inorder(root->right);
}

int main() {
    AVLNode* root = new AVLNode(30);
    root->left = new AVLNode(20);
    root->left->left = new AVLNode(10);
    root->height = 3;
    root->left->height = 2;

    std::cout << "Burilishdan oldingi ildiz: " << root->val << "\n";
    root = rotateRight(root);
    std::cout << "O'ng burilishdan keyingi yangi ildiz: " << root->val << "\n";
    std::cout << "Yangi ildiz balandligi: " << root->height << "\n";
    std::cout << "Inorder tartibi: ";
    inorder(root);
    std::cout << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
Chap va o'ng burilishlar BST xossalarini saqlagan holda daraxt balandligini kamaytiradi. Har bir burilish O(1) vaqt oladi va ko'rsatkichlarni yangilaydi.

## Ishlash natijasi:
```text
Burilishdan oldingi ildiz: 30
O'ng burilishdan keyingi yangi ildiz: 20
Yangi ildiz balandligi: 2
Inorder tartibi: 10 20 30
```

# 857-Topshiriq: Trie (Prefiks daraxti) - so'z qo'shish va qidirish
## Topshiriq sharti:
Kichik lotin harflari uchun `Trie` klassini yarating. Unga `insert(string word)` va `search(string word)` metodlarini qo'shing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>
#include <vector>

class Trie {
private:
    struct TrieNode {
        TrieNode* children[26];
        bool isEndOfWord;
        TrieNode() : isEndOfWord(false) {
            for (int i = 0; i < 26; ++i) children[i] = nullptr;
        }
    };
    TrieNode* root;

public:
    Trie() { root = new TrieNode(); }

    void insert(const std::string& word) {
        TrieNode* curr = root;
        for (char c : word) {
            int idx = c - 'a';
            if (curr->children[idx] == nullptr) {
                curr->children[idx] = new TrieNode();
            }
            curr = curr->children[idx];
        }
        curr->isEndOfWord = true;
    }

    bool search(const std::string& word) const {
        TrieNode* curr = root;
        for (char c : word) {
            int idx = c - 'a';
            if (curr->children[idx] == nullptr) return false;
            curr = curr->children[idx];
        }
        return curr->isEndOfWord;
    }
};

int main() {
    Trie trie;
    trie.insert("salom");
    trie.insert("samolyot");
    trie.insert("sariq");

    std::cout << "'salom' mavjudmi: " << (trie.search("salom") ? "Ha" : "Yo'q") << "\n";
    std::cout << "'sam' mavjudmi: " << (trie.search("sam") ? "Ha" : "Yo'q") << "\n";
    std::cout << "'sariq' mavjudmi: " << (trie.search("sariq") ? "Ha" : "Yo'q") << "\n";
    std::cout << "'olma' mavjudmi: " << (trie.search("olma") ? "Ha" : "Yo'q") << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
Trie daraxti so'zlarni belgilar bo'yicha ketma-ket saqlaydi. So'z qidirish va qo'shish vaqti so'z uzunligiga L proporsional: O(L).

## Ishlash natijasi:
```text
'salom' mavjudmi: Ha
'sam' mavjudmi: Yo'q
'sariq' mavjudmi: Ha
'olma' mavjudmi: Yo'q
```

# 858-Topshiriq: Trie - prefiks bo'yicha qidirish (startsWith) va prefiksli so'zlarni sanash
## Topshiriq sharti:
Trie klassini kengaytirib, berilgan prefiks bilan boshlanuvchi so'z borligini (`startsWith`) va shu prefiks bilan boshlanadigan so'zlar sonini hisoblovchi `countPrefix` metodini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

class AdvancedTrie {
private:
    struct Node {
        Node* children[26];
        int prefixCount;
        bool isEnd;
        Node() : prefixCount(0), isEnd(false) {
            for (int i = 0; i < 26; ++i) children[i] = nullptr;
        }
    };
    Node* root;

public:
    AdvancedTrie() { root = new Node(); }

    void insert(const std::string& word) {
        Node* curr = root;
        for (char c : word) {
            int idx = c - 'a';
            if (!curr->children[idx]) {
                curr->children[idx] = new Node();
            }
            curr = curr->children[idx];
            curr->prefixCount++;
        }
        curr->isEnd = true;
    }

    bool startsWith(const std::string& prefix) const {
        Node* curr = root;
        for (char c : prefix) {
            int idx = c - 'a';
            if (!curr->children[idx]) return false;
            curr = curr->children[idx];
        }
        return true;
    }

    int countPrefix(const std::string& prefix) const {
        Node* curr = root;
        for (char c : prefix) {
            int idx = c - 'a';
            if (!curr->children[idx]) return 0;
            curr = curr->children[idx];
        }
        return curr->prefixCount;
    }
};

int main() {
    AdvancedTrie trie;
    trie.insert("dastur");
    trie.insert("dasturchi");
    trie.insert("dasturlash");
    trie.insert("daftar");

    std::cout << "'dast' bilan boshlanuvchi bormi: " << (trie.startsWith("dast") ? "Ha" : "Yo'q") << "\n";
    std::cout << "'dast' prefiksli so'zlar soni: " << trie.countPrefix("dast") << "\n";
    std::cout << "'da' prefiksli so'zlar soni: " << trie.countPrefix("da") << "\n";
    std::cout << "'kitob' prefiksli so'zlar soni: " << trie.countPrefix("kitob") << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
Har bir tugunda `prefixCount` hisoblagichi saqlanadi. So'z qo'shilayotganda ushbu hisoblagich 1 ga oshirib boriladi, bu esa prefiks bilan boshlanuvchi so'zlar sonini O(L) da topishga imkon beradi.

## Ishlash natijasi:
```text
'dast' bilan boshlanuvchi bormi: Ha
'dast' prefiksli so'zlar soni: 3
'da' prefiksli so'zlar soni: 4
'kitob' prefiksli so'zlar soni: 0
```

# 859-Topshiriq: O'zaro kesishmaydigan to'plamlar (DSU / Disjoint Set Union)
## Topshiriq sharti:
Yo'lni qisqartirish (path compression) va o'lcham bo'yicha birlashtirish (union by rank) xususiyatlariga ega samarali `DisjointSet` klassini yarating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

class DSU {
private:
    std::vector<int> parent;
    std::vector<int> rank;

public:
    DSU(int n) : parent(n), rank(n, 0) {
        for (int i = 0; i < n; ++i) parent[i] = i;
    }

    int find(int i) {
        if (parent[i] == i) return i;
        return parent[i] = find(parent[i]); // Path compression
    }

    bool unite(int i, int j) {
        int rootI = find(i);
        int rootJ = find(j);
        if (rootI == rootJ) return false;

        // Union by rank
        if (rank[rootI] < rank[rootJ]) {
            parent[rootI] = rootJ;
        } else if (rank[rootI] > rank[rootJ]) {
            parent[rootJ] = rootI;
        } else {
            parent[rootJ] = rootI;
            rank[rootI]++;
        }
        return true;
    }

    bool isConnected(int i, int j) {
        return find(i) == find(j);
    }
};

int main() {
    DSU dsu(6);
    dsu.unite(0, 1);
    dsu.unite(1, 2);
    dsu.unite(3, 4);

    std::cout << "0 va 2 bog'langanmi: " << (dsu.isConnected(0, 2) ? "Ha" : "Yo'q") << "\n";
    std::cout << "0 va 3 bog'langanmi: " << (dsu.isConnected(0, 3) ? "Ha" : "Yo'q") << "\n";

    dsu.unite(2, 4);
    std::cout << "2 va 4 birlashtirilgach, 0 va 3 bog'langanmi: " << (dsu.isConnected(0, 3) ? "Ha" : "Yo'q") << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
DSU algoritmi qisqartirish va rank yordamida deyarli O(1) ammortizatsiyalangan vaqtda (Ackermann funksiyasining teskarisi alpha(N)) ishlaydi.

## Ishlash natijasi:
```text
0 va 2 bog'langanmi: Ha
0 va 3 bog'langanmi: Yo'q
2 va 4 birlashtirilgach, 0 va 3 bog'langanmi: Ha
```

# 860-Topshiriq: DSU yordamida yo'naltirilmagan grafda sikl borligini aniqlash
## Topshiriq sharti:
Grafdagi barcha qirralarni ko'rib chiqib, DSU yordamida yo'naltirilmagan grafda sikl (cycle) mavjud yoki yo'qligini aniqlovchi dastur yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

struct Edge {
    int u, v;
};

class DSU {
    std::vector<int> parent;
public:
    DSU(int n) : parent(n) {
        for (int i = 0; i < n; ++i) parent[i] = i;
    }
    int find(int x) {
        if (parent[x] == x) return x;
        return parent[x] = find(parent[x]);
    }
    bool unite(int x, int y) {
        int rx = find(x);
        int ry = find(y);
        if (rx == ry) return false; // Sikl topildi!
        parent[rx] = ry;
        return true;
    }
};

bool hasCycle(int n, const std::vector<Edge>& edges) {
    DSU dsu(n);
    for (const auto& edge : edges) {
        if (!dsu.unite(edge.u, edge.v)) {
            return true;
        }
    }
    return false;
}

int main() {
    int n = 4;
    std::vector<Edge> edges1 = {{0, 1}, {1, 2}, {2, 3}};
    std::cout << "1-grafda sikl bormi: " << (hasCycle(n, edges1) ? "Ha" : "Yo'q") << "\n";

    std::vector<Edge> edges2 = {{0, 1}, {1, 2}, {2, 3}, {3, 0}};
    std::cout << "2-grafda sikl bormi: " << (hasCycle(n, edges2) ? "Ha" : "Yo'q") << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
Agar qirraning ikki uchi allaqachon bir xil to'plamga (ildizga) tegishli bo'lsa, bu qirra ularni yana bog'laganda yopiq sikl hosil bo'ladi.

## Ishlash natijasi:
```text
1-grafda sikl bormi: Yo'q
2-grafda sikl bormi: Ha
```

# 861-Topshiriq: Grafni qo'shnilik ro'yxati (Adjacency List) orqali ifodalash
## Topshiriq sharti:
`Graph` sinfini yarating va unda tugunlar sonini, yo'naltirilgan va yo'naltirilmagan qirralar qo'shishni hamda butun grafni chiroyli chop etuvchi metodni yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

class Graph {
private:
    int V;
    std::vector<std::vector<int>> adj;
    bool isDirected;

public:
    Graph(int v, bool directed = false) : V(v), adj(v), isDirected(directed) {}

    void addEdge(int u, int v) {
        adj[u].push_back(v);
        if (!isDirected) {
            adj[v].push_back(u);
        }
    }

    void printGraph() const {
        for (int i = 0; i < V; ++i) {
            std::cout << "Tugun " << i << " qo'shnilari: ";
            for (int neighbor : adj[i]) {
                std::cout << neighbor << " ";
            }
            std::cout << "\n";
        }
    }
};

int main() {
    Graph g(4, false);
    g.addEdge(0, 1);
    g.addEdge(0, 2);
    g.addEdge(1, 2);
    g.addEdge(2, 3);

    std::cout << "Yo'naltirilmagan graf tuzilishi:\n";
    g.printGraph();

    return 0;
}
```

## Tushuntirish va Mantiq:
Qo'shnilik ro'yxati `vector<vector<int>>` xotirani O(V + E) da tejaydi va siyrak (sparse) graflar uchun matritsadan ancha afzaldir.

## Ishlash natijasi:
```text
Yo'naltirilmagan graf tuzilishi:
Tugun 0 qo'shnilari: 1 2 
Tugun 1 qo'shnilari: 0 2 
Tugun 2 qo'shnilari: 0 1 3 
Tugun 3 qo'shnilari: 2 
```

# 862-Topshiriq: Grafda Kenglik bo'yicha qidirish (BFS - Breadth First Search)
## Topshiriq sharti:
Graf bo'yicha boshlang'ich tugundan boshlab navbat (queue) orqali BFS qidiruvini amalga oshiring va tashrif buyurilgan tugunlar tartibini chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <queue>

void bfs(int start, const std::vector<std::vector<int>>& adj) {
    int n = adj.size();
    std::vector<bool> visited(n, false);
    std::queue<int> q;

    visited[start] = true;
    q.push(start);

    std::cout << "BFS tartibi: ";
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        std::cout << u << " ";

        for (int v : adj[u]) {
            if (!visited[v]) {
                visited[v] = true;
                q.push(v);
            }
        }
    }
    std::cout << "\n";
}

int main() {
    int V = 6;
    std::vector<std::vector<int>> adj(V);
    adj[0] = {1, 2};
    adj[1] = {0, 3, 4};
    adj[2] = {0, 4};
    adj[3] = {1, 5};
    adj[4] = {1, 2, 5};
    adj[5] = {3, 4};

    bfs(0, adj);

    return 0;
}
```

## Tushuntirish va Mantiq:
BFS har doim boshlang'ich tugundan qadam-baqadam kengayib boradi. Shu sababli vaznsiz graflarda u eng qisqa yo'lni kafolatlaydi. Vaqt murakkabligi: O(V + E).

## Ishlash natijasi:
```text
BFS tartibi: 0 1 2 3 4 5
```

# 863-Topshiriq: Grafda Chuqurlik bo'yicha qidirish (DFS - Depth First Search)
## Topshiriq sharti:
Grafda rekursiv DFS traversali algoritmini yarating. Har bir tugunga tashrif buyurilganida uning raqamini chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

void dfsHelper(int u, const std::vector<std::vector<int>>& adj, std::vector<bool>& visited) {
    visited[u] = true;
    std::cout << u << " ";

    for (int v : adj[u]) {
        if (!visited[v]) {
            dfsHelper(v, adj, visited);
        }
    }
}

void dfs(int start, const std::vector<std::vector<int>>& adj) {
    std::vector<bool> visited(adj.size(), false);
    std::cout << "DFS tartibi: ";
    dfsHelper(start, adj, visited);
    std::cout << "\n";
}

int main() {
    int V = 5;
    std::vector<std::vector<int>> adj(V);
    adj[0] = {1, 2};
    adj[1] = {0, 3};
    adj[2] = {0, 4};
    adj[3] = {1};
    adj[4] = {2};

    dfs(0, adj);

    return 0;
}
```

## Tushuntirish va Mantiq:
DFS rekursiv chaqiruv yoki stek yordamida iloji boricha chuqurroq kirib boradi va keyin orqaga qaytadi (backtracking). Vaqt murakkabligi: O(V + E).

## Ishlash natijasi:
```text
DFS tartibi: 0 1 3 2 4
```

# 864-Topshiriq: Bipartite (ikki ulushli) grafni tekshirish
## Topshiriq sharti:
Grafni ikkita rang (0 va 1) bilan bo'yash mumkinligini BFS yordamida tekshiruvchi `isBipartite` funksiyasini yozing (hech qaysi ikkita qo'shni tugun bir xil rangga ega bo'lmasligi kerak).

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <queue>

bool isBipartite(const std::vector<std::vector<int>>& adj) {
    int n = adj.size();
    std::vector<int> color(n, -1);

    for (int start = 0; start < n; ++start) {
        if (color[start] != -1) continue;

        std::queue<int> q;
        q.push(start);
        color[start] = 0;

        while (!q.empty()) {
            int u = q.front();
            q.pop();

            for (int v : adj[u]) {
                if (color[v] == -1) {
                    color[v] = 1 - color[u];
                    q.push(v);
                } else if (color[v] == color[u]) {
                    return false; // Bir xil rangdagi qo'shnilar
                }
            }
        }
    }
    return true;
}

int main() {
    // 4 ta tugunli kvadrat: 0-1-2-3-0 (Ikki ulushli)
    std::vector<std::vector<int>> graph1 = {{1, 3}, {0, 2}, {1, 3}, {0, 2}};
    std::cout << "1-graf bipartite: " << (isBipartite(graph1) ? "Ha" : "Yo'q") << "\n";

    // Uchburchak: 0-1-2-0 (Toq siklli, bipartite emas)
    std::vector<std::vector<int>> graph2 = {{1, 2}, {0, 2}, {0, 1}};
    std::cout << "2-graf bipartite: " << (isBipartite(graph2) ? "Ha" : "Yo'q") << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
Graf bipartite bo'lishi uchun uning tarkibida toq uzunlikdagi sikl bo'lmasligi zarur va yetarli. 2 ta rang berish algoritmi buni O(V + E) da tekshiradi.

## Ishlash natijasi:
```text
1-graf bipartite: Ha
2-graf bipartite: Yo'q
```

# 865-Topshiriq: Yo'naltirilgan grafda siklni aniqlash (DFS 3 xil rangli holat)
## Topshiriq sharti:
Yo'naltirilgan grafda orqaga yo'naltirilgan qirra (back edge) borligini 3 ta holat (0: tashrif buyurilmagan, 1: joriy rekursiya yo'lida, 2: to'liq yakunlangan) orqali aniqlovchi dastur yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

bool dfsCycle(int u, const std::vector<std::vector<int>>& adj, std::vector<int>& state) {
    state[u] = 1; // Joriy zanjirda

    for (int v : adj[u]) {
        if (state[v] == 1) return true; // Sikl topildi (orqaga qirra)
        if (state[v] == 0 && dfsCycle(v, adj, state)) return true;
    }

    state[u] = 2; // Qayta ishlandi
    return false;
}

bool hasDirectedCycle(int n, const std::vector<std::vector<int>>& adj) {
    std::vector<int> state(n, 0);
    for (int i = 0; i < n; ++i) {
        if (state[i] == 0) {
            if (dfsCycle(i, adj, state)) return true;
        }
    }
    return false;
}

int main() {
    int V = 3;
    // 0 -> 1 -> 2 -> 0 (Sikl bor)
    std::vector<std::vector<int>> g1(V);
    g1[0].push_back(1);
    g1[1].push_back(2);
    g1[2].push_back(0);

    std::cout << "G1 da sikl bormi: " << (hasDirectedCycle(V, g1) ? "Ha" : "Yo'q") << "\n";

    // 0 -> 1 -> 2 (Sikl yo'q - DAG)
    std::vector<std::vector<int>> g2(V);
    g2[0].push_back(1);
    g2[1].push_back(2);

    std::cout << "G2 da sikl bormi: " << (hasDirectedCycle(V, g2) ? "Ha" : "Yo'q") << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
Tugunning holati 1 bo'lganda unga qayta duch kelsak, bu joriy rekursiya stakidagi tugunga olib boruvchi sikl ekanligini bildiradi.

## Ishlash natijasi:
```text
G1 da sikl bormi: Ha
G2 da sikl bormi: Yo'q
```

# 866-Topshiriq: Topologik saralash - Kahn algoritmi (In-degree BFS)
## Topshiriq sharti:
Yo'naltirilgan asiklik grafda (DAG) kirish darajalari (in-degree) va navbat (queue) yordamida topologik saralashni (Kahn algoritmi) amalga oshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <queue>

std::vector<int> topologicalSortKahn(int n, const std::vector<std::vector<int>>& adj) {
    std::vector<int> inDegree(n, 0);
    for (int u = 0; u < n; ++u) {
        for (int v : adj[u]) {
            inDegree[v]++;
        }
    }

    std::queue<int> q;
    for (int i = 0; i < n; ++i) {
        if (inDegree[i] == 0) q.push(i);
    }

    std::vector<int> result;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        result.push_back(u);

        for (int v : adj[u]) {
            inDegree[v]--;
            if (inDegree[v] == 0) {
                q.push(v);
            }
        }
    }

    if (result.size() != n) {
        std::cout << "Grafda sikl mavjud! Topologik tartib mavjud emas.\n";
        return {};
    }
    return result;
}

int main() {
    int V = 6;
    std::vector<std::vector<int>> adj(V);
    // Masalan: 5->2, 5->0, 4->0, 4->1, 2->3, 3->1
    adj[5].push_back(2);
    adj[5].push_back(0);
    adj[4].push_back(0);
    adj[4].push_back(1);
    adj[2].push_back(3);
    adj[3].push_back(1);

    auto order = topologicalSortKahn(V, adj);
    std::cout << "Kahn algoritmi bo'yicha tartib: ";
    for (int node : order) std::cout << node << " ";
    std::cout << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
Kahn algoritmi har doim kirish darajasi (in-degree) 0 bo'lgan tugunlarni navbatga oladi va ularning chiquvchi qirralarini olib tashlaydi. Agar natijadagi tugunlar soni V dan kam bo'lsa, grafda sikl bor.

## Ishlash natijasi:
```text
Kahn algoritmi bo'yicha tartib: 4 5 2 0 3 1
```

# 867-Topshiriq: Topologik saralash - DFS va Stek yordamida
## Topshiriq sharti:
DAG grafida DFS qidiruvidan foydalanib va tugunlar ishlanib bo'lingach ularni stekka (stack) qo'shish orqali topologik saralashni amalga oshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <stack>

void dfsTopSort(int u, const std::vector<std::vector<int>>& adj, std::vector<bool>& visited, std::stack<int>& st) {
    visited[u] = true;
    for (int v : adj[u]) {
        if (!visited[v]) {
            dfsTopSort(v, adj, visited, st);
        }
    }
    st.push(u); // Barcha qo'shnilari tugagach, stekka solinadi
}

std::vector<int> topologicalSortDFS(int n, const std::vector<std::vector<int>>& adj) {
    std::vector<bool> visited(n, false);
    std::stack<int> st;

    for (int i = 0; i < n; ++i) {
        if (!visited[i]) {
            dfsTopSort(i, adj, visited, st);
        }
    }

    std::vector<int> result;
    while (!st.empty()) {
        result.push_back(st.top());
        st.pop();
    }
    return result;
}

int main() {
    int V = 6;
    std::vector<std::vector<int>> adj(V);
    adj[5].push_back(2);
    adj[5].push_back(0);
    adj[4].push_back(0);
    adj[4].push_back(1);
    adj[2].push_back(3);
    adj[3].push_back(1);

    auto res = topologicalSortDFS(V, adj);
    std::cout << "DFS topologik tartib: ";
    for (int x : res) std::cout << x << " ";
    std::cout << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
DFS da tugunning barcha bolalari to'liq qayta ishlangach, u stekka kiritiladi. Stekdan chiqarilganda esa eng boshlang'ich bog'liqliklar birinchi chiqadi.

## Ishlash natijasi:
```text
DFS topologik tartib: 5 4 2 3 1 0
```

# 868-Topshiriq: Dikshtra algoritmi (Dijkstra) - priority_queue yordamida
## Topshiriq sharti:
Og'irliklari musbat bo'lgan grafda boshlang'ich cho'qqidan barcha cho'qqilargacha eng qisqa masofalarni topuvchi Dijkstra algoritmini `std::priority_queue` yordamida yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <queue>

const int INF = 1e9;

struct Edge {
    int to;
    int weight;
};

std::vector<int> dijkstra(int start, int n, const std::vector<std::vector<Edge>>& adj) {
    std::vector<int> dist(n, INF);
    // min-heap: juftlik (masofa, tugun)
    std::priority_queue<std::pair<int, int>, std::vector<std::pair<int, int>>, std::greater<std::pair<int, int>>> pq;

    dist[start] = 0;
    pq.push({0, start});

    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();

        if (d > dist[u]) continue;

        for (const auto& edge : adj[u]) {
            int v = edge.to;
            int w = edge.weight;

            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}

int main() {
    int V = 5;
    std::vector<std::vector<Edge>> adj(V);
    adj[0].push_back({1, 4});
    adj[0].push_back({2, 1});
    adj[2].push_back({1, 2});
    adj[1].push_back({3, 1});
    adj[2].push_back({3, 5});
    adj[3].push_back({4, 3});

    auto distances = dijkstra(0, V, adj);
    for (int i = 0; i < V; ++i) {
        std::cout << "0 dan " << i << " gacha eng qisqa yo'l: " << distances[i] << "\n";
    }

    return 0;
}
```

## Tushuntirish va Mantiq:
Min-heap (priority_queue) har qadamda eng yaqin masofadagi tugunni O(log V) da tanlaydi. Butun algoritm O((V + E) log V) vaqtda ishlaydi.

## Ishlash natijasi:
```text
0 dan 0 gacha eng qisqa yo'l: 0
0 dan 1 gacha eng qisqa yo'l: 3
0 dan 2 gacha eng qisqa yo'l: 1
0 dan 3 gacha eng qisqa yo'l: 4
0 dan 4 gacha eng qisqa yo'l: 7
```

# 869-Topshiriq: Bellman-Ford algoritmi - manfiy og'irlikdagi qirralar va siklni aniqlash
## Topshiriq sharti:
Grafdagi qirralar ro'yxati asosida boshlang'ich tugundan masofalarni hisoblovchi va manfiy og'irlikdagi sikl (negative weight cycle) borligini tekshiruvchi Bellman-Ford algoritmini tuzing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

const int INF = 1e9;

struct Edge {
    int u, v, w;
};

bool bellmanFord(int start, int n, const std::vector<Edge>& edges, std::vector<int>& dist) {
    dist.assign(n, INF);
    dist[start] = 0;

    // V - 1 marta barcha qirralarni relaksatsiya qilamiz
    for (int i = 1; i <= n - 1; ++i) {
        for (const auto& e : edges) {
            if (dist[e.u] != INF && dist[e.u] + e.w < dist[e.v]) {
                dist[e.v] = dist[e.u] + e.w;
            }
        }
    }

    // V-chi qadam: agar yana qisqarsa, manfiy sikl mavjud
    for (const auto& e : edges) {
        if (dist[e.u] != INF && dist[e.u] + e.w < dist[e.v]) {
            return false; // Manfiy sikl bor
        }
    }
    return true;
}

int main() {
    int V = 4;
    std::vector<Edge> edges = {
        {0, 1, 4},
        {0, 2, 5},
        {1, 2, -2},
        {2, 3, 3},
        {3, 1, 1}
    };

    std::vector<int> dist;
    if (bellmanFord(0, V, edges, dist)) {
        std::cout << "0 dan masofalar: ";
        for (int i = 0; i < V; ++i) std::cout << dist[i] << " ";
        std::cout << "\n";
    } else {
        std::cout << "Grafda manfiy sikl topildi!\n";
    }

    return 0;
}
```

## Tushuntirish va Mantiq:
Bellman-Ford barcha qirralarni V-1 marta tekshiradi. O(V * E) murakkablikka ega va Dikshtradan farqli ravishda manfiy vaznlar bilan xatosiz ishlay oladi.

## Ishlash natijasi:
```text
0 dan masofalar: 0 4 2 5 
```

# 870-Topshiriq: Floyd-Warshall algoritmi - barcha juftliklar orasidagi eng qisqa yo'l
## Topshiriq sharti:
O(V^3) vaqtda barcha tugun juftliklari `(i, j)` orasidagi eng qisqa masofalar matritsasini hisoblovchi Floyd-Warshall algoritmini yarating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

const int INF = 1e8;

void floydWarshall(int n, std::vector<std::vector<int>>& dist) {
    for (int k = 0; k < n; ++k) {
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                if (dist[i][k] < INF && dist[k][j] < INF) {
                    dist[i][j] = std::min(dist[i][j], dist[i][k] + dist[k][j]);
                }
            }
        }
    }
}

int main() {
    int V = 4;
    std::vector<std::vector<int>> dist = {
        {0,   3,   INF, 7},
        {8,   0,   2,   INF},
        {5,   INF, 0,   1},
        {2,   INF, INF, 0}
    };

    floydWarshall(V, dist);

    std::cout << "Eng qisqa masofalar matritsasi:\n";
    for (int i = 0; i < V; ++i) {
        for (int j = 0; j < V; ++j) {
            if (dist[i][j] == INF) std::cout << "INF ";
            else std::cout << dist[i][j] << "   ";
        }
        std::cout << "\n";
    }

    return 0;
}
```

## Tushuntirish va Mantiq:
Floyd-Warshall dinamik dasturlash tamoyili asosida ishlaydi: har bir oraliq `k` tugunini ko'rib chiqib, `i -> k -> j` yo'li to'g'ridan-to'g'ri `i -> j` dan qisqaroq ekanini tekshiradi.

## Ishlash natijasi:
```text
Eng qisqa masofalar matritsasi:
0   3   5   6   
5   0   2   3   
3   6   0   1   
2   5   7   0   
```

# 871-Topshiriq: Kruskal algoritmi - Minimal Qamrovchi Daraxt (MST) va DSU
## Topshiriq sharti:
Grafning barcha qirralarini og'irligi bo'yicha saralab, DSU yordamida siklsiz eng arzon daraxtni (MST) quruvchi Kruskal algoritmini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

struct Edge {
    int u, v, weight;
    bool operator<(const Edge& other) const {
        return weight < other.weight;
    }
};

class DSU {
    std::vector<int> parent;
public:
    DSU(int n) : parent(n) {
        for (int i = 0; i < n; ++i) parent[i] = i;
    }
    int find(int x) {
        return parent[x] == x ? x : parent[x] = find(parent[x]);
    }
    bool unite(int x, int y) {
        int rx = find(x), ry = find(y);
        if (rx == ry) return false;
        parent[rx] = ry;
        return true;
    }
};

int kruskal(int n, std::vector<Edge>& edges) {
    std::sort(edges.begin(), edges.end());
    DSU dsu(n);
    int mstCost = 0;
    int edgesCount = 0;

    for (const auto& e : edges) {
        if (dsu.unite(e.u, e.v)) {
            mstCost += e.weight;
            edgesCount++;
            if (edgesCount == n - 1) break;
        }
    }
    return mstCost;
}

int main() {
    int V = 4;
    std::vector<Edge> edges = {
        {0, 1, 10},
        {0, 2, 6},
        {0, 3, 5},
        {1, 3, 15},
        {2, 3, 4}
    };

    std::cout << "Minimal qamrovchi daraxt vazni (Kruskal): " << kruskal(V, edges) << std::endl;

    return 0;
}
```

## Tushuntirish va Mantiq:
Kruskal algoritmi ochko'z (greedy) strategiyaga tayanadi: eng yengil qirralarni navbat bilan olib, DSU orqali sikl hosil qilmasligini kafolatlaydi. Vaqt murakkabligi: O(E log E).

## Ishlash natijasi:
```text
Minimal qamrovchi daraxt vazni (Kruskal): 19
```

# 872-Topshiriq: Prim algoritmi - Minimal Qamrovchi Daraxt (MST) priority_queue bilan
## Topshiriq sharti:
Ixtiyoriy cho'qqidan boshlab, eng yaqin qo'shni qirrani tanlab boruvchi Prim algoritmini priority_queue yordamida amalga oshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <queue>

struct Edge {
    int to, weight;
};

int prim(int n, const std::vector<std::vector<Edge>>& adj) {
    std::vector<bool> inMST(n, false);
    // (weight, node)
    std::priority_queue<std::pair<int, int>, std::vector<std::pair<int, int>>, std::greater<std::pair<int, int>>> pq;

    int totalCost = 0;
    pq.push({0, 0});

    while (!pq.empty()) {
        auto [w, u] = pq.top();
        pq.pop();

        if (inMST[u]) continue;
        inMST[u] = true;
        totalCost += w;

        for (const auto& e : adj[u]) {
            if (!inMST[e.to]) {
                pq.push({e.weight, e.to});
            }
        }
    }
    return totalCost;
}

int main() {
    int V = 4;
    std::vector<std::vector<Edge>> adj(V);
    adj[0].push_back({1, 10}); adj[1].push_back({0, 10});
    adj[0].push_back({2, 6});  adj[2].push_back({0, 6});
    adj[0].push_back({3, 5});  adj[3].push_back({0, 5});
    adj[1].push_back({3, 15}); adj[3].push_back({1, 15});
    adj[2].push_back({3, 4});  adj[3].push_back({2, 4});

    std::cout << "MST vazni (Prim): " << prim(V, adj) << std::endl;

    return 0;
}
```

## Tushuntirish va Mantiq:
Prim algoritmi zich graflar (dense graphs) uchun juda qulay bo'lib, daraxtni bosqichma-bosqich bitta umumiy tugundan o'stirib boradi. Vaqti: O(E log V).

## Ishlash natijasi:
```text
MST vazni (Prim): 19
```

# 873-Topshiriq: Dinamik dasturlash (DP) - Fibonachchi: Memoizatsiya va Tabulyatsiya
## Topshiriq sharti:
N-chi Fibonachchi sonini yuqoridan-pastga (top-down memoization) va pastdan-yuqoriga (bottom-up tabulation O(1) xotira) usullari bilan hisoblovchi dastur yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

long long fibMemo(int n, std::vector<long long>& memo) {
    if (n <= 1) return n;
    if (memo[n] != -1) return memo[n];
    return memo[n] = fibMemo(n - 1, memo) + fibMemo(n - 2, memo);
}

long long fibTabulation(int n) {
    if (n <= 1) return n;
    long long prev2 = 0, prev1 = 1, curr = 0;
    for (int i = 2; i <= n; ++i) {
        curr = prev1 + prev2;
        prev2 = prev1;
        prev1 = curr;
    }
    return curr;
}

int main() {
    int n = 40;
    std::vector<long long> memo(n + 1, -1);

    std::cout << "Fibonacci(" << n << ") Memoization: " << fibMemo(n, memo) << std::endl;
    std::cout << "Fibonacci(" << n << ") Tabulation: " << fibTabulation(n) << std::endl;

    return 0;
}
```

## Tushuntirish va Mantiq:
Eksponentsial O(2^N) vaqt oluvchi oddiy rekursiya oraliq natijalarni eslab qolish (memoization) orqali chiziqli O(N) ga tushiriladi. Tabulyatsiyada esa xotira O(1) ga kamaytiriladi.

## Ishlash natijasi:
```text
Fibonacci(40) Memoization: 102334155
Fibonacci(40) Tabulation: 102334155
```

# 874-Topshiriq: DP - 0/1 Ryukzak (Knapsack) masalasi
## Topshiriq sharti:
Og'irligi `W` bo'lgan ryukzakka har bir buyumni ko'pi bilan bir marta olgan holda maksimal qiymatni to'plash algoritmini 2D va 1D xotirali DP orqali yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int knapsack01(int W, const std::vector<int>& weights, const std::vector<int>& values) {
    int n = weights.size();
    std::vector<int> dp(W + 1, 0);

    for (int i = 0; i < n; ++i) {
        for (int w = W; w >= weights[i]; --w) {
            dp[w] = std::max(dp[w], dp[w - weights[i]] + values[i]);
        }
    }
    return dp[W];
}

int main() {
    int W = 50; // Ryukzak sig'imi
    std::vector<int> values  = {60, 100, 120};
    std::vector<int> weights = {10, 20, 30};

    int maxVal = knapsack01(W, weights, values);
    std::cout << "Maksimal to'plangan qiymat: " << maxVal << std::endl;

    return 0;
}
```

## Tushuntirish va Mantiq:
1D optimallashtirishda ichki sikl `W` dan `weights[i]` gacha teskari yuradi, bu esa ayni bir buyumning ayni qadamda takroran olinishining oldini oladi. Vaqt: O(N * W).

## Ishlash natijasi:
```text
Maksimal to'plangan qiymat: 220
```

# 875-Topshiriq: DP - Eng uzun umumiy qism ketma-ketlik (LCS)
## Topshiriq sharti:
Ikkita satr berilganda ularning eng uzun umumiy qism ketma-ketligi (Longest Common Subsequence) uzunligini hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

int longestCommonSubsequence(const std::string& text1, const std::string& text2) {
    int m = text1.size();
    int n = text2.size();
    std::vector<std::vector<int>> dp(m + 1, std::vector<int>(n + 1, 0));

    for (int i = 1; i <= m; ++i) {
        for (int j = 1; j <= n; ++j) {
            if (text1[i - 1] == text2[j - 1]) {
                dp[i][j] = 1 + dp[i - 1][j - 1];
            } else {
                dp[i][j] = std::max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }
    return dp[m][n];
}

int main() {
    std::string s1 = "abcde";
    std::string s2 = "ace";
    std::cout << "LCS uzunligi: " << longestCommonSubsequence(s1, s2) << std::endl;

    std::string s3 = "algorithm";
    std::string s4 = "altruistic";
    std::cout << "LCS uzunligi: " << longestCommonSubsequence(s3, s4) << std::endl;

    return 0;
}
```

## Tushuntirish va Mantiq:
Agar belgilar teng bo'lsa `dp[i-1][j-1] + 1`, aks holda chap yoki yuqori katakdagi maksimum qiymat olinadi. Vaqt va xotira murakkabligi: O(M * N).

## Ishlash natijasi:
```text
LCS uzunligi: 3
LCS uzunligi: 5
```

# 876-Topshiriq: DP - Eng uzun o'suvchi qism ketma-ketlik (LIS) O(N log N)
## Topshiriq sharti:
Massivning eng uzun qat'iy o'suvchi qism ketma-ketligini `std::lower_bound` ikkilik qidiruv bilan O(N log N) vaqtda hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int lengthOfLIS(const std::vector<int>& nums) {
    std::vector<int> tails;

    for (int x : nums) {
        auto it = std::lower_bound(tails.begin(), tails.end(), x);
        if (it == tails.end()) {
            tails.push_back(x);
        } else {
            *it = x;
        }
    }
    return tails.size();
}

int main() {
    std::vector<int> nums = {10, 9, 2, 5, 3, 7, 101, 18};
    std::cout << "LIS uzunligi: " << lengthOfLIS(nums) << std::endl;

    std::vector<int> nums2 = {0, 1, 0, 3, 2, 3};
    std::cout << "LIS uzunligi: " << lengthOfLIS(nums2) << std::endl;

    return 0;
}
```

## Tushuntirish va Mantiq:
Oddiy DP usuli O(N^2) bo'lsa, `tails` massivi va binary search yordamida Patience Sorting tamoyili orqali masala O(N log N) da yechiladi.

## Ishlash natijasi:
```text
LIS uzunligi: 4
LIS uzunligi: 4
```

# 877-Topshiriq: DP - Tangalar almashtirish (Coin Change) - Minimal tangalar soni
## Topshiriq sharti:
Berilgan tangalar nominalidan foydalanib belgilangan `amount` summani hosil qilish uchun eng kam tangalar sonini toping. Agar imkonsiz bo'lsa, -1 qaytaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int coinChange(const std::vector<int>& coins, int amount) {
    std::vector<int> dp(amount + 1, amount + 1);
    dp[0] = 0;

    for (int i = 1; i <= amount; ++i) {
        for (int coin : coins) {
            if (i >= coin) {
                dp[i] = std::min(dp[i], dp[i - coin] + 1);
            }
        }
    }
    return dp[amount] > amount ? -1 : dp[amount];
}

int main() {
    std::vector<int> coins = {1, 2, 5};
    int amount = 11;
    std::cout << "11 summani hosil qilish uchun minimal tangalar: " << coinChange(coins, amount) << std::endl;

    std::vector<int> coins2 = {2};
    std::cout << "3 summani hosil qilish uchun minimal tangalar: " << coinChange(coins2, 3) << std::endl;

    return 0;
}
```

## Tushuntirish va Mantiq:
Har bir `i` summa uchun barcha mos keluvchi tangalar sinab ko'riladi: `dp[i] = min(dp[i], dp[i - coin] + 1)`. Vaqt: O(amount * |coins|).

## Ishlash natijasi:
```text
11 summani hosil qilish uchun minimal tangalar: 3
3 summani hosil qilish uchun minimal tangalar: -1
```

# 878-Topshiriq: DP - Tangalar almashtirish - Usullar soni (Coin Change II)
## Topshiriq sharti:
Berilgan tangalar nominalidan foydalanib berilgan summani hosil qilishning barcha turlicha kombinatsiyalari (kombinatsiya tartibi muhim emas) sonini hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int changeWays(int amount, const std::vector<int>& coins) {
    std::vector<int> dp(amount + 1, 0);
    dp[0] = 1; // 0 summani hosil qilishning 1 ta usuli bor (hech narsa olmaslik)

    for (int coin : coins) {
        for (int i = coin; i <= amount; ++i) {
            dp[i] += dp[i - coin];
        }
    }
    return dp[amount];
}

int main() {
    int amount = 5;
    std::vector<int> coins = {1, 2, 5};
    std::cout << "5 summani hosil qilish kombinatsiyalari soni: " << changeWays(amount, coins) << std::endl;

    return 0;
}
```

## Tushuntirish va Mantiq:
Permutatsiyalar emas, faqat kombinatsiyalarni hisoblash uchun tashqi sikl bo'yicha tangalar, ichki sikl bo'yicha summalar yuritiladi.

## Ishlash natijasi:
```text
5 summani hosil qilish kombinatsiyalari soni: 4
```

# 879-Topshiriq: DP - Tahrirlash masofasi (Levenshtein Edit Distance)
## Topshiriq sharti:
Bitta satrni ikkinchisiga aylantirish uchun zarur bo'lgan minimal amallar sonini (belgi qo'shish, o'chirish, almashtirish) toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

int minDistance(const std::string& word1, const std::string& word2) {
    int m = word1.size();
    int n = word2.size();
    std::vector<std::vector<int>> dp(m + 1, std::vector<int>(n + 1, 0));

    for (int i = 0; i <= m; ++i) dp[i][0] = i;
    for (int j = 0; j <= n; ++j) dp[0][j] = j;

    for (int i = 1; i <= m; ++i) {
        for (int j = 1; j <= n; ++j) {
            if (word1[i - 1] == word2[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1];
            } else {
                dp[i][j] = 1 + std::min({
                    dp[i - 1][j],    // o'chirish
                    dp[i][j - 1],    // qo'shish
                    dp[i - 1][j - 1] // almashtirish
                });
            }
        }
    }
    return dp[m][n];
}

int main() {
    std::string w1 = "horse", w2 = "ros";
    std::cout << "'horse' -> 'ros' tahrirlash masofasi: " << minDistance(w1, w2) << std::endl;

    std::string w3 = "intention", w4 = "execution";
    std::cout << "'intention' -> 'execution' tahrirlash masofasi: " << minDistance(w3, w4) << std::endl;

    return 0;
}
```

## Tushuntirish va Mantiq:
Klassik Levenshtein masofasi dinamik jadvali har bir qadamda 3 ta tahrirlash amalini baholaydi va ularning eng kichigiga 1 qo'shadi.

## Ishlash natijasi:
```text
'horse' -> 'ros' tahrirlash masofasi: 3
'intention' -> 'execution' tahrirlash masofasi: 5
```

# 880-Topshiriq: DP - Maksimal qism massiv yig'indisi (Kadane algoritmi)
## Topshiriq sharti:
Musbat va manfiy sonlardan iborat massivda ketma-ket kelgan qism massivning maksimal yig'indisini O(N) vaqt va O(1) xotirada hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int maxSubArray(const std::vector<int>& nums) {
    int currentSum = nums[0];
    int maxSum = nums[0];

    for (size_t i = 1; i < nums.size(); ++i) {
        currentSum = std::max(nums[i], currentSum + nums[i]);
        maxSum = std::max(maxSum, currentSum);
    }
    return maxSum;
}

int main() {
    std::vector<int> arr = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
    std::cout << "Maksimal qism massiv yig'indisi: " << maxSubArray(arr) << std::endl;

    std::vector<int> arr2 = {5, 4, -1, 7, 8};
    std::cout << "Maksimal qism massiv yig'indisi: " << maxSubArray(arr2) << std::endl;

    return 0;
}
```

## Tushuntirish va Mantiq:
Kadane algoritmi dinamik qoidasi: `currentSum = max(nums[i], currentSum + nums[i])`. Agar avvalgi yig'indi manfiy bo'lsa, uni tashlab yangi elementdan boshlash afzalroq bo'ladi.

## Ishlash natijasi:
```text
Maksimal qism massiv yig'indisi: 6
Maksimal qism massiv yig'indisi: 23
```

# 881-Topshiriq: DP - Zinapoyaga chiqish (Climbing Stairs)
## Topshiriq sharti:
N ta pog'onadan iborat zinapoyaning eng tepasiga chiqish kerak. Har bir qadamda 1 yoki 2 ta pog'ona bosib o'tish mumkin bo'lsa, jami necha xil usul bilan chiqish mumkinligini hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int climbStairs(int n) {
    if (n <= 2) return n;
    int a = 1, b = 2, c = 0;
    for (int i = 3; i <= n; ++i) {
        c = a + b;
        a = b;
        b = c;
    }
    return b;
}

int main() {
    for (int i = 1; i <= 6; ++i) {
        std::cout << i << " pog'ona uchun usullar soni: " << climbStairs(i) << "\n";
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
Zinapoyaga chiqish muammosi Fibonachchi ketma-ketligiga mos keladi: `f(n) = f(n-1) + f(n-2)`. Vaqt: O(N), xotira: O(1).

## Ishlash natijasi:
```text
1 pog'ona uchun usullar soni: 1
2 pog'ona uchun usullar soni: 2
3 pog'ona uchun usullar soni: 3
4 pog'ona uchun usullar soni: 5
5 pog'ona uchun usullar soni: 8
6 pog'ona uchun usullar soni: 13
```

# 882-Topshiriq: DP - Matritsada minimal yo'l yig'indisi (Min Path Sum)
## Topshiriq sharti:
M x N o'lchamli to'rning yuqori chap burchagidan quyi o'ng burchagiga faqat o'ngga va pastga harakatlanib borishdagi eng kichik sonlar yig'indisini toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int minPathSum(const std::vector<std::vector<int>>& grid) {
    int m = grid.size();
    int n = grid[0].size();
    std::vector<std::vector<int>> dp(m, std::vector<int>(n, 0));

    dp[0][0] = grid[0][0];
    for (int j = 1; j < n; ++j) dp[0][j] = dp[0][j - 1] + grid[0][j];
    for (int i = 1; i < m; ++i) dp[i][0] = dp[i - 1][0] + grid[i][0];

    for (int i = 1; i < m; ++i) {
        for (int j = 1; j < n; ++j) {
            dp[i][j] = grid[i][j] + std::min(dp[i - 1][j], dp[i][j - 1]);
        }
    }
    return dp[m - 1][n - 1];
}

int main() {
    std::vector<std::vector<int>> grid = {
        {1, 3, 1},
        {1, 5, 1},
        {4, 2, 1}
    };

    std::cout << "Minimal yo'l yig'indisi: " << minPathSum(grid) << std::endl;

    return 0;
}
```

## Tushuntirish va Mantiq:
Har bir `(i, j)` katakka faqat yuqoridan yoki chapdan kelish mumkin. Shuning uchun `dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])` formulasi qo'llaniladi.

## Ishlash natijasi:
```text
Minimal yo'l yig'indisi: 7
```

# 883-Topshiriq: DP - Matritsalarni ko'paytirish zanjiri (Matrix Chain Multiplication)
## Topshiriq sharti:
O'lchamlari berilgan bir qator matritsalarni ko'paytirishda amallar sonini minimallashtirish uchun qavslarni eng maqbul qo'yishdagi minimal skalyar ko'paytirishlar sonini toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <climits>
#include <algorithm>

int matrixChainOrder(const std::vector<int>& p) {
    int n = p.size() - 1; // Matritsalar soni
    std::vector<std::vector<int>> m(n + 1, std::vector<int>(n + 1, 0));

    // L - zanjir uzunligi (2 dan n gacha)
    for (int L = 2; L <= n; ++L) {
        for (int i = 1; i <= n - L + 1; ++i) {
            int j = i + L - 1;
            m[i][j] = INT_MAX;
            for (int k = i; k <= j - 1; ++k) {
                int q = m[i][k] + m[k + 1][j] + p[i - 1] * p[k] * p[j];
                if (q < m[i][j]) {
                    m[i][j] = q;
                }
            }
        }
    }
    return m[1][n];
}

int main() {
    // Matritsalar o'lchamlari: A1(10x30), A2(30x5), A3(5x60)
    std::vector<int> arr = {10, 30, 5, 60};
    std::cout << "Minimal amallar soni: " << matrixChainOrder(arr) << std::endl;

    return 0;
}
```

## Tushuntirish va Mantiq:
Klassik oraliq DP (interval DP) muammosi. Har bir mumkin bo'lgan bo'linish nuqtasi `k` tekshirilib chiqiladi. Vaqt murakkabligi: O(N^3).

## Ishlash natijasi:
```text
Minimal amallar soni: 4500
```

# 884-Topshiriq: DP - Palindrom qism satrlar soni (Palindromic Substrings)
## Topshiriq sharti:
Berilgan satrda nechta palindrom qism satr mavjudligini dinamik dasturlash yoki markazdan kengayish (expand around center) usuli bilan hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

int countSubstrings(const std::string& s) {
    int n = s.size();
    int count = 0;

    auto expand = [&](int left, int right) {
        while (left >= 0 && right < n && s[left] == s[right]) {
            count++;
            left--;
            right++;
        }
    };

    for (int i = 0; i < n; ++i) {
        expand(i, i);     // Toq uzunlikdagi palindromlar markazi
        expand(i, i + 1); // Juft uzunlikdagi palindromlar markazi
    }
    return count;
}

int main() {
    std::string s1 = "abc";
    std::cout << "'abc' dagi palindromlar soni: " << countSubstrings(s1) << std::endl;

    std::string s2 = "aaa";
    std::cout << "'aaa' dagi palindromlar soni: " << countSubstrings(s2) << std::endl;

    return 0;
}
```

## Tushuntirish va Mantiq:
Har bir belgini va belgi oraliqlarini markaz deb olib tashqariga qarab kengayganda O(N^2) vaqtda va qo'shimcha O(1) xotirada barcha palindromlar sanaladi.

## Ishlash natijasi:
```text
'abc' dagi palindromlar soni: 3
'aaa' dagi palindromlar soni: 6
```

# 885-Topshiriq: Segmentlar daraxti (Segment Tree) - Oraliq yig'indisi (Range Sum Query)
## Topshiriq sharti:
N o'lchamli massiv ustida oraliq yig'indisini O(log N) da hisoblovchi `SegmentTree` klassini tuzing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

class SegmentTree {
private:
    int n;
    std::vector<int> tree;

    void build(const std::vector<int>& arr, int v, int tl, int tr) {
        if (tl == tr) {
            tree[v] = arr[tl];
        } else {
            int tm = (tl + tr) / 2;
            build(arr, 2 * v, tl, tm);
            build(arr, 2 * v + 1, tm + 1, tr);
            tree[v] = tree[2 * v] + tree[2 * v + 1];
        }
    }

    int query(int v, int tl, int tr, int l, int r) {
        if (l > r) return 0;
        if (l == tl && r == tr) return tree[v];
        int tm = (tl + tr) / 2;
        return query(2 * v, tl, tm, l, std::min(r, tm)) +
               query(2 * v + 1, tm + 1, tr, std::max(l, tm + 1), r);
    }

public:
    SegmentTree(const std::vector<int>& arr) {
        n = arr.size();
        tree.resize(4 * n, 0);
        build(arr, 1, 0, n - 1);
    }

    int query(int l, int r) {
        return query(1, 0, n - 1, l, r);
    }
};

int main() {
    std::vector<int> arr = {1, 3, 5, 7, 9, 11};
    SegmentTree st(arr);

    std::cout << "Sum[1..3] (3+5+7): " << st.query(1, 3) << std::endl;
    std::cout << "Sum[0..5] (barchasi): " << st.query(0, 5) << std::endl;

    return 0;
}
```

## Tushuntirish va Mantiq:
Segment daraxti massivni ikkiga bo'lib rekursiv saqlaydi va istalgan oraliqdagi yig'indini O(log N) vaqtda javoblaydi.

## Ishlash natijasi:
```text
Sum[1..3] (3+5+7): 15
Sum[0..5] (barchasi): 36
```

# 886-Topshiriq: Segment Tree - Bitta elementni yangilash (Point Update)
## Topshiriq sharti:
Segment daraxtiga bitta element qiymatini o'zgartirish (`update(pos, new_val)`) metodini qo'shing va oraliq yig'indisining to'g'ri yangilanishini namoyish eting.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

class SegmentTreeWithUpdate {
    int n;
    std::vector<int> tree;

    void update(int v, int tl, int tr, int pos, int new_val) {
        if (tl == tr) {
            tree[v] = new_val;
        } else {
            int tm = (tl + tr) / 2;
            if (pos <= tm) update(2 * v, tl, tm, pos, new_val);
            else update(2 * v + 1, tm + 1, tr, pos, new_val);
            tree[v] = tree[2 * v] + tree[2 * v + 1];
        }
    }

    int query(int v, int tl, int tr, int l, int r) {
        if (l > r) return 0;
        if (l == tl && r == tr) return tree[v];
        int tm = (tl + tr) / 2;
        return query(2 * v, tl, tm, l, std::min(r, tm)) +
               query(2 * v + 1, tm + 1, tr, std::max(l, tm + 1), r);
    }

public:
    SegmentTreeWithUpdate(int size) : n(size), tree(4 * size, 0) {}

    void update(int pos, int val) { update(1, 0, n - 1, pos, val); }
    int query(int l, int r) { return query(1, 0, n - 1, l, r); }
};

int main() {
    SegmentTreeWithUpdate st(5);
    st.update(0, 2);
    st.update(1, 4);
    st.update(2, 6);
    st.update(3, 8);
    st.update(4, 10);

    std::cout << "Oraliq summasi [1..3]: " << st.query(1, 3) << std::endl;
    st.update(2, 100); // 2-indeksdagi 6 ni 100 ga o'zgartiramiz
    std::cout << "2-indeks 100 ga yangilangach [1..3]: " << st.query(1, 3) << std::endl;

    return 0;
}
```

## Tushuntirish va Mantiq:
Yangi qiymat kiritilganda daraxtning ildizigacha bo'lgan O(log N) ta tugun yangilanadi. Bu juda yuqori unumdorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Oraliq summasi [1..3]: 18
2-indeks 100 ga yangilangach [1..3]: 112
```

# 887-Topshiriq: Fenvik daraxti (Fenwick Tree / Binary Indexed Tree)
## Topshiriq sharti:
Segment daraxtiga qaraganda kamroq xotira (atigi O(N)) talab qiluvchi va bit amallari `i += (i & -i)` asosida ishlovchi Fenwick daraxtini quring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

class FenwickTree {
private:
    int n;
    std::vector<int> bit;

public:
    FenwickTree(int size) : n(size), bit(size + 1, 0) {}

    void add(int idx, int delta) {
        idx++; // 1-indekslangan
        for (; idx <= n; idx += idx & -idx) {
            bit[idx] += delta;
        }
    }

    int prefixSum(int idx) const {
        idx++;
        int sum = 0;
        for (; idx > 0; idx -= idx & -idx) {
            sum += bit[idx];
        }
        return sum;
    }

    int rangeSum(int l, int r) const {
        return prefixSum(r) - (l > 0 ? prefixSum(l - 1) : 0);
    }
};

int main() {
    std::vector<int> arr = {3, 2, -1, 6, 5, 4, -3, 3};
    FenwickTree ft(arr.size());

    for (size_t i = 0; i < arr.size(); ++i) {
        ft.add(i, arr[i]);
    }

    std::cout << "Prefiks yig'indisi (0..4): " << ft.prefixSum(4) << std::endl;
    std::cout << "Oraliq yig'indisi (2..5): " << ft.rangeSum(2, 5) << std::endl;

    ft.add(3, 4); // 3-indeksga 4 qo'shamiz (6 + 4 = 10)
    std::cout << "Yangilangach oraliq yig'indisi (2..5): " << ft.rangeSum(2, 5) << std::endl;

    return 0;
}
```

## Tushuntirish va Mantiq:
Fenvik daraxti bitlarning eng kichik birligini `x & (-x)` ajratib olish orqali prefiks yig'indilarni va yangilanishlarni O(log N) da o'ta ixcham amalga oshiradi.

## Ishlash natijasi:
```text
Prefiks yig'indisi (0..4): 15
Oraliq yig'indisi (2..5): 14
Yangilangach oraliq yig'indisi (2..5): 18
```

# 888-Topshiriq: Min-Heap (Minimal to'da) noldan massiv asosida qurish
## Topshiriq sharti:
Dinamik `std::vector` asosida o'z MinHeap sinfingizni yozing. `push`, `popMin` va `siftUp`, `siftDown` mantiqlarini yarating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <stdexcept>

class MinHeap {
private:
    std::vector<int> heap;

    void siftUp(int i) {
        while (i > 0) {
            int parent = (i - 1) / 2;
            if (heap[i] < heap[parent]) {
                std::swap(heap[i], heap[parent]);
                i = parent;
            } else break;
        }
    }

    void siftDown(int i) {
        int n = heap.size();
        while (2 * i + 1 < n) {
            int left = 2 * i + 1;
            int right = 2 * i + 2;
            int smallest = left;
            if (right < n && heap[right] < heap[left]) smallest = right;

            if (heap[i] > heap[smallest]) {
                std::swap(heap[i], heap[smallest]);
                i = smallest;
            } else break;
        }
    }

public:
    void push(int val) {
        heap.push_back(val);
        siftUp(heap.size() - 1);
    }

    int popMin() {
        if (heap.empty()) throw std::runtime_error("Heap bo'sh!");
        int minVal = heap[0];
        heap[0] = heap.back();
        heap.pop_back();
        if (!heap.empty()) siftDown(0);
        return minVal;
    }

    bool empty() const { return heap.empty(); }
};

int main() {
    MinHeap mh;
    for (int x : {35, 12, 45, 2, 8, 19}) {
        mh.push(x);
    }

    std::cout << "MinHeap elementlari chiqarilishi: ";
    while (!mh.empty()) {
        std::cout << mh.popMin() << " ";
    }
    std::cout << std::endl;

    return 0;
}
```

## Tushuntirish va Mantiq:
Har bir element qo'shish O(log N) va eng kichigini olish O(log N) vaqt talab qiladi. Eng kichik qiymat doim 0-indeksda (ildizda) bo'ladi.

## Ishlash natijasi:
```text
MinHeap elementlari chiqarilishi: 2 8 12 19 35 45 
```

# 889-Topshiriq: Max-Heap va Heapify amali (O(N) da massivdan to'da hosil qilish)
## Topshiriq sharti:
Berilgan tartibsiz massivni O(N) vaqtda to'da holatiga keltiruvchi `heapify` algoritmini va `popMax` operatsiyasini yarating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

void maxHeapify(std::vector<int>& arr, int n, int i) {
    int largest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;

    if (left < n && arr[left] > arr[largest]) largest = left;
    if (right < n && arr[right] > arr[largest]) largest = right;

    if (largest != i) {
        std::swap(arr[i], arr[largest]);
        maxHeapify(arr, n, largest);
    }
}

void buildMaxHeap(std::vector<int>& arr) {
    int n = arr.size();
    for (int i = n / 2 - 1; i >= 0; --i) {
        maxHeapify(arr, n, i);
    }
}

int main() {
    std::vector<int> arr = {4, 10, 3, 5, 1};
    buildMaxHeap(arr);

    std::cout << "Max-heap ko'rinishi: ";
    for (int x : arr) std::cout << x << " ";
    std::cout << "\nEng katta element (ildiz): " << arr[0] << std::endl;

    return 0;
}
```

## Tushuntirish va Mantiq:
Oxirgi ota tugundan boshlab (`n / 2 - 1`) pastga tomon `heapify` qilib chiqilganda, matematik isbotga ko'ra butun to'da O(N) vaqtda quriladi.

## Ishlash natijasi:
```text
Max-heap ko'rinishi: 10 5 3 4 1 
Eng katta element (ildiz): 10
```

# 890-Topshiriq: Heap Sort (To'da yordamida saralash) algoritmi
## Topshiriq sharti:
Max-heap dan foydalanib massivni o'z joyida (in-place) O(N log N) vaqt va O(1) qo'shimcha xotira bilan o'sish tartibida saralang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

void heapify(std::vector<int>& arr, int n, int i) {
    int largest = i;
    int l = 2 * i + 1;
    int r = 2 * i + 2;

    if (l < n && arr[l] > arr[largest]) largest = l;
    if (r < n && arr[r] > arr[largest]) largest = r;

    if (largest != i) {
        std::swap(arr[i], arr[largest]);
        heapify(arr, n, largest);
    }
}

void heapSort(std::vector<int>& arr) {
    int n = arr.size();
    // 1. Max heap quramiz
    for (int i = n / 2 - 1; i >= 0; --i) {
        heapify(arr, n, i);
    }
    // 2. Birma-bir eng kattasini oxiriga olib o'tamiz
    for (int i = n - 1; i > 0; --i) {
        std::swap(arr[0], arr[i]);
        heapify(arr, i, 0);
    }
}

int main() {
    std::vector<int> arr = {12, 11, 13, 5, 6, 7};
    heapSort(arr);

    std::cout << "Saralangan massiv: ";
    for (int x : arr) std::cout << x << " ";
    std::cout << std::endl;

    return 0;
}
```

## Tushuntirish va Mantiq:
Heap sort algoritmi eng yomon holatda ham O(N log N) vaqtni kafolatlaydi va qo'shimcha xotira talab qilmaydi.

## Ishlash natijasi:
```text
Saralangan massiv: 5 6 7 11 12 13 
```

# 891-Topshiriq: QuickSelect - K-chi eng kichik elementni O(N) da topish
## Topshiriq sharti:
QuickSort bo'linishi (Lomuto yoki Hoare partition) asosida massivni to'liq saralamasdan o'rtacha O(N) vaqtda K-chi kichik elementni topuvchi QuickSelect algoritmini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int partition(std::vector<int>& arr, int left, int right) {
    int pivot = arr[right];
    int i = left;
    for (int j = left; j < right; ++j) {
        if (arr[j] <= pivot) {
            std::swap(arr[i], arr[j]);
            i++;
        }
    }
    std::swap(arr[i], arr[right]);
    return i;
}

int quickSelect(std::vector<int>& arr, int left, int right, int k) {
    if (left <= right) {
        int p = partition(arr, left, right);
        if (p == k) return arr[p];
        if (p > k) return quickSelect(arr, left, p - 1, k);
        return quickSelect(arr, p + 1, right, k);
    }
    return -1;
}

int main() {
    std::vector<int> nums = {7, 10, 4, 3, 20, 15};
    int k = 3; // 3-chi kichik (0-indeksda 2-indeksdagi: 3, 4, 7 -> 7)
    int val = quickSelect(nums, 0, nums.size() - 1, k - 1);

    std::cout << k << "-chi eng kichik element: " << val << std::endl;

    return 0;
}
```

## Tushuntirish va Mantiq:
QuickSelect har bir qadamda massivning faqat bitta yarmini qoldirib ketadi: N + N/2 + N/4 + ... = 2N, bu esa o'rtacha O(N) chiziqli vaqt beradi.

## Ishlash natijasi:
```text
3-chi eng kichik element: 7
```

# 892-Topshiriq: Monoton stek (Monotonic Stack) - Next Greater Element
## Topshiriq sharti:
Massivning har bir elementi uchun undan o'ngda joylashgan birinchi undan katta elementni O(N) vaqtda topuvchi monoton stek algoritmini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <stack>

std::vector<int> nextGreaterElements(const std::vector<int>& nums) {
    int n = nums.size();
    std::vector<int> result(n, -1);
    std::stack<int> st; // Indekslarni saqlaymiz

    for (int i = 0; i < n; ++i) {
        while (!st.empty() && nums[st.top()] < nums[i]) {
            result[st.top()] = nums[i];
            st.pop();
        }
        st.push(i);
    }
    return result;
}

int main() {
    std::vector<int> arr = {4, 5, 2, 25, 7, 8};
    auto res = nextGreaterElements(arr);

    for (size_t i = 0; i < arr.size(); ++i) {
        std::cout << arr[i] << " -> " << res[i] << "\n";
    }

    return 0;
}
```

## Tushuntirish va Mantiq:
Monoton kamayuvchi stekda indekslar saqlanadi. Katta element uchraganda stekdagi kichik elementlar chiqarilib, ularning natijasi sifatida yangi element belgilanadi. O(N) vaqt.

## Ishlash natijasi:
```text
4 -> 5
5 -> 25
2 -> 25
25 -> -1
7 -> 8
8 -> -1
```

# 893-Topshiriq: Monoton stek - Gistogrammada eng katta to'g'ri to'rtburchak maydoni
## Topshiriq sharti:
Ustunlar balandliklari massivi berilgan bo'lsa, gistogramma ichiga sig'uvchi maksimal to'g'ri to'rtburchak maydonini (Largest Rectangle in Histogram) O(N) da toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <stack>
#include <algorithm>

int largestRectangleArea(const std::vector<int>& heights) {
    std::stack<int> st;
    int maxArea = 0;
    int n = heights.size();

    for (int i = 0; i <= n; ++i) {
        int h = (i == n) ? 0 : heights[i];
        while (!st.empty() && h < heights[st.top()]) {
            int height = heights[st.top()];
            st.pop();
            int width = st.empty() ? i : i - st.top() - 1;
            maxArea = std::max(maxArea, height * width);
        }
        st.push(i);
    }
    return maxArea;
}

int main() {
    std::vector<int> h = {2, 1, 5, 6, 2, 3};
    std::cout << "Gistogrammadagi maksimal yuza: " << largestRectangleArea(h) << std::endl;

    return 0;
}
```

## Tushuntirish va Mantiq:
Monoton o'suvchi stek yordamida har bir ustun uchun chap va o'ng chegaralar O(1) ammortizatsiyalangan vaqtda aniqlanadi, umumiy vaqt O(N).

## Ishlash natijasi:
```text
Gistogrammadagi maksimal yuza: 10
```

# 894-Topshiriq: Monoton deka (Monotonic Deque) - Siljuvchi oyna maksimumi
## Topshiriq sharti:
K uzunlikdagi siljuvchi oyna massiv bo'ylab harakatlanganda, har bir oynadagi maksimal elementni O(N) da `std::deque` yordamida toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <deque>

std::vector<int> maxSlidingWindow(const std::vector<int>& nums, int k) {
    std::deque<int> dq; // Indekslar saqlanadi
    std::vector<int> result;

    for (int i = 0; i < (int)nums.size(); ++i) {
        // Oyna chegarasidan chiqib ketganlarni olib tashlash
        if (!dq.empty() && dq.front() == i - k) {
            dq.pop_front();
        }

        // Yangi elementdan kichik bo'lgan barcha orqa elementlarni o'chirish
        while (!dq.empty() && nums[dq.back()] < nums[i]) {
            dq.pop_back();
        }

        dq.push_back(i);

        // Oyna to'liq shakllangach
        if (i >= k - 1) {
            result.push_back(nums[dq.front()]);
        }
    }
    return result;
}

int main() {
    std::vector<int> nums = {1, 3, -1, -3, 5, 3, 6, 7};
    int k = 3;
    auto res = maxSlidingWindow(nums, k);

    std::cout << "Siljuvchi oyna (k=" << k << ") maksimallari: ";
    for (int x : res) std::cout << x << " ";
    std::cout << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
Deka elementlarni kamayish tartibida saqlaydi, shuning uchun oynadagi maksimum har doim `dq.front()` da bo'ladi. Har bir element deka ichiga 1 marta kiradi va chiqadi: O(N).

## Ishlash natijasi:
```text
Siljuvchi oyna (k=3) maksimallari: 3 3 5 5 6 7 
```

# 895-Topshiriq: KMP algoritmi (Knuth-Morris-Pratt) - O(N + M) satr qidiruvi
## Topshiriq sharti:
KMP algoritmining prefiks funksiyasi (`LPS` - Longest Prefix Suffix) massivini hisoblang va matn ichidan namunani O(N + M) vaqtda qidiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>
#include <vector>

std::vector<int> computeLPS(const std::string& pat) {
    int m = pat.size();
    std::vector<int> lps(m, 0);
    int len = 0;
    int i = 1;

    while (i < m) {
        if (pat[i] == pat[len]) {
            len++;
            lps[i] = len;
            i++;
        } else {
            if (len != 0) {
                len = lps[len - 1];
            } else {
                lps[i] = 0;
                i++;
            }
        }
    }
    return lps;
}

std::vector<int> KMPSearch(const std::string& pat, const std::string& txt) {
    std::vector<int> matches;
    int m = pat.size();
    int n = txt.size();
    auto lps = computeLPS(pat);

    int i = 0, j = 0;
    while (i < n) {
        if (pat[j] == txt[i]) {
            i++;
            j++;
        }
        if (j == m) {
            matches.push_back(i - j);
            j = lps[j - 1];
        } else if (i < n && pat[j] != txt[i]) {
            if (j != 0) {
                j = lps[j - 1];
            } else {
                i++;
            }
        }
    }
    return matches;
}

int main() {
    std::string txt = "ABABDABACDABABCABAB";
    std::string pat = "ABABCABAB";

    auto res = KMPSearch(pat, txt);
    std::cout << "Topilgan indekslar: ";
    for (int idx : res) std::cout << idx << " ";
    std::cout << std::endl;

    return 0;
}
```

## Tushuntirish va Mantiq:
KMP algoritmi mos kelmay qolgan holatda matn ko'rsatkichini orqaga qaytarmaydi, balki namunadagi LPS qiymatidan foydalanib sakraydi. O(N + M) vaqt.

## Ishlash natijasi:
```text
Topilgan indekslar: 10 
```

# 896-Topshiriq: Kosaraju algoritmi - Kuchli bog'langan komponentlar (SCC)
## Topshiriq sharti:
Yo'naltirilgan grafdagi barcha kuchli bog'langan komponentlarni (Strongly Connected Components) 2 ta DFS va transpozitsiya orqali toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <stack>

void dfs1(int u, const std::vector<std::vector<int>>& adj, std::vector<bool>& visited, std::stack<int>& st) {
    visited[u] = true;
    for (int v : adj[u]) {
        if (!visited[v]) dfs1(v, adj, visited, st);
    }
    st.push(u);
}

void dfs2(int u, const std::vector<std::vector<int>>& adjRev, std::vector<bool>& visited, std::vector<int>& comp) {
    visited[u] = true;
    comp.push_back(u);
    for (int v : adjRev[u]) {
        if (!visited[v]) dfs2(v, adjRev, visited, comp);
    }
}

void findSCCs(int n, const std::vector<std::vector<int>>& adj) {
    std::stack<int> st;
    std::vector<bool> visited(n, false);

    for (int i = 0; i < n; ++i) {
        if (!visited[i]) dfs1(i, adj, visited, st);
    }

    // Grafni teskarilash (Transpose)
    std::vector<std::vector<int>> adjRev(n);
    for (int u = 0; u < n; ++u) {
        for (int v : adj[u]) {
            adjRev[v].push_back(u);
        }
    }

    std::fill(visited.begin(), visited.end(), false);
    std::cout << "Kuchli bog'langan komponentlar (SCC):\n";
    while (!st.empty()) {
        int u = st.top();
        st.pop();
        if (!visited[u]) {
            std::vector<int> comp;
            dfs2(u, adjRev, visited, comp);
            std::cout << "[ ";
            for (int x : comp) std::cout << x << " ";
            std::cout << "]\n";
        }
    }
}

int main() {
    int V = 5;
    std::vector<std::vector<int>> adj(V);
    adj[1].push_back(0);
    adj[0].push_back(2);
    adj[2].push_back(1);
    adj[0].push_back(3);
    adj[3].push_back(4);

    findSCCs(V, adj);

    return 0;
}
```

## Tushuntirish va Mantiq:
Kosaraju algoritmi dastlab tugunlarni tugash vaqti bo'yicha saralaydi, so'ngra qirralar yo'nalishi teskarisiga o'girilgan grafda DFS o'tkazib SCC larni ajratadi.

## Ishlash natijasi:
```text
Kuchli bog'langan komponentlar (SCC):
[ 0 1 2 ]
[ 3 ]
[ 4 ]
```

# 897-Topshiriq: Qaytarilish (Backtracking) - N ta Vazir (N-Queens) masalasi
## Topshiriq sharti:
N x N shaxmat taxtasiga bir-biriga hujum qilmaydigan qilib N ta vazirni joylashtirishning barcha yechimlarini qaytaruvchi dastur yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <string>

bool isSafe(const std::vector<std::string>& board, int row, int col, int n) {
    for (int i = 0; i < row; ++i) {
        if (board[i][col] == 'Q') return false;
    }
    for (int i = row - 1, j = col - 1; i >= 0 && j >= 0; --i, --j) {
        if (board[i][j] == 'Q') return false;
    }
    for (int i = row - 1, j = col + 1; i >= 0 && j < n; --i, ++j) {
        if (board[i][j] == 'Q') return false;
    }
    return true;
}

void solveNQueens(int row, int n, std::vector<std::string>& board, int& solutionCount) {
    if (row == n) {
        solutionCount++;
        return;
    }
    for (int col = 0; col < n; ++col) {
        if (isSafe(board, row, col, n)) {
            board[row][col] = 'Q';
            solveNQueens(row + 1, n, board, solutionCount);
            board[row][col] = '.'; // Backtracking
        }
    }
}

int main() {
    for (int n = 4; n <= 8; ++n) {
        std::vector<std::string> board(n, std::string(n, '.'));
        int count = 0;
        solveNQueens(0, n, board, count);
        std::cout << n << " vazir uchun yechimlar soni: " << count << "\n";
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
Backtracking har bir satrga bittadan vazir qo'yib tekshiradi. Agar to'qnashuv bo'lsa, avvalgi satrga qaytib, keyingi ustunni sinab ko'radi.

## Ishlash natijasi:
```text
4 vazir uchun yechimlar soni: 2
5 vazir uchun yechimlar soni: 10
6 vazir uchun yechimlar soni: 4
7 vazir uchun yechimlar soni: 40
8 vazir uchun yechimlar soni: 92
```

# 898-Topshiriq: Backtracking - 9x9 Sudoku yechuvchisi (Sudoku Solver)
## Topshiriq sharti:
Berilgan to'liq bo'lmagan 9x9 Sudoku kataklarini to'ldiruvchi rekursiv backtracking yechimini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

bool isValid(const std::vector<std::vector<char>>& board, int row, int col, char c) {
    for (int i = 0; i < 9; ++i) {
        if (board[row][i] == c) return false;
        if (board[i][col] == c) return false;
        if (board[3 * (row / 3) + i / 3][3 * (col / 3) + i % 3] == c) return false;
    }
    return true;
}

bool solveSudoku(std::vector<std::vector<char>>& board) {
    for (int i = 0; i < 9; ++i) {
        for (int j = 0; j < 9; ++j) {
            if (board[i][j] == '.') {
                for (char c = '1'; c <= '9'; ++c) {
                    if (isValid(board, i, j, c)) {
                        board[i][j] = c;
                        if (solveSudoku(board)) return true;
                        board[i][j] = '.'; // Qaytarilish
                    }
                }
                return false;
            }
        }
    }
    return true;
}

int main() {
    std::vector<std::vector<char>> board = {
        {'5','3','.','.','7','.','.','.','.'},
        {'6','.','.','1','9','5','.','.','.'},
        {'.','9','8','.','.','.','.','6','.'},
        {'8','.','.','.','6','.','.','.','3'},
        {'4','.','.','8','.','3','.','.','1'},
        {'7','.','.','.','2','.','.','.','6'},
        {'.','6','.','.','.','.','2','8','.'},
        {'.','.','.','4','1','9','.','.','5'},
        {'.','.','.','.','8','.','.','7','9'}
    };

    if (solveSudoku(board)) {
        std::cout << "Yechilgan Sudoku birinchi qatori: ";
        for (int j = 0; j < 9; ++j) std::cout << board[0][j] << " ";
        std::cout << "\nSudoku to'liq muvaffaqiyatli yechildi!\n";
    }

    return 0;
}
```

## Tushuntirish va Mantiq:
Bo'sh kataklar uchun 1 dan 9 gacha raqamlar satr, ustun va 3x3 blok bo'yicha tekshiriladi. Mos kelsa keyingi katakka o'tiladi, aks holda nuqta qaytariladi.

## Ishlash natijasi:
```text
Yechilgan Sudoku birinchi qatori: 5 3 4 6 7 8 9 1 2 
Sudoku to'liq muvaffaqiyatli yechildi!
```

# 899-Topshiriq: Backtracking - To'plam qism to'plamlari (Subsets)
## Topshiriq sharti:
N ta elementdan iborat to'plamning barcha mumkin bo'lgan 2^N ta qism to'plamlarini (Power Set) backtracking yordamida generatsiya qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

void generateSubsets(int idx, const std::vector<int>& nums, std::vector<int>& current, std::vector<std::vector<int>>& result) {
    result.push_back(current);

    for (size_t i = idx; i < nums.size(); ++i) {
        current.push_back(nums[i]);
        generateSubsets(i + 1, nums, current, result);
        current.pop_back(); // Backtracking
    }
}

int main() {
    std::vector<int> nums = {1, 2, 3};
    std::vector<std::vector<int>> result;
    std::vector<int> current;

    generateSubsets(0, nums, current, result);

    std::cout << "Barcha qism to'plamlar (" << result.size() << " ta):\n";
    for (const auto& subset : result) {
        std::cout << "[ ";
        for (int x : subset) std::cout << x << " ";
        std::cout << "]\n";
    }

    return 0;
}
```

## Tushuntirish va Mantiq:
Har bir qadamda yangi element qo'shiladi, natijaga kiritiladi, keyingi indekslarga rekursiv o'tiladi va so'ngra element chiqarib olinadi.

## Ishlash natijasi:
```text
Barcha qism to'plamlar (8 ta):
[ ]
[ 1 ]
[ 1 2 ]
[ 1 2 3 ]
[ 1 3 ]
[ 2 ]
[ 2 3 ]
[ 3 ]
```

# 900-Topshiriq: Backtracking - Permutatsiyalar (Barcha o'rin almashtirishlar)
## Topshiriq sharti:
N ta takrorlanmas sondan iborat massivning barcha N! ta o'rin almashtirishlarini (permutations) rekursiv almashtirish (swap) yordamida hosil qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

void permute(int idx, std::vector<int>& nums, std::vector<std::vector<int>>& result) {
    if (idx == (int)nums.size()) {
        result.push_back(nums);
        return;
    }

    for (int i = idx; i < (int)nums.size(); ++i) {
        std::swap(nums[idx], nums[i]);
        permute(idx + 1, nums, result);
        std::swap(nums[idx], nums[i]); // Backtracking
    }
}

int main() {
    std::vector<int> nums = {1, 2, 3};
    std::vector<std::vector<int>> result;

    permute(0, nums, result);

    std::cout << "Permutatsiyalar soni: " << result.size() << "\n";
    for (const auto& p : result) {
        std::cout << "[ ";
        for (int x : p) std::cout << x << " ";
        std::cout << "]\n";
    }

    return 0;
}
```

## Tushuntirish va Mantiq:
In-place swap va backtracking usuli orqali qo'shimcha `used` massivisiz xotirani tejagan holda N! ta permutatsiyani generatsiya qiladi.

## Ishlash natijasi:
```text
Permutatsiyalar soni: 6
[ 1 2 3 ]
[ 1 3 2 ]
[ 2 1 3 ]
[ 2 3 1 ]
[ 3 2 1 ]
[ 3 1 2 ]
```

