# 451-Topshiriq: Protokol e'lon qilish va qabul qilish asoslari
## Topshiriq sharti:
Qurilmaning yoqilishi va o'chirilishini ta'riflovchi protokol yarating va uni struct ga biriktiring.

## Yechim (Swift kodi):
```swift
import Foundation

protocol PowerControllable {
    func turnOn()
    func turnOff()
}

struct SmartBulb: PowerControllable {
    func turnOn() { print("Aqlli lampochka yoqildi.") }
    func turnOff() { print("Aqlli lampochka o'chirildi.") }
}

let bulb = SmartBulb()
bulb.turnOn()
bulb.turnOff()
```

## Tushuntirish va Mantiq:
Protokol (Protocol) — bu metodlar, xususiyatlar va boshqa talablarning qat'iy qolipidir (shartnomasi). Struktura, sinf yoki enum ushbu protokolni qabul qilib (adopt), undagi talablarni to'liq bajaradi.

## Ishlash natijasi:
```text
Aqlli lampochka yoqildi.
Aqlli lampochka o'chirildi.
```


# 452-Topshiriq: Xususiyat talablari: { get } va { get set }
## Topshiriq sharti:
Protokolda o'qiladigan va o'zgartiriladigan xususiyatlar talabini belgilang.

## Yechim (Swift kodi):
```swift
import Foundation

protocol IdentifiableItem {
    var id: String { get }
    var title: String { get set }
}

struct BookItem: IdentifiableItem {
    let id: String
    var title: String
}

var b = BookItem(id: "B-101", title: "Swift Asoslari")
b.title = "Swift 5.9 va Swift 6"
print("ID: \(b.id), Sarlavha: \(b.title)")
```

## Tushuntirish va Mantiq:
Protokol ichida maydon saqlanuvchimi yoki hisoblanganmi deb ko'rsatilmaydi, faqat uning nomi, turi va ruxsati ({ get } yoki { get set }) belgilanadi.

## Ishlash natijasi:
```text
ID: B-101, Sarlavha: Swift 5.9 va Swift 6
```


# 453-Topshiriq: mutating metod talablari (Struct lar uchun)
## Topshiriq sharti:
Struktura ichki holatini o'zgartira olishi uchun protokol metodiga 'mutating' qo'ying.

## Yechim (Swift kodi):
```swift
import Foundation

protocol Toggleable {
    mutating func toggle()
}

enum SwitchState: Toggleable {
    case on, off
    
    mutating func toggle() {
        self = (self == .on) ? .off : .on
    }
}

var light = SwitchState.off
light.toggle()
print("Holat: \(light)")
```

## Tushuntirish va Mantiq:
Agar protokol talab qilgan metod struktura yoki enum ichidagi qiymatlarni o'zgartirishi kutilsa, protokol deklaratsiyasida 'mutating' deb ko'rsatilishi shart.

## Ishlash natijasi:
```text
Holat: on
```


# 454-Topshiriq: Initsializator talablari va required init
## Topshiriq sharti:
Sinf protokol initsializatorini qabul qilganda 'required init' yozilishi shartligini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

protocol InitializableService {
    init(apiKey: String)
}

class CloudService: InitializableService {
    let apiKey: String
    
    required init(apiKey: String) {
        self.apiKey = apiKey
    }
}

let service = CloudService(apiKey: "API_998")
print("Servis kaliti: \(service.apiKey)")
```

## Tushuntirish va Mantiq:
Sinf protokoldan kelgan initsializatorni amalga oshirganda, uning barcha bo'lg'usi subclass lari ham bunga ega bo'lishi kafolatlanishi uchun 'required' so'zi majburiydir.

## Ishlash natijasi:
```text
Servis kaliti: API_998
```


# 455-Topshiriq: Faqat sinflar uchun protokollar: AnyObject
## Topshiriq sharti:
Protokolni faqat sinflar qabul qila oladigan qilib cheklang.

## Yechim (Swift kodi):
```swift
import Foundation

protocol CacheManagerDelegate: AnyObject {
    func cacheDidClear()
}

class MyDelegate: CacheManagerDelegate {
    func cacheDidClear() {
        print("Delegat xabardor qilindi: Kesh tozalandi.")
    }
}

let d = MyDelegate()
d.cacheDidClear()
```

## Tushuntirish va Mantiq:
'protocol MyProtocol: AnyObject' faqat sinflarga (Reference types) ruxsat beradi. Bu delegatsiya naqshida 'weak' ko'rsatkich ishlatish uchun shartdir.

## Ishlash natijasi:
```text
Delegat xabardor qilindi: Kesh tozalandi.
```


# 456-Topshiriq: Delegatsiya naqshi (Delegation Pattern) asoslari va weak havola
## Topshiriq sharti:
Tugma va uning bosilishini qabul qiluvchi delegat munosabatini yarating.

## Yechim (Swift kodi):
```swift
import Foundation

protocol ActionButtonDelegate: AnyObject {
    func buttonWasClicked()
}

class ActionButton {
    weak var delegate: ActionButtonDelegate?
    
    func tap() {
        print("Tugma bosildi.")
        delegate?.buttonWasClicked()
    }
}

class ScreenController: ActionButtonDelegate {
    func buttonWasClicked() {
        print("Ekran boshqaruvchisi: Tugma harakati ushlandi!")
    }
}

let screen = ScreenController()
let button = ActionButton()
button.delegate = screen
button.tap()
```

## Tushuntirish va Mantiq:
Delegatsiya — bu bir ob'ekt o'z vazifasini yoki hodisasini boshqa ob'ektga topshirish naqshidir. Retain Cycle (xotira sizib ketishi) oldini olish uchun delegat havolasi albatta 'weak' bo'lishi shart.

## Ishlash natijasi:
```text
Tugma bosildi.
Ekran boshqaruvchisi: Tugma harakati ushlandi!
```


# 457-Topshiriq: Protokollarni kengaytirish (Protocol Extensions): Standart realizatsiya
## Topshiriq sharti:
Protokol metodiga standart tana berib, uni ixtiyoriy qiling.

## Yechim (Swift kodi):
```swift
import Foundation

protocol Greetable {
    var name: String { get }
    func greet()
}

extension Greetable {
    func greet() {
        print("Assalomu alaykum, \(name)!")
    }
}

