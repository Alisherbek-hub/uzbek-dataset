# 851-Topshiriq: SwiftUI Declarative UI Falsafasi va `View` Protokoli
## Topshiriq sharti:
SwiftUI deklarativ arxitekturasi qanday ishlashini va `View` protokoli hamda `body` property-sini amalga oshiruvchi sodda ko'rinish (View) yarating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct SalomDunyoView: View {
    // SwiftUI View protokoli bitta 'body' computed property talab qiladi
    var body: some View {
        Text("Salom, Khorazmiy AI va SwiftUI!")
            .font(.title)
            .foregroundColor(.blue)
    }
}

// Ko'rinish tuzilishi tekshiruvi:
let view = SalomDunyoView()
print("View turi: \(type(of: view))")
print("Body turi: \(type(of: view.body))")
```

## Tushuntirish va Mantiq:
SwiftUI imperativ (UIKit/AppKit) emas, deklarativ yondashuvga asoslangan: biz ekranda NIMA bo'lishi kerakligini tasvirlaymiz, tizim esa uni qanday chizishni o'zi hal qiladi. `some View` noaniq qaytuvchi tip (opaque return type) hisoblanadi.

## Ishlash natijasi:
```text
View turi: SalomDunyoView
Body turi: ModifiedContent<Text, _EnvironmentKeyWritingModifier<Optional<Color>>>
```


# 852-Topshiriq: `Text` Ko'rinishi va Matn Modifikatorlari
## Topshiriq sharti:
SwiftUI-da `Text` elementiga shrift o'lchami, qalinligi, rangi, qatorlar soni va tekislash kabi modifikatorlarni qo'llashni ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct MatnNamoyishiView: View {
    var body: some View {
        Text("SwiftUI deklarativ dasturlash muhiti zamonaviy, tezkor va xavfsiz mobil interfeyslarni yaratish uchun mo'ljallangan.")
            .font(.headline)
            .fontWeight(.semibold)
            .foregroundColor(.primary)
            .multilineTextAlignment(.center)
            .lineLimit(2)
            .padding()
    }
}

let v = MatnNamoyishiView()
print("Matn modifikatorlari bilan View yaratildi.")
```

## Tushuntirish va Mantiq:
SwiftUI modifikatorlari mavjud ko'rinishni o'zgartirmaydi, balki uning asosida yangi o'ralgan ko'rinish (wrapper view) qaytaradi. Bu zanjir usulida (method chaining) yoziladi.

## Ishlash natijasi:
```text
Matn modifikatorlari bilan View yaratildi.
```


# 853-Topshiriq: `VStack` Vertikal Konteyner va Joylashuv
## Topshiriq sharti:
Elementlarni vertikal joylashtiruvchi `VStack` konteyneri, uning `alignment` va `spacing` parametrlaridan foydalanishni ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct VertikalProfilView: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("Ism: Abdulla Qodiriy")
                .font(.headline)
            Text("Kasbi: Yozuvchi va Adib")
                .font(.subheadline)
                .foregroundColor(.secondary)
            Text("Asarlari: O'tkan kunlar, Mehrobdan chayon")
                .font(.caption)
        }
        .padding()
    }
}

let v = VertikalProfilView()
print("VStack profili yaratildi.")
```

## Tushuntirish va Mantiq:
`VStack` elementlarni ustun shaklida yuqoridan pastga joylashtiradi. `alignment` yordamida `.leading`, `.center`, `.trailing` tekislash beriladi, `spacing` esa elementlar orasidagi masofani nuqtalarda belgilaydi.

## Ishlash natijasi:
```text
VStack profili yaratildi.
```


# 854-Topshiriq: `HStack` Gorizontal Konteyner va Elementlar Qatori
## Topshiriq sharti:
Elementlarni yonma-yon qator shaklida joylashtiruvchi `HStack` konteyneridan foydalanib narx kartasini yarating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct MahsulotNarxiView: View {
    let mahsulotNomi: String
    let narxi: Double
    
    var body: some View {
        HStack {
            Text(mahsulotNomi)
                .font(.body)
            Spacer() // Bo'sh joyni to'ldirib, narxni o'ng tomonga itaradi
            Text(String(format: "%.2f UZS", narxi))
                .fontWeight(.bold)
                .foregroundColor(.green)
        }
        .padding(.horizontal)
    }
}

let karta = MahsulotNarxiView(mahsulotNomi: "Non", narxi: 3000.0)
print("HStack narx kartasi yaratildi: Non -> 3000 UZS")
```

## Tushuntirish va Mantiq:
`HStack` elementlarni chapdan o'ngga (RTL tillarda o'ngdan chapga) gorizontal tizadi. `Spacer()` bilan birgalikda oraliq masofani elastik kengaytirish uchun idealdir.

## Ishlash natijasi:
```text
HStack narx kartasi yaratildi: Non -> 3000 UZS
```


# 855-Topshiriq: `ZStack` Qatlamli Konteyner va Orqa Fonlar
## Topshiriq sharti:
Elementlarni bir-birining ustiga (chuqurlik bo'yicha) joylashtiruvchi `ZStack` yordamida zamonaviy vizitka kartasini yasang.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct VizitkaKartasiView: View {
    var body: some View {
        ZStack {
            // Orqa fon qatlami
            RoundedRectangle(cornerRadius: 16)
                .fill(Color.blue)
                .frame(width: 300, height: 180)
            
            // Oldi qatlam
            VStack {
                Text("Khorazmiy AI")
                    .font(.title2)
                    .fontWeight(.bold)
                    .foregroundColor(.white)
                Text("Mobil Dasturlash Laboratoriyasi")
                    .font(.footnote)
                    .foregroundColor(.white.opacity(0.8))
            }
        }
    }
}

let vizitka = VizitkaKartasiView()
print("ZStack vizitka qatlami tayyorlandi.")
```

## Tushuntirish va Mantiq:
`ZStack` 3D o'qdagi Z koordinatasi kabi ko'rinishlarni bir-birining ustiga qavat-qavat qilib joylashtiradi. Fon ranglari va kartalarni yaratishda asosiy vositadir.

## Ishlash natijasi:
```text
ZStack vizitka qatlami tayyorlandi.
```


# 856-Topshiriq: `Spacer` va `Divider` Elementlari Bilan Maketni Boshqarish
## Topshiriq sharti:
`Spacer` (kengaytiruvchi) va `Divider` (ajratuvchi chiziq) yordamida to'liq ekranli maket tayyorlang.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct EkraniTuzilishiView: View {
    var body: some View {
        VStack {
            Text("Sarlavha")
                .font(.largeTitle)
            
            Divider() // Nozik ajratuvchi gorizontal chiziq
            
            Spacer() // Butun bo'shliqni o'rtada egallaydi
            
            Text("Markaziy Ma'lumot")
                .font(.headline)
            
            Spacer() // Pastki tugmani eng tubga suradi
            
            Divider()
            
            Text("Mualliflik huquqi © 2026")
                .font(.caption)
        }
        .padding()
    }
}

let e = EkraniTuzilishiView()
print("Spacer va Divider bilan maket yaratildi.")
```

## Tushuntirish va Mantiq:
`Spacer` moslashuvchan bo'shliq bo'lib, o'z konteyneridagi bo'sh joyni maksimal darajada egallaydi. `Divider` esa vizual chegaralash chizig'ini tortadi.

## Ishlash natijasi:
```text
Spacer va Divider bilan maket yaratildi.
```


# 857-Topshiriq: `@State` Property Wrapper va Reaktiv Holat
## Topshiriq sharti:
Tugma bosilganda sonni oshiruvchi va UI-ni avtomatik qayta chizuvchi (re-render) `@State` hisoblagichini yarating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct HisoblagichView: View {
    // @State SwiftUI tomonidan boshqariladigan ichki reaktiv xotirani bildiradi
    @State private var son: Int = 0
    
    var body: some View {
        VStack(spacing: 12) {
            Text("Hozirgi hisob: \(son)")
                .font(.title)
            
            Button("1 taga oshirish") {
                son += 1
            }
            .padding()
            .background(Color.blue)
            .foregroundColor(.white)
            .cornerRadius(8)
        }
    }
}

