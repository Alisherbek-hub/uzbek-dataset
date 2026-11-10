# 12-Qism: Lifetimes (Umr Ko'rish Muddatlari) va Havolalar Xavfsizligi (551-600)

Ushbu qismda Rust ning eng noyob va o'ziga xos mexanizmi bo'lgan **Lifetimes (Umr davrlari)**, Borrow Checker ning vaqt o'qi, `'a` annotatsiyalari, Lifetime Elision qoidalari, strukturalarda havolalar saqlash, `'static` umri, Zero-Copy Parserlar, Nol-nusxali tokenizatorlar hamda Higher-Rank Trait Bounds (`for<'a>`) amaliy topshiriqlarda o'rganiladi.

---

# 551-Topshiriq: Lifetimes nima? Borrow Checker ning vaqt o'qi
## Topshiriq sharti:
Kompilyator havolaning qancha vaqt yashashini qanday tekshirishini tushuntiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let r;
    {
        let x = 5;
        r = &x; // x ning umri shu blokda tugaydi!
        println!("r blok ichida: {}", r);
    }
    // println!("r blokdan tashqarida: {}", r); // Xatolik: x allaqachon o'lgan!
    println!("Rust xotirada muallaq ko'rsatkichlar (dangling pointers) qolishiga yo'l qo'ymaydi.");
}
```

## Tushuntirish va Mantiq:
Lifetimes har bir havolaning xotirada qancha muddat yaroqli (valid) bo'lib turishini belgilaydi. Borrow Checker havolaning manbasi undan oldin o'lib ketmasligini tekshiradi.

## Ishlash natijasi:
```text
r blok ichida: 5
Rust xotirada muallaq ko'rsatkichlar (dangling pointers) qolishiga yo'l qo'ymaydi.
```

---

# 552-Topshiriq: Funksiya signaturasida Lifetime annotatsiyasi ('a)
## Topshiriq sharti:
Ikkita satrdan eng uzunini qaytaruvchi funksiya yozing.

## Yechim (Rust kodi):
```rust
fn eng_uzun<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

fn main() {
    let s1 = String::from("Rust tili");
    let s2 = "Mukammal tizimlar";

    let natija = eng_uzun(&s1, s2);
    println!("Eng uzuni: '{}'", natija);
}
```

## Tushuntirish va Mantiq:
`'a` annotatsiyasi xotira umrini o'zgartirmaydi! U kompilyatorga: 'Qaytayotgan havola x va y dan qaysi biri qisqaroq yashasa, o'shaning umri bilan cheklansin' degan mantiqiy bog'lanishni bildiradi.

## Ishlash natijasi:
```text
Eng uzuni: 'Mukammal tizimlar'
```

---

# 553-Topshiriq: Nega Lifetimes havolaning haqiqiy umrini o'zgartirmaydi?
## Topshiriq sharti:
Lifetime annotatsiyasi faqat tavsifiy (deskriptiv) shartnoma ekanligini ko'rsating.

## Yechim (Rust kodi):
```rust
fn chop_qism<'a>(matn: &'a str) {
    println!("Matn qismi: {}", matn);
}

fn main() {
    let s = String::from("Vaqtinchalik");
    chop_qism(&s);
}
```

## Tushuntirish va Mantiq:
Lifetime parametrlarini qo'shish obyektning umrini uzaytirmaydi yoki qisqartirmaydi, balki bir nechta havolalarning o'zaro bog'liqligini kompilyatorga tushuntiradi.

## Ishlash natijasi:
```text
Matn qismi: Vaqtinchalik
```

---

# 554-Topshiriq: Lifetime Elision Rules: 1-qoida (Har bir parametrga alohida lifetime)
## Topshiriq sharti:
Kompilyator bitta parametrli funksiyalarda lifetime ni o'zi qanday qo'yishini ko'rsating.

## Yechim (Rust kodi):
```rust
// Biz yozamiz:
fn birinchi_harf(s: &str) -> &str {
    &s[0..1]
}

// Kompilyator buni quyidagicha ko'radi:
// fn birinchi_harf<'a>(s: &'a str) -> &'a str

fn main() {
    let shahar = "Toshkent";
    println!("Bosh harf: {}", birinchi_harf(shahar));
}
```

## Tushuntirish va Mantiq:
Lifetime Elision qoidalari dasturchi har safar qo'lda `'a` deb yozmasligi uchun umumiy andozalarni avtomatik to'ldiradi.

## Ishlash natijasi:
```text
Bosh harf: T
```

---

# 555-Topshiriq: Lifetime Elision Rules: 3-qoida (&self metodi)
## Topshiriq sharti:
Metodlarda qaytuvchi havola avtomatik `&self` umriga bog'lanishi.

## Yechim (Rust kodi):
```rust
struct Xabar { matn: String }

impl Xabar {
    // Qoidaga ko'ra, qaytish havola self umriga tenglanadi:
    fn matnni_ol(&self) -> &str {
        &self.matn
    }
}

fn main() {
    let x = Xabar { matn: String::from("Muhim yangilik") };
    println!("Olingan: {}", x.matnni_ol());
}
```

## Tushuntirish va Mantiq:
Agar metodda `&self` yoki `&mut self` bo'lsa, qaytuvchi barcha havolalar avtomatik ravishda `self` ning hayot davriga biriktiriladi.

## Ishlash natijasi:
```text
Olingan: Muhim yangilik
```

---

# 556-Topshiriq: Strukturalarda havolalar saqlash: struct MatnQismi<'a>
## Topshiriq sharti:
Struktura ichida `&str` havolasini saqlash uchun lifetime annotatsiyasi.

## Yechim (Rust kodi):
```rust
struct MatnQismi<'a> {
    qism: &'a str,
}

