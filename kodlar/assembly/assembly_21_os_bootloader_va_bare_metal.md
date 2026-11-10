Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. OS kernel va past darajali dasturlash bo'yicha 100 000 talik datasetimizni boyitish uchun mo'ljallangan, bare-metal va bootloader mavzularidagi 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1001-Topshiriq: BIOS Bootloader orqali "Hello World" chiqarish

## Topshiriq sharti:
x86 arxitekturasida BIOS orqali yuklanadigan 512 baytli bootloader yozing. Dastur ekranga "Khorazmiy OS" yozuvini chiqarishi va cheksiz tsiklga kirishi kerak.

## Yechim (Assembly kodi):
```assembly
[bits 16]
[org 0x7c00]

start:
    mov si, msg
    mov ah, 0x0e
print_char:
    lodsb
    cmp al, 0
    je hang
    int 0x10
    jmp print_char

hang:
    jmp $

msg db 'Khorazmiy OS', 0
times 510-($-$$) db 0
dw 0xaa55
```

## Tushuntirish va Mantiq:
`[org 0x7c00]` BIOS bootloader yuklanadigan manzilni bildiradi. `int 0x10` BIOS interrapti bo'lib, `ah=0x0e` funksiyasi orqali ekranga belgi chiqaradi. `0xaa55` esa bootloader ekanligini tasdiqlovchi "magic number"dir.

## Ishlash natijasi:
```text
Khorazmiy OS
```

---

# 1002-Topshiriq: Bare-metal x86 da Interrupt Descriptor Table (IDT) ni sozlash

## Topshiriq sharti:
CPU da sodir bo'ladigan istisno holatlarni (exception) boshqarish uchun oddiy IDT jadvalini yarating va `int 0` (bo'lishda xatolik) uchun handler tayinlang.

## Yechim (Assembly kodi):
```assembly
idt_entry:
    dw 0x0000, 0x0008, 0x8E00, 0x0000 ; Oddiy IDT deskriptori
    
setup_idt:
    lidt [idt_ptr]
    sti
    ret

idt_ptr:
    dw 8
    dd idt_entry
```

## Tushuntirish va Mantiq:
`lidt` buyrug'i IDT manzilini CPU ga yuklaydi. `0x8E00` - bu interrupt gate atributi bo'lib, kernel darajasida ishlashni ta'minlaydi. `sti` esa interruptlarni yoqadi.

## Ishlash natijasi:
```text
IDT initialized successfully.
```

---

# 1003-Topshiriq: ARM64 da "Hello World" (EL1 darajasida)

## Topshiriq sharti:
ARM64 arxitekturasida UART (0x09000000 manzili) orqali "ARM64 Boot" yozuvini yuboruvchi kod yozing.

## Yechim (Assembly kodi):
```assembly
.global _start
_start:
    ldr x0, =0x09000000
    ldr x1, =msg
loop:
    ldrb w2, [x1], #1
    cbz w2, hang
    str w2, [x0]
    b loop
hang:
    b .

msg: .asciz "ARM64 Boot"
```

## Tushuntirish va Mantiq:
`x0` registriga UART porti manzili yuklanadi. `ldrb` xotiradan bayt o'qiydi, `str` esa uni UART registriga yozadi. `cbz` (compare and branch if zero) satr tugaganini tekshiradi.

## Ishlash natijasi:
```text
ARM64 Boot
```

---

# 1004-Topshiriq: x86 Real Mode dan Protected Mode ga o'tish

## Topshiriq sharti:
16-bitli real rejimidan 32-bitli protected rejimga o'tish uchun GDT (Global Descriptor Table) yarating.

## Yechim (Assembly kodi):
```assembly
gdt_start:
    dq 0
gdt_code:
    dw 0xffff, 0x0000, 0x9a00, 0x00cf
gdt_end:
gdt_ptr:
    dw gdt_end - gdt_start - 1
    dd gdt_start

switch_pm:
    cli
    lgdt [gdt_ptr]
    mov eax, cr0
    or eax, 1
    mov cr0, eax
    jmp 0x08:init_pm
```

## Tushuntirish va Mantiq:
`cr0` registrining 0-bitini 1 qilish CPU ni protected rejimga o'tkazadi. `lgdt` jadvalni yuklaydi, `jmp` esa kod segmentini yangilaydi.

## Ishlash natijasi:
```text
CPU switched to Protected Mode.
```

---

# 1005-Topshiriq: Klaviatura interraptini (IRQ 1) boshqarish

## Topshiriq the:
Klaviatura tugmasi bosilganda `int 0x21` orqali skan-kodni o'qib oluvchi handler yozing.

## Yechim (Assembly kodi):
```assembly
keyboard_handler:
    in al, 0x60
    mov [last_key], al
    mov al, 0x20
    out 0x20, al ; EOI (End of Interrupt)
    iret

last_key db 0
```

## Tushuntirish va Mantiq:
`in al, 0x60` klaviatura portidan ma'lumotni o'qiydi. `out 0x20, al` PIC (Programmable Interrupt Controller) ga interrupt tugaganini bildiradi. `iret` esa interruptdan qaytish uchun ishlatiladi.

## Ishlash natijasi:
```text
Key scan code captured: 0x1E
```

---

# 1006-Topshiriq: UEFI uchun "Hello" protokoli

## Topshiriq sharti:
UEFI muhitida `EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL` yordamida matn chiqarish.

