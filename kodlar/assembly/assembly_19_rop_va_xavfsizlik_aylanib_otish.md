# 901-Topshiriq: ROP (Return-Oriented Programming) tushunchasi va Gadget tuzilishi
## Topshiriq sharti:
ROP va xavfsizlik aylanib o'tish tahlili: ROP (Return-Oriented Programming) tushunchasi va Gadget tuzilishi.

## Yechim (Assembly kodi):
```assembly
; ROP Gadget - 'ret' (0xC3) buyrug'i bilan tugaydigan kichik mashina kodlari parchasi
; Misol: pop rdi ; ret
section .text
global gadget_pop_rdi
gadget_pop_rdi:
    pop rdi              ; Stekning yuqori qiymatini RDI registriga oladi (1-argument)
    ret                  ; Stekdagi keyingi manzilga sakraydi
```

## Tushuntirish va Mantiq:
DEP/NX (No-Execute) xotira himoyasi stekdagi shellcodeni to'g'ridan-to'g'ri ishga tushirishga yo'l qo'ymaydi. ROP orqali dasturning o'zida yoki libc kutubxonasida mavjud bo'lgan instruksiya parchalari ('gadget'lar) ketma-ket chaqiriladi.

## Ishlash natijasi:
```text
Gadget chaqirilib, RDI registriga parametr yuklanadi va keyingi zanjirga o'tiladi.
```


# 902-Topshiriq: Oddiy ROP Zanjiri (ROP Chain) tuzish: Argument tayyorlash
## Topshiriq sharti:
ROP va xavfsizlik aylanib o'tish tahlili: Oddiy ROP Zanjiri (ROP Chain) tuzish: Argument tayyorlash.

## Yechim (Assembly kodi):
```assembly
; Stek xotirasidagi ROP zanjiri modeli:
; [Stek ofseti] -> [Gadget: pop rdi ; ret]
; [Stek ofseti + 8] -> [0xdeadbeef (rdi ga o'tuvchi qiymat)]
; [Stek ofseti + 16] -> [print_number funksiyasi manzili]
section .text
global execute_rop_demo
execute_rop_demo:
    ; Simulyatsiya qilingan stek o'tishi
    pop rdi              ; rdi = 0xdeadbeef
    ret                  ; target funksiyaga o'tish
```

## Tushuntirish va Mantiq:
ROP zanjiri stekka manzil va ma'lumotlarni qat'iy tartibda yozish orqali hosil qilinadi. Har bir `ret` buyrug'i stekdagi navbatdagi gadget yoki funksiya manzilini o'qiydi.

## Ishlash natijasi:
```text
RDI registri 0xDEADBEEF ga o'rnatiladi va nishon funksiya chaqiriladi.
```


# 903-Topshiriq: Ret2libc hujumi: system('/bin/sh') chaqiruvini tashkil qilish
## Topshiriq sharti:
ROP va xavfsizlik aylanib o'tish tahlili: Ret2libc hujumi: system('/bin/sh') chaqiruvini tashkil qilish.

## Yechim (Assembly kodi):
```assembly
; Ret2libc ROP sxemasi:
; 1. pop rdi ; ret  (manzili: 0x40120b)
; 2. '/bin/sh' satri manzili (libc yoki data bo'limidan)
; 3. system() funksiyasi manzili (libc ichidan)
; 4. exit() funksiyasi manzili
section .data
    bin_sh db '/bin/sh', 0
section .text
global ret2libc_stub
ret2libc_stub:
    lea rdi, [rel bin_sh]
    ; call system - C kutubxonasining system() funksiyasini chaqirish
    ret
```

## Tushuntirish va Mantiq:
NX yoqilgan tizimlarda xaker yangi shellcode kiritmasdan, xotirada allaqachon yuklangan `libc.so` dagi `system()` funksiyasiga `/bin/sh` manzilini uzatib qobiqqa ega bo'ladi.

## Ishlash natijasi:
```text
Linux terminal qobig'i (shell) ochiladi.
```


# 904-Topshiriq: ROP da Stek tekislash (16-bayt alignment) muammosi
## Topshiriq sharti:
ROP va xavfsizlik aylanib o'tish tahlili: ROP da Stek tekislash (16-bayt alignment) muammosi.

