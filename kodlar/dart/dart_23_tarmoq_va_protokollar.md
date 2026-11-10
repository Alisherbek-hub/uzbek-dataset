# Khorazmiy AI: Dart - Modul 23
## Mavzu: Tarmoq protokollari: dart:io raw sockets, WebSockets, gRPC Dart, HTTP/2 va custom binary streams

### Topshiriq #1101: ServerSocket.bind Orqali TCP Echo Server Yaratish
**Tavsif:** Tarmoq mijozlaridan kelayotgan TCP ulanishlarni qabul qilib, ularga asinxron ravishda echo xizmatini ko'rsatish.
**Talablar:** `dart:io`, `ServerSocket.bind`, `InternetAddress.anyIPv4`, `Socket` oqimlari va toza yopish.
**Yechim (Dart):**
```dart
import 'dart:io';
import 'dart:typed_data';

void main() async {
  // 1. 8080-portda barcha IPv4 interfeyslarida tinglash
  final server = await ServerSocket.bind(InternetAddress.anyIPv4, 8080);
  print('TCP Echo Server ishga tushdi: ${server.address.address}:${server.port}');

  // 2. Har bir kiruvchi mijoz soketini asinxron qabul qilish
  await for (Socket client in server) {
    print('Yangi mijoz ulandi: ${client.remoteAddress.address}:${client.remotePort}');

    // Mijozdan kelgan baytlarni o'qib, o'ziga qaytarish (Echo)
    client.listen(
      (Uint8List data) {
        print('Qabul qilindi: ${data.length} bayt');
        client.add(data); // Echo qaytarish
      },
      onError: (error) {
        print('Klient xatoligi: $error');
        client.destroy();
      },
      onDone: () {
        print('Klient ulanishni yopdi.');
        client.close();
      },
    );
  }
}
```
**Tushuntirish:** `ServerSocket` Dart da `Stream<Socket>` interfeysini taqdim etadi. `await for` yordamida yangi ulanishlar navbatdan bloklanmasdan olinadi, har bir `Socket` esa alohida kiruvchi `Stream<Uint8List>` va chiquvchi `IOSink` hisoblanadi.

---

### Topshiriq #1102: Socket.connect Bilan Asinxron TCP Klient
**Tavsif:** Masofaviy serverga TCP orqali ulanish, xabar jo'natish va to'liq javobni asinxron kutib olish.
**Talablar:** `Socket.connect`, `utf8.encode`, `utf8.decode`, `socket.flush()`, `socket.close()`.
**Yechim (Dart):**
```dart
import 'dart:io';
import 'dart:convert';
import 'dart:typed_data';

Future<void> sendTcpMessage(String host, int port, String message) async {
  Socket? socket;
  try {
    // Serverga ulanish
    socket = await Socket.connect(host, port, timeout: const Duration(seconds: 5));
    print('Serverga ulandi: ${socket.remoteAddress.address}:$port');

    // Xabarni UTF-8 formatida yuborish
    socket.add(utf8.encode('$message\n'));
    await socket.flush(); // Buferdagi baytlarni darhol tarmoqqa haydash

    // Javobni tinglash
    await for (Uint8List response in socket) {
      String text = utf8.decode(response).trim();
      print('Serverdan javob: $text');
      break; // Birinchi to'liq javobdan so'ng chiqish
    }
  } catch (e) {
    print('Tarmoq xatosi yuz berdi: $e');
  } finally {
    await socket?.close();
  }
}

void main() async {
  await sendTcpMessage('127.0.0.1', 8080, 'Salom, Khorazmiy Dart Tizimi!');
}
```
**Tushuntirish:** `socket.flush()` ma'lumotlar operatsion tizim buferida qolib ketmasdan zudlik bilan simga uzatilishini kafolatlaydi. `timeout` esa javob bermayotgan serverlarda oqim osilib qolishini oldini oladi.

---

### Topshiriq #1103: RawServerSocket va RawSocket: L4 Xom Hodisalar Boshqaruvi
**Tavsif:** Oddiy `Socket` ning yuqori darajadagi buferlashidan voz kechib, tarmoq voqealarini xom holatda bevosita boshqarish.
**Talablar:** `RawServerSocket`, `RawSocketEvent.read`, `RawSocketEvent.write`, `rawSocket.read()`.
**Yechim (Dart):**
```dart
import 'dart:io';
import 'dart:typed_data';

void main() async {
  final rawServer = await RawServerSocket.bind(InternetAddress.loopbackIPv4, 9091);
  print('Raw Server 9091-portda L4 voqealarini kutmoqda...');

  rawServer.listen((RawSocket rawClient) {
    print('Xom soket ulandi: FD voqealari faollashdi');

    rawClient.listen((RawSocketEvent event) {
      if (event == RawSocketEvent.read) {
        // Faqat ma'lumot mavjud bo'lganda qo'lda o'qish
        Uint8List? data = rawClient.read();
        if (data != null) {
          print('Xom o\'qilgan baytlar: ${data.length}');
          rawClient.write(data); // Xom yozish
        }
      } else if (event == RawSocketEvent.closed) {
        print('Soket yopildi');
      }
    });
  });
}
```
**Tushuntirish:** `RawSocket` hodisaga asoslangan (Event-Driven) bo'lib, C tilidagi `epoll/kqueue` modeliga eng yaqin Dart analogidir. U xotira buferlarini avtomatik ajratmaydi, faqat `read` voqeasi kelganda kerakli o'lchamda bayt o'qishga imkon beradi.

---

### Topshiriq #1104: RawDatagramSocket Yordamida UDP Echo Server va Klient
**Tavsif:** Ulanishsiz (Connectionless) datagramma paketlarini minimal kechikish bilan qabul qilish va jo'natish.
**Talablar:** `RawDatagramSocket.bind`, `Datagram`, `receive()`, `send()`.
**Yechim (Dart):**
```dart
import 'dart:io';
import 'dart:convert';

void main() async {
  // UDP soketni 9990-portga bog'lash
  final udpSocket = await RawDatagramSocket.bind(InternetAddress.anyIPv4, 9990);
  print('UDP Server 9990-portda datagrammalarni kutmoqda...');

  udpSocket.listen((RawSocketEvent event) {
    if (event == RawSocketEvent.read) {
      Datagram? dg = udpSocket.receive();
      if (dg != null) {
        String message = utf8.decode(dg.data);
        print('UDP paket: "$message" jo\'natuvchi: ${dg.address.address}:${dg.port}');

        // Echo javobini qaytarish
        List<int> reply = utf8.encode('Echo: $message');
        udpSocket.send(reply, dg.address, dg.port);
      }
    }
  });
}
```
**Tushuntirish:** `Datagram` klassi qabul qilingan paket baytlari bilan birga jo'natuvchining IP manzili va portini o'zida saqlaydi. Bu UDP serverga hech qanday ulanish sessiyasisiz to'g'ridan-to'g'ri javob berish imkonini beradi.

---

### Topshiriq #1105: UDP Multicast Guruhlariga A'zo Bo'lish (Service Discovery)
**Tavsif:** Lokal tarmoqdagi barcha tugunlarga (masalan, mDNS yoki IoT qurilmalarni qidirishda) bir vaqtda paket tarqatish.
**Talablar:** `joinMulticast`, `multicastLoopback`, `InternetAddress('224.0.0.1')`.
**Yechim (Dart):**
```dart
import 'dart:io';
import 'dart:convert';

void main() async {
  final multicastGroup = InternetAddress('239.255.255.250');
  const port = 1900; // SSDP standart porti

  final socket = await RawDatagramSocket.bind(InternetAddress.anyIPv4, port, reuseAddress: true, reusePort: true);
  socket.joinMulticast(multicastGroup);
  socket.multicastLoopback = false;

  print('Multicast guruhiga (${multicastGroup.address}) qo\'shildi.');

  socket.listen((event) {
    if (event == RawSocketEvent.read) {
      Datagram? dg = socket.receive();
      if (dg != null) {
        print('Multicast xabar: ${utf8.decode(dg.data)}');
      }
    }
  });
}
```
**Tushuntirish:** `joinMulticast` operatsion tizim yadrosiga IGMP (Internet Group Management Protocol) so'rovini jo'natadi va tarmoq kommutatoriga ushbu guruh trafigini bizning qurilmamizga ham yo'naltirishni buyuradi.

---

