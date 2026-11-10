# 751-Topshiriq: Stream asoslari (Stream.fromIterable)

## Topshiriq sharti:
Tayyor ro'yxatdan asinxron ma'lumotlar oqimini (`Stream`) hosil qiling va uni tinglang.

## Yechim (Dart kodi):
```dart
void main() {
  var sonlar = [10, 20, 30];
  Stream<int> oqim = Stream.fromIterable(sonlar);

  oqim.listen((son) {
    print('Oqimdan keldi: $son');
  });
}
```

## Tushuntirish va Mantiq:
`Stream` vaqt o'tishi bilan ketma-ket keladigan asinxron ma'lumotlar manbai bo'lib, `listen()` orqali qabul qilinadi.

## Ishlash natijasi:
```text
Oqimdan keldi: 10
Oqimdan keldi: 20
Oqimdan keldi: 30
```

# 752-Topshiriq: await for sikli bilan oqimni o'qish

## Topshiriq sharti:
`listen` callbacki o'rniga toza asinxron `await for` siklidan foydalaning.

## Yechim (Dart kodi):
```dart
Stream<String> salomlar() async* {
  yield 'Assalomu alaykum';
  yield 'Xush kelibsiz';
  yield 'Dart Streams';
}

void main() async {
  await for (var xabar in salomlar()) {
    print('Qabul qilindi: $xabar');
  }
  print('Oqim to\'liq yakunlandi.');
}
```

## Tushuntirish va Mantiq:
`await for` har bir element kelishini kutib, sinxron sikl kabi ketma-ket qayta ishlashga imkon beradi.

## Ishlash natijasi:
```text
Qabul qilindi: Assalomu alaykum
Qabul qilindi: Xush kelibsiz
Qabul qilindi: Dart Streams
Oqim to'liq yakunlandi.
```

# 753-Topshiriq: StreamSubscription boshqaruvi

## Topshiriq sharti:
`stream.listen` qaytargan `StreamSubscription` obyektidan foydalanib oqimni boshqaring.

## Yechim (Dart kodi):
```dart
void main() {
  var oqim = Stream.fromIterable([1, 2, 3]);

  var sub = oqim.listen(
    (data) => print('Data: $data'),
    onDone: () => print('Barcha ma\'lumotlar kelib bo\'ldi.'),
  );
}
```

## Tushuntirish va Mantiq:
`StreamSubscription` obunani to'xtatish (`cancel`), pauza qilish (`pause`) yoki yakunlanishini (`onDone`) kuzatishga imkon beradi.

## Ishlash natijasi:
```text
Data: 1
Data: 2
Data: 3
Barcha ma'lumotlar kelib bo'ldi.
```

# 754-Topshiriq: Single-subscription stream cheklovi

## Topshiriq sharti:
Oddiy oqimni faqat bitta marta tinglash mumkinligini, ikkinchi urinish xato berishini ko'rsating.

## Yechim (Dart kodi):
```dart
void main() {
  var oqim = Stream.fromIterable(['A', 'B']);

  oqim.listen((e) => print('1-tinglovchi: $e'));

  try {
    oqim.listen((e) => print('2-tinglovchi: $e'));
  } on StateError catch (e) {
    print('Xato: ${e.message}');
  }
}
```

## Tushuntirish va Mantiq:
Standart Stream faqat bitta abonentga mo'ljallangan (single-subscription). Bir nechta abonent uchun broadcast qilish kerak.

## Ishlash natijasi:
```text
1-tinglovchi: A
1-tinglovchi: B
Xato: Stream has already been listened to.
```

# 755-Topshiriq: asBroadcastStream bilan ko'p abonentli oqim

## Topshiriq sharti:
`asBroadcastStream()` orqali bir vaqtning o'zida bir nechta tinglovchilarga ma'lumot tarqating.

## Yechim (Dart kodi):
```dart
void main() {
  var oqim = Stream.fromIterable([100, 200]).asBroadcastStream();

  oqim.listen((val) => print('A tinglovchi: $val'));
  oqim.listen((val) => print('B tinglovchi: $val'));
}
```

## Tushuntirish va Mantiq:
Broadcast Stream ma'lumotni radio to'lqini kabi bir vaqtning o'zida barcha faol obunachilarga yetkazadi.

## Ishlash natijasi:
```text
A tinglovchi: 100
B tinglovchi: 100
A tinglovchi: 200
B tinglovchi: 200
```

# 756-Topshiriq: async* generator funksiyasi va yield

## Topshiriq sharti:
`async*` va `yield` yordamida vaqt oralig'i bilan yangi qiymat ishlab chiqaruvchi oqim tuzing.

## Yechim (Dart kodi):
```dart
Stream<int> sanashOqimi(int max) async* {
  for (int i = 1; i <= max; i++) {
    await Future.delayed(Duration(milliseconds: 5));
    yield i;
  }
}

void main() async {
  await for (var n in sanashOqimi(3)) {
    print('Hosil bo\'lgan son: $n');
  }
}
```

## Tushuntirish va Mantiq:
`async*` asinxron oqim generatori bo'lib, `yield` orqali qiymatlarni bittalab oqimga uzatadi.

## Ishlash natijasi:
```text
Hosil bo'lgan son: 1
Hosil bo'lgan son: 2
Hosil bo'lgan son: 3
```

# 757-Topshiriq: yield* orqali boshqa oqimni ulash

## Topshiriq sharti:
Generator ichida boshqa Stream ni `yield*` yordamida to'liq o'z oqimiga kiritish.

## Yechim (Dart kodi):
```dart
Stream<String> qism1() async* {
  yield 'A';
  yield 'B';
}

Stream<String> umumiyOqim() async* {
  yield 'Bosh';
  yield* qism1();
  yield 'Oxir';
}

void main() async {
  await for (var belgi in umumiyOqim()) {
    print(belgi);
  }
}
```

## Tushuntirish va Mantiq:
`yield*` boshqa oqimdagi barcha elementlarni birma-bir joriy oqimga yo'naltiradi.

## Ishlash natijasi:
```text
Bosh
A
B
Oxir
```

# 758-Topshiriq: StreamController va sink.add orqali ma'lumot uzatish

## Topshiriq sharti:
`StreamController` yaratib, uning `sink` kirishiga ma'lumot qo'shish va `stream` orqali o'qish.

## Yechim (Dart kodi):
```dart
import 'dart:async';

void main() {
  var controller = StreamController<String>();

  controller.stream.listen((xabar) {
    print('Controllerdan olindi: $xabar');
  });

  controller.sink.add('Salom');
  controller.sink.add('Reaktiv Dart');
  controller.close();
}
```

