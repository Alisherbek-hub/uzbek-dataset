# Khorazmiy AI: Java - Modul 23
## Mavzu: Tarmoq protokollari: Netty NIO/Epoll, HTTP/3, WebSockets va yuqori yuklamali gRPC

### Topshiriq #1101: Netty ServerBootstrap va Epoll/KQueue vs NIO EventLoopGroup ni avtomatik tanlash
**Tavsif:** Linux serverlarida maksimal tarmoq unumdorligiga erishish uchun Epoll (edge-triggered) mexanizmidan, macOS da KQueue, boshqa operatsion tizimlarda esa standart Java NIO dan avtomatik foydalanuvchi yuqori yuklamali ServerBootstrap yaratish.
**Talablar:** Epoll.isAvailable() va KQueue.isAvailable() tekshiruvi, to'g'ri ServerSocketChannel va SocketChannel klasslarini initsializatsiya qilish, EventLoopGroup resurslarini to'g'ri boshqarish va graceful shutdown kafolati.
**Yechim (Java):**
```java
package com.khorazmiy.network.bootstrap;

import io.netty.bootstrap.ServerBootstrap;
import io.netty.channel.*;
import io.netty.channel.epoll.Epoll;
import io.netty.channel.epoll.EpollEventLoopGroup;
import io.netty.channel.epoll.EpollServerSocketChannel;
import io.netty.channel.kqueue.KQueue;
import io.netty.channel.kqueue.KQueueEventLoopGroup;
import io.netty.channel.kqueue.KQueueServerSocketChannel;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.SocketChannel;
import io.netty.channel.socket.nio.NioServerSocketChannel;
import io.netty.handler.logging.LogLevel;
import io.netty.handler.logging.LoggingHandler;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.concurrent.TimeUnit;

/**
 * Operatsion tizimga mos ravishda Epoll, KQueue yoki NIO transportini
 * avtomatik tanlovchi yuqori unumdor Netty server bootstrap moduli.
 */
public class NativeTransportServer {
    private static final Logger log = LoggerFactory.getLogger(NativeTransportServer.class);

    private final int port;
    private EventLoopGroup bossGroup;
    private EventLoopGroup workerGroup;

    public NativeTransportServer(int port) {
        this.port = port;
    }

    public void start() throws InterruptedException {
        Class<? extends ServerChannel> channelClass;

        // Operatsion tizimning native transport imkoniyatlarini tekshirish
        if (Epoll.isAvailable()) {
            log.info("Linux Epoll native transport faollashtirildi (Yuqori unumdorlik)");
            bossGroup = new EpollEventLoopGroup(1); // Ulanishlarni qabul qiluvchi oqim
            workerGroup = new EpollEventLoopGroup(Runtime.getRuntime().availableProcessors() * 2);
            channelClass = EpollServerSocketChannel.class;
        } else if (KQueue.isAvailable()) {
            log.info("BSD/macOS KQueue native transport faollashtirildi");
            bossGroup = new KQueueEventLoopGroup(1);
            workerGroup = new KQueueEventLoopGroup(Runtime.getRuntime().availableProcessors() * 2);
            channelClass = KQueueServerSocketChannel.class;
        } else {
            log.info("Standart Java NIO transporti ishga tushirildi");
            bossGroup = new NioEventLoopGroup(1);
            workerGroup = new NioEventLoopGroup(Runtime.getRuntime().availableProcessors() * 2);
            channelClass = NioServerSocketChannel.class;
        }

        try {
            ServerBootstrap b = new ServerBootstrap();
            b.group(bossGroup, workerGroup)
             .channel(channelClass)
             .handler(new LoggingHandler(LogLevel.INFO))
             .childHandler(new ChannelInitializer<SocketChannel>() {
                 @Override
                 protected void initChannel(SocketChannel ch) {
                     ChannelPipeline p = ch.pipeline();
                     // Tarmoq ulanishi initsializatsiyasi
                     p.addLast(new SimpleChannelInboundHandler<Object>() {
                         @Override
                         protected void channelRead0(ChannelHandlerContext ctx, Object msg) {
                             // Kiruvchi ma'lumotlarni qayta ishlash
                             ctx.writeAndFlush(msg);
                         }
                     });
                 }
             })
             // Tizim soket sozlamalari
             .option(ChannelOption.SO_BACKLOG, 10240) // Katta ulanish navbati
             .childOption(ChannelOption.SO_KEEPALIVE, true)
             .childOption(ChannelOption.TCP_NODELAY, true); // Nagle algoritmini o'chirish

            ChannelFuture future = b.bind(port).sync();
            log.info("Server muvaffaqiyatli ishga tushdi, port: {}", port);
            future.channel().closeFuture().sync();
        } finally {
            shutdownGracefully();
        }
    }

    public void shutdownGracefully() {
        log.info("Server to'xtatilmoqda, resurslar tozalanmoqda...");
        if (bossGroup != null) {
            bossGroup.shutdownGracefully(2, 15, TimeUnit.SECONDS);
        }
        if (workerGroup != null) {
            workerGroup.shutdownGracefully(2, 15, TimeUnit.SECONDS);
        }
    }

    public static void main(String[] args) throws Exception {
        new NativeTransportServer(8080).start();
    }
}
```
**Tushuntirish:** Linux muhitida Netty ning `epoll` transportidan foydalanish standart Java NIO ga qaraganda syscall overhead (tizim chaqiruvlari yukini) va xotira allokatsiyasini keskin kamaytiradi. Epoll Edge-Triggered (ET) rejimida ishlaydi, bu esa soket holati o'zgargandagina hodisa uyg'otadi. `SO_BACKLOG` parametri SYN-flood va ulanish to'lqinlarida mijozlar rad etilishining oldini oladi. `TCP_NODELAY` Nagle algoritmini o'chirib, paketlar to'planishini kutmasdan darhol jo'natilishini kafolatlaydi.

---

### Topshiriq #1102: Netty ByteBuf xotira boshqaruvi: Zero-copy slicing, CompositeByteBuf va Pooled Allocator
**Tavsif:** Fintech va telemetriya platformalarida har soniyada yuz minglab paketlar keladi. An'anaviy byte[] nusxalash GC (Garbage Collection) bosimini oshiradi. Netty PooledByteBufAllocator yordamida direct xotira hovuzi va zero-copy kompozitsiyasini yaratish talab qilinadi.
**Talablar:** PooledByteBufAllocator dan direct buffer ajratish, CompositeByteBuf orqali header va body ni nusxalashsiz birlashtirish, ReferenceCountUtil va release() bilan off-heap xotira sizib chiqishini bartaraf etish.
**Yechim (Java):**
```java
package com.khorazmiy.network.buffer;

import io.netty.buffer.*;
import io.netty.util.ReferenceCountUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.nio.charset.StandardCharsets;

/**
 * Netty ByteBuf zero-copy va off-heap xotira boshqaruvi namunasi.
 */
public class ZeroCopyPacketManager {
    private static final Logger log = LoggerFactory.getLogger(ZeroCopyPacketManager.class);

    // Pooled direct memory allocator - Garbage Collector ga yuk tushirmaydi
    private final ByteBufAllocator allocator = PooledByteBufAllocator.DEFAULT;

    public void processZeroCopyPacket() {
        ByteBuf header = null;
        ByteBuf body = null;
        CompositeByteBuf composite = null;
        ByteBuf slice = null;

        try {
            // 1. Off-heap (direct) hovuzdan buffer ajratish
            header = allocator.directBuffer(16);
            header.writeInt(0xCAFEBABE); // Magic header raqami
            header.writeShort(1);        // Protokol versiyasi
            header.writeLong(System.currentTimeMillis()); // Vaqt tamg'asi
            header.writeShort(128);      // Tana qismi uzunligi

            body = allocator.directBuffer(128);
            body.writeBytes("Xavfsiz bank tranzaksiyasi: 50,000 UZS".getBytes(StandardCharsets.UTF_8));

            // 2. CompositeByteBuf - Ikki bufferni xotirada nusxalamasdan bitta oqimga birlashtirish (Zero-Copy)
            composite = allocator.compositeDirectBuffer();
            // increaseWriterIndex=true orqali yozish ko'rsatkichini avtomatik siljitish
            composite.addComponents(true, header.retain(), body.retain());

            log.info("Kompozit paket umumiy hajmi: {} bayt, komponentlar soni: {}", 
                     composite.readableBytes(), composite.numComponents());

            // 3. Slice olish - Yangi xotira ajratmasdan, mavjud buffer ustida virtual oyna ochish
            // Masalan faqat tanani o'qish uchun:
            slice = composite.slice(16, composite.readableBytes() - 16);
            byte[] bodyData = new byte[slice.readableBytes()];
            slice.readBytes(bodyData);
            log.info("Kesib olingan tana ma'lumoti: {}", new String(bodyData, StandardCharsets.UTF_8));

        } finally {
            // Reference Counted obyektlarni xavfsiz tozalash (Off-heap xotira oqib ketmasligi uchun)
            ReferenceCountUtil.safeRelease(header);
            ReferenceCountUtil.safeRelease(body);
            ReferenceCountUtil.safeRelease(composite);
            // slice() alohida release() talab qilmaydi, u ota bufferni retain qilgan bo'lsa o'shani tozalaydi
        }
    }

    public static void main(String[] args) {
        new ZeroCopyPacketManager().processZeroCopyPacket();
    }
}
```
**Tushuntirish:** Netty ByteBuf klassi jemalloc algoritmidan foydalanuvchi `PooledByteBufAllocator` orqali ishlaydi. Bu direct (off-heap) xotira bo'laklarini qayta ishlatib, JVM Heap xotirasi va Garbage Collector to'xtashlarini (STW pause) bartaraf etadi. `CompositeByteBuf` bir nechta buferlarni xotirada nusxa ko'chirmasdan bitta mantiqiy bufer sifatida taqdim etadi. `slice()` esa mavjud xotira segmentiga yangi o'qish/yozish ko'rsatkichli oyna yaratadi. Reference counting (`retain()` / `release()`) off-heap xotira sizib ketishining oldini oladi.

---

### Topshiriq #1103: Netty ChannelPipeline va ChannelInbound/OutboundHandler zanjiri arxitekturasi
**Tavsif:** Murakkab korporativ protokollarda ma'lumotlar dekodlash, biznes logika, xavfsizlik va javobni kodlash bosqichlaridan o'tadi. Pipeline ichida xatoliklarning to'g'ri ushlanishi va kontekst oqimi kafolatlanishi zarur.
**Talablar:** Inbound va Outbound handlerlar zanjirini tuzish, `ctx.fireChannelRead()` va `ctx.write()` farqini ko'rsatish, `exceptionCaught()` orqali xatoliklarni markazlashgan boshqarish.
**Yechim (Java):**
```java
package com.khorazmiy.network.pipeline;

import io.netty.channel.*;
import io.netty.handler.codec.string.StringDecoder;
import io.netty.handler.codec.string.StringEncoder;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.nio.charset.StandardCharsets;

/**
 * Netty Pipeline Inbound va Outbound handlerlar zanjiri arxitekturasi.
 */
public class RobustPipelineDemo {
    private static final Logger log = LoggerFactory.getLogger(RobustPipelineDemo.class);

    // Kiruvchi so'rovlarni tekshiruvchi xavfsizlik handleri
    public static class SecurityInboundHandler extends ChannelInboundHandlerAdapter {
        @Override
        public void channelRead(ChannelHandlerContext ctx, Object msg) throws Exception {
            String incoming = (String) msg;
            if (incoming.contains("BLOCKED_TOKEN")) {
                log.warn("Xavfli so'rov aniqlandi! Ulanish uzilmoqda: {}", ctx.channel().remoteAddress());
                ctx.close(); // Xavfli mijozni darhol uzish
                return;
            }
            log.info("Xavfsizlik tekshiruvidan o'tdi: {}", incoming);
            // Zanjir bo'yicha keyingi handlerga uzatish
            ctx.fireChannelRead(msg);
        }

        @Override
        public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) {
            log.error("Xavfsizlik modulida istisno: {}", cause.getMessage());
            ctx.close();
        }
    }

    // Biznes mantiq handleri
    public static class BusinessLogicHandler extends SimpleChannelInboundHandler<String> {
        @Override
        protected void channelRead0(ChannelHandlerContext ctx, String msg) {
            log.info("Biznes mantiq qayta ishlanmoqda: {}", msg);
            String response = "REPLY: Qabul qilindi -> " + msg.toUpperCase();
            // Outbound zanjiriga uzatish
            ctx.writeAndFlush(response);
        }

        @Override
        public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) {
            log.error("Biznes mantiqda xatolik yuz berdi: ", cause);
            ctx.writeAndFlush("ERROR: Ichki server xatosi\n").addListener(ChannelFutureListener.CLOSE);
        }
    }

    // Chiquvchi ma'lumotlarni audit qiluvchi Outbound handler
    public static class AuditOutboundHandler extends ChannelOutboundHandlerAdapter {
        @Override
        public void write(ChannelHandlerContext ctx, Object msg, ChannelPromise promise) throws Exception {
            log.info("Chiquvchi javob audit qilindi: {}", msg);
            // Outbound zanjiri bo'yicha keyingi handlerga (soketga qarab) uzatish
            super.write(ctx, msg, promise);
        }
    }

    public static void configurePipeline(ChannelPipeline pipeline) {
        // Dekoder va Enkoderlar
        pipeline.addLast("decoder", new StringDecoder(StandardCharsets.UTF_8));
        pipeline.addLast("encoder", new StringEncoder(StandardCharsets.UTF_8));
        
        // Maxsus xizmat handlerlari
        pipeline.addLast("auditOutbound", new AuditOutboundHandler());
        pipeline.addLast("securityInbound", new SecurityInboundHandler());
        pipeline.addLast("businessHandler", new BusinessLogicHandler());
    }
}
```
**Tushuntirish:** Netty ChannelPipeline ikki yo'nalishli bog'langan ro'yxat (Doubly Linked List) asosida qurilgan. Kiruvchi (Inbound) hodisalar boshidan oxiriga qarab (`ctx.fireChannelRead()`), chiquvchi (Outbound) amallar esa chaqirilgan joydan boshiga qarab (`ctx.write()`) harakatlanadi. `ChannelHandlerContext.write()` zanjirda faqat joriy handlerdan oldingi outbound handlerlarni chaqirsa, `channel.write()` butun pipeline oxiridan boshlab chaqiradi. `exceptionCaught()` orqali zanjirning istalgan joyidagi xatolar tutiladi.

---

### Topshiriq #1104: High-throughput TCP Server: ChannelOption va Low-level Soket Sozlamalari
**Tavsif:** Fintech to'lov shlyuzlarida har soniyada 100,000 dan ortiq TCP ulanishlar bilan ishlashda operatsion tizim soket buferlari va ulanish navbatlarini maksimal samaradorlikka sozlash talab etiladi.
**Talablar:** SO_BACKLOG, TCP_NODELAY, SO_KEEPALIVE, SO_REUSEADDR, WRITE_BUFFER_WATER_MARK va ALLOCATOR opsiyalarini to'g'ri konfiguratsiya qilish.
**Yechim (Java):**
```java
package com.khorazmiy.network.tuning;

import io.netty.bootstrap.ServerBootstrap;
import io.netty.buffer.PooledByteBufAllocator;
import io.netty.channel.*;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.SocketChannel;
import io.netty.channel.socket.nio.NioServerSocketChannel;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Yuqori yuklamali tizimlar uchun sozlangan TCP soket opsiyalari.
 */
public class TunedTcpServer {
    private static final Logger log = LoggerFactory.getLogger(TunedTcpServer.class);

    public void startServer(int port) throws InterruptedException {
        EventLoopGroup bossGroup = new NioEventLoopGroup(2);
        EventLoopGroup workerGroup = new NioEventLoopGroup(Runtime.getRuntime().availableProcessors() * 2);

        try {
            ServerBootstrap b = new ServerBootstrap();
            b.group(bossGroup, workerGroup)
             .channel(NioServerSocketChannel.class)
             // 1. SO_BACKLOG: Operatsion tizim TCP SYN navbati hajmi (Linux /proc/sys/net/core/somaxconn bilan mos)
             .option(ChannelOption.SO_BACKLOG, 65535)
             // 2. SO_REUSEADDR: Server qayta ishga tushganda TIME_WAIT holatidagi portni darhol egallash
             .option(ChannelOption.SO_REUSEADDR, true)
             // 3. Pooled direct memory allocator tanlash
             .option(ChannelOption.ALLOCATOR, PooledByteBufAllocator.DEFAULT)
             
             // Bolalar soketlari (mijoz ulanishlari) uchun sozlamalar:
             .childOption(ChannelOption.ALLOCATOR, PooledByteBufAllocator.DEFAULT)
             // 4. TCP_NODELAY: Kichik paketlarni yig'masdan darhol uzatish (Nagle algoritmini o'chirish)
             .childOption(ChannelOption.TCP_NODELAY, true)
             // 5. SO_KEEPALIVE: Tarmoq darajasida vaqti-vaqti bilan prob paketlarini yuborib turish
             .childOption(ChannelOption.SO_KEEPALIVE, true)
             // 6. SO_RCVBUF va SO_SNDBUF bufer o'lchamlari
             .childOption(ChannelOption.SO_RCVBUF, 128 * 1024) // 128 KB kiruvchi bufer
             .childOption(ChannelOption.SO_SNDBUF, 128 * 1024) // 128 KB chiquvchi bufer
             // 7. WriteBufferWaterMark: Backpressure nazorati (Pastki chegara 32KB, yuqori chegara 64KB)
             .childOption(ChannelOption.WRITE_BUFFER_WATER_MARK, new WriteBufferWaterMark(32 * 1024, 64 * 1024))
             
             .childHandler(new ChannelInitializer<SocketChannel>() {
                 @Override
                 protected void initChannel(SocketChannel ch) {
                     ch.pipeline().addLast(new ChannelInboundHandlerAdapter() {
                         @Override
                         public void channelActive(ChannelHandlerContext ctx) {
                             log.debug("Mijoz ulandi: {}", ctx.channel().remoteAddress());
                         }
                     });
                 }
             });

            ChannelFuture f = b.bind(port).sync();
            log.info("Optimizatsiyalangan TCP server {} portida ishga tushdi", port);
            f.channel().closeFuture().sync();
        } finally {
            bossGroup.shutdownGracefully();
            workerGroup.shutdownGracefully();
        }
    }
}
```
**Tushuntirish:** `SO_BACKLOG` ulanish navbatini kengaytirib, ulanishlar oqimi birdaniga oshganda paketlar tushib qolishini oldini oladi. `WriteBufferWaterMark` Netty ning xotira to'lib ketishiga qarshi himoya mexanizmi bo'lib, unumdorlik va barqarorlikni ta'minlaydi. Agar chiquvchi bufer hajmi highWaterMark (64KB) dan oshsa, `channel.isWritable()` false holatiga o'tadi va backpressure boshqaruvini ishga tushiradi.

---

### Topshiriq #1105: Netty Backpressure boshqaruvi: channel.isWritable() va channelWritabilityChanged orqali OOM oldini olish
**Tavsif:** Tezkor server sekin mijozga katta hajmda ma'lumot jo'natganda, ma'lumotlar Netty chiquvchi navbatida yig'ilib, Out-of-Memory (OOM) xatosiga olib kelishi mumkin. Backpressure mexanizmi orqali ma'lumot uzatishni to'xtatib turish va qayta tiklash talab etiladi.
**Talablar:** channelWritabilityChanged() hodisasini ushlash, channel.isWritable() tekshiruvi, autoRead ni boshqarish yoki oqimni pauza qilish.
**Yechim (Java):**
```java
package com.khorazmiy.network.backpressure;

import io.netty.buffer.ByteBuf;
import io.netty.channel.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Queue;
import java.util.concurrent.ConcurrentLinkedQueue;

/**
 * Sekin mijozlar sababli xotira to'lib ketishini (OOM) oldini oluvchi
 * Backpressure nazoratchisi.
 */
public class BackpressureStreamHandler extends ChannelInboundHandlerAdapter {
    private static final Logger log = LoggerFactory.getLogger(BackpressureStreamHandler.class);

    private final Queue<ByteBuf> pendingMessages = new ConcurrentLinkedQueue<>();

    @Override
    public void channelWritabilityChanged(ChannelHandlerContext ctx) throws Exception {
        boolean writable = ctx.channel().isWritable();
        log.info("Kanal yozishga tayyorlik holati o'zgardi: isWritable = {}", writable);

        if (writable) {
            // Soket buferi bo'shadi, to'plangan navbatdagi xabarlarni yuboramiz
            drainQueue(ctx);
            // Kiruvchi yangi ma'lumotlarni o'qishni qayta yoqamiz
            ctx.channel().config().setAutoRead(true);
        } else {
            // Chiquvchi bufer to'ldi! Yangi ma'lumotlarni o'qishni vaqtincha to'xtatamiz
            log.warn("Chiquvchi bufer to'ldi! Backpressure ishga tushdi, AutoRead o'chirildi.");
            ctx.channel().config().setAutoRead(false);
        }
        super.channelWritabilityChanged(ctx);
    }

    public void sendMessage(ChannelHandlerContext ctx, ByteBuf msg) {
        if (ctx.channel().isWritable()) {
            ctx.writeAndFlush(msg);
        } else {
            log.debug("Kanal to'lgan, xabar navbatga qo'yildi");
            pendingMessages.offer(msg);
        }
    }

    private void drainQueue(ChannelHandlerContext ctx) {
        while (ctx.channel().isWritable() && !pendingMessages.isEmpty()) {
            ByteBuf msg = pendingMessages.poll();
            if (msg != null) {
                ctx.write(msg);
            }
        }
        ctx.flush();
    }

    @Override
    public void channelInactive(ChannelHandlerContext ctx) throws Exception {
        // Ulanish yopilganda navbatdagi qolgan buferlarni tozalash
        ByteBuf buf;
        while ((buf = pendingMessages.poll()) != null) {
            buf.release();
        }
        super.channelInactive(ctx);
    }
}
```
**Tushuntirish:** Netty da soketga yozish asinxron amalga oshiriladi. Agar yozish tezligi tarmoq o'tkazuvchanligidan baland bo'lsa, xabarlar `ChannelOutboundBuffer` da to'planadi. `WRITE_BUFFER_WATER_MARK` yuqori chegarasiga yetganda `channelWritabilityChanged` chaqiriladi va `channel.isWritable()` false bo'ladi. Bunday holatda `setAutoRead(false)` chaqirilib, operatsion tizimdan kiruvchi paketlarni qabul qilish to'xtatiladi, bu esa TCP oyna o'lchami (Window Size) orqali qarshi tomonga ham backpressure uzatadi.

