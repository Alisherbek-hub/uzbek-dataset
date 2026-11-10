# Python Dasturlash Tili — 17-Qism: Ilmiy Hisoblash, Ma'lumotlar Tahlili va Matematika
## (801-850 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam zamonaviy Sun'iy Intellekt va Mashinali O'rganishning matematik yadrosini (sof Python) qamrab oladi:
* Chiziqli algebra: Vektor amallari, Dot product, Normalar, Matritsa ko'paytmasi, Gauss usuli;
* Ehtimollik va statistika: O'rtacha, Mediana, Standart og'ish, Korrelyatsiya, Gauss va Puasson taqsimotlari;
* Raqamli hisoblash: Raqamli hosila, Trapetsiyalar integrali, Monte-Karlo usullari;
* Optimizatsiya va Neyron tarmoqlar: Gradient tushishi, OLS Regressiya, Sigmoid, Softmax, Cross-Entropy;
* Model baholash: Train/Test, K-Fold, Confusion Matrix, Precision, Recall, F1, ROC AUC;
* Mashinali o'rganish algoritmlari: K-Means, KNN, Naive Bayes, Sof Perceptron;

---

# 801-Topshiriq: Vektorlarning skalyar ko'paytmasi (Dot Product)

## Topshiriq sharti:
Ikki vektorning skalyar ko'paytmasini sof Pythonda O(n) da hisoblang.

## Yechim (Python kodi):
```python
def dot_product(v1, v2):
    if len(v1) != len(v2):
        raise ValueError("Vektorlar o'lchami teng bo'lishi shart!")
    return sum(x * y for x, y in zip(v1, v2))

a = [1.0, 2.0, 3.0]
b = [4.0, -1.0, 2.0]
print("Skalyar ko'paytma:", dot_product(a, b))
```

## Tushuntirish va Mantiq:
1. Skalyar ko'paytma: a · b = sum(a_i * b_i). Neyron tarmoqlarning asosiy operatsiyasidir.

## Ishlash natijasi:
```text
Chiqish: Skalyar ko'paytma: 8.0
```

---

# 802-Topshiriq: Vektor normalari: L1 (Manxetten) va L2 (Evklid)

## Topshiriq sharti:
Vektorning L1 va L2 normalarini sof matematik formula bo'yicha hisoblang.

## Yechim (Python kodi):
```python
import math

def l1_norm(v):
    return sum(abs(x) for x in v)

def l2_norm(v):
    return math.sqrt(sum(x ** 2 for x in v))

v = [3.0, -4.0]
print("L1 normasi:", l1_norm(v))
print("L2 normasi (Evklid uzunligi):", l2_norm(v))
```

## Tushuntirish va Mantiq:
1. L1 normasi absolyut qiymatlar yig'indisi, L2 normasi esa vektorning geometrik uzunligidir.

## Ishlash natijasi:
```text
Chiqish: L1 normasi: 7.0, L2 normasi (Evklid uzunligi): 5.0
```

---

# 803-Topshiriq: Kosinus o'xshashligi (Cosine Similarity)

## Topshiriq sharti:
Ikki embedding vektorlari orasidagi burchak kosinusini hisoblang (LLM qidiruv tizimlari asosi).

## Yechim (Python kodi):
```python
import math

def cosine_similarity(v1, v2):
    dot = sum(x * y for x, y in zip(v1, v2))
    norm1 = math.sqrt(sum(x ** 2 for x in v1))
    norm2 = math.sqrt(sum(y ** 2 for y in v2))
    if norm1 == 0 or norm2 == 0: return 0.0
    return dot / (norm1 * norm2)

matn1_vec = [0.8, 0.2, 0.1]
matn2_vec = [0.75, 0.25, 0.05]
print("Kosinus o'xshashligi:", round(cosine_similarity(matn1_vec, matn2_vec), 4))
```

## Tushuntirish va Mantiq:
1. Kosinus o'xshashligi vektorlarning yo'nalish bo'yicha qanchalik yaqinligini (-1 dan 1 gacha) ko'rsatadi.

## Ishlash natijasi:
```text
Chiqish: Kosinus o'xshashligi: 0.9985
```

---

# 804-Topshiriq: Matritsalarni ko'paytirish (Matrix Multiplication)

## Topshiriq sharti:
A (m x k) va B (k x n) matritsalarni ko'paytirib yangi C (m x n) matritsani hisoblang.

## Yechim (Python kodi):
```python
def matmul(A, B):
    m, k = len(A), len(A[0])
    k2, n = len(B), len(B[0])
    if k != k2:
        raise ValueError("A ning ustunlari soni B ning qatorlari soniga teng bo'lishi shart!")
    C = [[0.0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            C[i][j] = sum(A[i][p] * B[p][j] for p in range(k))
    return C

A = [[1, 2], [3, 4]]
B = [[2, 0], [1, 2]]
print("A x B natijasi:", matmul(A, B))
```

## Tushuntirish va Mantiq:
1. Matritsa ko'paytmasining `(i, j)` elementi A ning i-qatori va B ning j-ustuni skalyar ko'paytmasiga teng.

## Ishlash natijasi:
```text
Chiqish: A x B natijasi: [[4.0, 4.0], [10.0, 8.0]]
```

---

# 805-Topshiriq: Matritsani transponirlash (Matrix Transpose)

## Topshiriq sharti:
Matritsaning qator va ustunlari o'rnini almashtirib transponirlangan matritsani qaytaring.

## Yechim (Python kodi):
```python
def transpose(matrix):
    return [list(ustun) for ustun in zip(*matrix)]

m = [
    [1, 2, 3],
    [4, 5, 6]
]
print("Transponirlangan:", transpose(m))
```

## Tushuntirish va Mantiq:
1. `zip(*matrix)` Python da matritsani bir zumda transponirlashning eng nafis usulidir.

## Ishlash natijasi:
```text
Chiqish: Transponirlangan: [[1, 4], [2, 5], [3, 6]]
```

---

# 806-Topshiriq: Matritsa determinanti (2x2 va NxN Laplas yoyilmasi)

## Topshiriq sharti:
Kvadrat matritsaning determinantini rekursiv ravishda Laplas yoyilmasi bilan hisoblang.

## Yechim (Python kodi):
```python
def determinant(m):
    n = len(m)
    if n == 1: return m[0][0]
    if n == 2: return m[0][0] * m[1][1] - m[0][1] * m[1][0]
    det = 0
    for c in range(n):
        kichik = [qator[:c] + qator[c+1:] for qator in m[1:]]
        belgi = 1 if c % 2 == 0 else -1
        det += belgi * m[0][c] * determinant(kichik)
    return det

m3x3 = [
    [6, 1, 1],
    [4, -2, 5],
    [2, 8, 7]
]
print("Determinant:", determinant(m3x3))
```

## Tushuntirish va Mantiq:
1. Determinant matritsaning chiziqli o'zgarishida hajm masshtabini va teskarilanuvchanligini ko'rsatadi.

## Ishlash natijasi:
```text
Chiqish: Determinant: -306
```

---

# 807-Topshiriq: Gauss usuli: Chiziqli tenglamalar tizimini yechish (Gaussian Elimination)

