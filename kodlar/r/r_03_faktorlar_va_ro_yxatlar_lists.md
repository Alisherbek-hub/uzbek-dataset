# 101-Topshiriq: Faktorlar (Factors) va darajalar (Levels)
## Topshiriq sharti:
Kategorik ma'lumotlarni faktor shaklida e'lon qiling va uning chastotasini ko'ring.

## Yechim (R kodi):
```r
jins <- factor(c("Erkak", "Ayol", "Ayol", "Erkak", "Erkak"))

print(jins)
cat("Darajalar (Levels):", levels(jins), "\n")
cat("Chastota jadvali:\n")
print(table(jins))
```

## Tushuntirish va Mantiq:
Faktorlar R tilida kategorik (nominal yoki ordinal) ma'lumotlarni tahlil qilish uchun xizmat qiladi. Ular xotirada raqamli butun sonlar sifatida ixcham saqlanadi.

## Ishlash natijasi:
```text
[1] Erkak Ayol  Ayol  Erkak Erkak
Levels: Ayol Erkak
Chastota jadvali:
jins
 Ayol Erkak 
    2     3
```


# 102-Topshiriq: Ro'yxatlar (Lists) yaratish va murojaat: $ va [[ ]]
## Topshiriq sharti:
Turli xil ma'lumot turlarini bitta ro'yxatda birlashtiring.

## Yechim (R kodi):
```r
talaba <- list(
  ism = "Sardor",
  yosh = 22,
  baholar = c(85, 90, 78),
  stipendiya = TRUE
)

cat("Talaba ismi:", talaba$ism, "\n")
cat("O'rtacha bahosi:", mean(talaba$baholar), "\n")
```

## Tushuntirish va Mantiq:
Ro'yxat (List) R-da turli tiplarni (son, matn, vektor, matritsa) o'z ichiga oluvchi eng moslashuvchan konteynerdir. Maydonlarga `$` yoki `[[nom]]` orqali murojaat qilinadi.

## Ishlash natijasi:
```text
Talaba ismi: Sardor 
O'rtacha bahosi: 84.33333
```


# 103-Topshiriq: Ro'yxat ustida lapply va sapply funksiyalari
## Topshiriq sharti:
Ro'yxatdagi har bir element uchun o'rtacha qiymatni hisoblang.

## Yechim (R kodi):
```r
guruhlar <- list(
  guruh_a = c(80, 85, 90),
  guruh_b = c(60, 75, 70),
  guruh_c = c(95, 98, 92)
)

ortachalar <- sapply(guruhlar, mean)
print(ortachalar)
```

## Tushuntirish va Mantiq:
`lapply()` natijani ro'yxat ko'rinishida qaytaradi, `sapply()` esa natijani vektorga soddalashtiradi (simplify).

## Ishlash natijasi:
```text
guruh_a guruh_b guruh_c 
     85      68      95
```


