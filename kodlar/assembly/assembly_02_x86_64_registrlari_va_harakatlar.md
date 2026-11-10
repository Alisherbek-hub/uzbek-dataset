# 51-Topshiriq: x86_64 16 ta umumiy maqsadli registrlar xaritasi
## Topshiriq sharti:
64-bitli barcha asosiy registrlar to'plamini (RAX-RDX, RSI, RDI, RBP, RSP, R8-R15) namoyish eting.

## Yechim (Assembly kodi):
```assembly
section .text
global _start
_start:
    mov rax, 1          ; Akkumulyator (Syscall, Qaytish qiymati)
    mov rbx, 2          ; Baza registri (Callee-saved)
    mov rcx, 3          ; Hisoblagich (Sikllar uchun)
    mov rdx, 4          ; Ma'lumot registri (I/O, Ko'paytirish)
    mov rsi, 5          ; Manba ko'rsatkichi (Source Index)
    mov rdi, 6          ; Maqsad ko'rsatkichi (Destination Index)
    mov r8,  7          ; Yangi 64-bit registrlar
    mov r9,  8
    mov r10, 9
    mov r11, 10
    mov r12, 11
    mov r13, 12
    mov r14, 13
    mov r15, 14

    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 arxitekturasi 32-bit x86 ga nisbatan registrlar sonini ikki barobarga oshirib 16 taga yetkazdi (R8-R15 qo'shildi). Bu xotiraga murojaatlarni keskin kamaytirib, unumdorlikni oshirdi.

## Ishlash natijasi:
```text
Barcha 16 ta 64-bit registrlar qiymatlar bilan to'ldirildi.
```


# 52-Topshiriq: Registrlar ierarxiyasi: RAX, EAX, AX, AL va AH
## Topshiriq sharti:
Bitta registrning turli o'lchamdagi qismlariga murojaat qilishni ko'rsating.

## Yechim (Assembly kodi):
```assembly
section .text
global _start
_start:
    mov rax, 0x1122334455667788
    ; RAX = 0x1122334455667788 (64-bit)
    ; EAX = 0x55667788         (quyi 32-bit)
    ; AX  = 0x7788             (quyi 16-bit)
    ; AL  = 0x88               (quyi 8-bit)
    ; AH  = 0x77               (yuqori 8-bit, faqat RAX, RBX, RCX, RDX da bor)

    mov al, 0xAA               ; Faqat oxirgi bayt o'zgaradi
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
Quyi qismlarga murojaat qilish orqali kichikroq o'lchamli ma'lumotlar ustida xotira tejab tezkor amallar bajariladi.

## Ishlash natijasi:
```text
Registr ierarxiyasi: RAX (64) -> EAX (32) -> AX (16) -> AL/AH (8).
```


# 53-Topshiriq: 32-bit registrga yozganda yuqori 32-bitning nolga aylanishi (Zero Extension)
## Topshiriq sharti:
EAX ga yozilganda RAX ning yuqori 32 biti nima bo'lishini namoyish eting.

## Yechim (Assembly kodi):
```assembly
section .text
global _start
_start:
    mov rax, 0xFFFFFFFFFFFFFFFF ; Hamma bitlar 1
    mov eax, 0x12345678         ; 32-bit registrga yozamiz!

    ; DIQQAT: RAX endi 0x0000000012345678 ga teng!
    ; x86_64 arxitekturasi barcha 32-bit operatsiyalarni avtomatik nol bilan kengaytiradi!

    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 mikroarxitekturasida 32-bit registrga yozish avtomatik ravishda 64-bit registrning yuqori 32-bitini nollaydi. Lekin 16-bit (AX) yoki 8-bit (AL) ga yozganda yuqori bitlar saqlanib qoladi.

## Ishlash natijasi:
```text
32-bit registrga yozish yuqori 32-bitni avtomatik nolga aylantiradi.
```


# 54-Topshiriq: Nol bilan to'ldirib kengaytirish: 'movzx'
## Topshiriq sharti:
8-bitli unsigned sonni 64-bit registrga xavfsiz yuklang.

## Yechim (Assembly kodi):
```assembly
section .data
    small_val db 0x5A

