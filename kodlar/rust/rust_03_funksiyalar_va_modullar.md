# 3-Qism: Funksiyalar, Modullar va Dastur Arxitekturasi (101-150)

Ushbu qismda Rust tilidagi funksiyalarning to'liq sintaksisi, parametrlar, ifodalar (expressions) va ko'rsatmalar (statements), erta chiqish, rekursiya, divergensiya (`-> !`), konstanta funksiyalar (`const fn`), funksiya ko'rsatkichlari (`fn pointer`), shuningdek, Rust ning modul tizimi (`mod`, `pub`, `use`, `super`, `pub(crate)`), ko'rinish doiralari va atributlari amaliy tahlil qilinadi.

---

# 101-Topshiriq: Funksiya deklaratsiyasi: fn nomi()
## Topshiriq sharti:
Oddiy xabarni konsolga chiqaruvchi mustaqil yordamchi funksiya yarating va uni `main` ichidan chaqiring.

## Yechim (Rust kodi):
```rust
fn salom_ber() {
    println!("Assalomu alaykum! Funksiyalar olamiga xush kelibsiz.");
}

fn main() {
    salom_ber();
    salom_ber();
}
```

## Tushuntirish va Mantiq:
Rust da funksiyalar `fn` kalit so'zi bilan e'lon qilinadi. Funksiya nomlari Rust konvensiyasiga binoan `snake_case` uslubida yoziladi.

## Ishlash natijasi:
```text
Assalomu alaykum! Funksiyalar olamiga xush kelibsiz.
Assalomu alaykum! Funksiyalar olamiga xush kelibsiz.
```

---

# 102-Topshiriq: Parametrlarga ega funksiyalar va qat'iy tip annotatsiyasi
## Topshiriq sharti:
Foydalanuvchi ismi va yoshini qabul qilib, ma'lumot beruvchi funksiya yozing.

## Yechim (Rust kodi):
```rust
fn foydalanuvchi_haqida(ism: &str, yosh: u8) {
    println!("Foydalanuvchi: {}, Yoshi: {} da.", ism, yosh);
}

fn main() {
    foydalanuvchi_haqida("Sardor", 24);
}
```

## Tushuntirish va Mantiq:
Rust da funksiya imzolarida (signature) har bir parametrning turi qat'iy va aniq ko'rsatilishi shart. Kompilyator funksiya parametrlarida turni taxmin qilmaydi.

## Ishlash natijasi:
```text
Foydalanuvchi: Sardor, Yoshi: 24 da.
```

---

# 103-Topshiriq: Qaytish qiymatiga ega funksiyalar (-> T)
## Topshiriq sharti:
Ikkita sonning yig'indisini hisoblab qaytaruvchi funksiya yozing.

## Yechim (Rust kodi):
```rust
fn qoshish(a: i32, b: i32) -> i32 {
    a + b // Nuqta-vergulsiz oxirgi qator - avtomatik qaytish qiymati
}

fn main() {
    let natija = qoshish(15, 27);
    println!("15 + 27 = {}", natija);
}
```

## Tushuntirish va Mantiq:
Qaytish qiymati strelka `-> T` belgisi bilan belgilanadi. Rust da oxirgi ifoda nuqta-vergulsiz qoldirilsa, u to'g'ridan-to'g'ri qaytariladi.

## Ishlash natijasi:
```text
15 + 27 = 42
```

---

# 104-Topshiriq: Ko'rsatmalar (Statements) vs Ifodalar (Expressions)
## Topshiriq sharti:
Nuqta-vergulning ifodani ko'rsatmaga aylantirishini va blok ichidan qiymat qaytishini ko'rsating.

## Yechim (Rust kodi):
```rust
fn main() {
    let y = {
        let x = 3;
        x + 1 // Agar oxiriga ';' qo'yilsa, () qaytadi
    };

    println!("y ning qiymati: {}", y);
}
```

## Tushuntirish va Mantiq:
Ko'rsatma (statement) harakatni bajaradi, lekin qiymat qaytarmaydi (oxirida `;` bo'ladi). Ifoda (expression) esa qiymat hisoblaydi va natija qaytaradi.

## Ishlash natijasi:
```text
y ning qiymati: 4
```

---

# 105-Topshiriq: return kalit so'zi orqali erta chiqish (Early Return)
## Topshiriq sharti:
Agar son nolga teng bo'lsa, hisob-kitobni to'xtatib erta chiqib ketuvchi funksiya tuzing.

## Yechim (Rust kodi):
```rust
fn xavfsiz_bolish(bolinuvchi: f64, boluvchi: f64) -> f64 {
    if boluvchi == 0.0 {
        println!("Ogohlantirish: Nolga bo'lish aniqlanmadi!");
        return 0.0; // Erta chiqish
    }
    bolinuvchi / boluvchi
}

fn main() {
    let javob = xavfsiz_bolish(100.0, 0.0);
    println!("Natija: {}", javob);
}
```

## Tushuntirish va Mantiq:
`return` kalit so'zi odatda shart bajarilganda funksiyadan muddatidan oldin (erta) chiqish uchun ishlatiladi.

## Ishlash natijasi:
```text
Ogohlantirish: Nolga bo'lish aniqlanmadi!
Natija: 0
```

---

# 106-Topshiriq: Kortej orqali bir nechta qiymat qaytarish
## Topshiriq sharti:
To'g'ri to'rtburchakning yuzi va perimetrini bitta funksiyadan qaytaring.

## Yechim (Rust kodi):
```rust
fn hisobla_tortburchak(a: f64, b: f64) -> (f64, f64) {
    let yuza = a * b;
    let perimetr = 2.0 * (a + b);
    (yuza, perimetr)
}

fn main() {
    let (yuzi, perimetri) = hisobla_tortburchak(5.0, 3.0);
    println!("Yuza: {}, Perimetr: {}", yuzi, perimetri);
}
```

## Tushuntirish va Mantiq:
Rust da bir nechta qiymat qaytarish uchun kortej (tuple) ishlatiladi. Qabul qiluvchi tomonda uni destructuring orqali alohida o'zgaruvchilarga olish mumkin.

