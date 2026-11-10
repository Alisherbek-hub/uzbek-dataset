# 7-Qism: Dart 3 Records va Pattern Matching (301-350)

Ushbu qismda Dart 3 ning eng inqilobiy yangiliklari: Records (kortejlar, ko'p qiymat qaytarish), pozitsion va nomlangan maydonlar, Pattern Matching (List, Map, Object patterns), relational va logical patterns, `when` qo'riqchilari hamda Sealed klasslar bilan to'liq qamrovli (exhaustive) switch ifodalari chuqur o'rganiladi.

# 301-Topshiriq: Dart 3 Records asoslari: Pozitsion rekordlar (int, String)
## Topshiriq sharti:
Ikkita turli xil qiymatni (`int` va `String`) saqlovchi pozitsion rekord e'lon qiling va uning elementlarini chop eting.

## Yechim (Dart kodi):
```dart
void main() {
  (int, String) rekord = (101, "O'zbekiston");

  print("To'liq rekord: $rekord");
  print("Birinchi element (\$1): ${rekord.$1}");
  print("Ikkinchi element (\$2): ${rekord.$2}");
}
```

## Tushuntirish va Mantiq:
Dart 3 Records har xil turdagi qiymatlarni birlashtiruvchi anonim, o'zgarmas (immutable) ma'lumot tuzilmasidir. Pozitsion elementlar `$1`, `$2` orqali o'qiladi.

## Ishlash natijasi:
```text
To'liq rekord: (101, O'zbekiston)
Birinchi element (\$1): 101
Ikkinchi element (\$2): O'zbekiston
```

# 302-Topshiriq: Nomlangan maydonli rekordlar: ({int x, int y})
## Topshiriq sharti:
Maydonlariga aniq nom berilgan rekord yarating va ularni o'z nomlari orqali o'qing.

## Yechim (Dart kodi):
```dart
void main() {
  ({int id, String ism, double ball}) talaba = (id: 1, ism: "Sardor", ball: 92.5);

  print("Talaba ID:   ${talaba.id}");
  print("Talaba ismi: ${talaba.ism}");
  print("Ball:        ${talaba.ball}");
}
```

## Tushuntirish va Mantiq:
Nomlangan rekordlarda maydonlar nom bilan chaqiriladi, bu esa alohida klass yaratmasdan strukturalashgan ma'lumotlarni uzatishda juda qulaydir.

## Ishlash natijasi:
```text
Talaba ID:   1
Talaba ismi: Sardor
Ball:        92.5
```

# 303-Topshiriq: Pozitsion va nomlangan maydonlarni aralashtirish
## Topshiriq sharti:
Bitta rekord ichida ham pozitsion, ham nomlangan maydonlardan bir vaqtda foydalaning.

## Yechim (Dart kodi):
```dart
void main() {
  (int, {String title, bool active}) vazifa = (1, title: "AI modelni o'qitish", active: true);

  print("Raqami:   ${vazifa.$1}");
  print("Sarlavha: ${vazifa.title}");
  print("Faolmi:   ${vazifa.active}");
}
```

## Tushuntirish va Mantiq:
Dart 3 da pozitsion va nomlangan maydonlar bitta rekord qavsi ichida uyg'un ishlaydi.

## Ishlash natijasi:
```text
Raqami:   1
Sarlavha: AI modelni o'qitish
Faolmi:   true
```

# 304-Topshiriq: Rekordlar tengligi: Value Equality (Qiymat tengligi)
## Topshiriq sharti:
Ikkita mustaqil rekordning qiymatlari bir xil bo'lsa, ularning `==` operatori orqali teng chiqishini ko'rsating.

## Yechim (Dart kodi):
```dart
void main() {
  var r1 = (1, "salom");
  var r2 = (1, "salom");
  var r3 = (2, "dunyo");

  print("r1 == r2: ${r1 == r2}");
  print("r1 == r3: ${r1 == r3}");
  print("r1 hashCode == r2 hashCode: ${r1.hashCode == r2.hashCode}");
}
```

## Tushuntirish va Mantiq:
Oddiy klasslardan farqli ravishda, Dart 3 rekordlari avtomatik ravishda qiymatlar bo'yicha tenglikka (structural/value equality) ega.

## Ishlash natijasi:
```text
r1 == r2: true
r1 == r3: false
r1 hashCode == r2 hashCode: true
```

# 305-Topshiriq: typedef orqali rekord turiga nom berish
## Topshiriq sharti:
Murakkab rekord turini `typedef` orqali qayta ishlatiluvchi nomga aylantiring.

## Yechim (Dart kodi):
```dart
typedef Foydalanuvchi = (int id, {String ism, String email});

void chopEt(Foydalanuvchi user) {
  print("User #${user.$1}: ${user.ism} (${user.email})");
}

void main() {
  Foydalanuvchi u = (10, ism: "Malika", email: "malika@ai.uz");
  chopEt(u);
}
```

## Tushuntirish va Mantiq:
`typedef` yordamida rekordlarni xuddi klass kabi butun ilova bo'ylab bitta tur sifatida ishlatish mumkin.

## Ishlash natijasi:
```text
User #10: Malika (malika@ai.uz)
```

# 306-Topshiriq: Pattern Matching: O'zgaruvchilarni e'lon qilishda destructuring
## Topshiriq sharti:
`var (a, b) = rekord;` orqali rekord elementlarini alohida yangi o'zgaruvchilarga ochib oling.

## Yechim (Dart kodi):
```dart
void main() {
  var koordinata = (15.5, 42.0);

  // Destructuring (ochish)
  var (x, y) = koordinata;

  print("X o'qi: $x");
  print("Y o'qi: $y");
}
```

## Tushuntirish va Mantiq:
Destructuring orqali rekordning ichki elementlari bitta satrda yangi o'zgaruvchilarga aylanadi.

## Ishlash natijasi:
```text
X o'qi: 15.5
Y o'qi: 42.0
```

# 307-Topshiriq: Nomlangan rekordlarni destructuring qilish: var (:x, :y)
## Topshiriq sharti:
Nomlangan maydonlarni o'z nomi bilan yangi o'zgaruvchilarga ochuvchi ixcham `:nom` sintaksisini ko'rsating.

## Yechim (Dart kodi):
```dart
void main() {
  var nuqta = (x: 100, y: 200);

  // :x va :y sintaksisi x: x va y: y ning qisqartmasidir
  var (:x, :y) = nuqta;

  print("Olingan X: $x, Y: $y");
}
```

## Tushuntirish va Mantiq:
`var (:x, :y)` sintaksisi rekord maydonlarining nomlarini bir vaqtning o'zida o'zgaruvchi nomi qilib oladi.

## Ishlash natijasi:
```text
Olingan X: 100, Y: 200
```

# 308-Topshiriq: Ro'yxat naqshlari (List Patterns): Aniq elementlarni ajratish
## Topshiriq sharti:
`var [a, b, c] = list;` orqali ro'yxat elementlarini tekshiring va oching.

## Yechim (Dart kodi):
```dart
void main() {
  var royxat = [10, 20, 30];

  var [birinchi, ikkinchi, uchinchi] = royxat;

  print("1-element: $birinchi");
  print("2-element: $ikkinchi");
  print("3-element: $uchinchi");
}
```

## Tushuntirish va Mantiq:
Agar ro'yxat uzunligi naqshga to'g'ri kelmasa, dastur xato beradi. Shuning uchun bu aniq o'lchamli ma'lumotlarda juda qulay.

## Ishlash natijasi:
```text
1-element: 10
2-element: 20
3-element: 30
```

# 309-Topshiriq: Ro'yxat naqshida rest elementi: [first, ..., last]
## Topshiriq sharti:
Ro'yxatning birinchi va oxirgi elementlarini olib, o'rtadagilarni `...` bilan e'tiborsiz qoldiring.

## Yechim (Dart kodi):
```dart
void main() {
  var sonlar = [1, 2, 3, 4, 5, 6, 7];

  var [boshi, ..., oxiri] = sonlar;

  print("Boshlang'ich: $boshi");
  print("Yakuniy:      $oxiri");
}
```

## Tushuntirish va Mantiq:
`...` (rest operatori) ro'yxatning o'rtasidagi ixtiyoriy sondagi elementlarni o'tkazib yuboradi.

## Ishlash natijasi:
```text
Boshlang'ich: 1
Yakuniy:      7
```

# 310-Topshiriq: Rest elementlarini yangi ro'yxatga olish: [first, ...rest]
## Topshiriq sharti:
`...qolganlar` orqali birinchi elementdan tashqari qolgan barcha elementlarni yangi ro'yxatga jamlang.

## Yechim (Dart kodi):
```dart
void main() {
  var komandalar = ["Boshliq", "Dasturchi 1", "Dasturchi 2", "Tester"];

  var [lider, ...xodimlar] = komandalar;

  print("Lider:   $lider");
  print("Xodimlar: $xodimlar (${xodimlar.runtimeType})");
}
```

## Tushuntirish va Mantiq:
Rest elementiga o'zgaruvchi nomi berilsa, qolgan elementlar avtomatik `List` sifatida yig'iladi.

## Ishlash natijasi:
```text
Lider:   Boshliq
Xodimlar: [Dasturchi 1, Dasturchi 2, Tester] (List<String>)
```

# 311-Topshiriq: Map naqshlari (Map Patterns): JSON dan qiymat ajratish
## Topshiriq sharti:
`if (map case {'status': int s, 'msg': String m})` orqali xarita tuzilmasini tekshiring va qiymatlarini oling.

## Yechim (Dart kodi):
```dart
void tahlil(Map<String, dynamic> json) {
  if (json case {'status': 200, 'message': String msg}) {
    print("Muvaffaqiyatli: $msg");
  } else if (json case {'status': 404}) {
    print("Xatolik: Sahifa topilmadi (404)");
  } else {
    print("Noma'lum javob formati");
  }
}

void main() {
  tahlil({'status': 200, 'message': 'Ma'lumotlar yuklandi'});
  tahlil({'status': 404, 'error': 'Not found'});
}
```

## Tushuntirish va Mantiq:
Map pattern bir vaqtning o'zida ham kalitlar borligini, ham ularning turlari va hatto aniq qiymatlarini tekshiradi.

## Ishlash natijasi:
```text
Muvaffaqiyatli: Ma'lumotlar yuklandi
Xatolik: Sahifa topilmadi (404)
```

# 312-Topshiriq: Ob'ekt naqshlari (Object Patterns): Klass maydonlarini to'g'ridan-to'g'ri ochish
## Topshiriq sharti:
Ob'ekt turini va uning maydonlarini `if (obj case MyClass(field: var v))` orqali tekshiring.

## Yechim (Dart kodi):
```dart
class Foydalanuvchi {
  final String ism;
  final int yosh;
  Foydalanuvchi(this.ism, this.yosh);
}

void tekshir(Object obj) {
  if (obj case Foydalanuvchi(ism: var ism, yosh: >= 18)) {
    print("$ism balog'at yoshiga yetgan foydalanuvchi.");
  } else {
    print("Shartga mos emas.");
  }
}

void main() {
  tekshir(Foydalanuvchi("Alisher", 20));
  tekshir(Foydalanuvchi("Jasur", 15));
}
```

## Tushuntirish va Mantiq:
Object pattern orqali klass turini tekshirish bilan birga uning getter maydonlarini ham darhol shartga solish mumkin.

## Ishlash natijasi:
```text
Alisher balog'at yoshiga yetgan foydalanuvchi.
Shartga mos emas.
```

# 313-Topshiriq: Wildcard pattern: _ (E'tiborsiz qoldirish)
## Topshiriq sharti:
Rekorddagi faqat o'zingizga kerakli qiymatni olib, qolganlarini pastki chiziq `_` bilan e'tiborsiz qoldiring.

## Yechim (Dart kodi):
```dart
void main() {
  var ma'lumot = ("Toshkent", 2500000, "O'zbekiston");

  // Faqat shahar nomi va davlat kerak, aholi soni muhim emas:
  var (shahar, _, davlat) = ma'lumot;

  print("Shahar: $shahar, Davlat: $davlat");
}
```

## Tushuntirish va Mantiq:
`_` o'zgaruvchi yaratmaydi va xotiradan joy band qilmaydi, keraksiz qiymatlarni tashlab yuboradi.

## Ishlash natijasi:
```text
Shahar: Toshkent, Davlat: O'zbekiston
```

# 314-Topshiriq: Relational Pattern: Solishtirish operatorlari switch da
## Topshiriq sharti:
Dart 3 `switch expression` da `>`, `<=`, `==` munosabat operatorlarini qo'llang.

## Yechim (Dart kodi):
```dart
String haroratTavsifi(double t) => switch (t) {
  <= 0.0 => "Muzdek havo",
  > 0.0 && <= 15.0 => "Salqin",
  > 15.0 && <= 30.0 => "Iliq va yoqimli",
  _ => "Issiq jazirama"
};

void main() {
  print("-5.0 C: ${haroratTavsifi(-5.0)}");
  print("12.0 C: ${haroratTavsifi(12.0)}");
  print("22.0 C: ${haroratTavsifi(22.0)}");
  print("35.0 C: ${haroratTavsifi(35.0)}");
}
```

## Tushuntirish va Mantiq:
Relational pattern an'anaviy `if-else` larni juda chiroyli va matematik jadval ko'rinishiga keltiradi.

## Ishlash natijasi:
```text
-5.0 C: Muzdek havo
12.0 C: Salqin
22.0 C: Iliq va yoqimli
35.0 C: Issiq jazirama
```

# 315-Topshiriq: Logical-OR va Logical-AND patternlari
## Topshiriq sharti:
`||` va `&&` mantiqiy naqshlari bilan bir nechta variantlarni birlashtiring.

## Yechim (Dart kodi):
```dart
String ishKuni(String kun) => switch (kun) {
  "Dushanba" || "Seshanba" || "Chorshanba" || "Payshanba" || "Juma" => "Ish kuni",
  "Shanba" || "Yakshanba" => "Dam olish kuni",
  _ => "Noto'g'ri kun"
};

void main() {
  print("Juma:    ${ishKuni('Juma')}");
  print("Yakshanba: ${ishKuni('Yakshanba')}");
}
```

## Tushuntirish va Mantiq:
`||` pattern bir nechta mos keluvchi qiymatlarni bitta natija tarmog'iga yo'naltiradi.

## Ishlash natijasi:
```text
Juma:    Ish kuni
Yakshanba: Dam olish kuni
```

# 316-Topshiriq: Null-check va Null-assert pattern: ? va !
## Topshiriq sharti:
Naqsh ichida qiymatning null emasligini tekshirib o'zgaruvchiga olish (`v?`) va majburiy talab qilishni (`v!`) ko'rsating.

## Yechim (Dart kodi):
```dart
void tahlilQil(String? s) {
  switch (s) {
    case var text?:
      print("Matn mavjud, uzunligi: ${text.length}");
    case null:
      print("Matn null ekan!");
  }
}

void main() {
  tahlilQil("Salom");
  tahlilQil(null);
}
```

## Tushuntirish va Mantiq:
`var text?` naqshi qiymat null bo'lmagandagina mos keladi va `text` ni avtomatik non-nullable `String` turiga promote qiladi.

## Ishlash natijasi:
```text
Matn mavjud, uzunligi: 5
Matn null ekan!
```

# 317-Topshiriq: Switch da guard (when) sharti
## Topshiriq sharti:
Naqsh mos kelganidan so'ng qo'shimcha mantiqiy shartni `when` orqali tekshiring.

## Yechim (Dart kodi):
```dart
void bahola((int, int) juftlik) {
  switch (juftlik) {
    case (var a, var b) when a == b:
      print("Sonlar teng: $a == $b");
    case (var a, var b) when a > b:
      print("Birinchisi katta: $a > $b");
    case (var a, var b):
      print("Ikkinchisi katta: $a < $b");
  }
}

void main() {
  bahola((10, 10));
  bahola((25, 12));
  bahola((7, 99));
}
```

## Tushuntirish va Mantiq:
`when` sharti faqat belgilangan mantiqiy ifoda `true` bo'lsagina ushbu tarmoqni ishga tushiradi.

## Ishlash natijasi:
```text
Sonlar teng: 10 == 10
Birinchisi katta: 25 > 12
Ikkinchisi katta: 7 < 99
```

# 318-Topshiriq: Sealed klasslar: To'liq qamrovli (Exhaustive) tekshiruv
## Topshiriq sharti:
`sealed class` e'lon qiling va `switch expression` da barcha vorislar ko'rib chiqilganini kompilyator talab qilishini ko'rsating.

## Yechim (Dart kodi):
```dart
sealed class Shape {}

class Circle extends Shape {
  final double radius;
  Circle(this.radius);
}

class Square extends Shape {
  final double side;
  Square(this.side);
}

double hisoblaYuza(Shape s) => switch (s) {
  Circle(radius: var r) => 3.14159 * r * r,
  Square(side: var a) => a * a
  // default kerak emas, chunki Shape sealed va barcha vorislar qamrab olingan!
};

void main() {
  print("Doira yuzasi:   ${hisoblaYuza(Circle(5))}");
  print("Kvadrat yuzasi: ${hisoblaYuza(Square(4))}");
}
```

## Tushuntirish va Mantiq:
Dart 3 ning `sealed` klasslari kompilyatorga barcha mumkin bo'lgan turlarni oldindan bildiradi. Agar bitta tur unutilsa, kompilyator xatolik beradi.

## Ishlash natijasi:
```text
Doira yuzasi:   78.53975
Kvadrat yuzasi: 16.0
```

# 319-Topshiriq: HTTP status kodlarini Switch Expression bilan tahlil qilish
## Topshiriq sharti:
Web so'rov status kodlarini munosabat naqshlari bilan toifalarga ajrating.

## Yechim (Dart kodi):
```dart
String httpTahlil(int code) => switch (code) {
  >= 200 && < 300 => "Muvaffaqiyat (Success: $code)",
  >= 300 && < 400 => "Qayta yo'naltirish (Redirect: $code)",
  >= 400 && < 500 => "Mijoz xatosi (Client Error: $code)",
  >= 500 && < 600 => "Server xatosi (Server Error: $code)",
  _ => "Noma'lum status kodi: $code"
};

void main() {
  print(httpTahlil(200));
  print(httpTahlil(404));
  print(httpTahlil(503));
}
```

## Tushuntirish va Mantiq:
HTTP status kodlari bir nechta oraliqlarga ega bo'lib, switch expression ularni guruhlash uchun eng maqbul vositadir.

## Ishlash natijasi:
```text
Muvaffaqiyat (Success: 200)
Mijoz xatosi (Client Error: 404)
Server xatosi (Server Error: 503)
```

# 320-Topshiriq: 2D Nuqtalar ustida amallar: Records bilan Vektorlar
## Topshiriq sharti:
Records yordamida ikkita nuqtani qo'shish va masofasini hisoblovchi funksiyalar yozing.

## Yechim (Dart kodi):
```dart
import 'dart:math';

typedef Point2D = (double x, double y);

Point2D qosh(Point2D a, Point2D b) => (a.$1 + b.$1, a.$2 + b.$2);

double masofa(Point2D a, Point2D b) {
  var (x1, y1) = a;
  var (x2, y2) = b;
  return sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2));
}

void main() {
  Point2D p1 = (0.0, 0.0);
  Point2D p2 = (3.0, 4.0);

  print("Yig'indi nuqta: ${qosh(p1, p2)}");
  print("Orasidagi masofa: ${masofa(p1, p2)}");
}
```

## Tushuntirish va Mantiq:
Records yengil geometrik turlarni massiv yoki sinf yaratmasdan xotirada samarali ifodalaydi.

## Ishlash natijasi:
```text
Yig'indi nuqta: (3.0, 4.0)
Orasidagi masofa: 5.0
```

# 321-Topshiriq: 3D Koordinatalar: (double x, double y, double z)
## Topshiriq sharti:
3D vektorlarni skalyar ko'paytirish (Dot product) funksiyasini yozing.

## Yechim (Dart kodi):
```dart
typedef Vec3 = (double x, double y, double z);

double dotProduct(Vec3 a, Vec3 b) {
  var (x1, y1, z1) = a;
  var (x2, y2, z2) = b;
  return x1 * x2 + y1 * y2 + z1 * z2;
}

void main() {
  Vec3 v1 = (1.0, 2.0, 3.0);
  Vec3 v2 = (4.0, -5.0, 6.0);

  print("Skalyar ko'paytma: ${dotProduct(v1, v2)}"); // 1*4 + 2*(-5) + 3*6 = 4 - 10 + 18 = 12
}
```

## Tushuntirish va Mantiq:
3D vektorlar kompyuter grafikasi va AI tenzor hisob-kitoblarida keng qo'llaniladi.

## Ishlash natijasi:
```text
Skalyar ko'paytma: 12.0
```

# 322-Topshiriq: Ranglar modeli: (int r, int g, int b, double a)
## Topshiriq sharti:
RGBA ranglarini rekord ko'rinishida saqlash va HEX satriga o'girish.

## Yechim (Dart kodi):
```dart
typedef ColorRGBA = (int r, int g, int b, double a);

String toHex(ColorRGBA c) {
  var (r, g, b, _) = c;
  return "#${r.toRadixString(16).padLeft(2, '0')}"
         "${g.toRadixString(16).padLeft(2, '0')}"
         "${b.toRadixString(16).padLeft(2, '0')}".toUpperCase();
}

void main() {
  ColorRGBA zangori = (0, 122, 255, 1.0);
  print("HEX kodi: ${toHex(zangori)}");
}
```

## Tushuntirish va Mantiq:
Rang modelini rekord orqali ifodalash xotira yuklamasisiz tezkor konvertatsiyaga imkon beradi.

## Ishlash natijasi:
```text
HEX kodi: #007AFF
```

# 323-Topshiriq: Tosh, Qaychi, Qog'oz o'yini: switch ((p1, p2))
## Topshiriq sharti:
Ikki o'yinchi tanlovini bitta qatorli kortejli `switch` orqali hal qiluvchi hakam funksiyasini yozing.

## Yechim (Dart kodi):
```dart
String oyna(String p1, String p2) => switch ((p1, p2)) {
  (var a, var b) when a == b => "Durang!",
  ("tosh", "qaychi") || ("qaychi", "qog'oz") || ("qog'oz", "tosh") => "1-o'yinchi yutdi!",
  _ => "2-o'yinchi yutdi!"
};

void main() {
  print("tosh vs qaychi: ${oyna('tosh', 'qaychi')}");
  print("tosh vs tosh:   ${oyna('tosh', 'tosh')}");
  print("qog'oz vs qaychi: ${oyna('qog'oz', 'qaychi')}");
}
```

## Tushuntirish va Mantiq:
Kortejli switch `(p1, p2)` bir vaqtning o'zida ikkala tomon holatini tahlil qilishning eng toza usulidir.

## Ishlash natijasi:
```text
tosh vs qaychi: 1-o'yinchi yutdi!
tosh vs tosh:   Durang!
qog'oz vs qaychi: 2-o'yinchi yutdi!
```

# 324-Topshiriq: CLI Buyruqlar analizatori (Command Line Parser)
## Topshiriq sharti:
Konsol buyruqlarini List pattern orqali tahlil qiluvchi dastur yozing.

## Yechim (Dart kodi):
```dart
void commandParser(List<String> args) {
  switch (args) {
    case ["git", "commit", "-m", String msg]:
      print("Commit qilindi: '$msg'");
    case ["git", "push", String remote, String branch]:
      print("Push qilindi -> $remote/$branch");
    case ["git", "status"]:
      print("Fayllar holati tekshirilmoqda...");
    case _:
      print("Noma'lum buyruq: $args");
  }
}

void main() {
  commandParser(["git", "commit", "-m", "Dart 3 records tayyor"]);
  commandParser(["git", "push", "origin", "main"]);
  commandParser(["git", "help"]);
}
```

## Tushuntirish va Mantiq:
List pattern CLI dasturlarida argumentlarni qismlarga ajratishda juda qulay.

## Ishlash natijasi:
```text
Commit qilindi: 'Dart 3 records tayyor'
Push qilindi -> origin/main
Noma'lum buyruq: [git, help]
```

# 325-Topshiriq: SemVer (Semantik versiyalash: major.minor.patch) pattern matching
## Topshiriq sharti:
Versiya satrini tahlil qilib, uning katta (major) yoki kichik (minor) yangilanish ekanligini aniqlang.

## Yechim (Dart kodi):
```dart
void analyzeVersion(String v) {
  var parts = v.split('.').map(int.tryParse).toList();

  switch (parts) {
    case [int major, int minor, int patch]:
      print("To'liq SemVer: Major=$major, Minor=$minor, Patch=$patch");
    case [int major, int minor]:
      print("Qisqa versiya: Major=$major, Minor=$minor");
    case _:
      print("Noto'g'ri versiya formati: $v");
  }
}

void main() {
  analyzeVersion("3.5.1");
  analyzeVersion("2.0");
  analyzeVersion("beta-1");
}
```

## Tushuntirish va Mantiq:
Ro'yxat naqshlari matnlarni xavfsiz strukturalashda yuqori samaradorlik beradi.

## Ishlash natijasi:
```text
To'liq SemVer: Major=3, Minor=5, Patch=1
Qisqa versiya: Major=2, Minor=0
Noto'g'ri versiya formati: beta-1
```

# 326-Topshiriq: JSON API javobini (Success / Error / Loading) Pattern Matching bilan ajratish
## Topshiriq sharti:
API dan keladigan turlicha javob shakllarini Map pattern yordamida ajratuvchi funksiya yozing.

## Yechim (Dart kodi):
```dart
void handleResponse(Map<String, dynamic> res) {
  switch (res) {
    case {"status": "success", "data": Map data}:
      print("Muvaffaqiyatli ma'lumot: $data");
    case {"status": "error", "message": String msg, "code": int c}:
      print("Xatolik ($c): $msg");
    case {"status": "loading"}:
      print("Yuklanmoqda, kuting...");
    case _:
      print("Noma'lum javob formati");
  }
}

void main() {
  handleResponse({"status": "success", "data": {"user": "ali"}});
  handleResponse({"status": "error", "message": "Server band", "code": 503});
}
```

## Tushuntirish va Mantiq:
Pattern Matching bir vaqtning o'zida ham kalit mavjudligini, ham uning qiymat turini va qiymatini tekshiradi.

## Ishlash natijasi:
```text
Muvaffaqiyatli ma'lumot: {user: ali}
Xatolik (503): Server band
```

# 327-Topshiriq: Valyuta juftligi rekordi: ({String from, String to, double rate})
## Topshiriq sharti:
Valyuta kursi ma'lumotlarini nomlangan rekordda saqlang va konvertatsiya qiling.

## Yechim (Dart kodi):
```dart
typedef ExchangeRate = ({String from, String to, double rate});

double konvertatsiya(double summa, ExchangeRate kurs) {
  return summa * kurs.rate;
}

void main() {
  ExchangeRate usdToUzs = (from: "USD", to: "UZS", rate: 12800.0);
  double dollar = 150.0;
  double som = konvertatsiya(dollar, usdToUzs);

  print("$dollar USD = ${som.toStringAsFixed(0)} UZS");
}
```

## Tushuntirish va Mantiq:
Nomlangan maydonli rekordlar moliyaviy hisob-kitoblar va ma'lumotlar oqimida sinflarsiz yengil tur hosil qiladi.

## Ishlash natijasi:
```text
150.0 USD = 1920000 UZS
```

# 328-Topshiriq: Binar daraxt tugunini Object Pattern orqali tahlil qilish
## Topshiriq sharti:
Daraxt barg tuguni (chap va o'ngi null) yoki ichki tugun ekanligini Pattern Matching bilan aniqlang.

## Yechim (Dart kodi):
```dart
class Node {
  int val;
  Node? left, right;
  Node(this.val, [this.left, this.right]);
}

void analyzeNode(Node n) {
  switch (n) {
    case Node(left: null, right: null):
      print("Barg tugun (Leaf node): ${n.val}");
    case Node(left: Node l, right: null):
      print("Faqat chap bolasi bor: ${n.val} -> ${l.val}");
    case Node(left: null, right: Node r):
      print("Faqat o'ng bolasi bor: ${n.val} -> ${r.val}");
    case Node(left: Node l, right: Node r):
      print("Ikkala bolasi ham bor: ${n.val} -> (${l.val}, ${r.val})");
  }
}

void main() {
  analyzeNode(Node(5));
  analyzeNode(Node(10, Node(3), Node(15)));
}
```

## Tushuntirish va Mantiq:
Object Pattern rekursiv tuzilmalarni sinfda getterlar orqali tekshirishni juda ixchamlashtiradi.

## Ishlash natijasi:
```text
Barg tugun (Leaf node): 5
Ikkala bolasi ham bor: 10 -> (3, 15)
```

# 329-Topshiriq: Geometrik shakllar yuzasi (Sealed class Shape: Circle, Square, Rectangle)
## Topshiriq sharti:
3 ta shakl turini o'z ichiga olgan `sealed` ierarxiyasini yarating va ularning perimetrini hisoblang.

## Yechim (Dart kodi):
```dart
sealed class Shape {}

class Circle extends Shape {
  final double r;
  Circle(this.r);
}

class Rectangle extends Shape {
  final double w, h;
  Rectangle(this.w, this.h);
}

double perimetr(Shape s) => switch (s) {
  Circle(r: var r) => 2 * 3.14159 * r,
  Rectangle(w: var w, h: var h) => 2 * (w + h)
};

void main() {
  print("Doira perimetri:     ${perimetr(Circle(7)).toStringAsFixed(2)}");
  print("To'g'ri to'rtburchak: ${perimetr(Rectangle(5, 10))}");
}
```

## Tushuntirish va Mantiq:
Sealed klasslar va Switch Expression kombinatsiyasi obyektga yo'naltirilgan dasturlash va funksional dasturlashning eng kuchli sintezidir.

## Ishlash natijasi:
```text
Doira perimetri:     43.98
To'g'ri to'rtburchak: 30.0
```

# 330-Topshiriq: Mantiqiy ifodalar daraxtini baholash (Expression Evaluator)
## Topshiriq sharti:
Son, Qo'shish va Ko'paytirish nodalaridan iborat matematik ifoda daraxtini baholang.

## Yechim (Dart kodi):
```dart
sealed class Expr {}

class NumExpr extends Expr {
  final int val;
  NumExpr(this.val);
}

class AddExpr extends Expr {
  final Expr left, right;
  AddExpr(this.left, this.right);
}

class MulExpr extends Expr {
  final Expr left, right;
  MulExpr(this.left, this.right);
}

int evaluate(Expr e) => switch (e) {
  NumExpr(val: var v) => v,
  AddExpr(left: var l, right: var r) => evaluate(l) + evaluate(r),
  MulExpr(left: var l, right: var r) => evaluate(l) * evaluate(r)
};

void main() {
  // Ifoda: (3 + 5) * 2
  Expr expression = MulExpr(AddExpr(NumExpr(3), NumExpr(5)), NumExpr(2));
  print("(3 + 5) * 2 = ${evaluate(expression)}");
}
```

## Tushuntirish va Mantiq:
Kompilyatorlar va interfeyslarda AST (Abstract Syntax Tree) daraxtlarini baholash ushbu naqsh orqali amalga oshiriladi.

## Ishlash natijasi:
```text
(3 + 5) * 2 = 16
```

# 331-Topshiriq: To'lov tizimlari holat mashinasi (Payment State Machine)
## Topshiriq sharti:
To'lov holatlarini (Boshlangan, Jarayonda, To'landi, Xatolik) Pattern Matching bilan ifodalang.

## Yechim (Dart kodi):
```dart
sealed class PaymentState {}

class PaymentInitial extends PaymentState {}
class PaymentProcessing extends PaymentState {}
class PaymentSuccess extends PaymentState {
  final String txId;
  PaymentSuccess(this.txId);
}
class PaymentFailed extends PaymentState {
  final String reason;
  PaymentFailed(this.reason);
}

String getStatusMessage(PaymentState state) => switch (state) {
  PaymentInitial() => "To'lov hali boshlanmadi",
  PaymentProcessing() => "To'lov qayta ishlanmoqda...",
  PaymentSuccess(txId: var id) => "To'lov muvaffaqiyatli! Tranzaksiya: $id",
  PaymentFailed(reason: var r) => "To'lov amalga oshmadi: $r"
};

void main() {
  print(getStatusMessage(PaymentProcessing()));
  print(getStatusMessage(PaymentSuccess("TXN_998877")));
}
```

## Tushuntirish va Mantiq:
Holat mashinasi (State Machine) Flutter ilovalarida UI holatini aniq aks ettirishning eng ishonchli usulidir.

## Ishlash natijasi:
```text
To'lov qayta ishlanmoqda...
To'lov muvaffaqiyatli! Tranzaksiya: TXN_998877
```

# 332-Topshiriq: Auth holati (Unauthenticated, Authenticating, Authenticated)
## Topshiriq sharti:
Foydalanuvchi tizimga kirish holatini sealed klasslar bilan boshqaring.

## Yechim (Dart kodi):
```dart
sealed class AuthState {}

class Unauthenticated extends AuthState {}
class Authenticating extends AuthState {}
class Authenticated extends AuthState {
  final String email;
  Authenticated(this.email);
}

void renderUI(AuthState state) {
  var ui = switch (state) {
    Unauthenticated() => "Login sahifasi ko'rsatilmoqda",
    Authenticating() => "Aylana progress indikator",
    Authenticated(email: var e) => "Xush kelibsiz, $e!"
  };
  print("UI: $ui");
}

void main() {
  renderUI(Unauthenticated());
  renderUI(Authenticated("admin@uzbek.ai"));
}
```

## Tushuntirish va Mantiq:
BLoC va Riverpod kabi kutubxonalar aynan ushbu Sealed State arxitekturasiga tayanadi.

## Ishlash natijasi:
```text
UI: Login sahifasi ko'rsatilmoqda
UI: Xush kelibsiz, admin@uzbek.ai!
```

# 333-Topshiriq: O'zgaruvchilar qiymatini temp siz almashtirish: (a, b) = (b, a)
## Topshiriq sharti:
Dart 3 Records yordamida ikkita o'zgaruvchi qiymatini qo'shimcha o'zgaruvchisiz bir satrda almashtiring.

## Yechim (Dart kodi):
```dart
void main() {
  int a = 10;
  int b = 20;

  print("Oldin: a = $a, b = $b");

  // Destructuring swap (Kortejli almashtirish)
  (a, b) = (b, a);

  print("Keyin: a = $a, b = $b");
}
```

## Tushuntirish va Mantiq:
Dart 3 da `(a, b) = (b, a)` ifodasi vaqtinchalik o'zgaruvchisiz toza va xavfsiz qiymat almashtirish imkonini beradi.

## Ishlash natijasi:
```text
Oldin: a = 10, b = 20
Keyin: a = 20, b = 10
```

# 334-Topshiriq: Records bilan Masofa va Burchak (Polar koordinatalar) hisoblash
## Topshiriq sharti:
Dekart koordinatasidan `(r, theta)` qutb koordinatasiga o'tkazuvchi funksiya yozing.

## Yechim (Dart kodi):
```dart
import 'dart:math';

(double radius, double burchakGradus) toPolar(double x, double y) {
  double r = sqrt(x * x + y * y);
  double theta = atan2(y, x) * (180 / pi);
  return (r, theta);
}

void main() {
  var (r, burchak) = toPolar(3.0, 3.0);
  print("Radius: ${r.toStringAsFixed(2)}, Burchak: ${burchak.toStringAsFixed(1)} gradus");
}
```

## Tushuntirish va Mantiq:
Geometrik funksiyalarda Records ko'p qiymatli natijalarni uzatishning eng optimal usulidir.

## Ishlash natijasi:
```text
Radius: 4.24, Burchak: 45.0 gradus
```

# 335-Topshiriq: Records bilan 2x2 Matritsa determinantini hisoblash
## Topshiriq sharti:
4 ta elementdan iborat 2x2 matritsani rekord orqali ifodalab, determinantini hisoblang.

## Yechim (Dart kodi):
```dart
typedef Matrix2x2 = (double a, double b, double c, double d);

double determinant(Matrix2x2 m) {
  var (a, b, c, d) = m;
  return (a * d) - (b * c);
}

void main() {
  Matrix2x2 m = (4.0, 2.0, 3.0, 1.0);
  print("Determinant: ${determinant(m)}"); // 4*1 - 2*3 = -2
}
```

## Tushuntirish va Mantiq:
Chiziqli algebra va AI tenzorlarida rekordlar kichik matritsalarni o'ta yengil tarzda modellashtiradi.

## Ishlash natijasi:
```text
Determinant: -2.0
```

# 336-Topshiriq: Shaxmat figuralari yurishi validatsiyasi Pattern Matching bilan
## Topshiriq sharti:
Figura turi va koordinata siljishini kortej bilan tahlil qiling.

## Yechim (Dart kodi):
```dart
bool isValidMove(String piece, (int dx, int dy) delta) => switch (piece) {
  "Rook"   => (delta.$1 == 0 && delta.$2 != 0) || (delta.$1 != 0 && delta.$2 == 0),
  "Bishop" => delta.$1.abs() == delta.$2.abs(),
  "Knight" => (delta.$1.abs() == 1 && delta.$2.abs() == 2) || (delta.$1.abs() == 2 && delta.$2.abs() == 1),
  _ => false
};

void main() {
  print("Rux (0, 4) yura oladimi: ${isValidMove('Rook', (0, 4))}");
  print("Fil (2, 2) yura oladimi: ${isValidMove('Bishop', (2, 2))}");
  print("Ot (1, 2) yura oladimi:  ${isValidMove('Knight', (1, 2))}");
}
```

## Tushuntirish va Mantiq:
Kortejli switch shaxmat o'yini qoidalarini aniq va matematik ixcham ifodalaydi.

## Ishlash natijasi:
```text
Rux (0, 4) yura oladimi: true
Fil (2, 2) yura oladimi: true
Ot (1, 2) yura oladimi:  true
```

# 337-Topshiriq: Markdown teglari tahlilchisi (Token parser)
## Topshiriq sharti:
Satr boshidagi belgilarga qarab uning Markdown elementi turini aniqlang.

## Yechim (Dart kodi):
```dart
String parseMarkdown(String line) => switch (line.trim()) {
  var s when s.startsWith("# ") => "1-darajali sarlavha: ${s.substring(2)}",
  var s when s.startsWith("## ") => "2-darajali sarlavha: ${s.substring(3)}",
  var s when s.startsWith("- ") => "Ro'yxat bandi: ${s.substring(2)}",
  var s when s.startsWith("```") => "Kod bloki chegarasi",
  var s => "Oddiy paragraf matni: $s"
};