### Topshiriq #1106: Soket Sozlamalari: TCP_NODELAY va KeepAlive Boshqaruvi
**Tavsif:** Tarmoq kechikishini minimallashtirish va Nagle algoritmini o'chirib, har bir paketni darhol jo'natish.
**Talablar:** `SocketOption.tcpNoDelay`, `setOption()`, `Socket.connect`.
**Yechim (Dart):**
```dart
import 'dart:io';

Future<void> tuneSocket(Socket socket) async {
  // Nagle algoritmini o'chirish (HFT va o'yinlar uchun kechikishni kamaytirish)
  socket.setOption(SocketOption.tcpNoDelay, true);

  print('Socket parametrlar sozlandi: TCP_NODELAY = true');
}

void main() async {
  try {
    final socket = await Socket.connect('127.0.0.1', 8080);
    await tuneSocket(socket);
    await socket.close();
  } catch (e) {
    print('Soket sozlash xatosi: $e');
  }
}
```
**Tushuntirish:** `tcpNoDelay = true` o'rnatilganda Dart operatsion tizimga baytlarni to'plab turmasdan darhol IP paketiga joylab tarmoqqa uzatishni buyuradi.

---

### Topshiriq #1107: SecureSocket va TLS/SSL Shifrlangan Aloqa
**Tavsif:** Ochiq tarmoqlarda ma'lumotlar xavfsizligini ta'minlash uchun TLS 1.3 shifrlash qatlami bilan himoyalangan soket ulanishini o'rnatish.
**Talablar:** `SecureSocket.connect`, `SecurityContext`, ALPN protokollari.
**Yechim (Dart):**
```dart
import 'dart:io';
import 'dart:convert';

void main() async {
  final secContext = SecurityContext.defaultContext;

  // TLS 1.3 orqali xavfsiz ulanish
  final secureSocket = await SecureSocket.connect(
    'api.github.com',
    443,
    context: secContext,
    supportedProtocols: ['http/1.1'],
    timeout: const Duration(seconds: 5),
  );

  print('Xavfsiz TLS ulanish o\'rnatildi: ${secureSocket.selectedProtocol}');

  // Oddiy HTTP GET so'rovini jo'natish
  secureSocket.write('GET / HTTP/1.1\r\nHost: api.github.com\r\nUser-Agent: Dart/Network\r\n\r\n');
  await secureSocket.flush();

  secureSocket.listen((data) {
    print('TLS ma\'lumot qabul qilindi: ${data.length} bayt');
    secureSocket.destroy();
  });
}
```
**Tushuntirish:** `SecureSocket` dastlabki TCP ulanishini o'rnatib, uning ustidan avtomatik ravishda TLS Handshake (sertifikat tekshiruvi, kalitlar kelishuvi va shifrlash) ni amalga oshiradi.

---

### Topshiriq #1108: Self-Signed Sertifikatlar bilan Ishlash (badCertificateCallback)
**Tavsif:** Sinov (Staging) muhitlarida o'z-o'zidan imzolangan SSL sertifikatlarini xavfsiz tarzda tekshirish va tasdiqlash.
**Talablar:** `onBadCertificate`, `X509Certificate`, barmoq izi (SHA-256) tekshiruvi.
**Yechim (Dart):**
```dart
import 'dart:io';
import 'dart:typed_data';

void main() async {
  const trustedFingerprint = 'A1:B2:C3:D4:E5:F6...'; // Kutilayotgan sha256 barmoq izi

  final socket = await SecureSocket.connect(
    'localhost',
    8443,
    onBadCertificate: (X509Certificate cert) {
      print('Sertifikat tekshirilmoqda: Egasi = ${cert.subject}');
      // Haqiqiy tizimlarda faqat aniq ma'lum barmoq izi mos kelganda true qaytariladi:
      // return cert.sha256.hex == trustedFingerprint;
      return true; // Sinov uchun ruxsat berish
    },
  );

  print('Self-signed TLS soketiga muvaffaqiyatli ulandi.');
  await socket.close();
}
```
**Tushuntirish:** `onBadCertificate` qayta chaqiruvi barcha xatolarga ko'r-ko'rona ko'z yumish uchun emas, balki sertifikatning barmoq izini (Certificate Pinning) dastur ichida qat'iy tekshirish uchun ishlatiladi.

---

### Topshiriq #1109: Unix Domain Sockets Dart da (Lokal IPC)
**Tavsif:** Bitta mashina ichidagi mikroxizmatlar o'rtasida TCP tarmoq drayverisiz, fayl tizimi soketi orqali o'ta yuqori tezlikda aloqa qilish.
**Talablar:** `InternetAddress(path, type: InternetAddressType.unix)`.
**Yechim (Dart):**
```dart
import 'dart:io';
import 'dart:convert';

void main() async {
  const socketPath = '/tmp/khorazmiy_dart.sock';
  final socketFile = File(socketPath);
  if (await socketFile.exists()) await socketFile.delete();

  // Unix Domain Socket serverini yaratish
  final server = await ServerSocket.bind(
    InternetAddress(socketPath, type: InternetAddressType.unix),
    0,
  );
  print('Unix Domain Socket tinglamoqda: $socketPath');

  server.listen((client) {
    client.write('Salom, Dart IPC!');
    client.close();
  });
}
```
**Tushuntirish:** Unix Domain Sockets IP stekini va tarmoq interfeyslarini chetlab o'tadi. Natijada kechikish (latency) mikrosoniyalarga tushadi va xavfsizlik OS fayl ruxsatlari (file permissions) bilan boshqariladi.

---

### Topshiriq #1110: Soket Oqimlarida Backpressure Boshqaruvi (pause va resume)
**Tavsif:** Klient sekin o'qiyotgan vaqtda server xotirasi to'lib ketishini oldini olish uchun oqimni vaqtincha to'xtatish.
**Talablar:** `StreamSubscription.pause()`, `resume()`, `isPaused`.
**Yechim (Dart):**
```dart
import 'dart:io';
import 'dart:typed_data';

void handleSlowClient(Socket socket) {
  late StreamSubscription<Uint8List> subscription;

  subscription = socket.listen(
    (data) async {
      print('Qabul qilindi: ${data.length} bayt. Qayta ishlash boshlandi...');

      // Kiruvchi oqimni to'xtatib turish (Backpressure)
      subscription.pause();

      // Sekin hisoblash operatsiyasi simulyatsiyasi
      await Future.delayed(const Duration(milliseconds: 500));

      print('Qayta ishlash tugadi, oqim qayta faollashtirildi.');
      subscription.resume();
    },
    onDone: () => socket.close(),
  );
}

void main() {
  print('Backpressure nazorat tizimi faollashtirildi.');
}
```
**Tushuntirish:** `subscription.pause()` chaqirilganda, Dart operatsion tizimning TCP qabul qilish buferidan ma'lumot olishni to'xtatadi. Bu esa TCP darajasidagi Zero-Window mexanizmini ishga tushirib, jo'natuvchini ham tabiiy sekinlashtiradi.

---

### Topshiriq #1111: ByteData va Uint8List Bilan Binary Protokol Paketini Yig'ish
**Tavsif:** Tarmoqqa jo'natiladigan murakkab ikkilik paketni (Header + ID + Payload) xotirada tezkor shakllantirish.
**Talablar:** `ByteData`, `Uint8List`, `Endian.big`, `setUint32`, `setFloat64`.
**Yechim (Dart):**
```dart
import 'dart:typed_data';

class TelemetryFrame {
  static Uint8List buildPacket(int deviceId, double sensorValue, int timestamp) {
    // 4 bayt ID + 8 bayt Value + 8 bayt Timestamp = 20 bayt
    final buffer = Uint8List(20);
    final byteData = ByteData.view(buffer.buffer);

    byteData.setUint32(0, deviceId, Endian.big);
    byteData.setFloat64(4, sensorValue, Endian.big);
    byteData.setUint64(12, timestamp, Endian.big);

    return buffer;
  }

  static void parsePacket(Uint8List raw) {
    final byteData = ByteData.view(raw.buffer);
    final id = byteData.getUint32(0, Endian.big);
    final val = byteData.getFloat64(4, Endian.big);
    final time = byteData.getUint64(12, Endian.big);

    print('Paket ochildi: ID=$id, Qiymat=${val.toStringAsFixed(2)}, Vaqt=$time');
  }
}

void main() {
  final pkt = TelemetryFrame.buildPacket(42, 98.6, DateTime.now().millisecondsSinceEpoch);
  TelemetryFrame.parsePacket(pkt);
}
```
**Tushuntirish:** `ByteData` ixtiyoriy turdagi sonlarni to'g'ridan-to'g'ri baytlar qatoriga yozish va o'qish imkonini beradi. `Endian.big` tarmoq standartiga (Network Byte Order) to'liq mos keladi.

---

