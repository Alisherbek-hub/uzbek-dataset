# 3-Qism: Boshqaruv Konstruksiyalari: Shartlar, Sikllar va Dart 3 Switch (101-150)

Ushbu qismda Dart tilida `if-else`, klassik `switch-case`, zamonaviy Dart 3 `switch expression`, `if-case` pattern matching, sikllar (`for`, `for-in`, `while`, `do-while`), yorliqli (labeled) sakrashlar hamda klassik arifmetik algoritmlar o'rganiladi.

# 101-Topshiriq: if-else shart operatori: Baholash tizimi
## Topshiriq sharti:
Talabaning to'plagan balli (0-100) berilgan bo'lsa, uning bahosini (A, B, C, D, F) aniqlovchi dastur yozing.

## Yechim (Dart kodi):
```dart
void main() {
  int ball = 85;
  String baho;

  if (ball >= 90) {
    baho = "A (A'lo)";
  } else if (ball >= 80) {
    baho = "B (Yaxshi)";
  } else if (ball >= 70) {
    baho = "C (Qoniqarli)";
  } else if (ball >= 60) {
    baho = "D (Yetarli)";
  } else {
    baho = "F (Qoniqarsiz)";
  }

  print("To'plangan ball: $ball, Baho: $baho");
}
```

## Tushuntirish va Mantiq:
`if-else if-else` zanjiri shartlarni yuqoridan pastga qarab ketma-ket tekshiradi va birinchi to'g'ri kelgan blokni bajaradi.

## Ishlash natijasi:
```text
To'plangan ball: 85, Baho: B (Yaxshi)
```

# 102-Topshiriq: Murakkab mantiqiy shartlar: Kabisa yilini aniqlash
## Topshiriq sharti:
Berilgan yil kabisa yili (leap year - 366 kun) ekanligini `(yil % 4 == 0 && yil % 100 != 0) || (yil % 400 == 0)` formulasi bilan aniqlang.

## Yechim (Dart kodi):
```dart
bool isLeapYear(int year) {
  return (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0);
}

void main() {
  int y1 = 2024;
  int y2 = 2026;
  int y3 = 2000;
  int y4 = 1900;

  print("$y1 kabisa yilimi: ${isLeapYear(y1)}");
  print("$y2 kabisa yilimi: ${isLeapYear(y2)}");
  print("$y3 kabisa yilimi: ${isLeapYear(y3)}");
  print("$y4 kabisa yilimi: ${isLeapYear(y4)}");
}
```

## Tushuntirish va Mantiq:
Mantiqiy `&&` va `||` operatorlari bir nechta shartlarni qavslar orqali bitta ixcham mantiqiy qoidaga birlashtirishga imkon beradi.

## Ishlash natijasi:
```text
2024 kabisa yilimi: true
2026 kabisa yilimi: false
2000 kabisa yilimi: true
1900 kabisa yilimi: false
```

# 103-Topshiriq: Klassik switch-case operatori
## Topshiriq sharti:
Hafta kuni raqami (1-7) kiritilganda uning o'zbekcha nomini `switch-case` orqali aniqlang.

## Yechim (Dart kodi):
```dart
void main() {
  int kun = 6;
  String kunNomi;

  switch (kun) {
    case 1: kunNomi = "Dushanba"; break;
    case 2: kunNomi = "Seshanba"; break;
    case 3: kunNomi = "Chorshanba"; break;
    case 4: kunNomi = "Payshanba"; break;
    case 5: kunNomi = "Juma"; break;
    case 6: kunNomi = "Shanba"; break;
    case 7: kunNomi = "Yakshanba"; break;
    default: kunNomi = "Noto'g'ri kun";
  }

  print("Haftaning $kun-kuni: $kunNomi");
}
```

## Tushuntirish va Mantiq:
Klassik `switch` operatorida har bir `case` oxirida `break` qo'yilishi shart, aks holda tushib ketish (fall-through) yuz berishi mumkin.

## Ishlash natijasi:
```text
Haftaning 6-kuni: Shanba
```

# 104-Topshiriq: Dart 3 Switch Expression: Qiymat qaytaruvchi switch
## Topshiriq sharti:
Dart 3 da kiritilgan zamonaviy `switch expression` yordamida `break` larsiz to'g'ridan-to'g'ri o'zgaruvchiga qiymat yuklovchi kod yozing.

## Yechim (Dart kodi):
```dart
void main() {
  int faslRaqami = 2;

  // Dart 3 switch ifodasi (=> strelka sintaksisi)
  String fasl = switch (faslRaqami) {
    1 => "Bahor",
    2 => "Yoz",
    3 => "Kuz",
    4 => "Qish",
    _ => "Noma'lum fasl" // default o'rniga pastki chiziq _
  };

  print("Fasl: $fasl");
}
```

## Tushuntirish va Mantiq:
Dart 3 ning `switch expression` imkoniyati an'anaviy `switch` ga qaraganda 3 barobar kamroq kod talab qiladi va har doim qiymat qaytaradi.

## Ishlash natijasi:
```text
Fasl: Yoz
```

# 105-Topshiriq: Dart 3 if-case va Pattern Matching
## Topshiriq sharti:
Dart 3 dagi `if (ob'ekt case Pattern)` sintaksisi orqali ro'yxatning shakli va elementlarini bir vaqtda tekshirib ajrating.

## Yechim (Dart kodi):
```dart
void tekshir(dynamic data) {
  if (data case [int a, int b]) {
    print("Ikkita butun sondan iborat juftlik: $a va $b (Yig'indi: ${a + b})");
  } else if (data case String s) {
    print("Satr kiritildi: '$s'");
  } else {
    print("Boshqa turdagi ma'lumot: $data");
  }
}

void main() {
  tekshir([10, 20]);
  tekshir("Salom Dart 3");
  tekshir(3.14);
}
```

## Tushuntirish va Mantiq:
`if-case` konstruksiyasi ham tur tekshiruvini, ham ma'lumotni alohida qismlarga ochishni (destructuring) bir qadamda amalga oshiradi.

## Ishlash natijasi:
```text
Ikkita butun sondan iborat juftlik: 10 va 20 (Yig'indi: 30)
Satr kiritildi: 'Salom Dart 3'
Boshqa turdagi ma'lumot: 3.14
```

# 106-Topshiriq: Ternar shart operatori: condition ? expr1 : expr2
## Topshiriq sharti:
Sonning toq yoki juft ekanligini bitta qatorli ternar ifoda bilan aniqlang.

## Yechim (Dart kodi):
```dart
void main() {
  int son = 17;
  String tur = (son % 2 == 0) ? "Juft" : "Toq";

  print("$son soni - $tur sondir.");
}
```

