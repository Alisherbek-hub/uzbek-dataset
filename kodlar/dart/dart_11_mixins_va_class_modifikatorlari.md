# 501-Topshiriq: Mixin asoslari (mixin va with kalit so'zlari)

## Topshiriq sharti:
Merosxo'rliksiz xulq-atvorni qayta ishlatish uchun `mixin` va `with` kalit so'zlarini qo'llang.

## Yechim (Dart kodi):
```dart
mixin Suzuvchi {
  void suzish() => print('Suvda suzmoqda...');
}

class Odam {}

class Giloschi extends Odam with Suzuvchi {}

void main() {
  var sportchi = Giloschi();
  sportchi.suzish();
}
```

## Tushuntirish va Mantiq:
`mixin` kodni boshqa klasslarga meros iyerarxiyasini buzmagan holda qo'shish (injektsiya) imkonini beradi.

## Ishlash natijasi:
```text
Suvda suzmoqda...
```

# 502-Topshiriq: Mixin ichida holat (state) va maydonlar saqlash

## Topshiriq sharti:
Mixin ichida o'zgaruvchilar e'lon qilish va ularni xulq-atvor bilan birga saqlashni ko'rsating.

## Yechim (Dart kodi):
```dart
mixin HarakatHisoblagich {
  int qadamlar = 0;

  void qadamTashlash() {
    qadamlar++;
    print('Qadam tashlandi. Jami: $qadamlar');
  }
}

class Sayyoh with HarakatHisoblagich {}

void main() {
  var s = Sayyoh();
  s.qadamTashlash();
  s.qadamTashlash();
  print('Yakuniy qadamlar: ${s.qadamlar}');
}
```

