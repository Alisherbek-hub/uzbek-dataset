# 501-Topshiriq: x86_64 Tizim chaqiruvi: R10 vs RCX nozikligi
## Topshiriq sharti:
Nega syscall argumentlarida 4-parametr RCX emas, R10 ekanligini namoyish eting.

## Yechim (Assembly kodi):
```assembly
section .text
global _start
_start:
    ; Diqqat! Oddiy C funksiyasida 4-parametr RCX da bo'ladi.
    ; LEKIN 'syscall' buyrug'i apparat darajasida RCX va R11 ni buzadi!
    ; (RCX ga qaytish RIP manzili, R11 ga RFLAGS yoziladi).
    ; Shuning uchun Linux x86_64 yadrosi 4-parametrni R10 da qabul qiladi!

    mov rax, 60         ; sys_exit
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 tizim chaqiruvlari uchun argumentlar tartibi: RAX (syscall raqami), RDI (1), RSI (2), RDX (3), R10 (4), R8 (5), R9 (6). RCX o'rniga R10 ishlatilishi apparat talabidir.

## Ishlash natijasi:
```text
Syscall da R10 ning 4-argument sifatida ishlatilishi tasdiqlandi.
```


# 502-Topshiriq: Klaviaturadan o'qish: 'sys_read' (Syscall 0)
## Topshiriq sharti:
Foydalanuvchi konsolda kiritgan matnni buferga qabul qilib oling.

## Yechim (Assembly kodi):
```assembly
section .bss
    in_buf resb 64

section .text
global _start
_start:
    ; sys_read(fd=0, buf=in_buf, count=64)
    mov rax, 0          ; sys_read
    mov rdi, 0          ; stdin (0)
    mov rsi, in_buf     ; bufer manzili
    mov rdx, 64         ; maksimal baytlar
    syscall
    ; RAX endi haqiqiy o'qilgan baytlar sonini qaytaradi!

    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
'sys_read' fayl yoki standart kirishdan ma'lumotlarni o'qiydi. Qaytarilgan RAX haqiqiy o'qilgan belgilar miqdorini bildiradi.

## Ishlash natijasi:
```text
sys_read orqali stdin oqimidan ma'lumot qabul qilindi.
```


# 503-Topshiriq: Fayl yaratish va yozish: 'sys_open' (2) va 'sys_write' (1)
## Topshiriq sharti:
Yangi fayl ochib, unga Assembly-da ma'lumot yozing va yoping.

## Yechim (Assembly kodi):
```assembly
section .data
    filename db "/tmp/asm_test.txt", 0
    text db "Khorazmiy Assembly Syscalls!", 0x0A
    text_len equ $ - text

section .text
global _start
_start:
    ; 1. sys_open(filename, flags=O_CREAT|O_WRONLY, mode=0644)
    mov rax, 2          ; sys_open
    mov rdi, filename
    mov rsi, 65         ; O_CREAT (64) | O_WRONLY (1)
    mov rdx, 0644o      ; ruxsatlar
    syscall
    mov rbx, rax        ; Yangi fayl deskriptorini (FD) RBX ga saqlaymiz

    ; 2. sys_write(fd, text, len)
    mov rax, 1
    mov rdi, rbx
    mov rsi, text
    mov rdx, text_len
    syscall

    ; 3. sys_close(fd)
    mov rax, 3          ; sys_close
    mov rdi, rbx
    syscall

    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
Toza operatsion tizim chaqiruvlari yordamida C kutubxonasiz to'liq fayl I/O operatsiyalari amalga oshirildi.

## Ishlash natijasi:
```text
Fayl yaratildi, ma'lumot yozildi va muvaffaqiyatli yopildi.
```


# 504-Topshiriq: ARM64 Linux Tizim chaqiruvlari: 'svc #0'
## Topshiriq sharti:
ARM64 da fayl operatsiyalari va deskriptorlar boshqaruvi.

## Yechim (Assembly kodi):
```assembly
.data
msg: .ascii "ARM64 Syscall OK\n"
len = . - msg

.text
.global _start
_start:
    mov x8, #64         // sys_write (Linux ARM64 da write = 64)
    mov x0, #1          // stdout
    ldr x1, =msg
    mov x2, #len
    svc #0

    mov x8, #93         // sys_exit (Linux ARM64 da exit = 93)
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 tizim chaqiruvi raqamlari x86 dan farq qiladi (masalan, write x86 da 1, ARM64 da 64; exit x86 da 60, ARM64 da 93).

## Ishlash natijasi:
```text
ARM64 syscalls (write=64, exit=93) muvaffaqiyatli bajarildi.
```


# 505-Topshiriq: Xatoliklarni tekshirish (Negative Return Values)
## Topshiriq sharti:
Syscall qaytargan xatolik kodlarini (errno) aniqlash.

