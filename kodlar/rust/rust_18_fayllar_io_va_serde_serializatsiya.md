# Rust Dasturlash Tili: Fayllar, I/O va Serde Serializatsiya

Ushbu modulda Rust'da fayllar bilan ishlash (`std::fs`), buferlangan o'qish/yozish (`BufReader`, `BufWriter`), oqimlar (`Cursor`, `Seek`), yo'llar (`Path`, `PathBuf`), standart kiritish/chiqarish (`stdin`, `stdout`, `stderr`), hamda Serde serializatsiya va ma'lumot formatlari (JSON, CSV, Binar) amaliy topshiriqlarda to'liq qamrab olingan.

---

# 851-Topshiriq: std::fs::File::create va write_all bilan yangi faylga matn yozish
## Topshiriq sharti:
Fayl yaratish va unga `io::Write` trait'ining `write_all` metodi yordamida baytlar yozish dasturini tuzing.
## Yechim (Rust kodi):
```rust
use std::fs::File;
use std::io::Write;

fn main() -> std::io::Result<()> {
    let mut fayl = File::create("namuna.txt")?;
    fayl.write_all(b"Rust tili bilan fayllarga yozish juda oson!\n")?;
    println!("Fayl muvaffaqiyatli yaratildi va matn yozildi.");
    Ok(())
}
```
## Tushuntirish va Mantiq:
`File::create` ko'rsatilgan nomda yangi fayl ochadi (agar mavjud bo'lsa, tozalaydi). `write_all` barcha baytlar to'liq yozilishini kafolatlaydi.
## Ishlash natijasi:
```text
Fayl muvaffaqiyatli yaratildi va matn yozildi.
```

---

# 852-Topshiriq: std::fs::read_to_string orqali butun faylni bitta String'ga o'qish
## Topshiriq sharti:
Diskdagi mavjud fayl tarkibini bir qatorda to'liq o'qib ekranga chiqaruvchi kod yozing.
## Yechim (Rust kodi):
```rust
use std::fs;

fn main() -> std::io::Result<()> {
    fs::write("salom.txt", "Assalomu alaykum, Rust dasturchisi!")?;

    let matn = fs::read_to_string("salom.txt")?;
    println!("Fayldan o'qilgan matn: {}", matn);

    fs::remove_file("salom.txt")?;
    Ok(())
}
```
## Tushuntirish va Mantiq:
`fs::read_to_string` faylni to'liq UTF-8 matn sifatida o'qiydi. Agar matn noto'g'ri UTF-8 bo'lsa, `InvalidData` xatoligi qaytariladi.
## Ishlash natijasi:
```text
Fayldan o'qilgan matn: Assalomu alaykum, Rust dasturchisi!
```

---

# 853-Topshiriq: std::fs::read orqali faylni baytlar massivi (Vec<u8>) sifatida o'qish
## Topshiriq sharti:
Ixtiyoriy binar faylni baytlar to'plami sifatida o'qib uning hajmini va dastlabki baytlarini chop eting.
## Yechim (Rust kodi):
```rust
use std::fs;

fn main() -> std::io::Result<()> {
    let ma_lumot = vec![0xDE, 0xAD, 0xBE, 0xEF, 0x01, 0x02];
    fs::write("binar.dat", &ma_lumot)?;

    let baytlar = fs::read("binar.dat")?;
    println!("O'qilgan baytlar soni: {}", baytlar.len());
    println!("Baytlar (hex): {:X?}", baytlar);

    fs::remove_file("binar.dat")?;
    Ok(())
}
```
## Tushuntirish va Mantiq:
`fs::read` rasmlar, audio va binar ma'lumotlarni hech qanday matnli o'zgartirishlarsiz xom baytlar (`Vec<u8>`) ko'rinishida xotiraga yuklaydi.
## Ishlash natijasi:
```text
O'qilgan baytlar soni: 6
Baytlar (hex): [DE, AD, BE, EF, 1, 2]
```

---

# 854-Topshiriq: std::fs::OpenOptions: Faylga ma'lumot qo'shish (Append mode)
## Topshiriq sharti:
Mavjud fayl oxiriga yangi qator qo'shish uchun `OpenOptions::new().append(true)` dan foydalaning.
## Yechim (Rust kodi):
```rust
use std::fs::OpenOptions;
use std::io::Write;

fn main() -> std::io::Result<()> {
    let mut fayl = OpenOptions::new()
        .create(true)
        .append(true)
        .open("log.txt")?;

    writeln!(fayl, "[LOG]: Yangi hodisa qayd etildi.")?;
    println!("Yangi qator fayl oxiriga qo'shildi.");
    std::fs::remove_file("log.txt")?;
    Ok(())
}
```
## Tushuntirish va Mantiq:
`OpenOptions` faylni ochish rejimlarini (read, write, append, truncate, create) nozik sozlash imkonini beradi.
## Ishlash natijasi:
```text
Yangi qator fayl oxiriga qo'shildi.
```

---

# 855-Topshiriq: OpenOptions bayroqlari: create_new va truncate
## Topshiriq sharti:
Fayl allaqachon mavjud bo'lsa xato berishi kerak bo'lganda `create_new(true)` qanday ishlashini ko'rsating.
## Yechim (Rust kodi):
```rust
use std::fs::OpenOptions;

fn main() {
    let _ = std::fs::write("mavjud.txt", "test");

    let natija = OpenOptions::new()
        .write(true)
        .create_new(true) // Fayl mavjud bo'lsa xato beradi!
        .open("mavjud.txt");

    match natija {
        Ok(_) => println!("Yangi fayl yaratildi"),
        Err(e) => println!("Kutilgan xatolik: fayl allaqachon mavjud ({})", e.kind()),
    }

    let _ = std::fs::remove_file("mavjud.txt");
}
```
## Tushuntirish va Mantiq:
`create_new(true)` fayl allaqachon mavjud bo'lsa uni ustidan yozib yuborishning oldini oladi (Atomik xavfsizlik).
## Ishlash natijasi:
```text
Kutilgan xatolik: fayl allaqachon mavjud (AlreadyExists)
```

---

# 856-Topshiriq: std::io::BufReader bilan katta faylni qatorma-qator o'qish
## Topshiriq sharti:
Katta hajmdagi faylni xotiraga to'liq yuklamasdan `BufReader` va `lines()` yordamida tejamkor o'qing.
## Yechim (Rust kodi):
```rust
use std::fs::File;
use std::io::{BufRead, BufReader, Write};

fn main() -> std::io::Result<()> {
    {
        let mut f = File::create("royxat.txt")?;
        writeln!(f, "1-qator: Alisher")?;
        writeln!(f, "2-qator: Bobur")?;
        writeln!(f, "3-qator: Nodira")?;
    }

    let fayl = File::open("royxat.txt")?;
    let reader = BufReader::new(fayl);

    for (indeks, qator) in reader.lines().enumerate() {
        println!("{}: {}", indeks + 1, qator?);
    }

    std::fs::remove_file("royxat.txt")?;
    Ok(())
}
```
## Tushuntirish va Mantiq:
`BufReader` tizimdan bir necha kilobaytlik bloklarda o'qiydi va diskka bo'ladigan murojaatlar sonini minglab baravarga kamaytiradi.
## Ishlash natijasi:
```text
1: 1-qator: Alisher
2: 2-qator: Bobur
3: 3-qator: Nodira
```

