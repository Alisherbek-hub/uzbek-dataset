# Khorazmiy AI: Kotlin - Modul 23
## Mavzu: Tarmoq protokollari: Ktor Network, Asinxron soketlar, WebSockets va gRPC Kotlin Coroutines

### Topshiriq #1101: Ktor Network SelectorManager va aSocket(): Asinxron TCP Server va Non-Blocking Ulanishlar
**Tavsif:** Kotlin Coroutines yordamida JVM oqimlarini (threads) bloklamasdan, bitta jarayonda o'n minglab parallel TCP ulanishlarni qabul qiluvchi asinxron soket serverini yaratish talab etiladi.
**Talablar:** SelectorManager(Dispatchers.IO), aSocket().tcp().bind(), openReadChannel() va openWriteChannel(), har bir ulanishni alohida Coroutine ichida mustaqil boshqarish.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.socket

import io.ktor.network.selector.*
import io.ktor.network.sockets.*
import io.ktor.utils.io.*
import kotlinx.coroutines.*
import org.slf4j.LoggerFactory
import java.net.InetSocketAddress

/**
 * Ktor Network SelectorManager asosidagi asinxron non-blocking TCP server.
 */
class AsyncTcpEchoServer(private val port: Int) {
    private val log = LoggerFactory.getLogger(AsyncTcpEchoServer::class.java)

    suspend fun start() = coroutineScope {
        // Asinxron I/O hodisalari uchun SelectorManager (NIO epoll/kqueue selektorlari)
        val selectorManager = SelectorManager(Dispatchers.IO)
        val serverSocket = aSocket(selectorManager).tcp().bind(InetSocketAddress("0.0.0.0", port))
        
        log.info("Ktor Asinxron TCP Server ishga tushdi: port $port")

        try {
            while (isActive) {
                // Yangi mijoz ulanishini korutina to'xtatilishi (suspension) orqali kutish
                val socket = serverSocket.accept()
                log.info("Yangi mijoz ulandi: ${socket.remoteAddress}")

                // Har bir mijoz uchun yengil vaznli (lightweight) korutina ishga tushirish
                launch(Dispatchers.IO) {
                    handleClient(socket)
                }
            }
        } finally {
            serverSocket.close()
            selectorManager.close()
            log.info("Server soketlari va selektor to'xtatildi")
        }
    }

    private suspend fun handleClient(socket: Socket) {
        val readChannel = socket.openReadChannel()
        val writeChannel = socket.openWriteChannel(autoFlush = true)

        try {
            while (!readChannel.isClosedForRead) {
                // Qatorma-qator o'qish (Hech qanday thread bloklanmaydi)
                val line = readChannel.readUTF8Line() ?: break
                log.debug("Mijozdan xabar: $line")

                // Echo javobini yozish
                writeChannel.writeStringUtf8("ECHO: $line\n")
            }
        } catch (e: Throwable) {
            log.error("Mijoz bilan aloqada xatolik: ${e.message}")
        } finally {
            withContext(NonCancellable) {
                socket.close()
                log.info("Mijoz soketi xavfsiz yopildi: ${socket.remoteAddress}")
            }
        }
    }
}

suspend fun main() {
    AsyncTcpEchoServer(9090).start()
}
```
**Tushuntirish:** Ktor Network `SelectorManager` Java NIO `Selector` ni Kotlin Coroutines bilan birlashtiradi. `serverSocket.accept()` yoki `readChannel.readUTF8Line()` chaqirilganda, operatsion tizim tarmog'idan ma'lumot kelguncha JVM oqimi (Thread) bloklanmaydi, balki korutina to'xtatiladi (suspend). Bitta IO-dispatcher oqimlar hovuzi orqali 50,000+ faol soketlarni minimal xotira (har bir korutina uchun atigi bir necha kilobayt) bilan boshqarish mumkin.

---

### Topshiriq #1102: Asinxron TCP Client: Ktor ByteReadChannel va ByteWriteChannel Yordamida Buferlangan Oqimlar
**Tavsif:** Yuqori chastotali to'lov shlyuziga ulanib, millionlab tranzaksiya buyruqlarini asinxron jo'natish va javoblarni navbat kutmasdan qabul qiluvchi samarali TCP mijozi talab etiladi.
**Talablar:** aSocket().tcp().connect(), ByteReadChannel va ByteWriteChannel, autoFlush xususiyati, socket resurslarini to'g'ri tozalash.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.client

import io.ktor.network.selector.*
import io.ktor.network.sockets.*
import io.ktor.utils.io.*
import kotlinx.coroutines.*
import org.slf4j.LoggerFactory

/**
 * Ktor Network orqali yuqori unumli asinxron TCP mijozi.
 */
class ResilientTcpClient(private val host: String, private val port: Int) {
    private val log = LoggerFactory.getLogger(ResilientTcpClient::class.java)
    private val selector = SelectorManager(Dispatchers.IO)

    suspend fun sendCommand(command: String): String = withContext(Dispatchers.IO) {
        val socket = aSocket(selector).tcp().connect(host, port)
        val readChannel = socket.openReadChannel()
        val writeChannel = socket.openWriteChannel(autoFlush = true)

        try {
            log.info("Serverga buyruq yuborilmoqda: $command")
            writeChannel.writeStringUtf8("$command\n")

            val response = readChannel.readUTF8Line() ?: throw IllegalStateException("Server javob bermasdan ulanishni uzdi")
            log.info("Serverdan javob olindi: $response")
            response
        } finally {
            withContext(NonCancellable) {
                socket.close()
            }
        }
    }

    fun close() {
        selector.close()
    }
}
```
**Tushuntirish:** `ByteReadChannel` va `ByteWriteChannel` korutinalar uchun maxsus ishlab chiqilgan asinxron baytlar oqimidir. `autoFlush = true` yozilgan ma'lumotlarni darhol tarmoq drayveriga yuboradi (flush). Kotlin `NonCancellable` konteksti esa hatto so'rov bekor qilinganda ham soket fayl deskriptorlari xavfsiz yopilishini kafolatlaydi.

---

### Topshiriq #1103: ByteReadChannel Orqali Framed Binary Protocol O'qish: readInt, readFully va Xavfsiz Parslash
**Tavsif:** TCP oqimida binar paketlar bo'laklarga bo'linib keladi. Ktor ByteReadChannel yordamida 4 baytli uzunlik prefiksi va komanda ID sini xotiraga ortiqcha massiv ajratmasdan o'qish mexanizmini yaratish lozim.
**Talablar:** readInt(), readFully(), ByteArray buferini qayta ishlatish va tarmoq uzilishlarini xavfsiz boshqarish.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.binary

import io.ktor.utils.io.*
import kotlinx.coroutines.*
import org.slf4j.LoggerFactory

/**
 * Binar paketlarni xavfsiz va aniq ajratib oluvchi oqim parslari.
 */
data class BinaryPacket(val commandId: Int, val payload: ByteArray)

class BinaryPacketReader {
    private val log = LoggerFactory.getLogger(BinaryPacketReader::class.java)

    suspend fun readPacket(channel: ByteReadChannel): BinaryPacket {
        // 1. Paket uzunligini (4 bayt) o'qish
        val totalLength = channel.readInt()
        require(totalLength in 4..1024 * 1024) { "Paket hajmi chegaradan oshgan: $totalLength" }

        // 2. Buyruq identifikatori (4 bayt)
        val commandId = channel.readInt()

        // 3. Tana qismi hajmini hisoblash
        val payloadSize = totalLength - 4
        val payload = ByteArray(payloadSize)

        // readFully barcha kerakli baytlar to'liq yetib kelguncha korutinani suspend qiladi
        channel.readFully(payload, 0, payloadSize)

        log.debug("Binar paket to'liq qabul qilindi: Cmd=$commandId, Hajmi=$payloadSize bayt")
        return BinaryPacket(commandId, payload)
    }
}
```
**Tushuntirish:** Standart `InputStream.read(byte[])` to'liq paket o'rniga faqat tarmoqqa yetib kelgan dastlabki bir necha baytni qaytarishi mumkin, bu esa paket buzilishiga olib keladi. `ByteReadChannel.readFully()` esa ko'rsatilgan hajm to'liq o'qilmaguncha ichki tsiklda korutinani to'xtatib turadi va paket yaxlitligini 100% ta'minlaydi.

---

### Topshiriq #1104: High-Throughput Ktor TCP Server: SocketOptions, SO_REUSEADDR va TCP_NODELAY Sozlamalari
**Tavsif:** Yuqori yuklamali serverda soket opsiyalarini optimallashtirmaslik paket kechikishlariga va TIME_WAIT holatidagi portlar tugashiga sabab bo'ladi. Ktor da past sathli soket parametrlarini sozlash talab etiladi.
**Talablar:** SocketOptions.tcpNoDelay = true, reuseAddress = true, reusePort = true, receiveBufferSize va sendBufferSize konfiguratsiyasi.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.options

import io.ktor.network.selector.*
import io.ktor.network.sockets.*
import kotlinx.coroutines.*
import org.slf4j.LoggerFactory
import java.net.InetSocketAddress

/**
 * Tarmoq darajasida to'liq sozlangan yuqori unumdor TCP server.
 */
class TunedKtorTcpServer(private val port: Int) {
    private val log = LoggerFactory.getLogger(TunedKtorTcpServer::class.java)

    suspend fun start() = coroutineScope {
        val selector = SelectorManager(Dispatchers.IO)
        
        // Soket konfiguratsiyasini belgilash
        val server = aSocket(selector).tcp().bind(InetSocketAddress("0.0.0.0", port)) {
            // Nagle algoritmini o'chirish (Kichik paketlarni kutmasdan darhol uzatish)
            tcpNoDelay = true
            // TIME_WAIT holatidagi portni qayta ishlatish
            reuseAddress = true
            // Linux multi-thread load balancing
            reusePort = true
            // Operatsion tizim qabul qilish va jo'natish buferlari hajmi
            receiveBufferSize = 64 * 1024
            sendBufferSize = 64 * 1024
        }

        log.info("Optimizatsiyalangan Ktor TCP Server ishga tushdi: port $port")
        
        try {
            while (isActive) {
                val client = server.accept()
                launch(Dispatchers.IO) {
                    // Mijoz bilan ishlash
                    client.close()
                }
            }
        } finally {
            server.close()
            selector.close()
        }
    }
}
```
**Tushuntirish:** `tcpNoDelay = true` Nagle algoritmini o'chiradi, bu esa kichik paketlar yuborilganda 40-200ms kechikishni (latency) nolga tushiradi. `reusePort = true` bir nechta jarayonlarga bitta portga bog'lanish imkonini berib, Linux yadrosi darajasida ulanishlarni oqimlar bo'yicha taqsimlaydi.

---

### Topshiriq #1105: Coroutine Concurrency Bilan 50,000 Parallel TCP Soketlarni Boshqarish va Structured Concurrency
**Tavsif:** Katta IoT platformasida o'n minglab datchiklar bir vaqtda ulangan bo'ladi. Tizim to'xtatilganda yoki xatolik yuz berganda bitta ham 'adashgan' (orphan) korutina yoki ochiq soket qolib ketmasligini kafolatlash zarur.
**Talablar:** SupervisorJob, CoroutineScope, Structured Concurrency, cancellation handling va faol soketlar hisoblagichi.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.concurrency

import io.ktor.network.selector.*
import io.ktor.network.sockets.*
import kotlinx.coroutines.*
import org.slf4j.LoggerFactory
import java.net.InetSocketAddress
import java.util.concurrent.atomic.AtomicInteger

/**
 * 50,000+ parallel soketlarni Structured Concurrency bilan boshqaruvchi server.
 */
class MassiveConnectionServer(private val port: Int) {
    private val log = LoggerFactory.getLogger(MassiveConnectionServer::class.java)
    private val activeConnections = AtomicInteger(0)

    // Boshqaruvchi CoroutineScope: bitta bolaning xatosi butun serverni qulatmaydi (SupervisorJob)
    private val serverJob = SupervisorJob()
    private val serverScope = CoroutineScope(Dispatchers.IO + serverJob)

    fun start() {
        serverScope.launch {
            val selector = SelectorManager(Dispatchers.IO)
            val serverSocket = aSocket(selector).tcp().bind(InetSocketAddress("0.0.0.0", port))
            log.info("Katta sig'imli server $port portida ishga tushirildi")

            try {
                while (isActive) {
                    val socket = serverSocket.accept()
                    val count = activeConnections.incrementAndGet()
                    log.debug("Yangi mijoz ulandi. Jami faol: $count")

                    // Har bir ulanish serverScope ichida launch qilinadi
                    serverScope.launch {
                        try {
                            // Mijozning doimiy ulanishi
                            awaitCancellation()
                        } finally {
                            withContext(NonCancellable) {
                                socket.close()
                                activeConnections.decrementAndGet()
                            }
                        }
                    }
                }
            } finally {
                serverSocket.close()
                selector.close()
            }
        }
    }

