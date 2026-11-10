# 11-Qism: Traits (Belgilar / Interfeyslar) va Dinamik Dispatch (501-550)

Ushbu qismda Rust dasturlash tilidagi umumiy xatti-harakatlarni birlashtiruvchi **Traits (Interfeyslar)**, traitlarni strukturalarga implement qilish, standart metodlar, Trait Bounds, `impl Trait`, Trait Objects va Dinamik Dispatch (`dyn Trait`), Vtable arxitekturasi, Standart traitlar (`Display`, `Debug`, `Clone`, `Copy`, `Default`, `PartialEq`, `Ord`), Operatorlarni qayta yuklash (`std::ops`), Assotsiatsiyalangan turlar (`Associated Types`), Supertraits hamda Orphan Rule qoidalari o'rganiladi.

---

# 501-Topshiriq: Trait nima? Xatti-harakat shartnomasi (Contract of Behavior)
## Topshiriq sharti:
Ob'ektlar qanday metodlarga ega bo'lishi kerakligini belgilovchi sodda trait e'lon qiling.

## Yechim (Rust kodi):
```rust
trait Salomlashuvchi {
    fn salom(&self) -> String;
}

struct Odam { ism: String }
struct Bot { versiya: u32 }

impl Salomlashuvchi for Odam {
    fn salom(&self) -> String { format!("Assalomu alaykum, men {}!", self.ism) }
}

impl Salomlashuvchi for Bot {
    fn salom(&self) -> String { format!("Bip-bup! Bot v{} ishga tushdi.", self.versiya) }
}

fn main() {
    let o = Odam { ism: String::from("Rustam") };
    let b = Bot { versiya: 2 };

    println!("{}", o.salom());
    println!("{}", b.salom());
}
```

## Tushuntirish va Mantiq:
Trait boshqa tillardagi `interface` ga o'xshaydi. U strukturalar qanday metodlarni bajarishi shartligini qat'iy belgilaydi.

## Ishlash natijasi:
```text
Assalomu alaykum, men Rustam!
Bip-bup! Bot v2 ishga tushdi.
```

---

# 502-Topshiriq: Standart metod implementatsiyasi (Default Method Implementation)
## Topshiriq sharti:
Trait ichida umumiy metodni oldindan yozib qo'ying.

## Yechim (Rust kodi):
```rust
trait Tavsif {
    fn sarlavha(&self) -> String;

    // Standart metod
    fn toliq_tavsif(&self) -> String {
        format!("(Standart tavsif: {})", self.sarlavha())
    }
}

struct Maqola { sarlavha_matni: String }

impl Tavsif for Maqola {
    fn sarlavha(&self) -> String { self.sarlavha_matni.clone() }
}

fn main() {
    let m = Maqola { sarlavha_matni: String::from("Rust da Traitlar") };
    println!("{}", m.toliq_tavsif());
}
```

## Tushuntirish va Mantiq:
Trait da metodning standart tanasi yozib qo'yilsa, struktura uni qayta yozishi shart emas, lekin xohlasa qayta yoza oladi (override).

## Ishlash natijasi:
```text
(Standart tavsif: Rust da Traitlar)
```

---

# 503-Topshiriq: Standart metodni qayta yozish (Overriding default methods)
## Topshiriq sharti:
Struktura uchun standart metodni o'ziga xos tarzda yangilang.

## Yechim (Rust kodi):
```rust
trait Signal {
    fn xabar(&self) -> &'static str { "Standart signal" }
}

struct MaxsusSignal;
impl Signal for MaxsusSignal {
    fn xabar(&self) -> &'static str { "Kritik maxsus signal!" }
}

fn main() {
    let s = MaxsusSignal;
    println!("{}", s.xabar());
}
```

## Tushuntirish va Mantiq:
Struktura trait ning standart metodini o'z kodi bilan to'liq almashtira oladi.

## Ishlash natijasi:
```text
Kritik maxsus signal!
```

---

# 504-Topshiriq: Trait Bounds: Generik parametrlarga shart qo'yish
## Topshiriq sharti:
Faqat ma'lum bir traitga ega turlarni qabul qiluvchi generik funksiya yozing.

## Yechim (Rust kodi):
```rust
trait ChopEtiluvchi {
    fn matn(&self) -> String;
}

struct Kitob { nom: String }
impl ChopEtiluvchi for Kitob {
    fn matn(&self) -> String { format!("Kitob: {}", self.nom) }
}

fn axborot_ber<T: ChopEtiluvchi>(obyekt: &T) {
    println!("{}", obyekt.matn());
}

fn main() {
    let k = Kitob { nom: String::from("Rust Qollanma") };
    axborot_ber(&k);
}
```

## Tushuntirish va Mantiq:
`<T: ChopEtiluvchi>` sharti faqat ushbu traitni implement qilgan turlar qabul qilinishini kompilyatsiyada tekshiradi.

## Ishlash natijasi:
```text
Kitob: Rust Qollanma
```

---

# 505-Topshiriq: impl Trait parametr sintaksisi
## Topshiriq sharti:
Trait Bound ni sodda `impl Trait` ko'rinishida yozing.

## Yechim (Rust kodi):
```rust
trait Ovoz {
    fn tovush(&self) -> &'static str;
}

struct Kuchuk;
impl Ovoz for Kuchuk { fn tovush(&self) -> &'static str { "Vov-vov!" } }

fn eshit(jonivor: &impl Ovoz) {
    println!("Tovush: {}", jonivor.tovush());
}

fn main() {
    eshit(&Kuchuk);
}
```

## Tushuntirish va Mantiq:
`item: &impl Trait` sintaksisi generik trait bound larning sintaktik shakaridir (syntactic sugar) va kodni juda toza qiladi.

## Ishlash natijasi:
```text
Tovush: Vov-vov!
```

---

# 506-Topshiriq: Bir nechta Trait Boundlar (+ operatori)
## Topshiriq sharti:
Parametr bir vaqtda ikkita traitga ega bo'lishini talab qiling.

## Yechim (Rust kodi):
```rust
use std::fmt::Display;

fn namoyish<T: Display + Clone>(val: &T) {
    let nusxa = val.clone();
    println!("Qiymat: {}", nusxa);
}

fn main() {
    let matn = String::from("Rust Ekosistema");
    namoyish(&matn);
}
```