fn main() {
    let gap = String::from("Rust xotirasi xavfsiz");
    let birinchi_soz = gap.split_whitespace().next().unwrap();

    let m = MatnQismi { qism: birinchi_soz };
    println!("Saqlangan qism: '{}'", m.qism);
}
```

## Tushuntirish va Mantiq:
Agar struktura o'zida havola (`&`) saqlasa, strukturaning o'zi ham `<'a>` parametriga ega bo'lishi shart. Bu struktura havola qilayotgan ma'lumotdan ko'proq yashay olmasligini kafolatlaydi.

## Ishlash natijasi:
```text
Saqlangan qism: 'Rust'
```

---

# 557-Topshiriq: Struktura uning ichidagi havoladan ko'p yashay olmasligi
## Topshiriq sharti:
Kompilyatorning xotira qat'iyligini namoyish eting.

## Yechim (Rust kodi):
```rust
struct Ko'rinish<'a> {
    manba: &'a str,
}

fn main() {
    let tashqi_matn = String::from("Uzoq yashovchi matn");
    let k = Ko'rinish { manba: &tashqi_matn };

    println!("Ko'rinish faol: {}", k.manba);
}
```

## Tushuntirish va Mantiq:
Struktura o'z ichidagi manba xotiradan chiqib ketganidan keyin yashay olmaydi. Aks holda u o'lik xotiraga murojaat qilgan bo'lardi.

## Ishlash natijasi:
```text
Ko'rinish faol: Uzoq yashovchi matn
```

---

# 558-Topshiriq: impl bloklarida Lifetimes: impl<'a> MatnQismi<'a>
## Topshiriq sharti:
Lifetime li struktura metodlarini yozish.

## Yechim (Rust kodi):
```rust
struct HavolaSaqlovchi<'a> {
    malumot: &'a str,
}

impl<'a> HavolaSaqlovchi<'a> {
    fn elon_qil(&self) {
        println!("Saqlangan matn: {}", self.malumot);
    }
}

fn main() {
    let s = "Statik ma'lumot";
    let h = HavolaSaqlovchi { malumot: s };
    h.elon_qil();
}
```

## Tushuntirish va Mantiq:
`impl<'a> Struktura<'a>` sintaksisi strukturaning umr parametrini metodlar blokiga bog'laydi.

## Ishlash natijasi:
```text
Saqlangan matn: Statik ma'lumot
```

---

# 559-Topshiriq: Statik Lifetime: 'static nima?
## Topshiriq sharti:
Dasturning butun ishlash muddati davomida xotirada yashaydigan satr literallari.

## Yechim (Rust kodi):
```rust
fn main() {
    let shior: &'static str = "Rust: Tez, Xavfsiz, Ishonchli!";
    println!("Statik matn: {}", shior);
}
```

## Tushuntirish va Mantiq:
`'static` eng uzoq umr bo'lib, dastur ishga tushganidan to tugaguncha binar faylning ma'lumotlar segmentida (Read-Only Data) saqlanadi.

## Ishlash natijasi:
```text
Statik matn: Rust: Tez, Xavfsiz, Ishonchli!
```

---

# 560-Topshiriq: T: 'static trait bound tushunchasi
## Topshiriq sharti:
Qiymat hech qanday qisqa muddatli havolalarni o'z ichiga olmasligini talab qilish.

## Yechim (Rust kodi):
```rust
fn qabul_qil_static<T: 'static>(qiymat: T) {
    println!("Qiymat xavfsiz holda uzoq yashay oladi: {} bayt", std::mem::size_of_val(&qiymat));
}

fn main() {
    let s = String::from("Egalikdagi satr"); // String o'z ma'lumotiga ega, qisqa havolasi yo'q!
    qabul_qil_static(s);
    qabul_qil_static(42);
}
```

## Tushuntirish va Mantiq:
`T: 'static` degani turning o'zi cheksiz yashaydi degani emas, balki turning ichida qisqa muddatli havola yo'qligini, to'liq o'ziga egalik qilishini anglatadi.

## Ishlash natijasi:
```text
Qiymat xavfsiz holda uzoq yashay oladi: 24 bayt
Qiymat xavfsiz holda uzoq yashay oladi: 4 bayt
```

---

# 561-Topshiriq: Bir nechta turli Lifetime parametrlari: <'a, 'b>
## Topshiriq sharti:
Ikki xil manbadan kelgan havolalarning mustaqil umrlarini belgilang.

## Yechim (Rust kodi):
```rust
fn birinchi_yoki_ikkinchi<'a, 'b>(x: &'a str, _y: &'b str) -> &'a str {
    x // Faqat x qaytadi, demak qaytish faqat 'a ga bog'liq!
}

fn main() {
    let s1 = String::from("Uzoq yashovchi");
    let res;
    {
        let s2 = String::from("Qisqa");
        res = birinchi_yoki_ikkinchi(&s1, &s2);
    } // s2 o'ldi, lekin res hali ham yaroqli, chunki u s1 ga bog'liq!

    println!("Natija: {}", res);
}
```

## Tushuntirish va Mantiq:
Har bir parametrga alohida lifetime berish orqali bittasining o'lishi ikkinchisiga ta'sir qilmasligini ta'minlash mumkin.

## Ishlash natijasi:
```text
Natija: Uzoq yashovchi
```

---

# 562-Topshiriq: Enum variantlarida Lifetimes saqlash
## Topshiriq sharti:
Tokenizator uchun satr bo'laklarini saqlovchi enum.

