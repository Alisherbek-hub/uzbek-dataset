# 351-Topshiriq: x86_64 Stek arxitekturasi: 'push' va 'pop'
## Topshiriq sharti:
LIFO (Last In First Out) tartibida registrlar qiymatini saqlash va tiklash.

## Yechim (Assembly kodi):
```assembly
section .text
global _start
_start:
    mov rax, 0xAAAA
    mov rbx, 0xBBBB

    push rax            ; RSP = RSP - 8, [RSP] = 0xAAAA
    push rbx            ; RSP = RSP - 8, [RSP] = 0xBBBB

    pop rcx             ; RCX = 0xBBBB (eng oxirgi tushgan birinchi chiqadi!)
    pop rdx             ; RDX = 0xAAAA

    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 da stek yuqori manzillardan pastki manzillarga qarab (High to Low) o'sadi. 'push' qilinganda RSP 8 baytga kamayadi, 'pop' da esa 8 baytga oshadi.

## Ishlash natijasi:
```text
push va pop orqali LIFO tamoyili muvaffaqiyatli isbotlandi.
```


# 352-Topshiriq: Funksiya chaqiruvi: 'call' va 'ret'
## Topshiriq sharti:
Funksiyaga o'tish va qaytish manzilini stek orqali boshqarish.

## Yechim (Assembly kodi):
```assembly
section .text
global _start

my_func:
    add rax, 10
    ret                 ; Stekdan qaytish manzilini (RIP) olib, o'sha manzilga sakraydi

_start:
    mov rax, 40
    call my_func        ; Qaytish manzilini stekka yozadi va my_func ga sakraydi
    ; rax endi 50 bo'ldi!

    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
'call' buyrug'i keyingi ko'rsatmaning manzilini (Return Address) avtomatik ravishda stekka push qiladi. 'ret' esa ushbu manzilni stekdan pop qilib, RIP ga yuklaydi.

## Ishlash natijasi:
```text
call va ret orqali funksiya chaqirildi va muvaffaqiyatli qaytildi.
```


# 353-Topshiriq: Funksiya Prologue va Epilogue (Stack Frame)
## Topshiriq sharti:
RBP (Base Pointer) orqali xavfsiz stek freymini yaratish va tiklash.

## Yechim (Assembly kodi):
```assembly
section .text
global _start

calculate:
    ; === Prologue ===
    push rbp            ; Eski RBP ni saqlaymiz
    mov rbp, rsp        ; Yangi fream bazasini o'rnatamiz
    sub rsp, 16         ; 16 bayt lokal o'zgaruvchilar uchun joy ajratamiz

    ; Lokal o'zgaruvchilarga murojaat:
    mov qword [rbp - 8], 25

    ; === Epilogue ===
    mov rsp, rbp        ; Stekni tiklaymiz
    pop rbp             ; Eski RBP ni qaytaramiz
    ret

_start:
    call calculate
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
Prologue va Epilogue funksiyalar chaqirilganda stekning buzilmasligini va lokal o'zgaruvchilar xavfsiz joylashishini ta'minlovchi arxitekturaviy qolipdir.

## Ishlash natijasi:
```text
Stack Frame (Prologue va Epilogue) to'g'ri o'rnatildi va tiklandi.
```


# 354-Topshiriq: Ixcham xotima: 'leave' ko'rsatmasi
## Topshiriq sharti:
Prologue da ajratilgan stek freamini bitta 'leave' buyrug'i bilan tiklash.

## Yechim (Assembly kodi):
```assembly
section .text
global _start

sub_routine:
    push rbp
    mov rbp, rsp
    sub rsp, 32

    ; 'leave' amali aynan quyidagiga teng:
    ; mov rsp, rbp
    ; pop rbp
    leave
    ret

_start:
    call sub_routine
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
'leave' buyrug'i x86 da freamni yopish uchun maxsus kiritilgan bo'lib, 'mov rsp, rbp' va 'pop rbp' o'rnini bitta 1 baytlik instruksiya bilan bosadi.

## Ishlash natijasi:
```text
leave buyrug'i yordamida stek freymi tozalandi.
```


# 355-Topshiriq: 16-baytlik Stek Alignment talabi (ABI)
## Topshiriq sharti:
Nega 'call' dan oldin RSP 16 ga karrali bo'lishi shartligi.

