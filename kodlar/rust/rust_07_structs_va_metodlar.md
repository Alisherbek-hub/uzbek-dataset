# 7-Qism: Structs (Strukturalar) va Metodlar (`impl`) (301-350)

Ushbu qismda Rust dasturlash tilidagi ma'lumotlar modellashning asosi bo'lgan **Strukturalar (Structs)**, nomlangan maydonli strukturalar, Tuple strukturalar, Newtype andozasi, Unit-like strukturalar, `impl` bloklari, metodlar (`&self`, `&mut self`, `self`), assotsiatsiyalangan konstruktorlar (`Self::new`), enkapsulyatsiya, `derive` makrolari hamda zamonaviy domen modellarini loyihalash o'rganiladi.

---

# 301-Topshiriq: Struktura (struct) nima? Ma'lumotlarni mantiqiy guruhlash
## Topshiriq sharti:
Foydalanuvchi ma'lumotlarini saqlovchi sodda struktura e'lon qiling va instansiya yarating.

## Yechim (Rust kodi):
```rust
struct Foydalanuvchi {
    ism: String,
    yosh: u8,
    faolmi: bool,
}

fn main() {
    let f = Foydalanuvchi {
        ism: String::from("Anvar"),
        yosh: 25,
        faolmi: true,
    };

    println!("Foydalanuvchi: {}, Yoshi: {}, Faolmi: {}", f.ism, f.yosh, f.faolmi);
}
```

## Tushuntirish va Mantiq:
Struktura bir-biri bilan bog'liq har xil turdagi ma'lumotlarni bitta mantiqiy nom ostida birlashtirish imkonini beradi.

## Ishlash natijasi:
```text
Foydalanuvchi: Anvar, Yoshi: 25, Faolmi: true
```

---

# 302-Topshiriq: O'zgaruvchan struktura instansiyasi va maydonlarni yangilash
## Topshiriq sharti:
`let mut` orqali struktura maydonini yangilang.

## Yechim (Rust kodi):
```rust
struct Xodim {
    ism: String,
    lavozim: String,
    maosh: u32,
}

fn main() {
    let mut x = Xodim {
        ism: String::from("Sardor"),
        lavozim: String::from("Junior"),
        maosh: 1000,
    };

    x.lavozim = String::from("Middle");
    x.maosh = 2200;

    println!("Xodim: {}, Lavozim: {}, Maosh: ${}", x.ism, x.lavozim, x.maosh);
}
```

## Tushuntirish va Mantiq:
Rust da faqat ayrim maydonlarni alohida `mut` qilib bo'lmaydi: strukturaning butun instansiyasi `let mut` bo'lishi shart.

## Ishlash natijasi:
```text
Xodim: Sardor, Lavozim: Middle, Maosh: $2200
```

---

# 303-Topshiriq: Field Init Shorthand: Parametr va maydon nomi bir xil bo'lganda
## Topshiriq sharti:
Konstruktor funksiyasida maydon nomlarini qisqartirib yozing.

## Yechim (Rust kodi):
```rust
struct Kitob {
    nomi: String,
    muallif: String,
}

fn yangi_kitob(nomi: String, muallif: String) -> Kitob {
    // 'nomi: nomi' o'rniga shunchaki 'nomi'
    Kitob { nomi, muallif }
}

fn main() {
    let k = yangi_kitob(String::from("Yulduzli tunlar"), String::from("Pirimqul Qodirov"));
    println!("Kitob: '{}', Muallif: {}", k.nomi, k.muallif);
}
```

## Tushuntirish va Mantiq:
Agar funksiya argumenti bilan struktura maydonining nomi bir xil bo'lsa, `maydon: maydon` deb takrorlamasdan qisqa yozish mumkin.

## Ishlash natijasi:
```text
Kitob: 'Yulduzli tunlar', Muallif: Pirimqul Qodirov
```

---

# 304-Topshiriq: Struct Update Syntax: ..boshqa_struct
## Topshiriq sharti:
Mavjud strukturadagi ma'lumotlarni olib, faqat bitta maydonni o'zgartirgan yangi nusxa yarating.

## Yechim (Rust kodi):
```rust
struct Profil {
    foydalanuvchi_nomi: String,
    email: String,
    kirishlar_soni: u64,
    faol: bool,
}

fn main() {
    let p1 = Profil {
        foydalanuvchi_nomi: String::from("user123"),
        email: String::from("user@test.uz"),
        kirishlar_soni: 42,
        faol: true,
    };

    let p2 = Profil {
        email: String::from("yangi_email@test.uz"),
        ..p1 // Qolgan barcha maydonlar p1 dan olinadi
    };

    println!("p2 foydalanuvchi: {}, email: {}", p2.foydalanuvchi_nomi, p2.email);
}
```

## Tushuntirish va Mantiq:
`..p1` sintaksisi ko'rsatilmagan barcha maydonlarni `p1` dan ko'chirib oladi.

## Ishlash natijasi:
```text
p2 foydalanuvchi: user123, email: yangi_email@test.uz
```

---

# 305-Topshiriq: Tuple Structs (Kortejsimon strukturalar)
## Topshiriq sharti:
Maydonlariga nom bermasdan, faqat turlar tartibini belgilovchi struktura tuzing.

## Yechim (Rust kodi):
```rust
struct Rang(u8, u8, u8); // RGB
struct Nuqta3D(f64, f64, f64); // X, Y, Z

fn main() {
    let qizil = Rang(255, 0, 0);
    let joy = Nuqta3D(12.5, 45.0, 3.14);

    println!("Rang RGB: ({}, {}, {})", qizil.0, qizil.1, qizil.2);
    println!("Koordinata: ({}, {}, {})", joy.0, joy.1, joy.2);
}
```

## Tushuntirish va Mantiq:
Tuple strukturalar har bir maydonga alohida nom o'ylab o'tirmasdan, qisqa va qat'iy tiplangan guruh yaratishda ishlatiladi.

## Ishlash natijasi:
```text
Rang RGB: (255, 0, 0)
Koordinata: (12.5, 45, 3.14)
```

---

# 306-Topshiriq: Newtype Pattern: Tip xavfsizligini ta'minlovchi bir qiymatli struktura
## Topshiriq sharti:
Santimetr va Millimetr turlarini adashtirib yuborishning oldini oluvchi Newtype tuzing.

## Yechim (Rust kodi):
```rust
struct Millimetr(u32);
struct Santimetr(u32);

fn kesish(uzunlik: Millimetr) {
    println!("{} mm kesildi.", uzunlik.0);
}

fn main() {
    let sm = Santimetr(50);
    let mm = Millimetr(500);

    kesish(mm);
    // kesish(sm); // Kompilyator xatolik beradi! Chunki turlar har xil!
}
```

## Tushuntirish va Mantiq:
Newtype andozasi bitta primitiv turni struktura ichiga o'rab oladi. Bu biznes-mantiqdagi jiddiy adashishlarni (masalan km va mil xatolarini) noldan yo'q qiladi.

## Ishlash natijasi:
```text
500 mm kesildi.
```

