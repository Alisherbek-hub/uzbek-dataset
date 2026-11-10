# 4-Qism: Funksiyalar, Parametrlar, Closures va Dart 3 Records (151-200)

Ushbu qismda Dart tilida funksiyalar e'lon qilish, arrow sintaksis (`=>`), pozitsion va nomlangan parametrlar, `required`, birinchi darajali funksiyalar, closure va yopilishlar, `typedef`, Dart 3 ko'p qiymat qaytaruvchi Records va rekursiya chuqur o'rganiladi.

# 151-Topshiriq: Standart funksiya e'lon qilish va chaqirish
## Topshiriq sharti:
Ikkita sonning yig'indisini hisoblovchi, aniq parametr turlari va qaytish turiga ega `int qosh(int a, int b)` funksiyasini yozing.

## Yechim (Dart kodi):
```dart
int qosh(int a, int b) {
  return a + b;
}

void main() {
  int natija = qosh(25, 40);
  print("Yig'indi: $natija");
}
```

## Tushuntirish va Mantiq:
Dart da har bir funksiya aniq qaytuvchi turga va parametr turlariga ega bo'lishi kodning xavfsiz va o'qilishi oson bo'lishini ta'minlaydi.

## Ishlash natijasi:
```text
Yig'indi: 65
```

# 152-Topshiriq: Qisqa funksiya sintaksisi: Arrow syntax (=>)
## Topshiriq sharti:
Bitta ifodadan iborat funksiyani strelka (`=>`) orqali ixcham yozing.

## Yechim (Dart kodi):
```dart
double kvadrat(double x) => x * x;
bool isEven(int n) => n % 2 == 0;

void main() {
  print("5.5 kvadrati: ${kvadrat(5.5)}");
  print("8 juftmi: ${isEven(8)}");
  print("7 juftmi: ${isEven(7)}");
}
```

## Tushuntirish va Mantiq:
`=> ifoda` sintaksisi `{ return ifoda; }` ning qisqartirilgan shaklidir.

## Ishlash natijasi:
```text
5.5 kvadrati: 30.25
8 juftmi: true
7 juftmi: false
```

# 153-Topshiriq: Ixtiyoriy pozitsion parametrlar: [int? yosh]
## Topshiriq sharti:
Kvadrat qavs `[...]` yordamida ikkinchi parametri ixtiyoriy bo'lgan salomlashish funksiyasini yozing.

## Yechim (Dart kodi):
```dart
void salom(String ism, [String? familiya]) {
  if (familiya != null) {
    print("Assalomu alaykum, $ism $familiya!");
  } else {
    print("Salom, $ism!");
  }
}

void main() {
  salom("Alisher", "Navoiy");
  salom("Bobur");
}
```

## Tushuntirish va Mantiq:
Kvadrat qavs ichidagi parametrlar tartib bo'yicha uzatiladi va agar uzatilmasa `null` qiymatga ega bo'ladi.

## Ishlash natijasi:
```text
Assalomu alaykum, Alisher Navoiy!
Salom, Bobur!
```

# 154-Topshiriq: Ixtiyoriy parametrlarga standart qiymat berish: [int yosh = 18]
## Topshiriq sharti:
Ixtiyoriy parametr berilmaganda ishlatiladigan sukut bo'yicha qiymatni belgilang.

## Yechim (Dart kodi):
```dart
void roldanOtkaz(String ism, [int yosh = 18]) {
  print("Foydalanuvchi: $ism, Yoshi: $yosh");
}

void main() {
  roldanOtkaz("Ali"); // Standart 18 olinadi
  roldanOtkaz("Vali", 25);
}
```

## Tushuntirish va Mantiq:
Standart qiymat berilganda parametr non-nullable bo'lib qoladi va null tekshiruvga ehtiyoj qolmaydi.

## Ishlash natijasi:
```text
Foydalanuvchi: Ali, Yoshi: 18
Foydalanuvchi: Vali, Yoshi: 25
```

# 155-Topshiriq: Nomlangan parametrlar: {String? ism}
## Topshiriq sharti:
Qavslar `{...}` ichida nomlangan parametrlar e'lon qiling va ularni ixtiyoriy tartibda chaqiring.

## Yechim (Dart kodi):
```dart
void mahsulotChopEt({String? nom, double? narx}) {
  print("Mahsulot: ${nom ?? 'Noma'lum'}, Narxi: ${narx ?? 0.0} so'm");
}

void main() {
  mahsulotChopEt(nom: "Kitob", narx: 45000);
  mahsulotChopEt(narx: 12000, nom: "Daftar"); // Tartibi muhim emas!
  mahsulotChopEt(nom: "Ruchka");
}
```

## Tushuntirish va Mantiq:
Nomlangan parametrlar Flutter vidjetlarida eng asosiy qurilish g'ishti bo'lib, argumentlarni aniq nom bilan chaqirish imkonini beradi.

## Ishlash natijasi:
```text
Mahsulot: Kitob, Narxi: 45000.0 so'm
Mahsulot: Daftar, Narxi: 12000.0 so'm
Mahsulot: Ruchka, Narxi: 0.0 so'm
```

# 156-Topshiriq: Majburiy nomlangan parametrlar: required
## Topshiriq sharti:
`required` kalit so'zi orqali nomlangan parametrning kiritilishi shart ekanligini ta'minlang.

## Yechim (Dart kodi):
```dart
void royxatdanOt({required String email, required String parol, String? nickname}) {
  print("Ro'yxatdan o'tdi: $email, Nickname: ${nickname ?? 'kiritilmagan'}");
}

void main() {
  royxatdanOt(email: "ali@uzbek.ai", parol: "secret123");
  royxatdanOt(email: "vali@uzbek.ai", parol: "pass456", nickname: "valijon");
}
```

## Tushuntirish va Mantiq:
`required` berilgan parametr kompilyator tomonidan qat'iy tekshiriladi va chaqiruvda tushirib qoldirilsa dastur kompilyatsiya bo'lmaydi.

## Ishlash natijasi:
```text
Ro'yxatdan o'tdi: ali@uzbek.ai, Nickname: kiritilmagan
Ro'yxatdan o'tdi: vali@uzbek.ai, Nickname: valijon
```

# 157-Topshiriq: Nomlangan parametrlarga standart qiymat berish
## Topshiriq sharti:
Serverga ulanish parametrlarini (`host = 'localhost'`, `port = 8080`) standart qiymatlar bilan yarating.

## Yechim (Dart kodi):
```dart
void serverniIshgaTushir({String host = "localhost", int port = 8080}) {
  print("Server ulandi: http://$host:$port");
}

void main() {
  serverniIshgaTushir(); // Standart parametrlar bilan
  serverniIshgaTushir(port: 9000);
  serverniIshgaTushir(host: "api.uzbek.ai", port: 443);
}
```

## Tushuntirish va Mantiq:
Standart qiymatlar API dizaynida ko'p uchraydigan holatlarni sukut bo'yicha yengillashtiradi.

