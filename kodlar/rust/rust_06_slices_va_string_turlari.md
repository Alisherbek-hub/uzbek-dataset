# 6-Qism: Slices (Bo'laklar) va String Turlari (251-300)

Ushbu qismda Rust da matnlar va kolleksiyalar bilan ishlashning eng muhim mavzulari: String Slices (`&str`), dinamik satrlar (`String`), UTF-8 baytlar arxitekturasi, nega Rust da to'g'ridan-to'g'ri indekslash taqiqlangani, massiv bo'laklari (`&[T]`), `format!` makrosi, qidiruv va filtratsiyalar, `Cow` (Clone-on-Write) hamda nol-nusxali (zero-copy) matn tahlili o'rganiladi.

---

# 251-Topshiriq: Slice (Bo'lak) nima? Fat Pointer tuzilishi
## Topshiriq sharti:
Slice ning xotirada qanday saqlanishini (ko'rsatkich + uzunlik) ko'rsating.

## Yechim (Rust kodi):
```rust
fn main() {
    let massiv = [10, 20, 30, 40, 50];
    let bolak: &[i32] = &massiv[1..4]; // 20, 30, 40

    println!("Bo'lak elementlari: {:?}", bolak);
    println!("Bo'lak uzunligi: {}", bolak.len());
    println!("Slice havolasi o'lchami: {} bayt (fat pointer)", std::mem::size_of_val(&bolak));
}
```

## Tushuntirish va Mantiq:
Slice Rust da 'Fat Pointer' deb ataladi: u oddiy 8 bayt emas, balki 16 bayt egallaydi (8 bayt xotira manzili ko'rsatkichi + 8 bayt bo'lak uzunligi).

## Ishlash natijasi:
```text
Bo'lak elementlari: [20, 30, 40]
Bo'lak uzunligi: 3
Slice havolasi o'lchami: 16 bayt (fat pointer)
```

---

# 252-Topshiriq: String Slice (&str) vs Heap String (String)
## Topshiriq sharti:
Statik binar ichidagi `&str` bilan dinamik Heap `String` ning farqini ko'rsating.

## Yechim (Rust kodi):
```rust
fn main() {
    // &str: dastur binar faylida statik saqlanadi yoki boshqa matndan qarzga olinadi
    let statik_matn: &'static str = "Men o'zgarmas &str man";

    // String: Heap xotirasida dinamik ajratiladi va o'sishi mumkin
    let mut dinamik_matn: String = String::from("Men Heap ");
    dinamik_matn.push_str("Stringiman");

    println!("{}", statik_matn);
    println!("{}", dinamik_matn);
}
```

## Tushuntirish va Mantiq:
`&str` faqat ko'rinish (view) bo'lib, o'zi xotirani egalik qilmaydi. `String` esa xotirani o'zi boshqaradi va kengaya oladi.

## Ishlash natijasi:
```text
Men o'zgarmas &str man
Men Heap Stringiman
```

---

# 253-Topshiriq: String strukturasining Stack dagi hajmi (24 bayt)
## Topshiriq sharti:
`String` obyekti Stack da qancha joy egallashini tahlil qiling.

## Yechim (Rust kodi):
```rust
fn main() {
    let s = String::from("Assalomu alaykum, O'zbekiston!");

    println!("String ning Stack dagi hajmi: {} bayt", std::mem::size_of::<String>());
    println!("Matn uzunligi (baytlarda): {}", s.len());
    println!("Xotira sig'imi (capacity): {}", s.capacity());
}
```

## Tushuntirish va Mantiq:
`String` Stack xotirasida har doim aynan 24 bayt joy egallaydi: 8 bayt Heap ko'rsatkichi, 8 bayt joriy uzunlik (len), va 8 bayt umumiy ajratilgan sig'im (capacity).

## Ishlash natijasi:
```text
String ning Stack dagi hajmi: 24 bayt
Matn uzunligi (baytlarda): 32
Xotira sig'imi (capacity): 32
```

---

# 254-Topshiriq: String yaratish: String::new() va with_capacity()
## Topshiriq sharti:
Oldindan sig'im ajratish orqali xotirani qayta taqsimlash (reallocation) xarajatlarini yo'qoting.

## Yechim (Rust kodi):
```rust
fn main() {
    // Sig'imi oldindan belgilangan String yaratamiz:
    let mut s = String::with_capacity(50);
    println!("Boshlang'ich sig'im: {}", s.capacity());

    s.push_str("Tezkor xotira ajratish");
    println!("Matn: '{}', Sig'im o'zgarmadi: {}", s, s.capacity());
}
```

## Tushuntirish va Mantiq:
`with_capacity()` katta matnlar yig'ilganda xotirani bir necha marta qayta-qayta ko'chirishning oldini oladi va ish faoliyatini 3-5 barobar oshiradi.

## Ishlash natijasi:
```text
Boshlang'ich sig'im: 50
Matn: 'Tezkor xotira ajratish', Sig'im o'zgarmadi: 50
```

---

# 255-Topshiriq: String::from() va .to_string() usullari
## Topshiriq sharti:
Satr literalidan `String` yaratishning standart usullarini ko'rsating.

## Yechim (Rust kodi):
```rust
fn main() {
    let s1 = String::from("Rust tili");
    let s2 = "Zamonaviy tizimlar".to_string();

    println!("s1: {}", s1);
    println!("s2: {}", s2);
}
```

## Tushuntirish va Mantiq:
`String::from()` va `.to_string()` bir xil natija beradi. `to_string()` `Display` traiti orqali ishlaydi, `String::from()` esa to'g'ridan-to'g'ri konvertatsiyadir.

## Ishlash natijasi:
```text
s1: Rust tili
s2: Zamonaviy tizimlar
```

---

# 256-Topshiriq: .to_owned() metodi orqali &str dan String yaratish
## Topshiriq sharti:
Borrow qilingan ma'lumotdan to'liq egali `String` olish.

## Yechim (Rust kodi):
```rust
fn main() {
    let matn_slice: &str = "O'zbekiston";
    let yangi_string: String = matn_slice.to_owned();

    println!("Yangi egalikdagi String: {}", yangi_string);
}
```

## Tushuntirish va Mantiq:
`.to_owned()` metodi `ToOwned` traitiga tayanib, qarzga olingan har qanday ma'lumotdan uning mustaqil egali nusxasini yaratadi.

## Ishlash natijasi:
```text
Yangi egalikdagi String: O'zbekiston
```

---

# 257-Topshiriq: String ga bitta belgi qo'shish: .push(char)
## Topshiriq sharti:
Satr oxiriga bitta `char` belgisini qo'shing.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut s = String::from("Salom");
    s.push('!');
    s.push(' ');
    s.push('🚀');

    println!("{}", s);
}
```

## Tushuntirish va Mantiq:
`.push()` bitta Unicode `char` belgisini qabul qiladi va uning UTF-8 baytlarini satr oxiriga ulaydi.

## Ishlash natijasi:
```text
Salom! 🚀
```

---

# 258-Topshiriq: String ga matn qo'shish: .push_str(&str)
## Topshiriq sharti:
Satr oxiriga butun boshli satr bo'lagini ulang.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut xabar = String::from("Rust");
    xabar.push_str(" dasturlash tili");

    println!("{}", xabar);
}
```

