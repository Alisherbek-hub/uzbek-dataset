# 551-Topshiriq: Generik klass asoslari (Quti<T>)

## Topshiriq sharti:
Ixtiyoriy tipdagi ma'lumotni o'zida xavfsiz saqlovchi generik `Quti<T>` klassini tuzing.

## Yechim (Dart kodi):
```dart
class Quti<T> {
  final T qiymat;

  Quti(this.qiymat);

  T olish() => qiymat;

  @override
  String toString() => 'Quti($qiymat) [T=${T}]';
}

void main() {
  var sonQuti = Quti<int>(42);
  var matnQuti = Quti<String>('Dart Generics');

  print(sonQuti);
  print(matnQuti);
}
```

## Tushuntirish va Mantiq:
`Quti<T>` har qanday turdagi qiymatni xavfsiz o'rab oladi, qaysi tur uzatilsa, o'sha turning xususiyatlarini saqlaydi.

## Ishlash natijasi:
```text
Quti(42) [T=int]
Quti(Dart Generics) [T=String]
```

# 552-Topshiriq: Generik funksiya asoslari

## Topshiriq sharti:
Ikkita bir xil turdagi parametrni Record ko'rinishida o'rinlarini almashtirib qaytaruvchi generik funksiya tuzing.

## Yechim (Dart kodi):
```dart
(T, T) almashtir<T>(T a, T b) {
  return (b, a);
}

void main() {
  var (x, y) = almashtir<int>(10, 20);
  print('Sonlar almashdi: x=$x, y=$y');

  var (s1, s2) = almashtir<String>('Salom', 'Dunyo');
  print('Matnlar almashdi: s1=$s1, s2=$s2');
}
```

## Tushuntirish va Mantiq:
Generik funksiyalar `funksiya<T>(...)` orqali turli tiplar uchun bitta umumiy mantiqni qayta yozish imkonini beradi.

## Ishlash natijasi:
```text
Sonlar almashdi: x=20, y=10
Matnlar almashdi: s1=Dunyo, s2=Salom
```

# 553-Topshiriq: Chegaralangan generiklar (Bounded Type: <T extends num>)

## Topshiriq sharti:
Faqat raqamli tiplar (`int`, `double`) bilan ishlovchi va ularni qo'shuvchi generik kalkulyator tuzing.

## Yechim (Dart kodi):
```dart
class RaqamliKalkulyator<T extends num> {
  T qosh(T a, T b) {
    return (a + b) as T;
  }
}

void main() {
  var intKalk = RaqamliKalkulyator<int>();
  print('5 + 7 = ${intKalk.qosh(5, 7)}');

  var doubleKalk = RaqamliKalkulyator<double>();
  print('3.14 + 2.86 = ${doubleKalk.qosh(3.14, 2.86)}');

  // RaqamliKalkulyator<String>(); // XATO: String num dan meros olmagan!
}
```

## Tushuntirish va Mantiq:
`<T extends num>` cheklovi generik parametr faqat `num` yoki uning vorislari (`int`, `double`) bo'lishini kafolatlaydi.

## Ishlash natijasi:
```text
5 + 7 = 12
3.14 + 2.86 = 6.0
```

# 554-Topshiriq: Dart Reified Generics (Ish vaqtida tiplarni saqlash)

## Topshiriq sharti:
Dartda Java kabi 'type erasure' yo'qligini, runtime da generik tiplar to'liq mavjudligini ko'rsating.

## Yechim (Dart kodi):
```dart
void tipTekshir(Object royxat) {
  if (royxat is List<int>) {
    print('Bu butun sonlar (int) ro\'yxati');
  } else if (royxat is List<String>) {
    print('Bu matnlar (String) ro\'yxati');
  } else {
    print('Boshqa turdagi ro\'yxat');
  }
}

void main() {
  var a = <int>[1, 2, 3];
  var b = <String>['a', 'b'];

  tipTekshir(a);
  tipTekshir(b);
}
```

## Tushuntirish va Mantiq:
Dartda generik tiplar 'reified' bo'lib, kompilyatsiyadan keyin o'chib ketmaydi, runtime vaqtida aniq tekshiriladi.

## Ishlash natijasi:
```text
Bu butun sonlar (int) ro'yxati
Bu matnlar (String) ro'yxati
```

# 555-Topshiriq: Generik typedef va Predikat funksiyalari

## Topshiriq sharti:
Ixtiyoriy tipdagi elementni shartga tekshiruvchi generic `Predikat<T>` nomli funksiya tipini belgilang.

## Yechim (Dart kodi):
```dart
typedef Predikat<T> = bool Function(T element);

List<T> maxsusFiltr<T>(List<T> royxat, Predikat<T> shart) {
  List<T> natija = [];
  for (var e in royxat) {
    if (shart(e)) {
      natija.add(e);
    }
  }
  return natija;
}

void main() {
  var sonlar = [1, 2, 3, 4, 5, 6];
  var juftlar = maxsusFiltr<int>(sonlar, (n) => n % 2 == 0);
  print('Juft sonlar: $juftlar');

  var sozlar = ['olma', 'anor', 'shaftoli', 'nok'];
  var uzunSozlar = maxsusFiltr<String>(sozlar, (s) => s.length > 4);
  print('Uzun so\'zlar: $uzunSozlar');
}
```

## Tushuntirish va Mantiq:
Generik typedef yordamida parametrli yuqori tartibli funksiyalar (Higher-order functions) toza va tushunarli yoziladi.

## Ishlash natijasi:
```text
Juft sonlar: [2, 4, 6]
Uzun so'zlar: [shaftoli]
```

# 556-Topshiriq: Generik Stack (LIFO) ma'lumotlar tuzilmasi

## Topshiriq sharti:
Har qanday turdagi ma'lumotlarni qabul qiluvchi `Stack<T>` sinfini tuzing.

## Yechim (Dart kodi):
```dart
class Stack<T> {
  final List<T> _elementlar = [];

  void push(T element) => _elementlar.add(element);

  T pop() {
    if (isEmpty) throw StateError('Stack bo\'sh');
    return _elementlar.removeLast();
  }

  T peek() {
    if (isEmpty) throw StateError('Stack bo\'sh');
    return _elementlar.last;
  }

  bool get isEmpty => _elementlar.isEmpty;
  int get length => _elementlar.length;
}

void main() {
  var s = Stack<double>();
  s.push(1.5);
  s.push(2.5);
  s.push(3.5);

  print('Cho\'qqi: ${s.peek()}');
  print('Olingan: ${s.pop()}');
  print('Qolgan uzunlik: ${s.length}');
}
```

## Tushuntirish va Mantiq:
Generik Stack faqat belgilangan turdagi ma'lumotlarni qabul qilib, xato tur tushib qolishini oldini oladi.

## Ishlash natijasi:
```text
Cho'qqi: 3.5
Olingan: 3.5
Qolgan uzunlik: 2
```

# 557-Topshiriq: Generik Navbat (Queue - FIFO) tuzilmasi

## Topshiriq sharti:
Navbatga qo'shish va birinchi bo'lib olishni ta'minlovchi `Navbat<T>` klassini yozing.

## Yechim (Dart kodi):
```dart
class Navbat<T> {
  final List<T> _qator = [];

  void enqueue(T item) => _qator.add(item);

  T dequeue() {
    if (isEmpty) throw StateError('Navbat bo\'sh');
    return _qator.removeAt(0);
  }

  bool get isEmpty => _qator.isEmpty;
}

void main() {
  var n = Navbat<String>();
  n.enqueue('Birinchi vazifa');
  n.enqueue('Ikkinchi vazifa');

  print('Bajarilmoqda: ${n.dequeue()}');
  print('Bajarilmoqda: ${n.dequeue()}');
}
```

## Tushuntirish va Mantiq:
FIFO navbati asinxron vazifalar va xabarlar oqimida generik tiplar bilan xavfsiz boshqariladi.

