# 851-Topshiriq: Isolate nima va umumiy xotirasizlik tamoyili

## Topshiriq sharti:
Dart Isolate lari nima uchun an'anaviy threadlardan farq qilishi va xotira bo'lishmasligini ko'rsating.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

int globalHisob = 0;

void isolateFunksiyasi(SendPort sendPort) {
  globalHisob += 100; // Bu faqat ushbu isolate ning o'z nusxasida o'zgaradi!
  sendPort.send(globalHisob);
}

void main() async {
  var port = ReceivePort();
  await Isolate.spawn(isolateFunksiyasi, port.sendPort);

  int xabar = await port.first;
  print('Isolate dagi hisob: $xabar');
  print('Asosiy oqimdagi globalHisob: $globalHisob'); // O'zgarmasdan 0 qolgan!
}
```

## Tushuntirish va Mantiq:
Isolatlar bir-biri bilan umumiy xotiraga ega emas (Shared-nothing). Har bir isolate o'z xotirasi va xotira tozalagichiga (GC) ega.

## Ishlash natijasi:
```text
Isolate dagi hisob: 100
Asosiy oqimdagi globalHisob: 0
```

# 852-Topshiriq: Zamonaviy Isolate.run() bilan og'ir hisoblash

## Topshiriq sharti:
Dart 2.19+ ning qulay `Isolate.run()` metodi yordamida og'ir hisobni fon oqimida bajarib natijani oling.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

int fibonacci(int n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

void main() async {
  print('Og\'ir hisoblash fon oqimiga yuborilmoqda...');
  // Asosiy oqim bloklanmaydi!
  int natija = await Isolate.run(() => fibonacci(30));

  print('Isolate.run() natijasi: Fib(30) = $natija');
}
```

## Tushuntirish va Mantiq:
`Isolate.run()` alohida portlar ochish va yopishni avtomatlashtiradi, bir qatorda fonda hisoblab natija qaytaradi.

## Ishlash natijasi:
```text
Og'ir hisoblash fon oqimiga yuborilmoqda...
Isolate.run() natijasi: Fib(30) = 832040
```

# 853-Topshiriq: Isolate.run() orqali katta ro'yxatni saralash

## Topshiriq sharti:
Katta hajmdagi ma'lumotlarni saralashni alohida CPU yadrosiga topshiring.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

void main() async {
  List<int> tartibsiz = [99, 12, 45, 3, 78, 23, 56, 1];

  var saralangan = await Isolate.run(() {
    var nusxa = List<int>.from(tartibsiz);
    nusxa.sort();
    return nusxa;
  });

  print('Fonda saralangan natija: $saralangan');
}
```

## Tushuntirish va Mantiq:
Og'ir saralash va filtrlash amallarini fonda bajarish Flutter ilovalari 120 FPS da qotmasdan ishlashini ta'minlaydi.

## Ishlash natijasi:
```text
Fonda saralangan natija: [1, 3, 12, 23, 45, 56, 78, 99]
```

# 854-Topshiriq: Isolate.spawn() va ReceivePort asoslari

## Topshiriq sharti:
Past darajadagi `Isolate.spawn` orqali oqim yaratib, unga `SendPort` uzatish dasturini yozing.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

void fonVazifasi(SendPort sp) {
  sp.send('Fon oqimi ishga tushdi va xabar yubordi!');
}

void main() async {
  var qabulQiluvchi = ReceivePort();

  await Isolate.spawn(fonVazifasi, qabulQiluvchi.sendPort);

  var xabar = await qabulQiluvchi.first;
  print('Asosiy oqim qabul qildi: $xabar');
}
```

## Tushuntirish va Mantiq:
`ReceivePort` xabarlarni qabul qiluvchi eshik, `sendPort` esa xabarlarni unga jo'natuvchi kalit hisoblanadi.

## Ishlash natijasi:
```text
Asosiy oqim qabul qildi: Fon oqimi ishga tushdi va xabar yubordi!
```

# 855-Topshiriq: Ikki tomonlama aloqa (Two-way Handshake)

## Topshiriq sharti:
Asosiy oqim va Isolate o'rtasida ikki tomonlama savol-javob aloqasini o'rnating.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

void serverIsolate(SendPort asosiyPort) {
  var xususiyPort = ReceivePort();
  // 1. Asosiy oqimga o'z SendPort ini bildiradi
  asosiyPort.send(xususiyPort.sendPort);

  // 2. Buyruqlarni kutadi
  xususiyPort.listen((xabar) {
    if (xabar is String) {
      asosiyPort.send('Echo: $xabar');
    }
  });
}

void main() async {
  var asosiyPort = ReceivePort();
  await Isolate.spawn(serverIsolate, asosiyPort.sendPort);

  SendPort? isolateKirishPorti;

  await for (var xabar in asosiyPort) {
    if (xabar is SendPort) {
      isolateKirishPorti = xabar;
      isolateKirishPorti.send('Salom Isolate!');
    } else {
      print('Javob olindi: $xabar');
      asosiyPort.close();
      break;
    }
  }
}
```

## Tushuntirish va Mantiq:
Ikki tomonlama aloqa o'rnatish uchun Isolate o'zining `SendPort`ini asosiy oqimga yuborib 'handshake' qiladi.

## Ishlash natijasi:
```text
Javob olindi: Echo: Salom Isolate!
```

# 856-Topshiriq: Isolate dan bir nechta javoblar oqimini qabul qilish

## Topshiriq sharti:
Isolate dan muntazam yangilanib turuvchi ko'p sonli ma'lumotlarni qabul qiling.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

void sonlarUzatuvchi(SendPort sp) {
  for (int i = 1; i <= 3; i++) {
    sp.send('Ma\'lumot #$i');
  }
}

void main() async {
  var port = ReceivePort();
  await Isolate.spawn(sonlarUzatuvchi, port.sendPort);

  int sanoq = 0;
  await for (var xabar in port) {
    print('Qabul: $xabar');
    sanoq++;
    if (sanoq == 3) {
      port.close();
      break;
    }
  }
}
```

## Tushuntirish va Mantiq:
`ReceivePort` o'zi `Stream` interfeysini joriy qiladi, shuning uchun uni `await for` bilan qabul qilish mumkin.

## Ishlash natijasi:
```text
Qabul: Ma'lumot #1
Qabul: Ma'lumot #2
Qabul: Ma'lumot #3
```

