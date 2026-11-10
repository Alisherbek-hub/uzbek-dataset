# 201-Topshiriq: Closures asoslari: Nomsiz funksiyalar sintaksisi
## Topshiriq sharti:
Ikki sonni qo'shuvchi nomsiz closure e'lon qiling va uni o'zgaruvchi orqali chaqiring.

## Yechim (Swift kodi):
```swift
import Foundation

let sumClosure: (Int, Int) -> Int = { (a: Int, b: Int) -> Int in
    return a + b
}

let result = sumClosure(15, 25)
print("Yig'indi: \(result)")
```

## Tushuntirish va Mantiq:
Swift-da Closure (kloujer) — bu o'zgaruvchiga yuklanishi yoki parametr sifatida uzatilishi mumkin bo'lgan mustaqil kod blokidir. 'in' kalit so'zi parametrlar va funksiya tanasini ajratib turadi.

## Ishlash natijasi:
```text
Yig'indi: 40
```


# 202-Topshiriq: Closure da tiplarni kontekstdan avtomatik aniqlash
## Topshiriq sharti:
Qaytish turi va parametr turlarini ko'rsatmasdan ixcham closure yozing.

## Yechim (Swift kodi):
```swift
import Foundation

let numbers = [5, 2, 8, 1, 9]

let sortedNumbers = numbers.sorted(by: { a, b in
    return a < b
})

print("Saralangan: \(sortedNumbers)")
```

## Tushuntirish va Mantiq:
Swift kontekstga qarab parametrlar va qaytish turini o'zi aniqlay oladi, shuning uchun closure ichida aniq tiplarni yozish shart emas.

## Ishlash natijasi:
```text
Saralangan: [1, 2, 5, 8, 9]
```


# 203-Topshiriq: Bitta ifodali closure larda yashirin qaytish (Implicit Returns)
## Topshiriq sharti:
Bitta qatordan iborat closure da 'return' kalit so'zini tashlab keting.

## Yechim (Swift kodi):
```swift
import Foundation

let words = ["olma", "anor", "shaftoli"]

let uppercaseWords = words.map { word in word.uppercased() }
print("Katta harflarda: \(uppercaseWords)")
```

## Tushuntirish va Mantiq:
Agar closure bitta ifodadan iborat bo'lsa, Swift 'return' so'zini talab qilmaydi va o'sha ifoda natijasini avtomatik qaytaradi.

## Ishlash natijasi:
```text
Katta harflarda: ["OLMA", "ANOR", "SHAFTOLI"]
```


# 204-Topshiriq: Qisqartirilgan argument nomlari: $0, $1
## Topshiriq sharti:
Argumentlarga nom bermasdan $0, $1 indekslari orqali murojaat qiling.

## Yechim (Swift kodi):
```swift
import Foundation

let values = [10, 3, 25, 7]

let descending = values.sorted { $0 > $1 }
let doubled = values.map { $0 * 2 }

print("Kamayish tartibida: \(descending)")
print("Ikkilangan: \(doubled)")
```

## Tushuntirish va Mantiq:
Swift closure ga uzatilgan argumentlarga avtomatik ravishda $0 (birinchi), $1 (ikkinchi), $2 (uchinchi) va h.k. nomlarini beradi.

## Ishlash natijasi:
```text
Kamayish tartibida: [25, 10, 7, 3]
Ikkilangan: [20, 6, 50, 14]
```


# 205-Topshiriq: Operator metodlarini closure sifatida uzatish
## Topshiriq sharti:
Taqqoslash operatorini to'g'ridan-to'g'ri saralash parametriga closure sifatida bering.

## Yechim (Swift kodi):
```swift
import Foundation

let list = [40, 10, 80, 20]

// Swift-da '>' operatori aslida (Int, Int) -> Bool funksiyasidir
let sortedList = list.sorted(by: >)
print("Operator orqali saralangan: \(sortedList)")
```

## Tushuntirish va Mantiq:
Swift-da operatorlar aslida oddiy funksiyalar bo'lganligi sababli, mos keluvchi istalgan operatorni (masalan, '>', '<', '+') closure o'rnida to'g'ridan-to'g'ri uzatish mumkin.

## Ishlash natijasi:
```text
Operator orqali saralangan: [80, 40, 20, 10]
```


# 206-Topshiriq: Trailing Closure sintaksisi (Dumli closure)
## Topshiriq sharti:
Funksiyaning oxirgi argumenti closure bo'lganda uni yumaloq qavsdan tashqariga chiqarib yozing.

## Yechim (Swift kodi):
```swift
import Foundation

func repeatAction(times: Int, action: () -> Void) {
    for _ in 1...times {
        action()
    }
}

// Qavsdan tashqarida yozilgan trailing closure:
repeatAction(times: 2) {
    print("Salom dunyo!")
}
```

## Tushuntirish va Mantiq:
Agar funksiyaning eng oxirgi parametri closure bo'lsa, chaqirish paytida qavsni yopib, closure kodini qavsdan tashqarida chiroyli blok shaklida yozish mumkin.

## Ishlash natijasi:
```text
Salom dunyo!
Salom dunyo!
```


# 207-Topshiriq: Bir nechta Trailing Closures (Multiple Trailing Closures - Swift 5.3+)
## Topshiriq sharti:
Muvaffaqiyatli va muvaffaqiyatsiz holatlar uchun ikkita trailing closure dan foydalaning.