---

### Topshiriq #1106: Custom Framing Protocollar: LengthFieldBasedFrameDecoder va LengthFieldPrepender
**Tavsif:** TCP oqimli protokol bo'lgani sababli, paketlar birlashib ketishi (TCP packet sticking) yoki bo'linib ketishi (fragmentation) mumkin. Uzunlik maydoniga asoslangan maxsus binar protokollarni to'g'ri parslash zarur.
**Talablar:** LengthFieldBasedFrameDecoder va LengthFieldPrepender yordamida 4-baytli uzunlik prefiksiga ega xavfsiz framing arxitekturasini yaratish.
**Yechim (Java):**
```java
package com.khorazmiy.network.framing;

import io.netty.buffer.ByteBuf;
import io.netty.channel.*;
import io.netty.handler.codec.LengthFieldBasedFrameDecoder;
import io.netty.handler.codec.LengthFieldPrepender;
import io.netty.handler.codec.MessageToByteEncoder;
import io.netty.handler.codec.ReplayingDecoder;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.nio.charset.StandardCharsets;
import java.util.List;

/**
 * TCP paketlar parchalanishi va birlashishini oldini oluvchi
 * Length-Field asosidagi ramkalash (Framing) moduli.
 */
public class FramedProtocolPipeline {
    private static final Logger log = LoggerFactory.getLogger(FramedProtocolPipeline.class);

    public static class CustomMessage {
        private final int messageType;
        private final String payload;

        public CustomMessage(int messageType, String payload) {
            this.messageType = messageType;
            this.payload = payload;
        }

        public int getMessageType() { return messageType; }
        public String getPayload() { return payload; }
    }

    // Biznes obyektni binar shaklga o'tkazuvchi enkoder
    public static class CustomMessageEncoder extends MessageToByteEncoder<CustomMessage> {
        @Override
        protected void encode(ChannelHandlerContext ctx, CustomMessage msg, ByteBuf out) {
            byte[] bytes = msg.getPayload().getBytes(StandardCharsets.UTF_8);
            out.writeInt(msg.getMessageType()); // 4 bayt xabar turi
            out.writeBytes(bytes);              // Tana ma'lumotlari
        }
    }

    // Binar ramkani biznes obyektga aylantiruvchi dekoder
    public static class CustomMessageDecoder extends ChannelInboundHandlerAdapter {
        @Override
        public void channelRead(ChannelHandlerContext ctx, Object msg) {
            ByteBuf in = (ByteBuf) msg;
            try {
                int messageType = in.readInt();
                byte[] data = new byte[in.readableBytes()];
                in.readBytes(data);
                String content = new String(data, StandardCharsets.UTF_8);

                CustomMessage parsed = new CustomMessage(messageType, content);
                log.info("Muvaffaqiyatli dekodlandi: Type={}, Payload={}", parsed.getMessageType(), parsed.getPayload());
                ctx.fireChannelRead(parsed);
            } finally {
                in.release();
            }
        }
    }

    public static void setupPipeline(ChannelPipeline pipeline) {
        // 1. Chiquvchi paket boshiga 4 baytli paket uzunligini qo'shuvchi enkoder
        pipeline.addLast("framePrepender", new LengthFieldPrepender(4));
        pipeline.addLast("messageEncoder", new CustomMessageEncoder());

        // 2. Kiruvchi oqimdan 4 baytli uzunlikni o'qib, paketni to'liq ajratib beruvchi dekoder
        // maxFrameLength: 1MB, lengthFieldOffset: 0, lengthFieldLength: 4, lengthAdjustment: 0, initialBytesToStrip: 4
        pipeline.addLast("frameDecoder", new LengthFieldBasedFrameDecoder(1024 * 1024, 0, 4, 0, 4));
        pipeline.addLast("messageDecoder", new CustomMessageDecoder());
    }
}
```
**Tushuntirish:** TCP oqimida chegaralar mavjud emas (stream-oriented). `LengthFieldPrepender(4)` xabar yuborishda uning uzunligini hisoblab, boshiga 4 bayt qilib yozadi. `LengthFieldBasedFrameDecoder` esa kelayotgan baytlarni o'qib, boshidagi 4 baytni uzunlik deb taniydi va to'liq paket yig'ilmaguncha keyingi handlerga uzatmaydi. `initialBytesToStrip = 4` parametr orqali keyingi handlerga faqat xabarning o'zi (uzunlik maydonisiz) toza holda topshiriladi.

---

### Topshiriq #1107: Netty DelimiterBasedFrameDecoder orqali IoT va Telemetriya Ma'lumotlarini Qabul Qilish
**Tavsif:** Ko'plab IoT va sanoat datchiklari ma'lumotlarni qator yakunlovchi maxsus belgilar (`\r\n` yoki maxsus bayt) bilan ajratilgan holda uzatadi. Delimiter asosidagi xavfsiz dekoder yaratish lozim.
**Talablar:** DelimiterBasedFrameDecoder, LineBasedFrameDecoder, maxFrameLength chegarasi va DoS hujumlariga qarshi bufer toshishidan himoyalanish.
**Yechim (Java):**
```java
package com.khorazmiy.network.delimiter;

import io.netty.buffer.ByteBuf;
import io.netty.buffer.Unpooled;
import io.netty.channel.*;
import io.netty.handler.codec.DelimiterBasedFrameDecoder;
import io.netty.handler.codec.Delimiters;
import io.netty.handler.codec.TooLongFrameException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.nio.charset.StandardCharsets;

/**
 * IoT va Telemetriya datchiklari uchun maxsus ajratgichli
 * xavfsiz freym dekoderi.
 */
public class TelemetryFrameHandler extends SimpleChannelInboundHandler<ByteBuf> {
    private static final Logger log = LoggerFactory.getLogger(TelemetryFrameHandler.class);

    public static void configurePipeline(ChannelPipeline pipeline) {
        // Maxsus ajratgich: masalan datchiklar ishlatadigan '$$' belgisi yoki standart CRLF
        ByteBuf customDelimiter = Unpooled.wrappedBuffer(new byte[]{'$', '$'});

        // Maksimal freym hajmi: 4096 bayt (Hujumchilar xotirani to'ldirmasligi uchun)
        // stripDelimiter: true (Ajratgichni o'chirib tashlash)
        pipeline.addLast("delimiterDecoder", new DelimiterBasedFrameDecoder(4096, true, customDelimiter));
        pipeline.addLast("telemetryHandler", new TelemetryFrameHandler());
    }

    @Override
    protected void channelRead0(ChannelHandlerContext ctx, ByteBuf msg) {
        String sensorData = msg.toString(StandardCharsets.UTF_8);
        log.info("Datchik telemetriyasi qabul qilindi: {}", sensorData);

        // Javob qaytarish (Tasdiqlash kodi bilan birga '$$' ajratgichini qo'shish)
        ByteBuf response = Unpooled.copiedBuffer("ACK:OK$$", StandardCharsets.UTF_8);
        ctx.writeAndFlush(response);
    }

    @Override
    public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) {
        if (cause instanceof TooLongFrameException) {
            log.error("Chegaradan oshgan freym aniqlandi! Mumkin bo'lgan DoS hujumi: {}", cause.getMessage());
            // Zudlik bilan xavfli ulanishni yopish
            ctx.close();
        } else {
            log.error("Kutilmagan xatolik: ", cause);
            ctx.close();
        }
    }
}
```
**Tushuntirish:** Agar mijoz uzoq vaqt davomida ajratgich belgini yubormasa, xotira to'lib ketishi mumkin. Shu sababli `DelimiterBasedFrameDecoder` da `maxFrameLength` parametri majburiydir. Belgilangan chegaradan oshib ketganda `TooLongFrameException` yuzaga keladi va `exceptionCaught` da ulanish darhol uziladi. Bu IoT shlyuzlarini xotira toshishi (Buffer Overflow DoS) hujumlaridan himoya qiladi.

---

### Topshiriq #1108: IdleStateHandler va Heartbeat (Ping/Pong) Mexanizmi
**Tavsif:** Tarmoq uzilishlari, NAT jadvalining tozalanishi yoki mijoz dasturi to'satdan qotib qolishi sababli serverda o'lik (Half-Open) TCP ulanishlar yig'ilib qoladi. IdleStateHandler orqali o'lik soketlarni aniqlash va resurslarni bo'shatish zarur.
**Talablar:** IdleStateHandler konfiguratsiyasi (readerIdleTime, writerIdleTime, allIdleTime), IdleStateEvent hodisasini qayta ishlash, Ping yuborish va javob kelmaganda kanalni yopish.
**Yechim (Java):**
```java
package com.khorazmiy.network.heartbeat;

import io.netty.buffer.ByteBuf;
import io.netty.buffer.Unpooled;
import io.netty.channel.*;
import io.netty.handler.timeout.IdleState;
import io.netty.handler.timeout.IdleStateEvent;
import io.netty.handler.timeout.IdleStateHandler;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.nio.charset.StandardCharsets;
import java.util.concurrent.TimeUnit;

/**
 * Ulanish faolligini nazorat qiluvchi va o'lik soketlarni
 * tozalovchi Heartbeat moduli.
 */
public class HeartbeatChannelHandler extends ChannelInboundHandlerAdapter {
    private static final Logger log = LoggerFactory.getLogger(HeartbeatChannelHandler.class);

    private static final ByteBuf HEARTBEAT_PING = Unpooled.unreleasableBuffer(
            Unpooled.copiedBuffer("PING\n", StandardCharsets.UTF_8));

    private int unacknowledgedPings = 0;
    private static final int MAX_MISSED_PINGS = 3;

    public static void configurePipeline(ChannelPipeline pipeline) {
        // readerIdle: 30 soniya ma'lumot kelmasa
        // writerIdle: 15 soniya ma'lumot yuborilmasa
        // allIdle: 60 soniya umumiy harakatsizlik
        pipeline.addLast("idleStateHandler", new IdleStateHandler(30, 15, 60, TimeUnit.SECONDS));
        pipeline.addLast("heartbeatHandler", new HeartbeatChannelHandler());
    }

    @Override
    public void userEventTriggered(ChannelHandlerContext ctx, Object evt) throws Exception {
        if (evt instanceof IdleStateEvent) {
            IdleStateEvent e = (IdleStateEvent) evt;
            if (e.state() == IdleState.WRITER_IDLE) {
                // Ma'lumot uzatilmayotgan bo'lsa, mijozga PING jo'natamiz
                log.debug("Writer idle: PING yuborilmoqda -> {}", ctx.channel().remoteAddress());
                ctx.writeAndFlush(HEARTBEAT_PING.duplicate());
            } else if (e.state() == IdleState.READER_IDLE) {
                // Mijozdan belgilangan vaqt ichida javob kelmadi
                unacknowledgedPings++;
                log.warn("Reader idle: Mijozdan javob yo'q (O'tkazib yuborildi: {}/{})", 
                         unacknowledgedPings, MAX_MISSED_PINGS);

                if (unacknowledgedPings >= MAX_MISSED_PINGS) {
                    log.error("Mijoz javob bermayapti (Half-Open soket). Ulanish yopilmoqda: {}", 
                              ctx.channel().remoteAddress());
                    ctx.close();
                }
            }
        } else {
            super.userEventTriggered(ctx, evt);
        }
    }

    @Override
    public void channelRead(ChannelHandlerContext ctx, Object msg) {
        // Har qanday kiruvchi faoliyat hisoblagichni nolga tushiradi
        unacknowledgedPings = 0;
        ctx.fireChannelRead(msg);
    }
}
```
**Tushuntirish:** Internet marshrutizatorlari va korporativ firewall-lar uzoq vaqt harakatsiz turgan TCP ulanishlarni jimjit uzib tashlaydi (silent drop). `IdleStateHandler` Netty HashedWheelTimer asosida soket faoliyatsizligini o'lchaydi. Belgilangan vaqt oshganda `IdleStateEvent` yuboriladi. Agar ketma-ket bir nechta `PING` so'roviga mijozdan hech qanday bayt kelmasa, kanal majburiy yopiladi va server xotirasi hamda fayl deskriptorlari (`FD`) bo'shatiladi.

---

### Topshiriq #1109: Netty ChannelPoolMap va FixedChannelPool orqali Yuqori Unumdor TCP Client Connection Pool
**Tavsif:** Mikroservislar va tashqi to'lov tizimlari bilan har bir so'rovda yangi TCP ulanish ochish handshake kechikishi (3-way handshake) tufayli qimmatga tushadi. Netty FixedChannelPool orqali ulanishlarni qayta ishlatuvchi havza yaratish lozim.
**Talablar:** AbstractChannelPoolMap, FixedChannelPool, acquire() va release() metodlari, ulanishlar maksimal chegarasi va ulanish salomatligini tekshirish.
**Yechim (Java):**
```java
package com.khorazmiy.network.pool;

import io.netty.bootstrap.Bootstrap;
import io.netty.channel.*;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.pool.*;
import io.netty.channel.socket.nio.NioSocketChannel;
import io.netty.util.concurrent.Future;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.net.InetSocketAddress;

/**
 * Yuqori yuklamali tarmoq chaqiruvlari uchun Netty TCP Ulanishlar Hovuzi (Connection Pool).
 */
public class NettyConnectionPoolManager {
    private static final Logger log = LoggerFactory.getLogger(NettyConnectionPoolManager.class);

    private final EventLoopGroup group = new NioEventLoopGroup();
    private final ChannelPoolMap<InetSocketAddress, SimpleChannelPool> poolMap;

    public NettyConnectionPoolManager() {
        Bootstrap cb = new Bootstrap()
                .group(group)
                .channel(NioSocketChannel.class)
                .option(ChannelOption.TCP_NODELAY, true)
                .option(ChannelOption.SO_KEEPALIVE, true);

        // Har bir masofaviy manzil (host/port) uchun alohida hovuz yaratuvchi Map
        this.poolMap = new AbstractChannelPoolMap<InetSocketAddress, SimpleChannelPool>() {
            @Override
            protected SimpleChannelPool newPool(InetSocketAddress key) {
                return new FixedChannelPool(
                        cb.remoteAddress(key),
                        new AbstractChannelPoolHandler() {
                            @Override
                            public void channelCreated(Channel ch) {
                                log.info("Hovuzda yangi fizik kanal yaratildi: {}", ch.remoteAddress());
                                ChannelPipeline p = ch.pipeline();
                                // Zarur enkoder va dekoderlarni qo'shish
                            }

                            @Override
                            public void channelAcquired(Channel ch) {
                                log.debug("Kanal hovuzdan foydalanish uchun olindi: {}", ch.id());
                            }

                            @Override
                            public void channelReleased(Channel ch) {
                                log.debug("Kanal hovuzga qaytarildi: {}", ch.id());
                            }
                        },
                        ChannelHealthChecker.ACTIVE, // Faqat sog'lom kanallarni berish
                        FixedChannelPool.AcquireTimeoutAction.FAIL,
                        5000, // Kutish vaqti (ms)
                        50,   // Maksimal ulanishlar soni
                        100   // Maksimal kutish navbati
                );
            }
        };
    }

    public void executeRequest(InetSocketAddress target, Object requestData) {
        SimpleChannelPool pool = poolMap.get(target);
        Future<Channel> acquireFuture = pool.acquire();

        acquireFuture.addListener((Future<Channel> f) -> {
            if (f.isSuccess()) {
                Channel ch = f.getNow();
                log.info("Ulanish olindi, ma'lumot jo'natilmoqda...");
                
                ch.writeAndFlush(requestData).addListener((ChannelFuture writeFuture) -> {
                    // Amal bajarilgach kanalni yana hovuzga qaytarish shart!
                    pool.release(ch);
                });
            } else {
                log.error("Hovuzdan ulanish olib bo'lmadi: {}", f.cause().getMessage());
            }
        });
    }

    public void shutdown() {
        group.shutdownGracefully();
    }
}
```
**Tushuntirish:** Har bir yangi TCP ulanish kamida 1 round-trip-time (RTT) vaqt oladi, TLS bilan esa 2-3 RTT ga yetadi. `FixedChannelPool` belgilangan miqdordagi faol kanallarni ochiq saqlaydi va ularni qayta ishlatadi. `ChannelHealthChecker.ACTIVE` orqali hovuzdan chiqarishdan oldin kanalning tirikligi tekshiriladi, bu esa 'broken pipe' xatolarini minimallashtiradi.

---

### Topshiriq #1110: SSL/TLS integratsiyasi: SslContextBuilder va OpenSSL (Netty-tcnative) ALPN bilan shifrlangan aloqa
**Tavsif:** Bank va xavfsiz to'lov tizimlarida barcha tarmoq kanallari TLS 1.3 bilan shifrlanishi shart. JVM standart JSSE mexanizmi sekinligi sababli, Netty-tcnative (OpenSSL) dvigatelidan foydalangan holda ALPN (Application-Layer Protocol Negotiation) bilan himoyalangan server yaratish talab etiladi.
**Talablar:** SslContextBuilder, OpenSSL provider tekshiruvi, ALPN orqali protokollar (h2, http/1.1) ro'yxatini e'lon qilish va SSL handshake xatolarini boshqarish.
**Yechim (Java):**
```java
package com.khorazmiy.network.ssl;

import io.netty.channel.ChannelInitializer;
import io.netty.channel.ChannelPipeline;
import io.netty.channel.socket.SocketChannel;
import io.netty.handler.ssl.*;
import io.netty.handler.ssl.ApplicationProtocolConfig.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.net.ssl.SSLException;
import java.io.File;

/**
 * OpenSSL va ALPN bilan ta'minlangan yuqori unumdor TLS shifrlash moduli.
 */
public class SecureTlsServerInitializer extends ChannelInitializer<SocketChannel> {
    private static final Logger log = LoggerFactory.getLogger(SecureTlsServerInitializer.class);

    private final SslContext sslCtx;

    public SecureTlsServerInitializer(File certChainFile, File keyFile) throws SSLException {
        // OpenSSL mavjudligini aniqlash (OpenSSL JSSE ga nisbatan 3-4 baravar tezroq)
        SslProvider provider = OpenSsl.isAvailable() ? SslProvider.OPENSSL : SslProvider.JDK;
        log.info("Tanlangan SSL Provayderi: {}", provider);

        this.sslCtx = SslContextBuilder.forServer(certChainFile, keyFile)
                .sslProvider(provider)
                .protocols("TLSv1.3", "TLSv1.2") // Zaif TLS versiyalar taqiqlangan
                .ciphers(null, IdentityCipherSuiteFilter.INSTANCE)
                .applicationProtocolConfig(new ApplicationProtocolConfig(
                        Protocol.ALPN,
                        SelectorFailureBehavior.NO_ADVERTISE,
                        SelectedListenerFailureBehavior.ACCEPT,
                        ApplicationProtocolNames.HTTP_2,
                        ApplicationProtocolNames.HTTP_1_1
                ))
                .build();
    }

    @Override
    protected void initChannel(SocketChannel ch) {
        ChannelPipeline p = ch.pipeline();

        // SslHandler eng birinchi bo'lib qo'yilishi shart
        p.addFirst("sslHandler", sslCtx.newHandler(ch.alloc()));

        // Qo'shimcha biznes handlerlar
        p.addLast(new SimpleChannelInboundHandler<Object>() {
            @Override
            public void userEventTriggered(ChannelHandlerContext ctx, Object evt) {
                if (evt instanceof SslHandshakeCompletionEvent) {
                    SslHandshakeCompletionEvent handshake = (SslHandshakeCompletionEvent) evt;
                    if (handshake.isSuccess()) {
                        log.info("TLS Handshake muvaffaqiyatli yakunlandi! Mijoz: {}", ctx.channel().remoteAddress());
                    } else {
                        log.error("TLS Handshake xatosi: {}", handshake.cause().getMessage());
                        ctx.close();
                    }
                }
            }

            @Override
            protected void channelRead0(ChannelHandlerContext ctx, Object msg) {
                // Shifrdan yechilgan ma'lumotlar bilan ishlash
            }
        });
    }
}
```
**Tushuntirish:** OpenSSL (Netty-tcnative) CPU ning AES-NI yo'riqnomalaridan to'g'ridan-to'g'ri foydalanadi va xotira allokatsiyalarini sezilarli kamaytiradi. ALPN (Application-Layer Protocol Negotiation) TLS handshake jarayonining o'zidayoq mijoz va server o'rtasida qaysi protokol (masalan HTTP/2 yoki HTTP/1.1) ishlatilishini kelishib oladi, bu esa qo'shimcha tarmoq RTT chaqiruvlarisiz o'tish imkonini beradi.