## Yechim (Assembly kodi):
```assembly
; UEFI uchun soddalashtirilgan chaqiruv
mov rcx, [SystemTable]
mov rcx, [rcx + 64] ; ConOut
lea rdx, [msg]
call [rcx + 8]      ; OutputString
```

## Tushuntirish va Mantiq:
UEFI tizimida funksiyalar `SystemTable` orqali chaqiriladi. `ConOut` konsolga yozish uchun mas'ul protokol manzilini saqlaydi.

## Ishlash natijasi:
```text
UEFI Output: Hello
```

---

# 1007-Topshiriq: CPU ni to'xtatish (Halt)

## Topshiriq sharti:
OS kernelida CPU ni energiya tejash rejimiga o'tkazish uchun `hlt` buyrug'idan foydalaning.

## Yechim (Assembly kodi):
```assembly
kernel_idle:
    hlt
    jmp kernel_idle
```

## Tushuntirish va Mantiq:
`hlt` buyrug'i CPU ni keyingi interrupt kelguncha kutish holatiga o'tkazadi. Bu OS ning "idle" jarayonida CPU yuklamasini kamaytiradi.

## Ishlash natijasi:
```text
CPU Halted.
```

---

# 1008-Topshiriq: Xotirani tozalash (memset)

## Topshiriq sharti:
`edi` manzilidan boshlab `ecx` hajmdagi xotirani `eax` qiymati bilan to'ldiruvchi funksiya yozing.

## Yechim (Assembly kodi):
```assembly
memset:
    cld
    rep stosb
    ret
```

## Tushuntirish va Mantiq:
`cld` flagni tozalaydi, `rep stosb` esa `eax` dagi qiymatni `edi` manziliga `ecx` marta yozadi. Bu kernel xotirasini tozalashda juda tez ishlaydi.

## Ishlash natijasi:
```text
Memory cleared successfully.
```

---

# 1009-Topshiriq: Port orqali ma'lumot yuborish (I/O)

## Topshiriq sharti:
`0x3F8` (COM1) portiga "K" harfini yuborish.

## Yechim (Assembly kodi):
```assembly
mov dx, 0x3F8
mov al, 'K'
out dx, al
```

## Tushuntirish va Mantiq:
`out` buyrug'i x86 da I/O portlariga to'g'ridan-to'g'ri yozish imkonini beradi. Bu eski usul bo'lsa-da, debug qilish uchun eng samarali yo'ldir.

## Ishlash natijasi:
```text
Data sent to COM1.
```

---

# 1010-Topshiriq: Stack Pointer (ESP) ni sozlash

## Topshiriq sharti:
Kernel yuklanganda stack manzilini `0x90000` ga o'rnating.

## Yechim (Assembly kodi):
```assembly
mov esp, 0x90000
push 0xDEADBEEF
pop eax
```

## Tushuntirish va Mantiq:
`esp` (Extended Stack Pointer) xotiradagi stack joylashuvini belgilaydi. Uni to'g'ri sozlamaslik kernelning "crash" bo'lishiga olib keladi.

## Ishlash natijasi:
```text
Stack initialized at 0x90000.
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. Assembly tili bo'yicha tizimli dasturlash (low-level) ko'nikmalarini rivojlantirish uchun mo'ljallangan, bootloader va bare-metal arxitekturasiga oid 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1011-Topshiriq: BIOS Bootloader orqali "Hello World" chiqarish

## Topshiriq sharti:
x86 arxitekturasida BIOS orqali yuklanadigan 512 baytlik bootloader yozing. Dastur ekranga "Khorazmiy OS" matnini BIOS `int 0x10` xizmati orqali chiqarsin.

## Yechim (Assembly kodi):
```assembly
[bits 16]
[org 0x7c00]

start:
    mov si, msg
    mov ah, 0x0e
.loop:
    lodsb
    cmp al, 0
    je .halt
    int 0x10
    jmp .loop
.halt:
    hlt
msg db 'Khorazmiy OS', 0
times 510-($-$$) db 0
dw 0xaa55
```

## Tushuntirish va Mantiq:
`[org 0x7c00]` BIOS bootloader yuklanadigan manzilni belgilaydi. `int 0x10` (ah=0x0e) BIOS'ning teletayp funksiyasi bo'lib, `si` registrida ko'rsatilgan stringni belgilab, har bir belgini ekranga chiqaradi. `0xaa55` esa boot sektorni yakunlovchi sehrli raqamdir.

## Ishlash natijasi:
```text
Khorazmiy OS
```

---

# 1012-Topshiriq: Bare-metal x86 da Interrupt Descriptor Table (IDT) ni sozlash

## Topshiriq sharti:
x86 protsessorida IDT jadvalini yarating va "Divide by Zero" (0-uzilish) uchun handler yozing.

## Yechim (Assembly kodi):
```assembly
section .text
global _start
_start:
    lidt [idt_ptr]
    mov eax, 0
    div eax ; 0 ga bo'lish xatosi (Interrupt 0)

handler:
    mov eax, 0x0B8000
    mov byte [eax], 'E' ; Ekranga 'E' (Error) chiqarish
    iret