## Yechim (Swift kodi):
```swift
import Foundation

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
    print("Xatolik ro'y berdi: \(error)")
}
```

## Tushuntirish va Mantiq:
Swift 5.3 dan boshlab bir nechta closure parametrlari qavsdan tashqarida ularning yorliqlarini ko'rsatgan holda chiroyli ketma-ket yozilishi mumkin.

## Ishlash natijasi:
```text
Vazifa muvaffaqiyatli bajarildi!
```


# 208-Topshiriq: Qiymatlarni qamrab olish (Capturing Values)
## Topshiriq sharti:
Tashqi o'zgaruvchining holatini xotirasida saqlab qoluvchi akkumulyator closure hosil qiling.

## Yechim (Swift kodi):
```swift
import Foundation

func makeAccumulator(initial: Int) -> () -> Int {
    var total = initial
    return {
        total += 10
        return total
    }
}

let counter = makeAccumulator(initial: 0)
print("1-qadam: \(counter())")
print("2-qadam: \(counter())")
print("3-qadam: \(counter())")
```

## Tushuntirish va Mantiq:
Closure o'zi e'lon qilingan kontekstdagi o'zgaruvchilarni 'capture' qiladi (ushlab qoladi). Funktsiya tugagandan keyin ham o'sha o'zgaruvchi xotirada yashashda davom etadi.

## Ishlash natijasi:
```text
1-qadam: 10
2-qadam: 20
3-qadam: 30
```


# 209-Topshiriq: Closures havola turi (Reference Type) ekanligi
## Topshiriq sharti:
Ikki xil o'zgaruvchiga bitta closure berilganda ular aynan bir xil xotirani ulashishini isbotlang.

## Yechim (Swift kodi):
```swift
import Foundation

func makeCounter() -> () -> Int {
    var count = 0
    return {
        count += 1
        return count
    }
}

let c1 = makeCounter()
let c2 = c1 // Havola nusxalandi

print("c1 orqali: \(c1())")
print("c2 orqali: \(c2())")
print("c1 orqali yana: \(c1())")
```

## Tushuntirish va Mantiq:
Funksiyalar va kloujerlar Swift-da Reference Type hisoblanadi. Ularni boshqa o'zgaruvchiga berish yangi nusxa yaratmaydi, balki bir xil havolani ulashadi.

## Ishlash natijasi:
```text
c1 orqali: 1
c2 orqali: 2
c1 orqali yana: 3
```


# 210-Topshiriq: Qochuvchi closure lar: @escaping
## Topshiriq sharti:
Asinxron kechiktirib chaqiriladigan yoki tashqi o'zgaruvchida saqlanadigan closure ga @escaping atributini qo'ying.

## Yechim (Swift kodi):
```swift
import Foundation

var completionHandlers: [() -> Void] = []

func registerHandler(handler: @escaping () -> Void) {
    print("Handler ro'yxatga olindi.")
    completionHandlers.append(handler)
}

registerHandler {
    print("Kechiktirilgan amaliyot bajarildi!")
}

print("Handlers soni: \(completionHandlers.count)")
completionHandlers.first?()
```

## Tushuntirish va Mantiq:
Agar closure funksiya tugaganidan keyin (masalan, asinxron javob kelganda yoki tashqi massivda saqlanganda) chaqirilsa, uning parametriga '@escaping' qo'yilishi shart.

## Ishlash natijasi:
```text
Handler ro'yxatga olindi.
Handlers soni: 1
Kechiktirilgan amaliyot bajarildi!
```


# 211-Topshiriq: Non-escaping closure larning standart xatti-harakati
## Topshiriq sharti:
Funksiya tugashidan oldin bajarilib bo'ladigan oddiy closure xavfsizligini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

func calculateSynchronously(action: () -> Void) {
    print("Boshlandi")
    action()
    print("Tugadi")
}

calculateSynchronously {
    print("Sinxron amal ijro etildi")
}
```

## Tushuntirish va Mantiq:
Standart holda Swift-da barcha closure parametrlari 'non-escaping' hisoblanadi. Bu kompilyatorga xotirani vaqtinchalik stekda optimallashtirish imkonini beradi.

## Ishlash natijasi:
```text
Boshlandi
Sinxron amal ijro etildi
Tugadi
```


# 212-Topshiriq: Kechiktirilgan hisoblash: @autoclosure
## Topshiriq sharti:
Ifodani avtomatik ravishda kloujerga o'rab, faqat kerak bo'lganda hisoblashni ta'minlang.

## Yechim (Swift kodi):
```swift
import Foundation

func logIfTrue(condition: Bool, message: @autoclosure () -> String) {
    if condition {
        print("LOG: \(message())")
    }
}

logIfTrue(condition: true, message: "Server muvaffaqiyatli ulandi")
logIfTrue(condition: false, message: "Bu satr hisoblanmaydi ham")
```

## Tushuntirish va Mantiq:
'@autoclosure' parametrga uzatilgan ifodani avtomatik qavssiz kloujerga aylantiradi. Bu kodni ixchamlashtiradi va ifoda faqat haqiqatdan ham kerak bo'lgandagina hisoblanadi (lazy evaluation).

## Ishlash natijasi:
```text
LOG: Server muvaffaqiyatli ulandi
```


# 213-Topshiriq: @autoclosure va @escaping kombinatsiyasi
## Topshiriq sharti:
Ham avtomatik qadoqlanadigan, ham keyinroq chaqiriladigan asinxron vazifani saqlang.

## Yechim (Swift kodi):
```swift
import Foundation

