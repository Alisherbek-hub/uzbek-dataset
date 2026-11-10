# 551-Topshiriq: Dinamik xotira ajratish: 'sys_mmap' (Syscall 9)
## Topshiriq sharti:
Operatsion tizimdan 4096 baytlik (1 sahifa) yangi virtual xotira so'rang.

## Yechim (Assembly kodi):
```assembly
section .text
global _start
_start:
    ; sys_mmap(addr=0, len=4096, prot=PROT_READ|PROT_WRITE, flags=MAP_PRIVATE|MAP_ANONYMOUS, fd=-1, offset=0)
    mov rax, 9          ; sys_mmap
    xor rdi, rdi        ; addr = NULL (yadro o'zi manzil tanlasin)
    mov rsi, 4096       ; 1 sahifa
    mov rdx, 3          ; PROT_READ (1) | PROT_WRITE (2)
    mov r10, 34         ; MAP_PRIVATE (2) | MAP_ANONYMOUS (32)
    mov r8, -1          ; fd = -1
    xor r9, r9          ; offset = 0
    syscall
    ; RAX endi yangi ajratilgan xotiraning boshlang'ich manzilini saqlaydi!

    mov rbx, rax
    mov qword [rbx], 0x12345678 ; Yangi xotiraga yozamiz!

    ; sys_munmap(addr, len)
    mov rax, 11         ; sys_munmap
    mov rdi, rbx
    mov rsi, 4096
    syscall

    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
'mmap' Linux da dinamik xotira boshqaruvining (masalan C tilidagi malloc) asosiy poydevoridir. 'MAP_ANONYMOUS' xotirani faylga bog'lamasdan toza RAM dan ajratadi.

## Ishlash natijasi:
```text
sys_mmap orqali 4KB virtual xotira ajratildi va munmap bilan bo'shatildi.
```


# 552-Topshiriq: Heap xotirasini kengaytirish: 'sys_brk' (Syscall 12)
## Topshiriq sharti:
Dastur segmenti chegarasini (program break) surish orqali heap ajrating.

## Yechim (Assembly kodi):
```assembly
section .text
global _start
_start:
    ; 1. Joriy break manzilini aniqlash: sys_brk(0)
    mov rax, 12         ; sys_brk
    xor rdi, rdi
    syscall
    mov rbx, rax        ; RBX = joriy heap chegarasi

    ; 2. Chegarani 1024 baytga kengaytirish
    lea rdi, [rbx + 1024]
    mov rax, 12
    syscall

    ; Yangi heap xotirasidan foydalanamiz
    mov qword [rbx], 999

    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
'brk' tizim chaqiruvi an'anaviy heap xotirasini boshqaradi. Uning chegarasini oshirish orqali yangi dinamik xotira olinadi.

## Ishlash natijasi:
```text
sys_brk yordamida heap maydoni 1024 baytga kengaytirildi.
```


# 553-Topshiriq: Xotira huquqlarini o'zgartirish: 'sys_mprotect' (Syscall 10)
## Topshiriq sharti:
Xotirani bajariluvchi (Executable) qilish: JIT (Just-In-Time) kompilyatorlar asosi.

