# Rust Dasturlash Tili: Unsafe Rust va FFI / C Interoperability

Ushbu modulda Rust'ning eng chuqur va qudratli imkoniyatlari: Unsafe Rust, xom ko'rsatkichlar (`*const T`, `*mut T`), pointer arifmetikasi, `transmute`, `#[repr(C)]`, C-FFI (tashqi C kutubxonalari bilan aloqa), `CString`/`CStr`, Inline Assembly (`asm!`), SIMD, `UnsafeCell` va xavfsiz abstraksiyalar (Safe Wrappers) to'liq yoritilgan.

---

# 901-Topshiriq: Unsafe Rust nima va uning 5 ta super-kuchi
## Topshiriq sharti:
Rust tilida `unsafe` kalit so'zi beradigan 5 ta asosiy imkoniyatni dastur orqali tushuntiring.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Unsafe Rust'ning 5 ta super-kuchi (Superpowers):");
    println!("1. Xom ko'rsatkichlarni (Raw Pointers) dereference qilish.");
    println!("2. Unsafe funksiya yoki metodlarni chaqirish.");
    println!("3. Unsafe trait'larni amalga oshirish (impl).");
    println!("4. O'zgaruvchan statik o'zgaruvchilarni (static mut) o'zgartirish.");
    println!("5. Union maydonlariga murojaat qilish.");
}
```
## Tushuntirish va Mantiq:
`unsafe` Rust borrow checkerni o'chirib qo'ymaydi, faqat yuqoridagi 5 ta xavfli operatsiyani dasturchi mas'uliyatiga topshiradi.
## Ishlash natijasi:
```text
Unsafe Rust'ning 5 ta super-kuchi (Superpowers):
1. Xom ko'rsatkichlarni (Raw Pointers) dereference qilish.
2. Unsafe funksiya yoki metodlarni chaqirish.
3. Unsafe trait'larni amalga oshirish (impl).
4. O'zgaruvchan statik o'zgaruvchilarni (static mut) o'zgartirish.
5. Union maydonlariga murojaat qilish.
```

---

# 902-Topshiriq: Raw pointer yaratish: *const T va *mut T
## Topshiriq sharti:
Xavfsiz (safe) kod ichida xom ko'rsatkichlarni hosil qilish dasturini yozing.
## Yechim (Rust kodi):
```rust
fn main() {
    let mut son: i32 = 42;

    // Raw pointer yaratish xavfsiz kodda ruxsat etiladi:
    let r1: *const i32 = &son as *const i32;
    let r2: *mut i32 = &mut son as *mut i32;

    println!("Immutable raw pointer: {:p}", r1);
    println!("Mutable raw pointer:   {:p}", r2);
}
```
## Tushuntirish va Mantiq:
Raw pointerlar yaratish xavfsiz, ammo ularning manzilidagi ma'lumotni o'qish (`*r1`) faqat `unsafe` blok ichida bajariladi.
## Ishlash natijasi:
```text
Immutable raw pointer: 0x...
Mutable raw pointer:   0x...
```

---

# 903-Topshiriq: Raw pointerni dereference qilish (*r)
## Topshiriq sharti:
Xom ko'rsatkich orqali qiymatni o'qish va o'zgartirishni `unsafe` blokda bajaring.
## Yechim (Rust kodi):
```rust
fn main() {
    let mut son = 10;
    let ptr = &mut son as *mut i32;

    unsafe {
        *ptr += 25; // Xom ko'rsatkich orqali yozish
        println!("Raw pointer orqali o'qilgan qiymat: {}", *ptr);
    }
}
```
## Tushuntirish va Mantiq:
Dasturchi pointer ko'rsatayotgan xotira manzili haqiqatan ham yaroqli ekanligiga 100% kafolat berishi shart.
## Ishlash natijasi:
```text
Raw pointer orqali o'qilgan qiymat: 35
```

---

# 904-Topshiriq: Raw pointer arifmetikasi: ptr.add(offset)
## Topshiriq sharti:
Massiv elementlari bo'ylab xom ko'rsatkichni siljitish (pointer arithmetic).
## Yechim (Rust kodi):
```rust
fn main() {
    let massiv = [10, 20, 30, 40];
    let ptr = massiv.as_ptr();

    unsafe {
        println!("0-element: {}", *ptr);
        println!("1-element: {}", *ptr.add(1));
        println!("2-element: {}", *ptr.add(2));
        println!("3-element: {}", *ptr.add(3));
    }
}
```
## Tushuntirish va Mantiq:
`ptr.add(n)` xotira manzilini `n * sizeof(T)` baytga oldinga siljitadi. C tilidagi `ptr + n` bilan aynan bir xil.
## Ishlash natijasi:
```text
0-element: 10
1-element: 20
2-element: 30
3-element: 40
```

---

# 905-Topshiriq: std::ptr::null va null pointer tekshiruvi
## Topshiriq sharti:
Nol ko'rsatkich (NULL pointer) yaratish va uni `is_null()` bilan tekshirish.
## Yechim (Rust kodi):
```rust
use std::ptr;

fn main() {
    let p_null: *const i32 = ptr::null();
    let p_valid: *const i32 = &100;

    println!("p_null null-mi:  {}", p_null.is_null());
    println!("p_valid null-mi: {}", p_valid.is_null());
}
```
## Tushuntirish va Mantiq:
Rust oddiy havolalarda (`&T`) NULL bo'lishiga yo'l qo'ymaydi, ammo raw pointerlar `ptr::null()` bo'lishi mumkin.
## Ishlash natijasi:
```text
p_null null-mi:  true
p_valid null-mi: false
```

---

# 906-Topshiriq: std::ptr::read va std::ptr::write
## Topshiriq sharti:
Egalikni ko'chirmasdan xom manzildan o'qish va xotiraga yozish amallarini bajaring.
## Yechim (Rust kodi):
```rust
use std::ptr;

fn main() {
    let mut son = 0;
    let ptr = &mut son as *mut i32;

    unsafe {
        ptr::write(ptr, 777);
        let oqildi = ptr::read(ptr);
        println!("ptr::read orqali olingan qiymat: {}", oqildi);
    }
}
```
## Tushuntirish va Mantiq:
`ptr::read` eski qiymatning destruktorini chaqirmasdan bitlarni nusxalab oladi, `ptr::write` esa eski qiymatni drop qilmasdan yozadi.
## Ishlash natijasi:
```text
ptr::read orqali olingan qiymat: 777
```

---

# 907-Topshiriq: std::ptr::copy va copy_nonoverlapping (C memcpy)
## Topshiriq sharti:
Bir massivdan ikkinchisiga baytlarni xom tezkor nusxalash.
## Yechim (Rust kodi):
```rust
use std::ptr;