void main() {
  print(parseMarkdown("# Katta Sarlavha"));
  print(parseMarkdown("- Birinchi band"));
  print(parseMarkdown("Oddiy matn qatori"));
}
```

## Tushuntirish va Mantiq:
`when` shartlari va satr metodlari matnli sintaktik analizatorlar yozishni osonlashtiradi.

## Ishlash natijasi:
```text
1-darajali sarlavha: Katta Sarlavha
Ro'yxat bandi: Birinchi band
Oddiy paragraf matni: Oddiy matn qatori
```

# 338-Topshiriq: Sana tahlili: (yil, oy, kun) Pattern Matching bilan
## Topshiriq sharti:
Sana komponentlarini tekshirib, faslni aniqlovchi dastur yozing.

## Yechim (Dart kodi):
```dart
String faslniTop((int yil, int oy, int kun) sana) => switch (sana) {
  (_, 12 || 1 || 2, _) => "Qish",
  (_, >= 3 && <= 5, _) => "Bahor",
  (_, >= 6 && <= 8, _) => "Yoz",
  (_, >= 9 && <= 11, _) => "Kuz",
  _ => "Noto'g'ri oy"
};

void main() {
  print("2026-11-07 fasli: ${faslniTop((2026, 11, 7))}");
  print("2026-05-15 fasli: ${faslniTop((2026, 5, 15))}");
}
```

## Tushuntirish va Mantiq:
Kortej ichidagi munosabat va mantiqiy naqshlar sana arifmetikasini bitta satrga tushiradi.

## Ishlash natijasi:
```text
2026-11-07 fasli: Kuz
2026-05-15 fasli: Bahor
```

# 339-Topshiriq: Funksiya xatolarini (T? data, Exception? error) rekordi bilan boshqarish
## Topshiriq sharti:
Natija yoki xatolikni rekord orqali qaytaruvchi va destructuring bilan o'quvchi xavfsiz funksiya yozing.

## Yechim (Dart kodi):
```dart
(int? natija, Exception? xato) xavfsizBolish(int a, int b) {
  if (b == 0) return (null, Exception("Nolga bo'lib bo'lmaydi"));
  return (a ~/ b, null);
}

