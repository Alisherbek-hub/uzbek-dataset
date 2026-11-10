# Rust Dasturlash Tili: Multithreading va Parallelizm

Ushbu modulda Rust dasturlash tilida ko'p oqimli dasturlash asoslari: `std::thread`, `mpsc` kanallari, `Arc`, `Mutex`, `RwLock`, `Atomic` operatsiyalari, `Send` va `Sync` trait'lari, `Condvar`, `Barrier`, `thread_local!` va parallel algoritmlar to'liq yoritilgan.

---

# 751-Topshiriq: std::thread::spawn bilan yangi oqim yaratish
## Topshiriq sharti:
Rust dasturida `std::thread::spawn` yordamida alohida oqim ishga tushirish va unda matn chop etish dasturini yozing.
## Yechim (Rust kodi):
```rust
use std::thread;
use std::time::Duration;

fn main() {
    thread::spawn(|| {
        for i in 1..=3 {
            println!("Yangi oqimdan salom: {}", i);
            thread::sleep(Duration::from_millis(10));
        }
    });

    for i in 1..=2 {
        println!("Asosiy oqimdan salom: {}", i);
        thread::sleep(Duration::from_millis(15));
    }
}
```
## Tushuntirish va Mantiq:
`thread::spawn` yangi operatsion tizim oqimini (native OS thread) yaratadi va closure ichidagi kodni parallel bajaradi.
## Ishlash natijasi:
```text
Asosiy oqimdan salom: 1
Yangi oqimdan salom: 1
Yangi oqimdan salom: 2
Asosiy oqimdan salom: 2
```

---

# 752-Topshiriq: thread::spawn closure'iga move kalit so'zi bilan ma'lumot uzatish
## Topshiriq sharti:
`move` kalit so'zidan foydalanib o'zgaruvchi egaligini yangi oqimga xavfsiz ko'chiring.
## Yechim (Rust kodi):
```rust
use std::thread;

fn main() {
    let sonlar = vec![10, 20, 30];

    let handle = thread::spawn(move || {
        println!("Oqim ichidagi vektor: {:?}", sonlar);
    });

    handle.join().unwrap();
}
```
## Tushuntirish va Mantiq:
`move` kalit so'zi closure'ga tashqi muhitdagi o'zgaruvchilarni qarzga olish o'rniga ularning to'liq egaligini o'zlashtirishni buyuradi.
## Ishlash natijasi:
```text
Oqim ichidagi vektor: [10, 20, 30]
```

---

# 753-Topshiriq: JoinHandle va handle.join() bilan oqim tugashini kutish
## Topshiriq sharti:
Asosiy oqim yangi oqim o'z ishini to'liq tugatmaguncha kutib turishi uchun `JoinHandle::join` metodini qo'llang.
## Yechim (Rust kodi):
```rust
use std::thread;
use std::time::Duration;

fn main() {
    let handle = thread::spawn(|| {
        println!("Ishchi oqim ish boshladi...");
        thread::sleep(Duration::from_millis(50));
        println!("Ishchi oqim ishini yakunladi!");
    });

    println!("Asosiy oqim ishchi tugashini kutmoqda...");
    handle.join().unwrap();
    println!("Barcha amallar muvaffaqiyatli yakunlandi.");
}
```
## Tushuntirish va Mantiq:
`join()` chaqirilganda chaqiruvchi oqim maqsadli oqim tugagunga qadar bloklanadi (kutiladi). Bu ma'lumotlar yo'qolishining oldini oladi.
## Ishlash natijasi:
```text
Asosiy oqim ishchi tugashini kutmoqda...
Ishchi oqim ish boshladi...
Ishchi oqim ishini yakunladi!
Barcha amallar muvaffaqiyatli yakunlandi.
```

---

# 754-Topshiriq: Thread'dan qaytgan natijani join().unwrap() orqali qabul qilish
## Topshiriq sharti:
Yangi oqimda hisoblangan natijani asosiy oqimga `join()` orqali qaytarib oling.
## Yechim (Rust kodi):
```rust
use std::thread;

fn main() {
    let handle = thread::spawn(|| {
        let x = 25;
        let y = 17;
        x * y // Oqimdan qaytuvchi qiymat
    });

    let natija = handle.join().unwrap();
    println!("Oqimdan qabul qilingan natija: {}", natija);
}
```
## Tushuntirish va Mantiq:
`JoinHandle<T>` oqim closure'idan qaytgan har qanday `T` turidagi natijani `Result<T, Box<dyn Any>>` ko'rinishida qaytaradi.
## Ishlash natijasi:
```text
Oqimdan qabul qilingan natija: 425
```

---

# 755-Topshiriq: Bir nechta oqimlarni loop ichida yaratish va barchasini join qilish
## Topshiriq sharti:
Loop orqali 5 ta mustaqil oqim ochib, ularning barchasini vektorga yig'ing va ketma-ket `join` qiling.
## Yechim (Rust kodi):
```rust
use std::thread;

fn main() {
    let mut dastalari = vec![];

    for i in 1..=5 {
        let h = thread::spawn(move || {
            format!("Oqim #{} muvaffaqiyatli ishladi", i)
        });
        dastalari.push(h);
    }

    for h in dastalari {
        let xabar = h.join().unwrap();
        println!("{}", xabar);
    }
}
```
## Tushuntirish va Mantiq:
Bir nechta oqimlarni boshqarish uchun ularning handle'larini `Vec<JoinHandle<T>>` ichida saqlash va sikl orqali join qilish qulaydir.
## Ishlash natijasi:
```text
Oqim #1 muvaffaqiyatli ishladi
Oqim #2 muvaffaqiyatli ishladi
Oqim #3 muvaffaqiyatli ishladi
Oqim #4 muvaffaqiyatli ishladi
Oqim #5 muvaffaqiyatli ishladi
```

---

# 756-Topshiriq: std::thread::sleep va Duration bilan kechikish kiritish
## Topshiriq sharti:
Oqimni belgilangan vaqt davomida to'xtatib turish dasturini yozing.
## Yechim (Rust kodi):
```rust
use std::thread;
use std::time::Duration;

fn main() {
    println!("3 soniyalik hisob boshlandi:");
    for soniya in (1..=3).rev() {
        println!("{}...", soniya);
        thread::sleep(Duration::from_millis(100)); // Misol tez ishlashi uchun 100ms
    }
    println!("Start!");
}
```
## Tushuntirish va Mantiq:
`thread::sleep` joriy oqimni belgilangan `Duration` davomida bloklaydi va CPU resursini boshqa jarayonlarga bo'shatadi.
## Ishlash natijasi:
```text
3 soniyalik hisob boshlandi:
3...
2...
1...
Start!
```

---

# 757-Topshiriq: thread::current().id() va nomini olish
## Topshiriq sharti:
Ishlayotgan oqimning unikal identifikatori (ThreadId) va nomini chop eting.
## Yechim (Rust kodi):
```rust
use std::thread;

fn main() {
    let joriy = thread::current();
    println!("Asosiy oqim nomi: {:?}", joriy.name());
    println!("Asosiy oqim ID:   {:?}", joriy.id());

    let h = thread::spawn(|| {
        let t = thread::current();
        println!("Yangi oqim ID:   {:?}", t.id());
    });
    h.join().unwrap();
}
```
## Tushuntirish va Mantiq:
`thread::current()` joriy oqimning meta-ma'lumotlarini (nom, id) olish imkonini beradi.
## Ishlash natijasi:
```text
Asosiy oqim nomi: Some("main")
Asosiy oqim ID:   ThreadId(...)
Yangi oqim ID:   ThreadId(...)
```

---

# 758-Topshiriq: thread::Builder yordamida oqimga nom berish va stack hajmini belgilash
## Topshiriq sharti:
`thread::Builder` orqali yangi oqim nomini 'Hisobchi' deb atang va stack hajmini 4MB qilib sozlang.
## Yechim (Rust kodi):
```rust
use std::thread;

fn main() {
    let builder = thread::Builder::new()
        .name(String::from("Hisobchi"))
        .stack_size(4 * 1024 * 1024); // 4 MB stack

    let handle = builder.spawn(|| {
        println!("Mening nomim: {}", thread::current().name().unwrap_or("Nomsiz"));
    }).unwrap();

    handle.join().unwrap();
}
```
## Tushuntirish va Mantiq:
`thread::Builder` oqim xususiyatlarini (stack hajmi, oqim nomi) operatsion tizim darajasida nozik sozlash imkonini beradi.
## Ishlash natijasi:
```text
Mening nomim: Hisobchi
```

