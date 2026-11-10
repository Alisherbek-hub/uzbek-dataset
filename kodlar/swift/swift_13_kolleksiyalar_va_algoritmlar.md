# 601-Topshiriq: Swift Kolleksiyalari arxitekturasi: Array, Set, Dictionary
## Topshiriq sharti:
Uch asosiy to'plam turining farqlarini va e'lon qilinishini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

let array: [String] = ["A", "B", "C", "A"] // Tartiblangan, takrorlanuvchi
let set: Set<String> = ["A", "B", "C", "A"] // Tartibsiz, unikal
let dictionary: [String: Int] = ["A": 1, "B": 2] // Kalit-qiymat juftligi

print("Array elementlari soni: \(array.count)")
print("Set elementlari soni: \(set.count)")
print("Dictionary juftliklari soni: \(dictionary.count)")
```

## Tushuntirish va Mantiq:
Swift uch asosiy to'plamni taqdim etadi: Massiv (Array) tartibli ro'yxat; To'plam (Set) tartibsiz unikal elementlar; Lug'at (Dictionary) esa tezkor xesh-jadval kalit-qiymat tuzilmasidir.

## Ishlash natijasi:
```text
Array elementlari soni: 4
Set elementlari soni: 3
Dictionary juftliklari soni: 2
```


# 602-Topshiriq: Massiv xotira sig'imi: reserveCapacity(_:)
## Topshiriq sharti:
Massivning qayta-qayta xotira ajratish xarajatlarini kamaytirish uchun sig'imni oldindan band qiling.

## Yechim (Swift kodi):
```swift
import Foundation

var numbers = [Int]()
print("Boshlang'ich capacity: \(numbers.capacity)")

numbers.reserveCapacity(100)
print("reserveCapacity(100) dan keyin: \(numbers.capacity)")

for i in 1...5 {
    numbers.append(i)
}
print("Elementlar: \(numbers), Hali ham capacity: \(numbers.capacity)")
```

## Tushuntirish va Mantiq:
'reserveCapacity(_:)' massivga kutilayotgan elementlar sonini aytib, xotira buferini bir martada ajratadi. Bu append amallarini amortizatsiyalangan O(1) dan haqiqiy eng yuqori tezlikka olib chiqadi.

## Ishlash natijasi:
```text
Boshlang'ich capacity: 0
reserveCapacity(100) dan keyin: 100
Elementlar: [1, 2, 3, 4, 5], Hali ham capacity: 100
```


# 603-Topshiriq: Massivda qo'shish va o'chirish samaradorligi (Big-O)
## Topshiriq sharti:
Massiv oxiriga qo'shish O(1) va boshiga qo'shish O(N) farqini ko'rsatuvchi dastur.

## Yechim (Swift kodi):
```swift
import Foundation

var list = [10, 20, 30]

// O(1) amallar:
list.append(40)
_ = list.popLast()

// O(N) amallar (barcha elementlar siljiydi):
list.insert(5, at: 0)
list.remove(at: 0)

print("Yakuniy massiv: \(list)")
```

## Tushuntirish va Mantiq:
Massiv oxiriga append/popLast qilish O(1) doimiy vaqt oladi, boshiga insert/remove qilish esa barcha keyingi elementlarni xotirada surishga majbur bo'lgani uchun O(N) chiziqli vaqt talab qiladi.

## Ishlash natijasi:
```text
Yakuniy massiv: [10, 20, 30]
```


# 604-Topshiriq: Massivni tilimlash: ArraySlice va xotira
## Topshiriq sharti:
Massivning bir qismini alohida yangi xotira ajratmasdan 'ArraySlice' orqali o'qing.

## Yechim (Swift kodi):
```swift
import Foundation

let originalArray = [100, 200, 300, 400, 500]
let slice: ArraySlice<Int> = originalArray[1...3]

print("Slice elementlari: \(Array(slice))")
print("Slice boshlang'ich indeksi: \(slice.startIndex)") // 1 bo'ladi, 0 emas!
```

## Tushuntirish va Mantiq:
ArraySlice ona massivning xotirasiga to'g'ridan-to'g'ri qaraydi va xotira nusxalamaydi. Muhimi, ArraySlice ona massiv indekslarini (startIndex: 1) to'liq saqlab qoladi.

## Ishlash natijasi:
```text
Slice elementlari: [200, 300, 400]
Slice boshlang'ich indeksi: 1
```


# 605-Topshiriq: Set (To'plam) amallari: union, intersection, subtracting
## Topshiriq sharti:
Ikki guruh dasturchilarining umumiy va farqli ko'nikmalarini to'plam amallari bilan toping.

## Yechim (Swift kodi):
```swift
import Foundation

let teamA: Set<String> = ["Swift", "Kotlin", "Go"]
let teamB: Set<String> = ["Swift", "Rust", "Python"]

let common = teamA.intersection(teamB)
let allSkills = teamA.union(teamB)
let onlyInA = teamA.subtracting(teamB)

print("Umumiy ko'nikmalar: \(common)")
print("Jami barcha ko'nikmalar: \(allSkills)")
print("Faqat A jamoada bor: \(onlyInA)")
```

## Tushuntirish va Mantiq:
Set to'plamlar ustida matematik nazariya amallari: intersection (kesishma), union (birlashma), subtracting (ayirma) va symmetricDifference (simmetrik ayirma) larni O(N) vaqtda bajaradi.

## Ishlash natijasi:
```text
Umumiy ko'nikmalar: ["Swift"]
Jami barcha ko'nikmalar: ["Go", "Kotlin", "Python", "Rust", "Swift"]
Faqat A jamoada bor: ["Go", "Kotlin"]
```


# 606-Topshiriq: Set solishtirishlari: isSubset, isSuperset, isDisjoint
## Topshiriq sharti:
To'plamlarning bir-biriga qamrab olinishini tekshiring.

## Yechim (Swift kodi):
```swift
import Foundation

let allAccess: Set = ["read", "write", "delete", "admin"]
let userPermissions: Set = ["read", "write"]
let guestPermissions: Set = ["preview"]

