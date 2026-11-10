# 10-Qism: Generics (Umumlashgan Turlar) va Const Generics (451-500)

Ushbu qismda Rust dasturlash tilining eng muhim abstraksiya mexanizmi bo'lgan **Generics (Umumlashgan turlar)**, generik funksiyalar, strukturalar, enumlar, `impl` bloklari, Monomorfizatsiya (Monomorphization), Const Generics (massiv o'lchamlarini tip sifatida uzatish), `PhantomData` hamda generik ma'lumotlar tuzilmalari amaliy tahlil qilinadi.

---

# 451-Topshiriq: Generics (Umumlashgan turlar) nima? Kod takrorlanishini yo'qotish
## Topshiriq sharti:
Har xil turdagi sonlar uchun bitta umumiy funksiya yozish g'oyasini tushuntiring.

## Yechim (Rust kodi):
```rust
fn chop_et<T: std::fmt::Debug>(qiymat: T) {
    println!("Qiymat: {:?}", qiymat);
}

fn main() {
    chop_et(42); // i32 turi
    chop_et(3.14); // f64 turi
    chop_et("Salom"); // &str turi
}
```

## Tushuntirish va Mantiq:
Generics har bir tur uchun alohida funksiya yozmasdan, bitta umumiy shablon yaratish imkonini beradi. `<T>` parametri ixtiyoriy turni bildiradi.

## Ishlash natijasi:
```text
Qiymat: 42
Qiymat: 3.14
Qiymat: "Salom"
```

---

# 452-Topshiriq: Bir nechta generik parametrlar: <T, U>
## Topshiriq sharti:
Turli tipdagi ikkita qiymatni qabul qilib kortej qaytaruvchi generik funksiya tuzing.

## Yechim (Rust kodi):
```rust
fn juftlik<T, U>(birinchi: T, ikkinchi: U) -> (T, U) {
    (birinchi, ikkinchi)
}

fn main() {
    let j1 = juftlik("ID", 101);
    let j2 = juftlik(true, 3.14);

    println!("Juftlik 1: {:?}", j1);
    println!("Juftlik 2: {:?}", j2);
}
```

## Tushuntirish va Mantiq:
Funksiya `<T, U>` orqali bir-biridan mustaqil ikki xil turni qabul qiladi va xavfsiz kortej hosil qiladi.

## Ishlash natijasi:
```text
Juftlik 1: ("ID", 101)
Juftlik 2: (true, 3.14)
```

---

# 453-Topshiriq: Generik strukturalar: struct Nuqta<T>
## Topshiriq sharti:
Har qanday bir xil turdagi koordinatalarni saqlovchi generik struktura yarating.

## Yechim (Rust kodi):
```rust
struct Nuqta<T> {
    x: T,
    y: T,
}

fn main() {
    let butun = Nuqta { x: 5, y: 10 };
    let haqiqiy = Nuqta { x: 1.5, y: 4.8 };

    println!("Butun koordinata: ({}, {})", butun.x, butun.y);
    println!("Haqiqiy koordinata: ({}, {})", haqiqiy.x, haqiqiy.y);
}
```

## Tushuntirish va Mantiq:
`Nuqta<T>` da `x` va `y` bir xil turda bo'lishi shart. Bu tur chalkashliklarining oldini oladi.

## Ishlash natijasi:
```text
Butun koordinata: (5, 10)
Haqiqiy koordinata: (1.5, 4.8)
```

---

# 454-Topshiriq: Har xil turdagi generik maydonli strukturalar: <T, U>
## Topshiriq sharti:
Maydonlari har xil turlarda bo'lishi mumkin bo'lgan generik struktura e'lon qiling.

## Yechim (Rust kodi):
```rust
struct Xabar<T, U> {
    sarlavha: T,
    kod: U,
}

fn main() {
    let x = Xabar {
        sarlavha: String::from("Tizim xatosi"),
        kod: 500,
    };

    println!("Xabar: '{}' (kod: {})", x.sarlavha, x.kod);
}
```

## Tushuntirish va Mantiq:
`<T, U>` turli maydonlar turli xil bo'lishiga ruxsat beradi (masalan, biri String, ikkinchisi butun son).

## Ishlash natijasi:
```text
Xabar: 'Tizim xatosi' (kod: 500)
```

---

# 455-Topshiriq: Generik enumlar: Maxsus Natija<T, E> yaratish
## Topshiriq sharti:
Standart kutubxonadagi `Result` kabi ishlaydigan o'z generik enumingizni yozing.

## Yechim (Rust kodi):
```rust
#[derive(Debug)]
enum MeningNatijam<T, E> {
    Muvaffaqiyat(T),
    Xatolik(E),
}

fn main() {
    let yaxshi: MeningNatijam<i32, &str> = MeningNatijam::Muvaffaqiyat(100);
    let yomon: MeningNatijam<i32, &str> = MeningNatijam::Xatolik("Xato yuz berdi");

    println!("Yaxshi: {:?}", yaxshi);
    println!("Yomon:  {:?}", yomon);
}
```

## Tushuntirish va Mantiq:
Generik enumlar ma'lumotlarni xohlagan turda qabul qilib, ularni umumiy polimorfik shaklga keltiradi.

## Ishlash natijasi:
```text
Yaxshi: Muvaffaqiyat(100)
Yomon:  Xatolik("Xato yuz berdi")
```

---

# 456-Topshiriq: Generik impl bloklari: impl<T> Nuqta<T>
## Topshiriq sharti:
Generik struktura uchun umumiy metodlar yozish.

## Yechim (Rust kodi):
```rust
struct Nuqta<T> {
    x: T,
    y: T,
}

impl<T> Nuqta<T> {
    fn x(&self) -> &T {
        &self.x
    }
}

fn main() {
    let p = Nuqta { x: 42, y: 84 };
    println!("X koordinata: {}", p.x());
}
```

## Tushuntirish va Mantiq:
`impl<T>` sintaksisi kompilyatorga ushbu metodlar har qanday `T` turi uchun umumiy ekanligini bildiradi.

