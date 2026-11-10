# 4-Qism: Ownership (Egalik) va Move Semantikasi (151-200)

Ushbu qismda Rust dasturlash tilining yuragi va eng asosiy inqilobiy xususiyati bo'lgan **Ownership (Egalik) tizimi**, Stack va Heap xotiralarining ishlash mexanizmi, Move semantikasi, `Copy` vs `Clone`, `drop` destruktorlari, RAII (Resource Acquisition Is Initialization), Typestate andozasi va xotira sizib ketishining (Memory Leaks) axlat yig'uvchisiz (GC siz) 100% oldini olish sirlari o'rganiladi.

---

# 151-Topshiriq: Ownership tizimining 3 ta oltin qoidasi
## Topshiriq sharti:
Rust da egalikning 3 ta asosiy tamoyilini kod va izohlar orqali namoyish eting.

## Yechim (Rust kodi):
```rust
fn main() {
    // 1-qoida: Rust da har bir qiymatning bitta egasi (owner) bo'ladi.
    // 2-qoida: Bir vaqtning o'zida faqat bitta egasi mavjud bo'lishi mumkin.
    // 3-qoida: Qachonki egasi o'z doirasidan (scope) chiqib ketsa, qiymat xotiradan o'chiriladi.

    {
        let salom = String::from("Salom Rust!");
        println!("Blok ichida: {}", salom);
    } // Bu yerda 'salom' o'z doirasidan chiqdi, xotira avtomatik tozalandi!

    println!("Blokdan tashqarida xotira allaqachon bo'shatilgan.");
}
```

## Tushuntirish va Mantiq:
Ownership Rust ga xotirani hech qanday Garbage Collectorsiz boshqarish imkonini beradi. Har bir obyektning qachon tugashi kompilyatsiya vaqtida aniq hisoblanadi.

## Ishlash natijasi:
```text
Blok ichida: Salom Rust!
Blokdan tashqarida xotira allaqachon bo'shatilgan.
```

---

# 152-Topshiriq: Stack va Heap xotiralari taqqosi
## Topshiriq sharti:
Stack da saqlanuvchi qat'iy o'lchamli son bilan Heap da saqlanuvchi dinamik satrni ko'rsating.

## Yechim (Rust kodi):
```rust
fn main() {
    let stack_son: i32 = 42; // Stack da tezkor va ketma-ket saqlanadi
    let heap_satr: String = String::from("Rust Xotirasi"); // Ko'rsatkich Stack da, haqiqiy baytlar Heap da

    println!("Stack qiymat: {}", stack_son);
    println!("Heap matn: {}", heap_satr);
}
```

## Tushuntirish va Mantiq:
Stack o'lchami oldindan ma'lum bo'lgan qat'iy ma'lumotlar uchun LIFO tarzida ishlaydi. Heap esa dastur ishlashi davomida o'lchami o'zgarishi mumkin bo'lgan dinamik resurslar uchun joy ajratadi.

## Ishlash natijasi:
```text
Stack qiymat: 42
Heap matn: Rust Xotirasi
```

---

# 153-Topshiriq: Copy semantikasi: Primitiv turlarning avtomatik nusxalanishi
## Topshiriq sharti:
Butun son boshqa o'zgaruvchiga berilganda asl qiymat ham yaroqli qolishini ko'rsating.

## Yechim (Rust kodi):
```rust
fn main() {
    let x = 100;
    let y = x; // x nusxalandi (Copy)

    println!("x = {}", x);
    println!("y = {}", y);
}
```

## Tushuntirish va Mantiq:
Stack da to'liq saqlanuvchi oddiy turlar (`i32`, `f64`, `bool`, `char`, qat'iy massivlar) `Copy` traitiga ega. Ular tayinlanganda xotiradagi baytlari avtomatik nusxalanadi.

## Ishlash natijasi:
```text
x = 100
y = 100
```

---

# 154-Topshiriq: Move semantikasi: Egalikning boshqa o'zgaruvchiga ko'chishi
## Topshiriq sharti:
String obyekti yangi o'zgaruvchiga o'zlashtirilganda dastlabki o'zgaruvchining yaroqsiz bo'lib qolishini ko'rsating.

## Yechim (Rust kodi):
```rust
fn main() {
    let s1 = String::from("Toshkent");
    let s2 = s1; // Egalik s1 dan s2 ga ko'chdi (MOVE)

    // println!("{}", s1); // Agar bu qatordagi izoh olib tashlansa, kompilyator xatolik beradi!
    println!("s2 = {}", s2);
}
```

## Tushuntirish va Mantiq:
Rust da Heap ma'lumotlari nusxalanmaydi, balki ko'rsatkich yangi egaga beriladi. Eski o'zgaruvchi `s1` darhol yaroqsiz (invalid) deb topiladi. Bu 'Move' deb ataladi.

## Ishlash natijasi:
```text
s2 = Toshkent
```

---

# 155-Topshiriq: Nega Shallow Copy o'rniga Move ishlatiladi? (Double Free xavfi)
## Topshiriq sharti:
Ikkita ko'rsatkich bitta Heap xotirasini bir vaqtda tozalashga urinishining oldi qanday olinishini tushuntiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let a = String::from("Xavfsiz Xotira");
    let b = a; // Agar bu shallow copy bo'lganda, scope oxirida ikkalasi bitta manzilni free qilardi!

    println!("Faqat 'b' egasi bo'lib qoldi: {}", b);
}
```

## Tushuntirish va Mantiq:
C++ da 'shallow copy' qilinganda ikkala o'zgaruvchi bir xil xotirani o'chirishga urinib 'Double Free' kiberxavfsizlik xatosini keltirib chiqaradi. Rust Move orqali bu muammoni tubdan yo'q qilgan.

## Ishlash natijasi:
```text
Faqat 'b' egasi bo'lib qoldi: Xavfsiz Xotira
```

---

# 156-Topshiriq: Qiymatni funksiyaga uzatishda Move bo'lishi
## Topshiriq sharti:
String ni funksiyaga qiymat sifatida uzatganda uning egasligi funksiyaga o'tishini namoyish eting.

## Yechim (Rust kodi):
```rust
fn egaslikni_ol(matn: String) {
    println!("Funksiya matnni qabul qildi: {}", matn);
} // Bu yerda 'matn' o'chiriladi!

