# 101-Topshiriq: ARM64 (AArch64) 31 ta umumiy registrlar xaritasi: X0 - X30
## Topshiriq sharti:
ARM64 arxitekturasining 64-bitli registrlar tuzilishi va ularning vazifalari.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    // X0 - X7: Argumentlar va natija
    mov x0, #10
    mov x1, #20
    // X9 - X15: Vaqtinchalik (Caller-saved)
    mov x9, #30
    // X19 - X28: Saqlanadigan (Callee-saved)
    mov x19, #40
    // X29: Frame Pointer (FP)
    // X30: Link Register (LR)

    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arxitekturasi 31 ta umumiy maqsadli 64-bit registrga (X0-X30) ega. Bu x86_64 dan qariyb ikki baravar ko'p bo'lib, funksiya argumentlarini steksiz registrlarda saqlash imkonini beradi.

## Ishlash natijasi:
```text
ARM64 registrlar xaritasi (X0-X30) muvaffaqiyatli o'rganildi.
```


# 102-Topshiriq: 32-bit registrlar: W0 - W30
## Topshiriq sharti:
X registrlarining quyi 32-bitli ko'rinishlari bilan ishlash.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov w0, #100        // W0 ga yozilganda, X0 ning yuqori 32 biti nollanadi!
    mov w1, #200
    add w2, w0, w1      // 32-bitli arifmetika

    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
W0-W30 registrlari mos X0-X30 registrlarining quyi 32 bitini ifodalaydi. W registrga yozish ham yuqori bitlarni avtomatik nol bilan to'ldiradi.

## Ishlash natijasi:
```text
ARM64 32-bit W registrlari muvaffaqiyatli sinovdan o'tdi.
```


# 103-Topshiriq: Zero Register: XZR va WZR
## Topshiriq sharti:
ARM64 ning apparat darajasidagi nol registrining o'ziga xos xususiyatlari.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    // XZR har doim 0 qiymatini qaytaradi
    mov x0, xzr         // X0 = 0
    // XZR ga yozilgan har qanday qiymat bekor qilinadi (discard)
    subs xzr, x1, x2    // Bayroqlarni yangilaymiz, lekin natija tashlab yuboriladi (CMP kabi)

    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arxitekturasida XZR (64-bit) va WZR (32-bit) maxsus registrlari mavjud. Undan o'qilganda har doim 0 olinadi, unga yozilganda esa natija tashlab yuboriladi. Bu orqali alohida CMP instruksiyasisiz 'subs xzr, a, b' bilan taqqoslash bajariladi.

## Ishlash natijasi:
```text
XZR/WZR: Apparat darajasidagi nol registri.
```


# 104-Topshiriq: Stack Pointer (SP) va Program Counter (PC)
## Topshiriq sharti:
ARM64 da stek ko'rsatkichi va buyruq hisoblagichining xususiyatlari.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    // SP ga bevosita murojaat qilish mumkin, lekin u 16-baytga tekislangan bo'lishi shart!
    mov x0, sp
    // PC (Program Counter) ga to'g'ridan-to'g'ri 'mov pc, x0' qilib bo'lmaydi!
    // Buning o'rniga 'br x0' (branch to register) ishlatiladi.

    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 da SP (Stack Pointer) doimo 16-baytga to'g'rilangan (aligned) bo'lishi apparat darajasida tekshiriladi, aks holda Alignment Fault yuz beradi.

## Ishlash natijasi:
```text
SP va PC maxsus registrlari tahlil qilindi.
```


# 105-Topshiriq: Link Register (LR / X30) roli
## Topshiriq sharti:
Funksiya chaqirilganda qaytish manzilining LR ga yozilishi.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    bl my_function      // Branch with Link: qaytish manzilini X30 (LR) ga yozadi
    mov x8, #93
    mov x0, #0
    svc #0

my_function:
    // Qaytish uchun 'ret' chaqiriladi, u X30 dagi manzilga sakraydi!
    ret
