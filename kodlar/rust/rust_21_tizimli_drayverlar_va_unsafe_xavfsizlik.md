Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. Rust ekotizimini chuqur o'rganish va tizimli dasturlash ko'nikmalarini oshirish uchun mo'ljallangan 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1001-Topshiriq: Unsafe blokida xotira xavfsizligini boshqarish

## Topshiriq sharti:
`unsafe` blokidan foydalanib, xom ko'rsatkich (raw pointer) orqali xotiradagi qiymatni o'zgartiring va uning xavfsizligini ta'minlang.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut num = 10;
    let ptr = &mut num as *mut i32;

    unsafe {
        *ptr += 20;
        println!("O'zgartirilgan qiymat: {}", *ptr);
    }
}
```

## Tushuntirish va Mantiq:
`*mut i32` raw pointer yaratildi. `unsafe` bloki ichida xotira manziliga to'g'ridan-to'g'ri murojaat qilib, qiymatni 20 ga oshirdik. Bu operatsiya Rust kompilyatori tomonidan tekshirilmaydi, shuning uchun xavfsizlik dasturchi zimmasida.

## Ishlash natijasi:
```text
O'zgartirilgan qiymat: 30
```

---

# 1002-Topshiriq: OS darajasidagi xotira xaritasi (Memory Mapping)

## Topshiriq sharti:
`libc` kutubxonasi yordamida operatsion tizim darajasida xotira ajratish (mmap) simulyatsiyasini bajaring.

## Yechim (Rust kodi):
```rust
fn main() {
    let size = 1024;
    // Oddiylik uchun xotira ajratishni simulyatsiya qilamiz
    let buffer: Vec<u8> = Vec::with_capacity(size);
    println!("OS darajasida {} bayt xotira ajratishga tayyor.", buffer.capacity());
}
```

## Tushuntirish va Mantiq:
OS drayverlari va past darajali tizimlar xotirani `mmap` orqali boshqaradi. Bu kod `Vec` orqali xotira ajratishning yuqori darajali abstraktsiyasini ko'rsatadi, bu esa xavfsiz xotira boshqaruvini ta'minlaydi.

## Ishlash natijasi:
```text
OS darajasida 1024 bayt xotira ajratishga tayyor.
```

---

# 1003-Topshiriq: Nol xarajatli abstraktsiya (Zero-cost Abstraction)

## Topshiriq sharti:
`Iterator` traitidan foydalanib, `map` va `filter` yordamida nol xarajatli abstraktsiyani namoyish eting.

## Yechim (Rust kodi):
```rust
fn main() {
    let nums = vec![1, 2, 3, 4, 5];
    let sum: i32 = nums.iter().filter(|&&x| x % 2 != 0).map(|&x| x * 2).sum();
    println!("Natija: {}", sum);
}
```

## Tushuntirish va Mantiq:
Rust'da `Iterator` zanjirlari kompilyatsiya vaqtida optimallashtiriladi va oddiy `for` sikli kabi tez ishlaydi. Bu "nol xarajatli abstraktsiya" tamoyilidir.

## Ishlash natijasi:
```text
Natija: 18
```

---

# 1004-Topshiriq: FFI (Foreign Function Interface) orqali C funksiyasini chaqirish

## Topshiriq sharti:
Rust kodidan `libc` kutubxonasidagi `puts` funksiyasini chaqiring.

## Yechim (Rust kodi):
```rust
use std::ffi::CString;
use std::os::raw::c_char;

extern "C" {
    fn puts(s: *const c_char) -> i32;
}

fn main() {
    let c_str = CString::new("Salom, Khorazmiy AI!").unwrap();
    unsafe {
        puts(c_str.as_ptr());
    }
}
```

## Tushuntirish va Mantiq:
`extern "C"` bloki orqali C tilidagi funksiyalar Rust'ga import qilinadi. `CString` Rust stringini C formatiga (null-terminated) o'tkazib beradi.

## Ishlash natijasi:
```text
Salom, Khorazmiy AI!
```

---

# 1005-Topshiriq: Union turlari va xotira nazorati

## Topshiriq sharti:
`union` yordamida bir xil xotira manzilida turli ma'lumot turlarini saqlashni ko'rsating.

## Yechim (Rust kodi):
```rust
union MyUnion {
    i: i32,
    f: f32,
}

fn main() {
    let u = MyUnion { i: 42 };
    unsafe {
        println!("Union qiymati: {}", u.i);
    }
}
```

## Tushuntirish va Mantiq:
`union` xotirani tejash uchun ishlatiladi. Undagi barcha maydonlar bir xil xotira manzilini egallaydi. `unsafe` blokisiz unga murojaat qilib bo'lmaydi.

## Ishlash natijasi:
```text
Union qiymati: 42
```

---

# 1006-Topshiriq: Volatile xotira operatsiyalari

## Topshiriq sharti:
`std::ptr::write_volatile` yordamida kompilyator optimallashtirishini chetlab o'tib, xotiraga yozing.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut x = 0;
    unsafe {
        std::ptr::write_volatile(&mut x, 100);
    }
    println!("Volatile qiymat: {}", x);
}
```

## Tushuntirish va Mantiq:
`write_volatile` drayverlar yozishda muhim, chunki u kompilyatorga bu xotira manzilini "o'zgaruvchan" deb belgilaydi va uni optimallashtirib tashlamaydi.

## Ishlash natijasi:
```text
Volatile qiymat: 100
```

---

# 1007-Topshiriq: Trait Object va Dinamik Dispatch

## Topshiriq sharti:
`dyn` kalit so'zi yordamida polimorfizmni amalga oshiring.

