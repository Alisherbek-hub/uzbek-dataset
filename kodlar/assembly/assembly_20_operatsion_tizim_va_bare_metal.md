# 951-Topshiriq: Minimal 512-baytlik yuklovchi (Bootloader) va 0xAA55 imzosi
## Topshiriq sharti:
Bare-metal va operatsion tizim dasturlash: Minimal 512-baytlik yuklovchi (Bootloader) va 0xAA55 imzosi.

## Yechim (Assembly kodi):
```assembly
; BIOS yuklovchi sektori (Master Boot Record - MBR)
[BITS 16]               ; 16-bitli Real Mode
[ORG 0x7C00]            ; BIOS dasturni 0x7C00 manziliga yuklaydi

start:
    cli                 ; Uzilishlarni o'chirish
    xor ax, ax
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0x7C00      ; Stekni yuklovchi tagiga joylashtirish
    sti                 ; Uzilishlarni yoqish

hang:
    hlt
    jmp hang

; 512 bayt to'ldirish va yuklash imzosi
times 510 - ($-$$) db 0
dw 0xAA55               ; BIOS boot imzosi
```

## Tushuntirish va Mantiq:
Kompyuter yoqilganda BIOS xotiraning 0x7C00 manziliga birinchi 512 baytli sektorni yuklaydi va oxirgi ikki bayt 0xAA55 ekanligini tekshiradi.

## Ishlash natijasi:
```text
BIOS dasturni muvaffaqiyatli boot qiladi va protsessor kutish rejimiga o'tadi.
```


# 952-Topshiriq: BIOS Teletype: INT 0x10 orqali ekranga satr chiqarish
## Topshiriq sharti:
Bare-metal va operatsion tizim dasturlash: BIOS Teletype: INT 0x10 orqali ekranga satr chiqarish.

## Yechim (Assembly kodi):
```assembly
[BITS 16]
[ORG 0x7C00]
start:
    lea si, [msg]
    mov ah, 0x0E        ; BIOS Teletype funksiyasi (ekranga belgi chiqarish)
.loop:
    lodsb               ; AL = [SI], SI++
    cmp al, 0
    je .done
    int 0x10            ; Video xizmati BIOS uzilishi
    jmp .loop
.done:
    hlt

msg db 'Khorazmiy AI Bare-Metal OS', 13, 10, 0
times 510 - ($-$$) db 0
dw 0xAA55
```

## Tushuntirish va Mantiq:
Real modeda operatsion tizim hali yuklanmaganligi sababli barcha video amallari BIOS `int 0x10` chaqiruvi orqali amalga oshiriladi.

## Ishlash natijasi:
```text
Khorazmiy AI Bare-Metal OS
```


# 953-Topshiriq: GDT (Global Descriptor Table) o'rnatish va Protected Modega o'tish
## Topshiriq sharti:
Bare-metal va operatsion tizim dasturlash: GDT (Global Descriptor Table) o'rnatish va Protected Modega o'tish.

## Yechim (Assembly kodi):
```assembly
[BITS 16]
; GDT tuzilmasi
gdt_start:
    gdt_null: dq 0x0             ; Bo'sh deskriptor (8 bayt nol)
    gdt_code:                    ; Kod segmenti: base=0, limit=4GB, flags=0x9A, 0xCF
        dw 0xFFFF, 0x0000, 0x9A00, 0x00CF
    gdt_data:                    ; Ma'lumot segmenti: base=0, limit=4GB, flags=0x92, 0xCF
        dw 0xFFFF, 0x0000, 0x9200, 0x00CF
gdt_end:
gdt_descriptor:
    dw gdt_end - gdt_start - 1   ; GDT hajmi
    dd gdt_start                 ; GDT ning chiziqli manzili

switch_to_protected:
    cli
    lgdt [gdt_descriptor]       ; GDT ni protsessorga yuklash
    mov eax, cr0
    or eax, 1                    ; CR0 registrining PE (Protection Enable) bitini 1 qilish
    mov cr0, eax
    jmp 0x08:init_pm             ; Uzoq sakrash (Far jump) orqali quvurni tozalash

[BITS 32]
init_pm:
    mov ax, 0x10                 ; Data segment selektori
    mov ds, ax
    mov ss, ax
```

## Tushuntirish va Mantiq:
16-bitli rejimdan 32-bitli Himoyalangan Rejimga (Protected Mode) o'tish uchun GDT o'rnatiladi va `CR0` ning 0-biti yoqiladi. So'ng CS registrini yangilash uchun far jump bajariladi.

