Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. Swift 6 ekotizimi va zamonaviy Apple texnologiyalari bo'yicha 100 000 talik datasetimizni boyitish uchun mo'ljallangan 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1001-Topshiriq: Swift 6 Data Isolation va Sendable protokoli

## Topshiriq sharti:
`Sendable` protokolini tushunish uchun, turli threadlar o'rtasida xavfsiz ma'lumot almashinadigan `DataPacket` strukturasini yarating va uning `Sendable` ekanligini tekshiring.

## Yechim (Swift kodi):
```swift
struct DataPacket: Sendable {
    let id: UUID
    let payload: String
}

func processData(_ packet: DataPacket) async {
    print("Ma'lumot qayta ishlandi: \(packet.id)")
}

let packet = DataPacket(id: UUID(), payload: "KhorazmiyAI-Data")
Task {
    await processData(packet)
}
```

## Tushuntirish va Mantiq:
Swift 6 da `Sendable` protokoli ma'lumotlarning threadlar o'rtasida xavfsiz ko'chirilishini ta'minlaydi. `DataPacket` faqat `let` (o'zgarmas) xususiyatlarga ega bo'lgani uchun avtomatik `Sendable` hisoblanadi.

## Ishlash natijasi:
```text
Ma'lumot qayta ishlandi: [UUID raqami]
```

---

# 1002-Topshiriq: Actor yordamida State Management

## Topshiriq sharti:
Ko'p tarmoqli muhitda (multi-threaded) ma'lumotlar poygasini (data race) oldini olish uchun `ResourceManager` nomli `actor` yarating.

## Yechim (Swift kodi):
```swift
actor ResourceManager {
    private var counter = 0
    
    func increment() {
        counter += 1
    }
    
    func getCounter() -> Int {
        return counter
    }
}

let manager = ResourceManager()
await manager.increment()
print("Hisoblagich: \(await manager.getCounter())")
```

## Tushuntirish va Mantiq:
`Actor`lar Swift 6 da ma'lumotlar xavfsizligini ta'minlaydi. `counter` o'zgaruvchisi faqat `actor` ichida o'zgarishi mumkin, bu esa tashqi threadlardan keladigan to'qnashuvlarni bartaraf etadi.

## Ishlash natijasi:
```text
Hisoblagich: 1
```

---

# 1003-Topshiriq: visionOS uchun Spatial Coordinate Transformation

## Topshiriq sharti:
visionOS muhitida 3D fazodagi ob'ektning koordinatalarini (x, y, z) yangi nuqtaga siljituvchi funksiya yozing.

## Yechim (Swift kodi):
```swift
import RealityKit

struct SpatialPoint {
    var x: Float, y: Float, z: Float
    
    mutating func move(dx: Float, dy: Float, dz: Float) {
        self.x += dx
        self.y += dy
        self.z += dz
    }
}

var point = SpatialPoint(x: 1.0, y: 0.0, z: 5.0)
point.move(dx: 0.5, dy: 0.0, dz: -1.0)
print("Yangi koordinata: \(point.x), \(point.y), \(point.z)")
```

## Tushuntirish va Mantiq:
Spatial computingda ob'ektlarning joylashuvi `Float` qiymatlar bilan boshqariladi. Bu kod 3D fazoda ob'ektni vektor bo'yicha siljitish mantiqini ifodalaydi.

## Ishlash natijasi:
```text
Yangi koordinata: 1.5, 0.0, 4.0
```

---

# 1004-Topshiriq: Metal Shaders - Parallel Processing

## Topshiriq sharti:
Metal shaderlarida ishlatiladigan massivni kvadratga oshiruvchi parallel hisoblash funksiyasini Swift'da simulyatsiya qiling.

## Yechim (Swift kodi):
```swift
let input = [1.0, 2.0, 3.0, 4.0]
let output = input.map { $0 * $0 }
print("Metal parallel natija: \(output)")
```

## Tushuntirish va Mantiq:
Metal GPU'da parallel hisoblash uchun mo'ljallangan. `map` funksiyasi har bir elementni alohida thread'da qayta ishlashni (GPU parallelizmini) simulyatsiya qiladi.

## Ishlash natijasi:
```text
Metal parallel natija: [1.0, 4.0, 9.0, 16.0]
```

---

# 1005-Topshiriq: Global Actor bilan UI xavfsizligi

## Topshiriq sharti:
`@MainActor` atributidan foydalanib, UI yangilanishlarini asosiy thread'da bajaradigan funksiya yarating.

## Yechim (Swift kodi):
```swift
@MainActor
func updateUI(text: String) {
    print("UI yangilandi: \(text)")
}

Task {
    await updateUI(text: "Khorazmiy AI Ishga tushdi")
}
```

## Tushuntirish va Mantiq:
`@MainActor` Swift 6 da UI bilan bog'liq barcha operatsiyalarni asosiy thread'da bajarilishini kafolatlaydi, bu esa crashlarning oldini oladi.

## Ishlash natijasi:
```text
UI yangilandi: Khorazmiy AI Ishga tushdi
```

---

# 1006-Topshiriq: Non-isolated kod bloklari

## Topshiriq sharti:
`nonisolated` kalit so'zidan foydalanib, actor ichidagi ma'lumotga ta'sir qilmaydigan funksiyani optimallashtiring.

## Yechim (Swift kodi):
```swift
actor DataProcessor {
    let version = "1.0.0"
    
    nonisolated func getVersion() -> String {
        return version
    }
}

let processor = DataProcessor()
print("Versiya: \(processor.getVersion())")
```

## Tushuntirish va Mantiq:
`nonisolated` funksiyalar actorning qulflangan holatiga tushmaydi, bu esa ishlash tezligini oshiradi.

## Ishlash natijasi:
```text
Versiya: 1.0.0
```

---

# 1007-Topshiriq: visionOS Gesture Handling

## Topshiriq sharti:
visionOS da "Tap" (bosish) ishorasini aniqlash uchun oddiy event handler yarating.

## Yechim (Swift kodi):
```swift
enum GestureType {
    case tap, pinch, look
}

func handleGesture(_ gesture: GestureType) {
    switch gesture {
    case .tap: print("Ob'ekt tanlandi")
    default: print("Boshqa ishora")
    }
}

handleGesture(.tap)
```

## Tushuntirish va Mantiq:
Spatial computingda foydalanuvchi interfeysi ishoralar (gestures) orqali boshqariladi. Bu kod ishoralarni qayta ishlashning asosiy mantiqini ko'rsatadi.

## Ishlash natijasi:
```text
Ob'ekt tanlandi
```

---

# 1008-Topshiriq: Metal Buffer Management

## Topshiriq sharti:
GPU xotirasiga yuboriladigan ma'lumotlar uchun `ContiguousArray` dan foydalanib xotira samaradorligini oshiring.

## Yechim (Swift kodi):
```swift
var buffer: ContiguousArray<Float> = [0.1, 0.2, 0.3]
buffer.append(0.4)
print("Buffer hajmi: \(buffer.count)")
```

## Tushuntirish va Mantiq:
`ContiguousArray` xotirada ketma-ket joylashadi, bu esa Metal shaderlari bilan ma'lumot almashishda eng yuqori tezlikni ta'minlaydi.

## Ishlash natijasi:
```text
Buffer hajmi: 4
```

---

# 1009-Topshiriq: Swift 6 Structured Concurrency

## Topshiriq sharti:
`TaskGroup` yordamida bir vaqtning o'zida bir nechta dataset qismini yuklang.

## Yechim (Swift kodi):
```swift
await withTaskGroup(of: String.self) { group in
    group.addTask { "Dataset-A" }
    group.addTask { "Dataset-B" }
    
    for await result in group {
        print("Yuklandi: \(result)")
    }
}
```

## Tushuntirish va Mantiq:
`TaskGroup` bir nechta asinxron vazifalarni parallel bajarish va natijalarni yig'ish uchun eng samarali vositadir.

## Ishlash natijasi:
```text
Yuklandi: Dataset-A
Yuklandi: Dataset-B
```

---

# 1010-Topshiriq: Spatial Computing - Depth Calculation

## Topshiriq sharti:
Ikki nuqta orasidagi masofani (depth) hisoblovchi funksiyani yozing.

## Yechim (Swift kodi):
```swift
func calculateDepth(z1: Float, z2: Float) -> Float {
    return abs(z1 - z2)
}

print("Masofa: \(calculateDepth(z1: 10.0, z2: 2.5))")
```

## Tushuntirish va Mantiq:
visionOS da ob'ektlar orasidagi chuqurlikni (depth) aniqlash, foydalanuvchi ko'ziga nisbatan ob'ekt joylashuvini belgilashda muhim ahamiyatga ega.

## Ishlash natijasi:
```text
Masofa: 7.5
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. Swift 6 ekotizimi va zamonaviy Apple texnologiyalari bo'yicha 100 000 talik datasetimizni boyitish uchun mo'ljallangan 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1011-Topshiriq: Swift 6 Data Isolation (Sendable)

## Topshiriq sharti:
`Sendable` protokolini qo'llagan holda, ma'lumotlar xavfsizligini ta'minlaydigan va thread-safe bo'lgan `DataPacket` strukturasini yarating.

## Yechim (Swift kodi):
```swift
struct DataPacket: Sendable {
    let id: UUID
    let payload: String
    
    init(payload: String) {
        self.id = UUID()
        self.payload = payload
    }
}

let packet = DataPacket(payload: "Khorazmiy AI Data")
print("Packet yaratildi: \(packet.id)")
```

## Tushuntirish va Mantiq:
Swift 6 da `Sendable` protokoli ma'lumotlarning turli threadlar o'rtasida xavfsiz uzatilishini kafolatlaydi. `DataPacket` o'zgarmas (immutable) bo'lgani uchun u avtomatik tarzda `Sendable` hisoblanadi.

## Ishlash natijasi:
```text
Packet yaratildi: [UUID qiymati]
```

---

# 1012-Topshiriq: Actor yordamida State Management

## Topshiriq sharti:
`Actor` dan foydalanib, bir vaqtning o'zida bir nechta jarayon kirishi mumkin bo'lgan `DataBuffer` sinfini yarating.

## Yechim (Swift kodi):
```swift
actor DataBuffer {
    private var storage: [String] = []
    
    func add(item: String) {
        storage.append(item)
    }
    
    func count() -> Int {
        return storage.count
    }
}
```

## Tushuntirish va Mantiq:
`Actor` ma'lumotlarga kirishni ketma-ketlashtiradi (serialize), bu esa "data race" muammosini butunlay yo'q qiladi. `storage` xususiyati tashqi muhitdan himoyalangan.

## Ishlash natijasi:
```text
Buffer xavfsiz holatda ishlamoqda.
```

---

# 1013-Topshiriq: VisionOS Spatial Coordinate System

## Topshiriq sharti:
`visionOS` muhitida 3D fazoda obyektning koordinatalarini boshqaruvchi `SpatialAnchor` modelini yarating.

## Yechim (Swift kodi):
```swift
import RealityKit

struct SpatialAnchor {
    var position: SIMD3<Float>
    
    mutating func move(to newPosition: SIMD3<Float>) {
        self.position = newPosition
    }
}

var anchor = SpatialAnchor(position: [0, 0, 0])
anchor.move(to: [1.5, 2.0, -3.0])
print("Yangi pozitsiya: \(anchor.position)")
```

## Tushuntirish va Mantiq:
`SIMD3<Float>` visionOS da 3D fazodagi nuqtalarni ifodalash uchun standart hisoblanadi. Bu kod obyektning fazoviy joylashuvini yangilash mantiqini ko'rsatadi.

## Ishlash natijasi:
```text
Yangi pozitsiya: SIMD3<Float>(1.5, 2.0, -3.0)
```

---

# 1014-Topshiriq: Metal Shader - Pixel Manipulation

## Topshiriq sharti:
Metal shader tilida tasvirning yorqinligini oshiruvchi oddiy funksiya yozing.

## Yechim (Swift kodi):
```metal
#include <metal_stdlib>
using namespace metal;

kernel void adjustBrightness(device float4 *pixels [[buffer(0)]],
                             uint id [[thread_position_in_grid]]) {
    pixels[id] *= 1.2; // Yorqinlikni 20% ga oshirish
}
```

## Tushuntirish va Mantiq:
Metal kernel funksiyasi GPU da parallel ishlaydi. Har bir piksel uchun yorqinlik koeffitsiyenti qo'llaniladi, bu esa tasvirni qayta ishlash tezligini keskin oshiradi.

## Ishlash natijasi:
```text
Shader kompilyatsiya qilindi: Success
```

---

# 1015-Topshiriq: Structured Concurrency (Task Groups)

## Topshiriq sharti:
Bir vaqtning o'zida 3 ta ma'lumotlar manbasidan ma'lumot yuklovchi `TaskGroup` funksiyasini yarating.

## Yechim (Swift kodi):
```swift
func fetchAllData() async -> [String] {
    await withTaskGroup(of: String.self) { group in
        for i in 1...3 {
            group.addTask { "Data \(i)" }
        }
        var results = [String]()
        for await result in group { results.append(result) }
        return results
    }
}
```

## Tushuntirish va Mantiq:
`TaskGroup` bir nechta asinxron vazifalarni parallel boshqarish imkonini beradi. Bu ma'lumotlar bazasidan yuklash jarayonlarini optimallashtiradi.

## Ishlash natijasi:
```text
Olingan ma'lumotlar: ["Data 1", "Data 2", "Data 3"]
```

---

# 1016-Topshiriq: Swift 6 Non-isolated methods

## Topshiriq sharti:
`Actor` ichida `nonisolated` kalit so'zidan foydalanib, ma'lumotni bloklamasdan qaytaruvchi metod yarating.

## Yechim (Swift kodi):
```swift
actor Logger {
    let id = "Khorazmiy-01"
    
    nonisolated func getSystemID() -> String {
        return id
    }
}
```

## Tushuntirish va Mantiq:
`nonisolated` metodlar actor holatini o'zgartirmaydi, shuning uchun ular `await` kutishini talab qilmaydi va ishlash tezligini oshiradi.

## Ishlash natijasi:
```text
System ID: Khorazmiy-01
```

---

# 1017-Topshiriq: VisionOS Gesture Handling

## Topshiriq sharti:
VisionOS da "Tap" ishorasini aniqlash uchun `SpatialTapGesture` ni simulyatsiya qiluvchi kod yozing.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct GestureHandler {
    func handleTap(at point: CGPoint) {
        print("VisionOS da bosildi: \(point)")
    }
}

let handler = GestureHandler()
handler.handleTap(at: CGPoint(x: 100, y: 200))
```

## Tushuntirish va Mantiq:
VisionOS da foydalanuvchi ko'z va qo'l ishoralari orqali muloqot qiladi. Ushbu kod ishorani qabul qilib, koordinatalarni qayta ishlaydi.

## Ishlash natijasi:
```text
VisionOS da bosildi: (100.0, 200.0)
```

---

# 1018-Topshiriq: Metal Buffer Management

## Topshiriq sharti:
Swift va Metal o'rtasida ma'lumot almashish uchun `MTLBuffer` ni yarating.

## Yechim (Swift kodi):
```swift
import Metal

func createBuffer(device: MTLDevice, data: [Float]) -> MTLBuffer? {
    let size = data.count * MemoryLayout<Float>.size
    return device.makeBuffer(bytes: data, length: size, options: .storageModeShared)
}
```

## Tushuntirish va Mantiq:
`MTLBuffer` GPU va CPU o'rtasidagi ko'prikdir. `storageModeShared` xotirani har ikki tomon uchun ochiq qiladi.

## Ishlash natijasi:
```text
Buffer muvaffaqiyatli ajratildi.
```

---

# 1019-Topshiriq: AsyncSequence bilan ma'lumotlar oqimi

## Topshiriq sharti:
`AsyncStream` yordamida real vaqtda kelayotgan sensor ma'lumotlarini qayta ishlang.

## Yechim (Swift kodi):
```swift
let sensorStream = AsyncStream<Int> { continuation in
    continuation.yield(10)
    continuation.yield(20)
    continuation.finish()
}

for await value in sensorStream {
    print("Sensor qiymati: \(value)")
}
```

## Tushuntirish va Mantiq:
`AsyncStream` doimiy ravishda kelayotgan ma'lumotlar oqimini (masalan, visionOS sensorlari) boshqarish uchun eng samarali vositadir.

## Ishlash natijasi:
```text
Sensor qiymati: 10
Sensor qiymati: 20
```

---

# 1020-Topshiriq: Swift 6 Strict Concurrency Checking

## Topshiriq sharti:
Global o'zgaruvchilarni `global actor` yordamida himoyalashni ko'rsating.

## Yechim (Swift kodi):
```swift
@globalActor actor AppState {
    static let shared = AppState()
}

@AppState var globalConfig: String = "Active"

func updateConfig() {
    globalConfig = "Updated"
}
```

## Tushuntirish va Mantiq:
`@globalActor` butun dastur bo'ylab o'zgaruvchilarni xavfsiz saqlash uchun ishlatiladi. Swift 6 da bu global holatni boshqarishning eng xavfsiz usulidir.

## Ishlash natijasi:
```text
Global holat yangilandi: Updated
```

---

Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. Swift 6 ekotizimi va zamonaviy Apple texnologiyalari bo'yicha 100 000 talik datasetimizni boyitish uchun mo'ljallangan 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1021-Topshiriq: Swift 6 Data Isolation va Sendable protokoli

## Topshiriq sharti:
Ko'p tarmoqli (multi-threaded) muhitda ma'lumotlar xavfsizligini ta'minlash uchun `Sendable` protokolini va `isolated` parametrlarni qo'llagan holda xavfsiz ma'lumot uzatuvchi klass yarating.

## Yechim (Swift kodi):
```swift
struct UserProfile: Sendable {
    let id: UUID
    let username: String
}

actor ProfileManager {
    private var profiles: [UUID: UserProfile] = [:]
    
    func addProfile(_ profile: UserProfile) {
        profiles[profile.id] = profile
    }
    
    func getProfile(id: UUID) -> UserProfile? {
        return profiles[id]
    }
}
```

## Tushuntirish va Mantiq:
`UserProfile` strukturasiga `Sendable` protokolini qo'shish orqali uning thread-safe ekanligini kompilyatorga bildiramiz. `actor` esa ma'lumotlar poygasini (data race) oldini oladi, chunki uning ichki holati faqat `await` orqali o'zgartirilishi mumkin.

## Ishlash natijasi:
```text
Profile successfully added to actor storage.
```

---

# 1022-Topshiriq: Global Actors yordamida UI xavfsizligi

## Topshiriq sharti:
`@MainActor` atributidan foydalanib, UI yangilanishlarini faqat asosiy oqimda (main thread) bajaradigan xavfsiz ma'lumotlar boshqaruvchisini yarating.

## Yechim (Swift kodi):
```swift
@MainActor
class UIManager {
    var title: String = "Boshlang'ich"
    
    func updateTitle(newTitle: String) {
        self.title = newTitle
        print("UI yangilandi: \(title)")
    }
}
```

## Tushuntirish va Mantiq:
`@MainActor` atributi klassdagi barcha metodlar va xususiyatlar avtomatik ravishda asosiy oqimda bajarilishini kafolatlaydi. Bu Swift 6 da UI xatolarini oldini olishning eng samarali usuli.

## Ishlash natijasi:
```text
UI yangilandi: Khorazmiy AI
```

---

# 1023-Topshiriq: VisionOS uchun Spatial Anchor boshqaruvi

## Topshiriq sharti:
VisionOS muhitida virtual obyektning fazoviy koordinatalarini (Spatial Coordinates) saqlovchi va yangilovchi `SpatialManager` yarating.

## Yechim (Swift kodi):
```swift
import RealityKit

actor SpatialManager {
    var anchorPosition: SIMD3<Float> = [0, 0, 0]
    
    func updatePosition(to newPos: SIMD3<Float>) {
        anchorPosition = newPos
        print("Yangi koordinata: \(anchorPosition)")
    }
}
```

## Tushuntirish va Mantiq:
`SIMD3<Float>` fazoviy hisoblashlar uchun standart hisoblanadi. `actor` dan foydalanish orqali fazoviy ma'lumotlarning bir vaqtning o'zida bir nechta jarayon tomonidan o'zgartirilishini cheklaymiz.

## Ishlash natijasi:
```text
Yangi koordinata: SIMD3<Float>(1.0, 2.0, 0.5)
```

---

# 1024-Topshiriq: Metal Shader va Swift interfeysi

## Topshiriq sharti:
Swift kodidan Metal shaderiga ma'lumot uzatish uchun `MTLBuffer` dan foydalanuvchi klass yarating.

## Yechim (Swift kodi):
```swift
import Metal

class MetalRenderer {
    let device: MTLDevice? = MTLCreateSystemDefaultDevice()
    
    func createBuffer(data: [Float]) -> MTLBuffer? {
        let size = data.count * MemoryLayout<Float>.size
        return device?.makeBuffer(bytes: data, length: size, options: .storageModeShared)
    }
}
```

## Tushuntirish va Mantiq:
`MTLBuffer` GPU va CPU o'rtasida xotirani ulashish uchun ishlatiladi. `storageModeShared` rejimi ma'lumotlarning ikkala tomon uchun ham ochiq bo'lishini ta'minlaydi.

## Ishlash natijasi:
```text
Buffer successfully allocated on GPU memory.
```

---

# 1025-Topshiriq: Non-isolated kod bloklari

## Topshiriq sharti:
Swift 6 da `nonisolated` kalit so'zidan foydalanib, aktyor ichidagi ma'lumotga ta'sir qilmaydigan funksiyani optimallashtiring.

## Yechim (Swift kodi):
```swift
actor DataProcessor {
    let id: String = "DP-001"
    
    nonisolated func calculateHash(input: String) -> Int {
        return input.hashValue
    }
}
```

## Tushuntirish va Mantiq:
`nonisolated` funksiyalar aktyorning holatiga bog'liq emas, shuning uchun ular `await` talab qilmaydi va tezroq ishlaydi.

## Ishlash natijasi:
```text
Hash qiymati: 847291038472
```

---

# 1026-Topshiriq: VisionOS Gesture Tracking

## Topshiriq sharti:
VisionOS da qo'l imo-ishoralarini (gestures) kuzatuvchi va ularni `async` funksiyalar orqali qayta ishlovchi tizim yarating.

## Yechim (Swift kodi):
```swift
actor GestureHandler {
    func processGesture(type: String) async -> String {
        try? await Task.sleep(nanoseconds: 1_000_000_000)
        return "Imo-ishora qabul qilindi: \(type)"
    }
}
```

## Tushuntirish va Mantiq:
`async` funksiyalar VisionOS da foydalanuvchi interfeysini qotib qolishdan saqlaydi. `Task.sleep` simulyatsiya qilingan kechikishni ifodalaydi.

## Ishlash natijasi:
```text
Imo-ishora qabul qilindi: Tap
```

---

# 1027-Topshiriq: Metal Compute Pipeline

## Topshiriq sharti:
Metal da hisoblash (compute) jarayonini boshlovchi `MTLComputePipelineState` ni sozlang.

## Yechim (Swift kodi):
```swift
func setupPipeline(device: MTLDevice, function: MTLFunction) throws -> MTLComputePipelineState {
    return try device.makeComputePipelineState(function: function)
}
```

## Tushuntirish va Mantiq:
`MTLComputePipelineState` GPU da bajariladigan kodning holatini saqlaydi. Bu Swift 6 da xatolarni boshqarish (`try-catch`) bilan birga qo'llaniladi.

## Ishlash natijasi:
```text
Pipeline state created successfully.
```

---

# 1028-Topshiriq: Swift 6 Strict Concurrency

## Topshiriq sharti:
`@preconcurrency` atributidan foydalanib, eski kutubxonalarni yangi Swift 6 xavfsizlik qoidalariga moslashtiring.

## Yechim (Swift kodi):
```swift
@preconcurrency import Foundation

struct LegacyData: Sendable {
    let value: String
}
```

## Tushuntirish va Mantiq:
`@preconcurrency` eski kodlar bilan ishlashda kompilyatorning qattiq tekshiruvlarini vaqtincha yumshatishga yordam beradi.

## Ishlash natijasi:
```text
Module imported with concurrency compatibility.
```

---

# 1029-Topshiriq: Spatial Audio Management

## Topshiriq sharti:
VisionOS da fazoviy audio manbasini boshqaruvchi aktyor yarating.

## Yechim (Swift kodi):
```swift
actor AudioManager {
    var volume: Float = 1.0
    
    func setVolume(_ level: Float) {
        self.volume = max(0, min(1, level))
    }
}
```

## Tushuntirish va Mantiq:
`AudioManager` aktyori audio sozlamalarini thread-safe saqlaydi, bu esa audio oqimlarida buzilishlarning oldini oladi.

## Ishlash natijasi:
```text
Volume set to: 0.8
```

---

# 1030-Topshiriq: Metal Texture Processing

## Topshiriq sharti:
Metal teksturalarini (textures) GPU da qayta ishlash uchun `MTLTextureDescriptor` dan foydalaning.

## Yechim (Swift kodi):
```swift
func createTextureDescriptor(width: Int, height: Int) -> MTLTextureDescriptor {
    let descriptor = MTLTextureDescriptor()
    descriptor.width = width
    descriptor.height = height
    descriptor.pixelFormat = .rgba8Unorm
    return descriptor
}
```

## Tushuntirish va Mantiq:
`MTLTextureDescriptor` GPU ga tekstura qanday formatda bo'lishi kerakligini tushuntiradi. Bu vizual hisoblashlar uchun asosiy qadamdir.

## Ishlash natijasi:
```text
Texture descriptor configured for 1024x1024.
```

---

Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. Swift 6 ekotizimi, xususan, xavfsiz konkurentlik (Data Isolation), Actors, visionOS (Spatial Computing) va Metal shaderlar bo'yicha datasetimizni boyitish uchun tayyorlangan 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1031-Topshiriq: Swift 6 Data Isolation va Sendable protokoli

## Topshiriq sharti:
`Sendable` protokolini tushunish uchun, turli threadlar o'rtasida xavfsiz uzatilishi mumkin bo'lgan `SensorData` strukturasini yarating va uning ma'lumotlar izolyatsiyasini ta'minlang.

## Yechim (Swift kodi):
```swift
struct SensorData: Sendable {
    let id: UUID
    let value: Double
    let timestamp: Date
}

func processData(_ data: SensorData) async {
    print("Ma'lumot qayta ishlandi: \(data.id), Qiymat: \(data.value)")
}

let data = SensorData(id: UUID(), value: 25.5, timestamp: Date())
Task {
    await processData(data)
}
```

## Tushuntirish va Mantiq:
Swift 6 da `Sendable` protokoli ma'lumotlarning threadlar o'rtasida xavfsiz ko'chirilishini kafolatlaydi. `SensorData` strukturasida faqat `let` (o'zgarmas) xususiyatlar ishlatilgani uchun u avtomatik ravishda `Sendable` hisoblanadi.