var scheduledTasks: [() -> Void] = []

func scheduleTask(_ task: @autoclosure @escaping () -> Void) {
    scheduledTasks.append(task)
}

scheduleTask(print("Rejalashtirilgan vazifa ijro etildi!"))
scheduledTasks.first?()
```

## Tushuntirish va Mantiq:
'@autoclosure @escaping' sintaksisi ifodani qavslarsiz parametr sifatida olib, uni kelajakda bajarish uchun saqlash imkonini beradi.

## Ishlash natijasi:
```text
Rejalashtirilgan vazifa ijro etildi!
```


# 214-Topshiriq: Closure Capture List: Qiymatni nusxalash ([x] in)
## Topshiriq sharti:
Tashqi o'zgaruvchi keyin o'zgarsa ham, closure yaratilgan paytdagi qiymatni saqlab qolishni ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

var count = 10

let printCurrent = { [count] in
    print("Qamrab olingan qiymat: \(count)")
}

count = 50
printCurrent()
print("Joriy o'zgaruvchi: \(count)")
```

## Tushuntirish va Mantiq:
Kloujer boshida '[count] in' deb yozilsa (capture list), count qiymati o'sha paytda immutably (o'zgarmas nusxa sifatida) ushlab qolinadi.

## Ishlash natijasi:
```text
Qamrab olingan qiymat: 10
Joriy o'zgaruvchi: 50
```


# 215-Topshiriq: Retain Cycle muammosi va [weak self]
## Topshiriq sharti:
Sinf nusxasi va kloujer o'rtasida o'zaro bog'lanish (memory leak) paydo bo'lishining oldini oling.

## Yechim (Swift kodi):
```swift
import Foundation

class NetworkManager {
    let name = "MainService"
    var onComplete: (() -> Void)?
    
    func setup() {
        onComplete = { [weak self] in
            guard let self = self else { return }
            print("Xizmat javob berdi: \(self.name)")
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
```

## Tushuntirish va Mantiq:
'[weak self]' ko'rsatkichi havola hisoblagichini (reference count) oshirmaydi va self ixtiyoriy payt xotiradan tozalanishiga to'sqinlik qilmaydi. Self nil bo'lishi mumkinligi sababli 'self?' ko'rinishida bo'ladi.

## Ishlash natijasi:
```text
Xizmat javob berdi: MainService
NetworkManager xotiradan tozalandi.
```


# 216-Topshiriq: unowned self va uning xavfsizlik chegarasi
## Topshiriq sharti:
Kloujer va obyektning umr davomiyligi mutlaqo bir xil bo'lgan vaziyatda unowned self ni qo'llang.

## Yechim (Swift kodi):
```swift
import Foundation

class Customer {
    let name: String
    lazy var greet: () -> String = { [unowned self] in
        return "Salom, mening ismim \(self.name)"
    }
    
    init(name: String) { self.name = name }
}

let customer = Customer(name: "Sherzod")
print(customer.greet())
```

## Tushuntirish va Mantiq:
'[unowned self]' xuddi 'weak' kabi havolani kuchaytirmaydi, lekin u self ni Optional qilmaydi. Agar obyekt xotiradan o'chib ketgandan so'ng unowned ga murojaat qilinsa, crash bo'ladi.

## Ishlash natijasi:
```text
Salom, mening ismim Sherzod
```


# 217-Topshiriq: Kolleksiya transformatsiyasi: map
## Topshiriq sharti:
Haroratlar massivini Selsiydan Farengeytga funktsional map orqali o'tkazing.

## Yechim (Swift kodi):
```swift
import Foundation

let celsiusTemps = [0.0, 10.0, 25.0, 37.0, 100.0]
let fahrenheitTemps = celsiusTemps.map { $0 * 1.8 + 32 }

print("Farengeyt: \(fahrenheitTemps)")
```

## Tushuntirish va Mantiq:
'map' metodi har bir elementga berilgan funktsiyani qo'llab, yangi bir xil o'lchamdagi o'zgartirilgan massiv qaytaradi.

## Ishlash natijasi:
```text
Farengeyt: [32.0, 50.0, 77.0, 98.6, 212.0]
```


# 218-Topshiriq: Kolleksiyani saralash: filter
## Topshiriq sharti:
Faqat 100 dollardan qimmat mahsulotlarni ajratib oling.

## Yechim (Swift kodi):
```swift
import Foundation

let prices = [29.99, 149.00, 89.50, 499.99, 12.00]
let expensive = prices.filter { $0 > 100.0 }

print("Qimmat tovarlar: \(expensive)")
```

## Tushuntirish va Mantiq:
'filter' metodi berilgan predikat shartiga 'true' javob bergan elementlarni yangi massivga saralab oladi.

## Ishlash natijasi:
```text
Qimmat tovarlar: [149.0, 499.99]
```


# 219-Topshiriq: To'plamni bitta qiymatga keltirish: reduce
## Topshiriq sharti:
Barcha sonlar ko'paytmasini bitta 'reduce' amali bilan hisoblang.

