# 14-Qism: Iteratorlar va Closurelar (Funksional Dasturlash) (651-700)

Ushbu qismda Rust ning funksional dasturlash qudrati bo'lgan **Closurelar (Anonim funksiyalar)**, ularning turlari (`Fn`, `FnMut`, `FnOnce`), `move` closurelar, **Iterator traiti**, `map`, `filter`, `fold`, `reduce`, `flat_map`, `zip`, `chain`, `peekable`, cheksiz iteratorlar, maxsus iteratorlar yaratish hamda Nol-xarajatli abstraksiya (Zero-cost functional pipelines) o'rganiladi.

---

# 651-Topshiriq: Closure nima? Anonim funksiyalar sintaksisi (|x| x + 1)
## Topshiriq sharti:
O'zgaruvchida saqlanuvchi va darhol chaqiriluvchi oddiy closure yarating.

## Yechim (Rust kodi):
```rust
fn main() {
    let bir_qosh = |x: i32| x + 1;

    let natija = bir_qosh(10);
    println!("Closure natijasi: {}", natija);
}
```

## Tushuntirish va Mantiq:
Closure bu parametrlarini `|a, b|` orasida qabul qiluvchi anonim inline funksiyadir. U o'zgaruvchilarda saqlanishi va boshqa funksiyalarga uzatilishi mumkin.

## Ishlash natijasi:
```text
Closure natijasi: 11
```

---

# 652-Topshiriq: Closurelarda tashqi o'zgaruvchilarni ushlash (Capturing environment)
## Topshiriq sharti:
Tashqi o'zgaruvchini closure ichida o'qish.

## Yechim (Rust kodi):
```rust
fn main() {
    let koeffitsiyent = 3;

    let kopaytir = |x| x * koeffitsiyent; // 'koeffitsiyent' tashqaridan ushlandi

    println!("5 * 3 = {}", kopaytir(5));
}
```

## Tushuntirish va Mantiq:
Oddiy funksiyalardan farqli ravishda, closurelar o'zlari e'lon qilingan muhitdagi tashqi o'zgaruvchilarni erkin ushlay (capture qila) oladi.

## Ishlash natijasi:
```text
5 * 3 = 15
```

---

# 653-Topshiriq: Fn traiti: O'zgarmas qarzga oluvchi closure
## Topshiriq sharti:
Tashqi muhitni o'zgartirmasdan faqat o'qish uchun foydalanuvchi closure.

## Yechim (Rust kodi):
```rust
fn main() {
    let matn = String::from("Rust");

    let oquvchi = || println!("Matn o'qildi: {}", matn);

    oquvchi();
    oquvchi(); // Fn bo'lgani uchun bir necha marta chaqirish mumkin
    println!("Asl matn hali ham yaroqli: {}", matn);
}
```

## Tushuntirish va Mantiq:
`Fn` traiti tashqi o'zgaruvchini `&T` (o'zgarmas havola) orqali ushlaydi va uni istalgancha ko'p chaqirish mumkin.

## Ishlash natijasi:
```text
Matn o'qildi: Rust
Matn o'qildi: Rust
Asl matn hali ham yaroqli: Rust
```

---

# 654-Topshiriq: FnMut traiti: O'zgaruvchan qarzga oluvchi closure
## Topshiriq sharti:
Tashqi o'zgaruvchi qiymatini har chaqiruvda o'zgartirib boruvchi closure.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut hisob = 0;

    let mut qoshuvchi = || {
        hisob += 10;
        println!("Joriy hisob: {}", hisob);
    };

    qoshuvchi();
    qoshuvchi();
}
```

## Tushuntirish va Mantiq:
`FnMut` traiti tashqi muhitni `&mut T` orqali ushlaydi. Closure ning o'zi ham `mut qoshuvchi` bo'lishi shart.

## Ishlash natijasi:
```text
Joriy hisob: 10
Joriy hisob: 20
```

---

# 655-Topshiriq: FnOnce traiti: Qiymat egasligini iste'mol qiluvchi closure
## Topshiriq sharti:
Tashqi resursni Move qilib faqat bir marta chaqirilishi mumkin bo'lgan closure.

## Yechim (Rust kodi):
```rust
fn main() {
    let ma'lumot = vec![1, 2, 3];

    let iste'molchi = || {
        let ichki = ma'lumot; // ma'lumot MOVE bo'ldi
        println!("Vektor uzunligi: {}", ichki.len());
    };

    iste'molchi();
    // iste'molchi(); // Xatolik: FnOnce faqat BIR MARTA chaqirilishi mumkin!
}
```

## Tushuntirish va Mantiq:
`FnOnce` tashqi resursni to'liq o'zlashtiradi (iste'mol qiladi). Shuning uchun u faqat bitta marta chaqirilishi mumkin.

## Ishlash natijasi:
```text
Vektor uzunligi: 3
```

---

# 656-Topshiriq: move closure: Egaslikni closure ichiga majburiy ko'chirish
## Topshiriq sharti:
`move` kalit so'zi bilan tashqi o'zgaruvchini closure ga o'tkazish.

## Yechim (Rust kodi):
```rust
fn main() {
    let ism = String::from("Sardor");

    let salom = move || {
        println!("Salom, {}!", ism);
    };

    salom();
    // println!("{}", ism); // Xatolik: ism closure ichiga MOVE bo'lgan!
}
```

## Tushuntirish va Mantiq:
`move ||` o'zgaruvchilarning egasligini closure xotirasiga o'tkazadi. Bu asosan oqimlarga (threads) ma'lumot uzatishda majburiydir.

## Ishlash natijasi:
```text
Salom, Sardor!
```

---

# 657-Topshiriq: Funksiyaga closure ni parametr sifatida uzatish
## Topshiriq sharti:
Yuqori tartibli funksiya yozib, unga ixtiyoriy closure uzating.

## Yechim (Rust kodi):
```rust
fn son_ustida_amal<F>(son: i32, amal: F) -> i32
where
    F: Fn(i32) -> i32,
{
    amal(son)
}

