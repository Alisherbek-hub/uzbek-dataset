# 1-Qism: Rust Asoslari, Tiplar va O'zgaruvchilar (1-50)

Ushbu qismda Rust dasturlash tilining poydevor tushunchalari: o'zgaruvchilar e'lon qilish (`let`, `let mut`, `const`), shadowing mexanizmi, skalar turlar (butun va suzuvchi nuqtali sonlar, bool, char), birikmali turlar (tuple, massiv), xavfsiz tur konvertatsiyasi va arifmetik amallar o'rganiladi.

---

# 1-Topshiriq: Rust dasturining kirish nuqtasi va println! makrosi
## Topshiriq sharti:
Rust dasturining asosiy kirish funksiyasi bo'lgan `main` funksiyasini yozing va konsolga 'Assalomu alaykum, Rust dasturchisi!' jumlasini chiqaring.

## Yechim (Rust kodi):
```rust
fn main() {
    // println! bu oddiy funksiya emas, balki makro hisoblanadi (buni ! belgisidan bilish mumkin)
    println!("Assalomu alaykum, Rust dasturchisi!");
}
```

## Tushuntirish va Mantiq:
Rust dasturlari `fn main()` funksiyasidan ishga tushadi. `println!` makrosi matnni standart terminalga chiqarib, avtomatik yangi qatorga o'tadi.

## Ishlash natijasi:
```text
Assalomu alaykum, Rust dasturchisi!
```

---

# 2-Topshiriq: let kalit so'zi va o'zgarmaslik (Immutability) tamoyili
## Topshiriq sharti:
Rust da o'zgaruvchi e'lon qiling va uning qiymatini ekranga chiqaring. Rust da standart holatda barcha o'zgaruvchilar o'zgarmas ekanligini namoyish eting.

## Yechim (Rust kodi):
```rust
fn main() {
    let shahar = "Toshkent";
    println!("Tanlangan shahar: {}", shahar);
    // shahar = "Samarqand"; // Ushbu qatordagi izoh olib tashlansa, kompilyator xatolik beradi
}
```

## Tushuntirish va Mantiq:
Rust xavfsizlikka yo'naltirilgan til bo'lib, `let` bilan e'lon qilingan o'zgaruvchilar standart bo'yicha o'zgarmas (immutable) bo'ladi. Bu dastur xotirasini kutilmagan o'zgarishlardan himoya qiladi.

## Ishlash natijasi:
```text
Tanlangan shahar: Toshkent
```

---

# 3-Topshiriq: let mut orqali o'zgaruvchan qiymatlar yaratish
## Topshiriq sharti:
`mut` kalit so'zidan foydalanib o'zgaruvchan o'zgaruvchi yarating, uning dastlabki qiymatini o'zgartiring va ikkala holatni chop eting.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut hisoblagich = 10;
    println!("Dastlabki hisoblagich: {}", hisoblagich);

    hisoblagich = 25;
    println!("O'zgartirilgan hisoblagich: {}", hisoblagich);
}
```

## Tushuntirish va Mantiq:
O'zgaruvchi qiymatini o'zgartirish talab etilsa, `let mut` sintaksisi ishlatiladi. `mut` Rust kompilyatoriga ushbu xotira katakchasiga yangi qiymat yozishga ruxsat beradi.

## Ishlash natijasi:
```text
Dastlabki hisoblagich: 10
O'zgartirilgan hisoblagich: 25
```

---

# 4-Topshiriq: const kalit so'zi va global konstantalar
## Topshiriq sharti:
Kompilyatsiya vaqtida hisoblanadigan global `const` o'zgaruvchi e'lon qiling. Tip annotatsiyasi majburiy ekanligini ko'rsating.

## Yechim (Rust kodi):
```rust
const MAKSIMAL_BALL: u32 = 100;
const PI_TAQRIBIY: f64 = 3.14159;

fn main() {
    println!("Maksimal ball: {}", MAKSIMAL_BALL);
    println!("Pi soni: {}", PI_TAQRIBIY);
}
```

## Tushuntirish va Mantiq:
`const` qiymatlar dastur davomida umuman o'zgarmaydi va kompilyatsiya vaqtida hisoblanadi. Ularning turi (`u32`, `f64`) har doim aniq ko'rsatilishi shart.

## Ishlash natijasi:
```text
Maksimal ball: 100
Pi soni: 3.14159
```

---

# 5-Topshiriq: Shadowing (O'zgaruvchini qayta e'lon qilish) mexanizmi
## Topshiriq sharti:
Bitta o'zgaruvchi nomini `let` orqali bir necha marta qayta e'lon qilib (shadowing), uning qiymatini yangilang.

## Yechim (Rust kodi):
```rust
fn main() {
    let x = 5;
    let x = x + 1; // 6
    {
        let x = x * 2; // 12 (ichki doirada)
        println!("Ichki blokdagi x: {}", x);
    }
    println!("Tashqi blokdagi x: {}", x);
}
```

## Tushuntirish va Mantiq:
Shadowing `mut` dan farq qiladi: bu yerda yangi o'zgaruvchi xuddi shu nom bilan qayta yaratiladi. Ichki blok tugagach, tashqi blokdagi qiymat o'z kuchida qoladi.

## Ishlash natijasi:
```text
Ichki blokdagi x: 12
Tashqi blokdagi x: 6
```

---

# 6-Topshiriq: Shadowing orqali ma'lumot turini o'zgartirish
## Topshiriq sharti:
Shadowing yordamida o'zgaruvchi nomini saqlagan holda uning turini satrdan (`&str`) songa (`usize`) o'zgartiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let probellar = "   "; // &str turi
    let probellar = probellar.len(); // usize turi (uzunligi)

    println!("Bo'sh joylar soni: {}", probellar);
}
```

## Tushuntirish va Mantiq:
Shadowing o'zgaruvchi nomini saqlab, yangi turdagi qiymat tayinlash imkonini beradi. `mut` bilan esa turni o'zgartirib bo'lmaydi.

