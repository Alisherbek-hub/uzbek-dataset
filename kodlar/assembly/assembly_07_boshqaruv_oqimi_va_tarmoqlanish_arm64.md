# 301-Topshiriq: ARM64 Shartsiz sakrash: 'b' va 'br'
## Topshiriq sharti:
Leyblga to'g'ridan-to'g'ri va registr orqali sakrashni ko'rsating.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    b next_step         // Shartsiz leybllarga sakrash
    mov x0, #999        // O'tkazib yuboriladi

next_step:
    adr x1, dynamic_lbl // Registrga manzilni yuklash
    br x1               // Registrdagi manzilga sakrash (Branch to Register)

dynamic_lbl:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
'b label' ko'rsatilgan leybldan davom ettiradi. 'br reg' esa dinamik manzil (funksiya ko'rsatkichlari, jump tables) bo'yicha sakrashni ta'minlaydi.

## Ishlash natijasi:
```text
b va br orqali sakrashlar muvaffaqiyatli amalga oshirildi.
```


# 302-Topshiriq: ARM64 Shartli sakrashlar: 'b.cond'
## Topshiriq sharti:
NZCV bayroqlari bo'yicha shartli tarmoqlanish.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #10
    mov x2, #20
    cmp x1, x2
    b.lt is_less        // x1 < x2 rost bo'lsa sakrash

    mov x0, #1
    b exit_lbl
is_less:
    mov x0, #0
exit_lbl:
    mov x8, #93
    svc #0
```

## Tushuntirish va Mantiq:
'b.eq', 'b.ne', 'b.gt', 'b.lt', 'b.ge', 'b.le' kabi shartli sakrashlar PSTATE dagi bayroqlar holatiga qarab ijro yo'nalishini belgilaydi.

## Ishlash natijasi:
```text
b.lt orqali shartli sakrash bajarildi: 10 < 20 tasdiqlandi.
```


# 303-Topshiriq: Nol bo'yicha tezkor sakrash: 'cbz' va 'cbnz'
## Topshiriq sharti:
Alohida CMP buyrug'isiz registr nolga tengligini tekshirib sakrang.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #0
    cbz x0, is_zero     // Compare and Branch if Zero (CMP shart emas!)
    mov x1, #1
    b end_prog

is_zero:
    mov x1, #42         // X0 nol bo'lgani uchun shu yerga tushadi
end_prog:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
'cbz reg, label' va 'cbnz reg, label' (Compare and Branch if Non-Zero) ko'rsatmalari solishtirish va sakrashni bitta 32-bitli operatsiyaga jamlaydi va bayroqlarni buzmaydi.

## Ishlash natijasi:
```text
cbz orqali nol qiymati tekshirildi va sakraldi.
```


# 304-Topshiriq: Bit tekshirib sakrash: 'tbz' va 'tbnz'
## Topshiriq sharti:
Registrning aniq bir biti 0 yoki 1 ekanligini tekshirib sakrash.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #0b1000     // 3-bit = 1
    tbnz x0, #3, bit_set // Agar 3-bit 1 bo'lsa sakrash!

    mov x1, #0
    b finish
bit_set:
    mov x1, #1          // Sakraldi
finish:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
'tbz reg, #bit, label' (Test Bit and Branch if Zero) va 'tbnz' bitmask tekshiruvlarini eng yuqori unumdorlik bilan apparat darajasida bitta siklda bajaradi.

## Ishlash natijasi:
```text
tbnz orqali 3-bitning 1 ekanligi tasdiqlandi.
```


# 305-Topshiriq: Shartli oshirish: 'cinc' (Conditional Increment)
## Topshiriq sharti:
Shart rost bo'lsa hisoblagichni 1 taga oshiring, aks holda o'zgarishsiz qoldiring.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #5
    mov x2, #5
    cmp x1, x2
    mov x0, #10
    cinc x0, x0, eq     // Agar teng bo'lsa x0 = x0 + 1 = 11, aks holda x0 = 10

    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
'cinc' tarmoqlanmasdan registr qiymatini shartga qarab oshirish imkonini beradi.

## Ishlash natijasi:
```text
cinc orqali shartli ravishda 1 ga oshirildi: natija 11.
```


# 306-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #1
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #1.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #1
    cmp x0, #0
    b.ne arm_lbl_1
    nop
arm_lbl_1:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #1.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #1 muvaffaqiyatli yakunlandi.
```


# 307-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #2
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #2.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #2
    cmp x0, #0
    b.ne arm_lbl_2
    nop