---

# 759-Topshiriq: std::sync::mpsc::channel orqali bittalik xabar yuborish
## Topshiriq sharti:
`mpsc` kanali yordamida bir oqimdan ikkinchi oqimga matnli xabar uzating.
## Yechim (Rust kodi):
```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();

    thread::spawn(move || {
        let xabar = String::from("Salom boshqa oqimdan!");
        tx.send(xabar).unwrap();
    });

    let qabul_qilindi = rx.recv().unwrap();
    println!("Qabul qilindi: {}", qabul_qilindi);
}
```
## Tushuntirish va Mantiq:
`mpsc` (Multiple Producer, Single Consumer) kanali oqimlararo ma'lumot uzatishning xavfsiz vositasidir. `tx` yuboradi, `rx` kutib oladi.
## Ishlash natijasi:
```text
Qabul qilindi: Salom boshqa oqimdan!
```

---

# 760-Topshiriq: mpsc kanalida bir nechta xabarlarni ketma-ket yuborish
## Topshiriq sharti:
Ishchi oqim bir nechta xabarlarni kanalga yuborishi va asosiy oqim ularni qabul qilishini dasturlang.
## Yechim (Rust kodi):
```rust
use std::sync::mpsc;
use std::thread;
use std::time::Duration;

fn main() {
    let (tx, rx) = mpsc::channel();

    thread::spawn(move || {
        let xabarlar = vec!["xabar 1", "xabar 2", "xabar 3"];
        for x in xabarlar {
            tx.send(x).unwrap();
            thread::sleep(Duration::from_millis(10));
        }
    });

    while let Ok(xabar) = rx.recv() {
        println!("Kanal xabari: {}", xabar);
    }
    println!("Kanal yopildi.");
}
```
## Tushuntirish va Mantiq:
Sender (`tx`) o'z doirasidan chiqib drop bo'lganda, `rx.recv()` `Err` qaytaradi va `while let` sikli tabiiy ravishda to'xtaydi.
## Ishlash natijasi:
```text
Kanal xabari: xabar 1
Kanal xabari: xabar 2
Kanal xabari: xabar 3
Kanal yopildi.
```

---

# 761-Topshiriq: mpsc receiver ustida iterator sifatida for loop yurgizish
## Topshiriq sharti:
`rx` qabul qiluvchisini iterator sifatida to'g'ridan-to'g'ri `for` siklida ishlating.
## Yechim (Rust kodi):
```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();

    thread::spawn(move || {
        for son in 1..=4 {
            tx.send(son * 10).unwrap();
        }
    });

    for qiymat in rx {
        println!("Iteratsiya orqali olindi: {}", qiymat);
    }
}
```
## Tushuntirish va Mantiq:
`Receiver<T>` `IntoIterator` trait'ini amalga oshiradi. U barcha senderlar drop bo'lgunga qadar xabarlarni bloklanib kutadi va qabul qiladi.
## Ishlash natijasi:
```text
Iteratsiya orqali olindi: 10
Iteratsiya orqali olindi: 20
Iteratsiya orqali olindi: 30
Iteratsiya orqali olindi: 40
```

---

# 762-Topshiriq: Multiple Producer (tx.clone()) bilan bir nechta oqimdan bitta qabul qiluvchiga yuborish
## Topshiriq sharti:
Ikki xil oqim bitta kanalga xabar yuborishi uchun `tx.clone()` dan foydalaning.
## Yechim (Rust kodi):
```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();

    let tx1 = tx.clone();
    thread::spawn(move || {
        tx1.send("1-ishchidan salom").unwrap();
    });

    let tx2 = tx;
    thread::spawn(move || {
        tx2.send("2-ishchidan salom").unwrap();
    });

    for _ in 0..2 {
        println!("Qabul: {}", rx.recv().unwrap());
    }
}
```
## Tushuntirish va Mantiq:
`mpsc` nomining ma'nosi 'Multiple Producer' dir: `tx` ko'rsatkichini istalgancha klonlab har xil oqimlarga tarqatish mumkin.
## Ishlash natijasi:
```text
Qabul: 1-ishchidan salom
Qabul: 2-ishchidan salom
```

---

# 763-Topshiriq: Synchronous channel: mpsc::sync_channel bilan buferlangan aloqa
## Topshiriq sharti:
Sig'imi 1 bo'lgan `sync_channel` yordamida bufer to'lganda jo'natuvchi oqim bloklanishini ko'rsating.
## Yechim (Rust kodi):
```rust
use std::sync::mpsc;
use std::thread;
use std::time::Duration;

fn main() {
    let (tx, rx) = mpsc::sync_channel(1);

    thread::spawn(move || {
        println!("Xabar 1 yuborilmoqda...");
        tx.send(1).unwrap();
        println!("Xabar 2 yuborilmoqda (bufer to'lgani uchun bloklanadi)...");
        tx.send(2).unwrap();
        println!("Xabar 2 qabul qilingach yuborildi!");
    });

    thread::sleep(Duration::from_millis(50));
    println!("Qabul qilindi: {}", rx.recv().unwrap());
    println!("Qabul qilindi: {}", rx.recv().unwrap());
}
```
## Tushuntirish va Mantiq:
`sync_channel(N)` chegaralangan buferga ega (bounded channel). Agar buferda bo'sh joy qolmasa, `send` chaqiruvchisi joy bo'shaguncha kutadi.
## Ishlash natijasi:
```text
Xabar 1 yuborilmoqda...
Xabar 2 yuborilmoqda (bufer to'lgani uchun bloklanadi)...
Qabul qilindi: 1
Xabar 2 qabul qilingach yuborildi!
Qabul qilindi: 2
```

---

# 764-Topshiriq: try_recv() bilan bloklanmasdan xabarni tekshirish
## Topshiriq sharti:
Kanalda xabar bo'lmasa asosiy oqim to'xtab qolmasdan o'z ishini davom ettirishi uchun `try_recv`dan foydalaning.
## Yechim (Rust kodi):
```rust
use std::sync::mpsc;
use std::thread;
use std::time::Duration;

fn main() {
    let (tx, rx) = mpsc::channel();

    thread::spawn(move || {
        thread::sleep(Duration::from_millis(30));
        tx.send("Kechikkan xabar").unwrap();
    });

    for _ in 0..5 {
        match rx.try_recv() {
            Ok(x) => { println!("Xabar keldi: {}", x); break; }
            Err(_) => { println!("Hali xabar yo'q, boshqa ish bajarilmoqda..."); }
        }
        thread::sleep(Duration::from_millis(10));
    }
}
```
## Tushuntirish va Mantiq:
`try_recv()` oqimni to'xtatmaydi (non-blocking). Agar xabar bo'lsa darhol beradi, bo'lmasa `Err(TryRecvError::Empty)` qaytaradi.
## Ishlash natijasi:
```text
Hali xabar yo'q, boshqa ish bajarilmoqda...
Hali xabar yo'q, boshqa ish bajarilmoqda...
Xabar keldi: Kechikkan xabar
```

---

# 765-Topshiriq: Arc<T> (Atomic Reference Counting) bilan ko'p oqimli xotira ulashish
## Topshiriq sharti:
Bir nechta oqimlar o'rtasida umumiy o'qish uchun `Arc<Vec<i32>>` strukturasidan foydalaning.
## Yechim (Rust kodi):
```rust
use std::sync::Arc;
use std::thread;

fn main() {
    let massiv = Arc::new(vec![10, 20, 30]);
    let mut dastalar = vec![];

    for i in 0..3 {
        let massiv_klon = Arc::clone(&massiv);
        let h = thread::spawn(move || {
            println!("Oqim {} o'qidi: {}", i, massiv_klon[i]);
        });
        dastalar.push(h);
    }

    for h in dastalar {
        h.join().unwrap();
    }
}
```
## Tushuntirish va Mantiq:
`Arc<T>` (Atomic Reference Counting) ko'p oqimli tizimlarda xavfsiz umumiy egalik (shared ownership) yaratadi. `Rc` dan farqli ravishda atomik amallar ishlatadi.
## Ishlash natijasi:
```text
Oqim 0 o'qidi: 10
Oqim 1 o'qidi: 20
Oqim 2 o'qidi: 30
```

