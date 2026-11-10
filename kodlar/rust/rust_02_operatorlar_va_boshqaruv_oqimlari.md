# 2-Qism: Operatorlar va Dastur Boshqaruv Oqimlari (51-100)

Ushbu qismda Rust dasturlash tilidagi mantiqiy tarmoqlanishlar (`if`, `else if`, `else`), ifodali (expression-based) boshqaruv, cheksiz va shartli tsikllar (`loop`, `while`, `for`), nomlangan tsikllar, kuchli pattern matching (`match`, match guards, `if let`, `while let`, `let else`) hamda klassik matematik va qidiruv algoritmlari o'rganiladi.

---

# 51-Topshiriq: if va else shart operatorlari
## Topshiriq sharti:
Kiritilgan son musbat yoki manfiy ekanligini if-else yordamida tekshiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let son = 15;

    if son > 0 {
        println!("Son musbat: {}", son);
    } else {
        println!("Son manfiy yoki nolga teng: {}", son);
    }
}
```

## Tushuntirish va Mantiq:
Rust da `if` sharti qavslarsiz `()` yoziladi, lekin jingalak qavslar `{}` majburiydir. Shart ifodasi har doim aniq `bool` turi bo'lishi shart (0 yoki 1 qabul qilinmaydi).

## Ishlash natijasi:
```text
Son musbat: 15
```

---

# 52-Topshiriq: if - else if - else zanjirli tarmoqlanish
## Topshiriq sharti:
Imtihon balliga qarab talabaning bahosini (A, B, C, F) aniqlang.

## Yechim (Rust kodi):
```rust
fn main() {
    let ball = 85;

    if ball >= 90 {
        println!("Baho: A (A'lo)");
    } else if ball >= 80 {
        println!("Baho: B (Yaxshi)");
    } else if ball >= 60 {
        println!("Baho: C (Qoniqarli)");
    } else {
        println!("Baho: F (Qoniqarsiz)");
    }
}
```

## Tushuntirish va Mantiq:
Bir nechta shartlarni ketma-ket tekshirish uchun `else if` zanjiridan foydalaniladi. Birinchi to'g'ri kelgan blok bajariladi va qolganlari tashlab ketiladi.

## Ishlash natijasi:
```text
Baho: B (Yaxshi)
```

---

# 53-Topshiriq: if ifodasi (expression) orqali o'zgaruvchiga qiymat biriktirish
## Topshiriq sharti:
Ternar operatori o'rniga Rust ning `let x = if condition { a } else { b };` sintaksisini qo'llang.

## Yechim (Rust kodi):
```rust
fn main() {
    let yosh = 19;
    let maqom = if yosh >= 18 { "Voyaga yetgan" } else { "Voyaga yetmagan" };

    println!("Fuqaro maqomi: {}", maqom);
}
```

## Tushuntirish va Mantiq:
Rust da `if` oddiy ko'rsatma (statement) emas, balki qiymat qaytaruvchi ifodadir (expression). Shu sababli Rust da boshqa tillardagi `?:` ternar operatori mavjud emas.

## Ishlash natijasi:
```text
Fuqaro maqomi: Voyaga yetgan
```

---

# 54-Topshiriq: if ifodasida turlarning bir xilligi talabi
## Topshiriq sharti:
if va else bloklaridan bir xil turdagi qiymat qaytishi shartligini ko'rsatuvchi dastur tuzing.

## Yechim (Rust kodi):
```rust
fn main() {
    let chegirma_bormi = true;
    let yakuniy_narx = if chegirma_bormi {
        100 - 15
    } else {
        100
    };

    println!("To'lov summasi: ${}", yakuniy_narx);
}
```

## Tushuntirish va Mantiq:
Kompilyator `yakuniy_narx` turini oldindan bilishi uchun `if` va `else` bloklari qaytaradigan qiymat turi mutlaqo bir xil (masalan `i32`) bo'lishi shart.

## Ishlash natijasi:
```text
To'lov summasi: $85
```

---

# 55-Topshiriq: Murakkab mantiqiy shartlar (AND, OR, NOT)
## Topshiriq sharti:
Berilgan yil kabisa (leap year) ekanligini mantiqiy amallar bilan aniqlang.

## Yechim (Rust kodi):
```rust
fn main() {
    let yil = 2024;
    let kabisami = (yil % 4 == 0 && yil % 100 != 0) || (yil % 400 == 0);

    if kabisami {
        println!("{} - kabisa yili (366 kun).", yil);
    } else {
        println!("{} - oddiy yil (365 kun).", yil);
    }
}
```

## Tushuntirish va Mantiq:
Rust da mantiqiy qisqa tutashuv (short-circuit evaluation) mavjud: agar `&&` ning chap tomoni yolg'on bo'lsa, o'ng tomoni hisoblanmaydi.

## Ishlash natijasi:
```text
2024 - kabisa yili (366 kun).
```

---

# 56-Topshiriq: Ichma-ich (nested) shartlar va ularni soddalashtirish
## Topshiriq sharti:
Foydalanuvchi tizimga kirish huquqini bir necha parametr bo'yicha tekshiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let foydalanuvchi_faol = true;
    let parol_togri = true;
    let admin = false;

    if foydalanuvchi_faol {
        if parol_togri {
            if admin {
                println!("Admin paneliga xush kelibsiz!");
            } else {
                println!("Foydalanuvchi profiliga xush kelibsiz!");
            }
        }
    }
}
```