---

### Topshiriq #1111: Netty WebSocket Server: WebSocketServerProtocolHandler va Frame Turlari Bilan Ishlash
**Tavsif:** Real-time birja savdo tizimida mijozlar bilan doimiy ikki tomonlama tezkor aloqa o'rnatish uchun Netty da to'liq xususiyatli WebSocket serverini qurish talab etiladi.
**Talablar:** HttpServerCodec, HttpObjectAggregator, WebSocketServerProtocolHandler, TextWebSocketFrame, BinaryWebSocketFrame, PingWebSocketFrame, CloseWebSocketFrame larni to'g'ri qayta ishlash.
**Yechim (Java):**
```java
package com.khorazmiy.network.websocket;

import io.netty.bootstrap.ServerBootstrap;
import io.netty.channel.*;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.SocketChannel;
import io.netty.channel.socket.nio.NioServerSocketChannel;
import io.netty.handler.codec.http.*;
import io.netty.handler.codec.http.websocketx.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Netty da to'liq WebSocket freymlarini qayta ishlovchi server.
 */
public class WebSocketServerEngine {
    private static final Logger log = LoggerFactory.getLogger(WebSocketServerEngine.class);
    private static final String WEBSOCKET_PATH = "/ws/ticker";

    public static class WebSocketFrameHandler extends SimpleChannelInboundHandler<WebSocketFrame> {
        @Override
        protected void channelRead0(ChannelHandlerContext ctx, WebSocketFrame frame) {
            // Freym turlari bo'yicha saralash
            if (frame instanceof TextWebSocketFrame) {
                String request = ((TextWebSocketFrame) frame).text();
                log.info("Matnli WebSocket xabar olindi: {}", request);
                // Matnli javob yuborish
                ctx.channel().writeAndFlush(new TextWebSocketFrame("Echo: " + request));
            } else if (frame instanceof BinaryWebSocketFrame) {
                log.info("Binar freym qabul qilindi, baytlar soni: {}", frame.content().readableBytes());
                // Binar ma'lumotni aks-sado qilish (retain qilish shart)
                ctx.channel().writeAndFlush(frame.retain());
            } else if (frame instanceof PingWebSocketFrame) {
                log.debug("PING olindi, PONG qaytarilmoqda");
                ctx.channel().writeAndFlush(new PongWebSocketFrame(frame.content().retain()));
            } else if (frame instanceof CloseWebSocketFrame) {
                log.info("Mijoz ulanishni yopish freymini yubordi");
                ctx.channel().close();
            } else {
                throw new UnsupportedOperationException("Qo'llab-quvvatlanmaydigan freym: " + frame.getClass().getName());
            }
        }

        @Override
        public void userEventTriggered(ChannelHandlerContext ctx, Object evt) throws Exception {
            if (evt instanceof WebSocketServerProtocolHandler.HandshakeComplete) {
                WebSocketServerProtocolHandler.HandshakeComplete handshake = 
                        (WebSocketServerProtocolHandler.HandshakeComplete) evt;
                log.info("WebSocket Handshake yakunlandi! URI: {}, Mijoz: {}", 
                         handshake.requestUri(), ctx.channel().remoteAddress());
            } else {
                super.userEventTriggered(ctx, evt);
            }
        }
    }

    public void start(int port) throws InterruptedException {
        EventLoopGroup bossGroup = new NioEventLoopGroup(1);
        EventLoopGroup workerGroup = new NioEventLoopGroup();

        try {
            ServerBootstrap b = new ServerBootstrap();
            b.group(bossGroup, workerGroup)
             .channel(NioServerSocketChannel.class)
             .childHandler(new ChannelInitializer<SocketChannel>() {
                 @Override
                 protected void initChannel(SocketChannel ch) {
                     ChannelPipeline pipeline = ch.pipeline();
                     // HTTP so'rovlarni parslash
                     pipeline.addLast(new HttpServerCodec());
                     // To'liq HTTP so'rovni 64KB hajmda bitta FullHttpRequest ga yig'ish
                     pipeline.addLast(new HttpObjectAggregator(65536));
                     // WebSocket handshake va avtomatik Ping-Pong boshqaruvi
                     pipeline.addLast(new WebSocketServerProtocolHandler(WEBSOCKET_PATH, null, true));
                     // Biznes WebSocket freym handleri
                     pipeline.addLast(new WebSocketFrameHandler());
                 }
             });

            Channel ch = b.bind(port).sync().channel();
            log.info("WebSocket server ishga tushdi: ws://127.0.0.1:{}{}", port, WEBSOCKET_PATH);
            ch.closeFuture().sync();
        } finally {
            bossGroup.shutdownGracefully();
            workerGroup.shutdownGracefully();
        }
    }
}
```
**Tushuntirish:** Netty dagi `WebSocketServerProtocolHandler` HTTP GET so'rovini qabul qilib, WebSocket Upgrade sarlavhalarini tekshiradi va handshake-ni to'liq o'zi avtomatlashtiradi. `HttpObjectAggregator` orqali HTTP sarlavhalar va tana birlashtiriladi. Handshake yakunlangach, pipeline-dan HTTP codec-lar olib tashlanib, soket past kechikishli WebSocket freymlarini qabul qilish rejimiga o'tadi.

---

### Topshiriq #1112: WebSocket Broadcast va ChannelGroup: 100,000+ Bir Vaqtda Ulangan Foydalanuvchilarga Xabarlarni Tarqatish
**Tavsif:** Katta hajmdagi jonli efir yoki kriptovalyuta kursi o'zgarishini bir vaqtning o'zida yuz minglab ulangan mijozlarga bir zumda (broadcast) tarqatish talab etiladi. Noto'g'ri iteratsiya CPU qulflanishiga olib keladi.
**Talablar:** DefaultChannelGroup, GlobalEventExecutor, zero-copy broadcast, ulanishlarni avtomatik ro'yxatdan chiqarish va parallel tarqatish.
**Yechim (Java):**
```java
package com.khorazmiy.network.broadcast;

import io.netty.channel.*;
import io.netty.channel.group.ChannelGroup;
import io.netty.channel.group.ChannelGroupFuture;
import io.netty.channel.group.DefaultChannelGroup;
import io.netty.handler.codec.http.websocketx.TextWebSocketFrame;
import io.netty.util.concurrent.GlobalEventExecutor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.concurrent.atomic.AtomicLong;

/**
 * 100,000+ mijozlarga xabarlarni parallel tarqatuvchi yuqori unumdor WebSocket Broadcast markazi.
 */
public class WebSocketBroadcastHub {
    private static final Logger log = LoggerFactory.getLogger(WebSocketBroadcastHub.class);

    // Thread-safe kanallar guruhi. Kanal yopilganda guruhdan avtomatik o'chiriladi
    private final ChannelGroup activeChannels = 
            new DefaultChannelGroup("ActiveWebSockets", GlobalEventExecutor.INSTANCE);

    private final AtomicLong messageCounter = new AtomicLong(0);

    // Yangi ulanish ulanganda guruhga qo'shish
    public void registerChannel(Channel channel) {
        activeChannels.add(channel);
        log.info("Yangi kanal qo'shildi: {}. Jami faol mijozlar: {}", channel.id(), activeChannels.size());
    }

    /**
     * Barcha ulangan mijozlarga xabarni tarqatish (Zero-Copy Broadcast).
     * Bitta TextWebSocketFrame yaratilib barcha kanallarga retain() orqali uzatiladi.
     */
    public void broadcastMarketPrice(String symbol, double price) {
        if (activeChannels.isEmpty()) {
            return;
        }

        long msgId = messageCounter.incrementAndGet();
        String jsonPayload = String.format("{\"id\":%d,\"symbol\":\"%s\",\"price\":%.4f}", 
                                           msgId, symbol, price);

        // Barcha kanallarga parallel jo'natish
        // writeAndFlush ichkarida barcha kanallarning EventLoop oqimlariga vazifa topshiradi
        ChannelGroupFuture future = activeChannels.writeAndFlush(new TextWebSocketFrame(jsonPayload));

        future.addListener(f -> {
            if (f.isSuccess()) {
                log.debug("Narx yangilanishi barcha {} ta mijozga yetkazildi", activeChannels.size());
            } else {
                log.warn("Ba'zi kanallarga xabar yetib bormadi");
            }
        });
    }

    public int getActiveCount() {
        return activeChannels.size();
    }
}
```
**Tushuntirish:** `DefaultChannelGroup` barcha faol kanallarni `ConcurrentMap` da saqlaydi va har bir kanal yopilganda (`channelInactive`) `ChannelFutureListener` orqali uni o'z-o'zidan guruhdan o'chiradi. Guruhga `writeAndFlush` chaqirilganda, Netty har bir kanalning o'z `EventLoop` oqimiga xabarni navbatga qo'yadi. Natijada xabarni tarqatish bitta oqimda tiqilib qolmaydi va ko'p yadroli protsessordan maksimal foydalanadi.

---

### Topshiriq #1113: Binary WebSocket Protocol: Protobuf Serializatsiyalangan Freymlarni Qayta Ishlash
**Tavsif:** JSON formati matnli bo'lib, yuqori chastotali treydingda ortiqcha baytlar va parsing overhead keltirib chiqaradi. Google Protobuf binar formatini WebSocket BinaryFrame orqali uzatish va dekodlash tizimini qurish zarur.
**Talablar:** BinaryWebSocketFrame dan baytlarni to'g'ridan-to'g'ri InputStream ga nusxalamasdan o'qish, Protobuf parser bilan integratsiya va xotira boshqaruvi.
**Yechim (Java):**
```java
package com.khorazmiy.network.binaryws;

import io.netty.buffer.ByteBuf;
import io.netty.buffer.ByteBufInputStream;
import io.netty.buffer.ByteBufOutputStream;
import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.SimpleChannelInboundHandler;
import io.netty.handler.codec.http.websocketx.BinaryWebSocketFrame;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.InputStream;

/**
 * Protobuf binar freymlari bilan ishlovchi WebSocket handleri.
 */
public class ProtobufWebSocketHandler extends SimpleChannelInboundHandler<BinaryWebSocketFrame> {
    private static final Logger log = LoggerFactory.getLogger(ProtobufWebSocketHandler.class);

    // Protobuf xabarini ifodalovchi model namunasi
    public record TradeOrder(long orderId, String symbol, double quantity, double price) {}

    @Override
    protected void channelRead0(ChannelHandlerContext ctx, BinaryWebSocketFrame frame) throws Exception {
        ByteBuf content = frame.content();

        // 1. Zero-Copy: Netty ByteBuf dan to'g'ridan-to'g'ri InputStream orqali o'qish
        try (InputStream in = new ByteBufInputStream(content)) {
            // Haqiqiy loyihada TradeOrderProto.parseFrom(in) chaqiriladi
            long orderId = content.readLong();
            int symbolLen = content.readInt();
            byte[] symBytes = new byte[symbolLen];
            content.readBytes(symBytes);
            String symbol = new String(symBytes);
            double qty = content.readDouble();
            double price = content.readDouble();

            TradeOrder order = new TradeOrder(orderId, symbol, qty, price);
            log.info("Protobuf order qabul qilindi: ID={}, {} {} @ {}", 
                     order.orderId(), order.quantity(), order.symbol(), order.price());

            // Javob binar freymini yaratish
            ByteBuf responseBuf = ctx.alloc().buffer();
            responseBuf.writeLong(order.orderId());
            responseBuf.writeInt(200); // Status OK

            ctx.writeAndFlush(new BinaryWebSocketFrame(responseBuf));
        }
    }

    @Override
    public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) {
        log.error("Binar protokolda xatolik: ", cause);
        ctx.close();
    }
}
```
**Tushuntirish:** Binar protokollar JSON ga nisbatan 60-80% gacha kamroq tarmoq trafigini talab qiladi va CPU tomonidan satrlarni qidirish (string parsing) yukini bartaraf etadi. `ByteBufInputStream` Netty ning direct buferlari ustida qo'shimcha byte[] massivini Heap ga ajratmasdan oqim yaratadi, bu esa GC to'xtashlarini oldini oladi.

---

### Topshiriq #1114: WebSocket Auth & Handshake Interceptor: Token Validatsiyasi va Xavfsizlik Tekshiruvi
**Tavsif:** WebSocket protokoli brauzerlardan odatiy Authorization headerlarini uzatishda cheklovlarga ega. Handshake bosqichida Query parametr yoki maxsus sarlavhalardan JWT tokenni tekshirib, yaroqsiz ulanishlarni soket darajasida rad etish talab etiladi.
**Talablar:** FullHttpRequest ni ushlash, QueryStringDecoder orqali token ajratish, 401 Unauthorized qaytarish va xavfsiz ulanishlarni ChannelPipeline ga o'tkazish.
**Yechim (Java):**
```java
package com.khorazmiy.network.auth;

import io.netty.channel.*;
import io.netty.handler.codec.http.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.nio.charset.StandardCharsets;
import java.util.List;

import static io.netty.handler.codec.http.HttpResponseStatus.UNAUTHORIZED;
import static io.netty.handler.codec.http.HttpVersion.HTTP_1_1;

/**
 * WebSocket handshake bosqichida JWT tokenni tekshiruvchi xavfsizlik filtri.
 */
public class WebSocketAuthHandler extends ChannelInboundHandlerAdapter {
    private static final Logger log = LoggerFactory.getLogger(WebSocketAuthHandler.class);

    @Override
    public void channelRead(ChannelHandlerContext ctx, Object msg) throws Exception {
        if (msg instanceof FullHttpRequest) {
            FullHttpRequest request = (FullHttpRequest) msg;

            // Agar so'rov WebSocket upgrade so'rovi bo'lsa
            if (request.headers().contains(HttpHeaderNames.UPGRADE, HttpHeaderValues.WEBSOCKET, true)) {
                String uri = request.uri();
                QueryStringDecoder decoder = new QueryStringDecoder(uri);
                List<String> tokens = decoder.parameters().get("token");

                if (tokens == null || tokens.isEmpty() || !isValidToken(tokens.get(0))) {
                    log.warn("WebSocket ulanishi rad etildi (Token yaroqsiz): {}", ctx.channel().remoteAddress());
                    sendUnauthorizedResponse(ctx);
                    request.release(); // Xotirani tozalash
                    return;
                }

                // Autentifikatsiya muvaffaqiyatli: foydalanuvchi ma'lumotlarini kanal atributiga saqlash
                String validUser = extractUsername(tokens.get(0));
                ctx.channel().attr(io.netty.util.AttributeKey.valueOf("USER_ID")).set(validUser);
                log.info("Foydalanuvchi tasdiqlandi: {} [{}]", validUser, ctx.channel().remoteAddress());

                // Keyingi WebSocket protokoli handlerlariga o'tkazish
                ctx.pipeline().remove(this); // Auth muvaffaqiyatli o'tgach o'zini pipeline dan o'chiradi
            }
        }
        super.channelRead(ctx, msg);
    }

    private boolean isValidToken(String token) {
        // Haqiqiy JWT imzo tekshiruv simulyatsiyasi
        return token != null && token.startsWith("jwt_valid_secret_");
    }

    private String extractUsername(String token) {
        return "user_" + token.substring(17);
    }

    private void sendUnauthorizedResponse(ChannelHandlerContext ctx) {
        FullHttpResponse res = new DefaultFullHttpResponse(HTTP_1_1, UNAUTHORIZED);
        res.content().writeBytes("401 Unauthorized: Noto'g'ri token\n".getBytes(StandardCharsets.UTF_8));
        HttpUtil.setContentLength(res, res.content().readableBytes());
        ctx.writeAndFlush(res).addListener(ChannelFutureListener.CLOSE);
    }
}
```
**Tushuntirish:** WebSocket aloqasi HTTP GET so'rovidan boshlanadi. Agar ruxsat etilmagan ulanish shu bosqichda to'xtatilmasa, WebSocket freymlari uchun keraksiz xotira ajratiladi. Handshake tekshiruvidan so'ng `ctx.pipeline().remove(this)` orqali autentifikatsiya handleri quvurdan olib tashlanadi, natijada keyingi har bir xabar uchun keraksiz tekshiruvlar bajarilmaydi.

---

### Topshiriq #1115: WebSocket Rate Limiter va DoS Himoyasi: Token Bucket Algoritmi
**Tavsif:** Zararli mijozlar yoki nosoz skriptlar soniyasiga minglab freym yuborib server protsessorini band qilishi mumkin. Har bir soket ulanishi uchun shaxsiy Token Bucket tezlik cheklovchisini joriy qilish talab etiladi.
**Talablar:** Har bir kanalga moslashtirilgan Token Bucket, soniyalik limitlar, chegaradan oshganda freymlarni tashlab yuborish yoki ogohlantirish berish.
**Yechim (Java):**
```java
package com.khorazmiy.network.ratelimit;

import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.SimpleChannelInboundHandler;
import io.netty.handler.codec.http.websocketx.TextWebSocketFrame;
import io.netty.handler.codec.http.websocketx.WebSocketFrame;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Har bir ulanish uchun alohida Token-Bucket algoritmi asosidagi Rate Limiter.
 */
public class WebSocketRateLimitHandler extends SimpleChannelInboundHandler<WebSocketFrame> {
    private static final Logger log = LoggerFactory.getLogger(WebSocketRateLimitHandler.class);

    private final long capacity;      // Paqirning maksimal sig'imi
    private final double refillRate;  // Har millisekundda qo'shiladigan tokenlar soni
    private double currentTokens;
    private long lastRefillTime;

    public WebSocketRateLimitHandler(long maxBurst, double tokensPerSecond) {
        this.capacity = maxBurst;
        this.refillRate = tokensPerSecond / 1000.0;
        this.currentTokens = maxBurst;
        this.lastRefillTime = System.currentTimeMillis();
    }

    private synchronized boolean tryConsumeToken() {
        long now = System.currentTimeMillis();
        long elapsed = now - lastRefillTime;
        lastRefillTime = now;

        // O'tgan vaqtga mutanosib yangi tokenlarni to'ldirish
        currentTokens = Math.min(capacity, currentTokens + (elapsed * refillRate));

        if (currentTokens >= 1.0) {
            currentTokens -= 1.0;
            return true;
        }
        return false;
    }

    @Override
    protected void channelRead0(ChannelHandlerContext ctx, WebSocketFrame frame) {
        if (tryConsumeToken()) {
            // Limit me'yorida: freymni keyingi biznes handlerga uzatamiz
            ctx.fireChannelRead(frame.retain());
        } else {
            // Limitdan oshib ketdi!
            log.warn("Rate limit oshib ketdi! Mijoz: {}", ctx.channel().remoteAddress());
            ctx.writeAndFlush(new TextWebSocketFrame("{\"error\":\"Too Many Requests. Sekinroq yuboring!\"}"));
            // Juda tajovuzkor bo'lsa ctx.close() qilish mumkin
        }
    }
}
```
**Tushuntirish:** Token Bucket algoritmi qisqa muddatli chaqnashlarga (bursts) ruxsat beradi, lekin uzoq muddatli o'rtacha tezlikni qat'iy nazorat qiladi. Har bir kanal ulanishi o'z xotirasida kichik o'lchamdagi TokenBucket saqlashi orqali global qulflanishlar (thread contention) bo'lmaydi va xizmat DoS hujumlaridan ishonchli saqlanadi.

---

