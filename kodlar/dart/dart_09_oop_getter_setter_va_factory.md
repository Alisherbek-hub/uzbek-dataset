# 401-Topshiriq: Getter asoslari (get kalit so'zi)

## Topshiriq sharti:
Tug'ilgan yil asosida joriy yoshni hisoblab beruvchi `yosh` getteriga ega Inson klassini tuzing.

## Yechim (Dart kodi):
```dart
class Inson {
  final String ism;
  final int tugilganYil;

  Inson(this.ism, this.tugilganYil);

  // Getter hisoblanadigan xususiyat qaytaradi
  int get yosh => DateTime.now().year - tugilganYil;
}

void main() {
  var odam = Inson('Nodir', 1998);
  print('${odam.ism}ning yoshi: ${odam.yosh} da');
}
```

## Tushuntirish va Mantiq:
`get` kalit so'zi orqali xususiyatga oddiy maydon kabi murojaat qilinadi, lekin u orqa fonda funksiya kabi hisoblanadi.

## Ishlash natijasi:
```text
Nodirning yoshi: 28 da
```

# 402-Topshiriq: Setter asoslari va qiymat validatsiyasi

## Topshiriq sharti:
Foydalanuvchi yoshini faqat musbat va 120 dan oshmagan holda o'rnatishga ruxsat beruvchi setter yozing.

## Yechim (Dart kodi):
```dart
class Foydalanuvchi {
  int _yosh = 0;

  int get yosh => _yosh;

  set yosh(int qiymat) {
    if (qiymat < 0 || qiymat > 120) {
      print('Xatolik: Noto\'g\'ri yosh ($qiymat)! Qiymat o\'zgarmadi.');
    } else {
      _yosh = qiymat;
    }
  }
}

void main() {
  var u = Foydalanuvchi();
  u.yosh = 25;
  print('O\'rnatilgan yosh: ${u.yosh}');

  u.yosh = -5;
  print('Oxirgi yosh: ${u.yosh}');
}
```

## Tushuntirish va Mantiq:
Setter orqali maydonga yangi qiymat berilganda avval shartlar tekshiriladi, bu inkapsulyatsiyaning asosiy qoidasidir.

## Ishlash natijasi:
```text
O'rnatilgan yosh: 25
Xatolik: Noto'g'ri yosh (-5)! Qiymat o'zgarmadi.
Oxirgi yosh: 25
```

# 403-Topshiriq: Getter va Setter birgalikda (Xavfsiz bank balansi)

## Topshiriq sharti:
Bank balansi manfiy bo'lishiga yo'l qo'ymaydigan getter va setter juftligini amalga oshiring.

## Yechim (Dart kodi):
```dart
class Hisob {
  double _balans = 0.0;

  double get balans => _balans;

  set balans(double yangiBalans) {
    if (yangiBalans < 0) {
      throw ArgumentError('Balans manfiy bo\'lishi mumkin emas!');
    }
    _balans = yangiBalans;
  }
}

void main() {
  var h = Hisob();
  h.balans = 150000;
  print('Balans: ${h.balans} so\'m');

  try {
    h.balans = -500;
  } catch (e) {
    print('Ushlangan xato: $e');
  }
}
```

## Tushuntirish va Mantiq:
Agar setterga noto'g'ri qiymat uzatilsa, `ArgumentError` tashlash orqali noto'g'ri ma'lumotlar saqlanishining oldi olinadi.

## Ishlash natijasi:
```text
Balans: 150000.0 so'm
Ushlangan xato: Invalid argument(s): Balans manfiy bo'lishi mumkin emas!
```

# 404-Topshiriq: Faqat o'qiladigan xususiyat (Read-only property)

## Topshiriq sharti:
Foydalanuvchining to'liq ismi (ism + familiya) va ID raqamini faqat o'qish mumkin bo'lgan klass tuzing.

## Yechim (Dart kodi):
```dart
class Shaxs {
  final String ism;
  final String familiya;
  final int id;

  Shaxs(this.ism, this.familiya, this.id);

  // Faqat o'qiladigan hisoblanadigan getter
  String get toliqIsm => '$ism $familiya';
}

void main() {
  var sh = Shaxs('Dilshod', 'Karimov', 1042);
  print('ID: ${sh.id}');
  print('F.I.SH: ${sh.toliqIsm}');
}
```

## Tushuntirish va Mantiq:
Klassda getter bor, ammo mos setter yo'q bo'lsa, xususiyat faqat o'qish rejimida bo'ladi (read-only property).

## Ishlash natijasi:
```text
ID: 1042
F.I.SH: Dilshod Karimov
```

# 405-Topshiriq: Doira yuzi va perimetri getterlari

## Topshiriq sharti:
Radius berilganda doira yuzi va aylana uzunligini getterlar orqali hisoblab beruvchi Doira klassini tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:math';

class Doira {
  double radius;

  Doira(this.radius);

  double get yuzi => pi * radius * radius;
  double get perimetr => 2 * pi * radius;
}

void main() {
  var d = Doira(5.0);
  print('Radius: ${d.radius}');
  print('Maydoni: ${d.yuzi.toStringAsFixed(2)}');
  print('Perimetri: ${d.perimetr.toStringAsFixed(2)}');

  d.radius = 10.0;
  print('
Radius o\'zgardi: ${d.radius}');
  print('Yangi maydon: ${d.yuzi.toStringAsFixed(2)}');
}
```

## Tushuntirish va Mantiq:
Radius o'zgarganda getterlar har gal chaqirilganda yangi qiymatni hisoblab beradi, alohida metod chaqirish shart emas.

## Ishlash natijasi:
```text
Radius: 5.0
Maydoni: 78.54
Perimetri: 31.42

Radius o'zgardi: 10.0
Yangi maydon: 314.16
```

# 406-Topshiriq: Harorat klassi getter va setterlari (Celsius <-> Fahrenheit)

## Topshiriq sharti:
Bitta maydonga ega, biroq ham Celsius, ham Fahrenheit bo'yicha qiymat o'qish va yozish imkonini beruvchi klass tuzing.

## Yechim (Dart kodi):
```dart
class Harorat {
  double _celsius = 0.0;

  double get celsius => _celsius;
  set celsius(double c) => _celsius = c;

  double get fahrenheit => (_celsius * 9 / 5) + 32;
  set fahrenheit(double f) => _celsius = (f - 32) * 5 / 9;
}

void main() {
  var t = Harorat();
  t.celsius = 25.0;
  print('25°C -> ${t.fahrenheit}°F');

  t.fahrenheit = 212.0;
  print('212°F -> ${t.celsius}°C');
}
```

## Tushuntirish va Mantiq:
Ichki holat bitta birlikda saqlanadi, ikkinchi birlik esa getter va setter formulalari orqali virtual ko'rinishda taqdim etiladi.

## Ishlash natijasi:
```text
25°C -> 77.0°F
212°F -> 100.0°C
```

# 407-Topshiriq: Oylik va yillik maosh bog'liqligi

## Topshiriq sharti:
Oylik maosh orqali yillik maoshni o'qish va aksincha yillik maosh orqali oylikni belgilovchi Maosh klassini yozing.

## Yechim (Dart kodi):
```dart
class Maosh {
  double oylik;

  Maosh(this.oylik);

  double get yillik => oylik * 12;
  set yillik(double jami) => oylik = jami / 12;
}

void main() {
  var m = Maosh(5000000);
  print('Oylik: ${m.oylik} -> Yillik: ${m.yillik}');

  m.yillik = 120000000;
  print('Yillik 120 mln -> Yangi oylik: ${m.oylik}');
}
```

## Tushuntirish va Mantiq:
Getter va setterlar o'zaro bog'liq tushunchalarni dasturchi uchun juda qulay sintaksisda boshqarishga imkon beradi.

## Ishlash natijasi:
```text
Oylik: 5000000.0 -> Yillik: 60000000.0
Yillik 120 mln -> Yangi oylik: 10000000.0
```

# 408-Topshiriq: Factory konstruktor asoslari

## Topshiriq sharti:
Oddiy konstruktor yangi nusxa qaytarsa, factory konstruktor qachon va qanday maqsadda ishlatilishini ko'rsating.

## Yechim (Dart kodi):
```dart
class Shakl {
  final String tur;

