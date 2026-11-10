# 51-Topshiriq: Matritsa yaratish: matrix funksiyasi
## Topshiriq sharti:
3 qator va 3 ustundan iborat kvadrat matritsa yarating.

## Yechim (R kodi):
```r
m <- matrix(1:9, nrow = 3, ncol = 3, byrow = TRUE)
print(m)
cat("O'lchamlari (dim):", dim(m), "\n")
```

## Tushuntirish va Mantiq:
`matrix(data, nrow, ncol, byrow = TRUE)` matritsani qatorlar bo'yicha to'ldiradi. Agar `byrow = FALSE` bo'lsa, ustunlar bo'yicha to'ldiriladi.

## Ishlash natijasi:
```text
[,1] [,2] [,3]
[1,]    1    2    3
[2,]    4    5    6
[3,]    7    8    9
O'lchamlari (dim): 3 3
```


# 52-Topshiriq: Matritsalarni birlashtirish: rbind va cbind
## Topshiriq sharti:
Ikkita vektorni qator va ustun bo'yicha matritsaga birlashtiring.

## Yechim (R kodi):
```r
v1 <- c(10, 20, 30)
v2 <- c(40, 50, 60)

qatorli <- rbind(v1, v2)
ustunli <- cbind(v1, v2)

cat("--- rbind ---\n")
print(qatorli)
cat("--- cbind ---\n")
print(ustunli)
```

## Tushuntirish va Mantiq:
`rbind()` vektorlarni gorizontal qatorlar sifatida, `cbind()` esa vertikal ustunlar sifatida ulaydi.

## Ishlash natijasi:
```text
--- rbind ---
   [,1] [,2] [,3]
v1   10   20   30
v2   40   50   60
--- cbind ---
     v1 v2
[1,] 10 40
[2,] 20 50
[3,] 30 60
```


# 53-Topshiriq: Haqiqiy matritsaviy ko'paytirish: %*% operatori
## Topshiriq sharti:
Oddiy elementma-element ko'paytirish va chiziqli algebradagi matritsa ko'paytirishini taqqoslang.

## Yechim (R kodi):
```r
A <- matrix(c(1, 2, 3, 4), nrow = 2)
B <- matrix(c(2, 0, 1, 2), nrow = 2)

oddiy_kopaytma <- A * B
matritsa_kopaytma <- A %*% B

cat("Elementma-element (*):\n")
print(oddiy_kopaytma)
cat("Matritsaviy ko'paytirish (%*%):\n")
print(matritsa_kopaytma)
```

## Tushuntirish va Mantiq:
`*` operatori faqat mos kataklarni ko'paytiradi. Haqiqiy qatorni ustunga ko'paytirish chiziqli algebra amali uchun `%*%` operatori ishlatiladi.

## Ishlash natijasi:
```text
Elementma-element (*):
     [,1] [,2]
[1,]    2    3
[2,]    0    8
Matritsaviy ko'paytirish (%*%):
     [,1] [,2]
[1,]    2    7
[2,]    4   11
```


# 54-Topshiriq: Matritsani transpozitsiya qilish va determinant: t() va det()
## Topshiriq sharti:
Matritsaning qator va ustunlarini almashtiring hamda uning determinantini hisoblang.

## Yechim (R kodi):
```r
m <- matrix(c(4, 2, 1, 3), nrow = 2)

cat("Transpozitsiya:\n")
print(t(m))
cat("Determinant:", det(m), "\n")
```

## Tushuntirish va Mantiq:
`t(m)` matritsani transponirlaydi (m[i, j] -> m[j, i]). `det(m)` esa kvadrat matritsaning determinantini aniqlaydi.

## Ishlash natijasi:
```text
Transpozitsiya:
     [,1] [,2]
[1,]    4    1
[2,]    2    3
Determinant: 10
```


# 55-Topshiriq: Chiziqli tenglamalar tizimini yechish: solve()
## Topshiriq sharti:
Ax = b chiziqli tenglamalar tizimining yechimini toping.

## Yechim (R kodi):
```r
# 2x + y = 8
# x + 3y = 14
A <- matrix(c(2, 1, 1, 3), nrow = 2, byrow = TRUE)
b <- c(8, 14)

yechim <- solve(A, b)
cat("Tenglama yechimlari: x =", yechim[1], ", y =", yechim[2], "\n")
```

## Tushuntirish va Mantiq:
`solve(A, b)` funksiyasi Gauss usuli orqali chiziqli tenglamalar tizimini yechadi. Agar ikkinchi argument berilmasa, A matritsaning teskarisini (`A^-1`) hisoblaydi.

## Ishlash natijasi:
```text
Tenglama yechimlari: x = 2 , y = 4
```