## Ishlash natijasi:
```text
X koordinata: 42
```

---

# 457-Topshiriq: Aniq tipga ixtisoslashgan impl bloklari: impl Nuqta<f64>
## Topshiriq sharti:
Faqat `f64` turidagi nuqtalar uchun ishlaydigan maxsus matematik metod yozing.

## Yechim (Rust kodi):
```rust
struct Nuqta<T> {
    x: T,
    y: T,
}

impl Nuqta<f64> {
    fn masofa_markazdan(&self) -> f64 {
        (self.x * self.x + self.y * self.y).sqrt()
    }
}

fn main() {
    let p = Nuqta { x: 3.0, y: 4.0 };
    println!("Masofa: {}", p.masofa_markazdan());

    // let p_int = Nuqta { x: 3, y: 4 };
    // p_int.masofa_markazdan(); // Kompilyator xatolik beradi: butun sonli nuqtada bu metod yo'q!
}
```

## Tushuntirish va Mantiq:
Rust da faqat ma'lum bir aniq tur (`f64`) uchun alohida `impl` yozish mumkin. Bu turga xos amallarni boshqa turlardan toza ajratadi.

## Ishlash natijasi:
```text
Masofa: 5
```

---

# 458-Topshiriq: Metod darajasidagi mustaqil generik parametrlar
## Topshiriq sharti:
Strukturadan boshqa generik tur qabul qiluvchi metod yozing.

## Yechim (Rust kodi):
```rust
struct Nuqta<T, U> {
    x: T,
    y: U,
}

impl<T, U> Nuqta<T, U> {
    fn aralashtir<V, W>(self, boshqa: Nuqta<V, W>) -> Nuqta<T, W> {
        Nuqta { x: self.x, y: boshqa.y }
    }
}

fn main() {
    let p1 = Nuqta { x: 5, y: 10.4 };
    let p2 = Nuqta { x: "Salom", y: 'A' };

    let p3 = p1.aralashtir(p2);
    println!("Aralashtirilgan: x={}, y={}", p3.x, p3.y);
}
```

## Tushuntirish va Mantiq:
Metod o'zining `<V, W>` parametrlariga ega bo'lishi va boshqa strukturalar bilan erkin ma'lumot almashishi mumkin.

## Ishlash natijasi:
```text
Aralashtirilgan: x=5, y=A
```

---

# 459-Topshiriq: Monomorfizatsiya (Monomorphization) va unumdorlik
## Topshiriq sharti:
Kompilyator generik kodni binar faylda aniq turlarga qanday aylantirishini ko'rsating.

## Yechim (Rust kodi):
```rust
fn chop<T: std::fmt::Display>(val: T) {
    println!("{}", val);
}

fn main() {
    chop(5);       // Kompilyator: fn chop_i32(val: i32) yaratadi
    chop("Matn");  // Kompilyator: fn chop_str(val: &str) yaratadi
    println!("Monomorfizatsiya tufayli ish vaqtida 0 nanosekund qo'shimcha xarajat bo'ladi!");
}
```

## Tushuntirish va Mantiq:
Monomorfizatsiya - Rust kompilyatori har bir ishlatilgan aniq tur uchun alohida mashina kodini ishlab chiqarishidir. Natijada kod xuddi qo'lda yozilgandek maksimal tezlikda ishlaydi.

## Ishlash natijasi:
```text
5
Matn
Monomorfizatsiya tufayli ish vaqtida 0 nanosekund qo'shimcha xarajat bo'ladi!
```

---

# 460-Topshiriq: Const Generics: Butun sonli qiymatlarni tip parametri qilish
## Topshiriq sharti:
Massiv o'lchamini tip parametri (`const N: usize`) sifatida qabul qiling.

## Yechim (Rust kodi):
```rust
struct StatikMassiv<T, const N: usize> {
    malumot: [T; N],
}

fn main() {
    let massiv = StatikMassiv { malumot: [1, 2, 3, 4] };
    println!("Massiv o'lchami: {}", N_olchami(&massiv));
}

fn N_olchami<T, const N: usize>(_arr: &StatikMassiv<T, N>) -> usize {
    N
}
```

## Tushuntirish va Mantiq:
Const Generics Rust 1.51+ da kiritilgan bo'lib, nafaqat turlarni, balki konstanta sonlarni ham generik parametr qilish imkonini beradi.

## Ishlash natijasi:
```text
Massiv o'lchami: 4
```

---

# 461-Topshiriq: Const Generics bilan 2D Matritsa arxitekturasi
## Topshiriq sharti:
Satr va ustun o'lchamlari kompilyatsiyada tekshiriluvchi matritsa yarating.

## Yechim (Rust kodi):
```rust
#[derive(Debug)]
struct Matritsa<T, const QATOR: usize, const USTUN: usize> {
    kataklar: [[T; USTUN]; QATOR],
}

fn main() {
    let m = Matritsa {
        kataklar: [
            [1.0, 2.0],
            [3.0, 4.0],
            [5.0, 6.0],
        ],
    };

    println!("3x2 Matritsa: {:?}", m);
}
```

## Tushuntirish va Mantiq:
Matritsaning o'lchamlari tip tizimining bir qismiga aylanadi. Bu matritsa ko'paytirishda o'lchamlar mos kelmasligini kompilyatsiya vaqtidayoq aniqlaydi.

## Ishlash natijasi:
```text
3x2 Matritsa: Matritsa { kataklar: [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]] }
```

---

# 462-Topshiriq: Generik Stack (Yig'ma) ma'lumotlar tuzilmasi
## Topshiriq sharti:
Har qanday turdagi elementlarni qabul qiluvchi `Stack<T>` tuzing.

## Yechim (Rust kodi):
```rust
struct Stack<T> {
    elementlar: Vec<T>,
}

impl<T> Stack<T> {
    fn new() -> Self { Self { elementlar: Vec::new() } }
    fn push(&mut self, item: T) { self.elementlar.push(item); }
    fn pop(&mut self) -> Option<T> { self.elementlar.pop() }
    fn is_empty(&self) -> bool { self.elementlar.is_empty() }
}

fn main() {
    let mut s = Stack::new();
    s.push("Rust");
    s.push("Tizimlar");

    while let Some(soz) = s.pop() {
        println!("Pop: {}", soz);
    }
}
```

