# 901-Topshiriq: `NavigationStack` Asoslari va Sarlavhalar
## Topshiriq sharti:
SwiftUI-da yangi `NavigationStack` konteyneri va uning sarlavha modifikatorlaridan foydalanishni ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct AsosiyNavigatsiyaView: View {
    var body: some View {
        NavigationStack {
            VStack(spacing: 20) {
                Text("Bosh sahifa kontenti")
                    .font(.body)
            }
            .navigationTitle("Asosiy Oyna")
            .navigationBarTitleDisplayMode(.inline)
        }
    }
}

let nv = AsosiyNavigatsiyaView()
print("NavigationStack bosh sahifasi yaratildi.")
```

## Tushuntirish va Mantiq:
`NavigationStack` (iOS 16+) eski `NavigationView` o'rnini bosuvchi zamonaviy navigatsiya konteyneri bo'lib, unumdorligi yuqori va dasturiy boshqaruvga to'liq moslashgan.

## Ishlash natijasi:
```text
NavigationStack bosh sahifasi yaratildi.
```


# 902-Topshiriq: `NavigationLink(value:)` Bilan Qiymatga Asoslangan Navigatsiya
## Topshiriq sharti:
`NavigationLink` ga qiymat (value) uzatish va uni deklarativ navigatsiya qilish usulini ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct QiymatliNavigatsiyaView: View {
    let shaharlar = ["Toshkent", "Xiva", "Buxoro", "Samarqand"]
    
    var body: some View {
        NavigationStack {
            List(shaharlar, id: \.self) { shahar in
                NavigationLink(shahar, value: shahar)
            }
            .navigationTitle("O'zbekiston Shaharlari")
            .navigationDestination(for: String.self) { shaharNomi in
                Text("Tanlangan shahar: \(shaharNomi)")
                    .font(.title2)
            }
        }
    }
}

let qn = QiymatliNavigatsiyaView()
print("Qiymatga asoslangan NavigationLink yaratildi.")
```

## Tushuntirish va Mantiq:
`NavigationLink(value:)` bosilganda to'g'ridan-to'g'ri yangi View yaratmaydi, balki qiymatni navigatsiya stackiga uzatadi. Qaysi ko'rinish ochilishini esa `.navigationDestination(for:)` hal qiladi.

## Ishlash natijasi:
```text
Qiymatga asoslangan NavigationLink yaratildi.
```


# 903-Topshiriq: Tiplangan Navigatsiya Marshruti (Custom Route Enum)
## Topshiriq sharti:
Ilova marshrutlarini `Hashable` enum yordamida xavfsiz va tiplangan (type-safe) boshqarishni ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

enum Marshrut: Hashable {
    case profil(id: Int)
    case sozlamalar
    case mahsulot(nomi: String, narxi: Double)
}

struct TiplanganMarshrutView: View {
    var body: some View {
        NavigationStack {
            VStack(spacing: 15) {
                NavigationLink("Profilga o'tish", value: Marshrut.profil(id: 42))
                NavigationLink("Sozlamalarga o'tish", value: Marshrut.sozlamalar)
                NavigationLink("iPhone mahsulotiga o'tish", value: Marshrut.mahsulot(nomi: "iPhone 15", narxi: 999.0))
            }
            .navigationDestination(for: Marshrut.self) { marshrut in
                switch marshrut {
                case .profil(let id):
                    Text("Foydalanuvchi profili: #\(id)")
                case .sozlamalar:
                    Text("Sozlamalar ekrani")
                case .mahsulot(let nomi, let narxi):
                    Text("Mahsulot: \(nomi) - $\(narxi)")
                }
            }
        }
    }
}

let tm = TiplanganMarshrutView()
print("Tiplangan Marshrut enum navigatsiyasi qurildi.")
```

## Tushuntirish va Mantiq:
`Hashable` enum marshrutlar orqali ilovadagi barcha mumkin bo'lgan sahifalarni bitta joyda markazlashgan va xavfsiz holda boshqarish mumkin.

## Ishlash natijasi:
```text
Tiplangan Marshrut enum navigatsiyasi qurildi.
```


# 904-Topshiriq: `NavigationPath` Bilan Dasturiy (Programmatic) Navigatsiya
## Topshiriq sharti:
Tugma orqali koddan turib istalgan sahifaga sakrash va navigatsiyani dasturiy boshqarish uchun `NavigationPath` dan foydalaning.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct DasturiyNavigatsiyaView: View {
    @State private var yol = NavigationPath()
    
    var body: some View {
        NavigationStack(path: $yol) {
            VStack {
                Button("1-bosqichga o'tish") {
                    yol.append(1) // Stackga 1 sonini qo'shish
                }
            }
            .navigationDestination(for: Int.self) { qadam in
                VStack {
                    Text("Bosqich raqami: \(qadam)")
                    Button("Keyingi bosqich") {
                        yol.append(qadam + 1)
                    }
                }
            }
        }
    }
}

let dn = DasturiyNavigatsiyaView()
print("NavigationPath dasturiy navigatsiyasi tayyorlandi.")
```

## Tushuntirish va Mantiq:
`NavigationPath` heterogen (turli xil) tiplarni o'zida saqlay oluvchi dinamik to'plam bo'lib, chuqur havolalar (deep links) va marshrutlar ro'yxatini boshqaradi.

## Ishlash natijasi:
```text
NavigationPath dasturiy navigatsiyasi tayyorlandi.
```


# 905-Topshiriq: Bosh Sahifaga Bir Zumda Qaytish (Pop to Root)
## Topshiriq sharti:
Nechta sahifa ichkariga kirilganidan qat'i nazar, bitta harakat bilan bosh sahifaga qaytishni (`path.removeAll()`) ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct PopToRootView: View {
    @State private var navigatsiyaYoli = NavigationPath()
    
    var body: some View {
        NavigationStack(path: $navigatsiyaYoli) {
            VStack {
                Button("Ro'yxatdan o'tishni boshlash") {
                    navigatsiyaYoli.append("Qadam 1")
                }
            }
            .navigationDestination(for: String.self) { qadam in
                VStack(spacing: 20) {
                    Text("Hozirgi manzil: \(qadam)")
                    Button("Keyingi qadam") {
                        navigatsiyaYoli.append("\(qadam) -> Yangi")
                    }
                    Button("Bosh sahifaga qaytish (Pop to Root)") {
                        navigatsiyaYoli.removeLast(navigatsiyaYoli.count)
                    }
                    .foregroundColor(.red)
                }
            }
        }
    }
}

let ptr = PopToRootView()
print("Pop to root mexanizmi muvaffaqiyatli ulandi.")
```

## Tushuntirish va Mantiq:
`navigatsiyaYoli.removeLast(navigatsiyaYoli.count)` stackdagi barcha sahifalarni birdaniga tozalaydi va foydalanuvchini zudlik bilan bosh sahifaga qaytaradi.

## Ishlash natijasi:
```text
Pop to root mexanizmi muvaffaqiyatli ulandi.
```


# 906-Topshiriq: `TabView` Asoslari va Pastki Menyu Barlari
## Topshiriq sharti:
Ilovaning asosiy bo'limlarini pastki paneldan almashtiruvchi `TabView` komponentini yarating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct IlovaAsosiyTabsView: View {
    var body: some View {
        TabView {
            Text("Lenta sahifasi")
                .tabItem {
                    Label("Lenta", systemImage: "house")
                }
            
            Text("Qidiruv sahifasi")
                .tabItem {
                    Label("Qidiruv", systemImage: "magnifyingglass")
                }
            
            Text("Profil sahifasi")
                .tabItem {
                    Label("Profil", systemImage: "person")
                }
        }
    }
}

let tabs = IlovaAsosiyTabsView()
print("TabView komponenti yaratildi.")
```

## Tushuntirish va Mantiq:
`TabView` iOS-dagi UITabBarController analogi bo'lib, ilovani asosiy sahifalarga bo'lish va foydalanuvchiga ular o'rtasida qulay harakatlanish imkonini beradi.

## Ishlash natijasi:
```text
TabView komponenti yaratildi.
```


# 907-Topshiriq: Dasturiy Tab Tanlash va Reaktiv Switch
## Topshiriq sharti:
`@State` o'zgaruvchisi orqali dasturiy koddan turib istalgan tabga o'tishni amalga oshiring.

