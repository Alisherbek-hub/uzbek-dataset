# C++ 25-Modul: Ma'lumotlar Bazasi Ichki Dvigatellari (Storage Engines, LSM-Trees va B+Trees)

Ushbu modulda RocksDB va LevelDB uslubidagi zamonaviy LSM-Tree va Concurrent B+Tree saqlash dvigatellarining chuqur arxitekturasi va ishlab turgan C++20 yechimlari keltirilgan.

### Topshiriq #1201: LSM-Tree MemTable uchun Lock-Free SkipList Node tuzilmasi
**Tavsif:** LSM-Tree (Log-Structured Merge-tree) arxitekturasida yozish operatsiyalari xotiradagi MemTable ga tushadi. MemTable ning asosi - saralangan ma'lumotlar strukturasi bo'lgan SkipList hisoblanadi. RocksDB/LevelDB kabi yuqori unumdor tizimlarda SkipList ko'p oqimli (concurrent) o'qishni blokirovkasiz (lock-free) ta'minlashi lozim.
**Talablar:** C++20 standarti. `SkipListNode` strukturasi ixtiyoriy balandlikdagi (probabilistic height) pointerlar massiviga ega bo'lsin. Pointerlar `std::atomic<Node*>` orqali ifodalansin va acquire-release xotira tartiblanishi (memory ordering) qo'llansin.
**Yechim (C++):**
```cpp
#include <iostream>
#include <atomic>
#include <memory>
#include <vector>
#include <random>
#include <string>

// Maksimal SkipList balandligi (LevelDB/RocksDB da 12 yoki 32)
constexpr int MAX_HEIGHT = 16;
constexpr float PROBABILITY = 0.25f;

// SkipList tugun (Node) strukturasi
template <typename Key, typename Value>
struct SkipListNode {
    Key key;
    Value value;
    int height;
    
    // Har bir darajadagi keyingi tugunga atomik ko'rsatkichlar massivi
    std::atomic<SkipListNode*> next[1];

    // Dinamik balandlik bilan tugun ajratish
    static SkipListNode* create(const Key& k, const Value& v, int h) {
        size_t size = sizeof(SkipListNode) + (h - 1) * sizeof(std::atomic<SkipListNode*>);
        void* mem = ::operator new(size);
        return new (mem) SkipListNode(k, v, h);
    }

    static void destroy(SkipListNode* node) {
        if (node) {
            node->~SkipListNode();
            ::operator delete(node);
        }
    }

private:
    SkipListNode(const Key& k, const Value& v, int h) : key(k), value(v), height(h) {
        for (int i = 0; i < h; ++i) {
            next[i].store(nullptr, std::memory_order_relaxed);
        }
    }
};

// Tasodifiy balandlik generatori (Geometric distribution)
class HeightGenerator {
    std::mt19937 rng;
    std::uniform_real_distribution<float> dist;
public:
    HeightGenerator() : rng(1337), dist(0.0f, 1.0f) {}

    int random_height() {
        int height = 1;
        while (height < MAX_HEIGHT && dist(rng) < PROBABILITY) {
            height++;
        }
        return height;
    }
};

int main() {
    HeightGenerator hg;
    auto node = SkipListNode<std::string, std::string>::create("user:1001", "Alisher Navoiy", hg.random_height());
    std::cout << "Node yaratildi: Key=" << node->key << ", Height=" << node->height << std::endl;
    SkipListNode<std::string, std::string>::destroy(node);
    return 0;
}
```
**Tushuntirish:** SkipList da moslashuvchan massiv (flexible array member) uslubi dinamik balandlik uchun faqat kerakli xotirani ajratadi. Atomic pointerlar va memory ordering yordamida o'quvchi oqimlar mutexsiz, to'liq lock-free holatda saralangan ma'lumotlarni o'qiy oladi.

### Topshiriq #1202: Concurrent SkipList Lock-Free Read va Point Lookup
**Tavsif:** Ma'lumotlar bazasida yozish oqimi MemTable ga yangi kalitlarni qo'shayotganda, ko'plab o'quvchi oqimlar hech qanday to'siqsiz (lock contention) kalitni binary-search tezligida qidirishi zarur.
**Talablar:** C++20, `std::memory_order_acquire` orqali keyingi pointerlarni xavfsiz o'qish, eng yuqori darajadan pastga qarab tushuvchi qidiruv algoritmi.
**Yechim (C++):**
```cpp
#include <iostream>
#include <atomic>
#include <optional>
#include <string>

template <typename Key, typename Value>
class ConcurrentSkipList {
    struct Node {
        Key key;
        Value value;
        int height;
        std::atomic<Node*> next[1];
        
        static Node* create(const Key& k, const Value& v, int h) {
            void* mem = ::operator new(sizeof(Node) + (h - 1) * sizeof(std::atomic<Node*>));
            return new (mem) Node(k, v, h);
        }
    private:
        Node(const Key& k, const Value& v, int h) : key(k), value(v), height(h) {
            for (int i = 0; i < h; ++i) next[i].store(nullptr, std::memory_order_relaxed);
        }
    };

    std::atomic<int> max_height_{1};
    Node* head_;

public:
    ConcurrentSkipList() {
        head_ = Node::create(Key{}, Value{}, 16);
    }

    // Lock-Free point lookup
    std::optional<Value> find(const Key& target) const {
        Node* curr = head_;
        int level = max_height_.load(std::memory_order_relaxed) - 1;

        for (; level >= 0; --level) {
            Node* next = curr->next[level].load(std::memory_order_acquire);
            while (next != nullptr && next->key < target) {
                curr = next;
                next = curr->next[level].load(std::memory_order_acquire);
            }
            if (next != nullptr && next->key == target) {
                return next->value; // Topildi!
            }
        }
        return std::nullopt; // Mavjud emas
    }
};

int main() {
    ConcurrentSkipList<std::string, std::string> skl;
    auto val = skl.find("order:999");
    std::cout << "Kalit holati: " << (val.has_value() ? *val : "Mavjud emas") << std::endl;
    return 0;
}
```
**Tushuntirish:** Har bir qavatda acquire semantikasi orqali ko'rsatkich o'qiladi. Bu xotira modelida yozuvchi oqim tomonidan kiritilgan kalit va qiymat to'liq sinxronlangan bo'lishini kafolatlaydi, o'quvchi esa hech qachon mutex kutmaydi.

### Topshiriq #1203: MemTable Interfeysi va Unumdor Write Path
**Tavsif:** LSM dvigatelida MemTable barcha kiruvchi `Put` va `Delete` so'rovlarini qabul qiladi. `Delete` aslida ma'lumotni darhol o'chirmaydi, balki Tombstone (o'chirish belgisi) yozuvini kiritadi.
**Talablar:** C++20, `ValueType::kTypeValue` va `ValueType::kTypeDeletion` enumlari, ichki SequenceNumber bilan versiyalash.
**Yechim (C++):**
```cpp
#include <iostream>
#include <string>
#include <cstdint>
#include <map>

enum class ValueType : uint8_t {
    kTypeDeletion = 0x0,
    kTypeValue = 0x1
};

struct ParsedInternalKey {
    std::string user_key;
    uint64_t sequence_number;
    ValueType type;
};

class MemTable {
    // Soddalashtirilgan internal saqlash (haqiqiy tizimda Concurrent SkipList)
    std::map<std::string, std::pair<ValueType, std::string>> table_;
    size_t approximate_memory_usage_{0};

public:
    void add(uint64_t seq, ValueType type, const std::string& key, const std::string& value) {
        // RocksDB uslubidagi internal key: [user_key][seq << 8 | type]
        table_[key] = {type, value};
        approximate_memory_usage_ += key.size() + value.size() + sizeof(seq) + sizeof(type);
    }

    bool get(const std::string& key, std::string* value) const {
        auto it = table_.find(key);
        if (it != table_.end()) {
            if (it->second.first == ValueType::kTypeDeletion) {
                return false; // O'chirilgan (Tombstone)
            }
            *value = it->second.second;
            return true;
        }
        return false;
    }

    size_t memory_usage() const { return approximate_memory_usage_; }
};

int main() {
    MemTable mem;
    mem.add(101, ValueType::kTypeValue, "balance:uzer1", "500000");
    std::string val;
    if (mem.get("balance:uzer1", &val)) {
        std::cout << "Balans: " << val << " so'm\n";
    }
    mem.add(102, ValueType::kTypeDeletion, "balance:uzer1", "");
    std::cout << "O'chirilgandan so'ng topildimi: " << (mem.get("balance:uzer1", &val) ? "Ha" : "Yo'q") << std::endl;
    return 0;
}
```
**Tushuntirish:** LSM daraxtlarida o'chirish operatsiyasi yangi yozuv qo'shish bilan bir xil xarajatga ega. Diskdagi eski yozuvlar keyinchalik Compaction paytida jismonan yo'q qilinadi.

### Topshiriq #1204: MemTable Xotira Kvotasi va Immutable MemTable Flush Trigger
**Tavsif:** MemTable hajmi belgilangan chegaraga (masalan 64MB) yetganda, u o'zgarishsiz (Immutable) holatga o'tishi va yangi bo'sh MemTable faollashishi lozim. Orqa fonda esa Immutable MemTable diskka SSTable qilib yoziladi.
**Talablar:** C++20, `std::shared_ptr`, atomik bayroqlar va oqimlararo sinxronizatsiya (`std::condition_variable`).
**Yechim (C++):**
```cpp
#include <iostream>
#include <memory>
#include <atomic>
#include <mutex>
#include <condition_variable>

class EngineMemoryManager {
    const size_t write_buffer_size_ = 4 * 1024 * 1024; // 4MB chegara
    std::atomic<size_t> current_mem_size_{0};
    std::atomic<bool> flush_needed_{false};
    std::mutex cv_mtx_;
    std::condition_variable cv_;

public:
    bool check_and_record_write(size_t bytes_written) {
        size_t prev = current_mem_size_.fetch_add(bytes_written, std::memory_order_relaxed);
        if (prev + bytes_written >= write_buffer_size_) {
            flush_needed_.store(true, std::memory_order_release);
            cv_.notify_one();
            return true; // MemTable to'ldi, switch talab qilinadi
        }
        return false;
    }

    void wait_for_flush_request() {
        std::unique_lock<std::mutex> lock(cv_mtx_);
        cv_.wait(lock, [this] { return flush_needed_.load(std::memory_order_acquire); });
        std::cout << "[Background Thread] Flush signali qabul qilindi. SSTable yozish boshlanmoqda...\n";
        flush_needed_.store(false, std::memory_order_relaxed);
        current_mem_size_.store(0, std::memory_order_relaxed);
    }
};

int main() {
    EngineMemoryManager mgr;
    // 5MB ma'lumot yozamiz
    if (mgr.check_and_record_write(5 * 1024 * 1024)) {
        std::cout << "[Writer Thread] Write buffer to'ldi! Immutable MemTable yaratildi.\n";
    }
    mgr.wait_for_flush_request();
    return 0;
}
```
**Tushuntirish:** Ushbu mexanizm LSM-Tree ning yozish kechikishini (write latency) minimallashtiradi: asosiy oqim xotirani almashtiradi va yozishda davom etadi, sekin disk I/O esa alohida fonda bajariladi.

### Topshiriq #1205: Arena Memory Allocator: MemTable Fragmentatsiyasiz Allokatsiya
**Tavsif:** Standart `malloc`/`new` millionlab mayda tugunlar ajratilganda xotirani fragmentatsiyaga uchratadi va sekinlashadi. LSM dvigatellari yagona blokli monotonic bump allocator (Arena) dan foydalanadi.
**Talablar:** C++20, 64-baytli cache-line alignment, 4096 baytli xotira bloklari, tezkor bump pointer.
**Yechim (C++):**
```cpp
#include <iostream>
#include <vector>
#include <cstdint>
#include <cassert>

class Arena {
    char* alloc_ptr_{nullptr};
    size_t alloc_bytes_remaining_{0};
    std::vector<char*> blocks_;
    size_t memory_usage_{0};
    static constexpr size_t BLOCK_SIZE = 4096;

    char* allocate_fallback(size_t bytes) {
        if (bytes > BLOCK_SIZE / 4) {
            // Juda katta ob'ektlar uchun alohida blok
            char* mem = new char[bytes];
            blocks_.push_back(mem);
            memory_usage_ += bytes;
            return mem;
        }
        // Yangi standart blok
        alloc_ptr_ = new char[BLOCK_SIZE];
        blocks_.push_back(alloc_ptr_);
        memory_usage_ += BLOCK_SIZE;
        alloc_bytes_remaining_ = BLOCK_SIZE - bytes;
        char* result = alloc_ptr_;
        alloc_ptr_ += bytes;
        return result;
    }

public:
    Arena() = default;
    ~Arena() {
        for (char* b : blocks_) delete[] b;
    }

    char* allocate_aligned(size_t bytes) {
        constexpr size_t align = sizeof(void*);
        size_t current_mod = reinterpret_cast<uintptr_t>(alloc_ptr_) & (align - 1);
        size_t slop = (current_mod == 0) ? 0 : align - current_mod;
        size_t needed = bytes + slop;

        if (needed <= alloc_bytes_remaining_) {
            char* result = alloc_ptr_ + slop;
            alloc_ptr_ += needed;
            alloc_bytes_remaining_ -= needed;
            return result;
        }
        return allocate_fallback(bytes);
    }

    size_t total_memory() const { return memory_usage_; }
};

int main() {
    Arena arena;
    char* p1 = arena.allocate_aligned(32);
    char* p2 = arena.allocate_aligned(64);
    std::cout << "Arena xotira sarfi: " << arena.total_memory() << " bayt\n";
    std::cout << "P1 va P2 masofasi: " << (p2 - p1) << " bayt\n";
    return 0;
}
```
**Tushuntirish:** Arena yordamida ajratilgan har bir alohida tugunni `free` qilish shart emas. Butun MemTable diskka yozib bo'lingach, bitta destruktor orqali barcha bloklar bir lahzada tozalanadi.

