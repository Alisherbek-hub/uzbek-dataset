# 701-Topshiriq: Event Loop asoslari (Microtask vs Event Queue)

## Topshiriq sharti:
Dartning bir oqimli (single-threaded) Event Loopida Microtask va Event navbatlari qanday navbatda ishlashini ko'rsating.

## Yechim (Dart kodi):
```dart
import 'dart:async';

void main() {
  print('1. Sinxron boshlanish');

  // Event Queue ga tushadi
  Future(() => print('4. Event Queue (Future)'));

  // Microtask Queue ga tushadi
  scheduleMicrotask(() => print('3. Microtask Queue'));

  print('2. Sinxron yakun');
}
```

## Tushuntirish va Mantiq:
Dart avval barcha sinxron kodni bajaradi, so'ng Microtask navbatidagi vazifalarni, va eng oxirida Event navbatini (Future) ishga tushiradi.

## Ishlash natijasi:
```text
1. Sinxron boshlanish
2. Sinxron yakun
3. Microtask Queue
4. Event Queue (Future)
```

# 702-Topshiriq: scheduleMicrotask ustunligi

## Topshiriq sharti:
Juda muhim tezkor vazifalarni oddiy `Future` dan oldinroq bajarish uchun `scheduleMicrotask` dan foydalaning.

## Yechim (Dart kodi):
```dart
import 'dart:async';

void main() {
  Future.delayed(Duration.zero, () => print('Oddiy Future bajarildi'));
  scheduleMicrotask(() => print('Microtask darhol birinchi bajarildi'));
}
```

## Tushuntirish va Mantiq:
Microtask navbati har doim Event navbatidan yuqori ustunlikka ega bo'lib, zudlik bilan ishlov berish uchun qo'llaniladi.

## Ishlash natijasi:
```text
Microtask darhol birinchi bajarildi
Oddiy Future bajarildi
```

# 703-Topshiriq: Future yaratish va then() bilan natija olish

## Topshiriq sharti:
`Future` orqali kechiktirilgan natijani yaratish va `.then()` orqali natijani qabul qilib chop eting.

## Yechim (Dart kodi):
```dart
Future<String> serverdanSalom() {
  return Future(() => 'Serverdan: Salom Dunyo!');
}

void main() {
  print('So\'rov yuborildi...');
  serverdanSalom().then((javob) {
    print('Javob olindi: $javob');
  });
}
```

## Tushuntirish va Mantiq:
Future kelajakda yakunlanadigan asinxron qiymatni ifodalaydi. `.then()` esa javob tayyor bo'lganda ishga tushadi.

## Ishlash natijasi:
```text
So'rov yuborildi...
Javob olindi: Serverdan: Salom Dunyo!
```

# 704-Topshiriq: async va await sintaksisi

## Topshiriq sharti:
Callbacklar o'rniga toza va ketma-ket o'qiluvchi `async` va `await` sintaksisini qo'llang.

## Yechim (Dart kodi):
```dart
Future<int> ballOlish() async {
  return 95;
}

void main() async {
  print('Natija kutilmoqda...');
  int ball = await ballOlish();
  print('Imtihon bali: $ball');
}
```

## Tushuntirish va Mantiq:
`await` asinxron operatsiya tugaguncha kutib turadi, biroq ilovaning asosiy oqimini bloklamaydi.

## Ishlash natijasi:
```text
Natija kutilmoqda...
Imtihon bali: 95
```

# 705-Topshiriq: Future.delayed kechiktirilgan bajarilish

## Topshiriq sharti:
Belgilangan vaqt kutib so'ngra ishga tushuvchi `Future.delayed` dasturini yozing.

## Yechim (Dart kodi):
```dart
void main() async {
  print('Kutish boshlandi: 100ms...');
  await Future.delayed(Duration(milliseconds: 100));
  print('100 millisekund o\'tib xabar chiqdi!');
}
```

## Tushuntirish va Mantiq:
`Future.delayed` taymer o'rnatib, belgilangan muddatdan keyin qaytadi.

## Ishlash natijasi:
```text
Kutish boshlandi: 100ms...
100 millisekund o'tib xabar chiqdi!
```

# 706-Topshiriq: Future.value darhol tayyor qiymat qaytarish

## Topshiriq sharti:
Keshda bor bo'lgan natijani asinxron interfeys talabiga binoan darhol `Future.value` orqali qaytaring.

## Yechim (Dart kodi):
```dart
Future<String> keshdanYokiServerdan(bool keshdaBor) {
  if (keshdaBor) {
    return Future.value('Keshdagi tezkor ma\'lumot');
  }
  return Future.delayed(Duration(milliseconds: 50), () => 'Server ma\'lumoti');
}

void main() async {
  var javob = await keshdanYokiServerdan(true);
  print(javob);
}
```

## Tushuntirish va Mantiq:
`Future.value` allaqachon hisoblangan tayyor qiymatni asinxron `Future` turiga o'rab beradi.

## Ishlash natijasi:
```text
Keshdagi tezkor ma'lumot
```

# 707-Topshiriq: Future.error darhol xatolik qaytarish

## Topshiriq sharti:
Shart bajarilmaganda asinxron xatolikni `Future.error` orqali darhol uzating.

## Yechim (Dart kodi):
```dart
Future<int> hisobla(int a) {
  if (a < 0) {
    return Future.error(ArgumentError('Son manfiy bo\'lmasligi kerak'));
  }
  return Future.value(a * 2);
}

void main() async {
  try {
    await hisobla(-5);
  } catch (e) {
    print('Ushlangan asinxron xato: $e');
  }
}
```

## Tushuntirish va Mantiq:
`Future.error` xatolik holatini asinxron oqimga uzatadi va u `try-catch` orqali ushlanadi.

## Ishlash natijasi:
```text
Ushlangan asinxron xato: Invalid argument(s): Son manfiy bo'lmasligi kerak
```

# 708-Topshiriq: Future.wait bilan parallel so'rovlarni kutish

## Topshiriq sharti:
Uchta mustaqil so'rovni bir vaqtda parallel yuborib, barchasi tugashini `Future.wait` bilan kuting.

## Yechim (Dart kodi):
```dart
Future<String> profilYuklash() async => 'Profil ma\'lumoti';
Future<String> xabarlarYuklash() async => 'Xabarlar ro\'yxati';
Future<String> balansYuklash() async => 'Hisob balansi: 500k';

void main() async {
  print('Barcha ma\'lumotlar parallel yuklanmoqda...');
  var natijalar = await Future.wait([
    profilYuklash(),
    xabarlarYuklash(),
    balansYuklash(),
  ]);

  for (var res in natijalar) {
    print('- $res');
  }
}
```