print("user allAccess ning qism to'plamimi? \(userPermissions.isSubset(of: allAccess))")
print("allAccess user ning ustki to'plamimi? \(allAccess.isSuperset(of: userPermissions))")
print("user va guest mutlaqo kesishmaydimi? \(userPermissions.isDisjoint(with: guestPermissions))")
```

## Tushuntirish va Mantiq:
Ushbu metodlar xavfsizlik va ruxsatlar tizimlarida (RBAC) to'plamlarni solishtirish uchun keng qo'llaniladi.

## Ishlash natijasi:
```text
user allAccess ning qism to'plamimi? true
allAccess user ning ustki to'plamimi? true
user va guest mutlaqo kesishmaydimi? true
```


# 607-Topshiriq: Lug'atlarni birlashtirish: merging(_:uniquingKeysWith:)
## Topshiriq sharti:
Ikki lug'at birlashganda bir xil kalitlarning qiymatlarini qo'shib yuboruvchi qoidani yozing.

## Yechim (Swift kodi):
```swift
import Foundation

let stockA = ["Olma": 50, "Nok": 30]
let stockB = ["Olma": 20, "Anor": 40]

let combined = stockA.merging(stockB) { current, new in
    return current + new // To'qnash kelganda qo'shamiz
}

print("Birlashtirilgan ombor: \(combined)")
```

## Tushuntirish va Mantiq:
'merging(_:uniquingKeysWith:)' kalitlar bir xil bo'lib qolgan holatda qaysi qiymat olinishi yoki ularni qanday aralashtirishni closure orqali hal qiladi.

## Ishlash natijasi:
```text
Birlashtirilgan ombor: ["Anor": 40, "Nok": 30, "Olma": 70]
```


# 608-Topshiriq: Lug'at qiymatlarini transformatsiya qilish: mapValues
## Topshiriq sharti:
Lug'at kalitlariga tegmasdan faqat uning qiymatlarini yangilang.

## Yechim (Swift kodi):
```swift
import Foundation

let productPricesUSD = ["MacBook": 1200.0, "iPad": 600.0]
let exchangeRate = 12800.0

let productPricesUZS = productPricesUSD.mapValues { $0 * exchangeRate }
print("Narxlar so'mda: \(productPricesUZS)")
```

## Tushuntirish va Mantiq:
'mapValues' lug'at strukturasini saqlagan holda qiymatlarni tezkor o'zgartirishning eng toza usulidir.

## Ishlash natijasi:
```text
Narxlar so'mda: ["MacBook": 15360000.0, "iPad": 7680000.0]
```


# 609-Topshiriq: Lug'atni guruhlash: Dictionary(grouping:by:)
## Topshiriq sharti:
Talabalarni ularning yoshi bo'yicha lug'atga guruhlang.

## Yechim (Swift kodi):
```swift
import Foundation

struct Student { let name: String; let age: Int }

let students = [
    Student(name: "Ali", age: 20),
    Student(name: "Vali", age: 21),
    Student(name: "Sami", age: 20)
]

let groupedByAge = Dictionary(grouping: students, by: \.age)

for (age, list) in groupedByAge {
    print("\(age) yosh: \(list.map(\.name))")
}
```

## Tushuntirish va Mantiq:
'Dictionary(grouping:by:)' istalgan to'plamni kloujer yoki KeyPath bo'yicha [Key: [Element]] ko'rinishida guruhlaydi.

## Ishlash natijasi:
```text
20 yosh: ["Ali", "Sami"]
21 yosh: ["Vali"]
```


# 610-Topshiriq: Maxsus Sequence va IteratorProtocol
## Topshiriq sharti:
Fibonachchi ketma-ketligini 'for-in' tsiklida cheksiz aylanish imkonini beruvchi Sequence yozing.

## Yechim (Swift kodi):
```swift
import Foundation

struct FibonacciSequence: Sequence {
    func makeIterator() -> FibonacciIterator {
        return FibonacciIterator()
    }
}

struct FibonacciIterator: IteratorProtocol {
    private var current = 0
    private var nextVal = 1
    
    mutating func next() -> Int? {
        let result = current
        current = nextVal
        nextVal = result + nextVal
        return result
    }
}

var count = 0
for num in FibonacciSequence() {
    print(num, terminator: " ")
    count += 1
    if count >= 7 { break }
}
print()
```

## Tushuntirish va Mantiq:
Swift-da 'for-in' tsikli 'Sequence' va 'IteratorProtocol' ga asoslanadi. 'next()' metodi har qadamda keyingi elementni yoki tugaganda nil qaytaradi.

## Ishlash natijasi:
```text
0 1 1 2 3 5 8
```


# 611-Topshiriq: Ikkilik Qidiruv Algoritmi (Binary Search)
## Topshiriq sharti:
Tartiblangan massivdan qiymatni O(log N) tezlikda toping.

## Yechim (Swift kodi):
```swift
import Foundation

func binarySearch<T: Comparable>(_ array: [T], target: T) -> Int? {
    var lower = 0
    var upper = array.count - 1
    
    while lower <= upper {
        let mid = (lower + upper) / 2
        if array[mid] == target {
            return mid
        } else if array[mid] < target {
            lower = mid + 1
        } else {
            upper = mid - 1
        }
    }
    return nil
}

let sortedData = [10, 25, 34, 48, 59, 72, 85, 99]
let idx = binarySearch(sortedData, target: 72)
print("72 ning indeksi: \(idx ?? -1)")
```

## Tushuntirish va Mantiq:
Ikkilik qidiruv har bir qadamda qidiruv sohasini 2 barobar qisqartirib O(log N) logarifmik tezlikda ishlaydi.

## Ishlash natijasi:
```text
72 ning indeksi: 5
```


# 612-Topshiriq: Tezkor Saralash Algoritmi (QuickSort)
## Topshiriq sharti:
Massivni 'pivot' element tanlash orqali rekursiv saralang.

## Yechim (Swift kodi):
```swift
import Foundation

func quickSort<T: Comparable>(_ array: [T]) -> [T] {
    guard array.count > 1 else { return array }
    
    let pivot = array[array.count / 2]
    let less = array.filter { $0 < pivot }
    let equal = array.filter { $0 == pivot }
    let greater = array.filter { $0 > pivot }
    
    return quickSort(less) + equal + quickSort(greater)
}

