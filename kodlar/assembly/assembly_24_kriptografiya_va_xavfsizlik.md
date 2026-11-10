# Khorazmiy AI: Assembly - Modul 24
## Mavzu: Kiberxavfsizlik, Kriptografiya (AES, RSA, ECC) va Xavfsiz Kodlash

### Topshiriq #1151: AES S-Box Substitutsiya Operatsiyasi
**Tavsif:** AES algoritmining asosiy bosqichi bo'lgan SubBytes uchun S-Box jadvalidan qiymat olish. Kriptografik tizimlarda xotiraga kirish vaqtini (timing attack) minimallashtirish zarur.
**Talablar:** S-Box jadvalidan indeks bo'yicha qiymatni xavfsiz va tezkor olish.
**Yechim (Assembly):**
```assembly
section .data
    sbox db 0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5 ; Qisqartirilgan jadval
section .text
    ; AL registrida kirish bayti bor deb faraz qilamiz
    movzx eax, al          ; Indeksni tozalash
    mov al, [sbox + eax]   ; S-Box qiymatini olish
```
**Tushuntirish:** `movzx` ko'rsatmasi orqali yuqori bitlardagi "axlat" ma'lumotlar tozalanadi, bu esa xavfsizlik va aniqlikni ta'minlaydi.

### Topshiriq #1152: Xavfsiz Xotira Tozalash (Zeroing)
**Tavsif:** Maxfiy kalitlar (keys) xotiradan o'chirilganda, ularning qoldiqlarini yo'q qilish.
**Talablar:** `rep stosb` yordamida xotirani nolga tenglash.
**Yechim (Assembly):**
```assembly
    mov edi, key_buffer    ; Kalit manzili
    mov ecx, 32            ; 32 baytli AES-256 kaliti
    xor eax, eax           ; EAX = 0
    rep stosb              ; Xotirani tozalash
```
**Tushuntirish:** `rep stosb` protsessor darajasida optimallashtirilgan bo'lib, xotirani eng tezkor tozalash usulidir.

### Topshiriq #1153: RSA Modulo Ko'paytirish (Montgomery)
**Tavsif:** Katta sonlar bilan ishlashda modulli ko'paytirishni amalga oshirish.
**Talablar:** 64-bitli registrlarda `mul` operatsiyasidan foydalanish.
**Yechim (Assembly):**
```assembly
    mov rax, [val1]
    mul qword [val2]       ; RDX:RAX = val1 * val2
    div qword [modulus]    ; Qoldiqni olish
```
**Tushuntirish:** `div` operatsiyasi qimmat bo'lgani uchun, real tizimlarda Montgomery reduksiyasi ishlatiladi, bu yerda asosiy mantiq ko'rsatilgan.

### Topshiriq #1154: ECC Nuqta Qo'shish (Point Addition)
**Tavsif:** Elliptik egri chiziqlar kriptografiyasida nuqtalarni qo'shish.
**Talablar:** Koordinatalar ustida modulli arifmetika.
**Yechim (Assembly):**
```assembly
    add rax, rbx           ; X1 + X2
    sub rax, rcx           ; Modulo operatsiyasi uchun ayirish
    cmp rax, [prime]       ; Prime dan katta bo'lsa
    jbe .done
    sub rax, [prime]       ; Modulo reduksiyasi
.done:
```
**Tushuntirish:** `jbe` (jump if below or equal) shartli o'tishi orqali "branch prediction" optimizatsiyasi amalga oshiriladi.

### Topshiriq #1155: XOR-based Stream Cipher
**Tavsif:** Ma'lumotlarni oqimli shifrlash uchun XOR operatsiyasidan foydalanish.
**Talablar:** Kalit oqimi (keystream) bilan ma'lumotni birlashtirish.
**Yechim (Assembly):**
```assembly
    mov rcx, 16            ; 16 baytli blok
.loop:
    mov al, [data + rcx]
    xor al, [key + rcx]    ; XOR shifrlash
    mov [data + rcx], al
    loop .loop
```
**Tushuntirish:** XOR operatsiyasi simmetrik bo'lib, shifrlash va deshifrlash uchun bir xil kod ishlatiladi.

### Topshiriq #1156: Stack Canary Himoyasi
**Tavsif:** Buffer overflow hujumlaridan himoya qilish uchun stekka "canary" qiymatini qo'yish.
**Talablar:** Funksiya boshida va oxirida qiymatni tekshirish.
**Yechim (Assembly):**
```assembly
    mov rax, [canary_val]
    mov [rbp-8], rax       ; Canary o'rnatish
    ; ... funksiya tanasi ...
    cmp [rbp-8], rax       ; Canary o'zgarganmi?
    jne .security_alert    ; Agar o'zgargan bo'lsa, xatolik
```
**Tushuntirish:** Bu usul stekdagi qaytish manzilini (return address) himoya qilishning standartidir.