## Tushuntirish va Mantiq:
`StreamController` oqimni to'liq boshqarish vositasi: `sink` unga ma'lumot yuboradi, `stream` esa o'qiydi.

## Ishlash natijasi:
```text
Controllerdan olindi: Salom
Controllerdan olindi: Reaktiv Dart
```

# 759-Topshiriq: StreamController.close() va onDone

## Topshiriq sharti:
Oqim yopilganda abonentlarga xabar yetkazilishini ko'rsating.

## Yechim (Dart kodi):
```dart
import 'dart:async';

void main() {
  var controller = StreamController<int>();

  controller.stream.listen(
    (n) => print('Son: $n'),
    onDone: () => print('Oqim muvaffaqiyatli yopildi!'),
  );

  controller.sink.add(42);
  controller.close();
}
```

## Tushuntirish va Mantiq:
Resurslar oqib ketmasligi (memory leak) uchun barcha controllerlar ish yakunlangach `close()` qilinishi shart.

## Ishlash natijasi:
```text
Son: 42
Oqim muvaffaqiyatli yopildi!
```

# 760-Topshiriq: StreamController.broadcast() bilan ko'p tinglovchi

## Topshiriq sharti:
Bir nechta abonent bir vaqtda tinglashi mumkin bo'lgan broadcast controller tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:async';

void main() {
  var controller = StreamController<String>.broadcast();

  controller.stream.listen((msg) => print('[Tinglovchi 1]: $msg'));
  controller.stream.listen((msg) => print('[Tinglovchi 2]: $msg'));

  controller.sink.add('Yangi yangilik e\'lon qilindi!');
  controller.close();
}
```

## Tushuntirish va Mantiq:
`StreamController.broadcast()` bir nechta UI vidjetlari bir xil ma'lumot oqimini mustaqil tinglashi uchun zarur.

## Ishlash natijasi:
```text
[Tinglovchi 1]: Yangi yangilik e'lon qilindi!
[Tinglovchi 2]: Yangi yangilik e'lon qilindi!
```

# 761-Topshiriq: Stream ustida map() amali

## Topshiriq sharti:
Harorat oqimidagi har bir Celsius qiymatini Fahrenheitga o'zgartiruvchi reaktiv transformatsiya yozing.

## Yechim (Dart kodi):
```dart
void main() async {
  var celsiusOqimi = Stream.fromIterable([0.0, 20.0, 100.0]);

  var fahrenheitOqimi = celsiusOqimi.map((c) => (c * 9 / 5) + 32);

  await for (var f in fahrenheitOqimi) {
    print('Fahrenheit: $f°F');
  }
}
```

## Tushuntirish va Mantiq:
`stream.map()` kelayotgan har bir asinxron hodisani yangi formatga o'zgartirib uzatadi.

## Ishlash natijasi:
```text
Fahrenheit: 32.0°F
Fahrenheit: 68.0°F
Fahrenheit: 212.0°F
```

# 762-Topshiriq: Stream ustida where() amali

## Topshiriq sharti:
Sensor ma'lumotlari oqimidan faqat kritik (50 dan yuqori) qiymatlarni o'tkazuvchi filtr tuzing.

## Yechim (Dart kodi):
```dart
void main() async {
  var sensorOqimi = Stream.fromIterable([22, 45, 68, 30, 85, 49]);

  var xavfliOqim = sensorOqimi.where((harorat) => harorat > 50);

  await for (var h in xavfliOqim) {
    print('DIQQAT: Yuqori harorat: $h°C');
  }
}
```

## Tushuntirish va Mantiq:
`stream.where()` faqat predikatga mos keluvchi asinxron voqealarni o'tkazadi.

## Ishlash natijasi:
```text
DIQQAT: Yuqori harorat: 68°C
DIQQAT: Yuqori harorat: 85°C
```

# 763-Topshiriq: Stream ustida take() va skip()

## Topshiriq sharti:
Oqimning dastlabki 1 ta elementini tashlab yuborib, keyingi 2 tasini oling.

## Yechim (Dart kodi):
```dart
void main() async {
  var oqim = Stream.fromIterable([10, 20, 30, 40, 50]);

  var natija = oqim.skip(1).take(2);

  await for (var n in natija) {
    print('Olingan: $n');
  }
}
```

## Tushuntirish va Mantiq:
`skip` va `take` oqimning faqat kerakli qismini qirqib olish imkonini beradi.

## Ishlash natijasi:
```text
Olingan: 20
Olingan: 30
```

# 764-Topshiriq: Stream ustida distinct() (Dublikatlarni to'xtatish)

## Topshiriq sharti:
Ketma-ket bir xil qiymat qayta-qayta kelganda ularni e'tiborga olmaydigan `distinct()` ni qo'llang.

## Yechim (Dart kodi):
```dart
void main() async {
  var holatlar = Stream.fromIterable(['ON', 'ON', 'OFF', 'OFF', 'ON']);

  var unikal = holatlar.distinct();

  await for (var h in unikal) {
    print('Holat o\'zgardi: $h');
  }
}
```

## Tushuntirish va Mantiq:
`distinct()` oldingi qiymat bilan teng bo'lgan yangi qiymatlarni tashlab yuboradi, faqat o'zgarish bo'lgandagina o'tkazadi.

## Ishlash natijasi:
```text
Holat o'zgardi: ON
Holat o'zgardi: OFF
Holat o'zgardi: ON
```

# 765-Topshiriq: Stream ustida fold() (Oqim yakunida agregatsiya)

## Topshiriq sharti:
Butun oqim tugagach barcha kelgan sonlar yig'indisini hisoblab yagona `Future` qaytaring.

## Yechim (Dart kodi):
```dart
void main() async {
  var savat = Stream.fromIterable([15000, 25000, 40000]);

  int jami = await savat.fold(0, (sum, narx) => sum + narx);
  print('Jami summa: $jami so\'m');
}
```

## Tushuntirish va Mantiq:
`stream.fold()` oqim yopilguniga qadar barcha elementlarni jamlaydi va yakuniy `Future<T>` beradi.

## Ishlash natijasi:
```text
Jami summa: 80000 so'm
```

# 766-Topshiriq: Stream ustida reduce() metodi

## Topshiriq sharti:
Oqimdagi barcha sonlarning maksimal qiymatini `reduce` yordamida aniqlang.

## Yechim (Dart kodi):
```dart
import 'dart:math';

