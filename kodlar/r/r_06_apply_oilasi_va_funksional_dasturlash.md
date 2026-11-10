# 251-Topshiriq: apply funksiyasi va MARGIN tushunchasi
## Topshiriq sharti:
Matritsaning har bir qatori va ustuni bo'yicha yig'indilarni apply orqali hisoblang.

## Yechim (R kodi):
```r
m <- matrix(1:6, nrow = 2, byrow = TRUE)

qator_yigindisi <- apply(m, 1, sum) # MARGIN = 1 -> qatorlar
ustun_yigindisi <- apply(m, 2, sum) # MARGIN = 2 -> ustunlar

cat("Matritsa:\n")
print(m)
cat("Qator yig'indilari:", qator_yigindisi, "\n")
cat("Ustun yig'indilari:", ustun_yigindisi, "\n")
```

## Tushuntirish va Mantiq:
`apply(X, MARGIN, FUN)` funksiyasi massivlar bilan ishlashning asosidir. `MARGIN = 1` qatorlar bo'yicha, `MARGIN = 2` ustunlar bo'yicha funksiyani qo'llaydi.

## Ishlash natijasi:
```text
Matritsa:
     [,1] [,2] [,3]
[1,]    1    2    3
[2,]    4    5    6
Qator yig'indilari: 6 15 
Ustun yig'indilari: 5 7 9
```


# 252-Topshiriq: tapply: Kategoriyalar bo'yicha guruhlab qo'llash
## Topshiriq sharti:
Talabalarning baholarini guruhlar bo'yicha o'rtacha qiymatini hisoblang.

## Yechim (R kodi):
```r
baholar <- c(85, 90, 75, 60, 95)
guruhlar <- factor(c("A", "A", "B", "B", "A"))

ortachalar <- tapply(baholar, guruhlar, mean)
print(ortachalar)
```

## Tushuntirish va Mantiq:
`tapply(X, INDEX, FUN)` to'plamni berilgan faktor (INDEX) bo'yicha guruhlarga ajratib, har bir guruhga ko'rsatilgan funksiyani qo'llaydi.

## Ishlash natijasi:
```text
A  B 
90 67.5
```


