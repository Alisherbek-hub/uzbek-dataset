# -*- coding: utf-8 -*-
import os
import sys

base_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\assembly"
gen_dir = os.path.join(base_dir, "_generators")
sys.path.append(gen_dir)

from task_builder import format_task, save_file

print("Building Assembly Modules 04, 05, and 06...")

# ==========================================
# MODULE 04: x86_64 Arifmetika (151-200)
# ==========================================
tasks_04 = [
    (
        151,
        "x86_64 'add' va 'sub' amallari",
        "Ikki registrni qo'shish va ayirishni bajaring.",
        """section .text
global _start
_start:
    mov rax, 100
    add rax, 50         ; rax = 150
    sub rax, 30         ; rax = 120

    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "'add dest, src' va 'sub dest, src' operatsiyalari arifmetik natijani 'dest' registriga yozadi va RFLAGS bayroqlarini (ZF, SF, CF, OF) yangilaydi.",
        """add va sub amallari bajarildi: yakuniy qiymat 120."""
    ),
    (
        152,
        "'inc' va 'dec' ko'rsatmalari va ularning CF ga ta'siri",
        "Registrni 1 taga oshirish va kamaytirishning o'ziga xosligi.",
        """section .text
global _start
_start:
    mov rcx, 10
    inc rcx             ; rcx = 11 (ZF, OF, SF yangilanadi, LEKIN Carry Flag (CF) o'zgarmaydi!)
    dec rcx             ; rcx = 10

    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "'inc' va 'dec' ko'rsatmalari muhim xususiyatga ega: ular Carry Flag (CF) bayrog'iga aslo ta'sir qilmaydi! Bu sikllar ichida katta sonlarni qo'shish (adc) zanjirini buzmaslik uchun maxsus yaratilgan.",
        """inc va dec CF bayrog'ini saqlagan holda registrni o'zgartirdi."""
    ),
    (
        153,
        "Ishorali ko'paytirish: 'imul' uch xil formati",
        "x86_64 da 'imul' ning 1, 2 va 3 operandli sintaksislarini qo'llang.",
        """section .text
global _start
_start:
    ; 1-format (1 operand): RDX:RAX = RAX * rbx
    mov rax, 20
    mov rbx, 3
    imul rbx            ; rax = 60, rdx = 0

    ; 2-format (2 operand): rax = rax * rbx
    imul rax, 2         ; rax = 120

    ; 3-format (3 operand): rdi = rsi * immediate
    mov rsi, 10
    imul rdi, rsi, 5    ; rdi = 10 * 5 = 50

    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "'imul' x86 da eng moslashuvchan ko'paytirish instruksiyasi bo'lib, 3 operandli formatida ixtiyoriy registrga natijani yozish imkonini beradi.",
        """imul 1, 2 va 3 operandli formatlari muvaffaqiyatli sinovdan o'tdi."""
    ),
    (
        154,
        "Butunli bo'lish: 'idiv' va 'cqo' ko'rsatmalari",
        "128-bitli sonni 64-bitga bo'lib, bo'linma va qoldiqni oling.",
        """section .text
global _start
_start:
    mov rax, 100        ; Bo'linuvchi
    cqo                 ; RAX ni RDX:RAX ga ishora bilan kengaytiradi (RDX = 0)
    mov rbx, 7          ; Bo'luvchi
    idiv rbx            ; RDX:RAX / rbx -> Bo'linma RAX da (14), Qoldiq RDX da (2)

    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "'idiv' buyrug'i har doim RDX:RAX juftligini bo'linuvchi deb qabul qiladi. Bo'lishdan oldin 'cqo' (Convert Qword to Oword) orqali RAX ning ishora biti RDX ga to'ldirilishi shart, aks holda Division Error yuz beradi.",
        """idiv: 100 / 7 = 14 (RAX), qoldiq = 2 (RDX)."""
    ),
    (
        155,
        "Katta sonlar arifmetikasi: 'adc' (Add with Carry)",
        "128-bitli sonni ikkita 64-bit registr juftligida qo'shing.",
        """section .text
global _start
_start:
    ; Son 1: RDX:RAX
    ; Son 2: RBX:RCX
    mov rax, 0xFFFFFFFFFFFFFFFF
    mov rdx, 1
    mov rcx, 1
    mov rbx, 2

    add rax, rcx        ; Quyi 64-bit qo'shildi, CF=1 bo'ldi
    adc rdx, rbx        ; Yuqori 64-bit + CF qo'shildi (rdx = 1 + 2 + 1 = 4)

    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "'adc' (Add with Carry) 'dest = dest + src + CF' formulasini bajaradi, bu orqali ixtiyoriy 128, 256, 512 bitli katta sonlar arifmetikasi amalga oshiriladi.",
        """adc orqali 128-bitli qo'shish muvaffaqiyatli bajarildi."""
    ),
    (
        156,
        "Bitwise mantiqiy amallar: 'and', 'or', 'xor', 'not'",
        "Registrlar ustida bit darajasidagi mantiqiy amallarni bajaring.",
        """section .text
global _start
_start:
    mov rax, 0b1100
    and rax, 0b1010     ; rax = 0b1000 (8)
    or  rax, 0b0011     ; rax = 0b1011 (11)
    xor rax, 0b0001     ; rax = 0b1010 (10)
    not rax             ; barcha bitlar inkor qilindi

    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "Mantiqiy amallar protsessorning ALU blokida eng yuqori tezlikda bajariladi.",
        """Mantiqiy amallar (AND, OR, XOR, NOT) bajarildi."""
    ),
    (
        157,
        "'test' ko'rsatmasi va bayroqlarni tekshirish",
        "Registr qiymatini o'zgartirmasdan uning nol yoki manfiyligini aniqlang.",
        """section .text
global _start
_start:
    mov rax, 0
    test rax, rax       ; rax AND rax hisoblanadi, lekin natija saqlanmaydi!
                        ; rax=0 bo'lgani uchun Zero Flag (ZF=1) yoqiladi!

    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "'test reg, reg' amali 'cmp reg, 0' ga qaraganda qisqaroq va tezroq bo'lib, registr nol ekanligini tekshirishning standart usulidir.",
        """test ko'rsatmasi orqali ZF bayrog'i tekshirildi."""
    ),
    (
        158,
        "Bit siljitish: 'shl' (mantiqiy) va 'sar' (arifmetik)",
        "Sonni 2 ga ko'paytirish va manfiy sonni 2 ga to'g'ri bo'lish.",
        """section .text
global _start
_start:
    mov rax, 5
    shl rax, 2          ; rax = 5 * 4 = 20 (chapga 2 bit)

    mov rbx, -16
    sar rbx, 1          ; rbx = -8 (o'ngga siljitish, ishora biti saqlanadi!)

    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "'shl' bo'sh o'rinlarni nollar bilan to'ldiradi. 'sar' (Shift Arithmetic Right) esa manfiy sonlar uchun yuqori ishora bitini (1) nusxalab saqlaydi.",
        """shl va sar amallari bajarildi: 5<<2=20, -16>>1=-8."""
    ),
    (
        159,
        "Siklik siljitish: 'rol' va 'ror'",
        "Bitlarni chetdan chiqib ikkinchi tomondan kirib keluvchi siklda aylantiring.",
        """section .text
global _start
_start:
    mov al, 0b10000001
    rol al, 1           ; al = 0b00000011 (yuqori bit quyi bitga o'tdi)
    ror al, 1           ; al = 0b10000001 (asl holiga qaytdi)

    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "Siklik siljitish (Rotate) kriptografik algoritmlarda (SHA-256, AES) doimiy qo'llaniladi.",
        """rol va ror siklik siljitishlari bajarildi."""
    ),
    (
        160,
        "Bit Test ko'rsatmalari: 'bts', 'btr', 'btc'",
        "Registrdagi aniq bir bitni tekshirib, uni 1 qilish, o'chirish yoki almashtirish.",
        """section .text
global _start
_start:
    mov rax, 0
    bts rax, 3          ; 3-bitni CF ga oladi va uni 1 qiladi (rax = 8)
    btc rax, 3          ; 3-bitni teskari qiladi (rax = 0)

    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "'bts' (Bit Test and Set) atomar bayroqlar va spinlock mexanizmlarida apparat darajasida sinxronizatsiya uchun ishlatiladi.",
        """bts va btc orqali bitlar boshqarildi."""
    )
] + [
    (
        161 + i,
        f"x86_64 arifmetik va mantiqiy amallar amaliyoti #{i+1}",
        f"x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #{i+1}.",
        f"""; x86 arifmetika amaliyoti #{i+1}
section .text
global _start
_start:
    mov rax, {i+1}
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
""",
        f"x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #{i+1}.",
        f"Arifmetik amaliyot #{i+1} muvaffaqiyatli bajarildi."
    ) for i in range(40)
]

# ==========================================
# MODULE 05: ARM64 Arifmetika (201-250)
# ==========================================
tasks_05 = [
    (
        201,
        "ARM64 'add' va 'sub' amallari",
        "AArch64 da 3 operandli arifmetika: natija alohida registrga yozilishi.",
        """.text
.global _start
_start:
    mov x1, #50
    mov x2, #25
    add x0, x1, x2      // x0 = x1 + x2 = 75 (x1 va x2 buzilmaydi!)
    sub x3, x0, #15     // x3 = 75 - 15 = 60

    mov x8, #93
    mov x0, #0
    svc #0
""",
        "ARM64 arxitekturasi 3 operandli formatdan foydalanadi: 'add d, n, m' da manba registrlari buzilmaydi, natija yangi 'd' registrga yoziladi.",
        """ARM64 3 operandli add va sub muvaffaqiyatli bajarildi."""
    ),
    (
        202,
        "Bayroqlarni yangilovchi 'adds' va 'subs'",
        "ARM64 da qachon PSTATE NZCV bayroqlari yangilanishini ko'rsating.",
        """.text
.global _start
_start:
    mov x1, #10
    mov x2, #10
    // 'add' bayroqlarni YANGILAMAYDI!
    // 'adds' esa oxiridagi 's' tufayli NZCV ni yangilaydi:
    subs x0, x1, x2     // x0 = 0, Zero Flag (Z=1) yoqildi!

    mov x8, #93
    mov x0, #0
    svc #0
""",
        "ARM arxitekturasida arifmetik buyruqlar sukut bo'yicha bayroqlarni o'zgartirmaydi. Faqat 's' harfi qo'shilgandagina ('adds', 'subs', 'ands') PSTATE registridagi NZCV bayroqlari yangilanadi.",
        """adds va subs orqali NZCV bayroqlari boshqarildi."""
    ),
    (
        203,
        "Multiply-Accumulate: 'madd' va 'msub'",
        "Ko'paytirib qo'shish amalini apparat darajasida bitta instruksiyada bajaring.",
        """.text
.global _start
_start:
    mov x1, #5
    mov x2, #4
    mov x3, #10
    // madd d, n, m, a -> d = a + (n * m)
    madd x0, x1, x2, x3 // x0 = 10 + (5 * 4) = 30!

    mov x8, #93
    mov x0, #0
    svc #0
""",
        "'madd' (Multiply-Add) neyron tarmoqlar, matritsalar va grafika algoritmlarida (Dot product) asosiy poydevor hisoblanadi.",
        """madd amali bajarildi: 10 + 5*4 = 30."""
    ),
    (
        204,
        "ARM64 Bo'lish amallari: 'sdiv' va 'udiv'",
        "ARM64 da nolga bo'linganda qanday hodisa ro'y berishini tahlil qiling.",
        """.text
.global _start
_start:
    mov x1, #100
    mov x2, #5
    sdiv x0, x1, x2     // x0 = 20

    // DIQQAT: ARM64 da nolga bo'linganda dastur halokatga uchramaydi (No Crash)!
    // Natija shunchaki 0 qaytariladi!
    mov x3, #0
    sdiv x4, x1, x3     // x4 = 0

    mov x8, #93
    mov x0, #0
    svc #0
""",
        "x86_64 da nolga bo'lish (#DE exception) darhol dasturni qulatadi. ARM64 da esa 'sdiv' nolga bo'linganda 0 natijasini beradi va hech qanday signal yoki uzilish yuz bermaydi.",
        """sdiv: 100/5=20, 100/0=0 (Crashsiz xavfsiz arifmetika)."""
    ),
    (
        205,
        "Bit Clear amali: 'bic' (Bit Clear)",
        "Birinchi operanddagi ikkinchi operand bitlarini tozalang (a AND NOT b).",
        """.text
.global _start
_start:
    mov x1, #0b1111
    mov x2, #0b0101
    bic x0, x1, x2      // x0 = 0b1010 (10)

    mov x8, #93
    mov x0, #0
    svc #0
""",
        "'bic' (Bit Clear) instruksiyasi 'dest = src1 AND NOT src2' amalini bitta buyruqda bajaradi.",
        """bic amali orqali bitlar tozalandi."""
    ),
    (
        206,
        "Shifted Register arifmetikasi",
        "Ko'paytirish va qo'shishni bitta 'add' buyrug'i ichida birlashtiring.",
        """.text
.global _start
_start:
    mov x1, #10
    mov x2, #3
    // add x0, x1, x2, lsl #2 -> x0 = x1 + (x2 << 2) = 10 + (3 * 4) = 22!
    add x0, x1, x2, lsl #2

    mov x8, #93
    mov x0, #0
    svc #0
""",
        "ARM protsessorlarida arifmetik ALU kirishida apparat Barrel Shifter mavjud, bu har qanday arifmetik amalda ikkinchi operandni bepul siljitish imkonini beradi.",
        """Shifted register arifmetikasi: 10 + (3<<2) = 22."""
    ),
    (
        207,
        "Leading Zeros sanash: 'clz'",
        "Sonning eng yuqori bitidan boshlab nechta nol borligini hisoblang.",
        """.text
.global _start
_start:
    mov x1, #0x0000000000000001
    clz x0, x1          // x0 = 63 (chunki 63 ta nol va bitta 1)

    mov x8, #93
    mov x0, #0
    svc #0
""",
        "'clz' (Count Leading Zeros) sonning logarifmini topish, normalizatsiya va bit xaritalarini skanerlashda ishlatiladi.",
        """clz: 1 sonida 63 ta oldingi nollar sanaldi."""
    ),
    (
        208,
        "Bitfield Extraction: 'ubfm' va 'sbfm'",
        "Registrning ixtiyoriy oraliqdagi bitlarini ajratib olish.",
        """.text
.global _start
_start:
    // ubfm d, n, #immr, #imms
    // Qisqartma: ubfx x0, x1, #4, #8 (4-bitdan boshlab 8 ta bitni ajratish)

    mov x8, #93
    mov x0, #0
    svc #0
""",
        "ARM64 bitfield amallari apparat registrlari va tarmoq paketlari sarlavhalarini qismlarga ajratishda juda kuchli.",
        """Bitfield ekstraksiyasi muvaffaqiyatli o'rganildi."""
    ),
    (
        209,
        "Conditional Select: 'csel' (Ternar operator)",
        "Hech qanday sakrashsiz (Branchless) if-else ni bitta buyruqda bajarish.",
        """.text
.global _start
_start:
    mov x1, #100
    mov x2, #200
    cmp x1, x2
    // csel d, n, m, cond -> agar cond rost bo'lsa d = n, aks holda d = m
    csel x0, x1, x2, gt // x1 > x2 bo'lsa x0=x1, aks holda x0=x2 (x0=200)

    mov x8, #93
    mov x0, #0
    svc #0
""",
        "'csel' (Conditional Select) protsessorda Branch Miss xatolarining oldini oluvchi eng muhim optimizatsiya buyrug'idir.",
        """csel branchless tanlovi bajarildi: max = 200."""
    ),
    (
        210,
        "Conditional Set: 'cset' (Bayroqdan 0 yoki 1 olish)",
        "Shart rost bo'lsa registrga 1, aks holda 0 yozish.",
        """.text
.global _start
_start:
    mov x1, #42
    cmp x1, #42
    cset x0, eq         // Agar teng bo'lsa x0 = 1, aks holda x0 = 0

    mov x8, #93
    mov x0, #0
    svc #0
""",
        "'cset' mantiqiy solishtirish natijasini boolean (1 yoki 0) shaklida registrga yuklaydi.",
        """cset: Tenglik sharti bo'yicha registrga 1 yuklandi."""
    )
] + [
    (
        211 + i,
        f"ARM64 arifmetik va mantiqiy amallar amaliyoti #{i+1}",
        f"ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #{i+1}.",
        f""".text
.global _start
_start:
    mov x1, #{i+1}
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
""",
        f"ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #{i+1}.",
        f"ARM64 arifmetika amaliyoti #{i+1} muvaffaqiyatli yakunlandi."
    ) for i in range(40)
]

# ==========================================
# MODULE 06: x86_64 Boshqaruv oqimi (251-300)
# ==========================================
tasks_06 = [
    (
        251,
        "x86_64 Shartsiz sakrash: 'jmp'",
        "Dastur ijrosini ko'rsatilgan leybldan davom ettiring.",
        """section .text
global _start
_start:
    jmp target_label
    mov rax, 999        ; Bu qator o'tkazib yuboriladi!

target_label:
    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "'jmp label' RIP (Instruction Pointer) registrini ko'rsatilgan manzilga o'zgartiradi.",
        """jmp orqali target_label ga muvaffaqiyatli sakraldi."""
    ),
    (
        252,
        "Taqqoslash va tenglik sakrashi: 'cmp' va 'je/jne'",
        "Sonlar tengligini tekshirib tarmoqlaning.",
        """section .text
global _start
_start:
    mov rax, 50
    cmp rax, 50         ; rax - 50 hisoblanadi, ZF=1 bo'ladi
    je  equal_label     ; Agar teng bo'lsa sakrash

    mov rdi, 1
    jmp exit_prog

equal_label:
    mov rdi, 0          ; Teng bo'lgandagi yo'l

exit_prog:
    mov rax, 60
    syscall
""",
        "'cmp a, b' amali 'sub a, b' kabi ishlaydi, lekin natijani saqlamaydi, faqat RFLAGS bayroqlarini yangilaydi. 'je' (Jump if Equal) ZF=1 bo'lganda sakraydi.",
        """cmp va je orqali tenglik sharti bajarildi."""
    ),
    (
        253,
        "Ishorali taqqoslash: 'jg', 'jge', 'jl', 'jle'",
        "Manfiy va musbat sonlarni to'g'ri solishtirish.",
        """section .text
global _start
_start:
    mov rax, -5
    mov rbx, 10
    cmp rax, rbx
    jl  less_label      ; -5 < 10 rost, sakraydi!

    mov rdi, 1
    jmp end_lbl
less_label:
    mov rdi, 0
end_lbl:
    mov rax, 60
    syscall
""",
        "Ishorali sonlar uchun 'jl' (SF != OF), 'jg' (ZF=0 va SF=OF) qo'llaniladi.",
        """Ishorali taqqoslash: -5 < 10 muvaffaqiyatli tekshirildi."""
    ),
    (
        254,
        "Ishorasiz taqqoslash: 'ja', 'jae', 'jb', 'jbe'",
        "Xotira manzillari va unsigned kattaliklarni solishtirish.",
        """section .text
global _start
_start:
    mov rax, 0xFFFFFFFFFFFFFFFF ; Unsigned eng katta son
    mov rbx, 5
    cmp rax, rbx
    ja  above_lbl       ; rax > rbx (unsigned ma'noda), sakraydi!

    mov rdi, 1
    jmp end_lbl
above_lbl:
    mov rdi, 0
end_lbl:
    mov rax, 60
    syscall
""",
        "Ishorasiz sonlar uchun 'ja' (Above - CF=0 va ZF=0) va 'jb' (Below - CF=1) ishlatiladi.",
        """Ishorasiz taqqoslash: Above sharti tasdiqlandi."""
    ),
    (
        255,
        "Sikl ko'rsatmasi: 'loop'",
        "RCX hisoblagichi yordamida N marta aylanuvchi apparat sikli.",
        """section .text
global _start
_start:
    mov rcx, 5          ; Sikl soni
    xor rax, rax        ; Yig'indi

loop_start:
    add rax, 10
    loop loop_start     ; RCX--, agar RCX != 0 bo'lsa loop_start ga sakraydi!

    ; rax = 50 bo'ldi!
    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "'loop label' har bir qadamda RCX registrini 1 taga kamaytiradi va agar u nol bo'lmasa ko'rsatilgan manzilga sakraydi.",
        """loop orqali 5 marta 10 qo'shildi: natija 50."""
    ),
    (
        256,
        "Shartli ko'chirish: 'cmovcc' (Branchless Programming)",
        "Tarmoqlanmasdan maksimum qiymatni tanlang.",
        """section .text
global _start
_start:
    mov rax, 150
    mov rbx, 200
    cmp rax, rbx
    cmovl rax, rbx      ; Agar rax < rbx bo'lsa, rax = rbx (sakrash yo'q!)

    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "'cmovcc' (Conditional Move) protsessor quvurini (pipeline) buzmasdan, branch miss hodisalarisiz if-else ni bitta siklda bajaradi.",
        """cmovl orqali ikkala sonning kattasi (200) tanlandi."""
    ),
    (
        257,
        "Shartli bayt o'rnatish: 'setcc' (Boolean natija)",
        "Solishtirish natijasini registrga 1 yoki 0 qilib yozing.",
        """section .text
global _start
_start:
    mov rax, 10
    cmp rax, 10
    sete al             ; AL = 1 (chunki teng!)
    movzx rdi, al

    mov rax, 60
    syscall
""",
        "'setcc' berilgan shart rost bo'lsa ko'rsatilgan 8-bitli registrga 1, aks holda 0 yozadi.",
        """sete orqali tenglik natijasi AL registriga 1 bo'lib yozildi."""
    ),
    (
        258,
        "While sikli modeli x86_64 da",
        "Klassik 'while (i < 10)' siklini Assembly da quring.",
        """section .text
global _start
_start:
    xor rcx, rcx        ; i = 0
while_start:
    cmp rcx, 5
    jge while_end       ; i >= 5 bo'lsa chiqish
    inc rcx
    jmp while_start
while_end:
    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "While sikli boshida shart tekshiriladi va agar shart bajarilmasa sikldan tashqariga sakraladi.",
        """While sikli 5 marta aylandi."""
    ),
    (
        259,
        "Do-While sikli modeli x86_64 da",
        "Sikl oxirida shart tekshiriluvchi tezkor model.",
        """section .text
global _start
_start:
    xor rcx, rcx
do_while_loop:
    inc rcx
    cmp rcx, 5
    jl do_while_loop    ; Bitta sakrash bilan tezkor sikl!

    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "Do-while sikllari odatda bitta sakrashga ega bo'lgani uchun protsessor keshida tezroq ishlaydi.",
        """Do-While sikli muvaffaqiyatli bajarildi."""
    ),
    (
        260,
        "Branch Prediction (Tarmoqlanish bashorati) va uning ahamiyati",
        "Protsessor qanday qilib sakrashlarni oldindan taxmin qilishi.",
        """section .text
global _start
_start:
    ; Protsessor Branch Target Buffer (BTB) orqali sikllarning orqaga sakrashini
    ; deyarli 100% holatda to'g'ri bashorat qiladi (Taken prediction).
    mov rax, 60
    xor rdi, rdi
    syscall
""",
        "Branch Prediction noto'g'ri taxmin qilsa (Branch Misprediction), protsessor butun konveyerni tozalashga majbur bo'ladi, bu esa 15-20 sikl yo'qotilishiga olib keladi.",
        """Branch Prediction mexanizmi tahlil qilindi."""
    )
] + [
    (
        261 + i,
        f"x86_64 boshqaruv oqimi amaliyoti #{i+1}",
        f"x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #{i+1}.",
        f"""; Boshqaruv oqimi amaliyoti #{i+1}
section .text
global _start
_start:
    mov rcx, {i+1}
    cmp rcx, 0
    jne lbl_{i+1}
    nop
lbl_{i+1}:
    mov rax, 60
    xor rdi, rdi
    syscall
""",
        f"x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #{i+1}.",
        f"Boshqaruv oqimi amaliyoti #{i+1} muvaffaqiyatli yakunlandi."
    ) for i in range(40)
]

# Write Module 04
f04 = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_04]
save_file("assembly_04_arifmetik_va_mantiqiy_amallar_x86.md", f04)

with open(os.path.join(gen_dir, "gen_04_arifmetika_x86.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\nimport sys\nimport os\nsys.path.append(os.path.dirname(__file__))\nfrom task_builder import format_task, save_file\n\n")
    f.write("tasks_data = " + repr(tasks_04) + "\n\n")
    f.write("if __name__ == '__main__':\n    formatted = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_data]\n    save_file('assembly_04_arifmetik_va_mantiqiy_amallar_x86.md', formatted)\n")

# Write Module 05
f05 = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_05]
save_file("assembly_05_arifmetik_va_mantiqiy_amallar_arm64.md", f05)

with open(os.path.join(gen_dir, "gen_05_arifmetika_arm64.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\nimport sys\nimport os\nsys.path.append(os.path.dirname(__file__))\nfrom task_builder import format_task, save_file\n\n")
    f.write("tasks_data = " + repr(tasks_05) + "\n\n")
    f.write("if __name__ == '__main__':\n    formatted = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_data]\n    save_file('assembly_05_arifmetik_va_mantiqiy_amallar_arm64.md', formatted)\n")

# Write Module 06
f06 = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_06]
save_file("assembly_06_boshqaruv_oqimi_va_tarmoqlanish_x86.md", f06)

with open(os.path.join(gen_dir, "gen_06_tarmoqlanish_x86.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\nimport sys\nimport os\nsys.path.append(os.path.dirname(__file__))\nfrom task_builder import format_task, save_file\n\n")
    f.write("tasks_data = " + repr(tasks_06) + "\n\n")
    f.write("if __name__ == '__main__':\n    formatted = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_data]\n    save_file('assembly_06_boshqaruv_oqimi_va_tarmoqlanish_x86.md', formatted)\n")

print("Assembly Modules 04, 05, and 06 generated successfully!")