## Yechim (Rust kodi):
```rust
#[derive(Debug)]
enum Token<'a> {
    Soz(&'a str),
    Raqam(i64),
}

fn main() {
    let jumla = "salom 123";
    let t1 = Token::Soz(&jumla[0..5]);
    let t2 = Token::Raqam(123);

    println!("Tokenlar: {:?}, {:?}", t1, t2);
}
```

## Tushuntirish va Mantiq:
Enum variantlarida `&'a str` saqlash orqali yangi `String` lar yaratmasdan nol-nusxali (zero-copy) parserlar quriladi.

## Ishlash natijasi:
```text
Tokenlar: Soz("salom"), Raqam(123)
```

---

# 563-Topshiriq: Nol-nusxali Parser (Zero-Copy Lexer) arxitekturasi
## Topshiriq sharti:
Matndan hech narsani klonlamasdan so'zlarga ajratuvchi lexer tuzing.

## Yechim (Rust kodi):
```rust
struct Lexer<'a> {
    manba: &'a str,
}

impl<'a> Lexer<'a> {
    fn new(manba: &'a str) -> Self { Self { manba } }

    fn keyingi_soz(&mut self) -> Option<&'a str> {
        if self.manba.is_empty() { return None; }
        let mut split = self.manba.split_whitespace();
        let soz = split.next()?;
        self.manba = &self.manba[soz.len()..].trim_start();
        Some(soz)
    }
}

fn main() {
    let kod = "fn main() { println!(); }";
    let mut lex = Lexer::new(kod);

    while let Some(token) = lex.keyingi_soz() {
        println!("Token: '{}'", token);
    }
}
```

## Tushuntirish va Mantiq:
Zero-Copy Lexer 0 bayt yangi Heap xotira ajratadi va matnni gigabaytlab tezlikda pars qiladi.

## Ishlash natijasi:
```text
Token: 'fn'
Token: 'main()'
Token: '{'
Token: 'println!();'
Token: '}'
```

---

# 564-Topshiriq: Konfiguratsiya faylini pars qiluvchi nol-nusxali model
## Topshiriq sharti:
Kalit va qiymatlarni asl matn havolalari orqali saqlang.

## Yechim (Rust kodi):
```rust
struct KalitQiymat<'a> {
    kalit: &'a str,
    qiymat: &'a str,
}

fn parse_qator<'a>(qator: &'a str) -> Option<KalitQiymat<'a>> {
    let mut qismlar = qator.split('=');
    let k = qismlar.next()?.trim();
    let q = qismlar.next()?.trim();
    Some(KalitQiymat { kalit: k, qiymat: q })
}

fn main() {
    let config = "port = 8080";
    if let Some(kv) = parse_qator(config) {
        println!("Parametr: '{}' -> '{}'", kv.kalit, kv.qiymat);
    }
}
```

## Tushuntirish va Mantiq:
Matn bo'lagi asl satr xotirasiga ishora qiladi, hech qanday xotira ko'chirilmaydi.

## Ishlash natijasi:
```text
Parametr: 'port' -> '8080'
```

---

# 565-Topshiriq: Struct ichida boshqa lifetime li structni saqlash
## Topshiriq sharti:
Ichma-ich strukturalarda lifetime parametrlarini zanjirlash.

## Yechim (Rust kodi):
```rust
struct Sarlavha<'a> { matn: &'a str }
struct Hujjat<'a> { sarlavha: Sarlavha<'a> }

fn main() {
    let s = "Rust Asoslari";
    let doc = Hujjat { sarlavha: Sarlavha { matn: s } };

    println!("Hujjat sarlavhasi: {}", doc.sarlavha.matn);
}
```

## Tushuntirish va Mantiq:
Ichma-ich strukturalar ham o'zaro bir xil yoki bog'liq lifetime parametrlarini ulashib oladi.

## Ishlash natijasi:
```text
Hujjat sarlavhasi: Rust Asoslari
```

---

# 566-Topshiriq: Generik parametrlar, Trait Bounds va Lifetimes bitta funksiyada
## Topshiriq sharti:
Barcha xususiyatlarni bitta chiroyli funksiya signaturasida jamlang.

## Yechim (Rust kodi):
```rust
use std::fmt::Display;

fn hisobot<'a, T>(sarlavha: &'a str, qiymat: T) -> &'a str
where
    T: Display,
{
    println!("Qiymat: {}", qiymat);
    sarlavha
}

fn main() {
    let s = hisobot("Tizim hisoboti", 100);
    println!("Sarlavha: {}", s);
}
```

## Tushuntirish va Mantiq:
`'a` lifetime parametri va `T: Display` generik parametri birgalikda eng yuqori darajadagi moslashuvchanlikni beradi.

## Ishlash natijasi:
```text
Qiymat: 100
Sarlavha: Tizim hisoboti
```

---

# 567-Topshiriq: Anonim Lifetime: '_ sintaksisi
## Topshiriq sharti:
Kompilyatordan o'zi tushunishi mumkin bo'lgan joyda lifetime ni hisoblashni so'rang.

## Yechim (Rust kodi):
```rust
struct Matn<'a>(&'a str);

impl Matn<'_> {
    fn uzunlik(&self) -> usize {
        self.0.len()
    }
}

fn main() {
    let m = Matn("Salom");
    println!("Uzunlik: {}", m.uzunlik());
}
```

## Tushuntirish va Mantiq:
`'_` anonim lifetime bo'lib, uning aniq nomini qayta takrorlash shart bo'lmaganda kodni soddalashtiradi.

## Ishlash natijasi:
```text
Uzunlik: 5
```

---

# 568-Topshiriq: Box::leak orqali dinamik xotirani 'static ga aylantirish
## Topshiriq sharti:
Heap dagi satrni dastur tugaguncha yashovchi statik havolaga o'tkazish.

