# 601-Topshiriq: Iterable dangasaligi (Lazy Evaluation)

## Topshiriq sharti:
`map` yoki `where` metodi darhol bajarilmasdan, faqat qiymat so'ralgandagina ishlashini ko'rsating.

## Yechim (Dart kodi):
```dart
void main() {
  var sonlar = [1, 2, 3];

  var dangasalar = sonlar.map((n) {
    print('Hisoblandi: $n');
    return n * 2;
  });

  print('Map chaqirildi, lekin hali hech narsa hisoblanmadi!');
  print('Endi birinchi element olinmoqda:');
  print('Natija: ${dangasalar.first}');
}
```

## Tushuntirish va Mantiq:
Dartda `Iterable` amallari dangasa (lazy) bo'lib, ular faqat elementga murojaat qilingandagina (masalan `.first` yoki `.toList()`) hisoblanadi.

## Ishlash natijasi:
```text
Map chaqirildi, lekin hali hech narsa hisoblanmadi!
Endi birinchi element olinmoqda:
Hisoblandi: 1
Natija: 2
```

# 602-Topshiriq: map() metodi asoslari

## Topshiriq sharti:
Sonlar ro'yxatidagi har bir elementni kvadratiga oshirib yangi ro'yxatga aylantiring.

## Yechim (Dart kodi):
```dart
void main() {
  var sonlar = [1, 2, 3, 4, 5];
  var kvadratlar = sonlar.map((x) => x * x).toList();

  print('Asl sonlar: $sonlar');
  print('Kvadratlar: $kvadratlar');
}
```

## Tushuntirish va Mantiq:
`map()` kolleksiyaning har bir elementini qabul qilib, o'zgartirilgan yangi elementlar to'plamini qaytaradi.

## Ishlash natijasi:
```text
Asl sonlar: [1, 2, 3, 4, 5]
Kvadratlar: [1, 4, 9, 16, 25]
```

# 603-Topshiriq: where() metodi bilan filtrlash

## Topshiriq sharti:
Ro'yxatdan faqat musbat va juft sonlarni ajratib oluvchi shartli filtr dasturini tuzing.

## Yechim (Dart kodi):
```dart
void main() {
  var sonlar = [-10, 5, 8, -4, 12, 7, 0, 16];
  var natija = sonlar.where((n) => n > 0 && n % 2 == 0).toList();

  print('Musbat va juft sonlar: $natija');
}
```

## Tushuntirish va Mantiq:
`where()` berilgan mantiqiy predikat rost (true) bo'lgan elementlarnigina o'tkazadi.

## Ishlash natijasi:
```text
Musbat va juft sonlar: [8, 12, 16]
```

# 604-Topshiriq: map() va where() zanjiri (Method Chaining)

## Topshiriq sharti:
Matnlar ro'yxatidan bo'sh bo'lmaganlarini ajratib, bosh harflarga o'tkazuvchi funksional zanjir tuzing.

## Yechim (Dart kodi):
```dart
void main() {
  var qatorlar = ['dart', '', 'flutter', '   ', 'web', 'ai'];

  var tozalangan = qatorlar
      .map((s) => s.trim())
      .where((s) => s.isNotEmpty)
      .map((s) => s.toUpperCase())
      .toList();

  print('Tozalangan va bosh harflarda: $tozalangan');
}
```

## Tushuntirish va Mantiq:
Funksional zanjir amallarni ketma-ket, qo'shimcha oraliq o'zgaruvchilarsiz toza bajarish imkonini beradi.

## Ishlash natijasi:
```text
Tozalangan va bosh harflarda: [DART, FLUTTER, WEB, AI]
```

# 605-Topshiriq: expand() metodi (1 dan ko'pga o'tkazish)

## Topshiriq sharti:
Har bir so'zni harflarga ajratib, barcha harflarni bitta tekis ro'yxatga yig'uvchi dastur yozing.

## Yechim (Dart kodi):
```dart
void main() {
  var sozlar = ['salom', 'dart'];

  var harflar = sozlar.expand((s) => s.split('')).toList();
  print('Barcha harflar: $harflar');
}
```

## Tushuntirish va Mantiq:
`expand()` har bir element uchun kichik ro'yxat hosil qilib, ularni bitta tekis `Iterable` ga yoyib beradi (flatMap analogi).

## Ishlash natijasi:
```text
Barcha harflar: [s, a, l, o, m, d, a, r, t]
```

# 606-Topshiriq: fold() metodi va boshlang'ich qiymat bilan agregatsiya

## Topshiriq sharti:
Boshlang'ich qiymat 100 bo'lgan holda ro'yxatdagi barcha xarajatlarni hisobdan ayirib boring.

## Yechim (Dart kodi):
```dart
void main() {
  var xarajatlar = [15, 20, 35];
  double boshlangichBalans = 100.0;

  double qoldiq = xarajatlar.fold(
    boshlangichBalans,
    (jami, xarajat) => jami - xarajat,
  );

  print('Qoldiq balans: $qoldiq');
}
```

## Tushuntirish va Mantiq:
`fold(initialValue, (prev, element) => ...)` har doim boshlang'ich qiymatdan boshlab elementlarni yagona natijaga keltirib beradi.

## Ishlash natijasi:
```text
Qoldiq balans: 30.0
```

# 607-Topshiriq: reduce() metodi bilan umumiy ko'paytma

## Topshiriq sharti:
Ro'yxatdagi barcha sonlarning ko'paytmasini `reduce` yordamida hisoblang.

## Yechim (Dart kodi):
```dart
void main() {
  var sonlar = [2, 3, 4, 5];
  int kopaytma = sonlar.reduce((a, b) => a * b);

  print('Umumiy ko\'paytma: $kopaytma');
}
```

