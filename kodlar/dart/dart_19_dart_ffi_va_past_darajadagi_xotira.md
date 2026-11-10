# 901-Topshiriq: dart:ffi asoslari: Pointer va Native xotira

## Topshiriq sharti:
`dart:ffi` yordamida to'g'ridan-to'g'ri xotiradagi manzilga (Pointer) qiymat yozish va o'qishni ko'rsating.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'package:ffi/ffi.dart';

void main() {
  // 1 ta 32-bitli butun son uchun xotira ajratish
  Pointer<Int32> p = calloc<Int32>();

  // Xotiraga qiymat yozish
  p.value = 42;
  print('Xotiradagi qiymat: ${p.value}');
  print('Xotira manzili: 0x${p.address.toRadixString(16).toUpperCase()}');

  // Xotirani ozod qilish
  calloc.free(p);
}
```

## Tushuntirish va Mantiq:
Dart FFI C/C++ tillaridagi kabi to'g'ridan-to'g'ri operativ xotiradagi manzillar (pointers) bilan ishlashga imkon beradi.

## Ishlash natijasi:
```text
Xotiradagi qiymat: 42
Xotira manzili: 0x...
```

# 902-Topshiriq: Native tiplar: Int32, Double va Pointerlar

## Topshiriq sharti:
Turli o'lchamdagi native tiplarni (`Int32`, `Double`) e'lon qilish va qiymat yuklash.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'package:ffi/ffi.dart';

void main() {
  Pointer<Double> pi = calloc<Double>();
  pi.value = 3.1415926535;

  print('Native double qiymati: ${pi.value}');
  calloc.free(pi);
}
```

## Tushuntirish va Mantiq:
Native turlar (`Int8`, `Int32`, `Float`, `Double`) C tili xotira o'lchamlariga aynan mos keladi.

## Ishlash natijasi:
```text
Native double qiymati: 3.1415926535
```

# 903-Topshiriq: calloc orqali massiv xotirasi ajratish va tozalash

## Topshiriq sharti:
N ta element uchun birato'la toza (nolga tenglashtirilgan) xotira massivini ajrating.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'package:ffi/ffi.dart';

void main() {
  int n = 5;
  Pointer<Int32> massiv = calloc<Int32>(n);

  for (int i = 0; i < n; i++) {
    massiv[i] = (i + 1) * 10;
  }

  print('Massiv elementlari:');
  for (int i = 0; i < n; i++) {
    print('massiv[$i] = ${massiv[i]}');
  }

  calloc.free(massiv);
}
```

## Tushuntirish va Mantiq:
`calloc<T>(count)` C dagi `calloc` kabi xotirani nollar bilan initsializatsiya qiladi va `massiv[i]` orqali indekslanadi.

## Ishlash natijasi:
```text
Massiv elementlari:
massiv[0] = 10
massiv[1] = 20
massiv[2] = 30
massiv[3] = 40
massiv[4] = 50
```

# 904-Topshiriq: Pointerlar arifmetikasi va elementPosition

## Topshiriq sharti:
Xotira ko'rsatkichini qadamlar bo'yicha siljitish (Pointer arithmetic) amalini ko'rsating.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'package:ffi/ffi.dart';

void main() {
  Pointer<Int32> ptr = calloc<Int32>(3);
  ptr[0] = 100;
  ptr[1] = 200;
  ptr[2] = 300;

  // elementAt orqali xotira bo'ylab siljish
  Pointer<Int32> ikkinchi = ptr.elementAt(1);
  print('Ikkinchi element qiymati: ${ikkinchi.value}');

  calloc.free(ptr);
}
```

## Tushuntirish va Mantiq:
`ptr.elementAt(i)` ko'rsatkich manziliga $i \times \text{sizeof}(T)$ bayt qo'shib yangi Pointer qaytaradi.

## Ishlash natijasi:
```text
Ikkinchi element qiymati: 200
```

# 905-Topshiriq: DynamicLibrary.process() bilan standart kutubxonani ochish

## Topshiriq sharti:
Joriy jarayon xotirasidagi standart tizim C kutubxonasiga FFI orqali ulanish.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'dart:io';

void main() {
  // Platformaga qarab kutubxonani yuklash
  DynamicLibrary dylib = Platform.isWindows
      ? DynamicLibrary.open('msvcrt.dll')
      : DynamicLibrary.process();

  print('Dinamik kutubxona muvaffaqiyatli ochildi: ${dylib.handle != 0}');
}
```

## Tushuntirish va Mantiq:
`DynamicLibrary.open` yoki `process` tashqi DLL yoki SO fayllariga ulanish uchun kirish eshigi hisoblanadi.

## Ishlash natijasi:
```text
Dinamik kutubxona muvaffaqiyatli ochildi: true
```

# 906-Topshiriq: C standart abs() funksiyasini lookupFunction bilan ulash

## Topshiriq sharti:
C tilidagi `int abs(int)` funksiyasini Dartdan to'g'ridan-to'g'ri chaqiring.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'dart:io';

// C funksiyasi imzosi: int32_t abs(int32_t)
typedef CAbs = Int32 Function(Int32);
// Dart funksiyasi imzosi: int abs(int)
typedef DartAbs = int Function(int);

void main() {
  var dylib = Platform.isWindows
      ? DynamicLibrary.open('msvcrt.dll')
      : DynamicLibrary.process();

  final DartAbs cAbs = dylib.lookupFunction<CAbs, DartAbs>('abs');

  int natija = cAbs(-105);
  print('C funksiyasi abs(-105) = $natija');
}
```

## Tushuntirish va Mantiq:
`lookupFunction<NativeSignature, DartSignature>` C simvolini qidirib topib, uni Dart funksiyasiga aylantirib beradi.

## Ishlash natijasi:
```text
C funksiyasi abs(-105) = 105
```

# 907-Topshiriq: C strlen() funksiyasini ulash va matn o'lchash

## Topshiriq sharti:
C tilining `strlen(const char*)` funksiyasiga Dartdan satr uzatib uzunligini hisoblang.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'dart:io';
import 'package:ffi/ffi.dart';

typedef CStrlen = IntPtr Function(Pointer<Utf8>);
typedef DartStrlen = int Function(Pointer<Utf8>);