## Yechim (Swift kodi):
```swift
import SwiftUI

enum AsosiyTab: Int {
    case asosiy = 0
    case savat = 1
}

struct DasturiyTabView: View {
    @State private var tanlanganTab: AsosiyTab = .asosiy
    
    var body: some View {
        TabView(selection: $tanlanganTab) {
            VStack {
                Text("Asosiy Bo'lim")
                Button("Savatga o'tish") {
                    tanlanganTab = .savat
                }
            }
            .tag(AsosiyTab.asosiy)
            .tabItem { Label("Asosiy", systemImage: "star") }
            
            VStack {
                Text("Savat Bo'limi")
                Button("Asosiyga qaytish") {
                    tanlanganTab = .asosiy
                }
            }
            .tag(AsosiyTab.savat)
            .tabItem { Label("Savat", systemImage: "cart") }
        }
    }
}

let dt = DasturiyTabView()
print("Dasturiy TabView selection bilan yaratildi.")
```

## Tushuntirish va Mantiq:
`TabView(selection: $tanlanganTab)` va har bir sahifaga `.tag(...)` berish orqali tablar tanlanishini koddan to'liq boshqarish mumkin.

## Ishlash natijasi:
```text
Dasturiy TabView selection bilan yaratildi.
```


# 908-Topshiriq: `NavigationSplitView` Bilan Ko'p Ustunli iPad va Mac Maketi
## Topshiriq sharti:
iPad va macOS uchun moslashuvchan ikki ustunli (Sidebar va Detail) `NavigationSplitView` yarating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct IkkiUstunliView: View {
    @State private var tanlanganMavzu: String? = "Kirish"
    let mavzular = ["Kirish", "Swift Asoslari", "SwiftUI Navigatsiya", "CoreML"]
    
    var body: some View {
        NavigationSplitView {
            // Chap ustun: Yon menyu (Sidebar)
            List(mavzular, id: \.self, selection: $tanlanganMavzu) { mavzu in
                Text(mavzu)
            }
            .navigationTitle("Mundarija")
        } detail: {
            // O'ng ustun: Tafsilotlar (Detail)
            if let m = tanlanganMavzu {
                Text("Tanlangan mavzu tafsilotlari: \(m)")
                    .font(.title2)
            } else {
                Text("Mavzuni tanlang")
            }
        }
    }
}

let iu = IkkiUstunliView()
print("NavigationSplitView yaratildi.")
```

## Tushuntirish va Mantiq:
`NavigationSplitView` iPad, Mac va katta ekranli iPhone-larda avtomatik moslashuvchi (adaptive split) interfeys yaratish uchun asosiy vositadir.

## Ishlash natijasi:
```text
NavigationSplitView yaratildi.
```


# 909-Topshiriq: `toolbar` va `ToolbarItem` Joylashuvi
## Topshiriq sharti:
Navigatsiya panelining yuqori o'ng, chap va pastki barlariga maxsus tugmalar joylashtirishni ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct ToolbarMisolView: View {
    var body: some View {
        NavigationStack {
            Text("Kontent maydoni")
                .navigationTitle("Fayllar")
                .toolbar {
                    ToolbarItem(placement: .navigationBarLeading) {
                        Button("Tahrirlash") { }
                    }
                    ToolbarItem(placement: .navigationBarTrailing) {
                        Button(action: { }) {
                            Image(systemName: "plus")
                        }
                    }
                    ToolbarItem(placement: .bottomBar) {
                        Text("Jami: 10 ta fayl")
                            .font(.caption)
                    }
                }
        }
    }
}

let tmView = ToolbarMisolView()
print("ToolbarItem-lar bilan boyitilgan ekran yaratildi.")
```

## Tushuntirish va Mantiq:
`toolbar` modifikatori va uning `.navigationBarLeading`, `.navigationBarTrailing`, `.bottomBar`, `.principal` kabi joylashuv nuqtalari interfeysni standart iOS uslubida jihozlaydi.

## Ishlash natijasi:
```text
ToolbarItem-lar bilan boyitilgan ekran yaratildi.
```


# 910-Topshiriq: `searchable` Modifikatori Bilan Qidiruv Tizimi
## Topshiriq sharti:
Ro'yxat tepasida integratsiyalashgan qidiruv satrini ochuvchi `.searchable` modifikatorini yarating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct QidiruvRoyxatiView: View {
    let davlatlar = ["O'zbekiston", "Qozog'iston", "Turkiya", "Yaponiya", "Germaniya"]
    @State private var qidiruvSozi = ""
    
    var filtrlanganDavlatlar: [String] {
        if qidiruvSozi.isEmpty {
            return davlatlar
        } else {
            return davlatlar.filter { $0.localizedCaseInsensitiveContains(qidiruvSozi) }
        }
    }
    
    var body: some View {
        NavigationStack {
            List(filtrlanganDavlatlar, id: \.self) { d in
                Text(d)
            }
            .navigationTitle("Davlatlar")
            .searchable(text: $qidiruvSozi, prompt: "Davlat nomini qidiring...")
        }
    }
}

let qr = QidiruvRoyxatiView()
print("Searchable qidiruv ro'yxati tayyorlandi.")
```

## Tushuntirish va Mantiq:
`.searchable` modifikatori iOS navigatsiya paneliga to'liq integratsiyalashgan, qidiruv animatsiyasi va tozalash tugmasiga ega standart qidiruv interfeysini qo'shadi.

## Ishlash natijasi:
```text
Searchable qidiruv ro'yxati tayyorlandi.
```


# 911-Topshiriq: `searchSuggestions` Yordamida Qidiruv Maslahatlari
## Topshiriq sharti:
Qidiruv maydoniga foydalanuvchi yozishdan oldin taklif etiluvchi tavsiyalar ro'yxatini ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct QidiruvTavsiyalariView: View {
    @State private var matn = ""
    
    var body: some View {
        NavigationStack {
            Text("Qidiruv natijalari: \(matn)")
                .navigationTitle("Kutubxona")
                .searchable(text: $matn) {
                    Text("Swift").searchCompletion("Swift")
                    Text("SwiftUI").searchCompletion("SwiftUI")
                    Text("Concurrency").searchCompletion("Concurrency")
                }
        }
    }
}

let qt = QidiruvTavsiyalariView()
print("Search suggestions bilan qidiruv yaratildi.")
```

## Tushuntirish va Mantiq:
`.searchCompletion(...)` modifikatori foydalanuvchi tavsiya qilingan so'z ustiga bosganda, o'sha so'zni to'g'ridan-to'g'ri qidiruv maydoniga kiritadi.

## Ishlash natijasi:
```text
Search suggestions bilan qidiruv yaratildi.
```


# 912-Topshiriq: MVVM Arxitekturasi: Nazariya va Komponentlar Bo'linishi
## Topshiriq sharti:
SwiftUI-da Model-View-ViewModel (MVVM) arxitekturasining uchala qatlamini aniq ko'rsatuvchi tuzilmani yarating.

## Yechim (Swift kodi):
```swift
import SwiftUI
import Observation

// 1. MODEL - Sof ma'lumot strukturasi
struct XodimModel: Identifiable {
    let id: Int
    let ism: String
    let lavozim: String
}

// 2. VIEWMODEL - Biznes mantiq va holat boshqaruvi
@Observable
class XodimlarViewModel {
    var xodimlar: [XodimModel] = []
    
    func yuklash() {
        self.xodimlar = [
            XodimModel(id: 1, ism: "Dilshod", lavozim: "iOS Team Lead"),
            XodimModel(id: 2, ism: "Malika", lavozim: "UI/UX Designer")
        ]
    }
}

// 3. VIEW - Faqat interfeysni chizish va hodisalarni ViewModelga uzatish
struct XodimlarView: View {
    @State private var viewModel = XodimlarViewModel()
    
    var body: some View {
        NavigationStack {
            List(viewModel.xodimlar) { xodim in
                VStack(alignment: .leading) {
                    Text(xodim.ism).font(.headline)
                    Text(xodim.lavozim).font(.subheadline).foregroundColor(.secondary)
                }
            }
            .navigationTitle("Jamoa")
            .onAppear {
                viewModel.yuklash()
            }
        }
    }
}

let mvvm = XodimlarView()
print("Klassik MVVM strukturasi SwiftUI uchun shakllantirildi.")
```

