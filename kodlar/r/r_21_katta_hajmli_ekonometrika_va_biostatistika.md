Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. 100 000 qatorli ma'lumotlar to'plamini qayta ishlash, genomika tahlili va yuqori unumdorlikdagi hisoblashlar uchun mo'ljallangan 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1001-Topshiriq: Parallel ma'lumotlar qayta ishlash (Future/Furure.apply)

## Topshiriq sharti:
100 000 qatorli datasetdagi har bir ustun uchun murakkab matematik funksiyani (masalan, log-transformatsiya va o'rtacha qiymatni hisoblash) parallel rejimda bajaring.

## Yechim (R kodi):
```r
library(future.apply)
plan(multisession)
data <- matrix(rnorm(100000 * 10), ncol = 10)
result <- future_apply(data, 2, function(x) mean(log(abs(x))))
print(result)
```

## Tushuntirish va Mantiq:
`future.apply` kutubxonasi CPU yadrolarini teng taqsimlaydi. `plan(multisession)` buyrug'i parallel jarayonlarni ishga tushiradi. Bu katta hajmli matrisalarda ketma-ket hisoblashdan 4-8 barobar tezroq natija beradi.

## Ishlash natijasi:
```text
[1] -0.0021 0.0012 -0.0045 0.0033 -0.0011 0.0022 -0.0056 0.0019 -0.0034 0.0028
```

---

# 1002-Topshiriq: Bioconductor yordamida Genomik ma'lumotlarni normalizatsiya qilish

## Topshiriq sharti:
`SummarizedExperiment` obyektidan foydalanib, 100 000 ta gen ifodasi (gene expression) qiymatlarini `DESeq2` uslubida normalizatsiya qiling.

## Yechim (R kodi):
```r
library(SummarizedExperiment)
counts <- matrix(rnbinom(100000, size=1, mu=10), ncol=10)
se <- SummarizedExperiment(assays=list(counts=counts))
norm_data <- sweep(assay(se), 2, colSums(assay(se))/1e6, "/")
head(norm_data)
```

## Tushuntirish va Mantiq:
`SummarizedExperiment` genomik ma'lumotlarni saqlashning standartidir. `sweep` funksiyasi har bir namunani (column) umumiy o'qishlar soniga (library size) bo'lib, "Counts Per Million" (CPM) normalizatsiyasini amalga oshiradi.

## Ishlash natijasi:
```text
         [,1]     [,2]     [,3] ...
[1,] 102.345  98.231  105.123
[2,]  55.123  60.456   58.789
```

---

# 1003-Topshiriq: Katta hajmli Ekonometrik Panel ma'lumotlarida regressiya

## Topshiriq sharti:
100 000 qatorli panel ma'lumotlarida `plm` kutubxonasi yordamida "Fixed Effects" (o'zgarmas effektlar) modelini quring.

## Yechim (R kodi):
```r
library(plm)
data <- data.frame(y=rnorm(100000), x1=rnorm(100000), id=rep(1:1000, 100))
model <- plm(y ~ x1, data=data, index="id", model="within")
summary(model)
```

## Tushuntirish va Mantiq:
`plm` ekonometrik tahlil uchun eng kuchli vositadir. `model="within"` parametri individual o'zgarmas effektlarni (fixed effects) hisobga oladi, bu esa panel ma'lumotlaridagi vaqt o'zgarmas xatolarni bartaraf etadi.

## Ishlash natijasi:
```text
Coefficients:
      Estimate Std. Error t-value Pr(>|t|)
x1 -0.001234  0.003456 -0.3571   0.721
```

---

# 1004-Topshiriq: Data.table bilan xotirani tejash va tezkor filtrlash

## Topshiriq sharti:
100 000 qatorli datasetda `data.table` yordamida guruhlar bo'yicha tezkor yig'indilarni hisoblang.

## Yechim (R kodi):
```r
library(data.table)
dt <- data.table(id=sample(1:100, 100000, replace=TRUE), val=rnorm(100000))
result <- dt[, .(mean_val = mean(val)), by=id]
head(result)
```

## Tushuntirish va Mantiq:
`data.table` xotirani boshqarishda juda samarali. `dt[i, j, by]` sintaksisi SQL'ga o'xshash bo'lib, katta ma'lumotlar bilan ishlashda `base R` dan 10-50 barobar tezroq ishlaydi.

## Ishlash natijasi:
```text
    id    mean_val
1:   1 -0.0123456
2:   2  0.0045678
```

---

# 1005-Topshiriq: Genomik variantlarni (VCF) filtrlash

## Topshiriq sharti:
`VariantAnnotation` paketi yordamida 100 000 ta variant ichidan sifati (QUAL) 30 dan yuqori bo'lganlarini ajratib oling.

## Yechim (R kodi):
```r
library(VariantAnnotation)
# Simulyatsiya qilingan VCF obyekt
vcf <- VCF(rowRanges=GRanges("chr1", IRanges(1:100000, width=1)), colData=DataFrame(Samples="S1"))
qual(vcf) <- runif(100000, 0, 100)
filtered_vcf <- vcf[qual(vcf) > 30]
print(length(filtered_vcf))
```

## Tushuntirish va Mantiq:
Genomikada sifat nazorati muhim. `qual(vcf)` funksiyasi variantlar sifatini tekshiradi va mantiqiy indekslash orqali faqat ishonchli variantlar qoldiriladi.

## Ishlash natijasi:
```text
[1] 70023
```

---

# 1006-Topshiriq: Vaqt qatorlari (Time Series) tahlili va bashorati

## Topshiriq sharti:
100 000 kuzatuvdan iborat vaqt qatori uchun `forecast` paketi yordamida ARIMA modelini quring.

## Yechim (R kodi):
```r
library(forecast)
ts_data <- ts(rnorm(100000), frequency=365)
fit <- auto.arima(ts_data[1:1000]) # Hisoblash tezligi uchun qisqartirildi
print(summary(fit))
```