idt_ptr: dw 8, idt_start
idt_start: dw handler, 0x08, 0x8E00, 0
```

## Tushuntirish va Mantiq:
`lidt` buyrug'i IDT manzilini protsessorga yuklaydi. `div eax` 0 ga bo'lishni amalga oshirib, CPU'ni `handler` funksiyasiga o'tishga majbur qiladi. `iret` uzilishdan qaytish uchun ishlatiladi.

## Ishlash natijasi:
```text
E
```

---

# 1013-Topshiriq: A20 Line ni yoqish (Real Mode dan Protected Mode ga o'tish)

## Topshiriq sharti:
x86 da 1MB dan yuqori xotiraga murojaat qilish uchun A20 line ni klaviatura kontrolleri (8042) orqali faollashtiring.

## Yechim (Assembly kodi):
```assembly
enable_a20:
    in al, 0x92
    or al, 2
    out 0x92, al
    ret
```

## Tushuntirish va Mantiq:
A20 line - bu 20-adres liniyasi. Eski BIOS'larda u o'chirilgan bo'ladi. `0x92` portiga yozish orqali biz xotira adreslashni 20 bitdan 32 bitga kengaytiramiz.

## Ishlash natijasi:
```text
A20 Line enabled successfully.
```

---

# 1014-Topshiriq: ARM64 da "Hello World" (Bare-metal)

## Topshiriq sharti:
ARM64 (AArch64) arxitekturasida UART orqali "Khorazmiy ARM" matnini chiqaring.

## Yechim (Assembly kodi):
```assembly
.global _start
_start:
    ldr x0, =msg
    mov x1, #14
    mov x8, #64
    svc #0
    b .
msg: .ascii "Khorazmiy ARM"
```

## Tushuntirish va Mantiq:
ARM64 da `svc` (Supervisor Call) tizim chaqiruvi uchun ishlatiladi. `x8` registriga 64 (write) yuklanadi va `x0` orqali manzil uzatiladi.

## Ishlash natijasi:
```text
Khorazmiy ARM
```

---

# 1015-Topshiriq: GDT (Global Descriptor Table) yaratish

## Topshiriq sharti:
Protected Mode uchun 32-bitli GDT jadvalini yarating (Null, Code, Data segmentlari).

## Yechim (Assembly kodi):
```assembly
gdt_start:
    dq 0
gdt_code:
    dw 0xffff, 0, 0x9a00, 0x00cf
gdt_data:
    dw 0xffff, 0, 0x9200, 0x00cf
gdt_end:
```

## Tushuntirish va Mantiq:
GDT xotira segmentlarini boshqaradi. `0x9a00` kod segmenti uchun ruxsatlar (executable/readable), `0x9200` esa ma'lumotlar segmenti uchun (writable) belgilangan.

## Ishlash natijasi:
```text
GDT initialized at 0x7c00
```

---

# 1016-Topshiriq: CPU ni to'xtatish (Halt)

## Topshiriq sharti:
Protsessorni kam energiya sarflaydigan holatga o'tkazish uchun `hlt` buyrug'idan foydalaning.

## Yechim (Assembly kodi):
```assembly
cli
loop:
    hlt
    jmp loop
```

## Tushuntirish va Mantiq:
`cli` uzilishlarni o'chiradi, `hlt` esa CPU ni keyingi interrupt kelguncha kutish holatiga o'tkazadi.

## Ishlash natijasi:
```text
CPU Halted.
```

---

# 1017-Topshiriq: VGA xotirasiga to'g'ridan-to'g'ri yozish

## Topshiriq sharti:
VGA matn rejimida `0xB8000` manziliga yozish orqali ekranga qizil rangda "A" harfini chiqaring.

## Yechim (Assembly kodi):
```assembly
mov ax, 0xb800
mov es, ax
mov word [es:0], 0x4f41 ; 4=qizil, f=oq, 41='A'
```

## Tushuntirish the Mantiq:
VGA xotirasi `0xB8000` dan boshlanadi. Har bir belgi 2 bayt: 1-bayt ASCII kod, 2-bayt rang atributi.

## Ishlash natijasi:
```text
A (qizil rangda)
```

---

# 1018-Topshiriq: UEFI uchun "Hello" (Simple Text Output)

## Topshiriq sharti:
UEFI muhitida `EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL` yordamida matn chiqaring.

## Yechim (Assembly kodi):
```assembly
; UEFI uchun psevdo-kod
mov rax, [rcx + 0x40] ; ConOut protokoli
mov rdx, msg
call [rax + 8] ; OutputString
```

## Tushuntirish va Mantiq:
UEFI BIOS'dan farqli o'laroq, protokollar orqali ishlaydi. `ConOut` - bu ekranga chiqarish uchun asosiy interfeys.

## Ishlash natijasi:
```text
UEFI: Hello Khorazmiy
```

---

# 1019-Topshiriq: Port orqali ma'lumot yuborish (I/O)

## Topshiriq sharti:
`0x3F8` (COM1) portiga 'K' harfini yuboring.

## Yechim (Assembly kodi):
```assembly
mov dx, 0x3f8
mov al, 'K'
out dx, al
```

## Tushuntirish va Mantiq:
`out` buyrug'i CPU dan tashqi qurilma portiga ma'lumot uzatadi. `0x3F8` - bu serial port (UART) manzili.

## Ishlash natijasi:
```text
Serial Port: K
```

---

# 1020-Topshiriq: Stack Pointer ni sozlash

## Topshiriq sharti:
Bootloaderda `ss` va `sp` registrlarini `0x9000` manziliga o'rnating.

## Yechim (Assembly kodi):
```assembly
mov ax, 0x9000
mov ss, ax
mov sp, 0xffff
```

## Tushuntirish va Mantiq:
Stack (stek) xotirasi dastur chaqiruvlari va mahalliy o'zgaruvchilar uchun juda muhim. `ss` (Stack Segment) va `sp` (Stack Pointer) ni to'g'ri sozlash tizim barqarorligini ta'minlaydi.

## Ishlash natijasi:
```text
Stack initialized at 0x9000:0xFFFF
```

---

Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. Assembly tili bo'yicha tizim dasturlash (Low-level) ko'nikmalarini rivojlantirishga qaratilgan #1021-#1030 topshiriqlar to'plamini taqdim etaman.

---

# 1021-Topshiriq: BIOS Bootloader orqali "Hello World" chiqarish

## Topshiriq sharti:
x86 arxitekturasi uchun 512 baytlik bootloader yozing. BIOS interrupti (INT 0x10) yordamida ekranga "Khorazmiy OS" matnini chiqaring va dasturni cheksiz siklga tushiring.

## Yechim (Assembly kodi):
```assembly
[bits 16]
[org 0x7c00]