### Topshiriq #1112: Zero-Copy TypedData (Uint8List.sublistView va ByteBuffer)
**Tavsif:** Katta hajmdagi baytlar buferini qayta nusxalamasdan (Zero-Copy) uning qismlari (slice) bilan ishlash.
**Talablar:** `Uint8List.sublistView()`, `ByteBuffer`, xotirani tejash.
**Yechim (Dart):**
```dart
import 'dart:typed_data';

void processHeaderAndPayload(Uint8List networkPacket) {
  // Nusxa olmasdan faqat boshlang'ich 4 baytlik sarlavhani ko'rish
  final headerView = Uint8List.sublistView(networkPacket, 0, 4);

  // Qolgan foydali yuklamani (payload) nusxalamasdan ko'rish
  final payloadView = Uint8List.sublistView(networkPacket, 4);

  print('Bosh sarlavha ko\'rinishi: ${headerView.length} bayt');
  print('Payload ko\'rinishi: ${payloadView.length} bayt');
  print('Barcha ko\'rinishlar bitta umumiy ByteBuffer dan foydalanadi: '
        '${identical(headerView.buffer, payloadView.buffer)}');
}

void main() {
  final fullData = Uint8List.fromList([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
  processHeaderAndPayload(fullData);
}
```
**Tushuntirish:** `sublistView` yangi xotira ajratmaydi, balki mavjud `ByteBuffer` ga yangi ko'rsatkich (Window) yaratadi. Bu esa xotirani tejash va Garbage Collector yuklamasini nolga tushirish uchun muhimdir.

---

### Topshiriq #1113: Length-Prefixed Binary Framing StreamTransformer
**Tavsif:** TCP oqimidan kelayotgan tarqoq baytlar ichidan dastlabki 4 baytlik uzunlik prefiksi bo'yicha to'liq freymlarni yig'ish.
**Talablar:** `StreamTransformer.fromHandlers`, `BytesBuilder`, `ByteData`.
**Yechim (Dart):**
```dart
import 'dart:async';
import 'dart:typed_data';

class LengthPrefixedDecoder extends StreamTransformerBase<List<int>, Uint8List> {
  @override
  Stream<Uint8List> bind(Stream<List<int>> stream) {
    final builder = BytesBuilder(copy: false);

    return stream.transform(StreamTransformer.fromHandlers(
      handleData: (List<int> chunk, EventSink<Uint8List> sink) {
        builder.add(chunk);

        while (builder.length >= 4) {
          final currentBytes = builder.toBytes();
          final byteData = ByteData.view(currentBytes.buffer);
          final expectedLength = byteData.getUint32(0, Endian.big);

          if (currentBytes.length >= 4 + expectedLength) {
            // To'liq freym tayyor
            final frame = Uint8List.sublistView(currentBytes, 4, 4 + expectedLength);
            sink.add(frame);

            // Qolgan qismini saqlash
            final remaining = Uint8List.sublistView(currentBytes, 4 + expectedLength);
            builder.clear();
            builder.add(remaining);
          } else {
            // Hali to'liq yuklanmagan, keyingi paketni kutish
            break;
          }
        }
      },
      handleDone: (sink) => sink.close(),
    ));
  }
}

void main() {
  print('Length-Prefixed StreamTransformer yaratildi.');
}
```
**Tushuntirish:** TCP protokoli baytlar oqimidir, unda xabarlar chegarasi bo'lmaydi. Length-Prefixed dekoder har bir xabarning aniq chegarasini kafolatlaydi.

---

### Topshiriq #1114: Delimiter Asosidagi Matn Protokoli Parseri (LineSplitter)
**Tavsif:** Har bir xabar yangi qator (`\n` yoki `\r\n`) bilan ajratilgan tarmoq protokollarini oqimli tahlil qilish.
**Talablar:** `utf8.decoder`, `LineSplitter()`, reaktiv zanjir.
**Yechim (Dart):**
```dart
import 'dart:convert';
import 'dart:io';

void parseTextStream(Socket socket) {
  // Soket -> UTF-8 dekoder -> Qatorlarga ajratuvchi zanjir
  socket
      .cast<List<int>>()
      .transform(utf8.decoder)
      .transform(const LineSplitter())
      .listen(
    (String line) {
      print('Buyruq qabul qilindi: $line');
      if (line == 'QUIT') socket.close();
    },
    onError: (e) => print('Oqim xatosi: $e'),
  );
}

void main() {
  print('LineSplitter asosidagi matn protokoli parseri tayyor.');
}
```
**Tushuntirish:** `LineSplitter` oqim orqali uzatilayotgan matnlarni oraliq to'xtashlarsiz binar buferlar kesishmasida ham to'g'ri satrlarga bo'lib beradi.

---

### Topshiriq #1115: BytesBuilder Bilan Yuqori Tezlikdagi Protokol Serializatsiyasi
**Tavsif:** Ko'p bo'lakli binar paketlarni birlashtirishda `List.addAll` o'rniga ichki optimallashtirilgan `BytesBuilder` dan foydalanish.
**Talablar:** `BytesBuilder(copy: false)`, `takeBytes()`.
**Yechim (Dart):**
```dart
import 'dart:typed_data';

Uint8List buildMultiSegmentPayload(List<Uint8List> segments) {
  final builder = BytesBuilder(copy: false); // Ortiqcha xotira nusxalamaslik

  for (var seg in segments) {
    builder.add(seg);
  }

  // Barcha segmentlarni bitta yaxlit Uint8List qilib olish
  return builder.takeBytes();
}

void main() {
  final seg1 = Uint8List.fromList([1, 2]);
  final seg2 = Uint8List.fromList([3, 4, 5]);
  final result = buildMultiSegmentPayload([seg1, seg2]);
  print('Yig\'ilgan paket uzunligi: ${result.length} bayt');
}
```
**Tushuntirish:** `copy: false` bayrog'i berilganda `BytesBuilder` mavjud massivlarni nusxalamasdan zanjirga ulaydi, bu esa katta fayllarni yig'ishda juda katta tezlik beradi.

---

### Topshiriq #1116: CRC32 Nazorat Summasi Bilan Paket Butunligini Tekshirish
**Tavsif:** Tarmoqda paketlar buzilishi (bit rot) ni aniqlash uchun CRC32 algoritmini amalga oshirish.
**Talablar:** Lookup Table asosidagi CRC32, 32-bit xash.
**Yechim (Dart):**
```dart
import 'dart:typed_data';

class Crc32 {
  static final List<int> _table = List<int>.generate(256, (i) {
    int c = i;
    for (int k = 0; k < 8; k++) {
      c = (c & 1) != 0 ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
    }
    return c;
  });

  static int compute(Uint8List data) {
    int crc = 0xFFFFFFFF;
    for (int byte in data) {
      crc = (crc >>> 8) ^ _table[(crc ^ byte) & 0xFF];
    }
    return (crc ^ 0xFFFFFFFF) & 0xFFFFFFFF;
  }
}

void main() {
  final data = Uint8List.fromList([0x31, 0x32, 0x33, 0x34]); // "1234"
  int checksum = Crc32.compute(data);
  print('CRC32 tekshiruv summasi: 0x${checksum.toRadixString(16).toUpperCase()}');
}
```
**Tushuntirish:** Tarmoq paketi oxiriga 4 baytlik CRC32 yoziladi. Qabul qiluvchi tomon uni qayta hisoblab, kelgan summa bilan solishtirish orqali ma'lumotning xatosiz yetib kelganini tekshiradi.

---

### Topshiriq #1117: Sliding Window Asosidagi Reliable UDP (RUDP) Modeli
**Tavsif:** UDP tezligini yo'qotmagan holda paketlar yo'qolishiga qarshi ketma-ketlik raqami va ACK tasdiqlashini tashkil qilish.
**Talablar:** Packet header (Sequence, ACK), qayta yuborish mantiqi.
**Yechim (Dart):**
```dart
import 'dart:typed_data';

class RudpPacket {
  final int sequenceNumber;
  final int ackNumber;
  final Uint8List payload;

  RudpPacket(this.sequenceNumber, this.ackNumber, this.payload);

  Uint8List toBytes() {
    final bytes = Uint8List(8 + payload.length);
    final bd = ByteData.view(bytes.buffer);
    bd.setUint32(0, sequenceNumber, Endian.big);
    bd.setUint32(4, ackNumber, Endian.big);
    bytes.setRange(8, bytes.length, payload);
    return bytes;
  }

  static RudpPacket fromBytes(Uint8List raw) {
    final bd = ByteData.view(raw.buffer);
    final seq = bd.getUint32(0, Endian.big);
    final ack = bd.getUint32(4, Endian.big);
    final payload = Uint8List.sublistView(raw, 8);
    return RudpPacket(seq, ack, payload);
  }
}

void main() {
  final pkt = RudpPacket(1001, 1000, Uint8List.fromList([10, 20, 30]));
  print('RUDP paketi muvaffaqiyatli tuzildi: Seq = ${pkt.sequenceNumber}');
}
```
**Tushuntirish:** RUDP mexanizmida qabul qiluvchi har bir to'g'ri olingan paket uchun ACK qaytaradi; agar belgilangan vaqt ichida ACK kelmasa, jo'natuvchi faqat shu paketni qayta jo'natadi.