fn main() {
    let kitob = String::from("Rust Dasturlash Asoslari");
    egaslikni_ol(kitob);

    // println!("{}", kitob); // Xatolik: 'kitob' egasligi allaqachon funksiyaga o'tib ketgan!
}
```

## Tushuntirish va Mantiq:
Funksiyaga parametr qiymat bo'yicha uzatilganda, xuddi tayinlashdagi kabi Move yuz beradi. Funksiya tugashi bilan resurs xotiradan butunlay o'chiriladi.

## Ishlash natijasi:
```text
Funksiya matnni qabul qildi: Rust Dasturlash Asoslari
```

---

# 157-Topshiriq: Funksiyadan qiymat qaytarish orqali egalikni qaytarib olish
## Topshiriq sharti:
Funksiya yaratgan yoki o'zgartirgan resursning egasligini chaqiruvchiga qaytarish.

## Yechim (Rust kodi):
```rust
fn matn_yarat() -> String {
    let yangi_satr = String::from("Yangi Obyekt");
    yangi_satr // Egalik chaqiruvchiga o'tadi
}

fn main() {
    let s = matn_yarat();
    println!("Olingan satr: {}", s);
}
```

## Tushuntirish va Mantiq:
Funksiya ichida yaratilgan Heap resursi `return` qilinganda o'chirilmaydi, balki uning egasligi tashqi o'zgaruvchiga topshiriladi.

## Ishlash natijasi:
```text
Olingan satr: Yangi Obyekt
```

---

# 158-Topshiriq: Egalikni uzatish va kortej orqali qaytarib olish
## Topshiriq sharti:
Funksiyaga resursni berib, uning natijasi bilan birga asl resursni ham qaytarib oling.

## Yechim (Rust kodi):
```rust
fn uzunlikni_hisobla(s: String) -> (String, usize) {
    let len = s.len();
    (s, len) // Ham asl String, ham uning uzunligi qaytariladi
}

fn main() {
    let s1 = String::from("Samarqand");
    let (s2, len) = uzunlikni_hisobla(s1);

    println!("'{}' so'zi uzunligi: {}", s2, len);
}
```

## Tushuntirish va Mantiq:
Borrowing bo'lmagan taqdirda ham kortejlar orqali egalikni qaytarib olish mumkin, ammo Rust buning uchun Borrowing (havolalar) tizimini tavsiya qiladi.

## Ishlash natijasi:
```text
'Samarqand' so'zi uzunligi: 9
```

---

# 159-Topshiriq: clone() metodi orqali Heap xotiradan chuqur nusxa olish
## Topshiriq sharti:
Move o'rniga Heap ma'lumotlarining haqiqiy mustaqil nusxasini yaratish.

## Yechim (Rust kodi):
```rust
fn main() {
    let s1 = String::from("Original Matn");
    let s2 = s1.clone(); // Heap da alohida yangi xotira ajratiladi

    println!("s1 = {}", s1);
    println!("s2 = {}", s2);
}
```

## Tushuntirish va Mantiq:
`.clone()` metodi Heap xotiradagi ma'lumotlarni to'liq takroran ajratadi. Ikkala o'zgaruvchi ham o'z mustaqil manziliga ega bo'ladi.

## Ishlash natijasi:
```text
s1 = Original Matn
s2 = Original Matn
```

---

# 160-Topshiriq: clone() ning unumdorlikka ta'siri tahlili
## Topshiriq sharti:
Katta satrlarni klonlash xotira va vaqt talab qilishini tushuntiruvchi misol.

## Yechim (Rust kodi):
```rust
fn main() {
    let katta_matn = "A".repeat(1_000_000); // 1 MB satr Heap da
    let nusxa = katta_matn.clone(); // Yana 1 MB yangi Heap xotira

    println!("Asl hajm: {} bayt", katta_matn.len());
    println!("Nusxa hajm: {} bayt", nusxa.len());
}
```

## Tushuntirish va Mantiq:
Rust da `clone()` ko'zga ko'rinadigan qilib qo'yilgan. Bu dasturchiga Heap nusxalash bepul emasligini va kerak bo'lmaganda havolalardan (`&`) foydalanish kerakligini eslatadi.

## Ishlash natijasi:
```text
Asl hajm: 1000000 bayt
Nusxa hajm: 1000000 bayt
```

---

# 161-Topshiriq: std::mem::drop orqali resursni muddatidan oldin bo'shatish
## Topshiriq sharti:
Obyekt o'z blokidan chiqishini kutmasdan, uni darhol xotiradan tozalang.

## Yechim (Rust kodi):
```rust
fn main() {
    let malumot = String::from("Katta hajmdagi vaqtinchalik fayl");
    println!("Ma'lumot yaratildi: {}", malumot);

    drop(malumot); // Xotira shu nuqtadayoq bo'shatiladi

    // println!("{}", malumot); // Xatolik: 'malumot' allaqachon drop qilingan!
    println!("Xotira muddatidan oldin muvaffaqiyatli tozalandi.");
}
```

## Tushuntirish va Mantiq:
`drop(x)` funksiyasi Rust standart kutubxonasida bo'lib, resursni darhol xotiradan o'chiradi. Bu og'ir resurslarni (fayl qulflari, xotira buferlari) tezda bo'shatishda juda muhim.

## Ishlash natijasi:
```text
Ma'lumot yaratildi: Katta hajmdagi vaqtinchalik fayl
Xotira muddatidan oldin muvaffaqiyatli tozalandi.
```

---

# 162-Topshiriq: RAII (Resource Acquisition Is Initialization) amaliyoti
## Topshiriq sharti:
Resurs yaratilganda initsializatsiya bo'lishi va blok tugaganda avtomatik tozalanishini kuzating.

## Yechim (Rust kodi):
```rust
struct XotiraBloki {
    nom: String,
}

impl Drop for XotiraBloki {
    fn drop(&mut self) {
        println!(">>> RAII: '{}' bloki xotiradan o'chirildi!", self.nom);
    }
}

fn main() {
    println!("Dastur boshlandi");
    {
        let _blok = XotiraBloki { nom: String::from("Bufer A") };
        println!("Blok ichida ish bajarilmoqda...");
    } // Bu yerda avtomatik drop ishga tushadi
    println!("Dastur tugadi");
}
```

## Tushuntirish va Mantiq:
RAII tamoyili bo'yicha har qanday resurs (xotira, fayl, tarmoq ulanishi) o'zgaruvchi bilan bog'lanadi va o'zgaruvchi o'lganda resurs 100% kafolat bilan tozalanadi.

## Ishlash natijasi:
```text
Dastur boshlandi
Blok ichida ish bajarilmoqda...
>>> RAII: 'Bufer A' bloki xotiradan o'chirildi!
Dastur tugadi
```

---

# 163-Topshiriq: Strukturalarda Move semantikasi
## Topshiriq sharti:
Struktura boshqa o'zgaruvchiga berilganda uning to'liq ko'chib o'tishini ko'rsating.

## Yechim (Rust kodi):
```rust
struct Foydalanuvchi {
    ism: String,
    yosh: u32,
}

