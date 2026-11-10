# 451-Topshiriq: Merosxo'rlik asoslari (extends kalit so'zi)

## Topshiriq sharti:
Ota klass (Hayvon) va undan meros oluvchi Bola klass (It) yarating, ota xususiyatlaridan foydalaning.

## Yechim (Dart kodi):
```dart
class Hayvon {
  final String nom;

  Hayvon(this.nom);

  void nafasOlish() => print('$nom nafas olmoqda.');
}

class It extends Hayvon {
  It(String nom) : super(nom);

  void vovullash() => print('$nom: Vov-vov!');
}

void main() {
  var bobik = It('Olapar');
  bobik.nafasOlish(); // Ota klass metodi
  bobik.vovullash();   // Bola klass metodi
}
```

## Tushuntirish va Mantiq:
`extends` kalit so'zi orqali bola klass ota klassning barcha ochiq maydon va metodlarini o'zlashtiradi.

## Ishlash natijasi:
```text
Olapar nafas olmoqda.
Olapar: Vov-vov!
```

# 452-Topshiriq: Super konstruktorni chaqirish

## Topshiriq sharti:
Ota klass konstruktori argument talab qilganda bola klass konstruktoridan `super(...)` orqali qiymat uzatishni ko'rsating.

## Yechim (Dart kodi):
```dart
class Shaxs {
  final String ism;
  final int yosh;

  Shaxs(this.ism, this.yosh);
}

class Xodim extends Shaxs {
  final double maosh;

  Xodim(String ism, int yosh, this.maosh) : super(ism, yosh);

  void info() {
    print('Xodim: $ism, Yoshi: $yosh, Maoshi: ${maosh.toStringAsFixed(0)} so\'m');
  }
}

void main() {
  var x = Xodim('Rustam', 29, 15000000);
  x.info();
}
```

## Tushuntirish va Mantiq:
Bola klass initsializatsiya qilinishidan oldin uning ota klassi konstruktori `super(ism, yosh)` orqali ishga tushiriladi.

## Ishlash natijasi:
```text
Xodim: Rustam, Yoshi: 29, Maoshi: 15000000 so'm
```

# 453-Topshiriq: Super-initializer formal parameters (Dart 2.17+)

## Topshiriq sharti:
Dartning zamonaviy `super.field` sintaksisi yordamida ota konstruktor parametrlarini ixcham uzating.

## Yechim (Dart kodi):
```dart
class Qurilma {
  final String brend;
  final double narx;

  Qurilma(this.brend, this.narx);
}

class Noutbuk extends Qurilma {
  final int ramGb;

  // super.brend va super.narx qisqartmasi
  Noutbuk(super.brend, super.narx, this.ramGb);

  @override
  String toString() => '$brend | ${ramGb}GB RAM | Narxi: ${narx.toStringAsFixed(0)} so\'m';
}

void main() {
  var n = Noutbuk('ThinkPad', 12000000, 32);
  print(n);
}
```

## Tushuntirish va Mantiq:
`super.brend` sintaksisi `String brend` va `: super(brend)` yozish o'rniga kodni ancha ixchamlashtiradi.

## Ishlash natijasi:
```text
ThinkPad | 32GB RAM | Narxi: 12000000 so'm
```

# 454-Topshiriq: Metodni qayta aniqlash (@override annotatsiyasi)

## Topshiriq sharti:
Ota klassdagi metodni bola klassda o'ziga xos mantiq bilan qayta yozishni (@override) ko'rsating.

## Yechim (Dart kodi):
```dart
class Transport {
  void harakatlanish() {
    print('Transport vositasi harakatlanmoqda.');
  }
}

class Samolyot extends Transport {
  @override
  void harakatlanish() {
    print('Samolyot osmonda uchmoqda.');
  }
}

void main() {
  Transport t = Samolyot();
  t.harakatlanish();
}
```

## Tushuntirish va Mantiq:
`@override` belgisi kompilyatorga ota klass metodini ataylab almashtirayotganimizni bildiradi va xatolardan saqlaydi.

## Ishlash natijasi:
```text
Samolyot osmonda uchmoqda.
```

# 455-Topshiriq: Ota metodni boladan chaqirish (super.metod())

## Topshiriq sharti:
Bola klass ota metodning ishini davom ettirishi uchun `super.metod()` dan qanday foydalanishini namoyish eting.

## Yechim (Dart kodi):
```dart
class Xabar {
  void chopEtish() {
    print('--- Boshlanish ---');
  }
}

class ChiroyliXabar extends Xabar {
  @override
  void chopEtish() {
    super.chopEtish(); // Ota klass ishini bajarish
    print('Maxsus bezatilgan xabar matni!');
    print('--- Yakun ---');
  }
}

void main() {
  var mx = ChiroyliXabar();
  mx.chopEtish();
}
```

## Tushuntirish va Mantiq:
`super.metod()` ota klassdagi asl logikani saqlab qolib, unga qo'shimcha yangi amallarni ulab qo'yish imkonini beradi.

## Ishlash natijasi:
```text
--- Boshlanish ---
Maxsus bezatilgan xabar matni!
--- Yakun ---
```

# 456-Topshiriq: Abstrakt klass va sof virtual metodlar

## Topshiriq sharti:
Bajarilishi majburiy bo'lgan metodlarga ega `abstract class` yarating va undan voris oling.

## Yechim (Dart kodi):
```dart
abstract class Shakl {
  // Tanasi yo'q abstrakt metod
  double yuzaHisobla();
}

class Kvadrat extends Shakl {
  final double tomon;

  Kvadrat(this.tomon);

  @override
  double yuzaHisobla() => tomon * tomon;
}

void main() {
  // Shakl s = Shakl(); // XATO: Abstrakt klassdan nusxa olinmaydi
  Shakl s = Kvadrat(6);
  print('Kvadrat yuzi: ${s.yuzaHisobla()}');
}
```

## Tushuntirish va Mantiq:
Abstrakt klasslar umumiy shartnoma (shablon) vazifasini o'taydi, ulardan bevosita obyekt yaratib bo'lmaydi.

## Ishlash natijasi:
```text
Kvadrat yuzi: 36.0
```

# 457-Topshiriq: Shablon Metod Naqshi (Template Method Pattern)

## Topshiriq sharti:
Abstrakt klassda umumiy algoritm skeletini yozib, ayrim qadamlarini voris klasslarga qoldiring.

## Yechim (Dart kodi):
```dart
abstract class MaqolaGenerator {
  void yaratish() {
    sarlavhaQoyish();
    tanaYozish();
    yakunlash();
  }

  void sarlavhaQoyish() => print('# Texnologiya yangiliklari');
  void tanaYozish(); // Abstrakt qadam
  void yakunlash() => print('Tahririyat: AI O\'zbekiston
');
}

class AiMaqola extends MaqolaGenerator {
  @override
  void tanaYozish() {
    print('BitNet 1-bit AI modellari mobil qurilmalarda tezkor ishlamoqda.');
  }
}

void main() {
  var maqola = AiMaqola();
  maqola.yaratish();
}
```

## Tushuntirish va Mantiq:
Template Method naqshida algoritmlarning tartibi ota sinfda belgilanadi, aniq qadamlar esa bolalarda amalga oshiriladi.

## Ishlash natijasi:
```text
# Texnologiya yangiliklari
BitNet 1-bit AI modellari mobil qurilmalarda tezkor ishlamoqda.
Tahririyat: AI O'zbekiston
```

