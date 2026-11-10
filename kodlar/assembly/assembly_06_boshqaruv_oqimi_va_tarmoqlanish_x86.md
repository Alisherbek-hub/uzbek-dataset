# 251-Topshiriq: x86_64 Shartsiz sakrash: 'jmp'
## Topshiriq sharti:
Dastur ijrosini ko'rsatilgan leybldan davom ettiring.

## Yechim (Assembly kodi):
```assembly
section .text
global _start
_start:
    jmp target_label
    mov rax, 999        ; Bu qator o'tkazib yuboriladi!

target_label:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
'jmp label' RIP (Instruction Pointer) registrini ko'rsatilgan manzilga o'zgartiradi.

## Ishlash natijasi:
```text
jmp orqali target_label ga muvaffaqiyatli sakraldi.
```


# 252-Topshiriq: Taqqoslash va tenglik sakrashi: 'cmp' va 'je/jne'
## Topshiriq sharti:
Sonlar tengligini tekshirib tarmoqlaning.

## Yechim (Assembly kodi):
```assembly
section .text
global _start
_start:
    mov rax, 50
    cmp rax, 50         ; rax - 50 hisoblanadi, ZF=1 bo'ladi
    je  equal_label     ; Agar teng bo'lsa sakrash

    mov rdi, 1
    jmp exit_prog

equal_label:
    mov rdi, 0          ; Teng bo'lgandagi yo'l

exit_prog:
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
'cmp a, b' amali 'sub a, b' kabi ishlaydi, lekin natijani saqlamaydi, faqat RFLAGS bayroqlarini yangilaydi. 'je' (Jump if Equal) ZF=1 bo'lganda sakraydi.

## Ishlash natijasi:
```text
cmp va je orqali tenglik sharti bajarildi.
```


# 253-Topshiriq: Ishorali taqqoslash: 'jg', 'jge', 'jl', 'jle'
## Topshiriq sharti:
Manfiy va musbat sonlarni to'g'ri solishtirish.

## Yechim (Assembly kodi):
```assembly
section .text
global _start
_start:
    mov rax, -5
    mov rbx, 10
    cmp rax, rbx
    jl  less_label      ; -5 < 10 rost, sakraydi!

    mov rdi, 1
    jmp end_lbl
less_label:
    mov rdi, 0
end_lbl:
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
Ishorali sonlar uchun 'jl' (SF != OF), 'jg' (ZF=0 va SF=OF) qo'llaniladi.

## Ishlash natijasi:
```text
Ishorali taqqoslash: -5 < 10 muvaffaqiyatli tekshirildi.
```


# 254-Topshiriq: Ishorasiz taqqoslash: 'ja', 'jae', 'jb', 'jbe'
## Topshiriq sharti:
Xotira manzillari va unsigned kattaliklarni solishtirish.

## Yechim (Assembly kodi):
```assembly
section .text
global _start
_start:
    mov rax, 0xFFFFFFFFFFFFFFFF ; Unsigned eng katta son
    mov rbx, 5
    cmp rax, rbx
    ja  above_lbl       ; rax > rbx (unsigned ma'noda), sakraydi!

    mov rdi, 1
    jmp end_lbl
above_lbl:
    mov rdi, 0
end_lbl:
    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
Ishorasiz sonlar uchun 'ja' (Above - CF=0 va ZF=0) va 'jb' (Below - CF=1) ishlatiladi.

## Ishlash natijasi:
```text
Ishorasiz taqqoslash: Above sharti tasdiqlandi.
```


# 255-Topshiriq: Sikl ko'rsatmasi: 'loop'
## Topshiriq sharti:
RCX hisoblagichi yordamida N marta aylanuvchi apparat sikli.

## Yechim (Assembly kodi):
```assembly
section .text
global _start
_start:
    mov rcx, 5          ; Sikl soni
    xor rax, rax        ; Yig'indi

loop_start:
    add rax, 10
    loop loop_start     ; RCX--, agar RCX != 0 bo'lsa loop_start ga sakraydi!

    ; rax = 50 bo'ldi!
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
'loop label' har bir qadamda RCX registrini 1 taga kamaytiradi va agar u nol bo'lmasa ko'rsatilgan manzilga sakraydi.

## Ishlash natijasi:
```text
loop orqali 5 marta 10 qo'shildi: natija 50.
```


# 256-Topshiriq: Shartli ko'chirish: 'cmovcc' (Branchless Programming)
## Topshiriq sharti:
Tarmoqlanmasdan maksimum qiymatni tanlang.

## Yechim (Assembly kodi):
```assembly
section .text
global _start
_start:
    mov rax, 150
    mov rbx, 200
    cmp rax, rbx
    cmovl rax, rbx      ; Agar rax < rbx bo'lsa, rax = rbx (sakrash yo'q!)

    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
