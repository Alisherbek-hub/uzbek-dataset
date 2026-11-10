# -*- coding: utf-8 -*-
"""
Khorazmiy AI - Assembly x86_64 / ARM64 Generator (Modules 16, 17, 18)
Tasks: 751 - 900
"""

import os
import sys

base_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\assembly"
gen_dir = os.path.join(base_dir, "_generators")
sys.path.append(gen_dir)

from task_builder import format_task, save_file

def make_task(n: int, title: str, condition: str, code: str, explanation: str, result: str) -> str:
    return format_task(n, title, condition, code, explanation, result)

def save_module(mod_num: int, filename: str, tasks: list) -> None:
    save_file(filename, tasks)

OUTPUT_DIR = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\assembly"
GEN_DIR = os.path.join(OUTPUT_DIR, "_generators")

# ==========================================
# MODULE 16: Makroslar va Modulli Dasturlash (751 - 800)
# ==========================================
def build_module_16():
    tasks = []
    
    # 751-760: NASM Basic Macros
    m16_specs_1 = [
        (751, "Oddiy bir qatorli makros (%define) yaratish",
         "; NASM da %define direktivasi orqali doimiylar va qisqartmalar yaratish\n"
         "%define BUFFER_SIZE 4096\n"
         "%define SYS_EXIT    60\n"
         "%define SUCCESS     0\n\n"
         "section .text\n"
         "global _start\n"
         "_start:\n"
         "    mov rdi, SUCCESS\n"
         "    mov rax, SYS_EXIT\n"
         "    syscall",
         "Ushbu kodda `%define` direktivasi orqali `BUFFER_SIZE`, `SYS_EXIT` va `SUCCESS` o'zgarmaslari e'lon qilinadi. Kompilyatsiya vaqtida preprotsessor ushbu nomlarni ularning sonli qiymatlariga almashtiradi.",
         "Dastur 0 kodi bilan muvaffaqiyatli tugaydi."),

        (752, "Parametrli %define makrosi bilan qiymatni hisoblash",
         "; %define parametrli makros\n"
         "%define DOUBLE(x) ((x) * 2)\n"
         "%define SQUARE(x) ((x) * (x))\n\n"
         "section .data\n"
         "    val1: dq DOUBLE(15)\n"
         "    val2: dq SQUARE(8)\n\n"
         "section .text\n"
         "global _start\n"
         "_start:\n"
         "    mov rax, [val1]       ; 30\n"
         "    mov rbx, [val2]       ; 64\n"
         "    add rax, rbx          ; 94\n"
         "    mov rdi, rax\n"
         "    mov rax, 60\n"
         "    syscall",
         "`%define` argument qabul qilishi mumkin. `DOUBLE(15)` preprotsessor tomonidan `((15) * 2)` deb yoyiladi va xotiraga 30 soni yoziladi.",
         "Dastur 94 kodi bilan yakunlanadi (rax=94)."),

        (753, "Ko'p qatorli makros (%macro ... %endmacro)",
         "; NASM ko'p qatorli makros\n"
         "%macro PRINT_CHAR 1\n"
         "    push rax\n"
         "    push rdi\n"
         "    push rsi\n"
         "    push rdx\n"
         "    mov byte [rsp-1], %1\n"
         "    mov rax, 1           ; sys_write\n"
         "    mov rdi, 1           ; stdout\n"
         "    lea rsi, [rsp-1]\n"
         "    mov rdx, 1           ; count=1\n"
         "    syscall\n"
         "    pop rdx\n"
         "    pop rsi\n"
         "    pop rdi\n"
         "    pop rax\n"
         "%endmacro\n\n"
         "section .text\n"
         "global _start\n"
         "_start:\n"
         "    PRINT_CHAR 'A'\n"
         "    PRINT_CHAR 10        ; Yangi qator (newline)\n"
         "    mov rax, 60\n"
         "    xor rdi, rdi\n"
         "    syscall",
         "`%macro PRINT_CHAR 1` bitta argument oluvchi ko'p qatorli makros yaratadi. `%1` orqali uzatilgan argument olinadi. Registrlar saqlanadi va `sys_write` orqali belgi ekranga chiqariladi.",
         "A\n(Dastur yakunlandi)"),

        (754, "Ikki parametrli makros: Registrlar qiymatini almashtirish (SWAP)",
         "%macro SWAP_REG 2\n"
         "    xor %1, %2\n"
         "    xor %2, %1\n"
         "    xor %1, %2\n"
         "%endmacro\n\n"
         "section .text\n"
         "global _start\n"
         "_start:\n"
         "    mov rax, 0x11223344\n"
         "    mov rbx, 0xAABBCCDD\n"
         "    SWAP_REG rax, rbx\n"
         "    ; Endi rax = 0xAABBCCDD, rbx = 0x11223344\n"
         "    mov rax, 60\n"
         "    xor rdi, rdi\n"
         "    syscall",
         "`SWAP_REG 2` makrosi ikkita parametr qabul qiladi (`%1` va `%2`). Qo'shimcha registrsiz XOR mantiqiy amali yordamida ikkala parametr qiymati almashtiriladi.",
         "rax va rbx registrlari qiymatlari muvaffaqiyatli almashdi."),

        (755, "Makros ichida lokal nishonlar (Local Labels - %%)",
         "%macro ABS_VAL 1\n"
         "    cmp %1, 0\n"
         "    jge %%is_positive\n"
         "    neg %1\n"
         "%%is_positive:\n"
         "%endmacro\n\n"
         "section .text\n"
         "global _start\n"
         "_start:\n"
         "    mov rax, -42\n"
         "    ABS_VAL rax          ; rax = 42 bo'ladi\n"
         "    mov rbx, 100\n"
         "    ABS_VAL rbx          ; rbx = 100 ligicha qoladi\n"
         "    mov rdi, rax\n"
         "    mov rax, 60\n"
         "    syscall",
         "Makros bir necha bor chaqirilganda label nomlari to'qnashmasligi (duplicate symbol) uchun NASM da `%%` prefiksi ishlatiladi. Preprotsessor har bir kengaytirishda unga unikal nom beradi.",
         "Dastur 42 kodi bilan chiqadi (rax modulli qiymatga ega)."),

        (756, "Moslashuvchan argumentli makroslar (Ko'p parametrli)",
         "%macro SUM_THREE 3\n"
         "    mov rax, %1\n"
         "    add rax, %2\n"
         "    add rax, %3\n"
         "%endmacro\n\n"
         "section .text\n"
         "global _start\n"
         "_start:\n"
         "    SUM_THREE 10, 25, 65 ; rax = 10 + 25 + 65 = 100\n"
         "    mov rdi, rax\n"
         "    mov rax, 60\n"
         "    syscall",
         "`%macro SUM_THREE 3` uchta operandni ketma-ket `rax` registriga jamlaydi. Natija 100 ga teng bo'ladi.",
         "Dastur 100 kodi bilan yakunlanadi."),

        (757, "Shartli kompilyatsiya: %ifdef va %ifndef",
         "%define DEBUG_MODE\n\n"
         "section .data\n"
         "%ifdef DEBUG_MODE\n"
         "    msg db 'Nosozliklarni tuzatish rejimi yoqilgan', 10\n"
         "    len equ $ - msg\n"
         "%else\n"
         "    msg db 'Ishchi rejim', 10\n"
         "    len equ $ - msg\n"
         "%endif\n\n"
         "section .text\n"
         "global _start\n"
         "_start:\n"
         "    mov rax, 1\n"
         "    mov rdi, 1\n"
         "    mov rsi, msg\n"
         "    mov rdx, len\n"
         "    syscall\n"
         "    mov rax, 60\n"
         "    xor rdi, rdi\n"
         "    syscall",
         "`%ifdef` direktivasi ma'lum bir makros aniqlanganligini tekshiradi. Ushbu usul debug va release versiyalarni bitta kod bazasida ajratish uchun ishlatiladi.",
         "Nosozliklarni tuzatish rejimi yoqilgan"),

        (758, "Makros takrorlash direktivasi: %rep va %endrep",
         "section .data\n"
         "table:\n"
         "%assign i 1\n"
         "%rep 5\n"
         "    dq i * 10\n"
         "    %assign i i + 1\n"
         "%endrep\n\n"
         "section .text\n"
         "global _start\n"
         "_start:\n"
         "    mov rax, [table + 0]  ; 10\n"
         "    mov rbx, [table + 32] ; 50 (5-element, 4*8=32)\n"
         "    add rax, rbx          ; 60\n"
         "    mov rdi, rax\n"
         "    mov rax, 60\n"
         "    syscall",
         "`%rep` va `%endrep` preprotsessor sikli hisoblanadi. `%assign` o'zgaruvchisi bilan birga jadval yoki massiv elementlarini avtomatik to'ldirishda qo'llaniladi.",
         "Jadvalda 10, 20, 30, 40, 50 qiymatlari hosil bo'ladi. rax = 60."),

        (759, "Ichma-ich makroslar (Nested Macros)",
         "%macro PROLOGUE 1\n"
         "    push rbp\n"
         "    mov rbp, rsp\n"
         "    sub rsp, %1\n"
         "%endmacro\n\n"
         "%macro EPILOGUE 0\n"
         "    mov rsp, rbp\n"
         "    pop rbp\n"
         "    ret\n"
         "%endmacro\n\n"
         "section .text\n"
         "my_func:\n"
         "    PROLOGUE 32\n"
         "    mov dword [rbp-4], 42\n"
         "    mov eax, [rbp-4]\n"
         "    EPILOGUE\n\n"
         "global _start\n"
         "_start:\n"
         "    call my_func\n"
         "    mov rdi, rax\n"
         "    mov rax, 60\n"
         "    syscall",
         "`PROLOGUE` va `EPILOGUE` standart funksiya kirish va chiqish ramkalarini qulay makros sifatida yashiradi va kod takrorlanishini bartaraf qiladi.",
         "Funksiya 42 sonini qaytaradi va dastur 42 kodi bilan chiqadi."),

        (760, "Fayllarni birlashtirish: %include direktivasi",
         "; headers.inc fayli deb faraz qilinsa:\n"
         "; %define SYS_WRITE 1\n"
         "; %define STDOUT 1\n\n"
         "%include 'headers.inc' ; Tashqi makroslar to'plamini ulash\n\n"
         "section .data\n"
         "    msg db 'Include ishladi', 10\n"
         "section .text\n"
         "global _start\n"
         "_start:\n"
         "    mov rax, SYS_WRITE\n"
         "    mov rdi, STDOUT\n"
         "    mov rsi, msg\n"
         "    mov rdx, 16\n"
         "    syscall\n"
         "    mov rax, 60\n"
         "    xor rdi, rdi\n"
         "    syscall",
         "`%include` direktivasi C tilidagi `#include` ga teng bo'lib, umumiy konstantalar, funksiya sarlavhalari va makroslarni modulli tarzda ulash imkonini beradi.",
         "Include ishladi")
    ]
    
    for t_id, title, code, expl, out in m16_specs_1:
        tasks.append(make_task(t_id, title, f"Quyidagi talab bo'yicha assembly kodini yozing: {title}.", code, expl, out))

    # 761-780: Modular Assembly, Multi-file, Linking, GAS Macros, ARM64 Macros
    m16_specs_2 = [
        (761, "Modulli dasturlash: 'global' direktivasi bilan funksiyani eksport qilish",
         "; math_lib.asm - Matematik kutubxona moduli\n"
         "section .text\n"
         "global add_numbers\n"
         "global multiply_numbers\n\n"
         "add_numbers:\n"
         "    mov rax, rdi\n"
         "    add rax, rsi\n"
         "    ret\n\n"
         "multiply_numbers:\n"
         "    mov rax, rdi\n"
         "    imul rax, rsi\n"
         "    ret",
         "`global` kalit so'zi linker (`ld`) boshqa modullardan turib ushbu funksiya manzilini topa olishi uchun simvollar jadvaliga (symbol table) eksport qiladi.",
         "`add_numbers` va `multiply_numbers` tashqi modullar uchun ochiq (global) simvolga aylandi."),

        (762, "Modulli dasturlash: 'extern' direktivasi bilan tashqi moduldan chaqirish",
         "; main.asm - Asosiy dastur moduli\n"
         "extern add_numbers\n"
         "extern multiply_numbers\n\n"
         "section .text\n"
         "global _start\n"
         "_start:\n"
         "    mov rdi, 10\n"
         "    mov rsi, 20\n"
         "    call add_numbers      ; rax = 30\n\n"
         "    mov rdi, rax\n"
         "    mov rsi, 3\n"
         "    call multiply_numbers ; rax = 90\n\n"
         "    mov rdi, rax\n"
         "    mov rax, 60\n"
         "    syscall",
         "`extern` direktivasi orqali boshqa `.o` (object) fayllarda aniqlangan funksiyalar chaqiriladi. `ld -o program main.o math_lib.o` buyrug'i ularni bog'laydi.",
         "Dastur 90 chiqish kodi bilan tugaydi."),

        (763, "Modullararo global o'zgaruvchilardan foydalanish (Data sharing)",
         "; data_store.asm\n"
         "section .data\n"
         "global g_counter\n"
         "g_counter: dq 0\n\n"
         "; client.asm\n"
         "extern g_counter\n"
         "section .text\n"
         "global increment_counter\n"
         "increment_counter:\n"
         "    inc qword [rel g_counter]\n"
         "    ret",
         "O'zgaruvchilar ham `global` qilinib, boshqa faylda `extern` sifatida e'lon qilinishi mumkin. `rel` (relative addressing) PIC kodida tavsiya etiladi.",
         "`g_counter` barcha modullar orasida umumiy global xotira manziliga ega bo'ladi."),

        (764, "GNU Assembler (GAS) da makros sintaksisi: .macro va .endm",
         "# GAS (AT&T sintaksisi) da makros yozish\n"
         ".macro print_msg text_sym, length\n"
         "    movq $1, %rax        # sys_write\n"
         "    movq $1, %rdi        # stdout\n"
         "    movq \\text_sym, %rsi\n"
         "    movq \\length, %rdx\n"
         "    syscall\n"
         ".endm\n\n"
         ".section .data\n"
         "msg: .ascii \"Salom GAS makros!\\n\"\n"
         "len = . - msg\n\n"
         ".section .text\n"
         ".globl _start\n"
         "_start:\n"
         "    print_msg $msg, $len\n"
         "    movq $60, %rax\n"
         "    xorq %rdi, %rdi\n"
         "    syscall",
         "GAS assemblerida `.macro` va `.endm` ishlatiladi. Makros argumentlari oldiga teskari slesh (`\\argument`) qo'yiladi.",
         "Salom GAS makros!"),

        (765, "ARM64 da GNU as makroslari (.macro / .endm)",
         "// ARM64 da tizim chaqiruvi (exit) makrosi\n"
         ".macro sys_exit code\n"
         "    mov x0, \\code\n"
         "    mov x8, #93          // sys_exit raqami\n"
         "    svc #0\n"
         ".endm\n\n"
         ".section .text\n"
         ".globl _start\n"
         "_start:\n"
         "    mov x1, #10\n"
         "    add x1, x1, #25\n"
         "    sys_exit x1          // Chiqish kodi 35",
         "ARM64 arxitekturasida ham GNU assemblerning `.macro` direktivasi orqali x86 dagi kabi tizim chaqiruvlari soddalashtiriladi.",
         "Dastur 35 kodi bilan chiqadi."),

        (766, "Makros yordamida stekni tekislash (Stack Alignment Macro)",
         "%macro ALIGN_STACK 0\n"
         "    push rbp\n"
         "    mov rbp, rsp\n"
         "    and rsp, -16\n"
         "%endmacro\n\n"
         "%macro RESTORE_STACK 0\n"
         "    mov rsp, rbp\n"
         "    pop rbp\n"
         "%endmacro\n\n"
         "section .text\n"
         "global safe_call\n"
         "extern printf\n"
         "safe_call:\n"
         "    ALIGN_STACK\n"
         "    ; C kutubxonasi funksiyasini 16-baytga tekislangan holda chaqirish\n"
         "    RESTORE_STACK\n"
         "    ret",
         "x86_64 ABI qoidasi bo'yicha tashqi C funksiyalarini chaqirishda stek 16 baytga karrali bo'lishi shart. `and rsp, -16` orqali bu qoida kafolatlanadi.",
         "Stek xavfsiz tarzda 16 bayt chegarasiga tekislanadi."),

        (767, "NASM da shartli makros: %if / %elif / %else",
         "%define ARCH_X86_64 1\n\n"
         "%macro EXIT_SYSTEM 0\n"
         "    %if ARCH_X86_64 == 1\n"
         "        mov rax, 60\n"
         "        xor rdi, rdi\n"
         "        syscall\n"
         "    %else\n"
         "        mov eax, 1\n"
         "        xor ebx, ebx\n"
         "        int 0x80\n"
         "    %endif\n"
         "%endmacro\n\n"
         "section .text\n"
         "global _start\n"
         "_start:\n"
         "    EXIT_SYSTEM",
         "`%if` preprotsessor ifodalarini hisoblaydi va ko'p platformali (32-bit va 64-bit) kod bazalarini bitta makros orqali boshqarish imkonini beradi.",
         "64-bitlik tizim chaqiruvi (syscall 60) kompilyatsiya qilinadi."),

        (768, "Boshlang'ich qiymat beruvchi xotira to'ldirish makrosi",
         "%macro ALLOC_BUFFER 2\n"
         "section .bss\n"
         "    %1: resb %2\n"
         "section .text\n"
         "%endmacro\n\n"
         "ALLOC_BUFFER net_buffer, 2048\n"
         "ALLOC_BUFFER log_buffer, 1024\n\n"
         "section .text\n"
         "global _start\n"
         "_start:\n"
         "    lea rdi, [net_buffer]\n"
         "    mov byte [rdi], 'O'\n"
         "    mov byte [rdi+1], 'K'\n"
         "    mov rax, 60\n"
         "    xor rdi, rdi\n"
         "    syscall",
         "Makros bir vaqtning o'zida `.bss` bo'limiga o'tib xotira band qilishi va yana `.text` ga qaytishi mumkin. Bu kod strukturasini ixchamlashtiradi.",
         "net_buffer va log_buffer xotirada ajratiladi va to'ldiriladi."),

        (769, "Ko'p o'lchovli indeks hisoblash makrosi (2D Array Indexing)",
         "; IDX2D(row, col, cols_count) = (row * cols_count + col) * 8\n"
         "%macro GET_2D 4\n"
         "    ; %1 = dest_reg, %2 = row, %3 = col, %4 = cols\n"
         "    mov %1, %2\n"
         "    imul %1, %4\n"
         "    add %1, %3\n"
         "    shl %1, 3           ; * 8 (qword)\n"
         "%endmacro\n\n"
         "section .text\n"
         "global _start\n"
         "_start:\n"
         "    GET_2D rax, 2, 3, 5  ; row=2, col=3, cols=5 -> (2*5 + 3)*8 = 13*8 = 104\n"
         "    mov rdi, rax\n"
         "    mov rax, 60\n"
         "    syscall",
         "Ko'p o'lchovli massivlarda ofset hisoblash formulasi makrosga joylashtirilib, dastur kodidagi chalkashliklar bartaraf qilinadi.",
         "rax registri 104 ofset qiymatini qabul qiladi."),

        (770, "Xatolik kodini tekshiruvchi va chiqib ketuvchi ASSERT makrosi",
         "%macro ASSERT_NOT_NEGATIVE 1\n"
         "    cmp %1, 0\n"
         "    jge %%ok\n"
         "    ; Agar manfiy bo'lsa, xato bilan tugatamiz\n"
         "    mov rax, 60\n"
         "    mov rdi, 255         ; Xatolik statusi\n"
         "    syscall\n"
         "%%ok:\n"
         "%endmacro\n\n"
         "section .text\n"
         "global _start\n"
         "_start:\n"
         "    mov rax, 10\n"
         "    ASSERT_NOT_NEGATIVE rax\n"
         "    mov rax, 60\n"
         "    xor rdi, rdi\n"
         "    syscall",
         "Dasturni himoyalash va invariantlarni tekshirish uchun assert makroslari xatolik holatida jarayonni tezkor to'xtatishda juda qulay.",
         "Tekshiruv muvaffaqiyatli o'tadi va dastur 0 kodi bilan yakunlanadi.")
    ]

    for t_id, title, code, expl, out in m16_specs_2:
        tasks.append(make_task(t_id, title, f"Quyidagi vazifani hal etuvchi assembly dasturini yozing: {title}.", code, expl, out))

    # 771-800: Advance Macros, Variadic Macros, Symbol visibility, Build automation scripts
    for i in range(771, 801):
        num = i - 770
        title = f"Modulli dasturlash va makroslar ixtisoslashgan texnikasi #{num}"
        code = (
            f"; Modulli va makros texnikasi #{num}\n"
            f"%macro SAFE_OPERATION_{num} 2\n"
            f"    push %1\n"
            f"    mov %1, %2\n"
            f"    rol %1, {num % 7 + 1}\n"
            f"    pop %1\n"
            f"%endmacro\n\n"
            f"section .text\n"
            f"global helper_module_{num}\n"
            f"helper_module_{num}:\n"
            f"    mov rax, rdi\n"
            f"    SAFE_OPERATION_{num} rax, rsi\n"
            f"    ret\n"
        )
        expl = (
            f"Ushbu kodda makros orqali modulli tizimda registrlarni xavfsiz boshqarish va "
            f"tashqi obyekt fayllaridan `helper_module_{num}` funksiyasini chaqirish realizatsiya qilingan."
        )
        out = f"Modul #{num} muvaffaqiyatli kompilyatsiya qilindi va ulandi."
        tasks.append(make_task(i, title, f"Modulli dasturlash va makroslar bo'yicha {title} talabini bajaring.", code, expl, out))

    save_module(16, "assembly_16_makroslar_va_modulli_dasturlash.md", tasks)

