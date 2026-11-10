# 9-Qism: Xatolar bilan Ishlash: Result, Option va Panic (401-450)

Ushbu qismda Rust dasturlash tilidagi xatoliklarni boshqarish falsafasi: tiklanmaydigan xatolar (`panic!`, `unreachable!`, `todo!`), tiklanadigan xatolar (`Result<T, E>`), qudratli `?` (savol belgisi) operatori, maxsus xato turlari va enumlari, `std::error::Error` va `From` traiti, xatolar zanjiri (error chaining) hamda xatolarni kombinatorlar (`map`, `and_then`, `or_else`) orqali qayta ishlash o'rganiladi.

---

# 401-Topshiriq: Rust xatolar falsafasi: Tiklanmaydigan vs Tiklanadigan
## Topshiriq sharti:
Rust da xatolar qanday ikkiga bo'linishini kod va izohlar bilan tushuntiring.

## Yechim (Rust kodi):
```rust
fn main() {
    // 1. Tiklanmaydigan (Unrecoverable): dastur davom eta olmaydigan kritik holat -> panic!
    // 2. Tiklanadigan (Recoverable): kutilgan va to'g'irlash mumkin bo'lgan holat -> Result<T, E>

    let son_satr = "123";
    match son_satr.parse::<i32>() {
        Ok(son) => println!("Tiklanadigan muvaffaqiyat: {}", son),
        Err(e) => println!("Xatoni to'g'irlash mumkin: {}", e),
    }
}
```

## Tushuntirish va Mantiq:
Boshqa tillardagi noaniq `try-catch` istisnolari o'rniga, Rust barcha kutilgan xatolarni aniq tur (`Result`) sifatida qaytarishni majburiy qiladi.

## Ishlash natijasi:
```text
Tiklanadigan muvaffaqiyat: 123
```

---

# 402-Topshiriq: panic! makrosi va dasturning to'xtashi
## Topshiriq sharti:
Kritik holatda dasturni `panic!` orqali to'xtatishni namoyish eting.

## Yechim (Rust kodi):
```rust
fn tekshir_yosh(yosh: i32) {
    if yosh < 0 {
        panic!("Halokatli xato: Yosh manfiy bo'lishi mumkin emas ({})!", yosh);
    }
    println!("Yaroqli yosh: {}", yosh);
}

fn main() {
    tekshir_yosh(25);
    // tekshir_yosh(-5); // Bu chaqiruv dasturni to'xtatadi
}
```

## Tushuntirish va Mantiq:
`panic!` dastur xotirasini tozalab (unwinding), terminalga xato xabarini va qator raqamini chiqaradi hamda dasturni darhol to'xtatadi.

## Ishlash natijasi:
```text
Yaroqli yosh: 25
```

---

# 403-Topshiriq: unreachable! makrosi: Yetib borilmaydigan kodni belgilash
## Topshiriq sharti:
Mantiqan hech qachon ishga tushmasligi kerak bo'lgan tarmoqqa `unreachable!` qo'ying.

## Yechim (Rust kodi):
```rust
fn fasl_oy_kunlari(oy: u32) -> u32 {
    match oy {
        1 | 3 | 5 | 7 | 8 | 10 | 12 => 31,
        4 | 6 | 9 | 11 => 30,
        2 => 28,
        _ => unreachable!("Oy har doim 1 dan 12 gacha bo'lishi kerak!"),
    }
}

fn main() {
    println!("Mart oyi kunlari: {}", fasl_oy_kunlari(3));
}
```

## Tushuntirish va Mantiq:
`unreachable!` kompilyatorga bu nuqtaga hech qachon yetib kelinmasligini bildiradi. Agar dasturchi xatoga yo'l qo'ygan bo'lsa, u darhol panic beradi.

## Ishlash natijasi:
```text
Mart oyi kunlari: 31
```

---

# 404-Topshiriq: todo! va unimplemented! makrolari
## Topshiriq sharti:
Kodni loyihalashda hali yozilmagan funksiyalarga vaqtinchalik joy qoldiring.

## Yechim (Rust kodi):
```rust
fn murakkab_neyrotarmoq_qatlami() -> f64 {
    // Kelajakda yoziladigan kod o'rniga:
    todo!("SIMD asosidagi 1-bit matritsa hisoblash algoritmi kiritilsin")
}

fn main() {
    println!("Dastur boshlandi.");
    // murakkab_neyrotarmoq_qatlami(); // Chaqirilsa, todo! xabari chiqadi
}
```

## Tushuntirish va Mantiq:
`todo!` va `unimplemented!` funksiya imzolarini tayyorlab qo'yib, kodni bosqichma-bosqich yozishda eng qulay vositadir.

## Ishlash natijasi:
```text
Dastur boshlandi.
```

---

# 405-Topshiriq: Result<T, E> enumi: Ok va Err variantlari
## Topshiriq sharti:
Bo'lish amalida xatoni `Result` orqali qaytaruvchi funksiya yozing.

## Yechim (Rust kodi):
```rust
fn xavfsiz_bolish(a: f64, b: f64) -> Result<f64, String> {
    if b == 0.0 {
        Err(String::from("Nolga bo'lish mumkin emas!"))
    } else {
        Ok(a / b)
    }
}

fn main() {
    match xavfsiz_bolish(10.0, 2.0) {
        Ok(javob) => println!("Natija: {}", javob),
        Err(xato) => println!("Xatolik: {}", xato),
    }

    match xavfsiz_bolish(10.0, 0.0) {
        Ok(javob) => println!("Natija: {}", javob),
        Err(xato) => println!("Xatolik: {}", xato),
    }
}
```

## Tushuntirish va Mantiq:
`Result<T, E>` ikkita variantga ega: `Ok(T)` (muvaffaqiyat) va `Err(E)` (xatolik sababi).

## Ishlash natijasi:
```text
Natija: 5
Xatolik: Nolga bo'lish mumkin emas!
```

---

# 406-Topshiriq: unwrap() va uning xavfi
## Topshiriq sharti:
`unwrap()` qanday ishlashini va nega ishlab chiqarishda ehtiyotkorlik talab qilishini ko'rsating.