## Tushuntirish va Mantiq:
`T: Trait1 + Trait2` bir nechta interfeys talablarini bitta parametrda birlashtiradi.

## Ishlash natijasi:
```text
Qiymat: Rust Ekosistema
```

---

# 507-Topshiriq: where klauzulasi orqali toza trait shartlari
## Topshiriq sharti:
Ko'p parametrli funksiyalarda shartlarni funksiya tanasidan oldin tartiblang.

## Yechim (Rust kodi):
```rust
use std::fmt::Display;

fn solishtir_va_chop<T, U>(a: T, b: U)
where
    T: Display + PartialEq,
    U: Display,
{
    println!("a = {}, b = {}", a, b);
}

fn main() {
    solishtir_va_chop(100, "Ball");
}
```

## Tushuntirish va Mantiq:
`where` klauzulasi funksiya signaturasining o'qilishini keskin yaxshilaydi.

## Ishlash natijasi:
```text
a = 100, b = Ball
```

---

# 508-Topshiriq: impl Trait qaytish qiymati sifatida
## Topshiriq sharti:
Aniq ichki turni yashirib, faqat uning traitini qaytaring.

## Yechim (Rust kodi):
```rust
trait Chizuvchi {
    fn chiz(&self);
}

struct Doira;
impl Chizuvchi for Doira {
    fn chiz(&self) { println!("Doira chizildi O"); }
}

fn shakl_yarat() -> impl Chizuvchi {
    Doira
}

fn main() {
    let s = shakl_yarat();
    s.chiz();
}
```

## Tushuntirish va Mantiq:
`-> impl Trait` yordamida funksiya ichki aniq strukturani yashirib, mijozga faqat interfeys beradi.

## Ishlash natijasi:
```text
Doira chizildi O
```

---

# 509-Topshiriq: Trait Objects va Dinamik Dispatch (&dyn Trait, Box<dyn Trait>)
## Topshiriq sharti:
Har xil strukturalarni bitta umumiy ro'yxatda saqlang.

## Yechim (Rust kodi):
```rust
trait Shakl {
    fn chiz(&self);
}

struct Kvadrat;
impl Shakl for Kvadrat { fn chiz(&self) { println!("[Kvadrat]"); } }

struct Doira;
impl Shakl for Doira { fn chiz(&self) { println!("(Doira)"); } }

fn main() {
    let shakllar: Vec<Box<dyn Shakl>> = vec![
        Box::new(Kvadrat),
        Box::new(Doira),
    ];

    for s in shakllar {
        s.chiz();
    }
}
```

## Tushuntirish va Mantiq:
`dyn Trait` dinamik polimorfizm (vtable orqali dispatch) ta'minlaydi. Turli strukturalar bitta vektor ichida erkin saqlanadi.

## Ishlash natijasi:
```text
[Kvadrat]
(Doira)
```

---

# 510-Topshiriq: Statik Dispatch (Monomorfizatsiya) vs Dinamik Dispatch (Vtable)
## Topshiriq sharti:
Ikkala usulning farqini namoyish etuvchi solishtirma dastur.

## Yechim (Rust kodi):
```rust
trait Salmoqli { fn vazn(&self) -> u32; }
struct Yuk(u32);
impl Salmoqli for Yuk { fn vazn(&self) -> u32 { self.0 } }

// Statik dispatch: kompilyatsiyada har bir tur uchun alohida kod generatsiya bo'ladi (tezroq)
fn statik_olchov<T: Salmoqli>(y: &T) { println!("Statik: {}", y.vazn()); }

// Dinamik dispatch: ish vaqtida fat pointer (vtable) orqali chaqiriladi
fn dinamik_olchov(y: &dyn Salmoqli) { println!("Dinamik: {}", y.vazn()); }

fn main() {
    let yuk = Yuk(500);
    statik_olchov(&yuk);
    dinamik_olchov(&yuk);
}
```

## Tushuntirish va Mantiq:
Statik dispatch maksimal tezlik beradi, dinamik dispatch esa xotirada turlarni aralash saqlash imkoniyatini yaratadi.

## Ishlash natijasi:
```text
Statik: 500
Dinamik: 500
```

---

# 511-Topshiriq: Standart Trait: Display (Inson tushunadigan formatlash)
## Topshiriq sharti:
Strukturangizni `println!("{}")` bilan chiroyli chiqaring.

## Yechim (Rust kodi):
```rust
use std::fmt;

struct Koordinata { kenglik: f64, uzunlik: f64 }

impl fmt::Display for Koordinata {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{:.2}° N, {:.2}° E", self.kenglik, self.uzunlik)
    }
}

fn main() {
    let k = Koordinata { kenglik: 41.29, uzunlik: 69.24 };
    println!("Toshkent: {}", k);
}
```

## Tushuntirish va Mantiq:
`Display` traiti foydalanuvchiga mo'ljallangan matnli ifodani shakllantirish uchun standart vositadir.

## Ishlash natijasi:
```text
Toshkent: 41.29° N, 69.24° E
```

---

# 512-Topshiriq: Standart Trait: Debug (Dasturchi uchun to'liq tahlil)
## Topshiriq sharti:
Qo'lda `Debug` traitini formatlab yozish.

## Yechim (Rust kodi):
```rust
use std::fmt;

struct SirliKod { kod: u32 }

impl fmt::Debug for SirliKod {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "SirliKod(***{})", self.kod % 100)
    }
}

fn main() {
    let s = SirliKod { kod: 9876 };
    println!("{:?}", s);
}
```

## Tushuntirish va Mantiq:
`Debug` ni qo'lda implement qilish orqali maxfiy ma'lumotlarni loglarda yashirish mumkin.

## Ishlash natijasi:
```text
SirliKod(***76)
```

---

# 513-Topshiriq: Standart Trait: Clone vs Copy
## Topshiriq sharti:
`Clone` chuqur nusxalashni, `Copy` esa oddiy bayt ko'chirishni talab qilishini ko'rsating.