void main() async {
  var sonlar = Stream.fromIterable([14, 88, 32, 99, 45]);

  int engKatta = await sonlar.reduce(max);
  print('Oqimdagi eng katta son: $engKatta');
}
```

## Tushuntirish va Mantiq:
`reduce` oqimdagi birinchi elementdan boshlab qolganlari ustida binar funksiyani qo'llaydi.

## Ishlash natijasi:
```text
Oqimdagi eng katta son: 99
```

# 767-Topshiriq: StreamSubscription.pause() va resume()

## Topshiriq sharti:
Tinglovchini vaqtincha to'xtatib turish va qayta davom ettirish mexanizmini ko'rsating.

## Yechim (Dart kodi):
```dart
import 'dart:async';

void main() {
  var controller = StreamController<int>();

  late StreamSubscription<int> sub;
  sub = controller.stream.listen((val) {
    print('Qabul: $val');
    if (val == 1) {
      print('Tinglovchi pauzaga qo\'yildi...');
      sub.pause();
      Future.delayed(Duration(milliseconds: 10), () {
        print('Tinglovchi davom etmoqda...');
        sub.resume();
      });
    }
  });

  controller.sink.add(1);
  controller.sink.add(2);
  controller.close();
}
```

## Tushuntirish va Mantiq:
`pause()` va `resume()` orqali buferlash va sekin abonentlar yuklamasini (Backpressure) boshqarish mumkin.

## Ishlash natijasi:
```text
Qabul: 1
Tinglovchi pauzaga qo'yildi...
Tinglovchi davom etmoqda...
Qabul: 2
```

# 768-Topshiriq: StreamSubscription.cancel() bilan obunani to'xtatish

## Topshiriq sharti:
Ma'lum shart bajarilganda obunani bekor qilib qolgan voqealarni qabul qilmaslikni ta'minlang.

## Yechim (Dart kodi):
```dart
import 'dart:async';

void main() {
  var controller = StreamController<int>();

  late StreamSubscription<int> sub;
  sub = controller.stream.listen((val) {
    print('Qabul: $val');
    if (val == 2) {
      print('Obuna bekor qilindi!');
      sub.cancel();
    }
  });

  controller.sink.add(1);
  controller.sink.add(2);
  controller.sink.add(3); // Qabul qilinmaydi
  controller.close();
}
```

## Tushuntirish va Mantiq:
`cancel()` chaqirilgach tinglovchi o'chiriladi va keyingi hodisalar unga yetib bormaydi.

## Ishlash natijasi:
```text
Qabul: 1
Qabul: 2
Obuna bekor qilindi!
```

# 769-Topshiriq: Stream.periodic davriy voqealar generatori

## Topshiriq sharti:
Har belgilangan millisekundda inkrement qiymat beruvchi `Stream.periodic` tuzing.

## Yechim (Dart kodi):
```dart
void main() async {
  var davriy = Stream.periodic(
    Duration(milliseconds: 10),
    (sanoq) => 'Taqqillash #$sanoq',
  ).take(3);

  await for (var t in davriy) {
    print(t);
  }
}
```

## Tushuntirish va Mantiq:
`Stream.periodic` taymer kabi belgilangan vaqt oralig'ida muntazam hodisalar ishlab chiqaradi.

## Ishlash natijasi:
```text
Taqqillash #0
Taqqillash #1
Taqqillash #2
```

# 770-Topshiriq: Stream.empty va Stream.error

## Topshiriq sharti:
Bo'sh yoki darhol xatolik chiqaruvchi maxsus oqimlarni yaratishni ko'rsating.

## Yechim (Dart kodi):
```dart
void main() async {
  var boshOqim = Stream<int>.empty();
  var elementlar = await boshOqim.toList();
  print('Bo\'sh oqim elementlari: $elementlar');

  var xatoOqim = Stream<int>.error('Xavfli nosozlik');
  xatoOqim.listen(
    (_) {},
    onError: (err) => print('Oqimdan xato olindi: $err'),
  );
}
```

## Tushuntirish va Mantiq:
Standart `Stream.empty()` va `Stream.error()` testlarda va zaxira holatlarda juda qo'l keladi.

## Ishlash natijasi:
```text
Bo'sh oqim elementlari: []
Oqimdan xato olindi: Xavfli nosozlik
```

# 771-Topshiriq: StreamTransformer yaratish (fromHandlers)

## Topshiriq sharti:
Kiruvchi oqimdagi harflarni kattalashtirib beruvchi maxsus `StreamTransformer` tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:async';

void main() async {
  var transformer = StreamTransformer<String, String>.fromHandlers(
    handleData: (matn, sink) {
      sink.add('*** ${matn.toUpperCase()} ***');
    },
  );

  var oqim = Stream.fromIterable(['dart', 'flutter']).transform(transformer);

  await for (var s in oqim) {
    print(s);
  }
}
```

## Tushuntirish va Mantiq:
`StreamTransformer` oqimni qayta ishlovchi murakkab filtrlarni alohida mustaqil modul sifatida yaratish imkonini beradi.

## Ishlash natijasi:
```text
*** DART ***
*** FLUTTER ***
```

# 772-Topshiriq: Stream xatolarini boshqarish (onError va handleError)

## Topshiriq sharti:
Oqim ichida yuz bergan xatolikni ushlab, uning ortidan kelayotgan ma'lumotlarni qabul qilishni davom ettiring.

## Yechim (Dart kodi):
```dart
Stream<int> xatoli() async* {
  yield 1;
  throw FormatException('Xato format');
}

void main() {
  xatoli().listen(
    (n) => print('Data: $n'),
    onError: (e) => print('Ushlangan xato: $e'),
  );
}
```

## Tushuntirish va Mantiq:
`listen` ichidagi `onError` callbacki oqim buzilishini xavfsiz ushlab qoladi.

## Ishlash natijasi:
```text
Data: 1
Ushlangan xato: FormatException: Xato format
```

# 773-Topshiriq: BLoC (Business Logic Component) naqshi asoslari

## Topshiriq sharti:
Hisoblagich (CounterBloc) holatini `StreamController` yordamida to'liq ajratilgan holda boshqaring.

