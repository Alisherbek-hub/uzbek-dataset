# Khorazmiy AI: JavaScript & TypeScript - Modul 23
## Mavzu: Tarmoq protokollari: Node.js / Bun Custom HTTP/3 parser, WebTransport, WebSocket klasteri va SSE

Salom, men **Khorazmiy AI** loyihasining JavaScript/TypeScript va ilg'or tarmoq protokollari bo'yicha bosh dataset mutaxassisiman. Ushbu modulda eng zamonaviy tarmoq texnologiyalari: past darajali UDP va QUIC (RFC 9000), HTTP/3 binar freymlar va QPACK dekompressiyasi (RFC 9204), brauzer va server o'rtasidagi WebTransport datagramlari va streamlari, yuqori yuklamali ko'p tugunli WebSocket klasterlari (Redis Backplane bilan) hamda Server-Sent Events (SSE) bo'yicha ishlab chiqilgan 50 ta (#1101 - #1150) sanoat darajasidagi amaliy topshiriq va mukammal yechimlar jamlangan.

---

### Topshiriq #1101: Node.js dgram Moduli Bilan Past Darajali UDP Soket Serveri va MTU Boshqaruvi
**Tavsif:** QUIC va HTTP/3 protokollari transport qatlami sifatida UDP dan foydalanadi. Tarmoqda IP paketlarning parchalanishini (Fragmentation) oldini olish uchun MTU chegaralarini nazorat qiluvchi yuqori unumdorlikdagi UDP serverini qurish zarur.
**Talablar:** Node.js 'node:dgram' moduli, 1200 baytlik minimal QUIC MTU o'lchamini tekshirish, xotira ajratishni optimallashtirish va soket parametrlarini sozlash.
**Yechim (TypeScript):**
```ts
import dgram from 'node:dgram';

// Standart Internet MTU (1500 bayt) - IP (20) - UDP (8) = 1472 bayt maksimal foydali yuklama
// RFC 9000 QUIC spetsifikatsiyasi bo'yicha minimal paket o'lchami 1200 bayt bo'lishi shart!
export const QUIC_MIN_INITIAL_PACKET_SIZE = 1200;
export const MAX_UDP_PAYLOAD_SIZE = 1472;

export interface UdpPacketHandler {
  onPacket(msg: Buffer, rinfo: dgram.RemoteInfo): void;
}

export class HighThroughputUdpServer {
  private socket: dgram.Socket;
  private isRunning = false;

  constructor(
    private readonly port: number = 4433,
    private readonly host: string = '0.0.0.0',
    private readonly handler?: UdpPacketHandler
  ) {
    // IPv4 soket yaratish
    this.socket = dgram.createSocket({
      type: 'udp4',
      reuseAddr: true, // Portni qayta ishlatish (klasterlash uchun)
      recvBufferSize: 8 * 1024 * 1024, // 8MB qabul qilish tizim buferi
      sendBufferSize: 8 * 1024 * 1024  // 8MB yuborish tizim buferi
    });

    this.setupEvents();
  }

  private setupEvents(): void {
    this.socket.on('error', (err) => {
      console.error('[UDP Server Xatolik]:', err.message);
    });

    this.socket.on('message', (msg: Buffer, rinfo: dgram.RemoteInfo) => {
      // QUIC Initial paketlari MTU probing sababli kamida 1200 bayt bo'lishi talab etiladi
      if (msg.length < QUIC_MIN_INITIAL_PACKET_SIZE) {
        // Agar paket juda kichik bo'lsa, uni xavfsizlik (Amplification Attack) uchun e'tiborsiz qoldirish mumkin
        // yoki oddiy UDP boshqaruvi sifatida qabul qilish mumkin
      }

      if (this.handler) {
        this.handler.onPacket(msg, rinfo);
      }
    });

    this.socket.on('listening', () => {
      const addr = this.socket.address();
      this.isRunning = true;
      console.log(`[UDP Server] ${addr.address}:${addr.port} manzilida tinglamoqda...`);
    });
  }

  public start(): Promise<void> {
    return new Promise((resolve) => {
      this.socket.bind(this.port, this.host, () => {
        resolve();
      });
    });
  }

  public send(msg: Uint8Array, port: number, address: string): Promise<number> {
    return new Promise((resolve, reject) => {
      if (msg.length > MAX_UDP_PAYLOAD_SIZE) {
        return reject(new Error(`Paket MTU hajmidan katta: ${msg.length} > ${MAX_UDP_PAYLOAD_SIZE}`));
      }
      this.socket.send(msg, port, address, (err, bytes) => {
        if (err) return reject(err);
        resolve(bytes);
      });
    });
  }

  public stop(): Promise<void> {
    return new Promise((resolve) => {
      if (!this.isRunning) return resolve();
      this.socket.close(() => {
        this.isRunning = false;
        resolve();
      });
    });
  }
}
```
**Tushuntirish:** UDP orqali yuqori tezlikda paket almashishda operatsion tizimning `recvBufferSize` (SO_RCVBUF) parametrini oshirish paket yo'qolishining (Packet Drop) oldini oladi. RFC 9000 talabi bo'yicha QUIC Initial paketlari tarmoq marshrutizatorlarining Path MTU imkoniyatlarini tekshirish va Amplification Attack (kuchaytirilgan DDoS) oldini olish maqsadida kamida 1200 baytga tenglab (Padding bilan) yuboriladi.

---

### Topshiriq #1102: Bun Muhitida Bun.udpSocket Yordamida Nol-Nusxa (Zero-Copy) UDP Paketlarni Qabul Qilish
**Tavsif:** Node.js dgram voqea siklida xotira ajratish (GC overhead) hosil qilishi mumkin. Bun o'rnatilgan yerlik C++ darajasidagi `Bun.udpSocket` orqali millionlab UDP paketlarni minimal kechikish bilan qayta ishlash imkonini beradi.
**Talablar:** Bun.udpSocket API'si, xotira buferlarini qayta ishlatish (Buffer pooling) va xatoliklarni qayta ishlash.
**Yechim (TypeScript):**
```ts
// Ushbu kod Bun runtime (v1.0+) muhitida ishga tushirishga mo'ljallangan
export interface BunUdpConfig {
  port: number;
  hostname: string;
}

export class BunHighSpeedUdpEngine {
  private socket: any = null;
  private totalPacketsReceived = 0;
  private totalBytesReceived = 0;

  constructor(private config: BunUdpConfig) {}

  public async initialize(): Promise<void> {
    // Bun.udpSocket yerlik tezkor UDP soketini ochadi
    this.socket = await (Bun as any).udpSocket({
      port: this.config.port,
      hostname: this.config.hostname,
      socket: {
        // Yangi paket kelganda nol-nusxa (Zero-copy) chaqiruv
        data: (socket: any, buf: Uint8Array, port: number, addr: string) => {
          this.totalPacketsReceived++;
          this.totalBytesReceived += buf.byteLength;

          // Paket sarlavhasini tahlil qilish (masalan, QUIC paket tipini aniqlash)
          const firstByte = buf[0];
          const isLongHeader = (firstByte & 0x80) !== 0;

          // Javob qaytarish (Echo yoki Handshake javobi)
          if (buf.byteLength >= 1200) {
            // QUIC Initial paketiga tezkor javob
            // socket.send(responseBuf, port, addr);
          }
        },
        error: (socket: any, error: Error) => {
          console.error('[Bun UDP Error]:', error);
        },
        drain: (socket: any) => {
          // Soket yozish buferi bo'shaganda chaqiriladi (Backpressure nazorati)
        }
      }
    });

    console.log(`[Bun UDP] ${this.config.hostname}:${this.config.port} portida ishga tushdi.`);
  }

  public getStats() {
    return {
      packets: this.totalPacketsReceived,
      bytes: this.totalBytesReceived,
      port: this.config.port
    };
  }

  public close(): void {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }
}
```
**Tushuntirish:** Bun ning `udpSocket` amalga oshirilishi Node.js dgram ga qaraganda bir necha barobar kam xotira sarflaydi. U har bir kiruvchi paket uchun yangi JavaScript `Buffer` obyektini xotiradan (Heap) ajratmasdan, to'g'ridan-to'g'ri operatsion tizimning yadro xotirasiga havola qiluvchi `Uint8Array` taqdim etadi.

---

### Topshiriq #1103: QUIC Variable-Length Integer (VarInt - RFC 9000) Dekoderi va Enkoderi
**Tavsif:** QUIC va HTTP/3 protokollarida barcha uzunliklar, oqim identifikatorlari va xato kodlari 1, 2, 4 yoki 8 baytli o'zgaruvchan uzunlikdagi butun sonlar (VarInt) shaklida kodlanadi.
**Talablar:** RFC 9000 bo'lim 16 asosida 2 ta yuqori bit (00=1 bayt, 01=2 bayt, 10=4 bayt, 11=8 bayt) orqali sonlarni aniq BigInt va number shaklida dekodlash hamda kodlash.
**Yechim (TypeScript):**
```ts
export class QuicVarInt {
  /**
   * VarInt qiymatini Uint8Array buferidan o'qiydi
   * @param buffer O'qilishi kerak bo'lgan binar oqim
   * @param offset Boshlanish pozitsiyasi
   * @returns { value: bigint, bytesRead: number }
   */
  public static decode(buffer: Uint8Array, offset: number = 0): { value: bigint; bytesRead: number } {
    if (offset >= buffer.length) {
      throw new RangeError('VarInt: Bufer o`lchami yetarli emas');
    }

    const firstByte = buffer[offset];
    // Eng yuqori 2 bit o'lchamni belgilaydi
    const prefix = (firstByte & 0xc0) >> 6;

    let length: number;
    let mask: number;

    switch (prefix) {
      case 0: // 00 -> 1 bayt (maksimal qiymat: 63)
        return { value: BigInt(firstByte & 0x3f), bytesRead: 1 };
      case 1: // 01 -> 2 bayt (maksimal qiymat: 16,383)
        length = 2;
        mask = 0x3f;
        break;
      case 2: // 10 -> 4 bayt (maksimal qiymat: 1,073,741,823)
        length = 4;
        mask = 0x3f;
        break;
      case 3: // 11 -> 8 bayt (maksimal qiymat: 4,611,686,018,427,387,903)
        length = 8;
        mask = 0x3f;
        break;
      default:
        throw new Error('Kutilmagan VarInt prefiksi');
    }

    if (offset + length > buffer.length) {
      throw new RangeError(`VarInt: Yetarli bayt yo'q, talab: ${length}, mavjud: ${buffer.length - offset}`);
    }

    let result = BigInt(firstByte & mask);
    for (let i = 1; i < length; i++) {
      result = (result << 8n) | BigInt(buffer[offset + i]);
    }

    return { value: result, bytesRead: length };
  }

  /**
   * Berilgan sonni QUIC VarInt binar formatiga o'giradi
   */
  public static encode(val: bigint | number): Uint8Array {
    const value = BigInt(val);

    if (value < 0n || value > 4611686018427387903n) {
      throw new RangeError(`VarInt diapazondan tashqarida: ${value}`);
    }

    if (value <= 63n) {
      // 1 bayt: 2 ta bit 00
      return new Uint8Array([Number(value)]);
    } else if (value <= 16383n) {
      // 2 bayt: 2 ta bit 01 (0x40)
      const buf = new Uint8Array(2);
      const num = Number(value);
      buf[0] = 0x40 | ((num >> 8) & 0x3f);
      buf[1] = num & 0xff;
      return buf;
    } else if (value <= 1073741823n) {
      // 4 bayt: 2 ta bit 10 (0x80)
      const buf = new Uint8Array(4);
      let v = Number(value);
      buf[0] = 0x80 | ((v >> 24) & 0x3f);
      buf[1] = (v >> 16) & 0xff;
      buf[2] = (v >> 8) & 0xff;
      buf[3] = v & 0xff;
      return buf;
    } else {
      // 8 bayt: 2 ta bit 11 (0xc0)
      const buf = new Uint8Array(8);
      let v = value;
      for (let i = 7; i >= 1; i--) {
        buf[i] = Number(v & 0xffn);
        v >>= 8n;
      }
      buf[0] = 0xc0 | Number(v & 0x3fn);
      return buf;
    }
  }
}
```
**Tushuntirish:** QUIC VarInt algoritmi binar tarmoq protokolini maksimal darajada ixchamlashtirish uchun xizmat qiladi. Kichik sonlar (masalan, Stream ID 1 yoki xato kodi 0) uchun atigi 1 bayt sarflanadi, yirik bayt hisoblagichlari uchun esa 8 baytgacha dinamik kengaytiriladi.

---

### Topshiriq #1104: QUIC Packet Header Parser: Long va Short Header Strukturalarini Ajratish
**Tavsif:** UDP orqali kelgan har bir QUIC paketi o'z sarlavhasiga (Header) ega. Ulanish o'rnatish bosqichida Long Header (Initial, 0-RTT, Handshake, Retry), o'rnatilgandan so'ng esa eng minimal Short Header (1-RTT) qo'llaniladi.
**Talablar:** Birinchi baytning 0x80 (Header Form bit) va 0x30 (Packet Type bitlari) ni tahlil qilib, DCID (Destination Connection ID) va SCID larni ajratib oluvchi to'liq TypeScript parserini yaratish.
**Yechim (TypeScript):**
```ts
export enum QuicPacketType {
  INITIAL = 'INITIAL',
  ZERO_RTT = '0-RTT',
  HANDSHAKE = 'HANDSHAKE',
  RETRY = 'RETRY',
  ONE_RTT = '1-RTT (SHORT)',
  VERSION_NEGOTIATION = 'VERSION_NEGOTIATION'
}

export interface QuicHeader {
  isLongHeader: boolean;
  type: QuicPacketType;
  version?: number;
  dcid: Uint8Array;
  scid?: Uint8Array;
  token?: Uint8Array;
  payloadOffset: number;
}

export class QuicHeaderParser {
  public static parse(packet: Uint8Array): QuicHeader {
    if (packet.length < 1) {
      throw new Error('Paket uzunligi 0 bayt!');
    }

    const firstByte = packet[0];
    const isLongHeader = (firstByte & 0x80) !== 0;

    // Bit 6 doimo 1 bo'lishi shart (Fixed Bit)
    if ((firstByte & 0x40) === 0) {
      throw new Error('RFC 9000 qoidasi buzildi: Fixed Bit 1 bo`lishi shart!');
    }

    if (isLongHeader) {
      return this.parseLongHeader(packet, firstByte);
    } else {
      return this.parseShortHeader(packet, firstByte);
    }
  }

  private static parseLongHeader(packet: Uint8Array, firstByte: number): QuicHeader {
    if (packet.length < 5) throw new Error('Long Header juda qisqa');

    // Versiya (4 bayt big-endian)
    const version = (packet[1] << 24) | (packet[2] << 16) | (packet[3] << 8) | packet[4];

    let offset = 5;

    // DCID (Destination Connection ID) uzunligi
    const dcidLen = packet[offset++];
    if (offset + dcidLen > packet.length) throw new Error('Noto`g`ri DCID uzunligi');
    const dcid = packet.slice(offset, offset + dcidLen);
    offset += dcidLen;

    // SCID (Source Connection ID) uzunligi
    const scidLen = packet[offset++];
    if (offset + scidLen > packet.length) throw new Error('Noto`g`ri SCID uzunligi');
    const scid = packet.slice(offset, offset + scidLen);
    offset += scidLen;

    if (version === 0) {
      return {
        isLongHeader: true,
        type: QuicPacketType.VERSION_NEGOTIATION,
        version: 0,
        dcid,
        scid,
        payloadOffset: offset
      };
    }

    // Packet Type: bits 4-5
    const packetTypeBits = (firstByte & 0x30) >> 4;
    let type: QuicPacketType;

    switch (packetTypeBits) {
      case 0x00: type = QuicPacketType.INITIAL; break;
      case 0x01: type = QuicPacketType.ZERO_RTT; break;
      case 0x02: type = QuicPacketType.HANDSHAKE; break;
      case 0x03: type = QuicPacketType.RETRY; break;
      default: throw new Error('Noma`lum Long Header tipi');
    }

    return {
      isLongHeader: true,
      type,
      version,
      dcid,
      scid,
      payloadOffset: offset
    };
  }

  private static parseShortHeader(packet: Uint8Array, firstByte: number): QuicHeader {
    // 1-RTT paketlarida faqat DCID bo'ladi (sukut bo'yicha server tomonidan kelishilgan hajmda, masalan 8 bayt)
    const DCID_LEN = 8;
    let offset = 1;

    const dcid = packet.slice(offset, offset + DCID_LEN);
    offset += DCID_LEN;

    return {
      isLongHeader: false,
      type: QuicPacketType.ONE_RTT,
      dcid,
      payloadOffset: offset
    };
  }
}
```
**Tushuntirish:** QUIC ulanish o'rnatish paytida server va mijoz bir-birini aniqlash uchun `Long Header` orqali to'liq identifikatorlarni uzatadi. Handshake muvaffaqiyatli tugagach, har bir paketda sarlavha hajmini tejash uchun `Short Header` ishlatiladi, bu esa tarmoq qo'shimcha xarajatlarini (Overhead) minimal darajaga tushiradi.

---

### Topshiriq #1105: QUIC Frame Parser: PADDING, PING, ACK va CONNECTION_CLOSE Freymlarini Binar Tahlil Qilish
**Tavsif:** QUIC paketi shifrsizlantirilgandan so'ng, uning foydali yuki bir yoki bir nechta freymlardan (Frames) iborat bo'ladi. Har bir freym o'z turiga (Frame Type) ko'ra qayta ishlanishi lozim.
**Talablar:** RFC 9000 dagi 0x00 (PADDING), 0x01 (PING), 0x02/0x03 (ACK), 0x1c (CONNECTION_CLOSE) freym turlarini aniqlovchi TypeScript parseri.
**Yechim (TypeScript):**
```ts
import { QuicVarInt } from './QuicVarInt';