## Yechim (Assembly kodi):
```assembly
; Ubuntu 18.04+ da system() yoki printf() chaqirilganda SSE ko'rsatmalari (movaps)
; stek 16-baytga to'g'rilanmagan bo'lsa SIGSEGV beradi.
; Yechim: zanjirga ortiqcha bitta 'ret' gadget qo'shish:
; [ret gadget manzili]          ; Stekni 8 baytga siljitadi (rsp % 16 == 0)
; [pop rdi; ret gadget manzili]
; [bin_sh manzili]
; [system manzili]
```

## Tushuntirish va Mantiq:
Zamonaviy glibc kutubxonasida `system` chaqirilganda stek 16 bayt chegarasida bo'lishi talab etiladi. ROP zanjiriga bitta `ret` gadgetini qo'yish orqali moslik ta'minlanadi.

## Ishlash natijasi:
```text
movaps xatosi chetlab o'tilib, zanjir muvaffaqiyatli ishlaydi.
```


# 905-Topshiriq: PLT va GOT mexanizmi (Procedure Linkage & Global Offset Table)
## Topshiriq sharti:
ROP va xavfsizlik aylanib o'tish tahlili: PLT va GOT mexanizmi (Procedure Linkage & Global Offset Table).

## Yechim (Assembly kodi):
```assembly
; puts@plt chaqiruvi tahlili:
; puts@plt:
;   jmp [rel puts@got]   ; Birinchi marta chaqirilganda resolverga boradi
;   push index
;   jmp resolver
section .text
global call_puts
extern puts
call_puts:
    lea rdi, [rel msg]
    call puts            ; PLT orqali dinamik bog'langan funksiya chaqiriladi
    ret
section .rodata
msg db 'Salom Dinamik Bog\'lanish!', 0
```

## Tushuntirish va Mantiq:
Dinamik kutubxonalar manzillari ASLR tufayli o'zgaruvchan bo'ladi. PLT/GOT dasturga libc funksiyalari manzillarini dastur ishga tushganda birinchi chaqiruvda dinamik aniqlash imkonini beradi.

## Ishlash natijasi:
```text
Salom Dinamik Bog'lanish!
```


# 906-Topshiriq: GOT Overwrite (GOT jadvalini qayta yozish) zaifligi
## Topshiriq sharti:
ROP va xavfsizlik aylanib o'tish tahlili: GOT Overwrite (GOT jadvalini qayta yozish) zaifligi.

## Yechim (Assembly kodi):
```assembly
; Agar binary 'Partial RELRO' bilan kompilyatsiya qilingan bo'lsa, GOT bo'limi yozish mumkin (writable) bo'ladi
; Hujumchi GOT jadvalidagi puts@got manzilini o'zboshimchalik bilan win() funksiyasi manziliga o'zgartiradi:
; mov [puts@got], win_address
; Keyingi safar puts('test') chaqirilganda puts emas, win() bajariladi!
```

## Tushuntirish va Mantiq:
Partial RELRO holatida GOT jadvaliga yozish huquqi saqlanadi. Full RELRO da esa dastur yuklangandan so'ng GOT o'qish rejimiga (read-only) o'tkaziladi.

## Ishlash natijasi:
```text
Funksiya ko'rsatkichi almashtirilib, oqim boshqariladi.
```


# 907-Topshiriq: Libc manzilini sizdirish (Information Leak via puts@plt)
## Topshiriq sharti:
ROP va xavfsizlik aylanib o'tish tahlili: Libc manzilini sizdirish (Information Leak via puts@plt).

## Yechim (Assembly kodi):
```assembly
; ASLR ni yengish uchun libc bazaviy manzilini bilish kerak.
; ROP zanjiri orqali puts(puts@got) chaqiriladi:
; 1. pop rdi ; ret
; 2. puts@got (puts ning GOT dagi manzili)
; 3. puts@plt (puts funksiyasini bajarish)
; 4. main (dastur qayta ishga tushishi uchun)
```

## Tushuntirish va Mantiq:
puts() funksiyasi GOT da saqlangan haqiqiy libc manzillarini ekranga chiqaradi. Olingan manzildan libc ofseti ayirilib, libc base manzili hisoblab topiladi.

## Ishlash natijasi:
```text
Libc bazaviy manzili aniqlandi va ASLR chetlab o'tildi.
```


# 908-Topshiriq: SROP (Sigreturn-Oriented Programming) asoslari
## Topshiriq sharti:
ROP va xavfsizlik aylanib o'tish tahlili: SROP (Sigreturn-Oriented Programming) asoslari.

