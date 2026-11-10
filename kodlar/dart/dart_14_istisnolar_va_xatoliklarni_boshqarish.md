# 651-Topshiriq: try-catch asoslari (Nolga bo'lish)

## Topshiriq sharti:
Kutilmagan arifmetik xatolik yuz berganda dastur to'xtab qolmasligi uchun `try-catch` dan foydalaning.

## Yechim (Dart kodi):
```dart
void main() {
  int a = 10;
  int b = 0;

  try {
    int natija = a ~/ b;
    print('Natija: $natija');
  } catch (e) {
    print('Xatolik ushlandi: $e');
  }

  print('Dastur odatiy tartibda davom etmoqda.');
}
```

## Tushuntirish va Mantiq:
`try` blokidagi xatolik `catch` ga o'tadi va dastur halokatga uchramasdan ishlashda davom etadi.

## Ishlash natijasi:
```text
Xatolik ushlandi: Unsupported operation: Result of integer division by zero cannot be represented as an integer
Dastur odatiy tartibda davom etmoqda.
```

# 652-Topshiriq: on ExceptionType bilan aniq istisnoni ushlash

## Topshiriq sharti:
Faqat `FormatException` xatosini ushlab, boshqa turdagi xatolarga tegmaydigan `on` blokini yozing.

## Yechim (Dart kodi):
```dart
void main() {
  String matn = '123a';

  try {
    int son = int.parse(matn);
    print('Son: $son');
  } on FormatException catch (e) {
    print('Format xatosi: Kiritilgan qiymat son emas! (${e.message})');
  }
}
```

## Tushuntirish va Mantiq:
`on Tur` orqali faqat ma'lum bir toifadagi istisnolar maxsus ushlanadi va ularga maqsadli ishlov beriladi.

## Ishlash natijasi:
```text
Format xatosi: Kiritilgan qiymat son emas! (Invalid radix-10 number)
```

# 653-Topshiriq: Bir nechta on bloklari va umumiy catch

## Topshiriq sharti:
Bir nechta har xil istisnolarni o'ziga xos tarzda va qolganlarini umumiy `catch` da boshqaring.

## Yechim (Dart kodi):
```dart
void tekshir(dynamic qiymat) {
  try {
    if (qiymat is String) {
      int.parse(qiymat);
    } else if (qiymat is int) {
      List<int> l = [1];
      print(l[qiymat]);
    }
  } on FormatException {
    print('Ushlandi: Noto\'g\'ri matn formati');
  } on RangeError {
    print('Ushlandi: Massiv chegarasidan chiqish');
  } catch (e) {
    print('Kutilmagan boshqa xato: $e');
  }
}

void main() {
  tekshir('abc');
  tekshir(5);
}
```

## Tushuntirish va Mantiq:
Yuqoridan pastga qarab mos keluvchi birinchi `on` bloki ishga tushadi, qolganlariga esa oxirgi `catch` ishlov beradi.

## Ishlash natijasi:
```text
Ushlandi: Noto'g'ri matn formati
Ushlandi: Massiv chegarasidan chiqish
```

# 654-Topshiriq: finally bloki va resurslarni tozalash

## Topshiriq sharti:
Xato bo'lishi yoki bo'lmasligidan qat'i nazar har doim bajarilishi kafolatlangan `finally` blokini qo'llang.

## Yechim (Dart kodi):
```dart
void faylBilanIshlash() {
  print('Fayl ochildi.');
  try {
    print('Faylga ma\'lumot yozilmoqda...');
    throw Exception('Disk to\'ldi xatosi');
  } catch (e) {
    print('Xatolik: $e');
  } finally {
    print('Har qanday holatda ham fayl yopildi!');
  }
}

void main() {
  faylBilanIshlash();
}
```

## Tushuntirish va Mantiq:
`finally` bloki xatolik yuz beradimi yoki muvaffaqiyatli yakunlanadimi, barcha tozalash amallarini kafolatli bajaradi.

## Ishlash natijasi:
```text
Fayl ochildi.
Faylga ma'lumot yozilmoqda...
Xatolik: Exception: Disk to'ldi xatosi
Har qanday holatda ham fayl yopildi!
```

# 655-Topshiriq: StackTrace obyekti va stek izini tahlil qilish

## Topshiriq sharti:
Xatolik qaysi qatorda va qaysi funksiyada yuz berganini StackTrace orqali aniqlang.

## Yechim (Dart kodi):
```dart
void funksiyaB() {
  throw FormatException('Tizim formati buzildi');
}

void funksiyaA() {
  funksiyaB();
}

void main() {
  try {
    funksiyaA();
  } catch (e, stackTrace) {
    print('Xato: $e');
    print('Stek izining birinchi qatori: ${stackTrace.toString().split('
').first}');
  }
}
```

## Tushuntirish va Mantiq:
`catch (e, stackTrace)` ikkinchi argumenti orqali xato yuz bergan chaqiruvlar zanjiri to'liq olinadi.

## Ishlash natijasi:
```text
Xato: FormatException: Tizim formati buzildi
Stek izining birinchi qatori: #0      funksiyaB (file:///...)
```

# 656-Topshiriq: rethrow kalit so'zi (Istisnoni qayta tashlash)

## Topshiriq sharti:
Xatoni log qilib, uni o'zgartirmasdan va stek izini saqlagan holda yuqoriga qayta uzating.

## Yechim (Dart kodi):
```dart
void xizmatQatlami() {
  try {
    int.parse('not_a_number');
  } catch (e) {
    print('[LOG]: Xizmat qatlamida xato qayd etildi.');
    rethrow; // Asl stek izi bilan yuqoriga tashlash
  }
}

void main() {
  try {
    xizmatQatlami();
  } catch (e) {
    print('[UI]: Foydalanuvchiga xabar berildi: $e');
  }
}
```

## Tushuntirish va Mantiq:
`rethrow` xatolikni ushlab, qisman ishlov berib, uning asl stek izini buzmasdan yuqori qatlamga yuborish uchun ishlatiladi.

## Ishlash natijasi:
```text
[LOG]: Xizmat qatlamida xato qayd etildi.
[UI]: Foydalanuvchiga xabar berildi: FormatException: Invalid radix-10 number (at character 1)
not_a_number
^
```

# 657-Topshiriq: Maxsus istisno klassi (Custom Exception)

## Topshiriq sharti:
`implements Exception` orqali ilovangiz uchun maxsus `MablagYetarliEmasException` sinfini tuzing.

## Yechim (Dart kodi):
```dart
class MablagYetarliEmasException implements Exception {
  final double talabQilingan;
  final double mavjud;

  MablagYetarliEmasException(this.talabQilingan, this.mavjud);

  @override
  String toString() => 'MablagYetarliEmasException: Talab: $talabQilingan so\'m, Mavjud: $mavjud so\'m';
}

void pulYechish(double summa, double balans) {
  if (summa > balans) {
    throw MablagYetarliEmasException(summa, balans);
  }
  print('Pul yechildi: $summa');
}

void main() {
  try {
    pulYechish(150000, 100000);
  } on MablagYetarliEmasException catch (e) {
    print('Ushlandi: $e');
  }
}
```

## Tushuntirish va Mantiq:
Domen mantiqidagi xatoliklarni maxsus klasslar orqali ifodalash kod o'qilishini va boshqaruvini osonlashtiradi.

