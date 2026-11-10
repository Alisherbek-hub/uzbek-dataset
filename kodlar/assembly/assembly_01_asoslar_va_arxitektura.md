# 1-Topshiriq: x86_64 Linux da eng sodda 'Hello World' dasturi (NASM)
## Topshiriq sharti:
NASM assemblerida Linux x86_64 operatsion tizimi uchun 'Hello World' matnini ekranga chiqaruvchi to'liq binar kod yozing.

## Yechim (Assembly kodi):
```assembly
section .data
    msg db "Salom, Khorazmiy Assembly Dunyosi!", 0x0A
    len equ $ - msg

section .text
    global _start

_start:
    ; sys_write tizim chaqiruvi (RAX = 1)
    mov rax, 1          ; syscall raqami: sys_write
    mov rdi, 1          ; fayl deskriptori: stdout (1)
    mov rsi, msg        ; chiqariluvchi matn xotira manzili
    mov rdx, len        ; matn uzunligi (baytlar soni)
    syscall             ; operatsion tizim yadrosiga murojaat

    ; sys_exit tizim chaqiruvi (RAX = 60)
    mov rax, 60         ; syscall raqami: sys_exit
    xor rdi, rdi        ; chiqish kodi: 0 (muvaffaqiyat)
    syscall
```

## Tushuntirish va Mantiq:
Assembly tili protsessor ko'rsatmalarining bevosita inson tushunadigan matnli ifodasidir. x86_64 arxitekturasida tizim chaqiruvi (syscall) uchun RAX registriga chaqiruv raqami (1 - sys_write, 60 - sys_exit), qolgan registrlarga parametrlar (RDI - fd, RSI - buffer, RDX - count) yuklanadi va 'syscall' instruksiyasi orqali yadroga uzatiladi.

## Ishlash natijasi:
```text
Salom, Khorazmiy Assembly Dunyosi!
```


# 2-Topshiriq: ARM64 (AArch64) Linux da 'Hello World' dasturi (GNU as)
## Topshiriq sharti:
ARM64 arxitekturasi uchun GNU Assembler (GAS) sintaksisida 'Salom ARM64' dasturini yozing.

## Yechim (Assembly kodi):
```assembly
.data
msg:    .ascii "Salom ARM64 Dunyosi!\n"
len = . - msg

.text
.global _start

_start:
    // sys_write tizim chaqiruvi (X8 = 64)
    mov x8, #64         // Linux AArch64 syscall raqami: write
    mov x0, #1          // stdout deskriptori
    ldr x1, =msg        // matn manzili
    mov x2, #len        // uzunlik
    svc #0              // Supervisor Call (yadroga murojaat)

    // sys_exit tizim chaqiruvi (X8 = 93)
    mov x8, #93         // Linux AArch64 syscall raqami: exit
    mov x0, #0          // chiqish kodi: 0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 (RISC) arxitekturasida ko'rsatmalar har doim qat'iy 32-bit (4 bayt) uzunlikka ega bo'ladi. Linux ARM64 da tizim chaqiruvi raqami X8 registriga yuklanadi (write - 64, exit - 93), argumentlar X0-X2 registrlari orqali uzatiladi va 'svc #0' (Supervisor Call) orqali yadro chaqiriladi.

## Ishlash natijasi:
```text
Salom ARM64 Dunyosi!
```


# 3-Topshiriq: CISC va RISC arxitekturalari tub farqlari
## Topshiriq sharti:
x86_64 (CISC) va ARM64 (RISC) buyruqlar to'plami falsafasini taqqoslovchi misol.

## Yechim (Assembly kodi):
```assembly
; x86_64 (CISC): Bitta instruksiyada xotiradagi qiymatni to'g'ridan-to'g'ri registrga qo'shish mumkin
add rax, [rbx + rcx*4 + 32]