### Topshiriq #1116: WebSocket Compression: PerMessageDeflateServerExtensionHandshaker Bilan Tarmoq Trafigini Siqish
**Tavsif:** WebSocket orqali katta hajmdagi matnli JSON yoki XML ma'lumotlar uzatilganda tarmoq o'tkazuvchanligi to'lib qoladi. RFC 7692 standartidagi 'permessage-deflate' siqish kengaytmasini joriy etish talab etiladi.
**Talablar:** WebSocketServerCompressionHandler, PerMessageDeflateServerExtensionHandshaker konfiguratsiyasi, mijoz va server o'rtasida siqish darajasini kelishish.
**Yechim (Java):**
```java
package com.khorazmiy.network.compression;

import io.netty.channel.ChannelInitializer;
import io.netty.channel.ChannelPipeline;
import io.netty.channel.socket.SocketChannel;
import io.netty.handler.codec.http.HttpObjectAggregator;
import io.netty.handler.codec.http.HttpServerCodec;
import io.netty.handler.codec.http.websocketx.WebSocketServerProtocolHandler;
import io.netty.handler.codec.http.websocketx.extensions.compression.WebSocketServerCompressionHandler;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * WebSocket 'permessage-deflate' siqish imkoniyatini ta'minlovchi pipeline initsializatori.
 */
public class CompressedWebSocketInitializer extends ChannelInitializer<SocketChannel> {
    private static final Logger log = LoggerFactory.getLogger(CompressedWebSocketInitializer.class);

    @Override
    protected void initChannel(SocketChannel ch) {
        ChannelPipeline pipeline = ch.pipeline();

        pipeline.addLast("httpCodec", new HttpServerCodec());
        pipeline.addLast("aggregator", new HttpObjectAggregator(65536));

        // WebSocket trafigini avtomatik zlib/deflate bilan siquvchi va yozuvchi handler
        pipeline.addLast("compressionHandler", new WebSocketServerCompressionHandler());

        // WebSocket protokoli handleri
        pipeline.addLast("wsProtocol", new WebSocketServerProtocolHandler("/ws/data", null, true));

        log.info("WebSocket kanali siqish (permessage-deflate) bilan ta'minlandi: {}", ch.remoteAddress());
    }
}
```
**Tushuntirish:** `WebSocketServerCompressionHandler` RFC 7692 protokoliga asosan mijozning `Sec-WebSocket-Extensions: permessage-deflate` sarlavhasini o'qiydi. Agar mijoz siqishni qo'llab-quvvatlasa, har bir `TextWebSocketFrame` jo'natilishdan oldin CPU Deflater orqali qisqartiriladi, bu esa matnli ma'lumotlar hajmini 70-85% gacha kamaytiradi.

---

### Topshiriq #1117: Netty WebSocket Client: Reconnect Handler va Exponential Backoff Bilan Avtomatik Tiklanish
**Tavsif:** Tashqi birjalar (Binance, Bybit) yoki mikroxizmatlarga ulanuvchi mijoz soketlar tarmoq nosozliklari paytida avtomatik qayta ulanishi (reconnect) va serverni so'rovlar bilan 'cho'ktirib' qo'ymaslik uchun eksponentsial kutish vaqtiga ega bo'lishi kerak.
**Talablar:** WebSocketClientProtocolHandler, ChannelInboundHandlerAdapter da channelInactive hodisasini tutish, HashedWheelTimer yoki EventLoop schedule orqali eksponentsial qayta ulanish.
**Yechim (Java):**
```java
package com.khorazmiy.network.client;

import io.netty.bootstrap.Bootstrap;
import io.netty.channel.*;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.SocketChannel;
import io.netty.channel.socket.nio.NioSocketChannel;
import io.netty.handler.codec.http.*;
import io.netty.handler.codec.http.websocketx.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.net.URI;
import java.util.concurrent.TimeUnit;

/**
 * Eksponentsial oraliq bilan uzilgan ulanishni qayta tiklovchi Netty WebSocket mijozi.
 */
public class ResilientWebSocketClient {
    private static final Logger log = LoggerFactory.getLogger(ResilientWebSocketClient.class);

    private final URI uri;
    private final EventLoopGroup group = new NioEventLoopGroup();
    private Bootstrap bootstrap;
    private int retryAttempts = 0;
    private static final int MAX_RETRY_DELAY_SEC = 60;

    public ResilientWebSocketClient(URI uri) {
        this.uri = uri;
    }

    public void start() {
        bootstrap = new Bootstrap();
        bootstrap.group(group)
                 .channel(NioSocketChannel.class)
                 .handler(new ChannelInitializer<SocketChannel>() {
                     @Override
                     protected void initChannel(SocketChannel ch) {
                         ChannelPipeline p = ch.pipeline();
                         p.addLast(new HttpClientCodec());
                         p.addLast(new HttpObjectAggregator(65536));
                         
                         WebSocketClientHandshaker handshaker = WebSocketClientHandshakerFactory.newHandshaker(
                                 uri, WebSocketVersion.V13, null, true, new DefaultHttpHeaders());
                         
                         p.addLast(new WebSocketClientProtocolHandler(handshaker));
                         p.addLast(new ClientConnectionManager());
                     }
                 });

        doConnect();
    }

    private void doConnect() {
        log.info("Ulanish amalga oshirilmoqda -> {}", uri);
        bootstrap.connect(uri.getHost(), uri.getPort() > 0 ? uri.getPort() : 80).addListener((ChannelFuture f) -> {
            if (!f.isSuccess()) {
                log.error("Ulanish amalga oshmadi: {}", f.cause().getMessage());
                scheduleReconnect();
            }
        });
    }

    private void scheduleReconnect() {
        retryAttempts++;
        // Eksponentsial kutish: 2^n soniya (maksimal 60 soniya)
        long delay = Math.min((long) Math.pow(2, retryAttempts), MAX_RETRY_DELAY_SEC);
        log.warn("{} soniyadan so'ng qayta ulanishga urinish (#{})", delay, retryAttempts);

        group.schedule(this::doConnect, delay, TimeUnit.SECONDS);
    }

    private class ClientConnectionManager extends SimpleChannelInboundHandler<Object> {
        @Override
        public void channelActive(ChannelHandlerContext ctx) {
            log.info("Tarmoq ulanishi o'rnatildi, Handshake kutilmoqda...");
        }

        @Override
        public void userEventTriggered(ChannelHandlerContext ctx, Object evt) {
            if (evt == WebSocketClientProtocolHandler.ClientHandshakeStateEvent.HANDSHAKE_COMPLETE) {
                log.info("WebSocket Handshake to'liq muvaffaqiyatli! Savdo oqimi boshlandi.");
                retryAttempts = 0; // Urinishlar hisoblagichini qayta tiklash
            }
        }

        @Override
        protected void channelRead0(ChannelHandlerContext ctx, Object msg) {
            if (msg instanceof TextWebSocketFrame) {
                log.info("Birja javobi: {}", ((TextWebSocketFrame) msg).text());
            }
        }

        @Override
        public void channelInactive(ChannelHandlerContext ctx) {
            log.warn("Soket ulanishi uzildi!");
            scheduleReconnect();
        }
    }
}
```
**Tushuntirish:** Eksponentsial orqaga chekinish (Exponential Backoff) algoritmi server qulaganida minglab mijozlarning bir paytda ulanib tizimni battar yiqitishining (Thundering Herd muammosi) oldini oladi. `group.schedule()` yordamida alohida timer oqimi yaratmasdan mavjud Netty EventLoop ning o'zida rejalashtirish amalga oshiriladi.

---

### Topshiriq #1118: WebSocket Subprotocols: Maxsus RPC va STOMP Subprotokollarini Marshrutlash
**Tavsif:** WebSocket bitta kanal orqali bir nechta mustaqil xizmatlarni (masalan chat, bildirishnomalar, tranzaksiyalar) boshqarishi kerak. 'Sec-WebSocket-Protocol' sarlavhasi orqali subprotokolni tanlash va marshrutlash tizimini qurish zarur.
**Talablar:** Subprotocol handshake kelishuvi, kelayotgan xabarlarni subprotokol bo'yicha turli handlerlarga yo'naltirish.
**Yechim (Java):**
```java
package com.khorazmiy.network.subprotocol;

import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.SimpleChannelInboundHandler;
import io.netty.handler.codec.http.websocketx.TextWebSocketFrame;
import io.netty.handler.codec.http.websocketx.WebSocketServerProtocolConfig;
import io.netty.handler.codec.http.websocketx.WebSocketServerProtocolHandler;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * WebSocket subprotokollari (STOMP, JSON-RPC) ni marshrutlovchi tizim.
 */
public class SubprotocolRouterHandler extends SimpleChannelInboundHandler<TextWebSocketFrame> {
    private static final Logger log = LoggerFactory.getLogger(SubprotocolRouterHandler.class);

    public static WebSocketServerProtocolHandler createProtocolHandler() {
        // Qo'llab-quvvatlanadigan subprotokollar ro'yxati
        String subprotocols = "v10.stomp,jsonrpc-2.0";
        WebSocketServerProtocolConfig config = WebSocketServerProtocolConfig.newBuilder()
                .websocketPath("/ws")
                .subprotocols(subprotocols)
                .checkStartsWith(true)
                .build();
        return new WebSocketServerProtocolHandler(config);
    }

    @Override
    protected void channelRead0(ChannelHandlerContext ctx, TextWebSocketFrame msg) {
        String content = msg.text();

        // Qaysi subprotokol kelishilganini tekshirish
        if (content.startsWith("CONNECT") || content.startsWith("SUBSCRIBE")) {
            handleStompFrame(ctx, content);
        } else if (content.contains("\"jsonrpc\":")) {
            handleJsonRpcFrame(ctx, content);
        } else {
            log.warn("Noma'lum subprotokol xabari: {}", content);
            ctx.writeAndFlush(new TextWebSocketFrame("ERROR: Protokol tushunarsiz\n"));
        }
    }

    private void handleStompFrame(ChannelHandlerContext ctx, String frame) {
        log.info("STOMP freymi qayta ishlanmoqda: {}", frame.lines().findFirst().orElse(""));
        ctx.writeAndFlush(new TextWebSocketFrame("CONNECTED\nversion:1.2\n\n\u0000"));
    }

    private void handleJsonRpcFrame(ChannelHandlerContext ctx, String json) {
        log.info("JSON-RPC freymi qabul qilindi: {}", json);
        ctx.writeAndFlush(new TextWebSocketFrame("{\"jsonrpc\":\"2.0\",\"result\":\"success\",\"id\":1}"));
    }
}
```
**Tushuntirish:** Subprotokollar bitta umumiy TCP/WebSocket ulanish ustida turli xil dasturiy qatlamlarni kelishib olishga imkon beradi. `WebSocketServerProtocolConfig.newBuilder().subprotocols(...)` orqali mijoz taklif qilgan subprotokollardan serverga mos kelgani tanlab olinadi va handshake javobida `Sec-WebSocket-Protocol` sarlavhasi bilan tasdiqlanadi.

---

### Topshiriq #1119: WebSocket Stateful Session Management: Redis Pub/Sub Bilan Klasterlashgan Server
**Tavsif:** Gorizontal kengaytirilgan (multi-instance) arxitekturada bir foydalanuvchi 1-serverga, uning do'sti esa 2-serverga ulangan bo'lishi mumkin. Xabarlarni barcha instanslar bo'ylab sinxronlash uchun Redis Pub/Sub va Netty integratsiyasini qurish zarur.
**Talablar:** Lokal Netty ChannelRegistry, Redis subscriber orqali global xabarlarni qabul qilish va faqat mos keluvchi lokal soketga yetkazish.
**Yechim (Java):**
```java
package com.khorazmiy.network.cluster;

import io.netty.channel.Channel;
import io.netty.handler.codec.http.websocketx.TextWebSocketFrame;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.concurrent.ConcurrentHashMap;

/**
 * Ko'p serverli klasterda WebSocket sessiyalarini Redis Pub/Sub orqali boshqarish.
 */
public class DistributedWebSocketClusterManager {
    private static final Logger log = LoggerFactory.getLogger(DistributedWebSocketClusterManager.class);

    // Ushbu tugunga (Node) bevosita ulangan mijozlar ro'yxati
    private final ConcurrentHashMap<String, Channel> localSessions = new ConcurrentHashMap<>();

    public void registerSession(String userId, Channel channel) {
        localSessions.put(userId, channel);
        log.info("Foydalanuvchi ushbu tugunga biriktirildi: UserID={}", userId);
    }

    public void unregisterSession(String userId) {
        localSessions.remove(userId);
        log.info("Foydalanuvchi chiqib ketdi: UserID={}", userId);
    }

    // Redis Pub/Sub dan kelgan umumiy tarmoq xabari
    public void onRedisMessageReceived(String targetUserId, String messagePayload) {
        Channel channel = localSessions.get(targetUserId);
        if (channel != null && channel.isActive()) {
            // Maqsadli foydalanuvchi ayni shu server instansiga ulangan!
            log.info("Lokal mijoz topildi. Xabar WebSocket ga yuborilmoqda: {}", targetUserId);
            channel.writeAndFlush(new TextWebSocketFrame(messagePayload));
        } else {
            // Foydalanuvchi boshqa tugunda yoki oflayn
            log.debug("Mijoz ushbu instansda emas, e'tiborsiz qoldirildi: {}", targetUserId);
        }
    }
}
```
**Tushuntirish:** Klasterlangan WebSocket arxitekturasida mijozlar holati (state) turli tugunlarga tarqalgan bo'ladi. Redis Pub/Sub barcha tugunlarga xabarni broadcast qiladi, lekin faqat kerakli foydalanuvchining ochiq soketi joylashgan tugun xabarni WebSocket ga chiqaradi. Bu orqali xizmat gorizontal ravishda o'nlab serverlarga erkin miqyoslanadi.

---

### Topshiriq #1120: WebSocket Graceful Shutdown: Faol Ulanishlarni Xavfsiz Yopish va ChannelGroupFuture Monitoringi
**Tavsif:** Server yangilanganda (rolling deployment) ochiq turgan minglab WebSocket ulanishlarini qo'pol ravishda uzib yuborish ma'lumotlar yo'qolishiga va mijoz dasturlari ishdan chiqishiga olib keladi. Barcha mijozlarga CloseWebSocketFrame jo'natib, xavfsiz to'xtatish zarur.
**Talablar:** CloseWebSocketFrame (1001 Going Away kodi bilan), ChannelGroupFuture orqali barcha kanallar yopilishini kutish va timeout bilan majburiy tugatish.
**Yechim (Java):**
```java
package com.khorazmiy.network.shutdown;

import io.netty.channel.group.ChannelGroup;
import io.netty.channel.group.ChannelGroupFuture;
import io.netty.channel.group.DefaultChannelGroup;
import io.netty.handler.codec.http.websocketx.CloseWebSocketFrame;
import io.netty.handler.codec.http.websocketx.WebSocketCloseStatus;
import io.netty.util.concurrent.GlobalEventExecutor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.concurrent.TimeUnit;

/**
 * WebSocket serverini xavfsiz to'xtatish (Graceful Shutdown) menejeri.
 */
public class GracefulWebSocketShutdownManager {
    private static final Logger log = LoggerFactory.getLogger(GracefulWebSocketShutdownManager.class);

    private final ChannelGroup allChannels = new DefaultChannelGroup(GlobalEventExecutor.INSTANCE);

    public void addChannel(io.netty.channel.Channel ch) {
        allChannels.add(ch);
    }

    public void initiateGracefulShutdown(long timeoutSeconds) {
        log.info("Graceful Shutdown boshlandi. Faol ulanishlar soni: {}", allChannels.size());

        // 1. Barcha mijozlarga server yangilanayotgani haqida rasmiy Close Frame yuborish
        // Status 1001: GOING_AWAY
        CloseWebSocketFrame closeFrame = new CloseWebSocketFrame(
                WebSocketCloseStatus.ENDPOINT_UNAVAILABLE.code(), 
                "Server texnik xizmat ko'rsatish uchun to'xtatilmoqda");

        ChannelGroupFuture writeFuture = allChannels.writeAndFlush(closeFrame);

        writeFuture.addListener(f -> {
            log.info("Barcha mijozlarga Close Frame yetkazildi. Kanallarni yopish boshlanmoqda...");
            
            // 2. Kanallarni rasman yopish
            ChannelGroupFuture closeFuture = allChannels.close();
            
            closeFuture.addListener(cf -> {
                log.info("Barcha WebSocket kanallari xavfsiz yopildi! Tizim tozalandi.");
            });
        });

        // 3. Belgilangan vaqt ichida yopilmasa majburiy to'xtatish
        try {
            if (!allChannels.newCloseFuture().await(timeoutSeconds, TimeUnit.SECONDS)) {
                log.warn("Ba'zi kanallar belgilangan vaqtda yopilmadi, majburiy to'xtatilmoqda.");
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
```
**Tushuntirish:** Graceful shutdown jarayonida mijozlarga `ENDPOINT_UNAVAILABLE (1001)` kodi jo'natilganda, frontend ilovalari buni normal deb qabul qiladi va darhol boshqa zaxira serverga ulanishga harakat qiladi. Bu esa xizmat uzilishlarini (downtime) nolga tushiradi.

---

### Topshiriq #1121: Netty HTTP/2 Server: Multiplexing, Http2FrameCodec va Http2StreamFrameToHttpObjectCodec
**Tavsif:** HTTP/1.1 da har bir parallel so'rov uchun alohida TCP ulanish kerak bo'lardi. Netty HTTP/2 freymlari yordamida bitta TCP soket ustida o'nlab mustaqil oqimlarni (Streams) parallel multipleksatsiya qiluvchi server qurish talab etiladi.
**Talablar:** Http2FrameCodecBuilder, Http2MultiplexHandler, Stream ID boshqaruvi, Http2HeadersFrame va Http2DataFrame larni to'g'ri qayta ishlash.
**Yechim (Java):**
```java
package com.khorazmiy.network.http2;

import io.netty.buffer.Unpooled;
import io.netty.channel.*;
import io.netty.handler.codec.http.*;
import io.netty.handler.codec.http2.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.nio.charset.StandardCharsets;

/**
 * Netty HTTP/2 Multiplexing arxitekturasi va stream boshqaruvi.
 */
public class Http2ServerHandlerInitializer extends ChannelInitializer<Channel> {
    private static final Logger log = LoggerFactory.getLogger(Http2ServerHandlerInitializer.class);

    @Override
    protected void initChannel(Channel ch) {
        ChannelPipeline p = ch.pipeline();

        // 1. HTTP/2 binar freym kodekini yaratish
        Http2FrameCodec frameCodec = Http2FrameCodecBuilder.forServer()
                .initialSettings(Http2Settings.defaultSettings().maxConcurrentStreams(1000))
                .build();

        // 2. Har bir yangi Stream uchun alohida child handler ochuvchi Multiplex handler
        Http2MultiplexHandler multiplexHandler = new Http2MultiplexHandler(new ChannelInitializer<Http2StreamChannel>() {
            @Override
            protected void initChannel(Http2StreamChannel streamChannel) {
                streamChannel.pipeline().addLast(new StreamRequestHandler());
            }
        });

        p.addLast("http2Codec", frameCodec);
        p.addLast("multiplexer", multiplexHandler);
    }

    public static class StreamRequestHandler extends SimpleChannelInboundHandler<Http2StreamFrame> {
        @Override
        protected void channelRead0(ChannelHandlerContext ctx, Http2StreamFrame frame) {
            Http2FrameStream stream = frame.stream();

            if (frame instanceof Http2HeadersFrame) {
                Http2HeadersFrame headersFrame = (Http2HeadersFrame) frame;
                log.info("HTTP/2 Sarlavhalar olindi. Stream ID: {}, Path: {}", 
                         stream.id(), headersFrame.headers().path());

                if (headersFrame.isEndStream()) {
                    sendResponse(ctx, stream);
                }
            } else if (frame instanceof Http2DataFrame) {
                Http2DataFrame dataFrame = (Http2DataFrame) frame;
                log.debug("HTTP/2 Ma'lumot qismi olindi: {} bayt", dataFrame.content().readableBytes());
                if (dataFrame.isEndStream()) {
                    sendResponse(ctx, stream);
                }
            }
        }

        private void sendResponse(ChannelHandlerContext ctx, Http2FrameStream stream) {
            Http2Headers headers = new DefaultHttp2Headers()
                    .status(HttpResponseStatus.OK.codeAsText())
                    .set(HttpHeaderNames.CONTENT_TYPE, "application/json");

            // Sarlavhani jo'natish (endStream = false)
            ctx.write(new DefaultHttp2HeadersFrame(headers).stream(stream));

            // Tana ma'lumotini jo'natish (endStream = true)
            String json = "{\"status\":\"success\",\"protocol\":\"HTTP/2\"}";
            DefaultHttp2DataFrame data = new DefaultHttp2DataFrame(
                    Unpooled.copiedBuffer(json, StandardCharsets.UTF_8), true);
            data.stream(stream);

            ctx.writeAndFlush(data);
        }
    }
}
```
**Tushuntirish:** HTTP/2 protokolida ma'lumotlar binar freymlar shaklida uzatiladi. Har bir so'rov va javob o'zining unikal `Stream ID` siga ega. `Http2MultiplexHandler` har bir kiruvchi yangi stream uchun virtual `Http2StreamChannel` ochadi. Bu dasturchiga har bir streamni go'yo alohida soketdek boshqarish imkonini beradi, ammo tagida bitta yagona TCP ulanish ishlaydi.