---

# 307-Topshiriq: Unit-like Structs: Maydonsiz birlik strukturalar
## Topshiriq sharti:
Hech qanday ma'lumot saqlamaydigan, faqat xatti-harakat (traiti) uchun xizmat qiluvchi struktura.

## Yechim (Rust kodi):
```rust
struct BosildiHodisasi;

fn hodisani_qayta_ishla(_e: BosildiHodisasi) {
    println!("Tugma bosilish hodisasi qayta ishlandi!");
}

fn main() {
    let e = BosildiHodisasi;
    println!("Birlik struktura o'lchami: {} bayt", std::mem::size_of::<BosildiHodisasi>());
    hodisani_qayta_ishla(e);
}
```

## Tushuntirish va Mantiq:
Unit-like strukturalar xotirada 0 bayt joy egallaydi. Ular holatsiz xizmatlar (State-less services) yoki marker traitlar uchun ishlatiladi.

## Ishlash natijasi:
```text
Birlik struktura o'lchami: 0 bayt
Tugma bosilish hodisasi qayta ishlandi!
```

---

# 308-Topshiriq: impl bloki va &self metodi
## Topshiriq sharti:
Struktura ichida uning maydonlarini o'qib hisob-kitob qiluvchi metod yozing.

## Yechim (Rust kodi):
```rust
struct Tortburchak {
    kenglik: u32,
    balandlik: u32,
}

impl Tortburchak {
    fn yuza(&self) -> u32 {
        self.kenglik * self.balandlik
    }
}

fn main() {
    let t = Tortburchak { kenglik: 30, balandlik: 50 };
    println!("To'rtburchak yuzi: {}", t.yuza());
}
```

## Tushuntirish va Mantiq:
`impl` bloki strukturaning metodlarini saqlaydi. `&self` metodi chaqirilganda, obyektning o'ziga o'zgarmas havola uzatiladi.

## Ishlash natijasi:
```text
To'rtburchak yuzi: 1500
```

---

# 309-Topshiriq: &mut self metodi: Obyektni o'zgartiruvchi metodlar
## Topshiriq sharti:
Struktura holatini ichkaridan yangilovchi metod tuzing.

## Yechim (Rust kodi):
```rust
struct Mashina {
    yoqilgi: f64,
}

impl Mashina {
    fn zapravka(&mut self, litr: f64) {
        self.yoqilgi += litr;
        println!("+ {:.1} litr quyildi. Bakda: {:.1} l", litr, self.yoqilgi);
    }
}

fn main() {
    let mut avto = Mashina { yoqilgi: 15.0 };
    avto.zapravka(25.0);
}
```

## Tushuntirish va Mantiq:
`&mut self` metodi chaqirilishi uchun obyektning o'zi `mut` bo'lishi shart va bu metod xavfsiz holda ichki maydonlarni o'zgartiradi.

## Ishlash natijasi:
```text
+ 25.0 litr quyildi. Bakda: 40.0 l
```

---

# 310-Topshiriq: self (Consuming) metodi: Obyektni iste'mol qiluvchi metodlar
## Topshiriq sharti:
Metod chaqirilgach, obyektni yo'q qilib boshqa turga aylantiring.

## Yechim (Rust kodi):
```rust
struct Xat {
    matn: String,
}

impl Xat {
    fn yuborish(self) {
        println!("Xat jo'natildi: '{}'", self.matn);
    } // 'self' bu yerda o'chiriladi
}

fn main() {
    let x = Xat { matn: String::from("Rust imtihoni natijalari") };
    x.yuborish();

    // x.yuborish(); // Xatolik: xat allaqachon yuborilgan (iste'mol bo'lgan)!
}
```

## Tushuntirish va Mantiq:
Metod parametrida shunchaki `self` ko'rsatilsa, chaqiruv paytida obyekt to'liq iste'mol qilinadi va uni qayta ishlatib bo'lmaydi.

## Ishlash natijasi:
```text
Xat jo'natildi: 'Rust imtihoni natijalari'
```

---

# 311-Topshiriq: Assotsiatsiyalangan funksiyalar (Konstruktorlar: Self::new)
## Topshiriq sharti:
`self` qabul qilmaydigan statik konstruktor yarating.

## Yechim (Rust kodi):
```rust
struct Foydalanuvchi {
    nom: String,
    id: u64,
}

impl Foydalanuvchi {
    fn new(nom: &str, id: u64) -> Self {
        Self { nom: nom.to_string(), id }
    }
}

fn main() {
    let f = Foydalanuvchi::new("Temur", 1001);
    println!("Foydalanuvchi #{}: {}", f.id, f.nom);
}
```

## Tushuntirish va Mantiq:
`Self::new` yoki `Tipi::metod()` orqali chaqiriladigan funksiyalar assotsiatsiyalangan funksiya deb ataladi. Ular yangi obyekt yaratish uchun standart usuldir.

## Ishlash natijasi:
```text
Foydalanuvchi #1001: Temur
```

---

# 312-Topshiriq: Bir nechta impl bloklari
## Topshiriq sharti:
Bitta strukturaning metodlarini bir nechta alohida `impl` bloklariga bo'lib yozing.

## Yechim (Rust kodi):
```rust
struct Kalkulyator;

impl Kalkulyator {
    fn qoshish(a: i32, b: i32) -> i32 { a + b }
}

impl Kalkulyator {
    fn kopaytirish(a: i32, b: i32) -> i32 { a * b }
}

fn main() {
    println!("10 + 5 = {}", Kalkulyator::qoshish(10, 5));
    println!("10 * 5 = {}", Kalkulyator::kopaytirish(10, 5));
}
```

## Tushuntirish va Mantiq:
Rust da bitta struktura uchun istalgancha `impl` bloki ochish mumkin. Bu katta kod bazalarida metodlarni mantiqiy guruhlarga ajratishda qulaydir.

## Ishlash natijasi:
```text
10 + 5 = 15
10 * 5 = 50
```

---

# 313-Topshiriq: Enkapsulyatsiya: Maydonlarni yashirish va Getter yaratish
## Topshiriq sharti:
Tashqaridan maydonni to'g'ridan-to'g'ri o'qishni taqiqlab, faqat getter orqali oching.

## Yechim (Rust kodi):
```rust
mod xavfsizlik {
    pub struct Shaxs {
        ism: String,
        jshshir: String, // private maydon
    }

    impl Shaxs {
        pub fn new(ism: &str, jshshir: &str) -> Self {
            Self { ism: ism.to_string(), jshshir: jshshir.to_string() }
        }

        pub fn ismni_ol(&self) -> &str {
            &self.ism
        }

        pub fn jshshir_oxirgi_raqamlari(&self) -> &str {
            &self.jshshir[self.jshshir.len()-4..]
        }
    }
}

fn main() {
    let sh = xavfsizlik::Shaxs::new("Malika", "12345678901234");
    println!("Shaxs: {}, JShShIR oxiri: ***{}", sh.ismni_ol(), sh.jshshir_oxirgi_raqamlari());
}
```