# 458-Topshiriq: Dartda Implicit Interface (Klass interfeys sifatida)

## Topshiriq sharti:
Dartda alohida `interface` kalit so'zi yo'q bo'lsa-da, har qanday oddiy klass interfeys vazifasini o'tashini ko'rsating.

## Yechim (Dart kodi):
```dart
class ChopEtuvchi {
  void chop(String matn) {
    print('Standart chop: $matn');
  }
}

// Boshqa klass ChopEtuvchini interfeys sifatida qabul qiladi
class MaxsusChopEtuvchi implements ChopEtuvchi {
  @override
  void chop(String matn) {
    print('MAXSUS: >>> $matn <<<');
  }
}

void main() {
  ChopEtuvchi printer = MaxsusChopEtuvchi();
  printer.chop('Salom Dunyo');
}
```

## Tushuntirish va Mantiq:
Dartda har bir klass avtomatik ravishda o'zining barcha ommaviy a'zolarini o'z ichiga olgan yashirin interfeysga ega bo'ladi.

## Ishlash natijasi:
```text
MAXSUS: >>> Salom Dunyo <<<
```

# 459-Topshiriq: extends va implements farqi

## Topshiriq sharti:
Bir klass ikkinchisidan `extends` qilganda kodni meros olishi, `implements` qilganda esa barchasini qaytadan yozishi shartligini ko'rsating.

## Yechim (Dart kodi):
```dart
class Ota {
  void a() => print('Ota A');
  void b() => print('Ota B');
}

// extends: ota metodlarni bevosita ishlatadi
class Voris extends Ota {}

// implements: ota metodlar tanasi o'tmaydi, majburiy qayta yoziladi
class Interfeyschi implements Ota {
  @override
  void a() => print('Interfeyschi A');

  @override
  void b() => print('Interfeyschi B');
}

void main() {
  var v = Voris();
  v.a();
  v.b();

  var i = Interfeyschi();
  i.a();
  i.b();
}
```

## Tushuntirish va Mantiq:
`extends` kodni qayta ishlatish (reuse) uchun, `implements` esa shartnomani qat'iy bajarish uchun mo'ljallangan.

## Ishlash natijasi:
```text
Ota A
Ota B
Interfeyschi A
Interfeyschi B
```

# 460-Topshiriq: Bir nechta interfeyslarni amalga oshirish

## Topshiriq sharti:
Bitta klass bir vaqtning o'zida bir nechta interfeyslarni (`implements A, B`) joriy qilishini ko'rsating.

## Yechim (Dart kodi):
```dart
abstract class Uchuvchi {
  void uchish();
}

abstract class Suzuvchi {
  void suzish();
}

class Ordaq implements Uchuvchi, Suzuvchi {
  final String nom;

  Ordaq(this.nom);

  @override
  void uchish() => print('$nom havoga ko\'tarildi.');

  @override
  void suzish() => print('$nom suvda suzmoqda.');
}

void main() {
  var ordak = Ordaq('Yovvoyi o\'rdak');
  ordak.uchish();
  ordak.suzish();
}
```

## Tushuntirish va Mantiq:
Dart bitta ota klassdan meros olishga (`extends`) ruxsat bersa-da, bir nechta interfeysni (`implements`) cheklovsiz ulash mumkin.

## Ishlash natijasi:
```text
Yovvoyi o'rdak havoga ko'tarildi.
Yovvoyi o'rdak suvda suzmoqda.
```

# 461-Topshiriq: Polimorfizm asoslari

## Topshiriq sharti:
Umumiy ota tipidagi ro'yxatda har xil turdagi bola obyektlarni saqlash va ularning o'ziga xos harakatini ishga tushirish.

## Yechim (Dart kodi):
```dart
abstract class MusiqaAsbobi {
  void chalish();
}

class Gitara extends MusiqaAsbobi {
  @override
  void chalish() => print('Gitara: Dring-dring 🎸');
}

class Pianino extends MusiqaAsbobi {
  @override
  void chalish() => print('Pianino: Do-Re-Mi 🎹');
}

class Nogora extends MusiqaAsbobi {
  @override
  void chalish() => print('Nog\'ora: Gumbur-gumbur 🥁');
}

void main() {
  List<MusiqaAsbobi> orkestr = [Gitara(), Pianino(), Nogora()];

  for (var asbob in orkestr) {
    asbob.chalish(); // Dinamik polimorfizm
  }
}
```

## Tushuntirish va Mantiq:
Dastur orkestrdagi har bir element aynan qaysi sinf ekanligini bilmasdan turib, uning polimorfik metodini chaqira oladi.

## Ishlash natijasi:
```text
Gitara: Dring-dring 🎸
Pianino: Do-Re-Mi 🎹
Nog'ora: Gumbur-gumbur 🥁
```

# 462-Topshiriq: is va as operatorlari (Turlarni tekshirish va o'tkazish)

## Topshiriq sharti:
Obyektning turini `is` orqali tekshirish va uni xavfsiz `as` orqali mos tipga aylantirishni amalga oshiring.

## Yechim (Dart kodi):
```dart
abstract class Ishchi {}

class Muhandis extends Ishchi {
  void chizish() => print('Sxema chizilmoqda...');
}

class Menejer extends Ishchi {
  void rejalashtirish() => print('Reja tuzilmoqda...');
}

void ishBajar(Ishchi i) {
  if (i is Muhandis) {
    // Dart avtomatik ravishda type promotion qiladi!
    i.chizish();
  } else if (i is Menejer) {
    i.rejalashtirish();
  }
}

void main() {
  ishBajar(Muhandis());
  ishBajar(Menejer());
}
```

## Tushuntirish va Mantiq:
Dart kompilyatori `if (x is T)` tekshiruvidan so'ng o'zgaruvchini avtomatik ravishda `T` turiga aylantiradi (Type Promotion).

## Ishlash natijasi:
```text
Sxema chizilmoqda...
Reja tuzilmoqda...
```

# 463-Topshiriq: Abstrakt getter va setterlar

## Topshiriq sharti:
Abstrakt klassda faqat getter imzosi e'lon qilinishi va voris klassda u qanday hisoblanishi ko'rsatilsin.

## Yechim (Dart kodi):
```dart
abstract class Geometriya {
  double get perimetr;
}

class TengTomonliUchburchak extends Geometriya {
  final double a;

  TengTomonliUchburchak(this.a);

  @override
  double get perimetr => 3 * a;
}

void main() {
  Geometriya g = TengTomonliUchburchak(5.0);
  print('Perimetr: ${g.perimetr}');
}
```

## Tushuntirish va Mantiq:
Abstrakt xususiyatlar voris klasslarni muayyan getter/setterlarni joriy qilishga majbur etadi.

## Ishlash natijasi:
```text
Perimetr: 15.0
```

# 464-Topshiriq: Ota klassdagi named konstruktorni chaqirish

## Topshiriq sharti:
Ota klassdagi nomlangan konstruktorni bola klass orqali chaqirish (`super.named(...)`).

## Yechim (Dart kodi):
```dart
class Xabar {
  final String matn;
  final String tur;

  Xabar(this.matn) : tur = 'Oddiy';
  Xabar.shoshilinch(this.matn) : tur = 'Shoshilinch!';
}

class MaxsusXabar extends Xabar {
  final int daraja;

  MaxsusXabar.kritik(String matn)
      : daraja = 1,
        super.shoshilinch(matn);
}

void main() {
  var x = MaxsusXabar.kritik('Tizim serveri javob bermayapti');
  print('Turi: ${x.tur}, Darajasi: ${x.daraja}, Matn: ${x.matn}');
}
```