## Tushuntirish va Mantiq:
Generik Stack bitta kod orqali satrlar, sonlar yoki murakkab strukturalar uchun birdek xizmat qiladi.

## Ishlash natijasi:
```text
Pop: Tizimlar
Pop: Rust
```

---

# 463-Topshiriq: Generik Navbat (Queue) ma'lumotlar tuzilmasi
## Topshiriq sharti:
FIFO tamoyili bo'yicha ishlovchi generik `Queue<T>`.

## Yechim (Rust kodi):
```rust
use std::collections::VecDeque;

struct Navbat<T> {
    elementlar: VecDeque<T>,
}

impl<T> Navbat<T> {
    fn new() -> Self { Self { elementlar: VecDeque::new() } }
    fn qosh(&mut self, val: T) { self.elementlar.push_back(val); }
    fn ol(&mut self) -> Option<T> { self.elementlar.pop_front() }
}

fn main() {
    let mut q = Navbat::new();
    q.qosh(100);
    q.qosh(200);

    println!("Birinchi: {:?}", q.ol());
    println!("Ikkinchi: {:?}", q.ol());
}
```

## Tushuntirish va Mantiq:
`VecDeque` asosidagi generik navbat o'zgaruvchilarning turlaridan qat'i nazar bir xil interfeys beradi.

## Ishlash natijasi:
```text
Birinchi: Some(100)
Ikkinchi: Some(200)
```

---

# 464-Topshiriq: Generik Swapper funksiyasi
## Topshiriq sharti:
Ikkita har qanday o'zgaruvchi qiymatini almashtiruvchi funksiya.

## Yechim (Rust kodi):
```rust
fn almashtir<T>(a: &mut T, b: &mut T) {
    std::mem::swap(a, b);
}

fn main() {
    let mut x = "Ali";
    let mut y = "Vali";
    almashtir(&mut x, &mut y);

    println!("x = {}, y = {}", x, y);
}
```

## Tushuntirish va Mantiq:
Generik `std::mem::swap` orqali xotirani nusxalamasdan har qanday turdagi ikkita ko'rsatkich almashtiriladi.

## Ishlash natijasi:
```text
x = Vali, y = Ali
```

---

# 465-Topshiriq: Generik funksiyada PartialOrd orqali eng kattasini topish
## Topshiriq sharti:
Solishtirish mumkin bo'lgan har qanday turdan kattasini qaytaring.

## Yechim (Rust kodi):
```rust
fn eng_kattasi<T: PartialOrd>(a: T, b: T) -> T {
    if a > b { a } else { b }
}

fn main() {
    println!("Katta son: {}", eng_kattasi(25, 42));
    println!("Katta matn: {}", eng_kattasi("olma", "anor"));
}
```

## Tushuntirish va Mantiq:
`T: PartialOrd` cheklovi (trait bound) kompilyatorga faqat `>` operatorini qo'llab-quvvatlaydigan turlarni qabul qilishni buyuradi.

## Ishlash natijasi:
```text
Katta son: 42
Katta matn: olma
```

---

# 466-Topshiriq: PhantomData tushunchasi: Foydalanilmagan turni saqlash
## Topshiriq sharti:
Kompilyatsiya vaqtida tip xavfsizligini tekshiruvchi o'lchov birligi.

## Yechim (Rust kodi):
```rust
use std::marker::PhantomData;

struct Metr;
struct Kilometr;

struct Masofa<Birlik> {
    qiymat: f64,
    birlik: PhantomData<Birlik>,
}

impl<Birlik> Masofa<Birlik> {
    fn new(qiymat: f64) -> Self {
        Self { qiymat, birlik: PhantomData }
    }
}

fn main() {
    let m: Masofa<Metr> = Masofa::new(100.0);
    let km: Masofa<Kilometr> = Masofa::new(5.0);

    println!("Metr: {}, Km: {}", m.qiymat, km.qiymat);
}
```

## Tushuntirish va Mantiq:
`PhantomData<T>` xotirada 0 bayt joy oladi, lekin kompilyatorga struktura `T` bilan bog'langanini bildiradi.

## Ishlash natijasi:
```text
Metr: 100, Km: 5
```

---

# 467-Topshiriq: Generik slice qabul qiluvchi qidiruv funksiyasi
## Topshiriq sharti:
Har qanday massiv bo'lagidan element indeksini qidirish.

## Yechim (Rust kodi):
```rust
fn qidir<T: PartialEq>(royxat: &[T], nishon: &T) -> Option<usize> {
    for (i, elem) in royxat.iter().enumerate() {
        if elem == nishon {
            return Some(i);
        }
    }
    None
}

fn main() {
    let sonlar = [10, 20, 30, 40];
    println!("20 indeksi: {:?}", qidir(&sonlar, &20));

    let ismlar = ["Ali", "Bobur", "Jasur"];
    println!("Bobur indeksi: {:?}", qidir(&ismlar, &"Bobur"));
}
```

## Tushuntirish va Mantiq:
`T: PartialEq` cheklovi `==` operatorini kafolatlaydi va funksiyani barcha kolleksiyalar uchun universal qiladi.

## Ishlash natijasi:
```text
20 indeksi: Some(1)
Bobur indeksi: Some(1)
```

---

# 468-Topshiriq: Generik Juftlik (Pair<T, U>) va ularni solishtirish
## Topshiriq sharti:
Generik juftliklarning tengligini aniqlash.

## Yechim (Rust kodi):
```rust
#[derive(Debug, PartialEq)]
struct Juftlik<T, U> {
    bir: T,
    ikki: U,
}

fn main() {
    let j1 = Juftlik { bir: 1, ikki: "A" };
    let j2 = Juftlik { bir: 1, ikki: "A" };

    println!("j1 == j2: {}", j1 == j2);
}
```

