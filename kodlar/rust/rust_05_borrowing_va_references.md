# 5-Qism: Borrowing (Qarz Olish) va References (Havolalar) (201-250)

Ushbu qismda Rust ning xotira arxitekturasining ikkinchi asosiy ustuni bo'lgan **Borrowing (Qarz olish)** mexanizmi, o'zgarmas havolalar (`&T`), o'zgaruvchan havolalar (`&mut T`), Dereferencing (`*`), Auto-dereferencing, Non-Lexical Lifetimes (NLL), Iterator Invalidation ning oldini olish, `split_at_mut` va Borrow Checker qoidalari amaliy topshiriqlarda chuqur tahlil qilinadi.

---

# 201-Topshiriq: Borrowing (Qarz olish) tushunchasi va & operatori
## Topshiriq sharti:
Egalikni bermasdan, ma'lumotdan vaqtincha foydalanishga berishni namoyish eting.

## Yechim (Rust kodi):
```rust
fn main() {
    let s1 = String::from("Rust tili");
    let uzunlik = hisobla_uzunlik(&s1); // s1 ning egasligi berilmadi, faqat havola (&) uzatildi

    println!("'{}' ning uzunligi: {}", s1, uzunlik);
}

fn hisobla_uzunlik(s: &String) -> usize {
    s.len()
} // Bu yerda 's' scope dan chiqadi, lekin havola bo'lgani uchun asl String o'chirilmaydi!
```

## Tushuntirish va Mantiq:
Borrowing qiymatni boshqa funksiya yoki o'zgaruvchiga vaqtincha foydalanish uchun berishdir. Qiymat o'z egasida qoladi va xotiradan o'chib ketmaydi.

## Ishlash natijasi:
```text
'Rust tili' ning uzunligi: 9
```

---

# 202-Topshiriq: O'zgarmas havolalar (Immutable References: &T)
## Topshiriq sharti:
O'zgarmas havola orqali qiymatni o'qish mumkinligi, lekin o'zgartirib bo'lmasligini ko'rsating.

## Yechim (Rust kodi):
```rust
fn main() {
    let shahar = String::from("Buxoro");
    let havola: &String = &shahar;

    println!("Shaharga havola: {}", havola);
    // havola.push_str(" qadimiy"); // Xatolik: &String orqali ma'lumotni o'zgartirib bo'lmaydi!
}
```

## Tushuntirish va Mantiq:
`&T` faqat o'qish huquqini beruvchi havoladir. U xotiradagi ma'lumotni o'zgartirishdan to'liq himoyalaydi.

## Ishlash natijasi:
```text
Shaharga havola: Buxoro
```

---

# 203-Topshiriq: Bir vaqtda bir nechta o'zgarmas havolalar yaratish (Aliasing)
## Topshiriq sharti:
Bitta o'zgaruvchidan istalgancha o'zgarmas havola olish mumkinligini namoyish eting.

## Yechim (Rust kodi):
```rust
fn main() {
    let ma'lumot = String::from("Markaziy Ma'lumot");

    let r1 = &ma'lumot;
    let r2 = &ma'lumot;
    let r3 = &ma'lumot;

    println!("r1: {}, r2: {}, r3: {}", r1, r2, r3);
}
```

## Tushuntirish va Mantiq:
Faqat o'qish amali hech qachon xotirani buzmaydi. Shu sababli Rust da bitta resursga bir vaqtning o'zida cheksiz miqdorda o'zgarmas havola (`&T`) olishga ruxsat beriladi.

## Ishlash natijasi:
```text
r1: Markaziy Ma'lumot, r2: Markaziy Ma'lumot, r3: Markaziy Ma'lumot
```

---

# 204-Topshiriq: O'zgaruvchan havolalar (Mutable References: &mut T)
## Topshiriq sharti:
Qiymatni havola orqali o'zgartirish uchun `&mut` dan foydalaning.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut shior = String::from("Rust");
    qoshimcha_yoz(&mut shior);

    println!("O'zgartirilgan shior: {}", shior);
}

fn qoshimcha_yoz(matn: &mut String) {
    matn.push_str(" kelajak tili!");
}
```

## Tushuntirish va Mantiq:
Agar qiymatni havola orqali o'zgartirish kerak bo'lsa, o'zgaruvchining o'zi `let mut` bo'lishi va havolasi `&mut` shaklida olinishi shart.

## Ishlash natijasi:
```text
O'zgartirilgan shior: Rust kelajak tili!
```

---

# 205-Topshiriq: Borrowing ning oltin qoidasi: Aliasing XOR Mutability
## Topshiriq sharti:
Bir vaqtda faqat 1 ta `&mut` YOKI istalgancha `&T` bo'lishi mumkinligini tushuntiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut x = 10;

    {
        let r1 = &mut x;
        *r1 += 5;
        println!("r1 orqali o'zgardi: {}", r1);
    } // r1 ning hayoti tugadi

    // Endi yangi o'zgarmas havola olish mumkin
    let r2 = &x;
    println!("r2 o'qidi: {}", r2);
}
```

## Tushuntirish va Mantiq:
Rust ning asosiy xavfsizlik qoidasi: Agar siz ma'lumotni o'zgartirmoqchi bo'lsangiz (`&mut`), u paytda boshqa hech kim uni o'qiy olmasligi va yoza olmasligi kerak.

## Ishlash natijasi:
```text
r1 orqali o'zgardi: 15
r2 o'qidi: 15
```

---