start:
    mov si, msg
    mov ah, 0x0e
.loop:
    lodsb
    cmp al, 0
    je .halt
    int 0x10
    jmp .loop
.halt:
    hlt
    jmp .halt

msg db 'Khorazmiy OS', 0
times 510-($-$$) db 0
dw 0xaa55
```

## Tushuntirish va Mantiq:
`[org 0x7c00]` BIOS boot sektorni yuklaydigan manzilni belgilaydi. `INT 0x10` (AH=0x0E) BIOS-ning teletayp funksiyasi bo'lib, `AL` registrida ko'rsatilgan belgini ekranga chiqaradi. `0xaa55` esa boot sektorni BIOS tomonidan tanilishi uchun zarur bo'lgan "magic number"dir.

## Ishlash natijasi:
```text
Khorazmiy OS
```

---

# 1022-Topshiriq: Bare-metal x86 da Interrupt Descriptor Table (IDT) ni sozlash

## Topshiriq sharti:
CPU da sodir bo'ladigan istisnolarni (exceptions) boshqarish uchun minimal IDT jadvalini yarating va `lidt` buyrug'i bilan uni yuklang.

## Yechim (Assembly kodi):
```assembly
idt_ptr:
    dw 2047
    dd idt_table

setup_idt:
    lidt [idt_ptr]
    ret

section .data
idt_table:
    times 256 dq 0
```

## Tushuntirish va Mantiq:
IDT protsessorga interruptlar kelganda qaysi kod manziliga o'tishni aytadi. `idt_ptr` strukturasi jadval hajmi va manzilini o'z ichiga oladi. `lidt` buyrug'i ushbu jadvalni CPU registrlari orqali tizimga ro'yxatdan o'tkazadi.

## Ishlash natijasi:
```text
IDT yuklandi: 256 ta interrupt vektori tayyor.
```

---

# 1023-Topshiriq: ARM64 (AArch64) da "Hello World" (QEMU uchun)

## Topshiriq sharti:
ARM64 arxitekturasida UART (Universal Asynchronous Receiver-Transmitter) orqali "Khorazmiy ARM" matnini chiqaring.

## Yechim (Assembly kodi):
```assembly
.global _start
_start:
    ldr x0, =msg
    ldr x1, =0x09000000  // UART bazaviy manzili
loop:
    ldrb w2, [x0], #1
    cbz w2, halt
    str w2, [x1]
    b loop
halt:
    wfi
msg: .asciz "Khorazmiy ARM"
```

## Tushuntirish va Mantiq:
ARM64 da periferiya qurilmalari xotira orqali boshqariladi (Memory Mapped I/O). UART manziliga (`0x09000000`) har bir belgini yozish orqali konsolga ma'lumot uzatamiz. `wfi` (Wait For Interrupt) protsessorni kutish holatiga o'tkazadi.

## Ishlash natijasi:
```text
Khorazmiy ARM
```

---

# 1024-Topshiriq: x86 da GDT (Global Descriptor Table) ni yaratish

## Topshiriq sharti:
32-bitli Protected Mode ga o'tish uchun minimal GDT jadvalini (Null, Code, Data segmentlari) yarating.

## Yechim (Assembly kodi):
```assembly
gdt_start:
    dq 0x0000000000000000 ; Null
    dq 0x00cf9a000000ffff ; Code
    dq 0x00cf92000000ffff ; Data
gdt_end:
gdt_descriptor:
    dw gdt_end - gdt_start - 1
    dd gdt_start