fn main() {
    let kvadrat = |x| x * x;
    println!("Kvadrat (6): {}", son_ustida_amal(6, kvadrat));
}
```

## Tushuntirish va Mantiq:
Generik parametr `F: Fn(...) -> ...` orqali funksiyalar closurelarni qabul qiladi va bu kodni o'ta moslashuvchan qiladi.

## Ishlash natijasi:
```text
Kvadrat (6): 36
```

---

# 658-Topshiriq: Iterator traiti va next() metodi
## Topshiriq sharti:
Iteratorning har bir chaqiruvda `Option<Item>` qaytarish mexanizmi.

## Yechim (Rust kodi):
```rust
fn main() {
    let sonlar = vec![10, 20];
    let mut iter = sonlar.iter();

    println!("1-qadam: {:?}", iter.next());
    println!("2-qadam: {:?}", iter.next());
    println!("3-qadam: {:?}", iter.next());
}
```

## Tushuntirish va Mantiq:
Rust da barcha iteratorlar `Iterator` traitiga tayanadi. Uning `next()` metodi keyingi elementni yoki tugaganda `None` qaytaradi.

## Ishlash natijasi:
```text
1-qadam: Some(10)
2-qadam: Some(20)
3-qadam: None
```

---

# 659-Topshiriq: iter(), iter_mut() va into_iter() farqi
## Topshiriq sharti:
Kolleksiyadan o'qish, o'zgartirish va iste'mol qilish iteratorlarini olish.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut v = vec![1, 2, 3];

    // iter(): &T (havolalar)
    for &elem in v.iter() { print!("{} ", elem); }
    println!();

    // iter_mut(): &mut T (o'zgartirish)
    for elem in v.iter_mut() { *elem *= 10; }

    // into_iter(): T (egaslikni oladi, vektor yo'qoladi)
    for elem in v.into_iter() { print!("{} ", elem); }
    println!();
}
```

## Tushuntirish va Mantiq:
`iter()` o'qish uchun, `iter_mut()` o'zgartirish uchun, `into_iter()` esa kolleksiyani yo'q qilib elementlarni to'liq o'zlashtirish uchun xizmat qiladi.

## Ishlash natijasi:
```text
1 2 3 
10 20 30 
```

---

# 660-Topshiriq: Lazy Iterators: Iteratorlarning dangasalik tamoyili
## Topshiriq sharti:
Adapterlar yakuniy iste'molchi chaqirilmaguncha ishga tushmasligini ko'rsating.

## Yechim (Rust kodi):
```rust
fn main() {
    let sonlar = vec![1, 2, 3];

    // Bu qatorda hech qanday hisob-kitob bajarilmaydi (Lazy!):
    let iter = sonlar.iter().map(|x| {
        println!("Map ishladi: {}", x);
        x * 2
    });

    println!("Iterator yaratildi, lekin hali ishlatilmadi.");

    // Faqat iste'molchi (.collect() yoki for) kelgandagina ishga tushadi:
    let _: Vec<_> = iter.collect();
}
```

## Tushuntirish va Mantiq:
Rust iteratorlari dangasa (lazy) hisoblanadi. Agar natija talab qilinmasa, hech qanday sikl aylanmaydi va resurs tejaladi.

## Ishlash natijasi:
```text
Iterator yaratildi, lekin hali ishlatilmadi.
Map ishladi: 1
Map ishladi: 2
Map ishladi: 3
```

---

# 661-Topshiriq: Iterator adapteri: map (Har bir elementni o'zgartirish)
## Topshiriq sharti:
Barcha sonlarni 3 barobar oshirib yangi vektor hosil qiling.

## Yechim (Rust kodi):
```rust
fn main() {
    let sonlar = vec![1, 2, 3, 4];
    let oshirilgan: Vec<i32> = sonlar.iter().map(|x| x * 3).collect();

    println!("3 barobar oshirilgan: {:?}", oshirilgan);
}
```

## Tushuntirish va Mantiq:
`map()` har bir elementga closureni qo'llab yangi iterator beradi.

## Ishlash natijasi:
```text
3 barobar oshirilgan: [3, 6, 9, 12]
```

---

# 662-Topshiriq: Iterator adapteri: filter (Shart bo'yicha saralash)
## Topshiriq sharti:
Faqat 10 dan katta bo'lgan sonlarni ajrating.

## Yechim (Rust kodi):
```rust
fn main() {
    let sonlar = vec![5, 12, 3, 18, 9, 25];
    let kattalar: Vec<_> = sonlar.into_iter().filter(|&x| x > 10).collect();

    println!("10 dan kattalar: {:?}", kattalar);
}
```

## Tushuntirish va Mantiq:
`filter()` predicate (shart) `true` bo'lgan elementlarnigina keyingi bosqichga o'tkazadi.