## Tushuntirish va Mantiq:
`Future.wait` barcha asinxron operatsiyalarni parallel ishga tushiradi va umumiy bajarilish vaqtini keskin qisqartiradi.

## Ishlash natijasi:
```text
Barcha ma'lumotlar parallel yuklanmoqda...
- Profil ma'lumoti
- Xabarlar ro'yxati
- Hisob balansi: 500k
```

# 709-Topshiriq: Future.any bilan eng tezkor serverni tanlash

## Topshiriq sharti:
Bir nechta serverdan qaysi biri birinchi javob bersa o'shani tanlab oluvchi `Future.any` ni qo'llang.

## Yechim (Dart kodi):
```dart
Future<String> serverA() async {
  await Future.delayed(Duration(milliseconds: 100));
  return 'Server A (Sekin)';
}

Future<String> serverB() async {
  await Future.delayed(Duration(milliseconds: 20));
  return 'Server B (Tezkor)';
}

void main() async {
  var engTezkor = await Future.any([serverA(), serverB()]);
  print('Birinchi yetib kelgan javob: $engTezkor');
}
```

## Tushuntirish va Mantiq:
`Future.any` birinchi muvaffaqiyatli yoki muvaffaqiyatsiz yakunlangan Future qiymatini qaytaradi.

## Ishlash natijasi:
```text
Birinchi yetib kelgan javob: Server B (Tezkor)
```

# 710-Topshiriq: Future.forEach bilan ketma-ket asinxron bajarish

## Topshiriq sharti:
Ro'yxatdagi elementlarni birin-ketin navbat bilan asinxron yuklashni `Future.forEach` orqali tuzing.

## Yechim (Dart kodi):
```dart
void main() async {
  var fayllar = ['fayl1.dart', 'fayl2.dart', 'fayl3.dart'];

  await Future.forEach(fayllar, (fayl) async {
    print('Yuklanmoqda: $fayl');
  });

  print('Barcha fayllar ketma-ket yuklandi.');
}
```

## Tushuntirish va Mantiq:
`Future.forEach` har bir element uchun asinxron funksiyani oldingisi tugagandan keyingina chaqiradi.

## Ishlash natijasi:
```text
Yuklanmoqda: fayl1.dart
Yuklanmoqda: fayl2.dart
Yuklanmoqda: fayl3.dart
Barcha fayllar ketma-ket yuklandi.
```

# 711-Topshiriq: Oddiy for sikli ichida await qilish

## Topshiriq sharti:
Massiv elementlarini bittalab asinxron qayta ishlash uchun `for` va `await` dan foydalaning.

## Yechim (Dart kodi):
```dart
Future<void> qadam(int n) async {
  print('Qadam $n bajarildi');
}

void main() async {
  for (int i = 1; i <= 3; i++) {
    await qadam(i);
  }
}
```

## Tushuntirish va Mantiq:
`for` sikli ichidagi `await` amallarning qat'iy navbat bilan ketma-ket bajarilishini ta'minlaydi.

## Ishlash natijasi:
```text
Qadam 1 bajarildi
Qadam 2 bajarildi
Qadam 3 bajarildi
```

# 712-Topshiriq: Completer<T> asoslari

## Topshiriq sharti:
Asinxron `Future` ni dasturchi xohlagan paytda qo'lda `complete()` orqali yakunlashni ko'rsating.

## Yechim (Dart kodi):
```dart
import 'dart:async';

Future<String> maxsusOperatsiya() {
  var completer = Completer<String>();

  // Tashqi voqea sodir bo'lganda
  Future.delayed(Duration(milliseconds: 20), () {
    completer.complete('Operatsiya muvaffaqiyatli yakunlandi');
  });

  return completer.future;
}

void main() async {
  var natija = await maxsusOperatsiya();
  print(natija);
}
```

## Tushuntirish va Mantiq:
`Completer` tashqi callbacklarni yoki past darajadagi API larni zamonaviy `Future` ga o'rash uchun xizmat qiladi.

## Ishlash natijasi:
```text
Operatsiya muvaffaqiyatli yakunlandi
```

# 713-Topshiriq: Completer bilan hodisani bir martalik kutish

## Topshiriq sharti:
Tugma bosilguncha yoki voqea yuz berguncha kutib turuvchi asinxron darvoza (Gate) tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:async';

class Darvoza {
  final Completer<void> _ochildi = Completer<void>();

  Future<void> kutish() => _ochildi.future;
  void ochish() => _ochildi.complete();
}

void main() async {
  var d = Darvoza();

  Future(() {
    print('Darvoza ochilmoqda...');
    d.ochish();
  });

  print('Darvoza oldida kutish...');
  await d.kutish();
  print('Darvoza ochildi, o\'tish mumkin!');
}
```

## Tushuntirish va Mantiq:
`Completer` yordamida dastur oqimini ma'lum shart bajarilguniga qadar qulay to'xtatib turish mumkin.

## Ishlash natijasi:
```text
Darvoza oldida kutish...
Darvoza ochilmoqda...
Darvoza ochildi, o'tish mumkin!
```

# 714-Topshiriq: Asinxron funksiyada try-catch bilan xatolik ushlash

## Topshiriq sharti:
`await` qilingan funksiyadagi nosozlikni oddiy sinxron kod kabi `try-catch` ichida ushlang.

## Yechim (Dart kodi):
```dart
Future<void> xavfliTarmoq() async {
  throw Exception('503 Service Unavailable');
}

void main() async {
  try {
    await xavfliTarmoq();
  } catch (e) {
    print('Asinxron xato ushlandi: $e');
  }
}
```

## Tushuntirish va Mantiq:
Dartda `async/await` asinxron xatoliklarni xuddi sinxron xatolar kabi an'anaviy `try-catch` bilan boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Asinxron xato ushlandi: Exception: 503 Service Unavailable
```

# 715-Topshiriq: Future.timeout bilan kutish muddatini cheklash

## Topshiriq sharti:
Javob belgilangan vaqt ichida kelmasa `timeout` orqali zaxira qiymat qaytarishni ko'rsating.

## Yechim (Dart kodi):
```dart
Future<String> sekinServer() async {
  await Future.delayed(Duration(milliseconds: 50));
  return 'Javob';
}

void main() async {
  String natija = await sekinServer().timeout(
    Duration(milliseconds: 20),
    onTimeout: () => 'Zaxira javob (Timeout bo\'ldi)',
  );

  print('Natija: $natija');
}
```

## Tushuntirish va Mantiq:
`.timeout(duration, onTimeout: ...)` xato tashlamasdan, zaxira qiymat (fallback) berishga ham imkon beradi.

## Ishlash natijasi:
```text
Natija: Zaxira javob (Timeout bo'ldi)
```