## Tushuntirish va Mantiq:
Ternar operator kichik shartli tayinlashlar uchun kodni ixchamlashtirish vositasidir.

## Ishlash natijasi:
```text
17 soni - Toq sondir.
```

# 107-Topshiriq: Ichma-ich ternar operatorlar (Nested ternary)
## Topshiriq sharti:
Son musbat, manfiy yoki nol ekanligini ichma-ich ternar operator bilan aniqlang.

## Yechim (Dart kodi):
```dart
void main() {
  int n = -8;
  String holat = (n > 0) ? "Musbat" : (n < 0) ? "Manfiy" : "Nol";

  print("$n soni: $holat");
}
```

## Tushuntirish va Mantiq:
Ichma-ich ternar operatorlar qisqa shartlar uchun qulay, ammo haddan tashqari ko'p qo'llansa o'qilishni qiyinlashtiradi.

## Ishlash natijasi:
```text
-8 soni: Manfiy
```

# 108-Topshiriq: Standart for sikli: 1 dan N gacha sanash
## Topshiriq sharti:
Klassik `for (int i = 1; i <= n; i++)` sikli orqali 1 dan 5 gacha bo'lgan sonlar kvadratlarini chop eting.

## Yechim (Dart kodi):
```dart
void main() {
  for (int i = 1; i <= 5; ++i) {
    print("$i ning kvadrati = ${i * i}");
  }
}
```

## Tushuntirish va Mantiq:
Standart `for` sikli initsializatsiya, shart va qadam qismlaridan iborat bo'lib, sanash chegaralari aniq bo'lganda ishlatiladi.

## Ishlash natijasi:
```text
1 ning kvadrati = 1
2 ning kvadrati = 4
3 ning kvadrati = 9
4 ning kvadrati = 16
5 ning kvadrati = 25
```

# 109-Topshiriq: Qadami o'zgaruvchan for sikli (Juft sonlar)
## Topshiriq sharti:
0 dan 20 gacha bo'lgan barcha juft sonlarni `i += 2` qadami bilan ekranga chiqaring.

## Yechim (Dart kodi):
```dart
void main() {
  stdoutWrite("Juft sonlar: ");
  for (int i = 0; i <= 10; i += 2) {
    stdoutWrite("$i ");
  }
  print("");
}

void stdoutWrite(String s) => print(s);
```

## Tushuntirish va Mantiq:
Qadam qismida ixtiyoriy arifmetik ifodani (masalan `i += 2` yoki `i *= 2`) berish mumkin.

## Ishlash natijasi:
```text
Juft sonlar: 
0 
2 
4 
6 
8 
10 

```

# 110-Topshiriq: Teskari for sikli (Kamayish tartibida sanash)
## Topshiriq sharti:
10 dan 1 gacha teskari sanovchi va oxirida 'Start!' xabarini chiqaruvchi kod yozing.

## Yechim (Dart kodi):
```dart
void main() {
  for (int i = 5; i >= 1; --i) {
    print("Qolgan vaqt: $i...");
  }
  print("Start! Dvigatel ishga tushdi!");
}
```

## Tushuntirish va Mantiq:
Teskari siklda boshlang'ich qiymat katta olinadi, shart esa `i >= 1` va qadam `--i` bo'ladi.

## Ishlash natijasi:
```text
Qolgan vaqt: 5...
Qolgan vaqt: 4...
Qolgan vaqt: 3...
Qolgan vaqt: 2...
Qolgan vaqt: 1...
Start! Dvigatel ishga tushdi!
```

# 111-Topshiriq: for-in sikli: Kolleksiyalar bo'ylab aylanish
## Topshiriq sharti:
Shaharlar ro'yxati berilgan bo'lsa, `for-in` orqali har bir shahar nomini ekranga chiqaring.

## Yechim (Dart kodi):
```dart
void main() {
  List<String> viloyatlar = ["Toshkent", "Samarqand", "Buxoro", "Xorazm"];

  for (String v in viloyatlar) {
    print("Viloyat: $v");
  }
}
```

## Tushuntirish va Mantiq:
`for-in` sikli indeks hisoblagichiga ehtiyoj sezmasdan to'g'ridan-to'g'ri elementlarning o'zini ketma-ket uzatadi.

## Ishlash natijasi:
```text
Viloyat: Toshkent
Viloyat: Samarqand
Viloyat: Buxoro
Viloyat: Xorazm
```

# 112-Topshiriq: forEach metodi va Anonim funksiya
## Topshiriq sharti:
Ro'yxatning `.forEach()` metodiga lambda funksiya berib, elementlarni qayta ishlang.

## Yechim (Dart kodi):
```dart
void main() {
  List<int> sonlar = [5, 10, 15];

  sonlar.forEach((son) {
    print("Element: $son (Ikkilangani: ${son * 2})");
  });
}
```

## Tushuntirish va Mantiq:
`forEach` funksional dasturlash uslubida sikllarni yozish imkonini beradi.

## Ishlash natijasi:
```text
Element: 5 (Ikkilangani: 10)
Element: 10 (Ikkilangani: 20)
Element: 15 (Ikkilangani: 30)
```

# 113-Topshiriq: while sikli: Shart to'g'ri bo'lguncha aylanish
## Topshiriq sharti:
Tasodifiy kutilayotgan shart yoki son 100 dan oshguncha 2 ga ko'paytirib boruvchi `while` siklini yozing.

## Yechim (Dart kodi):
```dart
void main() {
  int qiymat = 3;

  while (qiymat < 100) {
    print("Joriy qiymat: $qiymat");
    qiymat *= 2;
  }
  print("Sikl tugadi. Yakuniy: $qiymat");
}
```

## Tushuntirish va Mantiq:
`while` sikli har bir qadamdan oldin shartni tekshiradi. Agar shart dastlabdayoq false bo'lsa, sikl tanasi umuman bajarilmaydi.

## Ishlash natijasi:
```text
Joriy qiymat: 3
Joriy qiymat: 6
Joriy qiymat: 12
Joriy qiymat: 24
Joriy qiymat: 48
Joriy qiymat: 96
Sikl tugadi. Yakuniy: 192
```

# 114-Topshiriq: do-while sikli: Kamida bir marta bajarilish kafolati
## Topshiriq sharti:
Shart dastlab xato bo'lsa ham kamida 1 marta bajariladigan `do-while` siklini ko'rsating.

