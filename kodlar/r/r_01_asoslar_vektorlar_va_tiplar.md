# 1-Topshiriq: R konsoli bilan muloqot: print va cat funksiyalari
## Topshiriq sharti:
Ekranga xabarlarni chiqarish va o'zgaruvchilarni formatlab chop etish dasturini yozing.

## Yechim (R kodi):
```r
# print() obyekti va uning indeksini ko'rsatadi
print("Khorazmiy AI - R Tahlil Markaziga xush kelibsiz!")

# cat() bir nechta qiymatlarni birlashtirib bo'sh joysiz chiqaradi
nomi <- "R Dasturlash Tili"
versiya <- 4.3
cat("Tizim:", nomi, "| Versiya:", versiya, "\n")
```

## Tushuntirish va Mantiq:
R-da ma'lumot chiqarishning ikkita asosiy funksiyasi mavjud: `print()` obyektni o'zining strukturaviy ko'rinishida chiqaradi; `cat()` esa matn va o'zgaruvchilarni yangi qator belgisi `\n` bilan birlashtirib konsolga toza matn ko'rinishida uzatadi.

## Ishlash natijasi:
```text
[1] "Khorazmiy AI - R Tahlil Markaziga xush kelibsiz!"
Tizim: R Dasturlash Tili | Versiya: 4.3
```


# 2-Topshiriq: O'zgaruvchilar va biriktirish operatori: <- va =
## Topshiriq sharti:
R tilining an'anaviy biriktirish operatori `<-` orqali turli o'zgaruvchilar e'lon qiling.

## Yechim (R kodi):
```r
# R-da asosiy biriktirish operatori <- hisoblanadi
loyiha_nomi <- "Khorazmiy DataLab"
ishtirokchilar_soni <- 150
faol_holatda <- TRUE

cat("Loyiha:", loyiha_nomi, "\n")
cat("Ishtirokchilar:", ishtirokchilar_soni, "\n")
cat("Faolmi:", faol_holatda, "\n")
```

## Tushuntirish va Mantiq:
R dasturlash tilida qiymat biriktirish uchun an'anaviy ravishda chap strelka `<-` operatori qo'llaniladi. `=` operatori ham mavjud bo'lsa-da, u ko'proq funksiya argumentlarini uzatishda ishlatiladi. `<-` operatori R kodining o'qilishini tabiiy va aniq qiladi.

## Ishlash natijasi:
```text
Loyiha: Khorazmiy DataLab 
Ishtirokchilar: 150 
Faolmi: TRUE
```


# 3-Topshiriq: Atomik ma'lumotlar turlari: numeric, integer va character
## Topshiriq sharti:
Turli atomik tiplarga oid qiymatlar yarating va `typeof()` hamda `class()` orqali ularning turini tekshiring.

## Yechim (R kodi):
```r
son_double <- 42.5
son_integer <- 42L  # L suffiksi aniq Integer tipini bildiradi
matn <- "Statistika"
mantiqiy <- TRUE

cat("son_double turi:", typeof(son_double), "\n")
cat("son_integer turi:", typeof(son_integer), "\n")
cat("matn turi:", typeof(matn), "\n")
cat("mantiqiy turi:", typeof(mantiqiy), "\n")
```

## Tushuntirish va Mantiq:
R-da barcha oddiy sonlar sukut bo'yicha 64-bitli `numeric` (double) toifasida yaratiladi. Aniq butun son yaratish uchun son oxiriga `L` harfi qo'yiladi (masalan, `42L`). `typeof()` R ichki xotira turini, `class()` esa obyekt sinfini qaytaradi.

## Ishlash natijasi:
```text
son_double turi: double 
son_integer turi: integer 
matn turi: character 
mantiqiy turi: logical
```


# 4-Topshiriq: Vektor yaratish: c() funksiyasi (Combine)
## Topshiriq sharti:
Bir nechta sonli ma'lumotlarni birlashtirib vektor hosil qiling va uning uzunligini toping.

## Yechim (R kodi):
```r
haroratlar <- c(18.5, 21.0, 24.3, 19.8, 22.5)

print(haroratlar)
cat("O'lchovlar soni (uzunligi):", length(haroratlar), "\n")
cat("Turi:", typeof(haroratlar), "\n")
```