---

# 766-Topshiriq: Mutex<T> bilan ma'lumotni o'zaro bloklash
## Topshiriq sharti:
Bitta o'zgaruvchini `Mutex` ichida saqlash va uning qiymatini xavfsiz o'zgartirish dasturini yozing.
## Yechim (Rust kodi):
```rust
use std::sync::Mutex;

fn main() {
    let hisob = Mutex::new(0);

    {
        let mut qulf = hisob.lock().unwrap();
        *qulf += 10;
    }

    println!("Mutex qiymati: {:?}", hisob.lock().unwrap());
}
```
## Tushuntirish va Mantiq:
`Mutex<T>` (Mutual Exclusion) faqat bitta oqimga ma'lumotga kirish huquqini beradi. Ma'lumot qulflanganda boshqa oqimlar navbatda kutadi.
## Ishlash natijasi:
```text
Mutex qiymati: 10
```

---

# 767-Topshiriq: Arc<Mutex<T>> bilan ko'p oqimli hisoblagich (shared counter)
## Topshiriq sharti:
10 ta alohida oqim bitta hisoblagichni 1 tadan oshirib jami 10 ga yetkazuvchi dastur tuzing.
## Yechim (Rust kodi):
```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let hisoblagich = Arc::new(Mutex::new(0));
    let mut dastalar = vec![];

    for _ in 0..10 {
        let hisob_ref = Arc::clone(&hisoblagich);
        let h = thread::spawn(move || {
            let mut qulf = hisob_ref.lock().unwrap();
            *qulf += 1;
        });
        dastalar.push(h);
    }

    for h in dastalar {
        h.join().unwrap();
    }

    println!("Yakuniy hisoblagich: {}", *hisoblagich.lock().unwrap());
}
```
## Tushuntirish va Mantiq:
`Arc<Mutex<T>>` ko'p oqimli dasturlashning eng asosiy andozasidir: `Arc` barcha oqimlarga havola beradi, `Mutex` esa yozishni sinxronlaydi.
## Ishlash natijasi:
```text
Yakuniy hisoblagich: 10
```

---

# 768-Topshiriq: Deadlock (o'lik holat) xavfi va tushuntirish
## Topshiriq sharti:
Ikki oqim bir-birining qulfini kutib to'xtab qolish xavfini tushuntiruvchi mantiqni yozing.
## Yechim (Rust kodi):
```rust
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::Duration;

fn main() {
    let resurs_a = Arc::new(Mutex::new(1));
    let resurs_b = Arc::new(Mutex::new(2));

    let a1 = Arc::clone(&resurs_a);
    let b1 = Arc::clone(&resurs_b);

    // Agar oqim 1 A ni, keyin B ni olsa, oqim 2 esa aksincha B ni, keyin A ni olsa Deadlock kelib chiqadi!
    let h1 = thread::spawn(move || {
        let _qulf_a = a1.lock().unwrap();
        thread::sleep(Duration::from_millis(10));
        // let _qulf_b = b1.lock().unwrap(); // Deadlock manbasi
        println!("Oqim 1 xavfsiz tartibda ishladi");
    });

    let h2 = thread::spawn(move || {
        let _qulf_b = resurs_b.lock().unwrap();
        println!("Oqim 2 xavfsiz ishladi");
    });

    h1.join().unwrap();
    h2.join().unwrap();
}
```
## Tushuntirish va Mantiq:
Deadlock paydo bo'lmasligi uchun bir nechta qulflarni doimo qat'iy bir xil tartibda olish (masalan, avval Resurs A, keyin Resurs B) talab qilinadi.
## Ishlash natijasi:
```text
Oqim 2 xavfsiz ishladi
Oqim 1 xavfsiz tartibda ishladi
```

---

# 769-Topshiriq: try_lock bilan deadlock'dan qochish
## Topshiriq sharti:
`Mutex::try_lock` orqali agar qulf band bo'lsa darhol chekinish va boshqa ishni bajarishni ko'rsating.
## Yechim (Rust kodi):
```rust
use std::sync::Mutex;

fn main() {
    let mutex = Mutex::new(100);

    let qulf1 = mutex.lock().unwrap();

    match mutex.try_lock() {
        Ok(qulf2) => println!("Ikkinchi qulf olindi: {}", *qulf2),
        Err(_) => println!("Qulf band! Bloklanmasdan orqaga qaytildi."),
    }

    println!("Asl qulf qiymati: {}", *qulf1);
}
```
## Tushuntirish va Mantiq:
`try_lock()` oqimni uxlatmaydi. Agar qulf olinmasa `Err(TryLockError::WouldBlock)` beradi va deadlock bo'lishiga yo'l qo'ymaydi.
## Ishlash natijasi:
```text
Qulf band! Bloklanmasdan orqaga qaytildi.
Asl qulf qiymati: 100
```

---

# 770-Topshiriq: RwLock<T> (Read-Write Lock) bilan ko'p o'qish, bir yozish
## Topshiriq sharti:
Bir vaqtning o'zida bir nechta oqim ma'lumotni o'qishi, lekin faqat bittasi yoza olishi uchun `RwLock`dan foydalaning.
## Yechim (Rust kodi):
```rust
use std::sync::RwLock;

fn main() {
    let lock = RwLock::new(5);

    // Bir nechta o'qish qulflari (readers)
    {
        let r1 = lock.read().unwrap();
        let r2 = lock.read().unwrap();
        println!("O'qish: {} va {}", *r1, *r2);
    } // r1 va r2 bu yerda drop bo'ladi

    // Faqat bitta yozish qulfi (writer)
    {
        let mut w = lock.write().unwrap();
        *w += 10;
    }

    println!("Yangi qiymat: {}", *lock.read().unwrap());
}
```
## Tushuntirish va Mantiq:
`RwLock` o'qish amallari ko'p, yozish kam bo'lgan tizimlarda `Mutex`ga qaraganda ancha yuqori unumdorlik beradi.
## Ishlash natijasi:
```text
O'qish: 5 va 5
Yangi qiymat: 15
```

---

# 771-Topshiriq: RwLock: Bir nechta oqimdan parallel read() olish
## Topshiriq sharti:
3 ta oqim bir vaqtda bitta `RwLock`ni o'qishini namoyish qiling.
## Yechim (Rust kodi):
```rust
use std::sync::{Arc, RwLock};
use std::thread;

fn main() {
    let umumiy_matn = Arc::new(RwLock::new(String::from("Umumiy Ma'lumot")));
    let mut dastalar = vec![];

    for i in 1..=3 {
        let matn_ref = Arc::clone(&umumiy_matn);
        dastalar.push(thread::spawn(move || {
            let r = matn_ref.read().unwrap();
            println!("Oqim {} o'qidi: {}", i, *r);
        }));
    }

    for d in dastalar {
        d.join().unwrap();
    }
}
```
## Tushuntirish va Mantiq:
Har bir reader boshqa readerlarni bloklamaydi, ular parallel ravishda xotirani o'qiy oladi.
## Ishlash natijasi:
```text
Oqim 1 o'qidi: Umumiy Ma'lumot
Oqim 2 o'qidi: Umumiy Ma'lumot
Oqim 3 o'qidi: Umumiy Ma'lumot
```

---

# 772-Topshiriq: RwLock vs Mutex tezlik va vaziyat taqqoslash
## Topshiriq sharti:
Qaysi holatlarda Mutex, qaysi holatlarda RwLock tanlanishi kerakligini namoyish qiluvchi strukturani ko'rsating.
## Yechim (Rust kodi):
```rust
use std::sync::{Mutex, RwLock};

struct ServerHolati {
    foydalanuvchilar_soni: Mutex<u64>, // Tez-tez yangilanadi -> Mutex
    konfiguratsiya: RwLock<String>,     // Kam o'zgaradi, ko'p o'qiladi -> RwLock
}

fn main() {
    let holat = ServerHolati {
        foydalanuvchilar_soni: Mutex::new(0),
        konfiguratsiya: RwLock::new(String::from("v1.0-prod")),
    };

    *holat.foydalanuvchilar_soni.lock().unwrap() += 1;
    let cfg = holat.konfiguratsiya.read().unwrap();

    println!("Foydalanuvchilar: {}, Konfiguratsiya: {}", *holat.foydalanuvchilar_soni.lock().unwrap(), *cfg);
}
```
## Tushuntirish va Mantiq:
Tez-tez yoziladigan kichik ma'lumotlar uchun `Mutex` yengilroq. O'qish 90%+ bo'lgan katta strukturalar uchun `RwLock` afzal.
## Ishlash natijasi:
```text
Foydalanuvchilar: 1, Konfiguratsiya: v1.0-prod
```

