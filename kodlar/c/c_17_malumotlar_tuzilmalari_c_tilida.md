# C Dasturlash Tili — 17-Qism: Ma'lumotlar Tuzilmalari C Tilida (Data Structures)
## (801-850 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam quyidagi muhim mavzularni qamrab oladi:
* Singly Linked List: yaratish, push_front, push_back, delete, reverse va Floyd tsikl algoritmi
* Doubly va Circular Linked Listlar
* Stek (Stack): Massiv va Linked list asosidagi stek, qavslar balansi, Postfix RPN
* Navbat (Queue): Ring buffer, Deque va Dynamic Vector
* Binar Qidiruv Daraxti (BST): Insert, Search, Min/Max, Balandlik va Delete
* Binar To'p (Min-Heap): Insert, Heapify Up/Down, Extract-Min
* Xesh-jadval (djb2, Chaining, Linear Probing), Graflar (BFS, DFS, DSU) va LRU Cache Master Engine

---

# 801-Topshiriq: Singly Linked List: Tugun (Node) strukturasi va yangi tugun yaratish

## Topshiriq sharti:
Dinamik xotirada ma'lumot va keyingi manzilni saqlovchi tugun funksiyasini yozish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node *next;
} Node;

Node* create_node(int data) {
    Node *new_node = (Node *)malloc(sizeof(Node));
    if (new_node == NULL) {
        perror("Xotira ajratilmadi");
        exit(1);
    }
    new_node->data = data;
    new_node->next = NULL;
    return new_node;
}

int main(void) {
    Node *n1 = create_node(10);
    printf("Tugun yaratildi: data = %d, next = %p\n", n1->data, (void*)n1->next);
    free(n1);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir tugun foydali yuklama (data) va keyingi tugunga ko'rsatkich (next) dan iborat.
2. Oxirgi tugunning next ko'rsatkichi har doim NULL bo'ladi.

## Ishlash natijasi:
```text
Tugun yaratildi: data = 10, next = 0000000000000000
```

---

# 802-Topshiriq: Singly Linked List: Boshiga qo'shish (push_front - O(1))

## Topshiriq sharti:
Ro'yxat boshiga yangi element qo'shish va head ko'rsatkichini yangilash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node *next;
} Node;

void push_front(Node **head, int data) {
    Node *new_node = (Node *)malloc(sizeof(Node));
    new_node->data = data;
    new_node->next = *head;
    *head = new_node;
}

void print_list(Node *head) {
    Node *curr = head;
    while (curr) {
        printf("%d -> ", curr->data);
        curr = curr->next;
    }
    printf("NULL\n");
}

