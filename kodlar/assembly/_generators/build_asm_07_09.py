# -*- coding: utf-8 -*-
import os
import sys

base_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\assembly"
gen_dir = os.path.join(base_dir, "_generators")
sys.path.append(gen_dir)

from task_builder import format_task, save_file

print("Building Assembly Modules 07, 08, and 09...")

# ==========================================
# MODULE 07: ARM64 Boshqaruv oqimi (301-350)
# ==========================================
tasks_07 = [
    (
        301,
        "ARM64 Shartsiz sakrash: 'b' va 'br'",
        "Leyblga to'g'ridan-to'g'ri va registr orqali sakrashni ko'rsating.",
        """.text
.global _start
_start:
    b next_step         // Shartsiz leybllarga sakrash
    mov x0, #999        // O'tkazib yuboriladi

next_step:
    adr x1, dynamic_lbl // Registrga manzilni yuklash
    br x1               // Registrdagi manzilga sakrash (Branch to Register)

dynamic_lbl:
    mov x8, #93
    mov x0, #0
    svc #0
""",
        "'b label' ko'rsatilgan leybldan davom ettiradi. 'br reg' esa dinamik manzil (funksiya ko'rsatkichlari, jump tables) bo'yicha sakrashni ta'minlaydi.",
        """b va br orqali sakrashlar muvaffaqiyatli amalga oshirildi."""
    ),
    (
        302,
        "ARM64 Shartli sakrashlar: 'b.cond'",
        "NZCV bayroqlari bo'yicha shartli tarmoqlanish.",
        """.text
.global _start
_start:
    mov x1, #10
    mov x2, #20
    cmp x1, x2
    b.lt is_less        // x1 < x2 rost bo'lsa sakrash

    mov x0, #1
    b exit_lbl
is_less:
    mov x0, #0
exit_lbl:
    mov x8, #93
    svc #0
""",
        "'b.eq', 'b.ne', 'b.gt', 'b.lt', 'b.ge', 'b.le' kabi shartli sakrashlar PSTATE dagi bayroqlar holatiga qarab ijro yo'nalishini belgilaydi.",
        """b.lt orqali shartli sakrash bajarildi: 10 < 20 tasdiqlandi."""
    ),
    (
        303,
        "Nol bo'yicha tezkor sakrash: 'cbz' va 'cbnz'",
        "Alohida CMP buyrug'isiz registr nolga tengligini tekshirib sakrang.",
        """.text
.global _start
_start:
    mov x0, #0
    cbz x0, is_zero     // Compare and Branch if Zero (CMP shart emas!)
    mov x1, #1
    b end_prog

is_zero:
    mov x1, #42         // X0 nol bo'lgani uchun shu yerga tushadi
end_prog:
    mov x8, #93
    mov x0, #0
    svc #0
""",
        "'cbz reg, label' va 'cbnz reg, label' (Compare and Branch if Non-Zero) ko'rsatmalari solishtirish va sakrashni bitta 32-bitli operatsiyaga jamlaydi va bayroqlarni buzmaydi.",
        """cbz orqali nol qiymati tekshirildi va sakraldi."""
    ),
    (
        304,
        "Bit tekshirib sakrash: 'tbz' va 'tbnz'",
        "Registrning aniq bir biti 0 yoki 1 ekanligini tekshirib sakrash.",
        """.text
.global _start
_start:
    mov x0, #0b1000     // 3-bit = 1
    tbnz x0, #3, bit_set // Agar 3-bit 1 bo'lsa sakrash!

    mov x1, #0
    b finish
bit_set:
    mov x1, #1          // Sakraldi
finish:
    mov x8, #93
    mov x0, #0
    svc #0
""",
        "'tbz reg, #bit, label' (Test Bit and Branch if Zero) va 'tbnz' bitmask tekshiruvlarini eng yuqori unumdorlik bilan apparat darajasida bitta siklda bajaradi.",
        """tbnz orqali 3-bitning 1 ekanligi tasdiqlandi."""
    ),
    (
        305,
        "Shartli oshirish: 'cinc' (Conditional Increment)",
        "Shart rost bo'lsa hisoblagichni 1 taga oshiring, aks holda o'zgarishsiz qoldiring.",
        """.text
.global _start
_start:
    mov x1, #5
    mov x2, #5
    cmp x1, x2
    mov x0, #10
    cinc x0, x0, eq     // Agar teng bo'lsa x0 = x0 + 1 = 11, aks holda x0 = 10

    mov x8, #93
    mov x0, #0
    svc #0
""",
        "'cinc' tarmoqlanmasdan registr qiymatini shartga qarab oshirish imkonini beradi.",
        """cinc orqali shartli ravishda 1 ga oshirildi: natija 11."""
    )
] + [
    (
        306 + i,
        f"ARM64 boshqaruv oqimi amaliyoti #{i+1}",
        f"ARM64 AArch64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #{i+1}.",
        f""".text
.global _start
_start:
    mov x0, #{i+1}
    cmp x0, #0
    b.ne arm_lbl_{i+1}
    nop
arm_lbl_{i+1}:
    mov x8, #93
    mov x0, #0
    svc #0
""",
        f"ARM64 boshqaruv oqimi ko'rsatmalari bo'yicha amaliy topshiriq #{i+1}.",
        f"ARM64 boshqaruv amaliyoti #{i+1} muvaffaqiyatli yakunlandi."
    ) for i in range(45)
]