# 206-Topshiriq: Nega bir vaqtda ikkita &mut havola taqiqlanadi? (Data Race yo'qligi)
## Topshiriq sharti:
Ikkita o'zgaruvchan havola ruxsat berilmasligining kiberxavfsizlik sababini ko'rsating.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut hisob = 100;

    // Quyidagi kod kompilyatsiya xatoligiga sabab bo'ladi:
    // let h1 = &mut hisob;
    // let h2 = &mut hisob; // Xatolik: ikkinchi &mut havola!
    // println!("{}, {}", h1, h2);

    println!("Rust bir vaqtda 2 ta &mut havolani taqiqlab, 'Data Race' muammosini yo'q qiladi!");
    let h1 = &mut hisob;
    *h1 += 50;
    println!("Hisob yangilandi: {}", h1);
}
```

## Tushuntirish va Mantiq:
Agar ikkita havola bir vaqtda bitta xotiraga yozishga urinsa, poyga xatosi (Data Race) kelib chiqadi. Rust buni kompilyatsiya vaqtida to'xtatadi.

## Ishlash natijasi:
```text
Rust bir vaqtda 2 ta &mut havolani taqiqlab, 'Data Race' muammosini yo'q qiladi!
Hisob yangilandi: 150
```

---

# 207-Topshiriq: O'zgarmas havola bor joyda &mut olish taqiqlanishi
## Topshiriq sharti:
Birov o'qiyotgan paytda boshqa birov ma'lumotni o'zgartira olmasligini namoyish eting.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut matn = String::from("Asl nusxa");

    let oquvchi = &matn; // O'qish uchun havola
    println!("O'quvchi ko'rdi: {}", oquvchi);

    // Endi oquvchi ishlatib bo'lingach, &mut olish mumkin:
    let yozuvchi = &mut matn;
    yozuvchi.push_str(" (Yangilandi)");
    println!("Yozuvchi yozdi: {}", yozuvchi);
}
```

## Tushuntirish va Mantiq:
O'quvchi ma'lumotni o'qiyotgan vaqtda uning ostidagi zamin o'zgarib ketmasligi kerak. Shuning uchun `&T` faol bo'lgan davrda `&mut T` olish mumkin emas.

## Ishlash natijasi:
```text
O'quvchi ko'rdi: Asl nusxa
Yozuvchi yozdi: Asl nusxa (Yangilandi)
```

---

# 208-Topshiriq: Dereferencing: * operatori orqali qiymatni ochish
## Topshiriq sharti:
Ko'rsatkich ortidagi asl qiymatga `*` orqali murojaat qiling.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut son = 42;
    let havola = &mut son;

    *havola += 8; // * orqali 'son' ning o'ziga yozamiz

    println!("Asl son qiymati: {}", son);
}
```

## Tushuntirish va Mantiq:
`*` (dereference) operatori havola ishora qilib turgan asl xotira katakchasini ochadi. Qiymat yozish yoki primitiv qiymatni o'qishda ishlatiladi.

## Ishlash natijasi:
```text
Asl son qiymati: 50
```

---

# 209-Topshiriq: Auto-dereferencing (Avtomatik dereferensiya) metod chaqiruvlarida
## Topshiriq sharti:
Rust ning `.` operatori havolalarni avtomatik tarzda o'zi ochishini ko'rsating.

## Yechim (Rust kodi):
```rust
fn main() {
    let matn = String::from("Rust");
    let havola = &matn;

    // (*havola).len() deb yozish shart emas:
    println!("Uzunlik: {}", havola.len());
}
```

## Tushuntirish va Mantiq:
Rust dasturchi qulayligi uchun metod chaqiruvlarida (`.`) kerakli miqdorda `*` va `&` larni o'zi avtomatik qo'yadi.

## Ishlash natijasi:
```text
Uzunlik: 4
```

---

# 210-Topshiriq: Non-Lexical Lifetimes (NLL): Havola hayotining erta tugashi
## Topshiriq sharti:
Havolaning jingalak qavsgacha emas, balki oxirgi ishlatilgan qatorda tugashini namoyish eting.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut x = 5;

    let r1 = &x;
    println!("r1 qiymati: {}", r1); // r1 ning oxirgi ishlatilish nuqtasi

    // Rust 2018/2021/2024 NLL tufayli bu yerda r1 tugagan deb hisoblanadi:
    let r2 = &mut x;
    *r2 += 10;
    println!("r2 yangiladi: {}", r2);
}
```

## Tushuntirish va Mantiq:
Non-Lexical Lifetimes (NLL) borrow checker ning intellektual qobiliyatidir: havola o'z doirasi (scope) tugashini kutmasdan, oxirgi qatorda o'z huquqini bo'shatadi.

## Ishlash natijasi:
```text
r1 qiymati: 5
r2 yangiladi: 15
```

---

# 211-Topshiriq: Dangling References (Osilgan ko'rsatkichlar)ning to'xtatilishi
## Topshiriq sharti:
Funksiyadan lokal xotiraning havolasini qaytarib bo'lmasligini tushuntiring.

## Yechim (Rust kodi):
```rust
// Quyidagi kod kompilyatsiyadan o'tmaydi:
// fn xavfli_havola() -> &String {
//     let s = String::from("Salom");
//     &s // Xatolik: s funksiya tugashi bilan o'ladi, havola havoda muallaq qoladi!
// }

fn xavfsiz_usul() -> String {
    let s = String::from("Salom");
    s // Egalikning o'zi qaytariladi!
}

fn main() {
    let res = xavfsiz_usul();
    println!("Xavfsiz qaytgan matn: {}", res);
}
```

## Tushuntirish va Mantiq:
C da lokal o'zgaruvchi manzilini qaytarish 'Segmentation Fault' ga sabab bo'ladi. Rust da Borrow Checker bunday kodni kompilyatsiya qilishga umuman ruxsat bermaydi.

## Ishlash natijasi:
```text
Xavfsiz qaytgan matn: Salom
```

---

# 212-Topshiriq: Funksiyadan parametr sifatida kelgan havolani qaytarish
## Topshiriq sharti:
Kiruvchi havola bilan chiquvchi havola bir xil manbaga ega bo'lganda ruxsat berilishini ko'rsating.

## Yechim (Rust kodi):
```rust
fn bosh_harfni_ol(matn: &str) -> &str {
    &matn[0..1]
}

fn main() {
    let shahar = "Toshkent";
    let bosh = bosh_harfni_ol(shahar);

    println!("Bosh harf: {}", bosh);
}
```