## Yechim (Swift kodi):
```swift
import Foundation

let factors = [1, 2, 3, 4, 5]
let product = factors.reduce(1) { $0 * $1 }

print("1 dan 5 gacha ko'paytma: \(product)")
```

## Tushuntirish va Mantiq:
'reduce(initialResult, nextPartialResult)' boshlang'ich qiymatdan boshlab butun to'plam elementlarini ketma-ket yagona yakuniy qiymatga yig'adi.

## Ishlash natijasi:
```text
1 dan 5 gacha ko'paytma: 120
```


# 220-Topshiriq: Xotira tejovchi: reduce(into:)
## Topshiriq sharti:
Massivdagi so'zlar takrorlanishini yangi lug'atga reduce(into:) orqali xotira nusxalamasdan yig'ing.

## Yechim (Swift kodi):
```swift
import Foundation

let words = ["apple", "banana", "apple", "cherry", "banana", "apple"]

let counts = words.reduce(into: [:]) { countsDict, word in
    countsDict[word, default: 0] += 1
}

print("Statistika: \(counts)")
```

## Tushuntirish va Mantiq:
'reduce(into:)' oraliq nusxalarni yaratmasdan, bevosita inout akkumulyatorga o'zgartirish kiritadi, bu katta to'plamlar uchun ancha tezkor va tejamkordir.

## Ishlash natijasi:
```text
Statistika: ["banana": 2, "apple": 3, "cherry": 1]
```


# 221-Topshiriq: compactMap bilan ixtiyoriy nillarni filtrlash
## Topshiriq sharti:
Kiritilgan matnlardan faqat haqiqiy sonlarni saralab oling.

## Yechim (Swift kodi):
```swift
import Foundation

let mixedStrings = ["100", "iOS", "250", "Khorazmiy", "500"]
let numbers = mixedStrings.compactMap { Int($0) }

print("Valid sonlar: \(numbers)")
```

## Tushuntirish va Mantiq:
'compactMap' transformatsiya natijasida nil qaytgan barcha elementlarni avtomatik olib tashlab, toza unwrap bo'lgan massiv hosil qiladi.

## Ishlash natijasi:
```text
Valid sonlar: [100, 250, 500]
```


# 222-Topshiriq: flatMap bilan ichki massivlarni tekislash
## Topshiriq sharti:
Har bir foydalanuvchining ko'nikmalari ro'yxatini yagona umumiy ro'yxatga tekislang.

## Yechim (Swift kodi):
```swift
import Foundation

let skillsMatrix = [
    ["Swift", "SwiftUI"],
    ["Combine", "CoreData"],
    ["CoreML", "Metal"]
]

let allSkills = skillsMatrix.flatMap { $0 }
print("Barcha ko'nikmalar: \(allSkills)")
```

## Tushuntirish va Mantiq:
'flatMap' har bir element transformatsiyasidan hosil bo'lgan ketma-ketliklarni bitta tekis massivga birlashtiradi.

## Ishlash natijasi:
```text
Barcha ko'nikmalar: ["Swift", "SwiftUI", "Combine", "CoreData", "CoreML", "Metal"]
```


# 223-Topshiriq: Murakkab saralash: sorted(by:)
## Topshiriq sharti:
Foydalanuvchilarni avval yoshi bo'yicha, yoshlari teng bo'lsa ismi bo'yicha tartiblang.

## Yechim (Swift kodi):
```swift
import Foundation

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
    print("\(u.name): \(u.age) yosh")
}
```

## Tushuntirish va Mantiq:
'sorted(by:)' closure ga ikkita elementni solishtirish qoidasini berish orqali ixtiyoriy murakkab mezonlar bo'yicha saralash mumkin.

## Ishlash natijasi:
```text
Ali: 22 yosh
Bobur: 25 yosh
Zuhra: 25 yosh
```


# 224-Topshiriq: forEach metodi vs for-in tsikli
## Topshiriq sharti:
forEach metodi kloujer qabul qilishi va unda 'break' yoki 'continue' ishlamasligini tushuntiring.

## Yechim (Swift kodi):
```swift
import Foundation

let items = ["A", "B", "C"]

items.forEach { item in
    print("Element: \(item)")
    // forEach ichida 'return' faqat joriy closure chaqiruvidan chiqadi, butun tsikldan emas!
}
```

## Tushuntirish va Mantiq:
'forEach' funktsional uslubda to'plam bo'ylab aylanish uchun qulay, lekin undan 'break' yoki 'continue' yordamida chiqib bo'lmaydi.

## Ishlash natijasi:
```text
Element: A
Element: B
Element: C
```


# 225-Topshiriq: Barcha elementlar mosligini tekshirish: allSatisfy
## Topshiriq sharti:
Barcha talabalarning bahosi ijobiy (>=60) ekanligini bitta funktsional chaqiruv bilan tasdiqlang.

## Yechim (Swift kodi):
```swift
import Foundation

let scores = [75, 82, 90, 64, 88]
let allPassed = scores.allSatisfy { $0 >= 60 }

print("Barcha talabalar o'tdimi? \(allPassed)")
```

## Tushuntirish va Mantiq:
'allSatisfy' agar to'plamdagi har bir element berilgan shartga to'g'ri kelsa true, aks holda darhol false qaytaradi.

## Ishlash natijasi:
```text
Barcha talabalar o'tdimi? true
```