fn main() {
    let f1 = Foydalanuvchi {
        ism: String::from("Anvar"),
        yosh: 28,
    };
    let f2 = f1; // Butun struktura f2 ga ko'chdi

    println!("Yangi egasi: {}, Yoshi: {}", f2.ism, f2.yosh);
    // println!("{}", f1.ism); // Xatolik!
}
```

## Tushuntirish va Mantiq:
Struktura tarkibida `Copy` bo'lmagan birorta maydon (masalan `String`) bo'lsa, butun struktura Move xususiyatiga ega bo'ladi.

## Ishlash natijasi:
```text
Yangi egasi: Anvar, Yoshi: 28
```

---

# 164-Topshiriq: Qisman ko'chish (Partial Move): Bitta maydon ko'chirilishi
## Topshiriq sharti:
Strukturaning faqat bitta maydonini yangi o'zgaruvchiga oling.

## Yechim (Rust kodi):
```rust
struct Kitob {
    nomi: String,
    betlar_soni: u32,
}

fn main() {
    let k = Kitob {
        nomi: String::from("O'tkan kunlar"),
        betlar_soni: 350,
    };

    let kitob_nomi = k.nomi; // Faqat 'nomi' ko'chdi!
    println!("Olingan nom: {}", kitob_nomi);
    println!("Qolgan betlar soni (Copy maydon): {}", k.betlar_soni);
    // println!("{}", k.nomi); // Xatolik: faqat bu maydon ko'chib ketgan!
}
```

## Tushuntirish va Mantiq:
Rust maydonma-maydon egalikni kuzatadi. Bitta maydon ko'chib ketsa, qolgan maydonlar yaroqli bo'lib qoladi, lekin butun strukturaning o'zini butunligicha ishlatib bo'lmaydi.

## Ishlash natijasi:
```text
Olingan nom: O'tkan kunlar
Qolgan betlar soni (Copy maydon): 350
```

---

# 165-Topshiriq: Kortejlarda qisman ko'chish
## Topshiriq sharti:
Kortej ichidagi Heap elementini ko'chirib, boshqa primitiv elementini o'qish.

## Yechim (Rust kodi):
```rust
fn main() {
    let juftlik = (String::from("Rust"), 2024);

    let til = juftlik.0; // String ko'chib ketdi
    println!("Til nomi: {}", til);
    println!("Yil: {}", juftlik.1); // i32 qoldi va o'qilishi mumkin
}
```

## Tushuntirish va Mantiq:
Xuddi strukturalar kabi kortejlarda ham har bir katak alohida egalik huquqiga ega bo'lib, qisman ko'chishni qo'llab-quvvatlaydi.

## Ishlash natijasi:
```text
Til nomi: Rust
Yil: 2024
```

---

# 166-Topshiriq: Vektorlarda Move semantikasi va push qilish
## Topshiriq sharti:
Obyektni vektorga qo'shganda egalikning vektor ichiga ko'chishi.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut royxat = Vec::new();
    let matn = String::from("Birinchi element");

    royxat.push(matn); // 'matn' egaligi vektorga o'tdi

    // println!("{}", matn); // Xatolik: matn endi vektorga tegishli!
    println!("Vektordagi element: {}", royxat[0]);
}
```

## Tushuntirish va Mantiq:
Kolleksiyalar (`Vec`, `HashMap`) o'zlariga qo'shilgan elementlarning to'liq egasiga aylanadi. Vektor o'chirilganda uning barcha elementlari ham tozalanadi.

## Ishlash natijasi:
```text
Vektordagi element: Birinchi element
```

---

# 167-Topshiriq: Tsikl ichida Move qilish xatosi va uni to'g'irlash
## Topshiriq sharti:
Tsikl ichida tashqi o'zgaruvchini move qilib bo'lmasligi va yechimini ko'rsating.

## Yechim (Rust kodi):
```rust
fn main() {
    let shior = String::from("Rust tez va xavfsiz");

    for _ in 0..3 {
        // Har safar nusxasini uzatamiz, aks holda 1-qadamda move bo'lib ketardi
        chop_et(shior.clone());
    }
}

fn chop_et(s: String) {
    println!("Shior: {}", s);
}
```

## Tushuntirish va Mantiq:
Tsikl bir necha marta aylangani uchun, ichkariga to'g'ridan-to'g'ri `shior` uzatilsa, 2-qadamda qiymat yo'q bo'lib qoladi. Yechim - havolalar (`&`) yoki zarurat bo'lsa `.clone()`.

## Ishlash natijasi:
```text
Shior: Rust tez va xavfsiz
Shior: Rust tez va xavfsiz
Shior: Rust tez va xavfsiz
```

---

# 168-Topshiriq: Closurelarda 'move' kalit so'zi
## Topshiriq sharti:
Closure o'z muhitidagi qiymatni to'liq o'zlashtirib olishini namoyish eting.

## Yechim (Rust kodi):
```rust
fn main() {
    let xabar = String::from("Salom, Closure!");

    let mening_closure = move || {
        println!("Closure ichida: {}", xabar);
    };

    mening_closure();
    // println!("{}", xabar); // Xatolik: 'xabar' closure ichiga MOVE bo'lgan!
}
```

## Tushuntirish va Mantiq:
`move ||` closure kompilyatorga tashqi o'zgaruvchilarni qarzga olish o'rniga ularning to'liq egasligini closure xotirasiga ko'chirishni buyuradi. Bu oqimlarda (threads) majburiydir.

## Ishlash natijasi:
```text
Closure ichida: Salom, Closure!
```

---

# 169-Topshiriq: Option::take() orqali egalikni xavfsiz sug'urib olish
## Topshiriq sharti:
`Option` ichidagi qiymatni `None` qoldirgan holda o'zlashtiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut maumot: Option<String> = Some(String::from("Muhim xabar"));

    let olingan = maumot.take(); // Ichidagi qiymat ko'chadi, o'rnida None qoladi

    println!("Olingan: {:?}", olingan);
    println!("Asl o'zgaruvchi holati: {:?}", maumot);
}
```

## Tushuntirish va Mantiq:
`take()` metodi o'zgaruvchan havola ichidan qiymatni xavfsiz sug'urib olib, uning o'rniga `None` qo'yadi. Bu Rust da strukturalar bilan ishlashda eng ko'p ishlatiladigan usuldir.

## Ishlash natijasi:
```text
Olingan: Some("Muhim xabar")
Asl o'zgaruvchi holati: None
```

---

# 170-Topshiriq: std::mem::replace orqali xotiradagi qiymatni almashtirish
## Topshiriq sharti:
Eski qiymatni olib, o'rniga darhol yangisini qo'yish.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut eslatma = String::from("Eski eslatma");
    let eski = std::mem::replace(&mut eslatma, String::from("Yangi eslatma"));

    println!("Eski qiymat: {}", eski);
    println!("Yangi qiymat: {}", eslatma);
}
```