struct Employee: Greetable {
    let name: String
    // greet() yozish shart emas, default realizatsiya ishlaydi!
}

let emp = Employee(name: "Sherzod")
emp.greet()
```

## Tushuntirish va Mantiq:
Protocol Extension orqali barcha qabul qiluvchi tiplar uchun tayyor metod logikasini (Default Implementation) berish mumkin. Bu Swift-dagi Protocol-Oriented Programming (POP) asosidir.

## Ishlash natijasi:
```text
Assalomu alaykum, Sherzod!
```


# 458-Topshiriq: Protokol merosxo'rligi (Protocol Inheritance)
## Topshiriq sharti:
Bitta protokol boshqa protokolni kengaytirishi mumkinligini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

protocol Readable {
    func read()
}

protocol Writable {
    func write(data: String)
}

protocol FileStreamable: Readable, Writable {}

struct LocalFile: FileStreamable {
    func read() { print("Fayl o'qildi.") }
    func write(data: String) { print("Faylga yozildi: \(data)") }
}

let f = LocalFile()
f.read()
f.write(data: "Yangi satr")
```

## Tushuntirish va Mantiq:
Protokollar ham sinflar kabi boshqa protokollardan meros olishi va bir nechta protokollarni birlashtirishi mumkin.

## Ishlash natijasi:
```text
Fayl o'qildi.
Faylga yozildi: Yangi satr
```


# 459-Topshiriq: Protokol kompozitsiyasi (Protocol Composition: ProtocolA & ProtocolB)
## Topshiriq sharti:
Funksiya parametrida bir vaqtning o'zida bir nechta protokolni talab qiling.

## Yechim (Swift kodi):
```swift
import Foundation

protocol Named { var name: String { get } }
protocol Aged { var age: Int { get } }

struct User: Named, Aged {
    let name: String
    let age: Int
}

func printCelebration(celebrant: Named & Aged) {
    print("Tug'ilgan kuningiz bilan, \(celebrant.name)! \(celebrant.age) yosh muborak!")
}

let u = User(name: "Dilnoza", age: 24)
printCelebration(celebrant: u)
```

## Tushuntirish va Mantiq:
'&' operatori orqali yangi nomli protokol yaratmasdan, bir nechta protokol talablarini bir joyga kompozitsiya qilish mumkin.

## Ishlash natijasi:
```text
Tug'ilgan kuningiz bilan, Dilnoza! 24 yosh muborak!
```


# 460-Topshiriq: Protokolga moslikni tekshirish: is va as?
## Topshiriq sharti:
Kolleksiyadagi elementlar muayyan protokolga mos kelishini tekshiring.

## Yechim (Swift kodi):
```swift
import Foundation

protocol Playable {
    func play()
}

class AudioTrack: Playable {
    func play() { print("Musiqa yangramoqda...") }
}

class PhotoItem {}

let mediaList: [Any] = [AudioTrack(), PhotoItem()]

for item in mediaList {
    if let playable = item as? Playable {
        playable.play()
    } else {
        print("Ijro qilib bo'lmaydigan media.")
    }
}
```

## Tushuntirish va Mantiq:
Protokollarni oddiy tiplar kabi 'is' va 'as?' operatorlari orqali tekshirish va kasting qilish mumkin.

## Ishlash natijasi:
```text
Musiqa yangramoqda...
Ijro qilib bo'lmaydigan media.
```


# 461-Topshiriq: Standart protokol: CustomStringConvertible
## Topshiriq sharti:
Ob'ektning 'description' xususiyati orqali konsolga chiroyli chiqishini ta'minlang.

## Yechim (Swift kodi):
```swift
import Foundation

struct ServerStatus: CustomStringConvertible {
    let code: Int
    let text: String
    
    var description: String {
        return "Server Holati [\(code)]: \(text)"
    }
}

let status = ServerStatus(code: 200, text: "Barcha tizimlar normal")
print(status)
```

## Tushuntirish va Mantiq:
'CustomStringConvertible' protokoli tizimda String(describing:) va print() funksiyalari uchun matn taqdim etadi.

## Ishlash natijasi:
```text
Server Holati [200]: Barcha tizimlar normal
```


# 462-Topshiriq: Standart protokol: Equatable va avtomatik sintez
## Topshiriq sharti:
Tenglik operatorini (==) protokoldan avtomatik oling.

## Yechim (Swift kodi):
```swift
import Foundation

struct Vector2D: Equatable {
    let x: Double
    let y: Double
}

let v1 = Vector2D(x: 3.0, y: 4.0)
let v2 = Vector2D(x: 3.0, y: 4.0)
let v3 = Vector2D(x: 1.0, y: 0.0)

print("v1 == v2: \(v1 == v2)")
print("v1 == v3: \(v1 == v3)")
```

## Tushuntirish va Mantiq:
Barcha maydonlari Equatable bo'lgan strukturalarda 'Equatable' protokoli qo'shilishi bilan kompilyator '==' operatorini to'liq o'zi generatsiya qiladi.

## Ishlash natijasi:
```text
v1 == v2: true
v1 == v3: false
```


# 463-Topshiriq: Standart protokol: Comparable va saralash (<)
## Topshiriq sharti:
Ob'ektlarni tartiblash uchun faqat '<' operatorini yozing.

## Yechim (Swift kodi):
```swift
import Foundation

struct PriorityTask: Comparable {
    let title: String
    let priorityLevel: Int
    
    static func < (lhs: PriorityTask, rhs: PriorityTask) -> Bool {
        return lhs.priorityLevel < rhs.priorityLevel
    }
}

let t1 = PriorityTask(title: "Elektron pochta", priorityLevel: 2)
let t2 = PriorityTask(title: "Server nosozligi", priorityLevel: 10)

print("t1 < t2: \(t1 < t2)")
let sortedTasks = [t2, t1].sorted()
print("Birinchi: \(sortedTasks.first?.title ?? "")")
```

## Tushuntirish va Mantiq:
'Comparable' protokoli uchun faqat '<' operatori yozilsa kifoya: kompilyator qolgan barcha '>', '<=', '>=' operatorlarini avtomatik hosil qiladi.

## Ishlash natijasi:
```text
t1 < t2: true
Birinchi: Elektron pochta
```