## Ishlash natijasi:
```text
Bo'sh joylar soni: 3
```

---

# 7-Topshiriq: Ishtirokli butun sonlar (Signed Integers: i8, i16, i32, i64, i128)
## Topshiriq sharti:
Har xil o'lchamdagi ishorali butun sonlarni e'lon qiling va ularning manfiy hamda musbat qiymatlarini ko'rsating.

## Yechim (Rust kodi):
```rust
fn main() {
    let a: i8 = -120;
    let b: i16 = -30000;
    let c: i32 = 1_000_000;
    let d: i64 = -9_000_000_000_000;
    let e: i128 = 170_141_183_460_469_231_731_687_303_715_884_105_727;

    println!("i8: {}, i16: {}, i32: {}, i64: {}, i128: {}", a, b, c, d, e);
}
```

## Tushuntirish va Mantiq:
Ishtirokli butun sonlar `i` harfi bilan boshlanadi va manfiy hamda musbat qiymatlarni ifodalaydi. Katta sonlarni o'qish qulay bo'lishi uchun pastki chiziq `_` ishlatiladi.

## Ishlash natijasi:
```text
i8: -120, i16: -30000, i32: 1000000, i64: -9000000000000, i128: 170141183460469231731687303715884105727
```

---

# 8-Topshiriq: Ishorasiz butun sonlar (Unsigned Integers: u8, u16, u32, u64, u128)
## Topshiriq sharti:
Faqat musbat qiymat qabul qiluvchi ishorasiz turlarni e'lon qiling va ularning xususiyatini ko'rsating.

## Yechim (Rust kodi):
```rust
fn main() {
    let yosh: u8 = 25;
    let port: u16 = 8080;
    let aholi: u32 = 36_000_000;
    let masofa: u64 = 150_000_000_000;

    println!("Yosh: {}, Port: {}, Aholi: {}, Masofa: {}", yosh, port, aholi, masofa);
}
```

## Tushuntirish va Mantiq:
Ishorasiz sonlar `u` bilan belgilanadi va 0 dan boshlanadi. Ular manfiy son qabul qilmaydi, shuning hisobiga musbat diapazoni ikki barobar kengroq bo'ladi.

## Ishlash natijasi:
```text
Yosh: 25, Port: 8080, Aholi: 36000000, Masofa: 150000000000
```

---

# 9-Topshiriq: Arxitekturaga bog'liq turlar: isize va usize
## Topshiriq sharti:
`usize` turidan massiv elementlarini indekslash va xotira manzillari hisob-kitoblarida foydalaning.

## Yechim (Rust kodi):
```rust
fn main() {
    let mevalar = ["Olma", "Anor", "Uzum"];
    let indeks: usize = 1;

    println!("Indeks {}: {}", indeks, mevalar[indeks]);
    println!("Arxitektura ko'rsatkichi bayti: {} bayt", std::mem::size_of::<usize>());
}
```

## Tushuntirish va Mantiq:
`usize` va `isize` turlari dastur ishlayotgan kompyuter arxitekturasiga (32-bit yoki 64-bit) moslashadi. Rust da massivlarni indekslash faqat `usize` orqali ruxsat etiladi.

## Ishlash natijasi:
```text
Indeks 1: Anor
Arxitektura ko'rsatkichi bayti: 8 bayt
```

---

# 10-Topshiriq: Turli sanoq tizimlaridagi butun son literallari
## Topshiriq sharti:
O'nlik, o'n oltilik, sakkizlik, ikkilik va bayt literallarini e'lon qilib, ularni o'nlik tizimda chop eting.

## Yechim (Rust kodi):
```rust
fn main() {
    let onlik = 98_222;
    let on_oltilik = 0xff; // 255
    let sakkizlik = 0o77; // 63
    let ikkilik = 0b1111_0000; // 240
    let bayt_belgi: u8 = b'A'; // 65 (ASCII)

    println!("O'nlik: {}", onlik);
    println!("O'n oltilik (0xff): {}", on_oltilik);
    println!("Sakkizlik (0o77): {}", sakkizlik);
    println!("Ikkilik (0b1111_0000): {}", ikkilik);
    println!("Bayt literal (b'A'): {}", bayt_belgi);
}
```

## Tushuntirish va Mantiq:
Rust dasturchiga qulaylik yaratish uchun `0x` (hex), `0o` (octal), `0b` (binary) va `b'A'` (byte) prefikslarini qo'llab-quvvatlaydi.

## Ishlash natijasi:
```text
O'nlik: 98222
O'n oltilik (0xff): 255
Sakkizlik (0o77): 63
Ikkilik (0b1111_0000): 240
Bayt literal (b'A'): 65
```

---

# 11-Topshiriq: Son turlarining chegaraviy MIN va MAX konstantalari
## Topshiriq sharti:
`i32` va `u8` turlarining qabul qilishi mumkin bo'lgan eng kichik va eng katta qiymatlarini chop eting.

## Yechim (Rust kodi):
```rust
fn main() {
    println!("i8 MIN: {}, MAX: {}", i8::MIN, i8::MAX);
    println!("u8 MIN: {}, MAX: {}", u8::MIN, u8::MAX);
    println!("i32 MIN: {}, MAX: {}", i32::MIN, i32::MAX);
    println!("u32 MIN: {}, MAX: {}", u32::MIN, u32::MAX);
}
```

## Tushuntirish va Mantiq:
Rust da har bir primitiv son turi o'zining chegaralarini belgilovchi `MIN` va `MAX` assotsiatsiyalangan konstantalariga ega.

## Ishlash natijasi:
```text
i8 MIN: -128, MAX: 127
u8 MIN: 0, MAX: 255
i32 MIN: -2147483648, MAX: 2147483647
u32 MIN: 0, MAX: 4294967295
```

---

# 12-Topshiriq: Arifmetik to'lib ketish va wrapping_add metodi
## Topshiriq sharti:
`u8` turining maksimal qiymatiga (255) 1 qo'shganda xatoliksiz aylanib o'tish (wrapping) metodini qo'llang.