## Tushuntirish va Mantiq:
Maydonlar `pub` qilinmasa, ular faqat o'z moduli ichida ko'rinadi. Getter orqali ma'lumotning faqat xavfsiz qismini taqdim etish mumkin.

## Ishlash natijasi:
```text
Shaxs: Malika, JShShIR oxiri: ***1234
```

---

# 314-Topshiriq: Enkapsulyatsiya: Setter metodida ma'lumotni validatsiya qilish
## Topshiriq sharti:
Yaroqsiz qiymat berilishini tekshiruvchi setter metod yozing.

## Yechim (Rust kodi):
```rust
struct Talaba {
    ism: String,
    yosh: u8,
}

impl Talaba {
    fn new(ism: &str) -> Self {
        Self { ism: ism.to_string(), yosh: 18 }
    }

    fn yoshni_belgila(&mut self, yangi_yosh: u8) -> bool {
        if yangi_yosh >= 16 && yangi_yosh <= 80 {
            self.yosh = yangi_yosh;
            true
        } else {
            println!("Xatolik: Noto'g'ri yosh kiritildi ({})!", yangi_yosh);
            false
        }
    }
}

fn main() {
    let mut t = Talaba::new("Javohir");
    t.yoshni_belgila(21);
    t.yoshni_belgila(120);

    println!("Talaba yoshi: {}", t.yosh);
}
```

## Tushuntirish va Mantiq:
Setter metodlari ma'lumotlar yaxlitligini (Data Integrity) kafolatlaydi va obyektdagi holat har doim to'g'ri bo'lishini ta'minlaydi.

## Ishlash natijasi:
```text
Xatolik: Noto'g'ri yosh kiritildi (120)!
Talaba yoshi: 21
```

---

# 315-Topshiriq: Ichma-ich strukturalar (Nested Structs)
## Topshiriq sharti:
Kompyuter komponentlari (Protsessor va Xotira) strukturasini loyihalang.

## Yechim (Rust kodi):
```rust
struct Cpu {
    model: String,
    yadrolar: u32,
}

struct Kompyuter {
    nomi: String,
    cpu: Cpu,
    ram_gb: u32,
}

fn main() {
    let pc = Kompyuter {
        nomi: String::from("Ish stansiyasi"),
        cpu: Cpu {
            model: String::from("AMD Ryzen 9"),
            yadrolar: 16,
        },
        ram_gb: 64,
    };

    println!("{}: {} ({} yadroli), RAM: {} GB", pc.nomi, pc.cpu.model, pc.cpu.yadrolar, pc.ram_gb);
}
```

## Tushuntirish va Mantiq:
Strukturalar ichida boshqa strukturalarni joylashtirish murakkab real dunyo obyektlarini aniq va toza modellashtirishga xizmat qiladi.

## Ishlash natijasi:
```text
Ish stansiyasi: AMD Ryzen 9 (16 yadroli), RAM: 64 GB
```

---

# 316-Topshiriq: #[derive(Debug)] orqali strukturani konsolda chop etish
## Topshiriq sharti:
`{:?}` va `{:#?}` formatlari yordamida strukturani debug ko'rinishida chiqaring.

## Yechim (Rust kodi):
```rust
#[derive(Debug)]
struct Shahar {
    nomi: String,
    aholi: u64,
}

fn main() {
    let sh = Shahar {
        nomi: String::from("Samarqand"),
        aholi: 550_000,
    };

    println!("Oddiy debug: {:?}", sh);
    println!("Chiroyli debug:
{:#?}", sh);
}
```

## Tushuntirish va Mantiq:
`#[derive(Debug)]` atributi kompilyatordan avtomatik ravishda `Debug` traitini struktura uchun hosil qilishni so'raydi.

## Ishlash natijasi:
```text
Oddiy debug: Shahar { nomi: "Samarqand", aholi: 550000 }
Chiroyli debug:
Shahar {
    nomi: "Samarqand",
    aholi: 550000,
}
```

---

# 317-Topshiriq: #[derive(PartialEq, Eq)] orqali strukturalarni solishtirish
## Topshiriq sharti:
Ikkita struktura nusxalarining maydonma-maydon tengligini tekshiring.

## Yechim (Rust kodi):
```rust
#[derive(Debug, PartialEq, Eq)]
struct Mahsulot {
    id: u32,
    nom: String,
}

fn main() {
    let m1 = Mahsulot { id: 101, nom: String::from("Klaviatura") };
    let m2 = Mahsulot { id: 101, nom: String::from("Klaviatura") };
    let m3 = Mahsulot { id: 102, nom: String::from("Sichqoncha") };

    println!("m1 == m2: {}", m1 == m2);
    println!("m1 == m3: {}", m1 == m3);
}
```

## Tushuntirish va Mantiq:
`PartialEq` traiti `==` va `!=` operatorlarini barcha ichki maydonlarni avtomatik solishtirish orqali implement qiladi.

## Ishlash natijasi:
```text
m1 == m2: true
m1 == m3: false
```

---

# 318-Topshiriq: #[derive(Default)] orqali standart qiymatli strukturalar
## Topshiriq sharti:
Barcha maydonlariga o'z turining standart qiymatini biriktiruvchi atributni ko'rsating.

## Yechim (Rust kodi):
```rust
#[derive(Debug, Default)]
struct Sozlamalar {
    port: u16,
    kengaytma: bool,
    vaqt_chegarasi: u32,
}

fn main() {
    let standart = Sozlamalar::default();
    println!("Standart sozlamalar: {:?}", standart);
}
```

## Tushuntirish va Mantiq:
`Default::default()` sonlar uchun 0, mantiqiy ifodalar uchun `false`, matnlar uchun `""` qilib initsializatsiya qiladi.

## Ishlash natijasi:
```text
Standart sozlamalar: Sozlamalar { port: 0, kengaytma: false, vaqt_chegarasi: 0 }
```

---

# 319-Topshiriq: Qo'lda Default traitini implement qilish
## Topshiriq sharti:
O'zingiz xohlagan boshlang'ich qiymatlar bilan `Default` yarating.

## Yechim (Rust kodi):
```rust
#[derive(Debug)]
struct Server {
    ip: String,
    port: u16,
}

impl Default for Server {
    fn default() -> Self {
        Self {
            ip: String::from("127.0.0.1"),
            port: 8080,
        }
    }
}

fn main() {
    let s = Server::default();
    println!("Standart server: {}:{}", s.ip, s.port);
}
```

## Tushuntirish va Mantiq:
`impl Default for T` orqali standart konstruktor qiymatlarini domen talablariga moslab sozlash mumkin.

## Ishlash natijasi:
```text
Standart server: 127.0.0.1:8080
```

---

# 320-Topshiriq: Domen modeli: 2D Nuqta va Evklid masofasi
## Topshiriq sharti:
Ikkita nuqta o'rtasidagi masofani hisoblovchi metod yozing.