## Ishlash natijasi:
```text
Server ulandi: http://localhost:8080
Server ulandi: http://localhost:9000
Server ulandi: http://api.uzbek.ai:443
```

# 158-Topshiriq: Pozitsion va Nomlangan parametrlarni aralashtirish
## Topshiriq sharti:
Birinchi parametri majburiy pozitsion, keyingilari esa nomlangan parametrlar bo'lgan funksiya yozing.

## Yechim (Dart kodi):
```dart
void xabarYubor(String matn, {required String qabulQiluvchi, bool shoshilinch = false}) {
  String status = shoshilinch ? "[MUHIM!]" : "[Oddiy]";
  print("$status '$matn' -> $qabulQiluvchi ga yuborildi.");
}

void main() {
  xabarYubor("Hisobot tayyor", qabulQiluvchi: "Boshqaruvchi");
  xabarYubor("Serverda uzilish!", qabulQiluvchi: "Admin", shoshilinch: true);
}
```

## Tushuntirish va Mantiq:
Asosiy ob'ekt (matn) pozitsion, qo'shimcha konfiguratsiyalar esa nomlangan tarzda berilishi juda toza API uslubidir.

## Ishlash natijasi:
```text
[Oddiy] 'Hisobot tayyor' -> Boshqaruvchi ga yuborildi.
[MUHIM!] 'Serverda uzilish!' -> Admin ga yuborildi.
```

# 159-Topshiriq: Birinchi darajali funksiyalar (First-class functions)
## Topshiriq sharti:
Funksiyani oddiy o'zgaruvchiga qiymat sifatida yuklash va o'sha o'zgaruvchi orqali chaqirishni ko'rsating.

## Yechim (Dart kodi):
```dart
int ikkiKarra(int x) => x * 2;
int uchKarra(int x) => x * 3;

void main() {
  // Funksiyani o'zgaruvchiga yuklaymiz
  int Function(int) meningAmalim = ikkiKarra;
  print("Natija 1: ${meningAmalim(10)}");

  meningAmalim = uchKarra;
  print("Natija 2: ${meningAmalim(10)}");
}
```

## Tushuntirish va Mantiq:
Dart da funksiyalar birinchi darajali ob'ektlardir: ularni o'zgaruvchilarga yuklash, ro'yxatlarda saqlash va argument sifatida uzatish mumkin.

## Ishlash natijasi:
```text
Natija 1: 20
Natija 2: 30
```

# 160-Topshiriq: Funksiyani argument sifatida uzatish (Callback pattern)
## Topshiriq sharti:
Hisoblash amalini argument sifatida qabul qiluvchi `hisobla(int a, int b, int Function(int, int) amal)` funksiyasini yozing.

## Yechim (Dart kodi):
```dart
int hisobla(int a, int b, int Function(int, int) amal) {
  return amal(a, b);
}

void main() {
  int r1 = hisobla(20, 5, (x, y) => x + y);
  int r2 = hisobla(20, 5, (x, y) => x * y);
  int r3 = hisobla(20, 5, (x, y) => x - y);

  print("Qo'shish: $r1");
  print("Ko'paytirish: $r2");
  print("Ayirish: $r3");
}
```

## Tushuntirish va Mantiq:
Funksiyani argument sifatida qabul qiluvchi funksiyalar Higher-Order Functions (yuqori darajali funksiyalar) deb ataladi.

## Ishlash natijasi:
```text
Qo'shish: 25
Ko'paytirish: 100
Ayirish: 15
```

# 161-Topshiriq: Funksiyadan yangi funksiya qaytarish (Function Factory)
## Topshiriq sharti:
Belgilangan ko'paytiruvchi koeffitsiyentga ega yangi funksiya ishlab chiqaruvchi `makeMultiplier(int factor)` funksiyasini yozing.

## Yechim (Dart kodi):
```dart
int Function(int) makeMultiplier(int factor) {
  return (int x) => x * factor;
}

void main() {
  var doubleIt = makeMultiplier(2);
  var tripleIt = makeMultiplier(3);

  print("doubleIt(15): ${doubleIt(15)}");
  print("tripleIt(15): ${tripleIt(15)}");
}
```

## Tushuntirish va Mantiq:
Ichki anonim funksiya tashqi `factor` o'zgaruvchisini eslab qoladi va moslashtirilgan yangi funksiya hosil qiladi.

## Ishlash natijasi:
```text
doubleIt(15): 30
tripleIt(15): 45
```

# 162-Topshiriq: Yopilish (Closure) tushunchasi va xotira holati
## Topshiriq sharti:
Tashqi o'zgaruvchi qiymatini har bir chaqiruvda 1 ga oshirib boruvchi yopilish (Closure Counter) dasturini yozing.

## Yechim (Dart kodi):
```dart
int Function() makeCounter() {
  int hisob = 0;
  return () {
    hisob++;
    return hisob;
  };
}

void main() {
  var c1 = makeCounter();
  var c2 = makeCounter();

  print("c1: ${c1()}");
  print("c1: ${c1()}");
  print("c1: ${c1()}");

  print("c2: ${c2()}"); // c2 alohida mustaqil xotiraga ega!
}
```

## Tushuntirish va Mantiq:
Closure o'zi yaratilgan leksik doiradagi (lexical scope) o'zgaruvchilarni xotirada qamrab oladi va ular dastur tugaguncha saqlanadi.

## Ishlash natijasi:
```text
c1: 1
c1: 2
c1: 3
c2: 1
```

# 163-Topshiriq: typedef orqali funksiya turlariga nom berish
## Topshiriq sharti:
`typedef MatematikAmal = int Function(int, int);` yordamida funksiya turini nomlang va kodni toza qiling.

## Yechim (Dart kodi):
```dart
typedef MatematikAmal = int Function(int, int);

int bajar(int a, int b, MatematikAmal amal) {
  return amal(a, b);
}

void main() {
  MatematikAmal darajaAmali = (x, y) {
    int res = 1;
    for (int i = 0; i < y; ++i) res *= x;
    return res;
  };

  print("2^5 = ${bajar(2, 5, darajaAmali)}");
}
```

## Tushuntirish va Mantiq:
`typedef` murakkab funksiya imzolashlarini o'qilishi oson va qayta ishlatiladigan qisqa nomga aylantiradi.

## Ishlash natijasi:
```text
2^5 = 32
```

# 164-Topshiriq: Generik funksiyalar: <T> parametri bilan
## Topshiriq sharti:
Har qanday turdagi ro'yxatning birinchi elementini xavfsiz qaytaruvchi generik `T? getFirst<T>(List<T> list)` funksiyasini yozing.

## Yechim (Dart kodi):
```dart
T? getFirst<T>(List<T> list) {
  return list.isNotEmpty ? list.first : null;
}

void main() {
  List<int> sonlar = [10, 20, 30];
  List<String> sozlari = ["Salom", "Dunyo"];
  List<double> bosh = [];

  print("Birinchi son: ${getFirst(sonlar)}");
  print("Birinchi so'z: ${getFirst(sozlari)}");
  print("Bo'sh ro'yxat: ${getFirst(bosh)}");
}
```

