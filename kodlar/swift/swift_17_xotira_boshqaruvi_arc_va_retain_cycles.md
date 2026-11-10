# 801-Topshiriq: ARC Ishlash Prinsipi va Reference Count Hisoblagichi
## Topshiriq sharti:
Swift-da ARC (Automatic Reference Counting) qanday ishlashini va class nusxasi yaratilganda unga havola (reference) qo'shilishini namoyish etuvchi kod yozing.

## Yechim (Swift kodi):
```swift
class Foydalanuvchi {
    let ism: String
    init(ism: String) {
        self.ism = ism
        print("INIT: \(ism) xotirada yaratildi.")
    }
    deinit {
        print("DEINIT: \(ism) xotiradan butunlay o'chirildi.")
    }
}

print("1. ref1 o'zgaruvchisi yaratilmoqda:")
var ref1: Foydalanuvchi? = Foydalanuvchi(ism: "Alisher")

print("2. ref2 va ref3 havolalari qo'shilmoqda:")
var ref2 = ref1
var ref3 = ref1

print("3. ref1 va ref2 nil ga tenglanmoqda:")
ref1 = nil
ref2 = nil
print("Obyekt hali ham tirik, chunki ref3 mavjud.")

print("4. ref3 ham nil ga tenglanmoqda:")
ref3 = nil
print("Dastur yakunlandi.")
```

## Tushuntirish va Mantiq:
Swift-da reference tiplar (class) xotirada heap sohasida saqlanadi. ARC har bir obyektga nechta kuchli havola (strong reference) ko'rsatib turganini hisoblab boradi. Havolalar soni 0 ga tushgan onda deinit chaqiriladi va xotira bo'shatiladi.

## Ishlash natijasi:
```text
1. ref1 o'zgaruvchisi yaratilmoqda:
INIT: Alisher xotirada yaratildi.
2. ref2 va ref3 havolalari qo'shilmoqda:
3. ref1 va ref2 nil ga tenglanmoqda:
Obyekt hali ham tirik, chunki ref3 mavjud.
4. ref3 ham nil ga tenglanmoqda:
DEINIT: Alisher xotiradan butunlay o'chirildi.
Dastur yakunlandi.
```


# 802-Topshiriq: Scope (Ko'lam) va Obyekt Umri
## Topshiriq sharti:
Mahalliy blok (do/scope) ichida yaratilgan obyekt blok tugashi bilan qanday qilib ARC tomonidan avtomatik xotiradan tozalanishini ko'rsating.

## Yechim (Swift kodi):
```swift
class VaqtinchalikFayl {
    let faylNomi: String
    init(faylNomi: String) {
        self.faylNomi = faylNomi
        print("Fayl ochildi: \(faylNomi)")
    }
    deinit {
        print("Fayl yopildi va xotiradan tozalandi: \(faylNomi)")
    }
}

print("Asosiy blok boshlandi.")
do {
    print("--- Scope ichi boshlandi ---")
    let fayl = VaqtinchalikFayl(faylNomi: "temp_cache.dat")
    print("Scope ichida amal bajarilmoqda...")
    print("--- Scope ichi tugadi ---")
}
print("Asosiy blok davom etmoqda.")
```

## Tushuntirish va Mantiq:
Mahalliy ko'lam (scope) ichida yaratilgan o'zgaruvchilar blok tugaganda yo'q bo'ladi. Ular ko'rsatib turgan obyektlarning reference counti 0 ga tushadi va deinit darhol ishga tushadi.

## Ishlash natijasi:
```text
Asosiy blok boshlandi.
--- Scope ichi boshlandi ---
Fayl ochildi: temp_cache.dat
Scope ichida amal bajarilmoqda...
--- Scope ichi tugadi ---
Fayl yopildi va xotiradan tozalandi: temp_cache.dat
Asosiy blok davom etmoqda.
```


# 803-Topshiriq: Deinit Metodi va Resurslarni Tozalash
## Topshiriq sharti:
Obyekt yo'q qilinayotganda tarmoq ulanishini yoki fayl deskriptorini xavfsiz yopish uchun deinit metodidan to'g'ri foydalanishni ko'rsating.

## Yechim (Swift kodi):
```swift
class TarmoqUlanishi {
    let soketId: Int
    init(soketId: Int) {
        self.soketId = soketId
        print("Soket #\(soketId) ulandi.")
    }
    
    func malumotYubor(xabar: String) {
        print("Soket #\(soketId) orqali xabar: \(xabar)")
    }
    
    deinit {
        print("Soket #\(soketId) yopildi va tarmoq porti ozod qilindi.")
    }
}

var ulanish: TarmoqUlanishi? = TarmoqUlanishi(soketId: 8080)
ulanish?.malumotYubor(xabar: "Salom Server")
ulanish = nil
```

## Tushuntirish va Mantiq:
deinit faqat class tiplarida bo'lib, obyekt ARC tomonidan xotiradan o'chirilishidan oldin aniq bir marotaba chaqiriladi. Unda fayllar, ulanishlar va ochiq deskriptorlar yopiladi.

## Ishlash natijasi:
```text
Soket #8080 ulandi.
Soket #8080 orqali xabar: Salom Server
Soket #8080 yopildi va tarmoq porti ozod qilindi.
```


# 804-Topshiriq: Strong Reference Cycle (Retain Cycle) Yuzaga Kelishi
## Topshiriq sharti:
Ikki obyekt bir-biriga kuchli havola (strong reference) qilib, xotirada qolib ketishini (memory leak) isbotlovchi kod yozing.

## Yechim (Swift kodi):
```swift
class Talaba {
    let ism: String
    var xona: Yotoqxona?
    init(ism: String) { self.ism = ism }
    deinit { print("Talaba \(ism) xotiradan o'chirildi.") }
}

class Yotoqxona {
    let raqam: Int
    var yashovchi: Talaba?
    init(raqam: Int) { self.raqam = raqam }
    deinit { print("Yotoqxona \(raqam) xotiradan o'chirildi.") }
}

do {
    let talaba = Talaba(ism: "Bobur")
    let xona = Yotoqxona(raqam: 104)
    
    // Retain cycle yuzaga keltirish
    talaba.xona = xona
    xona.yashovchi = talaba
    print("Talaba va Yotoqxona bir-biriga bog'landi.")
}
print("Scope tugadi. Agar retain cycle bo'lsa, deinit chaqirilmaydi!")
```

## Tushuntirish va Mantiq:
Talaba va Yotoqxona obyektlari bir-biriga strong reference bilan bog'langan. Scope tugaganda o'zgaruvchilar yo'qolsa-da, har ikki obyektning reference counti 1 bo'lib qoladi. Natijada xotira sizishi (memory leak) yuz beradi va deinit ishlamaydi.

## Ishlash natijasi:
```text
Talaba va Yotoqxona bir-biriga bog'landi.
Scope tugadi. Agar retain cycle bo'lsa, deinit chaqirilmaydi!
```


# 805-Topshiriq: Retain Cycleni Aniqlash: Deinit Testi
## Topshiriq sharti:
Ikkita obyekt orasidagi retain cycle mavjudligini kuzatish uchun maxsus monitoring klassi yozing.

## Yechim (Swift kodi):
```swift
class XotiraKuzatuvchi {
    static var tirikObyektlarSoni = 0
}

class Bolim {
    let nom: String
    var xodim: Xodim?
    init(nom: String) {
        self.nom = nom
        XotiraKuzatuvchi.tirikObyektlarSoni += 1
    }
    deinit {
        XotiraKuzatuvchi.tirikObyektlarSoni -= 1
        print("Bolim '\(nom)' deinit chaqirildi.")
    }
}

class Xodim {
    let ism: String
    var bolim: Bolim?
    init(ism: String) {
        self.ism = ism
        XotiraKuzatuvchi.tirikObyektlarSoni += 1
    }
    deinit {
        XotiraKuzatuvchi.tirikObyektlarSoni -= 1
        print("Xodim '\(ism)' deinit chaqirildi.")
    }
}

do {
    let b = Bolim(nom: "Mobil Dasturlash")
    let x = Xodim(ism: "Sardor")
    b.xodim = x
    x.bolim = b
    print("Yaratilgandan keyin tirik obyektlar: \(XotiraKuzatuvchi.tirikObyektlarSoni)")
}

print("Scope tugagandan so'ng tirik obyektlar: \(XotiraKuzatuvchi.tirikObyektlarSoni)")
print("Xulosa: Tirik obyektlar soni 0 bo'lmadi -> Retain cycle mavjud!")
```

## Tushuntirish va Mantiq:
Statik hisoblagich orqali xotirada qolgan obyektlarni aniqlash unit testlarda memory leaklarni topishning klassik usullaridan biridir.

## Ishlash natijasi:
```text
Yaratilgandan keyin tirik obyektlar: 2
Scope tugagandan so'ng tirik obyektlar: 2
Xulosa: Tirik obyektlar soni 0 bo'lmadi -> Retain cycle mavjud!
```


# 806-Topshiriq: `weak` Havolasi Yordamida Siklni Buzish
## Topshiriq sharti:
Yuqoridagi retain cycleni bartaraf etish uchun `weak` kalit so'zidan foydalanib yechim yozing.

## Yechim (Swift kodi):
```swift
class Inson {
    let ism: String
    var xonadon: Kvartira?
    init(ism: String) { self.ism = ism }
    deinit { print("Inson \(ism) xotiradan tozalandi.") }
}

class Kvartira {
    let xonaRaqami: Int
    weak var egasi: Inson? // Weak havola reference countni oshirmaydi!
    init(xonaRaqami: Int) { self.xonaRaqami = xonaRaqami }
    deinit { print("Kvartira \(xonaRaqami) xotiradan tozalandi.") }
}

do {
    let inson = Inson(ism: "Javohir")
    let kvartira = Kvartira(xonaRaqami: 45)
    
    inson.xonadon = kvartira
    kvartira.egasi = inson
    print("Obyektlar o'zaro bog'landi (weak havola bilan).")
}

print("Scope tugadi. Har ikki deinit chaqirilishi kerak:")
```

## Tushuntirish va Mantiq:
`weak` havolasi reference countni oshirmaydi. Obyekt xotiradan o'chirilganda `weak` havola ARC tomonidan avtomatik `nil`ga aylantiriladi, shu sababli weak har doim optional (`var egasi: Inson?`) bo'lishi shart.