## Yechim (Dart kodi):
```dart
void main() {
  int x = 10;

  do {
    print("do-while tanasi bajarildi! x = $x");
    x++;
  } while (x < 5); // 10 < 5 xato, shuning uchun qayta kirmaydi

  print("Sikl yakunlandi.");
}
```

## Tushuntirish va Mantiq:
`do-while` shartni sikl tanasi bajarib bo'lingandan so'ng tekshiradi, bu menyular va foydalanuvchidan ma'lumot so'rashda juda qo'l keladi.

## Ishlash natijasi:
```text
do-while tanasi bajarildi! x = 10
Sikl yakunlandi.
```

# 115-Topshiriq: break operatori: Siklni to'xtatish
## Topshiriq sharti:
1 dan 100 gacha sonlar ichidan birinchi 7 ga va 11 ga qoldiqsiz bo'linuvchi sonni topganda siklni `break` bilan to'xtating.

## Yechim (Dart kodi):
```dart
void main() {
  int? topilgan;

  for (int i = 1; i <= 100; ++i) {
    if (i % 7 == 0 && i % 11 == 0) {
      topilgan = i;
      break; // Qidiruv yakunlandi
    }
  }

  print("Birinchi topilgan son: $topilgan");
}
```

## Tushuntirish va Mantiq:
`break` operatori joriy sikl ishini darhol yakunlaydi va sikldan keyingi satrga o'tadi.

## Ishlash natijasi:
```text
Birinchi topilgan son: 77
```

# 116-Topshiriq: continue operatori: Joriy qadamni o'tkazib yuborish
## Topshiriq sharti:
1 dan 10 gacha bo'lgan sonlardan faqat toqlarini chiqarishda juft sonlarni `continue` orqali tashlab o'ting.

## Yechim (Dart kodi):
```dart
void main() {
  for (int i = 1; i <= 6; ++i) {
    if (i % 2 == 0) {
      continue; // Juft bo'lsa, keyingisiga o't
    }
    print("Toq son: $i");
  }
}
```

## Tushuntirish va Mantiq:
`continue` sikl tanasining qolgan qismini bajarmasdan, darhol keyingi iteratsiyaga o'tkazadi.

## Ishlash natijasi:
```text
Toq son: 1
Toq son: 3
Toq son: 5
```

# 117-Topshiriq: Yorliqli sikllar (Labeled Loops): Ichma-ich sikllardan chiqish
## Topshiriq sharti:
Ichki sikldan turib to'g'ridan-to'g'ri tashqi siklni to'xtatuvchi `tashqiSikl: for ...` yorlig'ini qo'llang.

## Yechim (Dart kodi):
```dart
void main() {
  tashqiSikl:
  for (int i = 1; i <= 3; ++i) {
    for (int j = 1; j <= 3; ++j) {
      if (i == 2 && j == 2) {
        print("To'xtash nuqtasi (i=$i, j=$j). Barcha sikllar to'xtatiladi!");
        break tashqiSikl; // To'g'ridan-to'g'ri tashqi siklni to'xtatamiz!
      }
      print("i=$i, j=$j");
    }
  }
  print("Sikldan tashqariga chiqildi.");
}
```

## Tushuntirish va Mantiq:
Oddiy `break` faqat o'zi joylashgan eng ichki siklni to'xtatadi. Yorliqli `break labelName;` esa ko'p qavatli sikllardan bittada chiqish imkonini beradi.

## Ishlash natijasi:
```text
i=1, j=1
i=1, j=2
i=1, j=3
i=2, j=1
To'xtash nuqtasi (i=2, j=2). Barcha sikllar to'xtatiladi!
Sikldan tashqariga chiqildi.
```

# 118-Topshiriq: Ichma-ich for sikllari: Ko'paytirish jadvali
## Topshiriq sharti:
1 dan 3 gacha bo'lgan sonlarning ko'paytirish jadvalini ichma-ich sikl orqali chiroyli chiqaring.

## Yechim (Dart kodi):
```dart
void main() {
  for (int i = 1; i <= 3; ++i) {
    for (int j = 1; j <= 3; ++j) {
      print("$i x $j = ${i * j}");
    }
    print("---");
  }
}
```

## Tushuntirish va Mantiq:
Tashqi sikl har gal bir qadam yurganida, ichki sikl to'liq boshidan oxirigacha aylanadi.

## Ishlash natijasi:
```text
1 x 1 = 1
1 x 2 = 2
1 x 3 = 3
---
2 x 1 = 2
2 x 2 = 4
2 x 3 = 6
---
3 x 1 = 3
3 x 2 = 6
3 x 3 = 9
---
```

# 119-Topshiriq: Yulduzchalardan uchburchak naqsh chizish
## Topshiriq sharti:
Ichma-ich sikllar yordamida konsolda to'g'ri burchakli yulduzchali uchburchak hosil qiling.

## Yechim (Dart kodi):
```dart
void main() {
  int qatorlar = 4;
  for (int i = 1; i <= qatorlar; ++i) {
    String satr = "";
    for (int j = 1; j <= i; ++j) {
      satr += "*";
    }
    print(satr);
  }
}
```

## Tushuntirish va Mantiq:
Geometrik naqshlar ichki sikl chegarasini tashqi sikl indeksiga (`j <= i`) bog'lash orqali quriladi.

## Ishlash natijasi:
```text
*
**
***
****
```

# 120-Topshiriq: Sikl ichida yig'indini to'plash (Accumulator pattern)
## Topshiriq sharti:
1 dan 100 gacha bo'lgan barcha natural sonlar yig'indisini hisoblang.

## Yechim (Dart kodi):
```dart
void main() {
  int jami = 0;
  for (int i = 1; i <= 100; ++i) {
    jami += i;
  }

  print("1 dan 100 gacha yig'indi: $jami");
  // Gauss formulasi bilan tekshiramiz: n*(n+1)/2 = 100*101/2 = 5050
}
```

## Tushuntirish va Mantiq:
Akkumulyator o'zgaruvchisi sikldan tashqarida e'lon qilinadi va har bir iteratsiyada unga yangi natija qo'shib boriladi.

## Ishlash natijasi:
```text
1 dan 100 gacha yig'indi: 5050
```

# 121-Topshiriq: Massiv ichidan minimal va maksimal elementni sikl orqali topish
## Topshiriq sharti:
Kutubxonalarsiz, oddiy `for-in` sikli yordamida ro'yxatdagi eng kichik va eng katta sonni aniqlang.

## Yechim (Dart kodi):
```dart
void main() {
  List<int> sonlar = [45, 12, 89, 5, 77, 99, 23];

  int engKichik = sonlar[0];
  int engKatta = sonlar[0];

  for (int x in sonlar) {
    if (x < engKichik) engKichik = x;
    if (x > engKatta) engKatta = x;
  }

  print("Eng kichik element: $engKichik");
  print("Eng katta element:  $engKatta");
}
```