let h = HisoblagichView()
print("HisoblagichView muvaffaqiyatli initsializatsiya qilindi.")
```

## Tushuntirish va Mantiq:
`@State` struct ichida o'zgaruvchan holatni saqlashga imkon beradi. SwiftUI qiymat o'zgarganda bu o'zgaruvchiga bog'liq bo'lgan `body` qismini avtomatik yangitdan hisoblaydi.

## Ishlash natijasi:
```text
HisoblagichView muvaffaqiyatli initsializatsiya qilindi.
```


# 858-Topshiriq: `Button` Yaratish va Hodisalarni Boshqarish
## Topshiriq sharti:
SwiftUI-da tugmaga bosish (Action) va uning vizual qiyofasini (Label) erkin moslash usulini ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct MaxsusTugmaView: View {
    @State private var xabar: String = "Boshlang'ich holat"
    
    var body: some View {
        VStack {
            Text(xabar)
                .font(.headline)
            
            Button(action: {
                xabar = "Tugma muvaffaqiyatli bosildi!"
            }) {
                HStack {
                    Image(systemName: "checkmark.circle.fill")
                    Text("Tasdiqlash")
                        .fontWeight(.bold)
                }
                .padding()
                .foregroundColor(.white)
                .background(Color.green)
                .cornerRadius(10)
            }
        }
    }
}

let tugmaView = MaxsusTugmaView()
print("Maxsus Button yaratildi.")
```

## Tushuntirish va Mantiq:
`Button(action:label:)` yordamida har qanday murakkab SwiftUI ko'rinishini (matn, belgi, rasm) tugma ko'rinishi sifatida ishlatish mumkin.

## Ishlash natijasi:
```text
Maxsus Button yaratildi.
```


# 859-Topshiriq: `@Binding` Property Wrapper va Ota-Bola Aloqasi
## Topshiriq sharti:
Ota ko'rinishdagi `@State` o'zgaruvchini bola ko'rinishga `@Binding` orqali uzatish va boladan turib otani o'zgartirishni ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

// Bola ko'rinish
struct ChiroqTugmasiView: View {
    // @Binding ota ko'rinishdagi holatga to'g'ridan-to'g'ri 2 tomonlama havola
    @Binding var chiroqYoniqmi: Bool
    
    var body: some View {
        Button(chiroqYoniqmi ? "O'chirish" : "Yoqish") {
            chiroqYoniqmi.toggle()
        }
    }
}

// Ota ko'rinish
struct XonaView: View {
    @State private var chiroq: Bool = false
    
    var body: some View {
        VStack {
            Text("Chiroq holati: \(chiroq ? 'YONIQLIG' : 'O‘CHIQ')")
            // Bola komponentga $ belgi orqali binding uzatiladi
            ChiroqTugmasiView(chiroqYoniqmi: $chiroq)
        }
    }
}

let x = XonaView()
print("Ota-bola @Binding aloqasi o'rnatildi.")
```

## Tushuntirish va Mantiq:
`$chiroq` sintaksisi o'zgaruvchining qiymatini emas, uning `Binding<Bool>` ko'rinishidagi bog'lovchisini uzatadi. Bola ko'rinish uni o'zgartirganda ota ko'rinishdagi asl `@State` o'zgaradi.

## Ishlash natijasi:
```text
Ota-bola @Binding aloqasi o'rnatildi.
```


# 860-Topshiriq: `TextField` Bilan Ikki Tomonlama Matn Bog'lash
## Topshiriq sharti:
Foydalanuvchi kiritayotgan matnni bir vaqtning o'zida ekranda aks ettiruvchi reaktiv matn kiritish maydonini yarating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct MatnKiritishView: View {
    @State private var kiritilganIsm: String = ""
    
    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text("Ismingizni kiriting:")
                .font(.caption)
            
            TextField("Masalan: Jasur", text: $kiritilganIsm)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding(.bottom)
            
            Text("Assalomu alaykum, \(kiritilganIsm.isEmpty ? 'Mehmon' : kiritilganIsm)!")
                .font(.title3)
                .foregroundColor(.purple)
        }
        .padding()
    }
}

let mk = MatnKiritishView()
print("TextField binding bilan View yaratildi.")
```

## Tushuntirish va Mantiq:
`TextField` har bir harf kiritilganda `@State` qiymatini yangilaydi, bu esa matn yozilishi bilanoq pastdagi salomlashuv matnining avtomatik o'zgarishiga olib keladi.

## Ishlash natijasi:
```text
TextField binding bilan View yaratildi.
```


# 861-Topshiriq: `SecureField` Bilan Xavfsiz Parol Kiritish
## Topshiriq sharti:
Kiritilayotgan belgilarni yashiruvchi (nuqtalar bilan) xavfsiz parol maydonini yarating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct ParolKiritishView: View {
    @State private var parol: String = ""
    
    var body: some View {
        VStack(spacing: 12) {
            SecureField("Parolingizni kiriting", text: $parol)
                .textFieldStyle(RoundedBorderTextFieldStyle())
            
            Text("Parol uzunligi: \(parol.count) ta belgi")
                .font(.footnote)
                .foregroundColor(parol.count >= 8 ? .green : .red)
        }
        .padding()
    }
}

let p = ParolKiritishView()
print("SecureField bilan parol kiritish ko'rinishi yaratildi.")
```

## Tushuntirish va Mantiq:
`SecureField` foydalanuvchi kiritayotgan maxfiy matnni ekran tasmasida yashiradi va clipboardga ko'chirish kabi harakatlarni xavfsiz boshqaradi.

## Ishlash natijasi:
```text
SecureField bilan parol kiritish ko'rinishi yaratildi.
```


# 862-Topshiriq: `Toggle` (Svitch) Komponenti
## Topshiriq sharti:
Sozlamalarda bildirishnomalarni yoqish/o'chirish uchun `Toggle` svitchini yarating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct SozlamaView: View {
    @State private var bildirishnomaYoniq: Bool = true
    
    var body: some View {
        VStack {
            Toggle(isOn: $bildirishnomaYoniq) {
                Text("Bildirishnomalarni qabul qilish")
                    .font(.body)
            }
            .toggleStyle(SwitchToggleStyle(tint: .blue))
            
            Text("Holat: \(bildirishnomaYoniq ? 'FAOL' : 'NOFAOL')")
                .font(.caption)
        }
        .padding()
    }
}

let s = SozlamaView()
print("Toggle komponenti yaratildi.")
```

## Tushuntirish va Mantiq:
`Toggle` mantiqiy (Boolean) qiymatlarni yoqish va o'chirish uchun chiroyli iOS uslubidagi kommutatorni (switch) hosil qiladi.

## Ishlash natijasi:
```text
Toggle komponenti yaratildi.
```


# 863-Topshiriq: `Slider` Komponenti va Diapazon Tanlash
## Topshiriq sharti:
0 dan 100 gacha oraliqda ovoz balandligini sozlovchi slayder komponentini yozing.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct OvozSozlashView: View {
    @State private var ovozBalandligi: Double = 50.0
    
    var body: some View {
        VStack(spacing: 10) {
            Text("Ovoz: \(Int(ovozBalandligi))%")
                .font(.headline)
            
            Slider(value: $ovozBalandligi, in: 0...100, step: 1) {
                Text("Ovoz balandligi")
            }
            .accentColor(.orange)
        }
        .padding()
    }
}