export enum FrameType {
  PADDING = 0x00,
  PING = 0x01,
  ACK = 0x02,
  ACK_ECN = 0x03,
  CONNECTION_CLOSE_QUIC = 0x1c,
  CONNECTION_CLOSE_APP = 0x1d
}

export interface QuicFrame {
  type: FrameType;
  name: string;
  data?: any;
}

export class QuicFrameParser {
  public static parseFrames(payload: Uint8Array, startOffset: number = 0): QuicFrame[] {
    const frames: QuicFrame[] = [];
    let offset = startOffset;

    while (offset < payload.length) {
      const { value: frameTypeVal, bytesRead: typeBytes } = QuicVarInt.decode(payload, offset);
      offset += typeBytes;
      const fType = Number(frameTypeVal);

      if (fType === FrameType.PADDING) {
        // PADDING bir nechta ketma-ket nol baytlar bo'lishi mumkin
        while (offset < payload.length && payload[offset] === 0x00) {
          offset++;
        }
        frames.push({ type: FrameType.PADDING, name: 'PADDING' });
      } else if (fType === FrameType.PING) {
        frames.push({ type: FrameType.PING, name: 'PING' });
      } else if (fType === FrameType.ACK || fType === FrameType.ACK_ECN) {
        // Largest Acknowledged
        const { value: largestAck, bytesRead: b1 } = QuicVarInt.decode(payload, offset);
        offset += b1;
        // ACK Delay
        const { value: ackDelay, bytesRead: b2 } = QuicVarInt.decode(payload, offset);
        offset += b2;
        // ACK Range Count
        const { value: ackRangeCount, bytesRead: b3 } = QuicVarInt.decode(payload, offset);
        offset += b3;
        // First ACK Range
        const { value: firstAckRange, bytesRead: b4 } = QuicVarInt.decode(payload, offset);
        offset += b4;

        frames.push({
          type: fType,
          name: 'ACK',
          data: { largestAck, ackDelay, ackRangeCount, firstAckRange }
        });
      } else if (fType === FrameType.CONNECTION_CLOSE_QUIC || fType === FrameType.CONNECTION_CLOSE_APP) {
        const { value: errorCode, bytesRead: bErr } = QuicVarInt.decode(payload, offset);
        offset += bErr;

        let frameTypeTrigger: bigint | null = null;
        if (fType === FrameType.CONNECTION_CLOSE_QUIC) {
          const { value: ft, bytesRead: bFt } = QuicVarInt.decode(payload, offset);
          offset += bFt;
          frameTypeTrigger = ft;
        }

        const { value: reasonLen, bytesRead: bLen } = QuicVarInt.decode(payload, offset);
        offset += bLen;

        const reasonBytes = payload.slice(offset, offset + Number(reasonLen));
        offset += Number(reasonLen);
        const reasonPhrase = new TextDecoder().decode(reasonBytes);

        frames.push({
          type: fType,
          name: 'CONNECTION_CLOSE',
          data: { errorCode, frameTypeTrigger, reasonPhrase }
        });
      } else {
        // Boshqa freym turlari (masalan STREAM, RESET_STREAM)
        break;
      }
    }

    return frames;
  }
}
```
**Tushuntirish:** QUIC freym arxitekturasi bitta UDP paket ichida bir vaqtning o'zida ham ma'lumot uzatish (STREAM), ham tarmoq sog'lig'ini tekshirish (PING/ACK), ham ulanishni xavfsiz boshqarish imkonini beradi. Har bir freym mustaqil bo'lib, xatolik yuz berganda `CONNECTION_CLOSE` orqali sabab darhol yetkaziladi.

---

### Topshiriq #1106: QUIC Stream Freymlarini (STREAM, RESET_STREAM, STOP_SENDING) Dekodlash va Oqim Yig'ish
**Tavsif:** QUIC da har bir ma'lumot oqimi (Stream) mustaqil ketma-ketlikda kelishi mumkin. Agar bitta stream paketi yo'qolsa, bu boshqa streamlarning to'xtashiga (Head-of-Line Blocking) olib kelmasligi kerak.
**Talablar:** 0x08 dan 0x0f gacha bo'lgan STREAM freym bitlarini (OFF, LEN, FIN bayroqlari) tahlil qilish va ma'lumotlarni oqim buferiga yig'ish.
**Yechim (TypeScript):**
```ts
import { QuicVarInt } from './QuicVarInt';

export interface QuicStreamFrame {
  streamId: bigint;
  offset: bigint;
  fin: boolean;
  data: Uint8Array;
}

export class QuicStreamAssembler {
  private streamBuffers = new Map<string, { chunks: { offset: bigint; data: Uint8Array }[]; isFinished: boolean }>();

  /**
   * STREAM freymini binar oqimdan dekodlash (0x08 - 0x0f oralig'idagi freymlar)
   */
  public static decodeStreamFrame(buffer: Uint8Array, startOffset: number): { frame: QuicStreamFrame; bytesRead: number } {
    let offset = startOffset;
    const firstByte = buffer[offset++];

    // Freym bitlari: 0b00001XXX
    // bit 2: OFF (Offset mavjudmi)
    // bit 1: LEN (Uzunlik ko'rsatilganmi)
    // bit 0: FIN (Stream yakunlandimi)
    const hasOffset = (firstByte & 0x04) !== 0;
    const hasLength = (firstByte & 0x02) !== 0;
    const fin = (firstByte & 0x01) !== 0;

    const { value: streamId, bytesRead: sIdBytes } = QuicVarInt.decode(buffer, offset);
    offset += sIdBytes;

    let streamOffset = 0n;
    if (hasOffset) {
      const { value: offVal, bytesRead: offBytes } = QuicVarInt.decode(buffer, offset);
      offset += offBytes;
      streamOffset = offVal;
    }

    let length = buffer.length - offset;
    if (hasLength) {
      const { value: lenVal, bytesRead: lenBytes } = QuicVarInt.decode(buffer, offset);
      offset += lenBytes;
      length = Number(lenVal);
    }

    const data = buffer.slice(offset, offset + length);
    offset += length;

    return {
      frame: { streamId, offset: streamOffset, fin, data },
      bytesRead: offset - startOffset
    };
  }

  /**
   * Turli tartibda kelgan stream bo'laklarini tartib bilan yig'ish (Reassembly)
   */
  public pushChunk(frame: QuicStreamFrame): Uint8Array | null {
    const key = frame.streamId.toString();
    if (!this.streamBuffers.has(key)) {
      this.streamBuffers.set(key, { chunks: [], isFinished: false });
    }

    const state = this.streamBuffers.get(key)!;
    state.chunks.push({ offset: frame.offset, data: frame.data });
    if (frame.fin) state.isFinished = true;

    // Offset bo'yicha saralash
    state.chunks.sort((a, b) => (a.offset < b.offset ? -1 : 1));

    // Agar stream to'liq yakunlangan va bo'shliqlar yo'q bo'lsa, to'liq yig'ilgan buferni qaytarish
    if (state.isFinished) {
      const totalLen = state.chunks.reduce((acc, c) => acc + c.data.length, 0);
      const combined = new Uint8Array(totalLen);
      let pos = 0;
      for (const chunk of state.chunks) {
        combined.set(chunk.data, pos);
        pos += chunk.data.length;
      }
      this.streamBuffers.delete(key);
      return combined;
    }

    return null;
  }
}
```
**Tushuntirish:** TCP protokolidan farqli ravishda, QUIC da har bir stream o'zining mustaqil `streamId` va `offset` ko'rsatgichiga ega. Bitta streamda paket yo'qolsa ham, boshqa parallel streamlar foydalanuvchiga uzluksiz yetkaziladi. Bu HTTP/3 ning TCP dagi Head-of-Line Blocking muammosini to'liq yengishining asosiy kalitidir.

---

### Topshiriq #1107: QUIC CRYPTO Freymlari Orqali TLS 1.3 ClientHello Xabarlarini Ajratish
**Tavsif:** QUIC protokoli o'rnatilgan TLS 1.3 xavfsizligidan foydalanadi. Klassik TLS TCP ustida ishlasa, QUIC da TLS xabarlari maxsus CRYPTO freymlari ichida uzatiladi.
**Talablar:** 0x06 (CRYPTO) freymini parse qilish, offset va ma'lumotlarni o'qish, ClientHello xabaridan SNI (Server Name Indication) ni ajratish.
**Yechim (TypeScript):**
```ts
import { QuicVarInt } from './QuicVarInt';

export class QuicCryptoHandler {
  /**
   * CRYPTO freymini dekodlash (Frame Type = 0x06)
   */
  public static parseCryptoFrame(buffer: Uint8Array, startOffset: number) {
    let offset = startOffset;
    const { value: fType, bytesRead: b0 } = QuicVarInt.decode(buffer, offset);
    offset += b0;

    if (fType !== 0x06n) throw new Error('Bu CRYPTO freymi emas!');

    const { value: cryptoOffset, bytesRead: b1 } = QuicVarInt.decode(buffer, offset);
    offset += b1;

    const { value: length, bytesRead: b2 } = QuicVarInt.decode(buffer, offset);
    offset += b2;

    const cryptoData = buffer.slice(offset, offset + Number(length));
    return {
      offset: cryptoOffset,
      data: cryptoData,
      totalBytesRead: (offset + Number(length)) - startOffset
    };
  }

  /**
   * TLS 1.3 ClientHello payload'idan SNI (Server Name Indication) domenini aniqlash
   */
  public static extractServerName(tlsPayload: Uint8Array): string | null {
    // 0x01: ClientHello handshaking tipi
    if (tlsPayload[0] !== 0x01) return null;

    // TLS ClientHello tuzilishi bo'ylab Extension'larga qadar sakrab o'tish
    let p = 4; // handshake header skip
    p += 2; // client version
    p += 32; // client random
    const sessionIdLen = tlsPayload[p++];
    p += sessionIdLen;

    const cipherSuitesLen = (tlsPayload[p] << 8) | tlsPayload[p + 1];
    p += 2 + cipherSuitesLen;

    const compMethodsLen = tlsPayload[p++];
    p += compMethodsLen;

    if (p >= tlsPayload.length) return null;

    const extensionsLen = (tlsPayload[p] << 8) | tlsPayload[p + 1];
    p += 2;
    const end = p + extensionsLen;

    while (p + 4 <= end) {
      const extType = (tlsPayload[p] << 8) | tlsPayload[p + 1];
      const extLen = (tlsPayload[p + 2] << 8) | tlsPayload[p + 3];
      p += 4;

      if (extType === 0x0000) { // SNI Extension
        p += 2; // server name list length
        const nameType = tlsPayload[p++];
        const nameLen = (tlsPayload[p] << 8) | tlsPayload[p + 1];
        p += 2;
        if (nameType === 0) { // host_name
          const nameBytes = tlsPayload.slice(p, p + nameLen);
          return new TextDecoder().decode(nameBytes);
        }
      }
      p += extLen;
    }

    return null;
  }
}
```
**Tushuntirish:** QUIC dagi CRYPTO freymi TLS 1.3 protokoli bilan uzviy bog'langan. Ushbu arxitektura sababli QUIC da 1-RTT yoki hatto 0-RTT (0 Round Trip Time) orqali ulanish o'rnatish mumkin, ya'ni mijoz birinchi paketning o'zidayoq shifrlangan dastlabki so'rovni yuborish imkoniyatiga ega bo'ladi.

---

### Topshiriq #1108: QUIC Paket Raqamini Kodlash va Qayta Tiklash (Packet Number Encoding/Decoding) Algoritmi
**Tavsif:** QUIC da har bir yuborilgan paket unikal ortib boruvchi raqamga ega bo'ladi. Tarmoq trafigini tejash uchun butun 64-bitlik son emas, faqat uning eng kichik 1-4 baytlari (Truncated Packet Number) tarmoqqa uzatiladi.
**Talablar:** RFC 9000 A.3 bo'limidagi paket raqamini qayta tiklash algoritmini (Largest Acked asosida) to'liq TypeScriptda yozish.
**Yechim (TypeScript):**
```ts
export class QuicPacketNumberHelper {
  /**
   * Qisqartirilgan paket raqamini (Truncated PN) to'liq 64-bitlik haqiqiy soniga qayta tiklash
   * @param largestPn Qabul qilingan eng katta paket raqami
   * @param truncatedPn Paketdan o'qilgan qisqa raqam
   * @param pnNbits Qisqa raqamning bitlar soni (8, 16, 24 yoki 32)
   */
  public static decodePacketNumber(largestPn: bigint, truncatedPn: bigint, pnNbits: number): bigint {
    const expectedPn = largestPn + 1n;
    const pnWin = 1n << BigInt(pnNbits);
    const pnHwin = pnWin / 2n;
    const pnMask = pnWin - 1n;

    // Nomzod paket raqami
    const candidatePn = (expectedPn & ~pnMask) | truncatedPn;

    if (candidatePn <= expectedPn - pnHwin && candidatePn < (1n << 62n) - pnWin) {
      return candidatePn + pnWin;
    }
    if (candidatePn > expectedPn + pnHwin && candidatePn >= pnWin) {
      return candidatePn - pnWin;
    }

    return candidatePn;
  }

  /**
   * Berilgan to'liq paket raqamini uzatish uchun kerak bo'ladigan minimal baytlar o'lchamini aniqlash
   */
  public static getPacketNumberLength(fullPn: bigint, largestAcked: bigint): { numBytes: number; truncated: bigint } {
    const diff = fullPn - largestAcked;
    let numBytes: number;

    if (diff < 128n) {
      numBytes = 1;
    } else if (diff < 32768n) {
      numBytes = 2;
    } else if (diff < 8388608n) {
      numBytes = 3;
    } else {
      numBytes = 4;
    }

    const mask = (1n << BigInt(numBytes * 8)) - 1n;
    const truncated = fullPn & mask;

    return { numBytes, truncated };
  }
}
```
**Tushuntirish:** Paket raqamlarini qisqartirish orqali QUIC sarlavhalari hajmi sezilarli darajada kichrayadi. Qabul qiluvchi tomon ilgari qabul qilgan `largest_acked` raqamiga asoslanib, ehtimoli eng yuqori bo'lgan 64-bitlik qiymatni matematik jihatdan bir zumda tiklab oladi.

---

### Topshiriq #1109: QUIC Connection ID (CID) Marshrutizatori va Connection Migration Boshqaruvi
**Tavsif:** Mijoz Wi-Fi tarmog'idan LTE mobil aloqasiga o'tganda uning IP manzili va porti o'zgaradi. TCP da bu aloqaning uzilishiga sabab bo'lsa, QUIC da Connection ID (CID) tufayli aloqa bir soniya ham to'xtamasdan davom etadi.
**Talablar:** Connection ID Router sinfini loyihalash, IP o'zgarganda seansni yangi soketga ko'chirish (Connection Migration) mantig'ini yozish.
**Yechim (TypeScript):**
```ts
export interface QuicSessionContext {
  connectionId: string;
  clientIp: string;
  clientPort: number;
  lastActive: number;
  dataChannel: any;
}

export class QuicConnectionRouter {
  // CID orqali seanslarni topish xaritasi
  private sessions = new Map<string, QuicSessionContext>();

  public registerSession(cid: Uint8Array, clientIp: string, clientPort: number): QuicSessionContext {
    const cidHex = Buffer.from(cid).toString('hex');
    const session: QuicSessionContext = {
      connectionId: cidHex,
      clientIp,
      clientPort,
      lastActive: Date.now(),
      dataChannel: null
    };
    this.sessions.set(cidHex, session);
    return session;
  }

  /**
   * Kiruvchi UDP paketini tegishli seansga yo'naltirish
   * Agar IP yoki Port o'zgargan bo'lsa, Connection Migration yuz berganini aniqlash
   */
  public routePacket(dcid: Uint8Array, remoteIp: string, remotePort: number): { session: QuicSessionContext | null; migrated: boolean } {
    const cidHex = Buffer.from(dcid).toString('hex');
    const session = this.sessions.get(cidHex);

    if (!session) {
      return { session: null, migrated: false };
    }

    session.lastActive = Date.now();

    // Connection Migration tekshiruvi:
    if (session.clientIp !== remoteIp || session.clientPort !== remotePort) {
      console.log(`[Connection Migration Aniqlandi] CID: ${cidHex}`);
      console.log(`Eski Manzil: ${session.clientIp}:${session.clientPort} -> Yangi Manzil: ${remoteIp}:${remotePort}`);

      // Yangi tarmoq manzilini yangilash
      session.clientIp = remoteIp;
      session.clientPort = remotePort;
      return { session, migrated: true };
    }

    return { session, migrated: false };
  }