## Ishlash natijasi:
```text
Ushlandi: MablagYetarliEmasException: Talab: 150000.0 so'm, Mavjud: 100000.0 so'm
```

# 658-Topshiriq: Maxsus xato klassi (Custom Error)

## Topshiriq sharti:
`extends Error` yordamida dasturchi tomonidan qilingan xatoni ifodalovchi sinf tuzing.

## Yechim (Dart kodi):
```dart
class KonfiguratsiyaXatosi extends Error {
  final String parametr;
  KonfiguratsiyaXatosi(this.parametr);

  @override
  String toString() => 'KonfiguratsiyaXatosi: "$parametr" parametri ko\'rsatilmagan!';
}

void initsializatsiya(Map<String, String> config) {
  if (!config.containsKey('API_KEY')) {
    throw KonfiguratsiyaXatosi('API_KEY');
  }
}

void main() {
  try {
    initsializatsiya({});
  } on KonfiguratsiyaXatosi catch (e) {
    print('Dasturiy xatolik: $e');
  }
}
```

## Tushuntirish va Mantiq:
`Error` sinfidan meros olish odatda dastur kodidagi tuzatilishi shart bo'lgan mantiqiy nuqsonlarni bildiradi.

## Ishlash natijasi:
```text
Dasturiy xatolik: KonfiguratsiyaXatosi: "API_KEY" parametri ko'rsatilmagan!
```

# 659-Topshiriq: Dartda Error va Exception farqi

## Topshiriq sharti:
Nega `Exception` kutilgan tashqi xatolar uchun, `Error` esa tuzatilishi kerak bo'lgan dasturchi xatolari uchun ekanligini ko'rsating.

## Yechim (Dart kodi):
```dart
void namoyish() {
  // 1. Exception: Tarmoq uzilishi, kutilgan holat, ushlab hal qilish mumkin
  Exception kutilgan = Exception('Internet aloqasi mavjud emas');

  // 2. Error: Argument xatosi, dasturchi kodi noto'g'ri yozilgan
  Error dasturiyXato = ArgumentError('Indeks manfiy bo\'lishi mumkin emas');

  print('1: $kutilgan');
  print('2: $dasturiyXato');
}

void main() {
  namoyish();
}
```

## Tushuntirish va Mantiq:
Exception - dastur davomida yuzaga kelishi mumkin bo'lgan operatsion muammo. Error - dasturchining xatosi (bug) hisoblanadi.

## Ishlash natijasi:
```text
1: Exception: Internet aloqasi mavjud emas
2: Invalid argument(s): Indeks manfiy bo'lishi mumkin emas
```

# 660-Topshiriq: assert operatori va xato xabari

## Topshiriq sharti:
Ishlab chiqish (debug) rejimida parametrlarni tekshiruvchi `assert` operatorini qo'llang.

## Yechim (Dart kodi):
```dart
void foizHisobla(double qiymat) {
  assert(qiymat >= 0 && qiymat <= 100, 'Foiz 0 va 100 oralig\'ida bo\'lishi shart!');
  print('Qabul qilingan foiz: $qiymat%');
}

void main() {
  foizHisobla(85.5);
}
```

## Tushuntirish va Mantiq:
`assert` sharti yolg'on bo'lsa `AssertionError` tashlanadi; production (release) rejimida esa assertlar butunlay o'chiriladi.

## Ishlash natijasi:
```text
Qabul qilingan foiz: 85.5%
```

# 661-Topshiriq: ArgumentError parametr validatsiyasi

## Topshiriq sharti:
Funksiyaga noto'g'ri argument uzatilganda standart `ArgumentError` tashlashni amalga oshiring.

## Yechim (Dart kodi):
```dart
void royxatdanOtish(String login) {
  if (login.trim().isEmpty) {
    throw ArgumentError.value(login, 'login', 'Login bo\'sh bo\'lishi mumkin emas');
  }
  print('Login qabul qilindi: $login');
}

void main() {
  try {
    royxatdanOtish('   ');
  } on ArgumentError catch (e) {
    print('Xato: ${e.message} (Noto\'g\'ri qiymat: "${e.invalidValue}")');
  }
}
```

## Tushuntirish va Mantiq:
`ArgumentError.value()` qaysi parametr va qanday qiymat xato keltirib chiqarganini aniq ko'rsatadi.

## Ishlash natijasi:
```text
Xato: Login bo'sh bo'lishi mumkin emas (Noto'g'ri qiymat: "   ")
```

# 662-Topshiriq: RangeError chegaralar tekshiruvi

## Topshiriq sharti:
Indeks yoki oraliq belgilangan chegaradan chiqib ketganda `RangeError` tashlash dasturini tuzing.

## Yechim (Dart kodi):
```dart
void sahifaOchish(int sahifa, int jamiSahifalar) {
  RangeError.checkValueInInterval(sahifa, 1, jamiSahifalar, 'sahifa');
  print('$sahifa-sahifa ochildi.');
}

void main() {
  try {
    sahifaOchish(15, 10);
  } on RangeError catch (e) {
    print('Chegara xatosi: ${e.message}');
  }
}
```

## Tushuntirish va Mantiq:
`RangeError.checkValueInInterval` qiymat belgilangan min va max oraliqda ekanligini standart tekshiradi.

## Ishlash natijasi:
```text
Chegara xatosi: Not in inclusive range 1..10
```

# 663-Topshiriq: StateError noo'rin holatda chaqiruv

## Topshiriq sharti:
Obyekt noto'g'ri holatda turganda amal bajarishga urinilganda `StateError` tashlang.

## Yechim (Dart kodi):
```dart
class AudioPleyer {
  bool oynamoqdami = false;

  void toxtatish() {
    if (!oynamoqdami) {
      throw StateError('Pleyer allaqachon to\'xtagan!');
    }
    oynamoqdami = false;
    print('Pleyer to\'xtatildi.');
  }
}

void main() {
  var p = AudioPleyer();
  try {
    p.toxtatish();
  } on StateError catch (e) {
    print('Holat xatosi: ${e.message}');
  }
}
```

## Tushuntirish va Mantiq:
`StateError` obyektning joriy holati metodni bajarishga mos kelmaganda qo'llaniladi.

## Ishlash natijasi:
```text
Holat xatosi: Pleyer allaqachon to'xtagan!
```

# 664-Topshiriq: ConcurrentModificationError to'plam o'zgarishi xatosi

## Topshiriq sharti:
`for..in` sikli davomida to'plamdan element o'chirishga urinilganda chiqadigan xatoni ko'rsating.

## Yechim (Dart kodi):
```dart
void main() {
  var royxat = [1, 2, 3, 4];

  try {
    for (var n in royxat) {
      if (n == 2) {
        royxat.remove(n); // XATO: Iteratsiya vaqtida o'chirish taqiqlanadi
      }
    }
  } on ConcurrentModificationError {
    print('Xato ushlandi: Sikl davomida to\'plamni o\'zgartirib bo\'lmaydi!');
  }
}
```

## Tushuntirish va Mantiq:
Sikl vaqtida element o'chirish o'rniga `removeWhere()` yoki nusxa olish (`List.from`) tavsiya etiladi.

## Ishlash natijasi:
```text
Xato ushlandi: Sikl davomida to'plamni o'zgartirib bo'lmaydi!
```