## Tushuntirish va Mantiq:
R-da skalyar (bitta son) tushunchasi yo'q — har qanday oddiy son aslida 1 ta elementli vektordir. Bir nechta elementlarni birlashtirish uchun `c()` (combine) funksiyasi ishlatiladi. Vektor bir xil turdagi elementlardan iborat bo'lishi shart.

## Ishlash natijasi:
```text
[1] 18.5 21.0 24.3 19.8 22.5
O'lchovlar soni (uzunligi): 5 
Turi: double
```


# 5-Topshiriq: Ketma-ketliklar yaratish: : operatori va seq() funksiyasi
## Topshiriq sharti:
1 dan 10 gacha va ma'lum qadamli sonlar ketma-ketligini hosil qiling.

## Yechim (R kodi):
```r
ketma_ketlik1 <- 1:5
ketma_ketlik2 <- seq(from = 10, to = 30, by = 5)
ketma_ketlik3 <- seq(from = 0, to = 1, length.out = 5)

print(ketma_ketlik1)
print(ketma_ketlik2)
print(ketma_ketlik3)
```

## Tushuntirish va Mantiq:
`boshlanish:tugash` sintaksisi 1 qadamli ketma-ketlik hosil qiladi. `seq()` funksiyasi esa qadam kattaligini (`by`) yoki hosil bo'ladigan elementlar sonini (`length.out`) aniq belgilash imkonini beradi.

## Ishlash natijasi:
```text
[1] 1 2 3 4 5
[1] 10 15 20 25 30
[1] 0.00 0.25 0.50 0.75 1.00
```


# 6-Topshiriq: Takrorlanuvchi vektorlar: rep() funksiyasi
## Topshiriq sharti:
Elementlarni umumiy yoki ketma-ket takrorlab vektorlar yarating.

## Yechim (R kodi):
```r
takror1 <- rep(1:3, times = 2)
takror2 <- rep(1:3, each = 2)

cat("rep(times = 2):", takror1, "\n")
cat("rep(each = 2):", takror2, "\n")
```

## Tushuntirish va Mantiq:
`rep(x, times = n)` butun vektorni ketma-ket n marta takrorlaydi. `rep(x, each = n)` esa har bir alohida elementni n martadan takrorlab boradi.

## Ishlash natijasi:
```text
rep(times = 2): 1 2 3 1 2 3 
rep(each = 2): 1 1 2 2 3 3
```


# 7-Topshiriq: Vektorlashtirilgan arifmetik amallar
## Topshiriq sharti:
Sikl yozmasdan ikkita vektor ustida to'g'ridan-to'g'ri arifmetik amallarni bajaring.

## Yechim (R kodi):
```r
a <- c(10, 20, 30)
b <- c(1, 2, 3)

yigindi <- a + b
kopaytma <- a * b
bolinma <- a / b

print(yigindi)
print(kopaytma)
print(bolinma)
```

## Tushuntirish va Mantiq:
R-ning eng katta qudrati uning vektorlashtirilgan (vectorized) hisoblashlaridadir. Amallar har bir element ustida parallel ravishda C tilidagi SIMD tezligida bajariladi.

## Ishlash natijasi:
```text
[1] 11 22 33
[1] 10 40 90
[1] 10 10 10
```


# 8-Topshiriq: Qayta ishlash qoidasi (Recycling Rule)
## Topshiriq sharti:
Uzunligi teng bo'lmagan vektorlar qo'shilganda R qanday yo'l tutishini tahlil qiling.

## Yechim (R kodi):
```r
katta <- c(10, 20, 30, 40)
kichik <- c(1, 2)

natija <- katta + kichik
print(natija)
```

## Tushuntirish va Mantiq:
R qisqa vektorni uzun vektor o'lchamiga yetguncha boshidan takrorlab (recycle qilib) oladi. 10+1, 20+2, 30+1, 40+2 tarzida hisoblanadi.

## Ishlash natijasi:
```text
[1] 11 22 31 42
```


# 9-Topshiriq: Vektor indekslash (1-based indexing) va musbat indekslar
## Topshiriq sharti:
Vektorning 1-chi va 3-chi elementlarini ajratib oling.