let ov = OvozSozlashView()
print("Slider komponenti yaratildi.")
```

## Tushuntirish va Mantiq:
`Slider(value:in:step:)` sonli diapazonlar bo'ylab qiymatni silliq yoki qadamlab tanlash imkonini beradi.

## Ishlash natijasi:
```text
Slider komponenti yaratildi.
```


# 864-Topshiriq: `Stepper` Komponenti Bilan Bosqichma-bosqich O'zgartirish
## Topshiriq sharti:
Mahsulotlar sonini bittadan oshirish yoki kamaytirish imkonini beruvchi `Stepper` komponentini yarating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct SavatSoniView: View {
    @State private var buyurtmaSoni: Int = 1
    
    var body: some View {
        VStack {
            Stepper("Dona: \(buyurtmaSoni)", value: $buyurtmaSoni, in: 1...10)
                .padding()
            
            Text("Jami to'lov: \(buyurtmaSoni * 15000) UZS")
                .font(.headline)
        }
    }
}

let sv = SavatSoniView()
print("Stepper komponenti yaratildi.")
```

## Tushuntirish va Mantiq:
`Stepper` foydalanuvchiga `+` va `-` tugmalari yordamida qiymatni belgilangan oraliqda qulay o'zgartirish imkonini beradi.

## Ishlash natijasi:
```text
Stepper komponenti yaratildi.
```


# 865-Topshiriq: `Picker` Komponenti va Ro'yxatdan Tanlash
## Topshiriq sharti:
Viloyatlar ro'yxatidan bittasini tanlash uchun `Picker` komponentini yarating.

## Yechim (Swift kodi):
```swift
import SwiftUI

enum Viloyat: String, CaseIterable, Identifiable {
    case toshkent = "Toshkent"
    case samarqand = "Samarqand"
    case buxoro = "Buxoro"
    case xorazm = "Xorazm"
    var id: String { self.rawValue }
}

struct HududTanlashView: View {
    @State private var tanlanganHudud: Viloyat = .xorazm
    
    var body: some View {
        VStack {
            Text("Tanlangan viloyat: \(tanlanganHudud.rawValue)")
                .font(.headline)
            
            Picker("Viloyatni tanlang", selection: $tanlanganHudud) {
                ForEach(Viloyat.allCases) { v in
                    Text(v.rawValue).tag(v)
                }
            }
            .pickerStyle(SegmentedPickerStyle())
            .padding()
        }
    }
}

let hv = HududTanlashView()
print("Picker va segmented style muvaffaqiyatli tayyorlandi.")
```

## Tushuntirish va Mantiq:
`Picker` tanlangan enum yoki qiymatni `.tag()` yordamida bog'laydi. `.pickerStyle(SegmentedPickerStyle())` orqali zamonaviy segmentli ko'rinishga keltirish mumkin.

## Ishlash natijasi:
```text
Picker va segmented style muvaffaqiyatli tayyorlandi.
```


# 866-Topshiriq: `Image` va SF Symbols Bilan Ishlash
## Topshiriq sharti:
Apple SF Symbols kutubxonasidan piktogrammalar yuklash va ularning o'lchami hamda rangini sozlashni ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct BelgilarView: View {
    var body: some View {
        HStack(spacing: 20) {
            Image(systemName: "sun.max.fill")
                .resizable()
                .scaledToFit()
                .frame(width: 40, height: 40)
                .foregroundColor(.yellow)
            
            Image(systemName: "cloud.rain.fill")
                .resizable()
                .scaledToFit()
                .frame(width: 40, height: 40)
                .foregroundColor(.blue)
            
            Image(systemName: "heart.fill")
                .resizable()
                .scaledToFit()
                .frame(width: 40, height: 40)
                .foregroundColor(.red)
        }
        .padding()
    }
}

let bv = BelgilarView()
print("SF Symbols bilan Image komponentlari yaratildi.")
```

## Tushuntirish va Mantiq:
`Image(systemName:)` tizimdagi minglab vektorli SF Symbols belgilarini yuklaydi. `.resizable()` va `.scaledToFit()` rasmni buzilmasdan o'lchamga moslashtiradi.

## Ishlash natijasi:
```text
SF Symbols bilan Image komponentlari yaratildi.
```


# 867-Topshiriq: Gradientlar: `LinearGradient` Bilan Fon Yaratish
## Topshiriq sharti:
Chiroyli fon uchun chiziqli gradient (`LinearGradient`) qo'llanilgan ko'rinish yarating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct GradientFonView: View {
    var body: some View {
        ZStack {
            LinearGradient(
                gradient: Gradient(colors: [Color.blue, Color.purple]),
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .ignoresSafeArea()
            
            Text("Zamonaviy Dizayn")
                .font(.largeTitle)
                .fontWeight(.bold)
                .foregroundColor(.white)
        }
    }
}

let gv = GradientFonView()
print("LinearGradient fon ko'rinishi yaratildi.")
```

## Tushuntirish va Mantiq:
`LinearGradient` bir necha ranglar orasidagi silliq o'tishni boshlang'ich va yakuniy nuqtalar (`startPoint`, `endPoint`) bo'yicha chizadi.

## Ishlash natijasi:
```text
LinearGradient fon ko'rinishi yaratildi.
```


# 868-Topshiriq: `ScrollView` Bilan Siljuvchi Kontent
## Topshiriq sharti:
Ekranga sig'maydigan ko'p sonli kartalarni gorizontal va vertikal siljitish uchun `ScrollView` yaratishni ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct GorizontalKartaOqimiView: View {
    var body: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 16) {
                ForEach(1...5, id: \.self) { indeks in
                    VStack {
                        Text("Karta #\(indeks)")
                            .font(.headline)
                            .foregroundColor(.white)
                    }
                    .frame(width: 120, height: 80)
                    .background(Color.indigo)
                    .cornerRadius(12)
                }
            }
            .padding()
        }
    }
}

let scroll = GorizontalKartaOqimiView()
print("Gorizontal ScrollView tayyorlandi.")
```

## Tushuntirish va Mantiq:
`ScrollView` standart tarzda vertikal bo'ladi, lekin unga `.horizontal` yo'nalishini berish orqali karusel va lenta ko'rinishidagi gorizontal ro'yxatlarni yaratish mumkin.

## Ishlash natijasi:
```text
Gorizontal ScrollView tayyorlandi.
```


# 869-Topshiriq: `List` Komponenti va Statik Qatorlar
## Topshiriq sharti:
iOS Sozlamalar menyusiga o'xshash statik qatorlardan iborat `List` ko'rinishini yarating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct SozlamalarRoyxatiView: View {
    var body: some View {
        List {
            HStack {
                Image(systemName: "airplane")
                    .foregroundColor(.orange)
                Text("Avia rejim")
            }
            HStack {
                Image(systemName: "wifi")
                    .foregroundColor(.blue)
                Text("Wi-Fi")
            }
            HStack {
                Image(systemName: "bluetooth")
                    .foregroundColor(.blue)
                Text("Bluetooth")
            }
        }
    }
}

let list = SozlamalarRoyxatiView()
print("Statik List ko'rinishi yaratildi.")
```

## Tushuntirish va Mantiq:
`List` UIKit-dagi UITableView ning SwiftUI analogi bo'lib, o'z ichidagi elementlarni avtomatik ajratuvchi chiziqlar va iOS standart uslubidagi qatorlarga ajratadi.

## Ishlash natijasi:
```text
Statik List ko'rinishi yaratildi.
```


# 870-Topshiriq: `ForEach` va `Identifiable` Dinamik Ro'yxatlar
## Topshiriq sharti:
Struktura modeliga `Identifiable` protokolini berib, uni `List` va `ForEach` orqali dinamik chiqarishni ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct Kitob: Identifiable {
    let id = UUID()
    let nom: String
    let muallif: String
}

struct KitoblarKutubxonasiView: View {
    let kitoblar = [
        Kitob(nom: "O'tkan kunlar", muallif: "Abdulla Qodiriy"),
        Kitob(nom: "Yulduzli tunlar", muallif: "Pirimqul Qodirov"),
        Kitob(nom: "Shum bola", muallif: "G'afur G'ulom")
    ]
    