---

# 857-Topshiriq: std::io::BufWriter bilan buferlangan yozish va flush()
## Topshiriq sharti:
Ko'p marta kichik yozish amallarini `BufWriter`da to'plab keyin yozish.
## Yechim (Rust kodi):
```rust
use std::fs::File;
use std::io::{BufWriter, Write};

fn main() -> std::io::Result<()> {
    let fayl = File::create("bufer_test.txt")?;
    let mut writer = BufWriter::new(fayl);

    for i in 1..=3 {
        write!(writer, "Element #{}\n", i)?;
    }

    writer.flush()?; // Buferni diskka majburiy to'kib tashlash
    println!("Buferlangan ma'lumotlar diskka to'liq yozildi.");

    std::fs::remove_file("bufer_test.txt")?;
    Ok(())
}
```
## Tushuntirish va Mantiq:
`BufWriter` xotira buferi to'lgandagina diskka yozadi. `flush()` esa kutmasdan darhol diskka yozishni talab qiladi.
## Ishlash natijasi:
```text
Buferlangan ma'lumotlar diskka to'liq yozildi.
```

---

# 858-Topshiriq: std::io::Seek va SeekFrom: Fayl ichida ko'rsatkichni siljitish
## Topshiriq sharti:
Faylning ma'lum bir bayt offsetiga sakrab o'tish dasturini yozing.
## Yechim (Rust kodi):
```rust
use std::fs::File;
use std::io::{Read, Seek, SeekFrom, Write};

fn main() -> std::io::Result<()> {
    let mut fayl = File::create("seek_test.bin")?;
    fayl.write_all(b"0123456789ABCDEF")?;

    let mut fayl = File::open("seek_test.bin")?;
    // Boshidan 10-baytga sakraymiz
    fayl.seek(SeekFrom::Start(10))?;

    let mut bufer = [0u8; 4];
    fayl.read_exact(&mut bufer)?;
    println!("O'qilgan 4 bayt: {:?}", std::str::from_utf8(&bufer).unwrap());

    std::fs::remove_file("seek_test.bin")?;
    Ok(())
}
```
## Tushuntirish va Mantiq:
`Seek` trait'i `SeekFrom::Start(N)`, `SeekFrom::Current(N)` va `SeekFrom::End(N)` orqali faylning ixtiyoriy nuqtasiga tasodifiy murojaat (random access) beradi.
## Ishlash natijasi:
```text
O'qilgan 4 bayt: "ABCD"
```

---

# 859-Topshiriq: std::fs::copy orqali fayldan nusxa olish
## Topshiriq sharti:
Mavjud faylni yangi nom bilan nusxalash va ko'chirilgan baytlar sonini aniqlash.
## Yechim (Rust kodi):
```rust
use std::fs;

fn main() -> std::io::Result<()> {
    fs::write("asl.txt", "Ushbu ma'lumot nusxalanadi.")?;

    let nusxa_baytlar = fs::copy("asl.txt", "nusxa.txt")?;
    println!("Nusxalandi: {} bayt", nusxa_baytlar);

    let nusxa_matn = fs::read_to_string("nusxa.txt")?;
    println!("Nusxa tarkibi: {}", nusxa_matn);

    fs::remove_file("asl.txt")?;
    fs::remove_file("nusxa.txt")?;
    Ok(())
}
```
## Tushuntirish va Mantiq:
`fs::copy` operatsion tizimning optimallashtirilgan nusxalash mexanizmidan foydalanadi va ko'chirilgan bayt hajmini qaytaradi.
## Ishlash natijasi:
```text
Nusxalandi: 28 bayt
Nusxa tarkibi: Ushbu ma'lumot nusxalanadi.
```

---

# 860-Topshiriq: std::fs::rename orqali fayl nomini o'zgartirish
## Topshiriq sharti:
Fayl nomini 'eski.txt' dan 'yangi.txt' ga o'zgartirish dasturini yozing.
## Yechim (Rust kodi):
```rust
use std::fs;

fn main() -> std::io::Result<()> {
    fs::write("eski.txt", "Nom o'zgarishi kerak bo'lgan fayl")?;

    fs::rename("eski.txt", "yangi.txt")?;
    println!("Fayl nomi muvaffaqiyatli yangilandi: 'yangi.txt'");

    assert!(fs::metadata("yangi.txt").is_ok());
    assert!(fs::metadata("eski.txt").is_err());

    fs::remove_file("yangi.txt")?;
    Ok(())
}
```
## Tushuntirish va Mantiq:
`fs::rename` fayl tizimi darajasida atomik amal bo'lib, fayl tarkibini ko'chirmasdan uning yo'lini yoki nomini o'zgartiradi.
## Ishlash natijasi:
```text
Fayl nomi muvaffaqiyatli yangilandi: 'yangi.txt'
```

---

# 861-Topshiriq: std::fs::remove_file orqali faylni o'chirish
## Topshiriq sharti:
Yaratilgan faylni diskdan to'liq tozalash va tekshirish.
## Yechim (Rust kodi):
```rust
use std::fs;

fn main() -> std::io::Result<()> {
    fs::write("ochiriladigan.txt", "Vaqtinchalik ma'lumot")?;
    println!("Fayl mavjud: {}", std::path::Path::new("ochiriladigan.txt").exists());

    fs::remove_file("ochiriladigan.txt")?;
    println!("O'chirilgandan so'ng mavjud: {}", std::path::Path::new("ochiriladigan.txt").exists());
    Ok(())
}
```
## Tushuntirish va Mantiq:
`fs::remove_file` fayl linkini bekor qiladi va uning egallagan bloklarini bo'shatadi.
## Ishlash natijasi:
```text
Fayl mavjud: true
O'chirilgandan so'ng mavjud: false
```

---

# 862-Topshiriq: std::fs::create_dir_all bilan zanjirli papkalar yaratish
## Topshiriq sharti:
Bir nechta ichma-ich joylashgan papkalarni (masalan, `ota/bola/nevara`) bitta buyruq bilan yaratish.
## Yechim (Rust kodi):
```rust
use std::fs;

fn main() -> std::io::Result<()> {
    let yol = "ota_papka/bola_papka/nevara_papka";
    fs::create_dir_all(yol)?;

    println!("Zanjirli papkalar yaratildi: {}", yol);
    assert!(fs::metadata(yol)?.is_dir());

    fs::remove_dir_all("ota_papka")?;
    Ok(())
}
```
## Tushuntirish va Mantiq:
`create_dir_all` mavjud bo'lmagan barcha oraliq ota papkalarni avtomatik ravishda yaratadi (Unix `mkdir -p` kabi).
## Ishlash natijasi:
```text
Zanjirli papkalar yaratildi: ota_papka/bola_papka/nevara_papka
```

---

