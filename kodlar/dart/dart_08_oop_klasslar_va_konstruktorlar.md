# 8-Qism: OOP: Klasslar, Konstruktorlar va Maydonlar (351-400)

Ushbu qismda Dart tilida Ob'ektga Yo'naltirilgan Dasturlash (OOP): klasslar, generativ va nomlangan konstruktorlar, initializer list, `const` konstruktorlar, `copyWith` naqshi, xususiy maydonlar (`_`), statik a'zolar va ob'ektlar kompozitsiyasi amaliy kodlar orqali o'rganiladi.

# 351-Topshiriq: Klass e'lon qilish, maydonlar va metodlar
## Topshiriq sharti:
`Avtomobil` klassini yaratib, unga `model`, `yil` maydonlari hamda `malumot()` metodini qo'shing.

## Yechim (Dart kodi):
```dart
class Avtomobil {
  String model;
  int yil;

  Avtomobil(this.model, this.yil);

  void malumot() {
    print("Avtomobil modeli: $model, Ishlab chiqarilgan yili: $yil");
  }
}

void main() {
  var auto = Avtomobil("Chevrolet Gentra", 2024);
  auto.malumot();
}
```

## Tushuntirish va Mantiq:
Dart da klasslar ma'lumotlar (maydonlar) va xatti-harakatlarni (metodlar) bitta tur ichiga birlashtiradi.

## Ishlash natijasi:
```text
Avtomobil modeli: Chevrolet Gentra, Ishlab chiqarilgan yili: 2024
```

# 352-Topshiriq: Generativ konstruktor: this.field sintaksisi
## Topshiriq sharti:
Dart ning qisqa konstruktor parametrida `this.maydon` sintaksisi orqali o'zlashtirishni ko'rsating.

## Yechim (Dart kodi):
```dart
class Talaba {
  final String ism;
  final int kurs;

  // Qisqa generativ konstruktor
  Talaba(this.ism, this.kurs);
}

void main() {
  var t = Talaba("Anvar", 3);
  print("Talaba: ${t.ism}, Kursi: ${t.kurs}");
}
```

## Tushuntirish va Mantiq:
`this.ism` sintaksisi parametr qiymatini avtomatik ravishda maydonga yuklaydi, qo'shimcha `this.ism = ism;` deb yozish shart emas.

## Ishlash natijasi:
```text
Talaba: Anvar, Kursi: 3
```

# 353-Topshiriq: Nomlangan konstruktorlar (Named Constructors)
## Topshiriq sharti:
`Nuqta` klassi uchun standart `Nuqta(x, y)` va koordinata boshini hosil qiluvchi `Nuqta.origin()` nomlangan konstruktorini yozing.

## Yechim (Dart kodi):
```dart
class Nuqta {
  final double x, y;

  Nuqta(this.x, this.y);

  // Nomlangan konstruktor
  Nuqta.origin() : x = 0.0, y = 0.0;

  @override
  String toString() => "($x, $y)";
}

void main() {
  var p1 = Nuqta(5.0, 10.0);
  var p2 = Nuqta.origin();

  print("Nuqta 1: $p1");
  print("Nuqta 2 (boshlang'ich): $p2");
}
```

## Tushuntirish va Mantiq:
Nomlangan konstruktorlar bitta klass uchun turli maqsadlarda (masalan `fromJson`, `origin`, `zero`) ob'ekt yaratish imkonini beradi.

## Ishlash natijasi:
```text
Nuqta 1: (5.0, 10.0)
Nuqta 2 (boshlang'ich): (0.0, 0.0)
```

# 354-Topshiriq: Initializer List: Konstruktor tanasidan oldin hisoblash
## Topshiriq sharti:
`final` maydonlarni konstruktor tanasi bajarilishidan oldin hisoblab o'rnatuvchi Initializer List ni yozing.

## Yechim (Dart kodi):
```dart
class Tortburchak {
  final double eni, boyi;
  final double yuza;

  // Initializer list (ikki nuqtadan keyin)
  Tortburchak(this.eni, this.boyi) : yuza = eni * boyi;
}

void main() {
  var t = Tortburchak(6, 4);
  print("Eni: ${t.eni}, Bo'yi: ${t.boyi}, Yuzasi: ${t.yuza}");
}
```

## Tushuntirish va Mantiq:
Initializer list da barcha `final` maydonlar qiymat oladi va `assert` tekshiruvlari o'tkaziladi.

## Ishlash natijasi:
```text
Eni: 6.0, Bo'yi: 4.0, Yuzasi: 24.0
```

# 355-Topshiriq: const konstruktorlar va Immutable ob'ektlar
## Topshiriq sharti:
Kompilyatsiya vaqtida xotirada qat'iy bitta manzilga kanoniklashtiriladigan `const` konstruktorli klass yarating.

## Yechim (Dart kodi):
```dart
class Rang {
  final int red, green, blue;

  const Rang(this.red, this.green, this.blue);
}

void main() {
  const c1 = Rang(255, 0, 0);
  const c2 = Rang(255, 0, 0);

  print("c1 va c2 qiymatlari bir xil: ${c1.red == c2.red}");
  print("c1 va c2 xotiradagi aynan bitta ob'ekt (identical): ${identical(c1, c2)}");
}
```

## Tushuntirish va Mantiq:
`const` konstruktor barcha maydonlari `final` bo'lgan klasslarda ishlatiladi va Flutter vidjetlarini qayta chizishda ulkan xotira unumdorligini beradi.

## Ishlash natijasi:
```text
c1 va c2 qiymatlari bir xil: true
c1 va c2 xotiradagi aynan bitta ob'ekt (identical): true
```

# 356-Topshiriq: Qayta yo'naltiruvchi konstruktorlar (Redirecting constructors)
## Topshiriq sharti:
Bitta konstruktor chaqirilganda boshqa konstruktorga `this(...)` orqali yo'naltiruvchi kod yozing.

## Yechim (Dart kodi):
```dart
class Doira {
  final double radius;

  Doira(this.radius);

  // Qayta yo'naltiruvchi konstruktor
  Doira.birlik() : this(1.0);
}

void main() {
  var d1 = Doira(5.0);
  var d2 = Doira.birlik();

  print("d1 radiusi: ${d1.radius}");
  print("d2 radiusi: ${d2.radius}");
}
```

## Tushuntirish va Mantiq:
Redirecting constructor kod takrorlanishining oldini oladi va standart holatlarni markaziy konstruktorga yo'naltiradi.

## Ishlash natijasi:
```text
d1 radiusi: 5.0
d2 radiusi: 1.0
```

# 357-Topshiriq: Konstruktorda standart qiymatli parametrlar
## Topshiriq sharti:
Nomlangan parametrlar orqali sukut bo'yicha qiymatlarni konstruktorda belgilang.

## Yechim (Dart kodi):
```dart
class ServerConfig {
  final String host;
  final int port;
  final bool ssl;

  ServerConfig({this.host = "127.0.0.1", this.port = 8080, this.ssl = false});
}

void main() {
  var cfg1 = ServerConfig();
  var cfg2 = ServerConfig(host: "api.uzbek.ai", port: 443, ssl: true);

  print("Config 1: ${cfg1.host}:${cfg1.port} (SSL: ${cfg1.ssl})");
  print("Config 2: ${cfg2.host}:${cfg2.port} (SSL: ${cfg2.ssl})");
}
```

## Tushuntirish va Mantiq:
Standart qiymatlar orqali ob'ektni hech qanday argumentsiz ham xatosiz yaratish mumkin bo'ladi.

## Ishlash natijasi:
```text
Config 1: 127.0.0.1:8080 (SSL: false)
Config 2: api.uzbek.ai:443 (SSL: true)
```

# 358-Topshiriq: Statik maydonlar va Statik metodlar (static)
## Topshiriq sharti:
Klass nusxasisiz chaqiriladigan statik hisoblagich va yordamchi metodni yozing.

## Yechim (Dart kodi):
```dart
class Matematika {
  static const double pi = 3.1415926535;
  static int hisobChaqiruvlar = 0;

  static double kvadrat(double x) {
    hisobChaqiruvlar++;
    return x * x;
  }
}

void main() {
  print("PI doimiysi: ${Matematika.pi}");
  print("4 ning kvadrati: ${Matematika.kvadrat(4)}");
  print("Chaqiruvlar soni: ${Matematika.hisobChaqiruvlar}");
}
```

## Tushuntirish va Mantiq:
`static` a'zolar ob'ektga emas, balki butun klassning o'ziga tegishli bo'ladi va xotirada bitta nusxada saqlanadi.

## Ishlash natijasi:
```text
PI doimiysi: 3.1415926535
4 ning kvadrati: 16.0
Chaqiruvlar soni: 1
```

# 359-Topshiriq: toString() metodini qayta yuklash (Override)
## Topshiriq sharti:
Ob'ekt `print()` ga uzatilganda chiroyli matn chiqishi uchun `toString()` ni qayta yozing.

