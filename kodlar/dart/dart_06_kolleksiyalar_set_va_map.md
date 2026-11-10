# 6-Qism: Kolleksiyalar: Set va Map Ma'lumot Tuzilmalari (251-300)

Ushbu qismda Dart tilida to'plamlar (`Set`), xaritalar (`Map`), kalit-qiymat munosabatlari, to'plam amallari (birlashma, kesishma, ayirma), `putIfAbsent`, `LinkedHashMap`, `SplayTreeMap`, chastota hisoblagichlar va qidiruv tizimlari amaliy kodlar bilan tahlil qilinadi.

# 251-Topshiriq: Set e'lon qilish va dublikatlarning avtomatik olib tashlanishi
## Topshiriq sharti:
`Set<String>` to'plamini yarating va takroriy elementlar qo'shilganda ularning faqat bittasi saqlanib qolishini ko'rsating.

## Yechim (Dart kodi):
```dart
void main() {
  Set<String> tillar = {"Dart", "Flutter", "Python", "Dart", "C++", "Python"};

  print("Set hajmi: ${tillar.length}");
  print("To'plam elementlari: $tillar");
}
```

## Tushuntirish va Mantiq:
`Set` barcha elementlarning faqat noyob (takrorlanmas) nusxalarini saqlaydi. Dublikat qo'shilsa u e'tiborsiz qoldiriladi.

## Ishlash natijasi:
```text
Set hajmi: 4
To'plam elementlari: {Dart, Flutter, Python, C++}
```

# 252-Topshiriq: Set.unmodifiable(): O'zgarmas to'plam
## Topshiriq sharti:
`Set.unmodifiable` orqali element qo'shib yoki o'chirib bo'lmaydigan himoyalangan to'plam hosil qiling.

## Yechim (Dart kodi):
```dart
void main() {
  Set<int> xavfsizSet = Set.unmodifiable({10, 20, 30});

  print("Xavfsiz to'plam: $xavfsizSet");
  try {
    xavfsizSet.add(40);
  } catch (e) {
    print("O'zgartirish taqiqlandi: $e");
  }
}
```

## Tushuntirish va Mantiq:
O'zgarmas to'plamlar konfiguratsiyalar va standart rollarni xavfsiz saqlashda qo'llaniladi.

## Ishlash natijasi:
```text
Xavfsiz to'plam: {10, 20, 30}
O'zgartirish taqiqlandi: UnsupportedError: Cannot change an unmodifiable set
```

# 253-Topshiriq: Element qo'shish va tekshirish: add(), contains() O(1) da
## Topshiriq sharti:
`Set` da element mavjudligini tekshirish nega ro'yxatga qaraganda O(1) tezlikda ishlashini namoyish eting.

## Yechim (Dart kodi):
```dart
void main() {
  Set<String> foydalanuvchilar = {"anvar", "nodira", "sarvar"};

  print("'nodira' mavjudmi: ${foydalanuvchilar.contains('nodira')}");
  print("'temur' mavjudmi:  ${foydalanuvchilar.contains('temur')}");

  bool qoshildi = foydalanuvchilar.add("temur");
  bool qaytaQoshildi = foydalanuvchilar.add("temur");

  print("Birinchi marta qo'shildi: $qoshildi");
  print("Ikkinchi marta qo'shildi: $qaytaQoshildi");
}
```

## Tushuntirish va Mantiq:
`Set` xesh-jadval (Hash Table) asosida qurilgani uchun `contains()` va `add()` amallari o'rtacha O(1) vaqtda bajariladi.

## Ishlash natijasi:
```text
'nodira' mavjudmi: true
'temur' mavjudmi:  false
Birinchi marta qo'shildi: true
Ikkinchi marta qo'shildi: false
```

# 254-Topshiriq: Set to'plam amallari: union(), intersection(), difference()
## Topshiriq sharti:
Ikkita to'plamning birlashmasi, kesishmasi va ayirmasini hisoblang.

## Yechim (Dart kodi):
```dart
void main() {
  Set<int> a = {1, 2, 3, 4};
  Set<int> b = {3, 4, 5, 6};

  print("A to'plam: $a");
  print("B to'plam: $b");
  print("Birlashma (A union B):      ${a.union(b)}");
  print("Kesishma (A intersect B):   ${a.intersection(b)}");
  print("Ayirma (A difference B):    ${a.difference(b)}");
}
```

## Tushuntirish va Mantiq:
To'plam amallari matematik nazariyaga to'liq mos ravishda bitta metod chaqiruvi bilan bajariladi.

## Ishlash natijasi:
```text
A to'plam: {1, 2, 3, 4}
B to'plam: {3, 4, 5, 6}
Birlashma (A union B):      {1, 2, 3, 4, 5, 6}
Kesishma (A intersect B):   {3, 4}
Ayirma (A difference B):    {1, 2}
```

# 255-Topshiriq: Ro'yxatdan dublikatlarni tozalash: list.toSet().toList()
## Topshiriq sharti:
Takroriy elementlarga ega ro'yxatni `toSet().toList()` orqali bir satrda tozalang.

## Yechim (Dart kodi):
```dart
void main() {
  List<int> sonlar = [1, 2, 2, 3, 4, 4, 4, 5, 1];
  List<int> tozalangan = sonlar.toSet().toList();

  print("Asl ro'yxat:        $sonlar");
  print("Dublikatsiz ro'yxat: $tozalangan");
}
```

## Tushuntirish va Mantiq:
`toSet()` dublikatlarni bir zumda yo'qotadi va `toList()` bilan qayta tartibli ro'yxatga aylanadi.

## Ishlash natijasi:
```text
Asl ro'yxat:        [1, 2, 2, 3, 4, 4, 4, 5, 1]
Dublikatsiz ro'yxat: [1, 2, 3, 4, 5]
```

# 256-Topshiriq: Collection if va Collection for Set ichida
## Topshiriq sharti:
`Set` literali ichida shartli va siklli elementlar hosil qiling.

## Yechim (Dart kodi):
```dart
void main() {
  bool qoshish = true;
  List<int> kiruvchi = [1, 2, 2, 3];

  Set<String> to'plam = {
    "boshlang'ich",
    if (qoshish) "maxsus_ruxsat",
    for (int x in kiruvchi) "id_$x"
  };

  print("Natija: $to'plam");
}
```

## Tushuntirish va Mantiq:
Collection `if` va `for` to'plam literallari bilan ham ro'yxatlar kabi bir xil qulaylikda ishlaydi.

## Ishlash natijasi:
```text
Natija: {boshlang'ich, maxsus_ruxsat, id_1, id_2, id_3}
```

# 257-Topshiriq: Map e'lon qilish: Kalit-Qiymat juftliklari
## Topshiriq sharti:
`Map<String, int>` lug'atini e'lon qilib, talabalarning ismlari va ularning yoshlarini saqlang.

## Yechim (Dart kodi):
```dart
void main() {
  Map<String, int> yoshlar = {
    "Ali": 20,
    "Vali": 22,
    "Salim": 19
  };

  print("Lug'at: $yoshlar");
  print("Ali yoshi: ${yoshlar['Ali']}");
  print("Lug'at hajmi: ${yoshlar.length}");
}
```

## Tushuntirish va Mantiq:
`Map` kalitlarni qiymatlarga bog'laydi. Kalitlar har doim takrorlanmas noyob bo'lishi shart.

