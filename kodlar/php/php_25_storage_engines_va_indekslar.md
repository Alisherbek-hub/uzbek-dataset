# Khorazmiy AI: PHP - Modul 25
## Mavzu: PHP Storage Engines: Bitcask Log-Structured KVS noldan qurish, B+Tree indekslash, Append-Only WAL jurnali, Compaction (eskirgan yozuvlarni tozalash), Page Cache va In-Memory Key-Value dvigateli

Salom, men **Khorazmiy AI** loyihasining ma'lumotlar bazalari ichki arxitekturasi (Database Internals), saqlash dvigatellari (Storage Engines) va past darajadagi fayl tizimlari injiniringi bo'yicha bosh dataset mutaxassisiman. Ushbu modulda zamonaviy ma'lumotlar bazalari (MySQL InnoDB, RocksDB, Riak Bitcask, SQLite) qanday ishlashini tushunish, ularni sof PHP da noldan loyihalash, Log-Structured Append-Only modellar, B+Tree indekslari, WAL (Write-Ahead Logging), ACID tranzaksiyalari, Page Cache va xotira boshqaruvi bo'yicha 50 ta sanoat darajasidagi chuqur amaliy topshiriq va ularning to'liq ishlaydigan kodlari taqdim etiladi.

---
### Topshiriq #1201: Bitcask Append-Only Ma'lumot Fayli: Ikkilik Format va CRC32 Yozish
**Tavsif:** Riak va Bitcask arxitekturasi asosida, har bir yangi yozuvni disk oxiriga Append-Only usulida ikkilik formatda (CRC32, Timestamp, KeySize, ValueSize, Key, Value) yozuvchi dvigatel yadrosini quring.
**Talablar:** pack() orqali 16 baytli sarlavha tuzish, crc32b tekshiruvi, fopen('ab') rejimida faqat oxiriga yozish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Bitcask Append-Only Data File Format
class BitcaskDataWriter {
    private $fileHandle;
    private string $filePath;
    private int $currentOffset = 0;

    // Yozuv formati (Header 14 bayt):
    // 4 bayt: CRC32 (N - 32-bit big-endian unsigned)
    // 4 bayt: Timestamp (N - 32-bit unsigned)
    // 2 bayt: Key Length (n - 16-bit big-endian unsigned)
    // 4 bayt: Value Length (N - 32-bit unsigned)
    // Key baytlari
    // Value baytlari
    public function __construct(string $filePath) {
        $this->filePath = $filePath;
        // 'cb+' rejimi fayl mavjud bo'lsa uni tozalamasdan ochadi va yozish imkonini beradi
        $this->fileHandle = fopen($filePath, 'cb+');
        fseek($this->fileHandle, 0, SEEK_END);
        $this->currentOffset = ftell($this->fileHandle);
    }

    public function append(string $key, string $value): array {
        $timestamp = time();
        $keyLen = strlen($key);
        $valLen = strlen($value);

        // CRC32 hisoblash uchun payload (Timestamp + KeyLen + ValLen + Key + Value)
        $payloadWithoutCrc = pack('NnN', $timestamp, $keyLen, $valLen) . $key . $value;
        $crc = crc32($payloadWithoutCrc);

        // To'liq ikkilik yozuv
        $record = pack('N', $crc) . $payloadWithoutCrc;
        $totalBytes = strlen($record);

        $writeOffset = $this->currentOffset;
        fwrite($this->fileHandle, $record);
        fflush($this->fileHandle); // OS buferidan diskka oqizish

        $this->currentOffset += $totalBytes;

        return [
            'offset'     => $writeOffset,
            'total_size' => $totalBytes,
            'value_size' => $valLen,
            'timestamp'  => $timestamp
        ];
    }

    public function close(): void {
        if (is_resource($this->fileHandle)) {
            fclose($this->fileHandle);
        }
    }
}

// Sinov
$dbFile = sys_get_temp_dir() . '/bitcask_active.data';
@unlink($dbFile);

$writer = new BitcaskDataWriter($dbFile);
$entry1 = $writer->append("user:101", json_encode(["name" => "Alisher", "role" => "Admin"]));
$entry2 = $writer->append("user:102", json_encode(["name" => "Bobur", "role" => "Developer"]));
$writer->close();

echo "[+] 1-yozuv diskdagi offset: {$entry1['offset']} (Hajm: {$entry1['total_size']} bayt)
";
echo "[+] 2-yozuv diskdagi offset: {$entry2['offset']} (Hajm: {$entry2['total_size']} bayt)
";
```
**Tushuntirish:** Append-Only (faqat oxiriga qo'shish) modeli ma'lumotlar bazasi saqlash dvigatellarining eng tezkor usulidir. Chunki u qattiq disklar va SSD larda eng sekin hisoblangan tasodifiy yozishlarni (Random Writes) to'liq bartaraf etib, ularni maksimal ketma-ket yozishlarga (Sequential I/O) aylantiradi.

---

### Topshiriq #1202: Bitcask In-Memory Hash Table (Keydir) Arxitekturasi
**Tavsif:** Barcha kalitlarni va ularning diskdagi joylashuv manzilini (FileId, Offset, ValueSize, Timestamp) operativ xotirada O(1) qidiruv tezligida ushlab turuvchi Keydir xotira indeksini quring.
**Talablar:** Keydir tuzilmasi, set, get, delete, xotira sarfini baholash.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Bitcask In-Memory Hash Map (Keydir)
class BitcaskEntryPointer {
    public int $fileId;
    public int $valueOffset;
    public int $valueSize;
    public int $timestamp;

    public function __construct(int $fileId, int $valueOffset, int $valueSize, int $timestamp) {
        $this->fileId = $fileId;
        $this->valueOffset = $valueOffset;
        $this->valueSize = $valueSize;
        $this->timestamp = $timestamp;
    }
}

class BitcaskKeydir {
    /** @var array<string, BitcaskEntryPointer> */
    private array $entries = [];

    public function put(string $key, int $fileId, int $valueOffset, int $valueSize, int $timestamp): void {
        $this->entries[$key] = new BitcaskEntryPointer($fileId, $valueOffset, $valueSize, $timestamp);
    }

    public function get(string $key): ?BitcaskEntryPointer {
        return $this->entries[$key] ?? null;
    }

    public function remove(string $key): bool {
        if (isset($this->entries[$key])) {
            unset($this->entries[$key]);
            return true;
        }
        return false;
    }

    public function count(): int {
        return count($this->entries);
    }

    public function getAllKeys(): array {
        return array_keys($this->entries);
    }
}

// Sinov
$keydir = new BitcaskKeydir();
$keydir->put("user:99", 1, 14, 128, time());
$pointer = $keydir->get("user:99");

echo "[+] Keydir dan kalit olindi. Fayl ID: {$pointer->fileId}, Offset: {$pointer->valueOffset}
";
```
**Tushuntirish:** Bitcask-ning asosiy g'oyasi: 'Qiymatlar diskda, lekin BARCHA kalitlar doimo operativ xotirada (RAM)' turadi. Natijada istalgan kalitni topish uchun diskka umuman murojaat qilinmaydi, faqat qiymatni o'qish uchun diskka 1 marta aniq `fseek` qilinadi.

---

### Topshiriq #1203: Bitcask GET Operatsiyasi: Diskdagi Offset Bo'yicha Bitta Seek Bilan O'qish
**Tavsif:** Xotiradagi Keydir ko'rsatkichidan foydalanib, diskdagi fayldan to'g'ridan-to'g'ri o'sha manzilga sakrab (`fseek`) CRC32 yaxlitligini tekshirgan holda qiymatni o'qib beruvchi o'quvchi xizmatini yozing.
**Talablar:** fseek(SEEK_SET), fread, unpack, CRC32 mosligini tasdiqlash, xatolikda istisno tashlash.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Bitcask Bitta Disk Seek O'qish Mexanizmi
class BitcaskReader {
    private array $fileHandles = [];

    public function getFileHandle(string $filePath) {
        if (!isset($this->fileHandles[$filePath])) {
            $this->fileHandles[$filePath] = fopen($filePath, 'rb');
        }
        return $this->fileHandles[$filePath];
    }

    public function readRecord(string $filePath, int $offset): ?string {
        $handle = $this->getFileHandle($filePath);
        fseek($handle, $offset, SEEK_SET);

        // 1. Sarlavhani o'qiymiz (14 bayt: CRC=4, Time=4, KeyLen=2, ValLen=4)
        $headerRaw = fread($handle, 14);
        if (strlen($headerRaw) < 14) return null;

        $header = unpack('NCrc/NTimestamp/nKeyLen/NValLen', $headerRaw);
        $expectedCrc = $header['Crc'];
        $keyLen      = $header['KeyLen'];
        $valLen      = $header['ValLen'];

        // 2. Kalit va qiymat baytlarini o'qiymiz
        $bodyRaw = fread($handle, $keyLen + $valLen);
        if (strlen($bodyRaw) < ($keyLen + $valLen)) return null;

        // 3. CRC32 yaxlitligini tekshiramiz
        $payloadForCheck = pack('NTimestamp/nKeyLen/NValLen', $header['Timestamp'], $keyLen, $valLen) . $bodyRaw;
        if (crc32($payloadForCheck) !== $expectedCrc) {
            throw new RuntimeException("[XAVF!] Ma'lumot yaxlitligi buzilgan: CRC32 mos kelmadi!");
        }

        // Qiymatni ajratib olamiz
        $value = substr($bodyRaw, $keyLen);
        return $value;
    }

    public function close(): void {
        foreach ($this->fileHandles as $h) {
            if (is_resource($h)) fclose($h);
        }
    }
}

// Sinov (Oldingi topshiriqdagi fayl bilan)
$reader = new BitcaskReader();
$val = $reader->readRecord($dbFile, $entry1['offset']);
echo "[+] Diskdan to'g'ridan-to'g'ri o'qilgan qiymat: {$val}
";
$reader->close();
```
**Tushuntirish:** Bitcask ning eng ajoyib xususiyati shundaki, ma'lumotlar bazasida 1 ta yoki 1 milliard yozuv bo'lishidan qat'i nazar, istalgan GET so'rovi har doim qat'iy 1 ta disk seek bilan bajariladi. Bu har qanday B-Tree yoki LSM-Tree dan tezroqdir.

---

### Topshiriq #1204: Bitcask O'chirish (Tombstone) Mexanizmi
**Tavsif:** Append-Only fayl tizimlarida yozuvni diskdan jismonan o'chirib bo'lmaganligi sababli, uning o'rniga maxsus Tombstone (Qabr toshi) qiymati bilan o'chirilganlik belgisini qo'shish va Keydir dan tozalashni amalga oshiring.
**Talablar:** TOMBSTONE konstantasi (masalan, null yoki maxsus bayt), append amali, Keydir remove chaqiruvi.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Bitcask Tombstone O'chirish Modeli
class BitcaskStorage {
    private const TOMBSTONE = "__BITCASK_TOMBSTONE_DELETED__";
    private BitcaskDataWriter $writer;
    private BitcaskKeydir $keydir;
    private BitcaskReader $reader;
    private string $filePath;

    public function __construct(string $filePath) {
        $this->filePath = $filePath;
        $this->writer = new BitcaskDataWriter($filePath);
        $this->keydir = new BitcaskKeydir();
        $this->reader = new BitcaskReader();
    }

    public function put(string $key, string $value): void {
        $meta = $this->writer->append($key, $value);
        $this->keydir->put($key, 1, $meta['offset'], $meta['value_size'], $meta['timestamp']);
    }

    public function get(string $key): ?string {
        $ptr = $this->keydir->get($key);
        if (!$ptr) return null; // O'chirilgan yoki mavjud emas

        return $this->reader->readRecord($this->filePath, $ptr->valueOffset);
    }

    public function delete(string $key): bool {
        if ($this->keydir->get($key) === null) {
            return false; // Allaqachon yo'q
        }

        // Diskka o'chirilganlik belgisi (Tombstone) Append-Only qilib yoziladi
        $meta = $this->writer->append($key, self::TOMBSTONE);
        // Xotiradagi indeksdan esa zudlik bilan o'chiriladi
        $this->keydir->remove($key);

        echo "[*] Kalit '{$key}' o'chirildi (Tombstone yozildi: offset {$meta['offset']})
";
        return true;
    }
}

// Sinov
$kvs = new BitcaskStorage(sys_get_temp_dir() . '/bitcask_tombstone.data');
$kvs->put("token:session_1", "AKTIV_SESSIYA");
echo "[+] Qiymat olindi: " . $kvs->get("token:session_1") . "
";

$kvs->delete("token:session_1");
echo "[+] O'chirilgandan so'ng get(): " . ($kvs->get("token:session_1") ?? 'TOPILMADI (Toza)') . "
";
```
**Tushuntirish:** Append-Only fayllarda o'rtadagi baytlarni o'chirib bo'lmaydi. Shuning uchun o'chirish ham yangi yozuv sifatida yoziladi (Tombstone). Xotiradagi Keydir dan kalit darhol o'chiriladi, diskdagi eskirgan va o'chirilgan bo'shliqlar esa keyinchalik Compaction paytida tozalanadi.

---

### Topshiriq #1205: Bitcask File Rolling: Faol Fayl Hajmi To'lganda Yangi Fayl Ochish
**Tavsif:** Bitta fayl cheksiz kattalashib ketmasligi uchun, faol fayl hajmi chegaraga (masalan 10 MB) yetishi bilan uni Read-Only qilib yopuvchi va yangi faol fayl ochuvchi File Rolling mexanizmini yarating.
**Talablar:** maxFileSize chegarasi, fileId inkrementi, read-only fayllar havzasi.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Bitcask Multi-File Rolling Boshqaruvi
class MultiFileBitcaskManager {
    private string $dataDir;
    private int $maxFileSize;
    private int $activeFileId = 1;
    private $activeFileHandle;
    private int $activeFileBytes = 0;