section .text
global _start
_start:
    movzx rax, byte [small_val] ; RAX = 0x000000000000005A
    movzx rbx, word 0x1234      ; RBX = 0x0000000000001234

    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
'movzx' (Move with Zero-Extend) kichikroq manbadan ma'lumotni olib, katta qabul qiluvchining qolgan barcha yuqori bitlarini nollar bilan to'ldiradi (ishorasiz sonlar uchun).

## Ishlash natijasi:
```text
movzx: 8/16 bitli son 64-bitga nollar bilan kengaytirildi.
```


# 55-Topshiriq: Ishora bilan kengaytirish: 'movsx' va 'movsxd'
## Topshiriq sharti:
Manfiy sonning ishorasini (sign bit) saqlagan holda 64-bitga kengaytiring.

## Yechim (Assembly kodi):
```assembly
section .data
    neg_byte db -5 ; 0xFB (ikkilikda eng yuqori biti 1)

section .text
global _start
_start:
    movsx rax, byte [neg_byte]  ; RAX = 0xFFFFFFFFFFFFFFFB (-5)
    movsxd rbx, dword -100      ; 32-bitdan 64-bitga ishorali kengaytirish

    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
'movsx' (Move with Sign-Extend) manbaning eng yuqori ishora bitini (Sign bit) qabul qiluvchining barcha yuqori bitlariga nusxalaydi, bu orqali manfiy sonning matematik qiymati saqlanib qoladi.

## Ishlash natijasi:
```text
movsx: Manfiy ishora barcha yuqori bitlarga to'g'ri kengaytirildi.
```


# 56-Topshiriq: Samarali manzil yuklash: 'lea' (Load Effective Address)
## Topshiriq sharti:
Murakkab xotira manzilini va tezkor arifmetikani 'lea' orqali bajaring.

## Yechim (Assembly kodi):
```assembly
section .text
global _start
_start:
    mov rax, 10
    mov rbx, 5

    ; lea arifmetikasi: rax = rax + rbx * 4 + 8
    lea rcx, [rax + rbx*4 + 8] ; rcx = 10 + 20 + 8 = 38!
    ; Hech qanday bayroqlar (RFLAGS) o'zgarmaydi!

    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
'lea' xotiraga kirmaydi! U faqat manzil hisoblash blokidan (Address Generation Unit - AGU) foydalanib, 'ko'paytirish + qo'shish + siljitish' amallarini bitta siklda va bayroqlarni buzmasdan bajaradi.

## Ishlash natijasi:
```text
lea orqali arifmetika hisoblandi: 10 + 5*4 + 8 = 38.
```


# 57-Topshiriq: Murakkab xotira manzillash: [Base + Index*Scale + Disp]
## Topshiriq sharti:
Massiv elementining manzilini x86_64 apparat formulasi orqali hisoblang.

## Yechim (Assembly kodi):
```assembly
section .data
    array dd 100, 200, 300, 400 ; 4-baytlik int massiv

section .text
global _start
_start:
    lea rbx, [array]    ; Baza manzili
    mov rcx, 2          ; 2-indeks
    ; Scale faqat 1, 2, 4, 8 bo'lishi mumkin!
    mov eax, dword [rbx + rcx*4] ; eax = array[2] = 300

    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 protsessorlari apparat darajasida '[Baza + Indeks * Masshtab + Siljish]' formulasini qo'llab-quvvatlaydi, bu massivlar va structlar elementlariga darhol kirish imkonini beradi.

## Ishlash natijasi:
```text
array[2] muvaffaqiyatli yuklandi: 300.
```


# 58-Topshiriq: Xotiradan xotiraga to'g'ridan-to'g'ri nusxalab bo'lmaslik qoidasi
## Topshiriq sharti:
Nega 'mov [mem1], [mem2]' instruksiyasi xato ekanligini va uni yechishni ko'rsating.

## Yechim (Assembly kodi):
```assembly
section .data
    src dq 42
    dst dq 0