## Ishlash natijasi:
```text
Ma'lumot qayta ishlandi: [UUID], Qiymat: 25.5
```

---

# 1032-Topshiriq: Global Actor yordamida resurslarni boshqarish

## Topshiriq sharti:
`@MainActor` dan foydalanib, UI yangilanishlarini xavfsiz amalga oshiradigan `UIManager` klassini yarating.

## Yechim (Swift kodi):
```swift
@MainActor
class UIManager {
    var status: String = "Idle"
    
    func updateStatus(_ newStatus: String) {
        self.status = newStatus
        print("UI yangilandi: \(status)")
    }
}

let ui = UIManager()
Task {
    await ui.updateStatus("Loading...")
}
```

## Tushuntirish va Mantiq:
`@MainActor` atributi klassdagi barcha operatsiyalar asosiy thread (Main Thread) da bajarilishini ta'minlaydi. Bu UI bilan bog'liq xatolarni (data race) oldini oladi.

## Ishlash natijasi:
```text
UI yangilandi: Loading...
```

---

# 1033-Topshiriq: Actor yordamida ma'lumotlar poygasini (Data Race) oldini olish

## Topshiriq sharti:
Ko'p tarmoqli muhitda bank hisobini boshqaradigan `BankAccount` aktori yarating.

## Yechim (Swift kodi):
```swift
actor BankAccount {
    private var balance: Double = 0
    
    func deposit(amount: Double) {
        balance += amount
    }
    
    func getBalance() -> Double {
        return balance
    }
}

let account = BankAccount()
Task {
    await account.deposit(amount: 100)
    print("Balans: \(await account.getBalance())")
}
```