# 104-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #104
## Topshiriq sharti:
104-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 104, qiymatlar = c(104, 208))
cat("ID 104:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 104-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 104: 104 | Yig'indi: 312
```


# 105-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #105
## Topshiriq sharti:
105-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 105, qiymatlar = c(105, 210))
cat("ID 105:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 105-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 105: 105 | Yig'indi: 315
```


# 106-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #106
## Topshiriq sharti:
106-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 106, qiymatlar = c(106, 212))
cat("ID 106:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 106-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 106: 106 | Yig'indi: 318
```


# 107-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #107
## Topshiriq sharti:
107-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 107, qiymatlar = c(107, 214))
cat("ID 107:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 107-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 107: 107 | Yig'indi: 321
```


# 108-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #108
## Topshiriq sharti:
108-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 108, qiymatlar = c(108, 216))
cat("ID 108:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 108-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 108: 108 | Yig'indi: 324
```


# 109-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #109
## Topshiriq sharti:
109-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 109, qiymatlar = c(109, 218))
cat("ID 109:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 109-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 109: 109 | Yig'indi: 327
```


# 110-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #110
## Topshiriq sharti:
110-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 110, qiymatlar = c(110, 220))
cat("ID 110:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 110-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 110: 110 | Yig'indi: 330
```


# 111-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #111
## Topshiriq sharti:
111-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 111, qiymatlar = c(111, 222))
cat("ID 111:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 111-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 111: 111 | Yig'indi: 333
```


# 112-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #112
## Topshiriq sharti:
112-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 112, qiymatlar = c(112, 224))
cat("ID 112:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 112-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 112: 112 | Yig'indi: 336
```


# 113-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #113
## Topshiriq sharti:
113-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 113, qiymatlar = c(113, 226))
cat("ID 113:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 113-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 113: 113 | Yig'indi: 339
```


# 114-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #114
## Topshiriq sharti:
114-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 114, qiymatlar = c(114, 228))
cat("ID 114:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 114-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 114: 114 | Yig'indi: 342
```


# 115-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #115
## Topshiriq sharti:
115-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 115, qiymatlar = c(115, 230))
cat("ID 115:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 115-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 115: 115 | Yig'indi: 345
```


# 116-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #116
## Topshiriq sharti:
116-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 116, qiymatlar = c(116, 232))
cat("ID 116:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 116-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 116: 116 | Yig'indi: 348
```


# 117-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #117
## Topshiriq sharti:
117-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 117, qiymatlar = c(117, 234))
cat("ID 117:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 117-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 117: 117 | Yig'indi: 351
```


# 118-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #118
## Topshiriq sharti:
118-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 118, qiymatlar = c(118, 236))
cat("ID 118:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 118-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 118: 118 | Yig'indi: 354
```


# 119-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #119
## Topshiriq sharti:
119-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 119, qiymatlar = c(119, 238))
cat("ID 119:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 119-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 119: 119 | Yig'indi: 357
```


# 120-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #120
## Topshiriq sharti:
120-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 120, qiymatlar = c(120, 240))
cat("ID 120:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 120-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 120: 120 | Yig'indi: 360
```


# 121-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #121
## Topshiriq sharti:
121-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 121, qiymatlar = c(121, 242))
cat("ID 121:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 121-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 121: 121 | Yig'indi: 363
```


# 122-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #122
## Topshiriq sharti:
122-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 122, qiymatlar = c(122, 244))
cat("ID 122:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 122-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 122: 122 | Yig'indi: 366
```


# 123-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #123
## Topshiriq sharti:
123-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 123, qiymatlar = c(123, 246))
cat("ID 123:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 123-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 123: 123 | Yig'indi: 369
```


# 124-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #124
## Topshiriq sharti:
124-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 124, qiymatlar = c(124, 248))
cat("ID 124:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 124-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 124: 124 | Yig'indi: 372
```


# 125-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #125
## Topshiriq sharti:
125-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 125, qiymatlar = c(125, 250))
cat("ID 125:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 125-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 125: 125 | Yig'indi: 375
```


# 126-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #126
## Topshiriq sharti:
126-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 126, qiymatlar = c(126, 252))
cat("ID 126:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 126-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 126: 126 | Yig'indi: 378
```


# 127-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #127
## Topshiriq sharti:
127-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 127, qiymatlar = c(127, 254))
cat("ID 127:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 127-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 127: 127 | Yig'indi: 381
```


# 128-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #128
## Topshiriq sharti:
128-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 128, qiymatlar = c(128, 256))
cat("ID 128:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 128-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 128: 128 | Yig'indi: 384
```


# 129-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #129
## Topshiriq sharti:
129-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 129, qiymatlar = c(129, 258))
cat("ID 129:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 129-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 129: 129 | Yig'indi: 387
```


# 130-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #130
## Topshiriq sharti:
130-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 130, qiymatlar = c(130, 260))
cat("ID 130:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 130-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 130: 130 | Yig'indi: 390
```


# 131-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #131
## Topshiriq sharti:
131-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 131, qiymatlar = c(131, 262))
cat("ID 131:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 131-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 131: 131 | Yig'indi: 393
```


# 132-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #132
## Topshiriq sharti:
132-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 132, qiymatlar = c(132, 264))
cat("ID 132:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 132-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 132: 132 | Yig'indi: 396
```


# 133-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #133
## Topshiriq sharti:
133-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 133, qiymatlar = c(133, 266))
cat("ID 133:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 133-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 133: 133 | Yig'indi: 399
```


# 134-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #134
## Topshiriq sharti:
134-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 134, qiymatlar = c(134, 268))
cat("ID 134:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 134-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 134: 134 | Yig'indi: 402
```


# 135-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #135
## Topshiriq sharti:
135-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 135, qiymatlar = c(135, 270))
cat("ID 135:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 135-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 135: 135 | Yig'indi: 405
```


# 136-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #136
## Topshiriq sharti:
136-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 136, qiymatlar = c(136, 272))
cat("ID 136:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 136-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 136: 136 | Yig'indi: 408
```


# 137-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #137
## Topshiriq sharti:
137-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 137, qiymatlar = c(137, 274))
cat("ID 137:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 137-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 137: 137 | Yig'indi: 411
```


# 138-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #138
## Topshiriq sharti:
138-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 138, qiymatlar = c(138, 276))
cat("ID 138:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 138-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 138: 138 | Yig'indi: 414
```


# 139-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #139
## Topshiriq sharti:
139-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 139, qiymatlar = c(139, 278))
cat("ID 139:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 139-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 139: 139 | Yig'indi: 417
```


# 140-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #140
## Topshiriq sharti:
140-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 140, qiymatlar = c(140, 280))
cat("ID 140:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 140-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 140: 140 | Yig'indi: 420
```


# 141-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #141
## Topshiriq sharti:
141-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 141, qiymatlar = c(141, 282))
cat("ID 141:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 141-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 141: 141 | Yig'indi: 423
```


# 142-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #142
## Topshiriq sharti:
142-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 142, qiymatlar = c(142, 284))
cat("ID 142:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 142-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 142: 142 | Yig'indi: 426
```


# 143-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #143
## Topshiriq sharti:
143-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 143, qiymatlar = c(143, 286))
cat("ID 143:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 143-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 143: 143 | Yig'indi: 429
```


# 144-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #144
## Topshiriq sharti:
144-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 144, qiymatlar = c(144, 288))
cat("ID 144:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 144-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 144: 144 | Yig'indi: 432
```


# 145-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #145
## Topshiriq sharti:
145-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 145, qiymatlar = c(145, 290))
cat("ID 145:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 145-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 145: 145 | Yig'indi: 435
```


# 146-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #146
## Topshiriq sharti:
146-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 146, qiymatlar = c(146, 292))
cat("ID 146:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 146-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 146: 146 | Yig'indi: 438
```


# 147-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #147
## Topshiriq sharti:
147-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 147, qiymatlar = c(147, 294))
cat("ID 147:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 147-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 147: 147 | Yig'indi: 441
```


# 148-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #148
## Topshiriq sharti:
148-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 148, qiymatlar = c(148, 296))
cat("ID 148:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 148-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 148: 148 | Yig'indi: 444
```


# 149-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #149
## Topshiriq sharti:
149-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 149, qiymatlar = c(149, 298))
cat("ID 149:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 149-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 149: 149 | Yig'indi: 447
```


# 150-Topshiriq: Faktorlar va ro'yxatlar amaliyoti #150
## Topshiriq sharti:
150-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.

## Yechim (R kodi):
```r
lst <- list(id = 150, qiymatlar = c(150, 300))
cat("ID 150:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\n")
```

## Tushuntirish va Mantiq:
Ushbu 150-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.

## Ishlash natijasi:
```text
ID 150: 150 | Yig'indi: 450
```