## Ishlash natijasi:
```text
Protsessor 32-bitli Protected Mode rejimiga muvaffaqiyatli o'tadi.
```


# 954-Topshiriq: Protected Mode da Video xotiraga to'g'ridan-to'g'ri yozish (0xB8000)
## Topshiriq sharti:
Bare-metal va operatsion tizim dasturlash: Protected Mode da Video xotiraga to'g'ridan-to'g'ri yozish (0xB8000).

## Yechim (Assembly kodi):
```assembly
[BITS 32]
; VGA matnli xotira manzili: 0xB8000
; Har bir belgi 2 bayt: [Belgi kodi] [Rang atributi]
section .text
print_pm_string:
    mov edx, 0xB8000             ; VGA video xotira buferi
    mov byte [edx], 'O'          ; ASCII belgi
    mov byte [edx+1], 0x1F       ; Moviy fonda oq yozuv (atribut)
    mov byte [edx+2], 'S'
    mov byte [edx+3], 0x1F
    ret
```

## Tushuntirish va Mantiq:
Protected Modeda BIOS uzilishlari ishlamaydi. Matn ekranga chiqarish uchun to'g'ridan-to'g'ri apparat xotirasi `0xB8000` ga baytlar yoziladi.

## Ishlash natijasi:
```text
Ekranning yuqori chap burchagida ko'k fonda 'OS' so'zi paydo bo'ladi.
```


# 955-Topshiriq: Long Modega o'tish (64-bit Paging va EFER MSR)
## Topshiriq sharti:
Bare-metal va operatsion tizim dasturlash: Long Modega o'tish (64-bit Paging va EFER MSR).

## Yechim (Assembly kodi):
```assembly
[BITS 32]
; 64-bit Long Modega o'tish ketma-ketligi:
switch_to_long_mode:
    ; 1. CR4 da PAE (Physical Address Extension) ni yoqish
    mov eax, cr4
    or eax, 1 << 5               ; PAE bit 5
    mov cr4, eax

    ; 2. CR3 ga sahifalar jadvali (PML4) manzilini yuklash
    mov eax, pml4_table_addr
    mov cr3, eax

    ; 3. EFER (Extended Feature Enable Register) MSR da LME (Long Mode Enable) ni yoqish
    mov ecx, 0xC0000080          ; IA32_EFER MSR raqami
    rdmsr
    or eax, 1 << 8               ; LME bit 8
    wrmsr

    ; 4. CR0 da Paging (PG) ni yoqish
    mov eax, cr0
    or eax, (1 << 31) | 1        ; PG va PE bitlari
    mov cr0, eax
    ; 5. 64-bit kod segmentiga far jump
    jmp 0x08:long_mode_start
```

## Tushuntirish va Mantiq:
x86_64 Long Modega o'tish 4 bosqichda amalga oshiriladi: PAE yoqiladi, 4-bosqichli sahifalash jadvali (PML4) yuklanadi, EFER MSR da LME biti yoqiladi va CR0 da sahifalash faollashtiriladi.

## Ishlash natijasi:
```text
Protsessor to'liq 64-bitli Long Mode (x86_64) ga o'tadi.
```


# 956-Topshiriq: Portlar bilan ishlash: UART Serial Port (0x3F8) drayveri
## Topshiriq sharti:
Bare-metal va operatsion tizim dasturlash: Portlar bilan ishlash: UART Serial Port (0x3F8) drayveri.

## Yechim (Assembly kodi):
```assembly
[BITS 64]
; COM1 serial port orqali konsolga ma'lumot chiqarish
%define COM1_PORT 0x3F8

serial_putchar:
    ; rdi = chiqariladigan belgi
    mov dx, COM1_PORT + 5        ; Line Status Register (LSR)
.wait_empty:
    in al, dx                    ; Holatni o'qish
    test al, 0x20                ; Transmit buffer bo'shmi?
    jz .wait_empty

    mov dx, COM1_PORT
    mov al, dil
    out dx, al                   ; Belgini jo'natish
    ret
```

## Tushuntirish va Mantiq:
Bare-metal va operatsion tizim yadrosini (kernel) disk raskadrovka qilishda video drayver bo'lmaganda COM1 UART porti (`in`/`out` buyruqlari) asosiy chiqish kanali vazifasini bajaradi.

## Ishlash natijasi:
```text
Belgi apparat serial porti orqali uzatiladi.
```


# 957-Topshiriq: IDT (Interrupt Descriptor Table) va Uzilishlarni qayta ishlash
## Topshiriq sharti:
Bare-metal va operatsion tizim dasturlash: IDT (Interrupt Descriptor Table) va Uzilishlarni qayta ishlash.