## Yechim (Dart kodi):
```dart
class Kitob {
  final String sarlavha;
  final String muallif;

  Kitob(this.sarlavha, this.muallif);

  @override
  String toString() => "'$sarlavha' (Muallif: $muallif)";
}

void main() {
  var k = Kitob("O'tkan kunlar", "Abdulla Qodiriy");
  print("Kitob ma'lumoti: $k");
}
```

## Tushuntirish va Mantiq:
`@override toString()` ob'ektni disk raskadrovka qilishda va ekranga tushunarli chiqarishda shart hisoblanadi.

## Ishlash natijasi:
```text
Kitob ma'lumoti: 'O'tkan kunlar' (Muallif: Abdulla Qodiriy)
```

# 360-Topshiriq: operator == va hashCode ni to'g'ri qayta yuklash
## Topshiriq sharti:
Ikkita turli ob'ektning maydonlari bir xil bo'lsa, ularni teng deb tan oluvchi mantiqni yozing.

## Yechim (Dart kodi):
```dart
class Mahsulot {
  final int id;
  final String nom;

  Mahsulot(this.id, this.nom);

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is Mahsulot && runtimeType == other.runtimeType && id == other.id && nom == other.nom;

  @override
  int get hashCode => Object.hash(id, nom);
}

void main() {
  var m1 = Mahsulot(1, "Klaviatura");
  var m2 = Mahsulot(1, "Klaviatura");

  print("m1 == m2: ${m1 == m2}");
  print("Set ichida bitta bo'ladimi: ${{m1, m2}.length == 1}");
}
```

## Tushuntirish va Mantiq:
Dart da `operator ==` qayta yuklanganda albatta `hashCode` ham mos ravishda qayta yuklanishi shart, aks holda Set va Map larda xatolar yuzaga keladi.

## Ishlash natijasi:
```text
m1 == m2: true
Set ichida bitta bo'ladimi: true
```

# 361-Topshiriq: copyWith() naqshi: O'zgarmas ob'ektdan yangi nusxa olish
## Topshiriq sharti:
Flutter BLoC va holat boshqaruvida keng qo'llaniladigan `copyWith` metodini amalga oshiring.

## Yechim (Dart kodi):
```dart
class Profil {
  final String ism;
  final int yosh;
  final String shahar;

  Profil({required this.ism, required this.yosh, required this.shahar});

  Profil copyWith({String? ism, int? yosh, String? shahar}) {
    return Profil(
      ism: ism ?? this.ism,
      yosh: yosh ?? this.yosh,
      shahar: shahar ?? this.shahar,
    );
  }

  @override
  String toString() => "Profil(ism: $ism, yosh: $yosh, shahar: $shahar)";
}

void main() {
  var p1 = Profil(ism: "Aziz", yosh: 22, shahar: "Toshkent");
  // Faqat yoshini o'zgartirib yangi ob'ekt olamiz:
  var p2 = p1.copyWith(yosh: 23);

  print("Eski profil: $p1");
  print("Yangi profil: $p2");
}
```

## Tushuntirish va Mantiq:
`copyWith` o'zgarmas (immutable) ob'ektning ayrim xususiyatlarini yangilab, qolganlarini o'z holicha saqlab qolgan yangi nusxasini qaytaradi.

## Ishlash natijasi:
```text
Eski profil: Profil(ism: Aziz, yosh: 22, shahar: Toshkent)
Yangi profil: Profil(ism: Aziz, yosh: 23, shahar: Toshkent)
```

# 362-Topshiriq: Inkapsulyatsiya: Xususiy (Private) maydonlar va metodlar
## Topshiriq sharti:
Dart da nom oldiga pastki chiziq `_` qo'yish orqali maydonni kutubxona darajasida yopiq (private) qilishni ko'rsating.

## Yechim (Dart kodi):
```dart
class BankHisob {
  String egasi;
  double _balans; // Xususiy maydon

  BankHisob(this.egasi, double boshlangichBalans) : _balans = boshlangichBalans;

  void depozit(double summa) {
    if (summa > 0) _balans += summa;
  }

  double getBalans() => _balans;
}

void main() {
  var hisob = BankHisob("Dilshod", 100000);
  hisob.depozit(50000);

  print("Egasi: ${hisob.egasi}");
  print("Balans: ${hisob.getBalans()} so'm");
}
```

## Tushuntirish va Mantiq:
Dart da private darajasi boshqa tillardagi kabi klass emas, balki fayl (library) darajasidadir. `_` bilan boshlangan a'zolar tashqi fayllardan ko'rinmaydi.

## Ishlash natijasi:
```text
Egasi: Dilshod
Balans: 150000.0 so'm
```

# 363-Topshiriq: Xususiy konstruktor va Singleton (Yagona nusxa) naqshi
## Topshiriq sharti:
Dastur bo'yicha faqat bitta umumiy ob'ektga ega bo'lgan Singleton xizmatini yozing.

## Yechim (Dart kodi):
```dart
class DatabaseConnection {
  static DatabaseConnection? _instance;

  // Xususiy nomlangan konstruktor
  DatabaseConnection._internal();

  // Yagona nusxani beruvchi factory konstruktor
  factory DatabaseConnection() {
    return _instance ??= DatabaseConnection._internal();
  }

  void query(String sql) => print("SQL bajarilmoqda: $sql");
}

void main() {
  var db1 = DatabaseConnection();
  var db2 = DatabaseConnection();

  print("db1 va db2 bitta ob'ektmi: ${identical(db1, db2)}");
  db1.query("SELECT * FROM users");
}
```

## Tushuntirish va Mantiq:
Singleton naqshi ma'lumotlar bazasi aloqalari, sozlamalar va audio pleyerlar kabi resurslarni bitta umumiy nuqtadan boshqarishni ta'minlaydi.

## Ishlash natijasi:
```text
db1 va db2 bitta ob'ektmi: true
SQL bajarilmoqda: SELECT * FROM users
```

# 364-Topshiriq: Konstruktor parametrlarida assert tekshiruvi
## Topshiriq sharti:
Konstruktorga noto'g'ri qiymatlar uzatilishining oldini olish uchun `assert` qo'llang.

## Yechim (Dart kodi):
```dart
class FoydalanuvchiYoshi {
  final int yosh;

  FoydalanuvchiYoshi(this.yosh)
      : assert(yosh >= 0, "Yosh manfiy bo'lishi mumkin emas!"),
        assert(yosh <= 150, "Bunday yosh mavjud emas!");
}

void main() {
  var u = FoydalanuvchiYoshi(25);
  print("Yoshi qabul qilindi: ${u.yosh}");
}
```

## Tushuntirish va Mantiq:
Konstruktordagi `assert` qoidalari ishlab chiqish (debug) vaqtida mantiqiy xatoliklarni zudlik bilan aniqlaydi.

## Ishlash natijasi:
```text
Yoshi qabul qilindi: 25
```

# 365-Topshiriq: Geometrik shakl: Doira klassi
## Topshiriq sharti:
Radius berilganda diametr, yuza va perimetrni hisoblovchi to'liq sinf yozing.

## Yechim (Dart kodi):
```dart
class Doira {
  final double radius;
  static const double pi = 3.14159265;

  Doira(this.radius);

  double get diametr => 2 * radius;
  double get yuza => pi * radius * radius;
  double get perimetr => 2 * pi * radius;
}

void main() {
  var d = Doira(10.0);
  print("Radius:   ${d.radius}");
  print("Diametr:  ${d.diametr}");
  print("Yuzasi:   ${d.yuza.toStringAsFixed(2)}");
  print("Perimetr: ${d.perimetr.toStringAsFixed(2)}");
}
```

## Tushuntirish va Mantiq:
`get` getterlari orqali hisoblanadigan qiymatlarni xuddi oddiy maydon kabi qulay o'qish mumkin.

## Ishlash natijasi:
```text
Radius:   10.0
Diametr:  20.0
Yuzasi:   314.16
Perimetr: 62.83
```

# 366-Topshiriq: Bank hisob raqami: Tranzaksiyalar tarixi bilan
## Topshiriq sharti:
Har bir kirim va chiqim operatsiyasini ro'yxatda saqlovchi bank klassini yarating.

## Yechim (Dart kodi):
```dart
class Account {
  final String owner;
  double _balance = 0.0;
  final List<String> _history = [];

  Account(this.owner, double initial) {
    if (initial > 0) deposit(initial);
  }

  void deposit(double amount) {
    _balance += amount;
    _history.add("+$amount so'm kiritildi. Balans: $_balance");
  }

  bool withdraw(double amount) {
    if (amount <= _balance) {
      _balance -= amount;
      _history.add("-$amount so'm yechildi. Balans: $_balance");
      return true;
    }
    _history.add("Muvaffaqiyatsiz urinish: -$amount so'm (Yetarli emas)");
    return false;
  }

  void printStatement() {
    print("--- Tranzaksiyalar tarixi ($owner) ---");
    _history.forEach(print);
  }
}

void main() {
  var acc = Account("Otabek", 100000);
  acc.deposit(50000);
  acc.withdraw(30000);
  acc.withdraw(200000); // Rad etiladi

  acc.printStatement();
}
```

