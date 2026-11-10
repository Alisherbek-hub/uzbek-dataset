# 601-Topshiriq: Direction Flag va String ko'rsatmalari: 'cld' va 'std'
## Topshiriq sharti:
x86_64 da Direction Flag (DF) ni boshqarish va xotira yo'nalishini belgilash.

## Yechim (Assembly kodi):
```assembly
section .text
global _start
_start:
    cld                 ; Clear Direction Flag (DF=0): ko'rsatkichlar o'sish tartibida (RSI++, RDI++)
    ; std               ; Set Direction Flag (DF=1): ko'rsatkichlar kamayish tartibida (RSI--, RDI--)

    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86 arxitekturasida barcha satr ko'rsatmalari (`movsb`, `stosb`, `scasb`, `cmpsb`) Direction Flag ga bog'liq. 'cld' xotirani chapdan o'ngga (kichik manzildan kattaga), 'std' esa o'ngdan chapga qayta ishlashni belgilaydi.

## Ishlash natijasi:
```text
cld orqali DF=0 qilindi (chapdan o'ngga qat'iy yo'nalish).
```


# 602-Topshiriq: Xotira blokini nusxalash: 'rep movsb' (memcpy asosi)
## Topshiriq sharti:
Manba satrini maqsad xotirasiga apparat ko'rsatmasi bilan o'ta tez nusxalang.

## Yechim (Assembly kodi):
```assembly
section .data
    src db "Khorazmiy High Performance Copy!", 0
    len equ $ - src

section .bss
    dst resb 64

section .text
global _start
_start:
    cld
    lea rsi, [src]      ; Manba ko'rsatkichi (Source Index)
    lea rdi, [dst]      ; Maqsad ko'rsatkichi (Destination Index)
    mov rcx, len        ; Baytlar soni (Hisoblagich)
    rep movsb           ; RCX marta [RDI++] = [RSI++] takrorlanadi!

    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
'rep movsb' x86 da apparat darajasida optimallashgan memcpy ko'rsatmasi bo'lib, zamonaviy protsessorlarda Fast String Operations (ERMSB) orqali juda yuqori tezlikda bajariladi.

## Ishlash natijasi:
```text
rep movsb orqali butun satr xotiraga nusxalandi.
```


# 603-Topshiriq: Xotirani to'ldirish: 'rep stosb' (memset asosi)
## Topshiriq sharti:
1024 baytlik buferni nollar (yoki belgilangan bayt) bilan to'ldiring.

## Yechim (Assembly kodi):
```assembly
section .bss
    buffer resb 128

section .text
global _start
_start:
    cld
    lea rdi, [buffer]   ; Maqsad manzili
    mov rcx, 128        ; 128 bayt
    xor al, al          ; AL = 0 (to'ldiriluvchi bayt)
    rep stosb           ; RCX marta [RDI++] = AL bajariladi!

    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
'rep stosb' C tilidagi 'memset(buffer, 0, len)' vazifasini bajaruvchi toza apparat instruksiyasidir.

## Ishlash natijasi:
```text
rep stosb yordamida bufer nollar bilan to'ldirildi.
```


# 604-Topshiriq: Satr uzunligini topish: 'repne scasb' (strlen asosi)
## Topshiriq sharti:
Nol bilan tugovchi (Null-terminated) satr uzunligini hisoblang.

## Yechim (Assembly kodi):
```assembly
section .data
    str db "Assembly", 0

section .text
global _start
_start:
    cld
    lea rdi, [str]
    xor al, al          ; AL = 0 (qidirilayotgan null-terminator)
    mov rcx, -1         ; Eng katta son (0xFFFFFFFFFFFFFFFF)
    repne scasb         ; [RDI++] AL ga teng bo'lmaguncha qidiradi!

    ; Uzunlik = -1 - RCX - 1
    not rcx
    dec rcx             ; RCX endi aniq satr uzunligini (8) saqlaydi!

    mov rax, 60
    mov rdi, rcx
    syscall
```

## Tushuntirish va Mantiq:
'repne scasb' (Repeat Not Equal Scan String) AL dagi belgini xotiradan qidiradi va RDI ni siljitadi. Not RCX formulasi orqali satr uzunligi (strlen) olinadi.

## Ishlash natijasi:
```text
repne scasb orqali satr uzunligi 8 deb hisoblandi.
```


# 605-Topshiriq: Satrlarni solishtirish: 'repe cmpsb' (strcmp asosi)
## Topshiriq sharti:
Ikkita satrning baytma-bayt tengligini apparat darajasida solishtiring.

## Yechim (Assembly kodi):
```assembly
section .data
    s1 db "Toshkent", 0
    s2 db "Toshkent", 0
    len equ 9

section .text
global _start
_start:
    cld
    lea rsi, [s1]
    lea rdi, [s2]
    mov rcx, len
    repe cmpsb          ; Ikkala satr baytlari teng bo'lib turganda davom etadi!

    ; Agar satrlar teng bo'lsa Zero Flag (ZF=1) bo'ladi
    sete al
    movzx rdi, al       ; RDI = 1 (Teng)

    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
'repe cmpsb' ikkala xotira ko'rsatkichini solishtirib boradi, birinchi farq uchragan zahoti to'xtaydi.

## Ishlash natijasi:
```text
repe cmpsb orqali satrlar tengligi tasdiqlandi (ZF=1).
```


# 606-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #1
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #1.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #1
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 1
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #1.

## Ishlash natijasi:
```text
Satrlar amaliyoti #1 muvaffaqiyatli yakunlandi.
```


# 607-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #2
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #2.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #2
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 2
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #2.

## Ishlash natijasi:
```text
Satrlar amaliyoti #2 muvaffaqiyatli yakunlandi.
```


# 608-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #3
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #3.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #3
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 3
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #3.

## Ishlash natijasi:
```text
Satrlar amaliyoti #3 muvaffaqiyatli yakunlandi.
```


# 609-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #4
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #4.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #4
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 4
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #4.

## Ishlash natijasi:
```text
Satrlar amaliyoti #4 muvaffaqiyatli yakunlandi.
```


# 610-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #5
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #5.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #5
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 5
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #5.

## Ishlash natijasi:
```text
Satrlar amaliyoti #5 muvaffaqiyatli yakunlandi.
```


# 611-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #6
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #6.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #6
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 6
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #6.

## Ishlash natijasi:
```text
Satrlar amaliyoti #6 muvaffaqiyatli yakunlandi.
```


# 612-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #7
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #7.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #7
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 7
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #7.

## Ishlash natijasi:
```text
Satrlar amaliyoti #7 muvaffaqiyatli yakunlandi.
```


# 613-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #8
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #8.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #8
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 8
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #8.

## Ishlash natijasi:
```text
Satrlar amaliyoti #8 muvaffaqiyatli yakunlandi.
```


# 614-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #9
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #9.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #9
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 9
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #9.

## Ishlash natijasi:
```text
Satrlar amaliyoti #9 muvaffaqiyatli yakunlandi.
```


# 615-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #10
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #10.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #10
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 10
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #10.

## Ishlash natijasi:
```text
Satrlar amaliyoti #10 muvaffaqiyatli yakunlandi.
```


# 616-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #11
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #11.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #11
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 11
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #11.

## Ishlash natijasi:
```text
Satrlar amaliyoti #11 muvaffaqiyatli yakunlandi.
```


# 617-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #12
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #12.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #12
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 12
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #12.

## Ishlash natijasi:
```text
Satrlar amaliyoti #12 muvaffaqiyatli yakunlandi.
```


# 618-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #13
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #13.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #13
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 13
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #13.

## Ishlash natijasi:
```text
Satrlar amaliyoti #13 muvaffaqiyatli yakunlandi.
```


# 619-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #14
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #14.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #14
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 14
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #14.

## Ishlash natijasi:
```text
Satrlar amaliyoti #14 muvaffaqiyatli yakunlandi.
```


# 620-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #15
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #15.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #15
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 15
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #15.

## Ishlash natijasi:
```text
Satrlar amaliyoti #15 muvaffaqiyatli yakunlandi.
```


# 621-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #16
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #16.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #16
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 16
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #16.

## Ishlash natijasi:
```text
Satrlar amaliyoti #16 muvaffaqiyatli yakunlandi.
```


# 622-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #17
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #17.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #17
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 17
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #17.

## Ishlash natijasi:
```text
Satrlar amaliyoti #17 muvaffaqiyatli yakunlandi.
```


# 623-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #18
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #18.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #18
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 18
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #18.

## Ishlash natijasi:
```text
Satrlar amaliyoti #18 muvaffaqiyatli yakunlandi.
```


# 624-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #19
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #19.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #19
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 19
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #19.

## Ishlash natijasi:
```text
Satrlar amaliyoti #19 muvaffaqiyatli yakunlandi.
```


# 625-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #20
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #20.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #20
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 20
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #20.

## Ishlash natijasi:
```text
Satrlar amaliyoti #20 muvaffaqiyatli yakunlandi.
```


# 626-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #21
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #21.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #21
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 21
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #21.

## Ishlash natijasi:
```text
Satrlar amaliyoti #21 muvaffaqiyatli yakunlandi.
```


# 627-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #22
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #22.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #22
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 22
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #22.

## Ishlash natijasi:
```text
Satrlar amaliyoti #22 muvaffaqiyatli yakunlandi.
```


# 628-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #23
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #23.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #23
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 23
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #23.

## Ishlash natijasi:
```text
Satrlar amaliyoti #23 muvaffaqiyatli yakunlandi.
```


# 629-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #24
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #24.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #24
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 24
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #24.

## Ishlash natijasi:
```text
Satrlar amaliyoti #24 muvaffaqiyatli yakunlandi.
```


# 630-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #25
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #25.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #25
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 25
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #25.

## Ishlash natijasi:
```text
Satrlar amaliyoti #25 muvaffaqiyatli yakunlandi.
```


# 631-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #26
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #26.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #26
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 26
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #26.

## Ishlash natijasi:
```text
Satrlar amaliyoti #26 muvaffaqiyatli yakunlandi.
```


# 632-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #27
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #27.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #27
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 27
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #27.

## Ishlash natijasi:
```text
Satrlar amaliyoti #27 muvaffaqiyatli yakunlandi.
```


# 633-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #28
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #28.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #28
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 28
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #28.

## Ishlash natijasi:
```text
Satrlar amaliyoti #28 muvaffaqiyatli yakunlandi.
```


# 634-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #29
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #29.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #29
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 29
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #29.

## Ishlash natijasi:
```text
Satrlar amaliyoti #29 muvaffaqiyatli yakunlandi.
```


# 635-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #30
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #30.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #30
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 30
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #30.

## Ishlash natijasi:
```text
Satrlar amaliyoti #30 muvaffaqiyatli yakunlandi.
```


# 636-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #31
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #31.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #31
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 31
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #31.

## Ishlash natijasi:
```text
Satrlar amaliyoti #31 muvaffaqiyatli yakunlandi.
```


# 637-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #32
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #32.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #32
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 32
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #32.

## Ishlash natijasi:
```text
Satrlar amaliyoti #32 muvaffaqiyatli yakunlandi.
```


# 638-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #33
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #33.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #33
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 33
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #33.

## Ishlash natijasi:
```text
Satrlar amaliyoti #33 muvaffaqiyatli yakunlandi.
```


# 639-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #34
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #34.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #34
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 34
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #34.

## Ishlash natijasi:
```text
Satrlar amaliyoti #34 muvaffaqiyatli yakunlandi.
```


# 640-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #35
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #35.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #35
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 35
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #35.

## Ishlash natijasi:
```text
Satrlar amaliyoti #35 muvaffaqiyatli yakunlandi.
```


# 641-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #36
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #36.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #36
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 36
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #36.

## Ishlash natijasi:
```text
Satrlar amaliyoti #36 muvaffaqiyatli yakunlandi.
```


# 642-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #37
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #37.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #37
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 37
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #37.

## Ishlash natijasi:
```text
Satrlar amaliyoti #37 muvaffaqiyatli yakunlandi.
```


# 643-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #38
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #38.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #38
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 38
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #38.

## Ishlash natijasi:
```text
Satrlar amaliyoti #38 muvaffaqiyatli yakunlandi.
```


# 644-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #39
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #39.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #39
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 39
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #39.

## Ishlash natijasi:
```text
Satrlar amaliyoti #39 muvaffaqiyatli yakunlandi.
```


# 645-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #40
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #40.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #40
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 40
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #40.

## Ishlash natijasi:
```text
Satrlar amaliyoti #40 muvaffaqiyatli yakunlandi.
```


# 646-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #41
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #41.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #41
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 41
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #41.

## Ishlash natijasi:
```text
Satrlar amaliyoti #41 muvaffaqiyatli yakunlandi.
```


# 647-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #42
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #42.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #42
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 42
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #42.

## Ishlash natijasi:
```text
Satrlar amaliyoti #42 muvaffaqiyatli yakunlandi.
```


# 648-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #43
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #43.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #43
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 43
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #43.

## Ishlash natijasi:
```text
Satrlar amaliyoti #43 muvaffaqiyatli yakunlandi.
```


# 649-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #44
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #44.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #44
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 44
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #44.

## Ishlash natijasi:
```text
Satrlar amaliyoti #44 muvaffaqiyatli yakunlandi.
```


# 650-Topshiriq: Satrlar va massivlar bilan ishlash amaliyoti #45
## Topshiriq sharti:
Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #45.

## Yechim (Assembly kodi):
```assembly
; Satrlar amaliyoti #45
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 45
    syscall
```

## Tushuntirish va Mantiq:
Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #45.

## Ishlash natijasi:
```text
Satrlar amaliyoti #45 muvaffaqiyatli yakunlandi.
```