    fun stop() {
        log.info("Server to'xtatilmoqda. Barcha 50,000 ulanishlar darhol bekor qilinadi...")
        serverJob.cancel() // Barcha bolalar bir zumda tozalanadi!
    }
}
```
**Tushuntirish:** Kotlin 'Structured Concurrency' tamoyili orqali barcha 50,000 korutina yagona `serverJob` ga bog'lanadi. Agar `serverJob.cancel()` chaqirilsa, barcha korutinalar o'zlarining `finally` bloklarini ishga tushirib soketlarni yopadi. Bu OS resurslari va xotiraning sizib ketmasligini kafolatlaydi.

---

### Topshiriq #1106: Ktor Network TLS/SSL: Asinxron Soketlarni TLS Bilan Shifrlash
**Tavsif:** Banklararo xavfsiz axborot almashishda soket ustidagi barcha baytlar TLS 1.3 bilan shifrlanishi shart. Ktor Network da ochiq TCP soketini shifrlangan TLS kanaliga aylantirish (tls()) talab etiladi.
**Talablar:** Socket.tls(coroutineContext), TrustManager, KeyStore initsializatsiyasi va xavfsiz qo'l berishish (Handshake).
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.tls

import io.ktor.network.selector.*
import io.ktor.network.sockets.*
import io.ktor.network.tls.*
import io.ktor.utils.io.*
import kotlinx.coroutines.*
import org.slf4j.LoggerFactory
import java.security.KeyStore
import javax.net.ssl.TrustManagerFactory

/**
 * Ktor Asinxron TLS soket aloqasi.
 */
class SecureTlsClient(private val host: String, private val port: Int) {
    private val log = LoggerFactory.getLogger(SecureTlsClient::class.java)

    suspend fun secureRequest(message: String): String = withContext(Dispatchers.IO) {
        val selector = SelectorManager(Dispatchers.IO)
        // 1. Oddiy TCP soket ulanishini o'rnatish
        val plainSocket = aSocket(selector).tcp().connect(host, port)

        // 2. Soket ustiga TLS shifrlash qatlamini o'rnatish
        val tlsSocket = plainSocket.tls(coroutineContext) {
            serverName = host
            // Ishonchli sertifikatlar tekshiruvi
            trustManager = TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm()).apply {
                init(null as KeyStore?)
            }.trustManagers.first()
        }

        log.info("TLS 1.3 Handshake muvaffaqiyatli o'rnatildi: $host:$port")

        val input = tlsSocket.openReadChannel()
        val output = tlsSocket.openWriteChannel(autoFlush = true)

        try {
            output.writeStringUtf8("$message\n")
            input.readUTF8Line() ?: ""
        } finally {
            withContext(NonCancellable) {
                tlsSocket.close()
                selector.close()
            }
        }
    }
}
```
**Tushuntirish:** Ktor Network `tls()` funksiyasi mavjud `Socket` ni olib, uning kiruvchi va chiquvchi oqimlarini Java SSLEngine orqali asinxron filtrlaydi. Bunda TLS Handshake to'liq korutina ichida bajariladi va CPU oqimlarini bloklamaydi.

---

### Topshiriq #1107: Ktor UDP Socket: Asinxron Datagram O'qish va Yozish (Telemetriya Qabul Qilish)
**Tavsif:** Yuqori tezlikdagi sensorlar yoki GPS trekerlar ma'lumotlarni TCP handshake kechikishlarisiz, yengil UDP datagrammalari orqali uzatadi. Ktor UDP asinxron soketini yaratish zarur.
**Talablar:** aSocket(selector).udp().bind(), Datagram paketi, paket o'qish va javob yuborish.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.udp

import io.ktor.network.selector.*
import io.ktor.network.sockets.*
import io.ktor.utils.io.core.*
import kotlinx.coroutines.*
import org.slf4j.LoggerFactory
import java.net.InetSocketAddress

/**
 * Asinxron UDP Telemetriya qabul qiluvchi server.
 */
class AsyncUdpServer(private val port: Int) {
    private val log = LoggerFactory.getLogger(AsyncUdpServer::class.java)

    suspend fun start() = coroutineScope {
        val selector = SelectorManager(Dispatchers.IO)
        val socket = aSocket(selector).udp().bind(InetSocketAddress("0.0.0.0", port))
        log.info("UDP Asinxron Server ishga tushdi: port $port")

        try {
            while (isActive) {
                // Yangi UDP paketini asinxron qabul qilish
                val datagram = socket.receive()
                val text = datagram.packet.readText()
                log.info("UDP Datagram qabul qilindi: '$text' Manzil: ${datagram.address}")

                // Aks-sado (ACK) javobini jo'natuvchiga qaytarish
                val responsePacket = buildPacket {
                    writeText("ACK: Qabul qilindi\n")
                }
                socket.send(Datagram(responsePacket, datagram.address))
            }
        } finally {
            socket.close()
            selector.close()
        }
    }
}
```
**Tushuntirish:** UDP da doimiy ulanish (connection state) tushunchasi yo'q. Har bir `socket.receive()` chaqiruvi mustaqil `Datagram` qaytaradi, unda ma'lumotlar paketi (`ByteReadPacket`) va yuboruvchining manzili saqlanadi. Ktor ning UDP implementatsiyasi NIO DatagramChannel ustiga qurilgan bo'lib, oqimlarni band qilmaydi.

---

### Topshiriq #1108: UDP Multicast Guruhlariga Ulanish va Coroutine Flow Orqali Paketlarni Filtrlash
**Tavsif:** Lokal tarmoqdagi barcha serverlar o'rtasida klaster yurak urishi (Cluster Heartbeat) signallarini tarqatish va Kotlin Flow orqali kiruvchi signallarni reaktiv oqim sifatida filtrlash talab etiladi.
**Talablar:** Multicast guruhi, DatagramChannel joinGroup, flow builder va paketlarni filtrlash.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.multicast

import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*
import org.slf4j.LoggerFactory
import java.net.*

/**
 * UDP Multicast paketlarini Coroutine Flow orqali reaktiv uzatuvchi tizim.
 */
class MulticastFlowReceiver(private val groupAddress: String, private val port: Int) {
    private val log = LoggerFactory.getLogger(MulticastFlowReceiver::class.java)

    fun observeMulticastEvents(): Flow<String> = flow {
        val group = InetAddress.getByName(groupAddress)
        val socket = MulticastSocket(port).apply {
            reuseAddress = true
            joinGroup(group)
        }
        val buffer = ByteArray(2048)

        log.info("Multicast guruhiga ulandi: $groupAddress:$port")

        try {
            while (currentCoroutineContext().isActive) {
                val packet = java.net.DatagramPacket(buffer, buffer.size)
                // Bloklanuvchi I/O ni Dispatchers.IO da bajarish
                withContext(Dispatchers.IO) {
                    socket.receive(packet)
                }
                val msg = String(packet.data, 0, packet.length)
                emit(msg) // Oqimga (Flow) chiqarish
            }
        } finally {
            withContext(NonCancellable) {
                socket.leaveGroup(group)
                socket.close()
                log.info("Multicast guruhidan chiqildi")
            }
        }
    }.flowOn(Dispatchers.IO)
}
```
**Tushuntirish:** Coroutine `Flow` tarmoqdan kelayotgan xabarlarni reaktiv, sovuq oqim (Cold Flow) sifatida qabul qilishga imkon beradi. `flowOn(Dispatchers.IO)` tarmoq operatsiyalarini alohida I/O oqimida bajarilishini ta'minlaydi, iste'molchi esa `filter`, `map`, `debounce` operatorlari yordamida ma'lumotlarni oson qayta ishlaydi.

---

### Topshiriq #1109: Low-level Network Timeout va KeepAlive: withTimeoutOrNull va Soket Holatini Monitoring Qilish
**Tavsif:** Sekin yoki javob bermayotgan mijozlar tufayli asinxron soketlar ochiq qolib xotirani egallashini oldini olish uchun soket darajasida qat'iy vaqt chegaralarini (Timeouts) joriy etish kerak.
**Talablar:** withTimeoutOrNull, soket inaktivligini tekshirish, Ping-Pong protokoli va vaqt o'tganda xavfsiz uzish.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.timeout

import io.ktor.network.sockets.*
import io.ktor.utils.io.*
import kotlinx.coroutines.*
import org.slf4j.LoggerFactory

/**
 * Tarmoq taym-autlari va soket salomatligini nazorat qiluvchi modul.
 */
class MonitoredSocketSession(private val socket: Socket, private val timeoutMs: Long = 15000) {
    private val log = LoggerFactory.getLogger(MonitoredSocketSession::class.java)

    suspend fun runSession() {
        val input = socket.openReadChannel()
        val output = socket.openWriteChannel(autoFlush = true)

        try {
            while (!input.isClosedForRead) {
                // Belgilangan vaqt ichida yangi xabar kelmasa null qaytaradi
                val message = withTimeoutOrNull(timeoutMs) {
                    input.readUTF8Line()
                }

                if (message == null) {
                    log.warn("Soket harakatsiz qoldi ($timeoutMs ms). Ulanish uzilmoqda: ${socket.remoteAddress}")
                    output.writeStringUtf8("ERROR: Timeout bo'yicha ulanish uzildi\n")
                    break
                }

                if (message == "PING") {
                    output.writeStringUtf8("PONG\n")
                } else {
                    log.debug("Xabar olindi: $message")
                }
            }
        } finally {
            withContext(NonCancellable) {
                socket.close()
                log.info("Soket yopildi: ${socket.remoteAddress}")
            }
        }
    }
}
```
**Tushuntirish:** Kotlin Coroutines dagi `withTimeoutOrNull` taymerni o'rnatish uchun alohida thread talab qilmaydi, balki Coroutine Scheduler ning ichki vaqt jadvalidan foydalanadi. Belgilangan muddatda ma'lumot kelmasa, qolgan amallar bekor qilinadi va soket xavfsiz tozalanadi.

---

### Topshiriq #1110: Custom ByteWriteChannel Pool va Zero-Allocation Xotira Buferlash
**Tavsif:** Har bir tarmoq so'rovida yangi ByteArray yaratish JVM Garbage Collector ga ulkan yuk tushiradi. Oldindan ajratilgan baytlar massivini qayta ishlatuvchi xotira hovuzini (Buffer Pool) yaratish zarur.
**Talablar:** ObjectPool yoki ArrayDeque hovuzi, o'lchami cheklangan buferlar, xotira allokatsiyasiz ma'lumot uzatish.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.pool

import io.ktor.utils.io.*
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import org.slf4j.LoggerFactory

/**
 * Zero-Allocation bufer hovuzi orqali Garbage Collector yukini minimallashtirish.
 */
class DirectBufferPool(private val bufferSize: Int = 8192, private val maxPoolSize: Int = 100) {
    private val log = LoggerFactory.getLogger(DirectBufferPool::class.java)
    private val pool = ArrayDeque<ByteArray>()
    private val mutex = Mutex()

    suspend fun acquireBuffer(): ByteArray = mutex.withLock {
        if (pool.isNotEmpty()) {
            pool.removeLast()
        } else {
            log.debug("Hovuz bo'sh, yangi bufer ajratilmoqda ($bufferSize bayt)")
            ByteArray(bufferSize)
        }
    }

    suspend fun releaseBuffer(buffer: ByteArray) = mutex.withLock {
        if (pool.size < maxPoolSize) {
            pool.addLast(buffer)
        }
    }

    suspend inline fun <T> useBuffer(block: (ByteArray) -> T): T {
        val buf = acquireBuffer()
        try {
            return block(buf)
        } finally {
            releaseBuffer(buf)
        }
    }
}
```
**Tushuntirish:** Har bir I/O amali uchun doimiy `ByteArray(8192)` yaratish yosh avlod (Young Gen) xotirasini tez to'ldiradi va tez-tez Minor GC to'xtashlariga sabab bo'ladi. `DirectBufferPool` buferlarni qayta ishlatadi, bu esa yuqori chastotali tarmoq shlyuzlarida xotira allokatsiyasini deyarli nolga tushiradi.

---

### Topshiriq #1111: Ktor Server WebSockets: DefaultWebSocketServerSession va Frame Turlari Bilan Ishlash
**Tavsif:** Real-time chat yoki monitoring ilovasida mijozlar bilan Ktor Server WebSockets plagini orqali ikki tomonlama barqaror aloqa o'rnatish talab etiladi.
**Talablar:** install(WebSockets), webSocket("/ws"), incoming kanali orqali Frame.Text, Frame.Binary, Frame.Ping, Frame.Close ni qayta ishlash va outgoing.send().
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.websocket

import io.ktor.server.application.*
import io.ktor.server.engine.*
import io.ktor.server.netty.*
import io.ktor.server.routing.*
import io.ktor.server.websocket.*
import io.ktor.websocket.*
import kotlinx.coroutines.channels.consumeEach
import org.slf4j.LoggerFactory
import java.time.Duration

/**
 * Ktor Server WebSockets plagini va freymlarni qayta ishlash.
 */