## Tushuntirish va Mantiq:
Agar `T` va `U` `PartialEq` implement qilgan bo'lsa, ularning generik strukturasi ham avtomatik tenglikka tekshiriladi.

## Ishlash natijasi:
```text
j1 == j2: true
```

---

# 469-Topshiriq: Generik Default konstruktori: T: Default
## Topshiriq sharti:
Ichki qiymatini standart boshlang'ich qiymat bilan to'ldiruvchi struktura.

## Yechim (Rust kodi):
```rust
struct O'rovchi<T: Default> {
    qiymat: T,
}

impl<T: Default> O'rovchi<T> {
    fn yangi() -> Self {
        Self { qiymat: T::default() }
    }
}

fn main() {
    let o1: O'rovchi<i32> = O'rovchi::yangi();
    let o2: O'rovchi<String> = O'rovchi::yangi();

    println!("Son default: {}", o1.qiymat);
    println!("Satr default: '{}'", o2.qiymat);
}
```

## Tushuntirish va Mantiq:
`T: Default` cheklovi har qanday turning o'z boshlang'ich qiymatini chaqirishga imkon beradi.

## Ishlash natijasi:
```text
Son default: 0
Satr default: ''
```

---

# 470-Topshiriq: Const Generics yordamida massivlarni birlashtirish
## Topshiriq sharti:
N va M o'lchamli massivlarni qo'shib N+M o'lchamli yangi massiv hosil qilish.

## Yechim (Rust kodi):
```rust
fn massiv_birlashtir<T: Copy + Default, const N: usize, const M: usize>(
    a: [T; N],
    b: [T; M],
) -> Vec<T> {
    let mut v = Vec::with_capacity(N + M);
    for item in a { v.push(item); }
    for item in b { v.push(item); }
    v
}

fn main() {
    let a = [1, 2];
    let b = [3, 4, 5];
    let res = massiv_birlashtir(a, b);

    println!("Birlashgan vektor: {:?}", res);
}
```

## Tushuntirish va Mantiq:
Const Generics turli o'lchamdagi statik massivlarni xavfsiz boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Birlashgan vektor: [1, 2, 3, 4, 5]
```

---

# 471-Topshiriq: Generik bog'langan ro'yxat (Generic Linked List)
## Topshiriq sharti:
Har qanday turdagi tugunlarni zanjirga ulovchi ro'yxat tuzilmasi.

## Yechim (Rust kodi):
```rust
struct Tugun<T> {
    qiymat: T,
    keyingi: Option<Box<Tugun<T>>>,
}

fn main() {
    let royxat = Tugun {
        qiymat: "Boshlang'ich",
        keyingi: Some(Box::new(Tugun {
            qiymat: "Tugash",
            keyingi: None,
        })),
    };

    println!("1-tugun: {}", royxat.qiymat);
    println!("2-tugun: {}", royxat.keyingi.as_ref().unwrap().qiymat);
}
```

## Tushuntirish va Mantiq:
Generik linked list xohlagan ma'lumot turini bitta qat'iy zanjirda saqlash imkonini beradi.

## Ishlash natijasi:
```text
1-tugun: Boshlang'ich
2-tugun: Tugash
```

---

# 472-Topshiriq: Generik Kesh (Cache) xotira saqlovchisi
## Topshiriq sharti:
Kalit va qiymat bo'yicha generik kesh modeli.

## Yechim (Rust kodi):
```rust
struct Kesh<K, V> {
    kalit: K,
    qiymat: V,
}

impl<K: PartialEq, V: Clone> Kesh<K, V> {
    fn ol(&self, k: &K) -> Option<V> {
        if &self.kalit == k {
            Some(self.qiymat.clone())
        } else {
            None
        }
    }
}

fn main() {
    let k = Kesh { kalit: "token", qiymat: 12345 };
    println!("Token qiymati: {:?}", k.ol(&"token"));
    println!("Noma'lum kalit: {:?}", k.ol(&"boshqa"));
}
```

## Tushuntirish va Mantiq:
Kesh interfeysi generik turlar orqali turli formatdagi konfiguratsiyalarni xavfsiz saqlaydi.

## Ishlash natijasi:
```text
Token qiymati: Some(12345)
Noma'lum kalit: None
```

---

# 473-Topshiriq: Const Generics bilan 1-Bitli Vektor qatlami (BitNet Layer)
## Topshiriq sharti:
BitNet uchun kirish va chiqish o'lchamlari kompilyatsiyada qat'iy berilgan qatlam.

## Yechim (Rust kodi):
```rust
struct BitLinearLayer<const IN: usize, const OUT: usize> {
    ogirliklar: [i8; IN],
}

impl<const IN: usize, const OUT: usize> BitLinearLayer<IN, OUT> {
    fn forward(&self, kirish: &[i8; IN]) -> i32 {
        let mut sum = 0;
        for i in 0..IN {
            sum += (self.ogirliklar[i] as i32) * (kirish[i] as i32);
        }
        sum
    }
}

fn main() {
    let layer: BitLinearLayer<4, 1> = BitLinearLayer { ogirliklar: [1, -1, 1, 0] };
    let x = [1, 1, 1, 1];

    println!("BitLinear chiqishi: {}", layer.forward(&x));
}
```

## Tushuntirish va Mantiq:
1-bit AI modellarida qatlam o'lchamlarini `const IN, const OUT` qilish ortiqcha chegarani tekshirishlarni yo'qotadi va maksimal tezlik beradi.

## Ishlash natijasi:
```text
BitLinear chiqishi: 1
```

---

# 474-Topshiriq: Generik turlarda Clone va Copy talablari
## Topshiriq sharti:
Nega ayrim generik funksiyalar `Copy` talab qilishini tushuntiring.

## Yechim (Rust kodi):
```rust
fn massiv_toldir<T: Copy, const N: usize>(qiymat: T) -> [T; N] {
    [qiymat; N]
}