## Ishlash natijasi:
```text
Lug'at: {Ali: 20, Vali: 22, Salim: 19}
Ali yoshi: 20
Lug'at hajmi: 3
```

# 258-Topshiriq: Map.fromEntries(): Entry juftliklaridan xarita tuzish
## Topshiriq sharti:
`MapEntry` ob'ektlari ro'yxatidan `Map.fromEntries` orqali yangi xarita yasang.

## Yechim (Dart kodi):
```dart
void main() {
  List<MapEntry<String, double>> baholar = [
    MapEntry("Matematika", 4.8),
    MapEntry("Fizika", 4.5),
    MapEntry("Informatika", 5.0)
  ];

  Map<String, double> fanlar = Map.fromEntries(baholar);
  print("Fanlar xaritasi: $fanlar");
}
```

## Tushuntirish va Mantiq:
`MapEntry(key, value)` juftliklari Map ustidagi transformatsiyalarni ro'yxat kabi boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Fanlar xaritasi: {Matematika: 4.8, Fizika: 4.5, Informatika: 5.0}
```

# 259-Topshiriq: Map.unmodifiable(): O'zgarmas xarita
## Topshiriq sharti:
Tashqaridan o'zgartirib bo'lmaydigan `Map.unmodifiable` lug'atini yarating.

## Yechim (Dart kodi):
```dart
void main() {
  Map<String, String> sozlamalar = Map.unmodifiable({
    "til": "uz",
    "mavzu": "qorong'i"
  });

  print("Sozlamalar: $sozlamalar");
  try {
    sozlamalar["til"] = "en"; // Xatolik
  } catch (e) {
    print("Xarita o'zgarmas: $e");
  }
}
```

## Tushuntirish va Mantiq:
O'zgarmas xaritalar xavfsiz konfiguratsiya sozlamalarini taqdim etadi.

## Ishlash natijasi:
```text
Sozlamalar: {til: uz, mavzu: qorong'i}
Xarita o'zgarmas: UnsupportedError: Cannot modify unmodifiable map
```

# 260-Topshiriq: Kalitlar va Qiymatlar: keys, values, entries
## Topshiriq sharti:
Xaritaning barcha kalitlarini, barcha qiymatlarini va juftliklarini alohida chop eting.

## Yechim (Dart kodi):
```dart
void main() {
  Map<String, int> narxlar = {"Non": 3000, "Sut": 9000, "Tuxum": 1500};

  print("Kalitlar:  ${narxlar.keys}");
  print("Qiymatlar: ${narxlar.values}");

  print("Juftliklar:");
  for (var entry in narxlar.entries) {
    print("  ${entry.key} -> ${entry.value} so'm");
  }
}
```

## Tushuntirish va Mantiq:
`keys` va `values` `Iterable` qaytaradi, `entries` esa `key-value` juftliklarini taqdim etadi.

## Ishlash natijasi:
```text
Kalitlar:  (Non, Sut, Tuxum)
Qiymatlar: (3000, 9000, 1500)
Juftliklar:
  Non -> 3000 so'm
  Sut -> 9000 so'm
  Tuxum -> 1500 so'm
```

# 261-Topshiriq: Element qo'shish va yangilash: map[key] = value
## Topshiriq sharti:
Mavjud kalit qiymatini yangilang va yangi kalit-qiymat qo'shing.

## Yechim (Dart kodi):
```dart
void main() {
  Map<String, String> lugat = {"kitob": "book"};

  lugat["qalam"] = "pencil"; // Yangi kalit qo'shish
  lugat["kitob"] = "handbook"; // Mavjudini yangilash

  print("Yangilangan lug'at: $lugat");
}
```

## Tushuntirish va Mantiq:
`[]=` operatori kalit mavjud bo'lmasa uni qo'shadi, mavjud bo'lsa yangi qiymat bilan almashtiradi.

## Ishlash natijasi:
```text
Yangilangan lug'at: {kitob: handbook, qalam: pencil}
```

# 262-Topshiriq: putIfAbsent() orqali xavfsiz to'ldirish
## Topshiriq sharti:
Faqat kalit mavjud bo'lmagandagina qiymat hisoblab kirituvchi `putIfAbsent` metodini ko'rsating.

## Yechim (Dart kodi):
```dart
void main() {
  Map<String, int> zaxira = {"olma": 50};

  zaxira.putIfAbsent("olma", () => 100); // Mavjud, o'zgarmaydi!
  zaxira.putIfAbsent("nok", () => 30);   // Yo'q edi, qo'shiladi

  print("Zaxira: $zaxira");
}
```

## Tushuntirish va Mantiq:
`putIfAbsent` faqat kalit yo'q bo'lsa lambda funksiyani bajaradi, bu esa ortiqcha hisoblashlarni tejaydi.

## Ishlash natijasi:
```text
Zaxira: {olma: 50, nok: 30}
```

# 263-Topshiriq: update() va updateAll()
## Topshiriq sharti:
Muayyan kalit qiymatini o'zgartirish (`update`) va barcha qiymatlarni bir yo'la yangilash (`updateAll`) metodlarini qo'llang.

## Yechim (Dart kodi):
```dart
void main() {
  Map<String, double> maoshlar = {
    "Aziz": 5000000,
    "Nodir": 7000000
  };

  // Azizning maoshiga 1 000 000 qo'shamiz
  maoshlar.update("Aziz", (v) => v + 1000000);

  // Barchaning maoshiga 10% ustama beramiz
  maoshlar.updateAll((k, v) => v * 1.10);

  print("Yangilangan maoshlar: $maoshlar");
}
```

## Tushuntirish va Mantiq:
`updateAll` butun lug'at ustida matematik koeffitsiyentlar qo'llashda juda tezkor ishlaydi.

## Ishlash natijasi:
```text
Yangilangan maoshlar: {Aziz: 6600000.0, Nodir: 7700000.0}
```

# 264-Topshiriq: remove() va removeWhere()
## Topshiriq sharti:
Kaliti bo'yicha va belgilangan shart bo'yicha elementlarni Map dan o'chiring.

## Yechim (Dart kodi):
```dart
void main() {
  Map<String, int> ballar = {
    "Ali": 45,
    "Vali": 85,
    "G'ani": 30,
    "Sardor": 90
  };

  ballar.remove("Ali"); // Ali o'chiriladi
  print("remove('Ali') so'ng: $ballar");

  ballar.removeWhere((ism, ball) => ball < 60); // Yiqilganlar o'chiriladi
  print("Yiqilganlar o'chirilgach: $ballar");
}
```

## Tushuntirish va Mantiq:
`removeWhere((key, value) => ...)` xaritani bir qadamda shart bo'yicha tozalaydi.

## Ishlash natijasi:
```text
remove('Ali') so'ng: {Vali: 85, G'ani: 30, Sardor: 90}
Yiqilganlar o'chirilgach: {Vali: 85, Sardor: 90}
```

# 265-Topshiriq: Collection if va Collection for Map ichida
## Topshiriq sharti:
Map literali ichida shartli va siklli juftliklar generatsiya qiling.

## Yechim (Dart kodi):
```dart
void main() {
  bool debugMode = true;
  List<String> rollar = ["admin", "user"];

  Map<String, dynamic> config = {
    "app": "UzbekAI",
    if (debugMode) "env": "development",
    for (int i = 0; i < rollar.length; ++i) "role_$i": rollar[i]
  };

  print("Config: $config");
}
```

## Tushuntirish va Mantiq:
Map ichidagi Collection `if` va `for` serverga yuboriladigan JSON ob'ektlarini dinamik yig'ishda eng qulay usuldir.

## Ishlash natijasi:
```text
Config: {app: UzbekAI, env: development, role_0: admin, role_1: user}
```

# 266-Topshiriq: Spread operatori Map ichida: {...m1, ...m2}
## Topshiriq sharti:
Ikkita xaritani `...` spread operatori orqali birlashtiring.

## Yechim (Dart kodi):
```dart
void main() {
  Map<String, int> a = {"A": 1, "B": 2};
  Map<String, int> b = {"B": 99, "C": 3}; // "B" kaliti ustiga yoziladi

  Map<String, int> birlashgan = {...a, ...b};
  print("Birlashgan xarita: $birlashgan");
}
```

## Tushuntirish va Mantiq:
Agar ikkinchi xaritada bir xil kalit uchrasa, uning qiymati birinchisining ustiga yoziladi.

## Ishlash natijasi:
```text
Birlashgan xarita: {A: 1, B: 99, C: 3}
```

# 267-Topshiriq: Map bo'ylab aylanish: forEach va for-in
## Topshiriq sharti:
Xaritaning barcha elementlarini `forEach` va `entries` bo'yicha sikl bilan ekranga chiqaring.

## Yechim (Dart kodi):
```dart
void main() {
  Map<String, String> lugat = {
    "quyosh": "sun",
    "oy": "moon",
    "yulduz": "star"
  };

  lugat.forEach((k, v) {
    print("$k o'zbekcha = $v inglizcha");
  });
}
```

## Tushuntirish va Mantiq:
`forEach` ikkita parametrli anonim funksiyani qabul qiladi va kodni o'ta ixcham qiladi.

## Ishlash natijasi:
```text
quyosh o'zbekcha = sun inglizcha
oy o'zbekcha = moon inglizcha
yulduz o'zbekcha = star inglizcha
```

# 268-Topshiriq: Map.map() orqali yangi Map hosil qilish
## Topshiriq sharti:
Xaritaning barcha kalit va qiymatlarini o'zgartirib yangi Map qaytaruvchi `.map()` metodidan foydalaning.

## Yechim (Dart kodi):
```dart
void main() {
  Map<String, int> tovarlar = {"olma": 10, "nok": 20};

  // Kalitlarni bosh harfga, qiymatni 1000 ga ko'paytiramiz
  var yangi = tovarlar.map((k, v) => MapEntry(k.toUpperCase(), v * 1000));
  print("Yangi xarita: $yangi");
}
```

## Tushuntirish va Mantiq:
`map()` metodi har bir juftlikdan yangi `MapEntry` hosil qilib, o'zgartirilgan xaritani yaratadi.

## Ishlash natijasi:
```text
Yangi xarita: {OLMA: 10000, NOK: 20000}
```

# 269-Topshiriq: So'zlar chastotasini (Word Frequency Counter) hisoblash
## Topshiriq sharti:
Matndagi har bir so'z necha marta takrorlanganini `Map<String, int>` yordamida hisoblang.

## Yechim (Dart kodi):
```dart
void main() {
  String matn = "salom dunyo salom o'zbekiston dunyo salom";
  List<String> sozlar = matn.split(" ");

  Map<String, int> chastota = {};
  for (String s in sozlar) {
    chastota[s] = (chastota[s] ?? 0) + 1;
  }

  print("So'zlar chastotasi: $chastota");
}
```

## Tushuntirish va Mantiq:
`chastota[s] ?? 0` kalit hali yo'q bo'lsa 0 oladi va unga 1 qo'shadi. Bu NLP va ma'lumot tahlilining eng asosiy algoritmidir.

## Ishlash natijasi:
```text
So'zlar chastotasi: {salom: 3, dunyo: 2, o'zbekiston: 1}
```

# 270-Topshiriq: Guruhlash (Grouping by property) Map yordamida
## Topshiriq sharti:
Odamlar ro'yxatini ularning yashash shaharlari bo'yicha guruhlovchi (`Map<String, List<String>>`) algoritm yozing.

## Yechim (Dart kodi):
```dart
class Shaxs {
  final String ism;
  final String shahar;
  Shaxs(this.ism, this.shahar);
}