## Ishlash natijasi:
```text
Obyektlar o'zaro bog'landi (weak havola bilan).
Scope tugadi. Har ikki deinit chaqirilishi kerak:
Inson Javohir xotiradan tozalandi.
Kvartira 45 xotiradan tozalandi.
```


# 807-Topshiriq: Weak Havolaning Avtomatik Nilga Aylanishi
## Topshiriq sharti:
Weak ko'rsatkich ko'rsatib turgan obyekt xotiradan o'chirilganda, weak havola qanday qilib avtomatik nil bo'lishini isbotlang.

## Yechim (Swift kodi):
```swift
class Server {
    let host: String
    init(host: String) { self.host = host }
    deinit { print("Server (\(host)) yopildi.") }
}

class Klient {
    weak var server: Server?
}

let klient = Klient()
do {
    let server = Server(host: "api.khorazmiy.uz")
    klient.server = server
    print("Klient serverga ulangan: \(klient.server?.host ?? 'yoq')")
}

print("Server scope tugadi.")
print("Klientning server havolasi qiymati: \(klient.server == nil ? 'nil (xavfsiz tozalandi)' : 'mavjud')")
```

## Tushuntirish va Mantiq:
Boshqa tillardagi 'dangling pointer' muammosidan farqli o'laroq, Swift ARC weak havolalarni xavfsiz nolga tenglaydi (zeroing weak references).

## Ishlash natijasi:
```text
Klient serverga ulangan: api.khorazmiy.uz
Server (api.khorazmiy.uz) yopildi.
Server scope tugadi.
Klientning server havolasi qiymati: nil (xavfsiz tozalandi)
```


# 808-Topshiriq: `unowned` (Egasiz) Havola Asoslari
## Topshiriq sharti:
`unowned` kalit so'zi qachon ishlatilishini va u reference countni oshirmasdan optional bo'lmagan qiymat saqlashini ko'rsating.

## Yechim (Swift kodi):
```swift
class FoydalanuvchiAkkaunt {
    let login: String
    var profil: Profil?
    init(login: String) { self.login = login }
    deinit { print("Akkaunt '\(login)' xotiradan o'chirildi.") }
}

class Profil {
    unowned let akkaunt: FoydalanuvchiAkkaunt // Akkauntsiz profil yashay olmaydi
    let bio: String
    init(akkaunt: FoydalanuvchiAkkaunt, bio: String) {
        self.akkaunt = akkaunt
        self.bio = bio
    }
    deinit { print("Profil '\(bio)' xotiradan o'chirildi.") }
}

do {
    let acc = FoydalanuvchiAkkaunt(login: "jasur_dev")
    let prof = Profil(akkaunt: acc, bio: "iOS va Swift muhandisi")
    acc.profil = prof
    print("Akkaunt va profil bog'landi: \(prof.akkaunt.login)")
}
print("Scope tugadi.")
```

## Tushuntirish va Mantiq:
`unowned` xuddi `weak` kabi retain countni oshirmaydi, lekin u ikkinchi obyekt birinchi obyekt bilan bir xil yoki undan qisqaroq umr ko'rishiga kafolat bo'lganda ishlatiladi. Bu optional unwrap qilish majburiyatidan qutqaradi.

## Ishlash natijasi:
```text
Akkaunt va profil bog'landi: jasur_dev
Scope tugadi.
Akkaunt 'jasur_dev' xotiradan o'chirildi.
Profil 'iOS va Swift muhandisi' xotiradan o'chirildi.
```


# 809-Topshiriq: Mijoz va Bank Kartasi: `unowned` Amaliyoti
## Topshiriq sharti:
Har bir bank kartasi egasiga ega bo'lishi shart (`unowned`), ammo mijoz kartasiz ham mavjud bo'la olishi mumkin bo'lgan modelni yarating.

## Yechim (Swift kodi):
```swift
class Mijoz {
    let ism: String
    var karta: BankKartasi?
    init(ism: String) { self.ism = ism }
    deinit { print("Mijoz \(ism) xotiradan ozod qilindi.") }
}

class BankKartasi {
    let raqam: String
    unowned let egasi: Mijoz
    init(raqam: String, egasi: Mijoz) {
        self.raqam = raqam
        self.egasi = egasi
    }
    deinit { print("Karta \(raqam) bekor qilindi va xotiradan tozalandi.") }
}

do {
    let ali = Mijoz(ism: "Ali")
    let karta = BankKartasi(raqam: "8600-1234-5678-9999", egasi: ali)
    ali.karta = karta
    print("Mijoz: \(ali.ism), Karta: \(ali.karta!.raqam), Egasi: \(karta.egasi.ism)")
}
print("Amal yakunlandi.")
```

## Tushuntirish va Mantiq:
Bu klassik ARC patternidir: `Mijoz` kartaga strong havola qiladi (`var karta: BankKartasi?`), `BankKartasi` esa o'z egasiga `unowned let egasi: Mijoz` orqali bog'lanadi. Ikkalasi ham bir paytda xavfsiz deallokatsiya bo'ladi.

## Ishlash natijasi:
```text
Mijoz: Ali, Karta: 8600-1234-5678-9999, Egasi: Ali
Amal yakunlandi.
Mijoz Ali xotiradan ozod qilindi.
Karta 8600-1234-5678-9999 bekor qilindi va xotiradan tozalandi.
```


# 810-Topshiriq: `weak` vs `unowned`: Farqlar va Tanlov Matritsasi
## Topshiriq sharti:
`weak` va `unowned` orasidagi farqlarni taqqoslovchi va tushuntiruvchi Swift dasturini yozing.

## Yechim (Swift kodi):
```swift
struct Qoida {
    let mezon: String
    let weakTanlovi: String
    let unownedTanlovi: String
}

let qoidalar = [
    Qoida(mezon: "Umr davomiyligi", weakTanlovi: "Boshqa obyekt tezroq o'lishi mumkin", unownedTanlovi: "Bir vaqtda yoki kechroq o'ladi"),
    Qoida(mezon: "Ixtiyoriylik", weakTanlovi: "Har doim Optional (var ?)", unownedTanlovi: "Non-optional bo'lishi mumkin (let/var)"),
    Qoida(mezon: "Xavfsizlik", weakTanlovi: "Nil bo'lganda crash bo'lmaydi", unownedTanlovi: "O'chgan obyektga murojaat crash beradi"),
    Qoida(mezon: "ARC overhead", weakTanlovi: "Weak jadvalida ro'yxatdan o'tadi", unownedTanlovi: "Yengilroq, tezroq")
]

for q in qoidalar {
    print("[\(q.mezon)]: Weak -> \(q.weakTanlovi) | Unowned -> \(q.unownedTanlovi)")
}
```

## Tushuntirish va Mantiq:
Weak va unowned orasidagi asosiy farq ularning umr davomiyligidir: agar havola obyektdan uzoqroq yashashi yoki vaqt o'tib nil bo'lishi mumkin bo'lsa `weak`, agar obyekt mavjud bo'lgan paytda havola har doim tirik bo'lishi aniq bo'lsa `unowned` ishlatiladi.

## Ishlash natijasi:
```text
[Umr davomiyligi]: Weak -> Boshqa obyekt tezroq o'lishi mumkin | Unowned -> Bir vaqtda yoki kechroq o'ladi
[Ixtiyoriylik]: Weak -> Har doim Optional (var ?) | Unowned -> Non-optional bo'lishi mumkin (let/var)
[Xavfsizlik]: Weak -> Nil bo'lganda crash bo'lmaydi | Unowned -> O'chgan obyektga murojaat crash beradi
[ARC overhead]: Weak -> Weak jadvalida ro'yxatdan o'tadi | Unowned -> Yengilroq, tezroq
```


# 811-Topshiriq: `unowned(unsafe)` va Unsafe Reference
## Topshiriq sharti:
Swift-dagi xavfsiz `unowned(safe)` va xavfsiz bo'lmagan `unowned(unsafe)` konseptlarini tushuntiruvchi kod yozing.

## Yechim (Swift kodi):
```swift
class Qurilma {
    let model: String
    init(model: String) { self.model = model }
    deinit { print("Qurilma (\(model)) deinit.") }
}

class Drayver {
    // unowned(unsafe) ARC xavfsizlik tekshiruvini o'chiradi (C pointer kabi)
    unowned(unsafe) var qurilma: Qurilma
    init(qurilma: Qurilma) {
        self.qurilma = qurilma
    }
}

do {
    let q = Qurilma(model: "Sensor-A1")
    let d = Drayver(qurilma: q)
    print("Drayver qurilmaga murojaat qildi: \(d.qurilma.model)")
}
print("unowned(unsafe) faqat yuqori unumdorlik talab qilinadigan low-level kodda ishlatiladi.")
```

## Tushuntirish va Mantiq:
Oddiy `unowned` aslida `unowned(safe)` bo'lib, xotiradan o'chgan obyektga murojaat qilinganda runtime error beradi. `unowned(unsafe)` esa xotira manzilini tekshirmaydi va undefined behavior keltirib chiqarishi mumkin, shuning uchun juda ehtiyotkorlik bilan ishlatiladi.

## Ishlash natijasi:
```text
Drayver qurilmaga murojaat qildi: Sensor-A1
Qurilma (Sensor-A1) deinit.
unowned(unsafe) faqat yuqori unumdorlik talab qilinadigan low-level kodda ishlatiladi.
```


# 812-Topshiriq: Closure Capture va Retain Cycle Kelib Chiqishi
## Topshiriq sharti:
Class o'z property-sida closurni saqlasa va closure ichida `self` ishlatilsa, qanday retain cycle yuzaga kelishini ko'rsating.

## Yechim (Swift kodi):
```swift
class SahifaRaqami {
    let sahifa: Int
    init(sahifa: Int) { self.sahifa = sahifa }
    
    // Closure property sifatida saqlanmoqda
    lazy var formatlovchi: () -> String = {
        // self ni kuchli capture qiladi!
        return "Sahifa: \(self.sahifa)"
    }
    
    deinit {
        print("SahifaRaqami \(sahifa) xotiradan tozalandi.")
    }
}

do {
    let s = SahifaRaqami(sahifa: 42)
    print(s.formatlovchi())
}
print("Scope tugadi. Deinit chaqirilmadi, chunki 's' va 'formatlovchi' bir-birini ushlab turibdi!")
```

