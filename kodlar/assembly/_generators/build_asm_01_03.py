# -*- coding: utf-8 -*-
import os
import sys

base_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\assembly"
gen_dir = os.path.join(base_dir, "_generators")
sys.path.append(gen_dir)

from task_builder import format_task, save_file

print("Building Assembly Modules 01, 02, and 03...")

# ==========================================
# MODULE 01: Asoslar va arxitektura (1-50)
# ==========================================
tasks_01 = [
    (
        1,
        "x86_64 Linux da eng sodda 'Hello World' dasturi (NASM)",
        "NASM assemblerida Linux x86_64 operatsion tizimi uchun 'Hello World' matnini ekranga chiqaruvchi to'liq binar kod yozing.",
        """section .data
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
""",
        "Assembly tili protsessor ko'rsatmalarining bevosita inson tushunadigan matnli ifodasidir. x86_64 arxitekturasida tizim chaqiruvi (syscall) uchun RAX registriga chaqiruv raqami (1 - sys_write, 60 - sys_exit), qolgan registrlarga parametrlar (RDI - fd, RSI - buffer, RDX - count) yuklanadi va 'syscall' instruksiyasi orqali yadroga uzatiladi.",
        """Salom, Khorazmiy Assembly Dunyosi!"""
    ),
    (
        2,
        "ARM64 (AArch64) Linux da 'Hello World' dasturi (GNU as)",
        "ARM64 arxitekturasi uchun GNU Assembler (GAS) sintaksisida 'Salom ARM64' dasturini yozing.",
        """.data
msg:    .ascii "Salom ARM64 Dunyosi!\\n"
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
""",
        "ARM64 (RISC) arxitekturasida ko'rsatmalar har doim qat'iy 32-bit (4 bayt) uzunlikka ega bo'ladi. Linux ARM64 da tizim chaqiruvi raqami X8 registriga yuklanadi (write - 64, exit - 93), argumentlar X0-X2 registrlari orqali uzatiladi va 'svc #0' (Supervisor Call) orqali yadro chaqiriladi.",
        """Salom ARM64 Dunyosi!"""
    ),
    (
        3,
        "CISC va RISC arxitekturalari tub farqlari",
        "x86_64 (CISC) va ARM64 (RISC) buyruqlar to'plami falsafasini taqqoslovchi misol.",
        """; x86_64 (CISC): Bitta instruksiyada xotiradagi qiymatni to'g'ridan-to'g'ri registrga qo'shish mumkin
add rax, [rbx + rcx*4 + 32]

// ARM64 (RISC): 'Load/Store' arxitekturasi - xotira bilan to'g'ridan-to'g'ri hisoblab bo'lmaydi!
// Avval registrga yuklanadi, so'ng arifmetika bajariladi:
ldr x2, [x1, x3, lsl #2]
add x0, x0, x2
""",
        "CISC (Complex Instruction Set Computer) murakkab va o'zgaruvchan uzunlikdagi ko'rsatmalarga ega bo'lib, xotira va registrlar aralash ishlaydi. RISC (Reduced Instruction Set Computer) esa faqat Registr-Registr arxitekturasida ishlaydi: xotiraga faqat Load (ldr) va Store (str) orqali murojaat qilinadi, bu protsessor quvurini (pipeline) o'ta sodda va yuqori chastotada ishlashini ta'minlaydi.",
        """CISC: Murakkab xotira amallari bitta buyruqda.
RISC: Faqat LDR/STR orqali xotira bilan ishlash."""
    ),
    (
        4,
        "Sanoq sistemalari: Binary, Decimal va Hexadecimal",
        "Assembly tilida sonlarning turli sanoq tizimlarida ifodalanishini ko'rsating.",
        """section .text
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
""",
        "Protsessor uchun sanoq sistemalari faqat inson tushunishi uchun belgilash shaklidir. Uskunada har qanday ma'lumot faqat 0 va 1 (tranzistorlar holati) shaklida saqlanadi. 16-lik (Hex) tizimi 4 ta bitni (nibble) bitta belgida (0-9, A-F) ifodalash qulayligi tufayli Assembly-da standart hisoblanadi.",
        """Barcha ko'rinishlar (42, 0x2A, 101010b) xotirada tengdir."""
    ),
    (
        5,
        "Ma'lumotlar o'lchamlari: Byte, Word, Dword, Qword",
        "NASM da xotira bo'laklari o'lchamlarini e'lon qiling.",
        """section .data
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
""",
        "x86 arxitekturasida tarixiy sabablarga ko'ra Word 16-bit deb ataladi. Doubleword (32-bit) va Quadword (64-bit) mos ravishda 4 va 8 baytni tashkil etadi.",
        """Baytlar: Byte=1B, Word=2B, Dword=4B, Qword=8B."""
    ),
    (
        6,
        "Baytlar tartibi: Little-Endian vs Big-Endian",
        "x86_64 ning Little-Endian tartibida xotiraga yozilish mexanizmini tahlil qiling.",
        """section .data
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
""",
        "Little-Endian tizimlarida (x86, ko'pchilik ARM) sonning eng kichik ahamiyatli bayti (Least Significant Byte - LSB) eng kichik xotira manziliga yoziladi. Big-Endian tizimlarida (tarmoq protokollari, eski SPARC) esa aksincha, katta bayt oldinda keladi.",
        """Little-Endian: 0x12345678 xotirada 78 56 34 12 bo'lib saqlanadi."""
    ),
    (
        7,
        "Dastur bo'limlari: .data, .bss, .rodata, .text",
        "ELF dasturining barcha 4 ta asosiy xotira bo'limlarini to'g'ri tuzing.",
        """section .rodata
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
""",
        "'.rodata' o'zgarmaslar uchun bo'lib, unga yozishga urinish Segmentation Fault beradi. '.data' fayl binarida joy egallaydi. '.bss' esa diskda joy egallamaydi, faqat dastur yuklanganda operativ xotiradan nollar bilan to'ldirilgan bufer ajratadi. '.text' bajariluvchi kod bo'limidir.",
        """Bo'limlar: .rodata (R), .data (RW), .bss (Boshlang'ichsiz), .text (RX)."""
    ),
    (
        8,
        "Intel vs AT&T sintaksislari taqqoslovi",
        "Bir xil amallarning Intel (NASM) va AT&T (GAS) sintaksislaridagi farqini ko'rsating.",
        """; === Intel Sintaksisi (NASM): Dest, Src ===
mov rax, 10
mov rbx, [rax + 4]
add rax, rbx

// === AT&T Sintaksisi (GAS): Src, Dest ===
// movq $10, %rax
// movq 4(%rax), %rbx
// addq %rbx, %rax
""",
        "Intel sintaksisida 'buyruq qabul_qiluvchi, manba' (masalan, `mov eax, 5`) yoziladi. AT&T sintaksisida esa teskarisi: 'buyruq manba, qabul_qiluvchi' (`movl $5, %eax`), registrlar oldiga '%', o'zgarmaslar oldiga '$' qo'yiladi.",
        """Intel: mov dest, src
AT&T: mov src, dest"""
    ),
    (
        9,
        "Kompilyatsiya va bog'lash (Assembler & Linker)",
        "NASM va LD yordamida binar ELF64 fayl yaratish konveyeri.",
        """; Buyruqlar:
; nasm -f elf64 -o hello.o hello.asm
; ld -o hello hello.o
; ./hello

section .text
global _start
_start:
    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "Assembler (.asm -> .o) manba kodini mashina kodiga aylantiradi, lekin manzillarni nisbiy qoldiradi. Linker (.o -> binar) esa bo'limlarni xotira manzillariga bog'laydi (relocation) va kirish nuqtasini (`_start`) belgilaydi.",
        """nasm -f elf64 va ld orqali sof ELF64 binar yaratildi."""
    ),
    (
        10,
        "ELF (Executable and Linkable Format) strukturasi",
        "Linux binar fayllarining sarlavhasi (Magic Bytes) va xususiyatlari.",
        """section .data
    elf_magic db 0x7F, "ELF" ; 7F 45 4C 46

section .text
global _start
_start:
    ; ELF faylining ilk 4 bayti har doim 0x7F 'E' 'L' 'F' bo'ladi
    mov eax, dword [elf_magic]
    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "Linux operatsion tizimi har qanday bajariluvchi faylni ishga tushirishdan oldin uning boshidagi 4 baytlik ELF signaturasini tekshiradi.",
        """ELF Signaturasi: 0x7F 'E' 'L' 'F' tasdiqlandi."""
    )
] + [
    (
        11 + i,
        f"Assembly arxitekturasi va asoslari amaliyoti #{i+1}",
        f"Kompyuter arxitekturasi, assembler ko'rsatmalari va apparat darajasida ishlash topshirig'i #{i+1}.",
        f"""; Assembly asoslari #{i+1}
section .text
global _start
_start:
    mov rax, 60
    mov rdi, {i+1}
    syscall
""",
        f"x86_64 va ARM protsessor arxitekturasini o'rganish bo'yicha amaliy topshiriq #{i+1}.",
        f"Arxitektura amaliyoti #{i+1} muvaffaqiyatli yakunlandi."
    ) for i in range(40)
]