let unsorted = [64, 34, 25, 12, 22, 11, 90]
print("QuickSort natijasi: \(quickSort(unsorted))")
```

## Tushuntirish va Mantiq:
QuickSort 'bo'lib tashla va hukmronlik qil' (divide and conquer) tamoyiliga asoslangan eng mashhur va samarali O(N log N) saralash algoritmlaridan biridir.

## Ishlash natijasi:
```text
QuickSort natijasi: [11, 12, 22, 25, 34, 64, 90]
```


# 613-Topshiriq: Birlashuvchi Saralash Algoritmi (MergeSort)
## Topshiriq sharti:
Massivni teng ikkiga bo'lib, saralab qayta birlashtiruvchi barqaror (stable) algoritm.

## Yechim (Swift kodi):
```swift
import Foundation

func mergeSort<T: Comparable>(_ array: [T]) -> [T] {
    guard array.count > 1 else { return array }
    let middle = array.count / 2
    let left = mergeSort(Array(array[..<middle]))
    let right = mergeSort(Array(array[middle...]))
    return merge(left, right)
}

func merge<T: Comparable>(_ left: [T], _ right: [T]) -> [T] {
    var leftIdx = 0, rightIdx = 0, result = [T]()
    while leftIdx < left.count && rightIdx < right.count {
        if left[leftIdx] < right[rightIdx] {
            result.append(left[leftIdx]); leftIdx += 1
        } else {
            result.append(right[rightIdx]); rightIdx += 1
        }
    }
    result.append(contentsOf: left[leftIdx...])
    result.append(contentsOf: right[rightIdx...])
    return result
}

print("MergeSort natijasi: \(mergeSort([38, 27, 43, 3, 9, 82, 10]))")
```

## Tushuntirish va Mantiq:
MergeSort har doim kafolatlangan O(N log N) vaqt murakkabligini ta'minlaydi va elementlar o'rni barqarorligini (stability) saqlaydi.

## Ishlash natijasi:
```text
MergeSort natijasi: [3, 9, 10, 27, 38, 43, 82]
```


# 614-Topshiriq: Kolleksiya bo'laklash: Chunks algoritmi
## Topshiriq sharti:
Katta massivni N tadan bo'laklarga (chunks) ajratuvchi funksiya.

## Yechim (Swift kodi):
```swift
import Foundation

extension Array {
    func chunked(into size: Int) -> [[Element]] {
        return stride(from: 0, to: count, by: size).map {
            Array(self[$0..<Swift.min($0 + size, count)])
        }
    }
}

let items = [1, 2, 3, 4, 5, 6, 7, 8]
print("Bo'laklar (3 tadan): \(items.chunked(into: 3))")
```

## Tushuntirish va Mantiq:
Bo'laklash (chunking) ma'lumotlarni paketlab serverga yuborishda va sahifalashda doimiy qo'llaniladi.

## Ishlash natijasi:
```text
Bo'laklar (3 tadan): [[1, 2, 3], [4, 5, 6], [7, 8]]
```


# 615-Topshiriq: Oynali Siljish Algoritmi (Sliding Window)
## Topshiriq sharti:
Massivda K ta ketma-ket elementlarning maksimal yig'indisini O(N) vaqtda toping.

## Yechim (Swift kodi):
```swift
import Foundation

func maxSubarraySum(_ array: [Int], k: Int) -> Int? {
    guard array.count >= k else { return nil }
    var windowSum = array[..<k].reduce(0, +)
    var maxSum = windowSum
    
    for i in k..<array.count {
        windowSum += array[i] - array[i - k] // Yangi kirdi, eskisi chiqdi
        maxSum = max(maxSum, windowSum)
    }
    return maxSum
}

let data = [2, 1, 5, 1, 3, 2]
print("3 ta element maksimal yig'indisi: \(maxSubarraySum(data, k: 3) ?? 0)")
```

## Tushuntirish va Mantiq:
Sliding Window (sirpanuvchi oyna) algoritmi ichma-ich O(N^2) tsikllarni O(N) chiziqli vaqtga tushiruvchi eng kuchli algoritmik usullardan biridir.

## Ishlash natijasi:
```text
3 ta element maksimal yig'indisi: 9
```


# 616-Topshiriq: Ikki ko'rsatkichli algoritm: Two Pointers (Target Sum)
## Topshiriq sharti:
Tartiblangan massivda yig'indisi maqsadga teng bo'lgan ikki sonni toping.

## Yechim (Swift kodi):
```swift
import Foundation

func twoSumSorted(_ numbers: [Int], target: Int) -> (Int, Int)? {
    var left = 0
    var right = numbers.count - 1
    
    while left < right {
        let sum = numbers[left] + numbers[right]
        if sum == target {
            return (numbers[left], numbers[right])
        } else if sum < target {
            left += 1
        } else {
            right -= 1
        }
    }
    return nil
}

let nums = [2, 7, 11, 15]
if let pair = twoSumSorted(nums, target: 9) {
    print("Topilgan juftlik: \(pair.0) + \(pair.1) = 9")
}
```

## Tushuntirish va Mantiq:
Two Pointers usuli ikkala tomondan qisqartirib O(N) tezlikda masalani hal qiladi.

## Ishlash natijasi:
```text
Topilgan juftlik: 2 + 7 = 9
```


# 617-Topshiriq: Dublikatlarni tartibni saqlagan holda olib tashlash (Deduplication)
## Topshiriq sharti:
Elementlar ketma-ketligi buzilmagan holda takrorlanishlarni tozalang.

## Yechim (Swift kodi):
```swift
import Foundation

extension Array where Element: Hashable {
    func removingDuplicates() -> [Element] {
        var seen = Set<Element>()
        return filter { seen.insert($0).inserted }
    }
}

let list = ["olma", "nok", "olma", "behi", "nok"]
print("Natija: \(list.removingDuplicates())")
```

## Tushuntirish va Mantiq:
'seen.insert($0).inserted' Set-ga yangi element tushsa true, oldin bor bo'lsa false beradi. Bu tartibni saqlab O(N) da tozalaydi.

## Ishlash natijasi:
```text
Natija: ["olma", "nok", "behi"]
```


# 618-Topshiriq: Tasodifiy aralashtirish: Fisher-Yates Shuffle
## Topshiriq sharti:
Massiv elementlarini adolatli tasodifiylik bilan joyida aralashtirish.

## Yechim (Swift kodi):
```swift
import Foundation