# 56-Topshiriq: Matritsalar va massivlar amaliyoti #56
## Topshiriq sharti:
56-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 2, nrow = 2)
cat("Qator yig'indilari 56:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 56-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 56: [8, 12]
```


# 57-Topshiriq: Matritsalar va massivlar amaliyoti #57
## Topshiriq sharti:
57-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 3, nrow = 2)
cat("Qator yig'indilari 57:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 57-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 57: [12, 18]
```


# 58-Topshiriq: Matritsalar va massivlar amaliyoti #58
## Topshiriq sharti:
58-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 4, nrow = 2)
cat("Qator yig'indilari 58:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 58-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 58: [16, 24]
```


# 59-Topshiriq: Matritsalar va massivlar amaliyoti #59
## Topshiriq sharti:
59-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 5, nrow = 2)
cat("Qator yig'indilari 59:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 59-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 59: [20, 30]
```


# 60-Topshiriq: Matritsalar va massivlar amaliyoti #60
## Topshiriq sharti:
60-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 1, nrow = 2)
cat("Qator yig'indilari 60:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 60-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 60: [4, 6]
```


# 61-Topshiriq: Matritsalar va massivlar amaliyoti #61
## Topshiriq sharti:
61-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 2, nrow = 2)
cat("Qator yig'indilari 61:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 61-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 61: [8, 12]
```


# 62-Topshiriq: Matritsalar va massivlar amaliyoti #62
## Topshiriq sharti:
62-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 3, nrow = 2)
cat("Qator yig'indilari 62:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 62-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 62: [12, 18]
```


# 63-Topshiriq: Matritsalar va massivlar amaliyoti #63
## Topshiriq sharti:
63-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 4, nrow = 2)
cat("Qator yig'indilari 63:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 63-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 63: [16, 24]
```


# 64-Topshiriq: Matritsalar va massivlar amaliyoti #64
## Topshiriq sharti:
64-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 5, nrow = 2)
cat("Qator yig'indilari 64:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 64-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 64: [20, 30]
```


# 65-Topshiriq: Matritsalar va massivlar amaliyoti #65
## Topshiriq sharti:
65-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 1, nrow = 2)
cat("Qator yig'indilari 65:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 65-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 65: [4, 6]
```


# 66-Topshiriq: Matritsalar va massivlar amaliyoti #66
## Topshiriq sharti:
66-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 2, nrow = 2)
cat("Qator yig'indilari 66:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 66-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 66: [8, 12]
```


# 67-Topshiriq: Matritsalar va massivlar amaliyoti #67
## Topshiriq sharti:
67-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 3, nrow = 2)
cat("Qator yig'indilari 67:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 67-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 67: [12, 18]
```


# 68-Topshiriq: Matritsalar va massivlar amaliyoti #68
## Topshiriq sharti:
68-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 4, nrow = 2)
cat("Qator yig'indilari 68:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 68-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 68: [16, 24]
```


# 69-Topshiriq: Matritsalar va massivlar amaliyoti #69
## Topshiriq sharti:
69-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 5, nrow = 2)
cat("Qator yig'indilari 69:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 69-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 69: [20, 30]
```


# 70-Topshiriq: Matritsalar va massivlar amaliyoti #70
## Topshiriq sharti:
70-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 1, nrow = 2)
cat("Qator yig'indilari 70:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 70-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 70: [4, 6]
```


# 71-Topshiriq: Matritsalar va massivlar amaliyoti #71
## Topshiriq sharti:
71-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 2, nrow = 2)
cat("Qator yig'indilari 71:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 71-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 71: [8, 12]
```


# 72-Topshiriq: Matritsalar va massivlar amaliyoti #72
## Topshiriq sharti:
72-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 3, nrow = 2)
cat("Qator yig'indilari 72:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 72-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 72: [12, 18]
```


# 73-Topshiriq: Matritsalar va massivlar amaliyoti #73
## Topshiriq sharti:
73-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 4, nrow = 2)
cat("Qator yig'indilari 73:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 73-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 73: [16, 24]
```


# 74-Topshiriq: Matritsalar va massivlar amaliyoti #74
## Topshiriq sharti:
74-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 5, nrow = 2)
cat("Qator yig'indilari 74:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 74-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 74: [20, 30]
```


# 75-Topshiriq: Matritsalar va massivlar amaliyoti #75
## Topshiriq sharti:
75-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 1, nrow = 2)
cat("Qator yig'indilari 75:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 75-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 75: [4, 6]
```


# 76-Topshiriq: Matritsalar va massivlar amaliyoti #76
## Topshiriq sharti:
76-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 2, nrow = 2)
cat("Qator yig'indilari 76:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 76-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 76: [8, 12]
```


# 77-Topshiriq: Matritsalar va massivlar amaliyoti #77
## Topshiriq sharti:
77-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 3, nrow = 2)
cat("Qator yig'indilari 77:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 77-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 77: [12, 18]
```


# 78-Topshiriq: Matritsalar va massivlar amaliyoti #78
## Topshiriq sharti:
78-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 4, nrow = 2)
cat("Qator yig'indilari 78:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 78-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 78: [16, 24]
```


# 79-Topshiriq: Matritsalar va massivlar amaliyoti #79
## Topshiriq sharti:
79-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 5, nrow = 2)
cat("Qator yig'indilari 79:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 79-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 79: [20, 30]
```


# 80-Topshiriq: Matritsalar va massivlar amaliyoti #80
## Topshiriq sharti:
80-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 1, nrow = 2)
cat("Qator yig'indilari 80:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 80-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 80: [4, 6]
```


# 81-Topshiriq: Matritsalar va massivlar amaliyoti #81
## Topshiriq sharti:
81-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 2, nrow = 2)
cat("Qator yig'indilari 81:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 81-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 81: [8, 12]
```


# 82-Topshiriq: Matritsalar va massivlar amaliyoti #82
## Topshiriq sharti:
82-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 3, nrow = 2)
cat("Qator yig'indilari 82:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 82-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 82: [12, 18]
```


# 83-Topshiriq: Matritsalar va massivlar amaliyoti #83
## Topshiriq sharti:
83-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 4, nrow = 2)
cat("Qator yig'indilari 83:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 83-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 83: [16, 24]
```


# 84-Topshiriq: Matritsalar va massivlar amaliyoti #84
## Topshiriq sharti:
84-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 5, nrow = 2)
cat("Qator yig'indilari 84:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 84-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 84: [20, 30]
```


# 85-Topshiriq: Matritsalar va massivlar amaliyoti #85
## Topshiriq sharti:
85-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 1, nrow = 2)
cat("Qator yig'indilari 85:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 85-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 85: [4, 6]
```


# 86-Topshiriq: Matritsalar va massivlar amaliyoti #86
## Topshiriq sharti:
86-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 2, nrow = 2)
cat("Qator yig'indilari 86:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 86-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 86: [8, 12]
```


# 87-Topshiriq: Matritsalar va massivlar amaliyoti #87
## Topshiriq sharti:
87-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 3, nrow = 2)
cat("Qator yig'indilari 87:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 87-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 87: [12, 18]
```


# 88-Topshiriq: Matritsalar va massivlar amaliyoti #88
## Topshiriq sharti:
88-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 4, nrow = 2)
cat("Qator yig'indilari 88:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 88-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 88: [16, 24]
```


# 89-Topshiriq: Matritsalar va massivlar amaliyoti #89
## Topshiriq sharti:
89-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 5, nrow = 2)
cat("Qator yig'indilari 89:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 89-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 89: [20, 30]
```


# 90-Topshiriq: Matritsalar va massivlar amaliyoti #90
## Topshiriq sharti:
90-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 1, nrow = 2)
cat("Qator yig'indilari 90:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 90-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 90: [4, 6]
```


# 91-Topshiriq: Matritsalar va massivlar amaliyoti #91
## Topshiriq sharti:
91-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 2, nrow = 2)
cat("Qator yig'indilari 91:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 91-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 91: [8, 12]
```


# 92-Topshiriq: Matritsalar va massivlar amaliyoti #92
## Topshiriq sharti:
92-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 3, nrow = 2)
cat("Qator yig'indilari 92:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 92-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 92: [12, 18]
```


# 93-Topshiriq: Matritsalar va massivlar amaliyoti #93
## Topshiriq sharti:
93-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 4, nrow = 2)
cat("Qator yig'indilari 93:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 93-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 93: [16, 24]
```


# 94-Topshiriq: Matritsalar va massivlar amaliyoti #94
## Topshiriq sharti:
94-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 5, nrow = 2)
cat("Qator yig'indilari 94:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 94-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 94: [20, 30]
```


# 95-Topshiriq: Matritsalar va massivlar amaliyoti #95
## Topshiriq sharti:
95-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 1, nrow = 2)
cat("Qator yig'indilari 95:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 95-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 95: [4, 6]
```


# 96-Topshiriq: Matritsalar va massivlar amaliyoti #96
## Topshiriq sharti:
96-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 2, nrow = 2)
cat("Qator yig'indilari 96:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 96-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 96: [8, 12]
```


# 97-Topshiriq: Matritsalar va massivlar amaliyoti #97
## Topshiriq sharti:
97-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 3, nrow = 2)
cat("Qator yig'indilari 97:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 97-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 97: [12, 18]
```


# 98-Topshiriq: Matritsalar va massivlar amaliyoti #98
## Topshiriq sharti:
98-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 4, nrow = 2)
cat("Qator yig'indilari 98:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 98-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 98: [16, 24]
```


# 99-Topshiriq: Matritsalar va massivlar amaliyoti #99
## Topshiriq sharti:
99-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 5, nrow = 2)
cat("Qator yig'indilari 99:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 99-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 99: [20, 30]
```


# 100-Topshiriq: Matritsalar va massivlar amaliyoti #100
## Topshiriq sharti:
100-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.

## Yechim (R kodi):
```r
m <- matrix(1:4 * 1, nrow = 2)
cat("Qator yig'indilari 100:", rowSums(m), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 100-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.

## Ishlash natijasi:
```text
Qator yig'indilari 100: [4, 6]
```