## Yechim (Rust kodi):
```rust
trait Driver { fn load(&self); }
struct Disk;
impl Driver for Disk { fn load(&self) { println!("Disk drayveri yuklandi."); } }

fn main() {
    let d: Box<dyn Driver> = Box::new(Disk);
    d.load();
}
```

## Tushuntirish va Mantiq:
`dyn Driver` dinamik dispatchni anglatadi. Bu dastur ishlayotgan vaqtda qaysi funksiya chaqirilishini aniqlaydi, bu esa moslashuvchan tizimlar uchun muhim.

## Ishlash natijasi:
```text
Disk drayveri yuklandi.
```

---

# 1008-Topshiriq: Xotira xavfsizligi (Ownership)

## Topshiriq sharti:
`Box` yordamida xotirani heap'da boshqarish va ownership ko'chishini ko'rsating.

## Yechim (Rust kodi):
```rust
fn main() {
    let b = Box::new(10);
    let c = b; // Ownership ko'chdi
    println!("Qiymat: {}", c);
}
```

## Tushuntirish va Mantiq:
Rust'ning asosiy xususiyati — ownership. `b` dan `c` ga o'tishda xotira qayta ajratilmaydi, faqat ko'rsatkich egasi o'zgaradi.

## Ishlash natijasi:
```text
Qiymat: 10
```

---

# 1009-Topshiriq: Inline Assembly (Asm)

## Topshiriq sharti:
`asm!` makrosi yordamida oddiy assembly kodini bajaring.

## Yechim (Rust kodi):
```rust
use std::arch::asm;

fn main() {
    let x: u64;
    unsafe {
        asm!("mov {}, 5", out(reg) x);
    }
    println!("Assembly orqali olingan qiymat: {}", x);
}
```

## Tushuntirish va Mantiq:
`asm!` makrosi to'g'ridan-to'g'ri CPU instruksiyalarini yozishga imkon beradi. Bu drayverlar va past darajali tizim dasturlashda juda muhim.

## Ishlash natijasi:
```text
Assembly orqali olingan qiymat: 5
```

---

# 1010-Topshiriq: Send va Sync traitlari

## Topshiriq sharti:
`Send` traitini tushunish uchun threadlar o'rtasida ma'lumot uzatishni ko'rsating.

## Yechim (Rust kodi):
```rust
use std::thread;

fn main() {
    let data = vec![1, 2, 3];
    let handle = thread::spawn(move || {
        println!("Thread ichida: {:?}", data);
    });
    handle.join().unwrap();
}
```

## Tushuntirish va Mantiq:
`move` kalit so'zi `data` ownershipini threadga o'tkazadi. `Send` traitiga ega bo'lgan turlar threadlar o'rtasida xavfsiz ko'chirilishi mumkin.

## Ishlash natijasi:
```text
Thread ichida: [1, 2, 3]
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. Rust dasturlash tilining tizimli dasturlashdagi imkoniyatlarini ochib beruvchi, xotira xavfsizligi va yuqori unumdorlikka qaratilgan 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1011-Topshiriq: Raw Pointer (Xom ko'rsatkich) bilan xavfsiz ishlash

## Topshiriq sharti:
`unsafe` blokidan foydalanib, xom ko'rsatkich (raw pointer) orqali qiymatni o'qish va uni xavfsiz Rust referensiyasiga aylantirish funksiyasini yozing.

## Yechim (Rust kodi):
```rust
fn main() {
    let data = 42;
    let ptr = &data as *const i32;

    unsafe {
        if !ptr.is_null() {
            let val = *ptr;
            println!("Xom ko'rsatkichdagi qiymat: {}", val);
        }
    }
}
```

## Tushuntirish va Mantiq:
`*const i32` bu xom ko'rsatkichdir. `unsafe` bloki Rust kompilyatoriga biz xotira xavfsizligini o'z zimmamizga olayotganimizni bildiradi. `*ptr` operatsiyasi ko'rsatkich ko'rsatayotgan manzilni dereference qiladi.

## Ishlash natijasi:
```text
Xom ko'rsatkichdagi qiymat: 42
```

---

# 1012-Topshiriq: FFI orqali C funksiyasini chaqirish

## Topshiriq sharti:
Rust dasturidan standart C kutubxonasining `abs()` funksiyasini FFI (Foreign Function Interface) orqali chaqiring.

## Yechim (Rust kodi):
```rust
extern "C" {
    fn abs(input: i32) -> i32;
}

fn main() {
    unsafe {
        let n = -10;
        println!("{} ning absolyut qiymati: {}", n, abs(n));
    }
}
```

## Tushuntirish va Mantiq:
`extern "C"` bloki tashqi C funksiyalarini e'lon qilish uchun ishlatiladi. Bu Rust va C o'rtasidagi ABI (Application Binary Interface) mosligini ta'minlaydi.

## Ishlash natijasi:
```text
-10 ning absolyut qiymati: 10
```

---

# 1013-Topshiriq: Nol xarajatli abstraktsiya (Trait va Inline)

## Topshiriq sharti:
`#[inline]` atributidan foydalanib, kichik funksiyani kompilyatsiya vaqtida optimallashtirish va trait yordamida polimorfizmni nol xarajat bilan amalga oshiring.

## Yechim (Rust kodi):
```rust
trait Calculator {
    fn calculate(&self, a: i32, b: i32) -> i32;
}

struct Adder;

impl Calculator for Adder {
    #[inline(always)]
    fn calculate(&self, a: i32, b: i32) -> i32 { a + b }
}

fn main() {
    let calc = Adder;
    println!("Natija: {}", calc.calculate(10, 20));
}
```

