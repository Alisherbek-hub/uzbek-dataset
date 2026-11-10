# Assembly (x86_64 va ARM64): Mukammal Ensiklopediya va Fundamental Qo'llanma
**Loyiha:** Khorazmiy AI — O'zbek Tilidagi Katta Dasturlash Dataseti  
**Muallif:** Khorazmiy AI Assembly / Low-Level Systems Specialist  
**Qamrovi:** Protsessorlar arxitekturasi (CISC vs RISC), x86_64 va ARM64 registrlari, Xotira xaritalash, Stek freymi, Calling Conventions (ABI), Tizim chaqiruvlari (Syscalls), SIMD va Vektorli hisoblash (SSE, AVX, Neon), C va Assembly integratsiyasi, Makroslar va modulli dasturlash, Reverse Engineering (Teskari muhandislik), Kiberxavfsizlik (Shellcoding, ROP zanjirlari, PAC/BTI himoyalari), Bare-Metal va Operatsion Tizimlar yadrosi.

---

## Mundarija
1. [Kirish va Quyi Darajadagi Dasturlash Falsafasi](#1-kirish-va-quyi-darajadagi-dasturlash-falsafasi)
2. [Arxitekturalar Qiyosiy Tahlili: CISC (x86_64) vs RISC (ARM64)](#2-arxitekturalar-qiyosiy-tahlili-cisc-x86_64-vs-risc-arm64)
3. [Protsessor Registrlari Tizimi va Flaglar Anatomiyasi](#3-protsessor-registrlari-tizimi-va-flaglar-anatomiyasi)
4. [Xotira Modeli, Stek Xotirasi va Calling Conventions (ABI)](#4-xotira-modeli-stek-xotirasi-va-calling-conventions-abi)
5. [Arifmetik, Mantiqiy va Boshqaruv Oqimi Buyruqlari](#5-arifmetik-mantiqiy-va-boshqaruv-oqimi-buyruqlari)
6. [Tizim Chaqiruvlari (Syscalls) va Yadro Bilan Aloqa](#6-tizim-chaqiruvlari-syscalls-va-yadro-bilan-aloqa)
7. [SIMD va Parallel Vektorli Hisoblash: SSE, AVX va Neon](#7-simd-va-parallel-vektorli-hisoblash-sse-avx-va-neon)
8. [C Dasturlash Tili va Assembly Integratsiyasi](#8-c-dasturlash-tili-va-assembly-integratsiyasi)
9. [Reverse Engineering (Teskari Muhandislik) Asoslari](#9-reverse-engineering-teskari-muhandislik-asoslari)
10. [Kiberxavfsizlik, Zaifliklar va ROP (Return-Oriented Programming)](#10-kiberxavfsizlik-zaifliklar-va-rop-return-oriented-programming)
11. [Bare-Metal, Bootloader va Operatsion Tizim Yadrosi](#11-bare-metal-bootloader-va-operatsion-tizim-yadrosi)
12. [Xulosa va Assembly Muhandisining Oltin Qoidalari](#12-xulosa-va-assembly-muhandisining-oltin-qoidalari)

---

## 1. Kirish va Quyi Darajadagi Dasturlash Falsafasi

Assembly (Assembler tili) — inson aqli va kremniy chiplari (protsessor tranzistorlari) o'rtasidagi eng to'g'ridan-to'g'ri, eng samimiy va shaffof aloqa vositasidir. Python, Java, JavaScript yoki Go kabi yuqori darajadagi tillar dasturchini operatsion tizim va protsessor apparaturasidan uzoqlashtiruvchi abstraksiya qatlamlarini (Garbage Collector, Virtual Machine, Runtime) taqdim etsa, Assembly tili protsessor registrlarini, kesh qatlamlarini (L1, L2, L3) va xotira manzillarini to'g'ridan-to'g'ri boshqarish imkonini beradi.

Mashina kodi — protsessor tushunadigan yagona narsa bo'lib, u binar baytlar (masalan, `0x90` yoki `0x48 0x31 0xC0`) ketma-ketligidan iborat. Assembly esa ushbu sonli opkodlarga (opcode) inson o'qiy oladigan mnemonikalarni (`nop` yoki `xor rax, rax`) biriktiradi.

### Nega Bugungi Kunda Assembly O'rganish Shart?
- **Kiberxavfsizlik va Ekspluatatsiya:** Xakerlar va xavfsizlik mutaxassislari zaifliklarni (Buffer Overflow, ROP, Heap corruption) manba kodi darajasida emas, balki xotiradagi binar assembly darajasida tahlil qiladilar.
- **Teskari Muhandislik (Reverse Engineering):** Manba kodi (source code) mavjud bo'lmagan zararli dasturlarni (Malware analysis) yoki yopiq drayverlarni dekompilyatsiya qilishning yagona yo'li assembly tilini bilishdir.
- **Kritik Tezlik va SIMD:** Yuqori unumdorlik talab qiluvchi sohalar (3D grafika, kompyuter ko'rishi, sun'iy intellekt neyron tarmoqlari tensori, audio/video enkoderlar) AVX-512 va ARM Neon ko'rsatmalari orqali to'g'ridan-to'g'ri yoziladi.
- **Bare-Metal va Operatsion Tizimlar:** Bootloader, protsessor uzilishlari drayveri (Interrupt Handlers), kontekst almashinishi (Context Switch) va sahifalash (Paging) C tilida to'liq yozilishi mumkin emas — ular qat'iy ravishda assemblyda bajariladi.

---

## 2. Arxitekturalar Qiyosiy Tahlili: CISC (x86_64) vs RISC (ARM64)

Zamonaviy hisoblash olamida ikki buyuk arxitektura falsafasi hukmronlik qiladi:

```
┌────────────────────────────────────────────────────────┬────────────────────────────────────────────────────────┐
│             x86_64 (AMD64 / Intel 64)                 │                    ARM64 (AArch64)                     │
├────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
│ Falsafasi: CISC (Complex Instruction Set Computer)    │ Falsafasi: RISC (Reduced Instruction Set Computer)     │
│ Buyruqlar uzunligi: O'zgaruvchan (1 dan 15 baytgacha) │ Buyruqlar uzunligi: Qat'iy bir xil (4 bayt / 32 bit)   │
│ Registrlar soni: 16 ta umumiy registr (RAX..R15)      │ Registrlar soni: 31 ta umumiy registr (X0..X30) + SP/XZR│
│ Xotira modeli: Register-Memory (add [rax], rbx mumkin)│ Xotira modeli: Qat'iy Load-Store (faqat LDR/STR)      │
│ Quvvat sarfi: Yuqori, kuchli sovutish talab qiladi    │ Quvvat sarfi: Juda kam, mobil va energiya tejamkor     │
│ Asosiy sohasi: Serverlar, shaxsiy kompyuterlar, super-│ Asosiy sohasi: Smartfonlar, Apple Silicon (M1/M2/M3), │
│ kompyuterlar, og'ir hisoblash infratuzilmalari        │ AWS Graviton, serverlar va IoT qurilmalari            │
└────────────────────────────────────────────────────────┴────────────────────────────────────────────────────────┘
```

### Muhim Farq: Load-Store Falsafasi
x86_64 arxitekturasida bitta buyruqning o'zidayoq RAM dagi qiymatni registrga qo'shish mumkin:
```assembly
add [rax + 8], rbx    ; x86_64: xotiradagi qiymat o'qiladi, rbx qo'shiladi va yana xotiraga yoziladi
```
ARM64 arxitekturasida bu qat'iyan taqiqlangan! Xotira bilan faqat `ldr` (load) va `str` (store) orqali ishlanadi:
```assembly
ldr x2, [x0, #8]      // ARM64: avval xotiradan x2 registriga olinadi
add x2, x2, x1        // protsessor ichida hisoblanadi
str x2, [x0, #8]      // natija xotiraga qaytarib yoziladi
```

---

## 3. Protsessor Registrlari Tizimi va Flaglar Anatomiyasi

### x86_64 Registrlari Ierarxiyasi
x86_64 dagi barcha registrlar orqaga moslik (backward compatibility) tamoyiliga ega:
- `RAX` (64-bit) ──> `EAX` (32-bit) ──> `AX` (16-bit) ──> `AH` (yuqori 8-bit), `AL` (quyi 8-bit)
- `RBX` (64) ──> `EBX` (32) ──> `BX` (16) ──> `BH` / `BL`
- `RCX` (64) ──> `ECX` (32) ──> `CX` (16) ──> `CH` / `CL`
- `RDX` (64) ──> `EDX` (32) ──> `DX` (16) ──> `DH` / `DL`
- `RSI`, `RDI`, `RBP`, `RSP`
- `R8` dan `R15` gacha: `R8` (64), `R8D` (32), `R8W` (16), `R8B` (8)

### ARM64 Registrlari Ierarxiyasi
- `X0` - `X30`: 64-bitli umumiy maqsadli registrlar.
- `W0` - `W30`: Mos 32-bitli quyi registrlar.
- `XZR` / `WZR`: Doimiy nol registri (Zero Register). Unga yozilgan qiymat yo'qoladi, o'qilsa doim 0 beradi.
- `SP`: Stack Pointer.
- `PC`: Program Counter (instruksiya manzili, to'g'ridan-to'g'ri yozib bo'lmaydi).
- `X30` (LR): Link Register — `bl` orqali chaqirilgan funksiyadan qaytish manzilini saqlaydi.
- `X29` (FP): Frame Pointer — Stek freymining asosi.

### Bayroqlar (Flags / NZCV)
Har bir arifmetik yoki mantiqiy amaldan so'ng holat bayroqlari yangilanadi:
- **ZF (Zero Flag) / Z:** Natija 0 bo'lsa 1 bo'ladi.
- **SF (Sign Flag) / N (Negative):** Natija manfiy (eng yuqori bit 1) bo'lsa 1 bo'ladi.
- **CF (Carry Flag) / C:** Belgisiz (unsigned) sonlarda ko'chirish yoki qarz olish yuz berganda 1 bo'ladi.
- **OF (Overflow Flag) / V:** Belgili (signed) sonlarda to'lib ketish sodir bo'lganda 1 bo'ladi.

---

## 4. Xotira Modeli, Stek Xotirasi va Calling Conventions (ABI)

Jarayonning virtual xotira xaritasi quyidagi asosiy bo'limlarga bo'linadi:
1. **.text bo'limi:** Mashina kodlari (faqat o'qish va bajarish: RX).
2. **.rodata bo'limi:** O'zgarmas ma'lumotlar, string konstantalar (faqat o'qish: R).
3. **.data bo'limi:** Boshlang'ich qiymatga ega global va statik o'zgaruvchilar (RW).
4. **.bss bo'limi:** Boshlang'ich qiymatsiz (nol bilan to'ldiriladigan) o'zgaruvchilar (RW).
5. **Heap (Xip):** Dinamik ajratiladigan xotira (`brk`, `mmap`, `malloc`), yuqori manzillarga qarab o'sadi.
6. **Stack (Stek):** Mahalliy o'zgaruvchilar va qaytish manzillari, yuqori manzillardan pastga (0x7FFFFFFF... dan 0 ga qarab) pasayib boradi.

### Calling Conventions (Funksiya Chaqiruv Standartlari)
Har bir tizim funksiyaga argumentlarni uzatish bo'yicha qat'iy ABI ga ega:

#### Linux System V AMD64 ABI (x86_64)
- **Argumentlar registrlari:**
  1. `RDI`, 2. `RSI`, 3. `RDX`, 4. `RCX`, 5. `R8`, 6. `R9`. Qo'shimcha argumentlar stekka push qilinadi.
- **Qaytuvchi qiymat:** `RAX` (agar 128-bit bo'lsa `RDX:RAX`).
- **Callee-saved registrlar (funksiya o'zgartirmasligi shart):** `RBX`, `RSP`, `RBP`, `R12`, `R13`, `R14`, `R15`.
- **Caller-saved registrlar (chaqiruvchi o'zi saqlashi shart):** `RAX`, `RCX`, `RDX`, `RSI`, `RDI`, `R8`..`R11`.
- **Red Zone:** Stek ko'rsatkichi `RSP` ostidagi 128 baytlik xavfsiz zona. Signal kelmagunicha `sub rsp` qilmasdan ham vaqtinchalik foydalanish mumkin.
- **Stack Alignment:** Tashqi funksiya (`call`) chaqirilishidan oldin `RSP` 16 baytga karrali bo'lishi shart (`RSP % 16 == 0`).

#### ARM64 AAPCS (ARM Architecture Procedure Call Standard)
- **Argumentlar:** `X0` dan `X7` gacha bo'lgan registrlar orqali uzatiladi.
- **Qaytuvchi qiymat:** `X0` (yoki `X0:X1`).
- **Callee-saved registrlar:** `X19` dan `X28` gacha va `X29` (FP).
- **Caller-saved registrlar:** `X9` dan `X15` gacha.

---

## 5. Arifmetik, Mantiqiy va Boshqaruv Oqimi Buyruqlari

### x86_64 Buyruqlari
- **Harakat:** `mov`, `movzx` (nol bilan kengaytirish), `movsx` (belgi bilan kengaytirish), `lea` (manzil hisoblash).
- **Arifmetika:** `add`, `sub`, `imul`, `idiv` (`rdx:rax` juftligini bo'ladi), `inc`, `dec`, `neg`.
- **Mantiq:** `and`, `or`, `xor`, `not`, `shl`, `shr`, `sar` (arifmetik siljitish), `rol`, `ror`.
- **Shartli sakrashlar:** `cmp a, b` yoki `test a, b` dan so'ng:
  - `je` / `jz` (teng), `jne` / `jnz` (teng emas).
  - Belgisiz: `ja` (katta), `jb` (kichik), `jae`, `jbe`.
  - Belgili: `jg` (katta), `jl` (kichik), `jge`, `jle`.

### ARM64 Buyruqlari
- **Harakat:** `mov`, `mvn`, `ldr`, `str`, `ldp` (juftlikni o'qish), `stp` (juftlikni yozish).
- **Arifmetika:** `add`, `sub`, `mul`, `sdiv`, `udiv`, `madd` ($a = b 	imes c + d$), `msub`.
- **Filialsiz shart:** `csel` (Conditional Select), `cset` (shartga qarab 1 yoki 0 o'rnatish):
```assembly
cmp w0, w1
csel w0, w0, w1, gt   // agar w0 > w1 bo'lsa w0 qoladi, aks holda w1 tanlanadi
```
- **Tarmoqlanish:** `b` (sakrash), `bl` (chaqirish, LR ga manzil yoziladi), `ret` (LR bo'yicha qaytish), `cbz` / `cbnz` (agar 0 bo'lsa sakrash).

---

## 6. Tizim Chaqiruvlari (Syscalls) va Yadro Bilan Aloqa

Foydalanuvchi rejimidagi (Ring 3 / EL0) ilova fayl ochish, ekranga yozish yoki tarmoqqa paket jo'natish uchun imtiyozli rejimdagi (Ring 0 / EL1) Operatsion Tizim yadrosiga murojaat qilishi shart. Bu jarayon tizim chaqiruvi (Syscall) orqali amalga oshiriladi.

```
┌─────────────────────────────────┬─────────────────────────────────┐
│     Linux x86_64 Syscalls       │       Linux ARM64 Syscalls      │
├─────────────────────────────────┼─────────────────────────────────┤
│ Buyruq: syscall                 │ Buyruq: svc #0                  │
│ Syscall raqami registri: RAX    │ Syscall raqami registri: X8     │
│ Argumentlar: RDI, RSI, RDX,     │ Argumentlar: X0, X1, X2,        │
│              R10, R8, R9        │              X3, X4, X5         │
│ Qaytuvchi natija: RAX           │ Qaytuvchi natija: X0            │
│ Syscall raqamlari:              │ Syscall raqamlari:              │
│   sys_read: 0                   │   sys_read: 63                  │
│   sys_write: 1                  │   sys_write: 64                 │
│   sys_open: 2                   │   sys_openat: 56                │
│   sys_close: 3                  │   sys_close: 57                 │
│   sys_mmap: 9                   │   sys_mmap: 222                 │
│   sys_exit: 60                  │   sys_exit: 93                  │
└─────────────────────────────────┴─────────────────────────────────┘
```

---

## 7. SIMD va Parallel Vektorli Hisoblash: SSE, AVX va Neon

Oddiy buyruqlar SISD (Single Instruction, Single Data) rejimida bitta skalyar son ustida ishlasa, SIMD (Single Instruction, Multiple Data) bitta protsessor taktida birdaniga 4, 8 yoki 16 ta sonni parallel ravishda hisoblaydi.

### Rivojlanish Bosqichlari:
1. **MMX:** 64-bit registrlar (eskirgan).
2. **SSE / SSE2 / SSE4.2:** 128-bit `XMM0` - `XMM15` registrlari (4 ta 32-bit float yoki 2 ta 64-bit double).
3. **AVX / AVX2:** 256-bit `YMM0` - `YMM15` registrlari (8 ta float). 3 ta operandli sintaksis (`vaddps ymm0, ymm1, ymm2`).
4. **AVX-512:** 512-bit `ZMM0` - `ZMM31` registrlari (16 ta 32-bit float).
5. **ARM Neon:** 128-bit `V0` - `V31` (yoki `Q0` - `Q31`) registrlari.

---

## 8. C Dasturlash Tili va Assembly Integratsiyasi

Zamonaviy dasturiy ta'minot arxitekturasida butun loyihani faqat assemblyda yozish amaliy emas. Eng to'g'ri yondashuv — asosiy biznes-mantiqni C/C++ da yozib, eng muhim, kritik sikllarni va apparat bilan aloqa qismlarini alohida `.asm` modullarida realizatsiya qilish va ularni bog'lashdir (linking).

### C dan Assembly Funksiyasini Chaqirish Qadamlari:
1. **Assembly kodi (`fast_math.asm`):**
```assembly
section .text
global fast_dot_product
fast_dot_product:
    ; rdi = float* a, rsi = float* b, rdx = int n
    xorps xmm0, xmm0
    ; ... vektorli hisoblash ...
    ret
```
2. **Kompilyatsiya va Bog'lash:**
```bash
nasm -f elf64 fast_math.asm -o fast_math.o
gcc -O3 main.c fast_math.o -o application
```

---

## 9. Reverse Engineering (Teskari Muhandislik) Asoslari

Reverse Engineering — bu binar faylning ichki arxitekturasi, ishlash mexanizmi va algoritmlarini uning assembler kodini tahlil qilish orqali o'rganish san'atidir.

### Dasturchi va Tahlilchining Asosiy Qurollari:
- `objdump -d -M intel binary`: Mashina kodini Intel sintaksisidagi assemblyga aylantirish.
- `readelf -h -l -S binary`: ELF sarlavhalari, segmentlari va bo'limlarini ko'rish.
- `nm` va `strings`: Binar ichidagi eksport qilingan simvollar va ochiq matnlarni topish.
- `strace` va `ltrace`: Dastur chaqirayotgan tizim chaqiruvlari (syscalls) va dinamik kutubxona chaqiruvlarini jonli kuzatish.
- `GDB` (GEF / Pwndbg plaginlari bilan): Dinamik disk raskadrovka, xotira va registrlarni qadamma-qadam tekshirish.
- `Ghidra` (NSA) va `IDA Pro`: Binar kodni dekompilyatsiya qilib, C ga o'xshash soxta kod (pseudocode) hosil qilish.

---

## 10. Kiberxavfsizlik, Zaifliklar va ROP (Return-Oriented Programming)

Xotira xavfsizligi buzilishlari (Memory Corruption) binar xavfsizlikning fundamental muammosidir.

### Asosiy Xuruj Texnikalari:
1. **Stack Buffer Overflow:** Chegara tekshirilmagan kiritish (`gets`, `strcpy`) natijasida stekdagi mahalliy bufer toshib, saqlangan Frame Pointer (`RBP`) va Qaytish Manzilini (`Return Address`) qayta yozadi.
2. **Shellcoding:** Dastur xotirasiga o'zboshimchalik bilan mashina kodlarini (odatda `sys_execve("/bin/sh")`) joylashtirib, ijroni unga yo'naltirish.
3. **ROP (Return-Oriented Programming):** DEP/NX (ijro taqiqlangan stek) sharoitida yangi kod kiritmasdan, binary yoki `libc` dagi mavjud `ret` bilan tugovchi ko'rsatmalar parchalarini ('gadget'larni) zanjir qilib ulab, tizim ustidan to'liq nazorat o'rnatish.

### Apparat va Tizim Himoyalari:
- **DEP / NX (Data Execution Prevention):** Stek va xip xotiralarida kod bajarilishini apparat darajasida taqiqlash.
- **ASLR (Address Space Layout Randomization):** Stek, Heap va dinamik kutubxonalar manzillarini har bir ishga tushishda tasodifiy (random) joylashtirish.
- **Stack Canaries (SSP):** Stek freymi oxiriga maxfiy nazorat qiymatini (canary) qo'yish va funksiyadan chiqishda uning yaxlitligini tekshirish.
- **ARM64 PAC (Pointer Authentication):** Qaytish manzillarini apparat darajasida kriptografik imzo bilan himoyalash (`paciasp`, `autiasp`).

---

## 11. Bare-Metal, Bootloader va Operatsion Tizim Yadrosi

Bare-Metal dasturlash — hech qanday operatsion tizim, kutubxona yoki drayverlar bo'lmagan "yalang'och" protsessor ustida to'g'ridan-to'g'ri kod yozishdir.

### x86 Kompyuterining Ishga Tushish Zanjiri:
1. **Reset Vector (0xFFFFFFF0):** Protsessor quvvat olganda 16-bitli Real Mode rejimida ish boshlaydi.
2. **BIOS / UEFI:** Apparaturani (RAM, PCI qurilmalari) tekshiradi (POST) va birinchi saqlovchi qurilmaning 1-sektorini (512 bayt) `0x7C00` manziliga yuklaydi.
3. **MBR Yuklovchi (Bootloader):** Oxirgi ikki bayti `0xAA55` bo'lgan ushbu 512 baytli kod operatsion tizim yadrosini xotiraga yuklashga tayyorlaydi.
4. **Protected Mode (32-bit):** GDT (Global Descriptor Table) o'rnatilib, `CR0.PE = 1` qilinadi.
5. **Long Mode (64-bit):** Sahifalar jadvali (PML4) yaratilib `CR3` ga yuklanadi, `CR4.PAE = 1`, `EFER.LME = 1` va `CR0.PG = 1` qilinib to'liq 64-bitli dunyoga qadam qo'yiladi.

---

## 12. Xulosa va Assembly Muhandisining Oltin Qoidalari

1. **Registrlarni Qadrlang:** Registrlar — xotira ierarxiyasidagi eng tezkor resursdir. RAM ga har bir murojaat kesh orqali yuzlab takt yo'qotishga sabab bo'lishi mumkin.
2. **ABI ga Qat'iy Amal Qiling:** Callee-saved registrlarni saqlamaslik yoki stekni 16-baytga tekislamaslik tushunarsiz va qiyin topiladigan qulashlarga (crash) olib keladi.
3. **Shartli Tarmoqlanishdan Mumkin Qadar Qoching:** Protsessor filial bashoratchisi (Branch Predictor) adashganda o'nlab taktlar behuda sarflanadi. Shartli tanlash (`cmov`, `csel`) buyruqlaridan foydalaning.
4. **Xavfsizlikni Unutmang:** Hech qachon foydalanuvchi ma'lumotlariga ishonmang. Har bir bufer hajmini qat'iy tekshiring va zamonaviy himoya mexanizmlari (Canary, ASLR, PAC) ishlash prinsiplarini yodda tuting.

Ushbu ensiklopediya va unga biriktirilgan 20 ta mavzulashtirilgan modul (1000 ta amaliy topshiriq) o'zbek tilida quyi darajadagi dasturlash, kiberxavfsizlik va tizim muhandisligi bo'yicha eng mukammal va professional qo'llanma bo'lib xizmat qiladi.