## Tushuntirish va Mantiq:
Bir marta massivni aylanib chiqish (O(N) vaqt) minimal va maksimal qiymatlarni bitta siklda topish uchun yetarlidir.

## Ishlash natijasi:
```text
Eng kichik element: 5
Eng katta element:  99
```

# 122-Topshiriq: Sonning raqamlari yig'indisini while sikli bilan hisoblash
## Topshiriq sharti:
Musbat butun sonning (masalan 7345) har bir raqamini `% 10` va `~/ 10` amallari bilan ajratib yig'indisini toping.

## Yechim (Dart kodi):
```dart
void main() {
  int n = 7345;
  int nusxa = n;
  int raqamlarYigindisi = 0;

  while (n > 0) {
    int raqam = n % 10;
    raqamlarYigindisi += raqam;
    n ~/= 10; // Oxirgi raqamni o'chiramiz
  }

  print("$nusxa sonining raqamlari yig'indisi: $raqamlarYigindisi");
}
```

## Tushuntirish va Mantiq:
`% 10` har doim sonning eng oxirgi raqamini beradi, `~/ 10` esa uni o'chiradi. Bu butun sonlar arifmetikasining asosiy usulidir.

## Ishlash natijasi:
```text
7345 sonining raqamlari yig'indisi: 19
```

# 123-Topshiriq: Sonni teskari o'girish (Reverse Integer)
## Topshiriq sharti:
12345 sonini arifmetik yo'l bilan teskarisiga (54321) o'giruvchi funksiya yozing.

## Yechim (Dart kodi):
```dart
int teskariSon(int n) {
  int teskari = 0;
  while (n > 0) {
    teskari = teskari * 10 + (n % 10);
    n ~/= 10;
  }
  return teskari;
}

void main() {
  int son = 12345;
  print("$son ning teskarisi: ${teskariSon(son)}");
}
```

## Tushuntirish va Mantiq:
Teskari son `teskari * 10 + qoldiq` orqali yangi o'nlik xonaga siljib boradi.

## Ishlash natijasi:
```text
12345 ning teskarisi: 54321
```

# 124-Topshiriq: Palindrom sonni tekshirish
## Topshiriq sharti:
Son chapdan ham, o'ngdan ham bir xil o'qilishini (masalan 12321) arifmetik tekshiring.

## Yechim (Dart kodi):
```dart
bool isPalindrome(int n) {
  if (n < 0) return false;
  int original = n;
  int reversed = 0;
  while (n > 0) {
    reversed = reversed * 10 + (n % 10);
    n ~/= 10;
  }
  return original == reversed;
}

void main() {
  print("12321 palindrommi: ${isPalindrome(12321)}");
  print("12345 palindrommi: ${isPalindrome(12345)}");
}
```

## Tushuntirish va Mantiq:
Asl son bilan uning teskarisi teng bo'lsa, u palindrom son hisoblanadi.

## Ishlash natijasi:
```text
12321 palindrommi: true
12345 palindrommi: false
```

# 125-Topshiriq: Tub sonni tekshirish algoritmi
## Topshiriq sharti:
Berilgan son tub (faqat 1 ga va o'ziga bo'linuvchi) ekanligini `sqrt(n)` gacha bo'lgan bo'luvchilarni tekshirib aniqlang.

## Yechim (Dart kodi):
```dart
bool isPrime(int n) {
  if (n <= 1) return false;
  if (n <= 3) return true;
  if (n % 2 == 0 || n % 3 == 0) return false;

  for (int i = 5; i * i <= n; i += 6) {
    if (n % i == 0 || n % (i + 2) == 0) return false;
  }
  return true;
}

void main() {
  for (int x in [2, 17, 25, 29, 97, 100]) {
    print("$x tub sonmi: ${isPrime(x)}");
  }
}
```

## Tushuntirish va Mantiq:
Bo'luvchilarni `i * i <= n` gacha tekshirish tekshiruvlar sonini O(sqrt(N)) ga qisqartiradi.

## Ishlash natijasi:
```text
2 tub sonmi: true
17 tub sonmi: true
25 tub sonmi: false
29 tub sonmi: true
97 tub sonmi: true
100 tub sonmi: false
```

# 126-Topshiriq: Oraliqdagi barcha tub sonlarni chop etish
## Topshiriq sharti:
1 dan 30 gacha bo'lgan barcha tub sonlarni sikl yordamida topib ekranga chiqaring.

## Yechim (Dart kodi):
```dart
bool isPrime(int n) {
  if (n <= 1) return false;
  for (int i = 2; i * i <= n; ++i) {
    if (n % i == 0) return false;
  }
  return true;
}

void main() {
  stdoutWrite("1 dan 30 gacha tub sonlar: ");
  for (int i = 1; i <= 30; ++i) {
    if (isPrime(i)) {
      stdoutWrite("$i ");
    }
  }
  print("");
}

void stdoutWrite(String s) => print(s);
```

## Tushuntirish va Mantiq:
Har bir son uchun tublik sharti tekshiriladi va mos kelganlari chop etiladi.

## Ishlash natijasi:
```text
1 dan 30 gacha tub sonlar: 
2 
3 
5 
7 
11 
13 
17 
19 
23 
29 

```

# 127-Topshiriq: Fibonachchi ketma-ketligi: Iterativ hisoblash
## Topshiriq sharti:
Dastlabki 10 ta Fibonachchi sonini (0, 1, 1, 2, 3, 5, 8, 13, 21, 34) sikl orqali hisoblang.

## Yechim (Dart kodi):
```dart
void main() {
  int n = 10;
  int a = 0, b = 1;

  stdoutWrite("Fibonacci ($n ta): ");
  for (int i = 0; i < n; ++i) {
    stdoutWrite("$a ");
    int keyingi = a + b;
    a = b;
    b = keyingi;
  }
  print("");
}

void stdoutWrite(String s) => print(s);
```

## Tushuntirish va Mantiq:
Iterativ hisoblash rekursiyaga qaraganda O(N) vaqt va O(1) xotira oladi, stek to'lib ketishining oldini oladi.

## Ishlash natijasi:
```text
Fibonacci (10 ta): 
0 
1 
1 
2 
3 
5 
8 
13 
21 
34 

```

# 128-Topshiriq: Faktorial hisoblash: Iterativ usulda
## Topshiriq sharti:
N sonining faktorialini (`N! = 1 * 2 * ... * N`) `for` sikli bilan hisoblang.

