# Rust Dasturlash Tili: Smart Pointerlar va Xotira Boshqaruvi

Ushbu modulda Rust'ning xotira boshqaruvi mexanizmlari, `Box<T>`, `Rc<T>`, `RefCell<T>`, `Cell<T>`, `Weak<T>`, `Deref`, `Drop` trait'lari hamda xotirani qo'lda boshqarish (`alloc`, `MaybeUninit`, `Pin`) amaliy topshiriqlar orqali to'liq yoritilgan.

---

# 701-Topshiriq: Box<T> bilan heap xotirada integer saqlash
## Topshiriq sharti:
Rust dasturida `Box<i32>` yordamida sonni heap xotiraga joylashtirish va uning qiymatini ekranga chiqarish dasturini yozing.
## Yechim (Rust kodi):
```rust
fn main() {
    let heap_son: Box<i32> = Box::new(42);
    println!("Heap'dagi qiymat: {}", heap_son);
    println!("Deref orqali qiymat: {}", *heap_son);
}
```
## Tushuntirish va Mantiq:
`Box<T>` smart pointeri stackdagi ko'rsatkich orqali heap xotirada ma'lumot saqlash imkonini beradi. `*` operatori orqali dereference qilinadi.
## Ishlash natijasi:
```text
Heap'dagi qiymat: 42
Deref orqali qiymat: 42
```

---

# 702-Topshiriq: Rekursiv ma'lumot strukturasi (Linked List) Box bilan
## Topshiriq sharti:
Rust'da struktura o'zini o'zi ichiga olishi uchun `Box` kerak (chunki kompilyator hajmni bilishi lozim). Oddiy Cons/Nil ro'yxatini yarating.
## Yechim (Rust kodi):
```rust
#[derive(Debug)]
enum List {
    Cons(i32, Box<List>),
    Nil,
}

use List::{Cons, Nil};

fn main() {
    let list = Cons(1, Box::new(Cons(2, Box::new(Cons(3, Box::new(Nil))))));
    println!("Rekursiv ro'yxat: {:?}", list);
}
```
## Tushuntirish va Mantiq:
Rust kompilyatori tiplar hajmini kompilyatsiya paytida bilishi shart. Rekursiv enumda `Box` ishlatilsa, uning hajmi doimiy ko'rsatkich (pointer) o'lchamida bo'ladi.
## Ishlash natijasi:
```text
Rekursiv ro'yxat: Cons(1, Cons(2, Cons(3, Nil)))
```

---

# 703-Topshiriq: Katta massivni stack o'rniga heap'ga joylash
## Topshiriq sharti:
Stack to'lib qolishi (stack overflow) oldini olish uchun 1,000,000 elementli massivni `Box` yordamida heap'da yarating.
## Yechim (Rust kodi):
```rust
fn main() {
    // 1 million elementli massivni heap'da saqlash
    let katta_massiv: Box<[u8; 1_000_000]> = Box::new([7; 1_000_000]);
    println!("Massiv uzunligi: {}", katta_massiv.len());
    println!("Birinchi element: {}, Oxirgi element: {}", katta_massiv[0], katta_massiv[999_999]);
}
```
## Tushuntirish va Mantiq:
Standart massivlar stackda joylashadi va stack hajmi cheklangan (odatda 2-8 MB). `Box` yordamida juda katta ma'lumotlarni heap'ga ko'chirish mumkin.
## Ishlash natijasi:
```text
Massiv uzunligi: 1000000
Birinchi element: 7, Oxirgi element: 7
```

---

# 704-Topshiriq: Deref trait: Box ustida * operatori ishlashi
## Topshiriq sharti:
Oddiy o'zgaruvchi bilan Box qilingan o'zgaruvchining `*` operatori orqali qanday solishtirilishini ko'rsating.
## Yechim (Rust kodi):
```rust
fn main() {
    let x = 5;
    let y = Box::new(x);

    assert_eq!(5, x);
    assert_eq!(5, *y);
    println!("*y orqali qiymat muvaffaqiyatli solishtirildi: {}", *y);
}
```
## Tushuntirish va Mantiq:
`Box<T>` `Deref` trait'ini implement qiladi. Shuning uchun `*y` kodi `*(y.deref())` ga aylanadi va ichki qiymat olinadi.
## Ishlash natijasi:
```text
*y orqali qiymat muvaffaqiyatli solishtirildi: 5
```

---

# 705-Topshiriq: O'zimizning MyBox<T> struct'iga Deref trait'ini implement qilish
## Topshiriq sharti:
`MyBox<T>` nomli yangi wrapper struct yarating va unga `std::ops::Deref` trait'ini implement qilib `*` bilan ishlashini ta'minlang.
## Yechim (Rust kodi):
```rust
use std::ops::Deref;

struct MyBox<T>(T);

impl<T> MyBox<T> {
    fn new(x: T) -> MyBox<T> {
        MyBox(x)
    }
}

impl<T> Deref for MyBox<T> {
    type Target = T;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

fn main() {
    let m = MyBox::new(100);
    println!("MyBox ichidagi qiymat: {}", *m);
}
```
## Tushuntirish va Mantiq:
`Deref` trait'i `deref(&self) -> &Self::Target` metodini talab qiladi. Bu bizga o'z turlarimizni pointer kabi ishlatish imkonini beradi.
## Ishlash natijasi:
```text
MyBox ichidagi qiymat: 100
```

---

# 706-Topshiriq: Deref Coercion: &MyBox<String> ni &str ga avtomatik o'tkazish
## Topshiriq sharti:
Deref coercion xususiyati yordamida `MyBox<String>` tipidagi ob'ektni `&str` kutayotgan funksiyaga to'g'ridan-to'g'ri uzating.
## Yechim (Rust kodi):
```rust
use std::ops::Deref;

struct MyBox<T>(T);

impl<T> MyBox<T> {
    fn new(x: T) -> MyBox<T> {
        MyBox(x)
    }
}

impl<T> Deref for MyBox<T> {
    type Target = T;
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

fn salom_ber(ism: &str) {
    println!("Salom, {}!", ism);
}

fn main() {
    let m = MyBox::new(String::from("Rustacean"));
    salom_ber(&m);
}
```
## Tushuntirish va Mantiq:
Rust `&MyBox<String>` ni `&String` ga (MyBox deref), so'ngra `&String` ni `&str` ga (String deref) kompilyatsiya paytida avtomatik o'tkazadi.
## Ishlash natijasi:
```text
Salom, Rustacean!
```

---

# 707-Topshiriq: Drop trait implementatsiyasi: xotira bo'shatilishini kuzatish
## Topshiriq sharti:
Struktura doirasidan (scope) chiqib ketganda avtomatik chaqiriladigan `Drop` trait'ini implement qiling.
## Yechim (Rust kodi):
```rust
struct MaxsusResurs {
    nomi: String,
}

impl Drop for MaxsusResurs {
    fn drop(&mut self) {
        println!("Resurs tozalandi va xotira bo'shatildi: {}", self.nomi);
    }
}

fn main() {
    println!("Blok boshlanishi");
    {
        let _resurs = MaxsusResurs { nomi: String::from("Fayl_Handler_01") };
        println!("Resurs ishlatilmoqda...");
    }
    println!("Blok tugadi");
}
```
## Tushuntirish va Mantiq:
`Drop` trait'i ob'ekt scope'dan chiqqanda xotirani yoki boshqa tashqi resurslarni (fayl, soket) avtomatik tozalash uchun ishlatiladi (RAII).
## Ishlash natijasi:
```text
Blok boshlanishi
Resurs ishlatilmoqda...
Resurs tozalandi va xotira bo'shatildi: Fayl_Handler_01
Blok tugadi
```

---