---

# 773-Topshiriq: std::sync::atomic::AtomicBool bilan to'xtatish bayrog'i
## Topshiriq sharti:
`AtomicBool` yordamida ikkinchi oqimga to'xtash signalini uzating.
## Yechim (Rust kodi):
```rust
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;
use std::thread;
use std::time::Duration;

fn main() {
    let ishlamoqda = Arc::new(AtomicBool::new(true));
    let ish_flag = Arc::clone(&ishlamoqda);

    let h = thread::spawn(move || {
        let mut sanagich = 0;
        while ish_flag.load(Ordering::Relaxed) {
            sanagich += 1;
            thread::sleep(Duration::from_millis(5));
        }
        println!("Ishchi to'xtatildi, qilingan ish: {}", sanagich);
    });

    thread::sleep(Duration::from_millis(20));
    ishlamoqda.store(false, Ordering::Relaxed);
    h.join().unwrap();
}
```
## Tushuntirish va Mantiq:
`Atomic` tiplar qulfsiz (lock-free) va CPU apparat darajasida sinxronizatsiya qilinadi, bu qulflarga qaraganda juda kam resurs sarflaydi.
## Ishlash natijasi:
```text
Ishchi to'xtatildi, qilingan ish: ...
```

---

# 774-Topshiriq: AtomicUsize bilan qulfsiz (lock-free) hisoblagich
## Topshiriq sharti:
`AtomicUsize::fetch_add` orqali 10 ta oqimdan umumiy hisoblagichni qulfsiz oshiring.
## Yechim (Rust kodi):
```rust
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;
use std::thread;

fn main() {
    let hisob = Arc::new(AtomicUsize::new(0));
    let mut dastalar = vec![];

    for _ in 0..10 {
        let hisob_ref = Arc::clone(&hisob);
        dastalar.push(thread::spawn(move || {
            for _ in 0..100 {
                hisob_ref.fetch_add(1, Ordering::SeqCst);
            }
        }));
    }

    for d in dastalar {
        d.join().unwrap();
    }

    println!("Yakuniy atomik hisob: {}", hisob.load(Ordering::SeqCst));
}
```
## Tushuntirish va Mantiq:
`fetch_add` atomik tarzda qiymatni oshiradi va eski qiymatni qaytaradi. Hech qanday mutex yoki bloklanish ro'y bermaydi.
## Ishlash natijasi:
```text
Yakuniy atomik hisob: 1000
```

---

# 775-Topshiriq: Ordering tushunchasi: SeqCst vs Relaxed
## Topshiriq sharti:
Xotira ketma-ketligi (memory ordering) bo'yicha `SeqCst` va `Relaxed` farqini tushuntiruvchi misol.
## Yechim (Rust kodi):
```rust
use std::sync::atomic::{AtomicI32, Ordering};

fn main() {
    let atom = AtomicI32::new(10);

    // Relaxed: faqat atomiklik kafolatlanadi, boshqa o'zgaruvchilar bilan tartib kafolatlanmaydi
    atom.store(20, Ordering::Relaxed);
    let val1 = atom.load(Ordering::Relaxed);

    // SeqCst (Sequentially Consistent): butun tizimda qat'iy global ketma-ketlik kafolatlanadi
    atom.store(30, Ordering::SeqCst);
    let val2 = atom.load(Ordering::SeqCst);

    println!("Relaxed: {}, SeqCst: {}", val1, val2);
}
```
## Tushuntirish va Mantiq:
`Ordering::SeqCst` eng xavfsiz va qat'iy tartibdir. `Ordering::Relaxed` eng tez ishlaydi, ammo operatsiyalar protsessor tomonidan o'rni almashtirilishi mumkin.
## Ishlash natijasi:
```text
Relaxed: 20, SeqCst: 30
```

---

# 776-Topshiriq: Atomic compare_exchange (CAS) operatsiyasi
## Topshiriq sharti:
Qiymat kutilganidek bo'lsagina uni yangilovchi Compare-And-Swap (CAS) operatsiyasini dasturlang.
## Yechim (Rust kodi):
```rust
use std::sync::atomic::{AtomicI32, Ordering};

fn main() {
    let atom = AtomicI32::new(100);

    // Agar joriy qiymat 100 bo'lsa, uni 200 ga o'zgartir
    let muvaffaqiyat = atom.compare_exchange(100, 200, Ordering::SeqCst, Ordering::SeqCst);
    println!("Almashtirish natijasi: {:?}", muvaffaqiyat);
    println!("Yangi qiymat: {}", atom.load(Ordering::SeqCst));

    // Endi yana 100 ga teng deb o'zgartirmoqchi bo'lsak, muvaffaqiyatsiz bo'ladi
    let xato = atom.compare_exchange(100, 300, Ordering::SeqCst, Ordering::SeqCst);
    println!("Noto'g'ri taxmin natijasi: {:?}", xato);
}
```
## Tushuntirish va Mantiq:
`compare_exchange` zamonaviy lock-free algoritmlarning (navbatlar, stacklar) asosiy poydevori hisoblanadi.
## Ishlash natijasi:
```text
Almashtirish natijasi: Ok(100)
Yangi qiymat: 200
Noto'g'ri taxmin natijasi: Err(200)
```

---

# 777-Topshiriq: Send trait'i: Oqimlararo uzatish mumkin bo'lgan tiplar
## Topshiriq sharti:
Nima sababdan `Send` trait'i ob'ekt egaligini boshqa oqimga o'tkazishni kafolatlashini tushuntiring.
## Yechim (Rust kodi):
```rust
fn tekshir_send<T: Send>() {
    println!("Ushbu tur Send trait'ini amalga oshiradi va oqimlararo uzatilishi mumkin!");
}

fn main() {
    tekshir_send::<i32>();
    tekshir_send::<String>();
    tekshir_send::<Vec<u8>>();
    // tekshir_send::<*const i32>(); // Bu qator xato beradi, chunki raw pointer !Send
}
```
## Tushuntirish va Mantiq:
Rust'da deyarli barcha tiplar avtomatik `Send` hisoblanadi, agar ular oqimlar o'rtasida ko'chirilganda xavf tug'dirmasa.
## Ishlash natijasi:
```text
Ushbu tur Send trait'ini amalga oshiradi va oqimlararo uzatilishi mumkin!
Ushbu tur Send trait'ini amalga oshiradi va oqimlararo uzatilishi mumkin!
Ushbu tur Send trait'ini amalga oshiradi va oqimlararo uzatilishi mumkin!
```

---

# 778-Topshiriq: Sync trait'i: Oqimlararo xavfsiz umumiy foydalanish
## Topshiriq sharti:
Agar `&T` turi `Send` bo'lsa, `T` turi `Sync` hisoblanishini tushuntiruvchi misol tuzing.
## Yechim (Rust kodi):
```rust
fn tekshir_sync<T: Sync>() {
    println!("Ushbu tur Sync trait'iga ega va bir vaqtda ko'p oqimdan o'qilishi xavfsiz!");
}

fn main() {
    tekshir_sync::<i32>();
    tekshir_sync::<std::sync::Mutex<i32>>();
    // tekshir_sync::<std::cell::RefCell<i32>>(); // Bu qator xato beradi, chunki RefCell !Sync
}
```
## Tushuntirish va Mantiq:
`T: Sync` bo'lsa, unga bo'lgan havolani (`&T`) xavfsiz tarzda bir nechta oqimlarga uzatish mumkin. `Mutex<T>` `Sync`dir, lekin `RefCell<T>` emas.
## Ishlash natijasi:
```text
Ushbu tur Sync trait'iga ega va bir vaqtda ko'p oqimdan o'qilishi xavfsiz!
Ushbu tur Sync trait'iga ega va bir vaqtda ko'p oqimdan o'qilishi xavfsiz!
```

---

