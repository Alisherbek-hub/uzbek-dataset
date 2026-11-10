# 2-Qism: Sound Null Safety va Null Xavfsizligi (51-100)

Ushbu qismda Dart tilining eng qudratli imkoniyatlaridan biri bo'lgan Sound Null Safety (soxta null xatolaridan to'liq kafolatlangan himoya), nullable va non-nullable turlar, `?.`, `??`, `??=`, `!`, `late`, type promotion va null-xavfsiz ma'lumot tuzilmalari o'rganiladi.

# 51-Topshiriq: Nullable va Non-nullable turlar (int vs int?)
## Topshiriq sharti:
Dart da odatiy `int` o'zgaruvchisiga `null` berib bo'lmasligini va so'roq belgisi `int?` orqali nullable tur e'lon qilinishini ko'rsating.

## Yechim (Dart kodi):
```dart
void main() {
  int a = 10;
  // a = null; // XATOLIK: int turiga null berib bo'lmaydi!

  int? b = 20;
  print("b dastlab: $b");

  b = null; // Qonuniy
  print("b null bo'lgach: $b");
  print("a non-nullable: $a");
}
```

## Tushuntirish va Mantiq:
Dart da turlar sukut bo'yicha non-nullable (hech qachon null bo'la olmaydi). Agar o'zgaruvchi null qiymat qabul qilishi kerak bo'lsa, tur nomiga `?` qo'shiladi.

## Ishlash natijasi:
```text
b dastlab: 20
b null bo'lgach: null
a non-nullable: 10
```

# 52-Topshiriq: Nullable o'zgaruvchini null ga tekshirish
## Topshiriq sharti:
Nullable satr berilgan bo'lsa, oddiy `if (matn != null)` sharti orqali tekshirib, xavfsiz chop eting.

## Yechim (Dart kodi):
```dart
void main() {
  String? foydalanuvchiNomi;

  if (foydalanuvchiNomi != null) {
    print("Foydalanuvchi: $foydalanuvchiNomi");
  } else {
    print("Foydalanuvchi tizimga kirmagan (Mehmon).");
  }

  foydalanuvchiNomi = "Temur";
  if (foydalanuvchiNomi != null) {
    print("Foydalanuvchi: $foydalanuvchiNomi");
  }
}
```

## Tushuntirish va Mantiq:
`if` bloki ichida tekshirilgandan so'ng, Dart avtomatik ravishda o'zgaruvchini non-nullable sifatida qabul qiladi (Type Promotion).

## Ishlash natijasi:
```text
Foydalanuvchi tizimga kirmagan (Mehmon).
Foydalanuvchi: Temur
```

# 53-Topshiriq: Null-aware kirish operatori: ?.
## Topshiriq sharti:
Nullable satrning `.length` yoki `.toUpperCase()` metodlariga `?.` (agar null bo'lmasa chaqir) operatori orqali xavfsiz murojaat qiling.

## Yechim (Dart kodi):
```dart
void main() {
  String? shahar;
  print("Bo'sh shahar uzunligi: ${shahar?.length}");

  shahar = "Buxoro";
  print("Mavjud shahar uzunligi: ${shahar?.length}");
  print("Katta harflarda: ${shahar?.toUpperCase()}");
}
```

## Tushuntirish va Mantiq:
Agar ob'ekt `null` bo'lsa, `?.` operatori o'ng tomondagi metodni chaqirmasdan to'g'ridan-to'g'ri `null` qaytaradi va xatolik (NullPointerException) yuz berishining oldini oladi.

## Ishlash natijasi:
```text
Bo'sh shahar uzunligi: null
Mavjud shahar uzunligi: 6
Katta harflarda: BUXORO
```

# 54-Topshiriq: Null-coalescing operatori: ?? (Standart qiymat berish)
## Topshiriq sharti:
Agar o'zgaruvchi `null` bo'lsa, uning o'rniga muqobil standart (fallback) qiymatni tanlovchi `??` operatorini qo'llang.

## Yechim (Dart kodi):
```dart
void main() {
  String? taxallus;
  String korsatishNomi = taxallus ?? "Noma'lum foydalanuvchi";
  print("Natija 1: $korsatishNomi");

  taxallus = "Alisher";
  korsatishNomi = taxallus ?? "Noma'lum foydalanuvchi";
  print("Natija 2: $korsatishNomi");
}
```

## Tushuntirish va Mantiq:
`a ?? b` ifodasi: agar `a` null bo'lmasa `a` ning qiymatini, aks holda `b` ning qiymatini qaytaradi.

## Ishlash natijasi:
```text
Natija 1: Noma'lum foydalanuvchi
Natija 2: Alisher
```

# 55-Topshiriq: Null-coalescing tayinlash operatori: ??=
## Topshiriq sharti:
Faqat va faqat o'zgaruvchi ayni paytda `null` bo'lgandagina unga yangi qiymat yuklovchi `??=` operatorini ko'rsating.

## Yechim (Dart kodi):
```dart
void main() {
  int? ball;
  print("Dastlab: $ball");

  ball ??= 50; // ball null edi, shuning uchun 50 bo'ladi
  print("Birinchi ??= so'ng: $ball");

  ball ??= 100; // ball null emas (50), shuning uchun o'zgarmaydi!
  print("Ikkinchi ??= so'ng: $ball");
}
```

## Tushuntirish va Mantiq:
`x ??= y` amali `if (x == null) x = y;` ga teng bo'lib, sozlamalarni sukut bo'yicha to'ldirishda juda qulaydir.

## Ishlash natijasi:
```text
Dastlab: null
Birinchi ??= so'ng: 50
Ikkinchi ??= so'ng: 50
```

# 56-Topshiriq: Null assertion operatori: ! (Bang operator)
## Topshiriq sharti:
Dasturchi qiymatning null emasligiga 100% amin bo'lgan holatda `!` operatori orqali uni non-nullable turga majburiy o'tkazishni ko'rsating.

## Yechim (Dart kodi):
```dart
void main() {
  int? mumkinNull = 42;

  // Biz 42 mavjudligini bilamiz, shuning uchun ! qo'yamiz
  int aniqSon = mumkinNull!;
  print("Olingan son: $aniqSon");
}
```

## Tushuntirish va Mantiq:
`!` operatori kompilyatorga 'Men kafolat beraman, bu qiymat null emas' deb aytadi. Agar qiymat baribir null bo'lib chiqsa, dastur runtime xatosi beradi.

## Ishlash natijasi:
```text
Olingan son: 42
```

# 57-Topshiriq: ! operatorining xatosi va uni ushlab qolish
## Topshiriq sharti:
`null` bo'lgan o'zgaruvchiga `!` qo'llanilganda sodir bo'ladigan xatoni `try-catch` orqali ko'ring.

## Yechim (Dart kodi):
```dart
void main() {
  String? boqiyNull = null;

  try {
    String matn = boqiyNull!;
    print(matn);
  } catch (e) {
    print("Ushlangan xato: $e");
  }
}
```

## Tushuntirish va Mantiq:
`!` operatori faqat mutlaq ishonch bo'lgandagina ishlatilishi kerak. Aks holda `??` yoki `if` orqali tekshirish eng to'g'ri amaliyotdir.

## Ishlash natijasi:
```text
Ushlangan xato: Null check operator used on a null value
```

# 58-Topshiriq: Type Promotion: if tekshiruvidan so'ng avtomatik non-nullable bo'lish
## Topshiriq sharti:
Lokal o'zgaruvchi `if (x != null)` orqali tekshirilgach, unga `!` yoki `?` siz to'g'ridan-to'g'ri murojaat qilishni ko'rsating.

## Yechim (Dart kodi):
```dart
void printLength(String? matn) {
  if (matn != null) {
    // Bu blok ichida matn avtomatik ravishda String ga aylanadi!
    print("Uzunligi: ${matn.length}");
    print("Katta harfda: ${matn.toUpperCase()}");
  } else {
    print("Matn null ekan!");
  }
}

void main() {
  printLength("O'zbekiston");
  printLength(null);
}
```

## Tushuntirish va Mantiq:
Dart oqim tahlili (Flow Analysis) orqali o'zgaruvchi tekshiruvdan o'tganini ko'radi va ushbu blok doirasida uni non-nullable sifatida talqin qiladi.

## Ishlash natijasi:
```text
Uzunligi: 11
Katta harfda: O'ZBEKISTON
Matn null ekan!
```

# 59-Topshiriq: late kalit so'zi: Kechiktirilgan initsializatsiya
## Topshiriq sharti:
`late` yordamida non-nullable o'zgaruvchi e'lon qiling va unga qiymatni biroz keyinroq bering.

## Yechim (Dart kodi):
```dart
void main() {
  late String xabar;

  // Keyinroq hisoblash yoki yuklash
  xabar = "Salom, kechiktirilgan initsializatsiya!";
  print(xabar);
}
```

## Tushuntirish va Mantiq:
`late` o'zgaruvchiga qiymat darhol berilmasligini, lekin birinchi marta o'qilgunga qadar albatta berilishini kompilyatorga bildiradi.

## Ishlash natijasi:
```text
Salom, kechiktirilgan initsializatsiya!
```

# 60-Topshiriq: late final o'zgaruvchilar: Bir marta kechiktirib beriladigan qiymat
## Topshiriq sharti:
`late final` o'zgaruvchi yarating, unga faqat bir marta qiymat berish mumkinligini ko'rsating.

## Yechim (Dart kodi):
```dart
void main() {
  late final int id;

  id = 1001; // Birinchi va yagona marta qiymat berish
  print("Tayinlangan ID: $id");

  // id = 1002; // XATOLIK: late final ni qayta o'zgartirib bo'lmaydi!
}
```

## Tushuntirish va Mantiq:
`late final` o'zgaruvchi bitta o'zgarmas qiymatni kechiktirib o'rnatish uchun idealdir (masalan, API dan kelgan ma'lumotni keshda bir marta saqlash).