# 464-Topshiriq: Standart protokol: Hashable va Dictionary kalitlari
## Topshiriq sharti:
Ob'ektni Set to'plamida va Dictionary kaliti sifatida ishlatish.

## Yechim (Swift kodi):
```swift
import Foundation

struct UserKey: Hashable {
    let departmentID: Int
    let employeeCode: String
}

var accessRights: [UserKey: String] = [:]
let key1 = UserKey(departmentID: 10, employeeCode: "EMP_A")
accessRights[key1] = "Admin ruxsati"

print("Ruxsat: \(accessRights[key1] ?? "")")
```

## Tushuntirish va Mantiq:
'Hashable' protokoli ob'ektning 'hash(into:)' xesh kodini hosil qiladi va uni Set va Lug'atlar uchun yaroqli qiladi.

## Ishlash natijasi:
```text
Ruxsat: Admin ruxsati
```


# 465-Topshiriq: Standart protokol: Identifiable
## Topshiriq sharti:
SwiftUI uchun unikal 'id' maydonini ta'minlovchi protokol.

## Yechim (Swift kodi):
```swift
import Foundation

struct CustomerProfile: Identifiable {
    let id: UUID
    let name: String
}

let customer = CustomerProfile(id: UUID(), name: "Nodir")
print("Identifikator o'rnatildi: \(customer.name)")
```

## Tushuntirish va Mantiq:
'Identifiable' protokoli faqat bitta 'id: Hashable' xususiyatini talab qiladi va SwiftUI List va ForEach ko'rinishlarida elementlarni tanib olish uchun ishlatiladi.

## Ishlash natijasi:
```text
Identifikator o'rnatildi: Nodir
```


# 466-Topshiriq: Standart protokol: CaseIterable
## Topshiriq sharti:
Enum barcha holatlarini ro'yxat sifatida olish (`allCases`).

## Yechim (Swift kodi):
```swift
import Foundation

enum AppTab: CaseIterable {
    case home, search, favorites, profile
}

print("Jami bo'limlar: \(AppTab.allCases.count) ta")
for tab in AppTab.allCases {
    print("- \(tab)")
}
```

## Tushuntirish va Mantiq:
'CaseIterable' enum ning barcha variantlarini 'allCases' massivi orqali taqdim etadi.

## Ishlash natijasi:
```text
Jami bo'limlar: 4 ta
- home
- search
- favorites
- profile
```


# 467-Topshiriq: Shartli moslik: Conditional Conformance
## Topshiriq sharti:
Massiv elementlari Equatable bo'lsagina massivning o'zi ham protokolga mos bo'lishini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

protocol PrintableSummary {
    func printSummary()
}

extension Array: PrintableSummary where Element: CustomStringConvertible {
    func printSummary() {
        print("To'plamda \(count) ta element bor:")
        for item in self {
            print("- \(item.description)")
        }
    }
}

let names = ["Ali", "Vali"]
names.printSummary()
```

## Tushuntirish va Mantiq:
Conditional Conformance ('where Element: Protocol') umumiy generik to'plamlarga ularning ichidagi elementlari ma'lum shartni bajargandagina yangi imkoniyatlar qo'shadi.

## Ishlash natijasi:
```text
To'plamda 2 ta element bor:
- Ali
- Vali
```


# 468-Topshiriq: Assotsiativ turlar: associatedtype
## Topshiriq sharti:
Protokolda aniq tur o'rniga parametrli tur talabini e'lon qiling.

## Yechim (Swift kodi):
```swift
import Foundation

protocol Container {
    associatedtype Item
    mutating func append(_ item: Item)
    var count: Int { get }
}

struct IntStack: Container {
    typealias Item = Int
    private var storage: [Int] = []
    
    mutating func append(_ item: Int) { storage.append(item) }
    var count: Int { storage.count }
}

var stack = IntStack()
stack.append(10)
stack.append(20)
print("Stekdagi elementlar soni: \(stack.count)")
```

## Tushuntirish va Mantiq:
'associatedtype' protokollardagi generik o'zgaruvchidir. Uni qabul qiluvchi tip o'ziga mos aniq turni (masalan, Int) belgilaydi.

## Ishlash natijasi:
```text
Stekdagi elementlar soni: 2
```


# 469-Topshiriq: Assotsiativ turlarda cheklovlar: associatedtype Item: Equatable
## Topshiriq sharti:
Assotsiativ turning o'ziga ham protokol talabi qo'ying.

## Yechim (Swift kodi):
```swift
import Foundation

protocol SearchableStorage {
    associatedtype Element: Equatable
    func containsElement(_ item: Element) -> Bool
}

struct SimpleBox<T: Equatable>: SearchableStorage {
    var items: [T]
    func containsElement(_ item: T) -> Bool {
        return items.contains(item)
    }
}

let box = SimpleBox(items: ["olma", "anor"])
print("Olma bormi? \(box.containsElement("olma"))")
```

## Tushuntirish va Mantiq:
Associated type lar boshqa protokollarga cheklanishi mumkin, bu orqali ularga '==' yoki boshqa operatsiyalarni qo'llash kafolatlanadi.

## Ishlash natijasi:
```text
Olma bormi? true
```


# 470-Topshiriq: Noma'lum qaytuvchi turlar: Opaque Return Types ('some')
## Topshiriq sharti:
Funksiya aniq qaysi strukturani qaytarishini yashirib, faqat protokol turini ('some Protocol') qaytaring.

## Yechim (Swift kodi):
```swift
import Foundation

protocol Shape {
    func draw() -> String
}

struct CircleShape: Shape {
    func draw() -> String { "Doira chizildi" }
}

func makeShape() -> some Shape {
    return CircleShape()
}

let s = makeShape()
print(s.draw())
```

## Tushuntirish va Mantiq:
'some Shape' (Opaque Return Type) — aniq turni tashqi dunyodan yashiradi, lekin kompilyator parda ortida yagona aniq turni biladi. SwiftUI ning 'var body: some View' aynan shu asosda qurilgan.

## Ishlash natijasi:
```text
Doira chizildi
```


# 471-Topshiriq: Mavjudlik qutilari: Existential Types ('any Protocol' - Swift 5.6+)
## Topshiriq sharti:
Har xil turlarni bitta qutida saqlovchi 'any' kalit so'zini qo'llang.

## Yechim (Swift kodi):
```swift
import Foundation