## Tushuntirish va Mantiq:
`#[inline(always)]` kompilyatorga funksiya tanasini chaqirilgan joyga to'g'ridan-to'g'ri joylashtirishni buyuradi, bu esa funksiya chaqiruvi xarajatini (overhead) yo'qotadi.

## Ishlash natijasi:
```text
Natija: 30
```

---

# 1014-Topshiriq: Unsafe kodda xotirani ajratish (Manual Allocation)

## Topshiriq sharti:
`std::alloc` yordamida xotirani qo'lda ajrating va uni `unsafe` blokida tozalang.

## Yechim (Rust kodi):
```rust
use std::alloc::{alloc, dealloc, Layout};

fn main() {
    unsafe {
        let layout = Layout::new::<i32>();
        let ptr = alloc(layout) as *mut i32;
        *ptr = 100;
        println!("Ajratilgan xotiradagi qiymat: {}", *ptr);
        dealloc(ptr as *mut u8, layout);
    }
}
```

## Tushuntirish va Mantiq:
`Layout` xotira blokining hajmi va hizalanishini (alignment) belgilaydi. `alloc` xotira ajratadi, `dealloc` esa uni bo'shatadi. Bu xotira sizishining (memory leak) oldini olish uchun muhim.

## Ishlash natijasi:
```text
Ajratilgan xotiradagi qiymat: 100
```

---

# 1015-Topshiriq: Volatile xotira operatsiyalari (Drayverlar uchun)

## Topshiriq sharti:
Drayver dasturlashda muhim bo'lgan `read_volatile` funksiyasidan foydalanib, xotira manzilidan qiymatni o'qing.

## Yechim (Rust kodi):
```rust
use std::ptr::read_volatile;

fn main() {
    let val = 500;
    let ptr = &val as *const i32;
    unsafe {
        let read_val = read_volatile(ptr);
        println!("Volatile o'qilgan qiymat: {}", read_val);
    }
}
```

## Tushuntirish va Mantiq:
`read_volatile` kompilyatorga bu xotira manzili tashqi omillar (masalan, apparat qurilmasi) tomonidan o'zgarishi mumkinligini bildiradi, shuning uchun optimallashtirishda uni o'tkazib yubormaslik kerak.

## Ishlash natijasi:
```text
Volatile o'qilgan qiymat: 500
```

---

# 1016-Topshiriq: Union (Birlashma) turlari

## Topshiriq sharti:
`union` turidan foydalanib, bir xil xotira maydonida turli xil ma'lumot turlarini saqlang.

## Yechim (Rust kodi):
```rust
union MyUnion {
    i: i32,
    f: f32,
}

fn main() {
    let u = MyUnion { i: 42 };
    unsafe {
        println!("Union qiymati (i): {}", u.i);
    }
}
```

## Tushuntirish va Mantiq:
`union` C tilidagi kabi ishlaydi. U xotirani tejash uchun ishlatiladi, lekin qaysi maydonni o'qishni dasturchi nazorat qilishi kerak, shuning uchun `unsafe` talab qilinadi.

## Ishlash natijasi:
```text
Union qiymati (i): 42
```

---

# 1017-Topshiriq: Transmute funksiyasi bilan turlarni o'zgartirish

## Topshiriq sharti:
`std::mem::transmute` yordamida `[u8; 4]` massivini `u32` turiga o'tkazing.

## Yechim (Rust kodi):
```rust
use std::mem::transmute;

fn main() {
    let bytes: [u8; 4] = [0, 0, 0, 1];
    let num: u32 = unsafe { transmute(bytes) };
    println!("O'tkazilgan raqam: {}", u32::from_be(num));
}
```

## Tushuntirish va Mantiq:
`transmute` xotiradagi bitlarni o'zgartirmasdan, bir turdan ikkinchisiga majburiy o'tkazadi. Bu juda xavfli, chunki noto'g'ri foydalanish xotira xatolariga olib keladi.

## Ishlash natijasi:
```text
O'tkazilgan raqam: 1
```

---

# 1018-Topshiriq: Xavfsiz Wrapper (Sarmoya) yaratish

## Topshiriq sharti:
`unsafe` kodni yashiradigan va foydalanuvchiga xavfsiz interfeys taqdim etadigan `struct` yarating.

## Yechim (Rust kodi):
```rust
struct SafePointer {
    ptr: *mut i32,
}

impl SafePointer {
    fn new(val: i32) -> Self {
        let ptr = Box::into_raw(Box::new(val));
        SafePointer { ptr }
    }
    fn get(&self) -> i32 { unsafe { *self.ptr } }
}

fn main() {
    let sp = SafePointer::new(99);
    println!("Xavfsiz o'qilgan qiymat: {}", sp.get());
}
```

## Tushuntirish va Mantiq:
Bu "Encapsulation" prinsipi. `unsafe` kod ichkarida yashiringan, tashqi foydalanuvchi esa faqat xavfsiz `get()` metodini ko'radi.

## Ishlash natijasi:
```text
Xavfsiz o'qilgan qiymat: 99
```

---

# 1019-Topshiriq: Nullable ko'rsatkichni tekshirish

## Topshiriq sharti:
`*const T` ko'rsatkichi `null` ekanligini tekshirib, xavfsiz `Option` turiga o'tkazing.

## Yechim (Rust kodi):
```rust
fn main() {
    let ptr: *const i32 = std::ptr::null();
    
    let val = if ptr.is_null() {
        None
    } else {
        unsafe { Some(*ptr) }
    };

    match val {
        Some(v) => println!("Qiymat: {}", v),
        None => println!("Ko'rsatkich null!"),
    }
}
```

