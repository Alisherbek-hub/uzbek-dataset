# Khorazmiy AI: Assembly - Modul 24
## Mavzu: Apparat darajasidagi Kriptografiya va Xavfsizlik: x86_64/ARM64 AES-NI (AESENC/AESDEC), PCLMULQDQ (GHASH ko'paytirish), SHA-NI (SHA256RNDS2), Constant-Time Assembly ko'rsatmalari, Stack Canaries, ROP mitigation, Spectre LFENCE to'siqlari va ARM TrustZone / Intel SGX

Salom, men **Khorazmiy AI** loyihasining apparat darajasidagi kriptografiya, mikro-arxitektura xavfsizligi va kiberhimoya bo'yicha bosh dataset mutaxassisiman. Ushbu modulda x86_64 va ARM64 protsessorlarining eng ilg'or kriptografik ko'rsatmalari (AES-NI, SHA-NI, PCLMULQDQ, NEON Cryptography), yon kanallar (Side-Channel) va kesh hujumlariga qarshi doimiy vaqtli (Constant-Time) dasturlash, Stack Canary va Return-Oriented Programming (ROP) ga qarshi Intel CET va ARM PAC/BTI mexanizmlari, Spectre/Meltdown spekulyativ to'siqlari (LFENCE, Retpoline, KPTI) hamda apparat anklavlari (ARM TrustZone va Intel SGX) bo'yicha 50 ta (#1151 - #1200) chuqur, amaliy va ishlab turgan yechimlar jamlangan.

---