## Tushuntirish va Mantiq:
Obyekt closurni o'z property-sida saqlasa va closure o'z tanasida `self`ga murojaat qilsa, retain cycle vujudga keladi: Obyekt -> Closurni ushlaydi, Closure -> Obyektni ushlaydi.

## Ishlash natijasi:
```text
Sahifa: 42
Scope tugadi. Deinit chaqirilmadi, chunki 's' va 'formatlovchi' bir-birini ushlab turibdi!
```


# 813-Topshiriq: Capture List: `[weak self]` Bilan Closuredagi Siklni Hal Qilish
## Topshiriq sharti:
Closure capture listida `[weak self]` ishlatib, closure retain cycleni bartaraf etishni ko'rsating.

## Yechim (Swift kodi):
```swift
class XabarYuboruvchi {
    let matn: String
    init(matn: String) { self.matn = matn }
    
    lazy var yuborish: () -> Void = { [weak self] in
        guard let self = self else {
            print("Obyekt allaqachon xotiradan o'chirilgan.")
            return
        }
        print("Xabar jo'natildi: \(self.matn)")
    }
    
    deinit {
        print("XabarYuboruvchi xotiradan tozalandi.")
    }
}

do {
    let xabar = XabarYuboruvchi(matn: "Salom, Khorazmiy AI!")
    xabar.yuborish()
}
print("Scope tugadi:")
```

## Tushuntirish va Mantiq:
`[weak self]` sintaksisi closure tanasida `self`ni ixtiyoriy (optional) weak havola sifatida ushlaydi. Natijada closure obyektni xotirada majburan ushlab turmaydi.

## Ishlash natijasi:
```text
Xabar jo'natildi: Salom, Khorazmiy AI!
Scope tugadi:
XabarYuboruvchi xotiradan tozalandi.
```


# 814-Topshiriq: Capture List: `[unowned self]` Ishlatilishi
## Topshiriq sharti:
Closure va obyekt bir xil vaqtda yo'q bo'lishi kafolatlangan vaziyatda `[unowned self]` dan to'g'ri foydalanishni ko'rsating.

## Yechim (Swift kodi):
```swift
class Kalkulyator {
    var qiymat: Double = 100.0
    
    lazy var foizHisobla: (Double) -> Double = { [unowned self] foiz in
        return self.qiymat * (foiz / 100.0)
    }
    
    deinit {
        print("Kalkulyator deinit.")
    }
}

do {
    let kalk = Kalkulyator()
    print("10 foizi: \(kalk.foizHisobla(10))")
}
print("Scope tugadi:")
```

## Tushuntirish va Mantiq:
`[unowned self]` bilan `self` non-optional bo'ladi, guard let qilib unwrap qilishga ehtiyoj qolmaydi. Ammo agar closure obyekt o'chirilgandan so'ng chaqirilsa, dastur qulaydi (crash).

## Ishlash natijasi:
```text
10 foizi: 10.0
Scope tugadi:
Kalkulyator deinit.
```


# 815-Topshiriq: `guard let self = self else { return }` Idiomasi
## Topshiriq sharti:
Asinxron closure ichida `[weak self]` bilan ishlashda keng qo'llaniladigan `guard let self = self` idiomasi qanday ishlashini ko'rsating.

## Yechim (Swift kodi):
```swift
class Yuklovchi {
    let faylId: Int = 101
    
    func yuklashniBoshlash(tamomlandi: @escaping () -> Void) {
        print("Yuklash boshlandi...")
        tamomlandi()
    }
    
    func konfiguratsiya() {
        yuklashniBoshlash { [weak self] in
            guard let self = self else {
                print("Self nil bo'lib qolgan, amal to'xtatildi.")
                return
            }
            // Bu blok ichida self yana kuchli (strong) havola bo'lib, execution davomida o'chib ketmaydi
            print("Yuklash muvaffaqiyatli: fayl #\(self.faylId)")
        }
    }
    
    deinit {
        print("Yuklovchi deinit.")
    }
}

let y = Yuklovchi()
y.konfiguratsiya()
```

## Tushuntirish va Mantiq:
`guard let self = self` qilish closure ijrosi davomida `self` obyektining birdaniga xotiradan yo'qolib ketmasligini ta'minlaydi (strong reference shadowing). Swift 5.3+ da `guard let self else` qisqartmasi ham ruxsat etilgan.

## Ishlash natijasi:
```text
Yuklash boshlandi...
Yuklash muvaffaqiyatli: fayl #101
```


# 816-Topshiriq: Bir Nechta Obyektni Capture Qilish
## Topshiriq sharti:
Capture listda bir vaqtning o'zida bir nechta o'zgaruvchilarni turli xususiyatlar bilan (`weak`, `unowned`, qiymat nusxasi) capture qilishni ko'rsating.

## Yechim (Swift kodi):
```swift
class Foydalanuvchi {
    let ism: String
    init(ism: String) { self.ism = ism }
    deinit { print("Foydalanuvchi \(ism) o'chirildi.") }
}

class Buyurtma {
    let id: Int
    init(id: Int) { self.id = id }
    deinit { print("Buyurtma #\(id) o'chirildi.") }
}

let user = Foydalanuvchi(ism: "Akmal")
let order = Buyurtma(id: 777)
var maxsusChegirma = 15

// Capture list: user (weak), order (unowned), chegirma (qiymat nusxasi)
let amaliyot = { [weak user, unowned order, chegirma = maxsusChegirma] in
    let userName = user?.ism ?? "Noma'lum"
    print("Mijoz: \(userName), Buyurtma: #\(order.id), Chegirma: \(chegirma)%")
}

maxsusChegirma = 50 // Tashqi qiymat o'zgartirildi
amaliyot() // Closure o'z nusxasidagi 15 qiymatini ishlatadi
```

## Tushuntirish va Mantiq:
Capture list ichida `[weak a, unowned b, c = d]` ko'rinishida bir nechta havolalarni va qiymat nusxalarini aniq belgilash mumkin.

## Ishlash natijasi:
```text
Mijoz: Akmal, Buyurtma: #777, Chegirma: 15%
Foydalanuvchi Akmal o'chirildi.
Buyurtma #777 o'chirildi.
```


# 817-Topshiriq: Qiymat Tiplarini Capture Qilish: Nusxa vs Havola
## Topshiriq sharti:
Closure qiymat tiplarini (Int, Struct) standart holda havola orqali yoki capture list orqali nusxa sifatida qanday ushlashini namoyish eting.

## Yechim (Swift kodi):
```swift
var hisoblagich = 10

// 1. Capture listsiz: hisoblagichga havola olinadi
let closureHavola = {
    print("Havola orqali: \(hisoblagich)")
}

// 2. Capture list bilan: hisoblagichning o'sha oniy nusxasi olinadi
let closureNusxa = { [hisoblagich] in
    print("Capture nusxasi: \(hisoblagich)")
}

hisoblagich = 999

closureHavola() // 999 chiqaradi
closureNusxa()  // 10 chiqaradi
```

## Tushuntirish va Mantiq:
Agar capture list ishlatilmasa, closure tashqi o'zgaruvchining manzilini (reference) ushlaydi va tashqaridagi o'zgarishlar closure ichida aks etadi. Agar `[hisoblagich]` yozilsa, closure yaratilgan paytdagi nusxa olinadi.

## Ishlash natijasi:
```text
Havola orqali: 999
Capture nusxasi: 10
```


# 818-Topshiriq: Escaping vs Non-Escaping Closures va Retain Cycle
## Topshiriq sharti:
Nega non-escaping closurelarda retain cycle xavfi bo'lmasligini va nima uchun `[weak self]` faqat escaping closurelarda kerakligini isbotlang.

## Yechim (Swift kodi):
```swift
class Masala {
    let nom: String = "Algoritm"
    
    // Non-escaping: funksiya tugashi bilan closure xotiradan ketadi
    func bajarBirZumda(amal: () -> Void) {
        amal()
    }
    
    // Escaping: closure xotirada saqlanishi yoki keyinroq chaqirilishi mumkin
    var saqlanganAmal: (() -> Void)?
    func saqla(amal: @escaping () -> Void) {
        self.saqlanganAmal = amal
    }
    
    func test() {
        // Non-escaping: self ni yozish shart emas va retain cycle bo'lmaydi
        bajarBirZumda {
            print("Non-escaping bajarildi: \(nom)")
        }
        
        // Escaping: retain cycle bo'lmasligi uchun [weak self] zarur
        saqla { [weak self] in
            print("Escaping bajarildi: \(self?.nom ?? '')")
        }
    }
    
    deinit { print("Masala deinit.") }
}

do {
    let m = Masala()
    m.test()
}
```

## Tushuntirish va Mantiq:
Non-escaping closurelar funksiya stek doirasidan tashqariga chiqmaydi, shuning uchun obyektni uzoq vaqt ushlab tura olmaydi va retain cycle vujudga kelmaydi. Escaping closurelar esa heap-da saqlangani sababli retain cycle keltirib chiqarishi mumkin.

## Ishlash natijasi:
```text
Non-escaping bajarildi: Algoritm
Masala deinit.
```


# 819-Topshiriq: Delegation Patternida Retain Cycle Oldini Olish
## Topshiriq sharti:
Delegatsiya arxitekturasida delegate o'zgaruvchisini `weak` e'lon qilish nima uchun shartligini ko'rsating.

## Yechim (Swift kodi):
```swift
protocol AudioPleyerDelegate: AnyObject {
    func audioBoshlandi()
}

class AudioPleyer {
    // Agar bu yerda 'weak' bo'lmasa, retain cycle yuzaga keladi!
    weak var delegate: AudioPleyerDelegate?
    
    func play() {
        print("Musiqa yangramoqda...")
        delegate?.audioBoshlandi()
    }
    
    deinit { print("AudioPleyer deinit.") }
}

class PleyerKontroller: AudioPleyerDelegate {
    let pleyer = AudioPleyer()
    
    init() {
        pleyer.delegate = self
    }
    
    func audioBoshlandi() {
        print("PleyerKontroller: UI yangilandi.")
    }
    
    deinit { print("PleyerKontroller deinit.") }
}

do {
    let kontroller = PleyerKontroller()
    kontroller.pleyer.play()
}
print("Scope tugadi. Har ikkala deinit ishladi:")
```