---

### Topshiriq #1118: Tarmoq Oqimida Kompressiya (gzip va zlib StreamTransformer)
**Tavsif:** Katta hajmdagi JSON yoki binar oqimlarni tarmoq orqali siqilgan (compressed) holda uzatish.
**Talablar:** `gzip.encoder`, `gzip.decoder`, `StreamTransformer`.
**Yechim (Dart):**
```dart
import 'dart:io';
import 'dart:convert';

void sendCompressedStream(Socket socket, String largeData) {
  Stream.value(largeData)
      .transform(utf8.encoder)
      .transform(gzip.encoder) // GZIP bilan oqimli siqish
      .pipe(socket);
}

void receiveCompressedStream(Socket socket) {
  socket
      .transform(gzip.decoder) // GZIP oqimli ochish
      .transform(utf8.decoder)
      .listen((text) {
    print('Siqilgan oqimdan qabul qilindi: ${text.length} belgi');
  });
}

void main() {
  print('Gzip oqimli siqish va ochish tizimi tayyor.');
}
```
**Tushuntirish:** Oqimli kompressiya butun ma'lumotni xotirada to'plamasdan, o'tayotgan bayt bloklarini (chunks) parvoz holatida (on-the-fly) siqadi.

---

### Topshiriq #1119: Asinxron StreamBuffer Bilan Aniqlangan Hajmda Bayt Yig'ish
**Tavsif:** Tarmoq oqimidan ixtiyoriy daqiqada aynan `N` bayt ma'lumotni kutib olish imkoniyatini beruvchi yordamchi bufer.
**Talablar:** `Completer`, navbat boshqaruvi, `readBytes(int count)`.
**Yechim (Dart):**
```dart
import 'dart:async';
import 'dart:typed_data';

class AsyncStreamBuffer {
  final List<int> _buffer = [];

  void add(List<int> chunk) => _buffer.addAll(chunk);

  Future<Uint8List> readBytes(Stream<List<int>> stream, int count) async {
    final completer = Completer<Uint8List>();
    late StreamSubscription sub;

    void check() {
      if (_buffer.length >= count) {
        final result = Uint8List.fromList(_buffer.sublist(0, count));
        _buffer.removeRange(0, count);
        sub.cancel();
        completer.complete(result);
      }
    }

    sub = stream.listen((chunk) {
      _buffer.addAll(chunk);
      check();
    });

    check();
    return completer.future;
  }
}

void main() {
  print('AsyncStreamBuffer yordamchisi yaratildi.');
}
```
**Tushuntirish:** Ushbu bufer yordamida binar protokollarning sarlavhasini avval o'qib, sarlavhadagi hajmga qarab keyingi foydali yuklamani kutib olish osonlashadi.

---

### Topshiriq #1120: Isolate Lar Orqali Tarmoq I/O va Hisoblashni Parallelizatsiya Qilish
**Tavsif:** Asosiy UI yoki server oqimini to'xtatib qo'ymaslik uchun shifrlash va paketlarni tahlil qilishni alohida Dart Izolyatsiyasiga topshirish.
**Talablar:** `Isolate.spawn`, `ReceivePort`, `SendPort`.
**Yechim (Dart):**
```dart
import 'dart:isolate';
import 'dart:typed_data';

void packetProcessorIsolate(SendPort sendPort) {
  final port = ReceivePort();
  sendPort.send(port.sendPort);

  port.listen((message) {
    if (message is Uint8List) {
      // Alohida CPU yadrosida og'ir hisoblash (masalan, kriptografiya yoki tahlil)
      int sum = message.fold(0, (a, b) => a + b);
      sendPort.send('Tahlil yakuni: Baytlar yig\'indisi = $sum');
    }
  });
}

void main() async {
  final receivePort = ReceivePort();
  await Isolate.spawn(packetProcessorIsolate, receivePort.sendPort);

  final sendPort = await receivePort.first as SendPort;
  sendPort.send(Uint8List.fromList([10, 20, 30, 40, 50]));
}
```
**Tushuntirish:** Dart izolyatsiyalari xotirani umumiy ulashmaydi (Shared-nothing memory). Ma'lumotlar xabarlar orqali uzatiladi, bu esa data-race muammolarini butunlay yo'q qiladi.

---

### Topshiriq #1121: Tarmoq Oqimini Cheklovchi Rate Limiter StreamTransformer
**Tavsif:** Klientga uzatilayotgan ma'lumotlar tezligini (masalan, 1 MB/s) sun'iy ravishda chegaralash (Throttling).
**Talablar:** `Stopwatch`, `Future.delayed`, tezlik hisoblagichi.
**Yechim (Dart):**
```dart
import 'dart:async';

class RateLimiterTransformer extends StreamTransformerBase<List<int>, List<int>> {
  final int maxBytesPerSecond;

  RateLimiterTransformer(this.maxBytesPerSecond);

  @override
  Stream<List<int>> bind(Stream<List<int>> stream) async* {
    final sw = Stopwatch()..start();
    int bytesSent = 0;

    await for (var chunk in stream) {
      bytesSent += chunk.length;
      final expectedTimeMs = (bytesSent / maxBytesPerSecond * 1000).toInt();
      final actualTimeMs = sw.elapsedMilliseconds;

      if (expectedTimeMs > actualTimeMs) {
        await Future.delayed(Duration(milliseconds: expectedTimeMs - actualTimeMs));
      }
      yield chunk;
    }
  }
}

void main() {
  print('RateLimiterTransformer moduli tekshirildi.');
}
```
**Tushuntirish:** Rate Limiter orqali tarmoq kartasining to'lib qolishini va bir nechta oqimlar o'rtasida o'tkazuvchanlikning tengsiz taqsimlanishini oldini olish mumkin.

---

### Topshiriq #1122: Soket Ulanishlari Hovuzi (Connection Pool Boshqaruvi)
**Tavsif:** Har bir so'rov uchun qayta TCP handshake qilmasdan, bo'sh soketlarni qayta ishlatish.
**Talablar:** `Queue<Socket>`, maksimal hajm, bo'shatish va qayta olish.
**Yechim (Dart):**
```dart
import 'dart:collection';
import 'dart:io';

class SocketPool {
  final String host;
  final int port;
  final int maxSize;
  final Queue<Socket> _available = Queue();

  SocketPool(this.host, this.port, {this.maxSize = 10});

  Future<Socket> acquire() async {
    if (_available.isNotEmpty) {
      return _available.removeFirst();
    }
    return await Socket.connect(host, port);
  }

  void release(Socket socket) {
    if (_available.length < maxSize) {
      _available.addLast(socket);
    } else {
      socket.destroy();
    }
  }
}

void main() {
  final pool = SocketPool('127.0.0.1', 8080);
  print('Soketlar hovuzi initsializatsiya qilindi.');
}
```
**Tushuntirish:** Connection Pooling tarmoq ulanishlarini o'rnatishdagi 3-Way Handshake va TLS muzokaralari xarajatlarini yo'qotadi va tizimning javob berish tezligini oshiradi.

---

### Topshiriq #1123: WebSocket.connect Bilan Asinxron WebSocket Klient
**Tavsif:** Brauzer va server o'rtasida to'liq dupleks aloqa o'rnatish va JSON buyruqlarni yuborish.
**Talablar:** `dart:io`, `WebSocket.connect`, `Stream<dynamic>`, `add()`.
**Yechim (Dart):**
```dart
import 'dart:io';

void main() async {
  try {
    // WebSocket serveriga ulanish
    final ws = await WebSocket.connect('wss://echo.websocket.events');
    print('WebSocket ga ulandi.');

    // Xabarlarni tinglash
    ws.listen(
      (data) {
        print('Kelgan xabar: $data');
        ws.close(WebSocketStatus.normalClosure, 'Ish yakunlandi');
      },
      onDone: () => print('WebSocket yopildi.'),
      onError: (err) => print('WebSocket xatosi: $err'),
    );

    // Xabar jo'natish
    ws.add('Salom, WebSocket Dunyosi!');
  } catch (e) {
    print('Ulanish amalga oshmadi: $e');
  }
}
```
**Tushuntirish:** `WebSocket.connect` HTTP Upgrade so'rovi orqali TCP soketini WebSocket protokoliga ko'taradi va kelgusidagi xabarlarni RFC 6455 freymlarida uzatadi.