## Ishlash natijasi:
```text
10 dan kattalar: [12, 18, 25]
```

---

# 663-Topshiriq: Iterator adapteri: filter_map (Option qaytaruvchi filtr)
## Topshiriq sharti:
Matnlarni songa o'girib, faqat to'g'ri o'girilganlarini qoldiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let matnlar = vec!["10", "xato", "30", "salom", "50"];
    let sonlar: Vec<i32> = matnlar.iter().filter_map(|s| s.parse::<i32>().ok()).collect();

    println!("Ajratilgan sonlar: {:?}", sonlar);
}
```

## Tushuntirish va Mantiq:
`filter_map()` ham `filter`, ham `map` vazifasini bir amalda bajaradi: `Some(v)` bo'lsa `v` ni oladi, `None` bo'lsa tashlab ketadi.

## Ishlash natijasi:
```text
Ajratilgan sonlar: [10, 30, 50]
```

---

# 664-Topshiriq: Iterator iste'molchilari: sum(), product(), count()
## Topshiriq sharti:
Matematik yig'indi, ko'paytma va sonini bitta chaqiruvda oling.

## Yechim (Rust kodi):
```rust
fn main() {
    let sonlar = [1, 2, 3, 4, 5];

    println!("Yig'indi (sum):     {}", sonlar.iter().sum::<i32>());
    println!("Ko'paytma (product): {}", sonlar.iter().product::<i32>());
    println!("Soni (count):        {}", sonlar.iter().count());
}
```

## Tushuntirish va Mantiq:
Standart iste'molchi metodlar iteratorni to'liq aylanib chiqib, yagona natija beradi.

## Ishlash natijasi:
```text
Yig'indi (sum):     15
Ko'paytma (product): 120
Soni (count):        5
```

---

# 665-Topshiriq: Iterator iste'molchisi: fold() (Akkumulyator bilan yig'ish)
## Topshiriq sharti:
Boshlang'ich qiymatdan boshlab elementlarni yig'ish.

## Yechim (Rust kodi):
```rust
fn main() {
    let sonlar = [1, 2, 3, 4];

    // 100 boshlang'ich qiymat bilan: 100 + 1 + 2 + 3 + 4 = 110
    let jami = sonlar.iter().fold(100, |acc, &x| acc + x);

    println!("Fold natijasi: {}", jami);
}
```

## Tushuntirish va Mantiq:
`fold(boshlang'ich, |akkumulyator, element| ...)` boshqa tillardagi `reduce` ning yanada qulay va xavfsiz analogidir.

## Ishlash natijasi:
```text
Fold natijasi: 110
```

---

# 666-Topshiriq: Iterator iste'molchisi: reduce()
## Topshiriq sharti:
Boshlang'ich qiymatsiz to'plam elementlarini birlashtirish.

## Yechim (Rust kodi):
```rust
fn main() {
    let sonlar = [10, 20, 30];
    let yigindi = sonlar.iter().copied().reduce(|a, b| a + b);

    println!("Reduce yig'indisi: {:?}", yigindi);
}
```

## Tushuntirish va Mantiq:
`reduce()` birinchi elementni boshlang'ich deb oladi va agar to'plam bo'sh bo'lsa `None` qaytaradi.

## Ishlash natijasi:
```text
Reduce yig'indisi: Some(60)
```

---

# 667-Topshiriq: Iterator qidiruvchisi: find() va position()
## Topshiriq sharti:
Shartga mos birinchi element va uning indeksini toping.

## Yechim (Rust kodi):
```rust
fn main() {
    let sonlar = [12, 17, 24, 31, 40];

    let birinchi_toq = sonlar.iter().find(|&&x| x % 2 == 1);
    let toq_indeksi = sonlar.iter().position(|&x| x % 2 == 1);

    println!("Birinchi toq son: {:?}", birinchi_toq);
    println!("Uning indeksi:     {:?}", toq_indeksi);
}
```

## Tushuntirish va Mantiq:
`find()` qiymatning o'zini, `position()` esa uning indeksini qidiradi.

## Ishlash natijasi:
```text
Birinchi toq son: Some(17)
Uning indeksi:     Some(1)
```

---

# 668-Topshiriq: Mantiqiy tekshiruvchilar: any() va all()
## Topshiriq sharti:
To'plamda manfiy son bormi yoki hammasi musbatmi ekanligini aniqlang.

## Yechim (Rust kodi):
```rust
fn main() {
    let sonlar = [2, 4, 6, 8, 10];

    println!("Kamida bittasi toqmi (any): {}", sonlar.iter().any(|&x| x % 2 == 1));
    println!("Hammasi juftmi (all):       {}", sonlar.iter().all(|&x| x % 2 == 0));
}
```

## Tushuntirish va Mantiq:
`any()` kamida bitta `true` bo'lsa darhol to'xtaydi, `all()` esa bitta `false` bo'lsa darhol to'xtaydi (short-circuit).

## Ishlash natijasi:
```text
Kamida bittasi toqmi (any): false
Hammasi juftmi (all):       true
```

---

# 669-Topshiriq: Iterator adapteri: zip (Ikkita iteratorni juftlash)
## Topshiriq sharti:
Ismlar va yoshlar ro'yxatini bitta qatorda birlashtiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let ismlar = ["Ali", "Vali", "Sardor"];
    let yoshlar = [20, 25, 30];

    for (ism, yosh) in ismlar.iter().zip(yoshlar.iter()) {
        println!("{}: {} yoshda", ism, yosh);
    }
}
```

## Tushuntirish va Mantiq:
`zip()` ikkita oqimdan navbatma-navbat element olib, `(A, B)` juftligini hosil qiladi.

## Ishlash natijasi:
```text
Ali: 20 yoshda
Vali: 25 yoshda
Sardor: 30 yoshda
```

---

# 670-Topshiriq: Iterator adapteri: take() va skip()
## Topshiriq sharti:
Dastlabki 3 ta elementni olish va qolganini o'tkazib yuborish.

## Yechim (Rust kodi):
```rust
fn main() {
    let sonlar = [10, 20, 30, 40, 50, 60];

    let olingan: Vec<_> = sonlar.iter().skip(2).take(3).copied().collect();
    println!("2 ta o'tkazib 3 ta olindi: {:?}", olingan);
}
```

## Tushuntirish va Mantiq:
`skip(n)` va `take(m)` sahifalash (pagination) mexanizmlarida eng qulay kombinatsiyadir.

## Ishlash natijasi:
```text
2 ta o'tkazib 3 ta olindi: [30, 40, 50]
```

---

# 671-Topshiriq: Iterator adapteri: chain (Ikkita iteratorni ulash)
## Topshiriq sharti:
Ikki xil massivni ketma-ket bitta oqimga ulang.

## Yechim (Rust kodi):
```rust
fn main() {
    let a = [1, 2, 3];
    let b = [4, 5, 6];

    let zanjir: Vec<_> = a.iter().chain(b.iter()).copied().collect();
    println!("Uzluksiz zanjir: {:?}", zanjir);
}
```

## Tushuntirish va Mantiq:
`chain()` birinchi iterator tugashi bilan avtomatik ikkinchisiga ulanadi.

## Ishlash natijasi:
```text
Uzluksiz zanjir: [1, 2, 3, 4, 5, 6]
```

---

# 672-Topshiriq: Iterator adapteri: flat_map va flatten
## Topshiriq sharti:
Ichma-ich vektorlarni bitta tekis ro'yxatga aylantiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let jadvallar = vec![vec![1, 2], vec![3, 4], vec![5, 6]];
    let tekis: Vec<i32> = jadvallar.into_iter().flatten().collect();

    println!("Tekislangan ro'yxat: {:?}", tekis);
}
```