## Tushuntirish va Mantiq:
Inkapsulyatsiya hisob balansini ruxsatsiz o'zgartirishdan asraydi va barcha amallarni qayd qilib boradi.

## Ishlash natijasi:
```text
--- Tranzaksiyalar tarixi (Otabek) ---
+100000.0 so'm kiritildi. Balans: 100000.0
+50000.0 so'm kiritildi. Balans: 150000.0
-30000.0 so'm yechildi. Balans: 120000.0
Muvaffaqiyatsiz urinish: -200000.0 so'm (Yetarli emas)
```

# 367-Topshiriq: Ob'ektlar kompozitsiyasi: Foydalanuvchi va Manzil
## Topshiriq sharti:
Bitta klass boshqa klass ob'ektini o'z ichiga olishi (Has-A munosabati) ni ko'rsating.

## Yechim (Dart kodi):
```dart
class Manzil {
  final String viloyat;
  final String shahar;
  Manzil(this.viloyat, this.shahar);

  @override
  String toString() => "$shahar, $viloyat";
}

class Mijoz {
  final String ism;
  final Manzil manzil;

  Mijoz(this.ism, this.manzil);
}

void main() {
  var m = Mijoz("Gulnora", Manzil("Farg'ona", "Qo'qon"));
  print("Mijoz: ${m.ism}, Yashash joyi: ${m.manzil}");
}
```

## Tushuntirish va Mantiq:
Kompozitsiya orqali murakkab ma'lumot modellari kichik, mustaqil va qayta ishlatiluvchi bo'laklardan yig'iladi.

## Ishlash natijasi:
```text
Mijoz: Gulnora, Yashash joyi: Qo'qon, Farg'ona
```

# 368-Topshiriq: Super parametrlar (Dart 2.17+ super.field)
## Topshiriq sharti:
Voris klass konstruktorida ota klass maydonlariga `super.maydon` orqali to'g'ridan-to'g'ri qiymat uzating.

## Yechim (Dart kodi):
```dart
class Xodim {
  final String ism;
  final double maosh;
  Xodim(this.ism, this.maosh);
}

class Menejer extends Xodim {
  final String bolim;

  // super.ism va super.maosh qisqa sintaksisi
  Menejer(super.ism, super.maosh, this.bolim);
}

void main() {
  var m = Menejer("Sardor", 12000000, "IT Bo'limi");
  print("Menejer: ${m.ism}, Maosh: ${m.maosh}, Bo'lim: ${m.bolim}");
}
```

## Tushuntirish va Mantiq:
Dart 2.17 da kiritilgan `super.field` sintaksisi ota konstruktorga parametrlarni uzatishdagi ortiqcha kodlarni yo'qotdi.

## Ishlash natijasi:
```text
Menejer: Sardor, Maosh: 12000000.0, Bo'lim: IT Bo'limi
```

# 369-Topshiriq: Kompleks sonlar klassi (Complex) va operatorlar (+, *)
## Topshiriq sharti:
Haqiqiy va mavhum qismga ega kompleks sonlar sinfini yozing va `+` operatorini qayta yuklang.

## Yechim (Dart kodi):
```dart
class Complex {
  final double re, im;
  Complex(this.re, this.im);

  Complex operator +(Complex other) {
    return Complex(re + other.re, im + other.im);
  }

  @override
  String toString() => "$re + ${im}i";
}

void main() {
  var c1 = Complex(2, 3);
  var c2 = Complex(4, 5);
  var c3 = c1 + c2;

  print("c1: $c1");
  print("c2: $c2");
  print("c1 + c2 = $c3");
}
```

## Tushuntirish va Mantiq:
Operatorlarni qayta yuklash (`operator +`) matematik ob'ektlar bilan ishlashni tabiiy va qulay qiladi.

## Ishlash natijasi:
```text
c1: 2.0 + 3.0i
c2: 4.0 + 5.0i
c1 + c2 = 6.0 + 8.0i
```

# 370-Topshiriq: Vaqt oraliqlari klassi: TimeRange va kesishuvni tekshirish
## Topshiriq sharti:
Boshlanish va tugash vaqtiga ega oraliq sinfini va ikki oraliq kesishishini tekshiruvchi metod yozing.

## Yechim (Dart kodi):
```dart
class TimeRange {
  final int startHour;
  final int endHour;

  TimeRange(this.startHour, this.endHour)
      : assert(startHour < endHour, "Boshlanish vaqti tugashidan kichik bo'lishi shart!");

  bool overlaps(TimeRange other) {
    return startHour < other.endHour && other.startHour < endHour;
  }
}

void main() {
  var r1 = TimeRange(9, 12);  // 09:00 - 12:00
  var r2 = TimeRange(11, 14); // 11:00 - 14:00
  var r3 = TimeRange(14, 18); // 14:00 - 18:00

  print("r1 va r2 kesishadimi: ${r1.overlaps(r2)}");
  print("r1 va r3 kesishadimi: ${r1.overlaps(r3)}");
}
```

## Tushuntirish va Mantiq:
Vaqt oraliqlari taqvimlarda (Google Calendar) va rejalashtirish tizimlarida eng muhim matematik modeldir.

## Ishlash natijasi:
```text
r1 va r2 kesishadimi: true
r1 va r3 kesishadimi: false
```

# 371-Topshiriq: Custom Stack ma'lumotlar tuzilmasi klassi
## Topshiriq sharti:
Generik `CustomStack<T>` sinfini yozing, `push`, `pop`, `peek`, `isEmpty` metodlarini taqdim eting.

## Yechim (Dart kodi):
```dart
class CustomStack<T> {
  final List<T> _data = [];

  void push(T item) => _data.add(item);
  T pop() => _data.removeLast();
  T peek() => _data.last;
  bool get isEmpty => _data.isEmpty;
  int get size => _data.length;
}

void main() {
  var stack = CustomStack<int>();
  stack.push(10);
  stack.push(20);

  print("Tepa element: ${stack.peek()}");
  print("Chiqarildi:   ${stack.pop()}");
  print("Qolgan o'lcham: ${stack.size}");
}
```

## Tushuntirish va Mantiq:
Klasslar ichki ma'lumot tuzilmalarini toza interfeys bilan tashqi dunyodan himoyalaydi.

## Ishlash natijasi:
```text
Tepa element: 20
Chiqarildi:   20
Qolgan o'lcham: 1
```

# 372-Topshiriq: Logger (Jurnal) klassi log darajalari bilan
## Topshiriq sharti:
INFO, WARN, ERROR xabarlarini vaqt tamg'asi bilan konsolga chiqaruvchi logger yozing.

## Yechim (Dart kodi):
```dart
enum LogLevel { info, warn, error }

class Logger {
  final String tag;
  Logger(this.tag);

  void log(LogLevel level, String message) {
    String levelName = level.name.toUpperCase();
    print("[$levelName] [$tag]: $message");
  }

  void info(String msg) => log(LogLevel.info, msg);
  void warn(String msg) => log(LogLevel.warn, msg);
  void error(String msg) => log(LogLevel.error, msg);
}

void main() {
  var log = Logger("AuthService");
  log.info("Foydalanuvchi tizimga kirdi");
  log.warn("Parol eskirmoqda");
  log.error("Server bilan aloqa uzildi");
}
```

## Tushuntirish va Mantiq:
Tizimli jurnal qaydlari (logging) ilovalarni nosozliklardan tozalash va kuzatishning asosi hisoblanadi.

## Ishlash natijasi:
```text
[INFO] [AuthService]: Foydalanuvchi tizimga kirdi
[WARN] [AuthService]: Parol eskirmoqda
[ERROR] [AuthService]: Server bilan aloqa uzildi
```

# 373-Topshiriq: Oddiy HTTP Request modeli
## Topshiriq sharti:
URL, HTTP metod, Headerlar va Body ni o'z ichiga olgan so'rov sinfini tuzing.

## Yechim (Dart kodi):
```dart
class HttpRequestModel {
  final String url;
  final String method;
  final Map<String, String> headers;
  final String? body;

  HttpRequestModel({
    required this.url,
    this.method = "GET",
    this.headers = const {},
    this.body,
  });

  @override
  String toString() => "$method $url (Headers: ${headers.length})";
}

void main() {
  var req = HttpRequestModel(
    url: "https://api.uzbek.ai/v1/generate",
    method: "POST",
    headers: {"Authorization": "Bearer 12345"},
    body: '{"prompt": "Salom"}',
  );

  print("Yaratilgan so'rov: $req");
}
```

