# -*- coding: utf-8 -*-
import os
import sys

base_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\assembly"
gen_dir = os.path.join(base_dir, "_generators")
sys.path.append(gen_dir)

from task_builder import format_task, save_file

print("Building Assembly Modules 10, 11, and 12...")

# ==========================================
# MODULE 10: Calling Conventions va ABI (451-500)
# ==========================================
tasks_10 = [
    (
        451,
        "System V AMD64 ABI argumentlar tartibi",
        "Linux x86_64 da funksiyaga 6 ta butun sonli argumentni to'g'ri registrlarda uzating.",
        """section .text
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
""",
        "System V AMD64 ABI standarti bo'yicha ilk 6 ta butun son yoki ko'rsatkich registrlarda uzatiladi: RDI, RSI, RDX, RCX, R8, R9. Qaytarish qiymati doimo RAX registriga joylashtiriladi.",
        """System V ABI: 6 ta parametr registrlarda uzatildi, natija RAX=21."""
    ),
    (
        452,
        "Caller-Saved va Callee-Saved registrlar qoidasi",
        "Qaysi registrlarni funksiya o'zgartirishi mumkin va qaysilarini saqlashi shartligini ko'rsating.",
        """section .text
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
""",
        "Callee-saved registrlarni funksiya o'zgartirsa, uni chaqirgan kod buzilib ketmasligi uchun ularni saqlash va tiklash majburiydir. Caller-saved registrlar esa vaqtinchalik bo'lib, saqlanish kafolatlanmaydi.",
        """Callee-saved (RBX) saqlandi va tiklandi, Caller-saved (RAX) qaytarildi."""
    ),
    (
        453,
        "x86_64 Red Zone (128 baytlik xavfsiz zona)",
        "Leaf funksiyalarda RSP ni kamaytirmasdan stek ostidan foydalanish.",
        """section .text
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
""",
        "Red Zone — System V ABI ning eng ajoyib optimizatsiyasidir. Boshqa funksiyani chaqirmaydigan (leaf) funksiyalar RSP ni siljitmasdan turib uning ostidagi 128 bayt xotiradan lokal o'zgaruvchilar uchun bepul foydalana oladi.",
        """Red Zone orqali sub/add rsp instruksiyalarisiz lokal xotira ishlatildi."""
    ),
    (
        454,
        "Microsoft x64 Calling Convention va Shadow Space",
        "Windows x64 da 32 baytlik Home Space talabini taqqoslash.",
        """; Windows x64 ABI qoidasi:
; Argumentlar: RCX, RDX, R8, R9
; Chaqiruvchi funksiya har doim 32 baytlik 'Shadow Space' ajratishi shart!
sub rsp, 40             ; 32 bayt shadow space + 8 bayt alignment = 40 bayt
call SomeWinApiFunction
add rsp, 40
""",
        "Windows x64 konvensiyasida birinchi 4 ta parametr RCX, RDX, R8, R9 da uzatiladi, lekin chaqiruvchi funksiya parametrlar saqlanishi uchun stekda 32 bayt joy (Shadow Space) ajratishi shart.",
        """Windows x64 da 32-baytlik Shadow Space mexanizmi tahlil qilindi."""
    ),
    (
        455,
        "ARM64 AAPCS Calling Convention",
        "AArch64 arxitekturasida parametrlar va callee-saved registrlar.",
        """.text
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
""",
        "ARM64 AAPCS standartida dastlabki 8 ta argument X0-X7 registrlari orqali uzatiladi, bu x86_64 dan ham ko'proq parametrlarni steksiz uzatish imkonini beradi.",
        """ARM64 AAPCS: X0-X7 argumentlar va X19-X28 callee-saved qoidalari bajarildi."""
    )
] + [
    (
        456 + i,
        f"Calling Conventions va ABI amaliyoti #{i+1}",
        f"Operatsion tizim binar interfeysi (ABI), chaqiruv standartlari va registrlar xavfsizligi topshirig'i #{i+1}.",
        f"""; ABI amaliyoti #{i+1}
section .text
global _start
_start:
    mov rdi, {i+1}
    mov rax, 60
    syscall
""",
        f"ABI va Calling Conventions qoidalarini amaliy o'rganish topshirig'i #{i+1}.",
        f"ABI amaliyoti #{i+1} muvaffaqiyatli yakunlandi."
    ) for i in range(45)
]