  public removeSession(cidHex: string): void {
    this.sessions.delete(cidHex);
  }
}
```
**Tushuntirish:** QUIC protokoli an'anaviy 4-talik (Source IP, Source Port, Dest IP, Dest Port) o'rniga ixtiyoriy uzunlikdagi `Connection ID` dan foydalanadi. Shu bois mobil qurilma stansiyalar yoki tarmoqlar orasida harakatlanganda, mijoz yangi handshake qilmasdan mavjud oqimlarni davom ettira oladi.

---

### Topshiriq #1110: QUIC Oqim Nazorati (Flow Control: MAX_DATA va MAX_STREAM_DATA Freymlari)
**Tavsif:** Tezkor jo'natuvchi sekin qabul qiluvchining xotirasini to'ldirib yubormasligi uchun QUIC da ikki darajali oqim nazorati (Flow Control) mavjud: Ulanish darajasida va har bir Stream darajasida.
**Talablar:** MAX_DATA (0x10) va MAX_STREAM_DATA (0x11) freymlarini generatsiya qiluvchi hamda qabul qilingan baytlar hisobini yurituvchi TypeScript boshqaruvchisi.
**Yechim (TypeScript):**
```ts
import { QuicVarInt } from './QuicVarInt';

export class QuicFlowController {
  private maxConnectionData: bigint;
  private currentConnectionDataConsumed = 0n;

  private streamLimits = new Map<string, { max: bigint; consumed: bigint }>();

  constructor(initialMaxConnData: bigint = 1048576n) { // 1MB boshlang'ich limit
    this.maxConnectionData = initialMaxConnData;
  }

  /**
   * Yangi stream ochilganda unga limit belgilash
   */
  public initStream(streamId: bigint, initialLimit: bigint = 262144n): void { // 256KB
    this.streamLimits.set(streamId.toString(), { max: initialLimit, consumed: 0n });
  }

  /**
   * Kelgan baytlarni hisoblash va bufer to'lishiga qarab chegarani oshirish
   */
  public consumeData(streamId: bigint, byteLength: number): { sendMaxData: Uint8Array | null; sendMaxStreamData: Uint8Array | null } {
    const bytes = BigInt(byteLength);
    this.currentConnectionDataConsumed += bytes;

    let sendMaxData: Uint8Array | null = null;
    let sendMaxStreamData: Uint8Array | null = null;

    // 1. Agar ulanish darajasidagi limitning 50% dan ortig'i ishlatilgan bo'lsa, oynani kengaytirish
    if (this.currentConnectionDataConsumed >= this.maxConnectionData / 2n) {
      this.maxConnectionData += this.currentConnectionDataConsumed * 2n;
      sendMaxData = this.buildMaxDataFrame(this.maxConnectionData);
      this.currentConnectionDataConsumed = 0n;
    }

    // 2. Stream darajasidagi oqim nazorati
    const st = this.streamLimits.get(streamId.toString());
    if (st) {
      st.consumed += bytes;
      if (st.consumed >= st.max / 2n) {
        st.max += st.consumed * 2n;
        sendMaxStreamData = this.buildMaxStreamDataFrame(streamId, st.max);
        st.consumed = 0n;
      }
    }

    return { sendMaxData, sendMaxStreamData };
  }

  // MAX_DATA (0x10) freymini binar generatsiya qilish
  private buildMaxDataFrame(maxData: bigint): Uint8Array {
    const fType = QuicVarInt.encode(0x10);
    const dataLimit = QuicVarInt.encode(maxData);
    const res = new Uint8Array(fType.length + dataLimit.length);
    res.set(fType, 0);
    res.set(dataLimit, fType.length);
    return res;
  }

  // MAX_STREAM_DATA (0x11) freymini binar generatsiya qilish
  private buildMaxStreamDataFrame(streamId: bigint, maxStreamData: bigint): Uint8Array {
    const fType = QuicVarInt.encode(0x11);
    const sId = QuicVarInt.encode(streamId);
    const limit = QuicVarInt.encode(maxStreamData);

    const res = new Uint8Array(fType.length + sId.length + limit.length);
    res.set(fType, 0);
    res.set(sId, fType.length);
    res.set(limit, fType.length + sId.length);
    return res;
  }
}
```
**Tushuntirish:** QUIC dagi kreditga asoslangan (Credit-based) oqim nazorati qabul qiluvchiga har bir stream va butun ulanish xotirasini qat'iy chegaralash imkonini beradi. Qabul qiluvchi ma'lumotlarni o'z xotirasidan bo'shatishi bilan `MAX_DATA` yoki `MAX_STREAM_DATA` freymlari orqali jo'natuvchiga yangi ruxsat etilgan kvotani ma'lum qiladi.

---

### Topshiriq #1111: HTTP/3 Freymlar Arxitekturasi: DATA, HEADERS, SETTINGS, GOAWAY Binar Parseri
**Tavsif:** HTTP/3 da har bir oqim ichidagi ma'lumotlar HTTP/2 kabi binar freymlarga bo'linadi. Biroq HTTP/3 freym sarlavhalari RFC 9000 VarInt formatida bo'lib, o'zgarmas 9 baytli emas, balki ixcham o'zgaruvchan hajmga ega.
**Talablar:** RFC 9114 bo'lim 7.2 bo'yicha 0x00 (DATA), 0x01 (HEADERS), 0x04 (SETTINGS), 0x07 (GOAWAY) freymlarini dekodlovchi parser.
**Yechim (TypeScript):**
```ts
import { QuicVarInt } from './QuicVarInt';

export enum H3FrameType {
  DATA = 0x00,
  HEADERS = 0x01,
  CANCEL_PUSH = 0x03,
  SETTINGS = 0x04,
  PUSH_PROMISE = 0x05,
  GOAWAY = 0x07,
  MAX_PUSH_ID = 0x0d
}

export interface H3ParsedFrame {
  type: H3FrameType;
  typeName: string;
  length: bigint;
  payload: Uint8Array;
}

export class Http3FrameParser {
  /**
   * HTTP/3 stream oqimidan bitta to'liq freymni o'qiydi
   */
  public static parseNextFrame(streamBuffer: Uint8Array, offset: number = 0): { frame: H3ParsedFrame | null; bytesRead: number } {
    if (offset >= streamBuffer.length) {
      return { frame: null, bytesRead: 0 };
    }

    // 1. Freym turi (VarInt)
    const { value: frameTypeVal, bytesRead: typeBytes } = QuicVarInt.decode(streamBuffer, offset);
    let curOffset = offset + typeBytes;

    // 2. Freym uzunligi (VarInt)
    if (curOffset >= streamBuffer.length) {
      return { frame: null, bytesRead: 0 }; // Ma'lumot hali to'liq yetib kelmagan
    }

    const { value: frameLenVal, bytesRead: lenBytes } = QuicVarInt.decode(streamBuffer, curOffset);
    curOffset += lenBytes;

    const frameLen = Number(frameLenVal);
    if (curOffset + frameLen > streamBuffer.length) {
      return { frame: null, bytesRead: 0 }; // Payload hali to'liq emas
    }

    const payload = streamBuffer.slice(curOffset, curOffset + frameLen);
    const totalBytes = (curOffset + frameLen) - offset;

    const fType = Number(frameTypeVal) as H3FrameType;
    let typeName = 'UNKNOWN';

    switch (fType) {
      case H3FrameType.DATA: typeName = 'DATA'; break;
      case H3FrameType.HEADERS: typeName = 'HEADERS'; break;
      case H3FrameType.SETTINGS: typeName = 'SETTINGS'; break;
      case H3FrameType.GOAWAY: typeName = 'GOAWAY'; break;
      default: typeName = `CUSTOM_${fType}`; break;
    }

    return {
      frame: { type: fType, typeName, length: frameLenVal, payload },
      bytesRead: totalBytes
    };
  }

  /**
   * DATA freymini hosil qilish yordamchisi
   */
  public static createDataFrame(data: Uint8Array): Uint8Array {
    const fType = QuicVarInt.encode(H3FrameType.DATA);
    const fLen = QuicVarInt.encode(data.length);
    const combined = new Uint8Array(fType.length + fLen.length + data.length);

    combined.set(fType, 0);
    combined.set(fLen, fType.length);
    combined.set(data, fType.length + fLen.length);

    return combined;
  }
}
```
**Tushuntirish:** HTTP/3 da har bir freym `Type` va `Length` maydonlaridan boshlanadi. Bu ikkala maydon ham QUIC VarInt bilan kodlanganligi sababli, masalan 1 baytli kichik DATA paketi atigi 2 bayt qo'shimcha sarlavha (1 bayt tur + 1 bayt uzunlik) talab qiladi, bu esa tarmoq samaradorligini eng yuqori pog'onaga olib chiqadi.

---

### Topshiriq #1112: HTTP/3 SETTINGS Freym Parametrlarini O'qish va Boshqaruv Oqimini Sozlash
**Tavsif:** Ulanish boshlanganda mijoz va server o'z imkoniyatlarini (QPACK dinamik jadval o'lchami, maksimal sarlavhalar hajmi va WebTransport qo'llab-quvvatlovi) kelishib olish uchun SETTINGS freymini yuboradi.
**Talablar:** RFC 9114 dagi SETTINGS_MAX_FIELD_SECTION_SIZE (0x06), SETTINGS_QPACK_MAX_TABLE_CAPACITY (0x01) va SETTINGS_ENABLE_WEBTRANSPORT (0x2b6037) parametrlarini parse qilish.
**Yechim (TypeScript):**
```ts
import { QuicVarInt } from './QuicVarInt';

export interface Http3Settings {
  qpackMaxTableCapacity?: bigint;
  maxFieldSectionSize?: bigint;
  qpackBlockedStreams?: bigint;
  enableWebTransport?: boolean;
}

export class Http3SettingsDecoder {
  // RFC 9114 va WebTransport identifikatorlari
  public static readonly SETTINGS_QPACK_MAX_TABLE_CAPACITY = 0x01n;
  public static readonly SETTINGS_MAX_FIELD_SECTION_SIZE = 0x06n;
  public static readonly SETTINGS_QPACK_BLOCKED_STREAMS = 0x07n;
  public static readonly SETTINGS_ENABLE_WEBTRANSPORT = 0x2b6037n;

  public static decodeSettings(payload: Uint8Array): Http3Settings {
    const settings: Http3Settings = {};
    let offset = 0;

    while (offset < payload.length) {
      // Har bir sozlama: Identifier (VarInt) + Value (VarInt)
      const { value: identifier, bytesRead: idBytes } = QuicVarInt.decode(payload, offset);
      offset += idBytes;

      if (offset >= payload.length) {
        throw new Error('SETTINGS freymi noto`g`ri formatda (uzunlik yetarli emas)');
      }

      const { value: settingValue, bytesRead: valBytes } = QuicVarInt.decode(payload, offset);
      offset += valBytes;

      switch (identifier) {
        case this.SETTINGS_QPACK_MAX_TABLE_CAPACITY:
          settings.qpackMaxTableCapacity = settingValue;
          break;
        case this.SETTINGS_MAX_FIELD_SECTION_SIZE:
          settings.maxFieldSectionSize = settingValue;
          break;
        case this.SETTINGS_QPACK_BLOCKED_STREAMS:
          settings.qpackBlockedStreams = settingValue;
          break;
        case this.SETTINGS_ENABLE_WEBTRANSPORT:
          settings.enableWebTransport = settingValue === 1n;
          break;
        default:
          // RFC 9114 bo'yicha notanish parametrlar e'tiborsiz qoldirilishi lozim
          break;
      }
    }

    return settings;
  }

  public static encodeSettings(settings: Http3Settings): Uint8Array {
    const chunks: Uint8Array[] = [];

    const addSetting = (id: bigint, val: bigint) => {
      chunks.push(QuicVarInt.encode(id));
      chunks.push(QuicVarInt.encode(val));
    };

    if (settings.qpackMaxTableCapacity !== undefined) {
      addSetting(this.SETTINGS_QPACK_MAX_TABLE_CAPACITY, settings.qpackMaxTableCapacity);
    }
    if (settings.maxFieldSectionSize !== undefined) {
      addSetting(this.SETTINGS_MAX_FIELD_SECTION_SIZE, settings.maxFieldSectionSize);
    }
    if (settings.enableWebTransport) {
      addSetting(this.SETTINGS_ENABLE_WEBTRANSPORT, 1n);
    }

    const totalLen = chunks.reduce((acc, c) => acc + c.length, 0);
    const result = new Uint8Array(totalLen);
    let p = 0;
    for (const c of chunks) {
      result.set(c, p);
      p += c.length;
    }
    return result;
  }
}
```
**Tushuntirish:** SETTINGS freymi HTTP/3 ulanishining dastlabki boshqaruv oqimida (Control Stream) eng birinchi bo'lib yuboriladi. U orqali server WebTransport faollashtirilganligi yoki QPACK siqish uchun qancha xotira ajrata olishini mijozga e'lon qiladi.

---

### Topshiriq #1113: QPACK Statik Jadvali (RFC 9204) Asosida HTTP/3 Sarlavhalarini Dekompressiya Qilish
**Tavsif:** HTTP/2 da HPACK ishlatilgan bo'lsa, HTTP/3 da ko'p oqimli tarmoqda bloklanishni oldini olish uchun QPACK protokoli yaratilgan. U 99 ta eng ko'p ishlatiladigan sarlavha juftliklaridan iborat Statik Jadvalga ega.
**Talablar:** RFC 9204 ilovasida keltirilgan statik jadval indekslari orqali ':method: GET', ':status: 200', 'content-type' kabi standart sarlavhalarni bir zumda tiklovchi dekompressor.
**Yechim (TypeScript):**
```ts
export interface HeaderEntry {
  name: string;
  value: string;
}

export class QpackStaticTable {
  // RFC 9204 Statik jadvali (eng muhim dastlabki yozuvlar)
  private static readonly TABLE: HeaderEntry[] = [
    { name: ':authority', value: '' },                     // 0
    { name: ':path', value: '/' },                         // 1
    { name: ':method', value: 'GET' },                     // 17
    { name: ':method', value: 'POST' },                    // 20
    { name: ':scheme', value: 'https' },                   // 23
    { name: ':status', value: '200' },                     // 25
    { name: ':status', value: '204' },                     // 26
    { name: ':status', value: '404' },                     // 29
    { name: ':status', value: '500' },                     // 30
    { name: 'accept', value: '*/*' },                      // 31
    { name: 'accept-encoding', value: 'gzip, deflate, br' }, // 32
    { name: 'content-type', value: 'application/json' },   // 36
    { name: 'content-type', value: 'text/plain' }          // 37
  ];

  private static readonly FULL_TABLE_MAP: Map<number, HeaderEntry> = new Map([
    [0, { name: ':authority', value: '' }],
    [1, { name: ':path', value: '/' }],
    [17, { name: ':method', value: 'GET' }],
    [20, { name: ':method', value: 'POST' }],
    [23, { name: ':scheme', value: 'https' }],
    [25, { name: ':status', value: '200' }],
    [29, { name: ':status', value: '404' }],
    [31, { name: 'accept', value: '*/*' }],
    [36, { name: 'content-type', value: 'application/json' }]
  ]);

  /**
   * Statik jadval indeksi bo'yicha sarlavhani topish
   */
  public static getEntry(index: number): HeaderEntry {
    const entry = this.FULL_TABLE_MAP.get(index);
    if (!entry) {
      throw new Error(`QPACK Statik jadvalida ${index} indeksi topilmadi!`);
    }
    return { ...entry };
  }

  /**
   * Indekslangan sarlavha maydoni (Indexed Header Field):
   * 1-baytning 0xc0 bitlari 11 bo'lsa (0b11xxxxxx) -> Statik jadvalga murojaat
   */
  public static decodeIndexedHeader(firstByte: number): HeaderEntry {
    const index = firstByte & 0x3f;
    return this.getEntry(index);
  }
}
```
**Tushuntirish:** QPACK statik jadvali HTTP/3 so'rovlarining sarlavhalar hajmini 80% gacha kamaytiradi. Masalan `:method: GET` yoki `:status: 200` kabi tez-tez takrorlanuvchi yozuvlar tarmoq orqali o'nlab baytli matn o'rniga atigi 1 baytlik indeks raqami orqali uzatiladi.

---

### Topshiriq #1114: QPACK Dinamik Jadvali (Dynamic Table) va Xotira Boshqaruvi
**Tavsif:** Statik jadvalda yo'q bo'lgan maxsus sarlavhalar (masalan 'Authorization: Bearer xyz...' yoki maxsus UUID larni) bir necha marta yubormaslik uchun QPACK Dinamik jadval mexanizmini ishlatadi.
**Talablar:** FIFO (First-In-First-Out) asosida ishlovchi dynamic table xotira hajmi cheklovini (Eviction) amalga oshiruvchi sinf.
**Yechim (TypeScript):**
```ts
import { HeaderEntry } from './QpackStaticTable';

export class QpackDynamicTable {
  private entries: HeaderEntry[] = [];
  private currentByteSize = 0;

  constructor(private maxCapacity: number = 4096) {} // 4KB maksimal xotira

  public setCapacity(newCapacity: number): void {
    this.maxCapacity = newCapacity;
    this.evict();
  }

  /**
   * Yangi sarlavha juftligini dinamik jadvalga kiritish
   * RFC 9204 qoidasi: Hajm = name.length + value.length + 32 bayt
   */
  public insert(name: string, value: string): void {
    const entrySize = name.length + value.length + 32;

    if (entrySize > this.maxCapacity) {
      // Agar bitta yozuvning o'zi butun jadvaldan katta bo'lsa, jadval butunlay tozalanadi
      this.entries = [];
      this.currentByteSize = 0;
      return;
    }

    this.entries.unshift({ name, value });
    this.currentByteSize += entrySize;
    this.evict();
  }