## Tushuntirish va Mantiq:
Ichma-ich shartlar orqali bosqichma-bosqich tekshiruvlar amalga oshiriladi. Murakkab holatlarda kodni toza saqlash uchun `guard clauses` yoki `match` tavsiya etiladi.

## Ishlash natijasi:
```text
Foydalanuvchi profiliga xush kelibsiz!
```

---

# 57-Topshiriq: Cheksiz tsikl: loop va break operatori
## Topshiriq sharti:
`loop` orqali cheksiz tsikl oching va sanagich 5 ga yetganda `break` bilan chiqib keting.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut sanagich = 0;

    loop {
        sanagich += 1;
        println!("Tsikl qadami: {}", sanagich);

        if sanagich == 5 {
            break;
        }
    }
    println!("Tsikl yakunlandi.");
}
```

## Tushuntirish va Mantiq:
`loop` kalit so'zi to `break` buyrug'i berilguncha to'xtovsiz aylanadi. Bu mikrokontrollerlar, server tinglovchilari va o'yin sikllari uchun standartdir.

## Ishlash natijasi:
```text
Tsikl qadami: 1
Tsikl qadami: 2
Tsikl qadami: 3
Tsikl qadami: 4
Tsikl qadami: 5
Tsikl yakunlandi.
```

---

# 58-Topshiriq: loop dan break orqali qiymat qaytarish
## Topshiriq sharti:
`break qiymat;` sintaksisi orqali tsikldan hisoblangan natijani o'zgaruvchiga o'zlashtiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut hisoblagich = 0;

    let natija = loop {
        hisoblagich += 1;
        if hisoblagich == 10 {
            break hisoblagich * 2; // Natija sifatida 20 qaytariladi
        }
    };

    println!("Tsikl qaytargan natija: {}", natija);
}
```

## Tushuntirish va Mantiq:
Rust da `loop` bloki `break` orqali qiymat qaytara oladi. Bu amallarni bajarib, kerakli natija topilganda uni to'g'ridan-to'g'ri o'zgaruvchiga uzatish imkonini beradi.

## Ishlash natijasi:
```text
Tsikl qaytargan natija: 20
```

---

# 59-Topshiriq: Tsikl ichida continue bilan keyingi iteratsiyaga o'tish
## Topshiriq sharti:
1 dan 10 gacha sonlar ichida toq sonlarni chop eting, juft sonlarni `continue` bilan o'tkazib yuboring.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut n = 0;

    while n < 10 {
        n += 1;
        if n % 2 == 0 {
            continue; // Juft bo'lsa, qolgan kodni bajarma
        }
        println!("Toq son: {}", n);
    }
}
```

## Tushuntirish va Mantiq:
`continue` operatori joriy iteratsiyaning qolgan qismini tashlab yuboradi va darhol keyingi aylanishga o'tadi.

## Ishlash natijasi:
```text
Toq son: 1
Toq son: 3
Toq son: 5
Toq son: 7
Toq son: 9
```

---

# 60-Topshiriq: Nomlangan tsikllar (Loop Labels: 'label)
## Topshiriq sharti:
Tashqi tsiklga `'tashqi` deb nom bering va uning ishlashini namoyish eting.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut i = 0;

    'tashqi: loop {
        println!("Tashqi sikl: {}", i);
        let mut j = 0;
        loop {
            if j == 2 {
                break; // Faqat ichki sikldan chiqadi
            }
            j += 1;
        }
        i += 1;
        if i == 3 {
            break 'tashqi; // Tashqi sikldan to'liq chiqadi
        }
    }
}
```

## Tushuntirish va Mantiq:
Tsikl oldidan apostrof `'nom:` qo'yilsa, tsikl o'z belgisiga ega bo'ladi. Bu ichma-ich murakkab algoritmlarda boshqaruvni o'ta qulay qiladi.

## Ishlash natijasi:
```text
Tashqi sikl: 0
Tashqi sikl: 1
Tashqi sikl: 2
```

---

# 61-Topshiriq: Ichki tsikldan turib to'g'ridan-to'g'ri tashqi tsiklni to'xtatish
## Topshiriq sharti:
2D qidiruvda kerakli element topilganda ichki tsikldan tashqi tsiklni darhol to'xtating.

## Yechim (Rust kodi):
```rust
fn main() {
    let nishon = 7;
    let massiv = [[1, 2, 3], [4, 7, 6], [8, 9, 0]];

    'matritsa: for i in 0..3 {
        for j in 0..3 {
            if massiv[i][j] == nishon {
                println!("Nishon {} topildi koordinata: ({}, {})", nishon, i, j);
                break 'matritsa;
            }
        }
    }
}
```

## Tushuntirish va Mantiq:
`break 'belgi;` orqali bir necha pog'ona ichkaridan istalgan tashqi tsiklni bitta harakat bilan to'xtatish mumkin.

## Ishlash natijasi:
```text
Nishon 7 topildi koordinata: (1, 1)
```

---

# 62-Topshiriq: while tsikli: Shart asosida takrorlash
## Topshiriq sharti:
Shart to'g'ri bo'lib turganda ishlaydigan `while` tsiklini tuzing.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut son = 3;

    while son > 0 {
        println!("Sanagich: {}", son);
        son -= 1;
    }
    println!("Start!");
}
```

## Tushuntirish va Mantiq:
`while` har bir iteratsiyadan oldin shartni tekshiradi. Shart `false` bo'lishi bilan tsikl o'z ishini to'xtatadi.

## Ishlash natijasi:
```text
Sanagich: 3
Sanagich: 2
Sanagich: 1
Start!
```

---

# 63-Topshiriq: while tsikli orqali 2 ning darajalarini hisoblash
## Topshiriq sharti:
Son 1000 dan oshmaguncha uning 2 ga ko'payib borish ketma-ketligini chiqaring.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut daraja = 1;

    while daraja <= 1000 {
        print!("{} ", daraja);
        daraja *= 2;
    }
    println!();
}
```