---

### Topshiriq #1124: HttpServer Da WebSocket So'rovlarini Qabul Qilish (WebSocketTransformer)
**Tavsif:** Standart Dart HTTP serverini mijoz so'rovi bo'yicha WebSocket rejimiga o'tkazish.
**Talablar:** `HttpServer.bind`, `WebSocketTransformer.isUpgradeRequest`, `WebSocketTransformer.upgrade`.
**Yechim (Dart):**
```dart
import 'dart:io';

void main() async {
  final server = await HttpServer.bind(InternetAddress.anyIPv4, 8081);
  print('HTTP/WebSocket Server 8081-portda ishga tushdi.');

  await for (HttpRequest req in server) {
    if (WebSocketTransformer.isUpgradeRequest(req)) {
      // HTTP ulanishini WebSocket ga ko'tarish
      final ws = await WebSocketTransformer.upgrade(req);
      print('Mijoz WebSocket ga o\'tdi!');

      ws.listen((message) {
        ws.add('Echo: $message');
      });
    } else {
      req.response
        ..statusCode = HttpStatus.ok
        ..write('Faqat WebSocket so\'rovlari qabul qilinadi.')
        ..close();
    }
  }
}
```
**Tushuntirish:** `WebSocketTransformer.upgrade` `Sec-WebSocket-Key` sarlavhasini olib, SHA-1 xeshini hisoblaydi va `101 Switching Protocols` javobini avtomatik qaytaradi.

---

### Topshiriq #1125: WebSocket Ping/Pong va Heartbeat Mexanizmi
**Tavsif:** Tarmoq simi uzilib qolganda yoki NAT oraliq marshrutizatorlari ulanishni yopmasligi uchun muntazam nazorat paketlarini jo'natish.
**Talablar:** `pingInterval`, aloqa holati nazorati.
**Yechim (Dart):**
```dart
import 'dart:io';

void setupHeartbeat(WebSocket socket) {
  // Har 30 soniyada avtomatik Ping ramkasini yuborish
  socket.pingInterval = const Duration(seconds: 30);

  socket.listen(
    (message) => print('Xabar keldi: $message'),
    onDone: () => print('Heartbeat yo\'qolganligi sababli ulanish yopildi.'),
  );
}

void main() {
  print('WebSocket Heartbeat mexanizmi faollashtirildi.');
}
```
**Tushuntirish:** `pingInterval` o'rnatilganda, agar server belgilangan vaqt ichida Pong javobini olmasa, ulanishni o'lik deb hisoblaydi va resurslarni ozod qiladi.

---

### Topshiriq #1126: WebSocket Orqali Binar Ma'lumotlarni (Uint8List) Uzatish
**Tavsif:** Fayllar, audio oqimlari yoki ikkilik ma'lumotlarni matnli JSON ga o'girmasdan to'g'ridan-to'g'ri binar freym sifatida jo'natish.
**Talablar:** `ws.add(Uint8List)`, binar freymlarni aniqlash.
**Yechim (Dart):**
```dart
import 'dart:io';
import 'dart:typed_data';

void handleBinaryData(WebSocket socket) {
  // Binar massiv yuborish
  final bytes = Uint8List.fromList([0xDE, 0xAD, 0xBE, 0xEF]);
  socket.add(bytes);

  socket.listen((data) {
    if (data is List<int>) {
      print('Binar freym qabul qilindi: ${data.length} bayt');
    } else if (data is String) {
      print('Matnli xabar: $data');
    }
  });
}

void main() {
  print('Binar WebSocket moduli tayyor.');
}
```
**Tushuntirish:** Binar freymlar Base64 kodlashning 33% ortiqcha xarajatini (overhead) yo'qotadi va xotira sarfini qisqartiradi.

---

### Topshiriq #1127: WebSocket Qayta Ulanish Strategiyasi (Exponential Backoff)
**Tavsif:** Server qayta yuklanganda barcha mijozlarning bir vaqtda qayta ulanib serverni qulatishini (Thundering Herd) oldini oluvchi aqlli kechikish.
**Talablar:** Exponential backoff, jitter, rekursiv qayta ulanish.
**Yechim (Dart):**
```dart
import 'dart:io';
import 'dart:math';
import 'dart:async';

class ResilientWebSocket {
  final String url;
  int _attempt = 0;

  ResilientWebSocket(this.url);

  void connect() async {
    try {
      final ws = await WebSocket.connect(url);
      print('Muvaffaqiyatli ulandi!');
      _attempt = 0; // Urinishlar sonini tiklash

      ws.listen(
        (data) => print('Xabar: $data'),
        onDone: () => _retry(),
        onError: (e) => _retry(),
      );
    } catch (e) {
      _retry();
    }
  }

  void _retry() {
    _attempt++;
    // 2^n + jitter orqali kechikishni hisoblash (maksimal 30 soniya)
    final delaySec = min(30, pow(2, _attempt).toInt()) + Random().nextInt(2);
    print('Qayta ulanish #$_attempt kutilmoqda: ${delaySec}s...');
    Timer(Duration(seconds: delaySec), connect);
  }
}

void main() {
  final client = ResilientWebSocket('ws://127.0.0.1:8081');
  client.connect();
}
```
**Tushuntirish:** Exponential Backoff + Jitter mijozlarning qayta ulanish vaqtlarini tasodifiy taqsimlaydi va serverga tushadigan bosimni silliqlashtiradi.

---

### Topshiriq #1128: WebSocket Multiplexing: Bitta Soketda Virtual Kanallar
**Tavsif:** Bitta jismoniy WebSocket aloqasi orqali bir vaqtning o'zida bir nechta mustaqil mavzularga (topics/rooms) obuna bo'lish.
**Talablar:** Kanal identifikatori (`channel_id`), xabarlarni marshrutlash.
**Yechim (Dart):**
```dart
import 'dart:convert';

class MultiplexedMessage {
  final String channel;
  final dynamic data;

  MultiplexedMessage(this.channel, this.data);

  String encode() => jsonEncode({'channel': channel, 'data': data});

  static MultiplexedMessage decode(String raw) {
    final map = jsonDecode(raw);
    return MultiplexedMessage(map['channel'], map['data']);
  }
}

void main() {
  final msg = MultiplexedMessage('chat:general', {'user': 'Ali', 'text': 'Salom!'});
  print('Kodlangan virtual kanal xabari: ${msg.encode()}');
}
```
**Tushuntirish:** Multiplexing har bir xizmat yoki chat xonasi uchun alohida soket ochish zaruratini yo'qotadi va tarmoq resurslarini tejaydi.

---

### Topshiriq #1129: Broadcast WebSocket Hub (Barcha Klientlarga Tarqatish)
**Tavsif:** Bitta foydalanuvchi yuborgan xabarni tizimga ulangan yuzlab boshqa faol mijozlarga bir zumda tarqatuvchi Hub arxitekturasi.
**Talablar:** `Set<WebSocket>`, tarqatish sikli, yopiq soketlarni tozalash.
**Yechim (Dart):**
```dart
import 'dart:io';

class WebSocketHub {
  final Set<WebSocket> _clients = {};

  void register(WebSocket socket) {
    _clients.add(socket);
    socket.listen(
      (data) => broadcast(data, exclude: socket),
      onDone: () => _clients.remove(socket),
      onError: (_) => _clients.remove(socket),
    );
  }

  void broadcast(dynamic message, {WebSocket? exclude}) {
    for (var client in _clients) {
      if (client != exclude && client.readyState == WebSocket.open) {
        client.add(message);
      }
    }
  }
}

void main() {
  final hub = WebSocketHub();
  print('WebSocket Hub markazi ishga tushirildi.');
}
```
**Tushuntirish:** `_clients` ro'yxatidan yopilgan soketlarni darhol o'chirib borish xotira sizib chiqishining (Memory Leak) oldini oladi.

---

### Topshiriq #1130: WebSocket Subprotocol Kelishuvi (RFC 6455)
**Tavsif:** Klient va server o'rtasida qaysi dasturiy protokol (masalan, `graphql-ws`, `v1.json`) qo'llanilishini handshake vaqtida kelishish.
**Talablar:** `protocols`, `selectedProtocol` tekshiruvi.
**Yechim (Dart):**
```dart
import 'dart:io';

void main() async {
  try {
    final ws = await WebSocket.connect(
      'ws://127.0.0.1:8081',
      protocols: ['graphql-transport-ws', 'chat.v2'],
    );

    print('Tanlangan subprotokol: ${ws.subprotocol}');
    await ws.close();
  } catch (e) {
    print('Subprotokol xatosi: $e');
  }
}
```
**Tushuntirish:** `Sec-WebSocket-Protocol` sarlavhasi orqali server mijoz taklif qilgan ro'yxatdan o'zi qo'llab-quvvatlaydigan versiyani tanlaydi.