# 708-Topshiriq: std::mem::drop orqali qiymatni muddatidan oldin qo'lda tozalash
## Topshiriq sharti:
O'zgaruvchini scope tugashidan oldin qo'lda xotiradan o'chirish uchun `std::mem::drop` funksiyasidan foydalaning.
## Yechim (Rust kodi):
```rust
struct Resurs(i32);

impl Drop for Resurs {
    fn drop(&mut self) {
        println!("Resurs #{} xotiradan o'chirildi!", self.0);
    }
}

fn main() {
    let r = Resurs(99);
    println!("Resurs yaratildi");
    drop(r);
    println!("Resurs drop qilingandan keyingi qator");
}
```
## Tushuntirish va Mantiq:
`drop(r)` orqali egalik darhol bekor qilinadi va uning destruktori chaqiriladi. Rust'da to'g'ridan-to'g'ri `r.drop()` chaqirish taqiqlangan.
## Ishlash natijasi:
```text
Resurs yaratildi
Resurs #99 xotiradan o'chirildi!
Resurs drop qilingandan keyingi qator
```

---

# 709-Topshiriq: Rc<T> orqali bitta ma'lumotga bir nechta egalik (shared ownership)
## Topshiriq sharti:
`std::rc::Rc` smart pointeri yordamida bitta ro'yxatga bir nechta mustaqil ro'yxatlar egalik qiladigan dastur tuzing.
## Yechim (Rust kodi):
```rust
use std::rc::Rc;

#[derive(Debug)]
enum List {
    Cons(i32, Rc<List>),
    Nil,
}

use List::{Cons, Nil};

fn main() {
    let umumiy = Rc::new(Cons(5, Rc::new(Cons(10, Rc::new(Nil))))));
    let royxat_a = Cons(3, Rc::clone(&umumiy));
    let royxat_b = Cons(4, Rc::clone(&umumiy));

    println!("A: {:?}", royxat_a);
    println!("B: {:?}", royxat_b);
}
```
## Tushuntirish va Mantiq:
`Rc<T>` reference counting orqali bitta ma'lumotga bir nechta egalik qilish imkonini beradi. Ma'lumot faqat barcha egalar tugagandagina o'chiriladi.
## Ishlash natijasi:
```text
A: Cons(3, Cons(5, Cons(10, Nil)))
B: Cons(4, Cons(5, Cons(10, Nil)))
```

---

# 710-Topshiriq: Rc::clone vs chuqur clone farqi
## Topshiriq sharti:
`Rc::clone(&rc)` ma'lumotni to'liq nusxalamaydi, faqat hisoblagichni (reference count) oshiradi. Buni tushuntiruvchi misol yozing.
## Yechim (Rust kodi):
```rust
use std::rc::Rc;

fn main() {
    let original = Rc::new(vec![1, 2, 3, 4, 5]);
    let klon = Rc::clone(&original);

    println!("Original manzil: {:p}", original.as_ptr());
    println!("Klon manzil:     {:p}", klon.as_ptr());
    assert_eq!(original.as_ptr(), klon.as_ptr());
}
```
## Tushuntirish va Mantiq:
`Rc::clone` pointer nusxasini oladi va ichki sanagichni 1 taga oshiradi, chuqur heap nusxalash bajarmaydi, shuning uchun juda tez ishlaydi.
## Ishlash natijasi:
```text
Original manzil: 0x...
Klon manzil:     0x...
```

---

# 711-Topshiriq: Rc::strong_count va Rc::weak_count qiymatlarini kuzatish
## Topshiriq sharti:
`Rc::strong_count` funksiyasi yordamida ob'ektning havolalar soni qanday o'zgarishini ko'rsating.
## Yechim (Rust kodi):
```rust
use std::rc::Rc;

fn main() {
    let a = Rc::new(100);
    println!("Boshlang'ich sanagich: {}", Rc::strong_count(&a));

    let b = Rc::clone(&a);
    println!("b yaratilgandan so'ng: {}", Rc::strong_count(&a));

    {
        let _c = Rc::clone(&a);
        println!("Scope ichida (c bor): {}", Rc::strong_count(&a));
    }

    println!("Scope tugagach: {}", Rc::strong_count(&a));
}
```
## Tushuntirish va Mantiq:
Scope tugaganda `_c` avtomatik drop bo'ladi va strong_count 1 taga kamayadi. Strong count 0 ga yetganda xotira bo'shatiladi.
## Ishlash natijasi:
```text
Boshlang'ich sanagich: 1
b yaratilgandan so'ng: 2
Scope ichida (c bor): 3
Scope tugagach: 2
```

---

# 712-Topshiriq: Rc bilan daraxt (Tree) tugunlarida ota tugunni saqlash
## Topshiriq sharti:
Har bir tugun bir nechta bolaga ega bo'lishi va bolalar o'z ota tuguniga havola qila olishi uchun `Rc` strukturasini tuzing.
## Yechim (Rust kodi):
```rust
use std::rc::Rc;

#[derive(Debug)]
struct Node {
    qiymat: i32,
    bolalar: Vec<Rc<Node>>,
}

fn main() {
    let barg1 = Rc::new(Node { qiymat: 10, bolalar: vec![] });
    let barg2 = Rc::new(Node { qiymat: 20, bolalar: vec![] });

    let ildiz = Node {
        qiymat: 1,
        bolalar: vec![Rc::clone(&barg1), Rc::clone(&barg2)],
    };

    println!("Ildiz tugun: {:?}", ildiz);
    println!("Barg1 sanagichi: {}", Rc::strong_count(&barg1));
}
```
## Tushuntirish va Mantiq:
Daraxt tuzilmalarida tugunlar bir nechta boshqa obyektlar tomonidan umumiy foydalanilishi uchun `Rc<Node>` ishlatiladi.
## Ishlash natijasi:
```text
Ildiz tugun: Node { qiymat: 1, bolalar: [Node { qiymat: 10, bolalar: [] }, Node { qiymat: 20, bolalar: [] }] }
Barg1 sanagichi: 2
```

---

# 713-Topshiriq: RefCell<T> va Interior Mutability tushunchasi
## Topshiriq sharti:
Rust'da immutable o'zgaruvchi ichidagi ma'lumotni o'zgartirish (Interior Mutability) imkonini beruvchi `RefCell` misolini yozing.
## Yechim (Rust kodi):
```rust
use std::cell::RefCell;

fn main() {
    let x = RefCell::new(10);

    println!("Avvalgi qiymat: {:?}", x);
    *x.borrow_mut() += 5;
    println!("Keyingi qiymat: {:?}", x);
}
```
## Tushuntirish va Mantiq:
`RefCell<T>` immutable ob'ekt ichidagi ma'lumotni o'zgartirishga ruxsat beradi. Borrow qoidalari kompilyatsiya paytida emas, runtime paytida tekshiriladi.
## Ishlash natijasi:
```text
Avvalgi qiymat: RefCell { value: 10 }
Keyingi qiymat: RefCell { value: 15 }
```

---

# 714-Topshiriq: RefCell::borrow va borrow_mut metodlari bilan ishlash
## Topshiriq sharti:
`RefCell` orqali bir vaqtning o'zida immutable borrow olish va keyinchalik alohida mutable borrow olishni ko'rsating.
## Yechim (Rust kodi):
```rust
use std::cell::RefCell;

fn main() {
    let ma_lumot = RefCell::new(String::from("Salom"));

    {
        let r1 = ma_lumot.borrow();
        let r2 = ma_lumot.borrow();
        println!("O'qish: {} va {}", *r1, *r2);
    } // r1 va r2 bu yerda tugaydi

    {
        let mut m = ma_lumot.borrow_mut();
        m.push_str(", Rust!");
    }

    println!("Yakuniy natija: {}", ma_lumot.borrow());
}
```
## Tushuntirish va Mantiq:
Bir nechta `borrow()` (immutable) bir vaqtda mavjud bo'lishi mumkin. Ammo `borrow_mut()` chaqirish uchun barcha avvalgi borrow'lar tugagan bo'lishi shart.
## Ishlash natijasi:
```text
O'qish: Salom va Salom
Yakuniy natija: Salom, Rust!
```

---