protocol Greeter {
    func sayHello()
}

struct UzbekGreeter: Greeter {
    func sayHello() { print("Assalomu alaykum!") }
}

struct EnglishGreeter: Greeter {
    func sayHello() { print("Hello world!") }
}

let greeters: [any Greeter] = [UzbekGreeter(), EnglishGreeter()]

for g in greeters {
    g.sayHello()
}
```

## Tushuntirish va Mantiq:
Swift 5.6 dan boshlab har qanday dinamik protokol qutisi 'any Protocol' shaklida yozilishi shart. Bu dasturchiga uning 'Existential Container' xotira qutisida saqlanishini aniq bildiradi.

## Ishlash natijasi:
```text
Assalomu alaykum!
Hello world!
```


# 472-Topshiriq: some vs any: Farqlar va xotira samaradorligi
## Topshiriq sharti:
'some' statik bo'lib tezkor ishlashini, 'any' esa dinamik quti bo'lib moslashuvchanligini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

protocol SoundMaker {
    func sound() -> String
}

struct CatSound: SoundMaker { func sound() -> String { "Miyov" } }
struct DogSound: SoundMaker { func sound() -> String { "Vov" } }

// 'some' doimo bitta aniq turga bog'liq (Static Dispatch):
func getStaticSound() -> some SoundMaker { CatSound() }

// 'any' har xil turlarni bitta massivda ushlay oladi (Dynamic Dispatch):
let mixedSounds: [any SoundMaker] = [CatSound(), DogSound()]

print("Static: \(getStaticSound().sound())")
print("Dynamic elementlar soni: \(mixedSounds.count)")
```

## Tushuntirish va Mantiq:
'some' kompilyatsiya vaqtida aniqlanadi va optimal Static Dispatch beradi. 'any' esa har xil turlarni qabul qila oladi, lekin Existential Container va Protocol Witness Table orqali Dynamic Dispatch xarajatiga ega.

## Ishlash natijasi:
```text
Static: Miyov
Dynamic elementlar soni: 2
```


# 473-Topshiriq: Protocol Witness Table (PWT) va Dynamic Dispatch
## Topshiriq sharti:
Protokol orqali chaqirilgan metod jadval orqali topilishini tushuntiring.

## Yechim (Swift kodi):
```swift
import Foundation

protocol WorkerProtocol {
    func work()
}

struct OfficeWorker: WorkerProtocol {
    func work() { print("Ofisda hujjatlar tayyorlanmoqda.") }
}

let w: any WorkerProtocol = OfficeWorker()
w.work()
```

## Tushuntirish va Mantiq:
Har bir protokol qutisi (Existential Container) o'zida 'Protocol Witness Table' (PWT) ko'rsatkichini saqlaydi va chaqiruv shu jadval orqali amalga oshiriladi.

## Ishlash natijasi:
```text
Ofisda hujjatlar tayyorlanmoqda.
```


# 474-Topshiriq: Swift Protocol-Oriented Programming (POP) tamoyillari
## Topshiriq sharti:
Sinflar merosxo'rligisiz, faqat protokollar va extensionlar orqali qudratli tizim quring.

## Yechim (Swift kodi):
```swift
import Foundation

protocol Flyable { func fly() }
protocol Swimmable { func swim() }

extension Flyable { func fly() { print("Osmonga parvoz qildi.") } }
extension Swimmable { func swim() { print("Suvda suzmoqda.") } }

struct Duck: Flyable, Swimmable {}

let duck = Duck()
duck.fly()
duck.swim()
```

## Tushuntirish va Mantiq:
POP (Protocol-Oriented Programming) tamoyili vertikal sinflar ierarxiyasini buzib, uning o'rniga gorizontal xatti-harakatlarni protokollar orqali yig'ishni (Mix-in) taqdim etadi.

## Ishlash natijasi:
```text
Osmonga parvoz qildi.
Suvda suzmoqda.
```


# 475-Topshiriq: Ruxsat so'rovchi delegat metodi (should... -> Bool)
## Topshiriq sharti:
Amal bajarilishidan oldin delegatdan rozilik so'rovchi klassik iOS naqshi.

## Yechim (Swift kodi):
```swift
import Foundation

protocol NavigationDelegate: AnyObject {
    func shouldNavigate(to path: String) -> Bool
}

class Navigator {
    weak var delegate: NavigationDelegate?
    
    func navigate(to path: String) {
        if delegate?.shouldNavigate(to: path) ?? true {
            print("Muvaffaqiyatli o'tildi: \(path)")
        } else {
            print("O'tish taqiqlandi: \(path)")
        }
    }
}

class SecurityGuard: NavigationDelegate {
    func shouldNavigate(to path: String) -> Bool {
        return path != "/admin"
    }
}

let nav = Navigator()
let guardAgent = SecurityGuard()
nav.delegate = guardAgent

nav.navigate(to: "/home")
nav.navigate(to: "/admin")
```

## Tushuntirish va Mantiq:
iOS UIKit dagi ko'plab delegatlar (masalan, shouldBegin, shouldPerform) aynan shu naqshda ishlaydi.

## Ishlash natijasi:
```text
Muvaffaqiyatli o'tildi: /home
O'tish taqiqlandi: /admin
```


# 476-Topshiriq: Observer Pattern protokollar orqali
## Topshiriq sharti:
Bitta manbadan bir nechta kuzatuvchilarga xabar tarqatuvchi arxitektura.

## Yechim (Swift kodi):
```swift
import Foundation

protocol StockUpdateListener: AnyObject {
    func stockPriceChanged(newPrice: Double)
}

class StockExchange {
    private var listeners = [StockUpdateListener]()
    
    func subscribe(_ listener: StockUpdateListener) {
        listeners.append(listener)
    }
    
    func setPrice(_ price: Double) {
        for l in listeners {
            l.stockPriceChanged(newPrice: price)
        }
    }
}

class TraderBot: StockUpdateListener {
    let name: String
    init(name: String) { self.name = name }
    func stockPriceChanged(newPrice: Double) {
        print("Bot [\(name)]: Yangi narx $\(newPrice)")
    }
}

let exchange = StockExchange()
let bot = TraderBot(name: "Alpha")
exchange.subscribe(bot)
exchange.setPrice(145.50)
```