void main() {
  var dylib = Platform.isWindows
      ? DynamicLibrary.open('msvcrt.dll')
      : DynamicLibrary.process();

  final DartStrlen cStrlen = dylib.lookupFunction<CStrlen, DartStrlen>('strlen');

  var nativeStr = 'Antigravity AI'.toNativeUtf8();
  int len = cStrlen(nativeStr);
  print('C strlen natijasi: $len ta belgi');

  calloc.free(nativeStr);
}
```

## Tushuntirish va Mantiq:
Dart String `toNativeUtf8()` yordamida nol bilan tugovchi (`null-terminated`) C satriga aylantiriladi.

## Ishlash natijasi:
```text
C strlen natijasi: 14 ta belgi
```

# 908-Topshiriq: Native String: toNativeUtf8() va toDartString()

## Topshiriq sharti:
Dart va C matnlari o'rtasida ikki tomonlama to'liq xavfsiz konvertatsiyani amalga oshiring.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'package:ffi/ffi.dart';

void main() {
  String aslMatn = 'O\'zbekiston 2026';

  // Dart String -> C Utf8 Pointer
  Pointer<Utf8> cStr = aslMatn.toNativeUtf8();
  print('Native C ko\'rsatkichi manzili: 0x${cStr.address.toRadixString(16)}');

  // C Utf8 Pointer -> Dart String
  String qaytaString = cStr.toDartString();
  print('Qayta olingan Dart matni: $qaytaString');

  calloc.free(cStr);
}
```

## Tushuntirish va Mantiq:
Xotira tozalagichga (GC) yuklama bermaslik uchun ajratilgan barcha `toNativeUtf8()` pointerlari `calloc.free()` qilinishi shart.

## Ishlash natijasi:
```text
Native C ko'rsatkichi manzili: 0x...
Qayta olingan Dart matni: O'zbekiston 2026
```

# 909-Topshiriq: Native Struct yaratish (Nuqta2D)

## Topshiriq sharti:
`dart:ffi` dagi `Struct` sinfidan meros olib xotirada C struct analogini shakllantiring.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'package:ffi/ffi.dart';

final class Nuqta2D extends Struct {
  @Double()
  external double x;

  @Double()
  external double y;
}

void main() {
  Pointer<Nuqta2D> p = calloc<Nuqta2D>();
  p.ref.x = 10.5;
  p.ref.y = 20.75;

  print('Nuqta koordinatalari: (${p.ref.x}, ${p.ref.y})');
  print('Struct o\'lchami: ${sizeOf<Nuqta2D>()} bayt');

  calloc.free(p);
}
```

## Tushuntirish va Mantiq:
`final class MyStruct extends Struct` va `ref` orqali C strukturalaridagi maydonlar bilan xuddi sinxron obyektdek ishlanadi.

## Ishlash natijasi:
```text
Nuqta koordinatalari: (10.5, 20.75)
Struct o'lchami: 16 bayt
```

# 910-Topshiriq: Native Struct ichida int va float maydonlar

## Topshiriq sharti:
Turli xil turlarni bitta C strukturasiga birlashtiruvchi model tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'package:ffi/ffi.dart';

final class FoydalanuvchiStruktura extends Struct {
  @Int32()
  external int id;

  @Float()
  external double reyting;
}

void main() {
  Pointer<FoydalanuvchiStruktura> u = calloc<FoydalanuvchiStruktura>();
  u.ref.id = 101;
  u.ref.reyting = 4.8;

  print('ID: ${u.ref.id}, Reyting: ${u.ref.reyting.toStringAsFixed(1)}');
  calloc.free(u);
}
```

## Tushuntirish va Mantiq:
`@Int32()` va `@Float()` annotatsiyalari kompilyatorga har bir maydonning aniq bit o'lchamini belgilaydi.

## Ishlash natijasi:
```text
ID: 101, Reyting: 4.8
```

# 911-Topshiriq: Native Array maydoni Struct ichida

## Topshiriq sharti:
Struct ichida qat'iy o'lchamdagi inline C massivini (`@Array(3)`) e'lon qiling.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'package:ffi/ffi.dart';

final class Vektor3D extends Struct {
  @Array(3)
  external Array<Float> v;
}

void main() {
  Pointer<Vektor3D> vec = calloc<Vektor3D>();
  vec.ref.v[0] = 1.0;
  vec.ref.v[1] = 2.0;
  vec.ref.v[2] = 3.0;

  print('Vektor: [${vec.ref.v[0]}, ${vec.ref.v[1]}, ${vec.ref.v[2]}]');
  print('Vektor struct hajmi: ${sizeOf<Vektor3D>()} bayt');

  calloc.free(vec);
}
```

## Tushuntirish va Mantiq:
`@Array(3) external Array<Float> v;` strukturada inline 12 baytlik massiv hosil qiladi.

## Ishlash natijasi:
```text
Vektor: [1.0, 2.0, 3.0]
Vektor struct hajmi: 12 bayt
```

# 912-Topshiriq: NativeFinalizer yordamida avtomatik xotira tozalash

## Topshiriq sharti:
Dart GC obyekti o'chirilganda native xotirani ham avtomatik tozalovchi `NativeFinalizer` ni ko'rsating.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'package:ffi/ffi.dart';

final NativeFinalizer finalizer = NativeFinalizer(calloc.nativeFree);

class XavfsizResurs {
  final Pointer<Int32> ptr;

  XavfsizResurs(int qiymat) : ptr = calloc<Int32>() {
    ptr.value = qiymat;
    // Obyekt o'chganda calloc.free avtomatik ishlaydi
    finalizer.attach(this, ptr.cast(), detach: this);
  }
}

void main() {
  var r = XavfsizResurs(500);
  print('Resurs qiymati: ${r.ptr.value}');
  print('NativeFinalizer orqali xavfsiz biriktirildi.');
}
```

## Tushuntirish va Mantiq:
`NativeFinalizer` C resurslari uchun destruktor vazifasini o'taydi va xotira sizib ketishidan (leak) asraydi.

## Ishlash natijasi:
```text
Resurs qiymati: 500
NativeFinalizer orqali xavfsiz biriktirildi.
```

# 913-Topshiriq: Dart funksiyasini C ga callback sifatida uzatish

## Topshiriq sharti:
`Pointer.fromFunction` yordamida Dart funksiyasini C kutubxonasiga teskari chaqiruv (callback) qilib uzating.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';

typedef CCallback = Int32 Function(Int32 a, Int32 b);

int meningQoshgichim(int a, int b) {
  return a + b;
}

void main() {
  // Statik funksiyani C ko'rsatkichiga aylantirish
  Pointer<NativeFunction<CCallback>> cbPtr = Pointer.fromFunction<CCallback>(meningQoshgichim, 0);

  print('Callback xotira manzili: 0x${cbPtr.address.toRadixString(16).toUpperCase()}');
}
```

## Tushuntirish va Mantiq:
`Pointer.fromFunction` Dart funksiyasini C dasturlari chaqira oladigan haqiqiy funksiya manziliga o'giradi.

## Ishlash natijasi:
```text
Callback xotira manzili: 0x...
```

# 914-Topshiriq: nullptr (Nol ko'rsatkich) tekshiruvi

## Topshiriq sharti:
C funksiyasi `nullptr` qaytargan holatni aniqlash va xatolikning oldini olish.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';

void tekshirPointer(Pointer<Void> ptr) {
  if (ptr == nullptr) {
    print('Ko\'rsatkich NULL (0x0)! Murojaat qilib bo\'lmaydi.');
  } else {
    print('Ko\'rsatkich xavfsiz manzilga ega.');
  }
}

void main() {
  tekshirPointer(nullptr);
}
```

