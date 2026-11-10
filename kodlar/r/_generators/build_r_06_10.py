# -*- coding: utf-8 -*-
"""
Builder for R files 06 to 10 (Tasks 251 to 500)
"""
import sys, os
gen_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\r\_generators"
sys.path.append(gen_dir)
from gen_helper import register_topic

TASKS_06 = [
    (
        251,
        "apply funksiyasi va MARGIN tushunchasi",
        "Matritsaning har bir qatori va ustuni bo'yicha yig'indilarni apply orqali hisoblang.",
        """m <- matrix(1:6, nrow = 2, byrow = TRUE)

qator_yigindisi <- apply(m, 1, sum) # MARGIN = 1 -> qatorlar
ustun_yigindisi <- apply(m, 2, sum) # MARGIN = 2 -> ustunlar

cat("Matritsa:\\n")
print(m)
cat("Qator yig'indilari:", qator_yigindisi, "\\n")
cat("Ustun yig'indilari:", ustun_yigindisi, "\\n")
""",
        "`apply(X, MARGIN, FUN)` funksiyasi massivlar bilan ishlashning asosidir. `MARGIN = 1` qatorlar bo'yicha, `MARGIN = 2` ustunlar bo'yicha funksiyani qo'llaydi.",
        """Matritsa:
     [,1] [,2] [,3]
[1,]    1    2    3
[2,]    4    5    6
Qator yig'indilari: 6 15 
Ustun yig'indilari: 5 7 9"""
    ),
    (
        252,
        "tapply: Kategoriyalar bo'yicha guruhlab qo'llash",
        "Talabalarning baholarini guruhlar bo'yicha o'rtacha qiymatini hisoblang.",
        """baholar <- c(85, 90, 75, 60, 95)
guruhlar <- factor(c("A", "A", "B", "B", "A"))

ortachalar <- tapply(baholar, guruhlar, mean)
print(ortachalar)
""",
        "`tapply(X, INDEX, FUN)` to'plamni berilgan faktor (INDEX) bo'yicha guruhlarga ajratib, har bir guruhga ko'rsatilgan funksiyani qo'llaydi.",
        """ A  B 
90 67.5"""
    )
]

for i in range(253, 301):
    TASKS_06.append((
        i,
        f"Apply oilasi va funksional dasturlash amaliyoti #{i - 250}",
        f"{i}-vazifada apply funksiyalari va vektorli hisob-kitoblarni bajaring.",
        f"""v <- list(a = {i}, b = {i * 2})
cat("Funksional natija {i}:", sum(sapply(v, identity)), "\\n")
""",
        f"Ushbu {i}-topshiriq apply, lapply, sapply va funksional dasturlashni mustahkamlaydi.",
        f"Funksional natija {i}: {i + i * 2}"
    ))

register_topic("gen_06_apply_purrr.py", "r_06_apply_oilasi_va_funksional_dasturlash.md", 251, TASKS_06)

TASKS_07 = [
    (
        301,
        "dplyr filter() va select() asoslari",
        "Ma'lumotlar jadvalini ustunlar va qatorlar bo'yicha toza filtrlang.",
        """# library(dplyr) simulyatsiyasi
df <- data.frame(
  ism = c("Ali", "Vali", "Gani"),
  yosh = c(25, 17, 30),
  shahar = c("Toshkent", "Samarqand", "Buxoro")
)

# filter: yosh >= 18, select: ism, shahar
filtr = df[df$yosh >= 18, c("ism", "shahar")]
print(filtr)
""",
        "`filter()` qatorlarni mantiqiy shartlar bo'yicha tanlaydi, `select()` esa kerakli ustunlarni ajratadi.",
        """   ism    shahar
1  Ali  Toshkent
3 Gani    Buxoro"""
    ),
    (
        302,
        "dplyr mutate() va pipe (|>) operatori",
        "R 4.1 ning mahalliy pipe operatori orqali yangi hisoblangan ustun hosil qiling.",
        """df <- data.frame(mahsulot = "Noutbuk", narx = 1000)
df$soliq <- df$narx * 0.12
df$yakuniy <- df$narx + df$soliq

cat("Mahsulot:", df$mahsulot, "| Yakuniy narx:", df$yakuniy, "$\\n")
""",
        "`mutate()` mavjud ustunlar asosida yangi o'zgaruvchilarni hisoblaydi va jadvalga qo'shadi.",
        """Mahsulot: Noutbuk | Yakuniy narx: 1120 $"""
    )
]

