# Rust Dasturlash Tili: Asinxron Dasturlash va Tokio

Ushbu modulda Rust tilida asinxron dasturlashning nazariy va amaliy jihatlari: `std::future::Future`, `Poll`, `Context`, `Waker`, `Pin`, `Unpin`, holat mashinalari (State Machines), Tokio ekotizimi, tasklar, `join!`, `select!`, asinxron kanallar, tarmoq va I/O amallari to'liq qamrab olingan.

---

# 801-Topshiriq: std::future::Future trait strukturasi va ishlash printsipi
## Topshiriq sharti:
Rust standart kutubxonasidagi `std::future::Future` trait'ini tushuntiruvchi va qo'lda `Ready` qaytaruvchi Future yozing.
## Yechim (Rust kodi):
```rust
use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

struct TayyorFuture {
    qiymat: i32,
}

impl Future for TayyorFuture {
    type Output = i32;

    fn poll(self: Pin<&mut Self>, _cx: &mut Context<'_>) -> Poll<Self::Output> {
        println!("Future poll qilindi!");
        Poll::Ready(self.qiymat)
    }
}

fn main() {
    let mut fut = TayyorFuture { qiymat: 42 };
    // Standart kutubxonadagi Future poll metodini chaqirish uchun context kerak
    let waker = std::task::Waker::noop();
    let mut cx = Context::from_waker(&waker);
    let mut pinned = Pin::new(&mut fut);

    match pinned.as_mut().poll(&mut cx) {
        Poll::Ready(natija) => println!("Future tayyor natija berdi: {}", natija),
        Poll::Pending => println!("Future hali kutilmoqda"),
    }
}
```
## Tushuntirish va Mantiq:
Rust'da har qanday asinxron amal `Future` trait'ini amalga oshiradi. Uning `poll` metodi orqali holat `Poll::Ready` yoki `Poll::Pending` ekanligi aniqlanadi.
## Ishlash natijasi:
```text
Future poll qilindi!
Future tayyor natija berdi: 42
```

---

# 802-Topshiriq: Minimal qo'lbola Asinxron Executor yaratish
## Topshiriq sharti:
Future'larni `Poll::Ready` bo'lgunga qadar bloklab kutuvchi sodda `block_on` mexanizmini yozing.
## Yechim (Rust kodi):
```rust
use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll, Waker};

fn sodda_block_on<F: Future>(mut fut: F) -> F::Output {
    let waker = Waker::noop();
    let mut cx = Context::from_waker(&waker);
    let mut pinned = unsafe { Pin::new_unchecked(&mut fut) };

    loop {
        match pinned.as_mut().poll(&mut cx) {
            Poll::Ready(val) => return val,
            Poll::Pending => std::thread::yield_now(),
        }
    }
}

struct BirKechikishFuture {
    hisob: u32,
}

impl Future for BirKechikishFuture {
    type Output = &'static str;

    fn poll(mut self: Pin<&mut Self>, _cx: &mut Context<'_>) -> Poll<Self::Output> {
        if self.hisob == 0 {
            self.hisob += 1;
            println!("Hali tayyor emas: Pending");
            Poll::Pending
        } else {
            println!("Tayyor: Ready");
            Poll::Ready("Muvaffaqiyat!")
        }
    }
}

fn main() {
    let fut = BirKechikishFuture { hisob: 0 };
    let javob = sodda_block_on(fut);
    println!("Executor natijasi: {}", javob);
}
```
## Tushuntirish va Mantiq:
Asinxron executor Future ustida `poll` chaqiradi. Agar `Pending` bo'lsa kutadi, `Ready` bo'lsa yakuniy natijani qaytaradi.
## Ishlash natijasi:
```text
Hali tayyor emas: Pending
Tayyor: Ready
Executor natijasi: Muvaffaqiyat!
```

---

# 803-Topshiriq: State Machine transformatsiyasi: async fn ichki tuzilishi
## Topshiriq sharti:
Kompilyator `async fn` funksiyalarni qanday qilib enum holatlariga (state machine) aylantirishini ifodalovchi kod yozing.
## Yechim (Rust kodi):
```rust
enum AsinxronHolatMashinasi {
    Boshlangich,
    KutishBosqichi(u32),
    Tugallandi,
}

impl AsinxronHolatMashinasi {
    fn yangi() -> Self {
        AsinxronHolatMashinasi::Boshlangich
    }

    fn navbatdagi_qadam(&mut self) -> Option<&'static str> {
        match self {
            AsinxronHolatMashinasi::Boshlangich => {
                println!("1-bosqich: So'rov jo'natildi");
                *self = AsinxronHolatMashinasi::KutishBosqichi(1);
                None // Pending
            }
            AsinxronHolatMashinasi::KutishBosqichi(qadam) => {
                println!("2-bosqich: Javob qabul qilindi (qadam {})", qadam);
                *self = AsinxronHolatMashinasi::Tugallandi;
                Some("Asinxron vazifa yakunlandi!") // Ready
            }
            AsinxronHolatMashinasi::Tugallandi => None,
        }
    }
}

fn main() {
    let mut vazifa = AsinxronHolatMashinasi::yangi();
    while let None = vazifa.navbatdagi_qadam() {}
}
```
## Tushuntirish va Mantiq:
Rust'da `async/await` hech qanday yashirin allocation qilmaydi. U kodni kompakt enum holat mashinasiga aylantiradi, har bir `await` yangi holat hisoblanadi.
## Ishlash natijasi:
```text
1-bosqich: So'rov jo'natildi
2-bosqich: Javob qabul qilindi (qadam 1)
```

---

# 804-Topshiriq: Pin va Unpin nima uchun asinxron dasturlashda zarur
## Topshiriq sharti:
`Pin` smart pointeri Future ichidagi lokal havolalar xotirada ko'chib ketishining oldini olishini tushuntiring.
## Yechim (Rust kodi):
```rust
use std::pin::Pin;
use std::marker::PhantomPinned;

struct AsinxronKonteyner {
    ma_lumot: String,
    _pin: PhantomPinned, // Tipni !Unpin qiladi
}

fn main() {
    let obj = AsinxronKonteyner {
        ma_lumot: String::from("Ko'chmas xotira"),
        _pin: PhantomPinned,
    };

    // Heap'da qotirish (Box::pin)
    let pinned: Pin<Box<AsinxronKonteyner>> = Box::pin(obj);
    println!("Asinxron kontekstda xavfsiz qotirildi: {}", pinned.ma_lumot);
}
```
## Tushuntirish va Mantiq:
Future'lar o'zgaruvchilarga `await` orqali o'z-o'ziga havola (self-referential) saqlaydi. Agar xotirada joyi o'zgarsa, pointer buziladi. `Pin` buni taqiqlaydi.
## Ishlash natijasi:
```text
Asinxron kontekstda xavfsiz qotirildi: Ko'chmas xotira
```

---

# 805-Topshiriq: Waker mexanizmi: Qanday qilib CPU 100% yuklanishdan saqlanadi
## Topshiriq sharti:
Future tayyor bo'lmaganda executor doimiy aylanmasligi (busy loop) va `waker.wake()` chaqirilgandagina qayta uyg'onishini namoyish qiling.
## Yechim (Rust kodi):
```rust
use std::task::Waker;

struct IOMuvaffaqiyat {
    uygotuvchi: Option<Waker>,
}

impl IOMuvaffaqiyat {
    fn hodisa_keldi(&mut self) {
        println!("Tashqi tarmoq ma'lumoti keldi, Waker uyg'otiladi!");
        if let Some(w) = self.uygotuvchi.take() {
            w.wake();
        }
    }
}

fn main() {
    let mut io = IOMuvaffaqiyat { uygotuvchi: Some(Waker::noop()) };
    io.hodisa_keldi();
}
```
## Tushuntirish va Mantiq:
`Waker` operatsion tizim (epoll) yoki boshqa oqim hodisa tayyor bo'lganini executorgacha yetkazish vositasidir. Shunda CPU bo'sh vaqtda uxlaydi.
## Ishlash natijasi:
```text
Tashqi tarmoq ma'lumoti keldi, Waker uyg'otiladi!
```

---