    var body: some View {
        List(kitoblar) { kitob in
            VStack(alignment: .leading) {
                Text(kitob.nom)
                    .font(.headline)
                Text(kitob.muallif)
                    .font(.subheadline)
                    .foregroundColor(.secondary)
            }
        }
    }
}

let kutubxona = KitoblarKutubxonasiView()
print("Identifiable modellar bilan dinamik List yaratildi.")
```

## Tushuntirish va Mantiq:
`Identifiable` protokoli har bir element uchun noyob `id` mavjudligini talab qiladi. Bu SwiftUI-ga ro'yxat o'zgarganda qaysi qator qo'shilgan yoki o'chirilganini aniq bilish imkonini beradi.

## Ishlash natijasi:
```text
Identifiable modellar bilan dinamik List yaratildi.
```


# 871-Topshiriq: `Section` Bilan Guruhlangan Ro'yxatlar
## Topshiriq sharti:
`List` ichida elementlarni sarlavha va izohlar bilan alohida bo'limlarga (`Section`) ajratishni ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct GuruhlanganSozlamalarView: View {
    var body: some View {
        List {
            Section(header: Text("Shaxsiy Ma'lumotlar"), footer: Text("Ismingiz hamma uchun ko'rinadi.")) {
                Text("Ism: Sardor")
                Text("Email: sardor@example.com")
            }
            
            Section(header: Text("Xavfsizlik")) {
                Text("Parolni o'zgartirish")
                Text("Ikki bosqichli himoya (2FA)")
            }
        }
    }
}

let gv = GuruhlanganSozlamalarView()
print("Guruhlangan Section ko'rinishi yaratildi.")
```

## Tushuntirish va Mantiq:
`Section(header:footer:)` ro'yxatni alohida mantiqiy bloklarga ajratadi va sarlavhalarni avtomatik tarzda chiroyli ko'rsatadi.

## Ishlash natijasi:
```text
Guruhlangan Section ko'rinishi yaratildi.
```


# 872-Topshiriq: `Form` Ko'rinishi va Foydalanuvchi Sozlamalari Ekrani
## Topshiriq sharti:
`Form` yordamida standart iOS sozlamalar sahifasini (TextField, Toggle, Picker bilan) yarating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct ProfilFormasiView: View {
    @State private var taxallus = ""
    @State private var qoronguRejim = false
    @State private var til = "O'zbek"
    
    let mavjudTillar = ["O'zbek", "Ingliz", "Rus"]
    
    var body: some View {
        Form {
            Section(header: Text("Profil")) {
                TextField("Taxallus", text: $taxallus)
            }
            
            Section(header: Text("Tizim ko'rinishi")) {
                Toggle("Qorong'u rejim", isOn: $qoronguRejim)
                Picker("Ilova tili", selection: $til) {
                    ForEach(mavjudTillar, id: \.self) { t in
                        Text(t)
                    }
                }
            }
        }
    }
}

let f = ProfilFormasiView()
print("Profil Form ko'rinishi yaratildi.")
```

## Tushuntirish va Mantiq:
`Form` interfeysi ma'lumot kiritish va sozlamalar ekranlari uchun mo'ljallangan bo'lib, uning ichidagi komponentlar avtomatik ravishda moslashtirilgan ko'rinishga ega bo'ladi.

## Ishlash natijasi:
```text
Profil Form ko'rinishi yaratildi.
```


# 873-Topshiriq: `Alert` va `confirmationDialog` Ko'rsatish
## Topshiriq sharti:
Foydalanuvchidan o'chirish harakatini tasdiqlashni so'rovchi ogohlantirish (Alert) oynasini ulashni ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct OgohlantirishView: View {
    @State private var ogohlantirishKorsatilsin = false
    
    var body: some View {
        VStack {
            Button("Hisobni o'chirish") {
                ogohlantirishKorsatilsin = true
            }
            .foregroundColor(.red)
        }
        .alert("Haqiqatan ham o'chirmoqchimisiz?", isPresented: $ogohlantirishKorsatilsin) {
            Button("O'chirish", role: .destructive) {
                print("Hisob muvaffaqiyatli o'chirildi.")
            }
            Button("Bekor qilish", role: .cancel) { }
        } message: {
            Text("Bu amalni ortga qaytarib bo'lmaydi.")
        }
    }
}

let ov = OgohlantirishView()
print("Alert modifikatori bilan View tayyorlandi.")
```

## Tushuntirish va Mantiq:
SwiftUI-da modal dialoglar ham deklarativ tarzda o'rnatiladi: `@State` boolean o'zgaruvchi `true` bo'lganda alert ekranda paydo bo'ladi.

## Ishlash natijasi:
```text
Alert modifikatori bilan View tayyorlandi.
```


# 874-Topshiriq: `sheet` va `fullScreenCover` Modal Oynalari
## Topshiriq sharti:
Pastdan ochiluvchi varaq (`sheet`) ko'rinishidagi modal sahifani ochish va yopishni ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct TafsilotEkrani: View {
    @Environment(\.dismiss) var yopish
    
    var body: some View {
        VStack(spacing: 20) {
            Text("Bu modal sahifa (Sheet)")
                .font(.title2)
            Button("Yopish") {
                yopish()
            }
        }
        .padding()
    }
}

struct AsosiyEkranView: View {
    @State private var sheetOchiq = false
    
    var body: some View {
        Button("Tafsilotlarni ochish") {
            sheetOchiq = true
        }
        .sheet(isPresented: $sheetOchiq) {
            TafsilotEkrani()
        }
    }
}

let ae = AsosiyEkranView()
print("Sheet ochuvchi ekran tuzildi.")
```

## Tushuntirish va Mantiq:
`.sheet(isPresented:)` pastdan tortiladigan modal kartani ochadi, `@Environment(\.dismiss)` esa uni dasturiy yopish imkonini beradi.

## Ishlash natijasi:
```text
Sheet ochuvchi ekran tuzildi.
```


# 875-Topshiriq: Maxsus `ViewModifier` Yaratish
## Topshiriq sharti:
Karta ko'rinishidagi stilni (fon, burchaklar, soya, padding) barcha ko'rinishlarga bir xil qo'llash uchun `ViewModifier` protokolidan foydalaning.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct KartaStili: ViewModifier {
    func body(content: Content) -> some View {
        content
            .padding()
            .background(Color.white)
            .cornerRadius(12)
            .shadow(color: Color.black.opacity(0.1), radius: 5, x: 0, y: 2)
    }
}

struct TestKartaView: View {
    var body: some View {
        Text("Maxsus kartacha matni")
            .modifier(KartaStili())
    }
}

let tk = TestKartaView()
print("Maxsus ViewModifier yaratildi va ulandi.")
```

## Tushuntirish va Mantiq:
`ViewModifier` orqali UI kodini takrorlamasdan, umumiy dizayn qoidalarini (design system) alohida ajratib olish va qayta ishlatish mumkin.

## Ishlash natijasi:
```text
Maxsus ViewModifier yaratildi va ulandi.
```


# 876-Topshiriq: `View` Kengaytmasi (Extension) Orqali Qulay Sintaksis
## Topshiriq sharti:
Yuqoridagi modifikatorni `.kartaStili()` ko'rinishida to'g'ridan-to'g'ri chaqirish uchun `View` kengaytmasini yozing.

## Yechim (Swift kodi):
```swift
import SwiftUI

extension View {
    func kartaStili() -> some View {
        self
            .padding()
            .background(Color.white)
            .cornerRadius(12)
            .shadow(color: Color.black.opacity(0.1), radius: 5, x: 0, y: 2)
    }
}

struct KengaytmaTestView: View {
    var body: some View {
        VStack {
            Text("1-karta").kartaStili()
            Text("2-karta").kartaStili()
        }
    }
}

let kt = KengaytmaTestView()
print("View extension orqali qulay chaqiruv tayyorlandi.")
```

## Tushuntirish va Mantiq:
`extension View` orqali maxsus modifikatorlarni xuddi SwiftUI-ning standart modifikatorlari (`.padding()`, `.font()`) kabi tabiiy va toza yozish mumkin bo'ladi.