  // Private generative constructor
  Shakl._ichki(this.tur);

  // Factory constructor mavjud yoki maxsus nusxani qaytarishi mumkin
  factory Shakl(String tur) {
    if (tur.toLowerCase() == 'aylana') {
      return Shakl._ichki('Aylana shakli');
    } else {
      return Shakl._ichki('Oddiy ko\'pburchak: $tur');
    }
  }
}

void main() {
  var s1 = Shakl('aylana');
  var s2 = Shakl('uchburchak');

  print(s1.tur);
  print(s2.tur);
}
```

## Tushuntirish va Mantiq:
`factory` konstruktori yangi obyekt yaratish majburiyatida emas; u keshdan, subklassdan yoki shartga ko'ra mavjud obyektni qaytarishi mumkin.

## Ishlash natijasi:
```text
Aylana shakli
Oddiy ko'pburchak: uchburchak
```

# 409-Topshiriq: Factory konstruktor orqali Singleton Pattern

## Topshiriq sharti:
Ilova davomida bitta global nusxada mavjud bo'ladigan DatabaseConnection klassini factory orqali amalga oshiring.

## Yechim (Dart kodi):
```dart
class MalumotlarBazasi {
  final String ulanishUrl;
  static MalumotlarBazasi? _nusxa;

  // Private konstruktor
  MalumotlarBazasi._ichki(this.ulanishUrl);

  // Singleton factory
  factory MalumotlarBazasi([String url = 'postgres://localhost:5432']) {
    _nusxa ??= MalumotlarBazasi._ichki(url);
    return _nusxa!;
  }
}

void main() {
  var db1 = MalumotlarBazasi();
  var db2 = MalumotlarBazasi('boshqa_url');

  print('Bir xil obyektmi: ${identical(db1, db2)}');
  print('Ulanish URL: ${db2.ulanishUrl}');
}
```

## Tushuntirish va Mantiq:
Factory chaqirilganda har doim avval yaratilgan `_nusxa` qaytariladi, natijada faqat bitta instansiya bo'ladi.

## Ishlash natijasi:
```text
Bir xil obyektmi: true
Ulanish URL: postgres://localhost:5432
```

# 410-Topshiriq: Factory konstruktor orqali keshlovchi mexanizm (Cache Factory)

## Topshiriq sharti:
Bir xil parametr bilan qayta chaqirilganda yangi obyekt yaratmay, keshdagi obyektni qaytaruvchi klass tuzing.

## Yechim (Dart kodi):
```dart
class Rang {
  final String nom;
  static final Map<String, Rang> _kesh = {};

  Rang._ichki(this.nom);

  factory Rang(String nom) {
    return _kesh.putIfAbsent(nom.toLowerCase(), () => Rang._ichki(nom.toLowerCase()));
  }
}

void main() {
  var r1 = Rang('Qizil');
  var r2 = Rang('QIZIL');
  var r3 = Rang('Ko\'k');

  print('r1 va r2 bitta nusxami: ${identical(r1, r2)}');
  print('r1 va r3 bitta nusxami: ${identical(r1, r3)}');
}
```

## Tushuntirish va Mantiq:
`putIfAbsent` yordamida kalit keshda mavjud bo'lsa o'sha obyekt olinadi, aks holda yangisi yaratilib keshga joylanadi.

## Ishlash natijasi:
```text
r1 va r2 bitta nusxami: true
r1 va r3 bitta nusxami: false
```

# 411-Topshiriq: Factory konstruktor orqali JSON dan obyekt yaratish

## Topshiriq sharti:
`Map<String, dynamic>` ma'lumotlarini qabul qilib to'g'ri obyektga aylantiruvchi `User.fromJson` factory konstruktorini tuzing.

## Yechim (Dart kodi):
```dart
class Foydalanuvchi {
  final int id;
  final String ism;
  final String email;

  Foydalanuvchi({required this.id, required this.ism, required this.email});

  factory Foydalanuvchi.fromJson(Map<String, dynamic> json) {
    return Foydalanuvchi(
      id: json['id'] as int,
      ism: json['ism'] as String,
      email: json['email'] as String,
    );
  }

  @override
  String toString() => 'Foydalanuvchi(id: $id, ism: $ism, email: $email)';
}

void main() {
  Map<String, dynamic> serverData = {
    'id': 101,
    'ism': 'Jamshid',
    'email': 'jamshid@example.com'
  };

  var user = Foydalanuvchi.fromJson(serverData);
  print(user);
}
```

## Tushuntirish va Mantiq:
Dart/Flutterda API dan kelgan JSON lug'atlarni obyektga aylantirish uchun `factory Model.fromJson()` standarti ishlatiladi.

## Ishlash natijasi:
```text
Foydalanuvchi(id: 101, ism: Jamshid, email: jamshid@example.com)
```

# 412-Topshiriq: Factory orqali polimorfik subklasslar qaytarish

## Topshiriq sharti:
Turi bo'yicha mos subklass nusxasini qaytaruvchi factory konstruktor namunasini tuzing.

## Yechim (Dart kodi):
```dart
abstract class XabarYuboruvchi {
  void yuborish(String matn);

  factory XabarYuboruvchi(String kanal) {
    if (kanal == 'sms') return SmsYuboruvchi();
    if (kanal == 'email') return EmailYuboruvchi();
    throw ArgumentError('Noma\'lum kanal: $kanal');
  }
}

class SmsYuboruvchi implements XabarYuboruvchi {
  @override
  void yuborish(String matn) => print('SMS yuborildi: $matn');
}

class EmailYuboruvchi implements XabarYuboruvchi {
  @override
  void yuborish(String matn) => print('Email yuborildi: $matn');
}

void main() {
  var bot1 = XabarYuboruvchi('sms');
  var bot2 = XabarYuboruvchi('email');

  bot1.yuborish('Kodingiz: 1234');
  bot2.yuborish('Hisobot tayyor');
}
```

## Tushuntirish va Mantiq:
Factory konstruktor abstract sinfning o'zidan chaqirilgan holda uning aniq voris sinflarini qaytarishi mumkin.

## Ishlash natijasi:
```text
SMS yuborildi: Kodingiz: 1234
Email yuborildi: Hisobot tayyor
```

# 413-Topshiriq: Factory konstruktorda validatsiya va null qaytarish

## Topshiriq sharti:
Kiritilgan parametrlar noto'g'ri bo'lsa yoki shart bajarilmasa ishlov beruvchi factory konstruktor tuzing.

## Yechim (Dart kodi):
```dart
class EmailManzil {
  final String qiymat;

  EmailManzil._(this.qiymat);

  static EmailManzil? yaratish(String xom) {
    if (xom.contains('@') && xom.contains('.')) {
      return EmailManzil._(xom.trim().toLowerCase());
    }
    return null;
  }
}

void main() {
  var e1 = EmailManzil.yaratish('  ALI@GMAIL.COM ');
  var e2 = EmailManzil.yaratish('notogri-manzil');

  print('e1: ${e1?.qiymat}');
  print('e2: ${e2?.qiymat}');
}
```

## Tushuntirish va Mantiq:
Static factory yoki `yaratish` metodi orqali noto'g'ri qiymat kiritilganda null qaytarish (Smart Constructor) naqshi qo'llanadi.

## Ishlash natijasi:
```text
e1: ali@gmail.com
e2: null
```

# 414-Topshiriq: Operator overloading: + operatorini qayta aniqlash

## Topshiriq sharti:
Ikki o'lchovli Vektor (x, y) klassini yarating va `+` operatori yordamida ikkita vektorni qo'shish imkonini bering.

## Yechim (Dart kodi):
```dart
class Vektor2D {
  final double x;
  final double y;