### Topshiriq #1157: CRC32 Integritet Tekshiruvi
**Tavsif:** Ma'lumotlar uzatilganda yaxlitligini tekshirish.
**Talablar:** `crc32` CPU instruksiyasidan foydalanish.
**Yechim (Assembly):**
```assembly
    crc32 eax, [data_ptr]  ; Ma'lumot yaxlitligini hisoblash
```
**Tushuntirish:** Zamonaviy protsessorlardagi `crc32` instruksiyasi dasturiy hisoblashdan 10 barobar tezroq ishlaydi.

### Topshiriq #1158: Xavfsiz Tasodifiy Son Generatsiyasi (RDRAND)
**Tavsif:** Kriptografik kalitlar uchun yuqori entropiyali sonlar olish.
**Talablar:** `rdrand` instruksiyasidan foydalanish.
**Yechim (Assembly):**
```assembly
.retry:
    rdrand rax             ; Tasodifiy son generatsiyasi
    jnc .retry             ; Agar muvaffaqiyatsiz bo'lsa, qayta urinish
```
**Tushuntirish:** `rdrand` apparat darajasida tasodifiylikni ta'minlaydi, bu dasturiy generatorlardan xavfsizroq.

### Topshiriq #1159: Privileged Instruction Check
**Tavsif:** Dastur faqat foydalanuvchi rejimida (Ring 3) ishlashini ta'minlash.
**Talablar:** CPU imtiyoz darajasini tekshirish.
**Yechim (Assembly):**
```assembly
    mov eax, cs            ; Kod segmenti registrini olish
    and eax, 3             ; Imtiyoz darajasi (CPL)
    cmp eax, 3             ; Ring 3 da ekanligini tekshirish
    jne .privilege_error
```
**Tushuntirish:** Bu kod dasturning tizim darajasidagi (kernel) resurslarga ruxsatsiz kirishini oldini oladi.

### Topshiriq #1160: Constant-Time Comparison
**Tavsif:** Parollarni solishtirishda vaqtga asoslangan hujumlarni (timing attacks) oldini olish.
**Talablar:** Har doim bir xil vaqtda bajariladigan solishtirish.
**Yechim (Assembly):**
```assembly
    xor rcx, rcx           ; Farqni yig'ish
    mov rsi, pass1
    mov rdi, pass2
    mov rax, 16            ; Uzunlik
.loop:
    mov dl, [rsi]
    xor dl, [rdi]          ; Farqni olish
    or cl, dl              ; Farqlarni yig'ish
    inc rsi
    inc rdi
    dec rax
    jnz .loop
    test cl, cl            ; cl 0 ga tengmi?
```
**Tushuntirish:** `cmp` va `jne` ishlatilmaydi, chunki ular farq topilganda tezroq chiqib ketadi. Bu usul har doim barcha baytlarni tekshiradi.

---

### Topshiriq #1161: AES S-Box uchun Lookup Table optimizatsiyasi
**Tavsif:** AES algoritmining ishlash tezligini oshirish uchun S-Box (Substitution Box) qiymatlarini xotiradan tezkor o'qish va keshga moslash.
**Talablar:** S-Box jadvalini xotirada hizalash (alignment) va `XLAT` ko'rsatmasidan foydalanib qiymatni o'zgartirish.
**Yechim (Assembly):**
```assembly
section .data
    sbox db 0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5 ; Qisqartirilgan S-Box
section .text
    ; AL registrida kirish bayti mavjud
    lea ebx, [sbox]      ; S-Box manzilini yuklash
    xlat                 ; AL = [EBX + AL] (S-Box almashtiruvi)
    ; Natija AL registrida
```
**Tushuntirish:** `XLAT` ko'rsatmasi xotiradan ma'lumot olishni bitta siklda amalga oshiradi, bu esa kriptografik operatsiyalarda kechikishni minimallashtiradi.

### Topshiriq #1162: RSA uchun Modular Exponentiation (Kvadrat-ko'paytirish)
**Tavsif:** RSA shifrlashda katta sonlarni darajaga ko'tarish uchun "Square-and-Multiply" algoritmini implementatsiya qilish.
**Talablar:** 64-bitli registrlar yordamida modulli ko'paytirishni amalga oshirish.
**Yechim (Assembly):**
```assembly
; RDX:RAX = (RAX * RBX) mod RCX
mul_mod:
    mul rbx              ; RDX:RAX = RAX * RBX
    div rcx              ; RDX = qoldiq
    mov rax, rdx         ; Natijani RAX ga o'tkazish
    ret
```
**Tushuntirish:** `div` operatsiyasi qimmat bo'lgani uchun, bu yerda qoldiqni tezkor olish usuli qo'llanilgan.

### Topshiriq #1163: ECC (Elliptic Curve) Nuqta Qo'shish
**Tavsif:** Elliptik egri chiziqlar kriptografiyasida (ECC) ikki nuqtani qo'shish operatsiyasi.
**Talablar:** `y^2 = x^3 + ax + b` tenglamasi asosida nuqtalarni qo'shish.
**Yechim (Assembly):**
```assembly
; P1(x1, y1) + P2(x2, y2) = P3(x3, y3)
add_points:
    sub rax, rbx         ; x2 - x1
    mov rcx, rax         ; Maxrajni saqlash
    ; ... (Modular teskari qiymatni hisoblash)
    ; ... (Natijani hisoblash)
```
**Tushuntirish:** ECC operatsiyalari xavfsizligi modulli teskari qiymatni (modular inverse) topish tezligiga bog'liq.