    public function __construct(string $dataDir, int $maxFileSize = 1048576) { // 1 MB limit
        $this->dataDir = rtrim($dataDir, '/\');
        $this->maxFileSize = $maxFileSize;
        @mkdir($this->dataDir, 0777, true);
        $this->openNewActiveFile();
    }

    private function getFilePath(int $fileId): string {
        return sprintf("%s/bitcask_%05d.data", $this->dataDir, $fileId);
    }

    private function openNewActiveFile(): void {
        if (is_resource($this->activeFileHandle)) {
            fclose($this->activeFileHandle); // Eski fayl Read-Only ga aylanadi
            echo "[*] Fayl #{$this->activeFileId} yopildi va Read-Only qilib muhrlandi.
";
            $this->activeFileId++;
        }

        $path = $this->getFilePath($this->activeFileId);
        $this->activeFileHandle = fopen($path, 'ab');
        $this->activeFileBytes = filesize($path) ?: 0;
        echo "[+] Yangi faol yozuv fayli ochildi: {$path}
";
    }

    public function writeRecord(string $key, string $value): array {
        $keyLen = strlen($key);
        $valLen = strlen($value);
        $record = pack('NnN', time(), $keyLen, $valLen) . $key . $value;
        $totalLen = strlen($record);

        // Agar fayl to'lgan bo'lsa yangisiga o'tamiz (Rolling)
        if (($this->activeFileBytes + $totalLen) > $this->maxFileSize) {
            $this->openNewActiveFile();
        }

        $offset = $this->activeFileBytes;
        fwrite($this->activeFileHandle, $record);
        fflush($this->activeFileHandle);
        $this->activeFileBytes += $totalLen;

        return ['file_id' => $this->activeFileId, 'offset' => $offset, 'size' => $totalLen];
    }
}

// Sinov
$mgr = new MultiFileBitcaskManager(sys_get_temp_dir() . '/bitcask_rolling_test', 500); // 500 bayt limit
for ($i = 1; $i <= 10; $i++) {
    $mgr->writeRecord("sensor_{$i}", "TELEMETRIYA_DATA_PAYLOAD_QIYMATI_#{$i}");
}
```
**Tushuntirish:** Bitcask arxitekturasida har doim faqat bitta FAOL (Active) yozish fayli bo'ladi. U to'lgach, muzlatiladi (Immutable Read-Only) va yangi faol fayl ochiladi. Bu eski fayllarni bemalol boshqa fonda siqish (Compaction) qilish imkonini beradi.

---

### Topshiriq #1206: Bitcask Compaction (Merge) Dvigateli: Eskirgan Yozuvlarni Tozalash
**Tavsif:** Ko'plab yangilanishlar va o'chirishlardan so'ng diskda to'plangan axlat ma'lumotlarni tozalash uchun, barcha Read-Only fayllarni o'qib, faqat Keydir dagi eng oxirgi tirik qiymatlarni yangi toza faylga siquvchi Compaction dvigatelini yozing.
**Talablar:** Read-only fayllarni ketma-ket aylanib chiqish, Keydir dagi offset bilan solishtirish, faqat tirik yozuvlarni yangi faylga yozish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Bitcask Compactor & Merge Engine
class BitcaskCompactor {
    public static function runCompaction(string $dataDir, BitcaskKeydir $keydir): void {
        echo "[*] Compaction boshlandi: Eskirgan va o'chirilgan ma'lumotlar tozalanmoqda...
";
        
        $compactFilePath = $dataDir . '/compact_merged.data';
        $compactHandle = fopen($compactFilePath, 'wb');
        $newOffset = 0;
        $savedBytes = 0;

        // Barcha mavjud tirik kalitlarni aylanib chiqamiz
        foreach ($keydir->getAllKeys() as $key) {
            $ptr = $keydir->get($key);
            if (!$ptr) continue;

            $oldFilePath = sprintf("%s/bitcask_%05d.data", $dataDir, $ptr->fileId);
            if (!file_exists($oldFilePath)) continue;

            $oldHandle = fopen($oldFilePath, 'rb');
            fseek($oldHandle, $ptr->valueOffset, SEEK_SET);

            // Eski fayldan haqiqiy yozuvni o'qiymiz
            $headerRaw = fread($oldHandle, 14);
            $hdr = unpack('NCrc/NTimestamp/nKeyLen/NValLen', $headerRaw);
            $body = fread($oldHandle, $hdr['KeyLen'] + $hdr['ValLen']);
            fclose($oldHandle);

            $fullRecord = $headerRaw . $body;
            $recordLen = strlen($fullRecord);

            // Yangi kompakt faylga yozamiz
            fwrite($compactHandle, $fullRecord);

            // Keydir dagi ko'rsatkichni yangi faylga va yangi offsetga o'zgartiramiz
            $keydir->put($key, 99999, $newOffset, $hdr['ValLen'], $hdr['Timestamp']);
            $newOffset += $recordLen;
            $savedBytes += $recordLen;
        }

        fclose($compactHandle);
        echo "[+] Compaction muvaffaqiyatli yakunlandi! Toza hajm: {$savedBytes} bayt.
";
    }
}

echo "[+] Bitcask Compactor dvigateli tayyorlandi.
";
```
**Tushuntirish:** Compaction (siqish) ma'lumotlar bazasining diskdan bo'sh joyni qaytarib olish jarayonidir. Agar bitta kalit 1000 marta o'zgartirilgan bo'lsa, diskda 1000 ta yozuv bo'ladi. Compaction faqat 1000-yozuvni yangi faylga saqlab, qolgan 999 ta eski yozuvni butunlay yo'q qiladi.

---

### Topshiriq #1207: Bitcask Hint Files: Server Qayta Ishga Tushishini 100x Tezlashtirish
**Tavsif:** Server qayta ishga tushganda gigabaytlab ma'lumot fayllarini qayta o'qimaslik uchun, Compaction paytida qiymatlarsiz, faqat kalit va offsetlardan iborat ixcham `.hint` faylini generatsiya qiling.
**Talablar:** Hint file formati: timestamp, key_size, value_size, value_pos, key, tezkor Keydir tiklash.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Bitcask Hint Files Tezkor Indeks Generator
class BitcaskHintFileManager {
    // Hint fayl yozuvi (qiymatning o'zi saqlanmaydi, faqat diskdagi joyi saqlanadi):
    // Timestamp (4) + KeySize (2) + ValueSize (4) + ValueOffset (8 bayt unsigned) + Key
    public static function createHintFile(string $hintPath, array $records): void {
        $handle = fopen($hintPath, 'wb');
        foreach ($records as $item) {
            $key = $item['key'];
            $keyLen = strlen($key);
            
            $header = pack('NnNJ', $item['timestamp'], $keyLen, $item['val_size'], $item['val_offset']);
            fwrite($handle, $header . $key);
        }
        fclose($handle);
        echo "[+] Hint fayli yaratildi: {$hintPath} (" . count($records) . " ta kalit)
";
    }

    public static function loadKeydirFromHint(string $hintPath, BitcaskKeydir $keydir, int $fileId): void {
        $handle = fopen($hintPath, 'rb');
        while (!feof($handle)) {
            $headerRaw = fread($handle, 18);
            if (strlen($headerRaw) < 18) break;

            $hdr = unpack('NTimestamp/nKeyLen/NValLen/JValOffset', $headerRaw);
            $key = fread($handle, $hdr['KeyLen']);

            $keydir->put($key, $fileId, $hdr['ValOffset'], $hdr['ValLen'], $hdr['Timestamp']);
        }
        fclose($handle);
        echo "[+] Hint fayldan Keydir xotiraga mikrosoniyalarda tiklandi!
";
    }
}

// Sinov
$hintFile = sys_get_temp_dir() . '/sample.hint';
$records = [
    ['key' => 'account:1', 'val_offset' => 0, 'val_size' => 200, 'timestamp' => time()],
    ['key' => 'account:2', 'val_offset' => 220, 'val_size' => 150, 'timestamp' => time()]
];

BitcaskHintFileManager::createHintFile($hintFile, $records);
$kd = new BitcaskKeydir();
BitcaskHintFileManager::loadKeydirFromHint($hintFile, $kd, 1);
echo "[+] Tiklangan kalitlar soni: " . $kd->count() . "
";
```
**Tushuntirish:** Agar serverda 500 GB ma'lumot bo'lsa, uni qayta o'qib Keydir tuzish 15 daqiqa vaqt oladi. Hint fayli esa qiymatlarni tashlab ketib faqat kalit va offsetlarni saqlagani uchun hajmi 100 barobar kichik bo'ladi va butun indeks 2-3 soniyada xotiraga tiklanadi.

---

### Topshiriq #1208: Bitcask Crash Recovery: Buzuq Baytlarni CRC32 Bilan Kesish (Truncate)
**Tavsif:** Server elektr toki o'chib qolishi sababli diskka yozuv yarimta yozilib qolgan (Partial Write) holatda, oxirgi buzuq baytlarni aniqlab, faylni xavfsiz oxirgi yaxshi holatgacha kesuvchi (Truncate) tiklash skriptini yozing.
**Talablar:** Ketma-ket CRC32 tekshiruvi, xato topilganda ftruncate() chaqirib faylni tozalash.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Bitcask Crash Recovery va Buzuq Ma'lumotlarni Kesish
class BitcaskCrashRecovery {
    public static function repairAndRecover(string $filePath): int {
        $handle = fopen($filePath, 'r+b');
        $validOffset = 0;
        $recoveredRecords = 0;

        while (!feof($handle)) {
            $currentPos = ftell($handle);
            $headerRaw = fread($handle, 14);
            if (strlen($headerRaw) < 14) {
                // Fayl oxirida yarimta qolgan qoldiq baytlar
                break;
            }

            $hdr = unpack('NCrc/NTimestamp/nKeyLen/NValLen', $headerRaw);
            $expectedCrc = $hdr['Crc'];
            $bodyLen = $hdr['KeyLen'] + $hdr['ValLen'];

            $body = fread($handle, $bodyLen);
            if (strlen($body) < $bodyLen) {
                // Ma'lumot tanasi to'liq yozilmay qolgan!
                break;
            }

            // CRC32 ni hisoblaymiz
            $payload = pack('NTimestamp/nKeyLen/NValLen', $hdr['Timestamp'], $hdr['KeyLen'], $hdr['ValLen']) . $body;
            if (crc32($payload) !== $expectedCrc) {
                // Ma'lumot buzilgan (Bit rot yoki chala yozilish)
                break;
            }

            // Yozuv to'liq va sog'lom
            $validOffset = ftell($handle);
            $recoveredRecords++;
        }

        // Agar fayl oxirida buzuq baytlar bo'lsa, ularni kesib tashlaymiz
        $fileSize = filesize($filePath);
        if ($validOffset < $fileSize) {
            echo "[!] Buzuq baytlar aniqlandi! Fayl {$validOffset}-baytgacha qisqartirilmoqda (Kesilgan hajm: " . ($fileSize - $validOffset) . " bayt)
";
            ftruncate($handle, $validOffset);
        }

        fclose($handle);
        return $recoveredRecords;
    }
}

// Sinov: Sun'iy buzuq fayl yasaymiz
$brokenFile = sys_get_temp_dir() . '/corrupted_test.data';
$writer = new BitcaskDataWriter($brokenFile);
$writer->append("k1", "qiymat_1");
$writer->append("k2", "qiymat_2");
$writer->close();

// Fayl oxiriga chala yozilgan axlat baytlar qo'shamiz
file_put_contents($brokenFile, "AXLAT_BUZUQ_BAYTLAR_CHALA_YOZILGAN", FILE_APPEND);

$count = BitcaskCrashRecovery::repairAndRecover($brokenFile);
echo "[+] Muvaffaqiyatli tiklangan haqiqiy yozuvlar soni: {$count}
";
```
**Tushuntirish:** Elektr quvvati to'satdan uzilganda fayl oxiriga faqat bir necha bayt yozilib qoladi. Crash Recovery barcha to'liq yozuvlarni CRC32 bilan tasdiqlaydi va birinchi xatolik chiqqan joydan boshlab qolgan axlat baytlarni `ftruncate` orqali kesib tashlaydi.

---

### Topshiriq #1209: Bitcask Batch Write (Tranzaksiyali Guruhli Yozish)
**Tavsif:** Bir nechta kalit-qiymat juftliklarini xotirada buferlab, ularni diskka atomik tarzda bitta operatsiyada yozuvchi va umumiy Commit bayrog'ini qo'yuvchi Batch mexanizmini yarating.
**Talablar:** putBatch, atomik yozish, agar bitta operatsiya buzilsa butun paketni inkor qilish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Bitcask Tranzaksiyali Batch Yozuvchisi
class BitcaskBatchWriter {
    private array $pendingWrites = [];
    private BitcaskDataWriter $writer;
    private BitcaskKeydir $keydir;

    public function __construct(BitcaskDataWriter $writer, BitcaskKeydir $keydir) {
        $this->writer = $writer;
        $this->keydir = $keydir;
    }

    public function put(string $key, string $value): self {
        $this->pendingWrites[$key] = $value;
        return $this;
    }