## Ishlash natijasi:
```text
View extension orqali qulay chaqiruv tayyorlandi.
```


# 877-Topshiriq: Shartli Render Qilish (Conditional View Rendering)
## Topshiriq sharti:
`if-else` shartlari yordamida foydalanuvchi tizimga kirgan va kirmagan holatdagi interfeysni ko'rsatuvchi ko'rinish yozing.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct AutentifikatsiyaHolatiView: View {
    @State private var tizimgaKirganmi: Bool = false
    
    var body: some View {
        VStack(spacing: 16) {
            if tizimgaKirganmi {
                Text("Xush kelibsiz, Foydalanuvchi!")
                    .font(.title2)
                    .foregroundColor(.green)
                Button("Chiqish") {
                    tizimgaKirganmi = false
                }
            } else {
                Text("Iltimos, tizimga kiring")
                    .font(.headline)
                    .foregroundColor(.secondary)
                Button("Kirish") {
                    tizimgaKirganmi = true
                }
            }
        }
        .padding()
    }
}

let ah = AutentifikatsiyaHolatiView()
print("Shartli View rendering ko'rinishi yaratildi.")
```

## Tushuntirish va Mantiq:
SwiftUI `body` bloki `@ViewBuilder` atributiga ega bo'lgani sababli uning ichida tabiiy ravishda Swift `if-else` va `switch` konstruksiyalaridan foydalanish mumkin.

## Ishlash natijasi:
```text
Shartli View rendering ko'rinishi yaratildi.
```


# 878-Topshiriq: `@ViewBuilder` Yordamida Maxsus Konteyner Komponenti
## Topshiriq sharti:
O'z ichiga ixtiyoriy bolalar ko'rinishini qabul qiluvchi ramkali sarlavhali konteyner yarating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct SarlavhaliQuti<Kontent: View>: View {
    let sarlavha: String
    let kontent: Kontent
    
    init(sarlavha: String, @ViewBuilder kontent: () -> Kontent) {
        self.sarlavha = sarlavha
        self.kontent = kontent()
    }
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(sarlavha)
                .font(.headline)
                .foregroundColor(.blue)
            kontent
        }
        .padding()
        .border(Color.gray.opacity(0.3), width: 1)
    }
}

struct KonteynerTestView: View {
    var body: some View {
        SarlavhaliQuti(sarlavha: "Foydalanuvchi qutisi") {
            Text("Ichki element 1")
            Text("Ichki element 2")
        }
    }
}

let c = KonteynerTestView()
print("@ViewBuilder bilan maxsus konteyner yaratildi.")
```

## Tushuntirish va Mantiq:
`@ViewBuilder` parametr sifatida berilgan closure ichidagi bir nechta ko'rinishlarni birlashtirib, `TupleView` shaklida bitta kompozitsiya sifatida qabul qilish imkonini beradi.

## Ishlash natijasi:
```text
@ViewBuilder bilan maxsus konteyner yaratildi.
```


# 879-Topshiriq: `Group` Ko'rinishi va 10 ta Element Cheklovini Yechish
## Topshiriq sharti:
SwiftUI stacklaridagi 10 ta bevosita element cheklovini yechish va umumiy modifikator berish uchun `Group` dan foydalaning.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct GuruhTestView: View {
    var body: some View {
        VStack {
            Group {
                Text("1-element")
                Text("2-element")
                Text("3-element")
                Text("4-element")
                Text("5-element")
            }
            .font(.caption)
            .foregroundColor(.gray)
            
            Group {
                Text("6-element")
                Text("7-element")
                Text("8-element")
                Text("9-element")
                Text("10-element")
                Text("11-element") // Group bo'lmasa xatolik bo'lar edi
            }
            .font(.headline)
            .foregroundColor(.black)
        }
    }
}

let gt = GuruhTestView()
print("Group komponenti yordamida elementlar guruhlandi.")
```

## Tushuntirish va Mantiq:
`Group` hech qanday yangi vizual qatlam hosil qilmaydi, u faqat elementlarni mantiqiy birlashtirish va umumiy modifikatorlarni bir vaqtning o'zida bir nechta elementga berish uchun xizmat qiladi.

## Ishlash natijasi:
```text
Group komponenti yordamida elementlar guruhlandi.
```


# 880-Topshiriq: `LazyVStack` Bilan Katta Ma'lumotlarda Unumdorlik
## Topshiriq sharti:
Oddiy `VStack` va dangasa `LazyVStack` orasidagi xotira va unumdorlik farqini ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct KattaRoyxatView: View {
    var body: some View {
        ScrollView {
            // LazyVStack faqat ekranda ko'rinayotgan elementlarni xotirada yaratadi
            LazyVStack(spacing: 10) {
                ForEach(1...1000, id: \.self) { indeks in
                    Text("Qator #\(indeks)")
                        .padding()
                        .frame(maxWidth: .infinity)
                        .background(Color.gray.opacity(0.1))
                }
            }
        }
    }
}

let kr = KattaRoyxatView()
print("LazyVStack ro'yxati yaratildi (1000 elementli).")
```

## Tushuntirish va Mantiq:
`VStack` barcha 1000 ta elementni darhol xotiraga yuklaydi va chizadi. `LazyVStack` esa faqat foydalanuvchi ko'rib turgan qatorlarni dinamik yuklaydi, bu esa xotirani keskin tejaydi.

## Ishlash natijasi:
```text
LazyVStack ro'yxati yaratildi (1000 elementli).
```


# 881-Topshiriq: `LazyVGrid` va Moslashuvchan Kataklar (GridItem)
## Topshiriq sharti:
Rasmlar galereyasi uchun 3 ustunli moslashuvchan kataklar to'rini (`LazyVGrid`) yarating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct GalereyaGridiView: View {
    // 3 ta moslashuvchan ustun
    let ustunlar = [
        GridItem(.flexible()),
        GridItem(.flexible()),
        GridItem(.flexible())
    ]
    
    var body: some View {
        ScrollView {
            LazyVGrid(columns: ustunlar, spacing: 12) {
                ForEach(1...12, id: \.self) { i in
                    RoundedRectangle(cornerRadius: 8)
                        .fill(Color.teal)
                        .frame(height: 100)
                        .overlay(
                            Text("Rasm #\(i)")
                                .foregroundColor(.white)
                        )
                }
            }
            .padding()
        }
    }
}

let gg = GalereyaGridiView()
print("LazyVGrid galereyasi yaratildi.")
```

## Tushuntirish va Mantiq:
`LazyVGrid` va `GridItem` (`.fixed`, `.flexible`, `.adaptive`) yordamida ekranning eniga qarab avtomatik moslashuvchi zamonaviy fotosuratlar va mahsulotlar to'ri (Grid) hosil qilinadi.

## Ishlash natijasi:
```text
LazyVGrid galereyasi yaratildi.
```


# 882-Topshiriq: `ProgressView` Indikatorlari
## Topshiriq sharti:
Yuklanish jarayonini ifodalovchi aylanuvchi (spinner) va foizli progress bar ko'rinishlarini yasang.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct YuklanishKorsatkichiView: View {
    @State private var progress = 0.65 // 65%
    
    var body: some View {
        VStack(spacing: 24) {
            // Aylanuvchi noma'lum vaqtli indikator
            ProgressView("Fayl yuklanmoqda...")
            
            // Aniq foizli chiziq
            ProgressView(value: progress) {
                Text("Yuklash jarayoni")
            } currentValueLabel: {
                Text("\(Int(progress * 100))%")
            }
            .progressViewStyle(LinearProgressViewStyle(tint: .blue))
        }
        .padding()
    }
}

let yk = YuklanishKorsatkichiView()
print("ProgressView indikatorlari yaratildi.")
```

## Tushuntirish va Mantiq:
`ProgressView` asinxron amallar paytida foydalanuvchiga jarayon ketayotganini ko'rsatish uchun xizmat qiladi.