## Tushuntirish va Mantiq:
`flatten()` ichki kolleksiyalarni bitta chiziqli oqimga yoyadi.

## Ishlash natijasi:
```text
Tekislangan ro'yxat: [1, 2, 3, 4, 5, 6]
```

---

# 673-Topshiriq: Cheksiz iteratorlar (Infinite Iterators) va take()
## Topshiriq sharti:
0 dan boshlanuvchi cheksiz oqimdan faqat dastlabki 5 ta sonni oling.

## Yechim (Rust kodi):
```rust
fn main() {
    let cheksiz = 0..; // Cheksiz oraliq
    let dastlabki_5: Vec<_> = cheksiz.take(5).collect();

    println!("Cheksiz oqimdan 5 ta olindi: {:?}", dastlabki_5);
}
```

## Tushuntirish va Mantiq:
Rust ning dangasa (lazy) tabiati cheksiz ketma-ketliklarni yaratishga imkon beradi, chunki xotira faqat `take` qilinganicha sarflanadi.

## Ishlash natijasi:
```text
Cheksiz oqimdan 5 ta olindi: [0, 1, 2, 3, 4]
```

---

# 674-Topshiriq: Maxsus Iterator yaratish: impl Iterator for Fibonachchi
## Topshiriq sharti:
O'z Fibonachchi ketma-ketligi iteratoringizni yozing.

## Yechim (Rust kodi):
```rust
struct Fibonachchi {
    a: u64,
    b: u64,
}

impl Fibonachchi {
    fn new() -> Self { Self { a: 0, b: 1 } }
}

impl Iterator for Fibonachchi {
    type Item = u64;

    fn next(&mut self) -> Option<Self::Item> {
        let joriy = self.a;
        self.a = self.b;
        self.b = joriy + self.b;
        Some(joriy)
    }
}

fn main() {
    let fib = Fibonachchi::new();
    let birinchi_8: Vec<_> = fib.take(8).collect();

    println!("Fibonachchi sonlari: {:?}", birinchi_8);
}
```

## Tushuntirish va Mantiq:
`impl Iterator for T` qilish orqali har qanday matematik model standart iteratorga aylanadi va barcha `map`, `filter`, `take` metodlariga ega bo'ladi.

## Ishlash natijasi:
```text
Fibonachchi sonlari: [0, 1, 1, 2, 3, 5, 8, 13]
```

---

# 675-Topshiriq: Iterator adapteri: peekable() va peek()
## Topshiriq sharti:
Keyingi elementni oqimdan chiqarmasdan turib oldindan ko'rish.

## Yechim (Rust kodi):
```rust
fn main() {
    let sonlar = [1, 2, 3];
    let mut iter = sonlar.iter().peekable();

    println!("Oldindan ko'rindi: {:?}", iter.peek());
    println!("Asl o'qish:        {:?}", iter.next());
    println!("Yana ko'rindi:    {:?}", iter.peek());
}
```