## Tushuntirish va Mantiq:
`is_null()` metodi xavfsizdir. Biz `unsafe` blokini faqat `null` emasligiga ishonch hosil qilganimizdan keyin ishlatamiz.

## Ishlash natijasi:
```text
Ko'rsatkich null!
```

---

# 1020-Topshiriq: FFI orqali C stringini Rust stringiga o'girish

## Topshiriq sharti:
`std::ffi::CStr` yordamida C-stilidagi `*const i8` ko'rsatkichini Rust `&str` turiga aylantiring.

## Yechim (Rust kodi):
```rust
use std::ffi::CStr;

fn main() {
    let c_str: *const i8 = b"KhorazmiyAI\0".as_ptr() as *const i8;
    
    unsafe {
        let rust_str = CStr::from_ptr(c_str).to_str().unwrap();
        println!("Rust stringi: {}", rust_str);
    }
}
```

## Tushuntirish va Mantiq:
C stringlari `\0` (null terminator) bilan tugaydi. `CStr` bu xotira maydonini xavfsiz o'qish uchun vositadir. `to_str()` esa uni UTF-8 ga tekshirib o'giradi.

## Ishlash natijasi:
```text
Rust stringi: KhorazmiyAI
```

---

Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. Rust dasturlash tilining chuqur qatlamlari (low-level) bo'yicha 100 000 talik datasetimizni boyitish uchun mo'ljallangan #1021-#1030 topshiriqlar to'plamini taqdim etaman.

---

# 1021-Topshiriq: Unsafe blokda xotira xavfsizligini boshqarish

## Topshiriq sharti:
`unsafe` blokdan foydalanib, xom ko'rsatkich (raw pointer) orqali qiymatni o'zgartiring va xotira xavfsizligini ta'minlash uchun `std::ptr` funksiyalaridan foydalaning.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut data = 10;
    let ptr = &mut data as *mut i32;

    unsafe {
        *ptr += 20;
        println!("O'zgartirilgan qiymat: {}", *ptr);
    }
}
```

## Tushuntirish va Mantiq:
`*mut i32` ko'rsatkichi xotiradagi manzilni saqlaydi. `unsafe` blok ichida biz ushbu manzilga to'g'ridan-to'g'ri murojaat qilib, qiymatni o'zgartiramiz. Bu operatsiya Rust kompilyatori tomonidan tekshirilmaydi, shuning uchun dasturchi xotira xavfsizligi uchun javobgardir.

## Ishlash natijasi:
```text
O'zgartirilgan qiymat: 30
```

---

# 1022-Topshiriq: FFI orqali C funksiyasini chaqirish

## Topshiriq sharti:
Rust dasturida `libc` kutubxonasi orqali C tilidagi `abs` (modul) funksiyasini chaqiring.

## Yechim (Rust kodi):
```rust
extern "C" {
    fn abs(input: i32) -> i32;
}

fn main() {
    let number = -42;
    unsafe {
        println!("{} ning moduli: {}", number, abs(number));
    }
}
```

## Tushuntirish va Mantiq:
`extern "C"` bloki Rustga tashqi C kutubxonasidagi funksiyani qidirishni buyuradi. FFI (Foreign Function Interface) orqali chaqirilgan har qanday funksiya `unsafe` hisoblanadi, chunki Rust kompilyatori C kodining xavfsizligini kafolatlay olmaydi.

## Ishlash natijasi:
```text
-42 ning moduli: 42
```

---

# 1023-Topshiriq: Nol xarajatli abstraktsiya (Trait va Inline)

## Topshiriq sharti:
`#[inline]` atributi va `Trait` yordamida nol xarajatli abstraktsiyani namoyish eting.

## Yechim (Rust kodi):
```rust
trait Calculator {
    fn compute(&self, a: i32) -> i32;
}

struct Adder;

impl Calculator for Adder {
    #[inline(always)]
    fn compute(&self, a: i32) -> i32 { a + 10 }
}

fn main() {
    let calc = Adder;
    println!("Natija: {}", calc.compute(5));
}
```

## Tushuntirish va Mantiq:
`#[inline(always)]` kompilyatorga funksiya tanasini chaqiruv joyiga to'g'ridan-to'g'ri joylashtirishni buyuradi. Bu abstraktsiya (Trait) ishlatilgan bo'lsa-da, funksiya chaqiruvi uchun qo'shimcha xarajat (overhead) bo'lmasligini ta'minlaydi.

## Ishlash natijasi:
```text
Natija: 15
```

---

# 1024-Topshiriq: OS drayverlari uchun xotira xaritalash (MMIO)

## Topshiriq sharti:
Belgilangan xotira manziliga (masalan, 0xDEADBEEF) qiymat yozishga urinishni simulyatsiya qiling.

## Yechim (Rust kodi):
```rust
fn main() {
    let mmio_address = 0xDEADBEEF as *mut u32;
    
    // Eslatma: Bu kod real tizimda xatolik beradi (Segmentation Fault)
    // Shuning uchun faqat mantiqiy namoyish sifatida qaraladi.
    println!("MMIO manzili: {:p}", mmio_address);
}
```

## Tushuntirish va Mantiq:
OS drayverlari apparat qismlari bilan muloqot qilish uchun MMIO (Memory Mapped I/O) dan foydalanadi. Rustda bu `volatile` operatsiyalar orqali amalga oshiriladi, bu esa kompilyatorga xotira qiymatini optimallashtirmaslikni buyuradi.

## Ishlash natijasi:
```text
MMIO manzili: 0xdeadbeef
```

---