# 806-Topshiriq: Tokio Runtime arxitekturasi: multi-thread vs current-thread
## Topshiriq sharti:
Tokio multi-thread (barcha CPU yadrolari) va current-thread (bitta oqimli yengil) rejimlarining farqini ko'rsating.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Tokio Runtime turlari:");
    println!("1. Multi-Thread Runtime: Har bir CPU yadrosiga bittadan ishchi oqim (Work-Stealing).");
    println!("2. Current-Thread Runtime: Bitta asosiy oqim ichida barcha asinxron vazifalar bajariladi.");
    println!("3. #[tokio::main] sukut bo'yicha Multi-thread rejimini yoqadi.");
}
```
## Tushuntirish va Mantiq:
Multi-thread yuqori yuklamali veb-serverlar uchun, Current-thread esa CLI utility yoki kam resursli muhitlar (IoT) uchun mos.
## Ishlash natijasi:
```text
Tokio Runtime turlari:
1. Multi-Thread Runtime: Har bir CPU yadrosiga bittadan ishchi oqim (Work-Stealing).
2. Current-Thread Runtime: Bitta asosiy oqim ichida barcha asinxron vazifalar bajariladi.
3. #[tokio::main] sukut bo'yicha Multi-thread rejimini yoqadi.
```

---

# 807-Topshiriq: Asinxron funksiyani sinxron bloklash: block_on simulyatsiyasi
## Topshiriq sharti:
Sinxron kod ichidan asinxron funksiyani chaqirish va natijani kutish.
## Yechim (Rust kodi):
```rust
async fn asinxron_hisob(a: i32, b: i32) -> i32 {
    a + b
}

fn main() {
    // Rust 1.70+ da oddiy async blokni poll qilish
    let natija = {
        let waker = std::task::Waker::noop();
        let mut cx = std::task::Context::from_waker(&waker);
        let mut fut = std::pin::pin!(asinxron_hisob(15, 25));
        match fut.as_mut().poll(&mut cx) {
            std::task::Poll::Ready(res) => res,
            std::task::Poll::Pending => 0,
        }
    };

    println!("Asinxron hisob natijasi: {}", natija);
}
```
## Tushuntirish va Mantiq:
Kompilyatsiya vaqtida `async fn` avtomatik ravishda `impl Future<Output = T>` qaytaruvchi funksiyaga aylanadi.
## Ishlash natijasi:
```text
Asinxron hisob natijasi: 40
```

---

# 808-Topshiriq: tokio::spawn bilan yengil vazifalarni (Tasks) ishga tushirish
## Topshiriq sharti:
Bir nechta Tokio asinxron tasklarini ishga tushirish sintaksisini yozing.
## Yechim (Rust kodi):
```rust
// Tokio task spawn namunasi
fn main() {
    println!("tokio::spawn quyidagi tarzda yoziladi:");
    println!(r#"
#[tokio::main]
async fn main() {{
    let handle = tokio::spawn(async {{
        println!("Asinxron task fonida bajarildi");
        100
    }});

    let natija = handle.await.unwrap();
    println!("Natija: {{}}", natija);
}}
"#);
}
```
## Tushuntirish va Mantiq:
`tokio::spawn` operatsion tizim oqimiga qaraganda ancha yengil (bir necha yuz bayt) bo'lib, millionlab tasklarni bir vaqtda ochish imkonini beradi.
## Ishlash natijasi:
```text
tokio::spawn quyidagi tarzda yoziladi:

#[tokio::main]
async fn main() {
    let handle = tokio::spawn(async {
        println!("Asinxron task fonida bajarildi");
        100
    });

    let natija = handle.await.unwrap();
    println!("Natija: {}", natija);
}
```

---

# 809-Topshiriq: tokio::time::sleep bilan non-blocking kutish
## Topshiriq sharti:
`std::thread::sleep` (butun oqimni to'xtatadi) vs `tokio::time::sleep` (faqat joriy vazifani to'xtatadi) taqqoslash.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Sleep mexanizmlari taqqoslashi:");
    println!("- std::thread::sleep: OS oqimini to'liq bloklaydi, boshqa tasklar ham to'xtab qoladi.");
    println!("- tokio::time::sleep: Oqimni bo'shatadi, ishchi oqim boshqa minglab tasklarni bajarishda davom etadi.");
}
```
## Tushuntirish va Mantiq:
Asinxron dasturlarda hech qachon `thread::sleep` ishlatilmasligi kerak, chunki bu butun runtime unumdorligini falaj qiladi.
## Ishlash natijasi:
```text
Sleep mexanizmlari taqqoslashi:
- std::thread::sleep: OS oqimini to'liq bloklaydi, boshqa tasklar ham to'xtab qoladi.
- tokio::time::sleep: Oqimni bo'shatadi, ishchi oqim boshqa minglab tasklarni bajarishda davom etadi.
```

---

# 810-Topshiriq: tokio::join! makrosi bilan parallel bir vaqtda kutish
## Topshiriq sharti:
Bir nechta mustaqil asinxron amallarni `join!` orqali parallel kutish sintaksisini ko'rsating.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("tokio::join! sintaksisi:");
    println!(r#"
async fn vazifa_1() -> i32 {{ 10 }}
async fn vazifa_2() -> &'static str {{ "Salom" }}

#[tokio::main]
async fn main() {{
    let (a, b) = tokio::join!(vazifa_1(), vazifa_2());
    println!("Natijalar: {{}} va {{}}", a, b);
}}
"#);
}
```
## Tushuntirish va Mantiq:
`tokio::join!` barcha berilgan Future'larni parallel yurgizadi va ularning barchasi tugagach natijalarni kortej (tuple) sifatida qaytaradi.
## Ishlash natijasi:
```text
tokio::join! sintaksisi:

async fn vazifa_1() -> i32 { 10 }
async fn vazifa_2() -> &'static str { "Salom" }

#[tokio::main]
async fn main() {
    let (a, b) = tokio::join!(vazifa_1(), vazifa_2());
    println!("Natijalar: {} va {}", a, b);
}
```

---

# 811-Topshiriq: tokio::select! bilan tezkor birinchi kelganni tanlash (Racing)
## Topshiriq sharti:
Ikki amaldan qaysi biri birinchi tugasa shuning natijasini olish va qolganini bekor qilish.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("tokio::select! poyga mantiqi:");
    println!(r#"
#[tokio::main]
async fn main() {{
    tokio::select! {{
        res = asinxron_qidiruv_server1() => {{
            println!("1-server tezroq javob berdi: {:?}", res);
        }}
        res = asinxron_qidiruv_server2() => {{
            println!("2-server tezroq javob berdi: {:?}", res);
        }}
        _ = tokio::time::sleep(tokio::time::Duration::from_secs(2)) => {{
            println!("Vaqt tugadi (Timeout)!");
        }}
    }}
}}
"#);
}
```
## Tushuntirish va Mantiq:
`select!` makrosi birinchi tayyor bo'lgan `Future`ning kod blokini bajaradi va boshqa kutilayotgan Future'larni bekor qilib xotiradan tozalaydi.
## Ishlash natijasi:
```text
tokio::select! poyga mantiqi:

#[tokio::main]
async fn main() {
    tokio::select! {
        res = asinxron_qidiruv_server1() => {
            println!("1-server tezroq javob berdi: {:?}", res);
        }
        res = asinxron_qidiruv_server2() => {
            println!("2-server tezroq javob berdi: {:?}", res);
        }
        _ = tokio::time::sleep(tokio::time::Duration::from_secs(2)) => {
            println!("Vaqt tugadi (Timeout)!");
        }
    }
}
```

---

# 812-Topshiriq: tokio::time::timeout orqali vaqt chegarasini o'rnatish
## Topshiriq sharti:
Asinxron operatsiya belgilangan muddatdan oshib ketganda `Elapsed` xatosini berish tartibi.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("tokio::time::timeout qo'llanishi:");
    println!(r#"
use tokio::time::{timeout, Duration};

async fn sekin_amal() -> &'static str {
    tokio::time::sleep(Duration::from_secs(5)).await;
    "Tayyor"
}

#[tokio::main]
async fn main() {
    match timeout(Duration::from_secs(1), sekin_amal()).await {
        Ok(natija) => println!("O'z vaqtida bajarildi: {}", natija),
        Err(_) => println!("XATO: So'rov muddati tugadi (Timeout)!"),
    }
}
"#);
}
```
## Tushuntirish va Mantiq:
`timeout` amali asinxron tizimlarda cheksiz kutilishlarning oldini oladi va barqarorlikni ta'minlaydi.
## Ishlash natijasi:
```text
tokio::time::timeout qo'llanishi:

use tokio::time::{timeout, Duration};

async fn sekin_amal() -> &'static str {
    tokio::time::sleep(Duration::from_secs(5)).await;
    "Tayyor"
}

#[tokio::main]
async fn main() {
    match timeout(Duration::from_secs(1), sekin_amal()).await {
        Ok(natija) => println!("O'z vaqtida bajarildi: {}", natija),
        Err(_) => println!("XATO: So'rov muddati tugadi (Timeout)!"),
    }
}
```

---

# 813-Topshiriq: tokio::sync::mpsc asinxron kanallari
## Topshiriq sharti:
Asinxron oqimlar o'rtasida xabarlarni `send().await` va `recv().await` orqali uzatish.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("tokio::sync::mpsc namunasi:");
    println!(r#"
use tokio::sync::mpsc;

#[tokio::main]
async fn main() {
    let (tx, mut rx) = mpsc::channel(32);

    tokio::spawn(async move {
        tx.send("Asinxron xabar").await.unwrap();
    });

    if let Some(xabar) = rx.recv().await {
        println!("Qabul qilindi: {}", xabar);
    }
}
"#);
}
```
## Tushuntirish va Mantiq:
`tokio::sync::mpsc` kanallari to'liq asinxron bo'lib, oqimni emas, faqat joriy taskni to'xtatadi.
## Ishlash natijasi:
```text
tokio::sync::mpsc namunasi:

use tokio::sync::mpsc;

#[tokio::main]
async fn main() {
    let (tx, mut rx) = mpsc::channel(32);

    tokio::spawn(async move {
        tx.send("Asinxron xabar").await.unwrap();
    });

    if let Some(xabar) = rx.recv().await {
        println!("Qabul qilindi: {}", xabar);
    }
}
```

---

# 814-Topshiriq: tokio::sync::oneshot kanali: bitta natijani qaytarish
## Topshiriq sharti:
Bitta asinxron natijani yetkazib berish uchun `oneshot` kanalidan foydalanish.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("tokio::sync::oneshot misoli:");
    println!(r#"
use tokio::sync::oneshot;

#[tokio::main]
async fn main() {
    let (tx, rx) = oneshot::channel();

    tokio::spawn(async move {
        let natija = 42 * 2;
        tx.send(natija).unwrap();
    });

    let qabul = rx.await.unwrap();
    println!("Oneshot natija: {}", qabul);
}
"#);
}
```
## Tushuntirish va Mantiq:
`oneshot` kanali faqat 1 ta qiymat uzatishga mo'ljallangan bo'lib, juda kam xotira sarflaydi va tez ishlaydi.
## Ishlash natijasi:
```text
tokio::sync::oneshot misoli:

use tokio::sync::oneshot;

#[tokio::main]
async fn main() {
    let (tx, rx) = oneshot::channel();

    tokio::spawn(async move {
        let natija = 42 * 2;
        tx.send(natija).unwrap();
    });

    let qabul = rx.await.unwrap();
    println!("Oneshot natija: {}", qabul);
}
```

---

# 815-Topshiriq: tokio::sync::broadcast kanali: Pub/Sub modeli
## Topshiriq sharti:
Bitta manbadan bir nechta qabul qiluvchilarga (Fan-out) xabar tarqatuvchi broadcast kanali.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("tokio::sync::broadcast namunasi:");
    println!(r#"
use tokio::sync::broadcast;

#[tokio::main]
async fn main() {
    let (tx, _rx) = broadcast::channel(16);

    let mut rx1 = tx.subscribe();
    let mut rx2 = tx.subscribe();

    tx.send("Barchaga e'lon!").unwrap();

    println!("Abonent 1: {}", rx1.recv().await.unwrap());
    println!("Abonent 2: {}", rx2.recv().await.unwrap());
}
"#);
}
```
## Tushuntirish va Mantiq:
`broadcast` kanali chat xonalari va WebSocket ulanishlarida barcha foydalanuvchilarga xabarlarni tarqatish uchun idealdir.
## Ishlash natijasi:
```text
tokio::sync::broadcast namunasi:

use tokio::sync::broadcast;

#[tokio::main]
async fn main() {
    let (tx, _rx) = broadcast::channel(16);

    let mut rx1 = tx.subscribe();
    let mut rx2 = tx.subscribe();

    tx.send("Barchaga e'lon!").unwrap();

    println!("Abonent 1: {}", rx1.recv().await.unwrap());
    println!("Abonent 2: {}", rx2.recv().await.unwrap());
}
```

---

# 816-Topshiriq: tokio::sync::watch kanali: eng so'nggi holatni uzatish
## Topshiriq sharti:
Kanalda oraliq xabarlarni to'plamasdan faqat eng oxirgi qiymatni kuzatish tartibi.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("tokio::sync::watch xususiyati:");
    println!("- Faqat eng so'nggi holatni saqlaydi.");
    println!("- Yangi konfiguratsiyalar yoki server holatini boshqa tasklarga bildirish uchun qulay.");
}
```
## Tushuntirish va Mantiq:
`watch` kanali konfiguratsiya o'zgarishlarini (Hot-reload) kuzatuvchi tasklar uchun ishlatiladi.
## Ishlash natijasi:
```text
tokio::sync::watch xususiyati:
- Faqat eng so'nggi holatni saqlaydi.
- Yangi konfiguratsiyalar yoki server holatini boshqa tasklarga bildirish uchun qulay.
```

---

# 817-Topshiriq: tokio::sync::Mutex vs std::sync::Mutex
## Topshiriq sharti:
Qachon asinxron `tokio::sync::Mutex`, qachon esa sinxron `std::sync::Mutex` ishlatilishi kerakligini tushuntiring.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Mutex tanlash qoidalari:");
    println!("1. std::sync::Mutex: Agar qulf faqat qisqa operatsiyalar uchun olinsa va `.await` chaqirilmasa (Tezroq).");
    println!("2. tokio::sync::Mutex: Agar qulf olingan holatda `.await` nuqtasidan o'tish zarur bo'lsa (Deadlock oldini oladi).");
}
```
## Tushuntirish va Mantiq:
`std::sync::MutexGuard` `!Send` bo'lishi mumkin va `.await` orqali saqlansa Tokio xato beradi. Shuning uchun `.await` bilan birga `tokio::sync::Mutex` shart.
## Ishlash natijasi:
```text
Mutex tanlash qoidalari:
1. std::sync::Mutex: Agar qulf faqat qisqa operatsiyalar uchun olinsa va `.await` chaqirilmasa (Tezroq).
2. tokio::sync::Mutex: Agar qulf olingan holatda `.await` nuqtasidan o'tish zarur bo'lsa (Deadlock oldini oladi).
```

---

# 818-Topshiriq: spawn_blocking: CPU-intensiv va sinxron bloklovchi ishlarni xavfsiz bajarish
## Topshiriq sharti:
Kriptografik hisob yoki og'ir fayl amallarini `tokio::task::spawn_blocking` orqali alohida oqimga surish.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("spawn_blocking sintaksisi:");
    println!(r#"
#[tokio::main]
async fn main() {
    let natija = tokio::task::spawn_blocking(|| {
        // Og'ir CPU hisob-kitobi yoki sinxron fayl o'qish
        (1..=10_000_000).fold(0u64, |a, b| a + b)
    }).await.unwrap();

    println!("Og'ir hisob natijasi: {}", natija);
}
"#);
}
```
## Tushuntirish va Mantiq:
`spawn_blocking` asinxron executor oqimlarini bloklamaslik uchun maxsus ajratilgan sinxron oqimlar hovuzidan foydalanadi.
## Ishlash natijasi:
```text
spawn_blocking sintaksisi:

#[tokio::main]
async fn main() {
    let natija = tokio::task::spawn_blocking(|| {
        // Og'ir CPU hisob-kitobi yoki sinxron fayl o'qish
        (1..=10_000_000).fold(0u64, |a, b| a + b)
    }).await.unwrap();

    println!("Og'ir hisob natijasi: {}", natija);
}
```

---

# 819-Topshiriq: Asinxron TCP Echo Server arxitekturasi
## Topshiriq sharti:
`tokio::net::TcpListener` yordamida har bir mijozni alohida `tokio::spawn` bilan qabul qiluvchi Echo Server kodini yozing.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Asinxron TCP Echo Server strukturasi:");
    println!(r#"
use tokio::net::TcpListener;
use tokio::io::{AsyncReadExt, AsyncWriteExt};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let listener = TcpListener::bind("127.0.0.1:8080").await?;
    println!("Server 8080-portda tinglamoqda...");

    loop {
        let (mut socket, manzil) = listener.accept().await?;
        println!("Yangi ulanish: {}", manzil);

        tokio::spawn(async move {
            let mut bufer = [0u8; 1024];
            loop {
                let n = match socket.read(&mut bufer).await {
                    Ok(0) => return, // Ulanish yopildi
                    Ok(n) => n,
                    Err(_) => return,
                };
                if socket.write_all(&bufer[..n]).await.is_err() {
                    return;
                }
            }
        });
    }
}
"#);
}
```
## Tushuntirish va Mantiq:
`TcpListener::accept().await` non-blocking rejimda kutadi va yangi ulanish kelishi bilan uni yengil tokio taskiga uzatadi.
## Ishlash natijasi:
```text
Asinxron TCP Echo Server strukturasi:

use tokio::net::TcpListener;
use tokio::io::{AsyncReadExt, AsyncWriteExt};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let listener = TcpListener::bind("127.0.0.1:8080").await?;
    println!("Server 8080-portda tinglamoqda...");

    loop {
        let (mut socket, manzil) = listener.accept().await?;
        println!("Yangi ulanish: {}", manzil);

        tokio::spawn(async move {
            let mut bufer = [0u8; 1024];
            loop {
                let n = match socket.read(&mut bufer).await {
                    Ok(0) => return, // Ulanish yopildi
                    Ok(n) => n,
                    Err(_) => return,
                };
                if socket.write_all(&bufer[..n]).await.is_err() {
                    return;
                }
            }
        });
    }
}
```

---

# 820-Topshiriq: Asinxron TCP Client arxitekturasi
## Topshiriq sharti:
`tokio::net::TcpStream` yordamida serverga ulanish, xabar yozish va javobni o'qish.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Asinxron TCP Client:");
    println!(r#"
use tokio::net::TcpStream;
use tokio::io::{AsyncReadExt, AsyncWriteExt};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut stream = TcpStream::connect("127.0.0.1:8080").await?;
    stream.write_all(b"Salom Server!\n").await?;

    let mut bufer = [0u8; 128];
    let n = stream.read(&mut bufer).await?;
    println!("Serverdan javob: {}", String::from_utf8_lossy(&bufer[..n]));
    Ok(())
}
"#);
}
```
## Tushuntirish va Mantiq:
Asinxron mijozlar server javobini kutish jarayonida operatsion tizim oqimini band qilmaydi.
## Ishlash natijasi:
```text
Asinxron TCP Client:

use tokio::net::TcpStream;
use tokio::io::{AsyncReadExt, AsyncWriteExt};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut stream = TcpStream::connect("127.0.0.1:8080").await?;
    stream.write_all(b"Salom Server!\n").await?;

    let mut bufer = [0u8; 128];
    let n = stream.read(&mut bufer).await?;
    println!("Serverdan javob: {}", String::from_utf8_lossy(&bufer[..n]));
    Ok(())
}
```

---

# 821-Topshiriq: AsyncRead va AsyncWrite trait'lari
## Topshiriq sharti:
`AsyncReadExt` va `AsyncWriteExt` orqali taqdim etiladigan asosiy metodlar ro'yxati.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Asosiy Async I/O metodlari:");
    println!("- read(&mut buf): Baytlarni buferga o'qish");
    println!("- read_exact(&mut buf): Belgilangan aniq bayt hajmigacha to'liq o'qish");
    println!("- read_to_end(&mut vec): Oqim yopilguncha barcha baytlarni yig'ish");
    println!("- write_all(&buf): Barcha baytlar to'liq yozilishini kafolatlash");
    println!("- flush(): Buferlangan ma'lumotlarni tarmoqqa majburiy jo'natish");
}
```
## Tushuntirish va Mantiq:
Ushbu metodlar sinxron `std::io::Read` va `Write` ning asinxron muqobili bo'lib, har bir amal `.await` qilinadi.
## Ishlash natijasi:
```text
Asosiy Async I/O metodlari:
- read(&mut buf): Baytlarni buferga o'qish
- read_exact(&mut buf): Belgilangan aniq bayt hajmigacha to'liq o'qish
- read_to_end(&mut vec): Oqim yopilguncha barcha baytlarni yig'ish
- write_all(&buf): Barcha baytlar to'liq yozilishini kafolatlash
- flush(): Buferlangan ma'lumotlarni tarmoqqa majburiy jo'natish
```

---

# 822-Topshiriq: Asinxron fayllar bilan ishlash: tokio::fs
## Topshiriq sharti:
`tokio::fs::File` va `tokio::fs::read_to_string` yordamida diskdagi fayllarni asinxron o'qish.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("tokio::fs fayl amallari:");
    println!(r#"
use tokio::fs;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    fs::write("test.txt", "Asinxron Rust ma'lumotlari").await?;
    let matn = fs::read_to_string("test.txt").await?;
    println!("O'qildi: {}", matn);
    fs::remove_file("test.txt").await?;
    Ok(())
}
"#);
}
```
## Tushuntirish va Mantiq:
Operatsion tizim darajasida fayl operatsiyalari odatda bloklovchi bo'lgani sababli, `tokio::fs` ichki bloklovchi hovuzdan foydalanib asinxron interfeys beradi.
## Ishlash natijasi:
```text
tokio::fs fayl amallari:

use tokio::fs;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    fs::write("test.txt", "Asinxron Rust ma'lumotlari").await?;
    let matn = fs::read_to_string("test.txt").await?;
    println!("O'qildi: {}", matn);
    fs::remove_file("test.txt").await?;
    Ok(())
}
```

---

# 823-Topshiriq: Tokio Semaphore: Bir vaqtda maksimal N ta so'rovga ruxsat
## Topshiriq sharti:
`tokio::sync::Semaphore` bilan bir vaqtda bajariluvchi yuklamani (masalan, API so'rovlarini) cheklash.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("tokio::sync::Semaphore namunasi:");
    println!(r#"
use tokio::sync::Semaphore;
use std::sync::Arc;

#[tokio::main]
async fn main() {
    let semafor = Arc::new(Semaphore::new(3)); // Maksimal 3 ta parallel so'rov

    for i in 1..=10 {
        let sem = Arc::clone(&semafor);
        tokio::spawn(async move {
            let _ruxsat = sem.acquire().await.unwrap();
            println!("Vazifa {} ruxsat oldi va ishlamoqda...", i);
            tokio::time::sleep(tokio::time::Duration::from_millis(100)).await;
        });
    }
}
"#);
}
```
## Tushuntirish va Mantiq:
`Semaphore` tashqi xizmatlar yoki ma'lumotlar bazasiga bir vaqtda tushadigan ortiqcha so'rovlar yuklamasini (rate limit) to'xtatib turadi.
## Ishlash natijasi:
```text
tokio::sync::Semaphore namunasi:

use tokio::sync::Semaphore;
use std::sync::Arc;

#[tokio::main]
async fn main() {
    let semafor = Arc::new(Semaphore::new(3)); // Maksimal 3 ta parallel so'rov

    for i in 1..=10 {
        let sem = Arc::clone(&semafor);
        tokio::spawn(async move {
            let _ruxsat = sem.acquire().await.unwrap();
            println!("Vazifa {} ruxsat oldi va ishlamoqda...", i);
            tokio::time::sleep(tokio::time::Duration::from_millis(100)).await;
        });
    }
}
```

---