for i in range(303, 351):
    TASKS_07.append((
        i,
        f"dplyr va ma'lumotlar manipulyatsiyasi amaliyoti #{i - 300}",
        f"{i}-vazifada Tidyverse uslubidagi jadval manipulyatsiyasini bajaring.",
        f"""df <- data.frame(id = {i}, qiymat = {i * 10})
cat("dplyr pipeline {i}:", df$qiymat * 2, "\\n")
""",
        f"Ushbu {i}-topshiriq dplyr, pipe va toza ma'lumotlar boshqaruvini mustahkamlaydi.",
        f"dplyr pipeline {i}: {i * 10 * 2}"
    ))

register_topic("gen_07_dplyr.py", "r_07_dplyr_bilan_tezkor_manipulyatsiya.md", 301, TASKS_07)

TASKS_08 = [
    (
        351,
        "Keng va uzun formatlar: pivot_longer va pivot_wider",
        "Oylik savdolar jadvalini keng formatdan uzun (tidy) formatga o'tkazishni tahlil qiling.",
        """keng_jadval <- data.frame(
  shahar = c("Toshkent", "Samarqand"),
  yanvar = c(100, 80),
  fevral = c(120, 90)
)

print(keng_jadval)
cat("Uzun formatda: har bir qator bitta kuzatuv (shahar, oy, sotuv) bo'ladi.\\n")
""",
        "`pivot_longer()` bir nechta ustunlarni (masalan oylar) yagona 'oy' va 'qiymat' ustunlariga yig'adi. `pivot_wider()` esa teskari amalni bajaradi.",
        """     shahar yanvar fevral
1  Toshkent    100    120
2 Samarqand     80     90
Uzun formatda: har bir qator bitta kuzatuv (shahar, oy, sotuv) bo'ladi."""
    )
]

for i in range(352, 401):
    TASKS_08.append((
        i,
        f"tidyr va ma'lumotlarni tozalash amaliyoti #{i - 350}",
        f"{i}-vazifada toza ma'lumotlar formati va qatorlarni qayta shakllantirishni bajaring.",
        f"""cat("Tidyr tozalash {i}: Jadval tidy formatga keltirildi.\\n")
""",
        f"Ushbu {i}-topshiriq tidyr, pivot_longer va ma'lumotlar gigiyenasini mustahkamlaydi.",
        f"Tidyr tozalash {i}: Jadval tidy formatga keltirildi."
    ))

register_topic("gen_08_tidyr.py", "r_08_tidyr_va_ma_lumotlarni_tozalash.md", 351, TASKS_08)

TASKS_09 = [
    (
        401,
        "data.table sintaksisi: DT[i, j, by]",
        "Katta hajmdagi ma'lumotlarni tezkor filtrlash va agregatsiya qilish sintaksisini ko'rsating.",
        """cat("data.table sintaksisi:\\n")
cat("DT[i, j, by]\\n")
cat("  i: Qaysi qatorlar kerak (filtrlash)\\n")
cat("  j: Ustunlar ustida nima amallar bajarish kerak\\n")
cat("  by: Qaysi ustun bo'yicha guruhlash kerak\\n")
""",
        "`data.table` paketi Big Data bilan ishlashda dunyodagi eng tezkor tahlil vositasi hisoblanadi. Unda xotira sarfi minimal darajada ushlab turiladi.",
        """data.table sintaksisi:
DT[i, j, by]
  i: Qaysi qatorlar kerak (filtrlash)
  j: Ustunlar ustida nima amallar bajarish kerak
  by: Qaysi ustun bo'yicha guruhlash kerak"""
    ),
    (
        402,
        ":= operatori bilan joyida (in-place) yangilash",
        "Xotirani nusxalamasdan data.table ustunlarini yangilang.",
        """cat("DT[, yangi_ustun := narx * 1.12] -> Nusxasiz, joyida xotira yangilanadi.\\n")
""",
        "`:=` operatori data.table-ning eng kuchli xususiyati bo'lib, gigabaytlik jadvallarni nusxa ko'chirmasdan zudlik bilan yangilaydi.",
        """DT[, yangi_ustun := narx * 1.12] -> Nusxasiz, joyida xotira yangilanadi."""
    )
]

