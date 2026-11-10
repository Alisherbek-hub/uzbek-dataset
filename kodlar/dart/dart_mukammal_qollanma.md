# Dart Dasturlash Tili: Mukammal Qo'llanma va Ensiklopediya
## (Noldan Mobil Dasturlash, Flutter Ekotizimi, Sound Null Safety va On-Device AI)

> **Muallif:** Google Dart Jamoasi  
> **Standart:** Dart 3.x+ (Zamonaviy Standartlar)  
> **Asosiy yo'nalish:** Android, iOS, Web va Desktop uchun yagona kod bazasi (Flutter asosi) hamda mobil qurilmalarda AI modellarini ishlatish.

---

## MUNDARIJA

1. [1-Bob: Dart Falsafasi, JIT va AOT Kompilyatsiyasi](#1-bob)
2. [2-Bob: Sound Null Safety — Null Xatolaridan Butunlay Qutulish](#2-bob)
3. [3-Bob: O'zgaruvchilar: `var`, `final`, `const` va `late`](#3-bob)
4. [4-Bob: Kolleksiyalar: List, Set, Map va Dart 3 Records](#4-bob)
5. [5-Bob: Funksiyalar, Nomlangan Argumentlar va Closurelar](#5-bob)
6. [6-Bob: OOP: Konstruktorlar, Factory va Initializer Lists](#6-bob)
7. [7-Bob: Mixins (`with`) va Implitsit Interfeyslar (`implements`)](#7-bob)
8. [8-Bob: Asinxron Dasturlash: Event Loop, `Future` va `Stream`](#8-bob)
9. [9-Bob: Dart 3 Pattern Matching va Sealed Classes](#9-bob)
10. [10-Bob: Flutter bilan Aloqa va Reaktiv Arxitektura (State Management)](#10-bob)
11. [11-Bob: Maxsus Bob: Dart FFI orqali Mobil Qurilmada 1-Bit LLM Dvigateli](#11-bob)

---

<a name="1-bob"></a>
# 1-Bob: Dart Falsafasi, JIT va AOT Kompilyatsiyasi

Dart — bu bitta tilda ikkita kompilyatsiya rejimini birlashtirgan noyob texnologiyadir:
1. **JIT (Just-in-Time)**: Dasturni ishlab chiqish jarayonida (Development) kodni sekundning ulushida yangilash — **Hot Reload** imkonini beradi.
2. **AOT (Ahead-of-Time)**: Ishlab chiqarishga (Production) tayyor bo'lganda to'g'ridan-to'g'ri ARM yoki x86 mashina kodiga o'girilib, 60/120 FPS tezlikda ishlaydi.

```dart
void main() {
  print("Assalomu alaykum, Dart va Flutter dunyosi!");
}
```

---

<a name="2-bob"></a>
# 2-Bob: Sound Null Safety — Null Xatolaridan Butunlay Qutulish

Dart tilining eng katta yutug'i — bu **Sound Null Safety** tizimidir. O'zgaruvchilar standart holatda hech qachon `null` bo'la olmaydi. Bu esa dasturlarning kutilmagan "NullPointerException" tufayli qulashini 100% bartaraf etadi.

* `String nom = "Ali";` -> Hech qachon `null` bo'lmaydi.
* `String? sharif = null;` -> `?` orqali `null` bo'lishi mumkinligi bildiriladi.
* `sharif?.length` -> Xavfsiz chaqirish (Safe navigation).
* `sharif ?? "Noma'lum"` -> Agar null bo'lsa zaxira qiymat.

---

<a name="3-bob"></a>
# 3-Bob: O'zgaruvchilar: `var`, `final`, `const` va `late`

* `final`: Bir marta qiymat oladi va o'zgarmaydi (Runtime vaqtida hisoblanishi mumkin).
* `const`: Kompilyatsiya vaqtida qat'iy ma'lum bo'lgan mutlaq o'zgarmas doimiy qiymat.
* `late`: O'zgaruvchi keyinroq (birinchi murojaatda) initsializatsiya qilinishini kafolatlaydi.

```dart
final vaqt = DateTime.now(); // Runtime da aniqlanadi
const pi = 3.14159;          // Kompilyatsiyada ma'lum
late String malumot;
```

---

<a name="4-bob"></a>
# 4-Bob: Kolleksiyalar: List, Set, Map va Dart 3 Records

Dart da kolleksiyalar ichida shartli operatorlar (Collection `if` va Collection `for`) qo'llash juda qulay:
```dart
bool admin = true;
var navigatsiya = [
  "Bosh sahifa",
  "Profil",
  if (admin) "Boshqaruv paneli",
];
```

Dart 3 da kiritilgan **Records (Tuples)** orqali funksiyadan bir nechta qiymat qaytarish:
```dart
(String, int) odamni_ol() {
  return ("Jasur", 21);
}
```

---

<a name="5-bob"></a>
# 5-Bob: Funksiyalar, Nomlangan Argumentlar va Closurelar

Dart da parametrlar aniq nom bilan uzatilishi mumkin (Named Arguments):
```dart
void profilYarat({required String ism, int yosh = 18, String? shahar}) {
  print("Ism: $ism, Yosh: $yosh, Shahar: $shahar");
}

// Chaqirish
profilYarat(ism: "Alisher", shahar: "Toshkent");
```

---

<a name="6-bob"></a>
# 6-Bob: OOP: Konstruktorlar, Factory va Initializer Lists

Dart ning konstruktorlari juda ixcham:
```dart
class Foydalanuvchi {
  final String ism;
  final int ball;

  // Qisqa konstruktor
  Foydalanuvchi(this.ism, this.ball);

  // Nomlangan konstruktor
  Foydalanuvchi.boshlangich(String ism) : this(ism, 0);

  // Factory konstruktor (keshlangan yoki yangi obyekt qaytarish)
  factory Foydalanuvchi.fromJson(Map<String, dynamic> json) {
    return Foydalanuvchi(json['ism'] as String, json['ball'] as int);
  }
}
```

---

<a name="7-bob"></a>
# 7-Bob: Mixins (`with`) va Implitsit Interfeyslar (`implements`)

Dart da ko'p ota-onadan meros olish (Multiple Inheritance) o'rniga **Mixins** qo'llaniladi:
```dart
mixin Uchuvchi {
  void uchish() => print("Osmon uzra parvoz qilmoqda...");
}

class Qush with Uchuvchi {}
```

---

<a name="8-bob"></a>
# 8-Bob: Asinxron Dasturlash: Event Loop, `Future` va `Stream`

* `Future<T>`: Kelajakda bir marta qaytadigan qiymat (HTTP so'rov, fayl o'qish).
* `Stream<T>`: Vaqt davomida ketma-ket keluvchi ko'plab hodisalar oqimi (WebSockets, GPS signallari, AI token oqimi).

```dart
Future<String> serverdanYukla() async {
  await Future.delayed(Duration(milliseconds: 100));
  return "Ma'lumot keldi";
}

Stream<int> sonlarOqimi() async* {
  for (int i = 1; i <= 3; i++) {
    yield i;
  }
}
```

---

<a name="9-bob"></a>
# 9-Bob: Dart 3 Pattern Matching va Sealed Classes

Dart 3 da `switch` ifodasi qudratli tahlil quroliga aylandi:
```dart
sealed class Natija {}
class Muvaffaqiyat extends Natija { final String data; Muvaffaqiyat(this.data); }
class Xato extends Natija { final String xabar; Xato(this.xabar); }

String xabarBer(Natija res) => switch (res) {
  Muvaffaqiyat(data: var d) => "Muvaffaqiyat: $d",
  Xato(xabar: var x) => "Xatolik: $x",
};
```

---

<a name="10-bob"></a>
# 10-Bob: Flutter bilan Aloqa va Reaktiv Arxitektura

Flutter freymvorkida hamma narsa Widget hisoblanadi:
* `StatelessWidget`: O'zgarmas statik ekranlar.
* `StatefulWidget`: Dinamik, foydalanuvchi bosganda o'zgaruvchi ekranlar.
* `State Management`: BLoC, Riverpod va Provider orqali ma'lumotlar oqimini tartibga solish.

---

<a name="11-bob"></a>
# 11-Bob: Maxsus Bob: Dart FFI orqali Mobil Qurilmada 1-Bit LLM Dvigateli

Telefonda yoki planshetda sun'iy intellekt modelini internetga ulanmasdan (On-Device) ishlatish uchun Dart **FFI (Foreign Function Interface)** orqali C++/Rust kutubxonalariga to'g'ridan-to'g'ri murojaat qiladi:

```dart
// Dart da 1-Bit AI Kvantlangan Matritsa Ko'paytmasi simulyatsiyasi
class OneBitLayerDart {
  final int inDim;
  final int outDim;
  late final List<int> weights; // -1 yoki +1

  OneBitLayerDart(this.inDim, this.outDim) {
    weights = List.generate(inDim * outDim, (i) => (i % 2 == 0) ? 1 : -1);
  }

  List<double> forward(List<double> input) {
    assert(input.length == inDim);
    var output = List<double>.filled(outDim, 0.0);

    for (int j = 0; j < outDim; j++) {
      double sum = 0.0;
      for (int i = 0; i < inDim; i++) {
        int w = weights[i * outDim + j];
        sum += (w == 1) ? input[i] : -input[i];
      }
      output[j] = sum;
    }
    return output;
  }
}

void main() {
  final layer = OneBitLayerDart(4, 4);
  final input = [0.5, -0.2, 0.8, 0.1];
  final output = layer.forward(input);

  print("Dart On-Device AI Chiqishi: $output");
}
```

---

## XULOSA

Dart — zamonaviy mobil va ko'p platformali dasturlashning eng nafis va xavfsiz tili. Ushbu qo'llanma orqali O'zbekiston yoshlari iOS va Android smartfonlari uchun xalqaro darajadagi zamonaviy, tezkor va AI bilan qurollangan mobil ilovalarni yaratish sirlarini to'liq egallaydilar!
