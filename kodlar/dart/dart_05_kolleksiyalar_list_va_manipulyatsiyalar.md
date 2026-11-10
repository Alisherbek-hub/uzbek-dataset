# 5-Qism: Kolleksiyalar: List va Chuqur Manipulyatsiyalar (201-250)

Ushbu qismda Dart tilidagi asosiy kolleksiya bo'lgan `List` (o'suvchi va qat'iy o'lchamli ro'yxatlar), `List.generate`, `List.unmodifiable`, Collection `if`, Collection `for`, spread operatorlar, saralash, qidiruv va ko'p o'lchamli massivlar amaliy dasturlarda o'rganiladi.

# 201-Topshiriq: Fixed-length vs Growable List (Qat'iy va O'suvchi ro'yxatlar)
## Topshiriq sharti:
`List.filled(n, val)` orqali o'lchami o'zgarmas ro'yxat va `growable: true` bilan dinamik o'suvchi ro'yxat yaratish farqini ko'rsating.

## Yechim (Dart kodi):
```dart
void main() {
  // Qat'iy o'lchamli (Fixed-length) ro'yxat: yangi element qo'shib bo'lmaydi
  List<int> fixedList = List.filled(3, 0);
  fixedList[0] = 10;
  fixedList[1] = 20;
  fixedList[2] = 30;
  print("Fixed list: $fixedList");

  // O'suvchi (Growable) ro'yxat
  List<int> growableList = [];
  growableList.add(100);
  growableList.add(200);
  print("Growable list: $growableList");
}
```

## Tushuntirish va Mantiq:
`List.filled(length, fill, growable: false)` qat'iy o'lchamli bo'lib, unga `add()` yoki `remove()` chaqirilsa `UnsupportedError` tashlanadi.

## Ishlash natijasi:
```text
Fixed list: [10, 20, 30]
Growable list: [100, 200]
```

# 202-Topshiriq: List.generate() orqali dinamik hisoblangan ro'yxat yaratish
## Topshiriq sharti:
0 dan 9 gacha bo'lgan sonlarning kvadratlaridan iborat ro'yxatni `List.generate` bilan bitta satrda yarating.

## Yechim (Dart kodi):
```dart
void main() {
  List<int> kvadratlar = List.generate(5, (index) => index * index);
  print("Kvadratlar ro'yxati: $kvadratlar");

  List<String> tokenlar = List.generate(3, (i) => "token_#${i + 1}");
  print("Tokenlar: $tokenlar");
}
```

## Tushuntirish va Mantiq:
`List.generate(count, generator)` indeksi bo'yicha har bir elementni hisoblab chiqadi va ro'yxatni tezkor to'ldirishning eng nafis usulidir.

## Ishlash natijasi:
```text
Kvadratlar ro'yxati: [0, 1, 4, 9, 16]
Tokenlar: [token_#1, token_#2, token_#3]
```

# 203-Topshiriq: List.unmodifiable(): O'zgarmas himoyalangan ro'yxat
## Topshiriq sharti:
Tashqi kod tomonidan elementlarini o'zgartirib bo'lmaydigan `List.unmodifiable` ro'yxatini hosil qiling.

## Yechim (Dart kodi):
```dart
void main() {
  List<String> kunlar = List.unmodifiable(["Dushanba", "Seshanba", "Chorshanba"]);

  print("Kunlar: $kunlar");
  try {
    kunlar[0] = "Yakshanba"; // Xatolik
  } catch (e) {
    print("O'zgartirish taqiqlandi: $e");
  }
}
```

## Tushuntirish va Mantiq:
`List.unmodifiable()` o'zgarmas (immutable) ro'yxat yaratadi va ma'lumotlarning tasodifiy o'zgarishlaridan to'liq himoya qiladi.

## Ishlash natijasi:
```text
Kunlar: [Dushanba, Seshanba, Chorshanba]
O'zgartirish taqiqlandi: UnsupportedError: Cannot modify an unmodifiable list
```

# 204-Topshiriq: List.from() va List.of() farqi
## Topshiriq sharti:
`List.from()` (dinamik tekshiruv) va `List.of()` (aniq turdagi xavfsiz nusxa) farqini ko'rsating.

## Yechim (Dart kodi):
```dart
void main() {
  Iterable<num> sonlar = [1, 2.5, 3];

  // List.of turga qat'iy mos bo'lishi kerak: List<num>.of
  List<num> nusxa1 = List.of(sonlar);

  // List.from esa kerakli turga cast qilib nusxalaydi
  List<double> nusxa2 = List<double>.from(sonlar.map((e) => e.toDouble()));

  print("nusxa1: $nusxa1");
  print("nusxa2: $nusxa2");
}
```

## Tushuntirish va Mantiq:
`List.of(iterable)` elementlar turini qat'iy saqlaydi; `List.from(iterable)` esa boshqa turga o'tkazish imkonini beradi.

## Ishlash natijasi:
```text
nusxa1: [1, 2.5, 3]
nusxa2: [1.0, 2.5, 3.0]
```

# 205-Topshiriq: Element qo'shish: add(), addAll(), insert(), insertAll()
## Topshiriq sharti:
Ro'yxatning oxiriga va o'rtasiga elementlar hamda kolleksiyalar qo'shish metodlarini ko'rsating.

## Yechim (Dart kodi):
```dart
void main() {
  List<String> mevalar = ["Olma"];

  mevalar.add("Banan"); // Oxiriga bitta
  mevalar.addAll(["Uzum", "Anor"]); // Oxiriga bir nechta
  mevalar.insert(1, "Shaftoli"); // 1-indeksga bitta
  mevalar.insertAll(0, ["Gilos", "O'rik"]); // Boshiga bir nechta

  print("Natijaviy ro'yxat: $mevalar");
}
```

## Tushuntirish va Mantiq:
`add` va `addAll` ro'yxat oxiriga O(1) ammortizatsiyalangan vaqtda qo'shadi, `insert` esa qolgan elementlarni o'ngga siljitadi O(N).

## Ishlash natijasi:
```text
Natijaviy ro'yxat: [Gilos, O'rik, Olma, Shaftoli, Banan, Uzum, Anor]
```

# 206-Topshiriq: Element o'chirish: remove(), removeAt(), removeLast(), removeWhere()
## Topshiriq sharti:
Qiymati bo'yicha, indeksi bo'yicha, oxiridan va shart bo'yicha elementlarni o'chiring.

## Yechim (Dart kodi):
```dart
void main() {
  List<int> sonlar = [10, 25, 30, 25, 40, 55];

  sonlar.remove(25); // Birinchi uchragan 25 o'chiriladi
  print("remove(25) so'ng: $sonlar");

  sonlar.removeAt(0); // 0-indeksdagi 10 o'chiriladi
  print("removeAt(0) so'ng: $sonlar");

  sonlar.removeLast(); // Oxirgi 55 o'chiriladi
  print("removeLast() so'ng: $sonlar");

  sonlar.removeWhere((x) => x > 25); // 25 dan kattalari o'chiriladi
  print("removeWhere so'ng: $sonlar");
}
```

