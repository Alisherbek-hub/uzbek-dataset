# 8-Qism: Enums (Sanovchilar) va Quvvatli Pattern Matching (351-400)

Ushbu qismda Rust ning eng kuchli ifodalash vositalaridan biri bo'lgan **Algebraic Data Types (Algebraik ma'lumot turlari - Enums)**, ma'lumot tashiydigan variantlar, `Option<T>` enumi, nima uchun Rust da `null` yo'qligi, to'liq Pattern Matching (`match`, match guards, `@` binding, `if let`, `while let`, `let else`, `matches!`), Holat Mashinalari (State Machines) va Null Pointer Optimization (Niche filling) o'rganiladi.

---

# 351-Topshiriq: Enum (Sanovchi tur) nima? Asosiy tushuncha
## Topshiriq sharti:
Dunyo tomonlarini ifodalovchi sodda enum e'lon qiling va undan foydalaning.

## Yechim (Rust kodi):
```rust
#[derive(Debug)]
enum Yonalish {
    Shimol,
    Janub,
    Sharq,
    Garb,
}

fn main() {
    let harakat = Yonalish::Shimol;
    println!("Tanlangan yo'nalish: {:?}", harakat);
}
```

## Tushuntirish va Mantiq:
Enum (enumeration) mumkin bo'lgan barcha qiymatlar to'plamini sanab o'tish imkonini beradi. Har qanday vaqtda o'zgaruvchi faqat bitta variantga teng bo'ladi.

## Ishlash natijasi:
```text
Tanlangan yo'nalish: Shimol
```

---

# 352-Topshiriq: Enum variantlarini match orqali qayta ishlash
## Topshiriq sharti:
Har bir yo'nalish uchun mos xabarni match yordamida ekranga chiqaring.

## Yechim (Rust kodi):
```rust
enum Yonalish {
    Shimol, Janub, Sharq, Garb,
}

fn kompas(y: Yonalish) {
    match y {
        Yonalish::Shimol => println!("Oldinga to'g'ri yuring"),
        Yonalish::Janub  => println!("Orqaga buriling"),
        Yonalish::Sharq  => println!("O'ng tomonga buriling"),
        Yonalish::Garb   => println!("Chap tomonga buriling"),
    }
}

fn main() {
    kompas(Yonalish::Sharq);
}
```

## Tushuntirish va Mantiq:
`match` enumlar bilan ishlashning eng mukammal vositasidir. U har bir variantni alohida tarmoqda ko'rib chiqishni ta'minlaydi.

## Ishlash natijasi:
```text
O'ng tomonga buriling
```

---

# 353-Topshiriq: Ma'lumot tashiydigan enumlar (Tuple variantlari)
## Topshiriq sharti:
Variantlari ichida ma'lumot saqlovchi boy enum yarating.

## Yechim (Rust kodi):
```rust
#[derive(Debug)]
enum IPManzil {
    V4(u8, u8, u8, u8),
    V6(String),
}

fn main() {
    let uy = IPManzil::V4(127, 0, 0, 1);
    let server = IPManzil::V6(String::from("::1"));

    println!("Lokal IP: {:?}", uy);
    println!("Server IP: {:?}", server);
}
```

## Tushuntirish va Mantiq:
Boshqa ko'plab tillardan farqli ravishda, Rust enum variantlari ichida har xil turlardagi ma'lumotlarni saqlashi mumkin.

## Ishlash natijasi:
```text
Lokal IP: V4(127, 0, 0, 1)
Server IP: V6("::1")
```

---

# 354-Topshiriq: Strukturasimon variantli enumlar (Struct Variants)
## Topshiriq sharti:
Maydonlari nomlangan variantlarga ega enum tuzing.

## Yechim (Rust kodi):
```rust
#[derive(Debug)]
enum Xabar {
    Chiqish,
    Matn(String),
    Rang(u8, u8, u8),
    Kochirish { x: i32, y: i32 },
}

fn main() {
    let m = Xabar::Kochirish { x: 10, y: 25 };
    println!("Xabar obyekti: {:?}", m);
}
```

## Tushuntirish va Mantiq:
Enum variantlari ham nomsiz tuple, ham nomlangan struktura shaklida bo'lishi mumkin. Bu polimorfizmni merosxo'rliksiz hal qiladi.

## Ishlash natijasi:
```text
Xabar obyekti: Kochirish { x: 10, y: 25 }
```

---

# 355-Topshiriq: Enum variantlarini ochish (Pattern Destructuring)
## Topshiriq sharti:
`match` ichida enum variantidagi ichki qiymatlarni ajratib oling.

## Yechim (Rust kodi):
```rust
enum Xabar {
    Matn(String),
    Kochirish { x: i32, y: i32 },
}

fn qayta_ishla(x: Xabar) {
    match x {
        Xabar::Matn(s) => println!("Matnli xabar: {}", s),
        Xabar::Kochirish { x, y } => println!("Koordinata o'zgardi: ({}, {})", x, y),
    }
}

fn main() {
    qayta_ishla(Xabar::Matn(String::from("Assalomu alaykum")));
    qayta_ishla(Xabar::Kochirish { x: 50, y: 100 });
}
```

## Tushuntirish va Mantiq:
`match` ichki qiymatlarni osonlik bilan o'zgaruvchilarga bog'lab oladi va ulardan foydalanish imkonini beradi.

## Ishlash natijasi:
```text
Matnli xabar: Assalomu alaykum
Koordinata o'zgardi: (50, 100)
```

---

# 356-Topshiriq: Standart kutubxonadagi Option<T> enumi
## Topshiriq sharti:
Mavjud bo'lishi yoki bo'lmasligi mumkin bo'lgan qiymatni `Some` va `None` orqali ifodalang.

## Yechim (Rust kodi):
```rust
fn kvadrat_ildiz(x: f64) -> Option<f64> {
    if x >= 0.0 {
        Some(x.sqrt())
    } else {
        None // Manfiy sonning haqiqiy ildizi yo'q
    }
}

fn main() {
    println!("16 ning ildizi: {:?}", kvadrat_ildiz(16.0));
    println!("-4 ning ildizi: {:?}", kvadrat_ildiz(-4.0));
}
```