## Yechim (Assembly kodi):
```assembly
section .text
global _start
_start:
    ; System V AMD64 ABI talabi:
    ; Funksiya chaqirilayotgan lahzada (call dan oldin) RSP 16 ga karrali bo'lishi SHART!
    ; 'call' ning o'zi 8 baytlik qaytish manzilini yozgani uchun, funksiya ichiga
    ; kirganda RSP har doim 8 ga karrali bo'lib qoladi.
    ; Shuning uchun 'push rbp' (yana 8 bayt) qilinganda RSP yana 16 ga tekislanadi!

    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
Agar stek 16-baytga tekislanmagan bo'lsa, SSE/AVX vektorli ko'rsatmalar (movaps kabi) va C kutubxonasi funksiyalari General Protection Fault (#GP) beradi.

## Ishlash natijasi:
```text
16-baytlik Stack Alignment qoidasi tahlil qilindi.
```


# 356-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #1
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #1.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #1
section .text
global _start
_start:
    push 1
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #1.

## Ishlash natijasi:
```text
Stek amaliyoti #1 muvaffaqiyatli yakunlandi.
```


# 357-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #2
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #2.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #2
section .text
global _start
_start:
    push 2
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #2.

## Ishlash natijasi:
```text
Stek amaliyoti #2 muvaffaqiyatli yakunlandi.
```


# 358-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #3
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #3.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #3
section .text
global _start
_start:
    push 3
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #3.

## Ishlash natijasi:
```text
Stek amaliyoti #3 muvaffaqiyatli yakunlandi.
```


# 359-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #4
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #4.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #4
section .text
global _start
_start:
    push 4
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #4.

## Ishlash natijasi:
```text
Stek amaliyoti #4 muvaffaqiyatli yakunlandi.
```


# 360-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #5
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #5.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #5
section .text
global _start
_start:
    push 5
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #5.

## Ishlash natijasi:
```text
Stek amaliyoti #5 muvaffaqiyatli yakunlandi.
```


# 361-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #6
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #6.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #6
section .text
global _start
_start:
    push 6
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #6.

## Ishlash natijasi:
```text
Stek amaliyoti #6 muvaffaqiyatli yakunlandi.
```


# 362-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #7
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #7.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #7
section .text
global _start
_start:
    push 7
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #7.

## Ishlash natijasi:
```text
Stek amaliyoti #7 muvaffaqiyatli yakunlandi.
```


# 363-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #8
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #8.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #8
section .text
global _start
_start:
    push 8
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #8.

## Ishlash natijasi:
```text
Stek amaliyoti #8 muvaffaqiyatli yakunlandi.
```


# 364-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #9
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #9.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #9
section .text
global _start
_start:
    push 9
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #9.

## Ishlash natijasi:
```text
Stek amaliyoti #9 muvaffaqiyatli yakunlandi.
```


# 365-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #10
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #10.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #10
section .text
global _start
_start:
    push 10
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #10.

## Ishlash natijasi:
```text
Stek amaliyoti #10 muvaffaqiyatli yakunlandi.
```


# 366-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #11
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #11.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #11
section .text
global _start
_start:
    push 11
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #11.

## Ishlash natijasi:
```text
Stek amaliyoti #11 muvaffaqiyatli yakunlandi.
```


# 367-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #12
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #12.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #12
section .text
global _start
_start:
    push 12
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #12.

## Ishlash natijasi:
```text
Stek amaliyoti #12 muvaffaqiyatli yakunlandi.
```


# 368-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #13
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #13.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #13
section .text
global _start
_start:
    push 13
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #13.

## Ishlash natijasi:
```text
Stek amaliyoti #13 muvaffaqiyatli yakunlandi.
```


# 369-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #14
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #14.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #14
section .text
global _start
_start:
    push 14
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #14.

## Ishlash natijasi:
```text
Stek amaliyoti #14 muvaffaqiyatli yakunlandi.
```


# 370-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #15
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #15.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #15
section .text
global _start
_start:
    push 15
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #15.

## Ishlash natijasi:
```text
Stek amaliyoti #15 muvaffaqiyatli yakunlandi.
```


# 371-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #16
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #16.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #16
section .text
global _start
_start:
    push 16
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #16.

## Ishlash natijasi:
```text
Stek amaliyoti #16 muvaffaqiyatli yakunlandi.
```


# 372-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #17
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #17.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #17
section .text
global _start
_start:
    push 17
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #17.

## Ishlash natijasi:
```text
Stek amaliyoti #17 muvaffaqiyatli yakunlandi.
```


# 373-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #18
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #18.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #18
section .text
global _start
_start:
    push 18
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #18.

## Ishlash natijasi:
```text
Stek amaliyoti #18 muvaffaqiyatli yakunlandi.
```


# 374-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #19
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #19.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #19
section .text
global _start
_start:
    push 19
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #19.

## Ishlash natijasi:
```text
Stek amaliyoti #19 muvaffaqiyatli yakunlandi.
```


# 375-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #20
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #20.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #20
section .text
global _start
_start:
    push 20
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #20.

## Ishlash natijasi:
```text
Stek amaliyoti #20 muvaffaqiyatli yakunlandi.
```


# 376-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #21
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #21.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #21
section .text
global _start
_start:
    push 21
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #21.

## Ishlash natijasi:
```text
Stek amaliyoti #21 muvaffaqiyatli yakunlandi.
```


# 377-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #22
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #22.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #22
section .text
global _start
_start:
    push 22
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #22.

## Ishlash natijasi:
```text
Stek amaliyoti #22 muvaffaqiyatli yakunlandi.
```


# 378-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #23
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #23.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #23
section .text
global _start
_start:
    push 23
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #23.

## Ishlash natijasi:
```text
Stek amaliyoti #23 muvaffaqiyatli yakunlandi.
```


# 379-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #24
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #24.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #24
section .text
global _start
_start:
    push 24
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #24.

## Ishlash natijasi:
```text
Stek amaliyoti #24 muvaffaqiyatli yakunlandi.
```


# 380-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #25
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #25.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #25
section .text
global _start
_start:
    push 25
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #25.

## Ishlash natijasi:
```text
Stek amaliyoti #25 muvaffaqiyatli yakunlandi.
```


# 381-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #26
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #26.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #26
section .text
global _start
_start:
    push 26
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #26.

## Ishlash natijasi:
```text
Stek amaliyoti #26 muvaffaqiyatli yakunlandi.
```


# 382-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #27
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #27.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #27
section .text
global _start
_start:
    push 27
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #27.

## Ishlash natijasi:
```text
Stek amaliyoti #27 muvaffaqiyatli yakunlandi.
```


# 383-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #28
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #28.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #28
section .text
global _start
_start:
    push 28
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #28.

## Ishlash natijasi:
```text
Stek amaliyoti #28 muvaffaqiyatli yakunlandi.
```


# 384-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #29
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #29.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #29
section .text
global _start
_start:
    push 29
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #29.

## Ishlash natijasi:
```text
Stek amaliyoti #29 muvaffaqiyatli yakunlandi.
```


# 385-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #30
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #30.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #30
section .text
global _start
_start:
    push 30
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #30.

## Ishlash natijasi:
```text
Stek amaliyoti #30 muvaffaqiyatli yakunlandi.
```


# 386-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #31
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #31.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #31
section .text
global _start
_start:
    push 31
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #31.

## Ishlash natijasi:
```text
Stek amaliyoti #31 muvaffaqiyatli yakunlandi.
```


# 387-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #32
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #32.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #32
section .text
global _start
_start:
    push 32
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #32.

## Ishlash natijasi:
```text
Stek amaliyoti #32 muvaffaqiyatli yakunlandi.
```


# 388-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #33
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #33.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #33
section .text
global _start
_start:
    push 33
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #33.

## Ishlash natijasi:
```text
Stek amaliyoti #33 muvaffaqiyatli yakunlandi.
```


# 389-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #34
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #34.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #34
section .text
global _start
_start:
    push 34
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #34.

## Ishlash natijasi:
```text
Stek amaliyoti #34 muvaffaqiyatli yakunlandi.
```


# 390-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #35
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #35.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #35
section .text
global _start
_start:
    push 35
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #35.

## Ishlash natijasi:
```text
Stek amaliyoti #35 muvaffaqiyatli yakunlandi.
```


# 391-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #36
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #36.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #36
section .text
global _start
_start:
    push 36
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #36.

## Ishlash natijasi:
```text
Stek amaliyoti #36 muvaffaqiyatli yakunlandi.
```


# 392-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #37
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #37.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #37
section .text
global _start
_start:
    push 37
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #37.

## Ishlash natijasi:
```text
Stek amaliyoti #37 muvaffaqiyatli yakunlandi.
```


# 393-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #38
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #38.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #38
section .text
global _start
_start:
    push 38
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #38.

## Ishlash natijasi:
```text
Stek amaliyoti #38 muvaffaqiyatli yakunlandi.
```


# 394-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #39
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #39.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #39
section .text
global _start
_start:
    push 39
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #39.

## Ishlash natijasi:
```text
Stek amaliyoti #39 muvaffaqiyatli yakunlandi.
```


# 395-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #40
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #40.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #40
section .text
global _start
_start:
    push 40
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #40.

## Ishlash natijasi:
```text
Stek amaliyoti #40 muvaffaqiyatli yakunlandi.
```


# 396-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #41
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #41.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #41
section .text
global _start
_start:
    push 41
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #41.

## Ishlash natijasi:
```text
Stek amaliyoti #41 muvaffaqiyatli yakunlandi.
```


# 397-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #42
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #42.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #42
section .text
global _start
_start:
    push 42
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #42.

## Ishlash natijasi:
```text
Stek amaliyoti #42 muvaffaqiyatli yakunlandi.
```


# 398-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #43
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #43.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #43
section .text
global _start
_start:
    push 43
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #43.

## Ishlash natijasi:
```text
Stek amaliyoti #43 muvaffaqiyatli yakunlandi.
```


# 399-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #44
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #44.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #44
section .text
global _start
_start:
    push 44
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #44.

## Ishlash natijasi:
```text
Stek amaliyoti #44 muvaffaqiyatli yakunlandi.
```


# 400-Topshiriq: x86_64 stek xotirasi va funksiyalar amaliyoti #45
## Topshiriq sharti:
x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #45.

## Yechim (Assembly kodi):
```assembly
; Stek amaliyoti #45
section .text
global _start
_start:
    push 45
    pop rdi
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #45.

## Ishlash natijasi:
```text
Stek amaliyoti #45 muvaffaqiyatli yakunlandi.
```

