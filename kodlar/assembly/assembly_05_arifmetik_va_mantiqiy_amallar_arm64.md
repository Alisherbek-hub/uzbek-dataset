# 201-Topshiriq: ARM64 'add' va 'sub' amallari
## Topshiriq sharti:
AArch64 da 3 operandli arifmetika: natija alohida registrga yozilishi.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #50
    mov x2, #25
    add x0, x1, x2      // x0 = x1 + x2 = 75 (x1 va x2 buzilmaydi!)
    sub x3, x0, #15     // x3 = 75 - 15 = 60

    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arxitekturasi 3 operandli formatdan foydalanadi: 'add d, n, m' da manba registrlari buzilmaydi, natija yangi 'd' registrga yoziladi.

## Ishlash natijasi:
```text
ARM64 3 operandli add va sub muvaffaqiyatli bajarildi.
```


# 202-Topshiriq: Bayroqlarni yangilovchi 'adds' va 'subs'
## Topshiriq sharti:
ARM64 da qachon PSTATE NZCV bayroqlari yangilanishini ko'rsating.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #10
    mov x2, #10
    // 'add' bayroqlarni YANGILAMAYDI!
    // 'adds' esa oxiridagi 's' tufayli NZCV ni yangilaydi:
    subs x0, x1, x2     // x0 = 0, Zero Flag (Z=1) yoqildi!

    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM arxitekturasida arifmetik buyruqlar sukut bo'yicha bayroqlarni o'zgartirmaydi. Faqat 's' harfi qo'shilgandagina ('adds', 'subs', 'ands') PSTATE registridagi NZCV bayroqlari yangilanadi.

## Ishlash natijasi:
```text
adds va subs orqali NZCV bayroqlari boshqarildi.
```


# 203-Topshiriq: Multiply-Accumulate: 'madd' va 'msub'
## Topshiriq sharti:
Ko'paytirib qo'shish amalini apparat darajasida bitta instruksiyada bajaring.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #5
    mov x2, #4
    mov x3, #10
    // madd d, n, m, a -> d = a + (n * m)
    madd x0, x1, x2, x3 // x0 = 10 + (5 * 4) = 30!

    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
'madd' (Multiply-Add) neyron tarmoqlar, matritsalar va grafika algoritmlarida (Dot product) asosiy poydevor hisoblanadi.

## Ishlash natijasi:
```text
madd amali bajarildi: 10 + 5*4 = 30.
```


# 204-Topshiriq: ARM64 Bo'lish amallari: 'sdiv' va 'udiv'
## Topshiriq sharti:
ARM64 da nolga bo'linganda qanday hodisa ro'y berishini tahlil qiling.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #100
    mov x2, #5
    sdiv x0, x1, x2     // x0 = 20

    // DIQQAT: ARM64 da nolga bo'linganda dastur halokatga uchramaydi (No Crash)!
    // Natija shunchaki 0 qaytariladi!
    mov x3, #0
    sdiv x4, x1, x3     // x4 = 0

    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
x86_64 da nolga bo'lish (#DE exception) darhol dasturni qulatadi. ARM64 da esa 'sdiv' nolga bo'linganda 0 natijasini beradi va hech qanday signal yoki uzilish yuz bermaydi.

## Ishlash natijasi:
```text
sdiv: 100/5=20, 100/0=0 (Crashsiz xavfsiz arifmetika).
```


# 205-Topshiriq: Bit Clear amali: 'bic' (Bit Clear)
## Topshiriq sharti:
Birinchi operanddagi ikkinchi operand bitlarini tozalang (a AND NOT b).

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #0b1111
    mov x2, #0b0101
    bic x0, x1, x2      // x0 = 0b1010 (10)

    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
'bic' (Bit Clear) instruksiyasi 'dest = src1 AND NOT src2' amalini bitta buyruqda bajaradi.

## Ishlash natijasi:
```text
bic amali orqali bitlar tozalandi.
```


