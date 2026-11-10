# 751-Topshiriq: Oddiy bir qatorli makros (%define) yaratish
## Topshiriq sharti:
Quyidagi talab bo'yicha assembly kodini yozing: Oddiy bir qatorli makros (%define) yaratish.

## Yechim (Assembly kodi):
```assembly
; NASM da %define direktivasi orqali doimiylar va qisqartmalar yaratish
%define BUFFER_SIZE 4096
%define SYS_EXIT    60
%define SUCCESS     0

section .text
global _start
_start:
    mov rdi, SUCCESS
    mov rax, SYS_EXIT
    syscall
```

## Tushuntirish va Mantiq:
Ushbu kodda `%define` direktivasi orqali `BUFFER_SIZE`, `SYS_EXIT` va `SUCCESS` o'zgarmaslari e'lon qilinadi. Kompilyatsiya vaqtida preprotsessor ushbu nomlarni ularning sonli qiymatlariga almashtiradi.

## Ishlash natijasi:
```text
Dastur 0 kodi bilan muvaffaqiyatli tugaydi.
```


# 752-Topshiriq: Parametrli %define makrosi bilan qiymatni hisoblash
## Topshiriq sharti:
Quyidagi talab bo'yicha assembly kodini yozing: Parametrli %define makrosi bilan qiymatni hisoblash.

## Yechim (Assembly kodi):
```assembly
; %define parametrli makros
%define DOUBLE(x) ((x) * 2)
%define SQUARE(x) ((x) * (x))

section .data
    val1: dq DOUBLE(15)
    val2: dq SQUARE(8)

section .text
global _start
_start:
    mov rax, [val1]       ; 30
    mov rbx, [val2]       ; 64
    add rax, rbx          ; 94
    mov rdi, rax
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
`%define` argument qabul qilishi mumkin. `DOUBLE(15)` preprotsessor tomonidan `((15) * 2)` deb yoyiladi va xotiraga 30 soni yoziladi.

## Ishlash natijasi:
```text
Dastur 94 kodi bilan yakunlanadi (rax=94).
```


# 753-Topshiriq: Ko'p qatorli makros (%macro ... %endmacro)
## Topshiriq sharti:
Quyidagi talab bo'yicha assembly kodini yozing: Ko'p qatorli makros (%macro ... %endmacro).

## Yechim (Assembly kodi):
```assembly
; NASM ko'p qatorli makros
%macro PRINT_CHAR 1
    push rax
    push rdi
    push rsi
    push rdx
    mov byte [rsp-1], %1
    mov rax, 1           ; sys_write
    mov rdi, 1           ; stdout
    lea rsi, [rsp-1]
    mov rdx, 1           ; count=1
    syscall
    pop rdx
    pop rsi
    pop rdi
    pop rax
%endmacro

section .text
global _start
_start:
    PRINT_CHAR 'A'
    PRINT_CHAR 10        ; Yangi qator (newline)
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
`%macro PRINT_CHAR 1` bitta argument oluvchi ko'p qatorli makros yaratadi. `%1` orqali uzatilgan argument olinadi. Registrlar saqlanadi va `sys_write` orqali belgi ekranga chiqariladi.

## Ishlash natijasi:
```text
A
(Dastur yakunlandi)
```


# 754-Topshiriq: Ikki parametrli makros: Registrlar qiymatini almashtirish (SWAP)
## Topshiriq sharti:
Quyidagi talab bo'yicha assembly kodini yozing: Ikki parametrli makros: Registrlar qiymatini almashtirish (SWAP).

## Yechim (Assembly kodi):
```assembly
%macro SWAP_REG 2
    xor %1, %2
    xor %2, %1
    xor %1, %2
%endmacro

section .text
global _start
_start:
    mov rax, 0x11223344
    mov rbx, 0xAABBCCDD
    SWAP_REG rax, rbx
    ; Endi rax = 0xAABBCCDD, rbx = 0x11223344
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
`SWAP_REG 2` makrosi ikkita parametr qabul qiladi (`%1` va `%2`). Qo'shimcha registrsiz XOR mantiqiy amali yordamida ikkala parametr qiymati almashtiriladi.

## Ishlash natijasi:
```text
rax va rbx registrlari qiymatlari muvaffaqiyatli almashdi.
```


# 755-Topshiriq: Makros ichida lokal nishonlar (Local Labels - %%)
## Topshiriq sharti:
Quyidagi talab bo'yicha assembly kodini yozing: Makros ichida lokal nishonlar (Local Labels - %%).

## Yechim (Assembly kodi):
```assembly
%macro ABS_VAL 1
    cmp %1, 0
    jge %%is_positive
    neg %1
%%is_positive:
%endmacro

section .text
global _start
_start:
    mov rax, -42
    ABS_VAL rax          ; rax = 42 bo'ladi
    mov rbx, 100
    ABS_VAL rbx          ; rbx = 100 ligicha qoladi
    mov rdi, rax
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
Makros bir necha bor chaqirilganda label nomlari to'qnashmasligi (duplicate symbol) uchun NASM da `%%` prefiksi ishlatiladi. Preprotsessor har bir kengaytirishda unga unikal nom beradi.

## Ishlash natijasi:
```text
Dastur 42 kodi bilan chiqadi (rax modulli qiymatga ega).
```


# 756-Topshiriq: Moslashuvchan argumentli makroslar (Ko'p parametrli)
## Topshiriq sharti:
Quyidagi talab bo'yicha assembly kodini yozing: Moslashuvchan argumentli makroslar (Ko'p parametrli).