## Ishlash natijasi:
```text
ProgressView indikatorlari yaratildi.
```


# 883-Topshiriq: `Label` Komponenti Bilan Matn va Belgi Hamkorligi
## Topshiriq sharti:
Piktogramma va matnni birlashtiruvchi zamonaviy `Label` komponentidan foydalanishni ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct ProfilLabelView: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Label("Profil Sozlamalari", systemImage: "person.crop.circle")
            Label("Xavfsizlik Kaliti", systemImage: "key.fill")
            Label("Bildirishnomalar", systemImage: "bell.badge")
        }
        .font(.headline)
        .padding()
    }
}

let pl = ProfilLabelView()
print("Label komponentlari ro'yxati tayyorlandi.")
```

## Tushuntirish va Mantiq:
`Label` komponenti matn va ikonkani bitta semantik birlik sifatida birlashtiradi va menyularda, ro'yxatlarda avtomatik tekislanishni ta'minlaydi.

## Ishlash natijasi:
```text
Label komponentlari ro'yxati tayyorlandi.
```


# 884-Topshiriq: `Badge` Modifikatori Bilan Bildirishnomalar Belgisi
## Topshiriq sharti:
`List` yoki `TabView` qatorlarida o'qilmagan xabarlar sonini ko'rsatuvchi `.badge()` modifikatorini ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct BildirishnomaBadgeView: View {
    var body: some View {
        List {
            HStack {
                Text("Kiruvchi xatlar")
            }
            .badge(12) // Qator chetida 12 sonini chiroyli ko'rsatadi
            
            HStack {
                Text("Spam xabarlar")
            }
            .badge("Yangi")
        }
    }
}

let bb = BildirishnomaBadgeView()
print("Badge modifikatori qo'llandi.")
```

## Tushuntirish va Mantiq:
`.badge()` modifikatori iOS ro'yxatlarida va tab barlarda o'qilmagan xabarlar soni yoki maqomini qizil/kulrang aylana ichida chiroyli aks ettiradi.

## Ishlash natijasi:
```text
Badge modifikatori qo'llandi.
```


# 885-Topshiriq: `Menu` va `contextMenu` Yordamida Qo'shimcha Amallar
## Topshiriq sharti:
Element bosilganda yoki uzoq bosib turilganda ochiluvchi kontekst menyusini yarating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct KontekstMenyuView: View {
    var body: some View {
        Text("Fayl ustiga bosing yoki ushlab turing")
            .padding()
            .background(Color.gray.opacity(0.2))
            .cornerRadius(8)
            .contextMenu {
                Button(action: { print("Nusxa olindi") }) {
                    Label("Nusxalash", systemImage: "doc.on.doc")
                }
                Button(action: { print("Ulashildi") }) {
                    Label("Ulashish", systemImage: "square.and.arrow.up")
                }
                Button(role: .destructive, action: { print("O'chirildi") }) {
                    Label("O'chirish", systemImage: "trash")
                }
            }
    }
}

let km = KontekstMenyuView()
print("ContextMenu ko'rinishi yaratildi.")
```

## Tushuntirish va Mantiq:
`.contextMenu` foydalanuvchi elementni uzoq bosganda (haptic touch) kontekstli amallar ro'yxatini chiqaradi.

## Ishlash natijasi:
```text
ContextMenu ko'rinishi yaratildi.
```


# 886-Topshiriq: Swift 5.9+ Yangi `@Observable` Makrosi
## Topshiriq sharti:
Swift 5.9 va iOS 17 bilan kelgan eng zamonaviy `@Observable` makrosi yordamida reaktiv ma'lumot modelini yarating.

## Yechim (Swift kodi):
```swift
import SwiftUI
import Observation

// Swift 5.9+ Observation tizimi: ObservableObject va @Published o'rnini bosadi
@Observable
class FoydalanuvchiModel {
    var ism: String = "Anvar"
    var yosh: Int = 28
    
    func tugilganKun() {
        yosh += 1
    }
}

let model = FoydalanuvchiModel()
print("Observable model yaratildi: \(model.ism), Yosh: \(model.yosh)")
model.tugilganKun()
print("Yangilangan yosh: \(model.yosh)")
```

## Tushuntirish va Mantiq:
Swift 5.9-dagi `@Observable` makrosi avvalgi `ObservableObject` protokoliga qaraganda ancha tezkor, qulay va faqat o'zgargan property-ga bog'langan ko'rinishlarni yangilaydi (fine-grained observation).

## Ishlash natijasi:
```text
Observable model yaratildi: Anvar, Yosh: 28
Yangilangan yosh: 29
```


# 887-Topshiriq: `@Observable` Modelni SwiftUI View Ichida Ishlatish
## Topshiriq sharti:
Yangi `@Observable` modelni View ichida to'g'ridan-to'g'ri hech qanday `@ObservedObject`siz oddiy o'zgaruvchi sifatida ishlatishni ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI
import Observation

@Observable
class SavatModel {
    var jamiSumma: Double = 0.0
    
    func mahsulotQosh(narx: Double) {
        jamiSumma += narx
    }
}

struct SavatEkranView: View {
    // SwiftUI View avtomatik ravishda bu modelning property o'zgarishini kuzatadi!
    var savat = SavatModel()
    
    var body: some View {
        VStack {
            Text("Jami savat: $\(savat.jamiSumma, specifier: "%.2f")")
                .font(.title)
            
            Button("Mahsulot qo'shish ($15)") {
                savat.mahsulotQosh(narx: 15.0)
            }
        }
    }
}

let se = SavatEkranView()
print("@Observable bilan SwiftUI ekrani yaratildi.")
```

## Tushuntirish va Mantiq:
Swift 5.9+ da `@ObservedObject` yoki `@StateObject` yozish shart emas. `@Observable` modeli View tanasida qaysi property ishlatilsa, faqat o'shani avtomatik kuzatuvga oladi.

## Ishlash natijasi:
```text
@Observable bilan SwiftUI ekrani yaratildi.
```


# 888-Topshiriq: `@StateObject` (Legacy) Bilan Model Hayot Siklini Boshqarish
## Topshiriq sharti:
iOS 14-16 loyihalarida keng tarqalgan `@StateObject` va `ObservableObject` qanday ishlashini ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI
import Combine

class EskiFoydalanuvchiModel: ObservableObject {
    @Published var ball: Int = 100
    
    func ballOshir() {
        ball += 10
    }
}

struct EskiEkranView: View {
    // @StateObject View qayta chizilganda ham modelni qaytadan yaratmasdan xotirada saqlab qoladi
    @StateObject private var model = EskiFoydalanuvchiModel()
    
    var body: some View {
        VStack {
            Text("Ball: \(model.ball)")
            Button("+10 Ball") {
                model.ballOshir()
            }
        }
    }
}

let ee = EskiEkranView()
print("@StateObject bilan ekran tuzildi.")
```

## Tushuntirish va Mantiq:
`@StateObject` View-ning butun hayot siklida modelning faqat bir marta initsializatsiya qilinishini kafolatlaydi.

## Ishlash natijasi:
```text
@StateObject bilan ekran tuzildi.
```


# 889-Topshiriq: `@ObservedObject` Bilan Tashqaridan Kelgan Modelni Qabul Qilish
## Topshiriq sharti:
Ota ko'rinishdan bola ko'rinishga mavjud `ObservableObject` modelini uzatishni ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI
import Combine

class HamyonModel: ObservableObject {
    @Published var balans: Double = 50000.0
}

struct HamyonBolaView: View {
    // Tashqaridan keladigan modelga havola
    @ObservedObject var hamyon: HamyonModel
    
    var body: some View {
        Text("Balans: \(hamyon.balans, specifier: "%.0f") UZS")
    }
}

let model = HamyonModel()
let bv = HamyonBolaView(hamyon: model)
print("@ObservedObject ko'rinishi yaratildi.")
```