## Tushuntirish va Mantiq:
`.push_str()` parametr sifatida `&str` qabul qiladi va asl xotirani kengaytirib, yangi so'zlarni ulaydi.

## Ishlash natijasi:
```text
Rust dasturlash tili
```

---

# 259-Topshiriq: String dan oxirgi belgini sug'urib olish: .pop()
## Topshiriq sharti:
Satr oxiridan bittalab belgilarni o'chirish va ularni `Option<char>` sifatida olish.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut matn = String::from("Rust!");

    let oxirgi = matn.pop();
    println!("O'chirilgan belgi: {:?}", oxirgi);
    println!("Qolgan matn: {}", matn);
}
```

## Tushuntirish va Mantiq:
`.pop()` satrning oxirgi Unicode belgisini xavfsiz sug'urib oladi va satr uzunligini mos ravishda qisqartiradi.

## Ishlash natijasi:
```text
O'chirilgan belgi: Some('!')
Qolgan matn: Rust
```

---

# 260-Topshiriq: String o'rtasiga belgi yoki matn kiritish: insert va insert_str
## Topshiriq sharti:
Belgilangan bayt indeksiga yangi so'z joylashtiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut matn = String::from("Assalom dunyo");
    matn.insert_str(7, "go'zal "); // 7-bayt indeksiga joylashtirish

    println!("{}", matn);
}
```

## Tushuntirish va Mantiq:
`insert_str(index, string)` berilgan indeksdagi qolgan belgilarni o'ng tomonga surib, o'rtaga yangi matnni joylashtiradi.

## Ishlash natijasi:
```text
Assalom go'zal dunyo
```

---