## Yechim (Rust kodi):
```rust
struct Nuqta {
    x: f64,
    y: f64,
}

impl Nuqta {
    fn masofa(&self, boshqa: &Nuqta) -> f64 {
        let dx = self.x - boshqa.x;
        let dy = self.y - boshqa.y;
        (dx * dx + dy * dy).sqrt()
    }
}

fn main() {
    let p1 = Nuqta { x: 0.0, y: 0.0 };
    let p2 = Nuqta { x: 3.0, y: 4.0 };

    println!("Nuqtalar orasidagi masofa: {}", p1.masofa(&p2));
}
```

## Tushuntirish va Mantiq:
Pifagor teoremasi orqali hisoblanadigan masofa metodi ikkala nuqtani ham o'zgarishsiz qarzga oladi.

## Ishlash natijasi:
```text
Nuqtalar orasidagi masofa: 5
```

---

# 321-Topshiriq: Domen modeli: To'g'ri to'rtburchak va sig'dirish (can_hold)
## Topshiriq sharti:
Bitta to'rtburchak ikkinchisining ichiga sig'ishini tekshiruvchi metod tuzing.

## Yechim (Rust kodi):
```rust
struct Tortburchak {
    kenglik: u32,
    balandlik: u32,
}

impl Tortburchak {
    fn sigadimi(&self, boshqa: &Tortburchak) -> bool {
        self.kenglik > boshqa.kenglik && self.balandlik > boshqa.balandlik
    }
}

fn main() {
    let t1 = Tortburchak { kenglik: 80, balandlik: 50 };
    let t2 = Tortburchak { kenglik: 60, balandlik: 40 };
    let t3 = Tortburchak { kenglik: 90, balandlik: 60 };

    println!("t1 t2 ni sig'diradimi: {}", t1.sigadimi(&t2));
    println!("t1 t3 ni sig'diradimi: {}", t1.sigadimi(&t3));
}
```

## Tushuntirish va Mantiq:
Metod o'zining `&self` parametridan tashqari boshqa nusxaning `&Tortburchak` havolasini ham qabul qiladi.

## Ishlash natijasi:
```text
t1 t2 ni sig'diradimi: true
t1 t3 ni sig'diradimi: false
```

---

# 322-Topshiriq: Domen modeli: Bank hisobi va tranzaksiyalar jurnali
## Topshiriq sharti:
Har bir amaliyotni saqlab boruvchi to'liq bank hisobini yarating.

## Yechim (Rust kodi):
```rust
struct Hisob {
    egasi: String,
    balans: f64,
    tarix: Vec<String>,
}

impl Hisob {
    fn new(egasi: &str, boshlangich: f64) -> Self {
        Self {
            egasi: egasi.to_string(),
            balans: boshlangich,
            tarix: vec![format!("Boshlang'ich hisob: ${:.2}", boshlangich)],
        }
    }

    fn tolov(&mut self, summa: f64, maqsad: &str) -> bool {
        if self.balans >= summa {
            self.balans -= summa;
            self.tarix.push(format!("To'lov '{}': -${:.2}", maqsad, summa));
            true
        } else {
            false
        }
    }

    fn hisobot(&self) {
        println!("=== {} Hisoboti ===", self.egasi);
        for yozuv in &self.tarix {
            println!("  {}", yozuv);
        }
        println!("Yakuniy balans: ${:.2}", self.balans);
    }
}

fn main() {
    let mut h = Hisob::new("Bobur", 500.0);
    h.tolov(120.0, "Internet to'lovi");
    h.tolov(80.0, "Kofe va tushlik");
    h.hisobot();
}
```

## Tushuntirish va Mantiq:
Struktura ichida vektor saqlash murakkab amallar tarixini o'z ichiga oluvchi professional domen obyektlarini yaratish imkonini beradi.

## Ishlash natijasi:
```text
=== Bobur Hisoboti ===
  Boshlang'ich hisob: $500.00
  To'lov 'Internet to'lovi': -$120.00
  To'lov 'Kofe va tushlik': -$80.00
Yakuniy balans: $300.00
```

---

# 323-Topshiriq: Domen modeli: E-Commerce savati (Shopping Cart)
## Topshiriq sharti:
Tovarlarni qo'shish va umumiy narxni hisoblash modelini loyihalang.

## Yechim (Rust kodi):
```rust
struct Mahsulot {
    nomi: String,
    narxi: f64,
}

struct Savat {
    tovarlar: Vec<Mahsulot>,
}

impl Savat {
    fn new() -> Self {
        Self { tovarlar: Vec::new() }
    }

    fn qosh(&mut self, m: Mahsulot) {
        self.tovarlar.push(m);
    }

    fn jami_summa(&self) -> f64 {
        self.tovarlar.iter().map(|t| t.narxi).sum()
    }
}

fn main() {
    let mut s = Savat::new();
    s.qosh(Mahsulot { nomi: String::from("Sichqoncha"), narxi: 25.0 });
    s.qosh(Mahsulot { nomi: String::from("Monitor"), narxi: 180.0 });

    println!("Savatdagi jami to'lov: ${:.2}", s.jami_summa());
}
```

## Tushuntirish va Mantiq:
Strukturalar kompozitsiyasi orqali do'kon xarid tizimini sodda va tushunarli modellashtirish mumkin.

## Ishlash natijasi:
```text
Savatdagi jami to'lov: $205.00
```

---

# 324-Topshiriq: Domen modeli: RPG O'yin Qahramoni (Jang va Himoya)
## Topshiriq sharti:
Salomatlik (HP), hujum va tajriba parametrlariga ega qahramon metodlari.

## Yechim (Rust kodi):
```rust
struct Qahramon {
    nomi: String,
    hp: i32,
    hujum_kuchi: i32,
}

impl Qahramon {
    fn hujum_qil(&self, dushman: &mut Qahramon) {
        println!("{} {} ga {} zarba berdi!", self.nomi, dushman.nomi, self.hujum_kuchi);
        dushman.hp -= self.hujum_kuchi;
    }

    fn tirikmi(&self) -> bool {
        self.hp > 0
    }
}

fn main() {
    let ritsar = Qahramon { nomi: String::from("Artur"), hp: 100, hujum_kuchi: 35 };
    let mut ajdaho = Qahramon { nomi: String::from("Smog"), hp: 60, hujum_kuchi: 50 };

    ritsar.hujum_qil(&mut ajdaho);
    ritsar.hujum_qil(&mut ajdaho);

    println!("Ajdaho tirikmi: {}", ajdaho.tirikmi());
}
```

## Tushuntirish va Mantiq:
`&self` (hujumchi) va `&mut dushman` (zarba qabul qiluvchi) parametrlari o'yin mexanikalarini xatosiz ifodalaydi.

## Ishlash natijasi:
```text
Artur Smog ga 35 zarba berdi!
Artur Smog ga 35 zarba berdi!
Ajdaho tirikmi: false
```

---

# 325-Topshiriq: Domen modeli: Vaqt hisoblagich (Vaqt qo'shish arifmetikasi)
## Topshiriq sharti:
Soat, daqiqa va soniyalarni normallashtirib qo'shuvchi struktura.