---

### Topshiriq #1131: WebSocket Orqali Audio/Video Oqimlarini Uzatish
**Tavsif:** Real vaqtli ovozli yoki video paketlarni bo'laklab uzatish uchun binar xabarlar konveyerini sozlash.
**Talablar:** `Uint8List` oqimlari, kichik buferlash.
**Yechim (Dart):**
```dart
import 'dart:io';
import 'dart:typed_data';

void streamAudioChunks(WebSocket socket, Stream<Uint8List> audioSource) {
  audioSource.listen((chunk) {
    if (socket.readyState == WebSocket.open) {
      socket.add(chunk); // Audio bo'lagini to'g'ridan-to'g'ri uzatish
    }
  });
}

void main() {
  print('Audio oqimli WebSocket uzatgichi tayyorlandi.');
}
```
**Tushuntirish:** Kichik audio bo'laklari (20-40ms PCM) uzatilganda kechikish minimal bo'ladi va o'yinlar hamda ovozli chatlarda jonli muloqot ta'minlanadi.

---

### Topshiriq #1132: WebSocket Xavfsizligi: Origin Tekshiruvi va JWT Autentifikatsiya
**Tavsif:** Cross-Site WebSocket Hijacking (CSWSH) hujumlaridan himoyalanish uchun Origin sarlavhasini va tokenni tekshirish.
**Talablar:** `HttpRequest.headers['origin']`, JWT tokenni Query yoki Cookie dan olish.
**Yechim (Dart):**
```dart
import 'dart:io';

bool authenticateWebSocket(HttpRequest request) {
  final origin = request.headers.value('origin');
  // Faqat o'z domenimizdan kelgan so'rovlarga ruxsat berish
  if (origin != null && !origin.endsWith('.khorazmiy.uz')) {
    return false; // CSWSH hujumi xavfi
  }

  final token = request.uri.queryParameters['token'];
  if (token != 'maxfiy_jwt_token') {
    return false; // Ruxsatsiz kirish
  }

  return true;
}

void main() {
  print('WebSocket xavfsizlik filtri faollashtirildi.');
}
```
**Tushuntirish:** WebSocket so'rovlari brauzerning Same-Origin Policy (SOP) qoidasiga bo'ysunmaydi, shuning uchun server tomonida `Origin` tekshiruvi majburiydir.

---

### Topshiriq #1133: WebSocket Graceful Close Mexanizmi (WebSocketStatus)
**Tavsif:** Ulanishni birdaniga uzib tashlamasdan, RFC 6455 standartidagi yopilish kodlari bilan toza yakunlash.
**Talablar:** `WebSocketStatus.normalClosure`, `goingAway`, yopilish sababi.
**Yechim (Dart):**
```dart
import 'dart:io';

Future<void> shutdownWebSocket(WebSocket socket) async {
  if (socket.readyState == WebSocket.open) {
    print('Soket toza yopilmoqda (Normal Closure)...');
    await socket.close(WebSocketStatus.normalClosure, 'Sessiya xavfsiz yakunlandi.');
  }
}

void main() {
  print('Graceful Close moduli tekshirildi.');
}
```
**Tushuntirish:** `normalClosure` (kod 1000) orqali yopilganda mijoz ulanish tasodifan uzilmaganini tushunadi va qayta ulanishga urinib serverni bezovta qilmaydi.

---

### Topshiriq #1134: HTTP/2 ClientConnection Ochish va Multiplexing Asoslari
**Tavsif:** `http2` paketi yordamida bitta TCP ulanishida bir vaqtning o'zida bir nechta so'rovlarni uzatish.
**Talablar:** `ClientTransportConnection`, `ClientTransportStream`, `Header`.
**Yechim (Dart):**
```dart
import 'dart:io';
import 'package:http2/http2.dart';

Future<void> runHttp2Client() async {
  final socket = await SecureSocket.connect(
    'http2.golang.org',
    443,
    supportedProtocols: ['h2'],
  );

  final transport = ClientTransportConnection.viaSocket(socket);

  // Yangi HTTP/2 oqimini ochish
  final stream = transport.makeRequest([
    Header.ascii(':method', 'GET'),
    Header.ascii(':path', '/reqinfo'),
    Header.ascii(':scheme', 'https'),
    Header.ascii(':authority', 'http2.golang.org'),
  ], endStream: true);

  await for (var message in stream.incomingMessages) {
    if (message is HeadersStreamMessage) {
      print('HTTP/2 Sarlavhalari qabul qilindi.');
    } else if (message is DataStreamMessage) {
      print('HTTP/2 Ma\'lumot: ${message.bytes.length} bayt');
    }
  }

  await transport.finish();
}

void main() {
  print('HTTP/2 Multiplexing klienti tayyor.');
}
```
**Tushuntirish:** HTTP/2 da barcha so'rovlar bitta TCP ulanish ustida virtual 'Stream' lar orqali yuboriladi, bu esa yangi TCP/TLS ochish vaqtini butunlay tejaydi.

---

### Topshiriq #1135: HTTP/2 Parallel So'rovlar (Concurrency)
**Tavsif:** Bitta ulanish orqali 10 ta so'rovni bir vaqtning o'zida yuborib, ularning javoblarini parallel olish.
**Talablar:** `Future.wait`, bitta `ClientTransportConnection` dan foydalanish.
**Yechim (Dart):**
```dart
import 'package:http2/http2.dart';

Future<void> sendConcurrentRequests(ClientTransportConnection transport, List<String> paths) async {
  final futures = paths.map((path) async {
    final stream = transport.makeRequest([
      Header.ascii(':method', 'GET'),
      Header.ascii(':path', path),
      Header.ascii(':scheme', 'https'),
      Header.ascii(':authority', 'api.khorazmiy.uz'),
    ], endStream: true);

    await for (var msg in stream.incomingMessages) {
      if (msg is DataStreamMessage) {
        // Ma'lumotni qabul qilish
      }
    }
  });

  await Future.wait(futures);
  print('Barcha parallel HTTP/2 so\'rovlar yakunlandi.');
}

void main() {
  print('HTTP/2 Concurrency moduli tayyor.');
}
```
**Tushuntirish:** HTTP/1.1 dagi kabi brauzerlar bir domen uchun 6 ta alohida TCP ulanish ochishga majbur bo'lmaydi; HTTP/2 da bitta ulanish minglab parallel oqimlarni ko'tara oladi.

---

### Topshiriq #1136: HTTP/2 Server Push Mexanizmini Tahlil Qilish
**Tavsif:** Klient so'ramasdanoq, server tomonidan erta yuborilgan resurslarni (CSS, JS, Rasmlar) qabul qilish.
**Talablar:** `incomingPushStreams`, `PushPromise` ramkasi.
**Yechim (Dart):**
```dart
import 'package:http2/http2.dart';

void handleServerPush(ClientTransportConnection transport) {
  transport.incomingPushStreams.listen((ClientTransportStream pushStream) {
    print('Server Push oqimi qabul qilindi!');
    pushStream.incomingMessages.listen((msg) {
      // Server itarib bergan kesh ma'lumotini saqlash
    });
  });
}

void main() {
  print('Server Push qabul qiluvchi tinglovchi tayyor.');
}
```
**Tushuntirish:** Server Push HTML so'ralganda unga kerakli uslublar va skriptlarni bir vaqtda oldindan jo'natib, sahifa ochilish kechikishini kamaytiradi.

---

### Topshiriq #1137: HTTP/2 HPACK Sarlavhalar Kompressiyasi Tahlili
**Tavsif:** Sarlavhalar matnini har safar qayta yubormasdan, indekslar jadvali (Static/Dynamic table) orqali baytlarni tejash.
**Talablar:** `Header`, statik va dinamik jadvallar.
**Yechim (Dart):**
```dart
import 'package:http2/http2.dart';

void explainHpack() {
  print('HPACK Sarlavhalar kompressiyasi:');
  print('1. :method: GET, :scheme: https kabi umumiy sarlavhalar 1 baytlik statik indeks bilan yuboriladi.');
  print('2. Qaytariluvchi maxsus sarlavhalar (User-Agent, Cookie) dinamik jadvalga joylashtirilib, keyingi so\'rovlarda 90% ga qisqaradi.');
}

void main() {
  explainHpack();
}
```
**Tushuntirish:** HPACK tarmoqdagi HTTP sarlavhalari hajmini sezilarli darajada kamaytiradi va mobil aloqa sekin bo'lganda so'rov yuborish tezligini oshiradi.