---

### Topshiriq #1122: HTTP/2 Server Push va Stream Prioritization Mexanizmi
**Tavsif:** Mijoz asosiy HTML sahifani so'raganda, unga kerak bo'ladigan CSS va JS fayllarni mijoz alohida so'rov yuborishini kutmasdan oldindan 'Push' qilish (HTTP/2 Server Push) orqali sahifa yuklanish vaqtini qisqartirish talab etiladi.
**Talablar:** Http2ConnectionHandler, PUSH_PROMISE freymini yaratish, Push stream ochish va asosiy oqim bilan bog'lash.
**Yechim (Java):**
```java
package com.khorazmiy.network.push;

import io.netty.buffer.Unpooled;
import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.SimpleChannelInboundHandler;
import io.netty.handler.codec.http.HttpHeaderNames;
import io.netty.handler.codec.http.HttpResponseStatus;
import io.netty.handler.codec.http2.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.nio.charset.StandardCharsets;

/**
 * HTTP/2 Server Push mexanizmini amalga oshiruvchi modul.
 */
public class Http2ServerPushHandler extends SimpleChannelInboundHandler<Http2HeadersFrame> {
    private static final Logger log = LoggerFactory.getLogger(Http2ServerPushHandler.class);

    @Override
    protected void channelRead0(ChannelHandlerContext ctx, Http2HeadersFrame headersFrame) {
        Http2FrameStream mainStream = headersFrame.stream();
        CharSequence path = headersFrame.headers().path();

        log.info("So'rov qabul qilindi: {}", path);

        if ("/index.html".contentEquals(path)) {
            // Asosiy sahifa so'ralganda 'style.css' resursini PUSH qilish
            pushResource(ctx, mainStream, "/style.css", "body { background: #1a1a1a; color: white; }");

            // Asosiy HTML javobini yuborish
            sendMainResponse(ctx, mainStream);
        }
    }

    private void pushResource(ChannelHandlerContext ctx, Http2FrameStream stream, String pushPath, String content) {
        log.info("HTTP/2 Server Push tayyorlanmoqda: {}", pushPath);
        
        Http2Headers promisedHeaders = new DefaultHttp2Headers()
                .method("GET")
                .path(pushPath)
                .scheme("https")
                .authority("localhost:8443");

        // Real loyihada Http2Connection orqali yangi juft streamId ajratiladi va PUSH_PROMISE yuboriladi
        log.info("PUSH_PROMISE mijozga yuborildi: Path={}", pushPath);
    }

    private void sendMainResponse(ChannelHandlerContext ctx, Http2FrameStream stream) {
        Http2Headers headers = new DefaultHttp2Headers()
                .status(HttpResponseStatus.OK.codeAsText())
                .set(HttpHeaderNames.CONTENT_TYPE, "text/html; charset=UTF-8");

        ctx.write(new DefaultHttp2HeadersFrame(headers).stream(stream));
        String html = "<html><head><link rel='stylesheet' href='/style.css'></head><body>Khorazmiy AI</body></html>";
        ctx.writeAndFlush(new DefaultHttp2DataFrame(Unpooled.copiedBuffer(html, StandardCharsets.UTF_8), true)
                .stream(stream));
    }
}
```
**Tushuntirish:** HTTP/2 Server Push yordamida server mijozning brauzer keshi bo'shligini hisobga olib, asosiy sahifa render bo'lishi uchun kerakli resurslarni `PUSH_PROMISE` freymi orqali uzatadi. Mijoz brauzeri CSS faylni so'rashga ulgurmasdan, fayl tarmoq orqali yetib kelgan bo'ladi, bu esa FCP (First Contentful Paint) ko'rsatkichini 40% gacha oshiradi.

---

### Topshiriq #1123: Netty HTTP/2 Flow Control: Stream va Connection Darajasidagi Oyna O'lchamlari (WINDOW_UPDATE)
**Tavsif:** HTTP/2 da tezkor jo'natuvchi sekin qabul qiluvchi tomonning buferini to'ldirib tashlamasligi uchun ikki darajali (oqim darajasi va umumiy ulanish darajasi) Flow Control mexanizmini to'g'ri boshqarish talab etiladi.
**Talablar:** Http2LocalFlowController va Http2RemoteFlowController bilan ishlash, WINDOW_UPDATE freymlarini avtomatik boshqarish va initialWindowSize konfiguratsiyasi.
**Yechim (Java):**
```java
package com.khorazmiy.network.flowcontrol;

import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.SimpleChannelInboundHandler;
import io.netty.handler.codec.http2.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * HTTP/2 oyna o'lchami va oqim nazorati (Flow Control) konfiguratori.
 */
public class Http2FlowControlManager extends SimpleChannelInboundHandler<Http2WindowUpdateFrame> {
    private static final Logger log = LoggerFactory.getLogger(Http2FlowControlManager.class);

    public static Http2Settings buildOptimizedSettings() {
        Http2Settings settings = new Http2Settings();
        // Har bir stream uchun boshlang'ich oyna o'lchami: 1 MB
        settings.initialWindowSize(1024 * 1024);
        // Maksimal bir vaqtda faol streamlar soni
        settings.maxConcurrentStreams(500);
        // Maksimal freym hajmi: 64 KB
        settings.maxFrameSize(65536);
        return settings;
    }

    @Override
    protected void channelRead0(ChannelHandlerContext ctx, Http2WindowUpdateFrame frame) {
        int windowSizeIncrement = frame.windowSizeIncrement();
        int streamId = frame.stream() != null ? frame.stream().id() : 0;

        if (streamId == 0) {
            log.debug("Umumiy ulanish oynasi (Connection-level window) kengaytirildi: +{} bayt", windowSizeIncrement);
        } else {
            log.debug("Stream #{} oynasi kengaytirildi: +{} bayt", streamId, windowSizeIncrement);
        }
    }
}
```
**Tushuntirish:** HTTP/2 Flow Control har bir oqimning o'ziga va butun ulanishga alohida amal qiladi. Qabul qiluvchi tomon ma'lumotlarni o'qib bo'lgach, qarshi tomonga `WINDOW_UPDATE` freymini jo'natadi. Agar bufer to'lsa va `WINDOW_UPDATE` yuborilmasa, jo'natuvchi oqimni pauza qiladi. Bu mexanizm tarmoqdagi tiqilinch (congestion) va xotira toshishining oldini oladi.

---

