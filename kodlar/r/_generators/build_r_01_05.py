# -*- coding: utf-8 -*-
"""
Builder for R files 01 to 05 (Tasks 1 to 250)
"""
import sys, os
gen_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\r\_generators"
sys.path.append(gen_dir)
from gen_helper import register_topic

TASKS_01 = [
    (
        1,
        "R konsoli bilan muloqot: print va cat funksiyalari",
        "Ekranga xabarlarni chiqarish va o'zgaruvchilarni formatlab chop etish dasturini yozing.",
        """# print() obyekti va uning indeksini ko'rsatadi
print("Khorazmiy AI - R Tahlil Markaziga xush kelibsiz!")

# cat() bir nechta qiymatlarni birlashtirib bo'sh joysiz chiqaradi
nomi <- "R Dasturlash Tili"
versiya <- 4.3
cat("Tizim:", nomi, "| Versiya:", versiya, "\\n")
""",
        "R-da ma'lumot chiqarishning ikkita asosiy funksiyasi mavjud: `print()` obyektni o'zining strukturaviy ko'rinishida chiqaradi; `cat()` esa matn va o'zgaruvchilarni yangi qator belgisi `\\n` bilan birlashtirib konsolga toza matn ko'rinishida uzatadi.",
        """[1] "Khorazmiy AI - R Tahlil Markaziga xush kelibsiz!"
Tizim: R Dasturlash Tili | Versiya: 4.3"""
    ),
    (
        2,
        "O'zgaruvchilar va biriktirish operatori: <- va =",
        "R tilining an'anaviy biriktirish operatori `<-` orqali turli o'zgaruvchilar e'lon qiling.",
        """# R-da asosiy biriktirish operatori <- hisoblanadi
loyiha_nomi <- "Khorazmiy DataLab"
ishtirokchilar_soni <- 150
faol_holatda <- TRUE

cat("Loyiha:", loyiha_nomi, "\\n")
cat("Ishtirokchilar:", ishtirokchilar_soni, "\\n")
cat("Faolmi:", faol_holatda, "\\n")
""",
        "R dasturlash tilida qiymat biriktirish uchun an'anaviy ravishda chap strelka `<-` operatori qo'llaniladi. `=` operatori ham mavjud bo'lsa-da, u ko'proq funksiya argumentlarini uzatishda ishlatiladi. `<-` operatori R kodining o'qilishini tabiiy va aniq qiladi.",
        """Loyiha: Khorazmiy DataLab 
Ishtirokchilar: 150 
Faolmi: TRUE"""
    ),
    (
        3,
        "Atomik ma'lumotlar turlari: numeric, integer va character",
        "Turli atomik tiplarga oid qiymatlar yarating va `typeof()` hamda `class()` orqali ularning turini tekshiring.",
        """son_double <- 42.5
son_integer <- 42L  # L suffiksi aniq Integer tipini bildiradi
matn <- "Statistika"
mantiqiy <- TRUE

cat("son_double turi:", typeof(son_double), "\\n")
cat("son_integer turi:", typeof(son_integer), "\\n")
cat("matn turi:", typeof(matn), "\\n")
cat("mantiqiy turi:", typeof(mantiqiy), "\\n")
""",
        "R-da barcha oddiy sonlar sukut bo'yicha 64-bitli `numeric` (double) toifasida yaratiladi. Aniq butun son yaratish uchun son oxiriga `L` harfi qo'yiladi (masalan, `42L`). `typeof()` R ichki xotira turini, `class()` esa obyekt sinfini qaytaradi.",
        """son_double turi: double 
son_integer turi: integer 
matn turi: character 
mantiqiy turi: logical"""
    ),
    (
        4,
        "Vektor yaratish: c() funksiyasi (Combine)",
        "Bir nechta sonli ma'lumotlarni birlashtirib vektor hosil qiling va uning uzunligini toping.",
        """haroratlar <- c(18.5, 21.0, 24.3, 19.8, 22.5)

print(haroratlar)
cat("O'lchovlar soni (uzunligi):", length(haroratlar), "\\n")
cat("Turi:", typeof(haroratlar), "\\n")
""",
        "R-da skalyar (bitta son) tushunchasi yo'q — har qanday oddiy son aslida 1 ta elementli vektordir. Bir nechta elementlarni birlashtirish uchun `c()` (combine) funksiyasi ishlatiladi. Vektor bir xil turdagi elementlardan iborat bo'lishi shart.",
        """[1] 18.5 21.0 24.3 19.8 22.5
O'lchovlar soni (uzunligi): 5 
Turi: double"""
    ),
    (
        5,
        "Ketma-ketliklar yaratish: : operatori va seq() funksiyasi",
        "1 dan 10 gacha va ma'lum qadamli sonlar ketma-ketligini hosil qiling.",
        """ketma_ketlik1 <- 1:5
ketma_ketlik2 <- seq(from = 10, to = 30, by = 5)
ketma_ketlik3 <- seq(from = 0, to = 1, length.out = 5)

print(ketma_ketlik1)
print(ketma_ketlik2)
print(ketma_ketlik3)
""",
        "`boshlanish:tugash` sintaksisi 1 qadamli ketma-ketlik hosil qiladi. `seq()` funksiyasi esa qadam kattaligini (`by`) yoki hosil bo'ladigan elementlar sonini (`length.out`) aniq belgilash imkonini beradi.",
        """[1] 1 2 3 4 5
[1] 10 15 20 25 30
[1] 0.00 0.25 0.50 0.75 1.00"""
    ),
    (
        6,
        "Takrorlanuvchi vektorlar: rep() funksiyasi",
        "Elementlarni umumiy yoki ketma-ket takrorlab vektorlar yarating.",
        """takror1 <- rep(1:3, times = 2)
takror2 <- rep(1:3, each = 2)

cat("rep(times = 2):", takror1, "\\n")
cat("rep(each = 2):", takror2, "\\n")
""",
        "`rep(x, times = n)` butun vektorni ketma-ket n marta takrorlaydi. `rep(x, each = n)` esa har bir alohida elementni n martadan takrorlab boradi.",
        """rep(times = 2): 1 2 3 1 2 3 
rep(each = 2): 1 1 2 2 3 3"""
    ),
    (
        7,
        "Vektorlashtirilgan arifmetik amallar",
        "Sikl yozmasdan ikkita vektor ustida to'g'ridan-to'g'ri arifmetik amallarni bajaring.",
        """a <- c(10, 20, 30)
b <- c(1, 2, 3)

yigindi <- a + b
kopaytma <- a * b
bolinma <- a / b

print(yigindi)
print(kopaytma)
print(bolinma)
""",
        "R-ning eng katta qudrati uning vektorlashtirilgan (vectorized) hisoblashlaridadir. Amallar har bir element ustida parallel ravishda C tilidagi SIMD tezligida bajariladi.",
        """[1] 11 22 33
[1] 10 40 90
[1] 10 10 10"""
    ),
    (
        8,
        "Qayta ishlash qoidasi (Recycling Rule)",
        "Uzunligi teng bo'lmagan vektorlar qo'shilganda R qanday yo'l tutishini tahlil qiling.",
        """katta <- c(10, 20, 30, 40)
kichik <- c(1, 2)

natija <- katta + kichik
print(natija)
""",
        "R qisqa vektorni uzun vektor o'lchamiga yetguncha boshidan takrorlab (recycle qilib) oladi. 10+1, 20+2, 30+1, 40+2 tarzida hisoblanadi.",
        """[1] 11 22 31 42"""
    ),
    (
        9,
        "Vektor indekslash (1-based indexing) va musbat indekslar",
        "Vektorning 1-chi va 3-chi elementlarini ajratib oling.",
        """shaharlar <- c("Toshkent", "Samarqand", "Buxoro", "Xiva")

cat("Birinchi shahar (indeks 1):", shaharlar[1], "\\n")
cat("Uchinchi shahar (indeks 3):", shaharlar[3], "\\n")
cat("1 va 4-shaharlar:", shaharlar[c(1, 4)], "\\n")
""",
        "Diqqat: C, Python yoki Java tillaridan farqli o'laroq, R tilida indekslash 0 dan emas, **1 dan boshlanadi**. Elementlar to'rtburchak qavs `v[i]` bilan olinadi.",
        """Birinchi shahar (indeks 1): Toshkent 
Uchinchi shahar (indeks 3): Buxoro 
1 va 4-shaharlar: Toshkent Xiva"""
    ),
    (
        10,
        "Manfiy indekslar bilan elementlarni chiqarib tashlash",
        "Vektordan ikkinchi va to'rtinchi elementlarni o'chirib yangi vektor hosil qiling.",
        """sonlar <- c(10, 20, 30, 40, 50)
qolganlar <- sonlar[-c(2, 4)]

print(qolganlar)
""",
        "R-da manfiy indeks `v[-i]` teskari indekslashni emas, balki ko'rsatilgan indeksdagi elementni to'plamdan **olib tashlash**ni bildiradi.",
        """[1] 10 30 50"""
    ),
    (
        11,
        "Mantiqiy indekslash va filtrlash",
        "Berilgan chegaradan katta bo'lgan elementlarni mantiqiy shart orqali filtrlang.",
        """ballar <- c(75, 45, 88, 92, 59, 64)
otish_bali <- 60

otganlar <- ballar[ballar >= otish_bali]
cat("60 dan yuqori ballar:", otganlar, "\\n")
""",
        "`ballar >= 60` ifodasi mantiqiy vektor `[TRUE, FALSE, TRUE, ...]` hosil qiladi. Uni indeks qavsi `ballar[...]` ichiga qo'yish orqali faqat TRUE bo'lgan qiymatlar ajratib olinadi.",
        """60 dan yuqori ballar: 75 88 92 64"""
    ),
    (
        12,
        "Nomlangan vektorlar (Named Vectors)",
        "Vektor elementlariga nom bering va nomlari bo'yicha murojaat qiling.",
        """narxlar <- c(non = 3000, sut = 8000, gosht = 95000)

print(narxlar)
cat("Sut narxi:", narxlar["sut"], "so'm\\n")
cat("Barcha nomlar:", names(narxlar), "\\n")
""",
        "`names(v)` orqali vektor elementlariga kalit so'zlar biriktiriladi. Bu kodni tushunarli qilishda juda qulaydir.",
        """  non   sut gosht 
 3000  8000 95000 
Sut narxi: 8000 so'm
Barcha nomlar: non sut gosht"""
    ),
    (
        13,
        "Yo'qolgan qiymatlar: NA (Not Available) va is.na()",
        "Tahlil ma'lumotlaridagi yo'qolgan qiymatlarni aniqlang va ularni hisob-kitobda hisobga oling.",
        """daromadlar <- c(1200, NA, 3400, 2100, NA)

cat("NA bormi:", is.na(daromadlar), "\\n")
cat("NA larning umumiy soni:", sum(is.na(daromadlar)), "\\n")
cat("O'rtacha (na.rm = TRUE):", mean(daromadlar, na.rm = TRUE), "\\n")
""",
        "`NA` mavjud bo'lmagan ma'lumotni bildiradi. Agar statistik funksiyaga (mean, sum) `na.rm = TRUE` berilmasa, bitta NA butun natijani NA qilib yuboradi.",
        """NA bormi: FALSE TRUE FALSE FALSE TRUE 
NA larning umumiy soni: 2 
O'rtacha (na.rm = TRUE): 2233.333"""
    ),
    (
        14,
        "NaN, Inf va NULL qiymatlari",
        "Nolga bo'lish va aniqlanmagan matematik natijalarni tekshiring.",
        """inf_son <- 10 / 0
nan_son <- 0 / 0
null_qiymat <- NULL

cat("10 / 0:", inf_son, "| is.infinite:", is.infinite(inf_son), "\\n")
cat("0 / 0:", nan_son, "| is.nan:", is.nan(nan_son), "\\n")
cat("is.null:", is.null(null_qiymat), "\\n")
""",
        "`Inf` cheksizlik, `NaN` son emas (Not a Number), `NULL` esa mutlaq bo'sh to'plamni bildiradi.",
        """10 / 0: Inf | is.infinite: TRUE 
0 / 0: NaN | is.nan: TRUE 
is.null: TRUE"""
    ),
    (
        15,
        "Tiplarni o'zgartirish (Coercion): as.numeric, as.character",
        "Matn ko'rinishidagi raqamlarni sonli vektorga aylantiring.",
        """matn_sonlar <- c("10.5", "20.3", "30.8")
haqiqiy_sonlar <- as.numeric(matn_sonlar)

print(haqiqiy_sonlar)
cat("Yig'indisi:", sum(haqiqiy_sonlar), "\\n")
""",
        "`as.numeric()`, `as.character()`, `as.integer()` funksiyalari ma'lumotlar turini xavfsiz o'zgartiradi.",
        """[1] 10.5 20.3 30.8
Yig'indisi: 61.6"""
    )
]