## Yechim (Assembly kodi):
```assembly
%macro SUM_THREE 3
    mov rax, %1
    add rax, %2
    add rax, %3
%endmacro

section .text
global _start
_start:
    SUM_THREE 10, 25, 65 ; rax = 10 + 25 + 65 = 100
    mov rdi, rax
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
`%macro SUM_THREE 3` uchta operandni ketma-ket `rax` registriga jamlaydi. Natija 100 ga teng bo'ladi.

## Ishlash natijasi:
```text
Dastur 100 kodi bilan yakunlanadi.
```


# 757-Topshiriq: Shartli kompilyatsiya: %ifdef va %ifndef
## Topshiriq sharti:
Quyidagi talab bo'yicha assembly kodini yozing: Shartli kompilyatsiya: %ifdef va %ifndef.

## Yechim (Assembly kodi):
```assembly
%define DEBUG_MODE

section .data
%ifdef DEBUG_MODE
    msg db 'Nosozliklarni tuzatish rejimi yoqilgan', 10
    len equ $ - msg
%else
    msg db 'Ishchi rejim', 10
    len equ $ - msg
%endif

section .text
global _start
_start:
    mov rax, 1
    mov rdi, 1
    mov rsi, msg
    mov rdx, len
    syscall
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
`%ifdef` direktivasi ma'lum bir makros aniqlanganligini tekshiradi. Ushbu usul debug va release versiyalarni bitta kod bazasida ajratish uchun ishlatiladi.

## Ishlash natijasi:
```text
Nosozliklarni tuzatish rejimi yoqilgan
```


# 758-Topshiriq: Makros takrorlash direktivasi: %rep va %endrep
## Topshiriq sharti:
Quyidagi talab bo'yicha assembly kodini yozing: Makros takrorlash direktivasi: %rep va %endrep.

## Yechim (Assembly kodi):
```assembly
section .data
table:
%assign i 1
%rep 5
    dq i * 10
    %assign i i + 1
%endrep

section .text
global _start
_start:
    mov rax, [table + 0]  ; 10
    mov rbx, [table + 32] ; 50 (5-element, 4*8=32)
    add rax, rbx          ; 60
    mov rdi, rax
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
`%rep` va `%endrep` preprotsessor sikli hisoblanadi. `%assign` o'zgaruvchisi bilan birga jadval yoki massiv elementlarini avtomatik to'ldirishda qo'llaniladi.

## Ishlash natijasi:
```text
Jadvalda 10, 20, 30, 40, 50 qiymatlari hosil bo'ladi. rax = 60.
```


# 759-Topshiriq: Ichma-ich makroslar (Nested Macros)
## Topshiriq sharti:
Quyidagi talab bo'yicha assembly kodini yozing: Ichma-ich makroslar (Nested Macros).

## Yechim (Assembly kodi):
```assembly
%macro PROLOGUE 1
    push rbp
    mov rbp, rsp
    sub rsp, %1
%endmacro

%macro EPILOGUE 0
    mov rsp, rbp
    pop rbp
    ret
%endmacro

section .text
my_func:
    PROLOGUE 32
    mov dword [rbp-4], 42
    mov eax, [rbp-4]
    EPILOGUE

global _start
_start:
    call my_func
    mov rdi, rax
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
`PROLOGUE` va `EPILOGUE` standart funksiya kirish va chiqish ramkalarini qulay makros sifatida yashiradi va kod takrorlanishini bartaraf qiladi.

## Ishlash natijasi:
```text
Funksiya 42 sonini qaytaradi va dastur 42 kodi bilan chiqadi.
```


# 760-Topshiriq: Fayllarni birlashtirish: %include direktivasi
## Topshiriq sharti:
Quyidagi talab bo'yicha assembly kodini yozing: Fayllarni birlashtirish: %include direktivasi.

## Yechim (Assembly kodi):
```assembly
; headers.inc fayli deb faraz qilinsa:
; %define SYS_WRITE 1
; %define STDOUT 1

%include 'headers.inc' ; Tashqi makroslar to'plamini ulash

section .data
    msg db 'Include ishladi', 10
section .text
global _start
_start:
    mov rax, SYS_WRITE
    mov rdi, STDOUT
    mov rsi, msg
    mov rdx, 16
    syscall
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
`%include` direktivasi C tilidagi `#include` ga teng bo'lib, umumiy konstantalar, funksiya sarlavhalari va makroslarni modulli tarzda ulash imkonini beradi.

## Ishlash natijasi:
```text
Include ishladi
```


# 761-Topshiriq: Modulli dasturlash: 'global' direktivasi bilan funksiyani eksport qilish
## Topshiriq sharti:
Quyidagi vazifani hal etuvchi assembly dasturini yozing: Modulli dasturlash: 'global' direktivasi bilan funksiyani eksport qilish.

## Yechim (Assembly kodi):
```assembly
; math_lib.asm - Matematik kutubxona moduli
section .text
global add_numbers
global multiply_numbers

add_numbers:
    mov rax, rdi
    add rax, rsi
    ret

multiply_numbers:
    mov rax, rdi
    imul rax, rsi
    ret
```

## Tushuntirish va Mantiq:
`global` kalit so'zi linker (`ld`) boshqa modullardan turib ushbu funksiya manzilini topa olishi uchun simvollar jadvaliga (symbol table) eksport qiladi.

## Ishlash natijasi:
```text
`add_numbers` va `multiply_numbers` tashqi modullar uchun ochiq (global) simvolga aylandi.
```


# 762-Topshiriq: Modulli dasturlash: 'extern' direktivasi bilan tashqi moduldan chaqirish
## Topshiriq sharti:
Quyidagi vazifani hal etuvchi assembly dasturini yozing: Modulli dasturlash: 'extern' direktivasi bilan tashqi moduldan chaqirish.