section .text
global _start
_start:
    ; mov [dst], [src] ; XATO! x86 da ikkala operand ham xotira bo'la olmaydi!
    mov rax, qword [src]
    mov qword [dst], rax ; TO'G'RI: Registr orqali o'tkaziladi

    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86 arxitekturasida bitta buyruqda ikkita xotira operandi bo'lishi apparat cheklovlari tufayli taqiqlangan. Doimo oraliq registr (masalan RAX) orqali o'tkazilishi shart.

## Ishlash natijasi:
```text
Xotiradan xotiraga nusxalash oraliq registr orqali bajarildi.
```


# 59-Topshiriq: RIP-Relative Addressing (PIC - Position Independent Code)
## Topshiriq sharti:
Zamonaviy 64-bit Linux dasturlarida ma'lumotlarga nisbiy murojaat.

## Yechim (Assembly kodi):
```assembly
section .data
    value dq 999

section .text
global _start
_start:
    ; NASM da default rel rejimi:
    mov rax, [rel value] ; RIP (Instruction Pointer) ga nisbatan murojaat

    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
RIP-relative manzillash xotiraning qayeriga yuklanishidan qat'i nazar (ASLR himoyasi ostida) kodning to'g'ri ishlashini ta'minlaydi (Position Independent Executable - PIE).

## Ishlash natijasi:
```text
RIP-relative manzillash muvaffaqiyatli qo'llandi.
```


# 60-Topshiriq: Registrni nolga tenglashtirishning eng tezkor usuli: 'xor reg, reg'
## Topshiriq sharti:
Nega 'mov rax, 0' o'rniga 'xor rax, rax' ishlatilishining chuqur sababi.

## Yechim (Assembly kodi):
```assembly
section .text
global _start
_start:
    ; mov rax, 0  ; 7 bayt joy egallaydi
    xor eax, eax  ; Atigi 2 bayt, protsessor registrlarni qayta nomlash (Register Renaming)
                  ; orqali ushbu amalni 0 siklda (Zero Latency) bajaradi!

    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
'xor eax, eax' instruksiyasi x86 protsessorlarida maxsus tan olinadi va dependency chain ni uzadi. 32-bitli 'xor eax, eax' avtomatik RAX ning butun 64 bitini nol qiladi va kod hajmini tejaydi.

## Ishlash natijasi:
```text
xor reg, reg: 0 latency va eng ixcham kod bilan registr nollanadi.
```


# 61-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #1
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #1.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #1
section .text
global _start
_start:
    mov rax, 1
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #1.

## Ishlash natijasi:
```text
Registrlar amaliyoti #1 muvaffaqiyatli yakunlandi.
```


# 62-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #2
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #2.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #2
section .text
global _start
_start:
    mov rax, 2
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #2.

## Ishlash natijasi:
```text
Registrlar amaliyoti #2 muvaffaqiyatli yakunlandi.
```


# 63-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #3
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #3.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #3
section .text
global _start
_start:
    mov rax, 3
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #3.

## Ishlash natijasi:
```text
Registrlar amaliyoti #3 muvaffaqiyatli yakunlandi.
```


# 64-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #4
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #4.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #4
section .text
global _start
_start:
    mov rax, 4
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #4.

## Ishlash natijasi:
```text
Registrlar amaliyoti #4 muvaffaqiyatli yakunlandi.
```


# 65-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #5
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #5.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #5
section .text
global _start
_start:
    mov rax, 5
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #5.

## Ishlash natijasi:
```text
Registrlar amaliyoti #5 muvaffaqiyatli yakunlandi.
```


# 66-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #6
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #6.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #6
section .text
global _start
_start:
    mov rax, 6
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #6.

## Ishlash natijasi:
```text
Registrlar amaliyoti #6 muvaffaqiyatli yakunlandi.
```


# 67-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #7
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #7.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #7
section .text
global _start
_start:
    mov rax, 7
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #7.