  const Vektor2D(this.x, this.y);

  Vektor2D operator +(Vektor2D boshqa) {
    return Vektor2D(x + boshqa.x, y + boshqa.y);
  }

  @override
  String toString() => 'Vektor2D($x, $y)';
}

void main() {
  var v1 = Vektor2D(3.0, 4.0);
  var v2 = Vektor2D(1.5, 2.5);

  var v3 = v1 + v2;
  print('v1 + v2 = $v3');
}
```

## Tushuntirish va Mantiq:
Dartda `operator +` sintaksisi orqali har qanday maxsus klasslar uchun arifmetik operatorlarni qayta belgilash mumkin.

## Ishlash natijasi:
```text
v1 + v2 = Vektor2D(4.5, 6.5)
```

# 415-Topshiriq: Operator overloading: - va unar minus operatori

## Topshiriq sharti:
Vektor klassi uchun binar ayirish (`-`) va qarama-qarshi ishora beruvchi unar minus (`unary-`) operatorlarini yozing.

## Yechim (Dart kodi):
```dart
class Vektor {
  final double x;
  final double y;

  Vektor(this.x, this.y);

  // Binar ayirish (v1 - v2)
  Vektor operator -(Vektor boshqa) => Vektor(x - boshqa.x, y - boshqa.y);

  // Unar minus (-v1)
  Vektor operator -() => Vektor(-x, -y);

  @override
  String toString() => '($x, $y)';
}

void main() {
  var a = Vektor(10, 20);
  var b = Vektor(3, 7);

  print('a - b = ${a - b}');
  print('-a = ${-a}');
}
```

## Tushuntirish va Mantiq:
Parametrsiz `operator -()` metodi unar minusni (`-v`) qayta yuklaydi, parametrli esa ikkita obyektni ayirishni bildiradi.

## Ishlash natijasi:
```text
a - b = (7.0, 13.0)
-a = (-10.0, -20.0)
```

# 416-Topshiriq: Operator overloading: * (ko'paytirish)

## Topshiriq sharti:
Vektorni songa (skalyarga) ko'paytiruvchi `operator *` metodini amalga oshiring.

## Yechim (Dart kodi):
```dart
class Vektor {
  final double x;
  final double y;

  Vektor(this.x, this.y);

  Vektor operator *(num skalyar) => Vektor(x * skalyar, y * skalyar);

  @override
  String toString() => 'Vektor($x, $y)';
}

void main() {
  var v = Vektor(2.5, 4.0);
  var natija = v * 3;
  print('v * 3 = $natija');
}
```

## Tushuntirish va Mantiq:
`operator *(num skalyar)` yordamida obyektni o'ng tomonidagi skalyar songa qulay ko'paytirish mumkin.

## Ishlash natijasi:
```text
v * 3 = Vektor(7.5, 12.0)
```

# 417-Topshiriq: Indeks operatorlari: [] va []=

## Topshiriq sharti:
Lug'at yoki massiv kabi kvadrat qavs orqali element olish (`[]`) va yozish (`[]=`) operatorlarini yozing.

## Yechim (Dart kodi):
```dart
class Lugat {
  final Map<String, String> _sozlar = {};

  String? operator [](String kalit) => _sozlar[kalit];
  void operator []=(String kalit, String qiymat) => _sozlar[kalit] = qiymat;
}

void main() {
  var dict = Lugat();
  dict['apple'] = 'olma';
  dict['book'] = 'kitob';

  print('apple -> ${dict["apple"]}');
  print('book -> ${dict["book"]}');
  print('car -> ${dict["car"]}');
}
```

## Tushuntirish va Mantiq:
`operator []` va `operator []=` obyektlarga to'g'ridan-to'g'ri massiv yoki Map kabi indekslash imkoniyatini taqdim etadi.

## Ishlash natijasi:
```text
apple -> olma
book -> kitob
car -> null
```

# 418-Topshiriq: Tenglik operatori: operator == va hashCode

## Topshiriq sharti:
Maydonlari bir xil bo'lgan ikkita obyektni teng deb hisoblash uchun `operator ==` va `hashCode` ni qayta yozing.

## Yechim (Dart kodi):
```dart
class Nuqta {
  final int x;
  final int y;

  Nuqta(this.x, this.y);

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is Nuqta && other.x == x && other.y == y;
  }

  @override
  int get hashCode => Object.hash(x, y);
}

void main() {
  var p1 = Nuqta(3, 4);
  var p2 = Nuqta(3, 4);
  var p3 = Nuqta(5, 6);

  print('p1 == p2: ${p1 == p2}');
  print('p1 == p3: ${p1 == p3}');

  Set<Nuqta> toplanm = {p1, p2};
  print('Set dagi elementlar soni: ${toplanm.length}');
}
```

## Tushuntirish va Mantiq:
Agar `operator ==` qayta yozilsa, `hashCode` ham albatta qayta yozilishi shart, aks holda Set va Map kalitlarida xatolik yuz beradi.

## Ishlash natijasi:
```text
p1 == p2: true
p1 == p3: false
Set dagi elementlar soni: 1
```

# 419-Topshiriq: Taqqoslash operatorlari: < va > ni qayta yuklash

## Topshiriq sharti:
Ikkita mahsulotni narxi bo'yicha `<` va `>` operatorlari yordamida to'g'ridan-to'g'ri taqqoslang.

## Yechim (Dart kodi):
```dart
class Mahsulot {
  final String nom;
  final double narx;

  Mahsulot(this.nom, this.narx);

  bool operator <(Mahsulot boshqa) => narx < boshqa.narx;
  bool operator >(Mahsulot boshqa) => narx > boshqa.narx;
}

void main() {
  var m1 = Mahsulot('Non', 4000);
  var m2 = Mahsulot('Sut', 11000);

  print('Non Sutdan arzonga tushadimi: ${m1 < m2}');
  print('Non Sutdan qimmatmi: ${m1 > m2}');
}
```

## Tushuntirish va Mantiq:
Dartda `<` va `>` operatorlarini qayta belgilash orqali obyektlar orasidagi mantiqiy taqqoslashlarni soddalashtirish mumkin.

## Ishlash natijasi:
```text
Non Sutdan arzonga tushadimi: true
Non Sutdan qimmatmi: false
```

# 420-Topshiriq: Valyuta klassida + va - operatorlari

## Topshiriq sharti:
Bir xil valyutadagi pullarni xavfsiz qo'shish va ayirish imkonini beruvchi Pul klassini tuzing.

## Yechim (Dart kodi):
```dart
class Pul {
  final double miqdor;
  final String valyuta;

  Pul(this.miqdor, this.valyuta);

  Pul operator +(Pul boshqa) {
    if (valyuta != boshqa.valyuta) {
      throw ArgumentError('Valyutalar mos kelmadi: $valyuta vs ${boshqa.valyuta}');
    }
    return Pul(miqdor + boshqa.miqdor, valyuta);
  }

  @override
  String toString() => '${miqdor.toStringAsFixed(0)} $valyuta';
}

void main() {
  var p1 = Pul(50000, 'UZS');
  var p2 = Pul(30000, 'UZS');

  print('Jami: ${p1 + p2}');
}
```

## Tushuntirish va Mantiq:
Valyutalar har xil bo'lganda qo'shish xatolik beradi, bu moliyaviy xatoliklarning oldini oladi.

## Ishlash natijasi:
```text
Jami: 80000 UZS
```

# 421-Topshiriq: Maxsus matn konteyneri va * takrorlash operatori

## Topshiriq sharti:
Matnni ko'rsatilgan martagacha ko'paytirib (takrorlab) beruvchi maxsus Wrapper klassini tuzing.

## Yechim (Dart kodi):
```dart
class MatnBlok {
  final String matn;