## Tushuntirish va Mantiq:
`Option<T>` standart enum bo'lib, ikkita variantga ega: `Some(T)` (qiymat bor) va `None` (qiymat yo'q).

## Ishlash natijasi:
```text
16 ning ildizi: Some(4.0)
-4 ning ildizi: None
```

---

# 357-Topshiriq: Nega Rust da null / nil yo'q? (Milliard dollarlik xato)
## Topshiriq sharti:
Kompilyator `Option` ni ochishni qat'iy talab qilishi orqali crash ning oldini oling.

## Yechim (Rust kodi):
```rust
fn main() {
    let ism: Option<&str> = Some("Alisher");

    // Rust da to'g'ridan-to'g'ri ism.len() deb bo'lmaydi!
    // Avval uning ichida qiymat borligini tekshirish shart:
    match ism {
        Some(val) => println!("Ism uzunligi: {}", val.len()),
        None => println!("Ism mavjud emas!"),
    }
}
```

## Tushuntirish va Mantiq:
Toni Xoar 'null' ni o'zining 'milliard dollarlik xatosi' deb atagan. Rust da `null` yo'q, hamma ixtiyoriy qiymatlar `Option` bilan o'raladi va null pointer crash lari 0% ga tushiriladi.

## Ishlash natijasi:
```text
Ism uzunligi: 7
```

---

# 358-Topshiriq: Enumlar uchun impl metodlari yozish
## Topshiriq sharti:
Enum ichida o'zining xatti-harakatlarini belgilovchi metodlar tuzing.

## Yechim (Rust kodi):
```rust
enum Svetofor {
    Qizil, Sariq, Yashil,
}

impl Svetofor {
    fn vaqt_sekund(&self) -> u32 {
        match self {
            Svetofor::Qizil  => 60,
            Svetofor::Sariq => 5,
            Svetofor::Yashil => 45,
        }
    }
}

fn main() {
    let chiroq = Svetofor::Qizil;
    println!("Kutish vaqti: {} sekund", chiroq.vaqt_sekund());
}
```

## Tushuntirish va Mantiq:
Xuddi strukturalar kabi enumlar ham o'zining `impl` blokiga va metodlariga ega bo'lishi mumkin.

## Ishlash natijasi:
```text
Kutish vaqti: 60 sekund
```

---

# 359-Topshiriq: C-uslubidagi enumlar va raqamli diskriminantlar
## Topshiriq sharti:
HTTP status kodlarini raqamlar bilan belgilang va `as u16` orqali son qilib oling.

## Yechim (Rust kodi):
```rust
enum HttpStatus {
    Ok = 200,
    NotFound = 404,
    InternalError = 500,
}

fn main() {
    let kod = HttpStatus::NotFound;
    println!("Status raqami: {}", kod as u16);
}
```

## Tushuntirish va Mantiq:
Enum variantlariga butun sonlar biriktirilsa, ular C tili bilan to'liq mos keladi va `as` operatori orqali songa o'tkaziladi.

## Ishlash natijasi:
```text
Status raqami: 404
```

---

# 360-Topshiriq: Match to'liqligi (Exhaustiveness) va xavfsizlik
## Topshiriq sharti:
Kompilyator barcha variantlarni ko'rib chiqishni talab qilishi.

## Yechim (Rust kodi):
```rust
enum Holat { Boshlandi, DavomEtmoqda, Yakunlandi }

fn tekshir(h: Holat) {
    match h {
        Holat::Boshlandi => println!("Jarayon start oldi"),
        Holat::DavomEtmoqda => println!("Ish ketmoqda"),
        Holat::Yakunlandi => println!("Muvaffaqiyatli tugadi"),
    }
}

fn main() {
    tekshir(Holat::Yakunlandi);
}
```

## Tushuntirish va Mantiq:
Agar siz enumga kelajakda yangi variant qo'shsangiz, kompilyator uni barcha `match` bloklarida qo'shishni talab qiladi va hech qanday unutilgan holat qolmaydi.

## Ishlash natijasi:
```text
Muvaffaqiyatli tugadi
```

---

# 361-Topshiriq: Wildcard (_) yordamida qolgan holatlarni e'tiborsiz qoldirish
## Topshiriq sharti:
Faqat bitta variantni qoldirib, qolganlariga universal javob bering.

## Yechim (Rust kodi):
```rust
enum Rol { Admin, Moderator, Foydalanuvchi, Mehmon }

fn huquq(r: Rol) {
    match r {
        Rol::Admin => println!("To'liq tizim boshqaruvi"),
        _ => println!("Cheklangan foydalanuvchi huquqi"),
    }
}

fn main() {
    huquq(Rol::Foydalanuvchi);
}
```

## Tushuntirish va Mantiq:
`_` barcha boshqa ko'rsatilmagan variantlarni bitta blokda ushlab qoladi.

## Ishlash natijasi:
```text
Cheklangan foydalanuvchi huquqi
```

---

# 362-Topshiriq: Match Guardlar enumlar bilan
## Topshiriq sharti:
Enum variantidagi qiymat ustiga qo'shimcha shartlar yuklang.

## Yechim (Rust kodi):
```rust
enum Harorat {
    Selsiy(i32),
}

fn main() {
    let h = Harorat::Selsiy(35);

    match h {
        Harorat::Selsiy(t) if t > 30 => println!("Issiq ob-havo: {}°C", t),
        Harorat::Selsiy(t) if t < 0  => println!("Ayozli havo: {}°C", t),
        Harorat::Selsiy(t) => println!("Normal harorat: {}°C", t),
    }
}
```

## Tushuntirish va Mantiq:
Match guard `if` sharti variant ochilgandan keyin uning ichidagi qiymatni qo'shimcha filtrlash imkonini beradi.

## Ishlash natijasi:
```text
Issiq ob-havo: 35°C
```

---

# 363-Topshiriq: @ bog'lash operatori (Binding Operator) enumlar bilan
## Topshiriq sharti:
Oraliqni tekshirgan holda ichki qiymatni yangi nomga o'zlashtiring.