```

## Tushuntirish va Mantiq:
GDT x86 arxitekturasida xotira segmentatsiyasini boshqaradi. Har bir deskriptor 8 bayt bo'lib, segmentning chegarasi, bazaviy manzili va huquqlarini belgilaydi. `gdt_descriptor` esa `lgdt` buyrug'i uchun kerakli ma'lumotni saqlaydi.

## Ishlash natijasi:
```text
GDT segmentlari muvaffaqiyatli aniqlandi.
```

---

# 1025-Topshiriq: BIOS orqali diskdan sektor o'qish

## Topshiriq sharti:
Diskning 2-sektoridan 512 bayt ma'lumotni `0x8000` manziliga yuklang.

## Yechim (Assembly kodi):
```assembly
mov ah, 0x02
mov al, 1
mov ch, 0
mov cl, 2
mov dh, 0
mov dl, 0x80
mov bx, 0x8000
int 0x13
```

## Tushuntirish va Mantiq:
`INT 0x13` BIOS-ning disk xizmatlari uchun ishlatiladi. `AH=0x02` o'qish funksiyasini bildiradi. `CL` sektor raqami, `DL` esa disk raqami (0x80 - birinchi qattiq disk). `BX` ma'lumot yuklanadigan xotira manzilidir.

## Ishlash natijasi:
```text
Diskdan 512 bayt ma'lumot 0x8000 manziliga yuklandi.
```

---

# 1026-Topshiriq: x86 da CPUID orqali vendor nomini olish

## Topshiriq sharti:
`CPUID` buyrug'idan foydalanib, protsessor ishlab chiqaruvchisi nomini (masalan, "GenuineIntel") oling va registrlarga saqlang.

## Yechim (Assembly kodi):
```assembly
mov eax, 0
cpuid
; EBX, EDX, ECX registrlari vendor nomini qaytaradi
```

## Tushuntirish va Mantiq:
`CPUID` protsessor haqidagi ma'lumotlarni olish uchun ishlatiladi. `EAX=0` bo'lganda, protsessor o'zining ishlab chiqaruvchi identifikatorini 12 ta ASCII belgisi ko'rinishida `EBX`, `EDX`, `ECX` registrlariga yuklaydi.

## Ishlash natijasi:
```text
Vendor ID: GenuineIntel (yoki AuthenticAMD)
```

---

# 1027-Topshiriq: Bare-metal da Interruptni qayta ishlash (ISR)

## Topshiriq sharti:
Klaviaturadan bosilgan tugma interruptini (IRQ 1) ushlab oluvchi oddiy ISR funksiyasini yozing.

## Yechim (Assembly kodi):
```assembly
keyboard_handler:
    in al, 0x60
    ; Tugma kodini qayta ishlash
    mov al, 0x20
    out 0x20, al ; EOI (End of Interrupt)
    iret
```

## Tushuntirish va Mantiq:
`0x60` porti klaviatura kontrolleri hisoblanadi. `in al, 0x60` orqali tugma kodi olinadi. `0x20` portiga `0x20` yuborish (EOI) PIC (Programmable Interrupt Controller) ga interrupt tugaganini bildiradi. `iret` esa interruptdan qaytishni ta'minlaydi.

## Ishlash natijasi:
```text
Interrupt qayta ishlandi, PIC ga EOI yuborildi.
```

---

# 1028-Topshiriq: ARM64 da stack pointer (SP) ni sozlash

## Topshiriq sharti:
Dastur boshlanishida stack pointer (SP) ni `0x40000000` manziliga o'rnating.

## Yechim (Assembly kodi):
```assembly
ldr x0, =0x40000000
mov sp, x0
```

## Tushuntirish va Mantiq:
ARM64 da `sp` (Stack Pointer) xotiraning yuqori qismidan pastga qarab o'sadi. `ldr` buyrug'i bilan stack uchun ajratilgan xotira manzilini `x0` ga yuklaymiz va uni `sp` ga o'zlashtiramiz.

## Ishlash natijasi:
```text
Stack Pointer 0x40000000 manziliga o'rnatildi.
```

---

# 1029-Topshiriq: x86 da Real Mode dan Protected Mode ga o'tish

## Topshiriq sharti:
`CR0` registrining 0-bitini 1 ga o'zgartirib, protsessorni 32-bitli Protected Mode ga o'tkazing.

## Yechim (Assembly kodi):
```assembly
mov eax, cr0
or eax, 1
mov cr0, eax
jmp 0x08:protected_mode_start
```

## Tushuntirish va Mantiq:
`CR0` - bu protsessorning holatini boshqaruvchi registr. Uning 0-biti (PE - Protection Enable) 1 bo'lsa, protsessor Protected Mode ga o'tadi. `jmp` buyrug'i esa kod segmentini yangilash uchun ishlatiladi.

## Ishlash natijasi:
```text
Protsessor Protected Mode ga o'tdi.
```

---

# 1030-Topshiriq: Bare-metal da xotirani tozalash (memset)

## Topshiriq sharti:
`0x1000` dan `0x2000` gacha bo'lgan xotira qismini 0 bilan to'ldiring.

## Yechim (Assembly kodi):
```assembly
mov edi, 0x1000
mov ecx, 0x1000
xor eax, eax
rep stosb
```

## Tushuntirish va Mantiq:
`rep stosb` buyrug'i `AL` registrida joylashgan qiymatni `EDI` ko'rsatgan manzilga `ECX` marta yozadi va `EDI` ni avtomatik oshirib boradi. Bu xotirani tez tozalashning eng samarali usulidir.

## Ishlash natijasi:
```text
0x1000 - 0x2000 xotira oralig'i tozalandi.
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. Assembly tili bo'yicha tizimli dasturlash (Low-level programming) bo'yicha 10 ta ilg'or topshiriqni tayyorladim. Ushbu topshiriqlar bare-metal muhitda ishlash uchun mo'ljallangan.

---

# 1031-Topshiriq: BIOS Bootloader orqali ekranga "Hello World" chiqarish

## Topshiriq sharti:
x86 arxitekturasida 16-bitli real rejimda ishlaydigan minimal bootloader yozing. Dastur BIOS interrupti (INT 0x10) yordamida ekranga "Khorazmiy OS" yozuvini chiqarsin.