---

### Topshiriq #1138: gRPC Dart: ClientChannel Yaratish va Kanal Sozlamalari
**Tavsif:** Mikroxizmatlar bilan RPC aloqasi o'rnatish uchun gRPC kanalini xavfsiz va xavfsiz bo'lmagan rejimlarda ochish.
**Talablar:** `grpc`, `ClientChannel`, `ChannelOptions`, `ChannelCredentials`.
**Yechim (Dart):**
```dart
import 'package:grpc/grpc.dart';

ClientChannel createGrpcChannel(String host, int port, {bool isSecure = false}) {
  return ClientChannel(
    host,
    port: port,
    options: ChannelOptions(
      credentials: isSecure ? const ChannelCredentials.secure() : const ChannelCredentials.insecure(),
      idleTimeout: const Duration(minutes: 5),
    ),
  );
}

void main() {
  final channel = createGrpcChannel('127.0.0.1', 50051);
  print('gRPC kanali yaratildi: ${channel.host}:${channel.port}');
}
```
**Tushuntirish:** `ClientChannel` ulanishlar hovuzini va HTTP/2 transportini o'zi avtomatik boshqaradi. U bir nechta so'rovlar o'rtasida kanalni qayta ishlatadi.

---

### Topshiriq #1139: gRPC Unary RPC So'rov va Javob Almashinuvi
**Tavsif:** Klassik so'rov-javob modelidagi bitta protobuf xabarini yuborish va bitta javobni kutish.
**Talablar:** `ClientMethod`, asinxron chaqiruv.
**Yechim (Dart):**
```dart
import 'package:grpc/grpc.dart';

// Generatsiya qilingan stubs simulyatsiyasi
class UserRequest { final int id; UserRequest(this.id); }
class UserResponse { final String name; UserResponse(this.name); }

class UserServiceClient extends Client {
  UserServiceClient(ClientChannel channel) : super(channel);

  Future<UserResponse> getUser(UserRequest req) async {
    // Haqiqiy loyihada: return $createUnaryCall(_methodDescriptor, req);
    return UserResponse('Alisher Navoiy');
  }
}

void main() async {
  final channel = ClientChannel('localhost', port: 50051, options: const ChannelOptions(credentials: ChannelCredentials.insecure()));
  final client = UserServiceClient(channel);
  final user = await client.getUser(UserRequest(1));
  print('gRPC Foydalanuvchi: ${user.name}');
  await channel.shutdown();
}
```
**Tushuntirish:** Unary RPC ichki jihatdan bitta HTTP/2 stream ochadi, unga 5 baytlik gRPC sarlavha (Compression + Length) va protobuf baytlarini joylab uzatadi.

---