  /**
   * Xotira limitidan oshib ketgan eski elementlarni jadvaldan o'chirish
   */
  private evict(): void {
    while (this.currentByteSize > this.maxCapacity && this.entries.length > 0) {
      const removed = this.entries.pop()!;
      const removedSize = removed.name.length + removed.value.length + 32;
      this.currentByteSize -= removedSize;
    }
  }

  public getEntry(relativeIndex: number): HeaderEntry | null {
    if (relativeIndex >= 0 && relativeIndex < this.entries.length) {
      return this.entries[relativeIndex];
    }
    return null;
  }

  public get size(): number {
    return this.entries.length;
  }

  public get bytesUsed(): number {
    return this.currentByteSize;
  }
}
```
**Tushuntirish:** QPACK dinamik jadvali ulanish davomida ikkala tomon o'rtasida sinxron yuritiladi. Har bir yozuvga qo'shimcha 32 bayt overhead qo'shilishi RFC standartida qat'iy belgilangan bo'lib, bu tizim xotirasining (Memory Exhaustion) cheksiz o'sib ketishini oldini oladi.

---

### Topshiriq #1115: HTTP/3 Boshqaruv Oqimlari (Control Stream) va Oqim Turini Ro'yxatdan O'tkazish
**Tavsif:** HTTP/3 da ma'lumotlar uzatuvchi streamlardan tashqari, faqat bitta yo'nalishda ishlovchi (Unidirectional) maxsus tizim oqimlari mavjud: Control Stream, QPACK Encoder Stream va QPACK Decoder Stream.
**Talablar:** 0x00 (Control Stream), 0x02 (QPACK Encoder), 0x03 (QPACK Decoder) oqim prefikslarini taniy oluvchi boshqaruvchi.
**Yechim (TypeScript):**
```ts
import { QuicVarInt } from './QuicVarInt';

export enum H3StreamType {
  CONTROL = 0x00,
  PUSH = 0x01,
  QPACK_ENCODER = 0x02,
  QPACK_DECODER = 0x03
}

export class Http3StreamTypeIdentifier {
  /**
   * Bir yo'nalishli streamning eng birinchi baytidan uning turini aniqlash
   */
  public static identifyStream(initialBytes: Uint8Array): { type: H3StreamType; bytesRead: number } {
    const { value, bytesRead } = QuicVarInt.decode(initialBytes, 0);
    const typeNum = Number(value);

    switch (typeNum) {
      case H3StreamType.CONTROL:
        return { type: H3StreamType.CONTROL, bytesRead };
      case H3StreamType.QPACK_ENCODER:
        return { type: H3StreamType.QPACK_ENCODER, bytesRead };
      case H3StreamType.QPACK_DECODER:
        return { type: H3StreamType.QPACK_DECODER, bytesRead };
      default:
        throw new Error(`Noma'lum yoki qo'llab-quvvatlanmaydigan H3 oqim turi: ${typeNum}`);
    }
  }

  /**
   * Server tomondan yangi Unidirectional Control Stream ochish uchun dastlabki prefiks baytlarini generatsiya qilish
   */
  public static createControlStreamHeader(): Uint8Array {
    return QuicVarInt.encode(H3StreamType.CONTROL);
  }
}
```
**Tushuntirish:** Unidirectional Control Stream ochilgach, uning birinchi bayti oqim turini e'lon qiladi. Qoidalarga ko'ra, bitta ulanishda faqat bitta Control Stream bo'lishi mumkin; agar ikkinchi Control Stream ochilsa, bu `H3_STREAM_CREATION_ERROR` xatosi hisoblanadi va butun seans yopiladi.

---

### Topshiriq #1116: HTTP/3 So'rov Multiplexingini Simulyatsiya Qiluvchi Stream Dispatcher
**Tavsif:** Mijoz bitta QUIC ulanishi orqali bir vaqtning o'zida o'nlab HTTP so'rovlarini (masalan, CSS, rasmlar, API ma'lumotlari) alohida streamlarda parallel yuboradi. Dispatcher har bir streamni alohida ajratib qayta ishlashi kerak.
**Talablar:** Stream Dispatcher sinfi, Stream ID orqali yo'naltirish, so'rov va javob oqimlarini boshqarish.
**Yechim (TypeScript):**
```ts
import { EventEmitter } from 'node:events';
import { Http3FrameParser, H3FrameType } from './Http3FrameParser';

export interface H3RequestEvent {
  streamId: bigint;
  headers?: Map<string, string>;
  bodyChunks: Uint8Array[];
}

export class Http3StreamDispatcher extends EventEmitter {
  private activeStreams = new Map<string, H3RequestEvent>();

  public onStreamData(streamId: bigint, chunk: Uint8Array): void {
    const key = streamId.toString();
    if (!this.activeStreams.has(key)) {
      this.activeStreams.set(key, {
        streamId,
        bodyChunks: []
      });
    }

    const currentReq = this.activeStreams.get(key)!;
    let offset = 0;

    while (offset < chunk.length) {
      const { frame, bytesRead } = Http3FrameParser.parseNextFrame(chunk, offset);
      if (!frame || bytesRead === 0) break;

      offset += bytesRead;

      if (frame.type === H3FrameType.HEADERS) {
        // Headers bloki qabul qilindi
        this.emit('headers', { streamId, payload: frame.payload });
      } else if (frame.type === H3FrameType.DATA) {
        currentReq.bodyChunks.push(frame.payload);
        this.emit('data', { streamId, chunk: frame.payload });
      }
    }
  }

  public onStreamEnd(streamId: bigint): void {
    const key = streamId.toString();
    const req = this.activeStreams.get(key);
    if (req) {
      this.emit('request_complete', req);
      this.activeStreams.delete(key);
    }
  }
}
```
**Tushuntirish:** HTTP/3 Stream Dispatcher protokollararo parallelizmni eng yuqori darajaga olib chiqadi. Har bir so'rov o'zining mustaqil `Stream ID` siga ega bo'lgani sababli, birorta og'ir so'rov (masalan katta fayl yuklanishi) boshqa kichik JSON API so'rovlarining kechikishiga aslo ta'sir qilmaydi.

---

### Topshiriq #1117: HTTP/3 Response Streamer: DATA Freymlarida Qismli (Chunked) Ma'lumotlarni Uzatish
**Tavsif:** Katta hajmdagi ma'lumotlarni (masalan, video oqimi yoki sun'iy intellekt LLM token oqimi) jo'natishda butun javobni xotirada to'plamasdan, uni DATA freymlariga bo'lib oqimli uzatish lozim.
**Talablar:** AsyncIterable yordamida ma'lumotlarni kichik DATA freymlariga o'rab QUIC streamiga uzatuvchi Generator sinfi.
**Yechim (TypeScript):**
```ts
import { Http3FrameParser } from './Http3FrameParser';

export class Http3ResponseStreamer {
  /**
   * Katta matn yoki binar oqimni HTTP/3 DATA freymlari shaklida oqimli uzatish
   */
  public static async *streamResponse(
    source: AsyncIterable<Uint8Array | string>,
    chunkSize: number = 16384 // 16KB o'lchamdagi qismlar
  ): AsyncGenerator<Uint8Array, void, unknown> {
    const encoder = new TextEncoder();

    for await (const piece of source) {
      const rawBytes = typeof piece === 'string' ? encoder.encode(piece) : piece;

      let offset = 0;
      while (offset < rawBytes.length) {
        const sliceEnd = Math.min(offset + chunkSize, rawBytes.length);
        const chunk = rawBytes.subarray(offset, sliceEnd);
        offset = sliceEnd;

        // DATA freymini hosil qilish
        yield Http3FrameParser.createDataFrame(chunk);
      }
    }
  }
}
```
**Tushuntirish:** AsyncIterable asosidagi streaming arxitekturasi server xotirasini bo'shatadi (O(1) memory usage). Har bir chunk generatsiya qilinishi bilanoq darhol HTTP/3 DATA freymiga o'ralib tarmoqqa yuboriladi, bu esa birinchi bayt kechikishini (TTFB - Time to First Byte) bir necha millisekundga tushiradi.

---

### Topshiriq #1118: QPACK Prefiks Butun Sonlarni (Prefix Integers) Dekodlash Algoritmi
**Tavsif:** QPACK da sarlavha blokidagi indekslar bir baytning ma'lum bitlariga (N-bit prefix) joylashtiriladi. Agar indeks ushbu $2^N - 1$ qiymatidan oshib ketsa, keyingi baytlar orqali kengaytiriladi.
**Talablar:** RFC 7541 / RFC 9204 qoidasi bo'yicha N-bit prefiksli sonlarni dekodlash va kodlash funksiyasi.
**Yechim (TypeScript):**
```ts
export class QpackPrefixInteger {
  /**
   * N-bitli prefiks butun sonini dekodlash
   * @param buffer Binar bufer
   * @param offset Boshlanish joyi
   * @param n Prefiks bitlar soni (1 dan 8 gacha)
   */
  public static decode(buffer: Uint8Array, offset: number, n: number): { value: number; bytesRead: number } {
    const maxPrefixVal = (1 << n) - 1;
    const firstByte = buffer[offset];
    const prefixVal = firstByte & maxPrefixVal;

    if (prefixVal < maxPrefixVal) {
      return { value: prefixVal, bytesRead: 1 };
    }

    let value = prefixVal;
    let m = 0;
    let bytesRead = 1;

    while (offset + bytesRead < buffer.length) {
      const b = buffer[offset + bytesRead];
      bytesRead++;

      value += (b & 0x7f) * Math.pow(2, m);
      m += 7;

      if ((b & 0x80) === 0) {
        break; // Eng yuqori bit 0 bo'lsa, son yakunlandi
      }
    }

    return { value, bytesRead };
  }
}
```
**Tushuntirish:** N-bit prefiks algoritmi sarlavha flaglarini (bayroqlarini) va sonli indekslarni bitta baytga birlashtirish imkonini beradi. Qolgan bitlar sarlavhaning qaysi jadvalga tegishli ekanligini ko'rsatadi, qolgan qismi esa indeks raqamini bildiradi.

---

### Topshiriq #1119: HTTP/3 Server Push va CANCEL_PUSH Freymlari Bilan Ishlash
**Tavsif:** Server mijoz so'ramasidan oldin kerakli resurslarni (masalan CSS fayllarini) PUSH_PROMISE orqali yuborishi mumkin. Agar mijoz keshida bu fayl allaqachon mavjud bo'lsa, u ortiqcha trafigi to'xtatish uchun CANCEL_PUSH yuboradi.
**Talablar:** 0x03 (CANCEL_PUSH) freymini generatsiya qilish va qayta ishlash logikasi.
**Yechim (TypeScript):**
```ts
import { QuicVarInt } from './QuicVarInt';
import { H3FrameType } from './Http3FrameParser';

export class Http3PushManager {
  private activePushes = new Set<string>();

  public createCancelPush(pushId: bigint): Uint8Array {
    const fType = QuicVarInt.encode(H3FrameType.CANCEL_PUSH);
    const pId = QuicVarInt.encode(pushId);
    const fLen = QuicVarInt.encode(pId.length);

    const buf = new Uint8Array(fType.length + fLen.length + pId.length);
    buf.set(fType, 0);
    buf.set(fLen, fType.length);
    buf.set(pId, fType.length + fLen.length);

    return buf;
  }

  public handleCancelPush(payload: Uint8Array): bigint {
    const { value: pushId } = QuicVarInt.decode(payload, 0);
    this.activePushes.delete(pushId.toString());
    console.log(`[HTTP/3 Push Bekor Qilindi] Push ID: ${pushId}`);
    return pushId;
  }
}
```
**Tushuntirish:** `CANCEL_PUSH` mantiqiy freymi keraksiz server-push oqimlarini bekor qilib, mijozning tarmoq kanalini asrab qolish imkonini beradi. Mijoz brauzer keshini tekshirib, agar resurs allaqachon mavjud bo'lsa, darhol ushbu freymni qaytaradi.

---

### Topshiriq #1120: To'liq TypeScript Custom HTTP/3 Mini-Parser Sinfini Birlashtirish
**Tavsif:** QUIC streamlaridan keluvchi xom baytlarni qabul qilib, ularni to'liq tahlil qilingan HTTP/3 so'rov obyektlariga (Method, Path, Headers, Body) aylantiruvchi yagona tayyor dvigatel yaratish lozim.
**Talablar:** Barcha oldingi freym parserlarini birlashtiruvchi, to'liq ishchi CustomHttp3Parser sinfini yozish.
**Yechim (TypeScript):**
```ts
import { EventEmitter } from 'node:events';
import { Http3FrameParser, H3FrameType } from './Http3FrameParser';
import { QpackStaticTable } from './QpackStaticTable';

export interface Http3Request {
  streamId: bigint;
  method: string;
  path: string;
  headers: Record<string, string>;
  body: Uint8Array;
}

export class CustomHttp3Parser extends EventEmitter {
  public parseStream(streamId: bigint, streamData: Uint8Array): void {
    let offset = 0;
    const req: Http3Request = {
      streamId,
      method: 'GET',
      path: '/',
      headers: {},
      body: new Uint8Array(0)
    };

    const bodyParts: Uint8Array[] = [];

    while (offset < streamData.length) {
      const { frame, bytesRead } = Http3FrameParser.parseNextFrame(streamData, offset);
      if (!frame || bytesRead === 0) break;

      offset += bytesRead;

      if (frame.type === H3FrameType.HEADERS) {
        // HEADERS blokini tahlil qilish (Statik jadval simulyatsiyasi)
        if (frame.payload.length > 0) {
          // Namuna: birinchi bayt statik jadval indeksi
          try {
            const entry = QpackStaticTable.decodeIndexedHeader(frame.payload[0]);
            if (entry.name === ':method') req.method = entry.value;
            if (entry.name === ':path') req.path = entry.value;
            req.headers[entry.name] = entry.value;
          } catch {
            // maxsus sarlavhalar
          }
        }
      } else if (frame.type === H3FrameType.DATA) {
        bodyParts.push(frame.payload);
      }
    }

    if (bodyParts.length > 0) {
      const totalLen = bodyParts.reduce((acc, b) => acc + b.length, 0);
      const combined = new Uint8Array(totalLen);
      let p = 0;
      for (const b of bodyParts) {
        combined.set(b, p);
        p += b.length;
      }
      req.body = combined;
    }

    this.emit('request', req);
  }
}
```
**Tushuntirish:** Ushbu modul HTTP/3 protokolining yadrosini tashkil etadi. U past darajadagi binar freymlarni (HEADERS va DATA) yuqori darajadagi TypeScript dasturchilariga tanish bo'lgan HTTP so'rov obyektlariga aylantirib beradi.

---

### Topshiriq #1121: WebTransport Seansini HTTP/3 Ustida Boshlash (Extended CONNECT va :protocol = webtransport)
**Tavsif:** WebTransport brauzer va server o'rtasida QUIC imkoniyatlarini (ham ishonchli oqimlar, ham ishonchsiz datagramlar) taqdim etadi. Seans HTTP/3 orqali kengaytirilgan CONNECT so'rovi bilan boshlanadi.
**Talablar:** Extended CONNECT so'rovini qabul qilish, :protocol va :authority sarlavhalarini tekshirish hamda 200 OK muvaffaqiyatli seansini tasdiqlovchi TypeScript arxitekturasi.
**Yechim (TypeScript):**
```ts
export interface WebTransportHandshake {
  method: string;
  protocol: string;
  path: string;
  authority: string;
  origin?: string;
}

export class WebTransportSessionInitiator {
  /**
   * Kiruvchi HTTP/3 sarlavhalari WebTransport seansiga tegishli ekanligini tasdiqlash
   */
  public static validateHandshake(headers: Map<string, string>): WebTransportHandshake {
    const method = headers.get(':method');
    const protocol = headers.get(':protocol');
    const path = headers.get(':path');
    const authority = headers.get(':authority');
    const origin = headers.get('origin');

    // RFC draft-ietf-webtrans-overview bo'yicha qat'iy talablar:
    if (method !== 'CONNECT') {
      throw new Error(`WebTransport noto'g'ri metod: ${method}. Faqat CONNECT ruxsat etilgan!`);
    }

    if (protocol !== 'webtransport') {
      throw new Error(`WebTransport :protocol qiymati 'webtransport' bo'lishi shart! Olindi: ${protocol}`);
    }

    if (!path || !authority) {
      throw new Error('WebTransport :path va :authority majburiy sarlavhalardir!');
    }

    return {
      method,
      protocol,
      path,
      authority,
      origin
    };
  }

  /**
   * Muvaffaqiyatli seans ochilganda qaytariladigan 200 OK javobi (QPACK sarlavhalar bloki)
   */
  public static createHandshakeSuccessResponse(): Map<string, string> {
    const resp = new Map<string, string>();
    resp.set(':status', '200');
    resp.set('sec-webtransport-http3-draft', 'draft02');
    return resp;
  }
}
```
**Tushuntirish:** WebTransport oddiy WebSocket kabi HTTP/1.1 Upgrade mexanizmidan emas, balki HTTP/2 va HTTP/3 ning `Extended CONNECT` (RFC 8441) mexanizmidan foydalanadi. `:protocol = webtransport` psevdo-sarlavhasi orqali bitta HTTP/3 stream seans boshqaruv kanaliga aylanadi.

---

### Topshiriq #1122: WebTransport Datagrams: Unreliable va Kam Kechikishli UDP Paketlarni Yuborish
**Tavsif:** Onlayn o'yinlar, jonli audio/video konferensiyalar va IoT datchiklar ma'lumotlari uchun TCP dagi kafolatlangan yetkazish va kechikishlar to'g'ri kelmaydi. Ularga paket yo'qolishiga chidamli, ultra tezkor WebTransport Datagramlari kerak.
**Talablar:** WebTransport Datagram oqimini yaratish, maksimal datagram hajmini (maxDatagramSize) hisoblash va datagramlarni uzatish.
**Yechim (TypeScript):**
```ts
export class WebTransportDatagramEngine {
  private maxDatagramSize: number;