# 665-Topshiriq: UnsupportedError qo'llab-quvvatlanmagan operatsiya

## Topshiriq sharti:
O'zgarmas (unmodifiable) ro'yxatga element qo'shilganda yuz beruvchi xatoni boshqaring.

## Yechim (Dart kodi):
```dart
void main() {
  List<int> ozgarmas = List.unmodifiable([1, 2, 3]);

  try {
    ozgarmas.add(4);
  } on UnsupportedError catch (e) {
    print('Operatsiya taqiqlangan: ${e.message}');
  }
}
```

## Tushuntirish va Mantiq:
O'zgarmas to'plamlar ma'lumotlar xavfsizligini ta'minlaydi va har qanday o'zgartirish urinishida `UnsupportedError` beradi.

## Ishlash natijasi:
```text
Operatsiya taqiqlangan: Cannot add to an unmodifiable list
```

# 666-Topshiriq: Bo'sh to'plamdan element olish xatosi

## Topshiriq sharti:
Bo'sh ro'yxatning `.first` yoki `.single` xususiyatini o'qiganda yuz beruvchi xatolikni ushlang.

## Yechim (Dart kodi):
```dart
void main() {
  List<String> bosh = [];

  try {
    print(bosh.first);
  } on StateError catch (e) {
    print('Ushlandi: Bo\'sh ro\'yxatdan birinchi element olinmaydi (${e.message})');
  }
}
```

## Tushuntirish va Mantiq:
Bo'sh to'plamda `.firstOrNull` (Dart 3) ishlatish yoki `isEmpty` ni oldindan tekshirish tavsiya etiladi.

## Ishlash natijasi:
```text
Ushlandi: Bo'sh ro'yxatdan birinchi element olinmaydi (No element)
```

# 667-Topshiriq: Resurslarni boshqarish (Disposable / Closeable naqshi)

## Topshiriq sharti:
Ish yakunlangach resurslarni xavfsiz bo'shatuvchi `yopish()` metodiga ega klass tuzing.

## Yechim (Dart kodi):
```dart
class Resurs implements Exception {
  bool ochiq = true;

  void ish() {
    if (!ochiq) throw StateError('Resurs yopiq');
    print('Resurs ishlamoqda');
  }

  void yopish() {
    ochiq = false;
    print('Resurs tozalandi va yopildi.');
  }
}

void resursniIshlatish(void Function(Resurs) amal) {
  var r = Resurs();
  try {
    amal(r);
  } finally {
    r.yopish();
  }
}

void main() {
  resursniIshlatish((r) {
    r.ish();
  });
}
```

## Tushuntirish va Mantiq:
Loan pattern yoki `finally` yordamida har qanday resurs to'liq yopilishi kafolatlanadi.

## Ishlash natijasi:
```text
Resurs ishlamoqda
Resurs tozalandi va yopildi.
```

# 668-Topshiriq: Nested try-catch (Ichma-ich istisnolar)

## Topshiriq sharti:
Ichki xatolikni ushlab, boshqa amalni bajarish va uning ham xatolarini tashqi blokda ushlashni ko'rsating.

## Yechim (Dart kodi):
```dart
void main() {
  try {
    print('Tashqi blok boshlandi.');
    try {
      int.parse('xato');
    } catch (ichki) {
      print('Ichki xato ushlandi, zaxira reja ishga tushmoqda...');
      throw Exception('Zaxira server ham javob bermadi');
    }
  } catch (tashqi) {
    print('Tashqi blokda ushlandi: $tashqi');
  }
}
```

## Tushuntirish va Mantiq:
Ichki blokda yuz bergan ikkinchi xatolik tashqi blok orqali to'liq ushlab qolinadi.

## Ishlash natijasi:
```text
Tashqi blok boshlandi.
Ichki xato ushlandi, zaxira reja ishga tushmoqda...
Tashqi blokda ushlandi: Exception: Zaxira server ham javob bermadi
```

# 669-Topshiriq: Xatolik kontekstini boyituvchi qobiq istisno (Exception Wrapping)

## Topshiriq sharti:
Quyi qatlamdagi past darajadagi xatoni yuqori darajadagi biznes xatosiga o'rab qayta tashlang.

## Yechim (Dart kodi):
```dart
class XizmatIstisnosi implements Exception {
  final String xabar;
  final Object aslXato;

  XizmatIstisnosi(this.xabar, this.aslXato);

  @override
  String toString() => '$xabar (Sabab: $aslXato)';
}

void tolovQilish() {
  try {
    throw FormatException('Karta raqami yaroqsiz');
  } catch (e) {
    throw XizmatIstisnosi('To\'lovni amalga oshirib bo\'lmadi', e);
  }
}

void main() {
  try {
    tolovQilish();
  } catch (e) {
    print(e);
  }
}
```

## Tushuntirish va Mantiq:
Exception wrapping orqali foydalanuvchiga tushunarli xabar beriladi va tizim xatosi ham ichida saqlanadi.

## Ishlash natijasi:
```text
To'lovni amalga oshirib bo'lmadi (Sabab: FormatException: Karta raqami yaroqsiz)
```

# 670-Topshiriq: Barcha validatsiya xatolarini yig'uvchi istisno

## Topshiriq sharti:
Birinchi xatoda to'xtamay, formadagi barcha xatolarni ro'yxat qilib tashlovchi `FormValidationException` tuzing.

## Yechim (Dart kodi):
```dart
class FormaValidatsiyaIstisnosi implements Exception {
  final List<String> xatolar;
  FormaValidatsiyaIstisnosi(this.xatolar);

  @override
  String toString() => 'Validatsiya xatoliklari:
- ' + xatolar.join('
- ');
}

void formaniTekshir(String ism, int yosh) {
  List<String> xatolar = [];
  if (ism.isEmpty) xatolar.add('Ism kiritilishi shart');
  if (yosh < 18) xatolar.add('Yosh kamida 18 bo\'lishi kerak');

  if (xatolar.isNotEmpty) {
    throw FormaValidatsiyaIstisnosi(xatolar);
  }
}

void main() {
  try {
    formaniTekshir('', 16);
  } on FormaValidatsiyaIstisnosi catch (e) {
    print(e);
  }
}
```

## Tushuntirish va Mantiq:
Barcha xatoliklarni bitta paketda to'plab ko'rsatish foydalanuvchi tajribasini (UX) sezilarli oshiradi.

## Ishlash natijasi:
```text
Validatsiya xatoliklari:
- Ism kiritilishi shart
- Yosh kamida 18 bo'lishi kerak
```

# 671-Topshiriq: Tarmoq so'rovlari uchun NetworkException va status kodlari

## Topshiriq sharti:
HTTP status kodi va xato xabarini o'zida saqlovchi tarmoq istisnosini tuzing.

## Yechim (Dart kodi):
```dart
class TarmoqIstisnosi implements Exception {
  final int statusCode;
  final String message;

  TarmoqIstisnosi(this.statusCode, this.message);

  @override
  String toString() => 'TarmoqIstisnosi [$statusCode]: $message';
}

void serverdanYuklash(int id) {
  if (id <= 0) {
    throw TarmoqIstisnosi(400, 'ID musbat bo\'lishi kerak');
  }
  if (id == 99) {
    throw TarmoqIstisnosi(404, 'Foydalanuvchi topilmadi');
  }
}

void main() {
  try {
    serverdanYuklash(99);
  } on TarmoqIstisnosi catch (e) {
    print('Tarmoq xatosi: ${e.statusCode} -> ${e.message}');
  }
}
```