## Tushuntirish va Mantiq:
`while` noma'lum marta takrorlanadigan, faqat ma'lum bir matematik chegaraga bog'liq jarayonlar uchun qulaydir.

## Ishlash natijasi:
```text
1 2 4 8 16 32 64 128 256 512 
```

---

# 64-Topshiriq: while tsiklida bir nechta shartlarni birgalikda tekshirish
## Topshiriq sharti:
Ikkita ko'rsatkich (pointer) yaqinlashishini `while` tsiklida amalga oshiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut chap = 0;
    let mut ong = 10;

    while chap < ong && ong > 5 {
        println!("Chap: {}, O'ng: {}", chap, ong);
        chap += 1;
        ong -= 1;
    }
}
```

## Tushuntirish va Mantiq:
`while` shartida mantiqiy operatorlar yordamida bir vaqtning o'zida bir nechta chegaralar nazorat qilinadi.

## Ishlash natijasi:
```text
Chap: 0, O'ng: 10
Chap: 1, O'ng: 9
Chap: 2, O'ng: 8
Chap: 3, O'ng: 7
Chap: 4, O'ng: 6
```

---

# 65-Topshiriq: for tsikli va yarim ochiq intervallar (a..b)
## Topshiriq sharti:
`1..5` oralig'i bo'yicha for tsiklini ishlatib, 1 dan 4 gacha sonlarni chop eting.

## Yechim (Rust kodi):
```rust
fn main() {
    for i in 1..5 {
        println!("i qiymati: {}", i);
    }
}
```

## Tushuntirish va Mantiq:
`a..b` sintaksisi yarim ochiq interval bo'lib, `a` kiradi, lekin `b` kirmaydi (`a <= x < b`). Rust da xatoliklarni oldini olish uchun bu standart interval hisoblanadi.

## Ishlash natijasi:
```text
i qiymati: 1
i qiymati: 2
i qiymati: 3
i qiymati: 4
```

---

# 66-Topshiriq: for tsikli va yopiq intervallar (a..=b)
## Topshiriq sharti:
`1..=5` oralig'i yordamida oxirgi sonni ham o'z ichiga olgan tsikl tuzing.

## Yechim (Rust kodi):
```rust
fn main() {
    for i in 1..=5 {
        println!("Qadam: {}", i);
    }
}
```

## Tushuntirish va Mantiq:
`a..=b` inkluziv (yopiq) interval bo'lib, ikkala chegara ham tsiklga kiradi (`a <= x <= b`).

## Ishlash natijasi:
```text
Qadam: 1
Qadam: 2
Qadam: 3
Qadam: 4
Qadam: 5
```

---

# 67-Topshiriq: Intervallarni .rev() orqali teskari tartibda aylantirish
## Topshiriq sharti:
10 dan 1 gacha teskari sanash jarayonini for tsiklida bajaring.

## Yechim (Rust kodi):
```rust
fn main() {
    for son in (1..=5).rev() {
        println!("Vaqt qoldi: {}", son);
    }
    println!("Vaqt tugadi!");
}
```

## Tushuntirish va Mantiq:
Intervallar Rust da iterator bo'lgani sababli, ularga `.rev()` metodini qo'llash orqali teskari harakatlanish imkoniyati mavjud.

## Ishlash natijasi:
```text
Vaqt qoldi: 5
Vaqt qoldi: 4
Vaqt qoldi: 3
Vaqt qoldi: 2
Vaqt qoldi: 1
Vaqt tugadi!
```

---

# 68-Topshiriq: Massiv elementlari bo'ylab for tsikli orqali iteratsiya
## Topshiriq sharti:
Massiv elementlarini to'g'ridan-to'g'ri `for item in array` orqali aylanib chiqing.

## Yechim (Rust kodi):
```rust
fn main() {
    let shaharlar = ["Toshkent", "Buxoro", "Xiva", "Samarqand"];

    for shahar in shaharlar {
        println!("Tashrif manzili: {}", shahar);
    }
}
```

## Tushuntirish va Mantiq:
Rust da massiv elementlarini indekslarsiz to'g'ridan-to'g'ri iteratsiya qilish eng xavfsiz va eng tezkor usuldir, chunki bu ortiqcha chegarani tekshirish (bounds check) xarajatlarini yo'qotadi.

## Ishlash natijasi:
```text
Tashrif manzili: Toshkent
Tashrif manzili: Buxoro
Tashrif manzili: Xiva
Tashrif manzili: Samarqand
```

---

# 69-Topshiriq: for tsiklida .iter().enumerate() orqali indeks va qiymatni birga olish
## Topshiriq sharti:
Element bilan bir qatorda uning massivdagi tartib raqamini ham oling.

## Yechim (Rust kodi):
```rust
fn main() {
    let tillar = ["Rust", "C++", "Python"];

    for (indeks, til) in tillar.iter().enumerate() {
        println!("{}-o'rin: {}", indeks + 1, til);
    }
}
```

## Tushuntirish va Mantiq:
`.enumerate()` metodi har bir element uchun `(indeks, &element)` juftligini hosil qiladi, bu indeksni qo'lda sanash majburiyatidan xalos etadi.

## Ishlash natijasi:
```text
1-o'rin: Rust
2-o'rin: C++
3-o'rin: Python
```

---

# 70-Topshiriq: Tsiklda yig'indini akkumulyator orqali hisoblash
## Topshiriq sharti:
1 dan 100 gacha bo'lgan barcha sonlar yig'indisini for tsikli orqali hisoblang.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut jami = 0;

    for n in 1..=100 {
        jami += n;
    }

    println!("1 dan 100 gacha yig'indi: {}", jami);
}
```