## Tushuntirish va Mantiq:
`removeWhere` shartga mos keluvchi barcha elementlarni bir yo'la tozalash uchun juda samarali hisoblanadi.

## Ishlash natijasi:
```text
remove(25) so'ng: [10, 30, 25, 40, 55]
removeAt(0) so'ng: [30, 25, 40, 55]
removeLast() so'ng: [30, 25, 40]
removeWhere so'ng: [25]
```

# 207-Topshiriq: Ro'yxat xususiyatlari: first, last, single
## Topshiriq sharti:
Ro'yxatning birinchi, oxirgi va yagona elementlarini xavfsiz o'qishni ko'rsating.

## Yechim (Dart kodi):
```dart
void main() {
  List<String> tillar = ["Dart", "Python", "C++"];

  print("Birinchi element: ${tillar.first}");
  print("Oxirgi element:   ${tillar.last}");

  List<String> yagona = ["Yagona Element"];
  print("Single: ${yagona.single}");
}
```

## Tushuntirish va Mantiq:
`single` xususiyati ro'yxatda aniq 1 ta element bo'lishini talab qiladi, agar bo'sh yoki 2+ element bo'lsa xato beradi.

## Ishlash natijasi:
```text
Birinchi element: Dart
Oxirgi element:   C++
Single: Yagona Element
```

# 208-Topshiriq: Dart 3 xavfsiz firstOrNull va lastOrNull
## Topshiriq sharti:
Bo'sh ro'yxatlarda `first` xato bermasligi uchun Dart 3 ning `firstOrNull` va `lastOrNull` xususiyatlaridan foydalaning.

## Yechim (Dart kodi):
```dart
void main() {
  List<int> bosh = [];
  List<int> tola = [100, 200];

  print("Bo'sh ro'yxat firstOrNull: ${bosh.firstOrNull}");
  print("Bo'sh ro'yxat lastOrNull:  ${bosh.lastOrNull}");

  print("To'la ro'yxat firstOrNull: ${tola.firstOrNull}");
  print("To'la ro'yxat lastOrNull:  ${tola.lastOrNull}");
}
```

## Tushuntirish va Mantiq:
`firstOrNull` bo'sh ro'yxatlarda qulashning (StateError) oldini oladi va null-safety bilan mukammal integratsiyalashgan.

## Ishlash natijasi:
```text
Bo'sh ro'yxat firstOrNull: null
Bo'sh ro'yxat lastOrNull:  null
To'la ro'yxat firstOrNull: 100
To'la ro'yxat lastOrNull:  200
```

# 209-Topshiriq: Indeks operatsiyalari: indexOf(), lastIndexOf(), indexWhere()
## Topshiriq sharti:
Ro'yxatdan element yoki shartga mos keluvchi birinchi va oxirgi indeksni toping.

## Yechim (Dart kodi):
```dart
void main() {
  List<String> ranglar = ["qizil", "yashil", "ko'k", "yashil", "sariq"];

  print("'yashil' birinchi indeksi: ${ranglar.indexOf('yashil')}");
  print("'yashil' oxirgi indeksi:   ${ranglar.lastIndexOf('yashil')}");
  print("4 harfdan uzun rang indeksi: ${ranglar.indexWhere((r) => r.length > 5)}");
}
```

## Tushuntirish va Mantiq:
Topilmagan taqdirda ushbu metodlar har doim `-1` qaytaradi.

## Ishlash natijasi:
```text
'yashil' birinchi indeksi: 1
'yashil' oxirgi indeksi:   3
4 harfdan uzun rang indeksi: 1
```

# 210-Topshiriq: sublist(start, end): Ro'yxatni kesib olish
## Topshiriq sharti:
`sublist(start, [end])` orqali yangi qism ro'yxat nusxasini ajratib oling.

## Yechim (Dart kodi):
```dart
void main() {
  List<int> sonlar = [0, 1, 2, 3, 4, 5, 6, 7];

  List<int> qism1 = sonlar.sublist(2, 5); // 2, 3, 4
  List<int> qism2 = sonlar.sublist(5);    // 5 dan oxirigacha

  print("qism1 (2..5): $qism1");
  print("qism2 (5..oxiri): $qism2");
}
```

## Tushuntirish va Mantiq:
`sublist` yangi ro'yxat qaytaradi, asl ro'yxat elementlari esa o'zgarmasdan saqlanadi.

## Ishlash natijasi:
```text
qism1 (2..5): [2, 3, 4]
qism2 (5..oxiri): [5, 6, 7]
```

# 211-Topshiriq: getRange() va setRange() bilan oraliqni nusxalash
## Topshiriq sharti:
Bitta ro'yxatning oraliq qismini ikkinchi ro'yxatga `setRange` orqali xotira nusxasini ko'chiring.

## Yechim (Dart kodi):
```dart
void main() {
  List<int> manba = [10, 20, 30, 40, 50];
  List<int> nishon = [0, 0, 0, 0, 0];

  nishon.setRange(1, 4, manba, 0); // manbaning 0-dan boshlab nishonning 1..4 ga yozadi
  print("Natijaviy nishon: $nishon");
}
```

## Tushuntirish va Mantiq:
`setRange` mavjud massiv kataklarini to'g'ridan-to'g'ri yangilaydi va xotira ajratish xarajatlarini tejaydi.

## Ishlash natijasi:
```text
Natijaviy nishon: [0, 10, 20, 30, 0]
```

# 212-Topshiriq: Spread operatori: ... va ...?
## Topshiriq sharti:
Ro'yxat ichida boshqa ro'yxatlarni birlashtirishda `...` operatorining qulayligini ko'rsating.

## Yechim (Dart kodi):
```dart
void main() {
  List<int> a = [1, 2];
  List<int> b = [3, 4];
  List<int>? c = null;

  List<int> jam = [0, ...a, ...b, ...?c, 5];
  print("Birlashgan ro'yxat: $jam");
}
```

## Tushuntirish va Mantiq:
Spread operatori ro'yxat literallarini birlashtirishning eng o'qilishi oson va rasmiy uslubidir.

## Ishlash natijasi:
```text
Birlashgan ro'yxat: [0, 1, 2, 3, 4, 5]
```

# 213-Topshiriq: Collection if: Ro'yxat ichida shartli element qo'shish
## Topshiriq sharti:
Ro'yxat e'lon qilinayotgan paytning o'zida shartga qarab element qo'shuvchi Collection `if` dan foydalaning.

