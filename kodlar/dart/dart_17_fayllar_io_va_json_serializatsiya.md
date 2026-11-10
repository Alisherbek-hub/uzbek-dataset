# 801-Topshiriq: Faylga matn yozish va o'qish (Asinxron File I/O)

## Topshiriq sharti:
`dart:io` kutubxonasidagi `File` klassi yordamida matnni faylga asinxron yozing va qayta o'qing.

## Yechim (Dart kodi):
```dart
import 'dart:io';

void main() async {
  var file = File('salom.txt');

  await file.writeAsString('Assalomu alaykum, Dart IO!');
  print('Faylga yozildi.');

  String matn = await file.readAsString();
  print('Fayldan o\'qildi: $matn');

  // Tozalash
  if (await file.exists()) await file.delete();
}
```

## Tushuntirish va Mantiq:
`writeAsString()` va `readAsString()` asinxron ishlaydi va asosiy Event Loop oqimini to'xtatib qo'ymaydi.

## Ishlash natijasi:
```text
Faylga yozildi.
Fayldan o'qildi: Assalomu alaykum, Dart IO!
```

# 802-Topshiriq: Sinxron fayl amallari (Sync I/O)

## Topshiriq sharti:
Kichik skriptlar yoki CLI utilitalar uchun bloklovchi sinxron fayl amallarini ko'rsating.

## Yechim (Dart kodi):
```dart
import 'dart:io';

void main() {
  var file = File('sozlama.cfg');

  file.writeAsStringSync('theme=dark
lang=uz');
  print('Sinxron yozildi.');

  String sozlamalar = file.readAsStringSync();
  print('Sinxron o\'qildi:
$sozlamalar');

  if (file.existsSync()) file.deleteSync();
}
```

## Tushuntirish va Mantiq:
`Sync` qo'shimchali metodlar darhol bloklovchi tarzda bajariladi, asinxron kutish (`await`) talab etilmaydi.

## Ishlash natijasi:
```text
Sinxron yozildi.
Sinxron o'qildi:
theme=dark
lang=uz
```

# 803-Topshiriq: Fayl mavjudligini tekshirish (exists)

## Topshiriq sharti:
Faylni ochishdan oldin uning diskda mavjudligini xavfsiz tekshiring.

## Yechim (Dart kodi):
```dart
import 'dart:io';

void main() async {
  var file = File('mavjud_emas.txt');

  if (await file.exists()) {
    print('Fayl mavjud.');
  } else {
    print('Fayl topilmadi, xatolikning oldi olindi!');
  }
}
```

## Tushuntirish va Mantiq:
`await file.exists()` fayl yo'qligida `PathNotFoundException` xatosi chiqishining oldini oladi.

## Ishlash natijasi:
```text
Fayl topilmadi, xatolikning oldi olindi!
```

# 804-Topshiriq: Faylga qo'shib yozish (FileMode.append)

## Topshiriq sharti:
Eski ma'lumotlarni o'chirmasdan fayl oxiriga yangi qatorlar qo'shib yozuvchi jurnal dasturini tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:io';