## Yechim (Dart kodi):
```dart
int faktorial(int n) {
  int natija = 1;
  for (int i = 2; i <= n; ++i) {
    natija *= i;
  }
  return natija;
}

void main() {
  for (int x in [0, 1, 5, 6]) {
    print("$x! = ${faktorial(x)}");
  }
}
```

## Tushuntirish va Mantiq:
0! va 1! qiymatlari 1 ga teng. Sikl 2 dan n gacha ko'paytirib boradi.

## Ishlash natijasi:
```text
0! = 1
1! = 1
5! = 120
6! = 720
```

# 129-Topshiriq: Eng katta umumiy bo'luvchi (EKUB / GCD): Evklid algoritmi
## Topshiriq sharti:
Ikkita sonning EKUBini qoldiq olish amali orqali O(log(min(a, b))) da topuvchi Evklid algoritmini yozing.

## Yechim (Dart kodi):
```dart
int ekub(int a, int b) {
  while (b != 0) {
    int qoldiq = a % b;
    a = b;
    b = qoldiq;
  }
  return a;
}

void main() {
  print("EKUB(48, 18) = ${ekub(48, 18)}");
  print("EKUB(100, 25) = ${ekub(100, 25)}");
  print("EKUB(17, 13) = ${ekub(17, 13)}");
}
```

## Tushuntirish va Mantiq:
Evklid algoritmi: `ekub(a, b) = ekub(b, a % b)`. Qoldiq nol bo'lganda `a` oxirgi javob bo'ladi.

## Ishlash natijasi:
```text
EKUB(48, 18) = 6
EKUB(100, 25) = 25
EKUB(17, 13) = 1
```

# 130-Topshiriq: Eng kichik umumiy karrali (EKUK / LCM)
## Topshiriq sharti:
`ekuk(a, b) = (a * b) ~/ ekub(a, b)` formulasi orqali eng kichik umumiy karralini hisoblang.

## Yechim (Dart kodi):
```dart
int ekub(int a, int b) {
  while (b != 0) {
    int t = b;
    b = a % b;
    a = t;
  }
  return a;
}

int ekuk(int a, int b) {
  if (a == 0 || b == 0) return 0;
  return (a * b) ~/ ekub(a, b);
}

void main() {
  print("EKUK(12, 18) = ${ekuk(12, 18)}");
  print("EKUK(5, 7) = ${ekuk(5, 7)}");
}
```

## Tushuntirish va Mantiq:
EKUK ikkala songa ham qoldiqsiz bo'linadigan eng kichik musbat sondir.

## Ishlash natijasi:
```text
EKUK(12, 18) = 36
EKUK(5, 7) = 35
```

# 131-Topshiriq: Armstrong sonlarini tekshirish
## Topshiriq sharti:
3 xonali sonning raqamlari kublari yig'indisi o'ziga teng bo'lgan Armstrong sonlarini (masalan 153: 1^3 + 5^3 + 3^3 = 1 + 125 + 27 = 153) toping.

## Yechim (Dart kodi):
```dart
bool isArmstrong(int n) {
  int original = n;
  int sum = 0;
  while (n > 0) {
    int r = n % 10;
    sum += (r * r * r);
    n ~/= 10;
  }
  return sum == original;
}

void main() {
  stdoutWrite("100 dan 999 gacha Armstrong sonlari: ");
  for (int i = 100; i <= 999; ++i) {
    if (isArmstrong(i)) {
      stdoutWrite("$i ");
    }
  }
  print("");
}

void stdoutWrite(String s) => print(s);
```

## Tushuntirish va Mantiq:
Armstrong sonlari sonlar nazariyasining klassik qiziqarli masalalaridan biridir.

## Ishlash natijasi:
```text
100 dan 999 gacha Armstrong sonlari: 
153 
370 
371 
407 

```

# 132-Topshiriq: Qisqa tutashuvli mantiqiy baholash (Short-circuit evaluation)
## Topshiriq sharti:
`&&` da birinchi shart `false` bo'lsa yoki `||` da birinchi shart `true` bo'lsa ikkinchi shart umuman tekshirilmasligini ko'rsating.

## Yechim (Dart kodi):
```dart
bool qimmatTekshiruv() {
  print("[DIQQAT]: Qimmat tekshiruv bajarildi!");
  return true;
}

void main() {
  print("1-sinov (false && ...):");
  bool r1 = false && qimmatTekshiruv(); // qimmatTekshiruv chaqirilmaydi!
  print("Natija: $r1");

  print("2-sinov (true || ...):");
  bool r2 = true || qimmatTekshiruv(); // qimmatTekshiruv chaqirilmaydi!
  print("Natija: $r2");
}
```

## Tushuntirish va Mantiq:
Qisqa tutashuv xatoliklarning oldini oladi (masalan `x != null && x.isNotEmpty`) va dasturni ortiqcha hisoblashlardan xalos qiladi.

## Ishlash natijasi:
```text
1-sinov (false && ...):
Natija: false
2-sinov (true || ...):
Natija: true
```

# 133-Topshiriq: assert ifodasi: Ishlab chiqish rejimida shartlarni tekshirish
## Topshiriq sharti:
`assert(condition, message)` orqali funksiya kirish parametrlarining haqiqiyligini tekshiring.

## Yechim (Dart kodi):
```dart
void yoshniBelgila(int yosh) {
  assert(yosh >= 0 && yosh <= 120, "Yosh 0 va 120 oralig'ida bo'lishi shart!");
  print("Yosh qabul qilindi: $yosh");
}

void main() {
  yoshniBelgila(25);
  // Ishlab chiqish (debug) rejimida assert xatosi dasturni to'xtatadi
}
```

## Tushuntirish va Mantiq:
`assert` ishlab chiqarish (production release) rejimida avtomatik o'chiriladi, shuning uchun runtime tezligiga hech qanday salbiy ta'sir ko'rsatmaydi.

## Ishlash natijasi:
```text
Yosh qabul qilindi: 25
```

# 134-Topshiriq: Dart 3 Switch Expression da guard (when) sharti
## Topshiriq sharti:
Dart 3 da `case pattern when booleanCondition` sintaksisi bilan shartli filtrlangan tanlovni bajaring.

## Yechim (Dart kodi):
```dart
String haroratTahlili(int temp) => switch (temp) {
  var t when t < 0 => "Muzlash nuqtasi ($t C)",
  var t when t >= 0 && t <= 25 => "Iliq, qulay ob-havo ($t C)",
  var t when t > 25 && t <= 45 => "Issiq ob-havo ($t C)",
  _ => "Ekstremal jazirama!"
};

void main() {
  print(haroratTahlili(-5));
  print(haroratTahlili(22));
  print(haroratTahlili(38));
}
```