# 716-Topshiriq: Parallel va Ketma-ket ijro tezligi taqqosi

## Topshiriq sharti:
Ketma-ket 3 marta kutish bilan `Future.wait` orqali parallel kutish tezligini ko'rsating.

## Yechim (Dart kodi):
```dart
Future<void> ish() async => Future.delayed(Duration(milliseconds: 10));

void main() async {
  // Ketma-ket: 10 + 10 + 10 = 30 ms
  await ish();
  await ish();
  await ish();
  print('Ketma-ket bajarildi.');

  // Parallel: hammasi 10 ms ichida
  await Future.wait([ish(), ish(), ish()]);
  print('Parallel bajarildi.');
}
```

## Tushuntirish va Mantiq:
Mustaqil asinxron amallarni `Future.wait` bilan parallel bajarish tezlikni keskin oshiradi.

## Ishlash natijasi:
```text
Ketma-ket bajarildi.
Parallel bajarildi.
```

# 717-Topshiriq: Asinxron Kesh (Async Memoization)

## Topshiriq sharti:
Og'ir asinxron so'rov natijasini keshlab, keyingi chaqiruvlarda darhol tayyor `Future` ni qaytaruvchi klass tuzing.

## Yechim (Dart kodi):
```dart
class AsinxronKesh<T> {
  Future<T>? _keshlangan;

  Future<T> olish(Future<T> Function() yuklagich) {
    _keshlangan ??= yuklagich();
    return _keshlangan!;
  }
}

void main() async {
  var kesh = AsinxronKesh<String>();

  Future<String> yuklash() async {
    print('Serverga qimmat so\'rov ketdi...');
    return 'Server ma\'lumoti';
  }

  print(await kesh.olish(yuklash));
  print(await kesh.olish(yuklash)); // Qayta so'rov ketmaydi
}
```

## Tushuntirish va Mantiq:
Asinxron kesh bir xil ma'lumot uchun tarmoqqa bir necha marta ortiqcha so'rov yuborilishining oldini oladi.

## Ishlash natijasi:
```text
Serverga qimmat so'rov ketdi...
Server ma'lumoti
Server ma'lumoti
```

# 718-Topshiriq: Asinxron Semafor (Bir vaqtda N ta so'rov)

## Topshiriq sharti:
Bir vaqtning o'zida maksimal 2 ta operatsiya parallel ishlashiga ruxsat beruvchi semafor tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:async';

class Semafor {
  final int maxParallel;
  int _joriy = 0;
  final List<Completer<void>> _navbat = [];

  Semafor(this.maxParallel);

  Future<void> olish() async {
    if (_joriy < maxParallel) {
      _joriy++;
      return;
    }
    var completer = Completer<void>();
    _navbat.add(completer);
    await completer.future;
  }

  void qoyibYuborish() {
    if (_navbat.isNotEmpty) {
      var keyingi = _navbat.removeAt(0);
      keyingi.complete();
    } else {
      _joriy--;
    }
  }
}

void main() async {
  var sem = Semafor(2);
  print('Semafor yaratildi (max: 2)');
  await sem.olish();
  print('Birinchi slot olindi');
  await sem.olish();
  print('Ikkinchi slot olindi');
  sem.qoyibYuborish();
  print('Bitta slot bo\'shatildi');
}
```

## Tushuntirish va Mantiq:
Semafor apparat resurslarini yoki tarmoq ulanishlarini haddan tashqari ko'p parallel yuklamalardan asraydi.

## Ishlash natijasi:
```text
Semafor yaratildi (max: 2)
Birinchi slot olindi
Ikkinchi slot olindi
Bitta slot bo'shatildi
```

# 719-Topshiriq: Asinxron Vazifalar Navbati (Async Task Queue)

## Topshiriq sharti:
Vazifalarni navbatga qabul qilib, ularni birin-ketin navbat bilan bajaruvchi asinxron navbat tuzing.

## Yechim (Dart kodi):
```dart
class AsinxronNavbat {
  Future<void> _oxirgi = Future.value();

  Future<T> qoshish<T>(Future<T> Function() vazifa) {
    var keyingi = _oxirgi.then((_) => vazifa());
    _oxirgi = keyingi.catchError((_) {});
    return keyingi;
  }
}

void main() async {
  var queue = AsinxronNavbat();

  queue.qoshish(() async => print('Vazifa 1'));
  queue.qoshish(() async => print('Vazifa 2'));
  await queue.qoshish(() async => print('Vazifa 3'));
}
```

## Tushuntirish va Mantiq:
Asinxron navbat amallarning bir-biriga xalaqit bermasdan, qat'iy navbatda bajarilishini ta'minlaydi.

## Ishlash natijasi:
```text
Vazifa 1
Vazifa 2
Vazifa 3
```

# 720-Topshiriq: Asinxron Yuklash Holati Menejeri

## Topshiriq sharti:
Yuklanish boshlanganda va tugaganda holat bayrog'ini boshqaruvchi klass tuzing.

## Yechim (Dart kodi):
```dart
class YuklashMenejeri {
  bool yuklanmoqdami = false;

  Future<T> bajar<T>(Future<T> Function() amal) async {
    yuklanmoqdami = true;
    print('[HOLAT]: Yuklanmoqda...');
    try {
      return await amal();
    } finally {
      yuklanmoqdami = false;
      print('[HOLAT]: Tugallandi.');
    }
  }
}

void main() async {
  var m = YuklashMenejeri();
  var res = await m.bajar(() async => 'Foydalanuvchi ma\'lumotlari');
  print('Natija: $res');
}
```

## Tushuntirish va Mantiq:
Flutter UI da aylanuvchi progress indikatorlarini (CircularProgressIndicator) boshqarishda bu naqsh qo'llaniladi.

## Ishlash natijasi:
```text
[HOLAT]: Yuklanmoqda...
[HOLAT]: Tugallandi.
Natija: Foydalanuvchi ma'lumotlari
```

# 721-Topshiriq: Asinxron Polling mexanizmi

## Topshiriq sharti:
Serverdagi topshiriq tayyor bo'lguniga qadar har N vaqtda so'rov yuboruvchi asinxron tekshiruv tuzing.

## Yechim (Dart kodi):
```dart
Future<String> pollingTekshiruv({int maxUrinish = 3}) async {
  int urinish = 0;
  while (urinish < maxUrinish) {
    urinish++;
    print('$urinish-tekshiruv...');
    if (urinish == 2) {
      return 'Topshiriq tayyor!';
    }
    await Future.delayed(Duration(milliseconds: 10));
  }
  throw Exception('Muddati tugadi');
}