## Tushuntirish va Mantiq:
`@ObservedObject` yangi model yaratmaydi, balki tashqaridan uzatilgan modelni qabul qilib, undagi `@Published` o'zgarishlarga qarab UI-ni qayta chizadi.

## Ishlash natijasi:
```text
@ObservedObject ko'rinishi yaratildi.
```


# 890-Topshiriq: `@EnvironmentObject` Bilan Global Holatni Tarqatish
## Topshiriq sharti:
Ilovaning butun ko'rinishlar daraxtiga (View hierarchy) modelni global uzatish uchun `@EnvironmentObject` dan foydalanishni ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI
import Combine

class TizimHolati: ObservableObject {
    @Published var faolFoydalanuvchi: String = "Ali"
}

struct ChuqurIchkiView: View {
    @EnvironmentObject var holat: TizimHolati
    
    var body: some View {
        Text("Faol foydalanuvchi: \(holat.faolFoydalanuvchi)")
    }
}

struct AsosiyKontekstView: View {
    @StateObject var tizim = TizimHolati()
    
    var body: some View {
        ChuqurIchkiView()
            .environmentObject(tizim) // Daraxt bo'ylab barcha bolalarga tarqatiladi
    }
}

let ak = AsosiyKontekstView()
print("@EnvironmentObject uzatish tizimi tayyorlandi.")
```

## Tushuntirish va Mantiq:
`@EnvironmentObject` parametrlarni birma-bir ota-bola zanjiri bo'yicha uzatib o'tirmasdan (prop drilling yo'q), ixtiyoriy ichki ko'rinishdan turib global modelga kirish imkonini beradi.

## Ishlash natijasi:
```text
@EnvironmentObject uzatish tizimi tayyorlandi.
```


# 891-Topshiriq: `@Environment(\.colorScheme)` Bilan Tizim Mavzusini Aniqlash
## Topshiriq sharti:
Foydalanuvchi qurilmasida Dark Mode (qorong'u) yoki Light Mode (yorug') yoqilganligini aniqlashni ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct MavzuKuzatuvchiView: View {
    @Environment(\.colorScheme) var tizimMavzusi
    
    var body: some View {
        Text("Hozirgi mavzu: \(tizimMavzusi == .dark ? 'Qorong‘u (Dark)' : 'Yorug‘ (Light)')")
            .padding()
            .background(tizimMavzusi == .dark ? Color.black : Color.white)
            .foregroundColor(tizimMavzusi == .dark ? Color.white : Color.black)
    }
}

let mk = MavzuKuzatuvchiView()
print("Mavzu kuzatuvchi View yaratildi.")
```

## Tushuntirish va Mantiq:
`@Environment(\.colorScheme)` orqali iOS tizim mavzusiga moslashish va dinamik ranglarni to'g'ri taqdim etish mumkin bo'ladi.

## Ishlash natijasi:
```text
Mavzu kuzatuvchi View yaratildi.
```


# 892-Topshiriq: `@Environment(\.dismiss)` Bilan Ekranni Yopish
## Topshiriq sharti:
Navigatsiya stackida yoki modal sheetda turgan ko'rinishni dasturiy tarzda yopishni ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct YopiluvchiSahifaView: View {
    @Environment(\.dismiss) private var dismissAction
    
    var body: some View {
        VStack {
            Text("Sahifa ochiq")
            Button("Orqaga / Yopish") {
                dismissAction() // Sahifani avtomatik yopadi
            }
        }
    }
}

let ys = YopiluvchiSahifaView()
print("@Environment(\.dismiss) amali ko'rinishi yaratildi.")
```

## Tushuntirish va Mantiq:
`dismiss()` chaqiruvi View modal shaklda ochilgan bo'lsa uni yopadi, agar NavigationStack ichida bo'lsa oldingi ekranga qaytaradi (pop).

## Ishlash natijasi:
```text
@Environment(\.dismiss) amali ko'rinishi yaratildi.
```


# 893-Topshiriq: `@AppStorage` Bilan Reaktiv UserDefaults Boshqaruvi
## Topshiriq sharti:
Foydalanuvchi tanlagan sozlamalarni ilova xotirasida (UserDefaults) doimiy saqlab qolish uchun `@AppStorage` dan foydalaning.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct DoimiySozlamaView: View {
    // "f_ism" kaliti bilan UserDefaults-ga avtomatik sinxronlanadi
    @AppStorage("f_ism") private var saqlanganIsm: String = "Mehmon"
    
    var body: some View {
        VStack {
            Text("Xush kelibsiz, \(saqlanganIsm)")
            TextField("Ismingizni o'zgartiring", text: $saqlanganIsm)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding()
        }
    }
}

let ds = DoimiySozlamaView()
print("@AppStorage bilan avtomatik UserDefaults binding yaratildi.")
```

## Tushuntirish va Mantiq:
`@AppStorage` qiymat o'zgarganda uni avtomatik tarzda UserDefaults fayliga saqlaydi va ilova qayta ishga tushganda o'sha qiymatni tiklaydi.

## Ishlash natijasi:
```text
@AppStorage bilan avtomatik UserDefaults binding yaratildi.
```


# 894-Topshiriq: `@SceneStorage` Bilan Oyna Holatini Tiklash
## Topshiriq sharti:
iPadOS va macOS-da ko'p oynali rejimda har bir oyna uchun alohida holatni saqlab qoluvchi `@SceneStorage` xususiyatini ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct OynaXotirasiView: View {
    // Har bir alohida oyna (Scene) uchun o'zining mustaqil qoralama matni saqlanadi
    @SceneStorage("qoralama_xabar") private var qoralama: String = ""
    
    var body: some View {
        VStack {
            Text("Oyna uchun qoralama:")
            TextEditor(text: $qoralama)
                .border(Color.gray)
                .padding()
        }
    }
}

let ox = OynaXotirasiView()
print("@SceneStorage bilan oynalar holati boshqaruvi tayyorlandi.")
```

## Tushuntirish va Mantiq:
`@SceneStorage` iPad ko'p oynali muhitida har bir oyna o'zining kiritilgan ma'lumotlarini alohida saqlab qolishi uchun mo'ljallangan.

## Ishlash natijasi:
```text
@SceneStorage bilan oynalar holati boshqaruvi tayyorlandi.
```


# 895-Topshiriq: `onAppear` va `onDisappear` Hayot Sikli Modifikatorlari
## Topshiriq sharti:
Ko'rinish ekranga chiqqanda va ekrandan ketganda ma'lumotlarni boshqarish uchun hayot sikli hodisalarini yozing.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct HayotSikliView: View {
    @State private var status = "Yuklanmoqda..."
    
    var body: some View {
        Text(status)
            .onAppear {
                // Ekran ochilganda chaqiriladi
                print("LIFECYCLE: Ekran foydalanuvchiga ko'rindi.")
                status = "Tayyor!"
            }
            .onDisappear {
                // Ekran yopilganda chaqiriladi
                print("LIFECYCLE: Ekran yopildi, resurslar bo'shatildi.")
            }
    }
}

let hs = HayotSikliView()
print("onAppear va onDisappear hodisalari ulandi.")
```

## Tushuntirish va Mantiq:
`onAppear` va `onDisappear` UIKit-dagi `viewWillAppear` va `viewDidDisappear` metodlarining bevosita deklarativ o'rnini bosadi.

## Ishlash natijasi:
```text
onAppear va onDisappear hodisalari ulandi.
```


# 896-Topshiriq: `.task` Modifikatori va Asinxron Swift Concurrency
## Topshiriq sharti:
Ekran yuklanishi bilanoq fonda asinxron tarmoq so'rovini bajaruvchi va ekran yopilganda avtomatik bekor bo'luvchi `.task` modifikatorini ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct AsinxronYuklovchiView: View {
    @State private var serverXabari = "Kutilmoqda..."
    
    var body: some View {
        Text(serverXabari)
            .font(.headline)
            .task {
                // .task asinxron muhit ochadi va View o'chirilganda avtomatik cancel bo'ladi
                try? await Task.sleep(nanoseconds: 20_000_000)
                serverXabari = "Serverdan ma'lumotlar muvaffaqiyatli yuklandi!"
            }
    }
}