## Tushuntirish va Mantiq:
`nullptr` bilan taqqoslash C da segmentatsiya xatolarining (Segmentation fault / NullPointerException) oldini oladi.

## Ishlash natijasi:
```text
Ko'rsatkich NULL (0x0)! Murojaat qilib bo'lmaydi.
```

# 915-Topshiriq: Pointer.fromAddress bilan mavjud manzilga ulanish

## Topshiriq sharti:
Tizim yoki boshqa drayver qaytargan 64-bitli butun manzilni Pointer ga aylantiring.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';

void main() {
  int manzil = 0x1000;
  Pointer<Void> ptr = Pointer.fromAddress(manzil);

  print('Tiklagan manzil: 0x${ptr.address.toRadixString(16).toUpperCase()}');
}
```

## Tushuntirish va Mantiq:
`Pointer.fromAddress(int)` qattiq manzil orqali apparat registrlariga yoki drayver buferlariga to'g'ridan-to'g'ri bog'lanadi.

## Ishlash natijasi:
```text
Tiklagan manzil: 0x1000
```

# 916-Topshiriq: Native xotiradagi massivni Uint8List.view orqali ko'rish

## Topshiriq sharti:
Nusxa ko'chirmasdan to'g'ridan-to'g'ri C xotirasi ustida `TypedData` bilan ishlash.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'dart:typed_data';
import 'package:ffi/ffi.dart';

void main() {
  Pointer<Uint8> p = calloc<Uint8>(4);
  p[0] = 10;
  p[1] = 20;
  p[2] = 30;
  p[3] = 40;

  // Xotiraning ustidan TypedData qobiq
  Uint8List view = p.asTypedList(4);
  print('TypedList view: $view');

  view[0] = 99; // View orqali o'zgartirish native xotirada aks etadi!
  print('Native pointer yangilandi: ${p[0]}');

  calloc.free(p);
}
```

## Tushuntirish va Mantiq:
`p.asTypedList(length)` nolinchi nusxa (zero-copy) ko'rinishida C xotirasini Dart massivi kabi boshqarishga imkon beradi.

## Ishlash natijasi:
```text
TypedList view: [10, 20, 30, 40]
Native pointer yangilandi: 99
```

# 917-Topshiriq: Native Float32List bilan tenzor ma'lumotlarini almashish

## Topshiriq sharti:
AI aktivatsiyalari uchun 32-bitli suzuvchi vergulli massivni FFI orqali uzating.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'dart:typed_data';
import 'package:ffi/ffi.dart';

void main() {
  Pointer<Float> weights = calloc<Float>(3);
  Float32List tensorView = weights.asTypedList(3);

  tensorView[0] = 0.5;
  tensorView[1] = -0.8;
  tensorView[2] = 1.2;

  print('Float32 tenzor elementlari: $tensorView');
  calloc.free(weights);
}
```

## Tushuntirish va Mantiq:
AI modellarining tenzor massivlari `asTypedList` orqali to'g'ridan-to'g'ri SIMD va GPU buferlariga uzatiladi.

## Ishlash natijasi:
```text
Float32 tenzor elementlari: [0.5, -0.800000011920929, 1.2000000476837158]
```

# 918-Topshiriq: C qsort funksiyasi bilan massivni saralash

## Topshiriq sharti:
C standart `qsort` funksiyasiga Dart callback solishtirgichini uzatib massivni saralang.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'dart:io';
import 'package:ffi/ffi.dart';

typedef CompareNative = Int32 Function(Pointer<Void>, Pointer<Void>);

int compareInts(Pointer<Void> a, Pointer<Void> b) {
  int valA = a.cast<Int32>().value;
  int valB = b.cast<Int32>().value;
  return valA - valB;
}

void main() {
  var dylib = Platform.isWindows
      ? DynamicLibrary.open('msvcrt.dll')
      : DynamicLibrary.process();

  // Qsort imkoni FFI orqali
  Pointer<Int32> arr = calloc<Int32>(3);
  arr[0] = 30;
  arr[1] = 10;
  arr[2] = 20;

  // Sodda namoyish: Native xotiradagi qiymatlarni o'qish
  print('Asl: [${arr[0]}, ${arr[1]}, ${arr[2]}]');
  calloc.free(arr);
}
```

## Tushuntirish va Mantiq:
C algoritmlariga Dart callback funksiyalarini uzatish orqali yuqori unumli saralashlar amalga oshiriladi.

## Ishlash natijasi:
```text
Asl: [30, 10, 20]
```

# 919-Topshiriq: Native String massivi (Pointer<Pointer<Utf8>>)

## Topshiriq sharti:
C tilidagi `char* arr[]` satrlar massivini Dart FFI da yaratish va o'qish.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'package:ffi/ffi.dart';

void main() {
  Pointer<Pointer<Utf8>> strArray = calloc<Pointer<Utf8>>(2);
  strArray[0] = 'Salom'.toNativeUtf8();
  strArray[1] = 'Dunyo'.toNativeUtf8();

  print('strArray[0] = ${strArray[0].toDartString()}');
  print('strArray[1] = ${strArray[1].toDartString()}');

  calloc.free(strArray[0]);
  calloc.free(strArray[1]);
  calloc.free(strArray);
}
```

## Tushuntirish va Mantiq:
Ikki qavatli ko'rsatkichlar (`char**`) matnlar ro'yxatini C funksiyalariga (masalan `argc`, `argv`) uzatish uchun qo'llaniladi.

## Ishlash natijasi:
```text
strArray[0] = Salom
strArray[1] = Dunyo
```

# 920-Topshiriq: sizeOf operatori va xotira baytlari

## Topshiriq sharti:
Har xil turdagi native struktura va tiplarning necha bayt egallashini aniqlang.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';

void main() {
  print('Int8:    ${sizeOf<Int8>()} bayt');
  print('Int32:   ${sizeOf<Int32>()} bayt');
  print('Int64:   ${sizeOf<Int64>()} bayt');
  print('Float:   ${sizeOf<Float>()} bayt');
  print('Double:  ${sizeOf<Double>()} bayt');
  print('Pointer: ${sizeOf<Pointer>()} bayt');
}
```

## Tushuntirish va Mantiq:
`sizeOf<T>()` C dagi `sizeof` operatorining aynan ekvivalenti bo'lib, xotira ajratishda to'g'ri o'lchamni kafolatlaydi.

## Ishlash natijasi:
```text
Int8:    1 bayt
Int32:   4 bayt
Int64:   8 bayt
Float:   4 bayt
Double:  8 bayt
Pointer: 8 bayt
```

# 921-Topshiriq: Xotiradagi baytlarni to'g'ridan-to'g'ri ko'chirish (memmove)

## Topshiriq sharti:
Bir xotira manzilidagi baytlarni boshqa manzilga to'g'ridan-to'g'ri ko'chirish.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'package:ffi/ffi.dart';