void main() async {
  var natija = await pollingTekshiruv();
  print('Natija: $natija');
}
```

## Tushuntirish va Mantiq:
Polling fonda uzoq ishlaydigan vazifalarning holatini muntazam so'rab turish uchun xizmat qiladi.

## Ishlash natijasi:
```text
1-tekshiruv...
2-tekshiruv...
Natija: Topshiriq tayyor!
```

# 722-Topshiriq: Asinxron ma'lumotlarni qismlab (batch) yuklash

## Topshiriq sharti:
Katta ro'yxatdagi ID lar bo'yicha ma'lumotlarni 2 tadan guruhlab yuklovchi dastur yozing.

## Yechim (Dart kodi):
```dart
Future<List<String>> batchYuklash(List<int> ids) async {
  List<String> natijalar = [];
  for (int i = 0; i < ids.length; i += 2) {
    var guruh = ids.sublist(i, (i + 2 < ids.length) ? i + 2 : ids.length);
    print('Guruh yuklanmoqda: $guruh');
    natijalar.addAll(guruh.map((id) => 'Ma\'lumot #$id'));
  }
  return natijalar;
}

void main() async {
  var res = await batchYuklash([1, 2, 3, 4, 5]);
  print('Jami: ${res.length} ta');
}
```

## Tushuntirish va Mantiq:
Batch yuklash orqali serverga minglab alohida so'rovlar o'rniga kichik to'plamlar yuboriladi.

## Ishlash natijasi:
```text
Guruh yuklanmoqda: [1, 2]
Guruh yuklanmoqda: [3, 4]
Guruh yuklanmoqda: [5]
Jami: 5 ta
```

# 723-Topshiriq: Asinxron Pipeline (Bosqichma-bosqich o'zgartirish)

## Topshiriq sharti:
Kelayotgan matnni ketma-ket asinxron bosqichlardan o'tkazuvchi pipeline tuzing.

## Yechim (Dart kodi):
```dart
Future<String> bosqich1(String s) async => s.trim();
Future<String> bosqich2(String s) async => s.toUpperCase();
Future<String> bosqich3(String s) async => '>>> $s <<<';

void main() async {
  String xom = '   salom asinxron dunyo   ';
  String res = await bosqich1(xom).then(bosqich2).then(bosqich3);

  print('Pipeline natijasi: $res');
}
```

## Tushuntirish va Mantiq:
Asinxron pipeline ma'lumotlarni turli xizmatlar orqali ketma-ket qayta ishlashga imkon beradi.

## Ishlash natijasi:
```text
Pipeline natijasi: >>> SALOM ASINXRON DUNYO <<<
```

# 724-Topshiriq: Stale-While-Revalidate asinxron yangilash

## Topshiriq sharti:
Avval keshdagi eski ma'lumotni darhol qaytarib, orqa fonda serverdan yangilab qo'yuvchi naqsh tuzing.

## Yechim (Dart kodi):
```dart
class SwrKesh {
  String _oxirgi = 'Eski kesh ma\'lumoti';

  String olish() {
    _orqaFondaYangilash();
    return _oxirgi;
  }

  void _orqaFondaYangilash() {
    Future.delayed(Duration(milliseconds: 10), () {
      _oxirgi = 'Yangi server ma\'lumoti';
      print('[FONDA]: Kesh yangilandi!');
    });
  }
}

void main() async {
  var swr = SwrKesh();
  print('1-olish: ${swr.olish()}');
  await Future.delayed(Duration(milliseconds: 20));
  print('2-olish: ${swr.olish()}');
}
```

## Tushuntirish va Mantiq:
Stale-While-Revalidate foydalanuvchiga hech qanday kechikishsiz keshdagi ma'lumotni ko'rsatib, orqa fonda yangilaydi.

## Ishlash natijasi:
```text
1-olish: Eski kesh ma'lumoti
[FONDA]: Kesh yangilandi!
2-olish: Yangi server ma'lumoti
```

# 725-Topshiriq: Amaliy: BitNet AI Modelini Asinxron Yuklash

## Topshiriq sharti:
1-bit AI modelining og'irliklarini fayldan xotiraga asinxron yuklovchi va tayyorlik holatini qaytaruvchi dastur yozing.

## Yechim (Dart kodi):
```dart
class BitNetModel {
  final String modelNomi;
  final int parametrlarSoni;

  BitNetModel(this.modelNomi, this.parametrlarSoni);
}

Future<BitNetModel> loadBitNetModelAsync(String path) async {
  print('Model xotiraga yuklanmoqda: $path...');
  // Asinxron I/O yuklash simulyatsiyasi
  await Future.delayed(Duration(milliseconds: 50));
  print('Ternar og\'irliklar va RMSNorm parametrlar yuklandi.');
  return BitNetModel('BitNet-b1.58-100M-Uzbek', 100000000);
}

void main() async {
  var model = await loadBitNetModelAsync('assets/models/bitnet_uz.bin');
  print('Model tayyor: ${model.modelNomi} (${model.parametrlarSoni ~/ 1000000}M parametr)');
}
```

## Tushuntirish va Mantiq:
Mobil va IoT qurilmalarda on-device LLM modelining og'irliklarini asinxron yuklash UI qotib qolishining (ANR) oldini oladi.

## Ishlash natijasi:
```text
Model xotiraga yuklanmoqda: assets/models/bitnet_uz.bin...
Ternar og'irliklar va RMSNorm parametrlar yuklandi.
Model tayyor: BitNet-b1.58-100M-Uzbek (100M parametr)
```

# 726-Topshiriq: Future.doWhile asinxron sikli

## Topshiriq sharti:
Shart bajarilguniga qadar asinxron amallarni qayta bajaruvchi `Future.doWhile` dan foydalaning.

## Yechim (Dart kodi):
```dart
void main() async {
  int sanoq = 0;

  await Future.doWhile(() async {
    sanoq++;
    print('Sikl qadami: $sanoq');
    await Future.delayed(Duration(milliseconds: 10));
    return sanoq < 3; // true bo'lsa sikl davom etadi
  });

  print('doWhile sikli tugadi.');
}
```

## Tushuntirish va Mantiq:
`Future.doWhile` asinxron sikllarni rekursiyasiz va oqimni to'xtatmasdan bajarish uchun maxsus vositadir.

## Ishlash natijasi:
```text
Sikl qadami: 1
Sikl qadami: 2
Sikl qadami: 3
doWhile sikli tugadi.
```

# 727-Topshiriq: Asinxron Rekursiya (Async Recursion)

## Topshiriq sharti:
Daraxtsimon yoki qismlarga bo'lingan ma'lumotlarni asinxron rekursiv usulda chuqurlikka qarab tahlil qiling.

## Yechim (Dart kodi):
```dart
Future<int> asinxronFaktorial(int n) async {
  if (n <= 1) return 1;
  int oldingi = await asinxronFaktorial(n - 1);
  return n * oldingi;
}