## Yechim (Dart kodi):
```dart
void main() {
  bool isAdmin = true;
  bool isPremium = false;

  List<String> menyu = [
    "Bosh sahifa",
    "Profil",
    if (isAdmin) "Admin Panel",
    if (isPremium) "VIP Xizmatlar",
    "Chiqish"
  ];

  print("Foydalanuvchi menyusi: $menyu");
}
```

## Tushuntirish va Mantiq:
Collection `if` Flutter da `Widget` lar ro'yxatini shartli chizishda eng ko'p ishlatiladigan imkoniyatdir.

## Ishlash natijasi:
```text
Foydalanuvchi menyusi: [Bosh sahifa, Profil, Admin Panel, Chiqish]
```

# 214-Topshiriq: Collection for: Ro'yxat ichida siklli elementlar generatsiyasi
## Topshiriq sharti:
Kolleksiya ichida `for` siklini to'g'ridan-to'g'ri qo'llab yangi elementlar to'plamini hosil qiling.

## Yechim (Dart kodi):
```dart
void main() {
  List<int> kirish = [1, 2, 3];

  List<String> chiqish = [
    "#0",
    for (int x in kirish) "#$x",
    "#oxiri"
  ];

  print("Natija: $chiqish");
}
```

## Tushuntirish va Mantiq:
Collection `for` orqali oraliq ro'yxat yaratmasdan yangi elementlarni to'g'ridan-to'g'ri joylashtirish mumkin.

## Ishlash natijasi:
```text
Natija: [#0, #1, #2, #3, #oxiri]
```

# 215-Topshiriq: Collection if-else: Shartli muqobil element
## Topshiriq sharti:
Collection `if-else` orqali holatga qarab u yoki bu elementni ro'yxatga qo'shing.

## Yechim (Dart kodi):
```dart
void main() {
  bool tizimda = false;

  List<String> navBar = [
    "Asosiy",
    if (tizimda) "Profilim" else "Kirish / Ro'yxatdan o'tish"
  ];

  print("Navigatsiya: $navBar");
}
```

## Tushuntirish va Mantiq:
Collection `if-else` ternary operatoriga qaraganda ro'yxat literali ichida ancha tabiiy o'qiladi.

## Ishlash natijasi:
```text
Navigatsiya: [Asosiy, Kirish / Ro'yxatdan o'tish]
```

# 216-Topshiriq: Ro'yxatni saralash: sort()
## Topshiriq sharti:
Sonlar va satrlar ro'yxatini standart `sort()` metodi bilan o'sish tartibida saralang.

## Yechim (Dart kodi):
```dart
void main() {
  List<int> sonlar = [42, 12, 88, 5, 23];
  sonlar.sort();
  print("Saralangan sonlar: $sonlar");

  List<String> ismlar = ["Zuhra", "Ali", "Bobur", "Malika"];
  ismlar.sort();
  print("Alifbo bo'yicha: $ismlar");
}
```

## Tushuntirish va Mantiq:
Standart `sort()` Dual-Pivot Quicksort algoritmi asosida ishlaydi va o'rtacha O(N log N) vaqt oladi.

## Ishlash natijasi:
```text
Saralangan sonlar: [5, 12, 23, 42, 88]
Alifbo bo'yicha: [Ali, Bobur, Malika, Zuhra]
```

# 217-Topshiriq: Maxsus solishtirish qoidasi (Custom Comparator) bilan saralash
## Topshiriq sharti:
Sonlarni kamayish tartibida va satrlarni uzunligi bo'yicha saralovchi comparator yozing.

## Yechim (Dart kodi):
```dart
void main() {
  List<int> sonlar = [5, 20, 10, 40];
  sonlar.sort((a, b) => b.compareTo(a)); // Kamayish tartibida
  print("Kamayish tartibida: $sonlar");

  List<String> sozlar = ["Gilos", "Nok", "Shaftoli", "Olma"];
  sozlar.sort((a, b) => a.length.compareTo(b.length)); // Uzunligi bo'yicha
  print("Uzunligi bo'yicha: $sozlar");
}
```

## Tushuntirish va Mantiq:
`compareTo(b)`: agar `a < b` bo'lsa manfiy, teng bo'lsa 0, katta bo'lsa musbat son qaytaradi.

## Ishlash natijasi:
```text
Kamayish tartibida: [40, 20, 10, 5]
Uzunligi bo'yicha: [Nok, Olma, Gilos, Shaftoli]
```

# 218-Topshiriq: Ob'ektlar ro'yxatini maydon bo'yicha saralash
## Topshiriq sharti:
`Talaba` sinfi ob'ektlarini balli bo'yicha kamayish tartibida saralang.

## Yechim (Dart kodi):
```dart
class Talaba {
  final String ism;
  final int ball;
  Talaba(this.ism, this.ball);

  @override
  String toString() => "$ism ($ball ball)";
}

void main() {
  List<Talaba> talabalar = [
    Talaba("Rustam", 78),
    Talaba("Zilola", 95),
    Talaba("Akmal", 85)
  ];

  talabalar.sort((a, b) => b.ball.compareTo(a.ball)); // Eng yuqori ball oldinda

  print("Reyting:");
  talabalar.forEach((t) => print("- $t"));
}
```

## Tushuntirish va Mantiq:
Ob'ektlar ro'yxatini muayyan xususiyatlari bo'yicha tartiblash amaliy dasturlarning kundalik vazifasidir.

## Ishlash natijasi:
```text
Reyting:
- Zilola (95 ball)
- Akmal (85 ball)
- Rustam (78 ball)
```

# 219-Topshiriq: shuffle(): Ro'yxatni tasodifiy aralashtirish
## Topshiriq sharti:
Karta o'yini yoki tasodifiy test savollari uchun ro'yxat elementlari o'rnini `shuffle()` bilan almashtiring.

## Yechim (Dart kodi):
```dart
import 'dart:math';

void main() {
  List<int> sonlar = [1, 2, 3, 4, 5];
  sonlar.shuffle(Random(42)); // Deterministik seed

  print("Aralashgan ro'yxat: $sonlar");
}
```

## Tushuntirish va Mantiq:
`shuffle([Random])` Fisher-Yates algoritmi orqali O(N) vaqtda elementlarni xolisona tasodifiy tartibda aralashtiradi.

## Ishlash natijasi:
```text
Aralashgan ro'yxat: [2, 5, 4, 3, 1]
```

# 220-Topshiriq: reversed xususiyati va toList()
## Topshiriq sharti:
Asl ro'yxatni o'zgartirmasdan, uning teskari nusxasini oling.

## Yechim (Dart kodi):
```dart
void main() {
  List<String> harflar = ["A", "B", "C", "D"];
  List<String> teskari = harflar.reversed.toList();

  print("Asl ro'yxat:    $harflar");
  print("Teskari nusxa:  $teskari");
}
```