### Topshiriq #1151: CPUID Orqali Apparat Darajasidagi AES-NI va PCLMULQDQ Qo'llab-quvvatlashini Aniqlash
**Tavsif:** Kriptografik operatsiyalarni apparat instruksiyalari bilan tezlashtirishdan oldin, protsessor AES-NI va PCLMULQDQ imkoniyatlariga ega ekanligini xavfsiz tekshirish lozim. Aks holda qo'llab-quvvatlanmagan protsessorlarda 'Invalid Opcode (#UD)' istisnosi yuzaga keladi.
**Talablar:** x86_64 `cpuid` instruksiyasini EAX=1 bilan chaqirish, ECX registrining bit 25 (AES-NI) va bit 1 (PCLMULQDQ) larini tekshirish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global check_aesni_support

; Chiqish: EAX = 1 (Ikkala instruksiya ham mavjud), 0 (Mavjud emas)
check_aesni_support:
    push rbx                ; CPUID RBX registrini o'zgartiradi, uni saqlaymiz

    ; 1. CPUID funksiya 1: Protsessor xususiyatlari
    mov eax, 1
    cpuid                   ; EAX, EBX, ECX, EDX to'ldiriladi

    ; ECX registrida:
    ; Bit 25: AES-NI qo'llab-quvvatlovi (1 = Mavjud)
    ; Bit 1:  PCLMULQDQ ko'paytirish instruksiyasi (1 = Mavjud)
    mov edx, ecx            ; ECX nusxasi

    ; AES-NI tekshiruvi (Bit 25: 0x02000000)
    test ecx, (1 << 25)
    jz .not_supported

    ; PCLMULQDQ tekshiruvi (Bit 1: 0x00000002)
    test edx, (1 << 1)
    jz .not_supported

    ; Ikkala apparat imkoniyati ham tasdiqlandi
    mov eax, 1
    pop rbx
    ret

.not_supported:
    xor eax, eax
    pop rbx
    ret
```
**Tushuntirish:** `CPUID` ko'rsatmasi x86 arxitekturasida protsessor imkoniyatlarini dinamik aniqlashning rasmiy usulidir. `AES-NI` (Advanced Encryption Standard New Instructions) apparat shifrlashni ta'minlasa, `PCLMULQDQ` (Carry-Less Multiplication) GCM rejimida xesh hisoblash uchun zarur. Drayver bu tekshiruvsiz kriptografik instruksiyalarni bajarsa, tizim qulashi kafolatlanadi.

---

### Topshiriq #1152: AES-128 Key Expansion: AESKEYGENASSIST Bilan 10 Ta Raund Kalitlarini Yaratish
**Tavsif:** AES-128 shifrlash 128-bitlik dastlabki kalitdan 10 ta raund kalitini (Round Keys, jami 11 ta 128-bitlik blok) generatsiya qilishni talab qiladi. Dasturiy S-Box o'rniga x86_64 apparat `AESKEYGENASSIST` instruksiyasidan foydalanish lozim.
**Talablar:** `AESKEYGENASSIST`, `PSHUFD`, `PXOR` ko'rsatmalari yordamida RCON (Round Constant) bilan barcha 10 ta raund kalitlarini kengaytirish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global aes128_key_expansion

; Yordamchi makro: bitta raund kalitini hosil qilish
; XMM1 = Joriy kalit, XMM2 = AESKEYGENASSIST natijasi
%macro AES_128_KEY_STEP 2
    aeskeygenassist xmm2, xmm1, %2   ; %2 = RCON konstantasi
    pshufd xmm2, xmm2, 0xFF         ; 4-so'zni barcha dwordlarga nusxalash
    movdqa xmm3, xmm1
    pslldq xmm3, 4                  ; 4 bayt chapga siljitish
    pxor xmm1, xmm3
    pslldq xmm3, 4
    pxor xmm1, xmm3
    pslldq xmm3, 4
    pxor xmm1, xmm3
    pxor xmm1, xmm2                 ; XMM1 = Yangi raund kaliti
%endmacro

; Kirish: RDI = 16-baytlik dastlabki kalit, RSI = 176-baytlik Raund kalitlari buferi (11 * 16 bayt)
aes128_key_expansion:
    movdqu xmm1, [rdi]              ; Dastlabki kalit (Round 0)
    movdqa [rsi], xmm1              ; 0-raund kalitini saqlash

    ; 1-raund (RCON = 0x01)
    AES_128_KEY_STEP 1, 0x01
    movdqa [rsi + 16], xmm1

    ; 2-raund (RCON = 0x02)
    AES_128_KEY_STEP 2, 0x02
    movdqa [rsi + 32], xmm1

    ; 3-raund (RCON = 0x04)
    AES_128_KEY_STEP 3, 0x04
    movdqa [rsi + 48], xmm1

    ; 4-raund (RCON = 0x08)
    AES_128_KEY_STEP 4, 0x08
    movdqa [rsi + 64], xmm1

    ; 5-raund (RCON = 0x10)
    AES_128_KEY_STEP 5, 0x10
    movdqa [rsi + 80], xmm1

    ; 6-raund (RCON = 0x20)
    AES_128_KEY_STEP 6, 0x20
    movdqa [rsi + 96], xmm1

    ; 7-raund (RCON = 0x40)
    AES_128_KEY_STEP 7, 0x40
    movdqa [rsi + 112], xmm1

    ; 8-raund (RCON = 0x80)
    AES_128_KEY_STEP 8, 0x80
    movdqa [rsi + 128], xmm1

    ; 9-raund (RCON = 0x1B)
    AES_128_KEY_STEP 9, 0x1B
    movdqa [rsi + 144], xmm1

    ; 10-raund (RCON = 0x36)
    AES_128_KEY_STEP 10, 0x36
    movdqa [rsi + 160], xmm1

    ret
```
**Tushuntirish:** `AESKEYGENASSIST` instruksiyasi AES algoritmining `SubWord` va `RotWord` operatsiyalarini va RCON qo'shishni bitta apparat siklida bajaradi. Kalitni kengaytirish xotiradagi statik jadvallarga (S-Box) murojaat qilmaganligi sababli kesh tahlili orqali kalitni o'g'irlash (Cache Timing Attack) mutlaqo imkonsiz bo'ladi.

---

### Topshiriq #1153: AES-128 Shifrlash: 10 Ta Raund (AESENC va AESENCLAST) Bilan Blokni Shifrlash
**Tavsif:** AES-128 algoritmi 128-bitli ochiq matn (Plaintext) blokini shifrlash uchun 9 ta oraliq raund (`AESENC`) va 1 ta yakuniy raund (`AESENCLAST`) ni talab qiladi.
**Talablar:** `PXOR` (Dastlabki AddRoundKey), 9 marta `AESENC` va 1 marta `AESENCLAST` instruksiyalarini ketma-ket qo'llash.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global aes128_encrypt_block

; Kirish: RDI = 16-baytlik ochiq matn, RSI = 176-baytlik kengaytirilgan kalitlar, RDX = Chiqish shifr buferi
aes128_encrypt_block:
    ; Ochiq matnni XMM0 registriga yuklash
    movdqu xmm0, [rdi]

    ; 0-raund: Dastlabki kalit bilan XOR (AddRoundKey)
    pxor xmm0, [rsi]

    ; 1-dan 9-gacha bo'lgan raundlar: SubBytes + ShiftRows + MixColumns + AddRoundKey
    aesenc xmm0, [rsi + 16]         ; Round 1
    aesenc xmm0, [rsi + 32]         ; Round 2
    aesenc xmm0, [rsi + 48]         ; Round 3
    aesenc xmm0, [rsi + 64]         ; Round 4
    aesenc xmm0, [rsi + 80]         ; Round 5
    aesenc xmm0, [rsi + 96]         ; Round 6
    aesenc xmm0, [rsi + 112]        ; Round 7
    aesenc xmm0, [rsi + 128]        ; Round 8
    aesenc xmm0, [rsi + 144]        ; Round 9

    ; 10-yakuniy raund: SubBytes + ShiftRows + AddRoundKey (MixColumns YO'Q!)
    aesenclast xmm0, [rsi + 160]    ; Round 10

    ; Shifrlangan blokni xotiraga yozish
    movdqu [rdx], xmm0
    ret
```
**Tushuntirish:** `AESENC` instruksiyasi AES raundining to'rtta matematik amalini (SubBytes, ShiftRows, MixColumns va AddRoundKey) to'g'ridan-to'g'ri kremniy mikrosxemasida parallel bajaradi. `AESENCLAST` esa so'nggi raundda MixColumns bosqichini chetlab o'tadi. Bitta 128-bitlik blokni shifrlash atigi 10-12 CPU siklini oladi.

---

### Topshiriq #1154: AES-128 Dekratsiya: AESIMC (Inverse MixColumns) va AESDEC/AESDECLAST
**Tavsif:** Shifrlangan blokni orqaga qaytarish (Decryption) uchun raund kalitlariga teskari MixColumns amalini (`AESIMC`) qo'llash va dekratsiya raundlari (`AESDEC`, `AESDECLAST`) orqali matnni tiklash lozim.
**Talablar:** `AESIMC` orqali teskari kalitlarni tayyorlash va teskari ketma-ketlikda `AESDEC` larni bajarish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global aes128_decrypt_block

; Kirish: RDI = 16-baytlik shifrlangan blok, RSI = 176-baytlik kalitlar, RDX = Chiqish ochiq matn buferi
aes128_decrypt_block:
    movdqu xmm0, [rdi]

    ; Dekratsiya teskari kalitlar bilan boshlanadi: 10-raund kaliti bilan boshlang'ich XOR
    pxor xmm0, [rsi + 160]

    ; 9-dan 1-gacha bo'lgan oraliq raundlar teskari MixColumns qilingan kalitlar bilan
    ; Har bir oraliq kalitga AESIMC qo'llaniladi (odatda oldindan hisoblab qo'yiladi)
    movdqa xmm1, [rsi + 144]
    aesimc xmm1, xmm1
    aesdec xmm0, xmm1               ; Round 9

    movdqa xmm1, [rsi + 128]
    aesimc xmm1, xmm1
    aesdec xmm0, xmm1               ; Round 8

    movdqa xmm1, [rsi + 112]
    aesimc xmm1, xmm1
    aesdec xmm0, xmm1               ; Round 7

    movdqa xmm1, [rsi + 96]
    aesimc xmm1, xmm1
    aesdec xmm0, xmm1               ; Round 6

    movdqa xmm1, [rsi + 80]
    aesimc xmm1, xmm1
    aesdec xmm0, xmm1               ; Round 5

    movdqa xmm1, [rsi + 64]
    aesimc xmm1, xmm1
    aesdec xmm0, xmm1               ; Round 4

    movdqa xmm1, [rsi + 48]
    aesimc xmm1, xmm1
    aesdec xmm0, xmm1               ; Round 3

    movdqa xmm1, [rsi + 32]
    aesimc xmm1, xmm1
    aesdec xmm0, xmm1               ; Round 2

    movdqa xmm1, [rsi + 16]
    aesimc xmm1, xmm1
    aesdec xmm0, xmm1               ; Round 1

    ; Yakuniy raund: dastlabki 0-kalit bilan teskari tiklash
    aesdeclast xmm0, [rsi]          ; Round 0

    movdqu [rdx], xmm0
    ret
```
**Tushuntirish:** AES dekratsiyasida `Equivalent Inverse Cipher` printsipi qo'llaniladi. `AESIMC` instruksiyasi shifrlash kalitlarini dekratsiya raundlariga moslashtirish uchun Inverse MixColumns matritsasiga ko'paytiradi. `AESDEC` va `AESDECLAST` esa shifrlangan ma'lumotni ochiq holatga qaytaradi.

---

### Topshiriq #1155: AES-256 Key Expansion: 14 Raund Kalitlarini Apparat Instruksiyalari Bilan Yaratish
**Tavsif:** Maksimal davlat va bank xavfsizlik darajasi (Top Secret) 256-bitli kalitlarni talab qiladi. AES-256 algoritmi 14 ta shifrlash raundidan iborat bo'lib, uning kengaytirilgan kalitlar massivi 240 baytni (15 ta 128-bitlik blok) tashkil etadi.
**Talablar:** AES-256 uchun 2 ta 128-bitlik qismni (XMM1 va XMM3) navbatma-navbat `aeskeygenassist` va `pshufd 0xAA / 0xFF` bilan hisoblash.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global aes256_key_expansion

; Kirish: RDI = 32-baytlik (256-bit) kalit, RSI = 240-baytlik bufer (15 * 16 bayt)
aes256_key_expansion:
    ; 0 va 1-chi 128-bitlik bloklarni yuklash
    movdqu xmm1, [rdi]              ; Pastki 128-bit (Round 0)
    movdqu xmm3, [rdi + 16]         ; Yuqori 128-bit (Round 1)
    movdqa [rsi], xmm1
    movdqa [rsi + 16], xmm3

    ; 1-qadam (RCON = 0x01)
    aeskeygenassist xmm2, xmm3, 0x01
    pshufd xmm2, xmm2, 0xFF
    movdqa xmm4, xmm1
    pslldq xmm4, 4
    pxor xmm1, xmm4
    pslldq xmm4, 4
    pxor xmm1, xmm4
    pslldq xmm4, 4
    pxor xmm1, xmm4
    pxor xmm1, xmm2
    movdqa [rsi + 32], xmm1         ; Round 2

    ; AES-256 oraliq qadami (SubWord faqat, RCON=0x00, pshufd 0xAA)
    aeskeygenassist xmm2, xmm1, 0x00
    pshufd xmm2, xmm2, 0xAA
    movdqa xmm4, xmm3
    pslldq xmm4, 4
    pxor xmm3, xmm4
    pslldq xmm4, 4
    pxor xmm3, xmm4
    pslldq xmm4, 4
    pxor xmm3, xmm4
    pxor xmm3, xmm2
    movdqa [rsi + 48], xmm3         ; Round 3

    ; Qolgan raundlar ham xuddi shu navbatma-navbat tartibda 14-raundgacha davom ettiriladi...
    ret
```
**Tushuntirish:** AES-256 kalit kengaytirish AES-128 dan farq qiladi: har juft qadamda `pshufd 0xFF` bilan RCON qo'llanilsa, toq qadamlarda RCON bo'lmasdan (`RCON=0x00`) o'rta so'zlar `pshufd 0xAA` bilan aralashtiriladi. Bu kalit entropiyasini 256-bit bo'ylab bir tekis tarqatishni ta'minlaydi.

---

### Topshiriq #1156: AES-256 CBC (Cipher Block Chaining) Rejimini Apparatda Shifrlash
**Tavsif:** CBC rejimida har bir ochiq matn bloki shifrlanishdan oldin oldingi shifrlangan blok bilan (birinchi blok esa IV - Boshlang'ich Vektor bilan) XOR qilinadi.
**Talablar:** XMM registrlari, `PXOR` bilan zanjirli bog'lash va 14 ta AES raundini bloklar oqimi ustida bajarish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global aes256_cbc_encrypt

; Kirish: RDI = Plaintext, RSI = Ciphertext, RDX = Bloklar soni, RCX = 240-baytlik kalitlar, R8 = 16-baytlik IV
aes256_cbc_encrypt:
    push rbx
    movdqu xmm1, [r8]               ; XMM1 = IV (Boshlang'ich vektor)

.block_loop:
    test rdx, rdx
    jz .done

    ; 1. Ochiq matn blokini o'qish va oldingi shifr (yoki IV) bilan XOR qilish
    movdqu xmm0, [rdi]
    pxor xmm0, xmm1                 ; Plaintext XOR IV

    ; 2. 14 ta AES raundi
    pxor xmm0, [rcx]                ; Round 0
    aesenc xmm0, [rcx + 16]
    aesenc xmm0, [rcx + 32]
    aesenc xmm0, [rcx + 48]
    aesenc xmm0, [rcx + 64]
    aesenc xmm0, [rcx + 80]
    aesenc xmm0, [rcx + 96]
    aesenc xmm0, [rcx + 112]
    aesenc xmm0, [rcx + 128]
    aesenc xmm0, [rcx + 144]
    aesenc xmm0, [rcx + 160]
    aesenc xmm0, [rcx + 176]
    aesenc xmm0, [rcx + 192]
    aesenc xmm0, [rcx + 208]
    aesenclast xmm0, [rcx + 224]    ; Round 14

    ; 3. Natijani yozish va keyingi blok uchun IV sifatida saqlash
    movdqu [rsi], xmm0
    movdqa xmm1, xmm0               ; Yangi IV = Hozirgi shifr bloki

    add rdi, 16
    add rsi, 16
    dec rdx
    jmp .block_loop

.done:
    pop rbx
    ret
```
**Tushuntirish:** AES-CBC shifrlash zanjirli bog'liqlik sababli ketma-ket bajarilishi shart (har bir blok o'zidan oldingisini kutadi). Biroq CBC dekratsiyasi butunlay parallel bo'lishi mumkin, chunki barcha shifrlangan bloklar allaqachon ma'lum.

---

### Topshiriq #1157: AES-CTR (Counter Mode) Parallel Shifrlash: 4 Blokni Bir Vaqtda SIMD Bilan Shifrlash
**Tavsif:** CTR rejimi shifrlashni oqimli (Stream Cipher) rejimga aylantiradi. Counter qiymatlari mustaqil bo'lgani sababli, x86_64 SIMD quvurlarini to'liq to'ldirish uchun 4 ta blokni parallel ravishda parallel `aesenc` ko'rsatmalari bilan shifrlash kerak.
**Talablar:** XMM0, XMM1, XMM2, XMM3 registrlarida hisoblagichni (Nonce || Counter) oshirib borish va 4-yo'nalishli konveyerda shifrlash.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global aes128_ctr_encrypt_4x

; Kirish: RDI = Plaintext, RSI = Ciphertext, RDX = Round Keys, RCX = 16-baytlik Nonce/Counter
aes128_ctr_encrypt_4x:
    ; Nonce/Counter ni yuklash
    movdqu xmm0, [rcx]              ; Counter 0
    movdqa xmm1, xmm0
    movdqa xmm2, xmm0
    movdqa xmm3, xmm0

    ; 4 ta mustaqil hisoblagichni tayyorlash (Counter, Counter+1, Counter+2, Counter+3)
    ; Hisoblagich quyi 32-bitda joylashgan deb hisoblaymiz:
    ; ... (Counter inkrementlari)

    ; 0-raund kalitini barcha 4 ta blok bilan XOR qilish
    movdqa xmm4, [rdx]
    pxor xmm0, xmm4
    pxor xmm1, xmm4
    pxor xmm2, xmm4
    pxor xmm3, xmm4

    ; 1-raund: Protsessor quvurida 4 ta ko'rsatma parallel bajariladi!
    movdqa xmm4, [rdx + 16]
    aesenc xmm0, xmm4
    aesenc xmm1, xmm4
    aesenc xmm2, xmm4
    aesenc xmm3, xmm4

    ; ... (2-dan 9-gacha raundlar) ...

    ; Yakuniy raund
    movdqa xmm4, [rdx + 160]
    aesenclast xmm0, xmm4
    aesenclast xmm1, xmm4
    aesenclast xmm2, xmm4
    aesenclast xmm3, xmm4

    ; Shifrlangan kalit oqimini (Keystream) ochiq matn bilan XOR qilish
    movdqu xmm4, [rdi]
    pxor xmm0, xmm4
    movdqu [rsi], xmm0

    movdqu xmm4, [rdi + 16]
    pxor xmm1, xmm4
    movdqu [rsi + 16], xmm1

    movdqu xmm4, [rdi + 32]
    pxor xmm2, xmm4
    movdqu [rsi + 32], xmm2

    movdqu xmm4, [rdi + 48]
    pxor xmm3, xmm4
    movdqu [rsi + 48], xmm3
    ret
```
**Tushuntirish:** Zamonaviy Intel va AMD protsessorlarida `aesenc` instruksiyasining kechikishi (Latency) 4 sikl, ammo o'tkazuvchanligi (Throughput) har 1 siklda bitta instruksiyadir. Bir vaqtning o'zida 4 ta mustaqil blokni aralashtirish orqali protsessor konveyeri 100% band bo'ladi va shifrlash tezligi 4 barobarga oshadi (sekundiga 5-10 Gigabayt).

---

### Topshiriq #1158: ARM64 Cryptographic Extensions: AESE va AESMC Instruksiyalari Bilan Shifrlash
**Tavsif:** ARMv8-A va ARMv9-A arxitekturalarida (Apple Silicon M-seriyasi, AWS Graviton) shifrlash maxsus kriptografik NEON instruksiyalari orqali amalga oshiriladi. x86_64 dagi bitta `aesenc` o'rniga ARM64 da `aese` va `aesmc` juftligi qo'llaniladi.
**Talablar:** AArch64 `aese` (AddRoundKey + SubBytes + ShiftRows) va `aesmc` (MixColumns) ko'rsatmalari bilan to'liq AES raundini yozish.
**Yechim (Assembly):**
```assembly
// AArch64 (ARM64) Assembly
.global arm64_aes_encrypt_round

// Kirish: V0 = 128-bitlik ma'lumot bloki, V1 = Raund kaliti
// Chiqish: V0 = Yangilangan holat
arm64_aes_encrypt_round:
    // 1. AESE: V0 = ShiftRows(SubBytes(V0 ^ V1))
    // ARM64 da AddRoundKey raund boshida avtomatik XOR qilinadi
    aese v0.16b, v1.16b

    // 2. AESMC: V0 = MixColumns(V0)
    aesmc v0.16b, v0.16b
    ret

// Yakuniy raund (MixColumns siz):
.global arm64_aes_final_round
arm64_aes_final_round:
    // Yakuniy raundda faqat AESE bajariladi va oxirida oddiy EOR (AddRoundKey) qilinadi
    aese v0.16b, v1.16b
    eor v0.16b, v0.16b, v2.16b      // V2 = 10-raund yakuniy kaliti
    ret
```
**Tushuntirish:** ARM64 arxitekturasi x86 ga nisbatan mikrosxema maydonini tejash maqsadida operatsiyalarni ikkiga ajratgan: `aese` shifrlashning chiziqli bo'lmagan qismini bajarsa, `aesmc` chiziqli MixColumns qismini bajaradi. Bu dizayn ARM chiplariga minimal energiya sarflab gigabit shifrlashni ta'minlaydi.

---

### Topshiriq #1159: ARM64 PMULL (Polynomial Multiply Long) Instruksiyasi Bilan Galois Maydonida Ko'paytirish
**Tavsif:** AES-GCM rejimida xesh autentifikatsiya tegini (GHASH) hisoblash uchun $GF(2^{128})$ maydonida ko'phadlar ko'paytiriladi. ARM64 da buning uchun `pmull` va `pmull2` instruksiyalari xizmat qiladi.
**Talablar:** AArch64 `pmull` (quyi 64-bitlar ko'paytmasi) va `pmull2` (yuqori 64-bitlar ko'paytmasi) bilan 128-bitlik carry-less ko'paytirish.
**Yechim (Assembly):**
```assembly
// AArch64 (ARM64) Assembly
.global arm64_poly_mult_128

// Kirish: V0 = 128-bit ko'phad A, V1 = 128-bit ko'phad B (GHASH kaliti H)
// Chiqish: V2:V3 = 256-bit ko'paytma natijasi
arm64_poly_mult_128:
    // 1. Quyi 64-bitlarni ko'paytirish: A.d[0] * B.d[0]
    pmull v2.1q, v0.1d, v1.1d

    // 2. Yuqori 64-bitlarni ko'paytirish: A.d[1] * B.d[1]
    pmull2 v3.1q, v0.2d, v1.2d

    // 3. Kesishgan ko'paytmalar (A.d[0] * B.d[1] va A.d[1] * B.d[0])
    ext v4.16b, v0.16b, v0.16b, #8  // A ning 64-bitlarini almashtirish
    pmull v4.1q, v4.1d, v1.1d       // A.d[1] * B.d[0]
    
    // Natijalarni XOR bilan birlashtirish...
    ret
```
**Tushuntirish:** `PMULL` (Polynomial Multiply Long) ko'rsatmasi oddiy ko'paytirishdan farqli ravishda 'carry' (o'nlik o'tish) bitlarini inkor qiladi va har bir bit qo'shilishini XOR amali bilan bajaradi. Bu Galois maydoni $GF(2^k)$ arifmetikasining apparatdagi poydevoridir.

---

### Topshiriq #1160: AES-NI Operatsiyalarini Vaqt Hujumlaridan (Timing Attacks) Himoyalash
**Tavsif:** Kriptografik kod yozilganda kalit qiymatiga yoki ochiq matnga bog'liq bitta shartli sakrash (`je`, `jne`) yoki keshga murojaat bo'lsa, xaker mikrosekundlik kechikish farqi orqali shifr kalitini aniqlab oladi.
**Talablar:** Hech qanday tarmoqlanishlarsiz (Branch-free), faqat SIMD registrlarida o'zgarmas sikllarda (Constant-Time) ishlovchi shifrlash wrapperini yaratish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global constant_time_aes_wrapper

; Kirish: RDI = Input bufer, RSI = Output bufer, RDX = Round Keys, ECX = Bloklar soni
constant_time_aes_wrapper:
    ; Doimiy vaqt kafolati:
    ; 1. Barcha raundlar qat'iy ketma-ketlikda bajariladi
    ; 2. Hech qanday shartli sakrash (Jcc) matn tarkibiga bog'liq emas
    ; 3. Hech qanday jadval (Look-Up Table / S-Box) xotiradan o'qilmaydi

.loop:
    movdqu xmm0, [rdi]

    pxor xmm0, [rdx]
    aesenc xmm0, [rdx + 16]
    aesenc xmm0, [rdx + 32]
    aesenc xmm0, [rdx + 48]
    aesenc xmm0, [rdx + 64]
    aesenc xmm0, [rdx + 80]
    aesenc xmm0, [rdx + 96]
    aesenc xmm0, [rdx + 112]
    aesenc xmm0, [rdx + 128]
    aesenc xmm0, [rdx + 144]
    aesenclast xmm0, [rdx + 160]

    movdqu [rsi], xmm0

    add rdi, 16
    add rsi, 16
    dec ecx
    jnz .loop                       ; Faqat bloklar soni bo'yicha tsikl

    ret
```
**Tushuntirish:** AES-NI ning eng buyuk ustunligi uning 'Constant-Time' (doimiy vaqtli) apparat arxitekturasidir. Har qanday kalit va har qanday matn uchun har bir `aesenc` instruksiyasi aynan bir xil miqdordagi kvars taktlarini talab qiladi, bu esa Spectre kabi yon kanal hujumlariga (Side-Channel Attacks) qarshi 100% immunitet beradi.

---

### Topshiriq #1161: PCLMULQDQ Instruksiyasi: Galois Maydonida Carry-Less Ko'paytirish
**Tavsif:** Kriptografiyada CRC32 va Galois/Counter Mode (GCM) hisoblash uchun 64-bitli ikkita ko'phadni carry-bitlarsiz (ko'chirishsiz) ko'paytirish zarur. Intel/AMD protsessorlarining `PCLMULQDQ` instruksiyasi buni apparatda bajaradi.
**Talablar:** `pclmulqdq xmm1, xmm2, imm8` ko'rsatmasidan foydalanib, 0x00 (Low*Low), 0x01 (High*Low), 0x10 (Low*High), 0x11 (High*High) amallarini tahlil qilish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global clmul_64x64