## Tushuntirish va Mantiq:
`reduce()` ro'yxatning birinchi elementini boshlang'ich deb oladi va qolganlarini ketma-ket jamlaydi (ro'yxat bo'sh bo'lmasligi shart).

## Ishlash natijasi:
```text
Umumiy ko'paytma: 120
```

# 608-Topshiriq: any() va every() predikat tekshiruvlari

## Topshiriq sharti:
Guruhda 18 yoshdan kichiklar bor-yo'qligini (`any`) va barcha talabalar o'tganligini (`every`) tekshiring.

## Yechim (Dart kodi):
```dart
void main() {
  var yoshlar = [19, 21, 25, 17, 30];
  var ballar = [85, 90, 78, 65, 92];

  bool voyagaYetmaganBormi = yoshlar.any((y) => y < 18);
  bool hammaOtdimi = ballar.every((b) => b >= 60);

  print('18 dan kichik bormi: $voyagaYetmaganBormi');
  print('Hamma imtihondan o\'tdimi: $hammaOtdimi');
}
```

## Tushuntirish va Mantiq:
`any()` bitta bo'lsa ham mos element topsa `true`, `every()` esa hamma elementlar mos kelsagina `true` qaytaradi.

## Ishlash natijasi:
```text
18 dan kichik bormi: true
Hamma imtihondan o'tdimi: true
```

# 609-Topshiriq: take() va skip() bilan qismlarga ajratish

## Topshiriq sharti:
Ro'yxatning dastlabki 2 ta elementini tashlab yuborib (`skip`), keyingi 3 tasini olish (`take`) dasturini tuzing.

## Yechim (Dart kodi):
```dart
void main() {
  var sonlar = [10, 20, 30, 40, 50, 60, 70];

  var oraliq = sonlar.skip(2).take(3).toList();
  print('skip(2).take(3): $oraliq');
}
```

## Tushuntirish va Mantiq:
`skip(n)` boshidagi n ta elementni tashlab yuboradi, `take(m)` esa ketidan keluvchi ko'pi bilan m ta elementni oladi.

## Ishlash natijasi:
```text
skip(2).take(3): [30, 40, 50]
```

# 610-Topshiriq: takeWhile() va skipWhile() shartli kesish

## Topshiriq sharti:
Son musbat bo'lib turguniga qadar elementlarni olish (`takeWhile`) amalini qo'llang.

## Yechim (Dart kodi):
```dart
void main() {
  var oqim = [1, 3, 5, -2, 7, 9];

  var faqatBoshidagiMusbatlar = oqim.takeWhile((x) => x > 0).toList();
  var manfiydanKeyingilar = oqim.skipWhile((x) => x > 0).toList();

  print('Boshidagi musbatlar: $faqatBoshidagiMusbatlar');
  print('Manfiydan boshlab:   $manfiydanKeyingilar');
}
```

## Tushuntirish va Mantiq:
`takeWhile` shart yolg'on bo'lishi bilanoq to'xtaydi, `skipWhile` esa shart buzilgan paytdan boshlab qolgan barcha elementlarni oladi.

## Ishlash natijasi:
```text
Boshidagi musbatlar: [1, 3, 5]
Manfiydan boshlab:   [-2, 7, 9]
```

# 611-Topshiriq: firstWhere() va orElse xavfsiz qidiruv

## Topshiriq sharti:
Element topilmasa `StateError` xatosi tashlamasdan standart qiymat qaytaruvchi `orElse` parametrini qo'llang.

## Yechim (Dart kodi):
```dart
void main() {
  var sonlar = [5, 11, 23, 47];

  // 10 ga karrali birinchi son
  int topildi = sonlar.firstWhere(
    (n) => n % 10 == 0,
    orElse: () => -1,
  );

  print('10 ga karrali son: $topildi');
}
```

## Tushuntirish va Mantiq:
`firstWhere(test, orElse: () => def)` metodi element topilmagan holatda `orElse` dagi natijani xavfsiz qaytaradi.

## Ishlash natijasi:
```text
10 ga karrali son: -1
```

# 612-Topshiriq: lastWhere() metodi (Oxirgi mos elementni topish)

## Topshiriq sharti:
Ro'yxat ichidagi oxirgi juft sonni aniqlovchi dasturni tuzing.

## Yechim (Dart kodi):
```dart
void main() {
  var sonlar = [1, 4, 7, 8, 9, 12, 13];

  int oxirgiJuft = sonlar.lastWhere((n) => n % 2 == 0);
  print('Oxirgi juft son: $oxirgiJuft');
}
```

## Tushuntirish va Mantiq:
`lastWhere()` kolleksiyani orqasidan boshlab qidiradi va shartni qanoatlantiruvchi eng oxirgi elementni qaytaradi.

## Ishlash natijasi:
```text
Oxirgi juft son: 12
```

# 613-Topshiriq: singleWhere() metodi (Faqat bitta mos element)

## Topshiriq sharti:
Kolleksiyada shartga mos keluvchi yagona element borligini tekshirib uni oluvchi metodni ko'rsating.

## Yechim (Dart kodi):
```dart
void main() {
  var foydalanuvchilar = [
    {'id': 1, 'rol': 'foydalanuvchi'},
    {'id': 2, 'rol': 'admin'},
    {'id': 3, 'rol': 'foydalanuvchi'},
  ];

  var admin = foydalanuvchilar.singleWhere((u) => u['rol'] == 'admin');
  print('Yagona admin topildi: $admin');
}
```

## Tushuntirish va Mantiq:
`singleWhere()` agar shartga mos element 0 ta bo'lsa yoki 1 tadan ko'p bo'lsa darhol xatolik tashlaydi.

## Ishlash natijasi:
```text
Yagona admin topildi: {id: 2, rol: admin}
```

# 614-Topshiriq: followedBy() metodi (Dangasa birlashtirish)

## Topshiriq sharti:
Ikkita to'plamni yangi xotira ajratmasdan, bitta dangasa oqim sifatida birlashtiring.

## Yechim (Dart kodi):
```dart
void main() {
  var bosh = [1, 2, 3];
  var oxir = [4, 5, 6];

  var birlashma = bosh.followedBy(oxir);
  print('Birlashgan ketma-ketlik: ${birlashma.toList()}');
}
```

## Tushuntirish va Mantiq:
`followedBy()` yangi ro'yxat nusxasini yaratmasdan, ikkala kolleksiyani virtual zanjir sifatida ulaydi.

## Ishlash natijasi:
```text
Birlashgan ketma-ketlik: [1, 2, 3, 4, 5, 6]
```

# 615-Topshiriq: whereType<T>() bilan aniq turni filtrlash

## Topshiriq sharti:
Turli tiplar aralashgan ro'yxatdan faqat `double` tipidagi elementlarni ajratib oling.

## Yechim (Dart kodi):
```dart
void main() {
  var aralash = [1, 2.5, 'uch', 4.0, true, 5.75];

  var kasrlar = aralash.whereType<double>().toList();
  print('Faqat double sonlar: $kasrlar');
}
```

## Tushuntirish va Mantiq:
`whereType<T>()` filtrlash va avtomatik tur o'tkazishni (casting) bitta amalda xavfsiz bajaradi.

## Ishlash natijasi:
```text
Faqat double sonlar: [2.5, 4.0, 5.75]
```

# 616-Topshiriq: sync* generator funksiyasi va yield

## Topshiriq sharti:
`sync*` va `yield` yordamida sinxron ma'lumotlar oqimini generatsiya qiluvchi funksiya tuzing.

## Yechim (Dart kodi):
```dart
Iterable<int> oraliq(int start, int end) sync* {
  for (int i = start; i <= end; i++) {
    yield i;
  }
}

void main() {
  for (var son in oraliq(1, 5)) {
    print('Generator son: $son');
  }
}
```

## Tushuntirish va Mantiq:
`sync*` funksiyalari `yield` orqali qiymatlarni bittalab uzatadi va xotirani keraksiz to'ldirmaydi.

## Ishlash natijasi:
```text
Generator son: 1
Generator son: 2
Generator son: 3
Generator son: 4
Generator son: 5
```

# 617-Topshiriq: sync* orqali cheksiz Fibonacci oqimi

## Topshiriq sharti:
Cheksiz Fibonacci sonlarini hosil qiluvchi generator tuzing va undan `take(8)` orqali dastlabki 8 tasini oling.

## Yechim (Dart kodi):
```dart
Iterable<int> fibonacciGenerator() sync* {
  int a = 0, b = 1;
  while (true) {
    yield a;
    int temp = a + b;
    a = b;
    b = temp;
  }
}

void main() {
  var dastlabki8 = fibonacciGenerator().take(8).toList();
  print('Dastlabki 8 ta Fibonachchi soni: $dastlabki8');
}
```

## Tushuntirish va Mantiq:
Cheksiz generatorlar faqat so'ralgan miqdorda ishlaydi, `take(8)` olingach tsikl to'xtaydi.

## Ishlash natijasi:
```text
Dastlabki 8 ta Fibonachchi soni: [0, 1, 1, 2, 3, 5, 8, 13]
```

# 618-Topshiriq: yield* orqali boshqa oqimni kiritish

## Topshiriq sharti:
Generator ichida boshqa generator yoki ro'yxatni `yield*` orqali to'liq uzating.

## Yechim (Dart kodi):
```dart
Iterable<int> juftlar() sync* {
  yield 2;
  yield 4;
}

Iterable<int> barchaSonlar() sync* {
  yield 1;
  yield* juftlar(); // Boshqa oqimni to'liq uzatish
  yield 5;
}

void main() {
  print(barchaSonlar().toList());
}
```

## Tushuntirish va Mantiq:
`yield*` boshqa `Iterable` kolleksiyasining barcha elementlarini delegatsiya qilib joriy oqimga ulaydi.

## Ishlash natijasi:
```text
[1, 2, 4, 5]
```

# 619-Topshiriq: Iterable.generate() konstruktori

## Topshiriq sharti:
Indeks asosida elementlarni hosil qiluvchi `Iterable.generate` dan foydalaning.

## Yechim (Dart kodi):
```dart
void main() {
  var kvadratlar = Iterable<int>.generate(5, (i) => (i + 1) * (i + 1));
  print('Kvadratlar oqimi: ${kvadratlar.toList()}');
}
```

## Tushuntirish va Mantiq:
`Iterable.generate(count, generator)` ro'yxatni formulalar asosida ixcham to'ldirish imkonini beradi.

## Ishlash natijasi:
```text
Kvadratlar oqimi: [1, 4, 9, 16, 25]
```

# 620-Topshiriq: O'rtacha qiymatni fold orqali hisoblash

## Topshiriq sharti:
Sonlar ro'yxatining arifmetik o'rtachasini funksional usulda `fold` yordamida hisoblang.

## Yechim (Dart kodi):
```dart
void main() {
  var ballar = [80, 95, 75, 90, 85];

  double yigindi = ballar.fold(0.0, (sum, val) => sum + val);
  double ortacha = yigindi / ballar.length;

  print('O\'rtacha ball: ${ortacha.toStringAsFixed(1)}');
}
```

## Tushuntirish va Mantiq:
`fold` yordamida yig'indini hisoblab, uzunlikka bo'lish orqali o'rtacha qiymat topiladi.

## Ishlash natijasi:
```text
O'rtacha ball: 85.0
```

# 621-Topshiriq: Matn so'zlaridagi harflar sonini hisoblash

## Topshiriq sharti:
Gapdagi so'zlar uzunligini hisoblab, jami harflar sonini funksional zanjirda toping.

## Yechim (Dart kodi):
```dart
void main() {
  String gap = 'O\'zbekiston kelajagi buyuk davlat';

  int jamiHarflar = gap
      .split(' ')
      .map((soz) => soz.length)
      .reduce((a, b) => a + b);

  print('So\'zlardagi jami harflar: $jamiHarflar');
}
```

## Tushuntirish va Mantiq:
Matn so'zlarga bo'linadi, har birining uzunligi `map` orqali olinadi va `reduce` bilan jamlanadi.

## Ishlash natijasi:
```text
So'zlardagi jami harflar: 30
```

# 622-Topshiriq: Talabalar reytingini funksional tahlil qilish

## Topshiriq sharti:
Talabalar ro'yxatidan 80 dan yuqori ball to'plaganlarning ismlarini alifbo tartibida oling.

## Yechim (Dart kodi):
```dart
class Talaba {
  final String ism;
  final int ball;
  Talaba(this.ism, this.ball);
}

void main() {
  var talabalar = [
    Talaba('Zokir', 75),
    Talaba('Ali', 92),
    Talaba('Bekzod', 88),
    Talaba('Dilorom', 64),
  ];

  var aotchilar = talabalar
      .where((t) => t.ball >= 80)
      .map((t) => t.ism)
      .toList()
    ..sort();

  print('80+ olganlar: $aotchilar');
}
```

## Tushuntirish va Mantiq:
`where` -> `map` -> `sort` ketma-ketligi murakkab ma'lumotlarni saralash va filtratsiyalash uchun standartdir.

## Ishlash natijasi:
```text
80+ olganlar: [Ali, Bekzod]
```

# 623-Topshiriq: Map ustida funksional amallar (entries.map)

## Topshiriq sharti:
Lug'atning har bir juftligini formatlangan matnga aylantirishni `entries.map` orqali bajaring.

## Yechim (Dart kodi):
```dart
void main() {
  Map<String, double> narxlar = {
    'Olma': 12000,
    'Banan': 24000,
    'Uzum': 18000,
  };

  var narxlarMatni = narxlar.entries
      .map((e) => '${e.key}: ${e.value.toStringAsFixed(0)} so\'m')
      .join(', ');

  print('Katalog: $narxlarMatni');
}
```

## Tushuntirish va Mantiq:
`Map.entries` orqali Map xuddi `Iterable<MapEntry>` kabi barcha funksional metodlardan foydalana oladi.

## Ishlash natijasi:
```text
Katalog: Olma: 12000 so'm, Banan: 24000 so'm, Uzum: 18000 so'm
```

# 624-Topshiriq: Ikki ro'yxatni parallel juftlash (Zip funksiyasi)

## Topshiriq sharti:
Ikkita teng uzunlikdagi ro'yxatni parallel juftlab Recordlar ro'yxatiga aylantiruvchi `zip` funksiyasini yozing.

## Yechim (Dart kodi):
```dart
Iterable<(A, B)> zip<A, B>(List<A> a, List<B> b) sync* {
  int len = a.length < b.length ? a.length : b.length;
  for (int i = 0; i < len; i++) {
    yield (a[i], b[i]);
  }
}

void main() {
  var ismlar = ['Ali', 'Vali', 'G\'ani'];
  var yoshlar = [20, 25, 22];

  for (var (ism, yosh) in zip(ismlar, yoshlar)) {
    print('$ism: $yosh yoshda');
  }
}
```

## Tushuntirish va Mantiq:
Python dagi `zip()` funksiyasiga o'xshash ushbu generator ikkita oqimni elementma-element parallel birlashtiradi.

## Ishlash natijasi:
```text
Ali: 20 yoshda
Vali: 25 yoshda
G'ani: 22 yoshda
```

# 625-Topshiriq: Sirg'aluvchi oyna (Sliding Window) algoritmi

## Topshiriq sharti:
Ketma-ket N tadan elementni qamrab oluvchi sirg'aluvchi oyna funksional generatorini tuzing.

## Yechim (Dart kodi):
```dart
Iterable<List<T>> slidingWindow<T>(List<T> royxat, int windowSize) sync* {
  if (royxat.length < windowSize) return;
  for (int i = 0; i <= royxat.length - windowSize; i++) {
    yield royxat.sublist(i, i + windowSize);
  }
}

void main() {
  var sonlar = [1, 2, 3, 4, 5];
  var oynalar = slidingWindow(sonlar, 3).toList();

  print('3 talik sirg\'aluvchi oynalar: $oynalar');
}
```

## Tushuntirish va Mantiq:
Sliding Window ma'lumotlar tahlili, harakatlanuvchi o'rtachalar (moving average) va AI token kontekstini kesishda keng qo'llaniladi.

## Ishlash natijasi:
```text
3 talik sirg'aluvchi oynalar: [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
```

# 626-Topshiriq: Funksiyalar kompozitsiyasi (compose)

## Topshiriq sharti:
Ikkita funksiyani birlashtirib, birining chiqishini ikkinchisiga uzatuvchi `compose` funksiyasini yozing.

## Yechim (Dart kodi):
```dart
R Function(A) compose<A, B, R>(R Function(B) g, B Function(A) f) {
  return (A x) => g(f(x));
}

int ikkiKopaytir(int x) => x * 2;
int beshQosh(int x) => x + 5;

void main() {
  // (x + 5) * 2
  var hisobla = compose(ikkiKopaytir, beshQosh);
  print('Natija: ${hisobla(10)}'); // (10 + 5) * 2 = 30
}
```

## Tushuntirish va Mantiq:
Funksiyalar kompozitsiyasi matematik $(g \circ f)(x) = g(f(x))$ tamoyilini dasturlashda qo'llashdir.

## Ishlash natijasi:
```text
Natija: 30
```

# 627-Topshiriq: Funksiyani Karri-lashtirish (Currying)

## Topshiriq sharti:
Bir nechta argumentli funksiyani ketma-ket bir argumentli funksiyalar zanjiriga aylantiring.

## Yechim (Dart kodi):
```dart
int Function(int) qoshish(int a) {
  return (int b) => a + b;
}

void main() {
  var unQosh = qoshish(10);

  print('10 + 5 = ${unQosh(5)}');
  print('10 + 20 = ${unQosh(20)}');
}
```

## Tushuntirish va Mantiq:
Currying murakkab funksiyalarni qismlab ixtisoslashtirish va yangi qayta ishlatiluvchi funksiyalar yasashga xizmat qiladi.

## Ishlash natijasi:
```text
10 + 5 = 15
10 + 20 = 30
```

# 628-Topshiriq: Qisman qo'llash (Partial Application)

## Topshiriq sharti:
Ko'p parametrli funksiyaning dastlabki parametrlarini qotirib, yangi funksiya hosil qiling.

## Yechim (Dart kodi):
```dart
double chegirmaHisobla(double stavka, double narx) => narx * (1 - stavka);

void main() {
  // 10% li chegirma funksiyasini qisman hosil qilamiz
  double onFoizChegirma(double narx) => chegirmaHisobla(0.10, narx);

  print('100 mingdan: ${onFoizChegirma(100000)} so\'m');
  print('500 mingdan: ${onFoizChegirma(500000)} so\'m');
}
```

## Tushuntirish va Mantiq:
Partial application funksiya parametrlarining bir qismini oldindan belgilab, soddaroq funksiyalar yaratadi.

## Ishlash natijasi:
```text
100 mingdan: 90000.0 so'm
500 mingdan: 450000.0 so'm
```

# 629-Topshiriq: Memoization yuqori tartibli funksiyasi

## Topshiriq sharti:
Har qanday funksiya natijasini avtomatik xotirada saqlovchi umumiy `memoize` bezakchisini yozing.

## Yechim (Dart kodi):
```dart
R Function(T) memoize<T, R>(R Function(T) fn) {
  final Map<T, R> kesh = {};
  return (T arg) {
    return kesh.putIfAbsent(arg, () => fn(arg));
  };
}

int ogirHisoblash(int n) {
  print('Hisoblandi: $n');
  return n * n;
}

void main() {
  var tezkor = memoize(ogirHisoblash);

  print(tezkor(4));
  print(tezkor(4)); // Keshdan olinadi
}
```

## Tushuntirish va Mantiq:
`memoize` funksiyaning oldingi hisob-kitoblarini yodda saqlab, bir xil kirish uchun qayta hisoblashni bekor qiladi.

## Ishlash natijasi:
```text
Hisoblandi: 4
16
16
```

# 630-Topshiriq: Transpose funksional usulda

## Topshiriq sharti:
Matritsani (satrlar va ustunlar o'rnini) `Iterable.generate` va `map` yordamida transponirlang.

## Yechim (Dart kodi):
```dart
void main() {
  List<List<int>> m = [
    [1, 2, 3],
    [4, 5, 6],
  ];

  int rows = m.length;
  int cols = m[0].length;

  var transponirlangan = List.generate(
    cols,
    (c) => List.generate(rows, (r) => m[r][c]),
  );

  print('Transponirlangan: $transponirlangan');
}
```

## Tushuntirish va Mantiq:
Funksional ro'yxat generatsiyasi orqali matritsa satr va ustunlari o'rni toza almashtiriladi.

## Ishlash natijasi:
```text
Transponirlangan: [[1, 4], [2, 5], [3, 6]]
```

# 631-Topshiriq: So'zlar chastotasini hisoblash (Word frequency)

## Topshiriq sharti:
Matndagi so'zlarning necha marta uchrashini `fold` va `Map` yordamida hisoblang.

## Yechim (Dart kodi):
```dart
void main() {
  var matn = 'dart flutter dart ai flutter dart';
  var sozlar = matn.split(' ');

  var chastota = sozlar.fold<Map<String, int>>({}, (map, soz) {
    map[soz] = (map[soz] ?? 0) + 1;
    return map;
  });

  print('Chastota xaritasi: $chastota');
}
```

## Tushuntirish va Mantiq:
`fold` boshlang'ich bo'sh lug'at bilan boshlanib, har bir so'zning sanoq sonini yangilab boradi.

## Ishlash natijasi:
```text
Chastota xaritasi: {dart: 3, flutter: 2, ai: 1}
```

# 632-Topshiriq: Harakatlanuvchi O'rtacha (Moving Average)

## Topshiriq sharti:
Keltirilgan oyna uzunligi bo'yicha harakatlanuvchi o'rtacha qiymatlarni hisoblang.

## Yechim (Dart kodi):
```dart
List<double> movingAverage(List<double> data, int window) {
  List<double> result = [];
  for (int i = 0; i <= data.length - window; i++) {
    var sub = data.sublist(i, i + window);
    double avg = sub.reduce((a, b) => a + b) / window;
    result.add(avg);
  }
  return result;
}

void main() {
  var narxlar = [10.0, 20.0, 30.0, 40.0, 50.0];
  var ma = movingAverage(narxlar, 3);

  print('3 kunlik MA: $ma');
}
```

## Tushuntirish va Mantiq:
Harakatlanuvchi o'rtacha moliya va signallarni tekislashda ma'lumotlardagi shovqinlarni yo'qotish uchun qo'llaniladi.

## Ishlash natijasi:
```text
3 kunlik MA: [20.0, 30.0, 40.0]
```

# 633-Topshiriq: Predikatlarni mantiqiy birlashtirish (and/or)

## Topshiriq sharti:
Ikkita tekshiruv funksiyasini birlashtiruvchi `va` (and) hamda `yoki` (or) yordamchi funksiyalarini yozing.

## Yechim (Dart kodi):
```dart
bool Function(T) va<T>(bool Function(T) p1, bool Function(T) p2) {
  return (x) => p1(x) && p2(x);
}

void main() {
  bool musbat(int n) => n > 0;
  bool juft(int n) => n % 2 == 0;

  var musbatJuft = va(musbat, juft);

  print('4 musbat va juftmi: ${musbatJuft(4)}');
  print('-2 musbat va juftmi: ${musbatJuft(-2)}');
}
```

## Tushuntirish va Mantiq:
Predikatlar kompozitsiyasi shartli mantiqni alohida kichik qismlardan yig'ishga yordam beradi.

## Ishlash natijasi:
```text
4 musbat va juftmi: true
-2 musbat va juftmi: false
```

# 634-Topshiriq: Cheksiz Tub Sonlar Generator oqimi (sync*)

## Topshiriq sharti:
Barcha tub sonlarni cheksiz ravishda bittalab hisoblovchi generator yozing.

## Yechim (Dart kodi):
```dart
bool tubmi(int n) {
  if (n < 2) return false;
  for (int i = 2; i * i <= n; i++) {
    if (n % i == 0) return false;
  }
  return true;
}

Iterable<int> tubSonlar() sync* {
  int n = 2;
  while (true) {
    if (tubmi(n)) yield n;
    n++;
  }
}

void main() {
  var birinchi5Tub = tubSonlar().take(5).toList();
  print('Dastlabki 5 ta tub son: $birinchi5Tub');
}
```

## Tushuntirish va Mantiq:
`sync*` cheksiz algoritmlarni qulay shakllantiradi va dasturchi faqat o'ziga kerak bo'lganicha (`take`) oladi.

## Ishlash natijasi:
```text
Dastlabki 5 ta tub son: [2, 3, 5, 7, 11]
```

# 635-Topshiriq: Kolleksiyadagi eng ko'p uchragan elementni topish (Moda)

## Topshiriq sharti:
Ro'yxat ichida eng ko'p takrorlangan elementni funksional usulda aniqlang.

## Yechim (Dart kodi):
```dart
T engKopUchragan<T>(List<T> royxat) {
  var counts = <T, int>{};
  for (var x in royxat) {
    counts[x] = (counts[x] ?? 0) + 1;
  }
  return counts.entries.reduce((a, b) => a.value > b.value ? a : b).key;
}

void main() {
  var harflar = ['a', 'b', 'c', 'b', 'a', 'b'];
  print('Eng ko\'p uchragani: ${engKopUchragan(harflar)}');
}
```

## Tushuntirish va Mantiq:
`entries.reduce` orqali qiymatlari (counts) eng katta bo'lgan juftlik bir qatorda aniqlanadi.

## Ishlash natijasi:
```text
Eng ko'p uchragani: b
```

# 636-Topshiriq: Elementlar orasiga ajratuvchi qo'shish (Intersperse)

## Topshiriq sharti:
Har bir element orasiga berilgan ajratuvchi elementni joylashtiruvchi generator yozing.

## Yechim (Dart kodi):
```dart
Iterable<T> ajratuvchiQosh<T>(Iterable<T> manba, T ajratuvchi) sync* {
  var it = manba.iterator;
  if (it.moveNext()) {
    yield it.current;
    while (it.moveNext()) {
      yield ajratuvchi;
      yield it.current;
    }
  }
}

void main() {
  var sonlar = [1, 2, 3];
  var natija = ajratuvchiQosh(sonlar, 0).toList();
  print('Natija: $natija');
}
```

## Tushuntirish va Mantiq:
Flutter UI da vidjetlar orasiga Divider yoki bo'sh joy (SizedBox) qo'yishda bu naqsh juda foydali.

## Ishlash natijasi:
```text
Natija: [1, 0, 2, 0, 3]
```

# 637-Topshiriq: Rekursiv tekislash (Deep Flatten)

## Topshiriq sharti:
Ixtiyoriy chuqurlikdagi ichma-ich ro'yxatlarni to'liq bitta tekis ro'yxatga aylantiring.

## Yechim (Dart kodi):
```dart
List<dynamic> chuqurTekisla(List<dynamic> royxat) {
  List<dynamic> natija = [];
  for (var e in royxat) {
    if (e is List) {
      natija.addAll(chuqurTekisla(e));
    } else {
      natija.add(e);
    }
  }
  return natija;
}

void main() {
  var murakkab = [1, [2, [3, 4], 5], 6];
  print('Tekislangan: ${chuqurTekisla(murakkab)}');
}
```

## Tushuntirish va Mantiq:
Rekursiv tekislash har qanday chuqurlikdagi daraxtsimon massivlarni tekis oqimga aylantiradi.

## Ishlash natijasi:
```text
Tekislangan: [1, 2, 3, 4, 5, 6]
```

# 638-Topshiriq: fold yordamida ro'yxatni teskarisiga o'girish

## Topshiriq sharti:
Ichki `.reversed` ishlatmasdan, faqat `fold` yordamida teskari ro'yxat hosil qiling.

## Yechim (Dart kodi):
```dart
void main() {
  var sonlar = [1, 2, 3, 4];

  var teskari = sonlar.fold<List<int>>([], (list, e) => [e, ...list]);
  print('Teskari: $teskari');
}
```

## Tushuntirish va Mantiq:
Har bir yangi elementni ro'yxat boshiga qo'shib borish orqali tabiiy teskari tartib hosil bo'ladi.

## Ishlash natijasi:
```text
Teskari: [4, 3, 2, 1]
```

# 639-Topshiriq: Dekart Ko'paytmasi (Cartesian Product)

## Topshiriq sharti:
Ikkita to'plam elementlarining barcha mumkin bo'lgan juftliklarini hosil qiluvchi dastur yozing.

## Yechim (Dart kodi):
```dart
void main() {
  var ranglar = ['Qizil', 'Oq'];
  var olchamlar = ['S', 'M', 'L'];

  var mahsulotlar = [
    for (var r in ranglar)
      for (var o in olchamlar) (r, o)
  ];

  print('Kombinatsiyalar: $mahsulotlar');
}
```

## Tushuntirish va Mantiq:
Ichma-ich `for` list comprehension yordamida Dekart ko'paytmasi ixcham hosil qilinadi.

## Ishlash natijasi:
```text
Kombinatsiyalar: [(Qizil, S), (Qizil, M), (Qizil, L), (Oq, S), (Oq, M), (Oq, L)]
```

# 640-Topshiriq: Kombinatsiyalar generatsiyasi (2 talik juftliklar)

## Topshiriq sharti:
Ro'yxat ichidan takrorlanmas barcha 2 talik kombinatsiyalarni toping.

## Yechim (Dart kodi):
```dart
void main() {
  var elementlar = ['A', 'B', 'C', 'D'];
  List<(String, String)> juftliklar = [];

  for (int i = 0; i < elementlar.length; i++) {
    for (int j = i + 1; j < elementlar.length; j++) {
      juftliklar.add((elementlar[i], elementlar[j]));
    }
  }

  print('Barcha 2 talik kombinatsiyalar: $juftliklar');
}
```

## Tushuntirish va Mantiq:
Kombinatorika masalalarida $C_n^2$ juftliklar sonini hisoblash algoritmi.

## Ishlash natijasi:
```text
Barcha 2 talik kombinatsiyalar: [(A, B), (A, C), (A, D), (B, C), (B, D), (C, D)]
```

# 641-Topshiriq: Xatoliklarni yutuvchi xavfsiz map (tryMap)

## Topshiriq sharti:
Sonlarga o'girishda xatolik bo'lsa, ularni tashlab ketuvchi xavfsiz konverter tuzing.

## Yechim (Dart kodi):
```dart
void main() {
  var qatorlar = ['10', 'abc', '25', 'nol', '42'];

  var sonlar = qatorlar
      .map(int.tryParse)
      .where((n) => n != null)
      .cast<int>()
      .toList();

  print('Xavfsiz olingan sonlar: $sonlar');
}
```

## Tushuntirish va Mantiq:
`int.tryParse` xato tashlamay null qaytaradi, `where` esa barcha null larni tozalab tashlaydi.

## Ishlash natijasi:
```text
Xavfsiz olingan sonlar: [10, 25, 42]
```

# 642-Topshiriq: Matn qatorlarini sanash va tahlil qilish

## Topshiriq sharti:
Ko'p qatorli matndan har bir qatordagi so'zlar sonini hisoblovchi dastur yozing.

## Yechim (Dart kodi):
```dart
void main() {
  var matn = '''Dart dasturlash tili
Juda tezkor va xavfsiz
BitNet AI modelini yaratamiz''';

  var tahlil = matn
      .split('
')
      .map((qator) => qator.trim().split(' ').length)
      .toList();

  print('Har bir qatordagi so\'zlar soni: $tahlil');
}
```

## Tushuntirish va Mantiq:
Matnli fayllar va hisobotlarni tahlil qilishda funksional qatorlar bo'yicha `map` qilish juda qulay.

## Ishlash natijasi:
```text
Har bir qatordagi so'zlar soni: [3, 4, 4]
```

# 643-Topshiriq: JSON ro'yxatidan ma'lum maydon bo'yicha yig'indi

## Topshiriq sharti:
Mahsulotlar lug'ati ro'yxatidan faqat oziq-ovqat toifasidagilarning umumiy summasini hisoblang.

## Yechim (Dart kodi):
```dart
void main() {
  var items = [
    {'nom': 'Non', 'tur': 'ovqat', 'narx': 4000},
    {'nom': 'Daftar', 'tur': 'kanselyariya', 'narx': 6000},
    {'nom': 'Sut', 'tur': 'ovqat', 'narx': 10000},
  ];

  int ovqatSummasi = items
      .where((it) => it['tur'] == 'ovqat')
      .map((it) => it['narx'] as int)
      .fold(0, (sum, narx) => sum + narx);

  print('Oziq-ovqat summasi: $ovqatSummasi so\'m');
}
```

## Tushuntirish va Mantiq:
Kolleksiyalardan ma'lum shart bo'yicha yig'indilarni olish (SQL `SUM WHERE`) funksional zanjir orqali bajariladi.

## Ishlash natijasi:
```text
Oziq-ovqat summasi: 14000 so'm
```

# 644-Topshiriq: takeLast(n) va skipLast(n) funksiyalari

## Topshiriq sharti:
Ro'yxatning oxirgi N ta elementini oluvchi yoki oxirgi N tasini tashlab ketuvchi funksiyalarni tuzing.

## Yechim (Dart kodi):
```dart
List<T> takeLast<T>(List<T> list, int n) {
  if (n >= list.length) return list;
  return list.sublist(list.length - n);
}

List<T> skipLast<T>(List<T> list, int n) {
  if (n >= list.length) return [];
  return list.sublist(0, list.length - n);
}

void main() {
  var sonlar = [1, 2, 3, 4, 5];

  print('Oxirgi 2 tasi: ${takeLast(sonlar, 2)}');
  print('Oxirgi 2 tasiz: ${skipLast(sonlar, 2)}');
}
```

## Tushuntirish va Mantiq:
Standart `take` va `skip` boshidan ishlasa, `takeLast` va `skipLast` oxiridan hisoblashga xizmat qiladi.

## Ishlash natijasi:
```text
Oxirgi 2 tasi: [4, 5]
Oxirgi 2 tasiz: [1, 2, 3]
```

# 645-Topshiriq: Elementlarni juft-juft qilib birlashtirish (Pairwise)

## Topshiriq sharti:
Qo'shni elementlar orasidagi farqni hisoblash uchun qo'shni juftliklar generatorini yozing.

## Yechim (Dart kodi):
```dart
Iterable<(T, T)> pairwise<T>(List<T> list) sync* {
  for (int i = 0; i < list.length - 1; i++) {
    yield (list[i], list[i + 1]);
  }
}

void main() {
  var haroratlar = [20, 22, 21, 25];

  for (var (old, yangi) in pairwise(haroratlar)) {
    print('$old -> $yangi (Farq: ${yangi - old})');
  }
}
```

## Tushuntirish va Mantiq:
Pairwise ketma-ketlikdagi o'zgarishlar tezligi va qiyoslashlarni hisoblashda ishlatiladi.

## Ishlash natijasi:
```text
20 -> 22 (Farq: 2)
22 -> 21 (Farq: -1)
21 -> 25 (Farq: 4)
```

# 646-Topshiriq: Funksional qisqartirish va filtrlash (Sample)

## Topshiriq sharti:
Katta oqimdan har K-chi elementni tanlab oluvchi `sample` filtrini yozing.

## Yechim (Dart kodi):
```dart
Iterable<T> sample<T>(Iterable<T> items, int qadam) sync* {
  int i = 0;
  for (var item in items) {
    if (i % qadam == 0) yield item;
    i++;
  }
}

void main() {
  var sekundlar = Iterable<int>.generate(10, (i) => i);
  var namunalar = sample(sekundlar, 3).toList();

  print('Har 3-chi namuna: $namunalar');
}
```

## Tushuntirish va Mantiq:
Signallarni qayta ishlashda va graflarni chizishda haddan ortiq ko'p nuqtalarni kamaytirish (downsampling) uchun qo'llaniladi.

## Ishlash natijasi:
```text
Har 3-chi namuna: [0, 3, 6, 9]
```

# 647-Topshiriq: Bosh harflar bilan so'zlarni sarlavhaga aylantirish (Title Case)

## Topshiriq sharti:
Matndagi har bir so'zning birinchi harfini katta qilib beruvchi funksional transformatsiyani yozing.

## Yechim (Dart kodi):
```dart
String titleCase(String matn) {
  return matn
      .split(' ')
      .where((s) => s.isNotEmpty)
      .map((s) => s[0].toUpperCase() + s.substring(1).toLowerCase())
      .join(' ');
}

void main() {
  print(titleCase('dart dasturlash tili va flutter'));
}
```

## Tushuntirish va Mantiq:
Stringni so'zlarga bo'lib, har birini alohida `map` orqali formatlab qayta yig'ish (join) amalga oshirildi.

## Ishlash natijasi:
```text
Dart Dasturlash Tili Va Flutter
```

# 648-Topshiriq: Funksional yordamida Matnli qidiruv

## Topshiriq sharti:
Kitoblar ro'yxatidan qidiruv so'zi qatnashgan barcha kitoblarni topib konsolga chiqaring.

## Yechim (Dart kodi):
```dart
void main() {
  var kitoblar = [
    'O\'tkan kunlar - Abdulla Qodiriy',
    'Mehrobdan chayon - Abdulla Qodiriy',
    'Kecha va kunduz - Cho\'lpon',
    'Sariq devni minib - Xudoyberdi To\'xtaboyev',
  ];

  String sorov = 'qodiriy';

  var topilganlar = kitoblar
      .where((k) => k.toLowerCase().contains(sorov.toLowerCase()))
      .toList();

  print('Topilgan kitoblar: $topilganlar');
}
```

## Tushuntirish va Mantiq:
Matnli filtratsiyada registrni inobatga olmaslik uchun `toLowerCase()` bilan birga `contains()` ishlatiladi.

## Ishlash natijasi:
```text
Topilgan kitoblar: [O'tkan kunlar - Abdulla Qodiriy, Mehrobdan chayon - Abdulla Qodiriy]
```

# 649-Topshiriq: Softmax funksiyasi funksional Dart usulida

## Topshiriq sharti:
Neyron tarmoq chiqish logits vektorini ehtimolliklarga aylantiruvchi Softmax algoritmini yozing.

## Yechim (Dart kodi):
```dart
import 'dart:math';

List<double> softmax(List<double> logits) {
  double maxLogit = logits.reduce(max); // Sonlar toshib ketmasligi uchun barqarorlashtirish
  var exps = logits.map((x) => exp(x - maxLogit)).toList();
  double sumExp = exps.reduce((a, b) => a + b);
  return exps.map((e) => e / sumExp).toList();
}

void main() {
  List<double> logits = [2.0, 1.0, 0.1];
  var probs = softmax(logits);

  print('Softmax ehtimolliklari:');
  for (var p in probs) {
    print('${(p * 100).toStringAsFixed(1)}%');
  }
}
```

## Tushuntirish va Mantiq:
Softmax barcha qiymatlarni 0 va 1 orasiga tushirib, ularning umumiy yig'indisini 1 (100%) ga tenglashtiradi.

## Ishlash natijasi:
```text
Softmax ehtimolliklari:
65.9%
24.2%
9.9%
```

# 650-Topshiriq: Amaliy: BitNet Tokenlar Oqimi va Qadam-baqam Generatsiya Pipeline

## Topshiriq sharti:
AI til modeli yangi tokenlarni `sync*` generator orqali birma-bir ishlab chiqaruvchi inferensiya oqimini tuzing.

## Yechim (Dart kodi):
```dart
Iterable<String> generateTextStream(String boshPrompt, int maxTokens) sync* {
  var lugat = ['Dart', 'bilan', 'on-device', '1-bit', 'AI', 'tezkor', 'ishlamoqda!'];
  yield boshPrompt;

  for (int i = 0; i < maxTokens; i++) {
    // Model navbatdagi eng ehtimolli tokenni bashorat qiladi
    yield lugat[i % lugat.length];
  }
}

void main() {
  var oqim = generateTextStream('AI:', 6);

  print('Tokenlar generatsiyasi:');
  for (var token in oqim) {
    print('Token: "$token"');
  }
}
```

## Tushuntirish va Mantiq:
LLM matn generatsiyasida (streaming inference) tokenlar bittalab `yield` qilinadi, natijada foydalanuvchi darhol javobni ko'ra boshlaydi.

## Ishlash natijasi:
```text
Tokenlar generatsiyasi:
Token: "AI:"
Token: "Dart"
Token: "bilan"
Token: "on-device"
Token: "1-bit"
Token: "AI"
Token: "tezkor"

```