## Yechim (Dart kodi):
```dart
import 'dart:async';

class CounterBloc {
  int _count = 0;
  final _stateController = StreamController<int>.broadcast();

  Stream<int> get state => _stateController.stream;

  void increment() {
    _count++;
    _stateController.sink.add(_count);
  }

  void dispose() => _stateController.close();
}

void main() {
  var bloc = CounterBloc();
  bloc.state.listen((count) => print('Yangi hisob: $count'));

  bloc.increment();
  bloc.increment();
  bloc.dispose();
}
```

## Tushuntirish va Mantiq:
BLoC naqshi Flutterda UI va biznes mantiqni to'liq reaktiv Streamlar orqali ajratadi.

## Ishlash natijasi:
```text
Yangi hisob: 1
Yangi hisob: 2
```

# 774-Topshiriq: Reaktiv Qidiruv oqimi (SearchBloc)

## Topshiriq sharti:
Foydalanuvchi qidiruv so'zini kiritganda filtr natijalarini oqim orqali taqdim etuvchi BLoC tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:async';

class SearchBloc {
  final List<String> _katalog = ['Dart', 'Flutter', 'Firebase', 'BitNet'];
  final _searchController = StreamController<String>();
  final _resultController = StreamController<List<String>>.broadcast();

  Stream<List<String>> get results => _resultController.stream;

  SearchBloc() {
    _searchController.stream.listen((query) {
      var filtered = _katalog
          .where((item) => item.toLowerCase().contains(query.toLowerCase()))
          .toList();
      _resultController.sink.add(filtered);
    });
  }

  void search(String q) => _searchController.sink.add(q);

  void dispose() {
    _searchController.close();
    _resultController.close();
  }
}

void main() {
  var bloc = SearchBloc();
  bloc.results.listen((res) => print('Qidiruv natijasi: $res'));

  bloc.search('f');
  bloc.dispose();
}
```

## Tushuntirish va Mantiq:
Kiruvchi qidiruv so'zlari va chiquvchi natijalar mustaqil oqimlar orqali bog'lanadi.

## Ishlash natijasi:
```text
Qidiruv natijasi: [Flutter, Firebase]
```

# 775-Topshiriq: Amaliy: BitNet Token Generator Stream

## Topshiriq sharti:
1-bit AI model matn generatsiyasida har bir yangi tokenni real vaqt rejimida `Stream<String>` orqali uzatuvchi generator yozing.

## Yechim (Dart kodi):
```dart
Stream<String> streamBitNetTokens(String prompt) async* {
  var tokens = ['BitNet', 'b1.58', 'modeli', 'mobil', 'qurilmada', 'muvaffaqiyatli', 'ishlamoqda!'];

  for (var token in tokens) {
    await Future.delayed(Duration(milliseconds: 10)); // AI qadam inferensiyasi
    yield '$token ';
  }
}

void main() async {
  print('AI Javob bermoqda:');
  await for (var token in streamBitNetTokens('Salom')) {
    // Real vaqtda bittalab chop etish
    print(token.trim());
  }
}
```

## Tushuntirish va Mantiq:
ChatGPT va zamonaviy LLM ilovalarida 'typewriter effect' (yozuv mashinkasi effekti) aynan `Stream` orqali ta'minlanadi.

## Ishlash natijasi:
```text
AI Javob bermoqda:
BitNet
b1.58
modeli
mobil
qurilmada
muvaffaqiyatli
ishlamoqda!
```

# 776-Topshiriq: Streamlarni birlashtirish (Merge amali)

## Topshiriq sharti:
Ikkita turli manbadan kelayotgan oqimlarni bitta umumiy oqimga aralashtirib yuboring.

## Yechim (Dart kodi):
```dart
import 'dart:async';

Stream<T> mergeStreams<T>(Stream<T> s1, Stream<T> s2) {
  var controller = StreamController<T>();
  int tugaganlar = 0;

  void tekshirTugash() {
    tugaganlar++;
    if (tugaganlar == 2) controller.close();
  }

  s1.listen(controller.add, onError: controller.addError, onDone: tekshirTugash);
  s2.listen(controller.add, onError: controller.addError, onDone: tekshirTugash);

  return controller.stream;
}

void main() async {
  var oqim1 = Stream.fromIterable(['A1', 'A2']);
  var oqim2 = Stream.fromIterable(['B1', 'B2']);

  await for (var item in mergeStreams(oqim1, oqim2)) {
    print('Merge: $item');
  }
}
```

## Tushuntirish va Mantiq:
Merge operatsiyasi ikkala oqimning hodisalarini kelish tartibida bitta umumiy oqimga yo'naltiradi.

## Ishlash natijasi:
```text
Merge: A1
Merge: B1
Merge: A2
Merge: B2
```

# 777-Topshiriq: Streamlarni parallel juftlash (Stream Zip)

## Topshiriq sharti:
Ikkita oqimning mos elementlarini juft-juft qilib birlashtiruvchi operatsiyani yozing.

## Yechim (Dart kodi):
```dart
import 'dart:async';

Stream<(A, B)> zipStreams<A, B>(Stream<A> s1, Stream<B> s2) async* {
  var it1 = StreamIterator(s1);
  var it2 = StreamIterator(s2);

  while (await it1.moveNext() && await it2.moveNext()) {
    yield (it1.current, it2.current);
  }
}

void main() async {
  var ismlar = Stream.fromIterable(['Ali', 'Vali']);
  var yoshlar = Stream.fromIterable([20, 25]);

  await for (var (ism, yosh) in zipStreams(ismlar, yoshlar)) {
    print('$ism: $yosh yoshda');
  }
}
```

## Tushuntirish va Mantiq:
`StreamIterator` yordamida ikkala oqimni elementma-element sinxron harakatlantirib juftliklar hosil qilinadi.

## Ishlash natijasi:
```text
Ali: 20 yoshda
Vali: 25 yoshda
```

# 778-Topshiriq: CombineLatest naqshi (Eng so'nggi qiymatlarni birlashtirish)

## Topshiriq sharti:
Ikkala oqimning har doim eng oxirgi qiymatlarini birlashtirib turuvchi reaktiv naqsh tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:async';

class CombineLatest2<A, B> {
  A? _oxirgiA;
  B? _oxirgiB;
  final _controller = StreamController<(A, B)>.broadcast();

  Stream<(A, B)> get stream => _controller.stream;

  CombineLatest2(Stream<A> s1, Stream<B> s2) {
    s1.listen((a) {
      _oxirgiA = a;
      _emit();
    });
    s2.listen((b) {
      _oxirgiB = b;
      _emit();
    });
  }

  void _emit() {
    if (_oxirgiA != null && _oxirgiB != null) {
      _controller.add((_oxirgiA as A, _oxirgiB as B));
    }
  }
}

void main() async {
  var sA = StreamController<String>();
  var sB = StreamController<int>();

  var combo = CombineLatest2(sA.stream, sB.stream);
  combo.stream.listen((juft) => print('Yangi kombinatsiya: $juft'));

  sA.add('X');
  sB.add(1);
  sA.add('Y');
}
```