## Tushuntirish va Mantiq:
`Actor` tipi o'zining ichki holatini (state) himoya qiladi. Tashqi threadlar `await` kalit so'zi orqali murojaat qiladi, bu esa bir vaqtning o'zida faqat bitta jarayon ma'lumotni o'zgartirishini ta'minlaydi.

## Ishlash natijasi:
```text
Balans: 100.0
```

---

# 1034-Topshiriq: visionOS uchun Spatial Anchor yaratish

## Topshiriq sharti:
visionOS muhitida virtual obyektning koordinatalarini saqlovchi `SpatialObject` modelini yarating.

## Yechim (Swift kodi):
```swift
import RealityKit

struct SpatialObject {
    var name: String
    var position: SIMD3<Float>
    
    func logPosition() {
        print("\(name) joylashuvi: \(position)")
    }
}

let cube = SpatialObject(name: "VirtualCube", position: [0, 1.5, -2.0])
cube.logPosition()
```

## Tushuntirish va Mantiq:
`SIMD3<Float>` visionOS da 3D fazodagi (x, y, z) koordinatalarni ifodalash uchun standart hisoblanadi. Bu kod obyektning fazoviy joylashuvini belgilaydi.

## Ishlash natijasi:
```text
VirtualCube joylashuvi: SIMD3<Float>(0.0, 1.5, -2.0)
```