# 824-Topshiriq: CancellationToken bilan butun tizimni to'xtatish
## Topshiriq sharti:
`tokio_util::sync::CancellationToken` yordamida barcha ochiq tasklarga to'xtash signali yuborish.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("CancellationToken vazifasi:");
    println!("1. Bitta markaziy token yaratiladi.");
    println!("2. Barcha tasklarga uning bolalari tarqatiladi.");
    println!("3. `token.cancel()` chaqirilishi bilan barcha tasklar `cancelled().await` orqali to'xtaydi.");
}
```
## Tushuntirish va Mantiq:
Graceful shutdown vaqtida barcha fon xizmatlarini xavfsiz va bir vaqtda yopish uchun CancellationToken eng yaxshi yechimdir.
## Ishlash natijasi:
```text
CancellationToken vazifasi:
1. Bitta markaziy token yaratiladi.
2. Barcha tasklarga uning bolalari tarqatiladi.
3. `token.cancel()` chaqirilishi bilan barcha tasklar `cancelled().await` orqali to'xtaydi.
```

---

# 825-Topshiriq: Asinxron Retry pattern (qayta urinish)
## Topshiriq sharti:
Xatolik yuz berganda eksponentsial kechikish bilan qayta urinuvchi asinxron funksiya andozasi.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Asinxron qayta urinish (Retry) algoritmi:");
    println!(r#"
async fn qayta_urinish<F, Fut, T, E>(mut f: F, urinishlar_soni: usize) -> Result<T, E>
where
    F: FnMut() -> Fut,
    Fut: std::future::Future<Output = Result<T, E>>,
{
    let mut kechikish = 100; // millisekund
    for _ in 0..urinishlar_soni {
        match f().await {
            Ok(v) => return Ok(v),
            Err(_) => {
                tokio::time::sleep(tokio::time::Duration::from_millis(kechikish)).await;
                kechikish *= 2; // Eksponentsial oshirish
            }
        }
    }
    f().await
}
"#);
}
```
## Tushuntirish va Mantiq:
Tarmoqdagi vaqtinchalik nosozliklar (transient errors) paytida qayta urinish tizimning chidamliligini oshiradi.
## Ishlash natijasi:
```text
Asinxron qayta urinish (Retry) algoritmi:

async fn qayta_urinish<F, Fut, T, E>(mut f: F, urinishlar_soni: usize) -> Result<T, E>
where
    F: FnMut() -> Fut,
    Fut: std::future::Future<Output = Result<T, E>>,
{
    let mut kechikish = 100; // millisekund
    for _ in 0..urinishlar_soni {
        match f().await {
            Ok(v) => return Ok(v),
            Err(_) => {
                tokio::time::sleep(tokio::time::Duration::from_millis(kechikish)).await;
                kechikish *= 2; // Eksponentsial oshirish
            }
        }
    }
    f().await
}
```

---

# 826-Topshiriq: Asinxron Stream tushunchasi (Async Iterator)
## Topshiriq sharti:
`futures::Stream` yoki `tokio_stream::Stream` interfeysi: `poll_next` metodi qanday ishlashi.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Stream (Asinxron Iterator):");
    println!("Oddiy Iterator: next(&mut self) -> Option<Item>");
    println!("Stream:        poll_next(Pin<&mut Self>, &mut Context) -> Poll<Option<Item>>");
    println!("Stream ma'lumotlar oqimini vaqt o'tishi bilan ketma-ket qabul qilish uchun xizmat qiladi.");
}
```
## Tushuntirish va Mantiq:
Stream'lar WebSocket oqimlari, fayldan qatorma-qator asinxron o'qish yoki server sent events (SSE) uchun ishlatiladi.
## Ishlash natijasi:
```text
Stream (Asinxron Iterator):
Oddiy Iterator: next(&mut self) -> Option<Item>
Stream:        poll_next(Pin<&mut Self>, &mut Context) -> Poll<Option<Item>>
Stream ma'lumotlar oqimini vaqt o'tishi bilan ketma-ket qabul qilish uchun xizmat qiladi.
```

---

# 827-Topshiriq: Asinxron Heartbeat va Ping-Pong monitoringi
## Topshiriq sharti:
Har 5 soniyada serverga sog'lomlik xabari (Heartbeat) yuboruvchi asinxron fon vazifasi.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Heartbeat task:");
    println!(r#"
#[tokio::main]
async fn main() {
    let mut interval = tokio::time::interval(tokio::time::Duration::from_secs(5));

    tokio::spawn(async move {
        loop {
            interval.tick().await;
            println!("[HEARTBEAT]: Tizim sog'lom va faol...");
        }
    });
}
"#);
}
```
## Tushuntirish va Mantiq:
`tokio::time::interval` oraliq vaqtni o'z ichiga olgan holda aniq qadam bilan takrorlanuvchi amallarni boshqaradi.
## Ishlash natijasi:
```text
Heartbeat task:

#[tokio::main]
async fn main() {
    let mut interval = tokio::time::interval(tokio::time::Duration::from_secs(5));

    tokio::spawn(async move {
        loop {
            interval.tick().await;
            println!("[HEARTBEAT]: Tizim sog'lom va faol...");
        }
    });
}
```

---

# 828-Topshiriq: Async Trait muammosi va Rust 1.75+ yangilanishi
## Topshiriq sharti:
Nima uchun avval trait ichida `async fn` yozib bo'lmas edi va Rust 1.75+ da bu qanday yechildi?
## Yechim (Rust kodi):
```rust
// Rust 1.75+ versiyasidan boshlab trait ichida to'g'ridan-to'g'ri async fn yozish mumkin:
trait MalumotOmbori {
    async fn saqla(&self, kalit: &str, qiymat: &str) -> bool;
}

struct XotiraOmbori;

impl MalumotOmbori for XotiraOmbori {
    async fn saqla(&self, _kalit: &str, _qiymat: &str) -> bool {
        true
    }
}

fn main() {
    println!("Rust 1.75+ dan boshlab yerlik 'async fn in traits' (AFIT) to'liq qo'llab-quvvatlanadi!");
}
```
## Tushuntirish va Mantiq:
Rust 1.75 ga qadar `#[async_trait]` makrosi orqali `Box<dyn Future>` ajratilar edi. Endi esa nol xarajatli RPITIT (Return Position Impl Trait in Trait) orqali ishlaydi.
## Ishlash natijasi:
```text
Rust 1.75+ dan boshlab yerlik 'async fn in traits' (AFIT) to'liq qo'llab-quvvatlanadi!
```

---

# 829-Topshiriq: Asinxron Resurs Hovuzi (Connection Pool) arxitekturasi
## Topshiriq sharti:
Cheklangan ulanishlarni oqimlar o'rtasida qayta taqsimlovchi havza tuzilmasi.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Asinxron Ulanishlar Hovuzi (Connection Pool):");
    println!("1. Navbatda bir nechta faol ulanishlar saqlanadi.");
    println!("2. So'rov kelganda pool.get().await orqali ulanish olinadi.");
    println!("3. Ish tugagach, ulanish avtomatik ravishda hovuzga qaytariladi.");
}
```
## Tushuntirish va Mantiq:
Har bir so'rov uchun yangi TCP yoki DB ulanishi ochish o'rniga Connection Pool qo'llash kechikishni (latency) 10-50 baravar kamaytiradi.
## Ishlash natijasi:
```text
Asinxron Ulanishlar Hovuzi (Connection Pool):
1. Navbatda bir nechta faol ulanishlar saqlanadi.
2. So'rov kelganda pool.get().await orqali ulanish olinadi.
3. Ish tugagach, ulanish avtomatik ravishda hovuzga qaytariladi.
```

---

# 830-Topshiriq: Graceful Shutdown: CTRL+C signalini asinxron kutish
## Topshiriq sharti:
`tokio::signal::ctrl_c().await` yordamida dasturni to'xtatish buyrug'ini qabul qilish.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Graceful Shutdown namunasi:");
    println!(r#"
#[tokio::main]
async fn main() {
    println!("Server ishlamoqda. To'xtatish uchun Ctrl+C bosing...");
    tokio::signal::ctrl_c().await.expect("Signalni tinglashda xatolik");
    println!("Ctrl+C bosildi! Barcha resurslar xavfsiz saqlanib yopilmoqda...");
}
"#);
}
```
## Tushuntirish va Mantiq:
Graceful shutdown server ma'lumotlar bazasiga tranzaksiyalarni to'liq yozib tugatishiga va faol so'rovlarga javob berishiga imkon yaratadi.
## Ishlash natijasi:
```text
Graceful Shutdown namunasi:

#[tokio::main]
async fn main() {
    println!("Server ishlamoqda. To'xtatish uchun Ctrl+C bosing...");
    tokio::signal::ctrl_c().await.expect("Signalni tinglashda xatolik");
    println!("Ctrl+C bosildi! Barcha resurslar xavfsiz saqlanib yopilmoqda...");
}
```

