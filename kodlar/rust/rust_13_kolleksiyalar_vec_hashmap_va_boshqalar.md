# 13-Qism: Standart Kolleksiyalar: Vec, HashMap, HashSet, BTreeMap, VecDeque (601-650)

Ushbu qismda Rust standart kutubxonasining asosiy ma'lumotlar tuzilmalari: Dinamik massivlar (`Vec<T>`), Xesh jadvallari (`HashMap<K, V>`), To'plamlar (`HashSet<T>`), Qat'iy tartiblangan B-daraxt xaritalari (`BTreeMap`, `BTreeSet`), Ikki tomonlama navbatlar (`VecDeque`), Ustuvorlik navbatlari (`BinaryHeap`), Entry API, Chastotalarni hisoblash hamda xotira optimizatsiyasi o'rganiladi.

---

# 601-Topshiriq: Standart kolleksiyalar xaritasi: Vec, HashMap, BTreeMap, HashSet
## Topshiriq sharti:
Rust ning barcha asosiy standart kolleksiyalarini e'lon qilib namoyish eting.

## Yechim (Rust kodi):
```rust
use std::collections::{HashMap, HashSet, BTreeMap, VecDeque, BinaryHeap};

fn main() {
    let _v: Vec<i32> = Vec::new();
    let _hm: HashMap<&str, i32> = HashMap::new();
    let _hs: HashSet<i32> = HashSet::new();
    let _bm: BTreeMap<i32, &str> = BTreeMap::new();
    let _vd: VecDeque<i32> = VecDeque::new();
    let _bh: BinaryHeap<i32> = BinaryHeap::new();

    println!("Rust standart kutubxonasi barcha asosiy ma'lumotlar tuzilmalarini o'z ichiga oladi!");
}
```

## Tushuntirish va Mantiq:
Rust turli ehtiyojlar uchun optimallashtirilgan kolleksiyalarga ega: uzluksiz xotira (`Vec`), O(1) qidiruv (`HashMap`), tartiblangan qidiruv (`BTreeMap`), FIFO navbat (`VecDeque`), Max-Heap (`BinaryHeap`).

## Ishlash natijasi:
```text
Rust standart kutubxonasi barcha asosiy ma'lumotlar tuzilmalarini o'z ichiga oladi!
```

---

# 602-Topshiriq: Vec<T> yaratish usullari: new, vec![] va with_capacity
## Topshiriq sharti:
Vektor hosil qilishning eng qulay usullarini ko'rsating.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut v1 = Vec::new();
    v1.push(1);

    let v2 = vec![10, 20, 30]; // vec! makrosi
    let v3: Vec<i32> = Vec::with_capacity(100);

    println!("v1: {:?}, v2: {:?}, v3 sig'imi: {}", v1, v2, v3.capacity());
}
```

## Tushuntirish va Mantiq:
`vec![]` makrosi elementlarni tezkor ro'yxatlash uchun, `with_capacity` esa xotirani oldindan ajratib tezlikni oshirish uchun ishlatiladi.

## Ishlash natijasi:
```text
v1: [1], v2: [10, 20, 30], v3 sig'imi: 100
```

---

# 603-Topshiriq: Vektor xotirasi: len vs capacity va geometrik o'sish
## Topshiriq sharti:
Vektor kengayganda uning sig'imi qanday oshishini kuzating.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut v = Vec::new();
    println!("Boshida: len={}, cap={}", v.len(), v.capacity());

    for i in 1..=5 {
        v.push(i);
        println!("i={}: len={}, cap={}", i, v.len(), v.capacity());
    }
}
```

## Tushuntirish va Mantiq:
Vektor sig'imi yetmaganda, u xotirani 2 barobarga kengaytiradi (0 -> 4 -> 8). Bu o'rtacha (amortized) qo'shish vaqtini O(1) qiladi.

## Ishlash natijasi:
```text
Boshida: len=0, cap=0
i=1: len=1, cap=4
i=2: len=2, cap=4
i=3: len=3, cap=4
i=4: len=4, cap=4
i=5: len=5, cap=8
```

---

# 604-Topshiriq: Vektor metodlari: push, pop, insert, remove
## Topshiriq sharti:
Vektor elementlarini boshqaruvchi asosiy operatsiyalar.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut v = vec![10, 20, 30];
    v.push(40);
    println!("Push 40: {:?}", v);

    let oxirgi = v.pop();
    println!("Pop: {:?}, qoldi: {:?}", oxirgi, v);

    v.insert(1, 15); // 1-indeksga 15 qo'shish
    println!("Insert 15: {:?}", v);

    let ochirilgan = v.remove(2); // 20 o'chiriladi
    println!("Remove 20: {:?}, qoldi: {:?}", ochirilgan, v);
}
```

## Tushuntirish va Mantiq:
`push` va `pop` O(1) da ishlaydi, `insert` va `remove` esa elementlarni surishi kerak bo'lgani sababli O(N) vaqt oladi.

## Ishlash natijasi:
```text
Push 40: [10, 20, 30, 40]
Pop: Some(40), qoldi: [10, 20, 30]
Insert 15: [10, 15, 20, 30]
Remove 20: 20, qoldi: [10, 15, 30]
```

---

# 605-Topshiriq: Vektorni qisqartirish: retain metodi
## Topshiriq sharti:
Shartga mos kelmaydigan elementlarni bitta buyruq bilan tozalang.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut sonlar = vec![1, 2, 3, 4, 5, 6, 7, 8];

    // Faqat juft sonlarni saqlaymiz:
    sonlar.retain(|&x| x % 2 == 0);

    println!("Juft sonlar: {:?}", sonlar);
}
```