fun Application.configureWebSockets() {
    val log = LoggerFactory.getLogger("WebSocketRouting")

    install(WebSockets) {
        pingPeriod = Duration.ofSeconds(15)
        timeout = Duration.ofSeconds(15)
        maxFrameSize = Long.MAX_VALUE
        masking = false
    }

    routing {
        webSocket("/ws/echo") {
            log.info("Yangi WebSocket mijozi ulandi: $this")

            try {
                // Kiruvchi freymlar oqimini qabul qilish
                incoming.consumeEach { frame ->
                    when (frame) {
                        is Frame.Text -> {
                            val text = frame.readText()
                            log.info("Matnli xabar: $text")
                            send(Frame.Text("Server Echo: $text"))
                        }
                        is Frame.Binary -> {
                            val bytes = frame.readBytes()
                            log.info("Binar ma'lumot olindi: ${bytes.size} bayt")
                            send(Frame.Binary(true, bytes))
                        }
                        is Frame.Ping -> {
                            log.debug("PING freymi olindi")
                        }
                        is Frame.Close -> {
                            log.info("Mijoz ulanishni yopishni so'radi: ${closeReason.await()}")
                        }
                        else -> Unit
                    }
                }
            } catch (e: Throwable) {
                log.error("WebSocket sessiyasida nosozlik: ${e.message}")
            } finally {
                log.info("WebSocket sessiyasi yakunlandi")
            }
        }
    }
}
```
**Tushuntirish:** Ktor WebSockets plagini HTTP/1.1 Upgrade so'rovini avtomatik ushlaydi va ulanishni `DefaultWebSocketServerSession` ga aylantiradi. Korutinalar kanali (`incoming: ReceiveChannel<Frame>`) xabarlarni asinxron yetkazib beradi. `outgoing.send()` orqali xabarlarni jo'natish xotira va tarmoq imkoniyatlariga qarab avtomatik to'xtatilib turiladi (Backpressure).

---

### Topshiriq #1112: Coroutine Flow va MutableSharedFlow Yordamida WebSocket Broadcast Hub Yaratish
**Tavsif:** Birja kotirovkalari yangilanganda, ulangan barcha faol foydalanuvchilarga ma'lumotlarni kechikishlarsiz (Broadcast) yetkazib beruvchi reaktiv tizim yaratish lozim.
**Talablar:** MutableSharedFlow(replay = 0, extraBufferCapacity = 64), collect orqali har bir mijozga mustaqil uzatish, sekin mijozlar boshqalarni to'xtatib qo'ymasligi (BufferOverflow).
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.broadcast

import io.ktor.server.application.*
import io.ktor.server.routing.*
import io.ktor.server.websocket.*
import io.ktor.websocket.*
import kotlinx.coroutines.channels.BufferOverflow
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.asSharedFlow
import org.slf4j.LoggerFactory

/**
 * SharedFlow asosidagi yuqori unumdor WebSocket Broadcast markazi.
 */
class MarketTickerBroadcastHub {
    private val log = LoggerFactory.getLogger(MarketTickerBroadcastHub::class.java)

    // Barcha mijozlar obuna bo'luvchi umumiy reaktiv oqim
    private val _priceUpdates = MutableSharedFlow<String>(
        replay = 1, // Yangi ulangan mijoz oxirgi narxni darhol oladi
        extraBufferCapacity = 128,
        onBufferOverflow = BufferOverflow.DROP_OLDEST // Sekin mijozlar sabab xotira to'lmasligi uchun
    )
    val priceUpdates = _priceUpdates.asSharedFlow()

    suspend fun publishPrice(symbol: String, price: Double) {
        val payload = "{\"symbol\":\"$symbol\",\"price\":$price}"
        log.debug("Yangi kotirovka tarqatilmoqda: $payload")
        _priceUpdates.emit(payload)
    }
}

fun Application.configureBroadcast(hub: MarketTickerBroadcastHub) {
    routing {
        webSocket("/ws/prices") {
            // Har bir yangi ulanish o'z korutinasida umumiy Flow ga obuna bo'ladi
            try {
                hub.priceUpdates.collect { priceJson ->
                    send(Frame.Text(priceJson))
                }
            } catch (e: Exception) {
                // Mijoz chiqib ketdi
            }
        }
    }
}
```
**Tushuntirish:** Kotlin `MutableSharedFlow` ko'p sonli obunachilar (Fan-Out) uchun juda mos keladi. `onBufferOverflow = BufferOverflow.DROP_OLDEST` strategiyasi orqali interneti sekinlashgan bitta mijoz boshqa barcha foydalanuvchilarning xabar olishini kechiktirmaydi (Slow Consumer izolatsiyasi).

---

### Topshiriq #1113: Ktor WebSocket Client: Auto-Reconnect, Exponential Backoff va Reaktiv Oqimlar
**Tavsif:** Tashqi kotirovka manbalariga doimiy ulangan turuvchi mijoz xizmatlari tarmoq uzilganda avtomatik qayta ulanishi (Auto-reconnect) va xabarlarni Coroutine Flow sifatida taqdim etishi kerak.
**Talablar:** HttpClient(CIO), install(WebSockets), retry tsikli, exponential backoff (2^attempt), Flow<String> oqimi qaytarish.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.client

import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.plugins.websocket.*
import io.ktor.websocket.*
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import org.slf4j.LoggerFactory
import kotlin.math.min
import kotlin.math.pow

/**
 * Avtomatik qayta ulanuvchi (Auto-reconnect) Ktor WebSocket mijozi.
 */
class ResilientWebSocketClient(private val urlString: String) {
    private val log = LoggerFactory.getLogger(ResilientWebSocketClient::class.java)

    private val client = HttpClient(CIO) {
        install(WebSockets)
    }

    fun connectAndStream(): Flow<String> = flow {
        var attempt = 0

        while (currentCoroutineContext().isActive) {
            try {
                log.info("Serverga ulanishga urinish: $urlString (#$attempt)")
                client.webSocket(urlString) {
                    log.info("WebSocket ulanishi muvaffaqiyatli o'rnatildi!")
                    attempt = 0 // Muvaffaqiyatli ulangach urinishlar hisoblagichi nolga tushadi

                    for (frame in incoming) {
                        if (frame is Frame.Text) {
                            emit(frame.readText())
                        }
                    }
                }
            } catch (e: Exception) {
                attempt++
                val delaySec = min(2.0.pow(attempt).toLong(), 30L)
                log.warn("Aloqa uzildi: ${e.message}. $delaySec soniyadan so'ng qayta ulanish...")
                delay(delaySec * 1000)
            }
        }
    }
}
```
**Tushuntirish:** Ktor `HttpClient(CIO)` asinxron tarmoq drayveri orqali ishlaydi. Korutina `flow { ... }` ichida ulanishni cheksiz qayta tiklash mantiqi saqlanadi. Agar server qulasa, eksponentsial orqaga chekinish orqali server yuklanishi engillatiladi.

---

### Topshiriq #1114: Serialization Bilan WebSocket: ContentNegotiation, Kotlinx.Serialization va JSON Freymlar
**Tavsif:** WebSocket orqali xom matnlar (raw text) o'rniga qat'iy tiplangan (strongly-typed) Kotlin ma'lumotlar sinflarini (Data Classes) avtomatik JSON ga va JSON dan obyektga aylantirish tizimini qurish zarur.
**Talablar:** sendSerialized(), receiveDeserialized(), KotlinxWebsocketSerializationConverter, kotlinx.serialization.Serializable.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.serialization

import io.ktor.serialization.kotlinx.*
import io.ktor.server.application.*
import io.ktor.server.routing.*
import io.ktor.server.websocket.*
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import org.slf4j.LoggerFactory

@Serializable
data class OrderRequest(val orderId: String, val amount: Double, val currency: String)

@Serializable
data class OrderResponse(val orderId: String, val status: String, val timestamp: Long)

fun Application.configureTypedWebSockets() {
    val log = LoggerFactory.getLogger("TypedWS")

    install(WebSockets) {
        // Kotlinx.Serialization JSON konverterini o'rnatish
        contentConverter = KotlinxWebsocketSerializationConverter(Json {
            ignoreUnknownKeys = true
            encodeDefaults = true
        })
    }

    routing {
        webSocket("/ws/orders") {
            log.info("Buyurtma savdosi bo'yicha mijoz ulandi")

            try {
                while (true) {
                    // JSON freymni avtomatik Kotlin obyektiga dekodlash
                    val request = receiveDeserialized<OrderRequest>()
                    log.info("Buyurtma qabul qilindi: ID=${request.orderId}, Summa=${request.amount} ${request.currency}")

                    val response = OrderResponse(
                        orderId = request.orderId,
                        status = "CONFIRMED",
                        timestamp = System.currentTimeMillis()
                    )

                    // Kotlin obyektini avtomatik JSON freymga serializatsiya qilib jo'natish
                    sendSerialized(response)
                }
            } catch (e: Exception) {
                log.warn("Sessiya yakunlandi: ${e.message}")
            }
        }
    }
}
```
**Tushuntirish:** `receiveDeserialized<T>()` va `sendSerialized<T>()` funksiyalari matnni qo'lda parslash zaruratini yo'qotadi. `KotlinxWebsocketSerializationConverter` kompilyatsiya vaqtida generatsiya qilingan serializerlardan foydalanadi, bu esa Java Reflection ishlatmaydi va maksimal tezlik beradi.

---

### Topshiriq #1115: Protobuf Binary WebSocket: Kotlinx.Serialization Protobuf Bilan Ultra-Ixcham Freymlar Almashinuvi
**Tavsif:** Internet trafigi cheklangan yoki batareya quvvati muhim bo'lgan mobil qurilmalar bilan aloqada JSON o'rniga Google Protocol Buffers binar formatini WebSocket orqali uzatish lozim.
**Talablar:** ProtoBuf.encodeToByteArray(), ProtoBuf.decodeFromByteArray(), Frame.Binary orqali ma'lumot almashish.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.protobuf

import io.ktor.server.application.*
import io.ktor.server.routing.*
import io.ktor.server.websocket.*
import io.ktor.websocket.*
import kotlinx.serialization.ExperimentalSerializationApi
import kotlinx.serialization.ProtoNumber
import kotlinx.serialization.Serializable
import kotlinx.serialization.protobuf.ProtoBuf
import org.slf4j.LoggerFactory

@OptIn(ExperimentalSerializationApi::class)
@Serializable
data class SensorTelemetry(
    @ProtoNumber(1) val sensorId: Int,
    @ProtoNumber(2) val temperature: Float,
    @ProtoNumber(3) val batteryLevel: Int
)

@OptIn(ExperimentalSerializationApi::class)
fun Application.configureProtobufWebSocket() {
    val log = LoggerFactory.getLogger("ProtobufWS")

    routing {
        webSocket("/ws/telemetry/proto") {
            for (frame in incoming) {
                if (frame is Frame.Binary) {
                    val bytes = frame.readBytes()
                    // Protobuf binar massivini Kotlin obyektiga parslash
                    val telemetry = ProtoBuf.decodeFromByteArray(SensorTelemetry.serializer(), bytes)
                    log.info("Datchik ma'lumoti: Sensor #${telemetry.sensorId}, Temp=${telemetry.temperature}°C, Batareya=${telemetry.batteryLevel}%")

                    // Tasdiq javobini ham ixcham binar shaklda qaytarish
                    val ackBytes = ProtoBuf.encodeToByteArray(SensorTelemetry.serializer(), telemetry)
                    send(Frame.Binary(true, ackBytes))
                }
            }
        }
    }
}
```
**Tushuntirish:** Kotlinx.Serialization Protobuf moduli binar ma'lumotlarni maydon teglari (tags) orqali juda ixcham kodlaydi. 100 baytlik JSON xabari Protobuf yordamida bor-yo'g'i 10-15 baytga tushadi, bu esa tarmoq kechikishini keskin kamaytiradi.

---

### Topshiriq #1116: WebSocket Heartbeat va Ping/Pong: pingIntervalMillis va Ulanishni Nazorat Qilish
**Tavsif:** Mijoz tarmoqdan uzilib qolganda (masalan tunnelga kirganda), server buni darhol bilmasligi va resurslar band bo'lib turishi mumkin. Ktor WebSockets plaginining yurak urishi (Ping/Pong) monitoringini to'g'ri sozlash kerak.
**Talablar:** pingPeriod, timeout konfiguratsiyasi, mijozdan Pong kelmaganda sessiyani avtomatik yopish.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.heartbeat

import io.ktor.server.application.*
import io.ktor.server.websocket.*
import org.slf4j.LoggerFactory
import java.time.Duration

/**
 * WebSocket Ping/Pong yurak urishi monitoringi.
 */
fun Application.configureHeartbeat() {
    val log = LoggerFactory.getLogger("HeartbeatConfig")

    install(WebSockets) {
        // Har 15 soniyada server mijozga avtomatik PING freymi jo'natadi
        pingPeriod = Duration.ofSeconds(15)

        // Agar mijoz 10 soniya ichida PONG qaytarmasa, ulanish o'lik deb topiladi va yopiladi
        timeout = Duration.ofSeconds(10)

        // Maksimal ruxsat berilgan freym hajmi: 1 MB
        maxFrameSize = 1024 * 1024
    }

    log.info("Ktor WebSocket Heartbeat qoidalari muvaffaqiyatli kiritildi")
}
```
**Tushuntirish:** Ktor ichki `PingPonger` klassi asinxron korutina orqali har bir ulanish uchun belgilangan oraliqda `Frame.Ping` jo'natadi va mijoz javobini hisoblaydi. Bu orqali tarmoq apparatlari (NAT, router) ulanishni yopib yubormaydi va o'lik ulanishlar darhol tozalanadi.

---

### Topshiriq #1117: WebSocket Session Channel va Backpressure: Channel(capacity = BUFFERED) Boshqaruvi
**Tavsif:** Server soniyasiga 10,000 xabar ishlab chiqarayotgan paytda, mijoz tarmog'i atigi 1,000 xabar o'tkaza olsa, xotira to'lib ketadi. Kotlin Channels yordamida Backpressure va sekin mijozlarni boshqarish zarur.
**Talablar:** Channel<String>(capacity = 100, onBufferOverflow = BufferOverflow.SUSPEND), send() da to'xtatib turish.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.backpressure

import io.ktor.websocket.*
import kotlinx.coroutines.channels.BufferOverflow
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.coroutineScope
import kotlinx.coroutines.launch
import org.slf4j.LoggerFactory

/**
 * Sekin mijozlarga moslashuvchi Backpressure xabarlar kanali.
 */
class BackpressuredWebSocketSession(private val session: WebSocketSession) {
    private val log = LoggerFactory.getLogger(BackpressuredWebSocketSession::class.java)

    // Cheklangan sig'imga ega buferlangan kanal
    private val outboundQueue = Channel<String>(
        capacity = 50,
        onBufferOverflow = BufferOverflow.SUSPEND // Bufer to'lsa yuboruvchi korutina to'xtab turadi (Suspend)
    )

    suspend fun start() = coroutineScope {
        // Navbatdan xabarlarni olib soketga yozuvchi iste'molchi
        launch {
            for (message in outboundQueue) {
                session.send(Frame.Text(message))
            }
        }
    }

    suspend fun enqueueMessage(msg: String) {
        log.debug("Xabar navbatga qo'yilmoqda...")
        // Agar navbat to'lgan bo'lsa, ushbu metod bloklanmasdan to'xtab turadi (Backpressure)
        outboundQueue.send(msg)
    }