## Ishlash natijasi:
```text
Bajarilmoqda: Birinchi vazifa
Bajarilmoqda: Ikkinchi vazifa
```

# 558-Topshiriq: Generik Juftlik (Pair<A, B>) klassi

## Topshiriq sharti:
Ikkita turli turdagi qiymatlarni bitta bog'lamda saqlovchi `Juftlik<A, B>` klassini tuzing.

## Yechim (Dart kodi):
```dart
class Juftlik<A, B> {
  final A birinchi;
  final B ikkinchi;

  const Juftlik(this.birinchi, this.ikkinchi);

  @override
  String toString() => '($birinchi, $ikkinchi)';
}

void main() {
  var talaba = Juftlik<String, int>('Dilshod', 95);
  print('Talaba va bali: $talaba');
  print('Ism: ${talaba.birinchi}, Ball: ${talaba.ikkinchi}');
}
```

## Tushuntirish va Mantiq:
Ko'p parametrli generiklar (`<A, B>`) orqali bir-biriga bog'liq har xil turdagi ma'lumotlar juftligi hosil qilinadi.

## Ishlash natijasi:
```text
Talaba va bali: (Dilshod, 95)
Ism: Dilshod, Ball: 95
```

# 559-Topshiriq: Generik qidiruv funksiyasi

## Topshiriq sharti:
Ro'yxatdan berilgan shartga mos birinchi elementni yoki null qaytaruvchi generik funksiya yozing.

## Yechim (Dart kodi):
```dart
T? birinchiMoslik<T>(List<T> royxat, bool Function(T) shart) {
  for (var element in royxat) {
    if (shart(element)) return element;
  }
  return null;
}

void main() {
  var sonlar = [10, 15, 20, 25];
  var topildi = birinchiMoslik<int>(sonlar, (n) => n > 18);
  print('18 dan katta birinchi son: $topildi');

  var yoq = birinchiMoslik<int>(sonlar, (n) => n > 100);
  print('100 dan kattasi: $yoq');
}
```

## Tushuntirish va Mantiq:
Qaytuvchi qiymat `T?` bo'lib, element topilmagan holatda null qaytishi null-safety qoidasiga mos keladi.

## Ishlash natijasi:
```text
18 dan katta birinchi son: 20
100 dan kattasi: null
```

# 560-Topshiriq: Generik Maksimum topuvchi (<T extends Comparable<T>>)

## Topshiriq sharti:
O'zaro taqqoslanadigan ixtiyoriy turlar orasidan kattasini aniqlovchi generik funksiya tuzing.

## Yechim (Dart kodi):
```dart
T maksimum<T extends Comparable<T>>(T a, T b) {
  return a.compareTo(b) >= 0 ? a : b;
}

void main() {
  print('Katta son: ${maksimum(42, 99)}');
  print('Katta matn: ${maksimum("olma", "uzum")}');
}
```

## Tushuntirish va Mantiq:
`<T extends Comparable<T>>` cheklovi `compareTo()` metodining mavjudligini kafolatlaydi.

## Ishlash natijasi:
```text
Katta son: 99
Katta matn: uzum
```

# 561-Topshiriq: Generik ApiResponse modeli

## Topshiriq sharti:
Server javobini ma'lumot (`T data`), xatolik va holat kodi bilan ifodalovchi generik qobiq (envelope) klass tuzing.

## Yechim (Dart kodi):
```dart
class ApiResponse<T> {
  final int statusCode;
  final T? data;
  final String? error;

  ApiResponse.success(this.data)
      : statusCode = 200,
        error = null;

  ApiResponse.error(this.error, [this.statusCode = 400]) : data = null;

  bool get isSuccess => statusCode == 200 && data != null;

  @override
  String toString() => isSuccess ? 'Success($data)' : 'Error($statusCode: $error)';
}

void main() {
  var res1 = ApiResponse<String>.success('Foydalanuvchi ma\'lumotlari');
  var res2 = ApiResponse<String>.error('Server ulanishida xatolik', 500);

  print(res1);
  print(res2);
}
```

## Tushuntirish va Mantiq:
API bilan ishlashda generik `ApiResponse<T>` xizmat qiladi, natija xavfsiz holda tekshiriladi.

## Ishlash natijasi:
```text
Success(Foydalanuvchi ma'lumotlari)
Error(500: Server ulanishida xatolik)
```

# 562-Topshiriq: Generik Kesh (Cache) klassi

## Topshiriq sharti:
Kalit `K` va qiymat `V` generik parametrlariga ega xotira keshini tuzing.

## Yechim (Dart kodi):
```dart
class GenerikKesh<K, V> {
  final Map<K, V> _xotira = {};

  void yozish(K kalit, V qiymat) => _xotira[kalit] = qiymat;

  V? olish(K kalit) => _xotira[kalit];

  bool bormi(K kalit) => _xotira.containsKey(kalit);
}

void main() {
  var kesh = GenerikKesh<int, String>();
  kesh.yozish(1, 'Bir');
  kesh.yozish(2, 'Ikki');

  print('Kalit 1: ${kesh.olish(1)}');
  print('Kalit 5 bormi: ${kesh.bormi(5)}');
}
```

## Tushuntirish va Mantiq:
Kesh ma'lumotlar bazasi yoki tarmoq so'rovlarini kamaytirish uchun tur xavfsiz usulda ishlatiladi.

## Ishlash natijasi:
```text
Kalit 1: Bir
Kalit 5 bormi: false
```

# 563-Topshiriq: Generik Repozitoriy interfeysi (Repository<T, ID>)

## Topshiriq sharti:
Entity `T` va identifikator turi `ID` uchun standart CRUD metodlariga ega generik interfeys tuzing.

## Yechim (Dart kodi):
```dart
abstract class Repozitoriy<T, ID> {
  void saqlash(T entity);
  T? idBoyichaTopish(ID id);
  List<T> hammasi();
}

class Xodim {
  final int id;
  final String ism;
  Xodim(this.id, this.ism);
}

class XodimRepozitoriy implements Repozitoriy<Xodim, int> {
  final Map<int, Xodim> _jadval = {};

  @override
  void saqlash(Xodim entity) => _jadval[entity.id] = entity;

  @override
  Xodim? idBoyichaTopish(int id) => _jadval[id];

  @override
  List<Xodim> hammasi() => _jadval.values.toList();
}

void main() {
  var repo = XodimRepozitoriy();
  repo.saqlash(Xodim(10, 'Jasur'));

  var x = repo.idBoyichaTopish(10);
  print('Xodim topildi: ${x?.ism}');
}
```

## Tushuntirish va Mantiq:
`Repozitoriy<T, ID>` klassik DDD korxona naqshi bo'lib, har qanday model uchun CRUD interfeysini unifikatsiya qiladi.

## Ishlash natijasi:
```text
Xodim topildi: Jasur
```

# 564-Topshiriq: Generik Binar Daraxt Tuguni (TreeNode<T>)

## Topshiriq sharti:
Ixtiyoriy tipdagi qiymatni saqlovchi binar daraxt tugunini generik klass orqali tuzing.

## Yechim (Dart kodi):
```dart
class DaraxtTuguni<T> {
  T qiymat;
  DaraxtTuguni<T>? chap;
  DaraxtTuguni<T>? ong;

  DaraxtTuguni(this.qiymat, [this.chap, this.ong]);

  void inOrderChop() {
    chap?.inOrderChop();
    print(qiymat);
    ong?.inOrderChop();
  }
}

void main() {
  var daraxt = DaraxtTuguni<String>(
    'B',
    DaraxtTuguni('A'),
    DaraxtTuguni('C'),
  );

  print('Daraxt elementlari tartib bilan:');
  daraxt.inOrderChop();
}
```