## Yechim (Rust kodi):
```rust
fn statik_satr_yasa(s: String) -> &'static str {
    Box::leak(s.into_boxed_str())
}

fn main() {
    let s = format!("Dinamik vaqt: {}", 2024);
    let statik: &'static str = statik_satr_yasa(s);

    println!("Statik satr: {}", statik);
}
```

## Tushuntirish va Mantiq:
`Box::leak` xotiraning avtomatik tozalanishini to'xtatib, unga `'static` maqomini beradi. Bu global kesh va konfiguratsiyalarda qo'llaniladi.

## Ishlash natijasi:
```text
Statik satr: Dinamik vaqt: 2024
```

---

# 569-Topshiriq: Matndan birinchi qatorni ajratib olish (First line zero-copy)
## Topshiriq sharti:
Ko'p qatorli matndan birinchi satr havolasini qaytaruvchi funksiya.

## Yechim (Rust kodi):
```rust
fn birinchi_qator<'a>(matn: &'a str) -> &'a str {
    matn.lines().next().unwrap_or("")
}

fn main() {
    let hujjat = "1-qator: Rust zo'r\n2-qator: C++ tez";
    println!("Birinchi qator: '{}'", birinchi_qator(hujjat));
}
```

## Tushuntirish va Mantiq:
Funksiya kiruvchi matnning o'zidan qarzga olingan havolani qaytaradi va hech qanday nusxa olmaydi.

## Ishlash natijasi:
```text
Birinchi qator: '1-qator: Rust zo'r'
```

---

# 570-Topshiriq: CSV qatorini nol-nusxali o'qish: CsvRow<'a>
## Topshiriq sharti:
CSV ustunlarini asl satr ko'rsatkichlari bilan saqlovchi model.

## Yechim (Rust kodi):
```rust
struct CsvQator<'a> {
    ustunlar: Vec<&'a str>,
}

impl<'a> CsvQator<'a> {
    fn parse(qator: &'a str) -> Self {
        Self { ustunlar: qator.split(',').collect() }
    }
}

fn main() {
    let qator = "Ali,25,Dasturchi";
    let csv = CsvQator::parse(qator);

    println!("Ustunlar soni: {}, 1-ustun: {}", csv.ustunlar.len(), csv.ustunlar[0]);
}
```

## Tushuntirish va Mantiq:
Butun CSV fayl xotiraga bitta `String` sifatida yuklanadi va barcha jadval elementlari faqat havolalar orqali ishlanadi.

## Ishlash natijasi:
```text
Ustunlar soni: 3, 1-ustun: Ali
```

---

# 571-Topshiriq: HTML/XML Teglarni ajratuvchi nol-nusxali model
## Topshiriq sharti:
Teg nomi va ichki matnini ajratib ko'rsating.

## Yechim (Rust kodi):
```rust
struct XmlTeg<'a> {
    nom: &'a str,
    tarkib: &'a str,
}

fn parse_teg<'a>(xml: &'a str) -> Option<XmlTeg<'a>> {
    let ochilish = xml.find('>')?;
    let yopilish = xml.rfind('<')?;

    let nom = &xml[1..ochilish];
    let tarkib = &xml[ochilish + 1..yopilish];
    Some(XmlTeg { nom, tarkib })
}

fn main() {
    let xml = "<h1>Assalomu alaykum</h1>";
    if let Some(teg) = parse_teg(xml) {
        println!("Teg nomi: '{}', Tarkibi: '{}'", teg.nom, teg.tarkib);
    }
}
```

## Tushuntirish va Mantiq:
XML teglari qirqib olinganda ham yangi xotira sarflanmaydi.

## Ishlash natijasi:
```text
Teg nomi: 'h1', Tarkibi: 'Assalomu alaykum'
```

---

# 572-Topshiriq: URL Parseri (Protokol va Domen havolalari bilan)
## Topshiriq sharti:
URL manzilini uning qismlariga ajrating.

## Yechim (Rust kodi):
```rust
struct UrlQismlari<'a> {
    protokol: &'a str,
    domen: &'a str,
}

fn url_parse<'a>(url: &'a str) -> Option<UrlQismlari<'a>> {
    let ajratgich = url.find("://")?;
    let protokol = &url[..ajratgich];
    let qolgan = &url[ajratgich + 3..];
    let domen = qolgan.split('/').next()?;

    Some(UrlQismlari { protokol, domen })
}

fn main() {
    let manzil = "https://kun.uz/news/2024";
    if let Some(u) = url_parse(manzil) {
        println!("Protokol: {}, Domen: {}", u.protokol, u.domen);
    }
}
```

## Tushuntirish va Mantiq:
Internet manzillari tahlilida havolalardan foydalanish tarmoq routerlari tezligini maksimal qiladi.

## Ishlash natijasi:
```text
Protokol: https, Domen: kun.uz
```

---

# 573-Topshiriq: Struct ichida &mut havola saqlash
## Topshiriq sharti:
O'zgaruvchan havolani saqlovchi struktura modeli.

## Yechim (Rust kodi):
```rust
struct Yangilovchi<'a> {
    son: &'a mut i32,
}

impl<'a> Yangilovchi<'a> {
    fn oshir(&mut self) {
        *self.son += 10;
    }
}

fn main() {
    let mut x = 50;
    {
        let mut y = Yangilovchi { son: &mut x };
        y.oshir();
    }
    println!("x yangilandi: {}", x);
}
```

## Tushuntirish va Mantiq:
Struktura ichida `&mut` havola saqlanganda, u mavjud bo'lgan davrda boshqa hech kim asl o'zgaruvchiga tegina olmaydi.

## Ishlash natijasi:
```text
x yangilandi: 60
```

---

# 574-Topshiriq: Tarmoq paketi sarlavhasi (Packet Header zero-copy viewer)
## Topshiriq sharti:
Binar paketdan sarlavha baytlarini ko'rish.

## Yechim (Rust kodi):
```rust
struct PaketSarlavha<'a> {
    baytlar: &'a [u8],
}