# 779-Topshiriq: !Send va !Sync tiplar: Rc nima uchun multithreadingda ishlamaydi
## Topshiriq sharti:
`Rc<T>` non-atomic hisoblagichga ega bo'lgani sababli `!Send` va `!Sync` ekanligini ko'rsating.
## Yechim (Rust kodi):
```rust
// use std::rc::Rc;
// use std::thread;

fn main() {
    // let rc = Rc::new(10);
    // thread::spawn(move || {
    //     println!("{}", rc);
    // });
    // Yuqoridagi kod kompilyatsiya bo'lmaydi: `Rc<i32>` cannot be sent between threads safely
    println!("Rc multithreading uchun yaroqsiz (!Send), o'rniga Arc ishlatilishi shart!");
}
```
## Tushuntirish va Mantiq:
`Rc<T>` oddiy integer hisoblagichdan foydalanadi. Agar ikki oqim bir vaqtda uni klonlasa, data race yuzaga keladi. Shuning uchun Rust buni kompilyatsiya vaqtidayoq taqiqlaydi.
## Ishlash natijasi:
```text
Rc multithreading uchun yaroqsiz (!Send), o'rniga Arc ishlatilishi shart!
```

---

# 780-Topshiriq: Mutex poisoning holatini tushunish va qayta ishlash
## Topshiriq sharti:
Qulfni ushlab turgan oqim panic qilganda Mutex 'poisoned' (zaharlangan) bo'lishi va uni `into_inner()` bilan qutqarishni ko'rsating.
## Yechim (Rust kodi):
```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let lock = Arc::new(Mutex::new(42));
    let l_klon = Arc::clone(&lock);

    let _ = thread::spawn(move || {
        let _qulf = l_klon.lock().unwrap();
        panic!("Kutilmagan xato ro'y berdi!");
    }).join();

    // Endi lock zaharlangan (PoisonError)
    match lock.lock() {
        Ok(_) => println!("Qulf sog'lom"),
        Err(poison_err) => {
            println!("Mutex zaharlangan! Ammo ma'lumotni saqlab qolish mumkin.");
            let data = poison_err.into_inner();
            println!("Qutqarilgan qiymat: {}", *data);
        }
    }
}
```
## Tushuntirish va Mantiq:
Agar oqim Mutexni ushlab turganida panic qilsa, ma'lumot noaniq holatda qolgan bo'lishi mumkinligi uchun Mutex zaharlanadi (Poisoned).
## Ishlash natijasi:
```text
Mutex zaharlangan! Ammo ma'lumotni saqlab qolish mumkin.
Qutqarilgan qiymat: 42
```

---

# 781-Topshiriq: std::sync::Condvar (Condition Variable) orqali oqimlarni uyg'otish
## Topshiriq sharti:
`Condvar` yordamida ikkinchi oqim shart bajarilishini kutib turishi va birinchi oqim uni `notify_one()` bilan uyg'otishini ko'rsating.
## Yechim (Rust kodi):
```rust
use std::sync::{Arc, Mutex, Condvar};
use std::thread;
use std::time::Duration;

fn main() {
    let juftlik = Arc::new((Mutex::new(false), Condvar::new()));
    let juftlik_klon = Arc::clone(&juftlik);

    thread::spawn(move || {
        let (qulf, cvar) = &*juftlik_klon;
        thread::sleep(Duration::from_millis(50));
        let mut tayyor = qulf.lock().unwrap();
        *tayyor = true;
        println!("Ish bajarildi, kutayotgan oqimga signal berilmoqda...");
        cvar.notify_one();
    });

    let (qulf, cvar) = &*juftlik;
    let mut tayyor = qulf.lock().unwrap();
    while !*tayyor {
        tayyor = cvar.wait(tayyor).unwrap();
    }
    println!("Asosiy oqim signalni oldi va davom etmoqda!");
}
```
## Tushuntirish va Mantiq:
`Condvar::wait` oqimni xavfsiz uxlatadi va uning Mutexini vaqtincha ochadi. `notify_one()` signal berganda esa qayta qulflab uyg'otadi.
## Ishlash natijasi:
```text
Ish bajarildi, kutayotgan oqimga signal berilmoqda...
Asosiy oqim signalni oldi va davom etmoqda!
```

---

# 782-Topshiriq: Condvar bilan ko'p oqimlarni ommaviy uyg'otish: notify_all
## Topshiriq sharti:
`cvar.notify_all()` yordamida bir vaqtda kutib turgan barcha oqimlarga 'Start' signali bering.
## Yechim (Rust kodi):
```rust
use std::sync::{Arc, Mutex, Condvar};
use std::thread;

fn main() {
    let start_line = Arc::new((Mutex::new(false), Condvar::new()));
    let mut dastalar = vec![];

    for i in 1..=3 {
        let juft = Arc::clone(&start_line);
        dastalar.push(thread::spawn(move || {
            let (qulf, cvar) = &*juft;
            let mut start = qulf.lock().unwrap();
            while !*start {
                start = cvar.wait(start).unwrap();
            }
            println!("Yuguruvchi #{} marraga qarab yugurdi!", i);
        }));
    }

    let (qulf, cvar) = &*start_line;
    {
        let mut s = qulf.lock().unwrap();
        *s = true;
    }
    cvar.notify_all();

    for d in dastalar {
        d.join().unwrap();
    }
}
```
## Tushuntirish va Mantiq:
`notify_all()` kutish holatida turgan barcha oqimlarni baravariga uyg'otish uchun ishlatiladi.
## Ishlash natijasi:
```text
Yuguruvchi #1 marraga qarab yugurdi!
Yuguruvchi #2 marraga qarab yugurdi!
Yuguruvchi #3 marraga qarab yugurdi!
```

---

# 783-Topshiriq: std::sync::Barrier orqali belgilangan oqimlarni kutish
## Topshiriq sharti:
3 ta oqim bir vaqtda to'siqqa (`Barrier`) kelguncha bir-birini kutishini dasturlang.
## Yechim (Rust kodi):
```rust
use std::sync::{Arc, Barrier};
use std::thread;

fn main() {
    let tosiq = Arc::new(Barrier::new(3));
    let mut dastalar = vec![];

    for i in 1..=3 {
        let b = Arc::clone(&tosiq);
        dastalar.push(thread::spawn(move || {
            println!("Oqim {} tayyorgarlikni yakunladi", i);
            b.wait(); // Barcha 3 ta oqim yetib kelguncha to'xtaydi
            println!("Oqim {} to'siqdan o'tdi!", i);
        }));
    }

    for d in dastalar {
        d.join().unwrap();
    }
}
```
## Tushuntirish va Mantiq:
`Barrier` ko'p bosqichli parallel hisoblashlarda oqimlarning sinxron bir maromda qadam tashlashini ta'minlash uchun xizmat qiladi.
## Ishlash natijasi:
```text
Oqim 1 tayyorgarlikni yakunladi
Oqim 2 tayyorgarlikni yakunladi
Oqim 3 tayyorgarlikni yakunladi
Oqim 1 to'siqdan o'tdi!
Oqim 2 to'siqdan o'tdi!
Oqim 3 to'siqdan o'tdi!
```

---

# 784-Topshiriq: std::sync::Once bilan bir martalik global initsializatsiya
## Topshiriq sharti:
Bir nechta oqim murojaat qilganda ham funksiya faqat 1 marta bajarilishini `Once` bilan kafolatlang.
## Yechim (Rust kodi):
```rust
use std::sync::Once;
use std::thread;

static INITS_QILINDI: Once = Once::new();

fn global_sozlash() {
    println!(">>> OGOHLANTIRISH: Tizim faqat 1 marta global sozlandi! <<<");
}

fn main() {
    let mut dastalar = vec![];

    for _ in 0..4 {
        dastalar.push(thread::spawn(|| {
            INITS_QILINDI.call_once(|| {
                global_sozlash();
            });
            println!("Oqim ishladi");
        }));
    }

    for d in dastalar {
        d.join().unwrap();
    }
}
```
## Tushuntirish va Mantiq:
`Once::call_once` qancha oqim bir vaqtda chaqirishidan qat'i nazar, ichidagi closure faqat birinchi oqim tomonidan bir marotaba bajarilishini ta'minlaydi.
## Ishlash natijasi:
```text
>>> OGOHLANTIRISH: Tizim faqat 1 marta global sozlandi! <<<
Oqim ishladi
Oqim ishladi
Oqim ishladi
Oqim ishladi
```

---