## Tushuntirish va Mantiq:
Binar daraxt rekursiv generik ma'lumot tuzilmasi bo'lib, qidiruv va tartiblash uchun xizmat qiladi.

## Ishlash natijasi:
```text
Daraxt elementlari tartib bilan:
A
B
C
```

# 565-Topshiriq: Generik ro'yxatni bo'laklarga ajratish (Chunk)

## Topshiriq sharti:
Ro'yxatni berilgan o'lchamdagi kichik bo'laklarga (chunks) ajratuvchi generik funksiya tuzing.

## Yechim (Dart kodi):
```dart
List<List<T>> chunkList<T>(List<T> royxat, int olcham) {
  List<List<T>> bolaklar = [];
  for (int i = 0; i < royxat.length; i += olcham) {
    int oxir = (i + olcham < royxat.length) ? i + olcham : royxat.length;
    bolaklar.add(royxat.sublist(i, oxir));
  }
  return bolaklar;
}

void main() {
  var sonlar = [1, 2, 3, 4, 5, 6, 7, 8];
  var bolingan = chunkList<int>(sonlar, 3);
  print('3 tadan bo\'laklar: $bolingan');
}
```

## Tushuntirish va Mantiq:
Katta hajmdagi ma'lumotlar bilan ishlashda va pagination yaratishda ro'yxatni generik bo'laklash zarur bo'ladi.

## Ishlash natijasi:
```text
3 tadan bo'laklar: [[1, 2, 3], [4, 5, 6], [7, 8]]
```

# 566-Topshiriq: Generik Ro'yxatni tekislash (Flatten)

## Topshiriq sharti:
Ichma-ich joylashgan `List<List<T>>` ni bitta tekis `List<T>` ro'yxatga aylantiruvchi generik funksiya tuzing.

## Yechim (Dart kodi):
```dart
List<T> tekisla<T>(List<List<T>> qatlamlar) {
  return [for (var qatlam in qatlamlar) ...qatlam];
}

void main() {
  List<List<int>> matritsa = [
    [1, 2],
    [3, 4],
    [5, 6]
  ];

  var tekis = tekisla<int>(matritsa);
  print('Tekislangan ro\'yxat: $tekis');
}
```

## Tushuntirish va Mantiq:
Spread operator `...` yordamida ichki ro'yxatlar elementlari bitta tashqi ro'yxatga birlashtiriladi.

## Ishlash natijasi:
```text
Tekislangan ro'yxat: [1, 2, 3, 4, 5, 6]
```

# 567-Topshiriq: Generik takrorlanmas elementlar to'plami (Unique)

## Topshiriq sharti:
Ro'yxat ichidan takrorlanuvchi elementlarni olib tashlab tartibini saqlovchi generik funksiya yozing.

## Yechim (Dart kodi):
```dart
List<T> unikalElementlar<T>(List<T> royxat) {
  var korilganlar = <T>{};
  List<T> natija = [];

  for (var element in royxat) {
    if (korilganlar.add(element)) {
      natija.add(element);
    }
  }
  return natija;
}

void main() {
  var sonlar = [1, 3, 2, 3, 1, 4, 5, 2];
  print('Unikal sonlar: ${unikalElementlar(sonlar)}');

  var harflar = ['a', 'b', 'a', 'c'];
  print('Unikal harflar: ${unikalElementlar(harflar)}');
}
```

## Tushuntirish va Mantiq:
`Set.add()` metodi element mavjud bo'lmasa true qaytaradi, bu orqali tartibni saqlab unikal ro'yxat olinadi.

## Ishlash natijasi:
```text
Unikal sonlar: [1, 3, 2, 4, 5]
Unikal harflar: [a, b, c]
```

# 568-Topshiriq: Generik elementlarni guruhlash (groupBy)

## Topshiriq sharti:
Ro'yxat elementlarini belgilangan kalit funksiyasi bo'yicha Map ga guruhlovchi generik funksiya yozing.

## Yechim (Dart kodi):
```dart
Map<K, List<T>> guruhlash<T, K>(List<T> royxat, K Function(T) kalitTanlovchi) {
  Map<K, List<T>> xarita = {};
  for (var element in royxat) {
    K kalit = kalitTanlovchi(element);
    xarita.putIfAbsent(kalit, () => []).add(element);
  }
  return xarita;
}

void main() {
  var sozlar = ['olma', 'anor', 'behi', 'shaftoli', 'nok'];
  // Uzunligi bo'yicha guruhlash
  var guruhlangan = guruhlash<String, int>(sozlar, (s) => s.length);

  print('Uzunlik bo\'yicha: $guruhlangan');
}
```

## Tushuntirish va Mantiq:
`guruhlash<T, K>` SQL dagi `GROUP BY` amalining xotiradagi generik va tezkor varianti hisoblanadi.

## Ishlash natijasi:
```text
Uzunlik bo'yicha: {4: [olma, anor, behi], 8: [shaftoli], 3: [nok]}
```

# 569-Topshiriq: Generik Builder naqshi

## Topshiriq sharti:
Obyektni bosqichma-bosqich yig'uvchi va `build()` orqali natijani qaytaruvchi `Quruvchi<T>` interfeysini tuzing.

## Yechim (Dart kodi):
```dart
abstract class Quruvchi<T> {
  T build();
}

class Kompyuter {
  final String cpu;
  final int ram;
  Kompyuter(this.cpu, this.ram);

  @override
  String toString() => 'PC: $cpu, ${ram}GB RAM';
}

class KompyuterQuruvchi implements Quruvchi<Kompyuter> {
  String cpu = 'Core i5';
  int ram = 16;

  KompyuterQuruvchi setCpu(String c) {
    cpu = c;
    return this;
  }

  KompyuterQuruvchi setRam(int r) {
    ram = r;
    return this;
  }

  @override
  Kompyuter build() => Kompyuter(cpu, ram);
}

void main() {
  var pc = KompyuterQuruvchi().setCpu('Apple M3').setRam(32).build();
  print(pc);
}
```

## Tushuntirish va Mantiq:
Builder pattern murakkab obyektlarni zanjirli usulda (fluent API) qulay yig'ishga yordam beradi.

## Ishlash natijasi:
```text
PC: Apple M3, 32GB RAM
```

# 570-Topshiriq: Generik EventBus (Voqealar shinasi)

## Topshiriq sharti:
Tip bo'yicha voqealarni obuna qiluvchi va tarqatuvchi generik `EventBus` sinfini tuzing.

## Yechim (Dart kodi):
```dart
class EventBus {
  final Map<Type, List<void Function(dynamic)>> _obunalar = {};

  void on<T>(void Function(T) tinglovchi) {
    _obunalar.putIfAbsent(T, () => []).add((e) => tinglovchi(e as T));
  }

  void fire<T>(T voqea) {
    var tinglovchilar = _obunalar[T];
    if (tinglovchilar != null) {
      for (var t in tinglovchilar) {
        t(voqea);
      }
    }
  }
}

class KirishVoqeasi {
  final String ism;
  KirishVoqeasi(this.ism);
}

void main() {
  var bus = EventBus();
  bus.on<KirishVoqeasi>((e) => print('Xush kelibsiz: ${e.ism}'));

  bus.fire(KirishVoqeasi('Sherzod'));
}
```

## Tushuntirish va Mantiq:
Generik EventBus ilova komponentlari orasidagi bog'liqlikni uzish (decoupling) uchun ishlatiladi.

## Ishlash natijasi:
```text
Xush kelibsiz: Sherzod
```

# 571-Topshiriq: Generik Konverter (Mapper<From, To>)

## Topshiriq sharti:
Bir turdagi obyektni boshqa turga o'giruvchi `Konverter<Kirish, Chiqish>` interfeysi va amalini tuzing.