## Tushuntirish va Mantiq:
`replace(&mut target, yangi)` funksiyasi xotiradagi qiymatni bir harakatda yangisiga almashtirib, eskisining egasligini chaqiruvchiga beradi.

## Ishlash natijasi:
```text
Eski qiymat: Eski eslatma
Yangi qiymat: Yangi eslatma
```

---

# 171-Topshiriq: std::mem::take va Default traiti
## Topshiriq sharti:
Standart bo'sh qiymat qoldirib, mavjud qiymatni sug'urib olish.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut matn: String = String::from("Rust dasturchilari");
    let olingan = std::mem::take(&mut matn); // Bo'sh String "" qoladi

    println!("Olingan satr: '{}'", olingan);
    println!("Qolgan satr:  '{}'", matn);
}
```

## Tushuntirish va Mantiq:
`std::mem::take` turi `Default` implement qilgan o'zgaruvchilar uchun ishlab, ularning o'rniga `Default::default()` qoldiradi.

## Ishlash natijasi:
```text
Olingan satr: 'Rust dasturchilari'
Qolgan satr:  ''
```

---

# 172-Topshiriq: O'zgaruvchanlikning (Mutability) Move paytida yangilanishi
## Topshiriq sharti:
O'zgarmas o'zgaruvchini move qilib, uni yangi o'zgaruvchan o'zgaruvchiga aylantiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let o'zgarmas_satr = String::from("Salom");
    let mut o'zgaruvchan = o'zgarmas_satr; // Yangi egasi 'mut' bo'lishi mumkin!

    o'zgaruvchan.push_str(", Dunyo!");
    println!("{}", o'zgaruvchan);
}
```

## Tushuntirish va Mantiq:
O'zgaruvchanlik (mutability) qiymatning emas, balki aynan bog'langan nomning (binding) xususiyatidir. Move bo'lganda yangi egasi unga `mut` maqomini bera oladi.

## Ishlash natijasi:
```text
Salom, Dunyo!
```

---

# 173-Topshiriq: If-else tarmoqlarida Move qilish qoidalari
## Topshiriq sharti:
Agar bitta tarmoqda qiymat move bo'lsa, tarmoqdan keyin uni ishlatish taqiqlanishini tushuntiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let shart = true;
    let satr = String::from("Muhim fayl");

    if shart {
        let _yangi_ega = satr; // Bu tarmoqda move bo'ldi
        println!("Shart bajarildi, egalik o'tdi.");
    } else {
        println!("Boshqa harakat.");
    }

    // println!("{}", satr); // Kompilyator xatolik beradi: shart tufayli satr move bo'lgan bo'lishi mumkin!
}
```

## Tushuntirish va Mantiq:
Rust kompilyatori statik oqim tahlili (Control Flow Analysis) orqali qiymat biror tarmoqda move bo'lish ehtimoli bo'lsa ham, undan keyin foydalanishga yo'l qo'ymaydi.

## Ishlash natijasi:
```text
Shart bajarildi, egalik o'tdi.
```

---

# 174-Topshiriq: Match ifodasida pattern destrukturizatsiyasi va Move
## Topshiriq sharti:
`match` orqali strukturani ochishda uning ichki maydonlarining ko'chishi.

## Yechim (Rust kodi):
```rust
struct Xodim {
    ism: String,
    maosh: u32,
}

fn main() {
    let x = Xodim {
        ism: String::from("Bobur"),
        maosh: 3000,
    };

    match x {
        Xodim { ism, maosh } => {
            println!("Xodim {} maoshi: ${}", ism, maosh);
        }
    }
    // println!("{}", x.ism); // Xatolik: match ichida 'ism' move bo'ldi!
}
```

## Tushuntirish va Mantiq:
`match` patternlarida maydonlar o'zgaruvchilarga bog'langanda, agar maxsus `ref` ko'rsatilmasa, sukut bo'yicha Move amalga oshadi.

## Ishlash natijasi:
```text
Xodim Bobur maoshi: $3000
```

---

# 175-Topshiriq: Match ichida 'ref' kalit so'zi (Move ning oldini olish)
## Topshiriq sharti:
Obyektni move qilmasdan, faqat havola orqali match qiling.

## Yechim (Rust kodi):
```rust
struct Kitob {
    nom: String,
}

fn main() {
    let k = Kitob { nom: String::from("Alkimyogar") };

    match k {
        Kitob { ref nom } => {
            println!("Kitob nomi o'qildi: {}", nom);
        }
    }

    // 'k' hali ham to'liq yaroqli!
    println!("Asl kitob saqlanib qoldi: {}", k.nom);
}
```

## Tushuntirish va Mantiq:
`ref nom` kalit so'zi maydondan havola (`&`) oladi va uning ko'chib ketishiga (move) yo'l qo'ymaydi. Natijada asl struktura yaroqli bo'lib qoladi.

## Ishlash natijasi:
```text
Kitob nomi o'qildi: Alkimyogar
Asl kitob saqlanib qoldi: Alkimyogar
```

---

# 176-Topshiriq: Foydalanuvchi ma'lumotlar bazasi ulanishi (RAII Connection)
## Topshiriq sharti:
Ulanish yaratilganda ochilishi va o'lganda avtomatik uzilishi simulyatsiyasi.

## Yechim (Rust kodi):
```rust
struct DbConnection {
    url: String,
}

impl DbConnection {
    fn ulanish(url: &str) -> Self {
        println!("[DB] {} manziliga ulanildi.", url);
        Self { url: url.to_string() }
    }
}

impl Drop for DbConnection {
    fn drop(&mut self) {
        println!("[DB] {} ulanishi xavfsiz yopildi.", self.url);
    }
}