## Yechim (R kodi):
```r
shaharlar <- c("Toshkent", "Samarqand", "Buxoro", "Xiva")

cat("Birinchi shahar (indeks 1):", shaharlar[1], "\n")
cat("Uchinchi shahar (indeks 3):", shaharlar[3], "\n")
cat("1 va 4-shaharlar:", shaharlar[c(1, 4)], "\n")
```

## Tushuntirish va Mantiq:
Diqqat: C, Python yoki Java tillaridan farqli o'laroq, R tilida indekslash 0 dan emas, **1 dan boshlanadi**. Elementlar to'rtburchak qavs `v[i]` bilan olinadi.

## Ishlash natijasi:
```text
Birinchi shahar (indeks 1): Toshkent 
Uchinchi shahar (indeks 3): Buxoro 
1 va 4-shaharlar: Toshkent Xiva
```


# 10-Topshiriq: Manfiy indekslar bilan elementlarni chiqarib tashlash
## Topshiriq sharti:
Vektordan ikkinchi va to'rtinchi elementlarni o'chirib yangi vektor hosil qiling.

## Yechim (R kodi):
```r
sonlar <- c(10, 20, 30, 40, 50)
qolganlar <- sonlar[-c(2, 4)]

print(qolganlar)
```

## Tushuntirish va Mantiq:
R-da manfiy indeks `v[-i]` teskari indekslashni emas, balki ko'rsatilgan indeksdagi elementni to'plamdan **olib tashlash**ni bildiradi.

## Ishlash natijasi:
```text
[1] 10 30 50
```


# 11-Topshiriq: Mantiqiy indekslash va filtrlash
## Topshiriq sharti:
Berilgan chegaradan katta bo'lgan elementlarni mantiqiy shart orqali filtrlang.

## Yechim (R kodi):
```r
ballar <- c(75, 45, 88, 92, 59, 64)
otish_bali <- 60

otganlar <- ballar[ballar >= otish_bali]
cat("60 dan yuqori ballar:", otganlar, "\n")
```

## Tushuntirish va Mantiq:
`ballar >= 60` ifodasi mantiqiy vektor `[TRUE, FALSE, TRUE, ...]` hosil qiladi. Uni indeks qavsi `ballar[...]` ichiga qo'yish orqali faqat TRUE bo'lgan qiymatlar ajratib olinadi.

## Ishlash natijasi:
```text
60 dan yuqori ballar: 75 88 92 64
```


# 12-Topshiriq: Nomlangan vektorlar (Named Vectors)
## Topshiriq sharti:
Vektor elementlariga nom bering va nomlari bo'yicha murojaat qiling.

## Yechim (R kodi):
```r
narxlar <- c(non = 3000, sut = 8000, gosht = 95000)

print(narxlar)
cat("Sut narxi:", narxlar["sut"], "so'm\n")
cat("Barcha nomlar:", names(narxlar), "\n")
```

## Tushuntirish va Mantiq:
`names(v)` orqali vektor elementlariga kalit so'zlar biriktiriladi. Bu kodni tushunarli qilishda juda qulaydir.

## Ishlash natijasi:
```text
non   sut gosht 
 3000  8000 95000 
Sut narxi: 8000 so'm
Barcha nomlar: non sut gosht
```


# 13-Topshiriq: Yo'qolgan qiymatlar: NA (Not Available) va is.na()
## Topshiriq sharti:
Tahlil ma'lumotlaridagi yo'qolgan qiymatlarni aniqlang va ularni hisob-kitobda hisobga oling.

## Yechim (R kodi):
```r
daromadlar <- c(1200, NA, 3400, 2100, NA)

cat("NA bormi:", is.na(daromadlar), "\n")
cat("NA larning umumiy soni:", sum(is.na(daromadlar)), "\n")
cat("O'rtacha (na.rm = TRUE):", mean(daromadlar, na.rm = TRUE), "\n")
```

## Tushuntirish va Mantiq:
`NA` mavjud bo'lmagan ma'lumotni bildiradi. Agar statistik funksiyaga (mean, sum) `na.rm = TRUE` berilmasa, bitta NA butun natijani NA qilib yuboradi.