## Yechim (Dart kodi):
```dart
abstract class Konverter<Kirish, Chiqish> {
  Chiqish transform(Kirish input);
}

class FoydalanuvchiDto {
  final String ism;
  final int tugilganYil;
  FoydalanuvchiDto(this.ism, this.tugilganYil);
}

class FoydalanuvchiModel {
  final String ism;
  final int yosh;
  FoydalanuvchiModel(this.ism, this.yosh);
}

class DtoModelKonverter implements Konverter<FoydalanuvchiDto, FoydalanuvchiModel> {
  @override
  FoydalanuvchiModel transform(FoydalanuvchiDto input) {
    int yosh = 2026 - input.tugilganYil;
    return FoydalanuvchiModel(input.ism, yosh);
  }
}

void main() {
  var conv = DtoModelKonverter();
  var dto = FoydalanuvchiDto('Botir', 2000);
  var model = conv.transform(dto);

  print('Model: ${model.ism}, Yoshi: ${model.yosh}');
}
```

## Tushuntirish va Mantiq:
DTO va Domen modellari orasidagi konvertatsiyani generik interfeyslar orqali toza ajratish mumkin.

## Ishlash natijasi:
```text
Model: Botir, Yoshi: 26
```

# 572-Topshiriq: Generik Xotira ro'yxati (MemoryTable<T>)

## Topshiriq sharti:
Baza jadvallari kabi filtrlash va qo'shish imkonini beruvchi generik `XotiraJadvali<T>` tuzing.

## Yechim (Dart kodi):
```dart
class XotiraJadvali<T> {
  final List<T> _qatorlar = [];

  void kiritish(T qator) => _qatorlar.add(qator);

  List<T> qidirish(bool Function(T) shart) {
    return _qatorlar.where(shart).toList();
  }
}

void main() {
  var jadval = XotiraJadvali<String>();
  jadval.kiritish('Toshkent');
  jadval.kiritish('Samarqand');
  jadval.kiritish('Termiz');

  var tBilanBoshlanadigan = jadval.qidirish((sh) => sh.startsWith('T'));
  print('T bilan boshlanadigan shaharlar: $tBilanBoshlanadigan');
}
```

## Tushuntirish va Mantiq:
Generik xotira jadvali ma'lumotlar bazasisiz tezkor ma'lumotlar bilan manipulyatsiya qilish uchun qulaydir.

## Ishlash natijasi:
```text
T bilan boshlanadigan shaharlar: [Toshkent, Termiz]
```

# 573-Topshiriq: Generik Validatsiya natijasi (ValidationResult<T>)

## Topshiriq sharti:
Tekshiruvdan o'tgan qiymatni yoki xatolar ro'yxatini generik saqlovchi klass tuzing.

## Yechim (Dart kodi):
```dart
class ValidatsiyaNatijasi<T> {
  final T? qiymat;
  final List<String> xatolar;

  ValidatsiyaNatijasi.togri(this.qiymat) : xatolar = const [];
  ValidatsiyaNatijasi.xato(this.xatolar) : qiymat = null;

  bool get yaroqlimi => xatolar.isEmpty;
}

ValidatsiyaNatijasi<int> tekshirYosh(int yosh) {
  if (yosh < 0) return ValidatsiyaNatijasi.xato(['Yosh manfiy bo\'lmaydi']);
  if (yosh > 150) return ValidatsiyaNatijasi.xato(['Maksimal yoshdan katta']);
  return ValidatsiyaNatijasi.togri(yosh);
}

void main() {
  var r = tekshirYosh(25);
  print('Yaroqlimi: ${r.yaroqlimi}, Qiymat: ${r.qiymat}');

  var x = tekshirYosh(-5);
  print('Yaroqlimi: ${x.yaroqlimi}, Xatolar: ${x.xatolar}');
}
```

## Tushuntirish va Mantiq:
Generik validatsiya natijasi foydalanuvchi formalaridagi xatoliklarni xavfsiz va aniq qaytaradi.

## Ishlash natijasi:
```text
Yaroqlimi: true, Qiymat: 25
Yaroqlimi: false, Xatolar: [Yosh manfiy bo'lmaydi]
```

# 574-Topshiriq: Generik Cheklangan Ro'yxat (FixedSizeList<T>)

## Topshiriq sharti:
Maksimal sig'imidan oshib ketmaydigan, to'lganda eng eskisini chiqarib yuboruvchi generik bufer tuzing.

## Yechim (Dart kodi):
```dart
class CheklanganBufer<T> {
  final int sigim;
  final List<T> _ichki = [];

  CheklanganBufer(this.sigim);

  void qoshish(T element) {
    if (_ichki.length == sigim) {
      _ichki.removeAt(0); // Eng eskisini o'chirish
    }
    _ichki.add(element);
  }

  List<T> toList() => List.unmodifiable(_ichki);
}

void main() {
  var b = CheklanganBufer<int>(3);
  b.qoshish(1);
  b.qoshish(2);
  b.qoshish(3);
  b.qoshish(4); // 1 chiqib ketadi

  print('Bufer: ${b.toList()}');
}
```

## Tushuntirish va Mantiq:
Cheklangan bufer (Ring/Circular buffer analogi) oxirgi N ta xabarni yoki telemetriyani xotirada ushlab turish uchun ishlatiladi.

## Ishlash natijasi:
```text
Bufer: [2, 3, 4]
```

# 575-Topshiriq: Generik Matritsa klassi (Matritsa<T>)

## Topshiriq sharti:
Ixtiyoriy turdagi kataklarga ega bo'lgan 2D `Matritsa<T>` ma'lumotlar tuzilmasini tuzing.

## Yechim (Dart kodi):
```dart
class Matritsa<T> {
  final int qatorlar;
  final int ustunlar;
  final List<List<T>> _kataklar;

  Matritsa(this.qatorlar, this.ustunlar, T def)
      : _kataklar = List.generate(
          qatorlar,
          (_) => List.filled(ustunlar, def),
        );

  T get(int r, int c) => _kataklar[r][c];
  void set(int r, int c, T val) => _kataklar[r][c] = val;

  void chopEtish() {
    for (var satr in _kataklar) {
      print(satr.join(' '));
    }
  }
}

void main() {
  var shaxmat = Matritsa<String>(3, 3, '.');
  shaxmat.set(0, 0, 'X');
  shaxmat.set(1, 1, 'O');
  shaxmat.set(2, 2, 'X');

  shaxmat.chopEtish();
}
```

## Tushuntirish va Mantiq:
Generik parametr orqali matritsa nafaqat sonlar, balki matnlar, piksellar yoki shaxmat donalari uchun ham ishlaydi.

## Ishlash natijasi:
```text
X . .
. O .
. . X
```

# 576-Topshiriq: Generik Binar Qidiruv Daraxti (BST<T extends Comparable<T>>)

## Topshiriq sharti:
Taqqoslanuvchi turlar uchun elementlarni tartibli joylashtiruvchi Binar Qidiruv Daraxtini tuzing.

## Yechim (Dart kodi):
```dart
class BstTugun<T extends Comparable<T>> {
  T qiymat;
  BstTugun<T>? chap;
  BstTugun<T>? ong;

  BstTugun(this.qiymat);

  void qoshish(T yangi) {
    if (yangi.compareTo(qiymat) < 0) {
      if (chap == null) {
        chap = BstTugun(yangi);
      } else {
        chap!.qoshish(yangi);
      }
    } else {
      if (ong == null) {
        ong = BstTugun(yangi);
      } else {
        ong!.qoshish(yangi);
      }
    }
  }

  bool qidirish(T nishon) {
    int c = nishon.compareTo(qiymat);
    if (c == 0) return true;
    if (c < 0) return chap?.qidirish(nishon) ?? false;
    return ong?.qidirish(nishon) ?? false;
  }
}

void main() {
  var bst = BstTugun<int>(50);
  bst.qoshish(30);
  bst.qoshish(70);
  bst.qoshish(20);

  print('30 bormi: ${bst.qidirish(30)}');
  print('99 bormi: ${bst.qidirish(99)}');
}
```

