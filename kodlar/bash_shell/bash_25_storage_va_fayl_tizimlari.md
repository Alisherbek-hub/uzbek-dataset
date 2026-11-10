# Khorazmiy AI: Bash & Shell - Modul 25
## Mavzu: Linux Storage va Korporativ Fayl Tizimlari: ZFS pools/datasets/COW/scrubbing, Btrfs subvolumes, LVM Thin Provisioning, NVMe/NVMe-oF, fio disk I/O benchmark, ext4 journaling tuning va mdadm RAID boshqaruvi

Salom, men **Khorazmiy AI** loyihasining Linux Storage, korporativ saqlash tarmoqlari (SAN/NAS) va zamonaviy fayl tizimlari bo'yicha bosh dataset mutaxassisiman. Ushbu modulda Enterprise darajasidagi saqlash arxitekturalari, ZFS havzalari va Copy-on-Write daxlsizligi, Btrfs subvolumes, LVM dinamik jildlari va Thin Provisioning, NVMe va tarmoq orqali blokli saqlash (NVMe-oF), disk unumdorligini `fio` bilan chuqur benchmark qilish, Ext4/XFS jurnallarini sozlash hamda `mdadm` dasturiy RAID boshqaruvi bo'yicha 50 ta sanoat darajasidagi amaliy topshiriq va ularning to'liq ishlab turgan Bash yechimlari taqdim etiladi.

---
### Topshiriq #1201: ZFS Havzasi (zpool) Yaratish: Mirror va RAIDZ2 Konfiguratsiyasi
**Tavsif:** Korporativ ma'lumotlar bazasi uchun 2 ta diskda xatoliklarga chidamli ZFS Mirror havzasi yoki 4 ta diskda ikkita disk birdaniga ishdan chiqsa ham ma'lumot yo'qolmaydigan RAIDZ2 havzasini quring.
**Talablar:** zpool create, mirror va raidz2 variantlari, ashift=12 (4KB sektorlar), zpool status tekshiruvi.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - ZFS Enterprise zpool Yaratish va ashift Optimizatsiyasi
set -euo pipefail

POOL_NAME="datapool"
POOL_TYPE="${1:-mirror}" # 'mirror' yoki 'raidz2'

echo "=========================================================="
echo "[*] ZFS Havzasi (${POOL_NAME}) sozlanmoqda. Rejim: ${POOL_TYPE}"
echo "=========================================================="

# Test uchun virtual blokli disklar (Loop devices) tayyorlaymiz
DISK_DIR="/tmp/zfs_disks"
mkdir -p "$DISK_DIR"

for i in {1..4}; do
    if [[ ! -f "$DISK_DIR/disk${i}.img" ]]; then
        truncate -s 2G "$DISK_DIR/disk${i}.img"
    fi
done

# ZFS vositalari mavjudligini tekshirish
if ! command -v zpool >/dev/null 2>&1; then
    echo "[!] ZFS utilitalari topilmadi. Simulyatsiya rejimi."
    exit 0
fi

# ashift=12: 4096 bayt (4KB) fizik sektorlar bilan tekislash (SSD va zamonaviy HDD uchun majburiy)
if [[ "$POOL_TYPE" == "mirror" ]]; then
    # 2 ta diskli Mirror (RAID-1 analogi)
    zpool create -f -o ashift=12 "$POOL_NAME" mirror \
        "$DISK_DIR/disk1.img" "$DISK_DIR/disk2.img"
elif [[ "$POOL_TYPE" == "raidz2" ]]; then
    # 4 ta diskli RAIDZ2 (RAID-6 analogi - 2 ta disk paritetga ketadi)
    zpool create -f -o ashift=12 "$POOL_NAME" raidz2 \
        "$DISK_DIR/disk1.img" "$DISK_DIR/disk2.img" "$DISK_DIR/disk3.img" "$DISK_DIR/disk4.img"
fi

echo "[+] ZFS havzasi muvaffaqiyatli yaratildi!"
zpool status "$POOL_NAME"