fn main() {
    let manba = [1, 2, 3, 4, 5];
    let mut maqsad = [0; 5];

    unsafe {
        ptr::copy_nonoverlapping(manba.as_ptr(), maqsad.as_mut_ptr(), manba.len());
    }

    println!("Nusxalangan massiv: {:?}", maqsad);
}
```
## Tushuntirish va Mantiq:
`copy_nonoverlapping` C tilidagi `memcpy` ning to'g'ridan-to'g'ri analogi bo'lib, unumdorligi o'ta yuqori hisoblanadi.
## Ishlash natijasi:
```text
Nusxalangan massiv: [1, 2, 3, 4, 5]
```

---

# 908-Topshiriq: Unsafe funksiya: unsafe fn e'lon qilish va chaqirish
## Topshiriq sharti:
Chaqiruvchidan qat'iy talablarni talab qiluvchi `unsafe fn` e'lon qiling.
## Yechim (Rust kodi):
```rust
unsafe fn xavfli_bolish(boluvchi: i32) -> i32 {
    // Shart: boluvchi nol bo'lmasligi shart!
    100 / boluvchi
}

fn main() {
    unsafe {
        let natija = xavfli_bolish(5);
        println!("Unsafe funksiya natijasi: {}", natija);
    }
}
```
## Tushuntirish va Mantiq:
Agar funksiya noto'g'ri chaqirilsa Undefined Behavior kelib chiqishi mumkin bo'lsa, u `unsafe fn` deb e'lon qilinishi shart.
## Ishlash natijasi:
```text
Unsafe funksiya natijasi: 20
```

---

# 909-Topshiriq: Safe Abstraction: Xavfsiz qobiq (wrapper) yaratish
## Topshiriq sharti:
Ichida unsafe kod bo'lsa-da, tashqariga 100% xavfsiz interfeys beruvchi funksiya yozing (masalan, `split_at_mut`).
## Yechim (Rust kodi):
```rust
fn massivni_bol<T>(slice: &mut [T], oraliq: usize) -> (&mut [T], &mut [T]) {
    let uzunlik = slice.len();
    assert!(oraliq <= uzunlik);

    let ptr = slice.as_mut_ptr();

    unsafe {
        (
            std::slice::from_raw_parts_mut(ptr, oraliq),
            std::slice::from_raw_parts_mut(ptr.add(oraliq), uzunlik - oraliq),
        )
    }
}

fn main() {
    let mut sonlar = vec![1, 2, 3, 4, 5, 6];
    let (chap, ong) = massivni_bol(&mut sonlar, 3);
    println!("Chap: {:?}, O'ng: {:?}", chap, ong);
}
```
## Tushuntirish va Mantiq:
Rust falsafasining poydevori: pastki qatlamdagi xavfli operatsiyalarni xavfsiz abstraksiya bilan o'rab (Safe wrapper) yuqori qatlamni himoya qilish.
## Ishlash natijasi:
```text
Chap: [1, 2, 3], O'ng: [4, 5, 6]
```

---

# 910-Topshiriq: std::slice::from_raw_parts bilan massiv yasash
## Topshiriq sharti:
Xom manzil va uzunlikdan xavfsiz Rust slice (`&[T]`) hosil qilish.
## Yechim (Rust kodi):
```rust
use std::slice;

fn main() {
    let son = 12345;
    let ptr = &son as *const i32;

    unsafe {
        let s = slice::from_raw_parts(ptr, 1);
        println!("Slice uzunligi: {}, element: {}", s.len(), s[0]);
    }
}
```
## Tushuntirish va Mantiq:
`from_raw_parts` ko'rsatkichning yaroqli va ko'rsatilgan uzunlikda xotirada joylashganini talab qiladi.
## Ishlash natijasi:
```text
Slice uzunligi: 1, element: 12345
```

---

# 911-Topshiriq: std::str::from_utf8_unchecked: Tezkor satr yaratish
## Topshiriq sharti:
UTF-8 tekshiruvini chetlab o'tib, baytlar massivini zudlik bilan `&str` ga o'girish.
## Yechim (Rust kodi):
```rust
use std::str;

fn main() {
    let baytlar = b"Salom Rust 2024!";

    // Xavfsiz usul: str::from_utf8(baytlar) har bir baytni tekshiradi (O(N) vaqt)
    // Unsafe usul: agar biz baytlarning to'g'ri UTF-8 ekaniga 100% amin bo'lsak:
    let matn: &str = unsafe { str::from_utf8_unchecked(baytlar) };
    println!("Tezkor o'girilgan matn: {}", matn);
}
```
## Tushuntirish va Mantiq:
`from_utf8_unchecked` nol xarajatli (O(1)) konvertatsiya beradi, ammo agar baytlar noto'g'ri bo'lsa, dastur darhol qulaydi.
## Ishlash natijasi:
```text
Tezkor o'girilgan matn: Salom Rust 2024!
```

---

# 912-Topshiriq: std::mem::transmute: Bir tipni ikkinchisiga o'girish (bit-cast)
## Topshiriq sharti:
Bir xil o'lchamdagi ikki xil tipning bitlarini to'g'ridan-to'g'ri qayta talqin qilish.
## Yechim (Rust kodi):
```rust
use std::mem;

fn main() {
    let son: u32 = 0x41424344; // 'D', 'C', 'B', 'A' baytlari

    // 4 baytli u32 ni 4 baytli [u8; 4] massiviga aylantirish
    let baytlar: [u8; 4] = unsafe { mem::transmute(son) };
    println!("Transmute natijasi: {:X?}", baytlar);
}
```
## Tushuntirish va Mantiq:
`transmute` Rust'dagi eng xavfli operatsiyalardan biridir. Manba va maqsad turlarning hajmi aniq bir xil bo'lishi shart.
## Ishlash natijasi:
```text
Transmute natijasi: [44, 43, 42, 41]
```

---

# 913-Topshiriq: Mutable static o'zgaruvchilar: static mut
## Topshiriq sharti:
Global o'zgaruvchan holatni `static mut` bilan e'lon qilish va unga unsafe orqali murojaat qilish.
## Yechim (Rust kodi):
```rust
static mut GLOBAL_SANAGICH: u32 = 0;

fn oshir() {
    unsafe {
        GLOBAL_SANAGICH += 1;
    }
}

fn main() {
    oshir();
    oshir();
    unsafe {
        println!("Global hisob: {}", GLOBAL_SANAGICH);
    }
}
```
## Tushuntirish va Mantiq:
`static mut` multithreadingda race condition xavfini tug'dirgani sababli faqat `unsafe` blokda o'zgartiriladi (zamonaviy kodda `Atomic` yoki `Mutex` afzal).
## Ishlash natijasi:
```text
Global hisob: 2
```

---

# 914-Topshiriq: Unsafe Trait: unsafe trait va unsafe impl
## Topshiriq sharti:
Kompilyator avtomatik tekshira olmaydigan invariyantlarga ega unsafe trait yarating.
## Yechim (Rust kodi):
```rust
unsafe trait XavfsizXotiraUlashuvchi {
    fn tekshirish(&self) -> bool;
}

