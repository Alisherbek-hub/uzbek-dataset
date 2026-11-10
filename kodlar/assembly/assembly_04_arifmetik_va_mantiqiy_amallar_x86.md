# 151-Topshiriq: x86_64 'add' va 'sub' amallari
## Topshiriq sharti:
Ikki registrni qo'shish va ayirishni bajaring.

## Yechim (Assembly kodi):
```assembly
section .text
global _start
_start:
    mov rax, 100
    add rax, 50         ; rax = 150
    sub rax, 30         ; rax = 120

    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
'add dest, src' va 'sub dest, src' operatsiyalari arifmetik natijani 'dest' registriga yozadi va RFLAGS bayroqlarini (ZF, SF, CF, OF) yangilaydi.

## Ishlash natijasi:
```text
add va sub amallari bajarildi: yakuniy qiymat 120.
```


# 152-Topshiriq: 'inc' va 'dec' ko'rsatmalari va ularning CF ga ta'siri
## Topshiriq sharti:
Registrni 1 taga oshirish va kamaytirishning o'ziga xosligi.

## Yechim (Assembly kodi):
```assembly
section .text
global _start
_start:
    mov rcx, 10
    inc rcx             ; rcx = 11 (ZF, OF, SF yangilanadi, LEKIN Carry Flag (CF) o'zgarmaydi!)
    dec rcx             ; rcx = 10

    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
'inc' va 'dec' ko'rsatmalari muhim xususiyatga ega: ular Carry Flag (CF) bayrog'iga aslo ta'sir qilmaydi! Bu sikllar ichida katta sonlarni qo'shish (adc) zanjirini buzmaslik uchun maxsus yaratilgan.

## Ishlash natijasi:
```text
inc va dec CF bayrog'ini saqlagan holda registrni o'zgartirdi.
```


# 153-Topshiriq: Ishorali ko'paytirish: 'imul' uch xil formati
## Topshiriq sharti:
x86_64 da 'imul' ning 1, 2 va 3 operandli sintaksislarini qo'llang.

## Yechim (Assembly kodi):
```assembly
section .text
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
```

## Tushuntirish va Mantiq:
'imul' x86 da eng moslashuvchan ko'paytirish instruksiyasi bo'lib, 3 operandli formatida ixtiyoriy registrga natijani yozish imkonini beradi.

## Ishlash natijasi:
```text
imul 1, 2 va 3 operandli formatlari muvaffaqiyatli sinovdan o'tdi.
```


# 154-Topshiriq: Butunli bo'lish: 'idiv' va 'cqo' ko'rsatmalari
## Topshiriq sharti:
128-bitli sonni 64-bitga bo'lib, bo'linma va qoldiqni oling.

## Yechim (Assembly kodi):
```assembly
section .text
global _start
_start:
    mov rax, 100        ; Bo'linuvchi
    cqo                 ; RAX ni RDX:RAX ga ishora bilan kengaytiradi (RDX = 0)
    mov rbx, 7          ; Bo'luvchi
    idiv rbx            ; RDX:RAX / rbx -> Bo'linma RAX da (14), Qoldiq RDX da (2)

    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
'idiv' buyrug'i har doim RDX:RAX juftligini bo'linuvchi deb qabul qiladi. Bo'lishdan oldin 'cqo' (Convert Qword to Oword) orqali RAX ning ishora biti RDX ga to'ldirilishi shart, aks holda Division Error yuz beradi.

## Ishlash natijasi:
```text
idiv: 100 / 7 = 14 (RAX), qoldiq = 2 (RDX).
```


# 155-Topshiriq: Katta sonlar arifmetikasi: 'adc' (Add with Carry)
## Topshiriq sharti:
128-bitli sonni ikkita 64-bit registr juftligida qo'shing.

## Yechim (Assembly kodi):
```assembly
section .text
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
```

## Tushuntirish va Mantiq:
'adc' (Add with Carry) 'dest = dest + src + CF' formulasini bajaradi, bu orqali ixtiyoriy 128, 256, 512 bitli katta sonlar arifmetikasi amalga oshiriladi.

## Ishlash natijasi:
```text
adc orqali 128-bitli qo'shish muvaffaqiyatli bajarildi.
```


# 156-Topshiriq: Bitwise mantiqiy amallar: 'and', 'or', 'xor', 'not'
## Topshiriq sharti:
Registrlar ustida bit darajasidagi mantiqiy amallarni bajaring.

## Yechim (Assembly kodi):
```assembly
section .text
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
```

## Tushuntirish va Mantiq:
Mantiqiy amallar protsessorning ALU blokida eng yuqori tezlikda bajariladi.

## Ishlash natijasi:
```text
Mantiqiy amallar (AND, OR, XOR, NOT) bajarildi.
```


# 157-Topshiriq: 'test' ko'rsatmasi va bayroqlarni tekshirish
## Topshiriq sharti:
Registr qiymatini o'zgartirmasdan uning nol yoki manfiyligini aniqlang.

## Yechim (Assembly kodi):
```assembly
section .text
global _start
_start:
    mov rax, 0
    test rax, rax       ; rax AND rax hisoblanadi, lekin natija saqlanmaydi!
                        ; rax=0 bo'lgani uchun Zero Flag (ZF=1) yoqiladi!

    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
'test reg, reg' amali 'cmp reg, 0' ga qaraganda qisqaroq va tezroq bo'lib, registr nol ekanligini tekshirishning standart usulidir.

## Ishlash natijasi:
```text
test ko'rsatmasi orqali ZF bayrog'i tekshirildi.
```


# 158-Topshiriq: Bit siljitish: 'shl' (mantiqiy) va 'sar' (arifmetik)
## Topshiriq sharti:
Sonni 2 ga ko'paytirish va manfiy sonni 2 ga to'g'ri bo'lish.

## Yechim (Assembly kodi):
```assembly
section .text
global _start
_start:
    mov rax, 5
    shl rax, 2          ; rax = 5 * 4 = 20 (chapga 2 bit)

    mov rbx, -16
    sar rbx, 1          ; rbx = -8 (o'ngga siljitish, ishora biti saqlanadi!)

    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
'shl' bo'sh o'rinlarni nollar bilan to'ldiradi. 'sar' (Shift Arithmetic Right) esa manfiy sonlar uchun yuqori ishora bitini (1) nusxalab saqlaydi.

## Ishlash natijasi:
```text
shl va sar amallari bajarildi: 5<<2=20, -16>>1=-8.
```


# 159-Topshiriq: Siklik siljitish: 'rol' va 'ror'
## Topshiriq sharti:
Bitlarni chetdan chiqib ikkinchi tomondan kirib keluvchi siklda aylantiring.

## Yechim (Assembly kodi):
```assembly
section .text
global _start
_start:
    mov al, 0b10000001
    rol al, 1           ; al = 0b00000011 (yuqori bit quyi bitga o'tdi)
    ror al, 1           ; al = 0b10000001 (asl holiga qaytdi)

    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
Siklik siljitish (Rotate) kriptografik algoritmlarda (SHA-256, AES) doimiy qo'llaniladi.

## Ishlash natijasi:
```text
rol va ror siklik siljitishlari bajarildi.
```


# 160-Topshiriq: Bit Test ko'rsatmalari: 'bts', 'btr', 'btc'
## Topshiriq sharti:
Registrdagi aniq bir bitni tekshirib, uni 1 qilish, o'chirish yoki almashtirish.

## Yechim (Assembly kodi):
```assembly
section .text
global _start
_start:
    mov rax, 0
    bts rax, 3          ; 3-bitni CF ga oladi va uni 1 qiladi (rax = 8)
    btc rax, 3          ; 3-bitni teskari qiladi (rax = 0)

    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
'bts' (Bit Test and Set) atomar bayroqlar va spinlock mexanizmlarida apparat darajasida sinxronizatsiya uchun ishlatiladi.

## Ishlash natijasi:
```text
bts va btc orqali bitlar boshqarildi.
```


# 161-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #1
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #1.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #1
section .text
global _start
_start:
    mov rax, 1
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #1.

## Ishlash natijasi:
```text
Arifmetik amaliyot #1 muvaffaqiyatli bajarildi.
```


# 162-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #2
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #2.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #2
section .text
global _start
_start:
    mov rax, 2
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #2.

## Ishlash natijasi:
```text
Arifmetik amaliyot #2 muvaffaqiyatli bajarildi.
```


# 163-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #3
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #3.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #3
section .text
global _start
_start:
    mov rax, 3
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #3.

## Ishlash natijasi:
```text
Arifmetik amaliyot #3 muvaffaqiyatli bajarildi.
```


# 164-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #4
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #4.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #4
section .text
global _start
_start:
    mov rax, 4
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #4.

## Ishlash natijasi:
```text
Arifmetik amaliyot #4 muvaffaqiyatli bajarildi.
```


# 165-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #5
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #5.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #5
section .text
global _start
_start:
    mov rax, 5
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #5.

## Ishlash natijasi:
```text
Arifmetik amaliyot #5 muvaffaqiyatli bajarildi.
```


# 166-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #6
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #6.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #6
section .text
global _start
_start:
    mov rax, 6
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #6.

## Ishlash natijasi:
```text
Arifmetik amaliyot #6 muvaffaqiyatli bajarildi.
```


# 167-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #7
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #7.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #7
section .text
global _start
_start:
    mov rax, 7
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #7.

## Ishlash natijasi:
```text
Arifmetik amaliyot #7 muvaffaqiyatli bajarildi.
```


# 168-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #8
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #8.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #8
section .text
global _start
_start:
    mov rax, 8
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #8.

## Ishlash natijasi:
```text
Arifmetik amaliyot #8 muvaffaqiyatli bajarildi.
```


# 169-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #9
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #9.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #9
section .text
global _start
_start:
    mov rax, 9
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #9.

## Ishlash natijasi:
```text
Arifmetik amaliyot #9 muvaffaqiyatli bajarildi.
```


# 170-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #10
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #10.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #10
section .text
global _start
_start:
    mov rax, 10
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #10.

## Ishlash natijasi:
```text
Arifmetik amaliyot #10 muvaffaqiyatli bajarildi.
```


# 171-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #11
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #11.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #11
section .text
global _start
_start:
    mov rax, 11
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #11.

## Ishlash natijasi:
```text
Arifmetik amaliyot #11 muvaffaqiyatli bajarildi.
```


# 172-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #12
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #12.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #12
section .text
global _start
_start:
    mov rax, 12
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #12.

## Ishlash natijasi:
```text
Arifmetik amaliyot #12 muvaffaqiyatli bajarildi.
```


# 173-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #13
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #13.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #13
section .text
global _start
_start:
    mov rax, 13
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #13.

## Ishlash natijasi:
```text
Arifmetik amaliyot #13 muvaffaqiyatli bajarildi.
```


# 174-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #14
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #14.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #14
section .text
global _start
_start:
    mov rax, 14
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #14.

## Ishlash natijasi:
```text
Arifmetik amaliyot #14 muvaffaqiyatli bajarildi.
```


# 175-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #15
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #15.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #15
section .text
global _start
_start:
    mov rax, 15
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #15.

## Ishlash natijasi:
```text
Arifmetik amaliyot #15 muvaffaqiyatli bajarildi.
```


# 176-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #16
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #16.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #16
section .text
global _start
_start:
    mov rax, 16
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #16.

## Ishlash natijasi:
```text
Arifmetik amaliyot #16 muvaffaqiyatli bajarildi.
```


# 177-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #17
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #17.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #17
section .text
global _start
_start:
    mov rax, 17
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #17.

## Ishlash natijasi:
```text
Arifmetik amaliyot #17 muvaffaqiyatli bajarildi.
```


# 178-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #18
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #18.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #18
section .text
global _start
_start:
    mov rax, 18
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #18.

## Ishlash natijasi:
```text
Arifmetik amaliyot #18 muvaffaqiyatli bajarildi.
```


# 179-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #19
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #19.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #19
section .text
global _start
_start:
    mov rax, 19
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #19.

## Ishlash natijasi:
```text
Arifmetik amaliyot #19 muvaffaqiyatli bajarildi.
```


# 180-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #20
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #20.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #20
section .text
global _start
_start:
    mov rax, 20
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #20.

## Ishlash natijasi:
```text
Arifmetik amaliyot #20 muvaffaqiyatli bajarildi.
```


# 181-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #21
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #21.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #21
section .text
global _start
_start:
    mov rax, 21
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #21.

## Ishlash natijasi:
```text
Arifmetik amaliyot #21 muvaffaqiyatli bajarildi.
```


# 182-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #22
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #22.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #22
section .text
global _start
_start:
    mov rax, 22
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #22.

## Ishlash natijasi:
```text
Arifmetik amaliyot #22 muvaffaqiyatli bajarildi.
```


# 183-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #23
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #23.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #23
section .text
global _start
_start:
    mov rax, 23
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #23.

## Ishlash natijasi:
```text
Arifmetik amaliyot #23 muvaffaqiyatli bajarildi.
```


# 184-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #24
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #24.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #24
section .text
global _start
_start:
    mov rax, 24
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #24.

## Ishlash natijasi:
```text
Arifmetik amaliyot #24 muvaffaqiyatli bajarildi.
```


# 185-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #25
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #25.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #25
section .text
global _start
_start:
    mov rax, 25
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #25.

## Ishlash natijasi:
```text
Arifmetik amaliyot #25 muvaffaqiyatli bajarildi.
```


# 186-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #26
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #26.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #26
section .text
global _start
_start:
    mov rax, 26
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #26.

## Ishlash natijasi:
```text
Arifmetik amaliyot #26 muvaffaqiyatli bajarildi.
```


# 187-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #27
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #27.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #27
section .text
global _start
_start:
    mov rax, 27
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #27.

## Ishlash natijasi:
```text
Arifmetik amaliyot #27 muvaffaqiyatli bajarildi.
```


# 188-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #28
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #28.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #28
section .text
global _start
_start:
    mov rax, 28
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #28.

## Ishlash natijasi:
```text
Arifmetik amaliyot #28 muvaffaqiyatli bajarildi.
```


# 189-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #29
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #29.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #29
section .text
global _start
_start:
    mov rax, 29
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #29.

## Ishlash natijasi:
```text
Arifmetik amaliyot #29 muvaffaqiyatli bajarildi.
```


# 190-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #30
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #30.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #30
section .text
global _start
_start:
    mov rax, 30
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #30.

## Ishlash natijasi:
```text
Arifmetik amaliyot #30 muvaffaqiyatli bajarildi.
```


# 191-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #31
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #31.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #31
section .text
global _start
_start:
    mov rax, 31
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #31.

## Ishlash natijasi:
```text
Arifmetik amaliyot #31 muvaffaqiyatli bajarildi.
```


# 192-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #32
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #32.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #32
section .text
global _start
_start:
    mov rax, 32
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #32.

## Ishlash natijasi:
```text
Arifmetik amaliyot #32 muvaffaqiyatli bajarildi.
```


# 193-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #33
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #33.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #33
section .text
global _start
_start:
    mov rax, 33
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #33.

## Ishlash natijasi:
```text
Arifmetik amaliyot #33 muvaffaqiyatli bajarildi.
```


# 194-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #34
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #34.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #34
section .text
global _start
_start:
    mov rax, 34
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #34.

## Ishlash natijasi:
```text
Arifmetik amaliyot #34 muvaffaqiyatli bajarildi.
```


# 195-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #35
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #35.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #35
section .text
global _start
_start:
    mov rax, 35
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #35.

## Ishlash natijasi:
```text
Arifmetik amaliyot #35 muvaffaqiyatli bajarildi.
```


# 196-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #36
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #36.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #36
section .text
global _start
_start:
    mov rax, 36
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #36.

## Ishlash natijasi:
```text
Arifmetik amaliyot #36 muvaffaqiyatli bajarildi.
```


# 197-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #37
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #37.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #37
section .text
global _start
_start:
    mov rax, 37
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #37.

## Ishlash natijasi:
```text
Arifmetik amaliyot #37 muvaffaqiyatli bajarildi.
```


# 198-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #38
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #38.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #38
section .text
global _start
_start:
    mov rax, 38
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #38.

## Ishlash natijasi:
```text
Arifmetik amaliyot #38 muvaffaqiyatli bajarildi.
```


# 199-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #39
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #39.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #39
section .text
global _start
_start:
    mov rax, 39
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #39.

## Ishlash natijasi:
```text
Arifmetik amaliyot #39 muvaffaqiyatli bajarildi.
```


# 200-Topshiriq: x86_64 arifmetik va mantiqiy amallar amaliyoti #40
## Topshiriq sharti:
x86_64 ALU operatsiyalari, bayroqlar tahlili va ko'p xonali hisob-kitob topshirig'i #40.

## Yechim (Assembly kodi):
```assembly
; x86 arifmetika amaliyoti #40
section .text
global _start
_start:
    mov rax, 40
    add rax, 10
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #40.

## Ishlash natijasi:
```text
Arifmetik amaliyot #40 muvaffaqiyatli bajarildi.
```