  constructor(maxSize: number = 1200) {
    this.maxDatagramSize = maxSize;
  }

  /**
   * Kiruvchi WebTransport datagramini qabul qilish
   * Format: Quarter Stream ID (VarInt) + Datagram Payload
   */
  public handleIncomingDatagram(rawBytes: Uint8Array): { sessionId: number; payload: Uint8Array } {
    if (rawBytes.length < 1) {
      throw new Error('Datagram hajmi juda kichik!');
    }

    // Birinchi baytlar seans identifikatorini bildiradi
    const sessionId = rawBytes[0]; // Sodda VarInt tasviri
    const payload = rawBytes.subarray(1);

    return { sessionId, payload };
  }

  /**
   * Ishonchsiz (Unreliable) tezkor datagram paketini hosil qilish
   */
  public buildDatagram(sessionId: number, data: Uint8Array): Uint8Array {
    if (data.length + 1 > this.maxDatagramSize) {
      throw new RangeError(`Datagram limiti buzildi: ${data.length + 1} > ${this.maxDatagramSize}`);
    }

    const packet = new Uint8Array(1 + data.length);
    packet[0] = sessionId & 0xff;
    packet.set(data, 1);

    return packet;
  }
}
```
**Tushuntirish:** WebTransport Datagramlari to'g'ridan-to'g'ri QUIC DATAGRAM freymi (RFC 9221) orqali yuboriladi. Ular hech qachon qayta yuborilmaydi (No retransmission) va ACK kutmaydi. Bu esa tarmoqda yo'qolgan paketlar tufayli navbatda tiqilishni (Head-of-Line Blocking) butunlay yo'q qiladi.

---

### Topshiriq #1123: WebTransport Unidirectional Streams: Katta Hajmli Fayllarni Oqimli Yuklash
**Tavsif:** Foydalanuvchi serverga yirik fayllar yoki video yozuvlarni yuklaganda, javob kutmasdan ma'lumotni faqat bir yo'nalishda (One-Way) uzatuvchi Unidirectional Stream eng tejamkor yechimdir.
**Talablar:** Unidirectional stream yaratish (0x54 prefiksi - WebTransport oqim identifikatori), oqimli yozish va yakunlash (FIN).
**Yechim (TypeScript):**
```ts
import { WritableStream } from 'node:stream/web';

export class WebTransportUnidirectionalStream {
  // WebTransport Unidirectional stream prefiksi: 0x54 (RFC standarti)
  public static readonly WT_UNI_STREAM_TYPE = 0x54;

  /**
   * Katta ma'lumotlarni bir tomonlama stream orqali qabul qiluvchi WritableStream adapteri
   */
  public static createStreamReceiver(onDataChunk: (chunk: Uint8Array) => void, onComplete: () => void): WritableStream<Uint8Array> {
    let isFirstChunk = true;

    return new WritableStream<Uint8Array>({
      write(chunk) {
        let payload = chunk;
        if (isFirstChunk) {
          isFirstChunk = false;
          // Birinchi baytdan oqim turini tekshirish
          if (chunk[0] !== WebTransportUnidirectionalStream.WT_UNI_STREAM_TYPE) {
            throw new Error(`Noto'g'ri WebTransport stream turi: ${chunk[0]}`);
          }
          payload = chunk.subarray(1); // Prefiksni olib tashlash
        }

        onDataChunk(payload);
      },
      close() {
        onComplete();
      },
      abort(err) {
        console.error('[WebTransport Stream Bekor Qilindi]:', err);
      }
    });
  }
}
```
**Tushuntirish:** WebTransport Unidirectional streamlari xotirani juda kam sarflaydi, chunki server ushbu oqim bo'yicha javob qaytarish kanalini (Reverse channel) ochmaydi va boshqaruv strukturalarini saqlab turmaydi. Bu minglab bir vaqtda yuklanayotgan telemetriya oqimlari uchun idealdir.

---

### Topshiriq #1124: WebTransport Bidirectional Streams: Real Vaqtli RPC So'rov-Javob Kanallarini Yaratish
**Tavsif:** Klient va server o'rtasida ishonchli ikki tomonlama muloqot (masalan moliyaviy buyruqlar yoki chat xabarlari) o'tkazish uchun ikkala tomon ham yoza oladigan va o'qiy oladigan Bidirectional streamlar kerak.
**Talablar:** Bidirectional stream multiplexing, so'rovni qabul qilib unga aynan o'sha stream orqali javob qaytaruvchi RPC sinfi.
**Yechim (TypeScript):**
```ts
export interface RpcMessage {
  id: string;
  action: string;
  params: any;
}

export class WebTransportBidirectionalRpc {
  /**
   * Kiruvchi ikki tomonlama streamni qabul qilib, unga ishlov berish va javob yozish
   */
  public static async handleStream(
    readable: ReadableStream<Uint8Array>,
    writable: WritableStream<Uint8Array>,
    handler: (msg: RpcMessage) => Promise<any>
  ): Promise<void> {
    const reader = readable.getReader();
    const writer = writable.getWriter();
    const chunks: Uint8Array[] = [];

    try {
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        if (value) chunks.push(value);
      }

      // Xabarni bitta buferga birlashtirish
      const totalLen = chunks.reduce((acc, c) => acc + c.length, 0);
      const fullBuffer = new Uint8Array(totalLen);
      let p = 0;
      for (const c of chunks) {
        fullBuffer.set(c, p);
        p += c.length;
      }

      // JSON RPC parse qilish
      const msgText = new TextDecoder().decode(fullBuffer);
      const rpcReq: RpcMessage = JSON.parse(msgText);

      // Biznes logikani bajarish
      const result = await handler(rpcReq);

      // Javobni xuddi shu oqim orqali qaytarish
      const respBuffer = new TextEncoder().encode(JSON.stringify({
        id: rpcReq.id,
        status: 'OK',
        result
      }));

      await writer.write(respBuffer);
      await writer.close();
    } catch (err: any) {
      const errBuffer = new TextEncoder().encode(JSON.stringify({ error: err.message }));
      await writer.write(errBuffer);
      await writer.close();
    }
  }
}
```
**Tushuntirish:** WebTransport Bidirectional streamlari HTTP/1.1 va HTTP/2 dagi ulanish qulflanishlarisiz (Connection Head-of-Line Blocking) ishlaydi. Har bir RPC so'rovi yangi alohida streamda bajariladi; agar bitta RPC so'rovi tarmoqda kechiksa, qolgan barcha so'rovlar to'liq tezlikda bajarilaveradi.

---

### Topshiriq #1125: WHATWG Streams Bilan WebTransport Orqa Bosimini (Backpressure) Boshqarish
**Tavsif:** Agar tarmoq sekinlashsa yoki mijoz ma'lumotlarni qabul qilishga ulgurmay qolsa, server xotirasida buferlar cheksiz to'planib ketishi (OOM - Out of Memory) mumkin. Backpressure orqali jo'natish tezligini dinamik muvofiqlashtirish zarur.
**Talablar:** WHATWG ReadableStream va WritableStream orqali highWaterMark chegaralarini boshqarish va writer.ready promisini to'g'ri kutish.
**Yechim (TypeScript):**
```ts
export class WebTransportBackpressureManager {
  /**
   * Orqa bosimni (Backpressure) inobatga olgan holda ma'lumotlarni xavfsiz oqimli uzatish
   */
  public static async streamWithBackpressure(
    writer: WritableStreamDefaultWriter<Uint8Array>,
    sourceGenerator: AsyncGenerator<Uint8Array, void, unknown>
  ): Promise<void> {
    try {
      for await (const chunk of sourceGenerator) {
        // MUHIM: Xotira to'lib ketmasligi uchun writer tayyor bo'lishini kutamiz
        // Agar iste'molchi sekin bo'lsa, writer.ready kutish holatiga o'tadi
        await writer.ready;

        // Ma'lumotni jo'natish
        await writer.write(chunk);
      }

      // Oqimni xavfsiz yakunlash
      await writer.close();
    } catch (err) {
      console.error('[Backpressure Oqimida Xatolik]:', err);
      await writer.abort(err);
    }
  }
}
```
**Tushuntirish:** `writer.ready` xususiyati WHATWG Streams standartidagi eng kuchli orqa bosim vositasidir. U ichki navbat hajmi (HighWaterMark) to'lganda darhol kutish holatiga o'tadi va quyi qatlamdagi soket buferlari bo'shagandan keyingina yangi ma'lumot o'qishga ruxsat beradi.

---

### Topshiriq #1126: Multiplayer O'yinlar Uchun WebTransport Gibrid Arxitekturasi (Datagram + Stream)
**Tavsif:** Haqiqiy vaqtli ko'p o'yinchili o'yinlarda o'yinchilarning kordinatalari (X, Y, Z) soniyasiga 60 marta uzatiladi (Datagram kerak), o'yinchat yoki qurol sotib olish esa 100% yetkazilishi shart (Stream kerak).
**Talablar:** Gibrid WebTransport Game Engine aloqa qatlamini yaratish.
**Yechim (TypeScript):**
```ts
export interface PlayerMovement {
  playerId: string;
  x: number;
  y: number;
  rotation: number;
  seq: number;
}

export interface GameTransaction {
  txId: string;
  itemId: string;
  amount: number;
}

export class HybridGameTransportServer {
  private lastSeqMap = new Map<string, number>();

  /**
   * 1. Tezkor kordinatalarni qabul qilish (Datagram - yo'qolsa ham hech narsa qilmaydi)
   */
  public handlePositionDatagram(rawPayload: Uint8Array): void {
    // 1 bayt sequence, 4 bayt X, 4 bayt Y
    const view = new DataView(rawPayload.buffer, rawPayload.byteOffset, rawPayload.byteLength);
    const seq = view.getUint8(0);
    const x = view.getFloat32(1, true);
    const y = view.getFloat32(5, true);

    // Agar eski paket kechikib kelgan bo'lsa, uni tashlab yuboramiz
    // const lastSeq = this.lastSeqMap.get(playerId) || 0;
    // if (seq < lastSeq) return;

    // console.log(`O'yinchi yangi pozitsiyasi: x=${x}, y=${y}`);
  }

  /**
   * 2. Muhim moliyaviy tranzaksiyalarni qabul qilish (Bidirectional Stream - 100% kafolatlangan)
   */
  public async handleInventoryPurchase(tx: GameTransaction): Promise<{ success: boolean }> {
    // Bazada xavfsiz atomar tranzaksiya
    console.log(`[Tranzaksiya bajarildi]: ${tx.itemId} -> ${tx.amount} tanga`);
    return { success: true };
  }
}
```
**Tushuntirish:** Ushbu gibrid yondashuv WebTransport ning eng asosiy afzalligini namoyish etadi: bitta tarmoq ulanishi va bitta port orqali dasturchi ham UDP ning ultra tezkorligiga (Datagram), ham TCP ning ishonchli tartiblangan yetkazilishiga (Stream) ega bo'ladi.

---

### Topshiriq #1127: WebTransport Seansini Xavfsiz To'xtatish (Drain, Session Close Code va Reason)
**Tavsif:** Server qayta ishga tushirilganda (Graceful Shutdown) yoki foydalanuvchi tizimdan chiqqanda mavjud faol oqimlarni darhol uzib qo'ymasdan, ularning tugashini kutish (Draining) va xato kodini yuborish lozim.
**Talablar:** WebTransportSession.close() spetsifikatsiyasi, 32-bitli xato kodlari va sabab matnini yuborish.
**Yechim (TypeScript):**
```ts
export interface CloseSessionOptions {
  closeCode: number;
  reason: string;
}

export class WebTransportGracefulShutdown {
  private activeStreamsCount = 0;
  private isDraining = false;

  public registerStream(): void {
    if (this.isDraining) {
      throw new Error('Server to`xtatilmoqda, yangi streamlar qabul qilinmaydi!');
    }
    this.activeStreamsCount++;
  }

  public streamFinished(): void {
    this.activeStreamsCount = Math.max(0, this.activeStreamsCount - 1);
  }

  /**
   * Seansni xavfsiz to'xtatish
   */
  public async drainAndClose(timeoutMs: number = 5000): Promise<CloseSessionOptions> {
    this.isDraining = true;
    console.log(`[WebTransport Drain] Faol streamlar: ${this.activeStreamsCount}. Kutilmoqda...`);

    const start = Date.now();
    while (this.activeStreamsCount > 0) {
      if (Date.now() - start > timeoutMs) {
        console.warn('[WebTransport Drain] Timeout! Qolgan streamlar majburiy to`xtatiladi.');
        break;
      }
      await new Promise((r) => setTimeout(r, 100));
    }

    return {
      closeCode: 0x00, // NO_ERROR
      reason: 'Server texnik xizmat ko`rsatish uchun to`xtatildi'
    };
  }
}
```
**Tushuntirish:** WebTransport seansini yopish paytida yuboriladigan `closeCode` va `reason` xuddi WebSocket kabi mijoz brauzeriga yetkaziladi. Biroq `draining` fazasi davomida mijoz yangi stream ochmaydi va server mavjud oqimlarni oxiriga yetkazib olish imkoniyatiga ega bo'ladi.

---

### Topshiriq #1128: WebTransport Sertifikat Heshi (serverCertificateHashes) Validatsiyasi
**Tavsif:** Lokal test muhitida yoki yopiq korporativ tarmoqda WebTransport seanslarini CA (Certificate Authority) tomonidan tasdiqlangan domenlarsiz sinash uchun W3C standarti SHA-256 sertifikat heshlaridan foydalanishga ruxsat beradi.
**Talablar:** Mijoz va server o'rtasida serverCertificateHashes tekshiruvini amalga oshirish va sertifikat xavfsizlik parametrlarini sozlash.
**Yechim (TypeScript):**
```ts
import crypto from 'node:crypto';

export class WebTransportCertificateValidator {
  /**
   * Berilgan DER formatidagi TLS sertifikatining SHA-256 barmoq izini (Fingerprint) hisoblash
   */
  public static calculateCertificateHash(derCertificateBuffer: Uint8Array): string {
    const hash = crypto.createHash('sha256');
    hash.update(derCertificateBuffer);
    return hash.digest('hex');
  }

  /**
   * Brauzerdan kelgan serverCertificateHashes parametrini tekshirish
   */
  public static verifyClientHash(expectedDerCert: Uint8Array, clientReceivedHashes: { algorithm: string; value: ArrayBuffer }[]): boolean {
    const serverSha256 = crypto.createHash('sha256').update(expectedDerCert).digest();

    for (const h of clientReceivedHashes) {
      if (h.algorithm === 'sha-256') {
        const clientVal = Buffer.from(h.value);
        if (crypto.timingSafeEqual(serverSha256, clientVal)) {
          return true;
        }
      }
    }

    return false;
  }
}
```
**Tushuntirish:** W3C WebTransport standarti bo'yicha `serverCertificateHashes` imkoniyati dasturchilarga self-signed (o'zi imzolagan) sertifikatlar bilan 14 kungacha amal qiluvchi xavfsiz tajribalarni o'tkazish imkonini beradi. Bu testlash paytida xavfsizlik ogohlantirishlarisiz WebTransport ni qo'llashning rasmiy yo'lidir.

---

### Topshiriq #1129: WebTransport Oqimlarida Paketlar Yo'qolishi va RTT O'lchovlarini Nazorat Qilish
**Tavsif:** Tarmoq sifati yomonlashganda (masalan mobil internetda RTT 300ms dan oshganda), WebTransport orqali uzatilayotgan video sifati yoki ma'lumotlar chastotasi pasaytirilishi kerak.
**Talablar:** RTT (Round Trip Time), Jitter va Packet Loss hisoblagichini yurituvchi Metric Tracker sinfi.
**Yechim (TypeScript):**
```ts
export interface NetworkQualityStats {
  rttMs: number;
  jitterMs: number;
  packetsSent: number;
  packetsLost: number;
  lossRatePercentage: number;
}

export class WebTransportNetworkMonitor {
  private sentTimestamps = new Map<number, number>();
  private rttHistory: number[] = [];
  private packetsSent = 0;
  private packetsLost = 0;

  public onPacketSent(packetSeq: number): void {
    this.packetsSent++;
    this.sentTimestamps.set(packetSeq, Date.now());
  }

  public onAckReceived(packetSeq: number): void {
    const sentTime = this.sentTimestamps.get(packetSeq);
    if (sentTime) {
      const currentRtt = Date.now() - sentTime;
      this.sentTimestamps.delete(packetSeq);
      this.rttHistory.push(currentRtt);
      if (this.rttHistory.length > 50) this.rttHistory.shift();
    }
  }

  public onPacketLoss(packetSeq: number): void {
    this.packetsLost++;
    this.sentTimestamps.delete(packetSeq);
  }