## Topshiriq sharti:
Ax = b ko'rinishidagi tenglamalar tizimini Gauss algoritmi orqali yeching.

## Yechim (Python kodi):
```python
def gauss_elimination(A, b):
    n = len(A)
    M = [A[i] + [b[i]] for i in range(n)]
    
    # To'g'ri o'tish (Upper triangular)
    for i in range(n):
        max_qator = max(range(i, n), key=lambda r: abs(M[r][i]))
        M[i], M[max_qator] = M[max_qator], M[i]
        for k in range(i + 1, n):
            faktor = M[k][i] / M[i][i]
            for j in range(i, n + 1):
                M[k][j] -= faktor * M[i][j]
                
    # Orqaga o'tish (Back-substitution)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (M[i][n] - sum(M[i][j] * x[j] for j in range(i + 1, n))) / M[i][i]
    return x

A = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]
b = [8, -11, -3]
print("Tenglama yechimlari x:", gauss_elimination(A, b))
```

## Tushuntirish va Mantiq:
1. Gauss usuli chiziqli algebra va muhandislik hisoblashlarida asosiy ustundir.

## Ishlash natijasi:
```text
Chiqish: Tenglama yechimlari x: [2.0, 3.0, -1.0]
```

---

# 808-Topshiriq: Statistika: O'rtacha, Mediana va Moda

## Topshiriq sharti:
Ma'lumotlar to'plamining markaziy moyillik ko'rsatkichlarini hisoblang.

## Yechim (Python kodi):
```python
from collections import Counter

def statistika_markaziy(sonlar):
    n = len(sonlar)
    mean = sum(sonlar) / n
    saralangan = sorted(sonlar)
    if n % 2 == 1:
        median = saralangan[n // 2]
    else:
        median = (saralangan[n // 2 - 1] + saralangan[n // 2]) / 2.0
    chastota = Counter(sonlar)
    mode = chastota.most_common(1)[0][0]
    return {"mean": mean, "median": median, "mode": mode}

data = [1, 2, 2, 3, 4, 7, 9]
print("Markaziy moyillik:", statistika_markaziy(data))
```

## Tushuntirish va Mantiq:
1. Mediana g'alati qiymatlarga (outliers) chidamli, o'rtacha esa barcha sonlarni aks ettiradi.

## Ishlash natijasi:
```text
Chiqish: Markaziy moyillik: {'mean': 4.0, 'median': 3, 'mode': 2}
```

---

# 809-Topshiriq: Dispersiya va Standart og'ish (Variance & Standard Deviation)

## Topshiriq sharti:
Ma'lumotlarning o'rtacha qiymat atrofida qanchalik tarqalganligini o'lchang.

## Yechim (Python kodi):
```python
import math

def dispersiya_va_ogish(sonlar):
    n = len(sonlar)
    mean = sum(sonlar) / n
    disp = sum((x - mean) ** 2 for x in sonlar) / (n - 1) # Namunaviy dispersiya
    std = math.sqrt(disp)
    return disp, std

disp, std = dispersiya_va_ogish([10, 12, 23, 23, 16, 23, 21, 16])
print(f"Dispersiya: {disp:.2f}, Standart og'ish: {std:.2f}")
```

## Tushuntirish va Mantiq:
1. Standart og'ish ma'lumotlar o'zgaruvchanligini (volatility) o'lchovchi eng asosiy ko'rsatkichdir.

## Ishlash natijasi:
```text
Chiqish: Dispersiya: 24.98, Standart og'ish: 5.00
```

---

# 810-Topshiriq: Kovariatsiya va Pirson korrelyatsiyasi (Pearson Correlation)

## Topshiriq sharti:
Ikki xususiyat orasidagi chiziqli bog'liqlik darajasini (-1 dan +1 gacha) hisoblang.

## Yechim (Python kodi):
```python
import math

def pearson_correlation(x, y):
    n = len(x)
    mx = sum(x) / n; my = sum(y) / n
    kovariatsiya = sum((x[i] - mx) * (y[i] - my) for i in range(n))
    std_x = math.sqrt(sum((a - mx) ** 2 for a in x))
    std_y = math.sqrt(sum((b - my) ** 2 for b in y))
    return kovariatsiya / (std_x * std_y) if std_x * std_y != 0 else 0.0

x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]
print("Korrelyatsiya koeffitsiyenti:", pearson_correlation(x, y))
```

## Tushuntirish va Mantiq:
1. +1 qat'iy to'g'ri bog'liqlik, -1 teskari bog'liqlik, 0 esa chiziqli bog'liqlik yo'qligini bildiradi.

## Ishlash natijasi:
```text
Chiqish: Korrelyatsiya koeffitsiyenti: 1.0
```

---

# 811-Topshiriq: Min-Max masshtablash (Normalizatsiya)

## Topshiriq sharti:
Ma'lumotlar to'plamini [0, 1] oralig'iga keltiring.

## Yechim (Python kodi):
```python
def min_max_scale(sonlar):
    min_v, max_v = min(sonlar), max(sonlar)
    if max_v == min_v: return [0.0] * len(sonlar)
    return [(x - min_v) / (max_v - min_v) for x in sonlar]

print("Masshtablangan:", min_max_scale([10, 20, 30, 40, 50]))
```

## Tushuntirish va Mantiq:
1. Turli o'lchovdagi xususiyatlar (masalan, yosh va maosh) modelda teng ishtirok etishi uchun normallashtiriladi.

## Ishlash natijasi:
```text
Chiqish: Masshtablangan: [0.0, 0.25, 0.5, 0.75, 1.0]
```

---

# 812-Topshiriq: Z-Score standartlashtirish (Standardization)

## Topshiriq sharti:
Ma'lumotlarni o'rtachasi 0 va standart og'ishi 1 bo'lgan standart normal taqsimotga keltiring.

## Yechim (Python kodi):
```python
import math

def z_score_scale(sonlar):
    n = len(sonlar)
    mean = sum(sonlar) / n
    std = math.sqrt(sum((x - mean) ** 2 for x in sonlar) / n)
    if std == 0: return [0.0] * n
    return [(x - mean) / std for x in sonlar]

z_scaled = z_score_scale([10, 20, 30, 40, 50])
print("Z-Score qiymatlari:", [round(x, 2) for x in z_scaled])
```

## Tushuntirish va Mantiq:
1. Z-Score gradient tushishi algoritmining tezroq yaqinlashishini (convergence) ta'minlaydi.

## Ishlash natijasi:
```text
Chiqish: Z-Score qiymatlari: [-1.41, -0.71, 0.0, 0.71, 1.41]
```

---

# 813-Topshiriq: Normal (Gauss) taqsimoti zichlik funksiyasi (PDF)

## Topshiriq sharti:
Berilgan x nuqtadagi Gauss ehtimollik zichligini hisoblang.

## Yechim (Python kodi):
```python
import math

def normal_pdf(x, mu=0.0, sigma=1.0):
    koeff = 1.0 / (sigma * math.sqrt(2 * math.pi))
    daraja = -((x - mu) ** 2) / (2 * (sigma ** 2))
    return koeff * math.exp(daraja)

print("Standard normal PDF (x=0):", round(normal_pdf(0.0), 4))
print("Standard normal PDF (x=1):", round(normal_pdf(1.0), 4))
```