## Tushuntirish va Mantiq:
Generik funksiya tur xavfsizligini ta'minlagan holda kodni istalgan ma'lumot turlari uchun universallashtiradi.

## Ishlash natijasi:
```text
Birinchi son: 10
Birinchi so'z: Salom
Bo'sh ro'yxat: null
```

# 165-Topshiriq: Generik turga cheklov qo'yish: <T extends num>
## Topshiriq sharti:
Faqat sonli turlar (`int` va `double`) bilan ishlovchi generik funksiya yarating.

## Yechim (Dart kodi):
```dart
T engKattasi<T extends num>(T a, T b) {
  return a > b ? a : b;
}

void main() {
  print("Kattasi (int):    ${engKattasi(15, 42)}");
  print("Kattasi (double): ${engKattasi(3.14, 2.71)}");
}
```

## Tushuntirish va Mantiq:
`<T extends num>` cheklovi `>` solishtirish operatorining mavjudligini kafolatlaydi va `String` kabi nomuvofiq turlar uzatilishini taqiqlaydi.

## Ishlash natijasi:
```text
Kattasi (int):    42
Kattasi (double): 3.14
```

# 166-Topshiriq: Rekursiv funksiya: Faktorial hisoblash
## Topshiriq sharti:
`n * faktorial(n - 1)` rekursiv formulasi bilan faktorialni hisoblang.

## Yechim (Dart kodi):
```dart
int fact(int n) {
  if (n <= 1) return 1;
  return n * fact(n - 1);
}

void main() {
  print("5! = ${fact(5)}");
  print("7! = ${fact(7)}");
}
```

## Tushuntirish va Mantiq:
Rekursiyada to'xtash sharti (`n <= 1`) bo'lishi shart, aks holda dastur cheksiz rekursiyaga tushib xotira xatosi beradi.

## Ishlash natijasi:
```text
5! = 120
7! = 5040
```

# 167-Topshiriq: Rekursiv funksiya: Tezkor darajaga ko'tarish (O(log N))
## Topshiriq sharti:
Oddiy O(N) sikl o'rniga binar bo'linish `power(x, n/2)` orqali $O(\log N)$ da darajani hisoblang.

## Yechim (Dart kodi):
```dart
double fastPower(double x, int n) {
  if (n == 0) return 1.0;
  if (n % 2 == 0) {
    double yarmi = fastPower(x, n ~/ 2);
    return yarmi * yarmi;
  } else {
    return x * fastPower(x, n - 1);
  }
}

void main() {
  print("2.0^10 = ${fastPower(2.0, 10)}");
  print("3.0^5  = ${fastPower(3.0, 5)}");
}
```

## Tushuntirish va Mantiq:
Binar darajalash har qadamda darajani 2 ga bo'lib boradi, 1000-darajani atigi 10 ta qadamda hisoblaydi.

## Ishlash natijasi:
```text
2.0^10 = 1024.0
3.0^5  = 243.0
```

# 168-Topshiriq: Rekursiya yordamida satrni teskari o'girish
## Topshiriq sharti:
Satrni rekursiv ravishda oxirgi belgisini boshiga qo'yib teskari o'giring.

## Yechim (Dart kodi):
```dart
String reverseRecursive(String s) {
  if (s.isEmpty) return "";
  return reverseRecursive(s.substring(1)) + s[0];
}

void main() {
  print(reverseRecursive("salom"));
  print(reverseRecursive("Flutter"));
}
```

## Tushuntirish va Mantiq:
Rekursiya har bir qadamda satrning birinchi belgisini ajratib oladi va qolgan qismi teskari qilingach oxiriga ulaydi.

## Ishlash natijasi:
```text
molas
rettulF
```

# 169-Topshiriq: Dart 3 Records: Funksiyadan bir nechta qiymat qaytarish
## Topshiriq sharti:
Funksiyadan bir vaqtning o'zida ham minimal, ham maksimal sonni Dart 3 ning `(int, int)` rekordi orqali qaytaring.

## Yechim (Dart kodi):
```dart
(int, int) minMax(List<int> list) {
  int minVal = list[0];
  int maxVal = list[0];

  for (int x in list) {
    if (x < minVal) minVal = x;
    if (x > maxVal) maxVal = x;
  }
  return (minVal, maxVal);
}

void main() {
  var sonlar = [45, 12, 89, 7, 99, 23];

  // Rekordni qabul qilib olamiz
  var (minVal, maxVal) = minMax(sonlar);

  print("Min: $minVal, Max: $maxVal");
}
```

## Tushuntirish va Mantiq:
Dart 3 Records qo'shimcha maxsus klass yaratmasdan bir nechta har xil qiymatlarni bitta ixcham kortej (tuple) sifatida qaytarish imkonini beradi.

## Ishlash natijasi:
```text
Min: 7, Max: 99
```

# 170-Topshiriq: Dart 3 Nomlangan maydonli Records qaytarish
## Topshiriq sharti:
Records da maydonlarga nom berib (`({double x, double y})`) koordinata qaytaruvchi funksiya yozing.

## Yechim (Dart kodi):
```dart
({double x, double y}) markazNuqta(double x1, double y1, double x2, double y2) {
  return (x: (x1 + x2) / 2, y: (y1 + y2) / 2);
}

void main() {
  var markaz = markazNuqta(0, 0, 10, 20);
  print("Markaz koordinatalari: X = ${markaz.x}, Y = ${markaz.y}");
}
```

## Tushuntirish va Mantiq:
Nomlangan maydonli rekordlar kodni tushunarli qiladi va qaytgan qiymatlarga `.x` yoki `.y` kabi to'g'ridan-to'g'ri murojaat qilish imkonini beradi.

## Ishlash natijasi:
```text
Markaz koordinatalari: X = 5.0, Y = 10.0
```

# 171-Topshiriq: Funksiyada void va Null qaytarish farqi
## Topshiriq sharti:
`void` qaytaruvchi funksiya bilan `Null` qaytaruvchi funksiya farqini ko'rsating.

## Yechim (Dart kodi):
```dart
void chopEt(String s) {
  print(s);
  // Hech qanday qiymat qaytarmaydi
}

Null qaytarNull() {
  print("Null qaytmoqda");
  return null; // Aniq null qaytarishi shart!
}

void main() {
  chopEt("Salom");
  Null n = qaytarNull();
  print("Olingan n: $n");
}
```

## Tushuntirish va Mantiq:
`void` qiymat yo'qligini bildiradi va uning natijasini o'zgaruvchiga olib bo'lmaydi. `Null` esa alohida tur bo'lib, uning yagona qiymati `null` dir.

## Ishlash natijasi:
```text
Salom
Null qaytmoqda
Olingan n: null
```

# 172-Topshiriq: Higher-Order Functions: O'z map funksiyamizni yozish
## Topshiriq sharti:
Standart `.map()` metodidan foydalanmasdan, ro'yxat elementlarini o'zgartiruvchi `myMap` funksiyasini yozing.