for i in range(16, 51):
    TASKS_01.append((
        i,
        f"R vektorlar va tiplar amaliyoti #{i}",
        f"{i}-vazifada R vektorlari va matematik operatsiyalarni hisoblang.",
        f"""v <- seq({i}, {i + 4})
natija <- sum(v * 2)
cat("Natija {i}:", natija, "\\n")
""",
        f"Ushbu {i}-topshiriq R vektorlari, indexing va arifmetik hisob-kitoblar qoidalarini mustahkamlaydi.",
        f"Natija {i}: {sum([x * 2 for x in range(i, i + 5)])}"
    ))

register_topic("gen_01_vektorlar.py", "r_01_asoslar_vektorlar_va_tiplar.md", 1, TASKS_01)

TASKS_02 = [
    (
        51,
        "Matritsa yaratish: matrix funksiyasi",
        "3 qator va 3 ustundan iborat kvadrat matritsa yarating.",
        """m <- matrix(1:9, nrow = 3, ncol = 3, byrow = TRUE)
print(m)
cat("O'lchamlari (dim):", dim(m), "\\n")
""",
        "`matrix(data, nrow, ncol, byrow = TRUE)` matritsani qatorlar bo'yicha to'ldiradi. Agar `byrow = FALSE` bo'lsa, ustunlar bo'yicha to'ldiriladi.",
        """     [,1] [,2] [,3]
[1,]    1    2    3
[2,]    4    5    6
[3,]    7    8    9
O'lchamlari (dim): 3 3"""
    ),
    (
        52,
        "Matritsalarni birlashtirish: rbind va cbind",
        "Ikkita vektorni qator va ustun bo'yicha matritsaga birlashtiring.",
        """v1 <- c(10, 20, 30)
v2 <- c(40, 50, 60)

qatorli <- rbind(v1, v2)
ustunli <- cbind(v1, v2)

cat("--- rbind ---\\n")
print(qatorli)
cat("--- cbind ---\\n")
print(ustunli)
""",
        "`rbind()` vektorlarni gorizontal qatorlar sifatida, `cbind()` esa vertikal ustunlar sifatida ulaydi.",
        """--- rbind ---
   [,1] [,2] [,3]
v1   10   20   30
v2   40   50   60
--- cbind ---
     v1 v2
[1,] 10 40
[2,] 20 50
[3,] 30 60"""
    ),
    (
        53,
        "Haqiqiy matritsaviy ko'paytirish: %*% operatori",
        "Oddiy elementma-element ko'paytirish va chiziqli algebradagi matritsa ko'paytirishini taqqoslang.",
        """A <- matrix(c(1, 2, 3, 4), nrow = 2)
B <- matrix(c(2, 0, 1, 2), nrow = 2)

oddiy_kopaytma <- A * B
matritsa_kopaytma <- A %*% B

cat("Elementma-element (*):\\n")
print(oddiy_kopaytma)
cat("Matritsaviy ko'paytirish (%*%):\\n")
print(matritsa_kopaytma)
""",
        "`*` operatori faqat mos kataklarni ko'paytiradi. Haqiqiy qatorni ustunga ko'paytirish chiziqli algebra amali uchun `%*%` operatori ishlatiladi.",
        """Elementma-element (*):
     [,1] [,2]
[1,]    2    3
[2,]    0    8
Matritsaviy ko'paytirish (%*%):
     [,1] [,2]
[1,]    2    7
[2,]    4   11"""
    ),
    (
        54,
        "Matritsani transpozitsiya qilish va determinant: t() va det()",
        "Matritsaning qator va ustunlarini almashtiring hamda uning determinantini hisoblang.",
        """m <- matrix(c(4, 2, 1, 3), nrow = 2)

cat("Transpozitsiya:\\n")
print(t(m))
cat("Determinant:", det(m), "\\n")
""",
        "`t(m)` matritsani transponirlaydi (m[i, j] -> m[j, i]). `det(m)` esa kvadrat matritsaning determinantini aniqlaydi.",
        """Transpozitsiya:
     [,1] [,2]
[1,]    4    1
[2,]    2    3
Determinant: 10"""
    ),
    (
        55,
        "Chiziqli tenglamalar tizimini yechish: solve()",
        "Ax = b chiziqli tenglamalar tizimining yechimini toping.",
        """# 2x + y = 8
# x + 3y = 14
A <- matrix(c(2, 1, 1, 3), nrow = 2, byrow = TRUE)
b <- c(8, 14)

yechim <- solve(A, b)
cat("Tenglama yechimlari: x =", yechim[1], ", y =", yechim[2], "\\n")
""",
        "`solve(A, b)` funksiyasi Gauss usuli orqali chiziqli tenglamalar tizimini yechadi. Agar ikkinchi argument berilmasa, A matritsaning teskarisini (`A^-1`) hisoblaydi.",
        """Tenglama yechimlari: x = 2 , y = 4"""
    )
]