## Tushuntirish va Mantiq:
MVVM arxitekturasi mas'uliyatlarni aniq ajratadi: Model faqat ma'lumotlarni saqlaydi, ViewModel ma'lumotlarni qayta ishlaydi va holatni boshqaradi, View esa faqat chiroyli qiyofani aks ettiradi.

## Ishlash natijasi:
```text
Klassik MVVM strukturasi SwiftUI uchun shakllantirildi.
```


# 913-Topshiriq: MVVM: Asinxron Tarmoq Holatlari (`UIState` Enum)
## Topshiriq sharti:
ViewModel ichida yuklanish (Loading), muvaffaqiyat (Success) va xatolik (Error) holatlarini enum orqali boshqarishni ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI
import Observation

enum YuklashHolati<T> {
    case boshlangich
    case yuklanmoqda
    case muvaffaqiyat(T)
    case xatolik(String)
}

@Observable
class YangiliklarViewModel {
    var holat: YuklashHolati<[String]> = .boshlangich
    
    func yangiliklarniYuklash() async {
        holat = .yuklanmoqda
        try? await Task.sleep(nanoseconds: 10_000_000)
        holat = .muvaffaqiyat(["Swift 6 chiqarildi", "Vision Pro yangilanishi"])
    }
}

let vm = YangiliklarViewModel()
print("Boshlang'ich holat: \(vm.holat)")
```

## Tushuntirish va Mantiq:
`UIState` enum yordamida View holatiga qarab avtomatik ravishda Spinner, Ma'lumotlar ro'yxati yoki Qayta urinish tugmasini chizishi mumkin.

## Ishlash natijasi:
```text
Boshlang'ich holat: boshlangich
```


# 914-Topshiriq: MVVM: `UIState` Enum Asosida View Render Qilish
## Topshiriq sharti:
Yuqoridagi `UIState` enumiga asoslanib `switch` orqali UI render qiluvchi to'liq View yozing.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct YangiliklarEkranView: View {
    @State private var viewModel = YangiliklarViewModel()
    
    var body: some View {
        VStack {
            switch viewModel.holat {
            case .boshlangich:
                Text("Ma'lumot yo'q, yuklash tugmasini bosing.")
            case .yuklanmoqda:
                ProgressView("Yangiliklar olinmoqda...")
            case .muvaffaqiyat(let yangiliklar):
                List(yangiliklar, id: \.self) { y in
                    Text(y)
                }
            case .xatolik(let xato):
                Text("Xatolik: \(xato)").foregroundColor(.red)
            }
        }
        .task {
            await viewModel.yangiliklarniYuklash()
        }
    }
}

let yv = YangiliklarEkranView()
print("UIState bo'yicha to'liq View yaratildi.")
```

## Tushuntirish va Mantiq:
Bu usul interfeysda hech qachon noaniq holat bo'lmasligini kafolatlaydi: yuklanayotganda spinner, natija kelganda ma'lumot chiqadi.

## Ishlash natijasi:
```text
UIState bo'yicha to'liq View yaratildi.
```


# 915-Topshiriq: Repository Pattern va Protokollar Bilan MVVM
## Topshiriq sharti:
Ma'lumotlar manbasini (API, Local DB) ViewModeldan ajratish uchun Repository patternini qo'llang.

## Yechim (Swift kodi):
```swift
import Foundation

protocol FoydalanuvchiRepository {
    func foydalanuvchiniOlish() async throws -> String
}

class HaqiqiyTarmoqRepository: FoydalanuvchiRepository {
    func foydalanuvchiniOlish() async throws -> String {
        return "Serverdan kelgan: Kamol"
    }
}

class TestMockRepository: FoydalanuvchiRepository {
    func foydalanuvchiniOlish() async throws -> String {
        return "Test: Mock Foydalanuvchi"
    }
}

@Observable
class ProfilViewModel {
    private let repo: FoydalanuvchiRepository
    var nom: String = ""
    
    init(repo: FoydalanuvchiRepository) {
        self.repo = repo
    }
    
    func yuklash() async {
        self.nom = (try? await repo.foydalanuvchiniOlish()) ?? "Xato"
    }
}

let vm = ProfilViewModel(repo: TestMockRepository())
print("Repository orqali ViewModel initsializatsiya qilindi.")
```

## Tushuntirish va Mantiq:
Repository patterni biznes mantiqni ma'lumotlar qaerdan (tarmoq, kesh, fayl) olinishidan to'liq mustaqil qiladi va unit test yozishni nihoyatda osonlashtiradi.

## Ishlash natijasi:
```text
Repository orqali ViewModel initsializatsiya qilindi.
```


# 916-Topshiriq: Custom EnvironmentKey Yaratish va Servislarni Ulash
## Topshiriq sharti:
SwiftUI muhitiga (Environment) o'z shaxsiy xizmatimizni qo'shish uchun `EnvironmentKey` yaratishni ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

// 1. Key yaratish
private struct AnalitikaKaliti: EnvironmentKey {
    static let defaultValue: String = "StandartAnalitikaXizmati"
}

// 2. Values kengaytmasi
extension EnvironmentValues {
    var analitikaNomi: String {
        get { self[AnalitikaKaliti.self] }
        set { self[AnalitikaKaliti.self] = newValue }
    }
}

struct AnalitikaKuzatuvchiView: View {
    @Environment(\.analitikaNomi) var analitika
    
    var body: some View {
        Text("Faol analitika: \(analitika)")
    }
}

let av = AnalitikaKuzatuvchiView()
print("Custom EnvironmentKey tizimi muvaffaqiyatli o'rnatildi.")
```

## Tushuntirish va Mantiq:
`EnvironmentKey` orqali butun ilova bo'ylab mavzular, autentifikatsiya tokenlari va umumiy xizmatlarni qulay tarqatish mumkin.

## Ishlash natijasi:
```text
Custom EnvironmentKey tizimi muvaffaqiyatli o'rnatildi.
```


# 917-Topshiriq: `PreferenceKey` Yordamida Boladan Otaga Ma'lumot Uzatish
## Topshiriq sharti:
Bola ko'rinish o'lchamini yoki parametrini ota ko'rinishga qaytarish uchun `PreferenceKey` dan foydalanishni ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct OynaBaladligiKaliti: PreferenceKey {
    static var defaultValue: CGFloat = 0
    static func reduce(value: inout CGFloat, nextValue: () -> CGFloat) {
        value = max(value, nextValue())
    }
}

struct BolaView: View {
    var body: some View {
        Text("Bola kontenti")
            .preference(key: OynaBaladligiKaliti.self, value: 50.0)
    }
}

struct OtaView: View {
    @State private var balandlik: CGFloat = 0
    
    var body: some View {
        VStack {
            BolaView()
            Text("Qabul qilingan balandlik: \(Int(balandlik)) pt")
        }
        .onPreferenceChange(OynaBaladligiKaliti.self) { yangiQiymat in
            balandlik = yangiQiymat
        }
    }
}

let ota = OtaView()
print("PreferenceKey ota-bola aloqasi yaratildi.")
```

## Tushuntirish va Mantiq:
Oddiy holatda parametrlar otadan bolaga o'tadi (`@Binding`). `PreferenceKey` esa ma'lumotlarni ierarxiya bo'ylab pastdan yuqoriga (boladan otaga) xavfsiz uzatish imkonini beradi.

## Ishlash natijasi:
```text
PreferenceKey ota-bola aloqasi yaratildi.
```


# 918-Topshiriq: `matchedGeometryEffect` Bilan Elementlar Animatsiyasi (Hero Animation)
## Topshiriq sharti:
Kichik kartaning katta sahifaga silliq o'tishi uchun `matchedGeometryEffect` va `@Namespace` dan foydalaning.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct HeroAnimatsiyaView: View {
    @Namespace private var animatsiyaFazosi
    @State private var kengaytirilganmi = false
    
    var body: some View {
        VStack {
            if !kengaytirilganmi {
                RoundedRectangle(cornerRadius: 10)
                    .fill(Color.blue)
                    .matchedGeometryEffect(id: "kartaId", in: animatsiyaFazosi)
                    .frame(width: 100, height: 100)
                    .onTapGesture {
                        withAnimation(.spring()) { kengaytirilganmi = true }
                    }
            } else {
                RoundedRectangle(cornerRadius: 24)
                    .fill(Color.blue)
                    .matchedGeometryEffect(id: "kartaId", in: animatsiyaFazosi)
                    .frame(width: 300, height: 400)
                    .onTapGesture {
                        withAnimation(.spring()) { kengaytirilganmi = false }
                    }
            }
        }
    }
}