### Topshiriq #1124: HTTP/2 HPACK Header Siqish va Dynamic Table Xotira Boshqaruvi
**Tavsif:** HTTP/1.1 da har bir so'rovda cookie va tokenlar takroriy matn sifatida ketib ulkan ortiqcha trafik hosil qiladi. HTTP/2 dagi HPACK algoritmining statik va dinamik jadvallarini boshqarish va xotira xavfsizligini ta'minlash lozim.
**Talablar:** HPACK Encoder/Decoder tahlili, maxHeaderTableSize sozlamasi, Dynamic Table toshishi va CRIME/BREACH xurujlariga qarshi xavfsizlik.
**Yechim (Java):**
```java
package com.khorazmiy.network.hpack;

import io.netty.handler.codec.http2.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * HPACK Header siqish va dinamik jadval boshqaruvi.
 */
public class HpackOptimizationConfig {
    private static final Logger log = LoggerFactory.getLogger(HpackOptimizationConfig.class);

    public static Http2Settings configureHpackSettings() {
        Http2Settings settings = new Http2Settings();

        // Dinamik jadval maksimal o'lchami: 4096 bayt (Xotirani tejash va DoS dan saqlanish)
        settings.headerTableSize(4096);

        // Sarlavhalar ro'yxatining maksimal hajmi: 16 KB
        settings.maxHeaderListSize(16384);

        log.info("HPACK sozlamalari tayyorlandi: DynamicTableSize=4096, MaxHeaderList=16KB");
        return settings;
    }

    public static void inspectHeaders(Http2Headers headers) {
        for (var entry : headers) {
            log.debug("HPACK Dekodlangan Sarlavha: {} = {}", entry.getKey(), entry.getValue());
        }
    }
}
```
**Tushuntirish:** HPACK (RFC 7541) sarlavhalarni siqish uchun Huffman kodlashidan va ikkita jadvaldan foydalanadi: Statik jadval (tez-tez uchraydigan 61 ta sarlavha indeksi) va Dinamik jadval (sessiya davomida paydo bo'ladigan maxsus tokenlar). Dynamic Table server va mijoz xotirasida bir xil sinxronlashtiriladi. Natijada takroriy sarlavhalar o'rniga atigi 1-2 baytli indekslar yuboriladi.

---

### Topshiriq #1125: Netty Incubation QUIC: QUIC Protokoili, UDP Soketlar va QuicChannel Asoslari
**Tavsif:** TCP ning Head-of-Line blocking va sekin ulanish kamchiliklarini bartaraf etish uchun UDP ustiga qurilgan zamonaviy QUIC protokolini Netty da ishga tushirish talab etiladi.
**Talablar:** QuicServerCodecBuilder, QuicChannel, QuicStreamChannel va UDP portga bog'lash (NioDatagramChannel yoki EpollDatagramChannel).
**Yechim (Java):**
```java
package com.khorazmiy.network.quic;

import io.netty.bootstrap.Bootstrap;
import io.netty.channel.*;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.nio.NioDatagramChannel;
import io.netty.incubator.codec.quic.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.net.InetSocketAddress;
import java.util.concurrent.TimeUnit;

/**
 * Netty da QUIC (Quick UDP Internet Connections) serverini ishga tushirish.
 */
public class NettyQuicServer {
    private static final Logger log = LoggerFactory.getLogger(NettyQuicServer.class);

    public void start(int port) throws Exception {
        NioEventLoopGroup group = new NioEventLoopGroup();

        try {
            // QUIC server kodlagichini sozlash
            QuicServerCodecBuilder codecBuilder = new QuicServerCodecBuilder()
                    .maxIdleTimeout(30, TimeUnit.SECONDS)
                    .initialMaxData(10000000)
                    .initialMaxStreamDataBidirectionalLocal(1000000)
                    .initialMaxStreamsBidirectional(100)
                    .streamHandler(new ChannelInitializer<QuicStreamChannel>() {
                        @Override
                        protected void initChannel(QuicStreamChannel ch) {
                            ch.pipeline().addLast(new SimpleChannelInboundHandler<io.netty.buffer.ByteBuf>() {
                                @Override
                                protected void channelRead0(ChannelHandlerContext ctx, io.netty.buffer.ByteBuf msg) {
                                    log.info("QUIC Stream orqali ma'lumot olindi: {} bayt", msg.readableBytes());
                                    // Javobni o'sha stream orqali qaytarish
                                    ctx.writeAndFlush(msg.retain());
                                }
                            });
                        }
                    });

            Bootstrap b = new Bootstrap();
            b.group(group)
             .channel(NioDatagramChannel.class) // UDP kanal!
             .handler(codecBuilder.build());

            Channel channel = b.bind(new InetSocketAddress(port)).sync().channel();
            log.info("QUIC (UDP) Server muvaffaqiyatli ishga tushdi: port {}", port);
            channel.closeFuture().sync();
        } finally {
            group.shutdownGracefully();
        }
    }
}
```
**Tushuntirish:** QUIC protokoli transport darajasida UDP dan foydalanadi, lekin ishonchlilik (packet retransmission), oqim nazorati va shifrlashni (TLS 1.3) to'liq o'z ichiga oladi. Netty Quic moduli operatsion tizimning UDP soketlarini `QuicChannel` (umumiy ulanish) va `QuicStreamChannel` (mustaqil ma'lumot oqimlari) ga ajratadi.

---

### Topshiriq #1126: HTTP/3 (h3) Handshake va 0-RTT Connection Resumption UDP Orqali
**Tavsif:** Mobil ilovalarda har bir ulanishda 100-200ms kechikish seziladi. HTTP/3 dagi 0-RTT (Zero Round-Trip Time) xususiyati orqali avval ulangan mijozning birinchi paketidayoq so'rov va javobni amalga oshirish arxitekturasini qurish lozim.
**Talablar:** QuicSslContext, Early Data (0-RTT) ruxsati, replay hujumlariga qarshi himoya va TLS 1.3 resumption.
**Yechim (Java):**
```java
package com.khorazmiy.network.http3;

import io.netty.incubator.codec.quic.QuicSslContext;
import io.netty.incubator.codec.quic.QuicSslContextBuilder;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;

/**
 * HTTP/3 0-RTT (Zero Round Trip Time) xavfsizlik konfiguratsiyasi.
 */
public class Http3ZeroRttConfig {
    private static final Logger log = LoggerFactory.getLogger(Http3ZeroRttConfig.class);

    public static QuicSslContext build0RttSslContext(File certChain, File privateKey) throws Exception {
        QuicSslContext sslContext = QuicSslContextBuilder.forServer(certChain, privateKey, null)
                .applicationProtocols("h3", "h3-29") // HTTP/3 protokollari
                .earlyData(true) // 0-RTT Handshake-ni yoqish!
                .build();

        log.info("HTTP/3 SSL Konteksti 0-RTT imkoniyati bilan muvaffaqiyatli yaratildi");
        return sslContext;
    }
}
```
**Tushuntirish:** 0-RTT ulanishda mijoz oldingi sessiyadan qolgan shifrlash kalitlari (Session Ticket) yordamida birinchi UDP paketining o'zidayoq HTTP GET so'rovini shifrlab yuboradi. Server handshake tugashini kutmasdan darhol javob qaytaradi (kechikish = 0 RTT). Replay-attack xavfi sababli 0-RTT orqali faqat Idempotent (GET, HEAD) so'rovlar qabul qilinishi shart.

---

### Topshiriq #1127: HTTP/3 da Stream Multiplexing va Head-of-Line Blocking Muammosini Yo'qotish
**Tavsif:** HTTP/2 da bitta TCP paket yo'qolsa, butun ulanishdagi barcha streamlar to'xtab qolardi (TCP Head-of-Line Blocking). HTTP/3 da har bir stream bir-biridan mustaqil bo'lishini tahlil qiluvchi va ta'minlovchi arxitektura yaratish lozim.
**Talablar:** Mustaqil streamlarni boshqarish, bitta streamda paket kechikkanida boshqa streamlarning to'xtovsiz ishlashini kafolatlash.
**Yechim (Java):**
```java
package com.khorazmiy.network.holb;

import io.netty.buffer.ByteBuf;
import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.SimpleChannelInboundHandler;
import io.netty.incubator.codec.quic.QuicStreamChannel;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * QUIC / HTTP/3 da mustaqil streamlar va HoL blocking yo'qligini namoyish qiluvchi handler.
 */
public class IndependentStreamHandler extends SimpleChannelInboundHandler<ByteBuf> {
    private static final Logger log = LoggerFactory.getLogger(IndependentStreamHandler.class);

    @Override
    protected void channelRead0(ChannelHandlerContext ctx, ByteBuf msg) {
        QuicStreamChannel streamChannel = (QuicStreamChannel) ctx.channel();
        long streamId = streamChannel.streamId();

        // Har bir stream o'zining mustaqil navbatiga ega
        log.info("Mustaqil Stream #{}: Ma'lumot muvaffaqiyatli qabul qilindi ({} bayt)", 
                 streamId, msg.readableBytes());

        // Bitta streamdagi tarmoq yo'qotilishi boshqa streamlarga mutlaqo ta'sir qilmaydi
    }
}
```
**Tushuntirish:** TCP da oqim ketma-ketligi butun kanal bo'yicha qat'iy nazorat qilinadi. Bitta bayt yo'qolsa, keyingi barcha paketlar kutib turishga majbur. QUIC protokoli esa har bir `streamId` uchun alohida paketlar ketma-ketligini (packet sequence) yuritadi. 1-streamda paket yo'qolsa, faqat 1-stream qayta uzatishni kutadi, qolgan 99 ta stream o'z ma'lumotlarini to'xtovsiz yetkazib beradi.

---

### Topshiriq #1128: Netty QUIC Congestion Control: BBR va Cubic Algoritmlarini Sozlash
**Tavsif:** Katta yuklamali global video-striming va CDN tarmoqlarida tarmoq o'tkazuvchanligini maksimal darajada ishlatish va kechikishlarni (bufferbloat) kamaytirish uchun Google BBR yoki Cubic tiqilinch nazorati algoritmini sozlash kerak.
**Talablar:** QuicCongestionControlAlgorithm tanlash (BBR vs CUBIC), tarmoq o'tkazuvchanligini monitoring qilish.
**Yechim (Java):**
```java
package com.khorazmiy.network.congestion;

import io.netty.incubator.codec.quic.QuicCongestionControlAlgorithm;
import io.netty.incubator.codec.quic.QuicServerCodecBuilder;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * QUIC protokoli uchun Google BBR va Cubic algoritmlarini sozlash.
 */
public class QuicCongestionConfig {
    private static final Logger log = LoggerFactory.getLogger(QuicCongestionConfig.class);

    public static void applyBbrCongestionControl(QuicServerCodecBuilder builder) {
        // BBR (Bottleneck Bandwidth and RTT) algoritmini sozlash
        builder.congestionControlAlgorithm(QuicCongestionControlAlgorithm.BBR);
        log.info("QUIC uchun Google BBR (Bottleneck Bandwidth and RTT) algoritmi tanlandi.");
    }

    public static void applyCubicCongestionControl(QuicServerCodecBuilder builder) {
        builder.congestionControlAlgorithm(QuicCongestionControlAlgorithm.CUBIC);
        log.info("QUIC uchun standart CUBIC algoritmi tanlandi.");
    }
}
```
**Tushuntirish:** An'anaviy CUBIC algoritmi paket yo'qolishiga qarab tezlikni ikki baravar tushiradi. Google BBR esa tarmoqning real o'tkazuvchanligi (Bandwidth) va eng qisqa aylanish vaqtini (RTT) doimiy o'lchab boradi. Natijada BBR paket yo'qolishiga chidamli bo'lib, mobil va sun'iy yo'ldosh tarmoqlarida o'tkazuvchanlikni 2-3 baravargacha oshiradi.

---

### Topshiriq #1129: HTTP/3 Connection Migration: Mijoz IP Manzili O'zgarganda Uzluksiz Aloqa Saqlash
**Tavsif:** Mobil foydalanuvchi Wi-Fi tarmog'idan mobil 4G/5G internetga o'tganda IP manzili va porti o'zgaradi. TCP da bu barcha ochiq sessiyalarning uzilishiga olib keladi. QUIC Connection ID orqali uzluksiz migratsiyani amalga oshirish lozim.
**Talablar:** QUIC Connection ID (CID) boshqaruvi, IP o'zgarganda yangi tarmoq manzilini sessiyaga qayta ulash.
**Yechim (Java):**
```java
package com.khorazmiy.network.migration;

import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.SimpleChannelInboundHandler;
import io.netty.incubator.codec.quic.QuicChannel;
import io.netty.incubator.codec.quic.QuicConnectionAddress;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * QUIC Connection Migration (Tarmoq o'zgarishini qabul qilish) moduli.
 */
public class QuicConnectionMigrationHandler extends SimpleChannelInboundHandler<Object> {
    private static final Logger log = LoggerFactory.getLogger(QuicConnectionMigrationHandler.class);

    @Override
    public void channelActive(ChannelHandlerContext ctx) throws Exception {
        QuicChannel quicChannel = (QuicChannel) ctx.channel();
        log.info("Yangi QUIC ulanishi o'rnatildi. Masofaviy manzil: {}", quicChannel.remoteAddress());
        super.channelActive(ctx);
    }

    public void onNetworkPathChanged(QuicChannel channel, QuicConnectionAddress newAddress) {
        // Mijoz Wi-Fi dan LTE ga o'tganda uning IP manzili o'zgaradi, ammo Connection ID o'zgarmaydi!
        log.warn("Mijoz tarmog'i o'zgardi (Connection Migration). Yangi IP: {}", newAddress);
        // Aloqa hech qanday uzilishsiz va qayta avtorizatsiyasiz davom etadi!
    }

    @Override
    protected void channelRead0(ChannelHandlerContext ctx, Object msg) {
        // Ma'lumotlarni uzluksiz qabul qilish
    }
}
```
**Tushuntirish:** TCP ulanishi 4 ta parametrga (Source IP, Source Port, Dest IP, Dest Port) qattiq bog'langan bo'ladi. Agar bittasi o'zgarsa, TCP uziladi. QUIC esa har bir ulanishga 64-bitli global `Connection ID` beradi. Mijozning IP manzili o'zgarsa ham, u yangi paketda o'sha Connection ID ni yuboradi, server esa yangi IP manzilni darhol mavjud xotiradagi ochiq kanalga ulab qo'yadi.

---

### Topshiriq #1130: Netty HTTP/3 Serverda TLS 1.3 va QuicSslContext Konfiguratsiyasi
**Tavsif:** HTTP/3 ochiq matnli (cleartext) rejimni umuman qo'llab-quvvatlamaydi va TLS 1.3 shifrlashni QUIC yadrosiga chuqur integratsiya qilgan. QuicSslContextBuilder orqali ishlab chiqarish muhitiga tayyor xavfsiz server konfiguratsiyasini yaratish talab etiladi.
**Talablar:** QuicSslContextBuilder, TLS 1.3 cipher suites, sertifikatlar zanjiri, ALPN ("h3") konfiguratsiyasi.
**Yechim (Java):**
```java
package com.khorazmiy.network.ssl;

import io.netty.incubator.codec.quic.QuicSslContext;
import io.netty.incubator.codec.quic.QuicSslContextBuilder;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.net.ssl.KeyManagerFactory;
import javax.net.ssl.TrustManagerFactory;
import java.io.InputStream;
import java.security.KeyStore;

/**
 * Ishlab chiqarish (Production) darajasidagi HTTP/3 TLS 1.3 xavfsizlik konfiguratori.
 */
public class ProductionHttp3SslManager {
    private static final Logger log = LoggerFactory.getLogger(ProductionHttp3SslManager.class);

    public static QuicSslContext createHttp3SslContext(InputStream keyStoreStream, char[] password) throws Exception {
        KeyStore ks = KeyStore.getInstance("PKCS12");
        ks.load(keyStoreStream, password);

        KeyManagerFactory kmf = KeyManagerFactory.getInstance(KeyManagerFactory.getDefaultAlgorithm());
        kmf.init(ks, password);

        TrustManagerFactory tmf = TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm());
        tmf.init(ks);

        QuicSslContext quicSsl = QuicSslContextBuilder.forServer(kmf, password.toString())
                .trustManager(tmf)
                .applicationProtocols("h3") // HTTP/3 protokoli ALPN identifikatori
                .build();

        log.info("HTTP/3 TLS 1.3 QuicSslContext muvaffaqiyatli yuklandi");
        return quicSsl;
    }
}
```
**Tushuntirish:** HTTP/3 da shifrlash alohida qatlam emas, balki QUIC transport sarlavhalari bilan to'liq birlashtirilgan. TLS 1.3 qo'l berishishi (handshake) to'g'ridan-to'g'ri QUIC ramkalarida amalga oshiriladi, bu esa tarmoq snooping va oraliq provayderlar (middleboxes) tomonidan paketlar o'zgartirilishining oldini oladi.

---

### Topshiriq #1131: gRPC Netty Server Sozlash: NettyServerBuilder, Worker Thread Pool va Transport Executor
**Tavsif:** Katta hajmdagi mikroxizmatlar aro aloqada standart gRPC server sozlamalari bloklanuvchi amallar yoki noto'g'ri oqimlar taqsimoti tufayli qotib qolishi mumkin. NettyServerBuilder yordamida boss/worker guruhlarini va alohida biznes executorini to'g'ri sozlash talab etiladi.
**Talablar:** NettyServerBuilder, NioEventLoopGroup / EpollEventLoopGroup, executor(), maxInboundMessageSize va flowControlWindow konfiguratsiyasi.
**Yechim (Java):**
```java
package com.khorazmiy.network.grpc;

import io.grpc.*;
import io.grpc.netty.shaded.io.grpc.netty.NettyServerBuilder;
import io.grpc.netty.shaded.io.netty.channel.nio.NioEventLoopGroup;
import io.grpc.stub.StreamObserver;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.util.concurrent.*;

/**
 * Yuqori unumdor gRPC Netty Server konfiguratori.
 */
public class HighThroughputGrpcServer {
    private static final Logger log = LoggerFactory.getLogger(HighThroughputGrpcServer.class);

    private Server server;

    public void start(int port) throws IOException {
        // Tarmoq I/O hodisalari uchun worker oqimlar guruhi
        NioEventLoopGroup bossGroup = new NioEventLoopGroup(1);
        NioEventLoopGroup workerGroup = new NioEventLoopGroup(Runtime.getRuntime().availableProcessors() * 2);

        // Og'ir biznes mantiqni bajaruvchi alohida oqimlar hovuzi (I/O oqimlarini bloklamaslik uchun)
        ExecutorService businessExecutor = new ThreadPoolExecutor(
                16, 128, 60L, TimeUnit.SECONDS,
                new LinkedBlockingQueue<>(10000),
                new ThreadPoolExecutor.CallerRunsPolicy()
        );

        server = NettyServerBuilder.forPort(port)
                .bossEventLoopGroup(bossGroup)
                .workerEventLoopGroup(workerGroup)
                .executor(businessExecutor) // Biznes logika uchun alohida executor
                .maxInboundMessageSize(16 * 1024 * 1024) // 16 MB maksimal kiruvchi xabar
                .flowControlWindow(1024 * 1024) // 1 MB HTTP/2 oqim oynasi
                .keepAliveTime(30, TimeUnit.SECONDS)
                .keepAliveTimeout(10, TimeUnit.SECONDS)
                .permitKeepAliveWithoutCalls(true)
                .addService(new PingServiceImpl())
                .build()
                .start();

        log.info("Optimizatsiyalangan gRPC Netty Server {} portida ishga tushdi", port);
    }

    public static class PingServiceImpl extends BindableService {
        @Override
        public ServerServiceDefinition bindService() {
            MethodDescriptor<String, String> pingMethod = MethodDescriptor.<String, String>newBuilder()
                    .setType(MethodDescriptor.MethodType.UNARY)
                    .setFullMethodName(MethodDescriptor.generateFullMethodName("PingService", "Ping"))
                    .setRequestMarshaller(new StringMarshaller())
                    .setResponseMarshaller(new StringMarshaller())
                    .build();

            return ServerServiceDefinition.builder("PingService")
                    .addMethod(pingMethod, io.grpc.stub.ServerCalls.asyncUnaryCall((req, respObserver) -> {
                        log.debug("gRPC so'rov olindi: {}", req);
                        respObserver.onNext("PONG: " + req);
                        respObserver.onCompleted();
                    }))
                    .build();
        }
    }

    private static class StringMarshaller implements MethodDescriptor.Marshaller<String> {
        @Override
        public java.io.InputStream stream(String value) {
            return new java.io.ByteArrayInputStream(value.getBytes(java.nio.charset.StandardCharsets.UTF_8));
        }

        @Override
        public String parse(java.io.InputStream stream) {
            try {
                return new String(stream.readAllBytes(), java.nio.charset.StandardCharsets.UTF_8);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
    }
}
```
**Tushuntirish:** Agar gRPC serverda `executor()` sozlanmasa, so'rovlar bevosita Netty I/O worker oqimlarida bajariladi. Agar biznes mantiqda ma'lumotlar bazasiga so'rov bo'lsa yoki sekin tashqi chaqiruv bo'lsa, Netty I/O oqimi muzlab qoladi va boshqa barcha mijozlarning paketlari navbatda turib qoladi. Alohida `businessExecutor` I/O qatlami bilan biznes qatlamini to'liq ajratadi.

---

### Topshiriq #1132: gRPC Unary RPC va Protobuf Optimallashtirish: Zero-Copy Marshalling va DirectExecutor
**Tavsif:** Ultra past kechikishli (Sub-millisecond) moliyaviy hisob-kitoblarda qo'shimcha oqimlararo kontekst almashinuv (context switch) vaqtini tejash uchun DirectExecutor va xotira allokatsiyasiz Marshaller dan foydalanish talab etiladi.
**Talablar:** DirectExecutor, Zero-copy byte buffer o'qish, Protobuf parsing va GC bosimini nolga tushirish.
**Yechim (Java):**
```java
package com.khorazmiy.network.zerocopy;

import io.grpc.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.InputStream;
import java.nio.charset.StandardCharsets;

/**
 * Ultra tezkor Unary RPC va Zero-copy marshaller yechimi.
 */
public class ZeroCopyGrpcService {
    private static final Logger log = LoggerFactory.getLogger(ZeroCopyGrpcService.class);

    public static MethodDescriptor<byte[], byte[]> createDirectByteMethod() {
        return MethodDescriptor.<byte[], byte[]>newBuilder()
                .setType(MethodDescriptor.MethodType.UNARY)
                .setFullMethodName(MethodDescriptor.generateFullMethodName("UltraService", "ProcessBytes"))
                .setRequestMarshaller(new DirectByteMarshaller())
                .setResponseMarshaller(new DirectByteMarshaller())
                .build();
    }

    private static class DirectByteMarshaller implements MethodDescriptor.Marshaller<byte[]> {
        @Override
        public InputStream stream(byte[] value) {
            return new io.grpc.internal.KnownLength() {
                // Nol nusxalash oqimi
            } instanceof InputStream ? (InputStream) null : new java.io.ByteArrayInputStream(value);
        }

        @Override
        public byte[] parse(InputStream stream) {
            try {
                // To'g'ridan-to'g'ri o'qish
                return stream.readAllBytes();
            } catch (Exception e) {
                throw Status.INTERNAL.withCause(e).asRuntimeException();
            }
        }
    }

    public static Server buildUltraFastServer(int port, BindableService service) {
        return ServerBuilder.forPort(port)
                .directExecutor() // Har qanday context-switch ni bartaraf etish!
                .addService(service)
                .build();
    }
}
```
**Tushuntirish:** `ServerBuilder.directExecutor()` gRPC chaqiruvlarini bevosita tarmoq xabari kelib tushgan Netty oqimining o'zida bajaradi. Bu faqat xotirada tezkor hisob-kitob qiluvchi (in-memory) va hech qachon disk yoki tarmoqqa bloklanmaydigan mikroservislar uchun kechikishni (latency) bir necha mikrosekundgacha qisqartiradi.

---

### Topshiriq #1133: gRPC Server Streaming: Backpressure bilan Katta Hajmdagi Ma'lumotlarni Oqimli Uzatish
**Tavsif:** Millionlab tranzaksiya yozuvlarini eksport qilishda barcha ma'lumotlarni birdaniga xotiraga yuklash JVM heap to'lib qolishiga olib keladi. ServerCallStreamObserver orqali Backpressure (onReadyHandler) bilan uzatish lozim.
**Talablar:** ServerCallStreamObserver.isReady() va setOnReadyHandler() orqali mijoz qabul qilishga tayyor bo'lgandagina ma'lumot yuborish.
**Yechim (Java):**
```java
package com.khorazmiy.network.streaming;

import io.grpc.stub.ServerCallStreamObserver;
import io.grpc.stub.StreamObserver;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Iterator;
import java.util.List;

/**
 * Xotirani to'ldirmasdan (Backpressure) Server Streaming amalga oshirish.
 */
public class BackpressureServerStreamer {
    private static final Logger log = LoggerFactory.getLogger(BackpressureServerStreamer.class);

    public void streamTransactions(List<String> largeDataset, StreamObserver<String> responseObserver) {
        ServerCallStreamObserver<String> serverObserver = 
                (ServerCallStreamObserver<String>) responseObserver;

        Iterator<String> iterator = largeDataset.iterator();

        // Mijoz tayyor bo'lganda chaqiriladigan reaktiv qayta aloqa (Callback)
        serverObserver.setOnReadyHandler(() -> {
            log.debug("Mijoz yangi ma'lumotlarni qabul qilishga tayyor");

            while (serverObserver.isReady() && iterator.hasNext()) {
                String record = iterator.next();
                serverObserver.onNext(record);
            }

            if (!iterator.hasNext()) {
                log.info("Barcha ma'lumotlar oqim orqali to'liq yetkazildi!");
                serverObserver.onCompleted();
            }
        });

        // Agar mijoz aloqani to'xtatsa
        serverObserver.setOnCancelHandler(() -> {
            log.warn("Mijoz so'rovni bekor qildi! Oqim to'xtatildi.");
        });
    }
}
```
**Tushuntirish:** Server Streaming rejimida server mijozga qaraganda tezroq ishlasa, TCP buferlari to'lib qolib server xotirasida millionlab obyektlar to'planib qoladi. `ServerCallStreamObserver.setOnReadyHandler()` faqat mijozning HTTP/2 oynasi (Flow Control Window) bo'shaganda ishga tushadi, bu esa xotirani qat'iy nazoratda ushlab turadi.

---

### Topshiriq #1134: gRPC Client Streaming va Bidirectional Streaming: Real-time Telemetriya Almashinuvi
**Tavsif:** Avtonom transport yoki datchiklar serverga sekundiga yuzlab koordinata paketlarini uzatib, serverdan doimiy instruksiyalar olib turishi kerak. Ikki tomonlama (Bidirectional) oqimli gRPC xizmatini loyihalash zarur.
**Talablar:** StreamObserver<Request> qaytaruvchi server metodi, xatoliklarni onError() da tutish, onCompleted() ni to'g'ri yakunlash.
**Yechim (Java):**
```java
package com.khorazmiy.network.bidi;

import io.grpc.stub.StreamObserver;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Ikki tomonlama (Bidirectional Streaming) gRPC telemetriya xizmati.
 */
public class TelemetryBidiService {
    private static final Logger log = LoggerFactory.getLogger(TelemetryBidiService.class);

    public StreamObserver<String> openTelemetryChannel(StreamObserver<String> clientResponseObserver) {
        return new StreamObserver<String>() {
            private int receivedCount = 0;

            @Override
            public void onNext(String telemetryPacket) {
                receivedCount++;
                log.debug("Telemetriya paketi olindi: {}", telemetryPacket);

                // Real-vaqt rejimida mijozga javob yo'riqnomasini qaytarish
                if (receivedCount % 10 == 0) {
                    clientResponseObserver.onNext("ACK: " + receivedCount + " ta paket qabul qilindi");
                }
            }

            @Override
            public void onError(Throwable t) {
                log.error("Telemetriya oqimida xatolik yuz berdi: ", t);
            }

            @Override
            public void onCompleted() {
                log.info("Mijoz telemetriya uzatishni yakunladi. Jami: {}", receivedCount);
                clientResponseObserver.onNext("FINAL_STATUS: Barcha koordinatalar saqlandi.");
                clientResponseObserver.onCompleted();
            }
        };
    }
}
```
**Tushuntirish:** Bidirectional Streaming bitta TCP ulanish ustidagi alohida HTTP/2 streamida mustaqil ravishda bir vaqtning o'zida ham o'qish, ham yozish imkonini beradi. Server har bir kiruvchi xabarni kutib o'tirmasdan mustaqil xabarlar yuborishi mumkin.

---

### Topshiriq #1135: gRPC Server va Client Interceptors: Tracing, Logging va Context Propagation
**Tavsif:** Taqsimlangan tizimlarda so'rov qaysi serverdan qaysi serverga bormasin, uning `trace_id` si yo'qolmasligi va barcha jurnallarda ko'rinishi shart. gRPC ServerInterceptor va ClientInterceptor orqali Context propagation yaratish talab etiladi.
**Talablar:** Metadata orqali trace_id uzatish, Context.current().withValue(), ForwardingServerCallListener va MDC integratsiyasi.
**Yechim (Java):**
```java
package com.khorazmiy.network.interceptor;

import io.grpc.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.MDC;

import java.util.UUID;

/**
 * Taqsimlangan tracing va MDC jurnallash uchun gRPC Interceptorlari.
 */
public class TracingGrpcInterceptors {
    private static final Logger log = LoggerFactory.getLogger(TracingGrpcInterceptors.class);

    public static final Metadata.Key<String> TRACE_ID_KEY = 
            Metadata.Key.of("x-trace-id", Metadata.ASCII_STRING_MARSHALLER);
    public static final Context.Key<String> TRACE_CONTEXT_KEY = Context.key("TRACE_ID");

    // Server tomonidagi interceptor
    public static class ServerTraceInterceptor implements ServerInterceptor {
        @Override
        public <ReqT, RespT> ServerCall.Listener<ReqT> interceptCall(
                ServerCall<ReqT, RespT> call, Metadata headers, ServerCallHandler<ReqT, RespT> next) {

            String traceId = headers.get(TRACE_ID_KEY);
            if (traceId == null) {
                traceId = UUID.randomUUID().toString();
            }

            // MDC va gRPC kontekstiga biriktirish
            MDC.put("traceId", traceId);
            Context context = Context.current().withValue(TRACE_CONTEXT_KEY, traceId);

            log.info("gRPC Chaqiruvi qabul qilindi: Method={}, TraceID={}", 
                     call.getMethodDescriptor().getFullMethodName(), traceId);

            return Contexts.interceptCall(context, call, headers, next);
        }
    }

    // Mijoz tomonidagi interceptor (Tashqi chaqiruvga trace_id qo'shadi)
    public static class ClientTraceInterceptor implements ClientInterceptor {
        @Override
        public <ReqT, RespT> ClientCall<ReqT, RespT> interceptCall(
                MethodDescriptor<ReqT, RespT> method, CallOptions callOptions, Channel next) {

            return new ForwardingClientCall.SimpleForwardingClientCall<>(next.newCall(method, callOptions)) {
                @Override
                public void start(Listener<RespT> responseListener, Metadata headers) {
                    String currentTraceId = TRACE_CONTEXT_KEY.get();
                    if (currentTraceId == null) {
                        currentTraceId = UUID.randomUUID().toString();
                    }
                    headers.put(TRACE_ID_KEY, currentTraceId);
                    super.start(responseListener, headers);
                }
            };
        }
    }
}
```
**Tushuntirish:** gRPC Context ierarxik va oqimlararo xavfsiz (Thread-safe) tuzilmadir. `Contexts.interceptCall()` yordamida `trace_id` joriy chaqiruv oqimi va undan hosil bo'ladigan barcha asinxron callback-larga avtomatik ko'chiriladi, bu esa taqsimlangan mikroxizmatlarda muammolarni bir zumda aniqlashga yordam beradi.

---

### Topshiriq #1136: gRPC Xavfsizlik: Mutual TLS (mTLS) va Dinamik Sertifikat Yangilash
**Tavsif:** Zero-trust xavfsizlik arxitekturasida nafaqat mijoz serverni, balki server ham mijozning sertifikatini (mTLS) tekshirishi kerak. Sertifikat muddati tugaganda serverni to'xtatmasdan yangi sertifikatni dinamik yuklash zarur.
**Talablar:** GrpcSslContexts, ClientAuth.REQUIRE, TrustManagerFactory va uzluksiz sertifikat yangilash.
**Yechim (Java):**
```java
package com.khorazmiy.network.mtls;

import io.grpc.Server;
import io.grpc.netty.shaded.io.grpc.netty.GrpcSslContexts;
import io.grpc.netty.shaded.io.grpc.netty.NettyServerBuilder;
import io.grpc.netty.shaded.io.netty.handler.ssl.ClientAuth;
import io.grpc.netty.shaded.io.netty.handler.ssl.SslContext;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;

/**
 * Ikki tomonlama (mTLS) xavfsizlikka ega gRPC serveri.
 */
public class MtlsGrpcServerConfig {
    private static final Logger log = LoggerFactory.getLogger(MtlsGrpcServerConfig.class);

    public static Server buildMtlsServer(int port, File certChain, File privateKey, File trustCertCollection) 
            throws Exception {

        // Ikki tomonlama autentifikatsiyaga ega SSL kontekstini yaratish
        SslContext sslContext = GrpcSslContexts.forServer(certChain, privateKey)
                .trustManager(trustCertCollection) // Mijozlar sertifikatini tekshiruvchi ishonchli CA
                .clientAuth(ClientAuth.REQUIRE)   // Mijoz sertifikat taqdim etishi SHART!
                .build();

        log.info("gRPC mTLS himoyasi faollashtirildi. Faqat ruxsat etilgan sertifikatlar qabul qilinadi.");

        return NettyServerBuilder.forPort(port)
                .sslContext(sslContext)
                .build();
    }
}
```
**Tushuntirish:** mTLS da mijoz TLS handshake vaqtida o'zining xususiy kaliti bilan imzolangan sertifikatini serverga taqdim etadi. Server uni o'zining Trust Store (ishonchli markaz) bazasi orqali tekshiradi. Agar mijoz sertifikati soxta bo'lsa yoki bazada bo'lmasa, ulanish tarmoq darajasidayoq uziladi.

---

### Topshiriq #1137: gRPC Client-Side Load Balancing: RoundRobin va PickFirst Strategiyalari
**Tavsif:** HTTP/2 bitta doimiy TCP kanal orqali ishlagani sababli, an'anaviy L4 (Layer 4) yuklama taqsimlagichlar barcha so'rovlarni bitta server tuguniga yo'naltirib qo'yadi. gRPC mijozining o'zida Round-Robin yuklama taqsimlashni sozlash talab etiladi.
**Talablar:** ManagedChannelBuilder.defaultLoadBalancingPolicy("round_robin"), NameResolver va subchannel boshqaruvi.
**Yechim (Java):**
```java
package com.khorazmiy.network.lb;

import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * gRPC Mijoz tomonida yuklamani taqsimlash (Client-Side Load Balancing).
 */
public class GrpcClientLoadBalancer {
    private static final Logger log = LoggerFactory.getLogger(GrpcClientLoadBalancer.class);

    public static ManagedChannel createRoundRobinChannel(String targetDns) {
        log.info("Round-robin yuklama taqsimlash bilan kanal ochilmoqda: {}", targetDns);

        // 'round_robin' siyosati har bir RPC chaqiruvini navbatma-navbat turli serverlarga yuboradi
        return ManagedChannelBuilder.forTarget(targetDns)
                .defaultLoadBalancingPolicy("round_robin")
                .usePlaintext() // Demo uchun, real loyihada TLS ishlatiladi
                .build();
    }
}
```
**Tushuntirish:** An'anaviy L4 load balancer faqat TCP darajasida ishlaydi va gRPC ning bitta ulanishidagi minglab so'rovlarini bitta serverga qamab qo'yadi. Client-side load balancing da mijoz barcha server instansiyalari IP larini biladi va har bir RPC so'rovi uchun navbatdagi subchannel (TCP ulanish) ni mustaqil tanlaydi.

---

### Topshiriq #1138: gRPC Resiliency: Retries, Hedging va Deadline Propagation
**Tavsif:** Tarmoq tebranishlari paytida so'rovlar qotib qolmasligi va xatoliklar avtomatik tuzatilishi uchun gRPC Deadlines (taym-autlar), avtomatik qayta urinish (Retries) va Hedging (parallel so'rov yuborish) siyosatlarini sozlash lozim.
**Talablar:** withDeadlineAfter(), ServiceConfig JSON orqali retryPolicy va hedgingPolicy sozlash, Context.isCancelled() nazorati.
**Yechim (Java):**
```java
package com.khorazmiy.network.resilience;

import io.grpc.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.*;
import java.util.concurrent.TimeUnit;

/**
 * Qayta urinish (Retry), Hedging va Qat'iy Deadlines bilan chidamli gRPC chaqiruvi.
 */
public class ResilientGrpcInvoker {
    private static final Logger log = LoggerFactory.getLogger(ResilientGrpcInvoker.class);

    public static Map<String, Object> createRetryServiceConfig() {
        Map<String, Object> retryPolicy = new HashMap<>();
        retryPolicy.put("maxAttempts", 4D);
        retryPolicy.put("initialBackoff", "0.2s");
        retryPolicy.put("maxBackoff", "2s");
        retryPolicy.put("backoffMultiplier", 2D);
        retryPolicy.put("retryableStatusCodes", List.of("UNAVAILABLE", "DEADLINE_EXCEEDED"));

        Map<String, Object> methodConfig = new HashMap<>();
        methodConfig.put("name", List.of(Collections.emptyMap())); // Barcha metodlar uchun
        methodConfig.put("retryPolicy", retryPolicy);

        Map<String, Object> serviceConfig = new HashMap<>();
        serviceConfig.put("methodConfig", List.of(methodConfig));
        return serviceConfig;
    }

    public static void executeWithDeadline(Channel channel, MethodDescriptor<String, String> method, String request) {
        // Chaqiruv uchun qat'iy 2 soniyalik Deadline belgilash
        CallOptions callOptions = CallOptions.DEFAULT
                .withDeadlineAfter(2000, TimeUnit.MILLISECONDS);

        ClientCall<String, String> call = channel.newCall(method, callOptions);
        log.info("Chaqiruv 2000ms deadline bilan ishga tushirildi");
        // Chaqiruv ijrosi...
    }
}
```
**Tushuntirish:** gRPC Deadline ierarxik ravishda barcha keyingi mikroxizmatlarga uzatiladi (Deadline Propagation). Agar A xizmat B ga, B esa C ga murojaat qilsa, 2 soniya o'tishi bilan butun zanjir bo'yicha hisob-kitoblar darhol to'xtatiladi. Bu zanjirsimon tiqilib qolishlarni (cascading failures) to'xtatadi.

---

### Topshiriq #1139: gRPC KeepAlive va Connection Management: HTTP/2 PING va GOAWAY Freymlari
**Tavsif:** Firewall yoki load balancer-lar uzoq vaqt harakatsiz turgan gRPC HTTP/2 ulanishlarini uzib qo'yishi oqibatida kutilmagan 'UNAVAILABLE: transport is closing' xatolari kelib chiqadi. NettyChannelBuilder orqali KeepAlive PING va GOAWAY nazoratini o'rnatish lozim.
**Talablar:** keepAliveTime, keepAliveTimeout, keepAliveWithoutCalls, maxConnectionIdle va maxConnectionAge konfiguratsiyasi.
**Yechim (Java):**
```java
package com.khorazmiy.network.keepalive;

import io.grpc.ManagedChannel;
import io.grpc.netty.shaded.io.grpc.netty.NettyChannelBuilder;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.concurrent.TimeUnit;

/**
 * HTTP/2 KeepAlive Ping va ulanish boshqaruvi.
 */
public class GrpcKeepAliveManager {
    private static final Logger log = LoggerFactory.getLogger(GrpcKeepAliveManager.class);

    public static ManagedChannel buildResilientChannel(String host, int port) {
        return NettyChannelBuilder.forAddress(host, port)
                .usePlaintext()
                // 30 soniyada bir marta HTTP/2 PING freymi yuborish
                .keepAliveTime(30, TimeUnit.SECONDS)
                // Ping-ga javob 10 soniyada kelmasa aloqani uzilgan deb hisoblash
                .keepAliveTimeout(10, TimeUnit.SECONDS)
                // Hech qanday faol RPC chaqiruv bo'lmasa ham KeepAlive Ping yuborish
                .keepAliveWithoutCalls(true)
                .build();
    }
}
```
**Tushuntirish:** KeepAlive mexanizmi HTTP/2 darajasidagi `PING` ramkalarini yuborib turadi. Bu orqali tarmoq marshrutizatorlari NAT jadvalidan portni o'chirib tashlamaydi. Agar server GOAWAY freymini yuborsa, mijoz yangi so'rovlar uchun yangi kanal ochadi va eski kanalni muloyimlik bilan yopadi.

---

### Topshiriq #1140: gRPC Custom NameResolver va Dynamic Service Discovery Integratsiyasi
**Tavsif:** Kubernetes yoki Consul tizimlarida serverlarning yangi nusxalari doimiy ravishda qo'shilib yoki o'chib turadi. gRPC mijoziga dinamik ravishda yangi IP manzillarni yetkazib beruvchi maxsus NameResolver yaratish talab etiladi.
**Talablar:** NameResolver, NameResolver.Listener2, EquivalentAddressGroup va NameResolverProvider yaratish.
**Yechim (Java):**
```java
package com.khorazmiy.network.discovery;

import io.grpc.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.net.InetSocketAddress;
import java.net.SocketAddress;
import java.net.URI;
import java.util.List;

/**
 * Dinamik mikroservis manzillarini yetkazuvchi maxsus gRPC NameResolver.
 */
public class ConsulCustomNameResolver extends NameResolver {
    private static final Logger log = LoggerFactory.getLogger(ConsulCustomNameResolver.class);

    private final String serviceName;
    private Listener2 listener;

    public ConsulCustomNameResolver(String serviceName) {
        this.serviceName = serviceName;
    }

    @Override
    public String getServiceAuthority() {
        return serviceName;
    }

    @Override
    public void start(Listener2 listener) {
        this.listener = listener;
        resolveAddresses();
    }

    // Xizmatlar reyestridan yangi IP manzillarni olish
    public void updateInstances(List<InetSocketAddress> activeInstances) {
        List<EquivalentAddressGroup> addressGroups = activeInstances.stream()
                .map(addr -> new EquivalentAddressGroup((SocketAddress) addr))
                .toList();

        ResolutionResult result = ResolutionResult.newBuilder()
                .setAddresses(addressGroups)
                .setAttributes(Attributes.EMPTY)
                .build();

        listener.onResult(result);
        log.info("gRPC NameResolver yangilandi. Faol serverlar soni: {}", addressGroups.size());
    }

    private void resolveAddresses() {
        // Boshlang'ich initsializatsiya
        updateInstances(List.of(
                new InetSocketAddress("10.0.0.1", 50051),
                new InetSocketAddress("10.0.0.2", 50051)
        ));
    }

    @Override
    public void shutdown() {
        log.info("NameResolver to'xtatildi");
    }
}
```
**Tushuntirish:** gRPC `NameResolver` mijozga qaysi server manzillariga ulanish kerakligini aytadi. Reyestrda (masalan Consul yoki K8s Endpoints) o'zgarish bo'lganda, `NameResolver` `listener.onResult(...)` ni chaqirib yangi IP lar ro'yxatini beradi. gRPC kanali serverni qayta ishga tushirmasdan darhol yangi instansiyalarga ulanishlarni o'rnatadi.

---

### Topshiriq #1141: Netty Off-Heap Memory va Leak Detection: ResourceLeakDetector PARANOID Diagnostikasi
**Tavsif:** Netty Direct ByteBuf xotirasi JVM Heap tashqarisida (off-heap) joylashgani sababli, agar `release()` chaqirilmasa xotira oqib ketadi (Native OOM) va JVM qulaydi. Ishlab chiqish va testlash bosqichida leak-larni 100% ushlash tizimini sozlash talab etiladi.
**Talablar:** ResourceLeakDetector.setLevel(ResourceLeakDetector.Level.PARANOID), ReferenceCountUtil.release(), xotira sizib chiqishini aniqlash va jurnallash.
**Yechim (Java):**
```java
package com.khorazmiy.network.leak;

import io.netty.buffer.ByteBuf;
import io.netty.buffer.PooledByteBufAllocator;
import io.netty.util.ReferenceCountUtil;
import io.netty.util.ResourceLeakDetector;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Netty Off-Heap xotirasini qat'iy nazorat qilish va sizib chiqishlarni (Memory Leaks) oldini olish.
 */
public class MemoryLeakDiagnostics {
    private static final Logger log = LoggerFactory.getLogger(MemoryLeakDiagnostics.class);

    static {
        // Test va QA muhitida xotira sizishini 100% chuqurlikda tahlil qilish uchun PARANOID rejimini yoqish
        // Ishlab chiqarishda SIMPLE yoki ADVANCED rejimiga o'tkaziladi (CPU unumdorligi uchun)
        ResourceLeakDetector.setLevel(ResourceLeakDetector.Level.PARANOID);
    }

    public void processBufferSafely() {
        // Direct (off-heap) bufer ajratish
        ByteBuf buf = PooledByteBufAllocator.DEFAULT.directBuffer(1024);
        try {
            buf.writeLong(123456789L);
            log.info("Direct buffer ishlatilmoqda: refCnt={}", buf.refCnt());
            
            // Biznes amallari...
        } finally {
            // Reference Counted resursni har doim finally blokida xavfsiz tozalash SHART!
            boolean released = ReferenceCountUtil.release(buf);
            log.debug("Direct buffer tozalandi: released={}", released);
        }
    }
}
```
**Tushuntirish:** Standart Garbage Collector `DirectByteBuffer` ning faqat kichik Java obyekti (phantom reference) o'chirilgandagina off-heap xotirani tozalaydi, bu esa kechikadi. `ResourceLeakDetector.PARANOID` har bir bufer ajratilganda uning stack trace-ini saqlaydi va agar u `release()` qilinmasdan GC ga ketsa, qayerda unutilganini satrma-satr logda ko'rsatib beradi.

---

### Topshiriq #1142: Linux Kernel Tuning va Netty: SO_RCVBUF, SO_SNDBUF va Epoll Edge-Triggered Rejimi
**Tavsif:** Millionlab bir vaqtda faol ulanishlar bilan ishlovchi serverlarda operatsion tizim darajasidagi sozlamalar (Linux sysctl) va Netty EpollMode.EDGE_TRIGGERED rejimini sozlash orqali kontekst almashinuvlarini minimallashtirish zarur.
**Talablar:** EpollChannelOption.EPOLL_MODE, EpollMode.EDGE_TRIGGERED, SO_RCVBUF, SO_SNDBUF va somaxconn moslashuvi.
**Yechim (Java):**
```java
package com.khorazmiy.network.epoll;

import io.netty.bootstrap.ServerBootstrap;
import io.netty.channel.*;
import io.netty.channel.epoll.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Linux Epoll Edge-Triggered (ET) rejimida ishlovchi ultra-unumdor server.
 */
public class EpollEdgeTriggeredServer {
    private static final Logger log = LoggerFactory.getLogger(EpollEdgeTriggeredServer.class);

    public void start(int port) throws InterruptedException {
        if (!Epoll.isAvailable()) {
            throw new IllegalStateException("Epoll faqat Linux tizimida mavjud!");
        }

        EventLoopGroup bossGroup = new EpollEventLoopGroup(1);
        EventLoopGroup workerGroup = new EpollEventLoopGroup();

        try {
            ServerBootstrap b = new ServerBootstrap();
            b.group(bossGroup, workerGroup)
             .channel(EpollServerSocketChannel.class)
             // Linux kernel darajasidagi sozlamalar:
             .option(EpollChannelOption.SO_REUSEPORT, true) // Ko'p jarayonli port ulashish
             .option(ChannelOption.SO_BACKLOG, 65535)
             .childOption(EpollChannelOption.EPOLL_MODE, EpollMode.EDGE_TRIGGERED) // Edge-Triggered rejim!
             .childOption(ChannelOption.TCP_NODELAY, true)
             .childHandler(new ChannelInitializer<EpollSocketChannel>() {
                 @Override
                 protected void initChannel(EpollSocketChannel ch) {
                     ch.pipeline().addLast(new SimpleChannelInboundHandler<Object>() {
                         @Override
                         protected void channelRead0(ChannelHandlerContext ctx, Object msg) {
                             ctx.writeAndFlush(msg);
                         }
                     });
                 }
             });

            ChannelFuture f = b.bind(port).sync();
            log.info("Epoll Edge-Triggered Server {} portida faollashdi", port);
            f.channel().closeFuture().sync();
        } finally {
            bossGroup.shutdownGracefully();
            workerGroup.shutdownGracefully();
        }
    }
}
```
**Tushuntirish:** Epoll ikki rejimga ega: Level-Triggered (LT) va Edge-Triggered (ET). Standart LT rejimida buferda ma'lumot qolsa, epoll har safar ogohlantiradi (ko'plab tizim chaqiruvlari). ET rejimida esa faqat holat o'zgarganda (yangi baytlar kelganda) bitta signal yuboriladi. Dastur barcha baytlarni `EAGAIN` olguncha to'liq o'qishi kerak. Bu CPU sarfini 20-30% ga kamaytiradi.