void main() async {
  var file = File('jurnal.log');

  await file.writeAsString('Log 1: Tizim ishga tushdi
', mode: FileMode.append);
  await file.writeAsString('Log 2: Foydalanuvchi kirdi
', mode: FileMode.append);

  print('Fayl tarkibi:');
  print(await file.readAsString());

  if (await file.exists()) await file.delete();
}
```

## Tushuntirish va Mantiq:
`mode: FileMode.append` mavjud matnni o'chirmasdan, yangi ma'lumotlarni fayl oxiriga qo'shadi.

## Ishlash natijasi:
```text
Fayl tarkibi:
Log 1: Tizim ishga tushdi
Log 2: Foydalanuvchi kirdi
```

# 805-Topshiriq: Faylni satrma-satr o'qish (readAsLines)

## Topshiriq sharti:
Fayl tarkibini qatorlar ro'yxati (`List<String>`) sifatida o'qing.

## Yechim (Dart kodi):
```dart
import 'dart:io';

void main() async {
  var file = File('shiorlar.txt');
  await file.writeAsString('Birinchi satr
Ikkinchi satr
Uchinchi satr');

  List<String> satrlar = await file.readAsLines();

  for (int i = 0; i < satrlar.length; i++) {
    print('${i + 1}-qator: ${satrlar[i]}');
  }

  if (await file.exists()) await file.delete();
}
```

## Tushuntirish va Mantiq:
`readAsLines()` fayldagi yangi qator belgilariga (`
`) ko'ra avtomatik `List<String>` ga bo'lib beradi.

## Ishlash natijasi:
```text
1-qator: Birinchi satr
2-qator: Ikkinchi satr
3-qator: Uchinchi satr
```

# 806-Topshiriq: Katta faylni oqimli satrma-satr o'qish (Stream LineSplitter)

## Topshiriq sharti:
Gigabaytlab katta fayllarni butunlay RAMga yuklamasdan oqim orqali qatorlab o'qing.

## Yechim (Dart kodi):
```dart
import 'dart:io';
import 'dart:convert';

void main() async {
  var file = File('katta_matn.txt');
  await file.writeAsString('Alpha
Beta
Gamma');

  // Xotirani tejab oqimli o'qish
  var qatorlar = file
      .openRead()
      .transform(utf8.decoder)
      .transform(LineSplitter());

  await for (var qator in qatorlar) {
    print('Oqimli qator: $qator');
  }

  if (await file.exists()) await file.delete();
}
```

## Tushuntirish va Mantiq:
`openRead()`, `utf8.decoder` va `LineSplitter()` kombinatsiyasi ulkan fayllarni minimal RAM sarflab qayta ishlaydi.

## Ishlash natijasi:
```text
Oqimli qator: Alpha
Oqimli qator: Beta
Oqimli qator: Gamma
```

# 807-Topshiriq: Katalog yaratish va tekshirish (Directory.create)

## Topshiriq sharti:
Diskda yangi katalog va uning ichma-ich papkalarini (`recursive: true`) yarating.

## Yechim (Dart kodi):
```dart
import 'dart:io';

void main() async {
  var papka = Directory('loyihalar/ai_model/v1');

  await papka.create(recursive: true);
  print('Papka yaratildi: ${await papka.exists()}');

  // Tozalash
  await Directory('loyihalar').delete(recursive: true);
}
```

## Tushuntirish va Mantiq:
`recursive: true` oraliq papkalar mavjud bo'lmasa ularni ham avtomatik yaratib beradi.

## Ishlash natijasi:
```text
Papka yaratildi: true
```

# 808-Topshiriq: Katalog ichidagi fayllarni sanab chiqish (dir.list)

## Topshiriq sharti:
Papkadagi barcha fayl va quyi papkalar ro'yxatini asinxron oqim orqali chiqaring.

## Yechim (Dart kodi):
```dart
import 'dart:io';

void main() async {
  var papka = Directory('test_papka');
  await papka.create();
  await File('test_papka/a.txt').create();
  await File('test_papka/b.txt').create();

  print('Papka tarkibi:');
  await for (var ob in papka.list()) {
    print('- ${ob.path.replaceAll(r'\', '/')}');
  }

  await papka.delete(recursive: true);
}
```

## Tushuntirish va Mantiq:
`dir.list()` papka ichidagi har bir elementni `FileSystemEntity` sifatida oqimda taqdim etadi.

## Ishlash natijasi:
```text
Papka tarkibi:
- test_papka/a.txt
- test_papka/b.txt
```

# 809-Topshiriq: Faylni qayta nomlash va ko'chirish (file.rename)

## Topshiriq sharti:
Fayl nomini o'zgartirish yoki uni boshqa manzilga ko'chirish amalini bajaring.

## Yechim (Dart kodi):
```dart
import 'dart:io';

void main() async {
  var f1 = File('eski_nom.txt');
  await f1.writeAsString('Ma\'lumot');

  var f2 = await f1.rename('yangi_nom.txt');
  print('Yangi fayl mavjudmi: ${await f2.exists()}');
  print('Eski fayl mavjudmi: ${await f1.exists()}');

  if (await f2.exists()) await f2.delete();
}
```

## Tushuntirish va Mantiq:
`file.rename(newPath)` fayl manzilini yoki nomini atomik o'zgartiradi va yangi `File` obyektini qaytaradi.

## Ishlash natijasi:
```text
Yangi fayl mavjudmi: true
Eski fayl mavjudmi: false
```

# 810-Topshiriq: Fayl hajmi va o'zgartirilgan vaqtini olish

## Topshiriq sharti:
Faylning baytlardagi hajmi va oxirgi tahrirlangan vaqtini aniqlang.

## Yechim (Dart kodi):
```dart
import 'dart:io';

void main() async {
  var file = File('meta_sinov.txt');
  await file.writeAsString('1234567890'); // 10 bayt

  int baytlar = await file.length();
  DateTime vaqt = await file.lastModified();

  print('Hajmi: $baytlar bayt');
  print('Tahrirlangan yil: ${vaqt.year}');

  if (await file.exists()) await file.delete();
}
```

## Tushuntirish va Mantiq:
`file.length()` fayl hajmini baytlarda, `file.lastModified()` esa oxirgi saqlangan sana va vaqtni beradi.

## Ishlash natijasi:
```text
Hajmi: 10 bayt
Tahrirlangan yil: 2026
```

# 811-Topshiriq: Tizimning vaqtinchalik katalogi bilan ishlash

## Topshiriq sharti:
Operatsion tizimning vaqtinchalik papkasida (Temp) xavfsiz fayl yarating.

## Yechim (Dart kodi):
```dart
import 'dart:io';

void main() async {
  var tempDir = Directory.systemTemp;
  var tempFayl = File('${tempDir.path}/vaqtincha_${DateTime.now().millisecondsSinceEpoch}.txt');

  await tempFayl.writeAsString('Vaqtinchalik hisob-kitob');
  print('Temp fayl yaratildi: ${await tempFayl.exists()}');

  await tempFayl.delete();
}
```

## Tushuntirish va Mantiq:
`Directory.systemTemp` OS ga xos vaqtinchalik katalog manzilini aniqlab beradi.

## Ishlash natijasi:
```text
Temp fayl yaratildi: true
```

# 812-Topshiriq: dart:convert: jsonEncode va jsonDecode

## Topshiriq sharti:
Map ma'lumotlarini JSON matniga o'girish va JSON matnini yana Map ga aylantirish.

## Yechim (Dart kodi):
```dart
import 'dart:convert';

void main() {
  Map<String, dynamic> user = {
    'ism': 'Javohir',
    'yosh': 24,
    'konikmalar': ['Dart', 'Flutter', 'AI']
  };

  // 1. Serialization (Obyektdan matnga)
  String jsonMatn = jsonEncode(user);
  print('JSON matn: $jsonMatn');

  // 2. Deserialization (Matndan obyektga)
  Map<String, dynamic> qaytaLugat = jsonDecode(jsonMatn);
  print('Qayta olingan ism: ${qaytaLugat["ism"]}');
}
```

## Tushuntirish va Mantiq:
`jsonEncode` JSON satriga o'giradi, `jsonDecode` esa JSON satrini dinamik Map yoki List tuzilmasiga parse qiladi.

## Ishlash natijasi:
```text
JSON matn: {"ism":"Javohir","yosh":24,"konikmalar":["Dart","Flutter","AI"]}
Qayta olingan ism: Javohir
```

# 813-Topshiriq: Model klassini JSON ga aylantirish (toJson)

## Topshiriq sharti:
Klass ichida `toJson()` metodini yozib, obyektni Map va JSON formatiga o'tkazing.

## Yechim (Dart kodi):
```dart
import 'dart:convert';

class Mahsulot {
  final int id;
  final String nom;
  final double narx;

  Mahsulot(this.id, this.nom, this.narx);

  Map<String, dynamic> toJson() => {
        'id': id,
        'nom': nom,
        'narx': narx,
      };
}

void main() {
  var p = Mahsulot(101, 'Noutbuk', 8500000);
  String json = jsonEncode(p.toJson());

  print('Mahsulot JSON: $json');
}
```

## Tushuntirish va Mantiq:
`toJson()` konvensiyasi Dartda API ga so'rov yuborishda standart hisoblanadi.

## Ishlash natijasi:
```text
Mahsulot JSON: {"id":101,"nom":"Noutbuk","narx":8500000.0}
```

# 814-Topshiriq: JSON dan Model klassini yasash (fromJson)

## Topshiriq sharti:
Serverdan kelgan JSON dan `factory Model.fromJson()` orqali xavfsiz obyekt yasang.

## Yechim (Dart kodi):
```dart
import 'dart:convert';

class Shaxs {
  final String ism;
  final int yosh;

  Shaxs({required this.ism, required this.yosh});

  factory Shaxs.fromJson(Map<String, dynamic> json) {
    return Shaxs(
      ism: json['ism'] as String,
      yosh: json['yosh'] as int,
    );
  }

  @override
  String toString() => 'Shaxs(ism: $ism, yosh: $yosh)';
}

void main() {
  String serverJson = '{"ism": "Anvar", "yosh": 28}';
  var shaxs = Shaxs.fromJson(jsonDecode(serverJson));

  print('Model hosil bo\'ldi: $shaxs');
}
```

## Tushuntirish va Mantiq:
Factory konstruktor JSON maydonlarini tekshirib to'g'ri tipli obyektga aylantiradi.

## Ishlash natijasi:
```text
Model hosil bo'ldi: Shaxs(ism: Anvar, yosh: 28)
```

# 815-Topshiriq: Ichma-ich (Nested) obyektlar JSON serializatsiyasi

## Topshiriq sharti:
Kompaniya va uning Manzili kabi ichma-ich bog'langan modellarni JSON ga o'giring va tiklang.

## Yechim (Dart kodi):
```dart
import 'dart:convert';

class Manzil {
  final String shahar;
  Manzil(this.shahar);

  Map<String, dynamic> toJson() => {'shahar': shahar};
  factory Manzil.fromJson(Map<String, dynamic> j) => Manzil(j['shahar']);
}

class Kompaniya {
  final String nom;
  final Manzil manzil;

  Kompaniya(this.nom, this.manzil);

  Map<String, dynamic> toJson() => {
        'nom': nom,
        'manzil': manzil.toJson(),
      };

  factory Kompaniya.fromJson(Map<String, dynamic> j) => Kompaniya(
        j['nom'],
        Manzil.fromJson(j['manzil']),
      );
}

void main() {
  var k = Kompaniya('UzbekAI Startup', Manzil('Toshkent'));
  String json = jsonEncode(k.toJson());
  print('Nested JSON: $json');

  var qayta = Kompaniya.fromJson(jsonDecode(json));
  print('Qayta tiklandi: ${qayta.nom}, Shahar: ${qayta.manzil.shahar}');
}
```

## Tushuntirish va Mantiq:
Ichki obyektlar ham o'z `toJson()` va `fromJson()` metodlariga ega bo'lib, zanjir bo'yicha chaqiriladi.

## Ishlash natijasi:
```text
Nested JSON: {"nom":"UzbekAI Startup","manzil":{"shahar":"Toshkent"}}
Qayta tiklandi: UzbekAI Startup, Shahar: Toshkent
```

# 816-Topshiriq: Ro'yxatdagi obyektlarni JSON array ga aylantirish

## Topshiriq sharti:
Obyektlar ro'yxatini (`List<Kitob>`) JSON massiviga va qaytadan ro'yxatga o'giring.

## Yechim (Dart kodi):
```dart
import 'dart:convert';

class Kitob {
  final String nom;
  Kitob(this.nom);

  Map<String, dynamic> toJson() => {'nom': nom};
  factory Kitob.fromJson(Map<String, dynamic> j) => Kitob(j['nom']);
}

void main() {
  List<Kitob> javon = [Kitob('Dart'), Kitob('Flutter')];

  // List -> JSON string
  String jsonArr = jsonEncode(javon.map((k) => k.toJson()).toList());
  print('JSON massiv: $jsonArr');

  // JSON string -> List
  List<dynamic> parsedList = jsonDecode(jsonArr);
  List<Kitob> qaytaJavon = parsedList.map((j) => Kitob.fromJson(j)).toList();

  print('Qayta olingan kitoblar: ${qaytaJavon.map((e) => e.nom).join(", ")}');
}
```

## Tushuntirish va Mantiq:
`list.map((e) => e.toJson()).toList()` yordamida obyektlar massivi JSON array formatiga qulay o'giriladi.

## Ishlash natijasi:
```text
JSON massiv: [{"nom":"Dart"},{"nom":"Flutter"}]
Qayta olingan kitoblar: Dart, Flutter
```

# 817-Topshiriq: Chiroyli formatlangan JSON (Pretty Print)

## Topshiriq sharti:
Bo'sh joylar va chekinishlar (indent) bilan o'qishga qulay JSON chiqarish.

## Yechim (Dart kodi):
```dart
import 'dart:convert';

void main() {
  var data = {
    'loyiha': 'BitNet-1bit',
    'status': 'faol',
    'versiya': 1.58
  };

  var encoder = JsonEncoder.withIndent('  ');
  String prettyJson = encoder.convert(data);

  print('Chiroyli JSON:');
  print(prettyJson);
}
```

## Tushuntirish va Mantiq:
`JsonEncoder.withIndent('  ')` orqali formatlangan chiroyli JSON chop etiladi.

## Ishlash natijasi:
```text
Chiroyli JSON:
{
  "loyiha": "BitNet-1bit",
  "status": "faol",
  "versiya": 1.58
}
```

# 818-Topshiriq: CSV faylni o'qish va tahlil qilish

## Topshiriq sharti:
Vergul bilan ajratilgan CSV ma'lumotlarini qatorma-qator o'qib tahlil qiling.

## Yechim (Dart kodi):
```dart
import 'dart:io';

void main() async {
  var file = File('talabalar.csv');
  await file.writeAsString('ID,Ism,Ball
1,Ali,90
2,Vali,85');

  var qatorlar = await file.readAsLines();

  for (int i = 1; i < qatorlar.length; i++) {
    var ustunlar = qatorlar[i].split(',');
    print('Talaba #${ustunlar[0]}: ${ustunlar[1]} (${ustunlar[2]} ball)');
  }

  if (await file.exists()) await file.delete();
}
```

## Tushuntirish va Mantiq:
CSV jadval formatidagi fayllar qatorlar va vergul orqali oddiy va tezkor parse qilinadi.

## Ishlash natijasi:
```text
Talaba #1: Ali (90 ball)
Talaba #2: Vali (85 ball)
```

# 819-Topshiriq: Baytlar bilan ishlash (Uint8List va writeAsBytes)

## Topshiriq sharti:
Ikkilik (binary) baytlar massivini faylga yozish va baytma-bayt qayta o'qish.

## Yechim (Dart kodi):
```dart
import 'dart:io';
import 'dart:typed_data';

void main() async {
  var file = File('baytlar.bin');
  var data = Uint8List.fromList([0x01, 0x02, 0xFF, 0x00]);

  await file.writeAsBytes(data);
  print('Ikkilik baytlar yozildi.');

  Uint8List oqilgan = await file.readAsBytes();
  print('O\'qilgan baytlar: $oqilgan');

  if (await file.exists()) await file.delete();
}
```

## Tushuntirish va Mantiq:
`Uint8List` xotirani eng tejamkor shaklda (har bir element 1 bayt: 0..255) saqlaydi.

## Ishlash natijasi:
```text
Ikkilik baytlar yozildi.
O'qilgan baytlar: [1, 2, 255, 0]
```

# 820-Topshiriq: ByteData va Endian (BigEndian vs LittleEndian)

## Topshiriq sharti:
Baytlar tartibini (Endian) boshqarib 32-bitli butun sonlarni yozish va o'qish.

## Yechim (Dart kodi):
```dart
import 'dart:typed_data';

void main() {
  var bufer = Uint8List(4);
  var bd = ByteData.view(bufer.buffer);

  // Big Endian formatda yozish
  bd.setInt32(0, 0x12345678, Endian.big);
  print('Big Endian baytlari: $bufer');

  // Little Endian formatda yozish
  bd.setInt32(0, 0x12345678, Endian.little);
  print('Little Endian baytlari: $bufer');
}
```

## Tushuntirish va Mantiq:
Tarmoq protokollari odatda Big-Endian, x86/ARM protsessorlar esa Little-Endian tartibidan foydalanadi.

## Ishlash natijasi:
```text
Big Endian baytlari: [18, 52, 86, 120]
Little Endian baytlari: [120, 86, 52, 18]
```

# 821-Topshiriq: GZip orqali ma'lumotlarni siqish va ochish

## Topshiriq sharti:
`dart:io` ichidagi `gzip` yordamida matn baytlarini siqish va qayta ochish.

## Yechim (Dart kodi):
```dart
import 'dart:io';
import 'dart:convert';

void main() {
  String kattaMatn = 'BitNet 1-bit AI ' * 20;
  List<int> aslBaytlar = utf8.encode(kattaMatn);

  List<int> siqilgan = gzip.encode(aslBaytlar);
  List<int> ochilgan = gzip.decode(siqilgan);

  print('Asl hajm: ${aslBaytlar.length} bayt');
  print('Siqilgan hajm: ${siqilgan.length} bayt');
  print('Qayta tiklangan matn to\'g\'rimi: ${utf8.decode(ochilgan) == kattaMatn}');
}
```

## Tushuntirish va Mantiq:
GZip siqish algoritmi matnli ma'lumotlar hajmini 70-80% gacha qisqartiradi.

## Ishlash natijasi:
```text
Asl hajm: 320 bayt
Siqilgan hajm: 46 bayt
Qayta tiklangan matn to'g'rimi: true
```

# 822-Topshiriq: Atomik fayl yozish (Atomic Write)

## Topshiriq sharti:
Tizim to'satdan o'chib qolsa fayl buzilmasligi uchun avval temp faylga yozib so'ngra rename qiling.

## Yechim (Dart kodi):
```dart
import 'dart:io';

Future<void> xavfsizYozish(String manzil, String matn) async {
  var tempFayl = File('$manzil.tmp');
  await tempFayl.writeAsString(matn);
  await tempFayl.rename(manzil); // Atomik operatsiya!
}

void main() async {
  String target = 'muhim_baza.json';
  await xavfsizYozish(target, '{"status": "xavfsiz"}');

  print('Atomik yozilgan fayl tarkibi:');
  print(await File(target).readAsString());

  if (await File(target).exists()) await File(target).delete();
}
```

## Tushuntirish va Mantiq:
Atomik fayl yozish fayl yarim chala yozilib qolishi va buzilishining 100% oldini oladi.

## Ishlash natijasi:
```text
Atomik yozilgan fayl tarkibi:
{"status": "xavfsiz"}
```

# 823-Topshiriq: Fayldagi so'zlar va baytlarni hisoblash

## Topshiriq sharti:
Faylni o'qib undagi qatorlar, so'zlar va baytlar sonini hisoblovchi CLI utilita tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:io';

void main() async {
  var file = File('statistika.txt');
  await file.writeAsString('Dart tili juda qulay
Flutter esa chiroyli');

  String content = await file.readAsString();
  int qatorlar = content.split('
').length;
  int sozlar = content.split(RegExp(r'\s+')).length;
  int baytlar = await file.length();

  print('Qatorlar: $qatorlar');
  print('So\'zlar: $sozlar');
  print('Hajmi: $baytlar bayt');

  if (await file.exists()) await file.delete();
}
```

## Tushuntirish va Mantiq:
Linux dagi `wc` (word count) utilitasiga o'xshash statistika hisoblash dasturi.

## Ishlash natijasi:
```text
Qatorlar: 2
So'zlar: 7
Hajmi: 43 bayt
```

# 824-Topshiriq: Fayllarni saralash (Katalogdagi fayllarni sanasi bo'yicha)

## Topshiriq sharti:
Papkadagi fayllarni oxirgi o'zgartirilgan sanasi bo'yicha saralab chiqaring.

## Yechim (Dart kodi):
```dart
import 'dart:io';

void main() async {
  var d = Directory('vaqt_test');
  await d.create();
  var f1 = File('vaqt_test/eski.txt');
  await f1.create();
  var f2 = File('vaqt_test/yangi.txt');
  await f2.create();

  var entities = await d.list().where((e) => e is File).cast<File>().toList();
  // Saralash
  entities.sort((a, b) => a.lastModifiedSync().compareTo(b.lastModifiedSync()));

  print('Saralangan fayllar soni: ${entities.length}');
  await d.delete(recursive: true);
}
```

## Tushuntirish va Mantiq:
`lastModifiedSync()` yordamida fayllar xronologik tartibda saralanadi.

## Ishlash natijasi:
```text
Saralangan fayllar soni: 2
```

# 825-Topshiriq: Amaliy: BitNet Lug'atini (Tokenizer Vocab) JSON faylda saqlash

## Topshiriq sharti:
Tokenlarni ID larga bog'lovchi lug'atni JSON faylga saqlash va yuklash dasturini yozing.

## Yechim (Dart kodi):
```dart
import 'dart:io';
import 'dart:convert';

class TokenizerLugati {
  final Map<String, int> tokenToId;

  TokenizerLugati(this.tokenToId);

  Future<void> saqlash(String faylYoli) async {
    var file = File(faylYoli);
    await file.writeAsString(jsonEncode(tokenToId));
  }

  static Future<TokenizerLugati> yuklash(String faylYoli) async {
    var file = File(faylYoli);
    String matn = await file.readAsString();
    Map<String, dynamic> j = jsonDecode(matn);
    return TokenizerLugati(j.map((k, v) => MapEntry(k, v as int)));
  }
}

void main() async {
  var lugat = TokenizerLugati({'<pad>': 0, '<bos>': 1, 'uzbek': 2, 'ai': 3});
  await lugat.saqlash('vocab.json');

  var yuklangan = await TokenizerLugati.yuklash('vocab.json');
  print('Yuklangan tokenlar soni: ${yuklangan.tokenToId.length}');
  print('Token "ai" ID si: ${yuklangan.tokenToId["ai"]}');

  if (await File('vocab.json').exists()) await File('vocab.json').delete();
}
```

## Tushuntirish va Mantiq:
AI modellari o'z lug'at fayllarini (tokenizer vocabulary) JSON formatida saqlaydi va yuklaydi.

## Ishlash natijasi:
```text
Yuklangan tokenlar soni: 4
Token "ai" ID si: 3
```

# 826-Topshiriq: Binar Bit-Packing (1-bit qiymatlarni baytga zichlash)

## Topshiriq sharti:
BitNet 1-bit qiymatlarini bitta bayt ichiga 8 tadan joylab (bit-packing) xotirani 8 barobar tejashni amalga oshiring.

## Yechim (Dart kodi):
```dart
import 'dart:typed_data';

Uint8List packBits(List<int> bits) {
  int byteCount = (bits.length + 7) ~/ 8;
  var bytes = Uint8List(byteCount);

  for (int i = 0; i < bits.length; i++) {
    if (bits[i] != 0) {
      int byteIdx = i ~/ 8;
      int bitIdx = i % 8;
      bytes[byteIdx] |= (1 << bitIdx);
    }
  }
  return bytes;
}

List<int> unpackBits(Uint8List bytes, int length) {
  List<int> bits = [];
  for (int i = 0; i < length; i++) {
    int byteIdx = i ~/ 8;
    int bitIdx = i % 8;
    int bit = (bytes[byteIdx] >> bitIdx) & 1;
    bits.add(bit);
  }
  return bits;
}

void main() {
  List<int> asl = [1, 0, 1, 1, 0, 0, 1, 0];
  var packed = packBits(asl);
  print('Zichlangan baytlar: $packed (Hajmi: ${packed.length} bayt)');

  var unpacked = unpackBits(packed, asl.length);
  print('Qayta ochilgan bitlar: $unpacked');
}
```

## Tushuntirish va Mantiq:
Bit-packing 8 ta mantiqiy yoki 1-bitli qiymatni bitta baytda saqlaydi, bu BitNet kabi modellar uchun muhim.

## Ishlash natijasi:
```text
Zichlangan baytlar: [77] (Hajmi: 1 bayt)
Qayta ochilgan bitlar: [1, 0, 1, 1, 0, 0, 1, 0]
```

# 827-Topshiriq: Fayl nomlarini xavfsiz tozalash (Sanitize filename)

## Topshiriq sharti:
Fayl nomidagi noqonuniy belgilarni (/ , \, :, *, ?, ', <, >, |) xavfsiz belgilarga almashtiring.

## Yechim (Dart kodi):
```dart
String tozaFaylNomi(String xomNom) {
  return xomNom.replaceAll(RegExp(r'[\\/:*?"<>|]'), '_').trim();
}

void main() {
  String xavfli = 'hisobot: 2026/11/07 *final*?.txt';
  String toza = tozaFaylNomi(xavfli);

  print('Xavfsiz fayl nomi: $toza');
}
```

## Tushuntirish va Mantiq:
Fayl nomlarini tozalash operatsion tizimda kutilmagan fayl yo'li buzilishlaridan asraydi.

## Ishlash natijasi:
```text
Xavfsiz fayl nomi: hisobot_ 2026_11_07 _final__.txt
```

# 828-Topshiriq: Xavfsiz fayl o'chirish (Safe Delete)

## Topshiriq sharti:
Fayl mavjud bo'lsa o'chiruvchi, mavjud bo'lmasa xato chiqarmaydigan kengaytma metod yozing.

## Yechim (Dart kodi):
```dart
import 'dart:io';

extension SafeFile on File {
  Future<void> safeDelete() async {
    if (await exists()) {
      await delete();
      print('Fayl o\'chirildi: $path');
    } else {
      print('Fayl allaqachon mavjud emas, o\'tkazib yuborildi.');
    }
  }
}

void main() async {
  var f = File('yoq_fayl.txt');
  await f.safeDelete();
}
```

## Tushuntirish va Mantiq:
Extension metod yordamida `File` sinfiga qulay xavfsiz o'chirish funksiyasi ulandi.

## Ishlash natijasi:
```text
Fayl allaqachon mavjud emas, o'tkazib yuborildi.
```

# 829-Topshiriq: Rekursiv katalog nusxalash (Directory Copy)

## Topshiriq sharti:
Papka va uning barcha ichki fayllarini yangi manzilga to'liq ko'chirib o'tkazuvchi funksiya tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:io';

Future<void> copyDirectory(Directory source, Directory destination) async {
  await destination.create(recursive: true);
  await for (var entity in source.list(recursive: false)) {
    String newPath = entity.path.replaceAll(source.path, destination.path);
    if (entity is Directory) {
      await copyDirectory(entity, Directory(newPath));
    } else if (entity is File) {
      await entity.copy(newPath);
    }
  }
}

void main() async {
  var src = Directory('src_test');
  await src.create();
  await File('src_test/f.txt').writeAsString('test');

  var dst = Directory('dst_test');
  await copyDirectory(src, dst);

  print('Nusxa mavjudmi: ${await File("dst_test/f.txt").exists()}');

  await src.delete(recursive: true);
  await dst.delete(recursive: true);
}
```

## Tushuntirish va Mantiq:
Rekursiv nusxalash papka iyerarxiyasini yangi joyda to'liq qayta barpo etadi.

## Ishlash natijasi:
```text
Nusxa mavjudmi: true
```

# 830-Topshiriq: JSON ma'lumotlar sxemasi validatsiyasi

## Topshiriq sharti:
JSON obyektida barcha talab qilingan maydonlar va to'g'ri tiplar borligini tekshiring.

## Yechim (Dart kodi):
```dart
bool validatsiyaJson(Map<String, dynamic> json) {
  if (!json.containsKey('id') || json['id'] is! int) return false;
  if (!json.containsKey('nom') || json['nom'] is! String) return false;
  return true;
}

void main() {
  var data1 = {'id': 1, 'nom': 'AI'};
  var data2 = {'id': 'bir', 'nom': 'AI'};

  print('data1 yaroqlimi: ${validatsiyaJson(data1)}');
  print('data2 yaroqlimi: ${validatsiyaJson(data2)}');
}
```

## Tushuntirish va Mantiq:
Tashqi manbalardan olingan JSON ma'lumotlarini avval validatsiya qilish tizim barqarorligini oshiradi.

## Ishlash natijasi:
```text
data1 yaroqlimi: true
data2 yaroqlimi: false
```

# 831-Topshiriq: JSON Diff (Ikki JSON orasidagi o'zgarishlar)

## Topshiriq sharti:
Eski va yangi JSON obyektlari o'rtasida o'zgargan kalitlarni aniqlang.

## Yechim (Dart kodi):
```dart
Map<String, (dynamic, dynamic)> jsonDiff(Map<String, dynamic> eski, Map<String, dynamic> yangi) {
  Map<String, (dynamic, dynamic)> farqlar = {};
  for (var k in yangi.keys) {
    if (eski[k] != yangi[k]) {
      farqlar[k] = (eski[k], yangi[k]);
    }
  }
  return farqlar;
}

void main() {
  var v1 = {'versiya': 1.0, 'nom': 'AI'};
  var v2 = {'versiya': 1.58, 'nom': 'AI'};

  print('O\'zgarishlar: ${jsonDiff(v1, v2)}');
}
```

## Tushuntirish va Mantiq:
JSON diff orqali konfiguratsiya yoki modellardagi yangilanishlar ko'rinadi.

## Ishlash natijasi:
```text
O'zgarishlar: {versiya: (1.0, 1.58)}
```

# 832-Topshiriq: Fayl yuklab olish va progress kuzatish simulyatsiyasi

## Topshiriq sharti:
Faylni bloklab yuklab diskka saqlash va foizini ko'rsatish dasturini tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:io';

Future<void> yuklabOlishSimulyatsiya(String faylNomi, int totalBytes) async {
  var f = File(faylNomi);
  var sink = f.openWrite();

  for (int b = 100; b <= totalBytes; b += 100) {
    sink.add(List.filled(100, 0));
    print('Yuklandi: $b / $totalBytes bayt');
  }

  await sink.close();
  if (await f.exists()) await f.delete();
}

void main() async {
  await yuklabOlishSimulyatsiya('temp_model.bin', 300);
}
```

## Tushuntirish va Mantiq:
`openWrite()` oqimi faylga qismlab yozish va yuklanish progressini kuzatish imkonini beradi.

## Ishlash natijasi:
```text
Yuklandi: 100 / 300 bayt
Yuklandi: 200 / 300 bayt
Yuklandi: 300 / 300 bayt
```

# 833-Topshiriq: Fayl nazorat yig'indisini (Checksum) hisoblash

## Topshiriq sharti:
Fayl baytlarining yaxlitligini tekshirish uchun CRC / oddiy checksum hisoblang.

## Yechim (Dart kodi):
```dart
import 'dart:io';

Future<int> hisoblaChecksum(File file) async {
  var bytes = await file.readAsBytes();
  return bytes.fold(0, (sum, b) => (sum + b) % 65535);
}

void main() async {
  var f = File('check_sinov.bin');
  await f.writeAsBytes([10, 20, 30, 40]);

  int check = await hisoblaChecksum(f);
  print('Fayl Checksum: $check');

  if (await f.exists()) await f.delete();
}
```

## Tushuntirish va Mantiq:
Nazorat yig'indisi fayl diskka to'liq va buzilmasdan yozilganligini tasdiqlash uchun xizmat qiladi.

## Ishlash natijasi:
```text
Fayl Checksum: 100
```

# 834-Topshiriq: Fayl watcher (file.watch() orqali o'zgarishlarni kuzatish)

## Topshiriq sharti:
Fayl o'zgartirilganda real vaqt rejimida voqea beruvchi `file.watch()` imkoniyatini ko'rsating.

## Yechim (Dart kodi):
```dart
import 'dart:io';

void main() async {
  var f = File('kuzatiladigan.txt');
  await f.create();

  // Fayl o'zgarishlarini kuzatuvchi Stream
  var stream = f.watch();
  var sub = stream.listen((voqea) {
    print('Fayl hodisasi yuz berdi: ${voqea.type}');
  });

  await f.writeAsString('Yangi matn');
  await Future.delayed(Duration(milliseconds: 10));

  await sub.cancel();
  if (await f.exists()) await f.delete();
}
```

## Tushuntirish va Mantiq:
`file.watch()` yoki `directory.watch()` fayllardagi o'zgarishlarni kuzatib Hot Reload kabi mexanizmlarni yaratishga imkon beradi.

## Ishlash natijasi:
```text
Fayl hodisasi yuz berdi: FileSystemEvent.modify
```

# 835-Topshiriq: Jurnal aylanishi (Log Rotation mexanizmi)

## Topshiriq sharti:
Log fayli ma'lum hajmga (masalan 100 bayt) yetganda uni arxivlab yangi fayl ochuvchi tizim tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:io';

class LogAylantirgich {
  final String path;
  final int maxBayt;

  LogAylantirgich(this.path, this.maxBayt);

  Future<void> yozish(String msg) async {
    var f = File(path);
    if (await f.exists() && await f.length() >= maxBayt) {
      await f.rename('$path.old');
      print('Log fayli limitga yetdi va arxivlandi.');
    }
    await File(path).writeAsString('$msg
', mode: FileMode.append);
  }
}

void main() async {
  var logger = LogAylantirgich('app.log', 40);
  await logger.yozish('1-qator juda uzun log xabari');
  await logger.yozish('2-qator yana bir log xabari');

  if (await File('app.log').exists()) await File('app.log').delete();
  if (await File('app.log.old').exists()) await File('app.log.old').delete();
}
```

## Tushuntirish va Mantiq:
Log rotation diskning to'lib qolishini oldini oluvchi server va ilova standart amaliyotidir.

## Ishlash natijasi:
```text
Log fayli limitga yetdi va arxivlandi.
```

# 836-Topshiriq: .env muhit faylini o'qish va tahlil qilish

## Topshiriq sharti:
Kalit=Qiymat formatidagi `.env` faylini o'qib Map ga aylantiruvchi dastur yozing.

## Yechim (Dart kodi):
```dart
import 'dart:io';

Future<Map<String, String>> loadEnv(String path) async {
  var file = File(path);
  Map<String, String> env = {};

  for (var line in await file.readAsLines()) {
    var trim = line.trim();
    if (trim.isEmpty || trim.startsWith('#')) continue;
    var parts = trim.split('=');
    if (parts.length == 2) {
      env[parts[0].trim()] = parts[1].trim();
    }
  }
  return env;
}

void main() async {
  var f = File('.env.test');
  await f.writeAsString('PORT=8080
DB_HOST=localhost
# Izoh');

  var config = await loadEnv('.env.test');
  print('Yuklangan PORT: ${config["PORT"]}');
  print('Yuklangan DB_HOST: ${config["DB_HOST"]}');

  if (await f.exists()) await f.delete();
}
```

## Tushuntirish va Mantiq:
Muhit o'zgaruvchilari maxfiy kalitlar va sozlamalarni koddan tashqarida xavfsiz saqlash uchun ishlatiladi.

## Ishlash natijasi:
```text
Yuklangan PORT: 8080
Yuklangan DB_HOST: localhost
```

# 837-Topshiriq: XML ma'lumotlarini oddiy tahlil qilish

## Topshiriq sharti:
Oddiy XML teglari orasidagi matnni RegExp orqali ajratib oluvchi yordamchi tuzing.

## Yechim (Dart kodi):
```dart
String? xmlTegQiymati(String xml, String teg) {
  var reg = RegExp('<$teg>(.*?)</$teg>');
  return reg.firstMatch(xml)?.group(1);
}

void main() {
  String xml = '<foydalanuvchi><ism>Sarvar</ism><yosh>30</yosh></foydalanuvchi>';

  print('Ism: ${xmlTegQiymati(xml, "ism")}');
  print('Yosh: ${xmlTegQiymati(xml, "yosh")}');
}
```

## Tushuntirish va Mantiq:
Eski tizimlar bilan integratsiyada XML ma'lumotlarini xavfsiz parse qilish zarurati tug'iladi.

## Ishlash natijasi:
```text
Ism: Sarvar
Yosh: 30
```

# 838-Topshiriq: Fayl ruxsatlari va rejimlarini tekshirish

## Topshiriq sharti:
Fayl atributlarini (fayl yoki katalog ekanligini) `FileSystemEntity.type` orqali aniqlang.

## Yechim (Dart kodi):
```dart
import 'dart:io';

void main() async {
  var f = File('stat_sinov.txt');
  await f.create();

  var tur = await FileSystemEntity.type(f.path);
  print('Fayl turi: $tur');

  if (await f.exists()) await f.delete();
}
```

## Tushuntirish va Mantiq:
`FileSystemEntity.type` yo'l mavjudligini va uning fayl, katalog yoki havola (link) ekanligini bildiradi.

## Ishlash natijasi:
```text
Fayl turi: FileSystemEntityType.file
```

# 839-Topshiriq: Xavfsiz vaqtinchalik papka bilan ishlash (WithTempDir)

## Topshiriq sharti:
Ish yakunlangach avtomatik o'chib ketuvchi vaqtinchalik muhit yaratuvchi yordamchi yozing.

## Yechim (Dart kodi):
```dart
import 'dart:io';

Future<T> withTempDirectory<T>(Future<T> Function(Directory) amal) async {
  var temp = await Directory.systemTemp.createTemp('uzb_ai_');
  try {
    return await amal(temp);
  } finally {
    if (await temp.exists()) await temp.delete(recursive: true);
  }
}

void main() async {
  await withTempDirectory((dir) async {
    print('Vaqtinchalik papka yaratildi: ${dir.path.contains("uzb_ai_")}');
    var f = File('${dir.path}/test.txt');
    await f.writeAsString('Salom');
    print('Fayl yozildi: ${await f.exists()}');
  });
  print('Vaqtinchalik papka to\'liq tozalandi.');
}
```

## Tushuntirish va Mantiq:
Avtomatlashgan testlarda vaqtincha fayllarni tozalash (cleanup) Loan naqshi orqali kafolatlanadi.

## Ishlash natijasi:
```text
Vaqtinchalik papka yaratildi: true
Fayl yozildi: true
Vaqtinchalik papka to'liq tozalandi.
```

# 840-Topshiriq: Binary protokollar uchun Serialization / Deserialization

## Topshiriq sharti:
Obyektni ixcham ikkilik formatga o'tkazuvchi va qayta tiklovchi klass tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:typed_data';

class BinarXabar {
  final int id;
  final int qiymat;

  BinarXabar(this.id, this.qiymat);

  Uint8List toBytes() {
    var b = Uint8List(4);
    var bd = ByteData.view(b.buffer);
    bd.setUint16(0, id);
    bd.setUint16(2, qiymat);
    return b;
  }

  factory BinarXabar.fromBytes(Uint8List bytes) {
    var bd = ByteData.view(bytes.buffer);
    return BinarXabar(bd.getUint16(0), bd.getUint16(2));
  }
}

void main() {
  var x = BinarXabar(101, 550);
  var bytes = x.toBytes();
  print('Binar baytlar: $bytes');

  var tiklangan = BinarXabar.fromBytes(bytes);
  print('Tiklandi: id=${tiklangan.id}, qiymat=${tiklangan.qiymat}');
}
```

## Tushuntirish va Mantiq:
Binar protokollar JSON ga nisbatan 5-10 baravar kamroq joy egallaydi va tezkor almashiladi.

## Ishlash natijasi:
```text
Binar baytlar: [0, 101, 2, 38]
Tiklandi: id=101, qiymat=550
```

# 841-Topshiriq: Fayl orqali IPC (Jarayonlararo aloqa) simulyatsiyasi

## Topshiriq sharti:
Bitta faylni signal berish kanali sifatida ishlatuvchi sodda IPC mexanizmini yozing.

## Yechim (Dart kodi):
```dart
import 'dart:io';

Future<void> signalYuborish(String buyruq) async {
  await File('ipc_signal.cmd').writeAsString(buyruq);
}

Future<String?> signalOqish() async {
  var f = File('ipc_signal.cmd');
  if (await f.exists()) {
    String c = await f.readAsString();
    await f.delete();
    return c;
  }
  return null;
}

void main() async {
  await signalYuborish('RELOAD_AI_MODEL');
  var buyruq = await signalOqish();
  print('IPC orqali qabul qilingan buyruq: $buyruq');
}
```

## Tushuntirish va Mantiq:
Faylli signallar turli jarayonlar orasida oddiy va ishonchli xabar almashish imkonini beradi.

## Ishlash natijasi:
```text
IPC orqali qabul qilingan buyruq: RELOAD_AI_MODEL
```

# 842-Topshiriq: Faylni teng bo'laklarga (Sharding/Chunking) bo'lish

## Topshiriq sharti:
Katta ma'lumotlarni belgilangan hajmdagi bir nechta kichik fayllarga bo'lib saqlang.

## Yechim (Dart kodi):
```dart
import 'dart:io';

Future<void> shardFayl(List<int> ma'lumotlar, int shardHajmi) async {
  int sanoq = 0;
  for (int i = 0; i < ma'lumotlar.length; i += shardHajmi) {
    int oxir = (i + shardHajmi < ma'lumotlar.length) ? i + shardHajmi : ma'lumotlar.length;
    var bolak = ma'lumotlar.sublist(i, oxir);
    sanoq++;
    await File('part_$sanoq.bin').writeAsBytes(bolak);
  }
  print('$sanoq ta qismga bo\'lindi.');

  // Tozalash
  for (int i = 1; i <= sanoq; i++) {
    await File('part_$i.bin').delete();
  }
}

void main() async {
  List<int> kattaData = List.generate(25, (i) => i);
  await shardFayl(kattaData, 10);
}
```

## Tushuntirish va Mantiq:
Sharding katta AI vaznlari yoki arxivlarni uzatishda yuklamani kamaytiradi.

## Ishlash natijasi:
```text
3 ta qismga bo'lindi.
```

# 843-Topshiriq: Fayl keshini TTL bo'yicha tozalash (Cache Expiry)

## Topshiriq sharti:
Belgilangan daqiqadan eski bo'lgan kesh fayllarini avtomatik o'chiruvchi xizmat tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:io';

Future<void> eskirganlarniTozalash(Directory dir, Duration maxYoshi) async {
  var now = DateTime.now();
  int ochirildi = 0;

  await for (var entity in dir.list()) {
    if (entity is File) {
      var yosh = now.difference(await entity.lastModified());
      if (yosh > maxYoshi) {
        await entity.delete();
        ochirildi++;
      }
    }
  }
  print('$ochirildi ta eskirgan kesh fayli tozalandi.');
}

void main() async {
  var d = Directory('kesh_papka');
  await d.create();
  await File('kesh_papka/a.tmp').create();

  await eskirganlarniTozalash(d, Duration(seconds: 0));
  await d.delete(recursive: true);
}
```

## Tushuntirish va Mantiq:
Kesh tozalash xizmati disk to'lib qolmasligini muntazam ta'minlab turadi.

## Ishlash natijasi:
```text
1 ta eskirgan kesh fayli tozalandi.
```

# 844-Topshiriq: Binar Model Fayli Header (Sarlavha) tuzilishi

## Topshiriq sharti:
Model faylining boshida Magic number, Versiya va O'lchamlarni saqlovchi sarlavha tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:typed_data';

class ModelSarlavhasi {
  final int magic; // 0x4249544E ('BITN')
  final int versiya;
  final int qatorlar;
  final int ustunlar;

  ModelSarlavhasi(this.magic, this.versiya, this.qatorlar, this.ustunlar);

  Uint8List toBytes() {
    var b = Uint8List(16);
    var bd = ByteData.view(b.buffer);
    bd.setUint32(0, magic);
    bd.setUint32(4, versiya);
    bd.setUint32(8, qatorlar);
    bd.setUint32(12, ustunlar);
    return b;
  }
}

void main() {
  var hdr = ModelSarlavhasi(0x4249544E, 1, 1024, 1024);
  var bytes = hdr.toBytes();

  print('Header hajmi: ${bytes.length} bayt');
  print('Sehrli raqam: 0x${hdr.magic.toRadixString(16).toUpperCase()}');
}
```

## Tushuntirish va Mantiq:
Barcha professional ikkilik formatlar (ELF, PNG, BitNet GGUF) fayl boshida o'ziga xos sarlavha (Header) saqlaydi.

## Ishlash natijasi:
```text
Header hajmi: 16 bayt
Sehrli raqam: 0x4249544E
```

# 845-Topshiriq: Qator bo'yicha JSON loglarini o'qish (JSONL formati)

## Topshiriq sharti:
Har bir qatori alohida JSON bo'lgan JSONL faylini o'qib tahlil qiling.

## Yechim (Dart kodi):
```dart
import 'dart:convert';

void main() {
  String jsonl = '''{"id": 1, "status": "ok"}
{"id": 2, "status": "error"}
{"id": 3, "status": "ok"}''';

  var qatorlar = jsonl.split('
');
  int xatolar = 0;

  for (var satr in qatorlar) {
    if (satr.trim().isEmpty) continue;
    var j = jsonDecode(satr);
    if (j['status'] == 'error') xatolar++;
  }

  print('JSONL dagi xatolar soni: $xatolar');
}
```

## Tushuntirish va Mantiq:
JSON Lines (.jsonl) formati katta hajmdagi datasetlar va loglarni oqimli o'qish uchun eng qulay standartdir.

## Ishlash natijasi:
```text
JSONL dagi xatolar soni: 1
```

# 846-Topshiriq: Parollangan fayl formati simulyatsiyasi (XOR Obfuscation)

## Topshiriq sharti:
Faylni oddiy baytlar niqoblash (obfuscation) bilan saqlash va qayta ochish.

## Yechim (Dart kodi):
```dart
import 'dart:typed_data';

Uint8List xorNiqob(Uint8List data, int kalit) {
  var out = Uint8List(data.length);
  for (int i = 0; i < data.length; i++) {
    out[i] = data[i] ^ kalit;
  }
  return out;
}

void main() {
  var original = Uint8List.fromList([1, 2, 3, 4]);
  var shifrlangan = xorNiqob(original, 0xAA);
  var qaytarilgan = xorNiqob(shifrlangan, 0xAA);

  print('Asl: $original');
  print('Niqoblangan: $shifrlangan');
  print('Qayta tiklangan: $qaytarilgan');
}
```

## Tushuntirish va Mantiq:
XOR xususiyati ($A \oplus K \oplus K = A$) eng tezkor ma'lumotlarni niqoblash imkonini beradi.

## Ishlash natijasi:
```text
Asl: [1, 2, 3, 4]
Niqoblangan: [171, 168, 169, 174]
Qayta tiklangan: [1, 2, 3, 4]
```

# 847-Topshiriq: Stream orqali fayl xeshini hisoblash

## Topshiriq sharti:
Xotiraga to'liq yuklamasdan oqim orqali fayl nazorat yig'indisini aniqlash.

## Yechim (Dart kodi):
```dart
import 'dart:io';

Future<int> streamHash(File f) async {
  int h = 0;
  await for (var chunk in f.openRead()) {
    for (var b in chunk) {
      h = (h * 31 + b) & 0x7FFFFFFF;
    }
  }
  return h;
}

void main() async {
  var f = File('hash_sinov.txt');
  await f.writeAsString('AI model tekshiruvi');

  int hash = await streamHash(f);
  print('Oqimli xesh: $hash');

  if (await f.exists()) await f.delete();
}
```

## Tushuntirish va Mantiq:
Katta fayllarning xeshini xotiradan oshib ketmasdan hisoblash uchun oqim zarur.

## Ishlash natijasi:
```text
Oqimli xesh: 1845946197
```

# 848-Topshiriq: Faylni xavfsiz zaxira qilish (Backup copy)

## Topshiriq sharti:
O'zgartirish kiritishdan oldin faylning `.bak` nusxasini yaratib qo'yuvchi mexanizm yozing.

## Yechim (Dart kodi):
```dart
import 'dart:io';

Future<void> zaxiraQilish(String path) async {
  var f = File(path);
  if (await f.exists()) {
    await f.copy('$path.bak');
    print('Zaxira nusxa yaratildi: $path.bak');
  }
}

void main() async {
  var f = File('asosiy.db');
  await f.writeAsString('muhim baza ma\'lumoti');

  await zaxiraQilish('asosiy.db');

  if (await File('asosiy.db').exists()) await File('asosiy.db').delete();
  if (await File('asosiy.db.bak').exists()) await File('asosiy.db.bak').delete();
}
```

## Tushuntirish va Mantiq:
Baza yoki konfiguratsiyani o'zgartirishdan oldin `.bak` nusxasini olish xavfsizlik qoidasidir.

## Ishlash natijasi:
```text
Zaxira nusxa yaratildi: asosiy.db.bak
```

# 849-Topshiriq: Katalog bo'yicha qidiruv (Rekursiv fayl topish)

## Topshiriq sharti:
Berilgan katalog va uning barcha ichki papkalaridan `.dart` kengaytmali fayllarni toping.

## Yechim (Dart kodi):
```dart
import 'dart:io';

Future<List<String>> findFiles(Directory dir, String kengaytma) async {
  List<String> topilganlar = [];
  await for (var entity in dir.list(recursive: true)) {
    if (entity is File && entity.path.endsWith(kengaytma)) {
      topilganlar.add(entity.path.replaceAll(r'\', '/'));
    }
  }
  return topilganlar;
}

void main() async {
  var d = Directory('d_test');
  await d.create();
  await File('d_test/main.dart').create();
  await File('d_test/readme.txt').create();

  var dartFayllar = await findFiles(d, '.dart');
  print('Topilgan Dart fayllar: $dartFayllar');

  await d.delete(recursive: true);
}
```

## Tushuntirish va Mantiq:
`list(recursive: true)` papka ichidagi barcha chuqur qatlamlarni aylanib chiqadi.

## Ishlash natijasi:
```text
Topilgan Dart fayllar: [d_test/main.dart]
```

# 850-Topshiriq: Amaliy: BitNet 1-bit Og'irliklarini Binary Faylga Saqlash va Xotiraga Yuklash

## Topshiriq sharti:
Ternar vaznlarni {-1, 0, +1} ikkilik faylga saqlab, so'ngra diskdan qayta yuklab matritsa ko'paytirishni bajaring.

## Yechim (Dart kodi):
```dart
import 'dart:io';
import 'dart:typed_data';

class BitNetModelStorage {
  static Future<void> saveWeights(String path, List<int> weights) async {
    // 0 -> 0, 1 -> 1, -1 -> 2 deb kodlaymiz (har biri 1 bayt)
    var bytes = Uint8List(weights.length);
    for (int i = 0; i < weights.length; i++) {
      if (weights[i] == 1) bytes[i] = 1;
      else if (weights[i] == -1) bytes[i] = 2;
      else bytes[i] = 0;
    }
    await File(path).writeAsBytes(bytes);
  }

  static Future<List<int>> loadWeights(String path) async {
    var bytes = await File(path).readAsBytes();
    List<int> weights = List.filled(bytes.length, 0);
    for (int i = 0; i < bytes.length; i++) {
      if (bytes[i] == 1) weights[i] = 1;
      else if (bytes[i] == 2) weights[i] = -1;
      else weights[i] = 0;
    }
    return weights;
  }
}

void main() async {
  String modelPath = 'bitnet_layer1.bin';
  List<int> aslVaznlar = [1, 0, -1, 1, -1, 0];

  await BitNetModelStorage.saveWeights(modelPath, aslVaznlar);
  print('BitNet vaznlari binary faylga yozildi.');

  var yuklangan = await BitNetModelStorage.loadWeights(modelPath);
  print('Yuklangan vaznlar: $yuklangan');

  if (await File(modelPath).exists()) await File(modelPath).delete();
}
```

## Tushuntirish va Mantiq:
BitNet b1.58 vaznlarini ikkilik formatda diskka saqlash va yuklash mobil qurilmalarda AI xotirasini tejashning poydevori hisoblanadi.

## Ishlash natijasi:
```text
BitNet vaznlari binary faylga yozildi.
Yuklangan vaznlar: [1, 0, -1, 1, -1, 0]
```