# 863-Topshiriq: std::fs::read_dir orqali papka ichidagi fayllarni ko'rish
## Topshiriq sharti:
Papka ichidagi barcha fayl va pastki papkalar ro'yxatini chiqaruvchi kod tuzing.
## Yechim (Rust kodi):
```rust
use std::fs;

fn main() -> std::io::Result<()> {
    let papka = "test_katalog";
    fs::create_dir(papka)?;
    fs::write(format!("{}/f1.txt", papka), "A")?;
    fs::write(format!("{}/f2.txt", papka), "B")?;

    println!("'{}' papkasi tarkibi:", papka);
    for entry in fs::read_dir(papka)? {
        let entry = entry?;
        println!(" - {:?}", entry.file_name());
    }

    fs::remove_dir_all(papka)?;
    Ok(())
}
```
## Tushuntirish va Mantiq:
`read_dir` katalog bo'ylab iteratsiya qiladi va har bir element uchun `DirEntry` obyektini qaytaradi.
## Ishlash natijasi:
```text
'test_katalog' papkasi tarkibi:
 - "f1.txt"
 - "f2.txt"
```

---

# 864-Topshiriq: DirEntry va fs::Metadata: Fayl hajmi va xususiyatlarini olish
## Topshiriq sharti:
Fayl hajmi, u faylmi yoki papkami, va ruxsatnomalarini aniqlash.
## Yechim (Rust kodi):
```rust
use std::fs;

fn main() -> std::io::Result<()> {
    fs::write("meta.txt", "Rust xavfsiz va tezkor til.")?;

    let meta = fs::metadata("meta.txt")?;
    println!("Fayl hajmi:     {} bayt", meta.len());
    println!("Bu oddiy faylmi: {}", meta.is_file());
    println!("Bu katalogmi:    {}", meta.is_dir());
    println!("Faqat o'qishmi:  {}", meta.permissions().readonly());

    fs::remove_file("meta.txt")?;
    Ok(())
}
```
## Tushuntirish va Mantiq:
`fs::metadata` fayl tizimidan fayl haqidagi to'liq meta-ma'lumotlarni operatsion tizim darajasida olib beradi.
## Ishlash natijasi:
```text
Fayl hajmi:     29 bayt
Bu oddiy faylmi: true
Bu katalogmi:    false
Faqat o'qishmi:  false
```

---

# 865-Topshiriq: std::fs::remove_dir_all bilan papkani to'liq tozalash
## Topshiriq sharti:
Ichida fayllari bo'lgan papkani butunlay o'chirish.
## Yechim (Rust kodi):
```rust
use std::fs;

fn main() -> std::io::Result<()> {
    let papka = "tozalanadigan_papka";
    fs::create_dir(papka)?;
    fs::write(format!("{}/fayl.txt", papka), "123")?;

    fs::remove_dir_all(papka)?;
    println!("Papka va barcha ichki fayllar xavfsiz o'chirildi.");
    Ok(())
}
```
## Tushuntirish va Mantiq:
`remove_dir_all` papka bo'sh bo'lmasa ham uni barcha ichki elementlari bilan birgalikda rekursiv o'chiradi.
## Ishlash natijasi:
```text
Papka va barcha ichki fayllar xavfsiz o'chirildi.
```

---

# 866-Topshiriq: std::path::Path va PathBuf bilan yo'llar yasash
## Topshiriq sharti:
`PathBuf` yordamida Windows (`\`) yoki Linux (`/`) separatorlarini hisobga olgan holda kross-platforma yo'l yasash.
## Yechim (Rust kodi):
```rust
use std::path::PathBuf;

fn main() {
    let mut yol = PathBuf::new();
    yol.push("loyiha");
    yol.push("src");
    yol.push("main.rs");

    println!("Yasalgan yo'l: {:?}", yol);
}
```
## Tushuntirish va Mantiq:
`PathBuf` o'zgaruvchan (owned) fayl yo'li bo'lib, tizimga mos ajratgichlarni (`/` yoki `\`) o'zi to'g'ri joylashtiradi.
## Ishlash natijasi:
```text
Yasalgan yo'l: "loyiha/src/main.rs"
```

---

# 867-Topshiriq: Path metodlari: parent, file_name va extension
## Topshiriq sharti:
Fayl yo'lidan ota papka, fayl nomi va uning kengaytmasini (extension) ajratib olish.
## Yechim (Rust kodi):
```rust
use std::path::Path;

fn main() {
    let yol = Path::new("/var/log/tizim.tar.gz");

    println!("Ota papka:   {:?}", yol.parent());
    println!("Fayl nomi:   {:?}", yol.file_name());
    println!("Kengaytma:   {:?}", yol.extension());
}
```
## Tushuntirish va Mantiq:
`Path` tekshiruvlari matnni string sifatida parse qilishdan ancha xavfsiz va platformalararo muvofiqlikni kafolatlaydi.
## Ishlash natijasi:
```text
Ota papka:   Some("/var/log")
Fayl nomi:   Some("tizim.tar.gz")
Kengaytma:   Some("gz")
```

---

# 868-Topshiriq: Path::exists, is_file va is_dir tekshiruvlari
## Topshiriq sharti:
Ko'rsatilgan yo'l mavjudmi va uning turini tekshiruvchi funksiya yozing.
## Yechim (Rust kodi):
```rust
use std::path::Path;

fn tahlil_qil(yol_str: &str) {
    let p = Path::new(yol_str);
    println!("Yo'l: '{}'", yol_str);
    println!("  Mavjudmi: {}", p.exists());
    println!("  Faylmi:   {}", p.is_file());
    println!("  Papkami:  {}", p.is_dir());
}

fn main() {
    tahlil_qil(".");
    tahlil_qil("mavjud_emas_fayl.xyz");
}
```
## Tushuntirish va Mantiq:
`Path::exists()` fayl yoki katalogning diskda jismonan bor yoki yo'qligini tezkor tekshiradi.
## Ishlash natijasi:
```text
Yo'l: '.'
  Mavjudmi: true
  Faylmi:   false
  Papkami:  true
Yo'l: 'mavjud_emas_fayl.xyz'
  Mavjudmi: false
  Faylmi:   false
  Papkami:  false
```

---

# 869-Topshiriq: Standart kiritish: std::io::stdin().read_line
## Topshiriq sharti:
Konsoldan qatorni o'qib olish va probellardan tozalash tartibini ko'rsating.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Foydalanuvchidan ma'lumot olish kodi quyidagicha tuziladi:");
    println!(r#"
use std::io;

fn main() -> io::Result<()> {{
    let mut kiritilgan = String::new();
    println!("Ismingizni kiriting:");
    io::stdin().read_line(&mut kiritilgan)?;
    println!("Salom, {{}}!", kiritilgan.trim());
    Ok(())
}}
"#);
}
```
## Tushuntirish va Mantiq:
`stdin().read_line` kiritilgan satrni oxiridagi `\n` belgisi bilan birga String buferiga qo'shib yozadi.
## Ishlash natijasi:
```text
Foydalanuvchidan ma'lumot olish kodi quyidagicha tuziladi:

use std::io;

fn main() -> io::Result<()> {
    let mut kiritilgan = String::new();
    println!("Ismingizni kiriting:");
    io::stdin().read_line(&mut kiritilgan)?;
    println!("Salom, {}!", kiritilgan.trim());
    Ok(())
}
```

---

# 870-Topshiriq: std::io::stdout() va flush() bilan so'rov matnini chiqarish
## Topshiriq sharti:
`print!` makrosidan keyin qator yangilanmasa ham matn konsolda darhol chiqishi uchun `flush()` qilish.
## Yechim (Rust kodi):
```rust
use std::io::{self, Write};

fn main() -> io::Result<()> {
    print!("Yuklanmoqda... ");
    io::stdout().flush()?; // Terminal buferini darhol tozalab ekranga chiqaradi
    println!("[TAYYOR]");
    Ok(())
}
```
## Tushuntirish va Mantiq:
Konsol ko'pincha satr bo'yicha buferlanadi (line-buffered). `flush()` qilmaslik so'rov matnining kechikib chiqishiga olib kelishi mumkin.
## Ishlash natijasi:
```text
Yuklanmoqda... [TAYYOR]
```

---

# 871-Topshiriq: Standart xatolik oqimi: eprintln! va stderr
## Topshiriq sharti:
Oddiy ma'lumotlarni stdout ga, xatolik xabarlarini esa stderr ga ajratib yuborish.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Bu oddiy standart chiqish (stdout)");
    eprintln!("Bu esa xatoliklar oqimi (stderr)");
}
```
## Tushuntirish va Mantiq:
`eprintln!` xatolik xabarlarini alohida kanalga yo'naltiradi, bu esa Unix trubalari (`|`) va faylga yo'naltirishda (`>`) xatoliklarning asosiy ma'lumotga aralashib ketmasligini ta'minlaydi.
## Ishlash natijasi:
```text
Bu oddiy standart chiqish (stdout)
Bu esa xatoliklar oqimi (stderr)
```

---

# 872-Topshiriq: std::io::Cursor: Xotiradagi buferni fayl kabi o'qish va yozish
## Topshiriq sharti:
`Cursor<Vec<u8>>` yordamida diskka yozmasdan xotirada fayl oqimi amallarini bajarish.
## Yechim (Rust kodi):
```rust
use std::io::{Cursor, Read, Seek, SeekFrom, Write};