## Tushuntirish va Mantiq:
`.reversed` `Iterable` qaytaradi. Uni to'liq yangi ro'yxatga aylantirish uchun `.toList()` chaqiriladi.

## Ishlash natijasi:
```text
Asl ro'yxat:    [A, B, C, D]
Teskari nusxa:  [D, C, B, A]
```

# 221-Topshiriq: contains() bilan element mavjudligini tekshirish
## Topshiriq sharti:
Ro'yxat ichida qidirilayotgan qiymat borligini `contains()` orqali O(N) da tekshiring.

## Yechim (Dart kodi):
```dart
void main() {
  List<String> ruxsatlar = ["READ", "WRITE", "EXECUTE"];

  print("WRITE bormi: ${ruxsatlar.contains('WRITE')}");
  print("DELETE bormi: ${ruxsatlar.contains('DELETE')}");
}
```

## Tushuntirish va Mantiq:
`contains(element)` elementning `==` operatori orqali mavjudligini tekshiradi.

## Ishlash natijasi:
```text
WRITE bormi: true
DELETE bormi: false
```

# 222-Topshiriq: any() va every() mantiqiy tekshiruvlari
## Topshiriq sharti:
Ro'yxatdagi kamida bitta element manfiymi (`any`) va barcha elementlar juftmi (`every`) ekanligini tekshiring.

## Yechim (Dart kodi):
```dart
void main() {
  List<int> sonlar = [2, 4, 6, -8, 10];

  bool kamidaBittaManfiy = sonlar.any((x) => x < 0);
  bool barchasiJuft = sonlar.every((x) => x % 2 == 0);
  bool barchasiMusbat = sonlar.every((x) => x > 0);

  print("Kamida bitta manfiy bormi: $kamidaBittaManfiy");
  print("Barcha sonlar juftmi:      $barchasiJuft");
  print("Barcha sonlar musbatmi:    $barchasiMusbat");
}
```

## Tushuntirish va Mantiq:
`any` kamida bitta true topsa darhol true qaytaradi; `every` esa bitta false topsa darhol false qaytaradi.

## Ishlash natijasi:
```text
Kamida bitta manfiy bormi: true
Barcha sonlar juftmi:      true
Barcha sonlar musbatmi:    false
```

# 223-Topshiriq: take() va takeWhile()
## Topshiriq sharti:
Ro'yxatdan shart bajarilib turguncha elementlarni oluvchi `takeWhile` metodini ko'rsating.

## Yechim (Dart kodi):
```dart
void main() {
  List<int> sonlar = [2, 4, 6, 7, 8, 10];

  var dastlabki3 = sonlar.take(3).toList();
  var toqGacha = sonlar.takeWhile((x) => x % 2 == 0).toList();

  print("take(3): $dastlabki3");
  print("takeWhile(juft): $toqGacha"); // 7 ga yetganda to'xtaydi
}
```

## Tushuntirish va Mantiq:
`takeWhile` birinchi marta shart bajarilmagan joyda to'xtaydi va keyingi elementlarni qaramaydi.

## Ishlash natijasi:
```text
take(3): [2, 4, 6]
takeWhile(juft): [2, 4, 6]
```

# 224-Topshiriq: skip() va skipWhile()
## Topshiriq sharti:
Shart bajarilib turguncha elementlarni tashlab o'tuvchi `skipWhile` metodini ko'rsating.

## Yechim (Dart kodi):
```dart
void main() {
  List<int> sonlar = [1, 3, 5, 8, 10, 11];

  var boshidan2Tashla = sonlar.skip(2).toList();
  var toqlarniTashla = sonlar.skipWhile((x) => x % 2 != 0).toList();

  print("skip(2): $boshidan2Tashla");
  print("skipWhile(toq): $toqlarniTashla"); // 8 dan boshlab qolganini oladi
}
```

## Tushuntirish va Mantiq:
`skipWhile` birinchi juft son 8 ga duch kelishi bilan to'xtashni bas qiladi va qolgan barcha elementlarni saqlab qoladi.

## Ishlash natijasi:
```text
skip(2): [5, 8, 10, 11]
skipWhile(toq): [8, 10, 11]
```

# 225-Topshiriq: join(separator): Ro'yxatni bitta matnga birlashtirish
## Topshiriq sharti:
Ro'yxatdagi so'zlarni yoki sonlarni vergul yoki chiziqcha orqali bitta `String` satriga aylantiring.

## Yechim (Dart kodi):
```dart
void main() {
  List<String> qismlar = ["Toshkent", "Samarqand", "Buxoro"];
  String birlashgan = qismlar.join(" -> ");

  List<int> sonlar = [1, 2, 3, 4, 5];
  String kod = sonlar.join("-");

  print("Marshrut: $birlashgan");
  print("Kod:      $kod");
}
```

## Tushuntirish va Mantiq:
`join(separator)` satr buferidan foydalanib barcha elementlarning `toString()` natijasini bitta matnga yig'adi.

## Ishlash natijasi:
```text
Marshrut: Toshkent -> Samarqand -> Buxoro
Kod:      1-2-3-4-5
```

# 226-Topshiriq: map(): Ro'yxatni boshqa turga o'zgartirish
## Topshiriq sharti:
Sonlar ro'yxatining har bir elementini 10 barobarga oshirib, natijani yangi ro'yxatga aylantiring.

## Yechim (Dart kodi):
```dart
void main() {
  List<int> sonlar = [1, 2, 3, 4, 5];
  List<int> kattalashgan = sonlar.map((x) => x * 10).toList();

  print("Asl sonlar:        $sonlar");
  print("10 ga ko'paytirilgan: $kattalashgan");
}
```

## Tushuntirish va Mantiq:
`.map(fn)` har bir elementga funksiyani qo'llaydi va natijaviy `Iterable` qaytaradi.

## Ishlash natijasi:
```text
Asl sonlar:        [1, 2, 3, 4, 5]
10 ga ko'paytirilgan: [10, 20, 30, 40, 50]
```

# 227-Topshiriq: where(): Shart bo'yicha filtrlash
## Topshiriq sharti:
Ro'yxatdan faqat musbat va 5 dan katta bo'lgan sonlarni `.where()` orqali ajratib oling.

## Yechim (Dart kodi):
```dart
void main() {
  List<int> sonlar = [-10, 3, 7, -2, 15, 0, 8];
  List<int> filtrlangan = sonlar.where((x) => x > 5).toList();

  print("5 dan katta musbat sonlar: $filtrlangan");
}
```

## Tushuntirish va Mantiq:
`.where(predicate)` berilgan shartga to'g'ri keladigan elementlarni filtrlaydi.