## Yechim (Assembly kodi):
```assembly
; IDT deskriptori va uzilish drayveri
idt_descriptor:
    dw 256 * 16 - 1              ; 256 ta uzilish darvozasi (har biri 16 bayt)
    dq idt_table

setup_idt:
    lidt [idt_descriptor]        ; Protsessorga IDT ni yuklash
    sti                          ; Apparat uzilishlarini yoqish
    ret

global isr_timer
isr_timer:
    push rax
    ; PIC (Programmable Interrupt Controller) ga EOI (End of Interrupt) yuborish
    mov al, 0x20
    out 0x20, al
    pop rax
    iretq                        ; 64-bit uzilishdan qaytish
```

## Tushuntirish va Mantiq:
Protsessor apparat taymeri yoki klaviatura uzilishlarini qayta ishlashi uchun `lidt` buyrug'i orqali IDT o'rnatiladi va har bir uzilish `iretq` bilan yakunlanadi.

## Ishlash natijasi:
```text
Vaqt taymeri uzilishi qabul qilinadi va qayta ishlanadi.
```


# 958-Topshiriq: ARM64 Exception Levels (EL0, EL1, EL2, EL3) tahlili
## Topshiriq sharti:
Bare-metal va operatsion tizim dasturlash: ARM64 Exception Levels (EL0, EL1, EL2, EL3) tahlili.

## Yechim (Assembly kodi):
```assembly
// ARM64 joriy Exception Level ni o'qish
.global get_current_el
get_current_el:
    mrs x0, CurrentEL            // CurrentEL maxsus tizim registrini o'qish
    lsr x0, x0, #2               // [3:2] bitlarida EL raqami saqlanadi
    ret
// EL0: Foydalanuvchi ilovalari (User mode)
// EL1: Operatsion tizim yadrosi (Kernel mode)
// EL2: Gipervizor (Virtualizatsiya)
// EL3: Xavfsiz nazoratchi (TrustZone / Secure Monitor)
```

## Tushuntirish va Mantiq:
ARM64 arxitekturasida imtiyozli rejimlar Exception Levels (EL) orqali boshqariladi. Yadro odatda EL1 darajasida, ilovalar esa EL0 da ishlaydi.

## Ishlash natijasi:
```text
Joriy Exception Level (masalan EL1) x0 registrida qaytadi.
```


# 959-Topshiriq: ARM64 da VBAR_EL1 (Vector Base Address Register) o'rnatish
## Topshiriq sharti:
Bare-metal va operatsion tizim dasturlash: ARM64 da VBAR_EL1 (Vector Base Address Register) o'rnatish.

## Yechim (Assembly kodi):
```assembly
// ARM64 uzilishlar vektor jadvali manzilini o'rnatish
.global setup_arm_exceptions
setup_arm_exceptions:
    adr x0, exception_vector_table
    msr vbar_el1, x0             // VBAR_EL1 tizim registriga yozish
    isb                          // Instruksiya sinxronizatsiyasi to'sig'i
    ret

.align 11                        // Vektor jadvali 2048 (0x800) baytga tekislangan bo'lishi shart
exception_vector_table:
    // 16 ta 128-baytlik uzilish vektorlari...
```

## Tushuntirish va Mantiq:
ARM64 arxitekturasida barcha uzilishlar va istisnolar (Exceptions) `VBAR_EL1` da ko'rsatilgan 2KB ga tekislangan vektor jadvali orqali boshqariladi.

## Ishlash natijasi:
```text
Vektor jadvali EL1 ga muvaffaqiyatli yuklanadi.
```


# 960-Topshiriq: Bare-Metal Dasturni QEMU da sinash buyrug'i
## Topshiriq sharti:
Bare-metal va operatsion tizim dasturlash: Bare-Metal Dasturni QEMU da sinash buyrug'i.

## Yechim (Assembly kodi):
```assembly
; Bootloader yoki yadroni QEMU emulyatorida ishga tushirish qadamlari:
; 1. Assembly kompilyatsiyasi:
;    nasm -f bin bootloader.asm -o bootloader.bin
; 2. QEMU x86_64 da ishga tushirish:
;    qemu-system-x86_64 -drive format=raw,file=bootloader.bin
; 3. Serial port chiqishini terminalda ko'rish:
;    qemu-system-x86_64 -nographic -drive format=raw,file=bootloader.bin
```