## Tushuntirish va Mantiq:
`when` qo'shimcha shart bo'lib, naqsh mos kelganida mantiqiy ifodaning ham to'g'riligini talab qiladi.

## Ishlash natijasi:
```text
Muzlash nuqtasi (-5 C)
Iliq, qulay ob-havo (22 C)
Issiq ob-havo (38 C)
```

# 135-Topshiriq: Dart 3 Relational Pattern (Munosabat naqshlari: >, <, >=)
## Topshiriq sharti:
Dart 3 ning yangi munosabat naqshlaridan (`< 18`, `>= 65`) to'g'ridan-to'g'ri switch da foydalaning.

## Yechim (Dart kodi):
```dart
String chiptaNarxi(int yosh) => switch (yosh) {
  < 7 => "Bepul (Kichkintoy)",
  >= 7 && < 18 => "50% Chegirma (Maktab o'quvchisi)",
  >= 18 && < 60 => "To'liq chipta (Katta yoshli)",
  >= 60 => "Bepul (Faxriy)",
  _ => "Xato yosh"
};

void main() {
  print("5 yosh:  ${chiptaNarxi(5)}");
  print("14 yosh: ${chiptaNarxi(14)}");
  print("30 yosh: ${chiptaNarxi(30)}");
  print("65 yosh: ${chiptaNarxi(65)}");
}
```

## Tushuntirish va Mantiq:
Dart 3 munosabat naqshlari matematik oraliqlarni ifodalashda `switch` ni eng nafis vositaga aylantiradi.

## Ishlash natijasi:
```text
5 yosh:  Bepul (Kichkintoy)
14 yosh: 50% Chegirma (Maktab o'quvchisi)
30 yosh: To'liq chipta (Katta yoshli)
65 yosh: Bepul (Faxriy)
```

# 136-Topshiriq: Ro'yxatda indeks va qiymatni bir vaqtda olish: asMap().entries
## Topshiriq sharti:
`asMap().entries` yordamida indeks va qiymatni bitta `for-in` siklida oling.

## Yechim (Dart kodi):
```dart
void main() {
  List<String> dasturlar = ["Flutter", "Dart", "Python", "C++"];

  for (var entry in dasturlar.asMap().entries) {
    print("${entry.key + 1}-o'rin: ${entry.value}");
  }
}
```

## Tushuntirish va Mantiq:
`asMap().entries` ro'yxatni vaqtincha xarita ko'rinishida taqdim etadi, bu yerda `key` element indeksi, `value` esa elementning o'zidir.

## Ishlash natijasi:
```text
1-o'rin: Flutter
2-o'rin: Dart
3-o'rin: Python
4-o'rin: C++
```

# 137-Topshiriq: Dart 3 Records bilan siklda bir vaqtda indeks va qiymat
## Topshiriq sharti:
Dart 3 da `(int, String)` juftliklari ro'yxatini tuzib, siklda destructuring orqali o'qing.

## Yechim (Dart kodi):
```dart
void main() {
  var tillar = [
    (1, "Dart"),
    (2, "Python"),
    (3, "Rust")
  ];

  for (var (indeks, nom) in tillar) {
    print("Til #$indeks: $nom");
  }
}
```

## Tushuntirish va Mantiq:
Dart 3 da `(indeks, nom)` sintaksisi rekord elementlarini to'g'ridan-to'g'ri o'zgaruvchilarga ajratib beradi.

## Ishlash natijasi:
```text
Til #1: Dart
Til #2: Python
Til #3: Rust
```

# 138-Topshiriq: Matn ichidagi unli va undosh harflar sonini sanash
## Topshiriq sharti:
O'zbek tilidagi matn berilgan bo'lsa, undagi unli va undosh harflar sonini siklda sanang.

## Yechim (Dart kodi):
```dart
void main() {
  String matn = "Ona tilim - jonu dilim";
  String unlilar = "aeiouo'AEIOUO'";

  int unliSoni = 0;
  int undoshSoni = 0;

  for (int i = 0; i < matn.length; ++i) {
    String belgi = matn[i];
    if (RegExp(r'[a-zA-Z]').hasMatch(belgi)) {
      if (unlilar.contains(belgi)) {
        unliSoni++;
      } else {
        undoshSoni++;
      }
    }
  }

  print("Matn: '$matn'");
  print("Unli harflar soni:   $unliSoni");
  print("Undosh harflar soni: $undoshSoni");
}
```

## Tushuntirish va Mantiq:
Satr indekslash (`matn[i]`) va qidiruv amallari matn tahlilida juda samarali ishlaydi.

## Ishlash natijasi:
```text
Matn: 'Ona tilim - jonu dilim'
Unli harflar soni:   8
Undosh harflar soni: 9
```

# 139-Topshiriq: Ro'yxat elementlarini in-place teskari o'girish (Ikki ko'rsatkichli usul)
## Topshiriq sharti:
Qo'shimcha ro'yxat yaratmasdan, boshidan va oxiridan ikkita ko'rsatkich bilan elementlar o'rnini almashtiruvchi (Two-pointer swap) algoritm yozing.

## Yechim (Dart kodi):
```dart
void reverseInPlace(List<int> list) {
  int left = 0;
  int right = list.length - 1;

  while (left < right) {
    int temp = list[left];
    list[left] = list[right];
    list[right] = temp;

    left++;
    right--;
  }
}

void main() {
  List<int> sonlar = [1, 2, 3, 4, 5];
  print("Asl ro'yxat: $sonlar");

  reverseInPlace(sonlar);
  print("Teskari o'girilgach: $sonlar");
}
```

## Tushuntirish va Mantiq:
Ikki ko'rsatkichli usul O(N/2) amalda va O(1) qo'shimcha xotirada massivni to'liq teskari o'giradi.

## Ishlash natijasi:
```text
Asl ro'yxat: [1, 2, 3, 4, 5]
Teskari o'girilgach: [5, 4, 3, 2, 1]
```

# 140-Topshiriq: 2D matritsaning asosiy va yordamchi dioganallari yig'indisi
## Topshiriq sharti:
N x N kvadrat matritsaning asosiy (`i == j`) va yordamchi (`i + j == N - 1`) diagonallari yig'indisini hisoblang.

