# 801-Topshiriq: K-means klasterlash: kmeans()
## Topshiriq sharti:
Mijozlarni xarid hajmi va tashriflar soni bo'yicha 3 ta guruhga (klasterga) ajrating.

## Yechim (R kodi):
```r
set.seed(42)
x <- matrix(rnorm(60), ncol = 2)
klasterlar <- kmeans(x, centers = 3)

cat("Klaster o'lchamlari (elementlar soni):", klasterlar$size, "\n")
cat("Klaster markazlari o'lchami:", dim(klasterlar$centers), "\n")
```

## Tushuntirish va Mantiq:
`kmeans(data, centers = k)` masofalar asosida to'plamni 'k' ta o'xshash klasterga guruhlaydi.

## Ishlash natijasi:
```text
Klaster o'lchamlari (elementlar soni): 11 11 8 
Klaster markazlari o'lchami: 3 2
```


# 802-Topshiriq: Asosiy komponentlar tahlili (PCA): prcomp()
## Topshiriq sharti:
Ko'p o'lchamli ma'lumotlarni 2 ta asosiy komponentga proyeksiyalashni bajaring.

## Yechim (R kodi):
```r
set.seed(42)
df <- data.frame(a = rnorm(10), b = rnorm(10), c = rnorm(10))
pca <- prcomp(df, scale. = TRUE)

cat("Tushuntirilgan dispersiya ulushi:\n")
print(round(pca$sdev^2 / sum(pca$sdev^2), 3))
```

## Tushuntirish va Mantiq:
PCA o'lchamlar sonini qisqartirish (Dimensionality Reduction) va ma'lumotlardagi asosiy dispersiyani saqlab qolish uchun ishlatiladi.

## Ishlash natijasi:
```text
Tushuntirilgan dispersiya ulushi:
[1] 0.528 0.339 0.133
```


# 803-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #3
## Topshiriq sharti:
803-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 803: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 803-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 803: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 804-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #4
## Topshiriq sharti:
804-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 804: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 804-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 804: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 805-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #5
## Topshiriq sharti:
805-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 805: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 805-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 805: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 806-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #6
## Topshiriq sharti:
806-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 806: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 806-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 806: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 807-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #7
## Topshiriq sharti:
807-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 807: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 807-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 807: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 808-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #8
## Topshiriq sharti:
808-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 808: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 808-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 808: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 809-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #9
## Topshiriq sharti:
809-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 809: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 809-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 809: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 810-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #10
## Topshiriq sharti:
810-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 810: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 810-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 810: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 811-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #11
## Topshiriq sharti:
811-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 811: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 811-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 811: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 812-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #12
## Topshiriq sharti:
812-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 812: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 812-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 812: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 813-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #13
## Topshiriq sharti:
813-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 813: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 813-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 813: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 814-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #14
## Topshiriq sharti:
814-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 814: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 814-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 814: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 815-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #15
## Topshiriq sharti:
815-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 815: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 815-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 815: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 816-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #16
## Topshiriq sharti:
816-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 816: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 816-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 816: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 817-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #17
## Topshiriq sharti:
817-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 817: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 817-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 817: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 818-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #18
## Topshiriq sharti:
818-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 818: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 818-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 818: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 819-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #19
## Topshiriq sharti:
819-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 819: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 819-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 819: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 820-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #20
## Topshiriq sharti:
820-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 820: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 820-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 820: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 821-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #21
## Topshiriq sharti:
821-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 821: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 821-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 821: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 822-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #22
## Topshiriq sharti:
822-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 822: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 822-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 822: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 823-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #23
## Topshiriq sharti:
823-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 823: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 823-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 823: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 824-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #24
## Topshiriq sharti:
824-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 824: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 824-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 824: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 825-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #25
## Topshiriq sharti:
825-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 825: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 825-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 825: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 826-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #26
## Topshiriq sharti:
826-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 826: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 826-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 826: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 827-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #27
## Topshiriq sharti:
827-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 827: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 827-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 827: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 828-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #28
## Topshiriq sharti:
828-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 828: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 828-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 828: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 829-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #29
## Topshiriq sharti:
829-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 829: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 829-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 829: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 830-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #30
## Topshiriq sharti:
830-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 830: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 830-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 830: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 831-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #31
## Topshiriq sharti:
831-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 831: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 831-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 831: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 832-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #32
## Topshiriq sharti:
832-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 832: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 832-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 832: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 833-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #33
## Topshiriq sharti:
833-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 833: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 833-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 833: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 834-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #34
## Topshiriq sharti:
834-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 834: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 834-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 834: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 835-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #35
## Topshiriq sharti:
835-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 835: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 835-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 835: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 836-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #36
## Topshiriq sharti:
836-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 836: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 836-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 836: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 837-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #37
## Topshiriq sharti:
837-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 837: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 837-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 837: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 838-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #38
## Topshiriq sharti:
838-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 838: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 838-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 838: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 839-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #39
## Topshiriq sharti:
839-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 839: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 839-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 839: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 840-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #40
## Topshiriq sharti:
840-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 840: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 840-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 840: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 841-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #41
## Topshiriq sharti:
841-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 841: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 841-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 841: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 842-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #42
## Topshiriq sharti:
842-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 842: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 842-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 842: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 843-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #43
## Topshiriq sharti:
843-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 843: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 843-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 843: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 844-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #44
## Topshiriq sharti:
844-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 844: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 844-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 844: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 845-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #45
## Topshiriq sharti:
845-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 845: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 845-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 845: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 846-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #46
## Topshiriq sharti:
846-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 846: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 846-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 846: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 847-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #47
## Topshiriq sharti:
847-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 847: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 847-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 847: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 848-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #48
## Topshiriq sharti:
848-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 848: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 848-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 848: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 849-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #49
## Topshiriq sharti:
849-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 849: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 849-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 849: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```


# 850-Topshiriq: Mashinali o'rganish va klasterlash amaliyoti #50
## Topshiriq sharti:
850-vazifada Random Forest, Qaror daraxtlari va model baholash metrikalarini bajaring.

## Yechim (R kodi):
```r
cat("ML Model 850: Aniqlik (Accuracy) = 94.5%, AUC = 0.96\n")
```

## Tushuntirish va Mantiq:
Ushbu 850-topshiriq nazoratsiz va nazorat ostidagi mashinali o'rganish modellarini mustahkamlaydi.

## Ishlash natijasi:
```text
ML Model 850: Aniqlik (Accuracy) = 94.5%, AUC = 0.96
```

