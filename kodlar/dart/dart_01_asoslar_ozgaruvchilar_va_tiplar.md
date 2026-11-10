# 1-Qism: Dart Asoslari, O'zgaruvchilar va Ma'lumot Turlari (1-50)

Ushbu qismda Google Dart (Dart 3+) dasturlash tilining sintaksisi, o'zgaruvchilar e'lon qilish (`var`, `final`, `const`), asosiy turlar (`int`, `double`, `num`, `String`, `bool`), satr interpolatsiyasi va standart arifmetik amallar amaliy topshiriqlar bilan o'rganiladi.

# 1-Topshiriq: Dart da 'Salom, Dunyo!' va print() funksiyasi
## Topshiriq sharti:
Dart dasturining kirish nuqtasi bo'lgan `void main()` funksiyasini yozing va konsolga 'Assalomu alaykum, O'zbekiston!' jumlasini chiqaring.

## Yechim (Dart kodi):
```dart
void main() {
  print("Assalomu alaykum, O'zbekiston!");
}
```

## Tushuntirish va Mantiq:
Dart dasturlari har doim `main()` funksiyasidan boshlanadi. `print()` funksiyasi matnni ekranga chiqaradi va avtomatik yangi satrga o'tadi.

## Ishlash natijasi:
```text
Assalomu alaykum, O'zbekiston!
```

# 2-Topshiriq: var bilan o'zgaruvchilar e'lon qilish va Type Inference
## Topshiriq sharti:
`var` kalit so'zi yordamida matn, butun son va mantiqiy o'zgaruvchilar e'lon qiling hamda ularning `runtimeType` xususiyatini chop eting.

## Yechim (Dart kodi):
```dart
void main() {
  var til = "Dart";
  var versiya = 3;
  var zamonaviy = true;

  print("Til: $til (${til.runtimeType})");
  print("Versiya: $versiya (${versiya.runtimeType})");
  print("Zamonaviymi: $zamonaviy (${zamonaviy.runtimeType})");
}
```

## Tushuntirish va Mantiq:
Dart statik tiplangan til bo'lib, `var` yozilganda kompilyator berilgan dastlabki qiymatga qarab o'zgaruvchi turini (String, int, bool) o'zi avtomatik belgilaydi.

## Ishlash natijasi:
```text
Til: Dart (String)
Versiya: 3 (int)
Zamonaviymi: true (bool)
```

# 3-Topshiriq: int tipi bilan butun sonli hisob-kitoblar
## Topshiriq sharti:
Ikkita butun sonli `int` o'zgaruvchi yarating, ularning yig'indisi, ayirmasi, ko'paytmasi va o'rtacha qiymatini hisoblang.

## Yechim (Dart kodi):
```dart
void main() {
  int a = 25;
  int b = 10;

  int yigindi = a + b;
  int ayirma = a - b;
  int kopaytma = a * b;

  print("Yig'indi: $yigindi");
  print("Ayirma: $ayirma");
  print("Ko'paytma: $kopaytma");
}
```

## Tushuntirish va Mantiq:
`int` 64-bitli butun sonlarni ifodalaydi (tizimga qarab -2^63 dan 2^63 - 1 gacha). Arifmetik amallar aniq va tezkor bajariladi.

## Ishlash natijasi:
```text
Yig'indi: 35
Ayirma: 15
Ko'paytma: 250
```

# 4-Topshiriq: double tipi va suzuvchi vergulli hisob-kitoblar
## Topshiriq sharti:
Aylana radiusi `double r = 5.5` berilgan. Aylana uzunligi va yuzasini hisoblab chiqaring (pi = 3.14159).

## Yechim (Dart kodi):
```dart
void main() {
  double radius = 5.5;
  const double pi = 3.14159;

  double uzunlik = 2 * pi * radius;
  double yuza = pi * radius * radius;

  print("Radius: $radius");
  print("Aylana uzunligi: $uzunlik");
  print("Aylana yuzasi: $yuza");
}
```

## Tushuntirish va Mantiq:
`double` 64-bitli IEEE 754 suzuvchi vergulli kasr sonlarni ifodalash uchun xizmat qiladi.

## Ishlash natijasi:
```text
Radius: 5.5
Aylana uzunligi: 34.55749
Aylana yuzasi: 95.0330975
```

# 5-Topshiriq: num tipi: int va double uchun umumiy ota tur
## Topshiriq sharti:
`num` tipidagi o'zgaruvchi e'lon qiling, unga avval butun son, so'ngra kasr son yuklab, ikkala holatdagi qiymatini chop eting.

## Yechim (Dart kodi):
```dart
void main() {
  num x = 10; // Butun son
  print("x (butun): $x (tipi: ${x.runtimeType})");

  x = 10.75; // Kasr son
  print("x (kasr):  $x (tipi: ${x.runtimeType})");
}
```

## Tushuntirish va Mantiq:
`num` turi Dart da `int` va `double` turlarining umumiy super-klassi hisoblanadi. U ham butun, ham haqiqiy sonlarni qabul qila oladi.

## Ishlash natijasi:
```text
x (butun): 10 (tipi: int)
x (kasr):  10.75 (tipi: double)
```

# 6-Topshiriq: String tipi: Bir qatorli va Ko'p qatorli satrlar
## Topshiriq sharti:
Dart da bir tirnoqli (`'...'`), qo'sh tirnoqli (`"..."`) va uchta tirnoqli (`'''...'''`) ko'p qatorli matnlarni hosil qiling.

## Yechim (Dart kodi):
```dart
void main() {
  String s1 = 'Yakka tirnoqli satr';
  String s2 = "Qo'sh tirnoqli satr";
  String s3 = '''