## Tushuntirish va Mantiq:
`peekable()` parserlar va kompilyatorlar uchun eng muhim vositadir: keyingi belgini ko'rib, shunga qarab qaror qabul qilishga imkon beradi.

## Ishlash natijasi:
```text
Oldindan ko'rindi: Some(1)
Asl o'qish:        Some(1)
Yana ko'rindi:    Some(2)
```

---

# 676-Topshiriq: Iterator adapteri: step_by()
## Topshiriq sharti:
Qadam tashlab (masalan har 2-elementni) o'qish.

## Yechim (Rust kodi):
```rust
fn main() {
    let sonlar = 0..=10;
    let juftlar: Vec<_> = sonlar.step_by(2).collect();

    println!("2 qadam bilan: {:?}", juftlar);
}
```

## Tushuntirish va Mantiq:
`step_by(step)` iteratsiyani berilgan qadam bo'yicha sakrab o'tkazadi.

## Ishlash natijasi:
```text
2 qadam bilan: [0, 2, 4, 6, 8, 10]
```

---

# 677-Topshiriq: Iterator adapteri: rev() (Teskari aylanish)
## Topshiriq sharti:
To'plamni oxiridan boshlab o'qish.

## Yechim (Rust kodi):
```rust
fn main() {
    let sozlar = ["Bir", "Ikki", "Uch"];
    let teskari: Vec<_> = sozlar.iter().rev().copied().collect();

    println!("Teskari: {:?}", teskari);
}
```

## Tushuntirish va Mantiq:
`DoubleEndedIterator` traitiga ega har qanday iterator `.rev()` bilan teskari aylantiriladi.

## Ishlash natijasi:
```text
Teskari: ["Uch", "Ikki", "Bir"]
```

---

# 678-Topshiriq: Funksional pipeline orqali toq sonlar kvadratlari yig'indisi
## Topshiriq sharti:
Bitta toza zanjirda hisoblash.

## Yechim (Rust kodi):
```rust
fn main() {
    let sonlar = 1..=10;

    let natija: i32 = sonlar
        .filter(|x| x % 2 != 0) // Faqat toqlar: 1, 3, 5, 7, 9
        .map(|x| x * x)          // Kvadratlari: 1, 9, 25, 49, 81
        .sum();                  // Yig'indisi: 165

    println!("Toq sonlar kvadratlari yig'indisi: {}", natija);
}
```

## Tushuntirish va Mantiq:
Funksional uslub kodni xatosiz, ixcham va toza matematik ko'rinishga keltiradi.

## Ishlash natijasi:
```text
Toq sonlar kvadratlari yig'indisi: 165
```

---

# 679-Topshiriq: Iterator partition(): To'plamni 2 ta vektorga ajratish
## Topshiriq sharti:
Juft va toq sonlarni bitta amalda ikkita alohida ro'yxatga oling.

## Yechim (Rust kodi):
```rust
fn main() {
    let sonlar = vec![1, 2, 3, 4, 5, 6];

    let (juftlar, toqlar): (Vec<i32>, Vec<i32>) = sonlar.into_iter().partition(|&n| n % 2 == 0);

    println!("Juftlar: {:?}", juftlar);
    println!("Toqlar:  {:?}", toqlar);
}
```

## Tushuntirish va Mantiq:
`partition()` shartga mos kelganlarni chapga, mos kelmaganlarni o'ngga ajratadi.

## Ishlash natijasi:
```text
Juftlar: [2, 4, 6]
Toqlar:  [1, 3, 5]
```

---

# 680-Topshiriq: Iterator unzip(): Juftliklar ro'yxatini ikkita alohida vektorga yoyish
## Topshiriq sharti:
`(X, Y)` kortejlari vektorini ikkita alohida vektorga ajrating.

## Yechim (Rust kodi):
```rust
fn main() {
    let juftliklar = vec![(1, "A"), (2, "B"), (3, "C")];
    let (sonlar, harflar): (Vec<i32>, Vec<&str>) = juftliklar.into_iter().unzip();

    println!("Sonlar:  {:?}", sonlar);
    println!("Harflar: {:?}", harflar);
}
```

## Tushuntirish va Mantiq:
`unzip()` `zip()` ning teskarisi bo'lib, kortejlar oqimini ajratadi.

## Ishlash natijasi:
```text
Sonlar:  [1, 2, 3]
Harflar: ["A", "B", "C"]
```

---