## Yechim (Rust kodi):
```rust
fn main() {
    let son: u8 = 255;
    let natija = son.wrapping_add(1);

    println!("255.wrapping_add(1) = {}", natija);
}
```

## Tushuntirish va Mantiq:
Standart qo'shishda (`+`) debug rejimida dastur to'xtaydi (panic). `wrapping_add` esa modul bo'yicha aylanadi (255 + 1 = 0).

## Ishlash natijasi:
```text
255.wrapping_add(1) = 0
```

---

# 13-Topshiriq: checked_add orqali xavfsiz qo'shish va Option qaytarish
## Topshiriq sharti:
Ikkita sonni qo'shishda to'lib ketish xavfini `checked_add` yordamida tekshiring va natijani chiqaring.

## Yechim (Rust kodi):
```rust
fn main() {
    let a: u8 = 200;
    let b: u8 = 100;

    match a.checked_add(b) {
        Some(natija) => println!("Yig'indi: {}", natija),
        None => println!("Xatolik: Son chegaradan oshib ketdi!"),
    }
}
```

## Tushuntirish va Mantiq:
`checked_add` metodi agar to'lib ketish yuz bersa `None`, aks holda `Some(natija)` qaytaradi. Bu xatoliklarning oldini olishda juda qulay.

## Ishlash natijasi:
```text
Xatolik: Son chegaradan oshib ketdi!
```

---

# 14-Topshiriq: saturating_add va saturating_sub bilan chegarada to'xtash
## Topshiriq sharti:
Chegaradan chiqib ketish o'rniga eng oxirgi minimal yoki maksimal qiymatda to'xtaydigan (saturating) hisob-kitob qiling.

## Yechim (Rust kodi):
```rust
fn main() {
    let max_u8: u8 = 250;
    let qoshish = max_u8.saturating_add(20);

    let min_u8: u8 = 5;
    let ayirish = min_u8.saturating_sub(10);

    println!("250.saturating_add(20) = {}", qoshish);
    println!("5.saturating_sub(10) = {}", ayirish);
}
```

## Tushuntirish va Mantiq:
`saturating_*` metodlari chegaradan chiqishga yo'l qo'ymaydi: maksimaldan oshsa `MAX` (255), noldan kamayib ketsa `MIN` (0) qiymatini qaytaradi.

## Ishlash natijasi:
```text
250.saturating_add(20) = 255
5.saturating_sub(10) = 0
```

---

# 15-Topshiriq: overflowing_mul orqali to'lib ketish bayrog'ini tekshirish
## Topshiriq sharti:
Ikkita sonni ko'paytirib, to'lib ketish yuz bergan yoki bermaganligini aniqlovchi mantiqiy belgi (flag) bilan birga oling.

## Yechim (Rust kodi):
```rust
fn main() {
    let a: u8 = 20;
    let b: u8 = 15; // 300 > 255
    let (natija, tolib_ketdi) = a.overflowing_mul(b);

    println!("Olingan qiymat: {}", natija);
    println!("To'lib ketish yuz berdimi: {}", tolib_ketdi);
}
```

## Tushuntirish va Mantiq:
`overflowing_*` funksiyalari juftlik `(T, bool)` qaytaradi: birinchi element o'ralgan natija, ikkinchi element esa to'lib ketish faktini bildiradi.

## Ishlash natijasi:
```text
Olingan qiymat: 44
To'lib ketish yuz berdimi: true
```

---

# 16-Topshiriq: Suzuvchi nuqtali sonlar: f32 va f64
## Topshiriq sharti:
32-bit va 64-bitli suzuvchi nuqtali haqiqiy sonlarni e'lon qiling va ularning aniqlik farqini ko'rsating.

## Yechim (Rust kodi):
```rust
fn main() {
    let son_f32: f32 = 0.12345678901234567;
    let son_f64: f64 = 0.12345678901234567;

    println!("f32 aniqligi: {}", son_f32);
    println!("f64 aniqligi: {}", son_f64);
}
```

## Tushuntirish va Mantiq:
Rust da standart suzuvchi nuqtali son `f64` hisoblanadi, chunki zamonaviy protsessorlarda u yuqori aniqlikda va deyarli f32 bilan bir xil tezlikda hisoblanadi.

## Ishlash natijasi:
```text
f32 aniqligi: 0.12345679
f64 aniqligi: 0.12345678901234567
```

---

# 17-Topshiriq: Suzuvchi nuqtali sonlar ustida asosiy arifmetik amallar
## Topshiriq sharti:
Suzuvchi nuqtali sonlar ustida qo'shish, ayirish, ko'paytirish, bo'lish va qoldiqli bo'lish amallarini bajaring.

## Yechim (Rust kodi):
```rust
fn main() {
    let a = 9.5f64;
    let b = 2.0f64;

    println!("Qo'shish: {}", a + b);
    println!("Ayirish: {}", a - b);
    println!("Ko'paytirish: {}", a * b);
    println!("Bo'lish: {}", a / b);
    println!("Qoldiq: {}", a % b);
}
```

## Tushuntirish va Mantiq:
Rust da arifmetik amallarda ikkala operand bir xil turda bo'lishi shart. `9.5f64` sintaksisi o'zgaruvchi turini to'g'ridan-to'g'ri son yonida belgilash imkonini beradi.

## Ishlash natijasi:
```text
Qo'shish: 11.5
Ayirish: 7.5
Ko'paytirish: 19
Bo'lish: 4.75
Qoldiq: 1.5
```

---

# 18-Topshiriq: Suzuvchi sonlarni yaxlitlash (round, floor, ceil, trunc)
## Topshiriq sharti:
Haqiqiy sonni matematik qoidalarga ko'ra yaxlitlash, pastga, yuqoriga yaxlitlash va butun qismini ajratib olishni bajaring.

## Yechim (Rust kodi):
```rust
fn main() {
    let x = 3.65;

    println!("round (matematik): {}", x.round());
    println!("floor (pastga):     {}", x.floor());
    println!("ceil (yuqoriga):    {}", x.ceil());
    println!("trunc (butun qism): {}", x.trunc());
}
```