## Yechim (Dart kodi):
```dart
List<R> myMap<T, R>(List<T> list, R Function(T) transform) {
  List<R> res = [];
  for (T item in list) {
    res.add(transform(item));
  }
  return res;
}

void main() {
  List<int> sonlar = [1, 2, 3, 4];
  List<String> satrlar = myMap(sonlar, (x) => "Son: $x");

  print(satrlar);
}
```

## Tushuntirish va Mantiq:
Ushbu mashq funksional dasturlash va umumiy transformatsiyalarning ichki ishlash mexanizmini to'liq tushuntiradi.

## Ishlash natijasi:
```text
[Son: 1, Son: 2, Son: 3, Son: 4]
```

# 173-Topshiriq: Higher-Order Functions: O'z filter funksiyamizni yozish
## Topshiriq sharti:
Standart `.where()` o'rniga shartga mos elementlarni saralovchi `myFilter` funksiyasini yozing.

## Yechim (Dart kodi):
```dart
List<T> myFilter<T>(List<T> list, bool Function(T) predicate) {
  List<T> res = [];
  for (T item in list) {
    if (predicate(item)) {
      res.add(item);
    }
  }
  return res;
}

void main() {
  List<int> sonlar = [10, 15, 20, 25, 30];
  List<int> juftlar = myFilter(sonlar, (x) => x % 2 == 0);

  print("Faqat juft sonlar: $juftlar");
}
```

## Tushuntirish va Mantiq:
`predicate` funksiyasi har bir element uchun `bool` qiymat qaytaradi va faqat `true` bo'lganlari olinadi.

## Ishlash natijasi:
```text
Faqat juft sonlar: [10, 20, 30]
```

# 174-Topshiriq: Funksiyalar kompozitsiyasi (Function Composition: f(g(x)))
## Topshiriq sharti:
Ikkita mustaqil funksiyani bitta yangi zanjirli funksiyaga birlashtiruvchi `compose` funksiyasini yozing.

## Yechim (Dart kodi):
```dart
R Function(T) compose<T, U, R>(R Function(U) f, U Function(T) g) {
  return (T x) => f(g(x));
}

void main() {
  int qoshBeshta(int x) => x + 5;
  int kvadrat(int x) => x * x;

  // avval 5 qo'shadi, keyin kvadratga ko'taradi: (x + 5)^2
  var hisobla = compose(kvadrat, qoshBeshta);

  print("hisobla(3) = (3 + 5)^2 = ${hisobla(3)}");
}
```

## Tushuntirish va Mantiq:
Funksiyalar kompozitsiyasi murakkab algoritmlarni kichik, mustaqil va qayta ishlatiluvchi funksiyalardan yig'ish imkonini beradi.

## Ishlash natijasi:
```text
hisobla(3) = (3 + 5)^2 = 64
```

# 175-Topshiriq: Vaqtni o'lchovchi Benchmark funksiyasi: measureTime()
## Topshiriq sharti:
Ixtiyoriy funksiyaning bajarilish vaqtini mikrosekundlarda o'lchovchi yordamchi funksiya yozing.

## Yechim (Dart kodi):
```dart
void measureTime(String nom, void Function() fn) {
  Stopwatch sw = Stopwatch()..start();
  fn();
  sw.stop();
  print("[$nom] Bajarilish vaqti: ${sw.elapsedMicroseconds} mks");
}

void main() {
  measureTime("1 milliongacha yig'indi", () {
    int sum = 0;
    for (int i = 0; i < 1000000; ++i) sum += i;
  });
}
```

## Tushuntirish va Mantiq:
`Stopwatch` sinfi Dart da eng aniq vaqt o'lchash qurilmasi bo'lib, unumdorlik sinovlari uchun standart hisoblanadi.

## Ishlash natijasi:
```text
[1 milliongacha yig'indi] Bajarilish vaqti: 1200 mks
```

# 176-Topshiriq: Higher-Order Functions: O'z reduce funksiyamizni yozish
## Topshiriq sharti:
Ro'yxatning barcha elementlarini bitta qiymatga yig'uvchi (masalan yig'indi yoki ko'paytma) `myReduce` funksiyasini noldan yozing.

## Yechim (Dart kodi):
```dart
T myReduce<T>(List<T> list, T Function(T acc, T element) combine) {
  if (list.isEmpty) throw StateError("Bo'sh ro'yxatni reduce qilib bo'lmaydi!");
  T acc = list[0];
  for (int i = 1; i < list.length; ++i) {
    acc = combine(acc, list[i]);
  }
  return acc;
}

void main() {
  List<int> sonlar = [1, 2, 3, 4, 5];
  int yigindi = myReduce(sonlar, (a, b) => a + b);
  int kopaytma = myReduce(sonlar, (a, b) => a * b);

  print("Yig'indi: $yigindi");
  print("Ko'paytma: $kopaytma");
}
```

## Tushuntirish va Mantiq:
`reduce` ro'yxatning birinchi elementini dastlabki akkumulyator sifatida olib, qolgan elementlar bilan ketma-ket birlashtiradi.

## Ishlash natijasi:
```text
Yig'indi: 15
Ko'paytma: 120
```

# 177-Topshiriq: Currying texnikasi: Ko'p parametrli funksiyani zanjirga ajratish
## Topshiriq sharti:
`f(a, b, c)` ni `f(a)(b)(c)` shaklida chaqiriladigan zanjirli bir parametrli funksiyalarga ajrating.

## Yechim (Dart kodi):
```dart
int Function(int) Function(int) qoshishZanjiri(int a) {
  return (int b) {
    return (int c) {
      return a + b + c;
    };
  };
}

void main() {
  // Bosqichma-bosqich parametr berish
  var qoshBeshta = qoshishZanjiri(5);
  var qoshBeshtaVaO'nta = qoshBeshta(10);

  int natija = qoshBeshtaVaO'nta(20);
  print("5 + 10 + 20 = $natija");

  // Bitta qatorda chaqirish
  print("1 + 2 + 3 = ${qoshishZanjiri(1)(2)(3)}");
}
```

## Tushuntirish va Mantiq:
Currying funksiyalarga parametrlarni bo'lib-bo'lib uzatish (qisman bajarish) imkonini beradi va funksional arxitekturada muhim o'rin tutadi.

## Ishlash natijasi:
```text
5 + 10 + 20 = 35
1 + 2 + 3 = 6
```

# 178-Topshiriq: Memoizatsiya (Keshlash) dekoratori yozish
## Topshiriq sharti:
Qimmat hisoblash natijalarini parametrlar bo'yicha Map da eslab qoluvchi `memoize` yordamchi funksiyasini yarating.