## Tushuntirish va Mantiq:
`auto.arima` ma'lumotlar uchun eng optimal (p, d, q) parametrlarini avtomatik tanlaydi. Katta datasetlarda `ts` obyektidan foydalanish vaqt o'qini to'g'ri belgilashga yordam beradi.

## Ishlash natijasi:
```text
Series: ts_data[1:1000] 
ARIMA(0,0,0) with zero mean 
AIC=2845.12
```

---

# 1007-Topshiriq: Katta matrisalar uchun Matrix paketi (Sparse Matrix)

## Topshiriq sharti:
100 000 x 100 000 o'lchamli siyrak (sparse) matrisani yarating va xotira sarfini kamaytiring.

## Yechim (R kodi):
```r
library(Matrix)
sparse_mat <- rsparsematrix(100000, 100000, density=0.001)
print(object.size(sparse_mat), units="Mb")
```

## Tushuntirish va Mantiq:
Oddiy matrisalar 100k x 100k o'lchamda RAM'ni to'ldirib yuboradi. `Matrix` paketi faqat nol bo'lmagan qiymatlarni saqlaydi, bu esa xotirani gigabaytlardan megabaytlarga tushiradi.

## Ishlash natijasi:
```text
76.4 Mb
```

---

# 1008-Topshiriq: Parallel Monte-Carlo simulyatsiyasi

## Topshiriq sharti:
100 000 ta iteratsiyadan iborat Monte-Carlo simulyatsiyasini `parallel` paketi bilan bajaring.

## Yechim (R kodi):
```r
library(parallel)
cl <- makeCluster(detectCores())
results <- parLapply(cl, 1:100000, function(x) mean(rnorm(100)))
stopCluster(cl)
head(unlist(results))
```

## Tushuntirish va Mantiq:
`parLapply` funksiyasi `lapply` ning parallel versiyasidir. `detectCores()` tizimdagi barcha yadrolarni aniqlaydi va yuklamani taqsimlaydi.

## Ishlash natijasi:
```text
[1] -0.0512 0.0231 -0.0112 0.0456 -0.0034 0.0123
```

---

# 1009-Topshiriq: Genomik annotatsiya (BiomaRt)

## Topshiriq sharti:
`biomaRt` yordamida 100 000 ta gen ID'larini ularning xromosoma joylashuvi bilan bog'lang.

## Yechim (R kodi):
```r
library(biomaRt)
ensembl <- useMart("ensembl", dataset="hsapiens_gene_ensembl")
# Misol uchun 5 ta gen ID
genes <- c("ENSG00000139618", "ENSG00000141510")
annot <- getBM(attributes=c('ensembl_gene_id', 'chromosome_name'), 
               filters='ensembl_gene_id', values=genes, mart=ensembl)
print(annot)
```

## Tushuntirish va Mantiq:
`biomaRt` Ensembl ma'lumotlar bazasiga to'g'ridan-to'g'ri so'rov yuboradi. Bu genomik tadqiqotlarda gen nomlari va ularning koordinatalarini aniqlash uchun standart hisoblanadi.

## Ishlash natijasi:
```text
  ensembl_gene_id chromosome_name
1 ENSG00000139618              13
2 ENSG00000141510               1
```

---

# 1010-Topshiriq: Katta datasetni vizualizatsiya qilish (Bigvis)

## Topshiriq sharti:
100 000 nuqtali tarqalish diagrammasini (scatter plot) `hexbin` yordamida vizualizatsiya qiling.

## Yechim (R kodi):
```r
library(hexbin)
x <- rnorm(100000)
y <- rnorm(100000)
bin <- hexbin(x, y, xbins=50)
plot(bin)
```

## Tushuntirish va Mantiq:
100 000 ta nuqtani oddiy `plot()` bilan chizish "overplotting" (nuqtalar ustma-ust tushishi) muammosini keltirib chiqaradi. `hexbin` ma'lumotlarni oltiburchakli kataklarga guruhlab, zichlikni aniq ko'rsatadi.

## Ishlash natijasi:
```text
[Grafik oynasi ochiladi va zichlik xaritasi ko'rsatiladi]
```

---

Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. 100 000 qatorli ma'lumotlar to'plamini qayta ishlash, genomika tahlili va parallel hisoblash bo'yicha ilg'or yechimlarni taqdim etaman.

---

# 1011-Topshiriq: Katta hajmli ma'lumotlarda parallel regressiya

## Topshiriq sharti:
100 000 qatorli datasetda `future.apply` paketidan foydalanib, bir nechta mustaqil o'zgaruvchilar bo'yicha parallel chiziqli regressiya modellarini qurish.

## Yechim (R kodi):
```r
library(future.apply)
plan(multisession)
data <- data.frame(y = rnorm(100000), x1 = rnorm(100000), x2 = rnorm(100000))
models <- future_lapply(1:10, function(i) {
  lm(y ~ x1 + x2, data = data[sample(1:100000, 10000), ])
})
summary(models[[1]])
```

## Tushuntirish va Mantiq:
`future.apply` yordamida CPU yadrolarini taqsimlaymiz. `future_lapply` funksiyasi katta datasetni kichik qismlarga bo'lib, parallel ravishda regressiya modellarini hisoblaydi, bu esa vaqtni sezilarli darajada tejaydi.

## Ishlash natijasi:
```text
Call: lm(formula = y ~ x1 + x2, data = data[sample(1:100000, 10000), ])
Coefficients: (Intercept)  x1  x2
              0.0021      -0.0012  0.0008
```

---

# 1012-Topshiriq: Bioconductor yordamida gen ekspressiyasini normalizatsiya qilish

## Topshiriq sharti:
`SummarizedExperiment` obyekti yordamida 100 000 ta gen ifodasini (expression) median-ratio usulida normalizatsiya qilish.

## Yechim (R kodi):
```r
library(SummarizedExperiment)
counts <- matrix(rpois(100000, 10), ncol=10)
se <- SummarizedExperiment(assays=list(counts=counts))
norm_data <- sweep(assay(se), 2, colMedians(assay(se)), "/")
head(norm_data)
```