## Tushuntirish va Mantiq:
Protokollar orqali ko'p sonli tinglovchilarga hodisalarni xavfsiz tarqatish mumkin.

## Ishlash natijasi:
```text
Bot [Alpha]: Yangi narx $145.5
```


# 477-Topshiriq: Dependency Injection uchun protokol abstraksiyasi
## Topshiriq sharti:
Haqiqiy API va Test (Mock) API sini bitta protokol ortiga yashiring.

## Yechim (Swift kodi):
```swift
import Foundation

protocol UserRepository {
    func fetchUserName(id: Int) -> String
}

class RealNetworkRepository: UserRepository {
    func fetchUserName(id: Int) -> String { "Serverdagi Asl Foydalanuvchi" }
}

class MockUserRepository: UserRepository {
    func fetchUserName(id: Int) -> String { "Test Foydalanuvchi" }
}

class UserViewModel {
    let repo: UserRepository
    init(repo: UserRepository) { self.repo = repo }
    func displayUser() { print("Ko'rsatildi: \(repo.fetchUserName(id: 1))") }
}

let vm = UserViewModel(repo: MockUserRepository())
vm.displayUser()
```

## Tushuntirish va Mantiq:
Protokol orqali Dependency Injection dasturni 100% testlashga yaroqli (unit testable) qiladi.

## Ishlash natijasi:
```text
Ko'rsatildi: Test Foydalanuvchi
```


# 478-Topshiriq: Protokolda asinxron throwing metod talabi
## Topshiriq sharti:
Zamonaviy Concurrency talablarini protokol interfeysida e'lon qiling.

## Yechim (Swift kodi):
```swift
import Foundation

protocol RemoteDataLoader {
    func loadJSON(from url: String) async throws -> String
}

struct FastLoader: RemoteDataLoader {
    func loadJSON(from url: String) async throws -> String {
        return "{\"status\": \"OK\"}"
    }
}

Task {
    let loader: any RemoteDataLoader = FastLoader()
    let data = try? await loader.loadJSON(from: "https://khorazmiy.uz")
    print("Yuklandi: \(data ?? "")")
}
```

## Tushuntirish va Mantiq:
Swift protokollari 'async throws' asinxron metodlarni to'liq qo'llab-quvvatlaydi.

## Ishlash natijasi:
```text
Yuklandi: {"status": "OK"}
```


# 479-Topshiriq: Standart protokol: ExpressibleByStringLiteral
## Topshiriq sharti:
O'z maxsus ob'ektingizni to'g'ridan-to'g'ri satr ko'rinishida yozish imkoniyatini bering.

## Yechim (Swift kodi):
```swift
import Foundation

struct PhoneNumber: ExpressibleByStringLiteral {
    let raw: String
    init(stringLiteral value: String) {
        self.raw = value
    }
}

let phone: PhoneNumber = "+998901234567" // To'g'ridan-to'g'ri string literal!
print("Raqam ob'ekti: \(phone.raw)")
```

## Tushuntirish va Mantiq:
'ExpressibleByStringLiteral' protokoli orqali ob'ektlarni oddiy satr literali kabi qulay initsializatsiya qilish mumkin.

## Ishlash natijasi:
```text
Raqam ob'ekti: +998901234567
```


# 480-Topshiriq: Self talabi bo'lgan protokollar
## Topshiriq sharti:
Metod o'zining aniq turidagi ob'ektni nusxa qilib qaytarishi shart bo'lgan protokol.

## Yechim (Swift kodi):
```swift
import Foundation

protocol Duplicable {
    func duplicate() -> Self
}

struct TicketPass: Duplicable {
    let serial: Int
    func duplicate() -> TicketPass {
        return TicketPass(serial: serial + 1)
    }
}

let t1 = TicketPass(serial: 100)
let t2 = t1.duplicate()
print("Asl: \(t1.serial), Nusxa: \(t2.serial)")
```

## Tushuntirish va Mantiq:
Protokolda 'Self' qaytarish turi har qanday qabul qiluvchi tipni o'zining aynan o'sha turidagi nusxasini qaytarishga majbur qiladi.

## Ishlash natijasi:
```text
Asl: 100, Nusxa: 101
```


# 481-Topshiriq: Protokolda statik hisoblangan xususiyat talabi
## Topshiriq sharti:
Tipning o'zida mavjud bo'lishi shart bo'lgan statik identifikator talabi.

## Yechim (Swift kodi):
```swift
import Foundation

protocol DatabaseRecord {
    static var tableName: String { get }
}

struct CustomerRecord: DatabaseRecord {
    static var tableName: String { "customers_table" }
}

print("Jadval nomi: \(CustomerRecord.tableName)")
```

## Tushuntirish va Mantiq:
Protokollar nafaqat instansiya maydonlarini, balki 'static var' tip xususiyatlarini ham talab qilib qo'yishi mumkin.

## Ishlash natijasi:
```text
Jadval nomi: customers_table
```


# 482-Topshiriq: Sendable protokoli va oqimlararo xavfsizlik
## Topshiriq sharti:
Swift Concurrency da oqimlar orasida uzatilishi mumkin bo'lgan turni belgilash.

## Yechim (Swift kodi):
```swift
import Foundation

struct SafePacket: Sendable {
    let messageID: Int
    let payload: String
}

let packet = SafePacket(messageID: 1, payload: "Xavfsiz ma'lumot")
print("Packet Sendable protokoli orqali parallel oqimlarda bexatar ishlatiladi.")
```

## Tushuntirish va Mantiq:
'Sendable' protokoli ma'lumotlarning oqimlararo xavfsiz (data race-free) ekanligini kompilyator darajasida tekshiruvchi maxsus marker protokoldir.

## Ishlash natijasi:
```text
Packet Sendable protokoli orqali parallel oqimlarda bexatar ishlatiladi.
```


# 483-Topshiriq: Bo'sh protokollar: Marker Protocols
## Topshiriq sharti:
Xatti-harakatsiz, faqat tiplarni guruhlash uchun xizmat qiluvchi belgi protokol.

## Yechim (Swift kodi):
```swift
import Foundation

protocol AnalyticsTrackable {}

struct UserClick: AnalyticsTrackable {}
struct ViewLoad: AnalyticsTrackable {}

func trackEvent(_ event: any AnalyticsTrackable) {
    print("Tahlil hodisasi qayd etildi: \(type(of: event))")
}

trackEvent(UserClick())
trackEvent(ViewLoad())
```