## Yechim (Dart kodi):
```dart
R Function(T) memoize<T, R>(R Function(T) fn) {
  final kesh = <T, R>{};
  return (T arg) {
    if (kesh.containsKey(arg)) {
      return kesh[arg]!;
    }
    final res = fn(arg);
    kesh[arg] = res;
    return res;
  };
}

void main() {
  int ogirAmal(int n) {
    print("[Hisoblash]: $n uchun bajarilmoqda...");
    return n * n;
  }

  var tezkorAmal = memoize(ogirAmal);

  print("1-chaqiruv: ${tezkorAmal(5)}");
  print("2-chaqiruv: ${tezkorAmal(5)}"); // Keshdan olinadi!
  print("3-chaqiruv: ${tezkorAmal(8)}");
}
```

## Tushuntirish va Mantiq:
Memoizatsiya orqali bir xil kiruvchi parametrlar uchun funksiya takroran hisoblanmaydi, balki keshdan darhol O(1) da qaytariladi.

## Ishlash natijasi:
```text
[Hisoblash]: 5 uchun bajarilmoqda...
1-chaqiruv: 25
2-chaqiruv: 25
[Hisoblash]: 8 uchun bajarilmoqda...
3-chaqiruv: 64
```

# 179-Topshiriq: Sinxron Generator funksiyalar: sync* va yield
## Topshiriq sharti:
`sync*` kalit so'zi va `yield` orqali dangasa (lazy) tartibda ketma-ket sonlarni qaytaruvchi `Iterable<int>` generatorini yozing.

## Yechim (Dart kodi):
```dart
Iterable<int> toqSonlar(int max) sync* {
  for (int i = 1; i <= max; i += 2) {
    yield i; // Navbatdagi elementni chiqaradi
  }
}

void main() {
  var generator = toqSonlar(7);

  print("Generator yaratildi, lekin hali aylanmadi.");
  for (int son in generator) {
    print("Olingan toq son: $son");
  }
}
```

## Tushuntirish va Mantiq:
`sync*` funksiyasi barcha elementlarni bir vaqtda xotiraga yuklamaydi, balki iste'molchi so'raganda `yield` orqali bittalab uzatadi.

## Ishlash natijasi:
```text
Generator yaratildi, lekin hali aylanmadi.
Olingan toq son: 1
Olingan toq son: 3
Olingan toq son: 5
Olingan toq son: 7
```

# 180-Topshiriq: yield* orqali boshqa kolleksiyalarni uzatish
## Topshiriq sharti:
`yield*` yordamida boshqa `Iterable` yoki generatorning barcha elementlarini o'z ichiga oluvchi generator yozing.

## Yechim (Dart kodi):
```dart
Iterable<int> oraliq(int start, int end) sync* {
  for (int i = start; i <= end; ++i) yield i;
}

Iterable<int> birlashganGenerator() sync* {
  yield 0;
  yield* oraliq(1, 3); // 1, 2, 3 ni ketma-ket chiqaradi
  yield 99;
}

void main() {
  print("Birlashgan generator natijasi: ${birlashganGenerator().toList()}");
}
```

## Tushuntirish va Mantiq:
`yield*` butun bir oraliqni delegatsiya qiladi va sikl ichida har birini qo'lda `yield` qilish zaruratini yo'qotadi.

## Ishlash natijasi:
```text
Birlashgan generator natijasi: [0, 1, 2, 3, 99]
```

# 181-Topshiriq: Fibonacci sonlarini sync* generatori bilan chiqarish
## Topshiriq sharti:
N ta Fibonachchi sonini dangasa (lazy) generatsiya qiluvchi funksiya yozing.

## Yechim (Dart kodi):
```dart
Iterable<int> fibonacciGenerator(int n) sync* {
  int a = 0, b = 1;
  for (int i = 0; i < n; ++i) {
    yield a;
    int next = a + b;
    a = b;
    b = next;
  }
}

void main() {
  print("Dastlabki 6 ta Fibonachchi:");
  for (int f in fibonacciGenerator(6)) {
    print(f);
  }
}
```

## Tushuntirish va Mantiq:
Generatorlar katta hajmdagi ketma-ketliklarni yaratishda xotirani tejashning eng qulay usulidir.

## Ishlash natijasi:
```text
Dastlabki 6 ta Fibonachchi:
0
1
1
2
3
5
```

# 182-Topshiriq: Funksiya parametrlarida Destructuring (Dart 3)
## Topshiriq sharti:
Dart 3 ning Record va List destrukturizatsiyasini to'g'ridan-to'g'ri funksiya parametrida qo'llang.

## Yechim (Dart kodi):
```dart
void nuqtaniChopEt((double x, double y) nuqta) {
  var (x, y) = nuqta;
  print("Nuqta koordinatalari: x=$x, y=$y");
}

void main() {
  nuqtaniChopEt((12.5, 40.0));
}
```

## Tushuntirish va Mantiq:
Dart 3 parametrlarni qabul qilish paytidayoq ularni alohida o'zgaruvchilarga ajratish imkoniyatini beradi.

## Ishlash natijasi:
```text
Nuqta koordinatalari: x=12.5, y=40.0
```

# 183-Topshiriq: Funksiya ichida ichki lokal funksiya (Nested function)
## Topshiriq sharti:
Tashqi koddan yashirin bo'lgan, faqat o'sha funksiya doirasida yordamchi vazifani bajaruvchi ichki funksiya yozing.

## Yechim (Dart kodi):
```dart
int faktorialYigindisi(List<int> sonlar) {
  // Ichki yordamchi funksiya
  int fact(int n) {
    int res = 1;
    for (int i = 2; i <= n; ++i) res *= i;
    return res;
  }

  int jami = 0;
  for (int s in sonlar) {
    jami += fact(s);
  }
  return jami;
}

void main() {
  List<int> royxat = [1, 2, 3]; // 1! + 2! + 3! = 1 + 2 + 6 = 9
  print("Faktoriallar yig'indisi: ${faktorialYigindisi(royxat)}");
}
```

## Tushuntirish va Mantiq:
Ichki funksiyalar kodni modullashtiradi va tashqi global maydonni ifloslantirmaydi.

## Ishlash natijasi:
```text
Faktoriallar yig'indisi: 9
```

# 184-Topshiriq: Sof funksiyalar (Pure Functions) va Nojo'ya ta'sirlardan qochish
## Topshiriq sharti:
Tashqi o'zgaruvchilarga ta'sir qilmaydigan, faqat kiritilgan parametrlarga tayanuvchi sof funksiyani yozing.

## Yechim (Dart kodi):
```dart
// Sof funksiya: berilgan ro'yxatni o'zgartirmaydi, yangi nusxa qaytaradi
List<int> sortPure(List<int> original) {
  List<int> copy = List.from(original);
  copy.sort();
  return copy;
}

void main() {
  List<int> asl = [5, 2, 8, 1];
  List<int> saralangan = sortPure(asl);

  print("Asl ro'yxat o'zgarmadi: $asl");
  print("Yangi saralangan:       $saralangan");
}
```

## Tushuntirish va Mantiq:
Sof funksiyalar testlash uchun o'ta oson va ko'p oqimli yoki reaktiv dasturlashda xatolar kelib chiqishining oldini oladi.