fn main() {
    {
        let _conn = DbConnection::ulanish("postgres://localhost:5432/asosiy");
        println!("[DB] So'rovlar bajarilmoqda...");
    }
    println!("Asosiy sikl davom etmoqda.");
}
```

## Tushuntirish va Mantiq:
Rust da tarmoq va DB ulanishlarini qo'lda yopish (`conn.close()`) shart emas. RAII orqali xato yuz bergan taqdirda ham ulanish hech qachon ochiq qolib ketmaydi.

## Ishlash natijasi:
```text
[DB] postgres://localhost:5432/asosiy manziliga ulanildi.
[DB] So'rovlar bajarilmoqda...
[DB] postgres://localhost:5432/asosiy ulanishi xavfsiz yopildi.
Asosiy sikl davom etmoqda.
```

---

# 177-Topshiriq: Dinamik bufer ajratish va xotira tozalanish monitoringi
## Topshiriq sharti:
Katta bufer ajratib, uning hayot davrini tekshiring.

## Yechim (Rust kodi):
```rust
struct KattaBufer {
    hajm: usize,
}

impl KattaBufer {
    fn yangi(hajm: usize) -> Self {
        println!(">>> Xotiradan {} bayt bufer ajratildi.", hajm);
        Self { hajm }
    }
}

impl Drop for KattaBufer {
    fn drop(&mut self) {
        println!("<<< Xotiradan {} bayt bufer tozalandi.", self.hajm);
    }
}

fn main() {
    let _b1 = KattaBufer::yangi(1024 * 1024);
    println!("Bufer bilan ish yakunlandi.");
}
```

## Tushuntirish va Mantiq:
Har bir obyekt o'zining butun resursini o'zi bilan olib ketadi. Bu xotira tozalanishini bashorat qilinadigan (deterministic) qiladi.

## Ishlash natijasi:
```text
>>> Xotiradan 1048576 bayt bufer ajratildi.
Bufer bilan ish yakunlandi.
<<< Xotiradan 1048576 bayt bufer tozalandi.
```

---

# 178-Topshiriq: Custom struct uchun #[derive(Clone, Copy)] qo'llash
## Topshiriq sharti:
O'z strukturangizga `Copy` xususiyatini berib, avtomatik nusxalanishini ta'minlang.

## Yechim (Rust kodi):
```rust
#[derive(Debug, Clone, Copy)]
struct Nuqta {
    x: i32,
    y: i32,
}

fn main() {
    let p1 = Nuqta { x: 10, y: 20 };
    let p2 = p1; // Copy bo'ldi, Move emas!

    println!("p1 = {:?}", p1);
    println!("p2 = {:?}", p2);
}
```

## Tushuntirish va Mantiq:
Agar strukturaning barcha maydonlari `Copy` bo'lsa, unga `#[derive(Clone, Copy)]` atributini berish mumkin. Shunda u primitiv son kabi erkin nusxalanadi.

## Ishlash natijasi:
```text
p1 = Nuqta { x: 10, y: 20 }
p2 = Nuqta { x: 10, y: 20 }
```

---

# 179-Topshiriq: Qachon Copy traitini qo'shib bo'lmaydi?
## Topshiriq sharti:
Heap ga ega strukturalarda nima uchun `Copy` taqiqlanishini tushuntiring.

## Yechim (Rust kodi):
```rust
#[derive(Debug, Clone)]
struct Shaxs {
    ism: String, // String Heap da, u Copy bo'la olmaydi!
    yosh: u8,
}

fn main() {
    let sh1 = Shaxs { ism: String::from("Dilshod"), yosh: 22 };
    let sh2 = sh1.clone(); // Majburiy ravishda clone() chaqiriladi

    println!("sh1: {:?}, sh2: {:?}", sh1, sh2);
}
```

## Tushuntirish va Mantiq:
Rust da Heap resursini boshqaruvchi turlarga `Copy` qo'shish qat'iyan taqiqlangan. Chunki bu yashirin va og'ir xotira ajratishlariga olib kelishi mumkin edi.

## Ishlash natijasi:
```text
sh1: Shaxs { ism: "Dilshod", yosh: 22 }, sh2: Shaxs { ism: "Dilshod", yosh: 22 }
```

---

# 180-Topshiriq: Heap satrlarini qo'shishda Move semantikasi (s1 + &s2)
## Topshiriq sharti:
`+` operatori birinchi satrning xotirasini qayta ishlatishini (reusing) ko'rsating.

## Yechim (Rust kodi):
```rust
fn main() {
    let s1 = String::from("Assalomu ");
    let s2 = String::from("alaykum!");

    let s3 = s1 + &s2; // s1 MOVE bo'ldi va kengaytirildi, s2 esa qarzga olindi

    // println!("{}", s1); // Xatolik: s1 ning xotirasi s3 ga aylandi!
    println!("Natija: {}", s3);
    println!("s2 hali ham saqlanib turibdi: {}", s2);
}
```

## Tushuntirish va Mantiq:
Rust da `String + &str` amali `s1` ning mavjud buferiga yangi baytlarni ulaydi. Bu yangi xotira ajratmasdan, mavjud xotiradan unumli foydalanish imkonini beradi.

## Ishlash natijasi:
```text
Natija: Assalomu alaykum!
s2 hali ham saqlanib turibdi: alaykum!
```

---

# 181-Topshiriq: Konsuming Builder (Fluent Builder) andozasi
## Topshiriq sharti:
`self` ni qabul qilib, o'zgartirib qaytaruvchi metodlar zanjirini tuzing.

## Yechim (Rust kodi):
```rust
struct ServerSozlama {
    host: String,
    port: u16,
}

impl ServerSozlama {
    fn yangi() -> Self {
        Self { host: String::from("127.0.0.1"), port: 80 }
    }

    fn host(mut self, h: &str) -> Self {
        self.host = h.to_string();
        self
    }

    fn port(mut self, p: u16) -> Self {
        self.port = p;
        self
    }
}

fn main() {
    let server = ServerSozlama::yangi()
        .host("0.0.0.0")
        .port(8080);

    println!("Server manzili: {}:{}", server.host, server.port);
}
```

## Tushuntirish va Mantiq:
Metod `self` ni (havola emas) qabul qilishi har bir chaqiruvda struktura egasligini yangi qadamga o'tkazadi va o'ta qulay zanjirli konfiguratsiya yaratadi.

## Ishlash natijasi:
```text
Server manzili: 0.0.0.0:8080
```

---

# 182-Topshiriq: Konsuming metodlar: Obyektni yo'q qilib, yangi formatga aylantirish
## Topshiriq sharti:
Xom ma'lumotni qayta ishlab, xom obyektni yaroqsiz qiluvchi metod yozing.

