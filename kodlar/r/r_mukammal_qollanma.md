# R Tili: Mukammal Ensiklopediya va Fundamental Ilmiy Dasturlash Qo'llanmasi
**Loyiha:** Khorazmiy AI — O'zbek Tilidagi Katta Dasturlash Dataseti  
**Muallif:** Khorazmiy AI R Dataset Specialist  
**Versiya:** R 4.3 / 4.4+ (Tidyverse 2.0, data.table, Rcpp, Shiny, Quarto)  
**Qamrovi:** R tili falsafasi va S merosi, Vektorlashtirilgan hisoblashlar, S3/S4/R6 obyekt modellari, Tidyverse va data.table orqali Katta ma'lumotlar manipulyatsiyasi, "Grammar of Graphics" (ggplot2), Matematik va Ekonometrik modellashtirish, Bioconductor va Genomika, Reaktiv Shiny ilovalari hamda Ilmiy AI agentlar integratsiyasi.

---

## Mundarija
1. [R Tili Tarixi, Falsafasi va Ilmiy Ekologiyasi](#1-r-tili-tarixi-falsafasi-va-ilmiy-ekologiyasi)
2. [R Arxitekturasi, Xotira Modeli va Vektorlashtirish](#2-r-arxitekturasi-xotira-modeli-va-vektorlashtirish)
3. [Obyektga Yo'naltirilgan Dasturlash Tizimlari (S3, S4, R6 va S7)](#3-obyektga-yonaltirilgan-dasturlash-tizimlari-s3-s4-r6-va-s7)
4. [Tidyverse Falsafasi va Toza Ma'lumotlar (Tidy Data)](#4-tidyverse-falsafasi-va-toza-malumotlar-tidy-data)
5. [data.table: Gigabaytlab Ma'lumotlarni Millisekundlarda Tahlil Qilish](#5-datatable-gigabaytlab-malumotlarni-millisekundlarda-tahlil-qilish)
6. [Vizualizatsiya San'ati: "Grammar of Graphics" va ggplot2](#6-vizualizatsiya-sanati-grammar-of-graphics-va-ggplot2)
7. [Statistika, Gipotezalar va Ekonometrik Modellashtirish](#7-statistika-gipotezalar-va-ekonometrik-modellashtirish)
8. [Bioinformatika, Genomika va Bioconductor](#8-bioinformatika-genomika-va-bioconductor)
9. [Interaktiv Veb Panellar: Reaktiv Shiny Arxitekturasi](#9-interaktiv-veb-panellar-reaktiv-shiny-arxitekturasi)
10. [Yuqori Unumdorlik: Rcpp, Parallel Hisob-kitoblar va AI](#10-yuqori-unumdorlik-rcpp-parallel-hisob-kitoblar-va-ai)

---

## 1. R Tili Tarixi, Falsafasi va Ilmiy Ekologiyasi

R tili 1993-yilda Oklend universitetida Ross Ihaka va Robert Gentleman tomonidan yaratilgan. U 1976-yilda Bell Labs laboratoriyasida Jon Chambers boshchiligida ishlab chiqilgan mashhur **S** tili asosiga qurilgan.

### 1.1. R ning Missiyasi
Dasturlash tillarining aksariyati dasturiy injiniring uchun yaratilgan bo'lsa, R maxsus **ma'lumotlar bilan muloqot qilish, statistik xulosa chiqarish va ilmiy kashfiyotlar qilish** uchun maxsus loyihalashtirilgan.

### 1.2. CRAN va Global Ekotizim
**CRAN (Comprehensive R Archive Network)** dunyodagi eng qat'iy tekshiriladigan paketlar repozitoriylaridan biridir. Unda 20 000 dan ortiq ilmiy paketlar mavjud bo'lib, har bir paket bir nechta operatsion tizimlarda avtomatik tekshiruvdan o'tkaziladi.

---

## 2. R Arxitekturasi, Xotira Modeli va Vektorlashtirish

R interpretator sifatida ishlaydi, ammo uning chuqur matematik yadrolari C va Fortran tillarida yozilgan BLAS (Basic Linear Algebra Subprograms) va LAPACK kutubxonalariga tayanadi.

### 2.1. Copy-on-Modify (Nusxalash va O'zgartirish)
R-da obyektlar qiymat semantikasiga ega. Agar siz o'zgaruvchini boshqasiga biriktirsangiz:
```r
x <- c(1, 2, 3)
y <- x
```
Ular xotiradagi bitta manzilga qarab turadi. Faqat `y[1] <- 10` qilib bitta elementi o'zgartirilganda R yangi xotira ajratadi (Copy-on-Modify).

### 2.2. Vektorlashtirish (Vectorization) Sehri
R-da `for` sikllari nisbatan sekinroq, chunki har bir iteratsiyada dinamik tip tekshiruvi amalga oshiriladi. Shu sababli R vektorli amallarni to'g'ridan-to'g'ri C darajasida SIMD (Single Instruction Multiple Data) ko'rsatmalari bilan hisoblaydi:
```r
# Sekin usul (For loop):
# for(i in 1:length(x)) res[i] <- x[i] * 2

# Tezkor va tabiiy R usuli (Vectorized):
res <- x * 2
```

---

## 3. Obyektga Yo'naltirilgan Dasturlash Tizimlari (S3, S4, R6 va S7)

R-dagi OOP dunyosi juda o'ziga xos bo'lib, bir necha tizimlarni o'z ichiga oladi:

### 3.1. S3 Tizimi (Informal & Generic-Function OO)
R-dagi eng sodda va eng ko'p ishlatiladigan tizim. Unda klasslar rasmiy deklaratsiya qilinmaydi, faqat obyektga `class` atributi biriktiriladi:
```r
mashina <- list(model = "Tesla", tezlik = 250)
class(mashina) <- "Avtomobil"
```
Umumiy funksiyalar (`print`, `summary`, `plot`) chaqirilganda `UseMethod()` mexanizmi ishga tushadi va `print.Avtomobil` metodini topib bajaradi.

### 3.2. S4 va R6
- **S4:** Qat'iy tiplash, formal sinf ta'rifi (`setClass`), Bioconductor loyihasida genetik ma'lumotlarni xatosiz boshqarishda standart hisoblanadi.
- **R6:** Ommabop tillar (Java, Python, C++) kabi inkapsulyatsiyalangan, malumotlarni joyida o'zgartiruvchi (reference semantics) klasslar tizimi. Shiny va API mijozlari yaratishda keng qo'llaniladi.

---

## 4. Tidyverse Falsafasi va Toza Ma'lumotlar (Tidy Data)

Hadley Wickham boshchiligida yaratilgan **Tidyverse** zamonaviy ma'lumotlar fanining (Data Science) global standartiga aylandi.

### 4.1. "Tidy Data" Uch Qoidasi:
1. Har bir o'zgaruvchi (variable) o'z ustuniga ega bo'lishi kerak.
2. Har bir kuzatuv (observation) o'z qatoriga ega bo'lishi kerak.
3. Har bir qiymat (value) o'z katagiga ega bo'lishi kerak.

### 4.2. Pipe Operatorlari (`%>%` va `|>`)
R 4.1 versiyasida mahalliy pipe `|>` qo'shildi. Pipe kodni ichma-ich qavslardan xalos etib, inson o'qishiga mos zanjirga aylantiradi:
```r
mahsulotlar |>
  filter(narx > 100) |>
  group_by(kategoriya) |>
  summarise(ortacha_sotuv = mean(sotuv))
```

---

## 5. data.table: Gigabaytlab Ma'lumotlarni Millisekundlarda Tahlil Qilish

Katta hajmdagi ma'lumotlar (Big Data) bilan ishlashda Matt Dowle tomonidan yaratilgan `data.table` paketi dunyoda eng tezkor tahlil vositasi hisoblanadi.
- Sintaksisi: `DT[i, j, by]`
  - `i`: qatorlarni filtrlash
  - `j`: ustunlar ustida hisoblashlar bajarish
  - `by`: guruhlash
- `:=` operatori yordamida ustunlarni xotirada nusxa ko'chirmasdan (in-place) yangilash orqali RAMdan maksimal tejamkor foydalanadi.

---

## 6. Vizualizatsiya San'ati: "Grammar of Graphics" va ggplot2

Leland Wilkinsonning ilmiy asari asosida yaratilgan `ggplot2` grafik chizishga yangicha yondashuv olib keldi. Har qanday grafik qatlamlardan (Layers) tashkil topadi:

```
[Mavzular (Theme): Shriftlar, Fon, Ranglar]
             ▲
[Koordinatalar (Coordinates): Dekart, Polar, Xarita]
             ▲
[Fasetlar (Facets): Ko'p panelli grafiklar]
             ▲
[Geometriyalar (Geometries): Nuqta, Chiziq, Ustun]
             ▲
[Estetika (Aesthetics): X, Y, Rang, Shakl, Hajm]
             ▲
[Ma'lumotlar (Data): Tidy Data Frame]
```

Ushbu qatlamli mantiq orqali murakkab ilmiy va biznes infografikalarni bir necha qatorda yaratish mumkin.

---

## 7. Statistika, Gipotezalar va Ekonometrik Modellashtirish

R statistika fanining rasmiy tilidir.
- **Parametrik va noparametrik testlar:** t-test, U-testi (Wilcoxon), ANOVA, Kruskal-Wallis, Chi-kvadrat.
- **Regressiya tahlili:** `lm()` orqali OLS (Oddiy eng kichik kvadratlar), `glm()` orqali logistik va Puasson regressiyalari.
- **Ekonometrika:** Ko'p omilli regressiyalarda multikollinearlik (VIF), geteroskedastiklik (Breusch-Pagan) va avtokorrelyatsiya (Durbin-Watson) testlari.
- **Vaqt qatorlari:** ARIMA, SARIMA, GARCH va Holt-Winters eksponentsial tekislash orqali bozor va makroiqtisodiy prognozlar.

---

## 8. Bioinformatika, Genomika va Bioconductor

R biotibbiyot va genomik tadqiqotlar bo'yicha dunyoda 1-o'rinda turadi. **Bioconductor** loyihasi:
- DNK, RNK ketma-ketliklari (Next-Generation Sequencing - NGS)
- Differensial gen ifodasi (DESeq2, edgeR)
- Yagona hujayrali transkriptomika (Single-cell RNA-seq / Seurat)
- Vulqon grafigi (Volcano Plot) va klasterlangan issiqlik xaritalari (ComplexHeatmap).

---

## 9. Interaktiv Veb Panellar: Reaktiv Shiny Arxitekturasi

R Shiny yordamida ma'lumotlar bo'yicha tahlilchilar HTML, CSS yoki JavaScript yozmasdan to'liq interaktiv veb-ilovalar yaratishi mumkin.
- **Reaktiv graf (Reactive Graph):** Foydalanuvchi slayderni surishi bilan faqat unga bog'liq bo'lgan hisob-kitoblar qayta bajariladi.
- Boshqaruv panellari (Dashboards), klinik tadqiqotlar natijalarini ko'rsatish va korporativ analitika tizimlari yaratish.

---

## 10. Yuqori Unumdorlik: Rcpp, Parallel Hisob-kitoblar va AI

R faqat statistik hisob-kitoblar bilan cheklanmaydi:
- **Rcpp (Dirk Eddelbuettel):** C++ kodini R ichida to'g'ridan-to'g'ri chaqirish orqali hisoblash tezligini 100-500 baravargacha oshirish.
- **Parallel hisoblashlar:** `future` va `parallel` paketlari orqali ko'p yadroli CPU klasterlaridan to'liq foydalanish.
- **AI va Katta Til Modellari:** R skriptlaridan OpenAI, Gemini, Claude API-lariga to'g'ridan-to'g'ri murojaat qilish, statistik hisobotlarni sun'iy intellekt orqali avtomatik sharhlash va prognoz agentlarini yaratish.

Ushbu 1000 ta topshiriqdan iborat mukammal amaliy to'plam sizni R tili asoslaridan boshlab ilmiy tadqiqotlar, biotibbiyot, ekonometrika va sun'iy intellekt muhandisligigacha olib boradi.