# 785-Topshiriq: std::sync::OnceLock bilan xavfsiz lazy global o'zgaruvchi
## Topshiriq sharti:
Rust 1.70+ versiyasida qo'shilgan `OnceLock<T>` bilan global konfiguratsiyani yaratish.
## Yechim (Rust kodi):
```rust
use std::sync::OnceLock;

static MAXSUS_KONFIG: OnceLock<String> = OnceLock::new();

fn konfigni_ol() -> &'static String {
    MAXSUS_KONFIG.get_or_init(|| {
        println!("Konfiguratsiya birinchi marta yuklanmoqda...");
        String::from("PORT=8080;ENV=PROD")
    })
}

fn main() {
    println!("1-murojaat: {}", konfigni_ol());
    println!("2-murojaat: {}", konfigni_ol());
}
```
## Tushuntirish va Mantiq:
`OnceLock<T>` qulflarsiz xavfsiz global statik o'zgaruvchilarni (Lazy static) dasturlash imkonini beradi.
## Ishlash natijasi:
```text
Konfiguratsiya birinchi marta yuklanmoqda...
1-murojaat: PORT=8080;ENV=PROD
2-murojaat: PORT=8080;ENV=PROD
```

---

# 786-Topshiriq: thread_local! makrosi orqali oqimga xos alohida xotira
## Topshiriq sharti:
Har bir oqim o'zining mustaqil hisoblagichiga ega bo'lishi uchun `thread_local!` e'lon qiling.
## Yechim (Rust kodi):
```rust
use std::cell::Cell;
use std::thread;

thread_local! {
    static OQIM_HISOB: Cell<u32> = Cell::new(0);
}

fn main() {
    OQIM_HISOB.with(|c| c.set(100));

    let h = thread::spawn(|| {
        OQIM_HISOB.with(|c| {
            c.set(50);
            println!("Yangi oqim hisobi: {}", c.get());
        });
    });

    h.join().unwrap();
    OQIM_HISOB.with(|c| {
        println!("Asosiy oqim hisobi o'zgarmadi: {}", c.get());
    });
}
```
## Tushuntirish va Mantiq:
`thread_local!` har bir oqim uchun xotirada alohida o'zgaruvchi nusxasini yaratadi. Oqimlar bir-birining qiymatini ko'rmaydi va qulflash talab qilinmaydi.
## Ishlash natijasi:
```text
Yangi oqim hisobi: 50
Asosiy oqim hisobi o'zgarmadi: 100
```

---

# 787-Topshiriq: ThreadLocal RefCell bilan oqim ichidagi kesh
## Topshiriq sharti:
Har bir oqim o'ziga tegishli matnli keshga ega bo'lishini `thread_local!` va `RefCell` bilan tashkil qiling.
## Yechim (Rust kodi):
```rust
use std::cell::RefCell;
use std::thread;

thread_local! {
    static OQIM_KESHI: RefCell<Vec<String>> = RefCell::new(vec![]);
}

fn keshga_yoz(matn: &str) {
    OQIM_KESHI.with(|k| k.borrow_mut().push(matn.to_string()));
}

fn main() {
    let h1 = thread::spawn(|| {
        keshga_yoz("A1");
        keshga_yoz("A2");
        OQIM_KESHI.with(|k| println!("Oqim 1 keshi: {:?}", *k.borrow()));
    });

    let h2 = thread::spawn(|| {
        keshga_yoz("B1");
        OQIM_KESHI.with(|k| println!("Oqim 2 keshi: {:?}", *k.borrow()));
    });

    h1.join().unwrap();
    h2.join().unwrap();
}
```
## Tushuntirish va Mantiq:
ThreadLocal o'zgaruvchilar bitta oqim ichida bo'lgani sababli, `Arc` yoki `Mutex` o'rniga yengil `RefCell` ishlatish xavfsizdir.
## Ishlash natijasi:
```text
Oqim 1 keshi: ["A1", "A2"]
Oqim 2 keshi: ["B1"]
```

---

# 788-Topshiriq: Parallel hisoblash: 1 dan N gacha yig'indini 4 ta oqimga bo'lib hisoblash
## Topshiriq sharti:
1 dan 1,000,000 gacha sonlar yig'indisini 4 ta oraliqqa bo'lib parallel hisoblang.
## Yechim (Rust kodi):
```rust
use std::thread;

fn main() {
    let oraliqlar = vec![
        (1..=250_000),
        (250_001..=500_000),
        (500_001..=750_000),
        (750_001..=1_000_000),
    ];

    let mut dastalar = vec![];

    for oraliq in oraliqlar {
        dastalar.push(thread::spawn(move || {
            let mut yigindi: u64 = 0;
            for son in oraliq {
                yigindi += son;
            }
            yigindi
        }));
    }

    let mut umumiy_yigindi: u64 = 0;
    for d in dastalar {
        umumiy_yigindi += d.join().unwrap();
    }

    println!("1 dan 1,000,000 gacha sonlar parallel yig'indisi: {}", umumiy_yigindi);
    assert_eq!(umumiy_yigindi, 1_000_000u64 * 1_000_001 / 2);
}
```
## Tushuntirish va Mantiq:
Vazifalarni oraliqlarga bo'lib (chunking) har birini alohida yadroda hisoblash CPU intensiv topshiriqlarni bir necha baravar tezlashtiradi.
## Ishlash natijasi:
```text
1 dan 1,000,000 gacha sonlar parallel yig'indisi: 500000500000
```

---

# 789-Topshiriq: Parallel massiv filtrlash (Map-Reduce modeli)
## Topshiriq sharti:
Katta massivdan juft sonlarni parallel qidirib topib umumiy natijaga birlashtiring.
## Yechim (Rust kodi):
```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let sonlar = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    let (tx, rx) = mpsc::channel();

    // 2 ta qismga bo'lamiz
    let bolak1 = sonlar[..5].to_vec();
    let bolak2 = sonlar[5..].to_vec();

    let tx1 = tx.clone();
    thread::spawn(move || {
        let juftlar: Vec<i32> = bolak1.into_iter().filter(|x| x % 2 == 0).collect();
        tx1.send(juftlar).unwrap();
    });

    thread::spawn(move || {
        let juftlar: Vec<i32> = bolak2.into_iter().filter(|x| x % 2 == 0).collect();
        tx.send(juftlar).unwrap();
    });

    let mut barcha_juftlar = vec![];
    for _ in 0..2 {
        barcha_juftlar.extend(rx.recv().unwrap());
    }

    barcha_juftlar.sort();
    println!("Filtrlangan juft sonlar: {:?}", barcha_juftlar);
}
```
## Tushuntirish va Mantiq:
Map-Reduce modeli: ma'lumotlar oqimlarga bo'lib beriladi (Map), so'ngra oraliq natijalar bitta markaziy kanalga yig'iladi (Reduce).
## Ishlash natijasi:
```text
Filtrlangan juft sonlar: [2, 4, 6, 8, 10]
```

---

# 790-Topshiriq: Oddiy Thread Pool (oqimlar havzasi) prototipi
## Topshiriq sharti:
Ishchi oqimlarni oldindan yaratib qo'yib kanal orqali vazifalar (Jobs) yuboruvchi Thread Pool quring.
## Yechim (Rust kodi):
```rust
use std::sync::{mpsc, Arc, Mutex};
use std::thread;

type Ish = Box<dyn FnOnce() + Send + 'static>;

struct OddiyThreadPool {
    ishchilar: Vec<thread::JoinHandle<()>>,
    yuboruvchi: mpsc::Sender<Ish>,
}

impl OddiyThreadPool {
    fn new(soni: usize) -> Self {
        let (tx, rx) = mpsc::channel();
        let umumiy_rx = Arc::new(Mutex::new(rx));
        let mut ishchilar = vec![];

        for _ in 0..soni {
            let rx_klon = Arc::clone(&umumiy_rx);
            let h = thread::spawn(move || loop {
                let ish = {
                    let qulf = rx_klon.lock().unwrap();
                    match qulf.recv() {
                        Ok(vazifa) => vazifa,
                        Err(_) => break, // Kanal yopildi
                    }
                };
                ish();
            });
            ishchilar.push(h);
        }

        OddiyThreadPool { ishchilar, yuboruvchi: tx }
    }

    fn bajar<F>(&self, f: F)
    where
        F: FnOnce() + Send + 'static,
    {
        self.yuboruvchi.send(Box::new(f)).unwrap();
    }
}

fn main() {
    let pool = OddiyThreadPool::new(2);
    for i in 1..=3 {
        pool.bajar(move || {
            println!("Vazifa #{} ishchi tomonidan bajarildi", i);
        });
    }
    std::thread::sleep(std::time::Duration::from_millis(50));
}
```
## Tushuntirish va Mantiq:
Thread Pool har bir vazifa uchun yangi oqim ochish xarajatlarini (overhead) yo'qotadi va mavjud oqimlardan qayta foydalanadi.
## Ishlash natijasi:
```text
Vazifa #1 ishchi tomonidan bajarildi
Vazifa #2 ishchi tomonidan bajarildi
Vazifa #3 ishchi tomonidan bajarildi
```