  MatnBlok(this.matn);

  MatnBlok operator *(int marta) {
    return MatnBlok(matn * marta);
  }

  @override
  String toString() => matn;
}

void main() {
  var yulduz = MatnBlok('*');
  var devor = yulduz * 10;
  print('Chiziq: $devor');
}
```

## Tushuntirish va Mantiq:
`matn * marta` ichki String takrorlashidan foydalanib o'z sinfimizda `*` operatorini qulay amalga oshirdik.

## Ishlash natijasi:
```text
Chiziq: **********
```

# 422-Topshiriq: Vaqt oralig'i (TimeSpan) uchun operator overloading

## Topshiriq sharti:
Soat va minutlardan iborat vaqt oraliqlarini qo'shuvchi `+` operatorini yozing.

## Yechim (Dart kodi):
```dart
class VaqtOraligi {
  final int jamiMinutlar;

  VaqtOraligi(int soat, int minut) : jamiMinutlar = soat * 60 + minut;
  VaqtOraligi.minut(this.jamiMinutlar);

  VaqtOraligi operator +(VaqtOraligi boshqa) {
    return VaqtOraligi.minut(jamiMinutlar + boshqa.jamiMinutlar);
  }

  @override
  String toString() => '${jamiMinutlar ~/ 60} soat ${jamiMinutlar % 60} minut';
}

void main() {
  var dars1 = VaqtOraligi(1, 20); // 1s 20m
  var dars2 = VaqtOraligi(0, 50); // 50m

  var jami = dars1 + dars2;
  print('Umumiy davomiylik: $jami');
}
```

## Tushuntirish va Mantiq:
Vaqt oraliqlari ichki bitta o'lchov birligida (minutlar) saqlanadi va operatorlar orqali qulay yig'iladi.

## Ishlash natijasi:
```text
Umumiy davomiylik: 2 soat 10 minut
```

# 423-Topshiriq: Kasr sonlar (Fraction) klassi va arifmetik amallar

## Topshiriq sharti:
Surat va maxrajdan iborat kasr sonlar klassini tuzing va `+` hamda `*` operatorlarini amalga oshiring.

## Yechim (Dart kodi):
```dart
class Kasr {
  final int surat;
  final int maxraj;

  Kasr(this.surat, this.maxraj) {
    if (maxraj == 0) throw ArgumentError('Maxraj nol bo\'lishi mumkin emas');
  }

  Kasr operator +(Kasr b) {
    return Kasr(surat * b.maxraj + b.surat * maxraj, maxraj * b.maxraj);
  }

  Kasr operator *(Kasr b) {
    return Kasr(surat * b.surat, maxraj * b.maxraj);
  }

  @override
  String toString() => '$surat/$maxraj';
}

void main() {
  var k1 = Kasr(1, 2);
  var k2 = Kasr(1, 3);

  print('$k1 + $k2 = ${k1 + k2}');
  print('$k1 * $k2 = ${k1 * k2}');
}
```

## Tushuntirish va Mantiq:
Kasrlar ustida amallar: $a/b + c/d = (ad+bc)/bd$ va $a/b \cdot c/d = ac/bd$ formulalari asosida ishlaydi.

## Ishlash natijasi:
```text
1/2 + 1/3 = 5/6
1/2 * 1/3 = 1/6
```

# 424-Topshiriq: Kompleks sonlar klassi va operator overloading

## Topshiriq sharti:
Haqiqiy va mavhum qismga ega Kompleks sonlar klassini yarating va `+` hamda `*` operatorlarini yozing.

## Yechim (Dart kodi):
```dart
class KompleksSon {
  final double re;
  final double im;

  KompleksSon(this.re, this.im);

  KompleksSon operator +(KompleksSon b) => KompleksSon(re + b.re, im + b.im);

  KompleksSon operator *(KompleksSon b) {
    // (a + bi)(c + di) = (ac - bd) + (ad + bc)i
    return KompleksSon(re * b.re - im * b.im, re * b.im + im * b.re);
  }

  @override
  String toString() => '$re + ${im}i';
}

void main() {
  var z1 = KompleksSon(2, 3);
  var z2 = KompleksSon(4, -1);

  print('z1 + z2 = ${z1 + z2}');
  print('z1 * z2 = ${z1 * z2}');
}
```

## Tushuntirish va Mantiq:
Kompleks sonlar algebraik qoidalari operator overloading yordamida tabiiy matematik ko'rinishda ifodalanadi.

## Ishlash natijasi:
```text
z1 + z2 = 6.0 + 2.0i
z1 * z2 = 11.0 + 10.0i
```

# 425-Topshiriq: Factory konstruktor yordamida Obyektlar Hovuzi (Object Pool)

## Topshiriq sharti:
Qayta ishlatiladigan resurslarni boshqaruvchi Obyektlar hovuzi (Object Pool) naqshini tuzing.

## Yechim (Dart kodi):
```dart
class Resurs {
  final int id;
  bool band = false;

  Resurs._(this.id);

  static final List<Resurs> _hovuz = List.generate(2, (i) => Resurs._(i + 1));

  static Resurs? olish() {
    for (var r in _hovuz) {
      if (!r.band) {
        r.band = true;
        return r;
      }
    }
    return null;
  }

  void ozodQilish() => band = false;
}

void main() {
  var r1 = Resurs.olish();
  var r2 = Resurs.olish();
  var r3 = Resurs.olish();

  print('R1 olindi: ${r1?.id}');
  print('R2 olindi: ${r2?.id}');
  print('R3 olindi: ${r3?.id}'); // Resurs yetarli emas

  r1?.ozodQilish();
  var r4 = Resurs.olish();
  print('R1 ozod bo\'lgach R4 olindi: ${r4?.id}');
}
```

## Tushuntirish va Mantiq:
Obyektlar hovuzi qimmat resurslarni qayta-qayta yaratmasdan, mavjudlarini navbat bilan ishlatish imkonini beradi.

## Ishlash natijasi:
```text
R1 olindi: 1
R2 olindi: 2
R3 olindi: null
R1 ozod bo'lgach R4 olindi: 1
```

# 426-Topshiriq: Matritsalar qo'shish uchun + operatori

## Topshiriq sharti:
Ikki o'lchovli matritsalar uchun `+` operatorini qayta yuklab, mos kataklarni qo'shuvchi dastur tuzing.

## Yechim (Dart kodi):
```dart
class Matritsa2D {
  final List<List<int>> data;

  Matritsa2D(this.data);

  Matritsa2D operator +(Matritsa2D boshqa) {
    int rows = data.length;
    int cols = data[0].length;
    List<List<int>> yangi = List.generate(
      rows,
      (r) => List.generate(cols, (c) => data[r][c] + boshqa.data[r][c]),
    );
    return Matritsa2D(yangi);
  }

  void chop() {
    for (var row in data) {
      print(row.join(' '));
    }
  }
}

void main() {
  var m1 = Matritsa2D([
    [1, 2],
    [3, 4]
  ]);
  var m2 = Matritsa2D([
    [5, 6],
    [7, 8]
  ]);

  var m3 = m1 + m2;
  print('m1 + m2:');
  m3.chop();
}
```

## Tushuntirish va Mantiq:
Ikki matritsa elementlari birma-bir qo'shilib, yangi `Matritsa2D` nusxasi shakllantiriladi.

## Ishlash natijasi:
```text
m1 + m2:
6 8
10 12
```

# 427-Topshiriq: Bitwise operatorlarni qayta yuklash (& va |)

## Topshiriq sharti:
Ruxsatlar to'plami (Permission bitmask) uchun `&` va `|` operatorlarini qayta belgilang.

## Yechim (Dart kodi):
```dart
class Ruxsat {
  final int maska;

  const Ruxsat(this.maska);

  static const oqish = Ruxsat(1); // 001
  static const yozish = Ruxsat(2); // 010
  static const ijro = Ruxsat(4);  // 100