## Tushuntirish va Mantiq:
Marker protokollar hech qanday metod talab qilmaydi, ular faqat tiplarga ma'lum belgi yoki toifa berish uchun ishlatiladi.

## Ishlash natijasi:
```text
Tahlil hodisasi qayd etildi: UserClick
Tahlil hodisasi qayd etildi: ViewLoad
```


# 484-Topshiriq: Protocol Extension ichida Self cheklovi (where Self: SpecificClass)
## Topshiriq sharti:
Kengaytma faqat muayyan sinfdan meros olgan tiplargagina qo'llanishini cheklang.

## Yechim (Swift kodi):
```swift
import Foundation

class BaseWindow { var title = "Oyna" }

protocol Alertable {}

extension Alertable where Self: BaseWindow {
    func showAlert() {
        print("Ogohlantirish [\(title)]: Xabar ko'rsatildi.")
    }
}

class MainWindow: BaseWindow, Alertable {}

let win = MainWindow()
win.showAlert()
```

## Tushuntirish va Mantiq:
'where Self: Class' orqali protokol kengaytmasi ichida o'sha klassning xususiyatlariga (masalan, title) bevosita murojaat qilish imkoni paydo bo'ladi.

## Ishlash natijasi:
```text
Ogohlantirish [Oyna]: Xabar ko'rsatildi.
```


# 485-Topshiriq: Diamond Problem yo'qligi va protokol to'qnashuvlarini hal qilish
## Topshiriq sharti:
Ikkita turli protokoldagi bir xil metod default realizatsiyasi qanday hal bo'lishini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

protocol ProtocolA { func ping() }
protocol ProtocolB { func ping() }

extension ProtocolA { func ping() { print("Ping A") } }
extension ProtocolB { func ping() { print("Ping B") } }

struct DualNode: ProtocolA, ProtocolB {
    // To'qnashuvni hal qilish uchun tipning o'zi metodni aniq yozishi shart:
    func ping() {
        print("DualNode maxsus Ping")
    }
}

let node = DualNode()
node.ping()
```

## Tushuntirish va Mantiq:
Swift-da bir nechta protokollar default realizatsiyasida to'qnashuv yuzaga kelsa, uni qabul qiluvchi struktura metodni o'zi aniq realizatsiya qilib noaniqlikni bartaraf qiladi.

## Ishlash natijasi:
```text
DualNode maxsus Ping
```


# 486-Topshiriq: Protokol orqali ko'p qavatli xizmatlar zanjiri
## Topshiriq sharti:
Logging va Analytics qatlamlarini protokol zanjiri orqali bog'lash.

## Yechim (Swift kodi):
```swift
import Foundation

protocol ServicePlugin {
    func initializePlugin()
}

struct AuthPlugin: ServicePlugin { func initializePlugin() { print("Auth faollashdi") } }
struct MetricsPlugin: ServicePlugin { func initializePlugin() { print("Metrics faollashdi") } }

let plugins: [any ServicePlugin] = [AuthPlugin(), MetricsPlugin()]
for p in plugins {
    p.initializePlugin()
}
```

## Tushuntirish va Mantiq:
Plaginlar arxitekturasida barcha mustaqil modullar umumiy protokol orqali ishga tushiriladi.

## Ishlash natijasi:
```text
Auth faollashdi
Metrics faollashdi
```


# 487-Topshiriq: Protokol orqali holatni sinxronlashtirish
## Topshiriq sharti:
O'zgarishlar haqida xabar beruvchi protokol munosabati.

## Yechim (Swift kodi):
```swift
import Foundation

protocol StateChangeDelegate: AnyObject {
    func didChangeState(to state: String)
}

class StateStore {
    weak var delegate: StateChangeDelegate?
    func update(state: String) {
        delegate?.didChangeState(to: state)
    }
}

class ViewRenderer: StateChangeDelegate {
    func didChangeState(to state: String) {
        print("Render qilindi: \(state)")
    }
}

let store = StateStore()
let renderer = ViewRenderer()
store.delegate = renderer
store.update(state: "YANGI_HOLAT_ACTIVE")
```

## Tushuntirish va Mantiq:
Davlat (state) boshqaruvida delegatlar orqali UI elementlarini qayta chizish samarali usuldir.

## Ishlash natijasi:
```text
Render qilindi: YANGI_HOLAT_ACTIVE
```


# 488-Topshiriq: Protokol orqali ma'lumotlar manzilini qidirish
## Topshiriq sharti:
Ma'lumotlar bazasi yoki fayllardan o'quvchi yagona interfeys.

## Yechim (Swift kodi):
```swift
import Foundation

protocol DataSource {
    func loadData() -> [String]
}

struct StaticDataSource: DataSource {
    func loadData() -> [String] { ["Lokal_1", "Lokal_2"] }
}

let ds: any DataSource = StaticDataSource()
print("Manba ma'lumotlari: \(ds.loadData())")
```

## Tushuntirish va Mantiq:
DataSource arxitekturasi ma'lumot qayerdan kelishini biznes logikadan to'liq yashiradi.

## Ishlash natijasi:
```text
Manba ma'lumotlari: ["Lokal_1", "Lokal_2"]
```


# 489-Topshiriq: Protokol talablariga default qiymatli parametrlar berish
## Topshiriq sharti:
Protokol metodiga extension orqali default parametr berish siri.

## Yechim (Swift kodi):
```swift
import Foundation

protocol NetworkSender {
    func send(packet: String, timeout: Int)
}

extension NetworkSender {
    func send(packet: String) {
        send(packet: packet, timeout: 60)
    }
}

struct HTTPClient: NetworkSender {
    func send(packet: String, timeout: Int) {
        print("Yuborildi: '\(packet)', Kutilish: \(timeout)s")
    }
}