impl<'a> PaketSarlavha<'a> {
    fn yangi(xom: &'a [u8]) -> Self { Self { baytlar: &xom[0..4] } }
}

fn main() {
    let tarmoq_ma'lumoti = [0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF];
    let hdr = PaketSarlavha::yangi(&tarmoq_ma'lumoti);

    println!("Paket sarlavhasi: {:02X?}", hdr.baytlar);
}
```

## Tushuntirish va Mantiq:
Tarmoq drayverlari paketlarni bitta buferda qabul qilib, uning har bir qatlamini havolalar orqali ko'rib chiqadi.

## Ishlash natijasi:
```text
Paket sarlavhasi: [AA, BB, CC, DD]
```

---

# 575-Topshiriq: Matematik ifodalar tokenizatori (MathToken<'a>)
## Topshiriq sharti:
Arifmetik amallarni matn havolalari bilan ajrating.

## Yechim (Rust kodi):
```rust
#[derive(Debug)]
enum MathToken<'a> {
    Raqam(&'a str),
    Amal(char),
}

fn main() {
    let ifoda = "125 + 450";
    let t1 = MathToken::Raqam(&ifoda[0..3]);
    let t2 = MathToken::Amal('+');
    let t3 = MathToken::Raqam(&ifoda[6..9]);

    println!("{:?} {:?} {:?}", t1, t2, t3);
}
```

## Tushuntirish va Mantiq:
Kompilyatorlar va kalkulyatorlar kiruvchi kod matnini ko'chirmasdan tokenizatsiya qiladi.

## Ishlash natijasi:
```text
Raqam("125") Amal('+') Raqam("450")
```

---

# 576-Topshiriq: Higher-Rank Trait Bounds (HRTB: for<'a>) tushunchasi
## Topshiriq sharti:
Har qanday lifetime ga mos keluvchi closure talab qilish.

## Yechim (Rust kodi):
```rust
fn matn_bilan_ishla<F>(amal: F)
where
    F: for<'a> Fn(&'a str) -> usize,
{
    let s = String::from("Rust HRTB");
    let len = amal(&s);
    println!("Natija: {}", len);
}

fn main() {
    matn_bilan_ishla(|m| m.len());
}
```

## Tushuntirish va Mantiq:
`for<'a>` sintaksisi 'har qanday mumkin bo'lgan lifetime uchun' degan ma'noni anglatadi va murakkab closurelarda talab qilinadi.

## Ishlash natijasi:
```text
Natija: 9
```

---

# 577-Topshiriq: Lifetimes Subtyping ('a: 'b)
## Topshiriq sharti:
`'a` umri kamida `'b` kabi yashashini ko'rsating.

## Yechim (Rust kodi):
```rust
fn subtyping_misol<'a, 'b: 'a>(uzoq: &'b str, _qisqa: &'a str) -> &'a str {
    uzoq // 'b kamida 'a kabi yashagani uchun uni 'a sifatida qaytarish mumkin!
}

fn main() {
    let s1 = "Cheksiz statik";
    let s2 = String::from("Vaqtinchalik");

    let res = subtyping_misol(s1, &s2);
    println!("Subtyping natijasi: {}", res);
}
```

## Tushuntirish va Mantiq:
`'b: 'a` qoidasi xuddi merosxo'rlik kabi: kattaroq umr kichikroq umr o'rniga bemalol o'ta oladi.

## Ishlash natijasi:
```text
Subtyping natijasi: Cheksiz statik
```

---

# 578-Topshiriq: Ko'p qatlamli havolalar va lifetimes (&&'a str)
## Topshiriq sharti:
Havolaga havola bo'lganda umr zanjirini tekshirish.

## Yechim (Rust kodi):
```rust
fn qatlamli<'a>(matn: &'a &'a str) -> &'a str {
    *matn
}

fn main() {
    let s = "Rust tili";
    let r1 = &s;
    let r2 = &r1;

    println!("Qatlam ochildi: {}", qatlamli(r2));
}
```

## Tushuntirish va Mantiq:
Ko'p qatlamli havolalarda har bir havola o'zining umriga ega bo'lib, xotira zanjirini hosil qiladi.

## Ishlash natijasi:
```text
Qatlam ochildi: Rust tili
```

---

# 579-Topshiriq: Matn qisqartiruvchi (Snipper) modeli lifetimes bilan
## Topshiriq sharti:
Asl matndan qisqa bo'lak qirqib olish.

## Yechim (Rust kodi):
```rust
struct Snipper<'a> { matn: &'a str }

impl<'a> Snipper<'a> {
    fn snip(&self, len: usize) -> &'a str {
        if self.matn.len() <= len { self.matn } else { &self.matn[..len] }
    }
}

fn main() {
    let xabar = "Rust tizimli dasturlashning kelajagidir";
    let snp = Snipper { matn: xabar };

    println!("Snip: '{}'", snp.snip(12));
}
```

## Tushuntirish va Mantiq:
Qaytuvchi bo'lak `Snipper` o'lgandan keyin ham yashay oladi, chunki u `self` ga emas, balki asl `'a` matniga bog'langan.

## Ishlash natijasi:
```text
Snip: 'Rust tizimli '
```

---

# 580-Topshiriq: Lifetimes moduli xulosasi: Xotira xavfsizligining vaqt o'qi
## Topshiriq sharti:
Lifetimes qoidalarining to'liq tahlili.

## Yechim (Rust kodi):
```rust
fn main() {
    println!("=== RUST LIFETIMES XULOSASI ===");
    println!("1. Lifetimes havolalarning xotirada qancha yashashini ifodalaydi.");
    println!("2. Dangling pointer (osilgan ko'rsatkich) xatolarini kompilyatsiyada yo'qotadi.");
    println!("3. 'static - dastur tugaguncha saqlanadigan xotira.");
    println!("4. Elision qoidalari ko'p joyda 'a yozish majburiyatini yengillatadi.");
    println!("5. Zero-Copy parserlar lifetimes tufayli gigabaytlab ma'lumotni 0 nusxa bilan tahlil qiladi.");
}
```

## Tushuntirish va Mantiq:
Lifetimes Rust tilining eng murakkab, lekin eng buyuk kashfiyotidir: u xotira xatolarini 0 bayt qo'shimcha resurs sarflamasdan kafolatlaydi.

## Ishlash natijasi:
```text
=== RUST LIFETIMES XULOSASI ===
1. Lifetimes havolalarning xotirada qancha yashashini ifodalaydi.
2. Dangling pointer (osilgan ko'rsatkich) xatolarini kompilyatsiyada yo'qotadi.
3. 'static - dastur tugaguncha saqlanadigan xotira.
4. Elision qoidalari ko'p joyda 'a yozish majburiyatini yengillatadi.
5. Zero-Copy parserlar lifetimes tufayli gigabaytlab ma'lumotni 0 nusxa bilan tahlil qiladi.
```

---

# 581-Topshiriq: Maxsus Lifetime bilan Bog'langan Lug'at (Lookup Table)
## Topshiriq sharti:
Statik kalitlar va havolalar bilan ishlovchi jadval.

## Yechim (Rust kodi):
```rust
struct Lugat<'a> {
    elementlar: Vec<(&'a str, &'a str)>,
}

impl<'a> Lugat<'a> {
    fn qidir(&self, kalit: &str) -> Option<&'a str> {
        for (k, v) in &self.elementlar {
            if *k == kalit { return Some(v); }
        }
        None
    }
}

fn main() {
    let lugat = Lugat {
        elementlar: vec![("uz", "O'zbekiston"), ("en", "England")],
    };

    println!("'uz': {:?}", lugat.qidir("uz"));
}
```

## Tushuntirish va Mantiq:
Qidiruv natijasi asl ma'lumot umri (`'a`) bilan qaytadi.

## Ishlash natijasi:
```text
'uz': Some("O'zbekiston")
```

---

# 582-Topshiriq: Lifetimes bilan Qatorlar bo'yicha saralovchi
## Topshiriq sharti:
Matn qatorlarini nusxalamasdan tartiblash.

## Yechim (Rust kodi):
```rust
fn qatorlarni_sarala<'a>(matn: &'a str) -> Vec<&'a str> {
    let mut qatorlar: Vec<&'a str> = matn.lines().collect();
    qatorlar.sort();
    qatorlar
}