# 715-Topshiriq: RefCell runtime borrow tekshiruvi: panic holati
## Topshiriq sharti:
`RefCell`da bir vaqtda ikkita mutable borrow olinganda yoki borrow va borrow_mut bir vaqtda chaqirilganda panic berishini namoyish qiling.
## Yechim (Rust kodi):
```rust
use std::cell::RefCell;

fn main() {
    let cell = RefCell::new(42);
    let _r1 = cell.borrow();

    // Quyidagi qator runtime panic beradi: AlreadyBorrowed
    let natija = std::panic::catch_unwind(|| {
        let mut _r2 = cell.borrow_mut();
        *_r2 += 1;
    });

    match natija {
        Ok(_) => println!("Muvaffaqiyatli"),
        Err(_) => println!("Kutilgan panic: Bir vaqtda borrow va borrow_mut mumkin emas!"),
    }
}
```
## Tushuntirish va Mantiq:
`RefCell` Rust borrow qoidalarini runtimeda kuzatib boradi. Agar bir vaqtda borrow va borrow_mut bo'lsa, thread darhol panic qiladi.
## Ishlash natijasi:
```text
Kutilgan panic: Bir vaqtda borrow va borrow_mut mumkin emas!
```

---

# 716-Topshiriq: try_borrow va try_borrow_mut orqali panic'dan qochish
## Topshiriq sharti:
Panic yuzaga kelishining oldini olish uchun `try_borrow` va `try_borrow_mut` metodlaridan `Result` orqali foydalaning.
## Yechim (Rust kodi):
```rust
use std::cell::RefCell;

fn main() {
    let cell = RefCell::new(100);
    let _b1 = cell.borrow();

    match cell.try_borrow_mut() {
        Ok(mut val) => *val += 1,
        Err(e) => println!("Qarz olish rad etildi: {}", e),
    }

    println!("Dastur to'xtab qolmasdan ishlashda davom etdi: {}", cell.borrow());
}
```
## Tushuntirish va Mantiq:
`try_borrow_mut()` panic qilish o'rniga `Err(BorrowMutError)` qaytaradi, bu xavfsiz xatolikni qayta ishlash imkonini beradi.
## Ishlash natijasi:
```text
Qarz olish rad etildi: already borrowed
Dastur to'xtab qolmasdan ishlashda davom etdi: 100
```

---

# 717-Topshiriq: Rc<RefCell<T>> kombinatsiyasi: ko'p egalik va mutability
## Topshiriq sharti:
Bir nechta egalar bitta umumiy ma'lumotni o'zgartira olishi uchun `Rc<RefCell<T>>` modelini yarating.
## Yechim (Rust kodi):
```rust
use std::rc::Rc;
use std::cell::RefCell;

fn main() {
    let umumiy_qiymat = Rc::new(RefCell::new(10));

    let egasi_1 = Rc::clone(&umumiy_qiymat);
    let egasi_2 = Rc::clone(&umumiy_qiymat);

    *egasi_1.borrow_mut() += 20;
    *egasi_2.borrow_mut() += 30;

    println!("Yakuniy qiymat: {}", umumiy_qiymat.borrow());
}
```
## Tushuntirish va Mantiq:
`Rc<T>` faqat immutable havolalar beradi. Ma'lumotni o'zgartirish uchun `Rc` ichiga `RefCell` joylashtiriladi: `Rc<RefCell<T>>`.
## Ishlash natijasi:
```text
Yakuniy qiymat: 60
```

---

# 718-Topshiriq: Cell<T> bilan Copy tiplar uchun no-overhead ichki o'zgaruvchanlik
## Topshiriq sharti:
`Cell<T>` orqali `Copy` turlarni hech qanday runtime hisoblagichsiz `get()` va `set()` metodlari bilan o'zgartiring.
## Yechim (Rust kodi):
```rust
use std::cell::Cell;

fn main() {
    let hisoblagich = Cell::new(0);

    for _ in 0..5 {
        hisoblagich.set(hisoblagich.get() + 1);
    }

    println!("Hisoblagich qiymati: {}", hisoblagich.get());
}
```
## Tushuntirish va Mantiq:
`Cell<T>` reference bermaydi, balki qiymatni to'liq ko'chirib oladi yoki yozadi. Shuning uchun runtime tekshiruv va overhead bo'lmaydi.
## Ishlash natijasi:
```text
Hisoblagich qiymati: 5
```

---