## Tushuntirish va Mantiq:
`retain` closure sharti `true` bo'lgan elementlarni joyida (in-place) qoldiradi va qolganlarini xotiradan tozalaydi.

## Ishlash natijasi:
```text
Juft sonlar: [2, 4, 6, 8]
```

---

# 606-Topshiriq: shrink_to_fit orqali ortiqcha xotirani bo'shatish
## Topshiriq sharti:
Vektor sig'imini uning haqiqiy uzunligiga tenglashtirib, operatsion tizimga qaytaring.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut v = Vec::with_capacity(100);
    v.extend([1, 2, 3]);

    println!("Oldin: len={}, cap={}", v.len(), v.capacity());
    v.shrink_to_fit();
    println!("Keyin: len={}, cap={}", v.len(), v.capacity());
}
```

## Tushuntirish va Mantiq:
`shrink_to_fit` xotirani tejash uchun foydalaniladi, ortiqcha zaxira xotira bekor qilinadi.

## Ishlash natijasi:
```text
Oldin: len=3, cap=100
Keyin: len=3, cap=3
```

---

# 607-Topshiriq: HashMap<K, V> yaratish va ma'lumot joylash (insert)
## Topshiriq sharti:
Lug'at (assotsiativ massiv) yaratib elementlar kiriting.

## Yechim (Rust kodi):
```rust
use std::collections::HashMap;

fn main() {
    let mut narxlar = HashMap::new();
    narxlar.insert("Olma", 12000);
    narxlar.insert("Nok", 25000);
    narxlar.insert("Uzum", 18000);

    println!("Lug'atdagi mevalar soni: {}", narxlar.len());
}
```

## Tushuntirish va Mantiq:
`HashMap<K, V>` kalit-qiymat juftliklarini o'rtacha O(1) qidiruv tezligida saqlaydi.

## Ishlash natijasi:
```text
Lug'atdagi mevalar soni: 3
```

---

# 608-Topshiriq: HashMap::get() orqali xavfsiz qiymat olish (Option<&V>)
## Topshiriq sharti:
Mavjud va mavjud bo'lmagan kalitlarni tekshiring.

## Yechim (Rust kodi):
```rust
use std::collections::HashMap;

fn main() {
    let mut ballar = HashMap::new();
    ballar.insert("Rust", 100);

    match ballar.get("Rust") {
        Some(&ball) => println!("Rust bali: {}", ball),
        None => println!("Topilmadi!"),
    }

    match ballar.get("Python") {
        Some(&ball) => println!("Python bali: {}", ball),
        None => println!("Python topilmadi!"),
    }
}
```

## Tushuntirish va Mantiq:
`get(&key)` metodi `Option<&V>` qaytaradi va kalit bo'lmasa dasturni crash bo'lishdan to'liq asraydi.

## Ishlash natijasi:
```text
Rust bali: 100
Python topilmadi!
```

---

# 609-Topshiriq: HashMap Entry API: entry().or_insert() (Chastota sanagich)
## Topshiriq sharti:
Matndagi har bir so'z necha marta qatnashganini Entry API bilan hisoblang.

## Yechim (Rust kodi):
```rust
use std::collections::HashMap;

fn main() {
    let matn = "rust go rust python rust go";
    let mut hisob = HashMap::new();

    for soz in matn.split_whitespace() {
        let sanagich = hisob.entry(soz).or_insert(0);
        *sanagich += 1;
    }

    println!("So'zlar soni: {:?}", hisob);
}
```

## Tushuntirish va Mantiq:
`entry(k).or_insert(v)` agar kalit bo'lmasa `v` ni qo'yadi va mavjud qiymatga `&mut V` havola qaytaradi. Bu Rust dagi eng go'zal idiomalardan biridir.

## Ishlash natijasi:
```text
So'zlar soni: {"go": 2, "python": 1, "rust": 3}
```

---

# 610-Topshiriq: HashMap keys() va values() bo'yicha iteratsiya
## Topshiriq sharti:
Lug'atning barcha kalitlari va qiymatlarini alohida o'qing.

## Yechim (Rust kodi):
```rust
use std::collections::HashMap;

fn main() {
    let mut xodimlar = HashMap::new();
    xodimlar.insert("Ali", 30);
    xodimlar.insert("Vali", 25);

    print!("Ismlar: ");
    for ism in xodimlar.keys() { print!("{} ", ism); }
    println!();

    print!("Yoshlar: ");
    for yosh in xodimlar.values() { print!("{} ", yosh); }
    println!();
}
```

## Tushuntirish va Mantiq:
`keys()` va `values()` iteratorlari xotirani nusxalamasdan kalitlar va qiymatlarni taqdim etadi.

## Ishlash natijasi:
```text
Ismlar: Ali Vali 
Yoshlar: 30 25 
```

---

# 611-Topshiriq: HashSet<T>: Unikal elementlar to'plami
## Topshiriq sharti:
Takrorlanuvchi elementlardan dublikatlarni yo'qotuvchi to'plam yarating.

## Yechim (Rust kodi):
```rust
use std::collections::HashSet;

fn main() {
    let mut raqamlar = HashSet::new();
    raqamlar.insert(10);
    raqamlar.insert(20);
    raqamlar.insert(10); // Qayta qo'shilmaydi

    println!("To'plamdagi unikal elementlar: {:?}", raqamlar);
    println!("20 mavjudmi: {}", raqamlar.contains(&20));
}
```

## Tushuntirish va Mantiq:
`HashSet<T>` faqat unikal elementlarni saqlaydi va `contains()` orqali O(1) da tekshirish imkonini beradi.

## Ishlash natijasi:
```text
To'plamdagi unikal elementlar: {10, 20}
20 mavjudmi: true
```

---

# 612-Topshiriq: HashSet to'plam amallari: Birlashma (union)
## Topshiriq sharti:
Ikkita to'plamni birlashtiring.

## Yechim (Rust kodi):
```rust
use std::collections::HashSet;