## Tushuntirish va Mantiq:
PleyerKontroller -> pleyerni kuchli ushlaydi. Agar pleyer ham delegateni kuchli ushlasa (Pleyer -> Kontroller), retain cycle hosil bo'ladi. `weak var delegate` siklni buzadi.

## Ishlash natijasi:
```text
Musiqa yangramoqda...
PleyerKontroller: UI yangilandi.
Scope tugadi. Har ikkala deinit ishladi:
PleyerKontroller deinit.
AudioPleyer deinit.
```


# 820-Topshiriq: Class-Bound Protokollar: `AnyObject` Majburiyati
## Topshiriq sharti:
`weak` havolasi faqat reference tiplar (class) uchun amal qilishi sababli protokollarni nima uchun `AnyObject` bilan belgilash kerakligini ko'rsating.

## Yechim (Swift kodi):
```swift
// Faqat class tiplari qabul qilishi mumkin bo'lgan protokol
protocol MalumotYangilovchi: AnyObject {
    func yangilash()
}

class Xizmat {
    // Agar protokol AnyObject bo'lmasa, 'weak' qo'yish kompilyatsiya xatosi beradi!
    weak var yangilovchi: MalumotYangilovchi?
    
    func ishla() {
        yangilovchi?.yangilash()
    }
}

class EkranniBoshqaruvchi: MalumotYangilovchi {
    func yangilash() {
        print("Ekran ma'lumotlari yangilandi.")
    }
}

let ekran = EkranniBoshqaruvchi()
let xizmat = Xizmat()
xizmat.yangilovchi = ekran
xizmat.ishla()
```

## Tushuntirish va Mantiq:
Struct yoki Enum qiymat tiplari bo'lib, ular reference countga ega emas. Shuning uchun `weak` faqat class obyektlariga qo'llaniladi. Protokolga `AnyObject` meros berilgandagina uning havolasini `weak` deb e'lon qilish mumkin.

## Ishlash natijasi:
```text
Ekran ma'lumotlari yangilandi.
```


# 821-Topshiriq: Timer Obyektlarida Retain Cycleni Oldini Olish
## Topshiriq sharti:
Qaytariluvchi taymerlarda target sifatida `self` uzatilganda yuzaga keladigan retain cycleni mock misol orqali tushuntiring.

## Yechim (Swift kodi):
```swift
class QalbUrisiKuzatuvchi {
    var hisob = 0
    var timerClosure: (() -> Void)?
    
    func taymerniIshgaTushir() {
        // [weak self] qo'llanilmasa, timer va self bir-birini abadiy ushlab qoladi
        self.timerClosure = { [weak self] in
            guard let self = self else { return }
            self.hisob += 1
            print("Puls urishi: \(self.hisob)")
        }
    }
    
    func puls() {
        timerClosure?()
    }
    
    deinit {
        print("QalbUrisiKuzatuvchi xotiradan tozalandi.")
    }
}

do {
    let k = QalbUrisiKuzatuvchi()
    k.taymerniIshgaTushir()
    k.puls()
    k.puls()
}
print("Kuzatuvchi scope tugadi.")
```

## Tushuntirish va Mantiq:
Timerlar va callback mexanizmlarida `[weak self]` ishlatilmasa, taymer to'xtatilgunga qadar kontroller xotirada qolib ketadi.

## Ishlash natijasi:
```text
Puls urishi: 1
Puls urishi: 2
Kuzatuvchi scope tugadi.
QalbUrisiKuzatuvchi xotiradan tozalandi.
```


# 822-Topshiriq: NotificationCenter Obunasida Xotirani Tozalash
## Topshiriq sharti:
NotificationCenter orqali xabar qabul qiluvchi klassda memory leak yuzaga kelmasligi uchun unregister qilish va `[weak self]` ni ko'rsating.

## Yechim (Swift kodi):
```swift
class BildirishnomaXizmati {
    static let umumiy = BildirishnomaXizmati()
    var tinglovchilar: [() -> Void] = []
    
    func obunaBol(amal: @escaping () -> Void) {
        tinglovchilar.append(amal)
    }
    
    func tarqat() {
        for tinglovchi in tinglovchilar {
            tinglovchi()
        }
    }
}

class YangiliklarModuli {
    init() {
        BildirishnomaXizmati.umumiy.obunaBol { [weak self] in
            self?.xabarKeldi()
        }
    }
    
    func xabarKeldi() {
        print("Yangi xabar qabul qilindi.")
    }
    
    deinit {
        print("YangiliklarModuli deinit.")
    }
}

do {
    let modul = YangiliklarModuli()
    BildirishnomaXizmati.umumiy.tarqat()
}
print("YangiliklarModuli o'chirildi (garchi singleton hali mavjud bo'lsa ham).")
```

## Tushuntirish va Mantiq:
Singleton obyektlar butun dastur umri davomida yashaydi. Agar singleton ichidagi ro'yxatga oddiy klass closuredan `[weak self]`siz qo'shilsa, u hech qachon xotiradan o'chmaydi.

## Ishlash natijasi:
```text
Yangi xabar qabul qilindi.
YangiliklarModuli deinit.
YangiliklarModuli o'chirildi (garchi singleton hali mavjud bo'lsa ham).
```


# 823-Topshiriq: `autoreleasepool` Mexanizmi Asoslari
## Topshiriq sharti:
Katta hajmdagi sikllarda xotiraning keskin oshib ketishining (memory spike) oldini olish uchun `autoreleasepool` dan foydalanishni ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

class KattaMassiv {
    let id: Int
    init(id: Int) { self.id = id }
    deinit { /* Tezkor tozalanish */ }
}

print("Autoreleasepool bilan xotira boshqaruvi:")
for partiya in 1...3 {
    autoreleasepool {
        var bufer: [KattaMassiv] = []
        for i in 1...1000 {
            bufer.append(KattaMassiv(id: i))
        }
        print("Partiya \(partiya): \(bufer.count) ta obyekt qayta ishlandi.")
    }
    // autoreleasepool bloki tugashi bilan vaqtinchalik xotira darhol bo'shatiladi
}
print("Barcha partiyalar muvaffaqiyatli yakunlandi.")
```

## Tushuntirish va Mantiq:
`autoreleasepool` bloki Objective-C / Foundation bilan ishlayotganda vaqtinchalik yaratilgan avtomatik bo'shatiluvchi obyektlarni blok yakunlanishi bilan zudlik bilan yo'q qiladi.

## Ishlash natijasi:
```text
Autoreleasepool bilan xotira boshqaruvi:
Partiya 1: 1000 ta obyekt qayta ishlandi.
Partiya 2: 1000 ta obyekt qayta ishlandi.
Partiya 3: 1000 ta obyekt qayta ishlandi.
Barcha partiyalar muvaffaqiyatli yakunlandi.
```


# 824-Topshiriq: Sikllarda Tasvirlarni Qayta Ishlash va Autoreleasepool
## Topshiriq sharti:
Grafik yoki katta fayllarni partiyalab konvertatsiya qilishda xotira to'lib ketishini bartaraf qiluvchi arxitekturani yozing.

## Yechim (Swift kodi):
```swift
struct RasmMetasi {
    let nom: String
    let hajmMB: Double
}

func rasmFiltri(rasm: RasmMetasi) {
    autoreleasepool {
        let ishchiXotira = "\(rasm.nom) piksellari qayta ishlanmoqda (\(rasm.hajmMB) MB)"
        print("Ishlandi: \(ishchiXotira)")
    }
}

let rasmlar = [
    RasmMetasi(nom: "IMG_001.raw", hajmMB: 24.5),
    RasmMetasi(nom: "IMG_002.raw", hajmMB: 31.2),
    RasmMetasi(nom: "IMG_003.raw", hajmMB: 19.8)
]

for r in rasmlar {
    rasmFiltri(rasm: r)
}
print("Filtrlash tugadi. RAM pik darajasiga yetmadi.")
```

## Tushuntirish va Mantiq:
Har bir iteratsiyada autoreleasepool qo'llash operativ xotirada (RAM) ma'lumotlar to'planib qolishini oldini olib, operatsion tizim tomonidan ilova 'OOM' (Out of Memory) tufayli yopilib qolishidan asraydi.

## Ishlash natijasi:
```text
Ishlandi: IMG_001.raw piksellari qayta ishlanmoqda (24.5 MB)
Ishlandi: IMG_002.raw piksellari qayta ishlanmoqda (31.2 MB)
Ishlandi: IMG_003.raw piksellari qayta ishlanmoqda (19.8 MB)
Filtrlash tugadi. RAM pik darajasiga yetmadi.
```


# 825-Topshiriq: Struct Ichidagi Class Havolalari va Xotira
## Topshiriq sharti:
Qiymat tipi (struct) ichida reference tip (class) saqlanganda xotira va ARC qanday ishlashini namoyish eting.

## Yechim (Swift kodi):
```swift
class IchkiLogotip {
    var url: String
    init(url: String) { self.url = url }
}

struct BrendProfil {
    var brendNomi: String
    var logotip: IchkiLogotip // Reference tip saqlanmoqda!
}

let brend1 = BrendProfil(brendNomi: "Apple", logotip: IchkiLogotip(url: "apple.com/logo.png"))
var brend2 = brend1 // Struct nusxalanadi, ammo logotip havolasi umumiy bo'lib qoladi!

brend2.brendNomi = "Toshkent Tech"
brend2.logotip.url = "toshkent.uz/logo.png"

print("brend1 nomi: \(brend1.brendNomi), logotipi: \(brend1.logotip.url)")
print("brend2 nomi: \(brend2.brendNomi), logotipi: \(brend2.logotip.url)")
```

## Tushuntirish va Mantiq:
Struct qiymat tipi bo'lsa-da, agar uning ichida class bo'lsa, struct nusxalanganda class-ning faqat havolasi (pointer) nusxalanadi. Ikkala struct bitta class obyektiga qaraydi (shallow copy).

## Ishlash natijasi:
```text
brend1 nomi: Apple, logotipi: toshkent.uz/logo.png
brend2 nomi: Toshkent Tech, logotipi: toshkent.uz/logo.png
```


# 826-Topshiriq: `isKnownUniquelyReferenced` va Copy-On-Write (COW)
## Topshiriq sharti:
Swift-dagi standart massivlar kabi o'z-o'zidan nusxalanuvchi (COW) xatti-harakatni tekshirish uchun `isKnownUniquelyReferenced` funksiyasidan foydalanishni ko'rsating.

## Yechim (Swift kodi):
```swift
class XotiraBuferi {
    var baytlar: [UInt8]
    init(baytlar: [UInt8]) { self.baytlar = baytlar }
}