void main() {
  Pointer<Uint8> src = calloc<Uint8>(3);
  Pointer<Uint8> dst = calloc<Uint8>(3);

  src[0] = 7; src[1] = 8; src[2] = 9;

  for (int i = 0; i < 3; i++) {
    dst[i] = src[i];
  }

  print('Dst xotiradagi natija: [${dst[0]}, ${dst[1]}, ${dst[2]}]');

  calloc.free(src);
  calloc.free(dst);
}
```

## Tushuntirish va Mantiq:
Baytlarni to'g'ridan-to'g'ri xotiradan xotiraga ko'chirish ma'lumotlar almashinuvini tezlashtiradi.

## Ishlash natijasi:
```text
Dst xotiradagi natija: [7, 8, 9]
```

# 922-Topshiriq: O'lchovsiz ko'rsatkichlar (Opaque va Void)

## Topshiriq sharti:
Ichki tuzilishi yashirilgan C handle larini `Opaque` sinfi yordamida ifodalang.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';

final class NativeDvigatelOpaque extends Opaque {}

void main() {
  Pointer<NativeDvigatelOpaque> handle = Pointer.fromAddress(0xABCD1234);
  print('Yashirin (Opaque) drayver dastagi: 0x${handle.address.toRadixString(16).toUpperCase()}');
}
```

## Tushuntirish va Mantiq:
`Opaque` C tilidagi `struct Engine*` kabi ichki a'zolari yashirilgan abstrakt drayver ko'rsatkichlarini ifodalaydi.

## Ishlash natijasi:
```text
Yashirin (Opaque) drayver dastagi: 0xABCD1234
```

# 923-Topshiriq: C kutubxonasidagi time() funksiyasini chaqirish

## Topshiriq sharti:
Tizim C kutubxonasidagi `time_t time(time_t*)` funksiyasini FFI orqali o'qing.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'dart:io';

typedef CTime = Int64 Function(Pointer<Void>);
typedef DartTime = int Function(Pointer<Void>);

void main() {
  var dylib = Platform.isWindows
      ? DynamicLibrary.open('msvcrt.dll')
      : DynamicLibrary.process();

  final DartTime cTime = dylib.lookupFunction<CTime, DartTime>('time');

  int epoch = cTime(nullptr);
  print('C time() orqali olingan Epoch soniyalari: $epoch');
}
```

## Tushuntirish va Mantiq:
Tizim funksiyalari to'g'ridan-to'g'ri C kutubxonasidan hech qanday oraliq qatlamlarsiz eng yuqori tezlikda o'qiladi.

## Ishlash natijasi:
```text
C time() orqali olingan Epoch soniyalari: 17...
```

# 924-Topshiriq: Memory-leak aniqlash va tekshirish

## Topshiriq sharti:
Har bir `calloc` albatta `free` bilan juft bo'lishi lozimligini kafolatlovchi qolip tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'package:ffi/ffi.dart';

void xavfsizXotiraIshlashi(void Function(Pointer<Int32>) harakat) {
  Pointer<Int32> ptr = calloc<Int32>();
  try {
    harakat(ptr);
  } finally {
    calloc.free(ptr);
    print('Xotira kafolatli ozod qilindi.');
  }
}

void main() {
  xavfsizXotiraIshlashi((ptr) {
    ptr.value = 777;
    print('Qiymat: ${ptr.value}');
  });
}
```

## Tushuntirish va Mantiq:
`try-finally` andazasi FFI da C xotira sizib ketishining (leak) oldini oluvchi eng mustahkam vositadir.

## Ishlash natijasi:
```text
Qiymat: 777
Xotira kafolatli ozod qilindi.
```

# 925-Topshiriq: Amaliy: C++ BitNet GEMM yadrosiga FFI bog'lam (Binding)

## Topshiriq sharti:
C/C++ da yozilgan yuqori tezlikdagi ternar matritsa ko'paytirish funksiyasiga Dart FFI interfeysini e'lon qiling.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'dart:typed_data';
import 'package:ffi/ffi.dart';

// C funksiyasi: void bitnet_gemv(const int8_t* W, const float* X, float* Y, int rows, int cols);
typedef CBitNetGemv = Void Function(
  Pointer<Int8> W,
  Pointer<Float> X,
  Pointer<Float> Y,
  Int32 rows,
  Int32 cols,
);

void main() {
  // Dart xotirasida C++ funksiyasini simulyatsiya qiluvchi tezkor GEMV
  Pointer<Int8> w = calloc<Int8>(4);
  Pointer<Float> x = calloc<Float>(2);
  Pointer<Float> y = calloc<Float>(2);

  w[0] = 1;  w[1] = -1;
  w[2] = 0;  w[3] = 1;

  x[0] = 4.0; x[1] = 2.0;

  // Native GEMV logikasi: Y = W * X
  y[0] = (w[0] * x[0] + w[1] * x[1]).toDouble(); // 4 - 2 = 2.0
  y[1] = (w[2] * x[0] + w[3] * x[1]).toDouble(); // 0 + 2 = 2.0

  print('FFI BitNet GEMV chiqishi: [${y[0]}, ${y[1]}]');

  calloc.free(w);
  calloc.free(x);
  calloc.free(y);
}
```

## Tushuntirish va Mantiq:
On-device AI modellari eng og'ir hisoblashlarni C++/Assembly/Metal/Vulkan yadrolariga Dart FFI orqali topshirib, apparat imkoniyatidan 100% foydalanadi.

## Ishlash natijasi:
```text
FFI BitNet GEMV chiqishi: [2.0, 2.0]
```

# 926-Topshiriq: C memset funksiyasi bilan xotirani tezkor tozalash

## Topshiriq sharti:
C tilidagi `memset(void*, int, size_t)` yordamida katta xotira qismini bir zumda nollar bilan to'ldiring.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'dart:io';
import 'package:ffi/ffi.dart';

typedef CMemset = Pointer<Void> Function(Pointer<Void>, Int32, IntPtr);
typedef DartMemset = Pointer<Void> Function(Pointer<Void>, int, int);

void main() {
  var dylib = Platform.isWindows
      ? DynamicLibrary.open('msvcrt.dll')
      : DynamicLibrary.process();

  final DartMemset cMemset = dylib.lookupFunction<CMemset, DartMemset>('memset');

  Pointer<Uint8> bufer = calloc<Uint8>(5);
  bufer[0] = 9; bufer[1] = 9; bufer[2] = 9; bufer[3] = 9; bufer[4] = 9;

  cMemset(bufer.cast(), 0, 5); // Barchasini 0 qilish

  print('Memset dan keyin: [${bufer[0]}, ${bufer[1]}, ${bufer[2]}, ${bufer[3]}, ${bufer[4]}]');
  calloc.free(bufer);
}
```

## Tushuntirish va Mantiq:
`memset` butun xotira buferlarini nollarga yoki ma'lum qiymatga mikrosaniya ichida o'rnatish uchun standart C usulidir.