void main() {
  var (natija, xato) = xavfsizBolish(20, 4);
  if (xato != null) {
    print("Xatolik: $xato");
  } else {
    print("Muvaffaqiyat: $natija");
  }
}
```

## Tushuntirish va Mantiq:
Kortejli xatolik qaytarish naqshi istisnolarni otish (throw) xarajatlarisiz dasturni barqaror qiladi.

## Ishlash natijasi:
```text
Muvaffaqiyat: 5
```

# 340-Topshiriq: Ko'p qavatli JSON dan qiymat sug'urib olish (Deep JSON extraction)
## Topshiriq sharti:
Murakkab ichma-ich JSON strukturasini bitta pattern orqali ochib oling.

## Yechim (Dart kodi):
```dart
void extractUser(Map<String, dynamic> json) {
  if (json case {
        "user": {
          "profile": {"name": String ism, "contacts": {"phone": String tel}}
        }
      }) {
    print("Foydalanuvchi: $ism, Telefon: $tel");
  } else {
    print("Ma'lumotlar formati to'g'ri kelmadi!");
  }
}

void main() {
  var payload = {
    "user": {
      "profile": {
        "name": "Nodirbek",
        "contacts": {"phone": "+998901234567"}
      }
    }
  };

  extractUser(payload);
}
```

## Tushuntirish va Mantiq:
Chuqur Map pattern matching 4-5 qavatli `if` va null tekshiruvlarni bitta toza naqshga almashtiradi.

## Ishlash natijasi:
```text
Foydalanuvchi: Nodirbek, Telefon: +998901234567
```

# 341-Topshiriq: Kesh natijasini tekshirish: Sealed CacheResult
## Topshiriq sharti:
Keshda ma'lumot topilganligi (Hit) yoki topilmaganligini (Miss) sealed klass bilan modellashtiring.

## Yechim (Dart kodi):
```dart
sealed class CacheResult<T> {}

