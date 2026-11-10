# 801-Topshiriq: Disassembly tahlili: Oddiy if/else shartining assemblydagi ko'rinishi
## Topshiriq sharti:
Reverse engineering va disassembly tahlili: Disassembly tahlili: Oddiy if/else shartining assemblydagi ko'rinishi.

## Yechim (Assembly kodi):
```assembly
; C kodi:
; if (x > 10) y = 1; else y = 2;
; Kompilyatsiya qilingan assembly (objdump -d ko'rinishi):
cmp edi, 10
jle .L_else
mov eax, 1
jmp .L_end
.L_else:
mov eax, 2
.L_end:
ret
```

## Tushuntirish va Mantiq:
Reverse engineeringda `cmp` va shartli sakrash (`jle`, `jge`, `jne`, `je`) juftligi yuqori darajadagi dasturlash tilidagi `if/else` operatori ekanligini anglatadi.

## Ishlash natijasi:
```text
Agar edi > 10 bo'lsa eax = 1, aks holda eax = 2 qaytadi.
```


# 802-Topshiriq: Sikl tahlili: For/While siklini assemblyda tanib olish
## Topshiriq sharti:
Reverse engineering va disassembly tahlili: Sikl tahlili: For/While siklini assemblyda tanib olish.

## Yechim (Assembly kodi):
```assembly
; C kodi: for (int i = 0; i < n; i++) sum += i;
; Disassembly tahlili:
    xor eax, eax         ; sum = 0
    xor edx, edx         ; i = 0
.loop_start:
    cmp edx, edi         ; i < n ?
    jge .loop_done       ; agar i >= n bo'lsa chiqish
    add eax, edx         ; sum += i
    inc edx              ; i++
    jmp .loop_start      ; sikl boshiga qaytish
.loop_done:
    ret
```

## Tushuntirish va Mantiq:
Orqaga sakrash (`jmp .loop_start`) va undan oldingi shartli chiqish (`jge`) sikl strukturasi (for/while loop) ning yaqqol belgisi hisoblanadi.

## Ishlash natijasi:
```text
Sikl n marta aylanib, 0 dan n-1 gacha sonlar yig'indisini qaytaradi.
```


# 803-Topshiriq: Switch/Case operatori va Sakrash jadvali (Jump Table) tahlili
## Topshiriq sharti:
Reverse engineering va disassembly tahlili: Switch/Case operatori va Sakrash jadvali (Jump Table) tahlili.

## Yechim (Assembly kodi):
```assembly
; switch (x) { case 0: ...; case 1: ...; case 2: ...; }
; Disassembly:
cmp edi, 3
ja .L_default            ; chegaradan oshsa defaultga
lea rdx, [rip + jump_table]
movsxd rax, dword [rdx + rdi*4]
add rax, rdx
jmp rax                  ; bevosita manzilga sakrash (indirect jump)

section .rodata
jump_table:
    dd .case0 - jump_table
    dd .case1 - jump_table
    dd .case2 - jump_table
    dd .case3 - jump_table
```

## Tushuntirish va Mantiq:
Kompilyatorlar ko'p tarmoqli switch operatorlarini samarali qilish uchun `jmp [table + index*4]` ko'rinishidagi sakrash jadvallarini tuzadi. Bu O(1) vaqt murakkabligini beradi.

## Ishlash natijasi:
```text
Tanlangan indeks bo'yicha tegishli case blokiga to'g'ridan-to'g'ri o'tiladi.
```


# 804-Topshiriq: Strukturaga murojaat (Struct member access) tahlili
## Topshiriq sharti:
Reverse engineering va disassembly tahlili: Strukturaga murojaat (Struct member access) tahlili.

## Yechim (Assembly kodi):
```assembly
; struct User { int id; char role; double balance; };
; Disassembly tahlili:
mov eax, [rdi]           ; ofset 0: id (int, 4 bayt)
movzx edx, byte [rdi+4]  ; ofset 4: role (char, 1 bayt)
movsd xmm0, [rdi+8]      ; ofset 8: balance (padding 3 baytdan so'ng 8 bayt double)
ret
```

## Tushuntirish va Mantiq:
Baza registriga ofset qo'shib murojaat qilish (`[rdi + offset]`) xotiradagi C strukturasi (`struct`) a'zolarini o'qish naqshidir.