## Ishlash natijasi:
```text
Asl ro'yxat o'zgarmadi: [5, 2, 8, 1]
Yangi saralangan:       [1, 2, 5, 8]
```

# 185-Topshiriq: Argumentlar validatsiyasi va xatolik tashlash (ArgumentError)
## Topshiriq sharti:
Parametrlar shartga mos kelmasa `ArgumentError.value()` orqali aniq xabar beruvchi funksiya yozing.

## Yechim (Dart kodi):
```dart
double bo'lish(double a, double b) {
  if (b == 0.0) {
    throw ArgumentError.value(b, "b", "Nolga bo'lish mumkin emas!");
  }
  return a / b;
}

void main() {
  print("10 / 2 = ${bo'lish(10, 2)}");

  try {
    bo'lish(10, 0);
  } catch (e) {
    print("Ushlangan xatolik: $e");
  }
}
```

## Tushuntirish va Mantiq:
Kiritilgan qiymatlarni darhol tekshirish 'fail-fast' tamoyiliga mos bo'lib, xatolarni erta bosqichda to'xtatadi.

## Ishlash natijasi:
```text
10 / 2 = 5.0
Ushlangan xatolik: Invalid argument (b): Nolga bo'lish mumkin emas!: 0.0
```

# 186-Topshiriq: Funksiya natijasini Result klassi bilan qaytarish (Success / Failure)
## Topshiriq sharti:
Istisnolardan (Exception) qochish uchun natijani muvaffaqiyat yoki xatolik shaklida ifodalovchi funksional `Result` modelini yarating.

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

Result<int> kvadratIldiz(int n) {
  if (n < 0) return Failure("Manfiy sonning haqiqiy ildizi yo'q!");
  for (int i = 0; i * i <= n; ++i) {
    if (i * i == n) return Success(i);
  }
  return Failure("Aniq butun ildiz mavjud emas!");
}

void main() {
  var r1 = kvadratIldiz(49);
  var r2 = kvadratIldiz(-4);

  switch (r1) {
    case Success(data: var v): print("Ildiz: $v");
    case Failure(error: var e): print("Xato: $e");
  }

  switch (r2) {
    case Success(data: var v): print("Ildiz: $v");
    case Failure(error: var e): print("Xato: $e");
  }
}
```

## Tushuntirish va Mantiq:
`Result` naqshi zamonaviy dasturlashda xatolarni kutilgan holat sifatida boshqarishning eng qulay usulidir.

## Ishlash natijasi:
```text
Ildiz: 7
Xato: Manfiy sonning haqiqiy ildizi yo'q!
```

# 187-Topshiriq: Qisman bajariluvchi funksiyalar (Partial Application)
## Topshiriq sharti:
Birinchi parametri oldindan belgilangan funksiyani qaytaruvchi yordamchi kod yozing.

## Yechim (Dart kodi):
```dart
double Function(double) chegirmaHisoblagich(double foiz) {
  return (double narx) => narx * (1 - foiz / 100);
}

void main() {
  var qoraJuma = chegirmaHisoblagich(30.0); // 30% chegirma
  var talaba = chegirmaHisoblagich(15.0);   // 15% chegirma

  print("100 000 so'mlik mahsulot (30% chegirma): ${qoraJuma(100000)} so'm");
  print("100 000 so'mlik mahsulot (15% chegirma): ${talaba(100000)} so'm");
}
```

## Tushuntirish va Mantiq:
Partial application umumiy funksiyalardan maxsus maqsadli yangi funksiyalar yasashga xizmat qiladi.

## Ishlash natijasi:
```text
100 000 so'mlik mahsulot (30% chegirma): 70000.0 so'm
100 000 so'mlik mahsulot (15% chegirma): 85000.0 so'm
```

# 188-Topshiriq: Funksional quvur (Pipeline) zanjiri
## Topshiriq sharti:
Matnni ketma-ket tozalovchi va formatlovchi funksiyalar zanjirini yarating.

## Yechim (Dart kodi):
```dart
String tozalash(String s) => s.trim();
String kichikHarf(String s) => s.toLowerCase();
String chiziqchaAlmash(String s) => s.replaceAll(" ", "-");

String pipeline(String input, List<String Function(String)> bosqichlar) {
  String natija = input;
  for (var bosqich in bosqichlar) {
    natija = bosqich(natija);
  }
  return natija;
}

void main() {
  String xomMatn = "   O'zbekiston Sun'iy Intellekti   ";
  String slug = pipeline(xomMatn, [tozalash, kichikHarf, chiziqchaAlmash]);

  print("Natijaviy URL slug: $slug");
}
```

## Tushuntirish va Mantiq:
Quvur (Pipeline) arxitekturasi ma'lumotlarni bosqichma-bosqich o'zgartirishni juda o'qilishi oson qiladi.

## Ishlash natijasi:
```text
Natijaviy URL slug: o'zbekiston-sun'iy-intellekti
```

# 189-Topshiriq: Matematik ifodalarni baholovchi funksional kalkulyator
## Topshiriq sharti:
Operatorlar xaritasi (`Map<String, double Function(double, double)>`) orqali moslashuvchan kalkulyator tuzing.

## Yechim (Dart kodi):
```dart
class Kalkulyator {
  final Map<String, double Function(double, double)> _amallar = {
    "+": (a, b) => a + b,
    "-": (a, b) => a - b,
    "*": (a, b) => a * b,
    "/": (a, b) => a / b,
  };

  void yangiAmalQosh(String belgi, double Function(double, double) amal) {
    _amallar[belgi] = amal;
  }

  double hisobla(double a, String op, double b) {
    if (!_amallar.containsKey(op)) throw UnsupportedError("Noma'lum amal: $op");
    return _amallar[op]!(a, b);
  }
}

void main() {
  var calc = Kalkulyator();

  print("12 + 8 = ${calc.hisobla(12, "+", 8)}");
  print("12 * 8 = ${calc.hisobla(12, "*", 8)}");

  // Yangi daraja amali qo'shamiz
  calc.yangiAmalQosh("^", (a, b) {
    double res = 1;
    for (int i = 0; i < b.toInt(); ++i) res *= a;
    return res;
  });

  print("2 ^ 5 = ${calc.hisobla(2, "^", 5)}");
}
```

## Tushuntirish va Mantiq:
Funksiyalar xaritasi orqali dasturga `if-else` larni o'zgartirmasdan yangi operatsiyalar qo'shish (Open-Closed Principle) mumkin.

## Ishlash natijasi:
```text
12 + 8 = 20.0
12 * 8 = 96.0
2 ^ 5 = 32.0
```

# 190-Topshiriq: Kaskad operatori (..) bilan ob'ektlarni sozlash
## Topshiriq sharti:
Kaskad `..` operatori orqali bitta ob'ekt ustida ketma-ket bir nechta metodlarni chaqiring.

## Yechim (Dart kodi):
```dart
class MatnBufer {
  String _qiymat = "";
  void qosh(String s) => _qiymat += s;
  void tozalash() => _qiymat = "";
  void chopEt() => print("Matn: $_qiymat");
}

