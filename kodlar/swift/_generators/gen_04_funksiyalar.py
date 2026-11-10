# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

tasks_data = [
    (
        151,
        "Funksiya e'lon qilish va chaqirish asoslari",
        "Foydalanuvchiga salom beruvchi va tizim vaqtini ko'rsatuvchi standart funksiya yozing.",
        """import Foundation

func printSystemGreeting() {
    print("Xush kelibsiz! Khorazmiy AI tizimi faol.")
}

printSystemGreeting()
""",
        "Swift-da funksiyalar 'func' kalit so'zi bilan e'lon qilinadi, nomidan so'ng qavslar va funksiya tanasi jingalak qavsda yoziladi.",
        """Xush kelibsiz! Khorazmiy AI tizimi faol."""
    ),
    (
        152,
        "Qiymat qaytarmaydigan funksiyalar: Void va ()",
        "Funksiyaning qaytarish turi Void yoki () ekanligini ko'rsating.",
        """import Foundation

func logActivity(message: String) -> Void {
    print("[LOG]: \\(message)")
}

func logDebug(message: String) -> () {
    print("[DEBUG]: \\(message)")
}

logActivity(message: "Foydalanuvchi tizimga kirdi")
logDebug(message: "Xotira 45MB band")
""",
        "Swift-da agar funksiya hech qanday natija qaytarmasa, qaytish turi yozilmasligi mumkin, yoki 'Void', yoxud bo'sh kortej '()' deb belgilanishi mumkin.",
        """[LOG]: Foydalanuvchi tizimga kirdi
[DEBUG]: Xotira 45MB band"""
    ),
    (
        153,
        "Parametrlarga ega va qiymat qaytaruvchi funksiya",
        "Ikki sonning ko'paytmasini hisoblab qaytaruvchi funksiya tuzing.",
        """import Foundation

func multiply(a: Int, b: Int) -> Int {
    return a * b
}

let result = multiply(a: 7, b: 8)
print("7 * 8 = \\(result)")
""",
        "Funksiya parametrlari 'nom: Tip' shaklida beriladi, natija turi esa ko'rsatkich '->' belgisi bilan ifodalanadi.",
        """7 * 8 = 56"""
    ),
    (
        154,
        "Argument yorliqlari (Argument Labels) va parametr nomlari",
        "Tashqi chaqiruvda boshqa nom, ichki kodda boshqa nom ishlatuvchi funksiya yozing.",
        """import Foundation

func calculateTax(for grossIncome: Double, withRate rate: Double) -> Double {
    return grossIncome * rate
}

let tax = calculateTax(for: 5000.0, withRate: 0.12)
print("Soliq miqdori: $\\(tax)")
""",
        "Swift-da har bir parametr ikkita nomga ega bo'lishi mumkin: tashqi argument yorlig'i (argument label) va ichki parametr nomi (parameter name). Bu ingliz tili jumlalari kabi ravon o'qilishini ta'minlaydi.",
        """Soliq miqdori: $600.0"""
    ),
    (
        155,
        "Tashqi argument yorlig'ini yashirish (Wildcard '_')",
        "Chaqirish paytida parametr nomini yozmaslik uchun '_' dan foydalaning.",
        """import Foundation

func square(_ number: Int) -> Int {
    return number * number
}

let res = square(9)
print("9 ning kvadrati: \\(res)")
""",
        "Agar tashqi argument yorlig'i o'rniga pastki chiziq (_) qo'yilsa, funksiyani chaqirishda parametr nomini yozish shart bo'lmaydi.",
        """9 ning kvadrati: 81"""
    ),
    (
        156,
        "Apple API Design Guidelines bo'yicha parametr nomlash",
        "Apple standartlari bo'yicha inglizcha grammatikaga mos ravon funksiya sarlavhasi tuzing.",
        """import Foundation

func move(from startCity: String, to destinationCity: String) {
    print("\\(startCity) shahridan \\(destinationCity) shahriga yo'lga chiqildi.")
}

move(from: "Toshkent", to: "Samarqand")
""",
        "Apple API Design Guidelines ga ko'ra, funksiya chaqirilishi tabiiy jumla kabi o'qilishi lozim: 'move(from: A, to: B)'.",
        """Toshkent shahridan Samarqand shahriga yo'lga chiqildi."""
    ),
    (
        157,
        "Standart parametr qiymatlari (Default Parameter Values)",
        "Xabar yuborishda port va timeout parametrlariga default qiymatlar bering.",
        """import Foundation

func sendPacket(data: String, port: Int = 8080, timeout: Double = 30.0) {
    print("Ma'lumot: '\\(data)', Port: \\(port), Kutilish: \\(timeout)s")
}

sendPacket(data: "Salom")
sendPacket(data: "Maxfiy", port: 443)
sendPacket(data: "Tezkor", port: 9000, timeout: 5.0)
""",
        "Standart qiymatga ega parametrlar funksiya chaqirilganda kiritilishi ixtiyoriydir. Bu funksiya versiyalarini ko'paytirmasdan qulaylik yaratadi.",
        """Ma'lumot: 'Salom', Port: 8080, Kutilish: 30.0s
Ma'lumot: 'Maxfiy', Port: 443, Kutilish: 30.0s
Ma'lumot: 'Tezkor', Port: 9000, Kutilish: 5.0s"""
    ),
    (
        158,
        "O'zgaruvchan sondagi parametrlar (Variadic Parameters: ...)",
        "Ixtiyoriy miqdordagi sonlarning o'rtacha arifmetigini hisoblovchi variadic funksiya yozing.",
        """import Foundation

func average(_ numbers: Double...) -> Double {
    guard !numbers.isEmpty else { return 0.0 }
    let total = numbers.reduce(0, +)
    return total / Double(numbers.count)
}

print("O'rtacha (3 ta son): \\(average(10.0, 20.0, 30.0))")
print("O'rtacha (5 ta son): \\(average(5.0, 15.0, 25.0, 35.0, 45.0))")
""",
        "Tip nomidan so'ng uchta nuqta (...) qo'yilishi parametrni variadic qiladi. Funksiya tanasi ichida u mos turdagi massiv ([T]) sifatida qabul qilinadi.",
        """O'rtacha (3 ta son): 20.0
O'rtacha (5 ta son): 25.0"""
    ),
    (
        159,
        "Bir nechta variadic parametrlarga ega funksiya (Swift 5.4+)",
        "Bir vaqtning o'zida ikkita turli variadic argumentlarni qabul qiluvchi funksiyani ko'rsating.",
        """import Foundation

func processBatch(tags: String..., values: Int...) {
    print("Teglar: \\(tags), Qiymatlar: \\(values)")
}

processBatch(tags: "iOS", "Swift", values: 10, 20, 30)
""",
        "Swift 5.4 dan boshlab bitta funksiyada bir nechta variadic parametrlar ishlatishga ruxsat berilgan, faqat ularning argument yorliqlari aniq ko'rsatilishi lozim.",
        """Teglar: ["iOS", "Swift"], Qiymatlar: [10, 20, 30]"""
    ),
    (
        160,
        "inout parametrlari: Xotira manzilini o'zgartirish (Pass-by-reference)",
        "Ikkita sonning qiymatini almashtiruvchi maxsus swap funksiyasini 'inout' bilan yozing.",
        """import Foundation

func customSwap(a: inout Int, b: inout Int) {
    let temp = a
    a = b
    b = temp
}

var x = 100
var y = 200
print("Oldin: x=\\(x), y=\\(y)")

customSwap(a: &x, b: &y)
print("Keyin: x=\\(x), y=\\(y)")
""",
        "'inout' parametri qiymatning nusxasini emas, balki funksiyaga o'zgaruvchining manzilini uzatadi. Chaqirish paytida o'zgaruvchi oldiga '&' belgisi qo'yiladi.",
        """Oldin: x=100, y=200
Keyin: x=200, y=100"""
    ),
    (
        161,
        "inout ning Copy-In Copy-Out modeli",
        "Funksiya ichida o'zgartirilgan parametr faqat funksiya tugaganda tashqi manzilga yozilishini isbotlang.",
        """import Foundation

var globalCounter = 10

func modify(val: inout Int) {
    val += 5
    // Bu yerda val qiymati 15 bo'ladi
}

modify(val: &globalCounter)
print("Yakuniy hisoblagich: \\(globalCounter)")
""",
        "Swift inout parametrlarida 'call-by-value-result' (copy-in copy-out) modelidan foydalanadi: parametr chaqirilganda nusxalanadi va funksiyadan chiqishda yana joyiga qaytarib yoziladi.",
        """Yakuniy hisoblagich: 15"""
    ),
    (
        162,
        "Funksiyadan nomlangan Tuple qaytarish",
        "Matndan undosh va unli harflar sonini bitta funksiyada hisoblang.",
        """import Foundation

func countLetters(in text: String) -> (vowels: Int, consonants: Int) {
    let vowelsSet: Set<Character> = ["a", "e", "i", "o", "u"]
    var vCount = 0
    var cCount = 0
    
    for char in text.lowercased() where char.isLetter {
        if vowelsSet.contains(char) {
            vCount += 1
        } else {
            cCount += 1
        }
    }
    return (vowels: vCount, consonants: cCount)
}

let counts = countLetters(in: "Swift Tilida Funksiyalar")
print("Unlilar: \\(counts.vowels) ta, Undoshlar: \\(counts.consonants) ta")
""",
        "Nomlangan kortejlar funksiyadan bir nechta bog'liq ma'lumotlarni alohida struktura tuzmasdan qaytarishning eng toza usulidir.",
        """Unlilar: 7 ta, Undoshlar: 14 ta"""
    ),
    (
        163,
        "Funksiyadan Optional qaytarish",
        "Foydalanuvchilar ro'yxatidan ID bo'yicha qidirib, topilmasa nil qaytaring.",
        """import Foundation

let usersDB = [1: "Sardor", 2: "Nodira", 3: "Javohir"]

func findUser(by id: Int) -> String? {
    return usersDB[id]
}

if let user = findUser(by: 2) {
    print("Topildi: \\(user)")
}

let notFound = findUser(by: 99)
print("Mavjud bo'lmagan: \\(notFound ?? "Topilmadi")")
""",
        "Agar funksiya natijasi har doim ham mavjud bo'lmasligi mumkin bo'lsa, qaytarish turi 'T?' qilinadi.",
        """Topildi: Nodira
Mavjud bo'lmagan: Topilmadi"""
    ),
    (
        164,
        "Funksiya tiplari (Function Types): (T1, T2) -> R",
        "Funksiyani oddiy o'zgaruvchi kabi e'lon qilib unga boshqa funksiyani biriktiring.",
        """import Foundation

func addNumbers(_ a: Int, _ b: Int) -> Int {
    return a + b
}

var mathOperation: (Int, Int) -> Int = addNumbers

let calc = mathOperation(15, 25)
print("Hisoblangan: \\(calc)")
""",
        "Swift-da funksiyalar 'birinchi darajali fuqarolar' (first-class citizens) hisoblanadi. Funksiyaning ham o'z tipi mavjud: masalan, (Int, Int) -> Int.",
        """Hisoblangan: 40"""
    ),
    (
        165,
        "Funksiyani parametr sifatida uzatish",
        "Matnlarni filtrlovchi va transformatsiya qiluvchi umumiy funksiya tuzing.",
        """import Foundation

func applyOperation(on value: Int, using function: (Int) -> Int) -> Int {
    return function(value)
}

func triple(_ n: Int) -> Int {
    return n * 3
}

let ans = applyOperation(on: 12, using: triple)
print("12 ning 3 karraligi: \\(ans)")
""",
        "Boshqa funksiyani parametr qilib oluvchi yoki funksiya qaytaruvchi funksiyalar 'Yuqori Tartibli Funksiyalar' (Higher-Order Functions) deyiladi.",
        """12 ning 3 karraligi: 36"""
    ),
    (
        166,
        "Funksiyadan yangi funksiya qaytarish",
        "Qadam o'lchamiga qarab maxsus hisoblagich funksiya ishlab chiqaruvchi zavod funksiya tuzing.",
        """import Foundation

func makeStepCounter(step: Int) -> (Int) -> Int {
    func counter(value: Int) -> Int {
        return value + step
    }
    return counter
}

let stepByFive = makeStepCounter(step: 5)
print("10 ga 5 qo'shildi: \\(stepByFive(10))")
print("20 ga 5 qo'shildi: \\(stepByFive(20))")
""",
        "Funksiya boshqa ichki funksiyani qaytarishi mumkin. Bu funktsional dasturlashda moslashuvchanlikni oshiradi.",
        """10 ga 5 qo'shildi: 15
20 ga 5 qo'shildi: 25"""
    ),
    (
        167,
        "Ichma-ich funksiyalar (Nested Functions)",
        "Murakkab hisoblash mantiqini funksiya ichida yordamchi funksiyachalarga ajrating.",
        """import Foundation

func calculateTotalCost(price: Double, isVIP: Bool) -> Double {
    func applyVIPDiscount(_ base: Double) -> Double {
        return base * 0.85
    }
    
    func applyDeliveryFee(_ base: Double) -> Double {
        return base + 10.0
    }
    
    let discounted = isVIP ? applyVIPDiscount(price) : price
    return applyDeliveryFee(discounted)
}

print("VIP narxi: $\\(calculateTotalCost(price: 100.0, isVIP: true))")
print("Oddiy narx: $\\(calculateTotalCost(price: 100.0, isVIP: false))")
""",
        "Funksiya tanasi ichida e'lon qilingan funksiyalar 'nested functions' deyiladi. Ular faqat o'sha ota funksiya ichida ko'rinadi va kodni toza saqlaydi.",
        """VIP narxi: $95.0
Oddiy narx: $110.0"""
    ),
    (
        168,
        "Natijani e'tiborsiz qoldirish: @discardableResult",
        "Qaytargan qiymati o'zgaruvchiga olinmasa ham ogohlantirish bermaydigan metod yozing.",
        """import Foundation

class ShoppingCart {
    var items: [String] = []
    
    @discardableResult
    func addItem(_ item: String) -> Int {
        items.append(item)
        return items.count
    }
}

let cart = ShoppingCart()
cart.addItem("MacBook") // Qaytgan Int qiymat olinmasa ham warning chiqmaydi!
let totalItems = cart.addItem("iPhone")
print("Savatdagi jami mahsulotlar: \\(totalItems)")
""",
        "Odatda Swift qaytgan qiymat ishlatilmasa ogohlantirish (warning) beradi. '@discardableResult' atributi esa kompilyatorga natijani ishlatmaslik normal holat ekanligini bildiradi.",
        """Savatdagi jami mahsulotlar: 2"""
    ),
    (
        169,
        "Rekursiv funksiyalar: Faktorial hisoblash",
        "Matematik faktorialni funksiyaning o'z-o'zini chaqirishi orqali hisoblang.",
        """import Foundation

func factorial(_ n: Int) -> Int {
    if n <= 1 {
        return 1
    }
    return n * factorial(n - 1)
}

print("5 faktorial = \\(factorial(5))")
""",
        "Rekursiyada albatta to'xtash sharti (base condition) bo'lishi shart, aks holda stack overflow yuz beradi.",
        """5 faktorial = 120"""
    ),
    (
        170,
        "Funksiyalarni qayta yuklash (Function Overloading)",
        "Bir xil nomli, ammo har xil parametrli bir nechta funksiyalarni e'lon qiling.",
        """import Foundation

func printDetail(_ value: Int) {
    print("Butun son: \\(value)")
}

func printDetail(_ value: String) {
    print("Matn qatori: \\(value)")
}

func printDetail(_ value: Double, precision: Int) {
    print("Aniq son: \\(String(format: "%.*f", precision, value))")
}

printDetail(42)
printDetail("Swift 5.9")
printDetail(3.14159, precision: 2)
""",
        "Swift parametrlari soni, turi yoki argument yorliqlari har xil bo'lgan bir xil nomli funksiyalarni muammosiz ajrata oladi.",
        """Butun son: 42
Matn qatori: Swift 5.9
Aniq son: 3.14"""
    ),
    (
        171,
        "Xatolik tashlovchi funksiyalar: throws va try",
        "Noto'g'ri kiritish holatida maxsus xato tashlovchi funksiya yarating.",
        """import Foundation

enum ValidationError: Error {
    case emptyText
    case tooShort(minimum: Int)
}

func validateUsername(_ name: String) throws -> String {
    if name.isEmpty {
        throw ValidationError.emptyText
    }
    if name.count < 4 {
        throw ValidationError.tooShort(minimum: 4)
    }
    return name.lowercased()
}

do {
    let valid = try validateUsername("Ali")
    print("Muvaffaqiyatli: \\(valid)")
} catch ValidationError.tooShort(let min) {
    print("Xato: Ism kamida \\(min) ta belgidan iborat bo'lishi kerak!")
} catch {
    print("Boshqa xato: \\(error)")
}
""",
        "'throws' kalit so'zi funksiya o'z ishida istisno (Error) yuzaga keltirishi mumkinligini bildiradi. Uni chaqirishda 'try' qo'yish majburiydir.",
        """Xato: Ism kamida 4 ta belgidan iborat bo'lishi kerak!"""
    ),
    (
        172,
        "Qayta xatolik tashlash: 'rethrows' kalit so'zi",
        "Parametr qilib olingan closure xato tashlasagina o'zi ham xato tashlaydigan funksiyani ko'rsating.",
        """import Foundation

func runSafely(action: () throws -> Void) rethrows {
    print("Harakat boshlandi...")
    try action()
    print("Harakat muvaffaqiyatli yakunlandi.")
}

// Xato tashlamaydigan closure berilganda 'try' talab qilinmaydi:
runSafely {
    print("Oddiy xavfsiz kod bajarildi.")
}
""",
        "'rethrows' faqat o'z parametrlaridagi closure lardan kelib chiqqan holda xatolik otadi. Agar berilgan closure xato tashlamasa, chaqiruvchi kod 'try' yozishi shart emas.",
        """Harakat boshlandi...
Oddiy xavfsiz kod bajarildi.
Harakat muvaffaqiyatli yakunlandi."""
    ),
    (
        173,
        "defer operatori bilan resurslarni kafolatli tozalash",
        "Fayl yoki ulanish ochilganda funksiyadan qanday chiqilishidan qat'i nazar uni yopishni ta'minlang.",
        """import Foundation

func openAndProcessFile() {
    print("1. Fayl ochildi.")
    defer {
        print("4. Fayl xavfsiz yopildi (defer).")
    }
    
    print("2. Fayl ma'lumotlari o'qilmoqda...")
    print("3. O'qish yakunlandi.")
}

openAndProcessFile()
""",
        "'defer' bloki funksiyadan normal chiqiladimi, 'return' bo'ladimi yoki xato 'throw' qilinadimi — albatta eng oxirida ishga tushadi.",
        """1. Fayl ochildi.
2. Fayl ma'lumotlari o'qilmoqda...
3. O'qish yakunlandi.
4. Fayl xavfsiz yopildi (defer)."""
    ),
    (
        174,
        "Bir nechta defer bloklarining LIFO tartibi",
        "Bir nechta defer yozilganda ularning teskari (oxirgi kirgan - birinchi chiqqan) tartibda ishlashini ko'rsating.",
        """import Foundation

func deferSequence() {
    print("Boshlanish")
    defer { print("1-defer (oxirida)") }
    defer { print("2-defer (o'rtada)") }
    defer { print("3-defer (birinchi bo'lib)") }
    print("Tugash")
}

deferSequence()
""",
        "Swift-da bir nechta 'defer' bloklari stek (LIFO - Last-In-First-Out) tamoyilida ishlaydi: oxirgi e'lon qilingan defer eng birinchi bo'lib ijro etiladi.",
        """Boshlanish
Tugash
3-defer (birinchi bo'lib)
2-defer (o'rtada)
1-defer (oxirida)"""
    ),
    (
        175,
        "Hech qachon qaytmaydigan funksiyalar: Never qaytish turi",
        "Ilovaning to'xtatuvchi tizim funksiyalarida 'Never' turini qo'llang.",
        """import Foundation

func terminateApp(withReason reason: String) -> Never {
    print("Kritik xatolik: \\(reason). Tizim to'xtatildi.")
    exit(1)
}

// terminateApp(withReason: "Xotira buzildi") // Bu funksiya hech qachon chaqiruvchiga qaytib kelmaydi
print("Never turi kompilyatorga funksiyadan keyingi kod bajarilmasligini bildiradi.")
""",
        "'Never' qaytaruvchi funksiya dastur oqimini doimiy to'xtatadi yoki cheksiz tsiklga kiradi. Kompilyator bunday funksiyadan keyin 'return' talab qilmaydi.",
        """Never turi kompilyatorga funksiyadan keyingi kod bajarilmasligini bildiradi."""
    ),
    (
        176,
        "Asinxron funksiyalar: async va await",
        "Tarmoqdan ma'lumot yuklashni simulyatsiya qiluvchi zamonaviy 'async' funksiya yozing.",
        """import Foundation

func fetchServerTime() async -> String {
    try? await Task.sleep(nanoseconds: 10_000_000) // 10ms kutish
    return "2026-11-08T12:00:00Z"
}

Task {
    let time = await fetchServerTime()
    print("Server vaqti olindi: \\(time)")
}
""",
        "Swift modern concurrency tizimida 'async' funksiyalar oqimni (thread) to'sib qo'ymasdan (non-blocking) vaqtinchalik to'xtatib turishga imkon beradi.",
        """Server vaqti olindi: 2026-11-08T12:00:00Z"""
    ),
    (
        177,
        "async throws kombinatsiyasi",
        "Ham asinxron, ham xatolik tashlashi mumkin bo'lgan funksiyani tuzing.",
        """import Foundation

enum NetworkError: Error {
    case timeout
}

func downloadUserData(id: Int) async throws -> String {
    if id <= 0 {
        throw NetworkError.timeout
    }
    return "Foydalanuvchi ma'lumotlari #\\(id)"
}

Task {
    do {
        let user = try await downloadUserData(id: 42)
        print("Yuklandi: \\(user)")
    } catch {
        print("Yuklashda xato: \\(error)")
    }
}
""",
        "'async throws' bir vaqtning o'zida asinxronlik va xatoliklarni boshqarishni birlashtiradi. Chaqirilganda 'try await' ketma-ketligi yoziladi.",
        """Yuklandi: Foydalanuvchi ma'lumotlari #42"""
    ),
    (
        178,
        "Generik funksiya asoslari",
        "Ixtiyoriy turdagi massivning oxirgi va birinchi elementini almashtiruvchi funksiya yozing.",
        """import Foundation

func swapFirstAndLast<T>(_ array: inout [T]) {
    guard array.count > 1 else { return }
    let lastIdx = array.count - 1
    array.swapAt(0, lastIdx)
}

var numbers = [1, 2, 3, 4]
swapFirstAndLast(&numbers)
print("Sonlar almashdi: \\(numbers)")

var words = ["Boshi", "O'rtasi", "Oxiri"]
swapFirstAndLast(&words)
print("So'zlar almashdi: \\(words)")
""",
        "Generik funksiyalar ('<T>') kodni bitta yozib, har qanday ma'lumot turi bilan tip xavfsizligini yo'qotmagan holda qayta ishlatish imkonini beradi.",
        """Sonlar almashdi: [4, 2, 3, 1]
So'zlar almashdi: ["Oxiri", "O'rtasi", "Boshi"]"""
    ),
    (
        179,
        "Funksiya kompozitsiyasi (Function Composition)",
        "Ikkita mustaqil funksiyani birlashtirib yangi funksiya hosil qiluvchi kompozitor yozing.",
        """import Foundation

func addFive(_ x: Int) -> Int { return x + 5 }
func multiplyTwo(_ x: Int) -> Int { return x * 2 }

func compose(_ f: @escaping (Int) -> Int, _ g: @escaping (Int) -> Int) -> (Int) -> Int {
    return { x in g(f(x)) }
}

let addThenMultiply = compose(addFive, multiplyTwo)
// (3 + 5) * 2 = 16
print("Natija: \\(addThenMultiply(3))")
""",
        "Funksiya kompozitsiyasi funktsional dasturlashning asosiy ustunlaridan biri bo'lib, kichik va mustaqil funksiyalardan murakkab konveyerlar qurishga xizmat qiladi.",
        """Natija: 16"""
    ),
    (
        180,
        "Memoizatsiya (Memoization) orqali keshlovchi funksiya",
        "Qimmat hisob-kitoblar natijasini lug'atda keshlab oluvchi funksiya yarating.",
        """import Foundation

func makeMemoizedSquare() -> (Int) -> Int {
    var cache: [Int: Int] = [:]
    return { n in
        if let cached = cache[n] {
            print("Keshdan olindi (\\(n))")
            return cached
        }
        let computed = n * n
        cache[n] = computed
        print("Yangi hisoblandi (\\(n))")
        return computed
    }
}

let square = makeMemoizedSquare()
print(square(4))
print(square(4)) // Keshdan chiqadi
""",
        "Memoizatsiya qimmat hisoblangan natijalarni xotirada saqlab, bir xil kiruvchi parametrlar uchun qayta hisoblashni chetlab o'tadi.",
        """Yangi hisoblandi (4)
16
Keshdan olindi (4)
16"""
    ),
    (
        181,
        "Valyutani formatlovchi funksiya",
        "Sonni o'zbek so'mi yoki dollar ko'rinishida formatlab chiquvchi yordamchi funksiya.",
        """import Foundation

func formatCurrency(amount: Double, code: String = "UZS") -> String {
    let formattedNumber = String(format: "%.2f", amount)
    return "\\(formattedNumber) \\(code)"
}

print(formatCurrency(amount: 150000.5))
print(formatCurrency(amount: 49.99, code: "USD"))
""",
        "Biznes logikada doimiy ishlatiladigan formatlash funksiyalari aniq parametrlar bilan arxitekturani yengillashtiradi.",
        """150000.50 UZS
49.99 USD"""
    ),
    (
        182,
        "Predicate logikasi: Filtrlash qoidasi funksiyasi",
        "Massivdan muayyan qoidaga mos elementlarni tanlovchi universal funksiya tuzing.",
        """import Foundation

func filterList<T>(items: [T], predicate: (T) -> Bool) -> [T] {
    var result: [T] = []
    for item in items {
        if predicate(item) {
            result.append(item)
        }
    }
    return result
}

let words = ["Kitob", "Oyna", "Kompyuter", "Uy"]
let longWords = filterList(items: words) { $0.count > 5 }
print("5 tadan uzun so'zlar: \\(longWords)")
""",
        "Predicate — mantiqiy Bool qaytaruvchi funksiya bo'lib, u ma'lumotlarni saralash va filtrlash shartini ifodalaydi.",
        """5 tadan uzun so'zlar: ["Kompyuter"]"""
    ),
    (
        183,
        "Karrilash (Currying) tushunchasi funksiyalarda",
        "Ko'p parametrli funksiyani bitta parametrdan qabul qiluvchi zanjirli funksiyalarga ajrating.",
        """import Foundation

func curriedAdd(_ a: Int) -> (Int) -> Int {
    return { b in a + b }
}

let addTen = curriedAdd(10)
print("10 + 5 = \\(addTen(5))")
print("10 + 20 = \\(addTen(20))")
""",
        "Karrilash (Currying) f(a, b) funksiyasini f(a)(b) ko'rinishidagi zanjirga aylantirish usulidir.",
        """10 + 5 = 15
10 + 20 = 30"""
    ),
    (
        184,
        "Swift 5.9 Typed Throws ga poydevor yaratish",
        "Aniq xatolik turiga ixtisoslashgan Result qaytaruvchi mustahkam funksiya.",
        """import Foundation

enum MathError: Error {
    case divisionByZero
}

func safeDivide(_ a: Double, _ b: Double) -> Result<Double, MathError> {
    guard b != 0 else {
        return .failure(.divisionByZero)
    }
    return .success(a / b)
}

switch safeDivide(10.0, 2.0) {
case .success(let val):
    print("Natija: \\(val)")
case .failure(let err):
    print("Xato: \\(err)")
}
""",
        "Result tipi muvaffaqiyat (Success) va aniq xatolik (Failure: Error) turlarini o'zida saqlovchi mustahkam funktsional yechimdir.",
        """Natija: 5.0"""
    ),
    (
        185,
        "Kompilyator optimizatsiyasi: @inline(__always)",
        "Juda kichik va tez-tez chaqiriladigan funksiyalarni to'g'ridan-to'g'ri chaqiruv nuqtasiga joylashtirishni ko'rsating.",
        """import Foundation

@inline(__always)
func fastMin(_ a: Int, _ b: Int) -> Int {
    return a < b ? a : b
}

let m = fastMin(14, 8)
print("Minimal: \\(m)")
""",
        "'@inline(__always)' atributi kompilyatorga funksiya chaqirish xarajatlarini (call overhead) yo'qotib, kodni to'g'ridan-to'g'ri shu nuqtaga qo'yishni buyuradi.",
        """Minimal: 8"""
    ),
    (
        186,
        "Matritsani tekshiruvchi funksiya",
        "Ikki o'lchamli massiv to'g'ri to'rtburchak matritsa ekanligini tasdiqlang.",
        """import Foundation

func isValidMatrix(_ grid: [[Int]]) -> Bool {
    guard let firstRow = grid.first, !firstRow.isEmpty else { return false }
    let expectedCols = firstRow.count
    return grid.allSatisfy { $0.count == expectedCols }
}

let m1 = [[1, 2], [3, 4], [5, 6]]
let m2 = [[1, 2], [3]]

print("m1 matritsami? \\(isValidMatrix(m1))")
print("m2 matritsami? \\(isValidMatrix(m2))")
""",
        "Funksiya ma'lumotlar tuzilmasining barcha elementlarini allSatisfy orqali tekshirib to'g'riligini kafolatlaydi.",
        """m1 matritsami? true
m2 matritsami? false"""
    ),
    (
        187,
        "C kutubxonalari bilan moslik: @convention(c)",
        "C tili bilan interfeys hosil qiluvchi funksiya ko'rsatkichini e'lon qiling.",
        """import Foundation

let cFunction: @convention(c) (Int32, Int32) -> Int32 = { a, b in
    return a + b
}

let sum = cFunction(10, 20)
print("C uslubidagi funksiya natijasi: \\(sum)")
""",
        "'@convention(c)' atributi Swift funksiyasini C dasturlash tilidagi oddiy ko'rsatkich (function pointer) sifatida talqin qilish imkonini beradi.",
        """C uslubidagi funksiya natijasi: 30"""
    ),
    (
        188,
        "Funksiya parametrlarining o'zgarmasligi (let xususiyati)",
        "Funksiya parametrlari standart holda o'zgarmas ekanligini va uni qanday qayta ishlashni ko'rsating.",
        """import Foundation

func normalizeScore(input: Int) -> Int {
    // input += 5 // Kompilyatsiya xatosi: 'input' is a 'let' constant
    var mutableInput = input
    mutableInput += 5
    return min(mutableInput, 100)
}

print("Ball: \\(normalizeScore(input: 98))")
""",
        "Swift-da barcha funksiya parametrlari avtomatik ravishda 'let' o'zgarmaslaridir. Ularni o'zgartirish uchun lokal nusxa olinishi yoki 'inout' qo'llanishi kerak.",
        """Ball: 100"""
    ),
    (
        189,
        "Builder pattern uslubidagi ravon (fluent) funksiyalar",
        "Obyektni sozlab o'zini qaytaruvchi metodlar zanjirini yarating.",
        """import Foundation

class AlertBuilder {
    private var title = ""
    private var message = ""
    
    func setTitle(_ title: String) -> AlertBuilder {
        self.title = title
        return self
    }
    
    func setMessage(_ message: String) -> AlertBuilder {
        self.message = message
        return self
    }
    
    func build() -> String {
        return "Ogohlantirish: [\\(title)] - \\(message)"
    }
}

let alert = AlertBuilder()
    .setTitle("Xato")
    .setMessage("Tarmoq bilan aloqa yo'q")
    .build()

print(alert)
""",
        "O'zini ('self') qaytaruvchi funksiyalar zanjirli chaqiruvlarni (method chaining) tashkil etishda juda qulaydir.",
        """Ogohlantirish: [Xato] - Tarmoq bilan aloqa yo'q"""
    ),
    (
        190,
        "Matndan raqamlarni ajratuvchi sanitizatsiya funksiyasi",
        "Telefon raqamidagi ortiqcha belgilarni tozalovchi funksiya yozing.",
        """import Foundation

func sanitizePhoneNumber(_ raw: String) -> String {
    return raw.filter { $0.isNumber }
}

let phone = "+998 (90) 123-45-67"
let cleanPhone = sanitizePhoneNumber(phone)
print("Tozalangan raqam: \\(cleanPhone)")
""",
        "Oddiy va aniq vazifaga yo'naltirilgan funksiyalar kodning qayta ishlatilishini osonlashtiradi.",
        """Tozalangan raqam: 998901234567"""
    ),
    (
        191,
        "Matnni xavfsiz kesuvchi yordamchi funksiya",
        "Matn uzunligidan oshib ketmagan holda dastlabki N ta belgisini oluvchi funksiya.",
        """import Foundation

func safePrefix(_ text: String, maxLength: Int) -> String {
    return String(text.prefix(maxLength))
}

print("Prefix (5): \\(safePrefix("Khorazmiy", maxLength: 5))")
print("Prefix (20): \\(safePrefix("Swift", maxLength: 20))")
""",
        "'prefix' metodi massiv yoki matn chegarasidan chiqib ketish xatolarini xavfsiz hal qiladi.",
        """Prefix (5): Khora
Prefix (20): Swift"""
    ),
    (
        192,
        "Funksiyalar massivini boshqarish",
        "Bir nechta transformatsiya funksiyalarini massivga yig'ib ketma-ket qo'llang.",
        """import Foundation

let pipeline: [(String) -> String] = [
    { $0.trimmingCharacters(in: .whitespaces) },
    { $0.lowercased() },
    { $0.replacingOccurrences(of: " ", with: "_") }
]

var query = "  Khorazmiy AI Loyihasi  "
for transform in pipeline {
    query = transform(query)
}

print("Qayta ishlangan slug: \\(query)")
""",
        "Funksiya tiplaridan massiv yaratish orqali ma'lumotlarni qayta ishlovchi moslashuvchan konveyer (pipeline) tuzish mumkin.",
        """Qayta ishlangan slug: khorazmiy_ai_loyihasi"""
    ),
    (
        193,
        "Ko'p o'lchamli massivni tekislovchi funksiya",
        "Ichma-ich joylashgan massivlarni yagona qatorga keltiruvchi generik funksiya.",
        """import Foundation

func flatten<T>(_ arrays: [[T]]) -> [T] {
    var result: [T] = []
    for arr in arrays {
        result.append(contentsOf: arr)
    }
    return result
}

let nested = [[1, 2], [3, 4], [5]]
print("Tekislangan: \\(flatten(nested))")
""",
        "Generik funksiya har qanday turdagi ichma-ich massivlarni samarali birlashtiradi.",
        """Tekislangan: [1, 2, 3, 4, 5]"""
    ),
    (
        194,
        "Satrdagi so'zlarni sanovchi statistika funksiyasi",
        "Matndagi har bir so'z necha marta qatnashganini hisoblang.",
        """import Foundation

func wordFrequencies(in text: String) -> [String: Int] {
    let words = text.lowercased().split(separator: " ")
    var freqs: [String: Int] = [:]
    for word in words {
        freqs[String(word), default: 0] += 1
    }
    return freqs
}

let stats = wordFrequencies(in: "swift tezkor swift xavfsiz va zamonaviy")
print("So'zlar chastotasi: \\(stats)")
""",
        "Lug'atning 'default:' parametri bilan birlashtirilgan hisoblash funksiyasi juda ixcham kod beradi.",
        """So'zlar chastotasi: ["zamonaviy": 1, "tezkor": 1, "xavfsiz": 1, "va": 1, "swift": 2]"""
    ),
    (
        195,
        "Shartli ravishda qiymat almashtiruvchi inout funksiya",
        "Agar qiymat chegaradan past bo'lsa uni avtomatik minimal chegaraga tenglashtiring.",
        """import Foundation

func clampMin(value: inout Int, minLimit: Int) {
    if value < minLimit {
        value = minLimit
    }
}

var currentFps = 24
clampMin(value: &currentFps, minLimit: 30)
print("Moslashtirilgan FPS: \\(currentFps)")
""",
        "'inout' parametri orqali tashqi o'zgaruvchini funksiya ichida bevosita tekshirish va tuzatish mumkin.",
        """Moslashtirilgan FPS: 30"""
    ),
    (
        196,
        "Tasodifiy qiymat generator funksiyasi",
        "Berilgan oraliqdan tasodifiy son tanlovchi funksiya tuzing.",
        """import Foundation

func getRandomElement<T>(from array: [T]) -> T? {
    return array.randomElement()
}

let answers = ["Ha", "Yo'q", "Balki"]
let choice = getRandomElement(from: answers)
print("Tanlov: \\(choice ?? "")")
""",
        "Generik funksiya ixtiyoriy massivdan tasodifiy elementni xavfsiz ajratadi.",
        """Tanlov: Ha"""
    ),
    (
        197,
        "Sana va vaqt farqini soniyalarda hisoblovchi funksiya",
        "Ikki Date ob'ekti orasidagi vaqt farqini hisoblang.",
        """import Foundation

func secondsBetween(start: Date, end: Date) -> TimeInterval {
    return end.timeIntervalSince(start)
}

let now = Date()
let future = now.addingTimeInterval(120) // +2 daqiqa
let diff = secondsBetween(start: now, end: future)
print("Farq soniyalarda: \\(diff)s")
""",
        "Foundation-ning Date va TimeInterval turlari bilan ishlovchi sodda va aniq funksiya.",
        """Farq soniyalarda: 120.0s"""
    ),
    (
        198,
        "Xatolikni log qilib nil qaytaruvchi yordamchi wrapper funksiya",
        "Throwing funksiyani o'rab olib, nosozlik bo'lsa konsolga yozib nil beruvchi utilita yozing.",
        """import Foundation

func executeWithLogging<T>(_ action: () throws -> T) -> T? {
    do {
        return try action()
    } catch {
        print("[OGOHLANTIRISH]: Funksiya xato berdi: \\(error)")
        return nil
    }
}

let okResult = executeWithLogging { return 100 * 2 }
print("Natija: \\(okResult ?? 0)")
""",
        "Wrapper funksiyalar xatoliklarni qayta ishlashni markazlashtiradi.",
        """Natija: 200"""
    ),
    (
        199,
        "Rekursiya bilan massivdagi elementlar yig'indisini topish",
        "Tsikllarsiz, sof funktsional rekursiya orqali yig'indini hisoblang.",
        """import Foundation

func recursiveSum(_ list: [Int]) -> Int {
    guard let first = list.first else { return 0 }
    return first + recursiveSum(Array(list.dropFirst()))
}

print("Yig'indi: \\(recursiveSum([1, 2, 3, 4, 5]))")
""",
        "Funktsional dasturlashda rekursiya massiv boshini olib, qolgan qismiga o'zini chaqirish tamoyilida ishlaydi.",
        """Yig'indi: 15"""
    ),
    (
        200,
        "Amaliy loyiha: Matematik va Moliyaviy tahlil hisoblagich moduli",
        "Turli soliq, foiz stavkasi va oylik kredit to'lovlarini hisoblovchi yaxlit moliyaviy kalkulyator funksiyalar moduli.",
        """import Foundation

typealias FinancialResult = (monthlyPayment: Double, totalInterest: Double, totalPayout: Double)

func calculateLoan(principal: Double, annualRate: Double, months: Int) -> FinancialResult {
    let monthlyRate = (annualRate / 100.0) / 12.0
    let factor = pow(1.0 + monthlyRate, Double(months))
    let monthly = (principal * monthlyRate * factor) / (factor - 1.0)
    let totalPayout = monthly * Double(months)
    let totalInterest = totalPayout - principal
    
    return (monthlyPayment: monthly, totalInterest: totalInterest, totalPayout: totalPayout)
}

let loan = calculateLoan(principal: 10000.0, annualRate: 12.0, months: 12)
print("=== KREDIT HISOB-KITOBI ===")
print("Oylik to'lov:     $\\(String(format: "%.2f", loan.monthlyPayment))")
print("Jami foiz:        $\\(String(format: "%.2f", loan.totalInterest))")
print("Jami qaytarish:   $\\(String(format: "%.2f", loan.totalPayout))")
""",
        "Ushbu yakuniy loyihada 'typealias', nomlangan tuple qaytarish, formulali hisob-kitoblar va formatlash professional moliyaviy dastur shaklida mujassamlashtirildi.",
        """=== KREDIT HISOB-KITOBI ===
Oylik to'lov:     $888.49
Jami foiz:        $661.86
Jami qaytarish:   $10661.86"""
    )
]

tasks = [format_task(*t) for t in tasks_data]
save_file("swift_04_funksiyalar_va_inout_parametrlari.md", tasks)