## Ishlash natijasi:
```text
Struktura a'zolari ofsetlari (0, 4, 8) orqali aniqlanadi.
```


# 805-Topshiriq: Funksiya chaqiruvi tahlili: Fastcall vs System V ABI
## Topshiriq sharti:
Reverse engineering va disassembly tahlili: Funksiya chaqiruvi tahlili: Fastcall vs System V ABI.

## Yechim (Assembly kodi):
```assembly
; x86_64 System V ABI (Linux):
; Argumentlar tartibi: RDI, RSI, RDX, RCX, R8, R9
mov rdi, 10              ; 1-argument
mov rsi, 20              ; 2-argument
call calculate

; Windows x64 ABI:
; Argumentlar: RCX, RDX, R8, R9 va 32-bayt shadow space
sub rsp, 40              ; 32 bayt shadow space + 8 tekislash
mov rcx, 10              ; 1-argument
mov rdx, 20              ; 2-argument
call calculate
add rsp, 40
```

## Tushuntirish va Mantiq:
Reverse engineeringda operatsion tizimni aniqlash va funksiyalarga nima uzatilayotganini tushunish uchun ABI chaqiruv konvensiyasini bilish muhimdir.

## Ishlash natijasi:
```text
Linux va Windows ABI argument uzatish registrlari farqi yaqqol namoyon bo'ladi.
```


# 806-Topshiriq: Optimizatsiya qilingan ko'paytirish (LEA va siljitishlar)
## Topshiriq sharti:
Reverse engineering va disassembly tahlili: Optimizatsiya qilingan ko'paytirish (LEA va siljitishlar).

## Yechim (Assembly kodi):
```assembly
; C: x * 10
; Kompilyator imul o'rniga LEA kombinatsiyasini qo'llaydi:
lea eax, [rdi + rdi*4]   ; eax = x * 5
shl eax, 1               ; eax = (x * 5) * 2 = x * 10
ret
```

## Tushuntirish va Mantiq:
Reverse engineering jarayonida `imul` buyrug'i bo'lmasa ham, `lea` va `shl` ketma-ketligi o'zgarmas songa ko'paytirish optimizatsiyasi ekanligini ko'rsatadi.

## Ishlash natijasi:
```text
Funksiya kiruvchi argumentni 10 ga ko'paytirib qaytaradi.
```


# 807-Topshiriq: Optimizatsiya qilingan bo'lish: Sehrli sonlar (Magic Numbers / Reciprocal Multiplication)
## Topshiriq sharti:
Reverse engineering va disassembly tahlili: Optimizatsiya qilingan bo'lish: Sehrli sonlar (Magic Numbers / Reciprocal Multiplication).

## Yechim (Assembly kodi):
```assembly
; C: x / 3 (unsigned)
; Kompilyator div o'rniga ko'paytirish qo'llaydi:
mov eax, edi
mov edx, 0xAAAAAAAB     ; Sehrli multiplikator (2^33 / 3)
mul rdx                  ; rdx:rax = x * magic
shr rdx, 1               ; rdx = x / 3
mov eax, edx
ret
```

## Tushuntirish va Mantiq:
Bo'lish (`div`) protsessorda ko'p takt oladi. Kompilyatorlar o'zgarmas songa bo'lishni ko'paytirish va siljitish bilan almashtiradi (reciprocal multiplication).

## Ishlash natijasi:
```text
Kiruvchi son 3 ga aniq bo'linadi.
```


# 808-Topshiriq: Rekursiya tahlili: Fibonachchi funksiyasi
## Topshiriq sharti:
Reverse engineering va disassembly tahlili: Rekursiya tahlili: Fibonachchi funksiyasi.