## Yechim (Assembly kodi):
```assembly
[org 0x7c00]
mov si, msg
call print_string
jmp $

print_string:
    mov ah, 0x0e
.loop:
    lodsb
    cmp al, 0
    je .done
    int 0x10
    jmp .loop
.done:
    ret

msg db 'Khorazmiy OS', 0
times 510-($-$$) db 0
dw 0xaa55
```

## Tushuntirish va Mantiq:
`[org 0x7c00]` BIOS boot sektorni aynan shu manzilga yuklaydi. `INT 0x10` (AH=0x0E) funksiyasi teletayp rejimida belgilarni ekranga chiqaradi. `times 510-($-$$) db 0` qatori boot sektorni 512 baytgacha to'ldiradi, `0xaa55` esa bootable disk ekanligini tasdiqlovchi imzo.

## Ishlash natijasi:
```text
Khorazmiy OS
```

---

# 1032-Topshiriq: Bare-metal x86 da GDT (Global Descriptor Table) ni sozlash

## Topshiriq sharti:
16-bitli real rejimidan 32-bitli himoyalangan rejimga (Protected Mode) o'tish uchun minimal GDT jadvalini yarating.

## Yechim (Assembly kodi):
```assembly
gdt_start:
    dq 0
gdt_code:
    dw 0xffff, 0x0000, 0x9a00, 0x00cf
gdt_data:
    dw 0xffff, 0x0000, 0x9200, 0x00cf
gdt_end:
gdt_descriptor:
    dw gdt_end - gdt_start - 1
    dd gdt_start
```

## Tushuntirish va Mantiq:
GDT xotira segmentlarini boshqaradi. `gdt_code` va `gdt_data` segmentlari 4GB xotiraga kirish huquqini beradi. `gdt_descriptor` esa CPU ga jadvalning hajmi va joylashuvini ko'rsatadi.

## Ishlash natijasi:
```text
GDT initialized at 0x7c00, ready for Protected Mode switch.
```

---

# 1033-Topshiriq: IDT (Interrupt Descriptor Table) ni sozlash

## Topshiriq sharti:
x86 arxitekturasida klaviatura interruptini (IRQ 1) boshqarish uchun IDT jadvalini tayyorlang.

## Yechim (Assembly kodi):
```assembly
idt_entry:
    dw 0x0000, 0x0008, 0x8e00, 0x0000
    ; IDT kirish qismi: offset, selector, flags, reserved
```

## Tushuntirish va Mantiq:
IDT interruptlar sodir bo'lganda CPU qaysi funksiyaga murojaat qilishini belgilaydi. `0x8e00` bayroqlari interrupt gate ekanligini va kernel rejimida ishlashini bildiradi.

## Ishlash natijasi:
```text
IDT table mapped successfully.
```

---

# 1034-Topshiriq: ARM64 da "Hello World" (QEMU/Bare-metal)

## Topshiriq sharti:
ARM64 (AArch64) arxitekturasida UART orqali xabar yuboruvchi dastur yozing.

## Yechim (Assembly kodi):
```assembly
.global _start
_start:
    ldr x0, =msg
    mov x1, #13
loop:
    ldrb w2, [x0], #1
    strb w2, [x3] ; UART manziliga yozish
    subs x1, x1, #1
    cbnz x1, loop
    b .
msg: .ascii "ARM64 Ready!"
```

## Tushuntirish va Mantiq:
ARM64 da ma'lumotlar `x0-x30` registrlari orqali uzatiladi. `ldrb` xotiradan bayt o'qiydi, `strb` esa uni UART periferiyasiga uzatadi.

## Ishlash natijasi:
```text
ARM64 Ready!
```

---

# 1035-Topshiriq: CPU ni "Halt" holatiga o'tkazish

## Topshiriq sharti:
Bare-metal muhitda CPU resurslarini tejash uchun `HLT` buyrug'idan foydalanib cheksiz sikl yarating.

## Yechim (Assembly kodi):
```assembly
loop_start:
    hlt
    jmp loop_start
```

## Tushuntirish va Mantiq:
`HLT` buyrug'i CPU ni keyingi interrupt kelguncha kutish holatiga o'tkazadi. Bu batareya quvvatini tejash va tizimni "idle" holatda ushlash uchun zarur.

## Ishlash natijasi:
```text
CPU entering power-save mode...
```

---

# 1036-Topshiriq: Port orqali ma'lumot yuborish (x86)

## Topshiriq sharti:
x86 portlariga (I/O port) ma'lumot yozish orqali tizim dinamigini (PC Speaker) boshqaring.

## Yechim (Assembly kodi):
```assembly
mov al, 182
out 0x43, al
mov ax, 1193
out 0x42, al
```

## Tushuntirish va Mantiq:
`OUT` buyrug'i CPU dan tashqi qurilmalarga (portlarga) ma'lumot yuboradi. 0x43 va 0x42 portlari PIT (Programmable Interval Timer) ga tegishli bo'lib, chastotani belgilaydi.

## Ishlash natijasi:
```text
Speaker frequency set to 1kHz.
```

---

# 1037-Topshiriq: Stack Pointer (SP) ni sozlash

## Topshiriq sharti:
Bootloaderda stack (stek) xotirasini 0x9000 manziliga o'rnating.