## Tushuntirish va Mantiq:
API lar bilan ishlashda status kodlariga ko'ra mos UI dialoglari chiqarish osonlashadi.

## Ishlash natijasi:
```text
Tarmoq xatosi: 404 -> Foydalanuvchi topilmadi
```

# 672-Topshiriq: Ma'lumotlar bazasi tranzaksiyasini rollback qilish

## Topshiriq sharti:
Xato yuz berganda barcha o'zgarishlarni bekor qiluvchi tranzaksiya blokini yozing.

## Yechim (Dart kodi):
```dart
void pulOtqazish(double summa) {
  print('Tranzaksiya boshlandi.');
  try {
    print('Hisobdan $summa so\'m yechildi.');
    if (summa > 500000) {
      throw Exception('Limitdan oshdi!');
    }
    print('Qabul qiluvchiga yetkazildi.');
    print('Tranzaksiya muvaffaqiyatli commit qilindi.');
  } catch (e) {
    print('Xato: $e');
    print('ROLLBACK: Mablag\' qaytarildi!');
  }
}

void main() {
  pulOtqazish(700000);
}
```

## Tushuntirish va Mantiq:
Moliyaviy operatsiyalarda xato sodir bo'lganda `catch` orqali rollback (bekor qilish) qat'iy ta'minlanishi shart.

## Ishlash natijasi:
```text
Tranzaksiya boshlandi.
Hisobdan 700000.0 so'm yechildi.
Xato: Exception: Limitdan oshdi!
ROLLBACK: Mablag' qaytarildi!
```

# 673-Topshiriq: Qayta urinish mexanizmi (Retry Logic)

## Topshiriq sharti:
Nosozlik yuz berganda maksimal N marta qayta urinib ko'ruvchi umumiy `retry` funksiyasini tuzing.

## Yechim (Dart kodi):
```dart
T qaytaUrinish<T>(T Function() harakat, {int maxUrinish = 3}) {
  int urinish = 0;
  while (true) {
    try {
      urinish++;
      return harakat();
    } catch (e) {
      print('$urinish-urinish muvaffaqiyatsiz bo\'ldi.');
      if (urinish >= maxUrinish) {
        rethrow;
      }
    }
  }
}

void main() {
  int sanoq = 0;
  var natija = qaytaUrinish(() {
    sanoq++;
    if (sanoq < 3) throw Exception('Tarmoq uzildi');
    return 'Ma\'lumot muvaffaqiyatli yuklandi!';
  });

  print(natija);
}
```

## Tushuntirish va Mantiq:
Vaqtinchalik tarmoq uzilishlarida qayta urinish (retry) tizimning mustahkamligini oshiradi.

## Ishlash natijasi:
```text
1-urinish muvaffaqiyatsiz bo'ldi.
2-urinish muvaffaqiyatsiz bo'ldi.
Ma'lumot muvaffaqiyatli yuklandi!
```

# 674-Topshiriq: Global xatoliklarni ushlash va jurnalga yozish

## Topshiriq sharti:
Dasturdagi barcha xatoliklarni ro'yxatga olib boruvchi markazlashgan Logger tizimini tuzing.

## Yechim (Dart kodi):
```dart
class XatolarJurnali {
  static final List<String> jurnali = [];

  static void qaydEtish(Object xato, StackTrace stackTrace) {
    String vaqt = '14:00:00';
    jurnali.add('[$vaqt] XATO: $xato');
  }
}

void main() {
  try {
    throw StateError('Kutilmagan global uzilish');
  } catch (e, st) {
    XatolarJurnali.qaydEtish(e, st);
  }

  print('Jurnal:');
  for (var yozuv in XatolarJurnali.jurnali) {
    print(yozuv);
  }
}
```

## Tushuntirish va Mantiq:
Markazlashtirilgan xatoliklar jurnali (Crashlytics, Sentry) ilova barqarorligini kuzatish uchun muhimdir.

## Ishlash natijasi:
```text
Jurnal:
[14:00:00] XATO: Bad state: Kutilmagan global uzilish
```

# 675-Topshiriq: Amaliy: TensorDimensionMismatchException (AI tensor xatosi)

## Topshiriq sharti:
BitNet matritsa ko'paytirishda o'lchamlar mos kelmaganda tashlanuvchi maxsus istisno sinfini tuzing.

## Yechim (Dart kodi):
```dart
class TensorDimensionMismatchException implements Exception {
  final int chapUstunlar;
  final int ongQatorlar;

  TensorDimensionMismatchException(this.chapUstunlar, this.ongQatorlar);

  @override
  String toString() =>
      'TensorDimensionMismatchException: Matritsa ko\'paytirish mumkin emas! '
      'Chap ustun ($chapUstunlar) != O\'ng qator ($ongQatorlar)';
}

void matritsaKopaytir(int aRows, int aCols, int bRows, int bCols) {
  if (aCols != bRows) {
    throw TensorDimensionMismatchException(aCols, bRows);
  }
  print('Matritsalar muvaffaqiyatli ko\'paytirildi: [$aRows x $bCols]');
}

void main() {
  try {
    matritsaKopaytir(2, 3, 4, 2); // 3 != 4
  } on TensorDimensionMismatchException catch (e) {
    print('Tensor xatoligi: $e');
  }
}
```

## Tushuntirish va Mantiq:
AI va chuqur o'rganish kutubxonalarida (PyTorch, TensorFlow, BitNet) tenzor shakllari mos kelmasligi eng keng tarqalgan xato bo'lib, maxsus istisno bilan boshqariladi.

## Ishlash natijasi:
```text
Tensor xatoligi: TensorDimensionMismatchException: Matritsa ko'paytirish mumkin emas! Chap ustun (3) != O'ng qator (4)
```

# 676-Topshiriq: runZonedGuarded orqali global asinxron xatoliklarni ushlash

## Topshiriq sharti:
Butun ilovadagi ushlanmagan (unhandled) barcha asinxron xatoliklarni yagona nuqtada ushlang.

## Yechim (Dart kodi):
```dart
import 'dart:async';

void main() {
  runZonedGuarded(() {
    print('Ilova zonada ishga tushdi.');
    // Asinxron xatolik
    Future.delayed(Duration(milliseconds: 10), () {
      throw Exception('Asinxron kutilmagan nosozlik!');
    });
  }, (xato, stackTrace) {
    print('[GLOBAL USHLANDI]: $xato');
  });
}
```

## Tushuntirish va Mantiq:
`runZonedGuarded` Flutter va Dart backend ilovalarida dastur kutilmaganda to'xtab qolmasligi uchun global xatoliklar qopqoni sifatida xizmat qiladi.

## Ishlash natijasi:
```text
Ilova zonada ishga tushdi.
[GLOBAL USHLANDI]: Exception: Asinxron kutilmagan nosozlik!
```

# 677-Topshiriq: Future.catchError usuli

## Topshiriq sharti:
`async/await` siz `Future` zanjirida xatoliklarni `.catchError()` orqali ushlashni ko'rsating.