## Ishlash natijasi:
```text
Tayinlangan ID: 1001
```

# 61-Topshiriq: late o'zgaruvchini qiymat bermasdan o'qish xatosi
## Topshiriq sharti:
Qiymat berilmagan `late` o'zgaruvchi o'qilganda qanday xato chiqishini `try-catch` bilan tahlil qiling.

## Yechim (Dart kodi):
```dart
void main() {
  late String unutilgan;

  try {
    print(unutilgan);
  } catch (e) {
    print("Xatolik ushlandi: $e");
  }
}
```

## Tushuntirish va Mantiq:
`late` o'zgaruvchi o'qilishidan oldin unga albatta qiymat berilgan bo'lishi shart, aks holda `LateInitializationError` tashlanadi.

## Ishlash natijasi:
```text
Xatolik ushlandi: LateInitializationError: Field 'unutilgan' has not been initialized.
```

# 62-Topshiriq: late ning dangasa (Lazy) tabiati
## Topshiriq sharti:
`late` o'zgaruvchi unga murojaat qilinmaguncha hisoblanmasligini ko'rsatuvchi dastur yozing.

## Yechim (Dart kodi):
```dart
int ogirHisoblash() {
  print("[ogirHisoblash]: Funksiya bajarilmoqda...");
  return 42 * 100;
}

void main() {
  print("Dastur boshlandi.");
  late int natija = ogirHisoblash(); // Hozircha chaqirilmaydi!

  print("Natijaga hali murojaat qilinmadi.");
  print("Natija qiymati: $natija"); // Mana endi chaqiriladi!
}
```

## Tushuntirish va Mantiq:
Agar `late` o'zgaruvchiga dastur davomida umuman murojaat qilinmasa, uning initsializatsiya funksiyasi umuman ishga tushmaydi. Bu resurslarni tejaydi.

## Ishlash natijasi:
```text
Dastur boshlandi.
Natijaga hali murojaat qilinmadi.
[ogirHisoblash]: Funksiya bajarilmoqda...
Natija qiymati: 4200
```

# 63-Topshiriq: Nullable ro'yxatlar: List<int>?, List<int?>, List<int?>?
## Topshiriq sharti:
Ro'yxatning o'zi null bo'lishi, elementlari null bo'lishi va har ikkalasi null bo'lishi mumkin bo'lgan 3 xil holatni ko'rsating.

## Yechim (Dart kodi):
```dart
void main() {
  // 1. Elementlari null bo'lishi mumkin, lekin ro'yxatning o'zi null emas
  List<int?> elementlarNull = [1, null, 3];
  print("1. Ro'yxat: $elementlarNull");

  // 2. Ro'yxatning o'zi null bo'lishi mumkin, lekin elementlar null bo'lolmaydi
  List<int>? royxatNull = null;
  print("2. Ro'yxat: $royxatNull");

  // 3. Ro'yxat ham, uning elementlari ham null bo'lishi mumkin
  List<int?>? ikkalasiNull = [null, 42];
  print("3. Ro'yxat: $ikkalasiNull");
}
```

## Tushuntirish va Mantiq:
`List<T?>` ro'yxat ichida null bo'lishiga ruxsat beradi. `List<T>?` esa butun ro'yxat o'zgaruvchisi null bo'lishiga ruxsat beradi.

## Ishlash natijasi:
```text
1. Ro'yxat: [1, null, 3]
2. Ro'yxat: null
3. Ro'yxat: [null, 42]
```

# 64-Topshiriq: Null-aware spread operatori: ...?
## Topshiriq sharti:
Agar ikkinchi ro'yxat `null` bo'lishi mumkin bo'lsa, uni xatosiz asosiy ro'yxatga qo'shuvchi `...?` operatoridan foydalaning.