# 1025-Topshiriq: Unsafe kodda "Dangling Pointer" nazorati

## Topshiriq sharti:
`Box::into_raw` yordamida xotirani boshqarish va uni `Box::from_raw` bilan qayta tiklash.

## Yechim (Rust kodi):
```rust
fn main() {
    let b = Box::new(100);
    let raw = Box::into_raw(b);
    
    unsafe {
        println!("Qiymat: {}", *raw);
        let _ = Box::from_raw(raw); // Xotirani tozalash
    }
}
```

## Tushuntirish va Mantiq:
`Box::into_raw` xotira boshqaruvini Rust'dan olib, dasturchiga o'tkazadi. `Box::from_raw` esa xotirani qayta `Box` egiligiga o'tkazib, scope tugaganda xotirani avtomatik tozalashni (deallocation) ta'minlaydi.

## Ishlash natijasi:
```text
Qiymat: 100
```

---

# 1026-Topshiriq: Volatile o'qish va yozish

## Topshiriq sharti:
`std::ptr::read_volatile` yordamida xotiradan ma'lumotni xavfsiz o'qish.

## Yechim (Rust kodi):
```rust
use std::ptr;

fn main() {
    let mut val = 50;
    unsafe {
        let ptr = &val as *const i32;
        let read_val = ptr::read_volatile(ptr);
        println!("O'qilgan qiymat: {}", read_val);
    }
}
```

## Tushuntirish va Mantiq:
`read_volatile` kompilyatorga ushbu xotira manzilidagi ma'lumot tashqi omillar (masalan, drayver) tomonidan o'zgarishi mumkinligini bildiradi, shuning uchun optimallashtirishni cheklaydi.

## Ishlash natijasi:
```text
O'qilgan qiymat: 50
```

---

# 1027-Topshiriq: FFI orqali C struct bilan ishlash

## Topshiriq sharti:
`#[repr(C)]` atributi yordamida Rust structini C formatiga moslashtirish.

## Yechim (Rust kodi):
```rust
#[repr(C)]
struct Point {
    x: i32,
    y: i32,
}

fn main() {
    let p = Point { x: 10, y: 20 };
    println!("C-mos struct: x={}, y={}", p.x, p.y);
}
```

## Tushuntirish va Mantiq:
`#[repr(C)]` Rust kompilyatoriga struct xotirada C tilidagi kabi tartibda joylashishini kafolatlaydi. Bu FFI orqali C funksiyalariga struct yuborishda juda muhimdir.

## Ishlash natijasi:
```text
C-mos struct: x=10, y=20
```

---

# 1028-Topshiriq: Union turlari va Unsafe

## Topshiriq sharti:
`union` turidan foydalanib, bir xil xotira maydonida ikki xil turdagi ma'lumotni saqlash.

## Yechim (Rust kodi):
```rust
union MyUnion {
    i: i32,
    f: f32,
}

fn main() {
    let u = MyUnion { i: 42 };
    unsafe {
        println!("Union qiymati: {}", u.i);
    }
}
```

## Tushuntirish va Mantiq:
`union` xotirani tejash uchun ishlatiladi. Rustda union maydonlariga kirish har doim `unsafe` hisoblanadi, chunki qaysi maydon faol ekanligini kompilyator bilmaydi.

## Ishlash natijasi:
```text
Union qiymati: 42
```

---

# 1029-Topshiriq: Null ko'rsatkichni tekshirish

## Topshiriq sharti:
`ptr.is_null()` funksiyasidan foydalanib, xavfsiz tekshiruvni amalga oshirish.

## Yechim (Rust kodi):
```rust
fn main() {
    let ptr: *const i32 = std::ptr::null();
    
    if ptr.is_null() {
        println!("Ko'rsatkich null!");
    } else {
        println!("Ko'rsatkich mavjud.");
    }
}
```

## Tushuntirish va Mantiq:
`std::ptr::null()` xotirada hech narsaga ishora qilmaydigan manzilni qaytaradi. `is_null()` metodi xotira xavfsizligini ta'minlash uchun eng muhim himoya vositalaridan biridir.

## Ishlash natijasi:
```text
Ko'rsatkich null!
```

---

# 1030-Topshiriq: Transmute orqali turlarni o'zgartirish

## Topshiriq sharti:
`std::mem::transmute` yordamida `u32` ni `f32` ga o'zgartirish.

## Yechim (Rust kodi):
```rust
use std::mem;

fn main() {
    let u: u32 = 0x3f800000;
    let f: f32 = unsafe { mem::transmute(u) };
    println!("Transmute natijasi: {}", f);
}
```

## Tushuntirish va Mantiq:
`transmute` eng xavfli funksiyalardan biri bo'lib, u xotiradagi bitlarni o'zgartirmasdan turib, bir turdan ikkinchi turga majburiy o'tkazadi. Bu faqat juda zarur bo'lgan past darajali operatsiyalarda qo'llaniladi.

## Ishlash natijasi:
```text
Transmute natijasi: 1
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. Rust dasturlash tilining chuqur qatlamlari (low-level) bo'yicha 100 000 talik datasetimizni boyitish uchun mo'ljallangan #1031 dan #1040 gacha bo'lgan maxsus modullarni taqdim etaman.

---

# 1031-Topshiriq: Unsafe blokda xotira xavfsizligini boshqarish

## Topshiriq sharti:
`unsafe` blokdan foydalanib, xom ko'rsatkich (raw pointer) orqali xotiradagi qiymatni o'zgartiring va uning xavfsizligini tekshiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut num = 10;
    let ptr = &mut num as *mut i32;

    unsafe {
        *ptr += 20;
    }

    println!("O'zgartirilgan qiymat: {}", num);
}
```