# 681-Topshiriq: Iterator inspect() orqali pipeline oralig'ini kuzatish (Debug)
## Topshiriq sharti:
Oqim ichida qanday ma'lumotlar o'tayotganini konsolga chiqarib tekshiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let _natija: Vec<i32> = (1..=3)
        .inspect(|x| println!("Boshlang'ich: {}", x))
        .map(|x| x * 10)
        .inspect(|x| println!("Ko'paytirilgan: {}", x))
        .collect();
}
```

## Tushuntirish va Mantiq:
`inspect` oraliq logging uchun qulay vositadir va ma'lumotlarni o'zgartirmaydi.

## Ishlash natijasi:
```text
Boshlang'ich: 1
Ko'paytirilgan: 10
Boshlang'ich: 2
Ko'paytirilgan: 20
Boshlang'ich: 3
Ko'paytirilgan: 30
```

---

# 682-Topshiriq: Iterator scan(): O'zgaruvchan holat bilan hisoblash
## Topshiriq sharti:
Kümülatif yig'indi (Running Total) ketma-ketligini hosil qiling.

## Yechim (Rust kodi):
```rust
fn main() {
    let sonlar = [1, 2, 3, 4];

    let yigindi: Vec<i32> = sonlar.iter().scan(0, |holat, &x| {
        *holat += x;
        Some(*holat)
    }).collect();

    println!("O'suvchi yig'indi: {:?}", yigindi);
}
```

## Tushuntirish va Mantiq:
`scan` ichki o'zgaruvchan holatga ega iterator hosil qiladi.

## Ishlash natijasi:
```text
O'suvchi yig'indi: [1, 3, 6, 10]
```

---

# 683-Topshiriq: Iterator cycle() orqali cheksiz aylanma hosil qilish
## Topshiriq sharti:
Ranglarni navbatma-navbat cheksiz chiqaruvchi oqim.

## Yechim (Rust kodi):
```rust
fn main() {
    let ranglar = ["Qizil", "Yashil", "Kok"];
    let aylanma: Vec<_> = ranglar.iter().cycle().take(7).copied().collect();

    println!("7 ta davriy rang: {:?}", aylanma);
}
```

## Tushuntirish va Mantiq:
`cycle()` to'plam tugashi bilan uni yana boshidan qayta boshlaydi.

## Ishlash natijasi:
```text
7 ta davriy rang: ["Qizil", "Yashil", "Kok", "Qizil", "Yashil", "Kok", "Qizil"]
```

---

# 684-Topshiriq: Zero-cost Abstraction: Iteratorlarning unumdorligi
## Topshiriq sharti:
Rust da iterator zanjiri nima sababdan C uslubidagi `for` tsiklichalik tez ishlashini tushuntiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let v = [10, 20, 30, 40, 50];
    let sum: i32 = v.iter().map(|x| x * 2).sum();

    println!("Sum: {}", sum);
    println!("LLVM kompilyatori barcha closure va iteratorlarni bitta optimallashtirilgan SIMD registrli mashina kodiga aylantiradi!");
}
```

## Tushuntirish va Mantiq:
Rust da funksional iteratorlar qo'shimcha xotira sarflamaydi. Kompilyator ularni to'liq 'unroll' qilib eng tezkor mashina ko'rsatmalariga aylantiradi.

## Ishlash natijasi:
```text
Sum: 300
LLVM kompilyatori barcha closure va iteratorlarni bitta optimallashtirilgan SIMD registrli mashina kodiga aylantiradi!
```

---

# 685-Topshiriq: Closure yordamida dinamik solishtiruvchi (Dynamic Comparator)
## Topshiriq sharti:
Foydalanuvchi talabiga ko'ra o'suvchi yoki kamayuvchi saralash.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut sonlar = vec![5, 2, 8, 1, 9];
    let kamayuvchi = true;

    sonlar.sort_by(|a, b| {
        if kamayuvchi { b.cmp(a) } else { a.cmp(b) }
    });

    println!("Saralangan: {:?}", sonlar);
}
```

## Tushuntirish va Mantiq:
Closurelar tashqi o'zgaruvchilarni ushlashi orqali dinamik saralash qoidalarini tuzishga imkon beradi.

## Ishlash natijasi:
```text
Saralangan: [9, 8, 5, 2, 1]
```

---

# 686-Topshiriq: Matndan unikal so'zlar sonini topish funksional zanjirda
## Topshiriq sharti:
Matnni tozalab, bo'lib, unikal so'zlarni sanash.

## Yechim (Rust kodi):
```rust
use std::collections::HashSet;

fn unikal_sozlar_soni(matn: &str) -> usize {
    matn.split_whitespace()
        .map(|s| s.trim_matches(|c: char| !c.is_alphabetic()).to_lowercase())
        .filter(|s| !s.is_empty())
        .collect::<HashSet<_>>()
        .len()
}