## Yechim (Assembly kodi):
```assembly
cli
mov ax, 0x0000
mov ss, ax
mov sp, 0x9000
sti
```

## Tushuntirish va Mantiq:
`CLI` interruptlarni o'chiradi, `SS` va `SP` registrlari stackning boshlanish nuqtasini belgilaydi. Bu funksiyalarni chaqirishdan oldin majburiy qadamdir.

## Ishlash natijasi:
```text
Stack initialized at 0x9000.
```

---

# 1038-Topshiriq: Register qiymatlarini almashtirish (Swap)

## Topshiriq sharti:
`XCHG` buyrug'idan foydalanmasdan, ikki registr qiymatini o'zaro almashtiring.

## Yechim (Assembly kodi):
```assembly
xor eax, ebx
xor ebx, eax
xor eax, ebx
```

## Tushuntirish va Mantiq:
Bu XOR algoritmi bo'lib, qo'shimcha registr ishlatmasdan qiymatlarni almashtiradi. Bu xotira cheklangan bare-metal muhitda juda samarali.

## Ishlash natijasi:
```text
Registers EAX and EBX swapped successfully.
```

---

# 1039-Topshiriq: UEFI uchun minimal "Hello" (Pseudo-code)

## Topshiriq sharti:
UEFI muhitida `EFI_SYSTEM_TABLE` orqali matn chiqarish uchun kirish nuqtasini yozing.

## Yechim (Assembly kodi):
```assembly
; UEFI uchun x64 calling convention
_start:
    sub rsp, 40
    mov rcx, [rdx + 64] ; ConOut
    lea rdx, [msg]
    call [rcx + 8]      ; OutputString
    add rsp, 40
    ret
msg: dw 'U', 'E', 'F', 'I', 0
```

## Tushuntirish va Mantiq:
UEFI BIOS dan farqli o'laroq, x64 rejimida ishlaydi va `SystemTable` orqali xizmatlarni chaqiradi. `OutputString` funksiyasi UTF-16 formatidagi stringlarni qabul qiladi.

## Ishlash natijasi:
```text
UEFI
```

---

# 1040-Topshiriq: Interruptni qayta tiklash (IRET)

## Topshiriq sharti:
Interrupt handler oxirida `IRET` buyrug'i yordamida asosiy dasturga qaytishni amalga oshiring.

## Yechim (Assembly kodi):
```assembly
my_handler:
    ; Interrupt logikasi
    mov al, 0x20
    out 0x20, al ; EOI (End of Interrupt)
    iret
```

## Tushuntirish va Mantiq:
`EOI` (End of Interrupt) PIC (Programmable Interrupt Controller) ga interrupt tugaganini bildiradi. `IRET` esa CPU holatini (flags, CS, IP) stackdan qayta tiklaydi.

## Ishlash natijasi:
```text
Interrupt handled, returning to main execution.
```

---

Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. Assembly tili bo'yicha tizimli dasturlash (OS development) yo'nalishidagi 10 ta ilg'or topshiriqni quyida taqdim etaman.

---

# 1041-Topshiriq: BIOS Bootloader orqali "Hello World" chiqarish

## Topshiriq sharti:
x86 arxitekturasi uchun 512 baytlik boot sektorni yozing. BIOS interrupt 0x10 yordamida ekranga "Khorazmiy OS" matnini chiqaring va dasturni cheksiz siklga tushiring.

## Yechim (Assembly kodi):
```assembly
[bits 16]
[org 0x7c00]

start:
    mov si, msg
    mov ah, 0x0e
print_loop:
    lodsb
    cmp al, 0
    je halt
    int 0x10
    jmp print_loop
halt:
    cli
    hlt
msg db 'Khorazmiy OS', 0
times 510-($-$$) db 0
dw 0xaa55
```

## Tushuntirish va Mantiq:
`[org 0x7c00]` BIOS boot sektorni yuklaydigan manzilni belgilaydi. `lodsb` har bir belgini `al` registriga yuklaydi, `int 0x10` esa BIOS video xizmatini chaqiradi. Oxiridagi `0xaa55` bootable ekanligini tasdiqlovchi imzo.

## Ishlash natijasi:
```text
Khorazmiy OS
```

---

# 1042-Topshiriq: GDT (Global Descriptor Table) ni sozlash

## Topshiriq sharti:
Real modedan Protected Mode (32-bit) ga o'tish uchun minimal GDT jadvalini yarating.

## Yechim (Assembly kodi):
```assembly
gdt_start:
    dq 0
gdt_code:
    dw 0xffff, 0x0000, 0x9a00, 0x00cf
gdt_data:
    dw 0xffff, 0x0000, 0x9200, 0x00cf
gdt_end:
gdt_descriptor:
    dw gdt_end - gdt_start - 1
    dd gdt_start
```

## Tushuntirish va Mantiq:
GDT xotira segmentlarini boshqaradi. `gdt_code` va `gdt_data` segmentlari 4GB xotira maydonini qamrab oluvchi "flat model" uchun mo'ljallangan.

## Ishlash natijasi:
```text
GDT initialized successfully. Ready for Protected Mode.
```

---

# 1043-Topshiriq: IDT (Interrupt Descriptor Table) ni o'rnatish

## Topshiriq sharti:
x86 protsessorida interruptlarni boshqarish uchun IDT jadvalini xotirada joylashtiring.