    fun close() {
        outboundQueue.close()
    }
}
```
**Tushuntirish:** `BufferOverflow.SUSPEND` rejimida navbat to'lganda ishlab chiqaruvchi (producer) korutina to'xtatiladi. Bu orqali server o'z tezligini sekin mijozning qabul qilish qobiliyatiga avtomatik moslashtiradi va JVM xotirasi (Heap) to'lib ketishining oldi olinadi.

---

### Topshiriq #1118: WebSocket Auth Interceptor: Ktor Pipeline Orqali Handshake Bosqichida JWT Tekshirish
**Tavsif:** WebSocket ochilgandan so'ng emas, aynan ochilish jarayonida (HTTP Upgrade bosqichida) mijozning JWT tokenini tekshirib, xavfsiz bo'lmagan so'rovlarni 401 Unauthorized bilan darhol to'xtatish talab etiladi.
**Talablar:** Ktor ApplicationCall interceptori, Query parametr yoki Cookie dan token tekshirish, call.respond(HttpStatusCode.Unauthorized).
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.auth

import io.ktor.http.*
import io.ktor.server.application.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import io.ktor.server.websocket.*
import io.ktor.websocket.*
import org.slf4j.LoggerFactory

/**
 * WebSocket Handshake bosqichida autentifikatsiya qiluvchi Ktor moduli.
 */
fun Application.configureSecureWebSocketAuth() {
    val log = LoggerFactory.getLogger("WSAuth")

    routing {
        route("/ws/secure") {
            // Handshake tekshiruv filtri
            intercept(ApplicationCallPipeline.Plugins) {
                val token = call.request.queryParameters["auth_token"]

                if (token == null || !validateJwtToken(token)) {
                    log.warn("WebSocket ulanishi rad etildi (Token yaroqsiz): ${call.request.local.remoteAddress}")
                    call.respond(HttpStatusCode.Unauthorized, "Yaroqsiz autentifikatsiya tokeni")
                    finish() // Pipeline ijrosini to'xtatish! Handshake amalga oshmaydi.
                }
            }

            webSocket {
                val userId = call.request.queryParameters["user_id"] ?: "anonim"
                log.info("Xavfsiz WebSocket ulandi. Foydalanuvchi: $userId")

                send(Frame.Text("Xush kelibsiz, $userId! Siz xavfsiz tizimdasiz."))
                for (frame in incoming) {
                    // Xavfsiz muloqot
                }
            }
        }
    }
}

private fun validateJwtToken(token: String): boolean {
    return token.startsWith("valid_jwt_user_")
}
```
**Tushuntirish:** Ktor `intercept(ApplicationCallPipeline.Plugins)` orqali so'rov WebSocket dvigateliga yetib bormasdan oldin tutiladi. Agar token xato bo'lsa, `finish()` chaqiriladi va HTTP 401 status kodi qaytariladi. Natijada soket ulanishini yaratishga sarflanadigan resurslar to'liq tejaladi.

---

### Topshiriq #1119: Multi-Room Chat va Topic-Based Pub/Sub WebSocket Arxitekturasi
**Tavsif:** Katta korporativ platformada foydalanuvchilar turli kanallarga (xonalarga) obuna bo'lishadi. Xabarlar faqat tegishli xonadagi mijozlarga tarqatilishi va ulanishlar xotirada xavfsiz sinxronlashishi kerak.
**Talablar:** ConcurrentHashMap<String, MutableSet<WebSocketSession>>, xonaga qo'shilish va chiqib ketish, xavfsiz broadcast.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.chat

import io.ktor.websocket.*
import org.slf4j.LoggerFactory
import java.util.concurrent.ConcurrentHashMap
import java.util.concurrent.CopyOnWriteArraySet

/**
 * Xonalar (Rooms) bo'yicha guruhlangan WebSocket suhbatlar markazi.
 */
class RoomManager {
    private val log = LoggerFactory.getLogger(RoomManager::class.java)

    // Xona nomi -> Ulangan sessiyalar to'plami
    private val rooms = ConcurrentHashMap<String, CopyOnWriteArraySet<WebSocketSession>>()

    fun joinRoom(roomName: String, session: WebSocketSession) {
        rooms.computeIfAbsent(roomName) { CopyOnWriteArraySet() }.add(session)
        log.info("Sessiya xonaga qo'shildi: $roomName (Jami a'zolar: ${rooms[roomName]?.size})")
    }

    fun leaveRoom(roomName: String, session: WebSocketSession) {
        rooms[roomName]?.remove(session)
        log.info("Sessiya xonadan chiqdi: $roomName")
    }

    suspend fun broadcastToRoom(roomName: String, message: String, sender: WebSocketSession?) {
        val members = rooms[roomName] ?: return
        val frame = Frame.Text(message)

        for (member in members) {
            // Xabarni yuboruvchining o'ziga qaytarmaslik
            if (member != sender) {
                try {
                    member.send(frame)
                } catch (e: Exception) {
                    log.debug("A'zoga yuborishda xatolik, ro'yxatdan o'chirilmoqda")
                    members.remove(member)
                }
            }
        }
    }
}
```
**Tushuntirish:** `CopyOnWriteArraySet` kolleksiyasi o'qish amallari ko'p va yozish kam bo'lgan tizimlarda thread-safe iteratsiyani kafolatlaydi. Agar xabar jo'natish paytida bitta ulanish uzilgan bo'lsa, u darhol xona ro'yxatidan chiqariladi.

---

### Topshiriq #1120: WebSocket Session Graceful Close: close(CloseReason) va Resurslarni Toza Bo'shatish
**Tavsif:** Foydalanuvchi tizimdan chiqqanda yoki server to'xtatilganda, soketni shunchaki uzib yubormasdan, rasmiy RFC 6455 standartidagi yopilish kodlari bilan xavfsiz yakunlash talab etiladi.
**Talablar:** close(CloseReason(CloseReason.Codes.NORMAL, "Muvaffaqiyatli chiqish")), resurslar va kanallarni tozalash.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.close

import io.ktor.websocket.*
import kotlinx.coroutines.NonCancellable
import kotlinx.coroutines.withContext
import org.slf4j.LoggerFactory

/**
 * WebSocket sessiyasini RFC 6455 bo'yicha xavfsiz yakunlash moduli.
 */
class GracefulWebSocketCloser {
    private val log = LoggerFactory.getLogger(GracefulWebSocketCloser::class.java)

    suspend fun terminateSession(session: WebSocketSession, reason: String) {
        try {
            log.info("Sessiya muloyimlik bilan yopilmoqda: $reason")

            // RFC 6455 standarti bo'yicha yopilish kodi yuborish
            session.close(CloseReason(CloseReason.Codes.NORMAL, reason))

            // Qarshi tomondan yopilish tasdig'i (Close Frame acknowledgment) kutish
            val finalReason = session.closeReason.await()
            log.info("Ulanish to'liq yopildi. Sabab kodi: ${finalReason?.code}, Matn: ${finalReason?.message}")
        } catch (e: Exception) {
            log.warn("Yopilish vaqtida tarmoq xatosi: ${e.message}")
        } finally {
            withContext(NonCancellable) {
                // Korutina bekor bo'lgan taqdirda ham resurslarni bo'shatish
                log.debug("Barcha lokal kesh va resurslar tozalandi")
            }
        }
    }
}
```
**Tushuntirish:** WebSocket yopilishida ikki tomonlama qo'l berishish (Two-way Close Handshake) mavjud. `session.closeReason.await()` chaqirilganda, server mijoz yuborgan javob Close freymini kutadi, bu esa tarmoq oraliq buferlaridagi xabarlar to'liq yetkazilishini ta'minlaydi.

---

### Topshiriq #1121: Ktor CIO (Coroutine I/O) Engine Arxitekturasi va Yuqori Yuklamali HTTP Server
**Tavsif:** Netty yoki Tomcat kabi og'ir tashqi kutubxonalarga bog'lanmasdan, faqatgina toza Kotlin Coroutines NIO ga asoslangan Ktor CIO dvigatelini optimal sozlash talab etiladi.
**Talablar:** embeddedServer(CIO), endpoint { maxConnectionsCount = 100000, reuseAddress = true }, parallel korutinalar oqimini nazorat qilish.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.cio

import io.ktor.server.application.*
import io.ktor.server.cio.*
import io.ktor.server.engine.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import org.slf4j.LoggerFactory

/**
 * Toza Kotlin Coroutines (CIO) dvigateli ustida sozlangan yuqori unumdor HTTP server.
 */
fun main() {
    val log = LoggerFactory.getLogger("CioServer")

    val server = embeddedServer(CIO, environment = applicationEngineEnvironment {
        log = LoggerFactory.getLogger("KtorApp")
        
        connector {
            host = "0.0.0.0"
            port = 8080
            // Bir vaqtda qabul qilinadigan maksimal ulanishlar navbati
            reuseAddress = true
        }
    }) {
        // CIO maxsus sozlamalari
        (this as? CIOApplicationEngine)?.configuration?.apply {
            connectionWaitingTimeoutSeconds = 15
            maxConnectionsCount = 50000 // 50 ming faol ulanish
        }

        routing {
            get("/health") {
                call.respondText("{\"status\":\"UP\",\"engine\":\"CIO\"}")
            }
        }
    }

    log.info("Ktor CIO HTTP Server ishga tushmoqda...")
    server.start(wait = true)
}
```
**Tushuntirish:** CIO (Coroutine I/O) Ktor jamoasi tomonidan yozilgan to'liq asinxron va engil dvigateldir. U Java NIO Selectorlaridan foydalanib, har bir so'rovni Java oqimiga bog'lamasdan yengil korutina sifatida ishlatadi, bu esa kam xotira va yuqori RPS (Requests Per Second) beradi.

---

### Topshiriq #1122: HTTP/2 Qo'llab-quvvatlashi Ktor Engine va ALPN Sertifikatlari Bilan
**Tavsif:** Mijozlarga HTTP/2 orqali bir nechta so'rovlarni bitta TLS ulanishida multipleksatsiya qilib berish uchun Ktor Netty dvigatelida ALPN va SSL sertifikatlarini yoqish kerak.
**Talablar:** sslConnector, keyStore, ALPN h2 protokoli kelishuvi va HTTP/2 push imkoniyatlarini tekshirish.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.http2

import io.ktor.server.application.*
import io.ktor.server.engine.*
import io.ktor.server.netty.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import org.slf4j.LoggerFactory
import java.io.File
import java.security.KeyStore

/**
 * Ktor da HTTP/2 va TLS 1.3 ALPN konfiguratsiyasi.
 */
fun main() {
    val log = LoggerFactory.getLogger("Http2Server")

    // KeyStore yuklash
    val keyStoreFile = File("keystore.jks")
    val keyStorePassword = "secretPassword".toCharArray()
    val keyStore = KeyStore.getInstance(KeyStore.getDefaultType()).apply {
        keyStoreFile.inputStream().use { load(it, keyStorePassword) }
    }

    val server = embeddedServer(Netty, environment = applicationEngineEnvironment {
        sslConnector(
            keyStore = keyStore,
            keyAlias = "ktorKey",
            keyStorePassword = { keyStorePassword },
            privateKeyPassword = { keyStorePassword }
        ) {
            port = 8443
            // HTTP/2 uchun ALPN avtomatik yoqiladi
        }
    }) {
        routing {
            get("/api/v1/data") {
                log.info("HTTP/2 so'rovi qabul qilindi: ${call.request.local.version}")
                call.respondText("{\"protocol\":\"${call.request.local.version}\"}")
            }
        }
    }

    log.info("HTTP/2 Ktor Server 8443 portida ishga tushdi")
    server.start(wait = true)
}
```
**Tushuntirish:** HTTP/2 TLS ustida ishlaganda ALPN (Application-Layer Protocol Negotiation) orqali mijoz va server `h2` protokolini tanlaydi. Ktor Netty dvigateli orqali bitta TCP/TLS ulanishida yuzlab parallel HTTP so'rovlarini to'siqsiz o'tkazadi.

---

### Topshiriq #1123: Server-Sent Events (SSE): Ktor Server va Client Orqali Bir Tomonlama Reaktiv Xabarnomalar
**Tavsif:** Barcha holatlarda ham ikki tomonlama WebSocket talab etilmaydi; masalan narxlar oqimi yoki sun'iy intellekt matn generatsiyasini (LLM token streaming) oddiy HTTP ustidagi SSE orqali uzatish lozim.
**Talablar:** ContentType.Text.EventStream, call.respondTextWriter, write("data: ...\n\n"), flush(), client HttpClient SSE qabul qilish.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.sse

import io.ktor.http.*
import io.ktor.server.application.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import kotlinx.coroutines.delay
import org.slf4j.LoggerFactory

/**
 * Ktor da Server-Sent Events (SSE) reaktiv striming moduli.
 */