fn main() {
    let jumla = "Rust tili, juda tezkor Rust tili!";
    println!("Unikal so'zlar: {}", unikal_sozlar_soni(jumla));
}
```

## Tushuntirish va Mantiq:
Funksional pipeline matnni bir necha bosqichda tozalab tahlil qiladi.

## Ishlash natijasi:
```text
Unikal so'zlar: 3
```

---

# 687-Topshiriq: Iterator min_by_key va max_by_key
## Topshiriq sharti:
Struktura maydoni bo'yicha eng kichik va eng kattasini toping.

## Yechim (Rust kodi):
```rust
struct Talaba { ism: &'static str, ball: u32 }

fn main() {
    let talabalar = [
        Talaba { ism: "Ali", ball: 85 },
        Talaba { ism: "Vali", ball: 98 },
        Talaba { ism: "Jasur", ball: 74 },
    ];

    let eng_yaxshi = talabalar.iter().max_by_key(|t| t.ball).unwrap();
    println!("Eng yuqori ball: {} ({})", eng_yaxshi.ism, eng_yaxshi.ball);
}
```

## Tushuntirish va Mantiq:
`max_by_key` closure yordamida solishtirish mezonini belgilash imkonini beradi.

## Ishlash natijasi:
```text
Eng yuqori ball: Vali (98)
```

---

# 688-Topshiriq: Iteratorlar orqali HashMap hosil qilish
## Topshiriq sharti:
Kortejlar iteratoridan to'g'ridan-to'g'ri xesh-jadval yasang.

## Yechim (Rust kodi):
```rust
use std::collections::HashMap;

fn main() {
    let kalitlar = ["uz", "ru", "en"];
    let qiymatlar = ["O'zbek", "Rus", "Ingliz"];

    let lugat: HashMap<_, _> = kalitlar.iter().copied().zip(qiymatlar.iter().copied()).collect();

    println!("Hosil bo'lgan lug'at: {:?}", lugat);
}
```

## Tushuntirish va Mantiq:
`zip().collect::<HashMap<_, _>>()` lug'atlarni bir qatorda yig'ishning eng qulay usulidir.

## Ishlash natijasi:
```text
Hosil bo'lgan lug'at: {"en": "Ingliz", "ru": "Rus", "uz": "O'zbek"}
```

---

# 689-Topshiriq: Iterator fuse() adapteri
## Topshiriq sharti:
Bir marta `None` qaytargach doimiy `None` berish kafolati.

## Yechim (Rust kodi):
```rust
fn main() {
    let sonlar = [1, 2];
    let mut iter = sonlar.iter().fuse();

    println!("{:?}", iter.next());
    println!("{:?}", iter.next());
    println!("{:?}", iter.next());
    println!("{:?}", iter.next()); // Doimiy None
}
```

## Tushuntirish va Mantiq:
`fuse()` iterator tugaganidan keyin ham xavfsiz chaqirilishini ta'minlaydi.

## Ishlash natijasi:
```text
Some(1)
Some(2)
None
None
```

---

# 690-Topshiriq: Iteratorlar va Closurelar moduli xulosasi
## Topshiriq sharti:
Funksional dasturlash va yuqori tezlik uyg'unligi.

## Yechim (Rust kodi):
```rust
fn main() {
    println!("=== RUST ITERATORLAR VA CLOSURELAR XULOSASI ===");
    println!("1. Closurelar - tashqi muhitni ushlay oladigan anonim funksiyalar.");
    println!("2. Fn, FnMut, FnOnce - qarzga olish va egaslikka qarab ajratiladi.");
    println!("3. Iteratorlar dangasa (lazy) va nol xarajatli (zero-cost).");
    println!("4. map, filter, fold, zip - kodni toza va ixcham qiladi.");
    println!("5. LLVM optimizatsiyalari tufayli iteratorlar C for tsiklidek maksimal tezlikda ishlaydi.");
}
```

## Tushuntirish va Mantiq:
Rust da funksional dasturlash unumdorlikdan voz kechishni talab qilmaydi: go'zallik va tezlik bitta tilda birlashgan.

## Ishlash natijasi:
```text
=== RUST ITERATORLAR VA CLOSURELAR XULOSASI ===
1. Closurelar - tashqi muhitni ushlay oladigan anonim funksiyalar.
2. Fn, FnMut, FnOnce - qarzga olish va egaslikka qarab ajratiladi.
3. Iteratorlar dangasa (lazy) va nol xarajatli (zero-cost).
4. map, filter, fold, zip - kodni toza va ixcham qiladi.
5. LLVM optimizatsiyalari tufayli iteratorlar C for tsiklidek maksimal tezlikda ishlaydi.
```

---

# 691-Topshiriq: Closure bilan oddiy Memoizatsiya (Keshlovchi closure)
## Topshiriq sharti:
Oldin hisoblangan natijani saqlovchi yordamchi.

## Yechim (Rust kodi):
```rust
struct Keshlovchi<T, F>
where
    F: Fn(T) -> T,
    T: Copy + PartialEq,
{
    hisob: F,
    qiymat: Option<(T, T)>,
}

impl<T, F> Keshlovchi<T, F>
where
    F: Fn(T) -> T,
    T: Copy + PartialEq,
{
    fn new(hisob: F) -> Self { Self { hisob, qiymat: None } }
    fn ol(&mut self, arg: T) -> T {
        if let Some((kirish, chiqish)) = self.qiymat {
            if kirish == arg { return chiqish; }
        }
        let res = (self.hisob)(arg);
        self.qiymat = Some((arg, res));
        res
    }
}

fn main() {
    let mut k = Keshlovchi::new(|x| x * 10);
    println!("1-marta: {}", k.ol(5));
    println!("2-marta (keshdan): {}", k.ol(5));
}
```

## Tushuntirish va Mantiq:
Closure va struktura kombinatsiyasi orqali hisoblangan natijalar keshlanadi.

## Ishlash natijasi:
```text
1-marta: 50
2-marta (keshdan): 50
```

---

# 692-Topshiriq: Iterator flat_map bilan so'zlarni harflarga ajratish
## Topshiriq sharti:
So'zlar ro'yxatidan barcha harflar oqimini oling.

## Yechim (Rust kodi):
```rust
fn main() {
    let sozlar = ["salom", "dunyo"];
    let harflar: Vec<char> = sozlar.iter().flat_map(|s| s.chars()).collect();

    println!("Barcha harflar: {:?}", harflar);
}
```

## Tushuntirish va Mantiq:
`flat_map` har bir so'zdan yangi iterator hosil qilib, ularni bitta tekis oqimga ulaydi.

## Ishlash natijasi:
```text
Barcha harflar: ['s', 'a', 'l', 'o', 'm', 'd', 'u', 'n', 'y', 'o']
```

---

# 693-Topshiriq: Iterator take_while va skip_while
## Topshiriq sharti:
Musbat sonlar tugaguncha olish.

## Yechim (Rust kodi):
```rust
fn main() {
    let sonlar = [5, 4, 3, -1, 2, 1];
    let musbatlar: Vec<_> = sonlar.iter().take_while(|&&x| x > 0).copied().collect();

    println!("Boshdagi musbatlar: {:?}", musbatlar);
}
```

## Tushuntirish va Mantiq:
`take_while` shart buzilishi bilan to'xtaydi.

## Ishlash natijasi:
```text
Boshdagi musbatlar: [5, 4, 3]
```

---

# 694-Topshiriq: Iterator interleave orqali ikkita ro'yxatni navbatma-navbat olish
## Topshiriq sharti:
Ikkita massivni navbati bilan birlashtirish.

## Yechim (Rust kodi):
```rust
fn main() {
    let a = [1, 3, 5];
    let b = [2, 4, 6];

    let birlashgan: Vec<_> = a.iter().zip(b.iter()).flat_map(|(&x, &y)| [x, y]).collect();
    println!("Navbatli ro'yxat: {:?}", birlashgan);
}
```

## Tushuntirish va Mantiq:
Zip va flat_map orqali elementlar navbatma-navbat joylashtiriladi.

## Ishlash natijasi:
```text
Navbatli ro'yxat: [1, 2, 3, 4, 5, 6]
```

---

# 695-Topshiriq: Iterator fold orqali eng katta sonni topish
## Topshiriq sharti:
Maksimum qiymatni fold orqali aniqlash.

## Yechim (Rust kodi):
```rust
fn main() {
    let sonlar = [15, 82, 34, 99, 12];
    let max = sonlar.iter().fold(i32::MIN, |acc, &x| acc.max(x));

    println!("Maksimum son: {}", max);
}
```

## Tushuntirish va Mantiq:
`fold` bilan har qanday matematik taqqoslashni amalga oshirish mumkin.

## Ishlash natijasi:
```text
Maksimum son: 99
```

---

# 696-Topshiriq: Closure bilan shartli qidiruv yordamchisi
## Topshiriq sharti:
Funksiyaga moslashuvchan filtr berish.

## Yechim (Rust kodi):
```rust
fn filtrla<F>(arr: &[i32], shart: F) -> Vec<i32>
where F: Fn(&i32) -> bool {
    arr.iter().copied().filter(shart).collect()
}

fn main() {
    let sonlar = [1, 2, 3, 4, 5, 6];
    let kattalar = filtrla(&sonlar, |&x| x > 3);
    println!("3 dan kattalar: {:?}", kattalar);
}
```

## Tushuntirish va Mantiq:
Yuqori tartibli funksiyalar kodni qayta ishlatish imkonini beradi.

## Ishlash natijasi:
```text
3 dan kattalar: [4, 5, 6]
```

---

# 697-Topshiriq: Iterator chunks orqali juftliklar yig'indisini hisoblash
## Topshiriq sharti:
Har 2 ta elementni qo'shib yangi ro'yxat hosil qiling.

## Yechim (Rust kodi):
```rust
fn main() {
    let sonlar = [1, 2, 3, 4, 5, 6];
    let yigindilar: Vec<i32> = sonlar.chunks(2).map(|c| c.iter().sum()).collect();

    println!("Juftliklar yig'indisi: {:?}", yigindilar);
}
```

## Tushuntirish va Mantiq:
`chunks` bo'laklari ustida alohida amallar bajariladi.

## Ishlash natijasi:
```text
Juftliklar yig'indisi: [3, 7, 11]
```

---

# 698-Topshiriq: Iterator all bilan massivda nol yo'qligini tekshirish
## Topshiriq sharti:
Xavfsiz bo'lish uchun barcha sonlar nol emasligini aniqlang.

## Yechim (Rust kodi):
```rust
fn main() {
    let sonlar = [1, 5, 8, 12];
    let xavfsizmi = sonlar.iter().all(|&x| x != 0);

    println!("Nol yo'qmi: {}", xavfsizmi);
}
```

## Tushuntirish va Mantiq:
Xavfsizlik tekshiruvlari all orqali oson kechadi.

## Ishlash natijasi:
```text
Nol yo'qmi: true
```

---

# 699-Topshiriq: Iterator orqali so'zlar uzunligi ro'yxatini olish
## Topshiriq sharti:
Har bir so'z necha harfdan iboratligini aniqlang.

## Yechim (Rust kodi):
```rust
fn main() {
    let sozlar = ["Rust", "Tezkor", "Xavfsiz"];
    let uzunliklar: Vec<usize> = sozlar.iter().map(|s| s.len()).collect();

    println!("Uzunliklar: {:?}", uzunliklar);
}
```

## Tushuntirish va Mantiq:
So'zlar uzunliklari xaritasini tezkor shakllantirish.

## Ishlash natijasi:
```text
Uzunliklar: [4, 6, 7]
```

---

# 700-Topshiriq: Funksional pipeline yakuniy xulosasi
## Topshiriq sharti:
Rust da funksional uslub eng toza kod andozasidir.

## Yechim (Rust kodi):
```rust
fn main() {
    println!("Rust iteratorlari va closurelari nafaqat chiroyli, balki maksimal tezkor hamdir!");
}
```

## Tushuntirish va Mantiq:
Rust funksional dasturlashni tizimli tezlik bilan birlashtiradi.

## Ishlash natijasi:
```text
Rust iteratorlari va closurelari nafaqat chiroyli, balki maksimal tezkor hamdir!
```

---