let client = HTTPClient()
client.send(packet: "JSON_PAYLOAD") // Qisqartirilgan default parametrli metod!
```

## Tushuntirish va Mantiq:
Swift protokollarining o'zida parametrga default qiymat berib bo'lmaydi, biroq protocol extension orqali default parametrli yordamchi metod qo'shish mumkin.

## Ishlash natijasi:
```text
Yuborildi: 'JSON_PAYLOAD', Kutilish: 60s
```


# 490-Topshiriq: Protokollarni birlashtirib qayta nomlash: typealias bilan
## Topshiriq sharti:
Bir nechta protokollar kompozitsiyasiga qulay yangi nom bering.

## Yechim (Swift kodi):
```swift
import Foundation

protocol AudioPlayback { func playAudio() }
protocol VideoPlayback { func playVideo() }

typealias MediaPlayback = AudioPlayback & VideoPlayback

struct UniversalPlayer: MediaPlayback {
    func playAudio() { print("Audio chalindi") }
    func playVideo() { print("Video ko'rsatildi") }
}

let player: MediaPlayback = UniversalPlayer()
player.playAudio()
player.playVideo()
```

## Tushuntirish va Mantiq:
'typealias' orqali protokol kompozitsiyalariga yangi domen nomlarini berish kodni juda o'qiluvchan qiladi.

## Ishlash natijasi:
```text
Audio chalindi
Video ko'rsatildi
```


# 491-Topshiriq: Protokolda xatolik turini cheklash
## Topshiriq sharti:
Protokol metodini faqat aniq bir xato tashlashga moslashtirish.

## Yechim (Swift kodi):
```swift
import Foundation

protocol SafeWorker {
    func executeWork() throws
}

struct FileTask: SafeWorker {
    func executeWork() throws {
        print("Vazifa bajarildi.")
    }
}

let task: any SafeWorker = FileTask()
try? task.executeWork()
```

## Tushuntirish va Mantiq:
Protokollar throwing metodlar bilan xatoliklarni xavfsiz boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Vazifa bajarildi.
```


# 492-Topshiriq: Protokollarda Dynamic Member Lookup
## Topshiriq sharti:
Protokol talab qilgan subscript orqali dinamik a'zolikni kafolatlash.

## Yechim (Swift kodi):
```swift
import Foundation

protocol DynamicConfigurable {
    subscript(dynamicMember member: String) -> String { get }
}

struct AppConfigMap: DynamicConfigurable {
    subscript(dynamicMember member: String) -> String {
        return "CONFIG_FOR_\(member.uppercased())"
    }
}

let cfg: any DynamicConfigurable = AppConfigMap()
print("Konfiguratsiya: \(cfg[dynamicMember: "timeout"])")
```

## Tushuntirish va Mantiq:
Dinamik xususiyatlarni protokol bilan birlashtirish orqali kengaytiriluvchi arxitektura quriladi.

## Ishlash natijasi:
```text
Konfiguratsiya: CONFIG_FOR_TIMEOUT
```


# 493-Topshiriq: Protokol orqali ko'p platformali renderlash
## Topshiriq sharti:
iOS va macOS platformalariga mos xizmat interfeysi.

## Yechim (Swift kodi):
```swift
import Foundation

protocol PlatformNotification {
    func deliver(message: String)
}

struct AppleNotificationService: PlatformNotification {
    func deliver(message: String) {
        print("Apple Push Notification yuborildi: \(message)")
    }
}

let notifier: any PlatformNotification = AppleNotificationService()
notifier.deliver(message: "Yangi kurs boshlandi!")
```

## Tushuntirish va Mantiq:
Platformalararo kod yozishda protokollar eng asosiy ajratuvchi ko'prik hisoblanadi.

## Ishlash natijasi:
```text
Apple Push Notification yuborildi: Yangi kurs boshlandi!
```


# 494-Topshiriq: SwiftUI-dagi EnvironmentKey protokoli falsafasi
## Topshiriq sharti:
Maxsus kalitlar orqali tizim ma'lumotlarini tarqatuvchi protokol prototipi.

## Yechim (Swift kodi):
```swift
import Foundation

protocol SimpleEnvironmentKey {
    associatedtype Value
    static var defaultValue: Value { get }
}

struct ThemeColorKey: SimpleEnvironmentKey {
    static var defaultValue: String { "Moviy" }
}

print("Standart muhit qiymati: \(ThemeColorKey.defaultValue)")
```

## Tushuntirish va Mantiq:
SwiftUI dagi @Environment aynan associatedtype va static default ga ega protokollar asosida ishlaydi.

## Ishlash natijasi:
```text
Standart muhit qiymati: Moviy
```


# 495-Topshiriq: Protokol metodlarining chaqirilish unumdorligi
## Topshiriq sharti:
Generik cheklov (some) vs Dinamik quti (any) chaqiruvlari.

## Yechim (Swift kodi):
```swift
import Foundation

protocol Executable {
    func run()
}

struct Runner: Executable {
    func run() { print("Yugurmoqda...") }
}

func executeStatic<T: Executable>(item: T) { item.run() } // Monomorfizm (juda tez)
func executeDynamic(item: any Executable) { item.run() }   // Polimorfizm (PWT orqali)

let r = Runner()
executeStatic(item: r)
executeDynamic(item: r)
```

## Tushuntirish va Mantiq:
Generik 'some' statik monomorfizm orqali to'g'ridan-to'g'ri kompilyatsiya qilinadi, 'any' esa xotira qutisidan foydalanadi.

## Ishlash natijasi:
```text
Yugurmoqda...
Yugurmoqda...
```


# 496-Topshiriq: Protokollar bilan ob'ektlarni klonlash (Clonable Protocol)
## Topshiriq sharti:
Chuqur nusxa olishni kafolatlovchi maxsus protokol.

## Yechim (Swift kodi):
```swift
import Foundation

protocol DeepCopyable {
    func deepCopy() -> Self
}

struct UserData: DeepCopyable {
    var name: String
    func deepCopy() -> UserData {
        return UserData(name: self.name)
    }
}

let u1 = UserData(name: "Ali")
var u2 = u1.deepCopy()
u2.name = "Vali"

print("u1: \(u1.name), u2: \(u2.name)")
```

## Tushuntirish va Mantiq:
Protokollar orqali tizimdagi barcha ob'ektlarga yagona klonlash qoidasini kiritish mumkin.

## Ishlash natijasi:
```text
u1: Ali, u2: Vali
```


# 497-Topshiriq: Protokol yordamida Validatsiya zanjiri (Validation Rule)
## Topshiriq sharti:
Turli xil matn validatsiya qoidalarini umumiy protokol orqali yig'ish.