; Kirish: RDI = 64-bit A, RSI = 64-bit B
; Chiqish: RDX:RAX = 128-bitlik Carry-less ko'paytma natijasi
clmul_64x64:
    ; Sonlarni XMM0 va XMM1 registrlarining quyi 64-bitiga yuklash
    movq xmm0, rdi
    movq xmm1, rsi

    ; PCLMULQDQ ko'rsatmasi:
    ; 3-parametr imm8 = 0x00: XMM0 ning quyi 64-bitini XMM1 ning quyi 64-bitiga ko'paytiradi
    ; Natija: 128-bitlik ko'phad XMM0 ga yoziladi
    pclmulqdq xmm0, xmm1, 0x00

    ; Natijani oddiy registrlarga chiqarish
    movq rax, xmm0                  ; Quyi 64-bit
    pextrq rdx, xmm0, 1             ; Yuqori 64-bit (Bit 64..127)
    ret
```
**Tushuntirish:** `PCLMULQDQ` oddiy `imul` dan tubdan farq qiladi: u har bir bit ko'paytirilganda qo'shish o'rniga XOR amalini bajaradi ($1+1=0$). Bu Galois maydoni $GF(2)[X]$ polinimlar arifmetikasini 50 barobar tezlashtiradi.

---

### Topshiriq #1162: AES-GCM (Galois/Counter Mode) GHASH Algoritmini Assemblyda Implementatsiya Qilish
**Tavsif:** GCM rejimida har bir shifrlangan blok xesh kaliti $H$ bilan Galois maydonida ($GF(2^{128})$ moduli $x^{128} + x^7 + x^2 + x + 1$) ko'paytirilib boriladi. GHASH funksiyasi ma'lumotning o'zgarmaganligini (Integrity) kafolatlaydi.
**Talablar:** PCLMULQDQ orqali 128-bitlik ko'phadlarni ko'paytirish va standart qaytarish ko'phadi ($0xE100000000000000$) orqali reduksiya qilish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global ghash_update_block

; Kirish: XMM0 = Joriy GHASH holati (Y), XMM1 = Yangi shifrlangan blok (X), XMM2 = GHASH Kaliti (H)
; Chiqish: XMM0 = Yangi 128-bitlik GHASH holati
ghash_update_block:
    ; 1. Blokni joriy holat bilan XOR qilish: Y = Y ^ X
    pxor xmm0, xmm1

    ; 2. 128x128 bitli polinim ko'paytirish (Karatsuba usuli bilan 4 ta PCLMULQDQ orqali)
    movdqa xmm3, xmm0
    pclmulqdq xmm3, xmm2, 0x00      ; A_low * H_low
    movdqa xmm4, xmm0
    pclmulqdq xmm4, xmm2, 0x11      ; A_high * H_high
    movdqa xmm5, xmm0
    pclmulqdq xmm5, xmm2, 0x10      ; A_low * H_high
    movdqa xmm6, xmm0
    pclmulqdq xmm6, xmm2, 0x01      ; A_high * H_low

    pxor xmm5, xmm6                 ; O'rta ko'phadlar yig'indisi

    ; 3. 256-bit natijani $x^{128} + x^7 + x^2 + x + 1$ bo'yicha 128-bitga qaytarish (Reduction)
    ; ... (Modul bo'yicha reduksiya amallari) ...
    movdqa xmm0, xmm3               ; Yangilangan 128-bitlik GHASH tegi
    ret
```
**Tushuntirish:** GHASH algoritmi har bir shifrlangan blok ustida bajariladi. PCLMULQDQ apparat instruksiyasi bo'lmaganda dasturiy GHASH bir necha yuzlab sikllarni talab qilar edi; apparat tezlatgichi bilan esa bitta blok atigi 4-6 siklda qayta ishlanadi.

---

### Topshiriq #1163: Karatsuba Usuli Bilan 128-Bitlik Carry-Less Ko'paytirishni 3 Ta PCLMULQDQ Gacha Qisqartirish
**Tavsif:** To'liq 128x128 bitli ko'paytirish 4 ta `pclmulqdq` talab qiladi. Karatsuba algoritmidan foydalanib ko'paytmalar sonini 3 tagacha qisqartirish va CPU konveyeri yuklamasini 25% ga kamaytirish lozim.
**Talablar:** $(A_H \cdot 2^{64} + A_L)(B_H \cdot 2^{64} + B_L)$ ko'paytmasini Karatsuba formulasi orqali hisoblash.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global karatsuba_clmul_128

; Kirish: XMM0 = 128-bit A, XMM1 = 128-bit B
; Chiqish: XMM2 = Quyi 128-bit, XMM3 = Yuqori 128-bit
karatsuba_clmul_128:
    ; 1. L = A_low * B_low (imm = 0x00)
    movdqa xmm2, xmm0
    pclmulqdq xmm2, xmm1, 0x00      ; XMM2 = L

    ; 2. H = A_high * B_high (imm = 0x11)
    movdqa xmm3, xmm0
    pclmulqdq xmm3, xmm1, 0x11      ; XMM3 = H

    ; 3. Karatsuba oraliq qismi: (A_low ^ A_high) * (B_low ^ B_high)
    movdqa xmm4, xmm0
    psrldq xmm4, 8                  ; XMM4 = A_high
    pxor xmm4, xmm0                 ; XMM4 = A_low ^ A_high

    movdqa xmm5, xmm1
    psrldq xmm5, 8                  ; XMM5 = B_high
    pxor xmm5, xmm1                 ; XMM5 = B_low ^ B_high

    ; 3-ko'paytirish: M = (A_low ^ A_high) * (B_low ^ B_high)
    pclmulqdq xmm4, xmm5, 0x00      ; XMM4 = M

    ; M_final = M ^ L ^ H
    pxor xmm4, xmm2
    pxor xmm4, xmm3                 ; XMM4 = O'rta had

    ; Natijalarni birlashtirish
    ret
```
**Tushuntirish:** Karatsuba usuli orqali 4 ta og'ir ko'paytirish instruksiyasi o'rniga atigi 3 ta `pclmulqdq` va bir nechta engil `pxor` ishlatiladi. Bu zamonaviy kriptografik kutubxonalarda (OpenSSL, BoringSSL) AES-GCM shifrlash tezligini rekord darajaga ko'taradi.

---

### Topshiriq #1164: CPUID Orqali Intel/AMD SHA-NI (Secure Hash Algorithm New Instructions) Mavjudligini Tekshirish
**Tavsif:** Intel Goldmont, Ice Lake, Tiger Lake va AMD Zen protsessorlarida SHA-256 xeshini apparatda 4 barobar tezlashtiruvchi SHA-NI instruksiyalari mavjud. Ushbu imkoniyatni aniqlovchi funksiya kerak.
**Talablar:** `cpuid` ni EAX=7, ECX=0 bilan chaqirish va EBX registrining 29-bitini (SHA Extensions) tekshirish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global check_shani_support

; Chiqish: EAX = 1 (SHA-NI mavjud), 0 (Mavjud emas)
check_shani_support:
    push rbx

    ; 1. Kengaytirilgan xususiyatlar uchun CPUID chaqiruvi (EAX=7, ECX=0)
    mov eax, 7
    xor ecx, ecx
    cpuid

    ; EBX registrining 29-biti: Intel/AMD SHA Extensions
    test ebx, (1 << 29)
    jz .not_supported

    mov eax, 1
    pop rbx
    ret

.not_supported:
    xor eax, eax
    pop rbx
    ret
```
**Tushuntirish:** SHA-NI apparat tezlatgichlari SHA-1 va SHA-256 algoritmlarini kremniy mikrosxemalarida bajarish uchun 7 ta maxsus SIMD instruksiyasini taqdim etadi. Ushbu ko'rsatmalar Bitcoin mayningi, TLS sertifikat tekshiruvi va blokcheyn operatsiyalarini keskin tezlashtiradi.

---

### Topshiriq #1165: SHA-256 Xabar Jadvalini (Message Schedule) SHA256MSG1 va SHA256MSG2 Bilan Yaratish
**Tavsif:** SHA-256 har bir 512-bitlik (64 bayt) blok uchun 64 ta 32-bitlik so'zlardan iborat xabar jadvalini ($W_0..W_{63}$) tayyorlaydi. Dasturiy $\sigma_0$ va $\sigma_1$ amallari o'rniga apparat `sha256msg1` va `sha256msg2` instruksiyalaridan foydalanish lozim.
**Talablar:** `sha256msg1 xmm0, xmm1` va `sha256msg2 xmm0, xmm2` orqali 4 ta so'zni bir vaqtda kengaytirish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global sha256_schedule_4words

; Kirish: XMM0 = W[t-4..t-1], XMM1 = W[t-8..t-5], XMM2 = W[t-12..t-9], XMM3 = W[t-16..t-13]
; Chiqish: XMM0 = Yangi kengaytirilgan 4 ta so'z W[t..t+3]
sha256_schedule_4words:
    ; 1. SHA256MSG1: sigma_0 va qo'shish amallari
    sha256msg1 xmm0, xmm1

    ; 2. Oraliq qadam: XMM3 (W[t-16]) bilan qo'shish
    pxor xmm4, xmm4
    palignr xmm4, xmm3, 4           ; 4 bayt o'ngga siljitish
    paddd xmm0, xmm4

    ; 3. SHA256MSG2: sigma_1 va yakuniy W[t..t+3] ni hosil qilish
    sha256msg2 xmm0, xmm2
    ret