fn main() -> std::io::Result<()> {
    let mut oqim = Cursor::new(Vec::new());

    oqim.write_all(b"Salom Xotira!")?;
    oqim.seek(SeekFrom::Start(0))?;

    let mut matn = String::new();
    oqim.read_to_string(&mut matn)?;
    println!("Cursor orqali o'qildi: {}", matn);
    Ok(())
}
```
## Tushuntirish va Mantiq:
`Cursor` har qanday `AsRef<[u8]>` yoki `&mut Vec<u8>` ustida `Read`, `Write` va `Seek` trait'larini ishlatish imkonini beradi (Testlash uchun ayni muddao).
## Ishlash natijasi:
```text
Cursor orqali o'qildi: Salom Xotira!
```

---

# 873-Topshiriq: Custom I/O Stream Wrapper: Harf sanovchi Reader
## Topshiriq sharti:
O'qilgan har bir baytni sanab boruvchi maxsus `CountingReader` strukturasini yozing.
## Yechim (Rust kodi):
```rust
use std::io::{self, Read};

struct CountingReader<R> {
    ichki: R,
    hisob: usize,
}

impl<R: Read> CountingReader<R> {
    fn new(ichki: R) -> Self {
        CountingReader { ichki, hisob: 0 }
    }
}

impl<R: Read> Read for CountingReader<R> {
    fn read(&mut self, buf: &mut [u8]) -> io::Result<usize> {
        let n = self.ichki.read(buf)?;
        self.hisob += n;
        Ok(n)
    }
}

fn main() -> io::Result<()> {
    let manba = b"Rust 2024 I/O";
    let mut cr = CountingReader::new(&manba[..]);
    let mut bufer = [0u8; 100];
    let n = cr.read(&mut bufer)?;

    println!("O'qilgan matn: {}", std::str::from_utf8(&bufer[..n]).unwrap());
    println!("Jami o'qilgan baytlar soni: {}", cr.hisob);
    Ok(())
}
```
## Tushuntirish va Mantiq:
Rust I/O adapterlari bir-birining ustiga qatlam-qatlam o'ralishi (Decorator pattern) mumkin.
## Ishlash natijasi:
```text
O'qilgan matn: Rust 2024 I/O
Jami o'qilgan baytlar soni: 13
```

---

# 874-Topshiriq: Serde nima va uning ekotizimdagi o'rni
## Topshiriq sharti:
Serde (Serializer / Deserializer) asosiy tushunchalari va ma'lumotlar oqimini tushuntiring.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Serde falsafasi:");
    println!("1. Rust strukturasi -> [Serializer] -> JSON / YAML / TOML / Bincode");
    println!("2. JSON / Binar -> [Deserializer] -> Rust strukturasi");
    println!("3. Intermediate Representation (Data Model) yordamida har qanday tur har qanday formatga bog'lanadi.");
}
```
## Tushuntirish va Mantiq:
Serde deyarli barcha formatlarni qo'llab-quvvatlaydi va o'zining nol xarajatli (zero-cost) arxitekturasi bilan dunyodagi eng tez serializatsiya tizimlaridan biri hisoblanadi.
## Ishlash natijasi:
```text
Serde falsafasi:
1. Rust strukturasi -> [Serializer] -> JSON / YAML / TOML / Bincode
2. JSON / Binar -> [Deserializer] -> Rust strukturasi
3. Intermediate Representation (Data Model) yordamida har qanday tur har qanday formatga bog'lanadi.
```

---

# 875-Topshiriq: Serde Derive makrolari strukturasi
## Topshiriq sharti:
Strukturaga serializatsiya xususiyatini beruvchi atributlarni ko'rsating.
## Yechim (Rust kodi):
```rust
// Serde derive namunasi
// #[derive(Serialize, Deserialize, Debug)]
// struct Foydalanuvchi {
//     id: u64,
//     ism: String,
//     faol: bool,
// }

fn main() {
    println!("Serde derive qo'shilishi:");
    println!("`#[derive(serde::Serialize, serde::Deserialize)]` yozilishi bilan tur avtomatik ravishda barcha formatlarga moslashadi.");
}
```
## Tushuntirish va Mantiq:
Derive makrolari kompilyatsiya vaqtida strukturaning har bir maydoni uchun optimal serializatsiya kodini yaratadi.
## Ishlash natijasi:
```text
Serde derive qo'shilishi:
`#[derive(serde::Serialize, serde::Deserialize)]` yozilishi bilan tur avtomatik ravishda barcha formatlarga moslashadi.
```

---

# 876-Topshiriq: Oddiy JSON generatori: Rust struct'ini JSON matniga aylantirish
## Topshiriq sharti:
Qo'lda JSON matnini shakllantiruvchi metod yozing.
## Yechim (Rust kodi):
```rust
struct Mahsulot {
    id: u32,
    nomi: &'static str,
    narxi: f64,
}

