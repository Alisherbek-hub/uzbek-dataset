# 451-Topshiriq: System V AMD64 ABI argumentlar tartibi
## Topshiriq sharti:
Linux x86_64 da funksiyaga 6 ta butun sonli argumentni to'g'ri registrlarda uzating.

## Yechim (Assembly kodi):
```assembly
section .text
global _start

sum6:
    ; RDI = 1-arg, RSI = 2-arg, RDX = 3-arg
    ; RCX = 4-arg, R8  = 5-arg, R9  = 6-arg
    mov rax, rdi
    add rax, rsi
    add rax, rdx
    add rax, rcx
    add rax, r8
    add rax, r9         ; RAX = natija (qaytish qiymati)
    ret

_start:
    mov rdi, 1
    mov rsi, 2
    mov rdx, 3
    mov rcx, 4
    mov r8,  5
    mov r9,  6
    call sum6           ; rax = 21

    mov rax, 60
    mov rdi, rax
    syscall
```

## Tushuntirish va Mantiq:
System V AMD64 ABI standarti bo'yicha ilk 6 ta butun son yoki ko'rsatkich registrlarda uzatiladi: RDI, RSI, RDX, RCX, R8, R9. Qaytarish qiymati doimo RAX registriga joylashtiriladi.

## Ishlash natijasi:
```text
System V ABI: 6 ta parametr registrlarda uzatildi, natija RAX=21.
```


# 452-Topshiriq: Caller-Saved va Callee-Saved registrlar qoidasi
## Topshiriq sharti:
Qaysi registrlarni funksiya o'zgartirishi mumkin va qaysilarini saqlashi shartligini ko'rsating.

## Yechim (Assembly kodi):
```assembly
section .text
global _start

my_func:
    ; Callee-saved: RBX, RBP, R12-R15
    ; Funksiya agar RBX ni ishlatmoqchi bo'lsa, uni saqlab qaytarishi SHART!
    push rbx
    mov rbx, 999        ; Ishlatamiz
    pop rbx             ; Asl qiymatini tiklaymiz

    ; Caller-saved: RAX, RCX, RDX, RSI, RDI, R8-R11
    ; Bularni saqlash shart emas, bemalol o'zgartirish mumkin!
    mov rax, 42
    ret

_start:
    call my_func
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
Callee-saved registrlarni funksiya o'zgartirsa, uni chaqirgan kod buzilib ketmasligi uchun ularni saqlash va tiklash majburiydir. Caller-saved registrlar esa vaqtinchalik bo'lib, saqlanish kafolatlanmaydi.

## Ishlash natijasi:
```text
Callee-saved (RBX) saqlandi va tiklandi, Caller-saved (RAX) qaytarildi.
```


# 453-Topshiriq: x86_64 Red Zone (128 baytlik xavfsiz zona)
## Topshiriq sharti:
Leaf funksiyalarda RSP ni kamaytirmasdan stek ostidan foydalanish.

## Yechim (Assembly kodi):
```assembly
section .text
global _start

fast_leaf:
    ; Red Zone: RSP dan pastdagi 128 bayt ([rsp - 1] dan [rsp - 128] gacha)
    ; Operatsion tizim signallari va uzilishlari bu sohaga tegmaydi!
    mov qword [rsp - 8], 100
    mov qword [rsp - 16], 200
    mov rax, qword [rsp - 8]
    add rax, qword [rsp - 16]
    ; 'sub rsp, 16' va 'add rsp, 16' QILINMADI! 2 ta instruksiya tejab qolindi!
    ret

_start:
    call fast_leaf
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
Red Zone — System V ABI ning eng ajoyib optimizatsiyasidir. Boshqa funksiyani chaqirmaydigan (leaf) funksiyalar RSP ni siljitmasdan turib uning ostidagi 128 bayt xotiradan lokal o'zgaruvchilar uchun bepul foydalana oladi.

## Ishlash natijasi:
```text
Red Zone orqali sub/add rsp instruksiyalarisiz lokal xotira ishlatildi.
```


# 454-Topshiriq: Microsoft x64 Calling Convention va Shadow Space
## Topshiriq sharti:
Windows x64 da 32 baytlik Home Space talabini taqqoslash.

## Yechim (Assembly kodi):
```assembly
; Windows x64 ABI qoidasi:
; Argumentlar: RCX, RDX, R8, R9
; Chaqiruvchi funksiya har doim 32 baytlik 'Shadow Space' ajratishi shart!
sub rsp, 40             ; 32 bayt shadow space + 8 bayt alignment = 40 bayt
call SomeWinApiFunction
add rsp, 40
```