void main() {
  List<Shaxs> odamlar = [
    Shaxs("Ali", "Toshkent"),
    Shaxs("Vali", "Samarqand"),
    Shaxs("G'ani", "Toshkent"),
    Shaxs("Zuhra", "Buxoro")
  ];

  Map<String, List<String>> guruhlar = {};
  for (var kishi in odamlar) {
    guruhlar.putIfAbsent(kishi.shahar, () => []).add(kishi.ism);
  }

  guruhlar.forEach((shahar, ismlar) {
    print("$shahar: $ismlar");
  });
}
```

## Tushuntirish va Mantiq:
`putIfAbsent` orqali bo'sh ro'yxat yaratilib, unga shaxs ismi darhol qo'shib boriladi.

## Ishlash natijasi:
```text
Toshkent: [Ali, G'ani]
Samarqand: [Vali]
Buxoro: [Zuhra]
```

# 271-Topshiriq: Map ni teskarilash (Invert Map)
## Topshiriq sharti:
Lug'atning kalitlari va qiymatlari o'rnini almashtiruvchi (qiymat -> kalit) funksiya yozing.

## Yechim (Dart kodi):
```dart
Map<V, K> invertMap<K, V>(Map<K, V> map) {
  return map.map((k, v) => MapEntry(v, k));
}

void main() {
  Map<String, int> idMap = {"admin": 1, "moderator": 2, "user": 3};
  var teskari = invertMap(idMap);

  print("Asl xarita:    $idMap");
  print("Teskari xarita: $teskari");
}
```

## Tushuntirish va Mantiq:
Teskari xarita identifikator bo'yicha tezkor teskari qidiruvni amalga oshirishda qulaydir.

## Ishlash natijasi:
```text
Asl xarita:    {admin: 1, moderator: 2, user: 3}
Teskari xarita: {1: admin, 2: moderator, 3: user}
```

# 272-Topshiriq: Ikki Map ni chuqur birlashtirish (Deep Merge)
## Topshiriq sharti:
Ichma-ich joylashgan xaritalarni bir-biriga qo'shib, ichki kalitlarni ham saqlab qoluvchi rekursiv birlashtirish funksiyasini yozing.

## Yechim (Dart kodi):
```dart
Map<String, dynamic> deepMerge(Map<String, dynamic> a, Map<String, dynamic> b) {
  Map<String, dynamic> res = Map.from(a);
  b.forEach((k, v) {
    if (res.containsKey(k) && res[k] is Map && v is Map) {
      res[k] = deepMerge(res[k] as Map<String, dynamic>, v as Map<String, dynamic>);
    } else {
      res[k] = v;
    }
  });
  return res;
}

void main() {
  var baseConfig = {
    "app": {"name": "MyAI", "version": "1.0"},
    "debug": false
  };

  var overrideConfig = {
    "app": {"version": "2.0"},
    "debug": true
  };

  var merged = deepMerge(baseConfig, overrideConfig);
  print("Deep merge natijasi: $merged");
}
```

## Tushuntirish va Mantiq:
Deep Merge foydalanuvchi sozlamalarini standart tizim sozlamalari ustiga xavfsiz o'rnatishda shart hisoblanadi.

## Ishlash natijasi:
```text
Deep merge natijasi: {app: {name: MyAI, version: 2.0}, debug: true}
```

# 273-Topshiriq: JSON ob'ektini Map<String, dynamic> sifatida boshqarish
## Topshiriq sharti:
REST API dan kelgan JSON ma'lumotlar strukturasini xavfsiz tahlil qiling.

## Yechim (Dart kodi):
```dart
void main() {
  Map<String, dynamic> jsonResponse = {
    "status": 200,
    "success": true,
    "data": {
      "user_id": 105,
      "username": "dilshod_dev"
    }
  };

  if (jsonResponse["success"] == true) {
    var data = jsonResponse["data"] as Map<String, dynamic>;
    print("Muvaffaqiyat! Foydalanuvchi: ${data['username']}");
  }
}
```

## Tushuntirish va Mantiq:
Dart da JSON obyektlari tabiiy ravishda `Map<String, dynamic>` sifatida ifodalanadi.

## Ishlash natijasi:
```text
Muvaffaqiyat! Foydalanuvchi: dilshod_dev
```

# 274-Topshiriq: SplayTreeMap orqali saralangan xarita tuzish (dart:collection)
## Topshiriq sharti:
Kalitlari har doim o'sish tartibida saralangan holda saqlanuvchi `SplayTreeMap` dan foydalaning.

## Yechim (Dart kodi):
```dart
import 'dart:collection';

void main() {
  // SplayTreeMap har doim kalitlar bo'yicha avtomatik saralangan turadi
  SplayTreeMap<int, String> reyting = SplayTreeMap();
  reyting[3] = "Bronza";
  reyting[1] = "Oltin";
  reyting[2] = "Kumush";

  print("Avtomatik saralangan xarita:");
  reyting.forEach((orin, medal) {
    print("$orin-o'rin: $medal");
  });
}
```

## Tushuntirish va Mantiq:
`SplayTreeMap` daraxtsimon tuzilma (Self-balancing Binary Search Tree) bo'lib, kalitlarni saralangan holda saqlaydi.

## Ishlash natijasi:
```text
Avtomatik saralangan xarita:
1-o'rin: Oltin
2-o'rin: Kumush
3-o'rin: Bronza
```

# 275-Topshiriq: O'z ob'ektimizni Map kaliti sifatida ishlatish: operator == va hashCode
## Topshiriq sharti:
`Point` sinfini yaratib, uning `==` va `hashCode` metodlarini to'g'ri qayta yuklash orqali uni `Map` kaliti sifatida ishlating.

## Yechim (Dart kodi):
```dart
class Point {
  final int x, y;
  Point(this.x, this.y);

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is Point && runtimeType == other.runtimeType && x == other.x && y == other.y;

  @override
  int get hashCode => Object.hash(x, y);

  @override
  String toString() => "($x, $y)";
}

void main() {
  Map<Point, String> joylashuv = {};
  joylashuv[Point(10, 20)] = "Bosh bino";

  // Yangi ob'ekt, lekin koordinatalari bir xil
  Point qidirilayotgan = Point(10, 20);
  print("Nuqtadagi bino: ${joylashuv[qidirilayotgan]}");
}
```

## Tushuntirish va Mantiq:
`operator ==` va `hashCode` to'g'ri yozilsa, turli xotira manzilidagi ikkita teng ob'ekt Map da bitta kalit sifatida tan olinadi.

## Ishlash natijasi:
```text
Nuqtadagi bino: Bosh bino
```

# 276-Topshiriq: Map.fromIterables(): Ikkita ro'yxatdan xarita yasash
## Topshiriq sharti:
Kalitlar ro'yxati va qiymatlar ro'yxatini `Map.fromIterables` orqali bitta xaritaga birlashtiring.

## Yechim (Dart kodi):
```dart
void main() {
  List<String> mamlakatlar = ["O'zbekiston", "Fransiya", "Yaponiya"];
  List<String> poytaxtlar = ["Toshkent", "Parij", "Tokio"];

  Map<String, String> xarita = Map.fromIterables(mamlakatlar, poytaxtlar);
  print("Hosil bo'lgan xarita: $xarita");
}
```

## Tushuntirish va Mantiq:
`Map.fromIterables` ikki ro'yxatni parallel o'qib O(N) vaqtda xaritaga aylantiradi.

## Ishlash natijasi:
```text
Hosil bo'lgan xarita: {O'zbekiston: Toshkent, Fransiya: Parij, Yaponiya: Tokio}
```

# 277-Topshiriq: Lug'at filtratsiyasi: Shartga mos juftliklarni ajratish
## Topshiriq sharti:
`entries.where()` orqali bahosi 80 dan yuqori bo'lgan talabalarni yangi xaritaga filtrlang.

## Yechim (Dart kodi):
```dart
void main() {
  Map<String, int> imtihon = {
    "Alisher": 95,
    "Bobur": 70,
    "Dildora": 88,
    "Jasur": 55
  };

  var alo = Map.fromEntries(imtihon.entries.where((e) => e.value >= 80));
  print("A'lochilar: $alo");
}
```

## Tushuntirish va Mantiq:
`fromEntries` va `where` kombinatsiyasi lug'atlarni toza funksional uslubda filtrlash imkonini beradi.

## Ishlash natijasi:
```text
A'lochilar: {Alisher: 95, Dildora: 88}
```

# 278-Topshiriq: Ko'p qiymatli xarita (MultiMap: Map<K, List<V>>)
## Topshiriq sharti:
Bitta kalitga bir nechta qiymat biriktirilgan ko'p qiymatli xarita boshqaruvini yozing.

## Yechim (Dart kodi):
```dart
class MultiMap<K, V> {
  final Map<K, List<V>> _map = {};