'cmovcc' (Conditional Move) protsessor quvurini (pipeline) buzmasdan, branch miss hodisalarisiz if-else ni bitta siklda bajaradi.

## Ishlash natijasi:
```text
cmovl orqali ikkala sonning kattasi (200) tanlandi.
```


# 257-Topshiriq: Shartli bayt o'rnatish: 'setcc' (Boolean natija)
## Topshiriq sharti:
Solishtirish natijasini registrga 1 yoki 0 qilib yozing.

## Yechim (Assembly kodi):
```assembly
section .text
global _start
_start:
    mov rax, 10
    cmp rax, 10
    sete al             ; AL = 1 (chunki teng!)
    movzx rdi, al

    mov rax, 60
    syscall
```

## Tushuntirish va Mantiq:
'setcc' berilgan shart rost bo'lsa ko'rsatilgan 8-bitli registrga 1, aks holda 0 yozadi.

## Ishlash natijasi:
```text
sete orqali tenglik natijasi AL registriga 1 bo'lib yozildi.
```


# 258-Topshiriq: While sikli modeli x86_64 da
## Topshiriq sharti:
Klassik 'while (i < 10)' siklini Assembly da quring.

## Yechim (Assembly kodi):
```assembly
section .text
global _start
_start:
    xor rcx, rcx        ; i = 0
while_start:
    cmp rcx, 5
    jge while_end       ; i >= 5 bo'lsa chiqish
    inc rcx
    jmp while_start
while_end:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
While sikli boshida shart tekshiriladi va agar shart bajarilmasa sikldan tashqariga sakraladi.

## Ishlash natijasi:
```text
While sikli 5 marta aylandi.
```


# 259-Topshiriq: Do-While sikli modeli x86_64 da
## Topshiriq sharti:
Sikl oxirida shart tekshiriluvchi tezkor model.

## Yechim (Assembly kodi):
```assembly
section .text
global _start
_start:
    xor rcx, rcx
do_while_loop:
    inc rcx
    cmp rcx, 5
    jl do_while_loop    ; Bitta sakrash bilan tezkor sikl!

    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
Do-while sikllari odatda bitta sakrashga ega bo'lgani uchun protsessor keshida tezroq ishlaydi.

## Ishlash natijasi:
```text
Do-While sikli muvaffaqiyatli bajarildi.
```


# 260-Topshiriq: Branch Prediction (Tarmoqlanish bashorati) va uning ahamiyati
## Topshiriq sharti:
Protsessor qanday qilib sakrashlarni oldindan taxmin qilishi.

## Yechim (Assembly kodi):
```assembly
section .text
global _start
_start:
    ; Protsessor Branch Target Buffer (BTB) orqali sikllarning orqaga sakrashini
    ; deyarli 100% holatda to'g'ri bashorat qiladi (Taken prediction).
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
Branch Prediction noto'g'ri taxmin qilsa (Branch Misprediction), protsessor butun konveyerni tozalashga majbur bo'ladi, bu esa 15-20 sikl yo'qotilishiga olib keladi.

## Ishlash natijasi:
```text
Branch Prediction mexanizmi tahlil qilindi.
```


# 261-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #1
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #1.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #1
section .text
global _start
_start:
    mov rcx, 1
    cmp rcx, 0
    jne lbl_1
    nop
lbl_1:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #1.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #1 muvaffaqiyatli yakunlandi.
```


# 262-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #2
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #2.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #2
section .text
global _start
_start:
    mov rcx, 2
    cmp rcx, 0
    jne lbl_2
    nop
lbl_2:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #2.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #2 muvaffaqiyatli yakunlandi.
```


# 263-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #3
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #3.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #3
section .text
global _start
_start:
    mov rcx, 3
    cmp rcx, 0
    jne lbl_3
    nop
lbl_3:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #3.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #3 muvaffaqiyatli yakunlandi.
```


# 264-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #4
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #4.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #4
section .text
global _start
_start:
    mov rcx, 4
    cmp rcx, 0
    jne lbl_4
    nop
lbl_4:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #4.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #4 muvaffaqiyatli yakunlandi.
```


# 265-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #5
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #5.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #5
section .text
global _start
_start:
    mov rcx, 5
    cmp rcx, 0
    jne lbl_5
    nop
lbl_5:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #5.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #5 muvaffaqiyatli yakunlandi.
```