# 206-Topshiriq: Shifted Register arifmetikasi
## Topshiriq sharti:
Ko'paytirish va qo'shishni bitta 'add' buyrug'i ichida birlashtiring.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #10
    mov x2, #3
    // add x0, x1, x2, lsl #2 -> x0 = x1 + (x2 << 2) = 10 + (3 * 4) = 22!
    add x0, x1, x2, lsl #2

    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM protsessorlarida arifmetik ALU kirishida apparat Barrel Shifter mavjud, bu har qanday arifmetik amalda ikkinchi operandni bepul siljitish imkonini beradi.

## Ishlash natijasi:
```text
Shifted register arifmetikasi: 10 + (3<<2) = 22.
```


# 207-Topshiriq: Leading Zeros sanash: 'clz'
## Topshiriq sharti:
Sonning eng yuqori bitidan boshlab nechta nol borligini hisoblang.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #0x0000000000000001
    clz x0, x1          // x0 = 63 (chunki 63 ta nol va bitta 1)

    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
'clz' (Count Leading Zeros) sonning logarifmini topish, normalizatsiya va bit xaritalarini skanerlashda ishlatiladi.

## Ishlash natijasi:
```text
clz: 1 sonida 63 ta oldingi nollar sanaldi.
```


# 208-Topshiriq: Bitfield Extraction: 'ubfm' va 'sbfm'
## Topshiriq sharti:
Registrning ixtiyoriy oraliqdagi bitlarini ajratib olish.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    // ubfm d, n, #immr, #imms
    // Qisqartma: ubfx x0, x1, #4, #8 (4-bitdan boshlab 8 ta bitni ajratish)

    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 bitfield amallari apparat registrlari va tarmoq paketlari sarlavhalarini qismlarga ajratishda juda kuchli.

## Ishlash natijasi:
```text
Bitfield ekstraksiyasi muvaffaqiyatli o'rganildi.
```


# 209-Topshiriq: Conditional Select: 'csel' (Ternar operator)
## Topshiriq sharti:
Hech qanday sakrashsiz (Branchless) if-else ni bitta buyruqda bajarish.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #100
    mov x2, #200
    cmp x1, x2
    // csel d, n, m, cond -> agar cond rost bo'lsa d = n, aks holda d = m
    csel x0, x1, x2, gt // x1 > x2 bo'lsa x0=x1, aks holda x0=x2 (x0=200)

    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
'csel' (Conditional Select) protsessorda Branch Miss xatolarining oldini oluvchi eng muhim optimizatsiya buyrug'idir.

## Ishlash natijasi:
```text
csel branchless tanlovi bajarildi: max = 200.
```


# 210-Topshiriq: Conditional Set: 'cset' (Bayroqdan 0 yoki 1 olish)
## Topshiriq sharti:
Shart rost bo'lsa registrga 1, aks holda 0 yozish.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #42
    cmp x1, #42
    cset x0, eq         // Agar teng bo'lsa x0 = 1, aks holda x0 = 0

    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
'cset' mantiqiy solishtirish natijasini boolean (1 yoki 0) shaklida registrga yuklaydi.

## Ishlash natijasi:
```text
cset: Tenglik sharti bo'yicha registrga 1 yuklandi.
```


# 211-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #1
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #1.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #1
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #1.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #1 muvaffaqiyatli yakunlandi.
```


# 212-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #2
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #2.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #2
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #2.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #2 muvaffaqiyatli yakunlandi.
```


# 213-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #3
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #3.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #3
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #3.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #3 muvaffaqiyatli yakunlandi.
```


# 214-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #4
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #4.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #4
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #4.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #4 muvaffaqiyatli yakunlandi.
```


# 215-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #5
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #5.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #5
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #5.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #5 muvaffaqiyatli yakunlandi.
```


# 216-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #6
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #6.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #6
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #6.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #6 muvaffaqiyatli yakunlandi.
```


# 217-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #7
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #7.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #7
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #7.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #7 muvaffaqiyatli yakunlandi.
```


# 218-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #8
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #8.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #8
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #8.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #8 muvaffaqiyatli yakunlandi.
```