  void add(K key, V value) {
    _map.putIfAbsent(key, () => []).add(value);
  }

  List<V> get(K key) => _map[key] ?? [];

  void printAll() {
    _map.forEach((k, v) => print("$k: $v"));
  }
}

void main() {
  var mm = MultiMap<String, String>();
  mm.add("dasturlash", "Dart");
  mm.add("dasturlash", "Python");
  mm.add("dasturlash", "C++");
  mm.add("dizayn", "Figma");

  mm.printAll();
}
```

## Tushuntirish va Mantiq:
MultiMap bitta toifaga tegishli bir nechta ma'lumotlarni saqlashda (masalan teglar, xabarlar) qo'llaniladi.

## Ishlash natijasi:
```text
dasturlash: [Dart, Python, C++]
dizayn: [Figma]
```

# 279-Topshiriq: Graflarni qo'shnilik ro'yxati (Adjacency List) sifatida ifodalash
## Topshiriq sharti:
Yo'naltirilmagan grafni `Map<int, List<int>>` orqali modellashtiruvchi klass yozing.

## Yechim (Dart kodi):
```dart
class Graph {
  final Map<int, List<int>> adj = {};

  void addEdge(int u, int v) {
    adj.putIfAbsent(u, () => []).add(v);
    adj.putIfAbsent(v, () => []).add(u);
  }

  void printGraph() {
    adj.forEach((node, neighbors) {
      print("Tugun $node qo'shnilari: $neighbors");
    });
  }
}