# 261-Topshiriq: String ni tozalash: clear() va uning xotiraga ta'siri
## Topshiriq sharti:
Satrni bo'shating, ammo uning ajratilgan xotira sig'imini saqlab qoling.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut s = String::from("Katta matn ma'lumoti");
    println!("Tozalashdan oldin: len={}, cap={}", s.len(), s.capacity());

    s.clear();
    println!("Tozalashdan so'ng: len={}, cap={}", s.len(), s.capacity());
}
```

## Tushuntirish va Mantiq:
`.clear()` satr uzunligini 0 qiladi, biroq avval ajratilgan Heap buferini bo'shatmaydi. Bu keyingi yozishlarda qayta xotira ajratmasdan tez ishlashni ta'minlaydi.

## Ishlash natijasi:
```text
Tozalashdan oldin: len=22, cap=22
Tozalashdan so'ng: len=0, cap=22
```

---

# 262-Topshiriq: Nega Rust da s[0] deb satrni indekslash taqiqlangan?
## Topshiriq sharti:
Rust satrlarni UTF-8 baytlar sifatida saqlashi va indekslash nega xavfli ekanligini ko'rsating.

## Yechim (Rust kodi):
```rust
fn main() {
    let salom = "Salom"; // Har bir lotin harfi 1 bayt
    let ruscha = "Привет"; // Har bir kirill harfi 2 bayt!

    println!("'{}' uzunligi baytlarda: {}", salom, salom.len());
    println!("'{}' uzunligi baytlarda: {}", ruscha, ruscha.len());
    // ruscha[0] ruxsat berilsa, 2 baytli harfning yarim bayti olinib, xato belgi hosil bo'lardi!
}
```

## Tushuntirish va Mantiq:
Rust da barcha `String` va `&str` lar qat'iy UTF-8 dir. Belgilar 1 dan 4 baytgacha bo'lgani sababli, indekslash O(1) vaqtda kafolatlanmaydi va harflarni parchalab yuborishi mumkin.

## Ishlash natijasi:
```text
'Salom' uzunligi baytlarda: 5
'Привет' uzunligi baytlarda: 12
```

---

# 263-Topshiriq: Satr baytlarini aylanib chiqish: .bytes()
## Topshiriq sharti:
Matnni tashkil etgan har bir xom bayt qiymatini chop eting.

## Yechim (Rust kodi):
```rust
fn main() {
    let matn = "Rust";

    print!("Baytlar: ");
    for b in matn.bytes() {
        print!("{} ", b);
    }
    println!();
}
```

## Tushuntirish va Mantiq:
`.bytes()` matnning har bir baytini `u8` soni ko'rinishida beruvchi iterator qaytaradi.

## Ishlash natijasi:
```text
Baytlar: 82 117 115 116 
```

---

# 264-Topshiriq: Satr belgilarini aylanib chiqish: .chars()
## Topshiriq sharti:
Harfma-harf to'liq Unicode belgilarini ajratib oling.

## Yechim (Rust kodi):
```rust
fn main() {
    let matn = "O'zbekiston 🇺🇿";

    print!("Belgilar: ");
    for c in matn.chars() {
        print!("[{}] ", c);
    }
    println!();
}
```

## Tushuntirish va Mantiq:
`.chars()` metodi UTF-8 baytlarini birlashtirib, har bir to'liq 4-baytli Unicode `char` skalar qiymatini hosil qiladi.

## Ishlash natijasi:
```text
Belgilar: [O] ['] [z] [b] [e] [k] [i] [s] [t] [o] [n] [ ] [🇺] [🇿] 
```

---

# 265-Topshiriq: Satrdan xavfsiz slice olish va is_char_boundary tekshiruvi
## Topshiriq sharti:
Matndan bo'lak olayotganda harf o'rtasidan bo'lib yubormaslikni tekshiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let matn = "Qo'shiq";
    let indeks = 2;

    if matn.is_char_boundary(indeks) {
        println!("Xavfsiz bo'lak: '{}'", &matn[0..indeks]);
    } else {
        println!("Xatolik: Indeks harf o'rtasiga to'g'ri keldi!");
    }
}
```

## Tushuntirish va Mantiq:
`.is_char_boundary(i)` metodi berilgan indeks UTF-8 belgisining boshlanish nuqtasimi yoki yo'qligini tekshiradi.

## Ishlash natijasi:
```text
Xavfsiz bo'lak: 'Qo'
```

---

# 266-Topshiriq: Bo'shliqlarni tozalash: trim(), trim_start(), trim_end()
## Topshiriq sharti:
Matn atrofidagi probellar va yangi qator belgilarini tozalang.

## Yechim (Rust kodi):
```rust
fn main() {
    let xom = "   \n  Salom Rust Dunyosi!   \t  ";

    println!("To'liq tozalangan:  '{}'", xom.trim());
    println!("Faqat boshidan:     '{}'", xom.trim_start());
    println!("Faqat oxiridan:     '{}'", xom.trim_end());
}
```

## Tushuntirish va Mantiq:
`trim()` yangi xotira ajratmaydi! U faqat boshlang'ich va oxirgi probellarni chetlab o'tuvchi yangi `&str` bo'lagini qaytaradi.

## Ishlash natijasi:
```text
To'liq tozalangan:  'Salom Rust Dunyosi!'
Faqat boshidan:     'Salom Rust Dunyosi!   \t  '
Faqat oxiridan:     '   \n  Salom Rust Dunyosi!'
```

---

# 267-Topshiriq: Maxsus belgilarni tozalash: trim_matches()
## Topshiriq sharti:
Matn ikki chetidan faqat ma'lum belgilarni (masalan vergul yoki qavslarni) o'chiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let matn = "///Tizim Log Fayli///";
    let toza = matn.trim_matches('/');

    println!("Tozalangan: {}", toza);
}
```

## Tushuntirish va Mantiq:
`trim_matches(pattern)` berilgan belgi yoki shartga mos keluvchi chekka belgilarni qirqib tashlaydi.

## Ishlash natijasi:
```text
Tozalangan: Tizim Log Fayli
```

---

# 268-Topshiriq: Matnni ajratish: split() iteratori
## Topshiriq sharti:
Vergul bilan ajratilgan ma'lumotlarni qismlarga bo'ling.

## Yechim (Rust kodi):
```rust
fn main() {
    let mevalar = "Olma,Anor,Uzum,Shaftoli";

    for meva in mevalar.split(',') {
        println!("Meva: {}", meva);
    }
}
```

## Tushuntirish va Mantiq:
`split()` ajratgich bo'yicha matnni bo'laklarga (`&str`) ajratadi va yangi satr yaratmasdan nol nusxa bilan ishlaydi.

## Ishlash natijasi:
```text
Meva: Olma
Meva: Anor
Meva: Uzum
Meva: Shaftoli
```

---

# 269-Topshiriq: Qatorlar bo'yicha ajratish: lines()
## Topshiriq sharti:
Ko'p qatorli matnni qatorlarga ajratib, ularning tartib raqamini chiqaring.

## Yechim (Rust kodi):
```rust
fn main() {
    let hujjat = "1-qator: Kirish\n2-qator: Asosiy qism\n3-qator: Xulosa";

    for (raqam, qator) in hujjat.lines().enumerate() {
        println!("{}: {}", raqam + 1, qator);
    }
}
```

## Tushuntirish va Mantiq:
`.lines()` usuli ham `\n`, ham Windows uslubidagi `\r\n` qator ko'chirishlarini avtomatik to'g'ri ajratadi.

## Ishlash natijasi:
```text
1: 1-qator: Kirish
2: 2-qator: Asosiy qism
3: 3-qator: Xulosa
```

---

# 270-Topshiriq: Bo'shliqlardan ajratish: split_whitespace()
## Topshiriq sharti:
Barcha oraliq bo'shliqlar, tab va yangi qatorlarni inobatga olgan holda so'zlarni ajrating.

## Yechim (Rust kodi):
```rust
fn main() {
    let matn = "Bugun    havo   juda    go'zal  va   iliq";

    let sozlar: Vec<&str> = matn.split_whitespace().collect();
    println!("Ajratilgan so'zlar: {:?}", sozlar);
}
```

## Tushuntirish va Mantiq:
`split_whitespace()` ketma-ket kelgan bir nechta probellarni bitta deb hisoblaydi va bo'sh elementlar hosil qilmaydi.

## Ishlash natijasi:
```text
Ajratilgan so'zlar: ["Bugun", "havo", "juda", "go'zal", "va", "iliq"]
```

---

# 271-Topshiriq: Matn qismini almashtirish: replace() va replacen()
## Topshiriq sharti:
Matn ichidagi so'zni yangisiga almashtirib, yangi `String` hosil qiling.

## Yechim (Rust kodi):
```rust
fn main() {
    let jumla = "Men C++ ni bilaman. C++ juda tez.";
    let yangi_jumla = jumla.replace("C++", "Rust");

    println!("Asl:   {}", jumla);
    println!("Yangi: {}", yangi_jumla);
}
```

## Tushuntirish va Mantiq:
`replace()` qidirilgan barcha so'zlarni almashtirib, yangi `String` yaratadi. `replacen()` esa almashtirishlar sonini cheklash imkonini beradi.

## Ishlash natijasi:
```text
Asl:   Men C++ ni bilaman. C++ juda tez.
Yangi: Men Rust ni bilaman. Rust juda tez.
```

---

# 272-Topshiriq: Matn ichida qidirish: contains, starts_with, ends_with
## Topshiriq sharti:
Satr boshlanishi, tugashi va ichida so'z borligini tekshiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let fayl = "arxiv_2024_backup.tar.gz";

    println!("Arxivmi: {}", fayl.starts_with("arxiv"));
    println!(".gz formatidami: {}", fayl.ends_with(".gz"));
    println!("2024 bormi: {}", fayl.contains("2024"));
}
```