## Tushuntirish va Mantiq:
Binar qidiruv daraxti elementlarni $O(\log n)$ vaqt murakkabligida izlash va tartiblash imkonini beradi.

## Ishlash natijasi:
```text
30 bormi: true
99 bormi: false
```

# 577-Topshiriq: Generik Ikki Yoqlama Bog'langan Ro'yxat (Doubly Linked List)

## Topshiriq sharti:
Har bir tuguni oldingi va keyingi tugunga havola saqlovchi generik `Bog'langanRoyxat<T>` klassini tuzing.

## Yechim (Dart kodi):
```dart
class Tugun<T> {
  T qiymat;
  Tugun<T>? oldingi;
  Tugun<T>? keyingi;
  Tugun(this.qiymat);
}

class IkkiYoqlamaRoyxat<T> {
  Tugun<T>? bosh;
  Tugun<T>? oxir;

  void qoshish(T qiymat) {
    var yangi = Tugun(qiymat);
    if (oxir == null) {
      bosh = oxir = yangi;
    } else {
      oxir!.keyingi = yangi;
      yangi.oldingi = oxir;
      oxir = yangi;
    }
  }

  void chopEtish() {
    var joriy = bosh;
    List<T> l = [];
    while (joriy != null) {
      l.add(joriy.qiymat);
      joriy = joriy.keyingi;
    }
    print(l.join(' <-> '));
  }
}

void main() {
  var royxat = IkkiYoqlamaRoyxat<String>();
  royxat.qoshish('A');
  royxat.qoshish('B');
  royxat.qoshish('C');

  royxat.chopEtish();
}
```

## Tushuntirish va Mantiq:
Ikki yoqlama bog'langan ro'yxat elementlarni har ikki yo'nalishda tezkor qo'shish va o'chirishga qulay.

## Ishlash natijasi:
```text
A <-> B <-> C
```

# 578-Topshiriq: Generik Ustunlik Navbati (PriorityQueue<T>)

## Topshiriq sharti:
Eng yuqori ustunlikka (kichik yoki katta) ega elementni birinchi chiqaruvchi generik navbat tuzing.

## Yechim (Dart kodi):
```dart
class UstunlikNavbati<T extends Comparable<T>> {
  final List<T> _heap = [];

  void push(T element) {
    _heap.add(element);
    _heap.sort(); // Sodda tartiblash
  }

  T pop() {
    if (_heap.isEmpty) throw StateError('Navbat bo\'sh');
    return _heap.removeAt(0); // Eng kichigi / muhimi birinchi
  }

  int get length => _heap.length;
}

void main() {
  var navbat = UstunlikNavbati<int>();
  navbat.push(45);
  navbat.push(12);
  navbat.push(89);
  navbat.push(5);

  print('Birinchi olingan: ${navbat.pop()}');
  print('Ikkinchi olingan: ${navbat.pop()}');
}
```

## Tushuntirish va Mantiq:
Priority Queue algoritmlarda (Dijkstra, A*) eng ustuvor tugunlarni birinchi tartibda ko'rib chiqish uchun ishlatiladi.

## Ishlash natijasi:
```text
Birinchi olingan: 5
Ikkinchi olingan: 12
```

# 579-Topshiriq: Generik Graf ma'lumotlar tuzilmasi (Graf<T> va BFS)

## Topshiriq sharti:
Tugunlar va qirralardan iborat generik Graf tuzilmasini va kenglik bo'yicha qidiruv (BFS) algoritmini yozing.

## Yechim (Dart kodi):
```dart
class Graf<T> {
  final Map<T, List<T>> _qoshnilar = {};

  void qirraQosh(T u, T v) {
    _qoshnilar.putIfAbsent(u, () => []).add(v);
    _qoshnilar.putIfAbsent(v, () => []).add(u);
  }

  List<T> bfs(T boshlangich) {
    List<T> tartib = [];
    Set<T> tashrif = {boshlangich};
    List<T> navbat = [boshlangich];

    while (navbat.isNotEmpty) {
      T joriy = navbat.removeAt(0);
      tartib.add(joriy);

      for (var qoshni in _qoshnilar[joriy] ?? []) {
        if (!tashrif.contains(qoshni)) {
          tashrif.add(qoshni);
          navbat.add(qoshni);
        }
      }
    }
    return tartib;
  }
}

void main() {
  var g = Graf<String>();
  g.qirraQosh('Toshkent', 'Samarqand');
  g.qirraQosh('Toshkent', 'Farg\'ona');
  g.qirraQosh('Samarqand', 'Buxoro');

  print('BFS marshruti: ${g.bfs("Toshkent")}');
}
```

## Tushuntirish va Mantiq:
Generik Graf shahar nomlari, tarmoq tugunlari yoki ijtimoiy tarmoq foydalanuvchilarini modellashtirishga xizmat qiladi.

## Ishlash natijasi:
```text
BFS marshruti: [Toshkent, Samarqand, Farg'ona, Buxoro]
```

# 580-Topshiriq: Generik LRU (Least Recently Used) Kesh tizimi

## Topshiriq sharti:
Sig'imi cheklangan va eng kam ishlatilgan elementni avtomatik o'chiruvchi generik `LruKesh<K, V>` tuzing.

## Yechim (Dart kodi):
```dart
class LruKesh<K, V> {
  final int sigim;
  final Map<K, V> _map = {};

  LruKesh(this.sigim);

  V? get(K kalit) {
    if (!_map.containsKey(kalit)) return null;
    V qiymat = _map.remove(kalit)!;
    _map[kalit] = qiymat; // Oxiriga qo'yish (eng yangi)
    return qiymat;
  }

  void put(K kalit, V qiymat) {
    if (_map.containsKey(kalit)) {
      _map.remove(kalit);
    } else if (_map.length >= sigim) {
      K engEski = _map.keys.first;
      _map.remove(engEski);
    }
    _map[kalit] = qiymat;
  }

  @override
  String toString() => _map.toString();
}

void main() {
  var kesh = LruKesh<int, String>(2);
  kesh.put(1, 'Bir');
  kesh.put(2, 'Ikki');
  kesh.get(1); // 1 ishlatildi, endi 2 eng eski
  kesh.put(3, 'Uch'); // 2 o'chib ketadi

  print('Kesh holati: $kesh');
}
```

## Tushuntirish va Mantiq:
LRU kesh xotiradan oqilona foydalanish va eng ommabop elementlarni tezkor saqlash standarti hisoblanadi.

## Ishlash natijasi:
```text
Kesh holati: {1: Bir, 3: Uch}
```

# 581-Topshiriq: Generik Prefiks Daraxti (Trie ma'lumot tuzilmasi)

## Topshiriq sharti:
Lug'atdagi so'zlarni harflar bo'yicha tez qidiruvchi va avtomatik to'ldiruvchi Trie tuzilmasini yozing.

## Yechim (Dart kodi):
```dart
class TrieTugun {
  final Map<String, TrieTugun> bolalar = {};
  bool sozOxirimi = false;
}

class TrieDaraxt {
  final TrieTugun ildiz = TrieTugun();

  void qoshish(String soz) {
    var joriy = ildiz;
    for (int i = 0; i < soz.length; i++) {
      String harf = soz[i];
      joriy = joriy.bolalar.putIfAbsent(harf, () => TrieTugun());
    }
    joriy.sozOxirimi = true;
  }

  bool mavjudmi(String soz) {
    var joriy = ildiz;
    for (int i = 0; i < soz.length; i++) {
      String harf = soz[i];
      if (!joriy.bolalar.containsKey(harf)) return false;
      joriy = joriy.bolalar[harf]!;
    }
    return joriy.sozOxirimi;
  }
}

void main() {
  var trie = TrieDaraxt();
  trie.qoshish('dart');
  trie.qoshish('data');

  print('dart bormi: ${trie.mavjudmi("dart")}');
  print('dark bormi: ${trie.mavjudmi("dark")}');
}
```