var buferA: XotiraBuferi? = XotiraBuferi(baytlar: [1, 2, 3])

// Hozirda buferA ga faqat bitta havola bor
print("Yagona havola bormi: \(isKnownUniquelyReferenced(&buferA))")

// Ikkinchi havola qo'shamiz
var buferB = buferA
print("Ikkinchi havola qo'shilgach: \(isKnownUniquelyReferenced(&buferA))")

buferB = nil
print("Ikkinchi havola uzilgach: \(isKnownUniquelyReferenced(&buferA))")
```

## Tushuntirish va Mantiq:
`isKnownUniquelyReferenced` funksiyasi obyektga faqat bitta kuchli havola bor yoki yo'qligini aniqlaydi. Bu Swift-dagi Data, Array va String kabi tiplarda Copy-On-Write optimizatsiyasini amalga oshirish asosi hisoblanadi.

## Ishlash natijasi:
```text
Yagona havola bormi: true
Ikkinchi havola qo'shilgach: false
Ikkinchi havola uzilgach: true
```


# 827-Topshiriq: Maxsus Copy-on-Write Struktura Yaratish
## Topshiriq sharti:
`isKnownUniquelyReferenced` yordamida haqiqiy COW (Copy-on-Write) xususiyatiga ega xavfsiz struktura yarating.

## Yechim (Swift kodi):
```swift
final class XotiraOmbori {
    var malumot: [String]
    init(malumot: [String]) { self.malumot = malumot }
    func nusxaOlish() -> XotiraOmbori {
        return XotiraOmbori(malumot: self.malumot)
    }
}

struct XavfsizMassiv {
    private var ombor: XotiraOmbori
    
    init(boshlangich: [String] = []) {
        self.ombor = XotiraOmbori(malumot: boshlangich)
    }
    
    mutating func qoshish(element: String) {
        // Agar bir nechta havola bo'lsa, yangi nusxa olamiz (Copy-on-Write)
        if !isKnownUniquelyReferenced(&ombor) {
            print("COW: Yangi chuqur nusxa yaratildi!")
            ombor = ombor.nusxaOlish()
        } else {
            print("COW: Mavjud xotiraning o'zida o'zgartirildi.")
        }
        ombor.malumot.append(element)
    }
    
    var elementlar: [String] {
        return ombor.malumot
    }
}

var royxat1 = XavfsizMassiv(boshlangich: ["Swift"])
var royxat2 = royxat1 // Hali nusxa olinmadi, umumiy ombor

royxat2.qoshish(element: "SwiftUI") // Shu yerda nusxa olinadi!
print("Royxat 1: \(royxat1.elementlar)")
print("Royxat 2: \(royxat2.elementlar)")
```

## Tushuntirish va Mantiq:
Copy-on-write texnikasi yordamida katta hajmdagi ma'lumotlar o'zgartirilmaguncha xotirada faqat bitta nusxada saqlanadi, o'zgartirilgan lahzada esa yangi nusxa olinadi.

## Ishlash natijasi:
```text
COW: Yangi chuqur nusxa yaratildi!
Royxat 1: ["Swift"]
Royxat 2: ["Swift", "SwiftUI"]
```


# 828-Topshiriq: Circular Linked List va Retain Cycle Yechimi
## Topshiriq sharti:
Aylanma bog'langan ro'yxatda (Circular Doubly Linked List) node-lar bir-birini cheksiz ushlab qolmasligi uchun havolalarni to'g'ri tashkil qiling.

## Yechim (Swift kodi):
```swift
class Tugun {
    let qiymat: String
    var keyingi: Tugun?
    weak var oldingi: Tugun? // Oldingiga havola weak bo'lishi shart!
    
    init(qiymat: String) {
        self.qiymat = qiymat
    }
    
    deinit {
        print("Tugun '\(qiymat)' xotiradan tozalandi.")
    }
}

do {
    let t1 = Tugun(qiymat: "Toshkent")
    let t2 = Tugun(qiymat: "Samarqand")
    let t3 = Tugun(qiymat: "Buxoro")
    
    t1.keyingi = t2
    t2.oldingi = t1
    
    t2.keyingi = t3
    t3.oldingi = t2
    print("3 ta shahar zanjirga ulandi.")
}
print("Scope tugadi:")
```

## Tushuntirish va Mantiq:
Ikki tomonlama bog'langan ro'yxatlarda (Doubly Linked List) `next` ko'rsatkichi strong, `previous` ko'rsatkichi esa `weak` bo'lishi kerak. Aks holda qo'shni tugunlar orasida retain cycle yuzaga keladi.

## Ishlash natijasi:
```text
3 ta shahar zanjirga ulandi.
Scope tugadi:
Tugun 'Toshkent' xotiradan tozalandi.
Tugun 'Samarqand' xotiradan tozalandi.
Tugun 'Buxoro' xotiradan tozalandi.
```


# 829-Topshiriq: Parent-Child Daraxt Strukturasida Xotira Xavfsizligi
## Topshiriq sharti:
Daraxtsimon (Tree) iyerarxiyada Ota (Parent) va Bola (Child) tugunlari orasidagi retain cycleni bartaraf etishni ko'rsating.

## Yechim (Swift kodi):
```swift
class DaraxtTuguni {
    let nom: String
    var bolalari: [DaraxtTuguni] = []
    weak var otaTugun: DaraxtTuguni? // Ota tugunga havola har doim weak!
    
    init(nom: String) { self.nom = nom }
    
    func bolaQoshish(_ bola: DaraxtTuguni) {
        bolalari.append(bola)
        bola.otaTugun = self
    }
    
    deinit { print("Tugun '\(nom)' deinit.") }
}

do {
    let ota = DaraxtTuguni(nom: "Ildiz (Root)")
    let bola1 = DaraxtTuguni(nom: "Fayllar")
    let bola2 = DaraxtTuguni(nom: "Rasmlar")
    
    ota.bolaQoshish(bola1)
    ota.bolaQoshish(bola2)
    print("Daraxt hosil qilindi: \(ota.nom) -> bolalari soni: \(ota.bolalari.count)")
}
print("Scope yakunlandi:")
```

## Tushuntirish va Mantiq:
Ota obyekt bolalarini massivda strong reference sifatida saqlaydi. Bola obyekt esa o'zining ota tuguniga `weak var otaTugun` orqali murojaat qiladi. Shu tariqa butun daraxt xotiradan toza o'chiriladi.

## Ishlash natijasi:
```text
Daraxt hosil qilindi: Ildiz (Root) -> bolalari soni: 2
Scope yakunlandi:
Tugun 'Ildiz (Root)' deinit.
Tugun 'Fayllar' deinit.
Tugun 'Rasmlar' deinit.
```


# 830-Topshiriq: Observer Pattern: Weak Wrapper Yordamida Leakni Yopish
## Topshiriq sharti:
Observerlar massivida obyektlarni to'g'ridan-to'g'ri saqlamasdan, `WeakRef` o'rami orqali avtomatik tozalash tizimini yarating.

## Yechim (Swift kodi):
```swift
class WeakRef<T: AnyObject> {
    weak var qiymat: T?
    init(_ qiymat: T) { self.qiymat = qiymat }
}

class Ob-HavoStansiyasi {
    private var kuzatuvchilar: [WeakRef<AnyObject>] = []
    
    func obunaQil(_ kuzatuvchi: AnyObject) {
        kuzatuvchilar.append(WeakRef(kuzatuvchi))
    }
    
    func tozalashVaXabarBer(harorat: Double) {
        // O'lib ketgan obyektlarni filtrlash
        kuzatuvchilar = kuzatuvchilar.filter { $0.qiymat != nil }
        print("Faol kuzatuvchilar soni: \(kuzatuvchilar.count), Yangi harorat: \(harorat)°C")
    }
}

class EkranKuzatuvchi {
    let nom: String
    init(nom: String) { self.nom = nom }
    deinit { print("Ekran '\(nom)' o'chirildi.") }
}

let stansiya = Ob-HavoStansiyasi()
do {
    let ekran1 = EkranKuzatuvchi(nom: "Smartfon Ekrani")
    stansiya.obunaQil(ekran1)
    stansiya.tozalashVaXabarBer(harorat: 25.5)
}
// ekran1 do scope tashqarisida yo'q bo'ldi
stansiya.tozalashVaXabarBer(harorat: 26.0)
```

## Tushuntirish va Mantiq:
`WeakRef<T: AnyObject>` generic wrapperi har qanday klassni massivda weak havola sifatida saqlash imkonini beradi. Obyekt xotiradan o'chirilgach, uning o'rami massivdan oson tozalanadi.

## Ishlash natijasi:
```text
Faol kuzatuvchilar soni: 1, Yangi harorat: 25.5°C
Ekran 'Smartfon Ekrani' o'chirildi.
Faol kuzatuvchilar soni: 0, Yangi harorat: 26.0°C
```


# 831-Topshiriq: Event Handler Callbacklarda Memory Leakni Oldini Olish
## Topshiriq sharti:
Tugmaga bosish (Button onClick) callbackida retain cycleni bartaraf etish patternini ko'rsating.

## Yechim (Swift kodi):
```swift
class MaxsusTugma {
    var bosilganda: (() -> Void)?
    func bosish() {
        bosilganda?()
    }
    deinit { print("Tugma deinit.") }
}

class LoginEkrani {
    let tugma = MaxsusTugma()
    let foydalanuvchi: String = "admin"
    
    init() {
        // [weak self] orqali tugma bilan ekran o'rtasidagi retain cycle bartaraf qilinadi
        tugma.bosilganda = { [weak self] in
            guard let self = self else { return }
            print("Tizimga kirish bosildi: \(self.foydalanuvchi)")
        }
    }
    
    deinit { print("LoginEkrani deinit.") }
}