## Yechim (Rust kodi):
```rust
struct Vaqt {
    soat: u32,
    daqiqa: u32,
    soniya: u32,
}

impl Vaqt {
    fn sekund_qosh(&mut self, s: u32) {
        let jami_sekund = self.soniya + s;
        self.soniya = jami_sekund % 60;

        let jami_daqiqa = self.daqiqa + (jami_sekund / 60);
        self.daqiqa = jami_daqiqa % 60;

        self.soat = (self.soat + (jami_daqiqa / 60)) % 24;
    }
}

fn main() {
    let mut v = Vaqt { soat: 10, daqiqa: 58, soniya: 40 };
    v.sekund_qosh(150); // 2 daqiqa 30 sekund qo'shiladi

    println!("Yangi vaqt: {:02}:{:02}:{:02}", v.soat, v.daqiqa, v.soniya);
}
```

## Tushuntirish va Mantiq:
Struktura metodlari ichida murakkab 60 lik va 24 lik vaqt chegaralari nazorat qilinadi.

## Ishlash natijasi:
```text
Yangi vaqt: 11:01:10
```

---

# 326-Topshiriq: Builder andozasi (UserBuilder) orqali obyekt yig'ish
## Topshiriq sharti:
Ko'p parametrli strukturalarni xatosiz bosqichma-bosqich qurish.

## Yechim (Rust kodi):
```rust
struct Foydalanuvchi {
    ism: String,
    yosh: u8,
    vip: bool,
}

struct FoydalanuvchiBuilder {
    ism: String,
    yosh: u8,
    vip: bool,
}

impl FoydalanuvchiBuilder {
    fn new(ism: &str) -> Self {
        Self { ism: ism.to_string(), yosh: 18, vip: false }
    }

    fn yosh(mut self, y: u8) -> Self { self.yosh = y; self }
    fn vip(mut self, v: bool) -> Self { self.vip = v; self }

    fn build(self) -> Foydalanuvchi {
        Foydalanuvchi { ism: self.ism, yosh: self.yosh, vip: self.vip }
    }
}

fn main() {
    let user = FoydalanuvchiBuilder::new("Davron")
        .yosh(29)
        .vip(true)
        .build();

    println!("Yaratildi: {}, {} yosh, VIP={}", user.ism, user.yosh, user.vip);
}
```

## Tushuntirish va Mantiq:
Builder andozasi ixtiyoriy parametrlarga ega obyektlarni toza va xatosiz initsializatsiya qilish imkonini beradi.

## Ishlash natijasi:
```text
Yaratildi: Davron, 29 yosh, VIP=true
```

---

# 327-Topshiriq: Immutable Update metodi (with_*)
## Topshiriq sharti:
Obyektni o'zgartirmasdan, yangi o'zgargan klonini qaytarish.

## Yechim (Rust kodi):
```rust
#[derive(Clone, Debug)]
struct Nuqta {
    x: i32,
    y: i32,
}

impl Nuqta {
    fn with_x(&self, yangi_x: i32) -> Self {
        Self { x: yangi_x, y: self.y }
    }
}

fn main() {
    let p1 = Nuqta { x: 5, y: 10 };
    let p2 = p1.with_x(25);

    println!("p1 = {:?}", p1);
    println!("p2 = {:?}", p2);
}
```

## Tushuntirish va Mantiq:
`with_*` funksional dasturlash uslubi bo'lib, asl obyektning immutability (o'zgarmaslik) qoidasini to'liq saqlab qoladi.

## Ishlash natijasi:
```text
p1 = Nuqta { x: 5, y: 10 }
p2 = Nuqta { x: 25, y: 10 }
```

---

# 328-Topshiriq: Rekursiv strukturalar va Box<Self> zarurati
## Topshiriq sharti:
Struktura ichida o'zini saqlash uchun nima sababdan `Box` talab qilinishini ko'rsating.

## Yechim (Rust kodi):
```rust
struct FaylDaraxti {
    nom: String,
    ichki_papka: Option<Box<FaylDaraxti>>,
}

fn main() {
    let papka = FaylDaraxti {
        nom: String::from("root"),
        ichki_papka: Some(Box::new(FaylDaraxti {
            nom: String::from("documents"),
            ichki_papka: None,
        })),
    };

    println!("Asosiy papka: {}, Ichki: {}", papka.nom, papka.ichki_papka.as_ref().unwrap().nom);
}
```

## Tushuntirish va Mantiq:
Rust har bir turning Stack dagi hajmini kompilyatsiyada bilishi shart. Rekursiv strukturada cheksiz o'lcham xatosi bo'lmasligi uchun aniq 8 baytli `Box` ko'rsatkichidan foydalaniladi.

## Ishlash natijasi:
```text
Asosiy papka: root, Ichki: documents
```

---

# 329-Topshiriq: Struktura yordamida Stack (Yig'ma) ma'lumotlar tuzilmasi
## Topshiriq sharti:
LIFO tamoyili bo'yicha ishlovchi Stack tuzing (`push`, `pop`, `peek`).

## Yechim (Rust kodi):
```rust
struct Yigma {
    elementlar: Vec<i32>,
}

impl Yigma {
    fn new() -> Self { Self { elementlar: Vec::new() } }
    fn push(&mut self, val: i32) { self.elementlar.push(val); }
    fn pop(&mut self) -> Option<i32> { self.elementlar.pop() }
    fn peek(&self) -> Option<&i32> { self.elementlar.last() }
}

fn main() {
    let mut s = Yigma::new();
    s.push(10);
    s.push(20);

    println!("Oxirgi element (peek): {:?}", s.peek());
    println!("Olingan (pop): {:?}", s.pop());
    println!("Yangi oxirgi: {:?}", s.peek());
}
```

## Tushuntirish va Mantiq:
Struktura enkapsulyatsiyasi vektorning ortiqcha metodlarini yashirib, faqat qat'iy Stack interfeysini qoldiradi.

## Ishlash natijasi:
```text
Oxirgi element (peek): Some(20)
Olingan (pop): Some(20)
Yangi oxirgi: Some(10)
```

---

# 330-Topshiriq: Struktura maydonida funksiya ko'rsatkichini saqlash
## Topshiriq sharti:
Har bir obyektga uning xatti-harakatini belgilovchi maxsus funksiyani biriktiring.

## Yechim (Rust kodi):
```rust
struct Tugma {
    nom: String,
    harakat: fn(&str),
}

fn bosilganda(nom: &str) {
    println!("'{}' tugmasi bosildi!", nom);
}

fn main() {
    let btn = Tugma {
        nom: String::from("Saqlash"),
        harakat: bosilganda,
    };

    (btn.harakat)(&btn.nom);
}
```

## Tushuntirish va Mantiq:
Funksiya ko'rsatkichlari maydon sifatida saqlanishi orqali UI tugmalari, callbacklar va hodisalar boshqaruvchisi quriladi.

## Ishlash natijasi:
```text
'Saqlash' tugmasi bosildi!
```

---

# 331-Topshiriq: Struktura xotirasining tekislanishi (Struct Alignment & Padding)
## Topshiriq sharti:
Maydonlar tartibining xotira o'lchamiga ta'sirini ko'rsating.