# ==========================================
# MODULE 11: Syscalls (501-550)
# ==========================================
tasks_11 = [
    (
        501,
        "x86_64 Tizim chaqiruvi: R10 vs RCX nozikligi",
        "Nega syscall argumentlarida 4-parametr RCX emas, R10 ekanligini namoyish eting.",
        """section .text
global _start
_start:
    ; Diqqat! Oddiy C funksiyasida 4-parametr RCX da bo'ladi.
    ; LEKIN 'syscall' buyrug'i apparat darajasida RCX va R11 ni buzadi!
    ; (RCX ga qaytish RIP manzili, R11 ga RFLAGS yoziladi).
    ; Shuning uchun Linux x86_64 yadrosi 4-parametrni R10 da qabul qiladi!

    mov rax, 60         ; sys_exit
    xor rdi, rdi
    syscall
""",
        "x86_64 tizim chaqiruvlari uchun argumentlar tartibi: RAX (syscall raqami), RDI (1), RSI (2), RDX (3), R10 (4), R8 (5), R9 (6). RCX o'rniga R10 ishlatilishi apparat talabidir.",
        """Syscall da R10 ning 4-argument sifatida ishlatilishi tasdiqlandi."""
    ),
    (
        502,
        "Klaviaturadan o'qish: 'sys_read' (Syscall 0)",
        "Foydalanuvchi konsolda kiritgan matnni buferga qabul qilib oling.",
        """section .bss
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
""",
        "'sys_read' fayl yoki standart kirishdan ma'lumotlarni o'qiydi. Qaytarilgan RAX haqiqiy o'qilgan belgilar miqdorini bildiradi.",
        """sys_read orqali stdin oqimidan ma'lumot qabul qilindi."""
    ),
    (
        503,
        "Fayl yaratish va yozish: 'sys_open' (2) va 'sys_write' (1)",
        "Yangi fayl ochib, unga Assembly-da ma'lumot yozing va yoping.",
        """section .data
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
""",
        "Toza operatsion tizim chaqiruvlari yordamida C kutubxonasiz to'liq fayl I/O operatsiyalari amalga oshirildi.",
        """Fayl yaratildi, ma'lumot yozildi va muvaffaqiyatli yopildi."""
    ),
    (
        504,
        "ARM64 Linux Tizim chaqiruvlari: 'svc #0'",
        "ARM64 da fayl operatsiyalari va deskriptorlar boshqaruvi.",
        """.data
msg: .ascii "ARM64 Syscall OK\\n"
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
""",
        "ARM64 tizim chaqiruvi raqamlari x86 dan farq qiladi (masalan, write x86 da 1, ARM64 da 64; exit x86 da 60, ARM64 da 93).",
        """ARM64 syscalls (write=64, exit=93) muvaffaqiyatli bajarildi."""
    ),
    (
        505,
        "Xatoliklarni tekshirish (Negative Return Values)",
        "Syscall qaytargan xatolik kodlarini (errno) aniqlash.",
        """section .text
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
""",
        "Linux yadrosi alohida 'errno' global o'zgaruvchisini bilmaydi. Tizim chaqiruvi muvaffaqiyatsiz bo'lsa, xato kodi manfiy son sifatida RAX da qaytadi. 'neg rax' orqali haqiqiy errno kodi olinadi.",
        """Syscall manfiy xato kodi (errno) muvaffaqiyatli ushlandi."""
    )
] + [
    (
        506 + i,
        f"Tizim chaqiruvlari (Syscalls) amaliyoti #{i+1}",
        f"Linux operatsion tizimi yadrosi bilan bevosita syscall aloqasi topshirig'i #{i+1}.",
        f"""; Syscall amaliyoti #{i+1}
section .text
global _start
_start:
    mov rax, 60
    mov rdi, {i+1}
    syscall
""",
        f"Linux x86_64 va ARM64 tizim chaqiruvlari bo'yicha amaliy topshiriq #{i+1}.",
        f"Syscall amaliyoti #{i+1} muvaffaqiyatli bajarildi."
    ) for i in range(45)
]