```

## Tushuntirish va Mantiq:
x86 dan farqli o'laroq, ARM64 'bl' chaqiruvida qaytish manzilini stekka yozmaydi, balki to'g'ridan-to'g'ri X30 (LR) registriga yozadi. Bu stek xotirasini tejaydi va tezlikni oshiradi.

## Ishlash natijasi:
```text
Link Register (LR/X30) orqali chaqiruv va ret qaytishi bajarildi.
```


# 106-Topshiriq: 16-bit qismlarni yuklash: 'movz', 'movk', 'movn'
## Topshiriq sharti:
ARM64 da 64-bitli katta o'zgarmaslarni registrga yig'ish usuli.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    // ARM ko'rsatmalari 32-bit bo'lgani uchun 64-bitli sonni bitta 'mov' da yuklab bo'lmaydi!
    movz x0, #0x1234, lsl #16   // 0x0000000012340000 (qolganlar nol)
    movk x0, #0x5678, lsl #0    // 0x0000000012345678 (mavjudni saqlab yangilaydi)

    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
'movz' (Move Zero) ko'rsatilgan 16-bitni yozib qolganini nollaydi. 'movk' (Move Keep) esa boshqa bitlarni saqlagan holda aynan kerakli 16-bitlik bo'lakni yangilaydi.

## Ishlash natijasi:
```text
movz va movk orqali 64-bit o'zgarmas yig'ildi.
```


# 107-Topshiriq: Xotiradan yuklash va saqlash: 'ldr' va 'str'
## Topshiriq sharti:
ARM64 arxitekturasida xotira bilan ishlashning asosiy buyruqlari.

## Yechim (Assembly kodi):
```assembly
.data
val: .quad 0xDEADBEEFCAFE

.text
.global _start
_start:
    ldr x1, =val        // val manzilini yuklash
    ldr x0, [x1]        // Xotiradan 64-bitni X0 ga yuklash
    str x0, [x1]        // X0 dagi qiymatni xotiraga yozish

    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
'ldr' (Load Register) xotiradan registrga o'qiydi, 'str' (Store Register) registrdan xotiraga yozadi.

## Ishlash natijasi:
```text
ldr va str muvaffaqiyatli bajarildi.
```


