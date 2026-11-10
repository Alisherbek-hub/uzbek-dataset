# 701-Topshiriq: C dasturidan tashqi Assembly funksiyasini chaqirish
## Topshiriq sharti:
C da 'extern int asm_add(int a, int b);' deb e'lon qilib, Assembly da uni yozing.

## Yechim (Assembly kodi):
```assembly
; asm_func.asm
section .text
global asm_add

asm_add:
    ; RDI = a, RSI = b
    mov rax, rdi
    add rax, rsi        ; RAX = a + b
    ret
```

## Tushuntirish va Mantiq:
C kompilyatori (GCC/Clang) funksiya nomini to'g'ridan-to'g'ri leybllar jadvaliga qo'yadi. 'global asm_add' orqali u C linkeriga ochiq bo'ladi.

## Ishlash natijasi:
```text
C dasturi Assembly funksiyasini chaqirib natijani oldi.
```


# 702-Topshiriq: Assembly dasturidan libc 'printf' funksiyasini chaqirish
## Topshiriq sharti:
C standart kutubxonasidagi 'printf' orqali formatlangan matn chiqaring.

## Yechim (Assembly kodi):
```assembly
section .data
    fmt db "Natija: %d, Server: %s", 0x0A, 0
    server db "Khorazmiy", 0

section .text
global main
extern printf

main:
    push rbp
    mov rbp, rsp

    ; RDI = fmt, RSI = 42, RDX = server
    lea rdi, [fmt]
    mov rsi, 42
    lea rdx, [server]
    xor eax, eax        ; AL = 0 (suzuvchi nuqtali vektorlar soni nol)
    call printf

    leave
    xor eax, eax
    ret
```