## Tushuntirish va Mantiq:
Ushbu metodlar `bool` qaytaradi va fayl nomlarini, yo'llarni va matn qoidalarini tekshirishda juda qulaydir.

## Ishlash natijasi:
```text
Arxivmi: true
.gz formatidami: true
2024 bormi: true
```

---

# 273-Topshiriq: So'zning indeksini topish: find() va rfind()
## Topshiriq sharti:
Matn ichida qidirilayotgan qismning boshlanish bayt indeksini aniqlang.

## Yechim (Rust kodi):
```rust
fn main() {
    let matn = "Rust tili - eng zo'r dasturlash tili";

    println!("Birinchi 'tili': {:?}", matn.find("tili"));
    println!("Oxirgi 'tili':   {:?}", matn.rfind("tili"));
    println!("Mavjud emas:     {:?}", matn.find("Python"));
}
```

## Tushuntirish va Mantiq:
`find()` birinchi uchragan indeksni `Option<usize>`, `rfind()` esa oxirgi uchragan indeksni qaytaradi.

## Ishlash natijasi:
```text
Birinchi 'tili': Some(5)
Oxirgi 'tili':   Some(33)
Mavjud emas:     None
```

---

# 274-Topshiriq: format! makrosi orqali dinamik satr yig'ish
## Topshiriq sharti:
Har xil turdagi o'zgaruvchilarni bitta formatlangan `String` ga birlashtiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let foydalanuvchi = "Ali";
    let ball = 95.5;
    let orin = 1;

    let hisobot = format!("{}-o'rin: {} (Ball: {:.1})", orin, foydalanuvchi, ball);
    println!("{}", hisobot);
}
```

## Tushuntirish va Mantiq:
`format!` xuddi `println!` kabi ishlaydi, faqat terminalga chiqarmasdan natijani yangi `String` sifatida qaytaradi.

## Ishlash natijasi:
```text
1-o'rin: Ali (Ball: 95.5)
```

---

# 275-Topshiriq: Massiv bo'laklari (Array Slices: &[T])
## Topshiriq sharti:
Massivning istalgan oralig'ini qarzga oluvchi funksiya yozing.

## Yechim (Rust kodi):
```rust
fn chop_et_bolak(bolak: &[i32]) {
    println!("Bo'lak hajmi: {}, Elementlar: {:?}", bolak.len(), bolak);
}