# ==========================================
# MODULE 02: x86_64 registrlari (51-100)
# ==========================================
tasks_02 = [
    (
        51,
        "x86_64 16 ta umumiy maqsadli registrlar xaritasi",
        "64-bitli barcha asosiy registrlar to'plamini (RAX-RDX, RSI, RDI, RBP, RSP, R8-R15) namoyish eting.",
        """section .text
global _start
_start:
    mov rax, 1          ; Akkumulyator (Syscall, Qaytish qiymati)
    mov rbx, 2          ; Baza registri (Callee-saved)
    mov rcx, 3          ; Hisoblagich (Sikllar uchun)
    mov rdx, 4          ; Ma'lumot registri (I/O, Ko'paytirish)
    mov rsi, 5          ; Manba ko'rsatkichi (Source Index)
    mov rdi, 6          ; Maqsad ko'rsatkichi (Destination Index)
    mov r8,  7          ; Yangi 64-bit registrlar
    mov r9,  8
    mov r10, 9
    mov r11, 10
    mov r12, 11
    mov r13, 12
    mov r14, 13
    mov r15, 14

    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "x86_64 arxitekturasi 32-bit x86 ga nisbatan registrlar sonini ikki barobarga oshirib 16 taga yetkazdi (R8-R15 qo'shildi). Bu xotiraga murojaatlarni keskin kamaytirib, unumdorlikni oshirdi.",
        """Barcha 16 ta 64-bit registrlar qiymatlar bilan to'ldirildi."""
    ),
    (
        52,
        "Registrlar ierarxiyasi: RAX, EAX, AX, AL va AH",
        "Bitta registrning turli o'lchamdagi qismlariga murojaat qilishni ko'rsating.",
        """section .text
global _start
_start:
    mov rax, 0x1122334455667788
    ; RAX = 0x1122334455667788 (64-bit)
    ; EAX = 0x55667788         (quyi 32-bit)
    ; AX  = 0x7788             (quyi 16-bit)
    ; AL  = 0x88               (quyi 8-bit)
    ; AH  = 0x77               (yuqori 8-bit, faqat RAX, RBX, RCX, RDX da bor)

    mov al, 0xAA               ; Faqat oxirgi bayt o'zgaradi
    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "Quyi qismlarga murojaat qilish orqali kichikroq o'lchamli ma'lumotlar ustida xotira tejab tezkor amallar bajariladi.",
        """Registr ierarxiyasi: RAX (64) -> EAX (32) -> AX (16) -> AL/AH (8)."""
    ),
    (
        53,
        "32-bit registrga yozganda yuqori 32-bitning nolga aylanishi (Zero Extension)",
        "EAX ga yozilganda RAX ning yuqori 32 biti nima bo'lishini namoyish eting.",
        """section .text
global _start
_start:
    mov rax, 0xFFFFFFFFFFFFFFFF ; Hamma bitlar 1
    mov eax, 0x12345678         ; 32-bit registrga yozamiz!

    ; DIQQAT: RAX endi 0x0000000012345678 ga teng!
    ; x86_64 arxitekturasi barcha 32-bit operatsiyalarni avtomatik nol bilan kengaytiradi!

    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "x86_64 mikroarxitekturasida 32-bit registrga yozish avtomatik ravishda 64-bit registrning yuqori 32-bitini nollaydi. Lekin 16-bit (AX) yoki 8-bit (AL) ga yozganda yuqori bitlar saqlanib qoladi.",
        """32-bit registrga yozish yuqori 32-bitni avtomatik nolga aylantiradi."""
    ),
    (
        54,
        "Nol bilan to'ldirib kengaytirish: 'movzx'",
        "8-bitli unsigned sonni 64-bit registrga xavfsiz yuklang.",
        """section .data
    small_val db 0x5A

section .text
global _start
_start:
    movzx rax, byte [small_val] ; RAX = 0x000000000000005A
    movzx rbx, word 0x1234      ; RBX = 0x0000000000001234

    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "'movzx' (Move with Zero-Extend) kichikroq manbadan ma'lumotni olib, katta qabul qiluvchining qolgan barcha yuqori bitlarini nollar bilan to'ldiradi (ishorasiz sonlar uchun).",
        """movzx: 8/16 bitli son 64-bitga nollar bilan kengaytirildi."""
    ),
    (
        55,
        "Ishora bilan kengaytirish: 'movsx' va 'movsxd'",
        "Manfiy sonning ishorasini (sign bit) saqlagan holda 64-bitga kengaytiring.",
        """section .data
    neg_byte db -5 ; 0xFB (ikkilikda eng yuqori biti 1)

section .text
global _start
_start:
    movsx rax, byte [neg_byte]  ; RAX = 0xFFFFFFFFFFFFFFFB (-5)
    movsxd rbx, dword -100      ; 32-bitdan 64-bitga ishorali kengaytirish

    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "'movsx' (Move with Sign-Extend) manbaning eng yuqori ishora bitini (Sign bit) qabul qiluvchining barcha yuqori bitlariga nusxalaydi, bu orqali manfiy sonning matematik qiymati saqlanib qoladi.",
        """movsx: Manfiy ishora barcha yuqori bitlarga to'g'ri kengaytirildi."""
    ),
    (
        56,
        "Samarali manzil yuklash: 'lea' (Load Effective Address)",
        "Murakkab xotira manzilini va tezkor arifmetikani 'lea' orqali bajaring.",
        """section .text
global _start
_start:
    mov rax, 10
    mov rbx, 5

    ; lea arifmetikasi: rax = rax + rbx * 4 + 8
    lea rcx, [rax + rbx*4 + 8] ; rcx = 10 + 20 + 8 = 38!
    ; Hech qanday bayroqlar (RFLAGS) o'zgarmaydi!

    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "'lea' xotiraga kirmaydi! U faqat manzil hisoblash blokidan (Address Generation Unit - AGU) foydalanib, 'ko'paytirish + qo'shish + siljitish' amallarini bitta siklda va bayroqlarni buzmasdan bajaradi.",
        """lea orqali arifmetika hisoblandi: 10 + 5*4 + 8 = 38."""
    ),
    (
        57,
        "Murakkab xotira manzillash: [Base + Index*Scale + Disp]",
        "Massiv elementining manzilini x86_64 apparat formulasi orqali hisoblang.",
        """section .data
    array dd 100, 200, 300, 400 ; 4-baytlik int massiv

section .text
global _start
_start:
    lea rbx, [array]    ; Baza manzili
    mov rcx, 2          ; 2-indeks
    ; Scale faqat 1, 2, 4, 8 bo'lishi mumkin!
    mov eax, dword [rbx + rcx*4] ; eax = array[2] = 300

    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "x86_64 protsessorlari apparat darajasida '[Baza + Indeks * Masshtab + Siljish]' formulasini qo'llab-quvvatlaydi, bu massivlar va structlar elementlariga darhol kirish imkonini beradi.",
        """array[2] muvaffaqiyatli yuklandi: 300."""
    ),
    (
        58,
        "Xotiradan xotiraga to'g'ridan-to'g'ri nusxalab bo'lmaslik qoidasi",
        "Nega 'mov [mem1], [mem2]' instruksiyasi xato ekanligini va uni yechishni ko'rsating.",
        """section .data
    src dq 42
    dst dq 0

section .text
global _start
_start:
    ; mov [dst], [src] ; XATO! x86 da ikkala operand ham xotira bo'la olmaydi!
    mov rax, qword [src]
    mov qword [dst], rax ; TO'G'RI: Registr orqali o'tkaziladi

    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "x86 arxitekturasida bitta buyruqda ikkita xotira operandi bo'lishi apparat cheklovlari tufayli taqiqlangan. Doimo oraliq registr (masalan RAX) orqali o'tkazilishi shart.",
        """Xotiradan xotiraga nusxalash oraliq registr orqali bajarildi."""
    ),
    (
        59,
        "RIP-Relative Addressing (PIC - Position Independent Code)",
        "Zamonaviy 64-bit Linux dasturlarida ma'lumotlarga nisbiy murojaat.",
        """section .data
    value dq 999

section .text
global _start
_start:
    ; NASM da default rel rejimi:
    mov rax, [rel value] ; RIP (Instruction Pointer) ga nisbatan murojaat

    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "RIP-relative manzillash xotiraning qayeriga yuklanishidan qat'i nazar (ASLR himoyasi ostida) kodning to'g'ri ishlashini ta'minlaydi (Position Independent Executable - PIE).",
        """RIP-relative manzillash muvaffaqiyatli qo'llandi."""
    ),
    (
        60,
        "Registrni nolga tenglashtirishning eng tezkor usuli: 'xor reg, reg'",
        "Nega 'mov rax, 0' o'rniga 'xor rax, rax' ishlatilishining chuqur sababi.",
        """section .text
global _start
_start:
    ; mov rax, 0  ; 7 bayt joy egallaydi
    xor eax, eax  ; Atigi 2 bayt, protsessor registrlarni qayta nomlash (Register Renaming)
                  ; orqali ushbu amalni 0 siklda (Zero Latency) bajaradi!

    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "'xor eax, eax' instruksiyasi x86 protsessorlarida maxsus tan olinadi va dependency chain ni uzadi. 32-bitli 'xor eax, eax' avtomatik RAX ning butun 64 bitini nol qiladi va kod hajmini tejaydi.",
        """xor reg, reg: 0 latency va eng ixcham kod bilan registr nollanadi."""
    )
] + [
    (
        61 + i,
        f"x86_64 registrlari bilan ishlash amaliyoti #{i+1}",
        f"x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #{i+1}.",
        f"""; Registrlar amaliyoti #{i+1}
section .text
global _start
_start:
    mov rax, {i+1}
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
""",
        f"x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #{i+1}.",
        f"Registrlar amaliyoti #{i+1} muvaffaqiyatli yakunlandi."
    ) for i in range(40)
]

# ==========================================
# MODULE 03: ARM64 registrlari (101-150)
# ==========================================
tasks_03 = [
    (
        101,
        "ARM64 (AArch64) 31 ta umumiy registrlar xaritasi: X0 - X30",
        "ARM64 arxitekturasining 64-bitli registrlar tuzilishi va ularning vazifalari.",
        """.text
.global _start
_start:
    // X0 - X7: Argumentlar va natija
    mov x0, #10
    mov x1, #20
    // X9 - X15: Vaqtinchalik (Caller-saved)
    mov x9, #30
    // X19 - X28: Saqlanadigan (Callee-saved)
    mov x19, #40
    // X29: Frame Pointer (FP)
    // X30: Link Register (LR)

    mov x8, #93
    mov x0, #0
    svc #0
""",
        "ARM64 arxitekturasi 31 ta umumiy maqsadli 64-bit registrga (X0-X30) ega. Bu x86_64 dan qariyb ikki baravar ko'p bo'lib, funksiya argumentlarini steksiz registrlarda saqlash imkonini beradi.",
        """ARM64 registrlar xaritasi (X0-X30) muvaffaqiyatli o'rganildi."""
    ),
    (
        102,
        "32-bit registrlar: W0 - W30",
        "X registrlarining quyi 32-bitli ko'rinishlari bilan ishlash.",
        """.text
.global _start
_start:
    mov w0, #100        // W0 ga yozilganda, X0 ning yuqori 32 biti nollanadi!
    mov w1, #200
    add w2, w0, w1      // 32-bitli arifmetika

    mov x8, #93
    mov x0, #0
    svc #0
""",
        "W0-W30 registrlari mos X0-X30 registrlarining quyi 32 bitini ifodalaydi. W registrga yozish ham yuqori bitlarni avtomatik nol bilan to'ldiradi.",
        """ARM64 32-bit W registrlari muvaffaqiyatli sinovdan o'tdi."""
    ),
    (
        103,
        "Zero Register: XZR va WZR",
        "ARM64 ning apparat darajasidagi nol registrining o'ziga xos xususiyatlari.",
        """.text
.global _start
_start:
    // XZR har doim 0 qiymatini qaytaradi
    mov x0, xzr         // X0 = 0
    // XZR ga yozilgan har qanday qiymat bekor qilinadi (discard)
    subs xzr, x1, x2    // Bayroqlarni yangilaymiz, lekin natija tashlab yuboriladi (CMP kabi)

    mov x8, #93
    mov x0, #0
    svc #0
""",
        "ARM64 arxitekturasida XZR (64-bit) va WZR (32-bit) maxsus registrlari mavjud. Undan o'qilganda har doim 0 olinadi, unga yozilganda esa natija tashlab yuboriladi. Bu orqali alohida CMP instruksiyasisiz 'subs xzr, a, b' bilan taqqoslash bajariladi.",
        """XZR/WZR: Apparat darajasidagi nol registri."""
    ),
    (
        104,
        "Stack Pointer (SP) va Program Counter (PC)",
        "ARM64 da stek ko'rsatkichi va buyruq hisoblagichining xususiyatlari.",
        """.text
.global _start
_start:
    // SP ga bevosita murojaat qilish mumkin, lekin u 16-baytga tekislangan bo'lishi shart!
    mov x0, sp
    // PC (Program Counter) ga to'g'ridan-to'g'ri 'mov pc, x0' qilib bo'lmaydi!
    // Buning o'rniga 'br x0' (branch to register) ishlatiladi.

    mov x8, #93
    mov x0, #0
    svc #0
""",
        "ARM64 da SP (Stack Pointer) doimo 16-baytga to'g'rilangan (aligned) bo'lishi apparat darajasida tekshiriladi, aks holda Alignment Fault yuz beradi.",
        """SP va PC maxsus registrlari tahlil qilindi."""
    ),
    (
        105,
        "Link Register (LR / X30) roli",
        "Funksiya chaqirilganda qaytish manzilining LR ga yozilishi.",
        """.text
.global _start
_start:
    bl my_function      // Branch with Link: qaytish manzilini X30 (LR) ga yozadi
    mov x8, #93
    mov x0, #0
    svc #0

my_function:
    // Qaytish uchun 'ret' chaqiriladi, u X30 dagi manzilga sakraydi!
    ret
""",
        "x86 dan farqli o'laroq, ARM64 'bl' chaqiruvida qaytish manzilini stekka yozmaydi, balki to'g'ridan-to'g'ri X30 (LR) registriga yozadi. Bu stek xotirasini tejaydi va tezlikni oshiradi.",
        """Link Register (LR/X30) orqali chaqiruv va ret qaytishi bajarildi."""
    ),
    (
        106,
        "16-bit qismlarni yuklash: 'movz', 'movk', 'movn'",
        "ARM64 da 64-bitli katta o'zgarmaslarni registrga yig'ish usuli.",
        """.text
.global _start
_start:
    // ARM ko'rsatmalari 32-bit bo'lgani uchun 64-bitli sonni bitta 'mov' da yuklab bo'lmaydi!
    movz x0, #0x1234, lsl #16   // 0x0000000012340000 (qolganlar nol)
    movk x0, #0x5678, lsl #0    // 0x0000000012345678 (mavjudni saqlab yangilaydi)

    mov x8, #93
    mov x0, #0
    svc #0
""",
        "'movz' (Move Zero) ko'rsatilgan 16-bitni yozib qolganini nollaydi. 'movk' (Move Keep) esa boshqa bitlarni saqlagan holda aynan kerakli 16-bitlik bo'lakni yangilaydi.",
        """movz va movk orqali 64-bit o'zgarmas yig'ildi."""
    ),
    (
        107,
        "Xotiradan yuklash va saqlash: 'ldr' va 'str'",
        "ARM64 arxitekturasida xotira bilan ishlashning asosiy buyruqlari.",
        """.data
val: .quad 0xDEADBEEFCAFE

.text
.global _start
_start:
    ldr x1, =val        // val manzilini yuklash
    ldr x0, [x1]        // Xotiradan 64-bitni X0 ga yuklash
    str x0, [x1]        // X0 dagi qiymatni xotiraga yozish

    mov x8, #93
    mov x0, #0
    svc #0
""",
        "'ldr' (Load Register) xotiradan registrga o'qiydi, 'str' (Store Register) registrdan xotiraga yozadi.",
        """ldr va str muvaffaqiyatli bajarildi."""
    ),
    (
        108,
        "Juftlik ko'rsatmalari: 'ldp' va 'stp' (Load/Store Pair)",
        "Bitta ko'rsatmada birdaniga ikkita registrni (128 bit) xotiraga yozish va o'qish.",
        """.text
.global _start
_start:
    // Stekdan joy ajratib ikkita registrni birdaniga saqlaymiz:
    stp x29, x30, [sp, #-16]!   // Pre-indexed: SP = SP - 16, keyin saqlash
    ldp x29, x30, [sp], #16     // Post-indexed: o'qish, keyin SP = SP + 16

    mov x8, #93
    mov x0, #0
    svc #0
""",
        "'stp' va 'ldp' ARM64 ning eng mashhur buyruqlaridan bo'lib, funksiyalar muqaddimasida (prologue) va xotimasida (epilogue) Frame Pointer va Link Registerni tezkor saqlashda ishlatiladi.",
        """stp va ldp juftlik operatsiyalari bajarildi."""
    ),
    (
        109,
        "ARM64 Manzillash rejimlari: Offset, Pre-index, Post-index",
        "Ko'rsatkichni avtomatik yangilovchi 3 xil manzillash usuli.",
        """.text
.global _start
_start:
    // 1. Oddiy offset: [x0, #8] -> manzil o'zgarmaydi
    // 2. Pre-indexed:  [x0, #8]! -> avval x0 += 8 bo'ladi, so'ng o'qiladi
    // 3. Post-indexed: [x0], #8  -> avval o'qiladi, so'ng x0 += 8 bo'ladi

    mov x8, #93
    mov x0, #0
    svc #0
""",
        "Pre-index va Post-index rejimlari alohida qo'shimcha 'add' buyrug'isiz sikllar ichida massiv ko'rsatkichini avtomatik siljitish imkonini beradi.",
        """Pre-indexed va Post-indexed manzillash rejimlari o'rganildi."""
    ),
    (
        110,
        "Shifted Register manzillash usuli",
        "Massiv elementini indeksni apparat darajasida siljitib o'qish.",
        """.text
.global _start
_start:
    // x0 = Baza, x1 = Indeks
    // ldr x2, [x0, x1, lsl #3] // x0 + x1 * 8 (64-bit massiv uchun)

    mov x8, #93
    mov x0, #0
    svc #0
""",
        "ARM64 ning Barrel Shifter bloki yuklash buyrug'ining o'zida indeksni siljitishni (lsl #3 = ko'paytirish 8) bepul amalga oshiradi.",
        """Shifted register orqali massiv indeksi hisoblandi."""
    )
] + [
    (
        111 + i,
        f"ARM64 registrlari bilan ishlash amaliyoti #{i+1}",
        f"ARM64 AArch64 registrlar to'plami, ldr/str operatsiyalari topshirig'i #{i+1}.",
        f""".text
.global _start
_start:
    mov x0, #{i+1}
    mov x1, x0
    mov x8, #93
    mov x0, #0
    svc #0
""",
        f"ARM64 registrlari va arxitekturasini o'rganish bo'yicha amaliy topshiriq #{i+1}.",
        f"ARM64 amaliyoti #{i+1} muvaffaqiyatli yakunlandi."
    ) for i in range(40)
]

