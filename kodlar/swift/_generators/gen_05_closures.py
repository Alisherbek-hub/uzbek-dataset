# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

tasks_data = [
    (
        201,
        "Closures asoslari: Nomsiz funksiyalar sintaksisi",
        "Ikki sonni qo'shuvchi nomsiz closure e'lon qiling va uni o'zgaruvchi orqali chaqiring.",
        """import Foundation

let sumClosure: (Int, Int) -> Int = { (a: Int, b: Int) -> Int in
    return a + b
}

let result = sumClosure(15, 25)
print("Yig'indi: \\(result)")
""",
        "Swift-da Closure (kloujer) — bu o'zgaruvchiga yuklanishi yoki parametr sifatida uzatilishi mumkin bo'lgan mustaqil kod blokidir. 'in' kalit so'zi parametrlar va funksiya tanasini ajratib turadi.",
        """Yig'indi: 40"""
    ),
    (
        202,
        "Closure da tiplarni kontekstdan avtomatik aniqlash",
        "Qaytish turi va parametr turlarini ko'rsatmasdan ixcham closure yozing.",
        """import Foundation

let numbers = [5, 2, 8, 1, 9]

let sortedNumbers = numbers.sorted(by: { a, b in
    return a < b
})

print("Saralangan: \\(sortedNumbers)")
""",
        "Swift kontekstga qarab parametrlar va qaytish turini o'zi aniqlay oladi, shuning uchun closure ichida aniq tiplarni yozish shart emas.",
        """Saralangan: [1, 2, 5, 8, 9]"""
    ),
    (
        203,
        "Bitta ifodali closure larda yashirin qaytish (Implicit Returns)",
        "Bitta qatordan iborat closure da 'return' kalit so'zini tashlab keting.",
        """import Foundation

let words = ["olma", "anor", "shaftoli"]

let uppercaseWords = words.map { word in word.uppercased() }
print("Katta harflarda: \\(uppercaseWords)")
""",
        "Agar closure bitta ifodadan iborat bo'lsa, Swift 'return' so'zini talab qilmaydi va o'sha ifoda natijasini avtomatik qaytaradi.",
        """Katta harflarda: ["OLMA", "ANOR", "SHAFTOLI"]"""
    ),
    (
        204,
        "Qisqartirilgan argument nomlari: $0, $1",
        "Argumentlarga nom bermasdan $0, $1 indekslari orqali murojaat qiling.",
        """import Foundation

let values = [10, 3, 25, 7]

let descending = values.sorted { $0 > $1 }
let doubled = values.map { $0 * 2 }

print("Kamayish tartibida: \\(descending)")
print("Ikkilangan: \\(doubled)")
""",
        "Swift closure ga uzatilgan argumentlarga avtomatik ravishda $0 (birinchi), $1 (ikkinchi), $2 (uchinchi) va h.k. nomlarini beradi.",
        """Kamayish tartibida: [25, 10, 7, 3]
Ikkilangan: [20, 6, 50, 14]"""
    ),
    (
        205,
        "Operator metodlarini closure sifatida uzatish",
        "Taqqoslash operatorini to'g'ridan-to'g'ri saralash parametriga closure sifatida bering.",
        """import Foundation

let list = [40, 10, 80, 20]

// Swift-da '>' operatori aslida (Int, Int) -> Bool funksiyasidir
let sortedList = list.sorted(by: >)
print("Operator orqali saralangan: \\(sortedList)")
""",
        "Swift-da operatorlar aslida oddiy funksiyalar bo'lganligi sababli, mos keluvchi istalgan operatorni (masalan, '>', '<', '+') closure o'rnida to'g'ridan-to'g'ri uzatish mumkin.",
        """Operator orqali saralangan: [80, 40, 20, 10]"""
    ),
    (
        206,
        "Trailing Closure sintaksisi (Dumli closure)",
        "Funksiyaning oxirgi argumenti closure bo'lganda uni yumaloq qavsdan tashqariga chiqarib yozing.",
        """import Foundation

func repeatAction(times: Int, action: () -> Void) {
    for _ in 1...times {
        action()
    }
}

// Qavsdan tashqarida yozilgan trailing closure:
repeatAction(times: 2) {
    print("Salom dunyo!")
}
""",
        "Agar funksiyaning eng oxirgi parametri closure bo'lsa, chaqirish paytida qavsni yopib, closure kodini qavsdan tashqarida chiroyli blok shaklida yozish mumkin.",
        """Salom dunyo!
Salom dunyo!"""
    ),
    (
        207,
        "Bir nechta Trailing Closures (Multiple Trailing Closures - Swift 5.3+)",
        "Muvaffaqiyatli va muvaffaqiyatsiz holatlar uchun ikkita trailing closure dan foydalaning.",
        """import Foundation

func performTask(onSuccess: () -> Void, onFailure: (String) -> Void) {
    let isConnected = true
    if isConnected {
        onSuccess()
    } else {
        onFailure("Tarmoq xatosi")
    }
}

performTask {
    print("Vazifa muvaffaqiyatli bajarildi!")
} onFailure: { error in
    print("Xatolik ro'y berdi: \\(error)")
}
""",
        "Swift 5.3 dan boshlab bir nechta closure parametrlari qavsdan tashqarida ularning yorliqlarini ko'rsatgan holda chiroyli ketma-ket yozilishi mumkin.",
        """Vazifa muvaffaqiyatli bajarildi!"""
    ),
    (
        208,
        "Qiymatlarni qamrab olish (Capturing Values)",
        "Tashqi o'zgaruvchining holatini xotirasida saqlab qoluvchi akkumulyator closure hosil qiling.",
        """import Foundation

func makeAccumulator(initial: Int) -> () -> Int {
    var total = initial
    return {
        total += 10
        return total
    }
}

let counter = makeAccumulator(initial: 0)
print("1-qadam: \\(counter())")
print("2-qadam: \\(counter())")
print("3-qadam: \\(counter())")
""",
        "Closure o'zi e'lon qilingan kontekstdagi o'zgaruvchilarni 'capture' qiladi (ushlab qoladi). Funktsiya tugagandan keyin ham o'sha o'zgaruvchi xotirada yashashda davom etadi.",
        """1-qadam: 10
2-qadam: 20
3-qadam: 30"""
    ),
    (
        209,
        "Closures havola turi (Reference Type) ekanligi",
        "Ikki xil o'zgaruvchiga bitta closure berilganda ular aynan bir xil xotirani ulashishini isbotlang.",
        """import Foundation

func makeCounter() -> () -> Int {
    var count = 0
    return {
        count += 1
        return count
    }
}

let c1 = makeCounter()
let c2 = c1 // Havola nusxalandi

print("c1 orqali: \\(c1())")
print("c2 orqali: \\(c2())")
print("c1 orqali yana: \\(c1())")
""",
        "Funksiyalar va kloujerlar Swift-da Reference Type hisoblanadi. Ularni boshqa o'zgaruvchiga berish yangi nusxa yaratmaydi, balki bir xil havolani ulashadi.",
        """c1 orqali: 1
c2 orqali: 2
c1 orqali yana: 3"""
    ),
    (
        210,
        "Qochuvchi closure lar: @escaping",
        "Asinxron kechiktirib chaqiriladigan yoki tashqi o'zgaruvchida saqlanadigan closure ga @escaping atributini qo'ying.",
        """import Foundation

var completionHandlers: [() -> Void] = []

func registerHandler(handler: @escaping () -> Void) {
    print("Handler ro'yxatga olindi.")
    completionHandlers.append(handler)
}

registerHandler {
    print("Kechiktirilgan amaliyot bajarildi!")
}

print("Handlers soni: \\(completionHandlers.count)")
completionHandlers.first?()
""",
        "Agar closure funksiya tugaganidan keyin (masalan, asinxron javob kelganda yoki tashqi massivda saqlanganda) chaqirilsa, uning parametriga '@escaping' qo'yilishi shart.",
        """Handler ro'yxatga olindi.
Handlers soni: 1
Kechiktirilgan amaliyot bajarildi!"""
    ),
    (
        211,
        "Non-escaping closure larning standart xatti-harakati",
        "Funksiya tugashidan oldin bajarilib bo'ladigan oddiy closure xavfsizligini ko'rsating.",
        """import Foundation

func calculateSynchronously(action: () -> Void) {
    print("Boshlandi")
    action()
    print("Tugadi")
}

calculateSynchronously {
    print("Sinxron amal ijro etildi")
}
""",
        "Standart holda Swift-da barcha closure parametrlari 'non-escaping' hisoblanadi. Bu kompilyatorga xotirani vaqtinchalik stekda optimallashtirish imkonini beradi.",
        """Boshlandi
Sinxron amal ijro etildi
Tugadi"""
    ),
    (
        212,
        "Kechiktirilgan hisoblash: @autoclosure",
        "Ifodani avtomatik ravishda kloujerga o'rab, faqat kerak bo'lganda hisoblashni ta'minlang.",
        """import Foundation

func logIfTrue(condition: Bool, message: @autoclosure () -> String) {
    if condition {
        print("LOG: \\(message())")
    }
}

logIfTrue(condition: true, message: "Server muvaffaqiyatli ulandi")
logIfTrue(condition: false, message: "Bu satr hisoblanmaydi ham")
""",
        "'@autoclosure' parametrga uzatilgan ifodani avtomatik qavssiz kloujerga aylantiradi. Bu kodni ixchamlashtiradi va ifoda faqat haqiqatdan ham kerak bo'lgandagina hisoblanadi (lazy evaluation).",
        """LOG: Server muvaffaqiyatli ulandi"""
    ),
    (
        213,
        "@autoclosure va @escaping kombinatsiyasi",
        "Ham avtomatik qadoqlanadigan, ham keyinroq chaqiriladigan asinxron vazifani saqlang.",
        """import Foundation

var scheduledTasks: [() -> Void] = []

func scheduleTask(_ task: @autoclosure @escaping () -> Void) {
    scheduledTasks.append(task)
}

scheduleTask(print("Rejalashtirilgan vazifa ijro etildi!"))
scheduledTasks.first?()
""",
        "'@autoclosure @escaping' sintaksisi ifodani qavslarsiz parametr sifatida olib, uni kelajakda bajarish uchun saqlash imkonini beradi.",
        """Rejalashtirilgan vazifa ijro etildi!"""
    ),
    (
        214,
        "Closure Capture List: Qiymatni nusxalash ([x] in)",
        "Tashqi o'zgaruvchi keyin o'zgarsa ham, closure yaratilgan paytdagi qiymatni saqlab qolishni ko'rsating.",
        """import Foundation

var count = 10

let printCurrent = { [count] in
    print("Qamrab olingan qiymat: \\(count)")
}

count = 50
printCurrent()
print("Joriy o'zgaruvchi: \\(count)")
""",
        "Kloujer boshida '[count] in' deb yozilsa (capture list), count qiymati o'sha paytda immutably (o'zgarmas nusxa sifatida) ushlab qolinadi.",
        """Qamrab olingan qiymat: 10
Joriy o'zgaruvchi: 50"""
    ),
    (
        215,
        "Retain Cycle muammosi va [weak self]",
        "Sinf nusxasi va kloujer o'rtasida o'zaro bog'lanish (memory leak) paydo bo'lishining oldini oling.",
        """import Foundation

class NetworkManager {
    let name = "MainService"
    var onComplete: (() -> Void)?
    
    func setup() {
        onComplete = { [weak self] in
            guard let self = self else { return }
            print("Xizmat javob berdi: \\(self.name)")
        }
    }
    
    deinit {
        print("NetworkManager xotiradan tozalandi.")
    }
}

var manager: NetworkManager? = NetworkManager()
manager?.setup()
manager?.onComplete?()
manager = nil // Xotiradan to'g'ri o'chadi
""",
        "'[weak self]' ko'rsatkichi havola hisoblagichini (reference count) oshirmaydi va self ixtiyoriy payt xotiradan tozalanishiga to'sqinlik qilmaydi. Self nil bo'lishi mumkinligi sababli 'self?' ko'rinishida bo'ladi.",
        """Xizmat javob berdi: MainService
NetworkManager xotiradan tozalandi."""
    ),
    (
        216,
        "unowned self va uning xavfsizlik chegarasi",
        "Kloujer va obyektning umr davomiyligi mutlaqo bir xil bo'lgan vaziyatda unowned self ni qo'llang.",
        """import Foundation

class Customer {
    let name: String
    lazy var greet: () -> String = { [unowned self] in
        return "Salom, mening ismim \\(self.name)"
    }
    
    init(name: String) { self.name = name }
}

let customer = Customer(name: "Sherzod")
print(customer.greet())
""",
        "'[unowned self]' xuddi 'weak' kabi havolani kuchaytirmaydi, lekin u self ni Optional qilmaydi. Agar obyekt xotiradan o'chib ketgandan so'ng unowned ga murojaat qilinsa, crash bo'ladi.",
        """Salom, mening ismim Sherzod"""
    ),
    (
        217,
        "Kolleksiya transformatsiyasi: map",
        "Haroratlar massivini Selsiydan Farengeytga funktsional map orqali o'tkazing.",
        """import Foundation

let celsiusTemps = [0.0, 10.0, 25.0, 37.0, 100.0]
let fahrenheitTemps = celsiusTemps.map { $0 * 1.8 + 32 }

print("Farengeyt: \\(fahrenheitTemps)")
""",
        "'map' metodi har bir elementga berilgan funktsiyani qo'llab, yangi bir xil o'lchamdagi o'zgartirilgan massiv qaytaradi.",
        """Farengeyt: [32.0, 50.0, 77.0, 98.6, 212.0]"""
    ),
    (
        218,
        "Kolleksiyani saralash: filter",
        "Faqat 100 dollardan qimmat mahsulotlarni ajratib oling.",
        """import Foundation

let prices = [29.99, 149.00, 89.50, 499.99, 12.00]
let expensive = prices.filter { $0 > 100.0 }

print("Qimmat tovarlar: \\(expensive)")
""",
        "'filter' metodi berilgan predikat shartiga 'true' javob bergan elementlarni yangi massivga saralab oladi.",
        """Qimmat tovarlar: [149.0, 499.99]"""
    ),
    (
        219,
        "To'plamni bitta qiymatga keltirish: reduce",
        "Barcha sonlar ko'paytmasini bitta 'reduce' amali bilan hisoblang.",
        """import Foundation

let factors = [1, 2, 3, 4, 5]
let product = factors.reduce(1) { $0 * $1 }

print("1 dan 5 gacha ko'paytma: \\(product)")
""",
        "'reduce(initialResult, nextPartialResult)' boshlang'ich qiymatdan boshlab butun to'plam elementlarini ketma-ket yagona yakuniy qiymatga yig'adi.",
        """1 dan 5 gacha ko'paytma: 120"""
    ),
    (
        220,
        "Xotira tejovchi: reduce(into:)",
        "Massivdagi so'zlar takrorlanishini yangi lug'atga reduce(into:) orqali xotira nusxalamasdan yig'ing.",
        """import Foundation

let words = ["apple", "banana", "apple", "cherry", "banana", "apple"]

let counts = words.reduce(into: [:]) { countsDict, word in
    countsDict[word, default: 0] += 1
}

print("Statistika: \\(counts)")
""",
        "'reduce(into:)' oraliq nusxalarni yaratmasdan, bevosita inout akkumulyatorga o'zgartirish kiritadi, bu katta to'plamlar uchun ancha tezkor va tejamkordir.",
        """Statistika: ["banana": 2, "apple": 3, "cherry": 1]"""
    ),
    (
        221,
        "compactMap bilan ixtiyoriy nillarni filtrlash",
        "Kiritilgan matnlardan faqat haqiqiy sonlarni saralab oling.",
        """import Foundation

let mixedStrings = ["100", "iOS", "250", "Khorazmiy", "500"]
let numbers = mixedStrings.compactMap { Int($0) }

print("Valid sonlar: \\(numbers)")
""",
        "'compactMap' transformatsiya natijasida nil qaytgan barcha elementlarni avtomatik olib tashlab, toza unwrap bo'lgan massiv hosil qiladi.",
        """Valid sonlar: [100, 250, 500]"""
    ),
    (
        222,
        "flatMap bilan ichki massivlarni tekislash",
        "Har bir foydalanuvchining ko'nikmalari ro'yxatini yagona umumiy ro'yxatga tekislang.",
        """import Foundation

let skillsMatrix = [
    ["Swift", "SwiftUI"],
    ["Combine", "CoreData"],
    ["CoreML", "Metal"]
]

let allSkills = skillsMatrix.flatMap { $0 }
print("Barcha ko'nikmalar: \\(allSkills)")
""",
        "'flatMap' har bir element transformatsiyasidan hosil bo'lgan ketma-ketliklarni bitta tekis massivga birlashtiradi.",
        """Barcha ko'nikmalar: ["Swift", "SwiftUI", "Combine", "CoreData", "CoreML", "Metal"]"""
    ),
    (
        223,
        "Murakkab saralash: sorted(by:)",
        "Foydalanuvchilarni avval yoshi bo'yicha, yoshlari teng bo'lsa ismi bo'yicha tartiblang.",
        """import Foundation

struct User {
    let name: String
    let age: Int
}

let users = [
    User(name: "Zuhra", age: 25),
    User(name: "Ali", age: 22),
    User(name: "Bobur", age: 25)
]

let sortedUsers = users.sorted { u1, u2 in
    if u1.age == u2.age {
        return u1.name < u2.name
    }
    return u1.age < u2.age
}

for u in sortedUsers {
    print("\\(u.name): \\(u.age) yosh")
}
""",
        "'sorted(by:)' closure ga ikkita elementni solishtirish qoidasini berish orqali ixtiyoriy murakkab mezonlar bo'yicha saralash mumkin.",
        """Ali: 22 yosh
Bobur: 25 yosh
Zuhra: 25 yosh"""
    ),
    (
        224,
        "forEach metodi vs for-in tsikli",
        "forEach metodi kloujer qabul qilishi va unda 'break' yoki 'continue' ishlamasligini tushuntiring.",
        """import Foundation

let items = ["A", "B", "C"]

items.forEach { item in
    print("Element: \\(item)")
    // forEach ichida 'return' faqat joriy closure chaqiruvidan chiqadi, butun tsikldan emas!
}
""",
        "'forEach' funktsional uslubda to'plam bo'ylab aylanish uchun qulay, lekin undan 'break' yoki 'continue' yordamida chiqib bo'lmaydi.",
        """Element: A
Element: B
Element: C"""
    ),
    (
        225,
        "Barcha elementlar mosligini tekshirish: allSatisfy",
        "Barcha talabalarning bahosi ijobiy (>=60) ekanligini bitta funktsional chaqiruv bilan tasdiqlang.",
        """import Foundation

let scores = [75, 82, 90, 64, 88]
let allPassed = scores.allSatisfy { $0 >= 60 }

print("Barcha talabalar o'tdimi? \\(allPassed)")
""",
        "'allSatisfy' agar to'plamdagi har bir element berilgan shartga to'g'ri kelsa true, aks holda darhol false qaytaradi.",
        """Barcha talabalar o'tdimi? true"""
    ),
    (
        226,
        "Shartga mos birinchi element: first(where:)",
        "Matnlar ro'yxatidan 'K' harfi bilan boshlanuvchi eng birinchi so'zni toping.",
        """import Foundation

let techCompanies = ["Apple", "Google", "Khorazmiy AI", "Microsoft"]
let found = techCompanies.first { $0.hasPrefix("K") }

print("Topildi: \\(found ?? "Yo'q")")
""",
        "'first(where:)' berilgan mezon bo'yicha to'plamdan birinchi uchragan elementni topishi bilan skanerlashni to'xtatadi va uni Optional ko'rinishda qaytaradi.",
        """Topildi: Khorazmiy AI"""
    ),
    (
        227,
        "Shartga mos indeksni topish: firstIndex(where:)",
        "Massivda manfiy son qaysi indeksda joylashganini aniqlang.",
        """import Foundation

let series = [14, 25, 0, -8, 42]
if let idx = series.firstIndex(where: { $0 < 0 }) {
    print("Manfiy son indeksi: \\(idx)")
}
""",
        "'firstIndex(where:)' shartni qanoatlantiruvchi elementning indeksini topadi.",
        """Manfiy son indeksi: 3"""
    ),
    (
        228,
        "In-place shartli o'chirish: removeAll(where:)",
        "Massivning o'zidan barcha toq sonlarni o'chirib tashlang.",
        """import Foundation

var list = [1, 2, 3, 4, 5, 6, 7, 8]
list.removeAll { $0 % 2 != 0 }

print("Faqat juft sonlar qoldi: \\(list)")
""",
        "'removeAll(where:)' yangi massiv yaratmasdan, asl to'plamning o'zida shartga mos elementlarni O(N) tezlikda tozalaydi.",
        """Faqat juft sonlar qoldi: [2, 4, 6, 8]"""
    ),
    (
        229,
        "To'plamni ikkiga ajratish: partition(by:)",
        "Massivni musbat va manfiy qismlarga joyida (in-place) bo'ling.",
        """import Foundation

var numbers = [-5, 10, -2, 8, 3, -9]
let pivotIndex = numbers.partition { $0 > 0 }

print("Ajratish nuqtasi indeksi: \\(pivotIndex)")
print("Partitsiyalangan massiv: \\(numbers)")
""",
        "'partition(by:)' massiv elementlarini shartga mos kelmaydiganlarni oldinga, mos keladiganlarni orqaga surib, ikkala qism chegarasining indeksini qaytaradi.",
        """Ajratish nuqtasi indeksi: 3
Partitsiyalangan massiv: [-5, -9, -2, 8, 3, 10]"""
    ),
    (
        230,
        "min(by:) va max(by:) funktsional qidiruv",
        "So'zlar ichidan eng uzunini max(by:) orqali toping.",
        """import Foundation

let words = ["Swift", "Dasturlash", "AI", "Apple"]
let longest = words.max { $0.count < $1.count }

print("Eng uzun so'z: \\(longest ?? "")")
""",
        "'max(by:)' va 'min(by:)' ikkita elementni taqqoslash kloujeriga tayanib eng ekstremal qiymatni topadi.",
        """Eng uzun so'z: Dasturlash"""
    ),
    (
        231,
        "Funktsional zanjir (Method Chaining: filter, map, reduce)",
        "Juft sonlarni tanlab, ularni kvadratga oshirib, yakuniy yig'indisini hisoblang.",
        """import Foundation

let rawData = [1, 2, 3, 4, 5, 6]

let sumOfSquares = rawData
    .filter { $0 % 2 == 0 } // [2, 4, 6]
    .map { $0 * $0 }        // [4, 16, 36]
    .reduce(0, +)           // 56

print("Juft sonlar kvadratlari yig'indisi: \\(sumOfSquares)")
""",
        "Funktsional metodlarni bir-biriga zanjir qilish kodni deklarativ, toza va xatosiz o'qiladigan shaklga keltiradi.",
        """Juft sonlar kvadratlari yig'indisi: 56"""
    ),
    (
        232,
        "Kechiktirilgan konfiguratsiya closure lari",
        "UI komponentini o'rnatish paytida bitta blokda sozlab oluvchi naqsh yozing.",
        """import Foundation

class Label {
    var text = ""
    var fontSize = 14
}

func configureLabel(config: (Label) -> Void) -> Label {
    let lbl = Label()
    config(lbl)
    return lbl
}

let header = configureLabel { lbl in
    lbl.text = "Asosiy Sahifa"
    lbl.fontSize = 24
}

print("Yaratilgan Label: '\\(header.text)', o'lchami: \\(header.fontSize)pt")
""",
        "Kloujer orqali konfiguratsiya berish (Builder closure) Swift va SwiftUI da juda keng qo'llaniladi.",
        """Yaratilgan Label: 'Asosiy Sahifa', o'lchami: 24pt"""
    ),
    (
        233,
        "Hodisalarni boshqarish: Event Callback Closure",
        "Tugma bosilishini tinglovchi (listener) tizimni kloujer bilan hosil qiling.",
        """import Foundation

class ClickableButton {
    private var actionHandler: (() -> Void)?
    
    func onClick(perform: @escaping () -> Void) {
        self.actionHandler = perform
    }
    
    func userTapped() {
        print("Foydalanuvchi tugmani bosdi...")
        actionHandler?()
    }
}

let btn = ClickableButton()
btn.onClick {
    print("Hodisa ushlandi: Yangi sahifa ochilmoqda!")
}
btn.userTapped()
""",
        "Kloujerlar iOS arxitekturasida delegatlar o'rniga engil va qulay callback mexanizmi sifatida xizmat qiladi.",
        """Foydalanuvchi tugmani bosdi...
Hodisa ushlandi: Yangi sahifa ochilmoqda!"""
    ),
    (
        234,
        "Asinxron Completion Handler arxitekturasi",
        "Tarmoq so'rovi yakunlanganda natijani qaytaruvchi klassik iOS asinxron completion handler yozing.",
        """import Foundation

func fetchRemoteStatus(completion: @escaping (String) -> Void) {
    DispatchQueue.global().async {
        // Asinxron yuklanish
        let status = "STATUS_200_OK"
        completion(status)
    }
}

fetchRemoteStatus { result in
    print("Javob keldi: \\(result)")
}
""",
        "Swift Concurrency gacha bo'lgan davrda asinxron funksiyalar completion handler closure lari orqali natijani qaytargan.",
        """Javob keldi: STATUS_200_OK"""
    ),
    (
        235,
        "Result tipi bilan xavfsiz Completion Handler",
        "Muvaffaqiyat yoki xatolikni Result<Success, Failure> orqali qaytaruvchi callback yozing.",
        """import Foundation

enum APIError: Error {
    case badURL
}

func loadContent(from url: String, completion: @escaping (Result<String, APIError>) -> Void) {
    if url.isEmpty {
        completion(.failure(.badURL))
    } else {
        completion(.success("Server kontenti olindi"))
    }
}

loadContent(from: "https://khorazmiy.uz") { result in
    switch result {
    case .success(let data):
        print("Muvaffaqiyat: \\(data)")
    case .failure(let error):
        print("Xato: \\(error)")
    }
}
""",
        "Result<T, Error> tipi completion handler larda xatolik va natijani bitta o'zgaruvchida aniq ifodalash imkonini beradi.",
        """Muvaffaqiyat: Server kontenti olindi"""
    ),
    (
        236,
        "Swift Concurrency va @Sendable Closures",
        "Oqimlar orasida xavfsiz uzatilishi kafolatlangan @Sendable closure ni ko'rsating.",
        """import Foundation

func runConcurrentTask(action: @Sendable @escaping () -> Void) {
    Task {
        action()
    }
}

runConcurrentTask {
    print("Parallel oqimda xavfsiz bajarildi!")
}
""",
        "'@Sendable' atributi kloujerning o'zgaruvchan holatlarni (mutable state) data-race xatolarisiz xavfsiz uzata olishini Swift 6 kompilyatori darajasida tekshiradi.",
        """Parallel oqimda xavfsiz bajarildi!"""
    ),
    (
        237,
        "O'z-o'zini chaqiruvchi closure bilan initsializatsiya (Immediately Invoked Closure)",
        "Murakkab ob'ekt xususiyatini o'zgaruvchi e'lon qilingan joydayoq sozlang.",
        """import Foundation

let complexConfig: [String: String] = {
    var dict = [String: String]()
    dict["host"] = "127.0.0.1"
    dict["port"] = "5432"
    dict["db"] = "khorazmiy_core"
    return dict
}()

print("DB porti: \\(complexConfig["port"] ?? "")")
""",
        "'{ ... }()' sintaksisi closure ni e'lon qilib shu zahotiyoq ishga tushiradi va uning natijasini o'zgaruvchiga biriktiradi. Bu iOS da UI elementlarini sozlashda eng ko'p ishlatiladigan naqshdir.",
        """DB porti: 5432"""
    ),
    (
        238,
        "KeyPath bilan closure o'rnini bosish (\.property)",
        "Kloujer '{ $0.name }' o'rniga KeyPath '\\.name' dan foydalaning.",
        """import Foundation

struct Song {
    let title: String
    let durationSeconds: Int
}

let playlist = [
    Song(title: "O'zbegim", durationSeconds: 240),
    Song(title: "Lazgi", durationSeconds: 180)
]

let titles = playlist.map(\\.title)
print("Qo'shiqlar ro'yxati: \\(titles)")
""",
        "Swift-da '\\.propertyName' KeyPath ifodasini '(Root) -> Value' funksiyasi yoki kloujeri kutilyotgan istalgan joyda to'g'ridan-to'g'ri ishlatish mumkin.",
        """Qo'shiqlar ro'yxati: ["O'zbegim", "Lazgi"]"""
    ),
    (
        239,
        "KeyPath bilan tartiblash",
        "Obyektlar to'plamini muayyan maydon bo'yicha KeyPath yordamida saralang.",
        """import Foundation

struct Car {
    let model: String
    let topSpeed: Int
}

let cars = [
    Car(model: "Malibu", topSpeed: 220),
    Car(model: "Tracker", topSpeed: 190),
    Car(model: "Tahoe", topSpeed: 210)
]

let fastestCars = cars.sorted { $0.topSpeed > $1.topSpeed }
for c in fastestCars {
    print("\\(c.model): \\(c.topSpeed) km/soat")
}
""",
        "KeyPath xususiyatlaridan foydalanish kodni ancha ixcham va xavfsiz qiladi.",
        """Malibu: 220 km/soat
Tahoe: 210 km/soat
Tracker: 190 km/soat"""
    ),
    (
        240,
        "Predicate kombinatorlari (AND, OR, NOT combinators)",
        "Bir nechta tekshiruv shartlarini birlashtiruvchi funktsional kombinator tuzing.",
        """import Foundation

typealias Predicate<T> = (T) -> Bool

func and<T>(_ p1: @escaping Predicate<T>, _ p2: @escaping Predicate<T>) -> Predicate<T> {
    return { item in p1(item) && p2(item) }
}

let isPositive: Predicate<Int> = { $0 > 0 }
let isEven: Predicate<Int> = { $0 % 2 == 0 }

let isPositiveAndEven = and(isPositive, isEven)

print("4 mosmi? \\(isPositiveAndEven(4))")
print("-2 mosmi? \\(isPositiveAndEven(-2))")
print("3 mosmi? \\(isPositiveAndEven(3))")
""",
        "Funktsional dasturlashda predikatlarni birlashtiruvchi yuqori tartibli funksiyalar yordamida ixtiyoriy murakkab filtrlarni hosil qilish mumkin.",
        """4 mosmi? true
-2 mosmi? false
3 mosmi? false"""
    ),
    (
        241,
        "Funktsional Dependency Injection kloujer orqali",
        "Sinfga murakkab protokol o'rniga oddiy closure funksiya kiritib testlashni osonlashtiring.",
        """import Foundation

class TimePrinter {
    let timeProvider: () -> String
    
    init(timeProvider: @escaping () -> String) {
        self.timeProvider = timeProvider
    }
    
    func printCurrentTime() {
        print("Vaqt: \\(timeProvider())")
    }
}

// Haqiqiy yoki test vaqtini kiritish:
let mockPrinter = TimePrinter { "12:00 Mock Time" }
mockPrinter.printCurrentTime()
""",
        "Protokollarsiz, oddiy kloujer orqali bog'liqliklarni uzatish (Functional DI) arxitekturani nihoyatda yengil va testlashga oson qiladi.",
        """Vaqt: 12:00 Mock Time"""
    ),
    (
        242,
        "Around / Transaction Pattern: Xavfsiz oraliq bajarilishi",
        "Ma'lumotlar bazasi tranzaksiyasini avtomatik commit yoki rollback qiluvchi wrapper closure.",
        """import Foundation

func withDatabaseTransaction(operation: () throws -> Void) {
    print("TRANSACTION_BEGIN")
    do {
        try operation()
        print("TRANSACTION_COMMIT")
    } catch {
        print("TRANSACTION_ROLLBACK: \\(error)")
    }
}

withDatabaseTransaction {
    print("Foydalanuvchi hisobi yangilandi.")
}
""",
        "Ushbu naqsh harakatdan oldin va keyin bajarilishi shart bo'lgan mantiqni markazlashtiradi.",
        """TRANSACTION_BEGIN
Foydalanuvchi hisobi yangilandi.
TRANSACTION_COMMIT"""
    ),
    (
        243,
        "Kloujer bilan massiv elementlarini guruhlash (Dictionary(grouping:by:))",
        "So'zlarni ularning bosh harfi bo'yicha lug'atga guruhlang.",
        """import Foundation

let words = ["olma", "anor", "behi", "banan", "shaftoli"]

let grouped = Dictionary(grouping: words, by: { $0.first ?? " " })

for (char, group) in grouped.sorted(by: { $0.key < $1.key }) {
    print("'\\(char)': \\(group)")
}
""",
        "'Dictionary(grouping:by:)' to'plamni kloujerdan qaytgan kalit bo'yicha avtomatik guruhlaydi.",
        """'a': ["olma", "anor"]
'b': ["behi", "banan"]
's': ["shaftoli"]"""
    ),
    (
        244,
        "Debounce g'oyasi: Tez-tez chaqiruvlarni cheklovchi kloujer",
        "Qidiruv maydonida har bir harf bosilganda emas, so'nggi harakatdan keyin ishga tushuvchi mexanizm modeli.",
        """import Foundation

func simulateSearch(queries: [String], onSearch: (String) -> Void) {
    var lastQuery = ""
    for q in queries {
        lastQuery = q
    }
    // Faqat oxirgisini yuboramiz
    onSearch(lastQuery)
}

simulateSearch(queries: ["S", "Sw", "Swi", "Swift"]) { finalQuery in
    print("Qidiruv yuborildi: \\(finalQuery)")
}
""",
        "Mobil ilovalarda kloujerlar orqali foydalanuvchi kiritishini tejamkor boshqarish mumkin.",
        """Qidiruv yuborildi: Swift"""
    ),
    (
        245,
        "Rekursiv anonim kloujer yaratish",
        "O'z-o'zini chaqiruvchi closure ni o'zgaruvchi orqali tashkil etish.",
        """import Foundation

var fibonacci: ((Int) -> Int)!

fibonacci = { n in
    return n <= 1 ? n : fibonacci(n - 1) + fibonacci(n - 2)
}

print("Fibonacci(6) = \\(fibonacci(6))")
""",
        "Kloujer o'zgaruvchisi oldindan e'lon qilinishi sharti bilan kloujer tanasi ichida o'zini chaqirishi mumkin.",
        """Fibonacci(6) = 8"""
    ),
    (
        246,
        "Xatoliklarni transformatsiya qiluvchi closure: Result.mapError",
        "Xatolik turini boshqa umumiy domen xatoligiga o'zgartiring.",
        """import Foundation

enum NetworkError: Error { case timeout }
enum AppError: Error { case connectionFailed }

let failureResult: Result<String, NetworkError> = .failure(.timeout)

let mappedResult = failureResult.mapError { _ in AppError.connectionFailed }

switch mappedResult {
case .success(let val): print(val)
case .failure(let err): print("Transformatsiya qilingan xato: \\(err)")
}
""",
        "'mapError' Result ichidagi muvaffaqiyat qiymatiga tegmasdan, faqat xatolikni o'zgartiradi.",
        """Transformatsiya qilingan xato: connectionFailed"""
    ),
    (
        247,
        "Kloujerlar bilan konveyer (Pipeline) funktsional operatori",
        "Matematik ifodalarni 'x |> f |> g' uslubida bajaruvchi maxsus quvur (pipe) operatori.",
        """import Foundation

infix operator |> : AdditionPrecedence

func |> <T, U>(value: T, function: (T) -> U) -> U {
    return function(value)
}

let result = 10
    |> { $0 + 5 }
    |> { $0 * 2 }
    |> { "Natija: \\($0)" }

print(result)
""",
        "Funktsional dasturlash tillaridagi quvur (|>) operatori kodni chapdan o'ngga ravon o'qilishini ta'minlaydi.",
        """Natija: 30"""
    ),
    (
        248,
        "Kloujer yordamida xotirani kuzatish va loglash",
        "Funksiya necha marta chaqirilganini sanovchi profiling kloujeri.",
        """import Foundation

func createProfiledAction<T, R>(_ action: @escaping (T) -> R) -> ((T) -> R, () -> Int) {
    var callCount = 0
    let profiled: (T) -> R = { input in
        callCount += 1
        return action(input)
    }
    let getCount: () -> Int = { callCount }
    return (profiled, getCount)
}

let (calc, getCalls) = createProfiledAction { (x: Int) in x * 10 }
_ = calc(2)
_ = calc(5)
print("Funksiya jami \\(getCalls()) marta chaqirildi.")
""",
        "Kloujerlar orqali holatni qamrab olish (closure state capture) profiling va audit tizimlarida juda samarali.",
        """Funksiya jami 2 marta chaqirildi."""
    ),
    (
        249,
        "Shartli ravishda bajariluvchi Lazy Closure qutisi",
        "Qimmat hisoblanadigan qiymatni faqat bir marta hisoblab keshlovchi tuzilma.",
        """import Foundation

class LazyValue<T> {
    private let initializer: () -> T
    private var cached: T?
    
    init(_ initializer: @escaping () -> T) {
        self.initializer = initializer
    }
    
    var value: T {
        if let val = cached { return val }
        let newVal = initializer()
        cached = newVal
        return newVal
    }
}

let heavyCalculation = LazyValue {
    print("Qimmat hisob-kitob bajarildi!")
    return 42 * 100
}

print("Hali qiymat chaqirilmadi.")
print("Qiymat: \\(heavyCalculation.value)")
print("Ikkinchi chaqiruv: \\(heavyCalculation.value)")
""",
        "Kloujer orqali amalga oshirilgan kechiktirilgan hisoblash xotira va protsessor unumdorligini oshiradi.",
        """Hali qiymat chaqirilmadi.
Qimmat hisob-kitob bajarildi!
Qiymat: 4200
Ikkinchi chaqiruv: 4200"""
    ),
    (
        250,
        "Amaliy loyiha: Funktsional reaktiv buyurtmalar tahlili va saralash tizimi",
        "Katta onlayn do'kon buyurtmalarini funktsional zanjir (filter, map, sorted, reduce) orqali to'liq qayta ishlovchi modul.",
        """import Foundation

struct OrderItem {
    let name: String
    let price: Double
    let quantity: Int
}

struct Order {
    let id: Int
    let customer: String
    let items: [OrderItem]
    let isDelivered: Bool
}

let orders = [
    Order(id: 1, customer: "Aziz", items: [
        OrderItem(name: "iPhone", price: 999.0, quantity: 1),
        OrderItem(name: "G'ilof", price: 29.0, quantity: 2)
    ], isDelivered: true),
    Order(id: 2, customer: "Nilufar", items: [
        OrderItem(name: "iPad", price: 599.0, quantity: 1)
    ], isDelivered: false),
    Order(id: 3, customer: "Botir", items: [
        OrderItem(name: "AirPods", price: 199.0, quantity: 2),
        OrderItem(name: "Kabel", price: 19.0, quantity: 1)
    ], isDelivered: true)
]

// Faqat yetkazilgan buyurtmalarning umumiy daromadini hisoblash:
let deliveredRevenue = orders
    .filter(\\.isDelivered)
    .flatMap(\\.items)
    .map { $0.price * Double($0.quantity) }
    .reduce(0.0, +)

print("Yetkazilgan buyurtmalardan tushgan sof daromad: $\\(deliveredRevenue)")

// Har bir xaridor bo'yicha buyurtma summasini saralash:
let customerSummaries = orders.map { order -> (customer: String, total: Double) in
    let total = order.items.reduce(0.0) { $0 + ($1.price * Double($1.quantity)) }
    return (order.customer, total)
}.sorted { $0.total > $1.total }

for s in customerSummaries {
    print("Mijoz: \\(s.customer) - Jami: $\\(s.total)")
}
""",
        "Ushbu yakuniy amaliy loyihada Swift-ning barcha asosiy funktsional imkoniyatlari: 'filter', 'flatMap', 'map', 'reduce', KeyPath (\\.isDelivered) va kortejlar yordamida real biznes tahlili amalga oshirildi.",
        """Yetkazilgan buyurtmalardan tushgan sof daromad: $1474.0
Mijoz: Aziz - Jami: $1057.0
Mijoz: Nilufar - Jami: $599.0
Mijoz: Botir - Jami: $417.0"""
    )
]

tasks = [format_task(*t) for t in tasks_data]
save_file("swift_05_closures_va_funksional_usullar.md", tasks)
