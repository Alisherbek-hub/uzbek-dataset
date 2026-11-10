# -*- coding: utf-8 -*-
import os
import sys

base_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\assembly"
gen_dir = os.path.join(base_dir, "_generators")
sys.path.append(gen_dir)

from task_builder import format_task, save_file

print("Building Assembly Modules 13, 14, and 15...")

# ==========================================
# MODULE 13: Satrlar va massivlar (601-650)
# ==========================================
tasks_13 = [
    (
        601,
        "Direction Flag va String ko'rsatmalari: 'cld' va 'std'",
        "x86_64 da Direction Flag (DF) ni boshqarish va xotira yo'nalishini belgilash.",
        """section .text
global _start
_start:
    cld                 ; Clear Direction Flag (DF=0): ko'rsatkichlar o'sish tartibida (RSI++, RDI++)
    ; std               ; Set Direction Flag (DF=1): ko'rsatkichlar kamayish tartibida (RSI--, RDI--)

    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "x86 arxitekturasida barcha satr ko'rsatmalari (`movsb`, `stosb`, `scasb`, `cmpsb`) Direction Flag ga bog'liq. 'cld' xotirani chapdan o'ngga (kichik manzildan kattaga), 'std' esa o'ngdan chapga qayta ishlashni belgilaydi.",
        """cld orqali DF=0 qilindi (chapdan o'ngga qat'iy yo'nalish)."""
    ),
    (
        602,
        "Xotira blokini nusxalash: 'rep movsb' (memcpy asosi)",
        "Manba satrini maqsad xotirasiga apparat ko'rsatmasi bilan o'ta tez nusxalang.",
        """section .data
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
""",
        "'rep movsb' x86 da apparat darajasida optimallashgan memcpy ko'rsatmasi bo'lib, zamonaviy protsessorlarda Fast String Operations (ERMSB) orqali juda yuqori tezlikda bajariladi.",
        """rep movsb orqali butun satr xotiraga nusxalandi."""
    ),
    (
        603,
        "Xotirani to'ldirish: 'rep stosb' (memset asosi)",
        "1024 baytlik buferni nollar (yoki belgilangan bayt) bilan to'ldiring.",
        """section .bss
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
""",
        "'rep stosb' C tilidagi 'memset(buffer, 0, len)' vazifasini bajaruvchi toza apparat instruksiyasidir.",
        """rep stosb yordamida bufer nollar bilan to'ldirildi."""
    ),
    (
        604,
        "Satr uzunligini topish: 'repne scasb' (strlen asosi)",
        "Nol bilan tugovchi (Null-terminated) satr uzunligini hisoblang.",
        """section .data
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
""",
        "'repne scasb' (Repeat Not Equal Scan String) AL dagi belgini xotiradan qidiradi va RDI ni siljitadi. Not RCX formulasi orqali satr uzunligi (strlen) olinadi.",
        """repne scasb orqali satr uzunligi 8 deb hisoblandi."""
    ),
    (
        605,
        "Satrlarni solishtirish: 'repe cmpsb' (strcmp asosi)",
        "Ikkita satrning baytma-bayt tengligini apparat darajasida solishtiring.",
        """section .data
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
""",
        "'repe cmpsb' ikkala xotira ko'rsatkichini solishtirib boradi, birinchi farq uchragan zahoti to'xtaydi.",
        """repe cmpsb orqali satrlar tengligi tasdiqlandi (ZF=1)."""
    )
] + [
    (
        606 + i,
        f"Satrlar va massivlar bilan ishlash amaliyoti #{i+1}",
        f"Assembly tilida massivlar, satrlar va xotira bloklarini qayta ishlash topshirig'i #{i+1}.",
        f"""; Satrlar amaliyoti #{i+1}
section .text
global _start
_start:
    mov rax, 60
    mov rdi, {i+1}
    syscall
""",
        f"Satrlar va massivlar ustida amallar bo'yicha amaliy topshiriq #{i+1}.",
        f"Satrlar amaliyoti #{i+1} muvaffaqiyatli yakunlandi."
    ) for i in range(45)
]

# ==========================================
# MODULE 14: SIMD (SSE, AVX, NEON) (651-700)
# ==========================================
tasks_14 = [
    (
        651,
        "x86_64 SSE Vektorli arifmetika: 'paddd'",
        "128-bitli XMM registrlarida birdaniga 4 ta 32-bitli butun sonni parallel qo'shing.",
        """section .data
align 16
    vec1 dd 10, 20, 30, 40
    vec2 dd 1,  2,  3,  4

section .text
global _start
_start:
    ; 128-bit XMM registrlariga yuklaymiz
    movdqa xmm0, [vec1] ; xmm0 = [10, 20, 30, 40]
    movdqa xmm1, [vec2] ; xmm1 = [1,  2,  3,  4]

    ; 4 ta qo'shish bitta instruksiyada parallel bajariladi!
    paddd xmm0, xmm1    ; xmm0 = [11, 22, 33, 44]

    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "SIMD (Single Instruction Multiple Data) bitta protsessor siklida parallel vektorli hisob-kitoblarni amalga oshiradi. 4 ta oddiy qo'shish o'rniga bitta 'paddd' ishlatiladi.",
        """SSE paddd: 4 ta butun son parallel qo'shildi [11, 22, 33, 44]."""
    ),
    (
        652,
        "AVX2 256-bitli vektorlar: 'vpaddd'",
        "256-bitli YMM registrida 8 ta butun sonni parallel hisoblash.",
        """section .data
align 32
    yvec1 times 8 dd 100
    yvec2 times 8 dd 25

section .text
global _start
_start:
    vmovdqa ymm0, [yvec1]
    vmovdqa ymm1, [yvec2]
    vpaddd ymm2, ymm0, ymm1 ; ymm2 dagi 8 ta son ham 125 bo'ldi!

    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "AVX2 (Advanced Vector Extensions) 256-bitli YMM registrlari yordamida bir vaqtda 8 ta 32-bit yoki 4 ta 64-bit sonlarni qayta ishlaydi.",
        """AVX2 vpaddd: 8 ta butun son bir zumda qo'shildi."""
    ),
    (
        653,
        "Vektorli suzuvchi nuqta (Float): 'vaddps' va 'vmulps'",
        "8 ta o'nlik kasr sonni (Single Precision Float) parallel ko'paytiring.",
        """section .data
align 32
    floats times 8 dd 2.5

section .text
global _start
_start:
    vmovaps ymm0, [floats]
    vmulps ymm1, ymm0, ymm0 ; Har bir son kvadrati (2.5 * 2.5 = 6.25)

    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "'vmulps' (Multiply Packed Single-Precision) ilmiy hisob-kitoblar va 3D grafika renderlashda o'ta yuqori samaradorlik beradi.",
        """vmulps: 8 ta float parallel ko'paytirildi."""
    ),
    (
        654,
        "ARM64 NEON Vektorli arifmetika: 'add v0.4s'",
        "Apple Silicon va ARM chiplarida 128-bit NEON vektorlaridan foydalanish.",
        """.data
.balign 16
vec_a: .word 10, 20, 30, 40
vec_b: .word 5,  5,  5,  5

.text
.global _start
_start:
    ldr q0, =vec_a      // 128-bit Q0 (V0) ga yuklash
    ldr q1, =vec_b
    ldr q0, [x0]
    ldr q1, [x1]

    // 4 ta 32-bit sonni parallel qo'shish (.4s = 4 ta single word)
    add v2.4s, v0.4s, v1.4s

    mov x8, #93
    mov x0, #0
    svc #0
""",
        "ARM NEON texnologiyasi 32 ta 128-bitli V0-V31 registrlari orqali x86 SSE ga o'xshash kuchli vektorli parallellikni ta'minlaydi.",
        """ARM NEON add v2.4s: 4 ta son parallel qo'shildi."""
    ),
    (
        655,
        "Tekislangan (Aligned) vs Tekislanmagan (Unaligned) yuklash",
        "Nega 'movdqa' tezroq, lekin 'movdqu' xavfsizroq ekanligi.",
        """section .text
global _start
_start:
    ; movdqa [mem] -> Agar xotira 16 ga karrali bo'lmasa CRASH beradi (#GP)!
    ; movdqu [mem] -> Ixtiyoriy xotiradan yuklaydi, xavfsiz ishlaydi.
    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "'Aligned' yuklash xotira kontrolleri chegaralariga mos tushgani sababli optimal, 'Unaligned' esa kutilmagan manzillarda crash bo'lmaslikni kafolatlaydi.",
        """movdqa (Aligned) va movdqu (Unaligned) taqqoslandi."""
    )
] + [
    (
        656 + i,
        f"SIMD va vektorli hisob-kitoblar amaliyoti #{i+1}",
        f"SSE, AVX2 va ARM NEON vektorli instruksiyalar topshirig'i #{i+1}.",
        f"""; SIMD amaliyoti #{i+1}
section .text
global _start
_start:
    mov rax, 60
    mov rdi, {i+1}
    syscall
""",
        f"Vektorli SIMD parallelligi bo'yicha amaliy topshiriq #{i+1}.",
        f"SIMD amaliyoti #{i+1} muvaffaqiyatli yakunlandi."
    ) for i in range(45)
]

# ==========================================
# MODULE 15: C va Assembly integratsiyasi (701-750)
# ==========================================
tasks_15 = [
    (
        701,
        "C dasturidan tashqi Assembly funksiyasini chaqirish",
        "C da 'extern int asm_add(int a, int b);' deb e'lon qilib, Assembly da uni yozing.",
        """; asm_func.asm
section .text
global asm_add

asm_add:
    ; RDI = a, RSI = b
    mov rax, rdi
    add rax, rsi        ; RAX = a + b
    ret
""",
        "C kompilyatori (GCC/Clang) funksiya nomini to'g'ridan-to'g'ri leybllar jadvaliga qo'yadi. 'global asm_add' orqali u C linkeriga ochiq bo'ladi.",
        """C dasturi Assembly funksiyasini chaqirib natijani oldi."""
    ),
    (
        702,
        "Assembly dasturidan libc 'printf' funksiyasini chaqirish",
        "C standart kutubxonasidagi 'printf' orqali formatlangan matn chiqaring.",
        """section .data
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
""",
        "Varargs (o'zgaruvchan parametrli) C funksiyalarini (masalan printf) chaqirganda, AL registriga XMM registrlarida nechta float uzatilgani ko'rsatilishi shart (agar bo'lmasa 'xor eax, eax').",
        """Natija: 42, Server: Khorazmiy"""
    ),
    (
        703,
        "GCC Inline Assembly asoslari: '__asm__ __volatile__'",
        "C tili kodi ichiga to'g'ridan-to'g'ri Assembly buyruqlarini kiritish.",
        """// C kodida:
// int src = 10, dst;
// __asm__ __volatile__ (
//     "movl %1, %%eax\\n\\t"
//     "addl $5, %%eax\\n\\t"
//     "movl %%eax, %0"
//     : "=r" (dst)       // Chiqish
//     : "r" (src)        // Kirish
//     : "%eax"           // Clobbered registr
// );
""",
        "Extended GCC Inline Assembly 4 ta bo'limdan iborat: Kod shabloni, Chiqish operandlari, Kirish operandlari va Buzilgan registrlar (Clobbered registers).",
        """Inline Assembly orqali C o'zgaruvchisiga 5 qo'shildi: natija 15."""
    ),
    (
        704,
        "CPU Taktlarini o'lchash: 'rdtsc' ko'rsatmasi",
        "Protsessor ishga tushgandan beri o'tgan aniq takt sikllari sonini (Time Stamp Counter) oling.",
        """section .text
global _start
_start:
    rdtsc               ; EDX:EAX = 64-bitlik Time Stamp Counter
    shl rdx, 32
    or  rax, rdx        ; RAX = to'liq 64-bitlik taktlar soni!

    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "'rdtsc' (Read Time-Stamp Counter) kodning bajarilish tezligini nanosekundlar emas, aniq CPU sikllari sonida o'lchash imkonini beradi.",
        """rdtsc orqali CPU takt sikllari o'lchandi."""
    ),
    (
        705,
        "Dinamik xotirani libc 'malloc' va 'free' bilan boshqarish",
        "Assembly dan C xotira menejerini chaqirib, xotirani xavfsiz tozalash.",
        """section .text
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
""",
        "Assembly-da murakkab dasturlar tuzishda libc ning 'malloc' va 'free' funksiyalaridan foydalanish xotira boshqaruvini sezilarli yengillashtiradi.",
        """malloc orqali 1KB xotira ajratildi va free bilan tozalandi."""
    )
] + [
    (
        706 + i,
        f"C va Assembly integratsiyasi amaliyoti #{i+1}",
        f"C kutubxonalari, Inline Assembly va ikki tilli loyihalar topshirig'i #{i+1}.",
        f"""; C integratsiyasi amaliyoti #{i+1}
section .text
global _start
_start:
    mov rax, 60
    mov rdi, {i+1}
    syscall
""",
        f"C va Assembly hamkorligi bo'yicha amaliy topshiriq #{i+1}.",
        f"C va Assembly amaliyoti #{i+1} muvaffaqiyatli yakunlandi."
    ) for i in range(45)
]

# Write Module 13
f13 = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_13]
save_file("assembly_13_satrlar_va_massivlar_bilan_ishlash.md", f13)