## Yechim (Rust kodi):
```rust
fn main() {
    let yaxshi_natija: Result<i32, &str> = Ok(100);
    println!("Qiymat: {}", yaxshi_natija.unwrap());

    // let xato_natija: Result<i32, &str> = Err("Tarmoq xatosi");
    // xato_natija.unwrap(); // Dasturni to'g'ridan-to'g'ri PANIC qilib yuboradi!
}
```

## Tushuntirish va Mantiq:
`unwrap()` agar qiymat `Ok` bo'lsa uni ochadi, agar `Err` bo'lsa dasturni darhol to'xtatadi. Uni faqat 100% ishonchli testlarda ishlatish tavsiya etiladi.

## Ishlash natijasi:
```text
Qiymat: 100
```

---

# 407-Topshiriq: expect() metodi: Ma'noli xato xabari berish
## Topshiriq sharti:
Panic yuz berganda aynan qayerda nima bo'lganini tushuntiruvchi xabar bering.

## Yechim (Rust kodi):
```rust
fn main() {
    let son_matn = "42";
    let son = son_matn.parse::<i32>().expect("Konfiguratsiya porti butun son bo'lishi shart!");

    println!("O'qilgan port: {}", son);
}
```

## Tushuntirish va Mantiq:
`expect(xabar)` metodi `unwrap` ga o'xshaydi, lekin panic paytida aynan dasturchi bergan ma'noli xabarni chop etadi.

## Ishlash natijasi:
```text
O'qilgan port: 42
```

---

# 408-Topshiriq: unwrap_or() orqali zaxira qiymat berish
## Topshiriq sharti:
Xatolik yuz berganda xavfsiz boshlang'ich qiymatga o'ting.

## Yechim (Rust kodi):
```rust
fn main() {
    let xato_port = "sakson_sakson".parse::<u16>().unwrap_or(8080);
    let togri_port = "9000".parse::<u16>().unwrap_or(8080);

    println!("Xato holatda: {}", xato_port);
    println!("To'g'ri holatda: {}", togri_port);
}
```

## Tushuntirish va Mantiq:
`unwrap_or(default)` xatolik yuz berganda dasturni to'xtatmasdan, ko'rsatilgan zaxira qiymatni qaytaradi.

## Ishlash natijasi:
```text
Xato holatda: 8080
To'g'ri holatda: 9000
```

---

# 409-Topshiriq: unwrap_or_else() bilan hisoblanuvchi muqobil harakat
## Topshiriq sharti:
Xatolik sababini ko'rib, shunga qarab qiymat hisoblang.

## Yechim (Rust kodi):
```rust
fn main() {
    let matn = "not_a_number";
    let qiymat = matn.parse::<i32>().unwrap_or_else(|e| {
        println!("Parse xatosi ({}), standart 0 qiymati olindi.", e);
        0
    });

    println!("Yakuniy qiymat: {}", qiymat);
}
```

## Tushuntirish va Mantiq:
`unwrap_or_else(|err| ...)` xato obyektini closurega uzatadi va xatolikni log qilib, yangi qiymat qaytarishga imkon beradi.

## Ishlash natijasi:
```text
Parse xatosi (invalid digit found in string), standart 0 qiymati olindi.
Yakuniy qiymat: 0
```

---

# 410-Topshiriq: ? (Savol belgisi) operatori: Xatolarni erta uzatish (Error Propagation)
## Topshiriq sharti:
`?` operatori yordamida bir necha qadamli xatolarni bitta qatorda uzating.

## Yechim (Rust kodi):
```rust
fn kvadrat_ildiz_ol(matn: &str) -> Result<f64, String> {
    let son: f64 = matn.parse().map_err(|_| String::from("Raqamga aylantirib bo'lmadi"))?;

    if son < 0.0 {
        return Err(String::from("Manfiy sondan ildiz olib bo'lmaydi"));
    }

    Ok(son.sqrt())
}

fn main() {
    println!("Natija 1: {:?}", kvadrat_ildiz_ol("25.0"));
    println!("Natija 2: {:?}", kvadrat_ildiz_ol("abc"));
    println!("Natija 3: {:?}", kvadrat_ildiz_ol("-9.0"));
}
```

## Tushuntirish va Mantiq:
`?` operatori agar natija `Ok` bo'lsa ichidagi qiymatni chiqarib beradi, agar `Err` bo'lsa darhol funksiyadan o'sha xatoni `return` qiladi.

## Ishlash natijasi:
```text
Natija 1: Ok(5.0)
Natija 2: Err("Raqamga aylantirib bo'lmadi")
Natija 3: Err("Manfiy sondan ildiz olib bo'lmaydi")
```

---

# 411-Topshiriq: main funksiyasidan Result qaytarish
## Topshiriq sharti:
`fn main() -> Result<(), E>` orqali `main` ichida ham `?` operatorini qo'llang.

## Yechim (Rust kodi):
```rust
fn main() -> Result<(), Box<dyn std::error::Error>> {
    let son_matn = "1024";
    let son: u32 = son_matn.parse()?;

    println!("Muvaffaqiyatli o'qildi: {}", son);
    Ok(())
}
```

## Tushuntirish va Mantiq:
Rust da `main` funksiyasi ham `Result<(), E>` qaytara oladi. Bu xatoliklarni asosiy kirish nuqtasida juda qisqa boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Muvaffaqiyatli o'qildi: 1024
```

---

# 412-Topshiriq: Maxsus xato enumi (Custom Error Enum) yaratish
## Topshiriq sharti:
Loyihangizdagi barcha xatolarni bitta enumga birlashtiring.

## Yechim (Rust kodi):
```rust
#[derive(Debug)]
enum FoydalanuvchiXatosi {
    IsmBosh,
    YoshJudaKichik(u8),
    ParolXavfsizEmas,
}