## Tushuntirish va Mantiq:
`mut jami` akkumulyator o'zgaruvchisi har bir qadamda qiymatni o'zida to'plab boradi. Arifmetik progressiya formulasi n*(n+1)/2 = 5050 ga teng.

## Ishlash natijasi:
```text
1 dan 100 gacha yig'indi: 5050
```

---

# 71-Topshiriq: match ifodasi: Butun sonlar bo'yicha tarmoqlanish
## Topshiriq sharti:
Hafta kunining raqamiga (1-7) qarab kun nomini `match` orqali aniqlang.

## Yechim (Rust kodi):
```rust
fn main() {
    let kun = 3;

    let kun_nomi = match kun {
        1 => "Dushanba",
        2 => "Seshanba",
        3 => "Chorshanba",
        4 => "Payshanba",
        5 => "Juma",
        6 => "Shanba",
        7 => "Yakshanba",
        _ => "Noma'lum kun",
    };

    println!("{}-kun: {}", kun, kun_nomi);
}
```

## Tushuntirish va Mantiq:
`match` boshqa tillardagi `switch-case` ning Rust dagi ancha quvvatli analogidir. Rust da `break` yozish shart emas, har bir tarmoq avtomatik to'xtaydi.

## Ishlash natijasi:
```text
3-kun: Chorshanba
```

---

# 72-Topshiriq: match da bir nechta qiymatni bitta tarmoqda birlashtirish (|)
## Topshiriq sharti:
Oy raqamiga qarab faslni aniqlashda `|` (OR) patternidan foydalaning.

## Yechim (Rust kodi):
```rust
fn main() {
    let oy = 7;

    let fasl = match oy {
        12 | 1 | 2 => "Qish",
        3 | 4 | 5 => "Bahor",
        6 | 7 | 8 => "Yoz",
        9 | 10 | 11 => "Kuz",
        _ => "Bunday oy mavjud emas",
    };

    println!("{}-oy fasli: {}", oy, fasl);
}
```

## Tushuntirish va Mantiq:
`|` belgisi bir nechta muqobil qiymatlarni bitta tarmoqqa jamlash imkonini beradi va kod takrorlanishining oldini oladi.

## Ishlash natijasi:
```text
7-oy fasli: Yoz
```

---

# 73-Topshiriq: match da intervallardan foydalanish (a..=b)
## Topshiriq sharti:
Talaba yoshiga qarab uning ta'lim bosqichini aniqlang.

## Yechim (Rust kodi):
```rust
fn main() {
    let yosh = 14;

    let bosqich = match yosh {
        0..=6 => "Bog'cha yoshi",
        7..=17 => "Maktab o'quvchisi",
        18..=22 => "Talaba",
        _ => "Katta yoshli fuqaro",
    };

    println!("{} yosh: {}", yosh, bosqich);
}
```

## Tushuntirish va Mantiq:
`match` tarmoqlarida `..=` yopiq oraliqlari qo'llanilishi mumkin, bu katta diapazonlarni bitta qatorda ifodalashga xizmat qiladi.

## Ishlash natijasi:
```text
14 yosh: Maktab o'quvchisi
```

---

# 74-Topshiriq: match ning to'liqligi (Exhaustiveness) va wildcard (_) qoidasi
## Topshiriq sharti:
Kompilyator barcha holatlar ko'rib chiqilganligini talab qilishi va `_` rolini ko'rsating.

## Yechim (Rust kodi):
```rust
fn main() {
    let belgi = 'x';

    match belgi {
        'a' => println!("Birinchi unli harf"),
        'b' => println!("Ikkinchi harf"),
        _ => println!("Boshqa ixtiyoriy belgi: '{}'", belgi),
    }
}
```

## Tushuntirish va Mantiq:
Rust da `match` barcha mumkin bo'lgan qiymatlarni to'liq qamrab olishi (exhaustive) shart. `_` barcha qolgan holatlarni ushlab oluvchi universal tarmoqdir.

## Ishlash natijasi:
```text
Boshqa ixtiyoriy belgi: 'x'
```

---