## Tushuntirish va Mantiq:
CombineLatest login va parol maydonlari to'g'riligiga qarab 'Kirish' tugmasini faollashtirishda eng ko'p ishlatiladi.

## Ishlash natijasi:
```text
Yangi kombinatsiya: (X, 1)
Yangi kombinatsiya: (Y, 1)
```

# 779-Topshiriq: BehaviorSubject naqshi (Oxirgi qiymatni keshlovchi oqim)

## Topshiriq sharti:
Yangi obunachi qo'shilganda unga zudlik bilan eng oxirgi mavjud qiymatni beruvchi sinf tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:async';

class BehaviorSubject<T> {
  T _value;
  final _controller = StreamController<T>.broadcast();

  BehaviorSubject(this._value);

  T get value => _value;

  Stream<T> get stream async* {
    yield _value; // Yangi obunachiga darhol oxirgi qiymat
    yield* _controller.stream;
  }

  void add(T newValue) {
    _value = newValue;
    _controller.add(newValue);
  }
}

void main() async {
  var mavzu = BehaviorSubject<int>(10);
  mavzu.add(20);

  // Yangi tinglovchi ulanmoqda:
  mavzu.stream.listen((val) => print('Tinglovchi oldi: $val'));
}
```

## Tushuntirish va Mantiq:
RxDart dagi `BehaviorSubject` kabi ushbu naqsh UI qayta chizilganda ham so'nggi holatni saqlab qoladi.

## Ishlash natijasi:
```text
Tinglovchi oldi: 20
```

# 780-Topshiriq: ReplaySubject naqshi (Tarixni qayta o'ynatuvchi oqim)

## Topshiriq sharti:
Yangi tinglovchiga oldingi barcha o'tgan voqealar tarixini qayta eshittiruvchi oqim tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:async';

class ReplaySubject<T> {
  final List<T> _tarix = [];
  final _controller = StreamController<T>.broadcast();

  Stream<T> get stream async* {
    for (var e in _tarix) yield e; // Tarixni berish
    yield* _controller.stream;
  }

  void add(T item) {
    _tarix.add(item);
    _controller.add(item);
  }
}

void main() async {
  var rep = ReplaySubject<String>();
  rep.add('Xabar 1');
  rep.add('Xabar 2');

  // Kechroq obuna bo'lish:
  await for (var msg in rep.stream.take(2)) {
    print('Tarixdan qabul qilindi: $msg');
  }
}
```

## Tushuntirish va Mantiq:
ReplaySubject chat tarixini yoki o'tgan bildirishnomalarni yangi kirgan foydalanuvchiga to'liq ko'rsatishda qo'llanadi.

## Ishlash natijasi:
```text
Tarixdan qabul qilindi: Xabar 1
Tarixdan qabul qilindi: Xabar 2
```

# 781-Topshiriq: Stream DebounceTime transformatori

## Topshiriq sharti:
Oqimdagi qiymatlar orasida belgilangan vaqt tinchlik bo'lgandagina qiymatni o'tkazuvchi filtr tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:async';

Stream<T> debounceStream<T>(Stream<T> stream, Duration duration) {
  var controller = StreamController<T>();
  Timer? timer;

  stream.listen((data) {
    timer?.cancel();
    timer = Timer(duration, () => controller.add(data));
  }, onDone: () {
    timer?.cancel();
    controller.close();
  });

  return controller.stream;
}

void main() async {
  var c = StreamController<String>();
  var debounced = debounceStream(c.stream, Duration(milliseconds: 20));

  debounced.listen((data) => print('Debounced natija: $data'));

  c.add('A');
  c.add('B');
  c.add('C'); // Faqat C o'tadi
  await Future.delayed(Duration(milliseconds: 40));
  c.close();
}
```

## Tushuntirish va Mantiq:
Debounce qidiruv satridagi tinimsiz o'zgarishlarni bitta yakuniy so'rovga aylantiradi.

## Ishlash natijasi:
```text
Debounced natija: C
```

# 782-Topshiriq: Stream ThrottleTime transformatori

## Topshiriq sharti:
Birinchi element kelishi bilan uni o'tkazib, keyingi N vaqt ichidagilarini bloklovchi filtr tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:async';

Stream<T> throttleStream<T>(Stream<T> stream, Duration duration) {
  var controller = StreamController<T>();
  bool blok = false;

  stream.listen((data) {
    if (!blok) {
      controller.add(data);
      blok = true;
      Timer(duration, () => blok = false);
    }
  }, onDone: controller.close);

  return controller.stream;
}

void main() async {
  var c = StreamController<int>();
  var throttled = throttleStream(c.stream, Duration(milliseconds: 50));

  throttled.listen((n) => print('Throttled: $n'));

  c.add(1); // O'tadi
  c.add(2); // Blok
  c.add(3); // Blok
  await Future.delayed(Duration(milliseconds: 60));
  c.close();
}
```

## Tushuntirish va Mantiq:
Throttle o'yinlar va sensorlarda sekundiga yuzlab keladigan voqealarni cheklab turadi.

## Ishlash natijasi:
```text
Throttled: 1
```

# 783-Topshiriq: Stream BufferCount (Paketlash)

## Topshiriq sharti:
Elementlarni bittalab emas, har N tadan guruhlab (List) chiqaruvchi transformatsiya yozing.

## Yechim (Dart kodi):
```dart
import 'dart:async';

Stream<List<T>> bufferCount<T>(Stream<T> stream, int count) async* {
  List<T> bufer = [];
  await for (var item in stream) {
    bufer.add(item);
    if (bufer.length == count) {
      yield List.from(bufer);
      bufer.clear();
    }
  }
  if (bufer.isNotEmpty) yield bufer;
}

void main() async {
  var oqim = Stream.fromIterable([1, 2, 3, 4, 5]);
  await for (var paket in bufferCount(oqim, 2)) {
    print('Paket: $paket');
  }
}
```

## Tushuntirish va Mantiq:
`bufferCount` ma'lumotlarni guruhlab jo'natish yoki ekranga 2 ustun qilib joylashtirishda qo'llaniladi.