# 226-Topshiriq: Shartga mos birinchi element: first(where:)
## Topshiriq sharti:
Matnlar ro'yxatidan 'K' harfi bilan boshlanuvchi eng birinchi so'zni toping.

## Yechim (Swift kodi):
```swift
import Foundation

let techCompanies = ["Apple", "Google", "Khorazmiy AI", "Microsoft"]
let found = techCompanies.first { $0.hasPrefix("K") }

print("Topildi: \(found ?? "Yo'q")")
```

## Tushuntirish va Mantiq:
'first(where:)' berilgan mezon bo'yicha to'plamdan birinchi uchragan elementni topishi bilan skanerlashni to'xtatadi va uni Optional ko'rinishda qaytaradi.

## Ishlash natijasi:
```text
Topildi: Khorazmiy AI
```


# 227-Topshiriq: Shartga mos indeksni topish: firstIndex(where:)
## Topshiriq sharti:
Massivda manfiy son qaysi indeksda joylashganini aniqlang.

## Yechim (Swift kodi):
```swift
import Foundation

let series = [14, 25, 0, -8, 42]
if let idx = series.firstIndex(where: { $0 < 0 }) {
    print("Manfiy son indeksi: \(idx)")
}
```

## Tushuntirish va Mantiq:
'firstIndex(where:)' shartni qanoatlantiruvchi elementning indeksini topadi.

## Ishlash natijasi:
```text
Manfiy son indeksi: 3
```


# 228-Topshiriq: In-place shartli o'chirish: removeAll(where:)
## Topshiriq sharti:
Massivning o'zidan barcha toq sonlarni o'chirib tashlang.

## Yechim (Swift kodi):
```swift
import Foundation

var list = [1, 2, 3, 4, 5, 6, 7, 8]
list.removeAll { $0 % 2 != 0 }

print("Faqat juft sonlar qoldi: \(list)")
```

## Tushuntirish va Mantiq:
'removeAll(where:)' yangi massiv yaratmasdan, asl to'plamning o'zida shartga mos elementlarni O(N) tezlikda tozalaydi.

## Ishlash natijasi:
```text
Faqat juft sonlar qoldi: [2, 4, 6, 8]
```


# 229-Topshiriq: To'plamni ikkiga ajratish: partition(by:)
## Topshiriq sharti:
Massivni musbat va manfiy qismlarga joyida (in-place) bo'ling.

## Yechim (Swift kodi):
```swift
import Foundation

var numbers = [-5, 10, -2, 8, 3, -9]
let pivotIndex = numbers.partition { $0 > 0 }

print("Ajratish nuqtasi indeksi: \(pivotIndex)")
print("Partitsiyalangan massiv: \(numbers)")
```

## Tushuntirish va Mantiq:
'partition(by:)' massiv elementlarini shartga mos kelmaydiganlarni oldinga, mos keladiganlarni orqaga surib, ikkala qism chegarasining indeksini qaytaradi.

## Ishlash natijasi:
```text
Ajratish nuqtasi indeksi: 3
Partitsiyalangan massiv: [-5, -9, -2, 8, 3, 10]
```


# 230-Topshiriq: min(by:) va max(by:) funktsional qidiruv
## Topshiriq sharti:
So'zlar ichidan eng uzunini max(by:) orqali toping.

## Yechim (Swift kodi):
```swift
import Foundation

let words = ["Swift", "Dasturlash", "AI", "Apple"]
let longest = words.max { $0.count < $1.count }

print("Eng uzun so'z: \(longest ?? "")")
```

## Tushuntirish va Mantiq:
'max(by:)' va 'min(by:)' ikkita elementni taqqoslash kloujeriga tayanib eng ekstremal qiymatni topadi.

## Ishlash natijasi:
```text
Eng uzun so'z: Dasturlash
```


# 231-Topshiriq: Funktsional zanjir (Method Chaining: filter, map, reduce)
## Topshiriq sharti:
Juft sonlarni tanlab, ularni kvadratga oshirib, yakuniy yig'indisini hisoblang.

## Yechim (Swift kodi):
```swift
import Foundation

let rawData = [1, 2, 3, 4, 5, 6]

let sumOfSquares = rawData
    .filter { $0 % 2 == 0 } // [2, 4, 6]
    .map { $0 * $0 }        // [4, 16, 36]
    .reduce(0, +)           // 56

print("Juft sonlar kvadratlari yig'indisi: \(sumOfSquares)")
```

## Tushuntirish va Mantiq:
Funktsional metodlarni bir-biriga zanjir qilish kodni deklarativ, toza va xatosiz o'qiladigan shaklga keltiradi.

## Ishlash natijasi:
```text
Juft sonlar kvadratlari yig'indisi: 56
```


# 232-Topshiriq: Kechiktirilgan konfiguratsiya closure lari
## Topshiriq sharti:
UI komponentini o'rnatish paytida bitta blokda sozlab oluvchi naqsh yozing.

## Yechim (Swift kodi):
```swift
import Foundation

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

print("Yaratilgan Label: '\(header.text)', o'lchami: \(header.fontSize)pt")
```

## Tushuntirish va Mantiq:
Kloujer orqali konfiguratsiya berish (Builder closure) Swift va SwiftUI da juda keng qo'llaniladi.

## Ishlash natijasi:
```text
Yaratilgan Label: 'Asosiy Sahifa', o'lchami: 24pt
```