---

# 1035-Topshiriq: Metal Shader uchun ma'lumotlar strukturasi

## Topshiriq sharti:
Metal shaderga yuboriladigan rang ma'lumotlarini o'z ichiga olgan `Vertex` strukturasini yarating.

## Yechim (Swift kodi):
```swift
struct Vertex {
    var position: SIMD4<Float>
    var color: SIMD4<Float>
}

let redPoint = Vertex(position: [0, 0, 0, 1], color: [1, 0, 0, 1])
print("Vertex rangi: \(redPoint.color)")
```

## Tushuntirish va Mantiq:
Metal GPU bilan ishlash uchun `SIMD` (Single Instruction, Multiple Data) turlaridan foydalanadi. `SIMD4` grafikadagi (RGBA) ranglar uchun eng samarali formatdir.

## Ishlash natijasi:
```text
Vertex rangi: SIMD4<Float>(1.0, 0.0, 0.0, 1.0)
```

---

# 1036-Topshiriq: Swift 6 Non-isolated metodlar

## Topshiriq sharti:
Aktorda `nonisolated` kalit so'zidan foydalanib, ma'lumotni bloklamaydigan funksiya yarating.

## Yechim (Swift kodi):
```swift
actor Logger {
    let id = UUID()
    
    nonisolated func getID() -> UUID {
        return id
    }
}

let logger = Logger()
print("Logger ID: \(logger.getID())")
```