## Tushuntirish va Mantiq:
Trie daraxti matnli qidiruv, avtotekshiruv va lug'at algoritmlarida juda yuqori samaradorlik beradi.

## Ishlash natijasi:
```text
dart bormi: true
dark bormi: false
```

# 582-Topshiriq: Generik Funktor (Functor Pattern)

## Topshiriq sharti:
O'z ichidagi qiymatni o'zgartirib yangi qobiq qaytaruvchi `map` metodiga ega `Qobiq<T>` tuzing.

## Yechim (Dart kodi):
```dart
class Qobiq<T> {
  final T qiymat;

  Qobiq(this.qiymat);

  Qobiq<R> map<R>(R Function(T) f) {
    return Qobiq<R>(f(qiymat));
  }

  @override
  String toString() => 'Qobiq($qiymat)';
}

void main() {
  var q1 = Qobiq<int>(5);
  var q2 = q1.map((x) => x * 2).map((x) => 'Natija: $x');

  print(q2);
}
```

## Tushuntirish va Mantiq:
Funktor har qanday qobiqdagi qiymatni ochmasdan turib uning ustida funksiya qo'llash imkonini beradi.

## Ishlash natijasi:
```text
Qobiq(Natija: 10)
```

# 583-Topshiriq: Generik Monada (Monad flatMap zanjiri)

## Topshiriq sharti:
Ichma-ich qobiqlar hosil bo'lishining oldini oluvchi `flatMap` metodiga ega generik monada tuzing.

## Yechim (Dart kodi):
```dart
class Monada<T> {
  final T qiymat;

  Monada(this.qiymat);

  Monada<R> flatMap<R>(Monada<R> Function(T) f) {
    return f(qiymat);
  }

  @override
  String toString() => 'Monada($qiymat)';
}

Monada<int> kvadrat(int x) => Monada(x * x);
Monada<int> ikkiBaravar(int x) => Monada(x * 2);

void main() {
  var m = Monada(3).flatMap(kvadrat).flatMap(ikkiBaravar);
  print(m);
}
```

## Tushuntirish va Mantiq:
Monada zanjirli asinxron yoki hisoblash operatsiyalarini xavfsiz va ketma-ket bajarishga yordam beradi.

## Ishlash natijasi:
```text
Monada(18)
```

# 584-Topshiriq: Generik Service Locator (DI Konteyneri)

## Topshiriq sharti:
Ilovaning barcha xizmatlarini tipi bo'yicha ro'yxatdan o'tkazuvchi va qaytaruvchi `Locator` tuzing.

## Yechim (Dart kodi):
```dart
class ServisLokatari {
  static final Map<Type, dynamic> _servislar = {};

  static void royxatdanOtish<T>(T servis) {
    _servislar[T] = servis;
  }

  static T olish<T>() {
    var s = _servislar[T];
    if (s == null) throw StateError('Servis topilmadi: $T');
    return s as T;
  }
}

class ApiServis {
  void sorov() => print('API so\'rovi yuborildi.');
}

void main() {
  ServisLokatari.royxatdanOtish<ApiServis>(ApiServis());

  var api = ServisLokatari.olish<ApiServis>();
  api.sorov();
}
```

## Tushuntirish va Mantiq:
Flutterdagi `get_it` kutubxonasi aynan shu generik servis lokatori prinsipi asosida qurilgan.

## Ishlash natijasi:
```text
API so'rovi yuborildi.
```

# 585-Topshiriq: Generik Kuzatuvchi (Observable<T>)

## Topshiriq sharti:
Qiymat o'zgarganda barcha tinglovchilarga yangi qiymatni uzatuvchi generik `Kuzatiluvchi<T>` tuzing.

## Yechim (Dart kodi):
```dart
class Kuzatiluvchi<T> {
  T _qiymat;
  final List<void Function(T)> _tinglovchilar = [];

  Kuzatiluvchi(this._qiymat);

  T get qiymat => _qiymat;

  set qiymat(T yangi) {
    _qiymat = yangi;
    for (var t in _tinglovchilar) {
      t(yangi);
    }
  }

  void obuna(void Function(T) cb) => _tinglovchilar.add(cb);
}

void main() {
  var harorat = Kuzatiluvchi<double>(20.0);
  harorat.obuna((t) => print('Yangi harorat: $t°C'));

  harorat.qiymat = 22.5;
  harorat.qiymat = 25.0;
}
```

## Tushuntirish va Mantiq:
Generik kuzatiluvchi o'zgaruvchi reaktiv dasturlashning asosiy tayanchi hisoblanadi.

## Ishlash natijasi:
```text
Yangi harorat: 22.5°C
Yangi harorat: 25.0°C
```

# 586-Topshiriq: Generik Pipeline va Middleware tizimi

## Topshiriq sharti:
Ma'lumotni ketma-ket bir nechta filtrlardan o'tkazuvchi generik konveyer tuzing.

## Yechim (Dart kodi):
```dart
typedef Bosqich<T> = T Function(T input);

class Konveyer<T> {
  final List<Bosqich<T>> _bosqichlar = [];

  void qoshish(Bosqich<T> b) => _bosqichlar.add(b);

  T ishgaTushirish(T boshlangich) {
    T joriy = boshlangich;
    for (var b in _bosqichlar) {
      joriy = b(joriy);
    }
    return joriy;
  }
}

void main() {
  var p = Konveyer<String>();
  p.qoshish((s) => s.trim());
  p.qoshish((s) => s.toUpperCase());
  p.qoshish((s) => '>>> $s <<<');

  print(p.ishgaTushirish('   salom dunyo   '));
}
```

## Tushuntirish va Mantiq:
Pipeline arxitekturasi ma'lumotlarni bosqichma-bosqich tozalash va o'zgartirish uchun qulay.

## Ishlash natijasi:
```text
>>> SALOM DUNYO <<<
```

# 587-Topshiriq: Generik Smart Enum naqshi

## Topshiriq sharti:
Standart enumdan ko'ra boyroq xususiyatlarga ega bo'lgan generik `SmartEnum<T>` tuzing.

## Yechim (Dart kodi):
```dart
abstract class SmartEnum<T> {
  final String nom;
  final T qiymat;

  const SmartEnum(this.nom, this.qiymat);

  @override
  String toString() => '$nom: $qiymat';
}

class Muhit extends SmartEnum<String> {
  static const dev = Muhit._('DEVELOPMENT', 'http://localhost');
  static const prod = Muhit._('PRODUCTION', 'https://uzbekai.uz');

  const Muhit._(super.nom, super.qiymat);
}

void main() {
  print(Muhit.dev);
  print(Muhit.prod);
}
```

## Tushuntirish va Mantiq:
Smart Enum qo'shimcha metodlar va generik qiymatlarni bitta tushunchada birlashtiradi.

## Ishlash natijasi:
```text
DEVELOPMENT: http://localhost
PRODUCTION: https://uzbekai.uz
```

# 588-Topshiriq: Generik Serializatsiya shartnomasi

## Topshiriq sharti:
JSON ga o'giriluvchi va JSON dan qayta tiklanuvchi generik shartnomani tuzing.

## Yechim (Dart kodi):
```dart
abstract class Serializatsiya<T> {
  Map<String, dynamic> toJson();
}

class Shahar implements Serializatsiya<Shahar> {
  final String nom;
  final int aholi;

  Shahar(this.nom, this.aholi);

  @override
  Map<String, dynamic> toJson() => {'nom': nom, 'aholi': aholi};
}

void saqla<T extends Serializatsiya<T>>(T obyekt) {
  print('JSON saqlandi: ${obyekt.toJson()}');
}

void main() {
  saqla(Shahar('Samarqand', 550000));
}
```