## Yechim (Rust kodi):
```rust
struct Tartibsiz {
    a: u8,   // 1 bayt
    b: u64,  // 8 bayt (7 bayt padding qo'shiladi)
    c: u8,   // 1 bayt (7 bayt padding qo'shiladi) -> Jami 24 bayt!
}

fn main() {
    println!("Tartibsiz struktura hajmi: {} bayt", std::mem::size_of::<Tartibsiz>());
}
```

## Tushuntirish va Mantiq:
Protsessorlar xotirani o'z so'z o'lchamiga moslab o'qiydi. Shuning uchun Rust xotirani tekislash (padding) orqali tezlikni ta'minlaydi.

## Ishlash natijasi:
```text
Tartibsiz struktura hajmi: 24 bayt
```

---

# 332-Topshiriq: C tili bilan mos xotira joylashuvi: #[repr(C)]
## Topshiriq sharti:
Struktura xotirasini aynan C tili qoidalari bo'yicha tekislang.

## Yechim (Rust kodi):
```rust
#[repr(C)]
struct CPaket {
    id: u16,
    bayroq: u8,
}

fn main() {
    println!("C-mos struktura hajmi: {} bayt", std::mem::size_of::<CPaket>());
}
```

## Tushuntirish va Mantiq:
`#[repr(C)]` atributi Rust kompilyatoriga maydonlarni C tili qoidalariga ko'ra joylashtirishni buyuradi. Bu operatsion tizim drayverlari va FFI uchun shart.

## Ishlash natijasi:
```text
C-mos struktura hajmi: 4 bayt
```

---

# 333-Topshiriq: Custom Display traiti implementatsiyasi struktura uchun
## Topshiriq sharti:
Strukturani `{}` orqali chiroyli formatda chop etish imkonini bering.

## Yechim (Rust kodi):
```rust
use std::fmt;

struct Valyuta {
    belgi: char,
    miqdor: f64,
}

impl fmt::Display for Valyuta {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}{:.2}", self.belgi, self.miqdor)
    }
}

fn main() {
    let narx = Valyuta { belgi: '$', miqdor: 49.99 };
    println!("Maxsulot narxi: {}", narx);
}
```

## Tushuntirish va Mantiq:
`fmt::Display` traiti implement qilingach, struktura to'g'ridan-to'g'ri `println!("{}")` bilan chiroyli chiqadi.

## Ishlash natijasi:
```text
Maxsulot narxi: $49.99
```

---

# 334-Topshiriq: Struktura orqali rang konvertori (HEX dan RGB ga)
## Topshiriq sharti:
HEX satridan RGB strukturasini hosil qiluvchi konstruktor yozing.

## Yechim (Rust kodi):
```rust
#[derive(Debug)]
struct Rgb {
    r: u8,
    g: u8,
    b: u8,
}

impl Rgb {
    fn hex_dan(hex: &str) -> Option<Self> {
        let toza = hex.trim_start_matches('#');
        if toza.len() != 6 { return None; }

        let r = u8::from_str_radix(&toza[0..2], 16).ok()?;
        let g = u8::from_str_radix(&toza[2..4], 16).ok()?;
        let b = u8::from_str_radix(&toza[4..6], 16).ok()?;

        Some(Self { r, g, b })
    }
}

fn main() {
    let rang = Rgb::hex_dan("#FF5733");
    println!("Olingan rang: {:?}", rang);
}
```

## Tushuntirish va Mantiq:
Konstruktor xatolik bo'lishi mumkin bo'lganda `Option<Self>` qaytarishi xavfsiz arxitektura tamoyilidir.

## Ishlash natijasi:
```text
Olingan rang: Some(Rgb { r: 255, g: 87, b: 51 })
```

---

# 335-Topshiriq: Doira strukturasi va perimetr, yuza hisoblari
## Topshiriq sharti:
Geometrik doira modelini to'liq metodlari bilan tuzing.

## Yechim (Rust kodi):
```rust
struct Doira {
    radius: f64,
}

impl Doira {
    fn new(radius: f64) -> Self { Self { radius } }
    fn yuza(&self) -> f64 { std::f64::consts::PI * self.radius * self.radius }
    fn perimetr(&self) -> f64 { 2.0 * std::f64::consts::PI * self.radius }
}

fn main() {
    let d = Doira::new(10.0);
    println!("Doira yuzi: {:.2}, Perimetri: {:.2}", d.yuza(), d.perimetr());
}
```

## Tushuntirish va Mantiq:
Konstruktor va matematik metodlar yordamida geometrik shakllar ixcham va xatosiz loyihalanadi.

## Ishlash natijasi:
```text
Doira yuzi: 314.16, Perimetri: 62.83
```

---

# 336-Topshiriq: Struktura ichida qidiruv: Kutubxona katalogi
## Topshiriq sharti:
Kitoblar ro'yxatini boshqaruvchi va qidiruvchi kutubxona tizimi.

## Yechim (Rust kodi):
```rust
struct Kitob {
    nomi: String,
    janr: String,
}

struct Kutubxona {
    kitoblar: Vec<Kitob>,
}

impl Kutubxona {
    fn janr_boyicha(&self, j: &str) -> Vec<&Kitob> {
        self.kitoblar.iter().filter(|k| k.janr == j).collect()
    }
}

fn main() {
    let kutubxona = Kutubxona {
        kitoblar: vec![
            Kitob { nomi: String::from("Shum bola"), janr: String::from("Qissa") },
            Kitob { nomi: String::from("O'tkan kunlar"), janr: String::from("Roman") },
            Kitob { nomi: String::from("Kecha va kunduz"), janr: String::from("Roman") },
        ],
    };

    let romanlar = kutubxona.janr_boyicha("Roman");
    println!("Romanlar soni: {}", romanlar.len());
}
```

## Tushuntirish va Mantiq:
Kutubxona metodlari havolalar vektorini qaytarib, ortiqcha xotira ko'chirmasdan qidiruvni ta'minlaydi.

## Ishlash natijasi:
```text
Romanlar soni: 2
```

---

# 337-Topshiriq: Strukturalar bilan Binar Daraxt Tuguni (Binary Tree Node)
## Topshiriq sharti:
Binar qidiruv daraxti tugunini `Box` orqali hosil qiling.

## Yechim (Rust kodi):
```rust
struct DaraxtTugun {
    qiymat: i32,
    chap: Option<Box<DaraxtTugun>>,
    ong: Option<Box<DaraxtTugun>>,
}

fn main() {
    let ildiz = DaraxtTugun {
        qiymat: 10,
        chap: Some(Box::new(DaraxtTugun { qiymat: 5, chap: None, ong: None })),
        ong: Some(Box::new(DaraxtTugun { qiymat: 15, chap: None, ong: None })),
    };

    println!("Ildiz: {}, Chap bola: {}", ildiz.qiymat, ildiz.chap.as_ref().unwrap().qiymat);
}
```