### Topshiriq #1164: Xavfsiz Xotira Tozalash (Zeroing)
**Tavsif:** Maxfiy kalitlar xotirada qolib ketmasligi uchun ularni dastur tugagach o'chirish.
**Talablar:** `rep stosb` yordamida xotirani nolga tenglash.
**Yechim (Assembly):**
```assembly
clear_buffer:
    mov edi, buffer_ptr  ; Buffer manzili
    mov ecx, 32          ; 32 baytni tozalash
    xor eax, eax         ; EAX = 0
    rep stosb            ; Xotirani tozalash
```
**Tushuntirish:** `rep stosb` eng samarali usul bo'lib, protsessor darajasida xotirani tez tozalaydi.

### Topshiriq #1165: XOR asosida Stream Cipher
**Tavsif:** Ma'lumotlarni oddiy va tez shifrlash uchun XOR operatsiyasidan foydalanish.
**Talablar:** Kalit (key) va matnni bitma-bit XOR qilish.
**Yechim (Assembly):**
```assembly
encrypt_loop:
    mov al, [esi]        ; Matn bayti
    xor al, [key]        ; Kalit bilan XOR
    mov [edi], al        ; Shifrlangan matn
    inc esi
    inc edi
    loop encrypt_loop
```
**Tushuntirish:** XOR operatsiyasi teskari bo'lgani uchun, bir xil kod shifrlash va shifrdan chiqarish uchun ishlatiladi.

### Topshiriq #1166: Stack Canary (Buffer Overflow himoyasi)
**Tavsif:** Funksiya chaqiruvlarida stekni himoya qilish uchun "canary" qiymatini tekshirish.
**Talablar:** Funksiya boshida qiymatni stekka yozish va oxirida tekshirish.
**Yechim (Assembly):**
```assembly
check_canary:
    mov rax, [rbp-8]     ; Canary qiymatini olish
    cmp rax, [gs:0x28]   ; Global canary bilan solishtirish
    jne security_alert   ; Agar teng bo'lmasa, xavfsizlik xatosi
```
**Tushuntirish:** `gs` segmenti orqali tizim himoyasiga murojaat qilish eng xavfsiz usullardan biridir.

### Topshiriq #1167: SHA-256 uchun Bitwise Rotate
**Tavsif:** SHA-256 xeshlash algoritmi uchun zarur bo'lgan `ROR` (Rotate Right) operatsiyasi.
**Talablar:** 32-bitli qiymatni aylantirish.
**Yechim (Assembly):**
```assembly
; EAX qiymatini 7 bit o'ngga aylantirish
ror eax, 7
```
**Tushuntirish:** `ROR` ko'rsatmasi kriptografik algoritmlarda diffuziya effektini yaratish uchun juda muhim.

### Topshiriq #1168: Kriptografik Tasodifiy Sonlar (RDRAND)
**Tavsif:** Hardware-based tasodifiy sonlar generatoridan foydalanish.
**Talablar:** `rdrand` ko'rsatmasi orqali xavfsiz kalit generatsiyasi.
**Yechim (Assembly):**
```assembly
get_random:
    rdrand rax           ; Tasodifiy son olish
    jnc get_random       ; Agar muvaffaqiyatsiz bo'lsa, qayta urinish
```
**Tushuntirish:** `RDRAND` protsessorning o'zida joylashgan entropiya manbasidan foydalanadi, bu esa dasturiy generatorlardan xavfsizroq.

### Topshiriq #1169: HMAC uchun Hashni birlashtirish
**Tavsif:** Xabar autentifikatsiyasi kodi (HMAC) uchun kalit va xabarni birlashtirish.
**Talablar:** Xotirada ketma-ket joylashgan ma'lumotlarni birlashtirish.
**Yechim (Assembly):**
```assembly
concat_data:
    mov ecx, key_len
    rep movsb            ; Kalitni nusxalash
    mov ecx, msg_len
    rep movsb            ; Xabarni nusxalash
```
**Tushuntirish:** `rep movsb` xotira bloklarini ko'chirishda eng tezkor usul hisoblanadi.