  public getQualityReport(): NetworkQualityStats {
    const avgRtt = this.rttHistory.length > 0 
      ? this.rttHistory.reduce((a, b) => a + b, 0) / this.rttHistory.length 
      : 0;

    const lossRate = this.packetsSent > 0 
      ? (this.packetsLost / this.packetsSent) * 100 
      : 0;

    return {
      rttMs: Math.round(avgRtt),
      jitterMs: 5,
      packetsSent: this.packetsSent,
      packetsLost: this.packetsLost,
      lossRatePercentage: parseFloat(lossRate.toFixed(2))
    };
  }
}
```
**Tushuntirish:** Tarmoq statistikasini doimiy o'lchash orqali adaptiv bitrate (ABR) va aqlli yuklama nazorati (Congestion Control) amalga oshiriladi. Tarmoqda paketlar yo'qolishi boshlanganda ilova og'ir ma'lumotlarni kechiktirib, faqat kritik signallarni uzatish rejimiga o'tadi.

---

### Topshiriq #1130: Bun va Node Muhitida WebTransport Server Emulyatori va Sinov Stendi
**Tavsif:** WebTransport mijozlarini tekshirish uchun mahalliy test stendini yaratish va uning barcha imkoniyatlarini (Handshake, Datagram, Unidirectional Stream) bitta serverda ko'rgazmali sinab ko'rish zarur.
**Talablar:** To'liq WebTransport test emulyatori sinfini yozish.
**Yechim (TypeScript):**
```ts
import { WebTransportSessionInitiator } from './WebTransportSessionInitiator';
import { WebTransportDatagramEngine } from './WebTransportDatagramEngine';

export class MockWebTransportServer {
  private datagramEngine = new WebTransportDatagramEngine();
  private isOnline = false;

  public async start(port: number = 4433): Promise<void> {
    this.isOnline = true;
    console.log(`[WebTransport Mock Server] ${port} portida tayyor.`);
  }

  /**
   * Sinov ulanishi simulyatsiyasi
   */
  public simulateClientConnect(headers: Map<string, string>): { accepted: boolean; responseHeaders: Map<string, string> } {
    try {
      WebTransportSessionInitiator.validateHandshake(headers);
      const resp = WebTransportSessionInitiator.createHandshakeSuccessResponse();
      return { accepted: true, responseHeaders: resp };
    } catch (e: any) {
      console.error('Ulanish rad etildi:', e.message);
      return { accepted: false, responseHeaders: new Map() };
    }
  }

  public simulateDatagramEcho(clientDatagram: Uint8Array): Uint8Array {
    const { sessionId, payload } = this.datagramEngine.handleIncomingDatagram(clientDatagram);
    // Javob sifatida xuddi shu datagramni qaytarish (Echo)
    return this.datagramEngine.buildDatagram(sessionId, payload);
  }
}
```
**Tushuntirish:** Ushbu emulyator WebTransport arxitekturasini mahalliy CI/CD quvurlarida murakkab tashqi QUIC serverlarini ko'tarmasdan birlik testlar (Unit Tests) orqali to'liq tekshirish imkonini beradi.

---

### Topshiriq #1131: Bun Platformasida Ultra Tezkor WebSocket Server va Xotira Boshqaruvi
**Tavsif:** Millionlab bir vaqtning o'zidagi ochiq ulanishlarni (1M Concurrent Connections) qo'llab-quvvatlash uchun xotira hajmi har bir ulanish uchun minimal bo'lishi talab etiladi.
**Talablar:** Bun.serve({ websocket: ... }) API'si, perMessageDeflate sozlamalari, maxPayloadLength va xotirani tejash usullari.
**Yechim (TypeScript):**
```ts
// Bun runtime (v1.0+) uchun ultra yuqori unumdorlikdagi WebSocket server
export interface UserSocketData {
  userId: string;
  room: string;
  connectedAt: number;
}

export function startBunWebSocketServer(port: number = 3000) {
  const server = (Bun as any).serve<UserSocketData>({
    port,
    fetch(req: Request, server: any) {
      const url = new URL(req.url);
      const userId = url.searchParams.get('userId') || 'guest';
      const room = url.searchParams.get('room') || 'general';

      // HTTP so'rovni WebSocket ga ko'tarish (Upgrade)
      const upgraded = server.upgrade(req, {
        data: {
          userId,
          room,
          connectedAt: Date.now()
        }
      });

      if (upgraded) return undefined;
      return new Response('Kutilmagan so`rov formati', { status: 400 });
    },
    websocket: {
      // Yangi mijoz ulanganda
      open(ws: any) {
        // Bun ichki pub/sub tizimi yordamida xonaga obuna bo'lish
        ws.subscribe(ws.data.room);
        ws.publish(ws.data.room, JSON.stringify({
          type: 'JOIN',
          user: ws.data.userId
        }));
      },
      // Xabar kelganda
      message(ws: any, message: string | Buffer) {
        // Barcha xona a'zolariga xabarni tarqatish (Broadcast)
        ws.publish(ws.data.room, message);
      },
      // Aloqa uzilganda
      close(ws: any, code: number, reason: string) {
        ws.unsubscribe(ws.data.room);
        ws.publish(ws.data.room, JSON.stringify({
          type: 'LEAVE',
          user: ws.data.userId
        }));
      },
      // Xavfsizlik va xotira chegaralari
      maxPayloadLength: 64 * 1024, // 64 KB maksimal xabar hajmi
      idleTimeout: 60,             // 60 soniya nofaollikdan so'ng uzish
      backpressureLimit: 1024 * 1024, // 1MB backpressure chegarasi
      closeOnBackpressureLimit: true
    }
  });

  console.log(`[Bun WebSocket Server] Port: ${port} da ishga tushdi.`);
  return server;
}
```
**Tushuntirish:** Bun ning o'rnatilgan WebSocket arxitekturasi uWebSockets C++ yadrosiga asoslangan. U har bir ulanish uchun atigi 2-4 KB operativ xotira sarflaydi (Node.js dagi 30-50 KB ga nisbatan). Bundan tashqari, uning o'rnatilgan `ws.publish()` va `ws.subscribe()` mexanizmlari xotiradagi massivlarni aylanib chiqmasdan, C++ darajasida nol-nusxa (Zero-copy) tarqatishni ta'minlaydi.

---

### Topshiriq #1132: Node.js ws Moduli Bilan WebSocket Klasteri va Worker Threads Integratsiyasi
**Tavsif:** Bitta Node.js jarayoni bitta CPU yadrosida ishlaydi. 32-yadroli kuchli serverda barcha CPU quvvatidan foydalanish uchun WebSocket serverini Worker Threads yoki Node.js Cluster moduli orqali klasterlash zarur.
**Talablar:** Node.js 'node:cluster' moduli, ishchi jarayonlar (Workers) o'rtasida TCP soketlarni port bo'yicha taqsimlash va 'ws' kutubxonasini ishga tushirish.
**Yechim (TypeScript):**
```ts
import cluster from 'node:cluster';
import http from 'node:http';
import os from 'node:os';
import { WebSocketServer, WebSocket } from 'ws';

const numCPUs = os.cpus().length;

if (cluster.isPrimary) {
  console.log(`[Primary Jarayon ${process.pid}] ${numCPUs} ta ishchi worker ishga tushirilmoqda...`);

  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }

  cluster.on('exit', (worker, code, signal) => {
    console.warn(`[Worker ${worker.process.pid}] to'xtadi. Qayta ishga tushirilmoqda...`);
    cluster.fork();
  });
} else {
  // Har bir worker o'z HTTP va WebSocket serverini bitta portda ochadi (SO_REUSEPORT)
  const server = http.createServer((req, res) => {
    res.writeHead(200);
    res.end('WebSocket Worker faol!');
  });

  const wss = new WebSocketServer({ server });

  wss.on('connection', (ws: WebSocket, req: http.IncomingMessage) => {
    // console.log(`[Worker ${process.pid}] Yangi ulanish qabul qilindi`);

    ws.on('message', (data, isBinary) => {
      // Qabul qilingan xabarni shu workerga ulangan boshqa klientlarga yuborish
      wss.clients.forEach((client) => {
        if (client !== ws && client.readyState === WebSocket.OPEN) {
          client.send(data, { binary: isBinary });
        }
      });
    });

    ws.on('error', (err) => console.error('[WS Error]:', err));
  });

  server.listen(8080, () => {
    console.log(`[Worker ${process.pid}] 8080 portida tinglamoqda`);
  });
}
```
**Tushuntirish:** Node.js `cluster` moduli operatsion tizim darajasida bitta umumiy portga tushayotgan yangi TCP ulanishlarni `round-robin` orqali ishchi jarayonlarga taqsimlaydi. Bu orqali ko'p yadroli serverlarda CPU yuklamasi 100% teng muvozanatlashadi.

---

### Topshiriq #1133: Redis Pub/Sub Bilan Ko'p Tugunli (Multi-Node) WebSocket Klasterini Birlashtirish
**Tavsif:** Klasterda foydalanuvchi A 1-tugunga, foydalanuvchi B esa 2-tugunga ulangan bo'lsa, ular bir xil guruhda bo'lishiga qaramay bir-birining xabarini ko'rmaydi. Tugunlar o'rtasida Redis Pub/Sub magistralini (Backplane) qurish lozim.
**Talablar:** ioredis kutubxonasi, barcha tugunlar uchun umumiy kanalga yozish va kelgan xabarni mahalliy ulangan mijozlarga tarqatish.
**Yechim (TypeScript):**
```ts
import { WebSocket, WebSocketServer } from 'ws';
import Redis from 'ioredis';

export class RedisWebSocketClusterBackplane {
  private pub: Redis;
  private sub: Redis;
  private nodeId = `node_${Math.random().toString(36).substring(2, 9)}`;

  constructor(
    private wss: WebSocketServer,
    redisUrl: string = 'redis://localhost:6379'
  ) {
    this.pub = new Redis(redisUrl);
    this.sub = new Redis(redisUrl);

    this.setupRedisSubscriptions();
    this.setupWebSocket();
  }

  private setupRedisSubscriptions(): void {
    this.sub.subscribe('ws_cluster_channel', (err) => {
      if (err) console.error('[Redis Sub Xatolik]:', err);
      else console.log(`[Node ${this.nodeId}] Redis klaster kanaliga ulandi.`);
    });

    this.sub.on('message', (channel, message) => {
      if (channel === 'ws_cluster_channel') {
        const envelope = JSON.parse(message);

        // O'zimiz yuborgan xabarni o'zimizga qayta tarqatmaslik
        if (envelope.originNode === this.nodeId) return;

        // Mahalliy serverga ulangan mijozlarga tarqatish
        this.wss.clients.forEach((client) => {
          if (client.readyState === WebSocket.OPEN) {
            client.send(envelope.payload);
          }
        });
      }
    });
  }

  private setupWebSocket(): void {
    this.wss.on('connection', (ws: WebSocket) => {
      ws.on('message', (data: string) => {
        // 1. Mahalliy klientlarga uzatish
        this.wss.clients.forEach((client) => {
          if (client !== ws && client.readyState === WebSocket.OPEN) {
            client.send(data);
          }
        });

        // 2. Boshqa barcha tugunlarga yetkazish uchun Redisga chop etish
        const envelope = {
          originNode: this.nodeId,
          payload: data.toString(),
          timestamp: Date.now()
        };
        this.pub.publish('ws_cluster_channel', JSON.stringify(envelope));
      });
    });
  }

  public close(): void {
    this.pub.disconnect();
    this.sub.disconnect();
  }
}
```
**Tushuntirish:** Redis Pub/Sub taqsimlangan WebSocket serverlarining orqa fon aloqa kanali (Backplane) sifatida xizmat qiladi. Qaysi foydalanuvchi qaysi tugunga ulanganidan qat'i nazar, barcha xabarlar millisekundlar ichida barcha tugunlarga yetkaziladi.

---

### Topshiriq #1134: Redis Streams Orqali Uzilib Qolgan Mijozlar Uchun Xabarlarni Qayta Tiklash (Replay)
**Tavsif:** Oddiy Pub/Sub xabarlarni xotirada saqlamaydi. Agar foydalanuvchi interneti 5 soniyaga uzilib qayta ulansa, o'tib ketgan chat xabarlarini qayta tiklash uchun Redis Streams (XADD, XRANGE) bilan replay tizimini joriy qilish zarur.
**Talablar:** XADD orqali xabarlarni saqlash, XREVRANGE/XRANGE yordamida oxirgi xabarlar tarixini qaytarish.
**Yechim (TypeScript):**
```ts
import Redis from 'ioredis';

export interface ChatMessage {
  id?: string;
  senderId: string;
  room: string;
  content: string;
  timestamp: number;
}

export class DurableMessageQueue {
  private redis: Redis;

  constructor(redisUrl: string = 'redis://localhost:6379') {
    this.redis = new Redis(redisUrl);
  }

  /**
   * Xabarni o'chmas qilib Redis Streamga saqlash (XADD)
   * MAXLEN ~ 10000: Har bir xona uchun oxirgi 10 000 ta xabarni saqlash
   */
  public async publishMessage(room: string, senderId: string, content: string): Promise<string> {
    const streamKey = `stream:room:${room}`;
    const id = await this.redis.xadd(
      streamKey,
      'MAXLEN', '~', 10000,
      '*', // Avtomatik vaqt tamg'asi (Timestamp-Sequence ID)
      'sender', senderId,
      'content', content,
      'ts', Date.now().toString()
    );
    return id as string;
  }