---

# 831-Topshiriq: Async Fan-out va Fan-in modeli
## Topshiriq sharti:
Bitta topshiriqni bir vaqtda 5 ta taskka bo'lib (Fan-out), natijalarni bitta joyga yig'ish (Fan-in).
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Fan-out / Fan-in arxitekturasi:");
    println!("Fan-out: Bitta katta vazifani o'nlab parallel sub-tasklarga tarqatish.");
    println!("Fan-in: Barcha sub-tasklar natijalarini tokio::sync::mpsc kanali orqali bitta agregatorga yig'ish.");
}
```
## Tushuntirish va Mantiq:
Ushbu model asinxron qidiruv tizimlari, scraperlar va taqsimlangan tahlil modullari uchun asos hisoblanadi.
## Ishlash natijasi:
```text
Fan-out / Fan-in arxitekturasi:
Fan-out: Bitta katta vazifani o'nlab parallel sub-tasklarga tarqatish.
Fan-in: Barcha sub-tasklar natijalarini tokio::sync::mpsc kanali orqali bitta agregatorga yig'ish.
```

---

# 832-Topshiriq: tokio::task::JoinSet bilan dinamik tasklar guruhini boshqarish
## Topshiriq sharti:
Dinamik miqdordagi tasklarni `JoinSet`ga qo'shish va ularni tayyor bo'lish navbati bilan olish.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("tokio::task::JoinSet:");
    println!(r#"
use tokio::task::JoinSet;

#[tokio::main]
async fn main() {
    let mut toplam = JoinSet::new();

    for i in 1..=5 {
        toplam.spawn(async move {
            i * 2
        });
    }

    while let Some(res) = toplam.join_next().await {
        println!("Task tugadi: {}", res.unwrap());
    }
}
"#);
}
```
## Tushuntirish va Mantiq:
`JoinSet` tasklar qaysi tartibda tugashiga qarab natijalarni birin-ketin qaytaradi va barchasi tugaganda xotirani avtomatik tozalaydi.
## Ishlash natijasi:
```text
tokio::task::JoinSet:

use tokio::task::JoinSet;

#[tokio::main]
async fn main() {
    let mut toplam = JoinSet::new();

    for i in 1..=5 {
        toplam.spawn(async move {
            i * 2
        });
    }

    while let Some(res) = toplam.join_next().await {
        println!("Task tugadi: {}", res.unwrap());
    }
}
```

---

# 833-Topshiriq: Asinxron Kesh (Async TTL Cache) tushunchasi
## Topshiriq sharti:
Ma'lumotlarni belgilangan vaqt davomida asinxron keshda saqlash va muddati o'tgach qayta yangilash.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Asinxron TTL Kesh:");
    println!("1. Har bir kesh yozuviga `Instant` vaqti biriktiriladi.");
    println!("2. O'qish paytida vaqt tekshiriladi: agar muddat o'tgan bo'lsa, asinxron yangilanadi.");
}
```
## Tushuntirish va Mantiq:
Asinxron TTL kesh ma'lumotlar bazasiga qayta-qayta bir xil og'ir so'rovlar yuborilishining oldini oladi.
## Ishlash natijasi:
```text
Asinxron TTL Kesh:
1. Har bir kesh yozuviga `Instant` vaqti biriktiriladi.
2. O'qish paytida vaqt tekshiriladi: agar muddat o'tgan bo'lsa, asinxron yangilanadi.
```

---

# 834-Topshiriq: tokio::io::split bilan soketni o'qish va yozish qismlariga ajratish
## Topshiriq sharti:
Bitta TCP soketni bir vaqtning o'zida ham o'qish ham yozish uchun ikkita mustaqil oqimga ajratish.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("tokio::io::split:");
    println!(r#"
use tokio::io::{self, AsyncReadExt, AsyncWriteExt};
use tokio::net::TcpStream;

#[tokio::main]
async fn main() -> io::Result<()> {
    let socket = TcpStream::connect("127.0.0.1:8080").await?;
    let (mut oquvchi, mut yozuvchi) = io::split(socket);

    tokio::spawn(async move {
        yozuvchi.write_all(b"Salom!").await.unwrap();
    });

    let mut buf = [0u8; 10];
    oquvchi.read(&mut buf).await?;
    Ok(())
}
"#);
}
```
## Tushuntirish va Mantiq:
`split` yordamida bitta soketning o'qish qismi bitta taskda, yozish qismi boshqa taskda bir-biriga xalal bermasdan mustaqil ishlay oladi.
## Ishlash natijasi:
```text
tokio::io::split:

use tokio::io::{self, AsyncReadExt, AsyncWriteExt};
use tokio::net::TcpStream;

#[tokio::main]
async fn main() -> io::Result<()> {
    let socket = TcpStream::connect("127.0.0.1:8080").await?;
    let (mut oquvchi, mut yozuvchi) = io::split(socket);

    tokio::spawn(async move {
        yozuvchi.write_all(b"Salom!").await.unwrap();
    });

    let mut buf = [0u8; 10];
    oquvchi.read(&mut buf).await?;
    Ok(())
}
```

---

# 835-Topshiriq: Asinxron Pipeline: Bosqichma-bosqich qayta ishlash
## Topshiriq sharti:
1-bosqich (qabul qilish) -> 2-bosqich (shifrlash) -> 3-bosqich (saqlash) zanjirini asinxron kanallar bilan bog'lash.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Asinxron Quvur (Pipeline):");
    println!("Oqim 1 -> Kanal A -> Oqim 2 (Transformatsiya) -> Kanal B -> Oqim 3 (Saqlash)");
    println!("Har bir bosqich mustaqil task sifatida o'z tezligida parallel ishlaydi.");
}
```
## Tushuntirish va Mantiq:
Pipeline modeli katta hajmdagi video, audio yoki matnli oqimlarni uzluksiz parallel qayta ishlashda yuqori samaradorlik beradi.
## Ishlash natijasi:
```text
Asinxron Quvur (Pipeline):
Oqim 1 -> Kanal A -> Oqim 2 (Transformatsiya) -> Kanal B -> Oqim 3 (Saqlash)
Har bir bosqich mustaqil task sifatida o'z tezligida parallel ishlaydi.
```

---

# 836-Topshiriq: tokio::sync::Notify bilan oddiy signalizatsiya
## Topshiriq sharti:
`Condvar`ning asinxron muqobili bo'lgan `Notify` orqali taskni kutish va uyg'otish.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("tokio::sync::Notify:");
    println!(r#"
use tokio::sync::Notify;
use std::sync::Arc;

#[tokio::main]
async fn main() {
    let bildirishnoma = Arc::new(Notify::new());
    let b_klon = Arc::clone(&bildirishnoma);

    tokio::spawn(async move {
        println!("Tayyorgarlik ko'rilmoqda...");
        tokio::time::sleep(tokio::time::Duration::from_millis(50)).await;
        b_klon.notify_one();
    });

    bildirishnoma.notified().await;
    println!("Asosiy task uyg'ondi va ishni davom ettirdi!");
}
"#);
}
```
## Tushuntirish va Mantiq:
`Notify` hech qanday ma'lumot uzatmaydi, faqatgina asinxron signal (`notified().await`) berish uchun xizmat qiladi.
## Ishlash natijasi:
```text
tokio::sync::Notify:

use tokio::sync::Notify;
use std::sync::Arc;

#[tokio::main]
async fn main() {
    let bildirishnoma = Arc::new(Notify::new());
    let b_klon = Arc::clone(&bildirishnoma);

    tokio::spawn(async move {
        println!("Tayyorgarlik ko'rilmoqda...");
        tokio::time::sleep(tokio::time::Duration::from_millis(50)).await;
        b_klon.notify_one();
    });

    bildirishnoma.notified().await;
    println!("Asosiy task uyg'ondi va ishni davom ettirdi!");
}
```

---