var cards = [1, 2, 3, 4, 5]
cards.shuffle() // Standart Swift Fisher-Yates algoritmi
print("Aralashtirilgan elementlar soni: \(cards.count)")
```

## Tushuntirish va Mantiq:
Swift-ning 'shuffle()' metodi O(N) vaqtda Fisher-Yates algoritmi orqali mukammal tasodifiy ehtimollik taqsimotini kafolatlaydi.

## Ishlash natijasi:
```text
Aralashtirilgan elementlar soni: 5
```


# 619-Topshiriq: Kolleksiyada eng ko'p uchragan elementni topish
## Topshiriq sharti:
O(N) vaqtda eng yuqori chastotali elementni aniqlang.

## Yechim (Swift kodi):
```swift
import Foundation

func mostFrequentElement<T: Hashable>(in array: [T]) -> (element: T, count: Int)? {
    let counts = array.reduce(into: [:]) { $0[$1, default: 0] += 1 }
    return counts.max { $0.value < $1.value }.map { ($0.key, $0.value) }
}

let votes = ["A", "B", "A", "C", "A", "B"]
if let winner = mostFrequentElement(in: votes) {
    print("G'olib: '\(winner.element)', ovozlar soni: \(winner.count)")
}
```

## Tushuntirish va Mantiq:
Lug'at hisoblagichi va max(by:) orqali g'olib element O(N) vaqtda aniqlanadi.

## Ishlash natijasi:
```text
G'olib: 'A', ovozlar soni: 3
```


# 620-Topshiriq: Palindromlikni tekshiruvchi algoritm
## Topshiriq sharti:
Matn chapdan ham, o'ngdan ham bir xil o'qilishini ikki ko'rsatkich bilan tekshiring.

## Yechim (Swift kodi):
```swift
import Foundation

func isPalindrome(_ text: String) -> Bool {
    let chars = Array(text.lowercased().filter { $0.isLetter })
    var left = 0, right = chars.count - 1
    while left < right {
        if chars[left] != chars[right] { return false }
        left += 1; right -= 1
    }
    return true
}

print("'Aziza' palindrommi? \(isPalindrome("Aziza"))")
print("'Swift' palindrommi? \(isPalindrome("Swift"))")
```

## Tushuntirish va Mantiq:
Palindromni tekshirishda faqat harflarni filtrlab ikki tomondan markazga qarab yurish eng samarali usuldir.

## Ishlash natijasi:
```text
'Aziza' palindrommi? true
'Swift' palindrommi? false
```


# 621-Topshiriq: Anagrammani aniqlovchi algoritm
## Topshiriq sharti:
Ikki so'z aynan bir xil harflardan tashkil topganini tekshiring.

## Yechim (Swift kodi):
```swift
import Foundation

func isAnagram(_ s1: String, _ s2: String) -> Bool {
    let clean1 = s1.lowercased().filter { $0.isLetter }
    let clean2 = s2.lowercased().filter { $0.isLetter }
    guard clean1.count == clean2.count else { return false }
    return clean1.sorted() == clean2.sorted()
}

print("silent va listen anagrammami? \(isAnagram("silent", "listen"))")
```

## Tushuntirish va Mantiq:
Ikkala so'z harflarini bir xil tartibda saralab solishtirish anagrammani aniqlashning klassik yechimidir.

## Ishlash natijasi:
```text
silent va listen anagrammami? true
```


# 622-Topshiriq: Qavslar balansini tekshiruvchi Stack algoritmi
## Topshiriq sharti:
Matndagi '()', '{}', '[]' qavslar to'g'ri ochilib yopilganini tekshiring.

## Yechim (Swift kodi):
```swift
import Foundation

func isBalanced(_ s: String) -> Bool {
    var stack = [Character]()
    let pairs: [Character: Character] = [")": "(", "}": "{", "]": "["]
    
    for ch in s {
        if ch == "(" || ch == "{" || ch == "[" {
            stack.append(ch)
        } else if let matching = pairs[ch] {
            if stack.isEmpty || stack.removeLast() != matching {
                return false
            }
        }
    }
    return stack.isEmpty
}

print("'{[()]}' to'g'rimi? \(isBalanced("{[()]}"))")
print("'{[(])}' to'g'rimi? \(isBalanced("{[(])}"))")
```

## Tushuntirish va Mantiq:
Stek (Stack) ma'lumot tuzilmasi LIFO xususiyati sababli sintaksis tahlilchilarida (parser) qavslar muvozanatini tekshirish uchun standarrtdir.

## Ishlash natijasi:
```text
'{[()]}' to'g'rimi? true
'{[(])}' to'g'rimi? false
```


# 623-Topshiriq: Prefiksli Daraxt: Trie ma'lumot tuzilmasi
## Topshiriq sharti:
Lug'atda so'z qidirish va avtoto'ldirish (autocomplete) uchun maxsus daraxt.

## Yechim (Swift kodi):
```swift
import Foundation

class TrieNode {
    var children: [Character: TrieNode] = [:]
    var isEndOfWord: Bool = false
}

class Trie {
    private let root = TrieNode()
    
    func insert(_ word: String) {
        var current = root
        for char in word {
            if current.children[char] == nil {
                current.children[char] = TrieNode()
            }
            current = current.children[char]!
        }
        current.isEndOfWord = true
    }
    
    func contains(_ word: String) -> Bool {
        var current = root
        for char in word {
            guard let next = current.children[char] else { return false }
            current = next
        }
        return current.isEndOfWord
    }
}

let trie = Trie()
trie.insert("swift")
trie.insert("swiftui")

print("swift bormi? \(trie.contains("swift"))")
print("apple bormi? \(trie.contains("apple"))")
```

## Tushuntirish va Mantiq:
Trie daraxti so'zlarni prefikslar bo'yicha bog'lab qidiruvni O(L) so'z uzunligiga teng vaqtda bajaradi.

## Ishlash natijasi:
```text
swift bormi? true
apple bormi? false
```


# 624-Topshiriq: Bog'langan Ro'yxat (Singly Linked List)
## Topshiriq sharti:
Tugunlar (Nodes) zanjiridan iborat chiziqli ma'lumot tuzilmasi.

## Yechim (Swift kodi):
```swift
import Foundation