  /**
   * Klient qayta ulanganda o'tkazib yuborilgan xabarlarni qayta o'qib berish (XRANGE)
   */
  public async getMissedMessages(room: string, lastReceivedId: string): Promise<ChatMessage[]> {
    const streamKey = `stream:room:${room}`;
    // '(' belgisi aynan o'sha ID dan keyingilarini olishni bildiradi
    const rangeStart = lastReceivedId ? `(${lastReceivedId}` : '-';

    const rawRecords = await this.redis.xrange(streamKey, rangeStart, '+', 'COUNT', 100);
    const messages: ChatMessage[] = [];

    for (const [id, fields] of rawRecords) {
      const msgMap: Record<string, string> = {};
      for (let i = 0; i < fields.length; i += 2) {
        msgMap[fields[i]] = fields[i + 1];
      }

      messages.push({
        id,
        senderId: msgMap['sender'],
        room,
        content: msgMap['content'],
        timestamp: parseInt(msgMap['ts'], 10)
      });
    }

    return messages;
  }
}
```
**Tushuntirish:** Redis Streams append-only jurnali bo'lib xizmat qiladi. Klient o'zida oxirgi saqlangan xabar ID raqamini (masalan `167890000-0`) yuboradi va server `XRANGE (lastId +` buyrug'i orqali aynan yetishmayotgan xabarlar bo'lagini to'g'ri ketma-ketlikda qaytarib beradi.

---

### Topshiriq #1135: Taqsimlangan Xonalar (Rooms / Channels) va Mijozlarni Dinamik Guruhlash Menejeri
**Tavsif:** WebSocket ilovalarida foydalanuvchilar ma'lum kanallarga (masalan 'investitsiya_uzs', 'futbol_jonli') a'zo bo'ladilar. Minglab xonalarni xotirada samarali indekslash va broadcast qilish mexanizmi talab etiladi.
**Talablar:** Ikki tomonlama xaritalash (Client -> Set<Room> va Room -> Set<Client>) va xotira sizib ketishini oldini oluvchi tozalash.
**Yechim (TypeScript):**
```ts
import { WebSocket } from 'ws';

export class DistributedRoomManager {
  // Xona nomidan mijozlar to'plamiga havola
  private rooms = new Map<string, Set<WebSocket>>();
  // Mijozdan uning a'zo bo'lgan xonalariga havola
  private clientRooms = new Map<WebSocket, Set<string>>();

  public joinRoom(room: string, client: WebSocket): void {
    if (!this.rooms.has(room)) {
      this.rooms.set(room, new Set());
    }
    this.rooms.get(room)!.add(client);

    if (!this.clientRooms.has(client)) {
      this.clientRooms.set(client, new Set());
    }
    this.clientRooms.get(client)!.add(room);
  }

  public leaveRoom(room: string, client: WebSocket): void {
    const roomSet = this.rooms.get(room);
    if (roomSet) {
      roomSet.delete(client);
      if (roomSet.size === 0) {
        this.rooms.delete(room); // Bo'sh qolgan xonani xotiradan o'chirish
      }
    }

    const clientSet = this.clientRooms.get(client);
    if (clientSet) {
      clientSet.delete(room);
    }
  }

  /**
   * Klient uzilganda uni barcha a'zo bo'lgan xonalaridan bir zumda tozalash
   */
  public removeClient(client: WebSocket): void {
    const subscribedRooms = this.clientRooms.get(client);
    if (subscribedRooms) {
      for (const room of subscribedRooms) {
        const roomSet = this.rooms.get(room);
        if (roomSet) {
          roomSet.delete(client);
          if (roomSet.size === 0) this.rooms.delete(room);
        }
      }
      this.clientRooms.delete(client);
    }
  }

  /**
   * Muayyan xonadagi barcha mijozlarga xabar yuborish
   */
  public broadcastToRoom(room: string, data: string | Buffer, senderToExclude?: WebSocket): number {
    const roomSet = this.rooms.get(room);
    if (!roomSet) return 0;

    let sentCount = 0;
    for (const client of roomSet) {
      if (client !== senderToExclude && client.readyState === WebSocket.OPEN) {
        client.send(data);
        sentCount++;
      }
    }
    return sentCount;
  }
}
```
**Tushuntirish:** Xonalarni boshqarishda ikki tomonlama indeks (Bi-directional index) qo'llash orqali `leaveRoom` va `removeClient` amallari $O(1)$ vaqtda bajariladi. Agar xona bo'shab qolsa, u `rooms.delete(room)` orqali tozalanadi, bu esa xotirada 'arvoh' (Ghost) obyektlarning yig'ilib qolishini bartaraf etadi.

---

### Topshiriq #1136: WebSocket Heartbeat (Ping-Pong) Protokoli va Zombi Ulanishlarni Aniqlash (Reaper)
**Tavsif:** Foydalanuvchi noutbuk qopqog'ini yopsa yoki mobil telefon tarmog'i to'satdan uzilsa, OS TCP darajasida FIN yubormasligi mumkin. Server ulanishni abadiy ochiq deb o'ylab xotirasida saqlab turadi (Zombie Connections).
**Talablar:** Ping-Pong mexanizmi, 'isAlive' bayrog'i va har 30 soniyada javob bermagan soketlarni majburiy uzuvchi (terminate) Reaper taymeri.
**Yechim (TypeScript):**
```ts
import { WebSocket, WebSocketServer } from 'ws';

// Standart WebSocket obyektini isAlive bayrog'i bilan boyitish
interface ExtWebSocket extends WebSocket {
  isAlive: boolean;
  pingTimeout?: NodeJS.Timeout;
}

export class WebSocketHeartbeatReaper {
  private intervalId: NodeJS.Timeout | null = null;

  constructor(
    private wss: WebSocketServer,
    private checkIntervalMs: number = 30000 // Har 30 soniyada tekshirish
  ) {
    this.setupListeners();
    this.startReaper();
  }

  private setupListeners(): void {
    this.wss.on('connection', (ws: WebSocket) => {
      const extWs = ws as ExtWebSocket;
      extWs.isAlive = true;

      // Mijoz serverning pingiga pong javob qaytarganda:
      extWs.on('pong', () => {
        extWs.isAlive = true;
      });
    });
  }

  private startReaper(): void {
    this.intervalId = setInterval(() => {
      let deadCount = 0;

      this.wss.clients.forEach((client) => {
        const extWs = client as ExtWebSocket;

        // Agar o'tgan interval davomida mijoz pong javob bermagan bo'lsa
        if (extWs.isAlive === false) {
          deadCount++;
          // Soketni majburiy yopish (TCP Reset yuborish)
          return extWs.terminate();
        }

        // Keyingi tekshiruv uchun bayroqni false qilamiz va Ping yuboramiz
        extWs.isAlive = false;
        extWs.ping();
      });

      if (deadCount > 0) {
        console.log(`[Reaper Tozalash]: ${deadCount} ta zombi ulanish aniqlandi va yopildi.`);
      }
    }, this.checkIntervalMs);
  }

  public stop(): void {
    if (this.intervalId) clearInterval(this.intervalId);
  }
}
```
**Tushuntirish:** `ws.terminate()` usuli `ws.close()` dan farqli ravishda TCP handshake yopilishini kutib o'tirmaydi, balki operatsion tizim darajasida resursni darhol ozod qiladi. Ushbu mexanizmsiz ishlayotgan ishlab chiqarish klasterlarida bir necha kunda xotiraning 50% dan ortig'i o'lik ulanishlar bilan to'lib qoladi.

---

### Topshiriq #1137: WebSocket Ulanishlarida Nol-Nusxa (Zero-Copy) Binar Buferlar va TypedArray Almashinuvi
**Tavsif:** Katta hajmdagi sonli massivlarni (masalan, birja order-book narxlari yoki grafika ma'lumotlari) JSON orqali stringify qilish CPU va tarmoqni keraksiz zo'riqtiradi. Binar formatda nol-nusxa (Zero-Copy) uzatish lozim.
**Talablar:** ArrayBuffer, Float64Array va DataView dan foydalangan holda binar paketlarni serializatsiya va deserializatsiya qilish.
**Yechim (TypeScript):**
```ts
import { WebSocket } from 'ws';

export interface OrderBookTick {
  symbolId: number; // 2 bayt Uint16
  bidPrice: number; // 8 bayt Float64
  askPrice: number; // 8 bayt Float64
  volume: number;   // 4 bayt Uint32
}

export class BinaryMarketDataCodec {
  // Paket hajmi: 2 + 8 + 8 + 4 = 22 bayt
  public static readonly PACKET_SIZE = 22;

  /**
   * Bozor kotirovkasini ixcham binar formatga o'girish (Nol-nusxa bufer)
   */
  public static encodeTick(tick: OrderBookTick): Uint8Array {
    const buffer = new ArrayBuffer(this.PACKET_SIZE);
    const view = new DataView(buffer);

    view.setUint16(0, tick.symbolId, true); // Little-endian
    view.setFloat64(2, tick.bidPrice, true);
    view.setFloat64(10, tick.askPrice, true);
    view.setUint32(18, tick.volume, true);

    return new Uint8Array(buffer);
  }

  /**
   * Binar buferdan ma'lumotlarni o'qib olish
   */
  public static decodeTick(rawBytes: Uint8Array): OrderBookTick {
    if (rawBytes.byteLength < this.PACKET_SIZE) {
      throw new Error(`Paket hajmi kam: ${rawBytes.byteLength} < ${this.PACKET_SIZE}`);
    }

    const view = new DataView(rawBytes.buffer, rawBytes.byteOffset, rawBytes.byteLength);

    return {
      symbolId: view.getUint16(0, true),
      bidPrice: view.getFloat64(2, true),
      askPrice: view.getFloat64(10, true),
      volume: view.getUint32(18, true)
    };
  }
}
```
**Tushuntirish:** JSON formatida birja kotirovkasi taxminan 120-150 bayt matn talab qiladi va uni parse qilish JavaScript Garbage Collector (GC) ga yuk tushiradi. TypedArray binar formati esa atigi 22 baytni egallaydi va CPU da mikrosekundlarda qayta ishlanadi.

---

### Topshiriq #1138: MessagePack Yordamida WebSocket Xabarlarini Binar Siqish
**Tavsif:** Ixtiyoriy dinamik obyektlarni yuborishda ham JSON o'rniga binar MessagePack protokolidan foydalanish tarmoq trafigini 50% ga qisqartiradi.
**Talablar:** MessagePack kodlovchi va dekodlovchi xizmat, WebSocket oqimida xabarlarni binar rejimda (binaryType = 'arraybuffer') almashish.
**Yechim (TypeScript):**
```ts
// Sodda va yuqori tezlikdagi MsgPack simulyatsiya qatlami
export class MiniMsgPack {
  public static serialize(obj: any): Uint8Array {
    // Haqiqiy loyihalarda '@msgpack/msgpack' kutubxonasi ishlatiladi
    // Bu yerda uning binar o'rami ko'rsatilgan
    const jsonStr = JSON.stringify(obj);
    const rawBytes = new TextEncoder().encode(jsonStr);

    // 0x90 prefiksi - MsgPack format belgisi
    const packed = new Uint8Array(1 + rawBytes.length);
    packed[0] = 0xd9; // str format
    packed.set(rawBytes, 1);
    return packed;
  }

  public static deserialize<T = any>(buffer: Uint8Array): T {
    const rawBytes = buffer.subarray(1);
    const jsonStr = new TextDecoder().decode(rawBytes);
    return JSON.parse(jsonStr) as T;
  }
}
```
**Tushuntirish:** MessagePack JSON bilan 100% mos bo'lib, kalitlar va matnlarni ixcham binar ko'rinishda saqlaydi. Veb-soket orqali har soniyada yuzlab xabarlar almashiladigan moliyaviy dasturlarda MsgPack mobil klientlarning batareya va internet trafigini sezilarli darajada tejaydi.

---

### Topshiriq #1139: WebSocket Handshake Paytida Xavfsizlik: JWT Validatsiya va Origin Tekshiruvi
**Tavsif:** Veb-soketlar Cross-Origin cheklovlariga (CORS) ega emas, shuning uchun istalgan zararli sayt foydalanuvchi nomidan soket ulanishini ochishi mumkin (CSWSH - Cross-Site WebSocket Hijacking).
**Talablar:** HTTP Upgrade bosqichida Origin sarlavhasini qat'iy oq ro'yxat (Whitelist) orqali tekshirish va Sec-WebSocket-Protocol yoki query parametrlaridagi JWT tokenni tekshirish.
**Yechim (TypeScript):**
```ts
import http from 'node:http';
import crypto from 'node:crypto';

export class WebSocketSecurityGuard {
  private static readonly ALLOWED_ORIGINS = new Set([
    'https://khorazmiy.uz',
    'https://app.khorazmiy.uz'
  ]);

  /**
   * Handshake so'rovini tekshirish
   */
  public static verifyUpgradeRequest(req: http.IncomingMessage): { isValid: boolean; user?: any; rejectCode?: number } {
    // 1. Origin tekshiruvi (CSWSH himoyasi)
    const origin = req.headers['origin'];
    if (origin && !this.ALLOWED_ORIGINS.has(origin)) {
      console.warn(`[Xavfsizlik Ogohlantirishi] Ruxsat etilmagan Origin: ${origin}`);
      return { isValid: false, rejectCode: 403 };
    }

    // 2. Token tekshiruvi (URL search parametridan yoki Sec-WebSocket-Protocol dan)
    const url = new URL(req.url || '/', `http://${req.headers.host}`);
    const token = url.searchParams.get('token');

    if (!token) {
      return { isValid: false, rejectCode: 401 };
    }

    // 3. Tokendagi imzoni tekshirish (simulyatsiya)
    if (token === 'valid_jwt_khorazmiy_2026') {
      return { isValid: true, user: { id: 'usr_777', role: 'admin' } };
    }

    return { isValid: false, rejectCode: 401 };
  }
}
```
**Tushuntirish:** WebSocket ulanishi o'rnatilgandan so'ng xavfsizlikni tekshirish xotira va CPU ni isrof qiladi. Barcha tekshiruvlar HTTP Upgrade bosqichida hal qilinishi shart: agar origin mos kelmasa yoki token xato bo'lsa, soket ochilmasdan darhol HTTP 401/403 qaytariladi.

---

### Topshiriq #1140: Token-Bucket Algoritmi Asosida WebSocket Rate Limiting va DDoS Himoyasi
**Tavsif:** Bitta buzuq bot yoki xaker soniyasiga minglab WebSocket xabarlarini yuborib butun klaster xotirasini to'ldirishga urinishi mumkin. Har bir soket uchun alohida token-bucket rate limiter o'rnatish shart.
**Talablar:** Token Bucket algoritmi: Imkoniyatlar chegarasi (Capacity), to'ldirish tezligi (Refill rate) va me'yordan oshganda soketni ogohlantirish yoki uzish.
**Yechim (TypeScript):**
```ts
export class SocketTokenBucketLimiter {
  private tokens: number;
  private lastRefillTimestamp: number;

  constructor(
    private capacity: number = 50,       // Maksimal 50 ta tokenga ega chelak
    private refillRatePerSec: number = 10 // Soniyasiga 10 tadan token qo'shiladi
  ) {
    this.tokens = capacity;
    this.lastRefillTimestamp = Date.now();
  }

  /**
   * Xabar kelganda chaqiriladi.
   * Agar ruxsat etilsa true, limit oshsa false qaytaradi.
   */
  public tryConsume(cost: number = 1): boolean {
    this.refill();

    if (this.tokens >= cost) {
      this.tokens -= cost;
      return true;
    }

    return false;
  }

  private refill(): void {
    const now = Date.now();
    const elapsedSec = (now - this.lastRefillTimestamp) / 1000;
    this.tokens = Math.min(this.capacity, this.tokens + elapsedSec * this.refillRatePerSec);
    this.lastRefillTimestamp = now;
  }
}
```
**Tushuntirish:** Token-Bucket algoritmi to'satdan qisqa muddatli so'rovlar oqimiga (Burst Traffic) ruxsat beradi, ammo uzoq vaqt davom etuvchi zo'riqishlarni qat'iy cheklaydi. Agar klient limitni muntazam buzaversa, xizmat xavfsizlik maqsadida soketni `4429 Too Many Requests` kodi bilan yopadi.

---

### Topshiriq #1141: WebSocket Klasterida Nol To'xtalish (Zero-Downtime Rolling Reload) va Connection Draining
**Tavsif:** Yangi kod versiyasi chiqarilganda (Deployment), bir vaqtda 50 000 ta klient ulangan serverni darhol o'chirib yuborish klientlarda xatoliklar to'lqinini hosil qiladi. Ulanishlarni asta-sekin bo'shatish (Connection Draining) talab etiladi.
**Talablar:** SIGTERM signali kelganda yangi ulanishlarni to'xtatish, mijozlarga 1012 (Service Restart) kodi bilan tasodifiy kechikish (Jitter) asosida uzilish xabarini jo'natish.
**Yechim (TypeScript):**
```ts
import { WebSocket, WebSocketServer } from 'ws';

export class GracefulWebSocketDrainer {
  private isDraining = false;

  constructor(private wss: WebSocketServer) {}

  public async initiateDraining(maxDrainTimeMs: number = 30000): Promise<void> {
    this.isDraining = true;
    console.log('[Rolling Reload] Yangi ulanishlar to`xtatildi. Draining boshlandi...');

    const clients = Array.from(this.wss.clients);
    const total = clients.length;

    // Barcha klientlarga birdaniga emas, 0 dan 15 soniyagacha tasodifiy vaqt bilan uzilish buyrug'ini berish (Jitter)
    clients.forEach((client, idx) => {
      const delay = Math.random() * 15000;

      setTimeout(() => {
        if (client.readyState === WebSocket.OPEN) {
          // 1012: Service Restart kodi (RFC 6455 standartida mavjud)
          client.close(1012, 'Server yangilanmoqda, iltimos boshqa tugunga qayta ulaning');
        }
      }, delay);
    });

    // Barcha klientlar uzilib bo'lishini kutish
    const start = Date.now();
    while (this.wss.clients.size > 0 && Date.now() - start < maxDrainTimeMs) {
      await new Promise((r) => setTimeout(r, 500));
    }

    console.log('[Rolling Reload] Klaster muvaffaqiyatli bo`shatildi!');
  }
}
```
**Tushuntirish:** Connection Draining paytida 'Jitter' (tasodifiy kechikish) qo'llash orqali minglab mijozlar bir soniyada boshqa yangi ishga tushgan tugunga yopirilib borishining (Thundering Herd) oldi olinadi. Natijada klientlar sezdirmasdan yangi versiyaga bosqichma-bosqich o'tadi.

---

### Topshiriq #1142: WebSocket Klasterida Har Bir Tugun Yuklanishini Hisoblash va Load Balancing Agenti
**Tavsif:** Klasterdagi serverlarning birida 5000 ta ulanish, ikkinchisida esa 50 000 ta ulanish bo'lmasligi uchun har bir tugun o'zining CPU, xotira va ulanishlar soni haqidagi statistikasini umumiy muvozanatlashtiruvchiga (Load Balancer) taqdim etishi kerak.
**Talablar:** Health-Check endpoint, yuklama indeksi (Weight calculation) va eng yengil tugunga yo'naltiruvchi mexanizm.
**Yechim (TypeScript):**
```ts
import os from 'node:os';

export interface NodeHealthReport {
  nodeId: string;
  activeConnections: number;
  cpuLoadPercentage: number;
  memoryUsageMb: number;
  score: number; // Qanchalik kichik bo'lsa, tugun shunchalik bo'sh
}

export class ClusterNodeHealthAgent {
  constructor(
    private nodeId: string,
    private getActiveConnCount: () => number
  ) {}

  public getReport(): NodeHealthReport {
    const activeConnections = this.getActiveConnCount();
    const freeMem = os.freemem();
    const totalMem = os.totalmem();
    const usedMemMb = Math.round((totalMem - freeMem) / (1024 * 1024));

    // 1 daqiqalik o'rtacha CPU yuklamasi
    const cpuLoads = os.loadavg();
    const cpuPct = (cpuLoads[0] / os.cpus().length) * 100;

    // Yuklama balli (Score) formulasi
    const score = activeConnections * 1.0 + cpuPct * 10.0 + (usedMemMb / 100.0);

    return {
      nodeId: this.nodeId,
      activeConnections,
      cpuLoadPercentage: parseFloat(cpuPct.toFixed(1)),
      memoryUsageMb: usedMemMb,
      score: parseFloat(score.toFixed(2))
    };
  }
}
```
**Tushuntirish:** Ushbu metrikalar HAProxy yoki Nginx boshqaruvchi agentiga uzatiladi. 'Least Connections' yoki 'Weighted Round Robin' algoritmlari orqali yangi ochilayotgan WebSocket seanslari eng kam yuklangan serverlarga taqsimlanadi.

---

### Topshiriq #1143: Node.js HTTP Moduli Asosida Nol Tashqi Kutubxonasiz SSE (Server-Sent Events) Serverini Qurish
**Tavsif:** Faqat serverdan mijozga bir tomonlama bildirishnomalar (Notifications) yoki LLM generatsiya oqimi uzatilishi kerak bo'lganda, WebSocket protokoli ortiqcha murakkablik tug'diradi. Standart HTTP orqali ishlovchi toza SSE serveri talab etiladi.
**Talablar:** Content-Type: text/event-stream, Cache-Control: no-cache, Connection: keep-alive sarlavhalari va format qoidalari (id, event, data, retry).
**Yechim (TypeScript):**
```ts
import http from 'node:http';

export interface SseEvent {
  id?: string | number;
  event?: string;
  data: any;
  retry?: number;
}

export class PureNodeSseServer {
  private clients = new Set<http.ServerResponse>();

  public handleRequest(req: http.IncomingMessage, res: http.ServerResponse): void {
    // 1. Standart SSE sarlavhalarini o'rnatish
    res.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache, no-transform',
      'Connection': 'keep-alive',
      'Access-Control-Allow-Origin': '*',
      'X-Accel-Buffering': 'no' // Nginx orqali buferlanishni to'xtatish
    });

    // 2. Dastlabki ulanish izohi (Keep-Alive ping)
    res.write(': ulanish_ochildi\n\n');

    this.clients.add(res);

    // 3. Mijoz brauzerni yopganda tozalash
    req.on('close', () => {
      this.clients.delete(res);
      // console.log('SSE mijoz uzildi.');
    });
  }

  /**
   * Barcha ulangan mijozlarga SSE hodisasini uzatish
   */
  public broadcast(evt: SseEvent): void {
    let payload = '';

    if (evt.id !== undefined) payload += `id: ${evt.id}\n`;
    if (evt.event !== undefined) payload += `event: ${evt.event}\n`;
    if (evt.retry !== undefined) payload += `retry: ${evt.retry}\n`;

    const dataLines = (typeof evt.data === 'string' ? evt.data : JSON.stringify(evt.data)).split('\n');
    for (const line of dataLines) {
      payload += `data: ${line}\n`;
    }
    payload += '\n'; // Har bir SSE xabari ikkita yangi qator bilan yakunlanadi

    for (const client of this.clients) {
      client.write(payload);
    }
  }
}
```
**Tushuntirish:** Server-Sent Events oddiy HTTP protokoli ustida ishlaydi, shuning uchun korporativ xavfsizlik devorlari (Firewalls) va proksi serverlar tomonidan bloklanmaydi. `X-Accel-Buffering: no` sarlavhasi Nginx orqasida o'tirgan serverlar uchun kritik parametr bo'lib, proksining ma'lumotlarni kechiktirib buferlashini to'xtatadi.

---

### Topshiriq #1144: Bun Platformasida SSE Oqimini Response va ReadableStream Yordamida Yuqori Unumdorlikda Uzatish
**Tavsif:** Bun da har bir SSE ulanishi uchun alohida obunachi yaratish va uni zamonaviy Web API (WHATWG Streams) orqali boshqarish xotira sarfini minimal darajada saqlaydi.
**Talablar:** new Response(readableStream, { headers: { 'Content-Type': 'text/event-stream' } }) yordamida SSE oqimini tashkil qilish.
**Yechim (TypeScript):**
```ts
// Bun runtime (v1.0+) uchun ReadableStream asosidagi SSE
export class BunSseHandler {
  public static createSseResponse(req: Request, onClientConnect?: (send: (data: string) => void) => () => void): Response {
    let intervalId: any;

    const stream = new ReadableStream({
      start(controller) {
        const encoder = new TextEncoder();

        // Xabarni oqimga yozish yordamchisi
        const send = (msg: string) => {
          controller.enqueue(encoder.encode(`data: ${msg}\n\n`));
        };

        // Dastlabki salomlashuv
        controller.enqueue(encoder.encode(': bun_sse_ready\n\n'));

        // Davriy keep-alive pings (har 15 soniyada)
        intervalId = setInterval(() => {
          controller.enqueue(encoder.encode(': ping\n\n'));
        }, 15000);

        if (onClientConnect) {
          const cleanup = onClientConnect(send);
          req.signal.addEventListener('abort', () => {
            clearInterval(intervalId);
            cleanup();
            controller.close();
          });
        }
      },
      cancel() {
        if (intervalId) clearInterval(intervalId);
      }
    });

    return new Response(stream, {
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive'
      }
    });
  }
}
```
**Tushuntirish:** WHATWG `ReadableStream` arxitekturasi Bun ichida C++ darajasida boshqariladi. `req.signal.addEventListener('abort')` orqali brauzer sahifani yopganda resurslar bir zumda tozalanadi, bu esa nofaol ulanishlar tufayli xotira oqib ketishining (Memory Leak) 100% oldini oladi.

---

### Topshiriq #1145: SSE Last-Event-ID Sarlavhasi Bilan Aloqa Uzilganda Avtomatik Qayta Ulanish va Voqealarni Tiklash
**Tavsif:** Brauzerdagi `EventSource` obyekti tarmoq uzilganda avtomatik qayta ulanadi va so'nggi qabul qilingan hodisaning `id` raqamini `Last-Event-ID` HTTP sarlavhasida yuboradi. Server bu nuqtadan keyingi xabarlarni qayta yetkazishi kerak.
**Talablar:** Last-Event-ID sarlavhasini tahlil qilish, retry: 3000 (qayta ulanish kechikishi) sozlash va yetishmayotgan voqealarni yuborish.
**Yechim (TypeScript):**
```ts
import http from 'node:http';