## Tushuntirish va Mantiq:
`round()` eng yaqin butun songa, `floor()` kichik tomonga, `ceil()` katta tomonga yaxlitlaydi. `trunc()` esa kasr qismini shunchaki kesib tashlaydi.

## Ishlash natijasi:
```text
round (matematik): 4
floor (pastga):     3
ceil (yuqoriga):    4
trunc (butun qism): 3
```

---

# 19-Topshiriq: NaN (Not a Number) va is_nan() tekshiruvi
## Topshiriq sharti:
Matematik aniqlanmagan amalni (masalan, manfiy sondan ildiz olish) bajarib, `is_nan` orqali tekshiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let nol = 0.0f64;
    let nolga_bolish = 0.0 / nol;

    println!("Natija: {}", nolga_bolish);
    println!("NaN mi: {}", nolga_bolish.is_nan());
    println!("Cheksizmi: {}", (1.0 / nol).is_infinite());
}
```

## Tushuntirish va Mantiq:
Rust suzuvchi nuqtali sonlarda IEEE 754 standartiga to'liq amal qiladi. 0/0 `NaN` natijasini, 1/0 esa musbat cheksizlik (`inf`) beradi.

## Ishlash natijasi:
```text
Natija: NaN
NaN mi: true
Cheksizmi: true
```

---

# 20-Topshiriq: Mantiqiy tur (bool) va mantiqiy munosabatlar
## Topshiriq sharti:
Mantiqiy o'zgaruvchilar ustida `AND` (`&&`), `OR` (`||`) va `NOT` (`!`) operatorlarini sinab ko'ring.

## Yechim (Rust kodi):
```rust
fn main() {
    let oqishga_kirdi = true;
    let kontrakt_tolandi = false;

    let darsga_ruxsat = oqishga_kirdi && kontrakt_tolandi;
    let kutubxonaga_ruxsat = oqishga_kirdi || kontrakt_tolandi;
    let imtihondan_yiqildimi = !oqishga_kirdi;

    println!("Darsga ruxsat: {}", darsga_ruxsat);
    println!("Kutubxonaga ruxsat: {}", kutubxonaga_ruxsat);
    println!("Yiqildimi: {}", imtihondan_yiqildimi);
}
```

## Tushuntirish va Mantiq:
`bool` turi faqat `true` yoki `false` qiymatlarini oladi va xotirada 1 bayt joy egallaydi. Mantiqiy operatorlar shartli tarmoqlanishlarning asosi hisoblanadi.

## Ishlash natijasi:
```text
Darsga ruxsat: false
Kutubxonaga ruxsat: true
Yiqildimi: false
```

---

# 21-Topshiriq: char turi: 4 baytli Unicode skalar qiymat
## Topshiriq sharti:
Harf, raqam va maxsus belgilarni `char` turida e'lon qilib, ularning xotiradagi hajmini ko'rsating.

## Yechim (Rust kodi):
```rust
fn main() {
    let harf: char = 'Z';
    let belgi: char = '§';
    let xitoycha: char = '中';

    println!("Harf: {}, Belgi: {}, Xitoycha: {}", harf, belgi, xitoycha);
    println!("char o'lchami: {} bayt", std::mem::size_of::<char>());
}
```

## Tushuntirish va Mantiq:
Rust da `char` bitta baytli ASCII emas, balki to'liq 4-baytli Unicode skalar qiymatdir. Shuning uchun unda dunyodagi barcha yozuv belgilari saqlanishi mumkin.

## Ishlash natijasi:
```text
Harf: Z, Belgi: §, Xitoycha: 中
char o'lchami: 4 bayt
```

---

# 22-Topshiriq: char turining ichki tahlil metodlari
## Topshiriq sharti:
`char` turiga tegishli `is_alphabetic`, `is_numeric` va `to_uppercase` metodlaridan foydalaning.

## Yechim (Rust kodi):
```rust
fn main() {
    let belgi1 = 'a';
    let belgi2 = '7';

    println!("'{}' harfmi: {}", belgi1, belgi1.is_alphabetic());
    println!("'{}' raqammi: {}", belgi2, belgi2.is_numeric());
    println!("'{}' bosh harf shakli: {}", belgi1, belgi1.to_uppercase());
}
```

## Tushuntirish va Mantiq:
Rust ning `char` tipi Unicode standartiga asoslangan boy metodlar to'plamiga ega bo'lib, belgilarni osonlikcha tekshirish va o'zgartirish imkonini beradi.

## Ishlash natijasi:
```text
'a' harfmi: true
'7' raqammi: true
'a' bosh harf shakli: A
```

---

# 23-Topshiriq: Unicode va Emoji belgilari bilan to'liq ishlash
## Topshiriq sharti:
Rust char tipida zamonaviy emoji belgisini e'lon qiling va uni konsolga chiqaring.

## Yechim (Rust kodi):
```rust
fn main() {
    let yurak: char = '❤';
    let raketa: char = '🚀';
    let kulgi: char = '😄';

    println!("Rust loyihasi: {} {} {}", raketa, yurak, kulgi);
}
```

## Tushuntirish va Mantiq:
Rust har qanday valid Unicode skalar qiymatni, shu jumladan emojilarni standart primitiv darajada qo'llab-quvvatlaydi.

## Ishlash natijasi:
```text
Rust loyihasi: 🚀 ❤ 😄
```

---

# 24-Topshiriq: Kortejlar (Tuples): Yaratish va indeks orqali o'qish
## Topshiriq sharti:
Turli ma'lumot turlarini birlashtiruvchi kortej (tuple) yarating va uning elementlariga `.0`, `.1` sintaksisi orqali kiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let talaba: (&str, u8, f64) = ("Jasur", 21, 4.75);

    println!("Talaba ismi: {}", talaba.0);
    println!("Talaba yoshi: {}", talaba.1);
    println!("O'rtacha bali: {}", talaba.2);
}
```