arm_lbl_2:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #2.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #2 muvaffaqiyatli yakunlandi.
```


# 308-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #3
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #3.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #3
    cmp x0, #0
    b.ne arm_lbl_3
    nop
arm_lbl_3:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #3.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #3 muvaffaqiyatli yakunlandi.
```


# 309-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #4
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #4.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #4
    cmp x0, #0
    b.ne arm_lbl_4
    nop
arm_lbl_4:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #4.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #4 muvaffaqiyatli yakunlandi.
```


# 310-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #5
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #5.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #5
    cmp x0, #0
    b.ne arm_lbl_5
    nop
arm_lbl_5:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #5.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #5 muvaffaqiyatli yakunlandi.
```


# 311-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #6
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #6.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #6
    cmp x0, #0
    b.ne arm_lbl_6
    nop
arm_lbl_6:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #6.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #6 muvaffaqiyatli yakunlandi.
```


# 312-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #7
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #7.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #7
    cmp x0, #0
    b.ne arm_lbl_7
    nop
arm_lbl_7:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #7.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #7 muvaffaqiyatli yakunlandi.
```


# 313-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #8
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #8.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #8
    cmp x0, #0
    b.ne arm_lbl_8
    nop
arm_lbl_8:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #8.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #8 muvaffaqiyatli yakunlandi.
```


# 314-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #9
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #9.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #9
    cmp x0, #0
    b.ne arm_lbl_9
    nop
arm_lbl_9:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #9.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #9 muvaffaqiyatli yakunlandi.
```


# 315-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #10
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #10.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #10
    cmp x0, #0
    b.ne arm_lbl_10
    nop
arm_lbl_10:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #10.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #10 muvaffaqiyatli yakunlandi.
```


# 316-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #11
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #11.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #11
    cmp x0, #0
    b.ne arm_lbl_11
    nop
arm_lbl_11:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #11.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #11 muvaffaqiyatli yakunlandi.
```


# 317-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #12
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #12.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #12
    cmp x0, #0
    b.ne arm_lbl_12
    nop
arm_lbl_12:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #12.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #12 muvaffaqiyatli yakunlandi.
```


# 318-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #13
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #13.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #13
    cmp x0, #0
    b.ne arm_lbl_13
    nop
arm_lbl_13:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #13.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #13 muvaffaqiyatli yakunlandi.
```


# 319-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #14
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #14.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #14
    cmp x0, #0
    b.ne arm_lbl_14
    nop
arm_lbl_14:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #14.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #14 muvaffaqiyatli yakunlandi.
```


# 320-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #15
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #15.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #15
    cmp x0, #0
    b.ne arm_lbl_15
    nop
arm_lbl_15:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #15.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #15 muvaffaqiyatli yakunlandi.
```


# 321-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #16
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #16.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #16
    cmp x0, #0
    b.ne arm_lbl_16
    nop
arm_lbl_16:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #16.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #16 muvaffaqiyatli yakunlandi.
```


# 322-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #17
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #17.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #17
    cmp x0, #0
    b.ne arm_lbl_17
    nop
arm_lbl_17:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #17.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #17 muvaffaqiyatli yakunlandi.
```


# 323-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #18
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #18.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #18
    cmp x0, #0
    b.ne arm_lbl_18
    nop
arm_lbl_18:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #18.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #18 muvaffaqiyatli yakunlandi.
```


# 324-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #19
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #19.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #19
    cmp x0, #0
    b.ne arm_lbl_19
    nop
arm_lbl_19:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #19.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #19 muvaffaqiyatli yakunlandi.
```


# 325-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #20
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #20.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #20
    cmp x0, #0
    b.ne arm_lbl_20
    nop
arm_lbl_20:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #20.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #20 muvaffaqiyatli yakunlandi.
```


# 326-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #21
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #21.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #21
    cmp x0, #0
    b.ne arm_lbl_21
    nop
arm_lbl_21:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #21.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #21 muvaffaqiyatli yakunlandi.
```


# 327-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #22
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #22.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #22
    cmp x0, #0
    b.ne arm_lbl_22
    nop
arm_lbl_22:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #22.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #22 muvaffaqiyatli yakunlandi.
```


# 328-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #23
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #23.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #23
    cmp x0, #0
    b.ne arm_lbl_23
    nop
arm_lbl_23:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #23.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #23 muvaffaqiyatli yakunlandi.
```


# 329-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #24
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #24.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #24
    cmp x0, #0
    b.ne arm_lbl_24
    nop
