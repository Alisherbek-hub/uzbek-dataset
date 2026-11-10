# Rust Dasturlash Tili: Mukammal Qo'llanma va Ensiklopediya
## (Noldan Xotira Xavfsizligi, Tizimli Dasturlash va Zamonaviy AI Dvigatellarigacha)

> **Standart:** Rust Edition 2021 / 2024  
> **Asosiy tamoyil:** Axlat yig'uvchisiz (Garbage Collector siz) 100% xotira xavfsizligi va qo'rqmas parallelizm (Fearless Concurrency).

---

## MUNDARIJA

1. [1-Bob: Rust Falsafasi, Tarixi va Cargo Ekotizimi](#1-bob)
2. [2-Bob: O'zgaruvchilar, Mutability va Shadowing](#2-bob)
3. [3-Bob: Ownership (Egalik) Tizimi — Rust ning Yuragi](#3-bob)
4. [4-Bob: Borrowing (Qarz olish) va Havolalar Qoidalari](#4-bob)
5. [5-Bob: Lifetimes (Umr ko'rish muddatlari: `'a`)](#5-bob)
6. [6-Bob: Structs, Enums va Quvvatli Pattern Matching](#6-bob)
7. [7-Bob: Xatoliklarni Boshqarish: `Result`, `Option` va `?` Operatori](#7-bob)
8. [8-Bob: Traits, Generics va Dinamik Dispatch (`dyn Trait`)](#8-bob)
9. [9-Bob: Aqlli Ko'rsatkichlar: `Box`, `Rc`, `Arc`, `RefCell`](#9-bob)
10. [10-Bob: Qo'rqmas Parallelizm: `std::thread`, `mpsc`, `Mutex`, `Send & Sync`](#10-bob)
11. [11-Bob: Asinxron Rust va Tokio Dvigateli](#11-bob)
12. [12-Bob: Unsafe Rust va C-FFI Integratsiyasi](#12-bob)
13. [13-Bob: Maxsus Bob: Rust tilida 1-Bit LLM Tensor va Kvantlangan Matritsa](#13-bob)

---

<a name="1-bob"></a>
# 1-Bob: Rust Falsafasi, Tarixi va Cargo Ekotizimi

Rust tili Mozilla kompaniyasida Graydon Xor (Graydon Hoare) tomonidan ishlab chiqilgan bo'lib, Stack Overflow so'rovnomasida ketma-ket 8 yil davomida **"Dunyodagi eng sevimli dasturlash tili"** deb topildi.

### 1.1. Cargo — Zamonaviy Paket Menejeri
* `cargo new loyiha_nomi`: Yangi loyiha yaratish
* `cargo check`: Tezkor sintaktik va tip tekshiruvi (kompilyatsiyasiz)
* `cargo build --release`: Maksimal tezlikka optimallashtirib binar fayl chiqarish
* `cargo test`: O'rnatilgan birlik testlarini ishga tushirish

```rust
fn main() {
    println!("Assalomu alaykum, Rust dunyosi!");
}
```

---

<a name="2-bob"></a>
# 2-Bob: O'zgaruvchilar, Mutability va Shadowing

Rust da barcha o'zgaruvchilar standart holatda **o'zgarmas (immutable)** bo'ladi. O'zgaruvchini o'zgartirish uchun `mut` kalit so'zi talab qilinadi:

```rust
let x = 5;
// x = 6; // XATO! x immutable

let mut y = 10;
y = 15; // To'g'ri

// Shadowing (qayta e'lon qilish):
let matn = "   salom   ";
let matn = matn.trim(); // Tipini o'zgartirish ham mumkin
```

---

<a name="3-bob"></a>
# 3-Bob: Ownership (Egalik) Tizimi — Rust ning Yuragi

Rust tili C/C++ kabi qo'lda xotira tozalashni (free) ham, Java/Go/Python kabi orqa fonda xotirani tozalovchi GC ni ham talab qilmaydi. Uning o'rniga **Ownership** mexanizmi ishlaydi.

### Ownership ning 3 ta Oltin Qoidasi:
1. Rust da har bir qiymatning faqat **bitta egasi (owner)** bo'ladi.
2. Bir vaqtning o'zida faqat bitta egasi bo'lishi mumkin.
3. Egasi o'z doirasidan (scope) chiqib ketganda, qiymat xotiradan avtomatik **Drop** qilinadi (o'chiriladi).

```rust
{
    let s1 = String::from("O'zbekiston");
    let s2 = s1; // MOVE yuz berdi: s1 endi yaroqsiz!
    // println!("{}", s1); // KOMPILYATSIYA XATOSI!
    println!("{}", s2);
} // Bu yerda s2 xotiradan tozalanadi
```

---

<a name="4-bob"></a>
# 4-Bob: Borrowing (Qarz olish) va Havolalar Qoidalari

Egalikni topshirmasdan qiymatdan foydalanish uchun unga **havola (reference: `&`)** beriladi.

### Borrowing ning 2 ta Qat'iy Qoidasi:
* Bir vaqtning o'zida sizda xohlagancha **o'zgarmas havolalar (`&T`)** bo'lishi mumkin;
* YOKI faqat bittagina **o'zgaruvchan havola (`&mut T`)** bo'lishi mumkin.
* Ikkalasi bir vaqtda aslo mavjud bo'la olmaydi! Bu esa **Data Race** (poyga sharoiti) xatosini 100% yo'qotadi.

```rust
let mut kitob = String::from("O'tkan kunlar");
let r1 = &kitob; // O'qish uchun havola
let r2 = &kitob; // Yana bitta o'quvchi
println!("{} va {}", r1, r2);

let r3 = &mut kitob; // Endi yozish uchun bitta havola
r3.push_str(" (Abdulla Qodiriy)");
```

---

<a name="5-bob"></a>
# 5-Bob: Lifetimes (Umr ko'rish muddatlari: `'a`)

Lifetimes — havolalarning xotirada qancha vaqt yashashini kompilyatorga ko'rsatuvchi belgi bo'lib, **Dangling Pointer** (bo'shliqqa qaratilgan ko'rsatkich) xatolarini butunlay bartaraf etadi:

```rust
// Qaysi havola uzoqroq yashashini ko'rsatuvchi 'a generic lifetime
fn eng_uzun<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}
```

---

<a name="6-bob"></a>
# 6-Bob: Structs, Enums va Quvvatli Pattern Matching

Rust dagi `enum` lar boshqa tillardagi kabi oddiy raqamlar emas, balki ichida ma'lumot saqlay oluvchi **Algebraik Ma'lumotlar Turi (ADT)** dir:

```rust
enum Xabar {
    Chiqish,
    Kiritish(String),
    Kordinata { x: i32, y: i32 },
}

fn qayta_ishla(xabar: Xabar) {
    match xabar {
        Xabar::Chiqish => println!("Dastur to'xtatildi"),
        Xabar::Kiritish(matn) => println!("Kelgan matn: {}", matn),
        Xabar::Kordinata { x, y } => println!("Nuqta: ({}, {})", x, y),
    }
}
```

---

<a name="7-bob"></a>
# 7-Bob: Xatoliklarni Boshqarish: `Result`, `Option` va `?` Operatori

Rust da `null` yoki `nil` tushunchasi yo'q. Qiymat bor yoki yo'qligi `Option<T>` orqali ifodalanadi:
* `Option<T>`: `Some(qiymat)` yoki `None`.
* `Result<T, E>`: `Ok(natija)` yoki `Err(xatolik)`.

`?` operatori xatolik yuz berganda uni zudlik bilan tashqi chaqiruvchiga uzatadi:
```rust
use std::fs::File;
use std::io::{self, Read};

fn faylni_oqish(nom: &str) -> Result<String, io::Error> {
    let mut f = File::open(nom)?; // Xato bo'lsa darhol qaytadi
    let mut matn = String::new();
    f.read_to_string(&mut matn)?;
    Ok(matn)
}
```

---

<a name="8-bob"></a>
# 8-Bob: Traits, Generics va Dinamik Dispatch (`dyn Trait`)

`trait` — boshqa tillardagi interfeysga o'xshaydi, ammo undan ancha kuchliroq:
```rust
trait Ovoz {
    fn ovoz_chiqar(&self) -> String;
}

struct Mushuk;
impl Ovoz for Mushuk {
    fn ovoz_chiqar(&self) -> String {
        String::from("Miyov!")
    }
}
```

---

<a name="9-bob"></a>
# 9-Bob: Aqlli Ko'rsatkichlar: `Box`, `Rc`, `Arc`, `RefCell`

* `Box<T>`: Ma'lumotni Heap xotirada saqlash uchun.
* `Rc<T>`: Bitta oqimda ko'p egalik (Reference Counting).
* `Arc<T>`: Ko'p oqimli xavfsiz egalik (Atomic Reference Counting).
* `RefCell<T>`: Kompilyatsiya vaqtida emas, dastur ishlashi paytida (Runtime) qarz olishni tekshiruvchi Interior Mutability vositasi.

---

<a name="10-bob"></a>
# 10-Bob: Qo'rqmas Parallelizm: `std::thread`, `mpsc`, `Mutex`, `Send & Sync`

Rust ning shiori: **"Agar kod kompilyatsiya bo'lsa, unda poyga sharoiti (Data Race) bo'lmaydi!"**
```rust
use std::sync::{Arc, Mutex};
use std::thread;

let hisob = Arc::new(Mutex::new(0));
let mut handles = vec![];

for _ in 0..10 {
    let hisob_nusxa = Arc::clone(&hisob);
    let handle = thread::spawn(move || {
        let mut num = hisob_nusxa.lock().unwrap();
        *num += 1;
    });
    handles.push(handle);
}

for h in handles { h.join().unwrap(); }
println!("Yakuniy natija: {}", *hisob.lock().unwrap());
```

---

<a name="11-bob"></a>
# 11-Bob: Asinxron Rust va Tokio Dvigateli

Tokio kutubxonasi yordamida soniyasiga millionlab so'rovlarni o'tkazuvchi yuqori unumdorlikdagi asinxron tarmoq serverlari quriladi.

---

<a name="12-bob"></a>
# 12-Bob: Unsafe Rust va C-FFI Integratsiyasi

Rust ning barcha xavfsizlik cheklovlarini vaqtincha chetlab o'tib, apparat registrlari va C kutubxonalari bilan ishlash uchun `unsafe` bloki ishlatiladi.

---

<a name="13-bob"></a>
# 13-Bob: Maxsus Bob: Rust tilida 1-Bit LLM Tensor va Kvantlangan Matritsa

Rust tili xotira barqarorligi va yuqori tezligi tufayli zamonaviy AI freymvorklari (masalan, Hugging Face tomonidan yaratilgan **Candle** va **Burn**) uchun asosiy tilga aylanmoqda.

Quyidagi sof Rust dasturi 1-bitli kvantlangan vaznlar bilan xotirani tejab inferensiya qilishni amalga oshiradi:

```rust
pub struct OneBitLinear {
    in_features: usize,
    out_features: usize,
    weights: Vec<i8>, // -1 yoki +1
}

impl OneBitLinear {
    pub fn new(in_features: usize, out_features: usize) -> Self {
        let mut weights = Vec::with_capacity(in_features * out_features);
        for i in 0..(in_features * out_features) {
            weights.push(if i % 2 == 0 { 1 } else { -1 });
        }
        Self { in_features, out_features, weights }
    }

    pub fn forward(&self, input: &[f32]) -> Vec<f32> {
        assert_eq!(input.len(), self.in_features);
        let mut output = vec![0.0f32; self.out_features];

        for j in 0..self.out_features {
            let mut sum = 0.0f32;
            for i in 0..self.in_features {
                let w = self.weights[i * self.out_features + j];
                if w == 1 {
                    sum += input[i];
                } else {
                    sum -= input[i];
                }
            }
            output[j] = sum;
        }
        output
    }
}

fn main() {
    let layer = OneBitLinear::new(4, 4);
    let x = vec![0.5, -0.2, 0.8, 0.1];
    let y = layer.forward(&x);

    println!("Rust 1-Bit Model Chiqishi: {:?}", y);
}
```

---

## XULOSA

Rust — XXI asrning eng xavfsiz va eng tezkor tizimli dasturlash tili. Ushbu qo'llanma O'zbekiston yoshlariga eng ishonchli bulutli platformalar, kiberxavfsizlik vositalari va sun'iy intellekt modellarini yaratishda jahon darajasidagi bilim taqdim etadi!