## Tushuntirish va Mantiq:
Bola klass ota klassning aynan qaysi konstruktori ishga tushishini `super.shoshilinch(...)` orqali aniq ko'rsata oladi.

## Ishlash natijasi:
```text
Turi: Shoshilinch!, Darajasi: 1, Matn: Tizim serveri javob bermayapti
```

# 465-Topshiriq: covariant kalit so'zi bilan parametrlarni toraytirish

## Topshiriq sharti:
Ota metod umumiy tip qabul qilganda, bola metod uni aniqroq voris tipga toraytirishi uchun `covariant` ishlatish.

## Yechim (Dart kodi):
```dart
class Yemish {}
class Gosht extends Yemish {}

class Yirtqich {
  void ovqatlanish(covariant Gosht yemak) {
    print('Yirtqich go\'sht yemoqda.');
  }
}

class Sher extends Yirtqich {
  @override
  void ovqatlanish(Gosht yemak) {
    print('Sher go\'shtni paqqos tushirdi.');
  }
}

void main() {
  var sher = Sher();
  sher.ovqatlanish(Gosht());
}
```

## Tushuntirish va Mantiq:
`covariant` kalit so'zi bola klasslarga ota metod parametrlari turini qonuniy ravishda toraytirish (subtyping) huquqini beradi.

## Ishlash natijasi:
```text
Sher go'shtni paqqos tushirdi.
```

# 466-Topshiriq: Geometrik figuralar polimorfizmi (Shape to'plami)

## Topshiriq sharti:
Shakl ota klassi, Doira va To'rtburchak sinflari hamda umumiy maydon hisoblovchi funksiyani yozing.

## Yechim (Dart kodi):
```dart
import 'dart:math';

abstract class Shakl {
  double yuza();
}

class Doira extends Shakl {
  final double r;
  Doira(this.r);

  @override
  double yuza() => pi * r * r;
}

class Tortburchak extends Shakl {
  final double eni, boyi;
  Tortburchak(this.eni, this.boyi);

  @override
  double yuza() => eni * boyi;
}

double jamiYuza(List<Shakl> shakllar) {
  return shakllar.fold(0.0, (sum, s) => sum + s.yuza());
}

void main() {
  List<Shakl> figuralar = [Doira(3.0), Tortburchak(4.0, 5.0)];
  print('Jami yuza: ${jamiYuza(figuralar).toStringAsFixed(2)}');
}
```

## Tushuntirish va Mantiq:
Yangi figurani qo'shish uchun `jamiYuza` funksiyasini o'zgartirish shart emas (Open-Closed Principle).

## Ishlash natijasi:
```text
Jami yuza: 48.27
```

# 467-Topshiriq: To'lov tizimlari interfeysi (Payme, Click, Uzum)

## Topshiriq sharti:
Yagona `TolovTizimi` interfeysi orqali Payme va Click to'lovlarini bir xil standartda qabul qilish.

## Yechim (Dart kodi):
```dart
abstract class TolovTizimi {
  String get provayderNomi;
  bool tolash(double summa);
}

class PaymeTolov implements TolovTizimi {
  @override
  String get provayderNomi => 'Payme';

  @override
  bool tolash(double summa) {
    print('$provayderNomi orqali ${summa.toStringAsFixed(0)} so\'m to\'landi.');
    return true;
  }
}

class ClickTolov implements TolovTizimi {
  @override
  String get provayderNomi => 'Click';

  @override
  bool tolash(double summa) {
    print('$provayderNomi orqali ${summa.toStringAsFixed(0)} so\'m to\'landi.');
    return true;
  }
}

void tolovQabulQilish(TolovTizimi provayder, double summa) {
  provayder.tolash(summa);
}

void main() {
  tolovQabulQilish(PaymeTolov(), 75000);
  tolovQabulQilish(ClickTolov(), 120000);
}
```

## Tushuntirish va Mantiq:
Interfeys yordamida to'lov qabul qiluvchi modul provayderning ichki tafsilotlariga bog'liq bo'lmaydi (Dependency Inversion).

## Ishlash natijasi:
```text
Payme orqali 75000 so'm to'landi.
Click orqali 120000 so'm to'landi.
```

# 468-Topshiriq: Bildirishnoma xizmatlari (NotificationService)

## Topshiriq sharti:
SMS va Push bildirishnomalar yuboruvchi umumiy interfeys va ularni bir vaqtda ishlatish.

## Yechim (Dart kodi):
```dart
abstract class BildirishnomaXizmati {
  void yuborish(String qabulQiluvchi, String xabar);
}

class SmsXizmati implements BildirishnomaXizmati {
  @override
  void yuborish(String qabulQiluvchi, String xabar) {
    print('SMS [$qabulQiluvchi]: $xabar');
  }
}

class PushXizmati implements BildirishnomaXizmati {
  @override
  void yuborish(String qabulQiluvchi, String xabar) {
    print('PUSH [$qabulQiluvchi]: $xabar');
  }
}

void main() {
  List<BildirishnomaXizmati> kanallar = [SmsXizmati(), PushXizmati()];
  for (var k in kanallar) {
    k.yuborish('user_42', 'Parolingiz yangilandi!');
  }
}
```

## Tushuntirish va Mantiq:
Foydalanuvchiga bitta xabarni barcha mavjud kanallar (SMS, Push) orqali yuborish osonlashadi.

## Ishlash natijasi:
```text
SMS [user_42]: Parolingiz yangilandi!
PUSH [user_42]: Parolingiz yangilandi!
```

# 469-Topshiriq: Repository Pattern va Ma'lumotlar interfeysi

## Topshiriq sharti:
Foydalanuvchilarni saqlovchi Repository interfeysi va uning Xotiradagi (In-Memory) implementatsiyasini tuzing.

## Yechim (Dart kodi):
```dart
abstract class FoydalanuvchiOmbori {
  void saqlash(int id, String ism);
  String? topish(int id);
}

class XotiraOmbori implements FoydalanuvchiOmbori {
  final Map<int, String> _baza = {};

  @override
  void saqlash(int id, String ism) => _baza[id] = ism;

  @override
  String? topish(int id) => _baza[id];
}

void main() {
  FoydalanuvchiOmbori ombor = XotiraOmbori();
  ombor.saqlash(1, 'Sardor');

  print('Topildi: ${ombor.topish(1)}');
  print('Topildi: ${ombor.topish(2)}');
}
```

## Tushuntirish va Mantiq:
Repository naqshi ma'lumotlar saqlanish joyini (RAM, SQLite, Server) ilova biznes mantiqidan ajratadi.

## Ishlash natijasi:
```text
Topildi: Sardor
Topildi: null
```

# 470-Topshiriq: Audio pleyer vositalari iyerarxiyasi

## Topshiriq sharti:
Turli formatdagi audio fayllarni o'ynatuvchi pleyer klasslar tizimini polimorfizm orqali tuzing.