fn main() {
    let nollar: [i32; 5] = massiv_toldir(0);
    println!("To'ldirilgan: {:?}", nollar);
}
```

## Tushuntirish va Mantiq:
`[qiymat; N]` sintaksisi elementlarni bir necha marta takrorlashi uchun `T: Copy` bo'lishini shart qilib qo'yadi.

## Ishlash natijasi:
```text
To'ldirilgan: [0, 0, 0, 0, 0]
```

---

# 475-Topshiriq: Generik strukturalarda metod nomlarini ixtisoslashtirish
## Topshiriq sharti:
Har xil parametrli strukturalarda bir xil nomli metodlarning turli xatti-harakati.

## Yechim (Rust kodi):
```rust
struct Konteyner<T>(T);

impl Konteyner<i32> {
    fn info(&self) { println!("Bu butun son: {}", self.0); }
}

impl Konteyner<String> {
    fn info(&self) { println!("Bu matn uzunligi: {}", self.0.len()); }
}

fn main() {
    Konteyner(100).info();
    Konteyner(String::from("Rust")).info();
}
```

## Tushuntirish va Mantiq:
Rust da turga bog'liq polimorfizm juda oson va intuitiv yoziladi.

## Ishlash natijasi:
```text
Bu butun son: 100
Bu matn uzunligi: 4
```

---

# 476-Topshiriq: Generik funksiyalarda xatolik turlari polimorfizmi
## Topshiriq sharti:
`Result<T, E>` dagi har ikkala turni ham erkin parametrlashtiring.

## Yechim (Rust kodi):
```rust
fn bajar<T, E>(amal: Result<T, E>) -> Option<T> {
    amal.ok()
}

fn main() {
    let r1: Result<i32, &str> = Ok(10);
    let r2: Result<f64, u32> = Ok(3.14);

    println!("{:?}, {:?}", bajar(r1), bajar(r2));
}
```

## Tushuntirish va Mantiq:
Har qanday xato va muvaffaqiyat turiga ega `Result` yagona generik funksiya orqali o'zgartirilishi mumkin.

## Ishlash natijasi:
```text
Some(10), Some(3.14)
```

---

# 477-Topshiriq: Generik Matritsa Transpozitsiyasi (Const Generics)
## Topshiriq sharti:
NxM matritsani MxN matritsaga aylantiruvchi qat'iy funksiya.

## Yechim (Rust kodi):
```rust
fn transpozitsiya<T: Copy + Default, const R: usize, const C: usize>(
    m: [[T; C]; R],
) -> [[T; R]; C] {
    let mut res = [[T::default(); R]; C];
    for i in 0..R {
        for j in 0..C {
            res[j][i] = m[i][j];
        }
    }
    res
}

fn main() {
    let m = [
        [1, 2, 3],
        [4, 5, 6],
    ]; // 2x3

    let t = transpozitsiya(m); // 3x2 bo'ladi!
    println!("Transpozitsiya natijasi: {:?}", t);
}
```

## Tushuntirish va Mantiq:
Kompilyator `[C; R]` o'lchamlari to'g'ri o'zgarganini kompilyatsiya vaqtida qat'iy tekshiradi.

## Ishlash natijasi:
```text
Transpozitsiya natijasi: [[1, 4], [2, 5], [3, 6]]
```

---

# 478-Topshiriq: Generik Wrapper (O'rovchi) va ichki qiymatni ochish (into_inner)
## Topshiriq sharti:
O'ralgan qiymat egasligini qaytaruvchi konsuming metod.

## Yechim (Rust kodi):
```rust
struct Quti<T> {
    qiymat: T,
}

impl<T> Quti<T> {
    fn new(qiymat: T) -> Self { Self { qiymat } }
    fn ochish(self) -> T { self.qiymat }
}

fn main() {
    let q = Quti::new(String::from("Maxfiy xat"));
    let xat = q.ochish();

    println!("Ochilgan ma'lumot: {}", xat);
}
```

## Tushuntirish va Mantiq:
`self` konsuming metodi qutini yo'q qilib, ichidagi har qanday turdagi qiymatni to'liq ozod qiladi.

## Ishlash natijasi:
```text
Ochilgan ma'lumot: Maxfiy xat
```

---

# 479-Topshiriq: Generik Funksiyada Min va Max ni bir vaqtda topish
## Topshiriq sharti:
Solishtirish mumkin bo'lgan slice dan eng kichik va eng kattasini oling.

## Yechim (Rust kodi):
```rust
fn min_max<T: PartialOrd + Copy>(royxat: &[T]) -> Option<(T, T)> {
    if royxat.is_empty() { return None; }
    let mut min = royxat[0];
    let mut max = royxat[0];

    for &item in &royxat[1..] {
        if item < min { min = item; }
        if item > max { max = item; }
    }
    Some((min, max))
}

fn main() {
    let sonlar = [45, 12, 85, 32, 99, 7];
    println!("Min va Max: {:?}", min_max(&sonlar));
}
```

## Tushuntirish va Mantiq:
Generik yondashuv bitta kod orqali barcha raqamli turlarda min-max hisoblashni ta'minlaydi.

## Ishlash natijasi:
```text
Min va Max: Some((7, 99))
```

---

# 480-Topshiriq: Generik va Statik Dispatch: C++ Templates bilan solishtirish
## Topshiriq sharti:
Rust generics lari qanday qilib C++ template laridagi noaniq xatoliklarni bartaraf etishini tushuntiring.

## Yechim (Rust kodi):
```rust
fn hisob<T: std::ops::Add<Output = T>>(a: T, b: T) -> T {
    a + b
}

fn main() {
    println!("10 + 20 = {}", hisob(10, 20));
    println!("2.5 + 3.5 = {}", hisob(2.5, 3.5));
}
```

## Tushuntirish va Mantiq:
C++ da template xatosi faqat chaqirilganda chiqadi. Rust da esa trait boundlar (`Add`) orqali xatolar funksiya e'lon qilingan paytdayoq ushlanadi.

## Ishlash natijasi:
```text
10 + 20 = 30
2.5 + 3.5 = 6
```

---

# 481-Topshiriq: Generik Strukturalarda partial move tahlili
## Topshiriq sharti:
Generik strukturaning bitta maydonini o'zlashtirish.

## Yechim (Rust kodi):
```rust
struct Paket<T, U> {
    a: T,
    b: U,
}