## Ishlash natijasi:
```text
5 dan katta musbat sonlar: [7, 15, 8]
```

# 228-Topshiriq: expand(): Ichma-ich ro'yxatlarni tekislash (Flatten)
## Topshiriq sharti:
Ichma-ich joylashgan 2D ro'yxatni bitta tekis 1D ro'yxatga aylantirish uchun `.expand()` dan foydalaning.

## Yechim (Dart kodi):
```dart
void main() {
  List<List<int>> matritsa = [
    [1, 2, 3],
    [4, 5],
    [6, 7, 8, 9]
  ];

  List<int> tekis = matritsa.expand((qator) => qator).toList();
  print("Tekislangan ro'yxat: $tekis");
}
```

## Tushuntirish va Mantiq:
`.expand()` har bir elementdan yangi to'plam hosil qilib, ularni bitta oqimga ulaydi (boshqa tillardagi `flatMap`).

## Ishlash natijasi:
```text
Tekislangan ro'yxat: [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

# 229-Topshiriq: fold(): Boshlang'ich qiymatdan akkumulyatsiya qilish
## Topshiriq sharti:
Mahsulotlar narxlari ro'yxatidan dastlabki 10 000 so'm yetkazib berish xarajati bilan birga jami summani `.fold()` orqali hisoblang.

## Yechim (Dart kodi):
```dart
void main() {
  List<double> narxlar = [45000.0, 32000.0, 18000.0];
  double yetkazibBerish = 10000.0;

  double jami = narxlar.fold(yetkazibBerish, (sum, narx) => sum + narx);
  print("Jami to'lov (yetkazib berish bilan): $jami so'm");
}
```

## Tushuntirish va Mantiq:
`.fold(initialValue, combine)` boshlang'ich qiymatdan boshlab elementlarni yig'adi va bo'sh ro'yxatlarda ham xavfsiz ishlaydi.

## Ishlash natijasi:
```text
Jami to'lov (yetkazib berish bilan): 105000.0 so'm
```

# 230-Topshiriq: 2D Massiv (Matrix) yaratish va boshqarish
## Topshiriq sharti:
3 x 3 o'lchamli nollar bilan to'ldirilgan matritsa yarating va uning qiymatlarini o'zgartiring.

## Yechim (Dart kodi):
```dart
void main() {
  int rows = 3, cols = 3;
  // To'g'ri 2D matritsa yaratish: har bir qator yangi mustaqil ro'yxat bo'lishi shart!
  List<List<int>> matrix = List.generate(rows, (_) => List.filled(cols, 0));

  matrix[0][0] = 1;
  matrix[1][1] = 5;
  matrix[2][2] = 9;

  print("Matritsa ko'rinishi:");
  for (var row in matrix) {
    print(row);
  }
}
```

## Tushuntirish va Mantiq:
`List.generate` har bir qator uchun alohida yangi ro'yxat xotirasi ajratilishini kafolatlaydi.

## Ishlash natijasi:
```text
Matritsa ko'rinishi:
[1, 0, 0]
[0, 5, 0]
[0, 0, 9]
```

# 231-Topshiriq: 2D Matritsaning qatorlari va ustunlari yig'indisini hisoblash
## Topshiriq sharti:
2D massivning har bir qatori va har bir ustuni yig'indisini hisoblab chiqaring.

## Yechim (Dart kodi):
```dart
void main() {
  List<List<int>> m = [
    [1, 2, 3],
    [4, 5, 6]
  ];

  // Qatorlar yig'indisi
  for (int i = 0; i < m.length; ++i) {
    int rowSum = m[i].reduce((a, b) => a + b);
    print("$i-qator yig'indisi: $rowSum");
  }

  // Ustunlar yig'indisi
  for (int j = 0; j < m[0].length; ++j) {
    int colSum = 0;
    for (int i = 0; i < m.length; ++i) {
      colSum += m[i][j];
    }
    print("$j-ustun yig'indisi: $colSum");
  }
}
```

## Tushuntirish va Mantiq:
Qatorlar bo'yicha yig'ish xotirada ketma-ket joylashgani sababli juda tez bajariladi.

## Ishlash natijasi:
```text
0-qator yig'indisi: 6
1-qator yig'indisi: 15
0-ustun yig'indisi: 5
1-ustun yig'indisi: 7
2-ustun yig'indisi: 9
```

# 232-Topshiriq: Matritsani transpozitsiya qilish (Transpose Matrix)
## Topshiriq sharti:
M x N matritsani N x M o'lchamli transpozitsiyalangan yangi matritsaga aylantiring.

## Yechim (Dart kodi):
```dart
List<List<int>> transpose(List<List<int>> m) {
  int r = m.length;
  int c = m[0].length;

  return List.generate(c, (j) => List.generate(r, (i) => m[i][j]));
}

void main() {
  List<List<int>> orig = [
    [1, 2, 3],
    [4, 5, 6]
  ];

  var tr = transpose(orig);
  print("Asl o'lcham: 2x3, Transpozitsiya: 3x2:");
  for (var row in tr) print(row);
}
```

## Tushuntirish va Mantiq:
Transpozitsiya qator va ustun indekslari o'rnini almashtiradi: `tr[j][i] = m[i][j]`.

## Ishlash natijasi:
```text
Asl o'lcham: 2x3, Transpozitsiya: 3x2:
[1, 4]
[2, 5]
[3, 6]
```

# 233-Topshiriq: Ro'yxatni N bo'lakka (Chunks) bo'lish
## Topshiriq sharti:
Katta ro'yxatni har biri K tadan elementga ega kichik ro'yxatlarga bo'luvchi funksiya yozing.

## Yechim (Dart kodi):
```dart
List<List<T>> chunkList<T>(List<T> list, int chunkSize) {
  List<List<T>> chunks = [];
  for (int i = 0; i < list.length; i += chunkSize) {
    int end = (i + chunkSize < list.length) ? i + chunkSize : list.length;
    chunks.add(list.sublist(i, end));
  }
  return chunks;
}

void main() {
  List<int> sonlar = [1, 2, 3, 4, 5, 6, 7, 8];
  var bolaklar = chunkList(sonlar, 3);

  print("Bo'laklar: $bolaklar");
}
```

## Tushuntirish va Mantiq:
Chunking ma'lumotlarni sahifalashda (pagination) va guruhlab API ga jo'natishda (batching) keng qo'llaniladi.

## Ishlash natijasi:
```text
Bo'laklar: [[1, 2, 3], [4, 5, 6], [7, 8]]
```

# 234-Topshiriq: Siljuvchi oyna (Sliding Window) texnikasi ro'yxat ustida
## Topshiriq sharti:
K uzunlikdagi oynaning ketma-ket harakatlanishidagi maksimal yig'indisini hisoblang.

## Yechim (Dart kodi):
```dart
int maxSubarraySum(List<int> arr, int k) {
  if (arr.length < k) return 0;
  int windowSum = 0;
  for (int i = 0; i < k; ++i) windowSum += arr[i];

  int maxSum = windowSum;
  for (int i = k; i < arr.length; ++i) {
    windowSum += arr[i] - arr[i - k]; // Yangi kiradi, eski chiqadi
    if (windowSum > maxSum) maxSum = windowSum;
  }
  return maxSum;
}