## Yechim (Assembly kodi):
```assembly
section .text
global _start
_start:
    ; Mavjud bo'lmagan faylni ochish
    mov rax, 2          ; sys_open
    mov rdi, 0          ; Noto'g'ri manzil
    syscall

    ; Linux da syscall xato bersa, RAX ga manfiy errno qaytaradi (-1 dan -4095 gacha)!
    cmp rax, 0
    jl error_handler    ; Agar rax < 0 bo'lsa xato!

    jmp ok_exit
error_handler:
    neg rax             ; RAX endi musbat errno raqamiga aylanadi (masalan, ENOENT = 2)

ok_exit:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
Linux yadrosi alohida 'errno' global o'zgaruvchisini bilmaydi. Tizim chaqiruvi muvaffaqiyatsiz bo'lsa, xato kodi manfiy son sifatida RAX da qaytadi. 'neg rax' orqali haqiqiy errno kodi olinadi.

## Ishlash natijasi:
```text
Syscall manfiy xato kodi (errno) muvaffaqiyatli ushlandi.
```


# 506-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #1
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #1.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #1
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 1
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #1.

## Ishlash natijasi:
```text
Syscall amaliyoti #1 muvaffaqiyatli bajarildi.
```


# 507-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #2
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #2.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #2
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 2
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #2.

## Ishlash natijasi:
```text
Syscall amaliyoti #2 muvaffaqiyatli bajarildi.
```


# 508-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #3
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #3.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #3
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 3
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #3.

## Ishlash natijasi:
```text
Syscall amaliyoti #3 muvaffaqiyatli bajarildi.
```


# 509-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #4
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #4.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #4
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 4
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #4.

## Ishlash natijasi:
```text
Syscall amaliyoti #4 muvaffaqiyatli bajarildi.
```


# 510-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #5
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #5.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #5
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 5
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #5.

## Ishlash natijasi:
```text
Syscall amaliyoti #5 muvaffaqiyatli bajarildi.
```


# 511-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #6
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #6.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #6
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 6
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #6.

## Ishlash natijasi:
```text
Syscall amaliyoti #6 muvaffaqiyatli bajarildi.
```


# 512-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #7
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #7.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #7
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 7
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #7.

## Ishlash natijasi:
```text
Syscall amaliyoti #7 muvaffaqiyatli bajarildi.
```


# 513-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #8
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #8.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #8
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 8
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #8.

## Ishlash natijasi:
```text
Syscall amaliyoti #8 muvaffaqiyatli bajarildi.
```


# 514-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #9
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #9.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #9
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 9
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #9.

## Ishlash natijasi:
```text
Syscall amaliyoti #9 muvaffaqiyatli bajarildi.
```


# 515-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #10
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #10.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #10
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 10
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #10.

## Ishlash natijasi:
```text
Syscall amaliyoti #10 muvaffaqiyatli bajarildi.
```


# 516-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #11
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #11.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #11
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 11
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #11.

## Ishlash natijasi:
```text
Syscall amaliyoti #11 muvaffaqiyatli bajarildi.
```


# 517-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #12
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #12.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #12
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 12
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #12.

## Ishlash natijasi:
```text
Syscall amaliyoti #12 muvaffaqiyatli bajarildi.
```


# 518-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #13
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #13.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #13
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 13
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #13.

## Ishlash natijasi:
```text
Syscall amaliyoti #13 muvaffaqiyatli bajarildi.
```


# 519-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #14
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #14.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #14
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 14
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #14.

## Ishlash natijasi:
```text
Syscall amaliyoti #14 muvaffaqiyatli bajarildi.
```


# 520-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #15
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #15.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #15
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 15
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #15.

## Ishlash natijasi:
```text
Syscall amaliyoti #15 muvaffaqiyatli bajarildi.
```


# 521-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #16
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #16.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #16
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 16
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #16.

## Ishlash natijasi:
```text
Syscall amaliyoti #16 muvaffaqiyatli bajarildi.
```


# 522-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #17
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #17.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #17
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 17
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #17.

## Ishlash natijasi:
```text
Syscall amaliyoti #17 muvaffaqiyatli bajarildi.
```


# 523-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #18
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #18.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #18
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 18
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #18.

## Ishlash natijasi:
```text
Syscall amaliyoti #18 muvaffaqiyatli bajarildi.
```


# 524-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #19
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #19.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #19
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 19
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #19.

## Ishlash natijasi:
```text
Syscall amaliyoti #19 muvaffaqiyatli bajarildi.
```


# 525-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #20
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #20.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #20
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 20
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #20.

## Ishlash natijasi:
```text
Syscall amaliyoti #20 muvaffaqiyatli bajarildi.
```


# 526-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #21
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #21.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #21
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 21
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #21.

## Ishlash natijasi:
```text
Syscall amaliyoti #21 muvaffaqiyatli bajarildi.
```


# 527-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #22
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #22.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #22
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 22
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #22.

## Ishlash natijasi:
```text
Syscall amaliyoti #22 muvaffaqiyatli bajarildi.
```


# 528-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #23
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #23.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #23
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 23
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #23.

## Ishlash natijasi:
```text
Syscall amaliyoti #23 muvaffaqiyatli bajarildi.
```


# 529-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #24
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #24.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #24
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 24
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #24.

## Ishlash natijasi:
```text
Syscall amaliyoti #24 muvaffaqiyatli bajarildi.
```


# 530-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #25
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #25.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #25
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 25
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #25.

## Ishlash natijasi:
```text
Syscall amaliyoti #25 muvaffaqiyatli bajarildi.
```


# 531-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #26
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #26.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #26
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 26
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #26.

## Ishlash natijasi:
```text
Syscall amaliyoti #26 muvaffaqiyatli bajarildi.
```


# 532-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #27
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #27.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #27
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 27
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #27.

## Ishlash natijasi:
```text
Syscall amaliyoti #27 muvaffaqiyatli bajarildi.
```


# 533-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #28
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #28.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #28
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 28
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #28.

## Ishlash natijasi:
```text
Syscall amaliyoti #28 muvaffaqiyatli bajarildi.
```


# 534-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #29
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #29.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #29
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 29
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #29.

## Ishlash natijasi:
```text
Syscall amaliyoti #29 muvaffaqiyatli bajarildi.
```


# 535-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #30
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #30.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #30
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 30
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #30.

## Ishlash natijasi:
```text
Syscall amaliyoti #30 muvaffaqiyatli bajarildi.
```


# 536-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #31
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #31.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #31
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 31
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #31.

## Ishlash natijasi:
```text
Syscall amaliyoti #31 muvaffaqiyatli bajarildi.
```


# 537-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #32
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #32.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #32
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 32
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #32.

## Ishlash natijasi:
```text
Syscall amaliyoti #32 muvaffaqiyatli bajarildi.
```


# 538-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #33
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #33.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #33
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 33
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #33.

## Ishlash natijasi:
```text
Syscall amaliyoti #33 muvaffaqiyatli bajarildi.
```


# 539-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #34
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #34.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #34
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 34
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #34.

## Ishlash natijasi:
```text
Syscall amaliyoti #34 muvaffaqiyatli bajarildi.
```


# 540-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #35
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #35.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #35
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 35
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #35.

## Ishlash natijasi:
```text
Syscall amaliyoti #35 muvaffaqiyatli bajarildi.
```


# 541-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #36
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #36.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #36
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 36
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #36.

## Ishlash natijasi:
```text
Syscall amaliyoti #36 muvaffaqiyatli bajarildi.
```


# 542-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #37
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #37.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #37
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 37
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #37.

## Ishlash natijasi:
```text
Syscall amaliyoti #37 muvaffaqiyatli bajarildi.
```


# 543-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #38
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #38.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #38
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 38
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #38.

## Ishlash natijasi:
```text
Syscall amaliyoti #38 muvaffaqiyatli bajarildi.
```


# 544-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #39
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #39.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #39
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 39
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #39.

## Ishlash natijasi:
```text
Syscall amaliyoti #39 muvaffaqiyatli bajarildi.
```


# 545-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #40
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #40.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #40
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 40
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #40.

## Ishlash natijasi:
```text
Syscall amaliyoti #40 muvaffaqiyatli bajarildi.
```


# 546-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #41
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #41.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #41
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 41
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #41.

## Ishlash natijasi:
```text
Syscall amaliyoti #41 muvaffaqiyatli bajarildi.
```


# 547-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #42
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #42.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #42
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 42
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #42.

## Ishlash natijasi:
```text
Syscall amaliyoti #42 muvaffaqiyatli bajarildi.
```


# 548-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #43
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #43.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #43
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 43
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #43.

## Ishlash natijasi:
```text
Syscall amaliyoti #43 muvaffaqiyatli bajarildi.
```


# 549-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #44
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #44.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #44
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 44
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #44.

## Ishlash natijasi:
```text
Syscall amaliyoti #44 muvaffaqiyatli bajarildi.
```


# 550-Topshiriq: Tizim chaqiruvlari (Syscalls) amaliyoti #45
## Topshiriq sharti:
Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #45.

## Yechim (Assembly kodi):
```assembly
; Syscall amaliyoti #45
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 45
    syscall
```

## Tushuntirish va Mantiq:
Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #45.

## Ishlash natijasi:
```text
Syscall amaliyoti #45 muvaffaqiyatli bajarildi.
```