## Yechim (Rust kodi):
```rust
enum Xabar {
    Kod(u32),
}

fn main() {
    let x = Xabar::Kod(25);

    match x {
        Xabar::Kod(val @ 1..=50) => println!("1 dan 50 gacha oraliqda: {}", val),
        Xabar::Kod(boshqa) => println!("Boshqa kod: {}", boshqa),
    }
}
```

## Tushuntirish va Mantiq:
`val @ oraliq` orqali ham qiymatning oraliqqa mosligi tekshiriladi, ham o'sha son `val` nomli o'zgaruvchida saqlanadi.

## Ishlash natijasi:
```text
1 dan 50 gacha oraliqda: 25
```

---

# 364-Topshiriq: if let sintaksisi: Bitta variantni qisqa tekshirish
## Topshiriq sharti:
Faqat `Some` bo'lganda ishlovchi ixcham blok.

## Yechim (Rust kodi):
```rust
fn main() {
    let konfiguratsiya: Option<&str> = Some("dark_mode");

    if let Some(rejim) = konfiguratsiya {
        println!("Interfeys rejimi: {}", rejim);
    }
}
```

## Tushuntirish va Mantiq:
`if let` bitta holat uchun to'liq `match` yozish yukidan xalos qiladi.

## Ishlash natijasi:
```text
Interfeys rejimi: dark_mode
```

---

# 365-Topshiriq: if let ... else kombinatsiyasi
## Topshiriq sharti:
`None` holatini `else` orqali boshqaring.

## Yechim (Rust kodi):
```rust
fn main() {
    let xabar: Option<i32> = None;

    if let Some(son) = xabar {
        println!("Qabul qilindi: {}", son);
    } else {
        println!("Hech qanday xabar kelmadi.");
    }
}
```

## Tushuntirish va Mantiq:
`if let ... else` varianti mos kelmaganda muqobil ishni bajarishga xizmat qiladi.

## Ishlash natijasi:
```text
Hech qanday xabar kelmadi.
```

---

# 366-Topshiriq: while let sintaksisi: Variant mos kelguncha tsiklni yurgizish
## Topshiriq sharti:
Vektordan elementlarni `pop()` orqali tugaguncha o'qish.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut to'plam = vec![10, 20, 30];

    while let Some(son) = to'plam.pop() {
        println!("Sug'urildi: {}", son);
    }
}
```

## Tushuntirish va Mantiq:
`while let` har safar yangi variantni tekshiradi va u `None` bo'lishi bilan tsikl to'xtaydi.

## Ishlash natijasi:
```text
Sug'urildi: 30
Sug'urildi: 20
Sug'urildi: 10
```

---

# 367-Topshiriq: let else konstruksiyasi (Rust 2021/2024)
## Topshiriq sharti:
Agar variant `Some` bo'lmasa, darhol return qilish.

## Yechim (Rust kodi):
```rust
fn kvadrat(opt: Option<i32>) {
    let Some(val) = opt else {
        println!("Qiymat yo'q!");
        return;
    };
    println!("Kvadrat: {}", val * val);
}

fn main() {
    kvadrat(None);
    kvadrat(Some(6));
}
```

## Tushuntirish va Mantiq:
`let Some(x) = opt else { return; };` kodi o'zgaruvchini darhol tashqi darajaga chiqaradi va kodning o'qilishini yaxshilaydi.

## Ishlash natijasi:
```text
Qiymat yo'q!
Kvadrat: 36
```

---

# 368-Topshiriq: matches! makrosi orqali qisqa mantiqiy tekshiruv
## Topshiriq sharti:
Variantning ma'lum shartga to'g'ri kelishini `bool` qiymat sifatida olish.

## Yechim (Rust kodi):
```rust
enum TizimHolati {
    Faol,
    Kutish,
    Xato(u32),
}

fn main() {
    let holat = TizimHolati::Xato(500);

    let xatomi = matches!(holat, TizimHolati::Xato(_));
    println!("Tizimda xato bormi: {}", xatomi);
}
```

## Tushuntirish va Mantiq:
`matches!(qiymat, pattern)` berilgan ifoda pattern ga mos kelsa `true`, aks holda `false` qaytaradi.

## Ishlash natijasi:
```text
Tizimda xato bormi: true
```

---

# 369-Topshiriq: Holat Mashinasi (State Machine): Buyurtma hayot sikli
## Topshiriq sharti:
Buyurtma bosqichlarini enumlar orqali xavfsiz boshqaring.

## Yechim (Rust kodi):
```rust
enum BuyurtmaHolati {
    Yangi,
    TolovQilindi(f64),
    Yetkazilmoqda,
    Yakunlandi,
}

fn main() {
    let holat = BuyurtmaHolati::TolovQilindi(150.0);

    match holat {
        BuyurtmaHolati::Yangi => println!("Buyurtma qabul qilindi."),
        BuyurtmaHolati::TolovQilindi(summa) => println!("${} to'landi, omborga uzatildi.", summa),
        BuyurtmaHolati::Yetkazilmoqda => println!("Kuryer yo'lda."),
        BuyurtmaHolati::Yakunlandi => println!("Xarid muvaffaqiyatli yakunlandi."),
    }
}
```

## Tushuntirish va Mantiq:
Enumlar orqali qurilgan holat mashinasi mantiqsiz o'tishlar va kutilmagan holatlarni butunlay bartaraf etadi.

## Ishlash natijasi:
```text
$150 to'landi, omborga uzatildi.
```

---

# 370-Topshiriq: Domen modeli: HTTP So'rov turlari
## Topshiriq sharti:
GET, POST, PUT, DELETE so'rovlarini ma'lumotlari bilan modellashtiring.

## Yechim (Rust kodi):
```rust
enum HttpSorovi {
    Get { url: String },
    Post { url: String, payload: String },
    Delete { url: String, id: u64 },
}

fn bajar(sorov: HttpSorovi) {
    match sorov {
        HttpSorovi::Get { url } => println!("GET so'rovi: {}", url),
        HttpSorovi::Post { url, payload } => println!("POST {} ma'lumot: {}", url, payload),
        HttpSorovi::Delete { url, id } => println!("DELETE {} #{}", url, id),
    }
}