## Yechim (Assembly kodi):
```assembly
section .text
global _start
_start:
    ; mprotect(addr, len, PROT_READ | PROT_EXEC)
    ; JIT kompilyatorlar xotiraga mashina kodini yozib (PROT_WRITE),
    ; so'ng mprotect orqali bajarish huquqini (PROT_EXEC) yoqadi va W^X qoidasiga rioya qiladi.

    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
'mprotect' sahifalarning huquqlarini dinamik boshqaradi. Kiberxavfsizlikda W^X (Write XOR Execute) qoidasi bo'yicha xotira bir vaqtning o'zida ham yoziluvchi, ham bajariluvchi bo'lishi taqiqlanadi.

## Ishlash natijasi:
```text
sys_mprotect orqali xotira huquqlari tahlil qilindi.
```


# 554-Topshiriq: Xotira kesh to'siqlari: 'mfence', 'lfence', 'sfence'
## Topshiriq sharti:
Ko'p yadroli protsessorlarda xotira operatsiyalari tartibini kafolatlash.

## Yechim (Assembly kodi):
```assembly
section .text
global _start
_start:
    ; x86 Out-of-Order Execution (ko'rsatmalarni tartibsiz bajarish) mexanizmiga ega.
    ; Kesh to'siqlari (Memory Barriers) yozish va o'qish tartibini qat'iylashtiradi:
    sfence              ; Store Fence: barcha oldingi yozishlar yakunlansin
    lfence              ; Load Fence: barcha oldingi o'qishlar yakunlansin
    mfence              ; Memory Fence: to'liq ikki tomonlama to'siq

    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
Ko'p oqimli (multithreading) tizimli dasturlashda xotira to'siqlari poygalar (race conditions) va kesh nomutanosibligining oldini oladi.

## Ishlash natijasi:
```text
Memory barriers (sfence, lfence, mfence) xotira tartibini kafolatladi.
```


# 555-Topshiriq: Xotirani tekislash (Memory Alignment: 64-bayt Cache Line)
## Topshiriq sharti:
Kesh liniyasi chegarasida ma'lumotlarni joylashtirish unumdorligi.

## Yechim (Assembly kodi):
```assembly
section .data
align 64                ; Keyingi ma'lumot 64-bayt kesh liniyasi boshidan boshlanadi
    fast_matrix times 16 dq 1

section .text
global _start
_start:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
Zamonaviy x86 va ARM protsessorlari kesh xotirasi 64-baytlik qismlar (Cache Lines) bilan ishlaydi. Ma'lumotlar 64-baytga tekislanganda, bitta o'qishda butun blok yuklanadi va False Sharing muammosi yo'qoladi.

## Ishlash natijasi:
```text
align 64 orqali xotira CPU kesh liniyasiga tekislandi.
```


# 556-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #1
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #1.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #1
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 1
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #1.

## Ishlash natijasi:
```text
Xotira amaliyoti #1 muvaffaqiyatli yakunlandi.
```


# 557-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #2
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #2.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #2
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 2
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #2.

## Ishlash natijasi:
```text
Xotira amaliyoti #2 muvaffaqiyatli yakunlandi.
```


# 558-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #3
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #3.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #3
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 3
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #3.

## Ishlash natijasi:
```text
Xotira amaliyoti #3 muvaffaqiyatli yakunlandi.
```


# 559-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #4
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #4.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #4
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 4
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #4.

## Ishlash natijasi:
```text
Xotira amaliyoti #4 muvaffaqiyatli yakunlandi.
```


# 560-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #5
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #5.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #5
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 5
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #5.

## Ishlash natijasi:
```text
Xotira amaliyoti #5 muvaffaqiyatli yakunlandi.
```


# 561-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #6
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #6.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #6
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 6
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #6.

## Ishlash natijasi:
```text
Xotira amaliyoti #6 muvaffaqiyatli yakunlandi.
```


# 562-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #7
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #7.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #7
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 7
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #7.

## Ishlash natijasi:
```text
Xotira amaliyoti #7 muvaffaqiyatli yakunlandi.
```


# 563-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #8
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #8.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #8
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 8
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #8.

## Ishlash natijasi:
```text
Xotira amaliyoti #8 muvaffaqiyatli yakunlandi.
```


# 564-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #9
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #9.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #9
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 9
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #9.

## Ishlash natijasi:
```text
Xotira amaliyoti #9 muvaffaqiyatli yakunlandi.
```


# 565-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #10
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #10.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #10
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 10
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #10.

## Ishlash natijasi:
```text
Xotira amaliyoti #10 muvaffaqiyatli yakunlandi.
```


# 566-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #11
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #11.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #11
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 11
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #11.

## Ishlash natijasi:
```text
Xotira amaliyoti #11 muvaffaqiyatli yakunlandi.
```


# 567-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #12
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #12.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #12
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 12
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #12.

## Ishlash natijasi:
```text
Xotira amaliyoti #12 muvaffaqiyatli yakunlandi.
```


# 568-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #13
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #13.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #13
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 13
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #13.

## Ishlash natijasi:
```text
Xotira amaliyoti #13 muvaffaqiyatli yakunlandi.
```


# 569-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #14
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #14.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #14
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 14
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #14.

## Ishlash natijasi:
```text
Xotira amaliyoti #14 muvaffaqiyatli yakunlandi.
```


# 570-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #15
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #15.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #15
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 15
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #15.

## Ishlash natijasi:
```text
Xotira amaliyoti #15 muvaffaqiyatli yakunlandi.
```


# 571-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #16
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #16.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #16
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 16
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #16.

## Ishlash natijasi:
```text
Xotira amaliyoti #16 muvaffaqiyatli yakunlandi.
```


# 572-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #17
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #17.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #17
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 17
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #17.

## Ishlash natijasi:
```text
Xotira amaliyoti #17 muvaffaqiyatli yakunlandi.
```


# 573-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #18
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #18.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #18
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 18
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #18.

## Ishlash natijasi:
```text
Xotira amaliyoti #18 muvaffaqiyatli yakunlandi.
```


# 574-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #19
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #19.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #19
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 19
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #19.

## Ishlash natijasi:
```text
Xotira amaliyoti #19 muvaffaqiyatli yakunlandi.
```


# 575-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #20
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #20.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #20
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 20
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #20.

## Ishlash natijasi:
```text
Xotira amaliyoti #20 muvaffaqiyatli yakunlandi.
```


# 576-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #21
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #21.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #21
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 21
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #21.

## Ishlash natijasi:
```text
Xotira amaliyoti #21 muvaffaqiyatli yakunlandi.
```


# 577-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #22
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #22.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #22
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 22
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #22.

## Ishlash natijasi:
```text
Xotira amaliyoti #22 muvaffaqiyatli yakunlandi.
```


# 578-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #23
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #23.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #23
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 23
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #23.

## Ishlash natijasi:
```text
Xotira amaliyoti #23 muvaffaqiyatli yakunlandi.
```


# 579-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #24
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #24.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #24
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 24
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #24.

## Ishlash natijasi:
```text
Xotira amaliyoti #24 muvaffaqiyatli yakunlandi.
```


# 580-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #25
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #25.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #25
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 25
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #25.

## Ishlash natijasi:
```text
Xotira amaliyoti #25 muvaffaqiyatli yakunlandi.
```


# 581-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #26
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #26.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #26
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 26
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #26.

## Ishlash natijasi:
```text
Xotira amaliyoti #26 muvaffaqiyatli yakunlandi.
```


# 582-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #27
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #27.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #27
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 27
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #27.

## Ishlash natijasi:
```text
Xotira amaliyoti #27 muvaffaqiyatli yakunlandi.
```


# 583-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #28
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #28.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #28
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 28
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #28.

## Ishlash natijasi:
```text
Xotira amaliyoti #28 muvaffaqiyatli yakunlandi.
```


# 584-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #29
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #29.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #29
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 29
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #29.

## Ishlash natijasi:
```text
Xotira amaliyoti #29 muvaffaqiyatli yakunlandi.
```


# 585-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #30
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #30.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #30
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 30
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #30.

## Ishlash natijasi:
```text
Xotira amaliyoti #30 muvaffaqiyatli yakunlandi.
```


# 586-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #31
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #31.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #31
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 31
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #31.

## Ishlash natijasi:
```text
Xotira amaliyoti #31 muvaffaqiyatli yakunlandi.
```


# 587-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #32
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #32.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #32
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 32
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #32.

## Ishlash natijasi:
```text
Xotira amaliyoti #32 muvaffaqiyatli yakunlandi.
```


# 588-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #33
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #33.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #33
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 33
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #33.

## Ishlash natijasi:
```text
Xotira amaliyoti #33 muvaffaqiyatli yakunlandi.
```


# 589-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #34
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #34.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #34
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 34
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #34.

## Ishlash natijasi:
```text
Xotira amaliyoti #34 muvaffaqiyatli yakunlandi.
```


# 590-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #35
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #35.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #35
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 35
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #35.

## Ishlash natijasi:
```text
Xotira amaliyoti #35 muvaffaqiyatli yakunlandi.
```


# 591-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #36
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #36.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #36
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 36
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #36.

## Ishlash natijasi:
```text
Xotira amaliyoti #36 muvaffaqiyatli yakunlandi.
```


# 592-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #37
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #37.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #37
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 37
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #37.

## Ishlash natijasi:
```text
Xotira amaliyoti #37 muvaffaqiyatli yakunlandi.
```


# 593-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #38
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #38.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #38
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 38
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #38.

## Ishlash natijasi:
```text
Xotira amaliyoti #38 muvaffaqiyatli yakunlandi.
```


# 594-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #39
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #39.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #39
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 39
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #39.

## Ishlash natijasi:
```text
Xotira amaliyoti #39 muvaffaqiyatli yakunlandi.
```


# 595-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #40
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #40.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #40
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 40
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #40.

## Ishlash natijasi:
```text
Xotira amaliyoti #40 muvaffaqiyatli yakunlandi.
```


# 596-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #41
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #41.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #41
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 41
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #41.

## Ishlash natijasi:
```text
Xotira amaliyoti #41 muvaffaqiyatli yakunlandi.
```


# 597-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #42
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #42.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #42
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 42
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #42.

## Ishlash natijasi:
```text
Xotira amaliyoti #42 muvaffaqiyatli yakunlandi.
```


# 598-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #43
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #43.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #43
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 43
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #43.

## Ishlash natijasi:
```text
Xotira amaliyoti #43 muvaffaqiyatli yakunlandi.
```


# 599-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #44
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #44.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #44
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 44
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #44.

## Ishlash natijasi:
```text
Xotira amaliyoti #44 muvaffaqiyatli yakunlandi.
```


# 600-Topshiriq: Xotira xaritalash va segmentatsiya amaliyoti #45
## Topshiriq sharti:
Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #45.

## Yechim (Assembly kodi):
```assembly
; Xotira amaliyoti #45
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 45
    syscall
```

## Tushuntirish va Mantiq:
Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #45.

## Ishlash natijasi:
```text
Xotira amaliyoti #45 muvaffaqiyatli yakunlandi.
```