### Topshiriq #1206: Write-Ahead Log (WAL) Record Formati va CRC32 Integrity
**Tavsif:** Xotiradagi MemTable ga kiritilgan har bir o'zgarish elektr uzilishi yoki tizim qulashida yo'qolmasligi uchun diskdagi WAL faylga yozilishi shart. Har bir WAL yozuvi sarlavhasida CRC32 tekshiruv summasi va uning turi bo'lishi kerak.
**Talablar:** C++20, RecordType: kZeroType, kFullType, kFirstType, kMiddleType, kLastType. Standart WAL frame layout.
**Yechim (C++):**
```cpp
#include <iostream>
#include <vector>
#include <string>
#include <cstdint>
#include <cstring>

enum RecordType : uint8_t {
    kZeroType = 0,
    kFullType = 1,
    kFirstType = 2,
    kMiddleType = 3,
    kLastType = 4
};

#pragma pack(push, 1)
struct WalRecordHeader {
    uint32_t checksum; // CRC-32C
    uint16_t length;   // Ma'lumot uzunligi
    uint8_t type;      // RecordType
};
#pragma pack(pop)

// Soddalashtirilgan CRC32 hisoblagich
uint32_t calculate_crc32(const uint8_t* data, size_t len) {
    uint32_t crc = 0xFFFFFFFF;
    for (size_t i = 0; i < len; ++i) {
        crc ^= data[i];
        for (int j = 0; j < 8; ++j)
            crc = (crc >> 1) ^ (0xEDB88320 & -(crc & 1));
    }
    return ~crc;
}

std::vector<uint8_t> create_wal_record(const std::string& payload) {
    WalRecordHeader hdr;
    hdr.length = static_cast<uint16_t>(payload.size());
    hdr.type = kFullType;
    hdr.checksum = calculate_crc32(reinterpret_cast<const uint8_t*>(payload.data()), payload.size());

    std::vector<uint8_t> record(sizeof(WalRecordHeader) + payload.size());
    std::memcpy(record.data(), &hdr, sizeof(hdr));
    std::memcpy(record.data() + sizeof(hdr), payload.data(), payload.size());
    return record;
}

int main() {
    auto rec = create_wal_record("PUT user:42=Olimjon");
    std::cout << "Yaratilgan WAL record hajmi: " << rec.size() << " bayt\n";
    auto* hdr = reinterpret_cast<WalRecordHeader*>(rec.data());
    std::cout << "CRC32: 0x" << std::hex << hdr->checksum << ", Len: " << std::dec << hdr->length << std::endl;
    return 0;
}
```
**Tushuntirish:** WAL jurnali bloklarga (32KB) bo'linadi. Agar yozuv blok chegarasiga sig'masa, u First, Middle, Last qismlarga bo'linadi. CRC32 yordamida diskdagi yarim yozilgan (torn-write) xatolar aniqlanadi.

### Topshiriq #1207: Group Commit va WAL Writer Sync Strategiyalari
**Tavsif:** Har bir tranzaksiyada `fsync()` chaqirish qattiq disk yoki SSD I/O tezligini sekundiga 100-200 operatsiyagacha tushirib yuboradi. Group Commit mexanizmi bir nechta parallel oqimlarning yozuvlarini birlashtirib, bitta `fsync` bilan tasdiqlaydi.
**Talablar:** C++20, `std::mutex`, `std::condition_variable`, batch processing.
**Yechim (C++):**
```cpp
#include <iostream>
#include <vector>
#include <string>
#include <mutex>
#include <condition_variable>
#include <deque>

class WalGroupCommitter {
    std::mutex mtx_;
    std::condition_variable cv_;
    std::deque<std::string> pending_writes_;
    bool is_syncing_{false};

public:
    void append_and_sync(const std::string& record) {
        std::unique_lock<std::mutex> lock(mtx_);
        pending_writes_.push_back(record);

        // Agar boshqa oqim allaqachon diskka yozayotgan bo'lsa, navbatda kutamiz
        while (is_syncing_) {
            cv_.wait(lock);
        }

        // Leader bo'lib saylanamiz
        is_syncing_ = true;
        std::vector<std::string> batch;
        while (!pending_writes_.empty()) {
            batch.push_back(std::move(pending_writes_.front()));
            pending_writes_.pop_front();
        }
        lock.unlock();

        // Diskka yagona I/O bilan yozish (fdatasync simulyatsiyasi)
        std::cout << "[GroupCommit] Batch o'lchami: " << batch.size() 
                  << " ta yozuv yagona fsync() orqali diskka muxrlandi.\n";

        lock.lock();
        is_syncing_ = false;
        cv_.notify_all(); // Barcha kutayotgan oqimlarni uyg'otish
    }
};

int main() {
    WalGroupCommitter committer;
    committer.append_and_sync("TX_1: A -> B 100$");
    return 0;
}
```
**Tushuntirish:** Group Commit yuqori yuklamada (high contention) o'tkazuvchanlikni (throughput) 10-50 baravargacha oshiradi, chunki IOPS disk apparatiga optimal yetkaziladi.

### Topshiriq #1208: WAL Crash Recovery va MemTable Qayta Tiklash
**Tavsif:** Tizim to'satdan to'xtaganda, oxirgi flush qilinmagan ma'lumotlar WAL faylida saqlanib qolgan bo'ladi. Dvigatel ishga tushganda WAL boshidan o'qilib, barcha yozuvlar MemTable ga qayta kiritilishi shart.
**Talablar:** C++20, buzilgan yoki chala yozilgan yozuvlarni aniqlash va o'tkazib yuborish.
**Yechim (C++):**
```cpp
#include <iostream>
#include <vector>
#include <sstream>
#include <stdexcept>

struct RecoveredRecord {
    uint64_t seq;
    std::string key;
    std::string val;
};

class WalRecoveryEngine {
public:
    static std::vector<RecoveredRecord> replay_log(const std::vector<uint8_t>& raw_bytes) {
        std::vector<RecoveredRecord> records;
        size_t offset = 0;

        while (offset + 7 <= raw_bytes.size()) {
            // Sarlavhani o'qish (CRC: 4, Len: 2, Type: 1)
            uint16_t len = *reinterpret_cast<const uint16_t*>(&raw_bytes[offset + 4]);
            if (offset + 7 + len > raw_bytes.size()) {
                std::cout << "[Recovery] Ogohlantirish: Oxirgi yozuv chala qolgan (Crash torn-write). Replay to'xtatildi.\n";
                break;
            }
            std::string payload(reinterpret_cast<const char*>(&raw_bytes[offset + 7]), len);
            records.push_back({1001, "key", payload});
            offset += 7 + len;
        }
        return records;
    }
};

int main() {
    // 2 ta butun va 1 ta chala yozuvli baytlar
    std::vector<uint8_t> log_data = {
        0,0,0,0, 4,0, 1, 'd','a','t','a',
        0,0,0,0, 3,0, 1, 'k','e','y',
        0,0,0,0, 10,0, 1, 'x' // Chala yozuv
    };
    auto res = WalRecoveryEngine::replay_log(log_data);
    std::cout << "Muvaffaqiyatli tiklangan yozuvlar soni: " << res.size() << std::endl;
    return 0;
}
```
**Tushuntirish:** LSM dvigateli WAL oxiridagi to'liq bo'lmagan yozuvlarni xavfsiz qirqib tashlaydi (truncate), chunki ular foydalanuvchiga `success` javobi qaytarilmagan tranzaksiyalardir.

### Topshiriq #1209: SSTable Block Builder: Delta Encoding va Restart Array
**Tavsif:** SSTable fayli ichidagi 4KB li Data Block larda kalitlar leksikografik saralangan bo'ladi. LevelDB/RocksDB qo'shni kalitlarning umumiy prefiksini siqish uchun Delta Encoding va binar qidiruv uchun Restart Array ishlatadi.
**Talablar:** C++20, har 16 ta kalitda bir marta prefiks siqishni nollash (Restart point), `shared_len`, `unshared_len`, `value_len`.
**Yechim (C++):**
```cpp
#include <iostream>
#include <string>
#include <vector>
#include <string_view>
#include <cstdint>

class BlockBuilder {
    int restart_interval_{16};
    std::string buffer_;
    std::vector<uint32_t> restarts_;
    int counter_{0};
    std::string last_key_;

public:
    BlockBuilder(int interval = 16) : restart_interval_(interval) {
        restarts_.push_back(0); // Birinchi restart nuqtasi 0-offsetda
    }

    void add(std::string_view key, std::string_view value) {
        size_t shared = 0;
        if (counter_ < restart_interval_) {
            // Umumiy prefiks uzunligini hisoblash
            const size_t min_len = std::min(last_key_.size(), key.size());
            while (shared < min_len && last_key_[shared] == key[shared]) {
                shared++;
            }
        } else {
            // Yangi restart nuqtasi
            restarts_.push_back(static_cast<uint32_t>(buffer_.size()));
            counter_ = 0;
        }

        const size_t non_shared = key.size() - shared;
        // Format: [shared_len: varint][unshared_len: varint][val_len: varint][delta_key][value]
        buffer_.push_back(static_cast<char>(shared));
        buffer_.push_back(static_cast<char>(non_shared));
        buffer_.push_back(static_cast<char>(value.size()));

        buffer_.append(key.data() + shared, non_shared);
        buffer_.append(value.data(), value.size());

        last_key_ = std::string(key);
        counter_++;
    }

    std::string finish() {
        // Blok oxiriga Restart array va uning hajmini yozish
        for (uint32_t r : restarts_) {
            buffer_.append(reinterpret_cast<const char*>(&r), sizeof(r));
        }
        uint32_t num_restarts = static_cast<uint32_t>(restarts_.size());
        buffer_.append(reinterpret_cast<const char*>(&num_restarts), sizeof(num_restarts));
        return buffer_;
    }
};

int main() {
    BlockBuilder builder(2);
    builder.add("user_profile_1001", "Toshkent");
    builder.add("user_profile_1002", "Samarqand");
    std::string block = builder.finish();
    std::cout << "Siqilgan SSTable block hajmi: " << block.size() << " bayt\n";
    return 0;
}
```
**Tushuntirish:** Delta encoding kalitlar hajmini 70-80% ga qisqartiradi. Restart nuqtalari esa butun blokni boshidan dekodlamasdan, restart offsetlar bo'yicha tezkor binar qidiruv o'tkazishga imkon beradi.

### Topshiriq #1210: SSTable Block Reader va Restart Nuqtalari Bo'yicha Binary Search
**Tavsif:** Diskdan o'qilgan 4KB li Data Block ichidan kalitni qidirishda barcha delta-yozuvlarni ketma-ket o'qish sekinlik qiladi. Binar qidiruv orqali eng yaqin Restart nuqtasi topilib, faqat bir nechta yozuv chiziqli skaner qilinadi.
**Talablar:** C++20, restart array ni oxiridan o'qish, O(log(restarts) + interval) qidiruv murakkabligi.
**Yechim (C++):**
```cpp
#include <iostream>
#include <string>
#include <string_view>
#include <vector>
#include <cstring>

class BlockReader {
    const char* data_;
    size_t size_;
    uint32_t num_restarts_;
    uint32_t restart_offset_;

public:
    BlockReader(const char* data, size_t size) : data_(data), size_(size) {
        // Oxirgi 4 bayt restart array elementlari soni
        std::memcpy(&num_restarts_, data + size - 4, 4);
        restart_offset_ = size - 4 - (num_restarts_ * 4);
    }

    uint32_t get_restart_point(uint32_t idx) const {
        uint32_t offset;
        std::memcpy(&offset, data_ + restart_offset_ + (idx * 4), 4);
        return offset;
    }

    void print_stats() const {
        std::cout << "Block hajmi: " << size_ << " bayt, Restart nuqtalari soni: " << num_restarts_ << std::endl;
    }
};

int main() {
    // Soddalashtirilgan soxta block (oxirida 2 ta restart va soni 2)
    char sample_block[16] = {0};
    uint32_t r1 = 0, r2 = 4, count = 2;
    std::memcpy(sample_block + 4, &r1, 4);
    std::memcpy(sample_block + 8, &r2, 4);
    std::memcpy(sample_block + 12, &count, 4);

    BlockReader reader(sample_block, sizeof(sample_block));
    reader.print_stats();
    return 0;
}
```
**Tushuntirish:** Ushbu arxitektura diskdagi bloklar ichida doimiy kesh-line do'stona binar qidiruvni ta'minlaydi va CPU instruksiyalarini tejaydi.