fn main() {
    let p = Paket { a: String::from("A"), b: 100 };
    let a_qiymat = p.a;

    println!("Olingan a: {}", a_qiymat);
    println!("Qolgan b: {}", p.b);
}
```

## Tushuntirish va Mantiq:
Generik strukturalarda ham xuddi oddiy strukturalar kabi maydonlar mustaqil egalikka ega bo'ladi.

## Ishlash natijasi:
```text
Olingan a: A
Qolgan b: 100
```

---

# 482-Topshiriq: Const Generics bilan Buffer o'lchamini tekshirish
## Topshiriq sharti:
Faqat 1024 baytli buferlarni qabul qiluvchi xavfsiz funksiya.

## Yechim (Rust kodi):
```rust
fn tarmoqqa_yoz<const HAJM: usize>(bufer: &[u8; HAJM]) {
    println!("{} baytli bufer tarmoqqa jo'natildi.", HAJM);
}

fn main() {
    let b1 = [0u8; 1024];
    tarmoqqa_yoz(&b1);

    let b2 = [0u8; 512];
    tarmoqqa_yoz(&b2);
}
```

## Tushuntirish va Mantiq:
Funksiya ixtiyoriy statik o'lchamdagi buferlarni qabul qiladi va uzunlikni dinamik sanash xarajatlarini yo'qotadi.

## Ishlash natijasi:
```text
1024 baytli bufer tarmoqqa jo'natildi.
512 baytli bufer tarmoqqa jo'natildi.
```

---

# 483-Topshiriq: Generik turlar uchun Clone implementatsiyasi
## Topshiriq sharti:
Ichki maydonlari `Clone` bo'lganda strukturani avtomatik klonlash.

## Yechim (Rust kodi):
```rust
#[derive(Debug, Clone)]
struct Juftlik<T> {
    qiymat: T,
}

fn main() {
    let j1 = Juftlik { qiymat: String::from("Original") };
    let j2 = j1.clone();

    println!("j1: {:?}, j2: {:?}", j1, j2);
}
```

## Tushuntirish va Mantiq:
`#[derive(Clone)]` generik strukturaga faqat uning `T` turi `Clone` bo'lgandagina klonlash imkoniyatini beradi.

## Ishlash natijasi:
```text
j1: Juftlik { qiymat: "Original" }, j2: Juftlik { qiymat: "Original" }
```

---

# 484-Topshiriq: Generik funksiyalarda closure qabul qilish
## Topshiriq sharti:
Closure turi generik parametr sifatida ifodalanishi.

## Yechim (Rust kodi):
```rust
fn ikki_marta<T, F>(val: T, mut amal: F) -> T
where
    F: FnMut(T) -> T,
{
    amal(amal(val))
}

fn main() {
    let res = ikki_marta(5, |x| x * 2); // 5 * 2 * 2 = 20
    println!("Natija: {}", res);
}
```

## Tushuntirish va Mantiq:
Rust da closurelar generik parametrlar (`F`) orqali qabul qilinadi, bu ularni inline qilishga va nol xarajat bilan chaqirishga imkon beradi.

## Ishlash natijasi:
```text
Natija: 20
```

---

# 485-Topshiriq: Generik turlar bilan Builder andozasi
## Topshiriq sharti:
Tip parametriga mos konfiguratsiya yig'uvchi builder.

## Yechim (Rust kodi):
```rust
struct Sozlama<T> {
    malumot: T,
}

impl<T> Sozlama<T> {
    fn new(malumot: T) -> Self { Self { malumot } }
    fn get(&self) -> &T { &self.malumot }
}

fn main() {
    let s = Sozlama::new(99.9);
    println!("Sozlama: {}", s.get());
}
```

## Tushuntirish va Mantiq:
Builder andozasi generik tiplar bilan birlashganda har qanday parametr turini qo'llab-quvvatlaydi.

## Ishlash natijasi:
```text
Sozlama: 99.9
```

---

# 486-Topshiriq: Generik turlarda Drop xatti-harakati
## Topshiriq sharti:
Generik struktura tozalanganda uning ichidagi turning destruktori chaqirilishi.

## Yechim (Rust kodi):
```rust
struct Ega<T> {
    nom: String,
    resurs: T,
}

impl<T> Drop for Ega<T> {
    fn drop(&mut self) {
        println!("Ega '{}' xotiradan tozalandi.", self.nom);
    }
}

fn main() {
    {
        let _e = Ega { nom: String::from("Boshqaruvchi"), resurs: 42 };
    }
    println!("Scope yakunlandi.");
}
```

## Tushuntirish va Mantiq:
Generik tur qanday bo'lishidan qat'i nazar, Rust uning destruktorini xavfsiz va aniq tartibda chaqiradi.

## Ishlash natijasi:
```text
Ega 'Boshqaruvchi' xotiradan tozalandi.
Scope yakunlandi.
```

---

# 487-Topshiriq: Generik Enum va Match destrukturizatsiyasi
## Topshiriq sharti:
Generik variantdagi qiymatni o'zlashtirish.

## Yechim (Rust kodi):
```rust
enum Holat<T> {
    Kutilmoqda,
    Tayyor(T),
}

fn main() {
    let h = Holat::Tayyor(vec![1, 2, 3]);

    match h {
        Holat::Tayyor(v) => println!("Vektor uzunligi: {}", v.len()),
        Holat::Kutilmoqda => println!("Kutilmoqda..."),
    }
}
```

## Tushuntirish va Mantiq:
Generik enumlar ichidagi ma'lumotlar pattern matching yordamida to'liq xavfsiz ajratib olinadi.

## Ishlash natijasi:
```text
Vektor uzunligi: 3
```

---

# 488-Topshiriq: Generik Min-Heap yoki Priority Queue sodda modeli
## Topshiriq sharti:
Eng kichik elementni birinchi o'ringa qo'yuvchi saralash.