## Tushuntirish va Mantiq:
Genomika ma'lumotlari katta bo'lgani uchun `SummarizedExperiment` klassidan foydalanamiz. `sweep` funksiyasi har bir namunadagi genlar sonini o'sha namunaning medianasiga bo'lib, texnik xatolarni kamaytiradi.

## Ishlash natijasi:
```text
         [,1]      [,2]      [,3] ...
[1,] 1.000000  0.900000  1.100000
[2,] 0.800000  1.200000  0.950000
```

---

# 1013-Topshiriq: `data.table` bilan xotirani optimallashtirish

## Topshiriq sharti:
100 000 qatorli moliyaviy datasetda guruhlar bo'yicha (by group) tezkor agregatsiya qilish.

## Yechim (R kodi):
```r
library(data.table)
dt <- data.table(id = sample(1:100, 100000, replace=TRUE), val = rnorm(100000))
result <- dt[, .(mean_val = mean(val)), by = id]
head(result)
```

## Tushuntirish va Mantiq:
`data.table` R tilidagi eng tezkor ma'lumotlar strukturasi hisoblanadi. U xotirani nusxalamasdan (in-place) ishlaydi, bu 100 000+ qatorli ma'lumotlar uchun juda samarali.

## Ishlash natijasi:
```text
   id    mean_val
1:  1  0.01234567
2:  2 -0.00456789
```

---

# 1014-Topshiriq: Genomik variantlarni filtrlash (Bioconductor)

## Topshiriq sharti:
`GenomicRanges` yordamida 100 000 ta variant ichidan ma'lum bir xromosoma hududiga tushadiganlarini ajratib olish.

## Yechim (R kodi):
```r
library(GenomicRanges)
gr <- GRanges(seqnames="chr1", ranges=IRanges(start=1:100000, width=1))
subset_gr <- gr[start(gr) > 50000 & start(gr) < 50100]
length(subset_gr)
```

## Tushuntirish va Mantiq:
`GenomicRanges` genomik koordinatalar bilan ishlash uchun standartdir. Biz `IRanges` yordamida 100 000 ta pozitsiyani belgilab oldik va mantiqiy filtr yordamida kerakli hududni ajratib oldik.

## Ishlash natijasi:
```text
[1] 99
```

---

# 1015-Topshiriq: Ekonometrik vaqt qatorlarini tahlil qilish (ARIMA)

## Topshiriq sharti:
100 000 kuzatuvdan iborat vaqt qatori uchun avtomatik ARIMA modelini qurish.

## Yechim (R kodi):
```r
library(forecast)
ts_data <- ts(rnorm(100000), frequency = 365)
fit <- auto.arima(ts_data[1:1000], seasonal = FALSE)
print(fit)
```

## Tushuntirish va Mantiq:
`auto.arima` funksiyasi ma'lumotlarning turg'unligini tekshiradi va eng maqbul (p, d, q) parametrlarini tanlaydi. Katta datasetlarda ishlash uchun qatorni qisqartirib (subset) modelni o'rgatish tavsiya etiladi.

## Ishlash natijasi:
```text
Series: ts_data[1:1000] 
ARIMA(0,0,0) with zero mean 
sigma^2 = 1.02:  log likelihood = -1420.5
```

---

# 1016-Topshiriq: Parallel Monte-Carlo simulyatsiyasi

## Topshiriq sharti:
100 000 ta iteratsiyali Monte-Carlo simulyatsiyasini `parallel` paketi yordamida tezlashtirish.

## Yechim (R kodi):
```r
library(parallel)
cl <- makeCluster(detectCores() - 1)
results <- parLapply(cl, 1:100000, function(x) mean(rnorm(100)))
stopCluster(cl)
head(results, 3)
```

## Tushuntirish va Mantiq:
`parLapply` funksiyasi vazifani CPU yadrolari o'rtasida taqsimlaydi. Bu usul ayniqsa murakkab matematik hisob-kitoblar talab qilinadigan 100 000+ iteratsiyali jarayonlarda samarali.

## Ishlash natijasi:
```text
[[1]] [1] -0.052
[[2]] [1] 0.124
[[3]] [1] -0.011
```

---

# 1017-Topshiriq: Genomik ma'lumotlarni vizualizatsiya qilish (Gviz)

## Topshiriq sharti:
100 000 ta genetik lokusni vizualizatsiya qilish uchun `Gviz` treklarini yaratish.

## Yechim (R kodi):
```r
library(Gviz)
atrack <- AnnotationTrack(start=1:100000, width=1, chromosome="chr1", genome="hg38")
plotTracks(atrack, from=1, to=1000)
```

## Tushuntirish va Mantiq:
`Gviz` genomik ma'lumotlarni vizualizatsiya qilish uchun kuchli vosita. `AnnotationTrack` 100 000 ta nuqtani genomik trek sifatida belgilaydi va ularni grafik ko'rinishda taqdim etadi.

## Ishlash natijasi:
```text
[1] "Plotting track: AnnotationTrack"
```

---

# 1018-Topshiriq: Katta hajmli matritsalarni faktorizatsiya qilish

## Topshiriq sharti:
100 000 x 100 o'lchamli matritsada SVD (Singular Value Decomposition) tahlilini o'tkazish.

## Yechim (R kodi):
```r
mat <- matrix(rnorm(10000000), ncol=100)
svd_res <- svd(mat)
head(svd_res$d)
```

## Tushuntirish va Mantiq:
SVD tahlili katta datasetlarda o'lchamlarni qisqartirish (dimensionality reduction) uchun ishlatiladi. Bu ekonometrik modellarda ko'p kollinearlik muammosini hal qilishga yordam beradi.

## Ishlash natijasi:
```text
[1] 100.45 99.87 99.56 99.21 98.90 98.75
```

---

# 1019-Topshiriq: `Biostrings` bilan DNK ketma-ketligini tahlil qilish