## Yechim (Rust kodi):
```rust
#[derive(Debug, Clone, Copy)]
struct Nuqta { x: i32, y: i32 }

fn main() {
    let p1 = Nuqta { x: 10, y: 20 };
    let p2 = p1; // Copy bo'ldi

    println!("p1 = {:?}, p2 = {:?}", p1, p2);
}
```

## Tushuntirish va Mantiq:
`Copy` faqat xotirada to'liq Stack da yashaydigan oddiy turlar uchun mumkin bo'lib, avtomatik nusxalanadi.

## Ishlash natijasi:
```text
p1 = Nuqta { x: 10, y: 20 }, p2 = Nuqta { x: 10, y: 20 }
```

---

# 514-Topshiriq: Standart Trait: PartialEq va Eq (Tenglikni solishtirish)
## Topshiriq sharti:
Strukturalar uchun `==` operatorini qo'lda implement qiling.

## Yechim (Rust kodi):
```rust
struct Talaba {
    id: u32,
    ism: String,
}

impl PartialEq for Talaba {
    fn eq(&self, boshqa: &Self) -> bool {
        self.id == boshqa.id // Faqat ID si bir xil bo'lsa teng deb hisoblaymiz!
    }
}

fn main() {
    let t1 = Talaba { id: 101, ism: String::from("Ali") };
    let t2 = Talaba { id: 101, ism: String::from("Alisher") };

    println!("Talabalar tengmi: {}", t1 == t2);
}
```

## Tushuntirish va Mantiq:
Qo'lda `PartialEq` yozish orqali biznes mantiqqa mos tenglik qoidalarini (masalan, faqat unikal ID bo'yicha) belgilash mumkin.

## Ishlash natijasi:
```text
Talabalar tengmi: true
```

---

# 515-Topshiriq: Standart Trait: PartialOrd va Ord (Tartiblash va solishtirish)
## Topshiriq sharti:
Strukturalar uchun `>`, `<` operatorlarini maydon bo'yicha belgilang.

## Yechim (Rust kodi):
```rust
use std::cmp::Ordering;

#[derive(Eq, PartialEq)]
struct Mahsulot { nom: String, narx: u32 }

impl Ord for Mahsulot {
    fn cmp(&self, other: &Self) -> Ordering {
        self.narx.cmp(&other.narx)
    }
}

impl PartialOrd for Mahsulot {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

fn main() {
    let m1 = Mahsulot { nom: String::from("Qalam"), narx: 2000 };
    let m2 = Mahsulot { nom: String::from("Daftar"), narx: 5000 };

    println!("m1 < m2: {}", m1 < m2);
}
```

## Tushuntirish va Mantiq:
`Ord` traiti to'liq tartiblash imkonini beradi va strukturalarni `vector.sort()` orqali avtomatik saralashga yaroqli qiladi.

## Ishlash natijasi:
```text
m1 < m2: true
```

---

# 516-Topshiriq: Operatorlarni qayta yuklash: std::ops::Add (+ operatori)
## Topshiriq sharti:
Ikkita strukturani `+` bilan qo'shish.

## Yechim (Rust kodi):
```rust
use std::ops::Add;

#[derive(Debug)]
struct Pul { summa: f64 }

impl Add for Pul {
    type Output = Pul;

    fn add(self, other: Pul) -> Pul {
        Pul { summa: self.summa + other.summa }
    }
}

fn main() {
    let p1 = Pul { summa: 150.0 };
    let p2 = Pul { summa: 250.0 };
    let jami = p1 + p2;

    println!("Jami: ${:.2}", jami.summa);
}
```

## Tushuntirish va Mantiq:
Rust da barcha arifmetik operatorlar (`+`, `-`, `*`, `/`) standart traitlar orqali qayta yuklanadi.

## Ishlash natijasi:
```text
Jami: $400.00
```

---

# 517-Topshiriq: Operatorlarni qayta yuklash: std::ops::Sub (- operatori)
## Topshiriq sharti:
Strukturalar ayirmasini hisoblang.

## Yechim (Rust kodi):
```rust
use std::ops::Sub;

#[derive(Debug)]
struct Masofa { metr: i32 }

impl Sub for Masofa {
    type Output = Masofa;

    fn sub(self, other: Masofa) -> Masofa {
        Masofa { metr: self.metr - other.metr }
    }
}

fn main() {
    let m1 = Masofa { metr: 500 };
    let m2 = Masofa { metr: 120 };
    let farq = m1 - m2;

    println!("Farq: {} metr", farq.metr);
}
```

## Tushuntirish va Mantiq:
`Sub` traiti orqali `-` amali domen modellariga tabiiy matematik ko'rinish beradi.

## Ishlash natijasi:
```text
Farq: 380 metr
```

---

# 518-Topshiriq: Operatorlarni qayta yuklash: std::ops::Index ([] operatori)
## Topshiriq sharti:
Struktura elementlariga xuddi massiv kabi `[i]` bilan kirish.

## Yechim (Rust kodi):
```rust
use std::ops::Index;

struct Lugat {
    sozlar: Vec<String>,
}

impl Index<usize> for Lugat {
    type Output = String;

    fn index(&self, index: usize) -> &Self::Output {
        &self.sozlar[index]
    }
}

fn main() {
    let l = Lugat { sozlar: vec![String::from("Rust"), String::from("Tezlik")] };
    println!("0-so'z: {}", l[0]);
}
```

## Tushuntirish va Mantiq:
`Index` traiti qavs `[]` indekslash sintaksisini o'z kolleksiyangiz uchun sozlash imkonini beradi.

## Ishlash natijasi:
```text
0-so'z: Rust
```

---

# 519-Topshiriq: Konvertatsiya Traiti: From va Into
## Topshiriq sharti:
Bir turdan ikkinchisiga toza o'tishni yarating.

## Yechim (Rust kodi):
```rust
struct Son(i32);

impl From<i32> for Son {
    fn from(val: i32) -> Self { Son(val) }
}

fn main() {
    let s1 = Son::from(42);
    let s2: Son = 100.into(); // Into avtomatik hosil bo'ladi!

    println!("s1: {}, s2: {}", s1.0, s2.0);
}
```

## Tushuntirish va Mantiq:
Rust qoidasi: Agar siz `From<A> for B` ni implement qilsangiz, `Into<B> for A` avtomatik tarzda bepul taqdim etiladi.