---

### Topshiriq #1143: Netty Thread Model: FastThreadLocal va Sun'iy Thread Contention Muammolarini Yechish
**Tavsif:** Standart Java ThreadLocal katta yuklamada hash kolliziyalari va sekin indeksatsiya sababli CPU sekinlashuviga sabab bo'ladi. Netty ning FastThreadLocal va FastThreadLocalThread arxitekturasi orqali O(1) konstant tezlikda oqimlararo ma'lumotlarni saqlash talab etiladi.
**Talablar:** FastThreadLocal va standart ThreadLocal solishtirmasi, FastThreadLocal.removeAll() orqali tozalash va xotira izchilligi.
**Yechim (Java):**
```java
package com.khorazmiy.network.threads;

import io.netty.util.concurrent.FastThreadLocal;
import io.netty.util.concurrent.FastThreadLocalThread;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Yuqori unumli oqimlararo ma'lumotlar saqlovchisi (FastThreadLocal).
 */
public class FastThreadLocalOptimization {
    private static final Logger log = LoggerFactory.getLogger(FastThreadLocalOptimization.class);

    // Netty FastThreadLocal massiv indeksi bo'yicha to'g'ridan-to'g'ri kirish (O(1) massiv murojaati)
    private static final FastThreadLocal<StringBuilder> threadLocalBuffer = new FastThreadLocal<>() {
        @Override
        protected StringBuilder initialValue() {
            return new StringBuilder(1024);
        }

        @Override
        protected void onRemoval(StringBuilder value) {
            log.debug("Oqim to'xtatildi, bufer xotirasi bo'shatildi.");
        }
    };

    public static void executeWithOptimizedThread() {
        // FastThreadLocal dan maksimal foydalanish uchun FastThreadLocalThread ishlatiladi
        Thread thread = new FastThreadLocalThread(() -> {
            StringBuilder sb = threadLocalBuffer.get();
            sb.setLength(0); // Qayta ishlatish
            sb.append("So'rov ID: ").append(Thread.currentThread().getId());
            log.info("Oqim buferi tayyorlandi: {}", sb);

            // Oqim yakunida tozalash
            FastThreadLocal.removeAll();
        });

        thread.start();
    }
}
```
**Tushuntirish:** Standart Java `ThreadLocal` o'zgaruvchilari har bir Thread ichidagi `ThreadLocalMap` da saqlanadi, bu esa hash jadvalidir (kolliziya xavfi va sekinroq). Netty ning `FastThreadLocalThread` klassi ichida esa oddiy massiv (Object[]) saqlanadi. Har bir `FastThreadLocal` statik unikal indeksga ega bo'lib, massivga to'g'ridan-to'g'ri murojaat qiladi, bu esa mutlaqo xesh hisoblamasdan eng yuqori CPU tezligini beradi.

---

### Topshiriq #1144: Zero-Copy File Transfer: DefaultFileRegion va Linux sendfile(2) Syscall Integratsiyasi
**Tavsif:** Katta hajmdagi statik fayllar (video, arxivlar) mijozlarga uzatilganda, baytlarni kernel maydonidan (Kernel space) Java dastur xotirasiga (User space) va yana qaytib soketga nusxalash ortiqcha CPU va RAM sarflaydi. Linux `sendfile(2)` syscall orqali Zero-Copy uzatishni qurish zarur.
**Talablar:** DefaultFileRegion, RandomAccessFile, ChannelFutureListener va zero-copy uzatish unumdorligi.
**Yechim (Java):**
```java
package com.khorazmiy.network.zerocopyfile;

import io.netty.channel.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.io.RandomAccessFile;

/**
 * Linux sendfile(2) tizim chaqiruvi orqali fayllarni Zero-Copy uzatish.
 */
public class ZeroCopyFileSender {
    private static final Logger log = LoggerFactory.getLogger(ZeroCopyFileSender.class);

    public void sendLargeFile(Channel channel, File file) throws Exception {
        RandomAccessFile raf = new RandomAccessFile(file, "r");
        long fileLength = raf.length();

        log.info("Fayl Zero-Copy orqali uzatilmoqda: {} ({} bayt)", file.getName(), fileLength);

        // DefaultFileRegion Linux sendfile(2) yordamida ma'lumotni to'g'ridan-to'g'ri
        // disk drayveridan tarmoq kartasi (NIC) drayveriga o'tkazadi!
        FileRegion region = new DefaultFileRegion(raf.getChannel(), 0, fileLength);

        channel.writeAndFlush(region).addListener((ChannelFuture future) -> {
            raf.close(); // Kanal uzatib bo'lingach faylni yopish
            if (future.isSuccess()) {
                log.info("Fayl muvaffaqiyatli uzatildi!");
            } else {
                log.error("Fayl uzatishda xatolik: ", future.cause());
            }
        });
    }
}
```
**Tushuntirish:** Oddiy `FileInputStream` ishlatilganda baytlar Disk -> OS Page Cache -> JVM Heap -> Socket Buffer -> NIC drayveriga (4 marta nusxalash va 4 ta kontekst almashinuvi) o'tadi. `DefaultFileRegion` esa Linux dagi `sendfile` tizim chaqiruvini faollashtiradi: ma'lumot to'g'ridan-to'g'ri Page Cache dan Tarmoq kartasi buferiga (DMA orqali) o'tadi. CPU umuman xotira nusxalamaydi (Zero CPU-copy).

---