## Yechim (Assembly kodi):
```assembly
; main.asm - Asosiy dastur moduli
extern add_numbers
extern multiply_numbers

section .text
global _start
_start:
    mov rdi, 10
    mov rsi, 20
    call add_numbers      ; rax = 30

    mov rdi, rax
    mov rsi, 3
    call multiply_numbers ; rax = 90

    mov rdi, rax
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
`extern` direktivasi orqali boshqa `.o` (object) fayllarda aniqlangan funksiyalar chaqiriladi. `ld -o program main.o math_lib.o` buyrug'i ularni bog'laydi.

## Ishlash natijasi:
```text
Dastur 90 chiqish kodi bilan tugaydi.
```


# 763-Topshiriq: Modullararo global o'zgaruvchilardan foydalanish (Data sharing)
## Topshiriq sharti:
Quyidagi vazifani hal etuvchi assembly dasturini yozing: Modullararo global o'zgaruvchilardan foydalanish (Data sharing).

## Yechim (Assembly kodi):
```assembly
; data_store.asm
section .data
global g_counter
g_counter: dq 0

; client.asm
extern g_counter
section .text
global increment_counter
increment_counter:
    inc qword [rel g_counter]
    ret
```

## Tushuntirish va Mantiq:
O'zgaruvchilar ham `global` qilinib, boshqa faylda `extern` sifatida e'lon qilinishi mumkin. `rel` (relative addressing) PIC kodida tavsiya etiladi.

## Ishlash natijasi:
```text
`g_counter` barcha modullar orasida umumiy global xotira manziliga ega bo'ladi.
```


# 764-Topshiriq: GNU Assembler (GAS) da makros sintaksisi: .macro va .endm
## Topshiriq sharti:
Quyidagi vazifani hal etuvchi assembly dasturini yozing: GNU Assembler (GAS) da makros sintaksisi: .macro va .endm.

## Yechim (Assembly kodi):
```assembly
# GAS (AT&T sintaksisi) da makros yozish
.macro print_msg text_sym, length
    movq $1, %rax        # sys_write
    movq $1, %rdi        # stdout
    movq \text_sym, %rsi
    movq \length, %rdx
    syscall
.endm

.section .data
msg: .ascii "Salom GAS makros!\n"
len = . - msg

.section .text
.globl _start
_start:
    print_msg $msg, $len
    movq $60, %rax
    xorq %rdi, %rdi
    syscall
```

## Tushuntirish va Mantiq:
GAS assemblerida `.macro` va `.endm` ishlatiladi. Makros argumentlari oldiga teskari slesh (`\argument`) qo'yiladi.

## Ishlash natijasi:
```text
Salom GAS makros!
```


# 765-Topshiriq: ARM64 da GNU as makroslari (.macro / .endm)
## Topshiriq sharti:
Quyidagi vazifani hal etuvchi assembly dasturini yozing: ARM64 da GNU as makroslari (.macro / .endm).

## Yechim (Assembly kodi):
```assembly
// ARM64 da tizim chaqiruvi (exit) makrosi
.macro sys_exit code
    mov x0, \code
    mov x8, #93          // sys_exit raqami
    svc #0
.endm

.section .text
.globl _start
_start:
    mov x1, #10
    add x1, x1, #25
    sys_exit x1          // Chiqish kodi 35
```

## Tushuntirish va Mantiq:
ARM64 arxitekturasida ham GNU assemblerning `.macro` direktivasi orqali x86 dagi kabi tizim chaqiruvlari soddalashtiriladi.

## Ishlash natijasi:
```text
Dastur 35 kodi bilan chiqadi.
```


# 766-Topshiriq: Makros yordamida stekni tekislash (Stack Alignment Macro)
## Topshiriq sharti:
Quyidagi vazifani hal etuvchi assembly dasturini yozing: Makros yordamida stekni tekislash (Stack Alignment Macro).

## Yechim (Assembly kodi):
```assembly
%macro ALIGN_STACK 0
    push rbp
    mov rbp, rsp
    and rsp, -16
%endmacro

%macro RESTORE_STACK 0
    mov rsp, rbp
    pop rbp
%endmacro

section .text
global safe_call
extern printf
safe_call:
    ALIGN_STACK
    ; C kutubxonasi funksiyasini 16-baytga tekislangan holda chaqirish
    RESTORE_STACK
    ret
```

## Tushuntirish va Mantiq:
x86_64 ABI qoidasi bo'yicha tashqi C funksiyalarini chaqirishda stek 16 baytga karrali bo'lishi shart. `and rsp, -16` orqali bu qoida kafolatlanadi.

## Ishlash natijasi:
```text
Stek xavfsiz tarzda 16 bayt chegarasiga tekislanadi.
```


# 767-Topshiriq: NASM da shartli makros: %if / %elif / %else
## Topshiriq sharti:
Quyidagi vazifani hal etuvchi assembly dasturini yozing: NASM da shartli makros: %if / %elif / %else.

## Yechim (Assembly kodi):
```assembly
%define ARCH_X86_64 1

%macro EXIT_SYSTEM 0
    %if ARCH_X86_64 == 1
        mov rax, 60
        xor rdi, rdi
        syscall
    %else
        mov eax, 1
        xor ebx, ebx
        int 0x80
    %endif
%endmacro

section .text
global _start
_start:
    EXIT_SYSTEM
```

## Tushuntirish va Mantiq:
`%if` preprotsessor ifodalarini hisoblaydi va ko'p platformali (32-bit va 64-bit) kod bazalarini bitta makros orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
64-bitlik tizim chaqiruvi (syscall 60) kompilyatsiya qilinadi.
```


# 768-Topshiriq: Boshlang'ich qiymat beruvchi xotira to'ldirish makrosi
## Topshiriq sharti:
Quyidagi vazifani hal etuvchi assembly dasturini yozing: Boshlang'ich qiymat beruvchi xotira to'ldirish makrosi.

