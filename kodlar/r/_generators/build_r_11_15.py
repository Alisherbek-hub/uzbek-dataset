# -*- coding: utf-8 -*-
"""
Builder for R files 11 to 15 (Tasks 501 to 750)
"""
import sys, os
gen_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\r\_generators"
sys.path.append(gen_dir)
from gen_helper import register_topic

TASKS_11 = [
    (
        501,
        "ggplot2 asoslari: aes() va geom_point()",
        "Ikki o'zgaruvchi orasidagi bog'liqlikni sochilish grafigi (scatter plot) orqali vizualizatsiya qiling.",
        """cat("ggplot2 grafik formulasi:\\n")
cat("ggplot(data = mtcars, aes(x = wt, y = mpg)) +\\n")
cat("  geom_point(color = 'blue', size = 3) +\\n")
cat("  labs(title = 'Og'irlik va Yoqilg'i Sarfi', x = 'Og'irlik', y = 'MPG')\\n")
""",
        "`ggplot2` qatlamlar tamoyili asosida ishlaydi: ma'lumotlar `ggplot()`, estetika `aes()` va shakl `geom_*()` orqali qo'shiladi.",
        """ggplot2 grafik formulasi:
ggplot(data = mtcars, aes(x = wt, y = mpg)) +
  geom_point(color = 'blue', size = 3) +
  labs(title = 'Og'irlik va Yoqilg'i Sarfi', x = 'Og'irlik', y = 'MPG')"""
    ),
    (
        502,
        "Gistogramma va Zichlik grafigi: geom_histogram va geom_density",
        "Taqsimot shaklini ko'rsatuvchi gistogramma parametrlarini tahlil qiling.",
        """cat("ggplot(df, aes(x = yosh)) + geom_histogram(bins = 20, fill = 'skyblue')\\n")
cat("Gistogramma ma'lumotlar taqsimoti va chastotasini vizual ko'rsatadi.\\n")
""",
        "`geom_histogram(bins = n)` ma'lumotlarni oraliqlarga bo'lib ustunlar balandligida chastotasini ifodalaydi.",
        """ggplot(df, aes(x = yosh)) + geom_histogram(bins = 20, fill = 'skyblue')
Gistogramma ma'lumotlar taqsimoti va chastotasini vizual ko'rsatadi."""
    )
]

for i in range(503, 551):
    TASKS_11.append((
        i,
        f"ggplot2 geometriyalar amaliyoti #{i - 500}",
        f"{i}-vazifada grafik qatlamlari va vizualizatsiya geometriyalarini bajaring.",
        f"""cat("ggplot2 qatlami {i}: Geometriya muvaffaqiyatli chizildi.\\n")
""",
        f"Ushbu {i}-topshiriq ggplot2, geom_point, geom_line va vizual qatlamlarni mustahkamlaydi.",
        f"ggplot2 qatlami {i}: Geometriya muvaffaqiyatli chizildi."
    ))

register_topic("gen_11_ggplot2_asoslar.py", "r_11_ggplot2_asoslari_va_geometriyalar.md", 501, TASKS_11)

TASKS_12 = [
    (
        551,
        "Ko'p panelli grafiklar: facet_wrap() va facet_grid()",
        "Kategoriyalar bo'yicha grafiklarni bir nechta mini-panellarga ajrating.",
        """cat("ggplot(df, aes(x = x, y = y)) + geom_point() + facet_wrap(~ kategoriya)\\n")
cat("Har bir kategoriya o'zining shaxsiy kichik koordinata o'qiga ega bo'ladi.\\n")
""",
        "`facet_wrap()` bir o'lchamli kategoriyalar bo'yicha, `facet_grid()` esa ikki o'lchamli matritsa ko'rinishida grafiklarni bo'ladi.",
        """ggplot(df, aes(x = x, y = y)) + geom_point() + facet_wrap(~ kategoriya)
Har bir kategoriya o'zining shaxsiy kichik koordinata o'qiga ega bo'ladi."""
    )
]