void main() async {
  int f = await asinxronFaktorial(5);
  print('5! = $f');
}
```

## Tushuntirish va Mantiq:
Asinxron rekursiya har bir qadamda `await` orqali oraliq natijalarni kutib, yakuniy natijani hisoblaydi.

## Ishlash natijasi:
```text
5! = 120
```

# 728-Topshiriq: Asinxron Muteks (Async Lock)

## Topshiriq sharti:
Kritik qismga bir vaqtda faqat bitta asinxron chaqiruv kirishini ta'minlovchi asinxron qulf tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:async';

class AsinxronQulf {
  Completer<void>? _joriy;

  Future<void> qulflash() async {
    while (_joriy != null) {
      await _joriy!.future;
    }
    _joriy = Completer<void>();
  }

  void ochish() {
    var c = _joriy;
    _joriy = null;
    c?.complete();
  }
}

void main() async {
  var lock = AsinxronQulf();
  int balans = 100;

  Future<void> pulYechish(int summa) async {
    await lock.qulflash();
    try {
      int temp = balans;
      await Future.delayed(Duration(milliseconds: 10));
      balans = temp - summa;
      print('Yechildi: $summa, Qoldi: $balans');
    } finally {
      lock.ochish();
    }
  }

  await Future.wait([pulYechish(30), pulYechish(20)]);
}
```

## Tushuntirish va Mantiq:
Asinxron qulf (mutex) asinxron kodda 'race condition' xatolarining oldini oladi.

## Ishlash natijasi:
```text
Yechildi: 30, Qoldi: 70
Yechildi: 20, Qoldi: 50
```

# 729-Topshiriq: Asinxron Bekor Qilinuvchi Vazifa (CancellationToken)

## Topshiriq sharti:
Foydalanuvchi orqaga qaytganda uzoq ketayotgan operatsiyani bekor qilish mexanizmini tuzing.

## Yechim (Dart kodi):
```dart
class BekorQilishBelgisi {
  bool bekorQilindimi = false;
  void bekorQilish() => bekorQilindimi = true;
}

Future<void> yuklash(BekorQilishBelgisi token) async {
  for (int i = 1; i <= 5; i++) {
    if (token.bekorQilindimi) {
      print('Operatsiya bekor qilindi!');
      return;
    }
    print('Yuklanmoqda: $i/5');
    await Future.delayed(Duration(milliseconds: 10));
  }
}

void main() async {
  var token = BekorQilishBelgisi();
  Future.delayed(Duration(milliseconds: 25), () => token.bekorQilish());

  await yuklash(token);
}
```

## Tushuntirish va Mantiq:
CancellationToken uzoq asinxron jarayonlarni istalgan daqiqada xavfsiz to'xtatish uchun xizmat qiladi.

## Ishlash natijasi:
```text
Yuklanmoqda: 1/5
Yuklanmoqda: 2/5
Yuklanmoqda: 3/5
Operatsiya bekor qilindi!
```

# 730-Topshiriq: Asinxron Debounce mexanizmi

## Topshiriq sharti:
Qidiruv maydonida har bir harf terilganda emas, faqat yozish to'xtaganidan 50ms o'tgach qidiruvni ishga tushiring.

## Yechim (Dart kodi):
```dart
import 'dart:async';

class Debouncer {
  final Duration kechikish;
  Timer? _timer;

  Debouncer(this.kechikish);

  void chaqir(void Function() harakat) {
    _timer?.cancel();
    _timer = Timer(kechikish, harakat);
  }
}

void main() async {
  var debouncer = Debouncer(Duration(milliseconds: 30));

  print('Foydalanuvchi tez yozmoqda: "d", "da", "dar", "dart"');
  debouncer.chaqir(() => print('Qidirilmoqda: "d"'));
  debouncer.chaqir(() => print('Qidirilmoqda: "da"'));
  debouncer.chaqir(() => print('Qidirilmoqda: "dart"'));

  await Future.delayed(Duration(milliseconds: 50));
}
```

## Tushuntirish va Mantiq:
Debounce qidiruv va filtr kiritish maydonlarida serverga yuboriladigan ortiqcha so'rovlarni 90% ga kamaytiradi.

## Ishlash natijasi:
```text
Foydalanuvchi tez yozmoqda: "d", "da", "dar", "dart"
Qidirilmoqda: "dart"

```

# 731-Topshiriq: Asinxron Throttle (Ma'lum oraliqda faqat bitta chaqiruv)

## Topshiriq sharti:
Tugma tinimsiz bosilganda ham metod har 50 millisekundda faqat bir marta ishlashini kafolatlang.

## Yechim (Dart kodi):
```dart
class Throttler {
  final Duration interval;
  bool _bloklangan = false;

  Throttler(this.interval);

  void bajar(void Function() harakat) {
    if (_bloklangan) return;
    harakat();
    _bloklangan = true;
    Future.delayed(interval, () => _bloklangan = false);
  }
}

void main() {
  var t = Throttler(Duration(milliseconds: 50));

  t.bajar(() => print('1-bosish qabul qilindi'));
  t.bajar(() => print('2-bosish bloklandi'));
  t.bajar(() => print('3-bosish bloklandi'));
}
```

## Tushuntirish va Mantiq:
Throttle xarid qilish yoki to'lov tugmalarini takroriy bosishdan saqlash uchun ishlatiladi.

## Ishlash natijasi:
```text
1-bosish qabul qilindi
```

# 732-Topshiriq: Asinxron CountdownLatch (Bir nechta vazifani kutish)

## Topshiriq sharti:
Belgilangan N ta mustaqil asinxron xizmat ishga tushib bo'lgach asosiy tizimni ochuvchi Latch tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:async';

class CountdownLatch {
  int _sanoq;
  final Completer<void> _completer = Completer<void>();

  CountdownLatch(this._sanoq);

  void sanash() {
    _sanoq--;
    if (_sanoq <= 0 && !_completer.isCompleted) {
      _completer.complete();
    }
  }

  Future<void> kutish() => _completer.future;
}

void main() async {
  var latch = CountdownLatch(2);

  Future(() {
    print('Baza ulandi.');
    latch.sanash();
  });

  Future(() {
    print('Kesh tayyor.');
    latch.sanash();
  });

  await latch.kutish();
  print('Barcha xizmatlar tayyor: Tizim ishga tushdi!');
}
```

## Tushuntirish va Mantiq:
CountdownLatch parallel modullarning to'liq tayyor bo'lishini muvofiqlashtiruvchi klassik sinxronizatsiya vositasidir.

## Ishlash natijasi:
```text
Baza ulandi.
Kesh tayyor.
Barcha xizmatlar tayyor: Tizim ishga tushdi!
```

# 733-Topshiriq: Asinxron Retry with Jitter (Tasodifiy kechikish)

## Topshiriq sharti:
Qayta urinish vaqtiga tasodifiy kichik oraliq (jitter) qo'shib server to'qnashuvlarining oldini oling.

## Yechim (Dart kodi):
```dart
import 'dart:math';