struct Xotira;

unsafe impl XavfsizXotiraUlashuvchi for Xotira {
    fn tekshirish(&self) -> bool {
        true
    }
}

fn main() {
    let x = Xotira;
    println!("Unsafe trait muvaffaqiyatli amalga oshirildi: {}", x.tekshirish());
}
```
## Tushuntirish va Mantiq:
Agar trait'ni noto'g'ri implement qilish xotira buzilishiga (UB) olib kelsa (masalan, `Send` va `Sync`), trait `unsafe` deb belgilanadi.
## Ishlash natijasi:
```text
Unsafe trait muvaffaqiyatli amalga oshirildi: true
```

---

# 915-Topshiriq: Union tiplari: C uslubidagi union'lar bilan ishlash
## Topshiriq sharti:
Barcha maydonlari bitta umumiy xotira manzilida joylashuvchi `union` strukturasini tuzing.
## Yechim (Rust kodi):
```rust
#[repr(C)]
union Sinov {
    butun: u32,
    baytlar: [u8; 4],
}

fn main() {
    let mut u = Sinov { butun: 0x12345678 };

    unsafe {
        println!("Butun son: 0x{:X}", u.butun);
        println!("Birinchi bayt: 0x{:X}", u.baytlar[0]);
    }
}
```
## Tushuntirish va Mantiq:
`union` maydonlarini o'qish `unsafe` hisoblanadi, chunki Rust xotirada qaysi maydon saqlanganini runtimeda kuzatmaydi.
## Ishlash natijasi:
```text
Butun son: 0x12345678
Birinchi bayt: 0x78
```

---

# 916-Topshiriq: #[repr(C)] atributi: C tili bilan mos xotira hizalanishi
## Topshiriq sharti:
Struktura xotirada C kompilyatori (GCC/Clang) bilan aynan bir xil joylashishi uchun `#[repr(C)]` qo'llang.
## Yechim (Rust kodi):
```rust
#[repr(C)]
struct CRuxsatliStruktura {
    a: u8,
    b: u32,
}

fn main() {
    println!("repr(C) struktura hajmi: {} bayt", std::mem::size_of::<CRuxsatliStruktura>());
}
```
## Tushuntirish va Mantiq:
Rust sukut bo'yicha strukturadagi maydonlar o'rnini xotirani tejash uchun almashtirishi mumkin. `#[repr(C)]` esa C tartibini saqlaydi.
## Ishlash natijasi:
```text
repr(C) struktura hajmi: 8 bayt
```

---

# 917-Topshiriq: #[repr(transparent)] yangi turlar uchun
## Topshiriq sharti:
Yagona maydondan iborat strukturani xotirada uning ichki turi bilan aynan bir xil qilish.
## Yechim (Rust kodi):
```rust
#[repr(transparent)]
struct FoydalanuvchiId(u64);

fn main() {
    println!("FoydalanuvchiId hajmi: {} bayt", std::mem::size_of::<FoydalanuvchiId>());
    assert_eq!(std::mem::size_of::<FoydalanuvchiId>(), std::mem::size_of::<u64>());
}
```
## Tushuntirish va Mantiq:
`#[repr(transparent)]` C-FFI orqali newtype wrapperlarni to'g'ridan-to'g'ri xavfsiz uzatish imkonini beradi.
## Ishlash natijasi:
```text
FoydalanuvchiId hajmi: 8 bayt
```

---

# 918-Topshiriq: C-FFI: extern "C" blokida C standart funksiyasini chaqirish
## Topshiriq sharti:
C standart kutubxonasidagi `abs` (modul) funksiyasini Rust'dan chaqiring.
## Yechim (Rust kodi):
```rust
extern "C" {
    fn abs(input: i32) -> i32;
}

fn main() {
    let son = -42;
    let modul = unsafe { abs(son) };
    println!("C abs({}) natijasi: {}", son, modul);
}
```
## Tushuntirish va Mantiq:
`extern "C"` bloki C ABI (Application Binary Interface) bo'yicha tashqi funksiyalar bilan bog'lanishni ta'minlaydi.
## Ishlash natijasi:
```text
C abs(-42) natijasi: 42
```

---

# 919-Topshiriq: Rust funksiyasini C uchun eksport qilish: #[no_mangle]
## Topshiriq sharti:
C yoki C++ dasturlari chaqira olishi uchun Rust funksiyasini eksport qilish sintaksisini ko'rsating.
## Yechim (Rust kodi):
```rust
#[no_mangle]
pub extern "C" fn qoshish(a: i32, b: i32) -> i32 {
    a + b
}

fn main() {
    let yigindi = qoshish(15, 25);
    println!("Eksport qilinadigan funksiya natijasi: {}", yigindi);
}
```
## Tushuntirish va Mantiq:
`#[no_mangle]` Rust kompilyatoriga funksiya nomini shifrlamaslikni (symbol mangling qilmaslikni) buyuradi, shunda C linker uni to'g'ridan-to'g'ri topa oladi.
## Ishlash natijasi:
```text
Eksport qilinadigan funksiya natijasi: 40
```

---

# 920-Topshiriq: std::ffi::CString bilan Rust satrini C satriga aylantirish
## Topshiriq sharti:
Rust `String`ini oxirida `\0` (null-terminator) bo'lgan C satriga aylantirish dasturi.
## Yechim (Rust kodi):
```rust
use std::ffi::CString;

fn main() {
    let matn = "Salom C tili!";
    let c_matn = CString::new(matn).expect("CString xatoligi");

    println!("C satri (baytlar): {:?}", c_matn.as_bytes_with_nul());
}
```
## Tushuntirish va Mantiq:
C tilida barcha satrlar 0x00 bayti bilan tugaydi. `CString` xavfsiz tarzda matn oxiriga nol baytini qo'shib beradi.
## Ishlash natijasi:
```text
C satri (baytlar): [83, 97, 108, 111, 109, 32, 67, 32, 116, 105, 108, 105, 33, 0]
```

---