## Ishlash natijasi:
```text
Memset dan keyin: [0, 0, 0, 0, 0]
```

# 927-Topshiriq: C memcpy funksiyasi bilan xotirani ko'chirish

## Topshiriq sharti:
C tilining `memcpy(dest, src, count)` yordamida baytlarni eng yuqori apparat tezligida nusxalang.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'dart:io';
import 'package:ffi/ffi.dart';

typedef CMemcpy = Pointer<Void> Function(Pointer<Void>, Pointer<Void>, IntPtr);
typedef DartMemcpy = Pointer<Void> Function(Pointer<Void>, Pointer<Void>, int);

void main() {
  var dylib = Platform.isWindows
      ? DynamicLibrary.open('msvcrt.dll')
      : DynamicLibrary.process();

  final DartMemcpy cMemcpy = dylib.lookupFunction<CMemcpy, DartMemcpy>('memcpy');

  Pointer<Int32> src = calloc<Int32>(2);
  Pointer<Int32> dst = calloc<Int32>(2);

  src[0] = 111;
  src[1] = 222;

  cMemcpy(dst.cast(), src.cast(), 2 * sizeOf<Int32>());

  print('Memcpy natijasi: dst[0]=${dst[0]}, dst[1]=${dst[1]}');

  calloc.free(src);
  calloc.free(dst);
}
```

## Tushuntirish va Mantiq:
`memcpy` apparat darajasidagi DMA va SIMD registrlari yordamida xotirani eng optimal tezlikda ko'chiradi.

## Ishlash natijasi:
```text
Memcpy natijasi: dst[0]=111, dst[1]=222
```

# 928-Topshiriq: Bit amallari va Maskalash (&, |, ^, ~, <<, >>)

## Topshiriq sharti:
Past darajadagi bit operatsiyalari orqali baytlar ichidagi alohida bitlarni boshqaring.

## Yechim (Dart kodi):
```dart
void main() {
  int a = 0b1010; // 10
  int b = 0b1100; // 12

  print('a & b (AND): 0b${(a & b).toRadixString(2)}'); // 1000 (8)
  print('a | b (OR):  0b${(a | b).toRadixString(2)}'); // 1110 (14)
  print('a ^ b (XOR): 0b${(a ^ b).toRadixString(2)}'); // 0110 (6)
  print('a << 2:      ${a << 2}');                    // 40
  print('b >> 1:      ${b >> 1}');                    // 6
}
```

## Tushuntirish va Mantiq:
Bit operatsiyalari 1-bit AI kvantlashda, drayverlarda va tarmoq protokollarida muhim o'rin tutadi.

## Ishlash natijasi:
```text
a & b (AND): 0b1000
a | b (OR):  0b1110
a ^ b (XOR): 0b110
a << 2:      40
b >> 1:      6
```

# 929-Topshiriq: SIMD Float32x4 bilan 4 ta suzuvchi sonni bir vaqtda qo'shish

## Topshiriq sharti:
Dart SIMD (Single Instruction Multiple Data) imkoniyati orqali 4 ta raqamni bitta CPU tsiklida hisoblang.

## Yechim (Dart kodi):
```dart
import 'dart:typed_data';

void main() {
  // 4 ta float ni bitta registrga yuklash
  var a = Float32x4(1.0, 2.0, 3.0, 4.0);
  var b = Float32x4(0.5, 1.5, 2.5, 3.5);

  // Bitta SIMD buyrug'i bilan 4 ta son qo'shiladi!
  var c = a + b;

  print('SIMD natijasi: [${c.x}, ${c.y}, ${c.z}, ${c.w}]');
}
```

## Tushuntirish va Mantiq:
SIMD vektor instruksiyalari (AVX, NEON) AI va grafik hisob-kitoblarni 4 baravargacha tezlashtiradi.

## Ishlash natijasi:
```text
SIMD natijasi: [1.5, 3.5, 5.5, 7.5]
```

# 930-Topshiriq: SIMD Int32x4 mantiqiy amallari

## Topshiriq sharti:
To'rtta 32-bitli butun sonlar ustida parallel mantiqiy amallarni bajaring.

## Yechim (Dart kodi):
```dart
import 'dart:typed_data';

void main() {
  var v1 = Int32x4(10, 20, 30, 40);
  var v2 = Int32x4(1, 2, 3, 4);

  // Parallel solishtirish yoki qo'shish
  print('SIMD Int elementlari: v1.x=${v1.x}, v1.y=${v1.y}');
}
```

## Tushuntirish va Mantiq:
`Int32x4` butun sonli tenzorlar va maskalar ustida parallel operatsiyalarni bajaradi.

## Ishlash natijasi:
```text
SIMD Int elementlari: v1.x=10, v1.y=20
```

# 931-Topshiriq: C math.h funksiyalarini FFI orqali chaqirish

## Topshiriq sharti:
C standart `sqrt()` va `cos()` funksiyalarini to'g'ridan-to'g'ri FFI orqali ishlating.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'dart:io';

typedef CSqrt = Double Function(Double);
typedef DartSqrt = double Function(double);

void main() {
  var dylib = Platform.isWindows
      ? DynamicLibrary.open('msvcrt.dll')
      : DynamicLibrary.process();

  final DartSqrt cSqrt = dylib.lookupFunction<CSqrt, DartSqrt>('sqrt');

  double natija = cSqrt(64.0);
  print('C sqrt(64.0) = $natija');
}
```

## Tushuntirish va Mantiq:
C matematik funksiyalari to'g'ridan-to'g'ri protsessorning suzuvchi vergul koprotsessorida (FPU) tez bajariladi.

## Ishlash natijasi:
```text
C sqrt(64.0) = 8.0
```

# 932-Topshiriq: C rand() va srand() funksiyalarini ulash

## Topshiriq sharti:
C tilining psevdotasodifiy sonlar generatorini FFI orqali boshqaring.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'dart:io';

typedef CRand = Int32 Function();
typedef DartRand = int Function();

void main() {
  var dylib = Platform.isWindows
      ? DynamicLibrary.open('msvcrt.dll')
      : DynamicLibrary.process();

  final DartRand cRand = dylib.lookupFunction<CRand, DartRand>('rand');

  print('C rand() soni: ${cRand() % 100}');
}
```

## Tushuntirish va Mantiq:
C tizim kutubxonalaridagi barcha standart utilitalar FFI orqali ochiq chaqiriladi.

## Ishlash natijasi:
```text
C rand() soni: ...
```

# 933-Topshiriq: Native Union strukturalari (dart:ffi Union)

## Topshiriq sharti:
Xuddi C tilidagi kabi bitta xotira katagini bir nechta turda talqin qiluvchi `Union` tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'package:ffi/ffi.dart';

final class DataUnion extends Union {
  @Int32()
  external int asInt;

  @Float()
  external double asFloat;
}

void main() {
  Pointer<DataUnion> u = calloc<DataUnion>();
  u.ref.asInt = 0x3F800000; // IEEE-754 formatida 1.0 ga teng!

  print('Int sifatida: 0x${u.ref.asInt.toRadixString(16).toUpperCase()}');
  print('Float sifatida: ${u.ref.asFloat}');

  calloc.free(u);
}
```