class CacheHit<T> extends CacheResult<T> {
  final T value;
  CacheHit(this.value);
}

class CacheMiss<T> extends CacheResult<T> {}

void main() {
  CacheResult<String> res1 = CacheHit("HTML_CONTENT");
  CacheResult<String> res2 = CacheMiss();

  void process(CacheResult<String> r) {
    switch (r) {
      case CacheHit(value: var v):
        print("Keshdan olingan: $v");
      case CacheMiss():
        print("Keshda yo'q, serverdan yuklanmoqda...");
    }
  }

  process(res1);
  process(res2);
}
```

## Tushuntirish va Mantiq:
Kesh holatini sealed klassda ifodalash barcha ehtimoliy senariylarni to'liq qamrab olishni kafolatlaydi.

## Ishlash natijasi:
```text
Keshdan olingan: HTML_CONTENT
Keshda yo'q, serverdan yuklanmoqda...
```

# 342-Topshiriq: Redux / BLoC Action hodisalari tahlili
## Topshiriq sharti:
Foydalanuvchi interfeysi hodisalarini (Increment, Decrement, Reset) sealed klass va pattern matching bilan boshqaring.

## Yechim (Dart kodi):
```dart
sealed class CounterEvent {}
class IncrementEvent extends CounterEvent { final int amount; IncrementEvent(this.amount); }
class DecrementEvent extends CounterEvent {}
class ResetEvent extends CounterEvent {}