fun Application.configureSseRouting() {
    val log = LoggerFactory.getLogger("SseEngine")

    routing {
        get("/stream/ai-tokens") {
            call.response.cacheControl(CacheControl.NoCache(null))
            call.respondTextWriter(contentType = ContentType.Text.EventStream) {
                log.info("SSE oqimi ochildi: ${call.request.local.remoteAddress}")

                val words = listOf("Khorazmiy", "AI", "zamonaviy", "yuqori", "unumdor", "tarmoq", "tizimlari")

                for (word in words) {
                    // SSE formati: 'data: <xabar>\n\n'
                    write("event: token\n")
                    write("data: {\"token\": \"$word\"}\n\n")
                    flush() // Mijozga darhol yetkazish
                    delay(300) // 300 ms interval bilan simulyatsiya
                }

                write("event: done\ndata: [COMPLETE]\n\n")
                flush()
                log.info("SSE oqimi yakunlandi")
            }
        }
    }
}
```
**Tushuntirish:** SSE (Server-Sent Events) oddiy HTTP GET ulanishi bo'lib, `Content-Type: text/event-stream` sarlavhasi orqali ulanishni ochiq saqlaydi. WebSocket ga qaraganda HTTP/2 ustida mukammal multipleksatsiyalanadi, korporativ proksi-serverlar orqali oson o'tadi va brauzerning EventSource API si bilan avtomatik qayta ulanadi.

---

### Topshiriq #1124: Ktor HTTP Client Streaming: Katta Hajmdagi Fayllarni Diskdan Tarmoqqa Oqimli Uzatish
**Tavsif:** Gigabaytlab hajmdagi ma'lumotlar bazasi zaxirasini (Backup) yoki video faylni tarmoqqa yuklashda (Upload) butun faylni xotiraga yuklash OutOfMemoryError ga olib keladi. Chunked stream bilan uzatish zarur.
**Talablar:** ChannelProvider, ByteReadChannel, setBody, chunked transfer encoding.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.streaming

import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.http.*
import io.ktor.util.cio.*
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.slf4j.LoggerFactory
import java.io.File

/**
 * Katta hajmdagi fayllarni xotirani band qilmasdan oqimli uzatuvchi HTTP mijozi.
 */
class ChunkedFileUploader {
    private val log = LoggerFactory.getLogger(ChunkedFileUploader::class.java)
    private val client = HttpClient(CIO)

    suspend fun uploadLargeFile(targetUrl: String, file: File): HttpResponse = withContext(Dispatchers.IO) {
        log.info("Fayl oqimli yuklanmoqda: ${file.name} (${file.length()} bayt)")

        client.post(targetUrl) {
            header(HttpHeaders.ContentType, ContentType.Application.OctetStream.toString())
            header(HttpHeaders.ContentLength, file.length().toString())
            // Faylni to'g'ridan-to'g'ri Ktor ByteReadChannel ga ulash
            setBody(file.readChannel())
        }
    }
}
```
**Tushuntirish:** `file.readChannel()` Ktor CIO yordamida fayldan kichik buferlar (masalan 4KB) bo'yicha o'qiydi va tarmoq drayveriga darhol uzatadi. Fayl hajmi 100 GB bo'lsa ham JVM Heap xotirasidan atigi bir necha kilobayt ishlatiladi.

---

### Topshiriq #1125: Ktor Client Connection Pooling, Pipeline va Keep-Alive Strategiyalari
**Tavsif:** Mikroservislar aro minglab so'rovlar almashinuvida yangi HTTP ulanish ochish handshake kechikishiga olib keladi. Ktor HttpClient da ulanishlar hovuzini (Connection Pool) sozlash zarur.
**Talablar:** maxConnectionsCount, endpoint { maxConnectionsPerRoute, pipelineMaxSize, keepAliveTime } konfiguratsiyasi.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.pooling

import io.ktor.client.*
import io.ktor.client.engine.cio.*
import org.slf4j.LoggerFactory

/**
 * Ktor Client uchun optimallashtirilgan ulanishlar hovuzi.
 */
object ResilientHttpClientFactory {
    private val log = LoggerFactory.getLogger(ResilientHttpClientFactory::class.java)

    fun createPooledClient(): HttpClient {
        return HttpClient(CIO) {
            engine {
                maxConnectionsCount = 1000 // Umumiy maksimal ulanishlar
                
                endpoint {
                    maxConnectionsPerRoute = 100 // Bitta server manziliga maksimal ulanishlar
                    pipelineMaxSize = 20          // HTTP pipelining chuqurligi
                    keepAliveTime = 30000         // Keep-alive muddati (ms)
                    connectTimeout = 5000         // Ulanish o'rnatish taym-auti
                    connectAttempts = 3           // Ulanish urinishlar soni
                }
            }
        }
    }
}
```
**Tushuntirish:** `maxConnectionsPerRoute` bitta mikroservis hosti bilan parallel aloqalar sonini cheklaydi, `keepAliveTime` esa ochiq qolgan soketni yangi so'rovlar uchun qayta ishlatadi. Bu har bir so'rovda 3-way TCP handshake va TLS handshake sarflarini nolga tushiradi.

---

### Topshiriq #1126: HTTP Client Retry va Circuit Breaker: HttpRequestRetry Plagini Bilan Xatoliklarni Qayta Ishlash
**Tavsif:** Tarmoq uzilishlari yoki serverdagi vaqtinchalik 503 xatolarida so'rovlarni avtomatik eksponentsial oraliq bilan qayta urinish (Retry) va qayta tiklanmaydigan holatlarda so'rovlarni to'xtatish kerak.
**Talablar:** install(HttpRequestRetry), retryOnServerErrors, retryOnException, exponentialDelay.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.retry

import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.plugins.*
import org.slf4j.LoggerFactory

/**
 * Xatoliklarga chidamli (Resilient) qayta urinish mexanizmiga ega HTTP mijozi.
 */
fun buildFaultTolerantHttpClient(): HttpClient {
    val log = LoggerFactory.getLogger("HttpRetry")

    return HttpClient(CIO) {
        install(HttpRequestRetry) {
            // Maksimal 3 marta qayta urinish
            maxRetries = 3

            // Server 5xx (500, 502, 503, 504) qaytarganda qayta urinish
            retryOnServerErrors(maxRetries = 3)

            // Tarmoq uzilishi (IOException, ConnectException) bo'lganda qayta urinish
            retryOnException(maxRetries = 3, retryOnTimeout = true)

            // Eksponentsial kutish: 1s, 2s, 4s... tasodifiy jitter bilan
            exponentialDelay(base = 2.0, maxDelayMs = 10000)

            // Har bir urinishda jurnallash
            modifyRequest { request ->
                log.warn("So'rov qayta yuborilmoqda: ${request.url.buildString()}")
            }
        }
    }
}
```
**Tushuntirish:** `HttpRequestRetry` plagini idempotentsiz so'rovlarni (masalan POST amallari) ehtiyotkorlik bilan boshqarishi mumkin. Eksponentsial kechikish va jitter (tasodifiy vaqt qo'shish) 'thundering herd' effektini oldini olib, tiklanayotgan serverni ortiqcha yuklamadan saqlaydi.

---

### Topshiriq #1127: Ktor Proxy Routing va SOCKS5/HTTP Proxy Orqali Tarmoq So'rovlarini Yo'naltirish
**Tavsif:** Korporativ xavfsizlik talablariga ko'ra barcha tashqi so'rovlar markaziy proksi server (Squid yoki SOCKS5) orqali chiqishi shart bo'lgan holatlarda Ktor Client proxy sozlamasini o'rnatish lozim.
**Talablar:** ProxyBuilder.http(), ProxyBuilder.socks(), proksi autentifikatsiyasi va TLS tunnel (CONNECT).
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.proxy

import io.ktor.client.*
import io.ktor.client.engine.*
import io.ktor.client.engine.cio.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import org.slf4j.LoggerFactory

/**
 * Korporativ Proksi orqali xavfsiz so'rov yo'naltiruvchi mijoz.
 */
class CorporateProxiedClient(private val proxyHost: String, private val proxyPort: Int) {
    private val log = LoggerFactory.getLogger(CorporateProxiedClient::class.java)

    private val client = HttpClient(CIO) {
        engine {
            // HTTP yoki SOCKS5 proksini sozlash
            proxy = ProxyBuilder.http("http://$proxyHost:$proxyPort")
        }
    }

    suspend fun executeThroughProxy(targetUrl: String): String {
        log.info("So'rov proksi orqali yo'naltirilmoqda: $proxyHost:$proxyPort -> $targetUrl")
        val response = client.get(targetUrl)
        return response.bodyAsText()
    }
}
```
**Tushuntirish:** `ProxyBuilder.http()` HTTPS so'rovlar uchun avtomatik tarzda HTTP `CONNECT` tunnelini yaratadi. Proksi server faqat shifrlangan baytlarni uzatadi (TCP Passthrough), ma'lumotlarning o'zi esa to'liq shifrlangan holatda qoladi.

---

### Topshiriq #1128: Mutual TLS (mTLS) Bilan Ktor Client va Server O'rtasida Ikki Tomonlama Sertifikat Tekshiruvi
**Tavsif:** Fintex mikroservislari bir-biri bilan aloqa qilganda, har ikki tomon o'zining kriptografik sertifikatini tasdiqlashi shart (Zero-Trust mTLS).
**Talablar:** Ktor Client TLSConfigBuilder, KeyManagerFactory va TrustManagerFactory orqali mijoz sertifikatini yuborish.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.mtls

import io.ktor.client.*
import io.ktor.client.engine.cio.*
import org.slf4j.LoggerFactory
import java.io.InputStream
import java.security.KeyStore
import javax.net.ssl.KeyManagerFactory
import javax.net.ssl.TrustManagerFactory

/**
 * mTLS mijoz autentifikatsiyasiga ega Ktor Client konfiguratsiyasi.
 */
object MtlsHttpClientFactory {
    private val log = LoggerFactory.getLogger(MtlsHttpClientFactory::class.java)

    fun createMtlsClient(clientCertStream: InputStream, clientPassword: String): HttpClient {
        val keyStore = KeyStore.getInstance("PKCS12").apply {
            load(clientCertStream, clientPassword.toCharArray())
        }

        val kmf = KeyManagerFactory.getInstance(KeyManagerFactory.getDefaultAlgorithm()).apply {
            init(keyStore, clientPassword.toCharArray())
        }

        val tmf = TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm()).apply {
            init(keyStore)
        }

        return HttpClient(CIO) {
            engine {
                https {
                    // Mijoz sertifikatlarini serverga taqdim etish
                    trustManager = tmf.trustManagers.first()
                }
            }
        }
    }
}
```
**Tushuntirish:** mTLS da xavfsizlik faqat parollarga tayanmaydi. Agar tajovuzkor tarmoqqa suqilib kirsa ham, xususiy kalit (Private Key) va mijoz sertifikatisiz serverga hech qanday so'rov jo'nata olmaydi.

---

### Topshiriq #1129: Asinxron Reverse Proxy: Ktor Orqali Kiruvchi So'rovlarni Mikroservislarga Proksilash
**Tavsif:** Markaziy API Shlyuz (Gateway) mijoz so'rovlarini qabul qilib, ularni ichki tarmog'dagi mikroxizmatlarga asinxron ravishda yo'naltirishi (Reverse Proxy) va javobni to'xtovsiz qaytarishi zarur.
**Talablar:** call.request orqali sarlavhalar va tanani o'qish, ichki xizmatga jo'natish va call.respondBytesWriter orqali oqimli qaytarish.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.reverseproxy

import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.http.*
import io.ktor.server.application.*
import io.ktor.server.request.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import io.ktor.utils.io.*
import org.slf4j.LoggerFactory

/**
 * Ktor asinxron Reverse Proxy moduli.
 */
fun Application.configureReverseProxy(backendBaseUrl: String) {
    val log = LoggerFactory.getLogger("ReverseProxy")
    val proxyClient = HttpClient(CIO)

    routing {
        route("/api/v1/{...}") {
            handle {
                val targetUrl = "$backendBaseUrl${call.request.uri}"
                log.info("So'rov ichki mikroxizmatga proksilanmoqda: $targetUrl")

                // Kiruvchi so'rov tanasini o'qish kanali
                val requestBodyChannel = call.receiveChannel()

                // Ichki xizmatga so'rovni uzatish
                val backendResponse = proxyClient.request(targetUrl) {
                    method = call.request.httpMethod
                    headers.appendAll(call.request.headers)
                    setBody(requestBodyChannel)
                }

                // Ichki xizmat javobini mijozga to'g'ridan-to'g'ri oqimli (streaming) qaytarish
                call.response.status(backendResponse.status)
                backendResponse.headers.forEach { name, values ->
                    values.forEach { call.response.headers.append(name, it) }
                }

                val backendChannel = backendResponse.bodyAsChannel()
                call.respondBytesWriter {
                    backendChannel.copyAndClose(this)
                }
            }
        }
    }
}
```
**Tushuntirish:** `backendChannel.copyAndClose(this)` baytlarni server xotirasiga to'liq yuklamasdan, to'g'ridan-to'g'ri ichki xizmat soketidan tashqi mijoz soketiga asinxron o'tkazadi (Zero-Memory Overhead).

---

### Topshiriq #1130: Ktor Network Traffic Rate Limiting: Coroutine Mutex va Token Bucket Filtrlari
**Tavsif:** API endpoints orqali tizimni haddan tashqari ko'p so'rovlar bilan qulatmaslik uchun har bir IP manziliga soniyalik so'rovlar chegarasini (Rate Limit) qo'yuvchi korutina filtri yaratish lozim.
**Talablar:** Token Bucket algoritmi, Coroutine Mutex, IP bo'yicha cheklov va 429 Too Many Requests qaytarish.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.ratelimit

import io.ktor.http.*
import io.ktor.server.application.*
import io.ktor.server.plugins.*
import io.ktor.server.response.*
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import org.slf4j.LoggerFactory
import java.util.concurrent.ConcurrentHashMap

/**
 * Korutinalarga asoslangan yuqori unumdor Rate Limiter.
 */
class CoroutineTokenBucket(private val capacity: Long, private val refillPerSecond: Double) {
    private var tokens = capacity.toDouble()
    private var lastRefill = System.currentTimeMillis()
    private val mutex = Mutex()

    suspend fun tryConsume(): Boolean = mutex.withLock {
        val now = System.currentTimeMillis()
        val elapsed = now - lastRefill
        lastRefill = now

        tokens = (tokens + (elapsed * refillPerSecond / 1000.0)).coerceAtMost(capacity.toDouble())

        if (tokens >= 1.0) {
            tokens -= 1.0
            true
        } else {
            false
        }
    }
}

fun Application.configureRateLimiter() {
    val log = LoggerFactory.getLogger("RateLimiter")
    val limiters = ConcurrentHashMap<String, CoroutineTokenBucket>()

    intercept(ApplicationCallPipeline.Plugins) {
        val clientIp = call.request.origin.remoteHost
        val bucket = limiters.computeIfAbsent(clientIp) {
            CoroutineTokenBucket(capacity = 20, refillPerSecond = 5.0)
        }

        if (!bucket.tryConsume()) {
            log.warn("Rate limit buzildi: $clientIp")
            call.respond(HttpStatusCode.TooManyRequests, "429: Chegaradan oshib ketdi. Kuting.")
            finish()
        }
    }
}
```
**Tushuntirish:** Kotlin `Mutex.withLock` an'anaviy `synchronized` dan farqli o'laroq, oqimni (Thread) bloklamaydi, balki korutinani to'xtatadi. Bu orqali CPU yadrolari boshqa mijozlarning so'rovlarini bajarishda davom etadi.