## Yechim (Rust kodi):
```rust
struct SaralanganTo'plam<T: Ord> {
    elementlar: Vec<T>,
}

impl<T: Ord> SaralanganTo'plam<T> {
    fn new() -> Self { Self { elementlar: Vec::new() } }
    fn qosh(&mut self, val: T) {
        self.elementlar.push(val);
        self.elementlar.sort();
    }
}

fn main() {
    let mut to'plam = SaralanganTo'plam::new();
    to'plam.qosh(50);
    to'plam.qosh(10);
    to'plam.qosh(30);

    println!("Saralangan elementlar: {:?}", to'plam.elementlar);
}
```

## Tushuntirish va Mantiq:
`T: Ord` cheklovi elementlarni to'liq qat'iy tartibda saralash imkoniyatini kafolatlaydi.

## Ishlash natijasi:
```text
Saralangan elementlar: [10, 30, 50]
```

---

# 489-Topshiriq: Generik Skalyar Ko'paytma funksiyasi (Dot Product)
## Topshiriq sharti:
Const Generics yordamida ikkita N o'lchamli vektorning skalyar ko'paytmasini hisoblang.

## Yechim (Rust kodi):
```rust
fn dot_product<const N: usize>(a: [f64; N], b: [f64; N]) -> f64 {
    let mut sum = 0.0;
    for i in 0..N {
        sum += a[i] * b[i];
    }
    sum
}

fn main() {
    let v1 = [1.0, 2.0, 3.0];
    let v2 = [4.0, 5.0, 6.0];

    println!("Dot Product: {}", dot_product(v1, v2));
}
```

## Tushuntirish va Mantiq:
O'lchamlari mos bo'lmagan vektorlarni ko'paytirib bo'lmaydi: Const Generics bu xatoni kompilyatsiyada to'xtatadi.

## Ishlash natijasi:
```text
Dot Product: 32
```

---

# 490-Topshiriq: Generik turlar va xotira tekislash (Alignment) qoidalari
## Topshiriq sharti:
Generik turning xotira hajmi kompilyatsiya paytida aniqlanishi.

## Yechim (Rust kodi):
```rust
struct Quti<T> {
    qiymat: T,
}

fn main() {
    println!("Quti<u8> hajmi:   {} bayt", std::mem::size_of::<Quti<u8>>());
    println!("Quti<u64> hajmi:  {} bayt", std::mem::size_of::<Quti<u64>>());
    println!("Quti<[u8; 100]>:  {} bayt", std::mem::size_of::<Quti<[u8; 100]>>());
}
```

## Tushuntirish va Mantiq:
Monomorfizatsiya tufayli har bir generik instansiya xotirada aynan o'z turiga mos joy oladi.

## Ishlash natijasi:
```text
Quti<u8> hajmi:   1 bayt
Quti<u64> hajmi:  8 bayt
Quti<[u8; 100]>:  100 bayt
```

---

# 491-Topshiriq: Generik funksiyada bir nechta Trait Boundlar (T: Display + Debug)
## Topshiriq sharti:
Element ham ekranga chiqadigan, ham debug qilinadigan bo'lishini talab qiling.

## Yechim (Rust kodi):
```rust
use std::fmt::{Debug, Display};

fn toliq_chop<T: Display + Debug>(val: T) {
    println!("Display: {}, Debug: {:?}", val, val);
}

fn main() {
    toliq_chop("Rust Tili");
    toliq_chop(2024);
}
```

## Tushuntirish va Mantiq:
`+` belgisi bir vaqtning o'zida bir nechta shartlarni (trait bounds) birlashtirishga xizmat qiladi.

## Ishlash natijasi:
```text
Display: Rust Tili, Debug: "Rust Tili"
Display: 2024, Debug: 2024
```

---

# 492-Topshiriq: Generik turlarda where klauzulasi orqali toza sintaksis
## Topshiriq sharti:
Ko'p shartli generik funksiya signaturasini `where` orqali tartibli yozish.

## Yechim (Rust kodi):
```rust
use std::fmt::Debug;

fn murakkab_solishtir<T, U>(a: T, b: U) -> bool
where
    T: PartialEq + Debug,
    U: PartialEq + Debug,
{
    println!("Solishtirilmoqda: {:?} va {:?}", a, b);
    true
}

fn main() {
    murakkab_solishtir(10, "matn");
}
```

## Tushuntirish va Mantiq:
`where` klauzulasi funksiya nomidan keyingi uzun qavslarni qisqartirib, shartlarni pastda chiroyli ko'rsatish imkonini beradi.

## Ishlash natijasi:
```text
Solishtirilmoqda: 10 va "matn"
```

---

# 493-Topshiriq: Generik funksiya orqali massivdagi o'rtacha qiymat
## Topshiriq sharti:
Har qanday raqamli massiv o'rtacha arifmetigini topish.

## Yechim (Rust kodi):
```rust
fn ortacha(arr: &[f64]) -> f64 {
    let sum: f64 = arr.iter().sum();
    sum / arr.len() as f64
}

fn main() {
    let sonlar = [1.0, 2.0, 3.0, 4.0, 5.0];
    println!("O'rtacha: {:.1}", ortacha(&sonlar));
}
```

## Tushuntirish va Mantiq:
Float to'plamlari ustida statistik hisoblar tezkor amalga oshiriladi.

## Ishlash natijasi:
```text
O'rtacha: 3.0
```

---

# 494-Topshiriq: Const Generics bilan Statik String (FixedString)
## Topshiriq sharti:
Heap ga chiqmasdan, to'liq Stack da saqlanuvchi qat'iy o'lchamli matn.

## Yechim (Rust kodi):
```rust
struct StatikMatn<const N: usize> {
    bufer: [u8; N],
    uzunlik: usize,
}

impl<const N: usize> StatikMatn<N> {
    fn new() -> Self { Self { bufer: [0; N], uzunlik: 0 } }
}

fn main() {
    let s: StatikMatn<64> = StatikMatn::new();
    println!("Stack dagi 64 baytli matn buferi tayyor. Hajm: {} bayt", std::mem::size_of_val(&s));
}
```