## Yechim (Dart kodi):
```dart
Future<int> xavfliHisoblash() {
  return Future.error('Hisoblashda ma\'lumotlar yetarli emas');
}

void main() {
  xavfliHisoblash().then((natija) {
    print('Natija: $natija');
  }).catchError((xato) {
    print('catchError orqali ushlandi: $xato');
  });
}
```

## Tushuntirish va Mantiq:
`Future.catchError()` zanjirdagi ixtiyoriy bosqichda yuz bergan xatolikni ushlab, unga javob qaytarish imkonini beradi.

## Ishlash natijasi:
```text
catchError orqali ushlandi: Hisoblashda ma'lumotlar yetarli emas
```

# 678-Topshiriq: Completer da xatolikni uzatish (completeError)

## Topshiriq sharti:
`Completer` orqali asinxron natijaga xatolik qiymatini biriktirib yakunlang.

## Yechim (Dart kodi):
```dart
import 'dart:async';

Future<String> malumotOlish() {
  var completer = Completer<String>();
  // Simulyatsiya: xatolik sodir bo'ldi
  completer.completeError(TimeoutException('Kutish vaqti tugadi'));
  return completer.future;
}

void main() async {
  try {
    await malumotOlish();
  } catch (e) {
    print('Completer xatosi ushlandi: $e');
  }
}
```

## Tushuntirish va Mantiq:
`completer.completeError(xato)` asinxron operatsiyaning muvaffaqiyatsiz yakunlanganini xabar qiladi.

## Ishlash natijasi:
```text
Completer xatosi ushlandi: TimeoutException: Kutish vaqti tugadi
```

# 679-Topshiriq: Stream ichidagi xatoliklarni boshqarish (handleError)

## Topshiriq sharti:
Oqimdan kelayotgan xatoliklarni filtrlash va oqimni to'xtatmasdan davom ettirish dasturini yozing.

## Yechim (Dart kodi):
```dart
Stream<int> xatoliOqim() async* {
  yield 1;
  yield 2;
  throw Exception('Oqimda nosozlik yuz berdi');
}

void main() {
  xatoliOqim().handleError((xato) {
    print('Oqim xatosi ushlandi: $xato');
  }).listen((qiymat) {
    print('Olingan qiymat: $qiymat');
  });
}
```

## Tushuntirish va Mantiq:
`stream.handleError()` oqim orqali uzatilgan xatolarni tutib olib, qolgan qiymatlar eshittirilishini ta'minlaydi.

## Ishlash natijasi:
```text
Olingan qiymat: 1
Olingan qiymat: 2
Oqim xatosi ushlandi: Exception: Oqimda nosozlik yuz berdi
```

# 680-Topshiriq: Zanjir uzgich Naqshi (Circuit Breaker Pattern)

## Topshiriq sharti:
Ketma-ket 3 marta xato bo'lganda tizimni vaqtincha bloklovchi (ochiq holatga o'tuvchi) Circuit Breaker tuzing.

## Yechim (Dart kodi):
```dart
class CircuitBreaker {
  int xatolarSoni = 0;
  bool ochiqmi = false;

  void bajar(void Function() amal) {
    if (ochiqmi) {
      print('[CIRCUIT BREAKER OCHIQ]: So\'rovlar vaqtincha to\'xtatilgan!');
      return;
    }

    try {
      amal();
      xatolarSoni = 0; // Muvaffaqiyatli bo'lsa tozalash
    } catch (e) {
      xatolarSoni++;
      print('Xato #$xatolarSoni: $e');
      if (xatolarSoni >= 3) {
        ochiqmi = true;
        print('DIQQAT: Ketma-ket 3 ta xato! Circuit Breaker ochildi.');
      }
    }
  }
}

void main() {
  var cb = CircuitBreaker();
  for (int i = 0; i < 4; i++) {
    cb.bajar(() => throw Exception('Server uzildi'));
  }
}
```

## Tushuntirish va Mantiq:
Circuit Breaker qulagan tashqi xizmatlarni tinimsiz so'rovlar bilan yanada charchatmaslik uchun zanjirni uzadi.

## Ishlash natijasi:
```text
Xato #1: Exception: Server uzildi
Xato #2: Exception: Server uzildi
Xato #3: Exception: Server uzildi
DIQQAT: Ketma-ket 3 ta xato! Circuit Breaker ochildi.
[CIRCUIT BREAKER OCHIQ]: So'rovlar vaqtincha to'xtatilgan!
```

# 681-Topshiriq: TimeoutException va asinxron muddat tugashi

## Topshiriq sharti:
`Future.timeout` yordamida uzoq cho'zilgan operatsiyani to'xtatish va `TimeoutException` ni ushlash.

## Yechim (Dart kodi):
```dart
import 'dart:async';

Future<String> uzoqVazifa() async {
  await Future.delayed(Duration(milliseconds: 50));
  return 'Tayyor';
}

void main() async {
  try {
    // 20 ms da timeout beramiz
    await uzoqVazifa().timeout(Duration(milliseconds: 20));
  } on TimeoutException {
    print('Vaqt tugadi: Server juda kech javob bermoqda!');
  }
}
```

## Tushuntirish va Mantiq:
`.timeout(duration)` belgilangan vaqt ichida javob kelmasa avtomatik ravishda `TimeoutException` tashlaydi.

## Ishlash natijasi:
```text
Vaqt tugadi: Server juda kech javob bermoqda!
```

# 682-Topshiriq: Resurs qulflanishi (Deadlock) oldini olish

## Topshiriq sharti:
Qulflangan resursdan foydalanganda har doim ozod qilishni kafolatlovchi qulf mexanizmini tuzing.

## Yechim (Dart kodi):
```dart
class Muteks {
  bool qulflangan = false;

  void qulflash() {
    if (qulflangan) throw StateError('Resurs band!');
    qulflangan = true;
  }

  void ochish() => qulflangan = false;
}

void main() {
  var m = Muteks();
  try {
    m.qulflash();
    print('Resurs ustida xavfsiz amal bajarilmoqda...');
  } finally {
    m.ochish();
    print('Resurs qulfi ochildi.');
  }
}
```

## Tushuntirish va Mantiq:
Har doim `try-finally` ichida qulfni ochish (unlock) orqali tizimning to'xtab qolish xavfi (deadlock) bartaraf etiladi.

## Ishlash natijasi:
```text
Resurs ustida xavfsiz amal bajarilmoqda...
Resurs qulfi ochildi.
```

# 683-Topshiriq: Fayl tizimi istisnolari (FileSystemException)

## Topshiriq sharti:
Mavjud bo'lmagan fayl ochilishiga urinilganda maxsus fayl tizimi xatosini simulyatsiya qiling.

## Yechim (Dart kodi):
```dart
class FaylTizimiIstisnosi implements Exception {
  final String faylYoli;
  final String sabab;

  FaylTizimiIstisnosi(this.faylYoli, this.sabab);

  @override
  String toString() => 'FaylTizimiIstisnosi: $faylYoli - $sabab';
}

void faylOqish(String path) {
  if (!path.endsWith('.txt')) {
    throw FaylTizimiIstisnosi(path, 'Faqat .txt fayllar qo\'llab-quvvatlanadi');
  }
  print('Fayl o\'qildi: $path');
}

void main() {
  try {
    faylOqish('data.bin');
  } on FaylTizimiIstisnosi catch (e) {
    print('Fayl xatosi: $e');
  }
}
```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda kutilmagan formatlar yoki ruxsat yetishmasligi maxsus fayl istisnolari bilan ushlanadi.