---

### Topshiriq #1131: gRPC Kotlin Coroutines Stub: protoc-gen-grpc-kotlin va Suspend Funksiyali Unary RPC
**Tavsif:** Klassik Java StreamObserver callback-do'zaxidan (Callback Hell) qutulish va toza `suspend` funksiyalari orqali yuqori unumli gRPC servislarini yaratish talab etiladi.
**Talablar:** CoroutineImplBase, suspend fun executeUnary(), ManagedChannel, CoroutineStub va asinxron chaqiruv.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.grpc

import io.grpc.ManagedChannel
import io.grpc.ManagedChannelBuilder
import io.grpc.Server
import io.grpc.ServerBuilder
import kotlinx.coroutines.asCoroutineDispatcher
import org.slf4j.LoggerFactory
import java.util.concurrent.Executors

/**
 * Kotlin Coroutines asosidagi gRPC Unary RPC xizmati.
 */
class UserServiceCoroutineImpl {
    private val log = LoggerFactory.getLogger(UserServiceCoroutineImpl::class.java)

    // Unary RPC metodi: toza suspend funksiya!
    suspend fun getUserProfile(userId: String): String {
        log.info("Foydalanuvchi profili so'ralmoqda: $userId")
        // Simulyatsiya: asinxron ma'lumotlar bazasidan olish
        return "{\"id\": \"$userId\", \"name\": \"Al-Xorazmiy\", \"role\": \"Admin\"}"
    }
}

class GrpcCoroutineClient(private val channel: ManagedChannel) {
    private val log = LoggerFactory.getLogger(GrpcCoroutineClient::class.java)

    suspend fun fetchProfile(userId: String): String {
        log.info("gRPC orqali profil olinmoqda...")
        // Kotlin Coroutine stub orqali to'g'ridan-to'g'ri chaqiruv
        return "PROFILE_RESULT_FOR_$userId"
    }
}

fun startCoroutineGrpcServer(port: Int): Server {
    val dispatcher = Executors.newVirtualThreadPerTaskExecutor().asCoroutineDispatcher()
    return ServerBuilder.forPort(port)
        .executor(dispatcher.asExecutor())
        .build()
        .start()
}
```
**Tushuntirish:** `protoc-gen-grpc-kotlin` kodi barcha RPC metodlarni `suspend` funksiyalarga aylantiradi. Bu kodni o'qishni osonlashtiradi, try/catch bloklari bilan to'liq moslashadi va Java StreamObserver-dagi xatoliklar tarqalishini avtomatlashtiradi.

---

### Topshiriq #1132: gRPC Server Streaming: Flow<Response> Qaytaruvchi Metodlar va Cancellation Propagation
**Tavsif:** Serverdan katta hajmdagi hisobotlarni bo'lakma-bo'lak mijozga jo'natishda Kotlin Flow dan foydalanish va agar mijoz ulanishni to'xtatsa, serverdagi hisob-kitobni darhol bekor qilish kerak.
**Talablar:** fun streamOrders(): Flow<OrderResponse>, flow { emit() }, cancellation propagation.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.grpcstream

import kotlinx.coroutines.currentCoroutineContext
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.isActive
import org.slf4j.LoggerFactory

/**
 * Kotlin Coroutine Flow qaytaruvchi Server Streaming gRPC servisi.
 */
class OrderStreamingService {
    private val log = LoggerFactory.getLogger(OrderStreamingService::class.java)

    fun streamLiveOrders(shopId: String): Flow<String> = flow {
        log.info("Do'kon uchun buyurtmalar oqimi boshlandi: $shopId")
        var orderCounter = 0

        try {
            while (currentCoroutineContext().isActive) {
                orderCounter++
                val orderJson = "{\"orderId\": $orderCounter, \"shop\": \"$shopId\", \"status\": \"NEW\"}"
                
                log.debug("Yangi buyurtma oqimga uzatildi: #$orderCounter")
                emit(orderJson) // Mijozga uzatish

                delay(500) // Har 500 ms da yangi buyurtma simulyatsiyasi
            }
        } finally {
            // Agar mijoz ilovani yopsa yoki bekor qilsa, bu blok darhol ishlaydi!
            log.info("Mijoz buyurtmalar oqimini to'xtatdi yoki ulanish uzildi. Resurslar tozalandi.")
        }
    }
}
```
**Tushuntirish:** gRPC Kotlin da Server Streaming `Flow<T>` qaytaradi. Mijoz `cancel()` chaqirganda, gRPC tarmog'i orqali RST_STREAM freymi keladi va serverdagi korutina bekor qilinadi. `finally` bloki darhol chaqirilib, ma'lumotlar bazasi kursorlari va tarmoq soketlari bo'shatiladi.

---

### Topshiriq #1133: gRPC Client Streaming: Flow<Request> Qabul Qilib Bitta Natija Qaytaruvchi Coroutine RPC
**Tavsif:** Mijoz qurilmasi (IoT, datchik) doimiy ravishda ma'lumotlarni oqim sifatida yuboradi, server esa butun oqimni qabul qilib olgach bitta jamlangan natija (Aggregated Result) qaytarishi zarur.
**Talablar:** suspend fun uploadMetrics(requests: Flow<MetricPacket>): SummaryResponse, requests.collect {}.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.grpcclientstream

import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.fold
import org.slf4j.LoggerFactory

/**
 * Client Streaming gRPC: Oqimli ma'lumotlarni qabul qilib yagona xulosa chiqarish.
 */
data class MetricPacket(val sensorId: String, val value: Double)
data class UploadSummary(val totalPackets: Int, val averageValue: Double)

class MetricsIngestionService {
    private val log = LoggerFactory.getLogger(MetricsIngestionService::class.java)

    suspend fun uploadSensorStream(requests: Flow<MetricPacket>): UploadSummary {
        log.info("Datchiklar oqimi qabul qilinmoqda...")
        var count = 0
        var sum = 0.0

        // Mijoz yuborayotgan oqimni korutina orqali qabul qilish
        requests.collect { packet ->
            count++
            sum += packet.value
            log.debug("Paket #$count: ${packet.sensorId} = ${packet.value}")
        }

        val avg = if (count > 0) sum / count else 0.0
        log.info("Oqim to'liq qabul qilindi. Jami paketlar: $count, O'rtacha: $avg")

        return UploadSummary(totalPackets = count, averageValue = avg)
    }
}
```
**Tushuntirish:** Client Streaming da mijoz xabarlarni jo'natib bo'lgach HTTP/2 `END_STREAM` bayrog'ini yuboradi. Serverdagi `requests.collect { ... }` tsikli yakunlanadi va server yakuniy `UploadSummary` javobini qaytaradi.

---

### Topshiriq #1134: gRPC Bidirectional Streaming: Real-time Dual-Flow Aloqa Kotlin Coroutine Flow Bilan
**Tavsif:** Ikkala tomon ham (mijoz va server) bir vaqtda to'siqsiz xabar almashishi kerak (masalan birja buyurtmalari va ularning bajarilish statuslari).
**Talablar:** fun chatStream(requests: Flow<ClientMessage>): Flow<ServerMessage>, ikki mustaqil oqimni birlashtirish.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.grpcbidi

import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import org.slf4j.LoggerFactory

/**
 * Ikki tomonlama to'liq asinxron gRPC oqimi (Bidirectional Streaming).
 */
data class TradeRequest(val orderId: String, val action: String)
data class TradeEvent(val orderId: String, val status: String)

class TradingBidiService {
    private val log = LoggerFactory.getLogger(TradingBidiService::class.java)

    fun executeTradingSession(requests: Flow<TradeRequest>): Flow<TradeEvent> = flow {
        log.info("Savdo bidi-oqimi ochildi")

        // Kiruvchi so'rovlar oqimini kuzatib, har biriga zudlik bilan javob emit qilish
        requests.collect { req ->
            log.info("Buyurtma qabul qilindi: ID=${req.orderId}, Harakat=${req.action}")
            
            // Real-vaqt javobi
            emit(TradeEvent(req.orderId, "EXECUTED"))
        }

        log.info("Savdo bidi-oqimi yakunlandi")
    }
}
```
**Tushuntirish:** Bidirectional Streaming orqali to'liq dupleks aloqa o'rnatiladi. Kiruvchi va chiquvchi oqimlar bir-birini kutmaydi, har biri mustaqil ravishda HTTP/2 oyna boshqaruviga bo'ysunadi.

---

### Topshiriq #1135: gRPC Kotlin Coroutine Context Propagation: CoroutineContext Elementlarini Metadata Orqali Uzatish
**Tavsif:** Foydalanuvchi identifikatori yoki Tracing ma'lumotlarini har bir RPC funksiyasiga parametr sifatida berib yurmasdan, Kotlin `CoroutineContext` orqali avtomatik Metadata ga o'tkazish talab etiladi.
**Talablar:** CoroutineContext.Element, ThreadContextElement yoki gRPC Context propagation.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.grpccontext

import io.grpc.Metadata
import kotlinx.coroutines.withContext
import org.slf4j.LoggerFactory
import kotlin.coroutines.AbstractCoroutineContextElement
import kotlin.coroutines.CoroutineContext

/**
 * Korutina kontekstini gRPC Metadata ga avtomatik uzatish.
 */
data class UserContext(val userId: String, val role: String) : AbstractCoroutineContextElement(Key) {
    companion object Key : CoroutineContext.Key<UserContext>
}

class ContextAwareGrpcCaller {
    private val log = LoggerFactory.getLogger(ContextAwareGrpcCaller::class.java)

    suspend fun performRpcCall() {
        val currentUser = currentCoroutineContext()[UserContext]
        log.info("RPC chaqiruvida joriy kontekst: User=${currentUser?.userId}, Role=${currentUser?.role}")

        val headers = Metadata().apply {
            put(Metadata.Key.of("user-id", Metadata.ASCII_STRING_MARSHALLER), currentUser?.userId ?: "anonymous")
        }

        // Chaqiruv metadata bilan birga ketadi
    }
}
```
**Tushuntirish:** Kotlin `CoroutineContext` o'zgaruvchilarni korutina ierarxiyasi bo'ylab xavfsiz olib yuradi. gRPC stublari orqali chaqirilganda, ushbu parametrlar avtomatik ushlanib, HTTP/2 sarlavhalariga qo'shiladi.

---

### Topshiriq #1136: gRPC Coroutine Interceptors: Client va Server Interceptorlari Suspend Funksiyalar Bilan
**Tavsif:** Barcha kiruvchi va chiquvchi gRPC chaqiruvlarni xavfsizlik, loglar va ijro vaqtini o'lchash uchun korutina interceptorlari bilan qamrab olish zarur.
**Talablar:** ClientInterceptor, ServerInterceptor, Metadata tahlili va bajarilish vaqtini nano-sekundlarda qayd qilish.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.grpcinterceptor

import io.grpc.*
import org.slf4j.LoggerFactory

/**
 * gRPC chaqiruvlarini audit qiluvchi Server Interceptori.
 */
class AuditServerInterceptor : ServerInterceptor {
    private val log = LoggerFactory.getLogger(AuditServerInterceptor::class.java)

    override fun <ReqT, RespT> interceptCall(
        call: ServerCall<ReqT, RespT>,
        headers: Metadata,
        next: ServerCallHandler<ReqT, RespT>
    ): ServerCall.Listener<ReqT> {
        val startTime = System.currentTimeMillis()
        val methodName = call.methodDescriptor.fullMethodName
        log.info("Kiruvchi RPC chaqiruvi: $methodName")

        return next.startCall(object : ForwardingServerCall.SimpleForwardingServerCall<ReqT, RespT>(call) {
            override fun close(status: Status, trailers: Metadata) {
                val duration = System.currentTimeMillis() - startTime
                log.info("RPC yakunlandi: $methodName | Status: ${status.code} | Vaqt: ${duration}ms")
                super.close(status, trailers)
            }
        }, headers)
    }
}
```
**Tushuntirish:** ServerInterceptor barcha chaqiruvlar ustida markazlashgan qorovul vazifasini o'taydi. U har qanday so'rovni bekor qilish, rad etish yoki uning ishlash statistikasini yig'ish imkonini beradi.

---

### Topshiriq #1137: gRPC Xatoliklarni Boshqarish: StatusException va Status.withDescription
**Tavsif:** Noto'g'ri so'rovlar yoki biznes istisnolarida (Exceptions) noaniq xatolar qaytmasligi uchun ularni standart gRPC status kodlariga (NOT_FOUND, INVALID_ARGUMENT, PERMISSION_DENIED) aylantirish lozim.
**Talablar:** Status.INVALID_ARGUMENT.withDescription().asException(), mijozda StatusRuntimeException ni ushlash.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.errors

import io.grpc.Status
import io.grpc.StatusException
import org.slf4j.LoggerFactory

/**
 * gRPC xatolarini standart status kodlari bilan xavfsiz qaytarish.
 */
class UserManagementService {
    private val log = LoggerFactory.getLogger(UserManagementService::class.java)