### Topshiriq #1211: SSTable Index Block va BlockHandle Offset Strukturasi
**Tavsif:** SSTable ichida qaysi Data Block da qaysi kalitlar oralig'i yotganini bilish uchun Index Block ishlatiladi. Har bir Data Block ga ko'rsatkich `BlockHandle` (fayldagi offset va hajm) orqali ifodalanadi.
**Talablar:** C++20, BlockHandle strukturasini varint formatida kodlash va dekodlash.
**Yechim (C++):**
```cpp
#include <iostream>
#include <cstdint>
#include <string>
#include <sstream>

struct BlockHandle {
    uint64_t offset{0};
    uint64_t size{0};

    std::string encode() const {
        std::string buf;
        // Soddalashtirilgan varint encoding
        buf.append(reinterpret_cast<const char*>(&offset), sizeof(offset));
        buf.append(reinterpret_cast<const char*>(&size), sizeof(size));
        return buf;
    }

    static BlockHandle decode(const char* ptr) {
        BlockHandle h;
        h.offset = *reinterpret_cast<const uint64_t*>(ptr);
        h.size = *reinterpret_cast<const uint64_t*>(ptr + sizeof(uint64_t));
        return h;
    }
};

int main() {
    BlockHandle handle{4096, 4080}; // 4096-baytdan boshlanadi, 4080 bayt hajmda
    std::string encoded = handle.encode();
    BlockHandle restored = BlockHandle::decode(encoded.data());
    std::cout << "Restored BlockHandle: Offset=" << restored.offset << ", Size=" << restored.size << " bayt\n";
    return 0;
}
```
**Tushuntirish:** Index Block har bir Data Block ning eng katta kaliti (separator) va uning BlockHandle ini saqlaydi. SSTable dan kalit izlanganda avval Index Block o'qiladi, so'ng to'g'ri Data Block ga sakraladi.

### Topshiriq #1212: SSTable Footer Tuzilmasi va Magic Number Validatsiyasi
**Tavsif:** SSTable faylining eng oxirgi 48 bayti `Footer` deb ataladi. U Index Block va Meta Block larining `BlockHandle` larini hamda LevelDB/RocksDB ga xos Magic Number ni saqlaydi.
**Talablar:** C++20, Magic Number: `0xdb4775248b80fb57ULL`, doimiy 48-bayt o'lchamli Footer.
**Yechim (C++):**
```cpp
#include <iostream>
#include <cstdint>
#include <cstring>
#include <array>

constexpr uint64_t K_SSTABLE_MAGIC_NUMBER = 0xdb4775248b80fb57ULL;
constexpr size_t FOOTER_ENCODED_LENGTH = 48;

struct Footer {
    uint64_t metaindex_offset{0};
    uint64_t metaindex_size{0};
    uint64_t index_offset{0};
    uint64_t index_size{0};

    void encode_to(char* dst) const {
        std::memset(dst, 0, FOOTER_ENCODED_LENGTH);
        std::memcpy(dst, &metaindex_offset, 8);
        std::memcpy(dst + 8, &metaindex_size, 8);
        std::memcpy(dst + 16, &index_offset, 8);
        std::memcpy(dst + 24, &index_size, 8);
        std::memcpy(dst + 40, &K_SSTABLE_MAGIC_NUMBER, 8);
    }

    static bool decode_from(const char* src, Footer* out) {
        uint64_t magic;
        std::memcpy(&magic, src + 40, 8);
        if (magic != K_SSTABLE_MAGIC_NUMBER) {
            return false; // Fayl buzilgan yoki SSTable emas
        }
        std::memcpy(&out->metaindex_offset, src, 8);
        std::memcpy(&out->metaindex_size, src + 8, 8);
        std::memcpy(&out->index_offset, src + 16, 8);
        std::memcpy(&out->index_size, src + 24, 8);
        return true;
    }
};

int main() {
    std::array<char, FOOTER_ENCODED_LENGTH> buffer;
    Footer f{1024, 128, 2048, 256};
    f.encode_to(buffer.data());

    Footer read_footer;
    if (Footer::decode_from(buffer.data(), &read_footer)) {
        std::cout << "SSTable Footer tasdiqlandi! Index Offset: " << read_footer.index_offset << std::endl;
    }
    return 0;
}
```
**Tushuntirish:** SSTable fayli ochilganda doim faylning oxirgi 48 bayti o'qiladi. Agar Magic Number to'g'ri kelsa, undan olingan Index Block orqali butun fayl indeksi xotiraga yuklanadi.

### Topshiriq #1213: Standard Bloom Filter: Xesh Funksiyalar va Bitset Manipulyatsiyasi
**Tavsif:** Agar kalit SSTable da mavjud bo'lmasa, disk bloklarini keraksiz o'qish (read amplification) oldini olish uchun Bloom Filter qo'llaniladi. U kalit yo'qligini 100% aniqlik bilan kafolatlaydi.
**Talablar:** C++20, MurmurHash uslubidagi xesh algoritmi, bitta kalit uchun K ta xesh generatsiyasi (Kirsch-Mitzenmacher texnikasi).
**Yechim (C++):**
```cpp
#include <iostream>
#include <vector>
#include <string>
#include <cstdint>

class BloomFilter {
    std::vector<uint8_t> bits_;
    size_t num_bits_;
    int k_hashes_;

    uint32_t hash1(const std::string& key) const {
        uint32_t h = 0xbc9f1d34;
        for (char c : key) h = (h * 37) + c;
        return h;
    }
    uint32_t hash2(const std::string& key) const {
        uint32_t h = 0x31415926;
        for (char c : key) h = (h * 131) ^ c;
        return h;
    }

public:
    BloomFilter(size_t num_elements, int bits_per_key = 10) {
        num_bits_ = num_elements * bits_per_key;
        if (num_bits_ < 64) num_bits_ = 64;
        bits_.resize((num_bits_ + 7) / 8, 0);
        k_hashes_ = static_cast<int>(bits_per_key * 0.69); // ln(2)
        if (k_hashes_ < 1) k_hashes_ = 1;
    }

    void add(const std::string& key) {
        uint32_t h1 = hash1(key);
        uint32_t h2 = hash2(key);
        for (int i = 0; i < k_hashes_; ++i) {
            uint32_t combined = h1 + i * h2;
            size_t bit_pos = combined % num_bits_;
            bits_[bit_pos / 8] |= (1 << (bit_pos % 8));
        }
    }

    bool may_contain(const std::string& key) const {
        uint32_t h1 = hash1(key);
        uint32_t h2 = hash2(key);
        for (int i = 0; i < k_hashes_; ++i) {
            uint32_t combined = h1 + i * h2;
            size_t bit_pos = combined % num_bits_;
            if (!(bits_[bit_pos / 8] & (1 << (bit_pos % 8)))) {
                return false; // 100% mavjud emas!
            }
        }
        return true; // Ehtimol mavjud
    }
};

int main() {
    BloomFilter filter(1000);
    filter.add("client_uuid_99");
    std::cout << "Mavjud kalit tekshiruvi: " << (filter.may_contain("client_uuid_99") ? "Ha" : "Yo'q") << std::endl;
    std::cout << "Mavjud bo'lmagan kalit tekshiruvi: " << (filter.may_contain("client_uuid_unknown") ? "Ha" : "Yo'q") << std::endl;
    return 0;
}
```
**Tushuntirish:** Bloom Filter 1 bayt/kalit nisbatida taxminan 1% false positive beradi. Bu SSTable qidiruvida disk I/O ni 99% holatda yo'qqa chiqaradi.

### Topshiriq #1214: Blocked Bloom Filter (SIMD/AVX2 Cache-Line Optimallashgan)
**Tavsif:** Standart Bloom Filter bitlari butun xotira bo'ylab tarqalib, CPU L3 keshida bir nechta miss keltirib chiqaradi. RocksDB ning Blocked Bloom Filteri har bir kalitni bitta 64-baytli kesh-liniyaga (cache-line) joylashtiradi.
**Talablar:** C++20, 512-bitli bloklar, AVX2 yoki 64-baytli tekislash (alignment).
**Yechim (C++):**
```cpp
#include <iostream>
#include <vector>
#include <cstdint>
#include <string>
#include <immintrin.h>

class BlockedBloomFilter {
    struct alignas(64) CacheLineBlock {
        uint32_t words[16]{0}; // 64 bayt = 512 bit
    };
    std::vector<CacheLineBlock> blocks_;

public:
    BlockedBloomFilter(size_t num_blocks) : blocks_(num_blocks) {}

    void add(uint64_t hash) {
        size_t block_idx = (hash >> 32) % blocks_.size();
        uint32_t h = static_cast<uint32_t>(hash);
        auto& block = blocks_[block_idx];

        // 8 ta bit o'rnatish
        for (int i = 0; i < 8; ++i) {
            uint32_t bit_idx = (h + i * 0x9e3779b9) & 511;
            block.words[bit_idx / 32] |= (1U << (bit_idx % 32));
        }
    }

    bool may_contain(uint64_t hash) const {
        size_t block_idx = (hash >> 32) % blocks_.size();
        uint32_t h = static_cast<uint32_t>(hash);
        const auto& block = blocks_[block_idx];

        for (int i = 0; i < 8; ++i) {
            uint32_t bit_idx = (h + i * 0x9e3779b9) & 511;
            if (!(block.words[bit_idx / 32] & (1U << (bit_idx % 32)))) {
                return false;
            }
        }
        return true;
    }
};

int main() {
    BlockedBloomFilter bbf(1024);
    uint64_t key_hash = 0xdeadbeefcafebabeULL;
    bbf.add(key_hash);
    std::cout << "Blocked Bloom Filter natijasi: " << (bbf.may_contain(key_hash) ? "Mavjud bo'lishi mumkin" : "Yo'q") << std::endl;
    return 0;
}
```
**Tushuntirish:** Blocked Bloom Filter har bir kalit uchun faqat 1 ta CPU kesh-liniyasini o'qiydi. Bu zamonaviy serverlarda xotira tezligini (memory bandwidth) 3-4 baravar tejaydi.

### Topshiriq #1215: SSTable Filter Block Builder va Meta-Index Integratsiyasi
**Tavsif:** SSTable yaratilayotganda har bir Data Block uchun filtrlash ma'lumotlari to'planadi va faylning Meta Block qismiga `filter.rocksdb.BuiltinBloomFilter` nomi bilan yoziladi.
**Talablar:** C++20, Filter Block offset array, Meta-Index Block ga nom va BlockHandle juftligini kiritish.
**Yechim (C++):**
```cpp
#include <iostream>
#include <string>
#include <vector>
#include <map>

class FilterBlockBuilder {
    std::vector<std::string> keys_;
    std::string filter_data_;

public:
    void add_key(const std::string& key) {
        keys_.push_back(key);
    }

    void start_block(uint64_t block_offset) {
        // Har bir 2KB yoki 4KB block uchun yangi filtr qismi
        filter_data_.append("[FilterSlice for keys: " + std::to_string(keys_.size()) + "]");
        keys_.clear();
    }

    std::string finish() {
        return filter_data_;
    }
};

int main() {
    FilterBlockBuilder fb;
    fb.add_key("k1");
    fb.add_key("k2");
    fb.start_block(0);
    std::string res = fb.finish();
    std::cout << "Yaratilgan Filter Block: " << res << std::endl;
    return 0;
}
```
**Tushuntirish:** Filter Block Data Block larga mutanosib (masalan har 2KB offsetda) indekslanadi. O'quvchi Data Block offsetini bilishi bilan aynan unga tegishli filtr segmentini tekshiradi.

### Topshiriq #1216: SSTable TableBuilder: To'liq SSTable Faylini Diskka Yozish
**Tavsif:** Immutable MemTable to'liq saralangan ma'lumotlarni o'z ichiga oladi. `TableBuilder` ushbu kalitlarni qabul qilib, ketma-ket Data Block, Filter Block, Meta Index Block, Index Block va Footer ni bitta faylga birlashtiradi.
**Talablar:** C++20, write buffer, block flusher, to'liq SSTable layout.
**Yechim (C++):**
```cpp
#include <iostream>
#include <string>
#include <vector>

class MockWritableFile {
    std::string content_;
public:
    void append(const std::string& data) { content_.append(data); }
    size_t size() const { return content_.size(); }
    const std::string& content() const { return content_; }
};

class TableBuilder {
    MockWritableFile* file_;
    uint64_t offset_{0};
    size_t num_entries_{0};

public:
    TableBuilder(MockWritableFile* f) : file_(f) {}

    void add(const std::string& key, const std::string& val) {
        std::string record = key + "=" + val + ";";
        file_->append(record);
        offset_ += record.size();
        num_entries_++;
    }

    void finish() {
        // 1. Data Blocklar tugadi
        // 2. Index Block yozamiz
        std::string index = "[INDEX_BLOCK_DATA]";
        file_->append(index);
        // 3. Footer yozamiz (48 bayt)
        std::string footer(48, 'F');
        file_->append(footer);
        std::cout << "SSTable fayli muvaffaqiyatli qurildi! Jami hajm: " << file_->size() << " bayt\n";
    }
};

int main() {
    MockWritableFile file;
    TableBuilder builder(&file);
    builder.add("user:1", "Toshkent");
    builder.add("user:2", "Buxoro");
    builder.finish();
    return 0;
}
```
**Tushuntirish:** TableBuilder to'liq append-only rejimida ishlaydi. Hech qanday orqaga qaytish (random seek) talab qilinmaydi, bu esa NVMe va HDD disklarda maksimal yozish o'tkazuvchanligini ta'minlaydi.