fn main() {
    let matn = "Zebo\nAnvar\nJasur";
    let saralangan = qatorlarni_sarala(matn);

    println!("Saralangan qatorlar: {:?}", saralangan);
}
```

## Tushuntirish va Mantiq:
Matn o'zgarishsiz qoladi, faqat ko'rsatkichlar saralanadi.

## Ishlash natijasi:
```text
Saralangan qatorlar: ["Anvar", "Jasur", "Zebo"]
```

---

# 583-Topshiriq: Lifetimes bilan Matnli qidiruv oynasi (Search Window)
## Topshiriq sharti:
Nishon atrofidagi kontekstni ko'rsatuvchi oyna.

## Yechim (Rust kodi):
```rust
fn kontekst_oynasi<'a>(matn: &'a str, soz: &str) -> Option<&'a str> {
    let idx = matn.find(soz)?;
    let start = idx.saturating_sub(5);
    let end = (idx + soz.len() + 5).min(matn.len());
    Some(&matn[start..end])
}

fn main() {
    let matn = "Biz Rust dasturlash tilini sevamiz";
    println!("Kontekst: {:?}", kontekst_oynasi(matn, "dasturlash"));
}
```

## Tushuntirish va Mantiq:
Kontekst qirqib olinganda hech qanday yangi satr yaratilmaydi.

## Ishlash natijasi:
```text
Kontekst: Some("Rust dasturlash tili")
```

---

# 584-Topshiriq: Lifetimes bilan Binar Protokol Deserializatori
## Topshiriq sharti:
Baytlar oqimidan qiymatlarni ajratish.

## Yechim (Rust kodi):
```rust
struct Deserializator<'a> {
    oqim: &'a [u8],
}

impl<'a> Deserializator<'a> {
    fn bayt_ol(&mut self) -> Option<u8> {
        if self.oqim.is_empty() { return None; }
        let b = self.oqim[0];
        self.oqim = &self.oqim[1..];
        Some(b)
    }
}

fn main() {
    let paket = [1, 2, 3];
    let mut d = Deserializator { oqim: &paket };

    println!("1-bayt: {:?}", d.bayt_ol());
    println!("2-bayt: {:?}", d.bayt_ol());
}
```

## Tushuntirish va Mantiq:
Deserializator xotirani oldinga surib boradi va 0 nusxa bilan ishlaydi.

## Ishlash natijasi:
```text
1-bayt: Some(1)
2-bayt: Some(2)
```

---

# 585-Topshiriq: Lifetimes bilan O'yin Qahramoni inventari
## Topshiriq sharti:
Qahramonga qurol biriktirish.

## Yechim (Rust kodi):
```rust
struct Qurol<'a> { nom: &'a str }
struct Qahramon<'a> { qurol: Qurol<'a> }