## Ishlash natijasi:
```text
Paket: [1, 2]
Paket: [3, 4]
Paket: [5]
```

# 784-Topshiriq: Stream BufferTime (Vaqt bo'yicha buferlash)

## Topshiriq sharti:
Har N millisekund ichida to'plangan barcha voqealarni ro'yxat qilib chiqaruvchi oqim tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:async';

Stream<List<T>> bufferTime<T>(Stream<T> stream, Duration duration) {
  var controller = StreamController<List<T>>();
  List<T> bufer = [];

  var timer = Timer.periodic(duration, (_) {
    if (bufer.isNotEmpty) {
      controller.add(List.from(bufer));
      bufer.clear();
    }
  });

  stream.listen(bufer.add, onDone: () {
    timer.cancel();
    if (bufer.isNotEmpty) controller.add(bufer);
    controller.close();
  });

  return controller.stream;
}

void main() async {
  var c = StreamController<String>();
  var buffered = bufferTime(c.stream, Duration(milliseconds: 20));

  buffered.listen((paket) => print('Vaqt paketi: $paket'));

  c.add('xabar 1');
  c.add('xabar 2');
  await Future.delayed(Duration(milliseconds: 30));
  c.close();
}
```

## Tushuntirish va Mantiq:
Vaqt bo'yicha buferlash chat xabarlarini yoki tarmoq paketlarini to'plab yuborishda ishlatiladi.

## Ishlash natijasi:
```text
Vaqt paketi: [xabar 1, xabar 2]
```

# 785-Topshiriq: Stream SwitchMap naqshi (Eskisini bekor qilib yangisiga o'tish)

## Topshiriq sharti:
Yangi qidiruv so'zi kelganda oldingi qidiruv so'rovini to'xtatib eng so'nggisini tinglovchi naqsh tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:async';

class SwitchMapMisol {
  StreamSubscription? _sub;
  final _chiqish = StreamController<String>();

  Stream<String> get stream => _chiqish.stream;

  void yangiSorov(String sorov) {
    _sub?.cancel(); // Eskisini bekor qilish
    var yangiOqim = Stream.value('Natija: $sorov');
    _sub = yangiOqim.listen(_chiqish.add);
  }
}

void main() {
  var sm = SwitchMapMisol();
  sm.stream.listen(print);

  sm.yangiSorov('Dart');
  sm.yangiSorov('Flutter'); // Faqat so'nggisi ishlaydi
}
```

## Tushuntirish va Mantiq:
SwitchMap eskirgan asinxron so'rovlarning kechikib kelib yangi ma'lumotlarni buzishining oldini oladi.

## Ishlash natijasi:
```text
Natija: Flutter
```

# 786-Topshiriq: WebSocket ma'lumotlar oqimi simulyatsiyasi

## Topshiriq sharti:
Real vaqtda ikki tomonlama aloqa qiluvchi Stream simulyatsiyasini yozing.

## Yechim (Dart kodi):
```dart
import 'dart:async';

class WebSocketSimulyator {
  final _kirish = StreamController<String>();
  final _chiqish = StreamController<String>();

  Stream<String> get xabarlar => _chiqish.stream;

  void yuborish(String msg) {
    print('[WS MIJOZ YUBORDI]: $msg');
    // Server javobi simulyatsiyasi
    _chiqish.add('Server tasdiqladi: $msg');
  }

  void yopish() {
    _kirish.close();
    _chiqish.close();
  }
}

void main() {
  var ws = WebSocketSimulyator();
  ws.xabarlar.listen((msg) => print('[WS QABUL QILINDI]: $msg'));

  ws.yuborish('Ping');
  ws.yopish();
}
```

## Tushuntirish va Mantiq:
WebSocket aloqasi Dartda to'liq `Stream` (qabul qilish) va `StreamSink` (yuborish) orqali boshqariladi.

## Ishlash natijasi:
```text
[WS MIJOZ YUBORDI]: Ping
[WS QABUL QILINDI]: Server tasdiqladi: Ping
```

# 787-Topshiriq: Sensor oqimini tekislovchi filtr (Low-pass filter)

## Topshiriq sharti:
Shovqinli sensor o'lchovlarini eksponentsial harakatlanuvchi o'rtacha bilan tekislovchi oqim transformatsiyasini tuzing.

## Yechim (Dart kodi):
```dart
Stream<double> lowPassFilter(Stream<double> input, double alpha) async* {
  double? prev;
  await for (var val in input) {
    if (prev == null) {
      prev = val;
    } else {
      prev = alpha * val + (1 - alpha) * prev;
    }
    yield prev;
  }
}

void main() async {
  var shovqinli = Stream.fromIterable([10.0, 50.0, 12.0, 15.0]);
  var tekislangan = lowPassFilter(shovqinli, 0.3);

  await for (var val in tekislangan) {
    print('Tekislangan qiymat: ${val.toStringAsFixed(1)}');
  }
}
```

## Tushuntirish va Mantiq:
Low-pass filtr birdan sakragan shovqinlarni silliqlab, haqiqiy jismoniy harakatni aniq ifodalaydi.

## Ishlash natijasi:
```text
Tekislangan qiymat: 10.0
Tekislangan qiymat: 22.0
Tekislangan qiymat: 19.0
Tekislangan qiymat: 17.8
```

# 788-Topshiriq: UI tugma bosishlarini oqim orqali boshqarish

## Topshiriq sharti:
Tugma bosilishlarini `StreamController` orqali qabul qilib, jami bosishlar sonini hisoblang.

## Yechim (Dart kodi):
```dart
import 'dart:async';

class Tugma {
  final _bosishController = StreamController<void>.broadcast();
  Stream<void> get onBosildi => _bosishController.stream;

  void bosish() => _bosishController.add(null);
}

void main() {
  var btn = Tugma();
  int count = 0;
  btn.onBosildi.listen((_) {
    count++;
    print('Tugma bosildi! Jami: $count');
  });

  btn.bosish();
  btn.bosish();
}
```

## Tushuntirish va Mantiq:
Flutter va boshqa UI freymvorklarda hodisalar oqim (Event Stream) ko'rinishida tarqatiladi.

## Ishlash natijasi:
```text
Tugma bosildi! Jami: 1
Tugma bosildi! Jami: 2
```

# 789-Topshiriq: Progress Tracker Stream (0% dan 100% gacha)

## Topshiriq sharti:
Fayl yuklanish jarayonini foizlar ko'rinishida uzatuvchi progress oqimi tuzing.