# 921-Topshiriq: std::ffi::CStr bilan C satrini Rust &str ga o'girish
## Topshiriq sharti:
Nol bilan tugovchi ko'rsatkichdan Rust `&str` satrini xavfsiz qabul qilish.
## Yechim (Rust kodi):
```rust
use std::ffi::CStr;
use std::os::raw::c_char;

fn main() {
    let c_massiv: [c_char; 5] = [b'R' as c_char, b'u' as c_char, b's' as c_char, b't' as c_char, 0];
    let ptr = c_massiv.as_ptr();

    unsafe {
        let c_str = CStr::from_ptr(ptr);
        println!("Rust satriga o'girildi: {}", c_str.to_str().unwrap());
    }
}
```
## Tushuntirish va Mantiq:
`CStr::from_ptr` xotirada birinchi `\0` baytigacha o'qiydi va uni UTF-8 formatida Rust havolasiga aylantiradi.
## Ishlash natijasi:
```text
Rust satriga o'girildi: Rust
```

---

# 922-Topshiriq: C strukturasini Rust'da e'lon qilish va FFI orqali uzatish
## Topshiriq sharti:
C kutubxonalari bilan ma'lumot almashish uchun mos struktura yaratish.
## Yechim (Rust kodi):
```rust
#[repr(C)]
#[derive(Debug)]
struct Nuqta {
    x: f64,
    y: f64,
}

extern "C" fn nuqta_masofa(p: &Nuqta) -> f64 {
    (p.x * p.x + p.y * p.y).sqrt()
}

fn main() {
    let n = Nuqta { x: 3.0, y: 4.0 };
    let masofa = nuqta_masofa(&n);
    println!("Nuqtagacha masofa: {}", masofa);
}
```
## Tushuntirish va Mantiq:
`#[repr(C)]` tufayli `Nuqta` strukturasi xotirada C bilan to'liq mos keladi va ko'rsatkichlar orqali xavfsiz uzatiladi.
## Ishlash natijasi:
```text
Nuqtagacha masofa: 5
```

---

# 923-Topshiriq: Callback funksiyalari: Rust fn ko'rsatkichini uzatish
## Topshiriq sharti:
C kutubxonasi chaqirishi uchun Rust funksiya ko'rsatkichini (function pointer) callback sifatida uzating.
## Yechim (Rust kodi):
```rust
type CallbackFn = extern "C" fn(i32);

extern "C" fn mening_callback(qiymat: i32) {
    println!("C dan callback chaqirildi, qiymat: {}", qiymat);
}

fn hodisani_ishlat(cb: CallbackFn) {
    cb(100);
}

fn main() {
    hodisani_ishlat(mening_callback);
}
```
## Tushuntirish va Mantiq:
`extern "C" fn(...)` turlari C tili kutadigan standart ko'rsatkich formatiga to'liq mos keladi.
## Ishlash natijasi:
```text
C dan callback chaqirildi, qiymat: 100
```

---

# 924-Topshiriq: Opaque Pointers: Noaniq C obyektlarini boshqarish
## Topshiriq sharti:
C kutubxonasi tafsilotlarini yashirish uchun ishlatiladigan `*mut c_void` yoki noaniq strukturalar bilan ishlash.
## Yechim (Rust kodi):
```rust
enum OpaqueHandle {} // Bo'sh enum: Rust'da hech qachon to'g'ridan-to'g'ri yaratib bo'lmaydi

struct KutubxonaWrapper {
    tutqich: *mut OpaqueHandle,
}

fn main() {
    println!("Opaque pointerlar tashqi C resurslarini xavfsiz qobiq ichida saqlash uchun xizmat qiladi.");
}
```
## Tushuntirish va Mantiq:
Bo'sh enum (`enum Foo {}`) orqali yaratilgan pointerlar safe kodda xatolik bilan dereference qilinishining oldini oladi.
## Ishlash natijasi:
```text
Opaque pointerlar tashqi C resurslarini xavfsiz qobiq ichida saqlash uchun xizmat qiladi.
```

---

# 925-Topshiriq: std::mem::zeroed xotirani nollar bilan to'ldirish va uning xavfi
## Topshiriq sharti:
Xotirani nollashtirish qaysi tiplar uchun xavfli ekanligini tushuntiring.
## Yechim (Rust kodi):
```rust
use std::mem;

fn main() {
    // Integerlar uchun nollar xavfsiz:
    let son: u64 = unsafe { mem::zeroed() };
    println!("Nollashtirilgan son: {}", son);

    // DIQQAT: &T (havola) yoki NonNull<T> uchun zeroed chaqirish DARHOL UB beradi!
}
```
## Tushuntirish va Mantiq:
`mem::zeroed` barcha baytlarni 0 qiladi. Ammo Rust havolalari (`&T`) hech qachon 0 (null) bo'lolmasligi sababli, bu zudlik bilan Undefined Behavior keltirib chiqaradi.
## Ishlash natijasi:
```text
Nollashtirilgan son: 0
```

---

# 926-Topshiriq: Undefined Behavior (UB) nima va nima uchun halokatli
## Topshiriq sharti:
Kompilyator optimizatsiyalari va UB ning xavfli oqibatlari haqida tushuncha.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Undefined Behavior (UB) oqibatlari:");
    println!("1. Kompilyator qoidalar buzilgan deb hisoblab, kodning bir qismini butunlay o'chirib yuborishi mumkin.");
    println!("2. Xotira buzilishi (Memory corruption) va xavfsizlik zaifliklari (Exploits).");
    println!("3. Rust'ning barcha xavfsizlik kafolatlari yo'qoladi.");
}
```
## Tushuntirish va Mantiq:
Rust tilining bosh maqsadi - dasturda hech qanday sharoitda Undefined Behavior ro'y bermasligini kafolatlashdir.
## Ishlash natijasi:
```text
Undefined Behavior (UB) oqibatlari:
1. Kompilyator qoidalar buzilgan deb hisoblab, kodning bir qismini butunlay o'chirib yuborishi mumkin.
2. Xotira buzilishi (Memory corruption) va xavfsizlik zaifliklari (Exploits).
3. Rust'ning barcha xavfsizlik kafolatlari yo'qoladi.
```

---

# 927-Topshiriq: Dangling pointer (osilib qolgan ko'rsatkich) va oldini olish
## Topshiriq sharti:
Scope tugagach o'chib ketgan o'zgaruvchining manzilini saqlab qolish xatosi.
## Yechim (Rust kodi):
```rust
fn xavfli_manzil() -> *const i32 {
    let son = 42;
    &son as *const i32 // XATO: son funksiya tugashi bilan yo'q bo'ladi!
}