## Tushuntirish va Mantiq:
Agar funksiyadan qaytayotgan havola kiruvchi parametr havolasiga tayansa, u yaroqli bo'ladi, chunki ma'lumotning o'zi funksiyadan tashqarida yashaydi.

## Ishlash natijasi:
```text
Bosh harf: T
```

---

# 213-Topshiriq: Havolaning havolasi (References to References: &&T)
## Topshiriq sharti:
Havolaga ko'rsatkich yaratib, ko'p pog'onali dereferencing ni sinab ko'ring.

## Yechim (Rust kodi):
```rust
fn main() {
    let son = 100;
    let ref1 = &son;
    let ref2 = &ref1;

    println!("son: {}", son);
    println!("*ref1: {}", *ref1);
    println!("**ref2: {}", **ref2);
}
```

## Tushuntirish va Mantiq:
Rust da istalgancha chuqur havolalar yaratish mumkin. Har bir `*` bitta havola pog'onasini ochadi.

## Ishlash natijasi:
```text
son: 100
*ref1: 100
**ref2: 100
```

---

# 214-Topshiriq: Pattern Matching da 'ref' va '&' farqi
## Topshiriq sharti:
`&` mavjud havolani tekshirishda, `ref` esa yangi havola yaratishda ishlatilishini ko'rsating.

## Yechim (Rust kodi):
```rust
fn main() {
    let son = 42;
    let havola = &son;

    // & bilan tekshiramiz:
    let &qiymat = havola; // qiymat endi i32 turida

    // ref bilan havola olamiz:
    let ref yangi_havola = son; // yangi_havola &i32 turida

    println!("qiymat: {}, yangi_havola: {}", qiymat, *yangi_havola);
}
```

## Tushuntirish va Mantiq:
`&` pattern da destructuring qiladi (havolani yechadi), `ref` esa o'zgaruvchini Move qilmasdan unga havola hosil qiladi.

## Ishlash natijasi:
```text
qiymat: 42, yangi_havola: 42
```

---

# 215-Topshiriq: Struktura maydonlariga havola orqali kirish
## Topshiriq sharti:
Strukturaga `&` havola qilib, uning maydonlarini o'qish.

## Yechim (Rust kodi):
```rust
struct Avto {
    model: String,
    yil: u32,
}

fn malumot_ber(a: &Avto) {
    println!("Avto: {}, Yili: {}", a.model, a.yil);
}

fn main() {
    let mashina = Avto {
        model: String::from("Cobalt"),
        yil: 2023,
    };
    malumot_ber(&mashina);
    println!("Asl mashina yaroqli: {}", mashina.model);
}
```

## Tushuntirish va Mantiq:
Struktura havolasi orqali uning barcha maydonlarini o'qish mumkin va bunda strukturaning egasligi chaqiruvchida saqlanib qoladi.

## Ishlash natijasi:
```text
Avto: Cobalt, Yili: 2023
Asl mashina yaroqli: Cobalt
```

---

# 216-Topshiriq: Struktura maydonlarini &mut havola orqali yangilash
## Topshiriq sharti:
Funksiyaga `&mut Avto` berib, uning yili yoki modelini o'zgartiring.

## Yechim (Rust kodi):
```rust
struct Avto {
    model: String,
    yurgan_masofa: u32,
}

fn haydash(a: &mut Avto, km: u32) {
    a.yurgan_masofa += km;
}

fn main() {
    let mut m = Avto {
        model: String::from("Nexia"),
        yurgan_masofa: 50_000,
    };
    haydash(&mut m, 1200);

    println!("Yangi masofa: {} km", m.yurgan_masofa);
}
```

## Tushuntirish va Mantiq:
`&mut` orqali strukturaning istalgan maydonini xavfsiz yangilash mumkin. Hech qanday nusxalash talab etilmaydi.

## Ishlash natijasi:
```text
Yangi masofa: 51200 km
```

---

# 217-Topshiriq: Iterator Invalidation muammosining Rust da to'xtatilishi
## Topshiriq sharti:
Vektor elementiga havola ushlab turilgan paytda unga `push()` qilish taqiqlanishini ko'rsating.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut v = vec![1, 2, 3];
    let birinchi = &v[0]; // O'zgarmas havola olindi

    println!("Birinchi: {}", birinchi);

    // v.push(4); // Agar shu yerda push qilinsa, xotira boshqa manzilga ko'chib, 'birinchi' ko'rsatkichi osilib qolardi!
    v.push(4); // Bu yerda esa 'birinchi' boshqa ishlatilmagani uchun ruxsat beriladi!
    println!("Vektor yangilandi: {:?}", v);
}
```

## Tushuntirish va Mantiq:
C++ da `vector.push_back()` qilinganda barcha mavjud iteratorlar va ko'rsatkichlar buziladi (Iterator Invalidation). Rust bu halokatli xatoni 100% ushlab oladi.

## Ishlash natijasi:
```text
Birinchi: 1
Vektor yangilandi: [1, 2, 3, 4]
```

---

# 218-Topshiriq: get() metodi orqali xavfsiz Option<&T> olish
## Topshiriq sharti:
Massiv yoki vektordan indeks chegarasidan chiqib ketish xavfisiz havola olish.

## Yechim (Rust kodi):
```rust
fn main() {
    let mevalar = vec!["Olma", "Anor", "Uzum"];

    match mevalar.get(1) {
        Some(meva) => println!("Tanlangan meva: {}", meva),
        None => println!("Bunday indeks mavjud emas."),
    }

    match mevalar.get(10) {
        Some(meva) => println!("Tanlangan meva: {}", meva),
        None => println!("10-indeks topilmadi!"),
    }
}
```

## Tushuntirish va Mantiq:
To'g'ridan-to'g'ri `v[i]` indekslash chegaradan oshganda dasturni to'xtatadi. `.get(i)` esa `Option<&T>` qaytarib, dastur barqarorligini ta'minlaydi.

## Ishlash natijasi:
```text
Tanlangan meva: Anor
10-indeks topilmadi!
```

---

# 219-Topshiriq: get_mut() orqali elementni o'zgaruvchan havola sifatida xavfsiz olish
## Topshiriq sharti:
Vektor elementini xavfsiz tekshiruv bilan o'zgartiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut sonlar = vec![10, 20, 30];

    if let Some(elem) = sonlar.get_mut(1) {
        *elem += 500;
    }

    println!("Natijaviy vektor: {:?}", sonlar);
}
```