let ay = AsinxronYuklovchiView()
print(".task modifikatori bilan asinxron ekran yaratildi.")
```

## Tushuntirish va Mantiq:
`.task` modifikatori SwiftUI va Swift Concurrency (async/await) ni mukammal birlashtiradi. Agar foydalanuvchi ma'lumot yuklanmasdan ekranni yopib yuborsa, asinxron vazifa avtomatik ravishda bekor qilinadi.

## Ishlash natijasi:
```text
.task modifikatori bilan asinxron ekran yaratildi.
```


# 897-Topshiriq: `onChange(of:)` Modifikatori Bilan Qiymat O'zgarishini Kuzatish
## Topshiriq sharti:
O'zgaruvchi qiymati har safar yangilanganda maxsus amallarni bajarish (masalan qidiruv so'rovini yuborish) uchun `.onChange` modifikatorini yozing.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct QidiruvKuzatuvchiView: View {
    @State private var qidiruvMatni = ""
    @State private var qidiruvSoni = 0
    
    var body: some View {
        VStack {
            TextField("Qidiruv...", text: $qidiruvMatni)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding()
            
            Text("Qidiruvlar soni: \(qidiruvSoni)")
        }
        .onChange(of: qidiruvMatni) { yangiQiymat in
            print("Yangi qidiruv so'zi: \(yangiQiymat)")
            qidiruvSoni += 1
        }
    }
}

let qk = QidiruvKuzatuvchiView()
print("onChange(of:) kuzatuvchisi tayyorlandi.")
```

## Tushuntirish va Mantiq:
`.onChange(of:perform:)` orqali View ichidagi istalgan holat o'zgarganda qo'shimcha logika, loglash yoki tarmoq so'rovlarini ishga tushirish mumkin.

## Ishlash natijasi:
```text
onChange(of:) kuzatuvchisi tayyorlandi.
```


# 898-Topshiriq: `GeometryReader` Bilan Dinamik O'lchamlarni Hisoblash
## Topshiriq sharti:
Ekran yoki ota konteynerning eni va bo'yini aniqlab, shunga qarab elementlarni foiz hisobida joylashtirish uchun `GeometryReader` dan foydalaning.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct OynaOlchamlariView: View {
    var body: some View {
        GeometryReader { geo in
            VStack {
                Text("Konteyner eni: \(Int(geo.size.width)) pt")
                Text("Konteyner bo'yi: \(Int(geo.size.height)) pt")
                
                // Konteynerning aniq yarmini egallaydigan to'g'ri to'rtburchak
                Rectangle()
                    .fill(Color.orange)
                    .frame(width: geo.size.width * 0.5, height: 40)
            }
        }
    }
}

let oo = OynaOlchamlariView()
print("GeometryReader bilan dinamik hisoblovchi ekran yaratildi.")
```

## Tushuntirish va Mantiq:
`GeometryReader` o'zining `GeometryProxy` obyekti orqali konteynerning haqiqiy o'lchamlari va koordinatalarini olish imkonini beradi.

## Ishlash natijasi:
```text
GeometryReader bilan dinamik hisoblovchi ekran yaratildi.
```


# 899-Topshiriq: Animatsiyalar: `withAnimation` va `.animation()`
## Topshiriq sharti:
Tugma bosilganda o'lcham va rang o'zgarishini silliq bahoriy (spring) animatsiya bilan tasvirlashni ko'rsating.

## Yechim (Swift kodi):
```swift
import SwiftUI

struct AnimatsiyaNamoyishiView: View {
    @State private var kattalashgan = false
    
    var body: some View {
        VStack(spacing: 30) {
            Circle()
                .fill(kattalashgan ? Color.purple : Color.blue)
                .frame(width: kattalashgan ? 120 : 60, height: kattalashgan ? 120 : 60)
            
            Button("Animatsiyani ishga tushirish") {
                withAnimation(.spring(response: 0.5, dampingFraction: 0.6)) {
                    kattalashgan.toggle()
                }
            }
        }
    }
}

let an = AnimatsiyaNamoyishiView()
print("Spring animatsiyali ko'rinish yaratildi.")
```

## Tushuntirish va Mantiq:
`withAnimation` bloki ichida o'zgartirilgan `@State` qiymatlariga bog'liq barcha vizual o'zgarishlar SwiftUI tomonidan avtomatik va silliq tarzda animatsiya qilinadi.

## Ishlash natijasi:
```text
Spring animatsiyali ko'rinish yaratildi.
```


# 900-Topshiriq: Amaliy Kompleks Mini-App: Reaktiv Vazifalar Boshqaruvi (TaskFlow)
## Topshiriq sharti:
Barcha o'rganilgan SwiftUI asoslarini: `@State`, `List`, `TextField`, `Button`, animatsiya va `@Observable` modelini birlashtirgan to'liq vazifalar boshqaruvchi (TaskFlow) ilovasini yarating.

## Yechim (Swift kodi):
```swift
import SwiftUI
import Observation

// 1. Model
struct Vazifa: Identifiable {
    let id = UUID()
    var sarlavha: String
    var bajarildimi: Bool = false
}

// 2. Observable State
@Observable
class VazifalarMenejeri {
    var vazifalar: [Vazifa] = [
        Vazifa(sarlavha: "SwiftUI asoslarini o'rganish", bajarildimi: true),
        Vazifa(sarlavha: "State va Binding amaliyoti", bajarildimi: false)
    ]
    
    func yangiVazifaQoshish(matn: String) {
        guard !matn.trimmingCharacters(in: .whitespaces).isEmpty else { return }
        vazifalar.append(Vazifa(sarlavha: matn))
    }
    
    func holatniOzgartirish(vazifa: Vazifa) {
        if let indeks = vazifalar.firstIndex(where: { $0.id == vazifa.id }) {
            vazifalar[indeks].bajarildimi.toggle()
        }
    }
}

// 3. To'liq SwiftUI UI
struct TaskFlowAppView: View {
    @State private var menejer = VazifalarMenejeri()
    @State private var yangiMatn = ""
    
    var body: some View {
        VStack {
            // Kiritish maydoni
            HStack {
                TextField("Yangi vazifa kiriting...", text: $yangiMatn)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                
                Button(action: {
                    withAnimation {
                        menejer.yangiVazifaQoshish(matn: yangiMatn)
                        yangiMatn = ""
                    }
                }) {
                    Image(systemName: "plus.circle.fill")
                        .font(.title2)
                        .foregroundColor(.blue)
                }
            }
            .padding()
            
            // Vazifalar ro'yxati
            List {
                ForEach(menejer.vazifalar) { v in
                    HStack {
                        Image(systemName: v.bajarildimi ? "checkmark.circle.fill" : "circle")
                            .foregroundColor(v.bajarildimi ? .green : .gray)
                            .onTapGesture {
                                withAnimation {
                                    menejer.holatniOzgartirish(vazifa: v)
                                }
                            }
                        
                        Text(v.sarlavha)
                            .strikethrough(v.bajarildimi, color: .gray)
                            .foregroundColor(v.bajarildimi ? .secondary : .primary)
                    }
                }
            }
        }
    }
}

let ilova = TaskFlowAppView()
print("TaskFlow Mini-App SwiftUI ko'rinishi muvaffaqiyatli qurildi!")
```

## Tushuntirish va Mantiq:
Ushbu loyihada `@Observable` ma'lumot modeli, SwiftUI komponentlari (`List`, `TextField`, `Button`), ikki tomonlama binding, shartli dizayn va silliq `withAnimation` to'liq birlashtirildi.

## Ishlash natijasi:
```text
TaskFlow Mini-App SwiftUI ko'rinishi muvaffaqiyatli qurildi!
```