fn main() {
    let ptr = xavfli_manzil();
    println!("Osilib qolgan pointer olindi: {:p} (Uni dereference qilish qat'iyan man etiladi!)", ptr);
}
```
## Tushuntirish va Mantiq:
Stackdagi o'zgaruvchi xotiradan o'chgandan keyin uning xom manziliga murojaat qilish o'qish xatolariga olib keladi.
## Ishlash natijasi:
```text
Osilib qolgan pointer olindi: 0x... (Uni dereference qilish qat'iyan man etiladi!)
```

---

# 928-Topshiriq: Use-After-Free (UAF) va Double Free tushunchalari
## Topshiriq sharti:
Xotira bo'shatilgandan keyin murojaat qilish va ikki marta drop qilish muammolari.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("C tilidagi asosiy xotira xatolari:");
    println!("- Use-After-Free: free() qilingan xotirani qayta o'qish/yozish.");
    println!("- Double Free: Bitta xotira blokini ikki marta ketma-ket tozalash.");
    println!("Rust'ning Ownership va Borrowing tizimi ushbu xatolarni safe kodda butunlay imkonsiz qiladi.");
}
```
## Tushuntirish va Mantiq:
Rust xavfsiz kodda UAF va Double Free xatolarini kompilyatsiya bosqichidayoq to'xtatadi.
## Ishlash natijasi:
```text
C tilidagi asosiy xotira xatolari:
- Use-After-Free: free() qilingan xotirani qayta o'qish/yozish.
- Double Free: Bitta xotira blokini ikki marta ketma-ket tozalash.
Rust'ning Ownership va Borrowing tizimi ushbu xatolarni safe kodda butunlay imkonsiz qiladi.
```

---

# 929-Topshiriq: std::ptr::read_unaligned va write_unaligned
## Topshiriq sharti:
Xotirada to'g'ri tekislanmagan (unaligned) baytlardan xavfsiz qiymat o'qish.
## Yechim (Rust kodi):
```rust
use std::ptr;

fn main() {
    let baytlar = [0x00, 0x12, 0x34, 0x56, 0x78];
    // 1-indeksdagi toq bayt manzilidan u32 o'qish:
    let ptr = unsafe { baytlar.as_ptr().add(1) as *const u32 };

    let son = unsafe { ptr::read_unaligned(ptr) };
    println!("Tekislanmagan xotiradan o'qilgan son: 0x{:X}", son);
}
```
## Tushuntirish va Mantiq:
Oddiy dereference (`*ptr`) ko'rsatkichning hizalangan bo'lishini (masalan, 4 ga karrali) talab qiladi. Hizalanmagan bo'lsa `read_unaligned` ishlatiladi.
## Ishlash natijasi:
```text
Tekislanmagan xotiradan o'qilgan son: 0x78563412
```

---

# 930-Topshiriq: Inline Assembly: asm! makrosi bilan CPU ko'rsatmalarini bajarish
## Topshiriq sharti:
Rust kodining ichida to'g'ridan-to'g'ri assembler instruksiyasini (masalan, NOP) bajarish.
## Yechim (Rust kodi):
```rust
use std::arch::asm;

fn main() {
    println!("Assembler instruksiyasi bajarilmoqda...");
    unsafe {
        asm!("nop"); // No Operation: hech narsa qilmaydi
    }
    println!("NOP bajarildi.");
}
```
## Tushuntirish va Mantiq:
`asm!` makrosi orqali eng pastki apparat instruksiyalarini (portlar, maxsus CPU bayroqlari) to'g'ridan-to'g'ri chaqirish mumkin.
## Ishlash natijasi:
```text
Assembler instruksiyasi bajarilmoqda...
NOP bajarildi.
```

---

# 931-Topshiriq: asm! orqali CPU registrlaridan ma'lumot olish
## Topshiriq sharti:
Assembler registrlari bilan ma'lumot almashish (in va out operandlari).
## Yechim (Rust kodi):
```rust
use std::arch::asm;

fn main() {
    let mut x: u64 = 10;
    unsafe {
        asm!(
            "add {0}, 5",
            inout(reg) x,
        );
    }
    println!("Asm orqali 5 qo'shildi: {}", x);
}
```
## Tushuntirish va Mantiq:
`inout(reg)` kompilyatorga o'zgaruvchini bo'sh CPU registriga joylab, asm blokidan keyin qaytarib olishni aytadi.
## Ishlash natijasi:
```text
Asm orqali 5 qo'shildi: 15
```

---

# 932-Topshiriq: Volatile Memory: read_volatile va write_volatile
## Topshiriq sharti:
Kompilyator optimizatsiyasi o'chirib yubormasligi kerak bo'lgan xotira operatsiyalari (MMIO).
## Yechim (Rust kodi):
```rust
use std::ptr;

fn main() {
    let mut apparat_registr: u32 = 0;
    let ptr = &mut apparat_registr as *mut u32;

    unsafe {
        ptr::write_volatile(ptr, 1);
        let qiymat = ptr::read_volatile(ptr);
        println!("Volatile o'qilgan qiymat: {}", qiymat);
    }
}
```
## Tushuntirish va Mantiq:
Volatile amallar drayverlar va apparat registrlari (MMIO) bilan ishlashda kompilyatorning o'qish/yozishni keshlab olishining oldini oladi.
## Ishlash natijasi:
```text
Volatile o'qilgan qiymat: 1
```

---

# 933-Topshiriq: UnsafeCell<T>: Ichki o'zgaruvchanlikning (Interior Mutability) yagona asosi
## Topshiriq sharti:
`RefCell` va `Mutex` larning asosi bo'lgan `UnsafeCell` qanday ishlashini ko'rsating.
## Yechim (Rust kodi):
```rust
use std::cell::UnsafeCell;

fn main() {
    let cell = UnsafeCell::new(100);

    unsafe {
        let ptr = cell.get();
        *ptr += 50;
        println!("UnsafeCell ichidagi qiymat: {}", *cell.get());
    }
}
```
## Tushuntirish va Mantiq:
`UnsafeCell<T>` Rust'da immutable havola ichidagi ma'lumotni qonuniy ravishda o'zgartirishga ruxsat beruvchi yagona primitivdir.
## Ishlash natijasi:
```text
UnsafeCell ichidagi qiymat: 150
```

---

# 934-Topshiriq: SIMD intrinzikalari: Vektorli amallar asoslari
## Topshiriq sharti:
Protsessorning SIMD (Single Instruction, Multiple Data) imkoniyatlaridan foydalanish tushunchasi.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("SIMD (Apparat Vektorizatsiyasi):");
    println!("- 1 ta CPU instruksiyasi bilan bir vaqtda 4, 8 yoki 16 ta sonni qo'shish/ko'paytirish.");
    println!("- AVX2, AVX-512, ARM NEON qo'llab-quvvatlanadi.");
    println!("- Rust'da `std::arch` moduli orqali chaqiriladi.");
}
```
## Tushuntirish va Mantiq:
SIMD sun'iy intellekt, matrisalarni ko'paytirish va grafik ishlov berishda hisoblash tezligini 4-8 baravar oshiradi.
## Ishlash natijasi:
```text
SIMD (Apparat Vektorizatsiyasi):
- 1 ta CPU instruksiyasi bilan bir vaqtda 4, 8 yoki 16 ta sonni qo'shish/ko'paytirish.
- AVX2, AVX-512, ARM NEON qo'llab-quvvatlanadi.
- Rust'da `std::arch` moduli orqali chaqiriladi.
```

---

# 935-Topshiriq: Miri (Rust Undefined Behavior detector) qanday ishlaydi
## Topshiriq sharti:
Rust kodingizda xotira xatolari va UB bor-yo'qligini tekshiruvchi Miri vositasi.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Miri vositasi:");
    println!("- Rust dasturini oraliq IR darajasida interpretatsiya qiladi.");
    println!("- Stacked Borrows qoidalarini, xotira sizib chiqishini va UB larni aniqlaydi.");
    println!("- Buyruq: `cargo miri test`");
}
```
## Tushuntirish va Mantiq:
Miri har qanday Unsafe Rust kutubxonasini tekshirish uchun rasmiy va eng ishonchli vositadir.
## Ishlash natijasi:
```text
Miri vositasi:
- Rust dasturini oraliq IR darajasida interpretatsiya qiladi.
- Stacked Borrows qoidalarini, xotira sizib chiqishini va UB larni aniqlaydi.
- Buyruq: `cargo miri test`
```