# 233-Topshiriq: Hodisalarni boshqarish: Event Callback Closure
## Topshiriq sharti:
Tugma bosilishini tinglovchi (listener) tizimni kloujer bilan hosil qiling.

## Yechim (Swift kodi):
```swift
import Foundation

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
```

## Tushuntirish va Mantiq:
Kloujerlar iOS arxitekturasida delegatlar o'rniga engil va qulay callback mexanizmi sifatida xizmat qiladi.

## Ishlash natijasi:
```text
Foydalanuvchi tugmani bosdi...
Hodisa ushlandi: Yangi sahifa ochilmoqda!
```


# 234-Topshiriq: Asinxron Completion Handler arxitekturasi
## Topshiriq sharti:
Tarmoq so'rovi yakunlanganda natijani qaytaruvchi klassik iOS asinxron completion handler yozing.

## Yechim (Swift kodi):
```swift
import Foundation

func fetchRemoteStatus(completion: @escaping (String) -> Void) {
    DispatchQueue.global().async {
        // Asinxron yuklanish
        let status = "STATUS_200_OK"
        completion(status)
    }
}

fetchRemoteStatus { result in
    print("Javob keldi: \(result)")
}
```

## Tushuntirish va Mantiq:
Swift Concurrency gacha bo'lgan davrda asinxron funksiyalar completion handler closure lari orqali natijani qaytargan.

## Ishlash natijasi:
```text
Javob keldi: STATUS_200_OK
```


# 235-Topshiriq: Result tipi bilan xavfsiz Completion Handler
## Topshiriq sharti:
Muvaffaqiyat yoki xatolikni Result<Success, Failure> orqali qaytaruvchi callback yozing.

## Yechim (Swift kodi):
```swift
import Foundation

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
        print("Muvaffaqiyat: \(data)")
    case .failure(let error):
        print("Xato: \(error)")
    }
}
```

## Tushuntirish va Mantiq:
Result<T, Error> tipi completion handler larda xatolik va natijani bitta o'zgaruvchida aniq ifodalash imkonini beradi.

## Ishlash natijasi:
```text
Muvaffaqiyat: Server kontenti olindi
```


# 236-Topshiriq: Swift Concurrency va @Sendable Closures
## Topshiriq sharti:
Oqimlar orasida xavfsiz uzatilishi kafolatlangan @Sendable closure ni ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

func runConcurrentTask(action: @Sendable @escaping () -> Void) {
    Task {
        action()
    }
}

runConcurrentTask {
    print("Parallel oqimda xavfsiz bajarildi!")
}
```

## Tushuntirish va Mantiq:
'@Sendable' atributi kloujerning o'zgaruvchan holatlarni (mutable state) data-race xatolarisiz xavfsiz uzata olishini Swift 6 kompilyatori darajasida tekshiradi.

## Ishlash natijasi:
```text
Parallel oqimda xavfsiz bajarildi!
```


# 237-Topshiriq: O'z-o'zini chaqiruvchi closure bilan initsializatsiya (Immediately Invoked Closure)
## Topshiriq sharti:
Murakkab ob'ekt xususiyatini o'zgaruvchi e'lon qilingan joydayoq sozlang.

## Yechim (Swift kodi):
```swift
import Foundation

let complexConfig: [String: String] = {
    var dict = [String: String]()
    dict["host"] = "127.0.0.1"
    dict["port"] = "5432"
    dict["db"] = "khorazmiy_core"
    return dict
}()

print("DB porti: \(complexConfig["port"] ?? "")")
```

## Tushuntirish va Mantiq:
'{ ... }()' sintaksisi closure ni e'lon qilib shu zahotiyoq ishga tushiradi va uning natijasini o'zgaruvchiga biriktiradi. Bu iOS da UI elementlarini sozlashda eng ko'p ishlatiladigan naqshdir.

## Ishlash natijasi:
```text
DB porti: 5432
```


# 238-Topshiriq: KeyPath bilan closure o'rnini bosish (\.property)
## Topshiriq sharti:
Kloujer '{ $0.name }' o'rniga KeyPath '\.name' dan foydalaning.

## Yechim (Swift kodi):
```swift
import Foundation

struct Song {
    let title: String
    let durationSeconds: Int
}

let playlist = [
    Song(title: "O'zbegim", durationSeconds: 240),
    Song(title: "Lazgi", durationSeconds: 180)
]

let titles = playlist.map(\.title)
print("Qo'shiqlar ro'yxati: \(titles)")
```

## Tushuntirish va Mantiq:
Swift-da '\.propertyName' KeyPath ifodasini '(Root) -> Value' funksiyasi yoki kloujeri kutilyotgan istalgan joyda to'g'ridan-to'g'ri ishlatish mumkin.

## Ishlash natijasi:
```text
Qo'shiqlar ro'yxati: ["O'zbegim", "Lazgi"]
```


# 239-Topshiriq: KeyPath bilan tartiblash
## Topshiriq sharti:
Obyektlar to'plamini muayyan maydon bo'yicha KeyPath yordamida saralang.

## Yechim (Swift kodi):
```swift
import Foundation

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
    print("\(c.model): \(c.topSpeed) km/soat")
}
```

## Tushuntirish va Mantiq:
KeyPath xususiyatlaridan foydalanish kodni ancha ixcham va xavfsiz qiladi.

## Ishlash natijasi:
```text
Malibu: 220 km/soat
Tahoe: 210 km/soat
Tracker: 190 km/soat
```


# 240-Topshiriq: Predicate kombinatorlari (AND, OR, NOT combinators)
## Topshiriq sharti:
Bir nechta tekshiruv shartlarini birlashtiruvchi funktsional kombinator tuzing.

## Yechim (Swift kodi):
```swift
import Foundation