### Topshiriq #1217: Two-Level Iterator: Index va Data Blocklar Bo'yicha Harakatlanish
**Tavsif:** Diskdagi SSTable ni skaner qilishda `Two-Level Iterator` qo'llaniladi. Birinchi darajali iterator Index Block bo'ylab yurib kerakli Data Block ni topadi, ikkinchi darajali iterator esa o'sha blok ichidagi kalitlarni birma-bir o'qiydi.
**Talablar:** C++20, `Iterator` abstract interface: `Seek()`, `Next()`, `Valid()`, `key()`, `value()`.
**Yechim (C++):**
```cpp
#include <iostream>
#include <string>
#include <memory>
#include <vector>

class Iterator {
public:
    virtual ~Iterator() = default;
    virtual bool valid() const = 0;
    virtual void seek(const std::string& target) = 0;
    virtual void next() = 0;
    virtual std::string key() const = 0;
    virtual std::string value() const = 0;
};

class TwoLevelIterator : public Iterator {
    // Soddalashtirilgan ikki darajali iterator
    std::vector<std::pair<std::string, std::string>> sample_data_{
        {"a", "1"}, {"b", "2"}, {"c", "3"}
    };
    size_t current_idx_{0};

public:
    bool valid() const override { return current_idx_ < sample_data_.size(); }
    void seek(const std::string& target) override {
        current_idx_ = 0;
        while (current_idx_ < sample_data_.size() && sample_data_[current_idx_].first < target) {
            current_idx_++;
        }
    }
    void next() override { current_idx_++; }
    std::string key() const override { return sample_data_[current_idx_].first; }
    std::string value() const override { return sample_data_[current_idx_].second; }
};

int main() {
    TwoLevelIterator it;
    for (it.seek("b"); it.valid(); it.next()) {
        std::cout << it.key() << " -> " << it.value() << std::endl;
    }
    return 0;
}
```
**Tushuntirish:** Two-Level Iterator butun SSTable faylini xotiraga yuklamasdan, talabga binoan (lazily) 4KB bloklarni o'qiydi va disk keshi xotirasini tejaydi.

### Topshiriq #1218: MergingIterator (K-Way Merge) Min-Heap Priority Queue Bilan
**Tavsif:** LSM daraxtida bitta kalit MemTable da ham, bir nechta darajadagi SSTable fayllarida ham uchrashi mumkin. Range scan amalga oshirilganda barcha ushbu manbalar `MergingIterator` orqali yagona saralangan oqimga keltiriladi.
**Talablar:** C++20, `std::priority_queue`, K ta iterator ustida K-way merge (O(N log K)).
**Yechim (C++):**
```cpp
#include <iostream>
#include <vector>
#include <queue>
#include <string>

struct StreamEntry {
    std::string key;
    std::string value;
    size_t stream_id;

    bool operator>(const StreamEntry& other) const {
        return key > other.key; // Min-Heap uchun teskari taqqoslash
    }
};

class MergingIterator {
    std::priority_queue<StreamEntry, std::vector<StreamEntry>, std::greater<StreamEntry>> min_heap_;

public:
    void add_stream_entry(StreamEntry entry) {
        min_heap_.push(entry);
    }

    bool has_next() const { return !min_heap_.empty(); }

    StreamEntry pop_next() {
        StreamEntry top = min_heap_.top();
        min_heap_.pop();
        return top;
    }
};

int main() {
    MergingIterator merger;
    merger.add_stream_entry({"apple", "v1", 0});  // MemTable dan
    merger.add_stream_entry({"banana", "v2", 1}); // SSTable Level-0 dan
    merger.add_stream_entry({"apricot", "v3", 2});// SSTable Level-1 dan

    std::cout << "K-Way Merge natijasi:\n";
    while (merger.has_next()) {
        auto e = merger.pop_next();
        std::cout << "Key: " << e.key << ", Val: " << e.value << " (Stream: " << e.stream_id << ")\n";
    }
    return 0;
}
```
**Tushuntirish:** Min-heap yordamida K ta oqimdan eng kichik kalit O(log K) vaqtda olinadi. Agar bir xil kalit bir nechta oqimda bo'lsa, eng yangi SequenceNumber ga ega yozuv olinadi va eskilari tashlab yuboriladi.

### Topshiriq #1219: Manifest File va VersionEdit: LSM Metadata Jurnali
**Tavsif:** LSM dvigatelida doimiy yangi SSTable lar yaratiladi va eski fayllar o'chiriladi. Qaysi darajada (Level) qaysi fayllar mavjudligini xavfsiz saqlash uchun `MANIFEST` fayliga `VersionEdit` tranzaksiyalari yoziladi.
**Talablar:** C++20, qo'shilgan fayllar (`added_files`) va o'chirilgan fayllar (`deleted_files`) ro'yxatini atomik saqlash.
**Yechim (C++):**
```cpp
#include <iostream>
#include <vector>
#include <string>
#include <cstdint>

struct FileMetaData {
    uint64_t file_number;
    uint64_t file_size;
    std::string smallest_key;
    std::string largest_key;
};

class VersionEdit {
public:
    int level_{-1};
    std::vector<std::pair<int, uint64_t>> deleted_files_; // {level, file_num}
    std::vector<std::pair<int, FileMetaData>> new_files_;  // {level, metadata}

    void add_file(int level, uint64_t num, uint64_t size, const std::string& smallest, const std::string& largest) {
        new_files_.push_back({level, {num, size, smallest, largest}});
    }

    void delete_file(int level, uint64_t num) {
        deleted_files_.push_back({level, num});
    }

    void print_manifest_entry() const {
        std::cout << "[VersionEdit] O'chirildi: " << deleted_files_.size() 
                  << " ta fayl, Yangi qo'shildi: " << new_files_.size() << " ta SSTable.\n";
    }
};

int main() {
    VersionEdit edit;
    edit.delete_file(0, 105); // Level 0 dan 105-fayl o'chirildi
    edit.add_file(1, 108, 4194304, "order:100", "order:500"); // Level 1 ga 108-fayl qo'shildi
    edit.print_manifest_entry();
    return 0;
}
```
**Tushuntirish:** MANIFEST jurnali LSM-Tree ning o'ziga xos WAL faylidir. Tizim qayta ishga tushganda oxirgi barqaror daraxt holati MANIFEST orqali tiklanadi.

### Topshiriq #1220: VersionSet va Snapshot Isolation (Reference Counting)
**Tavsif:** Foydalanuvchi ma'lumotlar bazasidan Snapshot olganida, fondagi Compaction eski fayllarni jismonan o'chirib yubormasligi kerak. Bu `Version` ob'ektlarini `std::shared_ptr` yoki `ref_count` orqali boshqarish bilan hal qilinadi.
**Talablar:** C++20, atomik reference counting, dangling pointerlarsiz xavfsiz fayl tozalash.
**Yechim (C++):**
```cpp
#include <iostream>
#include <atomic>
#include <vector>

class Version {
    std::atomic<int> refs_{0};
public:
    int version_id{0};

    void ref() { refs_.fetch_add(1, std::memory_order_relaxed); }
    void unref() {
        if (refs_.fetch_sub(1, std::memory_order_acq_rel) == 1) {
            std::cout << "[Version " << version_id << "] Barcha snapshotlar tugadi. Resurslar tozalandi.\n";
            delete this;
        }
    }
};

int main() {
    Version* v1 = new Version();
    v1->version_id = 1;
    v1->ref(); // Asosiy dvigatel ushlab turibdi

    // Foydalanuvchi snapshot oldi
    v1->ref(); // Snapshot ushlab turibdi

    // Dvigatel yangi versiyaga o'tdi
    v1->unref();
    std::cout << "Dvigatel yangi versiyaga o'tdi, lekin snapshot hali ochiq.\n";

    // Snapshot o'qib bo'lindi
    v1->unref();
    return 0;
}
```
**Tushuntirish:** Snapshot Isolation yordamida o'quvchi oqimlar eski ma'lumotlar holatini xotirjam ko'raveradi, fondagi Compaction esa ularning ishlashiga xalal bermaydi.

### Topshiriq #1221: Minor Compaction: Immutable MemTable ni Level-0 SSTable ga Flush Qilish
**Tavsif:** Xotiradagi Immutable MemTable to'liq saralangan holatda bo'ladi. Minor Compaction jarayoni hech qanday boshqa fayllarni o'qimasdan, MemTable dagi ma'lumotlarni to'g'ridan-to'g'ri Level-0 SSTable qilib diskka tushiradi.
**Talablar:** C++20, diskka navbatdagi `file_number` bilan `.sst` yaratish va VersionEdit ni e'lon qilish.
**Yechim (C++):**
```cpp
#include <iostream>
#include <string>
#include <vector>

class MinorCompactor {
public:
    static void flush_memtable(uint64_t new_file_num, const std::vector<std::string>& memtable_keys) {
        std::cout << "[MinorCompaction] Fayl #" << new_file_num << ".sst Level-0 ga yozilmoqda. Kalitlar soni: " 
                  << memtable_keys.size() << std::endl;
        std::cout << "[MinorCompaction] Diapazon: [" << memtable_keys.front() 
                  << " ... " << memtable_keys.back() << "]\n";
    }
};

int main() {
    std::vector<std::string> keys = {"cust:1", "cust:2", "cust:3"};
    MinorCompactor::flush_memtable(42, keys);
    return 0;
}
```
**Tushuntirish:** Minor Compaction juda tez bajariladi, chunki CPU faqat xotiradan diskka ketma-ket yozadi. Shu sababli Level-0 dagi fayllar kalitlari bir-biri bilan kesishishi (overlap) mumkin.

### Topshiriq #1222: Leveled Compaction Score Hisoblash va Priority Tanlash
**Tavsif:** LSM-Tree da Level 1 dan boshlab har bir daraja oldingisidan 10 barobar katta hajmga ega bo'ladi (L1: 10MB, L2: 100MB, L3: 1GB). Qaysi daraja o'z limitidan oshib ketgan bo'lsa, uning `compaction_score` ko'rsatkichi eng yuqori bo'ladi va navbatdagi tozalashga tanlanadi.
**Talablar:** C++20, har bir daraja uchun `score = current_bytes / max_bytes` hisoblash.
**Yechim (C++):**
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

struct LevelScore {
    int level;
    double score;
};

class CompactionPicker {
    std::vector<uint64_t> max_bytes_per_level_{
        10 * 1024 * 1024,      // L1: 10 MB
        100 * 1024 * 1024,     // L2: 100 MB
        1000 * 1024 * 1024     // L3: 1 GB
    };

public:
    int pick_compaction_level(const std::vector<uint64_t>& current_bytes) {
        int best_level = -1;
        double best_score = 1.0; // 1.0 dan oshsa compaction zarur

        for (size_t lvl = 0; lvl < current_bytes.size(); ++lvl) {
            double score = static_cast<double>(current_bytes[lvl]) / max_bytes_per_level_[lvl];
            std::cout << "Level " << (lvl + 1) << " Score: " << score << "\n";
            if (score > best_score) {
                best_score = score;
                best_level = lvl + 1;
            }
        }
        return best_level;
    }
};

int main() {
    CompactionPicker picker;
    // L1: 15MB (limit 10MB), L2: 80MB (limit 100MB)
    std::vector<uint64_t> current = {15 * 1024 * 1024, 80 * 1024 * 1024};
    int chosen = picker.pick_compaction_level(current);
    std::cout << "Compaction uchun tanlangan daraja: Level " << chosen << std::endl;
    return 0;
}
```
**Tushuntirish:** Score 1.0 dan katta bo'lishi darajada ortiqcha fayllar to'planganini va disk o'qish kechikishi (read amplification) ortib ketayotganini bildiradi.

### Topshiriq #1223: Leveled Compaction Jarayoni: Level N va N+1 Fayllarini Birlashtirish
**Tavsif:** Tanlangan Level N dagi bitta SSTable va u bilan kalitlar diapazoni kesishgan (overlapping) Level N+1 dagi barcha fayllar ochiladi, MergingIterator orqali saralanadi va Level N+1 uchun yangi SSTable lar yoziladi.
**Talablar:** C++20, ikki daraja fayllarini k-way merge qilish va eski fayllarni MANIFEST da o'chirish.
**Yechim (C++):**
```cpp
#include <iostream>
#include <vector>
#include <string>

void execute_compaction(int src_level, const std::vector<std::string>& src_keys,
                        const std::vector<std::string>& dst_keys) {
    std::cout << "[Compaction] Level " << src_level << " va Level " << (src_level + 1) << " birlashtirilmoqda...\n";
    std::vector<std::string> merged;
    size_t i = 0, j = 0;
    while (i < src_keys.size() && j < dst_keys.size()) {
        if (src_keys[i] <= dst_keys[j]) {
            merged.push_back(src_keys[i++]);
        } else {
            merged.push_back(dst_keys[j++]);
        }
    }
    while (i < src_keys.size()) merged.push_back(src_keys[i++]);
    while (j < dst_keys.size()) merged.push_back(dst_keys[j++]);

    std::cout << "[Compaction] Yangi Level " << (src_level + 1) << " SSTable yozildi. Jami kalitlar: " 
              << merged.size() << std::endl;
}