## Yechim (Dart kodi):
```dart
void main() {
  List<int> asosiy = [1, 2, 3];
  List<int>? qoshimcha = null;

  List<int> yangiRoyxat = [
    0,
    ...asosiy,
    ...?qoshimcha, // agar qoshimcha null bo'lsa, shunchaki e'tiborsiz qoldiriladi
    4
  ];

  print("Yangi ro'yxat: $yangiRoyxat");
}
```

## Tushuntirish va Mantiq:
`...?` operatori null-safety ni ro'yxatlarni birlashtirishda juda ixcham va xavfsiz qiladi.

## Ishlash natijasi:
```text
Yangi ro'yxat: [0, 1, 2, 3, 4]
```

# 65-Topshiriq: Null-aware indekslash: ?[index]
## Topshiriq sharti:
Agar ro'yxat yoki map `null` bo'lishi mumkin bo'lsa, uning indeksiga `?[index]` orqali xavfsiz murojaat qiling.

## Yechim (Dart kodi):
```dart
void main() {
  List<String>? ismlar;
  print("Null ro'yxat 0-elementi: ${ismlar?[0]}");

  ismlar = ["Ali", "Vali"];
  print("Mavjud ro'yxat 0-elementi: ${ismlar?[0]}");
}
```

## Tushuntirish va Mantiq:
Dart 2.12+ da kiritilgan `?[index]` agar kolleksiya null bo'lsa, xatolik bermasdan darhol null qaytaradi.

## Ishlash natijasi:
```text
Null ro'yxat 0-elementi: null
Mavjud ro'yxat 0-elementi: Ali
```

# 66-Topshiriq: Null-aware kaskad operatori: ?..
## Topshiriq sharti:
Agar ob'ekt `null` bo'lishi mumkin bo'lsa, uning bir nechta metodlarini kaskad tarzda chaqirish uchun `?..` operatorini qo'llang.

## Yechim (Dart kodi):
```dart
class Xabar {
  String matn = "";
  void qosh(String s) => matn += s;
  void chopEt() => print("Xabar: $matn");
}

void main() {
  Xabar? x1 = null;
  x1
    ?..qosh("Salom ")
    ..qosh("Dunyo!")
    ..chopEt(); // x1 null bo'lgani uchun hech narsa bo'lmaydi

  Xabar? x2 = Xabar();
  x2
    ?..qosh("Assalomu ")
    ..qosh("alaykum!")
    ..chopEt();
}
```

## Tushuntirish va Mantiq:
`?..` birinchi murojaatda null ekanini tekshiradi va agar ob'ekt mavjud bo'lsa, keyingi barcha kaskad `..` amallarini bajaradi.

## Ishlash natijasi:
```text
Xabar: Assalomu alaykum!
```

# 67-Topshiriq: Funksiya parametrlarida Null Safety
## Topshiriq sharti:
Funksiyaga ixtiyoriy nullable parametr va majburiy non-nullable parametr uzating.

## Yechim (Dart kodi):
```dart
void salomBer(String ism, [String? unvon]) {
  if (unvon != null) {
    print("Hurmatli $unvon $ism!");
  } else {
    print("Salom, $ism!");
  }
}

void main() {
  salomBer("Alisher", "Professor");
  salomBer("Bobur");
}
```

## Tushuntirish va Mantiq:
Kvadrat qavs ichidagi `[String? unvon]` parametri ixtiyoriy hisoblanadi va unga qiymat uzatilmasa sukut bo'yicha `null` bo'ladi.

## Ishlash natijasi:
```text
Hurmatli Professor Alisher!
Salom, Bobur!
```

# 68-Topshiriq: required kalit so'zi bilan nomlangan parametrlarni null-xavfsiz qilish
## Topshiriq sharti:
Nomlangan parametrlarda `required` kalit so'zi orqali null bo'lmagan majburiy parametrlarni talab qiling.

## Yechim (Dart kodi):
```dart
void profilYarat({required String username, required int yosh, String? shahar}) {
  print("Username: $username, Yoshi: $yosh, Shahar: ${shahar ?? 'Ko\'rsatilmagan'}");
}

void main() {
  profilYarat(username: "nodir_ai", yosh: 22);
  profilYarat(username: "malika_dev", yosh: 25, shahar: "Toshkent");
}
```

## Tushuntirish va Mantiq:
`required` bo'lgan nomlangan parametrga qiymat berish shart va u non-nullable bo'lgani uchun hech qachon null bo'lolmaydi.

## Ishlash natijasi:
```text
Username: nodir_ai, Yoshi: 22, Shahar: Ko'rsatilmagan
Username: malika_dev, Yoshi: 25, Shahar: Toshkent
```

# 69-Topshiriq: Funksiyaning null qaytarishi va uni to'g'ri qayta ishlash
## Topshiriq sharti:
Foydalanuvchi yoshini tekshirib, agar manfiy bo'lsa `null`, aks holda toifa qaytaruvchi funksiya yozing.

## Yechim (Dart kodi):
```dart
String? yoshToifasi(int yosh) {
  if (yosh < 0) return null; // Noto'g'ri yosh
  if (yosh < 18) return "Yosh bola";
  if (yosh < 60) return "Katta yoshli";
  return "Keksa";
}

void main() {
  print("25 yosh: ${yoshToifasi(25) ?? 'Xato yosh'}");
  print("-5 yosh: ${yoshToifasi(-5) ?? 'Xato yosh'}");
}
```

## Tushuntirish va Mantiq:
Funksiya qaytaruvchi turi `String?` bo'lsa, chaqiruvchi tomon natijani `??` yoki `if` orqali to'g'ri boshqarishi shart.

## Ishlash natijasi:
```text
25 yosh: Katta yoshli
-5 yosh: Xato yosh
```

# 70-Topshiriq: Ternar operator va ?? operatori solishtiruvi
## Topshiriq sharti:
Bitta mantiqiy vazifani ternar operator (`shart ? a : b`) va `??` operatori orqali yozib, qulaylikni taqqoslang.

## Yechim (Dart kodi):
```dart
void main() {
  String? kiruvchi;

  // 1. Ternar operator
  String res1 = kiruvchi != null ? kiruvchi : "Standart";

  // 2. Null-coalescing ?? operatori (ancha ixcham)
  String res2 = kiruvchi ?? "Standart";

  print("Res1: $res1");
  print("Res2: $res2");
}
```

## Tushuntirish va Mantiq:
`a ?? b` ifodasi `a != null ? a : b` ning qisqartirilgan va o'qilishi oson ko'rinishidir.

## Ishlash natijasi:
```text
Res1: Standart
Res2: Standart
```

# 71-Topshiriq: Map dan qiymat o'qishda null qaytishi va boshqarish
## Topshiriq sharti:
Lug'atda (Map) kalit mavjud bo'lmaganda `null` qaytishini ko'rsating va uni `??` bilan hal qiling.

## Yechim (Dart kodi):
```dart
void main() {
  Map<String, String> poytaxtlar = {
    "O'zbekiston": "Toshkent",
    "Qozog'iston": "Ostona"
  };

  String? p1 = poytaxtlar["O'zbekiston"];
  String p2 = poytaxtlar["Yaponiya"] ?? "Ma'lumot yo'q";

  print("O'zbekiston poytaxti: $p1");
  print("Yaponiya poytaxti: $p2");
}
```