---

# 791-Topshiriq: Graceful Shutdown: Oqimlarni xavfsiz to'xtatish
## Topshiriq sharti:
Sender'ni drop qilish orqali ishchi oqimlarga tugash signalini berib ularning barchasini `join` qilish.
## Yechim (Rust kodi):
```rust
use std::sync::{mpsc, Arc, Mutex};
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();
    let rx = Arc::new(Mutex::new(rx));

    let mut ishchilar = vec![];
    for i in 1..=2 {
        let rx_klon = Arc::clone(&rx);
        ishchilar.push(thread::spawn(move || {
            while let Ok(xabar) = rx_klon.lock().unwrap().recv() {
                println!("Ishchi {} bajardi: {}", i, xabar);
            }
            println!("Ishchi {} to'xtadi", i);
        }));
    }

    tx.send("Ish 1").unwrap();
    tx.send("Ish 2").unwrap();
    drop(tx); // Kanalni yopamiz (Graceful shutdown)

    for h in ishchilar {
        h.join().unwrap();
    }
    println!("Barcha ishchilar xavfsiz to'xtatildi.");
}
```
## Tushuntirish va Mantiq:
`drop(tx)` qilinganda `recv()` xato qaytaradi va oqimlar sikldan chiqib xotirani tozalagan holda yakunlanadi.
## Ishlash natijasi:
```text
Ishchi 1 bajardi: Ish 1
Ishchi 2 bajardi: Ish 2
Ishchi 1 to'xtadi
Ishchi 2 to'xtadi
Barcha ishchilar xavfsiz to'xtatildi.
```

---

# 792-Topshiriq: Producer-Consumer navbati (Ring Buffer / Channel)
## Topshiriq sharti:
Ishlab chiqaruvchi (Producer) tez xabar qo'shishi, Iste'molchi (Consumer) esa sekinroq qayta ishlashi modelini quring.
## Yechim (Rust kodi):
```rust
use std::sync::mpsc;
use std::thread;
use std::time::Duration;

fn main() {
    let (tx, rx) = mpsc::sync_channel(2);

    let ishlab_chiqaruvchi = thread::spawn(move || {
        for mahsulot in 1..=4 {
            println!("+ Mahsulot #{} ishlab chiqarildi", mahsulot);
            tx.send(mahsulot).unwrap();
        }
    });

    let istemolchi = thread::spawn(move || {
        while let Ok(m) = rx.recv() {
            println!("- Mahsulot #{} iste'mol qilindi", m);
            thread::sleep(Duration::from_millis(15));
        }
    });

    ishlab_chiqaruvchi.join().unwrap();
    istemolchi.join().unwrap();
}
```
## Tushuntirish va Mantiq:
Producer-Consumer andozasi yuklamani tekislash va turli tezlikdagi quyi tizimlarni bufer orqali bog'lashda qo'llaniladi.
## Ishlash natijasi:
```text
+ Mahsulot #1 ishlab chiqarildi
+ Mahsulot #2 ishlab chiqarildi
- Mahsulot #1 iste'mol qilindi
+ Mahsulot #3 ishlab chiqarildi
- Mahsulot #2 iste'mol qilindi
+ Mahsulot #4 ishlab chiqarildi
- Mahsulot #3 iste'mol qilindi
- Mahsulot #4 iste'mol qilindi
```

---

# 793-Topshiriq: Prioritetli vazifalar taqsimlovchisi
## Topshiriq sharti:
Yuqori prioritetli vazifalarni oldin bajaruvchi maxsus ko'p oqimli dispatcher prototipini yozing.
## Yechim (Rust kodi):
```rust
use std::sync::{Arc, Mutex};
use std::collections::BinaryHeap;

#[derive(Eq, PartialEq, Ord, PartialOrd)]
struct Vazifa {
    prioritet: u32,
    nomi: &'static str,
}

fn main() {
    let navbat = Arc::new(Mutex::new(BinaryHeap::new()));

    {
        let mut q = navbat.lock().unwrap();
        q.push(Vazifa { prioritet: 1, nomi: "Kam muhim vazifa" });
        q.push(Vazifa { prioritet: 10, nomi: "Shoshilinch vazifa" });
        q.push(Vazifa { prioritet: 5, nomi: "O'rtacha vazifa" });
    }

    let n_ref = Arc::clone(&navbat);
    let h = std::thread::spawn(move || {
        let mut q = n_ref.lock().unwrap();
        while let Some(v) = q.pop() {
            println!("Bajarildi: {} (Prioritet: {})", v.nomi, v.prioritet);
        }
    });

    h.join().unwrap();
}
```
## Tushuntirish va Mantiq:
`BinaryHeap` orqali har doim eng katta prioritetli vazifa birinchi bo'lib qayta ishlanishi ta'minlanadi.
## Ishlash natijasi:
```text
Bajarildi: Shoshilinch vazifa (Prioritet: 10)
Bajarildi: O'rtacha vazifa (Prioritet: 5)
Bajarildi: Kam muhim vazifa (Prioritet: 1)
```

---

# 794-Topshiriq: Parallel qidiruv: Matndan so'zni oqimlar orqali topish
## Topshiriq sharti:
Katta matn qatorlaridan kerakli kalit so'zni 2 ta oqimda parallel qidirish dasturini tuzing.
## Yechim (Rust kodi):
```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let qatorlar = vec![
        "Rust xavfsiz til",
        "Python tez dasturlanadi",
        "Rust multithreading juda kuchli",
        "C++ past darajali til",
    ];

    let (tx, rx) = mpsc::channel();
    let kalit = "Rust";

    let yarmi = qatorlar.len() / 2;
    let qism1 = qatorlar[..yarmi].to_vec();
    let qism2 = qatorlar[yarmi..].to_vec();

    for qism in vec![qism1, qism2] {
        let t = tx.clone();
        thread::spawn(move || {
            for q in qism {
                if q.contains(kalit) {
                    t.send(q).unwrap();
                }
            }
        });
    }
    drop(tx);

    println!("Topilgan qatorlar:");
    for topildi in rx {
        println!(" - {}", topildi);
    }
}
```
## Tushuntirish va Mantiq:
Matnli korpuslarni parallel skanerlash va filtrlash orqali qidiruv tizimlarining tezligi oshiriladi.
## Ishlash natijasi:
```text
Topilgan qatorlar:
 - Rust xavfsiz til
 - Rust multithreading juda kuchli
```

---

# 795-Topshiriq: Parallel Matrix Multiplication (Matritsalarni ko'paytirish)
## Topshiriq sharti:
2x2 matritsaning har bir qatorini alohida oqimda hisoblovchi parallel dastur yozing.
## Yechim (Rust kodi):
```rust
use std::thread;

fn main() {
    let a = [[1, 2], [3, 4]];
    let b = [[5, 6], [7, 8]];

    let mut dastalari = vec![];

    for i in 0..2 {
        let qator_a = a[i];
        let ustunlar_b = b;
        dastalari.push(thread::spawn(move || {
            let mut natija_qator = [0, 0];
            for j in 0..2 {
                natija_qator[j] = qator_a[0] * ustunlar_b[0][j] + qator_a[1] * ustunlar_b[1][j];
            }
            natija_qator
        }));
    }

    let mut natija = [[0, 0], [0, 0]];
    for (i, h) in dastalari.into_iter().enumerate() {
        natija[i] = h.join().unwrap();
    }

    println!("Natijaviy matritsa: {:?}", natija);
}
```
## Tushuntirish va Mantiq:
Matritsa ko'paytirish qatorlari bir-biriga bog'liq bo'lmagani sababli uni parallel oqimlarga bo'lish eng ideal hisoblash shaklidir.
## Ishlash natijasi:
```text
Natijaviy matritsa: [[19, 22], [43, 50]]
```