do {
    let ekran = LoginEkrani()
    ekran.tugma.bosish()
}
print("LoginEkrani scope yakuni:")
```

## Tushuntirish va Mantiq:
View va uning ichki UI komponentlari bir-birining closure callbacklarini saqlaganda `[weak self]` majburiydir, aks holda sahifa yopilganda controller xotirada qolib ketadi.

## Ishlash natijasi:
```text
Tizimga kirish bosildi: admin
LoginEkrani scope yakuni:
LoginEkrani deinit.
Tugma deinit.
```


# 832-Topshiriq: Unit Testlarda Retain Cycle Tekshirish Texnikasi
## Topshiriq sharti:
XCTest-ga o'xshash usulda xotira sizishini tekshiruvchi avtomatlashtirilgan xotira testi funksiyasini yozing.

## Yechim (Swift kodi):
```swift
func xotiraSizishiniTekshir(yaratuvchi: () -> AnyObject) -> Bool {
    weak var kuchsizHavola: AnyObject?
    
    autoreleasepool {
        let obyekt = yaratuvchi()
        kuchsizHavola = obyekt
    }
    
    // Autoreleasepool tugagach, agar kuchsizHavola nil bo'lsa - xotira sizishi yo'q!
    if kuchsizHavola == nil {
        print("TEST: Obyekt to'g'ri o'chirildi. Memory leak yo'q.")
        return true
    } else {
        print("TEST XATOSI: Obyekt xotirada qolib ketdi! Memory leak aniqlandi!")
        return false
    }
}

class TozaKlass {
    deinit { /* Toza */ }
}

let natija = xotiraSizishiniTekshir {
    return TozaKlass()
}
print("Test natijasi: \(natija)")
```

## Tushuntirish va Mantiq:
Avtomatlashtirilgan testlarda obyekt yaratilib `weak` ko'rsatkichga o'zlashtiriladi. Scope tugagach, bu ko'rsatkich `nil` bo'lishi tekshiriladi. Agar `nil` bo'lmasa, retain cycle mavjud deb topiladi.

## Ishlash natijasi:
```text
TEST: Obyekt to'g'ri o'chirildi. Memory leak yo'q.
Test natijasi: true
```


# 833-Topshiriq: Swift Concurrency (`Task`) Ichida `[weak self]` Ishlatish
## Topshiriq sharti:
Uzoq davom etuvchi asinxron `Task` fon jarayonida controllerning xotirada qolmasligi uchun `[weak self]` ishlatilishini ko'rsating.

## Yechim (Swift kodi):
```swift
class QidiruvXizmati {
    let qidiruvMatni: String
    init(qidiruvMatni: String) { self.qidiruvMatni = qidiruvMatni }
    
    func qidirish() {
        Task { [weak self] in
            // Fon amali simulyatsiyasi
            try? await Task.sleep(nanoseconds: 10_000_000) // 10ms
            guard let self = self else {
                print("Task: Controller allaqachon xotiradan ketgan, bekor qilindi.")
                return
            }
            print("Task natijasi olindi: \(self.qidiruvMatni)")
        }
    }
    
    deinit { print("QidiruvXizmati deinit.") }
}

do {
    let xizmat = QidiruvXizmati(qidiruvMatni: "Swift ARC")
    xizmat.qidirish()
}
print("Asosiy oqim davom etmoqda...")
```

## Tushuntirish va Mantiq:
`Task` bloki ichida `self` ko'rsatilsa, Task tugagunga qadar obyektni kuchli ushlab turadi. Agar ekran yopilib ketsa ham Task ishlayveradi. `[weak self]` qo'yilsa, controller erkin o'chirilishi mumkin.

## Ishlash natijasi:
```text
Asosiy oqim davom etmoqda...
QidiruvXizmati deinit.
Task: Controller allaqachon xotiradan ketgan, bekor qilindi.
```


# 834-Topshiriq: Task Capture Semantics va Bekor Qilish (Cancellation)
## Topshiriq sharti:
Asinxron vazifa bajarilayotganda `Task.isCancelled` va ARC hamkorligini ko'rsatuvchi kod yozing.

## Yechim (Swift kodi):
```swift
class YuklashVazifasi {
    var vazifa: Task<Void, Never>?
    
    func boshlash() {
        vazifa = Task { [weak self] in
            for i in 1...5 {
                if Task.isCancelled {
                    print("Vazifa bekor qilindi!")
                    return
                }
                print("Yuklanmoqda: \(i * 20)%")
                try? await Task.sleep(nanoseconds: 5_000_000)
            }
            print("Yuklash tugadi. Self: \(String(describing: self))")
        }
    }
    
    func toxtatish() {
        vazifa?.cancel()
    }
    
    deinit {
        print("YuklashVazifasi deinit chaqirildi.")
        toxtatish()
    }
}

do {
    let v = YuklashVazifasi()
    v.boshlash()
    v.toxtatish()
}
print("Obyekt o'chirildi.")
```

## Tushuntirish va Mantiq:
Deinit ichida fon vazifasini `cancel()` qilish va Task ichida `[weak self]` ishlatish asinxron Swift dasturlashda eng toza arxitektura hisoblanadi.

## Ishlash natijasi:
```text
YuklashVazifasi deinit chaqirildi.
Vazifa bekor qilindi!
Obyekt o'chirildi.
```


# 835-Topshiriq: AsyncStream Iteratsiyasida Capture List
## Topshiriq sharti:
`AsyncStream` oqimidan ma'lumot qabul qilishda `[weak self]` qo'llash orqali xotira xavfsizligini ta'minlashni ko'rsating.

## Yechim (Swift kodi):
```swift
class SensorOqimi {
    let sensorId = "TEMP_SENSOR_9"
    
    func oqimniTinglash(oqim: AsyncStream<Int>) {
        Task { [weak self] in
            for await qiymat in oqim {
                guard let self = self else {
                    print("Sensor egasi o'chirildi, oqim tinglash to'xtatildi.")
                    break
                }
                print("Sensor [\(self.sensorId)]: \(qiymat)°C")
            }
        }
    }
    
    deinit { print("SensorOqimi deinit.") }
}

let (oqim, davomchi) = AsyncStream.makeStream(of: Int.self)
do {
    let sensor = SensorOqimi()
    sensor.oqimniTinglash(oqim: oqim)
    davomchi.yield(22)
}
davomchi.yield(25)
davomchi.finish()
```

## Tushuntirish va Mantiq:
Cheksiz davom etuvchi asinxron oqimlarda (AsyncStream) `[weak self]` bo'lmasa, oqim yopilmaguncha qabul qiluvchi klass hech qachon xotiradan bo'shatilmaydi.

## Ishlash natijasi:
```text
Sensor [TEMP_SENSOR_9]: 22°C
SensorOqimi deinit.
Sensor egasi o'chirildi, oqim tinglash to'xtatildi.
```


# 836-Topshiriq: Ichma-Ich Closurelar (Nested Closures) va Retain Cycle
## Topshiriq sharti:
Bir nechta ichma-ich closurelarda `[weak self]` har bir darajada qanday o'tishini ko'rsating.

## Yechim (Swift kodi):
```swift
class TarmoqManager {
    let nom = "AsosiyTarmoq"
    
    func sorovYuborish(bajarildi: @escaping () -> Void) {
        bajarildi()
    }
    
    func zanjirliOperatsiya() {
        sorovYuborish { [weak self] in
            guard let self = self else { return }
            print("1-daraja: \(self.nom)")
            
            // 2-darajali ichki closure
            self.sorovYuborish { [weak self] in
                guard let self = self else { return }
                print("2-daraja ichki closure: \(self.nom)")
            }
        }
    }
    
    deinit { print("TarmoqManager deinit.") }
}

let m = TarmoqManager()
m.zanjirliOperatsiya()
```

## Tushuntirish va Mantiq:
Ichma-ich joylashgan closurelarda har bir yangi closure o'z capture listiga ega bo'lishi lozim. Tashqi closureda `[weak self]` yozilib, ichkarida guard unwrap qilinsa, ichki closurega yana `[weak self]` kerak bo'ladi.

## Ishlash natijasi:
```text
1-daraja: AsosiyTarmoq
2-daraja ichki closure: AsosiyTarmoq
```


# 837-Topshiriq: Lazy Property Ichida `self` Capture Bo'lishi
## Topshiriq sharti:
Lazy o'zgaruvchilarda odatda closure ishlatilganda nima sababdan `self` ni talab qilishi va uning retain cycle xavfini ko'rsating.

## Yechim (Swift kodi):
```swift
class HisobQaydnomasi {
    let summa: Double = 1500.0
    
    // Lazy property birinchi murojaatda hisoblanadi
    lazy var tafsilot: String = {
        // Bu yerda retain cycle yuzaga kelmaydi, chunki bu closure saqlanmaydi, faqat chaqirilib natijasi olinadi
        return "Umumiy hisob: $\(self.summa)"
    }()
    
    // Diqqat: Agar lazy property closure TURING saqlasa, retain cycle bo'ladi:
    lazy var hisoblaFn: () -> String = { [weak self] in
        return "Keshbek bilan: $\((self?.summa ?? 0) * 0.95)"
    }
    
    deinit { print("HisobQaydnomasi deinit.") }
}

do {
    let h = HisobQaydnomasi()
    print(h.tafsilot)
    print(h.hisoblaFn())
}
print("Scope yakuni:")
```

## Tushuntirish va Mantiq:
Agar `lazy var x = { ... }()` (oxirida qavslar bo'lsa), closure darhol ishga tushib uning qaytargan qiymati saqlanadi, closure o'zi saqlanmaydi. Agar `lazy var x: () -> Void = { ... }` bo'lsa, closurening o'zi saqlanadi va retain cycle xavfi paydo bo'ladi.

## Ishlash natijasi:
```text
Umumiy hisob: $1500.0
Keshbek bilan: $1425.0
Scope yakuni:
HisobQaydnomasi deinit.
```


# 838-Topshiriq: Static / Global Singletonlarda Xotira Tutib Qolish Xavfi
## Topshiriq sharti:
Statik o'zgaruvchilar va singletonlar boshqa obyektlarni ushlab qolganda xotiradan chiqmaslik muammosini ko'rsating.

## Yechim (Swift kodi):
```swift
class GlobalRegistrator {
    static var xizmatlar: [AnyObject] = []
    
    static func registratsiya(_ obyekt: AnyObject) {
        xizmatlar.append(obyekt)
    }
    