## Yechim (Assembly kodi):
```assembly
fib:
    push rbp
    push rbx
    sub rsp, 8
    mov ebx, edi
    cmp ebx, 1
    jle .base_case
    lea edi, [ebx-1]
    call fib
    mov ebp, eax
    lea edi, [ebx-2]
    call fib
    add eax, ebp
    jmp .done
.base_case:
    mov eax, ebx
.done:
    add rsp, 8
    pop rbx
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Funksiya o'zining ichida o'zini qayta chaqirishi (`call fib`) va bazaviy shart (`jle .base_case`) rekursiyani belgilaydi.

## Ishlash natijasi:
```text
N-chi Fibonachchi soni hisoblanadi.
```


# 809-Topshiriq: ARM64 Disassembly: Shartli tanlash (CSEL) ni tahlil qilish
## Topshiriq sharti:
Reverse engineering va disassembly tahlili: ARM64 Disassembly: Shartli tanlash (CSEL) ni tahlil qilish.

## Yechim (Assembly kodi):
```assembly
// ARM64 disassembly:
// C: return (a > b) ? a : b;
cmp w0, w1
csel w0, w0, w1, gt
ret
```

## Tushuntirish va Mantiq:
ARM64 arxitekturasida filial bashoratini (branch prediction miss) chetlab o'tish uchun tarmoqlanmasdan tanlash buyrug'i `csel` ishlatiladi.

## Ishlash natijasi:
```text
Ikkita sondan kattasi registrda qaytariladi.
```


# 810-Topshiriq: Objdump va Disassembly vositalaridan foydalanish buyruqlari
## Topshiriq sharti:
Reverse engineering va disassembly tahlili: Objdump va Disassembly vositalaridan foydalanish buyruqlari.

## Yechim (Assembly kodi):
```assembly
; objdump buyruqlari tahlili:
; 1. To'liq disassembly ko'rish: objdump -M intel -d binary.elf
; 2. Barcha bo'limlar bilan birga ko'rish: objdump -D binary.elf
; 3. Relocation jadvallarini ko'rish: readelf -r binary.elf
; 4. Dinamik kutubxonalarni ko'rish: ldd binary.elf
```

## Tushuntirish va Mantiq:
Teskari muhandislikda `objdump` va `readelf` vositalari mashina kodini inson o'qiy oladigan assembly formatiga aylantirishda asosiy qurol hisoblanadi.

## Ishlash natijasi:
```text
ELF binar faylining ichki strukturasini to'liq ko'rish imkoniyati ta'minlanadi.
```


# 811-Topshiriq: Reverse engineering tahlil texnikasi #1
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #1 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #1
; Ghidra / IDA Pro decompiler tahlili
func_re_1:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x0101
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #1 logikasi tiklandi (deobfuscation qilindi).
```


# 812-Topshiriq: Reverse engineering tahlil texnikasi #2
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #2 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #2
; Ghidra / IDA Pro decompiler tahlili
func_re_2:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x0202
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #2 logikasi tiklandi (deobfuscation qilindi).
```


# 813-Topshiriq: Reverse engineering tahlil texnikasi #3
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #3 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #3
; Ghidra / IDA Pro decompiler tahlili
func_re_3:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x0303
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #3 logikasi tiklandi (deobfuscation qilindi).
```


# 814-Topshiriq: Reverse engineering tahlil texnikasi #4
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #4 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #4
; Ghidra / IDA Pro decompiler tahlili
func_re_4:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x0404
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #4 logikasi tiklandi (deobfuscation qilindi).
```


# 815-Topshiriq: Reverse engineering tahlil texnikasi #5
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #5 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #5
; Ghidra / IDA Pro decompiler tahlili
func_re_5:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x0505
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #5 logikasi tiklandi (deobfuscation qilindi).
```


# 816-Topshiriq: Reverse engineering tahlil texnikasi #6
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #6 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #6
; Ghidra / IDA Pro decompiler tahlili
func_re_6:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x0606
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #6 logikasi tiklandi (deobfuscation qilindi).
```


# 817-Topshiriq: Reverse engineering tahlil texnikasi #7
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #7 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #7
; Ghidra / IDA Pro decompiler tahlili
func_re_7:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x0707
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #7 logikasi tiklandi (deobfuscation qilindi).
```


# 818-Topshiriq: Reverse engineering tahlil texnikasi #8
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #8 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #8
; Ghidra / IDA Pro decompiler tahlili
func_re_8:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x0808
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #8 logikasi tiklandi (deobfuscation qilindi).
```


# 819-Topshiriq: Reverse engineering tahlil texnikasi #9
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #9 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #9
; Ghidra / IDA Pro decompiler tahlili
func_re_9:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x0909
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #9 logikasi tiklandi (deobfuscation qilindi).
```