fn royxatdan_otish(ism: &str, yosh: u8, parol: &str) -> Result<(), FoydalanuvchiXatosi> {
    if ism.trim().is_empty() {
        return Err(FoydalanuvchiXatosi::IsmBosh);
    }
    if yosh < 16 {
        return Err(FoydalanuvchiXatosi::YoshJudaKichik(yosh));
    }
    if parol.len() < 6 {
        return Err(FoydalanuvchiXatosi::ParolXavfsizEmas);
    }
    Ok(())
}

fn main() {
    println!("{:?}", royxatdan_otish("", 20, "parol123"));
    println!("{:?}", royxatdan_otish("Ali", 12, "parol123"));
    println!("{:?}", royxatdan_otish("Vali", 18, "parol123"));
}
```

## Tushuntirish va Mantiq:
Maxsus xato enumlari har bir xatolik holatini qat'iy tiplashtiradi va chaqiruvchiga har bir xato sababini aniq ko'rsatadi.

## Ishlash natijasi:
```text
Err(IsmBosh)
Err(YoshJudaKichik(12))
Ok(())
```

---

# 413-Topshiriq: Display traitini maxsus xato uchun implement qilish
## Topshiriq sharti:
Xato xabarini foydalanuvchiga tushunarli matn sifatida chiqaring.

## Yechim (Rust kodi):
```rust
use std::fmt;

#[derive(Debug)]
enum AppXato {
    FaylTopilmadi(String),
    RuxsatYoq,
}

impl fmt::Display for AppXato {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            AppXato::FaylTopilmadi(nom) => write!(f, "Fayl tizimda mavjud emas: '{}'", nom),
            AppXato::RuxsatYoq => write!(f, "Ushbu amalni bajarishga huquq yetarli emas!"),
        }
    }
}

fn main() {
    let xato = AppXato::FaylTopilmadi(String::from("config.json"));
    println!("Xatolik tavsifi: {}", xato);
}
```

## Tushuntirish va Mantiq:
`Display` traiti xatoning inson tushunadigan shaklini ifodalaydi va `std::error::Error` ning talabidir.

## Ishlash natijasi:
```text
Xatolik tavsifi: Fayl tizimda mavjud emas: 'config.json'
```

---

# 414-Topshiriq: std::error::Error traitini ulash
## Topshiriq sharti:
O'z xato turingizni Rust ning standart xatolar ekotizimiga qo'shing.

## Yechim (Rust kodi):
```rust
use std::fmt;
use std::error::Error;

#[derive(Debug)]
struct OddiyXato {
    kod: u32,
}

impl fmt::Display for OddiyXato {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "Xato kodi: #{}", self.kod)
    }
}

impl Error for OddiyXato {}

fn main() {
    let e = OddiyXato { kod: 404 };
    let xato_ob: &dyn Error = &e;

    println!("Standart xato: {}", xato_ob);
}
```

## Tushuntirish va Mantiq:
`impl Error for T {}` bo'sh implementatsiyasi xatoni `Box<dyn Error>` sifatida ishlatish imkonini beradi.

## Ishlash natijasi:
```text
Standart xato: Xato kodi: #404
```

---

# 415-Topshiriq: From traiti orqali xatolarni avtomatik konvertatsiya qilish
## Topshiriq sharti:
`ParseIntError` ni o'z maxsus xato turingizga avtomatik o'tkazing.

## Yechim (Rust kodi):
```rust
use std::num::ParseIntError;

#[derive(Debug)]
enum MeningXatom {
    SonXatosi(ParseIntError),
}

impl From<ParseIntError> for MeningXatom {
    fn from(e: ParseIntError) -> Self {
        MeningXatom::SonXatosi(e)
    }
}

fn sonni_oqish(matn: &str) -> Result<i32, MeningXatom> {
    let son = matn.parse::<i32>()?; // ? operatori avtomatik From::from ni chaqiradi!
    Ok(son)
}

fn main() {
    println!("Natija: {:?}", sonni_oqish("100"));
    println!("Xato:   {:?}", sonni_oqish("xato"));
}
```

## Tushuntirish va Mantiq:
`From` traiti implement qilinganda `?` operatori uchinchi tomon xatolarini avtomatik ravishda loyiha xato turiga o'giradi.

## Ishlash natijasi:
```text
Natija: Ok(100)
Xato:   Err(SonXatosi(ParseIntError { kind: InvalidDigit }))
```

---

# 416-Topshiriq: Result::map() orqali Ok qiymatini o'zgartirish
## Topshiriq sharti:
Xatoga teginmasdan, faqat muvaffaqiyatli qiymatni o'zgartiring.

## Yechim (Rust kodi):
```rust
fn hisobla(s: &str) -> Result<i32, std::num::ParseIntError> {
    s.parse::<i32>().map(|n| n * 10)
}

fn main() {
    println!("Muvaffaqiyat: {:?}", hisobla("5"));
    println!("Xatolik:      {:?}", hisobla("salom"));
}
```

## Tushuntirish va Mantiq:
`Result::map` faqat `Ok` bo'lganda ishlaydi va natijani yangi `Ok` ga o'raydi. `Err` bo'lsa o'zgarishsiz qoladi.

## Ishlash natijasi:
```text
Muvaffaqiyat: Ok(50)
Xatolik:      Err(ParseIntError { kind: InvalidDigit })
```

---

# 417-Topshiriq: Result::map_err() orqali xato turini o'zgartirish
## Topshiriq sharti:
Muvaffaqiyatga teginmasdan, faqat xato matnini yangilang.

## Yechim (Rust kodi):
```rust
fn oqish(s: &str) -> Result<i32, String> {
    s.parse::<i32>().map_err(|e| format!("Xato yuz berdi: {}", e))
}

fn main() {
    println!("Natija: {:?}", oqish("abc"));
}
```

## Tushuntirish va Mantiq:
`map_err()` xatoni qulayroq yoki loyiha talablariga mos formatga o'tkazishda ishlatiladi.

## Ishlash natijasi:
```text
Natija: Err("Xato yuz berdi: invalid digit found in string")
```

---

# 418-Topshiriq: Result::and_then() orqali operatsiyalarni zanjirlash
## Topshiriq sharti:
Ketma-ket ikkita `Result` qaytaruvchi amalni bajaring.

## Yechim (Rust kodi):
```rust
fn parse_qil(s: &str) -> Result<i32, &str> {
    s.parse::<i32>().map_err(|_| "Raqam emas")
}