## Ishlash natijasi:
```text
Yuza: 15, Perimetr: 16
```

---

# 107-Topshiriq: Funksiyaga argumentlarni qiymat bo'yicha (Pass by Value) uzatish
## Topshiriq sharti:
Primitiv nusxalanuvchi (Copy) turlarning funksiyaga uzatilganda asl nusxasi o'zgarmasligini ko'rsating.

## Yechim (Rust kodi):
```rust
fn qiymatni_oshir(mut x: i32) {
    x += 10;
    println!("Funksiya ichida x: {}", x);
}

fn main() {
    let son = 5;
    qiymatni_oshir(son);
    println!("Asl son main ichida: {}", son);
}
```

## Tushuntirish va Mantiq:
`i32` tipi `Copy` xususiyatiga ega bo'lgani sababli, funksiyaga uning to'liq nusxasi beriladi. Funksiya ichidagi o'zgarishlar tashqi o'zgaruvchiga aslo ta'sir qilmaydi.

## Ishlash natijasi:
```text
Funksiya ichida x: 15
Asl son main ichida: 5
```

---

# 108-Topshiriq: Rekursiv funksiya: Faktorial hisoblash
## Topshiriq sharti:
O'z-o'zini chaqiruvchi rekursiv faktorial funksiyasini yozing.

## Yechim (Rust kodi):
```rust
fn faktorial(n: u64) -> u64 {
    if n <= 1 {
        1
    } else {
        n * faktorial(n - 1)
    }
}

fn main() {
    let n = 5;
    println!("{}! = {}", n, faktorial(n));
}
```

## Tushuntirish va Mantiq:
Rekursiyada to'xtash sharti (base case: `n <= 1`) bo'lishi shart, aks holda dastur Stack xotirasini to'ldirib yuboradi (Stack Overflow).

## Ishlash natijasi:
```text
5! = 120
```

---

# 109-Topshiriq: Rekursiv funksiya: Fibonachchi soni
## Topshiriq sharti:
Klassik rekursiya orqali N-Fibonachchi sonini topuvchi funksiya tuzing.

## Yechim (Rust kodi):
```rust
fn fib(n: u32) -> u32 {
    match n {
        0 => 0,
        1 => 1,
        _ => fib(n - 1) + fib(n - 2),
    }
}

fn main() {
    println!("Fibonachchi (7): {}", fib(7));
}
```

## Tushuntirish va Mantiq:
Rust da `match` rekursiv funksiyalarda asosiy va rekursiv shartlarni aniq va go'zal ajratish imkonini beradi.

## Ishlash natijasi:
```text
Fibonachchi (7): 13
```

---

# 110-Topshiriq: Quyruq rekursiyasi (Tail Recursion) va akkumulyator
## Topshiriq sharti:
Akkumulyator orqali rekursiya chuqurligini optimallashtiruvchi faktorial tuzing.

## Yechim (Rust kodi):
```rust
fn faktorial_tail(n: u64, acc: u64) -> u64 {
    if n <= 1 {
        acc
    } else {
        faktorial_tail(n - 1, n * acc)
    }
}

fn main() {
    println!("6! (tail recursive) = {}", faktorial_tail(6, 1));
}
```

## Tushuntirish va Mantiq:
Quyruq rekursiyasida funksiya qaytaradigan oxirgi amal faqat o'zini chaqirishdan iborat bo'ladi. Bu zamonaviy kompilyatorlarga tsikl shakliga o'tkazish imkonini beradi.

## Ishlash natijasi:
```text
6! (tail recursive) = 720
```

---

# 111-Topshiriq: Ackermann funksiyasi: Chuqur rekursiya xatti-harakati
## Topshiriq sharti:
Matematikadagi o'ta tez o'suvchi Ackermann funksiyasini amalga oshiring.

## Yechim (Rust kodi):
```rust
fn ackermann(m: u32, n: u32) -> u32 {
    if m == 0 {
        n + 1
    } else if n == 0 {
        ackermann(m - 1, 1)
    } else {
        ackermann(m - 1, ackermann(m, n - 1))
    }
}

fn main() {
    println!("Ackermann(2, 3) = {}", ackermann(2, 3));
}
```

## Tushuntirish va Mantiq:
Ackermann funksiyasi oddiy primitiv rekursiv bo'lmagan funksiyalarning yorqin namunasidir. U kichik argumentlarda ham katta hisob-kitob talab etadi.

## Ishlash natijasi:
```text
Ackermann(2, 3) = 9
```

---

# 112-Topshiriq: Xanoy minoralari (Towers of Hanoi) boshqaruvi
## Topshiriq sharti:
Diskchalarni A ustundan C ustunga B orqali ko'chirish qadamlarini chop etuvchi rekursiv funksiya yozing.

## Yechim (Rust kodi):
```rust
fn hanoi(n: u32, bosh: char, yordamchi: char, maqsad: char) {
    if n == 1 {
        println!("Disk 1: {} -> {}", bosh, maqsad);
        return;
    }
    hanoi(n - 1, bosh, maqsad, yordamchi);
    println!("Disk {}: {} -> {}", n, bosh, maqsad);
    hanoi(n - 1, yordamchi, bosh, maqsad);
}

fn main() {
    println!("3 ta disk uchun Xanoy ko'chirishlari:");
    hanoi(3, 'A', 'B', 'C');
}
```

## Tushuntirish va Mantiq:
Xanoy minorasi algoritmi 2^n - 1 ta qadamda diskchalarni tartibli ko'chiradi va rekursiv fikrlashni rivojlantiradi.

## Ishlash natijasi:
```text
3 ta disk uchun Xanoy ko'chirishlari:
Disk 1: A -> C
Disk 2: A -> B
Disk 1: C -> B
Disk 3: A -> C
Disk 1: B -> A
Disk 2: B -> C
Disk 1: A -> C
```

---

# 113-Topshiriq: Diversiya qiluvchi (Diverging) funksiyalar: -> !
## Topshiriq sharti:
Hech qachon chaqiruvchiga qaytib kelmaydigan `!` (never) turidagi funksiya yozing.