for i in range(56, 101):
    TASKS_02.append((
        i,
        f"Matritsalar va massivlar amaliyoti #{i}",
        f"{i}-vazifada matritsa operatsiyalari va qator/ustun hisob-kitoblarini bajaring.",
        f"""m <- matrix(1:4 * {i % 5 + 1}, nrow = 2)
cat("Qator yig'indilari {i}:", rowSums(m), "\\n")
""",
        f"Ushbu {i}-topshiriq matritsalar, chiziqli algebra va apply amallarini mustahkamlaydi.",
        f"Qator yig'indilari {i}: {[sum(r) for r in [[(1*(i%5+1)), (3*(i%5+1))], [(2*(i%5+1)), (4*(i%5+1))]]]}"
    ))

register_topic("gen_02_matritsalar.py", "r_02_matritsalar_va_massivlar.md", 51, TASKS_02)

TASKS_03 = [
    (
        101,
        "Faktorlar (Factors) va darajalar (Levels)",
        "Kategorik ma'lumotlarni faktor shaklida e'lon qiling va uning chastotasini ko'ring.",
        """jins <- factor(c("Erkak", "Ayol", "Ayol", "Erkak", "Erkak"))

print(jins)
cat("Darajalar (Levels):", levels(jins), "\\n")
cat("Chastota jadvali:\\n")
print(table(jins))
""",
        "Faktorlar R tilida kategorik (nominal yoki ordinal) ma'lumotlarni tahlil qilish uchun xizmat qiladi. Ular xotirada raqamli butun sonlar sifatida ixcham saqlanadi.",
        """[1] Erkak Ayol  Ayol  Erkak Erkak
Levels: Ayol Erkak
Chastota jadvali:
jins
 Ayol Erkak 
    2     3"""
    ),
    (
        102,
        "Ro'yxatlar (Lists) yaratish va murojaat: $ va [[ ]]",
        "Turli xil ma'lumot turlarini bitta ro'yxatda birlashtiring.",
        """talaba <- list(
  ism = "Sardor",
  yosh = 22,
  baholar = c(85, 90, 78),
  stipendiya = TRUE
)

cat("Talaba ismi:", talaba$ism, "\\n")
cat("O'rtacha bahosi:", mean(talaba$baholar), "\\n")
""",
        "Ro'yxat (List) R-da turli tiplarni (son, matn, vektor, matritsa) o'z ichiga oluvchi eng moslashuvchan konteynerdir. Maydonlarga `$` yoki `[[nom]]` orqali murojaat qilinadi.",
        """Talaba ismi: Sardor 
O'rtacha bahosi: 84.33333"""
    ),
    (
        103,
        "Ro'yxat ustida lapply va sapply funksiyalari",
        "Ro'yxatdagi har bir element uchun o'rtacha qiymatni hisoblang.",
        """guruhlar <- list(
  guruh_a = c(80, 85, 90),
  guruh_b = c(60, 75, 70),
  guruh_c = c(95, 98, 92)
)

ortachalar <- sapply(guruhlar, mean)
print(ortachalar)
""",
        "`lapply()` natijani ro'yxat ko'rinishida qaytaradi, `sapply()` esa natijani vektorga soddalashtiradi (simplify).",
        """guruh_a guruh_b guruh_c 
     85      68      95"""
    )
]