## Tushuntirish va Mantiq:
`get_mut(i)` xavfsiz `Option<&mut T>` beradi va indeks mavjud bo'lsa elementni darhol o'zgartirishga imkon beradi.

## Ishlash natijasi:
```text
Natijaviy vektor: [10, 520, 30]
```

---

# 220-Topshiriq: Havolalar manzilini solishtirish: std::ptr::eq
## Topshiriq sharti:
Ikkita havola bitta xotira manziliga ishora qilayotganini aniqlang.

## Yechim (Rust kodi):
```rust
fn main() {
    let x = 42;
    let r1 = &x;
    let r2 = &x;
    let y = 42;
    let r3 = &y;

    println!("r1 va r2 bir xil manzilmi: {}", std::ptr::eq(r1, r2));
    println!("r1 va r3 bir xil manzilmi: {}", std::ptr::eq(r1, r3));
}
```

## Tushuntirish va Mantiq:
`std::ptr::eq` qiymatlarni emas, balki havolalarning xotiradagi fizik ko'rsatkich manzillarini solishtiradi.

## Ishlash natijasi:
```text
r1 va r2 bir xil manzilmi: true
r1 va r3 bir xil manzilmi: false
```

---

# 221-Topshiriq: Havolaning xotira hajmi: std::mem::size_of::<&T>()
## Topshiriq sharti:
Havolaning o'zi Stack da qancha joy egallashini ko'rsating.

## Yechim (Rust kodi):
```rust
fn main() {
    println!("&i32 hajmi: {} bayt", std::mem::size_of::<&i32>());
    println!("&String hajmi: {} bayt", std::mem::size_of::<&String>());
    println!("&[i32; 1000] hajmi: {} bayt", std::mem::size_of::<&[i32; 1000]>());
}
```

## Tushuntirish va Mantiq:
Rust da havolalar oddiy 64-bitli (yoki 32-bitli) mashina ko'rsatkichidir. Ular qaysi turga ishora qilishidan qat'i nazar, aynan 8 bayt (64-bit tizimda) joy egallaydi.

## Ishlash natijasi:
```text
&i32 hajmi: 8 bayt
&String hajmi: 8 bayt
&[i32; 1000] hajmi: 8 bayt
```

---

# 222-Topshiriq: Metodlarda &self: Obyektni o'qish uchun qarzga olish
## Topshiriq sharti:
`&self` metodining ishlash tamoyilini struktura misolida ko'rsating.

## Yechim (Rust kodi):
```rust
struct Doira {
    radius: f64,
}

impl Doira {
    fn yuza(&self) -> f64 {
        std::f64::consts::PI * self.radius * self.radius
    }
}

fn main() {
    let d = Doira { radius: 3.0 };
    println!("Doira yuzi: {:.2}", d.yuza());
    println!("Doira obyekti hali ham yaroqli, radiusi: {}", d.radius);
}
```

## Tushuntirish va Mantiq:
`&self` metodi chaqirilganda, struktura egasligi ko'chmaydi. Metod faqat o'qish huquqi bilan qarzga oladi.

## Ishlash natijasi:
```text
Doira yuzi: 28.27
Doira obyekti hali ham yaroqli, radiusi: 3
```

---

# 223-Topshiriq: Metodlarda &mut self: Obyektni o'zgartirish uchun qarzga olish
## Topshiriq sharti:
`&mut self` orqali obyekt holatini yangilovchi metod tuzing.

## Yechim (Rust kodi):
```rust
struct Spidometr {
    tezlik: u32,
}

impl Spidometr {
    fn tezlanish(&mut self, qoshimcha: u32) {
        self.tezlik += qoshimcha;
    }
}

fn main() {
    let mut s = Spidometr { tezlik: 60 };
    s.tezlanish(20);
    s.tezlanish(30);

    println!("Joriy tezlik: {} km/soat", s.tezlik);
}
```

## Tushuntirish va Mantiq:
`&mut self` metodi chaqiruvchidan o'zgaruvchan havolani oladi va metod ichida maydonlarni to'g'ridan-to'g'ri yangilash imkonini beradi.

## Ishlash natijasi:
```text
Joriy tezlik: 110 km/soat
```

---

# 224-Topshiriq: Reborrowing tushunchasi (&mut *ref)
## Topshiriq sharti:
Mavjud `&mut` havoladan yangi qisqa muddatli `&mut` havola hosil qilish.

## Yechim (Rust kodi):
```rust
fn yangila(son: &mut i32) {
    let ichki: &mut i32 = &mut *son; // Reborrow
    *ichki += 1;
}

fn main() {
    let mut x = 10;
    yangila(&mut x);
    println!("x = {}", x);
}
```

## Tushuntirish va Mantiq:
Reborrowing o'zgaruvchan havola egasligini yo'qotmasdan, uning ostidagi qiymatdan vaqtincha ikkinchi `&mut` qarz olish imkonini beradi.

## Ishlash natijasi:
```text
x = 11
```

---

# 225-Topshiriq: Bir vaqtda strukturaning turli maydonlarini qarzga olish (Disjoint Borrowing)
## Topshiriq sharti:
Strukturaning ikkita mustaqil maydonini alohida `&mut` qilib olish.

## Yechim (Rust kodi):
```rust
struct Nuqta {
    x: i32,
    y: i32,
}

fn main() {
    let mut p = Nuqta { x: 0, y: 0 };

    let ref_x = &mut p.x;
    *ref_x = 10;

    let ref_y = &mut p.y;
    *ref_y = 20;

    println!("Nuqta: ({}, {})", p.x, p.y);
}
```