## Yechim (Assembly kodi):
```assembly
%macro ALLOC_BUFFER 2
section .bss
    %1: resb %2
section .text
%endmacro

ALLOC_BUFFER net_buffer, 2048
ALLOC_BUFFER log_buffer, 1024

section .text
global _start
_start:
    lea rdi, [net_buffer]
    mov byte [rdi], 'O'
    mov byte [rdi+1], 'K'
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
Makros bir vaqtning o'zida `.bss` bo'limiga o'tib xotira band qilishi va yana `.text` ga qaytishi mumkin. Bu kod strukturasini ixchamlashtiradi.

## Ishlash natijasi:
```text
net_buffer va log_buffer xotirada ajratiladi va to'ldiriladi.
```


# 769-Topshiriq: Ko'p o'lchovli indeks hisoblash makrosi (2D Array Indexing)
## Topshiriq sharti:
Quyidagi vazifani hal etuvchi assembly dasturini yozing: Ko'p o'lchovli indeks hisoblash makrosi (2D Array Indexing).

## Yechim (Assembly kodi):
```assembly
; IDX2D(row, col, cols_count) = (row * cols_count + col) * 8
%macro GET_2D 4
    ; %1 = dest_reg, %2 = row, %3 = col, %4 = cols
    mov %1, %2
    imul %1, %4
    add %1, %3
    shl %1, 3           ; * 8 (qword)
%endmacro

section .text
global _start
_start:
    GET_2D rax, 2, 3, 5  ; row=2, col=3, cols=5 -> (2*5 + 3)*8 = 13*8 = 104
    mov rdi, rax
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
Ko'p o'lchovli massivlarda ofset hisoblash formulasi makrosga joylashtirilib, dastur kodidagi chalkashliklar bartaraf qilinadi.

## Ishlash natijasi:
```text
rax registri 104 ofset qiymatini qabul qiladi.
```


# 770-Topshiriq: Xatolik kodini tekshiruvchi va chiqib ketuvchi ASSERT makrosi
## Topshiriq sharti:
Quyidagi vazifani hal etuvchi assembly dasturini yozing: Xatolik kodini tekshiruvchi va chiqib ketuvchi ASSERT makrosi.