fn musbatmi(n: i32) -> Result<i32, &str> {
    if n > 0 { Ok(n) } else { Err("Musbat emas") }
}

fn main() {
    let res = parse_qil("50").and_then(musbatmi);
    println!("Zanjir natijasi: {:?}", res);

    let res_xato = parse_qil("-5").and_then(musbatmi);
    println!("Zanjir xatosi: {:?}", res_xato);
}
```

## Tushuntirish va Mantiq:
`and_then()` har bir qadam muvaffaqiyatli bo'lsagina keyingisiga o'tadi.

## Ishlash natijasi:
```text
Zanjir natijasi: Ok(50)
Zanjir xatosi: Err("Musbat emas")
```

---

# 419-Topshiriq: Result::or_else() orqali xatolikni ushlab muqobil Result sinash
## Topshiriq sharti:
Birinchi manzil ishlamasa, zaxira manzil orqali sinab ko'ring.

## Yechim (Rust kodi):
```rust
fn zaxira_bilan(birinchi: &str, zaxira: &str) -> Result<i32, &str> {
    birinchi.parse::<i32>()
        .map_err(|_| "1-manba xato")
        .or_else(|_| zaxira.parse::<i32>().map_err(|_| "2-manba ham xato"))
}

fn main() {
    println!("Natija: {:?}", zaxira_bilan("not_valid", "200"));
}
```

## Tushuntirish va Mantiq:
`or_else()` agar birinchi amal `Err` bersa, muqobil ikkinchi Result amalini ishga tushiradi.

## Ishlash natijasi:
```text
Natija: Ok(200)
```

---

# 420-Topshiriq: Option::ok_or() orqali Option dan Result ga o'tish
## Topshiriq sharti:
`None` uchraganda xato xabari hosil qiling.

## Yechim (Rust kodi):
```rust
fn main() {
    let element: Option<i32> = None;
    let res: Result<i32, &str> = element.ok_or("Element mavjud emas!");

    println!("Result ga o'girildi: {:?}", res);
}
```

## Tushuntirish va Mantiq:
`ok_or` `None` ni aniq xatoga ega `Err` ga aylantiradi.

## Ishlash natijasi:
```text
Result ga o'girildi: Err("Element mavjud emas!")
```

---

# 421-Topshiriq: Result::ok() orqali xatoni e'tiborsiz qoldirib Option ga o'tish
## Topshiriq sharti:
Xato sababi qiziq bo'lmaganda `Result` ni `Option` ga o'tkazing.

## Yechim (Rust kodi):
```rust
fn main() {
    let r1: Result<i32, &str> = Ok(42);
    let r2: Result<i32, &str> = Err("Tarmoq uzildi");

    println!("Ok dan Option:  {:?}", r1.ok());
    println!("Err dan Option: {:?}", r2.ok());
}
```

## Tushuntirish va Mantiq:
`r.ok()` amali `Ok(T)` ni `Some(T)` ga, har qanday `Err` ni esa `None` ga aylantiradi.

## Ishlash natijasi:
```text
Ok dan Option:  Some(42)
Err dan Option: None
```

---

# 422-Topshiriq: Result is_ok() va is_err() tekshiruvlari
## Topshiriq sharti:
Tezkor mantiqiy tekshiruvlarni bajaring.

## Yechim (Rust kodi):
```rust
fn main() {
    let res: Result<i32, &str> = Ok(10);

    println!("Muvaffaqiyatlimi: {}", res.is_ok());
    println!("Xatolikmi:        {}", res.is_err());
}
```

## Tushuntirish va Mantiq:
`is_ok()` va `is_err()` qiymatni ochmasdan turib uning holatini `bool` sifatida beradi.

## Ishlash natijasi:
```text
Muvaffaqiyatlimi: true
Xatolikmi:        false
```

---

# 423-Topshiriq: Bank hisobidan mablag' yechish xatolari modeli
## Topshiriq sharti:
Balans yetarli emasligi va hisob bloklanganligi xatolari.

## Yechim (Rust kodi):
```rust
#[derive(Debug)]
enum BankXatosi {
    MablagYetarliEmas { balans: f64, soralgan: f64 },
    HisobBloklangan,
}

struct Hisob { balans: f64, bloklangan: bool }

impl Hisob {
    fn yechish(&mut self, summa: f64) -> Result<(), BankXatosi> {
        if self.bloklangan {
            return Err(BankXatosi::HisobBloklangan);
        }
        if self.balans < summa {
            return Err(BankXatosi::MablagYetarliEmas { balans: self.balans, soralgan: summa });
        }
        self.balans -= summa;
        Ok(())
    }
}

fn main() {
    let mut h = Hisob { balans: 100.0, bloklangan: false };
    println!("{:?}", h.yechish(150.0));
}
```

## Tushuntirish va Mantiq:
Boy ma'lumotli xato variantlari qancha balans borligi va qancha so'ralganini aniq ko'rsatadi.

## Ishlash natijasi:
```text
Err(MablagYetarliEmas { balans: 100.0, soralgan: 150.0 })
```

---

# 424-Topshiriq: Box<dyn Error> orqali universal xatolar boshqaruvi
## Topshiriq sharti:
Har xil turdagi xatolarni bitta dinamik trait obyekti orqali qaytaring.

## Yechim (Rust kodi):
```rust
use std::error::Error;

fn bir_necha_xato(matn: &str) -> Result<i32, Box<dyn Error>> {
    let son: i32 = matn.parse()?; // ParseIntError avtomatik Box<dyn Error> ga o'tadi
    Ok(son * 2)
}