Future<void> retryWithJitter(int urinish) async {
  var random = Random();
  int asosiyVaqt = 1 << urinish; // 1, 2, 4...
  int jitter = random.nextInt(10); // 0..9 ms tasodifiy qo'shimcha
  int jamiKutish = asosiyVaqt * 10 + jitter;

  print('$urinish-urinish: $jamiKutish ms kutish belgilandi.');
  await Future.delayed(Duration(milliseconds: 5));
}

void main() async {
  for (int i = 0; i < 3; i++) {
    await retryWithJitter(i);
  }
}
```

## Tushuntirish va Mantiq:
Jitter yuz minglab qurilmalarning bir xil soniyada bir vaqtda qayta serverga yopirilishini (Thundering Herd) to'xtatadi.

## Ishlash natijasi:
```text
0-urinish: 14 ms kutish belgilandi.
1-urinish: 27 ms kutish belgilandi.
2-urinish: 42 ms kutish belgilandi.
```

# 734-Topshiriq: Asinxron Healthcheck (Tizim salomatligi monitoringi)

## Topshiriq sharti:
Server va bazani muntazam tekshirib, sog'lom holatni qaytaruvchi asinxron monitoring tuzing.

## Yechim (Dart kodi):
```dart
Future<Map<String, bool>> healthCheck() async {
  var db = await Future.value(true);
  var cache = await Future.value(true);

  return {'baza': db, 'kesh': cache};
}

void main() async {
  var holat = await healthCheck();
  print('Tizim salomatligi: $holat');
}
```

## Tushuntirish va Mantiq:
Microservice va backend arxitekturalarida healthcheck so'rovlari yuklama taqsimlagichlar (Load Balancer) uchun zarur.

## Ishlash natijasi:
```text
Tizim salomatligi: {baza: true, kesh: true}
```

# 735-Topshiriq: Asinxron Worker Pool simulyatsiyasi

## Topshiriq sharti:
Cheklangan sondagi ishchilar (Workers) yordamida ko'p sonli vazifalarni navbat bilan taqsimlang.

## Yechim (Dart kodi):
```dart
Future<void> worker(int id, List<String> vazifalar) async {
  while (vazifalar.isNotEmpty) {
    String ish = vazifalar.removeAt(0);
    print('Ishchi #$id: "$ish" ni bajardi');
    await Future.delayed(Duration(milliseconds: 5));
  }
}

void main() async {
  List<String> navbat = ['Vazifa A', 'Vazifa B', 'Vazifa C', 'Vazifa D'];

  await Future.wait([
    worker(1, navbat),
    worker(2, navbat),
  ]);

  print('Barcha vazifalar ishchilar tomonidan yakunlandi.');
}
```

## Tushuntirish va Mantiq:
Worker Pool fondagi og'ir vazifalarni cheklangan oqimlarda samarali taqsimlash imkonini beradi.

## Ishlash natijasi:
```text
Ishchi #1: "Vazifa A" ni bajardi
Ishchi #2: "Vazifa B" ni bajardi
Ishchi #1: "Vazifa C" ni bajardi
Ishchi #2: "Vazifa D" ni bajardi
Barcha vazifalar ishchilar tomonidan yakunlandi.
```

# 736-Topshiriq: Asinxron Generator va Future farqi

## Topshiriq sharti:
Bitta yakuniy qiymat qaytaruvchi `Future` bilan bir nechta qiymat uzatuvchi `async*` farqini ko'rsating.

## Yechim (Dart kodi):
```dart
Future<int> bittaQiymat() async {
  return 42;
}

Stream<int> birNechtaQiymat() async* {
  yield 1;
  yield 2;
  yield 3;
}

void main() async {
  print('Future natijasi: ${await bittaQiymat()}');

  print('Stream qiymatlari:');
  await for (var n in birNechtaQiymat()) {
    print('- $n');
  }
}
```

## Tushuntirish va Mantiq:
`Future` bitta asinxron natijani bildiradi, `Stream` esa vaqt davomida keluvchi qiymatlar ketma-ketligini taqdim etadi.

## Ishlash natijasi:
```text
Future natijasi: 42
Stream qiymatlari:
- 1
- 2
- 3
```

# 737-Topshiriq: Asinxron ma'lumotlarni oyna bo'yicha buferlash

## Topshiriq sharti:
Kelayotgan elementlarni vaqt oralig'i bo'yicha guruhlab chiqaruvchi bufer tuzing.

## Yechim (Dart kodi):
```dart
class AsinxronBufer {
  final List<String> _bufer = [];

  void qoshish(String xabar) => _bufer.add(xabar);

  Future<List<String>> oqizish() async {
    await Future.delayed(Duration(milliseconds: 10));
    var nusxa = List<String>.from(_bufer);
    _bufer.clear();
    return nusxa;
  }
}

void main() async {
  var b = AsinxronBufer();
  b.qoshish('Log 1');
  b.qoshish('Log 2');

  var paket = await b.oqizish();
  print('Chiqarilgan paket: $paket');
}
```

## Tushuntirish va Mantiq:
Telemetriya va loglarni bittalab emas, paketlab (batch) yuborish tarmoq yuklamasini kamaytiradi.

## Ishlash natijasi:
```text
Chiqarilgan paket: [Log 1, Log 2]
```

# 738-Topshiriq: Asinxron Tranzaksiya Kommiti

## Topshiriq sharti:
Asinxron qadamlar ketma-ketligini xavfsiz bajarib, xato yuz berganda to'xtatuvchi tranzaksiya tuzing.

## Yechim (Dart kodi):
```dart
Future<void> pulOtqazish(int summa) async {
  print('1. Asinxron balans tekshirilmoqda...');
  await Future.delayed(Duration(milliseconds: 5));
  print('2. Mablag\' yechildi.');
  await Future.delayed(Duration(milliseconds: 5));
  print('3. Qabul qiluvchiga qo\'shildi.');
  print('Tranzaksiya yakunlandi!');
}

void main() async {
  await pulOtqazish(50000);
}
```

## Tushuntirish va Mantiq:
Barcha qadamlar `await` bilan kafolatlangan holda bosqichma-bosqich bajariladi.

## Ishlash natijasi:
```text
1. Asinxron balans tekshirilmoqda...
2. Mablag' yechildi.
3. Qabul qiluvchiga qo'shildi.
Tranzaksiya yakunlandi!
```

# 739-Topshiriq: Asinxron Hesh hisoblash

## Topshiriq sharti:
Katta matnlar uchun fon rejimida asinxron hesh hisoblash simulyatsiyasini yozing.

## Yechim (Dart kodi):
```dart
Future<int> asinxronHash(String matn) async {
  return Future(() {
    return matn.codeUnits.fold(0, (h, c) => (h * 31 + c) & 0x7FFFFFFF);
  });
}