void main() {
  List<int> nums = [2, 1, 5, 1, 3, 2];
  print("K=3 bo'yicha maksimal oyna yig'indisi: ${maxSubarraySum(nums, 3)}");
}
```

## Tushuntirish va Mantiq:
Siljuvchi oyna har qadamda yig'indini qayta hisoblamasdan O(N) chiziqli vaqtda natija beradi.

## Ishlash natijasi:
```text
K=3 bo'yicha maksimal oyna yig'indisi: 9
```

# 235-Topshiriq: Ikki ro'yxatning kesishmasi (Intersection)
## Topshiriq sharti:
Ikkala ro'yxatda ham mavjud bo'lgan umumiy elementlarni toping.

## Yechim (Dart kodi):
```dart
List<int> intersection(List<int> a, List<int> b) {
  var setB = b.toSet();
  return a.where((x) => setB.contains(x)).toSet().toList();
}

void main() {
  List<int> l1 = [1, 2, 3, 4, 5];
  List<int> l2 = [3, 4, 5, 6, 7];

  print("Kesishma: ${intersection(l1, l2)}");
}
```

## Tushuntirish va Mantiq:
`Set.contains` O(1) da ishlagani sababli kesishma O(N + M) vaqtda hisoblanadi.

## Ishlash natijasi:
```text
Kesishma: [3, 4, 5]
```

# 236-Topshiriq: Ikki ro'yxatning birlashmasi (Union)
## Topshiriq sharti:
Ikki ro'yxatning barcha noyob elementlarini birlashtiruvchi kod yozing.

## Yechim (Dart kodi):
```dart
List<int> unionList(List<int> a, List<int> b) {
  return {...a, ...b}.toList();
}

void main() {
  List<int> l1 = [1, 2, 3];
  List<int> l2 = [3, 4, 5];

  print("Birlashma: ${unionList(l1, l2)}");
}
```

## Tushuntirish va Mantiq:
Dart da Set literali ichida spread operatori `{...a, ...b}` dublikatlarni avtomatik tozalab birlashtiradi.

## Ishlash natijasi:
```text
Birlashma: [1, 2, 3, 4, 5]
```

# 237-Topshiriq: Ikki ro'yxatning simmetrik ayirmasi
## Topshiriq sharti:
Faqat bitta ro'yxatda mavjud bo'lgan, lekin ikkalasida bir vaqtda bo'lmagan elementlarni toping.

## Yechim (Dart kodi):
```dart
List<int> symmetricDifference(List<int> a, List<int> b) {
  var sA = a.toSet();
  var sB = b.toSet();
  var diff1 = sA.difference(sB);
  var diff2 = sB.difference(sA);
  return diff1.union(diff2).toList();
}

void main() {
  List<int> l1 = [1, 2, 3, 4];
  List<int> l2 = [3, 4, 5, 6];

  print("Simmetrik ayirma: ${symmetricDifference(l1, l2)}");
}
```

## Tushuntirish va Mantiq:
Simmetrik ayirma `(A - B) union (B - A)` formulasi orqali topiladi.

## Ishlash natijasi:
```text
Simmetrik ayirma: [1, 2, 5, 6]
```

# 238-Topshiriq: Stack (Stek) ma'lumotlar tuzilmasini List asosida qurish
## Topshiriq sharti:
LIFO (Last-In-First-Out) tamoyili bilan ishlovchi `Stack<T>` klassini `List` yordamida yozing.

## Yechim (Dart kodi):
```dart
class Stack<T> {
  final List<T> _storage = [];

  void push(T val) => _storage.add(val);

  T? pop() {
    if (_storage.isEmpty) return null;
    return _storage.removeLast();
  }

  T? peek() {
    if (_storage.isEmpty) return null;
    return _storage.last;
  }

  bool get isEmpty => _storage.isEmpty;
  int get length => _storage.length;
}

void main() {
  var s = Stack<int>();
  s.push(10);
  s.push(20);
  s.push(30);

  print("Tepa element (peek): ${s.peek()}");
  print("Chiqarildi (pop):    ${s.pop()}");
  print("Yangi tepa:         ${s.peek()}");
}
```

## Tushuntirish va Mantiq:
Dart ning `add` va `removeLast` metodlari ro'yxat oxirida O(1) vaqtda ishlaydi, bu stek uchun eng optimal asosdir.

## Ishlash natijasi:
```text
Tepa element (peek): 30
Chiqarildi (pop):    30
Yangi tepa:         20
```

# 239-Topshiriq: Queue (Navbat) ma'lumotlar tuzilmasini qurish
## Topshiriq sharti:
FIFO (First-In-First-Out) qoidasi asosida ishlovchi navbat klassini yarating.

## Yechim (Dart kodi):
```dart
class SimpleQueue<T> {
  final List<T> _items = [];

  void enqueue(T item) => _items.add(item);

  T? dequeue() {
    if (_items.isEmpty) return null;
    return _items.removeAt(0); // Boshidan olish
  }

  bool get isEmpty => _items.isEmpty;
}

void main() {
  var q = SimpleQueue<String>();
  q.enqueue("Mijoz 1");
  q.enqueue("Mijoz 2");
  q.enqueue("Mijoz 3");

  print("Xizmat ko'rsatildi: ${q.dequeue()}");
  print("Xizmat ko'rsatildi: ${q.dequeue()}");
}
```

## Tushuntirish va Mantiq:
Navbat birinchi kirgan element birinchi xizmat olishini kafolatlaydi.

## Ishlash natijasi:
```text
Xizmat ko'rsatildi: Mijoz 1
Xizmat ko'rsatildi: Mijoz 2
```

# 240-Topshiriq: Doiraviy bufer (Circular Buffer) List asosida
## Topshiriq sharti:
Qat'iy o'lchamli va yangi ma'lumotlar eng eskisining ustiga yoziladigan doiraviy bufer klassini yozing.

## Yechim (Dart kodi):
```dart
class CircularBuffer<T> {
  final int capacity;
  final List<T?> _buffer;
  int _writeIndex = 0;
  int _count = 0;

  CircularBuffer(this.capacity) : _buffer = List.filled(capacity, null);