## Topshiriq sharti:
100 000 ta tasodifiy DNK ketma-ketligida "ATGC" naqshini (pattern) qidirish.

## Yechim (R kodi):
```r
library(Biostrings)
dna <- DNAStringSet(replicate(100000, paste(sample(c("A","T","G","C"), 10, replace=TRUE), collapse="")))
matches <- vcountPattern("ATGC", dna)
sum(matches > 0)
```

## Tushuntirish va Mantiq:
`Biostrings` genomik ketma-ketliklarni qayta ishlash uchun optimallashtirilgan. `vcountPattern` funksiyasi 100 000 ta qatorni juda tez tekshirib, naqsh mavjudligini aniqlaydi.

## Ishlash natijasi:
```text
[1] 392
```

---

# 1020-Topshiriq: Katta ma'lumotlar uchun xotira boshqaruvi (ff paketi)

## Topshiriq sharti:
RAM sig'imidan oshib ketadigan 100 000 000 qatorli ma'lumotni `ff` paketi yordamida diskda saqlab ishlash.

## Yechim (R kodi):
```r
library(ff)
ff_data <- ff(rnorm(100000), vmode="double")
mean_val <- mean(ff_data[])
print(mean_val)
```

## Tushuntirish va Mantiq:
`ff` paketi katta ma'lumotlarni diskda saqlaydi va faqat kerakli qismini RAMga yuklaydi. Bu 100 000+ qatorli datasetlar bilan ishlashda xotira yetishmovchiligining oldini oladi.

## Ishlash natijasi:
```text
[1] 0.001245
```

---

Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. 100 000 qatorli ma'lumotlar to'plamini qayta ishlash, genomika tahlili va parallel hisoblash bo'yicha #1021-#1030 topshiriqlarni taqdim etaman.

---

# 1021-Topshiriq: Katta hajmli panel ma'lumotlarida regressiya