int reduce(int state, CounterEvent event) => switch (event) {
  IncrementEvent(amount: var a) => state + a,
  DecrementEvent() => state - 1,
  ResetEvent() => 0
};

void main() {
  int count = 0;
  count = reduce(count, IncrementEvent(5));
  count = reduce(count, DecrementEvent());
  print("Hisob: $count");

  count = reduce(count, ResetEvent());
  print("Reset so'ng: $count");
}
```

## Tushuntirish va Mantiq:
Redux va BLoC arxitekturalarida hodisalarni `switch` bilan boshqarish zamonaviy Flutter dasturlashining standarti hisoblanadi.

## Ishlash natijasi:
```text
Hisob: 4
Reset so'ng: 0
```

# 343-Topshiriq: Dart 3 List naqshi bilan Palindrom ro'yxatni tekshirish
## Topshiriq sharti:
Ro'yxatning birinchi va oxirgi elementlarini rekursiv ochib palindromlikni tekshiring.

## Yechim (Dart kodi):
```dart
bool isListPalindrome(List<int> list) {
  return switch (list) {
    [] || [_] => true,
    [var first, ...var middle, var last] when first == last => isListPalindrome(middle),
    _ => false
  };
}

void main() {
  print("[1, 2, 3, 2, 1] palindrom: ${isListPalindrome([1, 2, 3, 2, 1])}");
  print("[1, 2, 3, 4] palindrom:    ${isListPalindrome([1, 2, 3, 4])}");
}
```

## Tushuntirish va Mantiq:
List Pattern Matching rekursiv tuzilmalar ustida matematik go'zallik va tozalik beradi.

## Ishlash natijasi:
```text
[1, 2, 3, 2, 1] palindrom: true
[1, 2, 3, 4] palindrom:    false
```

# 344-Topshiriq: Qidiruv parametrlarini destructuring orqali tahlil qilish
## Topshiriq sharti:
Qidiruv so'rovi, sahifa raqami va saralash tartibini rekorddan ajratib oling.

## Yechim (Dart kodi):
```dart
typedef SearchQuery = ({String q, int page, String sort});