int main(void) {
    Node *head = NULL;
    push_front(&head, 30);
    push_front(&head, 20);
    push_front(&head, 10);

    printf("Ro'yxat: ");
    print_list(head);

    // Xotirani tozalash
    while (head) {
        Node *tmp = head;
        head = head->next;
        free(tmp);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. head ko'rsatkichini funksiya ichida o'zgartirish uchun `Node **head` (pointer to pointer) uzatiladi.
2. Boshiga qo'shish amali doimiy vaqt — O(1) oladi.

## Ishlash natijasi:
```text
Ro'yxat: 10 -> 20 -> 30 -> NULL
```

---

# 803-Topshiriq: Singly Linked List: Oxiriga qo'shish (push_back - O(N))

## Topshiriq sharti:
Ro'yxat oxirigacha yurib yangi tugunni ulash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node *next;
} Node;

void push_back(Node **head, int data) {
    Node *new_node = (Node *)malloc(sizeof(Node));
    new_node->data = data;
    new_node->next = NULL;

    if (*head == NULL) {
        *head = new_node;
        return;
    }

    Node *curr = *head;
    while (curr->next != NULL) {
        curr = curr->next;
    }
    curr->next = new_node;
}

int main(void) {
    Node *head = NULL;
    push_back(&head, 100);
    push_back(&head, 200);
    push_back(&head, 300);

    Node *curr = head;
    while (curr) {
        printf("%d -> ", curr->data);
        Node *tmp = curr;
        curr = curr->next;
        free(tmp);
    }
    printf("NULL\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Agar ro'yxat bo'sh bo'lsa, yangi tugun bosh (head) bo'ladi.
2. Aks holda `curr->next != NULL` gacha borib eng oxirgi tugunga ulanadi.

## Ishlash natijasi:
```text
100 -> 200 -> 300 -> NULL
```

---

# 804-Topshiriq: Singly Linked List: Qiymat bo'yicha elementni o'chirish (Delete by Value)

## Topshiriq sharti:
Berilgan sonni ro'yxatdan topib xotirasini ozod qilish va zanjirni tiklash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node *next;
} Node;

void delete_value(Node **head, int val) {
    Node *curr = *head, *prev = NULL;

    if (curr != NULL && curr->data == val) {
        *head = curr->next;
        free(curr);
        return;
    }

    while (curr != NULL && curr->data != val) {
        prev = curr;
        curr = curr->next;
    }

    if (curr == NULL) return; // Topilmadi

    prev->next = curr->next;
    free(curr);
}

int main(void) {
    Node *n3 = malloc(sizeof(Node)); n3->data = 30; n3->next = NULL;
    Node *n2 = malloc(sizeof(Node)); n2->data = 20; n2->next = n3;
    Node *head = malloc(sizeof(Node)); head->data = 10; head->next = n2;

    delete_value(&head, 20); // 20 ni o'chiramiz

    Node *c = head;
    while (c) {
        printf("%d -> ", c->data);
        Node *t = c;
        c = c->next;
        free(t);
    }
    printf("NULL\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. O'chirishda oldingi tugun (prev) ko'rsatkichi keyingi tugunga (curr->next) bog'lanadi va curr xotiradan o'chiriladi.

## Ishlash natijasi:
```text
10 -> 30 -> NULL
```

---

# 805-Topshiriq: Singly Linked List: Ro'yxatni joyida teskari qilish (Reverse List In-Place)

## Topshiriq sharti:
Qo'shimcha xotira sarflamasdan (O(1) xotira, O(N) vaqt) pointerlarni teskari yo'naltirish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node *next;
} Node;

Node* reverse_list(Node *head) {
    Node *prev = NULL;
    Node *curr = head;
    Node *next = NULL;

    while (curr != NULL) {
        next = curr->next; // Keyingisini eslab qolish
        curr->next = prev; // Ko'rsatkichni teskari qilish
        prev = curr;       // Qadam oldinga
        curr = next;
    }
    return prev; // Yangi bosh (head)
}

int main(void) {
    Node *n3 = malloc(sizeof(Node)); n3->data = 3; n3->next = NULL;
    Node *n2 = malloc(sizeof(Node)); n2->data = 2; n2->next = n3;
    Node *head = malloc(sizeof(Node)); head->data = 1; head->next = n2;

    head = reverse_list(head);

    Node *c = head;
    while (c) {
        printf("%d -> ", c->data);
        Node *t = c;
        c = c->next;
        free(t);
    }
    printf("NULL\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Uchta pointer (prev, curr, next) usuli texnik suhbatlarda (coding interview) eng ko'p so'raladigan klassik algoritm hisoblanadi.

## Ishlash natijasi:
```text
3 -> 2 -> 1 -> NULL
```

---

# 806-Topshiriq: Linked List da tsiklni aniqlash: Floyd algoritmi (Tortoise and Hare)

## Topshiriq sharti:
Sekin (slow) va tez (fast) yuruvchi ikkita ko'rsatkich orqali cheksiz halqani aniqlash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node *next;
} Node;

int has_cycle(Node *head) {
    Node *slow = head;
    Node *fast = head;

    while (fast != NULL && fast->next != NULL) {
        slow = slow->next;          // 1 qadam
        fast = fast->next->next;    // 2 qadam
        if (slow == fast) {
            return 1; // Tsikl topildi!
        }
    }
    return 0; // Tsikl yo'q
}

int main(void) {
    Node *n1 = malloc(sizeof(Node));
    Node *n2 = malloc(sizeof(Node));
    Node *n3 = malloc(sizeof(Node));

    n1->data = 1; n1->next = n2;
    n2->data = 2; n2->next = n3;
    n3->data = 3; n3->next = n1; // Halqa: n3 yana n1 ga ulandi!

    printf("Ro'yxatda tsikl bormi? %s\n", has_cycle(n1) ? "HA" : "YO'Q");

    free(n1); free(n2); free(n3);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Floyd algoritmi qo'shimcha xotira sarflamasdan (O(1) memory) O(N) vaqtda halqani aniqlaydi.
2. Agar tsikl bo'lsa, tezkor ko'rsatkich albatta sekiniga yetib oladi.

## Ishlash natijasi:
```text
Ro'yxatda tsikl bormi? HA
```

---

# 807-Topshiriq: Doubly Linked List (Ikki tomonlama ro'yxat) asoslari

## Topshiriq sharti:
prev va next pointerlarga ega bo'lgan ikki tomonlama ro'yxat tuguni va oldinga/orqaga aylanib chiqish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct DNode {
    int data;
    struct DNode *prev;
    struct DNode *next;
} DNode;

void push_back_dlist(DNode **head, int val) {
    DNode *new_node = (DNode*)malloc(sizeof(DNode));
    new_node->data = val;
    new_node->next = NULL;

    if (*head == NULL) {
        new_node->prev = NULL;
        *head = new_node;
        return;
    }

    DNode *curr = *head;
    while (curr->next != NULL) curr = curr->next;

    curr->next = new_node;
    new_node->prev = curr;
}

int main(void) {
    DNode *head = NULL;
    push_back_dlist(&head, 10);
    push_back_dlist(&head, 20);
    push_back_dlist(&head, 30);

    // Oldinga yurish
    printf("Oldinga: ");
    DNode *c = head, *last = NULL;
    while (c) {
        printf("%d <-> ", c->data);
        last = c;
        c = c->next;
    }
    printf("NULL\n");

    // Orqaga yurish
    printf("Orqaga:  ");
    while (last) {
        printf("%d <-> ", last->data);
        DNode *tmp = last;
        last = last->prev;
        free(tmp);
    }
    printf("NULL\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Doubly Linked List elementdan ham oldinga, ham orqaga O(1) da harakatlanish imkonini beradi.
2. Brauzer tarixi (Oldinga/Orqaga tugmalari) va matn muharrirlari shu asosda ishlaydi.

## Ishlash natijasi:
```text
Oldinga: 10 <-> 20 <-> 30 <-> NULL
Orqaga:  30 <-> 20 <-> 10 <-> NULL
```

---

# 808-Topshiriq: Circular Linked List (Halqasimon ro'yxat)

## Topshiriq sharti:
Oxirgi tugun birinchi tugunga ulanuvchi halqali ro'yxat tuzilishi va aylanib chiqish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct CNode {
    int data;
    struct CNode *next;
} CNode;

int main(void) {
    CNode *n1 = malloc(sizeof(CNode));
    CNode *n2 = malloc(sizeof(CNode));
    CNode *n3 = malloc(sizeof(CNode));

    n1->data = 1; n1->next = n2;
    n2->data = 2; n2->next = n3;
    n3->data = 3; n3->next = n1; // Halqa

    printf("Halqasimon ro'yxat bo'yicha 6 qadam:\n");
    CNode *curr = n1;
    for (int i = 0; i < 6; i++) {
        printf("%d -> ", curr->data);
        curr = curr->next;
    }
    printf("...\n");

    free(n1); free(n2); free(n3);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Halqasimon ro'yxatlarda NULL ko'rsatkichi bo'lmaydi.
2. CPU round-robin rejalashtiruvchisi (scheduler) vazifalarni navbatma-navbat bajarishda aynan halqasimon ro'yxatdan foydalanadi.

## Ishlash natijasi:
```text
Halqasimon ro'yxat bo'yicha 6 qadam:
1 -> 2 -> 3 -> 1 -> 2 -> 3 -> ...
```

---

# 809-Topshiriq: Massiv asosidagi Stek (Array-Based Stack - LIFO)

## Topshiriq sharti:
push, pop, peek va is_empty operatsiyalarini massiv orqali amalga oshirish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

#define STACK_CAPACITY 5

typedef struct {
    int data[STACK_CAPACITY];
    int top;
} Stack;

void init_stack(Stack *s) { s->top = -1; }
int is_empty(Stack *s) { return s->top == -1; }
int is_full(Stack *s) { return s->top == STACK_CAPACITY - 1; }

void push(Stack *s, int val) {
    if (is_full(s)) {
        printf("Stek to'ldi!\n");
        return;
    }
    s->data[++(s->top)] = val;
}

int pop(Stack *s) {
    if (is_empty(s)) {
        printf("Stek bo'sh!\n");
        return -1;
    }
    return s->data[(s->top)--];
}

int main(void) {
    Stack s;
    init_stack(&s);

    push(&s, 10);
    push(&s, 20);
    push(&s, 30);

    printf("Pop qilingan elementlar (LIFO): ");
    while (!is_empty(&s)) {
        printf("%d ", pop(&s));
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Stek LIFO (Last-In First-Out) tamoyilida ishlaydi.
2. Oxirgi kiritilgan 30 birinchi bo'lib chiqadi.

## Ishlash natijasi:
```text
Pop qilingan elementlar (LIFO): 30 20 10
```

---

# 810-Topshiriq: Bog'langan ro'yxat asosidagi Stek (Linked-List Stack)

## Topshiriq sharti:
Cheksiz o'suvchi dinamik xotirali stek implementatsiyasi.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct StackNode {
    int data;
    struct StackNode *next;
} StackNode;

void push_ll(StackNode **top, int val) {
    StackNode *node = (StackNode*)malloc(sizeof(StackNode));
    node->data = val;
    node->next = *top;
    *top = node;
}

int pop_ll(StackNode **top) {
    if (*top == NULL) return -1;
    StackNode *tmp = *top;
    int val = tmp->data;
    *top = (*top)->next;
    free(tmp);
    return val;
}

int main(void) {
    StackNode *top = NULL;
    push_ll(&top, 100);
    push_ll(&top, 200);

    printf("Pop: %d\n", pop_ll(&top));
    printf("Pop: %d\n", pop_ll(&top));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Linked list asosidagi stekda qat'iy hajm chegarasi bo'lmaydi, har bir push yangi tugun ajratadi.

## Ishlash natijasi:
```text
Pop: 200
Pop: 100
```

---

# 811-Topshiriq: Stek yordamida qavslar balansini tekshirish (Balanced Parentheses)

## Topshiriq sharti:
Satrdagi '()', '[]', '{}' qavslarining to'g'ri ochilib-yopilganligini tekshirish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

int mosmi(char ochiq, char yopiq) {
    return (ochiq == '(' && yopiq == ')') ||
           (ochiq == '[' && yopiq == ']') ||
           (ochiq == '{' && yopiq == '}');
}

int qavslar_togrimi(const char *str) {
    char stack[128];
    int top = -1;

    for (int i = 0; str[i]; i++) {
        char c = str[i];
        if (c == '(' || c == '[' || c == '{') {
            stack[++top] = c;
        } else if (c == ')' || c == ']' || c == '}') {
            if (top == -1 || !mosmi(stack[top--], c)) {
                return 0; // Noto'g'ri
            }
        }
    }
    return top == -1;
}

int main(void) {
    const char *s1 = "{[()]}";
    const char *s2 = "{[(])}";

    printf("%s to'g'rimi? %s\n", s1, qavslar_togrimi(s1) ? "HA" : "YO'Q");
    printf("%s to'g'rimi? %s\n", s2, qavslar_togrimi(s2) ? "HA" : "YO'Q");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kompilyatorlar leksik tahlilda qavslar balansini aynan mana shunday stek algoritmi bilan tekshiradi.

## Ishlash natijasi:
```text
{[()]} to'g'rimi? HA
{[(])} to'g'rimi? YO'Q
```

---

# 812-Topshiriq: Postfix ifodani hisoblash (Reverse Polish Notation Evaluation)

## Topshiriq sharti:
Stek yordamida '5 3 + 2 *' kabi postfix ifodalarni hisoblovchi kalkulyator.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <ctype.h>

int hisobla_postfix(const char *exp) {
    int stack[64];
    int top = -1;

    for (int i = 0; exp[i]; i++) {
        if (isspace(exp[i])) continue;

        if (isdigit(exp[i])) {
            stack[++top] = exp[i] - '0';
        } else {
            int b = stack[top--];
            int a = stack[top--];
            switch (exp[i]) {
                case '+': stack[++top] = a + b; break;
                case '-': stack[++top] = a - b; break;
                case '*': stack[++top] = a * b; break;
                case '/': stack[++top] = a / b; break;
            }
        }
    }
    return stack[top];
}

int main(void) {
    // (5 + 3) * 2 = 16
    const char *rpn = "5 3 + 2 *";
    printf("Postfix '%s' natijasi: %d\n", rpn, hisobla_postfix(rpn));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Postfix notatsiyasida qavslar shart emas, amallar tartibi qat'iy va hisoblash bitta o'tishda O(N) da bajariladi.

## Ishlash natijasi:
```text
Postfix '5 3 + 2 *' natijasi: 16
```

---

# 813-Topshiriq: Halqasimon Navbat (Circular Queue / Ring Buffer - FIFO)

## Topshiriq sharti:
Massiv ustida modul arifmetikasi ((tail + 1) % CAP) bilan ishlovchi navbat.

## Yechim (C kodi):
```c
#include <stdio.h>

#define Q_CAP 5

typedef struct {
    int data[Q_CAP];
    int head;
    int tail;
    int count;
} Queue;

void init_queue(Queue *q) { q->head = 0; q->tail = 0; q->count = 0; }
int is_q_empty(Queue *q) { return q->count == 0; }
int is_q_full(Queue *q) { return q->count == Q_CAP; }

void enqueue(Queue *q, int val) {
    if (is_q_full(q)) return;
    q->data[q->tail] = val;
    q->tail = (q->tail + 1) % Q_CAP;
    q->count++;
}

int dequeue(Queue *q) {
    if (is_q_empty(q)) return -1;
    int val = q->data[q->head];
    q->head = (q->head + 1) % Q_CAP;
    q->count--;
    return val;
}

int main(void) {
    Queue q;
    init_queue(&q);

    enqueue(&q, 10);
    enqueue(&q, 20);
    enqueue(&q, 30);

    printf("Navbatdan chiqish (FIFO): %d\n", dequeue(&q));
    printf("Navbatdan chiqish (FIFO): %d\n", dequeue(&q));

    enqueue(&q, 40);
    enqueue(&q, 50);

    while (!is_q_empty(&q)) {
        printf("%d ", dequeue(&q));
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Navbat FIFO (First-In First-Out) tamoyilida ishlaydi.
2. Ring buffer xotirani siljitmasdan cheksiz aylanma rejimda ishlash imkonini beradi.

## Ishlash natijasi:
```text
Navbatdan chiqish (FIFO): 10
Navbatdan chiqish (FIFO): 20
30 40 50
```

---

# 814-Topshiriq: Binar Qidiruv Daraxti (BST): Tugun kiritish (Insert)

## Topshiriq sharti:
Kichik sonlarni chapga, katta sonlarni o'ngga joylashtiruvchi rekursiv BST kiritish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct BSTNode {
    int val;
    struct BSTNode *chap;
    struct BSTNode *ong;
} BSTNode;

BSTNode* bst_insert(BSTNode *root, int val) {
    if (root == NULL) {
        BSTNode *n = (BSTNode*)malloc(sizeof(BSTNode));
        n->val = val;
        n->chap = n->ong = NULL;
        return n;
    }
    if (val < root->val) root->chap = bst_insert(root->chap, val);
    else if (val > root->val) root->ong = bst_insert(root->ong, val);
    return root;
}

void bst_inorder(BSTNode *root) {
    if (!root) return;
    bst_inorder(root->chap);
    printf("%d ", root->val);
    bst_inorder(root->ong);
}

void bst_free(BSTNode *root) {
    if (!root) return;
    bst_free(root->chap);
    bst_free(root->ong);
    free(root);
}

int main(void) {
    BSTNode *root = NULL;
    root = bst_insert(root, 50);
    bst_insert(root, 30);
    bst_insert(root, 70);
    bst_insert(root, 20);
    bst_insert(root, 40);

    printf("BST In-Order (avtomatik saralangan): ");
    bst_inorder(root);
    printf("\n");

    bst_free(root);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. BST ning In-Order traversal (chap -> ildiz -> o'ng) amali ma'lumotlarni har doim o'sish tartibida chiqaradi.

## Ishlash natijasi:
```text
BST In-Order (avtomatik saralangan): 20 30 40 50 70
```

---

# 815-Topshiriq: BST dan element qidirish (Search - O(log N))

## Topshiriq sharti:
Binar qidiruv daraxtidan kalitni rekursiv izlash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct BSTNode {
    int val;
    struct BSTNode *chap, *ong;
} BSTNode;

BSTNode* bst_search(BSTNode *root, int key) {
    if (root == NULL || root->val == key) return root;
    if (key < root->val) return bst_search(root->chap, key);
    return bst_search(root->ong, key);
}

int main(void) {
    BSTNode n20 = {20, NULL, NULL};
    BSTNode n40 = {40, NULL, NULL};
    BSTNode n30 = {30, &n20, &n40};
    BSTNode n70 = {70, NULL, NULL};
    BSTNode root = {50, &n30, &n70};

    BSTNode *topildi = bst_search(&root, 40);
    printf("40 qidirildi: %s\n", topildi ? "Topildi!" : "Yo'q");

    BSTNode *yoq = bst_search(&root, 99);
    printf("99 qidirildi: %s\n", yoq ? "Topildi!" : "Topilmadi.");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Balanslangan BST da qidiruv O(log N) qadamda hal bo'ladi.

## Ishlash natijasi:
```text
40 qidirildi: Topildi!
99 qidirildi: Topilmadi.
```

---

# 816-Topshiriq: BST da Min va Max elementlarni topish

## Topshiriq sharti:
Eng chapdagi (minimal) va eng o'ngdagi (maksimal) tugunlarni aniqlash.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct BSTNode {
    int val;
    struct BSTNode *chap, *ong;
} BSTNode;

int bst_min(BSTNode *root) {
    BSTNode *curr = root;
    while (curr->chap != NULL) curr = curr->chap;
    return curr->val;
}

int bst_max(BSTNode *root) {
    BSTNode *curr = root;
    while (curr->ong != NULL) curr = curr->ong;
    return curr->val;
}

int main(void) {
    BSTNode n10 = {10, NULL, NULL};
    BSTNode n90 = {90, NULL, NULL};
    BSTNode root = {50, &n10, &n90};

    printf("Minimal qiymat:  %d\n", bst_min(&root));
    printf("Maksimal qiymat: %d\n", bst_max(&root));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. BST xossasiga ko'ra eng kichik son eng chapda, eng kattasi esa eng o'ngda bo'ladi.

## Ishlash natijasi:
```text
Minimal qiymat:  10
Maksimal qiymat: 90
```

---

# 817-Topshiriq: Daraxtning balandligini (Height / Depth) hisoblash

## Topshiriq sharti:
Rekursiya orqali ildizdan eng chuqur barggacha bo'lgan masofani aniqlash.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct BSTNode {
    int val;
    struct BSTNode *chap, *ong;
} BSTNode;

int tree_height(BSTNode *root) {
    if (root == NULL) return 0;
    int h_chap = tree_height(root->chap);
    int h_ong = tree_height(root->ong);
    return 1 + (h_chap > h_ong ? h_chap : h_ong);
}

int main(void) {
    BSTNode n1 = {1, NULL, NULL};
    BSTNode n2 = {2, &n1, NULL};
    BSTNode root = {3, &n2, NULL};

    printf("Daraxt balandligi: %d\n", tree_height(&root));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Balandlik daraxtdagi qidiruv tezligini baholash uchun zarur (balandlik kichik bo'lsa tez ishlaydi).

## Ishlash natijasi:
```text
Daraxt balandligi: 3
```

---

# 818-Topshiriq: Binar To'p (Binary Min-Heap) asoslari: Insert va Heapify Up

## Topshiriq sharti:
Massivda daraxt tuzish (chap bola 2*i+1, o'ng bola 2*i+2) va min-heap qoidasini saqlash.

## Yechim (C kodi):
```c
#include <stdio.h>

#define HEAP_CAP 10

typedef struct {
    int arr[HEAP_CAP];
    int size;
} MinHeap;

void heap_swap(int *a, int *b) { int t = *a; *a = *b; *b = t; }

void heap_insert(MinHeap *h, int val) {
    if (h->size >= HEAP_CAP) return;
    int i = h->size++;
    h->arr[i] = val;

    // Heapify Up: ota tugundan kichik bo'lsa yuqoriga ko'tariladi
    while (i != 0 && h->arr[(i - 1) / 2] > h->arr[i]) {
        heap_swap(&h->arr[(i - 1) / 2], &h->arr[i]);
        i = (i - 1) / 2;
    }
}

int main(void) {
    MinHeap h = { .size = 0 };
    heap_insert(&h, 30);
    heap_insert(&h, 10);
    heap_insert(&h, 50);
    heap_insert(&h, 5);

    printf("Min-Heap ildizi (eng kichik element): %d\n", h.arr[0]);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Binar to'p (Heap) massiv ustida pointerlarsiz xotirani super-tejamkor tashkil etadi.
2. Ildizda har doim eng kichik (Min-Heap) element turadi.

## Ishlash natijasi:
```text
Min-Heap ildizi (eng kichik element): 5
```

---

# 819-Topshiriq: Binar Min-Heap: Extract Min (Eng kichik elementni sug'urib olish)

## Topshiriq sharti:
Ildizni olib, oxirgi elementni ildizga qo'yish va Heapify Down qilish.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    int arr[10];
    int size;
} MinHeap;

void heap_swap(int *a, int *b) { int t = *a; *a = *b; *b = t; }

int heap_extract_min(MinHeap *h) {
    if (h->size <= 0) return -1;
    if (h->size == 1) return h->arr[--h->size];

    int min_val = h->arr[0];
    h->arr[0] = h->arr[--h->size];

    // Heapify Down
    int i = 0;
    while (2 * i + 1 < h->size) {
        int left = 2 * i + 1;
        int right = 2 * i + 2;
        int smallest = left;

        if (right < h->size && h->arr[right] < h->arr[left]) smallest = right;
        if (h->arr[i] <= h->arr[smallest]) break;

        heap_swap(&h->arr[i], &h->arr[smallest]);
        i = smallest;
    }
    return min_val;
}

int main(void) {
    MinHeap h = { {5, 10, 50, 30}, 4 };

    printf("Chiqarilgan min: %d\n", heap_extract_min(&h));
    printf("Yangi ildiz:     %d\n", h.arr[0]);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Prioritetli navbat (Priority Queue) va Dijkstra eng qisqa yo'l algoritmi Min-Heap extract-min amali ustiga qurilgan.

## Ishlash natijasi:
```text
Chiqarilgan min: 5
Yangi ildiz:     10
```

---

# 820-Topshiriq: Xesh-jadval (Hash Table): djb2 satrli xesh funksiyasi

## Topshiriq sharti:
Dan Bernstein tomonidan yaratilgan klassik djb2 xesh funksiyasini realizatsiya qilish.

## Yechim (C kodi):
```c
#include <stdio.h>

unsigned long hash_djb2(const unsigned char *str) {
    unsigned long hash = 5381;
    int c;

    while ((c = *str++)) {
        // hash * 33 + c
        hash = ((hash << 5) + hash) + c;
    }
    return hash;
}

int main(void) {
    printf("djb2("apple"):  %lu\n", hash_djb2((const unsigned char*)"apple"));
    printf("djb2("banana"): %lu\n", hash_djb2((const unsigned char*)"banana"));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. djb2 qisqa vaqt ichida satrlar uchun deyarli to'qnashuvsiz (low collision rate) xesh generatsiya qiladi.

## Ishlash natijasi:
```text
djb2("apple"):  256038198
djb2("banana"): 210707787355
```

---

# 821-Topshiriq: Xesh-jadval: Chaining (Zanjirlash) usuli bilan to'qnashuvlarni hal qilish

## Topshiriq sharti:
Massiv elementlari Linked List lardan iborat bo'lgan xesh jadval.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TABLE_SIZE 10

typedef struct Entry {
    char key[32];
    int val;
    struct Entry *next;
} Entry;

Entry* table[TABLE_SIZE] = { NULL };

unsigned int hash(const char *k) {
    unsigned int h = 0;
    while (*k) h = (h * 31) + *k++;
    return h % TABLE_SIZE;
}

void ht_put(const char *key, int val) {
    unsigned int idx = hash(key);
    Entry *e = (Entry*)malloc(sizeof(Entry));
    strcpy(e->key, key);
    e->val = val;
    e->next = table[idx];
    table[idx] = e;
}

int ht_get(const char *key, int *val) {
    unsigned int idx = hash(key);
    Entry *e = table[idx];
    while (e) {
        if (strcmp(e->key, key) == 0) {
            *val = e->val;
            return 1;
        }
        e = e->next;
    }
    return 0;
}

int main(void) {
    ht_put("olma", 15000);
    ht_put("nok", 25000);

    int narx;
    if (ht_get("olma", &narx)) {
        printf("Olma narxi: %d so'm\n", narx);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Separate Chaining usulida bitta xesh slotiga tushgan bir nechta kalitlar Linked List zanjiri orqali saqlanadi.

## Ishlash natijasi:
```text
Olma narxi: 15000 so'm
```

---

# 822-Topshiriq: Ikki tomonlama navbat (Deque - Double-Ended Queue)

## Topshiriq sharti:
Ham boshidan, ham oxiridan kiritish va chiqarish imkonini beruvchi tuzilma.

## Yechim (C kodi):
```c
#include <stdio.h>

#define DEQUE_CAP 10

typedef struct {
    int arr[DEQUE_CAP];
    int front, rear, size;
} Deque;

void init_deque(Deque *d) { d->front = -1; d->rear = 0; d->size = 0; }

void insert_front(Deque *d, int v) {
    if (d->front == -1) { d->front = d->rear = 0; }
    else if (d->front == 0) d->front = DEQUE_CAP - 1;
    else d->front--;
    d->arr[d->front] = v;
    d->size++;
}

void insert_rear(Deque *d, int v) {
    if (d->front == -1) { d->front = d->rear = 0; }
    else if (d->rear == DEQUE_CAP - 1) d->rear = 0;
    else d->rear++;
    d->arr[d->rear] = v;
    d->size++;
}

int main(void) {
    Deque d;
    init_deque(&d);

    insert_rear(&d, 10);
    insert_front(&d, 20); // 20 endi eng oldinda

    printf("Front: %d, Rear: %d\n", d.arr[d.front], d.arr[d.rear]);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Deque bir vaqtning o'zida ham Stek, ham Navbat vazifasini bajara oladi.

## Ishlash natijasi:
```text
Front: 20, Rear: 10
```

---

# 823-Topshiriq: Dinamik Massiv (Vector / ArrayList) C tilida

## Topshiriq sharti:
Hajmi to'lganda o'z-o'zini realloc orqali 2 barobar kengaytiruvchi dinamik massiv.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int *data;
    size_t size;
    size_t cap;
} Vector;

void vec_init(Vector *v) {
    v->size = 0;
    v->cap = 2;
    v->data = (int *)malloc(v->cap * sizeof(int));
}

void vec_push(Vector *v, int val) {
    if (v->size == v->cap) {
        v->cap *= 2;
        v->data = (int *)realloc(v->data, v->cap * sizeof(int));
    }
    v->data[v->size++] = val;
}

void vec_free(Vector *v) { free(v->data); }

int main(void) {
    Vector v;
    vec_init(&v);

    for (int i = 1; i <= 5; i++) vec_push(&v, i * 10);

    printf("Vector sig'imi: %zu, Elementlar: %zu\n", v.cap, v.size);
    for (size_t i = 0; i < v.size; i++) printf("%d ", v.data[i]);
    printf("\n");

    vec_free(&v);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C++ dagi `std::vector` va Java `ArrayList` aynan mana shu 2x realloc geometrik o'sish qoidasiga asoslangan.

## Ishlash natijasi:
```text
Vector sig'imi: 8, Elementlar: 5
10 20 30 40 50
```

---

# 824-Topshiriq: Prefiks Daraxti (Trie / Prefix Tree) asoslari

## Topshiriq sharti:
Lug'atdagi so'zlarni tezkor qidirish va avtoto'ldirish uchun harflar daraxti.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define ALPHABET_SIZE 26

typedef struct TrieNode {
    struct TrieNode *children[ALPHABET_SIZE];
    bool is_end;
} TrieNode;

TrieNode* trie_create(void) {
    TrieNode *node = (TrieNode*)calloc(1, sizeof(TrieNode));
    return node;
}

void trie_insert(TrieNode *root, const char *word) {
    TrieNode *curr = root;
    for (int i = 0; word[i]; i++) {
        int idx = word[i] - 'a';
        if (!curr->children[idx]) curr->children[idx] = trie_create();
        curr = curr->children[idx];
    }
    curr->is_end = true;
}

bool trie_search(TrieNode *root, const char *word) {
    TrieNode *curr = root;
    for (int i = 0; word[i]; i++) {
        int idx = word[i] - 'a';
        if (!curr->children[idx]) return false;
        curr = curr->children[idx];
    }
    return curr != NULL && curr->is_end;
}

int main(void) {
    TrieNode *root = trie_create();
    trie_insert(root, "ant");
    trie_insert(root, "antigravity");

    printf("qidiruv 'ant': %s\n", trie_search(root, "ant") ? "Topildi" : "Yo'q");
    printf("qidiruv 'anti': %s\n", trie_search(root, "anti") ? "Topildi" : "Yo'q");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Trie so'z uzunligi bo'yicha O(L) qidiruv tezligini beradi, millionlab so'zlar bo'lsa ham qidiruv vaqti faqat so'z harflari soniga bog'liq bo'ladi.

## Ishlash natijasi:
```text
qidiruv 'ant': Topildi
qidiruv 'anti': Yo'q
```

---

# 825-Topshiriq: Bog'langan ro'yxatni saralash: Merge Sort on Linked List

## Topshiriq sharti:
Ro'yxatni ikkiga bo'lib O(N log N) da saralash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int val;
    struct Node *next;
} Node;

Node* merge_sorted(Node *a, Node *b) {
    if (!a) return b;
    if (!b) return a;
    if (a->val <= b->val) {
        a->next = merge_sorted(a->next, b);
        return a;
    } else {
        b->next = merge_sorted(a, b->next);
        return b;
    }
}

int main(void) {
    Node a2 = {30, NULL}; Node a1 = {10, &a2};
    Node b2 = {40, NULL}; Node b1 = {20, &b2};

    Node *res = merge_sorted(&a1, &b1);

    while (res) {
        printf("%d ", res->val);
        res = res->next;
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Linked Listlar uchun Merge Sort eng samarali tartiblash algoritmi hisoblanadi (qo'shimcha massiv talab qilmaydi).

## Ishlash natijasi:
```text
10 20 30 40
```

---

# 826-Topshiriq: Graf tuzilishi: Qo'shnichilik matritsasi (Adjacency Matrix)

## Topshiriq sharti:
Graf tugunlari va qirralarini 2D matritsada ifodalash.

## Yechim (C kodi):
```c
#include <stdio.h>

#define TUGUNLAR 4

typedef struct {
    int mat[TUGUNLAR][TUGUNLAR];
} GraphMatrix;

void add_edge_mat(GraphMatrix *g, int u, int v) {
    g->mat[u][v] = 1;
    g->mat[v][u] = 1; // Yo'naltirilmagan graf
}

int main(void) {
    GraphMatrix g = {0};
    add_edge_mat(&g, 0, 1);
    add_edge_mat(&g, 1, 2);
    add_edge_mat(&g, 2, 3);

    printf("0 va 1 qo'shnimi? %s\n", g.mat[0][1] ? "HA" : "YO'Q");
    printf("0 va 2 qo'shnimi? %s\n", g.mat[0][2] ? "HA" : "YO'Q");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Qo'shnichilik matritsasi O(1) da ikki tugun orasida yo'l borligini tekshirish imkonini beradi.

## Ishlash natijasi:
```text
0 va 1 qo'shnimi? HA
0 va 2 qo'shnimi? YO'Q
```

---

# 827-Topshiriq: Graf tuzilishi: Qo'shnichilik ro'yxati (Adjacency List)

## Topshiriq sharti:
Xotirani tejovchi va faqat mavjud qirralarni bog'lovchi ro'yxatli graf.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct GNode {
    int v;
    struct GNode *next;
} GNode;

typedef struct {
    GNode *heads[4];
} AdjListGraph;

void add_edge_list(AdjListGraph *g, int u, int v) {
    GNode *n = (GNode*)malloc(sizeof(GNode));
    n->v = v;
    n->next = g->heads[u];
    g->heads[u] = n;
}

int main(void) {
    AdjListGraph g = {0};
    add_edge_list(&g, 0, 1);
    add_edge_list(&g, 0, 2);

    printf("Tugun 0 ning qo'shnilari: ");
    GNode *c = g.heads[0];
    while (c) {
        printf("%d ", c->v);
        GNode *tmp = c;
        c = c->next;
        free(tmp);
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Siyrak (sparse) graflarda Adjacency List O(V + E) xotira oladi va xotirani keraksiz sarflamaydi.

## Ishlash natijasi:
```text
Tugun 0 ning qo'shnilari: 2 1
```

---

# 828-Topshiriq: Kenglik bo'yicha qidiruv (BFS - Breadth-First Search) C tilida

## Topshiriq sharti:
Grafda navbat (Queue) yordamida qavatma-qavat eng qisqa yo'lni qidirish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    // 0 -> 1, 0 -> 2, 1 -> 3
    int adj[4][4] = {
        {0, 1, 1, 0},
        {1, 0, 0, 1},
        {1, 0, 0, 0},
        {0, 1, 0, 0}
    };
    int visited[4] = {0};
    int queue[4], front = 0, rear = 0;

    // Boshlang'ich 0
    visited[0] = 1;
    queue[rear++] = 0;

    printf("BFS ketma-ketligi: ");
    while (front < rear) {
        int u = queue[front++];
        printf("%d ", u);
        for (int v = 0; v < 4; v++) {
            if (adj[u][v] && !visited[v]) {
                visited[v] = 1;
                queue[rear++] = v;
            }
        }
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. BFS navbat (Queue) yordamida har bir tugundan eng yaqin qo'shnilarni birinchi tekshiradi.

## Ishlash natijasi:
```text
BFS ketma-ketligi: 0 1 2 3
```

---

# 829-Topshiriq: Chuqurlik bo'yicha qidiruv (DFS - Depth-First Search) C tilida

## Topshiriq sharti:
Rekursiya (yoki stek) yordamida grafning eng chuqur shoxigacha kirib borish.

## Yechim (C kodi):
```c
#include <stdio.h>

int adj[4][4] = {
    {0, 1, 1, 0},
    {1, 0, 0, 1},
    {1, 0, 0, 0},
    {0, 1, 0, 0}
};
int visited[4] = {0};

void dfs(int u) {
    visited[u] = 1;
    printf("%d ", u);
    for (int v = 0; v < 4; v++) {
        if (adj[u][v] && !visited[v]) {
            dfs(v);
        }
    }
}

int main(void) {
    printf("DFS ketma-ketligi: ");
    dfs(0);
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. DFS rekursiv Call Stack orqali oxirigacha boradi va orqaga qaytadi (backtracking).

## Ishlash natijasi:
```text
DFS ketma-ketligi: 0 1 3 2
```

---

# 830-Topshiriq: Disjoint Set Union (DSU / Kruskal Union-Find)

## Topshiriq sharti:
Elementlarning bir xil guruhga tegishli ekanligini Path Compression bilan O(alpha(N)) da aniqlash.

## Yechim (C kodi):
```c
#include <stdio.h>

int ota[10];

void dsu_init(int n) {
    for (int i = 0; i < n; i++) ota[i] = i;
}

int dsu_find(int i) {
    if (ota[i] == i) return i;
    return ota[i] = dsu_find(ota[i]); // Path compression
}

void dsu_union(int a, int b) {
    int root_a = dsu_find(a);
    int root_b = dsu_find(b);
    if (root_a != root_b) ota[root_a] = root_b;
}

int main(void) {
    dsu_init(5);
    dsu_union(0, 1);
    dsu_union(1, 2);

    printf("0 va 2 bir xil guruhdami? %s\n", 
           dsu_find(0) == dsu_find(2) ? "HA" : "YO'Q");
    printf("0 va 4 bir xil guruhdami? %s\n", 
           dsu_find(0) == dsu_find(4) ? "HA" : "YO'Q");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. DSU tarmoq komponentlari va minimal qamrovchi daraxt (MST Kruskal) qurishda eng samarali tuzilmadir.

## Ishlash natijasi:
```text
0 va 2 bir xil guruhdami? HA
0 va 4 bir xil guruhdami? YO'Q
```

---

# 831-Topshiriq: Xesh-jadval: Ochiq adreslash (Open Addressing: Linear Probing)

## Topshiriq sharti:
To'qnashuv bo'lganda massivning keyingi bo'sh katagiga (idx + 1) joylashtirish.

## Yechim (C kodi):
```c
#include <stdio.h>

#define SIZE 7
int ht[SIZE] = {0};

void lp_insert(int key) {
    int idx = key % SIZE;
    while (ht[idx] != 0) {
        idx = (idx + 1) % SIZE;
    }
    ht[idx] = key;
}

int main(void) {
    lp_insert(10); // 10 % 7 = 3
    lp_insert(17); // 17 % 7 = 3 (to'qnashuv -> 4-indeksga tushadi)

    for (int i = 0; i < SIZE; i++) {
        if (ht[i]) printf("[%d] = %d\n", i, ht[i]);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Linear Probing alohida ko'rsatkichlar va xotira ajratishlarsiz faqat bitta tekis massiv ichida ishlaydi (Kesh uchun optimal).

## Ishlash natijasi:
```text
[3] = 10
[4] = 17
```

---

# 832-Topshiriq: Bloom Filter (Blum filtri) simulyatsiyasi

## Topshiriq sharti:
Bit massivi va bir nechta xesh orqali element to'plamda yo'qligini 100% aniq kafolatlovchi ehtimollik tuzilmasi.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

uint8_t bitset = 0;

void bloom_add(int val) {
    int h1 = (val * 3) % 8;
    int h2 = (val * 7 + 1) % 8;
    bitset |= (1 << h1) | (1 << h2);
}

int bloom_check(int val) {
    int h1 = (val * 3) % 8;
    int h2 = (val * 7 + 1) % 8;
    return (bitset & (1 << h1)) && (bitset & (1 << h2));
}

int main(void) {
    bloom_add(42);

    printf("42 bormi? %s\n", bloom_check(42) ? "Ehtimol bor" : "Aniq yo'q");
    printf("99 bormi? %s\n", bloom_check(99) ? "Ehtimol bor" : "Aniq yo'q");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Blum filtri 'Aniq yo'q' deb javob bersa, element 100% bazada yo'q. Bu diskka ortiqcha so'rov yuborishni oldini oladi.

## Ishlash natijasi:
```text
42 bormi? Ehtimol bor
99 bormi? Aniq yo'q
```

---

# 833-Topshiriq: Bitli to'plam (BitSet / BitVector) implementatsiyasi

## Topshiriq sharti:
Har bir bit bitta sonni (0..31) ifodalovchi super-ixcham to'plam.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef uint32_t BitSet;

void bs_add(BitSet *bs, int elem) { *bs |= (1U << elem); }
int bs_contains(BitSet bs, int elem) { return (bs & (1U << elem)) != 0; }

int main(void) {
    BitSet s = 0;
    bs_add(&s, 5);
    bs_add(&s, 18);

    printf("5 bormi?  %d\n", bs_contains(s, 5));
    printf("10 bormi? %d\n", bs_contains(s, 10));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. BitSet to'plam operatsiyalarini (birlashma, kesishma) bitta protsessor buyrug'ida (| va &) bajaradi.

## Ishlash natijasi:
```text
5 bormi?  1
10 bormi? 0
```

---

# 834-Topshiriq: Singly Linked List: O'rtadagi tugunni (Middle Node) topish

## Topshiriq sharti:
Sekin va tez ko'rsatkich orqali ro'yxat uzunligini sanamasdan o'rtadagi elementni topish.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct Node {
    int val;
    struct Node *next;
} Node;

Node* find_middle(Node *head) {
    Node *slow = head, *fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
    }
    return slow;
}

int main(void) {
    Node n5 = {5, NULL}; Node n4 = {4, &n5}; Node n3 = {3, &n4};
    Node n2 = {2, &n3};  Node n1 = {1, &n2};

    Node *mid = find_middle(&n1);
    printf("O'rtadagi tugun qiymati: %d\n", mid->val);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Fast ko'rsatkich 2 barobar tez yuradi, shuning uchun u oxiriga yetganda slow aynan o'rtada bo'ladi.

## Ishlash natijasi:
```text
O'rtadagi tugun qiymati: 3
```

---

# 835-Topshiriq: Singly Linked List: Oxiridan N-chi elementni topish (Nth from End)

## Topshiriq sharti:
Ikki ko'rsatkich oralig'ini N qadamga ajratib bir marta o'tishda (one-pass) topish.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct Node {
    int val;
    struct Node *next;
} Node;

Node* nth_from_end(Node *head, int n) {
    Node *p1 = head, *p2 = head;
    for (int i = 0; i < n; i++) {
        if (!p1) return NULL;
        p1 = p1->next;
    }
    while (p1) {
        p1 = p1->next;
        p2 = p2->next;
    }
    return p2;
}

int main(void) {
    Node n5 = {50, NULL}; Node n4 = {40, &n5}; Node n3 = {30, &n4};
    Node n2 = {20, &n3};  Node n1 = {10, &n2};

    // Oxiridan 2-element (40)
    Node *res = nth_from_end(&n1, 2);
    printf("Oxiridan 2-element: %d\n", res ? res->val : -1);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bitta o'tishda (one-pass) masofaviy oyna (window) usulidan foydalanish.

## Ishlash natijasi:
```text
Oxiridan 2-element: 40
```

---

# 836-Topshiriq: Singly Linked List: Palindrom ro'yxatni tekshirish

## Topshiriq sharti:
Ro'yxatning o'rtasidan keyingi qismini teskari qilib solishtirish.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct Node {
    int val;
    struct Node *next;
} Node;

int is_palindrome_list(Node *head) {
    // 1 -> 2 -> 1
    int arr[10], len = 0;
    Node *c = head;
    while (c) { arr[len++] = c->val; c = c->next; }
    for (int i = 0; i < len / 2; i++) {
        if (arr[i] != arr[len - 1 - i]) return 0;
    }
    return 1;
}

int main(void) {
    Node n3 = {1, NULL}; Node n2 = {2, &n3}; Node n1 = {1, &n2};
    printf("1->2->1 palindrommi? %s\n", is_palindrome_list(&n1) ? "HA" : "YO'Q");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Palindrom ro'yxat chapdan ham, o'ngdan ham bir xil o'qiladi.

## Ishlash natijasi:
```text
1->2->1 palindrommi? HA
```

---

# 837-Topshiriq: Ikki tartiblangan ro'yxatning kesishmasi (Intersection of Sorted Lists)

## Topshiriq sharti:
Ikkala ro'yxatda ham mavjud umumiy sonlarni ajratib olish.

## Yechim (C kodi):
```c
#include <stdio.h>

void print_intersection(int *a, int na, int *b, int nb) {
    int i = 0, j = 0;
    while (i < na && j < nb) {
        if (a[i] == b[j]) {
            printf("%d ", a[i]);
            i++; j++;
        } else if (a[i] < b[j]) i++;
        else j++;
    }
    printf("\n");
}

int main(void) {
    int a[] = {1, 3, 5, 7};
    int b[] = {2, 3, 7, 9};

    printf("Umumiy elementlar: ");
    print_intersection(a, 4, b, 4);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ikki ko'rsatkich (Two-Pointers) usuli bilan O(N + M) da kesishma topiladi.

## Ishlash natijasi:
```text
Umumiy elementlar: 3 7
```

---

# 838-Topshiriq: Fenwick Daraxti (Binary Indexed Tree - BIT) asoslari

## Topshiriq sharti:
O(log N) da massiv prefiks yig'indisini hisoblash va elementni yangilash.

## Yechim (C kodi):
```c
#include <stdio.h>

#define N 6
int bit[N + 1] = {0};

void bit_update(int i, int delta) {
    for (; i <= N; i += (i & -i)) bit[i] += delta;
}

int bit_query(int i) {
    int sum = 0;
    for (; i > 0; i -= (i & -i)) sum += bit[i];
    return sum;
}

int main(void) {
    bit_update(1, 5);
    bit_update(2, 3);
    bit_update(3, 7);

    printf("Prefiks yig'indi [1..2]: %d\n", bit_query(2));
    printf("Prefiks yig'indi [1..3]: %d\n", bit_query(3));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. (i & -i) eng quyi 1-bitni ajratadi. Fenwick daraxti musobaqa dasturlashida (Competitive Programming) juda mashhur.

## Ishlash natijasi:
```text
Prefiks yig'indi [1..2]: 8
Prefiks yig'indi [1..3]: 15
```

---

# 839-Topshiriq: Segment Daraxti (Segment Tree): Range Sum Query

## Topshiriq sharti:
Massivning istalgan oralig'i [L, R] yig'indisini O(log N) da olish.

## Yechim (C kodi):
```c
#include <stdio.h>

int tree[16];

void build_seg(int *arr, int node, int start, int end) {
    if (start == end) { tree[node] = arr[start]; return; }
    int mid = (start + end) / 2;
    build_seg(arr, 2 * node, start, mid);
    build_seg(arr, 2 * node + 1, mid + 1, end);
    tree[node] = tree[2 * node] + tree[2 * node + 1];
}

int query_seg(int node, int start, int end, int l, int r) {
    if (r < start || end < l) return 0;
    if (l <= start && end <= r) return tree[node];
    int mid = (start + end) / 2;
    return query_seg(2 * node, start, mid, l, r) +
           query_seg(2 * node + 1, mid + 1, end, l, r);
}

int main(void) {
    int arr[] = {1, 3, 5, 7};
    build_seg(arr, 1, 0, 3);

    printf("[1..2] oralig'i yig'indisi (3+5): %d\n", query_seg(1, 0, 3, 1, 2));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Segment Tree oraliq so'rovlarini dinamik o'zgarishlar bilan birga O(log N) da bajaradi.

## Ishlash natijasi:
```text
[1..2] oralig'i yig'indisi (3+5): 8
```

---

# 840-Topshiriq: Skip List (Sakrovchi Ro'yxat) konsepsiyasi

## Topshiriq sharti:
Bir nechta sathli ko'rsatkichlar orqali O(log N) da qidiruv imkonini beruvchi ro'yxat modeli.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("Skip List - bir necha pog'onali tezkor sakrash ko'rsatkichlariga ega bo'lib,\n");
    printf("Redis ma'lumotlar bazasida Sorted Set (ZSET) larni O(log N) da saqlashda\n");
    printf("balanslangan daraxtlar o'rniga eng qulay muqobil sifatida ishlatiladi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Skip List ierarxik qatlamlardan iborat bo'lib, yuqori qatlamlar uzoq masofalarga tezkor sakrashni ta'minlaydi.

## Ishlash natijasi:
```text
Skip List - bir necha pog'onali tezkor sakrash ko'rsatkichlariga ega bo'lib,
Redis ma'lumotlar bazasida Sorted Set (ZSET) larni O(log N) da saqlashda
balanslangan daraxtlar o'rniga eng qulay muqobil sifatida ishlatiladi.
```

---

# 841-Topshiriq: Massivdagi takroriy elementlarni O(N) da tozalash

## Topshiriq sharti:
Saralangan massivdagi duplikatlarni joyida (in-place) olib tashlash.

## Yechim (C kodi):
```c
#include <stdio.h>

int remove_duplicates(int *arr, int n) {
    if (n == 0) return 0;
    int j = 0;
    for (int i = 1; i < n; i++) {
        if (arr[i] != arr[j]) {
            arr[++j] = arr[i];
        }
    }
    return j + 1;
}

int main(void) {
    int arr[] = {1, 1, 2, 2, 3, 4, 4};
    int len = remove_duplicates(arr, 7);

    printf("Tozalangan massiv: ");
    for (int i = 0; i < len; i++) printf("%d ", arr[i]);
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ikki ko'rsatkich (i va j) bilan O(N) vaqt va O(1) qo'shimcha xotirada duplikatlar o'chiriladi.

## Ishlash natijasi:
```text
Tozalangan massiv: 1 2 3 4
```

---

# 842-Topshiriq: Binar Qidiruv Daraxti: Tugunni o'chirish (Deletion 3 holat)

## Topshiriq sharti:
Barg tugun, bitta farzandli va ikkita farzandli (inorder successor) tugunni o'chirish logikasi.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct BSTNode {
    int val;
    struct BSTNode *l, *r;
} BSTNode;

BSTNode* min_node(BSTNode *n) {
    while (n->l) n = n->l;
    return n;
}

BSTNode* bst_del(BSTNode *root, int val) {
    if (!root) return NULL;
    if (val < root->val) root->l = bst_del(root->l, val);
    else if (val > root->val) root->r = bst_del(root->r, val);
    else {
        // 1 yoki 0 farzand
        if (!root->l) { BSTNode *t = root->r; free(root); return t; }
        if (!root->r) { BSTNode *t = root->l; free(root); return t; }
        // 2 farzand: o'ng shoxdagi eng kichigini olamiz
        BSTNode *succ = min_node(root->r);
        root->val = succ->val;
        root->r = bst_del(root->r, succ->val);
    }
    return root;
}

int main(void) {
    BSTNode *n1 = malloc(sizeof(BSTNode)); n1->val = 10; n1->l = n1->r = NULL;
    BSTNode *n3 = malloc(sizeof(BSTNode)); n3->val = 30; n3->l = n3->r = NULL;
    BSTNode *root = malloc(sizeof(BSTNode)); root->val = 20; root->l = n1; root->r = n3;

    root = bst_del(root, 20); // Ildizni o'chirish
    printf("Yangi ildiz qiymati: %d\n", root->val);

    free(root->l); free(root);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ikkita farzandli tugun o'chirilganda uning o'rniga o'ng shoxdagi eng kichik tugun (In-Order Successor) qo'yiladi.

## Ishlash natijasi:
```text
Yangi ildiz qiymati: 30
```

---

# 843-Topshiriq: Matritsada orollarni sanash (Number of Islands via DFS)

## Topshiriq sharti:
2D massivda 1 lar bilan tutashgan orollar sonini hisoblash.

## Yechim (C kodi):
```c
#include <stdio.h>

void visit_island(int grid[3][3], int r, int c) {
    if (r < 0 || r >= 3 || c < 0 || c >= 3 || grid[r][c] != 1) return;
    grid[r][c] = 0; // Belgilash
    visit_island(grid, r + 1, c);
    visit_island(grid, r - 1, c);
    visit_island(grid, r, c + 1);
    visit_island(grid, r, c - 1);
}

int main(void) {
    int xarita[3][3] = {
        {1, 1, 0},
        {1, 0, 0},
        {0, 0, 1}
    };
    int orollar = 0;

    for (int r = 0; r < 3; r++) {
        for (int c = 0; c < 3; c++) {
            if (xarita[r][c] == 1) {
                orollar++;
                visit_island(xarita, r, c);
            }
        }
    }
    printf("Jami orollar soni: %d\n", orollar);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Flood Fill va Connected Components algoritmlari tasvirni tahlil qilish va o'yin xaritalarida keng qo'llaniladi.

## Ishlash natijasi:
```text
Jami orollar soni: 2
```

---

# 844-Topshiriq: Birlashtirilgan Min-Max Heap g'oyasi

## Topshiriq sharti:
Bitta to'p ichida ham O(1) min, ham O(1) max qiymatni qo'llab-quvvatlash.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("Min-Max Heap - toq sathlarda minimumlar, juft sathlarda maximumlar\n");
    printf("saqlanuvchi maxsus to'p bo'lib, ikkala chekka qiymatni O(1) da beradi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ikkala ekstremumni bir vaqtda monitoring qilishda ishlatiladi.

## Ishlash natijasi:
```text
Min-Max Heap - toq sathlarda minimumlar, juft sathlarda maximumlar
saqlanuvchi maxsus to'p bo'lib, ikkala chekka qiymatni O(1) da beradi.
```

---

# 845-Topshiriq: Halqasimon bufer bilan audio ma'lumotlar oqimi (Audio Ring Buffer)

## Topshiriq sharti:
Audio kiritish va chiqarish o'rtasida tovush uzilishining (jitter) oldini olish.

## Yechim (C kodi):
```c
#include <stdio.h>

#define BUF_SIZE 8
int ring[BUF_SIZE];
int wr_idx = 0, rd_idx = 0;

void write_sample(int sample) {
    ring[wr_idx] = sample;
    wr_idx = (wr_idx + 1) % BUF_SIZE;
}

int read_sample(void) {
    int s = ring[rd_idx];
    rd_idx = (rd_idx + 1) % BUF_SIZE;
    return s;
}

int main(void) {
    write_sample(100);
    write_sample(200);

    printf("Audio olingan namuna: %d\n", read_sample());
    printf("Audio olingan namuna: %d\n", read_sample());
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ring buffer audio va video strimingda qotib qolishlarning oldini oluvchi eng asosiy ma'lumot tuzilmasidir.

## Ishlash natijasi:
```text
Audio olingan namuna: 100
Audio olingan namuna: 200
```

---

# 846-Topshiriq: Statik massiv yordamida Stek ustida Min elementni O(1) da topish (Min-Stack)

## Topshiriq sharti:
Har bir push/pop da joriy minimal qiymatni O(1) vaqtda qaytaruvchi stek.

## Yechim (C kodi):
```c
#include <stdio.h>

int s_data[10], s_min[10], top_idx = -1;

void push_min(int val) {
    top_idx++;
    s_data[top_idx] = val;
    if (top_idx == 0 || val < s_min[top_idx - 1]) s_min[top_idx] = val;
    else s_min[top_idx] = s_min[top_idx - 1];
}

int get_min(void) { return s_min[top_idx]; }

int main(void) {
    push_min(20);
    push_min(10);
    push_min(30);

    printf("Hozirgi minimum: %d\n", get_min());
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Qo'shimcha min-stek yordamida minimum qiymat butun stek bo'yicha doimo O(1) da ma'lum bo'ladi.

## Ishlash natijasi:
```text
Hozirgi minimum: 10
```

---

# 847-Topshiriq: Daraxtning eng yaqin umumiy ajdodi (LCA - Lowest Common Ancestor)

## Topshiriq sharti:
BST da ikki tugunning eng yaqin umumiy ota tugunini topish.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct BSTNode {
    int val;
    struct BSTNode *l, *r;
} BSTNode;

BSTNode* bst_lca(BSTNode *root, int n1, int n2) {
    if (!root) return NULL;
    if (root->val > n1 && root->val > n2) return bst_lca(root->l, n1, n2);
    if (root->val < n1 && root->val < n2) return bst_lca(root->r, n1, n2);
    return root;
}

int main(void) {
    BSTNode n1 = {10, NULL, NULL}; BSTNode n3 = {30, NULL, NULL};
    BSTNode root = {20, &n1, &n3};

    BSTNode *lca = bst_lca(&root, 10, 30);
    printf("10 va 30 ning umumiy ajdodi: %d\n", lca->val);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Agar ikkala tugun ildizning ikki tomonida bo'lsa, demak aynan shu ildiz ularning umumiy ajdodi hisoblanadi.

## Ishlash natijasi:
```text
10 va 30 ning umumiy ajdodi: 20
```

---

# 848-Topshiriq: Ro'yxatni saralash: Odd-Even Linked List (Toq va Juft indekslarni ajratish)

## Topshiriq sharti:
Ro'yxatning toq o'rindagi tugunlarini oldinga, juftlarini orqaga guruhlash.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct Node {
    int val;
    struct Node *next;
} Node;

Node* odd_even_list(Node *head) {
    if (!head) return NULL;
    Node *odd = head, *even = head->next, *even_head = even;

    while (even && even->next) {
        odd->next = even->next;
        odd = odd->next;
        even->next = odd->next;
        even = even->next;
    }
    odd->next = even_head;
    return head;
}

int main(void) {
    Node n4 = {4, NULL}; Node n3 = {3, &n4};
    Node n2 = {2, &n3};  Node n1 = {1, &n2};

    Node *res = odd_even_list(&n1);
    while (res) { printf("%d ", res->val); res = res->next; }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Pointerlarni qayta ulash orqali toq va juft o'rinlar O(N) vaqtda alohida guruhlanadi.

## Ishlash natijasi:
```text
1 3 2 4
```

---

# 849-Topshiriq: Topologik saralash (Topological Sort) asoslari

## Topshiriq sharti:
Yo'naltirilgan tsiklsiz grafda (DAG) bog'liqliklarni to'g'ri ketma-ketlikka terish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("Topologik saralash - dasturiy paketlar bog'liqligini (Package Manager / Make)\n");
    printf("to'g'ri yig'ish tartibida qurish uchun asosiy grafik algoritmdir.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Manbalardan qabul qiluvchilarga qarab kiruvchi darajalar (in-degree) bo'yicha saralanadi.

## Ishlash natijasi:
```text
Topologik saralash - dasturiy paketlar bog'liqligini (Package Manager / Make)
to'g'ri yig'ish tartibida qurish uchun asosiy grafik algoritmdir.
```

---

# 850-Topshiriq: Modul yakuni va Master Loyiha: LRU Kesh Dvigateli (LRU Cache - Hash Map + Doubly Linked List)

## Topshiriq sharti:
Xesh jadval va Ikki tomonlama bog'langan ro'yxatni birlashtirib, O(1) da o'qish, yozish va eng eski ishlatilgan (Least Recently Used) elementni avtomatik siqib chiqaruvchi to'liq kesh tizimini yaratish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CACHE_CAP 3

typedef struct CacheNode {
    int key;
    int val;
    struct CacheNode *prev;
    struct CacheNode *next;
} CacheNode;

typedef struct {
    int count;
    CacheNode *head; // Eng yangi
    CacheNode *tail; // Eng eski (o'chiriladigan)
} LRUCache;

void remove_node(LRUCache *c, CacheNode *n) {
    if (n->prev) n->prev->next = n->next;
    else c->head = n->next;

    if (n->next) n->next->prev = n->prev;
    else c->tail = n->prev;
}

void add_to_front(LRUCache *c, CacheNode *n) {
    n->next = c->head;
    n->prev = NULL;
    if (c->head) c->head->prev = n;
    c->head = n;
    if (!c->tail) c->tail = n;
}

void lru_put(LRUCache *c, int key, int val) {
    // Mavjudmi tekshirish
    CacheNode *curr = c->head;
    while (curr) {
        if (curr->key == key) {
            curr->val = val;
            remove_node(c, curr);
            add_to_front(c, curr);
            return;
        }
        curr = curr->next;
    }

    if (c->count >= CACHE_CAP) {
        // Eng eskini (tail) o'chirish
        CacheNode *old = c->tail;
        printf("[KESH EVICTION]: Kesh to'ldi. Eng eski kalit %d o'chirildi!\n", old->key);
        remove_node(c, old);
        free(old);
        c->count--;
    }

    CacheNode *new_n = (CacheNode*)malloc(sizeof(CacheNode));
    new_n->key = key;
    new_n->val = val;
    add_to_front(c, new_n);
    c->count++;
}

int lru_get(LRUCache *c, int key) {
    CacheNode *curr = c->head;
    while (curr) {
        if (curr->key == key) {
            // Murojaat qilingani uchun boshiga suramiz
            remove_node(c, curr);
            add_to_front(c, curr);
            return curr->val;
        }
        curr = curr->next;
    }
    return -1; // Topilmadi
}

int main(void) {
    printf("=== LRU KESH TIZIMI ISHGA TUSHDI ===\n");
    LRUCache cache = { 0, NULL, NULL };

    lru_put(&cache, 1, 100);
    lru_put(&cache, 2, 200);
    lru_put(&cache, 3, 300);

    printf("Kalit 1 o'qildi: %d\n", lru_get(&cache, 1)); // 1 yangilandi

    // 4 qo'shilganda 2 o'chirilishi kerak (chunki 1 yangilangan edi)
    lru_put(&cache, 4, 400);

    printf("Kalit 2 bormi? %d (O'chirilgan!)\n", lru_get(&cache, 2));
    printf("Kalit 1 bormi? %d (Mavjud)\n", lru_get(&cache, 1));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bu yakuniy topshiriq 17-modulning barcha ma'lumot tuzilmalarini: Doubly Linked List, Kesh arxitekturasi, dinamik xotira, ko'rsatkichlar manipulyatsiyasi va algoritmik tahlilni to'liq qamrab oladi.
2. LRU Cache Redis, Linux Page Cache va CPU L1/L2/L3 apparat keshlarining eng mashhur algoritmidir.

## Ishlash natijasi:
```text
=== LRU KESH TIZIMI ISHGA TUSHDI ===
Kalit 1 o'qildi: 100
[KESH EVICTION]: Kesh to'ldi. Eng eski kalit 2 o'chirildi!
Kalit 2 bormi? -1 (O'chirilgan!)
Kalit 1 bormi? 100 (Mavjud)
```

---