fn main() {
    let guruh1: HashSet<_> = [1, 2, 3].iter().cloned().collect();
    let guruh2: HashSet<_> = [3, 4, 5].iter().cloned().collect();

    let birlashma: HashSet<_> = guruh1.union(&guruh2).cloned().collect();
    println!("Birlashma: {:?}", birlashma);
}
```

## Tushuntirish va Mantiq:
`union()` ikkala to'plamning barcha elementlarini dublikatlarsiz birlashtiradi.

## Ishlash natijasi:
```text
Birlashma: {1, 2, 3, 4, 5}
```

---

# 613-Topshiriq: HashSet to'plam amallari: Kesishma (intersection)
## Topshiriq sharti:
Ikkala to'plamda ham mavjud bo'lgan umumiy elementlarni toping.

## Yechim (Rust kodi):
```rust
use std::collections::HashSet;

fn main() {
    let fan1: HashSet<_> = ["Ali", "Vali", "Gani"].iter().cloned().collect();
    let fan2: HashSet<_> = ["Vali", "Gani", "Sardor"].iter().cloned().collect();

    let ikkala_fanda: Vec<_> = fan1.intersection(&fan2).cloned().collect();
    println!("Ikkala fanda qatnashuvchilar: {:?}", ikkala_fanda);
}
```

## Tushuntirish va Mantiq:
`intersection()` umumiy elementlarni ajratib oladi.

## Ishlash natijasi:
```text
Ikkala fanda qatnashuvchilar: ["Gani", "Vali"]
```

---

# 614-Topshiriq: HashSet to'plam amallari: Farq (difference)
## Topshiriq sharti:
Birinchi to'plamda bor, lekin ikkinchisida yo'q elementlarni toping.

## Yechim (Rust kodi):
```rust
use std::collections::HashSet;

fn main() {
    let hamma: HashSet<_> = [1, 2, 3, 4, 5].iter().cloned().collect();
    let topshirganlar: HashSet<_> = [2, 4].iter().cloned().collect();

    let qarzdorlar: Vec<_> = hamma.difference(&topshirganlar).cloned().collect();
    println!("Qarzdorlar: {:?}", qarzdorlar);
}
```

## Tushuntirish va Mantiq:
`difference(&b)` to'plamlar ayirmasini hisoblaydi.

## Ishlash natijasi:
```text
Qarzdorlar: [1, 3, 5]
```

---

# 615-Topshiriq: BTreeMap<K, V>: Doimiy saralangan lug'at
## Topshiriq sharti:
Kalitlari har doim o'sish tartibida saqlanuvchi xarita tuzing.

## Yechim (Rust kodi):
```rust
use std::collections::BTreeMap;

fn main() {
    let mut saralangan = BTreeMap::new();
    saralangan.insert(1991, "Mustaqillik");
    saralangan.insert(2024, "Kelajak");
    saralangan.insert(1441, "Navoiy tavalludi");

    for (yil, voqea) in &saralangan {
        println!("{}-yil: {}", yil, voqea);
    }
}
```

## Tushuntirish va Mantiq:
`BTreeMap` elementlarni B-daraxt tuzilmasida saqlaydi va kalitlar har doim saralangan bo'ladi.

## Ishlash natijasi:
```text
1441-yil: Navoiy tavalludi
1991-yil: Mustaqillik
2024-yil: Kelajak
```

---

# 616-Topshiriq: BTreeMap::range() metodi orqali oraliq qidiruvi
## Topshiriq sharti:
Berilgan yillar oralig'idagi voqealarni toping.

## Yechim (Rust kodi):
```rust
use std::collections::BTreeMap;

fn main() {
    let mut narxlar = BTreeMap::new();
    narxlar.insert(10, "Arzon");
    narxlar.insert(25, "O'rtacha");
    narxlar.insert(50, "Qimmat");
    narxlar.insert(100, "Premium");

    println!("20 dan 60 gacha oraliq:");
    for (narx, nom) in narxlar.range(20..=60) {
        println!("${}: {}", narx, nom);
    }
}
```

## Tushuntirish va Mantiq:
B-daraxt oraliq so'rovlarini (range queries) O(log N) da bajarish imkoniyatiga ega.

## Ishlash natijasi:
```text
20 dan 60 gacha oraliq:
$25: O'rtacha
$50: Qimmat
```

---

# 617-Topshiriq: BTreeSet<T>: Saralangan unikal to'plam
## Topshiriq sharti:
Har doim o'sish tartibida turuvchi unikal sonlar to'plami.

## Yechim (Rust kodi):
```rust
use std::collections::BTreeSet;

fn main() {
    let mut sonlar = BTreeSet::new();
    sonlar.insert(42);
    sonlar.insert(7);
    sonlar.insert(99);
    sonlar.insert(7);

    println!("Saralangan to'plam: {:?}", sonlar);
}
```

## Tushuntirish va Mantiq:
`BTreeSet` avtomatik saralanishi tufayli tartiblangan ro'yxatlarni dublikatlarsiz saqlashda juda qulay.

## Ishlash natijasi:
```text
Saralangan to'plam: {7, 42, 99}
```

---

# 618-Topshiriq: VecDeque<T>: Ikki tomonlama navbat (Ring Buffer)
## Topshiriq sharti:
Boshidan va oxiridan O(1) da element qo'shish va sug'urish.

## Yechim (Rust kodi):
```rust
use std::collections::VecDeque;

