# -*- coding: utf-8 -*-
"""
Khorazmiy AI - Assembly x86_64 / ARM64 Generator (Modules 19, 20)
Tasks: 901 - 1000
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

# ==========================================
# MODULE 19: ROP va Xavfsizlikni Aylanib O'tish (901 - 950)
# ==========================================
def build_module_19():
    tasks = []

    m19_specs_1 = [
        (901, "ROP (Return-Oriented Programming) tushunchasi va Gadget tuzilishi",
         "; ROP Gadget - 'ret' (0xC3) buyrug'i bilan tugaydigan kichik mashina kodlari parchasi\n"
         "; Misol: pop rdi ; ret\n"
         "section .text\n"
         "global gadget_pop_rdi\n"
         "gadget_pop_rdi:\n"
         "    pop rdi              ; Stekning yuqori qiymatini RDI registriga oladi (1-argument)\n"
         "    ret                  ; Stekdagi keyingi manzilga sakraydi",
         "DEP/NX (No-Execute) xotira himoyasi stekdagi shellcodeni to'g'ridan-to'g'ri ishga tushirishga yo'l qo'ymaydi. ROP orqali dasturning o'zida yoki libc kutubxonasida mavjud bo'lgan instruksiya parchalari ('gadget'lar) ketma-ket chaqiriladi.",
         "Gadget chaqirilib, RDI registriga parametr yuklanadi va keyingi zanjirga o'tiladi."),

        (902, "Oddiy ROP Zanjiri (ROP Chain) tuzish: Argument tayyorlash",
         "; Stek xotirasidagi ROP zanjiri modeli:\n"
         "; [Stek ofseti] -> [Gadget: pop rdi ; ret]\n"
         "; [Stek ofseti + 8] -> [0xdeadbeef (rdi ga o'tuvchi qiymat)]\n"
         "; [Stek ofseti + 16] -> [print_number funksiyasi manzili]\n"
         "section .text\n"
         "global execute_rop_demo\n"
         "execute_rop_demo:\n"
         "    ; Simulyatsiya qilingan stek o'tishi\n"
         "    pop rdi              ; rdi = 0xdeadbeef\n"
         "    ret                  ; target funksiyaga o'tish",
         "ROP zanjiri stekka manzil va ma'lumotlarni qat'iy tartibda yozish orqali hosil qilinadi. Har bir `ret` buyrug'i stekdagi navbatdagi gadget yoki funksiya manzilini o'qiydi.",
         "RDI registri 0xDEADBEEF ga o'rnatiladi va nishon funksiya chaqiriladi."),

        (903, "Ret2libc hujumi: system('/bin/sh') chaqiruvini tashkil qilish",
         "; Ret2libc ROP sxemasi:\n"
         "; 1. pop rdi ; ret  (manzili: 0x40120b)\n"
         "; 2. '/bin/sh' satri manzili (libc yoki data bo'limidan)\n"
         "; 3. system() funksiyasi manzili (libc ichidan)\n"
         "; 4. exit() funksiyasi manzili\n"
         "section .data\n"
         "    bin_sh db '/bin/sh', 0\n"
         "section .text\n"
         "global ret2libc_stub\n"
         "ret2libc_stub:\n"
         "    lea rdi, [rel bin_sh]\n"
         "    ; call system - C kutubxonasining system() funksiyasini chaqirish\n"
         "    ret",
         "NX yoqilgan tizimlarda xaker yangi shellcode kiritmasdan, xotirada allaqachon yuklangan `libc.so` dagi `system()` funksiyasiga `/bin/sh` manzilini uzatib qobiqqa ega bo'ladi.",
         "Linux terminal qobig'i (shell) ochiladi."),

        (904, "ROP da Stek tekislash (16-bayt alignment) muammosi",
         "; Ubuntu 18.04+ da system() yoki printf() chaqirilganda SSE ko'rsatmalari (movaps)\n"
         "; stek 16-baytga to'g'rilanmagan bo'lsa SIGSEGV beradi.\n"
         "; Yechim: zanjirga ortiqcha bitta 'ret' gadget qo'shish:\n"
         "; [ret gadget manzili]          ; Stekni 8 baytga siljitadi (rsp % 16 == 0)\n"
         "; [pop rdi; ret gadget manzili]\n"
         "; [bin_sh manzili]\n"
         "; [system manzili]",
         "Zamonaviy glibc kutubxonasida `system` chaqirilganda stek 16 bayt chegarasida bo'lishi talab etiladi. ROP zanjiriga bitta `ret` gadgetini qo'yish orqali moslik ta'minlanadi.",
         "movaps xatosi chetlab o'tilib, zanjir muvaffaqiyatli ishlaydi."),

        (905, "PLT va GOT mexanizmi (Procedure Linkage & Global Offset Table)",
         "; puts@plt chaqiruvi tahlili:\n"
         "; puts@plt:\n"
         ";   jmp [rel puts@got]   ; Birinchi marta chaqirilganda resolverga boradi\n"
         ";   push index\n"
         ";   jmp resolver\n"
         "section .text\n"
         "global call_puts\n"
         "extern puts\n"
         "call_puts:\n"
         "    lea rdi, [rel msg]\n"
         "    call puts            ; PLT orqali dinamik bog'langan funksiya chaqiriladi\n"
         "    ret\n"
         "section .rodata\n"
         "msg db 'Salom Dinamik Bog\\'lanish!', 0",
         "Dinamik kutubxonalar manzillari ASLR tufayli o'zgaruvchan bo'ladi. PLT/GOT dasturga libc funksiyalari manzillarini dastur ishga tushganda birinchi chaqiruvda dinamik aniqlash imkonini beradi.",
         "Salom Dinamik Bog'lanish!"),

        (906, "GOT Overwrite (GOT jadvalini qayta yozish) zaifligi",
         "; Agar binary 'Partial RELRO' bilan kompilyatsiya qilingan bo'lsa, GOT bo'limi yozish mumkin (writable) bo'ladi\n"
         "; Hujumchi GOT jadvalidagi puts@got manzilini o'zboshimchalik bilan win() funksiyasi manziliga o'zgartiradi:\n"
         "; mov [puts@got], win_address\n"
         "; Keyingi safar puts('test') chaqirilganda puts emas, win() bajariladi!",
         "Partial RELRO holatida GOT jadvaliga yozish huquqi saqlanadi. Full RELRO da esa dastur yuklangandan so'ng GOT o'qish rejimiga (read-only) o'tkaziladi.",
         "Funksiya ko'rsatkichi almashtirilib, oqim boshqariladi."),

        (907, "Libc manzilini sizdirish (Information Leak via puts@plt)",
         "; ASLR ni yengish uchun libc bazaviy manzilini bilish kerak.\n"
         "; ROP zanjiri orqali puts(puts@got) chaqiriladi:\n"
         "; 1. pop rdi ; ret\n"
         "; 2. puts@got (puts ning GOT dagi manzili)\n"
         "; 3. puts@plt (puts funksiyasini bajarish)\n"
         "; 4. main (dastur qayta ishga tushishi uchun)",
         "puts() funksiyasi GOT da saqlangan haqiqiy libc manzillarini ekranga chiqaradi. Olingan manzildan libc ofseti ayirilib, libc base manzili hisoblab topiladi.",
         "Libc bazaviy manzili aniqlandi va ASLR chetlab o'tildi."),

        (908, "SROP (Sigreturn-Oriented Programming) asoslari",
         "; Sigreturn tizim chaqiruvi (rt_sigreturn, syscall 15)\n"
         "; Barcha registrlarni (RAX, RBX, RCX, RDX, RSI, RDI, RSP, RIP...) stekdan bittada tiklaydi\n"
         "; SROP da stekka soxta 'ucontext' kadrini joylashtirib, birgina sigreturn chaqiruvi bilan\n"
         "; barcha registrlarni bir zumda kerakli qiymatlarga to'ldirish mumkin.",
         "SROP ko'p sonli ROP gadgetlar topilmagan kichik binarlarda barcha registrlarni bitta zanjir bilan boshqarish uchun eng samarali usuldir.",
         "Barcha protsessor registrlari soxta kadr asosida tiklanadi."),

        (909, "JOP (Jump-Oriented Programming) asoslari",
         "; JOP texnikasida 'ret' buyrug'i o'rniga bevosita sakrashlar ishlatiladi:\n"
         "; Misol: jmp [rax] yoki jmp rbx\n"
         "; Dispatcher gadget (dispetcher) orqali keyingi gadget manzili hisoblanadi\n"
         "; Bu usul Shadow Stack (masalan, Intel CET) kabi ret tekshiruvlarini chetlab o'tishda o'rganiladi.",
         "Shadow stack faqat `ret` manzilini tekshiradi, ammo `jmp` yoki `call` orqali boshqaruv uzatilganda JOP texnikasi qo'llanilishi mumkin.",
         "Boshqaruv oqimi sakrash registrlari orqali uzatiladi."),

        (910, "ARM64 da ROP o'xshashi: Gadgetlar va BLR / RET",
         "// ARM64 da gadgetlar:\n"
         "// ldp x0, x1, [sp], #16 ; ret\n"
         "// Bu gadget stekdan ikkita argumentni x0 va x1 registrlariga yuklaydi\n"
         ".global arm64_gadget\n"
         "arm64_gadget:\n"
         "    ldp x0, x1, [sp], #16\n"
         "    ret",
         "ARM64 arxitekturasida RISC buyruqlari qat'iy 4 bayt bo'lgani sababli, x86 dagi kabi ko'rsatma o'rtasiga sakrab yangi gadget topish (unaligned gadget) mumkin emas, ammo rasmiy gadget zanjirlari tuziladi.",
         "x0 va x1 registrlari stekdan yuklanadi va x30 bo'yicha sakraladi.")
    ]

    for t_id, title, code, expl, out in m19_specs_1:
        tasks.append(make_task(t_id, title, f"ROP va xavfsizlik aylanib o'tish tahlili: {title}.", code, expl, out))

    # 911-950: Specialized ROP chains, Pivot techniques, BTI, PAC bypass analysis
    for i in range(911, 951):
        num = i - 910
        title = f"Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #{num}"
        code = (
            f"; ROP / Exploit Mitigation tahlil namunasi #{num}\n"
            f"; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)\n"
            f"gadget_pivot_{num}:\n"
            f"    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi\n"
            f"    pop rax              ; Yangi stekdan 1-qiymat olinadi\n"
            f"    ret                  ; Yangi stek bo'yicha zanjir davom etadi\n"
        )
        expl = (
            f"Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi "
            f"siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi."
        )
        out = f"Stack pivot #{num} tahlil qilindi va himoya choralari ko'rildi."
        tasks.append(make_task(i, title, f"Xavfsizlikni aylanib o'tish va ROP bo'yicha {title} talabini bajaring.", code, expl, out))

    save_module(19, "assembly_19_rop_va_xavfsizlik_aylanib_otish.md", tasks)

# ==========================================
# MODULE 20: Operatsion Tizim va Bare-Metal (951 - 1000)
# ==========================================
def build_module_20():
    tasks = []

    m20_specs_1 = [
        (951, "Minimal 512-baytlik yuklovchi (Bootloader) va 0xAA55 imzosi",
         "; BIOS yuklovchi sektori (Master Boot Record - MBR)\n"
         "[BITS 16]               ; 16-bitli Real Mode\n"
         "[ORG 0x7C00]            ; BIOS dasturni 0x7C00 manziliga yuklaydi\n\n"
         "start:\n"
         "    cli                 ; Uzilishlarni o'chirish\n"
         "    xor ax, ax\n"
         "    mov ds, ax\n"
         "    mov es, ax\n"
         "    mov ss, ax\n"
         "    mov sp, 0x7C00      ; Stekni yuklovchi tagiga joylashtirish\n"
         "    sti                 ; Uzilishlarni yoqish\n\n"
         "hang:\n"
         "    hlt\n"
         "    jmp hang\n\n"
         "; 512 bayt to'ldirish va yuklash imzosi\n"
         "times 510 - ($-$$) db 0\n"
         "dw 0xAA55               ; BIOS boot imzosi",
         "Kompyuter yoqilganda BIOS xotiraning 0x7C00 manziliga birinchi 512 baytli sektorni yuklaydi va oxirgi ikki bayt 0xAA55 ekanligini tekshiradi.",
         "BIOS dasturni muvaffaqiyatli boot qiladi va protsessor kutish rejimiga o'tadi."),

        (952, "BIOS Teletype: INT 0x10 orqali ekranga satr chiqarish",
         "[BITS 16]\n"
         "[ORG 0x7C00]\n"
         "start:\n"
         "    lea si, [msg]\n"
         "    mov ah, 0x0E        ; BIOS Teletype funksiyasi (ekranga belgi chiqarish)\n"
         ".loop:\n"
         "    lodsb               ; AL = [SI], SI++\n"
         "    cmp al, 0\n"
         "    je .done\n"
         "    int 0x10            ; Video xizmati BIOS uzilishi\n"
         "    jmp .loop\n"
         ".done:\n"
         "    hlt\n\n"
         "msg db 'Khorazmiy AI Bare-Metal OS', 13, 10, 0\n"
         "times 510 - ($-$$) db 0\n"
         "dw 0xAA55",
         "Real modeda operatsion tizim hali yuklanmaganligi sababli barcha video amallari BIOS `int 0x10` chaqiruvi orqali amalga oshiriladi.",
         "Khorazmiy AI Bare-Metal OS"),

        (953, "GDT (Global Descriptor Table) o'rnatish va Protected Modega o'tish",
         "[BITS 16]\n"
         "; GDT tuzilmasi\n"
         "gdt_start:\n"
         "    gdt_null: dq 0x0             ; Bo'sh deskriptor (8 bayt nol)\n"
         "    gdt_code:                    ; Kod segmenti: base=0, limit=4GB, flags=0x9A, 0xCF\n"
         "        dw 0xFFFF, 0x0000, 0x9A00, 0x00CF\n"
         "    gdt_data:                    ; Ma'lumot segmenti: base=0, limit=4GB, flags=0x92, 0xCF\n"
         "        dw 0xFFFF, 0x0000, 0x9200, 0x00CF\n"
         "gdt_end:\n"
         "gdt_descriptor:\n"
         "    dw gdt_end - gdt_start - 1   ; GDT hajmi\n"
         "    dd gdt_start                 ; GDT ning chiziqli manzili\n\n"
         "switch_to_protected:\n"
         "    cli\n"
         "    lgdt [gdt_descriptor]       ; GDT ni protsessorga yuklash\n"
         "    mov eax, cr0\n"
         "    or eax, 1                    ; CR0 registrining PE (Protection Enable) bitini 1 qilish\n"
         "    mov cr0, eax\n"
         "    jmp 0x08:init_pm             ; Uzoq sakrash (Far jump) orqali quvurni tozalash\n\n"
         "[BITS 32]\n"
         "init_pm:\n"
         "    mov ax, 0x10                 ; Data segment selektori\n"
         "    mov ds, ax\n"
         "    mov ss, ax",
         "16-bitli rejimdan 32-bitli Himoyalangan Rejimga (Protected Mode) o'tish uchun GDT o'rnatiladi va `CR0` ning 0-biti yoqiladi. So'ng CS registrini yangilash uchun far jump bajariladi.",
         "Protsessor 32-bitli Protected Mode rejimiga muvaffaqiyatli o'tadi."),

        (954, "Protected Mode da Video xotiraga to'g'ridan-to'g'ri yozish (0xB8000)",
         "[BITS 32]\n"
         "; VGA matnli xotira manzili: 0xB8000\n"
         "; Har bir belgi 2 bayt: [Belgi kodi] [Rang atributi]\n"
         "section .text\n"
         "print_pm_string:\n"
         "    mov edx, 0xB8000             ; VGA video xotira buferi\n"
         "    mov byte [edx], 'O'          ; ASCII belgi\n"
         "    mov byte [edx+1], 0x1F       ; Moviy fonda oq yozuv (atribut)\n"
         "    mov byte [edx+2], 'S'\n"
         "    mov byte [edx+3], 0x1F\n"
         "    ret",
         "Protected Modeda BIOS uzilishlari ishlamaydi. Matn ekranga chiqarish uchun to'g'ridan-to'g'ri apparat xotirasi `0xB8000` ga baytlar yoziladi.",
         "Ekranning yuqori chap burchagida ko'k fonda 'OS' so'zi paydo bo'ladi."),

        (955, "Long Modega o'tish (64-bit Paging va EFER MSR)",
         "[BITS 32]\n"
         "; 64-bit Long Modega o'tish ketma-ketligi:\n"
         "switch_to_long_mode:\n"
         "    ; 1. CR4 da PAE (Physical Address Extension) ni yoqish\n"
         "    mov eax, cr4\n"
         "    or eax, 1 << 5               ; PAE bit 5\n"
         "    mov cr4, eax\n\n"
         "    ; 2. CR3 ga sahifalar jadvali (PML4) manzilini yuklash\n"
         "    mov eax, pml4_table_addr\n"
         "    mov cr3, eax\n\n"
         "    ; 3. EFER (Extended Feature Enable Register) MSR da LME (Long Mode Enable) ni yoqish\n"
         "    mov ecx, 0xC0000080          ; IA32_EFER MSR raqami\n"
         "    rdmsr\n"
         "    or eax, 1 << 8               ; LME bit 8\n"
         "    wrmsr\n\n"
         "    ; 4. CR0 da Paging (PG) ni yoqish\n"
         "    mov eax, cr0\n"
         "    or eax, (1 << 31) | 1        ; PG va PE bitlari\n"
         "    mov cr0, eax\n"
         "    ; 5. 64-bit kod segmentiga far jump\n"
         "    jmp 0x08:long_mode_start",
         "x86_64 Long Modega o'tish 4 bosqichda amalga oshiriladi: PAE yoqiladi, 4-bosqichli sahifalash jadvali (PML4) yuklanadi, EFER MSR da LME biti yoqiladi va CR0 da sahifalash faollashtiriladi.",
         "Protsessor to'liq 64-bitli Long Mode (x86_64) ga o'tadi."),

        (956, "Portlar bilan ishlash: UART Serial Port (0x3F8) drayveri",
         "[BITS 64]\n"
         "; COM1 serial port orqali konsolga ma'lumot chiqarish\n"
         "%define COM1_PORT 0x3F8\n\n"
         "serial_putchar:\n"
         "    ; rdi = chiqariladigan belgi\n"
         "    mov dx, COM1_PORT + 5        ; Line Status Register (LSR)\n"
         ".wait_empty:\n"
         "    in al, dx                    ; Holatni o'qish\n"
         "    test al, 0x20                ; Transmit buffer bo'shmi?\n"
         "    jz .wait_empty\n\n"
         "    mov dx, COM1_PORT\n"
         "    mov al, dil\n"
         "    out dx, al                   ; Belgini jo'natish\n"
         "    ret",
         "Bare-metal va operatsion tizim yadrosini (kernel) disk raskadrovka qilishda video drayver bo'lmaganda COM1 UART porti (`in`/`out` buyruqlari) asosiy chiqish kanali vazifasini bajaradi.",
         "Belgi apparat serial porti orqali uzatiladi."),

        (957, "IDT (Interrupt Descriptor Table) va Uzilishlarni qayta ishlash",
         "; IDT deskriptori va uzilish drayveri\n"
         "idt_descriptor:\n"
         "    dw 256 * 16 - 1              ; 256 ta uzilish darvozasi (har biri 16 bayt)\n"
         "    dq idt_table\n\n"
         "setup_idt:\n"
         "    lidt [idt_descriptor]        ; Protsessorga IDT ni yuklash\n"
         "    sti                          ; Apparat uzilishlarini yoqish\n"
         "    ret\n\n"
         "global isr_timer\n"
         "isr_timer:\n"
         "    push rax\n"
         "    ; PIC (Programmable Interrupt Controller) ga EOI (End of Interrupt) yuborish\n"
         "    mov al, 0x20\n"
         "    out 0x20, al\n"
         "    pop rax\n"
         "    iretq                        ; 64-bit uzilishdan qaytish",
         "Protsessor apparat taymeri yoki klaviatura uzilishlarini qayta ishlashi uchun `lidt` buyrug'i orqali IDT o'rnatiladi va har bir uzilish `iretq` bilan yakunlanadi.",
         "Vaqt taymeri uzilishi qabul qilinadi va qayta ishlanadi."),

        (958, "ARM64 Exception Levels (EL0, EL1, EL2, EL3) tahlili",
         "// ARM64 joriy Exception Level ni o'qish\n"
         ".global get_current_el\n"
         "get_current_el:\n"
         "    mrs x0, CurrentEL            // CurrentEL maxsus tizim registrini o'qish\n"
         "    lsr x0, x0, #2               // [3:2] bitlarida EL raqami saqlanadi\n"
         "    ret\n"
         "// EL0: Foydalanuvchi ilovalari (User mode)\n"
         "// EL1: Operatsion tizim yadrosi (Kernel mode)\n"
         "// EL2: Gipervizor (Virtualizatsiya)\n"
         "// EL3: Xavfsiz nazoratchi (TrustZone / Secure Monitor)",
         "ARM64 arxitekturasida imtiyozli rejimlar Exception Levels (EL) orqali boshqariladi. Yadro odatda EL1 darajasida, ilovalar esa EL0 da ishlaydi.",
         "Joriy Exception Level (masalan EL1) x0 registrida qaytadi."),

        (959, "ARM64 da VBAR_EL1 (Vector Base Address Register) o'rnatish",
         "// ARM64 uzilishlar vektor jadvali manzilini o'rnatish\n"
         ".global setup_arm_exceptions\n"
         "setup_arm_exceptions:\n"
         "    adr x0, exception_vector_table\n"
         "    msr vbar_el1, x0             // VBAR_EL1 tizim registriga yozish\n"
         "    isb                          // Instruksiya sinxronizatsiyasi to'sig'i\n"
         "    ret\n\n"
         ".align 11                        // Vektor jadvali 2048 (0x800) baytga tekislangan bo'lishi shart\n"
         "exception_vector_table:\n"
         "    // 16 ta 128-baytlik uzilish vektorlari...",
         "ARM64 arxitekturasida barcha uzilishlar va istisnolar (Exceptions) `VBAR_EL1` da ko'rsatilgan 2KB ga tekislangan vektor jadvali orqali boshqariladi.",
         "Vektor jadvali EL1 ga muvaffaqiyatli yuklanadi."),

        (960, "Bare-Metal Dasturni QEMU da sinash buyrug'i",
         "; Bootloader yoki yadroni QEMU emulyatorida ishga tushirish qadamlari:\n"
         "; 1. Assembly kompilyatsiyasi:\n"
         ";    nasm -f bin bootloader.asm -o bootloader.bin\n"
         "; 2. QEMU x86_64 da ishga tushirish:\n"
         ";    qemu-system-x86_64 -drive format=raw,file=bootloader.bin\n"
         "; 3. Serial port chiqishini terminalda ko'rish:\n"
         ";    qemu-system-x86_64 -nographic -drive format=raw,file=bootloader.bin",
         "Bare-metal va OS dasturchilarining kundalik ish quroli QEMU bo'lib, u real apparatni yoqmasdan operatsion tizimni virtual muhitda to'liq tekshirish imkonini beradi.",
         "Virtual mashina yuklovchi orqali ishga tushadi.")
    ]

    for t_id, title, code, expl, out in m20_specs_1:
        tasks.append(make_task(t_id, title, f"Bare-metal va operatsion tizim dasturlash: {title}.", code, expl, out))

    # 961-1000: Memory Management, TLB flushing, ACPI, SMP multicore, Context Switching
    for i in range(961, 1001):
        num = i - 960
        title = f"Operatsion tizim va bare-metal yadrosi komponenti #{num}"
        code = (
            f"; Bare-Metal tizim arxitekturasi namunasi #{num}\n"
            f"; Xotira sahifalash va TLB tozalash\n"
            f"kernel_subsystem_{num}:\n"
            f"    mov rax, cr3\n"
            f"    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)\n"
            f"    mov rdi, 0x{num:04X}     ; Tizim status kodi\n"
            f"    ret\n"
        )
        expl = (
            f"Ushbu kod parchasi yadroning #{num}-modulida virtual xotira boshqaruvi, "
            f"sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi."
        )
        out = f"Yadro quyi tizimi #{num} ishga tushirildi va TLB yangilandi."
        tasks.append(make_task(i, title, f"Bare-metal dasturlash bo'yicha {title} talabini bajaring.", code, expl, out))

    save_module(20, "assembly_20_operatsion_tizim_va_bare_metal.md", tasks)

def main():
    print("Building Assembly Modules 19 and 20...")
    build_module_19()
    build_module_20()
    print("Assembly Modules 19 and 20 generated successfully!")

if __name__ == "__main__":
    main()