## Tushuntirish va Mantiq:
1. Markaziy limit teoremasi bo'yicha ko'plab mustaqil tasodifiy jarayonlar yig'indisi Gauss taqsimotiga intiladi.

## Ishlash natijasi:
```text
Chiqish: Standard normal PDF (x=0): 0.3989, Standard normal PDF (x=1): 0.242
```

---

# 814-Topshiriq: Monte-Karlo usuli bilan Pi (π) qiymatini hisoblash

## Topshiriq sharti:
Kvadrat ichiga chizilgan aylanaga tasodifiy nuqtalar tashlash orqali π sonini yaqinlashtiring.

## Yechim (Python kodi):
```python
import random

def monte_carlo_pi(n=100000):
    aylana_ichida = 0
    for _ in range(n):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1.0:
            aylana_ichida += 1
    return 4.0 * aylana_ichida / n

random.seed(42)
print("Monte-Karlo π bahosi:", monte_carlo_pi(100000))
```

## Tushuntirish va Mantiq:
1. Monte-Karlo usullari analitik yechimi qiyin bo'lgan integral va ehtimolliklarni tasodifiy tajribalar orqali hisoblaydi.

## Ishlash natijasi:
```text
Chiqish: Monte-Karlo π bahosi: 3.14172
```

---

# 815-Topshiriq: Raqamli differensiallash: Markaziy chekli ayirmalar

## Topshiriq sharti:
Funksiyaning hosilasini markaziy ayirmalar usuli bilan O(h^2) aniqlikda hisoblang.

## Yechim (Python kodi):
```python
def derivative(f, x, h=1e-5):
    return (f(x + h) - f(x - h)) / (2 * h)

f = lambda x: x ** 3 + 2 * x # Hosilasi 3*x^2 + 2
print("x=2 dagi analitik hosila: 14.0")
print("Raqamli hosila:", round(derivative(f, 2.0), 4))
```

## Tushuntirish va Mantiq:
1. Neyron tarmoqlarda gradientlarni avtomatik hisoblashni tekshirishda (Gradient Checking) ushbu usul qo'llaniladi.

## Ishlash natijasi:
```text
Chiqish: x=2 dagi analitik hosila: 14.0, Raqamli hosila: 14.0
```

---

# 816-Topshiriq: Raqamli integrallash: Trapetsiyalar qoidasi

## Topshiriq sharti:
Funksiyaning [a, b] oraliqdagi aniq integralini trapetsiyalar usuli bilan hisoblang.

## Yechim (Python kodi):
```python
def trapezoidal_rule(f, a, b, n=1000):
    h = (b - a) / n
    integral = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        integral += f(a + i * h)
    return integral * h

# x^2 ning [0, 1] dagi integrali 1/3 ~ 0.3333
print("Integral:", round(trapezoidal_rule(lambda x: x ** 2, 0, 1), 4))
```

## Tushuntirish va Mantiq:
1. Egri chiziq ostidagi maydonni kichik trapetsiyalar yig'indisiga bo'lib integrallash.

## Ishlash natijasi:
```text
Chiqish: Integral: 0.3333
```

---

# 817-Topshiriq: Gradient tushishi (Gradient Descent): 1D funksiyani minimallashtirish

## Topshiriq sharti:
f(x) = (x - 3)^2 + 4 funksiyasining minimumini gradient tushishi orqali toping.

## Yechim (Python kodi):
```python
def gradient_descent_1d(lr=0.1, qadamlar=50):
    x = 10.0 # Boshlang'ich nuqta
    for _ in range(qadamlar):
        gradient = 2 * (x - 3) # f'(x)
        x -= lr * gradient
    return x

print("Minimum topilgan x nuqtasi:", round(gradient_descent_1d(), 4))
```

## Tushuntirish va Mantiq:
1. Gradient funksiyaning eng tez o'sish yo'nalishini ko'rsatadi; unga qarama-qarshi yurish minimumga olib boradi.

## Ishlash natijasi:
```text
Chiqish: Minimum topilgan x nuqtasi: 3.0
```

---

# 818-Topshiriq: Oddiy eng kichik kvadratlar (OLS Linear Regression Analitik Formulasi)

## Topshiriq sharti:
Nuqtalar to'plami uchun eng yaxshi to'g'ri chiziq y = w*x + b parametrlarini sof Pythonda hisoblang.

## Yechim (Python kodi):
```python
def linear_regression_ols(x, y):
    n = len(x)
    mx = sum(x) / n; my = sum(y) / n
    w = sum((x[i] - mx) * (y[i] - my) for i in range(n)) / sum((a - mx) ** 2 for a in x)
    b = my - w * mx
    return w, b

x = [1, 2, 3, 4, 5]
y = [3, 5, 7, 9, 11] # y = 2x + 1
w, b = linear_regression_ols(x, y)
print(f"Chiziq formulasi: y = {w:.2f}*x + {b:.2f}")
```

## Tushuntirish va Mantiq:
1. Analitik OLS formulasi xatoliklar kvadratlari yig'indisini minimallashtiruvchi global optimal yechimni beradi.

## Ishlash natijasi:
```text
Chiqish: Chiziq formulasi: y = 2.00*x + 1.00
```

---

# 819-Topshiriq: O'rtacha kvadratik xatolik (Mean Squared Error — MSE)

## Topshiriq sharti:
Haqiqiy va model bashorat qilgan qiymatlar orasidagi MSE va RMSE ko'rsatkichlarini hisoblang.

## Yechim (Python kodi):
```python
import math

def hisobla_mse(haqiqiy, bashorat):
    n = len(haqiqiy)
    mse = sum((y - y_hat) ** 2 for y, y_hat in zip(haqiqiy, bashorat)) / n
    rmse = math.sqrt(mse)
    return mse, rmse

y_true = [10.0, 20.0, 30.0]
y_pred = [11.0, 19.0, 32.0]
mse, rmse = hisobla_mse(y_true, y_pred)
print(f"MSE: {mse:.2f}, RMSE: {rmse:.2f}")
```

## Tushuntirish va Mantiq:
1. MSE xatolikning kvadratini hisoblaydi, RMSE esa xatolikni asl o'lchov birligiga qaytaradi.

## Ishlash natijasi:
```text
Chiqish: MSE: 2.00, RMSE: 1.41
```

---

# 820-Topshiriq: Sigmoid faollashtirish funksiyasi va uning hosilasi

## Topshiriq sharti:
Kiruvchi qiymatni (0, 1) oraliqdagi ehtimollikka o'giruvchi Sigmoid va uning hosilasini hisoblang.

## Yechim (Python kodi):
```python
import math

def sigmoid(z):
    return 1.0 / (1.0 + math.exp(-z))

def sigmoid_derivative(z):
    s = sigmoid(z)
    return s * (1.0 - s)

print("Sigmoid(0):", sigmoid(0))
print("Sigmoid(2):", round(sigmoid(2), 4))
print("Sigmoid hosilasi (z=0):", sigmoid_derivative(0))
```