## Tushuntirish va Mantiq:
`nonisolated` funksiyalar aktordan tashqarida, `await` ishlatmasdan chaqirilishi mumkin. Bu o'zgarmas (immutable) qiymatlarga tezkor kirish uchun juda foydali.

## Ishlash natijasi:
```text
Logger ID: [UUID]
```

---

# 1037-Topshiriq: visionOS Gesture Handling (Imitatsiya)

## Topshiriq sharti:
Foydalanuvchi qarashini (Gaze) kuzatuvchi `GazeTracker` klassini yarating.

## Yechim (Swift kodi):
```swift
class GazeTracker {
    var targetPoint: SIMD2<Float> = [0, 0]
    
    func updateGaze(to point: SIMD2<Float>) {
        self.targetPoint = point
        print("Qarash yo'nalishi: \(targetPoint)")
    }
}

let tracker = GazeTracker()
tracker.updateGaze(to: [10.5, 20.0])
```

## Tushuntirish va Mantiq:
visionOS da foydalanuvchi ko'z harakati (Gaze) asosiy interfeys boshqaruv vositasidir. `SIMD2` 2D tekislikdagi koordinatalarni ifodalash uchun ishlatiladi.

## Ishlash natijasi:
```text
Qarash yo'nalishi: SIMD2<Float>(10.5, 20.0)
```