## Tushuntirish va Mantiq:
Rust kompilyatori etarlicha aqlli: agar siz strukturaning turli maydonlariga (`p.x` va `p.y`) murojaat qilsangiz, ularni bir-biriga xalaqit bermaydigan mustaqil xotiralar deb biladi.

## Ishlash natijasi:
```text
Nuqta: (10, 20)
```

---

# 226-Topshiriq: split_at_mut orqali massivni 2 ta mustaqil &mut bo'lakka bo'lish
## Topshiriq sharti:
Bitta massivning ikki yarmini bir vaqtda xavfsiz o'zgartirish.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut sonlar = [1, 2, 3, 4, 5, 6];

    let (chap, ong) = sonlar.split_at_mut(3);

    chap[0] = 100;
    ong[0] = 900;

    println!("Bo'lingan massiv natijasi: {:?}", sonlar);
}
```

## Tushuntirish va Mantiq:
`split_at_mut` standart kutubxona metodi bo'lib, massivni ikkita alohida `&mut [T]` ga ajratadi. Bu parallel saralash va Merge Sort uchun poydevordir.

## Ishlash natijasi:
```text
Bo'lingan massiv natijasi: [100, 2, 3, 900, 5, 6]
```

---

# 227-Topshiriq: Massiv elementlarini 2 barobar oshiruvchi funksiya (&mut [i32])
## Topshiriq sharti:
Massiv bo'lagiga havola olib, har bir elementni o'z joyida ko'paytirish.

## Yechim (Rust kodi):
```rust
fn ikki_hissa_qil(arr: &mut [i32]) {
    for elem in arr.iter_mut() {
        *elem *= 2;
    }
}

fn main() {
    let mut sonlar = [10, 20, 30, 40];
    ikki_hissa_qil(&mut sonlar);

    println!("Ko'paytirilgan massiv: {:?}", sonlar);
}
```

## Tushuntirish va Mantiq:
`arr.iter_mut()` har bir element uchun `&mut i32` beradi va `*elem *= 2` orqali xotiradagi sonlar joyida yangilanadi.

## Ishlash natijasi:
```text
Ko'paytirilgan massiv: [20, 40, 60, 80]
```

---

# 228-Topshiriq: Eng katta elementni topib, unga havola qaytaruvchi funksiya
## Topshiriq sharti:
Vektordan eng katta qiymatning o'zini emas, uning havolasini qaytaring.

## Yechim (Rust kodi):
```rust
fn eng_kattasi(royxat: &[i32]) -> Option<&i32> {
    if royxat.is_empty() { return None; }
    let mut max = &royxat[0];
    for elem in royxat {
        if elem > max {
            max = elem;
        }
    }
    Some(max)
}

fn main() {
    let raqamlar = [12, 65, 34, 89, 23];
    if let Some(&max) = eng_kattasi(&raqamlar) {
        println!("Eng katta son: {}", max);
    }
}
```

## Tushuntirish va Mantiq:
Funksiyaning qaytarayotgan havolasi kiruvchi `royxat` ga bog'liq. Bu nol qo'shimcha xotira sarflaydi va nusxa olmaydi.

## Ishlash natijasi:
```text
Eng katta son: 89
```

---

# 229-Topshiriq: Ikki ko'rsatkichli algoritm: Ikki chetidan havola orqali teskari o'girish
## Topshiriq sharti:
Ko'rsatkichlar yaqinlashishi orqali massivni joyida almashtirish.

## Yechim (Rust kodi):
```rust
fn teskari_massiv(arr: &mut [i32]) {
    let mut chap = 0;
    let mut ong = arr.len() - 1;

    while chap < ong {
        arr.swap(chap, ong);
        chap += 1;
        ong -= 1;
    }
}

fn main() {
    let mut a = [1, 2, 3, 4, 5];
    teskari_massiv(&mut a);
    println!("Natija: {:?}", a);
}
```

## Tushuntirish va Mantiq:
`arr.swap()` metodidan foydalanib, indekslar orqali elementlar joyi xavfsiz almashtiriladi.

## Ishlash natijasi:
```text
Natija: [5, 4, 3, 2, 1]
```

---

# 230-Topshiriq: Matndagi birinchi so'zga &str havola qaytaruvchi funksiya
## Topshiriq sharti:
String nusxasini olmay, asl matn ichidagi so'z bo'lagini qarzga oling.

## Yechim (Rust kodi):
```rust
fn birinchi_soz(s: &str) -> &str {
    let baytlar = s.as_bytes();
    for (i, &belgi) in baytlar.iter().enumerate() {
        if belgi == b' ' {
            return &s[0..i];
        }
    }
    s
}

fn main() {
    let jumla = String::from("Rust tili mukammal");
    let soz = birinchi_soz(&jumla);

    println!("Birinchi so'z: '{}'", soz);
}
```

## Tushuntirish va Mantiq:
Ushbu funksiya `String` ning hech bir baytini nusxalamaydi, balki to'g'ridan-to'g'ri `jumla` ning xotirasiga ishora qiluvchi `&str` qaytaradi.

## Ishlash natijasi:
```text
Birinchi so'z: 'Rust'
```

---

# 231-Topshiriq: O'zgarmas havoladan .clone() chaqirish tamoyili
## Topshiriq sharti:
`&T` orqali to'liq yangi mustaqil nusxa yaratish.

## Yechim (Rust kodi):
```rust
fn nusxa_yarat(s: &String) -> String {
    s.clone() // s qarzga olingan, lekin uning to'liq nusxasi qaytariladi
}