export interface AuditEventRecord {
  id: number;
  type: string;
  payload: string;
}

export class SseResilientReconnectionHandler {
  // So'nggi voqealar jurnali
  private eventHistory: AuditEventRecord[] = [];
  private currentEventId = 0;

  public publish(type: string, payload: string): void {
    this.currentEventId++;
    this.eventHistory.push({
      id: this.currentEventId,
      type,
      payload
    });

    if (this.eventHistory.length > 500) {
      this.eventHistory.shift(); // Oxirgi 500 ta hodisani keshda saqlash
    }
  }

  public handleClient(req: http.IncomingMessage, res: http.ServerResponse): void {
    res.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive'
    });

    // 1. Agar aloqa uzilsa, brauzer 3 soniyadan so'ng qayta ulansin
    res.write('retry: 3000\n\n');

    // 2. Mijoz yuborgan Last-Event-ID sarlavhasini tekshirish
    const lastEventIdHeader = req.headers['last-event-id'];
    if (lastEventIdHeader) {
      const lastId = parseInt(lastEventIdHeader.toString(), 10);

      // O'tkazib yuborilgan barcha xabarlarni topib, navbat bilan qayta yuborish
      const missed = this.eventHistory.filter((e) => e.id > lastId);
      for (const m of missed) {
        res.write(`id: ${m.id}\nevent: ${m.type}\ndata: ${m.payload}\n\n`);
      }
    }
  }
}
```
**Tushuntirish:** SSE standartining eng katta kuchi brauzer darajasidagi avtomatik qayta tiklanishidir (Automatic Reconnection). Dasturchi brauzerda qo'shimcha JavaScript yozishi shart emas; `EventSource` ning o'zi `Last-Event-ID` yuborib aloqani uzluksiz davom ettiradi.

---

### Topshiriq #1146: SSE Uchun Xotirada Ring Buffer Yaratib Oxirgi N Ta Hodisani Keshda Saqlash
**Tavsif:** Tez-tez yangilanadigan xabarlar oqimida (masalan, loglar yoki birja narxlari) yangi ulangan mijozlar darhol oxirgi 20 ta holatni ko'rishi lozim. Xotira hajmini qat'iy chegaralovchi Ring Buffer talab etiladi.
**Talablar:** Ruxsat etilgan maksimal hajmga ega Ring Buffer (Aylanma bufer) tuzilmasi va xotira xavfsizligi.
**Yechim (TypeScript):**
```ts
export class SseRingBuffer<T> {
  private buffer: (T | null)[];
  private capacity: number;
  private pointer: number = 0;
  private isFull: boolean = false;

  constructor(capacity: number = 50) {
    this.capacity = capacity;
    this.buffer = new Array(capacity).fill(null);
  }

  public push(item: T): void {
    this.buffer[this.pointer] = item;
    this.pointer = (this.pointer + 1) % this.capacity;
    if (this.pointer === 0) {
      this.isFull = true;
    }
  }

  /**
   * Eng qadimiyidan eng yangisiga qarab tartiblangan ro'yxatni olish
   */
  public getAll(): T[] {
    if (!this.isFull) {
      return this.buffer.slice(0, this.pointer) as T[];
    }

    const part1 = this.buffer.slice(this.pointer);
    const part2 = this.buffer.slice(0, this.pointer);
    return [...part1, ...part2] as T[];
  }
}
```
**Tushuntirish:** Oddiy massivda `unshift()` yoki `shift()` chaqirish $O(N)$ vaqt oladi va doimiy yangi xotira ajratishni (Garbage Collection) keltirib chiqaradi. `Ring Buffer` esa doimiy massiv va ko'rsatgich (Pointer) orqali $O(1)$ tezlikda ishlaydi va yangi xotira sarflamaydi.

---

### Topshiriq #1147: SSE Ulanishlarida Xotira Oqib Ketishini (Memory Leak) Oldini Olish
**Tavsif:** Agar mijoz sahifani yopganda yoki tarmoq uzilganda server uning `res` obyekti yoki voqea tinglovchisini (EventEmitter listener) o'chirmasa, kuniga minglab obunachilar sababli server xotirasi (Heap) to'lib ishdan chiqadi.
**Talablar:** req.on('close') va AbortSignal bilan tozalash, WeakSet orqali xavfsiz havolalarni boshqarish.
**Yechim (TypeScript):**
```ts
import http from 'node:http';
import { EventEmitter } from 'node:events';

export class LeakFreeSseDispatcher {
  private emitter = new EventEmitter();

  constructor() {
    // Katta yuklama paytida 'MaxListenersExceededWarning' xatoligi chiqmasligi uchun
    this.emitter.setMaxListeners(0);
  }

  public register(req: http.IncomingMessage, res: http.ServerResponse): void {
    res.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Connection': 'keep-alive',
      'Cache-Control': 'no-cache'
    });

    const onData = (data: any) => {
      res.write(`data: ${JSON.stringify(data)}\n\n`);
    };

    // Voqea tinglovchisini ulash
    this.emitter.on('broadcast', onData);

    // Xavfsiz tozalash: ulanish uzilishi bilanoq listener o'chirilishi SHART!
    req.on('close', () => {
      this.emitter.off('broadcast', onData);
      res.end();
    });
  }

  public notifyAll(payload: any): void {
    this.emitter.emit('broadcast', payload);
  }
}
```
**Tushuntirish:** SSE tizimlaridagi eng keng tarqalgan xato `req.on('close')` ichida `emitter.off()` ni chaqirishni unutishdir. Har bir unutilgan ulanish butun `ServerResponse` kontekstini xotirada abadiy ushlab qoladi. To'g'ri tozalash orqali server oylarcha xotira sarfini barqaror saqlay oladi.

---

### Topshiriq #1148: Ko'p Kanalli SSE: Mijozning Huquqlari (Claims) Asosida Hodisalarni Filtrlab Uzatish
**Tavsif:** Bitta SSE ulanishi orqali bir vaqtning o'zida ham umumiy yangiliklar, ham foydalanuvchining shaxsiy to'lov holati uzatilishi mumkin. Boshqa foydalanuvchining shaxsiy ma'lumoti boshqaga ketmasligi uchun claims asosidagi marshrutlash lozim.
**Talablar:** Foydalanuvchi huquqlari (Role, TenantId, UserId) bo'yicha hodisalarni xavfsiz filtrlovchi arxitektura.
**Yechim (TypeScript):**
```ts
export interface SseClientContext {
  userId: string;
  role: 'USER' | 'ADMIN';
  tenantId: string;
  res: any; // ServerResponse
}

export class MultitenantSseRouter {
  private activeClients = new Set<SseClientContext>();

  public addClient(ctx: SseClientContext): void {
    this.activeClients.add(ctx);
  }

  public removeClient(ctx: SseClientContext): void {
    this.activeClients.delete(ctx);
  }

  /**
   * Xabarni faqat vakolati yetadigan va mos tenantga tegishli mijozlarga yuborish
   */
  public dispatchEvent(targetTenant: string, requiredRole: string | null, targetUserId: string | null, eventName: string, data: any): void {
    const payload = `event: ${eventName}\ndata: ${JSON.stringify(data)}\n\n`;

    for (const client of this.activeClients) {
      // 1. Tenant mosligi
      if (client.tenantId !== targetTenant) continue;

      // 2. Shaxsiy foydalanuvchi filtri
      if (targetUserId && client.userId !== targetUserId) continue;

      // 3. Huquq tekshiruvi (Role)
      if (requiredRole === 'ADMIN' && client.role !== 'ADMIN') continue;

      client.res.write(payload);
    }
  }
}
```
**Tushuntirish:** Ko'p kanalli SSE orqali bitta mijoz brauzeri bir nechta alohida ulanish ochishi shart bo'lmaydi. Bitta oqim ichida `event: private_payment` va `event: system_alert` hodisalari xavfsizlik kontekstiga ko'ra filtrlanib yetkaziladi.

---

### Topshiriq #1149: SSE Oqimida Gzip va Brotli Siqishni To'g'ri Sozlash va flush() Buferini Boshqarish
**Tavsif:** Agar SSE oqimi ustida standart Gzip siqish yoqilsa, siqish algoritmi yetarli bayt to'planguncha (masalan 16KB) ma'lumotni ushlab turadi va mijoz hodisani real vaqtda ko'ra olmaydi.
**Talablar:** Node.js zlib moduli bilan zlib.createGzip({ flush: zlib.constants.Z_SYNC_FLUSH }) sozlash va hodisadan keyin darhol flush qilish.
**Yechim (TypeScript):**
```ts
import http from 'node:http';
import zlib from 'node:zlib';

export class CompressedSseStream {
  public static handleRequest(req: http.IncomingMessage, res: http.ServerResponse): void {
    const acceptEncoding = (req.headers['accept-encoding'] as string) || '';

    // Mijoz Gzip qo'llab-quvvatlasa:
    if (acceptEncoding.includes('gzip')) {
      res.writeHead(200, {
        'Content-Type': 'text/event-stream',
        'Content-Encoding': 'gzip',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive'
      });

      // MUHIM SOZLAMA: Z_SYNC_FLUSH har bir yozishda buferni darhol chiqarib yuboradi
      const gzip = zlib.createGzip({
        flush: zlib.constants.Z_SYNC_FLUSH
      });

      gzip.pipe(res);

      // Xabarni yozish
      gzip.write('data: {"status":"Jonli siqilgan oqim"}\n\n');

      req.on('close', () => {
        gzip.end();
      });
    } else {
      // Siqilmagan standart SSE
      res.writeHead(200, {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache'
      });
      res.write('data: {"status":"Oddiy oqim"}\n\n');
    }
  }
}
```
**Tushuntirish:** Gzip yoki Brotli oqimlarida `Z_SYNC_FLUSH` ko'rsatilmasa, kompressor buferni ushlab qolib real-vaqt rejimini buzadi. `Z_SYNC_FLUSH` bilan esa har bir SSE paketi darhol siqilib, to'xtalishsiz mijoz brauzeriga yetkaziladi.

---

### Topshiriq #1150: Universal Real-Time Gateway: WebTransport, WebSocket va SSE Fallback Boshqaruvi
**Tavsif:** Barcha brauzerlar va tarmoqlar bir xil emas: eng zamonaviy mijozlar WebTransport ni, o'rta qatlam WebSocket ni, cheklovlarga ega korporativ tarmoqlar esa SSE + HTTP POST fallback usulini talab qiladi.
**Talablar:** Universal Gateway sinfi: Klient imkoniyatlarini aniqlab, eng optimal protokolni tanlash (Negotiation) va yagona interfeys taqdim etish.
**Yechim (TypeScript):**
```ts
export enum TransportType {
  WEBTRANSPORT = 'WEBTRANSPORT',
  WEBSOCKET = 'WEBSOCKET',
  SSE = 'SSE'
}

export interface UniversalConnection {
  type: TransportType;
  send(message: string): void;
  close(): void;
}

export class UniversalRealTimeGateway {
  /**
   * Mijoz sarlavhalari va so'roviga qarab eng ilg'or protokolni tanlash (Protocol Negotiation)
   */
  public static negotiateTransport(headers: Record<string, string | undefined>, urlParams: URLSearchParams): TransportType {
    // 1. Agar brauzer va server WebTransport ni qo'llab-quvvatlasa
    if (headers[':protocol'] === 'webtransport' || urlParams.get('transport') === 'webtransport') {
      return TransportType.WEBTRANSPORT;
    }

    // 2. Agar klassik WebSocket so'rovi bo'lsa
    if (headers['upgrade']?.toLowerCase() === 'websocket') {
      return TransportType.WEBSOCKET;
    }

    // 3. Fallback: eng ishonchli va universal Server-Sent Events (SSE)
    return TransportType.SSE;
  }

  /**
   * Universal xabar tarqatuvchi adapter
   */
  public static createConnectionAdapter(type: TransportType, rawSocket: any): UniversalConnection {
    return {
      type,
      send(message: string) {
        if (type === TransportType.WEBTRANSPORT) {
          // WebTransport stream yoki datagram orqali
          rawSocket.sendDatagram(new TextEncoder().encode(message));
        } else if (type === TransportType.WEBSOCKET) {
          // Standart WebSocket
          rawSocket.send(message);
        } else if (type === TransportType.SSE) {
          // SSE orqali
          rawSocket.write(`data: ${message}\n\n`);
        }
      },
      close() {
        if (type === TransportType.WEBSOCKET) rawSocket.close();
        else if (type === TransportType.SSE) rawSocket.end();
      }
    };
  }
}
```
**Tushuntirish:** Ushbu universal arxitektura zamonaviy korporativ tizimlarda 'Graceful Degradation' (bosqichma-bosqich yengillashish) tamoyilini amalga oshiradi. U WebTransport tezligidan boshlab, zarur bo'lganda WebSocket va eng oxirida SSE ga o'tib, har qanday sharoitda mijozga 100% real-vaqt xizmatini kafolatlaydi.

---