  Ruxsat operator |(Ruxsat boshqa) => Ruxsat(maska | boshqa.maska);
  bool operator &(Ruxsat boshqa) => (maska & boshqa.maska) != 0;
}

void main() {
  var meningRuxsatim = Ruxsat.oqish | Ruxsat.yozish;

  print('O\'qish mumkinmi: ${meningRuxsatim & Ruxsat.oqish}');
  print('Yozish mumkinmi: ${meningRuxsatim & Ruxsat.yozish}');
  print('Ijro mumkinmi: ${meningRuxsatim & Ruxsat.ijro}');
}
```

## Tushuntirish va Mantiq:
`|` operatori ruxsatlarni birlashtiradi, `&` operatori esa kerakli ruxsat mavjudligini mantiqiy tekshiradi.

## Ishlash natijasi:
```text
O'qish mumkinmi: true
Yozish mumkinmi: true
Ijro mumkinmi: false
```

# 428-Topshiriq: Taqqoslash va Comparable interfeysi

## Topshiriq sharti:
Talabalar reytingini `Comparable<Talaba>` interfeysi va `<` operatori orqali saralashni tashkil eting.

## Yechim (Dart kodi):
```dart
class Talaba implements Comparable<Talaba> {
  final String ism;
  final double ball;

  Talaba(this.ism, this.ball);

  @override
  int compareTo(Talaba other) => ball.compareTo(other.ball);

  bool operator <(Talaba other) => ball < other.ball;

  @override
  String toString() => '$ism ($ball)';
}

void main() {
  var t1 = Talaba('Ali', 78.5);
  var t2 = Talaba('Vali', 89.0);

  print('Ali < Vali: ${t1 < t2}');

  var guruh = [t2, t1];
  guruh.sort();
  print('Saralangan: $guruh');
}
```

## Tushuntirish va Mantiq:
`Comparable` interfeysini joriy qilish ro'yxatning `sort()` metodida standart taqqoslash qoidasini ta'minlaydi.

## Ishlash natijasi:
```text
Ali < Vali: true
Saralangan: [Ali (78.5), Vali (89.0)]
```

# 429-Topshiriq: Factory orqali Immutable Config Singleton

## Topshiriq sharti:
Tizim konfiguratsiyasini faqat bir marta initsializatsiya qiluvchi factory konstruktor tuzing.

## Yechim (Dart kodi):
```dart
class AppConfig {
  final String appNomi;
  final String versiya;

  static AppConfig? _instance;

  AppConfig._(this.appNomi, this.versiya);

  factory AppConfig({String? appNomi, String? versiya}) {
    _instance ??= AppConfig._(appNomi ?? 'UzbekAI', versiya ?? '1.0.0');
    return _instance!;
  }
}

void main() {
  var c1 = AppConfig(appNomi: 'SuperAI', versiya: '2.5');
  var c2 = AppConfig(appNomi: 'Yangisi');

  print('c1 app: ${c1.appNomi}, versiya: ${c1.versiya}');
  print('c2 app: ${c2.appNomi}, versiya: ${c2.versiya}');
  print('Bir xil obyekt: ${identical(c1, c2)}');
}
```

## Tushuntirish va Mantiq:
Birinchi chaqiruvda qiymatlar o'rnatiladi, keyingi barcha murojaatlarda mavjud parametrlar o'zgarmay qaytadi.

## Ishlash natijasi:
```text
c1 app: SuperAI, versiya: 2.5
c2 app: SuperAI, versiya: 2.5
Bir xil obyekt: true
```

# 430-Topshiriq: Dinamik chegirma hisoblovchi getter

## Topshiriq sharti:
Mahsulot narxi va chegirma foiziga qarab yakuniy to'lov miqdorini dinamik hisoblovchi getter yozing.

## Yechim (Dart kodi):
```dart
class Xarid {
  double aslNarx;
  int chegirmaFoiz; // Masalan 20%

  Xarid(this.aslNarx, [this.chegirmaFoiz = 0]);

  double get yakuniyNarx => aslNarx * (1 - chegirmaFoiz / 100);
}

void main() {
  var x = Xarid(200000, 15);
  print('Asl narx: ${x.aslNarx} so\'m');
  print('Chegirma bilan: ${x.yakuniyNarx.toStringAsFixed(0)} so\'m');

  x.chegirmaFoiz = 25;
  print('25% chegirma bilan: ${x.yakuniyNarx.toStringAsFixed(0)} so\'m');
}
```

## Tushuntirish va Mantiq:
Getter yordamida o'zgaruvchan chegirma stavkasiga ko'ra har gal to'g'ri yakuniy narx hisoblanadi.

## Ishlash natijasi:
```text
Asl narx: 200000.0 so'm
Chegirma bilan: 170000 so'm
25% chegirma bilan: 150000 so'm
```

# 431-Topshiriq: Setter yordamida telefon raqamini formatlash

## Topshiriq sharti:
Har xil formatda kiritilgan raqamni faqat raqamlarga tozalab, +998 prefiksi bilan saqlovchi setter yozing.

## Yechim (Dart kodi):
```dart
class TelefonRaqam {
  String _raqam = '';

  String get raqam => _raqam;

  set raqam(String xom) {
    // Faqat raqamlarni ajratib olamiz
    String toza = xom.replaceAll(RegExp(r'[^0-9]'), '');
    if (toza.startsWith('998') && toza.length == 12) {
      _raqam = '+$toza';
    } else if (toza.length == 9) {
      _raqam = '+998$toza';
    } else {
      throw FormatException('Telefon raqami formati noto\'g\'ri');
    }
  }
}

void main() {
  var tel = TelefonRaqam();
  tel.raqam = '(90) 123-45-67';
  print('Saqlangan: ${tel.raqam}');

  tel.raqam = '+998 94 987 65 43';
  print('Saqlangan: ${tel.raqam}');
}
```

## Tushuntirish va Mantiq:
Setter kiritilgan qiymatni tozalaydi, standart holatga keltiradi va shundan keyingina maydonga yuklaydi.

## Ishlash natijasi:
```text
Saqlangan: +998901234567
Saqlangan: +998949876543
```

# 432-Topshiriq: Factory orqali Environment konfiguratsiyasi

## Topshiriq sharti:
Muhit turi ('dev', 'prod') bo'yicha mos konfiguratsiya sozlamalarini qaytaruvchi factory konstruktor tuzing.

## Yechim (Dart kodi):
```dart
class MuhitSozlamalari {
  final String apiEndpoint;
  final bool debugMode;

  MuhitSozlamalari._(this.apiEndpoint, this.debugMode);

  factory MuhitSozlamalari(String muhit) {
    if (muhit.toLowerCase() == 'prod') {
      return MuhitSozlamalari._('https://api.uzbekai.uz/v1', false);
    } else {
      return MuhitSozlamalari._('http://localhost:8080/v1', true);
    }
  }
}

void main() {
  var dev = MuhitSozlamalari('dev');
  var prod = MuhitSozlamalari('prod');

  print('Dev: ${dev.apiEndpoint}, debug=${dev.debugMode}');
  print('Prod: ${prod.apiEndpoint}, debug=${prod.debugMode}');
}
```

## Tushuntirish va Mantiq:
Factory konstruktor ilova muhitiga qarab avtomatik mos konfiguratsiya obyektini shakllantirib beradi.

## Ishlash natijasi:
```text
Dev: http://localhost:8080/v1, debug=true
Prod: https://api.uzbekai.uz/v1, debug=false
```

# 433-Topshiriq: Operator % (qoldiqli bo'lish) ni maxsus klassda qo'llash

## Topshiriq sharti:
Modul arifmetikasi (Z_n halqasi) elementlari uchun `%` va `+` operatorlarini qayta yuklang.

## Yechim (Dart kodi):
```dart
class ModuloArifmetika {
  final int qiymat;
  final int modul;

  ModuloArifmetika(int q, this.modul) : qiymat = (q % modul + modul) % modul;