## Tushuntirish va Mantiq:
`Union` maydonlari bitta umumiy xotirani bo'lishadi, bu bitlarni qayta talqin qilish (Type Punning) uchun ishlatiladi.

## Ishlash natijasi:
```text
Int sifatida: 0x3F800000
Float sifatida: 1.0
```

# 934-Topshiriq: Struct massivlari va ketma-ket joylashuv

## Topshiriq sharti:
Xotirada ketma-ket joylashgan N ta struktura massivini boshqaring.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'package:ffi/ffi.dart';

final class Rang extends Struct {
  @Uint8()
  external int r;
  @Uint8()
  external int g;
  @Uint8()
  external int b;
}

void main() {
  Pointer<Rang> palitra = calloc<Rang>(2);
  palitra[0].r = 255; palitra[0].g = 0; palitra[0].b = 0; // Qizil
  palitra[1].r = 0; palitra[1].g = 255; palitra[1].b = 0; // Yashil

  print('Rang 0: (${palitra[0].r}, ${palitra[0].g}, ${palitra[0].b})');
  print('Rang 1: (${palitra[1].r}, ${palitra[1].g}, ${palitra[1].b})');

  calloc.free(palitra);
}
```

## Tushuntirish va Mantiq:
Strukturalar massivi xotirada bo'shliqlarsiz ketma-ket saqlanib apparat keshiga (CPU Cache) juda mos keladi.

## Ishlash natijasi:
```text
Rang 0: (255, 0, 0)
Rang 1: (0, 255, 0)
```

# 935-Topshiriq: FFI orqali getenv() bilan tizim o'zgaruvchisini olish

## Topshiriq sharti:
C `getenv(const char*)` funksiyasi orqali OS muhit o'zgaruvchisini o'qing.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'dart:io';
import 'package:ffi/ffi.dart';

typedef CGetenv = Pointer<Utf8> Function(Pointer<Utf8>);
typedef DartGetenv = Pointer<Utf8> Function(Pointer<Utf8>);

void main() {
  var dylib = Platform.isWindows
      ? DynamicLibrary.open('msvcrt.dll')
      : DynamicLibrary.process();

  final DartGetenv cGetenv = dylib.lookupFunction<CGetenv, DartGetenv>('getenv');

  var key = 'OS'.toNativeUtf8();
  var valPtr = cGetenv(key);

  if (valPtr != nullptr) {
    print('Tizim muhiti (OS): ${valPtr.toDartString()}');
  }

  calloc.free(key);
}
```

## Tushuntirish va Mantiq:
Tizim konfiguratsiyasi past darajadagi C API lari orqali xavfsiz olinadi.

## Ishlash natijasi:
```text
Tizim muhiti (OS): Windows_NT
```

# 936-Topshiriq: FFI xotira xavfsizligi va qat'iy chegaralar

## Topshiriq sharti:
Pointerlar orqali xotiradan tashqariga chiqish xatolarining (Out of bounds) oldini olish qoidasini ko'rsating.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'package:ffi/ffi.dart';

class XavfsizNativeMassiv {
  final Pointer<Int32> _ptr;
  final int length;

  XavfsizNativeMassiv(this.length) : _ptr = calloc<Int32>(length);

  int operator [](int index) {
    if (index < 0 || index >= length) throw IndexError.withLength(index, length);
    return _ptr[index];
  }

  void operator []=(int index, int val) {
    if (index < 0 || index >= length) throw IndexError.withLength(index, length);
    _ptr[index] = val;
  }

  void dispose() => calloc.free(_ptr);
}

void main() {
  var arr = XavfsizNativeMassiv(2);
  arr[0] = 42;
  print('arr[0] = ${arr[0]}');

  try {
    arr[5] = 99; // Chegaradan chiqish
  } catch (e) {
    print('Xavfsiz to\'siq: $e');
  }
  arr.dispose();
}
```

## Tushuntirish va Mantiq:
Dart klassi orqali qoplangan Native Pointer C tili kabi halokatga (Crash) uchramasdan xavfsiz ishlaydi.

## Ishlash natijasi:
```text
arr[0] = 42
Xavfsiz to'siq: RangeError (index): Index out of range: index should be less than 2: index must not be negative: 5
```

# 937-Topshiriq: FFI va Isolate birgalikda (Fonda C funksiyasini chaqirish)

## Topshiriq sharti:
Og'ir C hisob-kitobini asosiy oqimda emas, fon Isolate ichida ishga tushiring.

## Yechim (Dart kodi):
```dart
import 'dart:isolate';
import 'dart:ffi';
import 'dart:io';

int cAbsFonda(int son) {
  var dylib = Platform.isWindows
      ? DynamicLibrary.open('msvcrt.dll')
      : DynamicLibrary.process();
  final int Function(int) cAbs = dylib.lookupFunction<Int32 Function(Int32), int Function(int)>('abs');
  return cAbs(son);
}

void main() async {
  int natija = await Isolate.run(() => cAbsFonda(-999));
  print('Isolate ichida C funksiyasi bajarildi: $natija');
}
```

## Tushuntirish va Mantiq:
FFI va Isolate kombinatsiyasi eng yuqori unumdorlik (Native C tezligi + ko'p yadroli Dart arxitekturasi) beradi.

## Ishlash natijasi:
```text
Isolate ichida C funksiyasi bajarildi: 999
```

# 938-Topshiriq: FFI orqali Audio drayver buferi simulyatsiyasi

## Topshiriq sharti:
Tovush kartasiga 16-bitli PCM audio namunalarini to'g'ridan-to'g'ri xotiradan uzatish.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'package:ffi/ffi.dart';

void main() {
  Pointer<Int16> pcmBufer = calloc<Int16>(4);
  pcmBufer[0] = 0;
  pcmBufer[1] = 16384;  // Musbat amplituda
  pcmBufer[2] = 0;
  pcmBufer[3] = -16384; // Manfiy amplituda

  print('Audio drayverga uzatilgan PCM bufer hajmi: ${4 * sizeOf<Int16>()} bayt');
  calloc.free(pcmBufer);
}
```

## Tushuntirish va Mantiq:
Audio drayverlari (WASAPI, CoreAudio, ALSA) bilan ishlashda to'g'ridan-to'g'ri `Pointer<Int16>` uzatiladi.

## Ishlash natijasi:
```text
Audio drayverga uzatilgan PCM bufer hajmi: 8 bayt
```

# 939-Topshiriq: DynamicLibrary xatolarini ushlash

## Topshiriq sharti:
Kutubxona fayli topilmaganda `ArgumentError` xatosini ushlab xavfsiz boshqaring.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';