# 266-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #6
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #6.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #6
section .text
global _start
_start:
    mov rcx, 6
    cmp rcx, 0
    jne lbl_6
    nop
lbl_6:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #6.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #6 muvaffaqiyatli yakunlandi.
```


# 267-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #7
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #7.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #7
section .text
global _start
_start:
    mov rcx, 7
    cmp rcx, 0
    jne lbl_7
    nop
lbl_7:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #7.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #7 muvaffaqiyatli yakunlandi.
```


# 268-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #8
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #8.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #8
section .text
global _start
_start:
    mov rcx, 8
    cmp rcx, 0
    jne lbl_8
    nop
lbl_8:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #8.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #8 muvaffaqiyatli yakunlandi.
```


# 269-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #9
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #9.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #9
section .text
global _start
_start:
    mov rcx, 9
    cmp rcx, 0
    jne lbl_9
    nop
lbl_9:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #9.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #9 muvaffaqiyatli yakunlandi.
```


# 270-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #10
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #10.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #10
section .text
global _start
_start:
    mov rcx, 10
    cmp rcx, 0
    jne lbl_10
    nop
lbl_10:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #10.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #10 muvaffaqiyatli yakunlandi.
```


# 271-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #11
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #11.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #11
section .text
global _start
_start:
    mov rcx, 11
    cmp rcx, 0
    jne lbl_11
    nop
lbl_11:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #11.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #11 muvaffaqiyatli yakunlandi.
```


# 272-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #12
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #12.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #12
section .text
global _start
_start:
    mov rcx, 12
    cmp rcx, 0
    jne lbl_12
    nop
lbl_12:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #12.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #12 muvaffaqiyatli yakunlandi.
```


# 273-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #13
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #13.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #13
section .text
global _start
_start:
    mov rcx, 13
    cmp rcx, 0
    jne lbl_13
    nop
lbl_13:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #13.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #13 muvaffaqiyatli yakunlandi.
```


# 274-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #14
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #14.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #14
section .text
global _start
_start:
    mov rcx, 14
    cmp rcx, 0
    jne lbl_14
    nop
lbl_14:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #14.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #14 muvaffaqiyatli yakunlandi.
```


# 275-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #15
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #15.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #15
section .text
global _start
_start:
    mov rcx, 15
    cmp rcx, 0
    jne lbl_15
    nop
lbl_15:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #15.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #15 muvaffaqiyatli yakunlandi.
```


# 276-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #16
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #16.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #16
section .text
global _start
_start:
    mov rcx, 16
    cmp rcx, 0
    jne lbl_16
    nop
lbl_16:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #16.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #16 muvaffaqiyatli yakunlandi.
```


# 277-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #17
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #17.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #17
section .text
global _start
_start:
    mov rcx, 17
    cmp rcx, 0
    jne lbl_17
    nop
lbl_17:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #17.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #17 muvaffaqiyatli yakunlandi.
```


# 278-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #18
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #18.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #18
section .text
global _start
_start:
    mov rcx, 18
    cmp rcx, 0
    jne lbl_18
    nop
lbl_18:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #18.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #18 muvaffaqiyatli yakunlandi.
```


# 279-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #19
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #19.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #19
section .text
global _start
_start:
    mov rcx, 19
    cmp rcx, 0
    jne lbl_19
    nop
lbl_19:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #19.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #19 muvaffaqiyatli yakunlandi.
```


# 280-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #20
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #20.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #20
section .text
global _start
_start:
    mov rcx, 20
    cmp rcx, 0
    jne lbl_20
    nop
lbl_20:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #20.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #20 muvaffaqiyatli yakunlandi.
```


# 281-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #21
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #21.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #21
section .text
global _start
_start:
    mov rcx, 21
    cmp rcx, 0
    jne lbl_21
    nop
lbl_21:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #21.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #21 muvaffaqiyatli yakunlandi.
```


# 282-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #22
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #22.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #22
section .text
global _start
_start:
    mov rcx, 22
    cmp rcx, 0
    jne lbl_22
    nop
lbl_22:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #22.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #22 muvaffaqiyatli yakunlandi.
```


# 283-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #23
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #23.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #23
section .text
global _start
_start:
    mov rcx, 23
    cmp rcx, 0
    jne lbl_23
    nop
lbl_23:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #23.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #23 muvaffaqiyatli yakunlandi.
```


# 284-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #24
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #24.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #24
section .text
global _start
_start:
    mov rcx, 24
    cmp rcx, 0
    jne lbl_24
    nop
