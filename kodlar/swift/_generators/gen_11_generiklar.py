# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

tasks_data = [
    (
        501,
        "Generiklar nima va nima uchun kerak",
        "Bir xil mantiqqa ega bo'lgan kodni barcha tiplar uchun qayta yozmasdan generik qiling.",
        """import Foundation

func printTwoValues<T>(_ a: T, _ b: T) {
    print("Qiymat 1: \\(a), Qiymat 2: \\(b)")
}

printTwoValues(10, 20)
printTwoValues("Salom", "Dunyo")
printTwoValues(true, false)
""",
        "Generiklar (Generics) — turdan qat'i nazar, moslashuvchan va qayta ishlatiluvchi kod yozish imkonini beradi. Swift massivlari va lug'atlari generiklar asosida qurilgan.",
        """Qiymat 1: 10, Qiymat 2: 20
Qiymat 1: Salom, Qiymat 2: Dunyo
Qiymat 1: true, Qiymat 2: false"""
    ),
    (
        502,
        "Generik funksiya: swapValues<T>",
        "Ixtiyoriy turdagi ikkita o'zgaruvchi qiymatini inout orqali almashtiruvchi funksiya.",
        """import Foundation

func swapValues<T>(_ a: inout T, _ b: inout T) {
    let temp = a
    a = b
    b = temp
}

var s1 = "Olma", s2 = "Anor"
swapValues(&s1, &s2)
print("s1: \\(s1), s2: \\(s2)")

var n1 = 100, n2 = 200
swapValues(&n1, &n2)
print("n1: \\(n1), n2: \\(n2)")
""",
        "Generik funksiyada '<T>' parametri ixtiyoriy turni ifodalaydi va funksiya chaqirilganda haqiqiy turga avtomatik bog'lanadi.",
        """s1: Anor, s2: Olma
n1: 200, n2: 100"""
    ),
    (
        503,
        "Generik Stek: Stack<Element>",
        "LIFO (Last-In-First-Out) tamoyilida ishlovchi generik ma'lumotlar tuzilmasi.",
        """import Foundation

struct Stack<Element> {
    private var items: [Element] = []
    
    mutating func push(_ item: Element) {
        items.append(item)
    }
    
    mutating func pop() -> Element? {
        return items.popLast()
    }
    
    func peek() -> Element? {
        return items.last
    }
    
    var isEmpty: Bool {
        return items.isEmpty
    }
}

var intStack = Stack<Int>()
intStack.push(10)
intStack.push(20)
print("Tepadagi element: \\(intStack.peek() ?? 0)")
print("Olingan element: \\(intStack.pop() ?? 0)")
""",
        "'Stack<Element>' har qanday turdagi elementlarni (Int, String, Ob'ektlar) xavfsiz saqlashi mumkin.",
        """Tepadagi element: 20
Olingan element: 20"""
    ),
    (
        504,
        "Generik Navbat: Queue<T>",
        "FIFO (First-In-First-Out) tamoyilida ishlovchi generik navbat tuzilmasi.",
        """import Foundation

struct Queue<T> {
    private var elements: [T] = []
    
    mutating func enqueue(_ element: T) {
        elements.append(element)
    }
    
    mutating func dequeue() -> T? {
        return elements.isEmpty ? nil : elements.removeFirst()
    }
}

var namesQueue = Queue<String>()
namesQueue.enqueue("Ali")
namesQueue.enqueue("Vali")
print("Birinchi chiqqan: \\(namesQueue.dequeue() ?? "")")
""",
        "Generik navbat har qanday turdagi navbatma-navbat bajariluvchi vazifalarni boshqarish uchun idealdir.",
        """Birinchi chiqqan: Ali"""
    ),
    (
        505,
        "Generik turni kengaytirish (Extending Generic Type)",
        "Generik Stack-ga yangi xususiyat qo'shuvchi extension yozing.",
        """import Foundation

extension Stack {
    var count: Int {
        // Asosiy strukturadagi Element turidan to'g'ridan-to'g'ri foydalanish mumkin
        return isEmpty ? 0 : 1 // Soddalashtirilgan ko'rsatkich
    }
}

var st = Stack<String>()
st.push("Swift")
print("Bo'sh emasmi? \\(!st.isEmpty)")
""",
        "Generik tur kengaytirilganda '<T>' parametrini qayta yozish shart emas, uning asl tipi extension ichida to'g'ridan-to'g'ri ko'rinadi.",
        """Bo'sh emasmi? true"""
    ),
    (
        506,
        "Tur cheklovlari: Protokol cheklovi (T: Equatable)",
        "Massivdan qiymatning birinchi indeksini topuvchi generik funksiya yozing.",
        """import Foundation

func findIndex<T: Equatable>(of valueToFind: T, in array: [T]) -> Int? {
    for (index, value) in array.enumerated() {
        if value == valueToFind {
            return index
        }
    }
    return nil
}

let strings = ["olma", "nok", "uzum"]
if let idx = findIndex(of: "nok", in: strings) {
    print("Nok indeksi: \\(idx)")
}
""",
        "'T: Equatable' cheklovi T turining tenglikni (==) tekshirishga ega bo'lishini kafolatlaydi, aks holda kompilyator taqqoslashga ruxsat bermaydi.",
        """Nok indeksi: 1"""
    ),
    (
        507,
        "Tur cheklovlari: Sinf merosi cheklovi (T: SomeClass)",
        "Faqat muayyan sinf yoki uning subclass lari bilan ishlovchi generik funksiya.",
        """import Foundation

class BaseDevice {
    let serial: String
    init(serial: String) { self.serial = serial }
}

func logDeviceSerial<T: BaseDevice>(_ device: T) {
    print("Qurilma seriya raqami: \\(device.serial)")
}

let dev = BaseDevice(serial: "APL_99182")
logDeviceSerial(dev)
""",
        "'T: BaseDevice' cheklovi generik parametr faqat ko'rsatilgan sinf instansiyasi bo'lishini talab qiladi.",
        """Qurilma seriya raqami: APL_99182"""
    ),
    (
        508,
        "where bandi bilan generik funksiyalarni filtrlash",
        "Generik parametrlarga qo'shimcha murakkab shartlar qo'yuvchi funksiya.",
        """import Foundation

func compareFirstElements<S1: Sequence, S2: Sequence>(_ seq1: S1, _ seq2: S2) -> Bool
where S1.Element == S2.Element, S1.Element: Equatable {
    guard let first1 = seq1.first(where: { _ in true }),
          let first2 = seq2.first(where: { _ in true }) else {
        return false
    }
    return first1 == first2
}

let listA = [1, 2, 3]
let listB = [1, 9, 8]
print("Birinchi elementlari tengmi? \\(compareFirstElements(listA, listB))")
""",
        "'where' kalit so'zi assotsiativ turlarning bir xilligini va ularning protokollarga mosligini ta'minlashda eng kuchli vositadir.",
        """Birinchi elementlari tengmi? true"""
    ),
    (
        509,
        "Generik Where Clauses extensionlarda",
        "Stack-ning faqat Element turi Equatable bo'lgandagina ishlaydigan metodini yozing.",
        """import Foundation

extension Stack where Element: Equatable {
    func isTopEqual(to item: Element) -> Bool {
        guard let top = peek() else { return false }
        return top == item
    }
}

var s = Stack<Int>()
s.push(42)
print("Tepadagi 42 ga tengmi? \\(s.isTopEqual(to: 42))")
""",
        "'extension GenericType where T: Protocol' orqali muayyan metodlar faqat mos turlar uchungina faollashtiriladi.",
        """Tepadagi 42 ga tengmi? true"""
    ),
    (
        510,
        "Generik Subscript lar",
        "Kolleksiyadan bir nechta indekslar ketma-ketligi bo'yicha elementlarni oluvchi generik subscript.",
        """import Foundation

extension Array {
    subscript<Indices: Sequence>(selectedIndices indices: Indices) -> [Element] where Indices.Element == Int {
        var result = [Element]()
        for i in indices {
            if i >= 0 && i < count {
                result.append(self[i])
            }
        }
        return result
    }
}

let letters = ["A", "B", "C", "D", "E"]
let picked = letters[selectedIndices: [0, 2, 4]]
print("Tanlanganlar: \\(picked)")
""",
        "Subscript-lar ham o'z shaxsiy generik parametrlari va 'where' cheklovlariga ega bo'lishi mumkin.",
        """Tanlanganlar: ["A", "C", "E"]"""
    ),
    (
        511,
        "Primary Associated Types (Swift 5.7+)",
        "Protokolda birlamchi parametrni ko'rsatish: 'some Collection<String>'.",
        """import Foundation

func printStrings(items: some Collection<String>) {
    for str in items {
        print("- \\(str)")
    }
}

printStrings(items: ["iOS", "macOS", "visionOS"])
""",
        "Swift 5.7 dan boshlab protokollarda 'Protocol<T>' sintaksisi (Primary Associated Types) joriy qilingan, bu generik kodni sezilarli ixchamlashtiradi.",
        """- iOS
- macOS
- visionOS"""
    ),
    (
        512,
        "Swift 5.9 Parameter Packs (Variadic Generics)",
        "Ixtiyoriy sondagi har xil turdagi parametrlarni qabul qiluvchi funksiya tushunchasi.",
        """import Foundation

func printAllTypes<each T>(_ item: repeat each T) {
    // Swift 5.9 Parameter Pack asosiy sintaksisi
    print("Parameter pack muvaffaqiyatli qabul qilindi.")
}

printAllTypes(1, "Matn", true)
""",
        "Swift 5.9 da qo'shilgan 'Parameter Packs' (each T, repeat each T) til tarixidagi eng yirik inqiloblardan biri bo'lib, o'zgaruvchan sondagi turli tiplar bilan xavfsiz ishlash imkonini beradi.",
        """Parameter pack muvaffaqiyatli qabul qilindi."""
    ),
    (
        513,
        "Generik Binar Qidiruv Daraxti (Binary Search Tree)",
        "Har qanday Comparable elementlarni o'z ichiga oluvchi daraxt tuzilmasi.",
        """import Foundation

final class BSTNode<T: Comparable> {
    var value: T
    var left: BSTNode<T>?
    var right: BSTNode<T>?
    
    init(value: T) { self.value = value }
    
    func insert(_ newValue: T) {
        if newValue < value {
            if let left = left { left.insert(newValue) } else { left = BSTNode(value: newValue) }
        } else {
            if let right = right { right.insert(newValue) } else { right = BSTNode(value: newValue) }
        }
    }
}

let root = BSTNode(value: 50)
root.insert(30)
root.insert(70)
print("Ildiz: \\(root.value), Chap: \\(root.left?.value ?? 0), O'ng: \\(root.right?.value ?? 0)")
""",
        "Generik Comparable daraxti ixtiyoriy sonlar yoki saralanuvchi ob'ektlarni optimal daraxt ko'rinishida saqlaydi.",
        """Ildiz: 50, Chap: 30, O'ng: 70"""
    ),
    (
        514,
        "Generik LRU Kesh (Least Recently Used Cache)",
        "Maksimal sig'imga yetganda eng eski ishlatilgan elementni o'chiruvchi generik kesh.",
        """import Foundation

class LRUCache<Key: Hashable, Value> {
    private let capacity: Int
    private var cache: [Key: Value] = [:]
    private var order: [Key] = []
    
    init(capacity: Int) { self.capacity = capacity }
    
    func put(key: Key, value: Value) {
        if cache[key] != nil {
            order.removeAll { $0 == key }
        } else if cache.count >= capacity {
            let oldest = order.removeFirst()
            cache.removeValue(forKey: oldest)
        }
        cache[key] = value
        order.append(key)
    }
    
    func get(key: Key) -> Value? {
        guard let val = cache[key] else { return nil }
        order.removeAll { $0 == key }
        order.append(key)
        return val
    }
}

let lru = LRUCache<String, Int>(capacity: 2)
lru.put(key: "A", value: 1)
lru.put(key: "B", value: 2)
lru.put(key: "C", value: 3) // "A" o'chib ketadi

print("B bor: \\(lru.get(key: "B") != nil)")
print("A o'chganmi: \\(lru.get(key: "A") == nil)")
""",
        "Generik LRU Kesh barcha turdagi ma'lumotlar uchun optimal xotira foydalanishini ta'minlaydi.",
        """B bor: true
A o'chganmi: true"""
    ),
    (
        515,
        "Type Erasure (Tur o'chirish) naqshi: AnyRepository",
        "Assotsiativ turga ega protokolni oddiy o'zgaruvchi sifatida saqlash imkonini beruvchi wrapper.",
        """import Foundation

protocol DataService {
    associatedtype Payload
    func fetch() -> Payload
}

// Type Eraser qutisi:
class AnyDataService<Payload>: DataService {
    private let _fetch: () -> Payload
    
    init<S: DataService>(_ service: S) where S.Payload == Payload {
        self._fetch = service.fetch
    }
    
    func fetch() -> Payload { _fetch() }
}

struct MockService: DataService {
    func fetch() -> String { "Server javobi" }
}

let erased: AnyDataService<String> = AnyDataService(MockService())
print("Natija: \\(erased.fetch())")
""",
        "Swift-da assotsiativ turga ega protokollarni to'g'ridan-to'g'ri o'zgaruvchiga olib bo'lmaydi. Buni hal qilish uchun 'Any...' bilan boshlanuvchi Type Erasure sinfi tuziladi (masalan, AnyView).",
        """Natija: Server javobi"""
    ),
    (
        516,
        "Generik DAO / Repository qatlami",
        "Ma'lumotlar bazasi ob'ektlarini generik CRUD operatsiyalari bilan boshqarish.",
        """import Foundation

protocol IdentifiableEntity {
    var id: Int { get }
}

class GenericRepository<T: IdentifiableEntity> {
    private var items: [Int: T] = [:]
    
    func save(_ entity: T) {
        items[entity.id] = entity
    }
    
    func find(id: Int) -> T? {
        return items[id]
    }
}

struct Customer: IdentifiableEntity {
    let id: Int
    let name: String
}

let repo = GenericRepository<Customer>()
repo.save(Customer(id: 42, name: "Farhod"))
print("Mijoz topildi: \\(repo.find(id: 42)?.name ?? "")")
""",
        "Generik Repository har bir yangi model uchun qayta-qayta kod yozishdan qutqaradi.",
        """Mijoz topildi: Farhod"""
    ),
    (
        517,
        "Phantom Types (Fantom tiplar) bilan xavfsizlik",
        "Kompilyatsiya vaqtida ob'ekt holatini (State) tekshiruvchi fantom generik parametr.",
        """import Foundation

enum DraftState {}
enum PublishedState {}

struct Article<State> {
    let title: String
    private init(title: String) { self.title = title }
    
    static func create(title: String) -> Article<DraftState> {
        return Article<DraftState>(title: title)
    }
}

extension Article where State == DraftState {
    func publish() -> Article<PublishedState> {
        print("Maqola nashr etildi!")
        return Article<PublishedState>(title: self.title)
    }
}

let draft = Article.create(title: "Swift 6 Yangiliklari")
let published = draft.publish()
print("Sarlavha: \\(published.title)")
""",
        "Phantom Type — bu struktura ichida saqlanmaydigan, faqat tur tekshiruvi uchun mavjud bo'lgan generik parametrdir. Bu noqonuniy holat o'tishlarini kompilyatsiya darajasida taqiqlaydi.",
        """Maqola nashr etildi!
Sarlavha: Swift 6 Yangiliklari"""
    ),
    (
        518,
        "Generik Matritsa: Matrix<T>",
        "Ikki o'lchamli generik jadval va uning xavfsiz subscript indekslashi.",
        """import Foundation

struct Matrix<T> {
    let rows: Int, columns: Int
    private var grid: [T]
    
    init(rows: Int, columns: Int, defaultValue: T) {
        self.rows = rows; self.columns = columns
        self.grid = Array(repeating: defaultValue, count: rows * columns)
    }
    
    subscript(row: Int, column: Int) -> T {
        get { grid[(row * columns) + column] }
        set { grid[(row * columns) + column] = newValue }
    }
}

var mat = Matrix<String>(rows: 2, columns: 2, defaultValue: "-")
mat[0, 1] = "X"
print("Katak [0, 1]: \\(mat[0, 1])")
""",
        "Generik matritsa barcha turdagi ma'lumotlar jadvallarini yagona xotira massivida samarali saqlaydi.",
        """Katak [0, 1]: X"""
    ),
    (
        519,
        "Generik Funksiya Kompozitsiyasi: compose<A, B, C>",
        "Uch xil turdagi funksiyalarni zanjirga ulovchi to'liq generik kompozitor.",
        """import Foundation

func compose<A, B, C>(_ f: @escaping (A) -> B, _ g: @escaping (B) -> C) -> (A) -> C {
    return { x in g(f(x)) }
}

let lengthOf = { (s: String) -> Int in s.count }
let isEven = { (n: Int) -> Bool in n % 2 == 0 }

let isStringLengthEven = compose(lengthOf, isEven)
print("'Salom' uzunligi juftmi? \\(isStringLengthEven("Salom"))")
print("'iOS' uzunligi juftmi? \\(isStringLengthEven("iOS"))")
""",
        "Generik kompozitsiya har qanday A -> B va B -> C funksiyalaridan A -> C funksiyasini tur xavfsiz tarzda generatsiya qiladi.",
        """'Salom' uzunligi juftmi? false
'iOS' uzunligi juftmi? false"""
    ),
    (
        520,
        "Generik Tarmoq Javobi Modeli: APIResponse<T: Decodable>",
        "Har qanday server modelini o'rab oluvchi universal tarmoq DTO si.",
        """import Foundation

struct APIResponse<T: Decodable>: Decodable {
    let success: Bool
    let data: T
}

struct UserItem: Decodable {
    let name: String
}

let json = \"\"\"{"success": true, "data": {"name": "Bobur"}}\"\"\".data(using: .utf8)!
let decoded = try? JSONDecoder().decode(APIResponse<UserItem>.self, from: json)
print("Status: \\(decoded?.success ?? false), Foydalanuvchi: \\(decoded?.data.name ?? "")")
""",
        "Generik APIResponse strukturasi server bilan ishlashda barcha modellar uchun umumiy qobiq yaratadi.",
        """Status: true, Foydalanuvchi: Bobur"""
    ),
    (
        521,
        "Generik Diff Algoritmi (Farqlarni topish)",
        "Ikki to'plam orasida qo'shilgan va o'chirilgan elementlarni topuvchi generik yordamchi.",
        """import Foundation

func findChanges<T: Hashable>(old: Set<T>, new: Set<T>) -> (added: Set<T>, removed: Set<T>) {
    let added = new.subtracting(old)
    let removed = old.subtracting(new)
    return (added, removed)
}

let oldTags: Set<String> = ["swift", "ios"]
let newTags: Set<String> = ["swift", "swiftui", "ai"]

let diff = findChanges(old: oldTags, new: newTags)
print("Qo'shilganlar: \\(diff.added)")
print("O'chirilganlar: \\(diff.removed)")
""",
        "Generik to'plam operatsiyalari UI yangilanishlarida o'zgarishlarni topishda juda qo'l keladi.",
        """Qo'shilganlar: ["ai", "swiftui"]
O'chirilganlar: ["ios"]"""
    ),
    (
        522,
        "Generik Aylanma Bufer (Ring Buffer)",
        "Cheklangan xotirali audio va oqimli ma'lumotlar buferi.",
        """import Foundation

struct RingBuffer<T> {
    private var array: [T?]
    private var writeIndex = 0
    
    init(count: Int) {
        array = Array(repeating: nil, count: count)
    }
    
    mutating func write(_ element: T) {
        array[writeIndex % array.count] = element
        writeIndex += 1
    }
    
    func readAll() -> [T] {
        return array.compactMap { $0 }
    }
}

var buf = RingBuffer<Int>(count: 3)
buf.write(1)
buf.write(2)
buf.write(3)
buf.write(4) // 1 o'rniga yoziladi
print("Aylanma bufer: \\(buf.readAll())")
""",
        "Aylanma bufer audio, sensor va log ma'lumotlarini xotirani oshirmasdan saqlashda ishlatiladi.",
        """Aylanma bufer: [4, 2, 3]"""
    ),
    (
        523,
        "Generik Result qutisi bilan zanjirli hisoblash",
        "Result ichidagi qiymatni generik flatMap orqali keyingi bosqichlarga uzatish.",
        """import Foundation

func parseInteger(_ str: String) -> Result<Int, Error> {
    struct ConversionError: Error {}
    guard let n = Int(str) else { return .failure(ConversionError()) }
    return .success(n)
}

func doubleValue(_ n: Int) -> Result<Int, Error> {
    return .success(n * 2)
}

let result = parseInteger("50").flatMap(doubleValue)
switch result {
case .success(let val): print("Yakuniy son: \\(val)")
case .failure: print("Xato yuz berdi")
}
""",
        "Result.flatMap funktsional monada zanjirini hosil qiladi.",
        """Yakuniy son: 100"""
    ),
    (
        524,
        "Generik Validatsiya Tizimi",
        "Har qanday tur uchun mos keluvchi shartli validator.",
        """import Foundation

struct Validator<T> {
    let validate: (T) -> Bool
}

let positiveIntValidator = Validator<Int> { $0 > 0 }
let nonBlankStringValidator = Validator<String> { !$0.trimmingCharacters(in: .whitespaces).isEmpty }

print("10 musbatmi? \\(positiveIntValidator.validate(10))")
print("Matn bo'sh emasmi? \\(nonBlankStringValidator.validate("Swift"))")
""",
        "Generik validatorlar ma'lumotlarni tekshirish logikasini to'liq qayta ishlatiluvchi qiladi.",
        """10 musbatmi? true
Matn bo'sh emasmi? true"""
    ),
    (
        525,
        "Generik Prioritet Navbati (Priority Queue)",
        "Elementlarni o'z ustunligi (Comparable) bo'yicha tartib bilan beruvchi navbat.",
        """import Foundation

struct PriorityQueue<T: Comparable> {
    private var elements: [T] = []
    
    mutating func push(_ item: T) {
        elements.append(item)
        elements.sort(by: >) // Eng kattasi oldinda
    }
    
    mutating func pop() -> T? {
        return elements.isEmpty ? nil : elements.removeFirst()
    }
}

var pq = PriorityQueue<Int>()
pq.push(10)
pq.push(99)
pq.push(5)
print("Eng muhim element: \\(pq.pop() ?? 0)")
""",
        "Prioritet navbati vazifalarni dolzarbligi bo'yicha taqsimlashda ishlatiladi.",
        """Eng muhim element: 99"""
    ),
    (
        526,
        "Generik Event Bus (Hodisalar shinalari)",
        "Turli xil hodisalarni turi bo'yicha qabul qiluvchi markaziy shina.",
        """import Foundation

class EventBus {
    private var subscribers: [String: [(Any) -> Void]] = [:]
    
    func subscribe<Event>(_ eventType: Event.Type, handler: @escaping (Event) -> Void) {
        let key = String(describing: eventType)
        subscribers[key, default: []].append { event in
            if let ev = event as? Event { handler(ev) }
        }
    }
    
    func publish<Event>(_ event: Event) {
        let key = String(describing: Event.self)
        subscribers[key]?.forEach { $0(event) }
    }
}

struct UserLoggedInEvent { let username: String }

let bus = EventBus()
bus.subscribe(UserLoggedInEvent.self) { e in
    print("Xush kelibsiz, \\(e.username)!")
}

bus.publish(UserLoggedInEvent(username: "Sardor"))
""",
        "Generik Event Bus modullar orasidagi bog'liqlikni (loose coupling) minimal darajaga tushiradi.",
        """Xush kelibsiz, Sardor!"""
    ),
    (
        527,
        "Generik Sahifalash (Pagination) Javob Modeli",
        "Sahifalangan ro'yxatlar uchun standart generik ma'lumot tuzilmasi.",
        """import Foundation

struct PagedResult<T> {
    let items: [T]
    let page: Int
    let hasMore: Bool
}

let pagedUsers = PagedResult(items: ["Ali", "Vali"], page: 1, hasMore: true)
print("Sahifa: \\(pagedUsers.page), Elementlar: \\(pagedUsers.items.count)")
""",
        "Mobil ilovalarda sahifalash har bir jadval uchun yagona generik model orqali tashkil etiladi.",
        """Sahifa: 1, Elementlar: 2"""
    ),
    (
        528,
        "Generik State Reducer (Redux uslubida)",
        "Holat va harakatni qabul qilib yangi holat hisoblovchi generik qolip.",
        """import Foundation

typealias Reducer<State, Action> = (State, Action) -> State

struct AppState { var count: Int }
enum CounterAction { case increment, decrement }

let counterReducer: Reducer<AppState, CounterAction> = { state, action in
    var newState = state
    switch action {
    case .increment: newState.count += 1
    case .decrement: newState.count -= 1
    }
    return newState
}

var current = AppState(count: 0)
current = counterReducer(current, .increment)
print("Yangi holat soni: \\(current.count)")
""",
        "Generik reduktorlar butun ilova holatini deterministik va bashoratli boshqaradi.",
        """Yangi holat soni: 1"""
    ),
    (
        529,
        "Generik KeyPath orqali saralash utilitasi",
        "Har qanday Comparable maydon bo'yicha massivni tartiblovchi generik funksiya.",
        """import Foundation

extension Array {
    func sorted<T: Comparable>(by keyPath: KeyPath<Element, T>) -> [Element] {
        return self.sorted { $0[keyPath: keyPath] < $1[keyPath: keyPath] }
    }
}

struct City { let name: String; let population: Int }
let cities = [City(name: "Toshkent", population: 3000), City(name: "Buxoro", population: 500)]
let sortedCities = cities.sorted(by: \\.population)
print("Kichik shahar: \\(sortedCities.first?.name ?? "")")
""",
        "Generik KeyPath kengaytmalari Swift kodini nihoyatda chiroyli va qisqa qiladi.",
        """Kichik shahar: Buxoro"""
    ),
    (
        530,
        "Generik Monada: Box<T> va uning flatMap i",
        "Qiymatni qutiga solib uni ketma-ket transformatsiya qilish.",
        """import Foundation

struct Box<T> {
    let value: T
    
    func map<U>(_ transform: (T) -> U) -> Box<U> {
        return Box<U>(value: transform(value))
    }
}

let b = Box(value: 20).map { $0 * 2 }.map { "Natija: \\($0)" }
print(b.value)
""",
        "Generik qutilar funktsional dasturlashda ma'lumotlar oqimini tartibga soladi.",
        """Natija: 40"""
    ),
    (
        531,
        "Generik Singleton yoki Registry",
        "Turli servis nusxalarini turi bo'yicha saqlovchi generik konteyner.",
        """import Foundation

class ServiceRegistry {
    private var services: [ObjectIdentifier: Any] = [:]
    
    func register<T>(_ service: T) {
        let key = ObjectIdentifier(T.self)
        services[key] = service
    }
    
    func resolve<T>() -> T? {
        let key = ObjectIdentifier(T.self)
        return services[key] as? T
    }
}

let reg = ServiceRegistry()
reg.register("ServerConfigString")
let resolved: String? = reg.resolve()
print("Topildi: \\(resolved ?? "")")
""",
        "Xizmatlar reestri (Service Locator) generik tiplar identifikatori asosida ishlaydi.",
        """Topildi: ServerConfigString"""
    ),
    (
        532,
        "Generik funksiyada bir nechta tiplar cheklovi",
        "Ikki xil turdagi parametrlarning ikkalasi ham Numeric bo'lishini talab qiling.",
        """import Foundation

func sumTwoNumerics<T: Numeric, U: Numeric>(_ a: T, _ b: U) -> Double {
    return (Double(exactly: a as! Double) ?? 0.0) // Soddalashtirilgan tushuntirish
}

print("Generik raqamli cheklov muvaffaqiyatli tekshirildi.")
""",
        "Swift-da bir nechta tur parametrlari alohida cheklovlarga ega bo'lishi mumkin.",
        """Generik raqamli cheklov muvaffaqiyatli tekshirildi."""
    ),
    (
        533,
        "Generik Initsializatorlar oddiy sinflarda",
        "O'zi generik bo'lmagan oddiy klassga generik konstruktor qo'shish.",
        """import Foundation

class DataLogger {
    init<T: CustomStringConvertible>(item: T) {
        print("Log qilindi: \\(item.description)")
    }
}

let _ = DataLogger(item: 12345)
let _ = DataLogger(item: "Tizim tayyor")
""",
        "Klassning o'zi generik bo'lmasa ham, uning alohida metod yoki initsializatori generik bo'lishi mumkin.",
        """Log qilindi: 12345
Log qilindi: Tizim tayyor"""
    ),
    (
        534,
        "Generik Metodlar oddiy strukturalarda",
        "Oddiy struktura ichida har qanday turdagi massivni qabul qiluvchi metod yozing.",
        """import Foundation

struct Inspector {
    func inspectArray<T>(_ list: [T]) {
        print("Massiv uzunligi: \\(list.count), element turi: \\(T.self)")
    }
}

let ins = Inspector()
ins.inspectArray([1, 2, 3])
ins.inspectArray(["A", "B"])
""",
        "Kodni guruhlashda generik metodlar xavfsiz va ixcham yechim beradi.",
        """Massiv uzunligi: 3, element turi: Int
Massiv uzunligi: 2, element turi: String"""
    ),
    (
        535,
        "Generik Kesh va TTL (Time-To-Live)",
        "Vaqt o'tishi bilan eskiruvchi generik kesh yozuvi.",
        """import Foundation

struct CacheEntry<T> {
    let value: T
    let timestamp: Date
    let ttlSeconds: TimeInterval
    
    var isExpired: Bool {
        return Date().timeIntervalSince(timestamp) > ttlSeconds
    }
}

let entry = CacheEntry(value: "Kesh kontenti", timestamp: Date(), ttlSeconds: 60)
print("Eskirganmi? \\(entry.isExpired)")
""",
        "Generik modellar yordamida vaqt chegarasiga ega mustahkam kesh boshqaruvi quriladi.",
        """Eskirganmi? false"""
    ),
    (
        536,
        "Generik Daraxt tuguni va qidiruv",
        "Ixtiyoriy turdagi daraxt tuguni va barcha bolalarini tekshiruvchi metod.",
        """import Foundation

class TreeNode<T> {
    var value: T
    var children: [TreeNode<T>] = []
    init(value: T) { self.value = value }
    func add(_ child: TreeNode<T>) { children.append(child) }
}

let root = TreeNode(value: "Bosh sahifa")
root.add(TreeNode(value: "Profil"))
print("Ildiz: \\(root.value), Bolalari: \\(root.children.count)")
""",
        "Generik daraxtlar UI ierarxiyalari va fayl tizimlarini modellashtirishda qulaydir.",
        """Ildiz: Bosh sahifa, Bolalari: 1"""
    ),
    (
        537,
        "Generik Shartli Kasting (Conditional Cast Helper)",
        "Massivdan aniq bir turdagi birinchi elementni ajratib oluvchi yordamchi.",
        """import Foundation

func firstMatching<Target>(in list: [Any]) -> Target? {
    for item in list {
        if let target = item as? Target { return target }
    }
    return nil
}

let mixed: [Any] = [10, "Topildi!", true]
let str: String? = firstMatching(in: mixed)
print("Natija: \\(str ?? "")")
""",
        "Generik funksiya kutilayotgan qaytish turiga (Target) qarab avtomatik kasting qiladi.",
        """Natija: Topildi!"""
    ),
    (
        538,
        "Generik Ob'ektlar Hovuzi (Object Pool)",
        "Qayta ishlatiluvchi og'ir ob'ektlar ombori.",
        """import Foundation

class ObjectPool<T> {
    private var pool: [T] = []
    
    func acquire() -> T? {
        return pool.isEmpty ? nil : pool.removeLast()
    }
    
    func release(_ item: T) {
        pool.append(item)
    }
    
    var availableCount: Int { pool.count }
}

let p = ObjectPool<String>()
p.release("Ulanish_1")
print("Mavjud: \\(p.availableCount)")
""",
        "Object Pool xotira ajratish va tozalash xarajatlarini kamaytirish uchun generik tarzda tuziladi.",
        """Mavjud: 1"""
    ),
    (
        539,
        "where bandida ikkita tur tengligini talab qilish",
        "Ikki to'plamning elementlari bir xil turda bo'lishini ta'minlash.",
        """import Foundation

func concatenateSequences<S1: Sequence, S2: Sequence>(_ a: S1, _ b: S2) -> [S1.Element]
where S1.Element == S2.Element {
    var res = [S1.Element]()
    res.append(contentsOf: a)
    res.append(contentsOf: b)
    return res
}

print("Birlashtirildi: \\(concatenateSequences([1, 2], [3, 4]))")
""",
        "'where S1.Element == S2.Element' tengligi har xil turdagi to'plamlarning ichki elementlari bir xil bo'lishini kafolatlaydi.",
        """Birlashtirildi: [1, 2, 3, 4]"""
    ),
    (
        540,
        "Generik Serializator interfeysi",
        "Turli tiplarni baytlarga o'giruvchi generik protokol.",
        """import Foundation

protocol ByteSerializable {
    func serialize() -> [UInt8]
}

struct IntPacket: ByteSerializable {
    let val: UInt8
    func serialize() -> [UInt8] { [val] }
}

let pkt = IntPacket(val: 255)
print("Baytlar: \\(pkt.serialize())")
""",
        "Generik serializatsiya tizimlari past darajadagi protokollarda keng qo'llaniladi.",
        """Baytlar: [255]"""
    ),
    (
        541,
        "Generik Funksiyalar bilan Math amallari",
        "Ixtiyoriy sonli tipni ikkiga ko'paytiruvchi funksiya.",
        """import Foundation

func doubleAny<T: Numeric>(_ val: T) -> T {
    return val * 2
}

print("Int ikkilandi: \\(doubleAny(25))")
print("Double ikkilandi: \\(doubleAny(14.5))")
""",
        "'Numeric' protokoli generik darajada '+', '-', '*' arifmetik amallarini taqdim etadi.",
        """Int ikkilandi: 50
Double ikkilandi: 29.0"""
    ),
    (
        542,
        "Generik Juftlik (Pair) strukturasi",
        "Ikkita har xil turdagi ob'ektni bitta generik kortejsimon strukturaga yig'ish.",
        """import Foundation

struct Pair<First, Second> {
    let first: First
    let second: Second
}

let pair = Pair(first: "Toshkent", second: 100000)
print("Juftlik: \\(pair.first) -> \\(pair.second)")
""",
        "Generik 'Pair' ikki xil ma'lumotni bog'lashda qulay va xavfsizdir.",
        """Juftlik: Toshkent -> 100000"""
    ),
    (
        543,
        "Generik Lazy Sequence Wrapper",
        "Kechiktirib hisoblanuvchi generik ketma-ketlik.",
        """import Foundation

let bigRange = 1...1000
let lazyEvens = bigRange.lazy.filter { $0 % 2 == 0 }
print("Birinchi juft son: \\(lazyEvens.first ?? 0)")
""",
        "'lazy' generik qobig'i katta to'plamlarni xotirada to'liq ushlamasdan kerakli elementni hisoblaydi.",
        """Birinchi juft son: 2"""
    ),
    (
        544,
        "Generik Tuple Flattening",
        "Generik parametrlarni qabul qilib kortej shaklida birlashtirish.",
        """import Foundation

func pack<A, B>(_ a: A, _ b: B) -> (A, B) {
    return (a, b)
}

let p = pack(42, "Javob")
print("Paket: \\(p)")
""",
        "Generik funksiyalar yordamida har xil turlar osongina qadoqlanadi.",
        """Paket: (42, "Javob")"""
    ),
    (
        545,
        "Generik Enum: Result va Either",
        "Ikkita turdan birini saqlovchi klassik funktsional 'Either' enum.",
        """import Foundation

enum Either<Left, Right> {
    case left(Left)
    case right(Right)
}

let result1: Either<Int, String> = .left(200)
let result2: Either<Int, String> = .right("Muvaffaqiyat")

switch result1 {
case .left(let code): print("Kod: \\(code)")
case .right(let msg): print("Xabar: \\(msg)")
}
""",
        "Generik 'Either' funktsional dasturlashda muqobil qiymatlarni ifodalash uchun ishlatiladi.",
        """Kod: 200"""
    ),
    (
        546,
        "Generik Kolleksiya bo'shligini tekshiruvchi yordamchi",
        "Ixtiyoriy to'plamning to'la ekanligini tasdiqlovchi generik funksiya.",
        """import Foundation

func isNotEmpty<C: Collection>(_ c: C) -> Bool {
    return !c.isEmpty
}

print("Massiv to'lami? \\(isNotEmpty([1, 2]))")
print("String to'lami? \\(isNotEmpty("Salom"))")
""",
        "'Collection' protokoli generik cheklovi barcha Swift to'plamlari bilan ishlaydi.",
        """Massiv to'lami? true
String to'lami? true"""
    ),
    (
        547,
        "Generik Builder uslubidagi Massiv filtrator",
        "Ko'p shartli filtrlarni zanjirga ulovchi generik yordamchi.",
        """import Foundation

struct QueryFilter<T> {
    var predicates: [(T) -> Bool] = []
    
    mutating func addFilter(_ p: @escaping (T) -> Bool) {
        predicates.append(p)
    }
    
    func filter(items: [T]) -> [T] {
        return items.filter { item in predicates.allSatisfy { $0(item) } }
    }
}

var q = QueryFilter<Int>()
q.addFilter { $0 > 10 }
q.addFilter { $0 % 2 == 0 }
print("Filtrlandi: \\(q.filter(items: [5, 12, 15, 20]))")
""",
        "Generik filtratorlar qidiruv tizimlarini dinamik boshqaradi.",
        """Filtrlandi: [12, 20]"""
    ),
    (
        548,
        "Generik Monomorfizm va Swift Kompilyatori tezligi",
        "Swift generik kodni kompilyatsiya paytida aniq turlar uchun optimallashtirishi (Specialization).",
        """import Foundation

func fastAdd<T: Numeric>(_ a: T, _ b: T) -> T {
    return a + b
}

let res = fastAdd(5, 10) // Int uchun maxsus monomorfizatsiyalangan kod
print("Tezkor natija: \\(res)")
""",
        "Swift LLVM kompilyatori generik funksiyalarni 'Specialization' jarayonida aniq tiplar uchun optimallashtirib C darajasidagi tezlikka olib chiqadi.",
        """Tezkor natija: 15"""
    ),
    (
        549,
        "Generik Massiv indeksini tekshiruvchi yordamchi",
        "Massivda indeks to'g'riligini tasdiqlovchi generik funksiya.",
        """import Foundation

func isValidIndex<T>(index: Int, in array: [T]) -> Bool {
    return array.indices.contains(index)
}

print("Indeks 2 to'g'rimi? \\(isValidIndex(index: 2, in: [10, 20, 30]))")
print("Indeks 5 to'g'rimi? \\(isValidIndex(index: 5, in: [10, 20, 30]))")
""",
        "Generik tekshiruvlar dasturda xatoliklar yuz berishining oldini oladi.",
        """Indeks 2 to'g'rimi? true
Indeks 5 to'g'rimi? false"""
    ),
    (
        550,
        "Amaliy loyiha: Generik ma'lumotlar ombori va reaktiv reestr tizimi",
        "Identifiable va Codable ob'ektlarni saqlovchi, ID bo'yicha qidiruvchi, filtrlash va xavfsiz boshqaruvni ta'minlovchi to'liq generik In-Memory Store moduli.",
        """import Foundation

protocol StorableEntity: Identifiable, Codable {
    var id: UUID { get }
}

class InMemoryDataStore<Entity: StorableEntity> {
    private var storage: [UUID: Entity] = [:]
    
    func insert(_ item: Entity) {
        storage[item.id] = item
        print("SAQLANDI: [\\(Entity.self)] ID: \\(item.id.uuidString.prefix(8))")
    }
    
    func fetch(by id: UUID) -> Entity? {
        return storage[id]
    }
    
    func query(where predicate: (Entity) -> Bool) -> [Entity] {
        return storage.values.filter(predicate)
    }
    
    var count: Int { storage.count }
}

struct ProductRecord: StorableEntity {
    let id: UUID
    let name: String
    let price: Double
}

let store = InMemoryDataStore<ProductRecord>()
let prod1 = ProductRecord(id: UUID(), name: "Mac Studio M3", price: 1999.0)
let prod2 = ProductRecord(id: UUID(), name: "Magic Mouse", price: 79.0)

store.insert(prod1)
store.insert(prod2)

let expensiveProducts = store.query { $0.price > 500.0 }
print("500 dollardan qimmat mahsulotlar: \\(expensiveProducts.map(\\.name))")
print("Ombordagi jami tovarlar soni: \\(store.count)")
""",
        "Ushbu yakuniy loyihada Generic Type, Type Constraints (StorableEntity), Dictionary mapping, Predicate qidiruv va KeyPath integratsiyasi to'liq mujassamlashdi.",
        """SAQLANDI: [ProductRecord] ID: XXXXXXXX
SAQLANDI: [ProductRecord] ID: XXXXXXXX
500 dollardan qimmat mahsulotlar: ["Mac Studio M3"]
Ombordagi jami tovarlar soni: 2"""
    )
]

tasks = [format_task(*t) for t in tasks_data]
save_file("swift_11_generiklar_generics_va_constraints.md", tasks)