fn main() {
    let original = String::from("Boshlang'ich");
    let nusxa = nusxa_yarat(&original);

    println!("Original: {}", original);
    println!("Nusxa:    {}", nusxa);
}
```

## Tushuntirish va Mantiq:
Havolaga ega bo'lish obyektni o'qish huquqini beradi. Agar obyekt `Clone` implement qilgan bo'lsa, havoladan yangi mustaqil egali nusxa olish mumkin.

## Ishlash natijasi:
```text
Original: Boshlang'ich
Nusxa:    Boshlang'ich
```

---

# 232-Topshiriq: Kortejlarda aralash havolalarni saqlash
## Topshiriq sharti:
Kortejda turli manbalardan olingan havolalarni birlashtirish.

## Yechim (Rust kodi):
```rust
fn main() {
    let ism = String::from("Nodir");
    let yosh = 30;

    let profil: (&String, &i32) = (&ism, &yosh);

    println!("Profil egasi: {}, Yoshi: {}", profil.0, profil.1);
}
```

## Tushuntirish va Mantiq:
Kortejlar havolalarni guruhlash uchun juda qulay. Har bir havola o'zining asl o'zgaruvchisiga ishora qilishda davom etadi.

## Ishlash natijasi:
```text
Profil egasi: Nodir, Yoshi: 30
```

---

# 233-Topshiriq: Shartli tarmoqlarda har xil o'zgaruvchidan havola tanlash
## Topshiriq sharti:
`if` ifodasi orqali ikkita sondan kattasining havolasini oling.

## Yechim (Rust kodi):
```rust
fn main() {
    let a = 15;
    let b = 25;

    let kattasi: &i32 = if a > b { &a } else { &b };

    println!("Kattasiga havola: {}", kattasi);
}
```

## Tushuntirish va Mantiq:
Ikkala havola ham bir xil doirada yashagani uchun, shart asosida tanlangan havola to'liq xavfsiz va yaroqlidir.

## Ishlash natijasi:
```text
Kattasiga havola: 25
```

---

# 234-Topshiriq: Havolalar massivi va ular bo'ylab iteratsiya
## Topshiriq sharti:
Bir nechta mustaqil satrlarning havolalaridan massiv tuzing.

## Yechim (Rust kodi):
```rust
fn main() {
    let s1 = String::from("Olma");
    let s2 = String::from("Anor");
    let s3 = String::from("Uzum");

    let havolalar = [&s1, &s2, &s3];

    for h in havolalar {
        println!("Meva: {}", h);
    }
}
```

## Tushuntirish va Mantiq:
Havolalar massivi orqali katta hajmdagi ma'lumotlarni nusxalamasdan, faqat ularning ko'rsatkichlarini tartiblash yoki filtrlash mumkin.

## Ishlash natijasi:
```text
Meva: Olma
Meva: Anor
Meva: Uzum
```

---

# 235-Topshiriq: Boshqa funksiya havolani o'zgartirishi oqibati
## Topshiriq sharti:
Funksiya orqali tashqi o'zgaruvchining qiymatini 10 ga oshiring.

## Yechim (Rust kodi):
```rust
fn oshir(val: &mut i32) {
    *val += 10;
}

fn main() {
    let mut raqam = 70;
    oshir(&mut raqam);
    oshir(&mut raqam);

    println!("Raqamning yakuniy holati: {}", raqam);
}
```

## Tushuntirish va Mantiq:
Parametr sifatida `&mut` uzatilganda, funksiyadagi barcha amallar to'g'ridan-to'g'ri asl xotira katagida o'z aksini topadi.

## Ishlash natijasi:
```text
Raqamning yakuniy holati: 90
```

---

# 236-Topshiriq: Palindrom tekshiruvi: Ikki tomondan havola orqali (Zero-copy)
## Topshiriq sharti:
Satr nusxasini olmay, baytlar havolasi orqali palindromlikni aniqlang.

## Yechim (Rust kodi):
```rust
fn palindrom_tekshir(s: &str) -> bool {
    let bayt = s.as_bytes();
    let mut i = 0;
    let mut j = bayt.len().saturating_sub(1);

    while i < j {
        if bayt[i] != bayt[j] {
            return false;
        }
        i += 1;
        j -= 1;
    }
    true
}

fn main() {
    println!("'kazak' palindrommi: {}", palindrom_tekshir("kazak"));
    println!("'dastur' palindrommi: {}", palindrom_tekshir("dastur"));
}
```

## Tushuntirish va Mantiq:
0 bayt qo'shimcha xotira sarflanadi. Barcha solishtirishlar bevosita asl matn xotirasida bajariladi.

## Ishlash natijasi:
```text
'kazak' palindrommi: true
'dastur' palindrommi: false
```

---

# 237-Topshiriq: Struktura ichida havolani o'zgartirish (Bank hisobi balansi)
## Topshiriq sharti:
Struktura metodida `&mut self` bilan tranzaksiya o'tkazing.

## Yechim (Rust kodi):
```rust
struct BankHisob {
    egasi: String,
    mablag: f64,
}

impl BankHisob {
    fn otkazma(&mut self, qoshimcha: f64) {
        self.mablag += qoshimcha;
        println!("{}: yangi balans = ${:.2}", self.egasi, self.mablag);
    }
}

fn main() {
    let mut hisob = BankHisob { egasi: String::from("Ali"), mablag: 120.0 };
    hisob.otkazma(80.5);
}
```

## Tushuntirish va Mantiq:
Metod `&mut self` orqali balansni joyida oshiradi va obyektning o'zini chaqiruvchida saqlab qoladi.

## Ishlash natijasi:
```text
Ali: yangi balans = $200.50
```

---

# 238-Topshiriq: Massiv bo'lagi (slice) ustida binar qidiruv havolalar bilan
## Topshiriq sharti:
Saralangan slice ga havola uzatib qidiruvni amalga oshiring.

## Yechim (Rust kodi):
```rust
fn binar_qidiruv<'a>(royxat: &'a [i32], nishon: i32) -> Option<usize> {
    let mut chap = 0;
    let mut ong = royxat.len();

    while chap < ong {
        let orta = chap + (ong - chap) / 2;
        if royxat[orta] == nishon {
            return Some(orta);
        } else if royxat[orta] < nishon {
            chap = orta + 1;
        } else {
            ong = orta;
        }
    }
    None
}