fn main() {
    let mut navbat = VecDeque::new();
    navbat.push_back(10);
    navbat.push_front(5);
    navbat.push_back(20);

    println!("Navbat: {:?}", navbat);
    println!("Oldidan sug'urildi: {:?}", navbat.pop_front());
    println!("Orqasidan sug'urildi: {:?}", navbat.pop_back());
    println!("Qoldi: {:?}", navbat);
}
```

## Tushuntirish va Mantiq:
`VecDeque` aylanma bufer (Ring Buffer) asosida qurilgan bo'lib, ikkala tomondan ham maksimal tezlikda qo'shish/olish imkonini beradi.

## Ishlash natijasi:
```text
Navbat: [5, 10, 20]
Oldidan sug'urildi: Some(5)
Orqasidan sug'urildi: Some(20)
Qoldi: [10]
```

---

# 619-Topshiriq: BinaryHeap<T>: Ustuvorlik navbati (Priority Queue / Max-Heap)
## Topshiriq sharti:
Har doim eng katta elementni birinchi bo'lib chiqaruvchi Max-Heap.

## Yechim (Rust kodi):
```rust
use std::collections::BinaryHeap;

fn main() {
    let mut heap = BinaryHeap::new();
    heap.push(15);
    heap.push(42);
    heap.push(8);
    heap.push(99);

    println!("Eng katta element (peek): {:?}", heap.peek());

    print!("Kattalik tartibida olinishi: ");
    while let Some(katta) = heap.pop() {
        print!("{} ", katta);
    }
    println!();
}
```

## Tushuntirish va Mantiq:
`BinaryHeap` har doim eng katta elementni O(log N) da taqdim etuvchi daraxt tuzilmasidir.

## Ishlash natijasi:
```text
Eng katta element (peek): Some(99)
Kattalik tartibida olinishi: 99 42 15 8 
```

---

# 620-Topshiriq: BinaryHeap ni Min-Heap qilish (std::cmp::Reverse)
## Topshiriq sharti:
Eng kichik element birinchi chiqadigan navbat yasang.

## Yechim (Rust kodi):
```rust
use std::collections::BinaryHeap;
use std::cmp::Reverse;

fn main() {
    let mut min_heap = BinaryHeap::new();
    min_heap.push(Reverse(30));
    min_heap.push(Reverse(10));
    min_heap.push(Reverse(50));

    print!("Kichiklik tartibida olinishi: ");
    while let Some(Reverse(kichik)) = min_heap.pop() {
        print!("{} ", kichik);
    }
    println!();
}
```

## Tushuntirish va Mantiq:
`Reverse(x)` solishtirish tartibini teskari qiladi va `BinaryHeap` ni Min-Heap ga aylantiradi.

## Ishlash natijasi:
```text
Kichiklik tartibida olinishi: 10 30 50 
```

---

# 621-Topshiriq: Vektor elementlarini dedup() orqali qo'shnilardan tozalash
## Topshiriq sharti:
Ketma-ket kelgan takroriy elementlarni olib tashlang.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut sonlar = vec![1, 1, 2, 3, 3, 3, 2, 2];
    sonlar.dedup();

    println!("Dedup natijasi: {:?}", sonlar);
}
```

## Tushuntirish va Mantiq:
`dedup` yonma-yon turgan bir xil elementlarni bitta qilib qisqartiradi.

## Ishlash natijasi:
```text
Dedup natijasi: [1, 2, 3, 2]
```

---

# 622-Topshiriq: Ikkita vektorni birlashtirish: extend va append
## Topshiriq sharti:
Bir vektorga ikkinchisini to'liq qo'shish.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut a = vec![1, 2];
    let mut b = vec![3, 4];

    a.append(&mut b); // b bo'shab qoladi, xotirasi a ga ulanadi

    println!("Birlashgan a: {:?}", a);
    println!("b qoldig'i: {:?}", b);
}
```

## Tushuntirish va Mantiq:
`append` ikkinchi vektorni Move qilib, uning xotira buferini birinchi vektorga tezkor ulaydi.

## Ishlash natijasi:
```text
Birlashgan a: [1, 2, 3, 4]
b qoldig'i: []
```

---

# 623-Topshiriq: Vektorlarni bo'laklarga ajratish: chunks va chunks_exact
## Topshiriq sharti:
Massivni N tadan bo'laklarga bo'lib iteratsiya qilish.

## Yechim (Rust kodi):
```rust
fn main() {
    let malumot = [1, 2, 3, 4, 5, 6, 7];

    println!("2 tadan bo'laklar:");
    for chunk in malumot.chunks(2) {
        println!("{:?}", chunk);
    }
}
```

## Tushuntirish va Mantiq:
`chunks(N)` to'plamni N tadan bo'laklarga ajratuvchi qulay iterator beradi.

## Ishlash natijasi:
```text
2 tadan bo'laklar:
[1, 2]
[3, 4]
[5, 6]
[7]
```

---

# 624-Topshiriq: Custom struct ni HashMap kaliti qilish (Hash + Eq)
## Topshiriq sharti:
O'z strukturangizni xesh-jadval kaliti sifatida ishlating.

## Yechim (Rust kodi):
```rust
use std::collections::HashMap;

#[derive(Hash, PartialEq, Eq, Debug)]
struct Koordinata { x: i32, y: i32 }

fn main() {
    let mut xarita = HashMap::new();
    xarita.insert(Koordinata { x: 0, y: 0 }, "Markaz");
    xarita.insert(Koordinata { x: 10, y: 20 }, "Baza");

    println!("(10, 20) manzili: {:?}", xarita.get(&Koordinata { x: 10, y: 20 }));
}
```

## Tushuntirish va Mantiq:
Strukturani HashMap kaliti qilish uchun unga `#[derive(Hash, PartialEq, Eq)]` atributlarini berish kifoyadir.