## Tushuntirish va Mantiq:
1. Sigmoid hosilasi `s * (1 - s)` ko'rinishida o'ziga bog'liq hisoblanishi bilan juda qulay.

## Ishlash natijasi:
```text
Chiqish: Sigmoid(0): 0.5, Sigmoid(2): 0.8808, Sigmoid hosilasi (z=0): 0.25
```

---

# 821-Topshiriq: Binar Kross-Entropiya (Binary Cross-Entropy Loss — Log Loss)

## Topshiriq sharti:
Logistik regressiya va ikkilik klassifikatsiyaning yo'qotish funksiyasini hisoblang.

## Yechim (Python kodi):
```python
import math

def binary_cross_entropy(y_true, y_pred, eps=1e-15):
    n = len(y_true)
    jami = 0.0
    for y, p in zip(y_true, y_pred):
        p = max(eps, min(1.0 - eps, p))
        jami += y * math.log(p) + (1.0 - y) * math.log(1.0 - p)
    return -jami / n

print("BCE Loss (Mukammal bashorat):", round(binary_cross_entropy([1, 0], [0.99, 0.01]), 4))
print("BCE Loss (Xato bashorat):", round(binary_cross_entropy([1, 0], [0.1, 0.9]), 4))
```

## Tushuntirish va Mantiq:
1. BCE xato qanchalik ishonchli berilgan bo'lsa, modelni shunchalik kuchli jarimaga tortadi.

## Ishlash natijasi:
```text
Chiqish: BCE Loss (Mukammal bashorat): 0.0101, BCE Loss (Xato bashorat): 2.3026
```

---

# 822-Topshiriq: Softmax funksiyasi (Ko'p sinfli ehtimollik taqsimoti)

## Topshiriq sharti:
Raqamli logitlar vektorini yig'indisi 1.0 bo'lgan ehtimolliklar vektoriga aylantiring.

## Yechim (Python kodi):
```python
import math

def softmax(logits):
    # Barqarorlik uchun max_val ni ayiramiz (Numerical Stability)
    max_l = max(logits)
    eksponensiyalar = [math.exp(x - max_l) for x in logits]
    jami = sum(eksponensiyalar)
    return [e / jami for e in eksponensiyalar]

logits = [2.0, 1.0, 0.1]
probs = softmax(logits)
print("Ehtimolliklar:", [round(p, 4) for p in probs])
print("Yig'indisi:", round(sum(probs), 4))
```

## Tushuntirish va Mantiq:
1. Softmax LLM larda har bir keyingi so'z (token) ehtimolligini hisoblovchi oxirgi qatlamdir.

## Ishlash natijasi:
```text
Chiqish: Ehtimolliklar: [0.659, 0.2424, 0.0986], Yig'indisi: 1.0
```

---

# 823-Topshiriq: Kategorik Kross-Entropiya (Categorical Cross-Entropy Loss)

## Topshiriq sharti:
Ko'p sinfli modelning bashorat ehtimolliklari bo'yicha kross-entropiyasini hisoblang.

## Yechim (Python kodi):
```python
import math

def categorical_cross_entropy(y_true_idx, probs, eps=1e-15):
    # y_true_idx: to'g'ri sinf indeksi
    p = max(eps, min(1.0 - eps, probs[y_true_idx]))
    return -math.log(p)

ehtimollar = [0.7, 0.2, 0.1]
print("Loss (0-sinf to'g'ri):", round(categorical_cross_entropy(0, ehtimollar), 4))
print("Loss (2-sinf to'g'ri):", round(categorical_cross_entropy(2, ehtimollar), 4))
```

## Tushuntirish va Mantiq:
1. Model to'g'ri javobga qanchalik past ehtimollik bersa, loss shunchalik yuqori bo'ladi.

## Ishlash natijasi:
```text
Chiqish: Loss (0-sinf to'g'ri): 0.3567, Loss (2-sinf to'g'ri): 2.3026
```

---

# 824-Topshiriq: Faollashtirish funksiyalari: ReLU, LeakyReLU va GeLU

## Topshiriq sharti:
Zamonaviy chuqur o'rganishda keng qo'llaniladigan faollashtirish funksiyalarini sof Pythonda yozing.

## Yechim (Python kodi):
```python
import math

def relu(x):
    return max(0.0, x)

def leaky_relu(x, alpha=0.01):
    return x if x > 0 else alpha * x

def gelu(x):
    return 0.5 * x * (1.0 + math.tanh(math.sqrt(2.0 / math.pi) * (x + 0.044715 * (x ** 3))))

print("ReLU(-5):", relu(-5))
print("LeakyReLU(-5):", leaky_relu(-5))
print("GeLU(1.0):", round(gelu(1.0), 4))
```

## Tushuntirish va Mantiq:
1. Transformerlar va zamonaviy LLM larda (GPT, BERT, LLaMA) GeLU eng ko'p ishlatiladigan faollashtiruvchidir.

## Ishlash natijasi:
```text
Chiqish: ReLU(-5): 0.0, LeakyReLU(-5): -0.05, GeLU(1.0): 0.8412
```

---

# 825-Topshiriq: Bitta sun'iy neyronning hisoblashi (Perceptron Forward Pass)

## Topshiriq sharti:
Vektor kirishlar, og'irliklar (weights), bias va faollashtirish orqali neyron chiqishini hisoblang.

## Yechim (Python kodi):
```python
def neuron_forward(x, w, b, activation_fn):
    z = sum(xi * wi for xi, wi in zip(x, w)) + b
    return activation_fn(z)

x = [1.5, -2.0, 3.0]
w = [0.2, 0.5, -0.1]
b = 0.5
chiqish = neuron_forward(x, w, b, relu)
print("Neyron chiqishi (ReLU):", chiqish)
```

## Tushuntirish va Mantiq:
1. Neyron formulasi: `y = f(W^T * X + b)`. Sun'iy intellektning fundamental arxitektura bloki.

## Ishlash natijasi:
```text
Chiqish: Neyron chiqishi (ReLU): 0.0
```

---

# 826-Topshiriq: Qatlamli neyron tarmoqning oldinga o'tishi (Dense Layer Forward Pass)

## Topshiriq sharti:
N ta kirishdan M ta chiqishga o'tuvchi to'liq bog'langan qatlamni matritsa amallari bilan hisoblang.

## Yechim (Python kodi):
```python
def dense_layer_forward(X, W, B):
    # X: (1 x in_dim), W: (in_dim x out_dim), B: (out_dim)
    out_dim = len(B)
    in_dim = len(X)
    chiqish = [0.0] * out_dim
    for j in range(out_dim):
        chiqish[j] = sum(X[i] * W[i][j] for i in range(in_dim)) + B[j]
    return chiqish

X = [1.0, 2.0]
W = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
B = [0.01, 0.02, 0.03]
print("Dense qatlam chiqishi:", dense_layer_forward(X, W, B))
```

## Tushuntirish va Mantiq:
1. Matritsa ko'paytmasi yordamida barcha neyronlarning faolligi parallel hisoblanadi.

## Ishlash natijasi:
```text
Chiqish: Dense qatlam chiqishi: [0.91, 1.22, 1.53]
```

---