## Yechim (Rust kodi):
```rust
struct XomFayl {
    tarkib: Vec<u8>,
}

struct ParsedFayl {
    matn: String,
}

impl XomFayl {
    fn parse(self) -> ParsedFayl {
        // Asl XomFayl iste'mol qilinadi va endi mavjud bo'lmaydi
        let s = String::from_utf8(self.tarkib).unwrap_or_default();
        ParsedFayl { matn: s }
    }
}

fn main() {
    let f = XomFayl { tarkib: vec![65, 66, 67] };
    let parsed = f.parse();

    println!("Pars qilingan matn: {}", parsed.matn);
    // println!("{:?}", f.tarkib); // Xatolik: 'f' iste'mol qilingan!
}
```

## Tushuntirish va Mantiq:
Konsuming metodlar obyektning hayot siklini nazorat qilishda beqiyosdir. Masalan, xom fayl parse qilingach, xom nusxaga qayta kirishning oldini oladi.

## Ishlash natijasi:
```text
Pars qilingan matn: ABC
```

---

# 183-Topshiriq: Typestate andozasi: Holat mashinasini (State Machine) Move orqali himoyalash
## Topshiriq sharti:
Eshik holatlarini (Yopiq, Ochiq) kompilyatsiya vaqtida xavfsiz boshqaring.

## Yechim (Rust kodi):
```rust
struct YopiqEshik;
struct OchiqEshik;

struct Eshik<Holat> {
    holat: std::marker::PhantomData<Holat>,
}

impl Eshik<YopiqEshik> {
    fn yangi() -> Self { Self { holat: std::marker::PhantomData } }
    fn och(self) -> Eshik<OchiqEshik> {
        println!("Eshik ochildi.");
        Eshik { holat: std::marker::PhantomData }
    }
}

impl Eshik<OchiqEshik> {
    fn yop(self) -> Eshik<YopiqEshik> {
        println!("Eshik yopildi.");
        Eshik { holat: std::marker::PhantomData }
    }
}

fn main() {
    let e1 = Eshik::yangi();
    let e2 = e1.och();
    let _e3 = e2.yop();
    // e2.och(); // Xatolik: ochiq eshikni qayta ochib bo'lmaydi, chunki e2 allaqachon yop() ga Move bo'lgan!
}
```

## Tushuntirish va Mantiq:
Typestate andozasi Move semantikasidan foydalanib, eski holatni yo'q qiladi va xato holatlarni kompilyatsiya paytidayoq ushlaydi.

## Ishlash natijasi:
```text
Eshik ochildi.
Eshik yopildi.
```

---

# 184-Topshiriq: Custom Drop destruktori va self maydonlari
## Topshiriq sharti:
`Drop` traiti orqali obyektdan qolgan hisobotni konsolga chiqaring.

## Yechim (Rust kodi):
```rust
struct AuditLog {
    amallar_soni: usize,
}

impl Drop for AuditLog {
    fn drop(&mut self) {
        println!("[AUDIT] Seans yakunlandi. Jami amallar: {}", self.amallar_soni);
    }
}

fn main() {
    let mut log = AuditLog { amallar_soni: 0 };
    log.amallar_soni += 5;
    println!("Dastur amallarni bajardi.");
}
```

## Tushuntirish va Mantiq:
`Drop` funksiyasida `&mut self` olinadi va obyekt xotiradan tozalanishidan bir soniya oldin oxirgi amallarni bajarishga imkon beradi.

## Ishlash natijasi:
```text
Dastur amallarni bajardi.
[AUDIT] Seans yakunlandi. Jami amallar: 5
```

---

# 185-Topshiriq: Nega Copy va Drop bir vaqtda mavjud bo'la olmaydi?
## Topshiriq sharti:
Kompilyatorning bu ikki qarama-qarshi tushunchaga bo'lgan munosabatini ko'rsating.

## Yechim (Rust kodi):
```rust
// Quyidagi kod kompilyatsiyadan o'tmaydi:
// #[derive(Copy, Clone)]
// struct Sinov;
// impl Drop for Sinov { fn drop(&mut self) {} }

fn main() {
    println!("Copy va Drop bir vaqtda bo'la olmaydi!");
    println!("Chunki Copy oddiy bayt nusxalashni anglatadi, Drop esa yagona resurs tozalanishini talab qiladi.");
}
```

## Tushuntirish va Mantiq:
Agar tip `Copy` bo'lsa, uning xotirada nechta nusxasi borligi noma'lum bo'ladi. Bu esa `Drop` qachon chaqirilishi kerakligi qoidasiga zid keladi.

## Ishlash natijasi:
```text
Copy va Drop bir vaqtda bo'la olmaydi!
Chunki Copy oddiy bayt nusxalashni anglatadi, Drop esa yagona resurs tozalanishini talab qiladi.
```

---

# 186-Topshiriq: std::mem::forget orqali destruktorni to'xtatish
## Topshiriq sharti:
Resursning `drop` chaqirilishini ataylab chetlab o'tish.

## Yechim (Rust kodi):
```rust
struct XavfliResurs;

impl Drop for XavfliResurs {
    fn drop(&mut self) {
        println!("Destruktor ishladi!");
    }
}

fn main() {
    let r = XavfliResurs;
    std::mem::forget(r); // Destruktor chaqirilmaydi

    println!("Obyekt xotirada 'unutilgan' bo'lib qoldi.");
}
```

## Tushuntirish va Mantiq:
`std::mem::forget` destruktorni bekor qiladi. Bu past darajadagi FFI (C bilan muloqot) yoki maxsus xotira ajratuvchilarda xotirani C ga o'tkazishda kerak bo'ladi.

## Ishlash natijasi:
```text
Obyekt xotirada 'unutilgan' bo'lib qoldi.
```

---

# 187-Topshiriq: std::mem::ManuallyDrop orqali qo'lda destruktor chaqirish
## Topshiriq sharti:
Xotira tozalanish vaqtini o'z qo'lingizga oling.

## Yechim (Rust kodi):
```rust
use std::mem::ManuallyDrop;

struct Signal {
    matn: String,
}

impl Drop for Signal {
    fn drop(&mut self) {
        println!("Signal o'chirildi: {}", self.matn);
    }
}

fn main() {
    let mut s = ManuallyDrop::new(Signal { matn: String::from("Tizim signali") });

    println!("Signal faol holatda.");

    unsafe {
        ManuallyDrop::drop(&mut s); // Qo'lda tozalash
    }

    println!("Asosiy oqim yakunlandi.");
}
```

## Tushuntirish va Mantiq:
`ManuallyDrop` avtomatik tozalanishni to'xtatadi va uni aniq `unsafe` blok ichida kerakli vaqtda chaqirish imkonini beradi.