## Ishlash natijasi:
```text
s1: 42, s2: 100
```

---

# 520-Topshiriq: TryFrom va TryInto: Xatolik berishi mumkin bo'lgan konvertatsiya
## Topshiriq sharti:
Faqat juft sonlarni qabul qiluvchi xavfsiz konvertor yozing.

## Yechim (Rust kodi):
```rust
use std::convert::TryFrom;

struct JuftSon(i32);

impl TryFrom<i32> for JuftSon {
    type Error = &'static str;

    fn try_from(val: i32) -> Result<Self, Self::Error> {
        if val % 2 == 0 {
            Ok(JuftSon(val))
        } else {
            Err("Son juft emas!")
        }
    }
}

fn main() {
    let j1 = JuftSon::try_from(10);
    let j2 = JuftSon::try_from(7);

    println!("10: {:?}", j1.is_ok());
    println!("7:  {:?}", j2.is_err());
}
```

## Tushuntirish va Mantiq:
`TryFrom` muvaffaqiyatsiz bo'lishi mumkin bo'lgan konvertatsiyalarda `Result` qaytarib, xatolikni ushlab qoladi.

## Ishlash natijasi:
```text
10: true
7:  true
```

---

# 521-Topshiriq: AsRef traiti: Arzon havola konvertatsiyasi
## Topshiriq sharti:
Funksiya ham `&str`, ham `&String` ni qabul qila olishi.

## Yechim (Rust kodi):
```rust
fn chop_qil<T: AsRef<str>>(matn: T) {
    println!("Matn: {}", matn.as_ref());
}

fn main() {
    chop_qil("Statik satr");
    chop_qil(String::from("Heap satr"));
}
```

## Tushuntirish va Mantiq:
`AsRef<str>` ko'p qirrali API yaratishda eng mashhur trait bo'lib, ortiqcha xotira ko'chirishsiz ishlaydi.

## Ishlash natijasi:
```text
Matn: Statik satr
Matn: Heap satr
```

---

# 522-Topshiriq: Drop traiti: Resurslarni avtomatik tozalash destruktori
## Topshiriq sharti:
Struktura xotiradan o'chirilayotganda maxsus xabar chiqaring.

## Yechim (Rust kodi):
```rust
struct MaxfiyAgent {
    kod: u32,
}

impl Drop for MaxfiyAgent {
    fn drop(&mut self) {
        println!("Agent #{} xotiradan o'chirildi va izlar yo'qotildi.", self.kod);
    }
}

fn main() {
    {
        let _agent = MaxfiyAgent { kod: 7 };
        println!("Agent vazifani bajarmoqda...");
    }
    println!("Operatsiya yakunlandi.");
}
```

## Tushuntirish va Mantiq:
`Drop` traiti xotira sizib ketishi (memory leak) va ochiq qolgan resurslarni bartaraf etish kafolatidir.

## Ishlash natijasi:
```text
Agent vazifani bajarmoqda...
Agent #7 xotiradan o'chirildi va izlar yo'qotildi.
Operatsiya yakunlandi.
```

---

# 523-Topshiriq: Supertraits: Traitlararo merosxo'rlik
## Topshiriq sharti:
Bitta trait boshqa traitning mavjud bo'lishini shart qilib qo'yishi.

## Yechim (Rust kodi):
```rust
use std::fmt::Display;

trait ChiroyliChop: Display {
    fn ramkada_chop(&self) {
        println!("+-------------------+");
        println!("| {:<17} |", self);
        println!("+-------------------+");
    }
}

struct Xabar(String);
impl Display for Xabar {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.0)
    }
}
impl ChiroyliChop for Xabar {}

fn main() {
    let x = Xabar(String::from("Rust Trait"));
    x.ramkada_chop();
}
```

## Tushuntirish va Mantiq:
`trait B: A` sintaksisi supertrait deb ataladi. `B` ni implement qilgan har qanday tur `A` ni ham bajarishi shart.

## Ishlash natijasi:
```text
+-------------------+
| Rust Trait        |
+-------------------+
```

---

# 524-Topshiriq: Marker Traits: Send va Sync
## Topshiriq sharti:
Oqimlararo xavfsiz uzatilish marker traitlari.

## Yechim (Rust kodi):
```rust
fn tekshir_send_sync<T: Send + Sync>() {
    println!("Bu tur oqimlararo 100% xavfsiz uzatiladi va umumiy o'qiladi!");
}

fn main() {
    tekshir_send_sync::<i32>();
    tekshir_send_sync::<String>();
}
```

## Tushuntirish va Mantiq:
`Send` va `Sync` marker traitlar bo'lib, ularda hech qanday metod yo'q. Ular kompilyatorga turning ko'p oqimli muhitda xavfsiz ekanligini kafolatlaydi.

## Ishlash natijasi:
```text
Bu tur oqimlararo 100% xavfsiz uzatiladi va umumiy o'qiladi!
Bu tur oqimlararo 100% xavfsiz uzatiladi va umumiy o'qiladi!
```

---

# 525-Topshiriq: Assotsiatsiyalangan turlar (Associated Types)
## Topshiriq sharti:
Trait ichida `type Item;` orqali bog'liq turni e'lon qiling.

## Yechim (Rust kodi):
```rust
trait Sanagich {
    type Element;
    fn keyingi(&mut self) -> Option<Self::Element>;
}

struct ButunSanagich { joriy: u32 }

impl Sanagich for ButunSanagich {
    type Element = u32;

    fn keyingi(&mut self) -> Option<Self::Element> {
        self.joriy += 1;
        Some(self.joriy)
    }
}

fn main() {
    let mut s = ButunSanagich { joriy: 0 };
    println!("Keyingi: {:?}", s.keyingi());
    println!("Keyingi: {:?}", s.keyingi());
}
```

## Tushuntirish va Mantiq:
Assotsiatsiyalangan turlar generik trait parametrlaridan farqli o'laroq, har bir struktura uchun faqat bitta aniq natijaviy turni bog'laydi.

## Ishlash natijasi:
```text
Keyingi: Some(1)
Keyingi: Some(2)
```

---