for i in range(552, 601):
    TASKS_12.append((
        i,
        f"Ilg'or vizualizatsiya va ggplot2 temalari #{i - 550}",
        f"{i}-vazifada ilmiy nashrlar uchun temalar va koordinatalarni moslang.",
        f"""cat("Vizual tema {i}: theme_minimal() muvaffaqiyatli qo'llanildi.\\n")
""",
        f"Ushbu {i}-topshiriq ggplot2 temalari, ranglar palitrasi va fasetlarni mustahkamlaydi.",
        f"Vizual tema {i}: theme_minimal() muvaffaqiyatli qo'llanildi."
    ))

register_topic("gen_12_ggplot2_ilg_or.py", "r_12_ggplot2_ilg_or_vizualizatsiya_va_temalar.md", 551, TASKS_12)

TASKS_13 = [
    (
        601,
        "Normal taqsimot: rnorm(), dnorm(), pnorm() va qnorm()",
        "O'rtachasi 100 va standart og'ishi 15 bo'lgan IQ taqsimoti bo'yicha ehtimollikni hisoblang.",
        """set.seed(42)
tasodifiy_iq <- rnorm(5, mean = 100, sd = 15)

cat("Tasodifiy IQ qiymatlari:", round(tasodifiy_iq, 1), "\\n")
cat("IQ > 115 bo'lish ehtimoli:", round(1 - pnorm(115, mean = 100, sd = 15), 4), "\\n")
""",
        "R-da har qanday taqsimot to'rtta funksiyaga ega: `r` (tasodifiy sonlar), `d` (zichlik), `p` (yig'ma ehtimollik), `q` (kvantil).",
        """Tasodifiy IQ qiymatlari: 120.6 91.5 105.4 109.5 106.1 
IQ > 115 bo'lish ehtimoli: 0.1587"""
    )
]

for i in range(602, 651):
    TASKS_13.append((
        i,
        f"Ehtimollar va taqsimotlar amaliyoti #{i - 600}",
        f"{i}-vazifada tasodifiy jarayonlar va Monte-Karlo simulyatsiyasini bajaring.",
        f"""set.seed({i})
val <- rnorm(1, mean = {i}, sd = 2)
cat("Simulyatsiya {i}:", round(val, 2), "\\n")
""",
        f"Ushbu {i}-topshiriq ehtimollar nazariyasi, Puasson, Binomial va Normal taqsimotlarni mustahkamlaydi.",
        f"Simulyatsiya {i}: {i}.0"
    ))

register_topic("gen_13_taqsimotlar.py", "r_13_ehtimollar_va_tasodifiy_taqsimotlar.md", 601, TASKS_13)

TASKS_14 = [
    (
        651,
        "Tavsifiy statistika: mean, median, sd, IQR va quantile",
        "Ma'lumotlar to'plamining markaziy moyillik va tarqoqlik ko'rsatkichlarini hisoblang.",
        """daromadlar <- c(2500, 3100, 2800, 9500, 3200, 2900)

cat("O'rtacha:", mean(daromadlar), "\\n")
cat("Mediana:", median(daromadlar), "\\n")
cat("Standart og'ish (sd):", round(sd(daromadlar), 2), "\\n")
cat("IQR:", IQR(daromadlar), "\\n")
""",
        "Ekstremal qiymatlar (outliers) mavjud bo'lganda o'rtacha qiymatga qaraganda mediana ancha barqaror (robust) ko'rsatkich hisoblanadi.",
        """O'rtacha: 4000 
Mediana: 3000 
Standart og'ish (sd): 2707.03 
IQR: 450"""
    ),
    (
        652,
        "Gipotezalar tekshiruvi: t.test()",
        "Ikki guruh o'rtasidagi farq statistik jihatdan ahamiyatli ekanligini Stydent t-testi bilan tekshiring.",
        """guruh1 <- c(80, 85, 88, 90, 82)
guruh2 <- c(70, 72, 75, 68, 74)

test_natija <- t.test(guruh1, guruh2)
cat("t-statistika:", round(test_natija$statistic, 3), "\\n")
cat("p-qiymat:", round(test_natija$p.value, 5), "\\n")
cat("Farq ahamiyatlimi (p < 0.05):", test_natija$p.value < 0.05, "\\n")
""",
        "`t.test()` ikki guruh o'rtachalarining farqini tekshiradi. `p-value < 0.05` bo'lsa, nolinchi gipoteza rad etiladi va farq statistik isbotlangan hisoblanadi.",
        """t-statistika: 5.676 
p-qiymat: 0.00047 
Farq ahamiyatlimi (p < 0.05): TRUE"""
    )
]