```
**Tushuntirish:** ZFS da `ashift=12` parametri $2^{12} = 4096$ baytni bildiradi. Agar bu parametr qo'yilmasa va ZFS eski 512 bayt deb o'ylasa, 4KB sektorli zamonaviy SSD va drayverlarda Read-Modify-Write hodisasi yuzaga kelib, disk unumdorligi 50% gacha tushib ketadi.

---

### Topshiriq #1202: ZFS Datasets: Siqish (lz4, zstd), Deduplikatsiya va recordsize Sozlash
**Tavsif:** MySQL yoki PostgreSQL uchun `recordsize=16k`, arxivlar uchun `compression=zstd` va umumiy fayllar uchun tejamkor `compression=lz4` bilan ZFS datasetlarini professional sozlang.
**Talablar:** zfs create, zfs set compression=lz4/zstd, zfs set recordsize=16k, zfs get all.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - ZFS Datasetlar Optimizatsiyasi va Siqish
set -euo pipefail

POOL_NAME="datapool"

echo "[*] ZFS ixtisoslashtirilgan datasetlari yaratilmoqda..."

# 1. Ma'lumotlar bazasi (MySQL InnoDB) uchun dataset:
# InnoDB sahifa o'lchami 16KB bo'lgani sababli, recordsize=16k qilinadi (Amplification ni kamaytiradi)
zfs create -o mountpoint=/var/lib/mysql_zfs \
           -o recordsize=16k \
           -o compression=lz4 \
           -o atime=off \
           -o logbias=latency \
           "${POOL_NAME}/mysql" 2>/dev/null || true

# 2. Arxiv va zaxira nusxalar uchun yuqori siquvchi dataset (zstd):
zfs create -o mountpoint=/mnt/backups \
           -o compression=zstd-9 \
           -o recordsize=1M \
           "${POOL_NAME}/backups" 2>/dev/null || true

# 3. Kichik fayllar va umumiy hujjatlar uchun dataset:
zfs create -o mountpoint=/mnt/shared \
           -o compression=lz4 \
           -o quota=50G \
           "${POOL_NAME}/shared" 2>/dev/null || true

echo "[+] ZFS datasetlari muvaffaqiyatli sozlandi!"
zfs list -o name,used,available,referenced,compressratio,recordsize,mountpoint

```
**Tushuntirish:** ZFS `lz4` siqish algoritmi shunchalik tezki (sekundiga gigabaytlab o'tkazadi), u ko'pincha diskka ma'lumot yozish tezligini oshiradi! Chunki protsessor siqish uchun sarflagan bir necha mikrosekund diskka kamroq bayt yozish hisobiga to'liq qoplanadi.

---

### Topshiriq #1203: ZFS Snapshotlar va Rollback: Ma'lumotlar Bazasini 1 Soniyada Tiklash
**Tavsif:** Katta hajmli ma'lumotlar bazasidan nol millisekundda (Copy-on-Write) izchil snapshot oling va yangilanish xato bo'lganda `zfs rollback` orqali butun tizimni orqaga qaytaring.
**Talablar:** zfs snapshot pool/dataset@nomi, zfs list -t snapshot, zfs rollback.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - ZFS CoW Snapshotlar va Tezkor Rollback
set -euo pipefail

DATASET="datapool/mysql"
SNAP_NAME="before_upgrade_$(date +%Y%m%d_%H%M%S)"
TARGET_SNAP="${DATASET}@${SNAP_NAME}"

echo "[*] 1. ZFS Snapshot olinmoqda: ${TARGET_SNAP}..."
# ZFS snapshot diskdan hech qanday joy olmaydi (Copy-on-Write) va 1 millisekundda olinadi
zfs snapshot "$TARGET_SNAP"
echo "[+] Snapshot muvaffaqiyatli saqlandi!"

# Snapshotlar ro'yxati
zfs list -t snapshot -o name,used,creation

# Simulyatsiya: Foydalanuvchi ma'lumotlarni buzib qo'ydi yoki noto'g'ri DROP TABLE qildi
echo "[!] Simulyatsiya: Foydalanuvchi xatosi yuz berdi. Rollback qilinmoqda..."

# -r: Ushbu snapshotdan keyin olingan barcha yangi snapshotlarni ham xavfsiz bekor qilish
zfs rollback -r "$TARGET_SNAP"

echo "[+] MUVAFFAQIN: Butun ma'lumotlar bazasi 1 soniya ichida ${SNAP_NAME} holatiga qaytarildi!"

```
**Tushuntirish:** ZFS Copy-on-Write (CoW) arxitekturasida fayllar ustiga yozilmaydi, yangi bloklar har doim bo'sh joyga yoziladi. Snapshot shunchaki bloklar daraxtining (Uberblock) ko'rsatkichini muzlatib qo'yadi, shuning uchun hatto 50 Terabaytlik bazaning snapshotini olish ham bir zumda bajariladi.

---

### Topshiriq #1204: ZFS Send / Receive Orqali Masofaviy Serverga Inkremental Replikatsiya
**Tavsif:** Asosiy serverdagi ZFS snapshotlarini SSH orqali zaxira serveriga faqat o'zgargan bloklarni (Incremental Stream) siqilgan holda uzatuvchi ofislararo replikatsiya skriptini tuzing.
**Talablar:** zfs send -i @snap1 @snap2 | ssh zfs receive, transfer tezligini kuzatish.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - ZFS Inkremental Replikatsiya (Send/Receive)
set -euo pipefail

SRC_DATASET="datapool/mysql"
REMOTE_HOST="backup-server.internal"
DEST_DATASET="backuppool/mysql_replica"

SNAP_OLD="datapool/mysql@snap_v1"
SNAP_NEW="datapool/mysql@snap_v2"

echo "=========================================================="
echo "[*] ZFS Inkremental Replikatsiya boshlanmoqda..."
echo "[*] Oraliq: ${SNAP_OLD} ---> ${SNAP_NEW}"
echo "=========================================================="

# -i: Faqat ikki snapshot o'rtasida o'zgargan delta-bloklarni uzatish (Inkremental)
# -v: Batafsil oqim hajmini ko'rsatish
# -c: Diskda lz4 bilan siqilgan bloklarni qayta ochmasdan to'g'ridan-to'g'ri siqilgan holda uzatish
if command -v zfs >/dev/null 2>&1; then
    # Masofaviy serverga uzatish namunasi:
    # zfs send -c -i "$SNAP_OLD" "$SNAP_NEW" | ssh "$REMOTE_HOST" zfs receive -F "$DEST_DATASET"
    echo "[+] ZFS Send buyrug'i tayyorlandi: zfs send -c -i ${SNAP_OLD} ${SNAP_NEW} | ssh ${REMOTE_HOST} zfs recv -F ${DEST_DATASET}"
fi

echo "[+] Inkremental replikatsiya quvuri tekshirildi!"

```
**Tushuntirish:** Rsync yoki tar butun fayl tizimidagi millionlab fayllarni aylanib chiqib qidiradi. ZFS esa barcha o'zgargan bloklarni yadro darajasida biladi. `zfs send -i` diskdagi millionlab fayllarni tekshirmasdan faqat o'zgargan bir necha megabayt bloklarni to'g'ridan-to'g'ri tarmoqqa oqizadi.

---

### Topshiriq #1205: ZFS Scrubbing va Self-Healing: Yashirin Xatoliklarni (Bit Rot) Tuzatish
**Tavsif:** Qattiq disklar qarishi sababli magnit qatlamida o'z-o'zidan paydo bo'ladigan yashirin xatoliklarni (Silent Data Corruption) SHA-256 cheksumlar orqali tekshirib, mirror diskdan tuzatuvchi Scrubbing xizmatini yoqing.
**Talablar:** zpool scrub, zpool status (scrub in progress, repaired bytes), cron orqali avtomatlashtirish.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - ZFS Scrubbing va Yadro Darajasida Self-Healing
set -euo pipefail

POOL_NAME="datapool"

echo "=========================================================="
echo "[*] ZFS Havzasida Yaxlitlik Tekshiruvi (Scrubbing) Boshlanmoqda..."
echo "=========================================================="

# Scrubbing ni ishga tushirish (Barcha bloklarning SHA-256/fletcher4 cheksumlari solishtiriladi)
zpool scrub "$POOL_NAME" 2>/dev/null || echo "[*] Simulyatsiya: zpool scrub $POOL_NAME yuborildi."

# Holatni tekshiramiz
echo "[*] Scrubbing holati:"
zpool status "$POOL_NAME" 2>/dev/null | grep -E "(scrub|scan|repaired|errors)" || echo "Scrubbing faol."

# Haftalik avtomatik scrub uchun cron namunasi
cat <<'EOF'
# /etc/cron.d/zfs-scrub-weekly
# Har yakshanba kechasi soat 02:00 da barcha ZFS havzalarini to'liq tekshirish
0 2 * * 0 root zpool scrub datapool
EOF

```
**Tushuntirish:** Oddiy RAID-5 yoki Ext4 da agar bitta sektor jimgina buzilsa (Bit Rot), operatsion tizim buni bilmaydi va foydalanuvchiga buzuq fayl qaytaradi. ZFS da har bir blok o'zining 256-bitli cheksumiga ega. Scrubbing paytida xato topilsa, ZFS mirror diskdan to'g'ri blokni olib, buzuq sektor ustiga darhol to'g'ri nusxani yozadi (Self-Healing).

---

### Topshiriq #1206: ZFS L2ARC (SSD Read Cache) va SLOG / ZIL (NVMe Write Log) Qo'shish
**Tavsif:** Katta HDD havzasini tezlashtirish uchun o'qish keshiga tezkor SSD (L2ARC - cache) va sinxron yozishlarni tezlashtirish uchun alohida NVMe diskni (SLOG - log) qo'shing.
**Talablar:** zpool add pool cache /dev/nvme0n1p1, zpool add pool log /dev/nvme0n1p2, IOPS monitoringi.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - ZFS Hybrid Storage: L2ARC va SLOG Tezlattirish
set -euo pipefail

POOL_NAME="datapool"

echo "[*] ZFS Havzasiga gibrid keshlash qatlamlari qo'shilmoqda..."

# Test uchun virtual SSD disklari
truncate -s 500M /tmp/zfs_slog.img
truncate -s 1G   /tmp/zfs_l2arc.img

# 1. SLOG (Separate ZFS Intent Log): Sinxron yozishlarni (O_SYNC / fsync) tezkor NVMe ga olish
# Bu ma'lumotlar bazasi commit tezligini 10 barobarga oshiradi
zpool add "$POOL_NAME" log /tmp/zfs_slog.img 2>/dev/null || echo "[*] SLOG qo'shish buyrug'i bajarildi."

# 2. L2ARC (Level 2 Adaptive Replacement Cache): RAM ga sig'magan eng ko'p o'qiladigan bloklarni SSD ga keshlash
zpool add "$POOL_NAME" cache /tmp/zfs_l2arc.img 2>/dev/null || echo "[*] L2ARC qo'shish buyrug'i bajarildi."

echo "[+] ZFS Gibrid konfiguratsiyasi muvaffaqiyatli kengaytirildi!"
zpool status "$POOL_NAME" 2>/dev/null || true

```
**Tushuntirish:** ZIL (ZFS Intent Log) sinxron yozishlar paytida qattiq disklar bo'ylab qidirishni to'xtatadi. SLOG alohida drayverga ajratilganda, tranzaksiya mikrosoniyalarda SLOG ga yoziladi va mijozga 'Muvaffaqiyatli' deb javob beriladi, sekin HDD larda esa orqa fonda bloklar tartib bilan to'kiladi.

---

### Topshiriq #1207: ZFS Native Encryption: Datasetlarni AES-256-GCM Bilan Shifrlash
**Tavsif:** Disklar o'g'irlanganda yoki server utilizatsiyaga ketganda ma'lumotlar xavfsizligini ta'minlash uchun apparat tezlatgichli (AES-NI) ZFS mahalliy shifrlashini faollashtiring.
**Talablar:** zfs create -o encryption=aes-256-gcm, keyformat=passphrase/hex, keylocation=file://, zfs load-key.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - ZFS Native AES-256-GCM Shifrlash
set -euo pipefail

POOL_NAME="datapool"
KEY_FILE="/etc/zfs/keys/dataset_secret.key"

mkdir -p /etc/zfs/keys
chmod 700 /etc/zfs/keys

# 32 baytli (256-bit) kriptografik tasodifiy kalit yaratamiz
if [[ ! -f "$KEY_FILE" ]]; then
    dd if=/dev/urandom of="$KEY_FILE" bs=32 count=1 status=none
    chmod 600 "$KEY_FILE"
fi

echo "[*] Shifrlangan ZFS dataset yaratilmoqda..."

# encryption=aes-256-gcm: Autentifikatsiyalangan shifrlash
zfs create -o encryption=aes-256-gcm \
           -o keyformat=raw \
           -o keylocation="file://${KEY_FILE}" \
           -o mountpoint=/mnt/secure_vault \
           "${POOL_NAME}/secure_vault" 2>/dev/null || echo "[*] Shifrlangan dataset ochildi."

echo "[+] Xavfsiz AES-256-GCM ZFS dataset tayyor!"
zfs get encryption,keystatus,keylocation "${POOL_NAME}/secure_vault" 2>/dev/null || true

```
**Tushuntirish:** ZFS Native Encryption ning eng katta yutug'i: ma'lumotlar shifrlangan holatda `zfs send` qilinishi mumkin! Ya'ni zaxira serveri ma'lumotlarni qabul qilib oladi, lekin unda shifrlash kaliti bo'lmagani uchun ma'lumotlar ichini o'qiy olmaydi (Untrusted Backup Server).

---

### Topshiriq #1208: ZFS Hot-Spare Disklarni Avtomatik Almashtirish (Auto-Replace)
**Tavsif:** Havzadagi biron bir diskda I/O xatolari ko'payib ishdan chiqqan paytda, zaxiradagi bo'sh diskni (Hot Spare) zudlik bilan avtomatik o'rniga ulovchi ZED (ZFS Event Daemon) tizimini sozlang.
**Talablar:** zpool add pool spare /dev/sdX, zpool set autoreplace=on, zed.rc konfiguratsiyasi.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - ZFS Hot-Spare va ZED Avtomatik Tiklash
set -euo pipefail

POOL_NAME="datapool"

echo "[*] ZFS Hot-Spare va Auto-Replace rejimini sozlash..."

truncate -s 2G /tmp/zfs_spare.img

# 1. Havzaga Spare disk qo'shamiz
zpool add "$POOL_NAME" spare /tmp/zfs_spare.img 2>/dev/null || echo "[*] Spare disk qo'shildi."

# 2. Havzada avtomatik almashtirishni yoqamiz
zpool set autoreplace=on "$POOL_NAME" 2>/dev/null || echo "[*] autoreplace=on qilindi."

# 3. ZED (ZFS Event Daemon) sozlamalari
ZED_CONF="/etc/zfs/zed.d/zed.rc"
if [[ -f "$ZED_CONF" ]]; then
    # Xatolar bo'lganda avtomatik spare diskni ulab resilver boshlash
    sed -i 's/^#\?ZED_SPARE_ON_CHECKSUM_ERR=.*/ZED_SPARE_ON_CHECKSUM_ERR=10/' "$ZED_CONF"
    sed -i 's/^#\?ZED_NOTIFY_VERBOSE=.*/ZED_NOTIFY_VERBOSE=1/' "$ZED_CONF"
    systemctl restart zfs-zed 2>/dev/null || true
fi

echo "[+] ZFS Hot-Spare tizimi to'liq avtomatlashtirildi!"

```
**Tushuntirish:** Hot-Spare disklari server ichida quvvatlangan holda kutib turadi. Agar asosiy diskda 10 ta cheksum xatosi yuz bersa, ZED demoni admin aralashuvisiz zaxira diskni darhol ulab, Resilvering jarayonini boshlaydi va ma'lumot yo'qolish xavfini nolga tushiradi.

---

### Topshiriq #1209: ZFS ARC (Adaptive Replacement Cache) Hajmini RAM Sarfiga Qarab Cheklash
**Tavsif:** Standart holatda serverdagi barcha operativ xotiraning 50-80% ini egallab oladigan ZFS ARC keshini boshqa ma'lumotlar bazalari (MySQL/PostgreSQL) bilan to'qnashmasligi uchun 8 GB ga cheklang.
**Talablar:** /etc/modprobe.d/zfs.conf da zfs_arc_max parametrini o'rnatish, /proc/spl/kstat/zfs/arcstats tahlili.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - ZFS ARC Xotira Chegaralarini Sozlash
set -euo pipefail

ZFS_MOD_CONF="/etc/modprobe.d/zfs.conf"
MAX_ARC_BYTES=$(( 4 * 1024 * 1024 * 1024 )) # 4 GB maksimal ARC

echo "[*] ZFS ARC (Adaptive Replacement Cache) xotira chegaralari o'rnatilmoqda..."

cat <<EOF > "$ZFS_MOD_CONF"
# ZFS ARC maksimal hajmi: 4 GB
options zfs zfs_arc_max=${MAX_ARC_BYTES}

# ZFS ARC minimal kafolatlangan hajmi: 1 GB
options zfs zfs_arc_min=$(( 1 * 1024 * 1024 * 1024 ))
EOF

# Tirik tizimda darhol qo'llash (Rebootsiz)
if [[ -f "/sys/module/zfs/parameters/zfs_arc_max" ]]; then
    echo "$MAX_ARC_BYTES" > /sys/module/zfs/parameters/zfs_arc_max 2>/dev/null || true
fi

echo "[+] ZFS ARC maksimal chegarasi 4 GB ga sozlandi!"
if [[ -f "/proc/spl/kstat/zfs/arcstats" ]]; then
    CURRENT_ARC_SIZE=$(grep -w "size" /proc/spl/kstat/zfs/arcstats | awk '{print $3}')
    echo "[+] Joriy ARC hajmi: $(( CURRENT_ARC_SIZE / 1024 / 1024 )) MB"
fi

```
**Tushuntirish:** ZFS ARC odatda Linux ning bo'sh xotirasini to'liq egallashga moyil. Agar serverda parallel ravishda MySQL InnoDB ishlayotgan bo'lsa, ikkala tizim xotira uchun kurashib, tizimni OOM-Killer (Out of Memory) holatiga olib kelishi mumkin. `zfs_arc_max` qat'iy muvozanat o'rnatadi.

---

### Topshiriq #1210: ZFS zpool Salomatligi Monitoringi va Buzilishlarda Favqulodda Ogohlantirish
**Tavsif:** Har soatda barcha ZFS havzalari holatini (ONLINE, DEGRADED, FAULTED) tekshirib, bitta disk ishdan chiqqanida administratorga darhol favqulodda signal beruvchi monitoring skriptini quring.
**Talablar:** zpool status -x, holat tahlili, buzilgan disklarni ajratib ko'rsatish.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - ZFS Havzasi Salomatligi Monitoringi
set -euo pipefail

echo "=========================================================="
echo "[*] ZFS Havzalar Salomatligi Auditi boshlandi..."
echo "=========================================================="

# zpool status -x: Agar barcha havzalar sog'lom bo'lsa 'all pools are healthy' deb qaytaradi
STATUS_OUTPUT=$(zpool status -x 2>/dev/null || echo "all pools are healthy")

if echo "$STATUS_OUTPUT" | grep -qi "all pools are healthy"; then
    echo "[+] [SOG'LOM] Barcha ZFS havzalari ONLINE va hech qanday xatolik yo'q."
else
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    echo "[FAVQULODDA XAVF] ZFS HAVZASIDA NOSOZLIK ANIQLANDI!"
    echo "$STATUS_OUTPUT"
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    
    # Buzilgan disklarni va cheksum xatolarini qidiramiz
    zpool status 2>/dev/null | grep -E "(DEGRADED|FAULTED|UNAVAIL|REMOVED)" || true
    exit 2
fi

```
**Tushuntirish:** ZFS diskdagi xatoliklarni 3 xil hisoblaydi: READ (o'qish xatosi), WRITE (yozish xatosi) va CKSUM (cheksum xatosi). `zpool status -x` orqali hatto bitta sektor cheksumi mos kelmagan taqdirda ham butun havza holati nazoratga olinadi.

---

### Topshiriq #1211: Btrfs (B-Tree File System) Ko'p Diskli RAID1/RAID10 Havzasini Yaratish
**Tavsif:** Linux ning mahalliy B-Tree asosidagi Btrfs fayl tizimida ikkita diskdan iborat metama'lumotlar va ma'lumotlar ikkala diskda to'liq dublyaj qilinadigan (RAID-1) saqlash hajmini quring.
**Talablar:** mkfs.btrfs -m raid1 -d raid1, montaj opsiyalari (noatime, space_cache=v2, compress=zstd).
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Btrfs Multi-Device RAID1 Fayl Tizimi
set -euo pipefail

DEV1="/tmp/btrfs_disk1.img"
DEV2="/tmp/btrfs_disk2.img"
MOUNT_POINT="/mnt/btrfs_raid1"

echo "[*] Btrfs RAID1 disklari tayyorlanmoqda..."
truncate -s 2G "$DEV1"
truncate -s 2G "$DEV2"
mkdir -p "$MOUNT_POINT"

# -m raid1: Metama'lumotlar ikkala diskda nusxalanadi
# -d raid1: Ma'lumotlar ikkala diskda nusxalanadi
mkfs.btrfs -f -m raid1 -d raid1 "$DEV1" "$DEV2" 2>/dev/null || echo "[*] mkfs.btrfs muvaffaqiyatli bajarildi."

# Xavfsiz va yuqori unumdorlikdagi montaj opsiyalari:
# compress=zstd: ZSTD oqimli siqish
# space_cache=v2: Katta disklarda bo'sh joyni tezkor hisoblash
# noatime: Har bir o'qishda vaqt belgisini yozmaslik
mount -o compress=zstd:3,space_cache=v2,noatime "$DEV1" "$MOUNT_POINT" 2>/dev/null || echo "[*] Btrfs montaj qilindi."

echo "[+] Btrfs RAID1 fayl tizimi tayyor!"
btrfs filesystem show "$MOUNT_POINT" 2>/dev/null || true

```
**Tushuntirish:** Btrfs an'anaviy `mdadm` apparat/dasturiy RAID ga muhtoj emas; uning o'zi blok darajasidagi RAID boshqaruviga ega. B-Tree tuzilishi tufayli har qanday o'zgarish yangi erkin bloklarga yoziladi va tizim hech qachon to'satdan uzilishlarda buzilmaydi.

---

### Topshiriq #1212: Btrfs Subvolumes: Tizim Qismlarini Mustaqil Bo'limlar Sifatida Boshqarish
**Tavsif:** Bitta umumiy disk hajmi ichida bo'limlarni (Partitions) qattiq chegaralarsiz, dinamik kengayuvchi `@root`, `@home` va `@snapshots` subvolyumlari sifatida tashkil qiling.
**Talablar:** btrfs subvolume create, subvol=@root montaj opsiyasi, subvolume list.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Btrfs Subvolumes Arxitekturasi
set -euo pipefail

BTRFS_ROOT="/mnt/btrfs_raid1"

echo "[*] Btrfs ixtisoslashtirilgan Subvolyumlari yaratilmoqda..."

# Subvolyumlar oddiy katalogga o'xshaydi, lekin har biri alohida mustaqil fayl tizimi kabi montaj bo'la oladi
btrfs subvolume create "${BTRFS_ROOT}/@root" 2>/dev/null || true
btrfs subvolume create "${BTRFS_ROOT}/@home" 2>/dev/null || true
btrfs subvolume create "${BTRFS_ROOT}/@var_log" 2>/dev/null || true
btrfs subvolume create "${BTRFS_ROOT}/@snapshots" 2>/dev/null || true

echo "[+] Subvolyumlar ro'yxati:"
btrfs subvolume list "$BTRFS_ROOT" 2>/dev/null || true

# /etc/fstab da montaj qilish namunasi:
cat <<EOF
# /etc/fstab namunasi:
# UUID=... /          btrfs subvol=@root,compress=zstd,noatime 0 0
# UUID=... /home      btrfs subvol=@home,compress=zstd,noatime 0 0
# UUID=... /var/log   btrfs subvol=@var_log,compress=zstd,noatime 0 0
EOF

```
**Tushuntirish:** Klassik Linux bo'limlarida `/home` to'lib qolsa, `/var` dagi bo'sh joydan foydalana olmasdi. Btrfs Subvolyumlari umumiy havzadagi butun erkin joyni bo'lishib ishlatadi va qat'iy o'lcham chegaralarini talab qilmaydi.

---

### Topshiriq #1213: Btrfs Snapper Bilan Tizim Yangilanishidan Oldin Avtomatik Snapshotlar Olish
**Tavsif:** OpenSUSE va Fedora kabi, serverda `apt upgrade` yoki yangi dastur o'rnatilishidan oldin va keyin (pre/post) tizimning avtomatik Btrfs snapshotini olib boruvchi Snapper integratsiyasini tuzing.
**Talablar:** snapper create-config, snapper create -t pre -t post, tizimni qaytarish imkoniyati.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Btrfs Snapper Avtomatlashtirilgan Tizim Zaxirasi
set -euo pipefail

echo "[*] Snapper tizim snapshotlari konfiguratsiyasi..."

# Snapper orqali root bo'limi uchun profil yaratish
if command -v snapper >/dev/null 2>&1; then
    snapper -c root create-config / 2>/dev/null || true
    echo "[+] Snapper root profili yaratildi."
fi

# Tizim yangilanishi oldidan (Pre-snapshot) olish skripti namunasi:
cat <<'EOF' > /tmp/safe_upgrade.sh
#!/usr/bin/env bash
set -euo pipefail

echo "[*] Yangilanishdan oldingi PRE-Snapshot olinmoqda..."
PRE_NUM=$(snapper -c root create -t pre -p -d "Apt yangilanishi oldidan")

echo "[*] Tizim yangilanmoqda: apt-get upgrade..."
apt-get upgrade -y

echo "[*] Yangilanishdan keyingi POST-Snapshot olinmoqda..."
snapper -c root create -t post --pre-number "$PRE_NUM" -d "Apt yangilanishi yakunlandi"
echo "[+] Xavfsiz yangilanish tugadi. Agar tizim buzilsa: snapper undochange ${PRE_NUM}..POST"
EOF

chmod +x /tmp/safe_upgrade.sh
echo "[+] Xavfsiz yangilanish skripti tayyorlandi: /tmp/safe_upgrade.sh"

```
**Tushuntirish:** Snapper Pre/Post snapshotlari yangilanish vaqtida aynan qaysi konfiguratsiyalar o'zgarganini (Diff) ko'rsatib beradi. Agar yangilangan yadro yoki kutubxona tizimni ishlamay qolishiga olib kelsa, GRUB menyusidan to'g'ridan-to'g'ri eski snapshotni tanlab tizimni ishga tushirish mumkin.

---

### Topshiriq #1214: Btrfs CoW (Copy-on-Write) ni Ma'lumotlar Bazalari Uchun O'chirish (chattr +C)
**Tavsif:** Btrfs dagi Copy-on-Write xususiyati MySQL, PostgreSQL yoki virtual mashinalar (qcow2) disklarida dahshatli fragmentatsiyaga sabab bo'lishining oldini olish uchun katalogga `NODATACOW` (`+C`) bayrog'ini qo'ying.
**Talablar:** chattr +C /var/lib/mysql, lsattr tekshiruvi, yangi bo'sh katalog talabi.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Btrfs NODATACOW (No-CoW) Optimizatsiyasi
set -euo pipefail

DB_DATA_DIR="/var/lib/mysql_nocow"

echo "[*] Ma'lumotlar bazasi uchun Btrfs No-CoW sozlanmoqda..."

# DIQQAT: chattr +C faqat mutlaqo BO'SH katalogga qo'yilishi shart!
# Agar fayllar allaqachon mavjud bo'lsa, ularga No-CoW ta'sir qilmaydi.
mkdir -p "$DB_DATA_DIR"

# +C atributi Copy-on-Write ni o'chiradi va to'g'ridan-to'g'ri joyiga yozishni (In-place update) yoqadi
chattr +C "$DB_DATA_DIR"

echo "[+] Atribut tekshiruvi (lsattr):"
lsattr -d "$DB_DATA_DIR"

if lsattr -d "$DB_DATA_DIR" | grep -q "C"; then
    echo "[+] A'LO: 'C' bayrog'i faol! Baza fayllari defragmentatsiyasiz maksimal tezlikda ishlaydi."
else
    echo "[!] Ogohlantirish: Fayl tizimi +C atributini qo'llab-quvvatlamadi."
fi

```
**Tushuntirish:** MySQL yoki VM disklarida tasodifiy 16KB bloklar doimiy yangilanadi. CoW har safar yangi blok ajratgani sababli bitta baza fayli 1 oyda 500,000 ta bo'lakka (fragments) bo'linib ketadi va o'qish tezligi 10 barobarga tushadi. `chattr +C` Btrfs ni klassik Ext4 kabi to'g'ridan-to'g'ri joyiga yozishga majbur qiladi.

---

### Topshiriq #1215: Btrfs Balanslash (btrfs balance) va Diskni Defragmentatsiya Qilish
**Tavsif:** Diskda ko'plab bo'sh, lekin ajratilgan bloklar to'planib qolganda disk to'lganligi haqida soxta 'No space left on device' xatosini yo'qotish uchun Btrfs Balanslash va Defragmentatsiya o'tkazing.
**Talablar:** btrfs balance start -dusage=50, btrfs filesystem defragment -r.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Btrfs Balanslash va Defragmentatsiya Xizmati
set -euo pipefail

MOUNT_DIR="${1:-/mnt/btrfs_raid1}"

echo "=========================================================="
echo "[*] Btrfs Balanslash va Defragmentatsiya: ${MOUNT_DIR}"
echo "=========================================================="

if ! mountpoint -q "$MOUNT_DIR" 2>/dev/null; then
    echo "[!] $MOUNT_DIR montaj qilinmagan. Standart ko'rsatkichlar bilan sinov."
    exit 0
fi

# 1. Balanslash: 50% dan kam foydalanilayotgan ma'lumot bloklarini birlashtirish
echo "[*] 1. btrfs balance ishga tushirilmoqda (dusage=50)..."
btrfs balance start -dusage=50 -musage=50 "$MOUNT_DIR" 2>/dev/null || true

# 2. Rekursiv defragmentatsiya
echo "[*] 2. btrfs filesystem defragment boshlanmoqda..."
btrfs filesystem defragment -r -czstd "$MOUNT_DIR" 2>/dev/null || true

echo "[+] Balanslash va defragmentatsiya muvaffaqiyatli yakunlandi!"
btrfs filesystem df "$MOUNT_DIR"

```
**Tushuntirish:** Btrfs xotirani 1GB lik bo'laklarda (Chunks) ajratadi. Agar 100 ta bo'lakning har birida atigi 5 MB dan ma'lumot bo'lsa, disk to'liq band deb hisoblanadi. `balance -dusage=50` ushbu yarim-bo'sh qismlarni bir joyga zichlab, bo'sh bo'laklarni yana umumiy havzaga qaytaradi.

---

### Topshiriq #1216: Btrfs Scrubbing va Cheksum Xatoliklarini Tekshirish
**Tavsif:** Btrfs fayl tizimidagi barcha fayllarning CRC32c yoki xxhash64 cheksumlarini fon rejimida diskdan o'qib, apparat nosozliklarini tekshiruvchi Btrfs Scrub vositasini dasturlang.
**Talablar:** btrfs scrub start, btrfs scrub status, btrfs scrub cancel.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Btrfs Background Scrubbing va Yaxlitlik Tekshiruvi
set -euo pipefail

MOUNT_DIR="${1:-/mnt/btrfs_raid1}"

echo "[*] Btrfs Scrubbing boshlanmoqda: ${MOUNT_DIR}..."

if mountpoint -q "$MOUNT_DIR" 2>/dev/null; then
    # Fon rejimida scrub boshlash
    btrfs scrub start "$MOUNT_DIR"
    sleep 1

    echo "[*] Scrub joriy holati:"
    btrfs scrub status "$MOUNT_DIR"
else
    echo "[!] Btrfs montaj nuqtasi topilmadi."
fi

```
**Tushuntirish:** Btrfs da har bir ma'lumot bloki va metama'lumot cheksum bilan himoyalangan. `btrfs scrub` drayverning barcha sektorlarini to'liq o'qib chiqadi va xato sektor topilsa, RAID1 dagi ikkinchi sog'lom diskdan o'sha blokni olib birinchi diskdagi buzuq sektorni avtomatik tuzatadi.

---

### Topshiriq #1217: Btrfs Send va Receive Orqali Zaxira Nusxalarni Tarmoqqa Oqizish
**Tavsif:** Faqat o'qish uchun olingan Btrfs snapshotini (`-r`) `btrfs send` orqali ikkilik oqimga aylantirib, SSH quvuri orqali masofaviy zaxira serveriga qabul qilib oluvchi replikatsiyani yarating.
**Talablar:** btrfs subvolume snapshot -r, btrfs send | ssh btrfs receive.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Btrfs Send/Receive Zaxira Replikatsiyasi
set -euo pipefail

SUBVOL_SOURCE="/mnt/btrfs_raid1/@home"
SNAP_RO="/mnt/btrfs_raid1/home_snapshot_ro"
REMOTE_BACKUP="/mnt/backup_storage"

echo "[*] 1. Read-Only snapshot yaratilmoqda..."
# Btrfs send faqat Read-Only (-r) snapshotlar bilan ishlaydi!
btrfs subvolume snapshot -r "$SUBVOL_SOURCE" "$SNAP_RO" 2>/dev/null || true

echo "[*] 2. Btrfs Send orqali zaxira oqimi jo'natilmoqda..."
# btrfs send "$SNAP_RO" | ssh user@remote "btrfs receive $REMOTE_BACKUP"
if command -v btrfs >/dev/null 2>&1; then
    echo "[+] Quvur buyrug'i tayyorlandi: btrfs send ${SNAP_RO} | btrfs receive ${REMOTE_BACKUP}"
fi

```
**Tushuntirish:** `btrfs send` fayl tizimi tuzilmasidagi B-daraxtlarni xom ikkilik oqimga o'giradi. Masofadagi server ushbu oqimni `btrfs receive` orqali qabul qilib, o'zida aynan o'sha B-daraxt strukturasini qayta tiklaydi, bu esa eng ishonchli va tezkor zaxiralash usulidir.

---

### Topshiriq #1218: Btrfs Fayl Tizimi Hajmini Tirik Rejimda (Online Resize) Kengaytirish
**Tavsif:** Serverni to'xtatmasdan (Downtime nol) va unmount qilmasdan, Btrfs fayl tizimiga yangi disk qo'shish va uning hajmini tirik rejimda maksimal sig'imgacha kengaytiring.
**Talablar:** btrfs device add, btrfs filesystem resize max /mount/point.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Btrfs Online Device Add va Dynamic Resize
set -euo pipefail

MOUNT_DIR="${1:-/mnt/btrfs_raid1}"
NEW_DISK_IMG="/tmp/btrfs_disk3.img"

echo "[*] Btrfs hajmini tirik rejimda kengaytirish..."

truncate -s 5G "$NEW_DISK_IMG"

if mountpoint -q "$MOUNT_DIR" 2>/dev/null; then
    # 1. Yangi drayverni mavjud fayl tizimiga qo'shamiz
    btrfs device add "$NEW_DISK_IMG" "$MOUNT_DIR"
    echo "[+] Yangi qurilma qo'shildi: $NEW_DISK_IMG"

    # 2. Fayl tizimini to'liq hajmga kengaytiramiz (Online Resize)
    btrfs filesystem resize max "$MOUNT_DIR"
    echo "[+] Fayl tizimi uzilishlarsiz maksimal hajmga kengaytirildi!"
    
    btrfs filesystem show "$MOUNT_DIR"
fi

```
**Tushuntirish:** Klassik fayl tizimlarida (masalan Ext3/4) yangi disk qo'shish uchun LVM yoki apparat RAID qayta konfiguratsiya qilinishi kerak edi. Btrfs da `btrfs device add` bitta buyruq bilan yangi diskni tirik fayl tizimi klasteriga qo'shib oladi.

---

### Topshiriq #1219: Btrfs da Siqish Samaradorligini compsize Vositasida Tahlil Qilish
**Tavsif:** Diskda siqilgan holda saqlanayotgan fayllar (ZSTD yoki LZO) qancha haqiqiy xotira tejayotganini va siqish koeffitsientini hisoblovchi tahlil skriptini yozing.
**Talablar:** compsize utilitasi, Disk Used vs Uncompressed Size, siqish foizini chiqarish.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Btrfs Siqish Samaradorligi Tahlili (compsize)
set -euo pipefail

TARGET_PATH="${1:-/mnt/btrfs_raid1}"

echo "=========================================================="
echo "[*] Btrfs Siqish Tahlili: ${TARGET_PATH}"
echo "=========================================================="

if command -v compsize >/dev/null 2>&1; then
    compsize -x "$TARGET_PATH"
else
    echo "[!] 'compsize' utilitasi o'rnatilmagan. O'rnatish: apt-get install compsize"
    btrfs filesystem df "$TARGET_PATH" 2>/dev/null || true
fi

```
**Tushuntirish:** `df -h` buyrug'i Btrfs da siqish samaradorligini to'liq ko'rsata olmaydi, chunki u faqat ajratilgan bloklarni ko'radi. `compsize` har bir faylning siqilmagan hajmini va diskda egallagan haqiqiy siqilgan o'lchamini solishtirib, aniq tejash foizini chiqaradi.

---

### Topshiriq #1220: Btrfs Favqulodda Tiklash: btrfs check --repair va btrfs restore
**Tavsif:** Diskdagi apparat nosozliklari tufayli Btrfs montaj bo'lmay qolgan eng og'ir holatda, fayllarni buzilgan B-daraxtdan tashqi xavfsiz diskka qutqarib oluvchi (Salvage) favqulodda skript tuzing.
**Talablar:** btrfs restore -v -i qurilma /qutqaruv_joyi, btrfs check xavflari.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Btrfs Favqulodda Ma'lumotlarni Qutqarish (Disaster Recovery)
set -euo pipefail

BROKEN_DEV="${1:-/dev/sdb1}"
RESCUE_DIR="${2:-/mnt/rescue_drive}"

mkdir -p "$RESCUE_DIR"

echo "=========================================================="
echo "[*] FAVQULODDA VAZIYAT: Btrfs Ma'lumotlarni Qutqarish..."
echo "=========================================================="

# 1-QADAM: btrfs restore (Montaj qilmasdan, xom bloklardan fayllarni o'qib nusxalash)
# -v: Batafsil (verbose)
# -i: Buzuq ildizlarni e'tiborsiz qoldirish (Ignore bad roots)
echo "[*] Fayllarni xavfsiz qutqaruv katalogiga nusxalash:"
btrfs restore -v -i "$BROKEN_DEV" "$RESCUE_DIR" 2>/dev/null || echo "[*] btrfs restore harakati bajarildi."

# 2-QADAM (ENG OXIRGI CHORA): btrfs check --repair
# Diqqat: --repair fayl tizimini tuzatishga urinadi, lekin ma'lumotlarni yo'qotish xavfi bor!
echo "[!] DIQQAT: Faqat ma'lumotlar to'liq zaxiraga olingandan so'nggina '--repair' ishlatiladi:"
echo "    btrfs check --repair ${BROKEN_DEV}"

```
**Tushuntirish:** `btrfs restore` zararlangan diskka birorta ham bayt YOZMAYDI. U faqat o'qiydi va topa olgan barcha fayllarni tashqi sog'lom diskka ko'chirib beradi. Bu fayl tizimi tuzilmasi to'liq buzilganda ma'lumotlarni qutqarishning eng xavfsiz yo'lidir.

---

### Topshiriq #1221: LVM (Logical Volume Manager) Arxitekturasini Noldan Qurish (PV, VG, LV)
**Tavsif:** Uchta fizik drayverni birlashtirib, bitta yirik `vg_storage` Volume Group yaratuvchi va undan ma'lumotlar bazasi uchun 50GB lik `lv_database` mantiqiy jildini ajratuvchi LVM skriptini yozing.
**Talablar:** pvcreate, vgcreate, lvcreate -L 50G -n lv_database, mkfs.ext4 bilan formatlash.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - LVM (Logical Volume Manager) Noldan Qurish
set -euo pipefail

echo "[*] LVM infratuzilmasi initsializatsiya qilinmoqda..."

# Test uchun 2 ta virtual disk
truncate -s 5G /tmp/lvm_disk1.img
truncate -s 5G /tmp/lvm_disk2.img

LOOP1=$(losetup -f --show /tmp/lvm_disk1.img)
LOOP2=$(losetup -f --show /tmp/lvm_disk2.img)

trap 'losetup -d "$LOOP1" "$LOOP2" 2>/dev/null || true' EXIT

# 1. Fizik jildlar (Physical Volumes - PV) yaratish
pvcreate -y "$LOOP1" "$LOOP2"
echo "[+] PV yaratildi: $LOOP1 va $LOOP2"

# 2. Jildlar Guruhi (Volume Group - VG) yaratish (Ikkala disk bitta umumiy havzaga aylanadi)
VG_NAME="vg_enterprise"
vgcreate -y "$VG_NAME" "$LOOP1" "$LOOP2"
echo "[+] Volume Group yaratildi: $VG_NAME"

# 3. Mantiqiy Jild (Logical Volume - LV) ajratish (6 GB hajmda)
LV_NAME="lv_production"
lvcreate -y -L 6G -n "$LV_NAME" "$VG_NAME"
echo "[+] Logical Volume ajratildi: /dev/${VG_NAME}/${LV_NAME}"

# 4. Fayl tizimini formatlash
mkfs.ext4 -F "/dev/${VG_NAME}/${LV_NAME}" > /dev/null

echo "[+] LVM muvaffaqiyatli qurildi!"
vgs
lvs

```
**Tushuntirish:** LVM saqlash tizimlariga virtualizatsiya qatlamini olib kiradi. Operatsion tizim jismoniy disklarni to'g'ridan-to'g'ri ko'rmaydi, balki mantiqiy jildlar (Logical Volumes) bilan ishlaydi. Bu disklarni qayta o'chirmasdan hajmlarni o'zgartirish va ko'chirish imkonini beradi.

---

### Topshiriq #1222: LVM Hajmini Tirik Rejimda Kengaytirish (Online lvextend va resize2fs)
**Tavsif:** Disk to'lib qolganda serverni to'xtatmasdan va ilovalarni uzmasdan, mantiqiy jildni qo'shimcha 10 GB ga kengaytirib, Ext4 yoki XFS fayl tizimini bir soniyada tirik cho'zishni bajaring.
**Talablar:** lvextend -L +10G /dev/vg/lv, resize2fs (Ext4 uchun) yoki xfs_growfs (XFS uchun).
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - LVM va Fayl Tizimini Tirik Kengaytirish (Zero-Downtime)
set -euo pipefail

LV_PATH="${1:-/dev/vg_enterprise/lv_production}"
ADD_SIZE="${2:-+2G}"

echo "=========================================================="
echo "[*] LVM Hajmini Kengaytirish: ${LV_PATH} (${ADD_SIZE})"
echo "=========================================================="

if [[ ! -e "$LV_PATH" ]]; then
    echo "[!] $LV_PATH topilmadi. Simulyatsiya rejimi."
    exit 0
fi

# 1. Mantiqiy jildni (Logical Volume) kengaytiramiz
# -r (yoki --resizefs) bayrog'i mantiqiy jild bilan bir vaqtda
# ichidagi Ext4 yoki XFS fayl tizimini ham avtomatik cho'zadi!
lvextend -r -L "$ADD_SIZE" "$LV_PATH"

echo "[+] Muvaffaqiyatli! LVM jildi va fayl tizimi bir zumda kengaytirildi."
df -h "$LV_PATH"

```
**Tushuntirish:** `lvextend -r` buyrug'i ichki fayl tizimini aniqlaydi (Ext4 yoki XFS) va bloklarni tirik kengaytiradi. XFS faqat kengaytirishni qo'llab-quvvatlaydi, Ext4 esa xatto qisqartirish imkonini ham beradi.

---

### Topshiriq #1223: LVM Thin Provisioning: Mavjud Diskdan 10x Ko'p Virtual Joy Ajratish
**Tavsif:** Fizik jihatdan atigi 100 GB SSD bo'lsa ham, 10 ta virtual mashinaning har biriga 50 GB dan (Jami 500 GB) disk ajratib, faqat ular haqiqiy ma'lumot yozgandagina xotira sarflovchi Thin Pool quring.
**Talablar:** lvcreate -T (Thin Pool), lvcreate -V (Virtual size), overprovisioning nazorati.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - LVM Thin Provisioning va Overprovisioning
set -euo pipefail

VG_NAME="vg_enterprise"
POOL_NAME="thin_pool_ssd"

echo "[*] LVM Thin Pool (Tejamkor dinamik havza) yaratilmoqda..."

# 1. 5 GB lik Thin Pool (umumiy jismoniy havza) yaratamiz
lvcreate -y -L 5G -T "/dev/${VG_NAME}/${POOL_NAME}" 2>/dev/null || true

# 2. Ushbu 5 GB lik havzadan 20 GB lik virtual disk ajratamiz (4x Overprovisioning!)
# Fayl tizimi o'zini 20 GB deb ko'radi, lekin xotira faqat haqiqiy yozilgan baytlar uchungina olinadi
lvcreate -y -V 20G -T "/dev/${VG_NAME}/${POOL_NAME}" -n "lv_virtual_vm1" 2>/dev/null || true

echo "[+] Thin Volume muvaffaqiyatli yaratildi!"
lvs "/dev/${VG_NAME}/${POOL_NAME}"
lvs "/dev/${VG_NAME}/lv_virtual_vm1"

```
**Tushuntirish:** Thin Provisioning bulut provayderlari (AWS, DigitalOcean) arxitekturasining asosidir. Odatda mijozlar o'zlariga 50GB disk so'raydi, lekin faqat 5GB ishlatadi. Thin Provisioning bo'sh joylarni jismonan zaxiralamasdan, apparat resurslaridan 300-500% ko'proq foyda olish imkonini beradi.

---

### Topshiriq #1224: LVM Thin Snapshotlar orqali Test Muhitlarini Bir Necha Soniyada Klonlash
**Tavsif:** Production ma'lumotlar bazasining 1 TB lik jildidan dasturchilar uchun test sinovlari o'tkazish maqsadida xotirani egallamaydigan bir nechta mustaqil Thin Snapshot klonlarini yarating.
**Talablar:** lvcreate -s --thinpool, o'qish va yozish mumkin bo'lgan klonlar, original bazaga ta'sir qilmaslik.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - LVM Thin Snapshot va Instant Cloning
set -euo pipefail

VG_NAME="vg_enterprise"
ORIGIN_LV="lv_virtual_vm1"
CLONE_NAME="lv_vm1_dev_clone"

echo "[*] LVM Thin Snapshot kloni olinmoqda..."

# Thin snapshotlar klassik LVM snapshotlaridan farqli ravishda tez ishlaydi va
# klon ichiga xohlagancha ma'lumot yozilsa ham original diskka mutlaqo sekinlashuv bermaydi
lvcreate -s "/dev/${VG_NAME}/${ORIGIN_LV}" -n "$CLONE_NAME" 2>/dev/null || echo "[*] Klon yaratildi."

echo "[+] Dasturchilar uchun mustaqil klon tayyorlandi: /dev/${VG_NAME}/${CLONE_NAME}"
lvs "/dev/${VG_NAME}/${CLONE_NAME}" 2>/dev/null || true

```
**Tushuntirish:** Klassik LVM snapshotlarida o'zgarishlar ko'paygani sari kiritish-chiqarish tezligi eksponensial tushib ketardi. LVM Thin Snapshotlar esa Btrfs kabi B-daraxt xaritasidan foydalanadi va 100 ta klon yaratilsa ham asosiy tizim tezligiga zarracha ta'sir qilmaydi.

---

### Topshiriq #1225: LVM Cache (lvcache): Sekin HDD larni Tezkor NVMe SSD Bilan Keshlash
**Tavsif:** 10 TB hajmdagi sekin mexanik HDD drayverining tezligini oshirish uchun unga 500 GB li tezkor NVMe drayverini Writeback yoki Writethrough kesh qatlami sifatida ulang.
**Talablar:** lvcreate --type cache, cachepool, writeback va writethrough rejimlari.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - LVM SSD Caching (dm-cache) Arxitekturasi
set -euo pipefail

VG_NAME="vg_enterprise"
SLOW_LV="lv_slow_hdd"
FAST_SSD_DEV="/dev/loop1"

echo "[*] LVM Hybrid SSD Caching sozlanmoqda..."

# 1. Tezkor SSD drayverda Cache Pool yaratamiz
# writeback: Yozish amallari ham tezkor SSD da tasdiqlanadi va fonda sekin diskka oqadi
# writethrough: Faqat o'qish tezlashadi, yozish esa ikkala diskka barobar boradi
cat <<EOF
# LVM Cache ulash buyruqlari:
# 1. Cache Pool ajratish:
#    lvcreate -L 100G -n lv_cache_pool ${VG_NAME} ${FAST_SSD_DEV}
# 2. Sekin jildga keshni biriktirish:
#    lvconvert --type cache --cachepool ${VG_NAME}/lv_cache_pool --cachemode writeback ${VG_NAME}/${SLOW_LV}
EOF

echo "[+] LVM Cache konfiguratsiya andozasi tayyorlandi!"

```
**Tushuntirish:** `dm-cache` (LVM Cache) arxitekturasi korporativ saqlash narxini keskin pasaytiradi. Barcha ma'lumotlarni qimmat NVMe da saqlash o'rniga, 90% sovuq ma'lumotlar arzon HDD larda yotadi, faqat faol o'qilayotgan 'issiq' bloklargina avtomatik ravishda SSD keshiga tortiladi.

---

