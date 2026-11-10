# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

tasks_data = [
    (
        51,
        "Optional tushunchasi va e'lon qilish",
        "Foydalanuvchining o'rta ismi bo'lishi yoki bo'lmasligi mumkin. Uni ifodalovchi Optional String e'lon qiling.",
        """import Foundation

var middleName: String? = nil
print("Boshlang'ich holat: \\(String(describing: middleName))")

middleName = "Karimovich"
print("Qiymat biriktirilgandan keyin: \\(String(describing: middleName))")
""",
        "Swift-da har qanday tip nomidan so'ng so'roq belgisi (?) qo'yilsa, u Optional turiga aylanadi. Bu ushbu o'zgaruvchi yo tegishli qiymatni, yoki 'nil' (qiymat yo'qligi)ni saqlashi mumkinligini bildiradi.",
        """Boshlang'ich holat: nil
Qiymat biriktirilgandan keyin: Optional("Karimovich")"""
    ),
    (
        52,
        "Optionals ichki arxitekturasi: Optional enum va .none / .some",
        "Swift-dagi Optional aslida ikkita holatga ega Generic Enum ekanligini ko'rsatuvchi dastur yozing.",
        """import Foundation

let explicitNone: Optional<Int> = Optional.none
let explicitSome: Optional<Int> = Optional.some(42)

switch explicitSome {
case .some(let value):
    print("Mavjud qiymat: \\(value)")
case .none:
    print("Qiymat yo'q (nil)")
}
""",
        "Swift-da 'T?' sintaksisi 'Optional<T>' enumining qisqartmasidir. Unda faqat ikkita holat bor: '.none' (nil ga teng) va '.some(Wrapped)' (haqiqiy qiymatni o'z ichiga olgan quti).",
        """Mavjud qiymat: 42"""
    ),
    (
        53,
        "Majburiy ochish (Forced Unwrapping: !) va xavfi",
        "Optional qutisini majburiy ochish (!) va nil bo'lganda yuzaga keladigan halokatli xatoni tushuntiring.",
        """import Foundation

let serverPort: Int? = 8080

// Qiymat borligiga 100% ishonch bo'lsa:
let unwrappedPort: Int = serverPort!
print("Ochiq port: \\(unwrappedPort)")

// Agar serverPort = nil bo'lib, serverPort! qilinsa, dastur fatal error beradi.
""",
        "Undov belgisi (!) majburiy ochish (forced unwrapping) operatoridir. Agar o'zgaruvchi nil bo'lsa, bu amal darhol Fatal Crash keltirib chiqaradi. Shuning uchun professional Swift kodida bu usuldan qat'iyan saqlanish tavsiya etiladi.",
        """Ochiq port: 8080"""
    ),
    (
        54,
        "Klassik Optional Binding: 'if let'",
        "Foydalanuvchi kiritgan elektron pochtani 'if let' orqali xavfsiz ochib tekshiring.",
        """import Foundation

let emailInput: String? = "dev@khorazmiy.uz"

if let validEmail = emailInput {
    print("Xush kelibsiz! Pochta: \\(validEmail.lowercased())")
} else {
    print("Elektron pochta manzili ko'rsatilmadi.")
}
""",
        "'if let' konstruktsiyasi Optional qiymatni tekshiradi: agar u nil bo'lmasa, uni vaqtinchalik o'zgarmasga ochadi va blok ichida to'g'ridan-to'g'ri xavfsiz ishlatish imkonini beradi.",
        """Xush kelibsiz! Pochta: dev@khorazmiy.uz"""
    ),
    (
        55,
        "Swift 5.7+ Shorthand 'if let' sintaksisi",
        "Swift 5.7 versiyasida qo'shilgan ixcham 'if let varName' sintaksisini qo'llang.",
        """import Foundation

let username: String? = "Ulugbek"

// Eski usul: if let username = username
// Swift 5.7+ ixcham usul:
if let username {
    print("Foydalanuvchi tizimga kirdi: \\(username)")
}
""",
        "Swift 5.7 dan boshlab, agar ochilayotgan o'zgarmas nomi optional o'zgaruvchi nomi bilan bir xil bo'lsa, 'if let nom' shaklida yozish mumkin, bu kodni ancha toza qiladi.",
        """Foydalanuvchi tizimga kirdi: Ulugbek"""
    ),
    (
        56,
        "Erta chiqish (Early Exit): 'guard let' operatori",
        "Funksiyada kerakli parametr mavjud bo'lmasa ishni erta to'xtatuvchi 'guard let' mexanizmini yozing.",
        """import Foundation

func processPayment(apiKey: String?, amount: Double) {
    guard let key = apiKey, !key.isEmpty else {
        print("Xatolik: API kalit taqdim etilmadi!")
        return
    }
    
    // key bu yerda butun funksiya oxirigacha oddiy String sifatida amal qiladi
    print("To'lov amalga oshirildi: $\\(amount), Kalit: \\(key)")
}

processPayment(apiKey: "API_SECRET_991", amount: 250.0)
processPayment(apiKey: nil, amount: 100.0)
""",
        "'guard let' shart bajarilmaganda majburiy ravishda oqimdan chiqishni (return, throw, break) talab qiladi. Eng katta afzalligi: ochilgan qiymat guard blokidan keyin ham ko'rinish sohasida (scope) qoladi.",
        """To'lov amalga oshirildi: $250.0, Kalit: API_SECRET_991
Xatolik: API kalit taqdim etilmadi!"""
    ),
    (
        57,
        "Bir nechta Optionallarni bir vaqtda ochish",
        "Bir nechta optional qiymatlarni bitta 'if let' qatorida tekshirib oching.",
        """import Foundation

let firstName: String? = "Alisher"
let lastName: String? = "Navoiy"
let birthYear: Int? = 1441

if let firstName, let lastName, let birthYear {
    print("Buyuk alloma: \\(firstName) \\(lastName), \\(birthYear)-yilda tug'ilgan.")
}
""",
        "Vergul bilan ajratilgan bir nechta optional tekshiruvlar barchasi nil bo'lmagandagina blok ichidagi kod bajariladi (mantiqiy AND tamoyili).",
        """Buyuk alloma: Alisher Navoiy, 1441-yilda tug'ilgan."""
    ),
    (
        58,
        "Nil-Coalescing operatori: '??'",
        "Foydalanuvchi taxallusi kiritilmagan bo'lsa standart 'Mehmon' qiymatini beruvchi ifoda tuzing.",
        """import Foundation

let inputNickname: String? = nil
let displayName = inputNickname ?? "Mehmon"

print("Salom, \\(displayName)!")
""",
        "Nil-coalescing ('??') operatori optional qiymat nil bo'lmaganda uning ichidagi qiymatni ochadi, agar nil bo'lsa o'ng tarafdagi standart (default) qiymatni qaytaradi.",
        """Salom, Mehmon!"""
    ),
    (
        59,
        "Zanjirli Nil-Coalescing (Chained '??')",
        "Bir nechta manbalardan (kesh, lokal baza, server) qiymat qidirish zanjirini tuzing.",
        """import Foundation

let memoryCache: String? = nil
let diskCache: String? = "Lokal xotiradagi rasm"
let defaultPlaceholder = "Standart placeholder.png"

let finalImage = memoryCache ?? diskCache ?? defaultPlaceholder
print("Yuklangan rasm: \\(finalImage)")
""",
        "Nil-coalescing operatorini zanjir shaklida ulab, birinchi uchragan nil bo'lmagan qiymatni tanlab olish mumkin.",
        """Yuklangan rasm: Lokal xotiradagi rasm"""
    ),
    (
        60,
        "Optional Chaining asoslari: '?.'",
        "Obyekt xususiyatiga murojaat qilishda xavfsiz zanjir hosil qiling.",
        """import Foundation

class Profile {
    var bio: String = "iOS dasturchisi"
}

class User {
    var profile: Profile?
}

let user = User()
// Profil mavjud emas, lekin xato bermaydi:
print("Bio: \\(String(describing: user.profile?.bio))")

user.profile = Profile()
print("Bio mavjud: \\(user.profile?.bio ?? "Yo'q")")
""",
        "Optional Chaining ('?.') zanjirdagi ixtiyoriy bo'g'in nil bo'lsa, xatoliksiz butun ifodani xavfsiz to'xtatadi va nil qaytaradi.",
        """Bio: nil
Bio mavjud: iOS dasturchisi"""
    ),
    (
        61,
        "Ko'p qavatli chuqur Optional Chaining",
        "To'rt qavatli obyektlar bog'lanishida shahar nomini xavfsiz o'qing.",
        """import Foundation

class City { var name: String = "Samarqand" }
class Address { var city: City? = City() }
class Company { var headOffice: Address? = Address() }
class Employee { var company: Company? = Company() }

let dev = Employee()
if let cityName = dev.company?.headOffice?.city?.name {
    print("Xodim shirkati joylashgan shahar: \\(cityName)")
}
""",
        "Chuqur ierarxiyalarda agar biror bo'g'in nil bo'lsa, Swift qolgan barcha bosqichlarni tashlab o'tadi va ifoda xavfsiz yakunlanadi.",
        """Xodim shirkati joylashgan shahar: Samarqand"""
    ),
    (
        62,
        "Optional Chaining orqali metodlarni chaqirish",
        "Agar obyekt mavjud bo'lsa uning metodini chaqiruvchi, yo'q bo'lsa e'tiborsiz qoldiruvchi dastur tuzing.",
        """import Foundation

class SoundEngine {
    func playBeep() {
        print("BEEP! Signal chalindi.")
    }
}

var audioPlayer: SoundEngine? = nil
audioPlayer?.playBeep() // Hech narsa yuz bermaydi

audioPlayer = SoundEngine()
audioPlayer?.playBeep() // Endi ishlaydi
""",
        "Optional obyektning metodini '?.' orqali chaqirganda, agar obyekt nil bo'lsa metod umuman bajarilmaydi va Void? (ya'ni ()) qaytariladi.",
        """BEEP! Signal chalindi."""
    ),
    (
        63,
        "Optional Chaining orqali Subscriptga murojaat",
        "Lug'at ichidagi massiv elementini xavfsiz indekslashni ko'rsating.",
        """import Foundation

var testScores: [String: [Int]]? = ["Ali": [95, 88, 100]]

let firstScore = testScores?["Ali"]?[0]
print("Birinchi baho: \\(String(describing: firstScore))")

testScores = nil
let missingScore = testScores?["Ali"]?[0]
print("Mavjud bo'lmaganda: \\(String(describing: missingScore))")
""",
        "Subscript qavslaridan oldin '?[' qo'yish orqali ixtiyoriy to'plamdan xavfsiz element ajratib olish mumkin.",
        """Birinchi baho: Optional(95)
Mavjud bo'lmaganda: nil"""
    ),
    (
        64,
        "Optional Chaining orqali qiymat o'zgartirish (Mutating)",
        "Agar obyekt mavjud bo'lsa uning xususiyatiga yangi qiymat yozing.",
        """import Foundation

class Car {
    var speed: Int = 0
}

var garageCar: Car? = nil
garageCar?.speed = 120 // Hech qanday ta'sir yo'q, xato ham bermaydi

garageCar = Car()
garageCar?.speed = 120
print("Avtomobil tezligi: \\(garageCar?.speed ?? 0) km/soat")
""",
        "Optional zanjir orqali qiymat biriktirishga urinishda, agar zanjirdagi havola nil bo'lsa, o'ng tarafdagi ifoda hisoblanmaydi ham va hech qanday o'zgarish sodir bo'lmaydi.",
        """Avtomobil tezligi: 120 km/soat"""
    ),
    (
        65,
        "Implicitly Unwrapped Optionals (Type!)",
        "E'lon qilingan paytda qiymatga ega bo'lmaydigan, ammo keyinchalik doim mavjud bo'lishi kafolatlangan turni ko'rsating.",
        """import Foundation

var assumedString: String! = "Bu doim mavjud bo'lishi kutilgan satr."
let regularString: String = assumedString // Majburiy unwrap (!) shart emas!

print("To'g'ridan-to'g'ri qiymat: \\(regularString)")
""",
        "Implicitly Unwrapped Optional ('Type!') oddiy Optional kabi ishlaydi, biroq unga murojaat qilinganda Swift uni avtomatik ochadi. Agar u nil bo'lib qolsa, run-time crash beradi.",
        """To'g'ridan-to'g'ri qiymat: Bu doim mavjud bo'lishi kutilgan satr."""
    ),
    (
        66,
        "Implicitly Unwrapped Optionals qo'llanilish sohasi (IBOutlet)",
        "UIKit va Storyboard interfeys elementlarida nima uchun IUO ishlatilishini tushuntiruvchi model yozing.",
        """import Foundation

class ViewController {
    var submitButtonTitle: String! // View yuklanganda tizim tomonidan kiritiladi
    
    func viewDidLoad() {
        submitButtonTitle = "Tasdiqlash"
    }
    
    func render() {
        print("Tugma yozuvi: \\(submitButtonTitle)")
    }
}

let vc = ViewController()
vc.viewDidLoad()
vc.render()
""",
        "iOS dasturlashda UIKit interfeys komponentlari (IBOutlet) initsializatsiya vaqtida mavjud bo'lmaydi, lekin viewDidLoad bosqichida tizim ularni to'ldiradi. Shu bois IUO qulay vosita hisoblanadi.",
        """Tugma yozuvi: Tasdiqlash"""
    ),
    (
        67,
        "Optional Pattern Matching: 'case let x?'",
        "For tsikli ichida faqat nil bo'lmagan elementlarni pattern matching orqali saralab oling.",
        """import Foundation

let optionalNumbers: [Int?] = [10, nil, 25, nil, 40]

print("Faqat haqiqiy sonlar:")
for case let number? in optionalNumbers {
    print("- \\(number)")
}
""",
        "'for case let x? in collection' sintaksisi optional to'plamdan faqat mavjud qiymatlarni ochib oladi va nil bo'lgan elementlarni avtomatik tashlab yuboradi.",
        """Faqat haqiqiy sonlar:
- 10
- 25
- 40"""
    ),
    (
        68,
        "Switch-case da Optionals va 'where' sharti",
        "Switch operatorida Optional qiymatning turli holatlarini tahlil qiling.",
        """import Foundation

let responseCode: Int? = 404

switch responseCode {
case .none:
    print("Serverdan hech qanday javob kelmadi.")
case .some(let code) where code == 200:
    print("Muvaffaqiyatli: 200 OK")
case .some(let code) where code >= 400:
    print("Xatolik kodi: \\(code)")
case .some(let code):
    print("Boshqa holat: \\(code)")
}
""",
        "Switch operatorida Optionals bilan to'liq naqsh moslashtirish (pattern matching) va 'where' qo'shimcha shartlarini bevosita qo'llash mumkin.",
        """Xatolik kodi: 404"""
    ),
    (
        69,
        "Optional 'map' metodi bilan transformatsiya",
        "Optional ichidagi qiymatni ochmasdan (if-let siz) unga funksiya qo'llab o'zgartiring.",
        """import Foundation

let rawInput: String? = "120"
let doubled: Int? = rawInput.flatMap { Int($0) }.map { $0 * 2 }

print("Ikkilangan: \\(String(describing: doubled))")

let emptyInput: String? = nil
let emptyDoubled = emptyInput.map { "Salom " + $0 }
print("Bo'sh holatda map: \\(String(describing: emptyDoubled))")
""",
        "Optional.map funksiyasi agar qutida qiymat bo'lsa uni o'zgartiradi va yana yangi Optional qaytaradi. Agar quti nil bo'lsa, hech qanday amal bajarilmay nil qaytadi.",
        """Ikkilangan: Optional(240)
Bo'sh holatda map: nil"""
    ),
    (
        70,
        "Optional 'flatMap' metodi",
        "Transformatsiya natijasi ham Optional bo'lganda, ikki qavatli Optional (T??) hosil bo'lishini flatMap bilan bartaraf qiling.",
        """import Foundation

let textNumber: String? = "500"

// map qilsak: Int?(String?) -> Int?? (ikki qavatli optional)
// flatMap esa bitta qatlamga tekislaydi (flatten):
let parsedNumber: Int? = textNumber.flatMap { Int($0) }

print("Natija: \\(String(describing: parsedNumber))")
""",
        "'flatMap' metodi transformatsiya funksiyasi ixtiyoriy boshqa Optional qaytarganda natijani yagona qatlamli Optional<U> ko'rinishiga keltiradi.",
        """Natija: Optional(500)"""
    ),
    (
        71,
        "Where sharti bilan Optional ochish",
        "Optional ochish jarayonida uning qiymatini qo'shimcha mantiqiy mezon bilan tekshiring.",
        """import Foundation

let userAge: Int? = 21

if let age = userAge, age >= 18 {
    print("Foydalanuvchi balog'at yoshiga yetgan: \\(age) yosh")
} else {
    print("Ruxsat berilmadi yoki yosh kiritilmadi.")
}
""",
        "Swift-da if-let ichida verguldan so'ng qo'shimcha mantiqiy shartlarni bog'lash mumkin, bu bir nechta ichma-ich if bloklarini yo'qotadi.",
        """Foydalanuvchi balog'at yoshiga yetgan: 21 yosh"""
    ),
    (
        72,
        "Double Optionals (Ikki qavatli Optionals) tushunchasi",
        "Optional ichidagi Optional (masalan, Int??) qanday vujudga kelishini va uni tahlil qilishni ko'rsating.",
        """import Foundation

let dict: [String: Int?] = ["mavjud": 42, "bosh": nil]

let val1 = dict["mavjud"] // Turi: Int??
let val2 = dict["bosh"]   // Turi: Int??
let val3 = dict["yoq"]    // Turi: Int??

print("mavjud: \\(String(describing: val1))")
print("bosh: \\(String(describing: val2))")
print("yoq: \\(String(describing: val3))")
""",
        "Lug'atdan qiymat olish o'zi Optional qaytaradi. Agar lug'atdagi qiymatning o'zi ham Optional bo'lsa, natija 'Int??' (ikki qavatli) bo'ladi.",
        """mavjud: Optional(Optional(42))
bosh: Optional(nil)
yoq: nil"""
    ),
    (
        73,
        "Lug'atdan ma'lumot o'qishda Optionallik",
        "Lug'atda mavjud bo'lmagan kalit murojaat qilinganda qanday qilib xavfsiz default qiymat olishni ko'rsating.",
        """import Foundation

let userAges = ["Ali": 25, "Vali": 30]

let aliAge: Int? = userAges["Ali"]
let hasanAge: Int? = userAges["Hasan"]

print("Ali: \\(aliAge ?? 0)")
print("Hasan: \\(hasanAge ?? 0)")

// Lug'atning o'zidagi default parametri:
let directDefault = userAges["Gani", default: 18]
print("Gani: \\(directDefault)")
""",
        "Lug'at kalit orqali indekslanganda doimo Optional qiymat beradi, chunki izlangan kalit bo'lmasligi mumkin. 'dict[key, default: val]' orqali to'g'ridan-to'g'ri no-optional qiymat olish ham mumkin.",
        """Ali: 25
Hasan: 0
Gani: 18"""
    ),
    (
        74,
        "String dan Int ga o'tkazishdagi Optionallik",
        "Foydalanuvchi matn shaklida kiritgan sonni raqamga aylantirib hisoblang.",
        """import Foundation

let stringOne = "450"
let stringTwo = "yuz dollar"

if let num1 = Int(stringOne) {
    print("Muvaffaqiyatli o'girildi: \\(num1)")
}

if let num2 = Int(stringTwo) {
    print("O'girildi: \\(num2)")
} else {
    print("'\\(stringTwo)' son emas, aylantirib bo'lmadi.")
}
""",
        "'Int(str)' initsializatori 'Int?' (failable) qaytaradi, chunki kiritilgan satrda harflar yoki noto'g'ri belgilar bo'lishi mumkin.",
        """Muvaffaqiyatli o'girildi: 450
'yuz dollar' son emas, aylantirib bo'lmadi."""
    ),
    (
        75,
        "Massivning first va last xususiyatlari",
        "Massiv bo'sh bo'lgan holatda indeks xatosi olmaslik uchun 'first' xususiyatidan foydalaning.",
        """import Foundation

let emptyList: [String] = []
let filledList = ["Toshkent", "Buxoro"]

print("Bo'sh ro'yxat birinchi elementi: \\(String(describing: emptyList.first))")
print("To'la ro'yxat birinchi elementi: \\(filledList.first ?? "Mavjud emas")")
""",
        "Massivni 'arr[0]' bilan o'qish bo'sh massivda Crash beradi. 'arr.first' va 'arr.last' esa xavfsiz tarzda Element? (Optional) qaytaradi.",
        """Bo'sh ro'yxat birinchi elementi: nil
To'la ro'yxat birinchi elementi: Toshkent"""
    ),
    (
        76,
        "Kolleksiyada 'first(where:)' va Optional natija",
        "Ro'yxatdan muayyan mezon bo'yicha birinchi mos kelgan elementni xavfsiz toping.",
        """import Foundation

let scores = [45, 62, 85, 91, 55]

let topGrade = scores.first(where: { $0 >= 80 })
if let score = topGrade {
    print("80 dan yuqori birinchi ball: \\(score)")
}
""",
        "'first(where:)' berilgan shartga javob beradigan eng birinchi elementni Optional ko'rinishida qaytaradi, mos element topilmasa nil beradi.",
        """80 dan yuqori birinchi ball: 85"""
    ),
    (
        77,
        "Kolleksiyadan nillarni tozalash: 'compactMap'",
        "Matnlar massividan faqat muvaffaqiyatli songa aylanganlarini ajratib oling.",
        """import Foundation

let rawInputs = ["10", "Swift", "35", "iOS", "99"]
let validNumbers: [Int] = rawInputs.compactMap { Int($0) }

print("Tozalangan sonlar: \\(validNumbers)")
""",
        "'compactMap' har bir elementga berilgan transformatsiyani qo'llaydi, natijadagi nil qiymatlarni avtomatik o'chiradi va no-optional to'plam hosil qiladi.",
        """Tozalangan sonlar: [10, 35, 99]"""
    ),
    (
        78,
        "Enum Associated Values bilan Optionals uyg'unligi",
        "Server javob holatini Optionals bilan boyitilgan Enum orqali ifodalang.",
        """import Foundation

enum NetworkState {
    case loading
    case success(data: String)
    case failure(errorMsg: String?)
}

let currentState: NetworkState = .failure(errorMsg: "Server bilan aloqa uzildi.")

switch currentState {
case .loading:
    print("Yuklanmoqda...")
case .success(let data):
    print("Ma'lumot olindi: \\(data)")
case .failure(let error):
    print("Xato: \\(error ?? "Noma'lum sabab")")
}
""",
        "Swift Enumlarining 'associated values' qismida ixtiyoriy turlarni, shu jumladan Optionallarni bemalol ishlatish mumkin.",
        """Xato: Server bilan aloqa uzildi."""
    ),
    (
        79,
        "Optional Boolean bilan mantiqiy taqqoslash",
        "Optional Bool qiymatini shartlarda to'g'ri tekshirish usullarini ko'rsating.",
        """import Foundation

let isSubscribed: Bool? = nil

// Usul 1: Aniq tekshirish
if isSubscribed == true {
    print("Obuna faol")
} else {
    print("Obuna yo'q yoki noaniq")
}

// Usul 2: Nil-coalescing
if isSubscribed ?? false {
    print("Obuna faol")
}
""",
        "Optional Bool faqat 'true', 'false' emas, balki 'nil' ham bo'lishi mumkin (uch xil holat). Shu sababli 'if optBool' deb to'g'ridan-to'g'ri yozib bo'lmaydi.",
        """Obuna yo'q yoki noaniq"""
    ),
    (
        80,
        "Optional Casting ('as?') va Binding birgalikda",
        "Har qanday turdagi ob'ektni xavfsiz kerakli klassga aylantiring.",
        """import Foundation

let rawData: Any = [1, 2, 3, 4, 5]

if let array = rawData as? [Int] {
    print("Massiv elementlari soni: \\(array.count)")
}
""",
        "'as?' operatori agar ma'lumot kutilgan turga mos kelsa Optional(qiymat), aks holda nil qaytaradi. Bu 'if let' bilan birlashganda kuchli xavfsizlik yaratadi.",
        """Massiv elementlari soni: 5"""
    ),
    (
        81,
        "Optional Closures (Funksiya parametrlari)",
        "Tugma bosilganda chaqirilishi mumkin bo'lgan, ammo majburiy bo'lmagan callback closure tuzing.",
        """import Foundation

class CustomButton {
    var onTap: (() -> Void)?
    
    func press() {
        print("Tugma bosildi.")
        onTap?() // Agar closure berilgan bo'lsa chaqiriladi
    }
}

let btn = CustomButton()
btn.press()

btn.onTap = {
    print("Callback muvaffaqiyatli ishga tushdi!")
}
btn.press()
""",
        "Closure o'zgaruvchilari optional bo'lganda 'closure?()' shaklida chaqiriladi. Agar closure nil bo'lsa, dastur xato bermaydi.",
        """Tugma bosildi.
Tugma bosildi.
Callback muvaffaqiyatli ishga tushdi!"""
    ),
    (
        82,
        "Guard let da murakkab 'where' tekshiruvi",
        "Mijozning yoshi va balansini bitta guard operatorida xavfsiz ochib tekshiring.",
        """import Foundation

func grantCredit(userAge: Int?, balance: Double?) {
    guard let age = userAge, age >= 21,
          let bal = balance, bal > 1000.0 else {
        print("Kredit ajratish talablariga mos kelmadi.")
        return
    }
    
    print("Kredit ma'qullandi! Yosh: \\(age), Balans: $\\(bal)")
}

grantCredit(userAge: 25, balance: 1500.0)
grantCredit(userAge: 19, balance: 2000.0)
""",
        "'guard let' da bir nechta optionallar va ularga bog'liq mantiqiy tekshiruvlarni ketma-ket joylashtirish mumkin.",
        """Kredit ma'qullandi! Yosh: 25, Balans: $1500.0
Kredit ajratish talablariga mos kelmadi."""
    ),
    (
        83,
        "Xatoliklarni Optional ga aylantirish: 'try?'",
        "Xatolik (error) tashlashi mumkin bo'lgan funksiyani 'try?' orqali xavfsiz chaqiring.",
        """import Foundation

enum DiskError: Error {
    case fileNotFound
}

func readFileContent(filename: String) throws -> String {
    if filename == "data.txt" {
        return "Fayl matni muvaffaqiyatli o'qildi."
    }
    throw DiskError.fileNotFound
}

let contentSuccess = try? readFileContent(filename: "data.txt")
let contentFail = try? readFileContent(filename: "secret.txt")

print("Muvaffaqiyatli: \\(contentSuccess ?? "Xato")")
print("Muvaffaqiyatsiz: \\(contentFail ?? "Fayl topilmadi")")
""",
        "'try?' operatori throwing funksiyaning natijasini Optional ga o'giradi: agar xatolik yuz bersa nil, aks holda Optional(natija) qaytaradi.",
        """Muvaffaqiyatli: Fayl matni muvaffaqiyatli o'qildi.
Muvaffaqiyatsiz: Fayl topilmadi"""
    ),
    (
        84,
        "Struct larda Optional maydonlar va Memberwise Init",
        "Kompilyator avtomatik yaratadigan struct konstruktorida optional maydonlar qanday ishlashini ko'rsating.",
        """import Foundation

struct Product {
    let id: Int
    let title: String
    var description: String? = nil
}

let p1 = Product(id: 1, title: "iPhone 16")
let p2 = Product(id: 2, title: "AirPods Pro", description: "Shovqinni bekor qiluvchi quloqchin")

print("P1 izoh: \\(p1.description ?? "Tavsif yo'q")")
print("P2 izoh: \\(p2.description ?? "Tavsif yo'q")")
""",
        "Swift struct lari o'zlarining avtomatik initsializatorlarida default nil qiymatiga ega bo'lgan optional maydonlarni ixtiyoriy parametr sifatida qoldirishga imkon beradi.",
        """P1 izoh: Tavsif yo'q
P2 izoh: Shovqinni bekor qiluvchi quloqchin"""
    ),
    (
        85,
        "Ota-bola havolalarida Optionallik",
        "Daraxtsimon ma'lumot tuzilmasida ixtiyoriy ota yoki bola tugunlarini bog'lang.",
        """import Foundation

class TreeNode {
    var value: String
    var parent: TreeNode?
    var children: [TreeNode] = []
    
    init(value: String) {
        self.value = value
    }
}

let root = TreeNode(value: "Ildiz")
let child = TreeNode(value: "Shoxcha 1")
child.parent = root
root.children.append(child)

print("Bola tugun otasining nomi: \\(child.parent?.value ?? "Otasi yo'q")")
""",
        "Ierarxik tuzilmalarda ildiz elementining otasi bo'lmaydi (nil), shuning uchun ota tugunga havola albatta Optional bo'lishi shart.",
        """Bola tugun otasining nomi: Ildiz"""
    ),
    (
        86,
        "Optional va Equatable (Tenglikni tekshirish)",
        "Ikkita Optional o'zgaruvchining tengligini to'g'ridan-to'g'ri '==' orqali solishtiring.",
        """import Foundation

let a: Int? = 100
let b: Int? = 100
let c: Int? = nil
let d: Int? = nil

print("a == b: \\(a == b)")
print("a == c: \\(a == c)")
print("c == d: \\(c == d)")
""",
        "Swift-da agar Wrapped turi Equatable bo'lsa, 'Optional<Wrapped>' ham avtomatik ravishda Equatable hisoblanadi. Shuning uchun ikkita nil qiymat o'zaro teng hisoblanadi.",
        """a == b: true
a == c: false
c == d: true"""
    ),
    (
        87,
        "Optional va Comparable xususiyati",
        "Swift zamonaviy versiyalarida Optionallarni to'g'ridan-to'g'ri '<' yoki '>' bilan solishtirish nima sababdan cheklanganini ko'rsating.",
        """import Foundation

let scoreA: Int? = 45
let scoreB: Int? = 90

// Swift-da xavfsizlik uchun Optionallarni bevosita solishtirish cheklangan.
// Avval ikkalasini ochib keyin solishtirish eng to'g'ri usul:
if let sA = scoreA, let sB = scoreB {
    print("Katta ball: \\(max(sA, sB))")
}
""",
        "Swift ilk versiyalarida nil boshqa sonlardan kichik deb qaralardi, bu mantiqiy chalkashliklarga sabab bo'lganligi uchun zamonaviy Swift-da optionallarni solishtirishdan oldin ularni ochish talab etiladi.",
        """Katta ball: 90"""
    ),
    (
        88,
        "String interpolyatsiyasida 'Optional(...)' ogohlantirishini yo'qotish",
        "Konsolga chop etganda noqulay 'Optional(\"...\")' matnini tozalash usullarini ko'rsating.",
        """import Foundation

let userCity: String? = "Toshkent"

// Tavsiya etilmaydi:
// print("Shahar: \\(userCity)") // Xcode ogohlantirish beradi

// To'g'ri usullar:
print("Shahar (??): \\(userCity ?? "Noma'lum")")
print("Shahar (describing): \\(String(describing: userCity))")
""",
        "Kompilyator String interpolyatsiyasi ichida yalang'och Optional ko'rsa ogohlantirish beradi. Buni nil-coalescing yoki String(describing:) bilan hal qilish lozim.",
        """Shahar (??): Toshkent
Shahar (describing): Optional("Toshkent")"""
    ),
    (
        89,
        "Null Object Pattern vs Swift Optionals",
        "Boshqa tillardagi 'Null Object Pattern' o'rniga Swift Optionals qanchalik xavfsiz ekanligini solishtiring.",
        """import Foundation

struct UserNotification {
    let message: String
}

func sendNotification(notification: UserNotification?) {
    guard let note = notification else {
        print("Yuborish uchun xabar yo'q.")
        return
    }
    print("Xabar yuborildi: \\(note.message)")
}

sendNotification(notification: nil)
sendNotification(notification: UserNotification(message: "Yangi dars tayyor!"))
""",
        "Boshqa tillarda NullPointerException dan qochish uchun soxta 'EmptyUser' kabi ob'ektlar yaratiladi. Swift-da esa til darajasidagi Optionals bu muammoni to'liq hal qiladi.",
        """Yuborish uchun xabar yo'q.
Xabar yuborildi: Yangi dars tayyor!"""
    ),
    (
        90,
        "CustomDebugStringConvertible bilan Optionallarni loglash",
        "Obyekt debug qilinganda uning optional maydonlarini chiroyli formatda ko'rsatuvchi tuzilma yozing.",
        """import Foundation

struct DeviceConfig: CustomDebugStringConvertible {
    let ipAddress: String
    let proxyPort: Int?
    
    var debugDescription: String {
        return "DeviceConfig(IP: \\(ipAddress), Port: \\(proxyPort.map(String.init) ?? "Standart"))"
    }
}

let conf = DeviceConfig(ipAddress: "192.168.1.1", proxyPort: nil)
print(conf.debugDescription)
""",
        "CustomDebugStringConvertible protokoli orqali log yozishda optional qiymatlarni map va unwrap orqali professional formatda ko'rsatish mumkin.",
        """DeviceConfig(IP: 192.168.1.1, Port: Standart)"""
    ),
    (
        91,
        "Set to'plamida Optionallarni saqlash",
        "Set ichiga Hashable bo'lgan Optionallarni joylash imkoniyatini sinab ko'ring.",
        """import Foundation

var statusCodes: Set<Int?> = [200, 404, nil, 200, nil, 500]

print("Set elementlari soni: \\(statusCodes.count)")
for code in statusCodes {
    print("Element: \\(String(describing: code))")
}
""",
        "Agar T turi Hashable bo'lsa, 'T?' turi ham avtomatik Hashable hisoblanadi. Set ichida faqat bitta nil qiymat saqlanishi mumkin, dublikatlar tashlab yuboriladi.",
        """Set elementlari soni: 4
Element: Optional(200)
Element: Optional(404)
Element: nil
Element: Optional(500)"""
    ),
    (
        92,
        "Funksiya argumentida Optional ga default 'nil' qiymat berish",
        "Ixtiyoriy parametrlarga ega qulay funksiya dizaynini yarating.",
        """import Foundation

func fetchUserData(userID: Int, authToken: String? = nil) {
    if let token = authToken {
        print("Xavfsiz so'rov userID: \\(userID), Token: \\(token)")
    } else {
        print("Ommaviy so'rov userID: \\(userID)")
    }
}

fetchUserData(userID: 101)
fetchUserData(userID: 102, authToken: "BEARER_XYZ")
""",
        "Funksiya parametriga '= nil' berilishi uni chaqiruvchi uchun to'liq ixtiyoriy (optional) qiladi.",
        """Ommaviy so'rov userID: 101
Xavfsiz so'rov userID: 102, Token: BEARER_XYZ"""
    ),
    (
        93,
        "Failable Initializer (init?): Muvaffaqiyatsiz bo'ladigan initsializatsiya",
        "Noto'g'ri ma'lumot kiritilganda nil qaytaruvchi klass/struct yarating.",
        """import Foundation

struct PositiveNumber {
    let value: Int
    
    init?(value: Int) {
        if value <= 0 {
            return nil
        }
        self.value = value
    }
}

let validNum = PositiveNumber(value: 50)
let invalidNum = PositiveNumber(value: -10)

print("Musbat: \\(validNum != nil)")
print("Manfiy: \\(invalidNum != nil)")
""",
        "'init?' orqali e'lon qilingan konstruktor obyekt xossalari talabga javob bermasa initsializatsiyani bekor qilib 'nil' qaytarishi mumkin.",
        """Musbat: true
Manfiy: false"""
    ),
    (
        94,
        "URL initsializatsiyasi va xavfsiz ochish",
        "Veb-manzilni URL turiga xavfsiz o'giruvchi failable initsializator bilan ishlang.",
        """import Foundation

let validAddress = "https://khorazmiy.uz"
let brokenAddress = "bu yerda bo'sh joylar bor va xato manzil"

if let url = URL(string: validAddress) {
    print("Muvaffaqiyatli URL: \\(url.host ?? "")")
}

if let _ = URL(string: brokenAddress) {
    print("Ochildi")
} else {
    print("Noto'g'ri URL formati!")
}
""",
        "Foundation-dagi URL(string:) konstruktori failable (URL?) bo'lib, standart RFC qoidalariga to'g'ri kelmaydigan matn berilsa nil qaytaradi.",
        """Muvaffaqiyatli URL: khorazmiy.uz
Noto'g'ri URL formati!"""
    ),
    (
        95,
        "JSON dan ma'lumot o'qishda Optional xavfsizligi",
        "JSON lug'atidan ma'lumotlarni xavfsiz sug'urib oluvchi modul yozing.",
        """import Foundation

let jsonResponse: [String: Any] = [
    "status": "success",
    "code": 200,
    "user": [
        "name": "Jamshid",
        "age": 29
    ]
]

if let code = jsonResponse["code"] as? Int,
   let userDict = jsonResponse["user"] as? [String: Any],
   let name = userDict["name"] as? String {
    print("Muvaffaqiyatli: Code \\(code), Ism: \\(name)")
}
""",
        "Ixtiyoriy tipdagi JSON ob'ektlarini tahlil qilishda 'as?' va 'if let' larning birgalikda ishlatilishi har qanday nosozliklarni oldini oladi.",
        """Muvaffaqiyatli: Code 200, Ism: Jamshid"""
    ),
    (
        96,
        "Dinamik quyish va unwrap zanjiri",
        "Turli ob'ektlar qutisidan aniq tipni ajratib olib qayta ishlang.",
        """import Foundation

let registry: [String: Any?] = [
    "counter": 15,
    "label": "Boshqaruv paneli",
    "emptyField": nil
]

for (key, val) in registry {
    if let realValue = val, let text = realValue as? String {
        print("Matn kaliti '\\(key)': \\(text)")
    }
}
""",
        "Any? qutisidan avval nil emasligini tekshirish, so'ngra as? orqali mos turga keltirish ikki bosqichli xavfsizlikni ta'minlaydi.",
        """Matn kaliti 'label': Boshqaruv paneli"""
    ),
    (
        97,
        "Massivni xavfsiz indekslash: Safe Subscript Extension",
        "Indeks chegaradan chiqib ketganda dastur halokatga uchramasdan nil qaytaruvchi extension yozing.",
        """import Foundation

extension Array {
    subscript(safe index: Index) -> Element? {
        return indices.contains(index) ? self[index] : nil
    }
}

let frameworks = ["SwiftUI", "UIKit", "Combine"]

print("Indeks 1: \\(frameworks[safe: 1] ?? "Yo'q")")
print("Indeks 5: \\(frameworks[safe: 5] ?? "Chegaradan tashqarida")")
""",
        "Swift-da xavfsiz massiv subscripti yaratish iOS dasturlashdagi eng mashhur va foydali arxitekturaviy naqshlardan biridir.",
        """Indeks 1: UIKit
Indeks 5: Chegaradan tashqarida"""
    ),
    (
        98,
        "In-out parametrlari va Optional o'zgaruvchilar",
        "Funksiya ichida Optional o'zgaruvchining qiymatini xavfsiz o'zgartiruvchi 'inout' mexanizmini ko'rsating.",
        """import Foundation

func incrementIfExists(counter: inout Int?) {
    if let current = counter {
        counter = current + 1
    } else {
        counter = 1
    }
}

var visits: Int? = nil
incrementIfExists(counter: &visits)
print("1-tashrif: \\(visits ?? 0)")

incrementIfExists(counter: &visits)
print("2-tashrif: \\(visits ?? 0)")
""",
        "'inout' parametri orqali tashqi o'zgaruvchining manziliga to'g'ridan-to'g'ri murojaat qilinadi va uning ichidagi Optional holati o'zgartiriladi.",
        """1-tashrif: 1
2-tashrif: 2"""
    ),
    (
        99,
        "Async/Await va Optionals hamkorligi",
        "Asinxron funksiyadan ixtiyoriy natija qaytarish va uni xavfsiz kutib olish dasturi.",
        """import Foundation

func findUserByID(id: Int) async -> String? {
    if id == 77 {
        return "Sanjar Nazarov"
    }
    return nil
}

Task {
    let user = await findUserByID(id: 77)
    print("Topilgan foydalanuvchi: \\(user ?? "Topilmadi")")
}
""",
        "Swift Concurrency-da asinxron funksiyalar ham 'async -> T?' ko'rinishida Optional qaytarishi mumkin va 'await' dan so'ng oddiy optional kabi ishlatiladi.",
        """Topilgan foydalanuvchi: Sanjar Nazarov"""
    ),
    (
        100,
        "Amaliy loyiha: Foydalanuvchi registratsiya shakli validatori",
        "Foydalanuvchi kiritgan ixtiyoriy ma'lumotlarni to'liq xavfsiz tekshiruvchi yaxlit modul yarating.",
        """import Foundation

struct RegistrationForm {
    var email: String?
    var ageString: String?
    var phone: String?
}

struct ValidatedUser {
    let email: String
    let age: Int
    let phone: String
}

func validate(form: RegistrationForm) -> ValidatedUser? {
    guard let rawEmail = form.email, rawEmail.contains("@"), rawEmail.contains(".") else {
        print("Xatolik: Noto'g'ri elektron pochta.")
        return nil
    }
    
    guard let ageStr = form.ageString, let age = Int(ageStr), age >= 16 else {
        print("Xatolik: Yosh kiritilmadi yoki 16 dan kichik.")
        return nil
    }
    
    let phone = form.phone ?? "+998000000000"
    
    return ValidatedUser(email: rawEmail.lowercased(), age: age, phone: phone)
}

let form1 = RegistrationForm(email: "ALISHER@GMAIL.COM", ageString: "22", phone: nil)
if let user = validate(form: form1) {
    print("Muvaffaqiyatli ro'yxatdan o'tdi: \\(user.email), Yosh: \\(user.age), Tel: \\(user.phone)")
}

let badForm = RegistrationForm(email: "not-an-email", ageString: "14", phone: nil)
let result = validate(form: badForm)
print("Xato forma natijasi: \\(String(describing: result))")
""",
        "Ushbu yakuniy loyihada Optionals ning barcha muhim jihatlari: 'guard let', 'Int(str)' failable parsing, nil-coalescing ('??') va failable return yaxlit tizimda qo'llandi.",
        """Muvaffaqiyatli ro'yxatdan o'tdi: alisher@gmail.com, Yosh: 22, Tel: +998000000000
Xatolik: Noto'g'ri elektron pochta.
Xato forma natijasi: nil"""
    )
]

tasks = [format_task(*t) for t in tasks_data]
save_file("swift_02_optionals_va_unwrapping.md", tasks)