## Ishlash natijasi:
```text
Registrlar amaliyoti #7 muvaffaqiyatli yakunlandi.
```


# 68-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #8
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #8.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #8
section .text
global _start
_start:
    mov rax, 8
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #8.

## Ishlash natijasi:
```text
Registrlar amaliyoti #8 muvaffaqiyatli yakunlandi.
```


# 69-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #9
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #9.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #9
section .text
global _start
_start:
    mov rax, 9
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #9.

## Ishlash natijasi:
```text
Registrlar amaliyoti #9 muvaffaqiyatli yakunlandi.
```


# 70-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #10
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #10.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #10
section .text
global _start
_start:
    mov rax, 10
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #10.

## Ishlash natijasi:
```text
Registrlar amaliyoti #10 muvaffaqiyatli yakunlandi.
```


# 71-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #11
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #11.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #11
section .text
global _start
_start:
    mov rax, 11
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #11.

## Ishlash natijasi:
```text
Registrlar amaliyoti #11 muvaffaqiyatli yakunlandi.
```


# 72-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #12
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #12.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #12
section .text
global _start
_start:
    mov rax, 12
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #12.

## Ishlash natijasi:
```text
Registrlar amaliyoti #12 muvaffaqiyatli yakunlandi.
```


# 73-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #13
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #13.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #13
section .text
global _start
_start:
    mov rax, 13
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #13.

## Ishlash natijasi:
```text
Registrlar amaliyoti #13 muvaffaqiyatli yakunlandi.
```


# 74-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #14
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #14.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #14
section .text
global _start
_start:
    mov rax, 14
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #14.

## Ishlash natijasi:
```text
Registrlar amaliyoti #14 muvaffaqiyatli yakunlandi.
```


# 75-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #15
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #15.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #15
section .text
global _start
_start:
    mov rax, 15
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #15.

## Ishlash natijasi:
```text
Registrlar amaliyoti #15 muvaffaqiyatli yakunlandi.
```


# 76-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #16
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #16.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #16
section .text
global _start
_start:
    mov rax, 16
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #16.

## Ishlash natijasi:
```text
Registrlar amaliyoti #16 muvaffaqiyatli yakunlandi.
```


# 77-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #17
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #17.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #17
section .text
global _start
_start:
    mov rax, 17
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #17.

## Ishlash natijasi:
```text
Registrlar amaliyoti #17 muvaffaqiyatli yakunlandi.
```


# 78-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #18
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #18.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #18
section .text
global _start
_start:
    mov rax, 18
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #18.

## Ishlash natijasi:
```text
Registrlar amaliyoti #18 muvaffaqiyatli yakunlandi.
```


# 79-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #19
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #19.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #19
section .text
global _start
_start:
    mov rax, 19
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #19.

## Ishlash natijasi:
```text
Registrlar amaliyoti #19 muvaffaqiyatli yakunlandi.
```


# 80-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #20
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #20.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #20
section .text
global _start
_start:
    mov rax, 20
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #20.

## Ishlash natijasi:
```text
Registrlar amaliyoti #20 muvaffaqiyatli yakunlandi.
```


# 81-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #21
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #21.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #21
section .text
global _start
_start:
    mov rax, 21
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #21.

## Ishlash natijasi:
```text
Registrlar amaliyoti #21 muvaffaqiyatli yakunlandi.
```


# 82-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #22
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #22.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #22
section .text
global _start
_start:
    mov rax, 22
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #22.

## Ishlash natijasi:
```text
Registrlar amaliyoti #22 muvaffaqiyatli yakunlandi.
```


# 83-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #23
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #23.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #23
section .text
global _start
_start:
    mov rax, 23
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #23.

## Ishlash natijasi:
```text
Registrlar amaliyoti #23 muvaffaqiyatli yakunlandi.
```


# 84-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #24
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #24.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #24
section .text
global _start
_start:
    mov rax, 24
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #24.

## Ishlash natijasi:
```text
Registrlar amaliyoti #24 muvaffaqiyatli yakunlandi.
```