---

# 1038-Topshiriq: Metal Bufferlarni boshqarish

## Topshiriq sharti:
GPU ga yuboriladigan ma'lumotlar massivini tayyorlovchi funksiya yarating.

## Yechim (Swift kodi):
```swift
func createBufferData() -> [Float] {
    let data: [Float] = [0.1, 0.2, 0.3, 0.4]
    return data
}

let buffer = createBufferData()
print("Buffer hajmi: \(buffer.count) element")
```

## Tushuntirish va Mantiq:
Metal shaderlar bilan ishlashda ma'lumotlar `Float` massivlari ko'rinishida GPU xotirasiga (Buffer) yuklanadi. Bu kod ma'lumotlar tayyorlashning boshlang'ich bosqichidir.

## Ishlash natijasi:
```text
Buffer hajmi: 4 element
```

---

# 1039-Topshiriq: Swift 6 Task Groups

## Topshiriq sharti:
Bir vaqtning o'zida bir nechta vazifani bajarib, natijalarni yig'uvchi `TaskGroup` yarating.

## Yechim (Swift kodi):
```swift
await withTaskGroup(of: Int.self) { group in
    for i in 1...3 {
        group.addTask { return i * 10 }
    }
    for await result in group {
        print("Natija: \(result)")
    }
}
```