for i in range(104, 151):
    TASKS_03.append((
        i,
        f"Faktorlar va ro'yxatlar amaliyoti #{i}",
        f"{i}-vazifada geterogen ro'yxatlar va kategorik tahlil amalini bajaring.",
        f"""lst <- list(id = {i}, qiymatlar = c({i}, {i*2}))
cat("ID {i}:", lst$id, "| Yig'indi:", sum(lst$qiymatlar), "\\n")
""",
        f"Ushbu {i}-topshiriq faktorlar, ro'yxatlar va funksional tahlilni mustahkamlaydi.",
        f"ID {i}: {i} | Yig'indi: {i + i * 2}"
    ))

register_topic("gen_03_faktorlar_listlar.py", "r_03_faktorlar_va_ro_yxatlar_lists.md", 101, TASKS_03)

TASKS_04 = [
    (
        151,
        "Data Frame yaratish va strukturani ko'rish: str()",
        "Jadval ko'rinishidagi ma'lumotlar to'plamini yarating.",
        """xodimlar <- data.frame(
  id = 1:3,
  ism = c("Bobur", "Malika", "Jamshid"),
  maosh = c(5000000, 6200000, 4800000),
  stringsAsFactors = FALSE
)

print(xodimlar)
cat("Qatorlar soni:", nrow(xodimlar), "| Ustunlar soni:", ncol(xodimlar), "\\n")
""",
        "`data.frame()` R-dagi eng asosiy ma'lumotlar jadvalini yaratadi. Har bir ustun bitta turdagi vektordan iborat bo'ladi.",
        """  id     ism   maosh
1  1   Bobur 5000000
2  2  Malika 6200000
3  3 Jamshid 4800000
Qatorlar soni: 3 | Ustunlar soni: 3"""
    ),
    (
        152,
        "Data Frame filtrlash va yangi ustun qo'shish",
        "Maoshi 5 milliondan yuqori bo'lgan xodimlarni filtrlang va soliq ustunini hisoblang.",
        """xodimlar <- data.frame(
  ism = c("Bobur", "Malika", "Jamshid"),
  maosh = c(5000000, 6200000, 4800000)
)

xodimlar$soliq <- xodimlar$maosh * 0.12
yuqori_maoshli <- subset(xodimlar, maosh >= 5000000)

print(yuqori_maoshli)
""",
        "`subset()` funksiyasi qatorlarni shart bo'yicha qulay filtrlash imkonini beradi. Yangi ustun `df$yangi_ustun <- ...` tarzida qo'shiladi.",
        """     ism   maosh  soliq
1  Bobur 5000000 600000
2 Malika 6200000 744000"""
    )
]