fn main() {
    let sonlar = [1, 2, 3, 4, 5, 6, 7, 8];

    chop_et_bolak(&sonlar[0..3]);
    chop_et_bolak(&sonlar[5..]);
}
```

## Tushuntirish va Mantiq:
`&[T]` massiv yoki vektorning ixtiyoriy uzluksiz qismiga xavfsiz oynadir (view). U butun to'plamni nusxalashdan qutqaradi.

## Ishlash natijasi:
```text
Bo'lak hajmi: 3, Elementlar: [1, 2, 3]
Bo'lak hajmi: 3, Elementlar: [6, 7, 8]
```

---

# 276-Topshiriq: Slice birinchi va oxirgi elementini xavfsiz olish: first() va last()
## Topshiriq sharti:
Bo'sh bo'lishi mumkin bo'lgan slice lardan birinchi va oxirgi elementlarni oling.

## Yechim (Rust kodi):
```rust
fn main() {
    let bosh: [i32; 0] = [];
    let tola = [10, 20, 30];

    println!("Bo'sh slice first(): {:?}", bosh.first());
    println!("To'la slice first(): {:?}", tola.first());
    println!("To'la slice last():  {:?}", tola.last());
}
```

## Tushuntirish va Mantiq:
`.first()` va `.last()` har doim `Option<&T>` qaytaradi, bu bo'sh massivlarda crash bo'lish xavfini butunlay bartaraf etadi.

## Ishlash natijasi:
```text
Bo'sh slice first(): None
To'la slice first(): Some(10)
To'la slice last():  Some(30)
```

---

# 277-Topshiriq: get(range) orqali xavfsiz oraliq slice olish
## Topshiriq sharti:
Indeks chegaradan oshganda dastur to'xtamasdan `None` qaytaruvchi metodni qo'llang.

## Yechim (Rust kodi):
```rust
fn main() {
    let massiv = [10, 20, 30, 40];

    match massiv.get(1..3) {
        Some(qism) => println!("Olingan qism: {:?}", qism),
        None => println!("Noto'g'ri oraliq!"),
    }

    match massiv.get(2..10) {
        Some(qism) => println!("Olingan qism: {:?}", qism),
        None => println!("Oraliq chegaradan oshib ketdi!"),
    }
}
```

## Tushuntirish va Mantiq:
`arr.get(range)` xavfsiz dasturlashning eng muhim metodlaridan biri bo'lib, chegaradan tashqariga chiqish xatolarining oldini oladi.

## Ishlash natijasi:
```text
Olingan qism: [20, 30]
Oraliq chegaradan oshib ketdi!
```

---

# 278-Topshiriq: O'zgaruvchan slice lar (&mut [T]) ustida saralash
## Topshiriq sharti:
Massivning faqat ma'lum bir qismini saralang.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut sonlar = [9, 8, 7, 3, 2, 1];

    // Faqat birinchi 3 ta elementni saralaymiz:
    sonlar[0..3].sort();

    println!("Qisman saralangan massiv: {:?}", sonlar);
}
```

## Tushuntirish va Mantiq:
Slicelar ustida to'g'ridan-to'g'ri `.sort()` chaqirish mumkin, bu butun massivni emas, faqat tanlangan oraliqni saralash imkonini beradi.

## Ishlash natijasi:
```text
Qisman saralangan massiv: [7, 8, 9, 3, 2, 1]
```

---

# 279-Topshiriq: Slice ni teskari qilish: reverse()
## Topshiriq sharti:
Massiv bo'lagi elementlarini o'z o'rnida teskari qilib qo'ying.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut harflar = ['A', 'B', 'C', 'D', 'E'];
    harflar.reverse();

    println!("Teskari massiv: {:?}", harflar);
}
```

## Tushuntirish va Mantiq:
`.reverse()` metodi qo'shimcha xotira sarflamasdan (in-place) slice dagi elementlar tartibini teskari qiladi.

## Ishlash natijasi:
```text
Teskari massiv: ['E', 'D', 'C', 'B', 'A']
```

---

# 280-Topshiriq: Sliceni ikkiga bo'lish: split_at()
## Topshiriq sharti:
O'zgarmas massivni belgilangan indeks bo'yicha ikkita mustaqil bo'lakka ajrating.

## Yechim (Rust kodi):
```rust
fn main() {
    let sonlar = [1, 2, 3, 4, 5, 6];
    let (chap, ong) = sonlar.split_at(2);

    println!("Chap bo'lak: {:?}", chap);
    println!("O'ng bo'lak:  {:?}", ong);
}
```

## Tushuntirish va Mantiq:
`split_at(mid)` bitta massivdan ikkita bog'liq bo'lmagan `&[T]` slice larni hosil qiladi.

## Ishlash natijasi:
```text
Chap bo'lak: [1, 2]
O'ng bo'lak:  [3, 4, 5, 6]
```

---

# 281-Topshiriq: Slice ustida binar qidiruv: binary_search()
## Topshiriq sharti:
Saralangan massivda elementning indeksini standart qidiruv bilan toping.

## Yechim (Rust kodi):
```rust
fn main() {
    let saralangan = [10, 25, 40, 55, 70, 85];

    match saralangan.binary_search(&55) {
        Ok(indeks) => println!("55 soni {}-indeksda topildi.", indeks),
        Err(joy) => println!("Topilmadi. Joylashishi kerak bo'lgan indeks: {}", joy),
    }
}
```

## Tushuntirish va Mantiq:
`binary_search` topilsa `Ok(index)`, topilmasa element saralash tartibini buzmasdan qo'yilishi mumkin bo'lgan `Err(insert_index)` ni qaytaradi.

## Ishlash natijasi:
```text
55 soni 3-indeksda topildi.
```

---

# 282-Topshiriq: Sliceni vektorga aylantirish: .to_vec()
## Topshiriq sharti:
Qarzga olingan slice dan to'liq mustaqil Heap vektori yasang.

## Yechim (Rust kodi):
```rust
fn main() {
    let massiv = [1, 2, 3];
    let bolak: &[i32] = &massiv[..];

    let mut v: Vec<i32> = bolak.to_vec();
    v.push(4);

    println!("Yangi vektor: {:?}", v);
}
```

## Tushuntirish va Mantiq:
`.to_vec()` slice elementlarining to'liq nusxasini olib, Heap xotirada yangi o'suvchi `Vec<T>` yaratadi.

## Ishlash natijasi:
```text
Yangi vektor: [1, 2, 3, 4]
```

---

# 283-Topshiriq: Slicelar orasida nusxa ko'chirish: copy_from_slice()
## Topshiriq sharti:
Bitta massiv elementlarini ikkinchisiga tezkor nusxalang.

## Yechim (Rust kodi):
```rust
fn main() {
    let manba = [100, 200, 300];
    let mut nishon = [0; 3];

    nishon.copy_from_slice(&manba);

    println!("Nishon massiv: {:?}", nishon);
}
```

## Tushuntirish va Mantiq:
`copy_from_slice()` apparat darajasidagi tezkor `memcpy` amalini bajaradi va xotirani bir harakatda to'ldiradi.

## Ishlash natijasi:
```text
Nishon massiv: [100, 200, 300]
```

---

# 284-Topshiriq: Stringni Vec<u8> baytlar vektoriga aylantirish
## Topshiriq sharti:
`into_bytes()` orqali satrning xom baytlarini o'zlashtiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let matn = String::from("ABC");
    let baytlar = matn.into_bytes(); // String iste'mol qilinadi, Vec<u8> qaytadi

    println!("Baytlar vektori: {:?}", baytlar);
}
```