## Ishlash natijasi:
```text
NA bormi: FALSE TRUE FALSE FALSE TRUE 
NA larning umumiy soni: 2 
O'rtacha (na.rm = TRUE): 2233.333
```


# 14-Topshiriq: NaN, Inf va NULL qiymatlari
## Topshiriq sharti:
Nolga bo'lish va aniqlanmagan matematik natijalarni tekshiring.

## Yechim (R kodi):
```r
inf_son <- 10 / 0
nan_son <- 0 / 0
null_qiymat <- NULL

cat("10 / 0:", inf_son, "| is.infinite:", is.infinite(inf_son), "\n")
cat("0 / 0:", nan_son, "| is.nan:", is.nan(nan_son), "\n")
cat("is.null:", is.null(null_qiymat), "\n")
```

## Tushuntirish va Mantiq:
`Inf` cheksizlik, `NaN` son emas (Not a Number), `NULL` esa mutlaq bo'sh to'plamni bildiradi.

## Ishlash natijasi:
```text
10 / 0: Inf | is.infinite: TRUE 
0 / 0: NaN | is.nan: TRUE 
is.null: TRUE
```


# 15-Topshiriq: Tiplarni o'zgartirish (Coercion): as.numeric, as.character
## Topshiriq sharti:
Matn ko'rinishidagi raqamlarni sonli vektorga aylantiring.

## Yechim (R kodi):
```r
matn_sonlar <- c("10.5", "20.3", "30.8")
haqiqiy_sonlar <- as.numeric(matn_sonlar)

print(haqiqiy_sonlar)
cat("Yig'indisi:", sum(haqiqiy_sonlar), "\n")
```

## Tushuntirish va Mantiq:
`as.numeric()`, `as.character()`, `as.integer()` funksiyalari ma'lumotlar turini xavfsiz o'zgartiradi.

## Ishlash natijasi:
```text
[1] 10.5 20.3 30.8
Yig'indisi: 61.6
```


# 16-Topshiriq: R vektorlar va tiplar amaliyoti #16
## Topshiriq sharti:
16-vazifada R vektorlari va matematik operatsiyalarni hisoblang.

## Yechim (R kodi):
```r
v <- seq(16, 20)
natija <- sum(v * 2)
cat("Natija 16:", natija, "\n")
```

## Tushuntirish va Mantiq:
Ushbu 16-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija 16: 180
```


# 17-Topshiriq: R vektorlar va tiplar amaliyoti #17
## Topshiriq sharti:
17-vazifada R vektorlari va matematik operatsiyalarni hisoblang.

## Yechim (R kodi):
```r
v <- seq(17, 21)
natija <- sum(v * 2)
cat("Natija 17:", natija, "\n")
```

## Tushuntirish va Mantiq:
Ushbu 17-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija 17: 190
```


# 18-Topshiriq: R vektorlar va tiplar amaliyoti #18
## Topshiriq sharti:
18-vazifada R vektorlari va matematik operatsiyalarni hisoblang.

## Yechim (R kodi):
```r
v <- seq(18, 22)
natija <- sum(v * 2)
cat("Natija 18:", natija, "\n")
```

## Tushuntirish va Mantiq:
Ushbu 18-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija 18: 200
```


# 19-Topshiriq: R vektorlar va tiplar amaliyoti #19
## Topshiriq sharti:
19-vazifada R vektorlari va matematik operatsiyalarni hisoblang.

## Yechim (R kodi):
```r
v <- seq(19, 23)
natija <- sum(v * 2)
cat("Natija 19:", natija, "\n")
```

## Tushuntirish va Mantiq:
Ushbu 19-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija 19: 210
```


# 20-Topshiriq: R vektorlar va tiplar amaliyoti #20
## Topshiriq sharti:
20-vazifada R vektorlari va matematik operatsiyalarni hisoblang.

## Yechim (R kodi):
```r
v <- seq(20, 24)
natija <- sum(v * 2)
cat("Natija 20:", natija, "\n")
```

## Tushuntirish va Mantiq:
Ushbu 20-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija 20: 220
```


# 21-Topshiriq: R vektorlar va tiplar amaliyoti #21
## Topshiriq sharti:
21-vazifada R vektorlari va matematik operatsiyalarni hisoblang.

## Yechim (R kodi):
```r
v <- seq(21, 25)
natija <- sum(v * 2)
cat("Natija 21:", natija, "\n")
```

## Tushuntirish va Mantiq:
Ushbu 21-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija 21: 230
```