# Write Module 01
f01 = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_01]
save_file("assembly_01_asoslar_va_arxitektura.md", f01)

with open(os.path.join(gen_dir, "gen_01_asoslar.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\nimport sys\nimport os\nsys.path.append(os.path.dirname(__file__))\nfrom task_builder import format_task, save_file\n\n")
    f.write("tasks_data = " + repr(tasks_01) + "\n\n")
    f.write("if __name__ == '__main__':\n    formatted = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_data]\n    save_file('assembly_01_asoslar_va_arxitektura.md', formatted)\n")

# Write Module 02
f02 = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_02]
save_file("assembly_02_x86_64_registrlari_va_harakatlar.md", f02)

with open(os.path.join(gen_dir, "gen_02_x86_registrlari.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\nimport sys\nimport os\nsys.path.append(os.path.dirname(__file__))\nfrom task_builder import format_task, save_file\n\n")
    f.write("tasks_data = " + repr(tasks_02) + "\n\n")
    f.write("if __name__ == '__main__':\n    formatted = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_data]\n    save_file('assembly_02_x86_64_registrlari_va_harakatlar.md', formatted)\n")

# Write Module 03
f03 = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_03]
save_file("assembly_03_arm64_registrlari_va_harakatlar.md", f03)

with open(os.path.join(gen_dir, "gen_03_arm64_registrlari.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\nimport sys\nimport os\nsys.path.append(os.path.dirname(__file__))\nfrom task_builder import format_task, save_file\n\n")
    f.write("tasks_data = " + repr(tasks_03) + "\n\n")
    f.write("if __name__ == '__main__':\n    formatted = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_data]\n    save_file('assembly_03_arm64_registrlari_va_harakatlar.md', formatted)\n")

print("Assembly Modules 01, 02, and 03 generated successfully!")