int main() {
    execute_compaction(1, {"a", "c", "e"}, {"b", "d", "f"});
    return 0;
}
```
**Tushuntirish:** Leveled Compaction Level 1 va undan yuqori darajalarda har bir faylning kalitlar diapazoni mutlaqo kesishmasligini (non-overlapping) kafolatlaydi. Shu sababli yuqori darajalarda kalitni qidirish bitta faylga to'g'ri keladi.

### Topshiriq #1224: Compaction Paytida Eskirgan Versiyalar va Tombstone larni Tozalash (MVCC GC)
**Tavsif:** Foydalanuvchi bir kalitni 10 marta yangilagan yoki o'chirgan bo'lsa, oraliq eski qiymatlar diskda joy egallab yotadi. Compaction paytida snapshotlardan eski bo'lgan ortiqcha versiyalar va tombstonelar jismonan yo'q qilinadi.
**Talablar:** C++20, `earliest_snapshot_seq` dan kichik bo'lgan eski versiyalarni filtrlash.
**Yechim (C++):**
```cpp
#include <iostream>
#include <vector>
#include <string>
#include <cstdint>

struct KeyVersion {
    std::string user_key;
    uint64_t seq;
    bool is_deleted;
    std::string value;
};

std::vector<KeyVersion> garbage_collect_versions(const std::vector<KeyVersion>& raw_input, uint64_t earliest_snapshot) {
    std::vector<KeyVersion> result;
    std::string last_seen_key = "";

    for (const auto& item : raw_input) {
        if (item.user_key != last_seen_key) {
            // Yangi kalitning eng so'nggi versiyasi
            last_seen_key = item.user_key;
            if (!item.is_deleted) {
                result.push_back(item);
            }
        } else {
            // Shu kalitning eski versiyasi
            if (item.seq >= earliest_snapshot) {
                // Hali ochiq snapshot ko'rishi kerak
                result.push_back(item);
            } else {
                std::cout << "[GC] Ortiqcha eski versiya tozalandi: " << item.user_key << " (Seq: " << item.seq << ")\n";
            }
        }
    }
    return result;
}

int main() {
    std::vector<KeyVersion> history = {
        {"user:1", 200, false, "Yangi_Manzil"},
        {"user:1", 150, false, "O'rta_Manzil"},
        {"user:1", 90,  false, "Eski_Manzil"}
    };
    uint64_t active_snapshot = 100;
    auto clean = garbage_collect_versions(history, active_snapshot);
    std::cout << "Qolgan versiyalar soni: " << clean.size() << std::endl;
    return 0;
}
```
**Tushuntirish:** Ushbu jarayon disk hajmini (space amplification) va kesh yuklamasini kamaytiradi. Tombstone ham eng quyi darajaga (masalan eng oxirgi Level ga) yetganda to'liq yo'q qilinadi.

### Topshiriq #1225: Block Cache (Sharded LRU Cache) Disk I/O ni Minimallashtirish
**Tavsif:** Diskdagi 4KB SSTable bloklarini takroriy o'qishni yo'qotish uchun xotirada Block Cache saqlanadi. Ko'p oqimli muhitda lock contention ni kamaytirish uchun kesh 16 ta mustaqil shardlarga bo'linadi.
**Talablar:** C++20, sharding (hash % 16), ikki tomonlama bog'langan ro'yxat (doubly linked list) va hash xarita orqali O(1) LRU eviction.
**Yechim (C++):**
```cpp
#include <iostream>
#include <list>
#include <unordered_map>
#include <mutex>
#include <string>
#include <memory>

class LRUCacheShard {
    size_t capacity_;
    std::list<std::pair<std::string, std::string>> lru_list_;
    std::unordered_map<std::string, decltype(lru_list_.begin())> table_;
    std::mutex mtx_;

public:
    LRUCacheShard(size_t cap = 100) : capacity_(cap) {}

    void insert(const std::string& key, const std::string& block_data) {
        std::lock_guard<std::mutex> lock(mtx_);
        auto it = table_.find(key);
        if (it != table_.end()) {
            lru_list_.erase(it->second);
        } else if (table_.size() >= capacity_) {
            auto last = lru_list_.end();
            --last;
            table_.erase(last->first);
            lru_list_.pop_back();
        }
        lru_list_.push_front({key, block_data});
        table_[key] = lru_list_.begin();
    }

    bool lookup(const std::string& key, std::string* out) {
        std::lock_guard<std::mutex> lock(mtx_);
        auto it = table_.find(key);
        if (it == table_.end()) return false;
        lru_list_.splice(lru_list_.begin(), lru_list_, it->second);
        *out = it->second->second;
        return true;
    }
};

int main() {
    LRUCacheShard cache(2);
    cache.insert("sst_1_blk_0", "DATA_BLOCK_0_BYTES");
    cache.insert("sst_1_blk_1", "DATA_BLOCK_1_BYTES");
    std::string res;
    if (cache.lookup("sst_1_blk_0", &res)) {
        std::cout << "Keshdan topildi: " << res << std::endl;
    }
    return 0;
}
```
**Tushuntirish:** Sharded LRU Cache yordamida yuzlab oqimlar turli shardlarga murojaat qilganda bir-birining yo'lini to'smaydi, bu esa millionlab IOPS ko'rsatkichiga erishish imkonini beradi.

### Topshiriq #1226: Row Cache (RocksDB Uslubida): Deserializatsiya Qilingan Yozuvlar Keshi
**Tavsif:** Block Cache 4KB siqilgan bloklarni saqlaydi, bu esa har bir o'qishda blokni ochish va binar qidiruvni talab qiladi. Row Cache esa to'g'ridan-to'g'ri kalit-qiymat juftligini CPU xotirasida saqlab, blok dekompressiyasini to'liq chetlab o'tadi.
**Talablar:** C++20, `std::unordered_map`, point-lookup da Block Cache dan oldin tekshirish, kesh invalidatsiyasi.
**Yechim (C++):**
```cpp
#include <iostream>
#include <unordered_map>
#include <string>
#include <optional>
#include <mutex>

class RowCache {
    std::unordered_map<std::string, std::string> cache_;
    std::mutex mtx_;

public:
    void put(const std::string& key, const std::string& val) {
        std::lock_guard<std::mutex> lock(mtx_);
        cache_[key] = val;
    }

    void invalidate(const std::string& key) {
        std::lock_guard<std::mutex> lock(mtx_);
        cache_.erase(key);
    }

    std::optional<std::string> get(const std::string& key) {
        std::lock_guard<std::mutex> lock(mtx_);
        auto it = cache_.find(key);
        if (it != cache_.end()) return it->second;
        return std::nullopt;
    }
};

int main() {
    RowCache rc;
    rc.put("user:account:42", "{"name":"Temur","status":"active"}");
    auto hit = rc.get("user:account:42");
    if (hit) {
        std::cout << "[RowCache HIT]: " << *hit << std::endl;
    }
    return 0;
}
```
**Tushuntirish:** Row Cache juda tez (sub-mikrosekund) javob beradi. Lekin har qanday `Put` yoki `Delete` operatsiyasi tegishli kalitni Row Cache dan zudlik bilan o'chirishi (invalidate) shart.

### Topshiriq #1227: MVCC Sequence Number Bit-Packing va InternalKey Tuzilmasi
**Tavsif:** RocksDB har bir foydalanuvchi kalitining oxiriga 8 baytli qiymat ulaydi: 56 bit SequenceNumber va 8 bit ValueType (Put, Delete, Merge). Bu kalitlarni vaqt bo'yicha tartiblash imkonini beradi.
**Talablar:** C++20, bitwise operations (`seq << 8 | type`), leksikografik taqqoslash.
**Yechim (C++):**
```cpp
#include <iostream>
#include <string>
#include <cstdint>
#include <cstring>

enum class ValueType : uint8_t {
    kTypeDeletion = 0,
    kTypeValue = 1
};

struct InternalKey {
    std::string user_key;
    uint64_t sequence_number;
    ValueType type;

    std::string encode() const {
        std::string res = user_key;
        uint64_t tag = (sequence_number << 8) | static_cast<uint8_t>(type);
        res.append(reinterpret_cast<const char*>(&tag), 8);
        return res;
    }

    static InternalKey decode(const std::string& raw) {
        InternalKey ik;
        ik.user_key = raw.substr(0, raw.size() - 8);
        uint64_t tag;
        std::memcpy(&tag, raw.data() + raw.size() - 8, 8);
        ik.sequence_number = tag >> 8;
        ik.type = static_cast<ValueType>(tag & 0xFF);
        return ik;
    }
};

int main() {
    InternalKey ik{"invoice:501", 10425, ValueType::kTypeValue};
    std::string wire = ik.encode();
    auto decoded = InternalKey::decode(wire);
    std::cout << "UserKey: " << decoded.user_key 
              << ", Seq: " << decoded.sequence_number 
              << ", Type: " << (decoded.type == ValueType::kTypeValue ? "Value" : "Delete") << std::endl;
    return 0;
}
```
**Tushuntirish:** InternalKey saralash komparatori user_key bo'yicha o'sish tartibida, bir xil kalit uchun esa sequence_number bo'yicha kamayish tartibida saralaydi. Natijada eng yangi yozuv doim birinchi chiqadi.

### Topshiriq #1228: MVCC Snapshot Qidiruvi: Eng So'nggi Ko'rinadigan Versiyani Topish
**Tavsif:** Tranzaksiya boshlanganda u joriy `snapshot_seq` ni oladi. LSM daraxti ichidan qidirilganda, faqat `seq <= snapshot_seq` shartini qanoatlantiruvchi birinchi yozuv qaytariladi, yangiroq o'zgarishlar esa ko'rinmaydi.
**Talablar:** C++20, MVCC ko'rinish filtri, Phantom read va Non-repeatable read muammolarining oldini olish.
**Yechim (C++):**
```cpp
#include <iostream>
#include <vector>
#include <string>
#include <optional>

struct VersionedRecord {
    std::string key;
    uint64_t seq;
    bool is_deleted;
    std::string val;
};

std::optional<std::string> mvcc_point_lookup(
    const std::vector<VersionedRecord>& records,
    const std::string& target_key,
    uint64_t snapshot_seq) 
{
    // Yozuvlar seq bo'yicha kamayish tartibida saralangan deb hisoblaymiz
    for (const auto& rec : records) {
        if (rec.key == target_key && rec.seq <= snapshot_seq) {
            if (rec.is_deleted) return std::nullopt; // O'chirilgan
            return rec.val; // Ushbu snapshot ko'rishi mumkin bo'lgan eng yangi qiymat
        }
    }
    return std::nullopt;
}

int main() {
    std::vector<VersionedRecord> history = {
        {"item:X", 300, false, "Narx_300"},
        {"item:X", 200, false, "Narx_200"},
        {"item:X", 100, false, "Narx_100"}
    };

    uint64_t tx_snapshot = 250; // Tranzaksiya 250-vaqtda boshlangan
    auto res = mvcc_point_lookup(history, "item:X", tx_snapshot);
    if (res) {
        std::cout << "Snapshot (" << tx_snapshot << ") ko'rgan qiymat: " << *res << std::endl;
    }
    return 0;
}
```
**Tushuntirish:** Snapshot Isolation hech qanday o'qish qulfisiz (read locks) to'liq tranzaksion konsistentlikni ta'minlaydi.

### Topshiriq #1229: WriteBatch Implementatsiyasi: Atomik Ko'p Qirrali Yozish
**Tavsif:** Bitta tranzaksiyada bir nechta kalitlarni birgalikda yozish yoki o'chirish kerak bo'lganda `WriteBatch` qo'llaniladi. U barcha o'zgarishlarni bitta baytli buferga yig'ib, WAL ga atomik bitta I/O bilan yozadi.
**Talablar:** C++20, count (yozuvlar soni), baytlar serializatsiyasi, `put()` va `delete_key()` metodlari.
**Yechim (C++):**
```cpp
#include <iostream>
#include <string>
#include <vector>
#include <cstdint>

class WriteBatch {
    std::string rep_;
    uint32_t count_{0};

public:
    WriteBatch() {
        rep_.resize(12, 0); // 8 bayt seq, 4 bayt count
    }

    void put(const std::string& key, const std::string& val) {
        rep_.push_back(1); // 1 = Put
        uint32_t klen = key.size();
        uint32_t vlen = val.size();
        rep_.append(reinterpret_cast<const char*>(&klen), 4);
        rep_.append(key);
        rep_.append(reinterpret_cast<const char*>(&vlen), 4);
        rep_.append(val);
        count_++;
    }

    void delete_key(const std::string& key) {
        rep_.push_back(0); // 0 = Delete
        uint32_t klen = key.size();
        rep_.append(reinterpret_cast<const char*>(&klen), 4);
        rep_.append(key);
        count_++;
    }

    uint32_t count() const { return count_; }
    size_t byte_size() const { return rep_.size(); }
};