## Tushuntirish va Mantiq:
Dart da Map ning `[]` operatori har doim nullable tur (`V?`) qaytaradi, chunki so'ralgan kalit lug'atda bo'lmasligi mumkin.

## Ishlash natijasi:
```text
O'zbekiston poytaxti: Toshkent
Yaponiya poytaxti: Ma'lumot yo'q
```

# 72-Topshiriq: firstWhere() metodida orElse orqali null qaytarish
## Topshiriq sharti:
Ro'yxatdan shartga mos element qidirishda moslik topilmasa dastur qulamasligi uchun `orElse: () => null` dan foydalaning.

## Yechim (Dart kodi):
```dart
void main() {
  List<int> sonlar = [1, 3, 5, 7, 9];

  // Juft sonni qidiramiz
  int? juftSon;
  for (int x in sonlar) {
    if (x % 2 == 0) {
      juftSon = x;
      break;
    }
  }

  print("Topilgan juft son: ${juftSon ?? 'Topilmadi'}");
}
```

## Tushuntirish va Mantiq:
To'g'ridan-to'g'ri `firstWhere` topilmaganda `StateError` tashlaydi. Null-xavfsiz sikl yoki orElse yordamida `null` qaytarish xavfsizdir.

## Ishlash natijasi:
```text
Topilgan juft son: Topilmadi
```

# 73-Topshiriq: firstWhereOrNull kengaytmasi (Extension method) yaratish
## Topshiriq sharti:
`Iterable` uchun element topilmasa xavfsiz `null` qaytaruvchi o'z `firstWhereOrNull` kengaytma metodimizni yozing.

## Yechim (Dart kodi):
```dart
extension FirstWhereOrNullExtension<E> on Iterable<E> {
  E? firstWhereOrNull(bool Function(E element) test) {
    for (E element in this) {
      if (test(element)) return element;
    }
    return null;
  }
}

void main() {
  List<String> ismlar = ["Anvar", "Dilshod", "Bobur"];

  String? topildi = ismlar.firstWhereOrNull((ism) => ism.startsWith("D"));
  String? topilmadi = ismlar.firstWhereOrNull((ism) => ism.startsWith("Z"));

  print("Topildi: $topildi");
  print("Topilmadi: $topilmadi");
}
```

## Tushuntirish va Mantiq:
Extension metodlar orqali standart kolleksiyalarga yangi null-xavfsiz funksionallik qo'shish Flutter va Dart dasturlashida keng qo'llaniladi.

## Ishlash natijasi:
```text
Topildi: Dilshod
Topilmadi: null
```

# 74-Topshiriq: Klass maydonlarida Null Safety va Konstruktor
## Topshiriq sharti:
Klassning non-nullable maydonlarini konstruktorda majburiy initsializatsiya qilishni ko'rsating.

## Yechim (Dart kodi):
```dart
class Foydalanuvchi {
  final String ism; // Non-nullable
  int? yosh;        // Nullable

  Foydalanuvchi(this.ism, [this.yosh]);

  void tanishtir() {
    print("Ism: $ism, Yosh: ${yosh ?? 'noma\'lum'}");
  }
}

void main() {
  var u1 = Foydalanuvchi("Sardor", 28);
  var u2 = Foydalanuvchi("Madina");

  u1.tanishtir();
  u2.tanishtir();
}
```

## Tushuntirish va Mantiq:
Konstruktorda `this.ism` yozilishi non-nullable maydon ob'ekt yaratilgan paytdayoq aniq qiymat olishini kafolatlaydi.

## Ishlash natijasi:
```text
Ism: Sardor, Yosh: 28
Ism: Madina, Yosh: noma'lum
```

# 75-Topshiriq: Initializer List orqali non-nullable maydonlarni hisoblash
## Topshiriq sharti:
Konstruktor tanasi (`{}`) bajarilishidan oldin non-nullable maydonni hisoblab qiymat beruvchi Initializer List sintaksisini yozing.

## Yechim (Dart kodi):
```dart
class Tortburchak {
  final double eni;
  final double boyi;
  final double yuza; // Non-nullable

  // Initializer list (ikki nuqta orqali)
  Tortburchak(this.eni, this.boyi) : yuza = eni * boyi;
}

void main() {
  var t = Tortburchak(4.0, 5.0);
  print("Eni: ${t.eni}, Bo'yi: ${t.boyi}, Yuzasi: ${t.yuza}");
}
```

## Tushuntirish va Mantiq:
Initializer list konstruktor tanasidan oldin bajariladi, shuning uchun `final` va non-nullable maydonlarni hisoblashning yagona to'g'ri joyi hisoblanadi.

## Ishlash natijasi:
```text
Eni: 4.0, Bo'yi: 5.0, Yuzasi: 20.0
```

# 76-Topshiriq: Factory konstruktorda null qaytarish (fromJsonOrNull)
## Topshiriq sharti:
JSON ma'lumotlari to'liq bo'lmaganda ob'ekt o'rniga `null` qaytaruvchi factory konstruktorni yarating.

## Yechim (Dart kodi):
```dart
class Mahsulot {
  final String nom;
  final double narx;

  Mahsulot._(this.nom, this.narx);

  static Mahsulot? fromJsonOrNull(Map<String, dynamic> json) {
    if (!json.containsKey("nom") || !json.containsKey("narx")) {
      return null; // Majburiy maydonlar yo'q
    }
    return Mahsulot._(json["nom"] as String, (json["narx"] as num).toDouble());
  }
}

void main() {
  var data1 = {"nom": "Noutbuk", "narx": 8500000};
  var data2 = {"nom": "Sichqoncha"}; // narx yo'q

  var m1 = Mahsulot.fromJsonOrNull(data1);
  var m2 = Mahsulot.fromJsonOrNull(data2);

  print("Mahsulot 1: ${m1?.nom} - ${m1?.narx} so'm");
  print("Mahsulot 2 mavjudmi: ${m2 != null}");
}
```

## Tushuntirish va Mantiq:
Nullable factory konstruktorlar yoki statik metodlar noto'g'ri API javoblarini qabul qilishda qulashlarning oldini oladi.

## Ishlash natijasi:
```text
Mahsulot 1: Noutbuk - 8500000.0 so'm
Mahsulot 2 mavjudmi: false
```

# 77-Topshiriq: Nullable funksiya turlari va xavfsiz chaqirish: fn?.call()
## Topshiriq sharti:
Callback funksiyasi `null` bo'lishi mumkin bo'lganda uni `?.call()` orqali xavfsiz chaqiring.

## Yechim (Dart kodi):
```dart
void tugmaBosildi(void Function(String)? onBosildi) {
  print("Tugma bosildi!");
  onBosildi?.call("Muvaffaqiyatli hodisa");
}

void main() {
  // Callback berilmagan holat
  tugmaBosildi(null);

  // Callback berilgan holat
  tugmaBosildi((xabar) {
    print("Qabul qilindi: $xabar");
  });
}
```