lbl_24:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #24.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #24 muvaffaqiyatli yakunlandi.
```


# 285-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #25
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #25.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #25
section .text
global _start
_start:
    mov rcx, 25
    cmp rcx, 0
    jne lbl_25
    nop
lbl_25:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #25.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #25 muvaffaqiyatli yakunlandi.
```


# 286-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #26
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #26.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #26
section .text
global _start
_start:
    mov rcx, 26
    cmp rcx, 0
    jne lbl_26
    nop
lbl_26:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #26.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #26 muvaffaqiyatli yakunlandi.
```


# 287-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #27
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #27.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #27
section .text
global _start
_start:
    mov rcx, 27
    cmp rcx, 0
    jne lbl_27
    nop
lbl_27:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #27.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #27 muvaffaqiyatli yakunlandi.
```


# 288-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #28
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #28.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #28
section .text
global _start
_start:
    mov rcx, 28
    cmp rcx, 0
    jne lbl_28
    nop
lbl_28:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #28.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #28 muvaffaqiyatli yakunlandi.
```


# 289-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #29
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #29.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #29
section .text
global _start
_start:
    mov rcx, 29
    cmp rcx, 0
    jne lbl_29
    nop
lbl_29:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #29.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #29 muvaffaqiyatli yakunlandi.
```


# 290-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #30
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #30.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #30
section .text
global _start
_start:
    mov rcx, 30
    cmp rcx, 0
    jne lbl_30
    nop
lbl_30:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #30.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #30 muvaffaqiyatli yakunlandi.
```


# 291-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #31
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #31.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #31
section .text
global _start
_start:
    mov rcx, 31
    cmp rcx, 0
    jne lbl_31
    nop
lbl_31:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #31.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #31 muvaffaqiyatli yakunlandi.
```


# 292-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #32
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #32.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #32
section .text
global _start
_start:
    mov rcx, 32
    cmp rcx, 0
    jne lbl_32
    nop
lbl_32:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #32.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #32 muvaffaqiyatli yakunlandi.
```


# 293-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #33
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #33.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #33
section .text
global _start
_start:
    mov rcx, 33
    cmp rcx, 0
    jne lbl_33
    nop
lbl_33:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #33.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #33 muvaffaqiyatli yakunlandi.
```


# 294-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #34
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #34.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #34
section .text
global _start
_start:
    mov rcx, 34
    cmp rcx, 0
    jne lbl_34
    nop
lbl_34:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #34.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #34 muvaffaqiyatli yakunlandi.
```


# 295-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #35
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #35.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #35
section .text
global _start
_start:
    mov rcx, 35
    cmp rcx, 0
    jne lbl_35
    nop
lbl_35:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #35.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #35 muvaffaqiyatli yakunlandi.
```


# 296-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #36
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #36.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #36
section .text
global _start
_start:
    mov rcx, 36
    cmp rcx, 0
    jne lbl_36
    nop
lbl_36:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #36.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #36 muvaffaqiyatli yakunlandi.
```


# 297-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #37
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #37.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #37
section .text
global _start
_start:
    mov rcx, 37
    cmp rcx, 0
    jne lbl_37
    nop
lbl_37:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #37.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #37 muvaffaqiyatli yakunlandi.
```


# 298-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #38
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #38.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #38
section .text
global _start
_start:
    mov rcx, 38
    cmp rcx, 0
    jne lbl_38
    nop
lbl_38:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #38.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #38 muvaffaqiyatli yakunlandi.
```


# 299-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #39
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #39.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #39
section .text
global _start
_start:
    mov rcx, 39
    cmp rcx, 0
    jne lbl_39
    nop
lbl_39:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #39.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #39 muvaffaqiyatli yakunlandi.
```


# 300-Topshiriq: x86_64 boshqaruv oqimi amaliyoti #40
## Topshiriq sharti:
x86_64 shartli sakrashlar, sikllar va tarmoqlanish topshirig'i #40.

## Yechim (Assembly kodi):
```assembly
; Boshqaruv oqimi amaliyoti #40
section .text
global _start
_start:
    mov rcx, 40
    cmp rcx, 0
    jne lbl_40
    nop
lbl_40:
    mov rax, 60
    xor rdi, rdi
    syscall
```

## Tushuntirish va Mantiq:
x86_64 boshqaruv oqimi bo'yicha amaliy topshiriq #40.

## Ishlash natijasi:
```text
Boshqaruv oqimi amaliyoti #40 muvaffaqiyatli yakunlandi.
```