## Tushuntirish va Mantiq:
`*mut i32` ko'rsatkichi xotiradagi manzilni saqlaydi. `unsafe` bloki Rust kompilyatoriga biz xotira xavfsizligini o'z zimmamizga olayotganimizni bildiradi. `*ptr` orqali qiymatni bevosita xotira manzilida o'zgartiramiz.

## Ishlash natijasi:
```text
O'zgartirilgan qiymat: 30
```

---

# 1032-Topshiriq: FFI orqali C funksiyasini chaqirish

## Topshiriq sharti:
Rust dasturida `libc` kutubxonasi orqali C tilidagi `abs` (modul) funksiyasini chaqiring.

## Yechim (Rust kodi):
```rust
extern "C" {
    fn abs(input: i32) -> i32;
}

fn main() {
    let val = -42;
    unsafe {
        println!("C funksiyasi natijasi: {}", abs(val));
    }
}
```

## Tushuntirish va Mantiq:
`extern "C"` bloki tashqi C kutubxonalariga interfeys yaratadi. `unsafe` bloki FFI (Foreign Function Interface) chaqiruvlari uchun majburiy, chunki Rust C funksiyasining xavfsizligini kafolatlay olmaydi.

## Ishlash natijasi:
```text
C funksiyasi natijasi: 42
```

---

# 1033-Topshiriq: Nol xarajatli abstraktsiya (Iterators)

## Topshiriq sharti:
`Iterator` traitidan foydalanib, massiv elementlarini kvadratga oshiruvchi va xotira sarfini minimallashtiruvchi (zero-cost) kod yozing.

## Yechim (Rust kodi):
```rust
fn main() {
    let nums = vec![1, 2, 3, 4];
    let squared: Vec<i32> = nums.iter().map(|&x| x * x).collect();
    println!("Natija: {:?}", squared);
}
```

## Tushuntirish va Mantiq:
`map` funksiyasi "lazy" (dangasa) hisoblanadi. U qo'shimcha sikl yaratmaydi, balki kompilyatsiya vaqtida optimallashtirilgan mashina kodiga aylanadi. Bu "nol xarajatli abstraktsiya"ning klassik namunasidir.

## Ishlash natijasi:
```text
Natija: [1, 4, 9, 16]
```

---

# 1034-Topshiriq: OS drayverlari uchun MMIO simulyatsiyasi

## Topshiriq sharti:
Xotiraga yo'naltirilgan kiritish-chiqarish (MMIO) uchun `volatile` yozish operatsiyasini simulyatsiya qiling.

## Yechim (Rust kodi):
```rust
use std::ptr::write_volatile;

fn main() {
    let mut register: u32 = 0;
    unsafe {
        write_volatile(&mut register as *mut u32, 0xABCD);
    }
    println!("Register qiymati: {:X}", register);
}
```