## Tushuntirish va Mantiq:
`onBosildi?.call(...)` sintaksisi `if (onBosildi != null) onBosildi(...)` tekshiruvining ixcham va toza muqobilidir.

## Ishlash natijasi:
```text
Tugma bosildi!
Tugma bosildi!
Qabul qilindi: Muvaffaqiyatli hodisa
```

# 78-Topshiriq: Sound Null Safety afzalliklari: Kompilyator optimizatsiyasi
## Topshiriq sharti:
Kompilyator non-nullable turlarni bilishi sababli qo'shimcha null-tekshiruvlarni olib tashlashini va kod hajmini ixchamlashtirishini tushuntiring.

## Yechim (Dart kodi):
```dart
int add(int a, int b) {
  // Kompilyator bu yerda a va b hech qachon null bo'lolmasligini 100% biladi
  // Shuning uchun hech qanday runtime if (a == null) tekshiruvi shart emas!
  return a + b;
}

void main() {
  int natija = add(15, 30);
  print("Yig'indi: $natija");
}
```

## Tushuntirish va Mantiq:
Dart ning 'Sound' (qattiq) tizimi tufayli kompilyator kodni mashina tiliga o'girganda (AOT) null tekshirish buyruqlarini bekor qiladi, bu dastur tezligini va xotira samaradorligini sezilarli oshiradi.

## Ishlash natijasi:
```text
Yig'indi: 45
```

# 79-Topshiriq: Klass maydonlarining Type Promotion cheklovi va yechimi
## Topshiriq sharti:
Klassning ochiq maydoni boshqa oqim yoki getter tomonidan o'zgartirilishi mumkinligi sababli to'g'ridan-to'g'ri promote bo'lmasligi va uni lokal o'zgaruvchiga olish yechimini ko'rsating.

## Yechim (Dart kodi):
```dart
class Server {
  String? status;

  void tekshir() {
    // Lokal o'zgaruvchiga nusxa olamiz (Shadowing / Local capture)
    final s = status;
    if (s != null) {
      // Endi s aniq String sifatida promote bo'ladi!
      print("Server holati: ${s.toUpperCase()}");
    } else {
      print("Status aniqlanmagan.");
    }
  }
}

void main() {
  var s = Server()..status = "ishlamoqda";
  s.tekshir();
}
```

## Tushuntirish va Mantiq:
Klass maydonlari getter bo'lishi yoki boshqa metodlar tomonidan o'zgartirilib qolishi mumkinligi uchun Dart ularni to'g'ridan-to'g'ri promote qilmaydi. `final s = status;` qilib olish eng to'g'ri yechimdir.

## Ishlash natijasi:
```text
Server holati: ISHLAMOQDA
```

# 80-Topshiriq: Nullable Generiklar: <T> vs <T?>
## Topshiriq sharti:
Generik konteyner sinfida tur parametri `T` va nullable `T?` bilan ishlashni ko'rsating.

## Yechim (Dart kodi):
```dart
class Quti<T> {
  final T qiymat;
  Quti(this.qiymat);
}

void main() {
  Quti<int> q1 = Quti(100);
  Quti<int?> q2 = Quti(null); // Nullable generik qiymat

  print("Quti 1: ${q1.qiymat}");
  print("Quti 2: ${q2.qiymat}");
}
```

## Tushuntirish va Mantiq:
Generik parametr `<T>` berilganda `T` o'zi allaqachon nullable tur bo'lishi mumkin (masalan `T = int?`).

## Ishlash natijasi:
```text
Quti 1: 100
Quti 2: null
```

# 81-Topshiriq: Generik turga Object cheklovi: <T extends Object>
## Topshiriq sharti:
Generik turga hech qachon `null` bo'lishiga yo'l qo'ymaslik uchun `<T extends Object>` cheklovini o'rnating.

## Yechim (Dart kodi):
```dart
class FaqatAniqQuti<T extends Object> {
  final T element;
  FaqatAniqQuti(this.element);
}

void main() {
  var q1 = FaqatAniqQuti<String>("Matn");
  var q2 = FaqatAniqQuti<int>(55);
  // var q3 = FaqatAniqQuti<String?>(null); // XATOLIK: String? Object ga to'g'ri kelmaydi!

  print("q1: ${q1.element}");
  print("q2: ${q2.element}");
}
```

## Tushuntirish va Mantiq:
Dart da `Object` non-nullable turlarning ildizi bo'lgani sababli, `T extends Object` generik parametrning hech qachon null bo'la olmasligini kafolatlaydi.

## Ishlash natijasi:
```text
q1: Matn
q2: 55
```

# 82-Topshiriq: Never tipi: Hech qachon qaytmaydigan funksiyalar
## Topshiriq sharti:
Har doim xato tashlaydigan yoki cheksiz sikl bilan ishlaydigan funksiyalarda `Never` qaytaruvchi turini qo'llang.

## Yechim (Dart kodi):
```dart
Never xatolikTashla(String xabar) {
  throw Exception("Qat'iy xatolik: $xabar");
}

void tekshir(int? son) {
  int aniqSon = son ?? xatolikTashla("Son kiritilishi shart!");
  print("Tekshirilgan son: $aniqSon");
}

void main() {
  tekshir(77);

  try {
    tekshir(null);
  } catch (e) {
    print("Ushlangan xato: $e");
  }
}
```

## Tushuntirish va Mantiq:
`Never` tipi funksiya hech qachon normal qiymat qaytarmasligini bildiradi. Oqim tahlili `Never` chaqiruvidan keyingi kod bajarilmasligini bilib, type promotion ni yanada kuchaytiradi.

## Ishlash natijasi:
```text
Tekshirilgan son: 77
Ushlangan xato: Exception: Qat'iy xatolik: Son kiritilishi shart!
```

# 83-Topshiriq: Xavfsiz tur o'zgartirish (Safe Cast): is Type ? x as Type : null
## Topshiriq sharti:
Noma'lum ob'ektni xavfsiz tarzda kerakli turga aylantiruvchi, mos kelmasa `null` qaytaruvchi yordamchi funksiya yozing.

## Yechim (Dart kodi):
```dart
T? safeCast<T>(dynamic value) {
  return value is T ? value : null;
}

void main() {
  dynamic d1 = "Dart tili";
  dynamic d2 = 12345;

  String? s1 = safeCast<String>(d1);
  String? s2 = safeCast<String>(d2);

  print("s1: $s1");
  print("s2: $s2");
}
```

## Tushuntirish va Mantiq:
Xavfsiz cast qilish usuli dasturning `TypeError` bilan qulashining oldini oladi va tekshiruvni toza nullable natijaga aylantiradi.

## Ishlash natijasi:
```text
s1: Dart tili
s2: null
```