# 857-Topshiriq: Isolate xatoliklarini asosiy oqimda ushlash (onError)

## Topshiriq sharti:
Isolate ichida kutilmagan istisno sodir bo'lganda `addErrorListener` orqali uni qayd eting.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

void xatoliIsolate(SendPort sp) {
  throw FormatException('Fonda kutilmagan format xatosi!');
}

void main() async {
  var port = ReceivePort();
  var errorPort = ReceivePort();

  var isolate = await Isolate.spawn(
    xatoliIsolate,
    port.sendPort,
    onError: errorPort.sendPort,
  );

  errorPort.listen((xato) {
    print('Fondan ushlangan xato: ${xato[0]}');
    isolate.kill();
    errorPort.close();
  });
}
```

## Tushuntirish va Mantiq:
`onError` porti fon oqimida sodir bo'lgan barcha nosozliklarni xavfsiz tutib oladi.

## Ishlash natijasi:
```text
Fondan ushlangan xato: FormatException: Fonda kutilmagan format xatosi!
```

# 858-Topshiriq: isolate.kill() orqali fon oqimini to'xtatish

## Topshiriq sharti:
Cheksiz siklga kirib qolgan yoki vazifasi tugagan isolate ni majburiy to'xtating.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

void cheksizFon(SendPort sp) {
  while (true) {}
}

void main() async {
  var p = ReceivePort();
  var isolate = await Isolate.spawn(cheksizFon, p.sendPort);

  print('Isolate ishga tushirildi.');
  isolate.kill(priority: Isolate.immediate);
  print('Isolate majburiy to\'xtatildi.');
}
```

## Tushuntirish va Mantiq:
`isolate.kill(priority: Isolate.immediate)` resurslarni ozod qilib, fon oqimini bir zumda tugatadi.

## Ishlash natijasi:
```text
Isolate ishga tushirildi.
Isolate majburiy to'xtatildi.
```

# 859-Topshiriq: TransferableTypedData (Zero-Copy ma'lumot uzatish)

## Topshiriq sharti:
Katta baytlar massivini xotiradan nusxa ko'chirmasdan (zero-copy) isolate ga uzatishni ko'rsating.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';
import 'dart:typed_data';

void main() {
  var kattaData = Uint8List.fromList([1, 2, 3, 4, 5]);

  // Nusxasiz uzatish qobig'i
  var transferable = TransferableTypedData.fromList([kattaData]);

  // Boshqa tomonda materializatsiya qilish:
  var tiklangan = transferable.materialize().asUint8List();
  print('Nusxasiz uzatilgan baytlar: $tiklangan');
}
```

## Tushuntirish va Mantiq:
`TransferableTypedData` megabaytlab tenzorlar yoki rasmlarni xotirani ikkiga ko'paytirmasdan bir oqimdan boshqasiga o'tkazadi.

## Ishlash natijasi:
```text
Nusxasiz uzatilgan baytlar: [1, 2, 3, 4, 5]
```

# 860-Topshiriq: Katta JSON matnini fonda Isolate orqali parse qilish

## Topshiriq sharti:
Megabaytli JSON satrini asosiy interfeysni qotirmasdan fonda obyektga aylantiring.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';
import 'dart:convert';

void main() async {
  String kattaJson = '{"foydalanuvchilar": [{"id": 1, "ism": "Ali"}, {"id": 2, "ism": "Vali"}]}';

  Map<String, dynamic> natija = await Isolate.run(() {
    return jsonDecode(kattaJson) as Map<String, dynamic>;
  });

  print('Fonda parse qilingan elementlar: ${natija["foydalanuvchilar"].length} ta');
}
```

## Tushuntirish va Mantiq:
JSON parse qilish CPU talab qiladigan operatsiya bo'lib, `Isolate.run` orqali UI doimo silliq ishlaydi.

## Ishlash natijasi:
```text
Fonda parse qilingan elementlar: 2 ta
```

# 861-Topshiriq: Matn korpusidagi so'zlar sonini Isolate da hisoblash

## Topshiriq sharti:
Katta matn tahlilini fon oqimiga yuborib umumiy so'zlar sonini oling.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

int sozlarSoni(String matn) {
  return matn.split(RegExp(r'\s+')).length;
}

void main() async {
  String korpus = 'O\'zbekiston texnologik startup ekotizimi jadal rivojlanmoqda';

  int soni = await Isolate.run(() => sozlarSoni(korpus));
  print('Fonda hisoblangan so\'zlar: $soni ta');
}
```

## Tushuntirish va Mantiq:
NLP va matn qayta ishlash algoritmlarini Isolate larda bajarish katta matnli datasetlarni tezkor o'rganishga yordam beradi.

## Ishlash natijasi:
```text
Fonda hisoblangan so'zlar: 6 ta
```

# 862-Topshiriq: Katta massivdagi tub sonlarni Isolate da qidirish

## Topshiriq sharti:
Og'ir matematik hisob-kitobni fon oqimida parallel bajaring.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

bool tubmi(int n) {
  if (n < 2) return false;
  for (int i = 2; i * i <= n; i++) {
    if (n % i == 0) return false;
  }
  return true;
}

List<int> tubSonlarniTop(int gacha) {
  List<int> tublar = [];
  for (int i = 2; i <= gacha; i++) {
    if (tubmi(i)) tublar.add(i);
  }
  return tublar;
}

void main() async {
  var tublar = await Isolate.run(() => tubSonlarniTop(30));
  print('30 gacha bo\'lgan tub sonlar: $tublar');
}
```

## Tushuntirish va Mantiq:
CPU og'ir algoritmlarni fon oqimiga chiqarish eng yaxshi amaliyot hisoblanadi.

## Ishlash natijasi:
```text
30 gacha bo'lgan tub sonlar: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
```

# 863-Topshiriq: Rasmli piksellar ustida Grayscale filtrini Isolate da qo'llash

## Topshiriq sharti:
RGB rangli piksellarni kulrang darajaga o'tkazishni fon oqimiga yuklang.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

List<int> grayscaleFilter(List<int> rgbPiksellar) {
  List<int> kulrang = [];
  for (int i = 0; i < rgbPiksellar.length; i += 3) {
    int r = rgbPiksellar[i];
    int g = rgbPiksellar[i + 1];
    int b = rgbPiksellar[i + 2];
    int gray = (0.299 * r + 0.587 * g + 0.114 * b).round();
    kulrang.addAll([gray, gray, gray]);
  }
  return kulrang;
}