# 820-Topshiriq: Reverse engineering tahlil texnikasi #10
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #10 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #10
; Ghidra / IDA Pro decompiler tahlili
func_re_10:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x0A0A
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #10 logikasi tiklandi (deobfuscation qilindi).
```


# 821-Topshiriq: Reverse engineering tahlil texnikasi #11
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #11 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #11
; Ghidra / IDA Pro decompiler tahlili
func_re_11:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x0B0B
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #11 logikasi tiklandi (deobfuscation qilindi).
```


# 822-Topshiriq: Reverse engineering tahlil texnikasi #12
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #12 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #12
; Ghidra / IDA Pro decompiler tahlili
func_re_12:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x0C0C
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #12 logikasi tiklandi (deobfuscation qilindi).
```


# 823-Topshiriq: Reverse engineering tahlil texnikasi #13
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #13 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #13
; Ghidra / IDA Pro decompiler tahlili
func_re_13:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x0D0D
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #13 logikasi tiklandi (deobfuscation qilindi).
```


# 824-Topshiriq: Reverse engineering tahlil texnikasi #14
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #14 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #14
; Ghidra / IDA Pro decompiler tahlili
func_re_14:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x0E0E
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #14 logikasi tiklandi (deobfuscation qilindi).
```


# 825-Topshiriq: Reverse engineering tahlil texnikasi #15
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #15 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #15
; Ghidra / IDA Pro decompiler tahlili
func_re_15:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x0F0F
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #15 logikasi tiklandi (deobfuscation qilindi).
```


# 826-Topshiriq: Reverse engineering tahlil texnikasi #16
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #16 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #16
; Ghidra / IDA Pro decompiler tahlili
func_re_16:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x1010
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #16 logikasi tiklandi (deobfuscation qilindi).
```


# 827-Topshiriq: Reverse engineering tahlil texnikasi #17
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #17 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #17
; Ghidra / IDA Pro decompiler tahlili
func_re_17:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x1111
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #17 logikasi tiklandi (deobfuscation qilindi).
```


# 828-Topshiriq: Reverse engineering tahlil texnikasi #18
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #18 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #18
; Ghidra / IDA Pro decompiler tahlili
func_re_18:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x1212
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #18 logikasi tiklandi (deobfuscation qilindi).
```


# 829-Topshiriq: Reverse engineering tahlil texnikasi #19
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #19 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #19
; Ghidra / IDA Pro decompiler tahlili
func_re_19:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x1313
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #19 logikasi tiklandi (deobfuscation qilindi).
```


# 830-Topshiriq: Reverse engineering tahlil texnikasi #20
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #20 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #20
; Ghidra / IDA Pro decompiler tahlili
func_re_20:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x1414
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #20 logikasi tiklandi (deobfuscation qilindi).
```


# 831-Topshiriq: Reverse engineering tahlil texnikasi #21
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #21 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #21
; Ghidra / IDA Pro decompiler tahlili
func_re_21:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x1515
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #21 logikasi tiklandi (deobfuscation qilindi).
```


# 832-Topshiriq: Reverse engineering tahlil texnikasi #22
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #22 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #22
; Ghidra / IDA Pro decompiler tahlili
func_re_22:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x1616
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #22 logikasi tiklandi (deobfuscation qilindi).
```


# 833-Topshiriq: Reverse engineering tahlil texnikasi #23
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #23 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #23
; Ghidra / IDA Pro decompiler tahlili
func_re_23:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x1717
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #23 logikasi tiklandi (deobfuscation qilindi).
```


# 834-Topshiriq: Reverse engineering tahlil texnikasi #24
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #24 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #24
; Ghidra / IDA Pro decompiler tahlili
func_re_24:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x1818
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #24 logikasi tiklandi (deobfuscation qilindi).
```


# 835-Topshiriq: Reverse engineering tahlil texnikasi #25
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #25 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #25
; Ghidra / IDA Pro decompiler tahlili
func_re_25:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x1919
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #25 logikasi tiklandi (deobfuscation qilindi).
```