fn main() {
    bajar(HttpSorovi::Get { url: String::from("/api/users") });
    bajar(HttpSorovi::Post { url: String::from("/api/login"), payload: String::from("{"user":"ali"}") });
}
```

## Tushuntirish va Mantiq:
API dizaynida har xil so'rov parametrlarini bitta enumga birlashtirish routing tizimini o'ta soddalashtiradi.

## Ishlash natijasi:
```text
GET so'rovi: /api/users
POST /api/login ma'lumot: {"user":"ali"}
```

---

# 371-Topshiriq: Domen modeli: JSON Qiymatlar Daraxti (AST)
## Topshiriq sharti:
Har qanday JSON ma'lumotini o'zida saqlay oluvchi rekursiv enum tuzing.

## Yechim (Rust kodi):
```rust
#[derive(Debug)]
enum JsonQiymat {
    Null,
    Bool(bool),
    Son(f64),
    Satr(String),
    Massiv(Vec<JsonQiymat>),
}

fn main() {
    let talaba_json = JsonQiymat::Massiv(vec![
        JsonQiymat::Satr(String::from("Jasur")),
        JsonQiymat::Son(21.0),
        JsonQiymat::Bool(true),
    ]);

    println!("JSON Daraxti: {:?}", talaba_json);
}
```

## Tushuntirish va Mantiq:
`serde_json` kutubxonasi aynan shunday `Value` enumi orqali ixtiyoriy JSON formatlarini pars qiladi.

## Ishlash natijasi:
```text
JSON Daraxti: Massiv([Satr("Jasur"), Son(21.0), Bool(true)])
```

---

# 372-Topshiriq: Domen modeli: To'lov tizimlari polimorfizmi
## Topshiriq sharti:
Har xil to'lov vositalarini enum variantlarida saqlang.

## Yechim (Rust kodi):
```rust
enum TolovUsuli {
    Naqd,
    PlastikKarta { karta_raqam: String, amal_qilish: String },
    KriptoHamyon { manzil: String },
}

fn tolov_qil(usul: TolovUsuli, summa: f64) {
    match usul {
        TolovUsuli::Naqd => println!("Naqd ${:.2} qabul qilindi.", summa),
        TolovUsuli::PlastikKarta { karta_raqam, .. } => println!("Karta {} orqali ${:.2} yechildi.", karta_raqam, summa),
        TolovUsuli::KriptoHamyon { manzil } => println!("{} hamyoniga ${:.2} o'tkazildi.", manzil, summa),
    }
}

fn main() {
    tolov_qil(TolovUsuli::Naqd, 50.0);
    tolov_qil(TolovUsuli::PlastikKarta { karta_raqam: String::from("8600****1234"), amal_qilish: String::from("12/28") }, 120.0);
}
```

## Tushuntirish va Mantiq:
Enumlar orqali turli parametrlarga ega to'lov turlarini merosxo'rliksiz bitta toza funksiyada boshqarish mumkin.

## Ishlash natijasi:
```text
Naqd $50.00 qabul qilindi.
Karta 8600****1234 orqali $120.00 yechildi.
```

---

# 373-Topshiriq: Geometrik shakllar va ularning yuzasini match orqali hisoblash
## Topshiriq sharti:
Doira, To'rtburchak va Uchburchak shakllarini hisoblang.

## Yechim (Rust kodi):
```rust
enum Shakl {
    Doira(f64),
    Tortburchak(f64, f64),
    Kvadrat(f64),
}

impl Shakl {
    fn yuza(&self) -> f64 {
        match self {
            Shakl::Doira(r) => std::f64::consts::PI * r * r,
            Shakl::Tortburchak(w, h) => w * h,
            Shakl::Kvadrat(a) => a * a,
        }
    }
}

fn main() {
    let sh = Shakl::Tortburchak(5.0, 4.0);
    println!("Yuza: {:.2}", sh.yuza());
}
```

## Tushuntirish va Mantiq:
Klassik OOP da bu vazifa abstrakt sinflar va polimorfizm bilan qilinsa, Rust da bitta ixcham enum va match bilan hal etiladi.

## Ishlash natijasi:
```text
Yuza: 20.00
```

---

# 374-Topshiriq: Option::unwrap_or() orqali zaxira qiymat berish
## Topshiriq sharti:
Qiymat `None` bo'lganda standart zaxira parametrini qo'llang.

## Yechim (Rust kodi):
```rust
fn main() {
    let sozlama: Option<&str> = None;
    let til = sozlama.unwrap_or("uzbek");

    println!("Amaldagi til: {}", til);
}
```

## Tushuntirish va Mantiq:
`unwrap_or(default)` qiymat bo'lsa uni oladi, yo'q bo'lsa ko'rsatilgan zaxira qiymatni qaytaradi.

## Ishlash natijasi:
```text
Amaldagi til: uzbek
```

---

# 375-Topshiriq: Option::map() orqali ichki qiymat ustida amal bajarish
## Topshiriq sharti:
`Some` ichidagi qiymatni ochmasdan turib unga funksiya qo'llang.

## Yechim (Rust kodi):
```rust
fn main() {
    let narx: Option<i32> = Some(100);
    let soliq_bilan = narx.map(|n| n + 12);

    println!("Soliq bilan yakuniy narx: {:?}", soliq_bilan);
}
```

## Tushuntirish va Mantiq:
`map()` agar qiymat `Some` bo'lsa closureni qo'llaydi, agar `None` bo'lsa o'zgarishsiz `None` qoldiradi.

## Ishlash natijasi:
```text
Soliq bilan yakuniy narx: Some(112)
```

---

# 376-Topshiriq: Option::and_then() orqali ketma-ket amallarni zanjirlash
## Topshiriq sharti:
Har bir qadami `Option` qaytaruvchi funksiyalarni bitta oqimga ulang.

## Yechim (Rust kodi):
```rust
fn foydalanuvchi_id(ism: &str) -> Option<u32> {
    if ism == "Ali" { Some(42) } else { None }
}

fn balansni_ol(id: u32) -> Option<f64> {
    if id == 42 { Some(1500.50) } else { None }
}