## Ishlash natijasi:
```text
Signal faol holatda.
Signal o'chirildi: Tizim signali
Asosiy oqim yakunlandi.
```

---

# 188-Topshiriq: Box<T> va Heap dagi qiymatning egasligi
## Topshiriq sharti:
Heap da son joylashtirib, uning egasligini ko'chiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let b1 = Box::new(500); // 500 Heap da saqlanadi
    let b2 = b1; // Heap ko'rsatkichi b2 ga ko'chdi

    println!("Heap dagi qiymat: {}", b2);
    // println!("{}", b1); // Xatolik: b1 move bo'lgan!
}
```

## Tushuntirish va Mantiq:
`Box<T>` eng sodda aqlli ko'rsatkich (Smart Pointer) bo'lib, Heap xotiradagi yagona egalikni ta'minlaydi.

## Ishlash natijasi:
```text
Heap dagi qiymat: 500
```

---

# 189-Topshiriq: Vektor sig'imi va xotira qayta ajratilishida Move
## Topshiriq sharti:
Vektor sig'imi oshganda ichidagi elementlarning yangi xotira manziliga ko'chishi.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut v = Vec::with_capacity(2);
    v.push(String::from("A"));
    v.push(String::from("B"));

    println!("Dastlabki sig'im: {}", v.capacity());
    v.push(String::from("C")); // Sig'im oshadi, yangi Heap xotiraga ko'chadi!
    println!("Yangi sig'im: {}", v.capacity());
}
```

## Tushuntirish va Mantiq:
Vektor sig'imi to'lganda, u avvalgi xotiradan ikki barobar katta yangi xotira so'raydi va barcha elementlarni yangi manzilga Move qiladi.

## Ishlash natijasi:
```text
Dastlabki sig'im: 2
Yangi sig'im: 4
```

---

# 190-Topshiriq: Zero-Sized Types (ZST) va ularning Move bo'lishi
## Topshiriq sharti:
0 baytli turlar xotirada joy olmasdan qanday move bo'lishini ko'rsating.

## Yechim (Rust kodi):
```rust
struct BoshMarker;

fn qabul_qil(m: BoshMarker) {
    let _yangi = m;
    println!("ZST muvaffaqiyatli Move bo'ldi!");
}

fn main() {
    let marker = BoshMarker;
    println!("ZST hajmi: {} bayt", std::mem::size_of::<BoshMarker>());
    qabul_qil(marker);
}
```

## Tushuntirish va Mantiq:
ZST turlari kompilyatsiyada xotiradan butunlay olib tashlanadi (0 bayt), lekin Rust ning tip xavfsizligi va egalik qoidalari ular uchun ham 100% to'liq ishlaydi.

## Ishlash natijasi:
```text
ZST hajmi: 0 bayt
ZST muvaffaqiyatli Move bo'ldi!
```

---

# 191-Topshiriq: Rekursiv strukturalarda kaskadli tozalanish (Drop Cascade)
## Topshiriq sharti:
Bog'langan ro'yxat (Linked List) oxiridan boshlab barcha tugunlarning ketma-ket o'chirilishi.

## Yechim (Rust kodi):
```rust
struct Tugun {
    qiymat: i32,
    keyingi: Option<Box<Tugun>>,
}

impl Drop for Tugun {
    fn drop(&mut self) {
        println!("Tugun ({}) xotiradan o'chirildi.", self.qiymat);
    }
}

fn main() {
    {
        let _royxat = Tugun {
            qiymat: 1,
            keyingi: Some(Box::new(Tugun {
                qiymat: 2,
                keyingi: None,
            })),
        };
        println!("Ro'yxat yaratildi.");
    }
    println!("Ro'yxat to'liq o'chirildi.");
}
```

## Tushuntirish va Mantiq:
Struktura o'chirilayotganda, uning ichidagi maydonlar ham o'chiriladi. Bu kaskadli tozalanish xotirada hech qanday unutilgan qoldiq qolmasligini kafolatlaydi.

## Ishlash natijasi:
```text
Ro'yxat yaratildi.
Tugun (1) xotiradan o'chirildi.
Tugun (2) xotiradan o'chirildi.
Ro'yxat to'liq o'chirildi.
```

---

# 192-Topshiriq: Bir nechta resurslarni bitta boshqaruvchiga topshirish (Manager Pattern)
## Topshiriq sharti:
Barcha resurslar egasligini bitta menejer strukturasiga yig'ing.

## Yechim (Rust kodi):
```rust
struct Resurs { nom: String }
struct Menejer { royxat: Vec<Resurs> }

fn main() {
    let r1 = Resurs { nom: String::from("Audio Dvigatel") };
    let r2 = Resurs { nom: String::from("Grafika Dvigateli") };

    let mut menejer = Menejer { royxat: Vec::new() };
    menejer.royxat.push(r1);
    menejer.royxat.push(r2);

    println!("Menejerdagi resurslar soni: {}", menejer.royxat.len());
}
```

## Tushuntirish va Mantiq:
Resurslar menejerga topshirilgach, ularning hayotiga faqat menejer javob beradi. Menejer o'lganda barcha ichki komponentlar ham xavfsiz yopiladi.

## Ishlash natijasi:
```text
Menejerdagi resurslar soni: 2
```

---

# 193-Topshiriq: Massivlarda elementlarni bittalab Move qilish cheklovi
## Topshiriq sharti:
Nega massivdan bitta elementni `arr[0]` orqali move qilib bo'lmaydi?

## Yechim (Rust kodi):
```rust
fn main() {
    let massiv = [String::from("Bir"), String::from("Ikki")];

    // let elem = massiv[0]; // Rust bunga ruxsat bermaydi, chunki massiv bo'shliq qoldira olmaydi!
    let elem = massiv[0].clone(); // Yechim: klonlash yoki indeks bo'yicha havola olish (&)

    println!("Olingan: {}", elem);
    println!("Massiv butun: {:?}", massiv);
}
```

## Tushuntirish va Mantiq:
Rust massivni qat'iy yaxlit blok deb hisoblaydi. Agar bitta element Move bo'lsa, massiv yarim bo'sh bo'lib qolardi va bu xotira xavfsizligiga ziddir.

## Ishlash natijasi:
```text
Olingan: Bir
Massiv butun: ["Bir", "Ikki"]
```

---