# 22-Topshiriq: R vektorlar va tiplar amaliyoti #22
## Topshiriq sharti:
22-vazifada R vektorlari va matematik operatsiyalarni hisoblang.

## Yechim (R kodi):
```r
v <- seq(22, 26)
natija <- sum(v * 2)
cat("Natija 22:", natija, "\n")
```

## Tushuntirish va Mantiq:
Ushbu 22-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija 22: 240
```


# 23-Topshiriq: R vektorlar va tiplar amaliyoti #23
## Topshiriq sharti:
23-vazifada R vektorlari va matematik operatsiyalarni hisoblang.

## Yechim (R kodi):
```r
v <- seq(23, 27)
natija <- sum(v * 2)
cat("Natija 23:", natija, "\n")
```

## Tushuntirish va Mantiq:
Ushbu 23-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija 23: 250
```


# 24-Topshiriq: R vektorlar va tiplar amaliyoti #24
## Topshiriq sharti:
24-vazifada R vektorlari va matematik operatsiyalarni hisoblang.

## Yechim (R kodi):
```r
v <- seq(24, 28)
natija <- sum(v * 2)
cat("Natija 24:", natija, "\n")
```

## Tushuntirish va Mantiq:
Ushbu 24-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija 24: 260
```


# 25-Topshiriq: R vektorlar va tiplar amaliyoti #25
## Topshiriq sharti:
25-vazifada R vektorlari va matematik operatsiyalarni hisoblang.

## Yechim (R kodi):
```r
v <- seq(25, 29)
natija <- sum(v * 2)
cat("Natija 25:", natija, "\n")
```

## Tushuntirish va Mantiq:
Ushbu 25-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija 25: 270
```


# 26-Topshiriq: R vektorlar va tiplar amaliyoti #26
## Topshiriq sharti:
26-vazifada R vektorlari va matematik operatsiyalarni hisoblang.

## Yechim (R kodi):
```r
v <- seq(26, 30)
natija <- sum(v * 2)
cat("Natija 26:", natija, "\n")
```

## Tushuntirish va Mantiq:
Ushbu 26-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija 26: 280
```


# 27-Topshiriq: R vektorlar va tiplar amaliyoti #27
## Topshiriq sharti:
27-vazifada R vektorlari va matematik operatsiyalarni hisoblang.

## Yechim (R kodi):
```r
v <- seq(27, 31)
natija <- sum(v * 2)
cat("Natija 27:", natija, "\n")
```

## Tushuntirish va Mantiq:
Ushbu 27-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija 27: 290
```


# 28-Topshiriq: R vektorlar va tiplar amaliyoti #28
## Topshiriq sharti:
28-vazifada R vektorlari va matematik operatsiyalarni hisoblang.

## Yechim (R kodi):
```r
v <- seq(28, 32)
natija <- sum(v * 2)
cat("Natija 28:", natija, "\n")
```

## Tushuntirish va Mantiq:
Ushbu 28-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija 28: 300
```


# 29-Topshiriq: R vektorlar va tiplar amaliyoti #29
## Topshiriq sharti:
29-vazifada R vektorlari va matematik operatsiyalarni hisoblang.

## Yechim (R kodi):
```r
v <- seq(29, 33)
natija <- sum(v * 2)
cat("Natija 29:", natija, "\n")
```

## Tushuntirish va Mantiq:
Ushbu 29-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija 29: 310
```


# 30-Topshiriq: R vektorlar va tiplar amaliyoti #30
## Topshiriq sharti:
30-vazifada R vektorlari va matematik operatsiyalarni hisoblang.

## Yechim (R kodi):
```r
v <- seq(30, 34)
natija <- sum(v * 2)
cat("Natija 30:", natija, "\n")
```