## Yechim (Assembly kodi):
```assembly
; Sigreturn tizim chaqiruvi (rt_sigreturn, syscall 15)
; Barcha registrlarni (RAX, RBX, RCX, RDX, RSI, RDI, RSP, RIP...) stekdan bittada tiklaydi
; SROP da stekka soxta 'ucontext' kadrini joylashtirib, birgina sigreturn chaqiruvi bilan
; barcha registrlarni bir zumda kerakli qiymatlarga to'ldirish mumkin.
```

## Tushuntirish va Mantiq:
SROP ko'p sonli ROP gadgetlar topilmagan kichik binarlarda barcha registrlarni bitta zanjir bilan boshqarish uchun eng samarali usuldir.

## Ishlash natijasi:
```text
Barcha protsessor registrlari soxta kadr asosida tiklanadi.
```


# 909-Topshiriq: JOP (Jump-Oriented Programming) asoslari
## Topshiriq sharti:
ROP va xavfsizlik aylanib o'tish tahlili: JOP (Jump-Oriented Programming) asoslari.

## Yechim (Assembly kodi):
```assembly
; JOP texnikasida 'ret' buyrug'i o'rniga bevosita sakrashlar ishlatiladi:
; Misol: jmp [rax] yoki jmp rbx
; Dispatcher gadget (dispetcher) orqali keyingi gadget manzili hisoblanadi
; Bu usul Shadow Stack (masalan, Intel CET) kabi ret tekshiruvlarini chetlab o'tishda o'rganiladi.
```

## Tushuntirish va Mantiq:
Shadow stack faqat `ret` manzilini tekshiradi, ammo `jmp` yoki `call` orqali boshqaruv uzatilganda JOP texnikasi qo'llanilishi mumkin.

## Ishlash natijasi:
```text
Boshqaruv oqimi sakrash registrlari orqali uzatiladi.
```


# 910-Topshiriq: ARM64 da ROP o'xshashi: Gadgetlar va BLR / RET
## Topshiriq sharti:
ROP va xavfsizlik aylanib o'tish tahlili: ARM64 da ROP o'xshashi: Gadgetlar va BLR / RET.

## Yechim (Assembly kodi):
```assembly
// ARM64 da gadgetlar:
// ldp x0, x1, [sp], #16 ; ret
// Bu gadget stekdan ikkita argumentni x0 va x1 registrlariga yuklaydi
.global arm64_gadget
arm64_gadget:
    ldp x0, x1, [sp], #16
    ret
```

## Tushuntirish va Mantiq:
ARM64 arxitekturasida RISC buyruqlari qat'iy 4 bayt bo'lgani sababli, x86 dagi kabi ko'rsatma o'rtasiga sakrab yangi gadget topish (unaligned gadget) mumkin emas, ammo rasmiy gadget zanjirlari tuziladi.

## Ishlash natijasi:
```text
x0 va x1 registrlari stekdan yuklanadi va x30 bo'yicha sakraladi.
```


# 911-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #1
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #1 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #1
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_1:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #1 tahlil qilindi va himoya choralari ko'rildi.
```


# 912-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #2
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #2 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #2
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_2:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #2 tahlil qilindi va himoya choralari ko'rildi.
```


# 913-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #3
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #3 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #3
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_3:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #3 tahlil qilindi va himoya choralari ko'rildi.
```


# 914-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #4
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #4 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #4
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_4:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #4 tahlil qilindi va himoya choralari ko'rildi.
```


# 915-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #5
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #5 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #5
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_5:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #5 tahlil qilindi va himoya choralari ko'rildi.
```


# 916-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #6
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #6 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #6
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_6:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #6 tahlil qilindi va himoya choralari ko'rildi.
```


# 917-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #7
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #7 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #7
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_7:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #7 tahlil qilindi va himoya choralari ko'rildi.
```


# 918-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #8
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #8 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #8
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_8:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #8 tahlil qilindi va himoya choralari ko'rildi.
```


# 919-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #9
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #9 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #9
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_9:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #9 tahlil qilindi va himoya choralari ko'rildi.
```


# 920-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #10
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #10 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #10
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_10:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #10 tahlil qilindi va himoya choralari ko'rildi.
```


# 921-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #11
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #11 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #11
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_11:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #11 tahlil qilindi va himoya choralari ko'rildi.
```


# 922-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #12
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #12 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #12
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_12:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #12 tahlil qilindi va himoya choralari ko'rildi.
```