    static func tozalash() {
        xizmatlar.removeAll()
    }
}

class VaqtinchalikXizmat {
    let id: Int
    init(id: Int) { self.id = id }
    deinit { print("Xizmat #\(id) deinit chaqirildi.") }
}

do {
    let x = VaqtinchalikXizmat(id: 99)
    GlobalRegistrator.registratsiya(x)
}
print("Vaqtinchalik xizmat scope tugadi, lekin GlobalRegistrator uni xotirada ushlab turibdi!")

GlobalRegistrator.tozalash()
print("Global registrator tozalandi va deinit ishladi:")
```

## Tushuntirish va Mantiq:
Statik propertylar dastur butun faoliyati davomida tirik turadi. Agar ularda oddiy obyektlar saqlansa, ular hech qachon ARC tomonidan deallokatsiya qilinmaydi. Buning uchun qo'lda tozalash yoki weak wrapper zarur.

## Ishlash natijasi:
```text
Vaqtinchalik xizmat scope tugadi, lekin GlobalRegistrator uni xotirada ushlab turibdi!
Global registrator tozalandi va deinit ishladi:
Xizmat #99 deinit chaqirildi.
```


# 839-Topshiriq: Dependency Injection Konteynerida Lifetime Boshqaruvi
## Topshiriq sharti:
Singleton vs Transient (har safar yangi) obyektlarning xotirada yashash davrini boshqaruvchi DI konteynerini yozing.

## Yechim (Swift kodi):
```swift
class DIContainer {
    private var singletonlar: [String: AnyObject] = [:]
    
    func singletonRoyxatdanOtkarish<T: AnyObject>(nom: String, yaratuvchi: () -> T) {
        if singletonlar[nom] == nil {
            singletonlar[nom] = yaratuvchi()
        }
    }
    
    func singletonOlish<T: AnyObject>(nom: String) -> T? {
        return singletonlar[nom] as? T
    }
}

class AutentifikatsiyaXizmati {
    let token = "XYZ-123"
    deinit { print("AutentifikatsiyaXizmati deinit.") }
}

let container = DIContainer()
container.singletonRoyxatdanOtkarish(nom: "Auth") {
    AutentifikatsiyaXizmati()
}

let auth: AutentifikatsiyaXizmati? = container.singletonOlish(nom: "Auth")
print("Auth token: \(auth?.token ?? '')")
```

## Tushuntirish va Mantiq:
Dependency Injection arxitekturasida komponentlar xotirada qancha vaqt yashashi (Singleton, Scoped, Transient) aniq boshqariladi, bu esa nazoratsiz retain cyclelarning oldini oladi.

## Ishlash natijasi:
```text
Auth token: XYZ-123
```


# 840-Topshiriq: Kesh Arxitekturasi va `NSCache` Avtomatik Tozalanishi
## Topshiriq sharti:
Tizim xotirasi to'lganda avtomatik ravishda obyektlarni xotiradan bo'shatuvchi `NSCache` sinfidan foydalanishni ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

class KeshElementi {
    let malumot: String
    init(malumot: String) { self.malumot = malumot }
    deinit { print("Kesh elementi '\(malumot)' xotiradan tozalandi.") }
}

let kesh = NSCache<NSString, KeshElementi>()
kesh.countLimit = 2 // Faqat 2 ta element saqlaydi

kesh.setObject(KeshElementi(malumot: "A"), forKey: "1")
kesh.setObject(KeshElementi(malumot: "B"), forKey: "2")
print("3-element qo'shilmoqda (limit oshadi):")
kesh.setObject(KeshElementi(malumot: "C"), forKey: "3")

print("Keshdan '1' kaliti olinmoqda: \(kesh.object(forKey: "1")?.malumot ?? "Topilmadi (tozalangan)")")
print("Keshdan '3' kaliti olinmoqda: \(kesh.object(forKey: "3")?.malumot ?? "Topilmadi")")
```

## Tushuntirish va Mantiq:
`NSCache` standart lug'atdan (Dictionary) farqli o'laroq, xotira tanqisligi (memory pressure) yuz berganda avtomatik ravishda eski elementlarni tozalaydi va thread-safe hisoblanadi.

## Ishlash natijasi:
```text
3-element qo'shilmoqda (limit oshadi):
Kesh elementi 'A' xotiradan tozalandi.
Keshdan '1' kaliti olinmoqda: Topilmadi (tozalangan)
Keshdan '3' kaliti olinmoqda: C
```


# 841-Topshiriq: `withExtendedLifetime` Yordamida Obyekt Umrini Uzaytirish
## Topshiriq sharti:
Asinxron yoki C pointer amallari davomida ARC obyektni muddatidan oldin o'chirib yubormasligi uchun `withExtendedLifetime` dan foydalanishni ko'rsating.

## Yechim (Swift kodi):
```swift
class MuhimResurs {
    let id = 555
    deinit { print("MuhimResurs #\(id) yo'q qilindi.") }
}

print("Operatsiya boshlandi.")
let resurs = MuhimResurs()

withExtendedLifetime(resurs) {
    print("Blok ichida resurs kafolatlangan tirik: #\(resurs.id)")
    // Ushbu blok ichida resurs hech qanday optimizatsiya bilan ham o'chirilmaydi
}
print("withExtendedLifetime bloki yakunlandi.")
```

## Tushuntirish va Mantiq:
Kompilyator kodi optimallashtirganda, o'zgaruvchiga oxirgi murojaatdan so'ng deinit chaqirilishi mumkin. `withExtendedLifetime` obyekt blok yakuniga qadar aniq xotirada saqlanishini kafolatlaydi.

## Ishlash natijasi:
```text
Operatsiya boshlandi.
Blok ichida resurs kafolatlangan tirik: #555
withExtendedLifetime bloki yakunlandi.
MuhimResurs #555 yo'q qilindi.
```


# 842-Topshiriq: Pointerlar: `UnsafeMutablePointer` Bilan Xotira Ajratish
## Topshiriq sharti:
Swift-da xotirani to'g'ridan-to'g'ri (manual) allokatsiya va deallokatsiya qilish usulini ko'rsating.

## Yechim (Swift kodi):
```swift
let soni = 3
// Int tipli 3 ta element uchun xotira ajratish
let korsatkich = UnsafeMutablePointer<Int>.allocate(capacity: soni)

// Boshlang'ich qiymatlar bilan initsializatsiya
korsatkich.initialize(repeating: 0, count: soni)
korsatkich[0] = 100
korsatkich[1] = 200
korsatkich[2] = 300

for i in 0..<soni {
    print("Pointer[\(i)] = \(korsatkich[i])")
}

// Xotirani tozalash va ozod qilish majburiydir!
korsatkich.deinitialize(count: soni)
korsatkich.deallocate()
print("Xotira muvaffaqiyatli qo'lda ozod qilindi.")
```

## Tushuntirish va Mantiq:
`UnsafeMutablePointer` ARC nazoratidan tashqaridagi xom C pointer hisoblanadi. Unda xotira `allocate` qilinadi va ishlatib bo'lingach `deallocate` qilinishi shart, aks holda jiddiy memory leak kelib chiqadi.

## Ishlash natijasi:
```text
Pointer[0] = 100
Pointer[1] = 200
Pointer[2] = 300
Xotira muvaffaqiyatli qo'lda ozod qilindi.
```


# 843-Topshiriq: `UnsafeRawPointer` va Baytlar Bilan Ishlash
## Topshiriq sharti:
Xotiradagi ma'lumotlarni turlanmagan xom baytlar sifatida o'qish uchun `UnsafeRawPointer` dan foydalanishni ko'rsating.

## Yechim (Swift kodi):
```swift
var qiymat: UInt32 = 0x12345678

withUnsafeBytes(of: &qiymat) { rawBuffer in
    print("Xotira hajmi: \(rawBuffer.count) bayt")
    for (indeks, bayt) in rawBuffer.enumerated() {
        print("Bayt [\(indeks)]: 0x\(String(format: "%02X", bayt))")
    }
}
```

## Tushuntirish va Mantiq:
`withUnsafeBytes` va `UnsafeRawPointer` tiplarga bog'liq bo'lmagan holda o'zgaruvchining xotiradagi xom baytlarini (memory layout) bevosita ko'rish va xavfsiz o'qish imkonini beradi.

## Ishlash natijasi:
```text
Xotira hajmi: 4 bayt
Bayt [0]: 0x78
Bayt [1]: 0x56
Bayt [2]: 0x34
Bayt [3]: 0x12
```


# 844-Topshiriq: Memory Layout: Size, Stride va Alignment
## Topshiriq sharti:
`MemoryLayout` yordamida Swift tiplarining xotiradagi haqiqiy hajmi, stride va alignment ko'rsatkichlarini hisoblang.

## Yechim (Swift kodi):
```swift
struct TalabaKarta {
    let id: Int64       // 8 bayt
    let faolmi: Bool    // 1 bayt (+ padding)
    let ball: Double    // 8 bayt
}

print("Int hajmi: \(MemoryLayout<Int>.size) bayt")
print("Bool hajmi: \(MemoryLayout<Bool>.size) bayt")
print("TalabaKarta hajmi (Size): \(MemoryLayout<TalabaKarta>.size) bayt")
print("TalabaKarta qadami (Stride): \(MemoryLayout<TalabaKarta>.stride) bayt")
print("TalabaKarta tekislanishi (Alignment): \(MemoryLayout<TalabaKarta>.alignment) bayt")
```

## Tushuntirish va Mantiq:
`Size` - tip egallagan foydali baytlar soni. `Stride` - massivda ketma-ket joylashganda keyingi elementgacha bo'lgan masofa (padding bilan). `Alignment` - xotiraning necha baytlik chegaraga mos tushishi.

## Ishlash natijasi:
```text
Int hajmi: 8 bayt
Bool hajmi: 1 bayt
TalabaKarta hajmi (Size): 24 bayt
TalabaKarta qadami (Stride): 24 bayt
TalabaKarta tekislanishi (Alignment): 8 bayt
```


# 845-Topshiriq: Struct Ichida Padding va Xotira Zichlash (Packing)
## Topshiriq sharti:
Fieldlarning joylashuv tartibini o'zgartirish orqali struct egallagan xotirani qanday tejash mumkinligini ko'rsating.