## Tushuntirish va Mantiq:
Kortej (tuple) har xil turdagi elementlarni bitta guruhga yig'ish imkonini beradi. Uning uzunligi qat'iy belgilangan bo'lib, keyinchalik o'zgarmaydi.

## Ishlash natijasi:
```text
Talaba ismi: Jasur
Talaba yoshi: 21
O'rtacha bali: 4.75
```

---

# 25-Topshiriq: Kortejni destrukturizatsiya (Destructuring) qilish
## Topshiriq sharti:
Kortejdagi ma'lumotlarni alohida o'zgaruvchilarga pattern matching orqali ajratib oling.

## Yechim (Rust kodi):
```rust
fn main() {
    let koordinata = (10, 20, 30);
    let (x, y, z) = koordinata;

    println!("X koordinata: {}", x);
    println!("Y koordinata: {}", y);
    println!("Z koordinata: {}", z);
}
```

## Tushuntirish va Mantiq:
Destructuring sintaksisi kortejdagi qiymatlarni bitta qatorda alohida o'zgaruvchilarga bo'lib olish imkonini beradi, bu kodning o'qilishini oshiradi.

## Ishlash natijasi:
```text
X koordinata: 10
Y koordinata: 20
Z koordinata: 30
```

---

# 26-Topshiriq: O'zgaruvchan kortej (mutable tuple) qiymatlarini yangilash
## Topshiriq sharti:
`mut` kortej yarating va uning ichidagi biror qiymatni o'zgartiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut tovar = ("Noutbuk", 1200);
    println!("Dastlabki narx: ${}", tovar.1);

    tovar.1 = 1050; // Yangi narx
    println!("Chegirmadagi narx: ${}", tovar.1);
}
```

## Tushuntirish va Mantiq:
Kortej `mut` qilib e'lon qilingan bo'lsa, uning ichki elementlarini o'zgartirish mumkin, biroq element turini o'zgartirib bo'lmaydi.

## Ishlash natijasi:
```text
Dastlabki narx: $1200
Chegirmadagi narx: $1050
```

---

# 27-Topshiriq: Bo'sh kortej: Unit tipi () va uning maqsadi
## Topshiriq sharti:
Qiymat qaytarmaydigan funksiyalar va amallar natijasi bo'lgan `()` (unit) tipini ko'rsating.

## Yechim (Rust kodi):
```rust
fn main() {
    let unit_qiymat: () = ();
    println!("Unit qiymat debug ko'rinishi: {:?}", unit_qiymat);
    println!("Unit turi xotira hajmi: {} bayt", std::mem::size_of::<()>());
}
```

## Tushuntirish va Mantiq:
Rust da `()` bo'sh kortej bo'lib, boshqa tillardagi `void` ga teng keladi. Eng muhimi, u xotirada 0 bayt joy egallaydi (Zero-sized type).

## Ishlash natijasi:
```text
Unit qiymat debug ko'rinishi: ()
Unit turi xotira hajmi: 0 bayt
```

---

# 28-Topshiriq: Massivlar (Arrays [T; N]): Bir xil turdagi statik to'plam
## Topshiriq sharti:
5 ta butun sondan iborat massiv e'lon qiling va uning elementlarini chop eting.

## Yechim (Rust kodi):
```rust
fn main() {
    let sonlar: [i32; 5] = [10, 20, 30, 40, 50];

    println!("1-element: {}", sonlar[0]);
    println!("Oxirgi element: {}", sonlar[4]);
    println!("To'liq massiv: {:?}", sonlar);
}
```

## Tushuntirish va Mantiq:
Massiv `[T; N]` shaklida belgilanadi, bu yerda `T` element turi, `N` esa uning qat'iy sonidir. Massivlar xotiraning Stack qismida ketma-ket joylashadi.

## Ishlash natijasi:
```text
1-element: 10
Oxirgi element: 50
To'liq massiv: [10, 20, 30, 40, 50]
```

---

# 29-Topshiriq: Massivni takrorlanuvchi qiymat bilan qulay to'ldirish
## Topshiriq sharti:
Bir xil boshlang'ich qiymatga ega bo'lgan massivni qisqa sintaksis `[qiymat; soni]` orqali yarating.

## Yechim (Rust kodi):
```rust
fn main() {
    let nollar: [i32; 6] = [0; 6]; // 6 ta nol
    let belgilar = ['*'; 5]; // 5 ta yulduzcha

    println!("Nollar massivi: {:?}", nollar);
    println!("Belgilar massivi: {:?}", belgilar);
}
```

## Tushuntirish va Mantiq:
`[boshlang'ich_qiymat; elementlar_soni]` sintaksisi katta hajmdagi massivlarni qo'lda yozmasdan, bir lahzada xavfsiz initsializatsiya qilishni ta'minlaydi.

## Ishlash natijasi:
```text
Nollar massivi: [0, 0, 0, 0, 0, 0]
Belgilar massivi: ['*', '*', '*', '*', '*']
```

---

# 30-Topshiriq: O'zgaruvchan massiv elementlarini yangilash
## Topshiriq sharti:
`mut` massiv yarating va uning ma'lum bir indeksidagi elementini o'zgartiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut baholar = [85, 90, 78, 92];
    println!("Dastlabki: {:?}", baholar);

    baholar[2] = 88; // 78 ni 88 ga o'zgartirish
    println!("O'zgartirilgan: {:?}", baholar);
}
```

## Tushuntirish va Mantiq:
Massiv `mut` bo'lsa, elementlar qayta tayinlanishi mumkin. Ammo massivning uzunligi hech qachon oshmaydi yoki kamaymaydi.

## Ishlash natijasi:
```text
Dastlabki: [85, 90, 78, 92]
O'zgartirilgan: [85, 90, 88, 92]
```

---

# 31-Topshiriq: Massiv uzunligi (.len()) va umumiy xotira hajmi
## Topshiriq sharti:
Massivning elementlar soni hamda uning Stack xotirasida egallagan aniq baytlar miqdorini hisoblang.

## Yechim (Rust kodi):
```rust
fn main() {
    let massiv: [i64; 4] = [100, 200, 300, 400];

    println!("Elementlar soni: {}", massiv.len());
    println!("Massiv egallagan bayt: {} bayt", std::mem::size_of_val(&massiv));
}
```

## Tushuntirish va Mantiq:
Har bir `i64` soni 8 bayt egallaydi. 4 ta elementdan iborat massiv xotirada aynan 4 * 8 = 32 bayt joy oladi. Ortiqcha qo'shimcha xarajat (overhead) mavjud emas.

## Ishlash natijasi:
```text
Elementlar soni: 4
Massiv egallagan bayt: 32 bayt
```

---

# 32-Topshiriq: Massiv chegarasidan chiqish (Out of Bounds) xavfsizligi
## Topshiriq sharti:
Rust da massiv elementiga indeks orqali murojaat qilishda kompilyator va ish vaqtidagi (runtime) xavfsizlik tekshiruvini tushuntiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let raqamlar = [1, 2, 3];
    let indeks = 1;

    if indeks < raqamlar.len() {
        println!("Tanlangan qiymat: {}", raqamlar[indeks]);
    } else {
        println!("Indeks massiv chegarasidan tashqarida!");
    }
}
```