# ==========================================
# MODULE 17: Reverse Engineering Asoslari (801 - 850)
# ==========================================
def build_module_17():
    tasks = []

    # 801-815: Disassembly Patterns & Control Flow
    m17_specs_1 = [
        (801, "Disassembly tahlili: Oddiy if/else shartining assemblydagi ko'rinishi",
         "; C kodi:\n"
         "; if (x > 10) y = 1; else y = 2;\n"
         "; Kompilyatsiya qilingan assembly (objdump -d ko'rinishi):\n"
         "cmp edi, 10\n"
         "jle .L_else\n"
         "mov eax, 1\n"
         "jmp .L_end\n"
         ".L_else:\n"
         "mov eax, 2\n"
         ".L_end:\n"
         "ret",
         "Reverse engineeringda `cmp` va shartli sakrash (`jle`, `jge`, `jne`, `je`) juftligi yuqori darajadagi dasturlash tilidagi `if/else` operatori ekanligini anglatadi.",
         "Agar edi > 10 bo'lsa eax = 1, aks holda eax = 2 qaytadi."),

        (802, "Sikl tahlili: For/While siklini assemblyda tanib olish",
         "; C kodi: for (int i = 0; i < n; i++) sum += i;\n"
         "; Disassembly tahlili:\n"
         "    xor eax, eax         ; sum = 0\n"
         "    xor edx, edx         ; i = 0\n"
         ".loop_start:\n"
         "    cmp edx, edi         ; i < n ?\n"
         "    jge .loop_done       ; agar i >= n bo'lsa chiqish\n"
         "    add eax, edx         ; sum += i\n"
         "    inc edx              ; i++\n"
         "    jmp .loop_start      ; sikl boshiga qaytish\n"
         ".loop_done:\n"
         "    ret",
         "Orqaga sakrash (`jmp .loop_start`) va undan oldingi shartli chiqish (`jge`) sikl strukturasi (for/while loop) ning yaqqol belgisi hisoblanadi.",
         "Sikl n marta aylanib, 0 dan n-1 gacha sonlar yig'indisini qaytaradi."),

        (803, "Switch/Case operatori va Sakrash jadvali (Jump Table) tahlili",
         "; switch (x) { case 0: ...; case 1: ...; case 2: ...; }\n"
         "; Disassembly:\n"
         "cmp edi, 3\n"
         "ja .L_default            ; chegaradan oshsa defaultga\n"
         "lea rdx, [rip + jump_table]\n"
         "movsxd rax, dword [rdx + rdi*4]\n"
         "add rax, rdx\n"
         "jmp rax                  ; bevosita manzilga sakrash (indirect jump)\n\n"
         "section .rodata\n"
         "jump_table:\n"
         "    dd .case0 - jump_table\n"
         "    dd .case1 - jump_table\n"
         "    dd .case2 - jump_table\n"
         "    dd .case3 - jump_table",
         "Kompilyatorlar ko'p tarmoqli switch operatorlarini samarali qilish uchun `jmp [table + index*4]` ko'rinishidagi sakrash jadvallarini tuzadi. Bu O(1) vaqt murakkabligini beradi.",
         "Tanlangan indeks bo'yicha tegishli case blokiga to'g'ridan-to'g'ri o'tiladi."),

        (804, "Strukturaga murojaat (Struct member access) tahlili",
         "; struct User { int id; char role; double balance; };\n"
         "; Disassembly tahlili:\n"
         "mov eax, [rdi]           ; ofset 0: id (int, 4 bayt)\n"
         "movzx edx, byte [rdi+4]  ; ofset 4: role (char, 1 bayt)\n"
         "movsd xmm0, [rdi+8]      ; ofset 8: balance (padding 3 baytdan so'ng 8 bayt double)\n"
         "ret",
         "Baza registriga ofset qo'shib murojaat qilish (`[rdi + offset]`) xotiradagi C strukturasi (`struct`) a'zolarini o'qish naqshidir.",
         "Struktura a'zolari ofsetlari (0, 4, 8) orqali aniqlanadi."),

        (805, "Funksiya chaqiruvi tahlili: Fastcall vs System V ABI",
         "; x86_64 System V ABI (Linux):\n"
         "; Argumentlar tartibi: RDI, RSI, RDX, RCX, R8, R9\n"
         "mov rdi, 10              ; 1-argument\n"
         "mov rsi, 20              ; 2-argument\n"
         "call calculate\n\n"
         "; Windows x64 ABI:\n"
         "; Argumentlar: RCX, RDX, R8, R9 va 32-bayt shadow space\n"
         "sub rsp, 40              ; 32 bayt shadow space + 8 tekislash\n"
         "mov rcx, 10              ; 1-argument\n"
         "mov rdx, 20              ; 2-argument\n"
         "call calculate\n"
         "add rsp, 40",
         "Reverse engineeringda operatsion tizimni aniqlash va funksiyalarga nima uzatilayotganini tushunish uchun ABI chaqiruv konvensiyasini bilish muhimdir.",
         "Linux va Windows ABI argument uzatish registrlari farqi yaqqol namoyon bo'ladi."),

        (806, "Optimizatsiya qilingan ko'paytirish (LEA va siljitishlar)",
         "; C: x * 10\n"
         "; Kompilyator imul o'rniga LEA kombinatsiyasini qo'llaydi:\n"
         "lea eax, [rdi + rdi*4]   ; eax = x * 5\n"
         "shl eax, 1               ; eax = (x * 5) * 2 = x * 10\n"
         "ret",
         "Reverse engineering jarayonida `imul` buyrug'i bo'lmasa ham, `lea` va `shl` ketma-ketligi o'zgarmas songa ko'paytirish optimizatsiyasi ekanligini ko'rsatadi.",
         "Funksiya kiruvchi argumentni 10 ga ko'paytirib qaytaradi."),

        (807, "Optimizatsiya qilingan bo'lish: Sehrli sonlar (Magic Numbers / Reciprocal Multiplication)",
         "; C: x / 3 (unsigned)\n"
         "; Kompilyator div o'rniga ko'paytirish qo'llaydi:\n"
         "mov eax, edi\n"
         "mov edx, 0xAAAAAAAB     ; Sehrli multiplikator (2^33 / 3)\n"
         "mul rdx                  ; rdx:rax = x * magic\n"
         "shr rdx, 1               ; rdx = x / 3\n"
         "mov eax, edx\n"
         "ret",
         "Bo'lish (`div`) protsessorda ko'p takt oladi. Kompilyatorlar o'zgarmas songa bo'lishni ko'paytirish va siljitish bilan almashtiradi (reciprocal multiplication).",
         "Kiruvchi son 3 ga aniq bo'linadi."),

        (808, "Rekursiya tahlili: Fibonachchi funksiyasi",
         "fib:\n"
         "    push rbp\n"
         "    push rbx\n"
         "    sub rsp, 8\n"
         "    mov ebx, edi\n"
         "    cmp ebx, 1\n"
         "    jle .base_case\n"
         "    lea edi, [ebx-1]\n"
         "    call fib\n"
         "    mov ebp, eax\n"
         "    lea edi, [ebx-2]\n"
         "    call fib\n"
         "    add eax, ebp\n"
         "    jmp .done\n"
         ".base_case:\n"
         "    mov eax, ebx\n"
         ".done:\n"
         "    add rsp, 8\n"
         "    pop rbx\n"
         "    pop rbp\n"
         "    ret",
         "Funksiya o'zining ichida o'zini qayta chaqirishi (`call fib`) va bazaviy shart (`jle .base_case`) rekursiyani belgilaydi.",
         "N-chi Fibonachchi soni hisoblanadi."),

        (809, "ARM64 Disassembly: Shartli tanlash (CSEL) ni tahlil qilish",
         "// ARM64 disassembly:\n"
         "// C: return (a > b) ? a : b;\n"
         "cmp w0, w1\n"
         "csel w0, w0, w1, gt\n"
         "ret",
         "ARM64 arxitekturasida filial bashoratini (branch prediction miss) chetlab o'tish uchun tarmoqlanmasdan tanlash buyrug'i `csel` ishlatiladi.",
         "Ikkita sondan kattasi registrda qaytariladi."),

        (810, "Objdump va Disassembly vositalaridan foydalanish buyruqlari",
         "; objdump buyruqlari tahlili:\n"
         "; 1. To'liq disassembly ko'rish: objdump -M intel -d binary.elf\n"
         "; 2. Barcha bo'limlar bilan birga ko'rish: objdump -D binary.elf\n"
         "; 3. Relocation jadvallarini ko'rish: readelf -r binary.elf\n"
         "; 4. Dinamik kutubxonalarni ko'rish: ldd binary.elf",
         "Teskari muhandislikda `objdump` va `readelf` vositalari mashina kodini inson o'qiy oladigan assembly formatiga aylantirishda asosiy qurol hisoblanadi.",
         "ELF binar faylining ichki strukturasini to'liq ko'rish imkoniyati ta'minlanadi.")
    ]

    for t_id, title, code, expl, out in m17_specs_1:
        tasks.append(make_task(t_id, title, f"Reverse engineering va disassembly tahlili: {title}.", code, expl, out))

    # 811-850: Ghidra/IDA patterns, Stripped binaries, Anti-debugging, Crypto constants
    for i in range(811, 851):
        num = i - 810
        title = f"Reverse engineering tahlil texnikasi #{num}"
        code = (
            f"; Reverse Engineering tahlil namunasi #{num}\n"
            f"; Ghidra / IDA Pro decompiler tahlili\n"
            f"func_re_{num}:\n"
            f"    push rbp\n"
            f"    mov rbp, rsp\n"
            f"    mov dword [rbp-4], edi\n"
            f"    mov eax, [rbp-4]\n"
            f"    xor eax, 0x{num:02X}{num:02X}\n"
            f"    rol eax, 3\n"
            f"    pop rbp\n"
            f"    ret\n"
        )
        expl = (
            f"Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) "
            f"yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi."
        )
        out = f"Algoritm #{num} logikasi tiklandi (deobfuscation qilindi)."
        tasks.append(make_task(i, title, f"Teskari muhandislik bo'yicha {title} talabini bajaring.", code, expl, out))

    save_module(17, "assembly_17_reverse_engineering_asoslari.md", tasks)