  ModuloArifmetika operator +(ModuloArifmetika b) {
    assert(modul == b.modul, 'Modullar teng bo\'lishi kerak');
    return ModuloArifmetika((qiymat + b.qiymat) % modul, modul);
  }

  @override
  String toString() => '$qiymat (mod $modul)';
}

void main() {
  var a = ModuloArifmetika(7, 5); // 2
  var b = ModuloArifmetika(4, 5); // 4

  print('a = $a');
  print('b = $b');
  print('a + b = ${a + b}'); // 2 + 4 = 6 % 5 = 1
}
```

## Tushuntirish va Mantiq:
Kriptografiya va raqamli xavfsizlikda keng qo'llaniladigan modul arifmetikasi operator overloading orqali qulay ifodalandi.

## Ishlash natijasi:
```text
a = 2 (mod 5)
b = 4 (mod 5)
a + b = 1 (mod 5)
```

# 434-Topshiriq: Operator / va ~/ (butunli bo'lish) ni qayta yuklash

## Topshiriq sharti:
Maxsus o'lchov birligi (Dyuym/Santimetr) uchun bo'lish operatorlarini amalga oshiring.

## Yechim (Dart kodi):
```dart
class Masofa {
  final double metr;

  Masofa(this.metr);

  double operator /(Masofa boshqa) => metr / boshqa.metr;
  int operator ~/(Masofa boshqa) => metr ~/ boshqa.metr;
}

void main() {
  var devor = Masofa(10.0);
  var plita = Masofa(1.5);

  print('Haqiqiy nisbat (/): ${(devor / plita).toStringAsFixed(2)}');
  print('To\'liq sig\'adigan plitalar (~/): ${devor ~/ plita}');
}
```

## Tushuntirish va Mantiq:
`/` haqiqiy bo'linmani (`double`), `~/` esa butun sonli bo'linmani (`int`) qaytaruvchi mustaqil operatorlardir.

## Ishlash natijasi:
```text
Haqiqiy nisbat (/): 6.67
To'liq sig'adigan plitalar (~/): 6
```

# 435-Topshiriq: Polinom (Ko'phad) klassi va + operatori

## Topshiriq sharti:
Koeffitsiyentlar ro'yxatiga ega Polinom klassini tuzing va ikkita polinomni qo'shuvchi `+` operatorini yozing.

## Yechim (Dart kodi):
```dart
import 'dart:math';

class Polinom {
  final List<num> koeffitsiyentlar;

  Polinom(this.koeffitsiyentlar);

  Polinom operator +(Polinom boshqa) {
    int maxLen = max(koeffitsiyentlar.length, boshqa.koeffitsiyentlar.length);
    List<num> natija = [];
    for (int i = 0; i < maxLen; i++) {
      num a = i < koeffitsiyentlar.length ? koeffitsiyentlar[i] : 0;
      num b = i < boshqa.koeffitsiyentlar.length ? boshqa.koeffitsiyentlar[i] : 0;
      natija.add(a + b);
    }
    return Polinom(natija);
  }

  @override
  String toString() => koeffitsiyentlar.join(' + ');
}

void main() {
  var p1 = Polinom([1, 2, 3]); // 1 + 2x + 3x^2
  var p2 = Polinom([4, 5]);    // 4 + 5x

  print('p1 + p2 = ${p1 + p2}');
}
```

## Tushuntirish va Mantiq:
Har xil darajali polinomlarning mos koeffitsiyentlari qo'shilib yangi natijaviy ko'phad hosil qilinadi.

## Ishlash natijasi:
```text
p1 + p2 = 5 + 7 + 3
```

# 436-Topshiriq: Ko'p qatlamli obyektlar uchun kaskadli getterlar

## Topshiriq sharti:
Mijoz, uning manzili va shahri haqidagi ma'lumotni kaskadli getter orqali to'g'ridan-to'g'ri taqdim etuvchi klass yozing.

## Yechim (Dart kodi):
```dart
class Manzil {
  final String shahar;
  final String kocha;
  Manzil(this.shahar, this.kocha);
}

class Mijoz {
  final String ism;
  final Manzil manzil;

  Mijoz(this.ism, this.manzil);

  String get shaharNomi => manzil.shahar;
  String get toliqManzil => '${manzil.shahar}, ${manzil.kocha}';
}

void main() {
  var m = Mijoz('Shavkat', Manzil('Buxoro', 'Navoiy shoh ko\'chasi'));
  print('Mijoz shahri: ${m.shaharNomi}');
  print('Yetkazish manzili: ${m.toliqManzil}');
}
```

## Tushuntirish va Mantiq:
Getterlar ichki chuqur qatlamdagi obyekt ma'lumotlarini qulay tashqi interfeys sifatida ko'rsatish (Law of Demeter) imkonini beradi.

## Ishlash natijasi:
```text
Mijoz shahri: Buxoro
Yetkazish manzili: Buxoro, Navoiy shoh ko'chasi
```

# 437-Topshiriq: Factory orqali CSV qatorini obyektga aylantirish

## Topshiriq sharti:
Vergul bilan ajratilgan CSV matnidan obyekt tuzuvchi `factory CSVRow.fromCsv(String line)` konstruktorini yozing.

## Yechim (Dart kodi):
```dart
class MahsulotQatori {
  final int id;
  final String nom;
  final double narx;

  MahsulotQatori(this.id, this.nom, this.narx);

  factory MahsulotQatori.fromCsv(String csvSatr) {
    var qismlar = csvSatr.split(',');
    return MahsulotQatori(
      int.parse(qismlar[0].trim()),
      qismlar[1].trim(),
      double.parse(qismlar[2].trim()),
    );
  }

  @override
  String toString() => '#$id $nom - $narx so\'m';
}

void main() {
  var qator = '101, Smartfon Samsung, 3200000.0';
  var mahsulot = MahsulotQatori.fromCsv(qator);
  print(mahsulot);
}
```

## Tushuntirish va Mantiq:
CSV yoki matnli qatorlarni tahlil qilib obyektga aylantirish uchun factory konstruktor eng qulay vositadir.

## Ishlash natijasi:
```text
#101 Smartfon Samsung - 3200000.0 so'm
```

# 438-Topshiriq: Factory orqali URL manzilini tahlil qilish

## Topshiriq sharti:
Protokol, domen va yo'lni matndan ajratib oluvchi `factory UrlManzili.parse(String url)` konstruktorini yozing.

## Yechim (Dart kodi):
```dart
class UrlManzili {
  final String protokol;
  final String domen;
  final String yoli;

  UrlManzili._(this.protokol, this.domen, this.yoli);

  factory UrlManzili.parse(String xomUrl) {
    var uri = Uri.parse(xomUrl);
    return UrlManzili._(uri.scheme, uri.host, uri.path);
  }
}

void main() {
  var manzil = UrlManzili.parse('https://uzbekai.uz/api/v1/chat');
  print('Protokol: ${manzil.protokol}');
  print('Domen:    ${manzil.domen}');
  print('Yo\'l:     ${manzil.yoli}');
}
```

## Tushuntirish va Mantiq:
Ichki Dart Uri tahlilchisidan foydalanib o'z maxsus domen obyektimizni yaratuvchi qulay factory metod shakllantirildi.

## Ishlash natijasi:
```text
Protokol: https
Domen:    uzbekai.uz
Yo'l:     /api/v1/chat
```

# 439-Topshiriq: Setterda o'zgarishlar tarixi (Audit Log)

## Topshiriq sharti:
Har gal narx o'zgarganda eski va yangi qiymatni tarix ro'yxatiga qayd etib boruvchi setter tuzing.

## Yechim (Dart kodi):
```dart
class NarxMonitoring {
  double _narx;
  final List<String> tarix = [];

  NarxMonitoring(this._narx) {
    tarix.add('Boshlang\'ich narx: $_narx');
  }

  double get narx => _narx;