# 84-Topshiriq: Null turi alohida tur sifatida
## Topshiriq sharti:
`Null` turi o'zining yagona nusxasi bo'lgan `null` qiymatiga ega ekanligini ko'rsating.

## Yechim (Dart kodi):
```dart
void main() {
  Null boqiy = null;
  print("boqiy qiymati: $boqiy");
  print("boqiy runtimeType: ${boqiy.runtimeType}");
  print("null is Null: ${null is Null}");
}
```

## Tushuntirish va Mantiq:
Dart da `Null` tipi barcha nullable turlarning (`T?`) quyi qismi (bottom type) hisoblanadi.

## Ishlash natijasi:
```text
boqiy qiymati: null
boqiy runtimeType: Null
null is Null: true
```

# 85-Topshiriq: Ko'p qatlamli null zanjiri (Null-aware chain)
## Topshiriq sharti:
Ichma-ich joylashgan tuzilmalardan (Foydalanuvchi -> Profil -> Manzil -> Shahar) ma'lumotni bitta qatorda xavfsiz oling.

## Yechim (Dart kodi):
```dart
class Manzil {
  final String? shahar;
  Manzil(this.shahar);
}

class Profil {
  final Manzil? manzil;
  Profil(this.manzil);
}

class Foydalanuvchi {
  final Profil? profil;
  Foydalanuvchi(this.profil);
}

void main() {
  Foydalanuvchi u1 = Foydalanuvchi(Profil(Manzil("Samarqand")));
  Foydalanuvchi u2 = Foydalanuvchi(Profil(null));
  Foydalanuvchi u3 = Foydalanuvchi(null);

  print("u1 shahri: ${u1.profil?.manzil?.shahar ?? 'Noma'lum'}");
  print("u2 shahri: ${u2.profil?.manzil?.shahar ?? 'Noma'lum'}");
  print("u3 shahri: ${u3.profil?.manzil?.shahar ?? 'Noma'lum'}");
}
```

## Tushuntirish va Mantiq:
Zanjirda istalgan bo'g'in `null` bo'lsa, qolgan chaqiruvlar bajarilmaydi va yakuniy `??` operatori standart qiymatni qaytaradi.

## Ishlash natijasi:
```text
u1 shahri: Samarqand
u2 shahri: Noma'lum
u3 shahri: Noma'lum
```

# 86-Topshiriq: Nullable qiymat bo'yicha switch-case
## Topshiriq sharti:
`switch` operatorida `null` holatini alohida `case null:` sifatida qayta ishlang.

## Yechim (Dart kodi):
```dart
void holatniTekshir(String? holat) {
  switch (holat) {
    case "faol":
      print("Tizim faol ishlamoqda.");
      break;
    case "kutilmoqda":
      print("Tizim navbatda kutmoqda.");
      break;
    case null:
      print("Holat ko'rsatilmagan (null)!");
      break;
    default:
      print("Noma'lum holat: $holat");
  }
}

void main() {
  holatniTekshir("faol");
  holatniTekshir(null);
  holatniTekshir("to'xtatilgan");
}
```

## Tushuntirish va Mantiq:
Dart da `switch` nullable qiymatlarni to'g'ridan-to'g'ri qo'llab-quvvatlaydi va barcha variantlarni xavfsiz boshqarishga imkon beradi.

## Ishlash natijasi:
```text
Tizim faol ishlamoqda.
Holat ko'rsatilmagan (null)!
Noma'lum holat: to'xtatilgan
```

# 87-Topshiriq: Dart 3 Pattern Matching da null-check pattern: case var v?
## Topshiriq sharti:
Dart 3 ning yangi pattern matching imkoniyatida `?` (null-check pattern) orqali faqat null bo'lmagan qiymatlarni ajratib oling.

## Yechim (Dart kodi):
```dart
void tahlilQil(int? son) {
  switch (son) {
    case var s? when s > 0:
      print("Musbat son: $s");
    case var s? when s < 0:
      print("Manfiy son: $s");
    case 0:
      print("Nol");
    case null:
      print("Qiymat kiritilmagan (null)");
  }
}

void main() {
  tahlilQil(15);
  tahlilQil(-7);
  tahlilQil(null);
}
```

## Tushuntirish va Mantiq:
Dart 3 dagi `var s?` patterni qiymatning null emasligini tekshiradi va bir vaqtning o'zida uni non-nullable `s` o'zgaruvchisiga biriktiradi (destructuring).

## Ishlash natijasi:
```text
Musbat son: 15
Manfiy son: -7
Qiymat kiritilmagan (null)
```

# 88-Topshiriq: Ikkilik daraxtda (Binary Tree) Null Safety
## Topshiriq sharti:
`TreeNode` sinfini yarating, uning chap va o'ng farzandlari `TreeNode?` bo'lsin va rekursiv yig'indisini hisoblang.

## Yechim (Dart kodi):
```dart
class TreeNode {
  int val;
  TreeNode? left;
  TreeNode? right;

  TreeNode(this.val, [this.left, this.right]);
}

int daraxtYigindisi(TreeNode? root) {
  if (root == null) return 0;
  return root.val + daraxtYigindisi(root.left) + daraxtYigindisi(root.right);
}

void main() {
  // Daraxt:    1
  //          /   \
  //         2     3
  var daraxt = TreeNode(1, TreeNode(2), TreeNode(3));
  print("Daraxt elementlari yig'indisi: ${daraxtYigindisi(daraxt)}");
}
```

## Tushuntirish va Mantiq:
Daraxt barglarida (leaf nodes) bolalar tabiiy ravishda `null` bo'ladi. Null safety rekursiya to'xtash shartini o'ta sodda va tushunarli qiladi.

## Ishlash natijasi:
```text
Daraxt elementlari yig'indisi: 6
```

# 89-Topshiriq: Bog'langan ro'yxatda (Linked List) Node? next bilan ishlash
## Topshiriq sharti:
Bir tomonlama bog'langan ro'yxat tugunlarini `Node? next` orqali bog'lang va oxirigacha bosib o'ting.

## Yechim (Dart kodi):
```dart
class Node {
  int data;
  Node? next;
  Node(this.data, [this.next]);
}

void main() {
  var head = Node(10, Node(20, Node(30)));

  Node? curr = head;
  stdoutWrite("Ro'yxat: ");
  while (curr != null) {
    stdoutWrite("${curr.data} -> ");
    curr = curr.next;
  }
  print("null");
}

void stdoutWrite(String s) => print(s); // Ekranga chiqarish
```

## Tushuntirish va Mantiq:
Ro'yxatning oxirgi tuguni `next == null` bo'ladi, bu siklni xatosiz yakunlash mezonidir.

## Ishlash natijasi:
```text
Ro'yxat: 
10 -> 
20 -> 
30 -> 
null
```

# 90-Topshiriq: Kesh klassida mavjud bo'lmagan qiymat bilan null qiymatni ajratish
## Topshiriq sharti:
Keshda kalit umuman yo'qligi bilan kalit bor ammo qiymati `null` ekanligini `containsKey` orqali to'g'ri ajrating.