## Tushuntirish va Mantiq:
DTO (Data Transfer Object) modellari tarmoq so'rovlarini to'liq tartibga soladi.

## Ishlash natijasi:
```text
Yaratilgan so'rov: POST https://api.uzbek.ai/v1/generate (Headers: 1)
```

# 374-Topshiriq: Pagination (Sahifalash) metadata klassi
## Topshiriq sharti:
Joriy sahifa, har bir sahifadagi elementlar soni va jami elementlar orqali jami sahifalarni hisoblovchi sinf yozing.

## Yechim (Dart kodi):
```dart
class Pagination {
  final int currentPage;
  final int pageSize;
  final int totalItems;

  Pagination({required this.currentPage, required this.pageSize, required this.totalItems});

  int get totalPages => (totalItems / pageSize).ceil();
  bool get hasNext => currentPage < totalPages;
  bool get hasPrev => currentPage > 1;
}

void main() {
  var p = Pagination(currentPage: 2, pageSize: 10, totalItems: 45);

  print("Jami elementlar: ${p.totalItems}");
  print("Jami sahifalar:  ${p.totalPages}");
  print("Keyingi sahifa bormi: ${p.hasNext}");
  print("Oldingi sahifa bormi: ${p.hasPrev}");
}
```

## Tushuntirish va Mantiq:
Sahifalash hisob-kitoblari ma'lumotlar bazasi jadvallarini sahifalab ko'rsatishda standart hisoblanadi.

## Ishlash natijasi:
```text
Jami elementlar: 45
Jami sahifalar:  5
Keyingi sahifa bormi: true
Oldingi sahifa bormi: true
```

# 375-Topshiriq: Binar Tenzor shakli klassi: TensorShape(dims)
## Topshiriq sharti:
AI tenzorlarining o'lchamlarini (dimensions) saqlovchi va jami elementlar sonini hisoblovchi sinf yozing.

## Yechim (Dart kodi):
```dart
class TensorShape {
  final List<int> dims;
  TensorShape(this.dims);

  int get totalElements => dims.fold(1, (acc, dim) => acc * dim);
  int get rank => dims.length;

  @override
  String toString() => "[${dims.join('x')}]";
}

void main() {
  var shape = TensorShape([2, 4, 8]); // Masalan Batch x SeqLen x Dim

  print("Tenzor shakli: $shape");
  print("Tenzor rangi (o'lchami): ${shape.rank}D");
  print("Jami elementlar soni:    ${shape.totalElements}");
}
```

## Tushuntirish va Mantiq:
Tenzor shakli neyron tarmoqlar qatlamlari o'rtasida ma'lumotlar hajmini nazorat qilishning asosiy qismidir.

## Ishlash natijasi:
```text
Tenzor shakli: [2x4x8]
Tenzor rangi (o'lchami): 3D
Jami elementlar soni:    64
```

# 376-Topshiriq: Klass nusxalarini List ichida saqlash va saralash

## Topshiriq sharti:
Klass nusxalari (Talaba) ro'yxatini yaratish, ularni baholari bo'yicha kamayish tartibida saralash va filtrlash dasturini tuzing.

## Yechim (Dart kodi):
```dart
class Talaba {
  final String ism;
  final double ball;

  Talaba(this.ism, this.ball);

  @override
  String toString() => '$ism: $ball ball';
}

void main() {
  List<Talaba> guruh = [
    Talaba('Jasur', 84.5),
    Talaba('Madina', 95.0),
    Talaba('Bobur', 72.3),
    Talaba('Zuhra', 91.2),
  ];

  // Ball bo'yicha kamayish tartibida saralash
  guruh.sort((a, b) => b.ball.compareTo(a.ball));

  print('Saralangan reyting:');
  for (var t in guruh) {
    print('- $t');
  }

  // 90 dan yuqori ball to'plaganlar
  var aotchilar = guruh.where((t) => t.ball >= 90);
  print('
90+ olganlar: ${aotchilar.map((e) => e.ism).join(", ")}');
}
```

## Tushuntirish va Mantiq:
Klass obyektlarini List ichida saqlab, `sort()` metodi yordamida obyekt maydonlariga ko'ra saralash mumkin. `where()` yordamida ma'lum shartga ko'ra filtrlanadi.

## Ishlash natijasi:
```text
Saralangan reyting:
- Madina: 95.0 ball
- Zuhra: 91.2 ball
- Jasur: 84.5 ball
- Bobur: 72.3 ball

90+ olganlar: Madina, Zuhra
```

# 377-Topshiriq: Avtomobil klassi va yoqilg'i sarfi monitoringi

## Topshiriq sharti:
Avtomobil modeli, bak sig'imi va 100 km ga sarfi ko'rsatilgan klass yarating. Masofa bosib o'tganda yoqilg'i kamayishi va yoqilg'i quyish metodlarini yozing.

## Yechim (Dart kodi):
```dart
class Avtomobil {
  final String model;
  final double bakHajmi;
  final double sarf100km;
  double _mavjudYoqilgi;

  Avtomobil({
    required this.model,
    required this.bakHajmi,
    required this.sarf100km,
  }) : _mavjudYoqilgi = bakHajmi;

  double get mavjudYoqilgi => _mavjudYoqilgi;

  void haydash(double masofaKm) {
    double zarurYoqilgi = (masofaKm / 100) * sarf100km;
    if (zarurYoqilgi <= _mavjudYoqilgi) {
      _mavjudYoqilgi -= zarurYoqilgi;
      print('$model $masofaKm km yurdi. Qoldi: ${_mavjudYoqilgi.toStringAsFixed(1)} L');
    } else {
      print('$model uchun yoqilgi yetarli emas! Talab: ${zarurYoqilgi.toStringAsFixed(1)} L, Mavjud: ${_mavjudYoqilgi.toStringAsFixed(1)} L');
    }
  }

  void zapravka(double litr) {
    _mavjudYoqilgi = (_mavjudYoqilgi + litr).clamp(0, bakHajmi);
    print('$litr L quyildi. Bakdagi umumiy: ${_mavjudYoqilgi.toStringAsFixed(1)} L');
  }
}

void main() {
  var cobalt = Avtomobil(model: 'Cobalt', bakHajmi: 50.0, sarf100km: 7.5);
  cobalt.haydash(200);
  cobalt.haydash(500);
  cobalt.zapravka(20);
  cobalt.haydash(200);
}
```

## Tushuntirish va Mantiq:
Private maydon `_mavjudYoqilgi` tashqaridan faqat getter orqali o'qiladi. O'zgarishlar faqat `haydash()` va `zapravka()` metodlari orqali nazorat ostida amalga oshiriladi.

## Ishlash natijasi:
```text
Cobalt 200.0 km yurdi. Qoldi: 35.0 L
Cobalt uchun yoqilgi yetarli emas! Talab: 37.5 L, Mavjud: 35.0 L
20.0 L quyildi. Bakdagi umumiy: 50.0 L
Cobalt 200.0 km yurdi. Qoldi: 35.0 L
```

# 378-Topshiriq: Buyurtma (Order) va Buyurtma elementlari (OrderItem)

## Topshiriq sharti:
Har bir buyurtma elementi (nomi, narxi, miqdori) bo'lgan va butun buyurtma umumiy summasini hisoblovchi klasslar tizimini tuzing.

## Yechim (Dart kodi):
```dart
class BuyurtmaElementi {
  final String nom;
  final double narx;
  final int miqdor;

  BuyurtmaElementi(this.nom, this.narx, this.miqdor);

  double get jami => narx * miqdor;
}

class Buyurtma {
  final int id;
  final List<BuyurtmaElementi> elementlar = [];

  Buyurtma(this.id);

  void qoshish(BuyurtmaElementi item) {
    elementlar.add(item);
  }

  double get umumiySumma => elementlar.fold(0.0, (sum, item) => sum + item.jami);

  void chekChiqarish() {
    print('--- Buyurtma #$id Cheki ---');
    for (var it in elementlar) {
      print('${it.nom} x ${it.miqdor} dona = ${it.jami.toStringAsFixed(0)} so\'m');
    }
    print('JAMI TO\'LOV: ${umumiySumma.toStringAsFixed(0)} so\'m');
  }
}

void main() {
  var b = Buyurtma(101);
  b.qoshish(BuyurtmaElementi('Kofe Latte', 22000, 2));
  b.qoshish(BuyurtmaElementi('Kruassan', 18000, 3));
  b.chekChiqarish();
}
```

## Tushuntirish va Mantiq:
`Buyurtma` klassi ichida `List<BuyurtmaElementi>` saqlanadi va `fold` orqali elementlarning umumiy summasi avtomatik hisoblanadi.

## Ishlash natijasi:
```text
--- Buyurtma #101 Cheki ---
Kofe Latte x 2 dona = 44000 so'm
Kruassan x 3 dona = 54000 so'm
JAMI TO'LOV: 98000 so'm
```