## Tushuntirish va Mantiq:
`write_volatile`, kompilyatorga bu xotira manzilini optimallashtirish (o'chirib tashlash) mumkin emasligini aytadi. Bu drayverlar yozishda apparat ta'minoti bilan ishlash uchun juda muhim.

## Ishlash natijasi:
```text
Register qiymati: ABCD
```

---

# 1035-Topshiriq: Unsafe Union (Birlashma)

## Topshiriq sharti:
`union` dan foydalanib, bir xil xotira maydonida `f32` va `u32` turlarini saqlang.

## Yechim (Rust kodi):
```rust
union MyUnion {
    f: f32,
    u: u32,
}

fn main() {
    let u = MyUnion { u: 0x3F800000 };
    unsafe {
        println!("Float qiymati: {}", u.f);
    }
}
```

## Tushuntirish va Mantiq:
`union` xotirani tejash uchun ishlatiladi. Rustda union maydonlariga kirish `unsafe` hisoblanadi, chunki qaysi turdagi ma'lumot o'qilayotganini dasturchi o'zi nazorat qilishi kerak.

## Ishlash natijasi:
```text
Float qiymati: 1
```

---

# 1036-Topshiriq: Raw Pointer xavfsizligini tekshirish

## Topshiriq sharti:
Ko'rsatkichning `null` emasligini tekshirib, keyin uni xavfsiz dereference qiling.

## Yechim (Rust kodi):
```rust
fn main() {
    let val = 100;
    let ptr: *const i32 = &val;

    if !ptr.is_null() {
        unsafe {
            println!("Qiymat: {}", *ptr);
        }
    }
}
```

## Tushuntirish va Mantiq:
`is_null()` metodi xom ko'rsatkichlar bilan ishlashda xatoliklarning oldini olish uchun eng muhim himoya qatlamidir.

## Ishlash natijasi:
```text
Qiymat: 100
```

---

# 1037-Topshiriq: Box va Heap xotira

## Topshiriq sharti:
`Box` yordamida stack o'rniga heap xotirada ma'lumot saqlang va uning manzilini ko'rsating.

## Yechim (Rust kodi):
```rust
fn main() {
    let b = Box::new(500);
    println!("Heapdagi qiymat: {}, Manzil: {:p}", b, b);
}
```

## Tushuntirish va Mantiq:
`Box` - bu heap xotiraga ajratilgan ma'lumotga ko'rsatkich. Bu xotirani boshqarishda "Ownership" (egalik) modelining asosi hisoblanadi.

## Ishlash natijasi:
```text
Heapdagi qiymat: 500, Manzil: 0x... (dinamik manzil)
```

---

# 1038-Topshiriq: Transmute (Turlarni majburiy o'zgartirish)

## Topshiriq sharti:
`std::mem::transmute` yordamida `[u8; 4]` massivini `u32` turiga o'tkazing.

## Yechim (Rust kodi):
```rust
use std::mem::transmute;

fn main() {
    let bytes: [u8; 4] = [0, 0, 0, 1];
    let num: u32 = unsafe { transmute(bytes) };
    println!("O'girilgan son: {}", num.to_be());
}
```

## Tushuntirish va Mantiq:
`transmute` - bu Rustdagi eng xavfli funksiya. U bitlarni o'zgartirmasdan, tur (type) ni majburan boshqa turga o'tkazadi.

## Ishlash natijasi:
```text
O'girilgan son: 1
```

---

# 1039-Topshiriq: Drop trait va xotirani tozalash

## Topshiriq sharti:
`Drop` traitini implementatsiya qilib, obyekt xotiradan o'chirilayotganda xabar bering.

## Yechim (Rust kodi):
```rust
struct Resource;

impl Drop for Resource {
    fn drop(&mut self) {
        println!("Resurs tozalandi!");
    }
}

fn main() {
    let _r = Resource;
}
```

## Tushuntirish va Mantiq:
`Drop` trait - bu RAII (Resource Acquisition Is Initialization) tamoyilining asosi. Obyekt scope'dan chiqishi bilan `drop` avtomatik chaqiriladi.

## Ishlash natijasi:
```text
Resurs tozalandi!
```

---

# 1040-Topshiriq: Inline Assembly (OS darajasi)

## Topshiriq sharti:
`asm!` makrosidan foydalanib, oddiy qo'shish amalini bajaruvchi assembly kodini yozing.

## Yechim (Rust kodi):
```rust
use std::arch::asm;

fn main() {
    let mut x: u64 = 10;
    unsafe {
        asm!("add {0}, 5", inout(reg) x);
    }
    println!("Assembly natijasi: {}", x);
}
```

## Tushuntirish va Mantiq:
`asm!` makrosi to'g'ridan-to'g'ri CPU instruksiyalarini yozishga imkon beradi. Bu OS yadrosi yoki drayverlar yozishda eng past darajadagi nazoratni ta'minlaydi.

## Ishlash natijasi:
```text
Assembly natijasi: 15
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. Rust dasturlash tilining chuqur qatlamlarini (Low-level, Unsafe, FFI) qamrab oluvchi, modelimizni o'qitish uchun mo'ljallangan 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1041-Topshiriq: Unsafe blokda xotira xavfsizligini boshqarish

## Topshiriq sharti:
`unsafe` blokdan foydalanib, xom ko'rsatkich (raw pointer) orqali xotiradagi qiymatni o'zgartiring va uning xavfsizligini `Box` orqali qayta tiklang.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut data = 42;
    let ptr = &mut data as *mut i32;

    unsafe {
        *ptr += 10;
    }

    println!("O'zgartirilgan qiymat: {}", data);
}
```

## Tushuntirish va Mantiq:
`*mut i32` ko'rsatkichi xotira manzilini saqlaydi. `unsafe` blok ichida biz ushbu manzilga to'g'ridan-to'g'ri murojaat qilib, qiymatni o'zgartiramiz. Bu operatsiya Rust kompilyatori tomonidan tekshirilmaydi, shuning uchun xavfsizlik dasturchi zimmasida.

## Ishlash natijasi:
```text
O'zgartirilgan qiymat: 52
```

---

# 1042-Topshiriq: FFI orqali C funksiyasini chaqirish

## Topshiriq sharti:
Rust dasturida `libc` kutubxonasi orqali C tilidagi `abs` (modul) funksiyasini chaqiring.

## Yechim (Rust kodi):
```rust
extern "C" {
    fn abs(input: i32) -> i32;
}

fn main() {
    let number = -25;
    unsafe {
        println!("Abs qiymat: {}", abs(number));
    }
}
```

## Tushuntirish va Mantiq:
`extern "C"` bloki tashqi C funksiyalarini e'lon qilish uchun ishlatiladi. FFI (Foreign Function Interface) orqali biz C muhitidagi funksiyalarni Rust ichida ishlatamiz. Bu operatsiya har doim `unsafe` hisoblanadi.

## Ishlash natijasi:
```text
Abs qiymat: 25
```

---

# 1043-Topshiriq: Nol xarajatli abstraktsiya (Zero-cost Abstraction)

## Topshiriq sharti:
`Iterator` trait'idan foydalanib, `map` va `filter` yordamida ma'lumotlarni qayta ishlang. Bu kod kompilyatsiya vaqtida optimallashtirilgan mashina kodiga aylanishini ko'rsating.

## Yechim (Rust kodi):
```rust
fn main() {
    let nums = vec![1, 2, 3, 4, 5];
    let sum: i32 = nums.iter().filter(|&x| x % 2 != 0).map(|x| x * 2).sum();
    println!("Natija: {}", sum);
}
```

## Tushuntirish va Mantiq:
Rust'dagi iteratorlar "nol xarajatli" hisoblanadi. Kompilyator bu kodni qo'lda yozilgan `for` sikli kabi tez ishlaydigan mashina kodiga o'giradi. Hech qanday qo'shimcha runtime xarajat yo'q.

## Ishlash natijasi:
```text
Natija: 18
```

---

# 1044-Topshiriq: OS drayverlari uchun MMIO simulyatsiyasi

## Topshiriq sharti:
Drayverlar uchun xos bo'lgan MMIO (Memory Mapped I/O) ni simulyatsiya qiling. Muayyan xotira manziliga qiymat yozishni `volatile` operatsiyalar bilan bajaring.

## Yechim (Rust kodi):
```rust
use std::ptr::{read_volatile, write_volatile};

fn main() {
    let mut register: u32 = 0;
    unsafe {
        write_volatile(&mut register as *mut u32, 0xAA);
        println!("Register qiymati: {:X}", read_volatile(&register as *const u32));
    }
}
```

## Tushuntirish va Mantiq:
`volatile` operatsiyalar kompilyatorga bu xotira manzilini optimallashtirmaslikni (o'zgartirmaslikni) buyuradi. Bu drayverlar uchun juda muhim, chunki apparat ta'minoti (hardware) xotira qiymatini istalgan vaqtda o'zgartirishi mumkin.

## Ishlash natijasi:
```text
Register qiymati: AA
```

---

# 1045-Topshiriq: Unsafe Rust va Union turlari

## Topshiriq va Mantiq:
`union` turidan foydalanib, bir xil xotira maydonida `f32` va `u32` qiymatlarini saqlang.

## Yechim (Rust kodi):
```rust
union MyUnion {
    f: f32,
    u: u32,
}

fn main() {
    let u = MyUnion { u: 0x3f800000 };
    unsafe {
        println!("Float qiymati: {}", u.f);
    }
}
```

## Tushuntirish va Mantiq:
`union` xotirani tejash uchun ishlatiladi. Rust'da union maydonlariga kirish `unsafe` hisoblanadi, chunki kompilyator qaysi maydon faol ekanligini kafolatlay olmaydi.

## Ishlash natijasi:
```text
Float qiymati: 1
```

---

# 1046-Topshiriq: Xavfsiz abstraktsiya qatlami (Wrapper)

## Topshiriq sharti:
`unsafe` kodni xavfsiz `struct` ichiga o'rab, foydalanuvchiga xavfsiz interfeys taqdim eting.

## Yechim (Rust kodi):
```rust
struct SafePointer(Box<i32>);

impl SafePointer {
    fn new(val: i32) -> Self { SafePointer(Box::new(val)) }
    fn get(&self) -> i32 { *self.0 }
}

fn main() {
    let ptr = SafePointer::new(100);
    println!("Qiymat: {}", ptr.get());
}
```

## Tushuntirish va Mantiq:
Bu "Encapsulation" prinsipi. Biz xavfli xotira boshqaruvini `SafePointer` ichiga yashiramiz va tashqariga faqat xavfsiz metodlarni chiqaramiz.

## Ishlash natijasi:
```text
Qiymat: 100
```

---

# 1047-Topshiriq: Raw Pointer va Slice konvertatsiyasi

## Topshiriq sharti:
Xom ko'rsatkichni `std::slice::from_raw_parts` yordamida xavfsiz `slice` ga aylantiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let data = [10, 20, 30];
    let ptr = data.as_ptr();
    
    unsafe {
        let slice = std::slice::from_raw_parts(ptr, 3);
        println!("Slice: {:?}", slice);
    }
}
```

## Tushuntirish va Mantiq:
`from_raw_parts` funksiyasi xom ko'rsatkich va uzunlikni olib, uni Rust'ning xavfsiz `slice` turiga o'giradi. Bu operatsiya xotira xavfsizligini buzishi mumkin, shuning uchun `unsafe` talab qilinadi.

## Ishlash natijasi:
```text
Slice: [10, 20, 30]
```

---

# 1048-Topshiriq: Drop trait va xotirani tozalash

## Topshiriq sharti:
`Drop` trait'ini implementatsiya qilib, obyekt xotiradan o'chirilayotganda xabar bering.

## Yechim (Rust kodi):
```rust
struct Resource;

impl Drop for Resource {
    fn drop(&mut self) {
        println!("Resurs tozalandi!");
    }
}

fn main() {
    let _r = Resource;
}
```

## Tushuntirish va Mantiq:
Rust'da xotirani boshqarish (RAII) `Drop` trait'i orqali amalga oshiriladi. Obyekt scope'dan chiqqanda `drop` avtomatik chaqiriladi.

## Ishlash natijasi:
```text
Resurs tozalandi!
```

---

# 1049-Topshiriq: Inline Assembly (asm!)

## Topshiriq sharti:
Rust ichida `asm!` makrosidan foydalanib, oddiy qo'shish amalini bajaring.

## Yechim (Rust kodi):
```rust
use std::arch::asm;

fn main() {
    let mut x: u64 = 5;
    unsafe {
        asm!("add {0}, {1}", inout(reg) x, const 5);
    }
    println!("Natija: {}", x);
}
```

## Tushuntirish va Mantiq:
`asm!` makrosi to'g'ridan-to'g'ri CPU instruksiyalarini yozishga imkon beradi. Bu drayverlar va operatsion tizim yadro qismlarini yozishda ishlatiladi.

## Ishlash natijasi:
```text
Natija: 10
```

---

# 1050-Topshiriq: Send va Sync traitlari

## Topshiriq sharti:
`Send` trait'ini tushunish uchun threadlar o'rtasida ma'lumot uzatishni ko'rsating.

## Yechim (Rust kodi):
```rust
use std::thread;

fn main() {
    let data = String::from("Khorazmiy AI");
    let handle = thread::spawn(move || {
        println!("Thread ichida: {}", data);
    });
    handle.join().unwrap();
}
```

## Tushuntirish va Mantiq:
`Send` trait'i ma'lumotni bir thread'dan ikkinchisiga xavfsiz ko'chirish mumkinligini bildiradi. `move` kalit so'zi egalik huquqini thread'ga o'tkazadi.

## Ishlash natijasi:
```text
Thread ichida: Khorazmiy AI
```