## Yechim (Dart kodi):
```dart
Stream<int> faylYuklashJarayoni() async* {
  for (int foiz = 0; foiz <= 100; foiz += 25) {
    await Future.delayed(Duration(milliseconds: 5));
    yield foiz;
  }
}

void main() async {
  await for (var p in faylYuklashJarayoni()) {
    print('Yuklanish holati: $p%');
  }
}
```

## Tushuntirish va Mantiq:
Progress oqimi fayl yuklash yoki katta AI modellarini diskdan xotiraga o'qish jarayonini foydalanuvchiga ko'rsatishda qo'llanadi.

## Ishlash natijasi:
```text
Yuklanish holati: 0%
Yuklanish holati: 25%
Yuklanish holati: 50%
Yuklanish holati: 75%
Yuklanish holati: 100%
```

# 790-Topshiriq: Bildirishnomalar markazi (Notification Center)

## Topshiriq sharti:
Butun tizim bo'ylab bildirishnomalarni tarqatuvchi markazlashgan reaktiv markaz tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:async';

class BildirishnomaMarkazi {
  static final _oqim = StreamController<String>.broadcast();
  static Stream<String> get bildirishnomalar => _oqim.stream;

  static void yuborish(String xabar) => _oqim.add(xabar);
}

void main() {
  BildirishnomaMarkazi.bildirishnomalar.listen((msg) {
    print('[BILDIRISHNOMA]: $msg');
  });

  BildirishnomaMarkazi.yuborish('Yangi xabar keldi');
}
```

## Tushuntirish va Mantiq:
Statik broadcast stream butun ilova bo'ylab global xabarlarni istalgan ekranga yetkazadi.

## Ishlash natijasi:
```text
[BILDIRISHNOMA]: Yangi xabar keldi
```

# 791-Topshiriq: Ko'p foydalanuvchili Chat xonasi StreamController bilan

## Topshiriq sharti:
Foydalanuvchi ismi va xabar matnini barcha ishtirokchilarga yetkazuvchi Chat xonasini tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:async';

class ChatXonasi {
  final _controller = StreamController<String>.broadcast();

  Stream<String> get xabarlar => _controller.stream;

  void yozish(String foydalanuvchi, String matn) {
    _controller.add('$foydalanuvchi: $matn');
  }
}

void main() {
  var chat = ChatXonasi();

  chat.xabarlar.listen((xabar) => print('[Ekran]: $xabar'));

  chat.yozish('Jasur', 'Salom barchaga!');
  chat.yozish('Madina', 'Salom Jasur!');
}
```

## Tushuntirish va Mantiq:
Chat ilovalari bir nechta foydalanuvchi kirishlarini yagona broadcast oqim orqali aks ettiradi.

## Ishlash natijasi:
```text
[Ekran]: Jasur: Salom barchaga!
[Ekran]: Madina: Salom Jasur!
```

# 792-Topshiriq: Faylni baytma-bayt o'qish simulyatsiyasi (Chunk Stream)

## Topshiriq sharti:
Katta faylni kichik baytlar bloklariga bo'lib oqimda uzatuvchi generator yozing.

## Yechim (Dart kodi):
```dart
Stream<List<int>> oqimliFaylOqish() async* {
  yield [0x44, 0x61, 0x72, 0x74]; // 'Dart' baytlari
  yield [0x20, 0x33, 0x2E, 0x30]; // ' 3.0' baytlari
}

void main() async {
  await for (var chunk in oqimliFaylOqish()) {
    print('Blok olindi: ${chunk.length} bayt -> $chunk');
  }
}
```

## Tushuntirish va Mantiq:
Katta fayllar (videolar, AI vaznlari) xotirani to'ldirmasligi uchun oqim orqali qismlab (chunk) o'qiladi.

## Ishlash natijasi:
```text
Blok olindi: 4 bayt -> [68, 97, 114, 116]
Blok olindi: 4 bayt -> [32, 51, 46, 48]
```

# 793-Topshiriq: Audio oqimi va Ekvalayzer simulyatsiyasi

## Topshiriq sharti:
Audio chastota ma'lumotlarini qabul qilib, o'rtacha desibel darajasini ko'rsatuvchi reaktiv pleyer tuzing.

## Yechim (Dart kodi):
```dart
Stream<int> audioChastotalar() async* {
  yield 30;
  yield 65;
  yield 85;
}

void main() async {
  await for (var db in audioChastotalar()) {
    String bar = '=' * (db ~/ 10);
    print('[$db dB] $bar');
  }
}
```

## Tushuntirish va Mantiq:
Oqimlar audio signallarni real vaqtda qayta ishlash va vizualizatsiya qilish uchun idealdir.

## Ishlash natijasi:
```text
[30 dB] ===
[65 dB] ======
[85 dB] ========
```

# 794-Topshiriq: Reaktiv Hamyon balansi va tranzaksiyalar

## Topshiriq sharti:
Pul kirimi yoki chiqimi bo'lganda yangi balansni oqim orqali avtomatik e'lon qiluvchi hamyon tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:async';

class ReaktivHamyon {
  double _balans = 0;
  final _balansController = StreamController<double>.broadcast();

  Stream<double> get balansStream => _balansController.stream;

  void depozit(double summa) {
    _balans += summa;
    _balansController.add(_balans);
  }
}

void main() {
  var h = ReaktivHamyon();
  h.balansStream.listen((b) => print('Yangi balans: ${b.toStringAsFixed(0)} so\'m'));

  h.depozit(50000);
  h.depozit(25000);
}
```

## Tushuntirish va Mantiq:
Reaktiv hamyon tranzaksiya sodir bo'lishi bilan unga bog'liq barcha interfeyslarni avtomatik yangilaydi.

## Ishlash natijasi:
```text
Yangi balans: 50000 so'm
Yangi balans: 75000 so'm
```

# 795-Topshiriq: Birja narxlari monitoringi (Stock Ticker Stream)

## Topshiriq sharti:
Aksiya narxlari o'zgarishini muntazam yangilab turuvchi reaktiv birja simulyatorini yozing.

## Yechim (Dart kodi):
```dart
Stream<(String, double)> birjaNarxlari() async* {
  yield ('UZB_AI', 150.0);
  yield ('UZB_AI', 154.5);
  yield ('UZB_AI', 152.0);
}