fn main() {
    println!("{:?}", bir_necha_xato("15"));
    println!("{:?}", bir_necha_xato("xato"));
}
```

## Tushuntirish va Mantiq:
`Box<dyn Error>` prototiplashda har xil turdagi barcha xatolarni bitta umumiy nom ostida yig'ishning eng tez yo'lidir.

## Ishlash natijasi:
```text
Ok(30)
Err(ParseIntError { kind: InvalidDigit })
```

---

# 425-Topshiriq: std::panic::catch_unwind orqali Panic ni ushlab qolish
## Topshiriq sharti:
Kritik qismdagi panic ni ushlab, dasturning qolgan qismi ishlashini ta'minlang.

## Yechim (Rust kodi):
```rust
use std::panic;

fn xavfli_amal() {
    panic!("Kutilmagan halokat!");
}

fn main() {
    let natija = panic::catch_unwind(|| {
        xavfli_amal();
    });

    if natija.is_err() {
        println!("Panic ushlab qolindi! Tizim normal ishlashda davom etadi.");
    }
}
```

## Tushuntirish va Mantiq:
`catch_unwind` serverlar va ko'p oqimli tizimlarda bitta oqimdagi xato butun dasturni to'xtatib qo'ymasligi uchun ishlatiladi.

## Ishlash natijasi:
```text
Panic ushlab qolindi! Tizim normal ishlashda davom etadi.
```

---

# 426-Topshiriq: Vec<Result<T, E>> ni Result<Vec<T>, E> ga bitta collect() bilan o'girish
## Topshiriq sharti:
Agar ro'yxatda bitta ham xato bo'lsa butun ro'yxatni `Err` qilish.

## Yechim (Rust kodi):
```rust
fn main() {
    let satrlar = vec!["10", "20", "30"];
    let sonlar: Result<Vec<i32>, _> = satrlar.iter().map(|s| s.parse::<i32>()).collect();
    println!("Hammasi to'g'ri: {:?}", sonlar);

    let aralash = vec!["10", "xato", "30"];
    let natija_xato: Result<Vec<i32>, _> = aralash.iter().map(|s| s.parse::<i32>()).collect();
    println!("Biri xato bo'lsa: {:?}", natija_xato);
}
```

## Tushuntirish va Mantiq:
Rust ning `collect()` metodi sehrli xususiyatga ega: u `Iterator<Item = Result<T, E>>` dan to'g'ridan-to'g'ri `Result<Vec<T>, E>` hosil qila oladi.

## Ishlash natijasi:
```text
Hammasi to'g'ri: Ok([10, 20, 30])
Biri xato bo'lsa: Err(ParseIntError { kind: InvalidDigit })
```

---

# 427-Topshiriq: Result::as_ref() orqali ichki qiymatga havola olish
## Topshiriq sharti:
`Result<T, E>` egasligini bermasdan uning ichidagi `&T` ni o'qish.

## Yechim (Rust kodi):
```rust
fn main() {
    let res: Result<String, ()> = Ok(String::from("Muhim matn"));

    let res_ref: Result<&String, &()> = res.as_ref();
    println!("Havola orqali o'qildi: {:?}", res_ref);
    println!("Asl Result hali ham yaroqli: {:?}", res);
}
```

## Tushuntirish va Mantiq:
`as_ref()` ichki qiymatni Move qilmasdan, unga havola hosil qiladi.

## Ishlash natijasi:
```text
Havola orqali o'qildi: Ok("Muhim matn")
Asl Result hali ham yaroqli: Ok("Muhim matn")
```

---

# 428-Topshiriq: Tranzaksiya va Rollback (Orqaga qaytish) modeli
## Topshiriq sharti:
Xato yuz berganda avvalgi holatni saqlab qoluvchi tranzaksiya.

## Yechim (Rust kodi):
```rust
struct Hamyon { balans: i32 }

fn pul_otkazish(jo'natuvchi: &mut Hamyon, qabul_qiluvchi: &mut Hamyon, summa: i32) -> Result<(), &'static str> {
    if jo'natuvchi.balans < summa {
        return Err("Mablag' yetarli emas!");
    }
    // Tranzaksiya
    jo'natuvchi.balans -= summa;
    qabul_qiluvchi.balans += summa;
    Ok(())
}

fn main() {
    let mut h1 = Hamyon { balans: 50 };
    let mut h2 = Hamyon { balans: 20 };

    let res = pul_otkazish(&mut h1, &mut h2, 100);
    println!("Natija: {:?}", res);
    println!("H1 balansi: {}, H2 balansi: {}", h1.balans, h2.balans);
}
```

## Tushuntirish va Mantiq:
Xatolik erta aniqlanib tranzaksiya to'xtatiladi va hisoblar o'zgarmasdan qoladi.

## Ishlash natijasi:
```text
Natija: Err("Mablag' yetarli emas!")
H1 balansi: 50, H2 balansi: 20
```

---

# 429-Topshiriq: Foydalanuvchi ma'lumotlarini tekshiruvchi Validator zanjiri
## Topshiriq sharti:
Bir nechta shartlarni ketma-ket `?` bilan tekshirish.

## Yechim (Rust kodi):
```rust
fn parol_tekshir(p: &str) -> Result<(), &'static str> {
    if p.len() < 8 { return Err("Parol kamida 8 belgidan iborat bo'lishi kerak"); }
    if !p.chars().any(|c| c.is_numeric()) { return Err("Parolda kamida bitta raqam bo'lishi shart"); }
    Ok(())
}