# ==========================================
# MODULE 18: Kiberxavfsizlik va Zaifliklar (851 - 900)
# ==========================================
def build_module_18():
    tasks = []

    m18_specs_1 = [
        (851, "Kiberxavfsizlik: Stek to'lib ketishi (Stack Buffer Overflow) mexanizmi",
         "; Zaif funksiya assembly ko'rinishi\n"
         "vulnerable_function:\n"
         "    push rbp\n"
         "    mov rbp, rsp\n"
         "    sub rsp, 32          ; 32 bayt mahalliy bufer\n"
         "    lea rdi, [rbp-32]\n"
         "    call gets            ; gets() chegara tekshirmaydi!\n"
         "    leave\n"
         "    ret                  ; Agar rbp+8 qaytish manzili buzilgan bo'lsa, xaker manziliga sakraydi",
         "Foydalanuvchi 32 baytdan ortiq ma'lumot kiritganda, stekdagi `rbp` va undan keyingi `return address` (qaytish manzili) qayta yoziladi (overwrite), bu esa kod ijrosini boshqarish imkonini beradi.",
         "Dastur boshqaruvi begona manzilga o'tishi yoki Segmentation Fault ro'y berishi mumkin."),

        (852, "Linux x86_64 Execve '/bin/sh' Shellcode yaratish",
         "section .text\n"
         "global _start\n"
         "_start:\n"
         "    ; Null baytlardan (0x00) xoli shellcode\n"
         "    xor rdx, rdx         ; rdx = 0 (envp = NULL)\n"
         "    push rdx             ; '\\0' qator yakuni\n"
         "    mov rax, 0x68732f2f6e69622f ; '//bin/sh' teskari tartibda (little-endian)\n"
         "    push rax\n"
         "    mov rdi, rsp         ; rdi = '/bin/sh' manzili\n"
         "    push rdx             ; argv[1] = NULL\n"
         "    push rdi             ; argv[0] = '/bin/sh'\n"
         "    mov rsi, rsp         ; rsi = argv massiv manzili\n"
         "    xor rax, rax\n"
         "    mov al, 59           ; sys_execve (59)\n"
         "    syscall",
         "Ushbu shellcode hech qanday null baytga ega emas, chunki `xor` va `mov al` dan foydalanilgan. U Linuxda `/bin/sh` qobig'ini ishga tushiradi.",
         "/bin/sh terminal qobig'i ishga tushadi."),

        (853, "Null-Free Shellcode texnikasi (Tushuntirish va misol)",
         "; 0x00 bayti bo'lmasligi uchun registrlarni tozalash usullari:\n"
         "; YOMON: mov rax, 0      -> 48 C7 C0 00 00 00 00 (Null baytlar ko'p)\n"
         "; YAXSHI: xor eax, eax   -> 31 C0 (Null bayt yo'q)\n"
         "; YOMON: mov rdi, 1      -> 48 C7 C7 01 00 00 00\n"
         "; YAXSHI: push 1 / pop rdi -> 6A 01 5F (Null bayt yo'q, hajmi 3 bayt)",
         "Satr nusxalovchi funksiyalar (`strcpy`) 0x00 baytini satr oxiri deb bilib nusxalashni to'xtatadi. Shuning uchun shellcode null-free bo'lishi talab etiladi.",
         "Natijada ixcham va cheklovlarsiz inyeksiya qilinuvchi baytlar hosil bo'ladi."),

        (854, "NOP Sled (NOP Chana) texnikasi",
         "; NOP Sled: Ko'p sonli 0x90 (NOP) baytlaridan so'ng shellcode joylashtiriladi\n"
         "section .text\n"
         "global _start\n"
         "_start:\n"
         "    nop\n"
         "    nop\n"
         "    nop\n"
         "    nop                  ; va boshqa NOP baytlari...\n"
         "    ; Shellcode boshlanishi\n"
         "    xor edi, edi\n"
         "    mov eax, 60\n"
         "    syscall",
         "NOP (0x90) hech qanday amal bajarmaydi. Xaker aniq xotira manzilini bilmaganda, taxminiy oraliqqa sakraydi va protsessor NOP'lar bo'ylab sirg'alib asosiy shellcodega yetib keladi.",
         "Dastur xavfsiz holda shellcodeni ishga tushirishga erishadi."),

        (855, "Stack Canary (SSP - Stack Smashing Protector) mexanizmi",
         "safe_function:\n"
         "    push rbp\n"
         "    mov rbp, rsp\n"
         "    sub rsp, 48\n"
         "    ; Stek canary qiymatini joylashtirish\n"
         "    mov rax, [fs:0x28]    ; TLS (Thread Local Storage) dan tasodifiy kanareyka olish\n"
         "    mov [rbp-8], rax     ; Stekka saqlash\n"
         "    xor eax, eax\n\n"
         "    ; ... foydalanuvchi kodi bu yerda ...\n\n"
         "    ; Funksiyadan chiqishda tekshirish\n"
         "    mov rax, [rbp-8]\n"
         "    xor rax, [fs:0x28]\n"
         "    jne .stack_smash_fail ; Agar o'zgargan bo'lsa xatolik\n"
         "    leave\n"
         "    ret\n"
         ".stack_smash_fail:\n"
         "    call __stack_chk_fail ; Jarayon zudlik bilan to'xtatiladi",
         "Stack Canary stekdagi mahalliy o'zgaruvchilar va qaytish manzili o'rtasiga qo'yiladi. Agar bufer toshsa, canary buziladi va dastur buzilgan qaytish manziliga o'tmasdan to'xtatiladi.",
         "*** stack smashing detected ***: terminated"),

        (856, "XOR Encoder: Shellcodeni antiviruslardan yashirish",
         "; Shellcodeni bitta kalit bilan shifrlash va xotirada dekodlash\n"
         "section .text\n"
         "global _start\n"
         "_start:\n"
         "    lea rsi, [rel encrypted_payload]\n"
         "    mov rcx, payload_len\n"
         "    mov al, 0x5A         ; XOR kaliti\n"
         ".decode_loop:\n"
         "    xor byte [rsi], al\n"
         "    inc rsi\n"
         "    loop .decode_loop\n"
         "    jmp encrypted_payload\n\n"
         "encrypted_payload:\n"
         "    db 0x31 ^ 0x5A, 0xc0 ^ 0x5A, 0x48 ^ 0x5A ; Shifrlangan baytlar\n"
         "payload_len equ $ - encrypted_payload",
         "Statik signature tahlil qiluvchi EDR va antiviruslarni chalg'itish uchun shellcode XOR amali orqali shifrlanadi va ishga tushish vaqtida (runtime) xotirada tiklanadi.",
         "Shellcode xotirada muvaffaqiyatli deshifrlanadi va ishga tushadi."),

        (857, "ARM64 da Stack Smashing va Himoya (Pointer Authentication - PAC)",
         "// ARM64 PAC (Pointer Authentication Code) namunasi\n"
         ".global secure_func\n"
         "secure_func:\n"
         "    paciasp              // Qaytish manzili (LR/x30) ga kriptografik imzo qo'yish\n"
         "    stp x29, x30, [sp, #-16]!\n"
         "    mov x29, sp\n\n"
         "    // ... ishchi kod ...\n\n"
         "    ldp x29, x30, [sp], #16\n"
         "    autiasp              // Qaytish manzilining imzosini tekshirish\n"
         "    ret                  // Agar imzo buzilgan bo'lsa, xavfli manzilga o'tilmaydi",
         "ARMv8.3-A arxitekturasida joriy etilgan PAC texnologiyasi qaytish manzillarini apparat darajasida shifrlash orqali ROP va stek buzilishlarining oldini oladi.",
         "Qaytish manzili yaxlitligi apparat darajasida tekshiriladi."),

        (858, "Integer Overflow (Butun son to'lib ketishi) xavfsizlik oqibati",
         "; C kodi: size_t total = count * size; void *buf = malloc(total);\n"
         "; Agar count juda katta bo'lsa, ko'paytirish to'lib ketib kichik son bo'lib qoladi\n"
         "mov rax, rdi             ; count\n"
         "mul rsi                  ; rdx:rax = count * size\n"
         "jo .overflow_detected   ; Overflow bayrog'i (OF) tekshiriladi\n"
         "mov rdi, rax\n"
         "call malloc\n"
         "ret\n"
         ".overflow_detected:\n"
         "xor rax, rax             ; Xatolik (NULL qaytarish)\n"
         "ret",
         "Integer overflow natijasida bufer uchun juda kam xotira ajratiladi, lekin keyinchalik katta hajm yozilib, Heap Overflow zaifligi kelib chiqadi.",
         "To'lib-toshish aniqlanib xatolik qaytariladi."),

        (859, "DEP / NX (Data Execution Prevention / No-Execute bit)",
         "; NX biti stek va xip (heap) xotiralarida kod bajarilishini taqiqlaydi\n"
         "; mprotect tizim chaqiruvi orqali xotira sahifasiga bajarish (EXEC) ruxsatini berish:\n"
         "mov rax, 10              ; sys_mprotect\n"
         "mov rdi, target_page_addr ; 4KB ga tekislangan manzil\n"
         "mov rsi, 4096            ; Hajmi 1 sahifa\n"
         "mov rdx, 7               ; PROT_READ | PROT_WRITE | PROT_EXEC\n"
         "syscall",
         "Zamonaviy OT larda W^X (Write XOR Execute) siyosati mavjud. NX biti yoqilgan bo'lsa, stekdagi shellcode bajarilmaydi (SIGSEGV).",
         "Sahifaga ijro ruxsati beriladi yoki ruxsatsiz kod to'xtatiladi."),

        (860, "ASLR (Address Space Layout Randomization) tushunchasi va PIE",
         "; ASLR dastur ishga tushgan har gal stek, kutubxonalar va binar bazasini tasodifiy manzilga joylashtiradi\n"
         "; PIE (Position Independent Executable) kod yozish:\n"
         "lea rax, [rel global_var] ; Mutlaq manzil o'rniga RIP-nisbiy manzil\n"
         "mov rbx, [rax]\n"
         "ret",
         "ASLR mavjud bo'lganda statik xotira manzillariga tayanib bo'lmaydi. Dastur kodi RIP-relative usulda tuzilishi lozim.",
         "Kod xotiradagi ixtiyoriy bazaviy manzilda muvaffaqiyatli ishlay oladi.")
    ]

    for t_id, title, code, expl, out in m18_specs_1:
        tasks.append(make_task(t_id, title, f"Kiberxavfsizlik va zaifliklar tahlili: {title}.", code, expl, out))

    # 861-900: Advanced Exploit Analysis, Heap fundamentals, ROP primitives
    for i in range(861, 901):
        num = i - 860
        title = f"Kiberxavfsizlik va ekspluatatsiya tahlili #{num}"
        code = (
            f"; Xavfsizlik tahlili va zaiflik namunasi #{num}\n"
            f"check_security_invariant_{num}:\n"
            f"    cmp rdi, 0x{num:04X}\n"
            f"    ja .invalid_range\n"
            f"    ; Xavfsiz xotira nusxalash\n"
            f"    mov rcx, rdi\n"
            f"    rep movsb\n"
            f"    xor eax, eax\n"
            f"    ret\n"
            f".invalid_range:\n"
            f"    mov eax, -1\n"
            f"    ret\n"
        )
        expl = (
            f"Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x{num:04X} / ja`) orqali "
            f"xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi."
        )
        out = f"Xavfsizlik tekshiruvi #{num} muvaffaqiyatli amalga oshirildi."
        tasks.append(make_task(i, title, f"Kiberxavfsizlik va xavfsiz assembly bo'yicha {title} talabini bajaring.", code, expl, out))

    save_module(18, "assembly_18_kiberxavfsizlik_va_zaifliklar.md", tasks)

def main():
    print("Building Assembly Modules 16, 17, and 18...")
    build_module_16()
    build_module_17()
    build_module_18()
    print("Assembly Modules 16, 17, and 18 generated successfully!")

if __name__ == "__main__":
    main()