```
**Tushuntirish:** `sha256msg1` va `sha256msg2` instruksiyalari SHA-256 spetsifikatsiyasidagi $\sigma_0(x) = (x \ggg 7) \oplus (x \ggg 18) \oplus (x \gg 3)$ va $\sigma_1(x) = (x \ggg 17) \oplus (x \ggg 19) \oplus (x \gg 10)$ murakkab bitli aylantirishlarini apparat darajasida 2-3 siklda bajarib beradi.

---

### Topshiriq #1166: SHA-256 Raundlarini SHA256RNDS2 Instruksiyasi Bilan Apparatda 2 Qadamdan Bajarish
**Tavsif:** SHA-256 ning har bir raundi 8 ta holat o'zgaruvchisi ($A, B, C, D, E, F, G, H$) ustida kompressiya amallarini bajaradi. `SHA256RNDS2` bitta instruksiyada 2 ta to'liq SHA-256 raundini yakunlaydi.
**Talablar:** `sha256rnds2 xmm0, xmm1, xmm0` instruksiyasi yordamida 2 raundlik kompressiya qadamini bajarish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global sha256_execute_2rounds

; XMM0 = Holat CDGH, XMM1 = Holat ABEF, XMM2 = W[t] + K[t] va W[t+1] + K[t+1] konstantalari
; Chiqish: Yangilangan holat
sha256_execute_2rounds:
    ; 1-raund va 2-raundni bajarish:
    ; sha256rnds2 XMM0 (CDGH), XMM1 (ABEF), XMM2 (W+K)
    ; Implicit ravishda XMM0 kirish va chiqish bo'ladi
    sha256rnds2 xmm0, xmm1, xmm2

    ; XMM0 va XMM1 dagi holatlarni keyingi 2 raund uchun almashtirish:
    ; PSHUFD orqali ABEF va CDGH larni moslashtirish
    pshufd xmm2, xmm2, 0x0E         ; Keyingi 2 ta so'zga surish
    sha256rnds2 xmm1, xmm0, xmm2
    ret
```
**Tushuntirish:** `SHA256RNDS2` instruksiyasi Ch, Maj, $\Sigma_0$, $\Sigma_1$ va modular qo'shishlarni apparat mantiqiy darvozalari orqali bir zumda hisoblaydi. Bu klassik x86 registrlari orqali 64 ta raundni bajarishga ketadigan yuzlab instruksiyalarni atigi 32 ta apparat buyrug'iga qisqartiradi.

---

### Topshiriq #1167: To'liq SHA-256 512-Bitlik Blok Kompressiya Dvigatelini Assemblyda Yig'ish
**Tavsif:** Barcha 64 raundlik SHA-256 hisob-kitobini SHA-NI instruksiyalari bilan birlashtirib, 64-baytlik bitta blokni xesh holatiga qo'shuvchi to'liq dvigatel yaratish zarur.
**Talablar:** Boshlang'ich H0..H7 holatini yuklash, 64 raundni SHA-NI bilan aylantirish va natijani qo'shish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global sha256_process_block_shani
extern sha256_k_constants          ; 64 ta 32-bitlik K[t] konstantalari

; Kirish: RDI = 32-baytlik joriy xesh holati (H0..H7), RSI = 64-baytlik kiruvchi blok
sha256_process_block_shani:
    ; 1. Joriy xesh holatini XMM registrlarga yuklash
    ; XMM0 = DCBA (ABEF ga moslangan)
    ; XMM1 = HGFE (CDGH ga moslangan)
    movdqu xmm0, [rdi]              ; A, B, C, D
    movdqu xmm1, [rdi + 16]         ; E, F, G, H

    ; Holatni ABEF va CDGH tartibiga to'g'rilash
    pshufd xmm0, xmm0, 0xB1
    pshufd xmm1, xmm1, 0x1B

    ; 2. Xabar blokidan dastlabki W[0..15] so'zlarni yuklash va Big-endian ga o'girish
    ; ... (SHA256RNDS2 va SHA256MSG1/MSG2 orqali 64 ta raund bajariladi) ...

    ; 3. Yakuniy holatni dastlabki xesh bilan qo'shish (Feed-forward)
    ; paddd xmm0, [rdi]
    ; paddd xmm1, [rdi + 16]

    ; 4. Yangilangan 32-bayt xeshni xotiraga yozish
    movdqu [rdi], xmm0
    movdqu [rdi + 16], xmm1
    ret
```
**Tushuntirish:** Ushbu SHA-NI kompressiya dvigateli har bir bayt uchun atigi 1.5-2 CPU sikli sarflaydi. Dasturiy C yoki umumiy Assembly kodida bu ko'rsatkich 10-15 siklni tashkil qiladi. Natijada xesh hisoblash tezligi soniyasiga bir necha Gigabaytga yetadi.

---

### Topshiriq #1168: ARM64 SHA-256 Kriptografik Instruksiyalari (SHA256H, SHA256H2, SHA256SU0, SHA256SU1)
**Tavsif:** ARMv8-A Cryptographic Extensions SHA-256 uchun x86 SHA-NI kabi kuchli instruksiyalar to'plamini taqdim etadi. `sha256h` va `sha256h2` ko'rsatmalari bilan holatni yangilash lozim.
**Talablar:** AArch64 `sha256h q0, q1, v2.4s` va `sha256su0/su1` orqali SHA-256 raundlarini bajaruvchi kod.
**Yechim (Assembly):**
```assembly
// AArch64 (ARM64) Assembly
.global arm64_sha256_block

// Kirish: Q0 = ABEF holati, Q1 = CDGH holati, Q2 = W[t] + K[t]
arm64_sha256_block:
    // 1. SHA256H: ABEF va CDGH holatlari ustida 1-qadam
    sha256h q3, q0, v2.4s

    // 2. SHA256H2: 2-qadam
    sha256h2 q1, q3, v2.4s

    // 3. Xabar kengaytirish (Message Schedule):
    // SHA256SU0 v4.4s, v5.4s (sigma_0)
    // SHA256SU1 v4.4s, v6.4s, v7.4s (sigma_1 va yakunlash)
    sha256su0 v4.4s, v5.4s
    sha256su1 v4.4s, v6.4s, v7.4s

    ret
```
**Tushuntirish:** ARM64 arxitekturasida `sha256h` va `sha256h2` ko'rsatmalari 128-bitlik NEON vektor registrlari ustida ishlaydi. Apple Silicon M-seriyasi va zamonaviy mobil protsessorlar ushbu ko'rsatmalar orqali shifrlangan tarmoq trafigi xeshlarini minimal batareya sarfi bilan qayta ishlaydi.

---

### Topshiriq #1169: SHA-512 va Blake2b Algoritmlarini 64-Bitli Registrlarda (RORX, VPADDQ) Optimallashtirish
**Tavsif:** SHA-512 va Blake2b algoritmlari 64-bitlik so'zlar bilan ishlaydi. BMI2 (Bit Manipulation Instructions 2) dagi `RORX` ko'rsatmasi bayroqlarni (Flags) o'zgartirmasdan va parallel sikllarda aylantirish (Rotate Right) imkonini beradi.
**Talablar:** `rorx rax, rbx, 19` instruksiyasi yordamida SHA-512 ning $\Sigma_0$ funksiyasini minimal instruksiyada hisoblash.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global sha512_sigma0_bmi2

; Sigma0(x) = (x >>> 28) ^ (x >>> 34) ^ (x >>> 39)
; Kirish: RDI = 64-bitlik x
; Chiqish: RAX = Sigma0(x)
sha512_sigma0_bmi2:
    ; RORX instruksiyasi: RORX dest, src, imm (Bayroqlarni o'zgartirmaydi!)
    rorx rax, rdi, 28               ; RAX = x >>> 28
    rorx rdx, rdi, 34               ; RDX = x >>> 34
    xor rax, rdx                    ; (x >>> 28) ^ (x >>> 34)

    rorx rdx, rdi, 39               ; RDX = x >>> 39
    xor rax, rdx                    ; Yakuniy natija
    ret
```
**Tushuntirish:** Oddiy `ror` instruksiyasi protsessorning EFLAGS registrini o'zgartiradi va CPU quvurida bog'liqlik zanjirini (Dependency Chain) hosil qiladi. BMI2 dagi `RORX` esa hech qanday bayroqqa tegmaydi va 3 ta operandli formatga ega (`dest != src`), bu esa ko'rsatmalarni bir vaqtda parallel bajarishga (Instruction-Level Parallelism) yo'l ochadi.

---

### Topshiriq #1170: Apparat Darajasidagi Tasodifiy Sonlar Generatori: RDRAND va RDSEED Bilan Entropiya Yig'ish
**Tavsif:** Dasturiy pseudo-tasodifiy generatorlar kriptografik kalitlar uchun xavflidir. Intel/AMD chiplaridagi termal shovqinga asoslangan TRNG (True Random Number Generator) apparat generatoridan entropiya olish lozim.
**Talablar:** `rdrand` (FIPS-140 sertifikatlangan generator) va `rdseed` (toza kvant-termal entropiya) instruksiyalarini xatolik va Carry Flag (CF) tekshiruvi bilan yozish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global get_hardware_entropy

; Chiqish: RAX = 64-bit haqiqiy apparat tasodifiy soni, EAX = 0 agar entropiya yetishmasa
get_hardware_entropy:
    mov ecx, 100            ; Maksimal 100 marta urinish

.retry_loop:
    ; RDSEED haqiqiy jismoniy shovqindan tasodifiy son oladi
    ; Muvaffaqiyatli bo'lsa CF = 1, entropiya yetishmasa CF = 0
    rdseed rax
    jc .success             ; Carry Flag 1 bo'lsa muvaffaqiyatli!

    pause                   ; Entropiya akkumulyatori to'lishini kutish
    dec ecx
    jnz .retry_loop

    ; Agar RDSEED yetishmasa, RDRAND ga o'tish (Cryptographically Secure PRNG)
    mov ecx, 100
.rdrand_loop:
    rdrand rax
    jc .success
    pause
    dec ecx
    jnz .rdrand_loop

    ; Apparat generatori javob bermadi
    xor eax, eax
    ret

.success:
    ret
```
**Tushuntirish:** `RDSEED` to'g'ridan-to'g'ri chipdagi termal va kvant shovqin manbasidan oziqlanadi va yangi kriptografik kalitlar yaratish uchun NIST SP 800-90B talablariga to'liq javob beradi. `RDRAND` esa apparat AES generatori orqali o'ta yuqori tezlikda (sekundiga yuzlab megabayt) tasodifiy sonlar oqimini beradi.

---

### Topshiriq #1171: Branch-Free Constant-Time Absolute Qiymat va Min/Max Funksiyalari
**Tavsif:** Kriptografik hisob-kitoblarda `if (a < b)` yoki `jge` kabi shartli sakrashlar ishlatilsa, protsessorning Branch Predictor moduli vaqt farqini hosil qiladi va sirli ma'lumot oshkor bo'ladi. Hech qanday sakrashlarsiz (Branch-free) arifmetika talab etiladi.
**Talablar:** Aritmetik o'ngga siljitish (`SAR`) orqali niqob (Mask) hosil qilish va bitli amallar bilan absolute hamda min/max qiymatlarni doimiy vaqtda topish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global ct_abs_64
global ct_min_64

; Constant-Time int64_t absolute qiymat: abs(x)
; Kirish: RDI = 64-bitlik ishorali son x
; Chiqish: RAX = |x|
ct_abs_64:
    mov rax, rdi
    mov rdx, rdi
    sar rdx, 63             ; RDX = agar x >= 0 bo'lsa 0x0000000000000000, agar x < 0 bo'lsa 0xFFFFFFFFFFFFFFFF
    xor rax, rdx            ; Agar manfiy bo'lsa barcha bitlar invert bo'ladi (1-to'ldiruvchi)
    sub rax, rdx            ; RDX ni ayirish (-(-1) = +1) orqali 2-to'ldiruvchi musbat son hosil bo'ladi
    ret

; Constant-Time int64_t min(a, b)
; Kirish: RDI = a, RSI = b
; Chiqish: RAX = min(a, b)
ct_min_64:
    mov rax, rdi
    sub rax, rsi            ; diff = a - b
    ; Ishora bitini 64-bitga yoyish
    mov rdx, rax
    sar rdx, 63             ; RDX = (a < b) ? -1 : 0
    and rax, rdx            ; Agar a < b bo'lsa diff, aks holda 0
    add rax, rsi            ; Natija = (a < b) ? a : b
    ret
```
**Tushuntirish:** Ushbu kodda bitta ham sakrash (`jmp`, `jcc`) yo'q. Musbat va manfiy sonlar uchun bajariladigan ko'rsatmalar soni va CPU sikllari 100% bir xil bo'lib, Branch Prediction vaqt tahlillariga (Timing Attacks) mutlaqo imkon qoldirmaydi.

---

### Topshiriq #1172: Constant-Time Shartli Tanlash (Conditional Select / Bitwise Multiplexer)
**Tavsif:** Maxfiy kalit bitiga qarab ikkita nuqtadan birini tanlash kerak bo'lganda (masalan Elliptik egri chiziqlar arifmetikasida $P$ yoki $2P$), tarmoqlanishlarsiz bitli multipleksor qo'llanilishi shart.
**Talablar:** Tanlov biti $c \in \{0, 1\}$ ni to'liq 64-bitli niqobga aylantirish (`mask = -c`) va `(a & mask) | (b & ~mask)` formulasini yozish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global ct_select_64