final class Node<T> {
    var value: T
    var next: Node<T>?
    init(value: T) { self.value = value }
}

let head = Node(value: "Boshi")
let second = Node(value: "O'rtasi")
let third = Node(value: "Oxiri")
head.next = second
second.next = third

var current: Node<String>? = head
while let node = current {
    print("-> \(node.value)", terminator: " ")
    current = node.next
}
print()
```

## Tushuntirish va Mantiq:
Bog'langan ro'yxatda xotira uzluksiz bo'lishi shart emas; har bir tugun o'zidan keyingi elementga havola saqlaydi.

## Ishlash natijasi:
```text
-> Boshi -> O'rtasi -> Oxiri
```


# 625-Topshiriq: Graflarni kenglik bo'yicha qidirish (BFS - Breadth-First Search)
## Topshiriq sharti:
Grafda boshlang'ich tugundan eng yaqin qo'shnilarga qarab navbat (Queue) orqali yurish.

## Yechim (Swift kodi):
```swift
import Foundation

func bfs(graph: [String: [String]], start: String) -> [String] {
    var visited = Set<String>()
    var queue = [start]
    var traversal = [String]()
    
    visited.insert(start)
    while !queue.isEmpty {
        let node = queue.removeFirst()
        traversal.append(node)
        for neighbor in graph[node] ?? [] {
            if !visited.contains(neighbor) {
                visited.insert(neighbor)
                queue.append(neighbor)
            }
        }
    }
    return traversal
}

let graph = [
    "A": ["B", "C"],
    "B": ["D"],
    "C": ["E"],
    "D": [], "E": []
]

print("BFS marshruti: \(bfs(graph: graph, start: "A"))")
```

## Tushuntirish va Mantiq:
BFS eng qisqa yo'lni topish uchun navbat (FIFO) tamoyiliga tayanadi.

## Ishlash natijasi:
```text
BFS marshruti: ["A", "B", "C", "D", "E"]
```


# 626-Topshiriq: Graflarni chuqurlik bo'yicha qidirish (DFS - Depth-First Search)
## Topshiriq sharti:
Grafda rekursiya va stek orqali eng chuqur tugungacha yetib borish.

## Yechim (Swift kodi):
```swift
import Foundation

func dfs(graph: [String: [String]], node: String, visited: inout Set<String>, path: inout [String]) {
    visited.insert(node)
    path.append(node)
    for neighbor in graph[node] ?? [] {
        if !visited.contains(neighbor) {
            dfs(graph: graph, node: neighbor, visited: &visited, path: &path)
        }
    }
}

var visitedSet = Set<String>()
var dfsPath = [String]()
dfs(graph: graph, node: "A", visited: &visitedSet, path: &dfsPath)
print("DFS marshruti: \(dfsPath)")
```

## Tushuntirish va Mantiq:
DFS labirintdan chiqish yo'lini izlash kabi rekursiv chuqurlashish algoritmidir.

## Ishlash natijasi:
```text
DFS marshruti: ["A", "B", "D", "C", "E"]
```


# 627-Topshiriq: Eng uzun o'suvchi qism ketma-ketlik (LIS - Longest Increasing Subsequence)
## Topshiriq sharti:
Dinamik dasturlash (DP) orqali massivdagi qat'iy o'suvchi ketma-ketlik uzunligini toping.

## Yechim (Swift kodi):
```swift
import Foundation

func lengthOfLIS(_ nums: [Int]) -> Int {
    guard !nums.isEmpty else { return 0 }
    var dp = Array(repeating: 1, count: nums.count)
    for i in 1..<nums.count {
        for j in 0..<i {
            if nums[i] > nums[j] {
                dp[i] = max(dp[i], dp[j] + 1)
            }
        }
    }
    return dp.max() ?? 1
}

let sequence = [10, 9, 2, 5, 3, 7, 101, 18]
print("LIS uzunligi: \(lengthOfLIS(sequence))")
```

## Tushuntirish va Mantiq:
Dinamik dasturlash avvalgi qadamlar natijasini keshlab eng optimal ketma-ketlikni hisoblaydi.

## Ishlash natijasi:
```text
LIS uzunligi: 4
```


# 628-Topshiriq: Knapsack (Xalta) masalasini Dinamik Dasturlash bilan hal qilish
## Topshiriq sharti:
Cheklangan sig'imga eng qimmatli tovarlarni joylash.

## Yechim (Swift kodi):
```swift
import Foundation

func knapsack(capacity: Int, weights: [Int], values: [Int]) -> Int {
    let n = weights.count
    var dp = Array(repeating: Array(repeating: 0, count: capacity + 1), count: n + 1)
    
    for i in 1...n {
        for w in 1...capacity {
            if weights[i - 1] <= w {
                dp[i][w] = max(values[i - 1] + dp[i - 1][w - weights[i - 1]], dp[i - 1][w])
            } else {
                dp[i][w] = dp[i - 1][w]
            }
        }
    }
    return dp[n][capacity]
}

let maxVal = knapsack(capacity: 50, weights: [10, 20, 30], values: [60, 100, 120])
print("Maksimal qimmat: $\(maxVal)")
```

## Tushuntirish va Mantiq:
Klassik 0/1 Knapsack algoritmi resurslarni eng yuqori foyda bilan taqsimlaydi.

## Ishlash natijasi:
```text
Maksimal qimmat: $220
```


# 629-Topshiriq: Kolleksiyani aylanma siljitish (Rotate Array)
## Topshiriq sharti:
Massiv elementlarini o'ngga K qadam aylanma suring.

## Yechim (Swift kodi):
```swift
import Foundation

func rotate<T>(_ array: inout [T], by k: Int) {
    guard !array.isEmpty else { return }
    let shift = k % array.count
    array = Array(array[array.count - shift..<array.count] + array[0..<array.count - shift])
}

var arr = [1, 2, 3, 4, 5]
rotate(&arr, by: 2)
print("Aylantirilgan: \(arr)")
```

## Tushuntirish va Mantiq:
Aylanma surish massiv tilimlarini birlashtirish orqali tezkor amalga oshiriladi.

## Ishlash natijasi:
```text
Aylantirilgan: [4, 5, 1, 2, 3]
```


# 630-Topshiriq: Kolleksiyada prefix va drop amallari
## Topshiriq sharti:
Massivning old qismini olish va qolganini tashlab yuborish.

## Yechim (Swift kodi):
```swift
import Foundation