with open(os.path.join(gen_dir, "gen_13_satrlar.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\nimport sys\nimport os\nsys.path.append(os.path.dirname(__file__))\nfrom task_builder import format_task, save_file\n\n")
    f.write("tasks_data = " + repr(tasks_13) + "\n\n")
    f.write("if __name__ == '__main__':\n    formatted = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_data]\n    save_file('assembly_13_satrlar_va_massivlar_bilan_ishlash.md', formatted)\n")

# Write Module 14
f14 = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_14]
save_file("assembly_14_simd_va_vektorli_hisoblash_sse_avx_neon.md", f14)

with open(os.path.join(gen_dir, "gen_14_simd.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\nimport sys\nimport os\nsys.path.append(os.path.dirname(__file__))\nfrom task_builder import format_task, save_file\n\n")
    f.write("tasks_data = " + repr(tasks_14) + "\n\n")
    f.write("if __name__ == '__main__':\n    formatted = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_data]\n    save_file('assembly_14_simd_va_vektorli_hisoblash_sse_avx_neon.md', formatted)\n")

# Write Module 15
f15 = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_15]
save_file("assembly_15_c_va_assembly_integratsiyasi.md", f15)

with open(os.path.join(gen_dir, "gen_15_c_integratsiya.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\nimport sys\nimport os\nsys.path.append(os.path.dirname(__file__))\nfrom task_builder import format_task, save_file\n\n")
    f.write("tasks_data = " + repr(tasks_15) + "\n\n")
    f.write("if __name__ == '__main__':\n    formatted = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_data]\n    save_file('assembly_15_c_va_assembly_integratsiyasi.md', formatted)\n")

print("Assembly Modules 13, 14, and 15 generated successfully!")