# 75-Topshiriq: match ichida qo'shimcha shartlar: Match Guards
## Topshiriq sharti:
`match` tarmog'ida `if` shartini (guard) qo'shib, sonning juft yoki toqligini tekshiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let son = 8;

    match son {
        n if n < 0 => println!("{} - manfiy son", n),
        n if n % 2 == 0 => println!("{} - musbat juft son", n),
        n => println!("{} - musbat toq son", n),
    }
}
```

## Tushuntirish va Mantiq:
Match Guard `=>` belgisidan oldin `if shart` qo'yish imkonini beradi. Tarmoq faqat pattern mos kelganda VA guard `true` bo'lgandagina ishga tushadi.

## Ishlash natijasi:
```text
8 - musbat juft son
```

---

# 76-Topshiriq: Match guardlar orqali harorat holatini baholash
## Topshiriq sharti:
Harorat qiymatiga qarab tavsiya beruvchi match ifodasini yozing.

## Yechim (Rust kodi):
```rust
fn main() {
    let harorat = 38;

    match harorat {
        t if t > 40 => println!("O'ta issiq! Uyda qoling."),
        t if t >= 25 && t <= 40 => println!("Issiq va quyoshli ob-havo."),
        t if t >= 10 && t < 25 => println!("Yoqimli salqin havo."),
        _ => println!("Sovuq havo, issiq kiyining."),
    }
}
```

## Tushuntirish va Mantiq:
Guardlar yordamida matematik oraliqlar va mantiqiy bog'lanishlarni ifodalash kodni if-else zanjiriga qaraganda tartibli va o'qilishi oson qiladi.

## Ishlash natijasi:
```text
Issiq va quyoshli ob-havo.
```

---

# 77-Topshiriq: Kortejlarni match qilish va destrukturizatsiya
## Topshiriq sharti:
2D koordinata nuqtasining (x, y) qaysi o'qda yoki koordinata choragida joylashganini aniqlang.

## Yechim (Rust kodi):
```rust
fn main() {
    let nuqta = (0, 5);

    match nuqta {
        (0, 0) => println!("Koordinata boshida"),
        (0, y) => println!("Y o'qida, y = {}", y),
        (x, 0) => println!("X o'qida, x = {}", x),
        (x, y) => println!("Chorakda: ({}, {})", x, y),
    }
}
```

## Tushuntirish va Mantiq:
`match` bitta amalda ham kortejni qismlarga ajratadi (destructure), ham ma'lum qiymatlarni (masalan, 0) filtrlaydi.

## Ishlash natijasi:
```text
Y o'qida, y = 5
```

---

# 78-Topshiriq: @ bog'lash operatori (Binding Operator) match patternida
## Topshiriq sharti:
Oraliqni tekshirgan holda, unga tushgan aniq qiymatni alohida o'zgaruvchiga bog'lab oling.

## Yechim (Rust kodi):
```rust
fn main() {
    let id = 15;

    match id {
        raqam @ 1..=10 => println!("Birinchi o'nlikdagi ID: {}", raqam),
        raqam @ 11..=20 => println!("Ikkinchi o'nlikdagi ID: {}", raqam),
        boshqa => println!("Katta ID: {}", boshqa),
    }
}
```

## Tushuntirish va Mantiq:
`o'zgaruvchi @ oraliq` sintaksisi qiymat oraliqqa to'g'ri kelganda, aynan o'sha qiymatni o'zgaruvchida saqlab qolish imkonini beradi.

## Ishlash natijasi:
```text
Ikkinchi o'nlikdagi ID: 15
```

---

# 79-Topshiriq: if let sintaksisi: Yagona variantni qulay tekshirish
## Topshiriq sharti:
Faqat bitta holat qiziq bo'lganda, to'liq `match` o'rniga `if let` dan foydalaning.

## Yechim (Rust kodi):
```rust
fn main() {
    let ixtiyoriy_son: Option<i32> = Some(42);

    if let Some(qiymat) = ixtiyoriy_son {
        println!("Muvaffaqiyatli qiymat olindi: {}", qiymat);
    }
}
```

## Tushuntirish va Mantiq:
`if let` berilgan pattern mos kelsa blokni bajaradi. Bu bitta holat uchun to'liq `match ... _ => ()` yozish zaruratini yo'qotadi.

## Ishlash natijasi:
```text
Muvaffaqiyatli qiymat olindi: 42
```

---

# 80-Topshiriq: if let ... else kombinatsiyasi
## Topshiriq sharti:
`if let` bilan birga `else` blokini qo'llang.

## Yechim (Rust kodi):
```rust
fn main() {
    let variant: Option<&str> = None;

    if let Some(matn) = variant {
        println!("Matn mavjud: {}", matn);
    } else {
        println!("Hech qanday ma'lumot topilmadi.");
    }
}
```

## Tushuntirish va Mantiq:
`if let ... else` shartli konstruksiyasi pattern mos kelmaganda muqobil harakatni belgilash imkonini beradi.

## Ishlash natijasi:
```text
Hech qanday ma'lumot topilmadi.
```

---

# 81-Topshiriq: while let sintaksisi: Pattern mos kelguncha tsiklni davom ettirish
## Topshiriq sharti:
Vektor oxiridan elementlarni bittalab sug'urib olishda `while let` dan foydalaning.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut navbat = vec![1, 2, 3];

    while let Some(element) = navbat.pop() {
        println!("Navbatdan olindi: {}", element);
    }
}
```

## Tushuntirish va Mantiq:
`while let` har safar yangi qiymatni pattern bilan solishtiradi. `.pop()` oxir-oqibat `None` qaytarganda, tsikl avtomatik to'xtaydi.

## Ishlash natijasi:
```text
Navbatdan olindi: 3
Navbatdan olindi: 2
Navbatdan olindi: 1
```

---

# 82-Topshiriq: let else konstruksiyasi (Guard Clause uslubida erta chiqish)
## Topshiriq sharti:
Rust 2021/2024 ning yangi `let Some(x) = opt else { return; };` imkoniyatini qo'llang.

## Yechim (Rust kodi):
```rust
fn asosiy_tekshiruv(qiymat: Option<i32>) {
    let Some(son) = qiymat else {
        println!("Qiymat mavjud emas, funksiyadan chiqamiz!");
        return;
    };

    println!("Hisoblangan kvadrat: {}", son * son);
}