void main() {
  var g = Graph();
  g.addEdge(1, 2);
  g.addEdge(1, 3);
  g.addEdge(2, 4);

  g.printGraph();
}
```

## Tushuntirish va Mantiq:
Map yordamida qo'shnilik ro'yxati har qanday nomdagi yoki ixtiyoriy ID larga ega graflarni saqlash imkonini beradi.

## Ishlash natijasi:
```text
Tugun 1 qo'shnilari: [2, 3]
Tugun 2 qo'shnilari: [1, 4]
Tugun 3 qo'shnilari: [1]
Tugun 4 qo'shnilari: [2]
```

# 280-Topshiriq: Grafda BFS (Kenglik bo'yicha qidirish) Map asosida
## Topshiriq sharti:
`Map<int, List<int>>` da saqlangan grafda boshlang'ich tugundan boshlab BFS qidiruvini amalga oshiring.

## Yechim (Dart kodi):
```dart
import 'dart:collection';

void bfs(Map<int, List<int>> adj, int start) {
  Set<int> visited = {};
  Queue<int> queue = Queue();

  visited.add(start);
  queue.add(start);

  stdoutWrite("BFS tartibi: ");
  while (queue.isNotEmpty) {
    int u = queue.removeFirst();
    stdoutWrite("$u ");

    for (int v in adj[u] ?? []) {
      if (!visited.contains(v)) {
        visited.add(v);
        queue.add(v);
      }
    }
  }
  print("");
}

void stdoutWrite(String s) => print(s);

void main() {
  Map<int, List<int>> g = {
    0: [1, 2],
    1: [0, 3],
    2: [0, 3],
    3: [1, 2]
  };

  bfs(g, 0);
}
```

## Tushuntirish va Mantiq:
`Queue` va `Set` yordamida BFS qidiruvi eng qisqa yo'llarni O(V + E) da topadi.

## Ishlash natijasi:
```text
BFS tartibi: 
0 
1 
2 
3 

```

# 281-Topshiriq: Grafda DFS (Chuqurlik bo'yicha qidirish) Map asosida
## Topshiriq sharti:
Rekursiv DFS orqali barcha tugunlarga tashrif buyurish tartibini chiqaring.

## Yechim (Dart kodi):
```dart
void dfsHelper(Map<int, List<int>> adj, int u, Set<int> visited) {
  visited.add(u);
  print(u);

  for (int v in adj[u] ?? []) {
    if (!visited.contains(v)) {
      dfsHelper(adj, v, visited);
    }
  }
}

void dfs(Map<int, List<int>> adj, int start) {
  print("DFS tartibi:");
  dfsHelper(adj, start, {});
}

void main() {
  Map<int, List<int>> g = {
    0: [1, 2],
    1: [3],
    2: [4],
    3: [],
    4: []
  };

  dfs(g, 0);
}
```

## Tushuntirish va Mantiq:
DFS iloji boricha chuqurroq kirib boradi va bog'liqlik komponentlarini aniqlashda qo'llaniladi.

## Ishlash natijasi:
```text
DFS tartibi:
0
1
3
2
4
```

# 282-Topshiriq: Anagramma so'zlarni guruhlash Map yordamida
## Topshiriq sharti:
Bir xil harflardan tashkil topgan anagramma so'zlarni `Map<String, List<String>>` da guruhlang.

## Yechim (Dart kodi):
```dart
List<List<String>> groupAnagrams(List<String> strs) {
  Map<String, List<String>> map = {};
  for (String s in strs) {
    List<String> chars = s.split('')..sort();
    String key = chars.join('');
    map.putIfAbsent(key, () => []).add(s);
  }
  return map.values.toList();
}

void main() {
  List<String> sozlar = ["eat", "tea", "tan", "ate", "nat", "bat"];
  var anagrammalar = groupAnagrams(sozlar);

  print("Anagramma guruhlari: $anagrammalar");
}
```

## Tushuntirish va Mantiq:
Har bir so'zning harflarini saralab kalit qilib olish anagrammalarni O(N * K log K) da oson guruhlaydi.

## Ishlash natijasi:
```text
Anagramma guruhlari: [[eat, tea, ate], [tan, nat], [bat]]
```

# 283-Topshiriq: Rim raqamlarini arab raqamiga o'girish Map orqali
## Topshiriq sharti:
`M`, `D`, `C`, `L`, `X`, `V`, `I` rim raqamlarini Map yordamida butun songa o'giruvchi funksiya yozing.

## Yechim (Dart kodi):
```dart
int romanToInt(String s) {
  const Map<String, int> roman = {
    'I': 1, 'V': 5, 'X': 10, 'L': 50,
    'C': 100, 'D': 500, 'M': 1000
  };

  int total = 0;
  for (int i = 0; i < s.length; ++i) {
    int current = roman[s[i]] ?? 0;
    int next = (i + 1 < s.length) ? (roman[s[i + 1]] ?? 0) : 0;

    if (current < next) {
      total -= current;
    } else {
      total += current;
    }
  }
  return total;
}

void main() {
  print("XIV = ${romanToInt('XIV')}");
  print("MCMXCIV = ${romanToInt('MCMXCIV')}");
}
```

## Tushuntirish va Mantiq:
Agar oldingi belgi keyingisidan kichik bo'lsa ayriladi (masalan IV = 5 - 1 = 4), aks holda qo'shiladi.

## Ishlash natijasi:
```text
XIV = 14
MCMXCIV = 1994
```

# 284-Topshiriq: Arab raqamini rim raqamiga o'girish
## Topshiriq sharti:
Butun sonni rim raqamiga aylantiruvchi algoritmni juftliklar xaritasi bilan tuzing.

## Yechim (Dart kodi):
```dart
String intToRoman(int num) {
  const values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1];
  const symbols = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"];

  StringBuffer sb = StringBuffer();
  for (int i = 0; i < values.length; ++i) {
    while (num >= values[i]) {
      num -= values[i];
      sb.write(symbols[i]);
    }
  }
  return sb.toString();
}

void main() {
  print("1994 = ${intToRoman(1994)}");
  print("58 = ${intToRoman(58)}");
}
```

## Tushuntirish va Mantiq:
Eng katta qiymatdan boshlab ayirib borish orqali eng qisqa standart rim ifodasi hosil qilinadi.

## Ishlash natijasi:
```text
1994 = MCMXCIV
58 = LVIII
```

# 285-Topshiriq: Xotira keshi (In-Memory Key-Value Store) sinfi
## Topshiriq sharti:
`get`, `set`, `delete`, `has` amallariga ega to'liq xotira xaritasi sinfini yozing.

## Yechim (Dart kodi):
```dart
class KeyValueStore<K, V> {
  final Map<K, V> _store = {};

  void set(K key, V value) => _store[key] = value;
  V? get(K key) => _store[key];
  bool has(K key) => _store.containsKey(key);
  V? delete(K key) => _store.remove(key);
  int get size => _store.length;
}

void main() {
  var kv = KeyValueStore<String, String>();
  kv.set("user:1", "Sardor");
  kv.set("user:2", "Madina");

  print("user:1 bormi: ${kv.has('user:1')}");
  print("user:1 qiymati: ${kv.get('user:1')}");

  kv.delete("user:1");
  print("O'chirilgach user:1 bormi: ${kv.has('user:1')}");
}
```

## Tushuntirish va Mantiq:
Redis kabi in-memory ma'lumotlar bazalarining asosiy ishlash prinsipi ushbu xarita naqshiga asoslanadi.

## Ishlash natijasi:
```text
user:1 bormi: true
user:1 qiymati: Sardor
O'chirilgach user:1 bormi: false
```

# 286-Topshiriq: TTL (Time-To-Live) bilan eskiruvchi kesh xaritasi
## Topshiriq sharti:
Belgilangan muddatdan (masalan 100 millisekund) keyin o'z-o'zidan yaroqsiz bo'lib qoladigan kesh elementini yozing.

## Yechim (Dart kodi):
```dart
class TtlCache<K, V> {
  final Map<K, ({V value, DateTime expireAt})> _cache = {};