# 837-Topshiriq: Asinxron Cancellation Safety (Bekor qilish xavfsizligi)
## Topshiriq sharti:
`select!` ichida `Future` bekor bo'lganda ma'lumotlar yo'qolishi yoki chala qolishi xavfini tushuntirish.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Cancellation Safety qoidasi:");
    println!("- Agar Future `.await` nuqtasida to'xtab, select! tomonidan bekor qilinsa, uning drop qilinishi ma'lumot yo'qotmasligi kerak.");
    println!("- Masalan: `AsyncReadExt::read` xavfsiz emas (chunki bir qism baytlar o'qilib drop bo'lishi mumkin).");
    println!("- Buning oldini olish uchun ma'lumotlar buferini tashqarida saqlash tavsiya etiladi.");
}
```
## Tushuntirish va Mantiq:
Tokio dasturchisi `select!` ishlatganda Future'ning 'Cancel-safe' ekanligini hujjatlardan tekshirishi shart.
## Ishlash natijasi:
```text
Cancellation Safety qoidasi:
- Agar Future `.await` nuqtasida to'xtab, select! tomonidan bekor qilinsa, uning drop qilinishi ma'lumot yo'qotmasligi kerak.
- Masalan: `AsyncReadExt::read` xavfsiz emas (chunki bir qism baytlar o'qilib drop bo'lishi mumkin).
- Buning oldini olish uchun ma'lumotlar buferini tashqarida saqlash tavsiya etiladi.
```

---

# 838-Topshiriq: Custom Waker yaratish: RawWaker va RawWakerVTable
## Topshiriq sharti:
Standart kutubxonadagi pastki darajadagi Waker mexanizmi tuzilishini ko'rsating.
## Yechim (Rust kodi):
```rust
use std::task::{RawWaker, RawWakerVTable, Waker};

fn noop(_: *const ()) {}
fn clone_fn(p: *const ()) -> RawWaker { RawWaker::new(p, &VTABLE) }

static VTABLE: RawWakerVTable = RawWakerVTable::new(
    clone_fn,
    noop,
    noop,
    noop,
);

fn main() {
    let raw = RawWaker::new(std::ptr::null(), &VTABLE);
    let waker = unsafe { Waker::from_raw(raw) };
    waker.wake_by_ref();
    println!("Maxsus RawWaker muvaffaqiyatli sinovdan o'tkazildi!");
}
```
## Tushuntirish va Mantiq:
Embedded (no_std) tizimlarda xotira allokatsiyasiz o'z shaxsiy asinxron ijrochisini yaratish uchun `RawWaker` kerak bo'ladi.
## Ishlash natijasi:
```text
Maxsus RawWaker muvaffaqiyatli sinovdan o'tkazildi!
```

---

# 839-Topshiriq: Asinxron Webhook qabul qiluvchi prototip
## Topshiriq sharti:
Tashqi tizimlardan keladigan HTTP POST xabarlarini asinxron qabul qilib navbatga tashlash.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Webhook Server arxitekturasi:");
    println!("1. TCP port ochiladi.");
    println!("2. Har bir kiruvchi HTTP so'rov tokio::spawn orqali o'qiladi.");
    println!("3. JSON payload tezkor tekshirilib, mpsc kanaliga tashlanadi va darhol '200 OK' javobi qaytariladi.");
}
```
## Tushuntirish va Mantiq:
Webhook qabul qiluvchi tizimlar tashqi xizmatni kutdirib qo'ymaslik uchun ma'lumotni darhol xotiraga olib javob qaytarishi kerak.
## Ishlash natijasi:
```text
Webhook Server arxitekturasi:
1. TCP port ochiladi.
2. Har bir kiruvchi HTTP so'rov tokio::spawn orqali o'qiladi.
3. JSON payload tezkor tekshirilib, mpsc kanaliga tashlanadi va darhol '200 OK' javobi qaytariladi.
```

---

# 840-Topshiriq: Asinxron Batching (To'plab qayta ishlash)
## Topshiriq sharti:
Har bir xabarni alohida bazaga yozish o'rniga ularni 100 tadan yoki 1 soniyada to'plab yozish.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Asinxron Batching mantiqi:");
    println!("- mpsc kanalidan kelayotgan xabarlar buferga yig'iladi.");
    println!("- Agar bufer 100 taga yetsa YOKI 500ms vaqt o'tsa, to'plam bazaga bitta tranzaksiya bilan yoziladi.");
}
```
## Tushuntirish va Mantiq:
Batching usuli disk va tarmoq IO yuklamasini yuzlab baravarga qisqartirish imkonini beradi.
## Ishlash natijasi:
```text
Asinxron Batching mantiqi:
- mpsc kanalidan kelayotgan xabarlar buferga yig'iladi.
- Agar bufer 100 taga yetsa YOKI 500ms vaqt o'tsa, to'plam bazaga bitta tranzaksiya bilan yoziladi.
```

---

# 841-Topshiriq: Yielding: tokio::task::yield_now bilan oqimni boshqalarga berish
## Topshiriq sharti:
Uzun davom etuvchi hisob-kitob paytida boshqa tasklar och qolib ketmasligi (starvation) uchun oqimni bo'shatish.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("tokio::task::yield_now:");
    println!(r#"
#[tokio::main]
async fn main() {
    tokio::spawn(async {
        for i in 1..=3 {
            println!("Og'ir qadam: {}", i);
            tokio::task::yield_now().await; // Boshqa tasklarga navbat beramiz
        }
    }).await.unwrap();
}
"#);
}
```
## Tushuntirish va Mantiq:
`yield_now().await` joriy taskni navbatning oxiriga qo'yadi va Tokio boshqa navbatdagi tasklarni bajarishiga imkon beradi.
## Ishlash natijasi:
```text
tokio::task::yield_now:

#[tokio::main]
async fn main() {
    tokio::spawn(async {
        for i in 1..=3 {
            println!("Og'ir qadam: {}", i);
            tokio::task::yield_now().await; // Boshqa tasklarga navbat beramiz
        }
    }).await.unwrap();
}
```

---

# 842-Topshiriq: Asinxron Dead-Letter Queue (DLQ) tushunchasi
## Topshiriq sharti:
3 marta qayta urinishdan keyin ham bajarilmagan xabarlarni alohida 'nosozliklar ombori'ga yuborish.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Dead-Letter Queue (DLQ):");
    println!("Asosiy navbat -> Qayta urinish (Retry x3) -> Xato bo'lsa -> DLQ navbati.");
    println!("Bu xatolikli xabarlar tufayli butun navbat to'xtab qolishining oldini oladi.");
}
```
## Tushuntirish va Mantiq:
DLQ arxitekturasi asinxron tizimlarda ma'lumotlar yo'qolishiga yo'l qo'ymasdan xatolarni tahlil qilish imkonini beradi.
## Ishlash natijasi:
```text
Dead-Letter Queue (DLQ):
Asosiy navbat -> Qayta urinish (Retry x3) -> Xato bo'lsa -> DLQ navbati.
Bu xatolikli xabarlar tufayli butun navbat to'xtab qolishining oldini oladi.
```

---

# 843-Topshiriq: tokio::sync::Barrier orqali asinxron to'siq
## Topshiriq sharti:
Bir nechta asinxron tasklar belgilangan marraga baravar yetib kelishini kutish.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("tokio::sync::Barrier:");
    println!(r#"
use tokio::sync::Barrier;
use std::sync::Arc;

#[tokio::main]
async fn main() {
    let tosiq = Arc::new(Barrier::new(3));
    // 3 ta task tosiq.wait().await qilib bir-birini kutadi
}
"#);
}
```
## Tushuntirish va Mantiq:
Sinxron Barrier oqimni to'xtatsa, asinxron Barrier oqimni emas, faqat taskni kutdiradi.
## Ishlash natijasi:
```text
tokio::sync::Barrier:

use tokio::sync::Barrier;
use std::sync::Arc;

#[tokio::main]
async fn main() {
    let tosiq = Arc::new(Barrier::new(3));
    // 3 ta task tosiq.wait().await qilib bir-birini kutadi
}
```

---