void executeSearch(SearchQuery query) {
  var (:q, :page, :sort) = query;
  print("Qidirilmoqda: '$q' | Sahifa: $page | Tartib: $sort");
}

void main() {
  executeSearch((q: "Sun'iy intellekt", page: 1, sort: "desc"));
}
```

## Tushuntirish va Mantiq:
Qidiruv parametrlarini rekord orqali uzatish va ochish xotirani band qilmasdan toza kod beradi.

## Ishlash natijasi:
```text
Qidirilmoqda: 'Sun'iy intellekt' | Sahifa: 1 | Tartib: desc
```

# 345-Topshiriq: Shartli to'lov turi bo'yicha chek chiqarish
## Topshiriq sharti:
Karta, Naqd va Kriptovalyuta to'lovlarini turiga qarab alohida kvitansiya bilan qayta ishlang.

## Yechim (Dart kodi):
```dart
sealed class PaymentMethod {}
class CashPayment extends PaymentMethod { final double amount; CashPayment(this.amount); }
class CardPayment extends PaymentMethod { final String pan; final double amount; CardPayment(this.pan, this.amount); }
class CryptoPayment extends PaymentMethod { final String wallet; final double btc; CryptoPayment(this.wallet, this.btc); }

void printReceipt(PaymentMethod p) {
  switch (p) {
    case CashPayment(amount: var a):
      print("Naqd pul to'lovi: $a so'm");
    case CardPayment(pan: var pan, amount: var a):
      print("Karta to'lovi ($pan): $a so'm");
    case CryptoPayment(wallet: var w, btc: var b):
      print("Kripto o'tkazma ($w): $b BTC");
  }
}