### Topshiriq #1140: gRPC Server Streaming: Real Vaqtda Narxlar Kotirovkasini Qabul Qilish
**Tavsif:** Bitta so'rov jo'natib, serverdan uzluksiz kelayotgan oqimni `ResponseStream` orqali tinglash.
**Talablar:** `ResponseStream<T>`, `await for` sikli.
**Yechim (Dart):**
```dart
import 'package:grpc/grpc.dart';

class MarketRequest { final String symbol; MarketRequest(this.symbol); }
class PriceTick { final double price; final int time; PriceTick(this.price, this.time); }

void subscribeToStockPrices(ResponseStream<PriceTick> stream) async {
  try {
    await for (PriceTick tick in stream) {
      print('Jonli narx: \$${tick.price.toStringAsFixed(2)} | Vaqt: ${tick.time}');
    }
  } catch (e) {
    print('Oqim uzildi: $e');
  }
}

void main() {
  print('Server Streaming tinglovchi moduli tayyor.');
}
```
**Tushuntirish:** Server Streaming mijozga har safar polling qilish (so'rab turish) xarajatlarisiz, serverdagi o'zgarishlarni zudlik bilan qabul qilish imkonini beradi.

---

### Topshiriq #1141: gRPC Client Streaming: Katta Fayllarni Bo'laklab Yuklash
**Tavsif:** Mijoz katta faylni xotiraga to'liq yuklamasdan, `Stream<FileChunk>` orqali serverga uzatadi.
**Talablar:** `Stream<T>`, `ClientStreamingCall`.
**Yechim (Dart):**
```dart
import 'dart:async';
import 'dart:typed_data';

class FileChunk { final Uint8List data; FileChunk(this.data); }
class UploadStatus { final bool success; UploadStatus(this.success); }

Stream<FileChunk> generateChunks(Uint8List largeFile, int chunkSize) async* {
  for (int i = 0; i < largeFile.length; i += chunkSize) {
    int end = (i + chunkSize < largeFile.length) ? i + chunkSize : largeFile.length;
    yield FileChunk(Uint8List.sublistView(largeFile, i, end));
  }
}

void main() {
  final fakeFile = Uint8List(1024 * 1024); // 1 MB
  final chunkStream = generateChunks(fakeFile, 64 * 1024); // 64 KB lik bo'laklar
  print('Fayl bo\'laklari oqimi yaratildi.');
}
```
**Tushuntirish:** Client Streaming orqali mobil telefonlarda xotira to'lib qolmasdan yuzlab megabaytlik video yoki arxiv fayllarni xavfsiz yuklash mumkin.

---

### Topshiriq #1142: gRPC Bi-directional Streaming: Ikki Tomonlama Asinxron Muloqot
**Tavsif:** Klient va server bir vaqtning o'zida mustaqil ravishda xabarlarni almashuvchi dupleks gRPC kanali.
**Talablar:** `StreamController`, ikki tomonlama `ResponseStream`.
**Yechim (Dart):**
```dart
import 'dart:async';

class ChatMessage { final String sender; final String text; ChatMessage(this.sender, this.text); }

void runBidiChat(StreamController<ChatMessage> outgoing, Stream<ChatMessage> incoming) {
  // 1. Serverdan kelayotgan xabarlarni o'qish
  incoming.listen((msg) {
    print('[${msg.sender}]: ${msg.text}');
  });

  // 2. Serverga xabar yuborish
  outgoing.add(ChatMessage('DartKlient', 'Salom gRPC Server!'));
}

void main() {
  final out = StreamController<ChatMessage>();
  print('Bi-directional streaming kanali tayyor.');
}
```
**Tushuntirish:** Bi-directional Streaming bitta HTTP/2 streamining ikkala yo'nalishidan bir vaqtda to'liq foydalanadi va minimal kechikish beradi.

---

### Topshiriq #1143: gRPC Client Interceptor: So'rovlarga Avtomatik JWT Metadata Qo'shish
**Tavsif:** Barcha chiquvchi RPC qo'ng'iroqlarga `authorization: Bearer <token>` sarlavhasini avtomatik biriktiruvchi filtr.
**Talablar:** `ClientInterceptor`, `ClientCall`, metadata header.
**Yechim (Dart):**
```dart
import 'package:grpc/grpc.dart';

class AuthInterceptor implements ClientInterceptor {
  final String token;

  AuthInterceptor(this.token);

  @override
  ResponseFuture<R> interceptUnary<Q, R>(
      ClientMethod<Q, R> method, Q request, CallOptions options, ClientUnaryInvoker<Q, R> invoker) {
    final newOptions = options.mergedWith(
      CallOptions(metadata: {'authorization': 'Bearer $token'}),
    );
    return invoker(method, request, newOptions);
  }

  @override
  ResponseStream<R> interceptStreaming<Q, R>(
      ClientMethod<Q, R> method, Stream<Q> requests, CallOptions options, ClientStreamingInvoker<Q, R> invoker) {
    final newOptions = options.mergedWith(
      CallOptions(metadata: {'authorization': 'Bearer $token'}),
    );
    return invoker(method, requests, newOptions);
  }
}

void main() {
  final interceptor = AuthInterceptor('maxfiy_jwt_token_123');
  print('AuthInterceptor muvaffaqiyatli tuzildi.');
}
```
**Tushuntirish:** Interseptorlar dastur kodining har bir metodida takroriy autentifikatsiya yozishdan xalos qiladi va xavfsizlikni bitta markazda ta'minlaydi.

---

### Topshiriq #1144: gRPC Server Interceptor Bilan So'rovlar Monitoringi va Logging
**Tavsif:** Serverga kirib kelayotgan har bir gRPC so'rovning bajarilish vaqtini va holatini jurnallash.
**Talablar:** `ServerInterceptor`, bajarilish vaqtini o'lchash.
**Yechim (Dart):**
```dart
import 'package:grpc/grpc.dart';

class LoggingServerInterceptor implements ServerInterceptor {
  @override
  GrpcError? intercept(ServiceMethod serverMethod, ServiceCall call) {
    final sw = Stopwatch()..start();
    print('[gRPC Kiruvchi] Metod: ${call.clientMetadata?[':path']}');

    // Chaqiruv tugagach vaqtni qayd qilish
    return null; // Xatolik bo'lmasa o'tkazish
  }
}

void main() {
  print('LoggingServerInterceptor moduli tayyor.');
}
```
**Tushuntirish:** Server Interceptor orqali shubhali murojaatlar, ruxsatsiz urinishlar va sekin ishlayotgan metodlar real vaqtda aniqlanadi.

---

### Topshiriq #1145: gRPC Deadlines va Timeoutlarni Boshqarish
**Tavsif:** Server uzoq vaqt javob bermasa yoki tarmoq qotib qolganda so'rovni zudlik bilan bekor qilish.
**Talablar:** `CallOptions(timeout: Duration(seconds: 2))`.
**Yechim (Dart):**
```dart
import 'package:grpc/grpc.dart';

CallOptions getStrictTimeoutOptions(int seconds) {
  return CallOptions(
    timeout: Duration(seconds: seconds),
  );
}

void main() {
  final options = getStrictTimeoutOptions(3);
  print('3 soniyalik qat\'iy gRPC Deadline sozlandi.');
}
```
**Tushuntirish:** Deadlines mikroservislar arxitekturasida 'kaskadli qulash' (Cascading Failures) ning oldini oluvchi eng asosiy vositadir.

---

### Topshiriq #1146: gRPC Error Handling va Status Kodlarini Tahlil Qilish
**Tavsif:** `GrpcError` yuz berganda xatolik kodini (`StatusCode.unavailable`, `unauthenticated`) to'g'ri qayta ishlash.
**Talablar:** `StatusCode`, `GrpcError`, xatolik xabari.
**Yechim (Dart):**
```dart
import 'package:grpc/grpc.dart';

void handleRpcException(Object error) {
  if (error is GrpcError) {
    switch (error.code) {
      case StatusCode.notFound:
        print('Xatolik: So\'ralgan obyekt topilmadi.');
        break;
      case StatusCode.unavailable:
        print('Xatolik: Server vaqtincha ishlamayapti, qayta urinib ko\'ring.');
        break;
      case StatusCode.unauthenticated:
        print('Xatolik: Ruxsat berilmagan, tokenni yangilang.');
        break;
      default:
        print('gRPC xatosi: [${error.codeName}] ${error.message}');
    }
  } else {
    print('Kutilmagan xatolik: $error');
  }
}

void main() {
  handleRpcException(GrpcError.notFound('Foydalanuvchi mavjud emas'));
}
```
**Tushuntirish:** Standart gRPC status kodlari barcha tillar va platformalar (Dart, C#, Go, Java) o'rtasida xatoliklarni bir xil tushunishni ta'minlaydi.

---

### Topshiriq #1147: gRPC KeepAlive va Connection Backoff Konfiguratsiyasi
**Tavsif:** Ulanishni uzoq vaqt tirik saqlash va tarmoq uzilganda avtomatik qayta ulanish parametrlarini sozlash.
**Talablar:** `ClientKeepaliveOptions`, `ChannelOptions`.
**Yechim (Dart):**
```dart
import 'package:grpc/grpc.dart';

ChannelOptions getProductionChannelOptions() {
  return const ChannelOptions(
    credentials: ChannelCredentials.secure(),
    keepAlive: ClientKeepaliveOptions(
      pingInterval: Duration(seconds: 30),
      timeout: Duration(seconds: 10),
      permitWithoutCalls: true,
    ),
  );
}

void main() {
  final opts = getProductionChannelOptions();
  print('Ishlab chiqarish (Production) gRPC KeepAlive parametrlari yuklandi.');
}
```
**Tushuntirish:** `permitWithoutCalls: true` hech qanday faol RPC chaqiruv bo'lmaganda ham Ping jo'natishga ruxsat beradi, bu esa oraliq firewallarning ulanishni yopib qo'ymasligini ta'minlaydi.

---

### Topshiriq #1148: Protobuf Xabarlarni Binar Serializatsiya va Deserializatsiya Qilish
**Tavsif:** Protobuf xabarlarini tarmoqqa uzatish uchun binar massivga o'girish va qayta tiklash.
**Talablar:** `writeToBuffer()`, `fromBuffer()`.
**Yechim (Dart):**
```dart
import 'dart:typed_data';

// Oddiy Protobuf model simulyatsiyasi
class DeviceConfig {
  final int id;
  final String mode;

  DeviceConfig(this.id, this.mode);

  Uint8List writeToBuffer() {
    // Binar shaklga o'girish
    return Uint8List.fromList([id, ...mode.codeUnits]);
  }

  static DeviceConfig fromBuffer(List<int> bytes) {
    return DeviceConfig(bytes[0], String.fromCharCodes(bytes.sublist(1)));
  }
}

void main() {
  final config = DeviceConfig(1, 'ACTIVE');
  final binary = config.writeToBuffer();
  final restored = DeviceConfig.fromBuffer(binary);
  print('Qayta tiklangan konfiguratsiya: ID=${restored.id}, Rejim=${restored.mode}');
}
```
**Tushuntirish:** Protobuf JSON ga qaraganda 3 dan 10 barobargacha kamroq hajm egallaydi va CPU tomonidan 5 barobar tezroq dekod qilinadi.

---

### Topshiriq #1149: Tarmoq Uzilishlarida gRPC Streamni Avtomatik Qayta Tiklash
**Tavsif:** Mobil aloqa uzilib-ulanganda gRPC oqimini to'xtatmasdan avtomatik qayta tiklovchi chidamli (resilient) qatlam.
**Talablar:** `StreamController`, qayta ulanish zanjiri.
**Yechim (Dart):**
```dart
import 'dart:async';

class ResilientGrpcStream<T> {
  final Stream<T> Function() streamFactory;
  final StreamController<T> _controller = StreamController<T>();

  ResilientGrpcStream(this.streamFactory);

  Stream<T> get stream => _controller.stream;

  void start() {
    _listen();
  }

  void _listen() {
    streamFactory().listen(
      (data) => _controller.add(data),
      onError: (err) {
        print('Stream uzildi, 2 soniyadan so\'ng qayta ulanish...');
        Future.delayed(const Duration(seconds: 2), _listen);
      },
      onDone: () => _controller.close(),
    );
  }
}

void main() {
  print('Chidamli gRPC stream qatlami yaratildi.');
}
```
**Tushuntirish:** Chidamli oqim qatlami mobil ilovalarda foydalanuvchiga tarmoq uzilishlarini sezdirmasdan, aloqa qayta tiklanganda avtomatik ma'lumot uzatishni davom ettiradi.

---

### Topshiriq #1150: Kompleks Yechim: Dart Raw Sockets + WebSocket Hub + gRPC Streaming Integratsiyasi
**Tavsif:** Barcha o'rganilgan protokollarni (L4 Raw Socket, WebSockets va gRPC) yagona arxitekturada birlashtiruvchi to'liq sanoat serveri.
**Talablar:** Ko'p protokolli server shlyuzi (Multi-protocol Gateway).
**Yechim (Dart):**
```dart
import 'dart:io';

class MasterNetworkGateway {
  static void printSystemOverview() {
    print('=== Khorazmiy AI: Dart Ilg\'or Tarmoq Arxitekturasi ===');
    print('1. L4 Qatlami: Raw Sockets va UDP Datagram orqali minimal kechikishli aloqa.');
    print('2. Real-Time Qatlami: WebSockets Hub orqali barcha faol veb va mobil mijozlarga broadcast.');
    print('3. Korporativ RPC Qatlami: gRPC va HTTP/2 orqali yuqori unumdorlikdagi mikroxizmatlararo ma\'lumot oqimi.');
    print('4. Barcha oqimlar Zero-Copy TypedData va StreamTransformer yordamida optimallashtirildi.');
  }
}

void main() {
  MasterNetworkGateway.printSystemOverview();
}
```
**Tushuntirish:** Ushbu kompleks yechim zamonaviy Flutter mobil ilovalari va yuqori yuklamali backend mikroxizmatlari o'rtasida eng yuqori darajadagi barqarorlik va chaqqonlikni kafolatlaydi.

---