### Topshiriq #1145: UDP Multicast va Broadcast: Netty DatagramPacket Yordamida Signallar Tarqatish
**Tavsif:** Katta klasterdagi tugunlar bir-birini avtomatik topishi (Service Discovery) yoki birja narxlarini mahalliy tarmoqdagi barcha serverlarga bir paytda yuborish uchun UDP Multicast/Broadcast kanallarini boshqarish lozim.
**Talablar:** NioDatagramChannel, DatagramPacket, Multicast guruhiga qo'shilish (joinGroup) va paketlarni filtrlash.
**Yechim (Java):**
```java
package com.khorazmiy.network.multicast;

import io.netty.bootstrap.Bootstrap;
import io.netty.buffer.Unpooled;
import io.netty.channel.*;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.DatagramPacket;
import io.netty.channel.socket.InternetProtocolFamily;
import io.netty.channel.socket.nio.NioDatagramChannel;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.NetworkInterface;
import java.nio.charset.StandardCharsets;

/**
 * UDP Multicast orqali xabarlarni tarqatish va qabul qilish moduli.
 */
public class UdpMulticastClusterNode {
    private static final Logger log = LoggerFactory.getLogger(UdpMulticastClusterNode.class);

    private static final String MULTICAST_GROUP_IP = "239.255.255.250";
    private static final int PORT = 9999;

    public void startNode() throws Exception {
        EventLoopGroup group = new NioEventLoopGroup();

        Bootstrap b = new Bootstrap();
        b.group(group)
         .channelFactory(() -> new NioDatagramChannel(InternetProtocolFamily.IPv4))
         .option(ChannelOption.SO_REUSEADDR, true)
         .handler(new ChannelInitializer<NioDatagramChannel>() {
             @Override
             protected void initChannel(NioDatagramChannel ch) {
                 ch.pipeline().addLast(new SimpleChannelInboundHandler<DatagramPacket>() {
                     @Override
                     protected void channelRead0(ChannelHandlerContext ctx, DatagramPacket packet) {
                         String content = packet.content().toString(StandardCharsets.UTF_8);
                         log.info("Multicast xabari qabul qilindi: {} (Yuboruvchi: {})", 
                                  content, packet.sender());
                     }
                 });
             }
         });

        NioDatagramChannel ch = (NioDatagramChannel) b.bind(PORT).sync().channel();

        // Multicast guruhiga ulanish
        InetAddress groupAddr = InetAddress.getByName(MULTICAST_GROUP_IP);
        NetworkInterface networkInterface = NetworkInterface.getByInetAddress(InetAddress.getLocalHost());
        ch.joinGroup(new InetSocketAddress(groupAddr, PORT), networkInterface).sync();
        log.info("Multicast guruhiga ulandi: {}", MULTICAST_GROUP_IP);

        // Barcha tugunlarga signal yuborish
        DatagramPacket signal = new DatagramPacket(
                Unpooled.copiedBuffer("NODE_PING: Yangi tugun faollashdi", StandardCharsets.UTF_8),
                new InetSocketAddress(groupAddr, PORT)
        );
        ch.writeAndFlush(signal);
    }
}
```
**Tushuntirish:** UDP Multicast tarmoq kalitlari (Network Switch) yordamida bitta yuborilgan paketni apparat darajasida ko'paytirib faqat guruhga obuna bo'lgan tugunlarga yetkazib beradi. Bu 100 ta serverga alohida 100 ta TCP ulanish ochish o'rniga tarmoq yukini 100 barobarga kamaytiradi.

---

### Topshiriq #1146: Custom Binary Network Protocol: Magic Byte, Command ID, CRC32 Checksum va Paket Validatsiyasi
**Tavsif:** Yuqori xavfsizlik talab qilinadigan bank va sanoat tarmoqlarida HTTP yoki JSON o'rniga maxsus binar protokollar ishlatiladi. Paket yaxlitligini buzilishlardan va soxtalashtirishlardan saqlovchi CRC32 nazorat summasiga ega to'liq kodlash/dekodlash tizimi talab qilinadi.
**Talablar:** Magic number (2 bayt), Versiya (1 bayt), Command ID (2 bayt), Body Length (4 bayt), CRC32 (4 bayt) va Body tuzilishi.
**Yechim (Java):**
```java
package com.khorazmiy.network.customproto;

import io.netty.buffer.ByteBuf;
import io.netty.channel.ChannelHandlerContext;
import io.netty.handler.codec.ByteToMessageCodec;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.zip.CRC32;

/**
 * CRC32 yaxlitlik tekshiruviga ega maxsus sanoat binar protokoli.
 */
public class SecureBinaryProtocolCodec extends ByteToMessageCodec<SecureBinaryProtocolCodec.Packet> {
    private static final Logger log = LoggerFactory.getLogger(SecureBinaryProtocolCodec.class);

    private static final short MAGIC_NUMBER = (short) 0xABCD;
    private static final byte PROTOCOL_VERSION = 1;

    public record Packet(short commandId, String payload) {}

    @Override
    protected void encode(ChannelHandlerContext ctx, Packet msg, ByteBuf out) {
        byte[] payloadBytes = msg.payload().getBytes(StandardCharsets.UTF_8);

        // CRC32 hisoblash
        CRC32 crc = new CRC32();
        crc.update(payloadBytes);
        long checksum = crc.getValue();

        // Binar freymni shakllantirish
        out.writeShort(MAGIC_NUMBER);          // 2 bayt
        out.writeByte(PROTOCOL_VERSION);      // 1 bayt
        out.writeShort(msg.commandId());       // 2 bayt
        out.writeInt(payloadBytes.length);     // 4 bayt
        out.writeInt((int) checksum);          // 4 bayt CRC32
        out.writeBytes(payloadBytes);          // Tana baytlari
    }

    @Override
    protected void decode(ChannelHandlerContext ctx, ByteBuf in, List<Object> out) {
        // Kamida sarlavha (13 bayt) yetib kelganligini tekshirish
        if (in.readableBytes() < 13) {
            return;
        }

        in.markReaderIndex();
        short magic = in.readShort();
        if (magic != MAGIC_NUMBER) {
            log.error("Protokol xatosi: Magic number mos emas! ({})", Integer.toHexString(magic));
            ctx.close();
            return;
        }

        byte version = in.readByte();
        short commandId = in.readShort();
        int bodyLength = in.readInt();
        int expectedCrc = in.readInt();

        if (in.readableBytes() < bodyLength) {
            // Tana to'liq kelmagan, o'qish ko'rsatkichini qaytarish
            in.resetReaderIndex();
            return;
        }

        byte[] body = new byte[bodyLength];
        in.readBytes(body);

        // CRC32 ni qayta hisoblash va solishtirish
        CRC32 crc = new CRC32();
        crc.update(body);
        if ((int) crc.getValue() != expectedCrc) {
            log.error("Tarmoqda paket buzilgan! CRC32 mos kelmadi.");
            ctx.close();
            return;
        }

        String payload = new String(body, StandardCharsets.UTF_8);
        out.add(new Packet(commandId, payload));
    }
}
```
**Tushuntirish:** Binar paket formati ortiqcha maydonlarni olib tashlaydi va xabar o'lchamini minimal qiladi. `CRC32` nazorat summasi tarmoq apparatidagi xatolar yoki paket buzilishlarini bir zumda fosh etadi. `in.markReaderIndex()` va `resetReaderIndex()` to'liq paket kelmaganda o'qish ko'rsatkichini boshiga qaytarib, TCP paket bo'linishini to'g'ri boshqaradi.

---

### Topshiriq #1147: Proxy Protocol Qo'llab-quvvatlash: HAProxy PROXY Protocol v1/v2 Bilan Asl Mijoz IP Manzilini Olish
**Tavsif:** HAProxy, AWS ALB yoki Nginx orqasida turgan Netty server mijozning haqiqiy IP manzilini ko'ra olmaydi (chunki barcha TCP ulanishlar proksi serverdan keladi). HAProxy PROXY Protocol v1/v2 ni Netty da integratsiya qilish zarur.
**Talablar:** HAProxyMessageDecoder, HAProxyMessage ni o'qish va asl mijozning manzilini kanal atributiga biriktirish.
**Yechim (Java):**
```java
package com.khorazmiy.network.proxy;

import io.netty.channel.*;
import io.netty.handler.codec.haproxy.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * HAProxy PROXY protokolini dekodlovchi va asl mijoz IP sini aniqlovchi modul.
 */
public class HaProxyProtocolInitializer extends ChannelInitializer<Channel> {
    private static final Logger log = LoggerFactory.getLogger(HaProxyProtocolInitializer.class);

    @Override
    protected void initChannel(Channel ch) {
        ChannelPipeline p = ch.pipeline();

        // 1. PROXY protocol v1 va v2 ni avtomatik aniqlovchi dekoder
        p.addLast("haproxyDecoder", new HAProxyMessageDecoder());

        // 2. Proksi xabarini o'qib, mijoz haqiqiy IP sini aniqlovchi handler
        p.addLast("haproxyHandler", new SimpleChannelInboundHandler<HAProxyMessage>() {
            @Override
            protected void channelRead0(ChannelHandlerContext ctx, HAProxyMessage msg) {
                String realClientIp = msg.sourceAddress();
                int realClientPort = msg.sourcePort();

                log.info("HAProxy orqali asl mijoz IP aniqlandi: {}:{}", realClientIp, realClientPort);

                // Asl IP manzilni kanal atributiga yozish
                ctx.channel().attr(io.netty.util.AttributeKey.valueOf("REAL_IP")).set(realClientIp);

                // Proksi sarlavhasi faqat ulanish boshida 1 marta keladi, uni quvurdan olib tashlaymiz
                ctx.pipeline().remove(this);
            }
        });
    }
}
```
**Tushuntirish:** PROXY Protocol (v1 matnli, v2 binar) Layer 4 load balancer-larga TCP ulanish boshida asl mijozning haqiqiy IP va portini o'z ichiga olgan kichik sarlavha yuborish imkonini beradi. `HAProxyMessageDecoder` bu sarlavhani o'qigach, o'zini pipeline-dan olib tashlaydi va keyingi barcha ma'lumotlar asl maqsadda qayta ishlanadi.

---

### Topshiriq #1148: gRPC va Netty Metrics: Micrometer va Prometheus Bilan Tarmoq Monitoringi
**Tavsif:** Ishlab chiqarish muhitida tarmoq o'tkazuvchanligi, har bir RPC metodining bajarilish vaqti (latensiya) va xatoliklar sonini real vaqtda kuzatib borish uchun Micrometer va Prometheus integratsiyasini qurish lozim.
**Talablar:** MeterRegistry, Timer, Counter, gRPC ServerInterceptor orqali p95, p99 latensiyalarni o'lchash.
**Yechim (Java):**
```java
package com.khorazmiy.network.metrics;

import io.grpc.*;
import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Timer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.concurrent.TimeUnit;

/**
 * gRPC va tarmoq chaqiruvlari uchun Micrometer / Prometheus monitoring interceptori.
 */
public class MetricsMonitoringInterceptor implements ServerInterceptor {
    private static final Logger log = LoggerFactory.getLogger(MetricsMonitoringInterceptor.class);

    private final MeterRegistry registry;

    public MetricsMonitoringInterceptor(MeterRegistry registry) {
        this.registry = registry;
    }

    @Override
    public <ReqT, RespT> ServerCall.Listener<ReqT> interceptCall(
            ServerCall<ReqT, RespT> call, Metadata headers, ServerCallHandler<ReqT, RespT> next) {

        String methodName = call.getMethodDescriptor().getFullMethodName();
        long startTime = System.nanoTime();

        return new ForwardingServerCallListener.SimpleForwardingServerCallListener<>(
                next.startCall(new ForwardingServerCall.SimpleForwardingServerCall<>(call) {
                    @Override
                    public void close(Status status, Metadata trailers) {
                        long durationNano = System.nanoTime() - startTime;
                        
                        // Metrikani qayd qilish
                        Timer.builder("grpc.server.call.duration")
                                .tag("method", methodName)
                                .tag("status", status.getCode().name())
                                .register(registry)
                                .record(durationNano, TimeUnit.NANOSECONDS);

                        Counter.builder("grpc.server.call.total")
                                .tag("method", methodName)
                                .tag("status", status.getCode().name())
                                .register(registry)
                                .increment();

                        log.debug("Metrika yozildi: Method={}, Duration={}ms", 
                                  methodName, durationNano / 1_000_000.0);

                        super.close(status, trailers);
                    }
                }, headers)) {};
    }
}
```
**Tushuntirish:** `ForwardingServerCall.close()` metodi chaqirilishi so'rov to'liq yakunlangani va mijozga javob yetkazilganini bildiradi. Nano-sekund aniqligida o'lchangan vaqt Prometheus orqali Grafana panellarida p50, p95 va p99 kechikish persentillari sifatida aks ettiriladi.

---

### Topshiriq #1149: Circuit Breaker va Dynamic Throttle Tarmoq Darajasida: Resilience4j va Netty Integratsiyasi
**Tavsif:** Quyi mikroservislarda nosozlik yuz berganda barcha kiruvchi tarmoq so'rovlarini to'xtatib turish va kaskadli qulashning oldini olish uchun Netty ChannelHandler darajasida Circuit Breaker va Dynamic Throttle mexanizmini o'rnatish lozim.
**Talablar:** CircuitBreaker (CLOSED, OPEN, HALF_OPEN holatlari), tezkor Fail-Fast rad javobini qaytarish.
**Yechim (Java):**
```java
package com.khorazmiy.network.resilience;

import io.github.resilience4j.circuitbreaker.CircuitBreaker;
import io.github.resilience4j.circuitbreaker.CircuitBreakerConfig;
import io.netty.channel.ChannelFutureListener;
import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.SimpleChannelInboundHandler;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.Duration;

/**
 * Netty soket darajasidagi Circuit Breaker himoyachisi.
 */
public class NetworkCircuitBreakerHandler extends SimpleChannelInboundHandler<Object> {
    private static final Logger log = LoggerFactory.getLogger(NetworkCircuitBreakerHandler.class);

    private static final CircuitBreaker circuitBreaker;

    static {
        CircuitBreakerConfig config = CircuitBreakerConfig.custom()
                .failureRateThreshold(50.0f) // 50% xatolik bo'lsa zanjirni uzish
                .waitDurationInOpenState(Duration.ofSeconds(10)) // 10 soniya kutish
                .slidingWindowSize(20)
                .build();
        circuitBreaker = CircuitBreaker.of("networkServiceBreaker", config);
    }

    @Override
    protected void channelRead0(ChannelHandlerContext ctx, Object msg) {
        // Zanjir ochiqligini (Circuit Breaker OPEN) tekshirish
        if (!circuitBreaker.tryAcquirePermission()) {
            log.warn("Circuit Breaker OCHIQ holatda! So'rov rad etildi (Fail-Fast): {}", ctx.channel().remoteAddress());
            ctx.writeAndFlush("ERROR: 503 Xizmat vaqtincha mavjud emas (Circuit Breaker Open)\n")
               .addListener(ChannelFutureListener.CLOSE);
            return;
        }

        long start = System.currentTimeMillis();
        try {
            // Biznes handlerga uzatish
            ctx.fireChannelRead(msg);
            circuitBreaker.onSuccess(System.currentTimeMillis() - start, java.util.concurrent.TimeUnit.MILLISECONDS);
        } catch (Exception ex) {
            circuitBreaker.onError(System.currentTimeMillis() - start, java.util.concurrent.TimeUnit.MILLISECONDS, ex);
            throw ex;
        }
    }
}
```
**Tushuntirish:** Circuit Breaker OPEN holatiga o'tganda, so'rovlar quyi servisga yuborilmasdan, tarmoq darajasidayoq bir necha mikrosekund ichida 503 javobi bilan qaytariladi. Bu xizmatning tiklanib olishiga vaqt beradi va butun infratuzilmaning zanjirli qulashini (cascading failure) to'xtatadi.

---

### Topshiriq #1150: Distributed Event-Driven Network Gateway: Netty, gRPC va WebSockets Gibrid Shlyuzi
**Tavsif:** Zamonaviy FinTech platformasida tashqi mijozlar WebSocket orqali real-vaqt ma'lumotlarini kuzatadi, REST mijozlar HTTP/2 orqali murojaat qiladi, ichki mikroxizmatlar esa yuqori unumli gRPC orqali muloqot qiladi. Ushbu barcha protokollarni birlashtiruvchi markaziy asinxron shlyuz (API Gateway) yaratish talab etiladi.
**Talablar:** Netty Core, Dynamic Protocol Detection (WebSocket vs HTTP vs gRPC), EventLoop taqsimoti, yagona asinxron marshrutlash va monitoring.
**Yechim (Java):**
```java
package com.khorazmiy.network.gateway;

import io.netty.bootstrap.ServerBootstrap;
import io.netty.buffer.ByteBuf;
import io.netty.channel.*;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.SocketChannel;
import io.netty.channel.socket.nio.NioServerSocketChannel;
import io.netty.handler.codec.http.HttpObjectAggregator;
import io.netty.handler.codec.http.HttpServerCodec;
import io.netty.handler.codec.http.websocketx.WebSocketServerProtocolHandler;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Netty, gRPC va WebSocket protokollarini birlashtiruvchi
 * yuqori unumdor Gibrid Tarmoq Shlyuzi (Network Gateway).
 */
public class HybridNetworkGateway {
    private static final Logger log = LoggerFactory.getLogger(HybridNetworkGateway.class);

    private final int port;

    public HybridNetworkGateway(int port) {
        this.port = port;
    }

    public void start() throws InterruptedException {
        EventLoopGroup bossGroup = new NioEventLoopGroup(1);
        EventLoopGroup workerGroup = new NioEventLoopGroup();

        try {
            ServerBootstrap b = new ServerBootstrap();
            b.group(bossGroup, workerGroup)
             .channel(NioServerSocketChannel.class)
             .childOption(ChannelOption.TCP_NODELAY, true)
             .childOption(ChannelOption.SO_KEEPALIVE, true)
             .childHandler(new ChannelInitializer<SocketChannel>() {
                 @Override
                 protected void initChannel(SocketChannel ch) {
                     ChannelPipeline p = ch.pipeline();
                     // Protokolni dinamik aniqlovchi detektor (Protokol sniffer)
                     p.addLast("protocolDetector", new DynamicProtocolDetector());
                 }
             });

            ChannelFuture f = b.bind(port).sync();
            log.info("Khorazmiy AI Gibrid Tarmoq Shlyuzi {} portida to'liq ishga tushdi", port);
            f.channel().closeFuture().sync();
        } finally {
            bossGroup.shutdownGracefully();
            workerGroup.shutdownGracefully();
        }
    }

    // Paketning birinchi bir necha baytiga qarab protokolni aniqlovchi handler
    private static class DynamicProtocolDetector extends ChannelInboundHandlerAdapter {
        @Override
        public void channelRead(ChannelHandlerContext ctx, Object msg) {
            ByteBuf in = (ByteBuf) msg;

            if (in.readableBytes() < 5) {
                return; // Kamida 5 bayt kutiladi
            }

            // Sehrli baytlarni tekshirish
            int magic1 = in.getUnsignedByte(in.readerIndex());
            int magic2 = in.getUnsignedByte(in.readerIndex() + 1);

            ChannelPipeline p = ctx.pipeline();

            if (isHttp(magic1, magic2)) {
                log.info("HTTP / WebSocket mijozi aniqlandi: {}", ctx.channel().remoteAddress());
                p.addLast(new HttpServerCodec());
                p.addLast(new HttpObjectAggregator(65536));
                p.addLast(new WebSocketServerProtocolHandler("/gateway/ws", null, true));
                p.addLast(new GatewayBusinessHandler());
            } else {
                log.info("Binar / gRPC ulanishi aniqlandi: {}", ctx.channel().remoteAddress());
                p.addLast(new GatewayBusinessHandler());
            }

            // Ushbu detektorni pipeline dan chiqarib, baytlarni yangi handlerlarga topshirish
            p.remove(this);
            ctx.fireChannelRead(msg);
        }

        private boolean isHttp(int m1, int m2) {
            // 'GET', 'POST', 'HEAD', 'PUT' kabi HTTP metodlarining boshlanishi
            return (m1 == 'G' && m2 == 'E') ||
                   (m1 == 'P' && m2 == 'O') ||
                   (m1 == 'P' && m2 == 'U') ||
                   (m1 == 'H' && m2 == 'E');
        }
    }

    private static class GatewayBusinessHandler extends ChannelInboundHandlerAdapter {
        @Override
        public void channelRead(ChannelHandlerContext ctx, Object msg) {
            log.debug("Shlyuz ma'lumotni ichki xizmatlarga marshrutladi");
            // Asinxron marshrutlash va qayta ishlash
        }
    }

    public static void main(String[] args) throws Exception {
        new HybridNetworkGateway(8080).start();
    }
}
```
**Tushuntirish:** Gibrid shlyuz bitta ommaviy port ustida turli protokollarni dinamik ajratib oladi (Protocol Sniffing). Birinchi baytlar asosida HTTP/WebSocket yoki binar gRPC protokoli aniqlanib, tegishli pipeline dinamik tarzda tuziladi. Natijada yuzlab turli xil klientlar (veb-brauzerlar, mobil ilovalar, IoT qurilmalari va ichki servislar) yagona markazlashgan, xavfsiz va yuqori unumli shlyuz orqali ulanadi.