## Tushuntirish va Mantiq:
Daraxtsimon ma'lumot tuzilmalari `Option<Box<T>>` yordamida qat'iy va xavfsiz tarzda quriladi.

## Ishlash natijasi:
```text
Ildiz: 10, Chap bola: 5
```

---

# 338-Topshiriq: Struktura metodida o'zini iste'mol qilib (self) yangi qiymat qaytarish
## Topshiriq sharti:
Obyekt holatini qayta tiklab, yangi formatda chiqaruvchi metod.

## Yechim (Rust kodi):
```rust
struct O'lchov {
    metr: f64,
}

impl O'lchov {
    fn santimetrga(self) -> f64 {
        self.metr * 100.0
    }
}

fn main() {
    let olcham = O'lchov { metr: 2.5 };
    let sm = olcham.santimetrga();

    println!("2.5 metr = {} sm", sm);
}
```

## Tushuntirish va Mantiq:
`self` konsuming metodlari konvertatsiyalarda juda tabiiy ishlaydi: eski o'lchov o'chib, yangi natija hosil bo'ladi.

## Ishlash natijasi:
```text
2.5 metr = 250 sm
```

---

# 339-Topshiriq: Strukturalar uchun operatorlarni qayta yuklash (Add traiti)
## Topshiriq sharti:
`+` operatori yordamida ikkita nuqtani bir-biriga qo'shish.

## Yechim (Rust kodi):
```rust
use std::ops::Add;

#[derive(Debug, PartialEq)]
struct Vektor2D {
    x: f64,
    y: f64,
}

impl Add for Vektor2D {
    type Output = Self;

    fn add(self, boshqa: Self) -> Self::Output {
        Self { x: self.x + boshqa.x, y: self.y + boshqa.y }
    }
}

fn main() {
    let v1 = Vektor2D { x: 1.0, y: 2.0 };
    let v2 = Vektor2D { x: 3.0, y: 4.0 };
    let v3 = v1 + v2;

    println!("Vektorlar yig'indisi: {:?}", v3);
}
```

## Tushuntirish va Mantiq:
Rust da `std::ops::Add` traitini implement qilish orqali o'z strukturalaringiz ustida `+` arifmetik operatorini ishlatishingiz mumkin.

## Ishlash natijasi:
```text
Vektorlar yig'indisi: Vektor2D { x: 4.0, y: 6.0 }
```

---

# 340-Topshiriq: Massiv maydoniga ega bo'lgan strukturalar
## Topshiriq sharti:
Struktura ichida qat'iy massiv saqlab, uning o'rtacha qiymatini hisoblang.

## Yechim (Rust kodi):
```rust
struct BaholarJurnali {
    baholar: [u32; 4],
}

impl BaholarJurnali {
    fn ortacha(&self) -> f64 {
        let sum: u32 = self.baholar.iter().sum();
        sum as f64 / self.baholar.len() as f64
    }
}

fn main() {
    let j = BaholarJurnali { baholar: [85, 90, 95, 100] };
    println!("O'rtacha baho: {:.1}", j.ortacha());
}
```

## Tushuntirish va Mantiq:
Qat'iy massivlar Heap ga murojaat qilmaydi, shuning uchun butun struktura to'liq Stack da maksimal tezlikda ishlaydi.

## Ishlash natijasi:
```text
O'rtacha baho: 92.5
```

---

# 341-Topshiriq: Struktura bilan Oddiy Hisoblagich (Counter) modeli
## Topshiriq sharti:
Har chaqirilganda 1 ga oshadigan metod.

## Yechim (Rust kodi):
```rust
struct Sanagich {
    qiymat: u64,
}

impl Sanagich {
    fn yangi() -> Self { Self { qiymat: 0 } }
    fn qadam(&mut self) -> u64 {
        self.qiymat += 1;
        self.qiymat
    }
}

fn main() {
    let mut c = Sanagich::yangi();
    println!("1-qadam: {}", c.qadam());
    println!("2-qadam: {}", c.qadam());
    println!("3-qadam: {}", c.qadam());
}
```

## Tushuntirish va Mantiq:
Sanagich modeli inkrementatsiya vazifalarini toza va xavfsiz tarzda paketlaydi.

## Ishlash natijasi:
```text
1-qadam: 1
2-qadam: 2
3-qadam: 3
```

---

# 342-Topshiriq: Tarmoq paketi va Checksum hisoblash modeli
## Topshiriq sharti:
Ma'lumotlar yaxlitligini tekshiruvchi tarmoq paketi strukturasi.

## Yechim (Rust kodi):
```rust
struct Paket {
    id: u32,
    baytlar: Vec<u8>,
}

impl Paket {
    fn checksum(&self) -> u8 {
        self.baytlar.iter().fold(0, |acc, &b| acc ^ b)
    }
}

fn main() {
    let p = Paket { id: 1, baytlar: vec![10, 20, 30, 40] };
    println!("Paket #{} XOR checksum: {}", p.id, p.checksum());
}
```

## Tushuntirish va Mantiq:
Tarmoq protokollarida har bir paket o'zining checksum metodiga ega bo'lib, xatoliklarni aniqlaydi.

## Ishlash natijasi:
```text
Paket #1 XOR checksum: 20
```

---

# 343-Topshiriq: Struktura bilan Matritsa 2x2 va Determinant hisoblash
## Topshiriq sharti:
2x2 matritsaning determinantini aniqlovchi metod.

## Yechim (Rust kodi):
```rust
struct Matritsa2x2 {
    a: f64, b: f64,
    c: f64, d: f64,
}

impl Matritsa2x2 {
    fn determinant(&self) -> f64 {
        self.a * self.d - self.b * self.c
    }
}

fn main() {
    let m = Matritsa2x2 { a: 4.0, b: 2.0, c: 3.0, d: 5.0 };
    println!("Determinant: {}", m.determinant());
}
```

## Tushuntirish va Mantiq:
Chiziqli algebra hisoblari strukturalar orqali ixcham kodga aylanadi.

## Ishlash natijasi:
```text
Determinant: 14
```

---

# 344-Topshiriq: GPS koordinatasi va Ikki nuqta geografik yaqinligi
## Topshiriq sharti:
Kenglik va uzunlik bo'yicha nuqtalarni ifodalash.

## Yechim (Rust kodi):
```rust
struct GpsKoordinata {
    kenglik: f64,
    uzunlik: f64,
}

impl GpsKoordinata {
    fn bir_xilmi(&self, boshqa: &GpsKoordinata) -> bool {
        (self.kenglik - boshqa.kenglik).abs() < 0.0001 &&
        (self.uzunlik - boshqa.uzunlik).abs() < 0.0001
    }
}

fn main() {
    let p1 = GpsKoordinata { kenglik: 41.2995, uzunlik: 69.2401 }; // Toshkent
    let p2 = GpsKoordinata { kenglik: 41.2995, uzunlik: 69.2402 };

    println!("Bir xil manzilmi: {}", p1.bir_xilmi(&p2));
}
```

## Tushuntirish va Mantiq:
Suzuvchi sonlarni solishtirishda epsilon xatolik oralig'idan foydalanish amaliy standartdir.