typealias Predicate<T> = (T) -> Bool

func and<T>(_ p1: @escaping Predicate<T>, _ p2: @escaping Predicate<T>) -> Predicate<T> {
    return { item in p1(item) && p2(item) }
}

let isPositive: Predicate<Int> = { $0 > 0 }
let isEven: Predicate<Int> = { $0 % 2 == 0 }

let isPositiveAndEven = and(isPositive, isEven)

print("4 mosmi? \(isPositiveAndEven(4))")
print("-2 mosmi? \(isPositiveAndEven(-2))")
print("3 mosmi? \(isPositiveAndEven(3))")
```

## Tushuntirish va Mantiq:
Funktsional dasturlashda predikatlarni birlashtiruvchi yuqori tartibli funksiyalar yordamida ixtiyoriy murakkab filtrlarni hosil qilish mumkin.

## Ishlash natijasi:
```text
4 mosmi? true
-2 mosmi? false
3 mosmi? false
```


# 241-Topshiriq: Funktsional Dependency Injection kloujer orqali
## Topshiriq sharti:
Sinfga murakkab protokol o'rniga oddiy closure funksiya kiritib testlashni osonlashtiring.

## Yechim (Swift kodi):
```swift
import Foundation

class TimePrinter {
    let timeProvider: () -> String
    
    init(timeProvider: @escaping () -> String) {
        self.timeProvider = timeProvider
    }
    
    func printCurrentTime() {
        print("Vaqt: \(timeProvider())")
    }
}

// Haqiqiy yoki test vaqtini kiritish:
let mockPrinter = TimePrinter { "12:00 Mock Time" }
mockPrinter.printCurrentTime()
```

## Tushuntirish va Mantiq:
Protokollarsiz, oddiy kloujer orqali bog'liqliklarni uzatish (Functional DI) arxitekturani nihoyatda yengil va testlashga oson qiladi.

## Ishlash natijasi:
```text
Vaqt: 12:00 Mock Time
```


# 242-Topshiriq: Around / Transaction Pattern: Xavfsiz oraliq bajarilishi
## Topshiriq sharti:
Ma'lumotlar bazasi tranzaksiyasini avtomatik commit yoki rollback qiluvchi wrapper closure.

## Yechim (Swift kodi):
```swift
import Foundation

func withDatabaseTransaction(operation: () throws -> Void) {
    print("TRANSACTION_BEGIN")
    do {
        try operation()
        print("TRANSACTION_COMMIT")
    } catch {
        print("TRANSACTION_ROLLBACK: \(error)")
    }
}

withDatabaseTransaction {
    print("Foydalanuvchi hisobi yangilandi.")
}
```

## Tushuntirish va Mantiq:
Ushbu naqsh harakatdan oldin va keyin bajarilishi shart bo'lgan mantiqni markazlashtiradi.

## Ishlash natijasi:
```text
TRANSACTION_BEGIN
Foydalanuvchi hisobi yangilandi.
TRANSACTION_COMMIT
```


# 243-Topshiriq: Kloujer bilan massiv elementlarini guruhlash (Dictionary(grouping:by:))
## Topshiriq sharti:
So'zlarni ularning bosh harfi bo'yicha lug'atga guruhlang.

## Yechim (Swift kodi):
```swift
import Foundation

let words = ["olma", "anor", "behi", "banan", "shaftoli"]

let grouped = Dictionary(grouping: words, by: { $0.first ?? " " })

for (char, group) in grouped.sorted(by: { $0.key < $1.key }) {
    print("'\(char)': \(group)")
}
```

## Tushuntirish va Mantiq:
'Dictionary(grouping:by:)' to'plamni kloujerdan qaytgan kalit bo'yicha avtomatik guruhlaydi.

## Ishlash natijasi:
```text
'a': ["olma", "anor"]
'b': ["behi", "banan"]
's': ["shaftoli"]
```


# 244-Topshiriq: Debounce g'oyasi: Tez-tez chaqiruvlarni cheklovchi kloujer
## Topshiriq sharti:
Qidiruv maydonida har bir harf bosilganda emas, so'nggi harakatdan keyin ishga tushuvchi mexanizm modeli.

## Yechim (Swift kodi):
```swift
import Foundation

func simulateSearch(queries: [String], onSearch: (String) -> Void) {
    var lastQuery = ""
    for q in queries {
        lastQuery = q
    }
    // Faqat oxirgisini yuboramiz
    onSearch(lastQuery)
}

simulateSearch(queries: ["S", "Sw", "Swi", "Swift"]) { finalQuery in
    print("Qidiruv yuborildi: \(finalQuery)")
}
```

## Tushuntirish va Mantiq:
Mobil ilovalarda kloujerlar orqali foydalanuvchi kiritishini tejamkor boshqarish mumkin.

## Ishlash natijasi:
```text
Qidiruv yuborildi: Swift
```


# 245-Topshiriq: Rekursiv anonim kloujer yaratish
## Topshiriq sharti:
O'z-o'zini chaqiruvchi closure ni o'zgaruvchi orqali tashkil etish.

## Yechim (Swift kodi):
```swift
import Foundation