## Ishlash natijasi:
```text
(10, 20) manzili: Some("Baza")
```

---

# 625-Topshiriq: Graf modelini qo'shnilik ro'yxati (Adjacency List) bilan qurish
## Topshiriq sharti:
`HashMap<u32, Vec<u32>>` orqali yo'naltirilgan graf ifodalash.

## Yechim (Rust kodi):
```rust
use std::collections::HashMap;

struct Graf {
    qoshnilar: HashMap<u32, Vec<u32>>,
}

impl Graf {
    fn new() -> Self { Self { qoshnilar: HashMap::new() } }
    fn qirra_qosh(&mut self, dan: u32, ga: u32) {
        self.qoshnilar.entry(dan).or_default().push(ga);
    }
}

fn main() {
    let mut g = Graf::new();
    g.qirra_qosh(1, 2);
    g.qirra_qosh(1, 3);
    g.qirra_qosh(2, 4);

    println!("1-tugun qo'shnilari: {:?}", g.qoshnilar.get(&1));
}
```

## Tushuntirish va Mantiq:
Graf ma'lumot tuzilmalari xesh-jadvallar va vektorlar yordamida juda samarali saqlanadi.

## Ishlash natijasi:
```text
1-tugun qo'shnilari: Some([2, 3])
```

---

# 626-Topshiriq: Anagramma guruhlarini aniqlash (HashMap va saralash)
## Topshiriq sharti:
Bir xil harflardan tashkil topgan so'zlarni bitta guruhga yig'ing.

## Yechim (Rust kodi):
```rust
use std::collections::HashMap;

fn main() {
    let sozlar = ["kiyik", "kulgi", "ikki", "yikik"];
    let mut guruhlar: HashMap<String, Vec<&str>> = HashMap::new();

    for soz in sozlar {
        let mut harflar: Vec<char> = soz.chars().collect();
        harflar.sort();
        let kalit: String = harflar.into_iter().collect();

        guruhlar.entry(kalit).or_default().push(soz);
    }

    println!("Guruhlangan anagrammalar: {:?}", guruhlar);
}
```

## Tushuntirish va Mantiq:
Harflari saralangan so'z kalit qilib olinsa, barcha anagrammalar bitta ro'yxatga jamlanadi.

## Ishlash natijasi:
```text
Guruhlangan anagrammalar: {"giklu": ["kulgi"], "ikki": ["ikki"], "ikkiy": ["kiyik", "yikik"]}
```

---

# 627-Topshiriq: Top-K eng katta elementlarni BinaryHeap orqali topish
## Topshiriq sharti:
Katta massivdan eng katta 3 ta sonni tezkor ajratib oling.

## Yechim (Rust kodi):
```rust
use std::collections::BinaryHeap;

fn top_k(sonlar: &[i32], k: usize) -> Vec<i32> {
    let mut heap: BinaryHeap<i32> = sonlar.iter().copied().collect();
    let mut natija = Vec::new();
    for _ in 0..k {
        if let Some(katta) = heap.pop() {
            natija.push(katta);
        }
    }
    natija
}

fn main() {
    let sonlar = [4, 1, 7, 3, 8, 5];
    println!("Top 3 katta: {:?}", top_k(&sonlar, 3));
}
```

## Tushuntirish va Mantiq:
`BinaryHeap` O(N log N) o'rniga O(N + K log N) da Top-K elementlarni topish imkonini beradi.

## Ishlash natijasi:
```text
Top 3 katta: [8, 7, 5]
```

---

# 628-Topshiriq: HashMap ni teskari qilish (Invert Map: V -> K)
## Topshiriq sharti:
Lug'atdagi kalit va qiymatlarning o'rnini almashtiring.

## Yechim (Rust kodi):
```rust
use std::collections::HashMap;

fn main() {
    let mut poytaxtlar = HashMap::new();
    poytaxtlar.insert("Uzbekistan", "Tashkent");
    poytaxtlar.insert("France", "Paris");

    let teskari: HashMap<&str, &str> = poytaxtlar.into_iter().map(|(k, v)| (v, k)).collect();
    println!("Teskari lug'at: {:?}", teskari);
}
```

## Tushuntirish va Mantiq:
Iteratorlar yordamida kalit va qiymatlar o'rni bir harakatda almashtiriladi.

## Ishlash natijasi:
```text
Teskari lug'at: {"Paris": "France", "Tashkent": "Uzbekistan"}
```

---

# 629-Topshiriq: Palindromni VecDeque orqali tekshirish
## Topshiriq sharti:
Ikki chetidan bittalab sug'urib solishtirish.

## Yechim (Rust kodi):
```rust
use std::collections::VecDeque;

fn palindrommi(matn: &str) -> bool {
    let mut navbat: VecDeque<char> = matn.chars().collect();
    while navbat.len() > 1 {
        if navbat.pop_front() != navbat.pop_back() {
            return false;
        }
    }
    true
}

fn main() {
    println!("'radar': {}", palindrommi("radar"));
    println!("'rust':  {}", palindrommi("rust"));
}
```

## Tushuntirish va Mantiq:
`VecDeque` yordamida boshidan va oxiridan O(1) da element olib solishtirish oson kechadi.

## Ishlash natijasi:
```text
'radar': true
'rust':  false
```

---

# 630-Topshiriq: Matn ichidagi harflar sonini HashSet orqali sanash
## Topshiriq sharti:
Matnda necha xil unikal harf qatnashganini aniqlang.

## Yechim (Rust kodi):
```rust
use std::collections::HashSet;

fn unikal_harflar_soni(matn: &str) -> usize {
    matn.chars().filter(|c| !c.is_whitespace()).collect::<HashSet<_>>().len()
}

fn main() {
    println!("Unikal harflar: {}", unikal_harflar_soni("Assalomu alaykum"));
}
```