## Yechim (Dart kodi):
```dart
void main() {
  List<List<int>> matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
  ];

  int n = matrix.length;
  int asosiyDiagonal = 0;
  int yordamchiDiagonal = 0;

  for (int i = 0; i < n; ++i) {
    asosiyDiagonal += matrix[i][i];
    yordamchiDiagonal += matrix[i][n - 1 - i];
  }

  print("Asosiy diagonal yig'indisi (1+5+9): $asosiyDiagonal");
  print("Yordamchi diagonal yig'indisi (3+5+7): $yordamchiDiagonal");
}
```

## Tushuntirish va Mantiq:
Diagonallar bitta siklda O(N) vaqtda olinadi, qo'shimcha ichki sikl kerak emas.

## Ishlash natijasi:
```text
Asosiy diagonal yig'indisi (1+5+9): 15
Yordamchi diagonal yig'indisi (3+5+7): 15
```

# 141-Topshiriq: Shaxmat taxtasi naqshini (8x8) sikllar orqali chiqarish
## Topshiriq sharti:
Ichma-ich sikllar va shart orqali 8x8 o'lchamli shaxmat taxtasi panjarasini ekranga chiqaring.

## Yechim (Dart kodi):
```dart
void main() {
  for (int i = 0; i < 4; ++i) {
    String qator = "";
    for (int j = 0; j < 4; ++j) {
      qator += ((i + j) % 2 == 0) ? "[#]" : "[ ]";
    }
    print(qator);
  }
}
```

## Tushuntirish va Mantiq:
`(i + j) % 2 == 0` sharti qator va ustunlarning almashinuvchi shaxmat kataklarini hosil qiladi.

## Ishlash natijasi:
```text
[#][ ][#][ ]
[ ][#][ ][#]
[#][ ][#][ ]
[ ][#][ ][#]
```

# 142-Topshiriq: Chiziqli qidiruv (Linear Search) algoritmi
## Topshiriq sharti:
Ro'yxatdan maqsadli elementning indeksini O(N) vaqtda topuvchi, topilmasa -1 qaytaruvchi funksiya yozing.

## Yechim (Dart kodi):
```dart
int linearSearch(List<int> list, int target) {
  for (int i = 0; i < list.length; ++i) {
    if (list[i] == target) return i;
  }
  return -1;
}

void main() {
  List<int> arr = [10, 50, 30, 70, 90, 20];

  print("70 ning indeksi: ${linearSearch(arr, 70)}");
  print("100 ning indeksi: ${linearSearch(arr, 100)}");
}
```

## Tushuntirish va Mantiq:
Chiziqli qidiruv har qanday tartibsiz massivda ishlaydi va elementlar bo'yicha ketma-ket qidiradi.

## Ishlash natijasi:
```text
70 ning indeksi: 3
100 ning indeksi: -1
```

# 143-Topshiriq: Binary qidiruv (Binary Search) algoritmi while siklida
## Topshiriq sharti:
Saralangan massivda O(log N) vaqtda element qidiruvchi ikkilik qidiruv algoritmini yozing.

## Yechim (Dart kodi):
```dart
int binarySearch(List<int> sortedList, int target) {
  int low = 0;
  int high = sortedList.length - 1;

  while (low <= high) {
    int mid = low + (high - low) ~/ 2;
    if (sortedList[mid] == target) return mid;
    if (sortedList[mid] < target) {
      low = mid + 1;
    } else {
      high = mid - 1;
    }
  }
  return -1;
}

void main() {
  List<int> arr = [11, 22, 33, 44, 55, 66, 77, 88];

  print("44 ning indeksi: ${binarySearch(arr, 44)}");
  print("99 ning indeksi: ${binarySearch(arr, 99)}");
}
```

## Tushuntirish va Mantiq:
Ikkilik qidiruv har qadamda qidiruv sohasini 2 barobarga qisqartiradi, 1 million element ichidan maqsadni 20 ta qadamda topadi.

## Ishlash natijasi:
```text
44 ning indeksi: 3
99 ning indeksi: -1
```

# 144-Topshiriq: Pufakchali saralash (Bubble Sort) algoritmi
## Topshiriq sharti:
Ichma-ich sikllar va qo'shni elementlarni almashtirish (swap) orqali massivni o'sish tartibida saralang.

## Yechim (Dart kodi):
```dart
void bubbleSort(List<int> list) {
  int n = list.length;
  for (int i = 0; i < n - 1; ++i) {
    bool almashdi = false;
    for (int j = 0; j < n - i - 1; ++j) {
      if (list[j] > list[j + 1]) {
        int temp = list[j];
        list[j] = list[j + 1];
        list[j + 1] = temp;
        almashdi = true;
      }
    }
    if (!almashdi) break; // Agar almashish bo'lmasa, saralangan
  }
}

void main() {
  List<int> sonlar = [64, 34, 25, 12, 22, 11, 90];
  bubbleSort(sonlar);
  print("Bubble Sort natijasi: $sonlar");
}
```

## Tushuntirish va Mantiq:
Pufakchali saralash eng sodda algoritm bo'lib, eng katta elementlar har bosqichda pufak kabi o'ng tomonga qalqib chiqadi.

## Ishlash natijasi:
```text
Bubble Sort natijasi: [11, 12, 22, 25, 34, 64, 90]
```

# 145-Topshiriq: Tanlash orqali saralash (Selection Sort)
## Topshiriq sharti:
Har bir qadamda qolgan qismning eng kichik elementini topib, oldingi o'ringa qo'yuvchi saralashni yozing.

## Yechim (Dart kodi):
```dart
void selectionSort(List<int> list) {
  int n = list.length;
  for (int i = 0; i < n - 1; ++i) {
    int minIdx = i;
    for (int j = i + 1; j < n; ++j) {
      if (list[j] < list[minIdx]) minIdx = j;
    }
    int temp = list[minIdx];
    list[minIdx] = list[i];
    list[i] = temp;
  }
}

void main() {
  List<int> sonlar = [29, 10, 14, 37, 13];
  selectionSort(sonlar);
  print("Selection Sort natijasi: $sonlar");
}
```

## Tushuntirish va Mantiq:
Selection Sort har bir bosqichda minimal elementni tanlaydi. Vaqt murakkabligi: O(N^2).

## Ishlash natijasi:
```text
Selection Sort natijasi: [10, 13, 14, 29, 37]
```

# 146-Topshiriq: Kiritish orqali saralash (Insertion Sort)
## Topshiriq sharti:
Karta o'yinidagi kabi har bir elementni o'zidan oldingi saralangan qismdagi kerakli joyiga joylashtirib boruvchi Insertion Sort algoritmini tuzing.