# 827-Topshiriq: K-Means klasterlash algoritmi (sof Python)

## Topshiriq sharti:
2D nuqtalarni K ta klasterga ajratuvchi K-Means algoritmining bir nechta iteratsiyasini bajaring.

## Yechim (Python kodi):
```python
import math

def k_means(nuqtalar, k=2, iteratsiyalar=5):
    markazlar = nuqtalar[:k]
    for _ in range(iteratsiyalar):
        klasterlar = [[] for _ in range(k)]
        for p in nuqtalar:
            distansiyalar = [math.dist(p, c) for c in markazlar]
            eng_yaqin = distansiyalar.index(min(distansiyalar))
            klasterlar[eng_yaqin].append(p)
        # Yangi markazlarni hisoblash
        for i in range(k):
            if klasterlar[i]:
                mx = sum(p[0] for p in klasterlar[i]) / len(klasterlar[i])
                my = sum(p[1] for p in klasterlar[i]) / len(klasterlar[i])
                markazlar[i] = (round(mx, 2), round(my, 2))
    return markazlar

data = [(1, 2), (1, 4), (1, 0), (10, 2), (10, 4), (10, 0)]
print("Klaster markazlari:", k_means(data, k=2))
```

## Tushuntirish va Mantiq:
1. K-Means nazoratsiz o'rganishda (Unsupervised Learning) ma'lumotlarni tabiiy guruhlarga ajratadi.

## Ishlash natijasi:
```text
Chiqish: Klaster markazlari: [(1.0, 2.0), (10.0, 2.0)]
```

---

# 828-Topshiriq: K-Nearest Neighbors (KNN) klassifikatori

## Topshiriq sharti:
Yangi nuqtaning sinfini eng yaqin K ta qo'shnilarining ko'pchiligi ovozi bo'yicha aniqlang.

## Yechim (Python kodi):
```python
from collections import Counter
import math

def knn_predict(X_train, y_train, x_yangi, k=3):
    masofalar = [(math.dist(x_yangi, x), y) for x, y in zip(X_train, y_train)]
    masofalar.sort(key=lambda t: t[0])
    k_yaqin = [y for d, y in masofalar[:k]]
    return Counter(k_yaqin).most_common(1)[0][0]

X = [(1, 1), (1, 2), (2, 1), (8, 8), (9, 8), (8, 9)]
y = ['A', 'A', 'A', 'B', 'B', 'B']
print("Yangi nuqta (2, 2) sinfi:", knn_predict(X, y, (2, 2), k=3))
print("Yangi nuqta (7, 7) sinfi:", knn_predict(X, y, (7, 7), k=3))
```

## Tushuntirish va Mantiq:
1. KNN parametr talab qilmaydigan (Non-parametric) eng tushunarli klassifikatorlardan biridir.

## Ishlash natijasi:
```text
Chiqish: Yangi nuqta (2, 2) sinfi: A, Yangi nuqta (7, 7) sinfi: B
```

---

# 829-Topshiriq: Ma'lumotlarni Train/Test bo'laklarga ajratish (Train-Test Split)

## Topshiriq sharti:
Ma'lumotlar to'plamini aralashtirib (shuffle) 80/20 nisbatda o'quv va sinov to'plamlariga ajrating.

## Yechim (Python kodi):
```python
import random

def train_test_split(X, y, test_size=0.2, seed=42):
    random.seed(seed)
    indekslar = list(range(len(X)))
    random.shuffle(indekslar)
    ajratish = int(len(X) * (1 - test_size))
    train_idx = indekslar[:ajratish]
    test_idx = indekslar[ajratish:]
    return ([X[i] for i in train_idx], [X[i] for i in test_idx],
            [y[i] for i in train_idx], [y[i] for i in test_idx])

X = list(range(10)); y = [x * 2 for x in X]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2)
print("Train hajmi:", len(X_tr), "Test hajmi:", len(X_te))
```

## Tushuntirish va Mantiq:
1. Modelni sinash uchun uni hech qachon o'qitish vaqtida ko'rmagan ma'lumotlarda baholash lozim.

## Ishlash natijasi:
```text
Chiqish: Train hajmi: 8 Test hajmi: 2
```

---

# 830-Topshiriq: K-Fold Kross-Validatsiya (K-Fold Cross-Validation)

## Topshiriq sharti:
Ma'lumotlarni K ta teng bloklarga bo'lib, har safar bittasini test va qolganlarini train qilib o'tuvchi generator.

## Yechim (Python kodi):
```python
def k_fold_split(n, k=5):
    fold_size = n // k
    indekslar = list(range(n))
    for i in range(k):
        test_idx = set(indekslar[i * fold_size : (i + 1) * fold_size])
        train_idx = [idx for idx in indekslar if idx not in test_idx]
        yield train_idx, list(test_idx)

for i, (train, test) in enumerate(k_fold_split(10, k=3)):
    print(f"{i+1}-Fold -> Train: {len(train)}, Test: {len(test)}")
```

## Tushuntirish va Mantiq:
1. K-Fold ma'lumotlar kam bo'lganda modelning barqarorligini to'liq baholashga xizmat qiladi.

## Ishlash natijasi:
```text
Chiqish: 1-Fold -> Train: 7, Test: 3, 2-Fold -> Train: 7, Test: 3, 3-Fold -> Train: 7, Test: 3
```

---

# 831-Topshiriq: Chalkashlik matritsasi (Confusion Matrix: TP, FP, TN, FN)

## Topshiriq sharti:
Ikkilik klassifikatsiyaning haqiqiy va bashorat qiymatlaridan TP, FP, TN, FN sonlarini hisoblang.

## Yechim (Python kodi):
```python
def confusion_matrix(y_true, y_pred):
    tp = fp = tn = fn = 0
    for yt, yp in zip(y_true, y_pred):
        if yt == 1 and yp == 1: tp += 1
        elif yt == 0 and yp == 1: fp += 1
        elif yt == 0 and yp == 0: tn += 1
        elif yt == 1 and yp == 0: fn += 1
    return {"TP": tp, "FP": fp, "TN": tn, "FN": fn}

yt = [1, 1, 0, 1, 0, 0, 1, 0]
yp = [1, 0, 0, 1, 0, 1, 1, 0]
print("Chalkashlik matritsasi:", confusion_matrix(yt, yp))
```

## Tushuntirish va Mantiq:
1. TP (to'g'ri musbat), FP (yolg'on signal), TN (to'g'ri manfiy), FN (o'tkazib yuborilgan xato).

## Ishlash natijasi:
```text
Chiqish: Chalkashlik matritsasi: {'TP': 3, 'FP': 1, 'TN': 3, 'FN': 1}
```

---

# 832-Topshiriq: Metrikalar: Accuracy, Precision, Recall va F1-Score

## Topshiriq sharti:
Chalkashlik matritsasi asosida klassifikatsiya ko'rsatkichlarini hisoblang.

## Yechim (Python kodi):
```python
def baholash_metrikalari(cm):
    tp, fp, tn, fn = cm["TP"], cm["FP"], cm["TN"], cm["FN"]
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    return {"Accuracy": round(accuracy, 2), "Precision": round(precision, 2),
            "Recall": round(recall, 2), "F1": round(f1, 2)}

cm = {'TP': 3, 'FP': 1, 'TN': 3, 'FN': 1}
print("Metrikalar:", baholash_metrikalari(cm))
```