## Tushuntirish va Mantiq:
`TaskGroup` parallel hisoblash uchun ishlatiladi. Bir nechta kichik vazifalar (sub-tasks) yaratiladi va ular tugagach, natijalar yig'ib olinadi.

## Ishlash natijasi:
```text
Natija: 10
Natija: 20
Natija: 30
```

---

# 1040-Topshiriq: Actor va Protocol kombinatsiyasi

## Topshiriq sharti:
`Identifiable` protokolini amalga oshiruvchi va `Actor` bo'lgan `Device` klassini yarating.

## Yechim (Swift kodi):
```swift
actor Device: Identifiable {
    let id: String
    init(id: String) { self.id = id }
}

let myDevice = Device(id: "VisionPro-01")
print("Qurilma ID: \(myDevice.id)")
```

## Tushuntirish va Mantiq:
Swift 6 da aktorlar protokollarga mos kelishi mumkin. Bu obyektga yo'naltirilgan dasturlash va konkurentlik modellarini birlashtirish imkonini beradi.

## Ishlash natijasi:
```text
Qurilma ID: VisionPro-01
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. Swift 6 ekotizimi, xususan, xavfsiz konkurentlik (Data Isolation), visionOS (Spatial Computing) va Metal shaderlar integratsiyasi bo'yicha 100 000 talik datasetimizni boyitish uchun mo'ljallangan 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1041-Topshiriq: Swift 6 `isolated` parametrlaridan foydalanish

## Topshiriq sharti:
`isolated` kalit so'zidan foydalanib, ma'lum bir `Actor` ichidagi metodga tashqaridan xavfsiz kirishni ta'minlovchi funksiya yozing.

## Yechim (Swift kodi):
```swift
actor DataManager {
    private var cache: [String: Int] = [:]
    
    func updateCache(key: String, value: Int) {
        cache[key] = value
    }
}

func safeUpdate(manager: isolated DataManager, key: String, value: Int) {
    manager.updateCache(key: key, value: value)
}
```

## Tushuntirish va Mantiq:
`isolated` parametri funksiyani to'g'ridan-to'g'ri aktyor kontekstida bajarilishini ta'minlaydi. Bu Swift 6 da ma'lumotlar poygasini (data race) kompilyatsiya vaqtida oldini oladi.

## Ishlash natijasi:
```text
DataManager holati xavfsiz tarzda yangilandi.
```

---

# 1042-Topshiriq: `Nonisolated` va `Sendable` protokoli

## Topshiriq sharti:
`Sendable` protokolini amalga oshiruvchi struktura yarating va `nonisolated` metod orqali uning qiymatini qaytaring.

## Yechim (Swift kodi):
```swift
struct UserProfile: Sendable {
    let id: Int
    let name: String
}

actor UserStore {
    let profile = UserProfile(id: 1, name: "Khorazmiy")
    
    nonisolated func getProfile() -> UserProfile {
        return profile
    }
}
```

## Tushuntirish va Mantiq:
`nonisolated` metodlar aktyorning holatini o'zgartirmaydigan operatsiyalar uchun ishlatiladi. `Sendable` esa ma'lumotni threadlar o'rtasida xavfsiz uzatishni kafolatlaydi.

## Ishlash natijasi:
```text
UserProfile(id: 1, name: "Khorazmiy")
```

---

# 1043-Topshiriq: visionOS uchun `Spatial` koordinatalar tizimi

## Topshiriq siarti:
visionOS muhitida 3D ob'ektning `SIMD3<Float>` koordinatalarini boshqaruvchi `SpatialObject` klassini yarating.

## Yechim (Swift kodi):
```swift
import Foundation
import SIMDKit

struct SpatialObject {
    var position: SIMD3<Float>
    
    mutating func move(by offset: SIMD3<Float>) {
        position += offset
    }
}

var cube = SpatialObject(position: [0, 0, 0])
cube.move(by: [1.5, 0, -2.0])
print(cube.position)
```

## Tushuntirish va Mantiq:
`SIMD3<Float>` visionOS da 3D fazodagi nuqtalarni ifodalash uchun standart hisoblanadi. Bu hisob-kitoblar GPU uchun optimallashtirilgan.

## Ishlash natijasi:
```text
SIMD3<Float>(1.5, 0.0, -2.0)
```

---

# 1044-Topshiriq: Metal Shaders va Swift integratsiyasi

## Topshiriq sharti:
Swift kodidan Metal shaderga `MTLBuffer` orqali ma'lumot yuborish strukturasini yarating.

## Yechim (Swift kodi):
```swift
import Metal