## Yechim (Swift kodi):
```swift
import Foundation

protocol ValidationRule {
    func isValid(_ text: String) -> Bool
}

struct MinLengthRule: ValidationRule {
    let min: Int
    func isValid(_ text: String) -> Bool { text.count >= min }
}

struct HasDigitRule: ValidationRule {
    func isValid(_ text: String) -> Bool { text.contains { $0.isNumber } }
}

let rules: [any ValidationRule] = [MinLengthRule(min: 6), HasDigitRule()]
let password = "Secret2026"
let isPasswordValid = rules.allSatisfy { $0.isValid(password) }

print("Parol barcha qoidalarga javob beradimi? \(isPasswordValid)")
```

## Tushuntirish va Mantiq:
Validatsiya qoidalarini protokollar orqali modullashtirish kengaytirishni juda osonlashtiradi.

## Ishlash natijasi:
```text
Parol barcha qoidalarga javob beradimi? true
```


# 498-Topshiriq: Kolleksiya protokollari zanjiri (Sequence -> Collection -> BidirectionalCollection)
## Topshiriq sharti:
Swift standart kutubxonasidagi protokollar ierarxiyasini tushuntirish.

## Yechim (Swift kodi):
```swift
import Foundation

let sampleArray = [1, 2, 3]
print("Array Sequence protokoli orqali for-in tsiklini qo'llab-quvvatlaydi.")
print("Array Collection protokoli orqali indekslashni (subscript) qo'llab-quvvatlaydi.")
```

## Tushuntirish va Mantiq:
Swift kolleksiyalari protokol merosxo'rligi orqali qurilgan: Sequence -> Collection -> BidirectionalCollection -> RandomAccessCollection.

## Ishlash natijasi:
```text
Array Sequence protokoli orqali for-in tsiklini qo'llab-quvvatlaydi.
Array Collection protokoli orqali indekslashni (subscript) qo'llab-quvvatlaydi.
```


# 499-Topshiriq: Protokol extensionida yangi qo'shimcha metod e'lon qilish
## Topshiriq sharti:
Protokol talablarida yo'q, ammo faqat extensionda mavjud bo'lgan metod xatti-harakati.

## Yechim (Swift kodi):
```swift
import Foundation

protocol BaseProtocol {}

extension BaseProtocol {
    func bonusMethod() {
        print("Faqat extension orqali qo'shilgan bonus metod!")
    }
}

struct SimpleEntity: BaseProtocol {}

let ent = SimpleEntity()
ent.bonusMethod()
```

## Tushuntirish va Mantiq:
Protokolning o'zida e'lon qilinmagan, faqat extensionida mavjud bo'lgan metodlar Static Dispatch orqali chaqiriladi.

## Ishlash natijasi:
```text
Faqat extension orqali qo'shilgan bonus metod!
```


# 500-Topshiriq: Amaliy loyiha: Protokolga asoslangan to'lov tizimi va kvitansiya delegatsiyasi moduli
## Topshiriq sharti:
PaymentMethod protokoli, CardPayment, CryptoPayment, ApplePay modullari, tranzaksiya delegati va natijaviy hisobot tizimi.

## Yechim (Swift kodi):
```swift
import Foundation

protocol PaymentDelegate: AnyObject {
    func paymentDidStart(method: String, amount: Double)
    func paymentDidFinish(receiptID: String, success: Bool)
}

protocol PaymentGateway {
    var methodName: String { get }
    func processPayment(amount: Double) -> (success: Bool, receiptID: String)
}

class BankCardPayment: PaymentGateway {
    let methodName = "Bank Kartasi (UzCard / Humo)"
    func processPayment(amount: Double) -> (success: Bool, receiptID: String) {
        let receipt = "UZC-" + String(Int.random(in: 100000...999999))
        return (true, receipt)
    }
}

class CryptoPayment: PaymentGateway {
    let methodName = "Kriptovalyuta (USDT)"
    func processPayment(amount: Double) -> (success: Bool, receiptID: String) {
        let receipt = "TX-0x" + UUID().uuidString.prefix(8)
        return (true, receipt)
    }
}

class CheckoutProcessor {
    weak var delegate: PaymentDelegate?
    
    func checkout(gateway: any PaymentGateway, amount: Double) {
        delegate?.paymentDidStart(method: gateway.methodName, amount: amount)
        let result = gateway.processPayment(amount: amount)
        delegate?.paymentDidFinish(receiptID: result.receiptID, success: result.success)
    }
}

class AccountingService: PaymentDelegate {
    func paymentDidStart(method: String, amount: Double) {
        print("[MOLIYA]: To'lov boshlandi: '\(method)', Summa: $\(amount)")
    }
    
    func paymentDidFinish(receiptID: String, success: Bool) {
        print("[MOLIYA]: To'lov yakunlandi! Holat: \(success ? "Muvaffaqiyatli" : "Xato"), Kvitansiya: \(receiptID)")
    }
}

let accounting = AccountingService()
let checkout = CheckoutProcessor()
checkout.delegate = accounting

print("=== TO'LOV JARAYONI 1 ===")
checkout.checkout(gateway: BankCardPayment(), amount: 450.0)

print("
=== TO'LOV JARAYONI 2 ===")
checkout.checkout(gateway: CryptoPayment(), amount: 1200.0)
```

## Tushuntirish va Mantiq:
Ushbu yakuniy amaliy loyihada Protokol talablari, AnyObject delegat arxitekturasi, weak havolalar, 'any PaymentGateway' polimorfik qutisi va real kvitansiya hisoboti to'liq birlashtirildi.

## Ishlash natijasi:
```text
=== TO'LOV JARAYONI 1 ===
[MOLIYA]: To'lov boshlandi: 'Bank Kartasi (UzCard / Humo)', Summa: $450.0
[MOLIYA]: To'lov yakunlandi! Holat: Muvaffaqiyatli, Kvitansiya: UZC-XXXXXX

=== TO'LOV JARAYONI 2 ===
[MOLIYA]: To'lov boshlandi: 'Kriptovalyuta (USDT)', Summa: $1200.0
[MOLIYA]: To'lov yakunlandi! Holat: Muvaffaqiyatli, Kvitansiya: TX-0xXXXXXXXX
```