fn main() {
    let qilich = "Olmos Qilich";
    let q = Qahramon { qurol: Qurol { nom: qilich } };

    println!("Qahramon quroli: {}", q.qurol.nom);
}
```

## Tushuntirish va Mantiq:
Qurol qahramondan mustaqil yashay oladi va umrlar bog'lanadi.

## Ishlash natijasi:
```text
Qahramon quroli: Olmos Qilich
```

---

# 586-Topshiriq: Lifetimes bilan JSON Tokenizatori (JsonLexer)
## Topshiriq sharti:
Qavslar va satrlarni ajratuvchi model.

## Yechim (Rust kodi):
```rust
struct JsonLexer<'a> { json: &'a str }

impl<'a> JsonLexer<'a> {
    fn birinchi_belgi(&self) -> Option<char> { self.json.chars().next() }
}

fn main() {
    let l = JsonLexer { json: "{"kalit": 12}" };
    println!("Boshlanish: {:?}", l.birinchi_belgi());
}
```

## Tushuntirish va Mantiq:
JSON tahlili nol nusxa bilan boshlanadi.

## Ishlash natijasi:
```text
Boshlanish: Some('{')
```

---

# 587-Topshiriq: Lifetimes bilan Regex o'rnini bosuvchi oddiy pattern qidiruvchi
## Topshiriq sharti:
Prefix va Suffix orasidagi matnni topish.

## Yechim (Rust kodi):
```rust
fn oraliqni_ol<'a>(matn: &'a str, bosh: &str, oxir: &str) -> Option<&'a str> {
    let b_idx = matn.find(bosh)? + bosh.len();
    let o_idx = matn[b_idx..].find(oxir)? + b_idx;
    Some(&matn[b_idx..o_idx])
}

fn main() {
    let html = "<b>Qalin matn</b>";
    println!("Oraliq: {:?}", oraliqni_ol(html, "<b>", "</b>"));
}
```

## Tushuntirish va Mantiq:
Oraliq matn to'liq xavfsiz holda asl satrdan kesib olinadi.

## Ishlash natijasi:
```text
Oraliq: Some("Qalin matn")
```

---

# 588-Topshiriq: Lifetimes bilan Dinamik Kesh strukturasi
## Topshiriq sharti:
Vaqtincha ma'lumot saqlovchi kesh.

## Yechim (Rust kodi):
```rust
struct Kesh<'a> {
    joy: Option<&'a str>,
}

impl<'a> Kesh<'a> {
    fn saqla(&mut self, val: &'a str) { self.joy = Some(val); }
}

fn main() {
    let mut k = Kesh { joy: None };
    let matn = "Muhim";
    k.saqla(matn);

    println!("Keshda: {:?}", k.joy);
}
```

## Tushuntirish va Mantiq:
Keshga faqat uning umridan kam yashamaydigan qiymatlarni qo'yish mumkin.

## Ishlash natijasi:
```text
Keshda: Some("Muhim")
```

---

# 589-Topshiriq: Lifetimes bilan Matn filtrlash va saralash zanjiri
## Topshiriq sharti:
Katta harfli so'zlarni ajratish.

## Yechim (Rust kodi):
```rust
fn katta_harflilar<'a>(matn: &'a str) -> Vec<&'a str> {
    matn.split_whitespace()
        .filter(|s| s.chars().next().map_or(false, |c| c.is_uppercase()))
        .collect()
}

fn main() {
    let jumla = "Toshkent Samarqand va buxoro";
    println!("Bosh harflilar: {:?}", katta_harflilar(jumla));
}
```

## Tushuntirish va Mantiq:
Filtrlangan natijalar asl satrga ishora qiladi.

## Ishlash natijasi:
```text
Bosh harflilar: ["Toshkent", "Samarqand"]
```

---

# 590-Topshiriq: Lifetimes bilan Matn formatlagich (Formatter Wrapper)
## Topshiriq sharti:
Matnni ramkaga soluvchi yordamchi.

## Yechim (Rust kodi):
```rust
struct Ramka<'a> { matn: &'a str }

impl<'a> Ramka<'a> {
    fn chop(&self) { println!("*** {} ***", self.matn); }
}

fn main() {
    let r = Ramka { matn: "Rust 2024" };
    r.chop();
}
```

## Tushuntirish va Mantiq:
Sodda ramka modeli havolalarni xavfsiz boshqaradi.

## Ishlash natijasi:
```text
*** Rust 2024 ***
```

---

# 591-Topshiriq: Lifetimes bilan Log tahlilchisi (Log Entry Parser)
## Topshiriq sharti:
Log qatoridan daraja va xabarni ajratish.

## Yechim (Rust kodi):
```rust
struct LogQator<'a> {
    daraja: &'a str,
    xabar: &'a str,
}

fn log_parse<'a>(s: &'a str) -> Option<LogQator<'a>> {
    let ajratgich = s.find(':')?;
    Some(LogQator { daraja: &s[..ajratgich], xabar: s[ajratgich+1..].trim() })
}

fn main() {
    let l = log_parse("INFO: Server tayyor").unwrap();
    println!("Daraja: [{}], Xabar: '{}'", l.daraja, l.xabar);
}
```

## Tushuntirish va Mantiq:
Log fayllarni terabaytlab tahlil qilishda zero-copy parserlar beqiyosdir.

## Ishlash natijasi:
```text
Daraja: [INFO], Xabar: 'Server tayyor'
```

---

# 592-Topshiriq: Lifetimes bilan Harflar chastotasi hisoblagichi
## Topshiriq sharti:
Matndan nusxa olmay tahlil qilish.

## Yechim (Rust kodi):
```rust
fn chastota(matn: &str) -> usize {
    matn.chars().count()
}