void main() async {
  int h = await asinxronHash('BitNet-b1.58-Dart');
  print('Asinxron xesh: $h');
}
```

## Tushuntirish va Mantiq:
Hisoblash yuklamasini `Future(() => ...)` orqali navbatga qo'yib asosiy oqim qotishining oldi olinadi.

## Ishlash natijasi:
```text
Asinxron xesh: 1118167814
```

# 740-Topshiriq: Asinxron Validatsiya zanjiri

## Topshiriq sharti:
Foydalanuvchi ma'lumotlarini bir nechta asinxron server tekshiruvlaridan o'tkazing.

## Yechim (Dart kodi):
```dart
Future<bool> emailMavjudmi(String email) async => false;
Future<bool> spamEmasmi(String email) async => true;

Future<bool> tekshirEmail(String email) async {
  var band = await emailMavjudmi(email);
  if (band) return false;
  var toza = await spamEmasmi(email);
  return toza;
}

void main() async {
  bool ok = await tekshirEmail('info@uzbekai.uz');
  print('Email ro\'yxatdan o\'tishga yaroqlimi: $ok');
}
```

## Tushuntirish va Mantiq:
Bir nechta asinxron tekshiruvlar mantiqiy ketma-ketlikda xavfsiz bog'lanadi.

## Ishlash natijasi:
```text
Email ro'yxatdan o'tishga yaroqlimi: true
```

# 741-Topshiriq: Asinxron Webhook yuboruvchisi

## Topshiriq sharti:
Tashqi tizimga hodisa haqida asinxron bildirishnoma yuboruvchi dastur yozing.

## Yechim (Dart kodi):
```dart
Future<void> webhookYuborish(String url, Map<String, dynamic> voqea) async {
  print('Webhook yuborilmoqda: $url');
  await Future.delayed(Duration(milliseconds: 10));
  print('Webhook yetkazildi: ${voqea['nomi']}');
}

void main() async {
  await webhookYuborish('https://webhook.site/test', {'nomi': 'TOLOV_QABUL_QILINDI'});
}
```

## Tushuntirish va Mantiq:
Webhooklar tizimlararo integratsiyada voqealarni asinxron yetkazish standarti hisoblanadi.

## Ishlash natijasi:
```text
Webhook yuborilmoqda: https://webhook.site/test
Webhook yetkazildi: TOLOV_QABUL_QILINDI
```

# 742-Topshiriq: Asinxron Event Sourcing modeli

## Topshiriq sharti:
Hodisalar ro'yxatini asinxron o'qib joriy holatni qayta tiklashni ko'rsating.

## Yechim (Dart kodi):
```dart
Future<int> hisobniTiklash(List<int> tranzaksiyalar) async {
  int balans = 0;
  for (var t in tranzaksiyalar) {
    balans += t;
    await Future.delayed(Duration(milliseconds: 2));
  }
  return balans;
}

void main() async {
  var tarix = [1000, -200, 500, -100];
  int qoldiq = await hisobniTiklash(tarix);
  print('Tiklagan yakuniy balans: $qoldiq');
}
```

## Tushuntirish va Mantiq:
Event Sourcing hodisalar tarixini qayta ijro etish orqali aniq holatni tiklash imkonini beradi.

## Ishlash natijasi:
```text
Tiklagan yakuniy balans: 1200
```

# 743-Topshiriq: Asinxron Xotira Kalit-Qiymat Ombori (Async KV Store)

## Topshiriq sharti:
Baza kabi asinxron `set` va `get` metodlariga ega xotira omborini tuzing.

## Yechim (Dart kodi):
```dart
class AsinxronOmbor {
  final Map<String, String> _map = {};

  Future<void> set(String k, String v) async {
    _map[k] = v;
  }

  Future<String?> get(String k) async => _map[k];
}

void main() async {
  var db = AsinxronOmbor();
  await db.set('model', 'BitNet-1bit');
  var m = await db.get('model');

  print('Ombordan olindi: $m');
}
```

## Tushuntirish va Mantiq:
Asinxron KV interfeysi kelajakda kodni o'zgartirmasdan haqiqiy SQLite yoki Redis ga ulashga zamin yaratadi.

## Ishlash natijasi:
```text
Ombordan olindi: BitNet-1bit
```

# 744-Topshiriq: Asinxron Tezlik Cheklovchi (Rate Limiter - Token Bucket)

## Topshiriq sharti:
Sekundiga ruxsat berilgan so'rovlar sonini tokenlar chelagi orqali cheklovchi sinf tuzing.

## Yechim (Dart kodi):
```dart
class RateLimiter {
  int tokenlar = 2;

  Future<bool> ruxsatSora() async {
    if (tokenlar > 0) {
      tokenlar--;
      return true;
    }
    return false;
  }
}

void main() async {
  var limiter = RateLimiter();
  print('1-so\'rov: ${await limiter.ruxsatSora()}');
  print('2-so\'rov: ${await limiter.ruxsatSora()}');
  print('3-so\'rov: ${await limiter.ruxsatSora()}'); // Limitdan oshdi
}
```

## Tushuntirish va Mantiq:
Rate limiter API serverlarini haddan ortiq so'rovlar yuklamasidan (DDoS) asraydi.

## Ishlash natijasi:
```text
1-so'rov: true
2-so'rov: true
3-so'rov: false
```

# 745-Topshiriq: Asinxron Log yozuvchisi va Flush mexanizmi

## Topshiriq sharti:
Xabarlarni buferga yig'ib, `flush()` chaqirilganda asinxron diskka yozuvchi klass tuzing.

## Yechim (Dart kodi):
```dart
class AsinxronLogger {
  final List<String> _bufer = [];

  void yozish(String msg) => _bufer.add(msg);

  Future<void> flush() async {
    print('Diskka asinxron yozilmoqda (${_bufer.length} ta xabar)...');
    await Future.delayed(Duration(milliseconds: 10));
    _bufer.clear();
    print('Flush yakunlandi.');
  }
}