# 923-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #13
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #13 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #13
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_13:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #13 tahlil qilindi va himoya choralari ko'rildi.
```


# 924-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #14
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #14 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #14
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_14:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #14 tahlil qilindi va himoya choralari ko'rildi.
```


# 925-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #15
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #15 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #15
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_15:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #15 tahlil qilindi va himoya choralari ko'rildi.
```


# 926-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #16
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #16 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #16
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_16:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #16 tahlil qilindi va himoya choralari ko'rildi.
```


# 927-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #17
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #17 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #17
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_17:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #17 tahlil qilindi va himoya choralari ko'rildi.
```


# 928-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #18
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #18 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #18
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_18:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #18 tahlil qilindi va himoya choralari ko'rildi.
```


# 929-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #19
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #19 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #19
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_19:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #19 tahlil qilindi va himoya choralari ko'rildi.
```


# 930-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #20
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #20 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #20
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_20:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #20 tahlil qilindi va himoya choralari ko'rildi.
```


# 931-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #21
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #21 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #21
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_21:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #21 tahlil qilindi va himoya choralari ko'rildi.
```


# 932-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #22
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #22 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #22
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_22:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #22 tahlil qilindi va himoya choralari ko'rildi.
```


# 933-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #23
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #23 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #23
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_23:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #23 tahlil qilindi va himoya choralari ko'rildi.
```


# 934-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #24
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #24 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #24
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_24:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #24 tahlil qilindi va himoya choralari ko'rildi.
```


# 935-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #25
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #25 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #25
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_25:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #25 tahlil qilindi va himoya choralari ko'rildi.
```


# 936-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #26
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #26 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #26
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_26:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #26 tahlil qilindi va himoya choralari ko'rildi.
```


# 937-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #27
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #27 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #27
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_27:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #27 tahlil qilindi va himoya choralari ko'rildi.
```


# 938-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #28
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #28 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #28
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_28:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #28 tahlil qilindi va himoya choralari ko'rildi.
```


# 939-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #29
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #29 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #29
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_29:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #29 tahlil qilindi va himoya choralari ko'rildi.
```


# 940-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #30
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #30 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #30
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_30:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #30 tahlil qilindi va himoya choralari ko'rildi.
```


# 941-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #31
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #31 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #31
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_31:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #31 tahlil qilindi va himoya choralari ko'rildi.
```


# 942-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #32
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #32 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #32
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_32:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #32 tahlil qilindi va himoya choralari ko'rildi.
```


# 943-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #33
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #33 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #33
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_33:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #33 tahlil qilindi va himoya choralari ko'rildi.
```


# 944-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #34
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #34 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #34
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_34:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #34 tahlil qilindi va himoya choralari ko'rildi.
```


# 945-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #35
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #35 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #35
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_35:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #35 tahlil qilindi va himoya choralari ko'rildi.
```


# 946-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #36
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #36 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #36
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_36:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #36 tahlil qilindi va himoya choralari ko'rildi.
```


# 947-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #37
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #37 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #37
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_37:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #37 tahlil qilindi va himoya choralari ko'rildi.
```


# 948-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #38
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #38 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #38
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_38:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #38 tahlil qilindi va himoya choralari ko'rildi.
```


# 949-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #39
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #39 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #39
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_39:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #39 tahlil qilindi va himoya choralari ko'rildi.
```


# 950-Topshiriq: Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #40
## Topshiriq sharti:
Xavfsizlikni aylanib o'tish va ROP bo'yicha Ixtisoslashgan ROP va himoyalarni tahlil qilish texnikasi #40 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; ROP / Exploit Mitigation tahlil namunasi #40
; Stack pivot (Stekni xaker buferiga ko'chirish: xchg rsp, rax / ret)
gadget_pivot_40:
    mov rsp, rdi         ; RSP yangi sun'iy stekka yo'naltiriladi
    pop rax              ; Yangi stekdan 1-qiymat olinadi
    ret                  ; Yangi stek bo'yicha zanjir davom etadi
```

## Tushuntirish va Mantiq:
Ushbu tahlilda Stack Pivot usuli orqali kichik buferdan katta buferga stek ko'rsatkichi siljitilib, ROP zanjiri uzluksiz bajarilishi ta'minlanadi.

## Ishlash natijasi:
```text
Stack pivot #40 tahlil qilindi va himoya choralari ko'rildi.
```