# 526-Topshiriq: Assotsiatsiyalangan konstantalar traitlarda
## Topshiriq sharti:
Trait ichida konstanta talab qiling va uni strukturalarda belgilang.

## Yechim (Rust kodi):
```rust
trait Chegara {
    const MAKSIMAL: u32;
}

struct Server;
impl Chegara for Server {
    const MAKSIMAL: u32 = 10_000;
}

fn main() {
    println!("Server maksimal ulanishlari: {}", Server::MAKSIMAL);
}
```

## Tushuntirish va Mantiq:
Assotsiatsiyalangan konstantalar struktura xususiyatlarini standartlashtirish imkonini beradi.

## Ishlash natijasi:
```text
Server maksimal ulanishlari: 10000
```

---

# 527-Topshiriq: Blanket Implementations: Umumiy trait kengaytmasi
## Topshiriq sharti:
Muayyan shartga mos barcha turlarga yangi metod qo'shish.

## Yechim (Rust kodi):
```rust
trait Salomlashuvchi {
    fn shior(&self);
}

// Display ni bajargan BARCHA turlarga avtomatik Salomlashuvchi beriladi:
impl<T: std::fmt::Display> Salomlashuvchi for T {
    fn shior(&self) {
        println!(">>> Shior: {}", self);
    }
}

fn main() {
    42.shior();
    "Rust Kelajak".shior();
}
```

## Tushuntirish va Mantiq:
Blanket implementation Rust ning eng qudratli imkoniyatlaridan biri bo'lib, butun ekotizimga bitta harakat bilan yangi xatti-harakat beradi.

## Ishlash natijasi:
```text
>>> Shior: 42
>>> Shior: Rust Kelajak
```

---

# 528-Topshiriq: Orphan Rule (Yetim qoidasi) va Newtype andozasi
## Topshiriq sharti:
Nega tashqi tipga tashqi trait berib bo'lmaydi va uni qanday aylanib o'tish kerak?

## Yechim (Rust kodi):
```rust
// Vec<i32> tashqi, Display ham tashqi. Ularni to'g'ridan-to'g'ri bog'lab bo'lmaydi!
// Yechim: Newtype!
use std::fmt;

struct MeningVektorim(Vec<i32>);

impl fmt::Display for MeningVektorim {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "[{}]", self.0.iter().map(|n| n.to_string()).collect::<Vec<_>>().join(", "))
    }
}

fn main() {
    let v = MeningVektorim(vec![1, 2, 3]);
    println!("Display qilingan vektor: {}", v);
}
```

## Tushuntirish va Mantiq:
Yetim qoidasi (Orphan Rule) ikki xil kutubxona bitta tur ustida to'qnashmasligini ta'minlaydi. Newtype esa yangi lokal tur yaratib bu cheklovni yengadi.

## Ishlash natijasi:
```text
Display qilingan vektor: [1, 2, 3]
```

---

# 529-Topshiriq: Domen modeli: Logger traiti va konsol/fayl loggerlari
## Topshiriq sharti:
Xabarlarni turli manbalarga yozuvchi polimorfik tizim.

## Yechim (Rust kodi):
```rust
trait Logger {
    fn log(&self, xabar: &str);
}

struct KonsolLogger;
impl Logger for KonsolLogger {
    fn log(&self, xabar: &str) { println!("[KONSOL] {}", xabar); }
}

struct FaylLogger { fayl_nomi: String }
impl Logger for FaylLogger {
    fn log(&self, xabar: &str) { println!("[FAYL: {}] {}", self.fayl_nomi, xabar); }
}

fn main() {
    let loggerlar: Vec<Box<dyn Logger>> = vec![
        Box::new(KonsolLogger),
        Box::new(FaylLogger { fayl_nomi: String::from("app.log") }),
    ];

    for l in loggerlar {
        l.log("Tizim muvaffaqiyatli ishga tushdi.");
    }
}
```

## Tushuntirish va Mantiq:
Trait objects orqali dastur turli xil loggerlarni bitta umumiy ro'yxatda navbat bilan chaqira oladi.

## Ishlash natijasi:
```text
[KONSOL] Tizim muvaffaqiyatli ishga tushdi.
[FAYL: app.log] Tizim muvaffaqiyatli ishga tushdi.
```

---

# 530-Topshiriq: Domen modeli: Xabarnoma yuboruvchi (Notifier: SMS, Email, Telegram)
## Topshiriq sharti:
Ko'p kanalli xabar yuborish arxitekturasi.

## Yechim (Rust kodi):
```rust
trait Xabarnoma {
    fn yuborish(&self, matn: &str);
}

struct Sms;
impl Xabarnoma for Sms { fn yuborish(&self, m: &str) { println!("SMS: {}", m); } }

struct Telegram;
impl Xabarnoma for Telegram { fn yuborish(&self, m: &str) { println!("Telegram: {}", m); } }

fn main() {
    let xizmatlar: [&dyn Xabarnoma; 2] = [&Sms, &Telegram];
    for x in xizmatlar {
        x.yuborish("Xavfsizlik kodi: 7421");
    }
}
```

## Tushuntirish va Mantiq:
Har bir xizmat o'ziga xos API ga ega bo'lishi mumkin, lekin umumiy trait orqali bitta buyruq bilan ishga tushiriladi.

## Ishlash natijasi:
```text
SMS: Xavfsizlik kodi: 7421
Telegram: Xavfsizlik kodi: 7421
```

---

# 531-Topshiriq: Domen modeli: Sun'iy Intellekt Neyrotarmoq Qatlami (Layer traiti)
## Topshiriq sharti:
Har bir qatlam kirish vektorini qabul qilib chiqish vektorini hisoblaydigan trait.

## Yechim (Rust kodi):
```rust
trait Qatlam {
    fn forward(&self, kirish: &[f32]) -> Vec<f32>;
}

struct LinearQatlam { ogirlik: f32 }
impl Qatlam for LinearQatlam {
    fn forward(&self, kirish: &[f32]) -> Vec<f32> {
        kirish.iter().map(|&x| x * self.ogirlik).collect()
    }
}

fn main() {
    let model: Box<dyn Qatlam> = Box::new(LinearQatlam { ogirlik: 2.0 });
    let x = [1.0, 2.0, 3.0];
    let y = model.forward(&x);

    println!("Chiqish signallari: {:?}", y);
}
```