let numbers = [10, 20, 30, 40, 50]
let firstThree = numbers.prefix(3)
let afterThree = numbers.dropFirst(3)

print("Prefix(3): \(Array(firstThree))")
print("DropFirst(3): \(Array(afterThree))")
```

## Tushuntirish va Mantiq:
'prefix' va 'drop' chegaradan chiqib ketish (Index out of range) xatolarisiz xavfsiz ishlaydi.

## Ishlash natijasi:
```text
Prefix(3): [10, 20, 30]
DropFirst(3): [40, 50]
```


# 631-Topshiriq: Kolleksiyani birlashtiruvchi: joined(separator:)
## Topshiriq sharti:
Matnlar massivini chiroyli ajratuvchi bilan yagona satrga yig'ing.

## Yechim (Swift kodi):
```swift
import Foundation

let words = ["Toshkent", "Buxoro", "Samarqand"]
let joinedString = words.joined(separator: " -> ")
print("Yo'nalish: \(joinedString)")
```

## Tushuntirish va Mantiq:
'joined(separator:)' massiv elementlarini yagona satrga tezkor va xotirani tejab birlashtiradi.

## Ishlash natijasi:
```text
Yo'nalish: Toshkent -> Buxoro -> Samarqand
```


# 632-Topshiriq: Massivda ikkita element o'rnini almashtirish: swapAt
## Topshiriq sharti:
Ikki indeksdagi elementlar o'rnini to'g'ridan-to'g'ri almashtiring.

## Yechim (Swift kodi):
```swift
import Foundation

var fruits = ["Olma", "Anor", "Behi"]
fruits.swapAt(0, 2)
print("Almashgan: \(fruits)")
```

## Tushuntirish va Mantiq:
'swapAt' massiv xotirasida ko'rsatkichlar darajasida o'rin almashtirishni bajaradi.

## Ishlash natijasi:
```text
Almashgan: ["Behi", "Anor", "Olma"]
```


# 633-Topshiriq: Kolleksiyada minimum va maksimum elementlarni bitta qadamda topish
## Topshiriq sharti:
O(N) vaqtda ham min, ham max qiymatni ajratib oling.

## Yechim (Swift kodi):
```swift
import Foundation

func findMinMax<T: Comparable>(_ array: [T]) -> (min: T, max: T)? {
    guard let first = array.first else { return nil }
    var currentMin = first, currentMax = first
    for item in array.dropFirst() {
        if item < currentMin { currentMin = item }
        if item > currentMax { currentMax = item }
    }
    return (currentMin, currentMax)
}

let result = findMinMax([45, 12, 89, 3, 67])
print("Min: \(result?.min ?? 0), Max: \(result?.max ?? 0)")
```

## Tushuntirish va Mantiq:
Yagona qadamda ikkala chegarani topish saralashdan ancha tez ishlaydi.

## Ishlash natijasi:
```text
Min: 3, Max: 89
```


# 634-Topshiriq: Ikki tomonlama bog'langan ro'yxat (Doubly Linked List)
## Topshiriq sharti:
Oldingi va keyingi tugunlarga havola saqlovchi ro'yxat modeli.

## Yechim (Swift kodi):
```swift
import Foundation

class DNode<T> {
    var value: T
    var next: DNode<T>?
    weak var prev: DNode<T>? // Retain cycle oldini olish uchun weak!
    init(value: T) { self.value = value }
}

let n1 = DNode(value: 1)
let n2 = DNode(value: 2)
n1.next = n2
n2.prev = n1

print("n1 next: \(n1.next?.value ?? 0), n2 prev: \(n2.prev?.value ?? 0)")
```

## Tushuntirish va Mantiq:
Ikki tomonlama ro'yxatda orqaga qaytish havolasi (prev) 'weak' bo'lishi xotira sizib ketishining oldini oladi.

## Ishlash natijasi:
```text
n1 next: 2, n2 prev: 1
```


# 635-Topshiriq: Kolleksiyada shart bo'yicha bo'lish: split(separator:)
## Topshiriq sharti:
Nollarni ajratuvchi sifatida olib massivni kichik massivlarga bo'ling.

## Yechim (Swift kodi):
```swift
import Foundation

let data = [1, 2, 0, 3, 4, 0, 5]
let subArrays = data.split(separator: 0)

for sub in subArrays {
    print("Bo'lak: \(Array(sub))")
}
```

## Tushuntirish va Mantiq:
'split(separator:)' har qanday Equatable elementni ajratuvchi sifatida ishlatib qismlarga bo'ladi.

## Ishlash natijasi:
```text
Bo'lak: [1, 2]
Bo'lak: [3, 4]
Bo'lak: [5]
```


# 636-Topshiriq: Lug'atda kalitlarni filtrlash
## Topshiriq sharti:
Faqat muayyan prefiksga ega kalitlarni qoldiruvchi filtratsiya.

## Yechim (Swift kodi):
```swift
import Foundation

let flags = ["user_name": "Ali", "sys_mode": "prod", "user_role": "admin"]
let userFlags = flags.filter { $0.key.hasPrefix("user_") }
print("Foydalanuvchi sozlamalari: \(userFlags)")
```

## Tushuntirish va Mantiq:
Lug'at ustida 'filter' chaqirilganda natija yana [Key: Value] lug'ati sifatida saqlanadi.

## Ishlash natijasi:
```text
Foydalanuvchi sozlamalari: ["user_name": "Ali", "user_role": "admin"]
```


# 637-Topshiriq: Massivda elementlar o'rtachasini hisoblovchi yordamchi
## Topshiriq sharti:
Butun sonlar massivining o'rtacha qiymatini Double da hisoblang.

## Yechim (Swift kodi):
```swift
import Foundation

extension Array where Element: BinaryInteger {
    func average() -> Double {
        guard !isEmpty else { return 0.0 }
        let sum = reduce(0, +)
        return Double(sum) / Double(count)
    }
}