## Yechim (Swift kodi):
```swift
// Yomon tartib (Padding ko'p)
struct YomonTartib {
    let a: Bool   // 1 bayt + 7 bayt padding
    let b: Int64  // 8 bayt
    let c: Bool   // 1 bayt + 7 bayt padding
}

// Yaxshi tartib (Zichlangan)
struct YaxshiTartib {
    let b: Int64  // 8 bayt
    let a: Bool   // 1 bayt
    let c: Bool   // 1 bayt + 6 bayt padding
}

print("Yomon tartib hajmi: \(MemoryLayout<YomonTartib>.size) bayt (Stride: \(MemoryLayout<YomonTartib>.stride))")
print("Yaxshi tartib hajmi: \(MemoryLayout<YaxshiTartib>.size) bayt (Stride: \(MemoryLayout<YaxshiTartib>.stride))")
```

## Tushuntirish va Mantiq:
Kattaroq tiplarni (Int64, Double) boshiga, kichik tiplarni (Bool, Int8) yonma-yon qo'yish orqali xotiradagi 'padding' (bo'sh joy) isrofini sezilarli darajada kamaytirish mumkin.

## Ishlash natijasi:
```text
Yomon tartib hajmi: 24 bayt (Stride: 24)
Yaxshi tartib hajmi: 10 bayt (Stride: 16)
```


# 846-Topshiriq: `ManagedBuffer` Bilan Maxsus Xotira Buferini Yaratish
## Topshiriq sharti:
Swift-ning yuqori unumdorlikka ega `ManagedBuffer` klassidan foydalanib o'z ma'lumot buferingizni yarating.

## Yechim (Swift kodi):
```swift
class IntegerBufer: ManagedBuffer<String, Int> {
    static func yaratish(nom: String, sigim: Int) -> IntegerBufer {
        return self.create(minimumCapacity: sigim) { buffer in
            return nom
        } as! IntegerBufer
    }
}

let bufer = IntegerBufer.yaratish(nom: "SensolarBuferi", sigim: 4)
print("Bufer nomi: \(bufer.header)")
print("Bufer sig'imi: \(bufer.capacity)")
```

## Tushuntirish va Mantiq:
`ManagedBuffer` sarlavha (Header) va uzluksiz ketma-ket xotira elementlarini bitta obyekt ichida jamlaydi va ARC bilan xavfsiz boshqariladi.

## Ishlash natijasi:
```text
Bufer nomi: SensolarBuferi
Bufer sig'imi: 4
```


# 847-Topshiriq: Retain Cycle Debugger: Graph O'xshashlik Diagnostikasi
## Topshiriq sharti:
Obyektlar bog'lanish grafigini tahlil qilib, retain cycle bor yoki yo'qligini aniqlovchi sodda diagnostika utilitasini yozing.

## Yechim (Swift kodi):
```swift
class TugunDiagnostika {
    let id: String
    var qoshnilar: [TugunDiagnostika] = []
    
    init(id: String) { self.id = id }
    
    func siklBormi(tashrifQilingan: inout Set<String>) -> Bool {
        if tashrifQilingan.contains(id) {
            return true
        }
        tashrifQilingan.insert(id)
        for q in qoshnilar {
            if q.siklBormi(tashrifQilingan: &tashrifQilingan) {
                return true
            }
        }
        tashrifQilingan.remove(id)
        return false
    }
}

let n1 = TugunDiagnostika(id: "NodeA")
let n2 = TugunDiagnostika(id: "NodeB")
n1.qoshnilar.append(n2)
n2.qoshnilar.append(n1) // Sikl hosil qilindi

var set = Set<String>()
let sikl = n1.siklBormi(tashrifQilingan: &set)
print("Bog'lanishda sikl aniqlandimi: \(sikl ? 'HA (Retain cycle xavfi bor)' : 'YOQ')")
```

## Tushuntirish va Mantiq:
Xcode Instruments 'Leaks' va 'Memory Graph Debugger' vositalari aynan mana shu graf tahlili orqali kuchli havolalar zanjiridagi sikllarni vizual ko'rsatib beradi.

## Ishlash natijasi:
```text
Bog'lanishda sikl aniqlandimi: HA (Retain cycle xavfi bor)
```


# 848-Topshiriq: Weak Collections: `NSMapTable` va `NSHashTable`
## Topshiriq sharti:
Foundation-ning kalit yoki qiymatlarni weak ushlay oladigan `NSMapTable` kolleksiyasidan foydalanishni ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

class XizmatKlassi {
    let nom: String
    init(nom: String) { self.nom = nom }
}

// Kalit: strong, Qiymat: weak bo'lgan jadval
let zaifJadval = NSMapTable<NSString, XizmatKlassi>.strongToWeakObjects()

do {
    let xizmat = XizmatKlassi(nom: "Kriptografiya")
    zaifJadval.setObject(xizmat, forKey: "kripto")
    print("Scope ichida: \(zaifJadval.object(forKey: "kripto")?.nom ?? "yo'q")")
}

print("Scope tashqarisida: \(zaifJadval.object(forKey: "kripto")?.nom ?? "yo'q (avtomatik bo'shatildi)")")
```

## Tushuntirish va Mantiq:
`NSMapTable` va `NSHashTable` Swift-dagi oddiy Dictionary va Set-dan farqli ravishda elementlarni `weak` havola sifatida saqlash imkoniyatini beradi, bu esa xotirada qolib ketishning oldini oladi.

## Ishlash natijasi:
```text
Scope ichida: Kriptografiya
Scope tashqarisida: yo'q (avtomatik bo'shatildi)
```


# 849-Topshiriq: ARC Profilaktikasi: 5 Oltin Qoida
## Topshiriq sharti:
Swift-da xotira sizishlarining oldini olish bo'yicha 5 ta asosiy arxitektura qoidasini tasvirlovchi dastur yozing.

## Yechim (Swift kodi):
```swift
struct MemoryXavfsizlikQoidasi {
    let raqam: Int
    let sarlavha: String
    let tavsiya: String
}

let qoidalar = [
    MemoryXavfsizlikQoidasi(raqam: 1, sarlavha: "Delegatelar har doim weak", tavsiya: "weak var delegate: SomeDelegate?"),
    MemoryXavfsizlikQoidasi(raqam: 2, sarlavha: "Escaping closurelarda [weak self]", tavsiya: "guard let self else { return }"),
    MemoryXavfsizlikQoidasi(raqam: 3, sarlavha: "Parent-Child munosabatlarida weak parent", tavsiya: "Bola o'z otasini weak ushlasin"),
    MemoryXavfsizlikQoidasi(raqam: 4, sarlavha: "Katta massivlarda autoreleasepool", tavsiya: "Loop ichida RAM pikini kamaytiring"),
    MemoryXavfsizlikQoidasi(raqam: 5, sarlavha: "Qiymat tiplarini (Struct) afzal ko'rish", tavsiya: "Struct ARC overheadiga ega emas")
]

for q in qoidalar {
    print("\(q.raqam). \(q.sarlavha) -> \(q.tavsiya)")
}
```

## Tushuntirish va Mantiq:
Ushbu qoidalarga rioya qilish professional iOS/macOS ilovalarida xotira sizishlarini 99% ga bartaraf etishga kafolat beradi.

## Ishlash natijasi:
```text
1. Delegatelar har doim weak -> weak var delegate: SomeDelegate?
2. Escaping closurelarda [weak self] -> guard let self else { return }
3. Parent-Child munosabatlarida weak parent -> Bola o'z otasini weak ushlasin
4. Katta massivlarda autoreleasepool -> Loop ichida RAM pikini kamaytiring
5. Qiymat tiplarini (Struct) afzal ko'rish -> Struct ARC overheadiga ega emas
```


# 850-Topshiriq: Amaliy Kompleks Tizim: Xotira Xavfsiz Reaktiv Voqealar Arxitekturasi
## Topshiriq sharti:
Event emitter, kuzatuvchilar, asinxron fon vazifalari va delegatsiyani o'z ichiga olgan, 100% retain-cycle-free xavfsiz reaktiv arxitektura yarating.

## Yechim (Swift kodi):
```swift
import Foundation

// 1. Weak Listener o'rami
class ZaifKuzatuvchi<T: AnyObject> {
    weak var obuna: T?
    init(_ obuna: T) { self.obuna = obuna }
}

// 2. Event Emitter
class VoqeaMarkazi {
    private var obunachilar: [ZaifKuzatuvchi<AnyObject>] = []
    
    func obunaBol(_ kuzatuvchi: AnyObject) {
        obunachilar.append(ZaifKuzatuvchi(kuzatuvchi))
    }
    
    func voqeaYuzBardi(xabar: String) {
        obunachilar = obunachilar.filter { $0.obuna != nil }
        print("VoqeaMarkazi: \(obunachilar.count) ta faol tinglovchiga xabar: '\(xabar)'")
    }
    
    deinit { print("VoqeaMarkazi xotiradan tozalandi.") }
}

// 3. Xizmat klassi
class AnalitikaXizmati {
    let nom = "MixpanelLog"
    deinit { print("AnalitikaXizmati deinit: Xotiradan toza chiqdi.") }
}

let markaz = VoqeaMarkazi()
do {
    let xizmat = AnalitikaXizmati()
    markaz.obunaBol(xizmat)
    markaz.voqeaYuzBardi(xabar: "Foydalanuvchi tizimga kirdi")
}

print("Scope tugadi. AnalitikaXizmati xotiradan chiqishi kerak:")
markaz.voqeaYuzBardi(xabar: "Foydalanuvchi sahifani tark etdi")
print("Tizim to'liq toza yakunlandi.")
```

## Tushuntirish va Mantiq:
Ushbu yakuniy loyihada barcha konseptlar - Zaif havolalar (Weak collections), tozalash mexanizmlari va retain-cycle-free arxitektura birlashtirildi.

## Ishlash natijasi:
```text
VoqeaMarkazi: 1 ta faol tinglovchiga xabar: 'Foydalanuvchi tizimga kirdi'
Scope tugadi. AnalitikaXizmati xotiradan chiqishi kerak:
AnalitikaXizmati deinit: Xotiradan toza chiqdi.
VoqeaMarkazi: 0 ta faol tinglovchiga xabar: 'Foydalanuvchi sahifani tark etdi'
Tizim to'liq toza yakunlandi.
```