## Tushuntirish va Mantiq:
AI va chuqur o'rganish dvigatellarida neyrotarmoq qatlamlari `Qatlam` traiti orqali modulli yig'iladi.

## Ishlash natijasi:
```text
Chiqish signallari: [2.0, 4.0, 6.0]
```

---

# 532-Topshiriq: Traitlarda Object Safety (Ob'ekt xavfsizligi) qoidalari
## Topshiriq sharti:
Qachon traitni `dyn Trait` qilib ishlatish mumkin emasligini ko'rsating.

## Yechim (Rust kodi):
```rust
// Agar trait metodida Self qaytarilsa yoki metod generik bo'lsa, u Object Safe bo'lmaydi!
trait Xavfsiz {
    fn ishla(&self);
}

struct A;
impl Xavfsiz for A { fn ishla(&self) { println!("Xavfsiz dispatch"); } }

fn main() {
    let obj: Box<dyn Xavfsiz> = Box::new(A);
    obj.ishla();
}
```

## Tushuntirish va Mantiq:
Dinamik dispatch ishlashi uchun kompilyator vtable da aniq xotira hajmlarini bilishi kerak, shuning uchun `Self: Sized` yoki generik metodli traitlar `dyn Trait` bo'la olmaydi.

## Ishlash natijasi:
```text
Xavfsiz dispatch
```

---

# 533-Topshiriq: Domen modeli: Serializatsiya (ToBytes traiti)
## Topshiriq sharti:
Obyektlarni baytlar massiviga aylantiruvchi trait.

## Yechim (Rust kodi):
```rust
trait ToBytes {
    fn to_bytes(&self) -> Vec<u8>;
}

struct Buyruq(u32);
impl ToBytes for Buyruq {
    fn to_bytes(&self) -> Vec<u8> {
        self.0.to_be_bytes().to_vec()
    }
}

fn main() {
    let b = Buyruq(1024);
    println!("Baytlar ko'rinishi: {:?}", b.to_bytes());
}
```

## Tushuntirish va Mantiq:
Binar protokollar va tarmoq orqali uzatishda har bir ma'lumot `ToBytes` traiti bilan qulay konvertatsiya qilinadi.

## Ishlash natijasi:
```text
Baytlar ko'rinishi: [0, 0, 4, 0]
```

---

# 534-Topshiriq: Operatorlarni qayta yuklash: std::ops::Mul (* operatori)
## Topshiriq sharti:
Skalyar sonni vektorga ko'paytirish amali.

## Yechim (Rust kodi):
```rust
use std::ops::Mul;

#[derive(Debug)]
struct Vektor(f64, f64);

impl Mul<f64> for Vektor {
    type Output = Vektor;

    fn mul(self, skalyar: f64) -> Vektor {
        Vektor(self.0 * skalyar, self.1 * skalyar)
    }
}

fn main() {
    let v = Vektor(2.0, 3.0);
    let natija = v * 3.0;

    println!("Ko'paytirilgan vektor: {:?}", natija);
}
```

## Tushuntirish va Mantiq:
`Mul<Rhs>` traiti har xil turdagi operandlar o'rtasida ham ko'paytirishni ta'riflash imkonini beradi.

## Ishlash natijasi:
```text
Ko'paytirilgan vektor: Vektor(6.0, 9.0)
```

---

# 535-Topshiriq: Strategiya andozasi (Strategy Pattern) traitlar bilan
## Topshiriq sharti:
Saralash strategiyasini dinamik almashtirish.

## Yechim (Rust kodi):
```rust
trait SaralashStrategiyasi {
    fn sarala(&self, arr: &mut [i32]);
}

struct TezkorSaralash;
impl SaralashStrategiyasi for TezkorSaralash {
    fn sarala(&self, arr: &mut [i32]) { arr.sort(); }
}

fn main() {
    let mut sonlar = [5, 2, 8, 1];
    let strategiya: Box<dyn SaralashStrategiyasi> = Box::new(TezkorSaralash);

    strategiya.sarala(&mut sonlar);
    println!("Saralangan: {:?}", sonlar);
}
```

## Tushuntirish va Mantiq:
Strategiya andozasi algoritmlarni mijoz kodidan to'liq ajratib olish imkonini beradi.

## Ishlash natijasi:
```text
Saralangan: [1, 2, 5, 8]
```

---

# 536-Topshiriq: Domen modeli: Shakl yuzasi va perimetri traiti
## Topshiriq sharti:
Geometrik shakllarni interfeys orqali boshqarish.

## Yechim (Rust kodi):
```rust
trait Geometriya {
    fn yuza(&self) -> f64;
    fn perimetr(&self) -> f64;
}

struct Kvadrat { tomon: f64 }
impl Geometriya for Kvadrat {
    fn yuza(&self) -> f64 { self.tomon * self.tomon }
    fn perimetr(&self) -> f64 { 4.0 * self.tomon }
}

fn main() {
    let k = Kvadrat { tomon: 6.0 };
    println!("Yuza: {}, Perimetr: {}", k.yuza(), k.perimetr());
}
```

## Tushuntirish va Mantiq:
Har qanday geometrik shakl ushbu traitni bajarish orqali umumiy hisob-kitob dvigateliga ulanadi.

## Ishlash natijasi:
```text
Yuza: 36, Perimetr: 24
```

---

# 537-Topshiriq: Trait ob'ektlari hajmi: Fat Pointer (16 bayt)
## Topshiriq sharti:
`&dyn Trait` ning xotira o'lchamini tekshiring.

## Yechim (Rust kodi):
```rust
trait Oddiy {}

fn main() {
    println!("&dyn Oddiy ko'rsatkichi hajmi: {} bayt", std::mem::size_of::<&dyn Oddiy>());
}
```

## Tushuntirish va Mantiq:
Dinamik dispatch fat pointer orqali ishlaydi: 8 bayt ma'lumot manzili + 8 bayt vtable (virtual metodlar jadvali) ko'rsatkichi = 16 bayt.

## Ishlash natijasi:
```text
&dyn Oddiy ko'rsatkichi hajmi: 16 bayt
```