let ha = HeroAnimatsiyaView()
print("matchedGeometryEffect hero animatsiyasi tayyorlandi.")
```

## Tushuntirish va Mantiq:
`matchedGeometryEffect(id:in:)` ikki xil holatdagi elementlarni bitta identifikator bilan bog'laydi va ular o'rtasidagi o'lcham, joylashuv va burchak o'zgarishini avtomatik silliq harakatlantiradi.

## Ishlash natijasi:
```text
matchedGeometryEffect hero animatsiyasi tayyorlandi.
```


# 919-Topshiriq: Asimmetrik O'tishlar (`.transition(.asymmetric)`)
## Topshiriq sharti:
Element paydo bo'layotganda chapdan kirib kelishi, yo'qolayotganda esa o'ngga chiqib ketishi uchun asimmetrik o'tishni yozing.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct AsimmetrikOtishView: View {
    @State private var korinsinmi = false
    
    var body: some View {
        VStack {
            Button("Ko'rsatish / Yashirish") {
                withAnimation { korinsinmi.toggle() }
            }
            
            if korinsinmi {
                Text("Ekranga chiquvchi xabar")
                    .padding()
                    .background(Color.yellow)
                    .transition(
                        .asymmetric(
                            insertion: .move(edge: .leading),
                            removal: .move(edge: .trailing)
                        )
                    )
            }
        }
    }
}

let ao = AsimmetrikOtishView()
print("Asimmetrik tranzitsiya muvaffaqiyatli ulandi.")
```

## Tushuntirish va Mantiq:
`.asymmetric(insertion:removal:)` elementi kirib kelayotganda boshqa, o'chirilayotganda butunlay boshqa animatsiya turini qo'llash imkonini beradi.

## Ishlash natijasi:
```text
Asimmetrik tranzitsiya muvaffaqiyatli ulandi.
```


# 920-Topshiriq: `Canvas` va `Path` Bilan 2D Shakllar Chizish
## Topshiriq sharti:
SwiftUI `Canvas` komponentidan foydalanib ekranga yuqori tezlikda geometrik shakllar va chiziqlar chizishni ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct MaxsusShaklView: View {
    var body: some View {
        Canvas { context, size in
            var yol = Path()
            yol.move(to: CGPoint(x: 0, y: size.height))
            yol.addLine(to: CGPoint(x: size.width / 2, y: 0))
            yol.addLine(to: CGPoint(x: size.width, y: size.height))
            yol.closeSubpath()
            
            context.fill(yol, with: .color(.purple))
        }
        .frame(width: 150, height: 150)
    }
}

let ms = MaxsusShaklView()
print("Canvas yordamida 2D shakl chizildi.")
```

## Tushuntirish va Mantiq:
`Canvas` apparat tezlatkichiga (Metal) to'g'ridan-to'g'ri ulangan bo'lib, murakkab grafiklar va zarrachalar (particles) effektlarini chizish uchun juda yuqori unumdorlik beradi.

## Ishlash natijasi:
```text
Canvas yordamida 2D shakl chizildi.
```


# 921-Topshiriq: `TimelineView` Bilan Haqiqiy Vaqtli Animatsiya
## Topshiriq sharti:
Soniyalar o'tishini muntazam yangilab turuvchi vaqtinchalik ko'rinish yaratish uchun `TimelineView` dan foydalaning.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct HaqiqiyVaqtView: View {
    var body: some View {
        TimelineView(.periodic(from: .now, by: 1.0)) { timeline in
            Text("Joriy vaqt: \(timeline.date.formatted(date: .omitted, time: .standard))")
                .font(.headline)
        }
    }
}

let hv = HaqiqiyVaqtView()
print("TimelineView vaqt kuzatuvchisi yaratildi.")
```

## Tushuntirish va Mantiq:
`TimelineView` berilgan chastota (masalan har soniya yoki har kadr) bo'yicha ko'rinishni qayta chizib, sekundomer, soat va animatsiyalarni oson qurish imkonini beradi.

## Ishlash natijasi:
```text
TimelineView vaqt kuzatuvchisi yaratildi.
```


# 922-Topshiriq: UIKit Integratsiyasi: `UIViewRepresentable` Asoslari
## Topshiriq sharti:
SwiftUI ichida mavjud UIKit komponentini (masalan `UIActivityIndicatorView`) ishlatish uchun `UIViewRepresentable` protokolini amalga oshiring.

## Yechim (Swift kodi):
```swift
import SwiftUI
import UIKit

struct UIKitSpinnerView: UIViewRepresentable {
    let aylanmoqdami: Bool
    
    func makeUIView(context: Context) -> UIActivityIndicatorView {
        let spinner = UIActivityIndicatorView(style: .large)
        return spinner
    }
    
    func updateUIView(_ uiView: UIActivityIndicatorView, context: Context) {
        if aylanmoqdami {
            uiView.startAnimating()
        } else {
            uiView.stopAnimating()
        }
    }
}

let us = UIKitSpinnerView(aylanmoqdami: true)
print("UIViewRepresentable komponenti yaratildi.")
```

## Tushuntirish va Mantiq:
`UIViewRepresentable` protokoli orqali SwiftUI-da hali mavjud bo'lmagan yoki eski UIKit kutubxonalaridagi har qanday `UIView`ni oson integratsiya qilish mumkin.

## Ishlash natijasi:
```text
UIViewRepresentable komponenti yaratildi.
```


# 923-Topshiriq: `UIViewRepresentable` Koordinatori va Delegatsiya
## Topshiriq sharti:
UIKit ko'rinishining hodisalarini (delegatsiyasini) SwiftUI bindingiga yetkazish uchun `Coordinator` yaratishni ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI
import UIKit

struct UIKitMatnMaydoni: UIViewRepresentable {
    @Binding var matn: String
    
    func makeCoordinator() -> Koordinator {
        Koordinator(self)
    }
    
    func makeUIView(context: Context) -> UITextField {
        let field = UITextField()
        field.delegate = context.coordinator
        return field
    }
    
    func updateUIView(_ uiView: UITextField, context: Context) {
        uiView.text = matn
    }
    
    class Koordinator: NSObject, UITextFieldDelegate {
        var ota: UIKitMatnMaydoni
        init(_ ota: UIKitMatnMaydoni) { self.ota = ota }
        
        func textFieldDidChangeSelection(_ textField: UITextField) {
            ota.matn = textField.text ?? ""
        }
    }
}

print("UIViewRepresentable Coordinator klassi bilan tayyorlandi.")
```

## Tushuntirish va Mantiq:
`Coordinator` obyekti UIKit delegate va target-action mexanizmlari bilan SwiftUI o'rtasidagi ko'prik vazifasini bajaradi.

## Ishlash natijasi:
```text
UIViewRepresentable Coordinator klassi bilan tayyorlandi.
```


# 924-Topshiriq: SwiftUI-ni UIKit-da Ishlatish: `UIHostingController`
## Topshiriq sharti:
Mavjud UIKit (Storyboard yoki Programmatic) ilovasida SwiftUI ko'rinishini ochish uchun `UIHostingController` dan foydalaning.

## Yechim (Swift kodi):
```swift
import SwiftUI
import UIKit

struct SalomSwiftUIView: View {
    var body: some View {
        Text("SwiftUI ekrani")
    }
}

// UIKit UIViewController ichida:
func swiftuiEkranniOchish(joriyKontroller: UIViewController) {
    let swiftUIView = SalomSwiftUIView()
    let hostingController = UIHostingController(rootView: swiftUIView)
    joriyKontroller.present(hostingController, animated: true)
}

print("UIHostingController adapteri tayyorlandi.")
```

## Tushuntirish va Mantiq:
`UIHostingController(rootView:)` har qanday SwiftUI View-ni to'laqonli `UIViewController`ga aylantirib beradi.

## Ishlash natijasi:
```text
UIHostingController adapteri tayyorlandi.
```


# 925-Topshiriq: `@main` Ilova Kirish Nuqtasi va `WindowGroup`
## Topshiriq sharti:
SwiftUI ilovasining kirish fayli qanday tuzilishini va `WindowGroup` sahnasini ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

// @main atributi ilovaning asosiy boshlanish nuqtasini belgilaydi
struct MeningIlovamApp: App {
    var body: some Scene {
        WindowGroup {
            AsosiyNavigatsiyaView()
        }
    }
}

print("SwiftUI App va WindowGroup strukturasi tayyor.")
```