## Tushuntirish va Mantiq:
`collect::<HashSet<_>>()` takroriy belgilarni avtomatik tozalaydi.

## Ishlash natijasi:
```text
Unikal harflar: 8
```

---

# 631-Topshiriq: Kolleksiyalar moduli xulosasi: To'g'ri tanlov strategiyasi
## Topshiriq sharti:
Har bir ma'lumot tuzilmasidan qachon foydalanish qoidalari.

## Yechim (Rust kodi):
```rust
fn main() {
    println!("=== RUST STANDART KOLLEKSIYALAR XULOSASI ===");
    println!("1. Vec - ketma-ket ma'lumotlar uchun standart tanlov.");
    println!("2. HashMap - tezkor O(1) kalit-qiymat qidiruvi.");
    println!("3. HashSet - unikal elementlar va to'plam amallari.");
    println!("4. BTreeMap / BTreeSet - saralangan kalitlar va oraliq so'rovlari.");
    println!("5. VecDeque - ikkala tomondan tezkor navbatlar.");
    println!("6. BinaryHeap - ustuvorlik navbatlari va eng katta/kichik qiymatlar.");
}
```

## Tushuntirish va Mantiq:
Rust ning standart kolleksiyalari to'liq xotira xavfsizligi va optimal algoritmlar bilan ta'minlangan.

## Ishlash natijasi:
```text
=== RUST STANDART KOLLEKSIYALAR XULOSASI ===
1. Vec - ketma-ket ma'lumotlar uchun standart tanlov.
2. HashMap - tezkor O(1) kalit-qiymat qidiruvi.
3. HashSet - unikal elementlar va to'plam amallari.
4. BTreeMap / BTreeSet - saralangan kalitlar va oraliq so'rovlari.
5. VecDeque - ikkala tomondan tezkor navbatlar.
6. BinaryHeap - ustuvorlik navbatlari va eng katta/kichik qiymatlar.
```

---

# 632-Topshiriq: Telefon kitobchasi modeli: HashMap<String, Vec<String>>
## Topshiriq sharti:
Bitta ism ostida bir nechta telefon raqamlarini saqlash.

## Yechim (Rust kodi):
```rust
use std::collections::HashMap;

fn main() {
    let mut kitobcha: HashMap<String, Vec<String>> = HashMap::new();

    kitobcha.entry(String::from("Ali")).or_default().push(String::from("+998901112233"));
    kitobcha.entry(String::from("Ali")).or_default().push(String::from("+998994445566"));

    println!("Ali raqamlari: {:?}", kitobcha.get("Ali"));
}
```

## Tushuntirish va Mantiq:
Kolleksiyalar ichida boshqa kolleksiyalarni saqlash orqali ko'p qiymatli xaritalar (Multi-map) quriladi.

## Ishlash natijasi:
```text
Ali raqamlari: Some(["+998901112233", "+998994445566"])
```

---

# 633-Topshiriq: Bosh harflar bo'yicha so'zlarni guruhlash (Grouping by letter)
## Topshiriq sharti:
So'zlar ro'yxatini bosh harfiga ko'ra BTreeMap ga jamlang.

## Yechim (Rust kodi):
```rust
use std::collections::BTreeMap;

fn main() {
    let sozlar = ["olma", "anor", "shaftoli", "sholi", "uzum"];
    let mut guruh = BTreeMap::new();

    for soz in sozlar {
        let bosh = soz.chars().next().unwrap();
        guruh.entry(bosh).or_insert(Vec::new()).push(soz);
    }

    println!("Guruhlar: {:?}", guruh);
}
```

## Tushuntirish va Mantiq:
`BTreeMap` tufayli harflar alfavit tartibida chiqadi.

## Ishlash natijasi:
```text
Guruhlar: {'a': ["olma", "anor"], 's': ["shaftoli", "sholi"], 'u': ["uzum"]}
```

---

# 634-Topshiriq: Vektor elementlarini sort_by_key orqali saralash
## Topshiriq sharti:
Strukturalarni ularning maoshi bo'yicha tartiblang.

## Yechim (Rust kodi):
```rust
struct Xodim { ism: String, maosh: u32 }

fn main() {
    let mut xodimlar = vec![
        Xodim { ism: String::from("Ali"), maosh: 3000 },
        Xodim { ism: String::from("Vali"), maosh: 1500 },
    ];

    xodimlar.sort_by_key(|x| x.maosh);
    println!("Eng kam maosh: {} (${})", xodimlar[0].ism, xodimlar[0].maosh);
}
```

## Tushuntirish va Mantiq:
`sort_by_key` closure orqali kerakli maydon bo'yicha tezkor saralashni ta'minlaydi.

## Ishlash natijasi:
```text
Eng kam maosh: Vali ($1500)
```

---

# 635-Topshiriq: Valyutalar kursi lug'ati va konvertatsiya
## Topshiriq sharti:
Valyuta ayirboshlash xaritasi modeli.

## Yechim (Rust kodi):
```rust
use std::collections::HashMap;

fn main() {
    let mut kurslar = HashMap::new();
    kurslar.insert("USD", 12800.0);
    kurslar.insert("EUR", 13900.0);

    let summa_usd = 100.0;
    let summa_som = summa_usd * kurslar.get("USD").unwrap();

    println!("${} = {} so'm", summa_usd, summa_som);
}
```

## Tushuntirish va Mantiq:
Moliyaviy kurslar jadvali xesh-xaritalarda saqlanishi standart amaliyotdir.

## Ishlash natijasi:
```text
$100 = 1280000 so'm
```

---