---

# 936-Topshiriq: Stacked Borrows va Tree Borrows modellari
## Topshiriq sharti:
Rust'da bir nechta pointerlar bitta xotiraga murojaat qilganda ularning ustunlik iyerarxiyasi.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Stacked Borrows qoidasi:");
    println!("- Har bir pointer xotiraga kirish ruxsatnomasi stekiga (stack) ega.");
    println!("- Agar eski pointer ustidan yangi pointer o'qilsa, stekdagi tartib saqlanishi kerak.");
    println!("- Qoidalarni buzish kompilyator optimizatsiyalarining noto'g'ri ishlashiga olib keladi.");
}
```
## Tushuntirish va Mantiq:
Ushbu modellar Unsafe Rust qachon qonuniy va qachon noqonuniy ekanligini matematik jihatdan belgilaydi.
## Ishlash natijasi:
```text
Stacked Borrows qoidasi:
- Har bir pointer xotiraga kirish ruxsatnomasi stekiga (stack) ega.
- Agar eski pointer ustidan yangi pointer o'qilsa, stekdagi tartib saqlanishi kerak.
- Qoidalarni buzish kompilyator optimizatsiyalarining noto'g'ri ishlashiga olib keladi.
```

---

# 937-Topshiriq: FFI xatoliklarini qayta ishlash: errno bilan ishlash
## Topshiriq sharti:
C funksiyalari qaytargan xatolik kodlarini (errno) o'qish usuli.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("FFI errno boshqaruvi:");
    println!("- C funksiyasi odatda muvaffaqiyatsizlikda -1 yoki NULL qaytaradi.");
    println!("- Xato sababini aniqlash uchun `std::io::Error::last_os_error()` chaqiriladi.");
}
```
## Tushuntirish va Mantiq:
Rust'dagi `io::Error::last_os_error()` operatsion tizimning joriy oqimidagi oxirgi xatolik kodini avtomatik xabarga o'giradi.
## Ishlash natijasi:
```text
FFI errno boshqaruvi:
- C funksiyasi odatda muvaffaqiyatsizlikda -1 yoki NULL qaytaradi.
- Xato sababini aniqlash uchun `std::io::Error::last_os_error()` chaqiriladi.
```

---

# 938-Topshiriq: Dinamik kutubxonalarni yuklash (dlopen / LoadLibrary)
## Topshiriq sharti:
Dastur ishlayotgan vaqtda `.so` yoki `.dll` kutubxonasini xotiraga dinamik yuklash tushunchasi.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Dinamik kutubxona yuklash:");
    println!("- Rust'da `libloading` kutubxonasi orqali amalga oshiriladi.");
    println!("- Plugin tizimlari va plaginlarni qayta ishga tushirmasdan yuklash uchun xizmat qiladi.");
}
```
## Tushuntirish va Mantiq:
Dinamik bog'lanish dastur hajmini kichik saqlash va modullarni mustaqil yangilash imkonini beradi.
## Ishlash natijasi:
```text
Dinamik kutubxona yuklash:
- Rust'da `libloading` kutubxonasi orqali amalga oshiriladi.
- Plugin tizimlari va plaginlarni qayta ishga tushirmasdan yuklash uchun xizmat qiladi.
```

---

# 939-Topshiriq: OS Signallarini (SIGINT, SIGTERM) ushlashda Unsafe qoidalar
## Topshiriq sharti:
Signal handlerlar ichida nima uchun oddiy allokatsiya va mutex ishlatish taqiqlanganligi.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Signal Handler xavfsizligi:");
    println!("- Handler har qanday kutilmagan vaqtda asosiy kodni uzib qo'yadi.");
    println!("- Handler ichida faqat Asynchronous-Signal-Safe funksiyalar (masalan, atomik bayroqni o'zgartirish) chaqirilishi mumkin.");
}
```
## Tushuntirish va Mantiq:
Signal ichida Mutex qulflashga urinish zudlik bilan Deadlock keltirib chiqarishi mumkin.
## Ishlash natijasi:
```text
Signal Handler xavfsizligi:
- Handler har qanday kutilmagan vaqtda asosiy kodni uzib qo'yadi.
- Handler ichida faqat Asynchronous-Signal-Safe funksiyalar (masalan, atomik bayroqni o'zgartirish) chaqirilishi mumkin.
```

---

# 940-Topshiriq: Bit-Packing: Kichik maydonlarni bitta integerda saqlash
## Topshiriq sharti:
Bir nechta bayroqlarni bitwise siljitish orqali bitta bayt ichida ixcham saqlash.
## Yechim (Rust kodi):
```rust
struct Bayroqlar(u8);

impl Bayroqlar {
    const OQISH: u8 = 1 << 0;  // 0001
    const YOZISH: u8 = 1 << 1; // 0010
    const IJRO: u8 = 1 << 2;   // 0100

    fn yangi() -> Self { Bayroqlar(0) }
    fn qoshish(&mut self, b: u8) { self.0 |= b; }
    fn bormi(&self, b: u8) -> bool { (self.0 & b) != 0 }
}

fn main() {
    let mut b = Bayroqlar::yangi();
    b.qoshish(Bayroqlar::OQISH);
    b.qoshish(Bayroqlar::IJRO);

    println!("O'qish ruxsati: {}", b.bormi(Bayroqlar::OQISH));
    println!("Yozish ruxsati: {}", b.bormi(Bayroqlar::YOZISH));
    println!("Ijro ruxsati:   {}", b.bormi(Bayroqlar::IJRO));
}
```
## Tushuntirish va Mantiq:
Bit-packing xotirani tejaydi va apparat drayverlari bilan to'g'ridan-to'g'ri muloqot qilish imkonini beradi.
## Ishlash natijasi:
```text
O'qish ruxsati: true
Yozish ruxsati: false
Ijro ruxsati:   true
```