var fibonacci: ((Int) -> Int)!

fibonacci = { n in
    return n <= 1 ? n : fibonacci(n - 1) + fibonacci(n - 2)
}

print("Fibonacci(6) = \(fibonacci(6))")
```

## Tushuntirish va Mantiq:
Kloujer o'zgaruvchisi oldindan e'lon qilinishi sharti bilan kloujer tanasi ichida o'zini chaqirishi mumkin.

## Ishlash natijasi:
```text
Fibonacci(6) = 8
```


# 246-Topshiriq: Xatoliklarni transformatsiya qiluvchi closure: Result.mapError
## Topshiriq sharti:
Xatolik turini boshqa umumiy domen xatoligiga o'zgartiring.

## Yechim (Swift kodi):
```swift
import Foundation

enum NetworkError: Error { case timeout }
enum AppError: Error { case connectionFailed }

let failureResult: Result<String, NetworkError> = .failure(.timeout)

let mappedResult = failureResult.mapError { _ in AppError.connectionFailed }

switch mappedResult {
case .success(let val): print(val)
case .failure(let err): print("Transformatsiya qilingan xato: \(err)")
}
```

## Tushuntirish va Mantiq:
'mapError' Result ichidagi muvaffaqiyat qiymatiga tegmasdan, faqat xatolikni o'zgartiradi.

## Ishlash natijasi:
```text
Transformatsiya qilingan xato: connectionFailed
```


# 247-Topshiriq: Kloujerlar bilan konveyer (Pipeline) funktsional operatori
## Topshiriq sharti:
Matematik ifodalarni 'x |> f |> g' uslubida bajaruvchi maxsus quvur (pipe) operatori.

## Yechim (Swift kodi):
```swift
import Foundation

infix operator |> : AdditionPrecedence

func |> <T, U>(value: T, function: (T) -> U) -> U {
    return function(value)
}

let result = 10
    |> { $0 + 5 }
    |> { $0 * 2 }
    |> { "Natija: \($0)" }

print(result)
```

## Tushuntirish va Mantiq:
Funktsional dasturlash tillaridagi quvur (|>) operatori kodni chapdan o'ngga ravon o'qilishini ta'minlaydi.

## Ishlash natijasi:
```text
Natija: 30
```


# 248-Topshiriq: Kloujer yordamida xotirani kuzatish va loglash
## Topshiriq sharti:
Funksiya necha marta chaqirilganini sanovchi profiling kloujeri.

## Yechim (Swift kodi):
```swift
import Foundation

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
print("Funksiya jami \(getCalls()) marta chaqirildi.")
```

## Tushuntirish va Mantiq:
Kloujerlar orqali holatni qamrab olish (closure state capture) profiling va audit tizimlarida juda samarali.

## Ishlash natijasi:
```text
Funksiya jami 2 marta chaqirildi.
```


# 249-Topshiriq: Shartli ravishda bajariluvchi Lazy Closure qutisi
## Topshiriq sharti:
Qimmat hisoblanadigan qiymatni faqat bir marta hisoblab keshlovchi tuzilma.

## Yechim (Swift kodi):
```swift
import Foundation

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
print("Qiymat: \(heavyCalculation.value)")
print("Ikkinchi chaqiruv: \(heavyCalculation.value)")
```

## Tushuntirish va Mantiq:
Kloujer orqali amalga oshirilgan kechiktirilgan hisoblash xotira va protsessor unumdorligini oshiradi.

## Ishlash natijasi:
```text
Hali qiymat chaqirilmadi.
Qimmat hisob-kitob bajarildi!
Qiymat: 4200
Ikkinchi chaqiruv: 4200
```


# 250-Topshiriq: Amaliy loyiha: Funktsional reaktiv buyurtmalar tahlili va saralash tizimi
## Topshiriq sharti:
Katta onlayn do'kon buyurtmalarini funktsional zanjir (filter, map, sorted, reduce) orqali to'liq qayta ishlovchi modul.

## Yechim (Swift kodi):
```swift
import Foundation

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
    .filter(\.isDelivered)
    .flatMap(\.items)
    .map { $0.price * Double($0.quantity) }
    .reduce(0.0, +)

print("Yetkazilgan buyurtmalardan tushgan sof daromad: $\(deliveredRevenue)")

// Har bir xaridor bo'yicha buyurtma summasini saralash:
let customerSummaries = orders.map { order -> (customer: String, total: Double) in
    let total = order.items.reduce(0.0) { $0 + ($1.price * Double($1.quantity)) }
    return (order.customer, total)
}.sorted { $0.total > $1.total }

for s in customerSummaries {
    print("Mijoz: \(s.customer) - Jami: $\(s.total)")
}
```

## Tushuntirish va Mantiq:
Ushbu yakuniy amaliy loyihada Swift-ning barcha asosiy funktsional imkoniyatlari: 'filter', 'flatMap', 'map', 'reduce', KeyPath (\.isDelivered) va kortejlar yordamida real biznes tahlili amalga oshirildi.

## Ishlash natijasi:
```text
Yetkazilgan buyurtmalardan tushgan sof daromad: $1474.0
Mijoz: Aziz - Jami: $1057.0
Mijoz: Nilufar - Jami: $599.0
Mijoz: Botir - Jami: $417.0
```