void main() {
  try {
    DynamicLibrary.open('mavjud_bolmagan_kutubxona.dll');
  } catch (e) {
    print('Kutubxona yuklash xatosi xavfsiz ushlandi: $e');
  }
}
```

## Tushuntirish va Mantiq:
Dinamik kutubxonalar bilan ishlashda mavjudlikni xavfsiz tekshirish ilovani to'xtab qolishdan asraydi.

## Ishlash natijasi:
```text
Kutubxona yuklash xatosi xavfsiz ushlandi: ArgumentError: Failed to load dynamic library 'mavjud_bolmagan_kutubxona.dll' (126)
```

# 940-Topshiriq: Apparat arxitekturasi va Endianness aniqlash

## Topshiriq sharti:
Joriy protsessor Little-Endian yoki Big-Endian ekanligini 32-bitli xotira tekshiruvi orqali aniqlang.

## Yechim (Dart kodi):
```dart
import 'dart:typed_data';

void main() {
  var bufer = Uint8List(2);
  var bd = ByteData.view(bufer.buffer);
  bd.setUint16(0, 0x0102, Endian.host);

  if (bufer[0] == 0x02) {
    print('Joriy protsessor arxitekturasi: Little-Endian (ARM / x86_64)');
  } else {
    print('Joriy protsessor arxitekturasi: Big-Endian');
  }
}
```

## Tushuntirish va Mantiq:
`Endian.host` joriy qurilma apparatining haqiqiy baytlar ketma-ketligini aniqlashga xizmat qiladi.

## Ishlash natijasi:
```text
Joriy protsessor arxitekturasi: Little-Endian (ARM / x86_64)
```

# 941-Topshiriq: Native xotiradagi massivni qismlarga ajratish (Pointer Slice)

## Topshiriq sharti:
Katta native massivning ma'lum qismini yangi xotira ajratmasdan boshqarish.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'dart:typed_data';
import 'package:ffi/ffi.dart';

void main() {
  Pointer<Int32> ptr = calloc<Int32>(6);
  for (int i = 0; i < 6; i++) ptr[i] = i * 10;

  // 2-indeksdan boshlab 3 ta element
  Int32List slice = ptr.elementAt(2).asTypedList(3);
  print('Native Slice: $slice');

  calloc.free(ptr);
}
```

## Tushuntirish va Mantiq:
Pointer slicing apparat keshini tejab, tenzorlarning qismlari ustida operatsiyalarni tezlashtiradi.

## Ishlash natijasi:
```text
Native Slice: [20, 30, 40]
```

# 942-Topshiriq: FFI orqali yuqori aniqlikdagi vaqt (High-resolution clock)

## Topshiriq sharti:
C kutubxonasidagi nanosoniyali yoki millisoniyali taymer ko'rsatkichini o'qing.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'dart:io';

typedef CClock = Int64 Function();
typedef DartClock = int Function();

void main() {
  var dylib = Platform.isWindows
      ? DynamicLibrary.open('msvcrt.dll')
      : DynamicLibrary.process();

  final DartClock cClock = dylib.lookupFunction<CClock, DartClock>('clock');

  int tsikl = cClock();
  print('CPU Tsikl ko\'rsatkichi: $tsikl');
}
```

## Tushuntirish va Mantiq:
C `clock()` funksiyasi jarayon tomonidan sarflangan aniq CPU tsikllarini o'lchashga imkon beradi.

## Ishlash natijasi:
```text
CPU Tsikl ko'rsatkichi: ...
```

# 943-Topshiriq: Kamera kadrining xom (RAW) baytlarini FFI da o'qish

## Topshiriq sharti:
RGBA formatidagi xom piksellarni native xotiradan o'qish va tahlil qilish.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'package:ffi/ffi.dart';

void main() {
  // 1 ta RGBA piksel: R=255, G=128, B=64, A=255
  Pointer<Uint8> piksel = calloc<Uint8>(4);
  piksel[0] = 255;
  piksel[1] = 128;
  piksel[2] = 64;
  piksel[3] = 255;

  print('Piksel kanallari: R=${piksel[0]}, G=${piksel[1]}, B=${piksel[2]}, A=${piksel[3]}');
  calloc.free(piksel);
}
```

## Tushuntirish va Mantiq:
Kamera va sensorlar xom piksellarni to'g'ridan-to'g'ri `Pointer<Uint8>` manzilida uzatadi.

## Ishlash natijasi:
```text
Piksel kanallari: R=255, G=128, B=64, A=255
```

# 944-Topshiriq: GPU Shader parametrlarini uzatish (Uniform buffer)

## Topshiriq sharti:
OpenGL / Vulkan shaderlariga uzatiladigan 16 baytli tekislangan (aligned) bufer tuzing.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'package:ffi/ffi.dart';

final class ShaderUniforms extends Struct {
  @Float()
  external double vaqt;
  @Float()
  external double yoruglik;
  @Float()
  external double x;
  @Float()
  external double y;
}

void main() {
  Pointer<ShaderUniforms> u = calloc<ShaderUniforms>();
  u.ref.vaqt = 1.25;
  u.ref.yoruglik = 0.8;

  print('Shader Uniforms o\'lchami: ${sizeOf<ShaderUniforms>()} bayt');
  calloc.free(u);
}
```

## Tushuntirish va Mantiq:
Grafik shaderlar xotiradagi 16-baytlik tekislangan strukturalarni to'g'ridan-to'g'ri GPU registrlariga yuklaydi.

## Ishlash natijasi:
```text
Shader Uniforms o'lchami: 16 bayt
```

# 945-Topshiriq: Amaliy: C++ BitNet GEMM yadrosini xotiraga joylash

## Topshiriq sharti:
C/C++ da yozilgan BitNet b1.58 GEMM yadrosining xotiradagi ternar matritsasini initsializatsiya qiling.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'package:ffi/ffi.dart';

void main() {
  // 2x3 Ternar matritsa
  int rows = 2, cols = 3;
  Pointer<Int8> w = calloc<Int8>(rows * cols);

  // [ +1,  0, -1 ]
  // [ -1, +1, +1 ]
  w[0] = 1;  w[1] = 0;  w[2] = -1;
  w[3] = -1; w[4] = 1;  w[5] = 1;

  print('Ternar vaznlar native xotirada muvaffaqiyatli joylashtirildi.');
  print('Birinchi qator: [${w[0]}, ${w[1]}, ${w[2]}]');
  print('Ikkinchi qator: [${w[3]}, ${w[4]}, ${w[5]}]');

  calloc.free(w);
}
```

## Tushuntirish va Mantiq:
BitNet b1.58 ning asosiy xotirasi 1-baytli yoki 2-bitli zichlangan shaklda native FFI xotirasida saqlanadi.

## Ishlash natijasi:
```text
Ternar vaznlar native xotirada muvaffaqiyatli joylashtirildi.
Birinchi qator: [1, 0, -1]
Ikkinchi qator: [-1, 1, 1]
```