# 636-Topshiriq: BinaryHeap yordamida Task Scheduler (Vazifalar rejalashtirgich)
## Topshiriq sharti:
Ustuvorlik darajasiga (priority) ega vazifalar ijrosi.

## Yechim (Rust kodi):
```rust
use std::collections::BinaryHeap;

#[derive(Eq, PartialEq, Ord, PartialOrd)]
struct Vazifa {
    ustuvorlik: u8,
    nom: &'static str,
}

fn main() {
    let mut reja = BinaryHeap::new();
    reja.push(Vazifa { ustuvorlik: 1, nom: "Elektron xat yozish" });
    reja.push(Vazifa { ustuvorlik: 10, nom: "Server avariyasini tuzatish" });
    reja.push(Vazifa { ustuvorlik: 5, nom: "Kod tekshiruvi" });

    while let Some(v) = reja.pop() {
        println!("Bajarilmoqda [Ustuvorlik {}]: {}", v.ustuvorlik, v.nom);
    }
}
```

## Tushuntirish va Mantiq:
Eng muhim vazifalar har doim birinchi bo'lib bajariladi.

## Ishlash natijasi:
```text
Bajarilmoqda [Ustuvorlik 10]: Server avariyasini tuzatish
Bajarilmoqda [Ustuvorlik 5]: Kod tekshiruvi
Bajarilmoqda [Ustuvorlik 1]: Elektron xat yozish
```

---

# 637-Topshiriq: Nested Kolleksiyalar: Matritsa Vec<Vec<i32>>
## Topshiriq sharti:
Dinamik o'lchamli 2D matritsa hosil qilish.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut matritsa = vec![
        vec![1, 2],
        vec![3, 4],
    ];
    matritsa[0].push(5);

    println!("Dinamik matritsa: {:?}", matritsa);
}
```

## Tushuntirish va Mantiq:
Dinamik 2D matritsalar har bir satri alohida o'lchamda bo'lishiga ham ruxsat beradi.

## Ishlash natijasi:
```text
Dinamik matritsa: [[1, 2, 5], [3, 4]]
```

---

# 638-Topshiriq: HashMap Entry API: or_insert_with (Lazy baholash)
## Topshiriq sharti:
Faqat kerak bo'lganda qimmat qiymatni hisoblab kiritish.

## Yechim (Rust kodi):
```rust
use std::collections::HashMap;

fn main() {
    let mut kesh = HashMap::new();
    kesh.entry("token").or_insert_with(|| {
        println!("(Yangi token generatsiya qilindi)");
        String::from("ABC-123")
    });

    println!("Token: {:?}", kesh.get("token"));
}
```

## Tushuntirish va Mantiq:
`or_insert_with` closure orqali faqat kalit bo'lmagandagina qimmatbaho kodni ishga tushiradi.

## Ishlash natijasi:
```text
(Yangi token generatsiya qilindi)
Token: Some("ABC-123")
```

---

# 639-Topshiriq: Vektor split_off metodi orqali bo'lish
## Topshiriq sharti:
Vektorni belgilangan indeksdan boshlab yangi vektorga ajratish.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut v1 = vec![1, 2, 3, 4, 5];
    let v2 = v1.split_off(2); // 2-indeksdan boshlab v2 ga o'tadi

    println!("v1: {:?}", v1);
    println!("v2: {:?}", v2);
}
```

## Tushuntirish va Mantiq:
`split_off` bitta vektorni ikkita mustaqil `Vec` ga ajratadi.

## Ishlash natijasi:
```text
v1: [1, 2]
v2: [3, 4, 5]
```

---

# 640-Topshiriq: Vec::drain orqali oraliqni sug'urib olish
## Topshiriq sharti:
Vektor ichidan oraliq elementlarni olib, asl vektorni saqlab qolish.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut v = vec![10, 20, 30, 40, 50];
    let sugurilgan: Vec<_> = v.drain(1..3).collect(); // 20 va 30 sug'uriladi

    println!("Sug'urilgan: {:?}", sugurilgan);
    println!("Qolgan vektor: {:?}", v);
}
```

## Tushuntirish va Mantiq:
`drain(range)` oraliqdagi elementlarni iterator sifatida berib, o'rnini yopadi.

## Ishlash natijasi:
```text
Sug'urilgan: [20, 30]
Qolgan vektor: [10, 40, 50]
```

---

# 641-Topshiriq: SipHash va DoS hujumlaridan himoya
## Topshiriq sharti:
Rust standart HashMap ning kiberxavfsizlik xususiyati.

## Yechim (Rust kodi):
```rust
fn main() {
    println!("Rust standart HashMap i SipHash 1-3 algoritmidan foydalanadi.");
    println!("Bu xesh-to'qnashuvlar (HashDoS attacks) orqali serverlarni ishdan chiqarish xavfini yo'qotadi!");
}
```

## Tushuntirish va Mantiq:
Rust xavfsizlikka alohida urg'u beradi: xesh-jadvallar standart bo'yicha kriptografik mustahkam xeshlovchiga ega.

## Ishlash natijasi:
```text
Rust standart HashMap i SipHash 1-3 algoritmidan foydalanadi.
Bu xesh-to'qnashuvlar (HashDoS attacks) orqali serverlarni ishdan chiqarish xavfini yo'qotadi!
```

---

# 642-Topshiriq: HashSet bilan ro'yxatdan dublikatlarni tozalash
## Topshiriq sharti:
Vektordagi takroriy sonlarni yo'qoting.

## Yechim (Rust kodi):
```rust
use std::collections::HashSet;