## Yechim (Dart kodi):
```dart
abstract class AudioFayl {
  final String faylNomi;
  AudioFayl(this.faylNomi);
  void ijro();
}

class Mp3Fayl extends AudioFayl {
  Mp3Fayl(super.faylNomi);

  @override
  void ijro() => print('MP3 dekodlanmoqda va yangramoqda: $faylNomi');
}

class WavFayl extends AudioFayl {
  WavFayl(super.faylNomi);

  @override
  void ijro() => print('WAV siqilmagan audio oqimi ijro etilmoqda: $faylNomi');
}

void main() {
  List<AudioFayl> pleylist = [Mp3Fayl('qo\'shiq.mp3'), WavFayl('ovoz.wav')];
  for (var audio in pleylist) {
    audio.ijro();
  }
}
```

## Tushuntirish va Mantiq:
Har bir format o'ziga xos dekodlash mantiqiga ega, lekin tashqi pleyer uchun ularning barchasi `AudioFayl`dir.

## Ishlash natijasi:
```text
MP3 dekodlanmoqda va yangramoqda: qo'shiq.mp3
WAV siqilmagan audio oqimi ijro etilmoqda: ovoz.wav
```

# 471-Topshiriq: Liskov o'rinbosarlik prinsipi (LSP)

## Topshiriq sharti:
Voris klass ota klass o'rnida to'liq va kutilmagan xatolarsiz ishlay olishi tamoyilini namoyish eting.

## Yechim (Dart kodi):
```dart
abstract class Qush {
  void ovqatlanish() => print('Qush ozuqa termoqda.');
}

abstract class UchuvchiQush extends Qush {
  void uchish();
}

class Qaldirgoch extends UchuvchiQush {
  @override
  void uchish() => print('Qaldirg\'och havoda uchmoqda.');
}

class Pingvin extends Qush {
  void suzish() => print('Pingvin muzli suvda suzmoqda.');
}

void main() {
  Qush pingvin = Pingvin();
  pingvin.ovqatlanish();

  UchuvchiQush qaldirgoch = Qaldirgoch();
  qaldirgoch.uchish();
}
```

## Tushuntirish va Mantiq:
Agar Pingvin `UchuvchiQush`dan meros olib, xato tashlasa, LSP buziladi. Ierarxiyani to'g'ri bo'lish orqali bu muammo hal qilinadi.

## Ishlash natijasi:
```text
Qush ozuqa termoqda.
Qaldirg'och havoda uchmoqda.
```

# 472-Topshiriq: Super parametrlar bilan ixtiyoriy/nomlangan argumentlar

## Topshiriq sharti:
Ota klass nomlangan parametrlar qabul qilganda, bolada `super.param` qanday uzatilishini ko'rsating.

## Yechim (Dart kodi):
```dart
class BazaKomponent {
  final String id;
  final bool aktiv;

  BazaKomponent({required this.id, this.aktiv = true});
}

class Tugma extends BazaKomponent {
  final String matn;

  Tugma({required super.id, super.aktiv, required this.matn});

  @override
  String toString() => 'Tugma(id: $id, matn: "$matn", aktiv: $aktiv)';
}

void main() {
  var b1 = Tugma(id: 'btn_ok', matn: 'Tasdiqlash');
  var b2 = Tugma(id: 'btn_cancel', matn: 'Bekor qilish', aktiv: false);

  print(b1);
  print(b2);
}
```

## Tushuntirish va Mantiq:
Nomlangan parametrlar ham `super.param` orqali to'g'ridan-to'g'ri ota konstruktoriga uzatiladi.

## Ishlash natijasi:
```text
Tugma(id: btn_ok, matn: "Tasdiqlash", aktiv: true)
Tugma(id: btn_cancel, matn: "Bekor qilish", aktiv: false)
```

# 473-Topshiriq: Abstrakt klass konstruktori va uning roli

## Topshiriq sharti:
Abstrakt klassdan bevosita obyekt olinmasa ham, nega konstruktorga ega bo'lishini ko'rsatib bering.

## Yechim (Dart kodi):
```dart
abstract class Avtomobil {
  final String vinKod;
  final int ishlabChiqarilganYil;

  Avtomobil(this.vinKod, this.ishlabChiqarilganYil) {
    print('Avtomobil reestrdan o\'tkazilmoqda: VIN=$vinKod');
  }
}

class ElektrAvtomobil extends Avtomobil {
  final int batareyaKvt;

  ElektrAvtomobil(super.vinKod, super.ishlabChiqarilganYil, this.batareyaKvt);
}

void main() {
  var ev = ElektrAvtomobil('UZB1234567890', 2026, 75);
  print('Batareya sig\'imi: ${ev.batareyaKvt} kVt/soat');
}
```

## Tushuntirish va Mantiq:
Abstrakt klass konstruktori barcha voris klasslar uchun majburiy umumiy initsializatsiya va validatsiyani ta'minlaydi.

## Ishlash natijasi:
```text
Avtomobil reestrdan o'tkazilmoqda: VIN=UZB1234567890
Batareya sig'imi: 75 kVt/soat
```

# 474-Topshiriq: O'yin qahramonlari iyerarxiyasi (Hero, Warrior, Mage)

## Topshiriq sharti:
Qahramon (Hero) bazaviy klassi va jangchi (Warrior), sehrgar (Mage) sinflarini polimorfik hujum bilan modellashtiring.

## Yechim (Dart kodi):
```dart
abstract class Qahramon {
  final String ism;
  int jon;

  Qahramon(this.ism, this.jon);

  void zarbaBerish(Qahramon raqib);
}

class Jangchi extends Qahramon {
  Jangchi(super.ism, super.jon);

  @override
  void zarbaBerish(Qahramon raqib) {
    print('$ism qilich bilan chopdi (-25 HP)');
    raqib.jon -= 25;
  }
}

class Sehrgar extends Qahramon {
  Sehrgar(super.ism, super.jon);

  @override
  void zarbaBerish(Qahramon raqib) {
    print('$ism olovli shar otdi (-35 HP)');
    raqib.jon -= 35;
  }
}

void main() {
  var botir = Jangchi('Alpomish', 100);
  var jodugar = Sehrgar('Sehrgar', 80);

  botir.zarbaBerish(jodugar);
  jodugar.zarbaBerish(botir);

  print('${jodugar.ism} joni: ${jodugar.jon}');
  print('${botir.ism} joni: ${botir.jon}');
}
```

## Tushuntirish va Mantiq:
Polimorfik `zarbaBerish` metodi har bir qahramonning jang xususiyatlarini mustaqil boshqarishga imkon beradi.

## Ishlash natijasi:
```text
Alpomish qilich bilan chopdi (-25 HP)
Sehrgar olovli shar otdi (-35 HP)
Sehrgar joni: 55
Alpomish joni: 65
```

# 475-Topshiriq: UI vidjetlari daraxti simulyatsiyasi

## Topshiriq sharti:
Flutter vidjetlar daraxti prinsipiga o'xshash Widget, Text, Container abstrakt va aniq sinflarini tuzing.

## Yechim (Dart kodi):
```dart
abstract class Vidjet {
  void chizish(int burchak);
}

class MatnVidjet extends Vidjet {
  final String matn;
  MatnVidjet(this.matn);

  @override
  void chizish(int burchak) {
    print('${' ' * burchak}Text("$matn")');
  }
}

class KonteynerVidjet extends Vidjet {
  final List<Vidjet> bolalar;

  KonteynerVidjet(this.bolalar);

  @override
  void chizish(int burchak) {
    print('${' ' * burchak}Container:');
    for (var bola in bolalar) {
      bola.chizish(burchak + 2);
    }
  }
}

void main() {
  var ui = KonteynerVidjet([
    MatnVidjet('Sarlavha'),
    KonteynerVidjet([
      MatnVidjet('Ichki matn 1'),
      MatnVidjet('Ichki matn 2'),
    ]),
  ]);

  ui.chizish(0);
}
```