## Tushuntirish va Mantiq:
`into_bytes()` xotirani qayta ajratmaydi! U shunchaki mavjud Heap ko'rsatkichini `Vec<u8>` sifatida qayta talqin qiladi.

## Ishlash natijasi:
```text
Baytlar vektori: [65, 66, 67]
```

---

# 285-Topshiriq: Vec<u8> dan String yasash: String::from_utf8
## Topshiriq sharti:
Xom baytlar vektorining to'g'ri UTF-8 ekanligini tekshirib satrga o'giring.

## Yechim (Rust kodi):
```rust
fn main() {
    let baytlar = vec![82, 117, 115, 116]; // 'R', 'u', 's', 't'

    match String::from_utf8(baytlar) {
        Ok(satr) => println!("Hosil bo'lgan satr: {}", satr),
        Err(xato) => println!("Noto'g'ri UTF-8: {}", xato),
    }
}
```

## Tushuntirish va Mantiq:
Rust hech qachon noto'g'ri UTF-8 ma'lumotning `String` bo'lishiga yo'l qo'ymaydi. Shu sababli `from_utf8` har doim `Result` qaytaradi.

## Ishlash natijasi:
```text
Hosil bo'lgan satr: Rust
```

---

# 286-Topshiriq: String::from_utf8_lossy bilan buzilgan baytlarni xavfsiz o'qish
## Topshiriq sharti:
Noto'g'ri UTF-8 baytlar uchraganda ularni  belgisi bilan almashtirib o'qish.

## Yechim (Rust kodi):
```rust
fn main() {
    let xato_baytlar = vec![72, 101, 108, 108, 111, 0xFF, 33];
    let tozalangan = String::from_utf8_lossy(&xato_baytlar);

    println!("Lossy natija: {}", tozalangan);
}
```

## Tushuntirish va Mantiq:
`from_utf8_lossy` buzilgan har qanday baytni 'Unicode Replacement Character' () bilan almashtiradi va dastur crash bo'lishining oldini oladi.

## Ishlash natijasi:
```text
Lossy natija: Hello!
```

---

# 287-Topshiriq: Katta va kichik harflarga o'tkazish: to_uppercase va to_lowercase
## Topshiriq sharti:
Satr registrini to'liq Unicode qoidalariga mos ravishda o'zgartiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let matn = "o'zbekiston kelajagi buyuk davlat";

    println!("Katta harflar: {}", matn.to_uppercase());
    println!("Kichik harflar: {}", "RUST TILI".to_lowercase());
}
```

## Tushuntirish va Mantiq:
Ushbu metodlar butun dunyo tillarining barcha harf o'zgarish qoidalarini (masalan nemischa ß -> SS) to'g'ri bajaradi.

## Ishlash natijasi:
```text
Katta harflar: O'ZBEKISTON KELAJAGI BUYUK DAVLAT
Kichik harflar: rust tili
```

---

# 288-Topshiriq: Matnni takrorlash: repeat(n)
## Topshiriq sharti:
Satrni berilgan N marta takrorlab yangi `String` yarating.

## Yechim (Rust kodi):
```rust
fn main() {
    let chiziq = "-=".repeat(10);
    println!("{}", chiziq);
}
```

## Tushuntirish va Mantiq:
`repeat(n)` metodi kerakli hajmdagi xotirani bir martada ajratadi va matnni n marta takrorlab to'ldiradi.

## Ishlash natijasi:
```text
-=-=-=-=-=-=-=-=-=-=
```

---

# 289-Topshiriq: Cow<'a, str> (Clone-on-Write) tushunchasi
## Topshiriq sharti:
Agar o'zgartirish kerak bo'lmasa qarzga oluvchi, kerak bo'lsa klonlovchi aqlli turni ko'rsating.

## Yechim (Rust kodi):
```rust
use std::borrow::Cow;

fn xavfsiz_ajrat(matn: &str) -> Cow<str> {
    if matn.contains("xato") {
        Cow::Owned(matn.replace("xato", "tuzatildi"))
    } else {
        Cow::Borrowed(matn) // Nusxa olinmadi!
    }
}