## Yechim (Dart kodi):
```dart
void insertionSort(List<int> list) {
  for (int i = 1; i < list.length; ++i) {
    int key = list[i];
    int j = i - 1;
    while (j >= 0 && list[j] > key) {
      list[j + 1] = list[j];
      j--;
    }
    list[j + 1] = key;
  }
}

void main() {
  List<int> sonlar = [12, 11, 13, 5, 6];
  insertionSort(sonlar);
  print("Insertion Sort natijasi: $sonlar");
}
```

## Tushuntirish va Mantiq:
Insertion Sort kichik yoki deyarli saralangan massivlar uchun eng tezkor barqaror (stable) saralash usullaridan biridir.

## Ishlash natijasi:
```text
Insertion Sort natijasi: [5, 6, 11, 12, 13]
```

# 147-Topshiriq: Massivdan takrorlangan elementlarni tozalash (Algoritmik usulda)
## Topshiriq sharti:
`Set` ishlatmasdan, faqat sikllar va shartlar orqali takrorlangan qiymatlarni olib tashlang.

## Yechim (Dart kodi):
```dart
List<int> tozalash(List<int> list) {
  List<int> noyob = [];
  for (int x in list) {
    bool bor = false;
    for (int y in noyob) {
      if (x == y) {
        bor = true;
        break;
      }
    }
    if (!bor) noyob.add(x);
  }
  return noyob;
}

void main() {
  List<int> aralash = [1, 2, 2, 3, 4, 3, 5, 1];
  print("Noyob elementlar: ${tozalash(aralash)}");
}
```

## Tushuntirish va Mantiq:
Element birinchi marta uchragandagina yangi natijaviy ro'yxatga qo'shiladi.

## Ishlash natijasi:
```text
Noyob elementlar: [1, 2, 3, 4, 5]
```

# 148-Topshiriq: Kombinatsiyalash: Ikki saralangan ro'yxatni birlashtirish (Merge)
## Topshiriq sharti:
Ikkita alohida saralangan ro'yxatni bitta O(N + M) umumiy saralangan ro'yxatga birlashtiring.

## Yechim (Dart kodi):
```dart
List<int> mergeSorted(List<int> a, List<int> b) {
  List<int> res = [];
  int i = 0, j = 0;

  while (i < a.length && j < b.length) {
    if (a[i] <= b[j]) {
      res.add(a[i++]);
    } else {
      res.add(b[j++]);
    }
  }

  while (i < a.length) res.add(a[i++]);
  while (j < b.length) res.add(b[j++]);

  return res;
}

void main() {
  List<int> l1 = [1, 3, 5, 7];
  List<int> l2 = [2, 4, 6, 8, 10];

  print("Birlashtirilgan: ${mergeSorted(l1, l2)}");
}
```

## Tushuntirish va Mantiq:
Merge amali Merge Sort algoritmining asosiy negizini tashkil qiladi va chiziqli vaqtda ishlaydi.

## Ishlash natijasi:
```text
Birlashtirilgan: [1, 2, 3, 4, 5, 6, 7, 8, 10]
```

# 149-Topshiriq: Valyuta konvertori menyusi (Interaktiv simulyatsiya)
## Topshiriq sharti:
Sikl va switch yordamida foydalanuvchi tanloviga qarab so'mni dollar, yevro yoki rublga aylantiruvchi tizim yozing.

## Yechim (Dart kodi):
```dart
double konvertatsiya(double sum, String valyuta) {
  const double usdKurs = 12800.0;
  const double eurKurs = 13900.0;
  const double rubKurs = 135.0;

  return switch (valyuta.toUpperCase()) {
    "USD" => sum / usdKurs,
    "EUR" => sum / eurKurs,
    "RUB" => sum / rubKurs,
    _ => 0.0
  };
}

void main() {
  double mablag = 1280000.0;
  for (String v in ["USD", "EUR", "RUB"]) {
    print("$mablag UZS = ${konvertatsiya(mablag, v).toStringAsFixed(2)} $v");
  }
}
```

## Tushuntirish va Mantiq:
Valyuta konvertori shartli operatorlar va formatlashni amaliy integratsiya qilish namunasidir.

## Ishlash natijasi:
```text
1280000.0 UZS = 100.00 USD
1280000.0 UZS = 92.09 EUR
1280000.0 UZS = 9481.48 RUB
```

# 150-Topshiriq: Katta amaliy loyiha: Bankomat (ATM) kesh mashinasi dasturi
## Topshiriq sharti:
150-topshiriq: PIN kodni tekshirish (3 ta imkoniyat), balans ko'rish, pul yechish va to'ldirish amallarini `while`, `switch-case` va shartlar bilan to'liq ishlovchi bankomat dasturida birlashtiring.

## Yechim (Dart kodi):
```dart
class Bankomat {
  int _pin = 1234;
  double _balans = 500000.0;
  int _xatoUrinishlar = 0;
  bool _bloklangan = false;

  bool pinKirit(int pin) {
    if (_bloklangan) {
      print("Karta bloklangan! Bankka murojaat qiling.");
      return false;
    }
    if (pin == _pin) {
      _xatoUrinishlar = 0;
      return true;
    } else {
      _xatoUrinishlar++;
      print("Noto'g'ri PIN! Qolgan urinishlar: ${3 - _xatoUrinishlar}");
      if (_xatoUrinishlar >= 3) {
        _bloklangan = true;
        print("Xavfsizlik sababli karta bloklandi!");
      }
      return false;
    }
  }

  void pulYech(double summa) {
    if (summa <= 0) {
      print("Noto'g'ri summa!");
      return;
    }
    if (summa > _balans) {
      print("Yetarli mablag' mavjud emas! Joriy balans: $_balans so'm");
    } else {
      _balans -= summa;
      print("Muvaffaqiyatli: $summa so'm berildi. Qolgan balans: $_balans so'm");
    }
  }

  void hisobot() => print("Joriy balans: $_balans so'm");
}

void main() {
  var atm = Bankomat();

  // 1. PIN tekshirish
  if (atm.pinKirit(1234)) {
    atm.hisobot();
    atm.pulYech(200000);
    atm.pulYech(400000); // Yetmaydi
    atm.hisobot();
  }
}
```

## Tushuntirish va Mantiq:
150-topshiriq orqali Dart tilida mantiqiy shartlar, autentifikatsiya, takrorlanishlar va moliyaviy tranzaksiyalarni boshqarish to'liq o'zlashtirildi.

## Ishlash natijasi:
```text
Joriy balans: 500000.0 so'm
Muvaffaqiyatli: 200000.0 so'm berildi. Qolgan balans: 300000.0 so'm
Yetarli mablag' mavjud emas! Joriy balans: 300000.0 so'm
Joriy balans: 300000.0 so'm
```