void main() {
  MatnBufer()
    ..qosh("Assalomu ")
    ..qosh("alaykum ")
    ..qosh("Dart dasturchilari!")
    ..chopEt();
}
```

## Tushuntirish va Mantiq:
Kaskad operatori metod `void` qaytarsa ham ob'ektning o'ziga havolani ushlab qolib, zanjirli chaqiruvlarni osonlashtiradi.

## Ishlash natijasi:
```text
Matn: Assalomu alaykum Dart dasturchilari!
```

# 191-Topshiriq: Quyruq rekursiyasi (Tail Recursion) tahlili
## Topshiriq sharti:
Akkumulyator orqali natijani parametrlarda yig'ib boruvchi quyruq rekursiyasi faktorialini yozing.

## Yechim (Dart kodi):
```dart
int tailFact(int n, [int acc = 1]) {
  if (n <= 1) return acc;
  return tailFact(n - 1, n * acc); // Oxirgi amal faqat funksiya chaqiruvi!
}

void main() {
  print("5! = ${tailFact(5)}");
  print("6! = ${tailFact(6)}");
}
```

## Tushuntirish va Mantiq:
Quyruq rekursiyasida funksiya chaqiruvidan keyin boshqa arifmetik amal bajarilmaydi, bu esa kompilyatorga stekni optimallashtirish imkonini beradi.

## Ishlash natijasi:
```text
5! = 120
6! = 720
```

# 192-Topshiriq: Rekursiya chuqurligi va StackOverflowError tahlili
## Topshiriq sharti:
Dart da juda chuqur rekursiya chaqirilganda sodir bo'ladigan stek to'lishini `try-catch` bilan tahlil qiling.

## Yechim (Dart kodi):
```dart
void cheksizRekursiya(int qadam) {
  if (qadam > 50000) return; // Xavfsizlik chegarasi
  cheksizRekursiya(qadam + 1);
}

void main() {
  try {
    cheksizRekursiya(1);
    print("50,000 qadam muvaffaqiyatli bajarildi!");
  } catch (e) {
    print("Stek to'ldi: $e");
  }
}
```

## Tushuntirish va Mantiq:
Dart chaqiruvlar steki cheklangan bo'lib, o'ta chuqur hisob-kitoblarda rekursiya o'rniga oddiy sikllar ishlatilishi lozim.

## Ishlash natijasi:
```text
50,000 qadam muvaffaqiyatli bajarildi!
```

# 193-Topshiriq: Ikkilik sonni o'nlikka o'giruvchi rekursiv funksiya
## Topshiriq sharti:
Binar satrni (masalan '1101') rekursiya orqali o'nlik butun songa aylantiring.

## Yechim (Dart kodi):
```dart
int bin2Dec(String bin, [int power = 0]) {
  if (bin.isEmpty) return 0;
  int lastBit = int.parse(bin[bin.length - 1]);
  int value = lastBit * (1 << power);
  return value + bin2Dec(bin.substring(0, bin.length - 1), power + 1);
}

void main() {
  print("'101' -> ${bin2Dec('101')}");   // 5
  print("'1111' -> ${bin2Dec('1111')}"); // 15
}
```

## Tushuntirish va Mantiq:
Binar sonning har bir biti 2 ning darajasiga ko'paytirilib, rekursiv qo'shib boriladi.

## Ishlash natijasi:
```text
'101' -> 5
'1111' -> 15
```

# 194-Topshiriq: Rekursiv Palindrom satr tekshiruvi
## Topshiriq sharti:
Satr boshidagi va oxiridagi belgilarni tekshirib, ichkariga qarab qisqaruvchi rekursiv palindrom tekshiruvini yozing.

## Yechim (Dart kodi):
```dart
bool isStringPalindrome(String s) {
  if (s.length <= 1) return true;
  if (s[0] != s[s.length - 1]) return false;
  return isStringPalindrome(s.substring(1, s.length - 1));
}