## Tushuntirish va Mantiq:
Varargs (o'zgaruvchan parametrli) C funksiyalarini (masalan printf) chaqirganda, AL registriga XMM registrlarida nechta float uzatilgani ko'rsatilishi shart (agar bo'lmasa 'xor eax, eax').

## Ishlash natijasi:
```text
Natija: 42, Server: Khorazmiy
```


# 703-Topshiriq: GCC Inline Assembly asoslari: '__asm__ __volatile__'
## Topshiriq sharti:
C tili kodi ichiga to'g'ridan-to'g'ri Assembly buyruqlarini kiritish.

## Yechim (Assembly kodi):
```assembly
// C kodida:
// int src = 10, dst;
// __asm__ __volatile__ (
//     "movl %1, %%eax\n\t"
//     "addl $5, %%eax\n\t"
//     "movl %%eax, %0"
//     : "=r" (dst)       // Chiqish
//     : "r" (src)        // Kirish
//     : "%eax"           // Clobbered registr
// );
```

## Tushuntirish va Mantiq:
Extended GCC Inline Assembly 4 ta bo'limdan iborat: Kod shabloni, Chiqish operandlari, Kirish operandlari va Buzilgan registrlar (Clobbered registers).

## Ishlash natijasi:
```text
Inline Assembly orqali C o'zgaruvchisiga 5 qo'shildi: natija 15.
```


# 704-Topshiriq: CPU Taktlarini o'lchash: 'rdtsc' ko'rsatmasi
## Topshiriq sharti:
Protsessor ishga tushgandan beri o'tgan aniq takt sikllari sonini (Time Stamp Counter) oling.

## Yechim (Assembly kodi):
```assembly
section .text
global _start
_start:
    rdtsc               ; EDX:EAX = 64-bitlik Time Stamp Counter
    shl rdx, 32
    or  rax, rdx        ; RAX = to'liq 64-bitlik taktlar soni!

    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
'rdtsc' (Read Time-Stamp Counter) kodning bajarilish tezligini nanosekundlar emas, aniq CPU sikllari sonida o'lchash imkonini beradi.

## Ishlash natijasi:
```text
rdtsc orqali CPU takt sikllari o'lchandi.
```


# 705-Topshiriq: Dinamik xotirani libc 'malloc' va 'free' bilan boshqarish
## Topshiriq sharti:
Assembly dan C xotira menejerini chaqirib, xotirani xavfsiz tozalash.

## Yechim (Assembly kodi):
```assembly
section .text
global main
extern malloc, free

main:
    push rbp
    mov rbp, rsp

    mov rdi, 1024       ; 1024 bayt
    call malloc
    mov rbx, rax        ; Xotira ko'rsatkichi

    ; Xotiradan foydalanamiz...

    mov rdi, rbx
    call free           ; Bo'shatamiz

    leave
    xor eax, eax
    ret
```

## Tushuntirish va Mantiq:
Assembly-da murakkab dasturlar tuzishda libc ning 'malloc' va 'free' funksiyalaridan foydalanish xotira boshqaruvini sezilarli yengillashtiradi.

## Ishlash natijasi:
```text
malloc orqali 1KB xotira ajratildi va free bilan tozalandi.
```


# 706-Topshiriq: C va Assembly integratsiyasi amaliyoti #1
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #1.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #1
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 1
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #1.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #1 muvaffaqiyatli yakunlandi.
```


# 707-Topshiriq: C va Assembly integratsiyasi amaliyoti #2
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #2.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #2
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 2
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #2.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #2 muvaffaqiyatli yakunlandi.
```


# 708-Topshiriq: C va Assembly integratsiyasi amaliyoti #3
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #3.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #3
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 3
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #3.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #3 muvaffaqiyatli yakunlandi.
```


# 709-Topshiriq: C va Assembly integratsiyasi amaliyoti #4
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #4.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #4
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 4
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #4.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #4 muvaffaqiyatli yakunlandi.
```


# 710-Topshiriq: C va Assembly integratsiyasi amaliyoti #5
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #5.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #5
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 5
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #5.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #5 muvaffaqiyatli yakunlandi.
```


# 711-Topshiriq: C va Assembly integratsiyasi amaliyoti #6
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #6.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #6
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 6
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #6.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #6 muvaffaqiyatli yakunlandi.
```


# 712-Topshiriq: C va Assembly integratsiyasi amaliyoti #7
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #7.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #7
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 7
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #7.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #7 muvaffaqiyatli yakunlandi.
```


# 713-Topshiriq: C va Assembly integratsiyasi amaliyoti #8
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #8.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #8
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 8
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #8.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #8 muvaffaqiyatli yakunlandi.
```


# 714-Topshiriq: C va Assembly integratsiyasi amaliyoti #9
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #9.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #9
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 9
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #9.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #9 muvaffaqiyatli yakunlandi.
```


# 715-Topshiriq: C va Assembly integratsiyasi amaliyoti #10
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #10.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #10
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 10
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #10.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #10 muvaffaqiyatli yakunlandi.
```


# 716-Topshiriq: C va Assembly integratsiyasi amaliyoti #11
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #11.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #11
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 11
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #11.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #11 muvaffaqiyatli yakunlandi.
```


# 717-Topshiriq: C va Assembly integratsiyasi amaliyoti #12
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #12.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #12
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 12
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #12.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #12 muvaffaqiyatli yakunlandi.
```


# 718-Topshiriq: C va Assembly integratsiyasi amaliyoti #13
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #13.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #13
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 13
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #13.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #13 muvaffaqiyatli yakunlandi.
```


# 719-Topshiriq: C va Assembly integratsiyasi amaliyoti #14
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #14.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #14
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 14
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #14.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #14 muvaffaqiyatli yakunlandi.
```


# 720-Topshiriq: C va Assembly integratsiyasi amaliyoti #15
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #15.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #15
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 15
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #15.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #15 muvaffaqiyatli yakunlandi.
```


# 721-Topshiriq: C va Assembly integratsiyasi amaliyoti #16
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #16.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #16
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 16
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #16.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #16 muvaffaqiyatli yakunlandi.
```


# 722-Topshiriq: C va Assembly integratsiyasi amaliyoti #17
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #17.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #17
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 17
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #17.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #17 muvaffaqiyatli yakunlandi.
```


# 723-Topshiriq: C va Assembly integratsiyasi amaliyoti #18
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #18.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #18
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 18
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #18.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #18 muvaffaqiyatli yakunlandi.
```


# 724-Topshiriq: C va Assembly integratsiyasi amaliyoti #19
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #19.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #19
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 19
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #19.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #19 muvaffaqiyatli yakunlandi.
```


# 725-Topshiriq: C va Assembly integratsiyasi amaliyoti #20
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #20.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #20
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 20
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #20.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #20 muvaffaqiyatli yakunlandi.
```


# 726-Topshiriq: C va Assembly integratsiyasi amaliyoti #21
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #21.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #21
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 21
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #21.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #21 muvaffaqiyatli yakunlandi.
```


# 727-Topshiriq: C va Assembly integratsiyasi amaliyoti #22
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #22.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #22
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 22
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #22.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #22 muvaffaqiyatli yakunlandi.
```


# 728-Topshiriq: C va Assembly integratsiyasi amaliyoti #23
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #23.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #23
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 23
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #23.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #23 muvaffaqiyatli yakunlandi.
```


# 729-Topshiriq: C va Assembly integratsiyasi amaliyoti #24
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #24.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #24
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 24
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #24.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #24 muvaffaqiyatli yakunlandi.
```


# 730-Topshiriq: C va Assembly integratsiyasi amaliyoti #25
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #25.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #25
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 25
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #25.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #25 muvaffaqiyatli yakunlandi.
```


# 731-Topshiriq: C va Assembly integratsiyasi amaliyoti #26
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #26.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #26
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 26
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #26.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #26 muvaffaqiyatli yakunlandi.
```


# 732-Topshiriq: C va Assembly integratsiyasi amaliyoti #27
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #27.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #27
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 27
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #27.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #27 muvaffaqiyatli yakunlandi.
```


# 733-Topshiriq: C va Assembly integratsiyasi amaliyoti #28
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #28.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #28
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 28
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #28.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #28 muvaffaqiyatli yakunlandi.
```


# 734-Topshiriq: C va Assembly integratsiyasi amaliyoti #29
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #29.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #29
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 29
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #29.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #29 muvaffaqiyatli yakunlandi.
```


# 735-Topshiriq: C va Assembly integratsiyasi amaliyoti #30
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #30.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #30
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 30
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #30.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #30 muvaffaqiyatli yakunlandi.
```


# 736-Topshiriq: C va Assembly integratsiyasi amaliyoti #31
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #31.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #31
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 31
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #31.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #31 muvaffaqiyatli yakunlandi.
```


# 737-Topshiriq: C va Assembly integratsiyasi amaliyoti #32
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #32.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #32
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 32
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #32.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #32 muvaffaqiyatli yakunlandi.
```


# 738-Topshiriq: C va Assembly integratsiyasi amaliyoti #33
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #33.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #33
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 33
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #33.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #33 muvaffaqiyatli yakunlandi.
```


# 739-Topshiriq: C va Assembly integratsiyasi amaliyoti #34
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #34.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #34
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 34
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #34.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #34 muvaffaqiyatli yakunlandi.
```


# 740-Topshiriq: C va Assembly integratsiyasi amaliyoti #35
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #35.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #35
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 35
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #35.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #35 muvaffaqiyatli yakunlandi.
```


# 741-Topshiriq: C va Assembly integratsiyasi amaliyoti #36
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #36.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #36
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 36
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #36.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #36 muvaffaqiyatli yakunlandi.
```


# 742-Topshiriq: C va Assembly integratsiyasi amaliyoti #37
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #37.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #37
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 37
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #37.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #37 muvaffaqiyatli yakunlandi.
```


# 743-Topshiriq: C va Assembly integratsiyasi amaliyoti #38
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #38.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #38
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 38
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #38.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #38 muvaffaqiyatli yakunlandi.
```


# 744-Topshiriq: C va Assembly integratsiyasi amaliyoti #39
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #39.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #39
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 39
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #39.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #39 muvaffaqiyatli yakunlandi.
```


# 745-Topshiriq: C va Assembly integratsiyasi amaliyoti #40
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #40.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #40
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 40
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #40.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #40 muvaffaqiyatli yakunlandi.
```


# 746-Topshiriq: C va Assembly integratsiyasi amaliyoti #41
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #41.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #41
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 41
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #41.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #41 muvaffaqiyatli yakunlandi.
```


# 747-Topshiriq: C va Assembly integratsiyasi amaliyoti #42
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #42.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #42
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 42
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #42.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #42 muvaffaqiyatli yakunlandi.
```


# 748-Topshiriq: C va Assembly integratsiyasi amaliyoti #43
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #43.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #43
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 43
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #43.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #43 muvaffaqiyatli yakunlandi.
```


# 749-Topshiriq: C va Assembly integratsiyasi amaliyoti #44
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #44.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #44
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 44
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #44.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #44 muvaffaqiyatli yakunlandi.
```


# 750-Topshiriq: C va Assembly integratsiyasi amaliyoti #45
## Topshiriq sharti:
C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #45.

## Yechim (Assembly kodi):
```assembly
; C integratsiyasi amaliyoti #45
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 45
    syscall
```

## Tushuntirish va Mantiq:
C va Assembly hamkorligi bo'yicha amaliy topshiriq #45.

## Ishlash natijasi:
```text
C va Assembly amaliyoti #45 muvaffaqiyatli yakunlandi.
```