## Tushuntirish va Mantiq:
C/C++ tillaridan farqli ravishda, Rust da massiv chegarasidan tashqariga noqonuniy murojaat qilinsa, xotirani buzish o'rniga dastur panic bilan to'xtaydi.

## Ishlash natijasi:
```text
Tanlangan qiymat: 2
```

---

# 33-Topshiriq: Ko'p o'lchamli massivlar (2D Matrix)
## Topshiriq sharti:
3x3 o'lchamli ikki o'lchamli massiv (matritsa) yarating va uning markaziy hamda burchak elementlariga kiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let matritsa: [[i32; 3]; 3] = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ];

    println!("Markaziy element (1,1): {}", matritsa[1][1]);
    println!("O'ng quyi burchak (2,2): {}", matritsa[2][2]);
}
```

## Tushuntirish va Mantiq:
Rust da ko'p o'lchamli massivlar massivlar massividan iborat bo'lib, xotirada bitta uzluksiz chiziqli blokda saqlanadi, bu kesh unumdorligini oshiradi.

## Ishlash natijasi:
```text
Markaziy element (1,1): 5
O'ng quyi burchak (2,2): 9
```

---

# 34-Topshiriq: as operatori yordamida sonli tiplarni konvertatsiya qilish
## Topshiriq sharti:
`as` operatori orqali `i32` butun sonini `f64` haqiqiy songa aylantiring va bo'lish amalini aniq hisoblang.

## Yechim (Rust kodi):
```rust
fn main() {
    let a: i32 = 15;
    let b: i32 = 4;

    // Butun sonli bo'lish: 15 / 4 = 3
    let butun_bolish = a / b;
    // Haqiqiy sonli aniq bo'lish: 15.0 / 4.0 = 3.75
    let aniq_bolish = (a as f64) / (b as f64);

    println!("Butun sonli natija: {}", butun_bolish);
    println!("Aniq f64 natijasi: {}", aniq_bolish);
}
```

## Tushuntirish va Mantiq:
Rust da avtomatik implisit tur o'zgarishi yo'q. Bir turni ikkinchisiga o'tkazish uchun dasturchi `as` operatori orqali o'z niyatini qat'iy ifodalashi shart.

## Ishlash natijasi:
```text
Butun sonli natija: 3
Aniq f64 natijasi: 3.75
```

---

# 35-Topshiriq: Katta butun sondan kichik butun songa 'as' orqali o'tish (Truncating)
## Topshiriq sharti:
Katta `u32` sonini `u8` turiga o'tkazganda nima sodir bo'lishini namoyish eting.

## Yechim (Rust kodi):
```rust
fn main() {
    let katta_son: u32 = 300; // Ikkilikda: 00000001 00101100
    let kichik_son: u8 = katta_son as u8; // Oxirgi 8 bit: 00101100 (44)

    println!("300 as u8 = {}", kichik_son);
}
```

## Tushuntirish va Mantiq:
`as` orqali kattaroq butun sondan kichigiga o'tilganda, yuqori bitlar kesib tashlanadi (truncation). Bu ma'lumot yo'qolishiga sabab bo'lishi mumkin.

## Ishlash natijasi:
```text
300 as u8 = 44
```

---

# 36-Topshiriq: u8 baytidan char turiga as orqali xavfsiz o'tish
## Topshiriq sharti:
ASCII kodi bo'lgan `u8` sonini to'g'ridan-to'g'ri `char` belgisiga aylantiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let kod: u8 = 65;
    let belgi: char = kod as char;

    println!("ASCII {} kodi belgisi: '{}'", kod, belgi);
}
```

## Tushuntirish va Mantiq:
Har qanday `u8` qiymati valid ASCII (0-127) yoki valid Extended ASCII bo'lgani sababli, `u8 as char` konvertatsiyasi har doim xavfsiz va xatosiz ishlaydi.

## Ishlash natijasi:
```text
ASCII 65 kodi belgisi: 'A'
```

---