# 379-Topshiriq: Xodimlar va Bo'limlar modeli (Idoraviy tuzilma)

## Topshiriq sharti:
Bo'lim (Department) klassi va unga tegishli Xodimlar (Employee) ro'yxatini boshqaruvchi tuzilma yarating.

## Yechim (Dart kodi):
```dart
class Xodim {
  final String ism;
  final String lavozim;
  final double maosh;

  Xodim(this.ism, this.lavozim, this.maosh);
}

class Bolim {
  final String nom;
  final List<Xodim> _xodimlar = [];

  Bolim(this.nom);

  void qabulQilish(Xodim x) {
    _xodimlar.add(x);
  }

  double get umumiyOylikFond => _xodimlar.fold(0.0, (s, x) => s + x.maosh);

  void xodimlarRoyxati() {
    print('Bo\'lim: $nom (Xodimlar: ${_xodimlar.length})');
    for (var x in _xodimlar) {
      print('- ${x.ism} (${x.lavozim}): ${x.maosh.toStringAsFixed(0)} so\'m');
    }
    print('Oylik maosh fondi: ${umumiyOylikFond.toStringAsFixed(0)} so\'m
');
  }
}

void main() {
  var itBolim = Bolim('Dasturiy Ta\'minot');
  itBolim.qabulQilish(Xodim('Alisher', 'Dart/Flutter Tech Lead', 35000000));
  itBolim.qabulQilish(Xodim('Malika', 'AI Backend Engineer', 30000000));

  itBolim.xodimlarRoyxati();
}
```

## Tushuntirish va Mantiq:
Kompaniya tarkibidagi bo'lim va uning xodimlari orasidagi bir-ko'p (one-to-many) munosabat klasslar orqali modellashtirildi.

## Ishlash natijasi:
```text
Bo'lim: Dasturiy Ta'minot (Xodimlar: 2)
- Alisher (Dart/Flutter Tech Lead): 35000000 so'm
- Malika (AI Backend Engineer): 30000000 so'm
Oylik maosh fondi: 65000000 so'm
```

# 380-Topshiriq: Kutubxona katalogi (Kitob va Javon klasslari)

## Topshiriq sharti:
Kitob klassi va kutubxona javoni klassini yarating. Javonga kitob qo'shish, nomi bo'yicha qidirish va olish metodlarini yozing.

## Yechim (Dart kodi):
```dart
class Kitob {
  final String isbn;
  final String sarlavha;
  final String muallif;
  bool mavjud;

  Kitob(this.isbn, this.sarlavha, this.muallif, {this.mavjud = true});
}

class KutubxonaJavoni {
  final List<Kitob> kitoblar = [];

  void qoshish(Kitob k) => kitoblar.add(k);

  Kitob? topish(String nom) {
    for (var k in kitoblar) {
      if (k.sarlavha.toLowerCase().contains(nom.toLowerCase())) {
        return k;
      }
    }
    return null;
  }

  void kitobOlish(String nom) {
    var k = topish(nom);
    if (k != null) {
      if (k.mavjud) {
        k.mavjud = false;
        print('"${k.sarlavha}" kitobi berildi.');
      } else {
        print('"${k.sarlavha}" kitobi ayni vaqtda band.');
      }
    } else {
      print('Kitob topilmadi: $nom');
    }
  }
}

void main() {
  var javon = KutubxonaJavoni();
  javon.qoshish(Kitob('978-1', 'Dart Dasturlash Asoslari', 'Munir'));
  javon.qoshish(Kitob('978-2', 'O\'tkan Kunlar', 'Abdulla Qodiriy'));

  javon.kitobOlish('Dart');
  javon.kitobOlish('Dart');
}
```

## Tushuntirish va Mantiq:
`topish()` metodi `Kitob?` qaytaradi, null-safety yordamida kitob mavjudligi va holati tekshiriladi.

## Ishlash natijasi:
```text
"Dart Dasturlash Asoslari" kitobi berildi.
"Dart Dasturlash Asoslari" kitobi ayni vaqtda band.
```

# 381-Topshiriq: Raqamli soat klassi (Soat, minut, sekund hisobi)

## Topshiriq sharti:
Soat, minut, sekundni saqlovchi va sekundlar o'tganda vaqtni avtomatik yangilovchi DigitalClock klassini yarating.

## Yechim (Dart kodi):
```dart
class RaqamliSoat {
  int _soat;
  int _minut;
  int _sekund;

  RaqamliSoat([this._soat = 0, this._minut = 0, this._sekund = 0]);

  void sekundQoshish(int sek) {
    _sekund += sek;
    _minut += _sekund ~/ 60;
    _sekund %= 60;

    _soat += _minut ~/ 60;
    _minut %= 60;

    _soat %= 24;
  }

  String formatVaqt() {
    String f(int n) => n.toString().padLeft(2, '0');
    return '${f(_soat)}:${f(_minut)}:${f(_sekund)}';
  }
}

void main() {
  var soat = RaqamliSoat(23, 58, 45);
  print('Boshlang\'ich: ${soat.formatVaqt()}');

  soat.sekundQoshish(80);
  print('80 soniyadan keyin: ${soat.formatVaqt()}');

  soat.sekundQoshish(60);
  print('Yana 60 soniyadan keyin: ${soat.formatVaqt()}');
}
```

## Tushuntirish va Mantiq:
`padLeft(2, '0')` orqali bir xonali sonlar oldiga 0 qo'shiladi va 24 soatlik tizim bo'yicha to'g'ri o'tish hisoblanadi.

## Ishlash natijasi:
```text
Boshlang'ich: 23:58:45
80 soniyadan keyin: 00:00:05
Yana 60 soniyadan keyin: 00:01:05
```

# 382-Topshiriq: Harorat konverteri klassi (Celsius, Fahrenheit, Kelvin)

## Topshiriq sharti:
Haroratni saqlovchi va turli o'lchov birliklariga o'giruvchi (Fahrenheit, Kelvin) klass tuzing.

## Yechim (Dart kodi):
```dart
class Harorat {
  final double celsius;

  const Harorat.fromCelsius(this.celsius);
  Harorat.fromFahrenheit(double f) : celsius = (f - 32) * 5 / 9;
  Harorat.fromKelvin(double k) : celsius = k - 273.15;

  double get fahrenheit => (celsius * 9 / 5) + 32;
  double get kelvin => celsius + 273.15;

  @override
  String toString() => '${celsius.toStringAsFixed(1)}°C | ${fahrenheit.toStringAsFixed(1)}°F | ${kelvin.toStringAsFixed(2)}K';
}

void main() {
  var h1 = Harorat.fromCelsius(25.0);
  var h2 = Harorat.fromFahrenheit(98.6);
  var h3 = Harorat.fromKelvin(300.0);

  print('Xona harorati: $h1');
  print('Tana harorati: $h2');
  print('300 Kelvin:    $h3');
}
```

## Tushuntirish va Mantiq:
Bir nechta named konstruktorlar yordamida ixtiyoriy birlikdan obyekt yaratish mumkin va ichki holat bitta birlikda (Celsius) saqlanadi.

## Ishlash natijasi:
```text
Xona harorati: 25.0°C | 77.0°F | 298.15K
Tana harorati: 37.0°C | 98.6°F | 310.15K
300 Kelvin:    26.9°C | 80.3°F | 300.00K
```

# 383-Topshiriq: Foydalanuvchi profili va xavfsiz parol tekshiruvi

## Topshiriq sharti:
Foydalanuvchi parolini ochiq holda saqlamaydigan, xesh yoki oddiy xavfsizlik tekshiruviga ega User klassini yarating.

## Yechim (Dart kodi):
```dart
class Foydalanuvchi {
  final String login;
  final int _parolHash;

  Foydalanuvchi(this.login, String xomParol) : _parolHash = _hisoblaHash(xomParol);

  static int _hisoblaHash(String p) {
    // Oddiy xesh hisoblash misoli
    return p.codeUnits.fold(5381, (h, c) => ((h << 5) + h) + c);
  }

  bool parolTogrimi(String p) {
    return _hisoblaHash(p) == _parolHash;
  }
}

void main() {
  var user = Foydalanuvchi('sarvar', 'SirliParol123');
  print('Parol: "notogri" -> ${user.parolTogrimi("notogri")}');
  print('Parol: "SirliParol123" -> ${user.parolTogrimi("SirliParol123")}');
}
```

## Tushuntirish va Mantiq:
Xom parol xotirada saqlanmaydi, faqat uning xesh qiymati `_parolHash` saqlanadi. Bu xavfsizlik talablariga mos keladi.

## Ishlash natijasi:
```text
Parol: "notogri" -> false
Parol: "SirliParol123" -> true
```

# 384-Topshiriq: Matnli xabar klassi (Chat xabari modeli)