fn main() {
    println!("{:?}", parol_tekshir("qisqa"));
    println!("{:?}", parol_tekshir("harflarfaqat"));
    println!("{:?}", parol_tekshir("maxfiy123"));
}
```

## Tushuntirish va Mantiq:
Har bir xato o'z vaqtida ushlanadi va foydalanuvchiga aniq tushuntirish beriladi.

## Ishlash natijasi:
```text
Err("Parol kamida 8 belgidan iborat bo'lishi kerak")
Err("Parolda kamida bitta raqam bo'lishi shart")
Ok(())
```

---

# 430-Topshiriq: Result va xatolar moduli xulosasi
## Topshiriq sharti:
Rust da ishonchli dasturiy ta'minot qurish tamoyillari.

## Yechim (Rust kodi):
```rust
fn main() {
    println!("=== RUST XATOLARNI BOSHQARISH XULOSASI ===");
    println!("1. panic! - faqat tuzatib bo'lmaydigan dasturchi xatolari uchun.");
    println!("2. Result<T, E> - barcha biznes mantiqdagi xatolarni ifodalaydi.");
    println!("3. ? operatori xatolarni erta uzatishni soddalashtiradi.");
    println!("4. Maxsus xato enumlari har bir xatolik turini qat'iy nazorat qiladi.");
    println!("5. unwrap_or, map, and_then xatolarni xavfsiz kombinatsiyalashni ta'minlaydi.");
}
```

## Tushuntirish va Mantiq:
Rust ning xatolar bilan ishlash tizimi dasturlarni dunyodagi eng ishonchli va barqaror tizimlarga aylantiradi.

## Ishlash natijasi:
```text
=== RUST XATOLARNI BOSHQARISH XULOSASI ===
1. panic! - faqat tuzatib bo'lmaydigan dasturchi xatolari uchun.
2. Result<T, E> - barcha biznes mantiqdagi xatolarni ifodalaydi.
3. ? operatori xatolarni erta uzatishni soddalashtiradi.
4. Maxsus xato enumlari har bir xatolik turini qat'iy nazorat qiladi.
5. unwrap_or, map, and_then xatolarni xavfsiz kombinatsiyalashni ta'minlaydi.
```

---

# 431-Topshiriq: unwrap_or_default() bilan xavfsiz ochish
## Topshiriq sharti:
Xato yuz berganda tur uchun standart Default qiymatni olish.

## Yechim (Rust kodi):
```rust
fn main() {
    let r: Result<i32, &str> = Err("Noma'lum xato");
    let val = r.unwrap_or_default();

    println!("Qiymat: {}", val);
}
```

## Tushuntirish va Mantiq:
`unwrap_or_default()` sonlar uchun 0, satrlar uchun bo'sh matn qaytaradi.

## Ishlash natijasi:
```text
Qiymat: 0
```

---

# 432-Topshiriq: Result ichidagi havolalarni nusxalash: cloned()
## Topshiriq sharti:
`Result<&T, E>` dan `Result<T, E>` ga o'tish.

## Yechim (Rust kodi):
```rust
fn main() {
    let s = String::from("Rust");
    let res: Result<&String, ()> = Ok(&s);
    let yangi_res: Result<String, ()> = res.cloned();

    println!("Nusxalangan Result: {:?}", yangi_res);
}
```

## Tushuntirish va Mantiq:
`.cloned()` ichki havola ko'rsatib turgan ma'lumotni klonlab, yangi mustaqil obyekt beradi.

## Ishlash natijasi:
```text
Nusxalangan Result: Ok("Rust")
```

---

# 433-Topshiriq: Option va Result o'rtasida o'tish kombinatori: ok_or_else
## Topshiriq sharti:
Xatolik sababini closure orqali kechiktirib shakllantirish.

## Yechim (Rust kodi):
```rust
fn main() {
    let opt: Option<i32> = None;
    let res = opt.ok_or_else(|| format!("Xatolik vaqti: 12:00"));

    println!("{:?}", res);
}
```

## Tushuntirish va Mantiq:
`ok_or_else` dinamik formatlangan satrlarni faqat kerak bo'lganda yaratish uchun ishlatiladi.

## Ishlash natijasi:
```text
Err("Xatolik vaqti: 12:00")
```

---

# 434-Topshiriq: Result ichidagi qiymatni o'zgartiruvchi inspect metodi
## Topshiriq sharti:
Rust 2021/2024 ning yangi `inspect` va `inspect_err` imkoniyatlari.

## Yechim (Rust kodi):
```rust
fn main() {
    let r: Result<i32, &str> = Ok(42);

    let _ = r.inspect(|&x| println!("Muvaffaqiyatli qiymat: {}", x));
}
```

## Tushuntirish va Mantiq:
`inspect` oqimni buzmasdan oraliq logging qilish imkonini beradi.

## Ishlash natijasi:
```text
Muvaffaqiyatli qiymat: 42
```

---

# 435-Topshiriq: Xatolarni filtrlash: faqat ma'lum xatoni ushlash
## Topshiriq sharti:
Match orqali faqat kritik xatolarni qayta ishlash.

## Yechim (Rust kodi):
```rust
#[derive(Debug)]
enum Xato { Tarmoq, Auth, Boshqa }

fn bajar() -> Result<(), Xato> { Err(Xato::Auth) }

fn main() {
    if let Err(Xato::Auth) = bajar() {
        println!("Foydalanuvchi qayta tizimga kirishi kerak!");
    }
}
```

## Tushuntirish va Mantiq:
Pattern matching yordamida aynan kerakli xato turiga mos harakat belgilanadi.

## Ishlash natijasi:
```text
Foydalanuvchi qayta tizimga kirishi kerak!
```

---

# 436-Topshiriq: Result qaytaruvchi iteratorlarni filtrlash (filter_map)
## Topshiriq sharti:
Faqat muvaffaqiyatli qadamlarni qoldirish.

## Yechim (Rust kodi):
```rust
fn main() {
    let matnlar = vec!["10", "xato", "30", "yaroqsiz", "50"];

    let sonlar: Vec<i32> = matnlar.iter()
        .filter_map(|s| s.parse::<i32>().ok())
        .collect();

    println!("Saralangan sonlar: {:?}", sonlar);
}
```

## Tushuntirish va Mantiq:
`s.parse().ok()` `Result` ni `Option` ga o'tkazadi va `filter_map` faqat `Some` qiymatlarni oladi.

## Ishlash natijasi:
```text
Saralangan sonlar: [10, 30, 50]
```

---

# 437-Topshiriq: Ikki xil xato turini bitta umumiy enumga jamlash
## Topshiriq sharti:
`std::io::Error` va `ParseIntError` ni o'z ichiga oluvchi enum.

## Yechim (Rust kodi):
```rust
#[derive(Debug)]
enum YuklashXatosi {
    Io(String),
    Parse(std::num::ParseIntError),
}