void main() {
  print("'kiyik' palindrommi: ${isStringPalindrome('kiyik')}");
  print("'dart' palindrommi:  ${isStringPalindrome('dart')}");
}
```

## Tushuntirish va Mantiq:
Har bir qadamda chekka harflar solishtiriladi va satr 2 ta belgiga qisqartirib boriladi.

## Ishlash natijasi:
```text
'kiyik' palindrommi: true
'dart' palindrommi:  false
```

# 195-Topshiriq: Funksiya parametrlarini o'zgartirmaslik (Immutability kafolati)
## Topshiriq sharti:
Funksiya kiruvchi ro'yxatni o'zgartirib qo'ymasligi uchun uni `List.unmodifiable` bilan himoyalang.

## Yechim (Dart kodi):
```dart
void xavfsizQaytaIshlash(List<int> xomRo'yxat) {
  final himoyalangan = List<int>.unmodifiable(xomRo'yxat);

  print("Ro'yxat elementlari: $himoyalangan");
  try {
    himoyalangan[0] = 999; // Xatolik beradi
  } catch (e) {
    print("Kutilgan himoya: Ro'yxat o'zgarmas (UnsupportedError)!");
  }
}

void main() {
  List<int> sonlar = [1, 2, 3];
  xavfsizQaytaIshlash(sonlar);
}
```

## Tushuntirish va Mantiq:
`List.unmodifiable` tashqi kodning ma'lumotlarni tasodifan buzib qo'yishining oldini oladi.

## Ishlash natijasi:
```text
Ro'yxat elementlari: [1, 2, 3]
Kutilgan himoya: Ro'yxat o'zgarmas (UnsupportedError)!
```

# 196-Topshiriq: Retry (Qayta urinish) funksional naqshi
## Topshiriq sharti:
Muvaffaqiyatsiz bo'lgan operatsiyani belgilangan N marta qayta urinib ko'ruvchi `retry` Higher-Order funksiyasini yozing.

## Yechim (Dart kodi):
```dart
T retry<T>(T Function() operation, {int maxAttempts = 3}) {
  int attempts = 0;
  while (true) {
    try {
      attempts++;
      return operation();
    } catch (e) {
      if (attempts >= maxAttempts) {
        rethrow;
      }
      print("Urinish $attempts muvaffaqiyatsiz. Qayta urinilmoqda...");
    }
  }
}

void main() {
  int counter = 0;
  int res = retry(() {
    counter++;
    if (counter < 3) throw Exception("Tarmoqda uzilish");
    return 200; // 3-urinishda muvaffaqiyat
  });

  print("Muvaffaqiyatli yakun: Kod $res");
}
```

## Tushuntirish va Mantiq:
Retry funksiyasi tarmoq so'rovlari va beqaror xizmatlar bilan ishlashda chidamlilikni (resilience) ta'minlaydi.

## Ishlash natijasi:
```text
Urinish 1 muvaffaqiyatsiz. Qayta urinilmoqda...
Urinish 2 muvaffaqiyatsiz. Qayta urinilmoqda...
Muvaffaqiyatli yakun: Kod 200
```

# 197-Topshiriq: Xotira tejovchi generatordan qismini olish (take / skip)
## Topshiriq sharti:
Cheksiz generator natijasidan dastlabki N tasini olish uchun `take()` metodini qo'llang.

## Yechim (Dart kodi):
```dart
Iterable<int> juftSonlarCheksiz() sync* {
  int n = 0;
  while (true) {
    yield n;
    n += 2;
  }
}

void main() {
  // Cheksiz oqimdan faqat dastlabki 5 tasini olamiz
  var dastlabki5 = juftSonlarCheksiz().take(5).toList();
  print("Dastlabki 5 ta juft son: $dastlabki5");

  // 10 tasini tashlab keyingi 3 tasini olamiz
  var keyingi3 = juftSonlarCheksiz().skip(10).take(3).toList();
  print("10 tasidan keyingi 3 tasi: $keyingi3");
}
```

## Tushuntirish va Mantiq:
`take` va `skip` lazy generatorlar bilan mukammal ishlaydi va faqat kerakli qadamlargacha hisoblaydi.

## Ishlash natijasi:
```text
Dastlabki 5 ta juft son: [0, 2, 4, 6, 8]
10 tasidan keyingi 3 tasi: [20, 22, 24]
```

# 198-Topshiriq: Universal validatorlar zanjiri (Chain of Validators)
## Topshiriq sharti:
Matnni bir nechta qoidalarga (uzunligi > 6, raqam borligi, katta harf borligi) tekshiruvchi validator funksiyasini yarating.

## Yechim (Dart kodi):
```dart
typedef Validator = String? Function(String);

String? parolTekshir(String parol) {
  List<Validator> qoidalar = [
    (p) => p.length < 8 ? "Parol kamida 8 ta belgidan iborat bo'lishi kerak" : null,
    (p) => !p.contains(RegExp(r'[0-9]')) ? "Kamida bitta raqam bo'lishi kerak" : null,
    (p) => !p.contains(RegExp(r'[A-Z]')) ? "Kamida bitta bosh harf bo'lishi kerak" : null,
  ];

  for (var qoida in qoidalar) {
    String? xato = qoida(parol);
    if (xato != null) return xato;
  }
  return null; // Barchasi to'g'ri
}

void main() {
  print("1. 'pass':       ${parolTekshir('pass')}");
  print("2. 'password':   ${parolTekshir('password')}");
  print("3. 'Password12': ${parolTekshir('Password12') ?? 'Parol a'lo darajada!'}");
}
```

## Tushuntirish va Mantiq:
Validator funksiyalari ro'yxati kodni kengaytiriluvchi va toza qiladi.

## Ishlash natijasi:
```text
1. 'pass':       Parol kamida 8 ta belgidan iborat bo'lishi kerak
2. 'password':   Kamida bitta raqam bo'lishi kerak
3. 'Password12': Parol a'lo darajada!
```

# 199-Topshiriq: Dart 3 Records bilan natija va xatolikni birga qaytarish: (T? data, String? error)
## Topshiriq sharti:
Go tilidagi kabi `(data, err)` usulida natija qaytaruvchi Dart 3 rekordini yozing.

## Yechim (Dart kodi):
```dart
(double? natija, String? xato) xavfsizBolish(double a, double b) {
  if (b == 0.0) return (null, "Nolga bo'lish xatosi!");
  return (a / b, null);
}

void main() {
  var (res1, err1) = xavfsizBolish(10, 2);
  if (err1 != null) {
    print("Xato: $err1");
  } else {
    print("Muvaffaqiyat: $res1");
  }

  var (res2, err2) = xavfsizBolish(10, 0);
  if (err2 != null) {
    print("Xato: $err2");
  } else {
    print("Muvaffaqiyat: $res2");
  }
}
```

## Tushuntirish va Mantiq:
Dart 3 Records tufayli Go yoki Rust uslubidagi xavfsiz xatolik qaytarish usuli endi Dart da ham to'liq qo'llab-quvvatlanadi.

## Ishlash natijasi:
```text
Muvaffaqiyat: 5.0
Xato: Nolga bo'lish xatosi!
```

# 200-Topshiriq: Katta amaliy loyiha: Funksional ma'lumotlar qayta ishlash quvuri (Pipeline Processor)
## Topshiriq sharti:
200-topshiriq: Xom matnli buyurtmalar ro'yxatini qabul qilib, uni tozalash, filtrlash, soliq hisoblash va umumiy jami summani chiqaruvchi to'liq funksional quvur dasturini yozing.

## Yechim (Dart kodi):
```dart
class Buyurtma {
  final String id;
  final String mahsulot;
  final double narx;

  Buyurtma(this.id, this.mahsulot, this.narx);

  @override
  String toString() => "[$id] $mahsulot: $narx so'm";
}

void main() {
  // Xom matnli kirish ma'lumotlari
  List<String> xomQatorlar = [
    "ORD-1, Noutbuk, 8000000",
    "ORD-2, Sichqoncha, 150000",
    "BEKOR_QILINGAN, Noma'lum, 0",
    "ORD-3, Monitor, 2500000",
  ];

  // 1. Matnlarni Buyurtma ob'ektlariga aylantirish
  var buyurtmalar = xomQatorlar
      .where((s) => s.startsWith("ORD"))
      .map((s) {
        var qismlar = s.split(",");
        return Buyurtma(
          qismlar[0].trim(),
          qismlar[1].trim(),
          double.parse(qismlar[2].trim()),
        );
      })
      .toList();

  print("Muvaffaqiyatli parse qilingan buyurtmalar:");
  buyurtmalar.forEach((b) => print("  $b"));

  // 2. QQS solig'i bilan jami summani hisoblash (reduce / fold)
  double jamiNarx = buyurtmalar.fold(0.0, (sum, b) => sum + b.narx);
  double qqs = jamiNarx * 0.12; // 12% QQS
  double umumiySumma = jamiNarx + qqs;

  print("------------------------------------------");
  print("Jami sof narx: $jamiNarx so'm");
  print("QQS (12%):     $qqs so'm");
  print("To'lanishi kerak: $umumiySumma so'm");
  print("------------------------------------------");
}
```

## Tushuntirish va Mantiq:
200-topshiriq bilan Dart tilida funksiyalar, lambda ifodalar, yuqori darajali metodlar va ma'lumotlar oqimini toza arxitekturada boshqarish to'liq o'zlashtirildi.

## Ishlash natijasi:
```text
Muvaffaqiyatli parse qilingan buyurtmalar:
  [ORD-1] Noutbuk: 8000000.0 so'm
  [ORD-2] Sichqoncha: 150000.0 so'm
  [ORD-3] Monitor: 2500000.0 so'm
------------------------------------------
Jami sof narx: 10650000.0 so'm
QQS (12%):     1278000.0 so'm
To'lanishi kerak: 11928000.0 so'm
------------------------------------------
```