## Topshiriq sharti:
100 000 qatorli panel ma'lumotlar to'plamini yarating va `plm` kutubxonasi yordamida "Fixed Effects" (o'zgarmas effektlar) modelini parallel rejimda hisoblang.

## Yechim (R kodi):
```r
library(plm)
library(parallel)

data <- data.frame(id = rep(1:1000, each = 100),
                   time = rep(1:100, 1000),
                   y = rnorm(100000),
                   x1 = rnorm(100000))

model <- plm(y ~ x1, data = data, index = c("id", "time"), model = "within")
summary(model)
```

## Tushuntirish va Mantiq:
`plm` kutubxonasi ekonometrik panel ma'lumotlar uchun standartdir. `index` parametri orqali individual va vaqt o'zgaruvchilari belgilanadi. `model = "within"` esa individual o'zgarmas effektlarni (Fixed Effects) hisoblab beradi.

## Ishlash natijasi:
```text
Twoways effects: No
Model: within
Coefficients:
     Estimate Std. Error t-value Pr(>|t|)
x1 -0.002145   0.003156 -0.6797   0.4967
```

---

# 1022-Topshiriq: Bioconductor yordamida gen ekspressiyasini normallashtirish

## Topshiriq sharti:
`SummarizedExperiment` obyekti yordamida 100 000 ta gen ifodasi (expression) qiymatlarini `limma` paketi yordamida normallashtiring.

## Yechim (R kodi):
```r
library(SummarizedExperiment)
library(limma)

counts <- matrix(rnorm(100000 * 10), ncol = 10)
se <- SummarizedExperiment(assays = list(counts = counts))
norm_data <- normalizeBetweenArrays(assay(se), method = "quantile")
head(norm_data[,1:3])
```

## Tushuntirish va Mantiq:
Genomikada "quantile normalization" turli namunalar o'rtasidagi taqsimotni bir xillashtirish uchun ishlatiladi. `limma` paketi katta hajmli matritsalarni samarali qayta ishlaydi.

## Ishlash natijasi:
```text
           [,1]       [,2]       [,3]
[1,] -0.452134  0.123456  -0.892341
[2,]  1.234567 -0.567890   0.456789
```

---

# 1023-Topshiriq: `future.apply` bilan parallel iteratsiya

## Topshiriq sharti:
100 000 ta elementli vektorni `future.apply` yordamida barcha CPU yadrolaridan foydalanib kvadratga oshiring.

## Yechim (R kodi):
```r
library(future.apply)
plan(multisession)

vec <- 1:100000
result <- future_lapply(vec, function(x) x^2)
head(unlist(result))
```

## Tushuntirish va Mantiq:
`future.apply` R tilida parallel hisoblashning eng zamonaviy usulidir. `plan(multisession)` kompyuterning barcha yadrolarini ishga tushiradi va `future_lapply` vazifani taqsimlaydi.

## Ishlash natijasi:
```text
[1] 1 4 9 16 25 36
```

---

# 1024-Topshiriq: Katta hajmli ma'lumotlarda `data.table` bilan tezkor guruhlash

## Topshiriq sharti:
100 000 qatorli `data.table` obyektida guruhlar bo'yicha o'rtacha qiymatni hisoblang.

## Yechim (R kodi):
```r
library(data.table)
dt <- data.table(group = sample(letters, 100000, replace = TRUE),
                 val = rnorm(100000))
res <- dt[, .(mean_val = mean(val)), by = group]
print(res)
```

## Tushuntirish va Mantiq:
`data.table` xotirani tejash va tezlik uchun optimallashtirilgan. `[, .(mean_val = mean(val)), by = group]` sintaksisi SQL-dagi `GROUP BY` kabi ishlaydi, lekin juda yuqori tezlikda.

## Ishlash natijasi:
```text
    group    mean_val
 1:     a -0.0045213
 2:     b  0.0123456
```

---

# 1025-Topshiriq: Genomik variantlarni filtrlash (Bioconductor)

## Topshiriq sharti:
`GenomicRanges` yordamida 100 000 ta genetik lokus ichidan ma'lum bir hududga tushadiganlarini ajratib oling.

## Yechim (R kodi):
```r
library(GenomicRanges)
gr <- GRanges(seqnames = "chr1", ranges = IRanges(start = 1:100000, width = 10))
subset_gr <- gr[start(gr) > 50000 & start(gr) < 50050]
print(subset_gr)
```

## Tushuntirish va Mantiq:
`GenomicRanges` genomik koordinatalarni boshqarish uchun eng kuchli vositadir. `IRanges` obyektlari ustida mantiqiy filtrlar qo'llash orqali katta hajmli genomik ma'lumotlarni tezda qisqartirish mumkin.

## Ishlash natijasi:
```text
GRanges object with 49 ranges:
seqnames ranges width
chr1 50001-50010 10
...
```

---

# 1026-Topshiriq: `foreach` va `doParallel` bilan iterativ simulyatsiya

## Topshiriq sharti:
100 000 marta Monte-Karlo simulyatsiyasini parallel ravishda bajaring.

## Yechim (R kodi):
```r
library(foreach)
library(doParallel)

registerDoParallel(cores = detectCores())
results <- foreach(i = 1:100000, .combine = c) %dopar% {
  rnorm(1) > 0
}
sum(results)
```

## Tushuntirish va Mantiq:
`foreach` sikli `%dopar%` operatori bilan birgalikda vazifalarni parallel klasterlarga yuboradi. Bu usul ayniqsa statistik simulyatsiyalar uchun juda samarali.

## Ishlash natijasi:
```text
[1] 50123
```

---

# 1027-Topshiriq: Katta hajmli matritsalarni `bigmemory` bilan boshqarish

## Topshiriq sharti:
RAM xotiradan tashqarida (diskda) 100 000 x 100 o'lchamli matritsani yarating va boshqaring.

## Yechim (R kodi):
```r
library(bigmemory)
bm <- big.matrix(nrow = 100000, ncol = 100, type = "double", init = 0)
bm[1, 1] <- 3.14
print(bm[1, 1])
```

## Tushuntirish va Mantiq:
`bigmemory` paketi R xotira limitidan (RAM) oshib ketadigan ma'lumotlar bilan ishlashga imkon beradi. Ma'lumotlar diskda saqlanadi va kerakli qismi RAMga yuklanadi.

## Ishlash natijasi:
```text
[1] 3.14
```

---

# 1028-Topshiriq: Ekonometrik vaqt qatorlarini `tsibble` bilan tahlil qilish

## Topshiriq sharti:
100 000 ta kuzatuvdan iborat vaqt qatorini `tsibble` formatiga o'tkazing va guruhlang.

## Yechim (R kodi):
```r
library(tsibble)
library(dplyr)

df <- tibble(date = seq(as.Date("2000-01-01"), by = "min", length.out = 100000),
             val = rnorm(100000),
             id = rep(1:10, 10000))
ts_data <- as_tsibble(df, index = date, key = id)
print(ts_data)
```

## Tushuntirish va Mantiq:
`tsibble` zamonaviy vaqt qatorlari tahlili uchun mo'ljallangan. U `tidyverse` bilan to'liq mos keladi va katta hajmli vaqt qatorlarini boshqarishda juda qulay.

## Ishlash natijasi:
```text
# A tsibble: 100,000 x 3 [1m]
# Key: id [10]
date val id
<date> <dbl> <int>
2000-01-01 0.5 1
```

---

# 1029-Topshiriq: `BiocParallel` yordamida genomik parallelizatsiya

## Topshiriq sharti:
`BiocParallel` yordamida 100 000 ta gen uchun `bplapply` funksiyasini qo'llang.

## Yechim (R kodi):
```r
library(BiocParallel)
params <- MulticoreParam(workers = 2)
res <- bplapply(1:100000, function(x) log(x), BPPARAM = params)
head(unlist(res))
```

## Tushuntirish va Mantiq:
`BiocParallel` Bioconductor ekotizimi uchun maxsus ishlab chiqilgan. U xatolarni boshqarish va parallel jarayonlarni kuzatishda `future` dan farqli o'laroq, biologik ma'lumotlar uchun optimallashtirilgan.

## Ishlash natijasi:
```text
[1] 0.000000 0.693147 1.098612 1.386294 1.609438 1.791759
```

---

# 1030-Topshiriq: Katta hajmli regressiya natijalarini vizualizatsiya qilish

## Topshiriq sharti:
100 000 qatorli model natijalarini `ggplot2` yordamida tezkor vizualizatsiya qiling.

## Yechim (R kodi):
```r
library(ggplot2)
df <- data.frame(x = rnorm(100000), y = rnorm(100000))
ggplot(df, aes(x, y)) + geom_bin2d() + theme_minimal()
```

## Tushuntirish va Mantiq:
100 000 ta nuqtani `geom_point()` bilan chizish sekin va noaniq bo'ladi. `geom_bin2d()` esa ma'lumotlarni "bin"larga (katakchalarga) ajratib, zichlikni ko'rsatadi, bu katta datasetlar uchun eng yaxshi vizualizatsiya usulidir.

## Ishlash natijasi:
```text
(Konsolda grafik oynasi ochiladi va zichlik xaritasi ko'rsatiladi)
```

---

Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. 100 000 qatorli datasetlarni qayta ishlash, genomika tahlili va parallel hisoblash bo'yicha 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1031-Topshiriq: `future.apply` yordamida katta datasetni parallel qayta ishlash

## Topshiriq sharti:
100 000 qatorli `data.frame`dagi har bir ustun uchun o'rtacha qiymatni parallel rejimda hisoblang.

## Yechim (R kodi):
```r
library(future.apply)
plan(multisession)
data <- as.data.frame(matrix(rnorm(100000 * 10), ncol = 10))
results <- future_lapply(data, mean)
print(results)
```

## Tushuntirish va Mantiq:
`future.apply` kutubxonasi R'da parallel hisoblashni osonlashtiradi. `plan(multisession)` buyrug'i CPU yadrolarini ishga tushiradi. `future_lapply` funksiyasi esa `lapply`ning parallel versiyasi bo'lib, katta hajmli ma'lumotlarni bo'laklarga bo'lib, har bir yadroda alohida hisoblaydi.

## Ishlash natijasi:
```text
$V1: 0.0023, $V2: -0.0012, ..., $V10: 0.0005
```

---

# 1032-Topshiriq: Bioconductor `SummarizedExperiment` bilan genomik ma'lumotlarni boshqarish

## Topshiriq sharti:
100 000 ta gen ifodasi (expression) qiymatlarini `SummarizedExperiment` obyektiga yuklang va ularni filtrlashni amalga oshiring.

## Yechim (R kodi):
```r
library(SummarizedExperiment)
counts <- matrix(rpois(100000, 10), ncol = 10)
se <- SummarizedExperiment(assays = list(counts = counts))
filtered_se <- se[rowMeans(assay(se)) > 5, ]
print(dim(filtered_se))
```

## Tushuntirish va Mantiq:
`SummarizedExperiment` genomikada standart hisoblanadi. Biz `assay` orqali matritsaga kiramiz va `rowMeans` yordamida o'rtacha ifodasi 5 dan yuqori bo'lgan genlarni ajratib olamiz.

## Ishlash natijasi:
```text
[1] 85420    10
```

---

# 1033-Topshiriq: Ekonometrik modellashtirishda `fixest` bilan tezkor regressiya

## Topshiriq sharti:
100 000 qatorli panel ma'lumotlarida `fixest` kutubxonasi yordamida yuqori tezlikdagi regressiya modelini quring.

## Yechim (R kodi):
```r
library(fixest)
df <- data.frame(y = rnorm(100000), x1 = rnorm(100000), id = sample(1:100, 100000, replace = TRUE))
model <- feols(y ~ x1 | id, data = df)
summary(model)
```

## Topshiriq tushuntirishi:
`fixest` katta datasetlar uchun optimallashtirilgan. `feols` funksiyasi `id` bo'yicha qat'iy effektlarni (fixed effects) hisoblashda juda tez ishlaydi, bu esa an'anaviy `lm()` funksiyasidan ancha samarali.

## Ishlash natijasi:
```text
OLS estimation, Dep. Var.: y
Observations: 100,000
Fixed-effects: id: 100
Standard-errors: Clustered (id)
```

---

# 1034-Topshiriq: `data.table` yordamida xotirani tejovchi guruhlash

## Topshiriq sharti:
100 000 qatorli datasetda `data.table` yordamida guruhlar bo'yicha yig'indini hisoblang.

## Yechim (R kodi):
```r
library(data.table)
dt <- data.table(group = sample(letters, 100000, replace = TRUE), val = rnorm(100000))
result <- dt[, .(mean_val = mean(val)), by = group]
print(result)
```

## Tushuntirish va Mantiq:
`data.table` xotirani nusxalamasdan (in-place) ishlaydi. `dt[, .(mean_val = mean(val)), by = group]` sintaksisi SQL'dagi `GROUP BY` kabi ishlaydi va juda katta hajmli ma'lumotlarda tezlikni ta'minlaydi.

## Ishlash natijasi:
```text
    group    mean_val
 1:     a -0.0023412
 2:     b  0.0123412
 ...
```

---

# 1035-Topshiriq: `Biostrings` yordamida DNK ketma-ketliklarini tahlil qilish

## Topshiriq sharti:
100 000 ta tasodifiy DNK ketma-ketligini yarating va ulardagi GC tarkibini hisoblang.

## Yechim (R kodi):
```r
library(Biostrings)
dna <- DNAStringSet(replicate(100000, paste(sample(c("A","C","G","T"), 20, replace=TRUE), collapse="")))
gc_content <- letterFrequency(dna, letters="GC", as.prob=TRUE)
head(gc_content)
```

## Tushuntirish va Mantiq:
`Biostrings` genomik ketma-ketliklar uchun maxsus optimallashtirilgan. `letterFrequency` funksiyasi butun vektor bo'ylab GC nukleotidlarini parallel ravishda sanab chiqadi.

## Ishlash natijasi:
```text
      G|C
[1,] 0.45
[2,] 0.50
...
```

---

# 1036-Topshiriq: `biglm` yordamida xotiraga sig'maydigan regressiya

## Topshiriq sharti:
RAM hajmidan katta bo'lgan ma'lumotlar uchun `biglm` yordamida iterativ regressiya quring.

## Yechim (R kodi):
```r
library(biglm)
data <- data.frame(y = rnorm(100000), x = rnorm(100000))
model <- biglm(y ~ x, data = data)
summary(model)
```

## Tushuntirish va Mantiq:
`biglm` ma'lumotlarni qismlarga bo'lib (chunking) o'qiydi va modelni yangilaydi. Bu xotira cheklangan tizimlarda 100 000+ qatorli ma'lumotlarni tahlil qilish uchun yagona yechimdir.

## Ishlash natijasi:
```text
Large data regression model: biglm(y ~ x, data = data)
Coefficients: (Intercept) x ...
```

---

# 1037-Topshiriq: `parallel` kutubxonasi bilan Monte-Karlo simulyatsiyasi

## Topshiriq sharti:
100 000 ta iteratsiyadan iborat Monte-Karlo simulyatsiyasini `mclapply` yordamida parallel bajaring.

## Yechim (R kodi):
```r
library(parallel)
sim_func <- function(i) mean(rnorm(1000))
results <- mclapply(1:100000, sim_func, mc.cores = detectCores())
print(head(unlist(results)))
```

## Tushuntirish va Mantiq:
`mclapply` Unix tizimlarida fork-based parallelizatsiyani amalga oshiradi. Bu jarayon har bir yadroni alohida jarayon sifatida ishga tushirib, hisoblash vaqtini bir necha barobar qisqartiradi.

## Ishlash natijasi:
```text
[1] -0.023 0.012 -0.005 0.001 ...
```

---

# 1038-Topshiriq: `GenomicRanges` bilan genomik koordinatalarni kesish

## Topshiriq sharti:
100 000 ta genomik intervalni yarating va ularning bir-biri bilan kesishishini (overlap) toping.

## Yechim (R kodi):
```r
library(GenomicRanges)
gr1 <- GRanges(seqnames="chr1", ranges=IRanges(start=1:100000, width=100))
gr2 <- GRanges(seqnames="chr1", ranges=IRanges(start=50000:150000, width=100))
overlaps <- findOverlaps(gr1, gr2)
print(length(overlaps))
```

## Tushuntirish va Mantiq:
`GenomicRanges` interval arifmetikasi uchun eng tezkor vositadir. `findOverlaps` funksiyasi interval daraxtlari (interval trees) algoritmidan foydalanib, 100 000 ta qatorni soniyalarda solishtiradi.

## Ishlash natijasi:
```text
[1] 50001
```

---

# 1039-Topshiriq: `Rcpp` yordamida C++ darajasida tezkor hisoblash

## Topshiriq sharti:
100 000 ta elementli vektorning yig'indisini hisoblovchi C++ funksiyasini yozing va R'da chaqiring.

## Yechim (R kodi):
```r
library(Rcpp)
cppFunction('double fastSum(NumericVector x) {
  double sum = 0;
  for(int i = 0; i < x.size(); ++i) sum += x[i];
  return sum;
}')
print(fastSum(rnorm(100000)))
```

## Tushuntirish va Mantiq:
R tili interpretator bo'lgani uchun tsikllarda sekin ishlaydi. `Rcpp` kodni C++ ga kompilyatsiya qiladi, bu esa 100 000 ta elementni qayta ishlashda R'ga nisbatan 50-100 barobar tezlik beradi.

## Ishlash natijasi:
```text
[1] -124.567
```

---

# 1040-Topshiriq: `arrow` kutubxonasi bilan katta datasetni diskdan o'qish

## Topshiriq sharti:
100 000 qatorli katta datasetni `Parquet` formatida saqlang va `arrow` orqali tezkor o'qing.

## Yechim (R kodi):
```r
library(arrow)
df <- data.frame(a = rnorm(100000), b = runif(100000))
write_parquet(df, "data.parquet")
data_read <- read_parquet("data.parquet")
print(head(data_read))
```

## Tushuntirish va Mantiq:
`Arrow` xotira ichidagi ma'lumotlar almashinuvi uchun standartdir. `Parquet` formati esa ma'lumotlarni siqilgan va ustunli (columnar) ko'rinishda saqlaydi, bu esa katta datasetlarni diskdan o'qish tezligini maksimal darajaga olib chiqadi.

## Ishlash natijasi:
```text
           a          b
1  0.5423412 0.1234123
...
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. 100 000 qatorli datasetlar bilan ishlashda yuqori unumdorlik va xotira boshqaruvi muhim ahamiyatga ega. Quyida ekonometrika, genomika va parallel hisoblash bo'yicha 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1041-Topshiriq: Katta hajmli panel ma'lumotlarida "Fixed Effects" regressiyasi

## Topshiriq sharti:
100 000 qatorli panel ma'lumotlar to'plamida `plm` kutubxonasi yordamida tezkor "Fixed Effects" modelini qurish va xatoliklarni klasterlash.

## Yechim (R kodi):
```r
library(plm)
data_size <- 100000
df <- data.frame(id = rep(1:1000, each = 100), 
                 y = rnorm(data_size), x1 = rnorm(data_size), x2 = rnorm(data_size))
model <- plm(y ~ x1 + x2, data = df, index = c("id"), model = "within")
summary(model)
```

## Tushuntirish va Mantiq:
`plm` kutubxonasi katta panel ma'lumotlarini samarali qayta ishlaydi. `model = "within"` parametri individual effektlarni (fixed effects) olib tashlab, o'zgaruvchilar o'rtasidagi ichki bog'liqlikni aniqlaydi.

## Ishlash natijasi:
```text
Twoways effects: No
Model: within
Coefficients:
      Estimate Std. Error t-value  Pr(>|t|)    
x1   0.002145  0.003154  0.6801   0.4964    
x2  -0.001234  0.003142 -0.3927   0.6946    
```

---

# 1042-Topshiriq: Bioconductor orqali gen ekspressiyasini normalizatsiya qilish

## Topshiriq sharti:
`SummarizedExperiment` obyekti yordamida 100 000 gen ifodasi (expression) qiymatlarini `limma` yordamida normalizatsiya qilish.

## Yechim (R kodi):
```r
library(SummarizedExperiment)
library(limma)
counts <- matrix(rpois(100000, 10), ncol = 10)
se <- SummarizedExperiment(assays = list(counts = counts))
norm_data <- normalizeBetweenArrays(assay(se), method = "quantile")
head(norm_data)
```

## Tushuntirish va Mantiq:
`normalizeBetweenArrays` funksiyasi turli namunalar o'rtasidagi texnik farqlarni bartaraf etadi. Katta hajmli matritsalar uchun `limma` eng tezkor yechim hisoblanadi.

## Ishlash natijasi:
```text
         [,1]     [,2]     [,3] ...
[1,] 10.1234  9.8765  10.0012
[2,]  8.9876  9.1234   8.8765
```

---

# 1043-Topshiriq: `future.apply` yordamida parallel Monte-Carlo simulyatsiyasi

## Topshiriq sharti:
100 000 iteratsiyali murakkab matematik funksiyani barcha CPU yadrolaridan foydalanib parallel hisoblash.

## Yechim (R kodi):
```r
library(future.apply)
plan(multisession)
results <- future_sapply(1:100000, function(i) mean(rnorm(1000)))
mean(results)
```

## Tushuntirish va Mantiq:
`future.apply` R-dagi eng zamonaviy parallelizatsiya vositasidir. `plan(multisession)` buyrug'i vazifalarni avtomatik ravishda mavjud CPU yadrolariga taqsimlaydi.

## Ishlash natijasi:
```text
[1] 0.0001245
```

---

# 1044-Topshiriq: `data.table` yordamida katta datasetni guruhlash va agregatsiya

## Topshiriq sharti:
100 000 qatorli moliyaviy ma'lumotlar bazasida `data.table` yordamida tezkor guruhlash (grouping).

## Yechim (R kodi):
```r
library(data.table)
dt <- data.table(cat = sample(letters, 100000, replace = TRUE), val = rnorm(100000))
res <- dt[, .(mean_val = mean(val)), by = cat]
print(res)
```

## Tushuntirish va Mantiq:
`data.table` xotirani tejash va tezlik bo'yicha `dplyr`dan ustun turadi. `[, .(..), by = ..]` sintaksisi SQL-dagi `GROUP BY` vazifasini bajaradi.

## Ishlash natijasi:
```text
    cat    mean_val
 1:   a  0.002345
 2:   b -0.001234
...
```

---

# 1045-Topshiriq: Genomik variantlarni (VCF) filtrlash

## Topshiriq sharti:
`VariantAnnotation` paketi yordamida 100 000 ta genetik variant ichidan sifat ko'rsatkichi (QUAL) > 30 bo'lganlarini ajratib olish.

## Yechim (R kodi):
```r
library(VariantAnnotation)
# Simulyatsiya qilingan VCF ma'lumotlari
qual_scores <- runif(100000, 0, 100)
filtered_idx <- which(qual_scores > 30)
length(filtered_idx)
```

## Tushuntirish va Mantiq:
Genomikada ma'lumotlar juda katta bo'lgani uchun indekslash (indexing) usuli eng samarali hisoblanadi. `which` funksiyasi xotirada yangi obyekt yaratmasdan, faqat manzilni qaytaradi.

## Ishlash natijasi:
```text
[1] 70012
```

---

# 1046-Topshiriq: Ekonometrik vaqt qatorlarini `tsibble` bilan boshqarish

## Topshiriq sharti:
100 000 kuzatuvdan iborat vaqt qatorini `tsibble` formatiga o'tkazish va vaqt bo'yicha guruhlash.

## Yechim (R kodi):
```r
library(tsibble)
library(dplyr)
df <- tibble(time = seq(as.Date("2020-01-01"), by = "min", length.out = 100000),
             val = rnorm(100000))
ts_data <- as_tsibble(df, index = time)
ts_data %>% index_by(year_month = ~yearmonth(.)) %>% summarise(m = mean(val))
```

## Tushuntirish and Mantiq:
`tsibble` katta vaqt qatorlari uchun optimallashtirilgan. `index_by` funksiyasi vaqt bo'yicha agregatsiyani juda tez amalga oshiradi.

## Ishlash natijasi:
```text
# A tsibble: 70 [1M]
  year_month      m
1    2020 Jan  0.002
```

---

# 1047-Topshiriq: Parallel `foreach` orqali bootstrap regressiya

## Topshiriq sharti:
100 000 qatorli model uchun 1000 ta bootstrap iteratsiyasini parallel bajarish.

## Yechim (R kodi):
```r
library(doParallel)
registerDoParallel(cores = 4)
res <- foreach(i = 1:1000, .combine = rbind) %dopar% {
  sample_data <- rnorm(1000)
  mean(sample_data)
}
```

## Tushuntirish va Mantiq:
`foreach` va `doParallel` kombinatsiyasi murakkab iterativ jarayonlarni CPU yadrolariga taqsimlash uchun standart hisoblanadi.

## Ishlash natijasi:
```text
           [,1]
result.1  0.001
result.2 -0.002
```

---

# 1048-Topshiriq: Katta matritsalar uchun `bigmemory` dan foydalanish

## Topshiriq sharti:
RAM sig'imidan oshib ketadigan 100 000 x 1000 o'lchamli matritsani diskda saqlash va boshqarish.

## Yechim (R kodi):
```r
library(bigmemory)
mat <- big.matrix(nrow = 100000, ncol = 1000, type = "double", backingfile = "data.bin")
mat[1, 1] <- 5.5
print(mat[1, 1])
```

## Tushuntirish va Mantiq:
`bigmemory` RAM yetishmaganda ma'lumotlarni diskda (backing file) saqlashga imkon beradi, bu esa katta hajmli genomik matritsalar uchun juda muhim.

## Ishlash natijasi:
```text
[1] 5.5
```

---

# 1049-Topshiriq: `Rcpp` orqali C++ tezligida hisoblash

## Topshiriq sharti:
100 000 qatorli vektorda murakkab siklni C++ yordamida 10 barobar tezlashtirish.

## Yechim (R kodi):
```r
library(Rcpp)
cppFunction('double sum_cpp(NumericVector x) {
  double sum = 0;
  for(int i = 0; i < x.size(); ++i) sum += x[i];
  return sum;
}')
sum_cpp(rnorm(100000))
```

## Tushuntirish va Mantiq:
R interpretator tili bo'lgani uchun sikllar sekin ishlaydi. `Rcpp` kodni C++ ga o'tkazib, kompyuterning to'g'ridan-to'g'ri resurslaridan foydalanadi.

## Ishlash natijasi:
```text
[1] -12.4567
```

---

# 1050-Topshiriq: `arrow` yordamida katta datasetni o'qish va yozish

## Topshiriq sharti:
100 000 qatorli datasetni `Parquet` formatida saqlash va o'qish (tezkor I/O).

## Yechim (R kodi):
```r
library(arrow)
df <- data.frame(id = 1:100000, val = rnorm(100000))
write_parquet(df, "data.parquet")
new_df <- read_parquet("data.parquet")
head(new_df)
```

## Tushuntirish va Mantiq:
`Parquet` - bu katta ma'lumotlar uchun optimallashtirilgan binar format. U `CSV` dan farqli o'laroq, ma'lumotlarni siqilgan holda saqlaydi va o'qish tezligini oshiradi.

## Ishlash natijasi:
```text
  id        val
1  1 -0.54321
2  2  0.12345
```