## Topshiriq sharti:
Yuboruvchi, qabul qiluvchi, matn va yuborilgan vaqtni saqlovchi Message klassini yarating.

## Yechim (Dart kodi):
```dart
class Xabar {
  final String yuboruvchi;
  final String qabulQiluvchi;
  final String matn;
  final DateTime vaqt;
  bool oqildi;

  Xabar({
    required this.yuboruvchi,
    required this.qabulQiluvchi,
    required this.matn,
    DateTime? vaqt,
    this.oqildi = false,
  }) : vaqt = vaqt ?? DateTime.now();

  void oqildiBelgilash() => oqildi = true;

  @override
  String toString() {
    return '[${vaqt.hour.toString().padLeft(2, '0')}:${vaqt.minute.toString().padLeft(2, '0')}] '
           '$yuboruvchi -> $qabulQiluvchi: "$matn" (${oqildi ? "o'qildi" : "yangi"})';
  }
}

void main() {
  var xabar = Xabar(
    yuboruvchi: 'Anvar',
    qabulQiluvchi: 'Nodira',
    matn: 'Salom, Dart loyihasi tayyormi?',
    vaqt: DateTime(2026, 11, 7, 14, 30),
  );
  print(xabar);
  xabar.oqildiBelgilash();
  print(xabar);
}
```

## Tushuntirish va Mantiq:
DateTime default qiymatini konstruktor tanasida yoki initializer listda null tekshiruvi orqali initsializatsiya qilish mumkin.

## Ishlash natijasi:
```text
[14:30] Anvar -> Nodira: "Salom, Dart loyihasi tayyormi?" (yangi)
[14:30] Anvar -> Nodira: "Salom, Dart loyihasi tayyormi?" (o'qildi)
```

# 385-Topshiriq: Valyuta hamyoni klassi (Ko'p valyutali hisob)

## Topshiriq sharti:
Turli valyutalarda pul saqlaydigan va kurs bo'yicha umumiy balansni hisoblaydigan ValyutaHamyoni klassini tuzing.

## Yechim (Dart kodi):
```dart
class ValyutaHamyoni {
  final Map<String, double> balanslar = {};

  void depozit(String valyuta, double miqdor) {
    balanslar[valyuta] = (balanslar[valyuta] ?? 0.0) + miqdor;
  }

  double umumiyUZS(Map<String, double> kurslar) {
    double jami = 0.0;
    balanslar.forEach((v, m) {
      if (v == 'UZS') {
        jami += m;
      } else if (kurslar.containsKey(v)) {
        jami += m * kurslar[v]!;
      }
    });
    return jami;
  }
}

void main() {
  var hamyon = ValyutaHamyoni();
  hamyon.depozit('UZS', 500000);
  hamyon.depozit('USD', 100);
  hamyon.depozit('EUR', 50);

  Map<String, double> kurslar = {
    'USD': 12800.0,
    'EUR': 13800.0,
  };

  print('Umumiy balans (UZS): ${hamyon.umumiyUZS(kurslar).toStringAsFixed(0)} so\'m');
}
```

## Tushuntirish va Mantiq:
Map ichida valyuta kodlari va ularning balanslari saqlanadi, so'ng kurslar bo'yicha UZS ga o'girilib hisoblanadi.

## Ishlash natijasi:
```text
Umumiy balans (UZS): 2470000 so'm
```

# 386-Topshiriq: Matritsa klassi va 2D massiv amallari

## Topshiriq sharti:
Satr va ustun o'lchamiga ega Matritsa klassini yarating, elementlarni olish, qo'yish va matritsani chop etish imkonini bering.

## Yechim (Dart kodi):
```dart
class Matritsa {
  final int qatorlar;
  final int ustunlar;
  final List<List<double>> _kataklar;

  Matritsa(this.qatorlar, this.ustunlar, [double boshlangich = 0.0])
      : _kataklar = List.generate(
          qatorlar,
          (_) => List.filled(ustunlar, boshlangich),
        );

  double get(int r, int c) => _kataklar[r][c];
  void set(int r, int c, double val) => _kataklar[r][c] = val;

  void chopEtish() {
    for (var satr in _kataklar) {
      print(satr.map((e) => e.toStringAsFixed(1).padLeft(6)).join(' '));
    }
  }
}

void main() {
  var m = Matritsa(3, 3);
  for (int i = 0; i < 3; i++) {
    m.set(i, i, 1.0); // Birlik matritsa
  }
  m.set(0, 1, 2.5);
  m.chopEtish();
}
```

## Tushuntirish va Mantiq:
2D massiv Dartda `List<List<double>>` yordamida yaratiladi. `List.generate()` bilan qulay initsializatsiya qilinadi.

## Ishlash natijasi:
```text
   1.0    2.5    0.0
   0.0    1.0    0.0
   0.0    0.0    1.0
```

# 387-Topshiriq: Log yozuvchisi klassi (Logger klassi)

## Topshiriq sharti:
Turli darajadagi xabarlarni (INFO, WARN, ERROR) formatlab konsolga chiqaruvchi Logger klassini tuzing.

## Yechim (Dart kodi):
```dart
enum LogDaraja { info, ogohlantirish, xatolik }

class Logger {
  final String modulNomi;

  Logger(this.modulNomi);

  void _yoz(LogDaraja daraja, String xabar) {
    String belgi;
    switch (daraja) {
      case LogDaraja.info:
        belgi = '[INFO]';
      case LogDaraja.ogohlantirish:
        belgi = '[WARN]';
      case LogDaraja.xatolik:
        belgi = '[ERROR]';
    }
    print('$belgi [$modulNomi]: $xabar');
  }

  void info(String xabar) => _yoz(LogDaraja.info, xabar);
  void warn(String xabar) => _yoz(LogDaraja.ogohlantirish, xabar);
  void error(String xabar) => _yoz(LogDaraja.xatolik, xabar);
}

void main() {
  var log = Logger('AuthService');
  log.info('Foydalanuvchi tizimga kirdi');
  log.warn('Sessiya muddati tugamoqda');
  log.error('Noto\'g\'ri token taqdim etildi');
}
```

## Tushuntirish va Mantiq:
Logger klassi yordamida ilovadagi xabarlarni bir xil formatda va modullarga ajratgan holda konsolga chiqarish mumkin.

## Ishlash natijasi:
```text
[INFO] [AuthService]: Foydalanuvchi tizimga kirdi
[WARN] [AuthService]: Sessiya muddati tugamoqda
[ERROR] [AuthService]: Noto'g'ri token taqdim etildi
```

# 388-Topshiriq: Kalendar sanasi klassi va kabisa yili tekshiruvi

## Topshiriq sharti:
Yil, oy, kun parametrlarini qabul qiluvchi va berilgan yil kabisa yili ekanligini hisoblovchi Sana klassini yarating.

## Yechim (Dart kodi):
```dart
class Sana {
  final int yil;
  final int oy;
  final int kun;

  Sana(this.yil, this.oy, this.kun) {
    assert(oy >= 1 && oy <= 12, 'Oy 1 va 12 oralig\'ida bo\'lishi kerak');
    assert(kun >= 1 && kun <= 31, 'Kun 1 va 31 oralig\'ida bo\'lishi kerak');
  }

  bool get kabisaYilimi {
    return (yil % 4 == 0 && yil % 100 != 0) || (yil % 400 == 0);
  }

  @override
  String toString() => '${yil.toString().padLeft(4, '0')}-${oy.toString().padLeft(2, '0')}-${kun.toString().padLeft(2, '0')}';
}

void main() {
  var s1 = Sana(2024, 2, 29);
  var s2 = Sana(2026, 11, 7);

  print('$s1 -> Kabisa yili: ${s1.kabisaYilimi}');
  print('$s2 -> Kabisa yili: ${s2.kabisaYilimi}');
}
```

## Tushuntirish va Mantiq:
Kabisa yili formulasi: 4 ga karrali va 100 ga karrali bo'lmagan yoki 400 ga karrali bo'lgan yillar kabisa hisoblanadi.

## Ishlash natijasi:
```text
2024-02-29 -> Kabisa yili: true
2026-11-07 -> Kabisa yili: false
```

# 389-Topshiriq: Dinamik ro'yxat (Custom Dynamic Array klassi)

## Topshiriq sharti:
O'zining ichki massiv sig'imi to'lganda avtomatik kengayadigan CustomList klassini amalga oshiring.