## Ishlash natijasi:
```text
Bir xil manzilmi: true
```

---

# 345-Topshiriq: Struktura orqali Log xabarlarini boshqaruvchi (Logger)
## Topshiriq sharti:
Har xil darajadagi (INFO, WARN, ERROR) xabarlarni formatlab yozish.

## Yechim (Rust kodi):
```rust
struct OddiyLogger {
    tizim_nomi: String,
}

impl OddiyLogger {
    fn info(&self, xabar: &str) {
        println!("[{}] INFO: {}", self.tizim_nomi, xabar);
    }
    fn error(&self, xabar: &str) {
        println!("[{}] ERROR: {}", self.tizim_nomi, xabar);
    }
}

fn main() {
    let log = OddiyLogger { tizim_nomi: String::from("Billing") };
    log.info("To'lov qabul qilindi.");
    log.error("Ulanish uzildi!");
}
```

## Tushuntirish va Mantiq:
Logger obyektlari xizmat nomini o'zida saqlab, butun dastur bo'ylab xabarlarni bir xil formatda chiqaradi.

## Ishlash natijasi:
```text
[Billing] INFO: To'lov qabul qilindi.
[Billing] ERROR: Ulanish uzildi!
```

---

# 346-Topshiriq: Struktura orqali Binar hisoblagich (Flags)
## Topshiriq sharti:
Bit bayroqlarini struktura ichida o'rnatish va tekshirish.

## Yechim (Rust kodi):
```rust
struct Bayroqlar {
    holat: u8,
}

impl Bayroqlar {
    fn new() -> Self { Self { holat: 0 } }
    fn yoqish(&mut self, bit: u8) { self.holat |= 1 << bit; }
    fn tekshir(&self, bit: u8) -> bool { (self.holat & (1 << bit)) != 0 }
}

fn main() {
    let mut f = Bayroqlar::new();
    f.yoqish(2);

    println!("2-bit bormi: {}", f.tekshir(2));
    println!("3-bit bormi: {}", f.tekshir(3));
}
```

## Tushuntirish va Mantiq:
Strukturalar past darajadagi bit amallarini qulay va xavfsiz yuqori darajali metodlarga o'raydi.

## Ishlash natijasi:
```text
2-bit bormi: true
3-bit bormi: false
```

---

# 347-Topshiriq: Struktura bilan Valyuta hisobi (Valyutalar almashinuvi)
## Topshiriq sharti:
Valyutani ko'paytirish va boshqa kursga o'tkazish.

## Yechim (Rust kodi):
```rust
struct Valyuta {
    qiymat: f64,
    birlik: String,
}

impl Valyuta {
    fn usd_to_uzs(&self) -> Self {
        assert_eq!(self.birlik, "USD");
        Self { qiymat: self.qiymat * 12800.0, birlik: String::from("UZS") }
    }
}

fn main() {
    let dollar = Valyuta { qiymat: 50.0, birlik: String::from("USD") };
    let som = dollar.usd_to_uzs();

    println!("{:.0} {}", som.qiymat, som.birlik);
}
```

## Tushuntirish va Mantiq:
Strukturalar pul miqdori bilan uning birligini har doim birga olib yurishni ta'minlaydi.

## Ishlash natijasi:
```text
640000 UZS
```

---

# 348-Topshiriq: Struktura bilan Xarid cheki (Receipt Generator)
## Topshiriq sharti:
Xarid elementlarini qo'shib yakuniy chek chiqarish.

## Yechim (Rust kodi):
```rust
struct Chek {
    dokon: String,
    summa: f64,
}

impl Chek {
    fn yangi(dokon: &str) -> Self { Self { dokon: dokon.to_string(), summa: 0.0 } }
    fn xarid(&mut self, narx: f64) { self.summa += narx; }
    fn chop(&self) {
        println!("*** {} ***\nJami to'lov: ${:.2}", self.dokon, self.summa);
    }
}

fn main() {
    let mut c = Chek::yangi("Supermarket");
    c.xarid(12.50);
    c.xarid(37.50);
    c.chop();
}
```

## Tushuntirish va Mantiq:
Sodda metodlar kombinatsiyasi orqali hisob-kitoblar aniq nazorat qilinadi.

## Ishlash natijasi:
```text
*** Supermarket ***
Jami to'lov: $50.00
```

---

# 349-Topshiriq: Struktura bilan Foydalanuvchi huquqlari (RBAC) modeli
## Topshiriq sharti:
Foydalanuvchining roli va ruxsatlarini tekshiruvchi domen struktura.

## Yechim (Rust kodi):
```rust
struct Huquq {
    rol: String,
}

impl Huquq {
    fn adminmi(&self) -> bool { self.rol == "admin" }
    fn tahrirlay_oladimi(&self) -> bool { self.rol == "admin" || self.rol == "editor" }
}

fn main() {
    let h1 = Huquq { rol: String::from("editor") };
    println!("Adminmi: {}", h1.adminmi());
    println!("Tahrirlay oladimi: {}", h1.tahrirlay_oladimi());
}
```

## Tushuntirish va Mantiq:
Xavfsizlik rollarini struktura orqali boshqarish tizimdagi ruxsatnomalar mantiqini mustahkamlaydi.

## Ishlash natijasi:
```text
Adminmi: false
Tahrirlay oladimi: true
```

---

# 350-Topshiriq: Strukturalar va metodlar moduli xulosasi
## Topshiriq sharti:
Rust da ma'lumotlar va metodlarning toza ajratilishi haqida xulosa.

## Yechim (Rust kodi):
```rust
fn main() {
    println!("=== RUST STRUCTS VA METODLAR XULOSASI ===");
    println!("1. Struct faqat ma'lumotlarni saqlaydi, impl esa ularning metodlarini.");
    println!("2. &self (o'qish), &mut self (o'zgartirish), self (iste'mol qilish).");
    println!("3. Newtype va Tuple strukturalar tip xavfsizligini oshiradi.");
    println!("4. Enkapsulyatsiya (private maydonlar + getter/setter) ma'lumotlar yaxlitligini kafolatlaydi.");
    println!("5. Derive makrolari kod takrorlanishini 80% ga qisqartiradi.");
}
```

## Tushuntirish va Mantiq:
Rust obyektga yo'naltirilgan dasturlashdagi merosxo'rlik (inheritance) muammolaridan qochib, kompozitsiya va metodlar orqali toza modellashtirishni ta'minlaydi.

## Ishlash natijasi:
```text
=== RUST STRUCTS VA METODLAR XULOSASI ===
1. Struct faqat ma'lumotlarni saqlaydi, impl esa ularning metodlarini.
2. &self (o'qish), &mut self (o'zgartirish), self (iste'mol qilish).
3. Newtype va Tuple strukturalar tip xavfsizligini oshiradi.
4. Enkapsulyatsiya (private maydonlar + getter/setter) ma'lumotlar yaxlitligini kafolatlaydi.
5. Derive makrolari kod takrorlanishini 80% ga qisqartiradi.
```

---