  void add(T item) {
    _buffer[_writeIndex] = item;
    _writeIndex = (_writeIndex + 1) % capacity;
    if (_count < capacity) _count++;
  }

  List<T> toList() {
    List<T> res = [];
    int start = (_count < capacity) ? 0 : _writeIndex;
    for (int i = 0; i < _count; ++i) {
      res.add(_buffer[(start + i) % capacity] as T);
    }
    return res;
  }
}

void main() {
  var cb = CircularBuffer<int>(3);
  cb.add(1);
  cb.add(2);
  cb.add(3);
  print("To'la bufer: ${cb.toList()}");

  cb.add(4); // 1 ning ustiga yoziladi
  print("Yangi elementdan so'ng: ${cb.toList()}");
}
```

## Tushuntirish va Mantiq:
Doiraviy bufer loggerlar, sensor ma'lumotlari va so'nggi xabarlar tarixini saqlashda juda tejamkor ishlaydi.

## Ishlash natijasi:
```text
To'la bufer: [1, 2, 3]
Yangi elementdan so'ng: [2, 3, 4]
```

# 241-Topshiriq: Ro'yxat elementlarini N ta o'ringa o'ngga siljitish (Rotate List)
## Topshiriq sharti:
Massivni K qadam o'ngga siklik siljituvchi (masalan [1,2,3,4,5] va k=2 -> [4,5,1,2,3]) funksiya yozing.

## Yechim (Dart kodi):
```dart
List<T> rotateRight<T>(List<T> list, int k) {
  if (list.isEmpty) return list;
  k = k % list.length;
  if (k == 0) return list;

  return [...list.sublist(list.length - k), ...list.sublist(0, list.length - k)];
}

void main() {
  List<int> sonlar = [1, 2, 3, 4, 5];
  print("Asl ro'yxat: $sonlar");
  print("2 o'rin o'ngga: ${rotateRight(sonlar, 2)}");
}
```

## Tushuntirish va Mantiq:
`k % length` ortiqcha to'liq aylanishlarni bekor qiladi va qism ro'yxatlarni birlashtirib bir amalda siljitadi.

## Ishlash natijasi:
```text
Asl ro'yxat: [1, 2, 3, 4, 5]
2 o'rin o'ngga: [4, 5, 1, 2, 3]
```

# 242-Topshiriq: Ro'yxatdagi eng ko'p takrorlangan elementni (Moda) topish
## Topshiriq sharti:
Ro'yxat ichidan chastotasi eng yuqori bo'lgan elementni hisoblang.

## Yechim (Dart kodi):
```dart
T? findMode<T>(List<T> list) {
  if (list.isEmpty) return null;
  Map<T, int> counts = {};
  for (T item in list) {
    counts[item] = (counts[item] ?? 0) + 1;
  }

  T mode = list[0];
  int maxCount = 0;
  for (var entry in counts.entries) {
    if (entry.value > maxCount) {
      maxCount = entry.value;
      mode = entry.key;
    }
  }
  return mode;
}

void main() {
  List<String> javoblar = ["A", "B", "A", "C", "A", "B"];
  print("Eng ko'p tanlangan variant: ${findMode(javoblar)}");
}
```

## Tushuntirish va Mantiq:
Chastota xaritasi orqali statistik tahlil O(N) vaqtda oson topiladi.

## Ishlash natijasi:
```text
Eng ko'p tanlangan variant: A
```

# 243-Topshiriq: Ro'yxat medianasini hisoblash
## Topshiriq sharti:
Saralangan tartibda o'rtadagi qiymatni (juft bo'lsa o'rtadagi ikkitasining o'rtacha qiymatini) toping.

## Yechim (Dart kodi):
```dart
double findMedian(List<num> list) {
  List<num> copy = List.from(list)..sort();
  int n = copy.length;
  if (n % 2 != 0) {
    return copy[n ~/ 2].toDouble();
  } else {
    return (copy[(n ~/ 2) - 1] + copy[n ~/ 2]) / 2.0;
  }
}

void main() {
  print("Mediana [1, 3, 5]: ${findMedian([1, 5, 3])}");
  print("Mediana [1, 2, 3, 4]: ${findMedian([4, 1, 3, 2])}");
}
```

## Tushuntirish va Mantiq:
Mediana anomal keskin qiymatlarga (outliers) chidamli statistik ko'rsatkichdir.

## Ishlash natijasi:
```text
Mediana [1, 3, 5]: 3.0
Mediana [1, 2, 3, 4]: 2.5
```

# 244-Topshiriq: Prefiks yig'indilari (Prefix Sums) massivini hosil qilish
## Topshiriq sharti:
Oraliq summalarni O(1) da hisoblash uchun prefiks massivini quring.

## Yechim (Dart kodi):
```dart
class PrefixSum {
  late final List<int> _prefix;

  PrefixSum(List<int> nums) {
    _prefix = List.filled(nums.length + 1, 0);
    for (int i = 0; i < nums.length; ++i) {
      _prefix[i + 1] = _prefix[i] + nums[i];
    }
  }

  // [l..r] oraliq yig'indisi
  int rangeSum(int l, int r) => _prefix[r + 1] - _prefix[l];
}

void main() {
  List<int> sonlar = [2, 4, 1, 7, 3];
  var ps = PrefixSum(sonlar);

  print("Sum(1..3) (4+1+7): ${ps.rangeSum(1, 3)}");
}
```

## Tushuntirish va Mantiq:
Prefiks yig'indisi orqali oraliq yig'indilarni $O(1)$ da hisoblash mumkin.

## Ishlash natijasi:
```text
Sum(1..3) (4+1+7): 12
```

# 245-Topshiriq: Kadane algoritmi: Maksimal qism massiv yig'indisi
## Topshiriq sharti:
Musbat va manfiy sonlardan iborat ro'yxatda ketma-ket maksimal yig'indini O(N) da hisoblang.

## Yechim (Dart kodi):
```dart
int maxSubArray(List<int> nums) {
  int currentSum = nums[0];
  int maxSum = nums[0];

  for (int i = 1; i < nums.length; ++i) {
    currentSum = (nums[i] > currentSum + nums[i]) ? nums[i] : currentSum + nums[i];
    if (currentSum > maxSum) maxSum = currentSum;
  }
  return maxSum;
}

void main() {
  List<int> arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4];
  print("Maksimal qism massiv yig'indisi: ${maxSubArray(arr)}");
}
```

## Tushuntirish va Mantiq:
Kadane algoritmi dinamik dasturlash tamoyili asosida chiziqli vaqtda ishlaydi.

## Ishlash natijasi:
```text
Maksimal qism massiv yig'indisi: 6
```

# 246-Topshiriq: Ikki ko'rsatkichli Two Sum masalasi saralangan ro'yxatda
## Topshiriq sharti:
Saralangan ro'yxatdan yig'indisi `target` ga teng bo'lgan ikkita element indeksini O(N) da toping.

## Yechim (Dart kodi):
```dart
(int, int)? twoSumSorted(List<int> numbers, int target) {
  int left = 0;
  int right = numbers.length - 1;

  while (left < right) {
    int sum = numbers[left] + numbers[right];
    if (sum == target) return (left, right);
    if (sum < target) left++;
    else right--;
  }
  return null;
}