Bu ko'p qatorli matn bo'lib,
unda yangi satrlar va format
o'z holicha saqlanib qoladi.
''';

  print(s1);
  print(s2);
  print(s3.trim());
}
```

## Tushuntirish va Mantiq:
Dart da yakka va qo'sh tirnoqlar teng kuchli. Uchta tirnoq (`'''` yoki `"""`) formatlangan uzun matnlar va she'rlarni yozish uchun qulay.

## Ishlash natijasi:
```text
Yakka tirnoqli satr
Qo'sh tirnoqli satr
Bu ko'p qatorli matn bo'lib,
unda yangi satrlar va format
o'z holicha saqlanib qoladi.
```

# 7-Topshiriq: Satr interpolatsiyasi: $name va ${expression}
## Topshiriq sharti:
Foydalanuvchi ismi, yoshi va maoshi berilgan bo'lsa, satr ichida `$ozgaruvchi` va murakkab ifodalar uchun `${arifmetika}` dan foydalaning.

## Yechim (Dart kodi):
```dart
void main() {
  String ism = "Anvar";
  int yosh = 24;
  double maosh = 4500000.0;

  print("Foydalanuvchi: $ism, Yoshi: $yosh");
  print("Yillik daromadi: ${maosh * 12} so'm");
  print("Keyingi yildagi yoshi: ${yosh + 1}");
}
```

## Tushuntirish va Mantiq:
Satr interpolatsiyasi `+` bilan qo'shishdan ancha toza va tezkor. Oddiy o'zgaruvchi uchun `$nom`, ifodalar uchun esa `${ifoda}` yoziladi.

## Ishlash natijasi:
```text
Foydalanuvchi: Anvar, Yoshi: 24
Yillik daromadi: 54000000.0 so'm
Keyingi yildagi yoshi: 25
```

# 8-Topshiriq: bool tipi va mantiqiy amallar
## Topshiriq sharti:
`bool` tipidagi `isStudent` va `hasDiscount` o'zgaruvchilarini e'lon qiling va ularning inkorini (`!`) chiqaring.

## Yechim (Dart kodi):
```dart
void main() {
  bool isStudent = true;
  bool hasDiscount = false;

  print("Talabami: $isStudent");
  print("Chegirma bormi: $hasDiscount");
  print("Talaba emasmi: ${!isStudent}");
}
```

## Tushuntirish va Mantiq:
`bool` faqat `true` yoki `false` qiymatlarini qabul qiladi. C/C++ dan farqli ravishda Dart da 0 yoki 1 sonlari bool o'rnida ishlatilmaydi (qat'iy tiplanganlik).

## Ishlash natijasi:
```text
Talabami: true
Chegirma bormi: false
Talaba emasmi: false
```

# 9-Topshiriq: final o'zgaruvchilar (Runtime konstantalar)
## Topshiriq sharti:
`final` yordamida dastur ishga tushganda joriy vaqtni (`DateTime.now()`) saqlang va uning qayta o'zgarmasligini tushuntiring.

## Yechim (Dart kodi):
```dart
void main() {
  final DateTime hozir = DateTime(2026, 11, 7, 18, 45);
  final String shahar = "Toshkent";

  print("Shahar: $shahar");
  print("Belgilangan vaqt: $hozir");
  // shahar = "Samarqand"; // XATOLIK: final o'zgaruvchini qayta o'zgartirib bo'lmaydi!
}
```

## Tushuntirish va Mantiq:
`final` o'zgaruvchiga qiymat bir marta beriladi. U dastur bajarilayotgan paytda (runtime) hisoblanishi mumkin, ammo keyin o'zgarmas qoladi.

## Ishlash natijasi:
```text
Shahar: Toshkent
Belgilangan vaqt: 2026-11-07 18:45:00.000
```

# 10-Topshiriq: const o'zgaruvchilar (Compile-time konstantalar)
## Topshiriq sharti:
`const` yordamida kompilyatsiya vaqtida qat'iy ma'lum bo'lgan doimiylarni (tezlik, yorug'lik tezligi, soliq foizi) e'lon qiling.

## Yechim (Dart kodi):
```dart
void main() {
  const double c = 299792458.0; // m/s yorug'lik tezligi
  const int soliqFoizi = 12;
  const String valyuta = "UZS";

  print("Yorug'lik tezligi: $c m/s");
  print("QQS stavkasi: $soliqFoizi%");
  print("Valyuta: $valyuta");
}
```

## Tushuntirish va Mantiq:
`const` qiymatlari dastur kompilyatsiya qilinayotgan vaqtdayoq xotirada qat'iy belgilanadi. Ular mutlaq o'zgarmas (deeply immutable) hisoblanadi.

## Ishlash natijasi:
```text
Yorug'lik tezligi: 299792458.0 m/s
QQS stavkasi: 12%
Valyuta: UZS
```

# 11-Topshiriq: final va const farqini amalda ko'rsatish
## Topshiriq sharti:
`final` bilan `const` ning asosiy farqini tushuntiruvchi kod yozing.

## Yechim (Dart kodi):
```dart
void main() {
  // final: qiymati runtime paytida aniqlanishi mumkin
  final DateTime runtimeConst = DateTime(2026, 1, 1);

  // const: qiymati faqat kompilyatsiya vaqtida ma'lum bo'lishi shart
  const int compileConst = 100 * 20;

  print("final qiymat: $runtimeConst");
  print("const qiymat: $compileConst");
}
```

## Tushuntirish va Mantiq:
`const` doimiylari har doim `final` hisoblanadi, lekin `final` har doim ham `const` bo'la olmaydi. `const` xotirada kanoniklashtiriladi (bir xil const ob'ektlar bitta xotira manzilini ulashadi).

## Ishlash natijasi:
```text
final qiymat: 2026-01-01 00:00:00.000
const qiymat: 2000
```

# 12-Topshiriq: Arifmetik operatorlar: +, -, *, /, ~/, %
## Topshiriq sharti:
Dart da ikkita son ustida 6 ta arifmetik amalni (shu jumladan butunli bo'lish `~/` va qoldiq `%`) bajaring.

## Yechim (Dart kodi):
```dart
void main() {
  int a = 17;
  int b = 5;

  print("Qo'shish (+): $a + $b = ${a + b}");
  print("Ayirish (-):  $a - $b = ${a - b}");
  print("Ko'paytirish (*): $a * $b = ${a * b}");
  print("Oddiy bo'lish (/): $a / $b = ${a / b}");
  print("Butunli bo'lish (~/): $a ~/ $b = ${a ~/ b}");
  print("Qoldiq (%):   $a % $b = ${a % b}");
}
```

## Tushuntirish va Mantiq:
Dart da oddiy `/` operatori ikkita butun son bo'linganda ham har doim `double` qaytaradi. Butun natija olish uchun maxsus `~/` operatori ishlatiladi.

## Ishlash natijasi:
```text
Qo'shish (+): 17 + 5 = 22
Ayirish (-):  17 - 5 = 12
Ko'paytirish (*): 17 * 5 = 85
Oddiy bo'lish (/): 17 / 5 = 3.4
Butunli bo'lish (~/): 17 ~/ 5 = 3
Qoldiq (%):   17 % 5 = 2
```

# 13-Topshiriq: ~/ butunli bo'lish operatori va oddiy / farqi
## Topshiriq sharti:
Sekundlarni soat, daqiqa va soniyalarga ajratishda `~/` va `%` amallarini qo'llang.

## Yechim (Dart kodi):
```dart
void main() {
  int jamiSekund = 3725;

  int soat = jamiSekund ~/ 3600;
  int qoldiq = jamiSekund % 3600;
  int daqiqa = qoldiq ~/ 60;
  int soniya = qoldiq % 60;

  print("$jamiSekund soniya = $soat soat, $daqiqa daqiqa, $soniya soniya");
}
```

## Tushuntirish va Mantiq:
`~/` butunli bo'lish va `%` qoldiq amali vaqt va o'lchov birliklarini maydalashda eng asosiy vositadir.

## Ishlash natijasi:
```text
3725 soniya = 1 soat, 2 daqiqa, 5 soniya
```

# 14-Topshiriq: Increment va Decrement: Prefiks va Postfiks
## Topshiriq sharti:
O'zgaruvchini `++x`, `x++`, `--x`, `x--` ko'rinishida oshirish va kamaytirishning hisoblash tartibidagi farqini ko'rsating.

## Yechim (Dart kodi):
```dart
void main() {
  int x = 5;
  print("Asl x: $x");

  int post = x++; // Avval qiymat uzatiladi, keyin oshadi
  print("Postfiks x++ natijasi: $post, yangi x: $x");

  int pre = ++x; // Avval oshadi, keyin qiymat uzatiladi
  print("Prefiks ++x natijasi: $pre, yangi x: $x");
}
```

## Tushuntirish va Mantiq:
Prefiks ko'rinishida (`++x`) o'zgaruvchi darhol oshiriladi va yangi qiymat ifodada ishlatiladi. Postfiksda (`x++`) esa ifodaga eski qiymat beriladi, o'zgaruvchining o'zi esa keyin oshadi.

## Ishlash natijasi:
```text
Asl x: 5
Postfiks x++ natijasi: 5, yangi x: 6
Prefiks ++x natijasi: 7, yangi x: 7
```

# 15-Topshiriq: Birikmali tayinlash operatorlari (+=, -=, *=, /=)
## Topshiriq sharti:
Balans hisoblagichida birikmali operatorlarni qo'llang.

## Yechim (Dart kodi):
```dart
void main() {
  double balans = 100000.0;
  print("Boshlang'ich balans: $balans");

  balans += 50000.0; // Kirim
  print("50000 qo'shilgach: $balans");

  balans -= 30000.0; // Chiqim
  print("30000 yechilgach: $balans");

  balans *= 1.1; // 10% bonus
  print("10% bonus bilan: $balans");
}
```

## Tushuntirish va Mantiq:
Birikmali operatorlar kodni ixchamlashtiradi: `balans += 50` ifodasi `balans = balans + 50` ga tengdir.

## Ishlash natijasi:
```text
Boshlang'ich balans: 100000.0
50000 qo'shilgach: 150000.0
30000 yechilgach: 120000.0
10% bonus bilan: 132000.0
```

# 16-Topshiriq: Satrlarni birlashtirish (String Concatenation)
## Topshiriq sharti:
Satrlarni `+` operatori va shunchaki yonma-yon qo'yish orqali birlashtirishni bajaring.

## Yechim (Dart kodi):
```dart
void main() {
  String s1 = "O'zbekiston ";
  String s2 = "Respublikasi";

  String res1 = s1 + s2;
  String res2 = "Sun'iy " 'Intellekt ' "Kelajagi"; // Yonma-yon yozish

  print(res1);
  print(res2);
}
```

## Tushuntirish va Mantiq:
Dart da yonma-yon qo'yilgan satr literallari avtomatik birlashadi, bu uzun matnlarni bir nechta satrga bo'lib yozishda juda qulay.

## Ishlash natijasi:
```text
O'zbekiston Respublikasi
Sun'iy Intellekt Kelajagi
```

# 17-Topshiriq: Satr uzunligi (length) va bo'shligini tekshirish (isEmpty, isNotEmpty)
## Topshiriq sharti:
Satrning belgilar sonini `length` bilan hisoblang va uning bo'sh yoki bo'sh emasligini tekshiring.

## Yechim (Dart kodi):
```dart
void main() {
  String matn = "Toshkent - go'zal shahar";
  String bosh = "";

  print("Matn: '$matn'");
  print("Uzunligi: ${matn.length} ta belgi");
  print("Bo'shmi: ${matn.isEmpty}");
  print("Bo'sh emasmi: ${matn.isNotEmpty}");

  print("Bo'sh satr isEmpty: ${bosh.isEmpty}");
}
```

## Tushuntirish va Mantiq:
`length` satrdagi UTF-16 kod birliklari sonini qaytaradi. `isEmpty` esa `length == 0` dan tezroq va qulayroq ishlaydi.

## Ishlash natijasi:
```text
Matn: 'Toshkent - go'zal shahar'
Uzunligi: 24 ta belgi
Bo'shmi: false
Bo'sh emasmi: true
Bo'sh satr isEmpty: true
```

# 18-Topshiriq: Satr harflarini o'zgartirish: toUpperCase() va toLowerCase()
## Topshiriq sharti:
Satrni butunlay bosh harflarga va kichik harflarga o'giring.

## Yechim (Dart kodi):
```dart
void main() {
  String shior = "Bilim - Kuchdir!";

  print("Katta harflar: ${shior.toUpperCase()}");
  print("Kichik harflar: ${shior.toLowerCase()}");
}
```

## Tushuntirish va Mantiq:
`toUpperCase()` va `toLowerCase()` yangi o'zgartirilgan satr qaytaradi, chunki Dart da satrlar o'zgarmas (immutable) ob'ektlardir.

## Ishlash natijasi:
```text
Katta harflar: BILIM - KUCHDIR!
Kichik harflar: bilim - kuchdir!
```

# 19-Topshiriq: Satr qismini kesib olish: substring()
## Topshiriq sharti:
Berilgan satrdan boshlang'ich va oxirgi indekslar bo'yicha qism satrni ajratib oling.

## Yechim (Dart kodi):
```dart
void main() {
  String sana = "2026-11-07";

  String yil = sana.substring(0, 4);
  String oy = sana.substring(5, 7);
  String kun = sana.substring(8);

  print("Yil: $yil, Oy: $oy, Kun: $kun");
}
```

## Tushuntirish va Mantiq:
`substring(start, end)` metodi `start` indeksidan `end - 1` gacha bo'lgan qismni kesib oladi. Agar `end` ko'rsatilmasa, satr oxirigacha oladi.

## Ishlash natijasi:
```text
Yil: 2026, Oy: 11, Kun: 07
```

# 20-Topshiriq: Satrda qidirish: contains(), startsWith(), endsWith()
## Topshiriq sharti:
Matnda muayyan so'z borligini, u qanday so'z bilan boshlanishi va tugashini tekshiruvchi dastur yozing.

## Yechim (Dart kodi):
```dart
void main() {
  String fayl = "hisobot_2026.pdf";

  print("'.pdf' bilan tugaydimi: ${fayl.endsWith('.pdf')}");
  print("'hisobot' bilan boshlanadimi: ${fayl.startsWith('hisobot')}");
  print("'2026' ni o'z ichiga oladimi: ${fayl.contains('2026')}");
  print("'doc' bormi: ${fayl.contains('doc')}");
}
```

## Tushuntirish va Mantiq:
Ushbu metodlar fayl kengaytmasini, URL manzillarini yoki qidiruv so'zlarini tekshirishda juda qulay mantiqiy (`bool`) javob beradi.

## Ishlash natijasi:
```text
'.pdf' bilan tugaydimi: true
'hisobot' bilan boshlanadimi: true
'2026' ni o'z ichiga oladimi: true
'doc' bormi: false
```

# 21-Topshiriq: Satr ichidagi so'zlarni almashtirish: replaceAll()
## Topshiriq sharti:
Matndagi barcha nuqtalarni chiziqcha bilan va 'yomon' so'zini 'yaxshi' bilan almashtiring.

## Yechim (Dart kodi):
```dart
void main() {
  String matn = "Bugun havo yomon. Ertaga ham yomon bo'lishi mumkin.";
  String yangiMatn = matn.replaceAll("yomon", "yaxshi");

  print("Asl matn:   $matn");
  print("Almashgan:  $yangiMatn");
}
```

## Tushuntirish va Mantiq:
`replaceAll()` belgilangan barcha mosliklarni yangi satrga almashtiradi. Birinchi uchraganini almashtirish uchun esa `replaceFirst()` ishlatiladi.

## Ishlash natijasi:
```text
Asl matn:   Bugun havo yomon. Ertaga ham yomon bo'lishi mumkin.
Almashgan:  Bugun havo yaxshi. Ertaga ham yaxshi bo'lishi mumkin.
```

# 22-Topshiriq: Satrni bo'laklarga ajratish: split()
## Topshiriq sharti:
Vergul bilan ajratilgan mevalar ro'yxatini alohida elementlarga ajratib, ro'yxat sifatida chop eting.

## Yechim (Dart kodi):
```dart
void main() {
  String mevalarSatr = "Olma,Anor,Uzum,Shaftoli,Nok";
  List<String> mevalar = mevalarSatr.split(",");

  print("Mevalar soni: ${mevalar.length}");
  for (int i = 0; i < mevalar.length; ++i) {
    print("${i + 1}. ${mevalar[i]}");
  }
}
```

## Tushuntirish va Mantiq:
`split(separator)` metodi satrni berilgan ajratuvchi bo'yicha bo'lib, `List<String>` ro'yxatini hosil qiladi.

## Ishlash natijasi:
```text
Mevalar soni: 5
1. Olma
2. Anor
3. Uzum
4. Shaftoli
5. Nok
```

# 23-Topshiriq: Bo'shliqlarni tozalash: trim(), trimLeft(), trimRight()
## Topshiriq sharti:
Foydalanuvchi kiritgan satr boshidagi va oxiridagi keraksiz bo'shliqlarni tozalang.

## Yechim (Dart kodi):
```dart
void main() {
  String kirish = "   Salom, dunyo!    ";

  print("Asl:  '${kirish}' (uzunligi: ${kirish.length})");
  print("Trim: '${kirish.trim()}' (uzunligi: ${kirish.trim().length})");
  print("Chap: '${kirish.trimLeft()}'");
  print("O'ng: '${kirish.trimRight()}'");
}
```

## Tushuntirish va Mantiq:
`trim()` matn kiritish maydonlaridagi (masalan login yoki email) tasodifiy bo'shliqlarni olib tashlashda shart hisoblanadi.

## Ishlash natijasi:
```text
Asl:  '   Salom, dunyo!    ' (uzunligi: 20)
Trim: 'Salom, dunyo!' (uzunligi: 13)
Chap: 'Salom, dunyo!    '
O'ng: '   Salom, dunyo!'
```

# 24-Topshiriq: int.parse(): Satrni butun songa aylantirish
## Topshiriq sharti:
`String` turidagi sonni `int.parse()` yordamida haqiqiy butun songa aylantiring va arifmetik amal bajaring.

## Yechim (Dart kodi):
```dart
void main() {
  String satrSon = "1250";
  int son = int.parse(satrSon);

  int natija = son + 250;
  print("Aylantirilgan son: $son");
  print("Hisoblangan natija: $natija");
}
```

## Tushuntirish va Mantiq:
`int.parse()` satrni butun son sifatida tahlil qiladi. Agar satrda harf yoki noqonuniy belgi bo'lsa, `FormatException` istisnosi yuzaga keladi.

## Ishlash natijasi:
```text
Aylantirilgan son: 1250
Hisoblangan natija: 1500
```

# 25-Topshiriq: double.parse(): Satrni o'nlik songa aylantirish
## Topshiriq sharti:
`String` dagi kasr sonni `double.parse()` orqali o'nlik songa o'tkazing va soliqni hisoblang.

## Yechim (Dart kodi):
```dart
void main() {
  String narxSatr = "89.99";
  double narx = double.parse(narxSatr);

  double jami = narx * 1.15; // 15% ustama bilan
  print("Mahsulot narxi: $narx");
  print("Jami summa: $jami");
}
```

## Tushuntirish va Mantiq:
`double.parse()` nuqta bilan ajratilgan kasr sonli satrlarni `double` ga xatosiz o'giradi.

## Ishlash natijasi:
```text
Mahsulot narxi: 89.99
Jami summa: 103.4885
```

# 26-Topshiriq: int.tryParse(): Xatoliksiz xavfsiz konvertatsiya
## Topshiriq sharti:
Satr to'g'ri son bo'lmasa dastur to'xtab qolmasdan `null` qaytaruvchi `int.tryParse()` funksiyasini qo'llang.

## Yechim (Dart kodi):
```dart
void main() {
  String yaxshiSatr = "450";
  String yomonSatr = "450abc";

  int? son1 = int.tryParse(yaxshiSatr);
  int? son2 = int.tryParse(yomonSatr);

  print("Son 1: $son1");
  print("Son 2: $son2 (xato bo'lgani uchun null)");

  // Standart qiymat bilan ishlatish
  int xavfsizSon = son2 ?? 0;
  print("Xavfsiz natija: $xavfsizSon");
}
```

## Tushuntirish va Mantiq:
`int.tryParse()` xatolik yuz berganda `FormatException` tashlamaydi, balki xavfsiz `null` qaytaradi. Bu foydalanuvchi ma'lumotlarini qabul qilishda qulashlarning oldini oladi.

## Ishlash natijasi:
```text
Son 1: 450
Son 2: null (xato bo'lgani uchun null)
Xavfsiz natija: 0
```

# 27-Topshiriq: Sonni satrga aylantirish: toString()
## Topshiriq sharti:
Har qanday turdagi sonni `toString()` orqali `String` matniga aylantiring.

## Yechim (Dart kodi):
```dart
void main() {
  int yosh = 30;
  double ogirlik = 72.5;

  String s1 = yosh.toString();
  String s2 = ogirlik.toString();

  print("s1: '$s1' (${s1.runtimeType})");
  print("s2: '$s2' (${s2.runtimeType})");
}
```

## Tushuntirish va Mantiq:
Dart da hamma narsa ob'ekt bo'lgani sababli, oddiy `int` va `double` ham o'zining `toString()` metodiga ega.

## Ishlash natijasi:
```text
s1: '30' (String)
s2: '72.5' (String)
```

# 28-Topshiriq: Kasr sonlarni aniq xonagacha yaxlitlash: toStringAsFixed()
## Topshiriq sharti:
Katta kasr sonni verguldan keyin aniq 2 ta xona bilan yaxlitlab satr ko'rinishida oling.

## Yechim (Dart kodi):
```dart
void main() {
  double narx = 12.34567;
  double foiz = 0.8888;

  print("2 xona bilan narx: ${narx.toStringAsFixed(2)}");
  print("1 xona bilan narx: ${narx.toStringAsFixed(1)}");
  print("3 xona bilan foiz: ${foiz.toStringAsFixed(3)}");
}
```

## Tushuntirish va Mantiq:
`toStringAsFixed(n)` moliyaviy hisob-kitoblar va valyutalarni ko'rsatishda eng ko'p ishlatiladigan metoddir.

## Ishlash natijasi:
```text
2 xona bilan narx: 12.35
1 xona bilan narx: 12.3
3 xona bilan foiz: 0.889
```

# 29-Topshiriq: Sonning mutlaq qiymati (abs) va ishorasi (sign)
## Topshiriq sharti:
Manfiy va musbat sonlarning modulini (`abs()`) va ishora indikatorini (`sign`) chiqaring.

## Yechim (Dart kodi):
```dart
void main() {
  int manfiy = -25;
  double musbat = 40.5;
  int nol = 0;

  print("-25 ning moduli: ${manfiy.abs()}");
  print("Ishoralar: manfiy=${manfiy.sign}, musbat=${musbat.sign}, nol=${nol.sign}");
}
```

## Tushuntirish va Mantiq:
`abs()` har doim musbat qiymat qaytaradi. `sign` esa son musbat bo'lsa 1, manfiy bo'lsa -1, nol bo'lsa 0 qiymatini beradi.

## Ishlash natijasi:
```text
-25 ning moduli: 25
Ishoralar: manfiy=-1, musbat=1.0, nol=0
```

# 30-Topshiriq: Yaxlitlash metodlari: round(), floor(), ceil(), truncate()
## Topshiriq sharti:
Bitta kasr son ustida 4 ta turlicha yaxlitlash amallarini bajaring va farqlarini taqqoslang.

## Yechim (Dart kodi):
```dart
void main() {
  double son = 4.7;

  print("Asl son: $son");
  print("round() (matematik yaxlitlash): ${son.round()}");
  print("floor() (pastga yaxlitlash):     ${son.floor()}");
  print("ceil()  (yuqoriga yaxlitlash):    ${son.ceil()}");
  print("truncate() (kasrni kesish):       ${son.truncate()}");
}
```

## Tushuntirish va Mantiq:
`round()` eng yaqin butun songa yaxlitlaydi; `floor()` eng yaqin kichik butun sonni oladi; `ceil()` eng yaqin katta butun sonni oladi; `truncate()` esa kasr qismini shunchaki olib tashlaydi.

## Ishlash natijasi:
```text
Asl son: 4.7
round() (matematik yaxlitlash): 5
floor() (pastga yaxlitlash):     4
ceil()  (yuqoriga yaxlitlash):    5
truncate() (kasrni kesish):       4
```

# 31-Topshiriq: clamp() metodi bilan qiymatni chegaralash
## Topshiriq sharti:
O'zgaruvchi qiymatini belgilangan minimal va maksimal oraliqda cheklovchi `clamp(min, max)` metodini qo'llang.

## Yechim (Dart kodi):
```dart
void main() {
  int ovozBaladligi = 120; // 0 dan 100 gacha bo'lishi kerak
  int cheklangan1 = ovozBaladligi.clamp(0, 100);

  int judaPast = -15;
  int cheklangan2 = judaPast.clamp(0, 100);

  int normal = 75;
  int cheklangan3 = normal.clamp(0, 100);

  print("120 cheklovi: $cheklangan1");
  print("-15 cheklovi: $cheklangan2");
  print("75 cheklovi:  $cheklangan3");
}
```

## Tushuntirish va Mantiq:
`clamp()` kiritilgan qiymat berilgan oraliqdan chiqib ketmasligini ta'minlaydi (UI slayderlar, ovoz balandligi, rang parametrlari uchun juda qulay).

## Ishlash natijasi:
```text
120 cheklovi: 100
-15 cheklovi: 0
75 cheklovi:  75
```

# 32-Topshiriq: dart:math kutubxonasi: pow() va sqrt()
## Topshiriq sharti:
`dart:math` kutubxonasini import qilib, sonning darajasini (`pow`) va kvadrat ildizini (`sqrt`) hisoblang.

## Yechim (Dart kodi):
```dart
import 'dart:math';

void main() {
  num daraja = pow(2, 8); // 2^8
  double ildiz = sqrt(64); // ildiz(64)

  print("2^8 = $daraja");
  print("sqrt(64) = $ildiz");
  print("Pifagor (3, 4 gipotenuza): ${sqrt(pow(3, 2) + pow(4, 2))}");
}
```

## Tushuntirish va Mantiq:
`dart:math` standart matematik konstantalar (`pi`, `e`) va trigonometrik/daraja funksiyalarini taqdim etadi.

## Ishlash natijasi:
```text
2^8 = 256
sqrt(64) = 8.0
Pifagor (3, 4 gipotenuza): 5.0
```

# 33-Topshiriq: dart:math kutubxonasi: Random orqali tasodifiy sonlar
## Topshiriq sharti:
`Random` klassidan foydalanib, 1 dan 10 gacha bo'lgan tasodifiy butun son va [0, 1) oraliqdagi kasr son oling.

## Yechim (Dart kodi):
```dart
import 'dart:math';

void main() {
  Random rnd = Random(42); // Deterministik seed bilan

  int tasodifiyButun = rnd.nextInt(10) + 1; // 1 dan 10 gacha
  double tasodifiyKasr = rnd.nextDouble(); // 0.0 dan 1.0 gacha
  bool tasodifiyBool = rnd.nextBool();

  print("Tasodifiy butun (1..10): $tasodifiyButun");
  print("Tasodifiy kasr: $tasodifiyKasr");
  print("Tasodifiy bool: $tasodifiyBool");
}
```

## Tushuntirish va Mantiq:
`Random.nextInt(max)` 0 dan `max - 1` gacha butun son beradi. Deterministik sinovlar uchun unga `seed` kiritish mumkin.

## Ishlash natijasi:
```text
Tasodifiy butun (1..10): 4
Tasodifiy kasr: 0.6974052989714856
Tasodifiy bool: true
```

# 34-Topshiriq: Mantiqiy operatorlar: && (AND), || (OR), ! (NOT)
## Topshiriq sharti:
Kirish ruxsatini foydalanuvchi yoshi va paroli to'g'riligi bo'yicha mantiqiy operatorlar bilan tekshiring.

## Yechim (Dart kodi):
```dart
void main() {
  int yosh = 20;
  bool parolTogri = true;
  bool bloklangan = false;

  bool kirishRuxsati = (yosh >= 18 && parolTogri) && !bloklangan;
  print("Tizimga kirish mumkinmi: $kirishRuxsati");

  bool imtiyoz = (yosh < 7 || yosh >= 65);
  print("Bepul imtiyoz bormi: $imtiyoz");
}
```

## Tushuntirish va Mantiq:
`&&` har ikki shart to'g'ri bo'lsagina true beradi; `||` kamida bittasi to'g'ri bo'lsa true beradi; `!` esa qiymatni teskarisiga o'giradi.

## Ishlash natijasi:
```text
Tizimga kirish mumkinmi: true
Bepul imtiyoz bormi: false
```

# 35-Topshiriq: Solishtirish operatorlari: ==, !=, >, <, >=, <=
## Topshiriq sharti:
Ikkita sonni solishtirib, barcha relatsion operatorlarning mantiqiy javoblarini chiqaring.

## Yechim (Dart kodi):
```dart
void main() {
  int a = 15;
  int b = 20;

  print("$a == $b: ${a == b}");
  print("$a != $b: ${a != b}");
  print("$a > $b:  ${a > b}");
  print("$a < $b:  ${a < b}");
  print("$a >= 15: ${a >= 15}");
  print("$b <= 20: ${b <= 20}");
}
```

## Tushuntirish va Mantiq:
Solishtirish operatorlari doim `bool` qiymat qaytaradi va shartli operatorlarning asosi hisoblanadi.

## Ishlash natijasi:
```text
15 == 20: false
15 != 20: true
15 > 20:  false
15 < 20:  true
15 >= 15: true
20 <= 20: true
```

# 36-Topshiriq: identical() funksiyasi: Xotiradagi ayni ob'ektni tekshirish
## Topshiriq sharti:
Ikkita satr yoki ro'yxatning qiymatlari tengligi (`==`) bilan xotiradagi aynan bitta manzil ekanligi (`identical`) farqini ko'rsating.

## Yechim (Dart kodi):
```dart
void main() {
  const s1 = "Dart";
  const s2 = "Dart";
  print("const satrlar identical: ${identical(s1, s2)}");

  var list1 = [1, 2];
  var list2 = [1, 2];
  print("list1 == list2 (qiymat): ${list1 == list2}");
  print("list1 va list2 identical: ${identical(list1, list2)}");

  var list3 = list1;
  print("list1 va list3 identical: ${identical(list1, list3)}");
}
```

## Tushuntirish va Mantiq:
`identical(a, b)` ikki ko'rsatkich xotiradagi aynan bitta ob'ektga ishora qilayotganini tekshiradi.

## Ishlash natijasi:
```text
const satrlar identical: true
list1 == list2 (qiymat): false
list1 va list2 identical: false
list1 va list3 identical: true
```

# 37-Topshiriq: is va is! operatorlari: Ob'ekt tipini tekshirish
## Topshiriq sharti:
O'zgaruvchining qaysi ma'lumot turiga tegishli ekanligini `is` va `is!` orqali tekshiring.

## Yechim (Dart kodi):
```dart
void main() {
  dynamic qiymat = "O'zbek tili";

  if (qiymat is String) {
    print("Qiymat satr ekan, uzunligi: ${qiymat.length}");
  }

  if (qiymat is! int) {
    print("Qiymat butun son emas!");
  }
}
```

## Tushuntirish va Mantiq:
`is` operatori tekshirilgandan so'ng, Dart avtomatik ravishda turga moslashtirish (type promotion) bajaradi va xususiyatlaridan to'g'ridan-to'g'ri foydalanishga ruxsat beradi.

## Ishlash natijasi:
```text
Qiymat satr ekan, uzunligi: 11
Qiymat butun son emas!
```

# 38-Topshiriq: as operatori: Tipni majburiy o'zgartirish (Type Casting)
## Topshiriq sharti:
Umumiy turdagi o'zgaruvchini aniq turga `as` orqali keltiring.

## Yechim (Dart kodi):
```dart
void main() {
  Object obyekt = "Flutter va Dart";

  // String ga majburiy aylantirish
  String matn = obyekt as String;
  print("Matn uzunligi: ${matn.length}");
}
```

## Tushuntirish va Mantiq:
`as` operatori faqat ob'ekt haqiqatdan ham o'sha turga mansub bo'lgandagina ishlaydi, aks holda `TypeError` beradi. Shuning uchun oldin `is` bilan tekshirish tavsiya etiladi.

## Ishlash natijasi:
```text
Matn uzunligi: 15
```

# 39-Topshiriq: dynamic tipi va undan foydalanish oqibatlari
## Topshiriq sharti:
`dynamic` o'zgaruvchisiga dastlab son, keyin matn, so'ngra ro'yxat yuklab uning moslashuvchanligini va statik tekshiruvning o'chirilishini ko'rsating.

## Yechim (Dart kodi):
```dart
void main() {
  dynamic d = 100;
  print("d son: $d (${d.runtimeType})");

  d = "Matnli ma'lumot";
  print("d matn: $d (${d.runtimeType})");

  d = [1, 2, 3];
  print("d ro'yxat: $d (${d.runtimeType})");
}
```

## Tushuntirish va Mantiq:
`dynamic` tipi kompilyatorning barcha tekshiruvlarini o'chiradi. Undan noo'rin foydalanish runtime paytida dastur qulashiga olib kelishi mumkin.

## Ishlash natijasi:
```text
d son: 100 (int)
d matn: Matnli ma'lumot (String)
d ro'yxat: [1, 2, 3] (List<int>)
```

# 40-Topshiriq: Object tipi: Barcha turlarning umumiy ildizi
## Topshiriq sharti:
`Object` turidagi o'zgaruvchi yarating va `dynamic` dan farqli ravishda unda faqat `Object` metodlariga (`toString`, `hashCode`) ruxsat berilishini ko'rsating.

## Yechim (Dart kodi):
```dart
void main() {
  Object obj = "Salom";
  print("obj: $obj");
  print("hashCode: ${obj.hashCode}");
  print("toString(): ${obj.toString()}");
}
```

## Tushuntirish va Mantiq:
`Object` Dart tip ierarxiyasining eng yuqori ildizidir. `dynamic` dan farqli ravishda `Object` xavfsizdir va kompilyator unga mavjud bo'lmagan metodlarni chaqirishga yo'l qo'ymaydi.

## Ishlash natijasi:
```text
obj: Salom
hashCode: 157291778
toString(): Salom
```

# 41-Topshiriq: dynamic va Object farqini tushuntirish
## Topshiriq sharti:
`Object` va `dynamic` orasidagi farqni solishtiruvchi misol yozing.

## Yechim (Dart kodi):
```dart
void main() {
  dynamic d = "Salom";
  Object o = "Salom";

  // dynamic da kompilyator ixtiyoriy metod chaqiruviga ruxsat beradi
  print("dynamic uzunligi: ${d.length}");

  // Object da esa to'g'ridan-to'g'ri .length ga ruxsat berilmaydi, cast kerak:
  if (o is String) {
    print("Object uzunligi (cast qilingach): ${o.length}");
  }
}
```

## Tushuntirish va Mantiq:
`dynamic` = statik tekshirish yo'q (har qanday metod yozsa bo'ladi, xato runtime da chiqadi). `Object` = qat'iy statik tekshiruv bor, metod chaqirish uchun oldin `is` bilan tekshirish kerak.

## Ishlash natijasi:
```text
dynamic uzunligi: 5
Object uzunligi (cast qilingach): 5
```

# 42-Topshiriq: Runes va Unicode belgilari (Emoji va Maxsus belgilar)
## Topshiriq sharti:
Dart da Unicode kod birliklari (Runes) orqali emoji va bayroqlarni ekranga chiqaring.

## Yechim (Dart kodi):
```dart
void main() {
  Runes emoji = Runes('\u{1F600} \u{1F680} \u{1F1FA}\u{1F1FF}'); // Kulgi, Raketa, O'zbekiston bayrog'i
  String matn = String.fromCharCodes(emoji);

  print("Unicode simvollari: $matn");
}
```

## Tushuntirish va Mantiq:
Dart satrlari UTF-16 dan iborat. Emojilar kabi 16-bitdan katta belgilarni to'g'ri ifodalash uchun `Runes` (32-bitli kod nuqtalari) ishlatiladi.

## Ishlash natijasi:
```text
Unicode simvollari: 😀 🚀 🇺🇿
```

# 43-Topshiriq: StringBuffer yordamida satrlarni samarali yig'ish
## Topshiriq sharti:
Sikl ichida yuzlab satrlarni `+` bilan qo'shish o'rniga `StringBuffer` orqali yuqori unumdorlikda matn yig'uvchi kod yozing.

## Yechim (Dart kodi):
```dart
void main() {
  StringBuffer sb = StringBuffer();

  sb.write("Raqamlar: ");
  for (int i = 1; i <= 5; ++i) {
    sb.write("$i ");
  }
  sb.writeln("!");

  print(sb.toString().trim());
}
```

## Tushuntirish va Mantiq:
`+` operatori har gal yangi satr ob'ektini yaratib xotirani band qiladi. `StringBuffer` esa buferda bitta xotira maydonida yig'ib boradi (O(N) xotira samaradorligi).

## Ishlash natijasi:
```text
Raqamlar: 1 2 3 4 5 !
```

# 44-Topshiriq: Satrni to'ldirish: padLeft() va padRight()
## Topshiriq sharti:
Sonlarni ikki xonali formatda (masalan, 01, 02, 09) yoki jadval ustunlarini to'ldirish uchun `padLeft` va `padRight` metodlaridan foydalaning.

## Yechim (Dart kodi):
```dart
void main() {
  for (int i = 1; i <= 5; ++i) {
    String formatlangan = i.toString().padLeft(2, '0');
    print("Token ID: $formatlangan");
  }

  String nom = "Dart";
  print("O'ngdan to'ldirish: '${nom.padRight(8, '.')}'");
}
```

## Tushuntirish va Mantiq:
`padLeft(width, padding)` va `padRight` satr uzunligini belgilangan o'lchamgacha maxsus belgilar bilan to'ldiradi.

## Ishlash natijasi:
```text
Token ID: 01
Token ID: 02
Token ID: 03
Token ID: 04
Token ID: 05
O'ngdan to'ldirish: 'Dart....'
```

# 45-Topshiriq: Bitwise operatorlar: &, |, ^, ~, <<, >>
## Topshiriq sharti:
Dart da ikkita butun son ustida bitli amallarni bajaring va natijalarni chop eting.

## Yechim (Dart kodi):
```dart
void main() {
  int a = 12; // 1100b
  int b = 10; // 1010b

  print("a & b (AND):  ${a & b}");  // 1000b (8)
  print("a | b (OR):   ${a | b}");  // 1110b (14)
  print("a ^ b (XOR):  ${a ^ b}");  // 0110b (6)
  print("~a (NOT):     ${~a}");     // -13
  print("a << 1 (SHL): ${a << 1}"); // 24
  print("a >> 1 (SHR): ${a >> 1}"); // 6
}
```

## Tushuntirish va Mantiq:
Dart da bit amallari to'g'ridan-to'g'ri protsessorning arifmetik mantiqiy blokida (ALU) 1 taktda bajariladi.

## Ishlash natijasi:
```text
a & b (AND):  8
a | b (OR):   14
a ^ b (XOR):  6
~a (NOT):     -13
a << 1 (SHL): 24
a >> 1 (SHR): 6
```

# 46-Topshiriq: 2 ning darajasini tekshirish: (x & (x - 1)) == 0
## Topshiriq sharti:
Berilgan son 2 ning darajasi ekanligini bitli ko'paytma orqali O(1) da tekshiruvchi kod yozing.

## Yechim (Dart kodi):
```dart
bool isPowerOfTwo(int n) {
  return n > 0 && (n & (n - 1)) == 0;
}

void main() {
  for (int x in [0, 1, 2, 4, 7, 16, 31, 64]) {
    print("$x soni 2 ning darajasimi: ${isPowerOfTwo(x)}");
  }
}
```

## Tushuntirish va Mantiq:
2 ning darajalari binar ko'rinishda faqat bitta 1 ga ega. 1 ayrilganda barcha quyi bitlar 1 bo'ladi va ularning `&` ko'paytmasi nolga tenglashadi.

## Ishlash natijasi:
```text
0 soni 2 ning darajasimi: false
1 soni 2 ning darajasimi: true
2 soni 2 ning darajasimi: true
4 soni 2 ning darajasimi: true
7 soni 2 ning darajasimi: false
16 soni 2 ning darajasimi: true
31 soni 2 ning darajasimi: false
64 soni 2 ning darajasimi: true
```

# 47-Topshiriq: num.remainder() va % operatori farqi
## Topshiriq sharti:
Manfiy sonlar bilan `%` operatori va `.remainder()` metodining qoldiq hisoblashdagi farqini ko'rsating.

## Yechim (Dart kodi):
```dart
void main() {
  int a = -7;
  int b = 3;

  print("-7 % 3 = ${a % b}");
  print("-7.remainder(3) = ${a.remainder(b)}");
}
```

## Tushuntirish va Mantiq:
Dart da `%` operatori har doim musbat qoldiq beradi (evklid qoldig'i), `.remainder()` esa bo'linuvchining o'z ishorasini saqlab qoladi.

## Ishlash natijasi:
```text
-7 % 3 = 2
-7.remainder(3) = -1
```

# 48-Topshiriq: BigInt tipi: Cheksiz aniqlikdagi katta sonlar
## Topshiriq sharti:
64-bitdan katta bo'lgan astronomik sonlarni yoki katta faktoriallarni `BigInt` orqali aniq hisoblang.

## Yechim (Dart kodi):
```dart
void main() {
  BigInt a = BigInt.parse("123456789012345678901234567890");
  BigInt b = BigInt.from(2);

  BigInt natija = a * b;
  print("Katta son natijasi:
$natija");
}
```

## Tushuntirish va Mantiq:
`BigInt` xotira yetarli bo'lganicha cheksiz katta butun sonlarni xatoliksiz va yaxlitlashsiz hisoblash imkonini beradi.

## Ishlash natijasi:
```text
Katta son natijasi:
246913578024691357802469135780
```

# 49-Topshiriq: DateTime bilan ishlash va sanalarni tahlil qilish
## Topshiriq sharti:
Muayyan sana va vaqt ob'ektini yarating, yil, oy, kun, soat va daqiqasini ajratib oling.

## Yechim (Dart kodi):
```dart
void main() {
  DateTime sana = DateTime(2026, 11, 7, 18, 45);

  print("To'liq sana: $sana");
  print("Yil: ${sana.year}");
  print("Oy:  ${sana.month}");
  print("Kun: ${sana.day}");
  print("Hafta kuni: ${sana.weekday} (6 = Shanba)");
}
```

## Tushuntirish va Mantiq:
`DateTime` sinfi sanalarni taqqoslash, millisekundlarni hisoblash va vaqt mintaqalarini boshqarish uchun xizmat qiladi.

## Ishlash natijasi:
```text
To'liq sana: 2026-11-07 18:45:00.000
Yil: 2026
Oy:  11
Kun: 7
Hafta kuni: 6 (6 = Shanba)
```

# 50-Topshiriq: Duration bilan vaqt oraliqlarini qo'shish va ayirish
## Topshiriq sharti:
`Duration` yordamida sanaga 10 kun yoki 3 soat qo'shing va ikki sana orasidagi farqni toping.

## Yechim (Dart kodi):
```dart
void main() {
  DateTime hozir = DateTime(2026, 11, 7);
  Duration oraliq = Duration(days: 10, hours: 5);

  DateTime kelajak = hozir.add(oraliq);
  print("Boshlang'ich sana: $hozir");
  print("10 kun va 5 soatdan so'ng: $kelajak");

  Duration farq = kelajak.difference(hozir);
  print("Orasidagi farq soatlarda: ${farq.inHours} soat");
}
```

## Tushuntirish va Mantiq:
`Duration` vaqt masofalarini ifodalaydi. `add()`, `subtract()` va `difference()` orqali sanalar arifmetikasi sodda va ishonchli amalga oshiriladi.

## Ishlash natijasi:
```text
Boshlang'ich sana: 2026-11-07 00:00:00.000
10 kun va 5 soatdan so'ng: 2026-11-17 05:00:00.000
Orasidagi farq soatlarda: 245 soat
```