fn main() {
    let balans = Some("Ali")
        .and_then(foydalanuvchi_id)
        .and_then(balansni_ol);

    println!("Ali balansi: {:?}", balans);
}
```

## Tushuntirish va Mantiq:
`and_then()` (flat_map) har qanday qadamda `None` chiqsa darhol zanjirni to'xtatadi va xatoliksiz natija beradi.

## Ishlash natijasi:
```text
Ali balansi: Some(1500.5)
```

---

# 377-Topshiriq: Option::filter() orqali ichki qiymatni saralash
## Topshiriq sharti:
Shartga to'g'ri kelmasa `None` ga aylantiruvchi metod.

## Yechim (Rust kodi):
```rust
fn main() {
    let yosh: Option<u32> = Some(21);
    let voyaga_yetgan = yosh.filter(|&y| y >= 18);

    println!("Tekshiruv natijasi: {:?}", voyaga_yetgan);
}
```

## Tushuntirish va Mantiq:
`filter()` ichidagi shart `true` bo'lsa `Some` ni saqlaydi, aks holda `None` qaytaradi.

## Ishlash natijasi:
```text
Tekshiruv natijasi: Some(21)
```

---

# 378-Topshiriq: Rekursiv Enumlar va Box: Arifmetik ifodalar daraxti
## Topshiriq sharti:
Qo'shish, ko'paytirish va sonlarni daraxtsimon ifodalovchi enum.

## Yechim (Rust kodi):
```rust
enum Ifoda {
    Son(i32),
    Qoshish(Box<Ifoda>, Box<Ifoda>),
    Kopaytirish(Box<Ifoda>, Box<Ifoda>),
}

fn hisobla(i: &Ifoda) -> i32 {
    match i {
        Ifoda::Son(n) => *n,
        Ifoda::Qoshish(chap, ong) => hisobla(chap) + hisobla(ong),
        Ifoda::Kopaytirish(chap, ong) => hisobla(chap) * hisobla(ong),
    }
}

fn main() {
    // (5 + 3) * 2 = 16
    let daraxt = Ifoda::Kopaytirish(
        Box::new(Ifoda::Qoshish(Box::new(Ifoda::Son(5)), Box::new(Ifoda::Son(3)))),
        Box::new(Ifoda::Son(2)),
    );

    println!("Hisoblangan ifoda natijasi: {}", hisobla(&daraxt));
}
```

## Tushuntirish va Mantiq:
Kompilyator rekursiv enumlar o'lchamini bilishi uchun `Box` dan foydalanish shart. Bu kompilyatorlar va kalkulyatorlar yaratishning asosiy tamoyilidir.

## Ishlash natijasi:
```text
Hisoblangan ifoda natijasi: 16
```

---

# 379-Topshiriq: Niche Optimization (Null Pointer Optimization)
## Topshiriq sharti:
`Option<&T>` yoki `Option<Box<T>>` ning oddiy ko'rsatkich kabi 8 bayt joy olishini ko'rsating.

## Yechim (Rust kodi):
```rust
fn main() {
    println!("&i32 o'lchami:         {} bayt", std::mem::size_of::<&i32>());
    println!("Option<&i32> o'lchami:   {} bayt", std::mem::size_of::<Option<&i32>>());
    println!("Option<Box<i32>> o'lchami: {} bayt", std::mem::size_of::<Option<Box<i32>>>());
}
```

## Tushuntirish va Mantiq:
Rust da havolalar hech qachon 0x0 (null) bo'la olmasligi sababli, kompilyator `None` ni aynan 0x0 manziliga joylashtiradi. Natijada `Option<&T>` xotirada 0 bayt qo'shimcha sarf talab qiladi!

## Ishlash natijasi:
```text
&i32 o'lchami:         8 bayt
Option<&i32> o'lchami:   8 bayt
Option<Box<i32>> o'lchami: 8 bayt
```

---

# 380-Topshiriq: Enum variantlarini vektor ichida saqlash va tahlil qilish
## Topshiriq sharti:
Har xil buyruqlar ro'yxatini ketma-ket bajarish.

## Yechim (Rust kodi):
```rust
enum Buyruq {
    Chop(String),
    Kutish(u32),
    Toxtat,
}