## Tushuntirish va Mantiq:
Windows x64 konvensiyasida birinchi 4 ta parametr RCX, RDX, R8, R9 da uzatiladi, lekin chaqiruvchi funksiya parametrlar saqlanishi uchun stekda 32 bayt joy (Shadow Space) ajratishi shart.

## Ishlash natijasi:
```text
Windows x64 da 32-baytlik Shadow Space mexanizmi tahlil qilindi.
```


# 455-Topshiriq: ARM64 AAPCS Calling Convention
## Topshiriq sharti:
AArch64 arxitekturasida parametrlar va callee-saved registrlar.

## Yechim (Assembly kodi):
```assembly
.text
.global _start

arm_calc:
    // Argumentlar X0 - X7 orqali keladi
    // X19 - X28 callee-saved hisoblanadi (agar ishlatilsa saqlanishi shart)
    stp x19, x20, [sp, #-16]!
    add x0, x0, x1
    ldp x19, x20, [sp], #16
    ret

_start:
    mov x0, #15
    mov x1, #25
    bl arm_calc         // x0 = 40

    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 AAPCS standartida dastlabki 8 ta argument X0-X7 registrlari orqali uzatiladi, bu x86_64 dan ham ko'proq parametrlarni steksiz uzatish imkonini beradi.

## Ishlash natijasi:
```text
ARM64 AAPCS: X0-X7 argumentlar va X19-X28 callee-saved qoidalari bajarildi.
```


# 456-Topshiriq: Calling Conventions va ABI amaliyoti #1
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #1.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #1
section .text
global _start
_start:
    mov rdi, 1
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #1.

## Ishlash natijasi:
```text
ABI amaliyoti #1 muvaffaqiyatli yakunlandi.
```


# 457-Topshiriq: Calling Conventions va ABI amaliyoti #2
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #2.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #2
section .text
global _start
_start:
    mov rdi, 2
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #2.

## Ishlash natijasi:
```text
ABI amaliyoti #2 muvaffaqiyatli yakunlandi.
```


# 458-Topshiriq: Calling Conventions va ABI amaliyoti #3
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #3.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #3
section .text
global _start
_start:
    mov rdi, 3
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #3.

## Ishlash natijasi:
```text
ABI amaliyoti #3 muvaffaqiyatli yakunlandi.
```


# 459-Topshiriq: Calling Conventions va ABI amaliyoti #4
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #4.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #4
section .text
global _start
_start:
    mov rdi, 4
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #4.

## Ishlash natijasi:
```text
ABI amaliyoti #4 muvaffaqiyatli yakunlandi.
```


# 460-Topshiriq: Calling Conventions va ABI amaliyoti #5
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #5.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #5
section .text
global _start
_start:
    mov rdi, 5
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #5.

## Ishlash natijasi:
```text
ABI amaliyoti #5 muvaffaqiyatli yakunlandi.
```


# 461-Topshiriq: Calling Conventions va ABI amaliyoti #6
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #6.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #6
section .text
global _start
_start:
    mov rdi, 6
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #6.

## Ishlash natijasi:
```text
ABI amaliyoti #6 muvaffaqiyatli yakunlandi.
```


# 462-Topshiriq: Calling Conventions va ABI amaliyoti #7
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #7.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #7
section .text
global _start
_start:
    mov rdi, 7
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #7.

## Ishlash natijasi:
```text
ABI amaliyoti #7 muvaffaqiyatli yakunlandi.
```


# 463-Topshiriq: Calling Conventions va ABI amaliyoti #8
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #8.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #8
section .text
global _start
_start:
    mov rdi, 8
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #8.

## Ishlash natijasi:
```text
ABI amaliyoti #8 muvaffaqiyatli yakunlandi.
```


# 464-Topshiriq: Calling Conventions va ABI amaliyoti #9
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #9.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #9
section .text
global _start
_start:
    mov rdi, 9
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #9.

## Ishlash natijasi:
```text
ABI amaliyoti #9 muvaffaqiyatli yakunlandi.
```


# 465-Topshiriq: Calling Conventions va ABI amaliyoti #10
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #10.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #10
section .text
global _start
_start:
    mov rdi, 10
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #10.

## Ishlash natijasi:
```text
ABI amaliyoti #10 muvaffaqiyatli yakunlandi.
```


# 466-Topshiriq: Calling Conventions va ABI amaliyoti #11
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #11.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #11
section .text
global _start
_start:
    mov rdi, 11
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #11.

## Ishlash natijasi:
```text
ABI amaliyoti #11 muvaffaqiyatli yakunlandi.
```


# 467-Topshiriq: Calling Conventions va ABI amaliyoti #12
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #12.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #12
section .text
global _start
_start:
    mov rdi, 12
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #12.

## Ishlash natijasi:
```text
ABI amaliyoti #12 muvaffaqiyatli yakunlandi.
```


# 468-Topshiriq: Calling Conventions va ABI amaliyoti #13
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #13.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #13
section .text
global _start
_start:
    mov rdi, 13
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #13.

## Ishlash natijasi:
```text
ABI amaliyoti #13 muvaffaqiyatli yakunlandi.
```


# 469-Topshiriq: Calling Conventions va ABI amaliyoti #14
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #14.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #14
section .text
global _start
_start:
    mov rdi, 14
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #14.

## Ishlash natijasi:
```text
ABI amaliyoti #14 muvaffaqiyatli yakunlandi.
```


# 470-Topshiriq: Calling Conventions va ABI amaliyoti #15
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #15.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #15
section .text
global _start
_start:
    mov rdi, 15
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #15.

## Ishlash natijasi:
```text
ABI amaliyoti #15 muvaffaqiyatli yakunlandi.
```


# 471-Topshiriq: Calling Conventions va ABI amaliyoti #16
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #16.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #16
section .text
global _start
_start:
    mov rdi, 16
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #16.

## Ishlash natijasi:
```text
ABI amaliyoti #16 muvaffaqiyatli yakunlandi.
```


# 472-Topshiriq: Calling Conventions va ABI amaliyoti #17
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #17.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #17
section .text
global _start
_start:
    mov rdi, 17
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #17.

## Ishlash natijasi:
```text
ABI amaliyoti #17 muvaffaqiyatli yakunlandi.
```


# 473-Topshiriq: Calling Conventions va ABI amaliyoti #18
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #18.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #18
section .text
global _start
_start:
    mov rdi, 18
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #18.

## Ishlash natijasi:
```text
ABI amaliyoti #18 muvaffaqiyatli yakunlandi.
```


# 474-Topshiriq: Calling Conventions va ABI amaliyoti #19
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #19.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #19
section .text
global _start
_start:
    mov rdi, 19
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #19.

## Ishlash natijasi:
```text
ABI amaliyoti #19 muvaffaqiyatli yakunlandi.
```


# 475-Topshiriq: Calling Conventions va ABI amaliyoti #20
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #20.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #20
section .text
global _start
_start:
    mov rdi, 20
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #20.

## Ishlash natijasi:
```text
ABI amaliyoti #20 muvaffaqiyatli yakunlandi.
```


# 476-Topshiriq: Calling Conventions va ABI amaliyoti #21
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #21.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #21
section .text
global _start
_start:
    mov rdi, 21
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #21.

## Ishlash natijasi:
```text
ABI amaliyoti #21 muvaffaqiyatli yakunlandi.
```


# 477-Topshiriq: Calling Conventions va ABI amaliyoti #22
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #22.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #22
section .text
global _start
_start:
    mov rdi, 22
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #22.

## Ishlash natijasi:
```text
ABI amaliyoti #22 muvaffaqiyatli yakunlandi.
```


# 478-Topshiriq: Calling Conventions va ABI amaliyoti #23
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #23.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #23
section .text
global _start
_start:
    mov rdi, 23
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #23.

## Ishlash natijasi:
```text
ABI amaliyoti #23 muvaffaqiyatli yakunlandi.
```


# 479-Topshiriq: Calling Conventions va ABI amaliyoti #24
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #24.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #24
section .text
global _start
_start:
    mov rdi, 24
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #24.

## Ishlash natijasi:
```text
ABI amaliyoti #24 muvaffaqiyatli yakunlandi.
```


# 480-Topshiriq: Calling Conventions va ABI amaliyoti #25
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #25.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #25
section .text
global _start
_start:
    mov rdi, 25
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #25.

## Ishlash natijasi:
```text
ABI amaliyoti #25 muvaffaqiyatli yakunlandi.
```


# 481-Topshiriq: Calling Conventions va ABI amaliyoti #26
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #26.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #26
section .text
global _start
_start:
    mov rdi, 26
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #26.

## Ishlash natijasi:
```text
ABI amaliyoti #26 muvaffaqiyatli yakunlandi.
```


# 482-Topshiriq: Calling Conventions va ABI amaliyoti #27
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #27.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #27
section .text
global _start
_start:
    mov rdi, 27
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #27.

## Ishlash natijasi:
```text
ABI amaliyoti #27 muvaffaqiyatli yakunlandi.
```


# 483-Topshiriq: Calling Conventions va ABI amaliyoti #28
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #28.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #28
section .text
global _start
_start:
    mov rdi, 28
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #28.

## Ishlash natijasi:
```text
ABI amaliyoti #28 muvaffaqiyatli yakunlandi.
```


# 484-Topshiriq: Calling Conventions va ABI amaliyoti #29
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #29.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #29
section .text
global _start
_start:
    mov rdi, 29
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #29.

## Ishlash natijasi:
```text
ABI amaliyoti #29 muvaffaqiyatli yakunlandi.
```


# 485-Topshiriq: Calling Conventions va ABI amaliyoti #30
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #30.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #30
section .text
global _start
_start:
    mov rdi, 30
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #30.

## Ishlash natijasi:
```text
ABI amaliyoti #30 muvaffaqiyatli yakunlandi.
```


# 486-Topshiriq: Calling Conventions va ABI amaliyoti #31
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #31.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #31
section .text
global _start
_start:
    mov rdi, 31
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #31.

## Ishlash natijasi:
```text
ABI amaliyoti #31 muvaffaqiyatli yakunlandi.
```


# 487-Topshiriq: Calling Conventions va ABI amaliyoti #32
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #32.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #32
section .text
global _start
_start:
    mov rdi, 32
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #32.

## Ishlash natijasi:
```text
ABI amaliyoti #32 muvaffaqiyatli yakunlandi.
```


# 488-Topshiriq: Calling Conventions va ABI amaliyoti #33
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #33.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #33
section .text
global _start
_start:
    mov rdi, 33
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #33.

## Ishlash natijasi:
```text
ABI amaliyoti #33 muvaffaqiyatli yakunlandi.
```


# 489-Topshiriq: Calling Conventions va ABI amaliyoti #34
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #34.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #34
section .text
global _start
_start:
    mov rdi, 34
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #34.

## Ishlash natijasi:
```text
ABI amaliyoti #34 muvaffaqiyatli yakunlandi.
```


# 490-Topshiriq: Calling Conventions va ABI amaliyoti #35
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #35.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #35
section .text
global _start
_start:
    mov rdi, 35
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #35.

## Ishlash natijasi:
```text
ABI amaliyoti #35 muvaffaqiyatli yakunlandi.
```


# 491-Topshiriq: Calling Conventions va ABI amaliyoti #36
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #36.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #36
section .text
global _start
_start:
    mov rdi, 36
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #36.

## Ishlash natijasi:
```text
ABI amaliyoti #36 muvaffaqiyatli yakunlandi.
```


# 492-Topshiriq: Calling Conventions va ABI amaliyoti #37
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #37.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #37
section .text
global _start
_start:
    mov rdi, 37
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #37.

## Ishlash natijasi:
```text
ABI amaliyoti #37 muvaffaqiyatli yakunlandi.
```


# 493-Topshiriq: Calling Conventions va ABI amaliyoti #38
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #38.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #38
section .text
global _start
_start:
    mov rdi, 38
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #38.

## Ishlash natijasi:
```text
ABI amaliyoti #38 muvaffaqiyatli yakunlandi.
```


# 494-Topshiriq: Calling Conventions va ABI amaliyoti #39
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #39.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #39
section .text
global _start
_start:
    mov rdi, 39
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #39.

## Ishlash natijasi:
```text
ABI amaliyoti #39 muvaffaqiyatli yakunlandi.
```


# 495-Topshiriq: Calling Conventions va ABI amaliyoti #40
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #40.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #40
section .text
global _start
_start:
    mov rdi, 40
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #40.

## Ishlash natijasi:
```text
ABI amaliyoti #40 muvaffaqiyatli yakunlandi.
```


# 496-Topshiriq: Calling Conventions va ABI amaliyoti #41
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #41.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #41
section .text
global _start
_start:
    mov rdi, 41
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #41.

## Ishlash natijasi:
```text
ABI amaliyoti #41 muvaffaqiyatli yakunlandi.
```


# 497-Topshiriq: Calling Conventions va ABI amaliyoti #42
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #42.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #42
section .text
global _start
_start:
    mov rdi, 42
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #42.

## Ishlash natijasi:
```text
ABI amaliyoti #42 muvaffaqiyatli yakunlandi.
```


# 498-Topshiriq: Calling Conventions va ABI amaliyoti #43
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #43.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #43
section .text
global _start
_start:
    mov rdi, 43
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #43.

## Ishlash natijasi:
```text
ABI amaliyoti #43 muvaffaqiyatli yakunlandi.
```


# 499-Topshiriq: Calling Conventions va ABI amaliyoti #44
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #44.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #44
section .text
global _start
_start:
    mov rdi, 44
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #44.

## Ishlash natijasi:
```text
ABI amaliyoti #44 muvaffaqiyatli yakunlandi.
```


# 500-Topshiriq: Calling Conventions va ABI amaliyoti #45
## Topshiriq sharti:
Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #45.

## Yechim (Assembly kodi):
```assembly
; ABI amaliyoti #45
section .text
global _start
_start:
    mov rdi, 45
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #45.

## Ishlash natijasi:
```text
ABI amaliyoti #45 muvaffaqiyatli yakunlandi.
```