impl From<std::num::ParseIntError> for YuklashXatosi {
    fn from(e: std::num::ParseIntError) -> Self { YuklashXatosi::Parse(e) }
}

fn raqamni_ol(s: &str) -> Result<i32, YuklashXatosi> {
    let n = s.parse::<i32>()?;
    Ok(n)
}

fn main() {
    println!("{:?}", raqamni_ol("77"));
    println!("{:?}", raqamni_ol("abc"));
}
```

## Tushuntirish va Mantiq:
`From` traiti orqali har xil xatolar bitta umumiy enum soyaboni ostiga yig'iladi.

## Ishlash natijasi:
```text
Ok(77)
Err(Parse(ParseIntError { kind: InvalidDigit }))
```

---

# 438-Topshiriq: Result qiymatlarini solishtirish
## Topshiriq sharti:
Ikkita `Result` tengligini tekshirish.

## Yechim (Rust kodi):
```rust
fn main() {
    let r1: Result<i32, &str> = Ok(10);
    let r2: Result<i32, &str> = Ok(10);
    let r3: Result<i32, &str> = Err("Xato");

    println!("r1 == r2: {}", r1 == r2);
    println!("r1 == r3: {}", r1 == r3);
}
```

## Tushuntirish va Mantiq:
Rust da `Result` `PartialEq` implement qiladi va uning variantlari tenglikka tekshiriladi.

## Ishlash natijasi:
```text
r1 == r2: true
r1 == r3: false
```

---

# 439-Topshiriq: Xatolik jurnalini faylga o'xshatib konsolga chiqarish
## Topshiriq sharti:
Vaqt tamg'asi bilan xatolarni chiqaruvchi yordamchi.

## Yechim (Rust kodi):
```rust
fn log_xato(xabar: &str) {
    eprintln!("[XATOLIK] {}", xabar);
}

fn main() {
    let res: Result<(), &str> = Err("Baza bilan aloqa yo'qoldi");
    if let Err(e) = res {
        log_xato(e);
    }
}
```

## Tushuntirish va Mantiq:
`eprintln!` standart xato oqimiga (stderr) xabar chiqaradi.

## Ishlash natijasi:
```text
[XATOLIK] Baza bilan aloqa yo'qoldi
```

---

# 440-Topshiriq: Result bilan qadam-baqam arifmetik hisoblagich
## Topshiriq sharti:
Har bir qadamda xatolik ehtimoli bo'lgan hisob.

## Yechim (Rust kodi):
```rust
fn ildiz_va_bolish(x: f64, y: f64) -> Result<f64, &'static str> {
    if x < 0.0 { return Err("Manfiy ildiz"); }
    let ildiz = x.sqrt();

    if y == 0.0 { return Err("Nolga bo'lish"); }
    Ok(ildiz / y)
}

fn main() {
    println!("{:?}", ildiz_va_bolish(25.0, 2.0));
    println!("{:?}", ildiz_va_bolish(-4.0, 2.0));
    println!("{:?}", ildiz_va_bolish(16.0, 0.0));
}
```

## Tushuntirish va Mantiq:
Barcha xato shartlari ketma-ket tekshirilib, xavfsiz qiymat qaytariladi.

## Ishlash natijasi:
```text
Ok(2.5)
Err("Manfiy ildiz")
Err("Nolga bo'lish")
```

---

# 441-Topshiriq: Result ichidagi qiymatni Option kabi unwrap_unchecked qilish haqida ogohlantirish
## Topshiriq sharti:
Xavfsiz Rust da doimo xavfsiz unwrap usullaridan foydalanish zarurati.

## Yechim (Rust kodi):
```rust
fn main() {
    let r: Result<i32, ()> = Ok(99);

    // Xavfsiz usul:
    if let Ok(val) = r {
        println!("Xavfsiz ochildi: {}", val);
    }
}
```

## Tushuntirish va Mantiq:
Rust xavfsizligi shundaki, xatolar e'tibordan chetda qolib ketishining oldi olinadi.

## Ishlash natijasi:
```text
Xavfsiz ochildi: 99
```

---

# 442-Topshiriq: Xatolarni o'rab oluvchi kontekst (Error Context) andozasi
## Topshiriq sharti:
Xatoga qo'shimcha ma'lumot ulash.

## Yechim (Rust kodi):
```rust
fn qoshimcha_kontekst(res: Result<i32, &str>, fayl: &str) -> Result<i32, String> {
    res.map_err(|e| format!("{}: '{}' faylida", e, fayl))
}

fn main() {
    let xato = Err("O'qish xatosi");
    let boyitilgan = qoshimcha_kontekst(xato, "data.bin");

    println!("{:?}", boyitilgan);
}
```

## Tushuntirish va Mantiq:
`anyhow` kabi mashhur kutubxonalar aynan shu usulda xatoga kontekst qo'shadi.

## Ishlash natijasi:
```text
Err("O'qish xatosi: 'data.bin' faylida")
```

---

# 443-Topshiriq: Result bilan Rekursiv qidiruv xatolari
## Topshiriq sharti:
Daraxt ichidan tugun topilmaganda xato qaytarish.

## Yechim (Rust kodi):
```rust
fn qidir(daraja: u32) -> Result<u32, &'static str> {
    if daraja == 0 {
        Err("Tugun topilmadi")
    } else {
        Ok(daraja * 10)
    }
}

fn main() {
    println!("{:?}", qidir(3));
    println!("{:?}", qidir(0));
}
```

## Tushuntirish va Mantiq:
Rekursiyada xatolar `Result` orqali yuqoriga uzatiladi.

## Ishlash natijasi:
```text
Ok(30)
Err("Tugun topilmadi")
```

---

# 444-Topshiriq: Result bilan Timeout xatoligi simulyatsiyasi
## Topshiriq sharti:
Vaqt chegarasidan oshib ketgan amalni `Result` ga o'rash.

## Yechim (Rust kodi):
```rust
enum TarmoqXato { Timeout, ServerXatosi }