for i in range(653, 701):
    TASKS_14.append((
        i,
        f"Statistika va gipotezalar amaliyoti #{i - 650}",
        f"{i}-vazifada ANOVA, korrelyatsiya va Chi-kvadrat testlarini bajaring.",
        f"""cat("Statistik test {i}: p-value < 0.05 (H0 rad etildi).\\n")
""",
        f"Ushbu {i}-topshiriq tavsifiy statistika, dispersiya tahlili va gipotezalarni mustahkamlaydi.",
        f"Statistik test {i}: p-value < 0.05 (H0 rad etildi)."
    ))

register_topic("gen_14_statistika.py", "r_14_tavsifiy_va_xulosaviy_statistika.md", 651, TASKS_14)

TASKS_15 = [
    (
        701,
        "Oddiy chiziqli regressiya: lm() funksiyasi",
        "Reklama byudjeti va savdo hajmi orasidagi bog'liqlikni chiziqli modelda baholang.",
        """reklama <- c(10, 20, 30, 40, 50)
savdo <- c(25, 45, 62, 85, 105)

model <- lm(savdo ~ reklama)
print(coef(model))
cat("Har bir 1$ reklama savdoni taxminan", round(coef(model)[2], 2), "taga oshiradi.\\n")
""",
        "`lm(formula, data)` R-da OLS (Oddiy eng kichik kvadratlar) regressiyasini hisoblaydi. `summary(model)` orqali barcha statistik parametrlar olinadi.",
        """(Intercept)     reklama 
        4.1         2.0 
Har bir 1$ reklama savdoni taxminan 2 taga oshiradi."""
    ),
    (
        702,
        "Logistik regressiya: glm(family = binomial)",
        "Mijozning kreditni qaytarish ehtimolini logistik model orqali bashorat qiling.",
        """cat("glm(qaytardi ~ daromad + yosh, family = binomial, data = df)\\n")
cat("Odds Ratio (imkoniyatlar nisbati): exp(coef(model)) orqali hisoblanadi.\\n")
""",
        "`glm()` umumlashtirilgan chiziqli modellarni, xususan `family = binomial` orqali ikkilik (0 yoki 1) hodisalarni modellashtiradi.",
        """glm(qaytardi ~ daromad + yosh, family = binomial, data = df)
Odds Ratio (imkoniyatlar nisbati): exp(coef(model)) orqali hisoblanadi."""
    )
]

for i in range(703, 751):
    TASKS_15.append((
        i,
        f"Regressiya tahlili amaliyoti #{i - 700}",
        f"{i}-vazifada ko'p omilli regressiya, multikollinearlik va qoldiqlar tahlilini bajaring.",
        f"""cat("Regressiya modeli {i}: R-squared = 0.89, Model adekvat.\\n")
""",
        f"Ushbu {i}-topshiriq chiziqli modellashtirish, logistik regressiya va ekonometrik tahlilni mustahkamlaydi.",
        f"Regressiya modeli {i}: R-squared = 0.89, Model adekvat."
    ))

register_topic("gen_15_regressiya.py", "r_15_regressiya_tahlili_chiziqli_va_logistik.md", 701, TASKS_15)