# 836-Topshiriq: Reverse engineering tahlil texnikasi #26
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #26 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #26
; Ghidra / IDA Pro decompiler tahlili
func_re_26:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x1A1A
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #26 logikasi tiklandi (deobfuscation qilindi).
```


# 837-Topshiriq: Reverse engineering tahlil texnikasi #27
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #27 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #27
; Ghidra / IDA Pro decompiler tahlili
func_re_27:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x1B1B
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #27 logikasi tiklandi (deobfuscation qilindi).
```


# 838-Topshiriq: Reverse engineering tahlil texnikasi #28
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #28 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #28
; Ghidra / IDA Pro decompiler tahlili
func_re_28:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x1C1C
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #28 logikasi tiklandi (deobfuscation qilindi).
```


# 839-Topshiriq: Reverse engineering tahlil texnikasi #29
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #29 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #29
; Ghidra / IDA Pro decompiler tahlili
func_re_29:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x1D1D
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #29 logikasi tiklandi (deobfuscation qilindi).
```


# 840-Topshiriq: Reverse engineering tahlil texnikasi #30
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #30 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #30
; Ghidra / IDA Pro decompiler tahlili
func_re_30:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x1E1E
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #30 logikasi tiklandi (deobfuscation qilindi).
```


# 841-Topshiriq: Reverse engineering tahlil texnikasi #31
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #31 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #31
; Ghidra / IDA Pro decompiler tahlili
func_re_31:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x1F1F
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #31 logikasi tiklandi (deobfuscation qilindi).
```


# 842-Topshiriq: Reverse engineering tahlil texnikasi #32
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #32 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #32
; Ghidra / IDA Pro decompiler tahlili
func_re_32:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x2020
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #32 logikasi tiklandi (deobfuscation qilindi).
```


# 843-Topshiriq: Reverse engineering tahlil texnikasi #33
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #33 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #33
; Ghidra / IDA Pro decompiler tahlili
func_re_33:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x2121
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #33 logikasi tiklandi (deobfuscation qilindi).
```


# 844-Topshiriq: Reverse engineering tahlil texnikasi #34
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #34 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #34
; Ghidra / IDA Pro decompiler tahlili
func_re_34:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x2222
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #34 logikasi tiklandi (deobfuscation qilindi).
```


# 845-Topshiriq: Reverse engineering tahlil texnikasi #35
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #35 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #35
; Ghidra / IDA Pro decompiler tahlili
func_re_35:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x2323
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #35 logikasi tiklandi (deobfuscation qilindi).
```


# 846-Topshiriq: Reverse engineering tahlil texnikasi #36
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #36 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #36
; Ghidra / IDA Pro decompiler tahlili
func_re_36:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x2424
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #36 logikasi tiklandi (deobfuscation qilindi).
```


# 847-Topshiriq: Reverse engineering tahlil texnikasi #37
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #37 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #37
; Ghidra / IDA Pro decompiler tahlili
func_re_37:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x2525
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #37 logikasi tiklandi (deobfuscation qilindi).
```


# 848-Topshiriq: Reverse engineering tahlil texnikasi #38
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #38 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #38
; Ghidra / IDA Pro decompiler tahlili
func_re_38:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x2626
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #38 logikasi tiklandi (deobfuscation qilindi).
```


# 849-Topshiriq: Reverse engineering tahlil texnikasi #39
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #39 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #39
; Ghidra / IDA Pro decompiler tahlili
func_re_39:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x2727
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #39 logikasi tiklandi (deobfuscation qilindi).
```


# 850-Topshiriq: Reverse engineering tahlil texnikasi #40
## Topshiriq sharti:
Teskari muhandislik bo'yicha Reverse engineering tahlil texnikasi #40 talabini bajaring.

## Yechim (Assembly kodi):
```assembly
; Reverse Engineering tahlil namunasi #40
; Ghidra / IDA Pro decompiler tahlili
func_re_40:
    push rbp
    mov rbp, rsp
    mov dword [rbp-4], edi
    mov eax, [rbp-4]
    xor eax, 0x2828
    rol eax, 3
    pop rbp
    ret
```

## Tushuntirish va Mantiq:
Tahlil jarayonida `xor` va `rol` ketma-ketligi ma'lumotlarni shifrlash (obfuscation) yoki xesh hisoblash algoritmi belgisi sifatida namoyon bo'ladi.

## Ishlash natijasi:
```text
Algoritm #40 logikasi tiklandi (deobfuscation qilindi).
```