# 37-Topshiriq: Bitwise AND (&) amali va bit maskalash
## Topshiriq sharti:
Ikkita son ustida bitli `AND` amalini bajarib, ma'lum bir bitning yoqilganligini tekshiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let qiymat: u8 = 0b1101_1010;
    let maska: u8  = 0b0000_1000; // 4-bitni tekshiramiz

    let natija = qiymat & maska;
    println!("qiymat & maska = {:08b} (o'nlikda: {})", natija, natija);
}
```

## Tushuntirish va Mantiq:
`&` operatori ikkala bit ham 1 bo'lgandagina 1 qiymatini beradi. Bu apparat darajasida registrlarni o'qish va filtrlashda asosiy vositadir.

## Ishlash natijasi:
```text
qiymat & maska = 00001000 (o'nlikda: 8)
```

---

# 38-Topshiriq: Bitwise OR (|) amali va bayroqlarni (flags) yoqish
## Topshiriq sharti:
Bitli `OR` operatori yordamida kerakli bitni 1 holatiga keltiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let holat: u8  = 0b0000_0001; // O'qish ruxsati
    let yozish: u8 = 0b0000_0010; // Yozish ruxsati

    let toliq_ruxsat = holat | yozish;
    println!("Yangi huquqlar: {:08b}", toliq_ruxsat);
}
```

## Tushuntirish va Mantiq:
`|` operatori kamida bitta bit 1 bo'lsa natijani 1 qiladi. Tizimli dasturlashda bir nechta ruxsatnomalarni bitta baytda saqlash uchun ishlatiladi.

## Ishlash natijasi:
```text
Yangi huquqlar: 00000011
```

---

# 39-Topshiriq: Bitwise XOR (^) amali va bitlarni almashtirish
## Topshiriq sharti:
Bitli `XOR` yordamida bitlarni invert qilish va uchinchi o'zgaruvchisiz ikki sonni almashtirishni sinab ko'ring.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut a = 15;
    let mut b = 27;

    // XOR swap algoritmi
    a = a ^ b;
    b = a ^ b;
    a = a ^ b;

    println!("a ning yangi qiymati: {}", a);
    println!("b ning yangi qiymati: {}", b);
}
```

## Tushuntirish va Mantiq:
`^` (XOR) operatori bitlar turli bo'lganda 1, bir xil bo'lganda 0 qaytaradi. U kriptografiya va ma'lumotlarni shifrlashda nihoyatda keng qo'llaniladi.

## Ishlash natijasi:
```text
a ning yangi qiymati: 27
b ning yangi qiymati: 15
```

---

# 40-Topshiriq: Bitwise NOT (!) amali va bitlarni teskari qilish
## Topshiriq sharti:
Rust da bitlarni inkor qilish uchun `!` operatoridan foydalaning.

## Yechim (Rust kodi):
```rust
fn main() {
    let son: u8 = 0b0000_1111;
    let teskari: u8 = !son;

    println!("Dastlabki: {:08b}", son);
    println!("Teskari:   {:08b}", teskari);
}
```

## Tushuntirish va Mantiq:
Rust da boshqa tillardagi `~` o'rniga bitli inkor uchun ham `!` belgisi ishlatiladi. U barcha 0 larni 1 ga, 1 larni 0 ga aylantiradi.

## Ishlash natijasi:
```text
Dastlabki: 00001111
Teskari:   11110000
```

---

# 41-Topshiriq: Chapga bit surish (<<) orqali 2 ning darajasiga ko'paytirish
## Topshiriq sharti:
Chapga surish operatori yordamida sonni tezkor ravishda 2, 4, 8 ga ko'paytiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let son: u32 = 5;

    let kopaytirilgan_2 = son << 1; // 5 * 2 = 10
    let kopaytirilgan_4 = son << 2; // 5 * 4 = 20
    let kopaytirilgan_8 = son << 3; // 5 * 8 = 40

    println!("5 << 1 = {}", kopaytirilgan_2);
    println!("5 << 2 = {}", kopaytirilgan_4);
    println!("5 << 3 = {}", kopaytirilgan_8);
}
```

## Tushuntirish va Mantiq:
`<< N` amali sonning barcha bitlarini chapga N pog'ona suradi. Bu arifmetik jihatdan sonni 2^N ga ko'paytirishga teng va apparat darajasida 1 siklda bajariladi.

## Ishlash natijasi:
```text
5 << 1 = 10
5 << 2 = 20
5 << 3 = 40
```

---

# 42-Topshiriq: O'ngga bit surish (>>) orqali 2 ning darajasiga bo'lish
## Topshiriq sharti:
O'ngga surish operatori orqali sonni butunli bo'lishni bajaring.

## Yechim (Rust kodi):
```rust
fn main() {
    let son: u32 = 64;

    let bolingan_2 = son >> 1; // 32
    let bolingan_4 = son >> 2; // 16
    let bolingan_8 = son >> 3; // 8

    println!("64 >> 1 = {}", bolingan_2);
    println!("64 >> 2 = {}", bolingan_4);
    println!("64 >> 3 = {}", bolingan_8);
}
```

## Tushuntirish va Mantiq:
`>> N` amali sonni 2^N ga butunli bo'lishga teng bo'lib, o'ng tomondagi eng kichik ahamiyatli bitlar tushib qoladi.

## Ishlash natijasi:
```text
64 >> 1 = 32
64 >> 2 = 16
64 >> 3 = 8
```

---

# 43-Topshiriq: count_ones va count_zeros: Bitlarni apparat darajasida sanash
## Topshiriq sharti:
Sonning binar ko'rinishidagi 1 lar (popcount) va 0 lar sonini maxsus metodlar bilan hisoblang.

## Yechim (Rust kodi):
```rust
fn main() {
    let son: u8 = 0b1011_0101;

    println!("1 lar soni (popcount): {}", son.count_ones());
    println!("0 lar soni:            {}", son.count_zeros());
}
```

## Tushuntirish va Mantiq:
`count_ones()` zamonaviy protsessorlarning POPCNT instruksiyasidan foydalanadi va sun'iy intellekt, 1-bit modellar va kriptografiyada muhim hisoblanadi.

## Ishlash natijasi:
```text
1 lar soni (popcount): 5
0 lar soni:            3
```

---

# 44-Topshiriq: Type Alias (Tur taxallusi) yaratish
## Topshiriq sharti:
`type` kalit so'zi yordamida mavjud turlarga yangi semantik nom bering.

## Yechim (Rust kodi):
```rust
type Kilogramm = f64;
type FoydalanuvchiID = u64;

fn main() {
    let ogirlik: Kilogramm = 75.5;
    let id: FoydalanuvchiID = 10042;

    println!("Foydalanuvchi #{} og'irligi: {} kg", id, ogirlik);
}
```