## Tushuntirish va Mantiq:
`App` protokoli va `WindowGroup` sahnasi ko'p platformali (iOS, iPadOS, macOS, visionOS) ilovalarning derazalari hayot siklini boshqaradi.

## Ishlash natijasi:
```text
SwiftUI App va WindowGroup strukturasi tayyor.
```


# 926-Topshiriq: `@Environment(\.scenePhase)` Hayot Sikli
## Topshiriq sharti:
Ilova faol holatga kelganda (active) yoki fonga o'tganda (background) reaksiyani boshqarishni ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct SahnaKuzatuvchiView: View {
    @Environment(\.scenePhase) private var sahnaHolati
    
    var body: some View {
        Text("Ilova holati tekshirilmoqda")
            .onChange(of: sahnaHolati) { yangiHolat in
                switch yangiHolat {
                case .active:
                    print("Ilova hozir faol holatda (Active).")
                case .inactive:
                    print("Ilova nofaol holatda (Inactive).")
                case .background:
                    print("Ilova fon rejimiga o'tdi (Background). Xavfsiz saqlash!")
                @unknown default:
                    break
                }
            }
    }
}

let sk = SahnaKuzatuvchiView()
print("scenePhase kuzatuvchisi tayyorlandi.")
```

## Tushuntirish va Mantiq:
`scenePhase` butun ilova yoki ma'lum bir darcha fokusi o'zgarganini xabar beradi. Bu fonga o'tishda ma'lumotlarni saqlash yoki biometrik himoyani yoqish uchun zarur.

## Ishlash natijasi:
```text
scenePhase kuzatuvchisi tayyorlandi.
```


# 927-Topshiriq: `@FocusState` Bilan Klaviaturani Boshqarish
## Topshiriq sharti:
Matn maydoniga fokus berish va tugma bosilganda klaviaturani avtomatik yopishni amalga oshiring.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct FokusBoshqaruvchiView: View {
    enum Maydon {
        case ism, parol
    }
    
    @State private var ism = ""
    @State private var parol = ""
    @FocusState private var faolMaydon: Maydon?
    
    var body: some View {
        VStack {
            TextField("Ism", text: $ism)
                .focused($faolMaydon, equals: .ism)
            
            SecureField("Parol", text: $parol)
                .focused($faolMaydon, equals: .parol)
            
            Button("Klaviaturni yopish") {
                faolMaydon = nil // Fokusni olib tashlash klaviaturani yopadi
            }
        }
        .padding()
    }
}

let fb = FokusBoshqaruvchiView()
print("@FocusState klaviatura boshqaruvi ulandi.")
```

## Tushuntirish va Mantiq:
`@FocusState` qaysi TextField hozir kiritish fokusiga ega ekanini aniqlaydi va klaviaturani dasturiy tarzda ochish/yopish imkonini beradi.

## Ishlash natijasi:
```text
@FocusState klaviatura boshqaruvi ulandi.
```


# 928-Topshiriq: Accessibility: VoiceOver Qo'llab-quvvatlash
## Topshiriq sharti:
Imkoniyati cheklangan foydalanuvchilar uchun ekrandagi tugmaga maxsus VoiceOver ovozli tushuntirishlarini qo'shing.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct OvozliYordamchiView: View {
    var body: some View {
        Button(action: { }) {
            Image(systemName: "trash")
        }
        .accessibilityLabel("Xabarni o'chirish")
        .accessibilityHint("Bu tugmani bosish xatni savatga o'tkazadi")
    }
}

let oy = OvozliYordamchiView()
print("Accessibility parametrlari kiritildi.")
```

## Tushuntirish va Mantiq:
`.accessibilityLabel` va `.accessibilityHint` yordamida ko'rish qobiliyati past foydalanuvchilar VoiceOver orqali element vazifasini eshitishlari mumkin bo'ladi.

## Ishlash natijasi:
```text
Accessibility parametrlari kiritildi.
```


# 929-Topshiriq: Dynamic Type va `@ScaledMetric`
## Topshiriq sharti:
Tizimda shrift kattalashtirilganda unga mos ravishda piktogramma va chetlarni ham proporsional kattalashtiruvchi `@ScaledMetric` dan foydalaning.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct MasshtablanuvchiBelgiView: View {
    // Shrift kattalashganda 30 pt ham mutanosib ravishda o'sadi
    @ScaledMetric var belgiOlchami: CGFloat = 30.0
    
    var body: some View {
        HStack {
            Image(systemName: "star.fill")
                .frame(width: belgiOlchami, height: belgiOlchami)
            Text("Yulduzcha reytingi")
                .font(.body)
        }
    }
}

let mb = MasshtablanuvchiBelgiView()
print("@ScaledMetric dynamic type ko'rinishi yaratildi.")
```

## Tushuntirish va Mantiq:
`@ScaledMetric` foydalanuvchi tizim sozlamalarida shrift o'lchamini kattalashtirganda (Dynamic Type) rasmlar va oraliqlar mutanosibligini saqlab qoladi.

## Ishlash natijasi:
```text
@ScaledMetric dynamic type ko'rinishi yaratildi.
```


# 930-Topshiriq: Sensory Feedback (Haptic Touch)
## Topshiriq sharti:
Tugma bosilganda yoki amal yakunlanganda qurilmaning tebranishini (Haptic) faollashtiruvchi `.sensoryFeedback` modifikatorini ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct VibratsiyaTugmasiView: View {
    @State private var amaliyotMuvaffaqiyatlimi = false
    
    var body: some View {
        Button("To'lovni amalga oshirish") {
            amaliyotMuvaffaqiyatlimi.toggle()
        }
        // iOS 17+ zamonaviy haptic bildirishnomasi
        .sensoryFeedback(.success, trigger: amaliyotMuvaffaqiyatlimi)
    }
}

let vt = VibratsiyaTugmasiView()
print("sensoryFeedback modifikatori ulandi.")
```

## Tushuntirish va Mantiq:
`.sensoryFeedback(trigger:)` iOS 17+ da yangi deklarativ usul bo'lib, o'zgaruvchi qiymati o'zgarganda foydalanuvchiga jismoniy tebranish (taptic engine) javobini beradi.

## Ishlash natijasi:
```text
sensoryFeedback modifikatori ulandi.
```


# 931-Topshiriq: Pull to Refresh: `.refreshable` Modifikatori
## Topshiriq sharti:
Foydalanuvchi ro'yxatni pastga tortganda (pull-to-refresh) ma'lumotlarni asinxron yangilovchi modifikatorni yozing.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct YangilanuvchiRoyxatView: View {
    @State private var sonlar = [1, 2, 3]
    
    var body: some View {
        NavigationStack {
            List(sonlar, id: \.self) { s in
                Text("Element #\(s)")
            }
            .refreshable {
                // Asinxron yangilanish simulyatsiyasi
                try? await Task.sleep(nanoseconds: 15_000_000)
                sonlar.append(sonlar.count + 1)
            }
        }
    }
}

let yr = YangilanuvchiRoyxatView()
print("Pull to refresh (.refreshable) ulandi.")
```

## Tushuntirish va Mantiq:
`.refreshable` bloki ichida `await` orqali asinxron tarmoq ma'lumotlarini yuklash mumkin. Yuklanish tugaguncha indikator aylanib turadi.

## Ishlash natijasi:
```text
Pull to refresh (.refreshable) ulandi.
```


# 932-Topshiriq: Swipe Actions: Ro'yxat Qatorida Amallar
## Topshiriq sharti:
List qatorini chapga yoki o'ngga surishda (swipe) maxsus tugmalarni ko'rsatish uchun `.swipeActions` modifikatoridan foydalaning.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct QatorAmallariView: View {
    var body: some View {
        List {
            Text("Muhim hujjat.pdf")
                .swipeActions(edge: .trailing, allowsFullSwipe: true) {
                    Button(role: .destructive) {
                        print("Fayl o'chirildi")
                    } label: {
                        Label("O'chirish", systemImage: "trash")
                    }
                    
                    Button {
                        print("Fayl arxivlandi")
                    } label: {
                        Label("Arxiv", systemImage: "archivebox")
                    }
                    .tint(.blue)
                }
        }
    }
}