fn main() {
    asosiy_tekshiruv(None);
    asosiy_tekshiruv(Some(7));
}
```

## Tushuntirish va Mantiq:
`let else` konstruksiyasi pattern mos kelmasa darhol `diverge` qiluvchi (`return`, `break` yoki `panic`) blokni ishga tushiradi. Bu ichma-ichlikni keskin kamaytiradi.

## Ishlash natijasi:
```text
Qiymat mavjud emas, funksiyadan chiqamiz!
Hisoblangan kvadrat: 49
```

---

# 83-Topshiriq: Tub sonni aniqlash algoritmi
## Topshiriq sharti:
Berilgan butun sonning tub (faqat 1 ga va o'ziga bo'linadigan) ekanligini loop yordamida aniqlang.

## Yechim (Rust kodi):
```rust
fn main() {
    let son = 29;
    let mut tub = son > 1;
    let mut i = 2;

    while i * i <= son {
        if son % i == 0 {
            tub = false;
            break;
        }
        i += 1;
    }

    println!("{} soni tubmi: {}", son, tub);
}
```

## Tushuntirish va Mantiq:
Tublikni tekshirishda sonning kvadrat ildizigacha (`i * i <= son`) tekshirish O(sqrt(N)) yetarlidir, bu hisoblash vaqtini tejaydi.

## Ishlash natijasi:
```text
29 soni tubmi: true
```

---

# 84-Topshiriq: 1 dan N gacha bo'lgan barcha tub sonlarni ekranga chiqarish
## Topshiriq sharti:
1 dan 30 gacha bo'lgan tub sonlar ro'yxatini for tsikllari orqali toping.

## Yechim (Rust kodi):
```rust
fn main() {
    print!("Tub sonlar (1..30): ");
    for n in 2..=30 {
        let mut tub = true;
        for d in 2..n {
            if n % d == 0 {
                tub = false;
                break;
            }
        }
        if tub {
            print!("{} ", n);
        }
    }
    println!();
}
```

## Tushuntirish va Mantiq:
Ichma-ich for tsikllari yordamida har bir son barcha mumkin bo'lgan bo'luvchilarga tekshirilib, tublari saralab olinadi.

## Ishlash natijasi:
```text
Tub sonlar (1..30): 2 3 5 7 11 13 17 19 23 29 
```

---

# 85-Topshiriq: Faktorial hisoblash va katta sonlar chegarasi
## Topshiriq sharti:
Berilgan N sonining faktorialini (N!) for tsiklida `u64` yordamida hisoblang.

## Yechim (Rust kodi):
```rust
fn main() {
    let n = 10;
    let mut faktorial: u64 = 1;

    for i in 1..=n {
        faktorial *= i;
    }

    println!("{}! = {}", n, faktorial);
}
```

## Tushuntirish va Mantiq:
Faktorial geometrik tezlikda o'sadi. `u64` turi 20! gacha bo'lgan qiymatlarni sig'dira oladi, undan yuqorisi uchun `u128` yoki maxsus BigInt talab etiladi.

## Ishlash natijasi:
```text
10! = 3628800
```

---

# 86-Topshiriq: Fibonachchi ketma-ketligining N-hadini topish
## Topshiriq sharti:
Iterativ usulda Fibonachchi ketma-ketligining dastlabki 10 ta hadini chiqaring.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut a = 0;
    let mut b = 1;

    print!("Fibonachchi: ");
    for _ in 0..10 {
        print!("{} ", a);
        let keyingi = a + b;
        a = b;
        b = keyingi;
    }
    println!();
}
```

## Tushuntirish va Mantiq:
Iterativ yondashuv rekursiyaga nisbatan xotirani tejaydi (O(1) xotira) va ortiqcha Stack to'lib ketishining (Stack overflow) oldini oladi.

## Ishlash natijasi:
```text
Fibonachchi: 0 1 1 2 3 5 8 13 21 34 
```

---

# 87-Topshiriq: Evklid algoritmi: Eng Katta Umumiy Bo'luvchi (EKUB)
## Topshiriq sharti:
Ikkita sonning EKUB qiymatini qoldiqli bo'lish usuli bilan toping.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut a = 48;
    let mut b = 18;

    while b != 0 {
        let qoldiq = a % b;
        a = b;
        b = qoldiq;
    }

    println!("EKUB: {}", a);
}
```

## Tushuntirish va Mantiq:
Evklid algoritmi qadimgi va eng samarali algoritmlardan biridir. Har qadamda `(a, b) = (b, a % b)` almashtiriladi.

## Ishlash natijasi:
```text
EKUB: 6
```

---

# 88-Topshiriq: Eng Kichik Umumiy Karrali (EKUK) hisoblash
## Topshiriq sharti:
EKUB orqali ikkita sonning EKUK qiymatini hisoblang: `EKUK(a, b) = (a * b) / EKUB(a, b)`.

## Yechim (Rust kodi):
```rust
fn main() {
    let son1 = 12;
    let son2 = 18;

    let mut a = son1;
    let mut b = son2;
    while b != 0 {
        let temp = b;
        b = a % b;
        a = temp;
    }
    let ekub = a;
    let ekuk = (son1 * son2) / ekub;

    println!("EKUK({}, {}) = {}", son1, son2, ekuk);
}
```

## Tushuntirish va Mantiq:
EKUB topilgandan so'ng, ikki sonning ko'paytmasini EKUB ga bo'lish orqali ularning eng kichik umumiy karralisi osonlik bilan topiladi.

## Ishlash natijasi:
```text
EKUK(12, 18) = 36
```

---

# 89-Topshiriq: Palindrom sonni aniqlash (Raqamlarni teskari qilish)
## Topshiriq sharti:
Berilgan sonning teskari o'qilganda ham bir xil ekanligini while tsikli bilan tekshiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let asl_son = 12321;
    let mut temp = asl_son;
    let mut teskari = 0;

    while temp > 0 {
        let raqam = temp % 10;
        teskari = teskari * 10 + raqam;
        temp /= 10;
    }

    if asl_son == teskari {
        println!("{} - palindrom son!", asl_son);
    } else {
        println!("{} - oddiy son.", asl_son);
    }
}
```