  set narx(double yangiNarx) {
    tarix.add('O\'zgarish: $_narx -> $yangiNarx');
    _narx = yangiNarx;
  }
}

void main() {
  var nm = NarxMonitoring(5000);
  nm.narx = 5500;
  nm.narx = 6000;

  print('Tarix jurnali:');
  for (var yozuv in nm.tarix) {
    print('- $yozuv');
  }
}
```

## Tushuntirish va Mantiq:
Setter orqali nafaqat o'zgaruvchini o'rnatish, balki auditi yoki tarixini yozib borish ham osonlashadi.

## Ishlash natijasi:
```text
Tarix jurnali:
- Boshlang'ich narx: 5000.0
- O'zgarish: 5000.0 -> 5500.0
- O'zgarish: 5500.0 -> 6000.0
```

# 440-Topshiriq: Valyutalarni solishtirish uchun operator overloading

## Topshiriq sharti:
Turli hisobdagi mablag'larni solishtiruvchi `>=` va `<=` operatorlarini tuzing.

## Yechim (Dart kodi):
```dart
class Balans {
  final double summa;

  Balans(this.summa);

  bool operator >=(Balans b) => summa >= b.summa;
  bool operator <=(Balans b) => summa <= b.summa;
}

void main() {
  var b1 = Balans(50000);
  var b2 = Balans(50000);
  var b3 = Balans(70000);

  print('b1 >= b2: ${b1 >= b2}');
  print('b1 <= b3: ${b1 <= b3}');
}
```

## Tushuntirish va Mantiq:
Obyektlar o'rtasida `>=` va `<=` operatorlari orqali tabiiy shartli taqqoslashlar amalga oshiriladi.

## Ishlash natijasi:
```text
b1 >= b2: true
b1 <= b3: true
```

# 441-Topshiriq: O'lchov birliklari va arifmetik operatorlar

## Topshiriq sharti:
Santimetr va Metrlarni qo'shuvchi, ayiruvchi va formatlovchi Uzunlik klassini tuzing.

## Yechim (Dart kodi):
```dart
class Uzunlik {
  final double metr;

  Uzunlik.metr(this.metr);
  Uzunlik.santimetr(double sm) : metr = sm / 100;

  Uzunlik operator +(Uzunlik b) => Uzunlik.metr(metr + b.metr);
  Uzunlik operator -(Uzunlik b) => Uzunlik.metr(metr - b.metr);

  @override
  String toString() => '${metr.toStringAsFixed(2)} m (${(metr * 100).toStringAsFixed(0)} sm)';
}

void main() {
  var u1 = Uzunlik.metr(2.5);
  var u2 = Uzunlik.santimetr(75);

  print('u1: $u1');
  print('u2: $u2');
  print('u1 + u2: ${u1 + u2}');
}
```

## Tushuntirish va Mantiq:
Har xil birlikdagi kattaliklar ichki yagona asosiy birlikda (metr) saqlanadi va operatorlar yordamida aniq qo'shiladi.

## Ishlash natijasi:
```text
u1: 2.50 m (250 sm)
u2: 0.75 m (75 sm)
u1 + u2: 3.25 m (325 sm)
```

# 442-Topshiriq: Ranglar aralashmasi: Rang + Rang operatori

## Topshiriq sharti:
RGB rang komponentlarini o'rtacha aralashtiruvchi `+` operatorini yozing.

## Yechim (Dart kodi):
```dart
class RgbRang {
  final int r, g, b;

  const RgbRang(this.r, this.g, this.b);

  RgbRang operator +(RgbRang boshqa) {
    return RgbRang(
      (r + boshqa.r) ~/ 2,
      (g + boshqa.g) ~/ 2,
      (b + boshqa.b) ~/ 2,
    );
  }

  @override
  String toString() => 'RGB($r, $g, $b)';
}

void main() {
  var qizil = RgbRang(255, 0, 0);
  var kok = RgbRang(0, 0, 255);

  var aralashma = qizil + kok;
  print('Qizil + Ko\'k = $aralashma');
}
```

## Tushuntirish va Mantiq:
Ikki rangning mos kanallari o'rtachasi olinib yangi aralash rang hosil qilinadi.

## Ishlash natijasi:
```text
Qizil + Ko'k = RGB(127, 0, 127)
```

# 443-Topshiriq: Operator << ni buferga ma'lumot yozish sifatida ishlatish

## Topshiriq sharti:
C++ oqimlaridagi kabi `bufer << xabar` sintaksisini qo'llovchi MatnBuferi klassini tuzing.

## Yechim (Dart kodi):
```dart
class MatnBuferi {
  final StringBuffer _sb = StringBuffer();

  MatnBuferi operator <<(Object qiymat) {
    _sb.write(qiymat);
    return this; // Zanjirband chaqiruv uchun
  }

  @override
  String toString() => _sb.toString();
}

void main() {
  var buf = MatnBuferi();
  buf << 'O\'zbekiston' << ' - ' << 2026 << ' yil!';

  print(buf);
}
```

## Tushuntirish va Mantiq:
Operator `<<` o'z obyektini (`this`) qaytarsa, uni bir nechta ketma-ket amallar zanjiri (method chaining) sifatida ishlatish mumkin.

## Ishlash natijasi:
```text
O'zbekiston - 2026 yil!
```

# 444-Topshiriq: Factory orqali Mock (Test) servislarni taqdim etish

## Topshiriq sharti:
Test rejimida soxta ma'lumot beruvchi, real rejimda serverga ulanuvchi factory konstruktor tuzing.

## Yechim (Dart kodi):
```dart
abstract class FoydalanuvchiXizmati {
  String foydalanuvchiniOlish(int id);

  factory FoydalanuvchiXizmati({bool testRejimi = false}) {
    if (testRejimi) return _MockFoydalanuvchiXizmati();
    return _RealFoydalanuvchiXizmati();
  }
}

class _RealFoydalanuvchiXizmati implements FoydalanuvchiXizmati {
  @override
  String foydalanuvchiniOlish(int id) => 'Haqiqiy serverdan: User #$id';
}

class _MockFoydalanuvchiXizmati implements FoydalanuvchiXizmati {
  @override
  String foydalanuvchiniOlish(int id) => 'Test (Mock) foydalanuvchi: Temur';
}

void main() {
  var xizmat1 = FoydalanuvchiXizmati(testRejimi: true);
  var xizmat2 = FoydalanuvchiXizmati(testRejimi: false);

  print(xizmat1.foydalanuvchiniOlish(1));
  print(xizmat2.foydalanuvchiniOlish(1));
}
```

## Tushuntirish va Mantiq:
Dastur kodini o'zgartirmasdan bitta factory orqali test va ishlab chiqarish versiyalarini almashtirish mumkin.

## Ishlash natijasi:
```text
Test (Mock) foydalanuvchi: Temur
Haqiqiy serverdan: User #1
```

# 445-Topshiriq: Chegaralangan massiv va operator [] xavfsizligi

## Topshiriq sharti:
Indeks chegaradan chiqib ketganda xato bermay, standart default qiymat qaytaruvchi XavfsizMassiv klassini tuzing.

## Yechim (Dart kodi):
```dart
class XavfsizMassiv<T> {
  final List<T> _royxat;
  final T def;

  XavfsizMassiv(this._royxat, {required this.def});

  T operator [](int index) {
    if (index < 0 || index >= _royxat.length) {
      return def;
    }
    return _royxat[index];
  }
}