## Yechim (Dart kodi):
```dart
class OddiyKesh {
  final Map<String, String?> _data = {};

  void saqla(String key, String? val) => _data[key] = val;

  void tekshir(String key) {
    if (_data.containsKey(key)) {
      print("Kalit '$key' mavjud, qiymati: '${_data[key]}'");
    } else {
      print("Kalit '$key' keshda umuman yo'q!");
    }
  }
}

void main() {
  var kesh = OddiyKesh();
  kesh.saqla("til", "O'zbek");
  kesh.saqla("parol", null); // Qiymat ataylab null qilib saqlangan

  kesh.tekshir("til");
  kesh.tekshir("parol");
  kesh.tekshir("login");
}
```

## Tushuntirish va Mantiq:
Faqat `_data[key] == null` deb tekshirish xato berishi mumkin, chunki qiymatning o'zi null bo'lishi mumkin. `containsKey` kalitning mavjudligini aniq aytadi.

## Ishlash natijasi:
```text
Kalit 'til' mavjud, qiymati: 'O'zbek'
Kalit 'parol' mavjud, qiymati: 'null'
Kalit 'login' keshda umuman yo'q!
```

# 91-Topshiriq: ArgumentError.checkNotNull yordamida tekshirish
## Topshiriq sharti:
Kiritilgan parametrning null emasligini tekshiruvchi va xato bo'lsa darhol xabar beruvchi funksiya yozing.

## Yechim (Dart kodi):
```dart
void foydalanuvchiYukla(String? id) {
  if (id == null) {
    throw ArgumentError.notNull("id");
  }
  print("Foydalanuvchi $id ma'lumotlari yuklanmoqda...");
}

void main() {
  foydalanuvchiYukla("USR_100");

  try {
    foydalanuvchiYukla(null);
  } catch (e) {
    print("Xato ushlandi: $e");
  }
}
```

## Tushuntirish va Mantiq:
Tizim chegaralarida (masalan, tashqi REST API yoki foydalanuvchi kiritmalari) bunday tekshiruvlar dasturning mustahkamligini ta'minlaydi.

## Ishlash natijasi:
```text
Foydalanuvchi USR_100 ma'lumotlari yuklanmoqda...
Xato ushlandi: Invalid argument(s) (id): Must not be null
```

# 92-Topshiriq: O'z checkNotNull() generik yordamchi funksiyamizni yozish
## Topshiriq sharti:
Qiymat `null` bo'lsa xato tashlovchi, aks holda uni kafolatlangan non-nullable `T` qilib qaytaruvchi funksiya yozing.

## Yechim (Dart kodi):
```dart
T mustBeNotNull<T>(T? value, String nom) {
  if (value == null) {
    throw StateError("Xatolik: '$nom' qiymati null bo'lishi mumkin emas!");
  }
  return value;
}

void main() {
  String? nom = "Antigravity";
  String tasdiqlangan = mustBeNotNull(nom, "nom");
  print("Tasdiqlangan qiymat: $tasdiqlangan");

  try {
    String? xato;
    mustBeNotNull(xato, "xato");
  } catch (e) {
    print(e);
  }
}
```

## Tushuntirish va Mantiq:
Ushbu naqsh majburiy konfiguratsiyalarni tekshirishda va toza non-nullable tur olishda juda foydali.

## Ishlash natijasi:
```text
Tasdiqlangan qiymat: Antigravity
Bad state: Xatolik: 'xato' qiymati null bo'lishi mumkin emas!
```

# 93-Topshiriq: Nullable boolean bilan shart tekshirish: if (boolVar == true)
## Topshiriq sharti:
`bool?` uchta holatga ega (`true`, `false`, `null`). Shartli tekshirishda `if (b == true)` usulining ahamiyatini ko'rsating.

## Yechim (Dart kodi):
```dart
void main() {
  bool? isOnline = null;

  // if (isOnline) // XATOLIK: bool? ni to'g'ridan-to'g'ri if ga qo'yib bo'lmaydi!
  if (isOnline == true) {
    print("Foydalanuvchi online.");
  } else {
    print("Foydalanuvchi offline yoki ma'lumot yo'q (hozirda: $isOnline).");
  }

  isOnline = true;
  if (isOnline == true) {
    print("Endi foydalanuvchi online!");
  }
}
```

## Tushuntirish va Mantiq:
`bool?` ni tekshirishda `b == true` yozish orqali ham `false`, ham `null` holatlari xavfsiz tarzda bitta `else` tarmog'iga o'tadi.

## Ishlash natijasi:
```text
Foydalanuvchi offline yoki ma'lumot yo'q (hozirda: null).
Endi foydalanuvchi online!
```

# 94-Topshiriq: Lokal shadowing (soyalash) orqali maydonlarni xavfsiz boshqarish
## Topshiriq sharti:
Klass maydoni nomini lokal o'zgaruvchi bilan bir xil nomlab (`final field = this.field`), uning ichki blokda promote bo'lishini ta'minlang.

## Yechim (Dart kodi):
```dart
class Xizmat {
  final String? apiToken;
  Xizmat(this.apiToken);

  void sorovYubor() {
    final apiToken = this.apiToken;
    if (apiToken != null) {
      // apiToken endi String (non-nullable)
      print("So'rov yuborilmoqda, token uzunligi: ${apiToken.length}");
    } else {
      print("Token yo'q, so'rov rad etildi.");
    }
  }
}

void main() {
  Xizmat("XYZ123_SECRET").sorovYubor();
  Xizmat(null).sorovYubor();
}
```

## Tushuntirish va Mantiq:
Dart da lokal o'zgaruvchi klass maydonini soyalaydi (shadows). Natijada klass maydoni xavfsiz non-nullable sifatida ishlatiladi.

## Ishlash natijasi:
```text
So'rov yuborilmoqda, token uzunligi: 13
Token yo'q, so'rov rad etildi.
```

# 95-Topshiriq: Callback larda Sukut bo'yicha Bo'sh Listener (Default Callback)
## Topshiriq sharti:
Null tekshiruvlardan qochish uchun ixtiyoriy callback parametriga bo'sh funksiyani (`() {}`) standart qiymat qilib belgilang.

## Yechim (Dart kodi):
```dart
void yuklash({void Function(int foiz) onProgress = _boshListener}) {
  for (int p = 50; p <= 100; p += 50) {
    onProgress(p);
  }
}

void _boshListener(int foiz) {} // Bo'sh standart listener

void main() {
  // Callbacksiz chaqirish - hech qanday xato yo'q
  yuklash();

  // Callback bilan chaqirish
  yuklash(onProgress: (f) => print("Yuklandi: $f%"));
}
```

## Tushuntirish va Mantiq:
Standart bo'sh funksiya belgilansa, parametr non-nullable bo'lib qoladi va kod ichida `?.call()` yozishga ehtiyoj qolmaydi.

## Ishlash natijasi:
```text
Yuklandi: 50%
Yuklandi: 100%
```