## Tushuntirish va Mantiq:
Ushbu 30-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija 30: 320
```


# 31-Topshiriq: R vektorlar va tiplar amaliyoti #31
## Topshiriq sharti:
31-vazifada R vektorlari va matematik operatsiyalarni hisoblang.

## Yechim (R kodi):
```r
v <- seq(31, 35)
natija <- sum(v * 2)
cat("Natija 31:", natija, "\n")
```

## Tushuntirish va Mantiq:
Ushbu 31-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija 31: 330
```


# 32-Topshiriq: R vektorlar va tiplar amaliyoti #32
## Topshiriq sharti:
32-vazifada R vektorlari va matematik operatsiyalarni hisoblang.

## Yechim (R kodi):
```r
v <- seq(32, 36)
natija <- sum(v * 2)
cat("Natija 32:", natija, "\n")
```

## Tushuntirish va Mantiq:
Ushbu 32-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija 32: 340
```


# 33-Topshiriq: R vektorlar va tiplar amaliyoti #33
## Topshiriq sharti:
33-vazifada R vektorlari va matematik operatsiyalarni hisoblang.

## Yechim (R kodi):
```r
v <- seq(33, 37)
natija <- sum(v * 2)
cat("Natija 33:", natija, "\n")
```

## Tushuntirish va Mantiq:
Ushbu 33-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija 33: 350
```


# 34-Topshiriq: R vektorlar va tiplar amaliyoti #34
## Topshiriq sharti:
34-vazifada R vektorlari va matematik operatsiyalarni hisoblang.

## Yechim (R kodi):
```r
v <- seq(34, 38)
natija <- sum(v * 2)
cat("Natija 34:", natija, "\n")
```

## Tushuntirish va Mantiq:
Ushbu 34-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija 34: 360
```


# 35-Topshiriq: R vektorlar va tiplar amaliyoti #35
## Topshiriq sharti:
35-vazifada R vektorlari va matematik operatsiyalarni hisoblang.

## Yechim (R kodi):
```r
v <- seq(35, 39)
natija <- sum(v * 2)
cat("Natija 35:", natija, "\n")
```

## Tushuntirish va Mantiq:
Ushbu 35-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija 35: 370
```


# 36-Topshiriq: R vektorlar va tiplar amaliyoti #36
## Topshiriq sharti:
36-vazifada R vektorlari va matematik operatsiyalarni hisoblang.

## Yechim (R kodi):
```r
v <- seq(36, 40)
natija <- sum(v * 2)
cat("Natija 36:", natija, "\n")
```

## Tushuntirish va Mantiq:
Ushbu 36-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija 36: 380
```


# 37-Topshiriq: R vektorlar va tiplar amaliyoti #37
## Topshiriq sharti:
37-vazifada R vektorlari va matematik operatsiyalarni hisoblang.

## Yechim (R kodi):
```r
v <- seq(37, 41)
natija <- sum(v * 2)
cat("Natija 37:", natija, "\n")
```

## Tushuntirish va Mantiq:
Ushbu 37-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija 37: 390
```


# 38-Topshiriq: R vektorlar va tiplar amaliyoti #38
## Topshiriq sharti:
38-vazifada R vektorlari va matematik operatsiyalarni hisoblang.

## Yechim (R kodi):
```r
v <- seq(38, 42)
natija <- sum(v * 2)
cat("Natija 38:", natija, "\n")
```

## Tushuntirish va Mantiq:
Ushbu 38-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija 38: 400
```


# 39-Topshiriq: R vektorlar va tiplar amaliyoti #39
## Topshiriq sharti:
39-vazifada R vektorlari va matematik operatsiyalarni hisoblang.

## Yechim (R kodi):
```r
v <- seq(39, 43)
natija <- sum(v * 2)
cat("Natija 39:", natija, "\n")
```

## Tushuntirish va Mantiq:
Ushbu 39-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija 39: 410
```


# 40-Topshiriq: R vektorlar va tiplar amaliyoti #40
## Topshiriq sharti:
40-vazifada R vektorlari va matematik operatsiyalarni hisoblang.

## Yechim (R kodi):
```r
v <- seq(40, 44)
natija <- sum(v * 2)
cat("Natija 40:", natija, "\n")
```