## Tushuntirish va Mantiq:
`<T extends Serializatsiya<T>>` chegarasi funksiyaga faqat serializatsiya qila oladigan obyektlar kirishini ta'minlaydi.

## Ishlash natijasi:
```text
JSON saqlandi: {nom: Samarqand, aholi: 550000}
```

# 589-Topshiriq: Generik Comparator generatori (byKey)

## Topshiriq sharti:
Obyektning ixtiyoriy maydoni bo'yicha saralovchi umumiy solishtirgich funksiya generatorini yozing.

## Yechim (Dart kodi):
```dart
Comparator<T> solishtirgichYarat<T, K extends Comparable<K>>(K Function(T) kalit) {
  return (a, b) => kalit(a).compareTo(kalit(b));
}

class Xodim {
  final String ism;
  final int maosh;
  Xodim(this.ism, this.maosh);
}

void main() {
  var xodimlar = [
    Xodim('Nodir', 8000),
    Xodim('Anvar', 12000),
    Xodim('Zafar', 6000),
  ];

  xodimlar.sort(solishtirgichYarat((x) => x.maosh));

  for (var x in xodimlar) {
    print('${x.ism}: ${x.maosh}');
  }
}
```

## Tushuntirish va Mantiq:
Generik `solishtirgichYarat` yordamida har bir maydon uchun qaytadan qiyoslash kodi yozish shart bo'lmaydi.

## Ishlash natijasi:
```text
Zafar: 6000
Nodir: 8000
Anvar: 12000
```

# 590-Topshiriq: Generik Obyektlar Hovuzi (Object Pool<T>)

## Topshiriq sharti:
Yangi yaratish o'rniga foydalanilgan obyektlarni qayta beruvchi generik hovuz tuzing.

## Yechim (Dart kodi):
```dart
class ObyektlarHovuzi<T> {
  final T Function() yaratuvchi;
  final List<T> _boshlar = [];

  ObyektlarHovuzi(this.yaratuvchi);

  T olish() {
    if (_boshlar.isNotEmpty) {
      return _boshlar.removeLast();
    }
    return yaratuvchi();
  }

  void qaytarish(T obj) {
    _boshlar.add(obj);
  }
}

void main() {
  int sanoq = 0;
  var pool = ObyektlarHovuzi<String>(() => 'Obyekt #${++sanoq}');

  var o1 = pool.olish();
  print('Olindi: $o1');
  pool.qaytarish(o1);

  var o2 = pool.olish();
  print('Qayta olindi: $o2');
}
```

## Tushuntirish va Mantiq:
Obyektlar hovuzi xotira tozalagichiga (GC) yuklamani kamaytiradi.

## Ishlash natijasi:
```text
Olindi: Obyekt #1
Qayta olindi: Obyekt #1
```

# 591-Topshiriq: Generik Resurs Yuklagich (ResourceLoader<T>)

## Topshiriq sharti:
Resurs yuklash holatini (Kutilmoqda, Muvaffaqiyatli, Xato) generik sinf orqali boshqaring.

## Yechim (Dart kodi):
```dart
class ResursHolati<T> {
  final T? data;
  final bool yuklanmoqda;
  final String? xato;

  ResursHolati.loading() : data = null, yuklanmoqda = true, xato = null;
  ResursHolati.success(this.data) : yuklanmoqda = false, xato = null;
  ResursHolati.error(this.xato) : data = null, yuklanmoqda = false;
}

void main() {
  var s = ResursHolati<List<int>>.success([1, 2, 3]);
  print('Yuklandi: ${s.data}, yuklanmoqdami: ${s.yuklanmoqda}');
}
```

## Tushuntirish va Mantiq:
Mobil ilovalarda har qanday ma'lumotning yuklanish holatini bitta generik andaza bilan boshqarish mumkin.

## Ishlash natijasi:
```text
Yuklandi: [1, 2, 3], yuklanmoqdami: false
```

# 592-Topshiriq: Generik Pagination javobi (PaginatedResult<T>)

## Topshiriq sharti:
Sahifalangan ro'yxat, jami elementlar va sahifa raqamini saqlovchi generik model tuzing.

## Yechim (Dart kodi):
```dart
class SahifalanganNatija<T> {
  final List<T> elementlar;
  final int joriySahifa;
  final int jamiSahifalar;

  SahifalanganNatija({
    required this.elementlar,
    required this.joriySahifa,
    required this.jamiSahifalar,
  });

  bool get keyingisiBormi => joriySahifa < jamiSahifalar;
}

void main() {
  var page = SahifalanganNatija<String>(
    elementlar: ['A', 'B', 'C'],
    joriySahifa: 1,
    jamiSahifalar: 3,
  );

  print('Sahifa 1 elementlari: ${page.elementlar}');
  print('Yana sahifa bormi: ${page.keyingisiBormi}');
}
```

## Tushuntirish va Mantiq:
Pagination modeli serverdan keluvchi katta ro'yxatlarni qismlab ko'rsatish uchun ishlatiladi.

## Ishlash natijasi:
```text
Sahifa 1 elementlari: [A, B, C]
Yana sahifa bormi: true
```

# 593-Topshiriq: Generik Ro'yxatlar Farqi (Diff<T>)

## Topshiriq sharti:
Ikki ro'yxat o'rtasida qo'shilgan va o'chirilgan elementlarni topuvchi generik funksiya yozing.

## Yechim (Dart kodi):
```dart
(Set<T>, Set<T>) royxatlarFarqi<T>(List<T> eski, List<T> yangi) {
  var sEski = eski.toSet();
  var sYangi = yangi.toSet();

  var qoshilgan = sYangi.difference(sEski);
  var ochirilgan = sEski.difference(sYangi);

  return (qoshilgan, ochirilgan);
}

void main() {
  var eski = [1, 2, 3, 4];
  var yangi = [3, 4, 5, 6];

  var (qoshildi, ochirildi) = royxatlarFarqi(eski, yangi);
  print('Qo\'shildi: $qoshildi');
  print('O\'chirildi: $ochirildi');
}
```

## Tushuntirish va Mantiq:
Ro'yxatlar diff algoritmi virtual DOM va ro'yxat animatsiyalarini (DiffUtil) yangilashda muhim ahamiyatga ega.

## Ishlash natijasi:
```text
Qo'shildi: {5, 6}
O'chirildi: {1, 2}
```

# 594-Topshiriq: Generik Birlashma turi (Union2<A, B>)

## Topshiriq sharti:
Ikki xil turdan birini saqlash imkonini beruvchi generik `Union2<A, B>` klassini tuzing.

## Yechim (Dart kodi):
```dart
class Birlashma2<A, B> {
  final A? _a;
  final B? _b;

  Birlashma2.birinchi(A a) : _a = a, _b = null;
  Birlashma2.ikkinchi(B b) : _a = null, _b = b;

  R match<R>({required R Function(A) a, required R Function(B) b}) {
    if (_a != null) return a(_a as A);
    return b(_b as B);
  }
}

void main() {
  var u1 = Birlashma2<int, String>.birinchi(100);
  var u2 = Birlashma2<int, String>.ikkinchi('Yuz');

  print(u1.match(a: (val) => 'Son: $val', b: (val) => 'Matn: $val'));
  print(u2.match(a: (val) => 'Son: $val', b: (val) => 'Matn: $val'));
}
```

## Tushuntirish va Mantiq:
Union tipi bir o'zgaruvchida faqat bitta turdagi qiymat bo'lishini tur xavfsiz holda kafolatlaydi.

## Ishlash natijasi:
```text
Son: 100
Matn: Yuz
```

# 595-Topshiriq: Generik Type Cast xavfsizligi va cast metodlari

## Topshiriq sharti:
Dinamik ro'yxatni generik parametr bo'yicha xavfsiz filtrlash va to'g'ri turga o'tkazish funksiyasini yozing.