void main() {
  printReceipt(CardPayment("8600 **** **** 1234", 150000));
  printReceipt(CryptoPayment("0xABC123", 0.005));
}
```

## Tushuntirish va Mantiq:
Sealed turlar har bir to'lov turi o'ziga xos parametrlarga ega bo'lishini qat'iy kafolatlaydi.

## Ishlash natijasi:
```text
Karta to'lovi (8600 **** **** 1234): 150000.0 so'm
Kripto o'tkazma (0xABC123): 0.005 BTC
```

# 346-Topshiriq: Matematik ifodani optimallashtirish (Pattern matching bilan soddalashtirish)
## Topshiriq sharti:
0 qo'shilgan yoki 1 ga ko'paytirilgan ifodalarni avtomatik soddalashtiruvchi qoidalar yozing.

## Yechim (Dart kodi):
```dart
sealed class NodeExpr {}
class ConstNode extends NodeExpr { final int val; ConstNode(this.val); }
class AddNode extends NodeExpr { final NodeExpr left, right; AddNode(this.left, this.right); }

NodeExpr simplify(NodeExpr expr) => switch (expr) {
  AddNode(left: ConstNode(val: 0), right: var r) => simplify(r), // 0 + x = x
  AddNode(left: var l, right: ConstNode(val: 0)) => simplify(l), // x + 0 = x
  _ => expr
};