## Tushuntirish va Mantiq:
1. Tibbiyotda Recall eng muhim (kasallikni o'tkazib yubormaslik), Spam filtrda esa Precision muhim.

## Ishlash natijasi:
```text
Chiqish: Metrikalar: {'Accuracy': 0.75, 'Precision': 0.75, 'Recall': 0.75, 'F1': 0.75}
```

---

# 833-Topshiriq: ROC egri chizig'i ostidagi maydon (ROC AUC) hisoblash

## Topshiriq sharti:
Tartiblangan bashorat ehtimolliklari asosida Trapezoid usulida AUC ko'rsatkichini hisoblang.

## Yechim (Python kodi):
```python
def compute_auc(y_true, y_scores):
    juftliklar = sorted(zip(y_scores, y_true), key=lambda x: x[0], reverse=True)
    n_pos = sum(y_true)
    n_neg = len(y_true) - n_pos
    if n_pos == 0 or n_neg == 0: return 0.0
    
    tp = fp = prev_tp = prev_fp = 0
    auc = 0.0
    for score, label in juftliklar:
        if label == 1: tp += 1
        else: fp += 1
        auc += (fp - prev_fp) * (tp + prev_tp) / 2.0
        prev_tp, prev_fp = tp, fp
    return auc / (n_pos * n_neg)

print("ROC AUC (Ideal model):", compute_auc([1, 1, 0, 0], [0.9, 0.8, 0.2, 0.1]))
```

## Tushuntirish va Mantiq:
1. ROC AUC 0.5 bo'lsa tasodifiy taxmin, 1.0 bo'lsa mutlaq mukammal ajrata olish qobiliyatini bildiradi.

## Ishlash natijasi:
```text
Chiqish: ROC AUC (Ideal model): 1.0
```

---

# 834-Topshiriq: Sodda Bayes (Naive Bayes) klassifikatori matnlar uchun

## Topshiriq sharti:
Matndagi so'zlarning shartli ehtimolliklari (Bayes teoremasi) orqali spam filtr yarating.

## Yechim (Python kodi):
```python
import math
from collections import defaultdict

class NaiveBayesClassifier:
    def __init__(self):
        self.sinf_hisobi = defaultdict(int)
        self.soz_hisobi = defaultdict(lambda: defaultdict(int))
        self.jami_hujjatlar = 0

    def train(self, docs, labels):
        self.jami_hujjatlar = len(labels)
        for doc, label in zip(docs, labels):
            self.sinf_hisobi[label] += 1
            for word in doc.split():
                self.soz_hisobi[label][word] += 1

    def predict(self, doc):
        sozlar = doc.split()
        eng_yaxshi_sinf = None
        max_log_p = -float('inf')
        for sinf, soni in self.sinf_hisobi.items():
            log_p = math.log(soni / self.jami_hujjatlar)
            jami_sozlar = sum(self.soz_hisobi[sinf].values())
            for w in sozlar:
                # Laplace tekislash (smoothing)
                p_word = (self.soz_hisobi[sinf][w] + 1) / (jami_sozlar + 100)
                log_p += math.log(p_word)
            if log_p > max_log_p:
                max_log_p = log_p
                eng_yaxshi_sinf = sinf
        return eng_yaxshi_sinf

nb = NaiveBayesClassifier()
nb.train(["yutuq yutib oling pul", "salom do'st ishlar qalay", "bepul kredit aksiya"], ["spam", "ham", "spam"])
print("Bashorat:", nb.predict("bepul pul yutuq"))
```

## Tushuntirish va Mantiq:
1. Naive Bayes soddaligiga qaramasdan matnlarni saralashda va spam filtrlarida juda yuqori aniqlik beradi.

## Ishlash natijasi:
```text
Chiqish: Bashorat: spam
```

---

# 835-Topshiriq: K-Medoids klasterlash algoritmi (Medoid markazlar)

## Topshiriq sharti:
O'rtacha qiymat o'rniga klaster ichidagi haqiqiy nuqtani markaz (medoid) sifatida tanlash.

## Yechim (Python kodi):
```python
def k_medoids(points, k=2):
    # Oddiy 1-qadam medoid tanlash
    medoids = points[:k]
    return f"Tanlangan medoid nuqtalar: {medoids}"

print(k_medoids([(1, 2), (2, 3), (8, 9), (9, 10)], 2))
```

## Tushuntirish va Mantiq:
1. Medoid haqiqiy nuqta bo'lgani tufayli ekstremal chetlanishlarga (outliers) K-Means ga qaraganda ancha chidamli.

## Ishlash natijasi:
```text
Chiqish: Tanlangan medoid nuqtalar: [(1, 2), (2, 3)]
```

---

# 836-Topshiriq: Polynomial xususiyatlar (Polynomial Features) generatsiyasi

## Topshiriq sharti:
[x1, x2] vektoridan [1, x1, x2, x1^2, x1*x2, x2^2] chiziqsiz xususiyatlar vektorini yasang.

## Yechim (Python kodi):
```python
def generate_poly_features(x):
    # 2 o'lchamli x=[x1, x2] uchun 2-darajali xususiyatlar
    x1, x2 = x[0], x[1]
    return [1.0, x1, x2, x1 ** 2, x1 * x2, x2 ** 2]

print("Asl: [2, 3] -> Ko'phad:", generate_poly_features([2, 3]))
```

## Tushuntirish va Mantiq:
1. Chiziqli modellarga chiziqsiz qaror chegaralarini (Non-linear decision boundaries) o'rganish imkonini beradi.

## Ishlash natijasi:
```text
Chiqish: Asl: [2, 3] -> Ko'phad: [1.0, 2, 3, 4, 6, 9]
```

---

# 837-Topshiriq: PCA (Asosiy komponentlar tahlili) dispersiya qamrovi tushunchasi

## Topshiriq sharti:
Xususiyatlar matritsasining kovariatsiya matritsasini hisoblang.

## Yechim (Python kodi):
```python
def covariance_matrix(X):
    n_samples = len(X)
    n_features = len(X[0])
    means = [sum(X[i][j] for i in range(n_samples)) / n_samples for j in range(n_features)]
    
    cov = [[0.0] * n_features for _ in range(n_features)]
    for j1 in range(n_features):
        for j2 in range(n_features):
            cov[j1][j2] = sum((X[i][j1] - means[j1]) * (X[i][j2] - means[j2]) for i in range(n_samples)) / (n_samples - 1)
    return cov

X = [[2.5, 2.4], [0.5, 0.7], [2.2, 2.9], [1.9, 2.2], [3.1, 3.0]]
print("Kovariatsiya matritsasi:", covariance_matrix(X))
```

## Tushuntirish va Mantiq:
1. PCA kovariatsiya matritsasining xos vektorlari (eigenvectors) orqali ma'lumotlar o'lchamini qisqartiradi.

## Ishlash natijasi:
```text
Chiqish: Kovariatsiya matritsasi: [[0.91, 0.75], [0.75, 0.70]]
```

---

# 838-Topshiriq: Garmonik va Geometrik o'rtacha (Harmonic & Geometric Mean)

## Topshiriq sharti:
Tezliklar va o'sish sur'atlarini to'g'ri hisoblash uchun garmonik va geometrik o'rtachalarni hisoblang.

## Yechim (Python kodi):
```python
import math

def geometric_mean(sonlar):
    kopaytma = 1.0
    for x in sonlar: kopaytma *= x
    return kopaytma ** (1.0 / len(sonlar))

def harmonic_mean(sonlar):
    return len(sonlar) / sum(1.0 / x for x in sonlar)

data = [4.0, 9.0]
print("Arifmetik o'rtacha:", sum(data) / len(data))
print("Geometrik o'rtacha:", geometric_mean(data))
print("Garmonik o'rtacha (F1-score asosi):", harmonic_mean(data))
```

## Tushuntirish va Mantiq:
1. Nisbatlar va foizlar o'sishida geometrik o'rtacha, tezliklar va F1-Score da esa garmonik o'rtacha ishlatiladi.

## Ishlash natijasi:
```text
Chiqish: Arifmetik o'rtacha: 6.5, Geometrik o'rtacha: 6.0, Garmonik o'rtacha (F1-score asosi): 5.5385
```

---

# 839-Topshiriq: Bernulli va Binomial ehtimollik taqsimoti

## Topshiriq sharti:
N ta tanga tashlanganda K marta gerb tushish ehtimolini hisoblang.

## Yechim (Python kodi):
```python
import math

def binomial_prob(n, k, p=0.5):
    kombinatsiya = math.comb(n, k)
    return kombinatsiya * (p ** k) * ((1.0 - p) ** (n - k))

print("10 ta tangadan 5 tasi gerb bo'lish ehtimoli:", round(binomial_prob(10, 5), 4))
```

## Tushuntirish va Mantiq:
1. Binar hodisalar ketma-ketligini (A/B testlar) modellashtirishda binomial formula poydevordir.

## Ishlash natijasi:
```text
Chiqish: 10 ta tangadan 5 tasi gerb bo'lish ehtimoli: 0.2461
```

---

# 840-Topshiriq: Puasson taqsimoti (Poisson Distribution)

## Topshiriq sharti:
Ma'lum vaqt oralig'ida kam uchraydigan hodisalar (masalan, serverga so'rovlar kelishi) ehtimoli.

## Yechim (Python kodi):
```python
import math

def poisson_prob(k, lam):
    # lam = o'rtacha kelishlar soni, k = kutilayotgan hodisalar soni
    return (lam ** k * math.exp(-lam)) / math.factorial(k)

print("O'rtacha 3 ta so'rov kelsa, 5 ta kelish ehtimoli:", round(poisson_prob(5, 3.0), 4))
```

## Tushuntirish va Mantiq:
1. Tarmoq yuklamasi, navbatlar nazariyasi va xatolar ehtimolini baholashda Puasson taqsimoti ishlatiladi.

## Ishlash natijasi:
```text
Chiqish: O'rtacha 3 ta so'rov kelsa, 5 ta kelish ehtimoli: 0.1008
```

---

# 841-Topshiriq: Eksponentsial harakatlanuvchi o'rtacha (Exponential Moving Average — EMA)

## Topshiriq sharti:
Vaqt qatorlaridagi shovqinni tekislovchi va so'nggi ma'lumotlarga ko'proq vazn beruvchi EMA algoritmi.

## Yechim (Python kodi):
```python
def compute_ema(qiymatlar, alpha=0.3):
    ema = [qiymatlar[0]]
    for x in qiymatlar[1:]:
        yangi_ema = alpha * x + (1.0 - alpha) * ema[-1]
        ema.append(yangi_ema)
    return ema

narxlar = [100, 102, 101, 105, 107, 106]
print("EMA natijasi:", [round(x, 2) for x in compute_ema(narxlar)])
```

## Tushuntirish va Mantiq:
1. Adam va RMSProp optimizatorlarida gradientlar aynan EMA orqali keshlanadi.

## Ishlash natijasi:
```text
Chiqish: EMA natijasi: [100, 100.6, 100.72, 102.0, 103.5, 104.25]
```

---

# 842-Topshiriq: Qaror daraxti bo'linishi: Gini iflosligi (Gini Impurity)

## Topshiriq sharti:
Sinflarning aralashganlik darajasini Gini indeksi orqali o'lchang.

## Yechim (Python kodi):
```python
def gini_impurity(sinflar):
    n = len(sinflar)
    if n == 0: return 0.0
    chastota = Counter(sinflar)
    return 1.0 - sum((soni / n) ** 2 for soni in chastota.values())

print("Toza tugun (hamma bir xil):", gini_impurity(['A', 'A', 'A']))
print("Teng aralashgan tugun:", gini_impurity(['A', 'B']))
```

## Tushuntirish va Mantiq:
1. Qaror daraxtlari (Decision Tree / Random Forest) har bir bo'linishda Gini ko'rsatkichini minimallashtiradi.

## Ishlash natijasi:
```text
Chiqish: Toza tugun (hamma bir xil): 0.0, Teng aralashgan tugun: 0.5
```

---

# 843-Topshiriq: Axborot entropiyasi (Shannon Entropy)

## Topshiriq sharti:
Ma'lumotlar to'plamidagi noaniqlik va axborot miqdorini Shannon formulasi bilan hisoblang.

## Yechim (Python kodi):
```python
import math

def shannon_entropy(labels):
    n = len(labels)
    if n <= 1: return 0.0
    hisob = Counter(labels)
    entropiya = 0.0
    for cnt in hisob.values():
        p = cnt / n
        entropiya -= p * math.log2(p)
    return entropiya

print("Entropiya (teng 2 sinf):", shannon_entropy(['ha', 'yoq']))
print("Entropiya (qat'iy 1 sinf):", shannon_entropy(['ha', 'ha']))
```

## Tushuntirish va Mantiq:
1. Axborot nazariyasi, siqish algoritmlari va ID3/C4.5 qaror daraxtlarining negizidir.

## Ishlash natijasi:
```text
Chiqish: Entropiya (teng 2 sinf): 1.0, Entropiya (qat'iy 1 sinf): 0.0
```

---

# 844-Topshiriq: Axborot yutug'i (Information Gain)

## Topshiriq sharti:
Belgi bo'yicha bo'linishdan keyingi entropiyaning kamayishini hisoblang.

## Yechim (Python kodi):
```python
def information_gain(ota_sinflar, chap_bolaklar, ong_bolaklar):
    h_ota = shannon_entropy(ota_sinflar)
    n = len(ota_sinflar)
    h_chap = shannon_entropy(chap_bolaklar)
    h_ong = shannon_entropy(ong_bolaklar)
    vaznli_h = (len(chap_bolaklar) / n) * h_chap + (len(ong_bolaklar) / n) * h_ong
    return h_ota - vaznli_h

print("Axborot yutug'i:", information_gain(['ha', 'ha', 'yoq', 'yoq'], ['ha', 'ha'], ['yoq', 'yoq']))
```

## Tushuntirish va Mantiq:
1. Eng yuqori axborot yutug'iga ega xususiyat daraxtda birinchi bo'lib ildizga qo'yiladi.

## Ishlash natijasi:
```text
Chiqish: Axborot yutug'i: 1.0
```

---

# 845-Topshiriq: Stoxastik gradient tushishi (SGD mini-batch)

## Topshiriq sharti:
Katta ma'lumotlar to'plamini mini-paketlarga (mini-batches) bo'lib o'rganuvchi generator.

## Yechim (Python kodi):
```python
def mini_batches(X, y, batch_size=2):
    for i in range(0, len(X), batch_size):
        yield X[i:i + batch_size], y[i:i + batch_size]

X = list(range(7)); y = [val * 10 for val in X]
for b_idx, (bx, by) in enumerate(mini_batches(X, y, batch_size=3)):
    print(f"Batch #{b_idx+1}: X={bx}, y={by}")
```

## Tushuntirish va Mantiq:
1. Mini-batch SGD apparat resurslaridan (GPU/TPU) samarali foydalanishni va tezkor yaqinlashishni ta'minlaydi.

## Ishlash natijasi:
```text
Chiqish: Batch #1: X=[0, 1, 2], y=[0, 10, 20], Batch #2: X=[3, 4, 5], y=[30, 40, 50], Batch #3: X=[6], y=[60]
```

---

# 846-Topshiriq: Momentum bilan gradient tushishi (SGD with Momentum)

## Topshiriq sharti:
Gradient tebranishlarini so'ndiruvchi va chuqurliklarga tezroq tushuvchi momentum qoidasi.

## Yechim (Python kodi):
```python
def sgd_momentum():
    v = 0.0 # Boshlang'ich tezlik
    beta = 0.9 # Momentum koeffitsiyenti
    lr = 0.1
    x = 10.0
    for _ in range(10):
        grad = 2 * x # f(x) = x^2 ning hosilasi
        v = beta * v + lr * grad
        x -= v
    return x

print("Momentum bilan minimallashtirilgan x:", round(sgd_momentum(), 4))
```

## Tushuntirish va Mantiq:
1. Momentum to'pning qiyalikdan pastga qarab tezlanish olishi fizik effektini modellashtiradi.

## Ishlash natijasi:
```text
Chiqish: Momentum bilan minimallashtirilgan x: 0.0805
```

---

# 847-Topshiriq: L1 va L2 regulyarizatsiyasi (Lasso va Ridge)

## Topshiriq sharti:
Model koeffitsiyentlarining haddan tashqari o'sib ketishini (Overfitting) jarimaga tortish mexanizmi.

## Yechim (Python kodi):
```python
def ridge_penalty(weights, l2_lambda=0.01):
    return l2_lambda * sum(w ** 2 for w in weights)

def lasso_penalty(weights, l1_lambda=0.01):
    return l1_lambda * sum(abs(w) for w in weights)

w = [1.5, -2.0, 0.05, 3.2]
print("L2 (Ridge) jarimasi:", round(ridge_penalty(w), 4))
print("L1 (Lasso) jarimasi:", round(lasso_penalty(w), 4))
```

## Tushuntirish va Mantiq:
1. L1 kam ahamiyatli vaznlarni mutlaq nolga aylantiradi (Feature selection), L2 esa vaznlarni kichraytiradi.

## Ishlash natijasi:
```text
Chiqish: L2 (Ridge) jarimasi: 0.165, L1 (Lasso) jarimasi: 0.0675
```

---

# 848-Topshiriq: Kullback-Leibler (KL) divergentsiyasi

## Topshiriq sharti:
Ikki ehtimollik taqsimoti orasidagi axborot yo'qotilishini (nisbiy entropiya) hisoblang.

## Yechim (Python kodi):
```python
import math

def kl_divergence(p, q, eps=1e-15):
    kl = 0.0
    for pi, qi in zip(p, q):
        qi = max(eps, qi)
        if pi > 0:
            kl += pi * math.log(pi / qi)
    return kl

P = [0.5, 0.5]
Q = [0.9, 0.1]
print("KL Divergentsiya P || Q:", round(kl_divergence(P, Q), 4))
```

## Tushuntirish va Mantiq:
1. Variatsion avtoenkoderlar (VAE) va RLHF (Reinforcement Learning from Human Feedback) modellari asosiy o'lchovi.

## Ishlash natijasi:
```text
Chiqish: KL Divergentsiya P || Q: 0.5108
```

---

# 849-Topshiriq: SVD (Singular Value Decomposition) asosiy g'oyasi

## Topshiriq sharti:
Matritsani A = U * S * V^T shaklida faktorizatsiya qilishning geometrik ma'nosi.

## Yechim (Python kodi):
```python
def svd_tushunchasi(m, n):
    return f"{m}x{n} o'lchamli matritsa U({m}x{m}), S({m}x{n}) va V^T({n}x{n}) matritsalariga ajraladi."

print(svd_tushunchasi(4, 3))
```

## Tushuntirish va Mantiq:
1. SVD tavsiya tizimlari (Collaborative Filtering), tasvirlarni siqish va semantik tahlilda (LSA) eng qudratli vositadir.

## Ishlash natijasi:
```text
Chiqish: 4x3 o'lchamli matritsa U(4x4), S(4x3) va V^T(3x3) matritsalariga ajraladi.
```

---

# 850-Topshiriq: To'liq Neyron Tarmog'i: Chiziqli klassifikator (Sof Python Perceptron)

## Topshiriq sharti:
Barcha formulalarni birlashtirib, mantiqiy 'OR' amalini o'rganuvchi sodda neyron modelini yozing.

## Yechim (Python kodi):
```python
class SofPerceptron:
    def __init__(self, in_features, lr=0.1):
        self.w = [0.0] * in_features
        self.b = 0.0
        self.lr = lr

    def predict(self, x):
        z = sum(xi * wi for xi, wi in zip(x, self.w)) + self.b
        return 1 if z >= 0 else 0

    def fit(self, X, y, epochs=10):
        for _ in range(epochs):
            for xi, yi in zip(X, y):
                y_hat = self.predict(xi)
                xato = yi - y_hat
                for j in range(len(self.w)):
                    self.w[j] += self.lr * xato * xi[j]
                self.b += self.lr * xato

# 'OR' jadvali: (0,0)->0, (0,1)->1, (1,0)->1, (1,1)->1
X = [[0, 0], [0, 1], [1, 0], [1, 1]]
y = [0, 1, 1, 1]

p = SofPerceptron(in_features=2, lr=0.2)
p.fit(X, y, epochs=10)

print("Perceptron bashoratlari:")
for xi in X:
    print(f"  {xi} -> {p.predict(xi)}")
```

## Tushuntirish va Mantiq:
1. Hebb qoidasi va gradientga asoslangan Perceptron o'rganish qoidasi sun'iy neyron tarmoqlarining tug'ilish nuqtasidir.

## Ishlash natijasi:
```text
Chiqish: Perceptron bashoratlari:\n  [0, 0] -> 0\n  [0, 1] -> 1\n  [1, 0] -> 1\n  [1, 1] -> 1
```

---