### Topshiriq #1170: Constant-Time Comparison
**Tavsif:** Timing-attack (vaqt tahlili) hujumlaridan himoyalanish uchun kalitlarni doimiy vaqtda solishtirish.
**Talablar:** `cmp` o'rniga `xor` va `or` operatsiyalaridan foydalanish.
**Yechim (Assembly):**
```assembly
secure_cmp:
    xor al, [esi]        ; Baytlarni XOR qilish
    or bl, al            ; Natijalarni to'plash
    inc esi
    inc edi
    ; Agar BL nol bo'lsa, satrlar teng
```
**Tushuntirish:** `cmp` va `jne` (shartli o'tish) vaqtni o'zgartiradi, bu esa xakerlarga kalitni taxmin qilishga imkon beradi. `OR` operatsiyasi esa vaqtni doimiy saqlaydi.

---

### Topshiriq #1171: AES S-Box Substitutsiyasi
**Tavsif:** AES algoritmining asosiy qismi bo'lgan SubBytes bosqichini amalga oshirish. Xotiradan o'qish (Lookup table) vaqtida "side-channel" hujumlaridan himoyalanish uchun xavfsiz kodlash.
**Talablar:** S-Box jadvalidan foydalanib 16 baytli blokni transformatsiya qilish.
**Yechim (Assembly):**
```assembly
; AES S-Box almashtirish (x86-64)
; rdi - kirish bloki manzili, rsi - S-Box jadvali manzili
sub_bytes:
    mov rcx, 16          ; 16 baytli blok
.loop:
    movzx rax, byte [rdi] ; Baytni o'qish
    mov al, [rsi + rax]   ; S-Box orqali almashtirish
    mov [rdi], al         ; Natijani yozish
    inc rdi
    loop .loop
    ret
```
**Tushuntirish:** `movzx` buyrug'i orqali baytni 64-bitli registrga nol bilan to'ldirib o'tkazish xavfsizlikni ta'minlaydi va xotira manzillashda xatoliklarni oldini oladi.

### Topshiriq #1172: RSA uchun Modular Eksponentlash (Square-and-Multiply)
**Tavsif:** RSA shifrlashda katta sonlarni darajaga ko'tarishda samaradorlik va xavfsizlikni ta'minlash.
**Talablar:** `(base^exp) % mod` operatsiyasini bajarish.
**Yechim (Assembly):**
```assembly
; Oddiy kvadratlash va ko'paytirish algoritmi
power_mod:
    ; rdi: base, rsi: exp, rdx: mod
    mov rax, 1           ; Natija = 1
.loop:
    test rsi, rsi        ; Eksponent 0 ga tengmi?
    jz .done
    shr rsi, 1           ; Bitni tekshirish
    jnc .skip
    mul rdi              ; rax = rax * base
    div rdx              ; rax = rax % mod
.skip:
    imul rdi, rdi        ; base = base * base
    div rdx
    jmp .loop
.done:
    ret
```
**Tushuntirish:** `div` buyrug'i qimmat operatsiya bo'lgani uchun, real tizimlarda Montgomery ko'paytirishdan foydalanish tavsiya etiladi.

### Topshiriq #1173: ECC Nuqtani Qo'shish (Elliptic Curve)
**Tavsif:** Elliptik egri chiziqlar kriptografiyasida (ECC) ikki nuqtani qo'shish operatsiyasi.
**Talablar:** `P + Q = R` operatsiyasini bajarishda `x` va `y` koordinatalarini hisoblash.
**Yechim (Assembly):**
```assembly
; ECC nuqta qo'shish (qisqartirilgan)
ecc_add:
    ; P(x1, y1) va Q(x2, y2)
    sub rax, rbx         ; x2 - x1
    mov rcx, rax
    ; Inversiya hisoblash (Fermat's Little Theorem)
    ; ... (inversiya kodi)
    imul rax, rax        ; lambda^2
    sub rax, rdi         ; x3 = lambda^2 - x1 - x2
    ret
```
**Tushuntirish:** ECC operatsiyalarida vaqt tahlili (timing attack) hujumlariga qarshi doimiy vaqtli (constant-time) algoritmlar tanlanishi shart.

### Topshiriq #1174: Xavfsiz Xotirani Tozalash (Zeroing Memory)
**Tavsif:** Maxfiy kalitlar xotirada qolib ketmasligi uchun ularni dastur tugagach o'chirish.
**Talablar:** `memset` kabi funksiyalardan foydalanmasdan, kompilyator optimizatsiyasini chetlab o'tish.
**Yechim (Assembly):**
```assembly
secure_wipe:
    ; rdi: buffer, rsi: length
.wipe:
    mov byte [rdi], 0    ; Har bir baytni 0 ga tenglash
    inc rdi
    dec rsi
    jnz .wipe
    mfence               ; Xotira operatsiyalarini yakunlash
    ret
```
**Tushuntirish:** `mfence` buyrug'i protsessor xotira yozishni to'liq yakunlaganiga ishonch hosil qiladi, bu esa "dead store elimination" optimizatsiyasini oldini oladi.

### Topshiriq #1175: XOR Shifrlash (Stream Cipher)
**Tavsif:** Oddiy, ammo tezkor ma'lumotlarni yashirish usuli.
**Talablar:** Kalit (key) yordamida ma'lumotlar oqimini XORlash.
**Yechim (Assembly):**
```assembly
xor_cipher:
    ; rdi: data, rsi: key, rdx: length
.loop:
    mov al, [rdi]
    xor al, [rsi]        ; XOR operatsiyasi
    mov [rdi], al
    inc rdi
    inc rsi
    dec rdx
    jnz .loop
    ret
```
**Tushuntirish:** XOR operatsiyasi simmetrik bo'lgani uchun, bir xil funksiya ham shifrlash, ham deshifrlash uchun ishlatiladi.

### Topshiriq #1176: Stack Canary Tekshiruvi
**Tavsif:** Buffer overflow hujumlaridan himoyalanish uchun stack qiymatini tekshirish.
**Talablar:** Funksiya oxirida stack canary qiymati o'zgarganligini aniqlash.
**Yechim (Assembly):**
```assembly
check_canary:
    mov rax, [rbp-8]     ; Canary qiymatini o'qish
    cmp rax, [gs:0x28]   ; Global canary bilan solishtirish
    jne security_alert   ; Agar teng bo'lmasa, xavfsizlik xatosi
    ret
security_alert:
    ud2                  ; Dasturni majburiy to'xtatish
```
**Tushuntirish:** `gs:0x28` - bu Linux tizimlarida xavfsizlik uchun ishlatiladigan maxsus xotira joyi.

### Topshiriq #1177: HMAC (Hash-based Message Authentication)
**Tavsif:** Xabar yaxlitligini tekshirish uchun kalitli xesh funksiyasi.
**Talablar:** `Hash(key XOR opad, Hash(key XOR ipad, message))` strukturasini amalga oshirish.
**Yechim (Assembly):**
```assembly
; HMAC qismi: XOR ipad/opad
apply_pad:
    ; rdi: key, rsi: pad_byte
    mov rcx, 64          ; Blok hajmi
.loop:
    xor [rdi], sil
    inc rdi
    loop .loop
    ret
```
**Tushuntirish:** HMAC xabar o'zgartirilmaganligini va haqiqiy manbadan kelganligini kafolatlaydi.

### Topshiriq #1178: Salted Password Hashing
**Tavsif:** Parollarni saqlashda "salt" (tuz) qo'shish orqali Rainbow table hujumlaridan himoyalanish.
**Talablar:** Parol va saltni birlashtirib xesh funksiyasiga yuborish.
**Yechim (Assembly):**
```assembly
concat_salt:
    ; rdi: password, rsi: salt, rdx: buffer
    ; Parolni ko'chirish
    rep movsb
    ; Saltni qo'shish
    mov rcx, 16
    rep movsb
    ret
```
**Tushuntirish:** Salt har bir foydalanuvchi uchun noyob bo'lishi kerak, bu bir xil parollarning xesh qiymatlari bir xil bo'lishiga yo'l qo'ymaydi.

### Topshiriq #1179: Constant-Time Comparison
**Tavsif:** Ikki xesh yoki kalitni solishtirishda vaqt farqini yo'qotish.
**Talablar:** `memcmp` dan foydalanmasdan, barcha baytlarni tekshirib chiqish.
**Yechim (Assembly):**
```assembly
secure_compare:
    xor rax, rax
.loop:
    mov cl, [rdi]
    xor cl, [rsi]
    or al, cl            ; Farq bo'lsa, al 0 bo'lmaydi
    inc rdi
    inc rsi
    dec rdx
    jnz .loop
    ret                  ; 0 qaytsa - teng
```
**Tushuntirish:** Oddiy `cmp` va `jne` ishlatilsa, birinchi farqli baytda funksiya to'xtaydi, bu esa hujumchiga kalitni taxmin qilishga yordam beradi.

### Topshiriq #1180: Random Number Generator (RDRAND)
**Tavsif:** Kriptografik kalitlar uchun yuqori sifatli tasodifiy sonlar generatsiyasi.
**Talablar:** Protsessorning `RDRAND` instruksiyasidan foydalanish.
**Yechim (Assembly):**
```assembly
get_random:
    rdrand rax           ; Tasodifiy son generatsiyasi
    jnc get_random       ; Agar muvaffaqiyatsiz bo'lsa, qayta urinish
    ret
```
**Tushuntirish:** `RDRAND` apparat darajasida entropiyani ta'minlaydi, bu dasturiy ta'minot darajasidagi tasodifiy son generatorlaridan xavfsizroqdir.

---

### Topshiriq #1181: AES S-Box Substitutsiyasi
**Tavsif:** AES algoritmining asosiy qismi bo'lgan SubBytes bosqichini amalga oshirish. Xotira xavfsizligini ta'minlash uchun lookup table'dan foydalanish.
**Talablar:** 8-bitli qiymatni S-Box jadvali orqali almashtirish, xotira xavfsizligini ta'minlash.
**Yechim (Assembly):**
```assembly
section .data
    sbox db 0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5 ; Qisqartirilgan jadval
section .text
    ; AL registrida kirish bayti mavjud
    movzx eax, al          ; Indeksni tozalash
    mov al, [sbox + eax]   ; S-Box qiymatini olish
```
**Tushuntirish:** `movzx` buyrug'i orqali indeksni tozalash orqali "buffer overflow" xavfini kamaytirdik va to'g'ridan-to'g'ri xotira manzillashdan foydalandik.

### Topshiriq #1182: RSA Modular Eksponentlash (Kvadratlash usuli)
**Tavsif:** RSA shifrlashda katta sonlarni modulli darajaga ko'tarish.
**Talablar:** `(base^exp) % mod` amalini samarali bajarish.
**Yechim (Assembly):**
```assembly
; RDX:RAX = base, RBX = exp, RCX = mod
mod_exp:
    mov r8, 1           ; Natija = 1
.loop:
    test rbx, rbx       ; Eksponent tugadimi?
    jz .done
    shr rbx, 1          ; Bitni tekshirish
    jnc .skip
    mul r8              ; Natija = (Natija * base) % mod
    div rcx
    mov r8, rdx
.skip:
    mul rax             ; base = (base * base) % mod
    div rcx
    mov rax, rdx
    jmp .loop
.done:
```
**Tushuntirish:** "Square-and-multiply" algoritmi vaqt murakkabligini O(log n) ga tushiradi, bu kiberxavfsizlikda tezkor shifrlash uchun muhim.

### Topshiriq #1183: ECC Nuqta Qo'shish (Point Addition)
**Tavsif:** Elliptik egri chiziqlar kriptografiyasida (ECC) ikki nuqtani qo'shish.
**Talablar:** `P + Q = R` operatsiyasini bajarishda xatolarni boshqarish.
**Yechim (Assembly):**
```assembly
; P(x1, y1) va Q(x2, y2) nuqtalarini qo'shish
add_points:
    sub rax, rbx        ; x2 - x1
    div rcx             ; (y2 - y1) / (x2 - x1) mod p
    ; ... (ECC formulasi bo'yicha hisoblash)
```
**Tushuntirish:** ECC operatsiyalarida bo'lish amali modulli teskari qiymat (modular inverse) orqali amalga oshiriladi, bu yerda `div` xavfsizligiga e'tibor qaratildi.

### Topshiriq #1184: Xavfsiz Xotira Tozalash (Zeroing)
**Tavsif:** Maxfiy kalitlar ishlatilgandan so'ng xotirani o'chirish.
**Talablar:** Kompilyator optimizatsiyasi tomonidan olib tashlanmaydigan xotira tozalash.
**Yechim (Assembly):**
```assembly
secure_wipe:
    mov rcx, 32         ; 32 baytli kalit
    xor rax, rax
.wipe:
    mov [rdi], al       ; Xotiraga 0 yozish
    inc rdi
    loop .wipe
    mfence              ; Xotira operatsiyasini majburiy yakunlash
```
**Tushuntirish:** `mfence` buyrug'i protsessor keshidagi ma'lumotlarni tozalashni kafolatlaydi, bu "cold boot" hujumlaridan himoya qiladi.

### Topshiriq #1185: XOR Shifrlash (Stream Cipher)
**Tavsif:** Ma'lumotlarni kalit bilan XORlash orqali oddiy shifrlash.
**Talablar:** Kalit uzunligi va ma'lumot uzunligini moslashtirish.
**Yechim (Assembly):**
```assembly
xor_cipher:
    mov al, [rsi]       ; Kalit bayti
    xor [rdi], al       ; Ma'lumotni XORlash
    inc rdi
    inc rsi
    loop xor_cipher
```
**Tushuntirish:** XOR operatsiyasi simmetrik bo'lgani uchun shifrlash va deshifrlash uchun bir xil kod ishlatiladi, bu resurslarni tejaydi.

### Topshiriq #1186: Stack Canary Himoyasi
**Tavsif:** Buffer overflow hujumlarini aniqlash uchun stekka "canary" qiymatini qo'yish.
**Talablar:** Funksiya oxirida canary qiymatini tekshirish.
**Yechim (Assembly):**
```assembly
check_canary:
    mov rax, [rbp-8]    ; Saqlangan canary
    cmp rax, [gs:0x28]  ; Global canary bilan solishtirish
    jne security_alert  ; Agar teng bo'lmasa, xavfsizlik xatosi
```
**Tushuntirish:** `gs` segment registridan foydalanish operatsion tizim darajasidagi himoyani ta'minlaydi.

### Topshiriq #1187: HMAC (Hash-based Message Authentication Code)
**Tavsif:** Xabarning yaxlitligini tekshirish uchun HMAC qismini amalga oshirish.
**Talablar:** Kalit va xabarni birlashtirib hash funksiyasiga uzatish.
**Yechim (Assembly):**
```assembly
compute_hmac:
    ; Kalitni xabar bilan XORlash (inner pad)
    xor byte [rdi], 0x36
    ; Hash funksiyasini chaqirish (masalan, SHA-256)
    call sha256_update
```
**Tushuntirish:** 0x36 va 0x5C konstantalari HMAC standartiga muvofiq xavfsiz "padding" uchun ishlatiladi.

### Topshiriq #1188: Tasodifiy Sonlar Generatsiyasi (RDRAND)
**Tavsif:** Kriptografik kalitlar uchun yuqori sifatli tasodifiy son olish.
**Talablar:** CPU'ning `rdrand` instruksiyasidan foydalanish.
**Yechim (Assembly):**
```assembly
get_random:
    rdrand rax          ; Tasodifiy son generatsiyasi
    jnc get_random      ; Agar muvaffaqiyatsiz bo'lsa, qayta urinish
```
**Tushuntirish:** `rdrand` apparat darajasida entropiyani ta'minlaydi, bu dasturiy ta'minot darajasidagi generatorlardan ko'ra xavfsizroq.

### Topshiriq #1189: Xavfsiz String Taqqoslash (Constant Time)
**Tavsif:** Parollarni taqqoslashda "timing attack" hujumlarining oldini olish.
**Talablar:** Taqqoslash vaqti kirish ma'lumotlariga bog'liq bo'lmasligi kerak.
**Yechim (Assembly):**
```assembly
constant_time_cmp:
    xor rcx, rcx
.loop:
    mov al, [rdi]
    or al, [rsi]        ; Farqni to'plash
    inc rdi
    inc rsi
    cmp byte [rdi], 0
    jne .loop
    test rcx, rcx       ; RCX 0 bo'lsa, satrlar teng
```
**Tushuntirish:** `or` operatsiyasi orqali barcha baytlar tekshiriladi, bu "short-circuit" (erta chiqib ketish) orqali vaqtni o'lchash hujumlarini yo'q qiladi.

### Topshiriq #1190: Syscall Filtratsiyasi (Seccomp)
**Tavsif:** Dastur ruxsat etilgan syscall'lar bilan cheklash.
**Talablar:** Faqat kerakli syscall'larga ruxsat berish.
**Yechim (Assembly):**
```assembly
apply_seccomp:
    mov rax, 157        ; prctl syscall
    mov rdi, 22         ; PR_SET_SECCOMP
    mov rsi, 2          ; SECCOMP_MODE_FILTER
    syscall
```
**Tavsif:** Bu yondashuv dasturning zararli kod bajarish imkoniyatini minimal darajaga tushiradi, chunki ruxsatsiz syscall'lar bloklanadi.

---

### Topshiriq #1191: AES S-Box Substitutsiyasi (Xavfsiz kodlash)
**Tavsif:** AES algoritmining asosiy qismi bo'lgan S-Box almashtirish operatsiyasini xotira xavfsizligini ta'minlagan holda amalga oshirish.
**Talablar:** `AL` registrida berilgan baytni oldindan belgilangan S-Box jadvali orqali almashtirish.
**Yechim (Assembly):**
```assembly
section .data
    sbox db 0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5 ; Qisqartirilgan jadval
section .text
    ; AL registrida kiruvchi bayt mavjud
    movzx ebx, al           ; Indeksni EBX ga o'tkazish
    mov al, [sbox + ebx]    ; S-Box dan qiymatni olish
```
**Tushuntirish:** `movzx` buyrug'i qiymatni kengaytirib, xotira manzilini aniq hisoblash imkonini beradi, bu esa buffer overflow xavfini kamaytiradi.

### Topshiriq #1192: XOR asosidagi Stream Cipher (Kriptografiya)
**Tavsif:** Ma'lumotlarni kalit yordamida shifrlash (Stream Cipher).
**Talablar:** 16 baytli ma'lumotlar blokini 16 baytli kalit bilan XOR operatsiyasi orqali shifrlash.
**Yechim (Assembly):**
```assembly
    mov ecx, 16             ; 16 baytli sikl
    xor esi, esi
loop_cipher:
    mov al, [data + esi]
    xor al, [key + esi]     ; XOR shifrlash
    mov [data + esi], al
    inc esi
    loop loop_cipher
```
**Tushuntirish:** XOR operatsiyasi simmetrik bo'lgani uchun bir xil kod shifrlash va deshifrlash uchun ishlatiladi, bu esa resurslarni tejaydi.

### Topshiriq #1193: Stack Canary (Xavfsiz kodlash)
**Tavsif:** Buffer overflow hujumlarini aniqlash uchun stack himoyasini o'rnatish.
**Talablar:** Funksiya boshida stack qiymatini saqlash va tugashida tekshirish.
**Yechim (Assembly):**
```assembly
    mov rax, [fs:0x28]      ; Canary qiymatini olish
    mov [rbp-8], rax        ; Stackga saqlash
    ; ... funksiya tanasi ...
    mov rdx, [rbp-8]
    xor rdx, [fs:0x28]      ; Tekshirish
    jnz security_violation  ; Agar farqli bo'lsa, xavfsizlik xatosi
```
**Tushuntirish:** `fs:0x28` - bu operatsion tizim tomonidan berilgan tasodifiy qiymat bo'lib, stack buzilganligini aniqlashda eng samarali usuldir.

### Topshiriq #1194: RSA Modular Exponentiation (Kriptografiya)
**Tavsif:** RSA uchun zarur bo'lgan modulli eksponentlashning asosiy qismi.
**Talablar:** `(base^exp) % mod` amalini bajarish uchun `mul` va `div` dan foydalanish.
**Yechim (Assembly):**
```assembly
    mov rax, [base]
    mul rax                 ; Kvadratga oshirish
    div qword [mod]         ; Modulo operatsiyasi
    mov [result], rdx       ; Qoldiqni saqlash
```
**Tushuntirish:** `div` buyrug'i qoldiqni `rdx` registrida qoldiradi, bu kriptografik hisob-kitoblar uchun juda qulay.

### Topshiriq #1195: ECC Point Addition (Kriptografiya)
**Tavsif:** Elliptik egri chiziqlar (ECC) ustida nuqtalarni qo'shish.
**Talablar:** Ikki nuqta koordinatalarini qo'shishda xatolik yuz bermasligini ta'minlash.
**Yechim (Assembly):**
```assembly
    add rax, rbx            ; X1 + X2
    sub rax, [lambda]       ; Lambda qiymatini ayirish
    and rax, 0xFFFFFFFFFFFFFFFF ; Maydon chegarasini saqlash
```
**Tushuntirish:** ECC operatsiyalari katta sonlar bilan ishlashni talab qiladi, `and` operatsiyasi ma'lumotlar maydonidan chiqib ketmaslikni ta'minlaydi.

### Topshiriq #1196: Xavfsiz xotirani tozalash (Xavfsiz kodlash)
**Tavsif:** Maxfiy kalitlar ishlatilgandan so'ng xotirani o'chirish.
**Talablar:** `rep stosb` yordamida xotirani nolga tenglash.
**Yechim (Assembly):**
```assembly
    mov rcx, 32             ; 32 baytni tozalash
    xor al, al              ; 0 qiymati
    lea rdi, [key_buffer]
    rep stosb               ; Xotirani tozalash
```
**Tushuntirish:** `rep stosb` - xotirani tozalashning eng tezkor usuli, u ma'lumotlarning xotirada qolib ketib, keyinchalik o'qilishining oldini oladi.

### Topshiriq #1197: Constant-Time Comparison (Kriptografiya)
**Tavsif:** Parollarni solishtirishda vaqt tahlili (timing attack) hujumlarini oldini olish.
**Talablar:** Solishtirish vaqti kiritilgan ma'lumotga bog'liq bo'lmasligi kerak.
**Yechim (Assembly):**
```assembly
    xor rcx, rcx
    mov rdx, 0
compare_loop:
    mov al, [input + rcx]
    xor al, [stored + rcx]
    or rdx, rax             ; Farq bo'lsa, RDX nol bo'lmaydi
    inc rcx
    cmp rcx, 16
    jne compare_loop
```
**Tushuntirish:** `or` operatsiyasi orqali barcha baytlar tekshiriladi, bu esa "erta chiqish" (early exit) imkonini bermaydi va vaqt hujumlarini to'sadi.

### Topshiriq #1198: Random Number Generation (Kriptografiya)
**Tavsif:** `RDRAND` instruksiyasi yordamida tasodifiy son generatsiyasi.
**Talablar:** CPU ning apparatli tasodifiy son generatoridan foydalanish.
**Yechim (Assembly):**
```assembly
retry:
    rdrand rax              ; Tasodifiy son olish
    jnc retry               ; Agar muvaffaqiyatsiz bo'lsa, qayta urinish
    mov [random_val], rax
```
**Tushuntirish:** `RDRAND` xavfsizlik uchun eng yuqori entropiyani ta'minlaydi, chunki u apparat darajasida ishlaydi.

### Topshiriq #1199: Memory Boundary Check (Xavfsiz kodlash)
**Tavsif:** Berilgan bufer chegarasidan tashqariga yozishni oldini olish.
**Talablar:** Indeksning maksimal qiymatdan oshmasligini tekshirish.
**Yechim (Assembly):**
```assembly
    cmp rsi, 256            ; Maksimal o'lcham 256
    jae error_handler       ; Agar katta bo'lsa, xatolikka o'tish
    mov [buffer + rsi], al
```
**Tushuntirish:** `jae` (Jump if Above or Equal) shartli o'tish buyrug'i xotira xavfsizligini ta'minlashning eng asosiy himoya qalqonidir.

### Topshiriq #1200: Integrity Check (Kiberxavfsizlik)
**Tavsif:** Kod yaxlitligini tekshirish (Checksum).
**Talablar:** Kod segmenti uchun oddiy CRC hisoblash.
**Yechim (Assembly):**
```assembly
    xor rax, rax
    mov rcx, code_size
calc_crc:
    add al, [code_start + rcx]
    rol al, 1               ; Aylantirish orqali yaxlitlikni tekshirish
    loop calc_crc
```
**Tushuntirish:** `rol` (Rotate Left) operatsiyasi bitlar ketma-ketligini o'zgartirib, kodga kiritilgan kichik o'zgarishlarni ham aniqlashga yordam beradi.