---

# 538-Topshiriq: Trait metodlarida &mut self orqali obyektni o'zgartirish
## Topshiriq sharti:
Interfeys orqali obyekt holatini yangilovchi metod tuzing.

## Yechim (Rust kodi):
```rust
trait QaytaYuklash {
    fn reset(&mut self);
}

struct Sanagich { son: u32 }
impl QaytaYuklash for Sanagich {
    fn reset(&mut self) { self.son = 0; }
}

fn main() {
    let mut c = Sanagich { son: 100 };
    c.reset();
    println!("Joriy qiymat: {}", c.son);
}
```

## Tushuntirish va Mantiq:
`&mut self` metodi trait orqali ichki holatni tozalashga imkon beradi.

## Ishlash natijasi:
```text
Joriy qiymat: 0
```

---

# 539-Topshiriq: Trait metodida self (iste'mol qilish) xatti-harakati
## Topshiriq sharti:
Trait orqali obyektni yakuniy natijaga aylantirish.

## Yechim (Rust kodi):
```rust
trait Yakunlovchi {
    type Natija;
    fn tugat(self) -> Self::Natija;
}

struct Tranzaksiya { id: u32 }
impl Yakunlovchi for Tranzaksiya {
    type Natija = String;
    fn tugat(self) -> String { format!("Tranzaksiya #{} yakunlandi", self.id) }
}

fn main() {
    let t = Tranzaksiya { id: 77 };
    println!("{}", t.tugat());
}
```

## Tushuntirish va Mantiq:
Konsuming trait metodlari obyektning hayot davrini qat'iy nazorat qilishda qo'llaniladi.

## Ishlash natijasi:
```text
Tranzaksiya #77 yakunlandi
```

---

# 540-Topshiriq: Domen modeli: Ma'lumotlar bazasi interfeysi (Database Driver)
## Topshiriq sharti:
Mock va Real ma'lumotlar bazalarini bitta trait ostiga yig'ish.

## Yechim (Rust kodi):
```rust
trait Database {
    fn sorov(&self, sql: &str) -> String;
}

struct MockDb;
impl Database for MockDb {
    fn sorov(&self, _sql: &str) -> String { String::from("Mock ma'lumot: 1 qator") }
}

fn main() {
    let db: Box<dyn Database> = Box::new(MockDb);
    println!("{}", db.sorov("SELECT * FROM users"));
}
```

## Tushuntirish va Mantiq:
Baza bilan ishlashda traitlardan foydalanish birlik testlarida (Unit testing) soxta (Mock) bazani ulashni osonlashtiradi.

## Ishlash natijasi:
```text
Mock ma'lumot: 1 qator
```

---

# 541-Topshiriq: Standart Trait: Default ni qo'lda implement qilish
## Topshiriq sharti:
Domen obyekti uchun qulay boshlang'ich sozlamalar.

## Yechim (Rust kodi):
```rust
#[derive(Debug)]
struct AppConfig { port: u16, debug: bool }

impl Default for AppConfig {
    fn default() -> Self { Self { port: 3000, debug: true } }
}

fn main() {
    let cfg = AppConfig::default();
    println!("Standart sozlamalar: {:?}", cfg);
}
```

## Tushuntirish va Mantiq:
`Default` traiti obyektlarni standart parametrlar bilan xavfsiz initsializatsiya qiladi.

## Ishlash natijasi:
```text
Standart sozlamalar: AppConfig { port: 3000, debug: true }
```

---

# 542-Topshiriq: Trait bounds yordamida Min-Max algoritmi
## Topshiriq sharti:
`Ord` traitiga ega har qanday massivdan minimum qiymatni topish.

## Yechim (Rust kodi):
```rust
fn min_qiymat<T: Ord + Copy>(arr: &[T]) -> Option<T> {
    arr.iter().min().copied()
}

fn main() {
    println!("Min son: {:?}", min_qiymat(&[10, 5, 8, 2, 9]));
    println!("Min harf: {:?}", min_qiymat(&['Z', 'B', 'A']));
}
```

## Tushuntirish va Mantiq:
Standart kutubxona metodlari bilan trait bounds mukammal uyg'unlikda ishlaydi.

## Ishlash natijasi:
```text
Min son: Some(2)
Min harf: Some('A')
```

---

# 543-Topshiriq: Bitta strukturaning bir nechta turli traitlarni implement qilishi
## Topshiriq sharti:
Struktura ham `Display`, ham `Add`, ham `Clone` bo'lishi.

## Yechim (Rust kodi):
```rust
#[derive(Clone, Copy, Debug)]
struct Nuqta(i32, i32);

impl std::fmt::Display for Nuqta {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "({}, {})", self.0, self.1)
    }
}

fn main() {
    let p = Nuqta(5, 7);
    println!("Display: {}", p);
    println!("Debug:   {:?}", p);
}
```

## Tushuntirish va Mantiq:
Rust da sinflar merosxo'rligi o'rniga struktura istalgancha ko'p traitlarni bajarishi mumkin.

## Ishlash natijasi:
```text
Display: (5, 7)
Debug:   Nuqta(5, 7)
```

---

# 544-Topshiriq: Domen modeli: Avtoturargoh to'lovi hisoblagichi traiti
## Topshiriq sharti:
Turli transport vositalari (Yuk, Yengil, Motosikl) uchun tarif hisobi.

## Yechim (Rust kodi):
```rust
trait Tarif {
    fn hisobla_narx(&self, soat: u32) -> f64;
}

struct YengilAvto;
impl Tarif for YengilAvto { fn hisobla_narx(&self, s: u32) -> f64 { s as f64 * 10_000.0 } }

struct YukAvto;
impl Tarif for YukAvto { fn hisobla_narx(&self, s: u32) -> f64 { s as f64 * 25_000.0 } }

fn main() {
    let park: [&dyn Tarif; 2] = [&YengilAvto, &YukAvto];
    for t in park {
        println!("2 soatlik turargoh narxi: {} so'm", t.hisobla_narx(2));
    }
}
```

## Tushuntirish va Mantiq:
Dinamik dispatch biznes tariflarini yagona interfeysga keltirishning eng yaxshi usulidir.