## Tushuntirish va Mantiq:
Sonni 10 ga bo'lib oxirgi raqamini olish va uni 10 ga ko'paytirilgan yangi songa qo'shish orqali butun son matematik teskari qilinadi.

## Ishlash natijasi:
```text
12321 - palindrom son!
```

---

# 90-Topshiriq: Sonning barcha raqamlari yig'indisini hisoblash
## Topshiriq sharti:
Berilgan butun sonning har bir raqamini ajratib olib, ularning yig'indisini toping.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut son = 9845;
    let mut yigindi = 0;

    while son > 0 {
        yigindi += son % 10;
        son /= 10;
    }

    println!("Raqamlar yig'indisi: {}", yigindi);
}
```

## Tushuntirish va Mantiq:
`son % 10` oxirgi raqamni ajratadi, `son /= 10` esa oxirgi raqamni o'chiradi. Bu jarayon son 0 ga teng bo'lguncha davom etadi.

## Ishlash natijasi:
```text
Raqamlar yig'indisi: 26
```

---

# 91-Topshiriq: Armstrong sonini aniqlash
## Topshiriq sharti:
Raqamlari kublarining yig'indisi o'ziga teng bo'lgan 3 xonali sonni (masalan 153) tekshiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let son = 153;
    let mut temp = son;
    let mut yigindi = 0;

    while temp > 0 {
        let r = temp % 10;
        yigindi += r * r * r;
        temp /= 10;
    }

    println!("{} Armstrong sonimi: {}", son, yigindi == son);
}
```

## Tushuntirish va Mantiq:
153 = 1^3 + 5^3 + 3^3 = 1 + 125 + 27 = 153. Sharti to'liq bajarilgani uchun bu Armstrong soni hisoblanadi.

## Ishlash natijasi:
```text
153 Armstrong sonimi: true
```

---

# 92-Topshiriq: Mukammal sonni aniqlash (Bo'luvchilari yig'indisi)
## Topshiriq sharti:
O'zidan tashqari barcha bo'luvchilari yig'indisi o'ziga teng bo'lgan sonni (masalan 28) tekshiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let son = 28;
    let mut boluvchilar_yigindisi = 0;

    for i in 1..son {
        if son % i == 0 {
            boluvchilar_yigindisi += i;
        }
    }

    println!("{} mukammal sonmi: {}", son, boluvchilar_yigindisi == son);
}
```

## Tushuntirish va Mantiq:
28 ning bo'luvchilari: 1, 2, 4, 7, 14. Yig'indisi: 1+2+4+7+14 = 28. Demak, 28 mukammal son hisoblanadi.

## Ishlash natijasi:
```text
28 mukammal sonmi: true
```

---

# 93-Topshiriq: Karra jadvalini ichma-ich for tsikllari orqali chiqarish
## Topshiriq sharti:
1 dan 5 gacha sonlar uchun ko'paytirish jadvalini tekis ustunlar bilan chiqaring.

## Yechim (Rust kodi):
```rust
fn main() {
    for i in 1..=5 {
        for j in 1..=5 {
            print!("{:3} ", i * j);
        }
        println!();
    }
}
```

## Tushuntirish va Mantiq:
Ichma-ich `for` tsikllari matritsasimon jadvallarni chiqarishda asosiy vosita hisoblanadi. `{:3}` har bir songa 3 katak joy ajratadi.

## Ishlash natijasi:
```text
  1   2   3   4   5 
  2   4   6   8  10 
  3   6   9  12  15 
  4   8  12  16  20 
  5  10  15  20  25 
```

---

# 94-Topshiriq: Yulduzchalar yordamida to'g'ri burchakli uchburchak chizish
## Topshiriq sharti:
N qatordan iborat o'suvchi yulduzcha naqshini konsolga chiqaring.

## Yechim (Rust kodi):
```rust
fn main() {
    let qatorlar = 5;

    for i in 1..=qatorlar {
        for _ in 0..i {
            print!("*");
        }
        println!();
    }
}
```

## Tushuntirish va Mantiq:
Tashqi tsikl qatorlarni, ichki tsikl esa har bir qatordagi yulduzchalar sonini boshqaradi.

## Ishlash natijasi:
```text
*
**
***
****
*****
```

---

# 95-Topshiriq: Piramida shaklini bo'shliqlar va yulduzchalar bilan chizish
## Topshiriq sharti:
Markazga tekislangan simmetrik piramidani konsolda hosil qiling.

## Yechim (Rust kodi):
```rust
fn main() {
    let balandlik = 4;

    for i in 1..=balandlik {
        for _ in 0..(balandlik - i) {
            print!(" ");
        }
        for _ in 0..(2 * i - 1) {
            print!("*");
        }
        println!();
    }
}
```

## Tushuntirish va Mantiq:
Piramida hosil qilish uchun avval chap tomonga `balandlik - i` ta bo'shliq, so'ngra `2 * i - 1` ta yulduzcha chiqariladi.

## Ishlash natijasi:
```text
   *
  ***
 *****