void main() async {
  await for (var (belgi, narx) in birjaNarxlari()) {
    print('Ticker: $belgi -> \$$narx');
  }
}
```

## Tushuntirish va Mantiq:
Birja va moliya bozorlaridagi yuqori chastotali ma'lumotlar oqimlar orqali qayta ishlanadi.

## Ishlash natijasi:
```text
Ticker: UZB_AI -> \$150.0
Ticker: UZB_AI -> \$154.5
Ticker: UZB_AI -> \$152.0
```

# 796-Topshiriq: GPS Treking oqimi (Marshrut nuqtalari)

## Topshiriq sharti:
Harakatlanayotgan avtomobil koordinatalarini oqimda qabul qilib bosib o'tilgan yo'lni ko'rsating.

## Yechim (Dart kodi):
```dart
Stream<(double, double)> gpsOqimi() async* {
  yield (41.2995, 69.2401); // Toshkent
  yield (41.3050, 69.2450);
  yield (41.3100, 69.2500);
}

void main() async {
  await for (var (lat, lon) in gpsOqimi()) {
    print('GPS koordinata: lat=$lat, lon=$lon');
  }
}
```

## Tushuntirish va Mantiq:
Xaritalar va yetkazib berish ilovalarida haydovchi joylashuvi GPS oqimi orqali real vaqtda chiziladi.

## Ishlash natijasi:
```text
GPS koordinata: lat=41.2995, lon=69.2401
GPS koordinata: lat=41.305, lon=69.245
GPS koordinata: lat=41.31, lon=69.25
```

# 797-Topshiriq: Batareya quvvati o'zgarishini kuzatish

## Topshiriq sharti:
Qurilma zaryadi kamayib borishini kuzatib, 20% dan tushganda ogohlantiruvchi oqim yozing.

## Yechim (Dart kodi):
```dart
Stream<int> batareyaOqimi() async* {
  yield 25;
  yield 20;
  yield 15;
}

void main() async {
  await for (var foiz in batareyaOqimi()) {
    if (foiz <= 20) {
      print('Ogohlantirish: Zaryad $foiz%! Quvvatlash rejimiga o\'ting.');
    } else {
      print('Batareya: $foiz%');
    }
  }
}
```

## Tushuntirish va Mantiq:
Tizim hodisalarini oqim orqali kuzatish apparat holatini doimiy monitoring qilish imkonini beradi.

## Ishlash natijasi:
```text
Batareya: 25%
Ogohlantirish: Zaryad 20%! Quvvatlash rejimiga o'ting.
Ogohlantirish: Zaryad 15%! Quvvatlash rejimiga o'ting.
```

# 798-Topshiriq: Loglarni masofaviy serverga oqimli uzatish

## Topshiriq sharti:
Ilova loglarini to'plamasdan kelishi bilanoq oqim orqali masofaviy serverga yo'naltiring.

## Yechim (Dart kodi):
```dart
import 'dart:async';

void main() {
  var logStream = StreamController<String>();

  logStream.stream.listen((log) {
    print('[REMOTE SERVERGA YUBORILDI]: $log');
  });

  logStream.add('Foydalanuvchi kirish tugmasini bosdi');
  logStream.close();
}
```

## Tushuntirish va Mantiq:
Oqimli log uzatish ilova halokatga uchragan taqdirda ham eng oxirgi hodisalar yo'qolmasligini ta'minlaydi.

## Ishlash natijasi:
```text
[REMOTE SERVERGA YUBORILDI]: Foydalanuvchi kirish tugmasini bosdi
```

# 799-Topshiriq: AI so'rovini bekor qilish (Cancel Streaming Inference)

## Topshiriq sharti:
Foydalanuvchi 'To'xtatish' tugmasini bosganda AI tokenlar oqimini zudlik bilan uzuvchi mexanizm tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:async';

Stream<String> aiModelStream() async* {
  var tokens = ['Bir', 'Ikki', 'Uch', 'To\'rt'];
  for (var t in tokens) {
    await Future.delayed(Duration(milliseconds: 10));
    yield t;
  }
}

void main() async {
  late StreamSubscription sub;
  int sanoq = 0;

  sub = aiModelStream().listen((token) {
    print('Token: $token');
    sanoq++;
    if (sanoq == 2) {
      print('Foydalanuvchi generatsiyani to\'xtatdi!');
      sub.cancel();
    }
  });

  await Future.delayed(Duration(milliseconds: 50));
}
```

## Tushuntirish va Mantiq:
Obunani `sub.cancel()` qilish AI modelining ortiqcha tokenlar ishlab chiqarib quvvat sarflashini oldini oladi.

## Ishlash natijasi:
```text
Token: Bir
Token: Ikki
Foydalanuvchi generatsiyani to'xtatdi!
```

# 800-Topshiriq: Amaliy: BitNet Full Streaming Engine va Tezlik Hisoblagich

## Topshiriq sharti:
Prompt qabul qilib, tokenlarni oqimda chiqaruvchi va so'ngida sekundiga qancha token chiqarilganini hisoblovchi to'liq AI dvigatelini tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:async';

class BitNetStreamingEngine {
  Stream<String> generate(String prompt) async* {
    var tokens = [
      'O\'zbekiston', 'sun\'iy', 'intellekt', 'sohasida',
      'BitNet', '1-bit', 'texnologiyasini', 'joriy', 'qilmoqda!'
    ];

    for (var token in tokens) {
      await Future.delayed(Duration(milliseconds: 5));
      yield token;
    }
  }
}

void main() async {
  var engine = BitNetStreamingEngine();
  var sw = Stopwatch()..start();
  int tokenCount = 0;

  print('Prompt: "AI taraqqiyoti"
---');
  await for (var token in engine.generate('AI taraqqiyoti')) {
    print(token);
    tokenCount++;
  }
  sw.stop();

  double seconds = sw.elapsedMilliseconds / 1000.0;
  if (seconds == 0) seconds = 0.05;
  double tokensPerSec = tokenCount / seconds;

  print('---
Jami tokenlar: $tokenCount');
  print('Generatsiya tezligi: ${tokensPerSec.toStringAsFixed(1)} token/soniya');
}
```

## Tushuntirish va Mantiq:
On-device 1-bit LLM dvigateli matnni oqim ko'rinishida uzatadi va inferensiya tezligi (tok/sec) real vaqtda o'lchanadi.

## Ishlash natijasi:
```text
Prompt: "AI taraqqiyoti"
---
O'zbekiston
sun'iy
intellekt
sohasida
BitNet
1-bit
texnologiyasini
joriy
qilmoqda!
---
Jami tokenlar: 9
Generatsiya tezligi: 180.0 token/soniya
```