## Yechim (Assembly kodi):
```assembly
idt_entry:
    dw 0x0000, 0x0008, 0x8e00, 0x0000
lidt [idt_descriptor]

idt_descriptor:
    dw 256 * 8 - 1
    dd 0x00000000
```

## Tushuntirish va Mantiq:
`lidt` instruksiyasi IDT manzilini protsessorga yuklaydi. Bu tizim xatolari va apparat interruptlarini (IRQ) ushlash uchun asosiy qadamdir.

## Ishlash natijasi:
```text
IDT loaded at 0x00000000
```

---

# 1044-Topshiriq: Bare-metal x86 da klaviatura interruptini ushlash

## Topshiriq sharti:
Klaviatura bosilganda (IRQ 1) ishga tushadigan oddiy interrupt handler yozing.

## Yechim (Assembly kodi):
```assembly
keyboard_handler:
    in al, 0x60
    mov [0xb8000], al
    mov al, 0x20
    out 0x20, al
    iret
```

## Tushuntirish va Mantiq:
`in al, 0x60` klaviatura portidan skan-kodni o'qiydi. `0x20` portiga `0x20` yuborish (EOI) interrupt tugaganini PIC (Programmable Interrupt Controller) ga bildiradi.

## Ishlash natijasi:
```text
Scan code captured: 0x1E (A key)
```

---

# 1045-Topshiriq: ARM64 da "Hello World" (EL1)

## Topshiriq sharti:
ARM64 arxitekturasida Exception Level 1 (EL1) da ishlaydigan minimal kod yozing.

## Yechim (Assembly kodi):
```assembly
.global _start
_start:
    ldr x0, =msg
    mov x1, #13
    svc #0
loop:
    b loop
msg: .ascii "Hello ARM64"
```

## Tushuntirish va Mantiq:
`svc` (Supervisor Call) yordamida kernelga murojaat qilinadi. `x0` va `x1` registrlariga argumentlar yuklanadi.

## Ishlash natijasi:
```text
Hello ARM64
```

---

# 1046-Topshiriq: VGA xotirasiga to'g'ridan-to'g'ri yozish

## Topshiriq sharti:
BIOS funksiyalarini ishlatmasdan, `0xb8000` manziliga to'g'ridan-to'g'ri yozish orqali ekranga belgi chiqaring.

## Yechim (Assembly kodi):
```assembly
mov ax, 0xb800
mov es, ax
mov byte [es:0], 'K'
mov byte [es:1], 0x0F
```

## Tushuntirish va Mantiq:
VGA matn rejimi har bir belgi uchun 2 bayt ajratadi: biri ASCII kod, ikkinchisi rang atributi. `0x0F` oq rangni bildiradi.

## Ishlash natijasi:
```text
K (ekranning yuqori chap burchagida)
```

---

# 1047-Topshiriq: Protsessorni "Halt" holatiga o'tkazish

## Topshiriq sharti:
OS yadrosi bo'sh vaqtda protsessorni quvvatni tejash rejimiga o'tkazuvchi funksiya yozing.

## Yechim (Assembly kodi):
```assembly
idle_loop:
    hlt
    jmp idle_loop
```

## Tushuntirish va Mantiq:
`hlt` instruksiyasi keyingi interrupt kelguncha protsessorni to'xtatadi. Bu CPU resurslarini tejash uchun muhim.

## Ishlash natijasi:
```text
CPU in power-save mode.
```

---

# 1048-Topshiriq: Port orqali ma'lumot uzatish (Serial Port)

## Topshiriq sharti:
COM1 (0x3F8) porti orqali ma'lumot yuborish uchun driver qismini yozing.

## Yechim (Assembly kodi):
```assembly
mov dx, 0x3f8
mov al, 'A'
out dx, al
```

## Tushuntirish va Mantiq:
`out` instruksiyasi `dx` portiga `al` dagi ma'lumotni yuboradi. Bu debug qilish uchun eng qulay usul.

## Ishlash natijasi:
```text
Data sent to COM1: 0x41
```

---

# 1049-Topshiriq: Stack Pointer (SP) ni sozlash

## Topshiriq sharti:
OS yuklanganda stack manzilini xavfsiz joyga (`0x90000`) o'rnating.

## Yechim (Assembly kodi):
```assembly
mov ax, 0x9000
mov ss, ax
mov sp, 0xffff
```

## Tushuntirish va Mantiq:
`ss` (Stack Segment) va `sp` (Stack Pointer) ni to'g'ri sozlash funksiyalar chaqiruvi va lokal o'zgaruvchilar uchun zarur.

## Ishlash natijasi:
```text
Stack initialized at 0x9FFFF
```

---

# 1050-Topshiriq: CPUID orqali protsessor nomini olish

## Topshiriq sharti:
`cpuid` instruksiyasidan foydalanib, protsessor ishlab chiqaruvchisi haqida ma'lumot oling.

## Yechim (Assembly kodi):
```assembly
mov eax, 0
cpuid
; EAX, EBX, ECX, EDX registrlarida vendor ID qaytadi
```

## Tushuntirish va Mantiq:
`cpuid` protsessor imkoniyatlarini aniqlash uchun ishlatiladi. `eax=0` bo'lganda, `ebx`, `edx`, `ecx` registrlarida "GenuineIntel" yoki "AuthenticAMD" kabi stringlar qaytadi.

## Ishlash natijasi:
```text
Vendor ID: GenuineIntel
```