fn main() {
    let sonlar = [10, 20, 30, 40, 50, 60];
    let res = binar_qidiruv(&sonlar, 40);
    println!("40 soni indeksi: {:?}", res);
}
```

## Tushuntirish va Mantiq:
Massivga havola orqali binar qidiruv har qanday uzunlikdagi massivlar va vektorlar uchun universal ishlaydi.

## Ishlash natijasi:
```text
40 soni indeksi: Some(3)
```

---

# 239-Topshiriq: Borrow Checker ning xato xabarlarini tushunish
## Topshiriq sharti:
Borrow Checker xatolarining mantiqiy sababini tushuntiruvchi misol.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut raqam = 10;
    let r1 = &raqam;

    println!("r1 o'qimoqda: {}", r1);

    // r1 ishlatib bo'lingach, &mut olish mumkin
    let r2 = &mut raqam;
    *r2 = 20;

    println!("r2 o'zgartirdi: {}", r2);
}
```

## Tushuntirish va Mantiq:
Kompilyator xatosi dasturchiga qaysi qatorda birinchi havola olingani va qayerda to'qnashuv bo'lganini aniq ko'rsatadi.

## Ishlash natijasi:
```text
r1 o'qimoqda: 10
r2 o'zgartirdi: 20
```

---

# 240-Topshiriq: Havolalarning o'zaro o'rnini almashtirish: std::mem::swap
## Topshiriq sharti:
Ikkita `&mut` havola orqali ularning qiymatlarini bitta siklda almashtiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut a = String::from("Birinchi");
    let mut b = String::from("Ikkinchi");

    std::mem::swap(&mut a, &mut b);

    println!("a = {}", a);
    println!("b = {}", b);
}
```

## Tushuntirish va Mantiq:
`std::mem::swap` Move semantikasidan foydalanib, Heap xotirani nusxalamasdan, shunchaki xotira ko'rsatkichlarini almashtirib qo'yadi.

## Ishlash natijasi:
```text
a = Ikkinchi
b = Birinchi
```

---

# 241-Topshiriq: Vektor elementlarini filtrlashda havolalar (&T)
## Topshiriq sharti:
Vektor elementlarini o'zgartirmasdan, shartga moslarini tanlab olish.

## Yechim (Rust kodi):
```rust
fn main() {
    let sonlar = vec![5, 12, 8, 21, 3, 16];
    let mut kattalar = Vec::new();

    for son in &sonlar {
        if *son > 10 {
            kattalar.push(son); // &i32 havolalarni saqlaymiz
        }
    }

    print!("10 dan kattalar: ");
    for s in kattalar {
        print!("{} ", s);
    }
    println!();
}
```

## Tushuntirish va Mantiq:
Asl sonlar ko'chirilmaydi va klonlanmaydi. `kattalar` vektori shunchaki kerakli sonlarning havolalarini saqlaydi.

## Ishlash natijasi:
```text
10 dan kattalar: 12 21 16 
```

---

# 242-Topshiriq: String va &str o'rtasidagi borrowing munosabati
## Topshiriq sharti:
`&String` avtomatik ravishda `&str` ga o'tishini (Deref Coercion) ko'rsating.

## Yechim (Rust kodi):
```rust
fn chop_et(matn: &str) {
    println!("Chop etildi: {}", matn);
}

fn main() {
    let s = String::from("Salom Rust");
    chop_et(&s); // &String -> &str ga avtomatik o'tadi
    chop_et("Statik matn"); // &str to'g'ridan-to'g'ri o'tadi
}
```

## Tushuntirish va Mantiq:
Rust da funksiyalarga parametr sifatida `&String` emas, `&str` berish eng yaxshi amaliyot (best practice) hisoblanadi, chunki u ikkala turga ham mos keladi.

## Ishlash natijasi:
```text
Chop etildi: Salom Rust
Chop etildi: Statik matn
```

---

# 243-Topshiriq: Read-Write qulflari (RWLock) tamoyili borrowing da
## Topshiriq sharti:
Borrowing tizimi apparat darajasidagi o'qish/yozish qulfi bilan bir xil ekanligini ko'rsating.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut ma'lumot = 100;

    // Ko'p o'quvchilar:
    {
        let oquvchi1 = &ma'lumot;
        let oquvchi2 = &ma'lumot;
        println!("O'quvchilar: {} va {}", oquvchi1, oquvchi2);
    } // O'qish qulfi bo'shadi

    // Yagona yozuvchi:
    {
        let yozuvchi = &mut ma'lumot;
        *yozuvchi += 50;
        println!("Yozuvchi: {}", yozuvchi);
    } // Yozish qulfi bo'shadi
}
```

## Tushuntirish va Mantiq:
Rust ning borrow checker i parallel dasturlashdagi Read-Write Lock mexanizmini to'g'ridan-to'g'ri bitta oqimli kodda ham kompilyatsiya paytida kafolatlaydi.

## Ishlash natijasi:
```text
O'quvchilar: 100 va 100
Yozuvchi: 150
```

---

# 244-Topshiriq: Massivning faqat bir qismini &mut qilib uzatish
## Topshiriq sharti:
Funksiyaga butun massivni emas, uning oraliq bo'lagini uzating.

## Yechim (Rust kodi):
```rust
fn tozalash(qism: &mut [i32]) {
    for elem in qism {
        *elem = 0;
    }
}

fn main() {
    let mut massiv = [1, 2, 3, 4, 5, 6];
    tozalash(&mut massiv[2..5]); // 3, 4, 5 elementlar nollanadi

    println!("Natija: {:?}", massiv);
}
```

## Tushuntirish va Mantiq:
Slice `&mut [2..5]` faqat kerakli indekslar diapazoniga xavfsiz o'zgaruvchan havola beradi.

## Ishlash natijasi:
```text
Natija: [1, 2, 0, 0, 0, 6]
```

---

# 245-Topshiriq: Katta matn tahlilida havolalardan foydalanish
## Topshiriq sharti:
Matn ichidagi harflar sonini faqat havolalar orqali sanash.