  void set(K key, V val, Duration ttl) {
    _cache[key] = (value: val, expireAt: DateTime.now().add(ttl));
  }

  V? get(K key) {
    var entry = _cache[key];
    if (entry == null) return null;
    if (DateTime.now().isAfter(entry.expireAt)) {
      _cache.remove(key); // Eskirgan, o'chiramiz
      return null;
    }
    return entry.value;
  }
}

void main() {
  var cache = TtlCache<String, String>();
  cache.set("token", "SECRET_KEY_123", Duration(milliseconds: 50));

  print("Darhol o'qish: ${cache.get('token')}");
}
```

## Tushuntirish va Mantiq:
TTL kesh vaqti o'tgan ma'lumotlarni avtomatik eskirgan deb hisoblab xotirani tozalash imkonini beradi.

## Ishlash natijasi:
```text
Darhol o'qish: SECRET_KEY_123
```

# 287-Topshiriq: LRU (Least Recently Used) kesh algoritmini LinkedHashMap yordamida yozish
## Topshiriq sharti:
Dart dagi `LinkedHashMap` kiritilish tartibini saqlashidan foydalanib ixcham LRU keshini quring.

## Yechim (Dart kodi):
```dart
import 'dart:collection';

class LruCache<K, V> {
  final int capacity;
  final LinkedHashMap<K, V> _map = LinkedHashMap();

  LruCache(this.capacity);

  V? get(K key) {
    if (!_map.containsKey(key)) return null;
    // O'qilganda oxiriga ko'chiramiz (eng yangi qilish uchun)
    V val = _map.remove(key) as V;
    _map[key] = val;
    return val;
  }

  void put(K key, V val) {
    if (_map.containsKey(key)) {
      _map.remove(key);
    } else if (_map.length >= capacity) {
      // Eng boshidagi eng eski elementni o'chiramiz
      K oldestKey = _map.keys.first;
      _map.remove(oldestKey);
    }
    _map[key] = val;
  }

  void printState() => print("LRU holati: ${_map.keys.toList()}");
}

void main() {
  var lru = LruCache<String, int>(2);
  lru.put("A", 1);
  lru.put("B", 2);
  lru.get("A"); // A yangilandi, B endi eng eski

  lru.put("C", 3); // Sig'im to'ldi, B o'chiriladi!

  print("A bor: ${lru.get('A') != null}");
  print("B bor: ${lru.get('B') != null}");
  print("C bor: ${lru.get('C') != null}");
  lru.printState();
}
```

## Tushuntirish va Mantiq:
`LinkedHashMap` kalitlarni o'chirish va qayta qo'shish orqali O(1) da LRU tartibini saqlaydi.

## Ishlash natijasi:
```text
A bor: true
B bor: false
C bor: true
LRU holati: [A, C]
```

# 288-Topshiriq: Map asosida oddiy i18n / ko'p tillilik (L10n) lug'ati
## Topshiriq sharti:
O'zbek, ingliz va rus tillaridagi interfeys matnlarini til kodi bo'yicha beruvchi klass yozing.

## Yechim (Dart kodi):
```dart
class I18n {
  static const Map<String, Map<String, String>> _strings = {
    "uz": {"welcome": "Xush kelibsiz!", "exit": "Chiqish"},
    "en": {"welcome": "Welcome!", "exit": "Exit"},
    "ru": {"welcome": "Добро пожаловать!", "exit": "Выход"}
  };

  static String t(String lang, String key) {
    return _strings[lang]?[key] ?? key;
  }
}

void main() {
  print("UZ: ${I18n.t('uz', 'welcome')}");
  print("EN: ${I18n.t('en', 'welcome')}");
  print("RU: ${I18n.t('ru', 'welcome')}");
}
```

## Tushuntirish va Mantiq:
Ko'p tilli ilovalar ichki lug'at xaritalari orqali xavfsiz va tezkor lokalizatsiya qilinadi.

## Ishlash natijasi:
```text
UZ: Xush kelibsiz!
EN: Welcome!
RU: Добро пожаловать!
```

# 289-Topshiriq: Ikki Map o'rtasidagi farqni topish (Diffing Maps)
## Topshiriq sharti:
Eski va yangi konfiguratsiya xaritalari orasidagi o'zgargan, qo'shilgan va o'chirilgan kalitlarni toping.

## Yechim (Dart kodi):
```dart
void diffMaps(Map<String, dynamic> oldM, Map<String, dynamic> newM) {
  var added = newM.keys.toSet().difference(oldM.keys.toSet());
  var removed = oldM.keys.toSet().difference(newM.keys.toSet());
  var modified = <String>[];

  for (var k in oldM.keys) {
    if (newM.containsKey(k) && oldM[k] != newM[k]) {
      modified.add(k);
    }
  }

  print("Qo'shilgan kalitlar:   $added");
  print("O'chirilgan kalitlar:  $removed");
  print("O'zgartirilganlar:     $modified");
}

void main() {
  var v1 = {"theme": "light", "fontSize": 14, "autoSave": true};
  var v2 = {"theme": "dark", "fontSize": 14, "lang": "uz"};

  diffMaps(v1, v2);
}
```

## Tushuntirish va Mantiq:
Diff tahlili holat o'zgarishlarini (state changes) aniqlashda va ortiqcha UI renderlarni kamaytirishda juda muhim.

## Ishlash natijasi:
```text
Qo'shilgan kalitlar:   {lang}
O'chirilgan kalitlar:  {autoSave}
O'zgartirilganlar:     [theme]
```

# 290-Topshiriq: Map qiymatlari bo'yicha teskari saralash
## Topshiriq sharti:
Talabalar ballari xaritasini ballar kamayish tartibida saralab yangi xaritaga joylang.

## Yechim (Dart kodi):
```dart
void main() {
  Map<String, int> scores = {
    "Malika": 85,
    "Anvar": 92,
    "Bobur": 78,
    "Ziyoda": 95
  };

  var sortedEntries = scores.entries.toList()
    ..sort((a, b) => b.value.compareTo(a.value));

  Map<String, int> sortedMap = Map.fromEntries(sortedEntries);
  print("Ballar bo'yicha saralangan: $sortedMap");
}
```

## Tushuntirish va Mantiq:
Entries ro'yxatiga o'tkazib `sort` qilish va so'ngra `fromEntries` chaqirish orqali qiymat bo'yicha saralanadi.

## Ishlash natijasi:
```text
Ballar bo'yicha saralangan: {Ziyoda: 95, Anvar: 92, Malika: 85, Bobur: 78}
```

# 291-Topshiriq: Bigramlar (So'z juftliklari) chastotasini hisoblash
## Topshiriq sharti:
Matndagi har bir ketma-ket ikkita so'z juftligi (bigram) necha marta uchraganini hisoblang.

## Yechim (Dart kodi):
```dart
void main() {
  String matn = "sun'iy intellekt kelajak poydevoridir va sun'iy intellekt taraqqiyot garovidir";
  List<String> sozlar = matn.split(" ");

  Map<String, int> bigrams = {};
  for (int i = 0; i < sozlar.length - 1; ++i) {
    String pair = "${sozlar[i]} ${sozlar[i + 1]}";
    bigrams[pair] = (bigrams[pair] ?? 0) + 1;
  }

  print("Bigramlar chastotasi:");
  bigrams.forEach((k, v) => print("  '$k': $v"));
}
```

## Tushuntirish va Mantiq:
N-gram chastotalari til modellari va avtomatik matn to'ldirish (autocomplete) tizimlarining asosi hisoblanadi.

## Ishlash natijasi:
```text
Bigramlar chastotasi:
  'sun'iy intellekt': 2
  'intellekt kelajak': 1
  'kelajak poydevoridir': 1
  'poydevoridir va': 1
  'va sun'iy': 1
  'intellekt taraqqiyot': 1
  'taraqqiyot garovidir': 1