## Tushuntirish va Mantiq:
`type` alias yangi mustaqil tur yaratmaydi, balki mavjud turga qulay laqab (taxallus) beradi, bu kodning ma'nosini chuqurroq ifodalaydi.

## Ishlash natijasi:
```text
Foydalanuvchi #10042 og'irligi: 75.5 kg
```

---

# 45-Topshiriq: Formatlash makrolari: Positional argumentlar
## Topshiriq sharti:
`println!` ichida o'rin (indeks) bo'yicha argumentlarni qayta-qayta ishlatishni ko'rsating.

## Yechim (Rust kodi):
```rust
fn main() {
    let ism = "Ali";
    let til = "Rust";

    println!("{0} bugun {1} o'rganmoqda. Ha, aynan {0} {1}ni yaxshi ko'radi!", ism, til);
}
```

## Tushuntirish va Mantiq:
`{0}`, `{1}` positional parametrlari berilgan qiymatlarni kerakli tartibda va bir necha marta takrorlab chop etish imkonini beradi.

## Ishlash natijasi:
```text
Ali bugun Rust o'rganmoqda. Ha, aynan Ali Rustni yaxshi ko'radi!
```

---

# 46-Topshiriq: Formatlash makrolari: Nomlangan parametrlar
## Topshiriq sharti:
Format satrida parametrlarga nom berib, ularni xavfsiz joylashtiring.

## Yechim (Rust kodi):
```rust
fn main() {
    println!(
        "{shahar} shahrida havo harorati {harorat}°C daraja.",
        shahar = "Samarqand",
        harorat = 24
    );
}
```

## Tushuntirish va Mantiq:
Nomlangan parametrlar satr formatini o'ta tushunarli qiladi va parametrlar tartibi o'zgarishidan kelib chiqadigan xatolarni bartaraf etadi.

## Ishlash natijasi:
```text
Samarqand shahrida havo harorati 24°C daraja.
```

---

# 47-Topshiriq: Sonlarni formatlash: Kasr qismini aniq cheklash ({:.N})
## Topshiriq sharti:
Suzuvchi nuqtali sonning faqat kerakli 2 ta yoki 3 ta kasr xonasini chop eting.

## Yechim (Rust kodi):
```rust
fn main() {
    let pi = 3.141592653589793;

    println!("2 xonagacha: {:.2}", pi);
    println!("4 xonagacha: {:.4}", pi);
}
```

## Tushuntirish va Mantiq:
`{:.N}` formati haqiqiy sonning kasr qismini N ta raqamgacha yaxlitlab ko'rsatishni buyuradi.

## Ishlash natijasi:
```text
2 xonagacha: 3.14
4 xonagacha: 3.1416
```

---

# 48-Topshiriq: Sonlarni ikkilik ({:b}) va o'n oltilik ({:x}, {:X}) ko'rinishda chiqarish
## Topshiriq sharti:
Bitta sonning turli sanoq tizimlaridagi matnli ko'rinishini chiqaring.

## Yechim (Rust kodi):
```rust
fn main() {
    let son = 254;

    println!("O'nlikda:      {}", son);
    println!("Ikkilikda:     {:b}", son);
    println!("O'n oltilikda: {:x}", son);
    println!("Katta HEX da:  {:X}", son);
}
```

## Tushuntirish va Mantiq:
`:b` ikkilik sanoq tizimini, `:x` kichik harfli o'n oltilikni, `:X` esa bosh harfli o'n oltilikni ifodalaydi.

## Ishlash natijasi:
```text
O'nlikda:      254
Ikkilikda:     11111110
O'n oltilikda: fe
Katta HEX da:  FE
```

---

# 49-Topshiriq: Joy to'ldirish (Padding) va tekislash ({:>N}, {:0<N})
## Topshiriq sharti:
Matn yoki raqamlarni konsolda chiroyli jadval ko'rinishida tekislash uchun to'ldirish belgilarini ishlating.

## Yechim (Rust kodi):
```rust
fn main() {
    let son = 42;

    println!("O'ngga tekislash (10 ta joy): '{:>10}'", son);
    println!("Chapga tekislash (10 ta joy): '{:<10}'", son);
    println!("Nollar bilan to'ldirish:     '{:0>8}'", son);
}
```

## Tushuntirish va Mantiq:
`{:>N}` o'ng tomonga tekislaydi, `{:0>8}` esa uzunlik 8 ga yetguncha chap tomondan nollar bilan to'ldiradi. Bu hisobot va loglarni chiroyli chiqarishda qo'llaniladi.

## Ishlash natijasi:
```text
O'ngga tekislash (10 ta joy): '        42'
Chapga tekislash (10 ta joy): '42        '
Nollar bilan to'ldirish:     '00000042'
```

---

# 50-Topshiriq: Kompilyatsiya vaqtidagi tekshiruv va statik konstantalar
## Topshiriq sharti:
Kompilyatsiya vaqtida arifmetik ifodalar bilan hisoblanadigan murakkab `const` qiymatni e'lon qiling.

## Yechim (Rust kodi):
```rust
const SOAT_SEKUNDI: u64 = 60 * 60;
const KUN_SEKUNDI: u64 = SOAT_SEKUNDI * 24;
const HAFTA_SEKUNDI: u64 = KUN_SEKUNDI * 7;

fn main() {
    println!("1 soat: {} sekund", SOAT_SEKUNDI);
    println!("1 kun:  {} sekund", KUN_SEKUNDI);
    println!("1 hafta: {} sekund", HAFTA_SEKUNDI);
}
```

## Tushuntirish va Mantiq:
Rust kompilyatori barcha `const` ifodalarni kompilyatsiya vaqtida (compile-time) hisoblab chiqadi. Bu dasturning ishga tushish tezligini oshiradi va nolinchi sarf-xarajat ta'minlaydi.

## Ishlash natijasi:
```text
1 soat: 3600 sekund
1 kun:  86400 sekund
1 hafta: 604800 sekund
```

---