## Yechim (Rust kodi):
```rust
fn probellarni_sana(matn: &str) -> usize {
    matn.chars().filter(|&c| c == ' ').count()
}

fn main() {
    let jumla = "Rust tizimli dasturlash uchun eng zo'r til";
    let probellar = probellarni_sana(jumla);

    println!("Probellar soni: {}", probellar);
}
```

## Tushuntirish va Mantiq:
Katta matnlar bilan ishlaganda har doim `&str` uzatiladi, bu hech qanday xotira ko'chirish yoki nusxalashsiz tahlil qilish imkonini beradi.

## Ishlash natijasi:
```text
Probellar soni: 6
```

---

# 246-Topshiriq: O'zgaruvchan havolani boshqa o'zgaruvchan havolaga almashtirish
## Topshiriq sharti:
`&mut` ko'rsatkichining o'zini boshqa manzilga qaratish.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut x = 10;
    let mut y = 20;

    let mut ko'rsatkich = &mut x;
    *ko'rsatkich += 5;

    ko'rsatkich = &mut y; // Endi y ga qaratildi
    *ko'rsatkich += 15;

    println!("x = {}, y = {}", x, y);
}
```

## Tushuntirish va Mantiq:
`let mut ko'rsatkich: &mut T` o'zgaruvchining o'zi ham o'zgaruvchan bo'lib, uning qaysi katakka ishora qilishini o'zgartirish mumkin.

## Ishlash natijasi:
```text
x = 15, y = 35
```

---

# 247-Topshiriq: Havolalarning ko'p oqimli xavfsizlikka ta'siri (Sync traiti)
## Topshiriq sharti:
`&T` ko'p oqimga bemalol berilishi mumkinligining nazariy asosi.

## Yechim (Rust kodi):
```rust
fn main() {
    let son = 42;
    let havola = &son;

    println!("Havola xavfsiz o'qiladi: {}", havola);
    println!("Agar tur Sync bo'lsa, uning &T havolasini oqimlararo uzatish mumkin.");
}
```

## Tushuntirish va Mantiq:
Rust da agar tur `Sync` bo'lsa, uning o'zgarmas havolasi (`&T`) xotira poygasisiz (Data race siz) barcha oqimlar bo'ylab erkin tarqatilishi mumkin.

## Ishlash natijasi:
```text
Havola xavfsiz o'qiladi: 42
Agar tur Sync bo'lsa, uning &T havolasini oqimlararo uzatish mumkin.
```

---

# 248-Topshiriq: Struktura ichida qarz olingan ma'lumotni aks ettirish
## Topshiriq sharti:
Strukturadan `&str` maydonini qaytaruvchi getter metodi.

## Yechim (Rust kodi):
```rust
struct Xodim {
    ism: String,
}

impl Xodim {
    fn ismni_ol(&self) -> &str {
        &self.ism
    }
}

fn main() {
    let x = Xodim { ism: String::from("Rustam") };
    let ism_ref = x.ismni_ol();

    println!("Xodim ismi: {}", ism_ref);
}
```

## Tushuntirish va Mantiq:
Getter metodlari `&self` qabul qilib, o'z ichki maydonlarining havolalarini qaytaradi. Bu ma'lumotlarni o'g'irlamasdan yoki nusxalamasdan taqdim etish usulidir.

## Ishlash natijasi:
```text
Xodim ismi: Rustam
```

---

# 249-Topshiriq: Borrowing va xotira sizib ketishining (Memory Leak) mutlaq yo'qligi
## Topshiriq sharti:
Qarz olingan obyekt hech qachon xotirani o'zi bilan olib ketolmasligini ko'rsating.

## Yechim (Rust kodi):
```rust
fn main() {
    {
        let asl = String::from("Vaqtinchalik xotira");
        let _havola = &asl;
        println!("Havola faol.");
    } // Bu yerda 'asl' ham, 'havola' ham o'ldi, xotira 100% tozalandi!

    println!("Xotira to'liq bo'shatildi.");
}
```

## Tushuntirish va Mantiq:
Havola egalik qilmaydi, demak u xotiraning yopilishiga ham xalaqit bermaydi. Egasi o'lgan zahoti xotira har doim tozalanadi.

## Ishlash natijasi:
```text
Havola faol.
Xotira to'liq bo'shatildi.
```

---

# 250-Topshiriq: Borrowing moduli xulosasi: Rust super-kuchining poydevori
## Topshiriq sharti:
Egalik (Ownership) va Qarz olish (Borrowing) qoidalari sintezi.

## Yechim (Rust kodi):
```rust
fn main() {
    println!("=== RUST BORROWING TIZIMI QOIDALARI ===");
    println!("1. Har bir qiymat bitta egaga ega.");
    println!("2. Istalgancha &T (o'zgarmas havola) olish mumkin.");
    println!("3. Yoki faqat bitta &mut T (o'zgaruvchan havola) olish mumkin.");
    println!("4. Havolalar har doim o'z manbasidan ko'proq yashay olmaydi (Dangling pointer yo'q).");
    println!("5. Barcha tekshiruvlar 0 nanosoniya sarf bilan kompilyatsiyada bajariladi!");
}
```

## Tushuntirish va Mantiq:
Ushbu qoidalar Rust ni dunyodagi eng xavfsiz va eng ishonchli tizimli dasturlash tiliga aylantirgan fundamental ustundir.

## Ishlash natijasi:
```text
=== RUST BORROWING TIZIMI QOIDALARI ===
1. Har bir qiymat bitta egaga ega.
2. Istalgancha &T (o'zgarmas havola) olish mumkin.
3. Yoki faqat bitta &mut T (o'zgaruvchan havola) olish mumkin.
4. Havolalar har doim o'z manbasidan ko'proq yashay olmaydi (Dangling pointer yo'q).
5. Barcha tekshiruvlar 0 nanosoniya sarf bilan kompilyatsiyada bajariladi!
```

---