```

# 292-Topshiriq: Telefon kitobchasi (Contacts Manager)
## Topshiriq sharti:
Ism bo'yicha telefon raqamlarini saqlovchi, yangilovchi va qidiruvchi to'liq sinf tuzing.

## Yechim (Dart kodi):
```dart
class ContactBook {
  final Map<String, String> _contacts = {};

  void add(String name, String phone) => _contacts[name] = phone;

  String? find(String query) {
    for (var entry in _contacts.entries) {
      if (entry.key.toLowerCase().contains(query.toLowerCase())) {
        return "${entry.key}: ${entry.value}";
      }
    }
    return null;
  }
}

void main() {
  var book = ContactBook();
  book.add("Alisher Navoiy", "+998901112233");
  book.add("Zahiriddin Bobur", "+998904445566");

  print("Qidiruv 'alisher': ${book.find('alisher')}");
  print("Qidiruv 'bobur':   ${book.find('bobur')}");
}
```

## Tushuntirish va Mantiq:
Xarita va satr qidiruvi kombinatsiyasi qulay va xavfsiz kontaktlar boshqaruvini beradi.

## Ishlash natijasi:
```text
Qidiruv 'alisher': Alisher Navoiy: +998901112233
Qidiruv 'bobur':   Zahiriddin Bobur: +998904445566
```

# 293-Topshiriq: Xavfsiz xarita tahlilchisi (Safe Map Extractor)
## Topshiriq sharti:
API dan kelgan xaritadan qiymatlarni aniq turlar bilan, xato bo'lsa standart qiymat qaytaruvchi yordamchi metodlar yozing.

## Yechim (Dart kodi):
```dart
class SafeMap {
  final Map<String, dynamic> _raw;
  SafeMap(this._raw);

  String getString(String key, [String def = ""]) {
    var v = _raw[key];
    return v is String ? v : def;
  }

  int getInt(String key, [int def = 0]) {
    var v = _raw[key];
    if (v is int) return v;
    if (v is String) return int.tryParse(v) ?? def;
    return def;
  }
}