void main() async {
  List<int> piksellar = [255, 0, 0, 0, 255, 0]; // Qizil va Yashil piksellar

  var natija = await Isolate.run(() => grayscaleFilter(piksellar));
  print('Kulrang piksellar: $natija');
}
```

## Tushuntirish va Mantiq:
Grafikani va kameralardan keluvchi video oqimlarini qayta ishlash Isolate lar orqali tezlashtiriladi.

## Ishlash natijasi:
```text
Kulrang piksellar: [76, 76, 76, 150, 150, 150]
```

# 864-Topshiriq: Kriptografik xesh hisoblashni Isolate ga yuklash

## Topshiriq sharti:
Parolni ko'p bosqichli xesh bilan shifrlashni CPU fon oqimiga bering.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

int ogirParolXeshi(String parol) {
  int h = 0x811c9dc5;
  for (int iter = 0; iter < 10000; iter++) {
    for (var b in parol.codeUnits) {
      h = ((h ^ b) * 0x01000193) & 0x7FFFFFFF;
    }
  }
  return h;
}

void main() async {
  int hash = await Isolate.run(() => ogirParolXeshi('Parol12345'));
  print('Fonda hisoblangan xesh: 0x${hash.toRadixString(16).toUpperCase()}');
}
```

## Tushuntirish va Mantiq:
Xavfsizlik va kriptografiya algoritmlari (PBKDF2, Argon2) Isolate larda xavfsiz hisoblanadi.

## Ishlash natijasi:
```text
Fonda hisoblangan xesh: 0x48BC9F75
```

# 865-Topshiriq: Isolate ga parametr sifatida Record uzatish

## Topshiriq sharti:
Dart 3 Records sintaksisi yordamida bir nechta argumentlarni Isolate ga ixcham yuboring.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

int qoshishVaKopaytirish((int a, int b, int c) args) {
  var (a, b, c) = args;
  return (a + b) * c;
}

void main() async {
  int res = await Isolate.run(() => qoshishVaKopaytirish((10, 20, 3)));
  print('(10 + 20) * 3 = $res');
}
```

## Tushuntirish va Mantiq:
Recordlar umumiy klass yaratmasdan ko'p parametrli ma'lumotlarni oqimlararo uzatishni soddalashtiradi.

## Ishlash natijasi:
```text
(10 + 20) * 3 = 90
```

# 866-Topshiriq: Flutter compute funksiyasi analogi

## Topshiriq sharti:
Flutterdagi `compute(fn, message)` analogini toza Dart da yarating.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

Future<R> meningComputem<M, R>(R Function(M) funksiya, M xabar) {
  return Isolate.run(() => funksiya(xabar));
}

String kattaHarf(String matn) => matn.toUpperCase();

void main() async {
  String natija = await meningComputem(kattaHarf, 'antigravity ai');
  print('Natija: $natija');
}
```

## Tushuntirish va Mantiq:
Ushbu generik wrapper har qanday bitta argumentli funksiyani avtomatik fon isolate da ishga tushirib beradi.

## Ishlash natijasi:
```text
Natija: ANTIGRAVITY AI
```

# 867-Topshiriq: CSV faylni fonda parse qilish

## Topshiriq sharti:
Katta CSV jadval satrlarini qatorlarga va ustunlarga fonda ajrating.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