## Yechim (Dart kodi):
```dart
class MaxsusList {
  List<int?> _ichki = List.filled(2, null);
  int _uzunlik = 0;

  int get length => _uzunlik;

  void qoshish(int qiymat) {
    if (_uzunlik == _ichki.length) {
      _kengaytirish();
    }
    _ichki[_uzunlik++] = qiymat;
  }

  void _kengaytirish() {
    List<int?> yangi = List.filled(_ichki.length * 2, null);
    for (int i = 0; i < _uzunlik; i++) {
      yangi[i] = _ichki[i];
    }
    _ichki = yangi;
  }

  int operator [](int index) {
    if (index < 0 || index >= _uzunlik) throw IndexError.withLength(index, _uzunlik);
    return _ichki[index]!;
  }
}

void main() {
  var royxat = MaxsusList();
  royxat.qoshish(10);
  royxat.qoshish(20);
  royxat.qoshish(30); // Massiv avtomatik 4 gacha kengayadi
  royxat.qoshish(40);

  print('Elementlar soni: ${royxat.length}');
  for (int i = 0; i < royxat.length; i++) {
    print('[$i] = ${royxat[i]}');
  }
}
```

## Tushuntirish va Mantiq:
Massiv to'lganda uning sig'imi 2 baravarga oshiriladi (`growth factor = 2`), bu dinamik massivlarning klassik ishlash prinsipi hisoblanadi.

## Ishlash natijasi:
```text
Elementlar soni: 4
[0] = 10
[1] = 20
[2] = 30
[3] = 40
```

# 390-Topshiriq: Stack (To'plam) ma'lumotlar tuzilmasi klassi

## Topshiriq sharti:
LIFO (Last In First Out) tamoyili asosida ishlovchi Stack klassini (push, pop, peek, isEmpty) tuzing.

## Yechim (Dart kodi):
```dart
class Stack<T> {
  final List<T> _elementlar = [];

  void push(T element) => _elementlar.add(element);

  T pop() {
    if (isEmpty) throw StateError('Stack bo\'sh!');
    return _elementlar.removeLast();
  }

  T peek() {
    if (isEmpty) throw StateError('Stack bo\'sh!');
    return _elementlar.last;
  }

  bool get isEmpty => _elementlar.isEmpty;
  int get length => _elementlar.length;
}

void main() {
  var s = Stack<String>();
  s.push('A');
  s.push('B');
  s.push('C');

  print('Yuqori element: ${s.peek()}');
  print('Pop: ${s.pop()}');
  print('Pop: ${s.pop()}');
  print('Qoldiq uzunlik: ${s.length}');
}
```

## Tushuntirish va Mantiq:
Dartdagi `List.removeLast()` va `List.last` metodlari yordamida samarali O(1) vaqt murakkabligida Stack tuzilmasini yaratish mumkin.

## Ishlash natijasi:
```text
Yuqori element: C
Pop: C
Pop: B
Qoldiq uzunlik: 1
```

# 391-Topshiriq: Queue (Navbat) ma'lumotlar tuzilmasi klassi

## Topshiriq sharti:
FIFO (First In First Out) tamoyili asosida ishlovchi Queue klassini tuzing.

## Yechim (Dart kodi):
```dart
class Navbat<T> {
  final List<T> _qator = [];

  void enqueue(T item) => _qator.add(item);

  T dequeue() {
    if (isEmpty) throw StateError('Navbat bo\'sh!');
    return _qator.removeAt(0);
  }

  bool get isEmpty => _qator.isEmpty;
  int get length => _qator.length;
}

void main() {
  var navbat = Navbat<String>();
  navbat.enqueue('Mijoz #1');
  navbat.enqueue('Mijoz #2');
  navbat.enqueue('Mijoz #3');

  print('Xizmat ko\'rsatildi: ${navbat.dequeue()}');
  print('Xizmat ko\'rsatildi: ${navbat.dequeue()}');
  print('Kutayotganlar soni: ${navbat.length}');
}
```

## Tushuntirish va Mantiq:
Queue birinchi kelgan birinchi chiqadi tamoyili asosida ishlaydi. `enqueue` oxiriga qo'shadi, `dequeue` boshidan sug'uradi.

## Ishlash natijasi:
```text
Xizmat ko'rsatildi: Mijoz #1
Xizmat ko'rsatildi: Mijoz #2
Kutayotganlar soni: 1
```

# 392-Topshiriq: Shaxsiy kompyuter konfiguratsiyasi klassi (Kompozitsiya)

## Topshiriq sharti:
CPU, RAM va SSD klasslarini birlashtiruvchi Kompyuter klassini kompozitsiya usulida yarating.

## Yechim (Dart kodi):
```dart
class Protsessor {
  final String model;
  final int yadrolar;
  Protsessor(this.model, this.yadrolar);
}

class Xotira {
  final int hajmiGb;
  Xotira(this.hajmiGb);
}

class Kompyuter {
  final String brend;
  final Protsessor cpu;
  final Xotira ram;

  Kompyuter({required this.brend, required this.cpu, required this.ram});

  void tafsilotlar() {
    print('Kompyuter: $brend');
    print('- Protsessor: ${cpu.model} (${cpu.yadrolar} yadro)');
    print('- Tezkor xotira (RAM): ${ram.hajmiGb} GB');
  }
}

void main() {
  var pc = Kompyuter(
    brend: 'AI Workstation',
    cpu: Protsessor('Apple M3 Max', 16),
    ram: Xotira(64),
  );
  pc.tafsilotlar();
}
```

## Tushuntirish va Mantiq:
Kompozitsiya (has-a munosabati) orqali murakkab obyektlar soddaroq obyektlar yig'indisi sifatida shakllantiriladi.

## Ishlash natijasi:
```text
Kompyuter: AI Workstation
- Protsessor: Apple M3 Max (16 yadro)
- Tezkor xotira (RAM): 64 GB
```

# 393-Topshiriq: GPS koordinatalari va masofa hisoblash (Haversine)

## Topshiriq sharti:
Kenglik va uzunlikni saqlovchi GPSPoint klassi va ikki nuqta orasidagi masofani hisoblash dasturini yozing.

## Yechim (Dart kodi):
```dart
import 'dart:math';

class GpsNuqta {
  final double kenglik;
  final double uzunlik;

  const GpsNuqta(this.kenglik, this.uzunlik);

  double masofaKm(GpsNuqta boshqa) {
    const double r = 6371; // Yer radiusi km
    double dLat = _rad(boshqa.kenglik - kenglik);
    double dLon = _rad(boshqa.uzunlik - uzunlik);

    double a = sin(dLat / 2) * sin(dLat / 2) +
        cos(_rad(kenglik)) * cos(_rad(boshqa.kenglik)) * sin(dLon / 2) * sin(dLon / 2);
    double c = 2 * atan2(sqrt(a), sqrt(1 - a));
    return r * c;
  }

  static double _rad(double gradus) => gradus * pi / 180;
}

void main() {
  var toshkent = GpsNuqta(41.2995, 69.2401);
  var samarqand = GpsNuqta(39.6270, 66.9750);

  double km = toshkent.masofaKm(samarqand);
  print('Toshkent va Samarqand orasidagi masofa: ${km.toStringAsFixed(1)} km');
}
```

## Tushuntirish va Mantiq:
Haversine formulasi Yer sharidagi ikki geografik koordinata orasidagi katta aylana masofasini aniq hisoblaydi.

## Ishlash natijasi:
```text
Toshkent va Samarqand orasidagi masofa: 268.3 km
```

# 394-Topshiriq: Sensor o'lchovlari klassi (Statistika hisoblagich)

## Topshiriq sharti:
Sensor ma'lumotlarini qabul qiluvchi, min, max va o'rtacha qiymatni hisoblab boruvchi SensorStatistikasi klassini yarating.

## Yechim (Dart kodi):
```dart
import 'dart:math';

class SensorStatistikasi {
  double _min = double.infinity;
  double _max = -double.infinity;
  double _sum = 0.0;
  int _soni = 0;

  void qoshish(double qiymat) {
    _min = min(_min, qiymat);
    _max = max(_max, qiymat);
    _sum += qiymat;
    _soni++;
  }

  double get ortacha => _soni == 0 ? 0.0 : _sum / _soni;
  double get minQiymat => _soni == 0 ? 0.0 : _min;
  double get maxQiymat => _soni == 0 ? 0.0 : _max;

  void hisobot() {
    print('O\'lchovlar soni: $_soni');
    print('Min: $minQiymat | Max: $maxQiymat | O\'rtacha: ${ortacha.toStringAsFixed(2)}');
  }
}

void main() {
  var stat = SensorStatistikasi();
  [21.5, 22.0, 24.3, 19.8, 23.1].forEach(stat.qoshish);
  stat.hisobot();
}
```

## Tushuntirish va Mantiq:
Sensor o'lchovlari kelishi bilan min, max va yig'indini yangilab borish xotirani tejaydi (barcha qiymatlarni saqlash shart emas).

## Ishlash natijasi:
```text
O'lchovlar soni: 5
Min: 19.8 | Max: 24.3 | O'rtacha: 22.14
```

# 395-Topshiriq: Smartfon batareyasi zaryadi va quvvat sarfi