let qa = QatorAmallariView()
print("Swipe actions amallari tayyorlandi.")
```

## Tushuntirish va Mantiq:
`.swipeActions(edge:allowsFullSwipe:)` orqali Mail va Telegram kabi ilovalardagi tezkor surish amallarini yaratish mumkin.

## Ishlash natijasi:
```text
Swipe actions amallari tayyorlandi.
```


# 933-Topshiriq: Ro'yxat Qatorlarini O'chirish va Tartiblash (`onDelete`, `onMove`)
## Topshiriq sharti:
Foydalanuvchiga ro'yxatdagi elementlarni o'chirish va joyini almashtirish imkonini beruvchi kod yozing.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct TartiblanuvchiRoyxatView: View {
    @State private var tillar = ["Swift", "Kotlin", "Python", "Rust"]
    
    var body: some View {
        NavigationStack {
            List {
                ForEach(tillar, id: \.self) { til in
                    Text(til)
                }
                .onDelete { indekslar in
                    tillar.remove(atOffsets: indekslar)
                }
                .onMove { manba, manzil in
                    tillar.move(fromOffsets: manba, toOffset: manzil)
                }
            }
            .toolbar {
                EditButton() // Tahrirlash tugmasi
            }
        }
    }
}

let tr = TartiblanuvchiRoyxatView()
print("onDelete va onMove tartiblash mexanizmi yaratildi.")
```

## Tushuntirish va Mantiq:
`onDelete` va `onMove` hodisalari `EditButton()` bilan birgalikda to'laqonli ro'yxat tahrirlash imkoniyatini taqdim etadi.

## Ishlash natijasi:
```text
onDelete va onMove tartiblash mexanizmi yaratildi.
```


# 934-Topshiriq: Safe Area Chegaralari va `.ignoresSafeArea`
## Topshiriq sharti:
Ko'rinishni ekran chetidagi status bar va quyi qismlargacha yoyish uchun `.ignoresSafeArea` dan to'g'ri foydalanishni ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct XavfsizHududView: View {
    var body: some View {
        ZStack {
            Color.teal
                .ignoresSafeArea() // Butun ekranni egallaydi
            
            VStack {
                Text("Xavfsiz zona ichidagi matn")
                    .foregroundColor(.white)
            }
        }
    }
}

let xh = XavfsizHududView()
print("Safe Area boshqaruvi ulandi.")
```

## Tushuntirish va Mantiq:
`.ignoresSafeArea()` fonga to'liq ekranni qoplash imkonini beradi, ichki kontent esa tugmalar va matnlar tirqishlarga (notch, dynamic island) kirmasligi uchun saqlanadi.

## Ishlash natijasi:
```text
Safe Area boshqaruvi ulandi.
```


# 935-Topshiriq: Clean Architecture: Interactor / UseCase Qatlami
## Topshiriq sharti:
ViewModel ichidagi biznes logikani yanada ixchamlashtirish uchun UseCase qatlamini yaratishni ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

struct BuyurtmaYaratishUseCase {
    func execute(mahsulotId: Int, miqdor: Int) -> Bool {
        print("USE_CASE: #\(mahsulotId) dan \(miqdor) dona tekshirildi va tasdiqlandi.")
        return true
    }
}

class BuyurtmaViewModel {
    private let useCase = BuyurtmaYaratishUseCase()
    
    func sotibOlish() {
        let muvaffaqiyat = useCase.execute(mahsulotId: 101, miqdor: 2)
        print("ViewModel: Natija -> \(muvaffaqiyat)")
    }
}

let bvm = BuyurtmaViewModel()
bvm.sotibOlish()
```

## Tushuntirish va Mantiq:
Clean Architecture tamoyillariga ko'ra, murakkab biznes qoidalar ViewModel ichida emas, balki alohida Use Case (Interactor) sinflarida yoziladi.

## Ishlash natijasi:
```text
USE_CASE: #101 dan 2 dona tekshirildi va tasdiqlandi.
ViewModel: Natija -> true
```


# 936-Topshiriq: Coordinator / Router Pattern SwiftUI-da
## Topshiriq sharti:
Navigatsiya logikasini View-dan butunlay olib tashlab, alohida Router klassiga topshirishni ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI
import Observation

enum Sahifa: Hashable {
    case royxat
    case tafsilot(Int)
}

@Observable
class IlovaRouter {
    var navYoli = NavigationPath()
    
    func tafsilotgaOtish(id: Int) {
        navYoli.append(Sahifa.tafsilot(id))
    }
    
    func ortgaQaytish() {
        if !navYoli.isEmpty {
            navYoli.removeLast()
        }
    }
}

let router = IlovaRouter()
print("Ilova Routeri yaratildi. Hozirgi yo'l hajmi: \(router.navYoli.count)")
```

## Tushuntirish va Mantiq:
Router patterni navigatsiya mantiqini View-dan mustaqil qiladi va deep-link, bildirishnoma orqali ochilishlar va testlashni osonlashtiradi.

## Ishlash natijasi:
```text
Ilova Routeri yaratildi. Hozirgi yo'l hajmi: 0
```


# 937-Topshiriq: UI State Machine Bilan Holatlarni Boshqarish
## Topshiriq sharti:
Finite State Machine (FSM) orqali UI sahifasining holatlarini qat'iy boshqaruvchi tuzilma yarating.

## Yechim (Swift kodi):
```swift
enum VideoPlayerHolat {
    case toxtatilgan
    case ijroEtilmoqda(sekund: Int)
    case pauza(sekund: Int)
}

class VideoPlayerMashinasi {
    private(set) var holat: VideoPlayerHolat = .toxtatilgan
    
    func start() {
        holat = .ijroEtilmoqda(sekund: 0)
    }
    
    func toxtat() {
        holat = .toxtatilgan
    }
}

let pleyer = VideoPlayerMashinasi()
pleyer.start()
print("Pleyer holati: \(pleyer.holat)")
```

## Tushuntirish va Mantiq:
State Machine orqali bitta holatdan ikkinchisiga o'tishlar qat'iy tekshiriladi, natijada mantiqsiz holatlar (masalan yuklanmasdan turib ijro etish) oldi olinadi.

## Ishlash natijasi:
```text
Pleyer holati: ijroEtilmoqda(sekund: 0)
```


# 938-Topshiriq: EquatableView Bilan Keraksiz Qayta Chizilishlarni Oldini Olish
## Topshiriq sharti:
Murakkab View faqat ma'lum bir qiymat o'zgargandagina qayta render qilinishi uchun `Equatable` protokolini ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct QimmatView: View, Equatable {
    let id: Int
    let nomi: String
    
    static func == (chap: QimmatView, ong: QimmatView) -> Bool {
        // Faqat id teng bo'lsa render qilinmasin
        return chap.id == ong.id
    }
    
    var body: some View {
        Text("Element: \(nomi)")
    }
}

let qv = QimmatView(id: 1, nomi: "A").equatable()
print("EquatableView optimizatsiyasi ulandi.")
```

## Tushuntirish va Mantiq:
SwiftUI o'zgaruvchi yangilanganda barcha bolalarni qayta tekshiradi. `.equatable()` orqali agar parametrlar o'zgarmagan bo'lsa, qimmat `body` hisob-kitobini to'xtatish mumkin.

## Ishlash natijasi:
```text
EquatableView optimizatsiyasi ulandi.
```


# 939-Topshiriq: View Body Inside Function Call Warning Oldini Olish
## Topshiriq sharti:
`body` ichida og'ir hisob-kitoblarni bajarmasdan, ularni `computed property` yoki `ViewModel`ga ko'chirish qoidasini ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct OptimizatsiyaQoidasiView: View {
    let sonlar = [10, 20, 30, 40, 50]
    
    // YAXSHI AMALIYOT: Og'ir hisob-kitob body-dan tashqarida bo'lishi shart
    var ortachaQiymat: Double {
        Double(sonlar.reduce(0, +)) / Double(sonlar.count)
    }
    
    var body: some View {
        Text("O'rtacha: \(ortachaQiymat, specifier: "%.1f")")
    }
}