## Ishlash natijasi:
```text
Fayl xatosi: FaylTizimiIstisnosi: data.bin - Faqat .txt fayllar qo'llab-quvvatlanadi
```

# 684-Topshiriq: JSON parsingda TypeError boshqaruvi

## Topshiriq sharti:
Kutilgan son o'rniga matn kelib qolgandagi `TypeError` ni ushlab, standart qiymat o'rnatish.

## Yechim (Dart kodi):
```dart
int xavfsizYoshOlish(Map<String, dynamic> json) {
  try {
    return json['yosh'] as int;
  } on TypeError {
    print('Ogohlantirish: "yosh" maydoni int emas, 0 deb olindi.');
    return 0;
  }
}

void main() {
  Map<String, dynamic> noto'g'riJson = {'yosh': 'yigirma besh'};
  int yosh = xavfsizYoshOlish(noto'g'riJson);
  print('Yosh: $yosh');
}
```

## Tushuntirish va Mantiq:
API dan noto'g'ri turdagi ma'lumot kelganda `TypeError` ushlanib, ilova qulab tushishining oldi olinadi.

## Ishlash natijasi:
```text
Ogohlantirish: "yosh" maydoni int emas, 0 deb olindi.
Yosh: 0
```

# 685-Topshiriq: Maxsus Avtorizatsiya istisnosi (UnauthorizedException)

## Topshiriq sharti:
Foydalanuvchi huquqi yetarli bo'lmaganda tashlanuvchi `UnauthorizedException` sinfini tuzing.

## Yechim (Dart kodi):
```dart
class AvtorizatsiyaIstisnosi implements Exception {
  final String rol;
  AvtorizatsiyaIstisnosi(this.rol);

  @override
  String toString() => 'AvtorizatsiyaIstisnosi: "$rol" roli bu amalni bajara olmaydi!';
}

void adminPaneligaKirish(String rol) {
  if (rol != 'admin') {
    throw AvtorizatsiyaIstisnosi(rol);
  }
  print('Admin paneliga xush kelibsiz.');
}

void main() {
  try {
    adminPaneligaKirish('mehmon');
  } on AvtorizatsiyaIstisnosi catch (e) {
    print(e);
  }
}
```

## Tushuntirish va Mantiq:
Xavfsizlik talab qilinadigan bo'limlarda avtorizatsiya va ruxsatlar xatoliklari alohida tutiladi.

## Ishlash natijasi:
```text
AvtorizatsiyaIstisnosi: "mehmon" roli bu amalni bajara olmaydi!
```

# 686-Topshiriq: Token muddati o'tgan istisno (TokenExpiredException)

## Topshiriq sharti:
JWT token muddati tugaganda qayta kirishni talab qiluvchi maxsus istisno yozing.

## Yechim (Dart kodi):
```dart
class TokenMuddatiOtganIstisno implements Exception {
  final DateTime eskirganVaqt;
  TokenMuddatiOtganIstisno(this.eskirganVaqt);

  @override
  String toString() => 'TokenMuddatiOtganIstisno: Token $eskirganVaqt da o\'z kuchini yo\'qotgan';
}

void apiSorov(DateTime tokenMuddati) {
  if (DateTime.now().isAfter(tokenMuddati)) {
    throw TokenMuddatiOtganIstisno(tokenMuddati);
  }
}

void main() {
  try {
    apiSorov(DateTime(2026, 1, 1)); // Muddati o'tgan
  } on TokenMuddatiOtganIstisno catch (e) {
    print('Tokenni yangilash zarur: $e');
  }
}
```

## Tushuntirish va Mantiq:
Token muddati tugashi bilan ilova foydalanuvchini qayta login sahifasiga yo'naltiradi.

## Ishlash natijasi:
```text
Tokenni yangilash zarur: TokenMuddatiOtganIstisno: Token 2026-01-01 00:00:00.000 da o'z kuchini yo'qotgan
```

# 687-Topshiriq: Xatolik kodlari va lokalizatsiya (Ko'p tilli xabarlar)

## Topshiriq sharti:
Xatolik kodiga qarab o'zbek yoki ingliz tilida xabar qaytaruvchi tizim tuzing.

## Yechim (Dart kodi):
```dart
enum XatoKodi { tarmoqYoq, parolNotogri }

class LokalizatsiyaQilinganXato implements Exception {
  final XatoKodi kod;
  LokalizatsiyaQilinganXato(this.kod);

  String xabar(String til) {
    if (til == 'uz') {
      return switch (kod) {
        XatoKodi.tarmoqYoq => 'Internet aloqasi mavjud emas',
        XatoKodi.parolNotogri => 'Kiritilgan parol noto\'g\'ri',
      };
    } else {
      return switch (kod) {
        XatoKodi.tarmoqYoq => 'No internet connection',
        XatoKodi.parolNotogri => 'Incorrect password',
      };
    }
  }
}

void main() {
  var xato = LokalizatsiyaQilinganXato(XatoKodi.parolNotogri);
  print('O\'zbekcha: ${xato.xabar("uz")}');
  print('Inglizcha: ${xato.xabar("en")}');
}
```

## Tushuntirish va Mantiq:
Xatoliklarni kodlar (enum) orqali ifodalash ilovani turli tillarga qulay moslashtirish imkonini beradi.

## Ishlash natijasi:
```text
O'zbekcha: Kiritilgan parol noto'g'ri
Inglizcha: Incorrect password
```

# 688-Topshiriq: Eksponentsial orqaga chekinish (Exponential Backoff)

## Topshiriq sharti:
Qayta urinishlar orasidagi kutish vaqtini 2 baravardan oshirib boruvchi mexanizm tuzing.

## Yechim (Dart kodi):
```dart
void eksponentsialKutish(int urinish) {
  int soniya = 1 << urinish; // 2^urinish: 1, 2, 4, 8...
  print('$urinish-qayta urinish: $soniya soniya kutish rejalashtirildi.');
}

void main() {
  for (int i = 0; i < 4; i++) {
    eksponentsialKutish(i);
  }
}
```

## Tushuntirish va Mantiq:
Exponential backoff serverga tushadigan bosimni kamaytirish va tarmoq barqarorligini ta'minlash uchun standartdir.

## Ishlash natijasi:
```text
0-qayta urinish: 1 soniya kutish rejalashtirildi.
1-qayta urinish: 2 soniya kutish rejalashtirildi.
2-qayta urinish: 4 soniya kutish rejalashtirildi.
3-qayta urinish: 8 soniya kutish rejalashtirildi.
```

# 689-Topshiriq: Fallback keshdan o'qish (Offline-first error handling)

## Topshiriq sharti:
Tarmoqdan ma'lumot yuklab bo'lmaganda avtomatik keshdagi eski ma'lumotni beruvchi dastur tuzing.

## Yechim (Dart kodi):
```dart
String serverdanYuklash() {
  throw Exception('Internet uzilgan');
}

String ma'lumotOlish(Map<String, String> kesh) {
  try {
    return serverdanYuklash();
  } catch (e) {
    print('Tarmoq xatosi bo\'ldi. Keshdan olinmoqda...');
    return kesh['oxirgi_xabar'] ?? 'Bo\'sh';
  }
}

void main() {
  var kesh = {'oxirgi_xabar': 'Keshdagi muhim yangilik'};
  print('Natija: ${ma'lumotOlish(kesh)}');
}
```