## Yechim (Rust kodi):
```rust
fn halokatli_xato(xabar: &str) -> ! {
    panic!("Kritik xatolik: {}", xabar);
}

fn main() {
    let shart = true;
    if shart {
        println!("Dastur normal ishlamoqda.");
    } else {
        halokatli_xato("Kutilmagan holat yuz berdi!");
    }
}
```

## Tushuntirish va Mantiq:
`!` tipi 'never type' deb ataladi. U funksiyaning hech qachon normal qaytmasligini (dastur to'xtashini yoki cheksiz aylanib qolishini) bildiradi.

## Ishlash natijasi:
```text
Dastur normal ishlamoqda.
```

---

# 114-Topshiriq: const fn: Kompilyatsiya vaqtida hisoblanuvchi funksiyalar
## Topshiriq sharti:
`const fn` kalit so'zi orqali natijasi kompilyatsiyada aniqlanadigan funksiya tuzing.

## Yechim (Rust kodi):
```rust
const fn kvadrat(x: u32) -> u32 {
    x * x
}

const MAYDON: u32 = kvadrat(10); // Kompilyatsiya vaqtida 100 deb belgilanadi

fn main() {
    println!("Kompilyatsiyada hisoblangan maydon: {}", MAYDON);
}
```

## Tushuntirish va Mantiq:
`const fn` kompilyatsiya bosqichida statik konstantalarni hisoblash imkonini beradi. Uning ichida faqat deterministik va xavfsiz amallar bajarilishi mumkin.

## Ishlash natijasi:
```text
Kompilyatsiyada hisoblangan maydon: 100
```

---

# 115-Topshiriq: const fn yordamida massiv hajmini belgilash
## Topshiriq sharti:
Kompilyatsiya vaqtida funksiya natijasiga asoslanib massiv o'lchamini `[i32; HAJM]` qilib belgilang.

## Yechim (Rust kodi):
```rust
const fn hisobla_hajm(pogona: usize) -> usize {
    pogona * 4
}

const BUFER_HAJMI: usize = hisobla_hajm(8); // 32

fn main() {
    let bufer: [u8; BUFER_HAJMI] = [0; BUFER_HAJMI];
    println!("Bufer massiv uzunligi: {}", bufer.len());
}
```

## Tushuntirish va Mantiq:
Rust da massiv o'lchami har doim kompilyatsiya vaqtidagi konstanta bo'lishi shart. `const fn` bu talabni nolinchi xarajat bilan ta'minlaydi.

## Ishlash natijasi:
```text
Bufer massiv uzunligi: 32
```

---

# 116-Topshiriq: Funksiya ko'rsatkichlari (Function Pointers: fn(T) -> R)
## Topshiriq sharti:
Funksiyani o'zgaruvchida saqlang va uni boshqa nom bilan chaqiring.

## Yechim (Rust kodi):
```rust
fn kub(x: i32) -> i32 {
    x * x * x
}

fn main() {
    let f: fn(i32) -> i32 = kub;
    let javob = f(4);

    println!("Kub (4): {}", javob);
}
```

## Tushuntirish va Mantiq:
`fn(T) -> R` bu funksiya ko'rsatkichi (function pointer) bo'lib, xotiradagi funksiya kodining manziliga ishora qiladi.

## Ishlash natijasi:
```text
Kub (4): 64
```

---

# 117-Topshiriq: Funksiyani boshqa funksiyaga parametr sifatida uzatish (Yuqori tartibli funksiya)
## Topshiriq sharti:
Boshqa funksiyani argument sifatida qabul qilib, uni son ustida qo'llovchi funksiya yozing.

## Yechim (Rust kodi):
```rust
fn ikki_hissa(x: i32) -> i32 {
    x * 2
}

fn qollash(qiymat: i32, amal: fn(i32) -> i32) -> i32 {
    amal(qiymat)
}

fn main() {
    let natija = qollash(25, ikki_hissa);
    println!("Natija: {}", natija);
}
```

## Tushuntirish va Mantiq:
Funksiya ko'rsatkichlari orqali strategiya andozasi (Strategy Pattern) va moslashuvchan arxitekturalarni amalga oshirish mumkin.

## Ishlash natijasi:
```text
Natija: 50
```

---

# 118-Topshiriq: Funksiya ko'rsatkichlaridan iborat massiv
## Topshiriq sharti:
Bir nechta matematik amallarni massivda saqlab, tsiklda ketma-ket bajaring.

## Yechim (Rust kodi):
```rust
fn kvadrat(x: i32) -> i32 { x * x }
fn kub(x: i32) -> i32 { x * x * x }
fn inkor(x: i32) -> i32 { -x }

fn main() {
    let amallar: [fn(i32) -> i32; 3] = [kvadrat, kub, inkor];
    let son = 3;

    for amal in amallar {
        println!("Amal natijasi ({}): {}", son, amal(son));
    }
}
```

## Tushuntirish va Mantiq:
Bir xil imzoga ega bo'lgan funksiyalar massivlarda yoki kolleksiyalarda saqlanishi va dinamik ravishda navbati bilan chaqirilishi mumkin.

## Ishlash natijasi:
```text
Amal natijasi (3): 9
Amal natijasi (3): 27
Amal natijasi (3): -3
```

---

# 119-Topshiriq: Ichki funksiyalar (Nested Functions) e'lon qilish
## Topshiriq sharti:
Funksiya tanasi ichida faqat o'sha yerda kerak bo'ladigan yordamchi funksiya yarating.

## Yechim (Rust kodi):
```rust
fn tashqi_hisob(a: i32, b: i32) -> i32 {
    fn ichki_modul(x: i32) -> i32 {
        if x < 0 { -x } else { x }
    }

    ichki_modul(a) + ichki_modul(b)
}

fn main() {
    let res = tashqi_hisob(-15, 20);
    println!("Modullar yig'indisi: {}", res);
}
```

## Tushuntirish va Mantiq:
Rust da funksiyalar boshqa funksiyalar ichida e'lon qilinishi mumkin. Ular tashqi funksiyaning lokal o'zgaruvchilarini ushlay olmaydi, bu ularni xavfsiz qiladi.

## Ishlash natijasi:
```text
Modullar yig'indisi: 35
```

---

# 120-Topshiriq: Modul tizimiga kirish: mod kalit so'zi
## Topshiriq sharti:
`mod` yordamida mantiqiy kod guruhini (modul) hosil qiling.

## Yechim (Rust kodi):
```rust
mod xabar {
    pub fn salom() {
        println!("Xabar moduli: Xush kelibsiz!");
    }
}

fn main() {
    xabar::salom();
}
```

## Tushuntirish va Mantiq:
`mod` kalit so'zi kodni alohida nomlar maydoniga (namespace) ajratadi. Boshqa qismdan chaqirish uchun `modul_nomi::funksiya()` yo'li ishlatiladi.

## Ishlash natijasi:
```text
Xabar moduli: Xush kelibsiz!
```

---

# 121-Topshiriq: pub kalit so'zi va ochiqlik (Visibility) qoidalari
## Topshiriq sharti:
Moduldagi ochiq (public) va yopiq (private) funksiyalar farqini ko'rsating.

## Yechim (Rust kodi):
```rust
mod ombor {
    pub fn ochiq_tovar() {
        println!("Hamma ko'ra oladigan tovarlar.");
        yashirin_xisobot();
    }

    fn yashirin_xisobot() {
        println!("Faqat ombor ichida ko'rinadigan maxfiy hisobot.");
    }
}

fn main() {
    ombor::ochiq_tovar();
    // ombor::yashirin_xisobot(); // Xatolik: funksiya private!
}
```

## Tushuntirish va Mantiq:
Rust da hamma narsa standart bo'yicha yopiq (private) bo'ladi. Tashqaridan murojaat qilish uchun `pub` kalit so'zi qo'shilishi shart.

## Ishlash natijasi:
```text
Hamma ko'ra oladigan tovarlar.
Faqat ombor ichida ko'rinadigan maxfiy hisobot.
```

---

# 122-Topshiriq: Ichma-ich modullar (Nested Modules)
## Topshiriq sharti:
Modul ichida boshqa modul joylashtiring va chuqur yo'l bilan kiring.

## Yechim (Rust kodi):
```rust
mod tarmoq {
    pub mod xavfsizlik {
        pub fn shifrlash() {
            println!("Tarmoq trafigi shifrlanmoqda (AES-256)...");
        }
    }
}

fn main() {
    tarmoq::xavfsizlik::shifrlash();
}
```

## Tushuntirish va Mantiq:
Ichma-ich modullar murakkab tizimlarni daraxtsimon ierarxiyaga bo'lib, tartibli loyihalash imkonini beradi.

## Ishlash natijasi:
```text
Tarmoq trafigi shifrlanmoqda (AES-256)...
```

---

# 123-Topshiriq: use kalit so'zi orqali modul yo'lini qisqartirish
## Topshiriq sharti:
Uzoq yo'lni `use` orqali joriy doiraga olib kiring.

## Yechim (Rust kodi):
```rust
mod matematika {
    pub mod geometriya {
        pub fn doira_yuzi(radius: f64) -> f64 {
            3.14159 * radius * radius
        }
    }
}

use matematika::geometriya::doira_yuzi;

fn main() {
    let yuza = doira_yuzi(5.0);
    println!("Doira yuzi: {:.2}", yuza);
}
```

## Tushuntirish va Mantiq:
`use` kalit so'zi uzun nomlar maydonini qisqartirib, funksiyani xuddi joriy faylda yozilgandek bevosita chaqirishga imkon beradi.

## Ishlash natijasi:
```text
Doira yuzi: 78.54
```

---

# 124-Topshiriq: as kalit so'zi yordamida import nomini qayta nomlash
## Topshiriq sharti:
Bir xil nomli ikkita funksiyani to'qnashuvsiz import qilish uchun `as` dan foydalaning.

## Yechim (Rust kodi):
```rust
mod modul_a {
    pub fn ishla() { println!("Modul A ishlamoqda"); }
}
mod modul_b {
    pub fn ishla() { println!("Modul B ishlamoqda"); }
}

use modul_a::ishla as ishla_a;
use modul_b::ishla as ishla_b;

fn main() {
    ishla_a();
    ishla_b();
}
```

## Tushuntirish va Mantiq:
`use path as YangiNom` sintaksisi nomlar to'qnashuvini (naming collision) bartaraf etadi va kod ravshanligini oshiradi.

## Ishlash natijasi:
```text
Modul A ishlamoqda
Modul B ishlamoqda
```

---

# 125-Topshiriq: super kalit so'zi: Ota modulga (Parent Module) murojaat
## Topshiriq sharti:
Ichki moduldan o'zining ota modulidagi funksiyani chaqiring.

## Yechim (Rust kodi):
```rust
fn global_server_porti() -> u16 {
    8080
}

mod server {
    pub fn ishga_tushur() {
        let port = super::global_server_porti();
        println!("Server {}-portda ishga tushdi.", port);
    }
}

fn main() {
    server::ishga_tushur();
}
```

## Tushuntirish va Mantiq:
`super` fayl tizimidagi `..` (yuqori papka) kabi ishlaydi va ichki moduldan turib bevosita yuqoridagi ota modul elementlariga kirish imkonini beradi.

## Ishlash natijasi:
```text
Server 8080-portda ishga tushdi.
```

---

# 126-Topshiriq: self kalit so'zi: Joriy modulga aniq murojaat
## Topshiriq sharti:
`self::` orqali joriy doiradagi funksiyaga murojaat qiling.

## Yechim (Rust kodi):
```rust
mod hisob {
    pub fn oraliq() {
        println!("Oraliq hisob");
    }

    pub fn umumiy() {
        self::oraliq();
        println!("Umumiy yakun");
    }
}

fn main() {
    hisob::umumiy();
}
```

## Tushuntirish va Mantiq:
`self` joriy modul doirasini bildiradi (`./` kabi) va import zanjirlarida nomlarni aniqlashtirish uchun xizmat qiladi.

## Ishlash natijasi:
```text
Oraliq hisob
Umumiy yakun
```

---

# 127-Topshiriq: pub(crate) orqali butun loyiha doirasida ko'rinish
## Topshiriq sharti:
Faqat joriy crate ichida ko'rinadigan, ammo tashqi mijozlarga yopiq bo'lgan element yarating.

## Yechim (Rust kodi):
```rust
mod ichki_yadro {
    pub(crate) fn yadro_funksiyasi() {
        println!("Bu funksiya butun crate bo'ylab ochiq, ammo tashqariga yopiq.");
    }
}

fn main() {
    ichki_yadro::yadro_funksiyasi();
}
```

## Tushuntirish va Mantiq:
`pub(crate)` kutubxona yoki loyiha ichida barcha modullarga kirish huquqini beradi, lekin loyiha kutubxona sifatida boshqalar tomonidan ishlatilganda tashqi API ga chiqarmaydi.

## Ishlash natijasi:
```text
Bu funksiya butun crate bo'ylab ochiq, ammo tashqariga yopiq.
```

---

# 128-Topshiriq: pub(super) orqali faqat bevosita ota modulga ruxsat berish
## Topshiriq sharti:
Ichki modul elementini faqat uning otasiga ko'rinadigan qiling.

## Yechim (Rust kodi):
```rust
mod ota {
    pub mod bola {
        pub(super) fn faqat_otaga() {
            println!("Faqat ota modulga ko'rinuvchi maxfiy xizmat.");
        }
    }

    pub fn sinov() {
        bola::faqat_otaga();
    }
}

fn main() {
    ota::sinov();
}
```

## Tushuntirish va Mantiq:
`pub(super)` cheklangan ko'rinish beradi: faqat bir pog'ona yuqoridagi modul ushbu elementdan foydalana oladi.

## Ishlash natijasi:
```text
Faqat ota modulga ko'rinuvchi maxfiy xizmat.
```

---

# 129-Topshiriq: Modul ichida ochiq konstantalar va turlarni saqlash
## Topshiriq sharti:
Modul ichida `pub const` qiymatlarni saqlang va tashqaridan kiring.

## Yechim (Rust kodi):
```rust
mod fizika {
    pub const YORUGLIK_TEZLIGI: f64 = 299_792_458.0; // m/s
    pub const GRAVITATSIYA: f64 = 9.80665; // m/s^2
}

fn main() {
    println!("Yorug'lik tezligi: {} m/s", fizika::YORUGLIK_TEZLIGI);
    println!("Erkin tushish tezlanishi: {} m/s^2", fizika::GRAVITATSIYA);
}
```

## Tushuntirish va Mantiq:
Modullar nafaqat funksiyalarni, balki umumiy konstantalar, turlar va strukturalarni ham o'z ichiga oluvchi to'laqonli kutubxonachadir.

## Ishlash natijasi:
```text
Yorug'lik tezligi: 299792458 m/s
Erkin tushish tezlanishi: 9.80665 m/s^2
```

---

# 130-Topshiriq: pub use (Re-exporting) orqali toza tashqi API taqdim etish
## Topshiriq sharti:
Chuqur modul ichidagi funksiyani `pub use` yordamida tashqi darajaga olib chiqing.

## Yechim (Rust kodi):
```rust
mod ichki {
    pub mod dvigatel {
        pub fn start() {
            println!("Dvigatel 100% quvvatda ishga tushdi!");
        }
    }
}

// Re-export qilamiz
pub use ichki::dvigatel::start as dvigatelni_yoq;

fn main() {
    dvigatelni_yoq(); // Chuqur yo'lsiz to'g'ridan-to'g'ri chaqiramiz
}
```

## Tushuntirish va Mantiq:
`pub use` re-export mexanizmi kutubxona ichki murakkab strukturasini yashirib, foydalanuvchiga sodda va qulay interfeys yaratish imkonini beradi.

## Ishlash natijasi:
```text
Dvigatel 100% quvvatda ishga tushdi!
```

---

# 131-Topshiriq: Hujjatlashtirish izohlari (Doc Comments: ///)
## Topshiriq sharti:
Funksiya uchun Markdown formatidagi hujjat izohlarini yozing.

## Yechim (Rust kodi):
```rust
/// Ikkita sonning kattasini aniqlaydi.
///
/// # Misol
/// ```rust
/// let m = kattasi(10, 20);
/// assert_eq!(m, 20);
/// ```
fn kattasi(a: i32, b: i32) -> i32 {
    if a > b { a } else { b }
}

fn main() {
    println!("Kattasi: {}", kattasi(45, 92));
}
```

## Tushuntirish va Mantiq:
`///` izohlari `cargo doc` buyrug'i orqali avtomatik HTML hujjatlar sahifasiga aylanadi. Undagi kod bloklari esa `cargo test` da avtomatik test qilinadi.

## Ishlash natijasi:
```text
Kattasi: 92
```

---

# 132-Topshiriq: Modul darajasidagi hujjat izohlari (//! Module Docs)
## Topshiriq sharti:
Modul yoki crate boshida uning maqsadini tushuntiruvchi `//!` izohlarini qo'llang.

## Yechim (Rust kodi):
```rust
//! # Kripto Yordamchilar Moduli
//! Ushbu modul hash va xavfsizlik funksiyalarini o'z ichiga oladi.

mod hash {
    pub fn oddiy_hash(matn: &str) -> usize {
        matn.len() * 31
    }
}

fn main() {
    let h = hash::oddiy_hash("Rust2024");
    println!("Matn xash qiymati: {}", h);
}
```

## Tushuntirish va Mantiq:
`//!` izohlari o'zi joylashgan modul yoki faylning to'liq tavsifini beradi va hujjat sahifasining yuqori qismiga chiqadi.

## Ishlash natijasi:
```text
Matn xash qiymati: 248
```

---

# 133-Topshiriq: #[inline] atributi va funksiya chaqiruvini optimizatsiyalash
## Topshiriq sharti:
Tez chaqiriladigan kichik funksiyani inline qilish uchun atribut bering.

## Yechim (Rust kodi):
```rust
#[inline]
fn tezkor_qosh(a: i32, b: i32) -> i32 {
    a + b
}

fn main() {
    let s = tezkor_qosh(10, 20);
    println!("Yig'indi: {}", s);
}
```

## Tushuntirish va Mantiq:
`#[inline]` kompilyatorga funksiya chaqiruvi o'rniga uning kodini bevosita chaqirilgan joyga joylashtirishni (funksiya chaqirish xarajatini nolga tushirishni) tavsiya qiladi.

## Ishlash natijasi:
```text
Yig'indi: 30
```

---

# 134-Topshiriq: #[deprecated] atributi: Eskirgan funksiyalar haqida bildirish
## Topshiriq sharti:
Kelgusida olib tashlanadigan funksiyani eskirgan deb belgilang.

## Yechim (Rust kodi):
```rust
#[deprecated(since = "2.0.0", note = "Iltimos, yangi_hisob() funksiyasidan foydalaning")]
fn eski_hisob() {
    println!("Eski tizim ishladi.");
}

fn main() {
    #[allow(deprecated)]
    eski_hisob();
}
```

## Tushuntirish va Mantiq:
`#[deprecated]` atributi kompilyatorga ushbu funksiya ishlatilganda dasturchiga ogohlantirish (warning) chiqarishni buyuradi.

## Ishlash natijasi:
```text
Eski tizim ishladi.
```

---

# 135-Topshiriq: #[allow(unused_variables)] orqali ogohlantirishlarni nazorat qilish
## Topshiriq sharti:
Hali ishlatilmagan o'zgaruvchilar uchun kompilyator ogohlantirishini o'chirish.

## Yechim (Rust kodi):
```rust
fn main() {
    #[allow(unused_variables)]
    let x = 100; // Kompilyator warning chiqarmaydi

    println!("Dastur toza kompilatsiya bo'ldi.");
}
```

## Tushuntirish va Mantiq:
Rust kompilyatori ishlatilmagan o'zgaruvchilarni qat'iy nazorat qiladi. `#[allow(...)]` orqali prototiplash davrida kerakli ogohlantirishlarni o'chirib turish mumkin.

## Ishlash natijasi:
```text
Dastur toza kompilatsiya bo'ldi.
```

---

# 136-Topshiriq: Modulli arxitektura: Geometriya kalkulyatori
## Topshiriq sharti:
Aylana, to'g'ri to'rtburchak va uchburchak yuzasini hisoblovchi tartibli modul tuzing.

## Yechim (Rust kodi):
```rust
mod shakllar {
    pub const PI: f64 = 3.1415926535;

    pub fn doira_yuzi(r: f64) -> f64 {
        PI * r * r
    }

    pub fn tortburchak_yuzi(a: f64, b: f64) -> f64 {
        a * b
    }

    pub fn uchburchak_yuzi(asos: f64, balandlik: f64) -> f64 {
        0.5 * asos * balandlik
    }
}

fn main() {
    println!("Doira: {:.2}", shakllar::doira_yuzi(4.0));
    println!("To'rtburchak: {:.2}", shakllar::tortburchak_yuzi(4.0, 6.0));
    println!("Uchburchak: {:.2}", shakllar::uchburchak_yuzi(5.0, 8.0));
}
```

## Tushuntirish va Mantiq:
Geometrik vazifalarni modulga jamlash kodni qayta ishlatish (reusability) va loyiha tartibini oshiradi.

## Ishlash natijasi:
```text
Doira: 50.27
To'rtburchak: 24.00
Uchburchak: 20.00
```

---

# 137-Topshiriq: Modulli arxitektura: Harorat konvertori
## Topshiriq sharti:
Selsiy, Farengeyt va Kelvin shkalalari o'rtasida o'tish modulini yarating.

## Yechim (Rust kodi):
```rust
mod harorat {
    pub fn c_to_f(c: f64) -> f64 {
        c * 1.8 + 32.0
    }

    pub fn f_to_c(f: f64) -> f64 {
        (f - 32.0) / 1.8
    }

    pub fn c_to_k(c: f64) -> f64 {
        c + 273.15
    }
}

fn main() {
    let c = 25.0;
    println!("{}°C = {:.1}°F", c, harorat::c_to_f(c));
    println!("{}°C = {:.2} K", c, harorat::c_to_k(c));
}
```

## Tushuntirish va Mantiq:
Bir-biriga bog'liq matematik formulalarni modul ichida enkapsulyatsiya qilish xatoliklarni kamaytiradi.

## Ishlash natijasi:
```text
25°C = 77.0°F
25°C = 298.15 K
```

---

# 138-Topshiriq: Funksiyalar zanjiri (Function Piping) modeli
## Topshiriq sharti:
Bitta funksiya natijasini ikkinchisiga uzatish orqali ma'lumotni bosqichma-bosqich qayta ishlang.

## Yechim (Rust kodi):
```rust
fn tozalash(matn: &str) -> &str {
    matn.trim()
}

fn uzunlikni_ol(matn: &str) -> usize {
    matn.len()
}

fn kvadrat_qil(n: usize) -> usize {
    n * n
}

fn main() {
    let xom_matn = "   Rust tili   ";
    let natija = kvadrat_qil(uzunlikni_ol(tozalash(xom_matn)));

    println!("Qayta ishlash yakuni: {}", natija);
}
```

## Tushuntirish va Mantiq:
Funksional kompozitsiya ma'lumotlarni o'zgarishsiz (immutable) holatda bir bosqichdan ikkinchisiga uzatish imkonini beradi.

## Ishlash natijasi:
```text
Qayta ishlash yakuni: 81
```

---

# 139-Topshiriq: Binary Exponentiation: Sonning darajasini tezkor O(log N) da hisoblash
## Topshiriq sharti:
Katta darajalarni logarifmik qadamda hisoblovchi rekursiv/iterativ funksiya yozing.

## Yechim (Rust kodi):
```rust
fn tezkor_daraja(mut asos: u64, mut daraja: u32) -> u64 {
    let mut natija = 1;
    while daraja > 0 {
        if daraja % 2 == 1 {
            natija *= asos;
        }
        asos *= asos;
        daraja /= 2;
    }
    natija
}

fn main() {
    let asos = 3;
    let exp = 10;
    println!("{}^{} = {}", asos, exp, tezkor_daraja(asos, exp));
}
```

## Tushuntirish va Mantiq:
Binary exponentiation 3^10 ni 10 ta ko'paytirish o'rniga atigi 4 ta qadamda hisoblaydi, bu algoritmlar samaradorligini keskin oshiradi.

## Ishlash natijasi:
```text
3^10 = 59049
```

---

# 140-Topshiriq: Kvadrat ildizni Nyuton usulida (Newton-Raphson) yaqinlashtirish
## Topshiriq sharti:
Matematik yaqinlashish iteratsiyasi orqali kvadrat ildiz hisoblovchi funksiya tuzing.

## Yechim (Rust kodi):
```rust
fn nyuton_ildiz(son: f64) -> f64 {
    if son < 0.0 { return f64::NAN; }
    let mut taxmin = son / 2.0;
    for _ in 0..20 {
        taxmin = 0.5 * (taxmin + son / taxmin);
    }
    taxmin
}

fn main() {
    let x = 49.0;
    println!("{} sonining ildizi: {:.4}", x, nyuton_ildiz(x));
}
```

## Tushuntirish va Mantiq:
Nyuton usuli har bir iteratsiyada aniqlikni ikki barobar oshiradi va apparat darajasida float ildiz olishning asosiy tamoyilidir.

## Ishlash natijasi:
```text
49 sonining ildizi: 7.0000
```

---

# 141-Topshiriq: Valyuta konvertori funksiyasi
## Topshiriq sharti:
So'm, Dollar va Yevro kurslarini hisoblovchi funksiya yozing.

## Yechim (Rust kodi):
```rust
fn somga_otkaz(miqdor: f64, valyuta: &str) -> f64 {
    let kurs = match valyuta {
        "USD" => 12800.0,
        "EUR" => 13900.0,
        "RUB" => 140.0,
        _ => 1.0,
    };
    miqdor * kurs
}

fn main() {
    let dollar = 100.0;
    let sobiq_som = somga_otkaz(dollar, "USD");
    println!("${} = {} so'm", dollar, sobiq_som);
}
```

## Tushuntirish va Mantiq:
Pattern matching va funksiyalar yordamida moliyaviy hisob-kitoblar oson va xatosiz modellashtiriladi.

## Ishlash natijasi:
```text
$100 = 1280000 so'm
```

---

# 142-Topshiriq: Massivni joyida teskari o'girish (Reverse in-place)
## Topshiriq sharti:
Massivga havola qabul qilib, uning elementlarini teskari o'giruvchi funksiya yozing.

## Yechim (Rust kodi):
```rust
fn massivni_agdar(arr: &mut [i32]) {
    let len = arr.len();
    for i in 0..len / 2 {
        arr.swap(i, len - 1 - i);
    }
}

fn main() {
    let mut sonlar = [1, 2, 3, 4, 5];
    massivni_agdar(&mut sonlar);
    println!("Aylanma massiv: {:?}", sonlar);
}
```

## Tushuntirish va Mantiq:
`&mut [i32]` massiv bo'lagi (slice) qabul qilinib, `arr.swap()` orqali O(1) qo'shimcha xotira bilan massiv teskari qilinadi.

## Ishlash natijasi:
```text
Aylanma massiv: [5, 4, 3, 2, 1]
```

---

# 143-Topshiriq: Massiv medianasini hisoblash funksiyasi
## Topshiriq sharti:
Massiv nusxasini olib, saralab, medianasini topuvchi funksiya tuzing.

## Yechim (Rust kodi):
```rust
fn hisobla_mediana(mut arr: [i32; 5]) -> f64 {
    arr.sort();
    let mid = arr.len() / 2;
    if arr.len() % 2 == 1 {
        arr[mid] as f64
    } else {
        (arr[mid - 1] + arr[mid]) as f64 / 2.0
    }
}

fn main() {
    let sonlar = [7, 1, 9, 3, 5];
    println!("Mediana: {}", hisobla_mediana(sonlar));
}
```

## Tushuntirish va Mantiq:
Mediana to'plamning qoq o'rtasidagi qiymatdir. Funksiyaga massiv qiymat bo'yicha uzatilgani uchun asl massiv saralanmagan holatda qoladi.

## Ishlash natijasi:
```text
Mediana: 5
```

---

# 144-Topshiriq: Kompilyatsiya vaqtida Fibonachchi hisoblash (const fn)
## Topshiriq sharti:
`const fn` orqali Fibonachchining 10-hadini dastur kompilatsiya bo'layotgan paytdayoq hisoblang.

## Yechim (Rust kodi):
```rust
const fn const_fib(n: u32) -> u32 {
    let mut a = 0;
    let mut b = 1;
    let mut i = 0;
    while i < n {
        let temp = a + b;
        a = b;
        b = temp;
        i += 1;
    }
    a
}

const FIB_10: u32 = const_fib(10);

fn main() {
    println!("Kompilyatsiyada olingan Fib(10): {}", FIB_10);
}
```

## Tushuntirish va Mantiq:
Rust ning zamonaviy `const fn` dvigateli kompilatsiya vaqtida tsikllar (`while`, `for`) bilan ishlashga to'liq ruxsat beradi.

## Ishlash natijasi:
```text
Kompilyatsiyada olingan Fib(10): 55
```

---

# 145-Topshiriq: Modul ichida xotira o'lchamlarini tahlil qilish
## Topshiriq sharti:
Har xil turlarning bayt hajmini ko'rsatuvchi diagnostika moduli tuzing.

## Yechim (Rust kodi):
```rust
mod diagnostika {
    pub fn chop_et_hajm<T>(nom: &str) {
        println!("{:<10} xotirada: {} bayt", nom, std::mem::size_of::<T>());
    }
}

fn main() {
    diagnostika::chop_et_hajm::<u8>("u8");
    diagnostika::chop_et_hajm::<i32>("i32");
    diagnostika::chop_et_hajm::<f64>("f64");
    diagnostika::chop_et_hajm::<[i32; 10]>("[i32; 10]");
}
```

## Tushuntirish va Mantiq:
Generik funksiya va modullar kombinatsiyasi tizimli dasturlashda xotira sarfini nazorat qilishni qulaylashtiradi.

## Ishlash natijasi:
```text
u8         xotirada: 1 bayt
i32        xotirada: 4 bayt
f64        xotirada: 8 bayt
[i32; 10]  xotirada: 40 bayt
```

---

# 146-Topshiriq: Matritsani transpozitsiya qilish funksiyasi
## Topshiriq sharti:
3x3 matritsani satrlarini ustunlar bilan almashtiruvchi funksiya yozing.

## Yechim (Rust kodi):
```rust
fn transpozitsiya(m: [[i32; 3]; 3]) -> [[i32; 3]; 3] {
    let mut res = [[0; 3]; 3];
    for i in 0..3 {
        for j in 0..3 {
            res[j][i] = m[i][j];
        }
    }
    res
}

fn main() {
    let matritsa = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ];
    let t = transpozitsiya(matritsa);
    println!("Transpozitsiya natijasi: {:?}", t);
}
```

## Tushuntirish va Mantiq:
Chiziqli algebra va AI matritsa amallarida transpozitsiya eng ko'p qo'llaniladigan operatsiyalardan biridir.

## Ishlash natijasi:
```text
Transpozitsiya natijasi: [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
```

---

# 147-Topshiriq: Kompleks sonlar arifmetikasi (Kortejlar yordamida)
## Topshiriq sharti:
Kompleks sonlarni `(f64, f64)` korteji sifatida ifodalab, ko'paytirish funksiyasini yozing.

## Yechim (Rust kodi):
```rust
type Kompleks = (f64, f64); // (haqiqiy, mavhum)

fn kompleks_kopaytir(a: Kompleks, b: Kompleks) -> Kompleks {
    let haqiqiy = a.0 * b.0 - a.1 * b.1;
    let mavhum = a.0 * b.1 + a.1 * b.0;
    (haqiqiy, mavhum)
}

fn main() {
    let z1 = (2.0, 3.0); // 2 + 3i
    let z2 = (1.0, 4.0); // 1 + 4i
    let z3 = kompleks_kopaytir(z1, z2);

    println!("Ko'paytma: {} + {}i", z3.0, z3.1);
}
```

## Tushuntirish va Mantiq:
(a + bi)(c + di) = (ac - bd) + (ad + bc)i formulasi bo'yicha hisoblanadi. Type alias va funksiya kortejlar bilan ishlashni soddalashtiradi.

## Ishlash natijasi:
```text
Ko'paytma: -10 + 11i
```

---

# 148-Topshiriq: Satr ichidagi unli harflarni sanash funksiyasi
## Topshiriq sharti:
Berilgan matn ichidagi barcha o'zbek unli harflari miqdorini aniqlovchi funksiya tuzing.

## Yechim (Rust kodi):
```rust
fn unlilarni_sana(matn: &str) -> usize {
    let unlilar = ['a', 'e', 'i', 'o', 'u', 'o', 'A', 'E', 'I', 'O', 'U'];
    let mut sanagich = 0;
    for c in matn.chars() {
        if unlilar.contains(&c) {
            sanagich += 1;
        }
    }
    sanagich
}

fn main() {
    let jumlalar = "Rust tili xavfsiz va juda tez";
    println!("Unlilar soni: {}", unlilarni_sana(jumlalar));
}
```

## Tushuntirish va Mantiq:
`matn.chars()` iteratori har bir UTF-8 belgisini `char` sifatida oladi, `unlilar.contains(&c)` esa to'plamdan qidiradi.

## Ishlash natijasi:
```text
Unlilar soni: 9
```

---

# 149-Topshiriq: Matematik polindromik so'zlarni tekshirish
## Topshiriq sharti:
Matn to'g'ri va teskarisidan bir xil o'qilishini tekshiruvchi funksiya yozing.

## Yechim (Rust kodi):
```rust
fn palindrommi(soz: &str) -> bool {
    let tozalangan: Vec<char> = soz.chars().filter(|c| !c.is_whitespace()).collect();
    let len = tozalangan.len();
    for i in 0..len / 2 {
        if tozalangan[i] != tozalangan[len - 1 - i] {
            return false;
        }
    }
    true
}

fn main() {
    println!("'kiyik' palindrommi: {}", palindrommi("kiyik"));
    println!("'rust' palindrommi: {}", palindrommi("rust"));
}
```

## Tushuntirish va Mantiq:
So'zni harflarga ajratib, ikki chetidan markaz tomon solishtirib borish O(N) vaqt va xatosiz natijani ta'minlaydi.

## Ishlash natijasi:
```text
'kiyik' palindrommi: true
'rust' palindrommi: false
```

---

# 150-Topshiriq: To'liq modulli loyiha: Bank hisob operatsiyalari simulyatsiyasi
## Topshiriq sharti:
Kompakt va toza modul tizimi bilan bank balansi, to'lov va to'ldirish funksiyalarini loyihalashtiring.

## Yechim (Rust kodi):
```rust
mod bank {
    pub struct Hisob {
        balans: f64,
    }

    impl Hisob {
        pub fn yangi(boshlangich: f64) -> Self {
            Self { balans: boshlangich }
        }

        pub fn depozit(&mut self, summa: f64) {
            self.balans += summa;
            println!("+ ${} qo'shildi. Joriy balans: ${}", summa, self.balans);
        }

        pub fn yechish(&mut self, summa: f64) -> bool {
            if self.balans >= summa {
                self.balans -= summa;
                println!("- ${} yechildi. Qoldiq: ${}", summa, self.balans);
                true
            } else {
                println!("Xatolik: Mablag' yetarli emas! Balans: ${}", self.balans);
                false
            }
        }
    }
}

fn main() {
    let mut mijoz = bank::Hisob::yangi(500.0);
    mijoz.depozit(200.0);
    mijoz.yechish(150.0);
    mijoz.yechish(600.0);
}
```

## Tushuntirish va Mantiq:
Struktura maydonlari private saqlanib, faqat `pub` metodlar orqali o'zgartirilishi xavfsiz moliya arxitekturasining poydevori hisoblanadi.

## Ishlash natijasi:
```text
+ $200 qo'shildi. Joriy balans: $700
- $150 yechildi. Qoldiq: $550
Xatolik: Mablag' yetarli emas! Balans: $550
```

---