*******
```

---

# 96-Topshiriq: Massivdagi eng katta va eng kichik elementni bitta siklda topish
## Topshiriq sharti:
Sonlar to'plamidagi minimum va maksimum qiymatni for tsikli orqali aniqlang.

## Yechim (Rust kodi):
```rust
fn main() {
    let sonlar = [45, 12, 89, 7, 63, 102, 34];
    let mut min = sonlar[0];
    let mut max = sonlar[0];

    for &son in &sonlar[1..] {
        if son < min {
            min = son;
        }
        if son > max {
            max = son;
        }
    }

    println!("Minimum: {}, Maksimum: {}", min, max);
}
```

## Tushuntirish va Mantiq:
Bitta siklda ham minimum, ham maksimum aniqlanishi operatsiyalar sonini O(N) ga qisqartiradi.

## Ishlash natijasi:
```text
Minimum: 7, Maksimum: 102
```

---

# 97-Topshiriq: Massiv elementlarining o'rtacha arifmetik qiymatini hisoblash
## Topshiriq sharti:
Butun sonli massiv elementlari yig'indisini topib, uni aniq float shaklida chiqaring.

## Yechim (Rust kodi):
```rust
fn main() {
    let baholar = [80, 95, 70, 85, 90];
    let mut yigindi = 0;

    for &baho in &baholar {
        yigindi += baho;
    }

    let ortacha = (yigindi as f64) / (baholar.len() as f64);
    println!("O'rtacha ball: {:.2}", ortacha);
}
```

## Tushuntirish va Mantiq:
Yig'indini sonlar miqdoriga bo'lishdan oldin ikkala tomonni ham `f64` ga o'tkazish aniq o'nlik kasrli natijani kafolatlaydi.

## Ishlash natijasi:
```text
O'rtacha ball: 84.00
```

---

# 98-Topshiriq: Chiziqli qidiruv (Linear Search) algoritmi
## Topshiriq sharti:
Massiv ichidan qidirilayotgan sonning indeksini topuvchi tsikl tuzing.

## Yechim (Rust kodi):
```rust
fn main() {
    let royxat = [14, 52, 33, 84, 95, 26];
    let qidirilayotgan = 84;
    let mut topilgan_indeks: Option<usize> = None;

    for (i, &element) in royxat.iter().enumerate() {
        if element == qidirilayotgan {
            topilgan_indeks = Some(i);
            break;
        }
    }

    match topilgan_indeks {
        Some(idx) => println!("{} soni {}-indeksda topildi.", qidirilayotgan, idx),
        None => println!("Qidirilgan son topilmadi."),
    }
}
```

## Tushuntirish va Mantiq:
Chiziqli qidiruv har bir elementni ketma-ket solishtiradi. Element topilishi bilan `break` orqali tsikldan erta chiqiladi.

## Ishlash natijasi:
```text
84 soni 3-indeksda topildi.
```

---

# 99-Topshiriq: Binar qidiruv (Binary Search) algoritmi
## Topshiriq sharti:
Saralangan massivda logarifmik tezlikda (O(log N)) sonni topish algoritmini amalga oshiring.

## Yechim (Rust kodi):
```rust
fn main() {
    let saralangan = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91];
    let nishon = 23;

    let mut chap: usize = 0;
    let mut ong: usize = saralangan.len() - 1;
    let mut topildi = false;

    while chap <= ong {
        let orta = chap + (ong - chap) / 2;
        if saralangan[orta] == nishon {
            println!("Nishon {} {}-indeksda topildi!", nishon, orta);
            topildi = true;
            break;
        } else if saralangan[orta] < nishon {
            chap = orta + 1;
        } else {
            if orta == 0 { break; }
            ong = orta - 1;
        }
    }

    if !topildi {
        println!("Element topilmadi.");
    }
}
```

## Tushuntirish va Mantiq:
Binar qidiruv har qadamda qidiruv hududini teng ikkiga qisqartiradi. `orta = chap + (ong - chap)/2` formulasi butun son to'lib ketishining oldini oladi.

## Ishlash natijasi:
```text
Nishon 23 5-indeksda topildi!
```

---

# 100-Topshiriq: Kollats gipotezasi (Collatz Conjecture / 3n + 1 muammosi)
## Topshiriq sharti:
Son juft bo'lsa 2 ga bo'linadi, toq bo'lsa 3n+1 qilinadi. Son 1 ga yetguncha qadamlar sonini hisoblang.

## Yechim (Rust kodi):
```rust
fn main() {
    let mut n: u64 = 27;
    let mut qadamlar = 0;

    print!("Kollats zanjiri boshlanishi (27): ");
    while n != 1 {
        if n % 2 == 0 {
            n /= 2;
        } else {
            n = 3 * n + 1;
        }
        qadamlar += 1;
    }

    println!("1 ga yetib keldi. Jami qadamlar soni: {}", qadamlar);
}
```

## Tushuntirish va Mantiq:
Kollats muammosi matematikadagi eng mashhur ochiq masalalardan biridir. Har qanday musbat sondan boshlanganda zanjir oxir-oqibat 1 ga borib taqaladi.

## Ishlash natijasi:
```text
Kollats zanjiri boshlanishi (27): 1 ga yetib keldi. Jami qadamlar soni: 111
```

---