fn main() {
    let buyruqlar = vec![
        Buyruq::Chop(String::from("Tizim yuklanmoqda...")),
        Buyruq::Kutish(500),
        Buyruq::Toxtat,
    ];

    for b in buyruqlar {
        match b {
            Buyruq::Chop(matn) => println!("Chop: {}", matn),
            Buyruq::Kutish(ms) => println!("Kutish: {} ms", ms),
            Buyruq::Toxtat     => println!("Tizim to'xtatildi."),
        }
    }
}
```

## Tushuntirish va Mantiq:
Enumlar orqali skript buyruqlari, tranzaksiyalar va animatsiya ketma-ketliklari juda tartibli amalga oshiriladi.

## Ishlash natijasi:
```text
Chop: Tizim yuklanmoqda...
Kutish: 500 ms
Tizim to'xtatildi.
```

---

# 381-Topshiriq: Enum variantlarida kortejlar va maydonlar aralashmasi
## Topshiriq sharti:
Ko'p parametrli xabarlarni bitta enumda birlashtirish.

## Yechim (Rust kodi):
```rust
enum Log {
    Oddiy(&'static str),
    Ogohlantirish { kod: u32, xabar: String },
}

fn main() {
    let l1 = Log::Oddiy("Server ishga tushdi.");
    let l2 = Log::Ogohlantirish { kod: 101, xabar: String::from("Disk to'lmoqda") };

    match l1 {
        Log::Oddiy(m) => println!("INFO: {}", m),
        _ => (),
    }
    match l2 {
        Log::Ogohlantirish { kod, xabar } => println!("WARN [{}]: {}", kod, xabar),
        _ => (),
    }
}
```

## Tushuntirish va Mantiq:
Rust dasturchiga o'z ma'lumotlariga eng mos keladigan variant sintaksisini erkin tanlash imkonini beradi.

## Ishlash natijasi:
```text
INFO: Server ishga tushdi.
WARN [101]: Disk to'lmoqda
```

---

# 382-Topshiriq: C-enum ni butun sondan qayta yasash (TryFrom traiti)
## Topshiriq sharti:
Son kelganda uni xavfsiz holda enum variantiga aylantirish.

## Yechim (Rust kodi):
```rust
#[derive(Debug, PartialEq)]
enum Rang { Qizil = 1, Yashil = 2, Kok = 3 }

impl Rang {
    fn sondan(son: u8) -> Option<Self> {
        match son {
            1 => Some(Rang::Qizil),
            2 => Some(Rang::Yashil),
            3 => Some(Rang::Kok),
            _ => None,
        }
    }
}

fn main() {
    println!("2 soni rangi: {:?}", Rang::sondan(2));
    println!("9 soni rangi: {:?}", Rang::sondan(9));
}
```

## Tushuntirish va Mantiq:
Tashqi manbalardan (fayl, tarmoq) olingan sonlarni enumga aylantirishda tekshiruv har doim `Option` qaytarishi shart.

## Ishlash natijasi:
```text
2 soni rangi: Some(Yashil)
9 soni rangi: None
```

---

# 383-Topshiriq: Nested Pattern Matching: Enum ichida enum ochish
## Topshiriq sharti:
Ichma-ich enumlarni bitta chiroyli pattern bilan oching.

## Yechim (Rust kodi):
```rust
enum Tizim { Linux, Windows }
enum Dastur { WebServer(Tizim), Mobil }

fn main() {
    let app = Dastur::WebServer(Tizim::Linux);

    match app {
        Dastur::WebServer(Tizim::Linux) => println!("Linux dagi Web Server!"),
        Dastur::WebServer(Tizim::Windows) => println!("Windows dagi Web Server!"),
        Dastur::Mobil => println!("Mobil ilova"),
    }
}
```

## Tushuntirish va Mantiq:
Pattern Matching har qanday chuqurlikdagi ichma-ich tuzilmalarni bitta qatorda tekshirishga qodir.

## Ishlash natijasi:
```text
Linux dagi Web Server!
```

---

# 384-Topshiriq: Option unwrap_or_else() orqali hisoblanuvchi muqobil qiymat
## Topshiriq sharti:
Zaxira qiymat og'ir hisob-kitob talab qilganda 'lazy' yondashuvni qo'llang.

## Yechim (Rust kodi):
```rust
fn qimmat_hisob() -> i32 {
    println!("(Og'ir hisob-kitob bajarildi)");
    42
}

fn main() {
    let bor: Option<i32> = Some(100);
    let natija1 = bor.unwrap_or_else(qimmat_hisob);
    println!("Natija 1: {}", natija1);

    let yoq: Option<i32> = None;
    let natija2 = yoq.unwrap_or_else(qimmat_hisob);
    println!("Natija 2: {}", natija2);
}
```

## Tushuntirish va Mantiq:
`unwrap_or_else` faqat qiymat `None` bo'lgandagina closureni ishga tushiradi, bu esa resurslarni tejaydi.

## Ishlash natijasi:
```text
Natija 1: 100
(Og'ir hisob-kitob bajarildi)
Natija 2: 42
```

---

# 385-Topshiriq: Option::zip() orqali ikkita Option ni birlashtirish
## Topshiriq sharti:
Ikkala qiymat ham mavjud bo'lgandagina juftlik `(A, B)` hosil qilish.

## Yechim (Rust kodi):
```rust
fn main() {
    let ism = Some("Dilshod");
    let yosh = Some(26);

    let birlashgan = ism.zip(yosh);
    println!("Birlashgan ma'lumot: {:?}", birlashgan);

    let xato = ism.zip(None::<i32>);
    println!("Biri None bo'lsa: {:?}", xato);
}
```

## Tushuntirish va Mantiq:
`.zip()` metodi agar ikkala `Option` ham `Some` bo'lsa `Some((a, b))`, bittasi ham `None` bo'lsa `None` beradi.

## Ishlash natijasi:
```text
Birlashgan ma'lumot: Some(("Dilshod", 26))
Biri None bo'lsa: None
```

---

# 386-Topshiriq: Option::cloned() va copied() metodlari
## Topshiriq sharti:
`Option<&T>` havolasidan `Option<T>` qiymatiga xavfsiz o'tish.

## Yechim (Rust kodi):
```rust
fn main() {
    let son = 42;
    let opt_ref: Option<&i32> = Some(&son);
    let opt_val: Option<i32> = opt_ref.copied();

    println!("Nusxalangan qiymat: {:?}", opt_val);
}
```

## Tushuntirish va Mantiq:
`.copied()` primitiv turlar uchun avtomatik nusxalashni ta'minlaydi va havolalarni yechadi.

## Ishlash natijasi:
```text
Nusxalangan qiymat: Some(42)
```

---

# 387-Topshiriq: Enumlarda Default traiti va #[default] atributi
## Topshiriq sharti:
Enumning qaysi varianti standart bo'lishini `#[default]` bilan belgilang.

## Yechim (Rust kodi):
```rust
#[derive(Debug, Default, PartialEq)]
enum Rejim {
    #[default]
    Kutish,
    Ishlamoqda,
    Xato,
}

fn main() {
    let r = Rejim::default();
    println!("Standart rejim: {:?}", r);
}
```

## Tushuntirish va Mantiq:
Rust 1.62+ dan boshlab enumlarga `#[derive(Default)]` va variant ustiga `#[default]` qo'yish rasmiy standartga aylandi.

## Ishlash natijasi:
```text
Standart rejim: Kutish
```

---

# 388-Topshiriq: Matematik polimorfizm: 1-Bit kvantlangan qiymat enumi
## Topshiriq sharti:
1-bit AI tarmoqlari uchun ternar {-1, 0, +1} qiymatlarini enum bilan modellashtiring.

## Yechim (Rust kodi):
```rust
#[derive(Debug, Clone, Copy, PartialEq)]
enum TernarOgirlik {
    Manfiy, // -1
    Nol,    // 0
    Musbat, // +1
}

impl TernarOgirlik {
    fn songa(&self) -> i32 {
        match self {
            TernarOgirlik::Manfiy => -1,
            TernarOgirlik::Nol    => 0,
            TernarOgirlik::Musbat => 1,
        }
    }
}

fn main() {
    let w = TernarOgirlik::Manfiy;
    println!("Ternar qiymat: {:?}, Butun son: {}", w, w.songa());
}
```

## Tushuntirish va Mantiq:
Ternar va 1-bit AI dvigatellarida og'irliklarni enum orqali xavfsiz ifodalash mumkin.

## Ishlash natijasi:
```text
Ternar qiymat: Manfiy, Butun son: -1
```

---

# 389-Topshiriq: Domen modeli: Tarmoq xabari protokoli
## Topshiriq sharti:
Ping, Pong va Ma'lumot uzatish protokoli enumi.

## Yechim (Rust kodi):
```rust
enum Protokol {
    Ping,
    Pong,
    Malumot { id: u64, matn: String },
}

fn qayta_ishla(p: &Protokol) {
    match p {
        Protokol::Ping => println!("Pong javobi qaytarildi!"),
        Protokol::Pong => println!("Tizim tirik."),
        Protokol::Malumot { id, matn } => println!("[#{}] {}", id, matn),
    }
}

fn main() {
    qayta_ishla(&Protokol::Ping);
    qayta_ishla(&Protokol::Malumot { id: 101, matn: String::from("Salom Rust") });
}
```

## Tushuntirish va Mantiq:
Tarmoq protokollari enumlar orqali xatoliksiz va juda ixcham amalga oshiriladi.

## Ishlash natijasi:
```text
Pong javobi qaytarildi!
[#101] Salom Rust
```

---

# 390-Topshiriq: Enum variantlarini solishtirish: #[derive(PartialEq, Eq)]
## Topshiriq sharti:
Enum nusxalarining tengligini tekshirish.

## Yechim (Rust kodi):
```rust
#[derive(PartialEq, Debug)]
enum Rang { Qizil, Yashil }

fn main() {
    let r1 = Rang::Qizil;
    let r2 = Rang::Qizil;
    let r3 = Rang::Yashil;

    println!("r1 == r2: {}", r1 == r2);
    println!("r1 == r3: {}", r1 == r3);
}
```

## Tushuntirish va Mantiq:
`PartialEq` enum variantlari va ularning ichki qiymatlarini to'liq solishtirish imkonini beradi.

## Ishlash natijasi:
```text
r1 == r2: true
r1 == r3: false
```

---

# 391-Topshiriq: Enum bilan Foydalanuvchi buyrug'i CLI parseri
## Topshiriq sharti:
Terminal buyruqlarini (Yordam, Chiqish, Saqlash) parse qiluvchi enum.

## Yechim (Rust kodi):
```rust
enum CliBuyruq {
    Yordam,
    Chiqish,
    Ochish(String),
}

impl CliBuyruq {
    fn parse(kiruvchi: &str) -> Option<Self> {
        let qismlar: Vec<&str> = kiruvchi.split_whitespace().collect();
        match qismlar.as_slice() {
            ["yordam"] => Some(CliBuyruq::Yordam),
            ["chiqish"] => Some(CliBuyruq::Chiqish),
            ["ochish", fayl] => Some(CliBuyruq::Ochish(fayl.to_string())),
            _ => None,
        }
    }
}

fn main() {
    let cmd = CliBuyruq::parse("ochish test.txt");
    match cmd {
        Some(CliBuyruq::Ochish(f)) => println!("Fayl ochilmoqda: {}", f),
        _ => println!("Boshqa buyruq"),
    }
}
```

## Tushuntirish va Mantiq:
Slice pattern matching bilan enum kombinatsiyasi mukammal CLI dasturlar yaratishga asos bo'ladi.

## Ishlash natijasi:
```text
Fayl ochilmoqda: test.txt
```

---

# 392-Topshiriq: Option::ok_or() orqali Option dan Result ga o'tish
## Topshiriq sharti:
`None` uchraganda ma'lum bir xato xabari hosil qiling.

## Yechim (Rust kodi):
```rust
fn main() {
    let topildi: Option<i32> = None;
    let res: Result<i32, &str> = topildi.ok_or("Ma'lumot topilmadi!");

    println!("Natija: {:?}", res);
}
```

## Tushuntirish va Mantiq:
`ok_or(err)` metodi `Some(v)` ni `Ok(v)` ga, `None` ni esa ko'rsatilgan `Err(err)` ga aylantiradi.

## Ishlash natijasi:
```text
Natija: Err("Ma'lumot topilmadi!")
```

---

# 393-Topshiriq: Option::transpose() orqali Option<Result> ni Result<Option> ga aylantirish
## Topshiriq sharti:
Ichma-ich o'ralgan turlarning o'rnini almashtirish.

## Yechim (Rust kodi):
```rust
fn main() {
    let x: Option<Result<i32, &str>> = Some(Ok(42));
    let y: Result<Option<i32>, &str> = x.transpose();

    println!("Transposed: {:?}", y);
}
```

## Tushuntirish va Mantiq:
`transpose()` kombinatori ichma-ich turlarni inversiya qilib, `?` operatori bilan ishlashni osonlashtiradi.

## Ishlash natijasi:
```text
Transposed: Ok(Some(42))
```

---

# 394-Topshiriq: Domen modeli: Fayl tizimi nodelari (Fayl yoki Papka)
## Topshiriq sharti:
Fayllar va ichki elementli papkalarni bitta daraxtda saqlang.

## Yechim (Rust kodi):
```rust
enum Tugun {
    Fayl { nom: String, hajm: u64 },
    Papka { nom: String, ichidagilar: Vec<Tugun> },
}

fn jami_hajm(t: &Tugun) -> u64 {
    match t {
        Tugun::Fayl { hajm, .. } => *hajm,
        Tugun::Papka { ichidagilar, .. } => ichidagilar.iter().map(jami_hajm).sum(),
    }
}

fn main() {
    let root = Tugun::Papka {
        nom: String::from("root"),
        ichidagilar: vec![
            Tugun::Fayl { nom: String::from("a.txt"), hajm: 100 },
            Tugun::Fayl { nom: String::from("b.txt"), hajm: 200 },
        ],
    };

    println!("Papka umumiy hajmi: {} bayt", jami_hajm(&root));
}
```

## Tushuntirish va Mantiq:
Fayl tizimlari rekursiv enumlar orqali juda tabiiy va xavfsiz tarzda hisoblanadi.

## Ishlash natijasi:
```text
Papka umumiy hajmi: 300 bayt
```

---

# 395-Topshiriq: Enum variantlarini match qilishda bir nechta qiymatni birlashtirish (|)
## Topshiriq sharti:
Bir nechta variantda bir xil mantiqni bajarish.

## Yechim (Rust kodi):
```rust
enum HarfTuri { Unli, Undosh, Maxsus }

fn bahola(t: HarfTuri) {
    match t {
        HarfTuri::Unli | HarfTuri::Undosh => println!("Bu oddiy nutq tovushi"),
        HarfTuri::Maxsus => println!("Bu maxsus belgi"),
    }
}

fn main() {
    bahola(HarfTuri::Unli);
}
```

## Tushuntirish va Mantiq:
`|` belgisi bir nechta enum variantlariga bitta kod blokini biriktirish imkonini beradi.

## Ishlash natijasi:
```text
Bu oddiy nutq tovushi
```

---

# 396-Topshiriq: Option unwrap_or_default() metodi
## Topshiriq sharti:
`None` bo'lganda turning `Default::default()` qiymatini olish.

## Yechim (Rust kodi):
```rust
fn main() {
    let son: Option<i32> = None;
    let satr: Option<String> = None;

    println!("Son default: {}", son.unwrap_or_default());
    println!("Satr default: '{}'", satr.unwrap_or_default());
}
```

## Tushuntirish va Mantiq:
`unwrap_or_default()` turning standart qiymatini avtomatik chaqiradi.

## Ishlash natijasi:
```text
Son default: 0
Satr default: ''
```

---

# 397-Topshiriq: Enum ichida strukturalarni to'g'ridan-to'g'ri saqlash
## Topshiriq sharti:
Alohida e'lon qilingan strukturalarni enum variantlarida birlashtirish.

## Yechim (Rust kodi):
```rust
struct Video { davomiyligi: u32 }
struct Rasm { kenglik: u32, balandlik: u32 }

enum Media {
    V(Video),
    R(Rasm),
}

fn main() {
    let m = Media::R(Rasm { kenglik: 1920, balandlik: 1080 });
    match m {
        Media::V(v) => println!("Video: {} soniya", v.davomiyligi),
        Media::R(r) => println!("Rasm: {}x{}", r.kenglik, r.balandlik),
    }
}
```

## Tushuntirish va Mantiq:
Mavjud mustaqil strukturalarni umumiy polimorfik interfeysga keltirishning eng toza yo'lidir.

## Ishlash natijasi:
```text
Rasm: 1920x1080
```

---

# 398-Topshiriq: Option::flatten() orqali ikki qavatli Option ni tekislash
## Topshiriq sharti:
`Option<Option<T>>` ni `Option<T>` ga aylantiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let ichma_ich: Option<Option<i32>> = Some(Some(42));
    let tekis = ichma_ich.flatten();

    println!("Tekislangan qiymat: {:?}", tekis);

    let bosh: Option<Option<i32>> = Some(None);
    println!("Bosh tekislash: {:?}", bosh.flatten());
}
```

## Tushuntirish va Mantiq:
`.flatten()` qavatma-qavat bo'lib ketgan ixtiyoriy qiymatlarni bitta darajaga tushiradi.

## Ishlash natijasi:
```text
Tekislangan qiymat: Some(42)
Bosh tekislash: None
```

---

# 399-Topshiriq: Option qiymatlarini solishtirish qoidalari
## Topshiriq sharti:
`Some(10) > Some(5)` va `Some(x) > None` munosabatini ko'rsating.

## Yechim (Rust kodi):
```rust
fn main() {
    let a = Some(10);
    let b = Some(5);
    let c: Option<i32> = None;

    println!("Some(10) > Some(5): {}", a > b);
    println!("Some(5) > None:     {}", b > c);
}
```

## Tushuntirish va Mantiq:
Rust da `Option` `Ord` traitini implement qilgan bo'lib, har doim `None < Some(...)` deb baholanadi.

## Ishlash natijasi:
```text
Some(10) > Some(5): true
Some(5) > None:     true
```

---

# 400-Topshiriq: Enums va Pattern Matching moduli xulosasi
## Topshiriq sharti:
Algebraik ma'lumot turlarining tizimli afzalliklari.

## Yechim (Rust kodi):
```rust
fn main() {
    println!("=== RUST ENUMS VA PATTERN MATCHING XULOSASI ===");
    println!("1. Enumlar ma'lumot tashiydi (Tuple va Struct variantlari).");
    println!("2. Rust da Null yo'q, o'rnida Option<T> qo'llaniladi.");
    println!("3. Match to'liq (exhaustive) bo'lishi shart, bu xatolarni kompilyatsiyada yo'qotadi.");
    println!("4. Niche Optimization tufayli Option ko'rsatkichlari xotirada 0 bayt ortiqcha sarfga ega.");
    println!("5. if let, while let, let else va matches! kodni ixcham va xavfsiz qiladi.");
}
```

## Tushuntirish va Mantiq:
Enums va Pattern Matching kombinatsiyasi Rust tilini ma'lumotlarni modellashtirish bo'yicha dunyodagi eng qudratli tillardan biriga aylantirgan.

## Ishlash natijasi:
```text
=== RUST ENUMS VA PATTERN MATCHING XULOSASI ===
1. Enumlar ma'lumot tashiydi (Tuple va Struct variantlari).
2. Rust da Null yo'q, o'rnida Option<T> qo'llaniladi.
3. Match to'liq (exhaustive) bo'lishi shart, bu xatolarni kompilyatsiyada yo'qotadi.
4. Niche Optimization tufayli Option ko'rsatkichlari xotirada 0 bayt ortiqcha sarfga ega.
5. if let, while let, let else va matches! kodni ixcham va xavfsiz qiladi.
```

---
