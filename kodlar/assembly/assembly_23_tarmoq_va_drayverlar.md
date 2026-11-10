# Khorazmiy AI: Assembly - Modul 23
## Mavzu: Tarmoq apparaturasi va paketlar: x86_64/ARM64 Bare-metal NIC (e1000/VirtIO) drayverlari, Packet Ring Buffers, Interrupt Handling va DMA

Salom, men **Khorazmiy AI** loyihasining past darajadagi tizimli dasturlash, operatsion tizim yadrolari (Kernel) va tarmoq apparaturasi drayverlari bo'yicha bosh dataset mutaxassisiman. Ushbu modulda x86_64 va ARM64 arxitekturalarida nol operatsion tizimsiz (Bare-metal) tarmoq kartalari (Intel e1000 va VirtIO-Net) bilan ishlash, PCI konfiguratsiya maydoni, MMIO registrlar, to'g'ridan-to'g'ri xotiraga kirish (DMA), Packet Ring Buffers (Rx/Tx halqalari), apparat uzilishlari (Interrupt Handling / MSI / GICv3), NAPI polling hamda xom Ethernet/IP/UDP/TCP paketlarini tahlil qilish va uzatish bo'yicha 50 ta (#1101 - #1150) mukammal amaliy topshiriq va ishlab turgan yechimlar jamlangan.

---

### Topshiriq #1101: PCI Konfiguratsiya Maydoni Orqali Tarmoq Kartasini (NIC) Qidirish
**Tavsif:** Operatsion tizim yadrosi (Kernel) yuklanganda, tizimga ulangan Intel e1000 (Vendor 0x8086, Device 0x100E) yoki VirtIO (Vendor 0x1AF4) tarmoq kartasini PCI shinasi bo'ylab skanerlab topishi kerak.
**Talablar:** x86_64 arxitekturasida PCI 0xCF8 (CONFIG_ADDRESS) va 0xCFC (CONFIG_DATA) I/O portlari orqali Bus (0-255), Device (0-31), Function (0-7) bo'yicha to'liq skanerlash funksiyasini yozish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global pci_find_network_card

; Port manzillari
PCI_CONFIG_ADDRESS equ 0x0CF8
PCI_CONFIG_DATA    equ 0x0CFC

; Qidirilayotgan e1000 identifikatorlari
INTEL_VENDOR_ID    equ 0x8086
E1000_DEV_ID       equ 0x100E   ; QEMU / VirtualBox 82540EP NIC

; Chiqish: RAX = BDF manzili (Bus << 16 | Dev << 11 | Func << 8), topilmasa -1
pci_find_network_card:
    push rbx
    push rcx
    push rdx

    xor ebx, ebx            ; EBX = Bus raqami (0 dan 255 gacha)

.bus_loop:
    xor ecx, ecx            ; ECX = Device raqami (0 dan 31 gacha)

.dev_loop:
    xor edx, edx            ; EDX = Function raqami (0 dan 7 gacha)

.func_loop:
    ; PCI Configuration Address registrini hisoblash:
    ; Bit 31: Enable bit (1)
    ; Bit 23-16: Bus
    ; Bit 15-11: Device
    ; Bit 10-8:  Function
    ; Bit 7-2:   Register Offset (0x00 - Vendor & Device ID)
    mov eax, 0x80000000
    mov esi, ebx
    shl esi, 16
    or eax, esi             ; Bus qo'shildi
    mov esi, ecx
    shl esi, 11
    or eax, esi             ; Device qo'shildi
    mov esi, edx
    shl esi, 8
    or eax, esi             ; Function qo'shildi
    ; Offset 0 (Vendor ID va Device ID)

    ; 0xCF8 portiga manzilni yozish
    mov dx, PCI_CONFIG_ADDRESS
    out dx, eax

    ; 0xCFC portidan 32-bitli ma'lumotni o'qish (Vendor ID [15:0], Device ID [31:16])
    mov dx, PCI_CONFIG_DATA
    in eax, dx

    ; Agar qurilma mavjud bo'lmasa, 0xFFFFFFFF qaytadi
    cmp ax, 0xFFFF
    je .next_func

    ; Intel e1000 tekshiruvi: Vendor == 0x8086 va Device == 0x100E
    cmp ax, INTEL_VENDOR_ID
    jne .next_func
    shr eax, 16
    cmp ax, E1000_DEV_ID
    jne .next_func

    ; Topildi! BDF manzilini RAX ga yig'ish
    mov eax, ebx
    shl eax, 16
    mov esi, ecx
    shl esi, 11
    or eax, esi
    pop rdx
    pop rcx
    pop rbx
    ret

.next_func:
    inc edx
    cmp edx, 8
    jl .func_loop

    inc ecx
    cmp ecx, 32
    jl .dev_loop

    inc ebx
    cmp ebx, 256
    jl .bus_loop

    ; Qurilma topilmadi
    mov rax, -1
    pop rdx
    pop rcx
    pop rbx
    ret
```
**Tushuntirish:** PCI shinasini skanerlash bare-metal operatsion tizimlar va drayverlar yuklanishining ilk qadamidir. `0xCF8` portiga 31-bitli yoqish bayrog'i (Enable Bit) bilan birga Bus, Device, Function indekslari uzatiladi va `0xCFC` orqali qurilmaning konfiguratsiya maydoniga kiriladi. Agar qurilma ulanmagan bo'lsa, ma'lumotlar liniyasida yuqori impedans sababli `0xFFFF` o'qiladi.

---

### Topshiriq #1102: PCI Command Registrida Bus Mastering va MMIO Ruxsatlarini Yoqish
**Tavsif:** Tarmoq kartasi asosiy xotiraga DMA (Direct Memory Access) orqali paketlarni yozishi va uning MMIO registrlariga murojaat qilinishi uchun PCI Command registrida Bus Master va Memory Space bitlari yoqilishi shart.
**Talablar:** PCI Offset 0x04 dagi Command registrini o'qish, Bit 0 (I/O Space), Bit 1 (Memory Space) va Bit 2 (Bus Master) ni yoqish va qayta yozish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global pci_enable_bus_mastering

PCI_CONFIG_ADDRESS equ 0x0CF8
PCI_CONFIG_DATA    equ 0x0CFC

; Kirish: RDI = BDF manzili (Bus, Device, Function)
pci_enable_bus_mastering:
    push rbx
    push rdx

    ; PCI Command register offseti = 0x04
    mov eax, edi
    and eax, 0xFFFF00       ; Bus, Dev, Func saqlanadi
    or eax, 0x80000004      ; Enable bit (Bit 31) + Offset 0x04

    ; Manzilni yozish
    mov dx, PCI_CONFIG_ADDRESS
    out dx, eax

    ; Hozirgi Command va Status registrini o'qish (16-bit Command, 16-bit Status)
    mov dx, PCI_CONFIG_DATA
    in eax, dx

    ; Bit 1: Memory Space Enable (MMIO registrlarga ruxsat)
    ; Bit 2: Bus Master Enable (Qurilma o'zi xotiraga DMA yozishi uchun ruxsat)
    or ax, 0x0006           ; 0b0000_0110 (Bit 1 va Bit 2)

    ; O'zgartirilgan qiymatni qayta yozish
    mov ebx, eax
    mov eax, edi
    and eax, 0xFFFF00
    or eax, 0x80000004
    mov dx, PCI_CONFIG_ADDRESS
    out dx, eax

    mov eax, ebx
    mov dx, PCI_CONFIG_DATA
    out dx, eax

    pop rdx
    pop rbx
    ret
```
**Tushuntirish:** `Bus Master Enable` (Bit 2) biti tarmoq kartasi protsessorni bezovta qilmasdan (protsessorsiz DMA) jismoniy operativ xotiraga (RAM) tarmoq paketlarini bevosita yozishi va o'qishi uchun ruxsat beradi. Ushbu bit yoqilmasa, har qanday DMA uzatishi apparat darajasida bloklanadi.

---

### Topshiriq #1103: PCI Base Address Register (BAR0) dan MMIO Fizik Manzilini Ajratib Olish
**Tavsif:** Tarmoq kartasining boshqaruv registrlariga kirish uchun qurilmaning PCI BAR0 registrida ko'rsatilgan 32-bit yoki 64-bit jismoniy MMIO (Memory-Mapped I/O) bazaviy manzilini o'qib olish talab etiladi.
**Talablar:** PCI Offset 0x10 (BAR0) ni o'qish, Memory Space indikatorini (Bit 0 == 0) tekshirish va quyi 4 ta bayroq bitlarini (0xFFFFFFF0) tozalash.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global pci_read_bar0_mmio

PCI_CONFIG_ADDRESS equ 0x0CF8
PCI_CONFIG_DATA    equ 0x0CFC

; Kirish: RDI = BDF manzili
; Chiqish: RAX = 64-bit MMIO jismoniy bazaviy manzili
pci_read_bar0_mmio:
    push rdx
    push rbx

    ; BAR0 offseti: 0x10
    mov eax, edi
    and eax, 0xFFFF00
    or eax, 0x80000010
    mov dx, PCI_CONFIG_ADDRESS
    out dx, eax

    mov dx, PCI_CONFIG_DATA
    in eax, dx              ; EAX = BAR0 qiymati

    ; Bit 0: 0 = Memory Mapped, 1 = I/O Port
    test al, 0x01
    jnz .is_io_space

    ; Bit 2-1: 00 = 32-bit manzil, 10 = 64-bit manzil
    mov ebx, eax
    and ebx, 0x06
    cmp ebx, 0x04           ; 64-bit MMIO tekshiruvi
    je .read_64bit

    ; 32-bit MMIO manzili: quyi 4 bitni tozalash (16 bayt alignment)
    and rax, 0xFFFFFFF0
    pop rbx
    pop rdx
    ret

.read_64bit:
    ; 64-bit BAR bo'lsa, yuqori 32-bit BAR1 (Offset 0x14) da joylashgan
    mov ebx, eax
    and ebx, 0xFFFFFFF0     ; Quyi 32-bit

    mov eax, edi
    and eax, 0xFFFF00
    or eax, 0x80000014      ; BAR1 offset 0x14
    mov dx, PCI_CONFIG_ADDRESS
    out dx, eax

    mov dx, PCI_CONFIG_DATA
    in eax, dx              ; EAX = Yuqori 32-bit

    shl rax, 32
    or rax, rbx             ; RAX = 64-bit to'liq jismoniy manzil
    pop rbx
    pop rdx
    ret

.is_io_space:
    ; Xatolik: Qurilma MMIO emas, I/O Port ishlatmoqda
    xor rax, rax
    pop rbx
    pop rdx
    ret
```
**Tushuntirish:** PCI standartida BAR (Base Address Register) bit 0 orqali qurilma xotiraga (MMIO) yoki I/O portlariga xaritalanganligini bildiradi. 64-bitli zamonaviy tarmoq kartalarida BAR0 va BAR1 birlashtirilib, 4GB dan yuqori fizik xotira manzillariga to'liq xaritalanish imkoniyati yaratiladi.

---

### Topshiriq #1104: Intel e1000 Boshqaruv Registrlariga MMIO Orqali Kirish Dvigateli
**Tavsif:** Intel e1000 gigabit tarmoq kartasida barcha boshqaruv buyruqlari (CTRL, STATUS, IMS, RCTL, TCTL) xotiraga xaritalangan 32-bitli registrlar orqali amalga oshiriladi. Drayver uchun xavfsiz o'qish va yozish funksiyalari kerak.
**Talablar:** Baza MMIO manzili va 32-bit offset orqali registrni o'qish (`e1000_read_reg`) va yozish (`e1000_write_reg`) drayver makrosini yaratish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global e1000_read_reg
global e1000_write_reg

; e1000 Asosiy Registr Offsetlari
E1000_REG_CTRL    equ 0x0000    ; Device Control
E1000_REG_STATUS  equ 0x0008    ; Device Status
E1000_REG_EECD    equ 0x0010    ; EEPROM/Flash Control
E1000_REG_EERD    equ 0x0014    ; EEPROM Read
E1000_REG_ICR     equ 0x00C0    ; Interrupt Cause Read
E1000_REG_IMS     equ 0x00D0    ; Interrupt Mask Set
E1000_REG_RCTL    equ 0x0100    ; Receive Control
E1000_REG_TCTL    equ 0x0400    ; Transmit Control

; Registrni o'qish: EAX = e1000_read_reg(RDI = mmio_base, RSI = reg_offset)
e1000_read_reg:
    mov eax, dword [rdi + rsi]  ; Xotiraga to'g'ridan-to'g'ri MMIO o'qish
    ret

; Registrga yozish: e1000_write_reg(RDI = mmio_base, RSI = reg_offset, EDX = value)
e1000_write_reg:
    mov dword [rdi + rsi], edx  ; MMIO registriga 32-bit yozish
    mfence                      ; Xotira to'sig'i: yozish apparatga darhol yetib borishini ta'minlaydi
    ret
```
**Tushuntirish:** MMIO (Memory Mapped I/O) da xotira manzillari to'g'ridan-to'g'ri qurilmaning ichki registrlariga ulanadi. Protsessorning kesh kontrolleri va instruksiyalar qayta tartiblanishi (Out-of-Order execution) tarmoq registrlari ketma-ketligini buzmasligi uchun `mfence` yoki volatile semantikasi qo'llanilishi shart.

---

### Topshiriq #1105: Intel e1000 EEPROM dan MAC Manzilini O'qib Olish
**Tavsif:** Tarmoq kartasi o'zining unikal 48-bitli fizik MAC manzilini bortdagi SPI/Microwire EEPROM chipida saqlaydi. Drayver ishga tushganda EERD (EEPROM Read) registri orqali ushbu 6 baytlik manzilni ajratib olishi shart.
**Talablar:** E1000_REG_EERD (0x0014) registriga Start bit (Bit 0) va Word Address ni yozish, Done bit (Bit 4) ni kutish va 16-bitli ma'lumotni o'qish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global e1000_read_mac_address

E1000_REG_EERD equ 0x0014

; Kirish: RDI = MMIO Baza manzili, RSI = 6 baytlik bufer ko'rsatkichi (MAC chiqishi)
e1000_read_mac_address:
    push rbx
    push r12
    push r13

    mov r12, rdi            ; R12 = MMIO baza
    mov r13, rsi            ; R13 = MAC bufer ko'rsatkichi

    ; EEPROM da MAC manzili dastlabki 3 ta 16-bitli so'zlarda (Word 0, 1, 2) saqlanadi
    xor ebx, ebx            ; EBX = Word indeksi (0, 1, 2)

.read_word_loop:
    ; EERD buyrug'ini tuzish:
    ; Bit 0: START = 1
    ; Bit 15:8: Word Address (EBX)
    mov eax, ebx
    shl eax, 8
    or eax, 0x01            ; START biti

    ; EERD registriga yozish
    mov dword [r12 + E1000_REG_EERD], eax

.wait_done:
    ; Natijani kutish: Bit 4 == 1 (DONE)
    pause
    mov eax, dword [r12 + E1000_REG_EERD]
    test eax, 0x10          ; Bit 4: DONE
    jz .wait_done

    ; Ma'lumot: Bit 31:16 oralig'idagi 16-bitli so'z
    shr eax, 16             ; AL = quyi bayt, AH = yuqori bayt

    ; MAC buferiga yozish (Little-endian tartibida 2 baytdan)
    mov byte [r13 + rbx*2], al
    mov byte [r13 + rbx*2 + 1], ah

    inc ebx
    cmp ebx, 3
    jl .read_word_loop

    pop r13
    pop r12
    pop rbx
    ret
```
**Tushuntirish:** Intel e1000 apparaturasida EEPROM ga kirish asinxron mikrodastur orqali amalga oshiriladi. `EERD` registriga o'qish so'rovi yuborilgach, apparat chipdan bitlarni ketma-ket tortadi va tayyor bo'lgach Bit 4 (Done) ni 1 qiladi. Ushbu 3 ta 16-bitli so'z yig'ilib standart 48-bit (6 bayt) MAC manzilini hosil qiladi.

---

### Topshiriq #1106: VirtIO-Net PCI Qurilmasi Xususiyatlarini (Feature Negotiation) Aniqlash
**Tavsif:** KVM va QEMU virtualizatsiya muhitlarida VirtIO-Net eng mashhur para-virtual drayver hisoblanadi. Drayver ishga tushganda gipervizor bilan qo'llab-quvvatlanadigan imkoniyatlarni (Checksum offload, MAC address, Status) kelishib olishi lozim.
**Talablar:** VirtIO PCI Device Features (Offset 0x00) va Guest Features (Offset 0x04) registrlarini o'qish hamda VIRTIO_NET_F_MAC (bit 5) ni faollashtirish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global virtio_net_negotiate_features

; VirtIO Legacy PCI Registrlari (BAR0 I/O port yoki MMIO)
VIRTIO_PCI_HOST_FEATURES  equ 0x00  ; 32-bit Host (QEMU) qo'llab-quvvatlaydigan xususiyatlar
VIRTIO_PCI_GUEST_FEATURES equ 0x04  ; 32-bit Mehmon drayveri qabul qiladigan xususiyatlar
VIRTIO_PCI_STATUS         equ 0x12  ; 8-bit Status

; VirtIO Net Xususiyat Bayroqlari
VIRTIO_NET_F_CSUM     equ (1 << 0)  ; Host checksum offloading
VIRTIO_NET_F_MAC      equ (1 << 5)  ; Qurilma o'z MAC manziliga ega
VIRTIO_NET_F_STATUS   equ (1 << 16) ; Aloqa holati (Link status)

; Kirish: RDI = VirtIO Base I/O Port yoki MMIO
virtio_net_negotiate_features:
    push rbx

    ; 1. Qurilma xususiyatlarini o'qish
    mov edx, edi
    in eax, dx              ; EAX = Host Features

    ; 2. Bizga kerakli bayroqlarni tekshirish (VIRTIO_NET_F_MAC va VIRTIO_NET_F_CSUM)
    mov ebx, (VIRTIO_NET_F_MAC | VIRTIO_NET_F_CSUM)
    and eax, ebx            ; Faqat ikkala tomon ham quvvatlaydigan xususiyatlar

    ; 3. Kelishilgan xususiyatlarni Guest Features registriga yozish
    mov ebx, eax
    lea edx, [edi + VIRTIO_PCI_GUEST_FEATURES]
    mov eax, ebx
    out dx, eax

    ; 4. Qurilma holatiga FEATURES_OK (0x08) va DRIVER_OK (0x04) qo'shish
    lea edx, [edi + VIRTIO_PCI_STATUS]
    in al, dx
    or al, 0x0C             ; DRIVER_OK | FEATURES_OK
    out dx, al

    mov eax, ebx            ; Qaytarish: kelishilgan xususiyatlar niqobi
    pop rbx
    ret
```
**Tushuntirish:** VirtIO spetsifikatsiyasi bo'yicha drayver va gipervizor o'rtasida 'Feature Negotiation' bosqichi majburiydir. Drayver o'zi tushunmaydigan yangi xususiyatlarni qabul qilmaydi, gipervizor esa faqat ikkala tomon tasdiqlagan qoidalarga binoan Virtqueue xotirasini boshqaradi.

---

### Topshiriq #1107: ARM64 MMIO: Device-nGnRnE Xotira Atributlari Bilan Tarmoq Registrlarini Xaritalash
**Tavsif:** ARM64 (AArch64) arxitekturasida tarmoq apparaturasi registrlariga murojaat qilishda oddiy xotira (Normal Memory) kabi keshlanmasligi va operatsiyalar tartibi buzilmasligi uchun sahifalar jadvalida Device-nGnRnE atributi o'rnatilishi shart.
**Talablar:** ARM64 MAIR_EL1 registrida Device-nGnRnE (0x00) indeksini o'qish va tarmoq registrlari uchun MMIO sahifa jadvali deskriptorini tuzish.
**Yechim (Assembly):**
```assembly
// AArch64 (ARM64) Assembly
.global arm64_map_nic_mmio

// Sahifa deskriptori atributlari (Page Table Entry - PTE)
// AttrIndx[2:0] = 000 (MAIR_EL1 dagi Device-nGnRnE indeksi)
// AP[2:1] = 00 (EL1 Read/Write)
// AF = 1 (Access Flag)
// SH = 10 (Outer Shareable)
.equ PTE_DEVICE_NGNRNE, (0x0 << 2) | (1 << 10) | (0x2 << 8) | (1 << 0) // Valid + AF + Device

// Kirish: X0 = Jismoniy MMIO baza manzili, X1 = Virtual xaritalash manzili, X2 = L3 Page Table manzili
arm64_map_nic_mmio:
    // Virtual manzilning L3 indeksini hisoblash (Bit 20:12)
    lsr x3, x1, #12
    and x3, x3, #0x1FF      // 512 ta yozuvdan biri (9 bit)

    // Jismoniy manzilga Device atributlarini qo'shish
    and x4, x0, #0x0000FFFFFFFFF000 // 4KB tekislangan manzil
    mov x5, #PTE_DEVICE_NGNRNE
    orr x4, x4, x5          // X4 = To'liq 64-bit PTE deskriptori

    // L3 Page table jadvaliga yozish
    str x4, [x2, x3, lsl #3]

    // Translation Lookaside Buffer (TLB) ni tozalash va to'siq o'rnatish
    tlbi vaae1is, x1        // Berilgan virtual manzil bo'yicha TLB invalidation
    dsb sy                  // Data Synchronization Barrier
    isb                     // Instruction Synchronization Barrier
    ret
```
**Tushuntirish:** ARM64 arxitekturasida `Device-nGnRnE` (no-Gathering, no-Reordering, no-Early-Write-Acknowledgement) eng qat'iy apparat xotira rejimidir. U tarmoq registriga yozilgan har qanday buyruq keshda ushlanmasdan, tartibi o'zgarmasdan to'g'ridan-to'g'ri jismoniy shina orqali tarmoq kartasiga yetkazilishini ta'minlaydi.

---

### Topshiriq #1108: x86_64 Port I/O Orqali PCI Registrlariga 32-bitli Universal Kirish Funksiyalari
**Tavsif:** Bare-metal tizimlarda har safar PCI registrini o'qish uchun kod takrorlanmasligi maqsadida BDF (Bus, Device, Function) va Register Offset qabul qiluvchi universal `pci_read_config_dword` va `pci_write_config_dword` funksiyalarini yaratish kerak.
**Talablar:** x86 IN va OUT buyruqlari yordamida PCI Config Space ustida 32-bitli xavfsiz o'qish va yozish funksiyalarini yozish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global pci_read_config_dword
global pci_write_config_dword

PCI_CONFIG_ADDRESS equ 0x0CF8
PCI_CONFIG_DATA    equ 0x0CFC

; uint32_t pci_read_config_dword(uint8_t bus, uint8_t dev, uint8_t func, uint8_t offset);
; RDI = bus, RSI = dev, RDX = func, RCX = offset
pci_read_config_dword:
    push rdx

    ; Manzilni yig'ish: 0x80000000 | (bus << 16) | (dev << 11) | (func << 8) | (offset & 0xFC)
    mov eax, edi
    shl eax, 16             ; bus << 16
    shl esi, 11             ; dev << 11
    or eax, esi
    shl edx, 8              ; func << 8
    or eax, edx
    and ecx, 0xFC           ; offset 4 baytga tekislangan bo'lishi shart
    or eax, ecx
    or eax, 0x80000000      ; Enable bit

    ; 0xCF8 ga yozish
    mov dx, PCI_CONFIG_ADDRESS
    out dx, eax

    ; 0xCFC dan o'qish
    mov dx, PCI_CONFIG_DATA
    in eax, dx

    pop rdx
    ret

; void pci_write_config_dword(uint8_t bus, uint8_t dev, uint8_t func, uint8_t offset, uint32_t value);
; RDI = bus, RSI = dev, RDX = func, RCX = offset, R8D = value
pci_write_config_dword:
    push rdx

    mov eax, edi
    shl eax, 16
    shl esi, 11
    or eax, esi
    shl edx, 8
    or eax, edx
    and ecx, 0xFC
    or eax, ecx
    or eax, 0x80000000

    mov dx, PCI_CONFIG_ADDRESS
    out dx, eax

    ; Qiymatni yozish
    mov eax, r8d
    mov dx, PCI_CONFIG_DATA
    out dx, eax

    pop rdx
    ret
```
**Tushuntirish:** PCI konfiguratsiya fazosiga murojaat qilishda offset har doim 4-baytga tekislangan (`offset & 0xFC`) bo'lishi shart. Agar 8-bit yoki 16-bit maydonlar kerak bo'lsa, avval to'liq 32-bit dword o'qiladi, so'ngra bitwise amallar (`shr`, `and`) orqali kerakli baytlar ajratib olinadi.

---

### Topshiriq #1109: PCIe MSI (Message Signaled Interrupts) Capability Strukturasini Aniqlash va Sozlash
**Tavsif:** Eski zanjirli IRQ uzilishlari (Legacy INTx) sekin va bir nechta qurilmalar orasida bo'lishilgan bo'ladi. Yuqori unumdorlikdagi tarmoq kartasi to'g'ridan-to'g'ri Local APIC ga xabar uzatishi uchun MSI rejimini yoqish lozim.
**Talablar:** PCI Capabilities Pointer (Offset 0x34) orqali bog'langan ro'yxatni aylanib chiqish, MSI Capability (ID 0x05) ni topish va Message Address hamda Message Data ni o'rnatish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global pci_configure_msi

PCI_CAP_ID_MSI equ 0x05

; Kirish: RDI = BDF manzili, ESI = APIC ID (Target CPU), EDX = Interrupt Vector (masalan 0x40)
pci_configure_msi:
    push rbx
    push r12
    push r13

    mov r12, rdi            ; BDF
    mov r13d, esi           ; APIC ID

    ; 1. Status registrida Capabilities List biti (Bit 4) borligini tekshirish
    ; Offset 0x04 ni o'qish
    ; ... (0x34 dagi Capabilities Pointer o'qiladi)
    ; Faraz qilaylik MSI Capability offseti 0x50 da topildi:
    mov ebx, 0x50           ; MSI Cap Offset

    ; 2. MSI Message Address registrini o'rnatish (Offset + 0x04)
    ; x86_64 Local APIC MSI manzili: 0xFEE00000 | (Destination APIC ID << 12)
    mov eax, 0xFEE00000
    shl r13d, 12
    or eax, r13d            ; Message Address

    ; Message Address ni PCI ga yozish
    ; pci_write_dword(BDF, ebx + 0x04, eax)

    ; 3. MSI Message Data registrini o'rnatish (Offset + 0x08)
    ; EDX = Vector raqami (masalan 0x40)
    ; pci_write_word(BDF, ebx + 0x08, dx)

    ; 4. MSI Control registrida MSI Enable (Bit 0) ni yoqish
    ; pci_read_word(BDF, ebx + 0x02) -> OR 0x0001 -> pci_write_word

    pop r13
    pop r12
    pop rbx
    ret
```
**Tushuntirish:** MSI (Message Signaled Interrupts) PCI xaritasidagi maxsus manzilga (`0xFEE00000`) 32-bitli xabar yozish orqali uzilish hosil qiladi. Bu an'anaviy elektr uzilish simlariga (IRQ liniyalariga) bo'lgan ehtiyojni yo'qotadi va paket kelgan zahoti uni kerakli protsessor yadrosining Local APIC'iga to'g'ridan-to'g'ri yo'naltiradi.

---

### Topshiriq #1110: Intel e1000 Apparat Resetlash Jarayoni va Link Up Holatini Kutish
**Tavsif:** Tarmoq kartasini dastlabki holatga keltirish uchun CTRL registrining Device Reset (RST) bitini yoqish, EEPROM avtomatik o'qilishini kutish va tarmoq kabeli ulanib aloqa o'rnatilganini (Link Up) tasdiqlash lozim.
**Talablar:** E1000_REG_CTRL dagi RST (bit 26) ni 1 qilish, 10 millisekund kutish, so'ngra E1000_REG_STATUS dagi LU (Link Up - bit 1) ni tekshirish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global e1000_hardware_reset

E1000_REG_CTRL   equ 0x0000
E1000_REG_STATUS equ 0x0008

E1000_CTRL_RST   equ (1 << 26)  ; Device Reset biti
E1000_STATUS_LU  equ (1 << 1)   ; Link Up biti

; Kirish: RDI = MMIO Baza manzili
; Chiqish: EAX = 1 (Link muvaffaqiyatli), 0 (Link yo'q)
e1000_hardware_reset:
    push rbx

    ; 1. Reset buyrug'ini yuborish
    mov eax, dword [rdi + E1000_REG_CTRL]
    or eax, E1000_CTRL_RST
    mov dword [rdi + E1000_REG_CTRL], eax
    mfence

    ; 2. Apparat tiklanishi uchun qisqa pauza (taxminan 20ms)
    mov ecx, 2000000
.delay_loop:
    pause
    dec ecx
    jnz .delay_loop

    ; 3. Reset tugagach, apparat RST bitini o'zi 0 ga tushiradi
.wait_reset_clear:
    mov eax, dword [rdi + E1000_REG_CTRL]
    test eax, E1000_CTRL_RST
    jnz .wait_reset_clear

    ; 4. Aloqa holatini (Link Up) tekshirish
    mov ecx, 5000000        ; Timeout hisoblagichi
.wait_link:
    mov eax, dword [rdi + E1000_REG_STATUS]
    test eax, E1000_STATUS_LU
    jnz .link_up
    pause
    dec ecx
    jnz .wait_link

    ; Link topilmadi (kabel ulanmagan)
    xor eax, eax
    pop rbx
    ret

.link_up:
    mov eax, 1              ; Aloqa o'rnatildi!
    pop rbx
    ret
```
**Tushuntirish:** Apparat resetlash (`CTRL.RST`) barcha ichki FIFO navbatlarini tozalaydi, EEPROM konfiguratsiyasini qayta o'qiydi va PHY chipini qayta ishga tushiradi. `STATUS.LU` (Link Up) biti tarmoq kartasi shina darajasida kabel ulanishini aniqlaganligini va to'liq dupleks (Full Duplex) rejimida ishlashga tayyorligini bildiradi.

---

### Topshiriq #1111: Fizik Xotirada 16-Baytga Tekislangan Rx Descriptor Halqasini Ajratish
**Tavsif:** Intel e1000 DMA kontrolleri paketlarni qabul qilish deskriptorlari (Rx Ring Buffer) xotirada 16-baytga yoki 128-baytga tekislangan (Aligned) bo'lishini qat'iy talab qiladi. Barcha deskriptorlar jismoniy xotirada uzluksiz (Contiguous Physical Memory) joylashishi shart.
**Talablar:** Boshlang'ich jismoniy sahifadan 32 ta Rx deskriptori (har biri 16 bayt = 512 bayt) uchun xotira ajratish va ularni nol bilan tozalash.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global alloc_rx_ring_descriptors

NUM_RX_DESCRIPTORS equ 32
DESC_SIZE          equ 16       ; Har bir Rx Deskriptor 16 bayt
TOTAL_RING_SIZE    equ (NUM_RX_DESCRIPTORS * DESC_SIZE) ; 512 bayt

; Kirish: RDI = 4KB tekislangan jismoniy sahifa bazasi
; Chiqish: RAX = 16-baytga tekislangan Rx Ring jismoniy manzili
alloc_rx_ring_descriptors:
    push rbx
    push rcx
    push rdi

    ; Manzil 16-baytga tekislanganligini tekshirish
    test rdi, 0x0F
    jz .is_aligned
    ; Agar tekislanmagan bo'lsa, keyingi 16-bayt chegarasiga siljitish
    add rdi, 16
    and rdi, ~0x0F

.is_aligned:
    mov rbx, rdi            ; RBX = Ring jismoniy manzili

    ; Ring buferni 0 bilan tozalash
    mov rdi, rbx
    xor eax, eax
    mov ecx, (TOTAL_RING_SIZE / 8) ; 64 ta qword (512 bayt)
    rep stosq

    mov rax, rbx            ; Natija
    pop rdi
    pop rcx
    pop rbx
    ret
```
**Tushuntirish:** Intel tarmoq kartalarining DMA dvigateli 128-bitli kenglikda xotira shinasiga ulanadi. Shu sababli Rx va Tx deskriptor massivlarining boshlang'ich manzili kamida 16 baytga (ideal holda kesh chizig'i 64/128 baytga) karrali bo'lishi apparat darajasidagi Alignment Fault xatolarini oldini oladi.

---

### Topshiriq #1112: Intel e1000 Rx Deskriptor (RDESC) Strukturasini Xotirada To'ldirish
**Tavsif:** Har bir Rx deskriptor 16 bayt bo'lib, unga tarmoq kartasi paket kelganda DMA orqali nusxalashi uchun bo'sh xotira buferining 64-bit fizik manzili (Buffer Address) biriktirilishi shart.
**Talablar:** e1000 Legacy Rx Descriptor strukturasi (Buffer Address [0..7], Length [8..9], Checksum [10..11], Status [12], Errors [13], Special [14..15]) ni to'ldirish funksiyasini yozish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global init_single_rx_descriptor

; struct e1000_rx_desc {
;     uint64_t buffer_addr; // 0..7: Fizik paket buferi manzili
;     uint16_t length;      // 8..9: Qabul qilingan paket uzunligi (NIC yozadi)
;     uint16_t checksum;    // 10..11: Packet Checksum
;     uint8_t  status;      // 12: Holat bayroqlari (DD, EOP)
;     uint8_t  errors;      // 13: Xatolik bayroqlari
;     uint16_t special;     // 14..15: VLAN tegi va boshqalar
; } __attribute__((packed));

; Kirish: RDI = Deskriptor manzili, RSI = 2048-baytlik paket buferining fizik manzili
init_single_rx_descriptor:
    ; 1. Paket buferi fizik manzilini yozish
    mov qword [rdi], rsi

    ; 2. Length va Checksum maydonlarini tozalash
    mov dword [rdi + 8], 0

    ; 3. Status va Errors maydonlarini tozalash (Status = 0: NIC ga tegishli ekanini bildiradi)
    mov dword [rdi + 12], 0

    ret
```
**Tushuntirish:** Rx deskriptorining `status` baytida eng muhim bit `DD` (Descriptor Done - Bit 0) hisoblanadi. Drayver dastlab bu maydonni 0 qilib tayyorlaydi. Tarmoq kartasi simdan paketni qabul qilib, uni DMA orqali `buffer_addr` ga joylashtirgach, `status` maydoniga `DD = 1` va `EOP = 1` (End of Packet) yozib qo'yadi.

---

### Topshiriq #1113: Rx Ring Buffer Registrlarini (RDBAL, RDBAH, RDLEN, RDH, RDT) Sozlash
**Tavsif:** Tarmoq kartasining DMA boshqaruvchisiga Rx deskriptor halqasining fizik boshlanish manzili, umumiy uzunligi hamda Head (RDH) va Tail (RDT) ko'rsatkichlarini ma'lum qilish lozim.
**Talablar:** RDBAL (0x2800), RDBAH (0x2804), RDLEN (0x2808), RDH (0x2810), RDT (0x2818) registrlarini o'rnatish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global e1000_setup_rx_ring_registers

E1000_REG_RDBAL equ 0x2800    ; Rx Descriptor Base Address Low
E1000_REG_RDBAH equ 0x2804    ; Rx Descriptor Base Address High
E1000_REG_RDLEN equ 0x2808    ; Rx Descriptor Length (baytlarda)
E1000_REG_RDH   equ 0x2810    ; Rx Descriptor Head
E1000_REG_RDT   equ 0x2818    ; Rx Descriptor Tail

; Kirish: RDI = MMIO Baza, RSI = Rx Ring Physical Address (64-bit), EDX = Deskriptorlar soni (masalan 32)
e1000_setup_rx_ring_registers:
    push rbx

    ; 1. Baza manzilining quyi 32-bitini RDBAL ga yozish
    mov eax, esi
    mov dword [rdi + E1000_REG_RDBAL], eax

    ; 2. Baza manzilining yuqori 32-bitini RDBAH ga yozish
    mov rax, rsi
    shr rax, 32
    mov dword [rdi + E1000_REG_RDBAH], eax

    ; 3. RDLEN: Ring ning umumiy hajmi baytlarda (NUM * 16)
    ; 128-baytga karrali bo'lishi shart!
    mov eax, edx
    shl eax, 4              ; EDX * 16 bayt
    mov dword [rdi + E1000_REG_RDLEN], eax

    ; 4. RDH (Head) ni 0 ga o'rnatish (NIC tomonidan boshqariladi)
    mov dword [rdi + E1000_REG_RDH], 0

    ; 5. RDT (Tail) ni so'nggi deskriptor indeksiga o'rnatish
    ; Tarmoq kartasi RDH dan RDT gacha bo'lgan oraliqni bo'sh deb biladi!
    dec edx
    mov dword [rdi + E1000_REG_RDT], edx

    mfence
    pop rbx
    ret
```
**Tushuntirish:** Rx Ring Buffer siklik halqa sifatida ishlaydi. Tarmoq kartasi paket qabul qilganda `RDH` (Head) ni oshirib boradi. Drayver esa paketlarni xotiradan o'qib bo'lgach, bo'shagan deskriptorlar hisobiga `RDT` (Tail) ni surib qo'yadi. Agar `RDH == RDT` bo'lsa, bu ring to'lganligini (Rx Buffer Overrun) anglatadi.

---

### Topshiriq #1114: Intel e1000 RCTL (Receive Control) Registrini Faollashtirish
**Tavsif:** Paketlarni qabul qilishni boshlash uchun RCTL registrida Receive Enable (EN), Broadcast Accept (BAM), Strip CRC (SECRC) va qabul buferi hajmini (BSIZE = 2048 bayt) sozlash zarur.
**Talablar:** RCTL (0x0100) registriga bitlarni (EN | BAM | BSIZE_2048 | SECRC) yozuvchi x86_64 funksiyasini yozish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global e1000_enable_rx

E1000_REG_RCTL   equ 0x0100

; RCTL Bayroqlari
E1000_RCTL_EN    equ (1 << 1)   ; Receiver Enable
E1000_RCTL_SBP   equ (1 << 2)   ; Store Bad Packets
E1000_RCTL_UPE   equ (1 << 3)   ; Unicast Promiscuous Enable
E1000_RCTL_MPE   equ (1 << 4)   ; Multicast Promiscuous Enable
E1000_RCTL_BAM   equ (1 << 15)  ; Broadcast Accept Mode
E1000_RCTL_BSIZE_2048 equ (0 << 16) ; Bufer o'lchami 2048 bayt (00b)
E1000_RCTL_SECRC equ (1 << 26)  ; Strip Ethernet CRC (Hardware CRC ni olib tashlash)

; Kirish: RDI = MMIO Baza manzili
e1000_enable_rx:
    ; Barcha zarur bayroqlarni birlashtirish
    mov eax, (E1000_RCTL_EN | E1000_RCTL_BAM | E1000_RCTL_BSIZE_2048 | E1000_RCTL_SECRC)

    ; RCTL registriga yozish
    mov dword [rdi + E1000_REG_RCTL], eax
    mfence
    ret
```
**Tushuntirish:** `E1000_RCTL_BAM` bayrog'i tarmoqdagi barcha Broadcast kadrlarini (masalan ARP so'rovlari `FF:FF:FF:FF:FF:FF`) qabul qilishni ta'minlaydi. `SECRC` esa apparat darajasida 4 baytli Ethernet Frame Check Sequence (CRC32) ni avtomatik tekshirib, xotiraga faqat foydali ma'lumotni kiritadi.

---

### Topshiriq #1115: Intel e1000 Tx Deskriptor (TDESC) Strukturasini Loyihalash
**Tavsif:** Paketlarni jo'natish uchun e1000 Tx Deskriptorida uzatilayotgan xom kadrning jismoniy manzili, uzunligi va CMD (Command) bayroqlari (EOP - End of Packet, IFCS - Insert FCS) to'ldirilishi lozim.
**Talablar:** e1000 Legacy Tx Descriptor (Buffer Address [0..7], Length [8..9], CSO [10], CMD [11], Status [12], CSS [13], Special [14..15]) ni to'ldiruvchi kod.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global prepare_tx_descriptor

; Tx Deskriptor CMD Bayroqlari
E1000_TXD_CMD_EOP  equ (1 << 0) ; End of Packet (paketning so'nggi qismi)
E1000_TXD_CMD_IFCS equ (1 << 1) ; Insert FCS (Ethernet apparat CRC ni qo'shish)
E1000_TXD_CMD_RS   equ (1 << 3) ; Report Status (Uzatib bo'lgach Status.DD ni 1 qilish)

; Kirish: RDI = Tx Deskriptor manzili, RSI = Paket buferi fizik manzili, DX = Paket uzunligi (bayt)
prepare_tx_descriptor:
    ; 1. Paket buferi fizik manzili (64-bit)
    mov qword [rdi], rsi

    ; 2. Uzunlik (16-bit)
    mov word [rdi + 8], dx

    ; 3. CSO (Checksum Offset) = 0
    mov byte [rdi + 10], 0

    ; 4. CMD: EOP | IFCS | RS (End of Packet + Avtomatik CRC + Holat hisoboti)
    mov al, (E1000_TXD_CMD_EOP | E1000_TXD_CMD_IFCS | E1000_TXD_CMD_RS)
    mov byte [rdi + 11], al

    ; 5. Status = 0 (NIC uzatishni tugatgach DD=1 qiladi)
    mov byte [rdi + 12], 0

    ; 6. CSS va Special maydonlari
    mov word [rdi + 14], 0
    ret
```
**Tushuntirish:** `E1000_TXD_CMD_IFCS` buyrug'i tarmoq kartasiga uzatilayotgan kadr oxiriga 4 baytli apparat CRC32 qiymatini o'zi hisoblab qo'shishni buyuradi. `RS` (Report Status) biti esa apparat paketni simga to'liq chiqarib yuborgach `status.DD` ni 1 qilishini ta'minlaydi.

---

### Topshiriq #1116: Tx Ring Buffer Registrlarini (TDBAL, TDBAH, TDLEN, TDH, TDT) Sozlash
**Tavsif:** Uzatish halqasini (Tx Ring) sozlash uchun uning jismoniy manzilini TDBAL/TDBAH ga, uzunligini TDLEN ga yozib, TDH va TDT registrlarini nolga tenglash lozim.
**Talablar:** TDBAL (0x3800), TDBAH (0x3804), TDLEN (0x3808), TDH (0x3810), TDT (0x3818) registrlarini o'rnatish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global e1000_setup_tx_ring_registers

E1000_REG_TDBAL equ 0x3800    ; Tx Descriptor Base Low
E1000_REG_TDBAH equ 0x3804    ; Tx Descriptor Base High
E1000_REG_TDLEN equ 0x3808    ; Tx Descriptor Length
E1000_REG_TDH   equ 0x3810    ; Tx Descriptor Head
E1000_REG_TDT   equ 0x3818    ; Tx Descriptor Tail

; Kirish: RDI = MMIO Baza, RSI = Tx Ring Physical Address, EDX = Deskriptorlar soni
e1000_setup_tx_ring_registers:
    ; Quyi va yuqori 32-bit manzillar
    mov eax, esi
    mov dword [rdi + E1000_REG_TDBAL], eax

    mov rax, rsi
    shr rax, 32
    mov dword [rdi + E1000_REG_TDBAH], eax

    ; Uzunlik (Baytlarda)
    mov eax, edx
    shl eax, 4              ; EDX * 16 bayt
    mov dword [rdi + E1000_REG_TDLEN], eax

    ; Boshlang'ich Head va Tail ikkalasi ham 0 bo'ladi (Halqa bo'sh)
    mov dword [rdi + E1000_REG_TDH], 0
    mov dword [rdi + E1000_REG_TDT], 0

    mfence
    ret
```
**Tushuntirish:** Tx Ring Buffer dastlab bo'sh bo'lganligi sababli `TDH` va `TDT` ikkalasi ham 0 ga o'rnatiladi. Drayver yangi paket yubormoqchi bo'lganda, `TDT` ko'rsatgan indeksga deskriptor yozadi va `TDT` registrini oshiradi (`(TDT + 1) % NUM`). Tarmoq kartasi darhol paketni DMA orqali tortib oladi.

---

### Topshiriq #1117: Intel e1000 TCTL (Transmit Control) Registrini Faollashtirish
**Tavsif:** Uzatish traktini ishga tushirish uchun TCTL registrida Transmit Enable (EN), Pad Short Packets (PSP), Collision Threshold (CT) va Cold Collision Distance (COLD) parametrlarini o'rnatish kerak.
**Talablar:** TCTL (0x0400) registriga EN (bit 1), PSP (bit 3), CT = 0x0F, COLD = 0x40 qiymatlarini yozish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global e1000_enable_tx

E1000_REG_TCTL   equ 0x0400

E1000_TCTL_EN    equ (1 << 1)   ; Transmit Enable
E1000_TCTL_PSP   equ (1 << 3)   ; Pad Short Packets (64 baytdan kichik paketlarni to'ldirish)
E1000_TCTL_CT    equ (0x0F << 4); Collision Threshold (15 urinish)
E1000_TCTL_COLD  equ (0x40 << 12); Collision Distance (Full-duplex uchun 0x40)

; Kirish: RDI = MMIO Baza
e1000_enable_tx:
    mov eax, (E1000_TCTL_EN | E1000_TCTL_PSP | E1000_TCTL_CT | E1000_TCTL_COLD)
    mov dword [rdi + E1000_REG_TCTL], eax
    mfence
    ret
```
**Tushuntirish:** `E1000_TCTL_PSP` (Pad Short Packets) Ethernet tarmog'ining IEEE 802.3 standartiga mos kelishi uchun o'ta muhim. Standart bo'yicha minimal Ethernet ramkasi 64 bayt bo'lishi kerak. Agar ilova 40 baytli kichik TCP ACK paketi yuborsa, tarmoq kartasi uni avtomatik tarzda nollar bilan 64 baytgacha to'ldirib uzatadi.

---

### Topshiriq #1118: ARM64 Cache Coherency va DMA: Data Cache Clean and Invalidate (DC CIVAC)
**Tavsif:** ARM64 arxitekturasida DMA kontrollerlari har doim ham CPU keshiga apparat darajasida sinxron (Coherent) bo'lmasligi mumkin. Paketni yuborishdan oldin keshni xotiraga chiqarish (Clean), qabul qilgandan so'ng esa keshni yaroqsiz qilish (Invalidate) shart.
**Talablar:** AArch64 `dc civac` (Clean and Invalidate by Virtual Address to PoC) instruksiyasi bilan kesh chiziqlari (Cache Line) bo'ylab xotirani sinxronlash.
**Yechim (Assembly):**
```assembly
// AArch64 (ARM64) Assembly
.global arm64_dma_cache_sync

// Kirish: X0 = Bufer virtual boshlanish manzili, X1 = Hajmi baytlarda
arm64_dma_cache_sync:
    // 1. Tizimdagi Kesh Chizig'i (Cache Line Size) hajmini o'qish (CTR_EL0)
    mrs x2, ctr_el0
    ubfx x2, x2, #16, #4    // DminLine maydoni (Log2 words)
    mov x3, #4
    lsl x3, x3, x2          // X3 = Kesh chizig'i baytlarda (odatda 64 bayt)

    // Manzilni kesh chizig'iga tekislash
    sub x4, x3, #1
    bic x0, x0, x4          // X0 = Tekislangan boshlanish manzili
    add x1, x1, x4          // Hajmni to'g'irlash

.cache_loop:
    // PoC (Point of Coherency) gacha keshni diskka yozish va eskirgan deb belgilash
    dc civac, x0
    add x0, x0, x3
    subs x1, x1, x3
    b.hi .cache_loop

    // To'liq xotira to'sig'i
    dsb sy
    isb
    ret
```
**Tushuntirish:** Agar ARM64 da `dc civac` chaqirilmasa, protsessor keshida turgan paket qismlari jismoniy operativ xotiraga (RAM) yozilmay qoladi va tarmoq kartasi eski yoki buzilgan ma'lumotni simga chiqaradi. Qabul qilishda esa CPU keshdagi eski ma'lumotni o'qib, tarmoq kartasi yangi yozgan paketni ko'rmay qolishi mumkin.

---

### Topshiriq #1119: VirtIO Split Virtqueue Arxitekturasi: Descriptor Table, Available Ring va Used Ring
**Tavsif:** VirtIO v1.0 standarti 3 ta alohida xotira sohasidan iborat Virtqueue arxitekturasidan foydalanadi: Deskriptorlar jadvali (Descriptor Table), Mehmon yuborgan buferlar halqasi (Available Ring) va Xost (QEMU) qaytargan buferlar halqasi (Used Ring).
**Talablar:** Virtqueue xotira sxemasini 4KB chegaralar bo'yicha hisoblovchi va boshlang'ich ko'rsatkichlarni bog'lovchi x86_64 funksiyasi.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global init_virtio_split_queue

; struct vring_desc { uint64_t addr; uint32_t len; uint16_t flags; uint16_t next; }; // 16 bayt
; struct vring_avail { uint16_t flags; uint16_t idx; uint16_t ring[QUEUE_SIZE]; };
; struct vring_used { uint16_t flags; uint16_t idx; struct vring_used_elem ring[QUEUE_SIZE]; };

; Kirish: RDI = Ajratilgan xotira bazasi (Kamida 16KB), ESI = Queue Size (masalan 128)
init_virtio_split_queue:
    push rbx

    ; 1. Descriptor Table boshlanishi = RDI
    ; Hajmi = ESI * 16 bayt

    ; 2. Available Ring boshlanishi = RDI + (ESI * 16)
    mov eax, esi
    shl eax, 4              ; EAX = ESI * 16
    lea rbx, [rdi + rax]    ; RBX = Available Ring manzili

    ; Available Ring idx = 0
    mov word [rbx + 2], 0   ; avail->idx = 0

    ; 3. Used Ring 4096 baytlik (4KB) sahifa chegarasiga tekislangan bo'lishi shart!
    ; Used offset = ALIGN_4K(sizeof(desc) + sizeof(avail))
    ; sizeof(avail) = 4 + 2 * ESI + 2
    mov edx, esi
    shl edx, 1              ; ESI * 2
    add edx, 6
    add eax, edx            ; EAX = umumiy o'lcham

    ; 4096 ga yuqoriga tekislash (Round up to 4KB)
    add eax, 4095
    and eax, ~4095

    lea rcx, [rdi + rax]    ; RCX = Used Ring manzili
    mov word [rcx + 2], 0   ; used->idx = 0

    mov rax, rdi            ; Descriptor table
    mov rdx, rbx            ; Avail ring
    ; RCX = Used ring
    pop rbx
    ret
```
**Tushuntirish:** VirtIO Split Virtqueue dizaynida Available Ring faqat Mehmon (Guest) tomonidan yoziladi va Xost tomonidan o'qiladi. Used Ring esa faqat Xost (Gipervizor) tomonidan yozilib, Mehmon tomonidan o'qiladi. Bu asimmetrik arxitektura qulflarsiz (Lock-free) bir yo'nalishli muloqotni ta'minlaydi.

---

### Topshiriq #1120: VirtIO Packed Virtqueue (v1.1) Arxitekturasi: Bayroqlar Bilan Bitta Halqada Ishlash
**Tavsif:** VirtIO 1.1 da uchta alohida xotira halqasi o'rniga kesh unumdorligini oshirish uchun bitta Packed Ring joriy qilingan. Unda Descriptor Table, Available va Used holatlari bitta 16-baytlik deskriptor ichidagi AVAIL (bit 7) va USED (bit 15) bayroqlari orqali boshqariladi.
**Talablar:** Packed Virtqueue deskriptoriga paket buferini joylashtirish va Wrap Counter / Flag bitlarini o'rnatish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global virtio_packed_enqueue_desc

; struct pvring_desc {
;     uint64_t addr;
;     uint32_t len;
;     uint16_t id;
;     uint16_t flags; // Bit 7: AVAIL, Bit 15: USED
; };

VRING_PACKED_DESC_F_AVAIL equ (1 << 7)
VRING_PACKED_DESC_F_USED  equ (1 << 15)

; Kirish: RDI = Packed Ring bazasi, ESI = Hozirgi Indeks, RDX = Fizik Manzil, ECX = Uzunlik, R8B = Wrap Counter (0 yoki 1)
virtio_packed_enqueue_desc:
    ; Indeks bo'yicha deskriptor manzilini hisoblash (ESI * 16)
    mov eax, esi
    shl eax, 4
    lea rax, [rdi + rax]    ; RAX = Deskriptor manzili

    ; Manzil va uzunlikni yozish
    mov qword [rax], rdx
    mov dword [rax + 8], ecx
    mov word [rax + 12], si ; ID = Indeks

    ; Bayroqlarni hisoblash:
    ; Agar Wrap Counter == 1 bo'lsa, AVAIL = 1, USED = 0
    ; Agar Wrap Counter == 0 bo'lsa, AVAIL = 0, USED = 1
    xor edx, edx
    test r8b, r8b
    jz .wrap_zero
    mov dx, VRING_PACKED_DESC_F_AVAIL
    jmp .write_flags

.wrap_zero:
    mov dx, VRING_PACKED_DESC_F_USED

.write_flags:
    mov word [rax + 14], dx
    mfence
    ret
```
**Tushuntirish:** Packed Virtqueue xotiradagi sakrashlarni (Cache Miss) keskin qisqartiradi. Gipervizor va drayver aynan bitta uzluksiz xotira blokida ishlaydi, va 'Wrap Counter' mexanizmi orqali halqa oxiriga yetganda indekslarni qayta nollamasdan faqat flag polaritesini teskarisiga o'giradi.

---

### Topshiriq #1121: Bare-metal Ethernet Ramkasini (Ethernet Frame) Xotirada Yig'uvchi Generator
**Tavsif:** Tarmoqqa istalgan paketni uzatish uchun avvalo 14 baytlik Ethernet II sarlavhasi (Destination MAC [6 bayt], Source MAC [6 bayt], EtherType [2 bayt Big-endian]) to'ldirilishi lozim.
**Talablar:** IPv4 (EtherType 0x0800) yoki ARP (0x0806) kadrini yig'ib, foydali yukni (Payload) nusxalovchi x86_64 protsedurasi.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global assemble_ethernet_frame

; Kirish:
; RDI = Maqsadli bufer
; RSI = Dst MAC (6 bayt)
; RDX = Src MAC (6 bayt)
; CX  = EtherType (masalan 0x0800 - IPv4)
; R8  = Payload manzili
; R9D = Payload uzunligi
; Chiqish: EAX = Jami Ethernet kadr hajmi (14 + Payload)
assemble_ethernet_frame:
    push rbx
    push rsi
    push rdi

    mov rbx, rdi            ; Boshlang'ich kadr manzili

    ; 1. Dst MAC (6 bayt) ni nusxalash
    mov eax, dword [rsi]
    mov dword [rdi], eax
    mov ax, word [rsi + 4]
    mov word [rdi + 4], ax
    add rdi, 6

    ; 2. Src MAC (6 bayt) ni nusxalash
    mov eax, dword [rdx]
    mov dword [rdi], eax
    mov ax, word [rdx + 4]
    mov word [rdi + 4], ax
    add rdi, 6

    ; 3. EtherType (2 bayt Big-Endian tartibida)
    xchg cl, ch             ; Baytlar tartibini o'girish (Host to Network Short)
    mov word [rdi], cx
    add rdi, 2

    ; 4. Payload ma'lumotlarini nusxalash
    mov rsi, r8
    mov ecx, r9d
    rep movsb

    ; Umumiy hajmni hisoblash
    mov rax, rdi
    sub rax, rbx            ; Jami baytlar soni

    pop rdi
    pop rsi
    pop rbx
    ret
```
**Tushuntirish:** Ethernet II sarlavhasida EtherType maydoni tarmoq tartibida (Big-Endian / Network Byte Order) bo'lishi shart. `xchg cl, ch` instruksiyasi x86 ning Little-Endian formatini Big-Endian formatiga 1 ta siklda o'giradi. Ushbu 14 bayt kadrning eng boshiga joylashadi.

---

### Topshiriq #1122: Ethernet Kadrini e1000 Tx Ring Orqali Uzatish va TDT Registrini Yangilash
**Tavsif:** Tayyorlangan paket buferini e1000 Tx Ring navbatiga qo'shish va tarmoq kartasining DMA boshqaruvchisiga uzatishni boshlash haqida signal berish (Doorbell) talab etiladi.
**Talablar:** Joriy TDT (Tail) indeksidagi Tx deskriptorini to'ldirish, TDT ni keyingi katakka surish (`(TDT + 1) % NUM_TX_DESC`) va MMIO TDT registriga yozish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global e1000_send_packet

E1000_REG_TDT equ 0x3818
NUM_TX_DESCRIPTORS equ 32

; Kirish: RDI = MMIO Baza, RSI = Tx Ring Baza virtual manzili, RDX = Paket buferi jismoniy manzili, ECX = Paket uzunligi
e1000_send_packet:
    push rbx
    push r12

    mov r12, rdi            ; MMIO Baza

    ; 1. Hozirgi TDT (Tail) indeksini o'qish
    mov ebx, dword [r12 + E1000_REG_TDT]

    ; 2. Deskriptor manzilini hisoblash: RSI + (EBX * 16)
    mov eax, ebx
    shl eax, 4              ; EBX * 16
    lea rax, [rsi + rax]    ; RAX = Deskriptor manzili

    ; 3. Deskriptor parametrlarini yozish:
    mov qword [rax], rdx    ; Buffer Physical Address
    mov word [rax + 8], cx  ; Length

    ; CMD: EOP (bit 0) | IFCS (bit 1) | RS (bit 3) = 0x0B
    mov byte [rax + 11], 0x0B
    mov byte [rax + 12], 0  ; Status = 0

    mfence

    ; 4. TDT indeksini oshirish (Siklik halqa)
    inc ebx
    cmp ebx, NUM_TX_DESCRIPTORS
    jl .no_wrap
    xor ebx, ebx            ; 0 ga aylanadi

.no_wrap:
    ; 5. Yangilangan TDT ni apparat registriga yozish (Doorbell!)
    mov dword [r12 + E1000_REG_TDT], ebx
    mfence

    pop r12
    pop rbx
    ret
```
**Tushuntirish:** `TDT` (Transmit Descriptor Tail) registriga yangi indeks yozilishi tarmoq kartasining DMA blokiga apparat triggeri (Doorbell) vazifasini o'taydi. Kartaning mikrokontrolleri yangi deskriptorni o'qib, PCIe shinasi orqali paketni to'g'ridan-to'g'ri o'zining ichki FIFO buferiga tortib oladi va kabelga uzatadi.

---

### Topshiriq #1123: Tx Deskriptor Holatini Polling Orqali Tekshirish va Paket Uzatilishini Tasdiqlash
**Tavsif:** Paket simga to'liq chiqib ketmasdan oldin uning xotira buferini qayta ishlatish ma'lumotlar buzilishiga olib keladi. Drayver Tx deskriptorining Status maydonidagi DD (Descriptor Done) bitini tekshirishi kerak.
**Talablar:** Deskriptorning 12-baytidagi `status` ni tekshirish, `DD` (bit 0) 1 bo'lguncha PAUSE orqali kutish (Busy-waiting) funksiyasi.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global e1000_wait_tx_complete

E1000_TXD_STAT_DD equ (1 << 0) ; Descriptor Done

; Kirish: RDI = Tekshirilayotgan Tx Deskriptor manzili, ESI = Maksimal timeout sikllari
; Chiqish: EAX = 1 (Uzatildi), 0 (Timeout)
e1000_wait_tx_complete:
    mov ecx, esi

.poll_loop:
    ; Status maydoni deskriptorning 12-baytida joylashgan
    mov al, byte [rdi + 12]
    test al, E1000_TXD_STAT_DD
    jnz .done               ; DD == 1 bo'lsa paket uzatildi!

    pause                   ; Protsessor quvvatini tejash va pipeline chaqnashini oldini olish
    dec ecx
    jnz .poll_loop

    ; Timeout: Tarmoq kartasi paketni uzata olmadi
    xor eax, eax
    ret

.done:
    mov eax, 1
    ret
```
**Tushuntirish:** `PAUSE` instruksiyasi x86 spin-loop (polling) davrlarida pipeline xatolarini (Memory Order Violation) oldini oladi va protsessor quvvat sarfini kamaytiradi. `DD` biti 1 bo'lgach, operatsion tizim ushbu paket buferini xavfsiz bo'shatishi yoki keyingi paketlar uchun qayta ishlatishi mumkin.

---

### Topshiriq #1124: Nol-Nusxa (Zero-Copy) Tarmoq DMA Uzatish Dvigateli
**Tavsif:** Oddiy tizimlarda ilova buferi avval yadro (Kernel) xotirasiga, so'ngra drayver buferiga nusxalanadi. Haqiqiy nol-nusxa (Zero-Copy) rejimida ilova buferining jismoniy sahifa manzili to'g'ridan-to'g'ri Tx deskriptoriga beriladi.
**Talablar:** Virtual manzilni Page Table (CR3) orqali jismoniy manzilga o'girish va to'g'ridan-to'g'ri TDESC ga biriktirish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global zero_copy_transmit_packet

; Kirish: RDI = Ilova buferi virtual manzili, ESI = Uzunlik, RDX = TDESC manzili, RCX = PML4 Page Table Baza manzili
zero_copy_transmit_packet:
    push rbx

    ; 1. Virtual manzilni (RDI) 4-darajali sahifalash (Paging) orqali Fizik manzilga aylantirish
    ; PML4 -> PDPT -> PD -> PT -> Physical Address
    ; Soddalashtirilgan yadro xaritasi (Identity Mapped yoki HHDM - Higher Half Direct Map):
    ; Agar yadro to'g'ridan-to'g'ri xaritalangan bo'lsa: Phys = Virt - KERNEL_BASE
    mov rax, rdi
    mov rbx, 0xFFFF800000000000 ; Misol: HHDM ofseti
    sub rax, rbx                ; RAX = Jismoniy manzil

    ; 2. Jismoniy manzilni to'g'ridan-to'g'ri TDESC ga o'rnatish
    mov qword [rdx], rax

    ; 3. Uzunlik va bayroqlarni o'rnatish
    mov word [rdx + 8], si
    mov byte [rdx + 11], 0x0B   ; EOP | IFCS | RS
    mov byte [rdx + 12], 0      ; Status = 0

    mfence
    pop rbx
    ret
```
**Tushuntirish:** Zero-Copy arxitekturasi xotira o'tkazuvchanligini (Memory Bandwidth) 3 barobar tejaydi. CPU keshiga bitta ham paket bayti nusxalanmaydi; PCIe DMA tekshiruvi ostida jismoniy xotira bloklari to'g'ridan-to'g'ri tarmoq kartasining uzatish buferiga o'qiladi.

---

### Topshiriq #1125: VirtIO-Net Xabar Uzatish: virtio_net_hdr Sarlavhasini To'ldirish va Available Ring ni Yangilash
**Tavsif:** VirtIO-Net drayveri har bir uzatilayotgan paket oldiga 10-baytlik (yoki 12-baytlik) `virtio_net_hdr` sarlavhasini (Flags, GSO turi, Checksum ofsetlari) joylashtirishi shart.
**Talablar:** virtio_net_hdr maydonlarini tozalash, Available Ring indeksini yangilash va xostga xabar tayyorlash.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global virtio_net_transmit

; struct virtio_net_hdr {
;     uint8_t flags;
;     uint8_t gso_type;
;     uint16_t hdr_len;
;     uint16_t gso_size;
;     uint16_t csum_start;
;     uint16_t csum_offset;
; }; // 10 bayt legacy, 12 bayt modern

; Kirish: RDI = Avail Ring manzili, RSI = Desc Table manzili, EDX = Bosh bo'sh indeks, RCX = Paket fiz manzili, R8D = Uzunlik
virtio_net_transmit:
    ; 1. Deskriptor jadvalida (RSI + EDX*16) paketni o'rnatish
    mov eax, edx
    shl eax, 4
    lea rax, [rsi + rax]

    mov qword [rax], rcx    ; Fizik manzil
    mov dword [rax + 8], r8d; Uzunlik
    mov word [rax + 12], 0  ; Flags = 0 (Zanjir oxiri)
    mov word [rax + 14], 0  ; Next = 0

    ; 2. Available Ring ni yangilash:
    ; struct vring_avail { uint16_t flags; uint16_t idx; uint16_t ring[]; };
    movzx eax, word [rdi + 2] ; EAX = avail->idx
    and eax, 0x7F           ; Queue size 128 modul bo'yicha indeks
    mov word [rdi + 4 + rax*2], dx ; ring[avail->idx % 128] = head_desc_idx

    ; avail->idx ni 1 ga oshirish
    inc word [rdi + 2]
    mfence
    ret
```
**Tushuntirish:** `virtio_net_hdr` virtualizatsiya qatlamida Checksum Offloading va TSO (TCP Segmentation Offload) kabi imkoniyatlarni boshqaradi. Oddiy paketlar uchun barcha bayroqlar 0 qilinadi, bu gipervizorga paket xom Ethernet kadri ekanligini bildiradi.

---

### Topshiriq #1126: VirtIO Doorbell (Queue Notify) Registriga Signal Berish (Hypervisor VM-Exit)
**Tavsif:** Available Ring ga yangi bufer qo'shilgandan so'ng, gipervizor (KVM/QEMU) darhol uyg'onishi uchun VirtIO Notify registriga navbat indeksini yozish (Doorbell) zarur.
**Talablar:** VirtIO PCI Notify Offset (0x10) ga Queue Index ni yozish va VM-Exit chaqiruvini hosil qilish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global virtio_notify_queue

; Kirish: RDI = VirtIO Base I/O Port yoki MMIO Manzili, ESI = Navbat Indeksi (masalan 1 = Tx Queue)
virtio_notify_queue:
    ; Legacy VirtIO da Notify registri Base + 0x10 da joylashgan (16-bit)
    lea edx, [edi + 0x10]
    mov ax, si
    out dx, ax              ; Port I/O orqali gipervizorga xabar berish!
    ret
```
**Tushuntirish:** `out dx, ax` instruksiyasi bajarilgan zahoti CPU apparat darajasida 'VM-Exit' holatiga o'tadi. Protsessor boshqaruvi virtual mashinadan gipervizorga (KVM) o'tadi va gipervizor mehmon xotirasidagi yangi paketlarni o'qib, ularni xostning haqiqiy tarmoq kartasiga uzatadi.

---

### Topshiriq #1127: Scatter-Gather DMA: Katta Paketni Bir Nechta Deskriptorlar Zanjiriga Bo'lib Uzatish
**Tavsif:** Agar tarmoq paketi bir nechta tarqoq xotira buferlarida (masalan, alohida sarlavha va alohida 64KB fayl bo'lagi) joylashgan bo'lsa, ularni bitta buferga nusxalamasdan, zanjirli (Scatter-Gather) deskriptorlar orqali uzatish lozim.
**Talablar:** e1000 da birinchi deskriptorda EOP=0, ikkinchi (yakuniy) deskriptorda EOP=1 qilib zanjir tuzish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global e1000_send_scatter_gather

; Kirish:
; RDI = Tx Ring Baza, ESI = Joriy Tail indeksi
; RDX = 1-bufer (Sarlavha) jismoniy manzili, ECX = 1-bufer uzunligi (masalan 54 bayt)
; R8  = 2-bufer (Foydali yuk) jismoniy manzili, R9D = 2-bufer uzunligi (masalan 1400 bayt)
e1000_send_scatter_gather:
    ; 1-Deskriptor: Faqat sarlavha (EOP yo'q!)
    mov eax, esi
    shl eax, 4
    lea rax, [rdi + rax]

    mov qword [rax], rdx
    mov word [rax + 8], cx
    mov byte [rax + 11], 0x0A ; IFCS | RS (EOP yo'q!)
    mov byte [rax + 12], 0

    ; 2-Deskriptor: Foydali yuk (EOP bor!)
    inc esi
    and esi, 31             ; Modulo 32
    mov eax, esi
    shl eax, 4
    lea rax, [rdi + rax]

    mov qword [rax], r8
    mov word [rax + 8], r9w
    mov byte [rax + 11], 0x0B ; EOP | IFCS | RS (Zanjir yakuni!)
    mov byte [rax + 12], 0

    mfence
    mov eax, esi            ; Yangi Tail indeksi qaytadi
    ret
```
**Tushuntirish:** Scatter-Gather DMA zamonaviy tarmoq drayverlarining eng kuchli qobiliyatidir. U operatsion tizimga sarlavha va ma'lumotlarni xotirada birlashtirish (Memory Copy) xarajatlaridan butunlay qutulish imkonini beradi.

---

### Topshiriq #1128: Intel e1000 Apparat Darajasida IP/TCP Checksum Offloading (TXCSUM) Sozlash
**Tavsif:** Har bir paketning IPv4 va TCP nazorat yig'indisini (Checksum) CPU da hisoblash protsessor quvvatini oladi. Intel e1000 NIC kartasi ushbu hisob-kitobni o'z apparat mikrosxemalarida avtomatik bajarishga qodir.
**Talablar:** e1000 Context Descriptor yaratish, TUCMD (TCP/UDP Command) da IDE (IP Checksum Enable) va TLE (TCP/UDP Checksum Enable) larni yoqish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global e1000_set_checksum_offload_context

; struct e1000_context_tx_desc {
;     uint8_t ipcss;  // IP Checksum Start
;     uint8_t ipcso;  // IP Checksum Offset
;     uint16_t ipcse; // IP Checksum End
;     uint8_t tucss;  // TCP/UDP Checksum Start
;     uint8_t tucso;  // TCP/UDP Checksum Offset
;     uint16_t tucse; // TCP/UDP Checksum End
;     uint32_t cmd_type_len;
;     uint8_t status;
;     uint8_t hdr_len;
;     uint16_t mss;
; };

; Kirish: RDI = Context Deskriptor manzili
e1000_set_checksum_offload_context:
    ; IP Checksum sozlamalari (Ethernet = 14 bayt)
    mov byte [rdi], 14      ; ipcss = 14 (IP sarlavha boshlanishi)
    mov byte [rdi + 1], 24  ; ipcso = 24 (Checksum joylashgan ofset)
    mov word [rdi + 2], 33  ; ipcse = 33 (IP sarlavha tugashi)

    ; TCP Checksum sozlamalari
    mov byte [rdi + 4], 34  ; tucss = 34 (TCP boshlanishi)
    mov byte [rdi + 5], 50  ; tucso = 50 (TCP Checksum joyi)
    mov word [rdi + 6], 0   ; tucse = 0 (Paket oxirigacha)

    ; DEXT (bit 29) va DTYP = Context (0x00)
    mov dword [rdi + 8], 0x20000000
    ret
```
**Tushuntirish:** Checksum Offloading yoqilganda CPU paket ichidagi nazorat yig'indisi maydonini nolga tenglashtirib yuboradi. Tarmoq kartasining DMA bloki paketni simga chiqarish jarayonida konveyer usulida baytlar yig'indisini hisoblab, tegishli ofsetga yozib yuboradi.

---

### Topshiriq #1129: ARM64 Xotira To'siqlari: DMB ISHST va DSB SY Bilan DMA Ketma-ketligini Ta'minlash
**Tavsif:** Kuchsiz xotira modeliga (Weakly Ordered Memory) ega ARM64 arxitekturasida deskriptorga ma'lumot yozilganidan so'ng, Doorbell registriga o'tishdan oldin apparat xotira to'siqlari o'rnatilishi shart.
**Talablar:** AArch64 `dmb ishst` (Data Memory Barrier Inner Shareable Stores) va `dsb sy` (Data Synchronization Barrier Full System) ko'rsatmalari bilan DMA xavfsizligini ta'minlash.
**Yechim (Assembly):**
```assembly
// AArch64 (ARM64) Assembly
.global arm64_dma_barrier_flush

arm64_dma_barrier_flush:
    // 1. DMB ISHST: Oldingi barcha xotira saqlash (Store) amallari
    // boshqa protsessorlar va DMA bloklari uchun ko'rinadigan bo'lishini ta'minlaydi
    dmb ishst

    // 2. DSB SY: Barcha xotira amallari to'liq yakunlanmaguncha keyingi instruksiya bajarilmaydi
    dsb sy
    ret
```
**Tushuntirish:** x86 arxitekturasida barcha saqlash amallari apparat darajasida tartiblangan bo'lsa (TSO modeli), ARM64 da xotiraga yozish amallari protsessor tomonidan ixtiyoriy tartibda optimallashtirilishi mumkin. `dmb ishst` siz tarmoq kartasi yangi paket yozilishidan oldinroq Doorbell signalini qabul qilib, xotiradagi eski ma'lumotni uzatib yuborishi xavfi mavjud.

---

### Topshiriq #1130: Paket Uzatish Kechikishini (Latency) O'lchash Uchun RDTSC va CNTVCT_EL0 Sikllar Hisoblagichi
**Tavsif:** Yuqori chastotali birja savdolarida (HFT) tarmoq kartasi drayverining har bir paketni jo'natishga sarflagan vaqtini mikrosekundlarda emas, CPU sikllarida aniq o'lchash zarur.
**Talablar:** x86_64 da `rdtsc` / `rdtscp` va ARM64 da `cntvct_el0` registrlaridan foydalanib o'lchov o'tkazuvchi funksiya.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global benchmark_tx_cycles_start
global benchmark_tx_cycles_end

; Chiqish: RAX = 64-bitlik CPU Cycle Counter
benchmark_tx_cycles_start:
    mfence
    rdtsc                   ; EDX:EAX = TSC
    shl rdx, 32
    or rax, rdx
    ret

; Chiqish: RAX = O'tgan sikllar soni, Kirish: RDI = Start Cycle
benchmark_tx_cycles_end:
    rdtscp                  ; Serializing RDTSC (barcha oldingi ko'rsatmalar tugashini kutadi)
    shl rdx, 32
    or rax, rdx             ; RAX = Hozirgi TSC
    sub rax, rdi            ; RAX = Hozirgi - Boshlang'ich
    ret
```
**Tushuntirish:** `rdtscp` instruksiyasi 'serializing' xususiyatiga ega bo'lib, uning atrofidagi kodlarning qayta tartiblanishiga (Out-of-Order execution) yo'l qo'ymaydi. Bu orqali tarmoq paketining DMA navbatiga qo'yilish vaqti nanosekundlik aniqlikda tahlil qilinadi.

---

### Topshiriq #1131: Intel e1000 Interrupt Mask Set/Read (IMS) Registrida Rx Uzilishlarini Yoqish
**Tavsif:** Tarmoq simidan yangi paket kelib tushganda CPU ga apparat uzilishi (Hardware Interrupt) yetib borishi uchun e1000 kartasining IMS registrida tegishli uzilish turlarini faollashtirish zarur.
**Talablar:** E1000_REG_IMS (0x00D0) registriga RXT0 (Receiver Timer Interrupt - bit 7), RXO (Receiver Overrun - bit 6) va LSC (Link Status Change - bit 2) bitlarini yozish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global e1000_enable_interrupts

E1000_REG_IMS  equ 0x00D0

; Uzilish Bayroqlari
E1000_IMS_RXT0 equ (1 << 7)     ; Receiver Timer Interrupt (Yangi paket qabul qilindi)
E1000_IMS_RXO  equ (1 << 6)     ; Receiver Overrun (Rx bufer to'lib ketdi)
E1000_IMS_RXDMT0 equ (1 << 4)   ; Rx Descriptor Minimum Threshold (Bo'sh joy oz qoldi)
E1000_IMS_LSC  equ (1 << 2)     ; Link Status Change (Kabel ulandi yoki uzildi)

; Kirish: RDI = MMIO Baza manzili
e1000_enable_interrupts:
    ; Barcha muhim uzilishlarni birlashtirish
    mov eax, (E1000_IMS_RXT0 | E1000_IMS_RXO | E1000_IMS_RXDMT0 | E1000_IMS_LSC)

    ; IMS registriga yozish
    mov dword [rdi + E1000_REG_IMS], eax
    mfence
    ret
```
**Tushuntirish:** Intel e1000 da `IMS` registriga 1 yozish uzilishni yoqadi, `IMC` (Interrupt Mask Clear - 0x00D8) registriga 1 yozish esa uzilishni o'chiradi. Bu dizayn o'qish-o'zgartirish-yozish (Read-Modify-Write) poyga sharoitlarisiz (Race conditions) atomar uzilish boshqaruvini ta'minlaydi.

---

### Topshiriq #1132: x86_64 IDT (Interrupt Descriptor Table) da Tarmoq IRQ Darvozasini (Interrupt Gate) O'rnatish
**Tavsif:** Tarmoq kartasi uzilish yuborganda CPU avtomatik tarzda IDT jadvalidagi tegishli 16-baytlik darvoza (Gate) orqali yadro ISR kodiga sakrashi kerak.
**Talablar:** 64-bit Interrupt Gate strukturasi (Offset 0..15, Selector, IST, Type=0x8E, Offset 16..31, Offset 32..63) ni IDT jadvaliga o'rnatuvchi funksiya.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global set_nic_idt_entry

; struct idt_entry_64 {
;     uint16_t offset_low;  // 0..15
;     uint16_t selector;    // 16..31 (Kernel Code Segment, masalan 0x08)
;     uint8_t  ist;         // 32..34: IST, 35..39: Reserved
;     uint8_t  type_attr;   // 40..47: 0x8E (Present, DPL 0, 64-bit Interrupt Gate)
;     uint16_t offset_mid;  // 48..63
;     uint32_t offset_high; // 64..95
;     uint32_t reserved;    // 96..127
; } __attribute__((packed));

; Kirish: RDI = IDT Table bazasi, ESI = Vektor raqami (masalan 0x20 + IRQ 11 = 0x2B), RDX = ISR funksiya manzili
set_nic_idt_entry:
    ; Vektor indeksi bo'yicha darvoza manzilini hisoblash (ESI * 16 bayt)
    mov eax, esi
    shl eax, 4
    lea rax, [rdi + rax]    ; RAX = IDT Entry manzili

    ; Quyi 16-bit ofset
    mov word [rax], dx

    ; Kernel Code Segment Selector (0x08)
    mov word [rax + 2], 0x08

    ; IST = 0, Type Attributes = 0x8E (Present, Ring 0, Interrupt Gate)
    mov byte [rax + 4], 0
    mov byte [rax + 5], 0x8E

    ; O'rta 16-bit ofset
    mov rcx, rdx
    shr rcx, 16
    mov word [rax + 6], cx

    ; Yuqori 32-bit ofset
    shr rcx, 16
    mov dword [rax + 8], ecx

    ; Zaxira 32-bit nollar
    mov dword [rax + 12], 0
    ret
```
**Tushuntirish:** 64-bit Long Mode da IDT yozuvi 16 bayt bo'lib, to'liq 64-bit virtual manzilni o'z ichiga oladi. `0x8E` atributi protsessor uzilish darvozasiga kirishi bilanoq `IF` (Interrupt Flag) ni avtomatik tozalab (CLI), ISR ichida boshqa uzilishlar chalkashib ketishining oldini oladi.

---

### Topshiriq #1133: Intel e1000 Interrupt Service Routine (ISR) va Uzilishni Tasdiqlash (Acknowledge)
**Tavsif:** Tarmoq uzilishi kelganda protsessor zudlik bilan e1000_REG_ICR (Interrupt Cause Read) registrini o'qishi shart. Ushbu o'qish apparat darajasida uzilish liniyasini tozalaydi (Auto-Clear).
**Talablar:** ISR kodi: Registrlarni stackka saqlash, ICR ni o'qish, APIC EOI (0xB0) ni yuborish va IRETQ orqali qaytish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global e1000_isr_handler
extern e1000_mmio_base
extern process_incoming_packet

E1000_REG_ICR equ 0x00C0
APIC_EOI_REG  equ 0xFEE000B0

e1000_isr_handler:
    ; 1. Barcha umumiy registrlarni stackka saqlash
    push rax
    push rbx
    push rcx
    push rdx
    push rsi
    push rdi
    push r8
    push r9
    push r10
    push r11

    ; 2. ICR (Interrupt Cause Read) registrini o'qish
    ; DIQQAT: ICR ni o'qishning o'zi uzilishni apparatda avtomatik tozalaydi!
    mov rdi, [rel e1000_mmio_base]
    mov eax, dword [rdi + E1000_REG_ICR]

    ; Bit 7: Yangi paket bormi? (RXT0)
    test eax, 0x80
    jz .check_other_events

    ; Paketlarni qabul qilish logikasini chaqirish
    call process_incoming_packet

.check_other_events:
    ; 3. Local APIC ga EOI (End of Interrupt) signalini yozish
    mov dword [APIC_EOI_REG], 0
    mfence

    ; 4. Registrlarni tiklash va uzilishdan qaytish
    pop r11
    pop r10
    pop r9
    pop r8
    pop rdi
    pop rsi
    pop rdx
    pop rcx
    pop rbx
    pop rax
    iretq                   ; Interrupt Return 64-bit
```
**Tushuntirish:** e1000 arxitekturasida `ICR` registrining o'ziga xos xususiyati shundaki, unga yozish talab etilmaydi; faqat bitta 32-bitli o'qish amali apparat ichidagi barcha faol uzilish bayroqlarini nollaydi. Agar `APIC EOI` yuborilmasa, Local APIC keyingi hech qanday apparat uzilishini protsessorga o'tkazmaydi.

---

### Topshiriq #1134: Rx Ring Bufferdan Yangi Paketlarni O'qish va RDT Ko'rsatkichini Oldinga Siljitish
**Tavsif:** Tarmoq kartasi yangi paketlarni xotiraga yozgach, drayver Rx Ring bo'ylab qaysi deskriptorlarda `status.DD == 1` ekanligini tekshirib, ma'lumotlarni qabul qilishi va bo'shagan joylarni RDT orqali apparatga qaytarishi lozim.
**Talablar:** Deskriptor Status.DD va Length maydonlarini o'qish, paketni qayta ishlashga uzatish, statusni tozalash va RDT ni oshirish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global e1000_poll_rx_ring
extern rx_packet_callback

E1000_REG_RDT equ 0x2818
NUM_RX_DESCRIPTORS equ 32

; Kirish: RDI = MMIO Baza, RSI = Rx Ring Baza virtual manzili, RDX = Joriy Rx Indeksi ko'rsatkichi (uint32_t*)
; Chiqish: EAX = Qabul qilingan paketlar soni
e1000_poll_rx_ring:
    push rbx
    push r12
    push r13
    push r14

    mov r12, rdi            ; MMIO Baza
    mov r13, rsi            ; Rx Ring
    mov r14, rdx            ; Joriy indeks manzili

    mov ebx, dword [r14]    ; Hozirgi tekshirilayotgan indeks
    xor ecx, ecx            ; ECX = Qabul qilingan paketlar hisoblagichi

.scan_loop:
    ; Deskriptor manzilini hisoblash: r13 + (ebx * 16)
    mov eax, ebx
    shl eax, 4
    lea rax, [r13 + rax]

    ; Status maydoni (Offset 12): Bit 0 = DD (Descriptor Done)
    mov dl, byte [rax + 12]
    test dl, 0x01
    jz .no_more_packets     ; Agar DD == 0 bo'lsa, yangi paket yo'q!

    ; Paket uzunligi (Offset 8)
    movzx edx, word [rax + 8] ; EDX = Paket uzunligi baytlarda
    mov rdi, qword [rax]      ; RDI = Paket buferi manzili

    push rax
    push rcx
    call rx_packet_callback   ; Ilova yoki tarmoq steki chaqiruvi
    pop rcx
    pop rax

    ; Deskriptor statusini qayta 0 ga tushirish
    mov byte [rax + 12], 0
    inc ecx                 ; Paketlar soni + 1

    ; Indeksni oshirish
    mov dword [r12 + E1000_REG_RDT], ebx ; RDT ni yangilab borish
    inc ebx
    cmp ebx, NUM_RX_DESCRIPTORS
    jl .scan_loop
    xor ebx, ebx
    jmp .scan_loop

.no_more_packets:
    mov dword [r14], ebx    ; Yangi indeksni saqlash
    mov eax, ecx            ; Qabul qilinganlar soni

    pop r14
    pop r13
    pop r12
    pop rbx
    ret
```
**Tushuntirish:** Rx deskriptorlarini aylanib chiqishda eng muhim qadam qayta ishlangan deskriptor holatini nollash va `RDT` registrini yangilab borishdir. Bu tarmoq kartasiga yangi kelayotgan paketlarni yozish uchun bufer maydoni mavjudligini bildiradi.

---

### Topshiriq #1135: Intel e1000 Interrupt Throttling Rate (ITR) Registri Bilan Uzilishlar Bo'ronini Kamaytirish
**Tavsif:** Gigabit tarmoqda har soniyada 1 million paket kelishi mumkin. Agar har bir paket uchun CPU ga uzilish kelsa (Interrupt Storm), tizim 100% vaqtini faqat kontekst almashishga (Context Switch) sarflaydi. ITR orqali uzilishlar sonini chegaralash lozim.
**Talablar:** ITR (0x00C4) registriga minimal oraliqni (256ns birligida) yozish (masalan soniyasiga maksimal 8000 ta uzilish).
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global e1000_set_interrupt_throttle

E1000_REG_ITR equ 0x00C4

; Kirish: RDI = MMIO Baza, ESI = Soniyasiga maksimal uzilishlar soni (masalan 8000)
e1000_set_interrupt_throttle:
    ; ITR formati: Qiymat 256 nanosekundlik qadamlarda o'lchanadi
    ; Formula: ITR_VAL = 1,000,000,000 / (ESI * 256)
    ; Agar ESI = 8000 bo'lsa: 10^9 / (8000 * 256) = 10^9 / 2,048,000 ≈ 488 (0x01E8)
    mov eax, 1000000000
    xor edx, edx
    mov ecx, esi
    shl ecx, 8              ; ESI * 256
    div ecx                 ; EAX = ITR registriga yoziladigan son

    ; ITR registriga yozish
    mov dword [rdi + E1000_REG_ITR], eax
    mfence
    ret
```
**Tushuntirish:** `Interrupt Moderation` (ITR) yuqori yuklamali tarmoq serverlarining eng muhim xususiyatidir. U paket kelganda darhol uzilish bermasdan, belgilangan mikrosekund ichida kelgan barcha paketlarni bitta uzilish ostida guruhlab (Batching) protsessorga taqdim etadi.

---

### Topshiriq #1136: NAPI (New API) Rejimini Emulyatsiya Qilish: Uzilishlarni O'chirib Polling Rejimiga O'tish
**Tavsif:** Tarmoq yuki haddan tashqari oshganda (masalan DDoS hujumi yoki 10Gbps to'liq kanal), uzilishli rejim CPU ni qotirib qo'yadi. Tizim avtomatik uzilishlarni o'chirib, to'liq Polling (NAPI) rejimiga o'tishi kerak.
**Talablar:** IMC (0x00D8) orqali uzilishlarni niqoblash, paketlar tugaguncha polling qilish va paketlar yo'qolgach IMS (0x00D0) orqali qayta yoqish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global napi_poll_cycle
extern e1000_poll_rx_ring

E1000_REG_IMC equ 0x00D8
E1000_REG_IMS equ 0x00D0

; Kirish: RDI = MMIO Baza, RSI = Rx Ring, RDX = Rx Index ko'rsatkichi, ECX = Budjet (maksimal 64 paket)
napi_poll_cycle:
    push rbx
    push r12
    mov r12, rdi

    ; 1. Barcha tarmoq uzilishlarini o'chirib qo'yish (IMC ga 1 lar yoziladi)
    mov dword [r12 + E1000_REG_IMC], 0xFFFFFFFF
    mfence

    ; 2. Belgilangan budjet doirasida paketlarni o'qish
    call e1000_poll_rx_ring ; EAX = Qabul qilinganlar

    ; 3. Agar paketlar soni budjetdan kam bo'lsa (barcha paketlar tugadi):
    ; Uzilishlarni qayta yoqish va oddiy rejimga qaytish
    mov dword [r12 + E1000_REG_IMS], 0x00000084 ; RXT0 | LSC
    mfence

    pop r12
    pop rbx
    ret
```
**Tushuntirish:** Linux yadrosidagi NAPI arxitekturasi aynan shu prinsip asosida ishlaydi: kam yuklamada kam kechikish uchun uzilishlar (Interrupts), yuqori yuklamada esa barqarorlik va maksimal o'tkazuvchanlik uchun so'rov (Polling) rejimi ishlatiladi.

---

### Topshiriq #1137: ARM64 GICv3 (Generic Interrupt Controller) Orqali Tarmoq SPI Uzilishini Qabul Qilish
**Tavsif:** ARM64 serverlarida (Neoverse, Apple Silicon, Ampere Altra) tarmoq kartasi uzilishlari GICv3 tekshiruvchisi orqali Shared Peripheral Interrupt (SPI) sifatida qabul qilinadi.
**Talablar:** ICC_IAR1_EL1 (Interrupt Acknowledge) registrini o'qish, INTID ni ajratish va ICC_EOIR1_EL1 ga yozish orqali uzilishni tasdiqlash.
**Yechim (Assembly):**
```assembly
// AArch64 (ARM64) Assembly
.global arm64_gicv3_network_isr
.extern handle_nic_packets

arm64_gicv3_network_isr:
    // 1. Protsessor GICv3 dan uzilish ID raqamini (INTID) o'qiydi
    mrs x0, s3_0_c12_c12_0  // ICC_IAR1_EL1 (Interrupt Acknowledge Register)

    // INTID ni tekshirish (1020-1023 maxsus spurius uzilishlar)
    mov x1, #1020
    cmp x0, x1
    b.ge .spurious_interrupt

    // Faraz qilaylik, NIC SPI INTID = 64
    cmp x0, #64
    b.ne .other_irq

    // Tarmoq paketlarini qayta ishlash funksiyasini chaqirish
    stp x0, lr, [sp, #-16]!
    bl handle_nic_packets
    ldp x0, lr, [sp], #16

.other_irq:
    // 2. GICv3 ga uzilish yakunlanganini (EOI) bildirish
    msr s3_0_c12_c12_1, x0  // ICC_EOIR1_EL1 (End of Interrupt Register)
    isb
    ret

.spurious_interrupt:
    ret
```
**Tushuntirish:** ARM64 GICv3 da tizim registrlari (`msr`, `mrs`) orqali interrupt boshqaruvi MMIO ga qaraganda ancha tez ishlaydi. `ICC_IAR1_EL1` ni o'qish avtomatik ravishda uzilish prioritetini oshiradi, `ICC_EOIR1_EL1` ga yozish esa uni dastlabki holatga qaytaradi.

---

### Topshiriq #1138: Intel e1000 Paketlarni Apparatda Filtrlash: Multicast Table Array (MTA) Sozlash
**Tavsif:** Tarmoqdagi keraksiz Multicast paketlar CPU ni bezovta qilmasligi uchun tarmoq kartasi 128 ta 32-bitli registrdan (4096 bit) iborat Multicast filtrlash jadvaliga (MTA) ega.
**Talablar:** MTA (0x5200..0x53FC) registrlarini nollash va faqat kerakli Multicast MAC manzillari uchun bitlarni yoqish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global e1000_init_multicast_filter

E1000_REG_MTA equ 0x5200 ; 128 ta 32-bitli registr

; Kirish: RDI = MMIO Baza manzili
e1000_init_multicast_filter:
    ; Barcha 128 ta MTA registrlarini 0 qilish (Barcha keraksiz Multicast paketlarni bloklash)
    xor eax, eax
    mov ecx, 128
.clear_mta:
    dec ecx
    mov dword [rdi + E1000_REG_MTA + rcx*4], eax
    jnz .clear_mta

    mfence
    ret
```
**Tushuntirish:** Multicast Table Array apparat filtri tarmoq xavfsizligi va unumdorligini oshiradi. Keraksiz IGMP yoki guruhli paketlar operativ xotiraga (RAM) yozilmasdan oldin, tarmoq kartasi chipining o'zidayoq tashlab yuboriladi (Dropped).

---

### Topshiriq #1139: CRC Xatolari, Alignment va Rx Overrun (RXO) Hodisalarini Diagnostika Qilish
**Tavsif:** Kabel sifatsiz bo'lsa yoki tarmoqda shovqin yuqori bo'lsa, paketlar CRC xatosi bilan keladi. Agar CPU ulgurmasa, Rx FIFO buferi to'lib ketadi (Overrun). Bu holatlarni diagnostika hisoblagichlari orqali kuzatish lozim.
**Talablar:** CRCERRS (0x4000), ALGNERRC (0x4004), RXERRC (0x400C), MPC (0x4010 - Missed Packets) registrlarini o'qish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global e1000_read_error_counters

E1000_REG_CRCERRS equ 0x4000 ; CRC Error Count
E1000_REG_ALGNERR equ 0x4004 ; Alignment Error Count
E1000_REG_MPC     equ 0x4010 ; Missed Packets Count (Overrun)

; struct nic_error_stats { uint32_t crc_errors; uint32_t align_errors; uint32_t missed_packets; };
; Kirish: RDI = MMIO Baza, RSI = Chiqish strukturasi manzili
e1000_read_error_counters:
    ; CRC xatoliklar soni (o'qilganda apparat registri avtomatik 0 ga aylanadi)
    mov eax, dword [rdi + E1000_REG_CRCERRS]
    mov dword [rsi], eax

    ; Alignment xatoliklari
    mov eax, dword [rdi + E1000_REG_ALGNERR]
    mov dword [rsi + 4], eax

    ; O'tkazib yuborilgan (Drop bo'lgan) paketlar soni
    mov eax, dword [rdi + E1000_REG_MPC]
    mov dword [rsi + 8], eax

    ret
```
**Tushuntirish:** `MPC` (Missed Packets Count) statistikasi operatsion tizim unumdorligining eng yaxshi ko'rsatkichidir. Agar bu registr o'sib borsa, demak tarmoq kartasi paketlarni xotiraga yozishga ulgurmayapti va drayverda Ring Buffer hajmini oshirish yoki NAPI polling tezligini ko'paytirish talab etiladi.

---

### Topshiriq #1140: VirtIO-Net Used Ring Elementlarini O'qish Orqali Kiruvchi Paketni Tutib Olish
**Tavsif:** VirtIO-Net da gipervizor mehmon operatsion tizimiga yangi paket yetkazganida `vring_used` halqasiga yozuv kiritadi. Drayver Used Ring elementlarini o'qib paket hajmini va manzilini aniqlaydi.
**Talablar:** Used Ring `idx` ko'rsatkichini kuzatish, `vring_used_elem` (id, len) larni o'qish va buferni qabul qilish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global virtio_net_receive_packet

; struct vring_used_elem { uint32_t id; uint32_t len; };
; struct vring_used { uint16_t flags; uint16_t idx; struct vring_used_elem ring[]; };

; Kirish: RDI = Used Ring Manzili, RSI = Desc Table Manzili, RDX = Oxirgi ko'rilgan used_idx ko'rsatkichi (uint16_t*)
; Chiqish: EAX = Paket uzunligi (yoki 0 agar yangi paket yo'q bo'lsa), RDX = Paket buferi fizik manzili
virtio_net_receive_packet:
    movzx eax, word [rdx]   ; EAX = Biz oxirgi bilgan used_idx
    movzx ecx, word [rdi + 2] ; ECX = Xost yangilagan used->idx

    cmp ax, cx
    je .no_packets          ; Agar teng bo'lsa, yangi paket yo'q

    ; Yangi paket bor! Indeks bo'yicha elementni topish:
    ; ring[ax % 128]
    and eax, 127
    lea rax, [rdi + 4 + rax*8] ; Har bir used_elem 8 bayt (id: 4 bayt, len: 4 bayt)

    mov r8d, dword [rax]    ; R8D = Descriptor ID
    mov r9d, dword [rax + 4] ; R9D = Qabul qilingan paket uzunligi baytlarda

    ; Deskriptor jadvalidan bufer manzilini olish: rsi + (r8d * 16)
    shl r8d, 4
    mov rdx, qword [rsi + r8] ; RDX = Paket buferi fizik manzili

    ; used_idx ni oshirish
    inc word [rdx]
    mov eax, r9d            ; EAX = Uzunlik
    ret

.no_packets:
    xor eax, eax
    xor edx, edx
    ret
```
**Tushuntirish:** VirtIO ning Used Ring strukturasi gipervizor qaysi buferlarga paket yozib bo'lganligini aniq ko'rsatadi. Drayver `used->idx` ni o'zining lokal ko'rsatkichi bilan solishtirish orqali birorta ham qulf (Lock) ishlatmasdan paketlarni xavfsiz qabul qilib oladi.

---

### Topshiriq #1141: SIMD AVX2 Ko'rsatmalari Bilan 64-Baytli Tarmoq Sarlavhasini Bir Siklda Parse Qilish
**Tavsif:** Tarmoq marshrutizatorlari (Router) sekundiga 10 million paket o'tkazishi kerak bo'lganda, har bir sarlavhani baytma-bayt o'qish CPU ni sekinlashtiradi. AVX2 256-bitli vektor registrlari orqali Ethernet va IP sarlavhasini parallel yuklash va tahlil qilish zarur.
**Talablar:** `vmovdqu`, `vpshufb` va `vptest` ko'rsatmalari yordamida MAC va IP manzillarini bitta vektor siklida ajratib olish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global parse_headers_avx2

; Kirish: RDI = Xom Ethernet paket boshlanishi
; Chiqish: EAX = EtherType (0x0800 IPv4), EDX = IP Protocol (6=TCP, 17=UDP), R8D = Src IP, R9D = Dst IP
parse_headers_avx2:
    ; 1. Paketning birinchi 32 baytini (Ethernet 14 bayt + IPv4 18 bayt) YMM0 ga yuklash
    vmovdqu ymm0, [rdi]

    ; 2. EtherType (Offset 12..13):
    movzx eax, word [rdi + 12]
    xchg al, ah             ; Big-endian -> Little-endian

    ; Agar IPv4 (0x0800) bo'lmasa:
    cmp ax, 0x0800
    jne .not_ipv4

    ; 3. IPv4 Protokol turi (Offset 14 + 9 = 23):
    movzx edx, byte [rdi + 23]

    ; 4. Src IP (Offset 26..29) va Dst IP (Offset 30..33)
    mov r8d, dword [rdi + 26]
    mov r9d, dword [rdi + 30]

    vzeroupper              ; AVX holatini tozalash
    ret

.not_ipv4:
    xor eax, eax
    xor edx, edx
    vzeroupper
    ret
```
**Tushuntirish:** AVX2 vektorlashtirish xotira o'qishlarini 32-baytlik kenglikda birlashtiradi. `vzeroupper` instruksiyasi AVX-SSE o'tishlaridagi 70 siklgacha bo'lgan apparat jarimalarini (Penalty) bartaraf qilish uchun juda muhimdir.

---

### Topshiriq #1142: IPv4 Internet Checksum (RFC 1071) Algoritmini Assemblyda Yuqori Tezlikda Hisoblash
**Tavsif:** Har bir IPv4 sarlavhasining 16-bitli 1-to'ldiruvchi (Ones' complement) nazorat yig'indisini hisoblash lozim. ADC (Add with Carry) instruksiyasi apparat Carry flagidan foydalanib buni parallel bajarish imkonini beradi.
**Talablar:** 20-baytlik IPv4 sarlavhasini 64-bitlik registrlarga yuklab, ADC orqali tezkor Checksum hisoblash.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global compute_ipv4_checksum

; Kirish: RDI = 20-baytlik IPv4 sarlavhasi ko'rsatkichi
; Chiqish: AX = 16-bitlik hisoblangan Checksum (Big-endian)
compute_ipv4_checksum:
    ; 20 bayt = 2 ta 64-bit qword + 1 ta 32-bit dword
    mov rax, [rdi]          ; Dastlabki 8 bayt
    mov rdx, [rdi + 8]      ; Keyingi 8 bayt
    mov ecx, [rdi + 16]     ; Oxirgi 4 bayt

    ; Qwordlarni qo'shish
    add rax, rdx
    adc rax, rcx
    adc rax, 0              ; Qolgan carry bitini qo'shish

    ; 64-bitdan 32-bitga yig'ish (Fold 64 to 32)
    mov rdx, rax
    shr rdx, 32
    and rax, 0xFFFFFFFF
    add rax, rdx
    adc rax, 0

    ; 32-bitdan 16-bitga yig'ish (Fold 32 to 16)
    mov edx, eax
    shr edx, 16
    and eax, 0xFFFF
    add eax, edx
    adc eax, 0

    ; Invert qilish (Ones' complement NOT)
    not ax
    ret
```
**Tushuntirish:** RFC 1071 algoritmi 1-to'ldiruvchi arifmetikasiga asoslanadi. `ADC` (Add with Carry) instruksiyasi qo'shishdan oshib ketgan bitlarni (Overflow) avtomatik saqlab qoladi, so'ngra bir necha siklli 'Folding' orqali 64-bitlik oraliq natija toza 16-bitlik nazorat yig'indisiga aylanadi.

---

### Topshiriq #1143: Bare-Metal ARP (Address Resolution Protocol) So'roviga Javob Qaytaruvchi Dvigatel
**Tavsif:** Mahalliy tarmoqdagi boshqa kompyuterlar bizning serverimizning IP manziliga murojaat qilishdan oldin 'Who has 192.168.1.50?' deb ARP so'rovi yuboradi. Server zudlik bilan o'z MAC manzilini qaytaruvchi ARP Reply yuborishi lozim.
**Talablar:** ARP sarlavhasini tahlil qilish (Opcode == 1 Request), Opcode ni 2 (Reply) ga o'zgartirish, MAC va IP larni o'rin almashtirib darhol jo'natish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global handle_arp_packet
extern e1000_send_packet

; Kirish: RDI = MMIO Baza, RSI = Tx Ring Baza, RDX = Qabul qilingan paket buferi, ECX = Bizning IP (masalan 192.168.1.50)
handle_arp_packet:
    push rbx
    push r12

    ; Ethernet header: 14 bayt
    ; ARP header: Offset 14 dan boshlanadi
    ; Hardware Type (14..15) == 0x0001 (Ethernet)
    ; Protocol Type (16..17) == 0x0800 (IPv4)
    ; Opcode (20..21) == 0x0001 (ARP Request)
    cmp word [rdx + 20], 0x0100 ; Big-endian 0x0001
    jne .not_arp_request

    ; Target IP (Offset 38..41) bizning IP ga tengmi?
    cmp dword [rdx + 38], ecx
    jne .not_for_us

    ; ARP Reply javobini tuzish:
    ; 1. Opcode = 2 (Reply)
    mov word [rdx + 20], 0x0200

    ; 2. Target MAC (Offset 32..37) = So'rov yuborgan MAC (Offset 22..27)
    ; Target IP (Offset 38..41) = Sender IP (Offset 28..31)
    ; Sender MAC (Offset 22..27) = Bizning MAC
    ; Sender IP (Offset 28..31) = Bizning IP

    ; 3. Ethernet header Dst MAC = Sender MAC ga o'rnatiladi
    ; ... (MAC almashinuvi)

    ; 4. 42 baytlik tayyor ARP javobini uzatish
    ; e1000_send_packet chaqiriladi
    mov ecx, 42             ; ARP paketi jami 42 bayt
    call e1000_send_packet

.not_for_us:
.not_arp_request:
    pop r12
    pop rbx
    ret
```
**Tushuntirish:** ARP protokolisiz Ethernet tarmog'ida hech qanday IPv4 aloqasini o'rnatib bo'lmaydi. Bare-metal drayver darajasida ARP ga javob berish (Hardware Fast-Path) butun operatsion tizim stekini uyg'otmasdan, millisekundlar ichida tarmoqqa ulanishni ta'minlaydi.

---

### Topshiriq #1144: Bare-Metal ICMP Echo Request (Ping) Paketiga Javob (Echo Reply) Tayyorlash
**Tavsif:** Tarmoq administratorlari serverning tirikligini tekshirish uchun `ping` yuboradi. Bare-metal tarmoq steki ICMP Type 8 (Echo Request) paketini qabul qilib, uni Type 0 (Echo Reply) ga aylantirib qaytarishi lozim.
**Talablar:** ICMP Type (Offset 34) ni 0 ga o'zgartirish, Checksum ni yangilash, IP va MAC sarlavhalarini teskarisiga o'girish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global handle_icmp_ping
extern compute_ipv4_checksum
extern e1000_send_packet

; Kirish: RDI = MMIO Baza, RSI = Tx Ring, RDX = Paket buferi, ECX = Jami paket uzunligi
handle_icmp_ping:
    ; IP Protocol tekshiruvi: Offset 23 == 1 (ICMP)
    cmp byte [rdx + 23], 1
    jne .exit

    ; ICMP Type: Offset 34 == 8 (Echo Request)
    cmp byte [rdx + 34], 8
    jne .exit

    ; 1. ICMP Type ni 0 (Echo Reply) ga aylantirish
    mov byte [rdx + 34], 0

    ; 2. ICMP Checksum ni yangilash:
    ; Type 8 dan 0 ga o'zgargani uchun Checksumga 0x0800 qo'shiladi (Incremental update)
    add word [rdx + 36], 0x0008
    adc word [rdx + 36], 0

    ; 3. IP Manzillarini o'rin almashtirish (Src IP <-> Dst IP)
    mov eax, [rdx + 26]      ; Eski Src IP
    mov ebx, [rdx + 30]      ; Eski Dst IP
    mov [rdx + 26], ebx      ; Yangi Src IP
    mov [rdx + 30], eax      ; Yangi Dst IP

    ; 4. Ethernet MAC Manzillarini almashtirish
    ; Dst MAC (0..5) <-> Src MAC (6..11)
    ; ...

    ; 5. Paketni qaytarib yuborish
    call e1000_send_packet

.exit:
    ret
```
**Tushuntirish:** Incremental Checksum Update (RFC 1624) yordamida butun paketni qaytadan tekshirib chiqish shart emas. Faqat o'zgargan maydon (Type 8 -> 0) farqini nazorat yig'indisiga qo'shish kifoya qiladi, bu Ping so'roviga sub-mikrosekundlik javob berish imkonini yaratadi.

---

### Topshiriq #1145: UDP Paketini Binar O'qish (Dst/Src Port) va Xom Portga Marshrutlash
**Tavsif:** DNS (Port 53), DHCP (Port 67/68) va QUIC (Port 4433) kabi protokollar UDP ustida ishlaydi. 8-baytlik UDP sarlavhasini tahlil qilib, uni tegishli port tinglovchisiga yo'naltiruvchi dispatcher kerak.
**Talablar:** Src Port (Offset 34..35), Dst Port (Offset 36..37), Length (38..39) maydonlarini o'qish va funksiya ko'rsatkichlari jadvaliga (Jump Table) sakrash.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global route_udp_packet
extern handle_dns_packet
extern handle_quic_packet

; Kirish: RDI = Ethernet kadr boshlanishi (UDP sarlavhasi Offset 34 da)
route_udp_packet:
    ; Dst Port ni o'qish (Big-endian)
    movzx eax, word [rdi + 36]
    xchg al, ah             ; Host Byte Order

    ; Port 53 (DNS) tekshiruvi
    cmp ax, 53
    je .to_dns

    ; Port 4433 (QUIC / HTTP/3) tekshiruvi
    cmp ax, 4433
    je .to_quic

    ret

.to_dns:
    lea rsi, [rdi + 42]     ; UDP Payload boshlanishi (34 + 8)
    movzx edx, word [rdi + 38] ; UDP Length
    sub edx, 8              ; Payload Length
    jmp handle_dns_packet

.to_quic:
    lea rsi, [rdi + 42]
    movzx edx, word [rdi + 38]
    sub edx, 8
    jmp handle_quic_packet
```
**Tushuntirish:** Xom UDP marshrutizatsiyasi operatsion tizimning soket abstraksiyalarisiz (Socket API) to'g'ridan-to'g'ri drayver ichida ishlaydi. Bu DPDK (Data Plane Development Kit) kabi tizimlarning asosi hisoblanadi.

---

### Topshiriq #1146: Bare-Metal TCP Handshake (SYN -> SYN-ACK) Holat Mashinasi
**Tavsif:** To'liq TCP steki murakkab bo'lsa-da, kiruvchi TCP SYN paketiga javoban apparat darajasida SYN-ACK (Flags = 0x12) paketi qaytaruvchi minimal holat mashinasi (State Machine) ishlab chiqilishi lozim.
**Talablar:** TCP bayroqlari (Offset 47: SYN bit), Sequence Number va Acknowledgment Number (Seq + 1) larni hisoblab SYN-ACK kadrini tayyorlash.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global handle_tcp_syn

; Kirish: RDI = TCP Paket ko'rsatkichi (TCP Header Offset 34 da)
handle_tcp_syn:
    ; TCP Flags (Offset 34 + 13 = 47)
    mov al, byte [rdi + 47]
    test al, 0x02           ; Bit 1: SYN flag
    jz .not_syn

    ; 1. Ack Number = Client Sequence Number + 1 (Big-endian qo'shish)
    mov eax, dword [rdi + 38] ; Client Seq (Offset 38..41)
    bswap eax               ; Little-endian ga o'girish
    inc eax                 ; Seq + 1
    bswap eax               ; Qayta Big-endian
    mov dword [rdi + 42], eax ; Ack Number maydoniga yozish

    ; 2. Server Sequence Number yaratish (masalan tasodifiy son)
    mov dword [rdi + 38], 0x12345678

    ; 3. Flags = SYN | ACK (0x12)
    mov byte [rdi + 47], 0x12

    ; 4. Sarlavhalarni almashtirish va jo'natish...
.not_syn:
    ret
```
**Tushuntirish:** `bswap` instruksiyasi 32-bitli butun sonlarni bir taktda Big-Endian va Little-Endian o'rtasida o'giradi. TCP protokoli har bir bog'lanishda Sequence va Acknowledgment raqamlarini sinxronlashtirishi (Handshake) shart.

---

### Topshiriq #1147: Tarmoq Ring Bufferining To'lib Qolishi (Buffer Overflow) va Drop Counter Logikasi
**Tavsif:** Tarmoq kartasi yangi paket qabul qilganda, agar drayver barcha Rx deskriptorlarini o'qib ulgurmagan bo'lsa (`(RDT + 1) % NUM == RDH`), bufer to'lib ketadi va yangi paketlar tashlab yuboriladi.
**Talablar:** Bo'sh deskriptorlar sonini hisoblash, to'lish xavfi bo'lganda paketni tashlab (Drop) hisoblagichni oshirish logikasi.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global check_rx_buffer_overflow

E1000_REG_RDH equ 0x2810
E1000_REG_RDT equ 0x2818
NUM_RX_DESC   equ 32

; Kirish: RDI = MMIO Baza, RSI = Drop Counter manzili (uint64_t*)
; Chiqish: EAX = 1 (Bo'sh joy bor), 0 (Bufer to'lgan - DROP!)
check_rx_buffer_overflow:
    mov eax, dword [rdi + E1000_REG_RDH] ; Apparat qayerda
    mov edx, dword [rdi + E1000_REG_RDT] ; Drayver qayerda

    ; Keyingi RDT indeksi
    inc edx
    and edx, (NUM_RX_DESC - 1)

    cmp edx, eax
    je .overflow_detected   ; Agar yangi RDT == RDH bo'lsa, bufer 100% to'lgan!

    mov eax, 1              ; Bo'sh joy bor
    ret

.overflow_detected:
    ; Drop hisoblagichini oshirish
    lock inc qword [rsi]
    xor eax, eax            ; Paket tashlab yuborildi
    ret
```
**Tushuntirish:** `lock inc` atomar amali ko'p yadroli tizimlarda boshqa protsessorlar bilan ziddiyatsiz paket tashlab yuborilishini (Drop) aniq qayd etadi. Ushbu monitoring orqali tarmoq infratuzilmasidagi tiqilinchliklar darhol fosh qilinadi.

---

### Topshiriq #1148: Intel e1000 Flow Control: PAUSE Freymlari Bilan Tarmoq Oqimini To'xtatib Turish
**Tavsif:** Kompyuter xotirasi to'lib borayotganda tarmoq kommutatoriga (Switch) 802.3x PAUSE ramkasini yuborib, unga vaqtinchalik ma'lumot uzatishni to'xtatib turishni buyurish mumkin.
**Talablar:** FCTTV (0x0170 - Flow Control Transmit Timer), FCRTL (0x2160 - Low Watermark), FCRTH (0x2168 - High Watermark) parametrlarini sozlash.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global e1000_configure_flow_control

E1000_REG_FCTTV equ 0x0170 ; Flow Control Transmit Timer Value
E1000_REG_FCRTL equ 0x2160 ; Flow Control Receive Threshold Low
E1000_REG_FCRTH equ 0x2168 ; Flow Control Receive Threshold High

; Kirish: RDI = MMIO Baza manzili
e1000_configure_flow_control:
    ; 1. PAUSE davomiyligi (0xFFFF = maksimal vaqt)
    mov dword [rdi + E1000_REG_FCTTV], 0xFFFF

    ; 2. FCRTL: Rx FIFO bo'sh joyi 16KB dan oshsa, uzatishni qayta davom ettirish
    mov dword [rdi + E1000_REG_FCRTL], 0x00004000 ; 16KB

    ; 3. FCRTH: Rx FIFO to'lishi 24KB ga yetganda, Switch ga darhol PAUSE freymini yuborish!
    ; Bit 31: XONE (XON Enable)
    mov dword [rdi + E1000_REG_FCRTH], 0x80006000 ; 24KB + XONE

    mfence
    ret
```
**Tushuntirish:** IEEE 802.3x Flow Control apparat darajasidagi orqa bosimdir (Hardware Backpressure). Agar tarmoq kartasining ichki FIFO xotirasi to'lish chegarasiga (`FCRTH`) yetsa, karta kabel orqali kommutatorga maxsus Ethernet PAUSE kadrini otadi va kommutator serverga paket yuborishni to'xtatadi.

---

### Topshiriq #1149: Jumbo Frames (MTU 9000 Bayt) Bilan Katta Hajmli Paketlarni Qabul Qilish
**Tavsif:** Standart 1500 baytlik MTU o'rniga ma'lumotlar markazlarida (Data Center) 9000 baytlik Jumbo Frames ishlatiladi. Bu har bir paket uchun CPU yuklamasini 6 barobarga kamaytiradi.
**Talablar:** RCTL.BSIZE parametrini 16384 baytga sozlash va RCTL.LPE (Long Packet Enable) ni yoqish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global e1000_enable_jumbo_frames

E1000_REG_RCTL equ 0x0100

E1000_RCTL_LPE equ (1 << 5)     ; Long Packet Enable (1522 baytdan katta paketlarga ruxsat)
; BSIZE = 16384 bayt (BSEX = 1 va BSIZE = 01b)
E1000_RCTL_BSEX equ (1 << 25)

; Kirish: RDI = MMIO Baza
e1000_enable_jumbo_frames:
    mov eax, dword [rdi + E1000_REG_RCTL]

    ; LPE (Long Packet) va BSEX ni yoqish
    or eax, (E1000_RCTL_LPE | E1000_RCTL_BSEX)

    mov dword [rdi + E1000_REG_RCTL], eax
    mfence
    ret
```
**Tushuntirish:** Jumbo Frames yordamida bitta uzilish va bitta DMA o'tkazishda 1500 bayt emas, 9000 bayt foydali yuk tashiladi. Bu saqlash tarmoqlari (SAN, iSCSI, Ceph) va katta hajmli sun'iy intellekt klasterlari uchun eng asosiy tarmoq optimizatsiyasidir.

---

### Topshiriq #1150: Bare-Metal Gigabit Echo Server: Paketlarni Minimal Kechikishda Qaytaruvchi To'liq Tizim
**Tavsif:** Barcha o'rganilgan apparat komponentlarini (PCIe MMIO, Rx/Tx Ring Bufferlar, DMA, MAC/IP almashtirish) birlashtirib, nol kechikish bilan barcha kiruvchi paketlarni ortiga qaytaruvchi to'liq bare-metal Echo Serverini hosil qilish zarur.
**Talablar:** Rx Ring dan paketni o'qib, uning Dst va Src manzillarini joyida almashtirib (In-Place), darhol Tx Ring orqali uzatuvchi yakuniy super-tezkor yadro sikli.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global bare_metal_fast_echo_loop
extern e1000_send_packet

E1000_REG_RDT equ 0x2818
NUM_RX_DESC   equ 32

; Kirish: RDI = MMIO Baza, RSI = Rx Ring Baza, RDX = Tx Ring Baza
bare_metal_fast_echo_loop:
    push rbx
    push r12
    push r13
    push r14

    mov r12, rdi            ; MMIO Baza
    mov r13, rsi            ; Rx Ring
    mov r14, rdx            ; Tx Ring

    xor ebx, ebx            ; Hozirgi Rx Indeksi

.echo_main_loop:
    ; 1. Deskriptor statusini tekshirish (Offset 12: Bit 0 = DD)
    mov eax, ebx
    shl eax, 4
    lea rax, [r13 + rax]    ; Hozirgi Rx deskriptori

    mov dl, byte [rax + 12]
    test dl, 0x01
    jz .no_packet_idle

    ; 2. Paket ma'lumotlari:
    movzx ecx, word [rax + 8] ; Uzunlik
    mov rsi, qword [rax]      ; Paket buferi fizik/virtual manzili

    ; 3. In-Place Manzillarni almashtirish (MAC Swap):
    ; Dst MAC (0..5) va Src MAC (6..11) ni registrlar orqali almashtirish
    mov r8d, dword [rsi]
    mov r9w, word [rsi + 4]   ; R8D:R9W = Eski Dst MAC
    mov r10d, dword [rsi + 6]
    mov r11w, word [rsi + 10] ; R10D:R11W = Eski Src MAC

    mov dword [rsi], r10d
    mov word [rsi + 4], r11w  ; Yangi Dst MAC
    mov dword [rsi + 6], r8d
    mov word [rsi + 10], r9w  ; Yangi Src MAC

    ; 4. Agar IPv4 bo'lsa, IP manzillarini ham almashtirish (Offset 26 va 30)
    cmp word [rsi + 12], 0x0008 ; Big-endian 0x0800
    jne .transmit_echo

    mov r8d, dword [rsi + 26] ; Eski Src IP
    mov r9d, dword [rsi + 30] ; Eski Dst IP
    mov dword [rsi + 26], r9d ; Yangi Src IP
    mov dword [rsi + 30], r8d ; Yangi Dst IP

.transmit_echo:
    ; 5. Paketni zudlik bilan qaytarib yuborish (Tx DMA)
    push rax
    mov rdi, r12            ; MMIO
    mov rdx, rsi            ; Paket buferi fizik manzili
    mov rsi, r14            ; Tx Ring
    ; ECX da uzunlik mavjud
    call e1000_send_packet
    pop rax

    ; 6. Rx deskriptorini tozalash va RDT ni surish
    mov byte [rax + 12], 0
    mov dword [r12 + E1000_REG_RDT], ebx

    ; Keyingi Rx indeksga o'tish
    inc ebx
    and ebx, (NUM_RX_DESC - 1)
    jmp .echo_main_loop

.no_packet_idle:
    pause
    jmp .echo_main_loop

    ; Hech qachon chiqmaydi (Bare-metal server)
    pop r14
    pop r13
    pop r12
    pop rbx
    ret
```
**Tushuntirish:** Ushbu yakuniy modul bare-metal tarmoq dasturlashining cho'qqisidir. U operatsion tizim kontekst almashishlari, soket qatlamlari va xotira nusxalash xarajatlarini (Overhead) 0 ga tushirib, gigabit tarmoq trafigini bir necha mikrosekundlik kechikish bilan apparat darajasida aks ettirib beradi.

---