## Tushuntirish va Mantiq:
Mixinlar faqat metodlarni emas, balki ichki holat (o'zgaruvchilar)ni ham saqlashi mumkin.

## Ishlash natijasi:
```text
Qadam tashlandi. Jami: 1
Qadam tashlandi. Jami: 2
Yakuniy qadamlar: 2
```

# 503-Topshiriq: Bir nechta mixinlarni ketma-ket ulash (Linearization)

## Topshiriq sharti:
Bir nechta mixinlar qo'shilganda metodlarning chaqirilish tartibi va oxirgi mixinning ustunligini ko'rsating.

## Yechim (Dart kodi):
```dart
mixin A {
  void salom() => print('Salom A dan');
}

mixin B {
  void salom() => print('Salom B dan');
}

class Sinov with A, B {}

void main() {
  var s = Sinov();
  s.salom(); // B mixini A ning ustidan yozadi
}
```

## Tushuntirish va Mantiq:
`with A, B` ro'yxatida oxirgi turgan mixin eng ustun hisoblanadi (Linearization / Mixin Order).

## Ishlash natijasi:
```text
Salom B dan
```

# 504-Topshiriq: mixin on SuperType (Qo'llanish doirasini cheklash)

## Topshiriq sharti:
Mixin faqat ma'lum bir ota klassdan meros olgan sinflarda ishlatilishini `on` kalit so'zi bilan kafolatlang.

## Yechim (Dart kodi):
```dart
abstract class Jonivor {
  final String nom;
  Jonivor(this.nom);
}

// Faqat Jonivor dan chiqqan klasslar Uchuvchi bo'la oladi
mixin Uchuvchi on Jonivor {
  void uch() => print('$nom havoga ko\'tarildi!');
}

class Qush extends Jonivor with Uchuvchi {
  Qush(super.nom);
}

void main() {
  var burgut = Qush('Burgut');
  burgut.uch();
}
```

## Tushuntirish va Mantiq:
`mixin Uchuvchi on Jonivor` sintaksisi mixin ichida `nom` kabi `Jonivor` xususiyatlaridan to'liq xavfsiz foydalanish imkonini beradi.

## Ishlash natijasi:
```text
Burgut havoga ko'tarildi!
```

# 505-Topshiriq: Mixin ichida super chaqiruvlari

## Topshiriq sharti:
Mixin ichida `super.metod()` chaqirish orqali zanjirli harakatni amalga oshiring.

## Yechim (Dart kodi):
```dart
abstract class Baza {
  void bajar() => print('Baza bajarildi');
}

mixin Birinchi on Baza {
  @override
  void bajar() {
    super.bajar();
    print('Birinchi mixin bajarildi');
  }
}

class Dastur extends Baza with Birinchi {}

void main() {
  var d = Dastur();
  d.bajar();
}
```

## Tushuntirish va Mantiq:
Mixin ichidagi `super.metod()` chaqiruvi miksinlar zanjirida o'zidan oldingi sinf yoki mixinning metodini ishga tushiradi.

## Ishlash natijasi:
```text
Baza bajarildi
Birinchi mixin bajarildi
```

# 506-Topshiriq: Reaktiv Kuzatuvchi Mixini (ChangeNotifier uslubida)

## Topshiriq sharti:
Tinglovchilarni ro'yxatga oluvchi va o'zgarish bo'lganda ularni xabardor qiluvchi mixin tuzing.

## Yechim (Dart kodi):
```dart
typedef Tinglovchi = void Function();

mixin OzgarishXabarchisi {
  final List<Tinglovchi> _tinglovchilar = [];

  void tinglovchiQosh(Tinglovchi t) => _tinglovchilar.add(t);

  void xabarBer() {
    for (var t in _tinglovchilar) {
      t();
    }
  }
}

class Hisoblagich with OzgarishXabarchisi {
  int qiymat = 0;

  void oshir() {
    qiymat++;
    xabarBer();
  }
}

void main() {
  var h = Hisoblagich();
  h.tinglovchiQosh(() => print('Hisoblagich o\'zgardi: ${h.qiymat}'));

  h.oshir();
  h.oshir();
}
```

## Tushuntirish va Mantiq:
Flutterdagi `ChangeNotifier` ham xuddi shunday tamoyilda mixin yoki sinf sifatida holat boshqaruvida ishlaydi.

## Ishlash natijasi:
```text
Hisoblagich o'zgardi: 1
Hisoblagich o'zgardi: 2
```

# 507-Topshiriq: Log yozuvchi mixin (LoggingMixin)

## Topshiriq sharti:
Ixtiyoriy klassga avtomatik log yozish xususiyatini qo'shuvchi mixin tuzing.

## Yechim (Dart kodi):
```dart
mixin LogYozuvchi {
  void log(String xabar) {
    print('[${runtimeType}] [${DateTime.now().second}s]: $xabar');
  }
}

class Xizmat with LogYozuvchi {
  void start() => log('Xizmat ishga tushirildi');
}

void main() {
  var x = Xizmat();
  x.start();
}
```

## Tushuntirish va Mantiq:
`runtimeType` orqali mixin o'zi qo'shilgan joriy sinf nomini avtomatik aniqlay oladi.

## Ishlash natijasi:
```text
[Xizmat] [0s]: Xizmat ishga tushirildi
```

# 508-Topshiriq: Validatsiya mixini (ValidationMixin)

## Topshiriq sharti:
Email va parollarni tekshiruvchi yordamchi metodlarni saqlovchi mixin yozing.

## Yechim (Dart kodi):
```dart
mixin ValidatsiyaMixin {
  bool emailTogrimi(String email) {
    return email.contains('@') && email.contains('.');
  }

  bool parolKuchlimi(String parol) {
    return parol.length >= 8;
  }
}

class RoyxatdanOtish with ValidatsiyaMixin {
  void tekshir(String email, String parol) {
    print('Email to\'g\'rimi: ${emailTogrimi(email)}');
    print('Parol kuchlimi: ${parolKuchlimi(parol)}');
  }
}

void main() {
  var forma = RoyxatdanOtish();
  forma.tekshir('alisher@mail.uz', 'Maxfiy123');
}
```

## Tushuntirish va Mantiq:
Validatsiya mantiqini mixin ichida saqlash turli UI formalarida uni qayta ishlatishga imkon beradi.

## Ishlash natijasi:
```text
Email to'g'rimi: true
Parol kuchlimi: true
```

# 509-Topshiriq: Identifikatsiya beruvchi mixin (IdentifiableMixin)

## Topshiriq sharti:
Har bir yangi obyektga avtomatik takrorlanmas ID raqami taqdim etuvchi mixin tuzing.

## Yechim (Dart kodi):
```dart
mixin IdMixin {
  static int _hisob = 0;
  final int uniqueId = ++_hisob;
}

class Buyurtma with IdMixin {}
class Foydalanuvchi with IdMixin {}

void main() {
  var b1 = Buyurtma();
  var b2 = Buyurtma();
  var u1 = Foydalanuvchi();

  print('B1 ID: ${b1.uniqueId}');
  print('B2 ID: ${b2.uniqueId}');
  print('U1 ID: ${u1.uniqueId}');
}
```

## Tushuntirish va Mantiq:
Statik hisoblagich yordamida barcha miksinlangan obyektlar o'ziga xos global ID ga ega bo'ladi.

## Ishlash natijasi:
```text
B1 ID: 1
B2 ID: 2
U1 ID: 3
```

# 510-Topshiriq: Vaqt tamg'asi mixini (TimestampedMixin)

## Topshiriq sharti:
Obyekt yaratilgan va tahrirlangan vaqtni avtomatik qayd etib boruvchi mixin tuzing.

## Yechim (Dart kodi):
```dart
mixin VaqtTamgasi {
  final DateTime yaratildi = DateTime(2026, 11, 7, 10, 0);
  DateTime yangilandi = DateTime(2026, 11, 7, 10, 0);

  void yangilash() {
    yangilandi = DateTime(2026, 11, 7, 10, 30);
  }
}

class Post with VaqtTamgasi {
  String matn;
  Post(this.matn);
}

void main() {
  var post = Post('Dart 3.x qoidalari');
  print('Yaratildi: ${post.yaratildi}');

  post.yangilash();
  print('Yangilandi: ${post.yangilandi}');
}
```

## Tushuntirish va Mantiq:
Baza modellari uchun umumiy bo'lgan audit vaqtlarini mixin orqali barcha modellarga bir xilda ulash mumkin.

## Ishlash natijasi:
```text
Yaratildi: 2026-11-07 10:00:00.000
Yangilandi: 2026-11-07 10:30:00.000
```

# 511-Topshiriq: O'chirish holati mixini (SoftDeleteMixin)

## Topshiriq sharti:
Obyektni butunlay o'chirmasdan 'o'chirilgan' belgisi bilan boshqaruvchi mixin yozing.

## Yechim (Dart kodi):
```dart
mixin SoftDeleteMixin {
  bool _ochirilgan = false;

  bool get ochirilgan => _ochirilgan;

  void ochirish() => _ochirilgan = true;
  void tiklash() => _ochirilgan = false;
}

class Mahsulot with SoftDeleteMixin {
  final String nom;
  Mahsulot(this.nom);
}

void main() {
  var m = Mahsulot('Smartfon');
  print('O\'chirilganmi: ${m.ochirilgan}');

  m.ochirish();
  print('O\'chirishdan keyin: ${m.ochirilgan}');

  m.tiklash();
  print('Tiklashdan keyin: ${m.ochirilgan}');
}
```

## Tushuntirish va Mantiq:
Soft-delete ma'lumotlar bazasida obyektlarni butunlay yo'q qilmay, arxivlash tamoyilini ta'minlaydi.

## Ishlash natijasi:
```text
O'chirilganmi: false
O'chirishdan keyin: true
Tiklashdan keyin: false
```

# 512-Topshiriq: Dart 3: sealed class asoslari

## Topshiriq sharti:
Dart 3 ning `sealed` kalit so'zi yordamida yopiq tip iyerarxiyasini shakllantiring.

## Yechim (Dart kodi):
```dart
sealed class Natija {}

class Muvaffaqiyat extends Natija {
  final String xabar;
  Muvaffaqiyat(this.xabar);
}

class Xato extends Natija {
  final String sabab;
  Xato(this.sabab);
}

void main() {
  Natija n1 = Muvaffaqiyat('Ma\'lumot yuklandi');
  Natija n2 = Xato('Server 500');

  print('Natijalar yaratildi.');
}
```

## Tushuntirish va Mantiq:
`sealed class` o'z kutubxonasidan tashqarida voris olishni taqiqlaydi va barcha mumkin bo'lgan subtiplarni cheklaydi.

## Ishlash natijasi:
```text
Natijalar yaratildi.
```

# 513-Topshiriq: sealed class va to'liq qamrov tekshiruvi (Exhaustiveness checking)

## Topshiriq sharti:
`switch` da `default` shartini yozmasdan barcha holatlar tekshirilishini kafolatlang.

## Yechim (Dart kodi):
```dart
sealed class YuklashHolati {}

class Boshlangich extends YuklashHolati {}
class Yuklanmoqda extends YuklashHolati {}
class Tugallandi extends YuklashHolati {
  final String data;
  Tugallandi(this.data);
}

String holatMatni(YuklashHolati holat) {
  // Sealed class sababli barcha variantlar qamrab olinishi shart!
  return switch (holat) {
    Boshlangich() => 'Hali boshlanmadi',
    Yuklanmoqda() => 'Kuting, yuklanmoqda...',
    Tugallandi(:final data) => 'Ma\'lumot: $data',
  };
}

void main() {
  print(holatMatni(Boshlangich()));
  print(holatMatni(Yuklanmoqda()));
  print(holatMatni(Tugallandi('OK')));
}
```

## Tushuntirish va Mantiq:
Agar yangi subtip qo'shilsa va u `switch`da hisobga olinmasa, Dart kompilyatori xatolik ko'rsatib ogohlantiradi.

## Ishlash natijasi:
```text
Hali boshlanmadi
Kuting, yuklanmoqda...
Ma'lumot: OK
```

# 514-Topshiriq: sealed class bilan Result (Success / Failure) modeli

## Topshiriq sharti:
Dasturdagi operatsiyalar natijasini xavfsiz ifodalovchi Result algebraik ma'lumotlar turini tuzing.

## Yechim (Dart kodi):
```dart
sealed class Result<T> {}

class Success<T> extends Result<T> {
  final T data;
  Success(this.data);
}

class Failure<T> extends Result<T> {
  final String error;
  Failure(this.error);
}

Result<int> bolish(int a, int b) {
  if (b == 0) return Failure('Nolga bo\'lish mumkin emas');
  return Success(a ~/ b);
}

void main() {
  var r1 = bolish(10, 2);
  var r2 = bolish(10, 0);

  for (var r in [r1, r2]) {
    switch (r) {
      case Success(:var data):
        print('Natija: $data');
      case Failure(:var error):
        print('Xato: $error');
    }
  }
}
```

## Tushuntirish va Mantiq:
`Result<T>` naqshi istisnolarni (Exception) tashlamasdan, xatoliklarni qiymat sifatida boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Natija: 5
Xato: Nolga bo'lish mumkin emas
```

# 515-Topshiriq: sealed class bilan AuthStatus holatlar mashinasi

## Topshiriq sharti:
Autentifikatsiya jarayonini (Boshlang'ich, Tasdiqlangan, Chiqib ketgan) ifodalang.

## Yechim (Dart kodi):
```dart
sealed class Autentifikatsiya {}

class ChiqibKetgan extends Autentifikatsiya {}
class Jarayonda extends Autentifikatsiya {}
class Kirgan extends Autentifikatsiya {
  final String foydalanuvchi;
  Kirgan(this.foydalanuvchi);
}

void main() {
  Autentifikatsiya holat = Kirgan('Alisher');

  var matn = switch (holat) {
    ChiqibKetgan() => 'Iltimos, tizimga kiring',
    Jarayonda() => 'Tekshirilmoqda...',
    Kirgan(:var foydalanuvchi) => 'Xush kelibsiz, $foydalanuvchi!',
  };

  print(matn);
}
```

## Tushuntirish va Mantiq:
Pattern matching va sealed class kombinatsiyasi Flutter UI holatlarini (BLoC / Cubit / Riverpod) boshqarishda standartdir.

## Ishlash natijasi:
```text
Xush kelibsiz, Alisher!
```

# 516-Topshiriq: Dart 3: final class modifikatori

## Topshiriq sharti:
Tashqaridan `extends`, `implements` yoki `with` qilinishi to'liq taqiqlangan `final class` yarating.

## Yechim (Dart kodi):
```dart
final class XavfsizToken {
  final String qiymat;

  XavfsizToken(this.qiymat);

  void chop() => print('Token: $qiymat');
}

void main() {
  var t = XavfsizToken('abc_secret_123');
  t.chop();
}
```

## Tushuntirish va Mantiq:
`final class` modifikatori klassning o'z kutubxonasidan tashqarida hech qanday usul bilan o'zgartirilmasligini yoki meros olinmasligini kafolatlaydi.

## Ishlash natijasi:
```text
Token: abc_secret_123
```

# 517-Topshiriq: final class ichki kutubxonada voris olish qoidalari

## Topshiriq sharti:
`final class` dan faqat o'sha fayl (kutubxona) ichida voris olish mumkin va voris ham modifikatorga ega bo'lishi kerakligini ko'rsating.

## Yechim (Dart kodi):
```dart
final class BazaXavfsizlik {}

// Baza final bo'lsa, voris ham base, final yoki sealed bo'lishi shart!
final class KengaytirilganXavfsizlik extends BazaXavfsizlik {
  void tekshir() => print('Xavfsizlik tizimi faol.');
}

void main() {
  var k = KengaytirilganXavfsizlik();
  k.tekshir();
}
```

## Tushuntirish va Mantiq:
Dart 3 da `final class`dan meros oluvchi har qanday voris klass ham `base`, `final` yoki `sealed` modifikatori bilan yopilishi shart.

## Ishlash natijasi:
```text
Xavfsizlik tizimi faol.
```

# 518-Topshiriq: Dart 3: base class modifikatori

## Topshiriq sharti:
Faqat meros olishga (`extends`) ruxsat beruvchi, biroq `implements` qilishni taqiqlovchi `base class` tuzing.

## Yechim (Dart kodi):
```dart
base class AvtomobilBazas {
  void signal() => print('Bip-bip!');
}

base class Sedan extends AvtomobilBazas {}

void main() {
  var s = Sedan();
  s.signal();
}
```

## Tushuntirish va Mantiq:
`base class` klassning xulq-atvori buzilishining oldini oladi: boshqalar uni `implements` qilib ota metodlarini tashlab keta olmaydi.

## Ishlash natijasi:
```text
Bip-bip!
```

# 519-Topshiriq: base class orqali API barqarorligini ta'minlash

## Topshiriq sharti:
Kutubxona muallifi yangi metod qo'shganda tashqi kod buzilmasligi uchun `base` modifikatorini qo'llash.

## Yechim (Dart kodi):
```dart
base class ApiMijoz {
  void yangiMetodQoshildi() {
    print('Yangi xizmat ishlab turibdi');
  }
}

base class MeningMijozim extends ApiMijoz {}

void main() {
  var c = MeningMijozim();
  c.yangiMetodQoshildi();
}
```

## Tushuntirish va Mantiq:
Agar `ApiMijoz` faqat interfeys bo'lganida, unga metod qo'shilishi boshqalarning kodini buzardi. `base` da esa meros olingan metod avtomatik ishlaydi.

## Ishlash natijasi:
```text
Yangi xizmat ishlab turibdi
```

# 520-Topshiriq: Dart 3: interface class modifikatori

## Topshiriq sharti:
Tashqaridan faqat `implements` qilinishi mumkin bo'lgan, ammo `extends` qilib bo'lmaydigan `interface class` yarating.

## Yechim (Dart kodi):
```dart
interface class BildirishnomaShartnomasi {
  void yubor(String xabar) {
    print('Standart yuborish');
  }
}

class MeningXizmatim implements BildirishnomaShartnomasi {
  @override
  void yubor(String xabar) {
    print('Shaxsiy xabar: $xabar');
  }
}

void main() {
  BildirishnomaShartnomasi x = MeningXizmatim();
  x.yubor('Salom!');
}
```

## Tushuntirish va Mantiq:
`interface class` tashqi foydalanuvchilarni klass metodlarini to'liq qaytadan yozishga majbur qiladi va meros zanjiriga kiritmaydi.

## Ishlash natijasi:
```text
Shaxsiy xabar: Salom!
```

# 521-Topshiriq: Dart 3: abstract interface class (Sof interfeys)

## Topshiriq sharti:
Nusxa olinmaydigan va faqat amalga oshirish (`implements`) uchun mo'ljallangan sof interfeys ta'rifi.

## Yechim (Dart kodi):
```dart
abstract interface class XizmatKorsatuvchi {
  void ishniBajar();
}

class HaqiqiyXizmat implements XizmatKorsatuvchi {
  @override
  void ishniBajar() => print('Xizmat ko\'rsatildi.');
}

void main() {
  XizmatKorsatuvchi x = HaqiqiyXizmat();
  x.ishniBajar();
}
```

## Tushuntirish va Mantiq:
`abstract interface class` boshqa tillardagi (Java, C#, TS) an'anaviy `interface` tushunchasining Dart 3 dagi aynan ekvivalentidir.

## Ishlash natijasi:
```text
Xizmat ko'rsatildi.
```

# 522-Topshiriq: Dart 3: mixin class modifikatori

## Topshiriq sharti:
Ham oddiy klass (instansiya olinadigan), ham mixin (`with` qilib ulanadigan) gibrid `mixin class` tuzing.

## Yechim (Dart kodi):
```dart
mixin class Ovoz {
  void ovozBer() => print('Ovoz chiqarilmoqda...');
}

// 1. Oddiy klass sifatida nusxa olish
// 2. Mixin sifatida with orqali ulash
class Mushuk with Ovoz {}

void main() {
  var oddiyOvoz = Ovoz();
  oddiyOvoz.ovozBer();

  var mushuk = Mushuk();
  mushuk.ovozBer();
}
```

## Tushuntirish va Mantiq:
Dart 3 dan boshlab klassni mixin sifatida ishlatish uchun unga ochiqchasiga `mixin class` deb belgilash talab etiladi.

## Ishlash natijasi:
```text
Ovoz chiqarilmoqda...
Ovoz chiqarilmoqda...
```

# 523-Topshiriq: mixin class cheklovlari

## Topshiriq sharti:
`mixin class` `extends` kalit so'ziga ega bo'lmasligi va parametrlarga ega generativ konstruktorga ega bo'lolmasligini ko'rsating.

## Yechim (Dart kodi):
```dart
mixin class Yordamchi {
  // Faqat parametrsiz standart konstruktorga ruxsat bor
  void yordam() => print('Yordamchi funksiya bajarildi');
}

class Asosiy with Yordamchi {}

void main() {
  var a = Asosiy();
  a.yordam();
}
```

## Tushuntirish va Mantiq:
`mixin class` boshqa klasslardan meros ololmaydi va murakkab konstruktorlarga ega bo'la olmaydi.

## Ishlash natijasi:
```text
Yordamchi funksiya bajarildi
```

# 524-Topshiriq: Keshlovchi xulq-atvor mixini (CacheableMixin)

## Topshiriq sharti:
Metod natijalarini kalit bo'yicha keshda saqlovchi va takroriy hisoblashdan asrovchi mixin tuzing.

## Yechim (Dart kodi):
```dart
mixin KeshlovchiMixin {
  final Map<String, dynamic> _kesh = {};

  T keshdanYokiHisobla<T>(String kalit, T Function() hisoblagich) {
    if (_kesh.containsKey(kalit)) {
      print('Keshdan olindi: $kalit');
      return _kesh[kalit] as T;
    }
    print('Yangi hisoblandi: $kalit');
    T qiymat = hisoblagich();
    _kesh[kalit] = qiymat;
    return qiymat;
  }
}

class MatematikService with KeshlovchiMixin {
  int kvadrat(int n) => keshdanYokiHisobla('kv_$n', () => n * n);
}

void main() {
  var s = MatematikService();
  print(s.kvadrat(5));
  print(s.kvadrat(5)); // Keshdan olinadi
}
```

## Tushuntirish va Mantiq:
Mixin orqali ixtiyoriy xizmatga xotirada kesh saqlash imkoniyatini bir qatorda qo'shish mumkin.

## Ishlash natijasi:
```text
Yangi hisoblandi: kv_5
25
Keshdan olindi: kv_5
25
```

# 525-Topshiriq: Amaliy: Mixin yordamida BitNet Tensor normalizatsiyasi

## Topshiriq sharti:
Tensor ma'lumotlarini qabul qiluvchi va RMSNorm (Root Mean Square) normalizatsiya qiluvchi mixin tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:math';

mixin RmsNormMixin {
  List<double> rmsNorm(List<double> x, {double eps = 1e-5}) {
    double sumSq = x.fold(0.0, (s, val) => s + val * val);
    double rms = sqrt(sumSq / x.length + eps);
    return x.map((val) => val / rms).toList();
  }
}

class BitNetLayer with RmsNormMixin {
  void hisobla(List<double> x) {
    var normX = rmsNorm(x);
    print('Kirish: $x');
    print('RMSNorm: ${normX.map((e) => e.toStringAsFixed(2)).toList()}');
  }
}

void main() {
  var qatlam = BitNetLayer();
  qatlam.hisobla([1.0, 2.0, 3.0, 4.0]);
}
```

## Tushuntirish va Mantiq:
Llama va BitNet b1.58 neyron tarmoqlarida RMSNorm har bir blok boshida aktivatsiyalarni barqarorlashtirish uchun qo'llaniladi.

## Ishlash natijasi:
```text
Kirish: [1.0, 2.0, 3.0, 4.0]
RMSNorm: [0.37, 0.73, 1.10, 1.46]
```

# 526-Topshiriq: sealed class daraxti va Geometrik shakllar hisobi

## Topshiriq sharti:
Geometrik shakllar iyerarxiyasini `sealed` qilib, `switch` orqali maydon hisoblovchi to'liq funksiya yozing.

## Yechim (Dart kodi):
```dart
import 'dart:math';

sealed class Shakl {}

class Doira extends Shakl {
  final double radius;
  Doira(this.radius);
}

class Tortburchak extends Shakl {
  final double eni, boyi;
  Tortburchak(this.eni, this.boyi);
}

class Kvadrat extends Shakl {
  final double tomon;
  Kvadrat(this.tomon);
}

double yuzaHisobla(Shakl s) => switch (s) {
      Doira(:var radius) => pi * radius * radius,
      Tortburchak(:var eni, :var boyi) => eni * boyi,
      Kvadrat(:var tomon) => tomon * tomon,
    };

void main() {
  Shakl f1 = Doira(2.0);
  Shakl f2 = Kvadrat(5.0);

  print('Doira yuzi: ${yuzaHisobla(f1).toStringAsFixed(2)}');
  print('Kvadrat yuzi: ${yuzaHisobla(f2).toStringAsFixed(2)}');
}
```

## Tushuntirish va Mantiq:
`sealed class` tufayli `switch` ifodasida `default` bo'limi shart emas, har bir shakl turi aniq olinadi.

## Ishlash natijasi:
```text
Doira yuzi: 12.57
Kvadrat yuzi: 25.00
```

# 527-Topshiriq: sealed class bilan Tarmoq javoblari modeli

## Topshiriq sharti:
HTTP javoblarini (Success, ClientError, ServerError) ifodalovchi yopiq modellar tizimini tuzing.

## Yechim (Dart kodi):
```dart
sealed class TarmoqJavobi {}

class Muvaffaqiyatli extends TarmoqJavobi {
  final int kod;
  final String body;
  Muvaffaqiyatli(this.kod, this.body);
}

class MijozXatosi extends TarmoqJavobi {
  final int kod;
  final String sabab;
  MijozXatosi(this.kod, this.sabab);
}

class ServerXatosi extends TarmoqJavobi {
  final int kod;
  ServerXatosi(this.kod);
}

void tahlil(TarmoqJavobi j) {
  switch (j) {
    case Muvaffaqiyatli(:var body):
      print('Javob olindi: $body');
    case MijozXatosi(:var kod, :var sabab):
      print('Mijoz xatosi ($kod): $sabab');
    case ServerXatosi(:var kod):
      print('Serverda nosozlik: $kod');
  }
}

void main() {
  tahlil(Muvaffaqiyatli(200, '{"data": "salom"}'));
  tahlil(MijozXatosi(404, 'Sahifa topilmadi'));
}
```

## Tushuntirish va Mantiq:
Tarmoq xatolari va javoblari bitta `sealed` tur ostida birlashtirilib, xatoliklarni aniq ushlash ta'minlanadi.

## Ishlash natijasi:
```text
Javob olindi: {"data": "salom"}
Mijoz xatosi (404): Sahifa topilmadi
```

# 528-Topshiriq: sealed class bilan To'lov jarayoni holatlari

## Topshiriq sharti:
Kutilmoqda, Amalga oshirilmoqda, Muvaffaqiyatli va Xato to'lov holatlarini modellashtiring.

## Yechim (Dart kodi):
```dart
sealed class TolovHolati {}

class Kutilmoqda extends TolovHolati {}
class Jarayonda extends TolovHolati {
  final String tranzaksiyaId;
  Jarayonda(this.tranzaksiyaId);
}
class Bajarildi extends TolovHolati {
  final double summa;
  Bajarildi(this.summa);
}
class Xatolik extends TolovHolati {
  final String sabab;
  Xatolik(this.sabab);
}

void main() {
  TolovHolati holat = Bajarildi(50000);

  String xabar = switch (holat) {
    Kutilmoqda() => 'To\'lov kutilmoqda...',
    Jarayonda(:var tranzaksiyaId) => 'Tranzaksiya #$tranzaksiyaId tekshirilmoqda',
    Bajarildi(:var summa) => '${summa.toStringAsFixed(0)} so\'m muvaffaqiyatli to\'landi!',
    Xatolik(:var sabab) => 'Xatolik yuz berdi: $sabab',
  };

  print(xabar);
}
```

## Tushuntirish va Mantiq:
To'lov tizimlari holatlarini boshqarishda barcha holatlar nazorat ostida bo'ladi.

## Ishlash natijasi:
```text
50000 so'm muvaffaqiyatli to'landi!
```

# 529-Topshiriq: sealed class bilan AST (Abstract Syntax Tree) ifodalari

## Topshiriq sharti:
Arifmetik ifodalarni (Son, Qo'shish, Ko'paytirish) ifodalovchi rekursiv AST daraxtini va hisoblagichini tuzing.

## Yechim (Dart kodi):
```dart
sealed class Ifoda {}

class Son extends Ifoda {
  final int qiymat;
  Son(this.qiymat);
}

class Qoshish extends Ifoda {
  final Ifoda chap, ong;
  Qoshish(this.chap, this.ong);
}

class Kopaytirish extends Ifoda {
  final Ifoda chap, ong;
  Kopaytirish(this.chap, this.ong);
}

int hisobla(Ifoda ifoda) => switch (ifoda) {
      Son(:var qiymat) => qiymat,
      Qoshish(:var chap, :var ong) => hisobla(chap) + hisobla(ong),
      Kopaytirish(:var chap, :var ong) => hisobla(chap) * hisobla(ong),
    };

void main() {
  // (3 + 5) * 2
  var daraxt = Kopaytirish(
    Qoshish(Son(3), Son(5)),
    Son(2),
  );

  print('Hisoblash natijasi: ${hisobla(daraxt)}');
}
```

## Tushuntirish va Mantiq:
Kompilyatorlar va ifoda interpretatorlarida `sealed class` rekursiv daraxtlarni ifodalash uchun eng mukammal vositadir.

## Ishlash natijasi:
```text
Hisoblash natijasi: 16
```

# 530-Topshiriq: sealed class va Records bilan ma'lumotlarni destruktizatsiya qilish

## Topshiriq sharti:
Sealed class subtiplaridan Record qaytarish va ularni destruktizatsiya qilib olish namunasini ko'rsating.

## Yechim (Dart kodi):
```dart
sealed class Javob {}

class Muvaffaqiyat extends Javob {
  final (int, String) user;
  Muvaffaqiyat(this.user);
}

class Xato extends Javob {
  final int kod;
  Xato(this.kod);
}

void main() {
  Javob j = Muvaffaqiyat((42, 'Sanjar'));

  if (j case Muvaffaqiyat(user: (var id, var ism))) {
    print('Foydalanuvchi ID: $id, Ismi: $ism');
  }
}
```

## Tushuntirish va Mantiq:
Sealed class va Records birgalikda kuchli pattern matching orqali chuqur qatlamdagi qiymatlarni bitta satrda ajratib oladi.

## Ishlash natijasi:
```text
Foydalanuvchi ID: 42, Ismi: Sanjar
```

# 531-Topshiriq: base class va interface class o'zaro taqqosi

## Topshiriq sharti:
`base` faqat `extends` qilishga, `interface` esa faqat `implements` qilishga ruxsat berishini misolda taqqoslang.

## Yechim (Dart kodi):
```dart
base class BazaNamuna {
  void salom() => print('Base salom');
}

interface class InterfeysNamuna {
  void alik() => print('Interface alik');
}

// BazaNamuna ni faqat extends qilish mumkin
base class VorisBaza extends BazaNamuna {}

// InterfeysNamuna ni faqat implements qilish mumkin
class VorisInterfeys implements InterfeysNamuna {
  @override
  void alik() => print('Mening aligim');
}

void main() {
  var b = VorisBaza();
  b.salom();

  var i = VorisInterfeys();
  i.alik();
}
```

## Tushuntirish va Mantiq:
`base` to'liq kodni meros berishni, `interface` esa faqat shartnoma talab qilishni majburlovchi arxitekturaviy vositalardir.

## Ishlash natijasi:
```text
Base salom
Mening aligim
```

# 532-Topshiriq: final class orqali Xavfsiz Kalit Generatori

## Topshiriq sharti:
Kriptografik kalitlarni tashqaridan o'zgartirish yoki soxtalashtirishdan himoyalovchi `final class` tuzing.

## Yechim (Dart kodi):
```dart
final class MaxfiyKalit {
  final String _kalit;

  MaxfiyKalit(this._kalit);

  String get maskalanganKalit => '${_kalit.substring(0, 3)}****';
}

void main() {
  var k = MaxfiyKalit('SECRET_KEY_999');
  print('Kalit: ${k.maskalanganKalit}');
}
```

## Tushuntirish va Mantiq:
`final class` xavfsizlikka oid obyektlarni hech kim soxta subklass bilan almashtira olmasligini ta'minlaydi.

## Ishlash natijasi:
```text
Kalit: SEC****
```

# 533-Topshiriq: mixin class yordamida harakatlanuvchi komponent

## Topshiriq sharti:
Ham alohida sinf nusxasi, ham boshqa sinfga mixin sifatida qo'shiladigan `mixin class` tuzing.

## Yechim (Dart kodi):
```dart
mixin class Harakatlanuvchi {
  double tezlik = 0.0;

  void tezlash(double q) {
    tezlik += q;
    print('Joriy tezlik: $tezlik km/s');
  }
}

class Velosiped with Harakatlanuvchi {}

void main() {
  // 1. Alohida obyekt sifatida
  var h = Harakatlanuvchi();
  h.tezlash(10);

  // 2. Mixin sifatida
  var v = Velosiped();
  v.tezlash(25);
}
```

## Tushuntirish va Mantiq:
`mixin class` sinf va mixin chegarasini birlashtiradi va ikkala usulda ham chaqirilishga imkon beradi.

## Ishlash natijasi:
```text
Joriy tezlik: 10.0 km/s
Joriy tezlik: 25.0 km/s
```

# 534-Topshiriq: Mixin ichida Generic parametrlar

## Topshiriq sharti:
Ixtiyoriy tipdagi ma'lumotlarni saqlovchi generic `mixin Saqlagich<T>` yarating.

## Yechim (Dart kodi):
```dart
mixin Saqlagich<T> {
  final List<T> _quti = [];

  void saqla(T element) => _quti.add(element);
  T? oxirgisi() => _quti.isEmpty ? null : _quti.last;
}

class SonlarKonteyneri with Saqlagich<int> {}

void main() {
  var c = SonlarKonteyneri();
  c.saqla(100);
  c.saqla(200);

  print('Oxirgi element: ${c.oxirgisi()}');
}
```

## Tushuntirish va Mantiq:
Mixinlar o'z tip parametrlariga (`generic type arguments`) ega bo'lib, tur xavfsizligini ta'minlaydi.

## Ishlash natijasi:
```text
Oxirgi element: 200
```

# 535-Topshiriq: Bir nechta mixinlarda bir xil nomli metodlar to'qnashuvi

## Topshiriq sharti:
Ikkita mixinda bir xil metod bo'lsa, oxirgi mixin metod ustun kelishini tekshiring.

## Yechim (Dart kodi):
```dart
mixin Bir {
  String status() => 'Birinchi mixin';
}

mixin Ikki {
  String status() => 'Ikkinchi mixin';
}

class Sinov with Bir, Ikki {}

void main() {
  var s = Sinov();
  print(s.status());
}
```

## Tushuntirish va Mantiq:
Dart linearizatsiyasi bo'yicha `with Bir, Ikki` ro'yxatida o'ngdagi mixin metodlari chapdagilarni qayta yozadi (override).

## Ishlash natijasi:
```text
Ikkinchi mixin
```

# 536-Topshiriq: Mixin orqali Comparable xususiyatini qo'shish

## Topshiriq sharti:
Obyektga maydon bo'yicha solishtirish imkoniyatini taqdim etuvchi mixin tuzing.

## Yechim (Dart kodi):
```dart
mixin BahoTaqqoslagich on Object {
  double get ball;

  bool yuqorimi(BahoTaqqoslagich boshqa) => ball > boshqa.ball;
}

class Talaba with BahoTaqqoslagich {
  final String ism;
  @override
  final double ball;

  Talaba(this.ism, this.ball);
}

void main() {
  var t1 = Talaba('Temur', 85.0);
  var t2 = Talaba('Zohid', 92.5);

  print('Zohid Temurdan yuqorimi: ${t2.yuqorimi(t1)}');
}
```

## Tushuntirish va Mantiq:
Mixin talab qilgan `ball` getteri sinfda joriy etiladi va taqqoslash metodi avtomatik ulanadi.

## Ishlash natijasi:
```text
Zohid Temurdan yuqorimi: true
```

# 537-Topshiriq: Mixin orqali Iterable aylanuvchi xulq-atvorini ulash

## Topshiriq sharti:
Obyekt ichidagi elementlar bo'ylab oson aylanish imkonini beruvchi mixin tuzing.

## Yechim (Dart kodi):
```dart
mixin QatorlarAylanishi {
  List<String> get qatorlar;

  void qatorlarniChopEt() {
    for (int i = 0; i < qatorlar.length; i++) {
      print('${i + 1}. ${qatorlar[i]}');
    }
  }
}

class Hujjat with QatorlarAylanishi {
  @override
  final List<String> qatorlar;

  Hujjat(this.qatorlar);
}

void main() {
  var doc = Hujjat(['Birinchi band', 'Ikkinchi band', 'Xulosa']);
  doc.qatorlarniChopEt();
}
```

## Tushuntirish va Mantiq:
Mixin sinfdagi ma'lumotlar ustida umumiy algoritmlarni (chop etish, formatlash) oson bajaradi.

## Ishlash natijasi:
```text
1. Birinchi band
2. Ikkinchi band
3. Xulosa
```

# 538-Topshiriq: on kalit so'zi bilan bir nechta talablar (mixin M on A, B)

## Topshiriq sharti:
Mixin qo'shilishi uchun bir vaqtning o'zida bir nechta sinf yoki interfeyslarga mos kelishi shartini belgilang.

## Yechim (Dart kodi):
```dart
abstract class Qurilma {}
abstract class Ekranli {}

mixin SmartDispley on Qurilma, Ekranli {
  void korsat() => print('Smart displey ma\'lumot ko\'rsatmoqda');
}

class Smartfon extends Qurilma implements Ekranli with SmartDispley {}

void main() {
  var phone = Smartfon();
  phone.korsat();
}
```

## Tushuntirish va Mantiq:
`mixin on A, B` sharti faqatgina ham `A`dan meros olgan, ham `B`ni joriy qilgan sinflargina bu mixinni ulashiga ruxsat beradi.

## Ishlash natijasi:
```text
Smart displey ma'lumot ko'rsatmoqda
```

# 539-Topshiriq: Flutter Lifecycle mixin simulyatsiyasi

## Topshiriq sharti:
Ilova holati (pause, resume) o'zgarganda xabardor qiluvchi hayot sikli mixini tuzing.

## Yechim (Dart kodi):
```dart
enum AppHolati { faol, pauza, toxtatildi }

mixin HayotSikliKuzatuvchisi {
  void holatOzgarishi(AppHolati yangiHolat) {
    print('Ilova holati: $yangiHolat');
  }
}

class MeningSahifam with HayotSikliKuzatuvchisi {}

void main() {
  var sahifa = MeningSahifam();
  sahifa.holatOzgarishi(AppHolati.pauza);
  sahifa.holatOzgarishi(AppHolati.faol);
}
```

## Tushuntirish va Mantiq:
Flutterda `WidgetsBindingObserver` ilova sikli o'zgarishlarini kuzatish uchun aynan shunday ishlaydi.

## Ishlash natijasi:
```text
Ilova holati: AppHolati.pauza
Ilova holati: AppHolati.faol
```

# 540-Topshiriq: Option (Some, None) Monadasi sealed class orqali

## Topshiriq sharti:
Null qiymat o'rniga xavfsiz `Option<T>` turini `sealed class` yordamida quring.

## Yechim (Dart kodi):
```dart
sealed class Option<T> {}

class Some<T> extends Option<T> {
  final T value;
  Some(this.value);
}

class None<T> extends Option<T> {}

Option<String> foydalanuvchiTop(int id) {
  if (id == 1) return Some('Ali');
  return None();
}

void main() {
  var res = foydalanuvchiTop(1);
  var nom = switch (res) {
    Some(:var value) => 'Topildi: $value',
    None() => 'Foydalanuvchi mavjud emas',
  };
  print(nom);
}
```

## Tushuntirish va Mantiq:
Funksional dasturlashdagi `Option/Maybe` monadasi null tekshiruvlarini to'liq xavfsiz va aniq qiladi.

## Ishlash natijasi:
```text
Topildi: Ali
```

# 541-Topshiriq: Either (Left, Right) modeli sealed class orqali

## Topshiriq sharti:
Ikki xil qiymatdan birini (Xato yoki Muvaffaqiyat) saqlovchi Either monadasini tuzing.

## Yechim (Dart kodi):
```dart
sealed class Either<L, R> {}

class Left<L, R> extends Either<L, R> {
  final L value;
  Left(this.value);
}

class Right<L, R> extends Either<L, R> {
  final R value;
  Right(this.value);
}

Either<String, double> kvadratIldiz(double x) {
  if (x < 0) return Left('Manfiy sondan ildiz chiqmaydi');
  return Right(x * 0.5); // Sodda simulyatsiya
}

void main() {
  var javob = kvadratIldiz(-4);
  switch (javob) {
    case Left(:var value):
      print('Xato: $value');
    case Right(:var value):
      print('Natija: $value');
  }
}
```

## Tushuntirish va Mantiq:
Either konvensiyasiga ko'ra `Left` odatda xatolikni, `Right` esa to'g'ri qiymatni ifodalaydi.

## Ishlash natijasi:
```text
Xato: Manfiy sondan ildiz chiqmaydi
```

# 542-Topshiriq: Obyektni klonlash mixini (ClonableMixin)

## Topshiriq sharti:
Obyekt nusxasini xususiyatlari bilan birga ko'chirib yangisini qaytaruvchi mixin tuzing.

## Yechim (Dart kodi):
```dart
mixin NusxaOlish<T> {
  T nusxa();
}

class Sozlama implements NusxaOlish<Sozlama> {
  final String til;
  final bool tunda;

  Sozlama(this.til, this.tunda);

  @override
  Sozlama nusxa({String? til, bool? tunda}) {
    return Sozlama(til ?? this.til, tunda ?? this.tunda);
  }

  @override
  String toString() => 'Sozlama(til: $til, tunda: $tunda)';
}

void main() {
  var s1 = Sozlama('uz', false);
  var s2 = s1.nusxa(tunda: true);

  print('Asl: $s1');
  print('Nusxa: $s2');
}
```

## Tushuntirish va Mantiq:
`copyWith` yoki nusxa olish metodi Flutterda immutability holatlarini boshqarishda keng ishlatiladi.

## Ishlash natijasi:
```text
Asl: Sozlama(til: uz, tunda: false)
Nusxa: Sozlama(til: uz, tunda: true)
```

# 543-Topshiriq: Tranzaksiyalarni boshqarish mixini (TransactionMixin)

## Topshiriq sharti:
Amallar muvaffaqiyatsiz bo'lsa orqaga qaytaruvchi (Rollback) tranzaksiya mixini tuzing.

## Yechim (Dart kodi):
```dart
mixin TranzaksiyaMixin {
  int _boshlangich = 0;
  int joriy = 0;

  void boshlash() {
    _boshlangich = joriy;
    print('Tranzaksiya boshlandi. Boshlang\'ich: $_boshlangich');
  }

  void bekorQilish() {
    joriy = _boshlangich;
    print('Tranzaksiya bekor qilindi. Qaytarildi: $joriy');
  }
}

class Hamyon with TranzaksiyaMixin {
  Hamyon(int summa) {
    joriy = summa;
  }
}

void main() {
  var h = Hamyon(500);
  h.boshlash();
  h.joriy -= 300; // Xatolik yuz berdi deylik
  h.bekorQilish();
}
```

## Tushuntirish va Mantiq:
Mixin yordamida holatni orqaga qaytarish (rollback) tizimini osonlikcha modellashtirish mumkin.

## Ishlash natijasi:
```text
Tranzaksiya boshlandi. Boshlang'ich: 500
Tranzaksiya bekor qilindi. Qaytarildi: 500
```

# 544-Topshiriq: Reaktiv voqealarni filtrlash mixini (EventFilterMixin)

## Topshiriq sharti:
Kelayotgan voqealarni faqat ruxsat berilgan turlari bo'yicha saralovchi mixin tuzing.

## Yechim (Dart kodi):
```dart
mixin VoqeaFiltr {
  bool ruxsatBormi(String tur) => tur == 'MUHIM';

  void voqeaQabul(String tur, String xabar) {
    if (ruxsatBormi(tur)) {
      print('ISHLANDI [$tur]: $xabar');
    } else {
      print('E\'tiborga olinmadi: $tur');
    }
  }
}

class Xizmat with VoqeaFiltr {}

void main() {
  var x = Xizmat();
  x.voqeaQabul('ODDIY', 'Kundalik ping');
  x.voqeaQabul('MUHIM', 'Server xotirasi 95% ga yetdi!');
}
```

## Tushuntirish va Mantiq:
Mixinlar orqali reaktiv oqimlardagi filtrlash mantiqini modullarga ajratish qulay.

## Ishlash natijasi:
```text
E'tiborga olinmadi: ODDIY
ISHLANDI [MUHIM]: Server xotirasi 95% ga yetdi!
```

# 545-Topshiriq: base mixin va uning roli

## Topshiriq sharti:
Dart 3 da faqat `base` klasslarga qo'shilishi mumkin bo'lgan `base mixin` yaratish.

## Yechim (Dart kodi):
```dart
base mixin BazaMixin {
  void bazaAmali() => print('Baza mixin amali bajarildi');
}

base class MeningKlassim with BazaMixin {}

void main() {
  var k = MeningKlassim();
  k.bazaAmali();
}
```

## Tushuntirish va Mantiq:
`base mixin` ulanayotgan sinf ham `base` yoki `final` bo'lishini talab qiladi va arxitektura barqarorligini ta'minlaydi.

## Ishlash natijasi:
```text
Baza mixin amali bajarildi
```

# 546-Topshiriq: Mixin orqali JSON serializatsiya

## Topshiriq sharti:
Obyektni Map shakliga aylantiruvchi yordamchi mixin tuzing.

## Yechim (Dart kodi):
```dart
mixin MapgaAylantiruvchi {
  Map<String, dynamic> toMap();
}

class Kitob with MapgaAylantiruvchi {
  final String nom;
  final int bet;

  Kitob(this.nom, this.bet);

  @override
  Map<String, dynamic> toMap() => {'nom': nom, 'bet': bet};
}

void main() {
  var k = Kitob('Dart 3 Qo\'llanmasi', 320);
  print(k.toMap());
}
```

## Tushuntirish va Mantiq:
Interfeys va mixin yordamida obyektlarni serializatsiya qilish qoidalari standartlashtiriladi.

## Ishlash natijasi:
```text
{nom: Dart 3 Qo'llanmasi, bet: 320}
```

# 547-Topshiriq: Domain-Driven Design da class modifikatorlari

## Topshiriq sharti:
Domain Entity larni `final` va `sealed` turlar orqali tashqi buzilishlardan himoyalash.

## Yechim (Dart kodi):
```dart
final class FoydalanuvchiId {
  final int qiymat;
  const FoydalanuvchiId(this.qiymat);
}

final class FoydalanuvchiEntity {
  final FoydalanuvchiId id;
  final String ism;

  FoydalanuvchiEntity(this.id, this.ism);
}

void main() {
  var u = FoydalanuvchiEntity(FoydalanuvchiId(1), 'Sardor');
  print('Foydalanuvchi: ${u.ism}, ID: ${u.id.qiymat}');
}
```

## Tushuntirish va Mantiq:
DDD arxitekturasida domen modellarini `final` qilib yopish kutilmagan vorislik xatolarini butunlay yo'q qiladi.

## Ishlash natijasi:
```text
Foydalanuvchi: Sardor, ID: 1
```

# 548-Topshiriq: sealed class yordamida CLI buyruqlar interpretatori

## Topshiriq sharti:
Konsol buyruqlarini (Help, Run, Exit) `sealed` tur orqali xavfsiz boshqaring.

## Yechim (Dart kodi):
```dart
sealed class CliBuyruq {}

class YordamBuyrugi extends CliBuyruq {}
class IshgaTushirishBuyrugi extends CliBuyruq {
  final String fayl;
  IshgaTushirishBuyrugi(this.fayl);
}
class ChiqishBuyrugi extends CliBuyruq {}

void bajarish(CliBuyruq cmd) {
  switch (cmd) {
    case YordamBuyrugi():
      print('Buyruqlar: run <fayl>, exit, help');
    case IshgaTushirishBuyrugi(:var fayl):
      print('Fayl ishga tushirildi: $fayl');
    case ChiqishBuyrugi():
      print('Dastur yakunlandi.');
  }
}

void main() {
  bajarish(IshgaTushirishBuyrugi('model.dart'));
  bajarish(ChiqishBuyrugi());
}
```

## Tushuntirish va Mantiq:
CLI ilovalarda har bir buyruq o'z parametrlariga ega bo'lib, sealed class orqali aniq ajratiladi.

## Ishlash natijasi:
```text
Fayl ishga tushirildi: model.dart
Dastur yakunlandi.
```

# 549-Topshiriq: FastMathMixin: Vektorlar ustida tezkor amallar

## Topshiriq sharti:
Skalyar ko'paytma va vektor normasini tezkor hisoblovchi mixin yozing.

## Yechim (Dart kodi):
```dart
import 'dart:math';

mixin FastMathMixin {
  double dotProduct(List<double> a, List<double> b) {
    double sum = 0.0;
    for (int i = 0; i < a.length; i++) {
      sum += a[i] * b[i];
    }
    return sum;
  }

  double norma(List<double> a) => sqrt(dotProduct(a, a));
}

class VektorHisoblagich with FastMathMixin {}

void main() {
  var vh = VektorHisoblagich();
  List<double> a = [3.0, 4.0];
  print('Vektor normasi: ${vh.norma(a)}');
}
```

## Tushuntirish va Mantiq:
Hisoblash modullarini mixin sifatida ajratish AI matematik algoritmlarini bir nechta sinfda qayta ishlatishga yordam beradi.

## Ishlash natijasi:
```text
Vektor normasi: 5.0
```

# 550-Topshiriq: BitNet 1-bit Kvantlash va De-kvantlash Mixini

## Topshiriq sharti:
FP32 aktivatsiyalarini ternar {-1, 0, +1} ga kvantlovchi TernaryQuantizationMixin tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:math';

mixin TernaryQuantizationMixin {
  List<int> quantizeTernary(List<double> weights, {double threshold = 0.5}) {
    // BitNet b1.58 kvantlash: AbsMax ga normallashtirib round(-1, 0, 1) qilish
    double absMax = weights.map((e) => e.abs()).reduce(max);
    if (absMax == 0) return List.filled(weights.length, 0);

    return weights.map((w) {
      double scaled = w / absMax;
      if (scaled > threshold) return 1;
      if (scaled < -threshold) return -1;
      return 0;
    }).toList();
  }
}

class BitNetModel with TernaryQuantizationMixin {
  void sinov() {
    List<double> fpWeights = [0.85, -0.92, 0.12, -0.05, 0.74];
    var ternary = quantizeTernary(fpWeights, threshold: 0.3);

    print('FP32 vaznlar: $fpWeights');
    print('BitNet 1-bit {-1, 0, 1} kvantlangan: $ternary');
  }
}

void main() {
  var model = BitNetModel();
  model.sinov();
}
```

## Tushuntirish va Mantiq:
BitNet b1.58 da har bir og'irlik faqat 3 ta holatda {-1, 0, 1} saqlanadi, bu esa xotirani 16 barobar tejaydi.

## Ishlash natijasi:
```text
FP32 vaznlar: [0.85, -0.92, 0.12, -0.05, 0.74]
BitNet 1-bit {-1, 0, 1} kvantlangan: [1, -1, 0, 0, 1]
```