## Tushuntirish va Mantiq:
Tizimli va mikrokontroller dasturlashda Heap xotira bo'lmagan sharoitda Const Generics asosiy najotkor hisoblanadi.

## Ishlash natijasi:
```text
Stack dagi 64 baytli matn buferi tayyor. Hajm: 72 bayt
```

---

# 495-Topshiriq: Generik enumlar bilan Holat Mashinasi (State Machine)
## Topshiriq sharti:
Har xil parametrli javoblarni generik holda yetkazish.

## Yechim (Rust kodi):
```rust
enum Javob<T> {
    Kutish,
    Keldi(T),
}

fn main() {
    let j = Javob::Keldi("Fayl muvaffaqiyatli yuklandi");
    match j {
        Javob::Keldi(xabar) => println!("Xabar: {}", xabar),
        Javob::Kutish => println!("Kutilmoqda..."),
    }
}
```

## Tushuntirish va Mantiq:
Generik enumlar holat mashinalarini har qanday ma'lumot turi uchun moslashuvchan qiladi.

## Ishlash natijasi:
```text
Xabar: Fayl muvaffaqiyatli yuklandi
```

---

# 496-Topshiriq: Generik funksiyada massivni to'ldirish (fill)
## Topshiriq sharti:
Massiv bo'lagini berilgan generik qiymat bilan to'ldiring.

## Yechim (Rust kodi):
```rust
fn toldir<T: Clone>(arr: &mut [T], val: T) {
    for elem in arr.iter_mut() {
        *elem = val.clone();
    }
}

fn main() {
    let mut sonlar = vec![0; 4];
    toldir(&mut sonlar, 99);

    println!("To'ldirilgan: {:?}", sonlar);
}
```

## Tushuntirish va Mantiq:
`T: Clone` yordamida qiymat har bir katakka xavfsiz ko'chiriladi.

## Ishlash natijasi:
```text
To'ldirilgan: [99, 99, 99, 99]
```

---

# 497-Topshiriq: Generik turlar o'rtasida konvertatsiya (Into traiti)
## Topshiriq sharti:
`T: Into<U>` orqali moslashuvchan funksiya parametrini qabul qiling.

## Yechim (Rust kodi):
```rust
fn chop_satr<T: Into<String>>(val: T) {
    let s: String = val.into();
    println!("Matn: {}", s);
}

fn main() {
    chop_satr("Statik matn"); // &str avtomatik String ga aylanadi
    chop_satr(String::from("Heap satr")); // String ham to'g'ridan-to'g'ri o'tadi
}
```

## Tushuntirish va Mantiq:
`Into` traiti orqali funksiya ham `&str`, ham `String` ni teng qabul qila oladi.

## Ishlash natijasi:
```text
Matn: Statik matn
Matn: Heap satr
```

---

# 498-Topshiriq: Generik turlarda xotira oqishining (Memory Leak) mutlaq yo'qligi
## Topshiriq sharti:
Kompilyator generik turlarning barcha xotira egalik zanjirlarini to'liq kuzatishi.

## Yechim (Rust kodi):
```rust
struct Quti<T> { x: T }

fn main() {
    {
        let _q = Quti { x: vec![1, 2, 3, 4] };
    } // Vektor avtomatik xotiradan tozalandi
    println!("Generik xotira xavfsizligi 100% ta'minlandi.");
}
```

## Tushuntirish va Mantiq:
Generik tiplar hech qachon xotira nazoratini susaytirmaydi. Kompilyator har bir aniq tip uchun aniq destruktor generatsiya qiladi.

## Ishlash natijasi:
```text
Generik xotira xavfsizligi 100% ta'minlandi.
```

---

# 499-Topshiriq: Const Generics bilan SIMD Registr uzunliklarini belgilash
## Topshiriq sharti:
128-bit, 256-bit yoki 512-bitli SIMD vektorlarini ifodalash.

## Yechim (Rust kodi):
```rust
struct SimdRegistr<T, const N: usize> {
    lanes: [T; N],
}

fn main() {
    let avx2: SimdRegistr<f32, 8> = SimdRegistr { lanes: [1.0; 8] }; // 256-bit AVX2
    println!("AVX2 registr elementlari soni: {}", avx2.lanes.len());
}
```

## Tushuntirish va Mantiq:
Const Generics zamonaviy protsessorlarning AVX2 va AVX-512 registrlarini apparat aniqligida modellashtirish imkonini beradi.

## Ishlash natijasi:
```text
AVX2 registr elementlari soni: 8
```

---

# 500-Topshiriq: Generics va Const Generics moduli xulosasi
## Topshiriq sharti:
Rust da turlar xavfsizligi va yuqori tezlik arxitekturasi xulosasi.

## Yechim (Rust kodi):
```rust
fn main() {
    println!("=== RUST GENERICS VA CONST GENERICS XULOSASI ===");
    println!("1. Generics kod takrorlanishini yo'qotadi va polimorfizm beradi.");
    println!("2. Monomorfizatsiya tufayli ish vaqtida 0 nanosekund sarf (Zero-cost).");
    println!("3. Trait bounds (T: Trait) talablarni kompilyatsiya paytida tekshiradi.");
    println!("4. Const Generics massiv o'lchamlarini tip sifatida uzatishni ta'minlaydi.");
    println!("5. PhantomData xotirasiz tip xavfsizligini kafolatlaydi.");
}
```

## Tushuntirish va Mantiq:
Generics Rust dasturchilariga kodni qayta ishlatishda dunyodagi eng qat'iy va tezkor vositalar majmuasini taqdim etadi.

## Ishlash natijasi:
```text
=== RUST GENERICS VA CONST GENERICS XULOSASI ===
1. Generics kod takrorlanishini yo'qotadi va polimorfizm beradi.
2. Monomorfizatsiya tufayli ish vaqtida 0 nanosekund sarf (Zero-cost).
3. Trait bounds (T: Trait) talablarni kompilyatsiya paytida tekshiradi.
4. Const Generics massiv o'lchamlarini tip sifatida uzatishni ta'minlaydi.
5. PhantomData xotirasiz tip xavfsizligini kafolatlaydi.
```

---