let oq = OptimizatsiyaQoidasiView()
print("Toza optimallashtirilgan View yaratildi.")
```

## Tushuntirish va Mantiq:
SwiftUI `body` soniyasiga 60-120 marta qayta chaqirilishi mumkin. Shu sababli body ichida looplar, tartiblashlar va og'ir amallarni bajarish qat'iyan man etiladi.

## Ishlash natijasi:
```text
Toza optimallashtirilgan View yaratildi.
```


# 940-Topshiriq: Snapshot Testing Asoslari (Nazariya va Mock)
## Topshiriq sharti:
SwiftUI interfeysini vizual pikselma-piksel taqqoslash orqali testlash tamoyilini yozing.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct TestEkran: View {
    var body: some View {
        Text("Snapshot uchun ko'rinish")
    }
}

func testSnapshotMock(view: some View) -> Bool {
    print("SNAPSHOT TEST: View render qilindi va mos keldi.")
    return true
}

let muvaffaqiyat = testSnapshotMock(view: TestEkran())
print("Test natijasi: \(muvaffaqiyat)")
```

## Tushuntirish va Mantiq:
Snapshot testing interfeysning rasm nusxasini olib, kelajakda kod o'zgarganda dizaynda kutilmagan buzilishlar paydo bo'lmasligini tekshiradi.

## Ishlash natijasi:
```text
SNAPSHOT TEST: View render qilindi va mos keldi.
Test natijasi: true
```


# 941-Topshiriq: SwiftUI ViewInspector va Unit Test Tamoyillari
## Topshiriq sharti:
SwiftUI ko'rinishlaridagi matn va tugmalarni dasturiy tarzda tekshirish usulini ko'rsating.

## Yechim (Swift kodi):
```swift
struct OddiyProfilView {
    let sarlavha = "Xush kelibsiz"
}

func testProfilViewSarlavhasi() {
    let view = OddiyProfilView()
    assert(view.sarlavha == "Xush kelibsiz", "Sarlavha to'g'ri kelmadi!")
    print("UNIT TEST: View modellari to'g'ri tekshirildi.")
}

testProfilViewSarlavhasi()
```

## Tushuntirish va Mantiq:
SwiftUI struct-lari sof qiymat tiplari bo'lgani sababli, ularning ichki parametrlarini oddiy unit testlar orqali tezkor tekshirish mumkin.

## Ishlash natijasi:
```text
UNIT TEST: View modellari to'g'ri tekshirildi.
```


# 942-Topshiriq: Lokalizatsiya: Ko'p Tillilik (`LocalizedStringKey`)
## Topshiriq sharti:
SwiftUI-da matnlarni turli tillarga moslashtirish (Localization) mexanizmini ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct TilTanlashView: View {
    var body: some View {
        VStack {
            // Text avtomatik ravishda Localizable.strings faylidan tarjimani qidiradi
            Text("welcome_title")
            Text("login_button")
        }
    }
}

let tt = TilTanlashView()
print("Lokalizatsiya kalitlari bilan View yaratildi.")
```

## Tushuntirish va Mantiq:
SwiftUI-dagi barcha `Text` komponentlari avtomatik `LocalizedStringKey` qabul qiladi va qurilma tiliga qarab tarjimalarni yuklaydi.

## Ishlash natijasi:
```text
Lokalizatsiya kalitlari bilan View yaratildi.
```


# 943-Topshiriq: Swift Package Manager (SPM) Bilan UI Modulini Ajratish
## Topshiriq sharti:
Ilovani modullashtirish uchun mustaqil UI dizayn kutubxonasini (Design System Package) tuzish prinsiplari.

## Yechim (Swift kodi):
```swift
public struct AsosiyTugmaKomponenti: View {
    public let matn: String
    public let amal: () -> Void
    
    public init(matn: String, amal: @escaping () -> Void) {
        self.matn = matn
        self.amal = amal
    }
    
    public var body: some View {
        Button(matn, action: amal)
            .padding()
            .background(Color.blue)
            .foregroundColor(.white)
            .cornerRadius(8)
    }
}

print("SPM moduli uchun ochiq (public) komponent yaratildi.")
```

## Tushuntirish va Mantiq:
Katta loyihalarda umumiy komponentlar alohida Swift paketlariga (SPM) chiqariladi, bu esa kompilyatsiya vaqtini qisqartiradi va kodni toza saqlaydi.

## Ishlash natijasi:
```text
SPM moduli uchun ochiq (public) komponent yaratildi.
```


# 944-Topshiriq: Konteyner va Presentational Komponentlar Patterni
## Topshiriq sharti:
Ma'lumot oluvchi 'aqlli' konteyner va faqat ma'lumotni chizuvchi 'soqov' (dumb) prezentatsion komponentlarni ajratishni ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

// Presentational (Sof UI)
struct MahsulotQatoriView: View {
    let nom: String
    let narx: Double
    var body: some View {
        HStack {
            Text(nom)
            Spacer()
            Text("$\(narx, specifier: "%.2f")")
        }
    }
}

// Container (Mantiq va yuklash)
struct MahsulotlarKonteyneriView: View {
    @State private var mahsulotlar = [("Monitor", 250.0), ("Klaviatura", 45.0)]
    
    var body: some View {
        List(mahsulotlar, id: \.0) { m in
            MahsulotQatoriView(nom: m.0, narx: m.1)
        }
    }
}

let mkView = MahsulotlarKonteyneriView()
print("Konteyner va Prezentatsiya komponentlari ajratildi.")
```

## Tushuntirish va Mantiq:
Prezentatsion komponentlar o'z holatiga ega bo'lmaydi, ularni qayta ishlatish va alohida test qilish oson kechadi.

## Ishlash natijasi:
```text
Konteyner va Prezentatsiya komponentlari ajratildi.
```


# 945-Topshiriq: Dependency Injection Konteyneri Bilan ViewModel Yasash
## Topshiriq sharti:
ViewModel initsializatoriga servislarni avtomatik kiritish (DI) mexanizmini yozing.

## Yechim (Swift kodi):
```swift
protocol TarmoqXizmatiProtokol {
    func yuklash() -> String
}

class HaqiqiyTarmoq: TarmoqXizmatiProtokol {
    func yuklash() -> String { "Jonli ma'lumot" }
}

class FoydalanuvchiViewModel {
    let tarmoq: TarmoqXizmatiProtokol
    init(tarmoq: TarmoqXizmatiProtokol = HaqiqiyTarmoq()) {
        self.tarmoq = tarmoq
    }
}

let vmDefault = FoydalanuvchiViewModel()
print("Tarmoq natijasi: \(vmDefault.tarmoq.yuklash())")
```

## Tushuntirish va Mantiq:
Standart parametr qiymatlari (`= HaqiqiyTarmoq()`) orqali ishlab chiqarishda qulaylik, testlarda esa mock kiritish imkoniyati ta'minlanadi.

## Ishlash natijasi:
```text
Tarmoq natijasi: Jonli ma'lumot
```


# 946-Topshiriq: Dynamic Property Wrapper Yaratish
## Topshiriq sharti:
SwiftUI ichki mexanizmlari kabi ishlovchi maxsus `DynamicProperty` wrapperini yarating.

## Yechim (Swift kodi):
```swift
import SwiftUI

@propertyWrapper
struct TasodifiySon: DynamicProperty {
    @State private var qiymat = Int.random(in: 1...100)
    
    var wrappedValue: Int {
        get { qiymat }
        nonmutating set { qiymat = newValue }
    }
}

struct TasodifiyView: View {
    @TasodifiySon var son: Int
    
    var body: some View {
        Text("Tasodifiy: \(son)")
    }
}

let tv = TasodifiyView()
print("DynamicProperty wrapperi ishga tushirildi.")
```

## Tushuntirish va Mantiq:
`DynamicProperty` protokoliga mos property wrapperlar SwiftUI ko'rinishining hayot sikliga to'g'ridan-to'g'ri integratsiyalashadi.

## Ishlash natijasi:
```text
DynamicProperty wrapperi ishga tushirildi.
```


# 947-Topshiriq: App Storage vs Secure Enclave (Keychain) Saqlash
## Topshiriq sharti:
Maxfiy ma'lumotlar (parollar, tokenlar) nima sababdan UserDefaults-da emas, balki Keychain-da saqlanishi kerakligini ko'rsatuvchi tuzilma.