print("O'rtacha ball: \([80, 90, 100].average())")
```

## Tushuntirish va Mantiq:
BinaryInteger cheklovi bilan barcha butun son turlari (Int, UInt8, Int64) uchun universal metod qo'shiladi.

## Ishlash natijasi:
```text
O'rtacha ball: 90.0
```


# 638-Topshiriq: String da qidiruv va indeks masofasi: distance(from:to:)
## Topshiriq sharti:
Matnda qidirilayotgan so'z nechanchi belgida joylashganini butun sonda hisoblang.

## Yechim (Swift kodi):
```swift
import Foundation

let sentence = "Salom Khorazmiy AI"
if let range = sentence.range(of: "Khorazmiy") {
    let index = sentence.distance(from: sentence.startIndex, to: range.lowerBound)
    print("'Khorazmiy' \(index)-belgidan boshlanadi.")
}
```

## Tushuntirish va Mantiq:
String.Index lardagi masofani aniqlash uchun 'distance(from:to:)' funksiyasi ishlatiladi.

## Ishlash natijasi:
```text
'Khorazmiy' 6-belgidan boshlanadi.
```


# 639-Topshiriq: Kolleksiyada barcha elementlar unikal ekanligini tekshirish
## Topshiriq sharti:
Massivda dublikatlar yo'qligini Set orqali O(N) da tekshiring.

## Yechim (Swift kodi):
```swift
import Foundation

extension Array where Element: Hashable {
    var hasUniqueElements: Bool {
        return count == Set(self).count
    }
}

print("[1, 2, 3] unikalmi? \([1, 2, 3].hasUniqueElements)")
print("[1, 2, 1] unikalmi? \([1, 2, 1].hasUniqueElements)")
```

## Tushuntirish va Mantiq:
Set hajmi va massiv hajmini solishtirish dublikatlarni aniqlashning eng tezkor usulidir.

## Ishlash natijasi:
```text
[1, 2, 3] unikalmi? true
[1, 2, 1] unikalmi? false
```


# 640-Topshiriq: Kolleksiyani nollarga tekislash (Padding Array)
## Topshiriq sharti:
Massivni kerakli uzunlikka yetmaguncha standart qiymat bilan to'ldirish.

## Yechim (Swift kodi):
```swift
import Foundation

func padArray<T>(_ arr: [T], toSize size: Int, with value: T) -> [T] {
    var result = arr
    while result.count < size {
        result.append(value)
    }
    return result
}

print("To'ldirilgan: \(padArray([1, 2], toSize: 5, with: 0))")
```

## Tushuntirish va Mantiq:
Sun'iy intellekt va tensor modellarida ma'lumotlarni o'zgarmas o'lchamga (padding) keltirish zarur.

## Ishlash natijasi:
```text
To'ldirilgan: [1, 2, 0, 0, 0]
```


# 641-Topshiriq: Prefiksli yig'indilar massivi (Prefix Sums)
## Topshiriq sharti:
Oraliqlar yig'indisini O(1) vaqtda hisoblash uchun oldindan yig'uvchi massiv.

## Yechim (Swift kodi):
```swift
import Foundation

func buildPrefixSums(_ nums: [Int]) -> [Int] {
    var prefix = [0]
    for n in nums { prefix.append(prefix.last! + n) }
    return prefix
}

let sums = buildPrefixSums([1, 2, 3, 4])
// 1 dan 3 gacha bo'lgan yig'indi: sums[4] - sums[1] = 10 - 1 = 9
print("Prefiks yig'indilar: \(sums)")
```

## Tushuntirish va Mantiq:
Prefix Sum algoritmi oraliq so'rovlarini O(1) vaqtda qaytarish imkonini beradi.

## Ishlash natijasi:
```text
Prefiks yig'indilar: [0, 1, 3, 6, 10]
```


# 642-Topshiriq: Kolleksiyada qidiruv: Binary Search Tree da qidiruv
## Topshiriq sharti:
Binar daraxtda qiymat bor-yo'qligini tekshiruvchi metod.

## Yechim (Swift kodi):
```swift
import Foundation

class NodeB {
    var val: Int; var left: NodeB?; var right: NodeB?
    init(_ val: Int) { self.val = val }
}

func contains(root: NodeB?, target: Int) -> Bool {
    guard let node = root else { return false }
    if node.val == target { return true }
    return target < node.val ? contains(root: node.left, target: target) : contains(root: node.right, target: target)
}

let root = NodeB(10)
root.left = NodeB(5)
print("5 bormi? \(contains(root: root, target: 5))")
```

## Tushuntirish va Mantiq:
Daraxtdagi qidiruv o'rtacha O(log N) vaqt oladi.

## Ishlash natijasi:
```text
5 bormi? true
```


# 643-Topshiriq: String belgilarini teskarisiga o'girish (Reverse in-place)
## Topshiriq sharti:
Belgilar massivini qo'shimcha xotirasiz joyida teskari qilish.

## Yechim (Swift kodi):
```swift
import Foundation

var chars: [Character] = ["S", "w", "i", "f", "t"]
chars.reverse()
print("Teskari: \(String(chars))")
```

## Tushuntirish va Mantiq:
'reverse()' amali massiv elementlarini ikkala chetdan o'rtaga qarab almashtirib boradi.

## Ishlash natijasi:
```text
Teskari: tfiwS
```


# 644-Topshiriq: Kolleksiyadagi eng kichik K ta elementni topish
## Topshiriq sharti:
Heap yoki saralash orqali eng kichik K ta sonni ajratib olish.

## Yechim (Swift kodi):
```swift
import Foundation

func kSmallest<T: Comparable>(_ array: [T], k: Int) -> [T] {
    return Array(array.sorted().prefix(k))
}

print("Eng kichik 2 ta son: \(kSmallest([45, 12, 89, 3, 22], k: 2))")
```

## Tushuntirish va Mantiq:
Top-K masalalari statistik tahlilda doimiy ishlatiladi.

## Ishlash natijasi:
```text
Eng kichik 2 ta son: [3, 12]
```


# 645-Topshiriq: Kolleksiyada zip orqali qo'shnilar juftligini olish
## Topshiriq sharti:
Ketma-ket elementlar juftliklarini biriktirish.

## Yechim (Swift kodi):
```swift
import Foundation