## Tushuntirish va Mantiq:
Ushbu 40-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija 40: 420
```


# 41-Topshiriq: R vektorlar va tiplar amaliyoti #41
## Topshiriq sharti:
41-vazifada R vektorlari va matematik operatsiyalarni hisoblang.

## Yechim (R kodi):
```r
v <- seq(41, 45)
natija <- sum(v * 2)
cat("Natija 41:", natija, "\n")
```

## Tushuntirish va Mantiq:
Ushbu 41-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija 41: 430
```


# 42-Topshiriq: R vektorlar va tiplar amaliyoti #42
## Topshiriq sharti:
42-vazifada R vektorlari va matematik operatsiyalarni hisoblang.

## Yechim (R kodi):
```r
v <- seq(42, 46)
natija <- sum(v * 2)
cat("Natija 42:", natija, "\n")
```

## Tushuntirish va Mantiq:
Ushbu 42-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija 42: 440
```


# 43-Topshiriq: R vektorlar va tiplar amaliyoti #43
## Topshiriq sharti:
43-vazifada R vektorlari va matematik operatsiyalarni hisoblang.

## Yechim (R kodi):
```r
v <- seq(43, 47)
natija <- sum(v * 2)
cat("Natija 43:", natija, "\n")
```

## Tushuntirish va Mantiq:
Ushbu 43-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija 43: 450
```


# 44-Topshiriq: R vektorlar va tiplar amaliyoti #44
## Topshiriq sharti:
44-vazifada R vektorlari va matematik operatsiyalarni hisoblang.

## Yechim (R kodi):
```r
v <- seq(44, 48)
natija <- sum(v * 2)
cat("Natija 44:", natija, "\n")
```

## Tushuntirish va Mantiq:
Ushbu 44-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija 44: 460
```


# 45-Topshiriq: R vektorlar va tiplar amaliyoti #45
## Topshiriq sharti:
45-vazifada R vektorlari va matematik operatsiyalarni hisoblang.

## Yechim (R kodi):
```r
v <- seq(45, 49)
natija <- sum(v * 2)
cat("Natija 45:", natija, "\n")
```

## Tushuntirish va Mantiq:
Ushbu 45-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija 45: 470
```


# 46-Topshiriq: R vektorlar va tiplar amaliyoti #46
## Topshiriq sharti:
46-vazifada R vektorlari va matematik operatsiyalarni hisoblang.

## Yechim (R kodi):
```r
v <- seq(46, 50)
natija <- sum(v * 2)
cat("Natija 46:", natija, "\n")
```

## Tushuntirish va Mantiq:
Ushbu 46-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija 46: 480
```


# 47-Topshiriq: R vektorlar va tiplar amaliyoti #47
## Topshiriq sharti:
47-vazifada R vektorlari va matematik operatsiyalarni hisoblang.

## Yechim (R kodi):
```r
v <- seq(47, 51)
natija <- sum(v * 2)
cat("Natija 47:", natija, "\n")
```

## Tushuntirish va Mantiq:
Ushbu 47-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija 47: 490
```


# 48-Topshiriq: R vektorlar va tiplar amaliyoti #48
## Topshiriq sharti:
48-vazifada R vektorlari va matematik operatsiyalarni hisoblang.

## Yechim (R kodi):
```r
v <- seq(48, 52)
natija <- sum(v * 2)
cat("Natija 48:", natija, "\n")
```

## Tushuntirish va Mantiq:
Ushbu 48-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija 48: 500
```


# 49-Topshiriq: R vektorlar va tiplar amaliyoti #49
## Topshiriq sharti:
49-vazifada R vektorlari va matematik operatsiyalarni hisoblang.

## Yechim (R kodi):
```r
v <- seq(49, 53)
natija <- sum(v * 2)
cat("Natija 49:", natija, "\n")
```

## Tushuntirish va Mantiq:
Ushbu 49-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija 49: 510
```


# 50-Topshiriq: R vektorlar va tiplar amaliyoti #50
## Topshiriq sharti:
50-vazifada R vektorlari va matematik operatsiyalarni hisoblang.

## Yechim (R kodi):
```r
v <- seq(50, 54)
natija <- sum(v * 2)
cat("Natija 50:", natija, "\n")
```

## Tushuntirish va Mantiq:
Ushbu 50-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.

## Ishlash natijasi:
```text
Natija 50: 520
```