## Tushuntirish va Mantiq:
Offline-first yondashuvda tarmoq xatosi foydalanuvchiga to'sqinlik qilmasdan keshdagi ma'lumotlar bilan qoplanadi.

## Ishlash natijasi:
```text
Tarmoq xatosi bo'ldi. Keshdan olinmoqda...
Natija: Keshdagi muhim yangilik
```

# 690-Topshiriq: Dart Zone orqali xatoliklarni izolyatsiya qilish

## Topshiriq sharti:
Maxsus `Zone` yaratib, undagi kod bajarilishini va xatolarini boshqa qismlardan mustaqil boshqaring.

## Yechim (Dart kodi):
```dart
import 'dart:async';

void main() {
  Zone maxsusZona = Zone.current.fork(
    specification: ZoneSpecification(
      print: (self, parent, zone, line) {
        parent.print(zone, '[ZONA LOG]: $line');
      },
    ),
  );

  maxsusZona.run(() {
    print('Salom, maxsus zonadan!');
  });
}
```

## Tushuntirish va Mantiq:
Dart Zonalari oqimlarni, xatoliklar qopqonlarini va konsolga yozishlarni izolyatsiya qilish uchun ishlatiladi.

## Ishlash natijasi:
```text
[ZONA LOG]: Salom, maxsus zonadan!
```

# 691-Topshiriq: Model fayli topilmadi istisnosi (ModelNotFoundException)

## Topshiriq sharti:
AI modeli yuklanayotganda fayl yo'li mavjud bo'lmasa tashlanuvchi istisno tuzing.

## Yechim (Dart kodi):
```dart
class ModelTopilmadiIstisno implements Exception {
  final String faylYoli;
  ModelTopilmadiIstisno(this.faylYoli);

  @override
  String toString() => 'ModelTopilmadiIstisno: "$faylYoli" manzilda AI model topilmadi!';
}

void modelYuklash(String path) {
  if (path != 'model.bitnet') {
    throw ModelTopilmadiIstisno(path);
  }
  print('Model muvaffaqiyatli xotiraga yuklandi.');
}

void main() {
  try {
    modelYuklash('eski_model.bin');
  } on ModelTopilmadiIstisno catch (e) {
    print(e);
  }
}
```

## Tushuntirish va Mantiq:
On-device AI modellarini ishga tushirishda model fayllarining mavjudligi maxsus istisnolar bilan qat'iy nazorat qilinadi.

## Ishlash natijasi:
```text
ModelTopilmadiIstisno: "eski_model.bin" manzilda AI model topilmadi!
```

# 692-Topshiriq: Og'irliklar buzilganligi istisnosi (CorruptedWeightsException)

## Topshiriq sharti:
Model og'irliklarining nazorat yig'indisi (checksum) mos kelmaganda yuz beruvchi xatoni boshqaring.

## Yechim (Dart kodi):
```dart
class OgirliklarBuzuqIstisno implements Exception {
  final int kutilganCrc;
  final int haqiqiyCrc;

  OgirliklarBuzuqIstisno(this.kutilganCrc, this.haqiqiyCrc);

  @override
  String toString() => 'OgirliklarBuzuqIstisno: CRC mos kelmadi! Kutilgan: $kutilganCrc, Haqiqiy: $haqiqiyCrc';
}

void vaznlarniTekshir(int kutilgan, int haqiqiy) {
  if (kutilgan != haqiqiy) {
    throw OgirliklarBuzuqIstisno(kutilgan, haqiqiy);
  }
  print('Vaznlar yaxlitligi tasdiqlandi.');
}

void main() {
  try {
    vaznlarniTekshir(0xA1B2, 0xFFFF);
  } on OgirliklarBuzuqIstisno catch (e) {
    print('Xatolik: $e');
  }
}
```

## Tushuntirish va Mantiq:
Buzilgan yoki to'liq yuklanmagan AI vaznlarini ishga tushirish xato natijalarga sabab bo'lishining oldi olinadi.

## Ishlash natijasi:
```text
Xatolik: OgirliklarBuzuqIstisno: CRC mos kelmadi! Kutilgan: 41394, Haqiqiy: 65535
```

# 693-Topshiriq: Xotira yetishmovchiligi simulyatsiyasi

## Topshiriq sharti:
Katta tenzor yaratilganda xotira chegarasidan oshish holatini boshqaring.

## Yechim (Dart kodi):
```dart
void tenzorYaratish(int elementlarSoni) {
  const int maxChegara = 1000000;
  if (elementlarSoni > maxChegara) {
    throw StateError('Qurilma RAM xotirasi yetarli emas: talab $elementlarSoni element');
  }
  print('Tenzor uchun xotira ajratildi.');
}

void main() {
  try {
    tenzorYaratish(5000000);
  } on StateError catch (e) {
    print('Xotira xatosi: ${e.message}');
  }
}
```

## Tushuntirish va Mantiq:
Mobil qurilmalarda 1-bit AI model ishlaganda RAM chegaralari doimiy nazorat qilinishi zarur.

## Ishlash natijasi:
```text
Xotira xatosi: Qurilma RAM xotirasi yetarli emas: talab 5000000 element
```

# 694-Topshiriq: O'zgarmas holat invariantlarini tekshiruvchi Guard klassi

## Topshiriq sharti:
Funksiya chaqirilishidan oldin barcha zaruriy shartlarni tekshiruvchi Guard statik yordamchisini tuzing.

## Yechim (Dart kodi):
```dart
class Guard {
  static void musbatSon(num son, String parametr) {
    if (son <= 0) {
      throw ArgumentError('$parametr musbat bo\'lishi kerak (Kiritildi: $son)');
    }
  }
}

void tezlikniOshir(double tezlik) {
  Guard.musbatSon(tezlik, 'tezlik');
  print('Tezlik: $tezlik km/s');
}

void main() {
  try {
    tezlikniOshir(-10);
  } on ArgumentError catch (e) {
    print('Guard ushladi: ${e.message}');
  }
}
```

## Tushuntirish va Mantiq:
Guard sinflari dasturning kirish nuqtalarida mudofaa dasturlashini (Defensive Programming) qulaylashtiradi.

## Ishlash natijasi:
```text
Guard ushladi: tezlik musbat bo'lishi kerak (Kiritildi: -10.0)
```

# 695-Topshiriq: Xatoliklar konveyeri (Error Pipeline)

## Topshiriq sharti:
Xatolik yuz berganda uni qayta ishlab, xabar va kodni shakllantiruvchi pipeline tuzing.

## Yechim (Dart kodi):
```dart
String xatoniQaytaIshlash(Object xato) {
  if (xato is FormatException) return 'Noto\'g\'ri ma\'lumot formati';
  if (xato is TimeoutException) return 'Javob berish vaqti tugadi';
  return 'Kutilmagan xatolik yuz berdi';
}

void main() {
  print(xatoniQaytaIshlash(FormatException()));
  print(xatoniQaytaIshlash(TimeoutException('Vaqt')));
}
```

## Tushuntirish va Mantiq:
Xatoliklarni markazlashgan holda foydalanuvchi tushunadigan xabarlarga aylantirish qulay vositadir.