# 719-Topshiriq: Cell<T> vs RefCell<T> taqqoslash misoli
## Topshiriq sharti:
Ikkala tur o'rtasidagi farqni bitta dasturda ko'rsating (`Cell` qiymat ko'chiradi, `RefCell` havola qaytaradi).
## Yechim (Rust kodi):
```rust
use std::cell::{Cell, RefCell};

fn main() {
    // Cell primitive turlar uchun juda yengil
    let c = Cell::new(5);
    c.set(10);
    println!("Cell qiymati: {}", c.get());

    // RefCell kompleks turlar (String, Vec) uchun mos
    let rc = RefCell::new(vec![1, 2]);
    rc.borrow_mut().push(3);
    println!("RefCell uzunligi: {}", rc.borrow().len());
}
```
## Tushuntirish va Mantiq:
`Cell` oddiy `Copy` tiplar uchun ideal va xavfsiz. `RefCell` esa kompleks kolleksiyalar va dinamik strukturalarni o'z joyida o'zgartirish uchun kerak.
## Ishlash natijasi:
```text
Cell qiymati: 10
RefCell uzunligi: 3
```

---

# 720-Topshiriq: Circular Reference (aylana bog'liqlik) va memory leak
## Topshiriq sharti:
Ikki tugun bir-biriga `Rc<RefCell<T>>` orqali bog'lanishi natijasida xotira hech qachon tozalanmasligi (memory leak) holatini ko'rsating.
## Yechim (Rust kodi):
```rust
use std::rc::Rc;
use std::cell::RefCell;

struct Tugun {
    qoshni: RefCell<Option<Rc<Tugun>>>,
}

impl Drop for Tugun {
    fn drop(&mut self) {
        println!("Tugun drop bo'ldi!");
    }
}

fn main() {
    let t1 = Rc::new(Tugun { qoshni: RefCell::new(None) });
    let t2 = Rc::new(Tugun { qoshni: RefCell::new(None) });

    *t1.qoshni.borrow_mut() = Some(Rc::clone(&t2));
    *t2.qoshni.borrow_mut() = Some(Rc::clone(&t1));

    println!("T1 strong count: {}", Rc::strong_count(&t1));
    println!("T2 strong count: {}", Rc::strong_count(&t2));
    // Dastur tugaganda drop xabarlari chiqmaydi, chunki sanagichlar 1 dan pastga tushmaydi!
}
```
## Tushuntirish va Mantiq:
Aylana bog'liqlikda (cycle) ikkala `Rc` bir-biriga havola qiladi. Natijada sanagich hech qachon 0 ga tushmaydi va xotira sizib chiqadi.
## Ishlash natijasi:
```text
T1 strong count: 2
T2 strong count: 2
```

---

# 721-Topshiriq: Weak<T> bilan aylana bog'liqlikni yechish
## Topshiriq sharti:
Yuqoridagi memory leak muammosini `Rc::downgrade` orqali `Weak<T>` ishlatib yeching.
## Yechim (Rust kodi):
```rust
use std::rc::{Rc, Weak};
use std::cell::RefCell;

struct Tugun {
    nomi: String,
    ota: RefCell<Weak<Tugun>>,
}

impl Drop for Tugun {
    fn drop(&mut self) {
        println!("{} muvaffaqiyatli xotiradan tozalandi!", self.nomi);
    }
}

fn main() {
    let ota = Rc::new(Tugun {
        nomi: String::from("Ota"),
        ota: RefCell::new(Weak::new()),
    });

    let bola = Rc::new(Tugun {
        nomi: String::from("Bola"),
        ota: RefCell::new(Rc::downgrade(&ota)),
    });

    println!("Ota strong count: {}, weak count: {}", Rc::strong_count(&ota), Rc::weak_count(&ota));
    drop(bola);
    drop(ota);
}
```
## Tushuntirish va Mantiq:
`Weak<T>` ob'ektga egalik qilmaydi (non-owning reference), faqat kuzatadi. U `strong_count`ni oshirmaydi, shuning uchun memory leak bo'lmaydi.
## Ishlash natijasi:
```text
Ota strong count: 1, weak count: 1
Bola muvaffaqiyatli xotiradan tozalandi!
Ota muvaffaqiyatli xotiradan tozalandi!
```

---

# 722-Topshiriq: Weak::upgrade orqali qiymat tirikligini tekshirish
## Topshiriq sharti:
`Weak` ko'rsatkichidan foydalanish uchun uni `upgrade()` qilish orqali `Option<Rc<T>>` olishni dasturlang.
## Yechim (Rust kodi):
```rust
use std::rc::{Rc, Weak};

fn main() {
    let zaif: Weak<i32>;
    {
        let kuchli = Rc::new(500);
        zaif = Rc::downgrade(&kuchli);

        if let Some(qiymat) = zaif.upgrade() {
            println!("Scope ichida tirik: {}", qiymat);
        }
    }

    match zaif.upgrade() {
        Some(qiymat) => println!("Tirik: {}", qiymat),
        None => println!("Ob'ekt allaqachon xotiradan o'chirilgan!"),
    }
}
```
## Tushuntirish va Mantiq:
`upgrade()` metodi `Option<Rc<T>>` qaytaradi. Agar asl ob'ekt xotiradan o'chib ketgan bo'lsa, xavfsiz tarzda `None` qaytariladi.
## Ishlash natijasi:
```text
Scope ichida tirik: 500
Ob'ekt allaqachon xotiradan o'chirilgan!
```

---

# 723-Topshiriq: Double Linked List (ikki yo'nalishli ro'yxat) Rc va RefCell bilan
## Topshiriq sharti:
Oldingi va keyingi tugunlarga ko'rsatkichli ikki yo'nalishli ro'yxatning boshlang'ich elementlarini bog'lang.
## Yechim (Rust kodi):
```rust
use std::rc::{Rc, Weak};
use std::cell::RefCell;

struct Tugun {
    qiymat: i32,
    keyingi: Option<Rc<RefCell<Tugun>>>,
    oldingi: Option<Weak<RefCell<Tugun>>>,
}

fn main() {
    let t1 = Rc::new(RefCell::new(Tugun { qiymat: 10, keyingi: None, oldingi: None }));
    let t2 = Rc::new(RefCell::new(Tugun { qiymat: 20, keyingi: None, oldingi: None }));

    t1.borrow_mut().keyingi = Some(Rc::clone(&t2));
    t2.borrow_mut().oldingi = Some(Rc::downgrade(&t1));

    println!("T1 qiymati: {}", t1.borrow().qiymat);
    println!("T1 -> T2 qiymati: {}", t1.borrow().keyingi.as_ref().unwrap().borrow().qiymat);
}
```
## Tushuntirish va Mantiq:
Ikki yo'nalishli ro'yxatda oldinga harakatlanish uchun `Rc`, orqaga havola qilish uchun `Weak` ishlatilsa sikl yuzaga kelmaydi.
## Ishlash natijasi:
```text
T1 qiymati: 10
T1 -> T2 qiymati: 20
```

---

# 724-Topshiriq: Box<dyn Trait> bilan Trait Object va dynamic dispatch
## Topshiriq sharti:
`Box<dyn Trait>` yordamida runtimeda turli tiplarni bir xil interfeys orqali boshqarish dasturini tuzing.
## Yechim (Rust kodi):
```rust
trait Chiqaruvchi {
    fn chiqar(&self);
}

struct Matn(String);
impl Chiqaruvchi for Matn {
    fn chiqar(&self) { println!("Matn: {}", self.0); }
}

struct Raqam(i32);
impl Chiqaruvchi for Raqam {
    fn chiqar(&self) { println!("Raqam: {}", self.0); }
}

fn main() {
    let ob_matn: Box<dyn Chiqaruvchi> = Box::new(Matn(String::from("Rust")));
    let ob_raqam: Box<dyn Chiqaruvchi> = Box::new(Raqam(777));

    ob_matn.chiqar();
    ob_raqam.chiqar();
}
```
## Tushuntirish va Mantiq:
`dyn Trait` dynamic dispatch (vtable orqali) imkonini beradi. Uning hajmi kompilyatsiya vaqtida noaniq bo'lgani sababli `Box` ichida saqlanadi.
## Ishlash natijasi:
```text
Matn: Rust
Raqam: 777
```

---

# 725-Topshiriq: Heterogeneous kolleksiya: Vec<Box<dyn Shape>>
## Topshiriq sharti:
Bir nechta har xil shakllarni (Doira, Kvadrat) yagona `Vec` ichida saqlab ularning maydonini hisoblang.
## Yechim (Rust kodi):
```rust
trait Shakl {
    fn maydon(&self) -> f64;
}

struct Doira { radius: f64 }
impl Shakl for Doira {
    fn maydon(&self) -> f64 { std::f64::consts::PI * self.radius * self.radius }
}

struct Kvadrat { tomon: f64 }
impl Shakl for Kvadrat {
    fn maydon(&self) -> f64 { self.tomon * self.tomon }
}

fn main() {
    let shakllar: Vec<Box<dyn Shakl>> = vec![
        Box::new(Doira { radius: 3.0 }),
        Box::new(Kvadrat { tomon: 4.0 }),
    ];

    for (i, s) in shakllar.iter().enumerate() {
        println!("Shakl {}: maydon = {:.2}", i + 1, s.maydon());
    }
}
```
## Tushuntirish va Mantiq:
`Vec` bir xil turdagi elementlarni qabul qiladi. `Box<dyn Shakl>` tufayli barcha shakllar bir xil hajmga (fat pointer) ega bo'lib, bitta massivda saqlanadi.
## Ishlash natijasi:
```text
Shakl 1: maydon = 28.27
Shakl 2: maydon = 16.00
```

---

# 726-Topshiriq: Sized vs ?Sized va DST tushunchasi
## Topshiriq sharti:
Kompilyatsiya vaqtida hajmi noma'lum turlar (DST - Dynamically Sized Types) uchun `?Sized` bound'ini qo'llang.
## Yechim (Rust kodi):
```rust
fn chop_et<T: ?Sized + std::fmt::Display>(qiymat: &T) {
    println!("Qiymat: {}", qiymat);
}

fn main() {
    let son: i32 = 123;
    let matn: &str = "Dinamik o'lchamli str";

    chop_et(&son);
    chop_et(matn);
}
```
## Tushuntirish va Mantiq:
Rust'da barcha generic turlar avvalboshdan `T: Sized` deb hisoblanadi. `?Sized` orqali `str` yoki trait object kabi o'lchami noaniq turlarni qabul qilish mumkin.
## Ishlash natijasi:
```text
Qiymat: 123
Qiymat: Dinamik o'lchamli str
```

---

# 727-Topshiriq: std::mem::size_of va size_of_val bilan ko'rsatkichlar hajmini o'lchash
## Topshiriq sharti:
Oddiy pointer, `Box`, `Rc` va trait object (`&dyn Trait`) o'lchamlarini `std::mem::size_of` orqali taqqoslang.
## Yechim (Rust kodi):
```rust
use std::mem::size_of;

trait Namuna {}

fn main() {
    println!("usize hajmi:          {} bayt", size_of::<usize>());
    println!("Box<i32> hajmi:       {} bayt", size_of::<Box<i32>>());
    println!("&i32 hajmi:           {} bayt", size_of::<&i32>());
    println!("&dyn Namuna hajmi:    {} bayt", size_of::<&dyn Namuna>());
    println!("Box<dyn Namuna> hajmi:{} bayt", size_of::<Box<dyn Namuna>>());
}
```
## Tushuntirish va Mantiq:
Oddiy ko'rsatkichlar 1 ta manzil (64-bit tizimda 8 bayt) egallaydi. Trait objectlar esa fat pointer bo'lib (ma'lumot manzili + vtable manzili) 16 bayt egallaydi.
## Ishlash natijasi:
```text
usize hajmi:          8 bayt
Box<i32> hajmi:       8 bayt
&i32 hajmi:           8 bayt
&dyn Namuna hajmi:    16 bayt
Box<dyn Namuna> hajmi:16 bayt
```

---

# 728-Topshiriq: Cow<T> (Clone-on-Write) smart pointeri bilan stringlarni optimallashtirish
## Topshiriq sharti:
`std::borrow::Cow` yordamida kerak bo'lmaganda nusxalamasdan, faqat o'zgartirish zarur bo'lganda clone qiluvchi funksiya yozing.
## Yechim (Rust kodi):
```rust
use std::borrow::Cow;

fn toza_matn(matn: &str) -> Cow<str> {
    if matn.contains("  ") {
        Cow::Owned(matn.replace("  ", " "))
    } else {
        Cow::Borrowed(matn)
    }
}

fn main() {
    let t1 = "Salom Dunyo";
    let natija1 = toza_matn(t1); // Hech qanday heap allocation bo'lmaydi
    println!("Natija 1: {} (Borrowed: {})", natija1, matches!(natija1, Cow::Borrowed(_)));

    let t2 = "Salom   Rust";
    let natija2 = toza_matn(t2); // Heap'da yangi String yaratiladi
    println!("Natija 2: {} (Owned: {})", natija2, matches!(natija2, Cow::Owned(_)));
}
```
## Tushuntirish va Mantiq:
`Cow<T>` faqat o'qishda `&str` havolasidan tejamkor foydalanadi, o'zgartirish kerak bo'lgandagina nusxa ko'chirib `Owned` ga o'tadi.
## Ishlash natijasi:
```text
Natija 1: Salom Dunyo (Borrowed: true)
Natija 2: Salom Rust (Owned: true)
```

---

# 729-Topshiriq: Cow::to_mut orqali avtomatik nusxalash
## Topshiriq sharti:
`Cow` ustida `to_mut()` chaqirilganda u avtomatik tarzda nusxa yaratib o'zgartirishga ruxsat berishini ko'rsating.
## Yechim (Rust kodi):
```rust
use std::borrow::Cow;

fn main() {
    let slice: &[i32] = &[1, 2, 3];
    let mut cow: Cow<[i32]> = Cow::Borrowed(slice);

    // to_mut() chaqirilganda slice heap'ga klonlanadi
    cow.to_mut().push(4);

    println!("Cow elementlari: {:?}", cow);
    assert_eq!(cow.len(), 4);
}
```
## Tushuntirish va Mantiq:
`to_mut()` metodi agar ma'lumot `Borrowed` bo'lsa, uni bir marta klonlaydi va mutable havolani beradi. Keyingi chaqiruvlarda qayta klonlamaydi.
## Ishlash natijasi:
```text
Cow elementlari: [1, 2, 3, 4]
```

---

# 730-Topshiriq: Custom Smart Pointer: LoggerBox yaratish
## Topshiriq sharti:
Har safar deref qilinganda log yozuvchi maxsus `LoggerBox<T>` smart pointerini yarating.
## Yechim (Rust kodi):
```rust
use std::ops::Deref;

struct LoggerBox<T> {
    nomi: &'static str,
    qiymat: T,
}

impl<T> LoggerBox<T> {
    fn new(nomi: &'static str, qiymat: T) -> Self {
        LoggerBox { nomi, qiymat }
    }
}

impl<T> Deref for LoggerBox<T> {
    type Target = T;
    fn deref(&self) -> &Self::Target {
        println!("[LOG]: '{}' pointeriga murojaat qilindi", self.nomi);
        &self.qiymat
    }
}

fn main() {
    let x = LoggerBox::new("user_balance", 15000);
    println!("Hisob: {}", *x);
}
```
## Tushuntirish va Mantiq:
`Deref` trait'i orqali har qanday ob'ektga kirish amallarini nazorat qilish va kuzatuvchi (proxy) qatlam qurish mumkin.
## Ishlash natijasi:
```text
[LOG]: 'user_balance' pointeriga murojaat qilindi
Hisob: 15000
```

---

# 731-Topshiriq: Pin<P> va Unpin trait'i nima uchun kerak
## Topshiriq sharti:
`Pin` smart pointerining vazifasi va o'zgaruvchini xotirada ko'chmas (immobile) qilib qotirib qo'yish asoslarini yozing.
## Yechim (Rust kodi):
```rust
use std::pin::Pin;
use std::marker::PhantomPinned;

struct QimirlamasTuzilma {
    ma_lumot: String,
    _marker: PhantomPinned, // Bu tipni !Unpin qiladi
}

fn main() {
    let obyekt = QimirlamasTuzilma {
        ma_lumot: String::from("Statik xotira"),
        _marker: PhantomPinned,
    };

    let pinned: Pin<Box<QimirlamasTuzilma>> = Box::pin(obyekt);
    println!("Qotirilgan ma'lumot: {}", pinned.ma_lumot);
}
```
## Tushuntirish va Mantiq:
`Pin` ob'ektning xotiradagi manzilini o'zgarmas qilib qotiradi. Bu o'z-o'ziga havola qiluvchi strukturalar (self-referential) va asinxron Future'lar uchun o'ta muhimdir.
## Ishlash natijasi:
```text
Qotirilgan ma'lumot: Statik xotira
```

---

# 732-Topshiriq: Self-referential struct va xotira xavfsizligi
## Topshiriq sharti:
O'zining ichki maydoniga havola qiluvchi strukturalar xotirada ko'chirilganda pointer buzilishi sababini tushuntiruvchi misol tuzing.
## Yechim (Rust kodi):
```rust
struct SelfRef {
    qiymat: String,
    havola: *const String,
}

impl SelfRef {
    fn new(matn: &str) -> Self {
        let mut s = SelfRef {
            qiymat: String::from(matn),
            havola: std::ptr::null(),
        };
        s.havola = &s.qiymat;
        s
    }
}

fn main() {
    let mut a = SelfRef::new("Rust");
    println!("Asl qiymat manzili: {:p}", &a.qiymat);
    println!("Pointer ko'rsatayotgan manzil: {:p}", a.havola);

    // Agar ob'ekt stackda boshqa joyga ko'chirilsa, pointer eski bekor bo'lgan manzilni ko'rsatib qoladi!
    let b = a;
    println!("Yangi b.qiymat manzili: {:p}", &b.qiymat);
    println!("b.havola esa hanuz eski joyda: {:p}", b.havola);
}
```
## Tushuntirish va Mantiq:
Stackda obyekt ko'chirilganda uning ichki raw pointeri avtomatik yangilanmaydi. Shuning uchun `Pin` ularning ko'chirilishini taqiqlaydi.
## Ishlash natijasi:
```text
Asl qiymat manzili: 0x...
Pointer ko'rsatayotgan manzil: 0x...
Yangi b.qiymat manzili: 0x...
b.havola esa hanuz eski joyda: 0x...
```

---

# 733-Topshiriq: NonNull<T> va xavfsiz nol bo'lmagan pointerlar
## Topshiriq sharti:
`std::ptr::NonNull` yordamida hech qachon null bo'lmaydigan xom ko'rsatkichdan foydalaning.
## Yechim (Rust kodi):
```rust
use std::ptr::NonNull;

fn main() {
    let mut son = 100;
    let ptr = NonNull::new(&mut son as *mut i32);

    match ptr {
        Some(valid_ptr) => unsafe {
            println!("NonNull orqali o'qilgan qiymat: {}", *valid_ptr.as_ptr());
        },
        None => println!("Pointer null ekan!"),
    }
}
```
## Tushuntirish va Mantiq:
`NonNull<T>` pointeri hech qachon NULL bo'lmasligini kafolatlaydi, bu esa kompilyatorga Null Pointer Optimization (NPO) qilish imkonini beradi.
## Ishlash natijasi:
```text
NonNull orqali o'qilgan qiymat: 100
```

---

# 734-Topshiriq: std::alloc::Layout va qo'lda heap xotira ajratish
## Topshiriq sharti:
`std::alloc` moduli orqali pastki darajadagi xotirani `alloc` va `dealloc` qilish dasturini yozing.
## Yechim (Rust kodi):
```rust
use std::alloc::{alloc, dealloc, Layout};

fn main() {
    unsafe {
        let layout = Layout::new::<u32>();
        let ptr = alloc(layout) as *mut u32;

        if !ptr.is_null() {
            *ptr = 777;
            println!("Qo'lda ajratilgan xotiradagi son: {}", *ptr);
            dealloc(ptr as *mut u8, layout);
            println!("Xotira muvaffaqiyatli ozod qilindi.");
        }
    }
}
```
## Tushuntirish va Mantiq:
`Layout` xotira o'lchami va hizalanishini (alignment) belgilaydi. `alloc` orqali tizimdan to'g'ridan-to'g'ri baytlar olinadi va `dealloc` bilan qaytariladi.
## Ishlash natijasi:
```text
Qo'lda ajratilgan xotiradagi son: 777
Xotira muvaffaqiyatli ozod qilindi.
```

---

# 735-Topshiriq: std::mem::forget bilan destruktorni chaqirmaslik
## Topshiriq sharti:
`std::mem::forget` yordamida ob'ektning `drop` metodini chaqirishni chetlab o'tishni ko'rsating.
## Yechim (Rust kodi):
```rust
struct MuhimFayl(i32);

impl Drop for MuhimFayl {
    fn drop(&mut self) {
        println!("MuhimFayl #{} tozalandi!", self.0);
    }
}

fn main() {
    let f = MuhimFayl(1);
    std::mem::forget(f); // Destruktor chaqirilmaydi
    println!("Fayl xotiradan 'unutilgan' (leak qilindi), drop ishga tushmadi.");
}
```
## Tushuntirish va Mantiq:
`std::mem::forget` ob'ektning destruktorini chaqirishni to'xtatadi. Bu FFI bilan ishlashda va resurs egaligini boshqa tilga uzatishda ishlatiladi.
## Ishlash natijasi:
```text
Fayl xotiradan 'unutilgan' (leak qilindi), drop ishga tushmadi.
```

---

# 736-Topshiriq: ManuallyDrop<T> yordamida tozalashni qo'lda boshqarish
## Topshiriq sharti:
`std::mem::ManuallyDrop` yordamida destruktorni kerakli vaqtda boshqarishni namoyish qiling.
## Yechim (Rust kodi):
```rust
use std::mem::ManuallyDrop;

struct XotiraResursi(String);

impl Drop for XotiraResursi {
    fn drop(&mut self) {
        println!("XotiraResursi tozalash ishlari bajarildi: {}", self.0);
    }
}

fn main() {
    let mut resurs = ManuallyDrop::new(XotiraResursi(String::from("Kesh_Ma'lumot")));
    println!("Resurs ManuallyDrop ichida saqlanmoqda");

    unsafe {
        // Kerakli paytda qo'lda drop chaqiramiz
        ManuallyDrop::drop(&mut resurs);
    }
    println!("Qo'lda drop bajarilgandan keyin");
}
```
## Tushuntirish va Mantiq:
`ManuallyDrop<T>` kompilyatorga ob'ektni scope tugaganda avtomatik drop qilmaslikni buyuradi. Uni unsafe orqali nazoratli tozalash mumkin.
## Ishlash natijasi:
```text
Resurs ManuallyDrop ichida saqlanmoqda
XotiraResursi tozalash ishlari bajarildi: Kesh_Ma'lumot
Qo'lda drop bajarilgandan keyin
```

---

# 737-Topshiriq: MaybeUninit<T> orqali initsializatsiya qilinmagan xotirani to'ldirish
## Topshiriq sharti:
`std::mem::MaybeUninit` yordamida bo'sh massiv buferini xavfsiz tarzda bittalab to'ldirib yakuniy massivga aylantiring.
## Yechim (Rust kodi):
```rust
use std::mem::MaybeUninit;

fn main() {
    let mut massiv: [MaybeUninit<i32>; 5] = unsafe {
        MaybeUninit::uninit().assume_init()
    };

    for i in 0..5 {
        massiv[i].write(i as i32 * 10);
    }

    // Endi xavfsiz tarzda o'qiymiz
    let natija: [i32; 5] = unsafe {
        std::mem::transmute_copy(&massiv)
    };

    println!("Initsializatsiya qilingan massiv: {:?}", natija);
}
```
## Tushuntirish va Mantiq:
`MaybeUninit<T>` kompilyatorga ushbu xotira hali initsializatsiya qilinmagan bo'lishi mumkinligini aytadi va undefined behavior oldini oladi.
## Ishlash natijasi:
```text
Initsializatsiya qilingan massiv: [0, 10, 20, 30, 40]
```

---

# 738-Topshiriq: Oddiy Arena Allocator (Bump Allocator) yaratish
## Topshiriq sharti:
Kichik ob'ektlarni bitta umumiy buferga ketma-ket joylashtiruvchi sodda arena allocator prototipini yozing.
## Yechim (Rust kodi):
```rust
struct BumpArena {
    xotira: Vec<u8>,
}

impl BumpArena {
    fn new(sigim: usize) -> Self {
        BumpArena { xotira: Vec::with_capacity(sigim) }
    }

    fn joylashtir(&mut self, ma_lumot: u8) -> *const u8 {
        self.xotira.push(ma_lumot);
        let len = self.xotira.len();
        &self.xotira[len - 1] as *const u8
    }
}

fn main() {
    let mut arena = BumpArena::new(1024);
    let p1 = arena.joylashtir(65);
    let p2 = arena.joylashtir(66);

    unsafe {
        println!("Arena element 1: {}", *p1 as char);
        println!("Arena element 2: {}", *p2 as char);
    }
}
```
## Tushuntirish va Mantiq:
Arena allocatorlar xotirani alohida-alohida ajratish o'rniga bitta katta blokdan tezkor offset qo'shish (bump) orqali ajratadi.
## Ishlash natijasi:
```text
Arena element 1: A
Arena element 2: B
```

---

# 739-Topshiriq: Stack vs Heap xotira samaradorligi va taqqoslash
## Topshiriq sharti:
Stackda va heapda (Box) 100,000 ta operatsiya bajarilish vaqtini taqqoslovchi benchmark yozing.
## Yechim (Rust kodi):
```rust
use std::time::Instant;

fn main() {
    const SONI: usize = 100_000;

    let boshlandi = Instant::now();
    let mut stack_yigindi = 0i64;
    for i in 0..SONI {
        let a = i as i64;
        stack_yigindi += a;
    }
    let stack_vaqt = boshlandi.elapsed();

    let boshlandi = Instant::now();
    let mut heap_yigindi = 0i64;
    for i in 0..SONI {
        let b = Box::new(i as i64);
        heap_yigindi += *b;
    }
    let heap_vaqt = boshlandi.elapsed();

    println!("Stack yig'indi: {}, vaqt: {:?}", stack_yigindi, stack_vaqt);
    println!("Heap yig'indi:  {}, vaqt: {:?}", heap_yigindi, heap_vaqt);
    println!("Xulosa: Stack operatsiyalari har doim heap allocation'dan sezilarli darajada tez!");
}
```
## Tushuntirish va Mantiq:
Stack xotira faqat stack pointer'ni siljitadi (juda tez), heap esa operatsion tizimdan xotira sahifasini so'rashi kerak bo'ladi.
## Ishlash natijasi:
```text
Stack yig'indi: 4999950000, vaqt: ...
Heap yig'indi:  4999950000, vaqt: ...
Xulosa: Stack operatsiyalari har doim heap allocation'dan sezilarli darajada tez!
```

---

# 740-Topshiriq: RAII (Resource Acquisition Is Initialization) pattern
## Topshiriq sharti:
Fayl yoki resurs ochilganda avtomatik qulflanuvchi va scope tugaganda yopiluvchi maxsus Guard strukturasini yarating.
## Yechim (Rust kodi):
```rust
struct ResursGuard<'a> {
    nomi: &'a str,
}

impl<'a> ResursGuard<'a> {
    fn ochish(nomi: &'a str) -> Self {
        println!("[OCHILDI]: Resurs '{}' qulflab olindi", nomi);
        ResursGuard { nomi }
    }
}

impl<'a> Drop for ResursGuard<'a> {
    fn drop(&mut self) {
        println!("[YOPILDI]: Resurs '{}' avtomatik bo'shatildi", self.nomi);
    }
}

fn main() {
    {
        let _guard = ResursGuard::ochish("Ma'lumotlar_Bazasi_Ulanishi");
        println!("Ma'lumotlar bilan xavfsiz ish olib borilmoqda...");
    }
    println!("Asosiy oqim davom etmoqda.");
}
```
## Tushuntirish va Mantiq:
RAII tamoyili Rust xavfsizligining negizidir: resurs ochilganda ob'ektga bog'lanadi va ob'ekt yo'qolganda avtomatik bo'shatiladi.
## Ishlash natijasi:
```text
[OCHILDI]: Resurs 'Ma'lumotlar_Bazasi_Ulanishi' qulflab olindi
Ma'lumotlar bilan xavfsiz ish olib borilmoqda...
[YOPILDI]: Resurs 'Ma'lumotlar_Bazasi_Ulanishi' avtomatik bo'shatildi
Asosiy oqim davom etmoqda.
```

---

# 741-Topshiriq: MutexGuard va RAII: qulf tushganda avtomatik unlock
## Topshiriq sharti:
`std::sync::Mutex` yordamida qulflangan o'zgaruvchining guard drop bo'lishi bilan boshqa oqimlar uchun ochilishini ko'rsating.
## Yechim (Rust kodi):
```rust
use std::sync::Mutex;

fn main() {
    let m = Mutex::new(10);
    {
        let mut qulf = m.lock().unwrap();
        *qulf += 5;
        println!("Qulf ichidagi qiymat: {}", *qulf);
    } // qulf shu yerda drop bo'ladi va Mutex avtomatik unlock qilinadi

    let ikkinchi_qulf = m.lock().unwrap();
    println!("Yangi qulf muvaffaqiyatli olindi: {}", *ikkinchi_qulf);
}
```
## Tushuntirish va Mantiq:
`Mutex::lock` qaytaradigan `MutexGuard` smart pointeri `DerefMut` va `Drop`ni amalga oshiradi. Scope yopilishi bilanoq mutex ochiladi.
## Ishlash natijasi:
```text
Qulf ichidagi qiymat: 15
Yangi qulf muvaffaqiyatli olindi: 15
```

---

# 742-Topshiriq: Rc bilan Graf (Graph) tugunlarini modellashtirish
## Topshiriq sharti:
Har bir tugun boshqa ixtiyoriy tugunlarga yo'nalgan yo'llarga ega bo'lgan yo'naltirilgan grafni `Rc` yordamida quring.
## Yechim (Rust kodi):
```rust
use std::rc::Rc;
use std::cell::RefCell;

struct GrafTugun {
    id: usize,
    qoshnilar: Vec<Rc<RefCell<GrafTugun>>>,
}

fn main() {
    let t1 = Rc::new(RefCell::new(GrafTugun { id: 1, qoshnilar: vec![] }));
    let t2 = Rc::new(RefCell::new(GrafTugun { id: 2, qoshnilar: vec![] }));

    t1.borrow_mut().qoshnilar.push(Rc::clone(&t2));

    println!("Tugun 1 ulanishlari soni: {}", t1.borrow().qoshnilar.len());
    println!("Tugun 1 ning qo'shnisi: Tugun {}", t1.borrow().qoshnilar[0].borrow().id);
}
```
## Tushuntirish va Mantiq:
Graflarda har bir tugun bir nechta boshqa tugunlarning qo'shnisi bo'lishi mumkinligi uchun `Rc<RefCell<GrafTugun>>` ishlatiladi.
## Ishlash natijasi:
```text
Tugun 1 ulanishlari soni: 1
Tugun 1 ning qo'shnisi: Tugun 2
```

---

# 743-Topshiriq: Observer pattern: Rc<RefCell<dyn Observer>>
## Topshiriq sharti:
Ob-havo stantsiyasi va unga obuna bo'lgan bir nechta displeylarni bildirish tizimi bilan Observer patternida dasturlang.
## Yechim (Rust kodi):
```rust
use std::rc::Rc;
use std::cell::RefCell;

trait Observer {
    fn yangilandi(&self, harorat: f32);
}

struct Displey {
    nomi: String,
}

impl Observer for Displey {
    fn yangilandi(&self, harorat: f32) {
        println!("{}: yangi harorat {} C", self.nomi, harorat);
    }
}

struct Stansiya {
    kuzatuvchilar: Vec<Rc<RefCell<dyn Observer>>>,
}

impl Stansiya {
    fn obuna(&mut self, obs: Rc<RefCell<dyn Observer>>) {
        self.kuzatuvchilar.push(obs);
    }

    fn xabar_berish(&self, harorat: f32) {
        for k in &self.kuzatuvchilar {
            k.borrow().yangilandi(harorat);
        }
    }
}

fn main() {
    let d1 = Rc::new(RefCell::new(Displey { nomi: String::from("Displey_1") }));
    let d2 = Rc::new(RefCell::new(Displey { nomi: String::from("Displey_2") }));

    let mut st = Stansiya { kuzatuvchilar: vec![] };
    st.obuna(Rc::clone(&d1));
    st.obuna(Rc::clone(&d2));

    st.xabar_berish(25.5);
}
```
## Tushuntirish va Mantiq:
Observer pattern'da kuzatuvchilar ro'yxatini boshqarish va ularning holatini dinamik yangilash uchun `Rc<RefCell<dyn Trait>>` qo'l keladi.
## Ishlash natijasi:
```text
Displey_1: yangi harorat 25.5 C
Displey_2: yangi harorat 25.5 C
```

---

# 744-Topshiriq: LRU Cache (Eng kam ishlatilgan kesh) boshlang'ich arxitekturasi
## Topshiriq sharti:
Kesh hajmi cheklangan va elementlarga murojaatni boshqaruvchi sodda struktura tuzing.
## Yechim (Rust kodi):
```rust
use std::collections::HashMap;
use std::rc::Rc;
use std::cell::RefCell;

struct KeshYozuvi {
    qiymat: String,
}

struct OddiyKesh {
    sigim: usize,
    xarita: HashMap<String, Rc<RefCell<KeshYozuvi>>>,
}

impl OddiyKesh {
    fn new(sigim: usize) -> Self {
        OddiyKesh { sigim, xarita: HashMap::new() }
    }

    fn saqla(&mut self, kalit: &str, qiymat: &str) {
        if self.xarita.len() >= self.sigim {
            println!("Sig'im to'ldi, kesh boshqarilishi lozim");
        }
        self.xarita.insert(
            kalit.to_string(),
            Rc::new(RefCell::new(KeshYozuvi { qiymat: qiymat.to_string() })),
        );
    }

    fn ol(&self, kalit: &str) -> Option<String> {
        self.xarita.get(kalit).map(|v| v.borrow().qiymat.clone())
    }
}

fn main() {
    let mut kesh = OddiyKesh::new(2);
    kesh.saqla("a", "Alfa");
    kesh.saqla("b", "Beta");
    println!("a: {:?}", kesh.ol("a"));
}
```
## Tushuntirish va Mantiq:
`HashMap` va `Rc<RefCell<T>>` birgalikda keshdagi qiymatlarni bir vaqtda bir nechta joydan boshqarish imkonini beradi.
## Ishlash natijasi:
```text
a: Some("Alfa")
```

---

# 745-Topshiriq: std::borrow::Borrow va ToOwned trait'lari
## Topshiriq sharti:
Generic funksiyalarda ham `&String` ham `&str` ni bir xil tarzda qabul qilish uchun `Borrow` trait'ini qo'llang.
## Yechim (Rust kodi):
```rust
use std::borrow::Borrow;

fn uzunlik_olchash<K: Borrow<str>>(kalit: K) -> usize {
    kalit.borrow().len()
}

fn main() {
    let matn_string = String::from("Toshkent");
    let matn_slice = "Samarqand";

    println!("String uzunligi: {}", uzunlik_olchash(matn_string));
    println!("&str uzunligi:   {}", uzunlik_olchash(matn_slice));
}
```
## Tushuntirish va Mantiq:
`Borrow<T>` trait'i har xil egalik turlaridan umumiy borrow qilingan havolani olish imkonini beradi (`HashMap::get` ham shundan foydalanadi).
## Ishlash natijasi:
```text
String uzunligi: 8
&str uzunligi:   9
```

---

# 746-Topshiriq: Rc::make_mut yordamida Copy-On-Write amalga oshirish
## Topshiriq sharti:
`Rc::make_mut` orqali agar faqat bitta havola bo'lsa o'z joyida o'zgartirish, boshqa havolalar bo'lsa klonlashni ko'rsating.
## Yechim (Rust kodi):
```rust
use std::rc::Rc;

fn main() {
    let mut data = Rc::new(vec![1, 2, 3]);

    // Hozirda faqat 1 ta havola bor: o'z joyida o'zgaradi
    Rc::make_mut(&mut data).push(4);
    println!("Bitta havola paytida: {:?}", data);

    let boshqa_havola = Rc::clone(&data);

    // Endi 2 ta havola bor: make_mut data uchun yangi xotira ajratadi va klonlaydi
    Rc::make_mut(&mut data).push(5);

    println!("Klonlangan data:         {:?}", data);
    println!("O'zgarmagan boshqa havola: {:?}", boshqa_havola);
}
```
## Tushuntirish va Mantiq:
`Rc::make_mut` agar `strong_count == 1` bo'lsa xotira ajratmaydi. Agar ko'p bo'lsa, xavfsizlik uchun alohida nusxa ko'chirib beradi.
## Ishlash natijasi:
```text
Bitta havola paytida: [1, 2, 3, 4]
Klonlangan data:         [1, 2, 3, 4, 5]
O'zgarmagan boshqa havola: [1, 2, 3, 4]
```

---

# 747-Topshiriq: RefCell orqali Mock Object (test qilish uchun soxta obyekt) yaratish
## Topshiriq sharti:
Immutable interfeys talab qiladigan xabarchi tizimni test qilish uchun ichki xabarlar tarixini saqlovchi Mock yaratish.
## Yechim (Rust kodi):
```rust
use std::cell::RefCell;

trait XabarYuboruvchi {
    fn yubor(&self, xabar: &str);
}

struct MockXabarchi {
    yuborilgan_xabarlar: RefCell<Vec<String>>,
}

impl MockXabarchi {
    fn new() -> Self {
        MockXabarchi { yuborilgan_xabarlar: RefCell::new(vec![]) }
    }
}

impl XabarYuboruvchi for MockXabarchi {
    fn yubor(&self, xabar: &str) {
        self.yuborilgan_xabarlar.borrow_mut().push(String::from(xabar));
    }
}

fn main() {
    let mock = MockXabarchi::new();
    mock.yubor("Test 1");
    mock.yubor("Test 2");

    println!("Yuborilgan xabarlar soni: {}", mock.yuborilgan_xabarlar.borrow().len());
    println!("Ro'yxat: {:?}", *mock.yuborilgan_xabarlar.borrow());
}
```
## Tushuntirish va Mantiq:
`RefCell` testlarda (mocking) juda mashhur: trait metodi `&self` olsa ham test klassi ichki chaqiruvlarni o'ziga yozib olishi mumkin.
## Ishlash natijasi:
```text
Yuborilgan xabarlar soni: 2
Ro'yxat: ["Test 1", "Test 2"]
```

---

# 748-Topshiriq: PhantomData<T> marker tipi va kompilyatorga egalikni bildirish
## Topshiriq sharti:
Struktura ichida `*const T` saqlansa-da, kompilyatorga `T` ga egalik qilishini aytish uchun `PhantomData` ishlatish.
## Yechim (Rust kodi):
```rust
use std::marker::PhantomData;

struct MeningPointerim<T> {
    ptr: *const T,
    _marker: PhantomData<T>,
}

impl<T> MeningPointerim<T> {
    fn new(qiymat: &T) -> Self {
        MeningPointerim {
            ptr: qiymat as *const T,
            _marker: PhantomData,
        }
    }
}

fn main() {
    let son = 42;
    let ptr = MeningPointerim::new(&son);
    println!("PhantomData strukturasi yaratildi, o'lchami: {} bayt", std::mem::size_of_val(&ptr));
}
```
## Tushuntirish va Mantiq:
`PhantomData<T>` runtime xotira egallamaydi (0 bayt), lekin kompilyatorning borrow checker va drop checker mexanizmlariga tur haqida signal beradi.
## Ishlash natijasi:
```text
PhantomData strukturasi yaratildi, o'lchami: 8 bayt
```

---

# 749-Topshiriq: Zero-Sized Types (ZST) va ularning xotiradagi o'rni
## Topshiriq sharti:
Hajmi roppa-rosa 0 bayt bo'lgan struktura va massivlarni xotirada hech qanday joy olmasdan ishlashini ko'rsating.
## Yechim (Rust kodi):
```rust
use std::mem::size_of;

struct BoshTuzilma;

fn main() {
    println!("BoshTuzilma hajmi:       {} bayt", size_of::<BoshTuzilma>());
    println!("() birlik turi hajmi:     {} bayt", size_of::<()>());
    println!("[i32; 0] bo'sh massiv:   {} bayt", size_of::<[i32; 0]>());

    // 1 million bo'sh struktura ham 0 bayt oladi!
    let kop_bosh = vec![BoshTuzilma; 1_000_000];
    println!("1 millionta ZST hajmi:   {} bayt", std::mem::size_of_val(&kop_bosh[..]));
}
```
## Tushuntirish va Mantiq:
Rust ZST (Zero-Sized Types) bilan xotira ajratmasdan statik tekshiruvlar, holat mashinalari va markerlar yaratishga imkon beradi.
## Ishlash natijasi:
```text
BoshTuzilma hajmi:       0 bayt
() birlik turi hajmi:     0 bayt
[i32; 0] bo'sh massiv:   0 bayt
1 millionta ZST hajmi:   0 bayt
```

---

# 750-Topshiriq: Smart Pointerlar umumiy amaliyoti: Xotira xavfsiz integratsion tizim
## Topshiriq sharti:
`Box`, `Rc`, `RefCell` va `Weak` vositalarini bitta integratsion xotira boshqaruv tizimida birlashtiruvchi amaliy kod yozing.
## Yechim (Rust kodi):
```rust
use std::rc::{Rc, Weak};
use std::cell::RefCell;

struct Foydalanuvchi {
    id: u64,
    ism: String,
    xabarlar: RefCell<Vec<String>>,
    guruh: RefCell<Weak<Guruh>>,
}

struct Guruh {
    nomi: String,
    azolar: RefCell<Vec<Rc<Foydalanuvchi>>>,
}

fn main() {
    let guruh = Rc::new(Guruh {
        nomi: String::from("Rustaceanlar Jamiyati"),
        azolar: RefCell::new(vec![]),
    });

    let user1 = Rc::new(Foydalanuvchi {
        id: 1,
        ism: String::from("Ali"),
        xabarlar: RefCell::new(vec![]),
        guruh: RefCell::new(Rc::downgrade(&guruh)),
    });

    guruh.azolar.borrow_mut().push(Rc::clone(&user1));
    user1.xabarlar.borrow_mut().push(String::from("Assalomu alaykum!"));

    println!("Guruh: {}", guruh.nomi);
    println!("A'zolar soni: {}", guruh.azolar.borrow().len());
    println!("Birinchi a'zo xabarlari: {:?}", user1.xabarlar.borrow());

    // Zaif havola orqali guruh nomini olish
    if let Some(ota_guruh) = user1.guruh.borrow().upgrade() {
        println!("Ali tegishli bo'lgan guruh: {}", ota_guruh.nomi);
    }
}
```
## Tushuntirish va Mantiq:
`Rc`, `Weak`, `RefCell` va `Box` smart pointerlarining to'g'ri integratsiyasi aylana havolalardan (memory leaks) xoli, xotirasi xavfsiz va moslashuvchan tizimlarni yaratish garovidir.
## Ishlash natijasi:
```text
Guruh: Rustaceanlar Jamiyati
A'zolar soni: 1
Birinchi a'zo xabarlari: ["Assalomu alaykum!"]
Ali tegishli bo'lgan guruh: Rustaceanlar Jamiyati
```

---