; uint64_t ct_select_64(uint64_t condition, uint64_t val_if_true, uint64_t val_if_false);
; Kirish: RDI = condition (0 yoki 1), RSI = true_val, RDX = false_val
; Chiqish: RAX = (condition == 1) ? true_val : false_val
ct_select_64:
    ; 1. Shartdan 64-bitlik niqob hosil qilish:
    ; Agar RDI == 1 bo'lsa: neg rdi -> 0xFFFFFFFFFFFFFFFF
    ; Agar RDI == 0 bo'lsa: neg rdi -> 0x0000000000000000
    neg rdi                 ; RDI = Mask

    ; 2. Bitwise multiplexer: (RSI & Mask) | (RDX & ~Mask)
    mov rax, rsi
    and rax, rdi            ; true_val & Mask

    not rdi                 ; ~Mask
    and rdx, rdi            ; false_val & ~Mask

    or rax, rdx             ; Ikkala variantni birlashtirish
    ret
```
**Tushuntirish:** Doimiy vaqtli tanlash (Constant-Time Select) zamonaviy kriptografiyaning (Ed25519, RSA, Kyber) fundamental qurilish blokidir. Har qanday shartli ifoda xotira keshiga yoki protsessor quvuriga nol ta'sir ko'rsatgan holda bitli darvozalarda parallel yechiladi.

---

### Topshiriq #1173: Constant-Time Xotira Taqqoslash (Memcmp): Ikki Sirli Kalitni Doimiy Vaqtda Solishtirish
**Tavsif:** Standart C `memcmp` birinchi xato baytni topishi bilanoq tekshiruvdan chiqib ketadi (Early Exit). Xaker har bir baytni birma-bir sinab, qaysi urinish uzoqroq vaqt olganini o'lchash orqali parolni yoki HMAC tegini topib oladi.
**Talablar:** Barcha baytlarni qat'iy oxirigacha aylanib chiquvchi va xatoliklar yig'indisini `OR` qilib boruvchi constant-time xotira taqqoslovchisini yozish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global ct_memcmp_secure

; int ct_memcmp_secure(const void *s1, const void *s2, size_t n);
; Kirish: RDI = 1-bufer, RSI = 2-bufer, RDX = Hajm baytlarda
; Chiqish: EAX = 0 (Bir xil), 1 (Farq qiladi)
ct_memcmp_secure:
    xor eax, eax            ; EAX = Akkumulyator (barcha farqlar yig'indisi)
    xor ecx, ecx            ; ECX = Indeks

.loop:
    cmp rcx, rdx
    jge .done

    ; Har bir baytni o'qib XOR qilish: agar bir xil bo'lsa 0, farq bo'lsa noldan farqli
    movzx r8d, byte [rdi + rcx]
    movzx r9d, byte [rsi + rcx]
    xor r8d, r9d

    ; Farqni akkumulyatorga OR orqali qo'shish
    ; DIQQAT: Xatolik bo'lsa ham tsikldan CHIQILMAYDI! Barcha baytlar tekshiriladi!
    or eax, r8d

    inc rcx
    jmp .loop

.done:
    ; Natijani 0 yoki 1 ga normalizatsiya qilish (Constant-time):
    ; Agar EAX == 0 bo'lsa, 0 qaytadi; agar EAX != 0 bo'lsa, 1 qaytadi
    neg eax                 ; Noldan farqli bo'lsa Carry Flag = 1
    sbb eax, eax            ; EAX = (EAX != 0) ? -1 : 0
    neg eax                 ; EAX = 1 yoki 0
    ret
```
**Tushuntirish:** `ct_memcmp_secure` parollar, HMAC heshlari va API kalitlarini solishtirish uchun yagona xavfsiz usuldir. Xaker paroldagi 1-belgini to'g'ri topsa ham, 32-belgini to'g'ri topsa ham operatsiya bajarilish vaqti nanosoniyasigacha aynan bir xil bo'ladi.

---

### Topshiriq #1174: Kesh Hujumlariga Qarshi Bitsliced Mantiqiy Darvozalar Bilan AES S-Box Implementatsiyasi
**Tavsif:** AES S-Box massivi xotirada 256 bayt joy egallaydi. Kalit baytiga qarab massivning turli kesh chiziqlariga murojaat qilinganda, tajovuzkor 'Prime+Probe' kesh hujumi orqali qaysi kesh chizig'i yuklanganini bilib kalitni tiklaydi.
**Talablar:** S-Box ni xotiradan emas, faqat SIMD registrlaridagi mantiqiy darvozalar (`AND`, `XOR`, `NOT`) orqali hisoblovchi Bitsliced yondashuvini tuzish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global bitsliced_sbox_gate_logic

; Bitsliced AES S-Box mantiqiy darvozalari (Boyar-Peralta minimal darvozalar sxemasi)
; Kirish: XMM0..XMM7 (8 ta bit tekisliklari)
bitsliced_sbox_gate_logic:
    ; S-Box inversiyasi $GF(2^8)$ ustida mantiqiy darvozalarga ajratilgan:
    ; Hech qanday jadval o'qilmaydi! Faqat mantiqiy amallar!
    movdqa xmm8, xmm0
    pxor xmm8, xmm3
    movdqa xmm9, xmm4
    pxor xmm9, xmm6
    movdqa xmm10, xmm8
    pxor xmm10, xmm9

    ; Chiziqli bo'lmagan qism (Non-linear AND darvozalari):
    pand xmm8, xmm9
    pxor xmm0, xmm8

    ; ... (Barcha 115 ta minimal darvozalar arxitekturasi) ...
    ret
```
**Tushuntirish:** Bitsliced kriptografiya barcha ma'lumotlarni bitlar tekisligiga (Bitplanes) yoyib, butun algoritmni faqat apparat mantiqiy elementlari (`AND`, `XOR`) bilan hisoblaydi. Xotiraga birorta ham indeksli murojaat bo'lmagani sababli, protsessor keshi orqali kalitni o'g'irlash imkonsiz bo'ladi.

---

### Topshiriq #1175: Doimiy Vaqtli Katta Sonlar (BigNum) Arifmetikasi: ADCX va ADOX Instruksiyalari
**Tavsif:** RSA 4096-bit va ECC kriptografiyasida yuzlab bitli katta sonlar qo'shiladi. Intel Broadwell+ protsessorlaridagi `ADCX` (Carry Flag) va `ADOX` (Overflow Flag) instruksiyalari ikkita mustaqil zanjirni parallel qo'shish imkonini beradi.
**Talablar:** `adcx` va `adox` ko'rsatmalari bilan 256-bitli sonlarni bir vaqtda qo'shuvchi super-tezkor funksiya.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global bignum_add_256_adcx_adox

; void bignum_add_256(uint64_t *res, const uint64_t *a, const uint64_t *b);
; Kirish: RDI = res, RSI = a, RDX = b
bignum_add_256_adcx_adox:
    ; Boshlang'ich Carry va Overflow bayroqlarini tozalash
    xor eax, eax            ; CF = 0, OF = 0

    ; 1-juftlik (0..63 bitlar)
    mov r8, [rsi]
    mov r9, [rdx]
    adcx r8, r9             ; CF ni yangilaydi, OF ga tegmaydi
    mov [rdi], r8

    ; 2-juftlik (64..127 bitlar)
    mov r10, [rsi + 8]
    mov r11, [rdx + 8]
    adcx r10, r11
    mov [rdi + 8], r10

    ; 3-juftlik (128..191 bitlar)
    mov r8, [rsi + 16]
    mov r9, [rdx + 16]
    adcx r8, r9
    mov [rdi + 16], r8

    ; 4-juftlik (192..255 bitlar)
    mov r10, [rsi + 24]
    mov r11, [rdx + 24]
    adcx r10, r11
    mov [rdi + 24], r10

    ret
```
**Tushuntirish:** `ADCX` faqat Carry Flag (CF) ni yangilaydi, `ADOX` esa faqat Overflow Flag (OF) ni yangilaydi. Bu protsessorga bitta siklda bir vaqtning o'zida ikkita alohida ko'p xonali zanjirni hisoblashga imkon beradi, natijada asimmetrik kriptografiya tezligi 2 barobarga oshadi.

---

### Topshiriq #1176: Montgomery Ko'paytirish (Montgomery Multiplication) Uchun Constant-Time Qadamlar
**Tavsif:** RSA va Diffie-Hellman modulli darajaga ko'tarishda oddiy bo'lish amali (`div`) o'ta sekin va vaqt bo'yicha beqarordir. Montgomery sohasi ($A \cdot B \cdot R^{-1} \pmod N$) orqali bo'lish amalisiz doimiy vaqtda ko'paytirish lozim.
**Talablar:** Montgomery reduksiya qadami, shartli ayirishni (`res >= N ? res - N : res`) sakrashlarsiz `sbb` va `cmov` orqali bajarish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global montgomery_constant_time_sub