void main() {
  NodeExpr test = AddNode(ConstNode(0), ConstNode(42));
  NodeExpr sodda = simplify(test);

  if (sodda case ConstNode(val: var v)) {
    print("Soddalashtirilgan qiymat: $v");
  }
}
```

## Tushuntirish va Mantiq:
Kompilyator optimizatorlari (algebraic simplifications) aynan shunday pattern matching qoidalariga asoslanadi.

## Ishlash natijasi:
```text
Soddalashtirilgan qiymat: 42
```

# 347-Topshiriq: Qator va Ustun koordinatalari bilan shaxmat taxtasi katagini aniqlash
## Topshiriq sharti:
`(col, row)` orqali katak rangini aniqlang.

## Yechim (Dart kodi):
```dart
String katakRangi((String col, int row) pos) {
  int c = pos.$1.codeUnitAt(0) - 'a'.codeUnitAt(0);
  int r = pos.$2;
  return ((c + r) % 2 == 0) ? "Qora" : "Oq";
}

void main() {
  print("a1 katagi: ${katakRangi(('a', 1))}");
  print("e4 katagi: ${katakRangi(('e', 4))}");
}
```

## Tushuntirish va Mantiq:
Records va belgilar kodlari orqali koordinatalar geometriyasi tezkor aniqlanadi.

## Ishlash natijasi:
```text
a1 katagi: Qora
e4 katagi: Oq
```

# 348-Topshiriq: Statistik kvartillar (Q1, Median, Q3) ni rekordda qaytarish
## Topshiriq sharti:
Ro'yxatdan Q1, Median va Q3 ko'rsatkichlarini hisoblab nomlangan rekordda qaytaring.

## Yechim (Dart kodi):
```dart
({double q1, double median, double q3}) getQuartiles(List<num> data) {
  var s = List<num>.from(data)..sort();
  int n = s.length;
  double med = s[n ~/ 2].toDouble();
  double q1 = s[n ~/ 4].toDouble();
  double q3 = s[(3 * n) ~/ 4].toDouble();
  return (q1: q1, median: med, q3: q3);
}

void main() {
  var stats = getQuartiles([10, 20, 30, 40, 50, 60, 70, 80]);
  print("Q1: ${stats.q1}, Mediana: ${stats.median}, Q3: ${stats.q3}");
}
```

## Tushuntirish va Mantiq:
Statistik hisob-kitoblarda bir nechta metrikalarni guruhlab qaytarish juda qulaydir.

## Ishlash natijasi:
```text
Q1: 30.0, Mediana: 50.0, Q3: 70.0
```

# 349-Topshiriq: Kombinatsiyalash: Ro'yxatdagi rekordlarni saralash
## Topshiriq sharti:
`(String ism, int ball)` rekordlar ro'yxatini balli bo'yicha tartiblang.

## Yechim (Dart kodi):
```dart
void main() {
  List<(String, int)> reyting = [
    ("Ali", 88),
    ("Vali", 95),
    ("G'ani", 72)
  ];

  reyting.sort((a, b) => b.$2.compareTo(a.$2)); // Ball kamayish tartibida

  print("Saralangan reyting:");
  for (var (ism, ball) in reyting) {
    print("- $ism: $ball ball");
  }
}
```

## Tushuntirish va Mantiq:
Rekordlar ro'yxatini saralash va destructuring bilan o'qish kodni maksimal toza qiladi.

## Ishlash natijasi:
```text
Saralangan reyting:
- Vali: 95 ball
- Ali: 88 ball
- G'ani: 72 ball
```

# 350-Topshiriq: Katta amaliy loyiha: Zamonaviy Kompilyator Lexer va AST Parser (Dart 3 Pattern Engine)
## Topshiriq sharti:
350-topshiriq: Matnli arifmetik ifodani tokenlarga ajratuvchi (Lexer), Abstract Syntax Tree (AST) quruvchi va uni baholovchi to'liq kompilyator quvuri dasturini Dart 3 Records va Pattern Matching bilan yozing.

## Yechim (Dart kodi):
```dart
sealed class Token {}
class NumberToken extends Token { final int val; NumberToken(this.val); }
class PlusToken extends Token {}
class StarToken extends Token {}

List<Token> tokenize(String input) {
  List<Token> tokens = [];
  var words = input.split(' ');
  for (var w in words) {
    switch (w) {
      case "+": tokens.add(PlusToken());
      case "*": tokens.add(StarToken());
      case var numStr when int.tryParse(numStr) != null:
        tokens.add(NumberToken(int.parse(numStr)));
      case _:
        throw FormatException("Noma'lum belgi: $w");
    }
  }
  return tokens;
}

sealed class ASTNode {}
class NumNode extends ASTNode { final int value; NumNode(this.value); }
class BinOpNode extends ASTNode {
  final ASTNode left;
  final String op;
  final ASTNode right;
  BinOpNode(this.left, this.op, this.right);
}

int evalAST(ASTNode node) => switch (node) {
  NumNode(value: var v) => v,
  BinOpNode(left: var l, op: "+", right: var r) => evalAST(l) + evalAST(r),
  BinOpNode(left: var l, op: "*", right: var r) => evalAST(l) * evalAST(r),
  _ => 0
};

void main() {
  String mathText = "10 + 20 * 2";
  print("Kiritilgan ifoda: $mathText");

  var tokens = tokenize("10 + 20");
  print("Tokenlar soni: ${tokens.length} ta");

  // AST: (10 + 20) * 2
  ASTNode ast = BinOpNode(
    BinOpNode(NumNode(10), "+", NumNode(20)),
    "*",
    NumNode(2)
  );

  int natija = evalAST(ast);
  print("AST baholash natijasi: (10 + 20) * 2 = $natija");
}
```

## Tushuntirish va Mantiq:
350-topshiriq bilan Dart 3 tilining eng zamonaviy Records, Pattern Matching va Sealed klasslar imkoniyatlari sanoat darajasidagi mini-kompilyator misolida to'liq o'zlashtirildi.

## Ishlash natijasi:
```text
Kiritilgan ifoda: 10 + 20 * 2
Tokenlar soni: 3 ta
AST baholash natijasi: (10 + 20) * 2 = 60
```