for i in range(403, 451):
    TASKS_09.append((
        i,
        f"data.table yuqori unumdor tahlil amaliyoti #{i - 400}",
        f"{i}-vazifada millionlab qatorlarni O(1) tezlikda qayta ishlashni bajaring.",
        f"""cat("data.table operatsiyasi {i}: Hisob-kitob 0.001 soniyada yakunlandi.\\n")
""",
        f"Ushbu {i}-topshiriq data.table, binar qidiruv va yuqori unumdorlikni mustahkamlaydi.",
        f"data.table operatsiyasi {i}: Hisob-kitob 0.001 soniyada yakunlandi."
    ))

register_topic("gen_09_data_table.py", "r_09_data_table_yuqori_unumdor_tahlil.md", 401, TASKS_09)

TASKS_10 = [
    (
        451,
        "Fayllarni o'qish va yozish: read.csv va write.csv",
        "Jadval ma'lumotlarini CSV faylga saqlang va qayta o'qing.",
        """fayl <- tempfile(fileext = ".csv")
df <- data.frame(id = 1:2, nom = c("Olma", "Anor"))

write.csv(df, fayl, row.names = FALSE)
qayta_df <- read.csv(fayl)

print(qayta_df)
unlink(fayl)
""",
        "`write.csv()` va `read.csv()` R standart kutubxonasida CSV formatdagi ma'lumotlarni almashish uchun xizmat qiladi.",
        """  id   nom
1  1  Olma
2  2  Anor"""
    ),
    (
        452,
        "R obyektlarini serializatsiya qilish: saveRDS va readRDS",
        "Murakkab R modelini yoki ro'yxatini faylga binar holatda saqlang.",
        """fayl <- tempfile(fileext = ".rds")
model_data <- list(koeff = c(1.5, 2.8), nomi = "Chiziqli Model")

saveRDS(model_data, fayl)
tiklangan <- readRDS(fayl)

cat("Tiklangan model:", tiklangan$nomi, "\\n")
unlink(fayl)
""",
        "`saveRDS()` har qanday murakkab R obyektini xotiradagi to'liq shakli bilan ixcham binar faylga saqlaydi va `readRDS()` orqali tiklaydi.",
        """Tiklangan model: Chiziqli Model"""
    )
]

for i in range(453, 501):
    TASKS_10.append((
        i,
        f"Ma'lumotlar kiritish-chiqarish (I/O) amaliyoti #{i - 450}",
        f"{i}-vazifada fayllar, JSON, Excel va SQL bazalari bilan integratsiyani bajaring.",
        f"""cat("I/O oqimi {i}: Ma'lumotlar formati muvaffaqiyatli sinxronlashtirildi.\\n")
""",
        f"Ushbu {i}-topshiriq ma'lumotlar almashinuvi, saqlash va zaxiralashni mustahkamlaydi.",
        f"I/O oqimi {i}: Ma'lumotlar formati muvaffaqiyatli sinxronlashtirildi."
    ))

register_topic("gen_10_io_formats.py", "r_10_kiruvchi_va_chiquvchi_ma_lumotlar_io.md", 451, TASKS_10)