int main() {
    WriteBatch batch;
    batch.put("acc:from", "900$");
    batch.put("acc:to", "1100$");
    std::cout << "Batch elementlari: " << batch.count() << ", hajmi: " << batch.byte_size() << " bayt\n";
    return 0;
}
```
**Tushuntirish:** WriteBatch butunlay yoki umuman yozilmaslik (atomicity) tamoyilini kafolatlaydi. Agar yozish vaqtida tizim qulasa, chala batch WAL orqali rad etiladi.

### Topshiriq #1230: RocksDB Pipelined Write va JoinBatchGroup Mexanizmi
**Tavsif:** Yuzlab oqimlar bir vaqtda yozmoqchi bo'lganda, ularning barchasi WAL mutexi ustida urishishi (contention) tizimni sekinlashtiradi. RocksDB birinchi kelgan oqimni Leader qilib tayinlaydi va boshqa oqimlarning batchlarini bitta guruhga birlashtiradi.
**Talablar:** C++20, `std::atomic`, oqimlararo navbat va Leader-Follower yozish shakli.
**Yechim (C++):**
```cpp
#include <iostream>
#include <atomic>
#include <vector>
#include <thread>
#include <mutex>
#include <condition_variable>

struct Writer {
    int id;
    bool done{false};
    Writer* next{nullptr};
};

class WriteThreadCoordinator {
    std::atomic<Writer*> newest_writer_{nullptr};
    std::mutex mtx_;
    std::condition_variable cv_;

public:
    void join_batch_group(Writer* w) {
        w->next = newest_writer_.load(std::memory_order_relaxed);
        while (!newest_writer_.compare_exchange_weak(w->next, w, std::memory_order_release, std::memory_order_relaxed));

        if (w->next == nullptr) {
            // Ushbu oqim Leader bo'ldi!
            std::cout << "[Leader] Oqim #" << w->id << " guruh yozishini boshqarmoqda.\n";
            // Barcha qo'shilgan Follower larni diskka yozadi va ularni uyg'otadi
        } else {
            // Follower - natijani kutadi
            std::cout << "[Follower] Oqim #" << w->id << " Leader ga qo'shildi.\n";
        }
    }
};

int main() {
    WriteThreadCoordinator coord;
    Writer w1{1}, w2{2};
    coord.join_batch_group(&w1);
    coord.join_batch_group(&w2);
    return 0;
}
```
**Tushuntirish:** Pipelined Write CPU yadrolari o'rtasidagi kesh-chiziq almashinuvini (cache-line bouncing) keskin qisqartiradi va 100+ oqimli serverlarda o'tkazuvchanlikni saqlab qoladi.

### Topshiriq #1231: Concurrent B+Tree Node Tuzilmasi: Internal va Leaf Node
**Tavsif:** LSM-Tree bilan bir qatorda B+Tree zamonaviy relyatsion va kesh dvigatellarining (InnoDb, WiredTiger) asosiy indeksi hisoblanadi. B+Tree da ma'lumotlar faqat Leaf nodelarda saqlanadi, Internal nodelar esa faqat yo'naltiruvchi kalitlarni tutadi.
**Talablar:** C++20, `is_leaf` bayrog'i, `keys` massivi, `pointers/values` massivi, `next_sibling` ko'rsatkichi.
**Yechim (C++):**
```cpp
#include <iostream>
#include <vector>
#include <shared_mutex>
#include <memory>

template <typename Key, typename Value, int ORDER = 4>
struct BPlusTreeNode {
    bool is_leaf{false};
    int num_keys{0};
    Key keys[ORDER];
    
    // Internal node uchun bolalar ko'rsatkichlari, Leaf node uchun qiymatlar
    union {
        BPlusTreeNode* children[ORDER + 1];
        Value values[ORDER];
    };
    
    BPlusTreeNode* next_leaf{nullptr}; // Range scan uchun faqat leafda
    mutable std::shared_mutex rw_latch; // Concurrency uchun Read/Write latch

    BPlusTreeNode(bool leaf) : is_leaf(leaf) {
        if (!is_leaf) {
            for (int i = 0; i <= ORDER; ++i) children[i] = nullptr;
        }
    }
};

int main() {
    auto leaf = std::make_unique<BPlusTreeNode<int, std::string>>(true);
    leaf->keys[0] = 100;
    leaf->values[0] = "Mahsulot_A";
    leaf->num_keys = 1;
    std::cout << "B+Tree Leaf Node yaratildi. Kalit: " << leaf->keys[0] << ", Qiymat: " << leaf->values[0] << std::endl;
    return 0;
}
```
**Tushuntirish:** Leaf nodelarning `next_leaf` zanjiri bo'ylab bog'lanishi range scan (BETWEEN x AND y) so'rovlarini daraxt ildiziga qaytmasdan chiziqli tezlikda bajarishga imkon beradi.

### Topshiriq #1232: B+Tree Leaf Node Search va Split Operatsiyasi
**Tavsif:** Leaf tuguniga yangi kalit qo'shilayotganda, agar tugun to'lib qolgan bo'lsa (N == ORDER), u teng ikkiga bo'linadi (split). Kalitlarning yarmi yangi qo'shni tugunga o'tadi va o'rtadagi kalit ota tugunga uzatiladi.
**Talablar:** C++20, saralangan holda kiritish, split qilish va `next_leaf` ko'rsatkichini ulash.
**Yechim (C++):**
```cpp
#include <iostream>
#include <algorithm>

constexpr int DEGREE = 4;

struct LeafNode {
    int keys[DEGREE]{0};
    int count{0};
    LeafNode* next{nullptr};

    void insert_non_full(int key) {
        int i = count - 1;
        while (i >= 0 && keys[i] > key) {
            keys[i + 1] = keys[i];
            i--;
        }
        keys[i + 1] = key;
        count++;
    }

    LeafNode* split(int& parent_key) {
        LeafNode* sibling = new LeafNode();
        int mid = count / 2;
        parent_key = keys[mid];

        sibling->count = count - mid;
        for (int i = mid; i < count; ++i) {
            sibling->keys[i - mid] = keys[i];
        }
        count = mid;

        sibling->next = this->next;
        this->next = sibling;
        return sibling;
    }
};

int main() {
    LeafNode node;
    node.insert_non_full(10);
    node.insert_non_full(20);
    node.insert_non_full(30);
    node.insert_non_full(40);

    int promoted_key = 0;
    LeafNode* new_leaf = node.split(promoted_key);
    std::cout << "Split bajarildi! Promoted Key: " << promoted_key << "\n";
    std::cout << "Original Node count: " << node.count << ", Yangi Sibling count: " << new_leaf->count << std::endl;
    delete new_leaf;
    return 0;
}
```
**Tushuntirish:** B+Tree barcha barglarini bir xil balandlikda (balanced) saqlaydi. Split operatsiyasi doimiy O(log N) vaqt murakkabligini kafolatlaydi.

### Topshiriq #1233: B+Tree Internal Node Insert va Rekursiv Parent Split
**Tavsif:** Leaf node bo'lingandan so'ng chiqqan o'rta kalit ota (Internal) tugunga kiritiladi. Agar ota tugun ham to'lgan bo'lsa, split rekursiv ravishda daraxt ildizigacha (root) ko'tariladi.
**Talablar:** C++20, Internal node splitting, child pointerlarni to'g'ri qayta taqsimlash.
**Yechim (C++):**
```cpp
#include <iostream>
#include <vector>

struct InternalNode {
    std::vector<int> keys;
    std::vector<void*> children;

    void insert_child(int key, void* child) {
        auto it = std::lower_bound(keys.begin(), keys.end(), key);
        int idx = std::distance(keys.begin(), it);
        keys.insert(it, key);
        children.insert(children.begin() + idx + 1, child);
    }
};

int main() {
    InternalNode inode;
    inode.children.push_back((void*)0x1); // 0-child
    inode.insert_child(50, (void*)0x2);
    inode.insert_child(25, (void*)0x3);

    std::cout << "Internal node kalitlari soni: " << inode.keys.size() 
              << ", bolalar soni: " << inode.children.size() << std::endl;
    return 0;
}
```
**Tushuntirish:** Agar ildiz tugun bo'linsa, yangi ildiz tugun yaratiladi va uning ikkita bolasi bo'ladi. Bu butun B+Tree balandligi 1 ga oshadigan yagona holatdir.

### Topshiriq #1234: B+Tree Concurrent Latch Crabbing (Coupling) Read Protokoli
**Tavsif:** Bir nechta oqim daraxt bo'ylab harakatlanganda poyga holati (race condition) yuz bermasligi uchun Latch Crabbing ishlatiladi. O'qishda bola tugunning Shared Latchi olingandan keyingina ota tugunning latchi bo'shatiladi.
**Talablar:** C++20, `std::shared_lock`, zanjirli latch olish va chiqarish.
**Yechim (C++):**
```cpp
#include <iostream>
#include <shared_mutex>
#include <memory>

struct CrabbingNode {
    int key_val{0};
    CrabbingNode* child{nullptr};
    std::shared_mutex latch;
};

void concurrent_search(CrabbingNode* root, int target) {
    // 1. Root latchini olamiz
    root->latch.lock_shared();
    std::cout << "[Latch Crab] Root Read-Latch olindi.\n";
    CrabbingNode* curr = root;

    while (curr->child != nullptr) {
        CrabbingNode* next = curr->child;
        // Bolaning latchini olamiz
        next->latch.lock_shared();
        std::cout << "[Latch Crab] Bola Read-Latch olindi.\n";

        // Otani bo'shatamiz
        curr->latch.unlock_shared();
        std::cout << "[Latch Crab] Ota Read-Latch bo'shatildi.\n";
        curr = next;
    }

    std::cout << "[Latch Crab] Leafga yetib keldik. Qiymat o'qilmoqda...\n";
    curr->latch.unlock_shared();
}

int main() {
    CrabbingNode leaf{100, nullptr};
    CrabbingNode root{50, &leaf};
    concurrent_search(&root, 100);
    return 0;
}
```
**Tushuntirish:** Latch coupling hech qachon bir vaqtning o'zida ikkitadan ortiq tugunni ushlab turmaydi. Bu orqali yuqori darajadagi ota tugunlar darhol boshqa parallel oqimlar uchun bo'shatiladi.

### Topshiriq #1235: Optimistic Lock Coupling: O'qishda Read Locksiz B+Tree Traversing
**Tavsif:** Katta serverlarda hatto Shared Latch (Read Latch) olish ham CPU kesh liniyalarida ziddiyat keltirib chiqaradi. Optimistic Lock Coupling da har bir tugun atomik versiya raqamiga ega bo'ladi; o'quvchi latch olmaydi, faqat versiyani tekshiradi.
**Talablar:** C++20, `std::atomic<uint64_t> version_`, validate tekshiruvi, poyga aniqlanganda qayta urinish (retry).
**Yechim (C++):**
```cpp
#include <iostream>
#include <atomic>

struct OptNode {
    std::atomic<uint64_t> version{0};
    int key{0};
    int value{0};

    bool is_locked(uint64_t v) const { return (v & 1) != 0; }

    uint64_t read_lock_optimistic() const {
        while (true) {
            uint64_t v = version.load(std::memory_order_acquire);
            if (!is_locked(v)) return v;
            // Qulflangan bo'lsa kutamiz
        }
    }

    bool validate(uint64_t v) const {
        return version.load(std::memory_order_acquire) == v;
    }
};

int main() {
    OptNode node;
    node.key = 42;
    node.value = 1000;

    // Optimistik o'qish
    uint64_t v = node.read_lock_optimistic();
    int read_val = node.value; // Hech qanday mutexsiz to'g'ridan to'g'ri o'qish
    if (node.validate(v)) {
        std::cout << "Optimistik o'qish muvaffaqiyatli: " << read_val << std::endl;
    } else {
        std::cout << "Poyga yuz berdi, qayta urinish kerak!\n";
    }
    return 0;
}
```
**Tushuntirish:** Optimistic Lock Coupling zamonaviy xotiradagi indekslarda (masalan, LeanStore, HyPer) o'qish tezligini sof bitta oqimli tezlik darajasiga olib chiqadi.

### Topshiriq #1236: B+Tree Exclusive Write Latch Crabbing va Xavfsiz Tugun Bo'shatish
**Tavsif:** Yozish (Insert/Delete) paytida bola tugun to'lib ketgan bo'lsa, u bo'linishi mumkin. Agar bola xavfsiz bo'lsa (to'lmagan bo'lsa), ota tugunning barcha yuqori qulflari darhol bo'shatiladi.
**Talablar:** C++20, Exclusive lock chaining, safe node aniqlash (`count < DEGREE - 1`).
**Yechim (C++):**
```cpp
#include <iostream>
#include <mutex>
#include <vector>

struct SafeCrabNode {
    int count{0};
    int max_capacity{4};
    std::unique_ptr<std::mutex> mtx{std::make_unique<std::mutex>()};

    bool is_safe_for_insert() const {
        return count < max_capacity;
    }
};

void insert_latch_crabbing(std::vector<SafeCrabNode*>& path) {
    std::vector<SafeCrabNode*> locked_ancestors;
    for (auto* node : path) {
        node->mtx->lock();
        if (node->is_safe_for_insert()) {
            // Ushbu tugun xavfsiz, demak uning otalarida split yuz bermaydi!
            for (auto* ancestor : locked_ancestors) {
                ancestor->mtx->unlock();
            }
            locked_ancestors.clear();
        }
        locked_ancestors.push_back(node);
    }
    std::cout << "Eng pastki tugunga yetdik. Qulflangan ajdodlar soni: " << locked_ancestors.size() << "\n";
    for (auto* n : locked_ancestors) n->mtx->unlock();
}