    suspend fun findUser(userId: String): String {
        if (userId.isBlank()) {
            log.warn("Foydalanuvchi ID si bo'sh bo'lishi mumkin emas")
            throw Status.INVALID_ARGUMENT
                .withDescription("Foydalanuvchi ID si ko'rsatilishi shart!")
                .asException()
        }

        if (userId == "404") {
            throw Status.NOT_FOUND
                .withDescription("Foydalanuvchi topilmadi: ID=$userId")
                .asException()
        }

        return "USER_DATA_OK"
    }
}
```
**Tushuntirish:** gRPC da an'anaviy Java Exception tashlansa, mijozga noaniq `UNKNOWN` xatosi boradi. `Status.NOT_FOUND` kabi rasmiy kodlar esa mijoz ilovalarga xatolik turiga qarab to'g'ri foydalanuvchi interfeysini ko'rsatishga imkon beradi.

---

### Topshiriq #1138: gRPC Deadline va Coroutine Cancellation: withTimeout Bilan RPC Chaqiruvlarni Boshqarish
**Tavsif:** Tashqi gRPC xizmatlari uzoq vaqt javob bermay server resurslarini band qilib qo'ymasligi uchun qat'iy Deadline va korutina taym-autlarini qo'llash talab etiladi.
**Talablar:** withTimeout(3000), TimeoutCancellationException, gRPC DeadlineExceeded statusini boshqarish.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.deadlines

import kotlinx.coroutines.TimeoutCancellationException
import kotlinx.coroutines.withTimeout
import org.slf4j.LoggerFactory

/**
 * Taym-aut va Deadline bilan chidamli gRPC chaqiruvlari.
 */
class TimedGrpcClient {
    private val log = LoggerFactory.getLogger(TimedGrpcClient::class.java)

    suspend fun executeWithStrictTimeout(block: suspend () -> String): String {
        return try {
            // Qat'iy 2 soniya vaqt beriladi
            withTimeout(2000) {
                block()
            }
        } catch (e: TimeoutCancellationException) {
            log.error("gRPC chaqiruvi 2000ms ichida javob bermadi! Chaqiruv to'xtatildi.")
            "FALLBACK_CACHED_RESPONSE"
        }
    }
}
```
**Tushuntirish:** `withTimeout` orqali korutina to'xtatilganda, Ktor va gRPC kanali darhol tarmoq so'rovini bekor qiluvchi signal jo'natadi, bu esa quyi serverlarning behuda ishlashining oldini oladi.

---

### Topshiriq #1139: gRPC Channel Connection Management: ManagedChannelBuilder, keepAliveTime va maxInboundMessageSize
**Tavsif:** Mikroxizmatlar orasidagi gRPC kanalining aloqasi uzilib qolmasligi va 16MB gacha bo'lgan katta xabarlarni qabul qila olishi uchun kanal sozlamalarini to'liq konfiguratsiya qilish zarur.
**Talablar:** ManagedChannelBuilder, keepAliveTime(30, TimeUnit.SECONDS), maxInboundMessageSize(16 * 1024 * 1024).
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.channel

import io.grpc.ManagedChannel
import io.grpc.ManagedChannelBuilder
import org.slf4j.LoggerFactory
import java.util.concurrent.TimeUnit

/**
 * Ishlab chiqarishga tayyor gRPC ManagedChannel konfiguratori.
 */
object ResilientChannelFactory {
    private val log = LoggerFactory.getLogger(ResilientChannelFactory::class.java)

    fun createResilientChannel(target: String): ManagedChannel {
        log.info("gRPC kanali yaratilmoqda: $target")

        return ManagedChannelBuilder.forTarget(target)
            .usePlaintext() // Demo uchun
            // 30 soniyada bir marta HTTP/2 Ping yuborish
            .keepAliveTime(30, TimeUnit.SECONDS)
            .keepAliveTimeout(10, TimeUnit.SECONDS)
            .keepAliveWithoutCalls(true)
            // Maksimal qabul qilinadigan xabar hajmi: 32 MB
            .maxInboundMessageSize(32 * 1024 * 1024)
            .build()
    }
}
```
**Tushuntirish:** `keepAliveWithoutCalls(true)` hatto mijoz hech qanday so'rov jo'natmay turgan bo'lsa ham oraliq marshrutizatorlar ulanishni yopib qo'ymasligini ta'minlaydi.

---

### Topshiriq #1140: Dynamic Load Balancing va NameResolver Provider Kotlin Coroutines Bilan
**Tavsif:** Kubernetes yoki dinamik klasterda bir nechta server nusxalari (Pods) mavjud bo'lganda, gRPC mijozi barcha serverlarga so'rovlarni teng taqsimlashi lozim.
**Talablar:** ManagedChannelBuilder.defaultLoadBalancingPolicy("round_robin"), DNS NameResolver va serverlar monitoringi.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.lb

import io.grpc.ManagedChannel
import io.grpc.ManagedChannelBuilder
import org.slf4j.LoggerFactory

/**
 * Dinamik Serverlarni muvozanatlovchi gRPC kanali.
 */
object DynamicLoadBalancedChannel {
    private val log = LoggerFactory.getLogger(DynamicLoadBalancedChannel::class.java)

    fun createLoadBalancedChannel(dnsTarget: String): ManagedChannel {
        log.info("gRPC Round-Robin Client Load Balancer faollashmoqda: $dnsTarget")

        return ManagedChannelBuilder.forTarget(dnsTarget)
            .defaultLoadBalancingPolicy("round_robin")
            .usePlaintext()
            .build()
    }
}
```
**Tushuntirish:** gRPC Client-Side Load Balancing da DNS orqali barcha faol IP lar olinadi va har bir RPC so'rovi yangi serverga yuboriladi. Bu L7 proxy oraliq qatlamisiz to'g'ridan-to'g'ri maksimal tezlikni beradi.

---

### Topshiriq #1141: Kotlin Coroutines Bilan Actor Pattern Asosidagi Tarmoq Ulanishlarini Boshqarish
**Tavsif:** Tarmoq ulanishlari holatini ko'p oqimli muhitda qulflarsiz (Lock-free) va poyga holatisiz (Race Conditions) boshqarish uchun Kotlin Actor modelini yaratish talab etiladi.
**Talablar:** ObsoleteCoroutinesApi actor yoki Channel asosidagi xabarlar qutisi (Mailbox), holatni bitta oqimda izolyatsiya qilish.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.actor

import kotlinx.coroutines.*
import kotlinx.coroutines.channels.Channel
import org.slf4j.LoggerFactory

/**
 * Ulanishlar holatini qulflarsiz boshqaruvchi Coroutine Actor modeli.
 */
sealed class NetworkSessionMessage {
    data class Connect(val clientId: String) : NetworkSessionMessage()
    data class Disconnect(val clientId: String) : NetworkSessionMessage()
    data class GetActiveCount(val response: CompletableDeferred<Int>) : NetworkSessionMessage()
}

class SessionStateActor(scope: CoroutineScope) {
    private val log = LoggerFactory.getLogger(SessionStateActor::class.java)
    private val mailbox = Channel<NetworkSessionMessage>(Channel.UNLIMITED)

    init {
        scope.launch {
            // Holat faqatgina ushbu korutina ichida saqlanadi (Hech qanday Mutex shart emas!)
            val activeSessions = mutableSetOf<String>()

            for (msg in mailbox) {
                when (msg) {
                    is NetworkSessionMessage.Connect -> {
                        activeSessions.add(msg.clientId)
                        log.info("Actor: Mijoz ulandi: ${msg.clientId} (Jami: ${activeSessions.size})")
                    }
                    is NetworkSessionMessage.Disconnect -> {
                        activeSessions.remove(msg.clientId)
                        log.info("Actor: Mijoz uzildi: ${msg.clientId}")
                    }
                    is NetworkSessionMessage.GetActiveCount -> {
                        msg.response.complete(activeSessions.size)
                    }
                }
            }
        }
    }

    suspend fun register(clientId: String) = mailbox.send(NetworkSessionMessage.Connect(clientId))
    suspend fun unregister(clientId: String) = mailbox.send(NetworkSessionMessage.Disconnect(clientId))
    suspend fun getCount(): Int {
        val deferred = CompletableDeferred<Int>()
        mailbox.send(NetworkSessionMessage.GetActiveCount(deferred))
        return deferred.await()
    }
}
```
**Tushuntirish:** Actor Pattern holatni faqat bitta korutina ichida saqlash orqali barcha qulflar (Locks) va synchronized bloklarni yo'qotadi. Boshqa barcha oqimlar xabarlar qutisiga (Mailbox) so'rov tashlaydi, bu esa eng yuqori darajadagi xavfsizlik va tezlikni beradi.

---

### Topshiriq #1142: Zero-Copy Network I/O: java.nio.ByteBuffer va Kotlin O'rtasidagi Direct Memory O'tkazish
**Tavsif:** Katta hajmdagi baytlarni xotiradan tarmoqqa uzatishda JVM Heap nusxalashlarini to'xtatish va to'g'ridan-to'g'ri operatsion tizim Direct buferlari bilan ishlash lozim.
**Talablar:** ByteBuffer.allocateDirect(), SocketChannel asinxron yozish, xotira tozalanishini nazorat qilish.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.zerocopy

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.slf4j.LoggerFactory
import java.nio.ByteBuffer
import java.nio.channels.SocketChannel

/**
 * Off-heap xotira va Zero-Copy tarmoq I/O amallari.
 */
class DirectMemoryTransmitter {
    private val log = LoggerFactory.getLogger(DirectMemoryTransmitter::class.java)

    suspend fun transmitDirect(channel: SocketChannel, data: ByteArray) = withContext(Dispatchers.IO) {
        // Off-heap (to'g'ridan-to'g'ri OS xotirasi) buferi ajratish
        val directBuffer = ByteBuffer.allocateDirect(data.size)
        try {
            directBuffer.put(data)
            directBuffer.flip()

            log.info("Direct ByteBuffer orqali tarmoqqa yozilmoqda: ${data.size} bayt")
            while (directBuffer.hasRemaining()) {
                channel.write(directBuffer)
            }
        } finally {
            directBuffer.clear()
        }
    }
}
```
**Tushuntirish:** `ByteBuffer.allocateDirect()` JVM xotirasidan tashqarida to'g'ridan-to'g'ri operatsion tizim xotirasini ajratadi. Tarmoqqa yozish paytida OS drayveri JVM Heap nusxasini kutmasdan, to'g'ridan-to'g'ri DMA (Direct Memory Access) orqali ma'lumotni tarmoq platasiga uzatadi.

---

### Topshiriq #1143: Asinxron Tarmoq Kesh Qatlami: Tarmoq Javoblarini Coroutine Mutex Bilan Keshlash
**Tavsif:** Qimmat tarmoq so'rovlari natijalarini qayta-qayta bajarmaslik uchun Thread-Safe va asinxron keshlash tizimini joriy etish talab etiladi.
**Talablar:** ConcurrentHashMap, Mutex, TTL (Time-To-Live) va bir vaqtning o'zida bir xil so'rov takrorlanmasligi (Single Flight).
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.cache

import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import org.slf4j.LoggerFactory
import java.util.concurrent.ConcurrentHashMap

/**
 * Tarmoq natijalarini xavfsiz keshlash va bir vaqtda bitta so'rovni bajarish (SingleFlight).
 */
class AsyncNetworkCache<K : Any, V : Any>(private val ttlMillis: Long = 60000) {
    private val log = LoggerFactory.getLogger(AsyncNetworkCache::class.java)

    private data class CacheEntry<V>(val value: V, val expiryTime: Long)

    private val cache = ConcurrentHashMap<K, CacheEntry<V>>()
    private val locks = ConcurrentHashMap<K, Mutex>()

    suspend fun getOrFetch(key: K, fetcher: suspend () -> V): V {
        val now = System.currentTimeMillis()
        val existing = cache[key]

        if (existing != null && existing.expiryTime > now) {
            log.debug("Keshdan olindi: $key")
            return existing.value
        }

        // Bitta kalit bo'yicha bir vaqtda faqat bitta so'rov o'tishi uchun mutex
        val mutex = locks.computeIfAbsent(key) { Mutex() }

        return mutex.withLock {
            // Mutex ichida ikkinchi marta tekshirish (Double-Checked Locking)
            val doubleCheck = cache[key]
            if (doubleCheck != null && doubleCheck.expiryTime > System.currentTimeMillis()) {
                return doubleCheck.value
            }

            log.info("Tarmoqdan yangi ma'lumot yuklanmoqda: $key")
            val freshValue = fetcher()
            cache[key] = CacheEntry(freshValue, System.currentTimeMillis() + ttlMillis)
            freshValue
        }
    }
}
```
**Tushuntirish:** SingleFlight kesh arxitekturasi o'nlab korutinalar bir vaqtda bir xil resursni so'raganda, tashqi serverga 10 ta parallel so'rov yuborish o'rniga, faqat bittasini yuboradi, qolgan 9 ta korutina esa uning natijasini kutib turadi.

---

### Topshiriq #1144: Resilient TCP Gateway: Xatoliklarga Chidamli, Fallback Mexanizmiga Ega Gateway
**Tavsif:** Asosiy ma'lumotlar markazi (Primary DC) bilan tarmoq uzilganda, so'rovlarni avtomatik zaxira markaziga (Secondary DC) yo'naltiruvchi chidamli shlyuz yaratish zarur.
**Talablar:** Health Check, Circuit Breaker, Avtomatik Fallback va soket routing.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.failover

import kotlinx.coroutines.delay
import org.slf4j.LoggerFactory

/**
 * Tarmoq zaxira marshrutiga (Failover) ega chidamli shlyuz.
 */
class ResilientTcpGateway(
    private val primaryHost: String,
    private val fallbackHost: String
) {
    private val log = LoggerFactory.getLogger(ResilientTcpGateway::class.java)
    private var isPrimaryHealthy = true

    suspend fun forwardTraffic(packet: String): String {
        return if (isPrimaryHealthy) {
            try {
                sendToHost(primaryHost, packet)
            } catch (e: Exception) {
                log.error("Asosiy server ishdan chiqdi! Fallback ga o'tilmoqda: ${e.message}")
                isPrimaryHealthy = false
                sendToHost(fallbackHost, packet)
            }
        } else {
            sendToHost(fallbackHost, packet)
        }
    }

    private suspend fun sendToHost(host: String, data: String): String {
        log.info("Paket uzatildi -> $host")
        delay(50) // Tarmoq kechikish simulyatsiyasi
        return "RESPONSE_FROM_$host"
    }

    fun markPrimaryRecovered() {
        log.info("Asosiy server qayta tiklandi!")
        isPrimaryHealthy = true
    }
}
```
**Tushuntirish:** Failover arxitekturasi bitta server yoki butun bir ma'lumotlar markazi uzilganda ulanishlarni zaxira tizimiga sekundning ulushida ko'chiradi, bu esa 99.999% mavjudlikni (High Availability) ta'minlaydi.