## Ishlash natijasi:
```text
Noto'g'ri ma'lumot formati
Javob berish vaqti tugadi
```

# 696-Topshiriq: Kriptografik kalit formati xatosi (InvalidKeyException)

## Topshiriq sharti:
Kalit uzunligi kamida 32 bayt bo'lmaganda maxsus xatolik tashlang.

## Yechim (Dart kodi):
```dart
class YaroqsizKalitIstisno implements Exception {
  final int uzunlik;
  YaroqsizKalitIstisno(this.uzunlik);

  @override
  String toString() => 'YaroqsizKalitIstisno: Kalit 32 bayt bo\'lishi kerak, berildi: $uzunlik';
}

void shifrlash(String key) {
  if (key.length < 32) {
    throw YaroqsizKalitIstisno(key.length);
  }
  print('Xavfsiz shifrlash bajarildi.');
}

void main() {
  try {
    shifrlash('qisqa_kalit');
  } on YaroqsizKalitIstisno catch (e) {
    print(e);
  }
}
```

## Tushuntirish va Mantiq:
Xavfsizlik protokollarida kriptografik kalitlar to'liq tekshiruvdan o'tkaziladi.

## Ishlash natijasi:
```text
YaroqsizKalitIstisno: Kalit 32 bayt bo'lishi kerak, berildi: 11
```

# 697-Topshiriq: Avtomatik diagnostika hisoboti tayyorlash

## Topshiriq sharti:
Xato yuz berganda qurilma holati, xotira va vaqtni birlashtirib diagnostika faylini hosil qiling.

## Yechim (Dart kodi):
```dart
class DiagnostikaHisoboti {
  static String hisobot(Object xato, String modul) {
    return '''--- Nosozlik Hisoboti ---
Modul: $modul
Xato: $xato
Sana: 2026-11-07
Holat: Qayd etildi''';
  }
}

void main() {
  var rep = DiagnostikaHisoboti.hisobot(Exception('Tarmoq uzildi'), 'AuthModul');
  print(rep);
}
```

## Tushuntirish va Mantiq:
Nosozliklar haqida to'liq texnik kontekstni yig'ish muammoni tezkor tuzatishga ko'maklashadi.

## Ishlash natijasi:
```text
--- Nosozlik Hisoboti ---
Modul: AuthModul
Xato: Exception: Tarmoq uzildi
Sana: 2026-11-07
Holat: Qayd etildi
```

# 698-Topshiriq: Ko'p bosqichli autentifikatsiya (MFA) xatoliklari

## Topshiriq sharti:
SMS kod noto'g'ri kiritilganda urinishlar sonini hisoblovchi istisno tuzing.

## Yechim (Dart kodi):
```dart
class MfaXatoligi implements Exception {
  final int qolganUrinishlar;
  MfaXatoligi(this.qolganUrinishlar);

  @override
  String toString() => 'MfaXatoligi: Noto\'g\'ri kod! Qolgan urinishlar: $qolganUrinishlar';
}

void kodniTekshir(String kod, int urinishlar) {
  if (kod != '1234') {
    throw MfaXatoligi(urinishlar - 1);
  }
  print('Tasdiqlandi!');
}

void main() {
  try {
    kodniTekshir('9999', 3);
  } on MfaXatoligi catch (e) {
    print(e);
  }
}
```

## Tushuntirish va Mantiq:
Ikki bosqichli autentifikatsiyada urinishlar soni cheklangan bo'lib, xatolik orqali foydalanuvchiga bildiriladi.

## Ishlash natijasi:
```text
MfaXatoligi: Noto'g'ri kod! Qolgan urinishlar: 2
```

# 699-Topshiriq: Token kontekstidan oshib ketish (ContextLengthExceededException)

## Topshiriq sharti:
LLM modeliga uzatilgan prompt kontekst oynasidan (masalan 2048 token) oshib ketganda xato bering.

## Yechim (Dart kodi):
```dart
class KontekstChegarasiOshdiIstisno implements Exception {
  final int kiritilganTokenlar;
  final int maxTokenlar;

  KontekstChegarasiOshdiIstisno(this.kiritilganTokenlar, this.maxTokenlar);

  @override
  String toString() => 'KontekstChegarasiOshdiIstisno: $kiritilganTokenlar > $maxTokenlar (Kontekst to\'ldi!)';
}

void promptYuborish(int tokenlar) {
  const int maxLimit = 2048;
  if (tokenlar > maxLimit) {
    throw KontekstChegarasiOshdiIstisno(tokenlar, maxLimit);
  }
  print('Prompt muvaffaqiyatli qabul qilindi ($tokenlar token).');
}

void main() {
  try {
    promptYuborish(4096);
  } on KontekstChegarasiOshdiIstisno catch (e) {
    print(e);
  }
}
```

## Tushuntirish va Mantiq:
AI modellarining kontekst chegarasi oshib ketishi xotira toshishining oldini olish uchun qat'iy nazorat qilinadi.

## Ishlash natijasi:
```text
KontekstChegarasiOshdiIstisno: 4096 > 2048 (Kontekst to'ldi!)
```

# 700-Topshiriq: Amaliy: BitNet Inference Error Boundary (1-bit AI xavfsiz dvigateli)

## Topshiriq sharti:
BitNet model inferensiyasi jarayonida yuz berishi mumkin bo'lgan barcha xatoliklarni xavfsiz boshqaruvchi Engine klassini tuzing.

## Yechim (Dart kodi):
```dart
sealed class AiNatija {}

class AiMuvaffaqiyat extends AiNatija {
  final String javob;
  AiMuvaffaqiyat(this.javob);
}

class AiNosozlik extends AiNatija {
  final String xatolikXabari;
  AiNosozlik(this.xatolikXabari);
}

class BitNetEngine {
  AiNatija runInference(String prompt) {
    try {
      if (prompt.trim().isEmpty) {
        throw ArgumentError('Prompt bo\'sh bo\'lishi mumkin emas');
      }
      if (prompt.length > 500) {
        throw FormatException('Prompt haddan tashqari uzun');
      }

      // Xavfsiz ternar inferensiya simulyatsiyasi
      return AiMuvaffaqiyat('BitNet 1-bit AI javobi: "O\'zbekiston texnologik kelajagi porloq!"');
    } catch (e) {
      return AiNosozlik('Inferensiya xatosi: $e');
    }
  }
}

void main() {
  var engine = BitNetEngine();

  var res1 = engine.runInference('Kelajak haqida aytib ber');
  var res2 = engine.runInference('');

  for (var r in [res1, res2]) {
    switch (r) {
      case AiMuvaffaqiyat(:var javob):
        print('[AI JAVOBI]: $javob');
      case AiNosozlik(:var xatolikXabari):
        print('[XATOLIK TO\'SIG\'I]: $xatolikXabari');
    }
  }
}
```

## Tushuntirish va Mantiq:
Error Boundary naqshi AI dvigatelini to'liq qamrab olib, dastur hech qachon kutilmaganda to'xtab qolmasligini kafolatlaydi.

## Ishlash natijasi:
```text
[AI JAVOBI]: BitNet 1-bit AI javobi: "O'zbekiston texnologik kelajagi porloq!"
[XATOLIK TO'SIG'I]: Inferensiya xatosi: Invalid argument(s): Prompt bo'sh bo'lishi mumkin emas
```