int main() {
    SafeCrabNode root{2, 4}; // Xavfsiz
    SafeCrabNode leaf{4, 4}; // To'lgan (xavfsiz emas)
    std::vector<SafeCrabNode*> path = {&root, &leaf};
    insert_latch_crabbing(path);
    return 0;
}
```
**Tushuntirish:** B+Tree yozishlarida 95% dan ortiq holatlarda barg tugun xavfsiz bo'ladi yoki uning bevosita otasi xavfsiz bo'ladi. Shu sababli ildiz tuguni faqat 1-2 operatsiyaga ushlab turiladi.

### Topshiriq #1237: B+Tree Delete: Underflow va Sibling Borrow/Merge
**Tavsif:** Leaf tugunidan kalit o'chirilganda elementlar soni minimal chegaradan (ORDER/2) kamayib ketsa, qo'shni leafdan kalit qarzga olinadi (borrow) yoki ikkala leaf bitta qilib birlashtiriladi (merge).
**Talablar:** C++20, minimal to'ldirish omili (fill factor), merge va underflow ni boshqarish.
**Yechim (C++):**
```cpp
#include <iostream>
#include <vector>

struct DeletableLeaf {
    std::vector<int> keys;
    static constexpr size_t MIN_KEYS = 2;

    bool needs_rebalance() const {
        return keys.size() < MIN_KEYS;
    }

    bool try_borrow_from(DeletableLeaf& right_sibling) {
        if (right_sibling.keys.size() > MIN_KEYS) {
            keys.push_back(right_sibling.keys.front());
            right_sibling.keys.erase(right_sibling.keys.begin());
            return true;
        }
        return false;
    }
};

int main() {
    DeletableLeaf l1, l2;
    l1.keys = {10}; // Underflow! (MIN=2)
    l2.keys = {20, 30, 40}; // Ortiqcha kaliti bor

    if (l1.needs_rebalance()) {
        std::cout << "L1 Underflow holatida! Qo'shnidan qarz olamiz...\n";
        if (l1.try_borrow_from(l2)) {
            std::cout << "Qarz olindi! L1 hajmi: " << l1.keys.size() << ", L2 hajmi: " << l2.keys.size() << std::endl;
        }
    }
    return 0;
}
```
**Tushuntirish:** Underflow boshqaruvi B+Tree xotira zichligini saqlab qoladi va daraxt sahifalarining keraksiz bo'shab qolishini oldini oladi.

### Topshiriq #1238: B+Tree Range Scan Iterator va Leaf Forward Chaining
**Tavsif:** B+Tree ning asosiy kuchi oraliq qidiruvdadir (`SELECT * WHERE id >= 100 AND id <= 500`). Iterator boshlang'ich nuqtaga binar qidiruv bilan sakraydi, so'ngra `next_leaf` ko'rsatkichlari bo'yicha chiziqli siljiydi.
**Talablar:** C++20, `begin(min_key)`, `end(max_key)`, samarali oraliq skanerlash.
**Yechim (C++):**
```cpp
#include <iostream>
#include <vector>

struct Leaf {
    std::vector<int> keys;
    Leaf* next{nullptr};
};

class BTreeScanner {
public:
    static void scan_range(Leaf* start_leaf, int min_val, int max_val) {
        Leaf* curr = start_leaf;
        std::cout << "[Range Scan " << min_val << ".." << max_val << "]: ";
        while (curr != nullptr) {
            for (int k : curr->keys) {
                if (k >= min_val && k <= max_val) {
                    std::cout << k << " ";
                } else if (k > max_val) {
                    std::cout << "\n";
                    return; // Diapazondan chiqdik
                }
            }
            curr = curr->next;
        }
        std::cout << "\n";
    }
};

int main() {
    Leaf l2{{40, 50, 60}, nullptr};
    Leaf l1{{10, 20, 30}, &l2};
    BTreeScanner::scan_range(&l1, 20, 50);
    return 0;
}
```
**Tushuntirish:** B+Tree range skani qattiq disklar va SSD larda ketma-ket (sequential) o'qish afzalligidan maksimal foydalanadi va prefetchni faollashtiradi.

### Topshiriq #1239: OS Page Cache Prefetching va `posix_fadvise` Optimizatsiyasi
**Tavsif:** Katta hajmli Compaction yoki Range Scan paytida Linux yadrosiga oldindan ma'lumotlarni xotiraga yuklab turishni bildirish uchun `posix_fadvise(POSIX_FADV_SEQUENTIAL)` va `POSIX_FADV_WILLNEED` qo'llaniladi.
**Talablar:** C++20, OS file descriptors, asynchronous read-ahead chaqiruvlari.
**Yechim (C++):**
```cpp
#include <iostream>
#include <cstdint>

// Soddalashtirilgan posix_fadvise simulyatori
void advise_sequential_read(int fd, uint64_t offset, size_t len) {
    std::cout << "[posix_fadvise] Yadroga xabar: Offset " << offset 
              << ", Len " << len << " ketma-ket o'qiladi. Asinxron readahead faollashtirildi.\n";
}

int main() {
    advise_sequential_read(3, 0, 64 * 1024 * 1024); // 64MB SSTable fayli
    return 0;
}
```
**Tushuntirish:** Fadvise yadroga readahead oynasini 128KB dan 2MB gacha kattalashtirish imkonini beradi, bu esa I/O kutish vaqtini (iowait) 40% ga qisqartiradi.

### Topshiriq #1240: Memory-Mapped SSTable Reader (`mmap` Zero-Copy)
**Tavsif:** SSTable fayllarini oddiy `read()` tizim chaqiruvi bilan o'qish user-space va kernel-space o'rtasida ma'lumotlarni nusxalaydi. `mmap` orqali fayl to'g'ridan-to'g'ri virtual xotira manziliga bog'lanadi.
**Talablar:** C++20, `mmap` / `munmap` resurs boshqaruvi (RAII), xotiradagi baytlarni to'g'ridan-to'g'ri o'qish.
**Yechim (C++):**
```cpp
#include <iostream>
#include <string_view>
#include <memory>

class MmapFileView {
    const char* data_{nullptr};
    size_t size_{0};

public:
    MmapFileView(const char* mapped_data, size_t s) : data_(mapped_data), size_(s) {}

    std::string_view read_slice(size_t offset, size_t len) const {
        if (offset + len <= size_) {
            return std::string_view(data_ + offset, len);
        }
        return {};
    }
};

int main() {
    const char mock_mmap[] = "ROCKSDB_SSTABLE_HEADER_BLOCK_DATA_PAYLOAD";
    MmapFileView view(mock_mmap, sizeof(mock_mmap));
    auto slice = view.read_slice(0, 7);
    std::cout << "Zero-Copy o'qilgan sarlavha: " << slice << std::endl;
    return 0;
}
```
**Tushuntirish:** Mmap zero-copy o'qishni ta'minlaydi. Biroq yirik ma'lumotlar bazalarida TLB shootdown va sahifa xatolari (page fault) sababli RocksDB odatda faqat kichik L0/L1 fayllarida mmap ishlatadi.

### Topshiriq #1241: Disk I/O Rate Limiter: Flush va Compaction ni Me'yorlash
**Tavsif:** Agar fondagi Compaction juda tez ishlasa, u diskning barcha o'tkazuvchanligini band qilib, foydalanuvchining jonli o'qish/yozish so'rovlarini qotirib qo'yadi. Rate Limiter (Token Bucket) har soniyada ruxsat etilgan I/O baytlarini cheklaydi.
**Talablar:** C++20, Token Bucket algoritmi, `request_tokens(bytes)` va kechikish kiritish.
**Yechim (C++):**
```cpp
#include <iostream>
#include <chrono>
#include <thread>
#include <mutex>
#include <algorithm>

class RateLimiter {
    int64_t rate_bytes_per_sec_;
    int64_t available_tokens_;
    std::chrono::steady_clock::time_point last_refill_;
    std::mutex mtx_;

public:
    RateLimiter(int64_t limit_bytes) 
        : rate_bytes_per_sec_(limit_bytes), available_tokens_(limit_bytes),
          last_refill_(std::chrono::steady_clock::now()) {}

    void request(int64_t bytes) {
        std::lock_guard<std::mutex> lock(mtx_);
        auto now = std::chrono::steady_clock::now();
        auto elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(now - last_refill_).count();
        if (elapsed > 0) {
            available_tokens_ = std::min(rate_bytes_per_sec_, 
                available_tokens_ + (rate_bytes_per_sec_ * elapsed) / 1000);
            last_refill_ = now;
        }

        if (available_tokens_ < bytes) {
            std::cout << "[RateLimiter] Limit oshdi! " << bytes << " bayt uchun sun'iy pauza qo'yilmoqda.\n";
            std::this_thread::sleep_for(std::chrono::milliseconds(5));
        }
        available_tokens_ -= bytes;
    }
};

int main() {
    RateLimiter limiter(10 * 1024 * 1024); // 10 MB/s limit
    limiter.request(15 * 1024 * 1024);
    return 0;
}
```
**Tushuntirish:** Rate Limiter orqali ma'lumotlar bazasi p99 kechikishi (tail latency) barqaror saqlanadi va disk saturatsiyasi oldi olinadi.

### Topshiriq #1242: Write Stall Mexanizmi: Compaction Sekinlashganda Yozishni To'xtatish
**Tavsif:** Agar yozish oqimi juda tez bo'lsa va diskdagi Level-0 fayllar soni kritik chegaradan (masalan 20 tadan) oshib ketsa, LSM dvigateli yangi yozuvlarni sekinlashtiradi (slowdown) yoki to'liq to'xtatadi (stall).
**Talablar:** C++20, Level-0 fayllar soni tekshiruvi: <4 (Normal), 4..12 (Slowdown), >12 (Complete Stall).
**Yechim (C++):**
```cpp
#include <iostream>
#include <thread>
#include <chrono>

enum class WriteStallState {
    kNormal,
    kDelayed,
    kStopped
};

class WriteStallController {
public:
    static WriteStallState check_l0_health(int num_l0_files) {
        if (num_l0_files >= 12) {
            std::cout << "[WriteStall] DIQQAT: L0 fayllar soni " << num_l0_files 
                      << "! Barcha yozishlar to'xtatildi (STALL).\n";
            return WriteStallState::kStopped;
        } else if (num_l0_files >= 4) {
            std::cout << "[WriteStall] OGOHLANTIRISH: L0 to'lmoqda. Yozish 1ms ga sekinlashtirildi.\n";
            return WriteStallState::kDelayed;
        }
        return WriteStallState::kNormal;
    }
};

int main() {
    WriteStallController::check_l0_health(3);
    WriteStallController::check_l0_health(6);
    WriteStallController::check_l0_health(15);
    return 0;
}
```
**Tushuntirish:** Write Stall bo'lmasa, Level-0 dagi fayllar soni yuzlab bo'lib ketadi va har bitta `Get` so'rovi barcha L0 fayllarni diskdan ochib o'qishga majbur bo'lib, butun serverni falaj qiladi.

### Topshiriq #1243: Direct I/O (`O_DIRECT`) va Aligned Memory Buffer
**Tavsif:** OS Page Cache ikki marta keshlanishga (Double Caching) sabab bo'ladi: bir marta Block Cache da, bir marta Linux OS keshida. Direct I/O orqali OS Page Cache aylanib o'tiladi, biroq xotira manzillari va o'lchamlar qat'iy 4096 baytga tekislangan (aligned) bo'lishi shart.
**Talablar:** C++20, `posix_memalign` yoki `std::aligned_alloc`, 4096-bayt alignment.
**Yechim (C++):**
```cpp
#include <iostream>
#include <cstdlib>
#include <cstdint>
#include <cstring>

class DirectIOAlignedBuffer {
    void* buffer_{nullptr};
    size_t size_{0};

public:
    DirectIOAlignedBuffer(size_t size) : size_(size) {
        // Direct I/O uchun xotira 4096 ga karrali bo'lishi shart
        size_t aligned_size = (size + 4095) & ~4095;
        buffer_ = std::aligned_alloc(4096, aligned_size);
        std::memset(buffer_, 0, aligned_size);
    }

    ~DirectIOAlignedBuffer() {
        if (buffer_) std::free(buffer_);
    }

    void* get() { return buffer_; }
    size_t size() const { return size_; }
};

int main() {
    DirectIOAlignedBuffer buf(8192);
    std::cout << "Direct I/O buferi ajratildi: Manzil = " << buf.get() 
              << ", 4096 ga karrali: " << (reinterpret_cast<uintptr_t>(buf.get()) % 4096 == 0 ? "Ha" : "Yo'q") << std::endl;
    return 0;
}
```
**Tushuntirish:** Direct I/O NVMe disklardan maksimal IOPS olish va katta serverlarda kesh xotirasini tejash uchun eng muhim drayver rejimdir.

### Topshiriq #1244: Column Families (RocksDB Arxitekturasi) va Yagona WAL
**Tavsif:** RocksDB bir nechta mantiqiy jadvallarni (Column Families) bitta ma'lumotlar bazasida saqlash imkonini beradi. Har bir Column Family o'z MemTable va SSTable lariga ega, biroq ularning barchasi yagona umumiy WAL jurnalidan foydalanadi.
**Talablar:** C++20, `cf_id` (Column Family ID), ko'p jadvalli yozuvlarni yagona log oqimiga yozish.
**Yechim (C++):**
```cpp
#include <iostream>
#include <string>
#include <unordered_map>
#include <memory>