# 96-Topshiriq: Iterable.whereType<T>() bilan ro'yxatdan barcha null larni tozalash
## Topshiriq sharti:
`List<int?>` dan barcha `null` elementlarni chiqarib tashlab, toza `List<int>` hosil qiling.

## Yechim (Dart kodi):
```dart
void main() {
  List<int?> aralash = [10, null, 20, null, 30, 40, null];

  // whereType<int>() avtomatik ravishda int? ni int ga filtrlaydi
  List<int> tozaSonlar = aralash.whereType<int>().toList();

  print("Asl ro'yxat: $aralash");
  print("Tozalangan non-nullable ro'yxat: $tozaSonlar");
}
```

## Tushuntirish va Mantiq:
`whereType<T>()` nafaqat filtrlashni bajaradi, balki natijaviy ro'yxat turini ham to'g'ri `List<T>` (non-nullable) ga o'zgartiradi.

## Ishlash natijasi:
```text
Asl ro'yxat: [10, null, 20, null, 30, 40, null]
Tozalangan non-nullable ro'yxat: [10, 20, 30, 40]
```

# 97-Topshiriq: Dart 3 ning List.nonNulls kengaytmasi
## Topshiriq sharti:
Dart 3 da kiritilgan qulay `nonNulls` xususiyati orqali null qiymatlarni bitta so'z bilan filtrlang.

## Yechim (Dart kodi):
```dart
void main() {
  List<String?> shaharlar = ["Toshkent", null, "Samarqand", null, "Xiva"];

  // nonNulls metodi Dart 3 da mavjud
  var toza = shaharlar.nonNulls.toList();

  print("Tozalangan shaharlar: $toza (${toza.runtimeType})");
}
```

## Tushuntirish va Mantiq:
`collection.nonNulls` Dart 3 ning eng mashhur va ixcham xususiyatlaridan biridir.

## Ishlash natijasi:
```text
Tozalangan shaharlar: [Toshkent, Samarqand, Xiva] (List<String>)
```

# 98-Topshiriq: Map.putIfAbsent() va null qiymatlar
## Topshiriq sharti:
Lug'atda kalit bo'lmasa uni qo'shuvchi, agar mavjud bo'lsa o'zgartirmaydigan null-xavfsiz mantiqni yozing.

## Yechim (Dart kodi):
```dart
void main() {
  Map<String, int> hisoblar = {"Ali": 100};

  hisoblar.putIfAbsent("Ali", () => 500); // O'zgarmaydi, chunki bor
  hisoblar.putIfAbsent("Vali", () => 200); // Qo'shiladi

  print("Hisoblar: $hisoblar");
}
```

## Tushuntirish va Mantiq:
`putIfAbsent` kalit mavjudligini xavfsiz tekshiradi va ortiqcha qiymat hisoblash xarajatlarini tejaydi.

## Ishlash natijasi:
```text
Hisoblar: {Ali: 100, Vali: 200}
```

# 99-Topshiriq: Tashqi API dan kelgan xom ma'lumotlarni null-xavfsiz validatsiya qilish
## Topshiriq sharti:
Map ko'rinishidagi ma'lumotning har bir maydonini tekshirib, xavfsiz DTO (Data Transfer Object) ga o'tkazuvchi sinf yozing.

## Yechim (Dart kodi):
```dart
class FoydalanuvchiDTO {
  final int id;
  final String email;

  FoydalanuvchiDTO({required this.id, required this.email});

  factory FoydalanuvchiDTO.fromMap(Map<String, dynamic> map) {
    final id = map["id"];
    final email = map["email"];

    if (id is! int || email is! String) {
      throw FormatException("Ma'lumotlar to'liq emas yoki noto'g'ri turda!");
    }
    return FoydalanuvchiDTO(id: id, email: email);
  }
}

void main() {
  var xom = {"id": 1, "email": "info@uzbek.ai"};
  var user = FoydalanuvchiDTO.fromMap(xom);

  print("Foydalanuvchi muvaffaqiyatli yuklandi: ${user.id} -> ${user.email}");
}
```

## Tushuntirish va Mantiq:
Tashqi tarmoq ma'lumotlari (`dynamic`) Dart xotirasiga kirishida qat'iy tekshirilib, non-nullable turlarga o'tkazilishi xavfsizlikning oltin qoidasidir.

## Ishlash natijasi:
```text
Foydalanuvchi muvaffaqiyatli yuklandi: 1 -> info@uzbek.ai
```

# 100-Topshiriq: Katta amaliy xulosa: Null-xavfsiz foydalanuvchi profili va buyurtmalar tahlilchisi
## Topshiriq sharti:
100-topshiriq: Barcha o'rganilgan Null Safety imkoniyatlarini (`?.`, `??`, `late final`, non-nullable kolleksiyalar, extension) bitta to'liq, real-vaqt do'kon hisob-kitob dasturida birlashtiring.

## Yechim (Dart kodi):
```dart
class Buyurtma {
  final String id;
  final double summa;
  Buyurtma(this.id, this.summa);
}

class Mijoz {
  final String ism;
  final String? telefon;
  final List<Buyurtma>? buyurtmalar;
  late final double jamiXarajat;

  Mijoz({required this.ism, this.telefon, this.buyurtmalar}) {
    // null-aware va fold bilan xavfsiz hisoblash
    jamiXarajat = buyurtmalar?.fold<double>(0.0, (acc, b) => acc + b.summa) ?? 0.0;
  }

  void hisobotChopEt() {
    print("------------------------------------------");
    print("Mijoz: $ism");
    print("Aloqa: ${telefon ?? 'Kiritilmagan'}");
    print("Buyurtmalar soni: ${buyurtmalar?.length ?? 0} ta");
    print("Jami xarid summasi: $jamiXarajat so'm");
    print("------------------------------------------");
  }
}

void main() {
  var m1 = Mijoz(
    ism: "Farrux",
    telefon: "+998901234567",
    buyurtmalar: [
      Buyurtma("B-01", 150000),
      Buyurtma("B-02", 320000),
    ],
  );

  var m2 = Mijoz(
    ism: "Zuhra",
    buyurtmalar: null, // Buyurtmasi yo'q
  );

  m1.hisobotChopEt();
  m2.hisobotChopEt();
}
```

## Tushuntirish va Mantiq:
100-topshiriq orqali Dart tilining Sound Null Safety falsafasi amalda to'liq namoyon bo'ldi. Hech qanday kutilmagan null xatolarisiz toza va barqaror arxitektura yaratildi.

## Ishlash natijasi:
```text
------------------------------------------
Mijoz: Farrux
Aloqa: +998901234567
Buyurtmalar soni: 2 ta
Jami xarid summasi: 470000.0 so'm
------------------------------------------
------------------------------------------
Mijoz: Zuhra
Aloqa: Kiritilmagan
Buyurtmalar soni: 0 ta
Jami xarid summasi: 0.0 so'm
------------------------------------------
```