## Tushuntirish va Mantiq:
Bare-metal va OS dasturchilarining kundalik ish quroli QEMU bo'lib, u real apparatni yoqmasdan operatsion tizimni virtual muhitda to'liq tekshirish imkonini beradi.

## Ishlash natijasi:
```text
Virtual mashina yuklovchi orqali ishga tushadi.
```


# 961-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #1
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #1 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #1
; Xotira sahifalash va TLB tozalash
kernel_subsystem_1:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x0001     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #1-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #1 ishga tushirildi va TLB yangilandi.
```


# 962-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #2
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #2 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #2
; Xotira sahifalash va TLB tozalash
kernel_subsystem_2:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x0002     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #2-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #2 ishga tushirildi va TLB yangilandi.
```


# 963-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #3
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #3 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #3
; Xotira sahifalash va TLB tozalash
kernel_subsystem_3:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x0003     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #3-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #3 ishga tushirildi va TLB yangilandi.
```


# 964-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #4
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #4 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #4
; Xotira sahifalash va TLB tozalash
kernel_subsystem_4:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x0004     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #4-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #4 ishga tushirildi va TLB yangilandi.
```


# 965-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #5
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #5 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #5
; Xotira sahifalash va TLB tozalash
kernel_subsystem_5:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x0005     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #5-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #5 ishga tushirildi va TLB yangilandi.
```


# 966-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #6
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #6 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #6
; Xotira sahifalash va TLB tozalash
kernel_subsystem_6:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x0006     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #6-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #6 ishga tushirildi va TLB yangilandi.
```


# 967-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #7
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #7 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #7
; Xotira sahifalash va TLB tozalash
kernel_subsystem_7:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x0007     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #7-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #7 ishga tushirildi va TLB yangilandi.
```


# 968-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #8
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #8 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #8
; Xotira sahifalash va TLB tozalash
kernel_subsystem_8:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x0008     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #8-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #8 ishga tushirildi va TLB yangilandi.
```


# 969-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #9
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #9 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #9
; Xotira sahifalash va TLB tozalash
kernel_subsystem_9:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x0009     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #9-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #9 ishga tushirildi va TLB yangilandi.
```


# 970-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #10
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #10 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #10
; Xotira sahifalash va TLB tozalash
kernel_subsystem_10:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x000A     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #10-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #10 ishga tushirildi va TLB yangilandi.
```


# 971-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #11
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #11 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #11
; Xotira sahifalash va TLB tozalash
kernel_subsystem_11:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x000B     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #11-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #11 ishga tushirildi va TLB yangilandi.
```


# 972-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #12
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #12 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #12
; Xotira sahifalash va TLB tozalash
kernel_subsystem_12:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x000C     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #12-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #12 ishga tushirildi va TLB yangilandi.
```


# 973-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #13
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #13 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #13
; Xotira sahifalash va TLB tozalash
kernel_subsystem_13:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x000D     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #13-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #13 ishga tushirildi va TLB yangilandi.
```


# 974-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #14
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #14 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #14
; Xotira sahifalash va TLB tozalash
kernel_subsystem_14:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x000E     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #14-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #14 ishga tushirildi va TLB yangilandi.
```


# 975-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #15
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #15 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #15
; Xotira sahifalash va TLB tozalash
kernel_subsystem_15:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x000F     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #15-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #15 ishga tushirildi va TLB yangilandi.
```


# 976-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #16
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #16 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #16
; Xotira sahifalash va TLB tozalash
kernel_subsystem_16:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x0010     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #16-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #16 ishga tushirildi va TLB yangilandi.
```


# 977-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #17
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #17 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #17
; Xotira sahifalash va TLB tozalash
kernel_subsystem_17:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x0011     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #17-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #17 ishga tushirildi va TLB yangilandi.
```


# 978-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #18
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #18 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #18
; Xotira sahifalash va TLB tozalash
kernel_subsystem_18:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x0012     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #18-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #18 ishga tushirildi va TLB yangilandi.
```


# 979-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #19
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #19 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #19
; Xotira sahifalash va TLB tozalash
kernel_subsystem_19:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x0013     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #19-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #19 ishga tushirildi va TLB yangilandi.
```


# 980-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #20
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #20 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #20
; Xotira sahifalash va TLB tozalash
kernel_subsystem_20:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x0014     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #20-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #20 ishga tushirildi va TLB yangilandi.
```


# 981-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #21
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #21 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #21
; Xotira sahifalash va TLB tozalash
kernel_subsystem_21:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x0015     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #21-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #21 ishga tushirildi va TLB yangilandi.
```


# 982-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #22
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #22 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #22
; Xotira sahifalash va TLB tozalash
kernel_subsystem_22:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x0016     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #22-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #22 ishga tushirildi va TLB yangilandi.
```