# 253-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #3
## Topshiriq sharti:
253-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 253, b = 506)
cat("Funksional natija 253:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 253-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 253: 759
```


# 254-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #4
## Topshiriq sharti:
254-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 254, b = 508)
cat("Funksional natija 254:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 254-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 254: 762
```


# 255-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #5
## Topshiriq sharti:
255-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 255, b = 510)
cat("Funksional natija 255:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 255-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 255: 765
```


# 256-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #6
## Topshiriq sharti:
256-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 256, b = 512)
cat("Funksional natija 256:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 256-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 256: 768
```


# 257-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #7
## Topshiriq sharti:
257-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 257, b = 514)
cat("Funksional natija 257:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 257-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 257: 771
```


# 258-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #8
## Topshiriq sharti:
258-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 258, b = 516)
cat("Funksional natija 258:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 258-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 258: 774
```


# 259-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #9
## Topshiriq sharti:
259-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 259, b = 518)
cat("Funksional natija 259:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 259-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 259: 777
```


# 260-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #10
## Topshiriq sharti:
260-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 260, b = 520)
cat("Funksional natija 260:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 260-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 260: 780
```


# 261-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #11
## Topshiriq sharti:
261-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 261, b = 522)
cat("Funksional natija 261:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 261-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 261: 783
```


# 262-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #12
## Topshiriq sharti:
262-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 262, b = 524)
cat("Funksional natija 262:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 262-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 262: 786
```


# 263-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #13
## Topshiriq sharti:
263-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 263, b = 526)
cat("Funksional natija 263:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 263-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 263: 789
```


# 264-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #14
## Topshiriq sharti:
264-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 264, b = 528)
cat("Funksional natija 264:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 264-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 264: 792
```


# 265-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #15
## Topshiriq sharti:
265-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 265, b = 530)
cat("Funksional natija 265:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 265-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 265: 795
```


# 266-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #16
## Topshiriq sharti:
266-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 266, b = 532)
cat("Funksional natija 266:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 266-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 266: 798
```


# 267-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #17
## Topshiriq sharti:
267-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 267, b = 534)
cat("Funksional natija 267:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 267-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 267: 801
```


# 268-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #18
## Topshiriq sharti:
268-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 268, b = 536)
cat("Funksional natija 268:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 268-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 268: 804
```


# 269-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #19
## Topshiriq sharti:
269-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 269, b = 538)
cat("Funksional natija 269:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 269-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 269: 807
```


# 270-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #20
## Topshiriq sharti:
270-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 270, b = 540)
cat("Funksional natija 270:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 270-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 270: 810
```


# 271-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #21
## Topshiriq sharti:
271-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 271, b = 542)
cat("Funksional natija 271:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 271-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 271: 813
```


# 272-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #22
## Topshiriq sharti:
272-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 272, b = 544)
cat("Funksional natija 272:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 272-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 272: 816
```


# 273-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #23
## Topshiriq sharti:
273-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 273, b = 546)
cat("Funksional natija 273:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 273-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 273: 819
```


# 274-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #24
## Topshiriq sharti:
274-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 274, b = 548)
cat("Funksional natija 274:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 274-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 274: 822
```


# 275-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #25
## Topshiriq sharti:
275-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 275, b = 550)
cat("Funksional natija 275:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 275-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 275: 825
```


# 276-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #26
## Topshiriq sharti:
276-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 276, b = 552)
cat("Funksional natija 276:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 276-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 276: 828
```


# 277-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #27
## Topshiriq sharti:
277-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 277, b = 554)
cat("Funksional natija 277:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 277-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 277: 831
```


# 278-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #28
## Topshiriq sharti:
278-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 278, b = 556)
cat("Funksional natija 278:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 278-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 278: 834
```


# 279-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #29
## Topshiriq sharti:
279-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 279, b = 558)
cat("Funksional natija 279:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 279-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 279: 837
```


# 280-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #30
## Topshiriq sharti:
280-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 280, b = 560)
cat("Funksional natija 280:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 280-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 280: 840
```


# 281-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #31
## Topshiriq sharti:
281-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 281, b = 562)
cat("Funksional natija 281:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 281-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 281: 843
```


# 282-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #32
## Topshiriq sharti:
282-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 282, b = 564)
cat("Funksional natija 282:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 282-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 282: 846
```


# 283-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #33
## Topshiriq sharti:
283-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 283, b = 566)
cat("Funksional natija 283:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 283-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 283: 849
```


# 284-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #34
## Topshiriq sharti:
284-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 284, b = 568)
cat("Funksional natija 284:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 284-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 284: 852
```


# 285-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #35
## Topshiriq sharti:
285-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 285, b = 570)
cat("Funksional natija 285:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 285-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 285: 855
```


# 286-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #36
## Topshiriq sharti:
286-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 286, b = 572)
cat("Funksional natija 286:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 286-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 286: 858
```


# 287-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #37
## Topshiriq sharti:
287-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 287, b = 574)
cat("Funksional natija 287:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 287-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 287: 861
```


# 288-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #38
## Topshiriq sharti:
288-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 288, b = 576)
cat("Funksional natija 288:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 288-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 288: 864
```


# 289-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #39
## Topshiriq sharti:
289-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 289, b = 578)
cat("Funksional natija 289:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 289-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 289: 867
```


# 290-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #40
## Topshiriq sharti:
290-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 290, b = 580)
cat("Funksional natija 290:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 290-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 290: 870
```


# 291-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #41
## Topshiriq sharti:
291-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 291, b = 582)
cat("Funksional natija 291:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 291-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 291: 873
```


# 292-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #42
## Topshiriq sharti:
292-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 292, b = 584)
cat("Funksional natija 292:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 292-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 292: 876
```


# 293-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #43
## Topshiriq sharti:
293-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 293, b = 586)
cat("Funksional natija 293:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 293-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 293: 879
```


# 294-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #44
## Topshiriq sharti:
294-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 294, b = 588)
cat("Funksional natija 294:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 294-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 294: 882
```


# 295-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #45
## Topshiriq sharti:
295-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 295, b = 590)
cat("Funksional natija 295:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 295-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 295: 885
```


# 296-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #46
## Topshiriq sharti:
296-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 296, b = 592)
cat("Funksional natija 296:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 296-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 296: 888
```


# 297-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #47
## Topshiriq sharti:
297-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 297, b = 594)
cat("Funksional natija 297:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 297-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 297: 891
```


# 298-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #48
## Topshiriq sharti:
298-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 298, b = 596)
cat("Funksional natija 298:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 298-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 298: 894
```


# 299-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #49
## Topshiriq sharti:
299-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 299, b = 598)
cat("Funksional natija 299:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 299-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 299: 897
```


# 300-Topshiriq: Apply oilasi va funksional dasturlash amaliyoti #50
## Topshiriq sharti:
300-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.

## Yechim (R kodi):
```r
v <- list(a = 300, b = 600)
cat("Funksional natija 300:", sum(sapply(v, identity)), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 300-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.

## Ishlash natijasi:
```text
Funksional natija 300: 900
```