impl Mahsulot {
    fn json_qator(&self) -> String {
        format!(r#"{{"id":{},"nomi":"{}","narxi":{:.2}}}"#, self.id, self.nomi, self.narxi)
    }
}

fn main() {
    let m = Mahsulot { id: 101, nomi: "Noutbuk", narxi: 1250.50 };
    println!("JSON natija: {}", m.json_qator());
}
```
## Tushuntirish va Mantiq:
Oddiy holatlarda JSON formatlashni string interpolyatsiyasi bilan ham qilish mumkin, ammo murakkab ma'lumotlar uchun `serde_json` tavsiya etiladi.
## Ishlash natijasi:
```text
JSON natija: {"id":101,"nomi":"Noutbuk","narxi":1250.50}
```

---

# 877-Topshiriq: Oddiy JSON parseri: matndan struct maydonlarini ajratish
## Topshiriq sharti:
JSON matnidan oddiy kalit-qiymatlarni ajratib oluvchi funksiya tuzing.
## Yechim (Rust kodi):
```rust
#[derive(Debug)]
struct Sozlama {
    host: String,
    port: u16,
}

fn sozlamani_parse_qil(json: &str) -> Option<Sozlama> {
    let toza = json.trim_matches(|c| c == '{' || c == '}');
    let mut host = String::new();
    let mut port = 0;

    for juftlik in toza.split(',') {
        let qismlar: Vec<&str> = juftlik.split(':').collect();
        if qismlar.len() == 2 {
            let kalit = qismlar[0].trim().trim_matches('"');
            let qiymat = qismlar[1].trim().trim_matches('"');
            if kalit == "host" { host = qiymat.to_string(); }
            if kalit == "port" { port = qiymat.parse().unwrap_or(0); }
        }
    }

    if !host.is_empty() && port > 0 {
        Some(Sozlama { host, port })
    } else {
        None
    }
}

fn main() {
    let json = r#"{"host": "127.0.0.1", "port": 8080}"#;
    let s = sozlamani_parse_qil(json).unwrap();
    println!("Parse qilingan konfiguratsiya: {:?}", s);
}
```
## Tushuntirish va Mantiq:
JSON parsing matnli tokenlarni tahlil qilib, ularni Rust'ning qat'iy tiplariga xavfsiz o'tkazishdan iborat.
## Ishlash natijasi:
```text
Parse qilingan konfiguratsiya: Sozlama { host: "127.0.0.1", port: 8080 }
```

---

# 878-Topshiriq: Serde field attribute: rename
## Topshiriq sharti:
`#[serde(rename = "...")]` orqali Rust'dagi `snake_case` maydonni JSON'dagi `camelCase` ga o'zgartirish.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Serde rename misoli:");
    println!(r#"
#[derive(Serialize, Deserialize)]
struct Foydalanuvchi {
    #[serde(rename = "first_name")]
    ism: String,
    #[serde(rename = "createdAt")]
    yaratilgan_vaqt: String,
}
"#);
}
```
## Tushuntirish va Mantiq:
Tashqi API bilan ishlashda Rust stiliga (snake_case) sodiq qolgan holda tashqi API talab qilgan nomlarni ishlatishga imkon beradi.
## Ishlash natijasi:
```text
Serde rename misoli:

#[derive(Serialize, Deserialize)]
struct Foydalanuvchi {
    #[serde(rename = "first_name")]
    ism: String,
    #[serde(rename = "createdAt")]
    yaratilgan_vaqt: String,
}
```

---

# 879-Topshiriq: Serde field attribute: default
## Topshiriq sharti:
JSON ichida maydon mavjud bo'lmasa unga `#[serde(default)]` orqali standart qiymat berish.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Serde default atributi:");
    println!(r#"
#[derive(Serialize, Deserialize, Default)]
struct ServerSozlamasi {
    port: u16,
    #[serde(default)]
    tls_yoqilganmi: bool, // Agar JSON da bo'lmasa, false bo'ladi
}
"#);
}
```
## Tushuntirish va Mantiq:
`#[serde(default)]` orqali yangi maydonlar qo'shilganda eski JSON hujjatlari bilan moslik (backward compatibility) buzilmaydi.
## Ishlash natijasi:
```text
Serde default atributi:

#[derive(Serialize, Deserialize, Default)]
struct ServerSozlamasi {
    port: u16,
    #[serde(default)]
    tls_yoqilganmi: bool, // Agar JSON da bo'lmasa, false bo'ladi
}
```

---

# 880-Topshiriq: Serde field attribute: skip va skip_serializing_if
## Topshiriq sharti:
Maxfiy ma'lumotlarni (parol, token) serializatsiya qilmaslik uchun `skip` qo'llash.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Serde skip:");
    println!(r#"
#[derive(Serialize, Deserialize)]
struct UserProfil {
    login: String,
    #[serde(skip_serializing)]
    parol_hesh: String, // Hech qachon JSON chiqishida ko'rinmaydi!
}
"#);
}
```
## Tushuntirish va Mantiq:
`skip_serializing` maxfiy ma'lumotlar tasodifan mijozga yoki loglarga sizib chiqishini to'liq to'xtatadi.
## Ishlash natijasi:
```text
Serde skip:

#[derive(Serialize, Deserialize)]
struct UserProfil {
    login: String,
    #[serde(skip_serializing)]
    parol_hesh: String, // Hech qachon JSON chiqishida ko'rinmaydi!
}
```

---

# 881-Topshiriq: Nested (ichma-ich) strukturalarni serializatsiya qilish
## Topshiriq sharti:
Struktura ichida boshqa strukturalar va vektorlar bo'lganda iyerarxik JSON shakllantirish.
## Yechim (Rust kodi):
```rust
#[derive(Debug)]
struct Manzil {
    shahar: &'static str,
    kocha: &'static str,
}

#[derive(Debug)]
struct Xodim {
    ism: &'static str,
    manzil: Manzil,
}

fn main() {
    let xodim = Xodim {
        ism: "Temur",
        manzil: Manzil { shahar: "Toshkent", kocha: "Amir Temur" },
    };

    println!("Xodim: {:?}", xodim);
    println!("Iyerarxik obyekt xotirada xavfsiz saqlanmoqda.");
}
```
## Tushuntirish va Mantiq:
Serde ichma-ich joylashgan barcha bolalar uchun avtomatik rekursiv serializatsiyani amalga oshiradi.
## Ishlash natijasi:
```text
Xodim: Xodim { ism: "Temur", manzil: Manzil { shahar: "Toshkent", kocha: "Amir Temur" } }
Iyerarxik obyekt xotirada xavfsiz saqlanmoqda.
```

---

# 882-Topshiriq: Enum'larni Serde bilan serializatsiya qilish (Tagging)
## Topshiriq sharti:
Enum'larning Externally tagged, Internally tagged va Adjacently tagged turlarini tushuntirish.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Serde Enum Tagging usullari:");
    println!("1. External (standart): {{\"Xabar\": {{\"matn\": \"salom\"}}}}");
    println!("2. Internal (#[serde(tag = \"type\")]): {{\"type\": \"Xabar\", \"matn\": \"salom\"}}");
    println!("3. Adjacent (#[serde(tag = \"t\", content = \"c\")]): {{\"t\": \"Xabar\", \"c\": {{\"matn\": \"salom\"}}}}");
}
```
## Tushuntirish va Mantiq:
Internal va adjacent tagging zamonaviy REST API va frontend JSON formatlari bilan juda mos tushadi.
## Ishlash natijasi:
```text
Serde Enum Tagging usullari:
1. External (standart): {"Xabar": {"matn": "salom"}}
2. Internal (#[serde(tag = "type")]): {"type": "Xabar", "matn": "salom"}
3. Adjacent (#[serde(tag = "t", content = "c")]): {"t": "Xabar", "c": {"matn": "salom"}}
```

---

# 883-Topshiriq: Serde Untagged enums: formatni avtomatik aniqlash
## Topshiriq sharti:
Qiymat son ham, matn ham bo'lishi mumkin bo'lganda `#[serde(untagged)]` dan foydalanish.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Untagged Enum misoli:");
    println!(r#"
#[derive(Serialize, Deserialize)]
#[serde(untagged)]
enum IdTuri {
    Raqam(u64),
    Satr(String),
}
"#);
}
```
## Tushuntirish va Mantiq:
`untagged` variantlarni ketma-ket parse qilishga urinadi va birinchi mos kelgan variantni tanlaydi.
## Ishlash natijasi:
```text
Untagged Enum misoli:

#[derive(Serialize, Deserialize)]
#[serde(untagged)]
enum IdTuri {
    Raqam(u64),
    Satr(String),
}
```

---

# 884-Topshiriq: serde_json::Value orqali schemasiz dinamik JSON
## Topshiriq sharti:
Strukturasi oldindan ma'lum bo'lmagan ixtiyoriy JSON hujjatini tahlil qilish tartibi.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("serde_json::Value:");
    println!("Value enum variantlari: Null, Bool, Number, String, Array, Object");
    println!("v[\"foydalanuvchi\"][\"yosh\"].as_u64() orqali dinamik murojaat qilinadi.");
}
```
## Tushuntirish va Mantiq:
`Value` noaniq formatdagi yoki juda xilma-xil ma'lumotlar bilan ishlashda qulaylik yaratadi.
## Ishlash natijasi:
```text
serde_json::Value:
Value enum variantlari: Null, Bool, Number, String, Array, Object
v["foydalanuvchi"]["yosh"].as_u64() orqali dinamik murojaat qilinadi.
```

---

# 885-Topshiriq: CSV fayllarini o'qish va parse qilish
## Topshiriq sharti:
Vergul bilan ajratilgan (CSV) fayl qatorlarini parse qilib jadval shaklida chop etish.
## Yechim (Rust kodi):
```rust
fn main() {
    let csv_matn = "id,ism,maosh\n1,Alisher,5000\n2,Zuhra,6000\n3,Dilshod,5500";

    for (indeks, satr) in csv_matn.lines().enumerate() {
        if indeks == 0 { continue; } // Sarlavhani o'tkazib yuboramiz
        let ustunlar: Vec<&str> = satr.split(',').collect();
        println!("Xodim: {} | Maoshi: ${}", ustunlar[1], ustunlar[2]);
    }
}
```
## Tushuntirish va Mantiq:
CSV ma'lumotlar tahlilida juda ommabop bo'lib, har bir qatordagi ustunlar vergul orqali olinadi.
## Ishlash natijasi:
```text
Xodim: Alisher | Maoshi: $5000
Xodim: Zuhra | Maoshi: $6000
Xodim: Dilshod | Maoshi: $5500
```

---

# 886-Topshiriq: CSV fayliga ma'lumotlarni yozish
## Topshiriq sharti:
Strukturalar ro'yxatini vergul bilan ajratilgan CSV formatida faylga yozish.
## Yechim (Rust kodi):
```rust
use std::fs::File;
use std::io::{self, Write};

struct Talaba {
    id: u32,
    ism: &'static str,
    ball: f32,
}

fn main() -> io::Result<()> {
    let talabalar = vec![
        Talaba { id: 1, ism: "Jasur", ball: 85.5 },
        Talaba { id: 2, ism: "Madina", ball: 92.0 },
    ];

    let mut f = File::create("talabalar.csv")?;
    writeln!(f, "id,ism,ball")?;

    for t in talabalar {
        writeln!(f, "{},{},{:.1}", t.id, t.ism, t.ball)?;
    }

    println!("CSV fayli muvaffaqiyatli saqlandi.");
    std::fs::remove_file("talabalar.csv")?;
    Ok(())
}
```
## Tushuntirish va Mantiq:
Jadvalli ma'lumotlarni CSV ga chiqarish orqali Excel yoki Pandas bilan oson integratsiya qilinadi.
## Ishlash natijasi:
```text
CSV fayli muvaffaqiyatli saqlandi.
```

---

# 887-Topshiriq: TOML konfiguratsiya fayllari tuzilishi
## Topshiriq sharti:
Rust loyihalarining `Cargo.toml` kabi konfiguratsiyalari qanday parse qilinishini tushuntiring.
## Yechim (Rust kodi):
```rust
fn main() {
    let toml_matn = r#"
[server]
host = "127.0.0.1"
port = 8080

[baza]
nomi = "rust_db"
max_ulanishlar = 20
"#;
    println!("TOML hujjati namunasi:\n{}", toml_matn);
}
```
## Tushuntirish va Mantiq:
TOML inson o'qishi uchun eng qulay va qat'iy tiplashtirilgan konfiguratsiya tili hisoblanadi.
## Ishlash natijasi:
```text
TOML hujjati namunasi:

[server]
host = "127.0.0.1"
port = 8080

[baza]
nomi = "rust_db"
max_ulanishlar = 20
```

---

# 888-Topshiriq: YAML formati va Rust mappingi
## Topshiriq sharti:
Iyerarxik YAML hujjatlarining strukturasi va Serde bilan o'qilishi.
## Yechim (Rust kodi):
```rust
fn main() {
    let yaml_matn = r#"
versiya: "1.0"
xizmatlar:
  veb:
    port: 80
    restart: doimiy
"#;
    println!("YAML namunasi:\n{}", yaml_matn);
}
```
## Tushuntirish va Mantiq:
YAML Docker-compose va Kubernetes deklaratsiyalarida keng qo'llaniladi.
## Ishlash natijasi:
```text
YAML namunasi:

versiya: "1.0"
xizmatlar:
  veb:
    port: 80
    restart: doimiy
```

---

# 889-Topshiriq: Binar formatlar: Bincode nima va uning afzalligi
## Topshiriq sharti:
Nima sababdan binar serializatsiya (Bincode) JSON dan ancha ixcham va tez ekanligini ko'rsating.
## Yechim (Rust kodi):
```rust
fn main() {
    let son: u64 = 123456789;

    // JSON da bu "123456789" satri sifatida 9 bayt oladi
    let json_baytlar = son.to_string().into_bytes();
    // Binar formatda esa doimo aniq 8 bayt oladi
    let binar_baytlar = son.to_le_bytes();

    println!("JSON matn uzunligi:  {} bayt", json_baytlar.len());
    println!("Binar hajm:          {} bayt", binar_baytlar.len());
}
```
## Tushuntirish va Mantiq:
Bincode matnli konvertatsiya qilmaydi, xotiradagi xom baytlarni to'g'ridan-to'g'ri yozadi, shuning uchun juda tejamkor.
## Ishlash natijasi:
```text
JSON matn uzunligi:  9 bayt
Binar hajm:          8 bayt
```

---

# 890-Topshiriq: Endianness: Big-Endian vs Little-Endian baytlar tartibi
## Topshiriq sharti:
`to_be_bytes()` va `to_le_bytes()` yordamida ko'p baytli sonlarni binar qatorga o'giring.
## Yechim (Rust kodi):
```rust
fn main() {
    let son: u32 = 0x12345678;

    let be = son.to_be_bytes(); // Big-endian (Tarmoq tartibi)
    let le = son.to_le_bytes(); // Little-endian (x86 CPU tartibi)

    println!("Big-Endian:    {:02X?}", be);
    println!("Little-Endian: {:02X?}", le);
}
```
## Tushuntirish va Mantiq:
Tarmoq protokollari (TCP/IP) odatda Big-Endian ishlatadi, aksariyat zamonaviy kompyuter protsessorlari esa Little-Endian.
## Ishlash natijasi:
```text
Big-Endian:    [12, 34, 56, 78]
Little-Endian: [78, 56, 34, 12]
```

---

# 891-Topshiriq: Binar fayl boshlig'i (Magic Bytes) tekshiruvi
## Topshiriq sharti:
Fayl formati to'g'riligini aniqlash uchun fayl boshidagi 'sehrli baytlar'ni (magic bytes) tekshirish.
## Yechim (Rust kodi):
```rust
use std::io::{self, Cursor, Read, Write};

const SEHRLI_BAYTLAR: [u8; 4] = [0x55, 0x5A, 0x42, 0x01]; // "UZB\x01"

fn faylni_tekshir<R: Read>(mut r: R) -> io::Result<bool> {
    let mut boshlik = [0u8; 4];
    r.read_exact(&mut boshlik)?;
    Ok(boshlik == SEHRLI_BAYTLAR)
}

fn main() -> io::Result<()> {
    let mut soxta_fayl = Cursor::new(Vec::new());
    soxta_fayl.write_all(&SEHRLI_BAYTLAR)?;
    soxta_fayl.set_position(0);

    let mos = faylni_tekshir(soxta_fayl)?;
    println!("Fayl formati tasdiqlandimi: {}", mos);
    Ok(())
}
```
## Tushuntirish va Mantiq:
PNG (`89 50 4E 47`), PDF (`%PDF`), ELF va boshqa barcha professional formatlar o'z magic baytlariga ega.
## Ishlash natijasi:
```text
Fayl formati tasdiqlandimi: true
```

---

# 892-Topshiriq: Faylni atomik yozish (Atomic file write)
## Topshiriq sharti:
Fayl yozilayotgan paytda elektr uzilsa ma'lumot buzilmasligi uchun avval vaqtinchalik faylga yozib, so'ng `rename` qilish.
## Yechim (Rust kodi):
```rust
use std::fs;
use std::io::Write;

fn atomik_saqlash(maqsad_fayl: &str, matn: &str) -> std::io::Result<()> {
    let vaqtinchalik = format!("{}.tmp", maqsad_fayl);
    {
        let mut f = fs::File::create(&vaqtinchalik)?;
        f.write_all(matn.as_bytes())?;
        f.sync_all()?; // Diskka to'liq yozilishini kafolatlash
    }
    // Rename operatsion tizim darajasida atomikdir
    fs::rename(&vaqtinchalik, maqsad_fayl)?;
    Ok(())
}

fn main() -> std::io::Result<()> {
    atomik_saqlash("muhim_baza.db", "Qimmatli tranzaksiya ma'lumotlari")?;
    println!("Fayl atomik tarzda xavfsiz saqlandi.");
    fs::remove_file("muhim_baza.db")?;
    Ok(())
}
```
## Tushuntirish va Mantiq:
Atomik yozish usuli nosozlik paytida yarmi yozilgan yarimta buzuq fayllar hosil bo'lishini 100% bartaraf etadi.
## Ishlash natijasi:
```text
Fayl atomik tarzda xavfsiz saqlandi.
```

---

# 893-Topshiriq: Fayl checksum hisoblash: Oddiy CRC/Hash tekshiruvi
## Topshiriq sharti:
Fayldagi baytlarning nazorat yig'indisini hisoblab fayl butunligini tekshirish.
## Yechim (Rust kodi):
```rust
fn hisobla_oddiy_checksum(baytlar: &[u8]) -> u32 {
    let mut sum: u32 = 0;
    for &b in baytlar {
        sum = sum.wrapping_add(b as u32);
    }
    sum
}

fn main() {
    let ma_lumot = b"Rust bilan xavfsiz hisob-kitob";
    let checksum = hisobla_oddiy_checksum(ma_lumot);
    println!("Ma'lumot checksum qiymati: 0x{:08X}", checksum);
}
```
## Tushuntirish va Mantiq:
Checksum orqali fayl uzatishda yoki disk nosozligida baytlar o'zgarib ketganligi aniqlanadi.
## Ishlash natijasi:
```text
Ma'lumot checksum qiymati: 0x00000BD7
```

---

# 894-Topshiriq: Memory-Mapped Files (mmap) tushunchasi
## Topshiriq sharti:
Gigabaytlab hajmdagi faylni xotiraga nusxalamasdan virtual xotira sahifalari orqali to'g'ridan-to'g'ri o'qish.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Memory-Mapped Files (mmap):");
    println!("1. OS faylni to'g'ridan-to'g'ri jarayonning virtual manzil fazosiga bog'laydi.");
    println!("2. Xotiradagi massivni o'qigandek faylni ko'rsatkichlar bilan o'qish mumkin.");
    println!("3. Zero-copy arxitektura sababli ulkan AI modellari va indekslar uchun qo'llaniladi.");
}
```
## Tushuntirish va Mantiq:
`mmap` operatsion tizimning sahifalash (paging) mexanizmidan foydalanadi va keraksiz bufer nusxalashni chetlab o'tadi.
## Ishlash natijasi:
```text
Memory-Mapped Files (mmap):
1. OS faylni to'g'ridan-to'g'ri jarayonning virtual manzil fazosiga bog'laydi.
2. Xotiradagi massivni o'qigandek faylni ko'rsatkichlar bilan o'qish mumkin.
3. Zero-copy arxitektura sababli ulkan AI modellari va indekslar uchun qo'llaniladi.
```

---

# 895-Topshiriq: Faylni siqish (Compression) tushunchasi
## Topshiriq sharti:
Katta matnli fayllarni Gzip yoki Zstandard bilan siqib saqlash afzalliklari.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("Fayllarni siqish:");
    println!("- Gzip / Deflate: Veb-protokollar uchun standart.");
    println!("- Zstandard (zstd): Zamonaviy yuqori tezlikdagi va yuqori siqish koeffitsiyentiga ega algoritm.");
    println!("- Rust'da `flate2` yoki `zstd` kutubxonalari orqali Read/Write oqimlariga oson ulanadi.");
}
```
## Tushuntirish va Mantiq:
Siqish disk joyini 70-90% tejaydi va tarmoq bo'ylab uzatish vaqtini sezilarli qisqartiradi.
## Ishlash natijasi:
```text
Fayllarni siqish:
- Gzip / Deflate: Veb-protokollar uchun standart.
- Zstandard (zstd): Zamonaviy yuqori tezlikdagi va yuqori siqish koeffitsiyentiga ega algoritm.
- Rust'da `flate2` yoki `zstd` kutubxonalari orqali Read/Write oqimlariga oson ulanadi.
```