---

# 796-Topshiriq: Rayon kutubxonasi arxitekturasi: par_iter() nima
## Topshiriq sharti:
Katta ma'lumotlarni parallel qayta ishlash uchun Rayon work-stealing falsafasini tushuntiring.
## Yechim (Rust kodi):
```rust
// Rayon ekvivalenti: standart kutubxonadagi chunking bilan parallel iteratsiya
use std::thread;

fn main() {
    let massiv: Vec<i32> = (1..=8).collect();
    let bolak_hajmi = 2;

    let mut dastalar = vec![];
    for chunk in massiv.chunks(bolak_hajmi) {
        let bolak = chunk.to_vec();
        dastalar.push(thread::spawn(move || {
            bolak.into_iter().map(|x| x * x).collect::<Vec<i32>>()
        }));
    }

    let mut natijalar = vec![];
    for d in dastalar {
        natijalar.extend(d.join().unwrap());
    }

    println!("Parallel kvadratlar: {:?}", natijalar);
}
```
## Tushuntirish va Mantiq:
Rayon kutubxonasi `par_iter()` orqali ma'lumotlarni o'zi avtomatik bo'laklarga ajratib tizimdagi barcha protsessor yadrolariga taqsimlaydi.
## Ishlash natijasi:
```text
Parallel kvadratlar: [1, 4, 9, 16, 25, 36, 49, 64]
```

---

# 797-Topshiriq: Work-stealing algoritmi nima va nima uchun muhim
## Topshiriq sharti:
Bo'sh qolgan oqimlar boshqa oqimlarning navbatidan vazifa o'g'irlashi (work stealing) mantiqini ko'rsating.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Work-Stealing arxitekturasi:");
    println!("1. Har bir oqim o'zining Deque (Double-ended queue) navbatiga ega.");
    println!("2. Oqim o'z navbatining old qismidan ish oladi (LIFO kesh uchun tez).");
    println!("3. Oqim bo'shab qolsa, boshqa band oqimning orqa qismidan ish oladi (FIFO).");
    println!("Bu algoritm barcha CPU yadrolarini 100% bir tekisda yuklashga xizmat qiladi.");
}
```
## Tushuntirish va Mantiq:
Work-stealing algoritmi biror oqim qiyinroq vazifa bilan band bo'lganda, bo'sh o'tirgan oqimlarning unga yordamga kelishini ta'minlaydi.
## Ishlash natijasi:
```text
Work-Stealing arxitekturasi:
1. Har bir oqim o'zining Deque (Double-ended queue) navbatiga ega.
2. Oqim o'z navbatining old qismidan ish oladi (LIFO kesh uchun tez).
3. Oqim bo'shab qolsa, boshqa band oqimning orqa qismidan ish oladi (FIFO).
Bu algoritm barcha CPU yadrolarini 100% bir tekisda yuklashga xizmat qiladi.
```

---

# 798-Topshiriq: std::thread::panicking() bilan oqim panic holatini aniqlash
## Topshiriq sharti:
Destruktor ichida oqim hozirda panic qilayotgan yoki normal tugayotganligini aniqlash.
## Yechim (Rust kodi):
```rust
use std::thread;

struct PanicKuzatuvchi;

impl Drop for PanicKuzatuvchi {
    fn drop(&mut self) {
        if thread::panicking() {
            println!("Drop: Oqim panic qilib to'xtamoqda, favqulodda tozalash!");
        } else {
            println!("Drop: Oqim normal yakunlandi.");
        }
    }
}

fn main() {
    let _ = thread::spawn(|| {
        let _k = PanicKuzatuvchi;
        panic!("Xatolik!");
    }).join();
}
```
## Tushuntirish va Mantiq:
`thread::panicking()` funksiyasi joriy oqim qulash (unwinding) holatida ekanligini bildiradi va tozalash ishlarini to'g'ri boshqarishga yordam beradi.
## Ishlash natijasi:
```text
Drop: Oqim panic qilib to'xtamoqda, favqulodda tozalash!
```

---

# 799-Topshiriq: Unbounded channel xotira xavfi vs Bounded channel barqarorligi
## Topshiriq sharti:
Cheksiz kanal bilan cheklangan kanal farqini tushuntiruvchi misol tuzing.
## Yechim (Rust kodi):
```rust
use std::sync::mpsc;

fn main() {
    // 1. Unbounded channel: xotira to'lguncha cheksiz xabar qabul qiladi (Memory Exhaustion xavfi)
    let (tx_unbounded, _rx1) = mpsc::channel();
    for i in 0..1000 {
        tx_unbounded.send(i).unwrap();
    }
    println!("Unbounded kanalga 1000 ta xabar to'siqsiz yozildi.");

    // 2. Bounded channel: faqat belgilangan sig'imga ruxsat beradi (Backpressure va barqarorlik)
    let (tx_bounded, _rx2) = mpsc::sync_channel(2);
    tx_bounded.send("X1").unwrap();
    tx_bounded.send("X2").unwrap();
    println!("Bounded kanal to'ldi, keyingi yuborish oqimni xavfsiz to'xtatib turadi.");
}
```
## Tushuntirish va Mantiq:
Haqiqiy ishlab chiqarish (production) tizimlarida xotira to'lib ketmasligi (OOM) uchun har doim chegaralangan (bounded) kanallar tavsiya etiladi.
## Ishlash natijasi:
```text
Unbounded kanalga 1000 ta xabar to'siqsiz yozildi.
Bounded kanal to'ldi, keyingi yuborish oqimni xavfsiz to'xtatib turadi.
```

---

# 800-Topshiriq: Multithreading integratsion loyihasi: Parallel log tahlilchisi va real vaqt agregatori
## Topshiriq sharti:
Bir nechta oqimlar orqali katta log ma'lumotlarini parallel o'qib, xatoliklar (ERROR) sonini hisoblovchi to'liq tizim yarating.
## Yechim (Rust kodi):
```rust
use std::sync::{Arc, Mutex};
use std::thread;

struct LogHisoboti {
    error_soni: usize,
    warn_soni: usize,
    info_soni: usize,
}

fn main() {
    let loglar = vec![
        "INFO: Tizim ishga tushdi",
        "WARN: Xotira 80% to'ldi",
        "ERROR: Ulanish uzildi",
        "INFO: Foydalanuvchi tizimga kirdi",
        "ERROR: Fayl topilmadi",
        "INFO: So'rov muvaffaqiyatli yakunlandi",
    ];

    let hisobot = Arc::new(Mutex::new(LogHisoboti { error_soni: 0, warn_soni: 0, info_soni: 0 }));

    let mut dastalar = vec![];
    let bolak_hajmi = loglar.len() / 2;

    for chunk in loglar.chunks(bolak_hajmi) {
        let chunk_vec: Vec<String> = chunk.iter().map(|s| s.to_string()).collect();
        let hisobot_ref = Arc::clone(&hisobot);

        dastalar.push(thread::spawn(move || {
            let mut e = 0;
            let mut w = 0;
            let mut inf = 0;

            for satr in chunk_vec {
                if satr.starts_with("ERROR") { e += 1; }
                else if satr.starts_with("WARN") { w += 1; }
                else if satr.starts_with("INFO") { inf += 1; }
            }

            let mut qulf = hisobot_ref.lock().unwrap();
            qulf.error_soni += e;
            qulf.warn_soni += w;
            qulf.info_soni += inf;
        }));
    }

    for d in dastalar {
        d.join().unwrap();
    }

    let yakuniy = hisobot.lock().unwrap();
    println!("=== YAKUNIY LOG TAHLILI ===");
    println!("INFO  xabarlar: {}", yakuniy.info_soni);
    println!("WARN  xabarlar: {}", yakuniy.warn_soni);
    println!("ERROR xabarlar: {}", yakuniy.error_soni);
}
```
## Tushuntirish va Mantiq:
`Arc<Mutex<T>>` va oqimlarni taqsimlash yordamida katta hajmdagi matnli ma'lumotlar parallel tahlil qilinadi va umumiy hisobot xavfsiz shakllantiriladi.
## Ishlash natijasi:
```text
=== YAKUNIY LOG TAHLILI ===
INFO  xabarlar: 3
WARN  xabarlar: 1
ERROR xabarlar: 2
```

---