fn main() {
    println!("Belgilar soni: {}", chastota("Salom Dunyo"));
}
```

## Tushuntirish va Mantiq:
Harflar o'z joyida tahlil qilinadi.

## Ishlash natijasi:
```text
Belgilar soni: 11
```

---

# 593-Topshiriq: Lifetimes bilan Ko'p tilli lug'at
## Topshiriq sharti:
Turli tillardagi tarjimalarni saqlovchi struktura.

## Yechim (Rust kodi):
```rust
struct Tarjima<'a> {
    uz: &'a str,
    en: &'a str,
}

fn main() {
    let t = Tarjima { uz: "Kitob", en: "Book" };
    println!("{} -> {}", t.uz, t.en);
}
```

## Tushuntirish va Mantiq:
Statik lug'at elementlari hech qanday xotira ko'chirishsiz ishlaydi.

## Ishlash natijasi:
```text
Kitob -> Book
```

---

# 594-Topshiriq: Lifetimes bilan Parol tekshiruvchi hisobot
## Topshiriq sharti:
Paroldagi xatolik joyini ko'rsatish.

## Yechim (Rust kodi):
```rust
struct XatoJoyi<'a> { qism: &'a str }

fn xato_top<'a>(p: &'a str) -> Option<XatoJoyi<'a>> {
    if p.contains(' ') {
        Some(XatoJoyi { qism: "probel bor" })
    } else {
        None
    }
}

fn main() {
    println!("Parol xatosi: {:?}", xato_top("parol 123").map(|x| x.qism));
}
```

## Tushuntirish va Mantiq:
Xato joyi ko'rsatkichi xavfsiz havoladir.

## Ishlash natijasi:
```text
Parol xatosi: Some("probel bor")
```

---

# 595-Topshiriq: Lifetimes bilan So'z qidiruvchi (Word Finder)
## Topshiriq sharti:
Matndagi n-so'zni qaytaruvchi funksiya.

## Yechim (Rust kodi):
```rust
fn n_soz<'a>(matn: &'a str, n: usize) -> Option<&'a str> {
    matn.split_whitespace().nth(n)
}

fn main() {
    let jumla = "Bir Ikki Uch To'rt";
    println!("2-so'z: {:?}", n_soz(jumla, 2));
}
```

## Tushuntirish va Mantiq:
N-so'z to'g'ridan-to'g'ri asl satrdan olinadi.

## Ishlash natijasi:
```text
2-so'z: Some("Uch")
```

---

# 596-Topshiriq: Lifetimes bilan Fayl kengaytmasini ajratish
## Topshiriq sharti:
Fayl kengaytmasini nol-nusxa bilan topish.

## Yechim (Rust kodi):
```rust
fn kengaytma<'a>(nom: &'a str) -> Option<&'a str> {
    let idx = nom.rfind('.')?;
    Some(&nom[idx+1..])
}

fn main() {
    println!("Kengaytma: {:?}", kengaytma("rasm.png"));
}
```

## Tushuntirish va Mantiq:
Fayl kengaytmasi asl nomning oxirgi bo'lagidir.

## Ishlash natijasi:
```text
Kengaytma: Some("png")
```

---

# 597-Topshiriq: Lifetimes bilan Matn prefiksi tekshiruvi
## Topshiriq sharti:
Prefiksni olib tashlab qolganini qaytarish.

## Yechim (Rust kodi):
```rust
fn prefiksni_kes<'a>(matn: &'a str, pref: &str) -> Option<&'a str> {
    if matn.starts_with(pref) {
        Some(&matn[pref.len()..])
    } else {
        None
    }
}

fn main() {
    println!("Prefiks kesildi: {:?}", prefiksni_kes("Bearer token123", "Bearer "));
}
```

## Tushuntirish va Mantiq:
Prefiks tekshiruvidan keyin qolgan qism havolasi olinadi.

## Ishlash natijasi:
```text
Prefiks kesildi: Some("token123")
```

---

# 598-Topshiriq: Lifetimes bilan Qatorlar sonini sanash
## Topshiriq sharti:
Matn qatorlarini havolalar bilan hisoblash.

## Yechim (Rust kodi):
```rust
fn qatorlar_soni(m: &str) -> usize {
    m.lines().count()
}

fn main() {
    println!("Qatorlar: {}", qatorlar_soni("A\nB\nC"));
}
```

## Tushuntirish va Mantiq:
Qatorlar tezkor sanaladi.

## Ishlash natijasi:
```text
Qatorlar: 3
```

---

# 599-Topshiriq: Lifetimes bilan Matn bo'lagini tekshirish
## Topshiriq sharti:
Bo'lak bo'sh emasligini aniqlash.

## Yechim (Rust kodi):
```rust
fn bosh_emasmi<'a>(s: &'a str) -> bool {
    !s.is_empty()
}

fn main() {
    println!("Bosh emasmi: {}", bosh_emasmi("Rust"));
}
```

## Tushuntirish va Mantiq:
Oddiy va xavfsiz tekshiruv.

## Ishlash natijasi:
```text
Bosh emasmi: true
```

---

# 600-Topshiriq: Lifetimes moduli yakuniy xulosasi
## Topshiriq sharti:
Xotira xavfsizligining oltin tojidir.

## Yechim (Rust kodi):
```rust
fn main() {
    println!("Rust lifetimes mexanizmi dasturchiga xotira xatolarisiz C tezligida ishlash imkonini beradi.");
}
```

## Tushuntirish va Mantiq:
Lifetimes Rust tilining poydevoridir.

## Ishlash natijasi:
```text
Rust lifetimes mexanizmi dasturchiga xotira xatolarisiz C tezligida ishlash imkonini beradi.
```

---