fn main() {
    let s1 = "hamma narsa yaxshi";
    let r1 = xavfsiz_ajrat(s1);
    println!("r1: {} (Borrowed)", r1);

    let s2 = "bu yerda xato bor";
    let r2 = xavfsiz_ajrat(s2);
    println!("r2: {} (Owned)", r2);
}
```

## Tushuntirish va Mantiq:
`Cow` (Clone-on-Write) faqat zarurat tug'ilgandagina Heap xotira ajratadi, aks holda manbadan tekinga foydalanadi.

## Ishlash natijasi:
```text
r1: hamma narsa yaxshi (Borrowed)
r2: bu yerda tuzatildi bor (Owned)
```

---

# 290-Topshiriq: Matn ichidagi sonlarni ajratib olib parse qilish
## Topshiriq sharti:
Satrdan raqamlarni ajratib, ularni `i32` turiga o'giring va yig'indisini hisoblang.

## Yechim (Rust kodi):
```rust
fn main() {
    let malumot = "10 20 30 40";
    let mut yigindi = 0;

    for bolak in malumot.split_whitespace() {
        if let Ok(son) = bolak.parse::<i32>() {
            yigindi += son;
        }
    }

    println!("Yig'indi: {}", yigindi);
}
```

## Tushuntirish va Mantiq:
`.parse::<T>()` satrni berilgan songa o'tkazadi va agar xato bo'lsa `Err` qaytaradi.

## Ishlash natijasi:
```text
Yig'indi: 100
```

---

# 291-Topshiriq: CSV qatorini parse qilish (Nol nusxali yondashuv)
## Topshiriq sharti:
CSV qatoridagi ustunlarni yangi `String` yaratmasdan `&str` orqali saqlang.

## Yechim (Rust kodi):
```rust
fn main() {
    let csv_qator = "Ali,24,Dasturchi,Toshkent";
    let ustunlar: Vec<&str> = csv_qator.split(',').collect();

    println!("Ism:      {}", ustunlar[0]);
    println!("Yosh:     {}", ustunlar[1]);
    println!("Kasb:     {}", ustunlar[2]);
    println!("Yashash:  {}", ustunlar[3]);
}
```

## Tushuntirish va Mantiq:
Barcha ustunlar bevosita `csv_qator` xotirasiga ishora qiladi. 0 bayt qo'shimcha satr xotirasi sarflanadi.

## Ishlash natijasi:
```text
Ism:      Ali
Yosh:     24
Kasb:     Dasturchi
Yashash:  Toshkent
```

---

# 292-Topshiriq: Matndagi eng uzun so'zni aniqlash funksiyasi
## Topshiriq sharti:
Jumladagi eng ko'p harfli so'zni `&str` ko'rinishida toping.

## Yechim (Rust kodi):
```rust
fn eng_uzun_soz(matn: &str) -> &str {
    let mut eng_uzun = "";
    for soz in matn.split_whitespace() {
        if soz.len() > eng_uzun.len() {
            eng_uzun = soz;
        }
    }
    eng_uzun
}

fn main() {
    let matn = "Rust axlat yig'uvchisiz xotira xavfsizligini kafolatlaydi";
    println!("Eng uzun so'z: '{}'", eng_uzun_soz(matn));
}
```

## Tushuntirish va Mantiq:
Funksiya kiruvchi matnning o'zidan bo'lak qaytaradi, shuning uchun hech qanday nusxalash yuz bermaydi.

## Ishlash natijasi:
```text
Eng uzun so'z: 'xavfsizligini'
```

---

# 293-Topshiriq: URL query parametrlarini format! orqali xavfsiz shakllantirish
## Topshiriq sharti:
Parametrlarni URL satriga xavfsiz birlashtiring.

## Yechim (Rust kodi):
```rust
fn url_yasa(asosiy: &str, qidiruv: &str, sahifa: u32) -> String {
    format!("https://{}/qidiruv?q={}&page={}", asosiy, qidiruv, sahifa)
}

fn main() {
    let url = url_yasa("kun.uz", "rust_til", 1);
    println!("Yaratilgan URL: {}", url);
}
```

## Tushuntirish va Mantiq:
`format!` makrosi turli parametrlarni birlashtirib, standart formatdagi so'rov satrlarini hosil qilishda qulaydir.

## Ishlash natijasi:
```text
Yaratilgan URL: https://kun.uz/qidiruv?q=rust_til&page=1
```

---

# 294-Topshiriq: So'zlarni teskari tartibda joylashtirish
## Topshiriq sharti:
Jumlani so'zma-so'z teskari qilib yangi matn hosil qiling.

## Yechim (Rust kodi):
```rust
fn main() {
    let jumla = "Rust tili juda tez";
    let teskari_sozlar: Vec<&str> = jumla.split_whitespace().rev().collect();
    let yangi_jumla = teskari_sozlar.join(" ");

    println!("Teskari jumla: {}", yangi_jumla);
}
```

## Tushuntirish va Mantiq:
`.split_whitespace()`, `.rev()` va `.join(" ")` funksional zanjiri matnni tez va aniq o'zgartiradi.

## Ishlash natijasi:
```text
Teskari jumla: tez juda tili Rust
```

---

# 295-Topshiriq: Matndan raqam bo'lmagan belgilarni tozalash
## Topshiriq sharti:
Telefon raqamidan faqat raqamlarni ajratib oling.

## Yechim (Rust kodi):
```rust
fn raqamlarni_ajrat(tel: &str) -> String {
    tel.chars().filter(|c| c.is_numeric()).collect()
}