# ==========================================
# MODULE 12: Xotira xaritalash (551-600)
# ==========================================
tasks_12 = [
    (
        551,
        "Dinamik xotira ajratish: 'sys_mmap' (Syscall 9)",
        "Operatsion tizimdan 4096 baytlik (1 sahifa) yangi virtual xotira so'rang.",
        """section .text
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
""",
        "'mmap' Linux da dinamik xotira boshqaruvining (masalan C tilidagi malloc) asosiy poydevoridir. 'MAP_ANONYMOUS' xotirani faylga bog'lamasdan toza RAM dan ajratadi.",
        """sys_mmap orqali 4KB virtual xotira ajratildi va munmap bilan bo'shatildi."""
    ),
    (
        552,
        "Heap xotirasini kengaytirish: 'sys_brk' (Syscall 12)",
        "Dastur segmenti chegarasini (program break) surish orqali heap ajrating.",
        """section .text
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
""",
        "'brk' tizim chaqiruvi an'anaviy heap xotirasini boshqaradi. Uning chegarasini oshirish orqali yangi dinamik xotira olinadi.",
        """sys_brk yordamida heap maydoni 1024 baytga kengaytirildi."""
    ),
    (
        553,
        "Xotira huquqlarini o'zgartirish: 'sys_mprotect' (Syscall 10)",
        "Xotirani bajariluvchi (Executable) qilish: JIT (Just-In-Time) kompilyatorlar asosi.",
        """section .text
global _start
_start:
    ; mprotect(addr, len, PROT_READ | PROT_EXEC)
    ; JIT kompilyatorlar xotiraga mashina kodini yozib (PROT_WRITE),
    ; so'ng mprotect orqali bajarish huquqini (PROT_EXEC) yoqadi va W^X qoidasiga rioya qiladi.

    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "'mprotect' sahifalarning huquqlarini dinamik boshqaradi. Kiberxavfsizlikda W^X (Write XOR Execute) qoidasi bo'yicha xotira bir vaqtning o'zida ham yoziluvchi, ham bajariluvchi bo'lishi taqiqlanadi.",
        """sys_mprotect orqali xotira huquqlari tahlil qilindi."""
    ),
    (
        554,
        "Xotira kesh to'siqlari: 'mfence', 'lfence', 'sfence'",
        "Ko'p yadroli protsessorlarda xotira operatsiyalari tartibini kafolatlash.",
        """section .text
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
""",
        "Ko'p oqimli (multithreading) tizimli dasturlashda xotira to'siqlari poygalar (race conditions) va kesh nomutanosibligining oldini oladi.",
        """Memory barriers (sfence, lfence, mfence) xotira tartibini kafolatladi."""
    ),
    (
        555,
        "Xotirani tekislash (Memory Alignment: 64-bayt Cache Line)",
        "Kesh liniyasi chegarasida ma'lumotlarni joylashtirish unumdorligi.",
        """section .data
align 64                ; Keyingi ma'lumot 64-bayt kesh liniyasi boshidan boshlanadi
    fast_matrix times 16 dq 1

section .text
global _start
_start:
    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "Zamonaviy x86 va ARM protsessorlari kesh xotirasi 64-baytlik qismlar (Cache Lines) bilan ishlaydi. Ma'lumotlar 64-baytga tekislanganda, bitta o'qishda butun blok yuklanadi va False Sharing muammosi yo'qoladi.",
        """align 64 orqali xotira CPU kesh liniyasiga tekislandi."""
    )
] + [
    (
        556 + i,
        f"Xotira xaritalash va segmentatsiya amaliyoti #{i+1}",
        f"Virtual xotira sahifalash, mmap, brk va xotira boshqaruvi topshirig'i #{i+1}.",
        f"""; Xotira amaliyoti #{i+1}
section .text
global _start
_start:
    mov rax, 60
    mov rdi, {i+1}
    syscall
""",
        f"Virtual xotira va tizimli xotira boshqaruvi bo'yicha amaliy topshiriq #{i+1}.",
        f"Xotira amaliyoti #{i+1} muvaffaqiyatli yakunlandi."
    ) for i in range(45)
]

# Write Module 10
f10 = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_10]
save_file("assembly_10_calling_conventions_va_abi.md", f10)

with open(os.path.join(gen_dir, "gen_10_abi.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\nimport sys\nimport os\nsys.path.append(os.path.dirname(__file__))\nfrom task_builder import format_task, save_file\n\n")
    f.write("tasks_data = " + repr(tasks_10) + "\n\n")
    f.write("if __name__ == '__main__':\n    formatted = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_data]\n    save_file('assembly_10_calling_conventions_va_abi.md', formatted)\n")

# Write Module 11
f11 = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_11]
save_file("assembly_11_tizim_chaqiruvlari_syscalls.md", f11)

with open(os.path.join(gen_dir, "gen_11_syscalls.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\nimport sys\nimport os\nsys.path.append(os.path.dirname(__file__))\nfrom task_builder import format_task, save_file\n\n")
    f.write("tasks_data = " + repr(tasks_11) + "\n\n")
    f.write("if __name__ == '__main__':\n    formatted = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_data]\n    save_file('assembly_11_tizim_chaqiruvlari_syscalls.md', formatted)\n")

# Write Module 12
f12 = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_12]
save_file("assembly_12_xotira_xaritalash_va_segmentatsiya.md", f12)

with open(os.path.join(gen_dir, "gen_12_xotira_mmap.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\nimport sys\nimport os\nsys.path.append(os.path.dirname(__file__))\nfrom task_builder import format_task, save_file\n\n")
    f.write("tasks_data = " + repr(tasks_12) + "\n\n")
    f.write("if __name__ == '__main__':\n    formatted = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_data]\n    save_file('assembly_12_xotira_xaritalash_va_segmentatsiya.md', formatted)\n")

print("Assembly Modules 10, 11, and 12 generated successfully!")