## Tushuntirish va Mantiq:
Kompozit (Composite Pattern) yordamida daraxtsimon iyerarxik interfeys tuzilmasi shakllantirildi.

## Ishlash natijasi:
```text
Container:
  Text("Sarlavha")
  Container:
    Text("Ichki matn 1")
    Text("Ichki matn 2")
```

# 476-Topshiriq: Strategiya Naqshi (Strategy Pattern)

## Topshiriq sharti:
Turli saralash usullarini (Tezkor va Ko'pikli) alohida strategiya interfeyslari orqali amalga oshiring.

## Yechim (Dart kodi):
```dart
abstract class SaralashStrategiyasi {
  List<int> saralash(List<int> royxat);
}

class KopikliSaralash implements SaralashStrategiyasi {
  @override
  List<int> saralash(List<int> royxat) {
    print('Ko\'pikli saralash algoritmi ishga tushdi.');
    var nusxa = List<int>.from(royxat);
    nusxa.sort(); // Simulyatsiya
    return nusxa;
  }
}

class SaralovchiKontekst {
  SaralashStrategiyasi strategiya;

  SaralovchiKontekst(this.strategiya);

  List<int> bajar(List<int> data) => strategiya.saralash(data);
}

void main() {
  var kontekst = SaralovchiKontekst(KopikliSaralash());
  var natija = kontekst.bajar([5, 2, 8, 1]);
  print('Natija: $natija');
}
```

## Tushuntirish va Mantiq:
Strategy pattern ilovadagi xulq-atvor yoki algoritmlarni alohida sinflarga ajratib, ularni istalgan vaqtda almashtirish imkonini beradi.

## Ishlash natijasi:
```text
Ko'pikli saralash algoritmi ishga tushdi.
Natija: [1, 2, 5, 8]
```

# 477-Topshiriq: Kuzatuvchi Naqshi (Observer Pattern)

## Topshiriq sharti:
Yangiliklar tarqatuvchi kanal va unga a'zo bo'lgan o'quvchilarni Observer interfeysi orqali tuzing.

## Yechim (Dart kodi):
```dart
abstract class Kuzatuvchi {
  void yangilanish(String xabar);
}

class YangiliklarKanali {
  final List<Kuzatuvchi> _obunachilar = [];

  void obunaBolish(Kuzatuvchi k) => _obunachilar.add(k);

  void yangilikYuborish(String yangilik) {
    print('Kanal: "$yangilik" e\'lon qilindi.');
    for (var k in _obunachilar) {
      k.yangilanish(yangilik);
    }
  }
}

class Foydalanuvchi implements Kuzatuvchi {
  final String ism;
  Foydalanuvchi(this.ism);

  @override
  void yangilanish(String xabar) => print('$ism bildirishnoma oldi: $xabar');
}

void main() {
  var kanal = YangiliklarKanali();
  kanal.obunaBolish(Foydalanuvchi('Akmal'));
  kanal.obunaBolish(Foydalanuvchi('Nodira'));

  kanal.yangilikYuborish('Dart 3.5 versiyasi taqdim etildi!');
}
```

## Tushuntirish va Mantiq:
Observer naqshi bir obyekt holati o'zgarganda unga bog'liq barcha obyektlarga xabar yetkazishni ta'minlaydi.

## Ishlash natijasi:
```text
Kanal: "Dart 3.5 versiyasi taqdim etildi!" e'lon qilindi.
Akmal bildirishnoma oldi: Dart 3.5 versiyasi taqdim etildi!
Nodira bildirishnoma oldi: Dart 3.5 versiyasi taqdim etildi!
```

# 478-Topshiriq: Holat Naqshi (State Pattern)

## Topshiriq sharti:
Buyurtmaning har xil holatlari (Yangi, Yetkazilmoqda, Yakunlandi) uchun State interfeysini joriy qiling.

## Yechim (Dart kodi):
```dart
abstract class BuyurtmaHolati {
  void keyingi(Buyurtma buyurtma);
  String get holatNomi;
}

class YangiHolat implements BuyurtmaHolati {
  @override
  String get holatNomi => 'Yangi';

  @override
  void keyingi(Buyurtma b) {
    b.holat = YetkazilmoqdaHolati();
  }
}

class YetkazilmoqdaHolati implements BuyurtmaHolati {
  @override
  String get holatNomi => 'Yetkazilmoqda';

  @override
  void keyingi(Buyurtma b) {
    b.holat = YakunlandiHolati();
  }
}

class YakunlandiHolati implements BuyurtmaHolati {
  @override
  String get holatNomi => 'Yakunlandi';

  @override
  void keyingi(Buyurtma b) {
    print('Buyurtma allaqachon yakunlangan!');
  }
}

class Buyurtma {
  BuyurtmaHolati holat = YangiHolat();
  void oldinga() => holat.keyingi(this);
}

void main() {
  var b = Buyurtma();
  print('Boshlang\'ich: ${b.holat.holatNomi}');
  b.oldinga();
  print('Keyingi: ${b.holat.holatNomi}');
  b.oldinga();
  print('Oxirgi: ${b.holat.holatNomi}');
}
```

## Tushuntirish va Mantiq:
State pattern obyektning ichki holati o'zgarganda uning xulq-atvorini polimorfik tarzda o'zgartiradi.

## Ishlash natijasi:
```text
Boshlang'ich: Yangi
Keyingi: Yetkazilmoqda
Oxirgi: Yakunlandi
```

# 479-Topshiriq: Buyruq Naqshi (Command Pattern)

## Topshiriq sharti:
Bajarish (`execute`) va bekor qilish (`undo`) amallariga ega Command interfeysini tuzing.

## Yechim (Dart kodi):
```dart
abstract class Buyruq {
  void ijro();
  void bekorQilish();
}

class Chiroq {
  void yoqish() => print('Chiroq yondi 💡');
  void ochirish() => print('Chiroq o\'chdi 🌑');
}

class ChiroqYoqishBuyrugi implements Buyruq {
  final Chiroq chiroq;
  ChiroqYoqishBuyrugi(this.chiroq);

  @override
  void ijro() => chiroq.yoqish();

  @override
  void bekorQilish() => chiroq.ochirish();
}

void main() {
  var lamp = Chiroq();
  Buyruq cmd = ChiroqYoqishBuyrugi(lamp);

  cmd.ijro();
  cmd.bekorQilish();
}
```

## Tushuntirish va Mantiq:
Command pattern amallarni obyekt ko'rinishida qadoqlab, ularni navbatga qo'yish yoki bekor qilish imkonini yaratadi.

## Ishlash natijasi:
```text
Chiroq yondi 💡
Chiroq o'chdi 🌑
```

# 480-Topshiriq: Adapter Naqshi (Adapter Pattern)

## Topshiriq sharti:
Eski tizim metodini zamonaviy interfeys talablariga moslashtiruvchi Adapter klassini yozing.

## Yechim (Dart kodi):
```dart
// Yangi interfeys
abstract class ZamonaviyMijoz {
  void sorovYuborish(String json);
}

// Eski sinf
class EskiXmlTizim {
  void sendXml(String xml) {
    print('Eski serverga yuborildi: $xml');
  }
}

// Adapter
class XmlToModernAdapter implements ZamonaviyMijoz {
  final EskiXmlTizim eski;
  XmlToModernAdapter(this.eski);

  @override
  void sorovYuborish(String json) {
    // JSON ni XML ga o'girish (simulyatsiya)
    String xml = '<data>$json</data>';
    eski.sendXml(xml);
  }
}

void main() {
  ZamonaviyMijoz client = XmlToModernAdapter(EskiXmlTizim());
  client.sorovYuborish('{"ism": "Anvar"}');
}
```

## Tushuntirish va Mantiq:
Adapter bir-biriga mos kelmaydigan interfeyslarni birgalikda ishlashiga imkon beradi.

## Ishlash natijasi:
```text
Eski serverga yuborildi: <data>{"ism": "Anvar"}</data>
```

# 481-Topshiriq: Bezakchi Naqshi (Decorator Pattern)

## Topshiriq sharti:
Asosiy qahva ichimligiga sut va shakar qo'shib uning narxi va tavsifini kengaytiruvchi Decorator tuzing.

## Yechim (Dart kodi):
```dart
abstract class Ichimlik {
  double narx();
  String tavsif();
}

class OddiyQahva implements Ichimlik {
  @override
  double narx() => 15000;

  @override
  String tavsif() => 'Oddiy Espresso';
}

class SutliBezak implements Ichimlik {
  final Ichimlik ichimlik;
  SutliBezak(this.ichimlik);

  @override
  double narx() => ichimlik.narx() + 5000;

  @override
  String tavsif() => '${ichimlik.tavsif()} + Sut';
}

void main() {
  Ichimlik kofe = OddiyQahva();
  kofe = SutliBezak(kofe);

  print('${kofe.tavsif()} = ${kofe.narx().toStringAsFixed(0)} so\'m');
}
```

## Tushuntirish va Mantiq:
Decorator mavjud obyektning funksionalligini dinamik ravishda kengaytirish uchun kompozitsiyadan foydalanadi.

## Ishlash natijasi:
```text
Oddiy Espresso + Sut = 20000 so'm
```

# 482-Topshiriq: Fabrika Metodi Naqshi (Factory Method Pattern)

## Topshiriq sharti:
Hujjat yaratuvchi abstrakt sinf va uning vorislari orqali turli formatdagi sahifalarni oching.

## Yechim (Dart kodi):
```dart
abstract class Sahifa {
  void korsatish();
}

class MatnSahifasi implements Sahifa {
  @override
  void korsatish() => print('Matn sahifasi ochildi.');
}

abstract class HujjatYaratuvchi {
  Sahifa sahifaYarat(); // Factory method

  void ochish() {
    var p = sahifaYarat();
    p.korsatish();
  }
}

class MatnHujjat extends HujjatYaratuvchi {
  @override
  Sahifa sahifaYarat() => MatnSahifasi();
}

void main() {
  HujjatYaratuvchi doc = MatnHujjat();
  doc.ochish();
}
```

## Tushuntirish va Mantiq:
Factory Method aniq sinflarni yaratish vazifasini voris klasslarga topshiradi.

## Ishlash natijasi:
```text
Matn sahifasi ochildi.
```

# 483-Topshiriq: Proksi Naqshi (Proxy Pattern - Keshlovchi vositachi)

## Topshiriq sharti:
Og'ir tasvir faylini faqat kerak bo'lgandagina xotiraga yuklovchi Proksi klassini tuzing.

## Yechim (Dart kodi):
```dart
abstract class Rasm {
  void korsatish();
}

class HaqiqiyRasm implements Rasm {
  final String faylNomi;

  HaqiqiyRasm(this.faylNomi) {
    print('Diskdan yuklanmoqda: $faylNomi');
  }

  @override
  void korsatish() => print('Rasm ekranda: $faylNomi');
}

class ProksiRasm implements Rasm {
  final String faylNomi;
  HaqiqiyRasm? _haqiqiy;

  ProksiRasm(this.faylNomi);

  @override
  void korsatish() {
    _haqiqiy ??= HaqiqiyRasm(faylNomi); // Lazy loading
    _haqiqiy!.korsatish();
  }
}

void main() {
  Rasm rasm = ProksiRasm('kotta_surat.jpg');
  print('Proksi yaratildi, rasm hali yuklanmadi.');
  rasm.korsatish();
}
```

## Tushuntirish va Mantiq:
Proxy haqiqiy obyekt oldida turib, unga murojaatlarni nazorat qiladi va faqat zarur bo'lganda yuklaydi.

## Ishlash natijasi:
```text
Proksi yaratildi, rasm hali yuklanmadi.
Diskdan yuklanmoqda: kotta_surat.jpg
Rasm ekranda: kotta_surat.jpg
```

# 484-Topshiriq: Iterator interfeysini amalga oshirish

## Topshiriq sharti:
Dart standart `Iterator<T>` va `Iterable<T>` interfeyslarini o'z shaxsiy to'plamingiz uchun joriy qiling.

## Yechim (Dart kodi):
```dart
class JuftSonlar extends Iterable<int> {
  final int chegara;
  JuftSonlar(this.chegara);

  @override
  Iterator<int> get iterator => _JuftSonlarIterator(chegara);
}

class _JuftSonlarIterator implements Iterator<int> {
  final int chegara;
  int _joriy = 0;

  _JuftSonlarIterator(this.chegara);

  @override
  int get current => _joriy;

  @override
  bool moveNext() {
    _joriy += 2;
    return _joriy <= chegara;
  }
}

void main() {
  var juftlar = JuftSonlar(10);
  for (var son in juftlar) {
    print('Juft son: $son');
  }
}
```

## Tushuntirish va Mantiq:
`Iterable` interfeysi orqali yaratilgan obyektlar avtomatik `for..in` siklida, `map`, `where` metodlarida ishlaydi.

## Ishlash natijasi:
```text
Juft son: 2
Juft son: 4
Juft son: 6
Juft son: 8
Juft son: 10
```

# 485-Topshiriq: Shartnomaviy dasturlash (Design by Contract)

## Topshiriq sharti:
Metod bajarilishidan oldin va keyin shartlarni assert yoki istisnolar bilan tekshiruvchi interfeys tuzing.

## Yechim (Dart kodi):
```dart
abstract class BankTranzaksiya {
  void pulYechish(double miqdor);
}

class XavfsizTranzaksiya implements BankTranzaksiya {
  double balans = 100000;

  @override
  void pulYechish(double miqdor) {
    // Old shart (Pre-condition)
    assert(miqdor > 0, 'Miqdor musbat bo\'lishi kerak');
    assert(miqdor <= balans, 'Mablag\' yetarli emas');

    balans -= miqdor;

    // Yakuniy shart (Post-condition)
    assert(balans >= 0, 'Balans manfiy bo\'lib qolishi mumkin emas');
    print('Muvaffaqiyatli yechildi: $miqdor. Qoldiq: $balans');
  }
}

void main() {
  var t = XavfsizTranzaksiya();
  t.pulYechish(40000);
}
```

## Tushuntirish va Mantiq:
Shartnomaviy dasturlash kodning ishonchliligini va ma'lumotlar yaxlitligini ta'minlaydi.

## Ishlash natijasi:
```text
Muvaffaqiyatli yechildi: 40000.0. Qoldiq: 60000.0
```

# 486-Topshiriq: Bo'sh Obyekt Naqshi (Null Object Pattern)

## Topshiriq sharti:
Null qiymat qaytargandan ko'ra xavfsiz bo'sh harakat qiluvchi NullLogger obyektini tuzing.

## Yechim (Dart kodi):
```dart
abstract class Logger {
  void yozish(String xabar);
}

class HaqiqiyLogger implements Logger {
  @override
  void yozish(String xabar) => print('[LOG] $xabar');
}

class Bo'shLogger implements Logger {
  @override
  void yozish(String xabar) {
    // Hech narsa qilmaydi (No-op)
  }
}

void main() {
  Logger log = Bo'shLogger(); // Null o'rniga xavfsiz obyekt
  log.yozish('Bu yozuv chiqmaydi');
  print('Dastur hech qanday xatoliksiz davom etdi.');
}
```

## Tushuntirish va Mantiq:
Null Object Pattern null tekshiruvlarini kamaytiradi va kodni toza saqlaydi.

## Ishlash natijasi:
```text
Dastur hech qanday xatoliksiz davom etdi.
```

# 487-Topshiriq: Ko'p qatlamli merosxo'rlik zanjiri (A -> B -> C)

## Topshiriq sharti:
YashashTuri -> Umurtqali -> Sutemizuvchi iyerarxiyasida xususiyatlarning uzatilishini ko'rsating.

## Yechim (Dart kodi):
```dart
class TirikMavjudot {
  void nafas() => print('Kislorod olmoqda');
}

class Umurtqali extends TirikMavjudot {
  void suyakTuzilishi() => print('Umurtqa pog\'onasiga ega');
}

class Sutemizuvchi extends Umurtqali {
  void sutBilanOziqlantirish() => print('Bolalarini sut bilan boqadi');
}

void main() {
  var kiyik = Sutemizuvchi();
  kiyik.nafas();
  kiyik.suyakTuzilishi();
  kiyik.sutBilanOziqlantirish();
}
```

## Tushuntirish va Mantiq:
Ko'p bosqichli merosxo'rlikda eng quyi klass zanjirdagi barcha ota sinflar xususiyatlarini o'zlashtiradi.

## Ishlash natijasi:
```text
Kislorod olmoqda
Umurtqa pog'onasiga ega
Bolalarini sut bilan boqadi
```

# 488-Topshiriq: Abstrakt sinfda statik utility metodlar

## Topshiriq sharti:
Abstrakt sinfda faqat vorislar uchun emas, barcha uchun ochiq yordamchi statik metodlar yaratish.

## Yechim (Dart kodi):
```dart
abstract class MatematikaUtility {
  static double ortacha(List<num> sonlar) {
    if (sonlar.isEmpty) return 0.0;
    return sonlar.reduce((a, b) => a + b) / sonlar.length;
  }
}

void main() {
  var sonlar = [10, 20, 30, 40];
  print('O\'rtacha: ${MatematikaUtility.ortacha(sonlar)}');
}
```

## Tushuntirish va Mantiq:
Abstrakt sinflar statik yordamchi vositalarni (Namespace sifatida) guruhlash uchun qulaydir.

## Ishlash natijasi:
```text
O'rtacha: 25.0
```

# 489-Topshiriq: Kompozitsiya merosxo'rlikdan afzalroq tamoyili

## Topshiriq sharti:
Meros olish o'rniga komponentlarni maydon sifatida saqlash orqali moslashuvchanlikni oshirish.

## Yechim (Dart kodi):
```dart
class Dvigatel {
  void start() => print('Dvigatel ishga tushdi.');
}

class Mashina {
  final Dvigatel dvigatel; // Kompozitsiya

  Mashina(this.dvigatel);

  void yurish() {
    dvigatel.start();
    print('Mashina yo\'lga chiqdi.');
  }
}

void main() {
  var mashina = Mashina(Dvigatel());
  mashina.yurish();
}
```

## Tushuntirish va Mantiq:
Merosxo'rlik qattiq bog'liqlik keltirib chiqaradi, kompozitsiya esa qismlarni oson almashtirish imkonini beradi.

## Ishlash natijasi:
```text
Dvigatel ishga tushdi.
Mashina yo'lga chiqdi.
```

# 490-Topshiriq: Dinamik dispatch mexanizmi

## Topshiriq sharti:
Kompilyatsiya vaqtida noma'lum bo'lgan metod bajarilishi ish vaqtida obyekt turiga ko'ra aniqlanishini tekshiring.

## Yechim (Dart kodi):
```dart
abstract class Shakl {
  void kimman() => print('Men shaklman');
}

class Aylana extends Shakl {
  @override
  void kimman() => print('Men aylanaman');
}

void aniqla(Shakl s) {
  s.kimman(); // Dinamik dispatch
}

void main() {
  aniqla(Aylana());
}
```

## Tushuntirish va Mantiq:
Dinamik dispatch runtime vaqtida chaqirilayotgan obyektning haqiqiy klassi vtable orqali to'g'ri metodga yo'naltirilishini ta'minlaydi.

## Ishlash natijasi:
```text
Men aylanaman
```

# 491-Topshiriq: Bir xil nomli metodlar to'qnashuvi interfeyslarda

## Topshiriq sharti:
Ikkita interfeys bir xil nomli metodga ega bo'lganda voris klass uni yagona usulda qanday amalga oshiradi.

## Yechim (Dart kodi):
```dart
abstract class Alfa {
  void salom();
}

abstract class Beta {
  void salom();
}

class Gamma implements Alfa, Beta {
  @override
  void salom() {
    print('Alfa va Beta interfeyslari uchun yagona salom');
  }
}

void main() {
  var g = Gamma();
  g.salom();
}
```

## Tushuntirish va Mantiq:
Dartda bir xil imzoga ega interfeys metodlari bitta umumiy `@override` orqali ikkalasini ham qanoatlantiradi.

## Ishlash natijasi:
```text
Alfa va Beta interfeyslari uchun yagona salom
```

# 492-Topshiriq: Kesh xotira interfeysi (CacheStorage)

## Topshiriq sharti:
Xotira va disk uchun umumiy `KeshSaqlagich` interfeysini joriy qiling.

## Yechim (Dart kodi):
```dart
abstract class KeshSaqlagich {
  void yozish(String k, String v);
  String? oqish(String k);
}

class XotiraKesh implements KeshSaqlagich {
  final Map<String, String> _map = {};

  @override
  void yozish(String k, String v) => _map[k] = v;

  @override
  String? oqish(String k) => _map[k];
}

void main() {
  KeshSaqlagich k = XotiraKesh();
  k.yozish('til', 'uzbek');
  print('Kesh: ${k.oqish("til")}');
}
```

## Tushuntirish va Mantiq:
Interfeys yordamida dastur kesh qayerda saqlanishidan qat'i nazar bir xil ishlaydi.

## Ishlash natijasi:
```text
Kesh: uzbek
```

# 493-Topshiriq: Kriptografik shifrlash interfeysi

## Topshiriq sharti:
Turli shifrlash usullari uchun (XOR va Teskari matn) umumiy Shifrlagich interfeysi tuzing.

## Yechim (Dart kodi):
```dart
abstract class Shifrlagich {
  String shifrlash(String matn);
}

class TeskariShifr implements Shifrlagich {
  @override
  String shifrlash(String matn) => matn.split('').reversed.join('');
}

void main() {
  Shifrlagich sh = TeskariShifr();
  print('Shifrlangan: ${sh.shifrlash("Salom")}');
}
```

## Tushuntirish va Mantiq:
Shifrlash algoritmlarini alohida interfeys orqali amalga oshirish xavfsizlik modullarini oson yangilashga yordam beradi.

## Ishlash natijasi:
```text
Shifrlangan: molaS
```

# 494-Topshiriq: Log yozish interfeysi (LogAppender)

## Topshiriq sharti:
Konsolga va buferga yozuvchi turli log xizmatlari interfeysini tuzing.

## Yechim (Dart kodi):
```dart
abstract class LogChiqaruvchi {
  void yoz(String msg);
}

class KonsolChiqaruvchi implements LogChiqaruvchi {
  @override
  void yoz(String msg) => print('[Konsol]: $msg');
}

void main() {
  LogChiqaruvchi l = KonsolChiqaruvchi();
  l.yoz('Ish muvaffaqiyatli yakunlandi');
}
```

## Tushuntirish va Mantiq:
Log interfeysi yordamida ilova xabarlarini istalgan manzilga yo'naltirish mumkin.

## Ishlash natijasi:
```text
[Konsol]: Ish muvaffaqiyatli yakunlandi
```

# 495-Topshiriq: Tarmoq so'rovi mijozi interfeysi

## Topshiriq sharti:
Testlarda server o'rniga soxta ma'lumot beruvchi TarmoqMijozi interfeysi va uning Mock nusxasi.

## Yechim (Dart kodi):
```dart
abstract class TarmoqMijozi {
  String get(String url);
}

class TestMijozi implements TarmoqMijozi {
  @override
  String get(String url) => '{"status": "ok", "url": "$url"}';
}

void main() {
  TarmoqMijozi client = TestMijozi();
  print(client.get('/api/users'));
}
```

## Tushuntirish va Mantiq:
Interfeyslar yordamida unit-testlarda internet ulanishisiz tez va ishonchli sinovlar o'tkaziladi.

## Ishlash natijasi:
```text
{"status": "ok", "url": "/api/users"}
```

# 496-Topshiriq: Grafika renderlash dvigateli (Renderer)

## Topshiriq sharti:
2D va Matnli shakllarni ekranga chizuvchi abstrakt vosita tuzing.

## Yechim (Dart kodi):
```dart
abstract class Renderchi {
  void render(String shaklNomi);
}

class MatnliRenderchi implements Renderchi {
  @override
  void render(String shaklNomi) => print('[RENDER] Chizilmoqda: $shaklNomi');
}

void main() {
  Renderchi r = MatnliRenderchi();
  r.render('Kub 3D');
}
```

## Tushuntirish va Mantiq:
Grafika dvigatellari interfeyslar orqali platformaga xos kutubxonalardan mustaqil qilinadi.

## Ishlash natijasi:
```text
[RENDER] Chizilmoqda: Kub 3D
```

# 497-Topshiriq: Matn parse qilish va tokenizatsiya interfeysi

## Topshiriq sharti:
Turli qoidalarga ko'ra matnni so'zlarga bo'luvchi Tokenizator interfeysi tuzing.

## Yechim (Dart kodi):
```dart
abstract class Tokenizator {
  List<String> ajratish(String matn);
}

class BoshJoyTokenizator implements Tokenizator {
  @override
  List<String> ajratish(String matn) => matn.trim().split(RegExp(r'\s+'));
}

void main() {
  Tokenizator t = BoshJoyTokenizator();
  print(t.ajratish('AI model Dart tilida'));
}
```

## Tushuntirish va Mantiq:
Tokenizator interfeysi AI tabiiy til tahlilida turli tillarga xos segmentatorlarni oson almashtirish imkonini beradi.

## Ishlash natijasi:
```text
[AI, model, Dart, tilida]
```

# 498-Topshiriq: Sensor drayveri interfeysi

## Topshiriq sharti:
Akselerometr va Giroskop sensorlari uchun umumiy interfeys va o'qish amallari.

## Yechim (Dart kodi):
```dart
abstract class Sensor {
  String get sensorTuri;
  List<double> oqish();
}

class Akselerometr implements Sensor {
  @override
  String get sensorTuri => 'Akselerometr';

  @override
  List<double> oqish() => [0.0, 9.8, 0.1];
}

void main() {
  Sensor s = Akselerometr();
  print('${s.sensorTuri} ko\'rsatkichlari: ${s.oqish()}');
}
```

## Tushuntirish va Mantiq:
Mobil qurilmalarning turli sensorlari yagona interfeys orqali ilovaga ma'lumot uzatadi.

## Ishlash natijasi:
```text
Akselerometr ko'rsatkichlari: [0.0, 9.8, 0.1]
```

# 499-Topshiriq: Neft-gaz quvurlari va klapanlar polimorfizmi

## Topshiriq sharti:
Klapan interfeysi orqali ochiq, yopiq va sozlanuvchi kranlar oqimini polimorfik boshqaring.

## Yechim (Dart kodi):
```dart
abstract class Klapan {
  void ochish();
  void yopish();
  bool get ochiqmi;
}

class SharikliKlapan implements Klapan {
  bool _holat = false;

  @override
  void ochish() {
    _holat = true;
    print('Klapan ochildi.');
  }

  @override
  void yopish() {
    _holat = false;
    print('Klapan yopildi.');
  }

  @override
  bool get ochiqmi => _holat;
}

void main() {
  Klapan k = SharikliKlapan();
  k.ochish();
  print('Ochiq holat: ${k.ochiqmi}');
}
```

## Tushuntirish va Mantiq:
Sanoat avtomatizatsiyasida apparatura boshqaruvi polimorfik interfeyslar orqali amalga oshiriladi.

## Ishlash natijasi:
```text
Klapan ochildi.
Ochiq holat: true
```

# 500-Topshiriq: BitNet Transformer Qatlami Polimorfik Abstraksiyasi

## Topshiriq sharti:
Ternar {-1,0,1} vaznlar bilan ishlovchi polimorfik TransformerLayer va TernaryFeedForward sinflarini tuzing.

## Yechim (Dart kodi):
```dart
abstract class TransformerLayer {
  List<double> forward(List<double> input);
}

class TernaryFeedForward extends TransformerLayer {
  final int dModel;
  final List<int> ternaryWeights; // -1, 0, +1

  TernaryFeedForward(this.dModel, this.ternaryWeights);

  @override
  List<double> forward(List<double> input) {
    List<double> output = List.filled(dModel, 0.0);
    for (int i = 0; i < dModel; i++) {
      double sum = 0.0;
      for (int j = 0; j < dModel; j++) {
        int w = ternaryWeights[i * dModel + j];
        if (w == 1) sum += input[j];
        if (w == -1) sum -= input[j];
      }
      output[i] = sum;
    }
    return output;
  }
}

void main() {
  // 2x2 Ternary FeedForward
  var ff = TernaryFeedForward(2, [1, -1, 0, 1]);
  var res = ff.forward([4.0, 1.5]);

  print('Ternary Transformer Layer chiqishi: $res');
}
```

## Tushuntirish va Mantiq:
BitNet arxitekturasida barcha qatlamlar `TransformerLayer` interfeysidan voris oladi va ternar GEMV hisobini polimorfik bajaradi.

## Ishlash natijasi:
```text
Ternary Transformer Layer chiqishi: [2.5, 1.5]
```