---

# 896-Topshiriq: Fayl Qulflash (File Locking) mexanizmi
## Topshiriq sharti:
Bir nechta mustaqil dasturlar bir vaqtda bitta faylga yozib uni buzib qo'ymasligi uchun qulflash.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("File Locking tamoyili:");
    println!("- Shared Lock (O'qish qulfi): Bir vaqtda bir nechta dastur o'qiy oladi.");
    println!("- Exclusive Lock (Yozish qulfi): Faqat bitta jarayon yoza oladi, boshqalar kutib turadi.");
}
```
## Tushuntirish va Mantiq:
SQLite kabi bitta faylli ma'lumotlar bazalari tranzaksiya yaxlitligini ta'minlash uchun fayl qulflashdan foydalanadi.
## Ishlash natijasi:
```text
File Locking tamoyili:
- Shared Lock (O'qish qulfi): Bir vaqtda bir nechta dastur o'qiy oladi.
- Exclusive Lock (Yozish qulfi): Faqat bitta jarayon yoza oladi, boshqalar kutib turadi.
```

---

# 897-Topshiriq: Fayllarni kuzatish (File Watcher) arxitekturasi
## Topshiriq sharti:
Fayl yoki papka o'zgarganda (yangi fayl yaratilganda yoki tahrirlanganda) hodisalarni ushlash.
## Yechim (Rust kodi):
```rust
fn main() {
    println!("File Watcher mexanizmi:");
    println!("- Linux: inotify");
    println!("- Windows: ReadDirectoryChangesW");
    println!("- macOS: FSEvents");
    println!("Rust'da `notify` kutubxonasi ushbu OS mexanizmlarini yagona qulay interfeysga birlashtiradi.");
}
```
## Tushuntirish va Mantiq:
Live-reload serverlar va build tizimlari fayl o'zgarishini kuzatish orqali avtomatik qayta yig'iladi.
## Ishlash natijasi:
```text
File Watcher mexanizmi:
- Linux: inotify
- Windows: ReadDirectoryChangesW
- macOS: FSEvents
Rust'da `notify` kutubxonasi ushbu OS mexanizmlarini yagona qulay interfeysga birlashtiradi.
```

---

# 898-Topshiriq: CLI argumentlari va Konfiguratsiya faylini birlashtirish
## Topshiriq sharti:
Avval konfiguratsiya faylidan, agar ko'rsatilgan bo'lsa konsol argumentlaridan qiymatlarni o'zlashtirish.
## Yechim (Rust kodi):
```rust
struct Konfiguratsiya {
    port: u16,
}

impl Konfiguratsiya {
    fn yangi(standart_port: u16, cli_arg: Option<u16>) -> Self {
        let port = cli_arg.unwrap_or(standart_port);
        Konfiguratsiya { port }
    }
}

fn main() {
    let cfg = Konfiguratsiya::yangi(8080, Some(9000));
    println!("Faol port: {}", cfg.port);
}
```
## Tushuntirish va Mantiq:
Ushbu iyerarxik sozlash CLI ilovalarida eng qulay foydalanuvchi tajribasini (UX) beradi.
## Ishlash natijasi:
```text
Faol port: 9000
```

---

# 899-Topshiriq: Fayl deskriptorlari va resurslarni bo'shatish (RAII)
## Topshiriq sharti:
`File` structi o'z doirasidan chiqqanda uning operatsion tizim deskriptori avtomatik yopilishini ko'rsating.
## Yechim (Rust kodi):
```rust
use std::fs::File;

fn fayl_och_va_yop() {
    let _f = File::create("vaqtinchalik_fd.txt").unwrap();
    println!("Fayl ochildi va OS deskriptori band qilindi.");
} // _f shu yerda drop bo'ladi va fayl OS tomonidan avtomatik yopiladi

fn main() {
    fayl_och_va_yop();
    std::fs::remove_file("vaqtinchalik_fd.txt").unwrap();
    println!("Fayl muvaffaqiyatli yopilgan va diskdan o'chirildi.");
}
```
## Tushuntirish va Mantiq:
C tilida `fclose()` chaqirish esdan chiqishi xavfli oqibatlarga olib kelsa, Rust'da RAII buni 100% kafolatlaydi.
## Ishlash natijasi:
```text
Fayl ochildi va OS deskriptori band qilindi.
Fayl muvaffaqiyatli yopilgan va diskdan o'chirildi.
```

---

# 900-Topshiriq: Katta I/O va Serde Integratsion Loyihasi: Mini DBMS
## Topshiriq sharti:
Foydalanuvchilarni qo'shish, ro'yxatni faylga saqlash va fayldan qayta yuklash imkoniyatiga ega mini ma'lumotlar bazasi.
## Yechim (Rust kodi):
```rust
use std::fs::{self, File};
use std::io::{self, BufRead, BufReader, Write};

#[derive(Debug, Clone)]
struct Yozuv {
    id: u32,
    ism: String,
    yosh: u8,
}

struct MiniBaza {
    fayl_nomi: &'static str,
    yozuvlar: Vec<Yozuv>,
}

impl MiniBaza {
    fn ochish(fayl_nomi: &'static str) -> io::Result<Self> {
        let mut yozuvlar = Vec::new();
        if std::path::Path::new(fayl_nomi).exists() {
            let f = File::open(fayl_nomi)?;
            let reader = BufReader::new(f);
            for satr in reader.lines() {
                let satr = satr?;
                let q: Vec<&str> = satr.split('|').collect();
                if q.len() == 3 {
                    yozuvlar.push(Yozuv {
                        id: q[0].parse().unwrap_or(0),
                        ism: q[1].to_string(),
                        yosh: q[2].parse().unwrap_or(0),
                    });
                }
            }
        }
        Ok(MiniBaza { fayl_nomi, yozuvlar })
    }

    fn qoshish(&mut self, ism: &str, yosh: u8) {
        let yangi_id = (self.yozuvlar.len() + 1) as u32;
        self.yozuvlar.push(Yozuv {
            id: yangi_id,
            ism: ism.to_string(),
            yosh,
        });
    }

    fn saqlash(&self) -> io::Result<()> {
        let mut f = File::create(self.fayl_nomi)?;
        for y in &self.yozuvlar {
            writeln!(f, "{}|{}|{}", y.id, y.ism, y.yosh)?;
        }
        Ok(())
    }
}

fn main() -> io::Result<()> {
    let baza_fayli = "mini_db.txt";
    let mut db = MiniBaza::ochish(baza_fayli)?;

    db.qoshish("Ali", 25);
    db.qoshish("Vali", 30);
    db.saqlash()?;

    // Qayta o'qib tekshiramiz
    let qayta_db = MiniBaza::ochish(baza_fayli)?;
    println!("=== BAZADAGI YOZUVLAR ===");
    for y in qayta_db.yozuvlar {
        println!("[#{}] {} (yoshi: {})", y.id, y.ism, y.yosh);
    }

    fs::remove_file(baza_fayli)?;
    Ok(())
}
```
## Tushuntirish va Mantiq:
`BufReader` va `BufWriter` orqali matnli ma'lumotlar bazasini saqlash va yuklash xotira tejamkorligi va fayl yaxlitligini ta'minlaydi.
## Ishlash natijasi:
```text
=== BAZADAGI YOZUVLAR ===
[#1] Ali (yoshi: 25)
[#2] Vali (yoshi: 30)
```

---