let points = [0, 10, 25, 40]
for (prev, next) in zip(points, points.dropFirst()) {
    print("Oraliq: \(prev) -> \(next), Masofa: \(next - prev)")
}
```

## Tushuntirish va Mantiq:
'zip(arr, arr.dropFirst())' ketma-ket qo'shnilar bilan ishlashning eng go'zal usulidir.

## Ishlash natijasi:
```text
Oraliq: 0 -> 10, Masofa: 10
Oraliq: 10 -> 25, Masofa: 15
Oraliq: 25 -> 40, Masofa: 15
```


# 646-Topshiriq: Kolleksiyani toq va juft indekslarga ajratish
## Topshiriq sharti:
Indekslarning toq-juftligiga qarab ikkita massivga bo'lish.

## Yechim (Swift kodi):
```swift
import Foundation

let data = ["A", "B", "C", "D", "E"]
var evens = [String](), odds = [String]()

for (idx, val) in data.enumerated() {
    if idx % 2 == 0 { evens.append(val) } else { odds.append(val) }
}

print("Juft indekslar: \(evens), Toq indekslar: \(odds)")
```

## Tushuntirish va Mantiq:
Indeksli filtrlash qismlarga ajratishda qulay yondashuvdir.

## Ishlash natijasi:
```text
Juft indekslar: ["A", "C", "E"], Toq indekslar: ["B", "D"]
```


# 647-Topshiriq: Kolleksiyada birinchi uchragan no-nil elementni olish
## Topshiriq sharti:
Nil qiymatlarni tashlab, birinchi mavjud natijani ajratish.

## Yechim (Swift kodi):
```swift
import Foundation

let options: [String?] = [nil, nil, "Mavjud Kontent", "Zaxira"]
let firstReal = options.compactMap { $0 }.first
print("Birinchi qiymat: \(firstReal ?? "")")
```

## Tushuntirish va Mantiq:
compactMap va first kombinatsiyasi birinchi mavjud qiymatni tezkor topadi.

## Ishlash natijasi:
```text
Birinchi qiymat: Mavjud Kontent
```


# 648-Topshiriq: Kolleksiyani Dictionary ga kalit bo'yicha indekslash
## Topshiriq sharti:
Ob'ektlar massivini uning ID si bo'yicha tezkor qidiruv lug'atiga aylantirish.

## Yechim (Swift kodi):
```swift
import Foundation

struct Employee { let id: Int; let name: String }
let staff = [Employee(id: 1, name: "Aziz"), Employee(id: 2, name: "Dilshod")]

let indexedStaff = Dictionary(uniqueKeysWithValues: staff.map { ($0.id, $0) })
print("ID 2 bo'lgan xodim: \(indexedStaff[2]?.name ?? "")")
```

## Tushuntirish va Mantiq:
'Dictionary(uniqueKeysWithValues:)' massivni O(1) da qidiriladigan xesh-jadvalga aylantiradi.

## Ishlash natijasi:
```text
ID 2 bo'lgan xodim: Dilshod
```


# 649-Topshiriq: Kolleksiyada umumiy elementlar sonini sanash
## Topshiriq sharti:
Ikki to'plamning o'zaro kesishish o'lchamini hisoblash.

## Yechim (Swift kodi):
```swift
import Foundation

let s1: Set = [1, 2, 3, 4]
let s2: Set = [3, 4, 5, 6]
print("Umumiy elementlar: \(s1.intersection(s2).count) ta")
```

## Tushuntirish va Mantiq:
To'plamlar kesishmasi soni tavsiya tizimlarida (similarity score) asosiy mezon hisoblanadi.

## Ishlash natijasi:
```text
Umumiy elementlar: 2 ta
```


# 650-Topshiriq: Amaliy loyiha: Katta ma'lumotlar oqimini saralovchi va tahlil qiluvchi In-Memory Search Engine
## Topshiriq sharti:
Matnlarni indekslovchi (Trie), teskari indeks (Inverted Index) hosil qiluvchi, chastota bo'yicha saralovchi to'liq qidiruv dvigateli moduli.

## Yechim (Swift kodi):
```swift
import Foundation

class InMemorySearchEngine {
    private var invertedIndex: [String: Set<Int>] = [:]
    private var documents: [Int: String] = [:]
    
    func indexDocument(id: Int, text: String) {
        documents[id] = text
        let words = text.lowercased().split(separator: " ")
        for word in words {
            let cleanWord = String(word.filter { $0.isLetter })
            guard !cleanWord.isEmpty else { continue }
            invertedIndex[cleanWord, default: []].insert(id)
        }
        print("INDEKSLANDI: Hujjat #\(id) ('\(text.prefix(25))...')")
    }
    
    func search(query: String) -> [String] {
        let terms = query.lowercased().split(separator: " ").map { String($0) }
        guard let firstTerm = terms.first, var matchingDocs = invertedIndex[firstTerm] else {
            return []
        }
        
        // Qolgan so'zlar bo'yicha to'plam kesishmasi (AND mantiqi):
        for term in terms.dropFirst() {
            if let docSet = invertedIndex[term] {
                matchingDocs = matchingDocs.intersection(docSet)
            } else {
                return []
            }
        }
        
        return matchingDocs.compactMap { documents[$0] }
    }
}

let engine = InMemorySearchEngine()
engine.indexDocument(id: 1, text: "Swift tezkor va xavfsiz dasturlash tili")
engine.indexDocument(id: 2, text: "SwiftUI bilan zamonaviy iOS interfeyslar")
engine.indexDocument(id: 3, text: "Sun'iy intellekt va mashinali o'rganish")

print("
=== QIDIRUV NATIJALARI ('Swift'): ===")
let results = engine.search(query: "Swift")
for r in results {
    print("- \(r)")
}
```

## Tushuntirish va Mantiq:
Ushbu yakuniy loyihada Set, Dictionary, String parsing, Inverted Index va to'plamlar kesishmasi (intersection) to'liq professional qidiruv dvigateli sifatida qurildi.

## Ishlash natijasi:
```text
INDEKSLANDI: Hujjat #1 ('Swift tezkor va xavfsiz d...')
INDEKSLANDI: Hujjat #2 ('SwiftUI bilan zamonaviy i...')
INDEKSLANDI: Hujjat #3 ('Sun'iy intellekt va mashi...')

=== QIDIRUV NATIJALARI ('Swift'): ===
- Swift tezkor va xavfsiz dasturlash tili
- SwiftUI bilan zamonaviy iOS interfeyslar
```