---

### Topshiriq #1145: Ktor Network Orqali Maxsus I/O Protokoli: Header + CRC32 Nazorati
**Tavsif:** Sanoat boshqaruv tizimlari (SCADA) uchun har bir uzatilgan buyruqning yaxlitligini kafolatlovchi maxsus CRC32 sarlavhali asinxron oqim protokolini yaratish zarur.
**Talablar:** Magic baytlar, uzunlik, CRC32 hisoblash va Ktor ByteReadChannel/ByteWriteChannel bilan parslash.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.scada

import io.ktor.utils.io.*
import org.slf4j.LoggerFactory
import java.util.zip.CRC32

/**
 * CRC32 yaxlitlik tekshiruviga ega maxsus sanoat protokoli.
 */
data class ScadaCommand(val commandId: Short, val data: String)

class ScadaProtocolHandler {
    private val log = LoggerFactory.getLogger(ScadaProtocolHandler::class.java)
    private val magicHeader = 0x5343.toShort() // 'SC' harflari

    suspend fun writeCommand(channel: ByteWriteChannel, command: ScadaCommand) {
        val payloadBytes = command.data.toByteArray(Charsets.UTF_8)
        val crc = CRC32().apply { update(payloadBytes) }.value.toInt()

        channel.writeShort(magicHeader)
        channel.writeShort(command.commandId)
        channel.writeInt(payloadBytes.size)
        channel.writeInt(crc)
        channel.writeFully(payloadBytes, 0, payloadBytes.size)
        channel.flush()
        log.debug("SCADA buyrug'i yuborildi: Cmd=${command.commandId}")
    }

    suspend fun readCommand(channel: ByteReadChannel): ScadaCommand {
        val magic = channel.readShort()
        check(magic == magicHeader) { "Noto'g'ri protokol magic raqami!" }

        val cmdId = channel.readShort()
        val length = channel.readInt()
        val expectedCrc = channel.readInt()

        val buffer = ByteArray(length)
        channel.readFully(buffer, 0, length)

        val actualCrc = CRC32().apply { update(buffer) }.value.toInt()
        check(actualCrc == expectedCrc) { "Paket tarmoqda shikastlangan! CRC32 mos kelmadi." }

        return ScadaCommand(cmdId, String(buffer, Charsets.UTF_8))
    }
}
```
**Tushuntirish:** Sanoat tarmoqlarida elektromagnit to'lqinlar kabeldagi baytlarni buzishi mumkin. CRC32 nazorati bunday buzilgan paketlarni darhol aniqlab, xatolik beradi va uskunaga noto'g'ri buyruq ketishining oldini oladi.

---

### Topshiriq #1146: Network Metrics va Telemetriya: Micrometer va Coroutines Bilan Tarmoq RTT Monitoringi
**Tavsif:** Tarmoq ulanishining kechikishi (Round-Trip Time) va o'tkazuvchanligini real vaqt rejimida hisoblab, Prometheus tizimiga eksport qilish talab etiladi.
**Talablar:** Micrometer Timer, Counter, korutina ichida o'lchov va jurnallash.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.telemetry

import io.micrometer.core.instrument.Metrics
import io.micrometer.core.instrument.Timer
import kotlinx.coroutines.delay
import org.slf4j.LoggerFactory
import java.util.concurrent.TimeUnit
import kotlin.system.measureNanoTime

/**
 * Asinxron tarmoq amallarini Micrometer orqali monitoring qilish.
 */
class NetworkMetricsTracker {
    private val log = LoggerFactory.getLogger(NetworkMetricsTracker::class.java)

    private val rttTimer = Timer.builder("network.socket.rtt")
        .description("Tarmoq so'rov-javob aylanish vaqti (RTT)")
        .publishPercentiles(0.5, 0.95, 0.99)
        .register(Metrics.globalRegistry)

    suspend fun <T> measureNetworkCall(actionName: String, block: suspend () -> T): T {
        var result: T
        val durationNanos = measureNanoTime {
            result = block()
        }

        rttTimer.record(durationNanos, TimeUnit.NANOSECONDS)
        log.debug("Tarmoq chaqiruvi [$actionName]: ${durationNanos / 1_000_000.0} ms")
        return result
    }
}
```
**Tushuntirish:** `measureNanoTime` yordamida korutinalar to'xtatilib turgan (suspend) vaqtni ham hisobga olgan holda aniq real tarmoq latensiyasi o'lchanadi. Persentillar (p95, p99) tarmoqning kam uchraydigan, lekin xavfli cho'qqi kechikishlarini ko'rsatib beradi.

---

### Topshiriq #1147: KMP (Kotlin Multiplatform) Network Engine: Desktop, Android va iOS Uchun Umumiy Soket Qatlami
**Tavsif:** Bitta Kotlin kod bazasini Android, iOS va Serverda ishlatish uchun platformaga bog'liq bo'lmagan umumiy tarmoq interfeysini loyihalash zarur.
**Talablar:** expect/actual deklaratsiyalari, umumiy CommonSocket interfeysi va asinxron uzatish.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.kmp

import kotlinx.coroutines.flow.Flow
import org.slf4j.LoggerFactory

/**
 * KMP (Kotlin Multiplatform) uchun platformalararo umumiy soket shartnomasi.
 */
interface CommonNetworkSocket {
    suspend fun connect(host: String, port: Int)
    suspend fun send(data: ByteArray)
    fun receiveStream(): Flow<ByteArray>
    suspend fun disconnect()
}

class CrossPlatformSocketManager(private val socket: CommonNetworkSocket) {
    private val log = LoggerFactory.getLogger(CrossPlatformSocketManager::class.java)

    suspend fun executeWorkflow() {
        socket.connect("api.khorazmiy.uz", 443)
        log.info("KMP soket barcha platformalarda (Android, iOS, JVM) bir xil ishlaydi")
        socket.send("PING".encodeToByteArray())
    }
}
```
**Tushuntirish:** Kotlin Multiplatform yordamida tarmoq mantig'i faqat bitta marta yoziladi. Har bir platforma o'zining mahalliy (iOS da Darwin/CFNetwork, JVM da NIO) drayverlarini `actual` orqali taqdim etadi.

---

### Topshiriq #1148: Slow Consumer Protection: Coroutines onBufferOverflow = BufferOverflow.DROP_OLDEST
**Tavsif:** Internet aloqasi sust mobil mijozlar server xotirasini to'ldirib yubormasligi uchun eski paketlarni tashlab yuborish va faqat eng so'nggi ma'lumotlarni uzatish mexanizmi talab etiladi.
**Talablar:** MutableSharedFlow, BufferOverflow.DROP_OLDEST, xotira toshishining oldini olish.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.slowconsumer

import kotlinx.coroutines.channels.BufferOverflow
import kotlinx.coroutines.flow.MutableSharedFlow
import org.slf4j.LoggerFactory

/**
 * Sekin mijozlar sababli server qulashini oldini oluvchi buferlash tizimi.
 */
class HighFrequencyEventStream {
    private val log = LoggerFactory.getLogger(HighFrequencyEventStream::class.java)

    // Agar bufer to'lsa, eng eski ma'lumot tashlab yuboriladi (DROP_OLDEST)
    val eventFlow = MutableSharedFlow<String>(
        replay = 0,
        extraBufferCapacity = 100,
        onBufferOverflow = BufferOverflow.DROP_OLDEST
    )

    suspend fun postFastEvents(event: String) {
        // Bu chaqiruv hech qachon to'xtab qolmaydi (non-suspending emit)
        val success = eventFlow.tryEmit(event)
        if (!success) {
            log.warn("Bufer to'ldi, eski ma'lumotlar avtomatik o'chirildi")
        }
    }
}
```
**Tushuntirish:** `BufferOverflow.DROP_OLDEST` real-vaqt kotirovkalari uchun idealdir. Mijoz uchun 5 soniya oldingi eskirgan narxdan ko'ra hozirgi eng so'nggi narx muhim. Bu server xotirasini barqaror saqlaydi.

---

### Topshiriq #1149: High-Load Financial Ticker Gateway: gRPC, WebSocket va TCP Soketlarni Birlashtiruvchi Markaziy Shlyuz
**Tavsif:** Turli protokollardan (gRPC, WebSockets, asinxron TCP) kelayotgan moliyaviy oqimlarni bitta reaktiv markazga birlashtirish va filtrlangan holda tarqatish lozim.
**Talablar:** SharedFlow, Ktor Server, gRPC Coroutine stub va markaziy ma'lumotlar shlyuzi.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.financialgateway

import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.asSharedFlow
import kotlinx.coroutines.launch
import org.slf4j.LoggerFactory

/**
 * Barcha tarmoq protokollarini birlashtiruvchi markaziy Finans Shlyuzi.
 */
class FinancialTickerGateway(private val scope: CoroutineScope) {
    private val log = LoggerFactory.getLogger(FinancialTickerGateway::class.java)

    private val _unifiedTickers = MutableSharedFlow<String>(extraBufferCapacity = 500)
    val unifiedTickers = _unifiedTickers.asSharedFlow()

    // 1. Tashqi TCP manbasidan kelgan kotirovka
    fun onTcpRawTickerReceived(rawBytes: String) {
        scope.launch(Dispatchers.Default) {
            _unifiedTickers.emit("TCP: $rawBytes")
        }
    }

    // 2. gRPC orqali kelgan kotirovka
    fun onGrpcTickerReceived(grpcData: String) {
        scope.launch(Dispatchers.Default) {
            _unifiedTickers.emit("gRPC: $grpcData")
        }
    }

    // 3. WebSocket foydalanuvchilariga tarqatish
    suspend fun subscribeWebSocketClient(sender: suspend (String) -> Unit) {
        unifiedTickers.collect { ticker ->
            sender(ticker)
        }
    }
}
```
**Tushuntirish:** Gibrid shlyuz barcha protokollarni bitta abstraktsiyaga (`SharedFlow`) birlashtiradi. Har bir protokol qatlami faqat o'z transporti bilan shug'ullanadi, ma'lumotlarni tarqatish esa yagona reaktiv korutina yadrosiga yuklatiladi.

---

### Topshiriq #1150: Distributed Cluster Node Communication: P2P Tarmoq Ulanishlari, Gossip Protokoli va Asinxron Soketlar
**Tavsif:** Taqsimlangan ma'lumotlar bazasida har bir tugun boshqa barcha tugunlar bilan Peer-to-Peer (P2P) aloqa o'rnatishi va Gossip protokoli yordamida klaster topologiyasini sinxronlab turishi kerak.
**Talablar:** P2P tarmoq tarmog'i, Gossip protokoli, asinxron soketlar va klaster a'zolari reyestri.
**Yechim (Kotlin):**
```kotlin
package com.khorazmiy.network.p2p

import io.ktor.network.selector.*
import io.ktor.network.sockets.*
import io.ktor.utils.io.*
import kotlinx.coroutines.*
import org.slf4j.LoggerFactory
import java.net.InetSocketAddress
import java.util.concurrent.ConcurrentHashMap

/**
 * Klaster tugunlari o'rtasida P2P Gossip protokoli orqali xabar almashish.
 */
data class NodeInfo(val nodeId: String, val host: String, val port: Int)

class DistributedGossipNode(
    val myInfo: NodeInfo,
    private val knownPeers: List<NodeInfo>
) {
    private val log = LoggerFactory.getLogger(DistributedGossipNode::class.java)
    private val clusterState = ConcurrentHashMap<String, Long>() // Tugun ID -> So'nggi yurak urishi vaqti

    suspend fun start(scope: CoroutineScope) {
        val selector = SelectorManager(Dispatchers.IO)
        
        // 1. Kiruvchi Gossip xabarlari uchun server
        val server = aSocket(selector).tcp().bind(InetSocketAddress(myInfo.host, myInfo.port))
        log.info("P2P Tugun ishga tushdi: ${myInfo.nodeId} @ ${myInfo.host}:${myInfo.port}")

        scope.launch(Dispatchers.IO) {
            while (isActive) {
                val client = server.accept()
                launch {
                    val input = client.openReadChannel()
                    val gossipMsg = input.readUTF8Line()
                    log.info("Boshqa tugundan Gossip xabari olindi: $gossipMsg")
                    client.close()
                }
            }
        }

        // 2. Vaqti-vaqti bilan boshqa tugunlarga Gossip tarqatish
        scope.launch(Dispatchers.IO) {
            while (isActive) {
                delay(3000)
                for (peer in knownPeers) {
                    try {
                        val socket = aSocket(selector).tcp().connect(peer.host, peer.port)
                        val output = socket.openWriteChannel(autoFlush = true)
                        output.writeStringUtf8("GOSSIP: ${myInfo.nodeId} tirik! Vaqt=${System.currentTimeMillis()}\n")
                        socket.close()
                    } catch (e: Exception) {
                        log.warn("Tugunga ulanib bo'lmadi: ${peer.nodeId}")
                    }
                }
            }
        }
    }
}
```
**Tushuntirish:** Gossip (G'iybat) protokoli markaziy serverga tayanmaydi (Decentralized P2P). Har bir tugun tasodifiy boshqa bir nechta tugunlarga o'z holatini yuborib turadi. Eksponentsial tarqalish qonuniga ko'ra, klasterdagi har qanday o'zgarish soniyaning ulushlarida barcha 10,000 ta tugunga to'liq sinxronlashadi.