---

# 941-Topshiriq: Custom Vec prototipi: Xom xotira ajratish va sig'im
## Topshiriq sharti:
Standart kutubxonaning `Vec` strukturasiga o'xshash xom xotira ajratuvchi sodda struktura.
## Yechim (Rust kodi):
```rust
use std::alloc::{alloc, dealloc, realloc, Layout};

struct XomVektor {
    ptr: *mut i32,
    sigim: usize,
    uzunlik: usize,
}

impl XomVektor {
    fn yangi() -> Self {
        XomVektor { ptr: std::ptr::null_mut(), sigim: 0, uzunlik: 0 }
    }

    fn qoshish(&mut self, son: i32) {
        if self.sigim == 0 {
            let layout = Layout::array::<i32>(2).unwrap();
            self.ptr = unsafe { alloc(layout) as *mut i32 };
            self.sigim = 2;
        } else if self.uzunlik == self.sigim {
            let yangi_sigim = self.sigim * 2;
            let eski_layout = Layout::array::<i32>(self.sigim).unwrap();
            self.ptr = unsafe { realloc(self.ptr as *mut u8, eski_layout, yangi_sigim * 4) as *mut i32 };
            self.sigim = yangi_sigim;
        }

        unsafe {
            std::ptr::write(self.ptr.add(self.uzunlik), son);
        }
        self.uzunlik += 1;
    }
}

impl Drop for XomVektor {
    fn drop(&mut self) {
        if self.sigim > 0 {
            let layout = Layout::array::<i32>(self.sigim).unwrap();
            unsafe { dealloc(self.ptr as *mut u8, layout); }
            println!("XomVektor xotirasi ozod qilindi.");
        }
    }
}

fn main() {
    let mut v = XomVektor::yangi();
    v.qoshish(10);
    v.qoshish(20);
    v.qoshish(30);

    println!("Vektor uzunligi: {}, Sig'imi: {}", v.uzunlik, v.sigim);
}
```
## Tushuntirish va Mantiq:
`alloc`, `realloc` va `dealloc` yordamida o'z dinamik ma'lumotlar tuzilmalaringizni noldan qurish mumkin.
## Ishlash natijasi:
```text
Vektor uzunligi: 3, Sig'imi: 4
XomVektor xotirasi ozod qilindi.
```

---

# 942-Topshiriq: C kutubxonasidagi qator uzunligini hisoblash (strlen)
## Topshiriq sharti:
Nol bilan tugovchi ko'rsatkichning uzunligini sanovchi unsafe funksiya yozing.
## Yechim (Rust kodi):
```rust
unsafe fn mening_strlen(mut ptr: *const u8) -> usize {
    let mut len = 0;
    while *ptr != 0 {
        len += 1;
        ptr = ptr.add(1);
    }
    len
}

fn main() {
    let satr = b"Rust 2024\0";
    let uzunlik = unsafe { mening_strlen(satr.as_ptr()) };
    println!("Satr uzunligi: {}", uzunlik);
}
```
## Tushuntirish va Mantiq:
C tilidagi `strlen` aynan shunday xotira bo'ylab to birinchi `0` bayti uchraguncha ko'rsatkichni siljitib ishlaydi.
## Ishlash natijasi:
```text
Satr uzunligi: 9
```

---

# 943-Topshiriq: Xotira ko'chirish: memmove analogi
## Topshiriq sharti:
Ustma-ust tushishi mumkin bo'lgan (overlapping) xotirani xavfsiz ko'chirish.
## Yechim (Rust kodi):
```rust
use std::ptr;

fn main() {
    let mut massiv = [1, 2, 3, 4, 5];
    let ptr = massiv.as_mut_ptr();

    unsafe {
        // [1, 2, 3] ni 1 qadam o'ngga suramiz -> [1, 1, 2, 3, 5]
        ptr::copy(ptr, ptr.add(1), 3);
    }

    println!("Siljitilgan massiv: {:?}", massiv);
}
```
## Tushuntirish va Mantiq:
`ptr::copy` manba va maqsad xotira bloklari bir-birining ustiga tushgan holatda ham buzilishsiz nusxalashni kafolatlaydi (C'dagi `memmove`).
## Ishlash natijasi:
```text
Siljitilgan massiv: [1, 1, 2, 3, 5]
```

---

# 944-Topshiriq: Binar baytlarni float f32 ga to'g'ridan-to'g'ri o'girish
## Topshiriq sharti:
IEEE-754 standarti bo'yicha 4 ta baytni `f32` suzuvchi nuqtali songa o'girish.
## Yechim (Rust kodi):
```rust
fn main() {
    let baytlar: [u8; 4] = [0x00, 0x00, 0x80, 0x3F]; // 1.0f32 IEEE-754

    let son = f32::from_le_bytes(baytlar);
    println!("Qayta tiklangan float: {}", son);
}
```
## Tushuntirish va Mantiq:
Tarmoqdan kelgan baytlarni matematik sonlarga aylantirishda `from_le_bytes` va `from_be_bytes` eng xavfsiz va tez vositadir.
## Ishlash natijasi:
```text
Qayta tiklangan float: 1
```

---

# 945-Topshiriq: Fat Pointer ichki tuzilishi: Data pointer va VTable
## Topshiriq sharti:
Trait ob'ektlarining xotiradagi 2 ta pointerdan iborat ekanligini ko'rsatish.
## Yechim (Rust kodi):
```rust
use std::mem::transmute;

trait SinovTrait {
    fn salom(&self);
}

struct Ob;
impl SinovTrait for Ob {
    fn salom(&self) { println!("Salom!"); }
}

#[repr(C)]
struct TraitObjectFatPointer {
    data_ptr: *const (),
    vtable_ptr: *const (),
}

fn main() {
    let ob = Ob;
    let trait_ref: &dyn SinovTrait = &ob;

    let fat: TraitObjectFatPointer = unsafe { transmute(trait_ref) };
    println!("Ma'lumot manzili: {:p}", fat.data_ptr);
    println!("VTable manzili:   {:p}", fat.vtable_ptr);
}
```
## Tushuntirish va Mantiq:
Rust trait ob'ektlari (fat pointer) 16 bayt bo'lib, biri struktura manzilini, ikkinchisi virtual metodlar jadvalini (vtable) ko'rsatadi.
## Ishlash natijasi:
```text
Ma'lumot manzili: 0x...
VTable manzili:   0x...
```

---

# 946-Topshiriq: Slice Fat Pointer: Manzil va Uzunlik
## Topshiriq sharti:
`&[T]` slice'ining xotiradagi 2 ta usize hajmli (manzil + uzunlik) ko'rsatkichini tahlil qilish.
## Yechim (Rust kodi):
```rust
use std::mem::transmute;

#[repr(C)]
struct SliceFatPointer {
    ptr: *const i32,
    len: usize,
}

fn main() {
    let massiv = [10, 20, 30, 40];
    let slice: &[i32] = &massiv[..];

    let fat: SliceFatPointer = unsafe { transmute(slice) };
    println!("Slice manzili: {:p}, Uzunligi: {}", fat.ptr, fat.len);
    assert_eq!(fat.len, 4);
}
```
## Tushuntirish va Mantiq:
Rust slice'lari xotirada shunchaki `(boshlang'ich_manzil, elementlar_soni)` juftligidan iborat ixcham strukturadir.
## Ishlash natijasi:
```text
Slice manzili: 0x..., Uzunligi: 4
```

---

# 947-Topshiriq: Xom xotirani to'g'ri hizalash (Align to)
## Topshiriq sharti:
Xotira manzilini 16 baytlik yoki 64 baytlik chegaraga hizalash hisobi.
## Yechim (Rust kodi):
```rust
fn hizala(manzil: usize, hizalanish: usize) -> usize {
    (manzil + hizalanish - 1) & !(hizalanish - 1)
}