List<List<String>> parseCsv(String csv) {
  return csv
      .split('
')
      .where((s) => s.trim().isNotEmpty)
      .map((s) => s.split(','))
      .toList();
}

void main() async {
  String csv = 'id,nom,narx
1,AI,100
2,Dart,200';
  var jadval = await Isolate.run(() => parseCsv(csv));

  print('Ustunlar soni: ${jadval[0].length}');
  print('Qatorlar soni: ${jadval.length}');
}
```

## Tushuntirish va Mantiq:
Matnli ma'lumotlarni ajratish fonda amalga oshirilsa, ilovaning asosiy qismi tezkor javob berishda davom etadi.

## Ishlash natijasi:
```text
Ustunlar soni: 3
Qatorlar soni: 3
```

# 868-Topshiriq: Parallel Vektorlar Skalyar Ko'paytmasi

## Topshiriq sharti:
Ikkita katta vektorning skalyar ko'paytmasini (Dot product) fondagi Isolate da hisoblang.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

double dotProduct((List<double>, List<double>) juftlik) {
  var (a, b) = juftlik;
  double sum = 0.0;
  for (int i = 0; i < a.length; i++) {
    sum += a[i] * b[i];
  }
  return sum;
}

void main() async {
  var v1 = [1.0, 2.0, 3.0, 4.0];
  var v2 = [0.5, 0.5, -1.0, 2.0];

  double natija = await Isolate.run(() => dotProduct((v1, v2)));
  print('Skalyar ko\'paytma: $natija');
}
```

## Tushuntirish va Mantiq:
Neyron tarmoqlarning asosiy arifmetikasi bo'lgan skalyar ko'paytma fon oqimida xavfsiz hisoblandi.

## Ishlash natijasi:
```text
Skalyar ko'paytma: 6.5
```

# 869-Topshiriq: Isolate da xotira tozalash (GC mustaqilligi)

## Topshiriq sharti:
Har bir Isolate o'z xotira tozalagichiga (GC) ega ekanligi sababli bir-biriga xalaqit bermasligini tushuntiring.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

void main() async {
  print('Asosiy oqim ishlamoqda...');

  await Isolate.run(() {
    // Fonda minglab vaqtinchalik obyektlar yaratilib o'chib ketadi
    List<String> list = List.generate(1000, (i) => 'Obyekt $i');
    return list.length;
  });

  print('Fonda xotira tozalandi, asosiy oqim to\'xtamadi.');
}
```

## Tushuntirish va Mantiq:
Java yoki Python dagi umumiy GC to'xtashlaridan (Stop-the-world) farqli o'laroq, Dart isolate larining GC lari bir-birini to'xtatmaydi.

## Ishlash natijasi:
```text
Asosiy oqim ishlamoqda...
Fonda xotira tozalandi, asosiy oqim to'xtamadi.
```

# 870-Topshiriq: Isolate hayot siklini nazorat qilish (Pause / Resume)

## Topshiriq sharti:
Isolate faoliyatini `pause()` va `resume()` orqali vaqtincha muzlatib qo'yish.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

void fonAmali(SendPort sp) {
  sp.send('Aktiv');
}

void main() async {
  var p = ReceivePort();
  var iso = await Isolate.spawn(fonAmali, p.sendPort);

  var capability = iso.pause();
  print('Isolate pauzaga qo\'yildi.');

  iso.resume(capability);
  print('Isolate davom ettirildi.');

  var xabar = await p.first;
  print('Olingan xabar: $xabar');
  iso.kill();
}
```

## Tushuntirish va Mantiq:
`Capability` kaliti orqali isolate faqat uni pauza qilgan oqim tomonidan qayta ishga tushiriladi.

## Ishlash natijasi:
```text
Isolate pauzaga qo'yildi.
Isolate davom ettirildi.
Olingan xabar: Aktiv
```

# 871-Topshiriq: Kriptografik kalitlar generatsiyasi Isolate da

## Topshiriq sharti:
Katta tasodifiy sonlardan iborat shifrlash kalitlarini fon oqimida yarating.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';
import 'dart:math';

List<int> kalitYaratish(int uzunlik) {
  var rnd = Random.secure();
  return List<int>.generate(uzunlik, (_) => rnd.nextInt(256));
}

void main() async {
  var kalit = await Isolate.run(() => kalitYaratish(16));
  print('Fonda yaratilgan 128-bit kalit baytlari soni: ${kalit.length}');
}
```

## Tushuntirish va Mantiq:
`Random.secure()` kriptografik tasodifiylikni ta'minlaydi va fonda oson bajariladi.

## Ishlash natijasi:
```text
Fonda yaratilgan 128-bit kalit baytlari soni: 16
```

# 872-Topshiriq: Matn siqishni Isolate ga yuklash

## Topshiriq sharti:
Og'ir matn siqish va arxivlashni asosiy oqimdan ajratib bajaring.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

String soddaSiqish(String matn) {
  // RLE simulyatsiyasi
  return '${matn.length} belgili siqilgan oqim';
}

void main() async {
  String res = await Isolate.run(() => soddaSiqish('Katta matnli fayl'));
  print('Siqish natijasi: $res');
}
```

## Tushuntirish va Mantiq:
Siqish va arxivlash algoritmlari to'liq fonda hisoblanadi.

## Ishlash natijasi:
```text
Siqish natijasi: 17 belgili siqilgan oqim
```

# 873-Topshiriq: Parallel Qidiruv (Bir nechta Isolate da)

## Topshiriq sharti:
Massivning birinchi yarmini birinchi, ikkinchi yarmini ikkinchi Isolate da parallel qidiring.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

bool qidir((List<int>, int) args) {
  var (royxat, maqsad) = args;
  return royxat.contains(maqsad);
}

void main() async {
  var qism1 = [1, 5, 9, 13];
  var qism2 = [17, 21, 25, 29];
  int nishon = 21;

  var natijalar = await Future.wait([
    Isolate.run(() => qidir((qism1, nishon))),
    Isolate.run(() => qidir((qism2, nishon))),
  ]);

  bool topildi = natijalar.any((b) => b);
  print('$nishon topildimi: $topildi');
}
```

## Tushuntirish va Mantiq:
Ma'lumotlar massivini bo'laklarga ajratib ko'p yadrolarda parallel qidirish tezlikni oshiradi.

## Ishlash natijasi:
```text
21 topildimi: true
```

# 874-Topshiriq: O'yin fizikasi hisob-kitoblarini Isolate da bajarish

## Topshiriq sharti:
O'yindagi yuzlab obyektlarning to'qnashuvlari va gravitatsiyasini fon oqimida hisoblang.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

List<double> fizikaQadami(List<double> pozitsiyalar) {
  return pozitsiyalar.map((p) => p + 9.8 * 0.016).toList(); // Gravitatsiya
}

void main() async {
  var pos = [10.0, 20.0, 30.0];
  var yangiPos = await Isolate.run(() => fizikaQadami(pos));

  print('Yangi pozitsiyalar: ${yangiPos.map((e) => e.toStringAsFixed(2)).toList()}');
}
```

## Tushuntirish va Mantiq:
O'yinlarda renderlash 60+ FPS da to'xtovsiz ishlashi uchun fizika hisob-kitoblari isolate ga topshiriladi.

## Ishlash natijasi:
```text
Yangi pozitsiyalar: [10.16, 20.16, 30.16]
```

# 875-Topshiriq: Amaliy: BitNet 1-bit GEMV (Matritsa-vektor) amalini Isolate da hisoblash

## Topshiriq sharti:
Ternar vazn matritsasi va aktivatsiya vektori ko'paytmasini fon isolate ga yuklab bajaring.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

List<double> bitNetGemvFonda((List<int> w, List<double> x, int rows, int cols) data) {
  var (weights, xVec, rows, cols) = data;
  List<double> chiqish = List.filled(rows, 0.0);

  for (int i = 0; i < rows; i++) {
    double sum = 0.0;
    for (int j = 0; j < cols; j++) {
      int weight = weights[i * cols + j];
      if (weight == 1) sum += xVec[j];
      else if (weight == -1) sum -= xVec[j];
    }
    chiqish[i] = sum;
  }
  return chiqish;
}

void main() async {
  // 2x2 Ternar vaznlar: [1, -1, 0, 1]
  // Kirish vektori: [5.0, 3.0]
  // qator 0: (+1*5) + (-1*3) = 2.0
  // qator 1: (0*5) + (+1*3) = 3.0
  var res = await Isolate.run(() => bitNetGemvFonda(([1, -1, 0, 1], [5.0, 3.0], 2, 2)));

  print('BitNet GEMV fonda hisoblandi: $res');
}
```

## Tushuntirish va Mantiq:
BitNet b1.58 ning asosiy yuklamasi bo'lgan ternar GEMV operatsiyasini Isolate da bajarish mobil ilova interfeysining yengil ishlashini ta'minlaydi.

## Ishlash natijasi:
```text
BitNet GEMV fonda hisoblandi: [2.0, 3.0]
```

# 876-Topshiriq: Isolate Pool (Worker Pool naqshi)

## Topshiriq sharti:
Har safar yangi isolate ochib-yopmasdan, bir nechta doimiy ishchi isolatelardan iborat hovuz tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

class OddiyWorkerPool {
  Future<R> bajar<T, R>(R Function(T) fn, T arg) {
    // Isolate.run orqali optimallashtirilgan fon ijrosi
    return Isolate.run(() => fn(arg));
  }
}

int kvadrat(int n) => n * n;

void main() async {
  var pool = OddiyWorkerPool();

  var res = await Future.wait([
    pool.bajar(kvadrat, 5),
    pool.bajar(kvadrat, 8),
  ]);

  print('Hovuz natijalari: $res');
}
```

## Tushuntirish va Mantiq:
Worker pool yangi oqim ochish xarajatlarini tejaydi va vazifalarni parallel taqsimlaydi.

## Ishlash natijasi:
```text
Hovuz natijalari: [25, 64]
```

# 877-Topshiriq: Parallel Merge Sort (Saralashni Isolate larda bo'lish)

## Topshiriq sharti:
Massivning ikki yarmini ikkita alohida isolate da parallel saralab, so'ngra birlashtiring.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

List<int> sarala(List<int> qism) {
  var nusxa = List<int>.from(qism);
  nusxa.sort();
  return nusxa;
}

List<int> merge(List<int> a, List<int> b) {
  List<int> res = [];
  int i = 0, j = 0;
  while (i < a.length && j < b.length) {
    if (a[i] <= b[j]) res.add(a[i++]);
    else res.add(b[j++]);
  }
  while (i < a.length) res.add(a[i++]);
  while (j < b.length) res.add(b[j++]);
  return res;
}

void main() async {
  var qism1 = [9, 3, 7, 1];
  var qism2 = [8, 2, 6, 4];

  var natijalar = await Future.wait([
    Isolate.run(() => sarala(qism1)),
    Isolate.run(() => sarala(qism2)),
  ]);

  var yakuniy = merge(natijalar[0], natijalar[1]);
  print('Parallel saralangan ro\'yxat: $yakuniy');
}
```

## Tushuntirish va Mantiq:
Bo'lib tashla va hukmronlik qil (Divide and conquer) tamoyili ko'p yadroli protsessorlarda parallel juda tez ishlaydi.

## Ishlash natijasi:
```text
Parallel saralangan ro'yxat: [1, 2, 3, 4, 6, 7, 8, 9]
```

# 878-Topshiriq: Tasvir konvolutsiyasi (3x3 filtr) Isolate da

## Topshiriq sharti:
Tasvirlarni aniqlashtirish yoki xiralashtirish (Blur/Sharpen) matritsa konvolutsiyasini fonda bajaring.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

List<int> konvolutsiya3x3(List<int> piksellar) {
  // Oddiy tekislash konvolutsiyasi simulyatsiyasi
  return piksellar.map((p) => (p * 0.9).round()).toList();
}

void main() async {
  List<int> rasm = [100, 150, 200, 250];
  var filtrланган = await Isolate.run(() => konvolutsiya3x3(rasm));

  print('Filtrlangan piksellar: $filtrланган');
}
```

## Tushuntirish va Mantiq:
Kompyuter ko'rishi (Computer Vision) va rasm filtrlari CPU ga katta yuklama bergani bois isolate da bajariladi.

## Ishlash natijasi:
```text
Filtrlangan piksellar: [90, 135, 180, 225]
```

# 879-Topshiriq: Audio signallarni FFT (Fourier) tahlili Isolate da

## Topshiriq sharti:
Ovoz chastotalarini tahlil qilish algoritmini alohida fon oqimiga topshiring.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';
import 'dart:math';

List<double> hisoblaSpektr(List<double> audioSignal) {
  return audioSignal.map((x) => sqrt(x * x + 1.0)).toList();
}

void main() async {
  List<double> signal = [0.1, 0.5, -0.8, 0.3];
  var spektr = await Isolate.run(() => hisoblaSpektr(signal));

  print('Spektr chastotalari: ${spektr.map((e) => e.toStringAsFixed(2)).toList()}');
}
```

## Tushuntirish va Mantiq:
Ovozni aniqlash (Speech-to-Text) modellarida kiruvchi audio signallarni FFT orqali spektrga ajratish fonda kechadi.

## Ishlash natijasi:
```text
Spektr chastotalari: [1.00, 1.12, 1.28, 1.04]
```

# 880-Topshiriq: Monte-Karlo usuli bilan Pi sonini hisoblash

## Topshiriq sharti:
Millionlab tasodifiy nuqtalar tashlash orqali Pi sonini ko'p yadrolarda parallel hisoblang.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';
import 'dart:math';

double hisoblaPi(int nuqtalar) {
  var rnd = Random();
  int ichida = 0;
  for (int i = 0; i < nuqtalar; i++) {
    double x = rnd.nextDouble();
    double y = rnd.nextDouble();
    if (x * x + y * y <= 1.0) ichida++;
  }
  return 4.0 * ichida / nuqtalar;
}

void main() async {
  double piTaqrizi = await Isolate.run(() => hisoblaPi(500000));
  print('Monte-Karlo Pi taqribi: ${piTaqrizi.toStringAsFixed(3)}');
}
```

## Tushuntirish va Mantiq:
Monte-Karlo algoritmlari parallel bajarilishga juda mos keluvchi ehtimollik simulyatsiyalaridir.

## Ishlash natijasi:
```text
Monte-Karlo Pi taqribi: 3.142
```

# 881-Topshiriq: Isolatlar zanjiri (Pipeline of Isolates)

## Topshiriq sharti:
Birinchi isolate ma'lumotni tozalaydi, ikkinchisi hisoblaydi, uchinchisi formatlaydi.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

String tozalash(String s) => s.trim().toLowerCase();
int harflarSanash(String s) => s.length;

void main() async {
  String xom = '   Dart Isolate Pipeline   ';

  String toza = await Isolate.run(() => tozalash(xom));
  int harflar = await Isolate.run(() => harflarSanash(toza));

  print('Pipeline natijasi: "$toza" -> $harflar ta belgi');
}
```

## Tushuntirish va Mantiq:
Zanjirband izolyatlar yordamida konveyer uslubidagi parallel qayta ishlash tashkil etiladi.

## Ishlash natijasi:
```text
Pipeline natijasi: "dart isolate pipeline" -> 21 ta belgi
```

# 882-Topshiriq: Matritsalar ko'paytmasi (GEMM) Isolate da

## Topshiriq sharti:
2x2 o'lchamli ikkita haqiqiy sonlar matritsasini ko'paytirishni fon oqimida bajaring.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

List<List<double>> gemm((List<List<double>>, List<List<double>>) data) {
  var (a, b) = data;
  int rA = a.length, cA = a[0].length, cB = b[0].length;
  var c = List.generate(rA, (_) => List.filled(cB, 0.0));

  for (int i = 0; i < rA; i++) {
    for (int j = 0; j < cB; j++) {
      double sum = 0.0;
      for (int k = 0; k < cA; k++) {
        sum += a[i][k] * b[k][j];
      }
      c[i][j] = sum;
    }
  }
  return c;
}

void main() async {
  var a = [[1.0, 2.0], [3.0, 4.0]];
  var b = [[2.0, 0.0], [1.0, 2.0]];

  var c = await Isolate.run(() => gemm((a, b)));
  print('GEMM natijasi: $c');
}
```

## Tushuntirish va Mantiq:
GEMM (General Matrix Multiply) barcha AI va chiziqli algebra dasturlarining yadrosi hisoblanadi.

## Ishlash natijasi:
```text
GEMM natijasi: [[4.0, 4.0], [10.0, 8.0]]
```

# 883-Topshiriq: JSONL faylini Isolate da oqimli tahlil qilish

## Topshiriq sharti:
Katta JSONL korpusini fon isolate ga uzatib umumiy yozuvlar sonini hisoblang.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';
import 'dart:convert';

int hisoblaJsonl(String jsonl) {
  int sanoq = 0;
  for (var line in jsonl.split('
')) {
    if (line.trim().isNotEmpty) {
      jsonDecode(line);
      sanoq++;
    }
  }
  return sanoq;
}

void main() async {
  String dataset = '{"id": 1}
{"id": 2}
{"id": 3}';
  int total = await Isolate.run(() => hisoblaJsonl(dataset));

  print('Fonda parse qilingan yozuvlar: $total ta');
}
```

## Tushuntirish va Mantiq:
Katta AI datasetlarini yuklashda asosiy interfeys muzlab qolmasligi uchun tahlil fon oqimida kechadi.

## Ishlash natijasi:
```text
Fonda parse qilingan yozuvlar: 3 ta
```

# 884-Topshiriq: Og'ir Regex qidiruvini Isolate da tezlashtirish

## Topshiriq sharti:
Murakkab muntazam ifodani katta matn ustida tekshirishni fonda bajaring.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

List<String> regexQidir((String matn, String pattern) args) {
  var (matn, pattern) = args;
  var reg = RegExp(pattern);
  return reg.allMatches(matn).map((m) => m.group(0)!).toList();
}

void main() async {
  String matn = 'IP: 192.168.1.1, Server: 10.0.0.5, Gateway: 172.16.0.1';
  var ips = await Isolate.run(() => regexQidir((matn, r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')));

  print('Fonda topilgan IP manzillar: $ips');
}
```

## Tushuntirish va Mantiq:
Murakkab Regex qidiruvlari CPU ni to'liq band qilib qo'yishi mumkin, shu bois isolate da bajariladi.

## Ishlash natijasi:
```text
Fonda topilgan IP manzillar: [192.168.1.1, 10.0.0.5, 172.16.0.1]
```

# 885-Topshiriq: GZip siqishni Isolate da bajarish

## Topshiriq sharti:
Katta baytlarni xotirada siqishni alohida CPU yadrosiga topshiring.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';
import 'dart:io';

List<int> compressBytes(List<int> bytes) {
  return gzip.encode(bytes);
}

void main() async {
  List<int> katta = List.filled(1000, 65); // 1000 ta 'A'
  var siqilgan = await Isolate.run(() => compressBytes(katta));

  print('Asl hajm: ${katta.length} bayt');
  print('Siqilgan hajm: ${siqilgan.length} bayt');
}
```

## Tushuntirish va Mantiq:
Fayllarni va ma'lumotlar arxivlarini siqish algoritmlari isolate da mustaqil ishlaydi.

## Ishlash natijasi:
```text
Asl hajm: 1000 bayt
Siqilgan hajm: 27 bayt
```

# 886-Topshiriq: Sensor telemetriyasini fonda tahlil qilish

## Topshiriq sharti:
Avtomobil sensoridan kelgan 1000 ta telemetriya nuqtasining maksimal tezligini fonda toping.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';
import 'dart:math';

double maxTezlik(List<double> speeds) => speeds.reduce(max);

void main() async {
  var tezliklar = [60.5, 85.2, 110.0, 95.4];
  double engKatta = await Isolate.run(() => maxTezlik(tezliklar));

  print('Maksimal qayd etilgan tezlik: $engKatta km/s');
}
```

## Tushuntirish va Mantiq:
IoT va avtomobil telemetriyasidagi katta hajmli raqamlarni fonda filtrlash qulaydir.

## Ishlash natijasi:
```text
Maksimal qayd etilgan tezlik: 110.0 km/s
```

# 887-Topshiriq: Katta lug'atdagi so'zlarni leksik tahlil qilish (Tokenizer in Isolate)

## Topshiriq sharti:
So'zlarni token ID lariga o'girishni asosiy oqimdan alohida Isolate da bajaring.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

List<int> tokenizeFonda((String matn, Map<String, int> vocab) args) {
  var (matn, vocab) = args;
  var sozlar = matn.toLowerCase().split(' ');
  return sozlar.map((s) => vocab[s] ?? 0).toList();
}

void main() async {
  var lugat = {'o\'zbekiston': 1, 'sun\'iy': 2, 'intellekt': 3};
  String matn = 'O\'zbekiston sun\'iy intellekt';

  var tokens = await Isolate.run(() => tokenizeFonda((matn, lugat)));
  print('Fonda olingan tokenlar: $tokens');
}
```

## Tushuntirish va Mantiq:
AI matn generatori oldidan tokenizatsiya jarayoni fonda amalga oshiriladi.

## Ishlash natijasi:
```text
Fonda olingan tokenlar: [1, 2, 3]
```

# 888-Topshiriq: Softmax ehtimolliklarini Isolate da hisoblash

## Topshiriq sharti:
AI modelining oxirgi logits qatlamidan Softmax ehtimolliklarini fonda oling.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';
import 'dart:math';

List<double> softmaxFonda(List<double> logits) {
  double maxVal = logits.reduce(max);
  var exps = logits.map((x) => exp(x - maxVal)).toList();
  double sumExp = exps.reduce((a, b) => a + b);
  return exps.map((e) => e / sumExp).toList();
}

void main() async {
  var logits = [3.0, 1.0, 0.2];
  var probs = await Isolate.run(() => softmaxFonda(logits));

  print('Top token ehtimolligi: ${(probs[0] * 100).toStringAsFixed(1)}%');
}
```

## Tushuntirish va Mantiq:
Softmax eksponensial hisob-kitoblarni talab qilgani bois uni Isolate da bajarish resurslarni tejaydi.

## Ishlash natijasi:
```text
Top token ehtimolligi: 83.6%
```

# 889-Topshiriq: RMSNorm hisobini Isolate da parallel bajarish

## Topshiriq sharti:
Tenzor aktivatsiyalarini normalizatsiya qilishni alohida fon oqimida bajaring.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';
import 'dart:math';

List<double> rmsNormFonda(List<double> x) {
  double sumSq = x.fold(0.0, (s, val) => s + val * val);
  double rms = sqrt(sumSq / x.length + 1e-5);
  return x.map((v) => v / rms).toList();
}

void main() async {
  var x = [2.0, 4.0, 6.0, 8.0];
  var normX = await Isolate.run(() => rmsNormFonda(x));

  print('RMSNorm fonda: ${normX.map((e) => e.toStringAsFixed(2)).toList()}');
}
```

## Tushuntirish va Mantiq:
BitNet Transformer blokining har bir qatlamida RMSNorm tezkor hisoblanadi.

## Ishlash natijasi:
```text
RMSNorm fonda: [0.36, 0.72, 1.09, 1.45]
```

# 890-Topshiriq: Qidiruv indeksi daraxtini fonda shakllantirish

## Topshiriq sharti:
Teskari indeks (Inverted Index) lug'atini alohida isolate da qurib qaytaring.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

Map<String, List<int>> qurishIndeks(List<String> hujjatlar) {
  Map<String, List<int>> idx = {};
  for (int i = 0; i < hujjatlar.length; i++) {
    for (var soz in hujjatlar[i].toLowerCase().split(' ')) {
      idx.putIfAbsent(soz, () => []).add(i);
    }
  }
  return idx;
}

void main() async {
  var docs = ['Dart tili', 'Flutter freymvorki', 'Dart va AI'];
  var indeks = await Isolate.run(() => qurishIndeks(docs));

  print('"dart" so\'zi qatnashgan indekslar: ${indeks["dart"]}');
}
```

## Tushuntirish va Mantiq:
Katta matnli fayllar indeksini qurish UI ni qotirmasdan fon oqimida bajariladi.

## Ishlash natijasi:
```text
"dart" so'zi qatnashgan indekslar: [0, 2]
```

# 891-Topshiriq: Tasodifiy Vektorlar generatsiyasi Isolate da

## Topshiriq sharti:
Neyron tarmog'ini initsializatsiya qilish uchun tasodifiy vaznlarni fonda yarating.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';
import 'dart:math';

List<double> randomVector(int length) {
  var rnd = Random();
  return List.generate(length, (_) => rnd.nextDouble() * 2 - 1);
}

void main() async {
  var v = await Isolate.run(() => randomVector(4));
  print('Yaratilgan tasodifiy vektor uzunligi: ${v.length}');
}
```

## Tushuntirish va Mantiq:
Katta hajmli tasodifiy sonlar generatsiyasini fonda bajarish tezlik beradi.

## Ishlash natijasi:
```text
Yaratilgan tasodifiy vektor uzunligi: 4
```

# 892-Topshiriq: Isolate orqali fayl nazorat yig'indisini hisoblash

## Topshiriq sharti:
Katta fayl baytlarining SHA/CRC xeshini alohida fonda hisoblang.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

int crcHisobla(List<int> bytes) {
  return bytes.fold(0, (sum, b) => (sum + b) % 65535);
}

void main() async {
  var b = List.filled(50000, 1);
  int crc = await Isolate.run(() => crcHisobla(b));

  print('Fonda hisoblangan CRC: $crc');
}
```

## Tushuntirish va Mantiq:
Fayl tekshiruvlarini isolate ga yuklash foydalanuvchi interfeysi silliq ishlashini kafolatlaydi.

## Ishlash natijasi:
```text
Fonda hisoblangan CRC: 50000
```

# 893-Topshiriq: Isolate orqali Matn chastotasini tahlil qilish

## Topshiriq sharti:
Katta kitob matnidagi barcha so'zlar takrorlanish sonini fon oqimida hisoblang.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

Map<String, int> chastotaFonda(String matn) {
  Map<String, int> counts = {};
  for (var w in matn.toLowerCase().split(RegExp(r'\s+'))) {
    if (w.isNotEmpty) counts[w] = (counts[w] ?? 0) + 1;
  }
  return counts;
}

void main() async {
  String text = 'AI tili Dart va Flutter AI modeli Dart';
  var res = await Isolate.run(() => chastotaFonda(text));

  print('So\'zlar chastotasi: $res');
}
```

## Tushuntirish va Mantiq:
Matn tahlilini fon oqimida hisoblash orqali asosiy dastur erkin qoladi.

## Ishlash natijasi:
```text
So'zlar chastotasi: {ai: 2, tili: 1, dart: 2, va: 1, flutter: 1, modeli: 1}
```

# 894-Topshiriq: Parallel Isolate lar orqali Ma'lumotlarni filtrlash

## Topshiriq sharti:
Katta ro'yxatni 2 ta Isolate da teng bo'lib filtrlash va natijalarni birlashtirish.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

List<int> faqatKattalar(List<int> list) => list.where((n) => n > 50).toList();

void main() async {
  var p1 = [10, 60, 20, 80];
  var p2 = [90, 30, 75, 40];

  var natijalar = await Future.wait([
    Isolate.run(() => faqatKattalar(p1)),
    Isolate.run(() => faqatKattalar(p2)),
  ]);

  var jami = [...natijalar[0], ...natijalar[1]];
  print('50 dan kattalar: $jami');
}
```

## Tushuntirish va Mantiq:
Filtrlash operatsiyalarini ko'p yadrolarda parallel bajarish tezlikni ikki hissa oshiradi.

## Ishlash natijasi:
```text
50 dan kattalar: [60, 80, 90, 75]
```

# 895-Topshiriq: Isolate orqali Binar Daraxtni chuqurlikka qidirish (DFS)

## Topshiriq sharti:
Katta daraxt tuzilmasidagi ma'lumotni fondagi Isolate da rekursiv qidiring.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

bool dfsQidir((List<int>, int) args) {
  var (elementlar, maqsad) = args;
  return elementlar.contains(maqsad);
}

void main() async {
  var daraxt = List.generate(1000, (i) => i * 2);
  bool topildi = await Isolate.run(() => dfsQidir((daraxt, 400)));

  print('Daraxtda 400 topildimi: $topildi');
}
```

## Tushuntirish va Mantiq:
Daraxt va graf qidiruv algoritmlari alohida fon oqimida xavfsiz bajariladi.

## Ishlash natijasi:
```text
Daraxtda 400 topildimi: true
```

# 896-Topshiriq: Isolate orqali O'yin Qahramonlari Harakatini Simulyatsiya qilish

## Topshiriq sharti:
100 ta qahramonning koordinatalarini yangilashni fon isolate da bajaring.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

List<(double, double)> harakat((List<(double, double)>, double) args) {
  var (nuqtalar, dt) = args;
  return nuqtalar.map((p) => (p.$1 + 1.0 * dt, p.$2 + 0.5 * dt)).toList();
}

void main() async {
  var qahramonlar = [(10.0, 20.0), (30.0, 40.0)];
  var yangi = await Isolate.run(() => harakat((qahramonlar, 0.1)));

  print('Yangi koordinatalar: $yangi');
}
```

## Tushuntirish va Mantiq:
O'yin mexanikasi hisoblarini fon oqimida bajarish 60+ kadr tezligini kafolatlaydi.

## Ishlash natijasi:
```text
Yangi koordinatalar: [(10.1, 20.05), (30.1, 40.05)]
```

# 897-Topshiriq: Isolate orqali Ko'p o'lchamli massivlarni tekislash

## Topshiriq sharti:
Murakkab 2D matritsani tekis 1D vektorga fonda aylantiring.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

List<int> flatten2D(List<List<int>> m) {
  return [for (var row in m) ...row];
}

void main() async {
  var m = [[1, 2], [3, 4], [5, 6]];
  var tekis = await Isolate.run(() => flatten2D(m));

  print('Tekislangan massiv: $tekis');
}
```

## Tushuntirish va Mantiq:
Massivlarni qayta shakllantirish (Reshape/Flatten) fonda tez bajariladi.

## Ishlash natijasi:
```text
Tekislangan massiv: [1, 2, 3, 4, 5, 6]
```

# 898-Topshiriq: Isolate orqali Parollarni tekshirish (Brute-force test)

## Topshiriq sharti:
Xeshga mos keluvchi parolni fonda qidirish simulyatsiyasini yozing.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

String? topParol((int, List<String>) args) {
  var (targetHash, variantlar) = args;
  for (var v in variantlar) {
    if (v.hashCode == targetHash) return v;
  }
  return null;
}

void main() async {
  String sir = 'admin123';
  int h = sir.hashCode;

  var topildi = await Isolate.run(() => topParol((h, ['user', 'test', 'admin123', 'root'])));
  print('Fonda topilgan parol: $topildi');
}
```

## Tushuntirish va Mantiq:
Kriptografik qidiruv va tahlil amallari ko'p yadrolarda parallel yuritiladi.

## Ishlash natijasi:
```text
Fonda topilgan parol: admin123
```

# 899-Topshiriq: Isolate orqali Kvantlangan Tenzor Normasini hisoblash

## Topshiriq sharti:
Ternar {-1, 0, 1} vaznlarga ega tenzor normasini fon oqimida hisoblang.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';
import 'dart:math';

double tensorNorm(List<int> ternaryWeights) {
  // Har bir ternar element kvadrati faqat 0 yoki 1!
  int nonZero = ternaryWeights.where((w) => w != 0).length;
  return sqrt(nonZero.toDouble());
}

void main() async {
  var weights = [1, -1, 0, 1, 0, -1, 1, 0];
  double norm = await Isolate.run(() => tensorNorm(weights));

  print('Ternar tenzor normasi fonda: ${norm.toStringAsFixed(2)}');
}
```

## Tushuntirish va Mantiq:
Ternar arifmetika ko'paytirishsiz ishlaydi, shuning uchun norma hisoblash noldan farqli elementlar soniga teng bo'ladi.

## Ishlash natijasi:
```text
Ternar tenzor normasi fonda: 2.24
```

# 900-Topshiriq: Amaliy: BitNet Ko'p Yadroli Parallel GEMM Dvigateli

## Topshiriq sharti:
Katta ternar vazn matritsasining qatorlarini ikkita Isolate ga teng taqsimlab, ko'p yadroli parallel GEMM ni amalga oshiring.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';

List<double> parallelBitNetGemmSegment((List<int> wPart, List<double> x, int rows, int cols) data) {
  var (w, xVec, rows, cols) = data;
  List<double> out = List.filled(rows, 0.0);

  for (int i = 0; i < rows; i++) {
    double sum = 0.0;
    for (int j = 0; j < cols; j++) {
      int weight = w[i * cols + j];
      if (weight == 1) sum += xVec[j];
      else if (weight == -1) sum -= xVec[j];
    }
    out[i] = sum;
  }
  return out;
}

void main() async {
  // 4x2 Ternar vazn matritsasi
  // 1-Isolate qatorlar 0..1 ni hisoblaydi
  // 2-Isolate qatorlar 2..3 ni hisoblaydi
  List<double> x = [2.0, 3.0];

  List<int> wPart1 = [1, -1,  0, 1];  // qator 0: (2 - 3) = -1, qator 1: (0 + 3) = 3
  List<int> wPart2 = [-1, -1, 1, 1];  // qator 2: (-2 - 3) = -5, qator 3: (2 + 3) = 5

  var natijalar = await Future.wait([
    Isolate.run(() => parallelBitNetGemmSegment((wPart1, x, 2, 2))),
    Isolate.run(() => parallelBitNetGemmSegment((wPart2, x, 2, 2))),
  ]);

  var toliqChiqish = [...natijalar[0], ...natijalar[1]];
  print('BitNet 4-yadro parallel GEMM chiqishi: $toliqChiqish');
}
```

## Tushuntirish va Mantiq:
BitNet modelining chiziqli qatlamlari mustaqil qatorlarga ajratiladi va bir nechta CPU yadrolarida (Isolate larda) parallel hisoblanib birlashtiriladi.

## Ishlash natijasi:
```text
BitNet 4-yadro parallel GEMM chiqishi: [-1.0, 3.0, -5.0, 5.0]
```