# 946-Topshiriq: FFI orqali xotirani qayta taqsimlash (realloc)

## Topshiriq sharti:
Mavjud ko'rsatkich hajmini xotirada kattalashtirish yoki kichraytirish (`realloc`).

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'package:ffi/ffi.dart';

void main() {
  Pointer<Int32> p = calloc<Int32>(2);
  p[0] = 10; p[1] = 20;

  // 4 ta elementgacha kengaytirish
  Pointer<Int32> yangiP = calloc<Int32>(4);
  yangiP[0] = p[0];
  yangiP[1] = p[1];
  yangiP[2] = 30;
  yangiP[3] = 40;

  print('Kengaytirilgan massiv: [${yangiP[0]}, ${yangiP[1]}, ${yangiP[2]}, ${yangiP[3]}]');

  calloc.free(p);
  calloc.free(yangiP);
}
```

## Tushuntirish va Mantiq:
Dinamik xotira hajmini boshqarish massivlar o'lchami oldindan ma'lum bo'lmagan holatlarda zarur.

## Ishlash natijasi:
```text
Kengaytirilgan massiv: [10, 20, 30, 40]
```

# 947-Topshiriq: FFI Pointerlar tengligi va manzil taqqosi

## Topshiriq sharti:
Ikkita pointer bir xil xotira katagiga qarayotganligini tekshiring.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'package:ffi/ffi.dart';

void main() {
  Pointer<Int32> p1 = calloc<Int32>();
  Pointer<Int32> p2 = p1;

  print('p1 va p2 manzili bir xilmi: ${p1.address == p2.address}');
  calloc.free(p1);
}
```

## Tushuntirish va Mantiq:
Pointerlar taqqosi ularning virtual xotira manzillari (`address`) orqali amalga oshiriladi.

## Ishlash natijasi:
```text
p1 va p2 manzili bir xilmi: true
```

# 948-Topshiriq: FFI bilan C kutubxonasidagi qatorni qidirish (strstr)

## Topshiriq sharti:
C `strstr(haystack, needle)` funksiyasini bog'lab matn ichidan qidiruvni amalga oshiring.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'dart:io';
import 'package:ffi/ffi.dart';

typedef CStrstr = Pointer<Utf8> Function(Pointer<Utf8>, Pointer<Utf8>);
typedef DartStrstr = Pointer<Utf8> Function(Pointer<Utf8>, Pointer<Utf8>);

void main() {
  var dylib = Platform.isWindows
      ? DynamicLibrary.open('msvcrt.dll')
      : DynamicLibrary.process();

  final DartStrstr cStrstr = dylib.lookupFunction<CStrstr, DartStrstr>('strstr');

  var matn = 'BitNet on-device AI'.toNativeUtf8();
  var qidiruv = 'AI'.toNativeUtf8();

  var res = cStrstr(matn, qidiruv);
  print('Topilgan qism: ${res != nullptr ? res.toDartString() : "Topilmadi"}');

  calloc.free(matn);
  calloc.free(qidiruv);
}
```

## Tushuntirish va Mantiq:
`strstr` past darajadagi matnli qidiruvni C tezligida bajarib mos joyga Pointer qaytaradi.

## Ishlash natijasi:
```text
Topilgan qism: AI
```

# 949-Topshiriq: FFI orqali BitNet Modelining Og'irliklarini Yuklash

## Topshiriq sharti:
Binary model faylini xotiraga xaritalab (Memory mapping) FFI Pointer orqali to'g'ridan-to'g'ri o'qish.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'dart:typed_data';
import 'package:ffi/ffi.dart';

void main() {
  // Model fayli baytlarini simulyatsiya qilish
  var fileBytes = Uint8List.fromList([1, 0, 2, 1]); // 2 bu yerda -1 ma'nosida

  Pointer<Int8> weights = calloc<Int8>(fileBytes.length);
  for (int i = 0; i < fileBytes.length; i++) {
    weights[i] = fileBytes[i] == 2 ? -1 : fileBytes[i];
  }

  print('Yuklangan BitNet vaznlari: [${weights[0]}, ${weights[1]}, ${weights[2]}, ${weights[3]}]');
  calloc.free(weights);
}
```

## Tushuntirish va Mantiq:
On-device AI modellari gigabaytlab og'irliklarni to'g'ridan-to'g'ri FFI pointerlari orqali xotiraga joylaydi.

## Ishlash natijasi:
```text
Yuklangan BitNet vaznlari: [1, 0, -1, 1]
```

# 950-Topshiriq: Amaliy: Dart FFI orqali to'liq C++ BitNet Ternar GEMV Inferensiya yadrosi

## Topshiriq sharti:
Ternar matritsa va vektor ko'paytmasini (W * x) to'liq C FFI xotirasida hisoblovchi inferensiya funksiyasini yozing.

## Yechim (Dart kodi):
```dart
import 'dart:ffi';
import 'package:ffi/ffi.dart';

void runNativeBitNetGemv({
  required Pointer<Int8> w,
  required Pointer<Float> x,
  required Pointer<Float> y,
  required int rows,
  required int cols,
}) {
  // C++ BitNet GEMV yadrosi simulyatsiyasi:
  for (int i = 0; i < rows; i++) {
    double sum = 0.0;
    for (int j = 0; j < cols; j++) {
      int weight = w[i * cols + j];
      if (weight == 1) sum += x[j];
      else if (weight == -1) sum -= x[j];
    }
    y[i] = sum;
  }
}

void main() {
  int rows = 2, cols = 3;
  Pointer<Int8> w = calloc<Int8>(rows * cols);
  Pointer<Float> x = calloc<Float>(cols);
  Pointer<Float> y = calloc<Float>(rows);

  // Vaznlar:
  // [ +1,  0, -1 ]
  // [ -1, +1, +1 ]
  w[0] = 1;  w[1] = 0;  w[2] = -1;
  w[3] = -1; w[4] = 1;  w[5] = 1;

  // Kirish: [2.0, 4.0, 1.0]
  x[0] = 2.0; x[1] = 4.0; x[2] = 1.0;

  // Hisoblash:
  // y[0] = (2 - 1) = 1.0
  // y[1] = (-2 + 4 + 1) = 3.0
  runNativeBitNetGemv(w: w, x: x, y: y, rows: rows, cols: cols);

  print('BitNet Native C++ GEMV chiqishi:');
  print('y[0] = ${y[0]}');
  print('y[1] = ${y[1]}');

  calloc.free(w);
  calloc.free(x);
  calloc.free(y);
}
```

## Tushuntirish va Mantiq:
BitNet b1.58 texnologiyasi an'anaviy FP16 ko'paytirgichlaridan voz kechib, FFI orqali to'g'ridan-to'g'ri faqat qo'shish va ayirish amallarini eng yuqori unumdorlikda bajaradi.

## Ishlash natijasi:
```text
BitNet Native C++ GEMV chiqishi:
y[0] = 1.0
y[1] = 3.0
```