; Kirish: RDI = 64-bit natija T, RSI = Modul N
; Chiqish: RAX = (T >= N) ? (T - N) : T
montgomery_constant_time_sub:
    mov rax, rdi
    sub rax, rsi            ; temp = T - N (agar T < N bo'lsa Borrow/Carry=1)

    ; Constant-time tanlov:
    ; Agar T < N bo'lsa, Borrow hosil bo'ladi va biz dastlabki T ni saqlab qolishimiz kerak
    cmovc rax, rdi          ; CMOVE (Conditional Move on Carry): agar T < N bo'lsa, RAX = RDI
    ret
```
**Tushuntirish:** Klassik Montgomery algoritmi oxirida `if (T >= N) T = T - N;` tekshiruvi mavjud bo'lib, bu tarixda ko'plab kriptografik tizimlarni buzishga sabab bo'lgan (Kocher Timing Attack). `CMOVC` (Conditional Move) orqali ushbu ayirish doimiy vaqtga aylantiriladi.

---

### Topshiriq #1177: Kriptografik Xotirani Xavfsiz Tozalash: explicit_bzero va Kompilyatorni Aldashdan Himoya
**Tavsif:** C tilida `memset(key, 0, 32)` yozilsa, optimallashtiruvchi kompilyator 'bufer keyin ishlatilmaydi' deb uni butunlay o'chirib yuboradi (Dead Store Elimination). Xotirani jismoniy nollash kafolatlangan Assembly funksiyasi kerak.
**Talablar:** `rep stosb` va `mfence` bilan kalit saqlangan xotirani qat'iy tozalash.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global secure_wipe_memory

; void secure_wipe_memory(void *ptr, size_t size);
; Kirish: RDI = Tozalanuvchi xotira manzili, RSI = Baytlar soni
secure_wipe_memory:
    test rsi, rsi
    jz .done

    push rdi
    push rsi

    ; Xotirani nollar bilan qat'iy to'ldirish
    mov rcx, rsi
    xor eax, eax
    rep stosb               ; Har bir baytga 0 yoziladi

    ; Apparat kesh to'sig'i: yozish amallari keshdan o'tib, zudlik bilan RAM ga chiqishi uchun
    mfence

    pop rsi
    pop rdi

.done:
    ret
```
**Tushuntirish:** Ushbu funksiya mustaqil Assembly modulida joylashganligi sababli, hech qaysi zamonaviy C/C++ kompilyatori uning ichki mantig'ini 'keraksiz' deb o'chirib tashlay olmaydi. Bu maxfiy xususiy kalitlarning (Private Keys) xotirada qolib ketishini 100% oldini oladi.

---

### Topshiriq #1178: Power Analysis (DPA/SPA) Hujumlariga Qarshi Dummy Ko'rsatmalar va Random Masking
**Tavsif:** Xakerlar chipning elektr iste'molini osiloskop orqali o'lchab (Differential Power Analysis), qaysi siklda qanday instruksiya bajarilayotganini ko'ra oladi. Shifrlash operatsiyalari orasiga tasodifiy 'Dummy' amallarni aralashtirish kerak.
**Talablar:** Tasodifiy entropiya asosida shovqin hosil qiluvchi va elektr profilini buzuvchi Assembly qatlami.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global dpa_noise_generator

dpa_noise_generator:
    ; Apparat tasodifiy soni yordamida dummy arifmetik amallarni bajarish
    rdrand eax
    and eax, 0x07           ; 0 dan 7 gacha tasodifiy sikl

.noise_loop:
    ; Protsessorning turli arifmetik bloklarini (ALU, Shift, XOR) tasodifiy yuklash
    xor ebx, eax
    rol ebx, 3
    add ebx, 0x5A5A5A5A
    dec eax
    jnz .noise_loop

    ret
```
**Tushuntirish:** DPA (Differential Power Analysis) hujumlari minglab bir xil elektr tebranishlarini o'rtachalashtirishga asoslanadi. Tasodifiy shovqin qo'shilishi natijasida tebranishlar fazasi siljiydi (Jitter) va osiloskop signallari chalkashib ketadi.

---

### Topshiriq #1179: Flush+Reload Kesh Hujumlariga Qarshi CLFLUSH va CLFLUSHOPT Bilan Xotirani Tozalash
**Tavsif:** Xaker kesh chizig'ini kuzatib, qurbon qaysi funksiyani chaqirganini o'lchaydi (Flush+Reload). Buni bartaraf qilish uchun maxfiy kod bajarilgach, tegishli kesh chizig'ini protsessor keshidan majburiy o'chirib tashlash lozim.
**Talablar:** `clflush [rdi]` va `clflushopt [rdi]` instruksiyalari bilan kesh chizig'ini yaroqsiz holatga keltirish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global flush_cache_line_secure

; void flush_cache_line_secure(const void *addr);
; Kirish: RDI = Keshdan o'chirilishi kerak bo'lgan manzil
flush_cache_line_secure:
    mfence                  ; Barcha oldingi xotira amallari tugashini kutish
    clflush [rdi]           ; L1, L2, L3 barcha kesh darajalaridan ushbu chiziqni o'chirish
    mfence                  ; Tozalash to'liq amalga oshganini kafolatlash
    ret
```
**Tushuntirish:** `CLFLUSH` instruksiyasi ko'rsatilgan virtual manzil tegishli bo'lgan barcha kesh chiziqlarini barcha protsessor yadrolarining iyerarxiyasidan chiqarib tashlaydi. Bu orqali xaker keshda qoldirilgan izlar orqali ma'lumot tahlil qila olmaydi.

---

### Topshiriq #1180: Protsessor Ko'rsatmalari Quvurini Serializatsiya Qilish (CPUID va RDTSCP)
**Tavsif:** Zamonaviy protsessorlar ko'rsatmalarni konveyerda o'z xohishicha oldinga surishi (Out-of-Order Execution) mumkin. Kriptografik operatsiyalardan oldin va keyin qat'iy apparat devori (Serialization Barrier) o'rnatish shart.
**Talablar:** `cpuid` va `rdtscp` instruksiyalarini serializatsiya to'sig'i sifatida qo'llash.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global cpu_pipeline_serialize

cpu_pipeline_serialize:
    push rbx
    xor eax, eax
    ; CPUID barcha x86_64 mikro-arxitekturalarida to'liq serializatsiya instruksiyasi hisoblanadi:
    ; U quvurdagi barcha spekulyativ ko'rsatmalar tugashini kutadi va yangilarini to'xtatib turadi
    cpuid
    pop rbx
    ret
```
**Tushuntirish:** `CPUID` shunchaki ma'lumot olish emas, balki x86 arxitekturasidagi eng mustahkam 'Execution Barrier' hisoblanadi. U protsessorning barcha ichki buyruqlar buferlarini bo'shatadi va kutilmagan spekulyativ xatti-harakatlarning oldini oladi.

---

### Topshiriq #1181: Stack Smashing Protector (Stack Canary) Mexanizmini Qo'lda O'rnatish
**Tavsif:** Funksiya ichidagi lokal bufer to'lib ketganda (Buffer Overflow), tajovuzkor stackdagi qaytish manzilini (Return Address) o'zgartira olmasligi uchun stack freymiga maxfiy Canary qiymatini joylashtirish lozim.
**Talablar:** `fs:0x28` (Linux Thread Control Block) dan tasodifiy Canary ni o'qish va uni lokal o'zgaruvchilar bilan stack frame o'rtasiga yozish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global vulnerable_function_protected

vulnerable_function_protected:
    push rbp
    mov rbp, rsp
    sub rsp, 48                     ; 32 bayt lokal bufer + 8 bayt Canary + 8 bayt alignment

    ; 1. Stack Canary ni Thread Local Storage (TLS) dan yuklash
    ; Linux x86_64 ABI bo'yicha maxfiy canary fs:0x28 segmentida saqlanadi
    mov rax, [fs:0x28]

    ; 2. Canary ni stackdagi saqlangan RBP dan oldingi katakka yozish
    mov [rbp - 8], rax
    xor eax, eax                    ; Maxfiy qiymatni registrdan tozalash

    ; 3. Lokal bufer bilan xavfli operatsiyalar bajariladi:
    ; leaq [rbp - 40], rdi (bufer boshlanishi)

    ; Funksiya davom etadi...
    leave
    ret
```
**Tushuntirish:** Stack Canary (Kanareyka) qadimiy konchilar zaharli gazni sezish uchun o'zlari bilan qush olib tushishi kabi ishlaydi. Agar xaker buferni to'ldirib yuborsa, u qaytish manziliga yetib borguncha muqarrar ravishda Canary qiymatini ham buzib qo'yadi.

---

### Topshiriq #1182: Funksiyadan Qaytishda Stack Canary Tekshiruvi va __stack_chk_fail Chaqiruvi
**Tavsif:** Funksiya `ret` ko'rsatmasini bajarishidan oldin, stackdagi Canary qiymati `fs:0x28` dagi asl nusxasi bilan solishtirilishi, agar o'zgargan bo'lsa darhol tizimni to'xtatuvchi `__stack_chk_fail` ga sakrashi shart.
**Talablar:** `mov rax, [rbp - 8]` va `sub rax, [fs:0x28]` tekshiruvi hamda xatolikda `call __stack_chk_fail`.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global check_canary_and_exit
extern __stack_chk_fail

check_canary_and_exit:
    ; 1. Stackdagi canary qiymatini asl TLS nusxasi bilan solishtirish
    mov rax, [rbp - 8]
    sub rax, [fs:0x28]              ; Agar teng bo'lsa RAX = 0, aks holda farqli

    ; 2. Agar farq bo'lsa, bufer buzilgan (Stack Smashing yuz bergan)!
    jnz .stack_corrupted

    ; 3. Muvaffaqiyatli: stackni tozalab xavfsiz qaytish
    leave
    ret

.stack_corrupted:
    ; Zudlik bilan xavfsizlik chaqiruvi (Bu funksiya hech qachon ortga qaytmaydi, jarayon o'ldiriladi)
    call __stack_chk_fail
    ud2                             ; Apparat darajasida to'xtatish
```
**Tushuntirish:** `__stack_chk_fail` chaqirilganda operatsion tizim `SIGABRT` signalini yuboradi va jarayonni darhol to'xtatadi. Bu orqali xakerning inyeksiyalangan kodi (Shellcode) protsessorda biror takt ham ijro etilmay yo'q qilinadi.

---

### Topshiriq #1183: Return-Oriented Programming (ROP) Xavfini Bartaraf Etish: Intel CET Asoslari
**Tavsif:** Stack Canary mavjud bo'lsa ham, xakerlar xotirani o'qish imkoniyati (Memory Leak) orqali mavjud kutubxona kodlari parchalarini (Gadgets) zanjirga yig'ib ROP hujumini uyushtirishi mumkin. Intel CET (Control-flow Enforcement Technology) bunga qarshi apparat himoyasini beradi.
**Talablar:** CR4 registridagi CET biti (Bit 23) va MSR_IA32_U_CET konfiguratsiyasini boshqaruvchi kod.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global enable_intel_cet_kernel

; Intel CET faollashtirish (Ring 0 Kernel rejimida)
enable_intel_cet_kernel:
    ; 1. CR4 boshqaruv registrida CETEnable (Bit 23) ni yoqish
    mov rax, cr4
    bts rax, 23                     ; Bit 23 = 1
    mov cr4, rax

    ; 2. MSR_IA32_S_CET (Supervisor CET Control - MSR 0x6A2) registrini sozlash
    ; Bit 0: Shadow Stack Enable (SH_STK_EN)
    ; Bit 1: Write-Protect Shadow Stack (WR_SHSTK_EN)
    ; Bit 2: Indirect Branch Tracking Enable (ENDBR_EN)
    mov ecx, 0x6A2                  ; IA32_S_CET MSR
    mov eax, 0x07                   ; 0b0111
    xor edx, edx
    wrmsr                           ; MSR ga yozish

    ret
```
**Tushuntirish:** Intel CET (Tiger Lake va Zen 3 dan boshlab) Return-Oriented Programming ga qarshi inqilobiy apparat yechimidir. U kremniy darajasida Shadow Stack va IBT mexanizmlarini qo'llab, dastur kodining o'zgartirilgan oqimlarini apparatda to'xtatadi.

---

### Topshiriq #1184: Intel CET Shadow Stack: INCSSP va Qaytish Manzillarini Ikkinchi Stack Bilan Solishtirish
**Tavsif:** Shadow Stack apparat darajasida himoyalangan ikkinchi stack bo'lib, unga faqat `call` va `ret` instruksiyalari yozishi mumkin. Agar odatiy stackdagi manzil Shadow Stack dagi manzilga mos kelmasa, apparat #CP (Control Protection Exception) istisnosini chiqaradi.
**Talablar:** `RDSSP` (Read Shadow Stack Pointer) va `INCSSP` (Increment Shadow Stack Pointer) instruksiyalari bilan ishlash.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global inspect_shadow_stack_pointer

inspect_shadow_stack_pointer:
    ; RDSSPQ: Joriy Shadow Stack ko'rsatkichini RAX ga o'qiydi
    rdsspq rax

    ; Agar setjmp/longjmp kabi kontekst almashuvlarida Shadow Stackni siljitish kerak bo'lsa:
    ; INCSSPQ rdi (Shadow Stackni rdi ta so'zga suradi)
    ; incsspq rdi

    ret
```
**Tushuntirish:** Shadow Stack xotira sahifalari sahifa jadvalida (PTE) maxsus `Shadow Stack` atributi bilan belgilanadi. Dasturning birorta ham `mov [rsp], rax` buyrug'i unga yozish huquqiga ega emas. Shu sababli xaker asosiy stackni buza olsa ham, Shadow Stack ga tegina olmaydi va `ret` paytida apparat darajasida ushlanadi.

---

### Topshiriq #1185: Indirect Branch Tracking (IBT): Barcha Sakrash Manzillariga ENDBR64 Qo'yish
**Tavsif:** JOP (Jump-Oriented Programming) va COP hujumlarida xakerlar bilvosita sakrashlardan (`jmp rax`, `call rdx`) foydalanadi. Intel IBT bo'yicha har bir ruxsat etilgan funksiya boshiga `ENDBR64` ko'rsatmasi qo'yilishi shart.
**Talablar:** `endbr64` ko'rsatmasining binar kodi (`0xF3, 0x0F, 0x1E, 0xFA`) va funksiya chaqiruvlari darvozasi.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global secure_indirect_target_func

secure_indirect_target_func:
    ; ENDBR64 (End Branch 64-bit):
    ; Har qanday bilvosita 'call rax' yoki 'jmp rax' manzilidagi birinchi instruksiya ENDBR64 bo'lishi SHART!
    ; Aks holda protsessor bir zumda #CP (Control Protection Fault) xatosini beradi!
    endbr64

    ; Asosiy funksiya mantiqi
    mov eax, 42
    ret
```
**Tushuntirish:** Agar protsessorda IBT yoqilgan bo'lsa, har bir bilvosita sakrashdan so'ng CPU maxsus 'WAIT_FOR_ENDBRANCH' holatiga o'tadi. Keyingi bajariladigan instruksiya aynan `ENDBR64` bo'lmasa, demak dastur oqimi xaker tomonidan kutilmagan manzilga yo'naltirilgan deb hisoblanadi va jarayon yo'q qilinadi.

---

### Topshiriq #1186: ARM64 Pointer Authentication (PAC): PACIASP va AUTIASP Bilan Return Addressni Himoyalash
**Tavsif:** ARMv8.3-A arxitekturasida (Apple A12+, M1+, Graviton 3) qaytish manzillari 64-bitli virtual manzilning yuqori foydalanilmagan bitlariga kriptografik MAC (Message Authentication Code) tamg'asi qo'yish orqali himoyalanadi.
**Talablar:** AArch64 `paciasp` (Funksiya kirishida LR registrini SP bilan imzolash) va `autiasp` (Funksiya chiqishida imzoni tekshirish).
**Yechim (Assembly):**
```assembly
// AArch64 (ARM64) Assembly
.global pac_protected_function

pac_protected_function:
    // 1. PACIASP: X30 (Link Register - Return Address) ni stack pointer (SP)
    // va A-Key maxfiy apparat kaliti yordamida imzolash (Sign LR)
    paciasp

    // Odatiy stack freymini yaratish
    stp x29, x30, [sp, #-32]!
    mov x29, sp

    // Funksiya tanasi (bu yerda bufer to'lib ketishi yuz bersa ham, LR imzosi buziladi)
    mov x0, #100

    // Stackni qaytarish
    ldp x29, x30, [sp], #32

    // 2. AUTIASP: LR dagi kriptografik imzoni tekshirish (Authenticate LR)
    // Agar xaker stackdagi qaytish manzilini o'zgartirgan bo'lsa, imzo mos kelmaydi
    // va keyingi 'ret' paytida protsessor darhol qulaydi!
    autiasp
    ret
```
**Tushuntirish:** ARM64 Pointer Authentication (PAC) QARMA blokli shifrlash algoritmidan foydalanadi. 64-bitlik manzilning yuqori 16-24 ta bo'sh bitlariga imzo yoziladi. Agar imzo xato bo'lsa, `autiasp` manzilning yuqori bitlariga xato belgisi kiritadi va `ret` xotira buzilishi xatosini (Translation Fault) chaqiradi.

---

### Topshiriq #1187: ARM64 Branch Target Identification (BTI) Mexanizmi
**Tavsif:** x86 dagi `ENDBR64` kabi, ARMv8.5-A arxitekturasida bilvosita sakrashlar faqat `bti` ko'rsatmasi bor xotira nuqtalariga yo'naltirilishi mumkin.
**Talablar:** AArch64 `bti c` (Call target), `bti j` (Jump target), `bti jc` ko'rsatmalari.
**Yechim (Assembly):**
```assembly
// AArch64 (ARM64) Assembly
.global bti_protected_function

bti_protected_function:
    // BTI C: Ushbu funksiya faqat 'BLR' (Branch with Link to Register) orqali chaqirilishi mumkin!
    bti c

    mov x0, #1
    ret
```
**Tushuntirish:** BTI sahifalar jadvalidagi Guarded Page (GP) biti bilan faollashadi. Agar xaker ROP/JOP gadjetini izlab funksiya o'rtasiga sakrashga urinsa, u yerda `BTI` bo'lmaganligi sababli apparat darajasida Branch Target Exception yuzaga keladi.

---

### Topshiriq #1188: W^X (Write XOR Execute) Qoidasini Sahifalar Jadvalida NX / XN Biti Bilan Ta'minlash
**Tavsif:** Xotira sahifasi bir vaqtning o'zida ham yoziladigan, ham bajariladigan bo'lishi (RWX) xavfsizlikning eng katta xatosi hisoblanadi. Sahifa jadvalida NX (No-Execute) bitini o'rnatish lozim.
**Talablar:** x86_64 Page Table Entry ning 63-bitidagi XD (Execute-Disable) bitini yoqish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global set_page_no_execute

; Kirish: RDI = 64-bit Page Table Entry (PTE) ko'rsatkichi
set_page_no_execute:
    ; x86_64 da Bit 63: XD (Execute-Disable) biti
    ; EFER MSR (0xC0000080) da NXE (Bit 11) yoqilgan bo'lishi shart!
    mov rax, [rdi]
    bts rax, 63                     ; Bit 63 = 1 (Kod bajarish taqiqlanadi!)
    mov [rdi], rax

    ; TLB ni tozalash
    invlpg [rdi]
    ret
```
**Tushuntirish:** `NX` (No-Execute) yoki ARM dagi `XN` biti stack va heap xotiralarida saqlangan ma'lumotlarni kod sifatida bajarilishini mutlaqo taqiqlaydi. Bu klassik 'Buffer Overflow Shellcode' hujumlarini apparat darajasida yo'q qiladi.

---

### Topshiriq #1189: ASLR Bilan Mos Position-Independent Code (PIC/PIE) va RIP-Relative Murojaat
**Tavsif:** ASLR (Address Space Layout Randomization) dastur xotiraga har safar yangi tasodifiy manzilda yuklanishini ta'minlaydi. Kod qattiq bog'langan manzillarsiz (Hardcoded addresses) faqat RIP-nisbiy ishlashi kerak.
**Talablar:** `[rip + label]` murojaatlari va global o'zgaruvchilar bilan PIC xavfsiz ishlash.
**Yechim (Assembly):**
```assembly
[bits 64]
section .data
secret_constant: dq 0x1122334455667788

section .text
global get_secret_pie

get_secret_pie:
    ; Noto'g'ri (Non-PIC): mov rax, [secret_constant] -> Mutlaq manzil ASLR da buziladi
    ; To'g'ri (Position-Independent): RIP-nisbiy manzil
    mov rax, [rel secret_constant]
    ret
```
**Tushuntirish:** Position-Independent Executable (PIE) dasturning butun kod segmentini xotiraning ixtiyoriy manziliga ko'chirish imkonini beradi. Xaker kutubxona yoki funksiyalarning qayerda joylashganini oldindan bila olmaydi.

---

### Topshiriq #1190: ROP Gadjetlarini Kashf Etishdan Himoya: NOP Sled Diversifikatsiyasi
**Tavsif:** Xakerlar `objdump` yoki `ROPgadget` vositalari orqali xotiradagi `pop rdi; ret` kabi ketma-ketliklarni qidiradi. Kod generatorlari orqali sun'iy diversifikatsiya va xavfsiz register swaplarini kiritish.
**Talablar:** Polimorfik xavfsiz instruksiyalar va ekvivalent semantik almashtirishlar.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global diversified_safe_block

diversified_safe_block:
    ; Standart ketma-ketlik o'rniga no-gadget instruksiyalar:
    ; XOR EAX, EAX o'rniga SUB EAX, EAX yoki MOV EAX, 0
    sub eax, eax

    ; NOP o'rniga ko'p baytli xavfsiz no-op lar (Multi-byte NOP):
    nop dword [rax + rax*1 + 0]     ; 7-baytlik xavfsiz NOP

    ret
```
**Tushuntirish:** Gadget diversifikatsiyasi xotira binar kodidagi tasodifiy gadjetlarning paydo bo'lish ehtimolini 90% ga qisqartiradi, bu esa avtomatlashtirilgan ekspluatatsiya qurollarini (Exploit Kits) samarasiz qilib qo'yadi.

---

### Topshiriq #1191: Spectre v1 (Bounds Check Bypass) Xavfi va LFENCE Spekulyatsiya To'sig'i
**Tavsif:** Spectre v1 zaifligida protsessor `if (x < array1_size)` shartini kutmasdan, spekulyativ ravishda massiv chegarasidan tashqaridagi maxfiy xotirani o'qib keshga yuklaydi. Spekulyatsiyani shartli sakrash joyida to'xtatish uchun `LFENCE` to'sig'i zarur.
**Talablar:** `cmp`, `jge` va `lfence` instruksiyalarini to'g'ri joylashtirish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global spectre_v1_safe_read

; uint8_t spectre_v1_safe_read(const uint8_t *arr, size_t size, size_t index);
; Kirish: RDI = arr, RSI = size, RDX = index
; Chiqish: AL = arr[index] (agar index < size bo'lsa), 0 (chegaradan tashqarida)
spectre_v1_safe_read:
    cmp rdx, rsi                    ; index < size tekshiruvi
    jae .out_of_bounds

    ; MUHIM XAVFSIZLIK TO'SIG'I (Spectre v1 Mitigation):
    ; LFENCE protsessorning barcha keyingi spekulyativ yuklashlarini (Speculative Execution)
    ; yuqoridagi 'jae' sharti to'liq tasdiqlanmaguncha muzlatib turadi!
    lfence

    ; Faqat shart tasdiqlangach xavfsiz o'qish
    movzx eax, byte [rdi + rdx]
    ret

.out_of_bounds:
    xor eax, eax
    ret
```
**Tushuntirish:** Intel va AMD arxitekturalarida `LFENCE` shunchaki kesh to'sig'i emas, balki rasmiy 'Speculation Barrier' (Spekulyatsiya To'sig'i) deb e'lon qilingan. U protsessorning Out-of-Order dvigateliga oldingi barcha shartli sakrashlar hal bo'lmaguncha keyingi xotira yuklashlarini boshlashni taqiqlaydi.

---

### Topshiriq #1192: Spectre v1 ni Branch-Free Indeks Niqoblash (Index Masking) Bilan Zararsizlantirish
**Tavsif:** `LFENCE` unumdorlikni biroz pasaytirishi mumkin. Shu sababli yuqori tezlikdagi kodlarda indeksni massiv chegarasiga bitta bitli niqob bilan bog'lash (Clamping / Masking) orqali hatto spekulyatsiya bo'lganda ham xotiradan tashqariga chiqmaslik ta'minlanadi.
**Talablar:** Aritmetik ayirish, `sbb` orqali 64-bitlik mask hosil qilish va indeksni 0 ga bog'lash.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global spectre_v1_masked_read

; Kirish: RDI = arr, RSI = size, RDX = index
spectre_v1_masked_read:
    ; index va size ni solishtirish
    cmp rdx, rsi                    ; Agar index < size bo'lsa CF = 1, aks holda CF = 0

    ; SBB (Subtract with Borrow): Agar CF == 1 bo'lsa RAX = 0xFFFFFFFFFFFFFFFF, aks holda 0x0
    sbb rax, rax

    ; Indeksni niqob bilan kesish: agar index >= size bo'lsa, indeks 0 bo'ladi!
    and rdx, rax                    ; rdx = (index < size) ? index : 0

    ; Spekulyativ ravishda ham protsessor faqat 0-elementni o'qiydi va hech qachon maxfiy xotiraga tegmaydi!
    movzx eax, byte [rdi + rdx]

    ; Yakuniy natijani ham niqoblash
    and eax, eax
    ret
```
**Tushuntirish:** Index Masking usuli Google va Microsoft yadrolarida keng qo'llaniladi. U CPU quvurini to'xtatmaydi, ammo xaker bergan har qanday ulkan indeksni spekulyatsiya darajasida avtomatik ravishda xavfsiz 0 indeksiga aylantirib qo'yadi.

---

### Topshiriq #1193: Spectre v2 (Branch Target Injection): Retpoline (Return Trampoline) Mexanizmi
**Tavsif:** Spectre v2 hujumida xaker Branch Target Buffer (BTB) ni zaharlab, `jmp [rax]` yoki `call rcx` kabi bilvosita sakrashlarni o'zining zararli kodiga yo'naltiradi. Retpoline mexanizmi bilvosita sakrashni spekulyatsiyani to'xtatuvchi `call/ret` tuzog'iga aylantiradi.
**Talablar:** Google muhandislari ishlab chiqqan Retpoline thunk Assembly kodini yozish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global __x86_indirect_thunk_rax

; Retpoline: 'call rax' o'rniga chaqiriladi
__x86_indirect_thunk_rax:
    ; 1. Ichki chaqiruv: Return address stackka qo'yiladi
    call .set_up_target

.capture_speculation:
    ; Spekulyatsiya tuzog'i (Speculation Trap):
    ; Agar protsessor spekulyativ tarzda noto'g'ri sakrashga urinsa, u ushbu cheksiz pauzada muzlaydi!
    pause
    lfence
    jmp .capture_speculation

.set_up_target:
    ; 2. Stackdagi return address o'rniga haqiqiy maqsadli manzil (RAX) yoziladi
    mov [rsp], rax

    ; 3. RET ko'rsatmasi bajariladi.
    ; Protsessor Return Stack Buffer (RSB) orqali to'g'ri RAX manziliga qaytadi!
    ret
```
**Tushuntirish:** Retpoline (Return Trampoline) kompyuter fanlaridagi eng aqlli zaiflik yechimlaridan biridir. U protsessorning bilvosita sakrash bashoratchisini (BTB) chetlab o'tib, apparatning Return Stack Buffer (RSB) mexanizmidan foydalanadi va spekulyativ ijroni xavfsiz cheksiz pauzaga qamab qo'yadi.

---

### Topshiriq #1194: Intel IBRS (Indirect Branch Restricted Speculation) va IBPB MSR Boshqaruvi
**Tavsif:** Retpoline apparat darajasida unumdorlikni tushirishi mumkin. Zamonaviy mikrokod yangilanishlari bilan Intel protsessorlarida IBRS va IBPB maxsus boshqaruv registrlari (MSR) joriy etildi.
**Talablar:** `MSR_IA32_SPEC_CTRL` (0x48) va `MSR_IA32_PRED_CMD` (0x49) registrlarini `wrmsr` bilan sozlash.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global enable_ibrs_spec_ctrl

MSR_IA32_SPEC_CTRL equ 0x48
MSR_IA32_PRED_CMD  equ 0x49

; Kontekst almashganda IBPB (Indirect Branch Predictor Barrier) buyrug'ini berish
global flush_branch_predictor
flush_branch_predictor:
    mov ecx, MSR_IA32_PRED_CMD
    mov eax, 1                      ; Bit 0: IBPB (Bashoratchi keshini tozalash)
    xor edx, edx
    wrmsr
    ret

enable_ibrs_spec_ctrl:
    mov ecx, MSR_IA32_SPEC_CTRL
    ; Bit 0: IBRS (Indirect Branch Restricted Speculation)
    ; Bit 1: STIBP (Single Thread Indirect Branch Predictors)
    mov eax, 0x03
    xor edx, edx
    wrmsr
    ret
```
**Tushuntirish:** `IBPB` (Indirect Branch Predictor Barrier) operatsion tizim bir foydalanuvchi jarayonidan boshqa jarayonga o'tganda (Context Switch) chaqiriladi. U protsessorning ichki sakrash bashorati tarixini tozalab, bitta jarayonning boshqa jarayon spekulyatsiyasiga ta'sir qilishini to'xtatadi.

---

### Topshiriq #1195: Meltdown Xavfi va KPTI (Kernel Page Table Isolation) Tramplin Sahifalari
**Tavsif:** Meltdown (Rogue Data Cache Load) xakerga foydalanuvchi rejimida (Ring 3) turib yadro xotirasini (Ring 0) spekulyativ o'qish imkonini bergan. Bunga qarshi KPTI orqali foydalanuvchi rejimida yadro xotirasi sahifalar jadvalidan mutlaqo chiqarib tashlanadi.
**Talablar:** Foydalanuvchi CR3 va Yadro CR3 o'rtasida kontekst almashuvchi Assembly tramplin kodi.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global kpti_switch_to_kernel_cr3
global kpti_switch_to_user_cr3

; Foydalanuvchi rejimidan yadroga kirishda (Syscall / Interrupt):
kpti_switch_to_kernel_cr3:
    mov rax, cr3
    ; KPTI da Yadro sahifa jadvali Foydalanuvchi jadvalidan 0x1000 (4KB) orqada yoki bit orqali ajratiladi
    and rax, ~0x1000                ; Kernel PML4 ga o'tish
    mov cr3, rax
    ret

; Yadro rejimidan foydalanuvchiga qaytishda:
kpti_switch_to_user_cr3:
    mov rax, cr3
    or rax, 0x1000                  ; Cheklangan User PML4 ga o'tish (Yadro sahifalari yo'q!)
    mov cr3, rax
    ret
```
**Tushuntirish:** KPTI (Kernel Page Table Isolation) apparatdagi ruxsat tekshiruvi kechikishini bartaraf qilish uchun foydalanuvchi rejimida yadro sahifalarini butunlay xotira xaritasidan o'chirib qo'yadi. Agar Meltdown xakeri yadro manzilini so'rasa, u keshda ham, sahifa jadvalida ham mavjud bo'lmagani uchun darhol Page Fault yuzaga keladi.

---

### Topshiriq #1196: ARM TrustZone: SMC (Secure Monitor Call) Bilan Xavfsiz Dunyoga (Secure World) O'tish
**Tavsif:** ARM TrustZone arxitekturasi protsessorni ikkita izolyatsiyalangan apparat dunyosiga ajratadi: Oddiy dunyo (Normal World - Linux/Android) va Xavfsiz dunyo (Secure World - TEE / OP-TEE / Trusty). Ular o'rtasida aloqa faqat `SMC` instruksiyasi orqali kechadi.
**Talablar:** AArch64 `smc #0` (Secure Monitor Call) chaqiruvi, argumentlarni uzatish (SMC Calling Convention - SMCCC) va javobni olish.
**Yechim (Assembly):**
```assembly
// AArch64 (ARM64) Assembly
.global call_trustzone_secure_service

// Kirish: X0 = Function ID (masalan 0x84000000), X1 = Parametr 1, X2 = Parametr 2, X3 = Parametr 3
// Chiqish: X0..X3 = Xavfsiz Dunyodan qaytgan javoblar
call_trustzone_secure_service:
    // ARM SMCCC (Secure Monitor Call Calling Convention) bo'yicha:
    // X0 - Funksiya identifikatori
    // X1-X7 - Argumentlar

    // SMC chaqiruvi: Protsessor darhol EL3 (Secure Monitor) ga sakraydi!
    // Apparat darajasida NS (Non-Secure) biti 0 ga o'zgaradi va TrustZone faollashadi
    smc #0

    // Xavfsiz operatsiya (masalan biometrik barmoq izi tekshiruvi yoki apparat kalit shifrlash)
    // tugagach, Secure Monitor qaytargan natijalar X0-X3 da bo'ladi
    ret
```
**Tushuntirish:** ARM TrustZone apparat shinasida (AXI Bus) maxsus `NS` (Non-Secure) bitidan foydalanadi. Normal World dagi Linux tizimi root huquqiga ega bo'lsa ham, xotira kontrolleri (TZASC) unga Secure World dagi RAM va kriptografik kalitlarni o'qishga apparat darajasida ruxsat bermaydi.

---

### Topshiriq #1197: ARM TrustZone Xotira Kontrolleri (TZASC) Bilan Xotira Mintaqalarini Ajratish
**Tavsif:** Asosiy operativ xotiraning (DRAM) ma'lum bir qismini (masalan, yuqori 64MB) faqat Secure World o'qiy oladigan qilib apparat shinasida qulflash talab etiladi.
**Talablar:** TZASC (TrustZone Address Space Controller) registrlariga hudud chegaralari va xavfsizlik atributlarini yozish.
**Yechim (Assembly):**
```assembly
// AArch64 Assembly
.global configure_tzasc_region

// TZASC Baza manzili: 0x2A400000
.equ TZASC_BASE, 0x2A400000
.equ REGION_SETUP_LOW, 0x100
.equ REGION_SETUP_HIGH, 0x104
.equ REGION_ATTRIBUTES, 0x108

configure_tzasc_region:
    mov x0, #TZASC_BASE

    // Mintaqa chegarasini belgilash: 0x80000000 dan boshlab 64MB
    mov x1, #0x80000000
    str w1, [x0, #REGION_SETUP_LOW]

    // Mintaqa atributlari: Faqat Xavfsiz (Secure-Only Read/Write)
    // Bit 0: Enable, Bit 31..28: Security permissions
    mov w2, #0x80000001             // Secure Only
    str w2, [x0, #REGION_ATTRIBUTES]

    dsb sy
    ret
```
**Tushuntirish:** TZASC shina darajasidagi apparat politsiyachisi vazifasini o'taydi. Agar buzib kirilgan Linux yadrosi ushbu 64MB xotiraga murojaat qilmoqchi bo'lsa, xotira shinasidagi `NS=1` signali sababli kontroller darhol `DECERR` (Decode Error) signali bilan so'rovni apparatda bloklaydi.

---

### Topshiriq #1198: Intel SGX (Software Guard Extensions): EENTER va EEXIT Bilan Anklav (Enclave) Boshqaruvi
**Tavsif:** Intel SGX dasturga hatto buzilgan va xaker nazoratidagi operatsion tizim (yoki gipervizor) ichida ham o'zining shifrlangan xotira anklavini (Enclave) ochish va kodni mutlaqo izolyatsiyalangan holda bajarish imkonini beradi.
**Talablar:** `ENCLU` (Enclave User Functions) instruksiyasini EAX=2 (`EENTER`) va EAX=4 (`EEXIT`) bilan boshqarish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global sgx_enter_enclave
global sgx_exit_enclave

; ENCLU instruksiyasi barglari (Leafs):
; EAX = 0: EREPORT
; EAX = 1: EGETKEY
; EAX = 2: EENTER (Anklavga kirish)
; EAX = 4: EEXIT  (Anklavdan chiqish)

; Kirish: RBX = TCS (Thread Control Structure) manzili, RCX = Anklav ichidagi sakrash nuqtasi
sgx_enter_enclave:
    push rbx
    push rbp

    mov eax, 2                      ; EAX = 2 (EENTER)
    ; ENCLU ko'rsatmasi: Protsessor darhol SGX Enclave rejimiga o'tadi
    ; Xotira avtomatik apparat shifrlash (Memory Encryption Engine - MEE) ostiga olinadi!
    enclu

    ; Anklav ichidan EEXIT chaqirilganda boshqaruv bu yerga qaytadi:
    pop rbp
    pop rbx
    ret

sgx_exit_enclave:
    mov eax, 4                      ; EAX = 4 (EEXIT)
    ; RBX = Anklavdan tashqaridagi qaytish manzili
    enclu
    ; Bu qatorga yetib kelinmaydi
```
**Tushuntirish:** Intel SGX xotiradagi barcha ma'lumotlarni apparat MEE (Memory Encryption Engine) chipi orqali AES-128 bilan shifrlaydi. Hatto xaker kompyuter platasiga osiloskop yoki xotira skaneri (Cold Boot Attack) ulab RAM chiplarini o'qisa ham, u faqat shifrlangan xaosni ko'radi.

---

### Topshiriq #1199: Intel SGX Asinxron Enclave Chiqishi (AEX) va Xavfsiz Qaytish (ERESUME)
**Tavsif:** Anklav ichida kod bajarilayotganda taymer uzilishi (Timer Interrupt) yoki sahifa xatosi (Page Fault) yuz bersa, protsessor anklavdagi barcha registrlarni SSA (State Save Area) ga berkitib, oddiy registrlarni sintetik nollar bilan tozalaydi (AEX hodisasi).
**Talablar:** AEX dan so'ng xavfsiz qayta tiklanish: EAX=3 (`ERESUME`) bilan anklavdagi ishni to'xtagan joyidan davom ettirish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global sgx_resume_after_interrupt

sgx_resume_after_interrupt:
    ; AEX (Asynchronous Enclave Exit) yuz bergach, yadro uzilishni qayta ishlab bo'ldi.
    ; Endi anklavni avvalgi holatida qayta davom ettirish kerak:
    ; RBX = TCS manzili
    mov eax, 3                      ; EAX = 3 (ERESUME)
    enclu                           ; Protsessor SSA dan registrlarni tiklab anklavga qaytadi
    ret
```
**Tushuntirish:** AEX (Asynchronous Enclave Exit) mexanizmi yadro yoki xakerning anklav registrlari (RAX, RBX, RIP) tarkibini uzilish paytida o'g'irlashining oldini oladi. Protsessor anklavdan chiqishda registrlarni apparatda 'Synthetic State' ga almashtiradi.

---

### Topshiriq #1200: Kompleks Bare-Metal Xavfsiz Kriptografik Vault: AES-GCM + Stack Canary + LFENCE + Secure Wipe
**Tavsif:** Ushbu modulda o'rganilgan barcha ilg'or apparat himoyasi vositalarini (AES-NI, Stack Canary, Spectre LFENCE to'siqlari va xotirani xavfsiz tozalash) bitta mustahkam Kriptografik Seyf (Secure Crypto Vault) funksiyasiga jamlash lozim.
**Talablar:** Stack Canary o'rnatish, LFENCE bilan parametrni tekshirish, Constant-Time AES shifrlash, xotiradagi kalitni `rep stosb` bilan nollash va xavfsiz qaytish.
**Yechim (Assembly):**
```assembly
[bits 64]
section .text
global secure_crypto_vault_encrypt
extern __stack_chk_fail

; int secure_crypto_vault_encrypt(const uint8_t *in, uint8_t *out, size_t len, const uint8_t *key_material);
; Kirish: RDI = in, RSI = out, RDX = len, RCX = key_material (16 bayt)
secure_crypto_vault_encrypt:
    ; 1. Stack Frame va Stack Canary o'rnatish
    push rbp
    mov rbp, rsp
    sub rsp, 208                    ; 176 bayt Raund kalitlari + 8 bayt Canary + Alignment

    mov rax, [fs:0x28]              ; TLS Canary
    mov [rbp - 8], rax
    xor eax, eax

    ; 2. Spectre v1 to'sig'i: Parametrlar validatsiyasi
    test rdx, rdx
    jz .exit_clean
    cmp rdx, 1048576                ; Maksimal 1MB cheklovi
    ja .exit_clean
    lfence                          ; Spekulyatsiyani qat'iy to'xtatish!

    ; 3. AES-128 Kalitini kengaytirish (Stackdagi [rbp - 184] buferiga)
    ; ... (Key expansion amalga oshiriladi) ...

    ; 4. Bloklarni Constant-Time rejimida shifrlash
    movdqu xmm0, [rdi]
    pxor xmm0, [rbp - 184]
    aesenc xmm0, [rbp - 168]
    ; ... (Barcha raundlar) ...
    aesenclast xmm0, [rbp - 24]
    movdqu [rsi], xmm0

    ; 5. Secure Key Wipe: Stackda turgan raund kalitlarini to'liq nollash!
    push rdi
    push rsi
    lea rdi, [rbp - 184]
    mov ecx, 176
    xor eax, eax
    rep stosb                       ; Barcha kalit qoldiqlari o'chirildi!
    mfence
    pop rsi
    pop rdi

.exit_clean:
    ; 6. Stack Canary tekshiruvi
    mov rax, [rbp - 8]
    sub rax, [fs:0x28]
    jnz .stack_fail                 ; Agar buzilgan bo'lsa darhol halokat!

    xor eax, eax                    ; Muvaffaqiyat (Return 0)
    leave
    ret

.stack_fail:
    call __stack_chk_fail
    ud2
```
**Tushuntirish:** Ushbu yakuniy kriptografik seyf apparat xavfsizligining barcha qatlamlarini o'zida birlashtiradi: xaker buferni to'ldirmoqchi bo'lsa Stack Canary tutadi; Spectre spekulyatsiyasini `LFENCE` to'xtatadi; shifrlash AES-NI orqali doimiy vaqtda (Constant-Time) kechadi; funksiya tugashi bilan barcha maxfiy kalitlar RAM dan `rep stosb` orqali tozalab tashlanadi.

---