# 194-Topshiriq: Vektor pop() orqali elementni xavfsiz sug'urish
## Topshiriq sharti:
Vektordan element sug'urib olinganda egalikning ko'chishi.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut v = vec![String::from("Alfa"), String::from("Beta")];

    let oxirgi = v.pop(); // Option<String> qaytaradi va egaslikni o'tkazadi

    println!("Sug'urib olingan: {:?}", oxirgi);
    println!("Vektorda qolganlar: {:?}", v);
}
```

## Tushuntirish va Mantiq:
`pop()` metodi oxirgi elementni sug'urib olib, uning egasligini chaqiruvchiga topshiradi va vektor hajmini qisqartiradi.

## Ishlash natijasi:
```text
Sug'urib olingan: Some("Beta")
Vektorda qolganlar: ["Alfa"]
```

---

# 195-Topshiriq: Funktsiyaga massivning to'liq egasligini uzatish
## Topshiriq sharti:
Butun boshli massiv egasligini funksiyaga o'tkazish.

## Yechim (Rust kodi):
```rust
fn massiv_iste'moli(arr: [String; 2]) {
    println!("Massiv qabul qilindi: {:?}", arr);
}

fn main() {
    let m = [String::from("A"), String::from("B")];
    massiv_iste'moli(m);

    // println!("{:?}", m); // Xatolik: butun massiv MOVE bo'lgan!
}
```

## Tushuntirish va Mantiq:
Agar butun massiv funksiyaga uzatilsa, massivdagi barcha elementlar to'liq yangi funksiya ixtiyoriga o'tadi.

## Ishlash natijasi:
```text
Massiv qabul qilindi: ["A", "B"]
```

---

# 196-Topshiriq: Option unwrap() orqali qiymat egasligini ochish
## Topshiriq sharti:
`Some(T)` ichidagi Heap qiymatini to'g'ridan-to'g'ri o'zgaruvchiga ko'chirish.

## Yechim (Rust kodi):
```rust
fn main() {
    let opt = Some(String::from("Muvaffaqiyatli ma'lumot"));
    let qiymat = opt.unwrap(); // Egalik 'qiymat' ga o'tdi

    println!("Ochilgan qiymat: {}", qiymat);
}
```

## Tushuntirish va Mantiq:
`unwrap()` konsuming metod bo'lib, `self` ni iste'mol qiladi va ichidagi `T` ning to'liq egasligini qaytaradi.

## Ishlash natijasi:
```text
Ochilgan qiymat: Muvaffaqiyatli ma'lumot
```

---

# 197-Topshiriq: Xotira xavfsizligi: Use-After-Free xatosining 0% ehtimoli
## Topshiriq sharti:
Rust kompilyatori qanday qilib o'chirilgan xotiraga qayta murojaat qilishni butunlay to'xtatishini ko'rsating.

## Yechim (Rust kodi):
```rust
fn main() {
    let s = String::from("Xavfsiz ma'lumot");
    drop(s);

    // println!("{}", s); // Kompilyator "borrow of moved value: `s`" xatoligi bilan dasturni to'xtatadi!
    println!("Rust Use-After-Free xatosini dastur ishga tushmasidanoq yo'q qiladi!");
}
```

## Tushuntirish va Mantiq:
C tilida dasturchilar eng ko'p yo'l qo'yadigan Use-After-Free xatosi Rust da kompilyator darajasida imkonsiz qilib qo'yilgan.

## Ishlash natijasi:
```text
Rust Use-After-Free xatosini dastur ishga tushmasidanoq yo'q qiladi!
```

---

# 198-Topshiriq: Ownership va ko'p oqimli xavfsizlik (Data Race yo'qligi)
## Topshiriq sharti:
Bitta resursga faqat bitta egasi bo'lishi qanday qilib oqimlar poygasini yo'qotishini tushuntiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let xabar = String::from("Oqimlar xabari");

    // Rust da bitta o'zgaruvchini ikki xil oqim bir vaqtda to'g'ridan-to'g'ri yozishi mumkin emas
    println!("Yagona egasi bor xabar: {}", xabar);
    println!("Bu xususiyat 'Fearless Concurrency' (Qo'rqmas parallelizm) ning asosi!");
}
```

## Tushuntirish va Mantiq:
Hech qanday ikki oqim bitta xotiraga bir vaqtda nazoratsiz yozolmaydi, chunki yagona egalik qoidasi bunga yo'l qo'ymaydi.

## Ishlash natijasi:
```text
Yagona egasi bor xabar: Oqimlar xabari
Bu xususiyat 'Fearless Concurrency' (Qo'rqmas parallelizm) ning asosi!
```

---

# 199-Topshiriq: Xotira oqishi (Memory Leak) va uning oldini olish
## Topshiriq sharti:
Rust da egalik tizimi xotira oqishining 99.9% tabiiy holatda oldini olishini ko'rsating.

## Yechim (Rust kodi):
```rust
fn main() {
    for _ in 0..1000 {
        let _vaqtinchalik = vec![1, 2, 3, 4, 5];
    } // Har bir aylanishda xotira darhol bo'shatiladi

    println!("1000 ta vektor yaratildi va hech qanday xotira oqishisiz tozalandi.");
}
```

## Tushuntirish va Mantiq:
Garbage Collector li tillarda GC tozalaguncha xotira ko'payib boradi. Rust da esa scope tugashi bilan xotira o'sha zahotiyoq operatsion tizimga qaytariladi.

## Ishlash natijasi:
```text
1000 ta vektor yaratildi va hech qanday xotira oqishisiz tozalandi.
```

---

# 200-Topshiriq: Xulosa: Nol xarajatli abstraksiya (Zero-cost Abstraction)
## Topshiriq sharti:
Ownership tizimining dastur ishlash tezligiga 0 nanosekund ham qo'shimcha yuk bo'lmasligini tushuntiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let s = String::from("Nol xarajat");
    let uzunlik = s.len();

    println!("Matn: '{}', uzunligi: {}", s, uzunlik);
    println!("Egalik tekshiruvlari faqat kompilyatsiya vaqtida bajariladi!");
    println!("Binar fayl ichida qo'shimcha tekshiruv kodlari umuman mavjud bo'lmaydi.");
}
```

## Tushuntirish va Mantiq:
Rust ning 'Zero-cost abstractions' shiori aynan shuni anglatadi: Siz yuqori darajadagi xotira xavfsizligiga ega bo'lasiz, ammo dasturingiz xuddi qo'lda optimallashtirilgan C kodi kabi maksimal tezlikda ishlaydi.

## Ishlash natijasi:
```text
Matn: 'Nol xarajat', uzunligi: 11
Egalik tekshiruvlari faqat kompilyatsiya vaqtida bajariladi!
Binar fayl ichida qo'shimcha tekshiruv kodlari umuman mavjud bo'lmaydi.
```

---