fn main() {
    let xom_tel = "+998 (90) 123-45-67";
    let toza = raqamlarni_ajrat(xom_tel);

    println!("Toza raqam: {}", toza);
}
```

## Tushuntirish va Mantiq:
`filter(|c| c.is_numeric())` va `.collect()` orqali faqat raqamlar saralanib yangi satrga yig'iladi.

## Ishlash natijasi:
```text
Toza raqam: 998901234567
```

---

# 296-Topshiriq: Qator uzunliklarini cheklash va '...' qo'shish (Truncate with Ellipsis)
## Topshiriq sharti:
Uzun sarlavhani belgilangan uzunlikda qirqib, oxiriga uch nuqta qo'ying.

## Yechim (Rust kodi):
```rust
fn qisqartir(matn: &str, max_len: usize) -> String {
    if matn.chars().count() <= max_len {
        matn.to_string()
    } else {
        let qism: String = matn.chars().take(max_len).collect();
        format!("{}...", qism)
    }
}

fn main() {
    let matn = "Rust 2024 yangi imkoniyatlari to'liq sharhi";
    println!("{}", qisqartir(matn, 15));
}
```

## Tushuntirish va Mantiq:
Unicode belgilar sonini to'g'ri hisoblash uchun `chars().count()` va `chars().take()` dan foydalanish xavfsizdir.

## Ishlash natijasi:
```text
Rust 2024 yangi...
```

---

# 297-Topshiriq: Massiv bo'lagini to'ldirish: fill() va fill_with()
## Topshiriq sharti:
Massivning tanlangan bo'lagini bir xil qiymat bilan to'ldiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut bufer = [0; 6];
    bufer[2..5].fill(99);

    println!("To'ldirilgan bufer: {:?}", bufer);
}
```

## Tushuntirish va Mantiq:
`.fill(val)` metodi butun slice bo'ylab ko'rsatilgan qiymatni nusxalab chiqadi.

## Ishlash natijasi:
```text
To'ldirilgan bufer: [0, 0, 99, 99, 99, 0]
```

---

# 298-Topshiriq: Satr boshidagi va oxiridagi belgilar sonini sanash
## Topshiriq sharti:
Satr boshidagi nollarni sanovchi yordamchi algoritm yozing.

## Yechim (Rust kodi):
```rust
fn bosh_nollarni_sana(s: &str) -> usize {
    s.chars().take_while(|&c| c == '0').count()
}

fn main() {
    let son_satr = "000045200";
    println!("Boshdagi nollar: {}", bosh_nollarni_sana(son_satr));
}
```

## Tushuntirish va Mantiq:
`take_while()` shart to'g'ri bo'lib turguncha belgilarni oladi va shart buzilishi bilan to'xtaydi.

## Ishlash natijasi:
```text
Boshdagi nollar: 4
```

---

# 299-Topshiriq: Slice bo'ylab oyna siljitish (Windows iterator: .windows(N))
## Topshiriq sharti:
Massiv bo'ylab N ta elementli suriluvchi oyna (sliding window) aylanishi.

## Yechim (Rust kodi):
```rust
fn main() {
    let haroratlar = [20, 22, 25, 24, 28, 30];

    println!("2 kunlik o'zgarishlar:");
    for oyna in haroratlar.windows(2) {
        println!("Oraliq: {} -> {}", oyna[0], oyna[1]);
    }
}
```

## Tushuntirish va Mantiq:
`.windows(size)` siljuvchi oyna iteratori bo'lib, vaqt ketma-ketliklari va signal tahlilida nihoyatda samaralidir.

## Ishlash natijasi:
```text
2 kunlik o'zgarishlar:
Oraliq: 20 -> 22
Oraliq: 22 -> 25
Oraliq: 25 -> 24
Oraliq: 24 -> 28
Oraliq: 28 -> 30
```

---

# 300-Topshiriq: Slices va String moduli xulosasi: To'liq xotira boshqaruvi
## Topshiriq sharti:
String va slice larning asosiy qoidalarini jamlovchi xulosa dastur.

## Yechim (Rust kodi):
```rust
fn main() {
    println!("=== RUST STRING VA SLICE XULOSASI ===");
    println!("1. String - Heap dagi kengayuvchi egali matn (24 bayt Stack da).");
    println!("2. &str - xotiradagi ixtiyoriy matnning 16 baytli ko'rinishi (Fat Pointer).");
    println!("3. Rust barcha matnlarni UTF-8 da saqlaydi, xom indekslash taqiqlangan.");
    println!("4. &[T] massiv va vektorlarning nol-nusxali oynasidir.");
    println!("5. Windows va Chunks iteratorlari yuqori unumdorlikni ta'minlaydi.");
}
```

## Tushuntirish va Mantiq:
Rust ning matn va slice arxitekturasi dasturchiga to'liq xavfsizlik va C tezligidagi unumdorlikni bir vaqtda beradi.

## Ishlash natijasi:
```text
=== RUST STRING VA SLICE XULOSASI ===
1. String - Heap dagi kengayuvchi egali matn (24 bayt Stack da).
2. &str - xotiradagi ixtiyoriy matnning 16 baytli ko'rinishi (Fat Pointer).
3. Rust barcha matnlarni UTF-8 da saqlaydi, xom indekslash taqiqlangan.
4. &[T] massiv va vektorlarning nol-nusxali oynasidir.
5. Windows va Chunks iteratorlari yuqori unumdorlikni ta'minlaydi.
```

---