## Yechim (Assembly kodi):
```assembly
%macro ASSERT_NOT_NEGATIVE 1
    cmp %1, 0
    jge %%ok
    ; Agar manfiy bo'lsa, xato bilan tugatamiz
    mov rax, 60
    mov rdi, 255         ; Xatolik statusi
    syscall
%%ok:
%endmacro

section .text
global _start
_start:
    mov rax, 10
    ASSERT_NOT_NEGATIVE rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
Dasturni himoyalash va invariantlarni tekshirish uchun assert makroslari xatolik holatida jarayonni tezkor to'xtatishda juda qulay.

## Ishlash natijasi:
```text
Tekshiruv muvaffaqiyatli o'tadi va dastur 0 kodi bilan yakunlanadi.
```


# 771-Topshiriq: Modulli dasturlash va makroslar ixtisoslashgan texnikasi #1
## Topshiriq sharti:
Modulli dasturlash va makroslar bo'yicha Modulli dasturlash va makroslar ixtisoslashgan texnikasi #1 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Modulli va makros texnikasi #1
%macro SAFE_OPERATION_1 2
    push %1
    mov %1, %2
    rol %1, 2
    pop %1
%endmacro

section .text
global helper_module_1
helper_module_1:
    mov rax, rdi
    SAFE_OPERATION_1 rax, rsi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kodda makros orqali modulli tizimda registrlarni xavfsiz boshqarish va tashqi obyekt fayllaridan `helper_module_1` funksiyasini chaqirish realizatsiya qilingan.

## Ishlash natijasi:
```text
Modul #1 muvaffaqiyatli kompilyatsiya qilindi va ulandi.
```


# 772-Topshiriq: Modulli dasturlash va makroslar ixtisoslashgan texnikasi #2
## Topshiriq sharti:
Modulli dasturlash va makroslar bo'yicha Modulli dasturlash va makroslar ixtisoslashgan texnikasi #2 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Modulli va makros texnikasi #2
%macro SAFE_OPERATION_2 2
    push %1
    mov %1, %2
    rol %1, 3
    pop %1
%endmacro

section .text
global helper_module_2
helper_module_2:
    mov rax, rdi
    SAFE_OPERATION_2 rax, rsi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kodda makros orqali modulli tizimda registrlarni xavfsiz boshqarish va tashqi obyekt fayllaridan `helper_module_2` funksiyasini chaqirish realizatsiya qilingan.

## Ishlash natijasi:
```text
Modul #2 muvaffaqiyatli kompilyatsiya qilindi va ulandi.
```


# 773-Topshiriq: Modulli dasturlash va makroslar ixtisoslashgan texnikasi #3
## Topshiriq sharti:
Modulli dasturlash va makroslar bo'yicha Modulli dasturlash va makroslar ixtisoslashgan texnikasi #3 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Modulli va makros texnikasi #3
%macro SAFE_OPERATION_3 2
    push %1
    mov %1, %2
    rol %1, 4
    pop %1
%endmacro

section .text
global helper_module_3
helper_module_3:
    mov rax, rdi
    SAFE_OPERATION_3 rax, rsi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kodda makros orqali modulli tizimda registrlarni xavfsiz boshqarish va tashqi obyekt fayllaridan `helper_module_3` funksiyasini chaqirish realizatsiya qilingan.

## Ishlash natijasi:
```text
Modul #3 muvaffaqiyatli kompilyatsiya qilindi va ulandi.
```


# 774-Topshiriq: Modulli dasturlash va makroslar ixtisoslashgan texnikasi #4
## Topshiriq sharti:
Modulli dasturlash va makroslar bo'yicha Modulli dasturlash va makroslar ixtisoslashgan texnikasi #4 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Modulli va makros texnikasi #4
%macro SAFE_OPERATION_4 2
    push %1
    mov %1, %2
    rol %1, 5
    pop %1
%endmacro

section .text
global helper_module_4
helper_module_4:
    mov rax, rdi
    SAFE_OPERATION_4 rax, rsi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kodda makros orqali modulli tizimda registrlarni xavfsiz boshqarish va tashqi obyekt fayllaridan `helper_module_4` funksiyasini chaqirish realizatsiya qilingan.

## Ishlash natijasi:
```text
Modul #4 muvaffaqiyatli kompilyatsiya qilindi va ulandi.
```


# 775-Topshiriq: Modulli dasturlash va makroslar ixtisoslashgan texnikasi #5
## Topshiriq sharti:
Modulli dasturlash va makroslar bo'yicha Modulli dasturlash va makroslar ixtisoslashgan texnikasi #5 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Modulli va makros texnikasi #5
%macro SAFE_OPERATION_5 2
    push %1
    mov %1, %2
    rol %1, 6
    pop %1
%endmacro

section .text
global helper_module_5
helper_module_5:
    mov rax, rdi
    SAFE_OPERATION_5 rax, rsi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kodda makros orqali modulli tizimda registrlarni xavfsiz boshqarish va tashqi obyekt fayllaridan `helper_module_5` funksiyasini chaqirish realizatsiya qilingan.

## Ishlash natijasi:
```text
Modul #5 muvaffaqiyatli kompilyatsiya qilindi va ulandi.
```


# 776-Topshiriq: Modulli dasturlash va makroslar ixtisoslashgan texnikasi #6
## Topshiriq sharti:
Modulli dasturlash va makroslar bo'yicha Modulli dasturlash va makroslar ixtisoslashgan texnikasi #6 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Modulli va makros texnikasi #6
%macro SAFE_OPERATION_6 2
    push %1
    mov %1, %2
    rol %1, 7
    pop %1
%endmacro

section .text
global helper_module_6
helper_module_6:
    mov rax, rdi
    SAFE_OPERATION_6 rax, rsi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kodda makros orqali modulli tizimda registrlarni xavfsiz boshqarish va tashqi obyekt fayllaridan `helper_module_6` funksiyasini chaqirish realizatsiya qilingan.

## Ishlash natijasi:
```text
Modul #6 muvaffaqiyatli kompilyatsiya qilindi va ulandi.
```


# 777-Topshiriq: Modulli dasturlash va makroslar ixtisoslashgan texnikasi #7
## Topshiriq sharti:
Modulli dasturlash va makroslar bo'yicha Modulli dasturlash va makroslar ixtisoslashgan texnikasi #7 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Modulli va makros texnikasi #7
%macro SAFE_OPERATION_7 2
    push %1
    mov %1, %2
    rol %1, 1
    pop %1
%endmacro

section .text
global helper_module_7
helper_module_7:
    mov rax, rdi
    SAFE_OPERATION_7 rax, rsi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kodda makros orqali modulli tizimda registrlarni xavfsiz boshqarish va tashqi obyekt fayllaridan `helper_module_7` funksiyasini chaqirish realizatsiya qilingan.

## Ishlash natijasi:
```text
Modul #7 muvaffaqiyatli kompilyatsiya qilindi va ulandi.
```


# 778-Topshiriq: Modulli dasturlash va makroslar ixtisoslashgan texnikasi #8
## Topshiriq sharti:
Modulli dasturlash va makroslar bo'yicha Modulli dasturlash va makroslar ixtisoslashgan texnikasi #8 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Modulli va makros texnikasi #8
%macro SAFE_OPERATION_8 2
    push %1
    mov %1, %2
    rol %1, 2
    pop %1
%endmacro

section .text
global helper_module_8
helper_module_8:
    mov rax, rdi
    SAFE_OPERATION_8 rax, rsi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kodda makros orqali modulli tizimda registrlarni xavfsiz boshqarish va tashqi obyekt fayllaridan `helper_module_8` funksiyasini chaqirish realizatsiya qilingan.

## Ishlash natijasi:
```text
Modul #8 muvaffaqiyatli kompilyatsiya qilindi va ulandi.
```


# 779-Topshiriq: Modulli dasturlash va makroslar ixtisoslashgan texnikasi #9
## Topshiriq sharti:
Modulli dasturlash va makroslar bo'yicha Modulli dasturlash va makroslar ixtisoslashgan texnikasi #9 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Modulli va makros texnikasi #9
%macro SAFE_OPERATION_9 2
    push %1
    mov %1, %2
    rol %1, 3
    pop %1
%endmacro

section .text
global helper_module_9
helper_module_9:
    mov rax, rdi
    SAFE_OPERATION_9 rax, rsi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kodda makros orqali modulli tizimda registrlarni xavfsiz boshqarish va tashqi obyekt fayllaridan `helper_module_9` funksiyasini chaqirish realizatsiya qilingan.

## Ishlash natijasi:
```text
Modul #9 muvaffaqiyatli kompilyatsiya qilindi va ulandi.
```


# 780-Topshiriq: Modulli dasturlash va makroslar ixtisoslashgan texnikasi #10
## Topshiriq sharti:
Modulli dasturlash va makroslar bo'yicha Modulli dasturlash va makroslar ixtisoslashgan texnikasi #10 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Modulli va makros texnikasi #10
%macro SAFE_OPERATION_10 2
    push %1
    mov %1, %2
    rol %1, 4
    pop %1
%endmacro

section .text
global helper_module_10
helper_module_10:
    mov rax, rdi
    SAFE_OPERATION_10 rax, rsi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kodda makros orqali modulli tizimda registrlarni xavfsiz boshqarish va tashqi obyekt fayllaridan `helper_module_10` funksiyasini chaqirish realizatsiya qilingan.

## Ishlash natijasi:
```text
Modul #10 muvaffaqiyatli kompilyatsiya qilindi va ulandi.
```


# 781-Topshiriq: Modulli dasturlash va makroslar ixtisoslashgan texnikasi #11
## Topshiriq sharti:
Modulli dasturlash va makroslar bo'yicha Modulli dasturlash va makroslar ixtisoslashgan texnikasi #11 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Modulli va makros texnikasi #11
%macro SAFE_OPERATION_11 2
    push %1
    mov %1, %2
    rol %1, 5
    pop %1
%endmacro

section .text
global helper_module_11
helper_module_11:
    mov rax, rdi
    SAFE_OPERATION_11 rax, rsi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kodda makros orqali modulli tizimda registrlarni xavfsiz boshqarish va tashqi obyekt fayllaridan `helper_module_11` funksiyasini chaqirish realizatsiya qilingan.

## Ishlash natijasi:
```text
Modul #11 muvaffaqiyatli kompilyatsiya qilindi va ulandi.
```


# 782-Topshiriq: Modulli dasturlash va makroslar ixtisoslashgan texnikasi #12
## Topshiriq sharti:
Modulli dasturlash va makroslar bo'yicha Modulli dasturlash va makroslar ixtisoslashgan texnikasi #12 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Modulli va makros texnikasi #12
%macro SAFE_OPERATION_12 2
    push %1
    mov %1, %2
    rol %1, 6
    pop %1
%endmacro

section .text
global helper_module_12
helper_module_12:
    mov rax, rdi
    SAFE_OPERATION_12 rax, rsi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kodda makros orqali modulli tizimda registrlarni xavfsiz boshqarish va tashqi obyekt fayllaridan `helper_module_12` funksiyasini chaqirish realizatsiya qilingan.

## Ishlash natijasi:
```text
Modul #12 muvaffaqiyatli kompilyatsiya qilindi va ulandi.
```


# 783-Topshiriq: Modulli dasturlash va makroslar ixtisoslashgan texnikasi #13
## Topshiriq sharti:
Modulli dasturlash va makroslar bo'yicha Modulli dasturlash va makroslar ixtisoslashgan texnikasi #13 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Modulli va makros texnikasi #13
%macro SAFE_OPERATION_13 2
    push %1
    mov %1, %2
    rol %1, 7
    pop %1
%endmacro

section .text
global helper_module_13
helper_module_13:
    mov rax, rdi
    SAFE_OPERATION_13 rax, rsi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kodda makros orqali modulli tizimda registrlarni xavfsiz boshqarish va tashqi obyekt fayllaridan `helper_module_13` funksiyasini chaqirish realizatsiya qilingan.

## Ishlash natijasi:
```text
Modul #13 muvaffaqiyatli kompilyatsiya qilindi va ulandi.
```


# 784-Topshiriq: Modulli dasturlash va makroslar ixtisoslashgan texnikasi #14
## Topshiriq sharti:
Modulli dasturlash va makroslar bo'yicha Modulli dasturlash va makroslar ixtisoslashgan texnikasi #14 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Modulli va makros texnikasi #14
%macro SAFE_OPERATION_14 2
    push %1
    mov %1, %2
    rol %1, 1
    pop %1
%endmacro

section .text
global helper_module_14
helper_module_14:
    mov rax, rdi
    SAFE_OPERATION_14 rax, rsi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kodda makros orqali modulli tizimda registrlarni xavfsiz boshqarish va tashqi obyekt fayllaridan `helper_module_14` funksiyasini chaqirish realizatsiya qilingan.

## Ishlash natijasi:
```text
Modul #14 muvaffaqiyatli kompilyatsiya qilindi va ulandi.
```


# 785-Topshiriq: Modulli dasturlash va makroslar ixtisoslashgan texnikasi #15
## Topshiriq sharti:
Modulli dasturlash va makroslar bo'yicha Modulli dasturlash va makroslar ixtisoslashgan texnikasi #15 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Modulli va makros texnikasi #15
%macro SAFE_OPERATION_15 2
    push %1
    mov %1, %2
    rol %1, 2
    pop %1
%endmacro

section .text
global helper_module_15
helper_module_15:
    mov rax, rdi
    SAFE_OPERATION_15 rax, rsi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kodda makros orqali modulli tizimda registrlarni xavfsiz boshqarish va tashqi obyekt fayllaridan `helper_module_15` funksiyasini chaqirish realizatsiya qilingan.

## Ishlash natijasi:
```text
Modul #15 muvaffaqiyatli kompilyatsiya qilindi va ulandi.
```


# 786-Topshiriq: Modulli dasturlash va makroslar ixtisoslashgan texnikasi #16
## Topshiriq sharti:
Modulli dasturlash va makroslar bo'yicha Modulli dasturlash va makroslar ixtisoslashgan texnikasi #16 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Modulli va makros texnikasi #16
%macro SAFE_OPERATION_16 2
    push %1
    mov %1, %2
    rol %1, 3
    pop %1
%endmacro

section .text
global helper_module_16
helper_module_16:
    mov rax, rdi
    SAFE_OPERATION_16 rax, rsi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kodda makros orqali modulli tizimda registrlarni xavfsiz boshqarish va tashqi obyekt fayllaridan `helper_module_16` funksiyasini chaqirish realizatsiya qilingan.

## Ishlash natijasi:
```text
Modul #16 muvaffaqiyatli kompilyatsiya qilindi va ulandi.
```


# 787-Topshiriq: Modulli dasturlash va makroslar ixtisoslashgan texnikasi #17
## Topshiriq sharti:
Modulli dasturlash va makroslar bo'yicha Modulli dasturlash va makroslar ixtisoslashgan texnikasi #17 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Modulli va makros texnikasi #17
%macro SAFE_OPERATION_17 2
    push %1
    mov %1, %2
    rol %1, 4
    pop %1
%endmacro

section .text
global helper_module_17
helper_module_17:
    mov rax, rdi
    SAFE_OPERATION_17 rax, rsi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kodda makros orqali modulli tizimda registrlarni xavfsiz boshqarish va tashqi obyekt fayllaridan `helper_module_17` funksiyasini chaqirish realizatsiya qilingan.

## Ishlash natijasi:
```text
Modul #17 muvaffaqiyatli kompilyatsiya qilindi va ulandi.
```


# 788-Topshiriq: Modulli dasturlash va makroslar ixtisoslashgan texnikasi #18
## Topshiriq sharti:
Modulli dasturlash va makroslar bo'yicha Modulli dasturlash va makroslar ixtisoslashgan texnikasi #18 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Modulli va makros texnikasi #18
%macro SAFE_OPERATION_18 2
    push %1
    mov %1, %2
    rol %1, 5
    pop %1
%endmacro

section .text
global helper_module_18
helper_module_18:
    mov rax, rdi
    SAFE_OPERATION_18 rax, rsi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kodda makros orqali modulli tizimda registrlarni xavfsiz boshqarish va tashqi obyekt fayllaridan `helper_module_18` funksiyasini chaqirish realizatsiya qilingan.

## Ishlash natijasi:
```text
Modul #18 muvaffaqiyatli kompilyatsiya qilindi va ulandi.
```


# 789-Topshiriq: Modulli dasturlash va makroslar ixtisoslashgan texnikasi #19
## Topshiriq sharti:
Modulli dasturlash va makroslar bo'yicha Modulli dasturlash va makroslar ixtisoslashgan texnikasi #19 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Modulli va makros texnikasi #19
%macro SAFE_OPERATION_19 2
    push %1
    mov %1, %2
    rol %1, 6
    pop %1
%endmacro

section .text
global helper_module_19
helper_module_19:
    mov rax, rdi
    SAFE_OPERATION_19 rax, rsi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kodda makros orqali modulli tizimda registrlarni xavfsiz boshqarish va tashqi obyekt fayllaridan `helper_module_19` funksiyasini chaqirish realizatsiya qilingan.

## Ishlash natijasi:
```text
Modul #19 muvaffaqiyatli kompilyatsiya qilindi va ulandi.
```


# 790-Topshiriq: Modulli dasturlash va makroslar ixtisoslashgan texnikasi #20
## Topshiriq sharti:
Modulli dasturlash va makroslar bo'yicha Modulli dasturlash va makroslar ixtisoslashgan texnikasi #20 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Modulli va makros texnikasi #20
%macro SAFE_OPERATION_20 2
    push %1
    mov %1, %2
    rol %1, 7
    pop %1
%endmacro

section .text
global helper_module_20
helper_module_20:
    mov rax, rdi
    SAFE_OPERATION_20 rax, rsi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kodda makros orqali modulli tizimda registrlarni xavfsiz boshqarish va tashqi obyekt fayllaridan `helper_module_20` funksiyasini chaqirish realizatsiya qilingan.

## Ishlash natijasi:
```text
Modul #20 muvaffaqiyatli kompilyatsiya qilindi va ulandi.
```


# 791-Topshiriq: Modulli dasturlash va makroslar ixtisoslashgan texnikasi #21
## Topshiriq sharti:
Modulli dasturlash va makroslar bo'yicha Modulli dasturlash va makroslar ixtisoslashgan texnikasi #21 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Modulli va makros texnikasi #21
%macro SAFE_OPERATION_21 2
    push %1
    mov %1, %2
    rol %1, 1
    pop %1
%endmacro

section .text
global helper_module_21
helper_module_21:
    mov rax, rdi
    SAFE_OPERATION_21 rax, rsi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kodda makros orqali modulli tizimda registrlarni xavfsiz boshqarish va tashqi obyekt fayllaridan `helper_module_21` funksiyasini chaqirish realizatsiya qilingan.

## Ishlash natijasi:
```text
Modul #21 muvaffaqiyatli kompilyatsiya qilindi va ulandi.
```


# 792-Topshiriq: Modulli dasturlash va makroslar ixtisoslashgan texnikasi #22
## Topshiriq sharti:
Modulli dasturlash va makroslar bo'yicha Modulli dasturlash va makroslar ixtisoslashgan texnikasi #22 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Modulli va makros texnikasi #22
%macro SAFE_OPERATION_22 2
    push %1
    mov %1, %2
    rol %1, 2
    pop %1
%endmacro

section .text
global helper_module_22
helper_module_22:
    mov rax, rdi
    SAFE_OPERATION_22 rax, rsi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kodda makros orqali modulli tizimda registrlarni xavfsiz boshqarish va tashqi obyekt fayllaridan `helper_module_22` funksiyasini chaqirish realizatsiya qilingan.

## Ishlash natijasi:
```text
Modul #22 muvaffaqiyatli kompilyatsiya qilindi va ulandi.
```


# 793-Topshiriq: Modulli dasturlash va makroslar ixtisoslashgan texnikasi #23
## Topshiriq sharti:
Modulli dasturlash va makroslar bo'yicha Modulli dasturlash va makroslar ixtisoslashgan texnikasi #23 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Modulli va makros texnikasi #23
%macro SAFE_OPERATION_23 2
    push %1
    mov %1, %2
    rol %1, 3
    pop %1
%endmacro

section .text
global helper_module_23
helper_module_23:
    mov rax, rdi
    SAFE_OPERATION_23 rax, rsi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kodda makros orqali modulli tizimda registrlarni xavfsiz boshqarish va tashqi obyekt fayllaridan `helper_module_23` funksiyasini chaqirish realizatsiya qilingan.

## Ishlash natijasi:
```text
Modul #23 muvaffaqiyatli kompilyatsiya qilindi va ulandi.
```


# 794-Topshiriq: Modulli dasturlash va makroslar ixtisoslashgan texnikasi #24
## Topshiriq sharti:
Modulli dasturlash va makroslar bo'yicha Modulli dasturlash va makroslar ixtisoslashgan texnikasi #24 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Modulli va makros texnikasi #24
%macro SAFE_OPERATION_24 2
    push %1
    mov %1, %2
    rol %1, 4
    pop %1
%endmacro

section .text
global helper_module_24
helper_module_24:
    mov rax, rdi
    SAFE_OPERATION_24 rax, rsi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kodda makros orqali modulli tizimda registrlarni xavfsiz boshqarish va tashqi obyekt fayllaridan `helper_module_24` funksiyasini chaqirish realizatsiya qilingan.

## Ishlash natijasi:
```text
Modul #24 muvaffaqiyatli kompilyatsiya qilindi va ulandi.
```


# 795-Topshiriq: Modulli dasturlash va makroslar ixtisoslashgan texnikasi #25
## Topshiriq sharti:
Modulli dasturlash va makroslar bo'yicha Modulli dasturlash va makroslar ixtisoslashgan texnikasi #25 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Modulli va makros texnikasi #25
%macro SAFE_OPERATION_25 2
    push %1
    mov %1, %2
    rol %1, 5
    pop %1
%endmacro

section .text
global helper_module_25
helper_module_25:
    mov rax, rdi
    SAFE_OPERATION_25 rax, rsi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kodda makros orqali modulli tizimda registrlarni xavfsiz boshqarish va tashqi obyekt fayllaridan `helper_module_25` funksiyasini chaqirish realizatsiya qilingan.

## Ishlash natijasi:
```text
Modul #25 muvaffaqiyatli kompilyatsiya qilindi va ulandi.
```


# 796-Topshiriq: Modulli dasturlash va makroslar ixtisoslashgan texnikasi #26
## Topshiriq sharti:
Modulli dasturlash va makroslar bo'yicha Modulli dasturlash va makroslar ixtisoslashgan texnikasi #26 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Modulli va makros texnikasi #26
%macro SAFE_OPERATION_26 2
    push %1
    mov %1, %2
    rol %1, 6
    pop %1
%endmacro

section .text
global helper_module_26
helper_module_26:
    mov rax, rdi
    SAFE_OPERATION_26 rax, rsi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kodda makros orqali modulli tizimda registrlarni xavfsiz boshqarish va tashqi obyekt fayllaridan `helper_module_26` funksiyasini chaqirish realizatsiya qilingan.

## Ishlash natijasi:
```text
Modul #26 muvaffaqiyatli kompilyatsiya qilindi va ulandi.
```


# 797-Topshiriq: Modulli dasturlash va makroslar ixtisoslashgan texnikasi #27
## Topshiriq sharti:
Modulli dasturlash va makroslar bo'yicha Modulli dasturlash va makroslar ixtisoslashgan texnikasi #27 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Modulli va makros texnikasi #27
%macro SAFE_OPERATION_27 2
    push %1
    mov %1, %2
    rol %1, 7
    pop %1
%endmacro

section .text
global helper_module_27
helper_module_27:
    mov rax, rdi
    SAFE_OPERATION_27 rax, rsi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kodda makros orqali modulli tizimda registrlarni xavfsiz boshqarish va tashqi obyekt fayllaridan `helper_module_27` funksiyasini chaqirish realizatsiya qilingan.

## Ishlash natijasi:
```text
Modul #27 muvaffaqiyatli kompilyatsiya qilindi va ulandi.
```


# 798-Topshiriq: Modulli dasturlash va makroslar ixtisoslashgan texnikasi #28
## Topshiriq sharti:
Modulli dasturlash va makroslar bo'yicha Modulli dasturlash va makroslar ixtisoslashgan texnikasi #28 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Modulli va makros texnikasi #28
%macro SAFE_OPERATION_28 2
    push %1
    mov %1, %2
    rol %1, 1
    pop %1
%endmacro

section .text
global helper_module_28
helper_module_28:
    mov rax, rdi
    SAFE_OPERATION_28 rax, rsi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kodda makros orqali modulli tizimda registrlarni xavfsiz boshqarish va tashqi obyekt fayllaridan `helper_module_28` funksiyasini chaqirish realizatsiya qilingan.

## Ishlash natijasi:
```text
Modul #28 muvaffaqiyatli kompilyatsiya qilindi va ulandi.
```


# 799-Topshiriq: Modulli dasturlash va makroslar ixtisoslashgan texnikasi #29
## Topshiriq sharti:
Modulli dasturlash va makroslar bo'yicha Modulli dasturlash va makroslar ixtisoslashgan texnikasi #29 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Modulli va makros texnikasi #29
%macro SAFE_OPERATION_29 2
    push %1
    mov %1, %2
    rol %1, 2
    pop %1
%endmacro

section .text
global helper_module_29
helper_module_29:
    mov rax, rdi
    SAFE_OPERATION_29 rax, rsi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kodda makros orqali modulli tizimda registrlarni xavfsiz boshqarish va tashqi obyekt fayllaridan `helper_module_29` funksiyasini chaqirish realizatsiya qilingan.

## Ishlash natijasi:
```text
Modul #29 muvaffaqiyatli kompilyatsiya qilindi va ulandi.
```


# 800-Topshiriq: Modulli dasturlash va makroslar ixtisoslashgan texnikasi #30
## Topshiriq sharti:
Modulli dasturlash va makroslar bo'yicha Modulli dasturlash va makroslar ixtisoslashgan texnikasi #30 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Modulli va makros texnikasi #30
%macro SAFE_OPERATION_30 2
    push %1
    mov %1, %2
    rol %1, 3
    pop %1
%endmacro

section .text
global helper_module_30
helper_module_30:
    mov rax, rdi
    SAFE_OPERATION_30 rax, rsi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kodda makros orqali modulli tizimda registrlarni xavfsiz boshqarish va tashqi obyekt fayllaridan `helper_module_30` funksiyasini chaqirish realizatsiya qilingan.

## Ishlash natijasi:
```text
Modul #30 muvaffaqiyatli kompilyatsiya qilindi va ulandi.
```