fn yuklash(vaqt_ms: u32) -> Result<&'static str, TarmoqXato> {
    if vaqt_ms > 1000 {
        Err(TarmoqXato::Timeout)
    } else {
        Ok("Ma'lumotlar to'liq yuklandi")
    }
}

fn main() {
    println!("{:?}", yuklash(500).is_ok());
    println!("{:?}", yuklash(1500).is_err());
}
```

## Tushuntirish va Mantiq:
Tarmoq va asinxron so'rovlarda timeout xatolari `Result` bilan modellashtiriladi.

## Ishlash natijasi:
```text
true
true
```

---

# 445-Topshiriq: Xato kodlarini HTTP statuslariga o'girish
## Topshiriq sharti:
Maxsus xato turidan HTTP status kodini chiqaruvchi metod.

## Yechim (Rust kodi):
```rust
enum XizmatXatosi { Topilmadi, RuxsatYoq, Noto'g'riMa'lumot }

impl XizmatXatosi {
    fn status_kodi(&self) -> u16 {
        match self {
            XizmatXatosi::Topilmadi => 404,
            XizmatXatosi::RuxsatYoq => 403,
            XizmatXatosi::Noto'g'riMa'lumot => 400,
        }
    }
}

fn main() {
    let x = XizmatXatosi::Topilmadi;
    println!("HTTP Status: {}", x.status_kodi());
}
```

## Tushuntirish va Mantiq:
Backend serverlarda xatolar avtomatik HTTP javob kodiga aylantiriladi.

## Ishlash natijasi:
```text
HTTP Status: 404
```

---

# 446-Topshiriq: Result bilan String validatsiyasi
## Topshiriq sharti:
Elektron pochta manzilini format bo'yicha tekshirish.

## Yechim (Rust kodi):
```rust
fn email_tekshir(email: &str) -> Result<(), &'static str> {
    if !email.contains('@') || !email.contains('.') {
        return Err("Email formati noto'g'ri ('@' va '.' bo'lishi kerak)");
    }
    Ok(())
}

fn main() {
    println!("{:?}", email_tekshir("admin@rust.uz"));
    println!("{:?}", email_tekshir("not_email"));
}
```

## Tushuntirish va Mantiq:
Validatsiya natijalari uchun `Result<(), E>` qaytarish standart amaliyotdir.

## Ishlash natijasi:
```text
Ok(())
Err("Email formati noto'g'ri ('@' va '.' bo'lishi kerak)")
```

---

# 447-Topshiriq: Result::expect_err orqali aynan xatolik borligini tekshirish
## Topshiriq sharti:
Birlik testlarida funksiya haqiqatan ham xato qaytarganini tekshirish.

## Yechim (Rust kodi):
```rust
fn main() {
    let res: Result<i32, &str> = Err("Kutilgan xatolik");
    let xato_xabari = res.expect_err("Funksiya xato qaytarishi kerak edi!");

    println!("Xato tekshirildi: {}", xato_xabari);
}
```

## Tushuntirish va Mantiq:
`expect_err()` agar natija `Err` bo'lsa xatoni qaytaradi, agar `Ok` bo'lsa panic qiladi (testlar uchun ayni muddao).

## Ishlash natijasi:
```text
Xato tekshirildi: Kutilgan xatolik
```

---

# 448-Topshiriq: Result qiymatini zaxira funktsiya orqali tiklash
## Topshiriq sharti:
Xatolik yuz berganda ikkinchi funksiya orqali ma'lumot olish.

## Yechim (Rust kodi):
```rust
fn birinchi_urinish() -> Result<String, ()> { Err(()) }
fn ikkinchi_urinish() -> Result<String, ()> { Ok(String::from("Zaxira server ma'lumoti")) }

fn main() {
    let res = birinchi_urinish().or_else(|_| ikkinchi_urinish());
    println!("Natija: {:?}", res);
}
```

## Tushuntirish va Mantiq:
`or_else` orqali zaxira serverlar va kesh mexanizmlari ishga tushiriladi.

## Ishlash natijasi:
```text
Natija: Ok("Zaxira server ma'lumoti")
```

---

# 449-Topshiriq: Xato turlarini o'zaro tenglikka tekshirish: #[derive(PartialEq)]
## Topshiriq sharti:
Xato enumiga `PartialEq` berib, unit testlarda solishtirish.

## Yechim (Rust kodi):
```rust
#[derive(Debug, PartialEq)]
enum HisobXato { NolgaBolish, ManfiyIldiz }

fn main() {
    let x1 = HisobXato::NolgaBolish;
    let x2 = HisobXato::NolgaBolish;

    println!("Xatolar bir xilmi: {}", x1 == x2);
}
```

## Tushuntirish va Mantiq:
Xatolarga `PartialEq` berish ularni testlarda `assert_eq!` bilan solishtirish imkonini beradi.

## Ishlash natijasi:
```text
Xatolar bir xilmi: true
```

---

# 450-Topshiriq: Result bilan Yakuniy Arxitektura xulosasi
## Topshiriq sharti:
Xatoliklarni boshqarish bo'yicha to'liq xulosa.

## Yechim (Rust kodi):
```rust
fn main() {
    println!("Rust tilida xatoliklar - bu istisno emas, balki oddiy ma'lumot turidir.");
    println!("Barcha xatolar aniq Result bilan qaytariladi va kompilyator ularni tekshirishni kafolatlaydi.");
}
```

## Tushuntirish va Mantiq:
Rust dasturchisi xatoliklar haqida dastur yozilayotgan paytdayoq o'ylashga majbur bo'ladi, shuning uchun Rust dasturlari yillar davomida uzluksiz ishlaydi.

## Ishlash natijasi:
```text
Rust tilida xatoliklar - bu istisno emas, balki oddiy ma'lumot turidir.
Barcha xatolar aniq Result bilan qaytariladi va kompilyator ularni tekshirishni kafolatlaydi.
```

---