void main() {
  var massiv = XavfsizMassiv<String>(['A', 'B', 'C'], def: 'Yo\'q');

  print('Index 1: ${massiv[1]}');
  print('Index 5: ${massiv[5]}');
  print('Index -1: ${massiv[-1]}');
}
```

## Tushuntirish va Mantiq:
Maxsus `operator []` yordamida massiv chegarasidan tashqariga chiqish xatosi (IndexError) ning oldi olinadi.

## Ishlash natijasi:
```text
Index 1: B
Index 5: Yo'q
Index -1: Yo'q
```

# 446-Topshiriq: Hisob-kitoblar uchun keshlanuvchi getter (Memoization)

## Topshiriq sharti:
Qimmat hisoblashni faqat bir marta bajarib, natijani keshda saqlovchi getterni amalga oshiring.

## Yechim (Dart kodi):
```dart
class FibonacciHisoblagich {
  final int n;
  int? _keshlangan;

  FibonacciHisoblagich(this.n);

  int get qiymat {
    _keshlangan ??= _hisobla(n);
    return _keshlangan!;
  }

  int _hisobla(int k) {
    print('Qimmat hisoblash bajarilmoqda...');
    if (k <= 1) return k;
    int a = 0, b = 1;
    for (int i = 2; i <= k; i++) {
      int temp = a + b;
      a = b;
      b = temp;
    }
    return b;
  }
}

void main() {
  var f = FibonacciHisoblagich(10);
  print('Birinchi chaqiruv: ${f.qiymat}');
  print('Ikkinchi chaqiruv: ${f.qiymat}');
}
```

## Tushuntirish va Mantiq:
Memoization usuli bilan getter chaqirilganda og'ir hisob-kitob faqat birinchi marta ishlaydi, so'ngra tayyor natija beriladi.

## Ishlash natijasi:
```text
Qimmat hisoblash bajarilmoqda...
Birinchi chaqiruv: 55
Ikkinchi chaqiruv: 55
```

# 447-Topshiriq: Factory orqali O'zgarmas Simvollar Jadvali (Symbol Table)

## Topshiriq sharti:
Kompilyator va interpretatorlarda bir xil identifikatorlarni bitta manzilga bog'lovchi Symbol klassini tuzing.

## Yechim (Dart kodi):
```dart
class MaxsusSimvol {
  final String nom;
  static final Map<String, MaxsusSimvol> _jadval = {};

  MaxsusSimvol._(this.nom);

  factory MaxsusSimvol(String nom) {
    return _jadval.putIfAbsent(nom, () => MaxsusSimvol._(nom));
  }
}

void main() {
  var s1 = MaxsusSimvol('x');
  var s2 = MaxsusSimvol('y');
  var s3 = MaxsusSimvol('x');

  print('s1 == s3 (bir xil obyekti): ${identical(s1, s3)}');
  print('s1 == s2 (turli obyekt):   ${identical(s1, s2)}');
}
```

## Tushuntirish va Mantiq:
String interning yoki simvollar jadvali barcha bir xil matnlar uchun bitta obyektni taqdim etib xotirani tejaydi.

## Ishlash natijasi:
```text
s1 == s3 (bir xil obyekti): true
s1 == s2 (turli obyekt):   false
```

# 448-Topshiriq: SQL so'rov quruvchi (Query Builder) va getter/setterlar

## Topshiriq sharti:
SQL so'rovini qismlardan yig'uvchi va `sql` getteri orqali to'liq so'rov matnini beruvchi klass tuzing.

## Yechim (Dart kodi):
```dart
class SqlQuruvchi {
  String _jadval = '';
  final List<String> _ustunlar = [];
  String? _shart;

  set jadval(String nom) => _jadval = nom;

  void ustunQosh(String u) => _ustunlar.add(u);
  void shartBer(String s) => _shart = s;

  String get sql {
    String cols = _ustunlar.isEmpty ? '*' : _ustunlar.join(', ');
    String q = 'SELECT $cols FROM $_jadval';
    if (_shart != null) {
      q += ' WHERE $_shart';
    }
    return '$q;';
  }
}

void main() {
  var q = SqlQuruvchi();
  q.jadval = 'foydalanuvchilar';
  q.ustunQosh('id');
  q.ustunQosh('ism');
  q.shartBer('yosh >= 18');

  print('Hosil bo\'lgan SQL:');
  print(q.sql);
}
```

## Tushuntirish va Mantiq:
Obyekt xususiyatlari o'rnatilgach, getter orqali to'liq sintaktik to'g'ri SQL so'rov matni generatsiya qilinadi.

## Ishlash natijasi:
```text
Hosil bo'lgan SQL:
SELECT id, ism FROM foydalanuvchilar WHERE yosh >= 18;
```

# 449-Topshiriq: Kvant bit (Qubit) holati va operator overloading

## Topshiriq sharti:
Kvant holatlarini (amplitudalar) ifodalovchi va holatlarni qo'shuvchi Qubit klassini tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:math';

class Qubit {
  final double alpha; // |0> amplitudasi
  final double beta;  // |1> amplitudasi

  Qubit(this.alpha, this.beta);

  Qubit operator +(Qubit boshqa) {
    double a = alpha + boshqa.alpha;
    double b = beta + boshqa.beta;
    double norm = sqrt(a * a + b * b);
    return Qubit(a / norm, b / norm);
  }

  @override
  String toString() => '${alpha.toStringAsFixed(2)}|0> + ${beta.toStringAsFixed(2)}|1>';
}

void main() {
  var q1 = Qubit(1.0, 0.0); // |0> holat
  var q2 = Qubit(0.0, 1.0); // |1> holat

  var superpozitsiya = q1 + q2;
  print('Superpozitsiya: $superpozitsiya');
}
```

## Tushuntirish va Mantiq:
Superpozitsiya holati normallashtirilgan amplitudalar bilan ifodalanadi va operator `+` orqali kvant interferensiyasi modellashtiriladi.

## Ishlash natijasi:
```text
Superpozitsiya: 0.71|0> + 0.71|1>
```

# 450-Topshiriq: BitNet 1-bit Ternary Tensor va Matritsa ko'paytirish (*)

## Topshiriq sharti:
Ternar {-1, 0, +1} vaznlarga ega bo'lgan 1-bit AI qatlami va matritsa ko'paytirish `*` operatorini tuzing.

## Yechim (Dart kodi):
```dart
class BitTensor {
  final int qatorlar;
  final int ustunlar;
  final List<int> vaznlar; // -1, 0, +1 (BitNet b1.58)

  BitTensor(this.qatorlar, this.ustunlar, this.vaznlar);

  // Haqiqiy vektor bilan ko'paytirish (W * x)
  List<double> operator *(List<double> x) {
    if (x.length != ustunlar) throw ArgumentError('O\'lchamlar mos emas');
    List<double> chiqish = List.filled(qatorlar, 0.0);

    for (int i = 0; i < qatorlar; i++) {
      double sum = 0.0;
      for (int j = 0; j < ustunlar; j++) {
        int w = vaznlar[i * ustunlar + j];
        // Ternar arifmetika: FP ko'paytirish shart emas, faqat qo'shish va ayirish!
        if (w == 1) {
          sum += x[j];
        } else if (w == -1) {
          sum -= x[j];
        }
      }
      chiqish[i] = sum;
    }
    return chiqish;
  }
}

void main() {
  // 2x3 o'lchamli Ternar vazn matritsasi
  // [ +1,  0, -1 ]
  // [ -1, +1, +1 ]
  var w = BitTensor(2, 3, [1, 0, -1, -1, 1, 1]);
  List<double> x = [2.0, 5.0, 3.0];

  // Chiqish:
  // qator 0: (+1*2) + (0*5) + (-1*3) = 2 - 3 = -1
  // qator 1: (-1*2) + (+1*5) + (+1*3) = -2 + 5 + 3 = 6
  var y = w * x;
  print('BitNet 1-bit GEMV chiqishi: $y');
}
```

## Tushuntirish va Mantiq:
BitNet b1.58 arxitekturasi vaznlarni {-1, 0, +1} ga kvantlaydi. Matritsa ko'paytirish ko'paytiruvchilarsiz (faqat qo'shish va ayirish bilan) ishlaydi.

## Ishlash natijasi:
```text
BitNet 1-bit GEMV chiqishi: [-1.0, 6.0]
```