void main() {
  List<int> sorted = [2, 7, 11, 15];
  var juftlik = twoSumSorted(sorted, 9);

  print("Yig'indisi 9 bo'lgan indekslar: $juftlik");
}
```

## Tushuntirish va Mantiq:
Saralangan massivda ikki chetdan yaqinlashish O(N) optimal vaqtni ta'minlaydi.

## Ishlash natijasi:
```text
Yig'indisi 9 bo'lgan indekslar: (0, 1)
```

# 247-Topshiriq: Ro'yxat ichidan eng katta K ta elementni topish (Top-K)
## Topshiriq sharti:
Massivni to'liq saralamasdan yoki qisman saralash orqali eng yuqori K ta elementni ajrating.

## Yechim (Dart kodi):
```dart
List<int> topK(List<int> list, int k) {
  List<int> nusxa = List.from(list);
  nusxa.sort((a, b) => b.compareTo(a)); // Kamayish tartibida
  return nusxa.take(k).toList();
}

void main() {
  List<int> ballar = [45, 89, 12, 95, 78, 64, 99];
  print("Top-3 eng yuqori ballar: ${topK(ballar, 3)}");
}
```

## Tushuntirish va Mantiq:
Top-K algoritmlari tavsiya tizimlari va qidiruv natijalarining birinchi sahifalarini tuzishda asosiy vositadir.

## Ishlash natijasi:
```text
Top-3 eng yuqori ballar: [99, 95, 89]
```

# 248-Topshiriq: Ro'yxat elementlari kombinatsiyalari (Juftliklar generatsiyasi)
## Topshiriq sharti:
Ro'yxatdagi barcha takrorlanmas juftliklarni `(a, b)` ichma-ich sikllar bilan hosil qiling.

## Yechim (Dart kodi):
```dart
List<(T, T)> juftliklar<T>(List<T> list) {
  List<(T, T)> res = [];
  for (int i = 0; i < list.length; ++i) {
    for (int j = i + 1; j < list.length; ++j) {
      res.add((list[i], list[j]));
    }
  }
  return res;
}

void main() {
  List<String> jamoalar = ["Paxtakor", "Nasaf", "Navbahor"];
  var o'yinlar = juftliklar(jamoalar);

  print("Barcha uchrashuvlar juftliklari:");
  o'yinlar.forEach((o) => print("- ${o.$1} vs ${o.$2}"));
}
```

## Tushuntirish va Mantiq:
Kombinatorika masalalarida $C(n, 2) = n(n-1)/2$ ta juftlik bitta ichma-ich sikl orqali hosil qilinadi.

## Ishlash natijasi:
```text
Barcha uchrashuvlar juftliklari:
- Paxtakor vs Nasaf
- Paxtakor vs Navbahor
- Nasaf vs Navbahor
```

# 249-Topshiriq: Ro'yxatni saralanganligini tekshirish (isSorted)
## Topshiriq sharti:
Ro'yxat o'sish tartibida tartiblangan yoki yo'qligini O(N) da tekshiruvchi funksiya yozing.

## Yechim (Dart kodi):
```dart
bool isSorted(List<int> list) {
  for (int i = 0; i < list.length - 1; ++i) {
    if (list[i] > list[i + 1]) return false;
  }
  return true;
}

void main() {
  print("[1, 2, 5, 8] saralanganmi: ${isSorted([1, 2, 5, 8])}");
  print("[1, 5, 2, 8] saralanganmi: ${isSorted([1, 5, 2, 8])}");
}
```

## Tushuntirish va Mantiq:
Qo'shni juftliklarni bir marta tekshirib chiqish massivning tartiblanganligini tasdiqlash uchun yetarlidir.

## Ishlash natijasi:
```text
[1, 2, 5, 8] saralanganmi: true
[1, 5, 2, 8] saralanganmi: false
```

# 250-Topshiriq: Katta amaliy loyiha: Xarid savatchasi va inventar boshqaruv tizimi
## Topshiriq sharti:
250-topshiriq: Mahsulot qo'shish, miqdorini o'zgartirish, o'chirish, qidirish va chegirmali jami chek summasini hisoblovchi to'liq `ShoppingCart` sinfini yozing.

## Yechim (Dart kodi):
```dart
class CartItem {
  final String id;
  final String title;
  final double price;
  int quantity;

  CartItem({required this.id, required this.title, required this.price, this.quantity = 1});

  double get total => price * quantity;

  @override
  String toString() => "$title x$quantity = ${total.toStringAsFixed(0)} so'm";
}

class ShoppingCart {
  final List<CartItem> _items = [];

  void addItem(String id, String title, double price) {
    var existing = _items.where((item) => item.id == id).firstOrNull;
    if (existing != null) {
      existing.quantity++;
    } else {
      _items.add(CartItem(id: id, title: title, price: price));
    }
  }

  void removeItem(String id) {
    _items.removeWhere((item) => item.id == id);
  }

  double calculateTotal({double discountPercent = 0.0}) {
    double subtotal = _items.fold(0.0, (acc, item) => acc + item.total);
    return subtotal * (1.0 - discountPercent / 100.0);
  }

  void printReceipt() {
    print("================ XARID CHEKI ================");
    for (var item in _items) {
      print("- $item");
    }
    print("---------------------------------------------");
    print("Jami summa: ${calculateTotal().toStringAsFixed(0)} so'm");
    print("10% chegirma bilan: ${calculateTotal(discountPercent: 10).toStringAsFixed(0)} so'm");
    print("=============================================");
  }
}

void main() {
  var cart = ShoppingCart();
  cart.addItem("p1", "Qahva", 25000);
  cart.addItem("p2", "Shokolad", 18000);
  cart.addItem("p1", "Qahva", 25000); // 2 ta bo'ladi

  cart.printReceipt();
}
```

## Tushuntirish va Mantiq:
250-topshiriq bilan Dart tilida `List` kolleksiyalari, ob'ektlar bilan ishlash, filtrlash, yig'ish va zamonaviy ma'lumotlar oqimi to'liq o'zlashtirildi.

## Ishlash natijasi:
```text
================ XARID CHEKI ================
- Qahva x2 = 50000 so'm
- Shokolad x1 = 18000 so'm
---------------------------------------------
Jami summa: 68000 so'm
10% chegirma bilan: 61200 so'm
=============================================
```