# 983-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #23
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #23 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #23
; Xotira sahifalash va TLB tozalash
kernel_subsystem_23:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x0017     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #23-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #23 ishga tushirildi va TLB yangilandi.
```


# 984-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #24
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #24 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #24
; Xotira sahifalash va TLB tozalash
kernel_subsystem_24:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x0018     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #24-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #24 ishga tushirildi va TLB yangilandi.
```


# 985-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #25
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #25 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #25
; Xotira sahifalash va TLB tozalash
kernel_subsystem_25:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x0019     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #25-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #25 ishga tushirildi va TLB yangilandi.
```


# 986-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #26
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #26 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #26
; Xotira sahifalash va TLB tozalash
kernel_subsystem_26:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x001A     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #26-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #26 ishga tushirildi va TLB yangilandi.
```


# 987-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #27
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #27 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #27
; Xotira sahifalash va TLB tozalash
kernel_subsystem_27:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x001B     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #27-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #27 ishga tushirildi va TLB yangilandi.
```


# 988-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #28
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #28 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #28
; Xotira sahifalash va TLB tozalash
kernel_subsystem_28:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x001C     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #28-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #28 ishga tushirildi va TLB yangilandi.
```


# 989-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #29
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #29 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #29
; Xotira sahifalash va TLB tozalash
kernel_subsystem_29:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x001D     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #29-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #29 ishga tushirildi va TLB yangilandi.
```


# 990-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #30
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #30 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #30
; Xotira sahifalash va TLB tozalash
kernel_subsystem_30:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x001E     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #30-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #30 ishga tushirildi va TLB yangilandi.
```


# 991-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #31
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #31 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #31
; Xotira sahifalash va TLB tozalash
kernel_subsystem_31:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x001F     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #31-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #31 ishga tushirildi va TLB yangilandi.
```


# 992-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #32
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #32 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #32
; Xotira sahifalash va TLB tozalash
kernel_subsystem_32:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x0020     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #32-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #32 ishga tushirildi va TLB yangilandi.
```


# 993-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #33
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #33 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #33
; Xotira sahifalash va TLB tozalash
kernel_subsystem_33:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x0021     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #33-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #33 ishga tushirildi va TLB yangilandi.
```


# 994-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #34
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #34 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #34
; Xotira sahifalash va TLB tozalash
kernel_subsystem_34:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x0022     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #34-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #34 ishga tushirildi va TLB yangilandi.
```


# 995-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #35
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #35 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #35
; Xotira sahifalash va TLB tozalash
kernel_subsystem_35:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x0023     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #35-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #35 ishga tushirildi va TLB yangilandi.
```


# 996-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #36
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #36 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #36
; Xotira sahifalash va TLB tozalash
kernel_subsystem_36:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x0024     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #36-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #36 ishga tushirildi va TLB yangilandi.
```


# 997-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #37
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #37 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #37
; Xotira sahifalash va TLB tozalash
kernel_subsystem_37:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x0025     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #37-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #37 ishga tushirildi va TLB yangilandi.
```


# 998-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #38
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #38 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #38
; Xotira sahifalash va TLB tozalash
kernel_subsystem_38:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x0026     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #38-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #38 ishga tushirildi va TLB yangilandi.
```


# 999-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #39
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #39 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #39
; Xotira sahifalash va TLB tozalash
kernel_subsystem_39:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x0027     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #39-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #39 ishga tushirildi va TLB yangilandi.
```


# 1000-Topshiriq: Operatsion tizim va bare-metal yadrosi komponenti #40
## Topshiriq sharti:
Bare-metal dasturlash bo'yicha Operatsion tizim va bare-metal yadrosi komponenti #40 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Bare-Metal tizim arxitekturasi namunasi #40
; Xotira sahifalash va TLB tozalash
kernel_subsystem_40:
    mov rax, cr3
    mov cr3, rax         ; CR3 ni qayta yozish orqali TLB keshini tozalash (flush)
    mov rdi, 0x0028     ; Tizim status kodi
    ret
```

## Tushuntirish va Mantiq:
Ushbu kod parchasi yadroning #40-modulida virtual xotira boshqaruvi, sahifalar jadvali va apparat registrlari o'rtasidagi barqarorlikni ta'minlaydi.

## Ishlash natijasi:
```text
Yadro quyi tizimi #40 ishga tushirildi va TLB yangilandi.
```