fn main() {
    let sonlar = vec![1, 2, 2, 3, 4, 4, 5];
    let unikal: HashSet<i32> = sonlar.into_iter().collect();

    println!("Unikal to'plam: {:?}", unikal);
}
```

## Tushuntirish va Mantiq:
`into_iter().collect::<HashSet<_>>()` eng qisqa dublikat tozalagichdir.

## Ishlash natijasi:
```text
Unikal to'plam: {1, 2, 3, 4, 5}
```

---

# 643-Topshiriq: Vektor swap_remove orqali O(1) da element o'chirish
## Topshiriq sharti:
Tartib muhim bo'lmaganda tezkor o'chirish.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut v = vec!["A", "B", "C", "D"];
    let ochirildi = v.swap_remove(1); // "B" o'rniga oxirgi "D" keladi!

    println!("O'chirildi: {}, Yangi vektor: {:?}", ochirildi, v);
}
```

## Tushuntirish va Mantiq:
`swap_remove` elementlarni surib o'tirmasdan, oxirgisini o'chirilgan joyga qo'yadi va O(1) tezlik beradi.

## Ishlash natijasi:
```text
O'chirildi: B, Yangi vektor: ["A", "D", "C"]
```

---

# 644-Topshiriq: HashMap dagi barcha qiymatlarni o'zgartirish
## Topshiriq sharti:
Har bir mahsulot narxini 10% ga oshiring.

## Yechim (Rust kodi):
```rust
use std::collections::HashMap;

fn main() {
    let mut narxlar = HashMap::new();
    narxlar.insert("Non", 4000);
    narxlar.insert("Sut", 8000);

    for narx in narxlar.values_mut() {
        *narx = (*narx as f64 * 1.1) as i32;
    }

    println!("Yangi narxlar: {:?}", narxlar);
}
```

## Tushuntirish va Mantiq:
`values_mut()` lug'at qiymatlarini o'z joyida o'zgartirish huquqini beradi.

## Ishlash natijasi:
```text
Yangi narxlar: {"Non": 4400, "Sut": 8800}
```

---

# 645-Topshiriq: BTreeSet bilan oraliq filtratsiyasi
## Topshiriq sharti:
Faqat 10 dan 50 gacha bo'lgan sonlarni tanlash.

## Yechim (Rust kodi):
```rust
use std::collections::BTreeSet;

fn main() {
    let to'plam: BTreeSet<i32> = [5, 12, 25, 48, 60, 75].into_iter().collect();
    let oraliq: Vec<&i32> = to'plam.range(10..=50).collect();

    println!("Tanlangan oraliq: {:?}", oraliq);
}
```

## Tushuntirish va Mantiq:
B-daraxt to'plami oraliqlarni saralangan holda beradi.

## Ishlash natijasi:
```text
Tanlangan oraliq: [12, 25, 48]
```

---

# 646-Topshiriq: VecDeque da aylanma siljish (Rotate Left / Rotate Right)
## Topshiriq sharti:
Navbat elementlarini aylantiring.

## Yechim (Rust kodi):
```rust
use std::collections::VecDeque;

fn main() {
    let mut v = VecDeque::from([1, 2, 3, 4]);
    v.rotate_left(1); // 1 boshidan oxiriga o'tadi

    println!("Aylantirilgan: {:?}", v);
}
```

## Tushuntirish va Mantiq:
`rotate_left` va `rotate_right` aylanma siljitishlarni O(1) qo'shimcha xotira bilan bajaradi.

## Ishlash natijasi:
```text
Aylantirilgan: [2, 3, 4, 1]
```

---

# 647-Topshiriq: Vektor sig'imini oldindan zaxiralash: reserve()
## Topshiriq sharti:
Keyingi katta qo'shishlar uchun joy ajrating.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut v = vec![1, 2];
    v.reserve(100);

    println!("Sig'im oshirildi: {}", v.capacity() >= 102);
}
```

## Tushuntirish va Mantiq:
`reserve(n)` vektorga qo'shimcha N ta element uchun joy ajratishni kafolatlaydi.

## Ishlash natijasi:
```text
Sig'im oshirildi: true
```

---

# 648-Topshiriq: HashMap bilan foydalanuvchi ma'lumotlarini qidirish
## Topshiriq sharti:
ID orqali profilni tezkor topish.

## Yechim (Rust kodi):
```rust
use std::collections::HashMap;

fn main() {
    let mut baza = HashMap::new();
    baza.insert(101, "Sardor");
    baza.insert(102, "Nodira");

    println!("ID 102 egasi: {:?}", baza.get(&102));
}
```

## Tushuntirish va Mantiq:
Foydalanuvchi bazalari xesh jadvallar orqali tezkor ishlaydi.

## Ishlash natijasi:
```text
ID 102 egasi: Some("Nodira")
```

---

# 649-Topshiriq: Kolleksiyalarni tozalash: clear()
## Topshiriq sharti:
Barcha elementlarni o'chirish.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut v = vec![1, 2, 3];
    v.clear();

    println!("Bo'shatilgan vektor: {:?}", v);
}
```

## Tushuntirish va Mantiq:
`clear()` elementlarni o'chiradi, lekin xotira sig'imi qayta ishlatish uchun saqlanadi.

## Ishlash natijasi:
```text
Bo'shatilgan vektor: []
```

---

# 650-Topshiriq: Kolleksiyalar moduli yakuniy xulosasi
## Topshiriq sharti:
Zamonaviy dasturlashda ma'lumotlar tuzilmalarining o'rni.

## Yechim (Rust kodi):
```rust
fn main() {
    println!("Rust kolleksiyalari xotirani tejash va maksimal unumdorlik uchun mukammal sozlangan.");
}
```

## Tushuntirish va Mantiq:
Kolleksiyalar algoritmlarning yuragidir.

## Ishlash natijasi:
```text
Rust kolleksiyalari xotirani tejash va maksimal unumdorlik uchun mukammal sozlangan.
```

---