## Topshiriq sharti:
Smartfon batareya quvvatini foizda hisoblovchi, ekran yoqilganda va ilova ishlaganda sarflanuvchi Battery klassini tuzing.

## Yechim (Dart kodi):
```dart
class Batareya {
  int _foiz;

  Batareya([this._foiz = 100]) {
    _foiz = _foiz.clamp(0, 100);
  }

  int get foiz => _foiz;

  void sarflash(int miqdor) {
    _foiz = (_foiz - miqdor).clamp(0, 100);
    if (_foiz <= 15 && _foiz > 0) {
      print('Ogohlantirish: Zaryad kam qoldi ($_foiz%)!');
    } else if (_foiz == 0) {
      print('Qurilma o\'chdi!');
    }
  }

  void quvvatlash(int miqdor) {
    _foiz = (_foiz + miqdor).clamp(0, 100);
    print('Zaryadlandi: $_foiz%');
  }
}

void main() {
  var bat = Batareya(30);
  bat.sarflash(20);
  bat.quvvatlash(50);
}
```

## Tushuntirish va Mantiq:
`clamp(0, 100)` qiymatni 0 va 100 oralig'idan chiqib ketmasligini kafolatlaydi.

## Ishlash natijasi:
```text
Ogohlantirish: Zaryad kam qoldi (10%)!
Zaryadlandi: 60%
```

# 396-Topshiriq: Mahsulot inventarizatsiyasi va ombor zaxirasini boshqarish

## Topshiriq sharti:
Ombor klassini yarating: mahsulotlarni qabul qilish, chiqarish va yetarli zaxirasi borligini tekshirish amallari.

## Yechim (Dart kodi):
```dart
class Ombor {
  final Map<String, int> _zaxira = {};

  void qoshish(String mahsulot, int miqdor) {
    _zaxira[mahsulot] = (_zaxira[mahsulot] ?? 0) + miqdor;
  }

  bool chiqarish(String mahsulot, int miqdor) {
    int mavjud = _zaxira[mahsulot] ?? 0;
    if (mavjud >= miqdor) {
      _zaxira[mahsulot] = mavjud - miqdor;
      return true;
    }
    return false;
  }

  void holat() {
    print('Ombor holati:');
    _zaxira.forEach((m, son) => print('- $m: $son dona'));
  }
}

void main() {
  var ombor = Ombor();
  ombor.qoshish('Noutbuk', 10);
  ombor.qoshish('Sichqoncha', 50);

  bool muvaffaqiyat = ombor.chiqarish('Noutbuk', 3);
  print('3 ta Noutbuk chiqarildi: $muvaffaqiyat');
  ombor.holat();
}
```

## Tushuntirish va Mantiq:
Ombordagi qoldiqlar Map da saqlanadi va mahsulot yetarli bo'lgandagina zaxiradan ayirib tasdiqlanadi.

## Ishlash natijasi:
```text
3 ta Noutbuk chiqarildi: true
Ombor holati:
- Noutbuk: 7 dona
- Sichqoncha: 50 dona
```

# 397-Topshiriq: Kesh xotira klassi (Oddiy Memory Cache)

## Topshiriq sharti:
Kalit-qiymat ko'rinishidagi ma'lumotlarni xotirada saqlovchi va tozalovchi MemoryCache klassini tuzing.

## Yechim (Dart kodi):
```dart
class XotiraKesh {
  final Map<String, dynamic> _kesh = {};

  void saqlash(String kalit, dynamic qiymat) {
    _kesh[kalit] = qiymat;
  }

  dynamic olish(String kalit) {
    return _kesh[kalit];
  }

  bool mavjudmi(String kalit) => _kesh.containsKey(kalit);

  void tozalash() => _kesh.clear();
}

void main() {
  var kesh = XotiraKesh();
  kesh.saqlash('user_1', {'ism': 'Farhod', 'rol': 'admin'});

  print('Mavjudmi: ${kesh.mavjudmi("user_1")}');
  print('Foydalanuvchi: ${kesh.olish("user_1")}');
  kesh.tozalash();
  print('Tozalangandan keyin: ${kesh.mavjudmi("user_1")}');
}
```

## Tushuntirish va Mantiq:
Kesh xotira tez-tez o'qiladigan ma'lumotlarni vaqtincha tezkor xotirada saqlash uchun mo'ljallangan.

## Ishlash natijasi:
```text
Mavjudmi: true
Foydalanuvchi: {ism: Farhod, rol: admin}
Tozalangandan keyin: false
```

# 398-Topshiriq: Foydalanuvchi sessiyasi klassi (Token va Yaroqlilik muddati)

## Topshiriq sharti:
Token, foydalanuvchi ID va tugash vaqtiga ega sessiya klassi va uning yaroqliligini tekshiruvchi metod yozing.

## Yechim (Dart kodi):
```dart
class Sessiya {
  final String token;
  final int userId;
  final DateTime tugashVaqti;

  Sessiya(this.token, this.userId, Duration davomiylik)
      : tugashVaqti = DateTime.now().add(davomiylik);

  bool get yaroqlimi => DateTime.now().isBefore(tugashVaqti);
}

void main() {
  var s1 = Sessiya('tok_xyz789', 42, Duration(hours: 2));
  var s2 = Sessiya('tok_expired', 10, Duration(seconds: -1));

  print('Sessiya 1 yaroqlimi: ${s1.yaroqlimi}');
  print('Sessiya 2 yaroqlimi: ${s2.yaroqlimi}');
}
```

## Tushuntirish va Mantiq:
`DateTime.now().isBefore(tugashVaqti)` tekshiruvi joriy vaqt belgilangan sessiya muddatidan o'tib ketganligini aniqlaydi.

## Ishlash natijasi:
```text
Sessiya 1 yaroqlimi: true
Sessiya 2 yaroqlimi: false
```

# 399-Topshiriq: Binar daraxt tuguni klassi (Binary TreeNode va qidiruv)

## Topshiriq sharti:
Binar daraxt tugunlari (qiymat, chap va o'ng farzand) klassini va qiymat qidirish funksiyasini yozing.

## Yechim (Dart kodi):
```dart
class DaraxtTuguni {
  int qiymat;
  DaraxtTuguni? chap;
  DaraxtTuguni? ong;

  DaraxtTuguni(this.qiymat, [this.chap, this.ong]);

  bool qidirish(int maqsad) {
    if (qiymat == maqsad) return true;
    if (maqsad < qiymat && chap != null) return chap!.qidirish(maqsad);
    if (maqsad > qiymat && ong != null) return ong!.qidirish(maqsad);
    return false;
  }
}

void main() {
  // Binar qidiruv daraxti:
  //      10
  //     /  \
  //    5    15
  var ildiz = DaraxtTuguni(10, DaraxtTuguni(5), DaraxtTuguni(15));

  print('5 qidirilmoqda: ${ildiz.qidirish(5)}');
  print('20 qidirilmoqda: ${ildiz.qidirish(20)}');
}
```

## Tushuntirish va Mantiq:
Binar daraxt rekursiv ma'lumotlar tuzilmasi bo'lib, har bir tugun o'z chap va o'ng bolalariga havola saqlaydi.

## Ishlash natijasi:
```text
5 qidirilmoqda: true
20 qidirilmoqda: false
```

# 400-Topshiriq: AI neyron modeli klassi (Vaznlar, bias va aktivatsiya)

## Topshiriq sharti:
Kirish vektorini vaznlar bilan ko'paytirib, bias qo'shib ReLU aktivatsiya funksiyasidan o'tkazuvchi Neyron klassini tuzing.

## Yechim (Dart kodi):
```dart
class Neyron {
  final List<double> vaznlar;
  final double bias;

  Neyron(this.vaznlar, this.bias);

  double relu(double x) => x > 0 ? x : 0.0;

  double hisobla(List<double> kirish) {
    if (kirish.length != vaznlar.length) {
      throw ArgumentError('Kirish va vaznlar o\'lchami teng bo\'lishi kerak');
    }

    double z = bias;
    for (int i = 0; i < kirish.length; i++) {
      z += kirish[i] * vaznlar[i];
    }
    return relu(z);
  }
}

void main() {
  var neyron = Neyron([0.5, -0.8, 1.2], -0.2);
  List<double> kirish = [1.0, 0.5, 0.5];

  // z = -0.2 + (1.0*0.5) + (0.5*-0.8) + (0.5*1.2) = -0.2 + 0.5 - 0.4 + 0.6 = 0.5
  double natija = neyron.hisobla(kirish);
  print('Neyron chiqishi: ${natija.toStringAsFixed(2)}');
}
```

## Tushuntirish va Mantiq:
Neyron $z = \sum (w_i \cdot x_i) + b$ formulasi bo'yicha chiziqli kombinatsiyani hisoblab, so'ng ReLU aktivatsiyasini qo'llaydi.

## Ishlash natijasi:
```text
Neyron chiqishi: 0.50
```