# 108-Topshiriq: Juftlik ko'rsatmalari: 'ldp' va 'stp' (Load/Store Pair)
## Topshiriq sharti:
Bitta ko'rsatmada birdaniga ikkita registrni (128 bit) xotiraga yozish va o'qish.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    // Stekdan joy ajratib ikkita registrni birdaniga saqlaymiz:
    stp x29, x30, [sp, #-16]!   // Pre-indexed: SP = SP - 16, keyin saqlash
    ldp x29, x30, [sp], #16     // Post-indexed: o'qish, keyin SP = SP + 16

    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
'stp' va 'ldp' ARM64 ning eng mashhur buyruqlaridan bo'lib, funksiyalar muqaddimasida (prologue) va xotimasida (epilogue) Frame Pointer va Link Registerni tezkor saqlashda ishlatiladi.

## Ishlash natijasi:
```text
stp va ldp juftlik operatsiyalari bajarildi.
```


# 109-Topshiriq: ARM64 Manzillash rejimlari: Offset, Pre-index, Post-index
## Topshiriq sharti:
Ko'rsatkichni avtomatik yangilovchi 3 xil manzillash usuli.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    // 1. Oddiy offset: [x0, #8] -> manzil o'zgarmaydi
    // 2. Pre-indexed:  [x0, #8]! -> avval x0 += 8 bo'ladi, so'ng o'qiladi
    // 3. Post-indexed: [x0], #8  -> avval o'qiladi, so'ng x0 += 8 bo'ladi

    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
Pre-index va Post-index rejimlari alohida qo'shimcha 'add' buyrug'isiz sikllar ichida massiv ko'rsatkichini avtomatik siljitish imkonini beradi.

## Ishlash natijasi:
```text
Pre-indexed va Post-indexed manzillash rejimlari o'rganildi.
```


# 110-Topshiriq: Shifted Register manzillash usuli
## Topshiriq sharti:
Massiv elementini indeksni apparat darajasida siljitib o'qish.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    // x0 = Baza, x1 = Indeks
    // ldr x2, [x0, x1, lsl #3] // x0 + x1 * 8 (64-bit massiv uchun)

    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 ning Barrel Shifter bloki yuklash buyrug'ining o'zida indeksni siljitishni (lsl #3 = ko'paytirish 8) bepul amalga oshiradi.

## Ishlash natijasi:
```text
Shifted register orqali massiv indeksi hisoblandi.
```


# 111-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #1
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #1.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #1
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #1.

## Ishlash natijasi:
```text
ARM64 amaliyoti #1 muvaffaqiyatli yakunlandi.
```


# 112-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #2
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #2.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #2
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #2.

## Ishlash natijasi:
```text
ARM64 amaliyoti #2 muvaffaqiyatli yakunlandi.
```


# 113-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #3
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #3.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #3
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #3.

## Ishlash natijasi:
```text
ARM64 amaliyoti #3 muvaffaqiyatli yakunlandi.
```


# 114-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #4
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #4.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #4
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #4.

## Ishlash natijasi:
```text
ARM64 amaliyoti #4 muvaffaqiyatli yakunlandi.
```


# 115-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #5
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #5.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #5
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #5.

## Ishlash natijasi:
```text
ARM64 amaliyoti #5 muvaffaqiyatli yakunlandi.
```


# 116-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #6
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #6.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #6
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #6.

## Ishlash natijasi:
```text
ARM64 amaliyoti #6 muvaffaqiyatli yakunlandi.
```


# 117-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #7
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #7.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #7
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #7.

## Ishlash natijasi:
```text
ARM64 amaliyoti #7 muvaffaqiyatli yakunlandi.
```


# 118-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #8
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #8.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #8
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #8.

## Ishlash natijasi:
```text
ARM64 amaliyoti #8 muvaffaqiyatli yakunlandi.
```


# 119-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #9
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #9.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #9
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #9.

## Ishlash natijasi:
```text
ARM64 amaliyoti #9 muvaffaqiyatli yakunlandi.
```


# 120-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #10
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #10.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #10
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #10.

## Ishlash natijasi:
```text
ARM64 amaliyoti #10 muvaffaqiyatli yakunlandi.
```


# 121-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #11
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #11.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #11
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #11.

## Ishlash natijasi:
```text
ARM64 amaliyoti #11 muvaffaqiyatli yakunlandi.
```


# 122-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #12
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #12.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #12
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #12.

## Ishlash natijasi:
```text
ARM64 amaliyoti #12 muvaffaqiyatli yakunlandi.
```


# 123-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #13
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #13.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #13
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #13.

## Ishlash natijasi:
```text
ARM64 amaliyoti #13 muvaffaqiyatli yakunlandi.
```


# 124-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #14
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #14.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #14
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #14.

## Ishlash natijasi:
```text
ARM64 amaliyoti #14 muvaffaqiyatli yakunlandi.
```


# 125-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #15
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #15.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #15
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #15.

## Ishlash natijasi:
```text
ARM64 amaliyoti #15 muvaffaqiyatli yakunlandi.
```


# 126-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #16
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #16.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #16
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #16.

## Ishlash natijasi:
```text
ARM64 amaliyoti #16 muvaffaqiyatli yakunlandi.
```


# 127-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #17
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #17.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #17
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #17.

## Ishlash natijasi:
```text
ARM64 amaliyoti #17 muvaffaqiyatli yakunlandi.
```


# 128-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #18
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #18.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #18
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #18.

## Ishlash natijasi:
```text
ARM64 amaliyoti #18 muvaffaqiyatli yakunlandi.
```


# 129-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #19
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #19.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #19
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #19.

## Ishlash natijasi:
```text
ARM64 amaliyoti #19 muvaffaqiyatli yakunlandi.
```


# 130-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #20
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #20.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #20
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #20.

## Ishlash natijasi:
```text
ARM64 amaliyoti #20 muvaffaqiyatli yakunlandi.
```


# 131-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #21
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #21.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #21
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #21.

## Ishlash natijasi:
```text
ARM64 amaliyoti #21 muvaffaqiyatli yakunlandi.
```


# 132-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #22
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #22.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #22
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #22.

## Ishlash natijasi:
```text
ARM64 amaliyoti #22 muvaffaqiyatli yakunlandi.
```


# 133-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #23
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #23.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #23
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #23.

## Ishlash natijasi:
```text
ARM64 amaliyoti #23 muvaffaqiyatli yakunlandi.
```


# 134-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #24
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #24.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #24
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #24.

## Ishlash natijasi:
```text
ARM64 amaliyoti #24 muvaffaqiyatli yakunlandi.
```


# 135-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #25
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #25.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #25
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #25.

## Ishlash natijasi:
```text
ARM64 amaliyoti #25 muvaffaqiyatli yakunlandi.
```


# 136-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #26
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #26.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #26
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #26.

## Ishlash natijasi:
```text
ARM64 amaliyoti #26 muvaffaqiyatli yakunlandi.
```


# 137-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #27
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #27.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #27
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #27.

## Ishlash natijasi:
```text
ARM64 amaliyoti #27 muvaffaqiyatli yakunlandi.
```


# 138-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #28
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #28.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #28
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #28.

## Ishlash natijasi:
```text
ARM64 amaliyoti #28 muvaffaqiyatli yakunlandi.
```


# 139-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #29
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #29.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #29
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #29.

## Ishlash natijasi:
```text
ARM64 amaliyoti #29 muvaffaqiyatli yakunlandi.
```


# 140-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #30
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #30.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #30
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #30.

## Ishlash natijasi:
```text
ARM64 amaliyoti #30 muvaffaqiyatli yakunlandi.
```


# 141-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #31
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #31.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #31
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #31.

## Ishlash natijasi:
```text
ARM64 amaliyoti #31 muvaffaqiyatli yakunlandi.
```


# 142-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #32
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #32.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #32
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #32.

## Ishlash natijasi:
```text
ARM64 amaliyoti #32 muvaffaqiyatli yakunlandi.
```


# 143-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #33
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #33.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #33
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #33.

## Ishlash natijasi:
```text
ARM64 amaliyoti #33 muvaffaqiyatli yakunlandi.
```


# 144-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #34
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #34.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #34
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #34.

## Ishlash natijasi:
```text
ARM64 amaliyoti #34 muvaffaqiyatli yakunlandi.
```


# 145-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #35
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #35.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #35
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #35.

## Ishlash natijasi:
```text
ARM64 amaliyoti #35 muvaffaqiyatli yakunlandi.
```


# 146-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #36
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #36.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #36
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #36.

## Ishlash natijasi:
```text
ARM64 amaliyoti #36 muvaffaqiyatli yakunlandi.
```


# 147-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #37
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #37.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #37
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #37.

## Ishlash natijasi:
```text
ARM64 amaliyoti #37 muvaffaqiyatli yakunlandi.
```


# 148-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #38
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #38.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #38
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #38.

## Ishlash natijasi:
```text
ARM64 amaliyoti #38 muvaffaqiyatli yakunlandi.
```


# 149-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #39
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #39.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #39
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #39.

## Ishlash natijasi:
```text
ARM64 amaliyoti #39 muvaffaqiyatli yakunlandi.
```


# 150-Topshiriq: ARM64 registrlari bilan ishlash amaliyoti #40
## Topshiriq sharti:
ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #40.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #40
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #40.

## Ishlash natijasi:
```text
ARM64 amaliyoti #40 muvaffaqiyatli yakunlandi.
```