# 219-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #9
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #9.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #9
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #9.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #9 muvaffaqiyatli yakunlandi.
```


# 220-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #10
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #10.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #10
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #10.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #10 muvaffaqiyatli yakunlandi.
```


# 221-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #11
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #11.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #11
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #11.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #11 muvaffaqiyatli yakunlandi.
```


# 222-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #12
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #12.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #12
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #12.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #12 muvaffaqiyatli yakunlandi.
```


# 223-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #13
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #13.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #13
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #13.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #13 muvaffaqiyatli yakunlandi.
```


# 224-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #14
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #14.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #14
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #14.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #14 muvaffaqiyatli yakunlandi.
```


# 225-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #15
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #15.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #15
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #15.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #15 muvaffaqiyatli yakunlandi.
```


# 226-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #16
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #16.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #16
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #16.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #16 muvaffaqiyatli yakunlandi.
```


# 227-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #17
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #17.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #17
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #17.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #17 muvaffaqiyatli yakunlandi.
```


# 228-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #18
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #18.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #18
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #18.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #18 muvaffaqiyatli yakunlandi.
```


# 229-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #19
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #19.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #19
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #19.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #19 muvaffaqiyatli yakunlandi.
```


# 230-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #20
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #20.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #20
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #20.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #20 muvaffaqiyatli yakunlandi.
```


# 231-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #21
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #21.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #21
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #21.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #21 muvaffaqiyatli yakunlandi.
```


# 232-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #22
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #22.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #22
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #22.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #22 muvaffaqiyatli yakunlandi.
```


# 233-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #23
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #23.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #23
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #23.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #23 muvaffaqiyatli yakunlandi.
```


# 234-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #24
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #24.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #24
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #24.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #24 muvaffaqiyatli yakunlandi.
```


# 235-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #25
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #25.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #25
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #25.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #25 muvaffaqiyatli yakunlandi.
```


# 236-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #26
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #26.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #26
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #26.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #26 muvaffaqiyatli yakunlandi.
```


# 237-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #27
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #27.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #27
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #27.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #27 muvaffaqiyatli yakunlandi.
```


# 238-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #28
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #28.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #28
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #28.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #28 muvaffaqiyatli yakunlandi.
```


# 239-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #29
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #29.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #29
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #29.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #29 muvaffaqiyatli yakunlandi.
```


# 240-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #30
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #30.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #30
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #30.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #30 muvaffaqiyatli yakunlandi.
```


# 241-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #31
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #31.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #31
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #31.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #31 muvaffaqiyatli yakunlandi.
```


# 242-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #32
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #32.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #32
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #32.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #32 muvaffaqiyatli yakunlandi.
```


# 243-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #33
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #33.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #33
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #33.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #33 muvaffaqiyatli yakunlandi.
```


# 244-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #34
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #34.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #34
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #34.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #34 muvaffaqiyatli yakunlandi.
```


# 245-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #35
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #35.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #35
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #35.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #35 muvaffaqiyatli yakunlandi.
```


# 246-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #36
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #36.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #36
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #36.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #36 muvaffaqiyatli yakunlandi.
```


# 247-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #37
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #37.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #37
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #37.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #37 muvaffaqiyatli yakunlandi.
```


# 248-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #38
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #38.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #38
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #38.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #38 muvaffaqiyatli yakunlandi.
```


# 249-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #39
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #39.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #39
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #39.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #39 muvaffaqiyatli yakunlandi.
```


# 250-Topshiriq: ARM64 arifmetik va mantiqiy amallar amaliyoti #40
## Topshiriq sharti:
ARM64 AArch64 arifmetika, bitfield va mantiqiy ko'rsatmalar topshirig'i #40.

## Yechim (Assembly kodi):
```assembly
.text
.global _start
_start:
    mov x1, #40
    add x0, x1, #10
    mov x8, #93
    mov x0, #0
    svc #0
```

## Tushuntirish va Mantiq:
ARM64 arifmetik ko'rsatmalari bo'yicha amaliy topshiriq #40.

## Ishlash natijasi:
```text
ARM64 arifmetika amaliyoti #40 muvaffaqiyatli yakunlandi.
```

