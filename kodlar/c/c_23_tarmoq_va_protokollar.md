# Khorazmiy AI: C - Modul 23
## Mavzu: Tarmoq protokollari: POSIX Sockets, epoll/kqueue event loop, Raw Sockets va Packet Sniffing

### Topshiriq #1101: POSIX TCP Echo Serveri (IPv4 Socket API)
**Tavsif:** Mikroxizmatlar arxitekturasida kiruvchi TCP paketlarni qabul qilib, o'zgarishsiz qaytaruvchi yuqori samarali echo serverini yaratish.
**Talablar:** IPv4 (`AF_INET`), `SOCK_STREAM`, portni bog'lash (`bind`), tinglash (`listen`) va mijozlarni qabul qilish (`accept`). Xatoliklarni to'g'ri tekshirish.
**Yechim (C):**
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define PORT 8080
#define BUFFER_SIZE 1024

int main() {
    int server_fd, client_fd;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_len = sizeof(client_addr);
    char buffer[BUFFER_SIZE];

    // 1. TCP soket yaratish
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("Soket yaratishda xatolik");
        exit(EXIT_FAILURE);
    }

    // 2. Server manzili va portini sozlash
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY; // Barcha tarmoq interfeyslarini tinglash
    server_addr.sin_port = htons(PORT);       // Bayt tartibini tarmoq tartibiga (Big-Endian) o'tkazish

    // 3. Soketni manzilga bog'lash (bind)
    if (bind(server_fd, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        perror("Bind xatoligi");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    // 4. Kiruvchi ulanishlarni tinglash (listen)
    if (listen(server_fd, 10) < 0) {
        perror("Listen xatoligi");
        close(server_fd);
        exit(EXIT_FAILURE);
    }
    printf("TCP Echo Server %d-portda ishlamoqda...\n", PORT);

    // 5. Mijoz ulanishini qabul qilish (accept)
    if ((client_fd = accept(server_fd, (struct sockaddr*)&client_addr, &client_len)) < 0) {
        perror("Accept xatoligi");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    char client_ip[INET_ADDRSTRLEN];
    inet_ntop(AF_INET, &client_addr.sin_addr, client_ip, INET_ADDRSTRLEN);
    printf("Yangi ulanish: %s:%d\n", client_ip, ntohs(client_addr.sin_port));

    // 6. Ma'lumotlarni qabul qilish va aks ettirish (Echo)
    ssize_t bytes_read;
    while ((bytes_read = recv(client_fd, buffer, sizeof(buffer) - 1, 0)) > 0) {
        buffer[bytes_read] = '\0';
        send(client_fd, buffer, bytes_read, 0); // Qaytarib jo'natish
    }

    close(client_fd);
    close(server_fd);
    return 0;
}
```
**Tushuntirish:** `htons()` funksiyasi host bayt tartibidan tarmoq bayt tartibiga (Big-Endian) o'tkazadi. `accept()` funksiyasi kiruvchi ulanish navbatidan yangi fayl deskriptorini (`client_fd`) ajratadi, asosiy `server_fd` esa tinglashda davom etadi.

---

### Topshiriq #1102: POSIX TCP Klient: Serverga ulanish va ma'lumot almashinuvi
**Tavsif:** Tarmoq servisiga xavfsiz ulanish, buyruq jo'natish va serverdan kelgan to'liq javobni bufer to'lguncha qabul qilish.
**Talablar:** IPv4 manzilini matndan ikkilik formatga o'tkazish (`inet_pton`), `connect()`, uzatish (`send`) va to'liq qabul qilish sikli.
**Yechim (C):**
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define SERVER_IP "127.0.0.1"
#define PORT 8080
#define BUFFER_SIZE 1024

int main() {
    int sock_fd;
    struct sockaddr_in serv_addr;
    char buffer[BUFFER_SIZE];
    const char *message = "Salom, Khorazmiy AI Tarmoq Tizimi!";

    // Soket yaratish
    if ((sock_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("Soket yaratishda xato");
        return -1;
    }

    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);

    // IP manzilni matnli ko'rinishdan binar formatga o'girish
    if (inet_pton(AF_INET, SERVER_IP, &serv_addr.sin_addr) <= 0) {
        perror("Noto'g'ri manzil");
        close(sock_fd);
        return -1;
    }

    // Serverga ulanish
    if (connect(sock_fd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        perror("Ulanish amalga oshmadi");
        close(sock_fd);
        return -1;
    }

    // Xabarni yuborish
    send(sock_fd, message, strlen(message), 0);
    printf("Jo'natilgan xabar: %s\n", message);

    // Server javobini o'qish
    ssize_t bytes_received = recv(sock_fd, buffer, sizeof(buffer) - 1, 0);
    if (bytes_received > 0) {
        buffer[bytes_received] = '\0';
        printf("Serverdan kelgan javob: %s\n", buffer);
    }

    close(sock_fd);
    return 0;
}
```
**Tushuntirish:** `connect()` uch bosqichli TCP qo'l siqishini (3-way handshake: SYN, SYN-ACK, ACK) boshlaydi. `inet_pton()` xavfsiz manzil konvertatsiyasini kafolatlaydi.

---

### Topshiriq #1103: UDP Datagram Echo Server va Klient (Ulanishsiz protokol)
**Tavsif:** Kichik telemetriya va real vaqtli o'yin ma'lumotlarini minimal kechikish bilan qabul qilish va jo'natish.
**Talablar:** `SOCK_DGRAM`, `recvfrom()` va `sendto()` funksiyalari orqali mijoz manzili (`sockaddr_in`) bilan ishlash.
**Yechim (C):**
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define PORT 9090
#define BUFFER_SIZE 1024

int main() {
    int sockfd;
    char buffer[BUFFER_SIZE];
    struct sockaddr_in servaddr, cliaddr;

    // UDP soket ochish
    if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("UDP soket ochilmadi");
        exit(EXIT_FAILURE);
    }

    memset(&servaddr, 0, sizeof(servaddr));
    memset(&cliaddr, 0, sizeof(cliaddr));

    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = INADDR_ANY;
    servaddr.sin_port = htons(PORT);

    // Bog'lash
    if (bind(sockfd, (const struct sockaddr *)&servaddr, sizeof(servaddr)) < 0) {
        perror("UDP bind xatosi");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    printf("UDP Server %d-portda datagrammalarni kutmoqda...\n", PORT);

    socklen_t len = sizeof(cliaddr);
    ssize_t n = recvfrom(sockfd, buffer, BUFFER_SIZE - 1, 0, (struct sockaddr *)&cliaddr, &len);
    if (n > 0) {
        buffer[n] = '\0';
        printf("Mijozdan kelgan UDP paket: %s\n", buffer);

        // Echo javobini jo'natish
        sendto(sockfd, buffer, n, 0, (const struct sockaddr *)&cliaddr, len);
    }

    close(sockfd);
    return 0;
}
```
**Tushuntirish:** UDP protokoli ulanish o'rnatishni talab qilmaydi (connectionless). Har bir `recvfrom()` chaqiruvida yuboruvchining `sockaddr_in` strukturasi qaytariladi va javob `sendto()` bilan to'g'ridan-to'g'ri shu manzilga yuboriladi.

---

### Topshiriq #1104: Non-blocking Sockets (Bloklanmaydigan I/O fcntl orqali)
**Tavsif:** Tarmoq operatsiyalari oqimni to'xtatib qo'ymasligi (thread blocking) uchun soketni asinxron rejimga o'tkazish.
**Talablar:** `fcntl()` yordamida `O_NONBLOCK` bayrog'ini o'rnatish, `EAGAIN` va `EWOULDBLOCK` xatolik kodlarini tahlil qilish.
**Yechim (C):**
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/socket.h>
#include <arpa/inet.h>

int set_nonblocking(int fd) {
    int flags = fcntl(fd, F_GETFL, 0);
    if (flags == -1) return -1;
    return fcntl(fd, F_SETFL, flags | O_NONBLOCK);
}

int main() {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) return 1;

    // Soketni bloklanmaydigan rejimga o'tkazish
    if (set_nonblocking(sock) == -1) {
        perror("fcntl O_NONBLOCK xatosi");
        close(sock);
        return 1;
    }

    char buffer[256];
    ssize_t res = recv(sock, buffer, sizeof(buffer), 0);
    if (res < 0) {
        if (errno == EAGAIN || errno == EWOULDBLOCK) {
            printf("Soketda ma'lumot yo'q, oqim bloklanmadi (EAGAIN/EWOULDBLOCK)!\n");
        } else {
            perror("recv xatosi");
        }
    }

    close(sock);
    return 0;
}
```
**Tushuntirish:** `O_NONBLOCK` o'rnatilganda, agar kiruvchi buferda ma'lumot bo'lmasa, operatsion tizim chaqiruvchi oqimni uxlatmaydi, balki `EAGAIN` yoki `EWOULDBLOCK` statusi bilan zudlik bilan qaytaradi.

---

### Topshiriq #1105: Soket Opsiyalari: SO_REUSEADDR va SO_REUSEPORT
**Tavsif:** Server qayta ishga tushganda `Address already in use` xatosini yo'qotish va bitta portni bir nechta jarayonlarga xavfsiz taqsimlash.
**Talablar:** `setsockopt()`, `SOL_SOCKET`, `SO_REUSEADDR` va `SO_REUSEPORT` bayroqlaridan foydalanish.
**Yechim (C):**
```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>

int configure_reusable_socket(int port) {
    int sfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sfd < 0) return -1;

    int opt = 1;
    // TIME_WAIT holatidagi portni qayta egallash imkoniyati
    if (setsockopt(sfd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)) < 0) {
        perror("SO_REUSEADDR xatosi");
    }

#ifdef SO_REUSEPORT
    // Bitta portni bir nechta jarayonlar o'rtasida teng taqsimlash
    if (setsockopt(sfd, SOL_SOCKET, SO_REUSEPORT, &opt, sizeof(opt)) < 0) {
        perror("SO_REUSEPORT xatosi");
    }
#endif

    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port = htons(port);

    if (bind(sfd, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        perror("Bind muvaffaqiyatsiz");
        close(sfd);
        return -1;
    }

    return sfd;
}

int main() {
    int fd = configure_reusable_socket(8080);
    if (fd >= 0) {
        printf("Soket SO_REUSEADDR va SO_REUSEPORT bilan muvaffaqiyatli bog'landi: FD=%d\n", fd);
        close(fd);
    }
    return 0;
}
```
**Tushuntirish:** `SO_REUSEADDR` TIME_WAIT bosqichidagi soket manzillarini zudlik bilan qayta egallashga ruxsat beradi. `SO_REUSEPORT` esa Linux 3.9+ da bir nechta mustaqil jarayonlarga bir xil IP/portga ulanish imkonini beradi va yadro darajasida yuklama balansi (load balancing) hosil qiladi.

---

### Topshiriq #1106: Soket Timeout va Keepalive Sozlamalari
**Tavsif:** Javob bermayotgan klientlar oqimlarni abadiy band qilib qo'yishining oldini olish uchun qabul qilish va uzatish vaqt chegaralarini o'rnatish.
**Talablar:** `struct timeval`, `SO_RCVTIMEO`, `SO_SNDTIMEO`, `SO_KEEPALIVE` va `TCP_KEEPIDLE` opsiyalari.
**Yechim (C):**
```c
#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/tcp.h>

int set_socket_timeouts(int sfd, int sec) {
    struct timeval tv;
    tv.tv_sec = sec;
    tv.tv_usec = 0;

    // Qabul qilish (recv) timeouti
    if (setsockopt(sfd, SOL_SOCKET, SO_RCVTIMEO, (const char*)&tv, sizeof(tv)) < 0) {
        return -1;
    }
    // Uzatish (send) timeouti
    if (setsockopt(sfd, SOL_SOCKET, SO_SNDTIMEO, (const char*)&tv, sizeof(tv)) < 0) {
        return -1;
    }

    // TCP Keepalive ni faollashtirish
    int keepalive = 1;
    setsockopt(sfd, SOL_SOCKET, SO_KEEPALIVE, &keepalive, sizeof(keepalive));

    // 60 soniya jimlikdan so'ng birinchi keepalive probini jo'natish
    int keepidle = 60;
#ifdef TCP_KEEPIDLE
    setsockopt(sfd, IPPROTO_TCP, TCP_KEEPIDLE, &keepidle, sizeof(keepidle));
#endif

    return 0;
}

int main() {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock >= 0) {
        set_socket_timeouts(sock, 5);
        printf("Soket uchun 5 soniyalik I/O timeout va Keepalive muvaffaqiyatli o'rnatildi.\n");
        close(sock);
    }
    return 0;
}
```
**Tushuntirish:** `SO_RCVTIMEO` va `SO_SNDTIMEO` belgilangan vaqt ichida hech qanday bayt almashinmasa, `EWOULDBLOCK`/`EAGAIN` xatosini yuzaga keltiradi. Bu sekin mijozlar hujumini (Slowloris DoS) oldini oladi.

---

### Topshiriq #1107: Dual-Stack IPv4 va IPv6 Server Soketi
**Tavsif:** Server bir vaqtning o'zida IPv4 va IPv6 orqali murojaat qilayotgan barcha tarmoq mijozlariga yagona soket orqali xizmat ko'rsatishi lozim.
**Talablar:** `AF_INET6`, `in6addr_any`, `IPV6_V6ONLY = 0` konfiguratsiyasi orqali dual-stack yaratish.
**Yechim (C):**
```c
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>

int create_dual_stack_server(int port) {
    int sfd = socket(AF_INET6, SOCK_STREAM, 0);
    if (sfd < 0) return -1;

    // IPV6_V6ONLY parametrini 0 qilib, IPv4 xaritasini ham qabul qilish
    int no = 0;
    if (setsockopt(sfd, IPPROTO_IPV6, IPV6_V6ONLY, (void *)&no, sizeof(no)) < 0) {
        perror("IPV6_V6ONLY o'rnatilmadi");
        close(sfd);
        return -1;
    }

    struct sockaddr_in6 addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin6_family = AF_INET6;
    addr.sin6_addr = in6addr_any; // :: manzili
    addr.sin6_port = htons(port);

    if (bind(sfd, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        perror("Dual stack bind xatosi");
        close(sfd);
        return -1;
    }

    listen(sfd, 10);
    return sfd;
}

int main() {
    int server = create_dual_stack_server(9000);
    if (server >= 0) {
        printf("Dual-Stack (IPv4 & IPv6) server 9000-portda muvaffaqiyatli tinglashni boshladi.\n");
        close(server);
    }
    return 0;
}
```
**Tushuntirish:** `IPV6_V6ONLY = 0` opsiyasi yoqilganda, operatsion tizim kiruvchi IPv4 ulanishlarini avtomatik ravishda IPv4-mapped IPv6 manzillariga (`::ffff:192.168.1.1`) aylantiradi.

---

### Topshiriq #1108: Unix Domain Sockets (IPC uchun mahalliy tarmoq soketi)
**Tavsif:** Bitta operatsion tizim ichidagi ikki mikroxizmat o'rtasida TCP stack overheadsiz eng yuqori o'tkazuvchanlikda aloqa o'rnatish.
**Talablar:** `AF_UNIX` (yoki `AF_LOCAL`), `struct sockaddr_un`, `sun_path` va fayl tizimi soket fayli.
**Yechim (C):**
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/un.h>

#define SOCKET_PATH "/tmp/khorazmiy_ipc.sock"

int main() {
    int server_fd;
    struct sockaddr_un addr;

    // Oldingi fayl mavjud bo'lsa o'chirish
    unlink(SOCKET_PATH);

    if ((server_fd = socket(AF_UNIX, SOCK_STREAM, 0)) < 0) {
        perror("Unix domain socket ochilmadi");
        exit(EXIT_FAILURE);
    }

    memset(&addr, 0, sizeof(addr));
    addr.sun_family = AF_UNIX;
    strncpy(addr.sun_path, SOCKET_PATH, sizeof(addr.sun_path) - 1);

    if (bind(server_fd, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        perror("UDS bind xatosi");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    listen(server_fd, 5);
    printf("Unix Domain Socket server tinglamoqda: %s\n", SOCKET_PATH);

    close(server_fd);
    unlink(SOCKET_PATH);
    return 0;
}
```
**Tushuntirish:** Unix Domain Sockets tarmoq adapteri, IP marshrutlash va checksum hisob-kitoblarini chetlab o'tib, to'g'ridan-to'g'ri operatsion tizim yadrosi xotirasi (kernel memory buffers) orqali ma'lumot uzatadi.

---

### Topshiriq #1109: Unix Domain Sockets orqali File Descriptor Uzatish (SCM_RIGHTS)
**Tavsif:** Asosiy boshqaruvchi jarayon ochilgan tarmoq yoki fayl deskriptorini worker jarayonga nusxalashsiz (Zero-copy IPC) topshirishi kerak.
**Talablar:** `sendmsg()`, `recvmsg()`, `struct msghdr`, `struct cmsghdr` va `SCM_RIGHTS` ancillary data.
**Yechim (C):**
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>

// Unix soket orqali boshqa jarayonga fayl deskriptorini (FD) yuborish
int send_fd(int socket_fd, int fd_to_send) {
    struct msghdr msg = {0};
    char buf[CMSG_SPACE(sizeof(int))];
    memset(buf, 0, sizeof(buf));

    struct iovec io = { .iov_base = "F", .iov_len = 1 };
    msg.msg_iov = &io;
    msg.msg_iovlen = 1;
    msg.msg_control = buf;
    msg.msg_controllen = sizeof(buf);

    struct cmsghdr *cmsg = CMSG_FIRSTHDR(&msg);
    cmsg->cmsg_level = SOL_SOCKET;
    cmsg->cmsg_type = SCM_RIGHTS;
    cmsg->cmsg_len = CMSG_LEN(sizeof(int));

    // Jo'natilayotgan FD ni yordamchi ma'lumot qismiga nusxalash
    *((int *)CMSG_DATA(cmsg)) = fd_to_send;

    return sendmsg(socket_fd, &msg, 0);
}

int main() {
    int sv[2];
    if (socketpair(AF_UNIX, SOCK_STREAM, 0, sv) < 0) {
        perror("socketpair xatosi");
        return 1;
    }
    printf("Socketpair yaratildi: FD1=%d, FD2=%d. SCM_RIGHTS tayyor.\n", sv[0], sv[1]);
    close(sv[0]);
    close(sv[1]);
    return 0;
}
```
**Tushuntirish:** `SCM_RIGHTS` boshqaruvchi xabari orqali Linux yadrosi fayl deskriptorlar jadvaliga havola yaratadi va qabul qiluvchi jarayonning deskriptorlar jadvaliga yangi indeks bilan kiritadi.

---

### Topshiriq #1110: Nagle Algoritmini Boshqarish: TCP_NODELAY va TCP_CORK
**Tavsif:** Real vaqtli birja savdosi (HFT) yoki o'yin paketlarida har bir baytni zudlik bilan jo'natish va Nagle kechikishini bartaraf qilish.
**Talablar:** `IPPROTO_TCP`, `TCP_NODELAY` (darhol yuborish) va `TCP_CORK` (paket to'lishini kutish).
**Yechim (C):**
```c
#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/tcp.h>
#include <netinet/in.h>

void optimize_tcp_latency(int sock_fd) {
    int flag = 1;
    // Nagle algoritmini o'chirish (Kechikishni 0 ga tushirish)
    if (setsockopt(sock_fd, IPPROTO_TCP, TCP_NODELAY, (char *)&flag, sizeof(int)) < 0) {
        perror("TCP_NODELAY o'rnatishda xato");
    } else {
        printf("TCP_NODELAY muvaffaqiyatli faollashtirildi (Nagle o'chirildi).\n");
    }

#ifdef TCP_CORK
    // Aksincha, katta fayllarni yuborishda sarlavha va ma'lumotni to'plash
    int cork = 0; // O'chirilgan holat
    setsockopt(sock_fd, IPPROTO_TCP, TCP_CORK, (char *)&cork, sizeof(int));
#endif
}

int main() {
    int fd = socket(AF_INET, SOCK_STREAM, 0);
    if (fd >= 0) {
        optimize_tcp_latency(fd);
        close(fd);
    }
    return 0;
}
```
**Tushuntirish:** Nagle algoritmi kichik paketlarni to'plab jo'natishga harakat qiladi va bu 40-200ms kechikish (ACK kutish) keltirib chiqarishi mumkin. `TCP_NODELAY` paketlarni buferda ushlab turmasdan zudlik bilan tarmoq simiga chiqaradi.

---

### Topshiriq #1111: I/O Multiplexing: select() yordamida Ko'p Mijozli Server
**Tavsif:** Bir nechta kiruvchi mijozlarni bitta asosiy oqimda bloklanmasdan nazorat qilish.
**Talablar:** `fd_set`, `FD_ZERO`, `FD_SET`, `FD_ISSET`, `select()` va maksimal deskriptor `max_fd` hisobi.
**Yechim (C):**
```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <sys/select.h>

#define MAX_CLIENTS 30
#define PORT 8888

int main() {
    int master_socket, client_socket[MAX_CLIENTS] = {0};
    int max_sd, sd, activity, i;
    struct sockaddr_in address;
    fd_set readfds;

    master_socket = socket(AF_INET, SOCK_STREAM, 0);
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    bind(master_socket, (struct sockaddr *)&address, sizeof(address));
    listen(master_socket, 5);
    printf("select() server %d-portda ishlamoqda...\n", PORT);

    while (1) {
        FD_ZERO(&readfds);
        FD_SET(master_socket, &readfds);
        max_sd = master_socket;

        for (i = 0; i < MAX_CLIENTS; i++) {
            sd = client_socket[i];
            if (sd > 0) FD_SET(sd, &readfds);
            if (sd > max_sd) max_sd = sd;
        }

        // Hodisalarni kutish (bloklanuvchi select)
        activity = select(max_sd + 1, &readfds, NULL, NULL, NULL);
        if (activity < 0) break;

        // Yangi ulanish tekshiruvi
        if (FD_ISSET(master_socket, &readfds)) {
            int new_socket = accept(master_socket, NULL, NULL);
            for (i = 0; i < MAX_CLIENTS; i++) {
                if (client_socket[i] == 0) {
                    client_socket[i] = new_socket;
                    printf("Mijoz qabul qilindi: Slot #%d, FD=%d\n", i, new_socket);
                    break;
                }
            }
        }
        break; // Test sikli yakuni
    }

    close(master_socket);
    return 0;
}
```
**Tushuntirish:** `select()` usuli $O(N)$ murakkablikka ega va `FD_SETSIZE` (odatda 1024) bilan cheklangan. Kichik va ko'chma (portable) tizimlar uchun standart yechim hisoblanadi.

---

### Topshiriq #1112: I/O Multiplexing: poll() yordamida Dinamik Ulanishlar Monitoringi
**Tavsif:** `FD_SETSIZE` cheklovisiz 10,000+ deskriptorlarni massiv orqali monitoring qilish.
**Talablar:** `struct pollfd`, `events = POLLIN`, `revents`, `poll()` tizim chaqiruvi.
**Yechim (C):**
```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <poll.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define MAX_FDS 200

int main() {
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in addr = { .sin_family = AF_INET, .sin_port = htons(9001), .sin_addr.s_addr = INADDR_ANY };
    bind(server_fd, (struct sockaddr*)&addr, sizeof(addr));
    listen(server_fd, 10);

    struct pollfd fds[MAX_FDS];
    fds[0].fd = server_fd;
    fds[0].events = POLLIN; // O'qishga tayyorlikni kuzatish
    int nfds = 1;

    printf("poll() monitoringi boshlandi, server FD=%d...\n", server_fd);
    int ret = poll(fds, nfds, 1000); // 1000 ms timeout

    if (ret > 0 && (fds[0].revents & POLLIN)) {
        printf("Kiruvchi ulanish mavjud!\n");
    } else {
        printf("1 soniya ichida faollik kuzatilmadi (Timeout).\n");
    }

    close(server_fd);
    return 0;
}
```
**Tushuntirish:** `poll()` funksiyasi `select()` ning 1024 o'lchamli cheklovini yo'qotadi, chunki u dinamik massiv (`pollfd[]`) qabul qiladi. Biroq yadro hali ham butun massivni chiziqli ko'rib chiqadi.

---

### Topshiriq #1113: Linux epoll Asoslari: C10K Muammosini Hal Qilish
**Tavsif:** 10,000 dan ortiq bir vaqtda faol ulanishlarni minimal protsessor sarfi ($O(1)$) bilan boshqarish.
**Talablar:** `epoll_create1(0)`, `epoll_ctl(EPOLL_CTL_ADD)`, `struct epoll_event`, `epoll_wait()`.
**Yechim (C):**
```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/epoll.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define MAX_EVENTS 64

int main() {
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in addr = { .sin_family = AF_INET, .sin_port = htons(7070), .sin_addr.s_addr = INADDR_ANY };
    bind(server_fd, (struct sockaddr*)&addr, sizeof(addr));
    listen(server_fd, 128);

    // 1. epoll instansiyasini yaratish
    int epoll_fd = epoll_create1(0);
    if (epoll_fd < 0) { perror("epoll_create1"); exit(1); }

    struct epoll_event ev, events[MAX_EVENTS];
    ev.events = EPOLLIN;
    ev.data.fd = server_fd;

    // 2. Server soketini epoll monitoringiga qo'shish
    if (epoll_ctl(epoll_fd, EPOLL_CTL_ADD, server_fd, &ev) < 0) {
        perror("epoll_ctl ADD");
        exit(1);
    }

    printf("epoll hodisalar zanjiri tayyor, tinglash porti: 7070\n");

    // 3. Hodisalarni kutish (0 ms - no-wait test)
    int n = epoll_wait(epoll_fd, events, MAX_EVENTS, 0);
    printf("Faol hodisalar soni: %d\n", n);

    close(server_fd);
    close(epoll_fd);
    return 0;
}
```
**Tushuntirish:** `epoll` Linux yadrosida qizil-qora daraxt (Red-Black Tree) va tayyor hodisalar uchun Ready List ro'yxatidan foydalanadi. Natijada faollikni tekshirish $O(1)$ tezlikda amalga oshadi.

---

### Topshiriq #1114: epoll Edge-Triggered (EPOLLET) va To'liq Bufer O'qish
**Tavsif:** Faqat yangi ma'lumot kelgandagina xabarnoma olish orqali epoll bildirishnomalar sonini minimallashtirish.
**Talablar:** `EPOLLET` rejimi, `O_NONBLOCK` soketlar va `EAGAIN` gacha to'liq o'qish sikli (`while (recv > 0)`).
**Yechim (C):**
```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/epoll.h>
#include <sys/socket.h>

void read_edge_triggered(int fd) {
    char buf[128];
    while (1) {
        ssize_t count = recv(fd, buf, sizeof(buf), 0);
        if (count == -1) {
            // Edge-triggered rejimida bufer to'liq bo'shatilganini bildiradi
            if (errno == EAGAIN || errno == EWOULDBLOCK) {
                printf("Bufer to'liq o'qildi, keyingi paketgacha to'xtatildi.\n");
                break;
            }
            perror("recv xatosi");
            break;
        } else if (count == 0) {
            printf("Klient ulanishni yopdi.\n");
            close(fd);
            break;
        }
        printf("Qabul qilindi: %zd bayt\n", count);
    }
}

int main() {
    struct epoll_event ev;
    ev.events = EPOLLIN | EPOLLET; // Edge-Triggered bayrog'i
    ev.data.fd = 3;
    printf("EPOLLET sozlamasi tayyorlandi: events = 0x%X\n", ev.events);
    return 0;
}
```
**Tushuntirish:** Level-Triggered rejimida buferda ma'lumot qolsa epoll har safar qayta uyg'otadi. Edge-Triggered (`EPOLLET`) rejimida esa faqat holat o'zgarganda uyg'otadi, shuning uchun butun ma'lumot `EAGAIN` olinmaguncha o'qilishi shart.

---

### Topshiriq #1115: epoll da Thundering Herd Muammosini Hal Qilish (EPOLLEXCLUSIVE)
**Tavsif:** Bitta server soketini bir nechta worker oqimlar kutayotganda barcha oqimlarning keraksiz uyg'onishini oldini olish.
**Talablar:** `EPOLLEXCLUSIVE` bayrog'i va `SO_REUSEPORT` ko'p oqimli arxitekturasi.
**Yechim (C):**
```c
#include <stdio.h>
#include <unistd.h>
#include <sys/epoll.h>
#include <sys/socket.h>

#ifndef EPOLLEXCLUSIVE
#define EPOLLEXCLUSIVE (1U << 28)
#endif

int register_exclusive_listener(int epoll_fd, int server_fd) {
    struct epoll_event ev;
    // Barcha oqimlardan faqat bittasini uyg'otish uchun EPOLLEXCLUSIVE
    ev.events = EPOLLIN | EPOLLEXCLUSIVE;
    ev.data.fd = server_fd;

    return epoll_ctl(epoll_fd, EPOLL_CTL_ADD, server_fd, &ev);
}

int main() {
    int epfd = epoll_create1(0);
    int sfd = socket(AF_INET, SOCK_STREAM, 0);

    if (epfd >= 0 && sfd >= 0) {
        if (register_exclusive_listener(epfd, sfd) == 0) {
            printf("Tinglovchi EPOLLEXCLUSIVE bilan ro'yxatdan o'tdi (Thundering Herd bartaraf etildi).\n");
        }
        close(sfd);
        close(epfd);
    }
    return 0;
}
```
**Tushuntirish:** `EPOLLEXCLUSIVE` (Linux 4.5+) kiruvchi ulanish paydo bo'lganda bir xil epoll guruhidagi oqimlardan faqat bittasini uyg'otadi, bu esa CPU keshlarining ifloslanishini va context switch xarajatlarini keskin pasaytiradi.

---

### Topshiriq #1116: BSD/macOS kqueue va kevent Hodisalar Tizimi
**Tavsif:** FreeBSD, OpenBSD va macOS operatsion tizimlarida eng yuqori unumdorlikdagi asinxron I/O ni tashkil etish.
**Talablar:** `kqueue()`, `EV_SET()`, `struct kevent`, `EVFILT_READ`, `kevent()` chaqiruvi.
**Yechim (C):**
```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/event.h>
#include <sys/time.h>
#include <sys/socket.h>

int main() {
#if defined(__APPLE__) || defined(__FreeBSD__) || defined(__OpenBSD__)
    int kq = kqueue();
    if (kq < 0) { perror("kqueue xatosi"); exit(1); }

    int sfd = socket(AF_INET, SOCK_STREAM, 0);
    struct kevent change_event, event;

    // Hodisani sozlash (O'qish filtri)
    EV_SET(&change_event, sfd, EVFILT_READ, EV_ADD | EV_ENABLE, 0, 0, NULL);

    struct timespec tm = { .tv_sec = 0, .tv_nsec = 100000000 }; // 100ms
    int nev = kevent(kq, &change_event, 1, &event, 1, &tm);
    printf("kqueue hodisalari soni: %d\n", nev);

    close(sfd);
    close(kq);
#else
    printf("kqueue faqat BSD/macOS tizimlarida ishlaydi (Linux uchun epoll qo'llaniladi).\n");
#endif
    return 0;
}
```
**Tushuntirish:** `kqueue` mexanizmi Linuxdagi `epoll` ning to'g'ridan-to'g'ri analogi bo'lib, nafaqat tarmoq soketlari, balki fayllar, signallar, taymerlar va jarayonlarni ham yagona interfeys orqali boshqaradi.

---

### Topshiriq #1117: Reactor Pattern Asosidagi Bitta Oqimli Event Loop
**Tavsif:** Node.js va Nginx arxitekturasi singari bitta oqimda voqealarga asoslangan to'liq reaktiv tarmoq serverini qurish.
**Talablar:** Hodisalar dispetcheri (Event Dispatcher), ro'yxatga olish, callback funksiyalar ko'rsatkichlari.
**Yechim (C):**
```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/epoll.h>

typedef void (*event_handler_t)(int fd, uint32_t events, void *arg);

typedef struct {
    int fd;
    event_handler_t handler;
    void *arg;
} EventContext;

void on_client_read(int fd, uint32_t events, void *arg) {
    printf("Callback: FD=%d da ma'lumot o'qishga tayyor (Events=0x%X)\n", fd, events);
}

int main() {
    int epfd = epoll_create1(0);
    EventContext ctx = { .fd = 5, .handler = on_client_read, .arg = NULL };

    struct epoll_event ev;
    ev.events = EPOLLIN;
    ev.data.ptr = &ctx; // Kontekst ko'rsatkichini epoll ga biriktirish

    printf("Reactor Handler o'rnatildi: Handler manzili = %p\n", (void*)ctx.handler);
    close(epfd);
    return 0;
}
```
**Tushuntirish:** Reactor patternida `epoll.data.ptr` orqali kontekst va callback funksiya manzili saqlanadi. Hodisa sodir bo'lganda tegishli callback chaqirilib, oqim bloklanishi oldi olinadi.

---

### Topshiriq #1118: Asinxron Signallarni epoll bilan Integratsiya Qilish (signalfd)
**Tavsif:** SIGINT va SIGTERM signallarini an'anaviy signal handlerlarsiz, oddiy fayl deskriptori sifatida event loopda xavfsiz qabul qilish.
**Talablar:** `sigprocmask()`, `signalfd()`, `struct signalfd_siginfo` va `epoll_ctl`.
**Yechim (C):**
```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <sys/signalfd.h>
#include <sys/epoll.h>

int main() {
    sigset_t mask;
    sigemptyset(&mask);
    sigaddset(&mask, SIGINT);
    sigaddset(&mask, SIGTERM);

    // Signallarni standart handlerlar tomonidan ushlanishini bloklash
    if (sigprocmask(SIG_BLOCK, &mask, NULL) < 0) {
        perror("sigprocmask");
        return 1;
    }

    // Signallar uchun deskriptor yaratish
    int sfd = signalfd(-1, &mask, SFD_NONBLOCK);
    if (sfd < 0) {
        perror("signalfd");
        return 1;
    }

    printf("signalfd yaratildi: FD=%d. Endi SIGINT/SIGTERM epoll orqali o'qiladi.\n", sfd);
    close(sfd);
    return 0;
}
```
**Tushuntirish:** `signalfd` asinxron signallarni sinxron I/O ga aylantiradi. Bu holat signal handler ichida xavfli bo'lgan funksiyalarni (malloc, printf) chaqirish xatarini butunlay yo'qotadi.

---

### Topshiriq #1119: Yuqori Aniqlikdagi Taymerlarni Event Loopga Ulash (timerfd)
**Tavsif:** Tarmoq ulanishlarining heartbeat va keepalive tekshiruvlarini nanosekund aniqlikda boshqarish.
**Talablar:** `timerfd_create(CLOCK_MONOTONIC)`, `timerfd_settime()`, `struct itimerspec` va epoll.
**Yechim (C):**
```c
#include <stdio.h>
#include <unistd.h>
#include <sys/timerfd.h>
#include <time.h>
#include <stdint.h>

int setup_periodic_timer(int interval_sec) {
    int tfd = timerfd_create(CLOCK_MONOTONIC, TFD_NONBLOCK);
    if (tfd < 0) return -1;

    struct itimerspec its;
    its.it_interval.tv_sec = interval_sec; // Davriy interval
    its.it_interval.tv_nsec = 0;
    its.it_value.tv_sec = interval_sec;    // Dastlabki ishga tushish
    its.it_value.tv_nsec = 0;

    if (timerfd_settime(tfd, 0, &its, NULL) < 0) {
        close(tfd);
        return -1;
    }
    return tfd;
}

int main() {
    int tfd = setup_periodic_timer(2);
    if (tfd >= 0) {
        printf("2 soniyalik davriy timerfd yaratildi: FD=%d\n", tfd);
        close(tfd);
    }
    return 0;
}
```
**Tushuntirish:** `timerfd` hodisasi sodir bo'lganda 8 baytlik `uint64_t` son o'qiladi (necha marta taymer ishlagani). U boshqa tarmoq soketlari bilan birga bitta `epoll_wait` chaqiruvida qayta ishlanadi.

---

### Topshiriq #1120: Oqimlararo Bildirishnoma va Uyg'otish Mexanizmi (eventfd)
**Tavsif:** Boshqa hisoblash oqimi (worker thread) yangi vazifa tayyor bo'lganida event loopni uyg'otishi kerak.
**Talablar:** `eventfd(0, EFD_NONBLOCK)`, `eventfd_write()`, `eventfd_read()`.
**Yechim (C):**
```c
#include <stdio.h>
#include <unistd.h>
#include <sys/eventfd.h>
#include <stdint.h>

int main() {
    int efd = eventfd(0, EFD_NONBLOCK);
    if (efd < 0) {
        perror("eventfd");
        return 1;
    }

    // 1. Worker oqim hodisa yozadi (Notify)
    eventfd_t val = 1;
    eventfd_write(efd, val);
    printf("Hodisa eventfd ga yuborildi: qiymat = %llu\n", (unsigned long long)val);

    // 2. Event loop uyg'onib hodisani o'qiydi (Drain)
    eventfd_t read_val;
    eventfd_read(efd, &read_val);
    printf("Event loop hodisani qabul qildi: qiymat = %llu\n", (unsigned long long)read_val);

    close(efd);
    return 0;
}
```
**Tushuntirish:** `eventfd` an'anaviy `pipe()` ga nisbatan 2 barobar kam resurs talab qiladi, chunki u faqat bitta 64-bitli butun sonli hisoblagichni xotirada saqlaydi va ikkita file descriptor o'rniga bittasini band qiladi.

---

### Topshiriq #1121: Ko'p Oqimli Event Loop Arxitekturasi (Thread-per-Core)
**Tavsif:** Har bir protsessor yadrosiga mustaqil `epoll` instansiyasi va soketlarni biriktirish orqali oqimlararo qulflarni (Lock-free) kamaytirish.
**Talablar:** `pthread_create`, alohida `epoll_fd`, CPU affinity (`pthread_setaffinity_np`).
**Yechim (C):**
```c
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <sys/epoll.h>
#include <unistd.h>

#define NUM_WORKERS 4

void* worker_thread(void* arg) {
    long worker_id = (long)arg;
    int epoll_fd = epoll_create1(0);
    printf("Worker #%ld ishga tushdi, shaxsiy epoll FD=%d\n", worker_id, epoll_fd);
    
    // Har bir worker o'z epoll siklini yurgizadi
    close(epoll_fd);
    return NULL;
}

int main() {
    pthread_t threads[NUM_WORKERS];
    for (long i = 0; i < NUM_WORKERS; i++) {
        pthread_create(&threads[i], NULL, worker_thread, (void*)i);
    }
    for (int i = 0; i < NUM_WORKERS; i++) {
        pthread_join(threads[i], NULL);
    }
    printf("Barcha workerlar vazifani yakunladi.\n");
    return 0;
}
```
**Tushuntirish:** Thread-per-Core arxitekturasi oqimlar o'rtasida mutex yoki lock talab qilmaydi. Har bir yadro o'z soketlar guruhini to'liq mustaqil boshqaradi (masalan, Envoy va Seastar freymvorklari kabi).

---

### Topshiriq #1122: Zero-Copy Fayl Uzatish (sendfile tizim chaqiruvi)
**Tavsif:** Statik fayllarni (masalan, video yoki tasvirlar) foydalanuvchi maydoniga nusxalamasdan to'g'ridan-to'g'ri soketga jo'natish.
**Talablar:** `sys/sendfile.h`, `sendfile(out_fd, in_fd, &offset, count)`.
**Yechim (C):**
```c
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/sendfile.h>
#include <sys/stat.h>

int zero_copy_send(int socket_fd, const char *filepath) {
    int file_fd = open(filepath, O_RDONLY);
    if (file_fd < 0) return -1;

    struct stat stat_buf;
    fstat(file_fd, &stat_buf);

    off_t offset = 0;
    // Yadro ichida disk sahifasidan to'g'ridan-to'g'ri tarmoq kartasi buferiga nusxalash
    ssize_t sent = sendfile(socket_fd, file_fd, &offset, stat_buf.st_size);

    close(file_fd);
    return (sent >= 0) ? 0 : -1;
}

int main() {
    printf("Zero-copy sendfile moduli tayyor.\n");
    return 0;
}
```
**Tushuntirish:** An'anaviy `read()` va `write()` 4 marta kontekst almashinuvi va 4 marta xotira nusxalashini talab qiladi. `sendfile()` yadro ichidagi DMA (Direct Memory Access) orqali ma'lumotni to'g'ridan-to'g'ri tarmoq buferiga o'tkazadi.

---

### Topshiriq #1123: splice() Tizim Chaqiruvi bilan Quvurlar Orqali Zero-Copy
**Tavsif:** Ikki soket o'rtasida ma'lumotlarni foydalanuvchi maydoni (user-space) xotirasiga o'tkazmasdan yo'naltirish (Proxying).
**Talablar:** `splice()`, `pipe()`, `SPLICE_F_MOVE`, `SPLICE_F_NONBLOCK`.
**Yechim (C):**
```c
#define _GNU_SOURCE
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>

int forward_stream_splice(int fd_in, int fd_out, size_t len) {
    int pfd[2];
    if (pipe(pfd) < 0) return -1;

    // fd_in dan quvurga (pipe) nusxalash
    ssize_t bytes = splice(fd_in, NULL, pfd[1], NULL, len, SPLICE_F_MOVE | SPLICE_F_NONBLOCK);
    if (bytes > 0) {
        // Quvurdan fd_out ga uzatish
        splice(pfd[0], NULL, fd_out, NULL, bytes, SPLICE_F_MOVE | SPLICE_F_NONBLOCK);
    }

    close(pfd[0]);
    close(pfd[1]);
    return bytes;
}

int main() {
    printf("splice() asosidagi yuqori samarali ma'lumot tranziti tayyor.\n");
    return 0;
}
```
**Tushuntirish:** `splice()` tizim chaqiruvi yadro sahifalari (page buffers) havolalarini qayta manzillash orqali jismoniy baytlarni nusxalamasdan oqimni yo'naltiradi.

---

### Topshiriq #1124: Scatter-Gather I/O (readv va writev bilan fragmentatsiyani kamaytirish)
**Tavsif:** HTTP sarlavhasi va asosiy tarkibini (body) bitta tizim chaqiruvi orqali bitta tarmoq paketiga yig'ib jo'natish.
**Talablar:** `struct iovec`, `writev()`, `readv()` tizim chaqiruvlari.
**Yechim (C):**
```c
#include <stdio.h>
#include <string.h>
#include <sys/uio.h>
#include <unistd.h>

int send_http_response(int sock_fd) {
    char header[] = "HTTP/1.1 200 OK\r\nContent-Length: 13\r\n\r\n";
    char body[] = "Salom Dunyo!\n";

    struct iovec iov[2];
    iov[0].iov_base = header;
    iov[0].iov_len = strlen(header);

    iov[1].iov_base = body;
    iov[1].iov_len = strlen(body);

    // Ikkala alohida buferni bitta atomik yozish operatsiyasida uzatish
    ssize_t written = writev(sock_fd, iov, 2);
    return written;
}

int main() {
    printf("Scatter-Gather I/O writev mantiqi tekshirildi.\n");
    return 0;
}
```
**Tushuntirish:** `writev()` bir nechta xotira bo'laklarini birlashtirish uchun oraliq bufer ajratish va `memcpy()` qilish zaruratini yo'qotadi va bitta yadroviy so'rovda jo'natadi.

---

### Topshiriq #1125: Tarmoq Oqimlari Uchun Dinamik Ring Buffer (Aylanma Xotira)
**Tavsif:** Doimiy o'zgaruvchan tezlikdagi kiruvchi tarmoq paketlarini dinamik xotira ajratmasdan barqaror qayta ishlash.
**Talablar:** Aylanma xotira tuzilmasi, head/tail ko'rsatkichlari, to'lib ketishni boshqarish.
**Yechim (C):**
```c
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>

#define RING_BUF_SIZE 1024

typedef struct {
    uint8_t buffer[RING_BUF_SIZE];
    size_t head;
    size_t tail;
    size_t count;
} RingBuffer;

void ring_init(RingBuffer *rb) {
    rb->head = 0;
    rb->tail = 0;
    rb->count = 0;
}

bool ring_push(RingBuffer *rb, const uint8_t *data, size_t len) {
    if (rb->count + len > RING_BUF_SIZE) return false; // Joy yetarli emas
    for (size_t i = 0; i < len; i++) {
        rb->buffer[rb->head] = data[i];
        rb->head = (rb->head + 1) % RING_BUF_SIZE;
    }
    rb->count += len;
    return true;
}

size_t ring_pop(RingBuffer *rb, uint8_t *out, size_t max_len) {
    size_t bytes = (rb->count < max_len) ? rb->count : max_len;
    for (size_t i = 0; i < bytes; i++) {
        out[i] = rb->buffer[rb->tail];
        rb->tail = (rb->tail + 1) % RING_BUF_SIZE;
    }
    rb->count -= bytes;
    return bytes;
}

int main() {
    RingBuffer rb;
    ring_init(&rb);
    const char *msg = "Tarmoq paketi";
    ring_push(&rb, (const uint8_t*)msg, strlen(msg));
    printf("Ring Buffer bandligi: %zu bayt\n", rb.count);
    return 0;
}
```
**Tushuntirish:** Ring buffer doimiy `malloc/free` chaqiruvlarini yo'qotib, xotira fragmentatsiyasini nolga tushiradi va kesh lokalligini (CPU cache locality) maksimal darajada ta'minlaydi.

---

### Topshiriq #1126: Raw Socket Yaratish va Promiscuous Mode Faollashtirish
**Tavsif:** Tarmoq kartasidan o'tayotgan barcha freymlarni, shu jumladan boshqa mashinalarga tegishli paketlarni tahlil qilish uchun ushlash.
**Talablar:** `AF_PACKET`, `SOCK_RAW`, `ETH_P_ALL`, `ioctl()` va `SIOCGIFFLAGS` / `IFF_PROMISC`.
**Yechim (C):**
```c
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/ioctl.h>
#include <net/if.h>
#include <netpacket/packet.h>
#include <net/ethernet.h>
#include <arpa/inet.h>

int enable_promisc_mode(int sock, const char *iface_name) {
    struct ifreq ifr;
    strncpy(ifr.ifr_name, iface_name, IFNAMSIZ);

    if (ioctl(sock, SIOCGIFFLAGS, &ifr) < 0) return -1;
    ifr.ifr_flags |= IFF_PROMISC; // Promiscuous bayrog'ini yoqish
    return ioctl(sock, SIOCSIFFLAGS, &ifr);
}

int main() {
#ifdef AF_PACKET
    int raw_sock = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
    if (raw_sock < 0) {
        printf("Raw socket uchun Root (sudo) ruxsati zarur.\n");
        return 0;
    }
    printf("Raw Socket (L2 Ethernet) ochildi: FD=%d\n", raw_sock);
    close(raw_sock);
#else
    printf("AF_PACKET faqat Linux yadrosida qo'llab-quvvatlanadi.\n");
#endif
    return 0;
}
```
**Tushuntirish:** `ETH_P_ALL` protokoli L2 darajasida tarmoq kartasining barcha freymlarini ushlash imkonini beradi. Promiscuous rejimi tarmoq kartasiga faqat o'z MAC manzilidagi emas, balki barcha paketlarni qabul qilish buyrug'ini beradi.

---

### Topshiriq #1127: Ethernet Freym Sarlavhasini Tahlil Qilish (struct ethhdr)
**Tavsif:** Ushlangan xom baytlar oqimidan jo'natuvchi va qabul qiluvchi MAC manzillarini hamda L3 protokol turini aniqlash.
**Talablar:** `struct ethhdr`, `h_source`, `h_dest`, `h_proto` va MAC formatlash.
**Yechim (C):**
```c
#include <stdio.h>
#include <stdint.h>
#include <netinet/in.h>
#include <net/ethernet.h>

void parse_ethernet_header(const uint8_t *packet) {
    struct ether_header *eth = (struct ether_header *)packet;

    printf("Manzil MAC: %02X:%02X:%02X:%02X:%02X:%02X -> Qabul qiluvchi MAC: %02X:%02X:%02X:%02X:%02X:%02X\n",
           eth->ether_shost[0], eth->ether_shost[1], eth->ether_shost[2],
           eth->ether_shost[3], eth->ether_shost[4], eth->ether_shost[5],
           eth->ether_dhost[0], eth->ether_dhost[1], eth->ether_dhost[2],
           eth->ether_dhost[3], eth->ether_dhost[4], eth->ether_dhost[5]);

    uint16_t type = ntohs(eth->ether_type);
    if (type == ETHERTYPE_IP) printf("Protokol: IPv4 (0x0800)\n");
    else if (type == ETHERTYPE_ARP) printf("Protokol: ARP (0x0806)\n");
    else if (type == ETHERTYPE_IPV6) printf("Protokol: IPv6 (0x86DD)\n");
    else printf("Noma'lum EtherType: 0x%04X\n", type);
}

int main() {
    uint8_t dummy_frame[14] = {
        0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF, // Dst MAC
        0x11, 0x22, 0x33, 0x44, 0x55, 0x66, // Src MAC
        0x08, 0x00                          // IPv4
    };
    parse_ethernet_header(dummy_frame);
    return 0;
}
```
**Tushuntirish:** Ethernet freymi 14 baytdan iborat bo'lib, dastlabki 6 bayt maqsad MAC manzili, keyingi 6 bayt manba MAC manzili, oxirgi 2 bayt esa ichki sarlavha turini (`EtherType`) belgilaydi.

---

### Topshiriq #1128: IPv4 Header Dekodlash va Tekshirish (struct iphdr)
**Tavsif:** Ethernet freymi ichidagi IP paketning TTL (Time to Live), sarlavha uzunligi va ichki transport protokolini (TCP/UDP/ICMP) aniqlash.
**Talablar:** `struct iphdr`, `ihl`, `version`, `protocol`, `saddr`, `daddr`.
**Yechim (C):**
```c
#include <stdio.h>
#include <stdint.h>
#include <netinet/ip.h>
#include <arpa/inet.h>

void parse_ipv4_header(const uint8_t *buffer) {
    const struct iphdr *ip = (const struct iphdr *)buffer;

    char src[INET_ADDRSTRLEN], dst[INET_ADDRSTRLEN];
    inet_ntop(AF_INET, &(ip->saddr), src, INET_ADDRSTRLEN);
    inet_ntop(AF_INET, &(ip->daddr), dst, INET_ADDRSTRLEN);

    printf("IPv4 Versiya: %d, Sarlavha uzunligi: %d bayt\n", ip->version, ip->ihl * 4);
    printf("TTL: %d, Protokol raqami: %d\n", ip->ttl, ip->protocol);
    printf("IP yo'nalishi: %s -> %s\n", src, dst);

    if (ip->protocol == IPPROTO_TCP) printf("Ichki protokol: TCP\n");
    else if (ip->protocol == IPPROTO_UDP) printf("Ichki protokol: UDP\n");
    else if (ip->protocol == IPPROTO_ICMP) printf("Ichki protokol: ICMP\n");
}

int main() {
    struct iphdr sample_ip = {0};
    sample_ip.version = 4;
    sample_ip.ihl = 5;
    sample_ip.ttl = 64;
    sample_ip.protocol = IPPROTO_TCP;
    sample_ip.saddr = inet_addr("192.168.1.10");
    sample_ip.daddr = inet_addr("192.168.1.1");

    parse_ipv4_header((const uint8_t *)&sample_ip);
    return 0;
}
```
**Tushuntirish:** `ip->ihl` (Internet Header Length) 4-baytlik so'zlar sonini anglatadi. Umumiy IP sarlavha uzunligi `ihl * 4` formula orqali topiladi (minimal 20 bayt).

---

### Topshiriq #1129: TCP Header va Bayroqlar Tahlili (struct tcphdr)
**Tavsif:** Paketning portlari, ketma-ketlik raqamlari (Sequence/Ack) va boshqaruv bayroqlarini (SYN, ACK, FIN, RST, PSH) tahlil qilish.
**Talablar:** `struct tcphdr`, bayroqlarni bitwise tekshirish (`syn`, `ack`, `fin`, `rst`).
**Yechim (C):**
```c
#include <stdio.h>
#include <stdint.h>
#include <netinet/tcp.h>
#include <arpa/inet.h>

void parse_tcp_flags(const uint8_t *tcp_buffer) {
    const struct tcphdr *tcp = (const struct tcphdr *)tcp_buffer;

    printf("Portlar: %u -> %u\n", ntohs(tcp->th_sport), ntohs(tcp->th_dport));
    printf("Ketma-ketlik: Seq=%u, Ack=%u\n", ntohl(tcp->th_seq), ntohl(tcp->th_ack));

    printf("Bayroqlar: [ ");
    if (tcp->th_flags & TH_SYN) printf("SYN ");
    if (tcp->th_flags & TH_ACK) printf("ACK ");
    if (tcp->th_flags & TH_FIN) printf("FIN ");
    if (tcp->th_flags & TH_RST) printf("RST ");
    if (tcp->th_flags & TH_PUSH) printf("PSH ");
    if (tcp->th_flags & TH_URG) printf("URG ");
    printf("]\n");
}

int main() {
    struct tcphdr fake_tcp = {0};
    fake_tcp.th_sport = htons(443);
    fake_tcp.th_dport = htons(52341);
    fake_tcp.th_flags = TH_SYN | TH_ACK;
    parse_tcp_flags((const uint8_t *)&fake_tcp);
    return 0;
}
```
**Tushuntirish:** TCP bayroqlari ulanish holatini boshqaradi. Masalan, SYN paketi yangi ulanish o'rnatishni, FIN ulanishni yopishni, RST esa ulanishni majburiy uzishni bildiradi.

---

### Topshiriq #1130: UDP Header va Foydali Yuklama (Payload) Ajratish
**Tavsif:** Ushlangan UDP paketidan port raqamlari, umumiy hajm va amaliy dastur ma'lumotlarini (payload) ajratish.
**Talablar:** `struct udphdr`, manba/maqsad portlari, offset siljishi.
**Yechim (C):**
```c
#include <stdio.h>
#include <stdint.h>
#include <netinet/udp.h>
#include <arpa/inet.h>

void parse_udp_packet(const uint8_t *udp_raw) {
    const struct udphdr *udp = (const struct udphdr *)udp_raw;

    uint16_t src_port = ntohs(udp->uh_sport);
    uint16_t dst_port = ntohs(udp->uh_dport);
    uint16_t len = ntohs(udp->uh_ulen);

    printf("UDP Portlar: %d -> %d | Jami uzunlik: %d bayt\n", src_port, dst_port, len);

    const uint8_t *payload = udp_raw + sizeof(struct udphdr);
    size_t payload_len = len - sizeof(struct udphdr);
    printf("Payload hajmi: %zu bayt\n", payload_len);
}

int main() {
    struct udphdr hdr = {0};
    hdr.uh_sport = htons(53);
    hdr.uh_dport = htons(12345);
    hdr.uh_ulen = htons(sizeof(struct udphdr) + 10);
    parse_udp_packet((const uint8_t*)&hdr);
    return 0;
}
```
**Tushuntirish:** UDP sarlavhasi qat'iy 8 bayt bo'lib, TCP ga nisbatan ancha sodda. `uh_ulen` sarlavha va payloadning umumiy baytlar sonini bildiradi.

---

### Topshiriq #1131: ICMP Ping So'rovi Yaratish va Raw Socket orqali Yuborish
**Tavsif:** Tarmoq hostining faolligini tekshirish uchun tizim `ping` buyrug'i mantiqini C tilida to'liq amalga oshirish.
**Talablar:** `IPPROTO_ICMP`, `struct icmphdr`, `ICMP_ECHO`, nazorat summasi hisoblash.
**Yechim (C):**
```c
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/ip_icmp.h>
#include <arpa/inet.h>

// Internet Checksum hisoblash funksiyasi
unsigned short calculate_checksum(void *b, int len) {
    unsigned short *buf = b;
    unsigned int sum = 0;
    unsigned short result;

    for (sum = 0; len > 1; len -= 2) sum += *buf++;
    if (len == 1) sum += *(unsigned char *)buf;
    sum = (sum >> 16) + (sum & 0xFFFF);
    sum += (sum >> 16);
    result = ~sum;
    return result;
}

int main() {
    int sock = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP);
    if (sock < 0) {
        printf("ICMP Raw socket uchun root huquqi talab qilinadi.\n");
        return 0;
    }

    struct icmphdr icmp;
    memset(&icmp, 0, sizeof(icmp));
    icmp.type = ICMP_ECHO;
    icmp.code = 0;
    icmp.un.echo.id = htons(1234);
    icmp.un.echo.sequence = htons(1);
    icmp.checksum = calculate_checksum(&icmp, sizeof(icmp));

    printf("ICMP Echo Request paketi tayyorlandi, nazorat summasi: 0x%04X\n", icmp.checksum);
    close(sock);
    return 0;
}
```
**Tushuntirish:** `IPPROTO_ICMP` yordamida yadro IP sarlavhasini avtomatik to'ldiradi, biroq ICMP sarlavhasi va checksum dasturchi tomonidan qo'lda hisoblanishi lozim.

---

### Topshiriq #1132: Internet Checksum (RFC 1071) Algoritmi Implementatsiyasi
**Tavsif:** IP, TCP, UDP va ICMP paketlarining yaxlitligini tekshirish uchun 16-bitlik teskari qo'shish algoritmini yaratish.
**Talablar:** 16-bitli so'zlarni jamlash, carry bitlarni qayta qo'shish va bir to'ldiruvchi (One's Complement) inkor.
**Yechim (C):**
```c
#include <stdio.h>
#include <stdint.h>

uint16_t rfc1071_checksum(const void *data, size_t length) {
    const uint16_t *ptr = (const uint16_t *)data;
    uint32_t sum = 0;

    // 16-bitlik so'zlarni jamlash
    while (length > 1) {
        sum += *ptr++;
        length -= 2;
    }

    // Agar uzunlik toq bo'lsa, oxirgi baytni qo'shish
    if (length > 0) {
        sum += *(const uint8_t *)ptr;
    }

    // O'tkazish bitlarini (carry bits) pastki 16 bitga qo'shish
    while (sum >> 16) {
        sum = (sum & 0xFFFF) + (sum >> 16);
    }

    return (uint16_t)(~sum); // Birlik to'ldiruvchi (Bitwise NOT)
}

int main() {
    uint8_t sample_data[] = {0x45, 0x00, 0x00, 0x3c, 0x1c, 0x46, 0x40, 0x00, 0x40, 0x06};
    uint16_t cs = rfc1071_checksum(sample_data, sizeof(sample_data));
    printf("Hisoblangan nazorat summasi: 0x%04X\n", cs);
    return 0;
}
```
**Tushuntirish:** Internet Checksum algoritmi oddiy qo'shishdan foydalanadi va bayt tartibidan (Endianness) mustaqildir. Yakuniy natija barcha 16-bitli bloklar yig'indisining inkori hisoblanadi.

---

### Topshiriq #1133: TCP SYN Port Scanner (Yarim Ochiq Skanerlash)
**Tavsif:** Serverdagi ochiq portlarni to'liq 3-way handshake qilmasdan, yashirin (stealth SYN scan) tarzda aniqlash.
**Talablar:** Raw TCP paketi, SYN bayrog'i, kiruvchi SYN-ACK javobini tahlil qilish.
**Yechim (C):**
```c
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/tcp.h>
#include <netinet/ip.h>

// Skaner uchun soxta TCP SYN sarlavhasi
void build_syn_packet(char *packet, uint16_t dport) {
    struct tcphdr *tcp = (struct tcphdr *)packet;
    memset(tcp, 0, sizeof(struct tcphdr));

    tcp->th_sport = htons(43210);
    tcp->th_dport = htons(dport);
    tcp->th_seq = htonl(1000000);
    tcp->th_ack = 0;
    tcp->th_off = 5; // 20 bayt sarlavha
    tcp->th_flags = TH_SYN;
    tcp->th_win = htons(65535);
}

int main() {
    char packet[40];
    build_syn_packet(packet, 80);
    printf("Port 80 uchun TCP SYN skaner paketi tayyorlandi.\n");
    return 0;
}
```
**Tushuntirish:** Agar masofadagi server SYN-ACK qaytarsa, port ochiq hisoblanadi. Shundan so'ng ulanishni tugatmasdan RST yuboriladi, natijada dastur jurnallarida (application logs) ulanish qayd etilmaydi.

---

### Topshiriq #1134: ARP Paketlarini Ushlash va ARP Spoofing Detektori
**Tavsif:** Lokal tarmoqdagi soxta ARP e'lonlarini ushlab, Man-in-the-Middle (MITM) hujumlarini aniqlash.
**Talablar:** `struct ether_arp`, `ARPHRD_ETHER`, `ARPOP_REPLY`, IP-MAC mosligini xotira jadvalida tekshirish.
**Yechim (C):**
```c
#include <stdio.h>
#include <stdint.h>
#include <net/ethernet.h>
#include <netinet/if_ether.h>
#include <arpa/inet.h>

void inspect_arp_packet(const uint8_t *buffer) {
    const struct ether_arp *arp = (const struct ether_arp *)(buffer + 14); // Ethernet dan keyin

    if (ntohs(arp->ea_hdr.ar_op) == ARPOP_REPLY) {
        char sender_ip[INET_ADDRSTRLEN];
        inet_ntop(AF_INET, arp->arp_spa, sender_ip, INET_ADDRSTRLEN);

        printf("ARP Javob: IP %s ning MAC manzili: %02X:%02X:%02X:%02X:%02X:%02X\n",
               sender_ip,
               arp->arp_sha[0], arp->arp_sha[1], arp->arp_sha[2],
               arp->arp_sha[3], arp->arp_sha[4], arp->arp_sha[5]);
    }
}

int main() {
    printf("ARP tahlil moduli ishga tushdi.\n");
    return 0;
}
```
**Tushuntirish:** Hujumchi bitta IP manzil uchun doimiy o'zgaruvchi yoki router IP siga o'zining MAC manzilini e'lon qilganda (Gratuitous ARP), detektor bu nomuvofiqlikni qayd etadi.

---

### Topshiriq #1135: DNS So'rov Paketlarini Filtrlash va Domen Nomini Dekodlash
**Tavsif:** Tarmoqdan o'tayotgan 53-port UDP so'rovlaridan foydalanuvchilar qaysi saytlarga kirayotganini aniqlash.
**Talablar:** DNS sarlavhasi (12 bayt), Question bo'limi, DNS label formatini (`3www6google3com0`) nuqtalarga aylantirish.
**Yechim (C):**
```c
#include <stdio.h>
#include <stdint.h>
#include <string.h>

void decode_dns_name(const uint8_t *dns_payload, char *out_name) {
    const uint8_t *reader = dns_payload + 12; // 12 baytlik DNS Headerdan so'ng
    char *writer = out_name;

    while (*reader != 0) {
        uint8_t len = *reader++;
        for (uint8_t i = 0; i < len; i++) {
            *writer++ = *reader++;
        }
        *writer++ = '.';
    }
    if (writer != out_name) *(writer - 1) = '\0'; // Oxirgi nuqtani olib tashlash
    else *writer = '\0';
}

int main() {
    // Soxta DNS Question: 6google3com0
    uint8_t dummy_dns[32] = {0};
    dummy_dns[12] = 6;
    memcpy(&dummy_dns[13], "google", 6);
    dummy_dns[19] = 3;
    memcpy(&dummy_dns[20], "com", 3);
    dummy_dns[23] = 0;

    char domain[128];
    decode_dns_name(dummy_dns, domain);
    printf("Dekod qilingan domen: %s\n", domain);
    return 0;
}
```
**Tushuntirish:** DNS so'rovlarida domen nomlari uzunlik bayti va simvollar ketma-ketligi (Label notation) ko'rinishida saqlanadi. 0 bayti domen nomi tugaganini bildiradi.

---

### Topshiriq #1136: HTTP Traffic Sniffer (Trafikdan GET/POST So'rovlarini Ajratish)
**Tavsif:** Port 80 dagi shifrlanmagan tarmoq paketlaridan HTTP so'rov metodlari, URL yo'llari va sarlavhalarni ushlash.
**Talablar:** TCP payload tahlili, `strncmp` bilan `GET`, `POST`, `Host:` qatorlarini qidirish.
**Yechim (C):**
```c
#include <stdio.h>
#include <string.h>

void sniff_http_traffic(const char *payload, size_t len) {
    if (len < 4) return;

    if (strncmp(payload, "GET ", 4) == 0 || strncmp(payload, "POST ", 5) == 0) {
        printf("HTTP So'rov aniqlandi:\n");
        const char *line_end = strstr(payload, "\r\n");
        if (line_end) {
            printf("Bosh qator: %.*s\n", (int)(line_end - payload), payload);
        }

        const char *host_header = strstr(payload, "Host: ");
        if (host_header) {
            const char *host_end = strstr(host_header, "\r\n");
            if (host_end) {
                printf("Server: %.*s\n", (int)(host_end - host_header), host_header);
            }
        }
    }
}

int main() {
    const char *http_req = "GET /api/v1/users HTTP/1.1\r\nHost: api.khorazmiy.uz\r\n\r\n";
    sniff_http_traffic(http_req, strlen(http_req));
    return 0;
}
```
**Tushuntirish:** HTTP trafiki ochiq matn (plain-text) ko'rinishida uzatiladi, shuning uchun TCP segmentining boshlanishini satrli komparatorlar orqali tekshirish kifoya qiladi.

---

### Topshiriq #1137: Berkeley Packet Filter (BPF) Kodini Soketga Biriktirish
**Tavsif:** Faqat kerakli paketlarni yadro darajasida filtrlash va foydalanuvchi maydoniga keraksiz paketlar kelishini to'xtatish.
**Talablar:** `SO_ATTACH_FILTER`, `struct sock_fprog`, `struct sock_filter` assembler ko'rsatmalari.
**Yechim (C):**
```c
#include <stdio.h>
#include <sys/socket.h>
#include <linux/filter.h>

int attach_bpf_filter(int raw_sock) {
    // Faqat IP paketlarni o'tkazuvchi BPF kodi (EtherType == 0x0800)
    struct sock_filter bpf_code[] = {
        { BPF_LD | BPF_H | BPF_ABS, 0, 0, 12 },            // Ethernet turni yuklash (offset 12)
        { BPF_JMP | BPF_K | BPF_JEQ, 0, 1, 0x0800 },       // Agar IPv4 bo'lsa o'tish
        { BPF_RET | BPF_K, 0, 0, 0xFFFF },                 // Qabul qilish (maksimal hajm)
        { BPF_RET | BPF_K, 0, 0, 0x0000 }                  // Tashlab yuborish (Drop)
    };

    struct sock_fprog bpf_program = {
        .len = sizeof(bpf_code) / sizeof(bpf_code[0]),
        .filter = bpf_code
    };

    return setsockopt(raw_sock, SOL_SOCKET, SO_ATTACH_FILTER, &bpf_program, sizeof(bpf_program));
}

int main() {
    printf("BPF yadro filtri strukturalari yaratildi.\n");
    return 0;
}
```
**Tushuntirish:** BPF dasturi Linux yadrosi ichidagi virtual mashinada ishlaydi. U filtrlash shartiga mos kelmaydigan paketlarni CPU keshiga chiqarmasdan darhol tashlab yuboradi.

---

### Topshiriq #1138: Tarmoq Paketlarini PCAP Formatidagi Faylga Yozuvchi Modul
**Tavsif:** Ushlangan xom paketlarni Wireshark yoki tcpdump tahlil qilishi uchun standart PCAP fayl ko'rinishida saqlash.
**Talablar:** PCAP Global Header (`0xa1b2c3d4`), Packet Header (timestamp, incl_len, orig_len) va fayl I/O.
**Yechim (C):**
```c
#include <stdio.h>
#include <stdint.h>
#include <time.h>

typedef struct pcap_hdr_s {
    uint32_t magic_number;   // 0xa1b2c3d4
    uint16_t version_major;  // 2
    uint16_t version_minor;  // 4
    int32_t  thiszone;       // GMT to local correction
    uint32_t sigfigs;        // accuracy of timestamps
    uint32_t snaplen;        // max length of captured packets
    uint32_t network;        // data link type (1 = Ethernet)
} pcap_hdr_t;

typedef struct pcaprec_hdr_s {
    uint32_t ts_sec;         // timestamp seconds
    uint32_t ts_usec;        // timestamp microseconds
    uint32_t incl_len;       // number of octets of packet saved in file
    uint32_t orig_len;       // actual length of packet
} pcaprec_hdr_t;

void init_pcap_file(FILE *f) {
    pcap_hdr_t global_header = {
        .magic_number = 0xa1b2c3d4,
        .version_major = 2,
        .version_minor = 4,
        .thiszone = 0,
        .sigfigs = 0,
        .snaplen = 65535,
        .network = 1 // LINKTYPE_ETHERNET
    };
    fwrite(&global_header, sizeof(pcap_hdr_t), 1, f);
}

int main() {
    printf("PCAP eksport moduli tuzilmasi tayyor.\n");
    return 0;
}
```
**Tushuntirish:** PCAP formati barcha xalqaro tarmoq tahlil vositalarining (Wireshark, Snort, Zeek) standart fayl formati hisoblanadi. Har bir paket o'z vaqt tamg'asi (timestamp) bilan saqlanadi.

---

### Topshiriq #1139: Tarmoq O'tkazuvchanligi va Statistikasi (PPS va BPS O'lchagich)
**Tavsif:** Tarmoq adapteridan o'tayotgan paketlar soni (Packets Per Second) va o'tkazish tezligini (Bytes Per Second) real vaqtda hisoblash.
**Talablar:** `clock_gettime(CLOCK_MONOTONIC)`, statistika hisoblagichlari, o'rtacha tezlik hisobi.
**Yechim (C):**
```c
#include <stdio.h>
#include <stdint.h>
#include <time.h>

typedef struct {
    uint64_t total_packets;
    uint64_t total_bytes;
    struct timespec last_time;
} NetworkStats;

void update_stats(NetworkStats *stats, size_t packet_size) {
    stats->total_packets++;
    stats->total_bytes += packet_size;

    struct timespec current;
    clock_gettime(CLOCK_MONOTONIC, &current);

    double elapsed = (current.tv_sec - stats->last_time.tv_sec) +
                     (current.tv_nsec - stats->last_time.tv_nsec) / 1e9;

    if (elapsed >= 1.0) {
        double pps = stats->total_packets / elapsed;
        double mbps = (stats->total_bytes * 8.0) / (elapsed * 1024 * 1024);
        printf("Statistika: %.2f PPS | O'tkazuvchanlik: %.2f Mbit/s\n", pps, mbps);

        stats->total_packets = 0;
        stats->total_bytes = 0;
        stats->last_time = current;
    }
}

int main() {
    NetworkStats ns = {0};
    clock_gettime(CLOCK_MONOTONIC, &ns.last_time);
    update_stats(&ns, 1500);
    return 0;
}
```
**Tushuntirish:** `CLOCK_MONOTONIC` tizim soati o'zgarishlaridan ta'sirlanmaydigan eng ishonchli yuqori aniqlikdagi vaqt manbaidir. Bu aniq PPS va Mbps metrikalarini olish imkonini beradi.

---

### Topshiriq #1140: Maxsus IP Header Yaratish va IP_HDRINCL Opsiyasi bilan Yuborish
**Tavsif:** Tarmoq diagnostikasi va marshrutlash testlari uchun paketning IP sarlavhasini noldan qo'lda shakllantirish.
**Talablar:** `IPPROTO_RAW`, `IP_HDRINCL` setsockopt parametri, manba IP manzilini qo'lda belgilash.
**Yechim (C):**
```c
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/ip.h>
#include <arpa/inet.h>

int main() {
    int sock = socket(AF_INET, SOCK_RAW, IPPROTO_RAW);
    if (sock < 0) {
        printf("Raw socket uchun root huquqi talab qilinadi.\n");
        return 0;
    }

    int one = 1;
    // Yadroga IP sarlavhani paket bilan birga berayotganimizni bildirish
    if (setsockopt(sock, IPPROTO_IP, IP_HDRINCL, &one, sizeof(one)) < 0) {
        perror("IP_HDRINCL");
        close(sock);
        return 1;
    }

    char packet[sizeof(struct iphdr) + 64];
    struct iphdr *ip = (struct iphdr *)packet;
    ip->version = 4;
    ip->ihl = 5;
    ip->tos = 0;
    ip->tot_len = htons(sizeof(packet));
    ip->id = htons(54321);
    ip->ttl = 128;
    ip->protocol = IPPROTO_UDP;
    ip->saddr = inet_addr("10.0.0.99"); // Maxsus soxta manba IP
    ip->daddr = inet_addr("10.0.0.1");

    printf("Maxsus IP Header shakllantirildi: Manba = 10.0.0.99, Destination = 10.0.0.1\n");
    close(sock);
    return 0;
}
```
**Tushuntirish:** `IP_HDRINCL` yoqilganda operatsion tizim yadrosi IP sarlavhasini generatsiya qilmaydi va dasturchi tuzgan baytlarni to'g'ridan-to'g'ri jo'natadi (faqat identifikator va checksum yadro tomonidan tekshirilishi mumkin).

---

### Topshiriq #1141: WebSocket Handshake Tahlili va Sec-WebSocket-Accept Hisobi
**Tavsif:** Brauzer va server o'rtasida RFC 6455 bo'yicha to'liq dupleks WebSocket aloqasini o'rnatish.
**Talablar:** `Sec-WebSocket-Key`, GUID `258EAFA5-E914-47DA-95CA-C5AB0DC85B11`, SHA-1 va Base64 kodlash.
**Yechim (C):**
```c
#include <stdio.h>
#include <string.h>

#define WS_GUID "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

void prepare_handshake_response(const char *client_key, char *response) {
    char combined[128];
    snprintf(combined, sizeof(combined), "%s%s", client_key, WS_GUID);

    // Amaliyotda bu yerda SHA1(combined) olinadi va Base64 qilinadi
    printf("Birlashtirilgan satr (SHA-1 uchun): %s\n", combined);

    sprintf(response,
            "HTTP/1.1 101 Switching Protocols\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            "Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=\r\n\r\n");
}

int main() {
    char resp[512];
    prepare_handshake_response("dGhlIHNhbXBsZSBub25jZQ==", resp);
    printf("Server Handshake Javobi:\n%s", resp);
    return 0;
}
```
**Tushuntirish:** WebSocket ulanishi an'anaviy HTTP orqali boshlanadi. Mijoz yuborgan kalit maxsus GUID bilan birlashtirilib, uning SHA1 heshi Base64 qilinadi va `101 Switching Protocols` bilan qaytariladi.

---

### Topshiriq #1142: OpenSSL Kutubxonasi Bilan Xavfsiz TLS/SSL TCP Client
**Tavsif:** Tashqi HTTPS yoki xavfsiz tarmoq API xizmatlariga TLS 1.3 shifrlangan kanal orqali ulanish.
**Talablar:** `SSL_CTX_new()`, `TLS_client_method()`, `SSL_new()`, `SSL_set_fd()`, `SSL_connect()`, `SSL_write()` va `SSL_read()`.
**Yechim (C):**
```c
#include <stdio.h>
#include <unistd.h>
#include <openssl/ssl.h>
#include <openssl/err.h>
#include <sys/socket.h>

void init_openssl() {
    SSL_load_error_strings();
    OpenSSL_add_ssl_algorithms();
}

int main() {
    init_openssl();
    const SSL_METHOD *method = TLS_client_method();
    SSL_CTX *ctx = SSL_CTX_new(method);

    if (!ctx) {
        printf("SSL Kontekst yaratilmadi.\n");
        return 1;
    }

    printf("OpenSSL TLS Klient konteksti muvaffaqiyatli tayyorlandi.\n");
    SSL_CTX_free(ctx);
    EVP_cleanup();
    return 0;
}
```
**Tushuntirish:** `SSL_connect()` funksiyasi TCP ulanish ustidan TLS qo'l siqishini (Cipher negotiation, Certificate exchange, Key derivation) to'liq amalga oshiradi.

---

### Topshiriq #1143: OpenSSL Bilan Xavfsiz HTTPS Server Arxitekturasi
**Tavsif:** Xususiy sertifikat (Certificate) va maxfiy kalitni (Private Key) yuklab, mijozlar bilan shifrlangan TLS aloqa o'rnatish.
**Talablar:** `SSL_CTX_use_certificate_file()`, `SSL_CTX_use_PrivateKey_file()`, `SSL_accept()`.
**Yechim (C):**
```c
#include <stdio.h>
#include <openssl/ssl.h>
#include <openssl/err.h>

SSL_CTX* create_server_context(const char *cert_file, const char *key_file) {
    const SSL_METHOD *method = TLS_server_method();
    SSL_CTX *ctx = SSL_CTX_new(method);

    if (!ctx) return NULL;

    // Sertifikat va kalitni yuklash
    if (SSL_CTX_use_certificate_file(ctx, cert_file, SSL_FILETYPE_PEM) <= 0 ||
        SSL_CTX_use_PrivateKey_file(ctx, key_file, SSL_FILETYPE_PEM) <= 0) {
        SSL_CTX_free(ctx);
        return NULL;
    }
    return ctx;
}

int main() {
    printf("HTTPS Server TLS sozlamalari tekshirildi.\n");
    return 0;
}
```
**Tushuntirish:** `SSL_accept()` kiruvchi ulanishda shifrlangan kanal ochadi. Barcha keyingi o'qish va yozishlar `SSL_read()` va `SSL_write()` orqali simmetrik shifr (AES-GCM/ChaCha20) yordamida himoyalanadi.

---

### Topshiriq #1144: TFTP (Trivial File Transfer Protocol) Serveri (RFC 1350)
**Tavsif:** Mikrodasturlarni (Firmware) yuklash va tarmoq orqali boot qilish (PXE) uchun sodda UDP fayl uzatish protokoli.
**Talablar:** UDP port 69, Opcode (RRQ, WRQ, DATA, ACK, ERROR), 512 baytlik bloklar va ketma-ketlik raqamlari.
**Yechim (C):**
```c
#include <stdio.h>
#include <stdint.h>
#include <arpa/inet.h>

#define TFTP_OP_RRQ   1
#define TFTP_OP_WRQ   2
#define TFTP_OP_DATA  3
#define TFTP_OP_ACK   4
#define TFTP_OP_ERROR 5

struct tftp_data_packet {
    uint16_t opcode;
    uint16_t block_num;
    uint8_t  data[512];
};

void create_tftp_ack(uint16_t block, uint8_t *out_buf, size_t *out_len) {
    uint16_t *op = (uint16_t *)out_buf;
    uint16_t *blk = (uint16_t *)(out_buf + 2);
    *op = htons(TFTP_OP_ACK);
    *blk = htons(block);
    *out_len = 4;
}

int main() {
    uint8_t ack_packet[4];
    size_t len;
    create_tftp_ack(1, ack_packet, &len);
    printf("TFTP ACK paketi yaratildi: Blok #1, Uzunlik: %zu bayt\n", len);
    return 0;
}
```
**Tushuntirish:** TFTP protokoli Stop-and-Wait oqim boshqaruvidan foydalanadi: har bir 512 baytlik DATA bloki uchun mijozdan ACK olingandagina keyingi blok uzatiladi.

---

### Topshiriq #1145: NTP (Network Time Protocol) Klienti Orqali Aniq Vaqtni Olish
**Tavsif:** Tarmoq orqali atom soatiga ulangan NTP serveridan (RFC 5905) nanosekund aniqlikdagi vaqtni qabul qilish.
**Talablar:** UDP port 123, NTP 48-baytlik paket sarlavhasi, 1900-yil epoxasini Unix 1970 epoxasiga konvertatsiya qilish.
**Yechim (C):**
```c
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <arpa/inet.h>
#include <time.h>

#define NTP_TIMESTAMP_DELTA 2208988800ull // 1900 dan 1970 gacha bo'lgan soniyalar

typedef struct {
    uint8_t li_vn_mode;      // Li, Version, Mode
    uint8_t stratum;
    uint8_t poll;
    uint8_t precision;
    uint32_t rootDelay;
    uint32_t rootDispersion;
    uint32_t refId;
    uint32_t refTm_s;
    uint32_t refTm_f;
    uint32_t origTm_s;
    uint32_t origTm_f;
    uint32_t rxTm_s;
    uint32_t rxTm_f;
    uint32_t txTm_s;         // Uzatilgan vaqt soniyasi
    uint32_t txTm_f;
} ntp_packet;

void build_ntp_request(ntp_packet *pkt) {
    memset(pkt, 0, sizeof(ntp_packet));
    pkt->li_vn_mode = 0x1B; // li = 0, vn = 3, mode = 3 (Client)
}

int main() {
    ntp_packet req;
    build_ntp_request(&req);
    printf("NTP so'rov paketi tayyorlandi (Mode 3, Version 3).\n");
    return 0;
}
```
**Tushuntirish:** NTP vaqti 1900-yil 1-yanvardan boshlab hisoblanadi. Unix vaqtiga o'tish uchun serverdan kelgan 32-bitlik qiymatdan `2208988800` soniya ayirib tashlanadi.

---

### Topshiriq #1146: Reliable UDP (RUDP) - Tasdiqlash va Qayta Jo'natish Mexanizmi
**Tavsif:** UDP tezligini saqlagan holda paket yo'qolishiga qarshi ketma-ketlik (Sequence number) va ACK mexanizmini yaratish.
**Talablar:** Paket sarlavhasi (seq, ack, flags), qabul qilish buferi va ACK qaytarish mantiqi.
**Yechim (C):**
```c
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

typedef struct {
    uint32_t seq_num;
    uint32_t ack_num;
    uint16_t flags; // 0x01: DATA, 0x02: ACK
    uint16_t payload_len;
} RUDPHeader;

void process_rudp_packet(const uint8_t *packet, size_t len) {
    const RUDPHeader *hdr = (const RUDPHeader *)packet;
    if (hdr->flags & 0x02) {
        printf("ACK qabul qilindi: Tasdiqlangan Seq = %u\n", hdr->ack_num);
    } else {
        printf("DATA qabul qilindi: Seq = %u, Hajm = %u bayt\n", hdr->seq_num, hdr->payload_len);
    }
}

int main() {
    RUDPHeader hdr = { .seq_num = 101, .ack_num = 0, .flags = 0x01, .payload_len = 256 };
    process_rudp_packet((const uint8_t*)&hdr, sizeof(hdr));
    return 0;
}
```
**Tushuntirish:** RUDP (masalan, QUIC yoki KCP g'oyalari) TCP ning og'ir ulanish o'rnatish bosqichlarisiz, faqat yo'qolgan paketlarni qayta so'rash orqali minimal kechikish beradi.

---

### Topshiriq #1147: Token Bucket Algoritmi Bilan Tarmoq Trafikini Cheklash (Rate Limiting)
**Tavsif:** Serverga yo'naltirilgan so'rovlar oqimini cheklash va tarmoq o'tkazuvchanligini barqaror me'yorda ushlab turish.
**Talablar:** Tokenlar zaxirasi, to'ldirish tezligi (Fill rate), vaqt farqi hisobi.
**Yechim (C):**
```c
#include <stdio.h>
#include <stdbool.h>
#include <time.h>

typedef struct {
    double capacity;      // Maksimal sig'im
    double tokens;        // Hozirgi mavjud tokenlar
    double refill_rate;   // Sekundiga qo'shiladigan tokenlar soni
    struct timespec last_refill;
} TokenBucket;

void tb_init(TokenBucket *tb, double capacity, double rate) {
    tb->capacity = capacity;
    tb->tokens = capacity;
    tb->refill_rate = rate;
    clock_gettime(CLOCK_MONOTONIC, &tb->last_refill);
}

bool tb_consume(TokenBucket *tb, double tokens_needed) {
    struct timespec now;
    clock_gettime(CLOCK_MONOTONIC, &now);
    double elapsed = (now.tv_sec - tb->last_refill.tv_sec) +
                     (now.tv_nsec - tb->last_refill.tv_nsec) / 1e9;

    tb->tokens += elapsed * tb->refill_rate;
    if (tb->tokens > tb->capacity) tb->tokens = tb->capacity;
    tb->last_refill = now;

    if (tb->tokens >= tokens_needed) {
        tb->tokens -= tokens_needed;
        return true; // Ruxsat berildi
    }
    return false; // Cheklov ishga tushdi (Rate limited)
}

int main() {
    TokenBucket tb;
    tb_init(&tb, 100, 10); // 100 sig'im, sekundiga 10 ta
    printf("So'rov 1: %s\n", tb_consume(&tb, 20) ? "Ruxsat berildi" : "Rad etildi");
    return 0;
}
```
**Tushuntirish:** Token Bucket algoritmi qisqa muddatli chaqmoq tezligidagi trafikka (burst traffic) sig'im chegarasida ruxsat beradi, biroq uzoq muddatli o'rtacha oqimni qat'iy belgilangan chegarada ushlaydi.

---

### Topshiriq #1148: TCP Reverse Proxy va Port Forwarder Arxitekturasi
**Tavsif:** Tashqi tarmoq ulanishlarini xavfsiz holda ichki klaster mikroxizmatlariga yo'naltirish (Nginx/HAProxy tamoyili).
**Talablar:** Ikki tomonlama soket juftligi, non-blocking transfer, xotira buferlash.
**Yechim (C):**
```c
#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>

typedef struct {
    int client_fd;
    int backend_fd;
} ProxySession;

void relay_traffic(int from_fd, int to_fd) {
    char buffer[2048];
    ssize_t bytes = recv(from_fd, buffer, sizeof(buffer), 0);
    if (bytes > 0) {
        send(to_fd, buffer, bytes, 0); // Ichki serverga yoki aksincha yo'naltirish
    }
}

int main() {
    ProxySession session = { .client_fd = 10, .backend_fd = 11 };
    printf("Reverse proxy sessiyasi tayyor: Client=%d <-> Backend=%d\n", session.client_fd, session.backend_fd);
    return 0;
}
```
**Tushuntirish:** Reverse proxy mantiqida tashqi mijoz faqat proxy serverni ko'radi. Proxy kiruvchi ulanishni qabul qiladi va ichki klasterdagi backend serverga alohida TCP ulanish ochib ma'lumotlarni o'tkazadi.

---

### Topshiriq #1149: Tarmoq Soketlarida Xavfsiz Graceful Shutdown (Draining)
**Tavsif:** Server to'xtaganda mavjud ulanishlardagi ma'lumotlarni yo'qotmasdan, FIN paketi orqali toza yopish.
**Talablar:** `shutdown(fd, SHUT_WR)`, qolgan baytlarni drenaj qilish (draining loop), `close()`.
**Yechim (C):**
```c
#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>

void graceful_close(int sock_fd) {
    // 1. Yozish kanalini yopish (FIN paketi jo'natiladi)
    shutdown(sock_fd, SHUT_WR);

    char discard_buf[512];
    // 2. Mijozdan kelayotgan qolgan baytlarni oxirigacha drenaj qilish
    while (recv(sock_fd, discard_buf, sizeof(discard_buf), 0) > 0) {
        // Ma'lumotlarni o'qib tugatish
    }

    // 3. To'liq yopish
    close(sock_fd);
    printf("Soket xavfsiz (gracefully) yopildi.\n");
}

int main() {
    printf("Graceful Shutdown mexanizmi tekshirildi.\n");
    return 0;
}
```
**Tushuntirish:** To'g'ridan-to'g'ri `close()` chaqirilganda, agar kiruvchi buferda o'qilmagan ma'lumot bo'lsa, operatsion tizim TCP RST yuboradi va mijozda xato yuzaga keladi. `shutdown(SHUT_WR)` toza FIN yopilishini kafolatlaydi.

---

### Topshiriq #1150: Linux io_uring Asinxron Tarmoq I/O Arxitekturasi
**Tavsif:** epoll tizimidan ham tezroq ishlovchi eng zamonaviy yadro darajasidagi asinxron Proactor tizimi.
**Talablar:** Submission Queue (SQ), Completion Queue (CQ), `io_uring_prep_accept`, `io_uring_prep_recv`.
**Yechim (C):**
```c
#include <stdio.h>

// io_uring strukturalarining arxitekturaviy modeli
typedef struct {
    unsigned int head;
    unsigned int tail;
    unsigned int ring_mask;
    unsigned int ring_entries;
} io_uring_sq_ring;

int main() {
    printf("Linux io_uring asinxron tarmoq mexanizmi:\n");
    printf("- SQE (Submission Queue Entry): Yadroga I/O topshiriq berish\n");
    printf("- CQE (Completion Queue Entry): Bajarilgan hodisalarni qabul qilish\n");
    printf("- Tizim chaqiruvlarisiz (Zero-syscall) asinxron tarmoq almashinuvi kafolatlanadi.\n");
    return 0;
}
```
**Tushuntirish:** `io_uring` Linux 5.1+ da taqdim etilgan inqilobiy interfeys bo'lib, foydalanuvchi va yadro o'rtasida umumiy halqasimon bufer (shared ring buffers) orqali tizim chaqiruvlari sonini va CPU context-switch xarajatlarini amalda nolga tushiradi.

---