# 844-Topshiriq: Asinxron Worker Pool arxitekturasi
## Topshiriq sharti:
M ta ishchi asinxron tasklar N ta kanal orqali kelayotgan vazifalarni doimiy iste'mol qilishi.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Asinxron Worker Pool:");
    println!("- 4 ta uzoq umr ko'ruvchi worker task spawn qilinadi.");
    println!("- Har biri `while let Some(ish) = rx.recv().await` orqali vazifalarni qabul qiladi.");
}
```
## Tushuntirish va Mantiq:
Worker pool yangi tasklarni qayta-qayta ochish xarajatlarini cheklaydi va yuklama balansini saqlaydi.
## Ishlash natijasi:
```text
Asinxron Worker Pool:
- 4 ta uzoq umr ko'ruvchi worker task spawn qilinadi.
- Har biri `while let Some(ish) = rx.recv().await` orqali vazifalarni qabul qiladi.
```

---

# 845-Topshiriq: Asinxron Tracing va Instrumentatsiya asoslari
## Topshiriq sharti:
`tracing` va `tokio` orqali asinxron operatsiyalarning qancha vaqt olganini loglash.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Tracing instrumentatsiyasi:");
    println!("- `tracing::instrument` makrosi har bir async fn uchun yangi span ochadi.");
    println!("- Tasklar o'rtasidagi o'tishlar va kutilishlar aniq vaqt belgilari bilan yoziladi.");
}
```
## Tushuntirish va Mantiq:
Asinxron dasturlarda an'anaviy thread ID bo'yicha loglash qiyin, shuning uchun Span va TraceID ga asoslangan `tracing` kutubxonasi ishlatiladi.
## Ishlash natijasi:
```text
Tracing instrumentatsiyasi:
- `tracing::instrument` makrosi har bir async fn uchun yangi span ochadi.
- Tasklar o'rtasidagi o'tishlar va kutilishlar aniq vaqt belgilari bilan yoziladi.
```

---

# 846-Topshiriq: Async DNS Resolver mexanizmi
## Topshiriq sharti:
Host nomini (domain) IP manzilga o'girish jarayonining asinxron ishlashi.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("tokio::net::lookup_host:");
    println!(r#"
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut manzillar = tokio::net::lookup_host("localhost:8080").await?;
    while let Some(manzil) = manzillar.next() {
        println!("Topilgan manzil: {}", manzil);
    }
    Ok(())
}
"#);
}
```
## Tushuntirish va Mantiq:
Standart kutubxonadagi DNS qidirish bloklovchi bo'lgani uchun Tokio uni fondagi oqimlar orqali non-blocking qiladi.
## Ishlash natijasi:
```text
tokio::net::lookup_host:

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut manzillar = tokio::net::lookup_host("localhost:8080").await?;
    while let Some(manzil) = manzillar.next() {
        println!("Topilgan manzil: {}", manzil);
    }
    Ok(())
}
```

---

# 847-Topshiriq: Asinxron MutexGuard va Scope xavfsizligi
## Topshiriq sharti:
Mutex qulfini `.await` orqali uzoq ushlab turmaslik va blokdan tez chiqish tavsiyasi.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Qulfni scope orqali tezda bo'shatish:");
    println!(r#"
// Yomon usul:
// let qulf = mutex.lock().await;
// sekin_tarmoq_amali().await; // Qulf tarmoq amali paytida ochiq qoladi!

// To'g'ri usul:
let data = {
    let qulf = mutex.lock().await;
    qulf.clone()
}; // Qulf shu zahoti yopildi
sekin_tarmoq_amali().await;
"#);
}
```
## Tushuntirish va Mantiq:
Qulfni asinxron amallar (`.await`) davomida ushlab turish boshqa barcha tasklarning to'xtab qolishiga olib keladi.
## Ishlash natijasi:
```text
Qulfni scope orqali tezda bo'shatish:

// Yomon usul:
// let qulf = mutex.lock().await;
// sekin_tarmoq_amali().await; // Qulf tarmoq amali paytida ochiq qoladi!

// To'g'ri usul:
let data = {
    let qulf = mutex.lock().await;
    qulf.clone()
}; // Qulf shu zahoti yopildi
sekin_tarmoq_amali().await;
```

---

# 848-Topshiriq: Asinxron Backpressure (Orqaga bosim) mexanizmi
## Topshiriq sharti:
Tezkor jo'natuvchi sekin iste'molchini xotirada yutib yubormasligi uchun bounded kanal va ruxsatnomalar.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Backpressure qoidasi:");
    println!("- Agar kanal sig'imi to'lsa, `tx.send().await` avtomatik tarzda jo'natuvchi taskni to'xtatib turadi.");
    println!("- Shunda xotira to'lib ketishi (Out-Of-Memory) butunlay bartaraf etiladi.");
}
```
## Tushuntirish va Mantiq:
Backpressure barqaror tarmoq tizimlarining eng muhim mezonidir.
## Ishlash natijasi:
```text
Backpressure qoidasi:
- Agar kanal sig'imi to'lsa, `tx.send().await` avtomatik tarzda jo'natuvchi taskni to'xtatib turadi.
- Shunda xotira to'lib ketishi (Out-Of-Memory) butunlay bartaraf etiladi.
```

---

# 849-Topshiriq: Asinxron Future polling lifecyle: Pending, Ready va Waker
## Topshiriq sharti:
Qo'lda Future poll qilganda lifecycleni to'liq kuzatuvchi kod yozing.
## Yechim (Rust kodi):
```rust
use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

struct SanagichFuture {
    joriy: u32,
    chegara: u32,
}

impl Future for SanagichFuture {
    type Output = u32;

    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output> {
        self.joriy += 1;
        println!("Poll bosqichi: joriy = {}", self.joriy);

        if self.joriy >= self.chegara {
            Poll::Ready(self.joriy)
        } else {
            cx.waker().wake_by_ref(); // Qayta uyg'otamiz
            Poll::Pending
        }
    }
}

fn main() {
    let mut fut = SanagichFuture { joriy: 0, chegara: 3 };
    let waker = std::task::Waker::noop();
    let mut cx = Context::from_waker(&waker);
    let mut p = Pin::new(&mut fut);

    loop {
        match p.as_mut().poll(&mut cx) {
            Poll::Ready(res) => { println!("Ready: {}", res); break; }
            Poll::Pending => { println!("Pending..."); }
        }
    }
}
```
## Tushuntirish va Mantiq:
`poll` har safar chaqirilganda agar ish bitmagan bo'lsa `waker.wake()` chaqirilib, executorga qayta urinish signali beriladi.
## Ishlash natijasi:
```text
Poll bosqichi: joriy = 1
Pending...
Poll bosqichi: joriy = 2
Pending...
Poll bosqichi: joriy = 3
Ready: 3
```

---

# 850-Topshiriq: Katta Asinxron Integratsion Loyiha: Asinxron Xabarlar Brokeri
## Topshiriq sharti:
Mavzular (Topics) bo'yicha xabarlarni tarqatuvchi to'liq asinxron chat/broker arxitekturasi.
## Yechim (Rust kodi):
```rust
use std::collections::HashMap;

struct XabarBrokeri {
    mavzular: HashMap<String, Vec<String>>,
}

impl XabarBrokeri {
    fn new() -> Self {
        XabarBrokeri { mavzular: HashMap::new() }
    }

    fn xabar_yuborish(&mut self, mavzu: &str, xabar: &str) {
        self.mavzular
            .entry(mavzu.to_string())
            .or_insert_with(Vec::new)
            .push(xabar.to_string());
    }

    fn xabarlarni_olish(&self, mavzu: &str) -> Option<&Vec<String>> {
        self.mavzular.get(mavzu)
    }
}

fn main() {
    let mut broker = XabarBrokeri::new();

    broker.xabar_yuborish("yangiliklar", "Rust 2024 relizi e'lon qilindi!");
    broker.xabar_yuborish("texnologiya", "Asinxron dasturlash yangi bosqichda.");

    println!("=== ASINXRON BROKER NATIJALARI ===");
    if let Some(royxat) = broker.xabarlarni_olish("yangiliklar") {
        for x in royxat {
            println!("[Yangilik]: {}", x);
        }
    }
    if let Some(royxat) = broker.xabarlarni_olish("texnologiya") {
        for x in royxat {
            println!("[Texno]: {}", x);
        }
    }
}
```
## Tushuntirish va Mantiq:
Asinxron xabarlar brokeri mavzular (topics), navbatlar va pub/sub mexanizmlari orqali mikroservislarni xavfsiz va samarali o'zaro bog'laydi.
## Ishlash natijasi:
```text
=== ASINXRON BROKER NATIJALARI ===
[Yangilik]: Rust 2024 relizi e'lon qilindi!
[Texno]: Asinxron dasturlash yangi bosqichda.
```

---