## Yechim (Swift kodi):
```swift
struct XavfsizSaqlashQoidasi {
    let ma'lumotTuri: String
    let tavsiyaQilinganJoy: String
    let sabab: String
}

let taqqoslash = [
    XavfsizSaqlashQoidasi(ma'lumotTuri: "Mavzu sozlamasi (Dark mode)", tavsiyaQilinganJoy: "@AppStorage (UserDefaults)", sabab: "Maxfiy emas, tezkor o'qish"),
    XavfsizSaqlashQoidasi(ma'lumotTuri: "API Access Token", tavsiyaQilinganJoy: "Keychain Services", sabab: "Shifrlangan apparat himoyasi"),
    XavfsizSaqlashQoidasi(ma'lumotTuri: "Biometrik kalitlar", tavsiyaQilinganJoy: "Secure Enclave", sabab: "Ekstremal darajadagi xavfsizlik")
]

for t in taqqoslash {
    print("[\(t.ma'lumotTuri)]: Joy -> \(t.tavsiyaQilinganJoy) (\(t.sabab))")
}
```

## Tushuntirish va Mantiq:
SwiftUI ilovalarida `@AppStorage` faqat xavfsiz bo'lmagan foydalanuvchi sozlamalari uchundir. Foydalanuvchi hisob ma'lumotlari esa har doim Keychain orqali saqlanishi zarur.

## Ishlash natijasi:
```text
[Mavzu sozlamasi (Dark mode)]: Joy -> @AppStorage (UserDefaults) (Maxfiy emas, tezkor o'qish)
[API Access Token]: Joy -> Keychain Services (Shifrlangan apparat himoyasi)
[Biometrik kalitlar]: Joy -> Secure Enclave (Ekstremal darajadagi xavfsizlik)
```


# 948-Topshiriq: SwiftUI Render Loop Diagnostikasi: `Self._printChanges()`
## Topshiriq sharti:
SwiftUI ko'rinishining nima sababdan qayta chizilayotganini tahlil qilish uchun yashirin `Self._printChanges()` vositasidan foydalanishni ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct DiagnostikaView: View {
    @State private var son = 0
    
    var body: some View {
        #if DEBUG
        // SwiftUI ichki diagnostika usuli: konsolda aynan qaysi o'zgaruvchi sabab bo'lganini ko'rsatadi
        let _ = Self._printChanges()
        #endif
        
        Text("Son: \(son)")
            .onTapGesture { son += 1 }
    }
}

let dv = DiagnostikaView()
print("Self._printChanges() diagnostikasi o'rnatildi.")
```

## Tushuntirish va Mantiq:
`Self._printChanges()` funksiyasi Xcode konsoliga har safar View qayta chizilganda qaysi property (masalan `@State`, `@Binding`) o'zgarganini chiqarib beradi.

## Ishlash natijasi:
```text
Self._printChanges() diagnostikasi o'rnatildi.
```


# 949-Topshiriq: Custom Environment Dismiss Interceptor (Tasdiqlash Oynasi)
## Topshiriq sharti:
Foydalanuvchi sahifani yopmoqchi bo'lganda saqlanmagan o'zgarishlar borligini eslatuvchi interceptor yarating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct SaqlashOgohlantirishView: View {
    @State private var tahrirlandi = true
    @State private var ogohlantirishOchiq = false
    @Environment(\.dismiss) private var dismissAction
    
    var body: some View {
        NavigationStack {
            VStack {
                Text("Tahrirlash sahifasi")
            }
            .navigationTitle("Hujjat")
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Bekor qilish") {
                        if tahrirlandi {
                            ogohlantirishOchiq = true
                        } else {
                            dismissAction()
                        }
                    }
                }
            }
            .alert("Saqlanmagan o'zgarishlar bor", isPresented: $ogohlantirishOchiq) {
                Button("O'zgarishlarni bekor qilish", role: .destructive) {
                    dismissAction()
                }
                Button("Davom etish", role: .cancel) { }
            }
        }
    }
}

let sov = SaqlashOgohlantirishView()
print("Dismiss interceptor muvaffaqiyatli ulandi.")
```

## Tushuntirish va Mantiq:
Foydalanuvchi ma'lumotlarini yo'qotib qo'ymasligi uchun yopish harakatini ushlab qolib, tasdiq so'rash professional interfeys talabidir.

## Ishlash natijasi:
```text
Dismiss interceptor muvaffaqiyatli ulandi.
```


# 950-Topshiriq: Amaliy Kompleks Loyiha: E-Commerce Do'kon Ilovasi Arxitekturasi
## Topshiriq sharti:
NavigationStack, NavigationPath, MVVM, Repository, Savat hisob-kitobi va to'liq sahifalar o'tishini birlashtirgan E-Commerce ilovasi arxitekturasini yarating.

## Yechim (Swift kodi):
```swift
import SwiftUI
import Observation

// 1. Model
struct Mahsulot: Identifiable, Hashable {
    let id: Int
    let nom: String
    let narx: Double
    let kategoriya: String
}

// 2. Repository
class MahsulotlarOmbori {
    func barchaMahsulotlar() -> [Mahsulot] {
        return [
            Mahsulot(id: 1, nom: "MacBook Pro M3", narx: 1999.0, kategoriya: "Kompyuter"),
            Mahsulot(id: 2, nom: "iPhone 15 Pro", narx: 999.0, kategoriya: "Telefon"),
            Mahsulot(id: 3, nom: "AirPods Max", narx: 549.0, kategoriya: "Audio")
        ]
    }
}

// 3. ViewModel
@Observable
class DokonViewModel {
    private let ombor = MahsulotlarOmbori()
    var mahsulotlar: [Mahsulot] = []
    var savat: [Mahsulot] = []
    var navigatsiyaYoli = NavigationPath()
    
    init() {
        self.mahsulotlar = ombor.barchaMahsulotlar()
    }
    
    var jamiSumma: Double {
        savat.reduce(0) { $0 + $1.narx }
    }
    
    func savatgaQoshish(_ mahsulot: Mahsulot) {
        savat.append(mahsulot)
    }
}

// 4. SwiftUI Ko'rinishlari
struct DokonIlovasiView: View {
    @State private var vm = DokonViewModel()
    
    var body: some View {
        NavigationStack(path: $vm.navigatsiyaYoli) {
            List(vm.mahsulotlar) { m in
                NavigationLink(value: m) {
                    HStack {
                        VStack(alignment: .leading) {
                            Text(m.nom).font(.headline)
                            Text(m.kategoriya).font(.caption).foregroundColor(.secondary)
                        }
                        Spacer()
                        Text("$\(m.narx, specifier: "%.2f")")
                            .fontWeight(.bold)
                    }
                }
            }
            .navigationTitle("Apple Store")
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: { vm.navigatsiyaYoli.append("SAVAT") }) {
                        HStack {
                            Image(systemName: "cart")
                            Text("\(vm.savat.count)")
                        }
                    }
                }
            }
            .navigationDestination(for: Mahsulot.self) { m in
                VStack(spacing: 20) {
                    Text(m.nom).font(.largeTitle).bold()
                    Text("Narxi: $\(m.narx, specifier: "%.2f")").font(.title2)
                    Button("Savatga qo'shish") {
                        vm.savatgaQoshish(m)
                    }
                    .buttonStyle(.borderedProminent)
                }
                .padding()
            }
            .navigationDestination(for: String.self) { maxsus in
                if maxsus == "SAVAT" {
                    VStack {
                        Text("Savatchangiz").font(.title)
                        List(vm.savat) { item in
                            Text("\(item.nom) - $\(item.narx, specifier: "%.2f")")
                        }
                        Text("Jami: $\(vm.jamiSumma, specifier: "%.2f")").font(.headline)
                    }
                }
            }
        }
    }
}

let dokon = DokonIlovasiView()
print("E-Commerce do'kon ilovasi arxitekturasi to'liq ishga tushirildi!")
```

## Tushuntirish va Mantiq:
Ushbu loyihada zamonaviy SwiftUI arxitekturasi: `NavigationStack(path:)`, `NavigationLink(value:)`, ko'p tipli navigatsiya marshrutlari, `@Observable` ViewModel va Repository to'liq mujassamlangan.

## Ishlash natijasi:
```text
E-Commerce do'kon ilovasi arxitekturasi to'liq ishga tushirildi!
```