## Ishlash natijasi:
```text
2 soatlik turargoh narxi: 20000 so'm
2 soatlik turargoh narxi: 50000 so'm
```

---

# 545-Topshiriq: Trait orqali Funksional kompozitsiya andozasi
## Topshiriq sharti:
Pipeline bosqichlarini trait orqali zanjirlash.

## Yechim (Rust kodi):
```rust
trait Bosqich {
    fn ishla(&self, kirish: String) -> String;
}

struct Tozalovchi;
impl Bosqich for Tozalovchi {
    fn ishla(&self, kirish: String) -> String { kirish.trim().to_string() }
}

fn main() {
    let b: Box<dyn Bosqich> = Box::new(Tozalovchi);
    let res = b.ishla(String::from("  salom   "));
    println!("Natija: '{}'", res);
}
```

## Tushuntirish va Mantiq:
Har bir ma'lumot qayta ishlash qadami mustaqil trait orqali ajratiladi.

## Ishlash natijasi:
```text
Natija: 'salom'
```

---

# 546-Topshiriq: Trait ichida self qaytaruvchi metodlar (Chaining)
## Topshiriq sharti:
O'zgartirib o'zini qaytaruvchi trait andozasi.

## Yechim (Rust kodi):
```rust
trait Kengaytiruvchi: Sized {
    fn qavsga_ol(self) -> Self;
}

impl Kengaytiruvchi for String {
    fn qavsga_ol(self) -> Self { format!("({})", self) }
}

fn main() {
    let s = String::from("Rust").qavsga_ol();
    println!("{}", s);
}
```

## Tushuntirish va Mantiq:
`Self: Sized` cheklovi konsuming metodlarga o'z obyektini qaytarish huquqini beradi.

## Ishlash natijasi:
```text
(Rust)
```

---

# 547-Topshiriq: Trait orqali saralash andozasi (Comparator)
## Topshiriq sharti:
Moslashuvchan solishtirish traiti.

## Yechim (Rust kodi):
```rust
trait Solishtiruvchi<T> {
    fn solishtir(&self, a: &T, b: &T) -> bool;
}

struct Kamayuvchi;
impl Solishtiruvchi<i32> for Kamayuvchi {
    fn solishtir(&self, a: &i32, b: &i32) -> bool { a > b }
}

fn main() {
    let cmp = Kamayuvchi;
    println!("10 > 5 mi: {}", cmp.solishtir(&10, &5));
}
```

## Tushuntirish va Mantiq:
Algoritmlar ichidagi qoidalarni generik traitlar orqali boshqarish mumkin.

## Ishlash natijasi:
```text
10 > 5 mi: true
```

---

# 548-Topshiriq: Domen modeli: Kripto Hamyon Imzolash Traiti
## Topshiriq sharti:
Tranzaksiyalarni imzolash interfeysi.

## Yechim (Rust kodi):
```rust
trait Imzolovchi {
    fn imzo_qoy(&self, xabar: &[u8]) -> Vec<u8>;
}

struct OddiyKalit;
impl Imzolovchi for OddiyKalit {
    fn imzo_qoy(&self, xabar: &[u8]) -> Vec<u8> {
        xabar.iter().map(|b| b ^ 0xAA).collect() // Oddiy simulyatsiya
    }
}

fn main() {
    let k = OddiyKalit;
    let imzo = k.imzo_qoy(b"Salom");
    println!("Imzo baytlari: {:?}", imzo);
}
```

## Tushuntirish va Mantiq:
Kriptografik operatsiyalarni traitlar orqali ajratish turli xavfsizlik chiplarini ulash imkonini beradi.

## Ishlash natijasi:
```text
Imzo baytlari: [217, 171, 198, 197, 199]
```

---

# 549-Topshiriq: Traitlar orqali o'lchov birliklari konvertatsiyasi
## Topshiriq sharti:
Harorat va masofalarni yagona interfeysga solish.

## Yechim (Rust kodi):
```rust
trait StandartBirlik {
    fn si_qiymat(&self) -> f64;
}

struct Dyuym(f64);
impl StandartBirlik for Dyuym {
    fn si_qiymat(&self) -> f64 { self.0 * 0.0254 } // Metrga
}

fn main() {
    let d = Dyuym(10.0);
    println!("10 dyuym = {} metr", d.si_qiymat());
}
```

## Tushuntirish va Mantiq:
Barcha o'lchovlar yagona SI xalqaro tizimiga keltiriladi.

## Ishlash natijasi:
```text
10 dyuym = 0.254 metr
```

---

# 550-Topshiriq: Traits moduli xulosasi: Rust polimorfizmining cho'qqisi
## Topshiriq sharti:
Statik va dinamik dispatch, trait bounds va abstraksiya qoidalari.

## Yechim (Rust kodi):
```rust
fn main() {
    println!("=== RUST TRAITS VA INTERFEYSLAR XULOSASI ===");
    println!("1. Traitlar xatti-harakat shartnomasidir (interfaces).");
    println!("2. Statik dispatch (T: Trait) - 0 nanosoniya sarf, monomorfizatsiya.");
    println!("3. Dinamik dispatch (&dyn Trait) - 16 baytli vtable fat pointer.");
    println!("4. Operatorlar (+, -, [], *) ops traitlari orqali qayta yuklanadi.");
    println!("5. Orphan Rule tizim xavfsizligini ta'minlaydi, Newtype uni hal qiladi.");
}
```

## Tushuntirish va Mantiq:
Rust da to'g'ri loyihalangan traitlar arxitekturasi dunyodagi eng ishonchli va kengaytiriluvchi tizimlarni yaratish kalitidir.

## Ishlash natijasi:
```text
=== RUST TRAITS VA INTERFEYSLAR XULOSASI ===
1. Traitlar xatti-harakat shartnomasidir (interfaces).
2. Statik dispatch (T: Trait) - 0 nanosoniya sarf, monomorfizatsiya.
3. Dinamik dispatch (&dyn Trait) - 16 baytli vtable fat pointer.
4. Operatorlar (+, -, [], *) ops traitlari orqali qayta yuklanadi.
5. Orphan Rule tizim xavfsizligini ta'minlaydi, Newtype uni hal qiladi.
```

---