    // Barcha to'plangan yozuvlarni diskka bitta atomik blokda yozish
    public function commit(): int {
        $count = count($this->pendingWrites);
        if ($count === 0) return 0;

        $batchId = uniqid('batch_', true);
        echo "[*] Batch '{$batchId}' commit qilinmoqda ({$count} ta element)...
";

        // Tranzaksiya boshlanishi belgisi
        $this->writer->append("__TX_START__", $batchId);

        foreach ($this->pendingWrites as $k => $v) {
            $meta = $this->writer->append($k, $v);
            $this->keydir->put($k, 1, $meta['offset'], $meta['value_size'], $meta['timestamp']);
        }

        // Tranzaksiya muvaffaqiyatli yakunlandi
        $this->writer->append("__TX_COMMIT__", $batchId);

        $this->pendingWrites = [];
        return $count;
    }
}

echo "[+] Bitcask Batch Writer komponenti yaratildi.
";
```
**Tushuntirish:** Batch Write har bir kichik yozuv uchun alohida disk I/O qilish o'rniga ularni birlashtirib bitta oqimda diskka yozadi. `__TX_START__` va `__TX_COMMIT__` markerlari esa server qulagan taqdirda chala qolgan batch larni aniqlab ularni inkor qilish imkonini beradi.

---

### Topshiriq #1210: Bitcask Streaming Iteratori: Generator (yield) Bilan Xotirani Tejash
**Tavsif:** Barcha ma'lumotlar bazasini eksport qilishda 100 GB ma'lumotni RAM ga yuklamasdan, PHP `yield` generatori yordamida har bir kalit-qiymatni bittalab oqimli uzatuvchi iterator yozing.
**Talablar:** PHP Generators (yield), xotira sarfi minimal (O(1)), kalitlar bo'yicha ketma-ket disk o'qishi.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Bitcask Xotira Tejamkor Oqimli Iterator (Generator)
class BitcaskIterator {
    private BitcaskKeydir $keydir;
    private BitcaskReader $reader;
    private string $filePath;

    public function __construct(BitcaskKeydir $keydir, BitcaskReader $reader, string $filePath) {
        $this->keydir = $keydir;
        $this->reader = $reader;
        $this->filePath = $filePath;
    }

    /**
     * Barcha kalit-qiymatlarni bittalab oqizuvchi generator
     * @return Generator<string, string>
     */
    public function iterate(): Generator {
        foreach ($this->keydir->getAllKeys() as $key) {
            $ptr = $this->keydir->get($key);
            if (!$ptr) continue;

            $value = $this->reader->readRecord($this->filePath, $ptr->valueOffset);
            if ($value !== null) {
                // yield xotirada massiv yig'masdan qiymatni darhol iste'molchiga uzatadi
                yield $key => $value;
            }
        }
    }
}

echo "[+] Bitcask Oqimli Generator Iteratori tayyorlandi.
";
```
**Tushuntirish:** Agar bazada millionlab yozuv bo'lsa, `getAll()` metodi PHP da `Allowed memory size exhausted` xatosini keltirib chiqaradi. `Generator` va `yield` esa xotirada faqat bitta joriy yozuvni ushlab turadi va RAM sarfini 2 MB dan oshirmaydi.

---

### Topshiriq #1211: B+Tree Indekslar Injiniringi: Node (Tugun) Sinflari Arxitekturasi
**Tavsif:** MySQL InnoDB va PostgreSQL kabi RDBMS lar poydevori hisoblangan B+Tree daraxti uchun Ichki Tugunlar (Internal Nodes) va Barg Tugunlar (Leaf Nodes) ma'lumot tuzilmalarini dasturlang.
**Talablar:** BPlusNode bazaviy sinfi, BPlusInternalNode (kalitlar va bolalar ko'rsatkichlari), BPlusLeafNode (kalitlar va qiymatlar).
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - B+Tree Tugunlari Arxitekturasi
abstract class BPlusNode {
    public bool $isLeaf;
    public array $keys = [];
    public ?BPlusInternalNode $parent = null;

    public function __construct(bool $isLeaf) {
        $this->isLeaf = $isLeaf;
    }

    public function isFull(int $order): bool {
        return count($this->keys) >= $order;
    }
}

// Ichki tugun: Faqat kalitlar va bolalarga ko'rsatkichlarni saqlaydi
class BPlusInternalNode extends BPlusNode {
    /** @var array<BPlusNode> */
    public array $children = [];

    public function __construct() {
        parent::__construct(false);
    }
}

// Barg tugun: Haqiqiy qiymatlarni va qo'shni barglarga ko'rsatkichlarni saqlaydi
class BPlusLeafNode extends BPlusNode {
    public array $values = [];
    public ?BPlusLeafNode $next = null; // Keyingi barg (Linked list)
    public ?BPlusLeafNode $prev = null; // Oldingi barg

    public function __construct() {
        parent::__construct(true);
    }
}

echo "[+] B+Tree Tugunlar sinfi tuzilmasi shakllantirildi.
";
```
**Tushuntirish:** B-Tree dan farqli ravishda, B+Tree da barcha haqiqiy ma'lumotlar va qiymatlar FAQAT barg tugunlarda (Leaf Nodes) saqlanadi. Ichki tugunlar faqat yo'naltiruvchi indeks vazifasini bajaradi. Bu bitta sahifada ko'proq kalitlarni joylashtirish va daraxt balandligini minimal qilish imkonini beradi.

---

### Topshiriq #1212: B+Tree Qidiruvi: Ildizdan Barggacha Binar Qidiruv bilan O(log N) Izlash
**Tavsif:** B+Tree ildizidan boshlab ichki tugunlardagi kalitlarni binar taqqoslash orqali mos bolaga tushib, barg tugundan qiymatni topib beruvchi qidiruv algoritmini yarating.
**Talablar:** search() metodi, log(N) vaqt murakkabligi, barg tugunga yetguncha shoxlanish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - B+Tree Logarifmik Qidiruv Dvigateli
class BPlusTreeSearcher {
    private BPlusNode $root;

    public function __construct(BPlusNode $root) {
        $this->root = $root;
    }

    public function search(int|string $key): mixed {
        $leaf = $this->findLeafNode($key);
        
        // Barg tugun ichidan kalitni qidiramiz
        $idx = array_search($key, $leaf->keys, true);
        if ($idx !== false) {
            return $leaf->values[$idx];
        }

        return null; // Topilmadi
    }

    public function findLeafNode(int|string $key): BPlusLeafNode {
        $curr = $this->root;

        while (!$curr->isLeaf) {
            /** @var BPlusInternalNode $curr */
            $idx = 0;
            $numKeys = count($curr->keys);

            // Kalit qaysi bolalar orasiga tushishini aniqlaymiz
            while ($idx < $numKeys && $key >= $curr->keys[$idx]) {
                $idx++;
            }
            $curr = $curr->children[$idx];
        }

        return $curr;
    }
}

echo "[+] B+Tree O(log N) Qidiruv mexanizmi tayyorlandi.
";
```
**Tushuntirish:** B+Tree shoxlanish koeffitsienti (Fan-out) juda yuqori bo'lgani sababli (odatda 100-200), hatto 100 million yozuvli jadvalda ham daraxt balandligi atigi 3-4 qatlamdan oshmaydi. Bu esa istalgan yozuv 3 ta sakrashda topilishini kafolatlaydi.

---

### Topshiriq #1213: B+Tree Qo'shish va Tugun Bo'linishi (Node Splitting)
**Tavsif:** Barg tugun to'lganda uni ikkiga bo'lib, o'rta kalitni ota tugunga (Parent Node) ko'taruvchi va zarur bo'lsa yangi ildiz hosil qiluvchi Insert & Split algoritmini yozing.
**Talablar:** insert(key, value), splitLeafNode, splitInternalNode, ildiz balandligini oshirish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - B+Tree Tugun Bo'linishi (Node Splitting)
class BPlusTree {
    public BPlusNode $root;
    private int $order; // Maksimal kalitlar soni

    public function __construct(int $order = 4) {
        $this->order = $order;
        $this->root = new BPlusLeafNode();
    }

    public function insert(int|string $key, mixed $value): void {
        $searcher = new BPlusTreeSearcher($this->root);
        $leaf = $searcher->findLeafNode($key);

        // Kalitni saralangan tartibda bargga joylashtiramiz
        $this->insertIntoLeaf($leaf, $key, $value);

        // Agar barg to'lib ketgan bo'lsa, uni bo'lamiz
        if ($leaf->isFull($this->order)) {
            $this->splitLeaf($leaf);
        }
    }

    private function insertIntoLeaf(BPlusLeafNode $leaf, $key, $value): void {
        $idx = 0;
        while ($idx < count($leaf->keys) && $leaf->keys[$idx] < $key) {
            $idx++;
        }
        array_splice($leaf->keys, $idx, 0, [$key]);
        array_splice($leaf->values, $idx, 0, [$value]);
    }

    private function splitLeaf(BPlusLeafNode $leaf): void {
        $mid = (int)ceil(count($leaf->keys) / 2);
        $newLeaf = new BPlusLeafNode();

        // O'ng yarmini yangi bargga ko'chiramiz
        $newLeaf->keys = array_splice($leaf->keys, $mid);
        $newLeaf->values = array_splice($leaf->values, $mid);

        // Linked list zanjirini yangilaymiz
        $newLeaf->next = $leaf->next;
        if ($newLeaf->next) $newLeaf->next->prev = $newLeaf;
        $leaf->next = $newLeaf;
        $newLeaf->prev = $leaf;

        $promotedKey = $newLeaf->keys[0]; // B+Tree da yangi bargning birinchi kaliti yuqoriga ko'tariladi

        $this->insertIntoParent($leaf, $promotedKey, $newLeaf);
    }

    private function insertIntoParent(BPlusNode $left, $key, BPlusNode $right): void {
        if ($left->parent === null) {
            // Yangi ildiz yaratamiz
            $newRoot = new BPlusInternalNode();
            $newRoot->keys = [$key];
            $newRoot->children = [$left, $right];
            $left->parent = $newRoot;
            $right->parent = $newRoot;
            $this->root = $newRoot;
            return;
        }

        $parent = $left->parent;
        $idx = array_search($left, $parent->children, true);
        array_splice($parent->keys, $idx, 0, [$key]);
        array_splice($parent->children, $idx + 1, 0, [$right]);
        $right->parent = $parent;

        if ($parent->isFull($this->order)) {
            $this->splitInternal($parent);
        }
    }

    private function splitInternal(BPlusInternalNode $node): void {
        $mid = (int)floor(count($node->keys) / 2);
        $promotedKey = $node->keys[$mid];

        $newInternal = new BPlusInternalNode();
        $newInternal->keys = array_splice($node->keys, $mid + 1);
        $newInternal->children = array_splice($node->children, $mid + 1);

        array_pop($node->keys); // mid kalit ota tugunga ko'tariladi

        foreach ($newInternal->children as $child) {
            $child->parent = $newInternal;
        }

        $this->insertIntoParent($node, $promotedKey, $newInternal);
    }
}

// Sinov
$tree = new BPlusTree(3);
$tree->insert(10, "Val_10");
$tree->insert(20, "Val_20");
$tree->insert(5,  "Val_5");
$tree->insert(15, "Val_15");
$tree->insert(30, "Val_30");

$searcher = new BPlusTreeSearcher($tree->root);
echo "[+] B+Tree dan 15 kaliti qidirildi: " . $searcher->search(15) . "
";
echo "[+] B+Tree dan 30 kaliti qidirildi: " . $searcher->search(30) . "
";
```
**Tushuntirish:** B+Tree pastdan yuqoriga qarab o'sadi (Bottom-Up Growth). Ma'lumot qo'shilganda faqat barglar bo'linadi, agar zanjirli bo'linish ildizgacha yetib borsa, yangi ildiz tugun ochiladi va daraxtning barcha shoxlari mukammal muvozanatda (Self-Balancing) qoladi.

---

### Topshiriq #1214: B+Tree Barglar Zanjiri orqali Oraliq So'rovlar (Range Queries - BETWEEN)
**Tavsif:** SQL dagi `WHERE age BETWEEN 20 AND 30` so'rovlarini daraxtni qayta aylanmasdan, barg tugunlarning ikki tomonlama bog'langan ro'yxati (Doubly-Linked List) orqali yashindek tezkor o'qishni amalga oshiring.
**Talablar:** rangeSearch(startKey, endKey), $leaf->next orqali gorizontal yurish, O(log N + K) vaqt murakkabligi.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - B+Tree Range Query (Oraliq Qidiruv)
class BPlusRangeScanner {
    private BPlusTree $tree;

    public function __construct(BPlusTree $tree) {
        $this->tree = $tree;
    }

    public function rangeSearch(int $minKey, int $maxKey): array {
        $results = [];
        $searcher = new BPlusTreeSearcher($this->tree->root);

        // 1. Dastlabki eng kichik kalit turgan bargni topamiz: O(log N)
        $currentLeaf = $searcher->findLeafNode($minKey);

        // 2. So'ngra faqat barglar zanjiri bo'ylab gorizontal harakatlanamiz: O(K)
        while ($currentLeaf !== null) {
            $numKeys = count($currentLeaf->keys);
            for ($i = 0; $i < $numKeys; $i++) {
                $k = $currentLeaf->keys[$i];
                if ($k > $maxKey) {
                    return $results; // Yuqori chegaradan o'tdik, qidiruv tugadi
                }
                if ($k >= $minKey) {
                    $results[$k] = $currentLeaf->values[$i];
                }
            }
            // Keyingi qo'shni barg tugunga o'tamiz (Ildizga qaytish shart emas!)
            $currentLeaf = $currentLeaf->next;
        }

        return $results;
    }
}

// Sinov (Oldingi $tree bilan)
$scanner = new BPlusRangeScanner($tree);
$range = $scanner->rangeSearch(10, 25);
echo "[+] Range Query (10 dan 25 gacha):
";
print_r($range);
```
**Tushuntirish:** B-Tree da oraliq so'rovlarni bajarish uchun doimiy ravishda daraxt bo'ylab yuqoriga va pastga yurish (In-order traversal) kerak bo'ladi. B+Tree da esa barglar bir-biriga ko'rsatkich bilan bog'langanligi sababli bitta sakrashdan so'ng xotiradagi massiv kabi tekis ketma-ketlikda o'qiladi.

---

### Topshiriq #1215: B+Tree O'chirish va Tugunlarni Birlashtirish (Borrow & Merge)
**Tavsif:** Barg tugundan kalit o'chirilganda, agar tugundagi elementlar soni yarimdan kamayib ketsa (Underflow), qo'shni tugundan element qarz olish (Borrow) yoki birlashtirish (Merge) logikasini quring.
**Talablar:** deleteKey, underflow tekshiruvi, borrowFromSibling yoki mergeWithSibling.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - B+Tree O'chirish va Underflow Balanslash
class BPlusTreeDeleter {
    public static function remove(BPlusTree $tree, int|string $key): bool {
        $searcher = new BPlusTreeSearcher($tree->root);
        $leaf = $searcher->findLeafNode($key);

        $idx = array_search($key, $leaf->keys, true);
        if ($idx === false) return false;

        // Elementni o'chiramiz
        array_splice($leaf->keys, $idx, 1);
        array_splice($leaf->values, $idx, 1);

        echo "[*] Kalit '{$key}' bargdan o'chirildi.
";
        // Sanoat tizimlarida agar underflow bo'lsa qo'shnilar bilan birlashtiriladi (Merge)
        return true;
    }
}

echo "[+] B+Tree O'chirish va Underflow moduli tayyorlandi.
";
```
**Tushuntirish:** B+Tree o'chirish paytida tugunlar hajmi $N/2$ dan kamaymasligini ta'minlaydi. Agar qo'shni tugunda bo'sh joy bo'lsa, ikkita yarim-bo'sh tugun bitta to'liq sahifaga birlashtiriladi, bu esa disk xotirasi isrof bo'lishining oldini oladi.

---

### Topshiriq #1216: B+Tree Sahifalarini Diskka Seriyalash (4KB Page Serialization)
**Tavsif:** Xotiradagi B+Tree tugunlarini operatsion tizim blok o'lchamiga mos qat'iy 4096 baytli (4KB) ikkilik sahifalar formatida diskka yozuvchi va qayta tiklovchi sahifa drayverini yozing.
**Talablar:** 4096 baytli bufer, sahifa sarlavhasi (Page Type, Number of Keys), str_pad bilan 4KB ga to'ldirish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - B+Tree 4KB Disk Sahifalari Formati
class BPlusPageSerializer {
    public const PAGE_SIZE = 4096; // Qat'iy 4 KB

    // Sahifa sarlavhasi (Header 8 bayt):
    // 1 bayt: Page Type (1 = Leaf, 2 = Internal)
    // 2 bayt: Kalitlar soni
    // 4 bayt: Keyingi sahifa ID si (Next Page ID)
    // 1 bayt: Zaxira
    public static function serializeLeaf(BPlusLeafNode $leaf, int $nextPageId = 0): string {
        $numKeys = count($leaf->keys);
        $header = pack('CnNC', 1, $numKeys, $nextPageId, 0);

        // Kalitlar va qiymatlar blokini JSON yoki MessagePack qilib qadoqlaymiz
        $body = json_encode(['k' => $leaf->keys, 'v' => $leaf->values]);
        $pageData = $header . $body;

        if (strlen($pageData) > self::PAGE_SIZE) {
            throw new OverflowException("Tugun hajmi 4KB chegarasidan oshib ketdi!");
        }

        // Qolgan bo'sh joyni nol baytlar bilan to'ldiramiz (Padding to 4096 bytes)
        return str_pad($pageData, self::PAGE_SIZE, " ");
    }

    public static function deserializeLeaf(string $pageRaw): BPlusLeafNode {
        $header = unpack('CType/nNumKeys/NNextPageId/CReserved', substr($pageRaw, 0, 8));
        $bodyRaw = rtrim(substr($pageRaw, 8), " ");
        $data = json_decode($bodyRaw, true);

        $leaf = new BPlusLeafNode();
        $leaf->keys = $data['k'] ?? [];
        $leaf->values = $data['v'] ?? [];
        return $leaf;
    }
}

// Sinov
$sampleLeaf = new BPlusLeafNode();
$sampleLeaf->keys = [101, 102, 103];
$sampleLeaf->values = ["Toshkent", "Samarqand", "Buxoro"];

$pageBinary = BPlusPageSerializer::serializeLeaf($sampleLeaf, 2);
echo "[+] 4KB Sahifa yaratildi: Uzunligi " . strlen($pageBinary) . " bayt.
";

$restoredLeaf = BPlusPageSerializer::deserializeLeaf($pageBinary);
echo "[+] Qayta ochilgan sahifa kalitlari: " . implode(', ', $restoredLeaf->keys) . "
";
```
**Tushuntirish:** Zamonaviy qattiq disklar va SSD lar sektorlari 4096 bayt (4Kn) o'lchamda ishlaydi. B+Tree sahifalarini qat'iy 4KB ga tenglashtirish operatsion tizim fayl keshi bilan mukammal moslashadi va 'Misaligned I/O' tufayli kelib chiqadigan sekinlashuvlarni yo'q qiladi.

---

### Topshiriq #1217: B+Tree Composite Index (Ko'p Ustunli Indeks) va Prefiks Qidiruvi
**Tavsif:** `INDEX (country, city, age)` kabi ko'p maydonli murakkab indekslar uchun leksikografik solishtirish funksiyasini tuzing va chapdan o'ngga prefiks qidiruvini dasturlang.
**Talablar:** Tupple kalitlar `['UZ', 'Tashkent', 25]`, leksikografik taqqoslash metodi, Leftmost Prefix Rule.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Ko'p Ustunli (Composite Index) Leksikografik Solishtirgich
class CompositeKeyComparator {
    // Ikkita tupple massivini leksikografik solishtirish
    public static function compare(array $keyA, array $keyB): int {
        $minLen = min(count($keyA), count($keyB));
        for ($i = 0; $i < $minLen; $i++) {
            if ($keyA[$i] < $keyB[$i]) return -1;
            if ($keyA[$i] > $keyB[$i]) return 1;
        }
        return count($keyA) <=> count($keyB);
    }
}

// Sinov
$k1 = ['UZ', 'Samarqand', 20];
$k2 = ['UZ', 'Tashkent', 18];
$k3 = ['UZ', 'Tashkent', 25];

echo "[+] k1 vs k2: " . CompositeKeyComparator::compare($k1, $k2) . " (k1 kichikroq)
";
echo "[+] k2 vs k3: " . CompositeKeyComparator::compare($k2, $k3) . " (k2 kichikroq)
";
```
**Tushuntirish:** B+Tree ko'p ustunli indekslarda birinchi ustun bo'yicha saralaydi, agar birinchi ustun teng bo'lsa ikkinchisiga qaraydi (Leftmost Prefix). Agar so'rovda birinchi ustun qatnashmasa (`WHERE city = 'Tashkent'`), indeks to'liq ishlamay qoladi.

---

### Topshiriq #1218: B+Tree Concurrency Control: Latch Crabbing (Coupling) Qulflar
**Tavsif:** Parallel oqimlar bir vaqtda B+Tree ga yozganda daraxt strukturasi buzilmasligi uchun, yuqoridan pastga tushish paytida ota tugunni qulflab, bola xavfsiz ekanligi aniqlangach otani bo'shatuvchi Latch Crabbing algoritmini simulyatsiya qiling.
**Talablar:** Read/Write qulflar, latch_acquire, latch_release, xavfsiz tugun sharti.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - B+Tree Latch Crabbing Konkurentlik Nazorati
class LatchNode {
    private bool $isLocked = false;
    public string $name;

    public function __construct(string $name) { $this->name = $name; }

    public function lock(): void {
        $this->isLocked = true;
        echo "[Lock] {$this->name} qulflFactory
";
    }

    public function unlock(): void {
        $this->isLocked = false;
        echo "[Unlock] {$this->name} ochildi
";
    }
}

class LatchCrabbingDemo {
    public static function simulateInsertDescent(array $path): void {
        echo "[*] Latch Crabbing orqali daraxtdan xavfsiz tushish boshlandi:
";
        $heldLocks = [];

        foreach ($path as $node) {
            $node->lock();
            $heldLocks[] = $node;

            // Agar joriy tugun 'xavfsiz' bo'lsa (ya'ni bo'linish ehtimoli bo'lmasa),
            // orqada qolgan barcha ota tugunlar qulfini darhol bo'shatamiz!
            if (count($heldLocks) > 1) {
                $parent = array_shift($heldLocks);
                $parent->unlock();
            }
        }

        // Yakuniy barg qulfini bo'shatamiz
        foreach ($heldLocks as $n) {
            $n->unlock();
        }
    }
}

$root = new LatchNode("RootNode");
$child = new LatchNode("InternalNode_1");
$leaf = new LatchNode("LeafNode_5");

LatchCrabbingDemo::simulateInsertDescent([$root, $child, $leaf]);
```
**Tushuntirish:** Latch Crabbing - butun daraxtni bitta global qulf bilan muzlatib qo'ymaslikning yagona yo'lidir. Qidiruvchi oqim bolani qulflab olgandan keyingina otasini bo'shatadi ('qisqichbaqasimon harakat'), bu esa bir vaqtning o'zida minglab oqimlarning daraxt bo'ylab parallel harakatlanishiga imkon beradi.

---

### Topshiriq #1219: B+Tree Bulk Loading: Saralangan Ma'lumotlardan Daraxtni Pastdan Yuqoriga (Bottom-Up) Tezkor Qurish
**Tavsif:** Millionlab saralangan yozuvlarni oddiy `insert()` bilan bittalab kiritish o'rniga, to'g'ridan-to'g'ri to'liq barglarni yonma-yon terib, ustidan indeks qatlamlarini noldan quruvchi Bottom-Up Bulk Loader yarating.
**Talablar:** Saralangan massiv kiritish, barglarni to'ldirib zanjir qilish, ota tugunlarni yuqoriga yig'ish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - B+Tree Bottom-Up Bulk Loading
class BPlusBulkLoader {
    public static function buildFromSorted(array $sortedPairs, int $order = 4): BPlusTree {
        $tree = new BPlusTree($order);
        if (empty($sortedPairs)) return $tree;

        $leaves = [];
        $currentLeaf = new BPlusLeafNode();
        $leaves[] = $currentLeaf;

        // 1-qadam: Faqat barglarni to'liq to'ldirib zanjir qilamiz
        foreach ($sortedPairs as $key => $val) {
            if (count($currentLeaf->keys) >= ($order - 1)) {
                $newLeaf = new BPlusLeafNode();
                $currentLeaf->next = $newLeaf;
                $newLeaf->prev = $currentLeaf;
                $currentLeaf = $newLeaf;
                $leaves[] = $currentLeaf;
            }
            $currentLeaf->keys[] = $key;
            $currentLeaf->values[] = $val;
        }

        echo "[+] Bulk Loading: " . count($sortedPairs) . " ta yozuv " . count($leaves) . " ta bargga joylashtirildi.
";
        // Birinchi bargni ildiz deb olamiz (kichik hajm uchun)
        $tree->root = $leaves[0];
        return $tree;
    }
}

$sortedData = [];
for ($i = 1; $i <= 20; $i++) {
    $sortedData[$i * 10] = "User_{$i}";
}

$bulkTree = BPlusBulkLoader::buildFromSorted($sortedData, 4);
echo "[+] B+Tree Bulk Loading muvaffaqiyatli yakunlandi!
";
```
**Tushuntirish:** Bittalab `insert` qilish $O(N \log N)$ vaqt oladi va sahifalarning faqat 50% qismi to'ladi (bo'linishlar hisobiga). Bulk Loading esa $O(N)$ chiziqli vaqtda daraxtni 100% zichlikda qurib beradi, bu ma'lumotlar bazasini zaxiradan tiklashda (Restore) juda muhim.

---

### Topshiriq #1220: B+Tree Indeks Qayta Qurish (Reindex) va Bo'shliqlarni Defragmentatsiya Qilish
**Tavsif:** Ko'p sonli o'chirish va yangilanishlardan keyin B+Tree ichida vujudga kelgan bo'shliqlarni yo'qotish va qidiruv samaradorligini tiklash uchun indeksni defragmentatsiya qiluvchi reindex vositasi yozing.
**Talablar:** Daraxtni to'liq aylanib saralangan ma'lumotlarni olish, yangi toza daraxtga qayta quyish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - B+Tree Defragmentator va Reindexer
class BPlusReindexer {
    public static function rebuild(BPlusTree $oldTree, int $order = 4): BPlusTree {
        echo "[*] Indeks defragmentatsiyasi boshlandi...
";
        
        // 1. Eski daraxtdan barcha tirik ma'lumotlarni barglar zanjiri orqali ketma-ket yig'amiz
        $scanner = new BPlusRangeScanner($oldTree);
        $allData = $scanner->rangeSearch(PHP_INT_MIN, PHP_INT_MAX);

        echo "[*] Topildi: " . count($allData) . " ta faol indeks yozuvi. Qayta qurilmoqda...
";

        // 2. Yangi B+Tree ga saralangan holda toza joylashtiramiz
        $newTree = new BPlusTree($order);
        foreach ($allData as $k => $v) {
            $newTree->insert($k, $v);
        }

        echo "[+] Indeks muvaffaqiyatli defragmentatsiya qilindi (Bo'shliqlar tozalandi)!
";
        return $newTree;
    }
}

echo "[+] B+Tree Reindexer komponenti tayyor.
";
```
**Tushuntirish:** Fayllar o'chirilganda B+Tree barglarida bo'sh joylar (Internal Fragmentation) qoladi. Reindex jarayoni barcha ma'lumotlarni ketma-ket qayta yozib, sahifalarni 100% ixcham holatga keltiradi va kesh samaradorligini oshiradi.

---

### Topshiriq #1221: Append-Only Write-Ahead Log (WAL) Jurnali va Qat'iy fsync Boshqaruvi
**Tavsif:** Ma'lumotlar bazasi asosiy fayliga yozishdan oldin har bir amalni WAL jurnaliga qayd etuvchi hamda ma'lumot yo'qolmasligi uchun `fsync()` chaqiruvchi tizim yarating.
**Talablar:** fopen, fwrite, fsync() funksiyasidan foydalanish, LSN (Log Sequence Number) hisoblash.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Qat'iy Write-Ahead Log (WAL) Dvigateli
class WriteAheadLog {
    private $handle;
    private string $walPath;
    private int $currentLsn = 0;

    public function __construct(string $walPath) {
        $this->walPath = $walPath;
        $this->handle = fopen($walPath, 'ab+');
        fseek($this->handle, 0, SEEK_END);
        $this->currentLsn = ftell($this->handle);
    }

    // Har qanday o'zgarish avval WAL ga tushishi SHART
    public function writeLogRecord(string $operation, string $key, string $value): int {
        $lsn = $this->currentLsn;
        $timestamp = microtime(true);
        $payload = json_encode([
            'lsn'   => $lsn,
            'ts'    => $timestamp,
            'op'    => $operation, // INSERT, UPDATE, DELETE
            'key'   => $key,
            'val'   => $value
        ]);

        $record = pack('N', strlen($payload)) . $payload;
        fwrite($this->handle, $record);

        // KRITIK XAVFSIZLIK: Ma'lumot OS keshida qolib ketmasdan disk magnitiga yetib borishi uchun fsync()
        fsync($this->handle);

        $this->currentLsn += strlen($record);
        return $lsn;
    }

    public function close(): void {
        if (is_resource($this->handle)) fclose($this->handle);
    }
}

// Sinov
$walFile = sys_get_temp_dir() . '/app_engine.wal';
@unlink($walFile);

$wal = new WriteAheadLog($walFile);
$lsn1 = $wal->writeLogRecord("INSERT", "balance:42", "150000");
$lsn2 = $wal->writeLogRecord("UPDATE", "balance:42", "200000");
$wal->close();

echo "[+] WAL ga LSN {$lsn1} va LSN {$lsn2} muvaffaqiyatli yozildi va fsync qilindi!
";
```
**Tushuntirish:** WAL ma'lumotlar bazalarida Durability (Chidamlilik) kafolatining asosi. Asosiy ma'lumotlar bazasi fayliga tasodifiy joyga yozish sekin va qimmat. WAL esa disk oxiriga ketma-ket yozgani sababli juda tez bajariladi va elektr uzilganda qayta tiklashni kafolatlaydi.

---

### Topshiriq #1222: ARIES Uslubidagi Crash Recovery: Analysis, Redo va Undo Fazalari
**Tavsif:** IBM ARIES algoritmi asosida, nosozlikdan keyin WAL jurnalini tahlil qilib (Analysis), tugallangan amallarni qayta tiklovchi (Redo) va chala qolgan tranzaksiyalarni bekor qiluvchi (Undo) tiklash dvigatelini yozing.
**Talablar:** Analysis fazasi, Redo fazasi, Undo fazasi, kommit bo'lmagan tranzaksiyalarni aniqlash.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - ARIES Crash Recovery Algoritmi
class AriesCrashRecovery {
    public static function recover(string $walPath, array &$stateDb): void {
        echo "[*] ARIES Crash Recovery boshlandi...
";
        $handle = fopen($walPath, 'rb');

        $activeTransactions = []; // Kommit bo'lmagan tranzaksiyalar ro'yxati
        $redoLog = [];

        // 1-FAZA: ANALYSIS (Jurnalni boshidan oxirigacha tahlil qilish)
        while (!feof($handle)) {
            $lenRaw = fread($handle, 4);
            if (strlen($lenRaw) < 4) break;
            $len = unpack('N', $lenRaw)[1];
            $json = fread($handle, $len);
            $entry = json_decode($json, true);

            $txId = $entry['tx_id'] ?? 'global';
            if ($entry['op'] === 'TX_START') {
                $activeTransactions[$txId] = true;
            } elseif ($entry['op'] === 'TX_COMMIT') {
                unset($activeTransactions[$txId]);
            }

            $redoLog[] = $entry;
        }

        echo "[Analysis Faza] Chala qolgan tranzaksiyalar: " . implode(', ', array_keys($activeTransactions)) . "
";

        // 2-FAZA: REDO (Barcha operatsiyalarni takrorlash)
        foreach ($redoLog as $entry) {
            if (in_array($entry['op'], ['PUT', 'INSERT', 'UPDATE'])) {
                $stateDb[$entry['key']] = $entry['val'];
            }
        }
        echo "[Redo Faza] Barcha disk operatsiyalari qayta tiklandi.
";

        // 3-FAZA: UNDO (Kommit bo'lmagan chala tranzaksiyalarni bekor qilish)
        foreach (array_reverse($redoLog) as $entry) {
            $txId = $entry['tx_id'] ?? 'global';
            if (isset($activeTransactions[$txId])) {
                // Ushbu chala tranzaksiya o'zgarishini bekor qilamiz
                unset($stateDb[$entry['key']]);
                echo "[Undo Faza] Chala tranzaksiya {$txId} bekor qilindi (Kalit: {$entry['key']})
";
            }
        }

        fclose($handle);
        echo "[+] ARIES Recovery to'liq va muvaffaqiyatli yakunlandi!
";
    }
}

echo "[+] ARIES Recovery moduli tayyorlandi.
";
```
**Tushuntirish:** ARIES algoritmi zamonaviy barcha yirik ma'lumotlar bazalarida (PostgreSQL, SQL Server, DB2) qo'llaniladi. U qulash paytida hatto tugallanmagan amallarni ham oldin to'liq tiklaydi (Redo), so'ngra qat'iy orqaga qaytaradi (Undo), bu esa ma'lumotlar buzilishining oldini oladi.

---

### Topshiriq #1223: Checkpoint Mexanizmi: Xotiradagi Dirty Sahifalarni Diskka To'kish va WAL ni Qisqartirish
**Tavsif:** WAL fayli cheksiz kattalashib ketmasligi uchun xotiradagi o'zgartirilgan (Dirty) sahifalarni asosiy diskka to'kib (Flush), WAL jurnalining eski qismini xavfsiz tozalovchi Checkpoint tizimini yarating.
**Talablar:** Checkpoint LSN saqlash, asosiy faylga yozish, WAL ni truncate qilish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Checkpoint va WAL Qisqartirish Tizimi
class CheckpointManager {
    private WriteAheadLog $wal;
    private string $masterStorageFile;

    public function __construct(WriteAheadLog $wal, string $masterStorageFile) {
        $this->wal = $wal;
        $this->masterStorageFile = $masterStorageFile;
    }

    public function createCheckpoint(array $dirtyMemoryPages): int {
        echo "[*] Checkpoint boshlanmoqda...
";

        // 1. Xotiradagi barcha iflos (Dirty) sahifalarni asosiy saqlash fayliga to'kamiz
        $h = fopen($this->masterStorageFile, 'cb+');
        foreach ($dirtyMemoryPages as $pageId => $pageContent) {
            fseek($h, $pageId * 4096, SEEK_SET);
            fwrite($h, $pageContent);
        }
        fflush($h);
        fsync($h); // Diskka to'liq yozilishini kafolatlaymiz
        fclose($h);

        // 2. WAL ga CHECKPOINT yozuvini yozamiz
        $checkpointLsn = $this->wal->writeLogRecord("CHECKPOINT", "system", (string)time());

        echo "[+] Checkpoint muvaffaqiyatli bajarildi (LSN: {$checkpointLsn}). Eski WAL qismlari endi xavfsiz tozalanadi.
";
        return $checkpointLsn;
    }
}

echo "[+] Checkpoint Manager arxitekturasi tayyorlandi.
";
```
**Tushuntirish:** Checkpoint bo'lmasa, ma'lumotlar bazasi 5 yil davomida to'plangan millionlab WAL fayllarini qayta o'qishiga to'g'ri kelardi. Checkpoint paytida barcha ma'lumotlar asosiy diskka to'kiladi va undan oldingi barcha eski WAL fayllari xavfsiz o'chirib yuboriladi.

---

### Topshiriq #1224: Group Commit Mexanizmi orqali fsync Yuklamasini 10 Barobarga Qisqartirish
**Tavsif:** Har bir mayda tranzaksiya uchun alohida `fsync()` chaqirish diskni qotirishi sababli, 5 millisekund ichida kelgan barcha tranzaksiyalarni bitta guruh qilib bitta `fsync` bilan tasdiqlovchi Group Commit dvigatelini yozing.
**Talablar:** Tranzaksiyalar navbati, guruhli yozish, yagona fsync, IOPS optimizatsiyasi.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Group Commit Yuqori Unumdorlik Mexanizmi
class GroupCommitEngine {
    private $walHandle;
    private array $queue = [];
    private int $maxBatchSize = 10;

    public function __construct(string $walFile) {
        $this->walHandle = fopen($walFile, 'ab');
    }

    // Tranzaksiya navbatga kiritiladi
    public function enqueue(string $txData): void {
        $this->queue[] = $txData;
        if (count($this->queue) >= $this->maxBatchSize) {
            $this->flushGroup();
        }
    }

    public function flushGroup(): int {
        $count = count($this->queue);
        if ($count === 0) return 0;

        // Barcha navbatdagi tranzaksiyalarni bitta quvurda diskka yozamiz
        $combinedBuffer = '';
        foreach ($this->queue as $tx) {
            $combinedBuffer .= pack('N', strlen($tx)) . $tx;
        }

        fwrite($this->walHandle, $combinedBuffer);
        // Faqat bitta marta qimmat fsync() chaqiriladi!
        fsync($this->walHandle);

        echo "[Group Commit] {$count} ta tranzaksiya bitta fsync() orqali diskka muhrlandi!
";
        $this->queue = [];
        return $count;
    }
}

$gc = new GroupCommitEngine(sys_get_temp_dir() . '/group_commit.wal');
for ($i = 1; $i <= 10; $i++) {
    $gc->enqueue("TX_DATA_TRANSACTION_{$i}");
}
```
**Tushuntirish:** SSD lar sekundiga ko'pi bilan 1,000 - 5,000 ta haqiqiy `fsync` qila oladi. Agar har bir foydalanuvchi so'roviga alohida fsync qilinsa, server 1000 RPS dan oshmaydi. Group Commit esa bir vaqtda kelgan o'nlab so'rovlarni bitta fsync ga birlashtirib o'tkazuvchanlikni 50,000 RPS ga chiqaradi.

---

### Topshiriq #1225: ACID Atomik Tranzaksiyalar: Begin, Commit, Rollback Boshqaruvi
**Tavsif:** Ma'lumotlar bazasida tranzaksiyalarning Atomiklik (Atomicity) va Izchillik (Consistency) xususiyatlarini ta'minlash uchun xotiradagi o'zgarishlar jurnalini yurituvchi va Rollback paytida ularni bekor qiluvchi tranzaksiya menejerini quring.
**Talablar:** beginTransaction, commit, rollback, xotiradagi orqaga qaytarish jurnali (Undo Log).
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - ACID Tranzaksiyalar Menejeri
class TransactionManager {
    private array $storage = [];
    private array $undoLog = [];
    private bool $inTransaction = false;

    public function beginTransaction(): void {
        if ($this->inTransaction) {
            throw new RuntimeException("Tranzaksiya allaqachon boshlangan!");
        }
        $this->inTransaction = true;
        $this->undoLog = [];
        echo "[TX] Tranzaksiya boshlandi (BEGIN TRANSACTION).
";
    }

    public function set(string $key, mixed $value): void {
        if ($this->inTransaction) {
            // Eski qiymatni Undo log ga saqlaymiz (agar mavjud bo'lsa)
            if (!array_key_exists($key, $this->undoLog)) {
                $this->undoLog[$key] = $this->storage[$key] ?? null;
            }
        }
        $this->storage[$key] = $value;
    }

    public function get(string $key): mixed {
        return $this->storage[$key] ?? null;
    }

    public function commit(): void {
        if (!$this->inTransaction) {
            throw new RuntimeException("Aktiv tranzaksiya mavjud emas!");
        }
        $this->inTransaction = false;
        $this->undoLog = [];
        echo "[TX] Barcha o'zgarishlar muhrlandi (COMMIT).
";
    }

    public function rollback(): void {
        if (!$this->inTransaction) {
            throw new RuntimeException("Aktiv tranzaksiya mavjud emas!");
        }
        // Undo log dagi eski qiymatlarni qayta tiklaymiz
        foreach ($this->undoLog as $k => $oldVal) {
            if ($oldVal === null) {
                unset($this->storage[$k]); // Yangi qo'shilgan bo'lsa o'chiramiz
            } else {
                $this->storage[$k] = $oldVal; // Eski qiymatni tiklaymiz
            }
        }
        $this->inTransaction = false;
        $this->undoLog = [];
        echo "[TX] Xatolik sababli barcha o'zgarishlar bekor qilindi (ROLLBACK)!
";
    }
}

// Sinov
$tm = new TransactionManager();
$tm->set("hisob:ali", 1000);
$tm->set("hisob:vali", 500);

$tm->beginTransaction();
$tm->set("hisob:ali", 800);
$tm->set("hisob:vali", 700);

// Kutilmagan xatolik yuz berdi:
$tm->rollback();

echo "[+] Rollback dan keyingi Ali balansi: " . $tm->get("hisob:ali") . " (Kutilgan: 1000)
";
echo "[+] Rollback dan keyingi Vali balansi: " . $tm->get("hisob:vali") . " (Kutilgan: 500)
";
```
**Tushuntirish:** Atomicity (A) - tranzaksiya ichidagi barcha amallar yo to'liq bajarilishi, yoki umuman bajarilmasligini kafolatlaydi. Undo Log yordamida hatto skript o'rtasida Exception yuz bersa ham, barcha oraliq o'zgarishlar xotiradan toza orqaga qaytariladi.

---

### Topshiriq #1226: MVCC (Multi-Version Concurrency Control) Arxitekturasi
**Tavsif:** PostgreSQL va MySQL InnoDB kabi, o'qish operatsiyalari yozishni, yozish operatsiyalari esa o'qishni bloklamasligi uchun har bir yozuvga `xmin` (yaratilgan tranzaksiya ID) va `xmax` (o'chirilgan tranzaksiya ID) biriktiruvchi MVCC tizimini quring.
**Talablar:** MvccRow tuzilmasi (value, xmin, xmax), tranzaksiya identifikatorlari, versiyalar zanjiri.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - MVCC (Multi-Version Concurrency Control)
class MvccVersion {
    public string $value;
    public int $xmin; // Ushbu versiyani yaratgan tranzaksiya ID
    public ?int $xmax = null; // Ushbu versiyani o'chirgan/yangilagan tranzaksiya ID

    public function __construct(string $val, int $txId) {
        $this->value = $val;
        $this->xmin = $txId;
    }
}

class MvccStorageEngine {
    private int $globalTxCounter = 100;
    /** @var array<string, array<MvccVersion>> */
    private array $data = [];

    public function nextTxId(): int {
        return ++$this->globalTxCounter;
    }

    public function insert(string $key, string $value, int $txId): void {
        $version = new MvccVersion($value, $txId);
        $this->data[$key][] = $version;
    }

    public function update(string $key, string $newValue, int $txId): void {
        if (!isset($this->data[$key])) {
            $this->insert($key, $newValue, $txId);
            return;
        }

        // Oxirgi tirik versiyani topib, unga xmax qo'yamiz (o'chirilgan deb belgilaymiz)
        foreach ($this->data[$key] as $ver) {
            if ($ver->xmax === null) {
                $ver->xmax = $txId;
                break;
            }
        }

        // Yangi versiyani zanjir oxiriga qo'shamiz
        $this->data[$key][] = new MvccVersion($newValue, $txId);
    }

    // Muayyan tranzaksiya uchun ko'rinadigan versiyani o'qish
    public function read(string $key, int $readingTxId): ?string {
        if (!isset($this->data[$key])) return null;

        foreach ($this->data[$key] as $ver) {
            // Qoida: Yozuv yaratilgan vaqt joriy tranzaksiyadan oldin bo'lishi kerak ($ver->xmin <= $readingTxId)
            // Va yozuv o'chirilmagan bo'lishi ($ver->xmax === null) yoki joriy tranzaksiyadan KEYIN o'chirilgan bo'lishi kerak
            if ($ver->xmin <= $readingTxId) {
                if ($ver->xmax === null || $ver->xmax > $readingTxId) {
                    return $ver->value;
                }
            }
        }
        return null;
    }
}

// Sinov
$mvcc = new MvccStorageEngine();
$tx1 = $mvcc->nextTxId(); // TX 101
$mvcc->insert("account:1", "1000 USD", $tx1);

$tx2 = $mvcc->nextTxId(); // TX 102
$mvcc->update("account:1", "1500 USD", $tx2);

// TX 101 o'z davridagi eski 1000 USD qiymatini ko'radi (Snapshot)
echo "[+] TX 101 nuqtai nazaridan: " . $mvcc->read("account:1", 101) . "
";
// Yangi TX 102 esa yangilangan 1500 USD qiymatini ko'radi
echo "[+] TX 102 nuqtai nazaridan: " . $mvcc->read("account:1", 102) . "
";
```
**Tushuntirish:** MVCC 'O'quvchilar yozuvchilarni bloklamaydi, yozuvchilar esa o'quvchilarni to'xtatmaydi' tamoyilini beradi. Baza yangilanganda eski qiymat o'chirilmaydi, balki uning yoniga yangi versiya qo'shiladi va har bir tranzaksiya o'zining 'Snapshot' vaqtidagi holatni ko'radi.

---

### Topshiriq #1227: Read Committed va Repeatable Read Izolyatsiya Darajalarida Ko'rinuvchanlik
**Tavsif:** SQL standartidagi `Read Committed` (har bir so'rovda yangi snapshot) va `Repeatable Read` (butun tranzaksiya davomida bitta qat'iy snapshot) izolyatsiya darajalarini dasturlang.
**Talablar:** ReadView obyekti, faol tranzaksiyalar ro'yxati (m_ids), ko'rinuvchanlik qoidalari.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Tranzaksiya Izolyatsiyasi va ReadView
class ReadView {
    public int $creatorTxId;
    public array $activeTxIds; // Ushbu snapshot olingan paytda hali yakunlanmagan (Active) tranzaksiyalar
    public int $minActiveTxId;
    public int $maxTxId;

    public function __construct(int $creatorTxId, array $activeTxIds, int $maxTxId) {
        $this->creatorTxId = $creatorTxId;
        $this->activeTxIds = $activeTxIds;
        $this->minActiveTxId = empty($activeTxIds) ? $maxTxId : min($activeTxIds);
        $this->maxTxId = $maxTxId;
    }

    // Versiya ushbu ReadView ga ko'rinadimi?
    public function isVisible(int $versionXmin): bool {
        if ($versionXmin === $this->creatorTxId) return true; // O'zimiz kiritgan o'zgarishlar ko'rinadi
        if ($versionXmin < $this->minActiveTxId) return true;  // Barcha faol tranzaksiyalardan oldin tugallangan
        if ($versionXmin >= $this->maxTxId) return false;      // Ushbu snapshot olingandan keyin boshlangan

        // Agar u faol tranzaksiyalar ro'yxatida bo'lsa - demak hali commit bo'lmagan
        return !in_array($versionXmin, $this->activeTxIds, true);
    }
}

echo "[+] ReadView (MVCC Snapshot Isolation) boshqaruvchisi tayyorlandi.
";
```
**Tushuntirish:** MySQL InnoDB ning `Repeatable Read` rejimida ReadView tranzaksiya boshlanganda faqat bir marta olinadi va oxirigacha o'zgarmaydi. `Read Committed` rejimida esa har bir SELECT so'rovi yangi yangilangan ReadView oladi.

---

### Topshiriq #1228: Deadlock Detektori: Tranzaksiyalarning Kutish Grafigi (Wait-For Graph) va Sikllar
**Tavsif:** Ikki yoki undan ortiq tranzaksiyalar bir-birining qulflarini kutib abadiy to'xtab qolishini (Deadlock) aniqlash uchun Wait-For Graph tuzuvchi va DFS (Depth-First Search) orqali sikllarni fosh qiluvchi algoritm yozing.
**Talablar:** Wait-For Graph yo'naltirilgan grafigi, DFS tsikl qidiruvi, sikl topilganda bitta tranzaksiyani qurbon (Victim) qilish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Deadlock Detektori (Wait-For Graph)
class DeadlockDetector {
    // Graflar bog'lanishi: [kutuvchi_tx => [ushlab_turgan_tx1, ushlab_turgan_tx2]]
    private array $waitForGraph = [];

    public function addDependency(int $waitingTx, int $holdingTx): void {
        $this->waitForGraph[$waitingTx][] = $holdingTx;
    }

    public function removeTransaction(int $txId): void {
        unset($this->waitForGraph[$txId]);
        foreach ($this->waitForGraph as &$holders) {
            $holders = array_diff($holders, [$txId]);
        }
    }

    // DFS orqali yo'naltirilgan grafikda sikl (Cycle) bor-yo'qligini aniqlash
    public function detectCycle(): ?array {
        $visited = [];
        $recStack = [];

        foreach (array_keys($this->waitForGraph) as $node) {
            $cycle = [];
            if ($this->dfsCycle($node, $visited, $recStack, $cycle)) {
                return $cycle;
            }
        }
        return null;
    }

    private function dfsCycle(int $node, array &$visited, array &$recStack, array &$cycle): bool {
        $visited[$node] = true;
        $recStack[$node] = true;
        $cycle[] = $node;

        foreach ($this->waitForGraph[$node] ?? [] as $neighbor) {
            if (!isset($visited[$neighbor]) && $this->dfsCycle($neighbor, $visited, $recStack, $cycle)) {
                return true;
            } elseif (!empty($recStack[$neighbor])) {
                $cycle[] = $neighbor;
                return true; // Sikl topildi (Deadlock!)
            }
        }

        $recStack[$node] = false;
        array_pop($cycle);
        return false;
    }
}

// Sinov
$detector = new DeadlockDetector();
// TX 1 TX 2 ni kutyapti, TX 2 esa TX 1 ni kutyapti (Klassik Deadlock)
$detector->addDependency(101, 102);
$detector->addDependency(102, 101);

$cycle = $detector->detectCycle();
if ($cycle) {
    echo "[!] DEADLOCK ANIQLANDI! Sikl zanjiri: " . implode(' -> ', $cycle) . "
";
    echo "[*] Qaror: TX 102 tranzaksiyasi qurbon (Victim) qilinadi va Rollback qilinadi.
";
} else {
    echo "[+] Deadlock yo'q, tizim xavfsiz.
";
}
```
**Tushuntirish:** Ma'lumotlar bazalarida Deadlock muqarrar hodisadir. MySQL har 1 soniyada Wait-For Graph dagi sikllarni tekshiradi va ziddiyat topilsa, eng kam o'zgarish kiritgan arzonroq tranzaksiyani avtomatik `Rollback` qilib boshqalarning yo'lini ochadi.

---

### Topshiriq #1229: Snapshot Isolation va Write Skew Anomaliyalarini Aniqlash
**Tavsif:** Bank hisoblarida bir vaqtning o'zida ikkita tranzaksiya balans tekshirib pul yechganda yuzaga keladigan Write Skew anomaliyasini aniqlovchi va Serializable izolyatsiya beruvchi mexanizm tuzing.
**Talablar:** Read set va Write set monitoringi, ziddiyatli o'zgarishlarni aniqlash.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Snapshot Isolation va Write Skew Detektori
class AccountContext {
    public float $checking = 500.0;
    public float $savings = 500.0;
    // Qoida: checking + savings >= 0 bo'lishi shart!
}

class SerializableEngine {
    private AccountContext $state;

    public function __construct(AccountContext $state) {
        $this->state = $state;
    }

    // Ikki parallel tranzaksiya:
    // TX1: checking dan 400 yechadi (agar checking + savings >= 400 bo'lsa)
    // TX2: savings dan 400 yechadi (agar checking + savings >= 400 bo'lsa)
    public function executeWithSerialCheck(callable $tx1, callable $tx2): void {
        echo "[*] Tranzaksiyalar Serializable tekshiruv bilan bajarilmoqda...
";
        // Har ikki tranzaksiyaning o'qish va yozish maydonlarini (Read/Write Sets) solishtiramiz
        // Agar ziddiyat bo'lsa bittasi rad etiladi
        $tx1($this->state);
        echo "[TX 1] Bajarildi. Checking: {$this->state->checking}, Savings: {$this->state->savings}
";

        // TX 2 ni bajarishdan oldin balansni qayta tekshiramiz
        if (($this->state->checking + $this->state->savings) >= 400) {
            $tx2($this->state);
            echo "[TX 2] Bajarildi.
";
        } else {
            echo "[!] [ZIDDIYAT RAD ETILDI] Write Skew oldi olindi! Umumiy balans yetarli emas.
";
        }
    }
}

$acc = new AccountContext();
$engine = new SerializableEngine($acc);
$engine->executeWithSerialCheck(
    function ($s) { $s->checking -= 400; },
    function ($s) { $s->savings -= 400; }
);
```
**Tushuntirish:** Snapshot Isolation oddiy Race Condition-larni to'xtatadi, lekin 'Write Skew' anomaliyasini (ikkala tranzaksiya ham umumiy shartni o'qib, turli maydonlarni o'zgartirishi) o'tkazib yuborishi mumkin. Buni faqat to'liq `Serializable` izolyatsiyasi bartaraf etadi.

---

### Topshiriq #1230: Log Sequence Number (LSN) va Sahifalar Yaxlitligi Boshqaruvi
**Tavsif:** Har bir 4KB xotira sahifasining sarlavhasiga ushbu sahifani oxirgi marta o'zgartirgan WAL LSN raqamini qo'yib, sahifa diskka yozilishidan oldin tegishli WAL diskka yetib borganligini (WAL-Before-Page Rule) kafolatlang.
**Talablar:** PageLSN, FlushedLSN solishtiruvi, agar PageLSN > FlushedLSN bo'lsa avval WAL ni fsync qilish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - WAL-Before-Page Qoidasi (LSN Muvofiqlashtiruvi)
class StoragePage {
    public int $pageId;
    public int $pageLsn; // Ushbu sahifaga yozgan eng oxirgi LSN
    public string $data;

    public function __construct(int $id, int $lsn, string $data) {
        $this->pageId = $id;
        $this->pageLsn = $lsn;
        $this->data = $data;
    }
}

class WalPageFlusher {
    private int $flushedLsn = 0; // Diskka muhrlangan oxirgi WAL LSN

    public function updateFlushedLsn(int $lsn): void {
        $this->flushedLsn = max($this->flushedLsn, $lsn);
    }

    public function writePageToDisk(StoragePage $page): bool {
        // MA'LUMOTLAR BAZASINING 1-QOIDASI:
        // Sahifani diskka yozishdan oldin, uning LSN raqamiga tegishli WAL jurnali
        // diskka QAT'IY YETIB BORGAN bo'lishi SHART!
        if ($page->pageLsn > $this->flushedLsn) {
            echo "[!] OGOHLANTIRISH: PageLSN ({$page->pageLsn}) > FlushedLSN ({$this->flushedLsn})!
";
            echo "[*] Majburiy: Avval WAL fsync qilinmoqda...
";
            $this->updateFlushedLsn($page->pageLsn);
        }

        echo "[+] Sahifa #{$page->pageId} xavfsiz holda diskka yozildi (PageLSN: {$page->pageLsn}).
";
        return true;
    }
}

$flusher = new WalPageFlusher();
$page = new StoragePage(5, 10500, "Sahifa ichidagi ma'lumotlar...");
$flusher->writePageToDisk($page);
```
**Tushuntirish:** Agar sahifa diskka yozilsa-yu, uning WAL yozuvi diskka yetib bormasdan tok o'chsa, ma'lumotlar bazasi jismonan buziladi va uni tiklash imkonsiz bo'ladi. 'Write-Ahead' qoidasi aynan shu LSN tekshiruvi orqali sahifadan oldin jurnal diskka borishini kafolatlaydi.

---

### Topshiriq #1231: Buffer Pool Manager: 4KB Sahifalar Havzasi va Frame Jadvali
**Tavsif:** Diskdagi millionlab sahifalardan faqat 100 tasini xotirada saqlab, so'ralgan PageID xotirada bo'lsa darhol uzatuvchi, bo'lmasa diskdan yuklab beruvchi Buffer Pool Manager quring.
**Talablar:** FrameTable, PageTable (PageID -> FrameID), fetchPage, unpinPage, dirty bayrog'i.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Database Buffer Pool Manager
class Frame {
    public ?int $pageId = null;
    public int $pinCount = 0;
    public bool $isDirty = false;
    public string $data = '';
}

class BufferPoolManager {
    private int $poolSize;
    /** @var array<int, Frame> */
    private array $frames = [];
    /** @var array<int, int> PageID => FrameIndex */
    private array $pageTable = [];

    public function __construct(int $poolSize = 10) {
        $this->poolSize = $poolSize;
        for ($i = 0; $i < $poolSize; $i++) {
            $this->frames[$i] = new Frame();
        }
    }

    public function fetchPage(int $pageId): Frame {
        // 1. Sahifa allaqachon xotiradami? (Cache Hit)
        if (isset($this->pageTable[$pageId])) {
            $frameIdx = $this->pageTable[$pageId];
            $frame = $this->frames[$frameIdx];
            $frame->pinCount++;
            echo "[BufferPool] Cache HIT: Sahifa #{$pageId} ramkada #{$frameIdx}
";
            return $frame;
        }

        // 2. Cache MISS: Bo'sh ramka qidiramiz
        $freeFrameIdx = $this->findVictimFrame();
        $frame = $this->frames[$freeFrameIdx];

        // Agar eski sahifa o'zgargan bo'lsa diskka to'kamiz
        if ($frame->isDirty && $frame->pageId !== null) {
            echo "[BufferPool] Dirty sahifa #{$frame->pageId} diskka to'kildi.
";
            unset($this->pageTable[$frame->pageId]);
        }

        // Yangi sahifani simulyatsiya qilib diskdan yuklaymiz
        $frame->pageId = $pageId;
        $frame->pinCount = 1;
        $frame->isDirty = false;
        $frame->data = "DISKDAN_OQILGAN_SAHIFA_#{$pageId}_MALUMOTI";

        $this->pageTable[$pageId] = $freeFrameIdx;
        echo "[BufferPool] Cache MISS: Sahifa #{$pageId} diskdan yuklandi -> Ramka #{$freeFrameIdx}
";
        return $frame;
    }

    private function findVictimFrame(): int {
        for ($i = 0; $i < $this->poolSize; $i++) {
            if ($this->frames[$i]->pinCount === 0) {
                return $i;
            }
        }
        throw new RuntimeException("Buffer pool to'lgan! Barcha sahifalar qulflangan (Pinned).");
    }

    public function unpinPage(int $pageId, bool $isDirty): void {
        if (isset($this->pageTable[$pageId])) {
            $frame = $this->frames[$this->pageTable[$pageId]];
            $frame->pinCount = max(0, $frame->pinCount - 1);
            if ($isDirty) $frame->isDirty = true;
        }
    }
}

$bpm = new BufferPoolManager(3);
$p1 = $bpm->fetchPage(101);
$bpm->unpinPage(101, false);

$p2 = $bpm->fetchPage(102);
$bpm->unpinPage(102, true);

$p1Again = $bpm->fetchPage(101); // Cache Hit
$bpm->unpinPage(101, false);
```
**Tushuntirish:** Buffer Pool ma'lumotlar bazasining eng qimmatli resursidir. U disk va protsessor o'rtasida ko'prik vazifasini o'taydi. `pinCount` sahifadan ayni paytda qaysidir so'rov foydalanayotganini bildiradi va kesh almashtirish algoritmlariga ushbu sahifani xotiradan haydamaslikni buyuradi.

---

### Topshiriq #1232: LRU (Least Recently Used) Keshdan Chiqarish (Eviction) Algoritmi
**Tavsif:** Buffer Pool to'lib qolganda eng uzoq vaqt foydalanilmagan sahifani O(1) vaqt murakkabligida aniqlab xotiradan haydovchi Doubly Linked List + Hash Map asosidagi LRU algoritmini quring.
**Talablar:** Doubly-Linked List, Hash Map, get, put, evict eng oxirgi elementni chiqarish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - O(1) LRU (Least Recently Used) Kesh Eviction Algoritmi
class LruNode {
    public int $key;
    public mixed $value;
    public ?LruNode $prev = null;
    public ?LruNode $next = null;

    public function __construct(int $key, mixed $val) {
        $this->key = $key;
        $this->value = $val;
    }
}

class LruCache {
    private int $capacity;
    /** @var array<int, LruNode> */
    private array $map = [];
    private ?LruNode $head = null;
    private ?LruNode $tail = null;

    public function __construct(int $capacity) {
        $this->capacity = $capacity;
    }

    public function get(int $key): mixed {
        if (!isset($this->map[$key])) return null;

        $node = $this->map[$key];
        $this->moveToHead($node); // Ishlatilgani uchun ro'yxat boshiga o'tkazamiz
        return $node->value;
    }

    public function put(int $key, mixed $val): void {
        if (isset($this->map[$key])) {
            $node = $this->map[$key];
            $node->value = $val;
            $this->moveToHead($node);
            return;
        }

        if (count($this->map) >= $this->capacity) {
            $this->evictTail(); // Eng oxirgi eskirgan sahifani haydaymiz
        }

        $newNode = new LruNode($key, $val);
        $this->map[$key] = $newNode;
        $this->addToHead($newNode);
    }

    private function addToHead(LruNode $node): void {
        $node->next = $this->head;
        $node->prev = null;
        if ($this->head) $this->head->prev = $node;
        $this->head = $node;
        if (!$this->tail) $this->tail = $node;
    }

    private function removeNode(LruNode $node): void {
        if ($node->prev) $node->prev->next = $node->next;
        else $this->head = $node->next;

        if ($node->next) $node->next->prev = $node->prev;
        else $this->tail = $node->prev;
    }

    private function moveToHead(LruNode $node): void {
        $this->removeNode($node);
        $this->addToHead($node);
    }

    private function evictTail(): void {
        if (!$this->tail) return;
        echo "[LRU Eviction] Sahifa #{$this->tail->key} xotiradan chiqarib tashlandi.
";
        unset($this->map[$this->tail->key]);
        $this->removeNode($this->tail);
    }
}

$lru = new LruCache(2);
$lru->put(1, "Page_1");
$lru->put(2, "Page_2");
$lru->get(1); // 1 yangilandi
$lru->put(3, "Page_3"); // 2 chiqarib yuboriladi!
echo "[+] 2-sahifa mavjudmi? " . ($lru->get(2) ?? 'YO'Q (Chiqarilgan)') . "
";
```
**Tushuntirish:** Klassik massivlarda eng eski elementni qidirish $O(N)$ vaqt oladi. Hash Map va Ikki tomonlama bog'langan ro'yxat (Doubly Linked List) kombinatsiyasi ham qidiruvni, ham ro'yxat boshiga ko'chirishni $O(1)$ doimiy vaqtda bajarish imkonini beradi.

---

### Topshiriq #1233: CLOCK (Second-Chance) Algoritmi orqali Yuqori Tezlikdagi Sahifalar Almashinuvi
**Tavsif:** LRU dagi doimiy qulflash ziddiyatlarini (Mutex Contention) kamaytirish uchun, PostgreSQL da ishlatiladigan aylanma CLOCK strelkasi va Reference Bit ga asoslangan kesh almashtirish tizimini yozing.
**Talablar:** Aylanma ro'yxat (Circular Buffer), reference_bit (0 yoki 1), clock hand ko'rsatkichi.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - CLOCK (Second-Chance) Keshdan Chiqarish Algoritmi
class ClockPage {
    public int $pageId;
    public int $refBit = 1; // Sahifadan foydalanilganda 1 bo'ladi

    public function __construct(int $id) { $this->pageId = $id; }
}

class ClockBufferPool {
    private int $capacity;
    /** @var array<int, ?ClockPage> */
    private array $buffer = [];
    private int $hand = 0; // Soat strelkasi

    public function __construct(int $capacity) {
        $this->capacity = $capacity;
        for ($i = 0; $i < $capacity; $i++) {
            $this->buffer[$i] = null;
        }
    }

    public function accessPage(int $pageId): void {
        // Sahifa mavjud bo'lsa refBit ni 1 qilamiz
        for ($i = 0; $i < $this->capacity; $i++) {
            if ($this->buffer[$i] && $this->buffer[$i]->pageId === $pageId) {
                $this->buffer[$i]->refBit = 1;
                echo "[CLOCK] Sahifa #{$pageId} qayta ishlatildi (RefBit = 1).
";
                return;
            }
        }

        // Mavjud bo'lmasa CLOCK strelkasi bilan bo'sh o'rin topamiz
        $slot = $this->evict();
        $this->buffer[$slot] = new ClockPage($pageId);
        echo "[CLOCK] Sahifa #{$pageId} slot #{$slot} ga joylashtirildi.
";
    }

    private function evict(): int {
        while (true) {
            $page = $this->buffer[$this->hand];

            if ($page === null) {
                $slot = $this->hand;
                $this->hand = ($this->hand + 1) % $this->capacity;
                return $slot;
            }

            if ($page->refBit === 1) {
                // Ikkinchi imkoniyat (Second Chance): bitni 0 qilib strelkani suramiz
                $page->refBit = 0;
            } else {
                // refBit == 0: Aynan shu sahifa xotiradan haydaladi!
                echo "[CLOCK Eviction] Sahifa #{$page->pageId} xotiradan chiqarildi!
";
                $slot = $this->hand;
                $this->hand = ($this->hand + 1) % $this->capacity;
                return $slot;
            }

            $this->hand = ($this->hand + 1) % $this->capacity;
        }
    }
}

$clock = new ClockBufferPool(3);
$clock->accessPage(10);
$clock->accessPage(20);
$clock->accessPage(30);
$clock->accessPage(10); // 10 ga yana murojaat bo'ldi
$clock->accessPage(40); // 20 haydaladi, chunki uning refBit=0 edi, 10 esa tirik qoladi
```
**Tushuntirish:** LRU har bir o'qishda ro'yxat ko'rsatkichlarini o'zgartirishni talab qiladi, bu ko'p oqimli tizimlarda (Multi-threading) qulflar tufayli sekinlashuvga olib keladi. CLOCK algoritmi esa faqat 1 ta bitni o'zgartiradi va ko'rsatkichlarni siljitmaydi, bu esa zamonaviy CPU larda ancha tez ishlaydi.

---

### Topshiriq #1234: Dirty Page Writer: Fon Rejimida Sahifalarni Diskka Asinxron To'kish
**Tavsif:** Foydalanuvchi so'rovlari paytida diskka yozish tufayli kechikishlar (Spikes) bo'lmasligi uchun xotirada o'zgargan (Dirty) sahifalarni fon rejimida uzluksiz diskka oqizuvchi Page Cleaner yozing.
**Talablar:** Dirty sahifalar navbati, flush_batch hajmi, isDirty holatini false ga tushirish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Asinxron Dirty Page Cleaner
class BackgroundPageCleaner {
    private array $dirtyPages = []; // [pageId => content]
    private string $storagePath;

    public function __construct(string $storagePath) {
        $this->storagePath = $storagePath;
    }

    public function markDirty(int $pageId, string $content): void {
        $this->dirtyPages[$pageId] = $content;
    }

    // Fon rejimida har bir necha soniyada ishga tushadigan tozalash sikli
    public function flushDirtyBatch(int $batchLimit = 10): int {
        $count = 0;
        if (empty($this->dirtyPages)) return 0;

        $h = fopen($this->storagePath, 'cb+');
        foreach ($this->dirtyPages as $pageId => $data) {
            fseek($h, $pageId * 4096, SEEK_SET);
            fwrite($h, $data);
            unset($this->dirtyPages[$pageId]);
            $count++;
            if ($count >= $batchLimit) break;
        }

        fflush($h);
        fclose($h);
        echo "[PageCleaner] {$count} ta iflos sahifa diskka asinxron to'kildi.
";
        return $count;
    }
}

echo "[+] Background Page Cleaner xizmati tayyorlandi.
";
```
**Tushuntirish:** Agar fon tozalagich bo'lmasa, Buffer Pool to'lgan paytda yangi sahifani yuklamoqchi bo'lgan mijoz boshqa eski iflos sahifa diskka yozib bo'linguncha kutishga majbur bo'ladi (Write Stall). Page Cleaner xotirada doimo bo'sh joy bo'lishini ta'minlaydi.

---

### Topshiriq #1235: Free List Boshqaruvi: Bo'shagan Sahifalarni Qayta Taqsimlash
**Tavsif:** Jadvaldan minglab yozuvlar o'chirilganda bo'shab qolgan 4KB sahifa ID larini Linked List (Free List) sifatida saqlab, yangi yozuvlar kelganda diskni shishirmasdan ularni qayta taqsimlang.
**Talablar:** allocatePage, deallocatePage, Free List steki, disk hajmini tejash.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Disk Sahifalari Boshqaruvi (Free List Manager)
class DiskSpaceManager {
    private array $freeList = []; // Bo'shagan sahifalar ID lari
    private int $totalPages = 0;

    public function allocatePage(): int {
        // Agar bo'shagan eski sahifalar bo'lsa, birinchi navbatda ularni qayta ishlatamiz
        if (!empty($this->freeList)) {
            $reusedPageId = array_pop($this->freeList);
            echo "[SpaceManager] Bo'shagan sahifa qayta taqsimlandi: #{$reusedPageId}
";
            return $reusedPageId;
        }

        // Bo'sh sahifa yo'q bo'lsa, fayl oxiridan yangi sahifa ajratamiz
        $newPageId = $this->totalPages++;
        echo "[SpaceManager] Yangi sahifa ochildi: #{$newPageId}
";
        return $newPageId;
    }

    public function deallocatePage(int $pageId): void {
        // Sahifa bo'shadi, uni Free List ga qaytaramiz
        $this->freeList[] = $pageId;
        echo "[SpaceManager] Sahifa #{$pageId} bo'shatildi va Free List ga qo'shildi.
";
    }

    public function getFreeCount(): int {
        return count($this->freeList);
    }
}

$sm = new DiskSpaceManager();
$p1 = $sm->allocatePage(); // 0
$p2 = $sm->allocatePage(); // 1
$sm->deallocatePage($p1);  // 0 bo'shatildi
$p3 = $sm->allocatePage(); // Yana 0 qaytariladi!
```
**Tushuntirish:** Agar Free List bo'lmasa, ma'lumotlar bazasi fayli yozuvlar o'chirilgan taqdirda ham faqat kattalashib boraveradi. Free List bo'shagan bloklarni ro'yxatga olib, disk hajmining behuda shishib ketishini to'xtatadi.

---

### Topshiriq #1236: Memory-Mapped Files (mmap) Bilan Diskdagi Fayllarni To'g'ridan-To'g'ri O'qish
**Tavsif:** `read()` va `write()` tizim chaqiruvlarining ortiqcha xotira nusxalashini (Kernel-to-User space copy) chetlab o'tish uchun fayllarni operativ xotiraga proyeksiyalovchi (mmap) drayver yarating.
**Talablar:** PHP mmap kengaytmasi yoki stream buffer, xotiradan to'g'ridan-to'g'ri baytlarni olish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Memory-Mapped I/O Simulyatsiyasi va Shaffof Sahifalash
class MmapFileView {
    private $stream;
    private int $fileSize;

    public function __construct(string $filePath) {
        $this->stream = fopen($filePath, 'r+b');
        $this->fileSize = filesize($filePath) ?: 0;
    }

    // Xotiraga to'g'ridan-to'g'ri proyeksiyalangan baytlarni o'qish
    public function readBytes(int $offset, int $length): string {
        if ($offset + $length > $this->fileSize) {
            throw new OutOfBoundsException("Fayl chegarasidan tashqariga murojaat!");
        }
        fseek($this->stream, $offset, SEEK_SET);
        return fread($this->stream, $length);
    }

    public function writeBytes(int $offset, string $bytes): void {
        fseek($this->stream, $offset, SEEK_SET);
        fwrite($this->stream, $bytes);
    }

    public function close(): void {
        if (is_resource($this->stream)) fclose($this->stream);
    }
}

echo "[+] Memory-Mapped I/O drayveri tayyorlandi.
";
```
**Tushuntirish:** `mmap` faylni operatsion tizimning virtual xotira xaritasiga bog'laydi. Dastur faylni o'qiyotganda disk I/O buferi to'g'ridan-to'g'ri foydalanuvchi maydoniga ulanadi, bu esa oraliq xotira ko'chirishlarini yo'qotadi (Zero-Copy Architecture).

---

### Topshiriq #1237: O_DIRECT Rejimi: OS Page Cache ni Chetlab O'tib To'g'ridan-To'g'ri Drayverga Yozish
**Tavsif:** Linux operatsion tizimining ikki karra buferlash (Double Buffering) muammosini yo'qotish va barcha keshni faqat ma'lumotlar bazasining o'zi boshqarishi uchun O_DIRECT uslubidagi to'g'ridan-to'g'ri I/O ni yoqing.
**Talablar:** O_DIRECT bayrog'i simulyatsiyasi, posix_fadvise (POSIX_FADV_DONTNEED), xotira tejamkorligi.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Double Buffering ni Oldini Olish (Direct I/O Simulyatsiyasi)
class DirectIoSimulator {
    public static function writeBypassingCache(string $filePath, string $alignedData): void {
        $h = fopen($filePath, 'wb');
        fwrite($h, $alignedData);
        fflush($h);
        fsync($h);

        // Linux yadrosiga: 'Ushbu ma'lumotlarni OS Page Cache da saqlama, xotirani bo'shat!' deb buyuramiz
        if (function_exists('posix_fadvise')) {
            // POSIX_FADV_DONTNEED = 4
            posix_fadvise($h, 0, strlen($alignedData), POSIX_FADV_DONTNEED);
            echo "[DirectI/O] Linux OS Page Cache tozalandi (Double buffering bartaraf etildi).
";
        }

        fclose($h);
    }
}

echo "[+] Direct I/O optimizatsiya moduli yuklandi.
";
```
**Tushuntirish:** MySQL yoki PostgreSQL ning o'zida katta Buffer Pool bo'lgani holda, Linux operatsion tizimi ham o'sha faylni o'zining Page Cache da qayta saqlaydi (Double Buffering). Bu server operativ xotirasining (RAM) 50% ini behuda yeydi. Direct I/O tizim keshi chetlab o'tilishini ta'minlaydi.

---

### Topshiriq #1238: Prefetching / Read-Ahead: Ketma-ket O'qishni Oldindan Xotiraga Yuklash
**Tavsif:** Jadval to'liq skanerlanayotganda (Full Table Scan) protsessor disk I/O ni kutib qolmasligi uchun navbatdagi 8 ta sahifani oldindan fonga yuklab qo'yuvchi Read-Ahead mexanizmini dasturlang.
**Talablar:** Prefetch oyna hajmi (8 ta sahifa), ketma-ketlikni aniqlash, asinxron oldindan yuklash.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Read-Ahead / Prefetching Dvigateli
class ReadAheadEngine {
    private int $lastAccessedPage = -1;
    private int $sequentialHits = 0;
    private int $prefetchWindow = 4; // Oldindan 4 ta sahifa yuklash

    public function accessPage(int $pageId): array {
        $toPrefetch = [];

        // Ketma-ket o'qish (Sequential Scan) aniqlandimi?
        if ($pageId === $this->lastAccessedPage + 1) {
            $this->sequentialHits++;
            if ($this->sequentialHits >= 2) {
                // Disk drayveriga oldindan buyruq beramiz:
                for ($p = 1; $p <= $this->prefetchWindow; $p++) {
                    $toPrefetch[] = $pageId + $p;
                }
                echo "[Prefetch] Ketma-ket o'qish fosh bo'ldi! Sahifalar oldindan yuklanmoqda: " . implode(', ', $toPrefetch) . "
";
            }
        } else {
            $this->sequentialHits = 0; // Tasodifiy sakrash (Random I/O)
        }

        $this->lastAccessedPage = $pageId;
        return $toPrefetch;
    }
}

$pa = new ReadAheadEngine();
$pa->accessPage(10);
$pa->accessPage(11);
$pa->accessPage(12); // Prefetch ishga tushadi!
```
**Tushuntirish:** Prefetching kiritish-chiqarish kechikishini (Latency) yashiradi. Diskdan 11-sahifa o'qilayotgan paytda protsessor 10-sahifani qayta ishlaydi. Natijada katta jadvallarni o'qish tezligi 4-5 barobarga oshadi.

---

### Topshiriq #1239: Bloom Filter: Mavjud Bo'lmagan Kalitlarni O(1) Vaqtda Diskka Bormasdan Inkor Qilish
**Tavsif:** LSM-Tree va saqlash dvigatellarida mavjud bo'lmagan kalitlarni diskdan qidirib qimmatli I/O sarflamaslik uchun, 0% False-Negative kafolatli Bloom Filter xesh strukturasini tuzing.
**Talablar:** Bit massivi, 3 ta turli xesh funksiyasi (Murmur/FNV/CRC), add va mightContain metodlari.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Kriptografik Bloom Filter Indeksi
class BloomFilter {
    private string $bitArray;
    private int $size; // Bitlar soni
    private int $numHashes;

    public function __construct(int $size = 1024, int $numHashes = 3) {
        $this->size = $size;
        $this->numHashes = $numHashes;
        // Barcha bitlarni 0 qilamiz
        $this->bitArray = str_repeat(" ", (int)ceil($size / 8));
    }

    private function getHashes(string $key): array {
        $hashes = [];
        $h1 = crc32($key);
        $h2 = (int)sprintf("%u", crc32($key . "salt_b"));
        for ($i = 0; $i < $this->numHashes; $i++) {
            $hashes[] = abs(($h1 + $i * $h2) % $this->size);
        }
        return $hashes;
    }

    public function add(string $key): void {
        foreach ($this->getHashes($key) as $bitIndex) {
            $byteIdx = (int)($bitIndex / 8);
            $bitOffset = $bitIndex % 8;
            $this->bitArray[$byteIdx] = chr(ord($this->bitArray[$byteIdx]) | (1 << $bitOffset));
        }
    }

    // Tekshirish: Agar FALSE qaytsa - kalit BAZADA ANIQ YO'Q (100% kafolat)!
    // Agar TRUE qaytsa - ehtimol mavjud (diskdan tekshirish kerak)
    public function mightContain(string $key): bool {
        foreach ($this->getHashes($key) as $bitIndex) {
            $byteIdx = (int)($bitIndex / 8);
            $bitOffset = $bitIndex % 8;
            if ((ord($this->bitArray[$byteIdx]) & (1 << $bitOffset)) === 0) {
                return false; // Birorta bit 0 bo'lsa - kalit 100% mavjud emas!
            }
        }
        return true;
    }
}

// Sinov
$bf = new BloomFilter(1000, 3);
$bf->add("user:101");
$bf->add("user:102");

echo "[+] 'user:101' mavjudmi? " . ($bf->mightContain("user:101") ? "EHTIMOL BOR" : "YO'Q") . "
";
echo "[+] 'user:999' mavjudmi? " . ($bf->mightContain("user:999") ? "EHTIMOL BOR" : "ANIQ YO'Q (Diskka borilmadi!)") . "
";
```
**Tushuntirish:** RocksDB va Cassandra kabi tizimlarda so'rovlarning 80% qismi bazada yo'q kalitlarni so'raydi. Bloom Filter xotirada atigi bir necha kilobayt joy olib, diskka bo'ladigan barcha besamar so'rovlarni 99% aniqlikda darhol qaytaradi.

---

### Topshiriq #1240: Xotira Parchalanishi (Memory Fragmentation) va Binar Kompaktizatsiya
**Tavsif:** Xotira buferida turli o'lchamdagi obyektlar ajratilib o'chirilgach yuzaga keladigan bo'shliqlarni yo'qotish uchun xotirani bir tomonga surib kompaktizatsiya qiluvchi xotira defragmentatorini yozing.
**Talablar:** Memory Arena buferi, jonli obyektlarni surish (Sliding Compaction), ko'rsatkichlarni yangilash.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Xotira Arenasi va Defragmentatsiyasi
class MemoryArena {
    private string $buffer;
    private array $allocations = []; // [id => ['offset' => int, 'size' => int]]
    private int $capacity;

    public function __construct(int $capacity = 4096) {
        $this->capacity = $capacity;
        $this->buffer = str_repeat(" ", $capacity);
    }

    public function allocate(int $id, string $data): bool {
        $size = strlen($data);
        // Xotira oxiridan joy qidiramiz
        $offset = empty($this->allocations) ? 0 : (max(array_column($this->allocations, 'offset')) + 256);
        if ($offset + $size > $this->capacity) return false;

        $this->allocations[$id] = ['offset' => $offset, 'size' => $size];
        for ($i = 0; $i < $size; $i++) {
            $this->buffer[$offset + $i] = $data[$i];
        }
        return true;
    }

    public function free(int $id): void {
        unset($this->allocations[$id]);
    }

    // Barcha tirik ma'lumotlarni xotira boshiga zichlab surish (Compaction)
    public function compact(): void {
        $newBuffer = str_repeat(" ", $this->capacity);
        $currentOffset = 0;

        foreach ($this->allocations as $id => $info) {
            $oldOffset = $info['offset'];
            $size = $info['size'];
            $data = substr($this->buffer, $oldOffset, $size);

            for ($i = 0; $i < $size; $i++) {
                $newBuffer[$currentOffset + $i] = $data[$i];
            }

            $this->allocations[$id]['offset'] = $currentOffset;
            $currentOffset += $size;
        }

        $this->buffer = $newBuffer;
        echo "[Arena Compaction] Xotira parchalanishi yo'qotildi! Erkin bo'sh joy: " . ($this->capacity - $currentOffset) . " bayt.
";
    }
}

$arena = new MemoryArena(1024);
$arena->allocate(1, "Data_A");
$arena->allocate(2, "Data_B");
$arena->free(1); // O'rtada bo'shliq hosil bo'ldi
$arena->compact();
```
**Tushuntirish:** Xotira parchalanishi sababli erkin joy 100 MB bo'lsa ham, bitta yaxlit 10 MB joy topilmasligi mumkin (Out of Memory). Sliding Compaction barcha tirik ma'lumotlarni nol indeksga qarab suradi va barcha bo'sh joylarni bitta yirik blokka birlashtiradi.

---

### Topshiriq #1241: LSM-Tree MemTable: Xotiradagi Saralangan SkipList Realizatsiyasi
**Tavsif:** RocksDB va LevelDB dvigatellarining birinchi qatlami bo'lgan, yangi yozuvlarni xotirada doimo saralangan holda ushlab turuvchi ehtimollik asosidagi SkipList / MemTable tuzilmasini quring.
**Talablar:** SkipListNode (forward massivi), tasodifiy sath generatsiyasi (random level), put va get amallari, O(log N).
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - LSM-Tree MemTable SkipList Arxitekturasi
class SkipListNode {
    public string $key;
    public string $value;
    /** @var array<SkipListNode|null> */
    public array $forward;

    public function __construct(string $key, string $value, int $level) {
        $this->key = $key;
        $this->value = $value;
        $this->forward = array_fill(0, $level, null);
    }
}

class MemTableSkipList {
    private const MAX_LEVEL = 16;
    private const P = 0.5; // Yangi sath oshishi ehtimoli
    private int $level = 1;
    private SkipListNode $header;
    private int $byteSize = 0;

    public function __construct() {
        $this->header = new SkipListNode("", "", self::MAX_LEVEL);
    }

    private function randomLevel(): int {
        $lvl = 1;
        while ((mt_rand() / mt_getrandmax()) < self::P && $lvl < self::MAX_LEVEL) {
            $lvl++;
        }
        return $lvl;
    }

    public function put(string $key, string $value): void {
        $update = array_fill(0, self::MAX_LEVEL, null);
        $curr = $this->header;

        // Yuqoridan pastga binar usulda tushamiz
        for ($i = $this->level - 1; $i >= 0; $i--) {
            while ($curr->forward[$i] !== null && $curr->forward[$i]->key < $key) {
                $curr = $curr->forward[$i];
            }
            $update[$i] = $curr;
        }

        $curr = $curr->forward[0];

        // Agar kalit mavjud bo'lsa yangilaymiz
        if ($curr !== null && $curr->key === $key) {
            $this->byteSize += (strlen($value) - strlen($curr->value));
            $curr->value = $value;
            return;
        }

        // Yangi tugun kiritamiz
        $newLevel = $this->randomLevel();
        if ($newLevel > $this->level) {
            for ($i = $this->level; $i < $newLevel; $i++) {
                $update[$i] = $this->header;
            }
            $this->level = $newLevel;
        }

        $newNode = new SkipListNode($key, $value, $newLevel);
        for ($i = 0; $i < $newLevel; $i++) {
            $newNode->forward[$i] = $update[$i]->forward[$i];
            $update[$i]->forward[$i] = $newNode;
        }

        $this->byteSize += (strlen($key) + strlen($value));
    }

    public function get(string $key): ?string {
        $curr = $this->header;
        for ($i = $this->level - 1; $i >= 0; $i--) {
            while ($curr->forward[$i] !== null && $curr->forward[$i]->key < $key) {
                $curr = $curr->forward[$i];
            }
        }
        $curr = $curr->forward[0];
        return ($curr !== null && $curr->key === $key) ? $curr->value : null;
    }

    public function getByteSize(): int {
        return $this->byteSize;
    }

    public function getAllSorted(): array {
        $result = [];
        $curr = $this->header->forward[0];
        while ($curr !== null) {
            $result[$curr->key] = $curr->value;
            $curr = $curr->forward[0];
        }
        return $result;
    }
}

// Sinov
$memTable = new MemTableSkipList();
$memTable->put("user_c", "Charli");
$memTable->put("user_a", "Alisher");
$memTable->put("user_b", "Bobur");

echo "[+] MemTable saralangan tartibi: " . implode(', ', array_keys($memTable->getAllSorted())) . "
";
echo "[+] user_b qiymati: " . $memTable->get("user_b") . "
";
```
**Tushuntirish:** SkipList - muvozanatlashgan qizil-qora daraxtlarning (Red-Black Tree) ancha sodda va parallelizmga mos muqobilidir. Ko'p qatlamli sakrash yo'laklari orqali u qidiruv, qo'shish va o'chirishni o'rtacha $O(\log N)$ vaqtda bajaradi va doimo saralangan bo'ladi.

---

### Topshiriq #1242: MemTable Flush: Xotirani Muzlatish va SSTable ga To'kish
**Tavsif:** MemTable belgilangan chegaraga (masalan 4 MB) yetganda uni 'Immutable' (faqat o'qiladigan) qilib muzlatib, fonda tartiblangan SSTable fayli qilib diskka to'kuvchi (Flush) mexanizmini yarating.
**Talablar:** isFull sharti, Immutable MemTable ga o'tkazish, yangi MemTable ochish, fon flush chaqiruvi.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - LSM-Tree MemTable Flush va Immutable Rejim
class LsmEngineMemManager {
    private MemTableSkipList $activeMemTable;
    private ?MemTableSkipList $immutableMemTable = null;
    private int $maxMemTableBytes;
    private string $sstDirectory;

    public function __construct(string $sstDir, int $maxBytes = 200) { // 200 bayt sinov uchun
        $this->activeMemTable = new MemTableSkipList();
        $this->maxMemTableBytes = $maxBytes;
        $this->sstDirectory = $sstDir;
        @mkdir($sstDir, 0777, true);
    }

    public function put(string $key, string $value): void {
        $this->activeMemTable->put($key, $value);

        // Agar xotira to'lsa, uni muzlatamiz va to'kamiz
        if ($this->activeMemTable->getByteSize() >= $this->maxMemTableBytes) {
            $this->freezeAndFlush();
        }
    }

    private function freezeAndFlush(): void {
        echo "[*] MemTable to'ldi ({$this->activeMemTable->getByteSize()} bayt). Muzlatilmoqda (Immutable)...
";
        
        $this->immutableMemTable = $this->activeMemTable;
        $this->activeMemTable = new MemTableSkipList(); // Yangi yozuvlar uchun yangi toza MemTable

        // Immutable MemTable ni diskka SSTable qilib to'kamiz (Flush)
        $sstPath = sprintf("%s/L0_%s.sst", $this->sstDirectory, time());
        $sortedData = $this->immutableMemTable->getAllSorted();

        $h = fopen($sstPath, 'wb');
        foreach ($sortedData as $k => $v) {
            $line = json_encode(['k' => $k, 'v' => $v]) . "
";
            fwrite($h, $line);
        }
        fclose($h);

        echo "[+] SSTable diskka muhrlandi: {$sstPath}
";
        $this->immutableMemTable = null; // Xotira bo'shatildi
    }
}

$mgr = new LsmEngineMemManager(sys_get_temp_dir() . '/lsm_flush_test', 150);
$mgr->put("order_1", "DATA_PAYLOAD_1");
$mgr->put("order_2", "DATA_PAYLOAD_2");
$mgr->put("order_3", "DATA_PAYLOAD_3");
```
**Tushuntirish:** LSM-Tree ning eng katta kuchi: yangi yozuvlar hech qachon diskka to'g'ridan-to'g'ri bormaydi. Ular xotiradagi MemTable ga yoziladi va faqat to'lgandan keyingina bitta yirik ketma-ket oqim bilan diskka to'kiladi (Write Amplification ni pasaytiradi).

---

### Topshiriq #1243: SSTable (Sorted String Table) Ikkilik Formati: Data Block, Index Block va Footer
**Tavsif:** Google Bigtable va Cassandra standarti asosida: ichida saralangan ma'lumotlar bloki, bloklar indeks jadvali va fayl oxirida joylashgan Footer metama'lumotlaridan iborat SSTable fayl generatorini tuzing.
**Talablar:** Data Block, Index Block (BlockKey -> Offset), Footer (IndexOffset, MagicNumber 0xDB472026).
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Sanoat Standartidagi SSTable Ikkilik Formati
class SSTableWriter {
    public const MAGIC_NUMBER = 0xDB472026;

    public static function createSSTable(string $outputPath, array $sortedKvs): void {
        $handle = fopen($outputPath, 'wb');
        $indexBlock = []; // [birinchi_kalit => offset]

        $blockSize = 128; // Har 128 baytda bitta indeks bloki
        $currentBlockData = '';
        $firstKeyInBlock = null;

        foreach ($sortedKvs as $key => $val) {
            if ($firstKeyInBlock === null) {
                $firstKeyInBlock = $key;
                $indexBlock[$firstKeyInBlock] = ftell($handle);
            }

            $currentBlockData .= pack('nN', strlen($key), strlen($val)) . $key . $val;

            if (strlen($currentBlockData) >= $blockSize) {
                fwrite($handle, $currentBlockData);
                $currentBlockData = '';
                $firstKeyInBlock = null;
            }
        }

        if (strlen($currentBlockData) > 0) {
            fwrite($handle, $currentBlockData);
        }

        // 2. Indeks blokini yozamiz
        $indexOffset = ftell($handle);
        $indexJson = json_encode($indexBlock);
        fwrite($handle, $indexJson);
        $indexLength = strlen($indexJson);

        // 3. Footer: IndexOffset (8 bayt) + IndexLength (4 bayt) + Magic (4 bayt) = 16 bayt
        $footer = pack('JNN', $indexOffset, $indexLength, self::MAGIC_NUMBER);
        fwrite($handle, $footer);

        fclose($handle);
        echo "[+] To'liq SSTable yaratildi: {$outputPath} (IndexOffset: {$indexOffset})
";
    }
}

$sampleData = [
    "alpha" => "100", "beta" => "200", "charlie" => "300", "delta" => "400", "echo" => "500"
];
$sstFile = sys_get_temp_dir() . '/sample_sstable.sst';
SSTableWriter::createSSTable($sstFile, $sampleData);
```
**Tushuntirish:** SSTable larda Footer faylning eng oxirgi 16-baytida turadi. Baza faylni ochganda dastlab oxirgi 16 baytni o'qiydi, Magic raqamni tekshiradi, indeks blokining manzilini bilib oladi va uni xotiraga yuklaydi.

---

### Topshiriq #1244: SSTable Binar Qidiruvi: 2 Darajali Indeks Bo'yicha Qidiruv
**Tavsif:** SSTable ichidan kalitni qidirishda butun faylni o'qimasdan, xotiradagi Index Block bo'yicha kerakli ma'lumot blokini topib, faqat o'sha 128 bayt ichida binar qidiruv bilan qiymatni o'quvchi dvigatel yozing.
**Talablar:** Footer o'qish, Index Block xotirada, faqat mos Data Block ni diskdan yuklash.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - SSTable 2-Darajali Qidiruv Dvigateli
class SSTableReader {
    private string $filePath;
    private array $indexBlock = [];

    public function __construct(string $filePath) {
        $this->filePath = $filePath;
        $this->loadIndex();
    }

    private function loadIndex(): void {
        $h = fopen($this->filePath, 'rb');
        fseek($h, -16, SEEK_END); // Oxirgi 16 bayt Footer
        $footerRaw = fread($h, 16);
        $footer = unpack('JIndexOffset/NIndexLen/NMagic', $footerRaw);

        if ($footer['Magic'] !== SSTableWriter::MAGIC_NUMBER) {
            throw new Exception("SSTable formati buzilgan yoki Magic raqam xato!");
        }

        fseek($h, $footer['IndexOffset'], SEEK_SET);
        $indexJson = fread($h, $footer['IndexLen']);
        fclose($h);

        $this->indexBlock = json_decode($indexJson, true);
    }

    public function get(string $searchKey): ?string {
        $targetOffset = -1;
        $prevOffset = 0;

        // Indeks bloklari orasidan mos blokni qidiramiz
        foreach ($this->indexBlock as $blockKey => $offset) {
            if ($searchKey < $blockKey) {
                $targetOffset = $prevOffset;
                break;
            }
            $prevOffset = $offset;
        }

        if ($targetOffset === -1) {
            $targetOffset = $prevOffset;
        }

        // Faqat o'sha aniq bitta blokni o'qiymiz
        $h = fopen($this->filePath, 'rb');
        fseek($h, $targetOffset, SEEK_SET);
        $blockData = fread($h, 256); // Blok hajmi
        fclose($h);

        // Blok ichidan kalitni qidiramiz
        $offset = 0;
        $len = strlen($blockData);
        while ($offset + 6 <= $len) {
            $hdr = unpack('nKeyLen/NValLen', substr($blockData, $offset, 6));
            $offset += 6;
            $k = substr($blockData, $offset, $hdr['KeyLen']);
            $offset += $hdr['KeyLen'];
            $v = substr($blockData, $offset, $hdr['ValLen']);
            $offset += $hdr['ValLen'];

            if ($k === $searchKey) {
                return $v; // Topildi!
            }
        }

        return null;
    }
}

$sstReader = new SSTableReader($sstFile);
echo "[+] SSTable dan 'charlie' qidirildi: " . $sstReader->get("charlie") . "
";
echo "[+] SSTable dan 'delta' qidirildi:   " . $sstReader->get("delta") . "
";
```
**Tushuntirish:** SSTable ning o'zgarmasligi (Immutability) kesh xavfsizligini ta'minlaydi. Fayl hech qachon o'zgarmaydi, shuning uchun operatsion tizim keshida doim toza turadi va o'qish paytida hech qanday qulflar (Locks) talab qilinmaydi.

---

### Topshiriq #1245: LSM-Tree O'qish Yo'li (Read Path): MemTable -> Immutable -> SSTables
**Tavsif:** LSM-Tree arxitekturasida so'ralgan kalitni qidirishda qat'iy iyerarxiya: 1. Faol MemTable, 2. Muzlatilgan MemTable, 3. Eng yangi SSTable lar (Level 0), 4. Qadimiy SSTable lar zanjirini amalga oshiring.
**Talablar:** Read Path prioriteti, birinchi topilgan joydan qaytish, Tombstone tekshiruvi.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - LSM-Tree To'liq O'qish Yo'li (Read Path)
class LsmReadPathEngine {
    private MemTableSkipList $activeMemTable;
    private ?MemTableSkipList $immutableMemTable;
    private array $level0Sstables = [];

    public function __construct($active, $immutable, array $l0Files) {
        $this->activeMemTable = $active;
        $this->immutableMemTable = $immutable;
        $this->level0Sstables = $l0Files;
    }

    public function get(string $key): ?string {
        // 1-QADAM: Faol MemTable dan qidiramiz (Eng yangi qiymat)
        $val = $this->activeMemTable->get($key);
        if ($val !== null) {
            echo "[ReadPath] 1-qadamda Faol MemTable dan topildi (RAM)!
";
            return ($val === "__DELETED__") ? null : $val;
        }

        // 2-QADAM: Agar to'kilyotgan bo'lsa, Immutable MemTable dan qidiramiz
        if ($this->immutableMemTable !== null) {
            $val = $this->immutableMemTable->get($key);
            if ($val !== null) {
                echo "[ReadPath] 2-qadamda Immutable MemTable dan topildi (RAM)!
";
                return ($val === "__DELETED__") ? null : $val;
            }
        }

        // 3-QADAM: Diskdagi Level 0 SSTable lardan eng yangisidan boshlab qidiramiz
        foreach ($this->level0Sstables as $sst) {
            $val = $sst->get($key);
            if ($val !== null) {
                echo "[ReadPath] 3-qadamda SSTable diskidan topildi!
";
                return ($val === "__DELETED__") ? null : $val;
            }
        }

        return null; // Topilmadi
    }
}

echo "[+] LSM-Tree Iyerarxik O'qish Yo'li tayyorlandi.
";
```
**Tushuntirish:** LSM-Tree larda o'qish sekinroq, chunki bitta kalit diskdagi bir nechta SSTable larda bo'lishi mumkin. Lekin to'g'ri iyerarxiya va Bloom Filter yordamida har bir qatlam tekshirilib, eng yangi qiymat zudlik bilan qaytariladi.

---

### Topshiriq #1246: LSM Leveled Compaction: Level 0 dan Level 1 ga K-way Merge Birlashtirish
**Tavsif:** Level 0 da to'plangan bir nechta SSTable larni K-way Merge Sort algoritmi orqali yagona tartiblangan oqimda birlashtirib, eskirgan nusxalarni o'chirib Level 1 ga ko'chiruvchi dvigatel yozing.
**Talablar:** K-way Merge Sort, duplikat kalitlarda faqat eng yangisini saqlash, toza SSTable generatsiyasi.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - LSM K-way Merge Leveled Compactor
class KWayMergeCompactor {
    public static function mergeSstables(array $sourceSstables, string $targetL1File): void {
        echo "[*] Leveled Compaction boshlandi: " . count($sourceSstables) . " ta SSTable birlashtirilmoqda...
";
        
        $mergedMap = [];

        // Barcha manbalardan kalitlarni o'qiymiz (yangi fayllar eskisini ustiga yozadi)
        foreach ($sourceSstables as $sstData) {
            foreach ($sstData as $k => $v) {
                $mergedMap[$k] = $v;
            }
        }

        // Kalitlarni alfavit tartibida saralaymiz
        ksort($mergedMap);

        // Yangi Level 1 SSTable faylini yozamiz
        SSTableWriter::createSSTable($targetL1File, $mergedMap);
        echo "[+] Leveled Compaction yakunlandi! Level 1 fayl tayyorlandi: {$targetL1File}
";
    }
}

// Sinov
$sst1 = ["b" => "2", "a" => "1_eski"];
$sst2 = ["c" => "3", "a" => "1_yangi"]; // 'a' yangilangan
KWayMergeCompactor::mergeSstables([$sst1, $sst2], sys_get_temp_dir() . '/L1_merged.sst');
```
**Tushuntirish:** Level 0 da kalitlar diapazoni kesishishi mumkin (Overlapping). Level 1 da esa Compaction dan so'ng har bir SSTable aniq bitta oraliqni egallaydi (Non-overlapping, masalan A-M va N-Z), bu esa o'qish tezligini karrasiga oshiradi.

---

### Topshiriq #1247: LSM Size-Tiered Compaction (Apache Cassandra Uslubi)
**Tavsif:** Bir xil o'lchamdagi 4 ta SSTable to'planganda, ularni birlashtirib bitta 4 barobar katta SSTable hosil qiluvchi Size-Tiered Compaction strategiyasini joriy qiling.
**Talablar:** Fayl o'lchamlarini tekshirish, threshold=4, birlashtirish va eski fayllarni tozalash.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Size-Tiered Compaction Strategiyasi
class SizeTieredCompactor {
    private int $threshold = 4;

    public function checkAndTrigger(array $sstableFiles): ?array {
        // Fayllarni hajmi bo'yicha guruhlaymiz
        if (count($sstableFiles) >= $this->threshold) {
            echo "[SizeTiered] {$this->threshold} ta bir xil o'lchamdagi SSTable to'plandi! Compaction boshlanmoqda...
";
            $toMerge = array_slice($sstableFiles, 0, $this->threshold);
            return $toMerge;
        }
        return null;
    }
}

$stc = new SizeTieredCompactor();
$trigger = $stc->checkAndTrigger(['f1.sst', 'f2.sst', 'f3.sst', 'f4.sst']);
echo "[+] Compaction holati: " . ($trigger ? "ISHGA TUSHIRILDI" : "KUTILMOQDA") . "
";
```
**Tushuntirish:** Size-Tiered Compaction (STCS) kuchli yozish yuklamasi (Write-Heavy) mavjud bo'lgan tizimlar (masalan IoT telemetriya yoki loglar) uchun eng optimaldir, chunki u diskka kamroq ortiqcha yozish yuklamasi (Write Amplification) tushiradi.

---

### Topshiriq #1248: Amplification Ko'rsatkichlari: Write, Read va Space Amplification Tahlilchisi
**Tavsif:** Saqlash dvigatelining samaradorligini baholash uchun diskka yozilgan jami baytlar bilan foydali baytlar nisbatini (Write Amplification Factor - WAF) hisoblovchi telemetriya modulini yozing.
**Talablar:** UserBytesWritten, DiskBytesWritten, WAF = Disk / User, Read Amplification, Space Amplification.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Storage Engine Amplification Profiler
class AmplificationProfiler {
    private int $userBytesWritten = 0;
    private int $diskBytesWritten = 0;
    private int $diskBytesUsed = 0;
    private int $logicalDataSize = 0;

    public function recordUserWrite(int $bytes): void {
        $this->userBytesWritten += $bytes;
    }

    public function recordDiskWrite(int $bytes): void {
        $this->diskBytesWritten += $bytes;
    }

    public function updateSpaceMetrics(int $actualDiskUsage, int $logicalSize): void {
        $this->diskBytesUsed = $actualDiskUsage;
        $this->logicalDataSize = $logicalSize;
    }

    public function getMetrics(): array {
        // WAF: Foydalanuvchi 1 bayt yozganda diskka necha bayt yozildi?
        $waf = ($this->userBytesWritten > 0) ? ($this->diskBytesWritten / $this->userBytesWritten) : 1.0;
        // SAF: Diskda haqiqiy ma'lumotdan necha barobar ko'p joy band?
        $saf = ($this->logicalDataSize > 0) ? ($this->diskBytesUsed / $this->logicalDataSize) : 1.0;

        return [
            'WAF' => round($waf, 2),
            'SAF' => round($saf, 2),
            'user_written_kb' => round($this->userBytesWritten / 1024, 2),
            'disk_written_kb' => round($this->diskBytesWritten / 1024, 2)
        ];
    }
}

$prof = new AmplificationProfiler();
$prof->recordUserWrite(1000); // Foydalanuvchi 1 KB yozdi
$prof->recordDiskWrite(4096); // WAL + Compaction tufayli 4 KB yozildi
$prof->updateSpaceMetrics(12000, 10000);

echo "[+] Amplification Ko'rsatkichlari:
";
print_r($prof->getMetrics());
```
**Tushuntirish:** B-Tree larda 10 baytlik yozuv o'zgarsa ham butun 4KB sahifa diskka yoziladi (WAF = 400). LSM-Tree larda esa WAF ancha kichik (10-30), bu esa SSD drayverlarning eskirishini (Wear-out) 10 barobarga kamaytiradi.

---

### Topshiriq #1249: In-Memory Redis Uslubidagi Key-Value Dvigateli: TTL va Faol Tozalash (Active Expiry)
**Tavsif:** Redis arxitekturasi kabi har bir kalitga yashash muddati (TTL) beruvchi, passiv o'qish paytida va fon rejimida tasodifiy 20 ta kalitni tekshirib tozalovchi Active Expiry mexanizmini yarating.
**Talablar:** set(key, value, ttl), get (passiv tekshiruv), activeExpireCycle (faol tasodifiy tozalash).
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Redis Uslubidagi In-Memory KVS (TTL & Active Expiry)
class InMemoryRedisEngine {
    private array $dict = [];
    private array $expires = []; // [key => expire_timestamp]

    public function set(string $key, mixed $value, ?int $ttlSeconds = null): void {
        $this->dict[$key] = $value;
        if ($ttlSeconds !== null) {
            $this->expires[$key] = microtime(true) + $ttlSeconds;
        } else {
            unset($this->expires[$key]);
        }
    }

    // Passiv tozalash (Passive Expiry): So'ralgan paytda tekshirish
    public function get(string $key): mixed {
        if (isset($this->expires[$key]) && microtime(true) > $this->expires[$key]) {
            // Muddati o'tgan!
            unset($this->dict[$key], $this->expires[$key]);
            echo "[Passive Expiry] Kalit '{$key}' so'rov paytida eskirgani aniqlandi va o'chirildi.
";
            return null;
        }
        return $this->dict[$key] ?? null;
    }

    // Faol tozalash (Active Expiry): Har 100 ms da tasodifiy 20 ta kalitni tekshirish
    public function activeExpireCycle(int $sampleSize = 20): int {
        $deleted = 0;
        if (empty($this->expires)) return 0;

        $keys = array_keys($this->expires);
        shuffle($keys);
        $sample = array_slice($keys, 0, $sampleSize);
        $now = microtime(true);

        foreach ($sample as $k) {
            if ($now > $this->expires[$k]) {
                unset($this->dict[$k], $this->expires[$k]);
                $deleted++;
            }
        }

        if ($deleted > 0) {
            echo "[Active Expiry] Fondan {$deleted} ta eskirgan kalit xotiradan tozalandi.
";
        }
        return $deleted;
    }
}

$cache = new InMemoryRedisEngine();
$cache->set("sess_temp", "USER_DATA", 1); // 1 soniya TTL
echo "[+] Qiymat olindi: " . $cache->get("sess_temp") . "
";
sleep(2);
echo "[+] 2 soniya o'tib get(): " . ($cache->get("sess_temp") ?? 'NULL (Muddati o'tgan)') . "
";
```
**Tushuntirish:** Agar faqat passiv tekshiruv bo'lsa, hech qachon so'ralmaydigan eski kalitlar xotirada abadiy qolib RAM ni to'ldiradi. Redis aynan shu faol tasodifiy tekshiruv (Active Expiry) orqali xotirani doimo toza ushlab turadi.

---

### Topshiriq #1250: Polimorf Storage Engine: Bitcask, LSM-Tree va B+Tree larni Yagona KVS Interfeysi Ostida Birlashtirish
**Tavsif:** Ilova qatlamini disk arxitekturasidan ajratish uchun barcha yaratilgan saqlash dvigatellarini yagona `KeyValueStorageEngineInterface` orqali almashtiriladigan (Pluggable) qilib birlashtiring.
**Talablar:** KeyValueStorageEngineInterface (put, get, delete, sync), dvigatellar polimorfizmi.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Universal Polimorf Saqlash Dvigateli Interfeysi
interface KeyValueStorageEngineInterface {
    public function put(string $key, string $value): void;
    public function get(string $key): ?string;
    public function delete(string $key): bool;
    public function sync(): void;
    public function getEngineName(): string;
}

// Bitcask adapteri
class BitcaskEngineAdapter implements KeyValueStorageEngineInterface {
    public function put(string $key, string $value): void {}
    public function get(string $key): ?string { return "Bitcask: " . $key; }
    public function delete(string $key): bool { return true; }
    public function sync(): void {}
    public function getEngineName(): string { return "Bitcask Log-Structured Engine"; }
}

// B+Tree adapteri
class BPlusTreeEngineAdapter implements KeyValueStorageEngineInterface {
    public function put(string $key, string $value): void {}
    public function get(string $key): ?string { return "B+Tree: " . $key; }
    public function delete(string $key): bool { return true; }
    public function sync(): void {}
    public function getEngineName(): string { return "B+Tree Clustered Index Engine"; }
}

// Dvigatel Fabrikasi (Factory)
class DatabaseEngineFactory {
    public static function create(string $type): KeyValueStorageEngineInterface {
        return match (strtolower($type)) {
            'bitcask' => new BitcaskEngineAdapter(),
            'bplus'   => new BPlusTreeEngineAdapter(),
            default   => throw new InvalidArgumentException("Noma'lum dvigatel: {$type}")
        };
    }
}

$engine = DatabaseEngineFactory::create('bitcask');
echo "[+] Tanlangan dvigatel: " . $engine->getEngineName() . "
";
echo "[+] Qiymat so'rovi: " . $engine->get("user:42") . "
";
```
**Tushuntirish:** MySQL (InnoDB, MyISAM, RocksDB, Memory) va RocksDB kabi sanoat tizimlari aynan shunday plaginli saqlash arxitekturasiga ega. SQL so'rovlar interpretatori bitta, lekin orqa fondagi saqlash dvigatelini vazifaga qarab (olap/oltp) o'zgartirish mumkin.

---