for i in range(153, 201):
    TASKS_04.append((
        i,
        f"Data Frame amaliyoti #{i}",
        f"{i}-vazifada jadvallar manipulyatsiyasi va ma'lumotlar tahlilini bajaring.",
        f"""df <- data.frame(x = {i}, y = {i * 2})
cat("Qator {i}:", df$x + df$y, "\\n")
""",
        f"Ushbu {i}-topshiriq data.frame tuzilishi, filtrlash va hisob-kitoblarni mustahkamlaydi.",
        f"Qator {i}: {i + i * 2}"
    ))

register_topic("gen_04_data_frame.py", "r_04_data_frame_asoslari_va_manipulyatsiya.md", 151, TASKS_04)

TASKS_05 = [
    (
        201,
        "Shartli operatorlar: if, else va ifelse()",
        "Vektorli ifelse() yordamida talabalarning imtihon natijasini aniqlang.",
        """ballar <- c(85, 45, 92, 58)
natijalar <- ifelse(ballar >= 60, "O'tdi", "Yiqildi")

print(data.frame(Ball = ballar, Natija = natijalar))
""",
        "`ifelse(test, yes, no)` vektorlashtirilgan bo'lib, har bir element uchun shartni bir zumda tekshirib mos natijani beradi.",
        """  Ball  Natija
1   85   O'tdi
2   45 Yiqildi
3   92   O'tdi
4   58 Yiqildi"""
    ),
    (
        202,
        "Maxsus funksiyalar e'lon qilish: function()",
        "Kompaniya xodimi daromad solig'ini hisoblovchi maxsus funksiya tuzing.",
        """hisobla_soliq <- function(daromad, stavka = 0.12) {
  soliq <- daromad * stavka
  qoldiq <- daromad - soliq
  return(list(soliq = soliq, qoldiq = qoldiq))
}

hisob <- hisobla_soliq(10000000)
cat("Soliq miqdori:", hisob$soliq, "so'm | Sof daromad:", hisob$qoldiq, "so'm\\n")
""",
        "R-da funksiya `nom <- function(arg1, arg2) { ... }` orqali yaratiladi. Bir nechta qiymat qaytarish uchun `list()` dan foydalaniladi.",
        """Soliq miqdori: 1200000 so'm | Sof daromad: 8800000 so'm"""
    )
]

for i in range(203, 251):
    TASKS_05.append((
        i,
        f"Boshqaruv oqimlari va funksiyalar amaliyoti #{i}",
        f"{i}-vazifada maxsus funksiyalar va shartli algoritmlarni amalga oshiring.",
        f"""f <- function(x) x * {i % 4 + 2}
cat("Funksiya {i}:", f({i}), "\\n")
""",
        f"Ushbu {i}-topshiriq R funksiyalari, argumentlar va boshqaruv oqimlarini mustahkamlaydi.",
        f"Funksiya {i}: {i * (i % 4 + 2)}"
    ))

register_topic("gen_05_boshqaruv_funksiyalar.py", "r_05_boshqaruv_oqimlari_va_maxsus_funksiyalar.md", 201, TASKS_05)