fn main() {
    let manzil = 1005;
    let hizalangan = hizala(manzil, 16);
    println!("{} manzili 16 ga hizalandi: {} (qoldiq: {})", manzil, hizalangan, hizalangan % 16);
    assert_eq!(hizalangan % 16, 0);
}
```
## Tushuntirish va Mantiq:
SIMD va GPU operatsiyalari xotiraning 16, 32 yoki 64 baytga karrali manzillarda joylashgan bo'lishini talab qiladi.
## Ishlash natijasi:
```text
1005 manzili 16 ga hizalandi: 1008 (qoldiq: 0)
```

---

# 948-Topshiriq: Memory Leakni atayin amalga oshirish: Box::into_raw
## Topshiriq sharti:
`Box` egaligini bekor qilib xom ko'rsatkichga aylantirish va xotirani qo'lda boshqarish.
## Yechim (Rust kodi):
```rust
fn main() {
    let x = Box::new(999);

    // Box::into_raw xotirani drop qilmaydi, xom pointer beradi
    let raw: *mut i32 = Box::into_raw(x);

    unsafe {
        println!("Qo'lda boshqarilayotgan qiymat: {}", *raw);
        // Xotirani qaytarib Box'ga olib tozalaymiz
        let _ = Box::from_raw(raw);
    }
    println!("Xotira xavfsiz tarzda tozalab olindi.");
}
```
## Tushuntirish va Mantiq:
`Box::into_raw` va `Box::from_raw` C-FFI ga ma'lumot uzatish va qaytarib olishda eng ommabop usuldir.
## Ishlash natijasi:
```text
Qo'lda boshqarilayotgan qiymat: 999
Xotira xavfsiz tarzda tozalab olindi.
```

---

# 949-Topshiriq: Apparat ko'rsatmalari: CPU Time-Stamp Counter (RDTSC)
## Topshiriq sharti:
Protsessorning taktlar sonini o'lchovchi apparat taymerini chaqirish tushunchasi.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("RDTSC (Read Time-Stamp Counter):");
    println!("- CPU ishga tushgandan buyon sanagan barcha taktlar (cycles) sonini o'qiydi.");
    println!("- Nanosekund darajasidagi o'ta aniq benchmarklar uchun qo'llaniladi.");
}
```
## Tushuntirish va Mantiq:
Standart operatsion tizim taymerlaridan ko'ra taktlar soni bo'yicha algoritmlar samaradorligini o'lchash ancha aniqdir.
## Ishlash natijasi:
```text
RDTSC (Read Time-Stamp Counter):
- CPU ishga tushgandan buyon sanagan barcha taktlar (cycles) sonini o'qiydi.
- Nanosekund darajasidagi o'ta aniq benchmarklar uchun qo'llaniladi.
```

---

# 950-Topshiriq: Unsafe Rust Integratsion Loyihasi: Xavfsiz C-Bufer qobig'i
## Topshiriq sharti:
Pastki darajadagi xom xotirani xavfsiz boshqaruvchi to'liq RAII `XavfsizBufer` strukturasini yarating.
## Yechim (Rust kodi):
```rust
use std::alloc::{alloc, dealloc, Layout};

pub struct XavfsizBufer {
    ptr: *mut u8,
    layout: Layout,
    sigim: usize,
}

impl XavfsizBufer {
    pub fn yangi(sigim: usize) -> Self {
        assert!(sigim > 0, "Sig'im noldan katta bo'lishi shart");
        let layout = Layout::array::<u8>(sigim).expect("Noto'g'ri layout");
        let ptr = unsafe { alloc(layout) };
        if ptr.is_null() {
            panic!("Xotira ajratib bo'lmadi (OOM)");
        }
        XavfsizBufer { ptr, layout, sigim }
    }

    pub fn yozish(&mut self, indeks: usize, qiymat: u8) {
        assert!(indeks < self.sigim, "Indeks chegaradan tashqarida!");
        unsafe {
            *self.ptr.add(indeks) = qiymat;
        }
    }

    pub fn oqish(&self, indeks: usize) -> u8 {
        assert!(indeks < self.sigim, "Indeks chegaradan tashqarida!");
        unsafe {
            *self.ptr.add(indeks)
        }
    }
}

impl Drop for XavfsizBufer {
    fn drop(&mut self) {
        unsafe {
            dealloc(self.ptr, self.layout);
        }
        println!("XavfsizBufer: Xotira xavfsiz bo'shatildi.");
    }
}

fn main() {
    let mut bufer = XavfsizBufer::yangi(4);
    bufer.yozish(0, b'R');
    bufer.yozish(1, b'u');
    bufer.yozish(2, b's');
    bufer.yozish(3, b't');

    println!("Bufer tarkibi: {}{}{}{}",
        bufer.oqish(0) as char,
        bufer.oqish(1) as char,
        bufer.oqish(2) as char,
        bufer.oqish(3) as char
    );
}
```
## Tushuntirish va Mantiq:
`XavfsizBufer` unsafe xotira ajratishni o'z ichiga olsa-da, tashqi foydalanuvchiga 100% xavfsiz (indekslar tekshiriladigan va avtomatik tozalanadigan) interfeys taqdim etadi.
## Ishlash natijasi:
```text
Bufer tarkibi: Rust
XavfsizBufer: Xotira xavfsiz bo'shatildi.
```

---
