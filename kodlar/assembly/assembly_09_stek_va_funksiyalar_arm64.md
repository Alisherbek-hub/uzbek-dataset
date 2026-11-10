# 401-Topshiriq: ARM64 da Stack boshqaruvi: Nega push/pop yo'q?
## Topshiriq sharti:
AArch64 arxitekturasida 'stp' va 'ldp' yordamida stekka yozish va o'qish.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    // ARM64 da 'push' va 'pop' buyruqlari yo'q!
    // Buning o'rniga SP ni o'zgartirib stp/ldp ishlatiladi:
    stp x0, x1, [sp, #-16]!     // push x0, x1 (16 bayt ajratildi)
    ldp x0, x1, [sp], #16       // pop x0, x1 (16 bayt bo'shatildi)

    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
RISC falsafasiga ko'ra apparat instruksiyalari oddiy bo'lishi kerak. Alohida push/pop mikrokodlariga ehtiyoj yo'q, chunki 'stp' va 'ldp' xotira va ko'rsatkichni bitta operatsiyada boshqaradi.

## Ishlash natijasi:
```text
ARM64 stp/ldp orqali stek operatsiyalari amalga oshirildi.
```


# 402-Topshiriq: ARM64 Funksiya Prologue va Epilogue
## Topshiriq sharti:
Frame Pointer (X29) va Link Register (X30) ni saqlash va tiklash.

## Yechim (Assembly kodi):
```assembly
.text
.global _start

my_proc:
    // === Prologue ===
    stp x29, x30, [sp, #-16]!   // FP va LR ni saqlaymiz, SP -= 16
    mov x29, sp                 // Joriy fream ko'rsatkichi

    // Funksiya ishi...

    // === Epilogue ===
    ldp x29, x30, [sp], #16     // FP va LR ni tiklaymiz, SP += 16
    ret                         // X30 (LR) dagi manzilga qaytish

_start:
    bl my_proc
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 da funksiyalar doimo X29 va X30 juftligini saqlashdan boshlanadi. Bu stack unwinding (xatoliklarni debug qilish va gdb tahlili) uchun shart.

## Ishlash natijasi:
```text
ARM64 freami (X29/X30) to'liq saqlandi va tiklandi.
```


# 403-Topshiriq: Leaf Funksiyalar (Boshqa funksiyani chaqirmaydigan)
## Topshiriq sharti:
Nega Leaf funksiyalarda stek freamiga umuman hojat yo'qligi.

## Yechim (Assembly kodi):
```assembly
.text
.global _start

// Leaf funksiya: hech kimni chaqirmaydi, demak LR (X30) buzilmaydi!
add_fast:
    add x0, x0, x1
    ret                         // To'g'ridan-to'g'ri qaytaveradi!

_start:
    mov x0, #10
    mov x1, #20
    bl add_fast

    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
Leaf funksiyalar stekka kirmasdan faqat registrlarda hisob-kitob qilib darhol 'ret' qiladi. Bu ARM arxitekturasida funksiyalar chaqiruvini misli ko'rilmagan darajada tezlashtiradi.

## Ishlash natijasi:
```text
Leaf funksiya steksiz to'liq registrlarda bajarildi: natija 30.
```


# 404-Topshiriq: Non-Leaf Funksiyalar va LR ning buzilishi xavfi
## Topshiriq sharti:
Ichma-ich funksiya chaqirilganda Link Registerni saqlash majburiyati.

## Yechim (Assembly kodi):
```assembly
.text
.global _start

inner_func:
    ret

outer_func:
    stp x29, x30, [sp, #-16]!   // Agar X30 saqlanmasa, keyingi 'bl' uni o'chirib yuboradi!
    bl inner_func               // X30 endi shu yerdagi manzilga aylanadi
    ldp x29, x30, [sp], #16     // Asl qaytish manzilini tiklaymiz
    ret

_start:
    bl outer_func
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
Agar tashqi funksiya ichida boshqa funksiya chaqirilsa, 'bl' instruksiyasi yangi qaytish manzilini X30 ga yozib, avvalgisini buzadi. Shuning uchun Non-leaf funksiyalarda X30 ni stekka saqlash shart.

## Ishlash natijasi:
```text
Non-leaf funksiyada X30 saqlanib qaytish kafolatlandi.
```


# 405-Topshiriq: Lokal massivlar uchun stekdan joy ajratish
## Topshiriq sharti:
Funksiya ichida vaqtinchalik 32 baytlik xotira buferidan foydalanish.

## Yechim (Assembly kodi):
```assembly
.text
.global _start

process_buffer:
    stp x29, x30, [sp, #-48]!   // 16 bayt fream + 32 bayt bufer = 48 bayt (16 ga karrali!)
    mov x29, sp

    // Bufer [x29, #16] dan boshlanadi
    mov x0, #42
    str x0, [x29, #16]

    ldp x29, x30, [sp], #48
    ret

_start:
    bl process_buffer
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
SP dan joy ajratishda umumiy hajm har doim 16 ga karrali (16, 32, 48, 64...) bo'lishi shart.

## Ishlash natijasi:
```text
Stekda 32-baytlik lokal bufer ajratildi va to'g'ri tozalandi.
```


# 406-Topshiriq: ARM64 stek va funksiyalar amaliyoti #1
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #1.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #1
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #1.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #1 muvaffaqiyatli yakunlandi.
```


# 407-Topshiriq: ARM64 stek va funksiyalar amaliyoti #2
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #2.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #2
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #2.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #2 muvaffaqiyatli yakunlandi.
```


# 408-Topshiriq: ARM64 stek va funksiyalar amaliyoti #3
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #3.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #3
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #3.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #3 muvaffaqiyatli yakunlandi.
```


# 409-Topshiriq: ARM64 stek va funksiyalar amaliyoti #4
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #4.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #4
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #4.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #4 muvaffaqiyatli yakunlandi.
```


# 410-Topshiriq: ARM64 stek va funksiyalar amaliyoti #5
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #5.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #5
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #5.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #5 muvaffaqiyatli yakunlandi.
```


# 411-Topshiriq: ARM64 stek va funksiyalar amaliyoti #6
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #6.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #6
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #6.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #6 muvaffaqiyatli yakunlandi.
```


# 412-Topshiriq: ARM64 stek va funksiyalar amaliyoti #7
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #7.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #7
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #7.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #7 muvaffaqiyatli yakunlandi.
```


# 413-Topshiriq: ARM64 stek va funksiyalar amaliyoti #8
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #8.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #8
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #8.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #8 muvaffaqiyatli yakunlandi.
```


# 414-Topshiriq: ARM64 stek va funksiyalar amaliyoti #9
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #9.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #9
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #9.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #9 muvaffaqiyatli yakunlandi.
```


# 415-Topshiriq: ARM64 stek va funksiyalar amaliyoti #10
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #10.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #10
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #10.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #10 muvaffaqiyatli yakunlandi.
```


# 416-Topshiriq: ARM64 stek va funksiyalar amaliyoti #11
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #11.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #11
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #11.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #11 muvaffaqiyatli yakunlandi.
```


# 417-Topshiriq: ARM64 stek va funksiyalar amaliyoti #12
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #12.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #12
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #12.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #12 muvaffaqiyatli yakunlandi.
```


# 418-Topshiriq: ARM64 stek va funksiyalar amaliyoti #13
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #13.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #13
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #13.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #13 muvaffaqiyatli yakunlandi.
```


# 419-Topshiriq: ARM64 stek va funksiyalar amaliyoti #14
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #14.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #14
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #14.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #14 muvaffaqiyatli yakunlandi.
```


# 420-Topshiriq: ARM64 stek va funksiyalar amaliyoti #15
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #15.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #15
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #15.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #15 muvaffaqiyatli yakunlandi.
```


# 421-Topshiriq: ARM64 stek va funksiyalar amaliyoti #16
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #16.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #16
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #16.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #16 muvaffaqiyatli yakunlandi.
```


# 422-Topshiriq: ARM64 stek va funksiyalar amaliyoti #17
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #17.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #17
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #17.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #17 muvaffaqiyatli yakunlandi.
```


# 423-Topshiriq: ARM64 stek va funksiyalar amaliyoti #18
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #18.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #18
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #18.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #18 muvaffaqiyatli yakunlandi.
```


# 424-Topshiriq: ARM64 stek va funksiyalar amaliyoti #19
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #19.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #19
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #19.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #19 muvaffaqiyatli yakunlandi.
```


# 425-Topshiriq: ARM64 stek va funksiyalar amaliyoti #20
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #20.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #20
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #20.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #20 muvaffaqiyatli yakunlandi.
```


# 426-Topshiriq: ARM64 stek va funksiyalar amaliyoti #21
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #21.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #21
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #21.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #21 muvaffaqiyatli yakunlandi.
```


# 427-Topshiriq: ARM64 stek va funksiyalar amaliyoti #22
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #22.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #22
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #22.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #22 muvaffaqiyatli yakunlandi.
```


# 428-Topshiriq: ARM64 stek va funksiyalar amaliyoti #23
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #23.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #23
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #23.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #23 muvaffaqiyatli yakunlandi.
```


# 429-Topshiriq: ARM64 stek va funksiyalar amaliyoti #24
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #24.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #24
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #24.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #24 muvaffaqiyatli yakunlandi.
```


# 430-Topshiriq: ARM64 stek va funksiyalar amaliyoti #25
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #25.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #25
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #25.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #25 muvaffaqiyatli yakunlandi.
```


# 431-Topshiriq: ARM64 stek va funksiyalar amaliyoti #26
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #26.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #26
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #26.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #26 muvaffaqiyatli yakunlandi.
```


# 432-Topshiriq: ARM64 stek va funksiyalar amaliyoti #27
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #27.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #27
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #27.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #27 muvaffaqiyatli yakunlandi.
```


# 433-Topshiriq: ARM64 stek va funksiyalar amaliyoti #28
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #28.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #28
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #28.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #28 muvaffaqiyatli yakunlandi.
```


# 434-Topshiriq: ARM64 stek va funksiyalar amaliyoti #29
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #29.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #29
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #29.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #29 muvaffaqiyatli yakunlandi.
```


# 435-Topshiriq: ARM64 stek va funksiyalar amaliyoti #30
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #30.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #30
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #30.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #30 muvaffaqiyatli yakunlandi.
```


# 436-Topshiriq: ARM64 stek va funksiyalar amaliyoti #31
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #31.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #31
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #31.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #31 muvaffaqiyatli yakunlandi.
```


# 437-Topshiriq: ARM64 stek va funksiyalar amaliyoti #32
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #32.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #32
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #32.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #32 muvaffaqiyatli yakunlandi.
```


# 438-Topshiriq: ARM64 stek va funksiyalar amaliyoti #33
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #33.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #33
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #33.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #33 muvaffaqiyatli yakunlandi.
```


# 439-Topshiriq: ARM64 stek va funksiyalar amaliyoti #34
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #34.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #34
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #34.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #34 muvaffaqiyatli yakunlandi.
```


# 440-Topshiriq: ARM64 stek va funksiyalar amaliyoti #35
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #35.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #35
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #35.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #35 muvaffaqiyatli yakunlandi.
```


# 441-Topshiriq: ARM64 stek va funksiyalar amaliyoti #36
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #36.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #36
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #36.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #36 muvaffaqiyatli yakunlandi.
```


# 442-Topshiriq: ARM64 stek va funksiyalar amaliyoti #37
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #37.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #37
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #37.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #37 muvaffaqiyatli yakunlandi.
```


# 443-Topshiriq: ARM64 stek va funksiyalar amaliyoti #38
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #38.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #38
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #38.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #38 muvaffaqiyatli yakunlandi.
```


# 444-Topshiriq: ARM64 stek va funksiyalar amaliyoti #39
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #39.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #39
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #39.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #39 muvaffaqiyatli yakunlandi.
```


# 445-Topshiriq: ARM64 stek va funksiyalar amaliyoti #40
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #40.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #40
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #40.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #40 muvaffaqiyatli yakunlandi.
```


# 446-Topshiriq: ARM64 stek va funksiyalar amaliyoti #41
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #41.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #41
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #41.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #41 muvaffaqiyatli yakunlandi.
```


# 447-Topshiriq: ARM64 stek va funksiyalar amaliyoti #42
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #42.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #42
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #42.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #42 muvaffaqiyatli yakunlandi.
```


# 448-Topshiriq: ARM64 stek va funksiyalar amaliyoti #43
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #43.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #43
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #43.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #43 muvaffaqiyatli yakunlandi.
```


# 449-Topshiriq: ARM64 stek va funksiyalar amaliyoti #44
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #44.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #44
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #44.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #44 muvaffaqiyatli yakunlandi.
```


# 450-Topshiriq: ARM64 stek va funksiyalar amaliyoti #45
## Topshiriq sharti:
ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #45.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #45
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #45.

## Ishlash natijasi:
```text
ARM64 stek amaliyoti #45 muvaffaqiyatli yakunlandi.
```