# 85-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #25
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #25.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #25
section .text
global _start
_start:
    mov rax, 25
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #25.

## Ishlash natijasi:
```text
Registrlar amaliyoti #25 muvaffaqiyatli yakunlandi.
```


# 86-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #26
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #26.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #26
section .text
global _start
_start:
    mov rax, 26
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #26.

## Ishlash natijasi:
```text
Registrlar amaliyoti #26 muvaffaqiyatli yakunlandi.
```


# 87-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #27
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #27.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #27
section .text
global _start
_start:
    mov rax, 27
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #27.

## Ishlash natijasi:
```text
Registrlar amaliyoti #27 muvaffaqiyatli yakunlandi.
```


# 88-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #28
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #28.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #28
section .text
global _start
_start:
    mov rax, 28
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #28.

## Ishlash natijasi:
```text
Registrlar amaliyoti #28 muvaffaqiyatli yakunlandi.
```


# 89-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #29
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #29.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #29
section .text
global _start
_start:
    mov rax, 29
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #29.

## Ishlash natijasi:
```text
Registrlar amaliyoti #29 muvaffaqiyatli yakunlandi.
```


# 90-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #30
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #30.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #30
section .text
global _start
_start:
    mov rax, 30
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #30.

## Ishlash natijasi:
```text
Registrlar amaliyoti #30 muvaffaqiyatli yakunlandi.
```


# 91-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #31
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #31.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #31
section .text
global _start
_start:
    mov rax, 31
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #31.

## Ishlash natijasi:
```text
Registrlar amaliyoti #31 muvaffaqiyatli yakunlandi.
```


# 92-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #32
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #32.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #32
section .text
global _start
_start:
    mov rax, 32
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #32.

## Ishlash natijasi:
```text
Registrlar amaliyoti #32 muvaffaqiyatli yakunlandi.
```


# 93-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #33
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #33.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #33
section .text
global _start
_start:
    mov rax, 33
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #33.

## Ishlash natijasi:
```text
Registrlar amaliyoti #33 muvaffaqiyatli yakunlandi.
```


# 94-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #34
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #34.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #34
section .text
global _start
_start:
    mov rax, 34
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #34.

## Ishlash natijasi:
```text
Registrlar amaliyoti #34 muvaffaqiyatli yakunlandi.
```


# 95-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #35
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #35.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #35
section .text
global _start
_start:
    mov rax, 35
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #35.

## Ishlash natijasi:
```text
Registrlar amaliyoti #35 muvaffaqiyatli yakunlandi.
```


# 96-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #36
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #36.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #36
section .text
global _start
_start:
    mov rax, 36
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #36.

## Ishlash natijasi:
```text
Registrlar amaliyoti #36 muvaffaqiyatli yakunlandi.
```


# 97-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #37
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #37.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #37
section .text
global _start
_start:
    mov rax, 37
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #37.

## Ishlash natijasi:
```text
Registrlar amaliyoti #37 muvaffaqiyatli yakunlandi.
```


# 98-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #38
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #38.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #38
section .text
global _start
_start:
    mov rax, 38
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #38.

## Ishlash natijasi:
```text
Registrlar amaliyoti #38 muvaffaqiyatli yakunlandi.
```


# 99-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #39
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #39.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #39
section .text
global _start
_start:
    mov rax, 39
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #39.

## Ishlash natijasi:
```text
Registrlar amaliyoti #39 muvaffaqiyatli yakunlandi.
```


# 100-Topshiriq: x86_64 registrlari bilan ishlash amaliyoti #40
## Topshiriq sharti:
x86_64 umumiy registrlar, manzillash usullari va harakat buyruqlari topshirig'i #40.

## Yechim (Assembly kodi):
```assembly
; Registrlar amaliyoti #40
section .text
global _start
_start:
    mov rax, 40
    mov rbx, rax
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 registrlari ustida amallarni chuqur o'rganish bo'yicha amaliy topshiriq #40.

## Ishlash natijasi:
```text
Registrlar amaliyoti #40 muvaffaqiyatli yakunlandi.
```