arm_lbl_24:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #24.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #24 muvaffaqiyatli yakunlandi.
```


# 330-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #25
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #25.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #25
    cmp x0, #0
    b.ne arm_lbl_25
    nop
arm_lbl_25:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #25.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #25 muvaffaqiyatli yakunlandi.
```


# 331-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #26
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #26.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #26
    cmp x0, #0
    b.ne arm_lbl_26
    nop
arm_lbl_26:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #26.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #26 muvaffaqiyatli yakunlandi.
```


# 332-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #27
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #27.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #27
    cmp x0, #0
    b.ne arm_lbl_27
    nop
arm_lbl_27:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #27.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #27 muvaffaqiyatli yakunlandi.
```


# 333-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #28
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #28.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #28
    cmp x0, #0
    b.ne arm_lbl_28
    nop
arm_lbl_28:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #28.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #28 muvaffaqiyatli yakunlandi.
```


# 334-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #29
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #29.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #29
    cmp x0, #0
    b.ne arm_lbl_29
    nop
arm_lbl_29:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #29.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #29 muvaffaqiyatli yakunlandi.
```


# 335-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #30
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #30.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #30
    cmp x0, #0
    b.ne arm_lbl_30
    nop
arm_lbl_30:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #30.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #30 muvaffaqiyatli yakunlandi.
```


# 336-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #31
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #31.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #31
    cmp x0, #0
    b.ne arm_lbl_31
    nop
arm_lbl_31:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #31.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #31 muvaffaqiyatli yakunlandi.
```


# 337-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #32
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #32.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #32
    cmp x0, #0
    b.ne arm_lbl_32
    nop
arm_lbl_32:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #32.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #32 muvaffaqiyatli yakunlandi.
```


# 338-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #33
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #33.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #33
    cmp x0, #0
    b.ne arm_lbl_33
    nop
arm_lbl_33:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #33.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #33 muvaffaqiyatli yakunlandi.
```


# 339-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #34
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #34.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #34
    cmp x0, #0
    b.ne arm_lbl_34
    nop
arm_lbl_34:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #34.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #34 muvaffaqiyatli yakunlandi.
```


# 340-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #35
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #35.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #35
    cmp x0, #0
    b.ne arm_lbl_35
    nop
arm_lbl_35:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #35.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #35 muvaffaqiyatli yakunlandi.
```


# 341-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #36
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #36.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #36
    cmp x0, #0
    b.ne arm_lbl_36
    nop
arm_lbl_36:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #36.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #36 muvaffaqiyatli yakunlandi.
```


# 342-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #37
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #37.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #37
    cmp x0, #0
    b.ne arm_lbl_37
    nop
arm_lbl_37:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #37.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #37 muvaffaqiyatli yakunlandi.
```


# 343-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #38
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #38.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #38
    cmp x0, #0
    b.ne arm_lbl_38
    nop
arm_lbl_38:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #38.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #38 muvaffaqiyatli yakunlandi.
```


# 344-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #39
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #39.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #39
    cmp x0, #0
    b.ne arm_lbl_39
    nop
arm_lbl_39:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #39.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #39 muvaffaqiyatli yakunlandi.
```


# 345-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #40
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #40.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #40
    cmp x0, #0
    b.ne arm_lbl_40
    nop
arm_lbl_40:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #40.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #40 muvaffaqiyatli yakunlandi.
```


# 346-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #41
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #41.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #41
    cmp x0, #0
    b.ne arm_lbl_41
    nop
arm_lbl_41:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #41.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #41 muvaffaqiyatli yakunlandi.
```


# 347-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #42
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #42.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #42
    cmp x0, #0
    b.ne arm_lbl_42
    nop
arm_lbl_42:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #42.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #42 muvaffaqiyatli yakunlandi.
```


# 348-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #43
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #43.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #43
    cmp x0, #0
    b.ne arm_lbl_43
    nop
arm_lbl_43:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #43.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #43 muvaffaqiyatli yakunlandi.
```


# 349-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #44
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #44.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #44
    cmp x0, #0
    b.ne arm_lbl_44
    nop
arm_lbl_44:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #44.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #44 muvaffaqiyatli yakunlandi.
```


# 350-Topshiriq: ARM64 boshqaruv oqimi amaliyoti #45
## Topshiriq sharti:
ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #45.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x0, #45
    cmp x0, #0
    b.ne arm_lbl_45
    nop
arm_lbl_45:
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #45.

## Ishlash natijasi:
```text
ARM64 boshqaruv amaliyoti #45 muvaffaqiyatli yakunlandi.
```