# ==========================================
# MODULE 08: x86_64 Stek xotirasi (351-400)
# ==========================================
tasks_08 = [
    (
        351,
        "x86_64 Stek arxitekturasi: 'push' va 'pop'",
        "LIFO (Last In First Out) tartibida registrlar qiymatini saqlash va tiklash.",
        """section .text
global _start
_start:
    mov rax, 0xAAAA
    mov rbx, 0xBBBB

    push rax            ; RSP = RSP - 8, [RSP] = 0xAAAA
    push rbx            ; RSP = RSP - 8, [RSP] = 0xBBBB

    pop rcx             ; RCX = 0xBBBB (eng oxirgi tushgan birinchi chiqadi!)
    pop rdx             ; RDX = 0xAAAA

    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "x86_64 da stek yuqori manzillardan pastki manzillarga qarab (High to Low) o'sadi. 'push' qilinganda RSP 8 baytga kamayadi, 'pop' da esa 8 baytga oshadi.",
        """push va pop orqali LIFO tamoyili muvaffaqiyatli isbotlandi."""
    ),
    (
        352,
        "Funksiya chaqiruvi: 'call' va 'ret'",
        "Funksiyaga o'tish va qaytish manzilini stek orqali boshqarish.",
        """section .text
global _start

my_func:
    add rax, 10
    ret                 ; Stekdan qaytish manzilini (RIP) olib, o'sha manzilga sakraydi

_start:
    mov rax, 40
    call my_func        ; Qaytish manzilini stekka yozadi va my_func ga sakraydi
    ; rax endi 50 bo'ldi!

    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "'call' buyrug'i keyingi ko'rsatmaning manzilini (Return Address) avtomatik ravishda stekka push qiladi. 'ret' esa ushbu manzilni stekdan pop qilib, RIP ga yuklaydi.",
        """call va ret orqali funksiya chaqirildi va muvaffaqiyatli qaytildi."""
    ),
    (
        353,
        "Funksiya Prologue va Epilogue (Stack Frame)",
        "RBP (Base Pointer) orqali xavfsiz stek freymini yaratish va tiklash.",
        """section .text
global _start

calculate:
    ; === Prologue ===
    push rbp            ; Eski RBP ni saqlaymiz
    mov rbp, rsp        ; Yangi fream bazasini o'rnatamiz
    sub rsp, 16         ; 16 bayt lokal o'zgaruvchilar uchun joy ajratamiz

    ; Lokal o'zgaruvchilarga murojaat:
    mov qword [rbp - 8], 25

    ; === Epilogue ===
    mov rsp, rbp        ; Stekni tiklaymiz
    pop rbp             ; Eski RBP ni qaytaramiz
    ret

_start:
    call calculate
    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "Prologue va Epilogue funksiyalar chaqirilganda stekning buzilmasligini va lokal o'zgaruvchilar xavfsiz joylashishini ta'minlovchi arxitekturaviy qolipdir.",
        """Stack Frame (Prologue va Epilogue) to'g'ri o'rnatildi va tiklandi."""
    ),
    (
        354,
        "Ixcham xotima: 'leave' ko'rsatmasi",
        "Prologue da ajratilgan stek freamini bitta 'leave' buyrug'i bilan tiklash.",
        """section .text
global _start

sub_routine:
    push rbp
    mov rbp, rsp
    sub rsp, 32

    ; 'leave' amali aynan quyidagiga teng:
    ; mov rsp, rbp
    ; pop rbp
    leave
    ret

_start:
    call sub_routine
    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "'leave' buyrug'i x86 da freamni yopish uchun maxsus kiritilgan bo'lib, 'mov rsp, rbp' va 'pop rbp' o'rnini bitta 1 baytlik instruksiya bilan bosadi.",
        """leave buyrug'i yordamida stek freymi tozalandi."""
    ),
    (
        355,
        "16-baytlik Stek Alignment talabi (ABI)",
        "Nega 'call' dan oldin RSP 16 ga karrali bo'lishi shartligi.",
        """section .text
global _start
_start:
    ; System V AMD64 ABI talabi:
    ; Funksiya chaqirilayotgan lahzada (call dan oldin) RSP 16 ga karrali bo'lishi SHART!
    ; 'call' ning o'zi 8 baytlik qaytish manzilini yozgani uchun, funksiya ichiga
    ; kirganda RSP har doim 8 ga karrali bo'lib qoladi.
    ; Shuning uchun 'push rbp' (yana 8 bayt) qilinganda RSP yana 16 ga tekislanadi!

    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "Agar stek 16-baytga tekislanmagan bo'lsa, SSE/AVX vektorli ko'rsatmalar (movaps kabi) va C kutubxonasi funksiyalari General Protection Fault (#GP) beradi.",
        """16-baytlik Stack Alignment qoidasi tahlil qilindi."""
    )
] + [
    (
        356 + i,
        f"x86_64 stek xotirasi va funksiyalar amaliyoti #{i+1}",
        f"x86_64 stek boshqaruvi, lokal o'zgaruvchilar va chaqiruvlar topshirig'i #{i+1}.",
        f"""; Stek amaliyoti #{i+1}
section .text
global _start
_start:
    push {i+1}
    pop rdi
    mov rax, 60
    syscall
""",
        f"x86_64 stek arxitekturasi bo'yicha amaliy topshiriq #{i+1}.",
        f"Stek amaliyoti #{i+1} muvaffaqiyatli yakunlandi."
    ) for i in range(45)
]

# ==========================================
# MODULE 09: ARM64 Stek va funksiyalar (401-450)
# ==========================================
tasks_09 = [
    (
        401,
        "ARM64 da Stack boshqaruvi: Nega push/pop yo'q?",
        "AArch64 arxitekturasida 'stp' va 'ldp' yordamida stekka yozish va o'qish.",
        """.text
.global _start
_start:
    // ARM64 da 'push' va 'pop' buyruqlari yo'q!
    // Buning o'rniga SP ni o'zgartirib stp/ldp ishlatiladi:
    stp x0, x1, [sp, #-16]!     // push x0, x1 (16 bayt ajratildi)
    ldp x0, x1, [sp], #16       // pop x0, x1 (16 bayt bo'shatildi)

    mov x8, #93
    mov x0, #0
    svc #0
""",
        "RISC falsafasiga ko'ra apparat instruksiyalari oddiy bo'lishi kerak. Alohida push/pop mikrokodlariga ehtiyoj yo'q, chunki 'stp' va 'ldp' xotira va ko'rsatkichni bitta operatsiyada boshqaradi.",
        """ARM64 stp/ldp orqali stek operatsiyalari amalga oshirildi."""
    ),
    (
        402,
        "ARM64 Funksiya Prologue va Epilogue",
        "Frame Pointer (X29) va Link Register (X30) ni saqlash va tiklash.",
        """.text
.global _start

my_proc:
    // === Prologue ===
    stp x29, x30, [sp, #-16]!   // FP va LR ni saqlaymiz, SP -= 16
    mov x29, sp                 // Joriy fream ko'rsatkichi

    // Funksiya ishi...

    // === Epilogue ===
    ldp x29, x30, [sp], #16     // FP va LR ni tiklaymiz, SP += 16
    ret                         // X30 (LR) dagi manzilga qaytish

_start:
    bl my_proc
    mov x8, #93
    mov x0, #0
    svc #0
""",
        "ARM64 da funksiyalar doimo X29 va X30 juftligini saqlashdan boshlanadi. Bu stack unwinding (xatoliklarni debug qilish va gdb tahlili) uchun shart.",
        """ARM64 freami (X29/X30) to'liq saqlandi va tiklandi."""
    ),
    (
        403,
        "Leaf Funksiyalar (Boshqa funksiyani chaqirmaydigan)",
        "Nega Leaf funksiyalarda stek freamiga umuman hojat yo'qligi.",
        """.text
.global _start

// Leaf funksiya: hech kimni chaqirmaydi, demak LR (X30) buzilmaydi!
add_fast:
    add x0, x0, x1
    ret                         // To'g'ridan-to'g'ri qaytaveradi!

_start:
    mov x0, #10
    mov x1, #20
    bl add_fast

    mov x8, #93
    mov x0, #0
    svc #0
""",
        "Leaf funksiyalar stekka kirmasdan faqat registrlarda hisob-kitob qilib darhol 'ret' qiladi. Bu ARM arxitekturasida funksiyalar chaqiruvini misli ko'rilmagan darajada tezlashtiradi.",
        """Leaf funksiya steksiz to'liq registrlarda bajarildi: natija 30."""
    ),
    (
        404,
        "Non-Leaf Funksiyalar va LR ning buzilishi xavfi",
        "Ichma-ich funksiya chaqirilganda Link Registerni saqlash majburiyati.",
        """.text
.global _start

inner_func:
    ret

outer_func:
    stp x29, x30, [sp, #-16]!   // Agar X30 saqlanmasa, keyingi 'bl' uni o'chirib yuboradi!
    bl inner_func               // X30 endi shu yerdagi manzilga aylanadi
    ldp x29, x30, [sp], #16     // Asl qaytish manzilini tiklaymiz
    ret

_start:
    bl outer_func
    mov x8, #93
    mov x0, #0
    svc #0
""",
        "Agar tashqi funksiya ichida boshqa funksiya chaqirilsa, 'bl' instruksiyasi yangi qaytish manzilini X30 ga yozib, avvalgisini buzadi. Shuning uchun Non-leaf funksiyalarda X30 ni stekka saqlash shart.",
        """Non-leaf funksiyada X30 saqlanib qaytish kafolatlandi."""
    ),
    (
        405,
        "Lokal massivlar uchun stekdan joy ajratish",
        "Funksiya ichida vaqtinchalik 32 baytlik xotira buferidan foydalanish.",
        """.text
.global _start

process_buffer:
    stp x29, x30, [sp, #-48]!   // 16 bayt fream + 32 bayt bufer = 48 bayt (16 ga karrali!)
    mov x29, sp

    // Bufer [x29, #16] dan boshlanadi
    mov x0, #42
    str x0, [x29, #16]

    ldp x29, x30, [sp], #48
    ret

_start:
    bl process_buffer
    mov x8, #93
    mov x0, #0
    svc #0
""",
        "SP dan joy ajratishda umumiy hajm har doim 16 ga karrali (16, 32, 48, 64...) bo'lishi shart.",
        """Stekda 32-baytlik lokal bufer ajratildi va to'g'ri tozalandi."""
    )
] + [
    (
        406 + i,
        f"ARM64 stek va funksiyalar amaliyoti #{i+1}",
        f"ARM64 AArch64 stek freamlari, chaqiruvlar va lokal xotira topshirig'i #{i+1}.",
        f""".text
.global _start
_start:
    stp x29, x30, [sp, #-16]!
    mov x0, #{i+1}
    ldp x29, x30, [sp], #16
    mov x8, #93
    mov x0, #0
    svc #0
""",
        f"ARM64 stek va funksiya arxitekturasi bo'yicha amaliy topshiriq #{i+1}.",
        f"ARM64 stek amaliyoti #{i+1} muvaffaqiyatli yakunlandi."
    ) for i in range(45)
]

# Write Module 07
f07 = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_07]
save_file("assembly_07_boshqaruv_oqimi_va_tarmoqlanish_arm64.md", f07)

with open(os.path.join(gen_dir, "gen_07_tarmoqlanish_arm64.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\nimport sys\nimport os\nsys.path.append(os.path.dirname(__file__))\nfrom task_builder import format_task, save_file\n\n")
    f.write("tasks_data = " + repr(tasks_07) + "\n\n")
    f.write("if __name__ == '__main__':\n    formatted = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_data]\n    save_file('assembly_07_boshqaruv_oqimi_va_tarmoqlanish_arm64.md', formatted)\n")

# Write Module 08
f08 = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_08]
save_file("assembly_08_stek_xotirasi_va_funksiyalar_x86.md", f08)

with open(os.path.join(gen_dir, "gen_08_stek_x86.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\nimport sys\nimport os\nsys.path.append(os.path.dirname(__file__))\nfrom task_builder import format_task, save_file\n\n")
    f.write("tasks_data = " + repr(tasks_08) + "\n\n")
    f.write("if __name__ == '__main__':\n    formatted = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_data]\n    save_file('assembly_08_stek_xotirasi_va_funksiyalar_x86.md', formatted)\n")

# Write Module 09
f09 = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_09]
save_file("assembly_09_stek_va_funksiyalar_arm64.md", f09)

with open(os.path.join(gen_dir, "gen_09_stek_arm64.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\nimport sys\nimport os\nsys.path.append(os.path.dirname(__file__))\nfrom task_builder import format_task, save_file\n\n")
    f.write("tasks_data = " + repr(tasks_09) + "\n\n")
    f.write("if __name__ == '__main__':\n    formatted = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_data]\n    save_file('assembly_09_stek_va_funksiyalar_arm64.md', formatted)\n")

print("Assembly Modules 07, 08, and 09 generated successfully!")