## Yechim (Dart kodi):
```dart
List<T> faqatTuridagilar<T>(List<dynamic> aralash) {
  return aralash.whereType<T>().toList();
}

void main() {
  List<dynamic> aralash = [1, 'Salom', 2.5, 42, 'Dunyo'];
  var butunSonlar = faqatTuridagilar<int>(aralash);
  var matnlar = faqatTuridagilar<String>(aralash);

  print('Faqat int: $butunSonlar');
  print('Faqat String: $matnlar');
}
```

## Tushuntirish va Mantiq:
`whereType<T>()` metodi aralash ro'yxatdan faqat `T` turiga mos keluvchi elementlarni ajratib, toza `List<T>` beradi.

## Ishlash natijasi:
```text
Faqat int: [1, 42]
Faqat String: [Salom, Dunyo]
```

# 596-Topshiriq: Generik Qidiruv Indeksi (Inverted Index)

## Topshiriq sharti:
Kalit so'zlar bo'yicha tegishli obyektlar ro'yxatini tez topuvchi teskari indeks ma'lumot tuzilmasini tuzing.

## Yechim (Dart kodi):
```dart
class TeskariIndeks<T> {
  final Map<String, Set<T>> _indeks = {};

  void indekslash(String kalitSoz, T obyekt) {
    _indeks.putIfAbsent(kalitSoz.toLowerCase(), () => {}).add(obyekt);
  }

  Set<T> qidirish(String kalitSoz) {
    return _indeks[kalitSoz.toLowerCase()] ?? {};
  }
}

void main() {
  var index = TeskariIndeks<int>(); // Kitob ID lari
  index.indekslash('dart', 101);
  index.indekslash('dart', 102);
  index.indekslash('flutter', 102);

  print('dart so\'zi qatnashgan kitoblar: ${index.qidirish("dart")}');
}
```

## Tushuntirish va Mantiq:
Teskari indeks qidiruv tizimlarining asosi bo'lib, so'zlar orqali hujjatlarni bir zumda topish imkonini beradi.

## Ishlash natijasi:
```text
dart so'zi qatnashgan kitoblar: {101, 102}
```

# 597-Topshiriq: Generik Bloom Filter (Ehtimolli qidiruv filtri)

## Topshiriq sharti:
Element mavjud emasligini 100% aniqlik bilan aytuvchi sodda Bloom filtri algoritmini yozing.

## Yechim (Dart kodi):
```dart
class BloomFiltr<T> {
  final List<bool> _bitlar;
  final int sigim;

  BloomFiltr(this.sigim) : _bitlar = List.filled(sigim, false);

  int _hash1(T obj) => (obj.hashCode.abs()) % sigim;
  int _hash2(T obj) => ((obj.hashCode.abs() * 31) >> 2) % sigim;

  void qoshish(T element) {
    _bitlar[_hash1(element)] = true;
    _bitlar[_hash2(element)] = true;
  }

  bool bolishiMumkinmi(T element) {
    return _bitlar[_hash1(element)] && _bitlar[_hash2(element)];
  }
}

void main() {
  var filter = BloomFiltr<String>(100);
  filter.qoshish('admin');

  print('admin bormi: ${filter.bolishiMumkinmi("admin")}');
  print('hacker bormi: ${filter.bolishiMumkinmi("hacker")}');
}
```

## Tushuntirish va Mantiq:
Bloom filtri xotirani minimal darajada ishlatib, element bazada yo'qligini darhol aniqlab beradi.

## Ishlash natijasi:
```text
admin bormi: true
hacker bormi: false
```

# 598-Topshiriq: Generik BitSet / BitMask to'plami

## Topshiriq sharti:
Butun sonlar bitlarida mantiqiy bayroqlarni tejab saqlovchi BitTo'plam klassini tuzing.

## Yechim (Dart kodi):
```dart
class BitToplam {
  int _maska = 0;

  void ornat(int bit) => _maska |= (1 << bit);
  void ochir(int bit) => _maska &= ~(1 << bit);
  bool tekshir(int bit) => (_maska & (1 << bit)) != 0;
}

void main() {
  var b = BitToplam();
  b.ornat(3);
  b.ornat(7);

  print('3-bit yoniqmi: ${b.tekshir(3)}');
  print('5-bit yoniqmi: ${b.tekshir(5)}');
  print('7-bit yoniqmi: ${b.tekshir(7)}');
}
```

## Tushuntirish va Mantiq:
BitSet bitta 64-bitlik `int` ichida 64 tagacha mantiqiy holatlarni xotiradan yutgan holda saqlaydi.

## Ishlash natijasi:
```text
3-bit yoniqmi: true
5-bit yoniqmi: false
7-bit yoniqmi: true
```

# 599-Topshiriq: Generik Kvantlangan Massiv (QuantizedArray<T>)

## Topshiriq sharti:
Kvantlangan butun sonlar va haqiqiy sonlar konvertatsiyasini ta'minlovchi klass tuzing.

## Yechim (Dart kodi):
```dart
class KvantlanganMassiv {
  final List<int> kvantlar;
  final double masshtab;

  KvantlanganMassiv(this.kvantlar, this.masshtab);

  List<double> dekvantlash() {
    return kvantlar.map((q) => q * masshtab).toList();
  }
}

void main() {
  // Masalan: kvantlar [-1, 0, 1] va scale = 0.5
  var m = KvantlanganMassiv([-1, 0, 1, 1], 0.5);
  print('Dekvantlangan FP32: ${m.dekvantlash()}');
}
```

## Tushuntirish va Mantiq:
Kvantlangan massiv past darajadagi int qiymatlarni masshtab koeffitsiyenti orqali asl haqiqiy songa qaytaradi.

## Ishlash natijasi:
```text
Dekvantlangan FP32: [-0.5, 0.0, 0.5, 0.5]
```

# 600-Topshiriq: Amaliy: BitNet Ko'p O'lchamli Generik Tensor (Tensor<T extends num>)

## Topshiriq sharti:
Shakl (shape: rows, cols) va elementlarni saqlovchi, reshape va transpose qila oladigan generik Tensor tuzing.

## Yechim (Dart kodi):
```dart
class Tensor<T extends num> {
  final List<int> shape;
  final List<T> data;

  Tensor(this.shape, this.data) {
    int total = shape.reduce((a, b) => a * b);
    if (data.length != total) {
      throw ArgumentError('Ma\'lumotlar soni shakl ko\'paytmasiga teng bo\'lishi kerak');
    }
  }

  int get rows => shape[0];
  int get cols => shape[1];

  T get(int r, int c) => data[r * cols + c];

  Tensor<T> transpose() {
    List<T> yangiData = List<T>.filled(data.length, data[0]);
    for (int r = 0; r < rows; r++) {
      for (int c = 0; c < cols; c++) {
        yangiData[c * rows + r] = get(r, c);
      }
    }
    return Tensor<T>([cols, rows], yangiData);
  }

  void chop() {
    print('Tensor $shape:');
    for (int r = 0; r < rows; r++) {
      var satr = [for (int c = 0; c < cols; c++) get(r, c)];
      print('  $satr');
    }
  }
}

void main() {
  // 2x3 o'lchamli BitNet Ternar vazn tensori
  var w = Tensor<int>([2, 3], [1, 0, -1, -1, 1, 0]);
  w.chop();

  var wT = w.transpose();
  print('Transponirlangan:');
  wT.chop();
}
```

## Tushuntirish va Mantiq:
Ko'p o'lchamli generik Tensor sinfi neyron tarmoqlarning qatlamlari va matritsali amallarining poydevori hisoblanadi.

## Ishlash natijasi:
```text
Tensor [2, 3]:
  [1, 0, -1]
  [-1, 1, 0]
Transponirlangan:
Tensor [3, 2]:
  [1, -1]
  [0, 1]
  [-1, 0]
```