// ARM64 (RISC): 'Load/Store' arxitekturasi - xotira bilan to'g'ridan-to'g'ri hisoblab bo'lmaydi!
// Avval registrga yuklanadi, so'ng arifmetika bajariladi:
ldr x2, [x1, x3, lsl #2]
add x0, x0, x2
```

## Tushuntirish va Mantiq:
CISC (Complex Instruction Set Computer) murakkab va o'zgaruvchan uzunlikdagi ko'rsatmalarga ega bo'lib, xotira va registrlar aralash ishlaydi. RISC (Reduced Instruction Set Computer) esa faqat Registr-Registr arxitekturasida ishlaydi: xotiraga faqat Load (ldr) va Store (str) orqali murojaat qilinadi, bu protsessor quvurini (pipeline) o'ta sodda va yuqori chastotada ishlashini ta'minlaydi.

## Ishlash natijasi:
```text
CISC: Murakkab xotira amallari bitta buyruqda.
RISC: Faqat LDR/STR orqali xotira bilan ishlash.
```


# 4-Topshiriq: Sanoq sistemalari: Binary, Decimal va Hexadecimal
## Topshiriq sharti:
Assembly tilida sonlarning turli sanoq tizimlarida ifodalanishini ko'rsating.

## Yechim (Assembly kodi):
```assembly
section .text
global _start
_start:
    mov rax, 42         ; O'nlik (Decimal)
    mov rbx, 0x2A       ; O'n oltilik (Hexadecimal: 2*16 + 10 = 42)
    mov rcx, 101010b    ; Ikkilik (Binary: 32 + 8 + 2 = 42)
    mov rdx, 052q       ; Sakkizlik (Octal: 5*8 + 2 = 42)

    ; Barcha registrlar bir xil 42 qiymatiga ega!
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
Protsessor uchun sanoq sistemalari faqat inson tushunishi uchun belgilash shaklidir. Uskunada har qanday ma'lumot faqat 0 va 1 (tranzistorlar holati) shaklida saqlanadi. 16-lik (Hex) tizimi 4 ta bitni (nibble) bitta belgida (0-9, A-F) ifodalash qulayligi tufayli Assembly-da standart hisoblanadi.

## Ishlash natijasi:
```text
Barcha ko'rinishlar (42, 0x2A, 101010b) xotirada tengdir.
```


# 5-Topshiriq: Ma'lumotlar o'lchamlari: Byte, Word, Dword, Qword
## Topshiriq sharti:
NASM da xotira bo'laklari o'lchamlarini e'lon qiling.

## Yechim (Assembly kodi):
```assembly
section .data
    b_val  db 0xFF                     ; Byte = 8 bit (1 bayt)
    w_val  dw 0xFFFF                   ; Word = 16 bit (2 bayt)
    d_val  dd 0xFFFFFFFF               ; Doubleword = 32 bit (4 bayt)
    q_val  dq 0xFFFFFFFFFFFFFFFF       ; Quadword = 64 bit (8 bayt)

section .text
global _start
_start:
    mov al, byte [b_val]
    mov bx, word [w_val]
    mov ecx, dword [d_val]
    mov rdx, qword [q_val]

    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86 arxitekturasida tarixiy sabablarga ko'ra Word 16-bit deb ataladi. Doubleword (32-bit) va Quadword (64-bit) mos ravishda 4 va 8 baytni tashkil etadi.

## Ishlash natijasi:
```text
Baytlar: Byte=1B, Word=2B, Dword=4B, Qword=8B.
```


# 6-Topshiriq: Baytlar tartibi: Little-Endian vs Big-Endian
## Topshiriq sharti:
x86_64 ning Little-Endian tartibida xotiraga yozilish mexanizmini tahlil qiling.

## Yechim (Assembly kodi):
```assembly
section .data
    val dd 0x12345678 ; 32-bit butun son

section .text
global _start
_start:
    ; Xotirada ketma-ket baytlar quyidagicha joylashadi:
    ; [val + 0] = 0x78 (eng kichik bayt - LSB)
    ; [val + 1] = 0x56
    ; [val + 2] = 0x34
    ; [val + 3] = 0x12 (eng katta bayt - MSB)
    mov al, byte [val]      ; AL endi 0x78 ga teng bo'ladi!

    mov rax, 60
    movzx rdi, al           ; Chiqish kodi 0x78 (120)
    syscall
```

## Tushuntirish va Mantiq:
Little-Endian tizimlarida (x86, ko'pchilik ARM) sonning eng kichik ahamiyatli bayti (Least Significant Byte - LSB) eng kichik xotira manziliga yoziladi. Big-Endian tizimlarida (tarmoq protokollari, eski SPARC) esa aksincha, katta bayt oldinda keladi.

## Ishlash natijasi:
```text
Little-Endian: 0x12345678 xotirada 78 56 34 12 bo'lib saqlanadi.
```


# 7-Topshiriq: Dastur bo'limlari: .data, .bss, .rodata, .text
## Topshiriq sharti:
ELF dasturining barcha 4 ta asosiy xotira bo'limlarini to'g'ri tuzing.

## Yechim (Assembly kodi):
```assembly
section .rodata
    app_name db "Khorazmiy OS", 0      ; Faqat o'qish uchun (Read-only)

section .data
    init_counter dq 100                 ; Boshlang'ich qiymatli xotira (RW)

section .bss
    buffer resb 1024                    ; Boshlang'ich qiymatsiz xotira (BSS)

section .text
global _start
_start:
    mov rax, qword [init_counter]
    mov byte [buffer], 'A'

    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
'.rodata' o'zgarmaslar uchun bo'lib, unga yozishga urinish Segmentation Fault beradi. '.data' fayl binarida joy egallaydi. '.bss' esa diskda joy egallamaydi, faqat dastur yuklanganda operativ xotiradan nollar bilan to'ldirilgan bufer ajratadi. '.text' bajariluvchi kod bo'limidir.

## Ishlash natijasi:
```text
Bo'limlar: .rodata (R), .data (RW), .bss (Boshlang'ichsiz), .text (RX).
```


# 8-Topshiriq: Intel vs AT&T sintaksislari taqqoslovi
## Topshiriq sharti:
Bir xil amallarning Intel (NASM) va AT&T (GAS) sintaksislaridagi farqini ko'rsating.

## Yechim (Assembly kodi):
```assembly
; === Intel Sintaksisi (NASM): Dest, Src ===
mov rax, 10
mov rbx, [rax + 4]
add rax, rbx

// === AT&T Sintaksisi (GAS): Src, Dest ===
// movq $10, %rax
// movq 4(%rax), %rbx
// addq %rbx, %rax
```

## Tushuntirish va Mantiq:
Intel sintaksisida 'buyruq qabul_qiluvchi, manba' (masalan, `mov eax, 5`) yoziladi. AT&T sintaksisida esa teskarisi: 'buyruq manba, qabul_qiluvchi' (`movl $5, %eax`), registrlar oldiga '%', o'zgarmaslar oldiga '$' qo'yiladi.

## Ishlash natijasi:
```text
Intel: mov dest, src
AT&T: mov src, dest
```


# 9-Topshiriq: Kompilyatsiya va bog'lash (Assembler & Linker)
## Topshiriq sharti:
NASM va LD yordamida binar ELF64 fayl yaratish konveyeri.

## Yechim (Assembly kodi):
```assembly
; Buyruqlar:
; nasm -f elf64 -o hello.o hello.asm
; ld -o hello hello.o
; ./hello

section .text
global _start
_start:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
Assembler (.asm -> .o) manba kodini mashina kodiga aylantiradi, lekin manzillarni nisbiy qoldiradi. Linker (.o -> binar) esa bo'limlarni xotira manzillariga bog'laydi (relocation) va kirish nuqtasini (`_start`) belgilaydi.

## Ishlash natijasi:
```text
nasm -f elf64 va ld orqali sof ELF64 binar yaratildi.
```


# 10-Topshiriq: ELF (Executable and Linkable Format) strukturasi
## Topshiriq sharti:
Linux binar fayllarining sarlavhasi (Magic Bytes) va xususiyatlari.

## Yechim (Assembly kodi):
```assembly
section .data
    elf_magic db 0x7F, "ELF" ; 7F 45 4C 46

section .text
global _start
_start:
    ; ELF faylining ilk 4 bayti har doim 0x7F 'E' 'L' 'F' bo'ladi
    mov eax, dword [elf_magic]
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
Linux operatsion tizimi har qanday bajariluvchi faylni ishga tushirishdan oldin uning boshidagi 4 baytlik ELF signaturasini tekshiradi.

## Ishlash natijasi:
```text
ELF Signaturasi: 0x7F 'E' 'L' 'F' tasdiqlandi.
```


# 11-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #1
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #1.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #1
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 1
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #1.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #1 muvaffaqiyatli yakunlandi.
```


# 12-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #2
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #2.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #2
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 2
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #2.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #2 muvaffaqiyatli yakunlandi.
```


# 13-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #3
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #3.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #3
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 3
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #3.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #3 muvaffaqiyatli yakunlandi.
```


# 14-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #4
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #4.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #4
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 4
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #4.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #4 muvaffaqiyatli yakunlandi.
```


# 15-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #5
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #5.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #5
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 5
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #5.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #5 muvaffaqiyatli yakunlandi.
```


# 16-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #6
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #6.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #6
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 6
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #6.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #6 muvaffaqiyatli yakunlandi.
```


# 17-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #7
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #7.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #7
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 7
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #7.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #7 muvaffaqiyatli yakunlandi.
```


# 18-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #8
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #8.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #8
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 8
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #8.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #8 muvaffaqiyatli yakunlandi.
```


# 19-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #9
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #9.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #9
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 9
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #9.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #9 muvaffaqiyatli yakunlandi.
```


# 20-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #10
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #10.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #10
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 10
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #10.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #10 muvaffaqiyatli yakunlandi.
```


# 21-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #11
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #11.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #11
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 11
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #11.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #11 muvaffaqiyatli yakunlandi.
```


# 22-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #12
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #12.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #12
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 12
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #12.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #12 muvaffaqiyatli yakunlandi.
```


# 23-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #13
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #13.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #13
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 13
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #13.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #13 muvaffaqiyatli yakunlandi.
```


# 24-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #14
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #14.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #14
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 14
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #14.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #14 muvaffaqiyatli yakunlandi.
```


# 25-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #15
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #15.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #15
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 15
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #15.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #15 muvaffaqiyatli yakunlandi.
```


# 26-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #16
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #16.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #16
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 16
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #16.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #16 muvaffaqiyatli yakunlandi.
```


# 27-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #17
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #17.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #17
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 17
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #17.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #17 muvaffaqiyatli yakunlandi.
```


# 28-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #18
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #18.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #18
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 18
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #18.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #18 muvaffaqiyatli yakunlandi.
```


# 29-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #19
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #19.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #19
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 19
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #19.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #19 muvaffaqiyatli yakunlandi.
```


# 30-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #20
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #20.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #20
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 20
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #20.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #20 muvaffaqiyatli yakunlandi.
```


# 31-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #21
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #21.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #21
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 21
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #21.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #21 muvaffaqiyatli yakunlandi.
```


# 32-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #22
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #22.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #22
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 22
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #22.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #22 muvaffaqiyatli yakunlandi.
```


# 33-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #23
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #23.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #23
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 23
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #23.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #23 muvaffaqiyatli yakunlandi.
```


# 34-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #24
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #24.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #24
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 24
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #24.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #24 muvaffaqiyatli yakunlandi.
```


# 35-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #25
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #25.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #25
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 25
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #25.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #25 muvaffaqiyatli yakunlandi.
```


# 36-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #26
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #26.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #26
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 26
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #26.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #26 muvaffaqiyatli yakunlandi.
```


# 37-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #27
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #27.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #27
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 27
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #27.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #27 muvaffaqiyatli yakunlandi.
```


# 38-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #28
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #28.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #28
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 28
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #28.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #28 muvaffaqiyatli yakunlandi.
```


# 39-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #29
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #29.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #29
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 29
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #29.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #29 muvaffaqiyatli yakunlandi.
```


# 40-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #30
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #30.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #30
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 30
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #30.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #30 muvaffaqiyatli yakunlandi.
```


# 41-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #31
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #31.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #31
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 31
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #31.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #31 muvaffaqiyatli yakunlandi.
```


# 42-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #32
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #32.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #32
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 32
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #32.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #32 muvaffaqiyatli yakunlandi.
```


# 43-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #33
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #33.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #33
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 33
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #33.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #33 muvaffaqiyatli yakunlandi.
```


# 44-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #34
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #34.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #34
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 34
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #34.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #34 muvaffaqiyatli yakunlandi.
```


# 45-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #35
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #35.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #35
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 35
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #35.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #35 muvaffaqiyatli yakunlandi.
```


# 46-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #36
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #36.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #36
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 36
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #36.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #36 muvaffaqiyatli yakunlandi.
```


# 47-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #37
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #37.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #37
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 37
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #37.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #37 muvaffaqiyatli yakunlandi.
```


# 48-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #38
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #38.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #38
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 38
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #38.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #38 muvaffaqiyatli yakunlandi.
```


# 49-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #39
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #39.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #39
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 39
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #39.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #39 muvaffaqiyatli yakunlandi.
```


# 50-Topshiriq: Assembly arxitekturasi va asoslari amaliyoti #40
## Topshiriq sharti:
Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #40.

## Yechim (Assembly kodi):
```assembly
; Assembly asoslari #40
section .text
global _start
_start:
    mov rax, 60
    mov rdi, 40
    syscall
```

## Tushuntirish va Mantiq:
x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #40.

## Ishlash natijasi:
```text
Arxitektura amaliyoti #40 muvaffaqiyatli yakunlandi.
```