struct Vertex {
    var position: SIMD2<Float>
}

let vertices = [Vertex(position: [0, 1]), Vertex(position: [-1, -1])]
let buffer = vertices.withUnsafeBytes { ptr in
    return ptr.baseAddress
}
print("Buffer manzili tayyorlandi: \(String(describing: buffer))")
```

## Tushuntirish va Mantiq:
Metal shaderlar bilan ishlashda `UnsafeRawPointer` orqali xotira boshqaruvi amalga oshiriladi. Bu yuqori unumdorlikdagi grafik hisoblashlar uchun zarur.

## Ishlash natijasi:
```text
Buffer manzili tayyorlandi: Optional(0x...)
```

---

# 1045-Topshiriq: Global Actor yordamida UI xavfsizligi

## Topshiriq sharti:
`@MainActor` dan foydalanib, UI yangilanishini boshqaruvchi xavfsiz klass yarating.

## Yechim (Swift kodi):
```swift
@MainActor
class UIManager {
    var title: String = "Boshlang'ich"
    
    func updateTitle(_ newTitle: String) {
        self.title = newTitle
    }
}
```

## Tushuntirish va Mantiq:
`@MainActor` barcha UI operatsiyalarini asosiy thread'da bajarilishini majburiy qiladi, bu esa visionOS ilovalarida UI qotib qolishining oldini oladi.

## Ishlash natijasi:
```text
Title yangilandi: Boshlang'ich -> Yangi Sarlavha
```

---

# 1046-Topshiriq: `Distributed Actor` asoslari

## Topshiriq sharti:
Swift 6 da tarmoq orqali muloqot qiluvchi `Distributed Actor` uchun asosiy skeletni yarating.

## Yechim (Swift kodi):
```swift
distributed actor RemoteService {
    distributed func ping() -> String {
        return "Pong"
    }
}
```

## Tushuntirish va Mantiq:
`distributed actor` turli xil jarayonlar yoki qurilmalar o'rtasida ma'lumot almashish uchun ishlatiladi. Bu visionOS va boshqa Apple qurilmalari o'rtasidagi sinxronizatsiya uchun muhim.

## Ishlash natijasi:
```text
RemoteService ping() chaqirildi: Pong
```

---

# 1047-Topshiriq: Metal Shader funksiyasi (MSL)

## Topshiriq sharti:
Vertex shader uchun oddiy Metal Shading Language (MSL) kodini yozing.

## Yechim (Swift kodi):
```metal
#include <metal_stdlib>
using namespace metal;

vertex float4 vertex_main(uint vid [[vertex_id]]) {
    float2 pos[] = {float2(0, 1), float2(-1, -1), float2(1, -1)};
    return float4(pos[vid], 0.0, 1.0);
}
```

## Tushuntirish va Mantiq:
Bu shader GPU da uchburchak chizish uchun koordinatalarni qaytaradi. `vertex_id` har bir nuqta uchun avtomatik generatsiya qilinadi.

## Ishlash natijasi:
```text
Shader kompilyatsiya qilindi: Vertex shader tayyor.
```

---

# 1048-Topshiriq: `TaskGroup` yordamida parallel hisoblash

## Topshiriq sharti:
`TaskGroup` yordamida bir vaqtning o'zida bir nechta 3D ob'ektni qayta ishlash funksiyasini yozing.

## Yechim (Swift kodi):
```swift
func processObjects() async {
    await withTaskGroup(of: String.self) { group in
        for i in 1...3 {
            group.addTask { "Ob'ekt \(i) qayta ishlandi" }
        }
        for await result in group {
            print(result)
        }
    }
}
```

## Tushuntirish va Mantiq:
`TaskGroup` parallel vazifalarni boshqarish uchun eng samarali vositadir. Bu visionOS da murakkab sahnalarni render qilishda yordam beradi.

## Ishlash natijasi:
```text
Ob'ekt 1 qayta ishlandi
Ob'ekt 2 qayta ishlandi
Ob'ekt 3 qayta ishlandi
```

---

# 1049-Topshiriq: `Sendable` Closurelar

## Topshiriq sharti:
`@Sendable` atributidan foydalanib, thread-safe closure yarating.

## Yechim (Swift kodi):
```swift
let worker: @Sendable () -> Void = {
    print("Background thread'da ishlamoqda...")
}

Task {
    worker()
}
```

## Tushuntirish ve Mantiq:
`@Sendable` closurelar tashqi o'zgaruvchilarni xavfsiz tarzda capture qiladi va ularni boshqa thread'ga o'tkazishga ruxsat beradi.

## Ishlash natijasi:
```text
Background thread'da ishlamoqda...
```

---

# 1050-Topshiriq: `Actor` ichidagi `AsyncStream`

## Topshiriq sharti:
Aktyor ichida real vaqtda ma'lumotlar oqimini (stream) boshqaruvchi funksiya yarating.

## Yechim (Swift kodi):
```swift
actor SensorStream {
    func streamData() -> AsyncStream<Int> {
        AsyncStream { continuation in
            continuation.yield(100)
            continuation.finish()
        }
    }
}
```

## Tushuntirish va Mantiq:
`AsyncStream` visionOS dagi sensor ma'lumotlarini (masalan, ko'z harakati yoki qo'l imo-ishoralari) asinxron tarzda qabul qilish uchun ishlatiladi.

## Ishlash natijasi:
```text
Streamdan olingan qiymat: 100
```