struct ColumnFamilyHandle {
    uint32_t id;
    std::string name;
};

class MultiCFEngine {
    std::unordered_map<uint32_t, std::string> cf_tables_;

public:
    void write_shared_wal(uint32_t cf_id, const std::string& key, const std::string& val) {
        std::cout << "[Shared WAL] CF_ID: " << cf_id << " -> " << key << "=" << val << "\n";
        cf_tables_[cf_id] += key + ",";
    }
};

int main() {
    ColumnFamilyHandle default_cf{0, "default"};
    ColumnFamilyHandle user_cf{1, "user_metadata"};
    MultiCFEngine engine;

    engine.write_shared_wal(default_cf.id, "setting:theme", "dark");
    engine.write_shared_wal(user_cf.id, "user:777:phone", "+998901234567");
    return 0;
}
```
**Tushuntirish:** Yagona WAL bir nechta Column Family larga tegishli atomik tranzaksiyalarni kafolatlaydi va disk boshchalari (seek) o'rtasidagi chalkashlikni bartaraf qiladi.

### Topshiriq #1245: SSTable Checksum Validatsiyasi (XXH3 va CRC32C)
**Tavsif:** Qattiq disklarda bit-rot yoki apparat xatolari sababli ma'lumotlar buzilishi (silent data corruption) yuz berishi mumkin. Har bir 4KB SSTable bloki oxiriga 4 baytli checksum qo'yiladi va har o'qishda tekshiriladi.
**Talablar:** C++20, blok o'qilganda checksum tekshirish, mos kelmasa `CorruptionException` chaqirish.
**Yechim (C++):**
```cpp
#include <iostream>
#include <cstdint>
#include <stdexcept>
#include <vector>

uint32_t simple_checksum(const uint8_t* data, size_t len) {
    uint32_t c = 0x12345678;
    for (size_t i = 0; i < len; ++i) c = (c * 31) ^ data[i];
    return c;
}

void verify_block_integrity(const std::vector<uint8_t>& block) {
    if (block.size() < 4) throw std::runtime_error("Blok juda kichik!");
    size_t payload_len = block.size() - 4;
    uint32_t expected_crc = simple_checksum(block.data(), payload_len);
    uint32_t stored_crc = *reinterpret_cast<const uint32_t*>(block.data() + payload_len);

    if (expected_crc != stored_crc) {
        throw std::runtime_error("[Disk Corruption] Checksum mos kelmadi! Blok buzilgan.");
    }
    std::cout << "[Integrity OK] Blok xavfsiz o'qildi.\n";
}

int main() {
    std::vector<uint8_t> block = {'H', 'E', 'L', 'L', 'O', 0, 0, 0, 0};
    uint32_t crc = simple_checksum(block.data(), 5);
    *reinterpret_cast<uint32_t*>(block.data() + 5) = crc;

    try {
        verify_block_integrity(block);
    } catch (const std::exception& e) {
        std::cerr << e.what() << std::endl;
    }
    return 0;
}
```
**Tushuntirish:** Ushbu mexanizm korruptsiyaga uchragan ma'lumotlar xotiraga yuklanib, boshqa jadvallarni ifloslantirishining oldini oladi.

### Topshiriq #1246: Compaction Filter: TTL O'tgan Yozuvlarni Avtomatik Tozalash
**Tavsif:** Foydalanuvchi ma'lumotlari uchun TTL (Time-To-Live) belgilangan bo'lsa, ularni qo'lda o'chirib chiqish qimmatga tushadi. RocksDB `CompactionFilter` interfeysi orqali eskirgan yozuvlarni Compaction vaqtida bir yo'la diskdan olib tashlaydi.
**Talablar:** C++20, `CompactionFilter` abstrakt sinfi, `Filter(key, value)` metodi, `kRemove` yoki `kKeep` qaytarish.
**Yechim (C++):**
```cpp
#include <iostream>
#include <string>
#include <chrono>

enum class Decision { kKeep, kRemove };

class CompactionFilter {
public:
    virtual ~CompactionFilter() = default;
    virtual Decision filter(const std::string& key, const std::string& val) const = 0;
};

class ExpiredOrderFilter : public CompactionFilter {
public:
    Decision filter(const std::string& key, const std::string& val) const override {
        if (key.rfind("order_temp:", 0) == 0) {
            std::cout << "[CompactionFilter] Vaqtinchalik buyurtma tozalandi: " << key << "\n";
            return Decision::kRemove;
        }
        return Decision::kKeep;
    }
};

int main() {
    ExpiredOrderFilter filter;
    Decision d1 = filter.filter("order_temp:99", "15$");
    Decision d2 = filter.filter("user:permanent:42", "Toshkent");
    std::cout << "D1: " << (d1 == Decision::kRemove ? "O'chirildi" : "Qoldirildi") << std::endl;
    std::cout << "D2: " << (d2 == Decision::kRemove ? "O'chirildi" : "Qoldirildi") << std::endl;
    return 0;
}
```
**Tushuntirish:** Compaction Filter hech qanday qo'shimcha disk I/O talab qilmaydi, chunki Compaction baribir fayllarni o'qib-yozayotgan bo'ladi.

### Topshiriq #1247: LSM Backup Engine va Hard Linklar Orqali Hot Backup
**Tavsif:** SSTable fayllari o'zgarmas (immutable) bo'lganligi sababli, LSM daraxtidan zaxira nusxa (backup) olish uchun ularni qayta nusxalash shart emas. POSIX `link()` (Hard Link) orqali nol-bayt nusxalash bilan soniyaning ulushlarida to'liq hot backup olinadi.
**Talablar:** C++20, MANIFEST snapshotini olish va SSTable fayllariga hard link yaratish.
**Yechim (C++):**
```cpp
#include <iostream>
#include <vector>
#include <string>

class BackupEngine {
public:
    static void create_instant_backup(const std::vector<std::string>& active_sst_files, const std::string& backup_dir) {
        std::cout << "[Hot Backup] Zaxira nusxa yaratilmoqda: " << backup_dir << "\n";
        for (const auto& file : active_sst_files) {
            // Haqiqiy Linux tizimida: link(file.c_str(), (backup_dir + "/" + file).c_str())
            std::cout << "  Hard Link yaratildi: " << file << " -> " << backup_dir << "/" << file << "\n";
        }
        std::cout << "[Hot Backup] Yakunlandi! Disk bo'sh joyi sarflanmadi (0 bytes extra).\n";
    }
};

int main() {
    std::vector<std::string> sst_files = {"000012.sst", "000015.sst", "000018.sst"};
    BackupEngine::create_instant_backup(sst_files, "/var/backups/db_snapshot_2026");
    return 0;
}
```
**Tushuntirish:** Hard linklar tufayli asosiy dvigatel eski fayllarni o'chirgan taqdirda ham, zaxira papkasidagi inode ko'rsatkichi saqlanib qoladi va ma'lumotlar xavfsiz bo'ladi.

### Topshiriq #1248: Persistent Tiered Cache (Secondary Cache NVMe SSD uchun)
**Tavsif:** RAM hajmi cheklangan (masalan 64GB), lekin bazalar terabaytlab hajmda bo'ladi. RocksDB NvmCache arxitekturasi RAM Block Cache to'lganda bloklarni sekin HDD ga emas, balki oraliq tezkor NVMe SSD Persistent Keshiga tushiradi.
**Talablar:** C++20, Tier 1 (RAM) va Tier 2 (NVMe Secondary Cache) o'rtasidagi kogerentlik.
**Yechim (C++):**
```cpp
#include <iostream>
#include <string>
#include <optional>

class SecondaryCacheTier {
public:
    void spill_to_nvme(const std::string& block_id, const std::string& data) {
        std::cout << "[Tier 2 NVMe Cache] Blok RAM dan NVMe keshiga surildi: " << block_id 
                  << " (" << data.size() << " bayt)\n";
    }

    std::optional<std::string> fetch_from_nvme(const std::string& block_id) {
        std::cout << "[Tier 2 NVMe Cache HIT] Blok NVMe dan o'qildi: " << block_id << "\n";
        return "DATA_FROM_NVME";
    }
};

int main() {
    SecondaryCacheTier tier2;
    tier2.spill_to_nvme("sst_block_999", "COMPRESSED_PAGE_DATA");
    auto res = tier2.fetch_from_nvme("sst_block_999");
    return 0;
}
```
**Tushuntirish:** Tiered Caching arxitekturasi DRAM xarajatlarini keskin kamaytirib, yirik bulutli ma'lumotlar omborlarida o'qish kechikishini mikrosekundlarda ushlab turadi.

### Topshiriq #1249: Prefix Bloom Filter va SeekForPrev Iteratori
**Tavsif:** Ko'pincha so'rovlar ma'lum bir prefiks bo'yicha beriladi (`WHERE user_id = 42 AND ...`). RocksDB Prefix Bloom Filter faqat butun kalitni emas, balki uning prefiksini xeshlaydi. Bu `SeekPrefix` chaqiruvlarida keraksiz SSTable larni chetlab o'tish imkonini beradi.
**Talablar:** C++20, SliceTransform (Prefiks uzunligini aniqlash), Prefix Bloom Filter integratsiyasi.
**Yechim (C++):**
```cpp
#include <iostream>
#include <string>
#include <string_view>

class SliceTransform {
    size_t prefix_len_{4};
public:
    SliceTransform(size_t len) : prefix_len_(len) {}

    std::string_view transform(std::string_view key) const {
        if (key.size() >= prefix_len_) return key.substr(0, prefix_len_);
        return key;
    }
};

int main() {
    SliceTransform slicer(8); // Har bir kalitning dastlabki 8 bayti prefiks
    std::string key1 = "usr_1001:order_1";
    std::string key2 = "usr_1001:order_2";

    std::cout << "Key1 Prefiks: " << slicer.transform(key1) << std::endl;
    std::cout << "Key2 Prefiks: " << slicer.transform(key2) << std::endl;
    std::cout << "Prefikslar tengmi: " << (slicer.transform(key1) == slicer.transform(key2) ? "Ha" : "Yo'q") << std::endl;
    return 0;
}
```
**Tushuntirish:** Prefix Bloom Filter orqali millionlab fayllar ichidan kerakli prefiksga ega ma'lumotlar bitta disk I/O bilan topiladi.

### Topshiriq #1250: To'liq LSM-Tree Storage Engine: Get, Put, Delete va Compaction API
**Tavsif:** Oldingi barcha komponentlarni (MemTable, WAL, SSTable, Bloom Filter, Compaction) yagona yuqori darajali `StorageEngine` sinfiga birlashtirish. Tizim to'liq ishlab turgan CRUD va flush sikliga ega bo'lishi lozim.
**Talablar:** C++20, to'liq ishlaydigan `DB::Open`, `DB::Put`, `DB::Get`, `DB::Delete` va `DB::Close` interfeysi.
**Yechim (C++):**
```cpp
#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>
#include <optional>
#include <memory>

class StorageEngine {
    std::unordered_map<std::string, std::string> memtable_;
    std::vector<std::pair<std::string, std::string>> disk_sstable_;
    uint64_t current_seq_{0};

public:
    static std::unique_ptr<StorageEngine> open(const std::string& db_path) {
        std::cout << "[StorageEngine] Ma'lumotlar bazasi ochildi: " << db_path << "\n";
        return std::make_unique<StorageEngine>();
    }

    void put(const std::string& key, const std::string& value) {
        current_seq_++;
        memtable_[key] = value;
        std::cout << "[PUT] Key=" << key << ", Seq=" << current_seq_ << "\n";
        if (memtable_.size() >= 3) {
            flush_to_disk();
        }
    }

    std::optional<std::string> get(const std::string& key) {
        // 1. MemTable dan qidiramiz
        auto it = memtable_.find(key);
        if (it != memtable_.end()) {
            std::cout << "[GET] MemTable dan topildi!\n";
            return it->second;
        }

        // 2. SSTable dan qidiramiz
        for (const auto& item : disk_sstable_) {
            if (item.first == key) {
                std::cout << "[GET] Disk SSTable dan topildi!\n";
                return item.second;
            }
        }
        return std::nullopt;
    }

    void delete_key(const std::string& key) {
        put(key, "[TOMBSTONE]");
    }

    void flush_to_disk() {
        std::cout << "[FLUSH] MemTable diskka SSTable qilib yozilmoqda...\n";
        for (auto& item : memtable_) {
            disk_sstable_.push_back(item);
        }
        memtable_.clear();
    }
};

int main() {
    auto db = StorageEngine::open("/tmp/khorazmiy_lsm_db");
    db->put("lang", "C++20");
    db->put("engine", "LSM-Tree");
    db->put("performance", "Ultra-High"); // Bu yerda flush chaqiriladi

    auto val = db->get("lang");
    if (val) {
        std::cout << "O'qilgan natija: " << *val << std::endl;
    }
    return 0;
}
```
**Tushuntirish:** Ushbu arxitektura RocksDB, LevelDB va Cassandra kabi tizimlarning yuragini tashkil etadi. Yozish doim xotiraga (RAM) tushadi, diskka esa faqat tartiblangan bloklar yoziladi.