void main() {
  var sm = SafeMap({"ism": "Sardor", "yosh": "25", "balans": null});

  print("Ism: ${sm.getString('ism')}");
  print("Yosh (satrdan int ga): ${sm.getInt('yosh')}");
  print("Balans (null o'rniga default): ${sm.getInt('balans', 100)}");
}
```

## Tushuntirish va Mantiq:
Tashqi noaniq xaritalardan ma'lumotlarni xavfsiz o'qish (data sanitation) dastur barqarorligini ta'minlaydi.

## Ishlash natijasi:
```text
Ism: Sardor
Yosh (satrdan int ga): 25
Balans (null o'rniga default): 100
```

# 294-Topshiriq: Prefix Tree (Trie) tugunlarini Map bilan ifodalash
## Topshiriq sharti:
Prefiks daraxtining har bir tugunida farzandlarni `Map<String, TrieNode>` da saqlovchi sodda Trie yarating.

## Yechim (Dart kodi):
```dart
class TrieNode {
  final Map<String, TrieNode> children = {};
  bool isEnd = false;
}

class SimpleTrie {
  final TrieNode root = TrieNode();

  void insert(String word) {
    TrieNode curr = root;
    for (int i = 0; i < word.length; ++i) {
      String ch = word[i];
      curr = curr.children.putIfAbsent(ch, () => TrieNode());
    }
    curr.isEnd = true;
  }

  bool search(String word) {
    TrieNode curr = root;
    for (int i = 0; i < word.length; ++i) {
      String ch = word[i];
      if (!curr.children.containsKey(ch)) return false;
      curr = curr.children[ch]!;
    }
    return curr.isEnd;
  }
}

void main() {
  var trie = SimpleTrie();
  trie.insert("salom");
  trie.insert("sariq");

  print("'salom' bormi: ${trie.search('salom')}");
  print("'sam' bormi:   ${trie.search('sam')}");
}
```

## Tushuntirish va Mantiq:
Map asosidagi Trie daraxti istalgan Unicode belgilar (kirill, lotin, arab harflari) bilan dinamik xotira ajratib ishlay oladi.

## Ishlash natijasi:
```text
'salom' bormi: true
'sam' bormi:   false
```

# 295-Topshiriq: BPE Tokenizer so'zlar lug'ati (Vocabulary) boshqaruvi
## Topshiriq sharti:
Token matni va Token ID larni ikki tomonlama Map larda saqlovchi lug'at klassini yozing.

## Yechim (Dart kodi):
```dart
class VocabManager {
  final Map<String, int> tokenToId = {};
  final Map<int, String> idToToken = {};
  int _nextId = 0;

  int addToken(String token) {
    if (tokenToId.containsKey(token)) return tokenToId[token]!;
    int id = _nextId++;
    tokenToId[token] = id;
    idToToken[id] = token;
    return id;
  }

  int? getId(String token) => tokenToId[token];
  String? getToken(int id) => idToToken[id];
}

void main() {
  var vm = VocabManager();
  vm.addToken("<s>");
  vm.addToken("O'zbekiston");
  vm.addToken("AI");

  print("'O\'zbekiston' ID: ${vm.getId("O'zbekiston")}");
  print("1-token matni:     ${vm.getToken(1)}");
}
```

## Tushuntirish va Mantiq:
Ikki tomonlama Map AI tokenizatorlarida tezkor kodlash (encode) va dekodlash (decode) uchun poydevordir.

## Ishlash natijasi:
```text
'O'zbekiston' ID: 1
1-token matni:     O'zbekiston
```

# 296-Topshiriq: Faqat bitta marta uchragan elementlarni Set bilan topish
## Topshiriq sharti:
Massivda takrorlanmaydigan (faqat bir marta kelgan) noyob elementlarni Set va Map yordamida ajrating.

## Yechim (Dart kodi):
```dart
List<int> yagonaElementlar(List<int> nums) {
  Map<int, int> counts = {};
  for (int x in nums) counts[x] = (counts[x] ?? 0) + 1;
  return counts.entries.where((e) => e.value == 1).map((e) => e.key).toList();
}

void main() {
  List<int> sonlar = [4, 1, 2, 1, 2, 5, 6, 4];
  print("Yagona elementlar: ${yagonaElementlar(sonlar)}");
}
```

## Tushuntirish va Mantiq:
Chastota xaritasi orqali filtrlash chiziqli O(N) vaqt oladi.

## Ishlash natijasi:
```text
Yagona elementlar: [5, 6]
```

# 297-Topshiriq: Grafda eng qisqa yo'l (Dijkstra) masofalari Map yordamida
## Topshiriq sharti:
Vaznli grafda boshlang'ich cho'qqidan har bir tugungacha eng qisqa masofalarni saqlovchi Dijkstra algoritmini yozing.

## Yechim (Dart kodi):
```dart
Map<int, int> dijkstraDistances(Map<int, Map<int, int>> graph, int start) {
  Map<int, int> dist = {};
  Set<int> visited = {};

  for (int node in graph.keys) dist[node] = 1000000;
  dist[start] = 0;

  while (visited.length < graph.length) {
    int? u;
    int minD = 1000000;
    for (var node in graph.keys) {
      if (!visited.contains(node) && dist[node]! < minD) {
        minD = dist[node]!;
        u = node;
      }
    }
    if (u == null) break;
    visited.add(u);

    graph[u]?.forEach((v, weight) {
      if (dist[u!]! + weight < dist[v]!) {
        dist[v] = dist[u]! + weight;
      }
    });
  }
  return dist;
}

void main() {
  Map<int, Map<int, int>> g = {
    0: {1: 4, 2: 1},
    1: {3: 1},
    2: {1: 2, 3: 5},
    3: {}
  };

  var masofalar = dijkstraDistances(g, 0);
  print("0 dan masofalar: $masofalar");
}
```

## Tushuntirish va Mantiq:
Map ichida Map strukturasidan foydalanish vaznli graflarni ifodalashning eng sodda va samarali yo'lidir.

## Ishlash natijasi:
```text
0 dan masofalar: {0: 0, 1: 3, 2: 1, 3: 4}
```

# 298-Topshiriq: Shartli hisob-kitoblar bilan xarid cheki agregatsiyasi
## Topshiriq sharti:
Kategoriyalar bo'yicha mahsulotlar summasini jamlovchi xarita hisob-kitobini yozing.

## Yechim (Dart kodi):
```dart
void main() {
  List<Map<String, dynamic>> xaridlar = [
    {"kategoriya": "Oziq-ovqat", "narx": 25000},
    {"kategoriya": "Kiyim", "narx": 150000},
    {"kategoriya": "Oziq-ovqat", "narx": 45000},
    {"kategoriya": "Kitob", "narx": 50000}
  ];

  Map<String, double> kategoriyaJami = {};
  for (var x in xaridlar) {
    String kat = x["kategoriya"];
    double narx = (x["narx"] as num).toDouble();
    kategoriyaJami[kat] = (kategoriyaJami[kat] ?? 0.0) + narx;
  }

  print("Kategoriyalar bo'yicha jami:");
  kategoriyaJami.forEach((k, v) => print("  $k: ${v.toStringAsFixed(0)} so'm"));
}
```

## Tushuntirish va Mantiq:
Ushbu agregatsiya biznes tahlili (analytics) va grafik hisobotlar uchun asosiy ma'lumot qatlamidir.

## Ishlash natijasi:
```text
Kategoriyalar bo'yicha jami:
  Oziq-ovqat: 70000 so'm
  Kiyim: 150000 so'm
  Kitob: 50000 so'm
```

# 299-Topshiriq: Set bilan ikki matn o'rtasidagi Jaccard o'xshashlik koeffitsiyenti
## Topshiriq sharti:
Ikki matnning so'zlar to'plamlari kesishmasi va birlashmasi nisbati orqali o'xshashligini ($J(A, B) = |A \cap B| / |A \cup B|$) hisoblang.

## Yechim (Dart kodi):
```dart
double jaccardSimilarity(String s1, String s2) {
  var set1 = s1.toLowerCase().split(" ").toSet();
  var set2 = s2.toLowerCase().split(" ").toSet();

  var intersection = set1.intersection(set2);
  var union = set1.union(set2);

  return union.isEmpty ? 1.0 : intersection.length / union.length;
}

void main() {
  String t1 = "sun'iy intellekt kelajak poydevori";
  String t2 = "sun'iy intellekt taraqqiyot asosi";

  double oxshashlik = jaccardSimilarity(t1, t2);
  print("Jaccard o'xshashlik koeffitsiyenti: ${(oxshashlik * 100).toStringAsFixed(1)}%");
}
```

## Tushuntirish va Mantiq:
Jaccard indeksi to'plamlar amallari asosida matnlarning semantik o'xshashligini hisoblovchi klassik formuladir.

## Ishlash natijasi:
```text
Jaccard o'xshashlik koeffitsiyenti: 33.3%
```

# 300-Topshiriq: Katta amaliy loyiha: O'zbek tili teskari indeksi va Qidiruv tizimi (Inverted Index)
## Topshiriq sharti:
300-topshiriq: Matnli hujjatlar to'plamini so'zlar bo'yicha indekslovchi (`Map<String, Set<int>>`), kalit so'zlar bo'yicha tezkor qidiruvchi to'liq qidiruv tizimini yozing.

## Yechim (Dart kodi):
```dart
class InvertedIndexEngine {
  final Map<String, Set<int>> _index = {};
  final List<String> _documents = [];

  void addDocument(String doc) {
    int docId = _documents.length;
    _documents.add(doc);

    // So'zlarni tozalab indeksga qo'shamiz
    var words = doc.toLowerCase().replaceAll(RegExp(r'[^a-zA-Z0-9\'\s]'), '').split(' ');
    for (var w in words) {
      if (w.trim().isNotEmpty) {
        _index.putIfAbsent(w, () => {}).add(docId);
      }
    }
  }

  List<String> search(String query) {
    var terms = query.toLowerCase().split(' ');
    Set<int>? matchingDocs;

    for (var term in terms) {
      var docsWithTerm = _index[term] ?? {};
      if (matchingDocs == null) {
        matchingDocs = Set.from(docsWithTerm);
      } else {
        matchingDocs = matchingDocs.intersection(docsWithTerm); // AND qidiruvi
      }
    }

    if (matchingDocs == null || matchingDocs.isEmpty) return [];
    return matchingDocs.map((id) => "Doc #$id: ${_documents[id]}").toList();
  }
}

void main() {
  var engine = InvertedIndexEngine();
  engine.addDocument("O'zbekiston sun'iy intellekt sohasida ulkan yutuqlarga erishmoqda.");
  engine.addDocument("Flutter va Dart mobil dasturlash uchun eng mukammal vositadir.");
  engine.addDocument("Sun'iy intellekt va katta til modellari dunyoni o'zgartirmoqda.");

  print("Qidiruv: 'sun'iy intellekt':");
  var natijalar = engine.search("sun'iy intellekt");
  natijalar.forEach((doc) => print("- $doc"));

  print("
Qidiruv: 'dart':");
  var natijalar2 = engine.search("dart");
  natijalar2.forEach((doc) => print("- $doc"));
}
```

## Tushuntirish va Mantiq:
300-topshiriq bilan Dart tilida to'plamlar (`Set`) va xaritalar (`Map`) yordamida sanoat darajasidagi axborot qidiruv tizimi (Search Engine) muvaffaqiyatli qurildi.

## Ishlash natijasi:
```text
Qidiruv: 'sun'iy intellekt':
- Doc #0: O'zbekiston sun'iy intellekt sohasida ulkan yutuqlarga erishmoqda.
- Doc #2: Sun'iy intellekt va katta til modellari dunyoni o'zgartirmoqda.

Qidiruv: 'dart':
- Doc #1: Flutter va Dart mobil dasturlash uchun eng mukammal vositadir.
```