void main() async {
  var log = AsinxronLogger();
  log.yozish('Tizim start oldi');
  log.yozish('Foydalanuvchi kirdi');

  await log.flush();
}
```

## Tushuntirish va Mantiq:
I/O amallarini guruhlab `flush` qilish dasturning umumiy unumdorligini oshiradi.

## Ishlash natijasi:
```text
Diskka asinxron yozilmoqda (2 ta xabar)...
Flush yakunlandi.
```

# 746-Topshiriq: Asinxron Profiling (Vazifa vaqtini o'lchash)

## Topshiriq sharti:
Asinxron operatsiyaning qancha vaqt olganini aniq millisekundlarda o'lchovchi yordamchi funksiya yozing.

## Yechim (Dart kodi):
```dart
Future<(T, int)> vaqtniOlcha<T>(Future<T> Function() amal) async {
  var sw = Stopwatch()..start();
  T natija = await amal();
  sw.stop();
  return (natija, sw.elapsedMilliseconds);
}

void main() async {
  var (natija, ms) = await vaqtniOlcha(() async {
    await Future.delayed(Duration(milliseconds: 15));
    return 'Hisoblandi';
  });

  print('Natija: $natija (Vaqt: kamida ${ms}ms)');
}
```

## Tushuntirish va Mantiq:
Stopwatch yordamida asinxron amallarning kechikishini (latency) o'lchab tahlil qilish mumkin.

## Ishlash natijasi:
```text
Natija: Hisoblandi (Vaqt: kamida 15ms)
```

# 747-Topshiriq: Asinxron Read/Write Lock mexanizmi

## Topshiriq sharti:
Bir nechta o'qish amallariga parallel, lekin yozish amaliga faqat yakkama-yakka ruxsat bering.

## Yechim (Dart kodi):
```dart
class RwLock {
  int oquvchilar = 0;
  bool yozuvchiBormi = false;

  void oqishBoshlash() {
    if (yozuvchiBormi) throw StateError('Yozilmoqda, o\'qish mumkin emas');
    oquvchilar++;
  }

  void oqishTugadi() => oquvchilar--;

  void yozishBoshlash() {
    if (oquvchilar > 0 || yozuvchiBormi) throw StateError('Resurs band');
    yozuvchiBormi = true;
  }

  void yozishTugadi() => yozuvchiBormi = false;
}

void main() {
  var lock = RwLock();
  lock.oqishBoshlash();
  lock.oqishBoshlash();
  print('2 ta o\'quvchi parallel o\'qimoqda: oquvchilar=${lock.oquvchilar}');
  lock.oqishTugadi();
  lock.oqishTugadi();
  lock.yozishBoshlash();
  print('Endi yozuvchi eksklyuziv band qildi: yozuvchiBormi=${lock.yozuvchiBormi}');
  lock.yozishTugadi();
}
```

## Tushuntirish va Mantiq:
RW Lock ko'p o'qiladigan va kam o'zgartiriladigan ma'lumotlar omborida yuqori o'tkazuvchanlikni ta'minlaydi.

## Ishlash natijasi:
```text
2 ta o'quvchi parallel o'qimoqda: oquvchilar=2
Endi yozuvchi eksklyuziv band qildi: yozuvchiBormi=true
```

# 748-Topshiriq: Asinxron Resurslarni zanjirli yuklash

## Topshiriq sharti:
Konfiguratsiya -> Foydalanuvchi -> Sozlamalar zanjirini ketma-ket asinxron yuklang.

## Yechim (Dart kodi):
```dart
Future<String> configYuklash() async => 'Config_OK';
Future<String> authYuklash(String cfg) async => 'Auth_OK ($cfg)';
Future<String> sozlamaYuklash(String auth) async => 'Sozlamalar_OK ($auth)';

void main() async {
  var cfg = await configYuklash();
  var auth = await authYuklash(cfg);
  var soz = await sozlamaYuklash(auth);

  print('Barcha zanjir yuklandi: $soz');
}
```

## Tushuntirish va Mantiq:
Oldingi bosqich natijasiga bog'liq bo'lgan zanjirlar ketma-ket `await` qilinadi.

## Ishlash natijasi:
```text
Barcha zanjir yuklandi: Sozlamalar_OK (Auth_OK (Config_OK))
```

# 749-Topshiriq: Asinxron Dinamik Konfiguratsiya yangilash

## Topshiriq sharti:
Orqa fonda har doim so'nggi konfiguratsiyani yangilab turuvchi asinxron servis tuzing.

## Yechim (Dart kodi):
```dart
class DinamikConfig {
  String apiUrl = 'https://api.v1.uzbekai.uz';

  Future<void> yangilash() async {
    await Future.delayed(Duration(milliseconds: 5));
    apiUrl = 'https://api.v2.uzbekai.uz';
    print('Konfiguratsiya v2 ga yangilandi.');
  }
}

void main() async {
  var cfg = DinamikConfig();
  print('Boshlang\'ich: ${cfg.apiUrl}');
  await cfg.yangilash();
  print('Yangilangan: ${cfg.apiUrl}');
}
```

## Tushuntirish va Mantiq:
Ilovani to'xtatmasdan serverdan yangi sozlamalarni asinxron yuklab almashtirish (Hot Reload Config).

## Ishlash natijasi:
```text
Boshlang'ich: https://api.v1.uzbekai.uz
Konfiguratsiya v2 ga yangilandi.
Yangilangan: https://api.v2.uzbekai.uz
```

# 750-Topshiriq: Amaliy: BitNet Asinxron Tokenizer va Embedding Lookup

## Topshiriq sharti:
Prompt matnini asinxron tokenlarga ajratib, har bir token uchun embedding vektorlarini jadvaldan oluvchi dastur yozing.

## Yechim (Dart kodi):
```dart
class BitNetEmbedding {
  static final Map<String, List<double>> _vektorlar = {
    'ai': [0.1, -0.5, 0.8],
    'dart': [0.9, 0.2, -0.1],
    'model': [-0.3, 0.7, 0.4],
  };

  static Future<List<List<double>>> embedPromptAsync(String prompt) async {
    // Asinxron tokenizatsiya
    await Future.delayed(Duration(milliseconds: 10));
    var tokenlar = prompt.toLowerCase().split(' ');

    List<List<double>> embeddings = [];
    for (var token in tokenlar) {
      embeddings.add(_vektorlar[token] ?? [0.0, 0.0, 0.0]);
    }
    return embeddings;
  }
}

void main() async {
  var vectors = await BitNetEmbedding.embedPromptAsync('dart ai model');
  print('Olingan embedding vektorlar soni: ${vectors.length}');
  print('Birinchi token vektori: ${vectors[0]}');
}
```

## Tushuntirish va Mantiq:
BitNet LLM modeliga kiruvchi so'zlar avval tokenizatsiya qilinadi va asinxron embedding jadvalidan raqamli vektorlarga o'giriladi.

## Ishlash natijasi:
```text
Olingan embedding vektorlar soni: 3
Birinchi token vektori: [0.9, 0.2, -0.1]
```

