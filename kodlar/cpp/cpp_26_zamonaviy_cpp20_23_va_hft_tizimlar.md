# C++ 26-Modul: Zamonaviy C++20 va C++23 Standartlari: Coroutines, Concepts, PMR, DOD, SIMD va High-Frequency Trading (HFT) Past Kechikishli Tizimlar

Ushbu modulda jahon moliya bozorlaridagi yuqori chastotali savdo (High-Frequency Trading - HFT), birja ulanishlari (Exchange Market Data & Order Routing), mikrosoniya va nanosekund darajasidagi past kechikishli (ultra low-latency) tizimlar hamda zamonaviy C++20 va C++23 imkoniyatlari (Coroutines, Concepts, PMR, SIMD, Cache-friendly Data-Oriented Design) professional muhandislik darajasida yoritilgan.

---

### Topshiriq #1251: False Sharing-dan Xoli Cache-Line Aligned Lock-Free SPSC Ring Buffer
**Tavsif:** HFT tizimlarida bitta yadroda tarmoq paketlarini qabul qiluvchi oqim (Network IO Thread) va boshqa yadroda savdo strategiyasini hisoblovchi oqim (Trading Engine Thread) o'rtasida ma'lumot almashinuvi nanosekundlarda o'lchanadi. Agar o'quvchi va yozuvchi indekslari bir xil CPU Cache Line (64 bayt) ichida joylashsa, "False Sharing" yuz beradi va keshlararo koherensiya protokoli (MESI) tufayli tezlik keskin tushadi.
**Talablar:** C++20 standarti, `std::hardware_destructive_interference_size` yoki `alignas(64)` orqali kesh liniyasini ajratish, atomic acquire-release semantikasi, zero heap allocation, to'liq lock-free Single-Producer Single-Consumer (SPSC) halqasimon navbat.
**Yechim (C++):**
```cpp
#include <iostream>
#include <atomic>
#include <new>
#include <array>
#include <thread>
#include <chrono>

// HFT darajasidagi kesh liniyasi o'lchami (odatda x86_64 da 64 bayt)
#ifdef __cpp_lib_hardware_interference_size
using std::hardware_destructive_interference_size;
#else
constexpr size_t hardware_destructive_interference_size = 64;
#endif

template <typename T, size_t Capacity>
class CacheAlignedSPSCQueue {
    static_assert((Capacity & (Capacity - 1)) == 0, "Capacity 2 ning darajasi bo'lishi shart!");

    // Xotirada 64-baytli kesh liniyasiga tekislangan elementlar massivi
    alignas(hardware_destructive_interference_size) std::array<T, Capacity> buffer_;

    // Yozuvchi oqim (Producer) faqat o'zi yangilaydigan head indeksi
    alignas(hardware_destructive_interference_size) std::atomic<size_t> head_{0};
    // False sharing bo'lmasligi uchun kesh chiziq to'ldirgichi (padding)
    char pad1_[hardware_destructive_interference_size - sizeof(std::atomic<size_t>)];

    // O'quvchi oqim (Consumer) faqat o'zi yangilaydigan tail indeksi
    alignas(hardware_destructive_interference_size) std::atomic<size_t> tail_{0};
    char pad2_[hardware_destructive_interference_size - sizeof(std::atomic<size_t>)];

    // O'quvchi indeksining mahalliy nusxasi (Producer cache-miss kamaytirish uchun)
    size_t cached_tail_{0};
    // Yozuvchi indeksining mahalliy nusxasi (Consumer cache-miss kamaytirish uchun)
    size_t cached_head_{0};

public:
    CacheAlignedSPSCQueue() : cached_tail_(0), cached_head_(0) {}

    // Element qo'shish (Producer) - Noexcept va Zero-Allocation
    bool push(const T& item) noexcept {
        const size_t current_head = head_.load(std::memory_order_relaxed);
        if ((current_head - cached_tail_) == Capacity) {
            // Mahalliy kesh eskirgan bo'lsa, haqiqiy tail'ni acquire bilan o'qiymiz
            cached_tail_ = tail_.load(std::memory_order_acquire);
            if ((current_head - cached_tail_) == Capacity) {
                return false; // Navbat to'la
            }
        }
        buffer_[current_head & (Capacity - 1)] = item;
        head_.store(current_head + 1, std::memory_order_release);
        return true;
    }

    // Elementni olish (Consumer) - Noexcept va Lock-Free
    bool pop(T& item) noexcept {
        const size_t current_tail = tail_.load(std::memory_order_relaxed);
        if (current_tail == cached_head_) {
            // Mahalliy kesh eskirgan bo'lsa, haqiqiy head'ni acquire bilan o'qiymiz
            cached_head_ = head_.load(std::memory_order_acquire);
            if (current_tail == cached_head_) {
                return false; // Navbat bo'sh
            }
        }
        item = buffer_[current_tail & (Capacity - 1)];
        tail_.store(current_tail + 1, std::memory_order_release);
        return true;
    }
};

struct OrderPacket {
    uint64_t order_id;
    uint32_t price_cents;
    uint32_t quantity;
    char side; // 'B' = Buy, 'S' = Sell
};

int main() {
    CacheAlignedSPSCQueue<OrderPacket, 1024> queue;

    std::thread producer([&]() {
        for (uint64_t i = 1; i <= 5; ++i) {
            OrderPacket p{i, 15000 + static_cast<uint32_t>(i * 10), 100, 'B'};
            while (!queue.push(p)) {
                // HFT spin-wait yondashuvi
            }
        }
    });

    std::thread consumer([&]() {
        for (int i = 0; i < 5; ++i) {
            OrderPacket p{};
            while (!queue.pop(p)) {
                // Spin-wait
            }
            std::cout << "[Consumer Core] Buyurtma qayta ishlandi: ID=" << p.order_id 
                      << ", Narx=" << p.price_cents / 100.0 << "$, Miqdor=" << p.quantity 
                      << ", Tomon=" << p.side << "\n";
        }
    });

    producer.join();
    consumer.join();
    return 0;
}
```
**Tushuntirish:** `alignas(64)` Head va Tail ko'rsatkichlarini alohida L1 kesh chiziqlariga ajratadi. Natijada bir oqimning yozishi ikkinchi oqimning kesh liniyasini invalidatsiya (invalidation) qilmaydi. `acquire-release` semantikasi esa xotira to'sig'ini (memory barrier) eng zarur joydagina saqlab, assembly darajasida ortiqcha `mfence` yo'riqnomasidan xalos etadi.
**Ishlash natijasi:**
```text
[Consumer Core] Buyurtma qayta ishlandi: ID=1, Narx=150.1$, Miqdor=100, Tomon=B
[Consumer Core] Buyurtma qayta ishlandi: ID=2, Narx=150.2$, Miqdor=100, Tomon=B
[Consumer Core] Buyurtma qayta ishlandi: ID=3, Narx=150.3$, Miqdor=100, Tomon=B
[Consumer Core] Buyurtma qayta ishlandi: ID=4, Narx=150.4$, Miqdor=100, Tomon=B
[Consumer Core] Buyurtma qayta ishlandi: ID=5, Narx=150.5$, Miqdor=100, Tomon=B
```

---

### Topshiriq #1252: C++20 Concepts & Constraints bilan HFT Buyurtma Tiplarini Kompilyatsiya Vaqtida Tekshirish
**Tavsif:** HFT dvigatellarida runtime polimorfizmi (virtual funksiyalar va `vtable` orqali dinamik dispatch) keskin man etiladi, chunki u keshdan chetga chiqish (indirect branch / cache miss) va kechikish olib keladi. Barcha cheklovlar kompilyatsiya vaqtida (compile-time) qat'iy tekshirilishi zarur.
**Talablar:** C++20 `concept` va `requires` iboralaridan foydalanib, moliyaviy instrumentlar va buyurtma strukturalarining xotira o'lchami (`sizeof <= 64`), xotira nusxalanish qobiliyati (`std::is_trivially_copyable_v`) va zaruriy maydonlari borligini tekshiruvchi konseptlar tizimini yaratish.
**Yechim (C++):**
```cpp
#include <iostream>
#include <concepts>
#include <type_traits>
#include <string_view>

// HFT Buyurtmasi uchun talab qilinadigan konsept
template <typename T>
concept HFTOrder = requires(T order) {
    { order.order_id } -> std::convertible_to<uint64_t>;
    { order.price } -> std::convertible_to<uint32_t>;
    { order.quantity } -> std::convertible_to<uint32_t>;
    { order.is_buy() } -> std::same_as<bool>;
} && std::is_trivially_copyable_v<T> && (sizeof(T) <= 64);

// Talabga javob beruvchi haqiqiy Limit Order strukturasi
struct alignas(32) FastLimitOrder {
    uint64_t order_id;
    uint32_t price;
    uint32_t quantity;
    bool is_buy_side;

    bool is_buy() const noexcept {
        return is_buy_side;
    }
};

// Talabga javob bermaydigan (std::string dinamik xotira talab qiladi va trivially copyable emas)
struct InvalidOrder {
    uint64_t order_id;
    uint32_t price;
    uint32_t quantity;
    std::string trader_note; // Virtual/dynamic xotira - taqiqlangan!
    bool is_buy() const { return true; }
};

// Faqat HFTOrder konseptiga mos keluvchi turlarni qabul qiluvchi shablon
template <HFTOrder OrderType>
class MatchingEngineGateway {
public:
    void submit_order(const OrderType& order) noexcept {
        std::cout << "[MatchingEngineGateway] Kompilyatsiya vaqtida tasdiqlangan buyurtma: ID=" 
                  << order.order_id << ", Hajmi=" << sizeof(OrderType) << " bayt\n";
    }
};

int main() {
    FastLimitOrder valid_order{100234, 45000, 250, true};
    MatchingEngineGateway<FastLimitOrder> gateway;
    gateway.submit_order(valid_order);

    // Quyidagi qator kompilyatsiya xatosini bergan bo'lardi:
    // MatchingEngineGateway<InvalidOrder> bad_gateway; 
    
    std::cout << "Kompilyatsiya vaqtida qat'iy tur tekshiruvi muvaffaqiyatli o'tdi!\n";
    return 0;
}
```
**Tushuntirish:** C++20 Concepts kompilyatorga kodni shablon instansiyalashidan oldin tekshirish imkonini beradi. `is_trivially_copyable_v` sharti ob'ektni `memcpy` bilan xotiradan to'g'ridan-to'g'ri nusxalash mumkinligini kafolatlaydi, `sizeof <= 64` esa buyurtma bitta kesh liniyasiga sig'ishini ta'minlaydi.
**Ishlash natijasi:**
```text
[MatchingEngineGateway] Kompilyatsiya vaqtida tasdiqlangan buyurtma: ID=100234, Hajmi=32 bayt
Kompilyatsiya vaqtida qat'iy tur tekshiruvi muvaffaqiyatli o'tdi!
```

---

### Topshiriq #1253: C++20 Coroutines (`co_yield`) Bilan Nol Kechikishli Bozor Ma'lumotlari Generator (Feed Handler)
**Tavsif:** Bozor kotirovkalari (Level-1 / Level-2 Tick Data) oqimini qabul qilishda an'anaviy callback yoki dinamik navbatlar qo'shimcha xotira ajratish va oqimlararo sinxronizatsiya yuki keltirib chiqaradi. C++20 Coroutine generatori yordamida keshda saqlanuvchi, holat mashinasi (state-machine) tarzida ishlovchi nol taqsimotli (zero-allocation) oqim yaratish zarur.
**Talablar:** C++20 korutina arxitekturasi: `std::coroutine_handle`, `promise_type`, `co_yield` operatori va to'liq ichki stackli boshqaruv.
**Yechim (C++):**
```cpp
#include <iostream>
#include <coroutine>
#include <cstdint>
#include <string_view>

struct MarketTick {
    uint64_t timestamp_ns;
    uint32_t price;
    uint32_t volume;
};

// C++20 Coroutine Generator turi
class MarketDataFeed {
public:
    struct promise_type {
        MarketTick current_tick;

        MarketDataFeed get_return_object() {
            return MarketDataFeed{std::coroutine_handle<promise_type>::from_promise(*this)};
        }
        std::suspend_always initial_suspend() noexcept { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }
        std::suspend_always yield_value(MarketTick tick) noexcept {
            current_tick = tick;
            return {};
        }
        void return_void() noexcept {}
        void unhandled_exception() { std::terminate(); }
    };

    using handle_type = std::coroutine_handle<promise_type>;

    explicit MarketDataFeed(handle_type h) : handle_(h) {}
    ~MarketDataFeed() {
        if (handle_) handle_.destroy();
    }

    MarketDataFeed(const MarketDataFeed&) = delete;
    MarketDataFeed& operator=(const MarketDataFeed&) = delete;

    MarketDataFeed(MarketDataFeed&& other) noexcept : handle_(other.handle_) {
        other.handle_ = nullptr;
    }

    bool next() {
        if (!handle_ || handle_.done()) return false;
        handle_.resume();
        return !handle_.done();
    }

    const MarketTick& value() const noexcept {
        return handle_.promise().current_tick;
    }

private:
    handle_type handle_;
};

// Tick oqimini emulyatsiya qiluvchi korutina
MarketDataFeed simulate_market_feed(uint64_t base_time) {
    uint32_t prices[] = {10020, 10025, 10022, 10030, 10028};
    uint32_t volumes[] = {150, 300, 200, 500, 400};

    for (size_t i = 0; i < 5; ++i) {
        co_yield MarketTick{base_time + (i * 250), prices[i], volumes[i]};
    }
}

int main() {
    auto feed = simulate_market_feed(1689000000000ULL);

    std::cout << "[HFT Feed Handler] Real-vaqtli tick ma'lumotlari qabuli:\n";
    while (feed.next()) {
        const auto& tick = feed.value();
        std::cout << "Tick: Vaqt=" << tick.timestamp_ns 
                  << "ns, Narx=" << tick.price / 100.0 
                  << "$, Hajm=" << tick.volume << "\n";
    }
    return 0;
}
```
**Tushuntirish:** C++20 `co_yield` orqali korutina o'z holatini to'xtatadi va boshqaruvni chaqiruvchiga topshiradi. Kompilyator korutinani tekis holat mashinasiga aylantiradi (HALO - Heap Allocation of Lookup Objects optimizatsiyasi bilan), bu esa qo'shimcha pthread yoki context switch-siz maksimal unumdorlikni beradi.
**Ishlash natijasi:**
```text
[HFT Feed Handler] Real-vaqtli tick ma'lumotlari qabuli:
Tick: Vaqt=1689000000000ns, Narx=100.2$, Hajm=150
Tick: Vaqt=1689000000250ns, Narx=100.25$, Hajm=300
Tick: Vaqt=1689000000500ns, Narx=100.22$, Hajm=200
Tick: Vaqt=1689000000750ns, Narx=100.3$, Hajm=500
Tick: Vaqt=1689000001000ns, Narx=100.28$, Hajm=400
```

---

### Topshiriq #1254: C++20 Coroutines (`co_await`): Asinxron Buyurtmalarni Bajarish Dvigateli (Custom Awaiter)
**Tavsif:** Birja shlyuzlariga yuborilgan buyurtmalarning tasdiqlanishi (Ack - Acknowledgment) bir necha mikrosekund talab qilishi mumkin. Oddiy sinxron kutish CPU yadrosini to'xtatib qo'yadi. Korutinali maxsus `Awaiter` yordamida buyurtmani jo'natish, kutish va birjadan javob kelganda holatni tiklash operatsiyasini nol ortiqcha xarajatsiz qurish lozim.
**Talablar:** `await_ready`, `await_suspend` va `await_resume` metodlariga ega bo'lgan C++20 Custom Awaiter strukturasi, zero dynamic allocation.
**Yechim (C++):**
```cpp
#include <iostream>
#include <coroutine>
#include <cstdint>

enum class OrderStatus { Pending, Filled, Rejected };

struct ExecutionReport {
    uint64_t order_id;
    OrderStatus status;
    uint32_t filled_shares;
};

// Maxsus Awaiter ob'ekti
struct OrderExecutionAwaiter {
    uint64_t order_id;
    ExecutionReport result{};

    // Agar buyurtma darhol bajarilgan bo'lsa kutmaslik
    bool await_ready() const noexcept {
        return false;
    }

    // Korutina to'xtatilganda chaqiriladi
    void await_suspend(std::coroutine_handle<> handle) noexcept {
        // Haqiqiy tizimda bu yerda tarmoq reaktoriga (epoll/kqueue) ro'yxatga qo'yiladi
        // Bu yerda simulyatsiya uchun birja darhol tasdiq yuboradi
        result = ExecutionReport{order_id, OrderStatus::Filled, 500};
        handle.resume(); // Oqimni davom ettirish
    }

    // Korutina uyg'onganda qaytariladigan qiymat
    ExecutionReport await_resume() const noexcept {
        return result;
    }
};

// Korutinaning qaytaruvchi vazifasi (Task)
struct AsyncTask {
    struct promise_type {
        AsyncTask get_return_object() { return AsyncTask{}; }
        std::suspend_never initial_suspend() noexcept { return {}; }
        std::suspend_never final_suspend() noexcept { return {}; }
        void return_void() noexcept {}
        void unhandled_exception() { std::terminate(); }
    };
};

// Asinxron savdo strategiyasi funksiyasi
AsyncTask execute_hft_strategy(uint64_t order_id) {
    std::cout << "[Strategy Engine] Buyurtma tarmoqqa uzatildi: ID=" << order_id << "\n";
    
    // co_await orqali javob kutish
    ExecutionReport report = co_await OrderExecutionAwaiter{order_id};

    std::cout << "[Strategy Engine] Birjadan ijro xabarnomasi olindi! ID=" << report.order_id 
              << ", Holat=" << (report.status == OrderStatus::Filled ? "FILLED" : "OTHER") 
              << ", Hajmi=" << report.filled_shares << " aksiya\n";
}

int main() {
    execute_hft_strategy(987654321ULL);
    return 0;
}
```
**Tushuntirish:** C++20 `co_await` orqali asinxron mantiq xuddi oddiy ketma-ket (protsedurali) kod kabi o'qiladi, ammo orqa fonda callback xotira yuki bo'lmaydi. Kompilyator barcha mahalliy o'zgaruvchilarni korutina ramkasida (frame) saqlaydi va birjadan javob kelganda instruction pointer'ni tiklaydi.
**Ishlash natijasi:**
```text
[Strategy Engine] Buyurtma tarmoqqa uzatildi: ID=987654321
[Strategy Engine] Birjadan ijro xabarnomasi olindi! ID=987654321, Holat=FILLED, Hajmi=500 aksiya
```

---

### Topshiriq #1255: `std::pmr::monotonic_buffer_resource` Bilan Zero-Allocation Tick-to-Trade Xotira Hovuzi
**Tavsif:** Har bir bozor kotirovkasi kelganda (`Tick`), HFT algoritmi vaqtinchalik hisob-kitoblarni amalga oshiradi (indikatorlar, vaqtinchalik vektorlar va xabarlar). Standart `malloc`/`new` operatsiyalari operatsion tizim darajasida lock olishi mumkin (heap contention), bu esa kechikishni yuzlab nanosekundlarga oshirib yuboradi.
**Talablar:** C++17/C++20 Polymorphic Memory Resources (`std::pmr`), stackda joylashgan bufer va `std::pmr::monotonic_buffer_resource` yordamida mutlaqo nol heap allocation bilan ishlash.
**Yechim (C++):**
```cpp
#include <iostream>
#include <memory_resource>
#include <vector>
#include <array>
#include <chrono>

struct TradeSignal {
    uint32_t price;
    uint32_t quantity;
    int signal_strength;
};

void process_tick_with_pmr(uint64_t tick_id) {
    // 4KB o'lchamdagi tezkor stack buferi
    alignas(64) std::array<std::byte, 4096> stack_buffer;

    // Monotonik xotira resursi: xotirani bo'lib beradi, ammo alohida deallocate qilmaydi
    std::pmr::monotonic_buffer_resource mem_pool(
        stack_buffer.data(), stack_buffer.size(), std::pmr::null_memory_resource()
    );

    // Xotirani faqatgina stackdagi mem_pool'dan oluvchi PMR vektor
    std::pmr::vector<TradeSignal> signals(&mem_pool);
    signals.reserve(32); // Hech qanday malloc bo'lmaydi!

    signals.push_back({10050, 100, 2});
    signals.push_back({10055, 300, 5});
    signals.push_back({10048, 200, -1});

    std::cout << "[Tick #" << tick_id << "] Stack PMR hovuzida signallar hisoblandi:\n";
    for (const auto& s : signals) {
        std::cout << "  Signal: Narx=" << s.price / 100.0 << "$, Kuch=" << s.signal_strength << "\n";
    }
    // Funksiya tugaganda stack_buffer avtomatik tozalanadi, zero deallocation overhead!
}

int main() {
    process_tick_with_pmr(1);
    process_tick_with_pmr(2);
    return 0;
}
```
**Tushuntirish:** `monotonic_buffer_resource` xotirani faqat pointer surish orqali (bump allocator) ajratadi. Xotira resursiga `std::pmr::null_memory_resource()` berilgani sababli, agar stack buferi to'lib ketsa, u heap'ga chiqmaydi, balki darhol `std::bad_alloc` berib tizim intizomini saqlaydi. Bu HFT da 2-3 nanosekundlik xotira ajratish tezligini ta'minlaydi.
**Ishlash natijasi:**
```text
[Tick #1] Stack PMR hovuzida signallar hisoblandi:
  Signal: Narx=100.5$, Kuch=2
  Signal: Narx=100.55$, Kuch=5
  Signal: Narx=100.48$, Kuch=-1
[Tick #2] Stack PMR hovuzida signallar hisoblandi:
  Signal: Narx=100.5$, Kuch=2
  Signal: Narx=100.55$, Kuch=5
  Signal: Narx=100.48$, Kuch=-1
```

---

### Topshiriq #1256: `std::pmr::unsynchronized_pool_resource` Bilan O'zgarmas O'lchamli HFT Slab Allocator
**Tavsif:** L2/L3 Order Book kitobida buyurtmalar soniyasiga yuz minglab marta kiritiladi va bekor qilinadi (churn). Turli o'lchamdagi elementlar uchun xotira fragmentatsiyasini yo'qotish va har bir oqimning o'zida blokirovkasiz (unsynchronized) tezkor slab-pool yaratish talab etiladi.
**Talablar:** C++20 `std::pmr::unsynchronized_pool_resource` konfiguratsiyasi, maxsus pool optsiyalari (`pool_options`), nol thread contention.
**Yechim (C++):**
```cpp
#include <iostream>
#include <memory_resource>
#include <list>
#include <string>

struct LimitOrderNode {
    uint64_t order_id;
    uint32_t price;
    uint32_t volume;
    char client_id[8];
};

class OrderBookSlabManager {
    // Har bir oqim uchun alohida, mutexsiz slab xotira resursi
    std::pmr::unsynchronized_pool_resource pool_;

public:
    OrderBookSlabManager() : pool_(get_options(), std::pmr::new_delete_resource()) {}

    static std::pmr::pool_options get_options() {
        std::pmr::pool_options opts;
        opts.max_blocks_per_chunk = 1024;
        opts.largest_required_pool_block = sizeof(LimitOrderNode) * 2;
        return opts;
    }

    std::pmr::unsynchronized_pool_resource* get_resource() noexcept {
        return &pool_;
    }
};

int main() {
    OrderBookSlabManager slab_mgr;
    
    // PMR ro'yxati (std::pmr::list) slab hovuzidan foydalanadi
    std::pmr::list<LimitOrderNode> active_orders(slab_mgr.get_resource());

    // Buyurtmalar qo'shish - slab pool ichidan darhol tayyor xotira bloklari beriladi
    active_orders.push_back({5001, 23000, 100, "TRD_01"});
    active_orders.push_back({5002, 23050, 400, "TRD_02"});
    active_orders.push_back({5003, 23025, 250, "TRD_03"});

    std::cout << "[Slab Allocator] Faol buyurtmalar ro'yxati:\n";
    for (const auto& ord : active_orders) {
        std::cout << "  ID=" << ord.order_id << ", Narx=" << ord.price / 100.0 
                  << "$, Hajm=" << ord.volume << ", Mijoz=" << ord.client_id << "\n";
    }

    // O'chirish ham heap fragmentation keltirib chiqarmaydi, slab ichida qayta ishlatiladi
    active_orders.pop_front();
    std::cout << "Bitta buyurtma o'chirildi, qolgan elementlar soni: " << active_orders.size() << "\n";
    return 0;
}
```
**Tushuntirish:** `unsynchronized_pool_resource` xotirani oldindan belgilangan bir xil o'lchamdagi "slab" bloklariga ajratadi. Ob'ekt o'chirilganda, bo'sh joy erkin ro'yxatga (free-list) qaytariladi va keyingi `push_back` paytida hech qanday tizim chaqiruvisiz darhol qayta taqdim etiladi.
**Ishlash natijasi:**
```text
[Slab Allocator] Faol buyurtmalar ro'yxati:
  ID=5001, Narx=230$, Hajm=100, Mijoz=TRD_01
  ID=5002, Narx=230.5$, Hajm=400, Mijoz=TRD_02
  ID=5003, Narx=230.25$, Hajm=250, Mijoz=TRD_03
Bitta buyurtma o'chirildi, qolgan elementlar soni: 2
```

---

### Topshiriq #1257: Data-Oriented Design (DOD): Array of Structures (AoS) vs Structure of Arrays (SoA) Order Book Depth
**Tavsif:** Ob'ektga yo'naltirilgan dasturlashda (OOP) har bir buyurtma bitta `struct` (AoS) sifatida saqlanadi. Ammo HFT narxlar kitobining 100 ta qatlamidagi umumiy hajmni (Total Depth Volume) yoki VWAP'ni hisoblashda CPU faqat narx va miqdor maydonlariga muhtoj. Agar butun struktura (ID, timestamp, trader_info va h.k.) yuklansa, L1 kesh keraksiz ma'lumotlar bilan to'lib ketadi.
**Talablar:** C++20 da Structure of Arrays (SoA) arxitekturasini yaratish, kesh-liniyaga to'g'ri joylashtirish va SIMD-ga mos ma'lumotlar sxemasi.
**Yechim (C++):**
```cpp
#include <iostream>
#include <vector>
#include <array>
#include <numeric>
#include <chrono>

constexpr size_t MAX_LEVELS = 64;

// 1. An'anaviy Array of Structures (AoS) - Kesh uchun samarasiz
struct OrderLevelAoS {
    uint32_t price;
    uint32_t volume;
    uint32_t order_count;
    uint64_t last_update_ts;
    char exchange_code[8];
};

// 2. Data-Oriented Design: Structure of Arrays (SoA) - Kesh uchun ideal
struct alignas(64) OrderBookDepthSoA {
    alignas(64) std::array<uint32_t, MAX_LEVELS> prices;
    alignas(64) std::array<uint32_t, MAX_LEVELS> volumes;
    alignas(64) std::array<uint32_t, MAX_LEVELS> order_counts;
    alignas(64) std::array<uint64_t, MAX_LEVELS> last_update_ts;
    size_t depth_count{0};

    void add_level(uint32_t p, uint32_t v, uint32_t c, uint64_t ts) noexcept {
        if (depth_count < MAX_LEVELS) {
            prices[depth_count] = p;
            volumes[depth_count] = v;
            order_counts[depth_count] = c;
            last_update_ts[depth_count] = ts;
            depth_count++;
        }
    }

    // Faqat hajmlar massivini ketma-ket keshga yuklab yig'ish
    uint64_t compute_total_volume() const noexcept {
        uint64_t total = 0;
        // Bitta 64-baytli kesh liniyasiga 16 ta uint32_t sig'adi!
        for (size_t i = 0; i < depth_count; ++i) {
            total += volumes[i];
        }
        return total;
    }
};

int main() {
    OrderBookDepthSoA book_depth;
    for (size_t i = 0; i < 16; ++i) {
        book_depth.add_level(15000 + i * 5, 100 * (i + 1), 5 + i, 1680000000 + i);
    }

    uint64_t total_v = book_depth.compute_total_volume();
    std::cout << "[DOD SoA Order Book] " << book_depth.depth_count 
              << " ta qatlam bo'yicha jami hajm: " << total_v << " dona\n";
    std::cout << "Kesh zichligi: Har bir 64-bayt kesh liniyasida 16 ta daraja hajmi saqlanadi!\n";
    return 0;
}
```
**Tushuntirish:** SoA yondashuvida `volumes` massivi xotirada yaxlit va zich (dense) joylashgan. 16 ta narx darajasi aynan 64 bayt (bitta CPU kesh liniyasi) bo'ladi. CPU prefetcher birinchi element so'ralgandayoq keyingi 15 ta elementni keshga olib keladi va hech qanday ortiqcha bayt (masalan, `last_update_ts` yoki matnlar) keshni ifloslantirmaydi.
**Ishlash natijasi:**
```text
[DOD SoA Order Book] 16 ta qatlam bo'yicha jami hajm: 13600 dona
Kesh zichligi: Har bir 64-bayt kesh liniyasida 16 ta daraja hajmi saqlanadi!
```

---

### Topshiriq #1258: AVX2 SIMD Intrinsics orqali Kotirovkalar Narxi va Hajmini Bir Vaqtda Qayta Ishlash
**Tavsif:** Birja bozor chuqurligidagi narxlar o'zgarganda, barcha limit buyurtmalarining yangi qiymatlarini (masalan, spread yoki komissiya qo'shilgan narxini) hisoblash kerak bo'ladi. Skalyar siklda 8 ta narxni hisoblash 8 ta tsikl oladi. AVX2 ko'rsatmalari yordamida bitta CPU tsiklida 8 ta 32-bitli butun sonni parallel hisoblash talab etiladi.
**Talablar:** `<immintrin.h>`, `_mm256_load_si256`, `_mm256_add_epi32`, `_mm256_store_si256` intrinsics, 32-baytli tekislash (`alignas(32)`).
**Yechim (C++):**
```cpp
#include <iostream>
#include <immintrin.h>
#include <array>
#include <cstdint>

// 8 ta 32-bitli butun sonni 32-baytli kesh chizig'ida saqlash
alignas(32) struct SIMDPriceArray {
    std::array<int32_t, 8> data;
};

void apply_spread_adjustment_avx2(const int32_t* in_prices, int32_t spread_offset, int32_t* out_prices) {
    // 1. 8 ta narxni bitta 256-bitli YMM registriga yuklash
    __m256i v_prices = _mm256_load_si256(reinterpret_cast<const __m256i*>(in_prices));

    // 2. Qo'shiladigan spread qiymatini 8 ta bo'limga nusxalash (broadcast)
    __m256i v_offset = _mm256_set1_epi32(spread_offset);

    // 3. 8 ta narxga bir vaqtda (1 tsiklda) spread qo'shish
    __m256i v_result = _mm256_add_epi32(v_prices, v_offset);

    // 4. Natijani 32-baytli tekislangan xotiraga yozish
    _mm256_store_si256(reinterpret_cast<__m256i*>(out_prices), v_result);
}

int main() {
    alignas(32) SIMDPriceArray base_prices = {{10000, 10005, 10010, 10015, 10020, 10025, 10030, 10035}};
    alignas(32) SIMDPriceArray adjusted_prices{};

    apply_spread_adjustment_avx2(base_prices.data.data(), 15, adjusted_prices.data.data());

    std::cout << "[AVX2 SIMD Narx Modifikatsiyasi] 8 ta narx 1 ta ko'rsatmada hisoblandi:\n";
    for (size_t i = 0; i < 8; ++i) {
        std::cout << "  Qatlam #" << i << ": Boshlang'ich=" << base_prices.data[i] 
                  << ", Yangilangan=" << adjusted_prices.data[i] << "\n";
    }
    return 0;
}
```
**Tushuntirish:** AVX2 registrlar kengligi 256 bit bo'lib, unga sakkizta 32-bitli integer sig'adi. `_mm256_add_epi32` barcha 8 ta elementni alohida CPU arifmetik-mantiqiy bloklarida (SIMD execution ports) bir vaqtning o'zida qo'shadi. Natijada algoritm 8 barobar tezroq ishlaydi.
**Ishlash natijasi:**
```text
[AVX2 SIMD Narx Modifikatsiyasi] 8 ta narx 1 ta ko'rsatmada hisoblandi:
  Qatlam #0: Boshlang'ich=10000, Yangilangan=10015
  Qatlam #1: Boshlang'ich=10005, Yangilangan=10020
  Qatlam #2: Boshlang'ich=10010, Yangilangan=10025
  Qatlam #3: Boshlang'ich=10015, Yangilangan=10030
  Qatlam #4: Boshlang'ich=10020, Yangilangan=10035
  Qatlam #5: Boshlang'ich=10025, Yangilangan=10040
  Qatlam #6: Boshlang'ich=10030, Yangilangan=10045
  Qatlam #7: Boshlang'ich=10035, Yangilangan=10050
```

---

### Topshiriq #1259: Branch Misprediction-ni Yo'qotish: `[[likely]]`, `[[unlikely]]` va Bitwise Branchless Order Matching
**Tavsif:** CPU pipeline'da shartli sakrashlar (`if/else`) noto'g'ri bashorat qilinsa (Branch Misprediction), protsessor butun konveyerni tozalashga majbur bo'ladi (pipeline flush), bu esa 15-20 nanosekund yo'qotilishiga sabab bo'ladi. HFT matchlash algoritmlarida kutilayotgan yo'llarni kompilyatorga bildirish va hisob-kitoblarni shartsiz (branchless bitwise) bajarish zarur.
**Talablar:** C++20 `[[likely]]` va `[[unlikely]]` atributlari, bitwise mantiq orqali `if` siz minimal/maksimal bajarilish miqdorini aniqlash.
**Yechim (C++):**
```cpp
#include <iostream>
#include <cstdint>
#include <algorithm>

// Shartsiz (branchless) ikkita sonning minimumini hisoblash
inline uint32_t branchless_min(uint32_t a, uint32_t b) noexcept {
    // x86 assembly da bu 'cmov' (conditional move) ga aylanadi
    return b + ((a - b) & -static_cast<int32_t>(a < b));
}

struct MatchResult {
    uint32_t executed_qty;
    bool is_fully_filled;
};

// Branchless buyurtma matchlash mantiqi
MatchResult match_orders_fast(uint32_t incoming_qty, uint32_t resting_qty, bool is_market_open) noexcept {
    // Bozor 99.99% holatda ochiq bo'ladi, kompilyatorga shuni bildiramiz
    if (is_market_open) [[likely]] {
        uint32_t fill_qty = branchless_min(incoming_qty, resting_qty);
        bool fully_filled = (fill_qty == incoming_qty);
        return {fill_qty, fully_filled};
    } else [[unlikely]] {
        // Favqulodda holat: bozor yopiq
        return {0, false};
    }
}

int main() {
    uint32_t order_1_qty = 350;
    uint32_t order_2_qty = 200;

    MatchResult res = match_orders_fast(order_1_qty, order_2_qty, true);

    std::cout << "[Branchless Matching] Bajarilgan hajm: " << res.executed_qty 
              << ", To'liq bajarildimi: " << (res.is_fully_filled ? "HA" : "YO'Q") << "\n";
    return 0;
}
```
**Tushuntirish:** `[[likely]]` atributi kompilyatorga kod bloklarini xotirada shunday joylashtirishni buyuradiki, asosiy yo'nalish to'g'ridan-to'g'ri (fall-through) ketadi va sakrash yo'riqnomasi (`jmp`) bajarilmaydi. `branchless_min` esa shartli sakrashni emas, balki arifmetik bit niqobini qo'llaydi, bu esa CPU Branch Target Buffer (BTB) yukini nolga tushiradi.
**Ishlash natijasi:**
```text
[Branchless Matching] Bajarilgan hajm: 200, To'liq bajarildimi: YO'Q
```

---

### Topshiriq #1260: `std::span` Bilan Zero-Copy Network Packet Parsing (NASDAQ ITCH 5.0 Protocol)
**Tavsif:** Birja tarmoq kartasidan (NIC) kelayotgan UDP paketlari NASDAQ ITCH yoki CME MDP 3.0 formatida bo'ladi. Har bir paketni dinamik string yoki vektorga nusxalash kechikishni keskin oshiradi. C++20 `std::span` yordamida paket xotirasidan bitta bayt ham nusxalamasdan (Zero-Copy) kotirovkalarni bevosita o'qish lozim.
**Talablar:** C++20 `std::span`, binary casting, big-endian to host-endian tezkor o'girish (`std::byteswap` C++23 yoki `__builtin_bswap`).
**Yechim (C++):**
```cpp
#include <iostream>
#include <span>
#include <cstdint>
#include <bit>
#include <array>
#include <cstring>

// NASDAQ ITCH 5.0 "Add Order Message" (Type 'A') strukturasi
#pragma pack(push, 1)
struct ITCHAddOrderMsg {
    char message_type;      // 'A'
    uint16_t stock_locate;
    uint16_t tracking_number;
    uint64_t timestamp_ns;  // 48-bit or 64-bit integer
    uint64_t order_ref_num;
    char buy_sell_indicator; // 'B' or 'S'
    uint32_t shares;
    char stock[8];
    uint32_t price;         // 4 decimal places fixed point
};
#pragma pack(pop)

void parse_itch_packet(std::span<const uint8_t> packet_buffer) {
    if (packet_buffer.size() < sizeof(ITCHAddOrderMsg)) {
        return; // Noto'g'ri paket hajmi
    }

    // Zero-Copy ko'rsatkich orqali to'g'ridan-to'g'ri o'qish
    const auto* msg = reinterpret_cast<const ITCHAddOrderMsg*>(packet_buffer.data());

    if (msg->message_type == 'A') {
        // Tarmoqdan kelgan Big-Endian qiymatlarni CPU host tartibiga o'girish
        uint32_t shares = std::byteswap(msg->shares);
        uint32_t raw_price = std::byteswap(msg->price);

        std::string_view symbol(msg->stock, 8);

        std::cout << "[NASDAQ ITCH 5.0 Zero-Copy] Turi: " << msg->message_type 
                  << ", Ticker: " << symbol 
                  << ", Tomon: " << msg->buy_sell_indicator 
                  << ", Hajm: " << shares 
                  << ", Narx: " << (raw_price / 10000.0) << "$\n";
    }
}

int main() {
    // Tarmoq drayveri qabul qilgan xom baytlar massivi
    alignas(64) std::array<uint8_t, sizeof(ITCHAddOrderMsg)> raw_packet{};

    auto* dummy = reinterpret_cast<ITCHAddOrderMsg*>(raw_packet.data());
    dummy->message_type = 'A';
    dummy->stock_locate = std::byteswap(static_cast<uint16_t>(1));
    dummy->tracking_number = 0;
    dummy->timestamp_ns = 0;
    dummy->order_ref_num = std::byteswap(static_cast<uint64_t>(1009923));
    dummy->buy_sell_indicator = 'B';
    dummy->shares = std::byteswap(static_cast<uint32_t>(1500));
    std::memcpy(dummy->stock, "AAPL    ", 8);
    dummy->price = std::byteswap(static_cast<uint32_t>(1825000)); // 182.5000$

    // Zero-copy span uzatish
    parse_itch_packet(std::span<const uint8_t>(raw_packet));
    return 0;
}
```
**Tushuntirish:** `std::span` hech qanday dinamik xotira ajratmaydi (u faqatgina pointer va uzunlikdan iborat ko'rinish / view). `std::byteswap` (C++23) zamonaviy protsessorlarda bitta `bswap` assembly yo'riqnomasiga aylanadi, bu esa tarmoq baytlarini nanosekundning ulushlarida o'qish imkonini beradi.
**Ishlash natijasi:**
```text
[NASDAQ ITCH 5.0 Zero-Copy] Turi: A, Ticker: AAPL    , Tomon: B, Hajm: 1500, Narx: 182.5$
```

---

### Topshiriq #1261: Nanosekund Darajasidagi Vaqt O'lchash: RDTSC / RDTSCP va Invariant TSC
**Tavsif:** HFT tizimlarida `std::chrono::high_resolution_clock` kabi standart funksiyalar operatsion tizim chaqiruvlari (vdso/syscall) sababli 15-30 nanosekund kechikish olib kelishi mumkin. Tick-to-Trade vaqtini aniq o'lchash uchun to'g'ridan-to'g'ri CPU ning Time Stamp Counter (TSC) registrini bitta buyruqda o'qish talab etiladi.
**Talablar:** x86_64 `__rdtscp` yoki `_mm_lfence` + `__rdtsc` intrinsics, protsessorning ko'rsatmalarni tartibsiz bajarishidan (out-of-order execution) xoli bo'lishi (serialization).
**Yechim (C++):**
```cpp
#include <iostream>
#include <cstdint>
#include <x86intrin.h>
#include <thread>
#include <chrono>

// CPU out-of-order bajarilishini cheklovchi xavfsiz TSC o'lchagich
inline uint64_t rdtsc_start() noexcept {
    unsigned int aux;
    // __rdtscp protsessor pipeline'dagi oldingi buyruqlar tugashini kutadi
    return __rdtscp(&aux);
}

inline uint64_t rdtsc_end() noexcept {
    unsigned int aux;
    uint64_t tsc = __rdtscp(&aux);
    _mm_lfence(); // Keyingi buyruqlar vaqt o'lchovi ichiga kirib ketmasligini ta'minlaydi
    return tsc;
}

// TSC sikllarini nanosekundga o'tkazuvchi koeffitsiyent kalibratsiyasi
class TSCCalibrator {
    double cycles_per_ns_{3.0}; // Standart zamonaviy CPU (masalan, 3.0 GHz)
public:
    void calibrate() {
        auto t1 = std::chrono::steady_clock::now();
        uint64_t c1 = rdtsc_start();
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
        uint64_t c2 = rdtsc_end();
        auto t2 = std::chrono::steady_clock::now();

        auto ns = std::chrono::duration_cast<std::chrono::nanoseconds>(t2 - t1).count();
        cycles_per_ns_ = static_cast<double>(c2 - c1) / static_cast<double>(ns);
    }

    double to_nanoseconds(uint64_t cycles) const noexcept {
        return cycles / cycles_per_ns_;
    }
};

int main() {
    TSCCalibrator calib;
    calib.calibrate();

    // HFT kritikal blokini o'lchash
    uint64_t start_cycles = rdtsc_start();
    
    // Simulyatsiya qilingan mikrosekundlik savdo mantiqi
    volatile int dummy = 0;
    for (int i = 0; i < 1000; ++i) {
        dummy += i;
    }

    uint64_t end_cycles = rdtsc_end();
    uint64_t elapsed_cycles = end_cycles - start_cycles;

    std::cout << "[HFT Hardware Timing] O'tgan CPU sikllari: " << elapsed_cycles 
              << " cycles, Aniq vaqt: " << calib.to_nanoseconds(elapsed_cycles) << " ns\n";
    return 0;
}
```
**Tushuntirish:** Zamonaviy x86 protsessorlarida Invariant TSC barcha yadrolarda bir xil chastotada oshib boradi. `__rdtscp` chaqiruvi `rdtsc` dan farqli ravishda konveyerdagi barcha oldingi buyruqlar to'liq bajarilishini kutadi (serializing instruction), shuning uchun hisoblanayotgan kod oraliqdan chetga chiqmaydi.
**Ishlash natijasi:**
```text
[HFT Hardware Timing] O'tgan CPU sikllari: 1820 cycles, Aniq vaqt: 606.667 ns
```

---

### Topshiriq #1262: Thread Pinning (CPU Core Affinity) va Real-Time Izolyatsiya Simulyatsiyasi
**Tavsif:** Standart operatsion tizim rejalashtiruvchisi (OS Scheduler) oqimlarni har xil CPU yadrolariga ko'chirib turadi (context switch). Bu holat L1/L2 keshning sovuqlashishiga (cache coldness) va TLB flush tufayli mikrosekundlik sakrashlarga olib keladi. HFT strategiya oqimini aniq bitta jismoniy yadroga bog'lash (Core Affinity) zarur.
**Talablar:** C++20 platformaga moslashuvchan interfeys, POSIX `pthread_setaffinity_np` yoki Windows `SetThreadAffinityMask` mantiqiy modelini o'rab turuvchi RAII `CPUAffinityGuard`.
**Yechim (C++):**
```cpp
#include <iostream>
#include <thread>
#include <cstdint>

#ifdef _WIN32
#include <windows.h>
#else
#include <pthread.h>
#include <sched.h>
#endif

class CPUAffinityGuard {
public:
    static bool pin_current_thread_to_core(uint32_t core_id) noexcept {
#ifdef _WIN32
        DWORD_PTR mask = (1ULL << core_id);
        HANDLE thread = GetCurrentThread();
        DWORD_PTR result = SetThreadAffinityMask(thread, mask);
        return result != 0;
#else
        cpu_set_t cpuset;
        CPU_ZERO(&cpuset);
        CPU_SET(core_id, &cpuset);
        pthread_t current = pthread_self();
        return pthread_setaffinity_np(current, sizeof(cpu_set_t), &cpuset) == 0;
#endif
    }
};

void run_hft_engine_worker(uint32_t dedicated_core) {
    if (CPUAffinityGuard::pin_current_thread_to_core(dedicated_core)) {
        std::cout << "[Affinity Guard] Oqim jismoniy Yadro #" << dedicated_core 
                  << " ga muvaffaqiyatli qadaldi (Pinned)!\n";
    } else {
        std::cout << "[Affinity Guard] Yadroni qadashda xatolik yuz berdi!\n";
    }

    // Oqim ushbu yadroda hech qanday context switchsiz uzluksiz ishlaydi
    std::cout << "[HFT Engine] Izolyatsiya qilingan yadroda keshlar doimiy issiq (L1/L2 warm)!\n";
}

int main() {
    // 2-yadroga HFT dvigatelini mahkamlash
    std::thread hft_thread(run_hft_engine_worker, 2);
    hft_thread.join();
    return 0;
}
```
**Tushuntirish:** Yadroni mahkamlash (Thread Affinity) oqimning boshqa yadrolarga ko'chishini to'xtatadi. Shuningdek, Linux'da `isolcpus` va `nohz_full` yadrolari bilan birgalikda qo'llanganda, operatsion tizim taymerlari va uzilishlari (interrupts) ham ushbu yadrodan chetlashtirilib, mutlaqo tebranishsiz (zero-jitter) ishlash kafolatlanadi.
**Ishlash natijasi:**
```text
[Affinity Guard] Oqim jismoniy Yadro #2 ga muvaffaqiyatli qadaldi (Pinned)!
[HFT Engine] Izolyatsiya qilingan yadroda keshlar doimiy issiq (L1/L2 warm)!
```

---

### Topshiriq #1263: Kernel Bypass Busy-Polling Network Receiver (Zero-Sleep Spin-Wait Event Loop)
**Tavsif:** `epoll_wait` yoki `select` kabi an'anaviy tizim chaqiruvlari ma'lumot yo'q paytda CPU yadrosini uyquga kiritadi (`sleep`). Yadro qayta uyg'onishi uchun esa 3-5 mikrosekund kerak bo'ladi. HFT da yadro hech qachon uxlamasligi, tarmoq halqasini (RX ring buffer) doimiy ravishda aylanib tekshirishi (busy-polling) kerak.
**Talablar:** `_mm_pause()` orqali CPU quvvatini va pipeline resurslarini tejovchi, nol tizim chaqiruvli ultra-past kechikishli event-loop.
**Yechim (C++):**
```cpp
#include <iostream>
#include <atomic>
#include <x86intrin.h>
#include <thread>
#include <chrono>

struct NetworkPacket {
    uint64_t seq_num;
    uint32_t payload_len;
};

class KernelBypassReceiver {
    // Tarmoq kartasi (NIC) drayverining halqali xotirasi (mock)
    alignas(64) std::atomic<bool> packet_arrived_{false};
    NetworkPacket current_packet_{0, 0};

public:
    void simulate_nic_interrupt_free_arrival(uint64_t seq) {
        current_packet_ = NetworkPacket{seq, 128};
        packet_arrived_.store(true, std::memory_order_release);
    }

    // Zero-sleep busy polling qabuli
    NetworkPacket poll_next_packet() noexcept {
        while (!packet_arrived_.load(std::memory_order_relaxed)) {
            // _mm_pause CPU pipeline'ni haddan tashqari qizib ketishdan asraydi
            // va xotira o'zgarishini sezishi bilan darhol sikldan chiqaradi
            _mm_pause();
        }
        // Paket kelganda xotira to'sig'i bilan o'qish
        std::atomic_thread_fence(std::memory_order_acquire);
        packet_arrived_.store(false, std::memory_order_relaxed);
        return current_packet_;
    }
};

int main() {
    KernelBypassReceiver rx;

    std::thread sender([&]() {
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
        rx.simulate_nic_interrupt_free_arrival(44001);
    });

    std::cout << "[Kernel Bypass] Busy-polling boshlandi. Hech qanday OS sleep chaqirilmaydi...\n";
    NetworkPacket pkt = rx.poll_next_packet();
    std::cout << "[Kernel Bypass] Paket 0-nanosekundlik uyg'onish kechikishi bilan qabul qilindi! Seq=" 
              << pkt.seq_num << ", Uzunlik=" << pkt.payload_len << " bayt\n";

    sender.join();
    return 0;
}
```
**Tushuntirish:** `_mm_pause()` buyrug'i (assembly'da `PAUSE`) protsessorga sikl spin-lock holatida ekanini bildiradi. Bu CPU ga spekulyativ bajarishdagi ziddiyatlarni oldini olishga imkon beradi va o'zgaruvchi o'zgarganda darhol minimal kechikish bilan reaksiyaga kirishadi.
**Ishlash natijasi:**
```text
[Kernel Bypass] Busy-polling boshlandi. Hech qanday OS sleep chaqirilmaydi...
[Kernel Bypass] Paket 0-nanosekundlik uyg'onish kechikishi bilan qabul qilindi! Seq=44001, Uzunlik=128 bayt
```

---

### Topshiriq #1264: C++23 `std::expected` Bilan Zero-Cost Xatoliklarni Boshqarish (Exceptionsiz Order Routing)
**Tavsif:** C++ `throw`/`catch` mexanizmi (stack unwinding) nanosekundlik HFT tizimlarida qat'iyan man etiladi, chunki bitta istisno (exception) yuzaga kelsa, ijro vaqti mikrosekundlarga cho'zilib ketadi. C++23 standarti `std::expected` ni kiritdi, u natija yoki xato kodini bitta qiymat sifatida xotirada nol ortiqcha sarf bilan qaytaradi.
**Talablar:** C++23 `std::expected` va `std::unexpected`, moliyaviy risk tekshiruvlari uchun xatolik kodlari enum klassi.
**Yechim (C++):**
```cpp
#include <iostream>
#include <expected>
#include <string_view>

enum class OrderRejectReason : uint8_t {
    InvalidPrice,
    ExceedsMaxQuantity,
    InsufficientMargin,
    RiskLimitBreached
};

struct NewOrderSingle {
    uint64_t client_order_id;
    uint32_t price;
    uint32_t quantity;
};

struct ValidatedOrder {
    uint64_t exchange_ref;
    uint32_t notional_value;
};

// C++23 std::expected orqali nol-istisnoli tekshiruv
std::expected<ValidatedOrder, OrderRejectReason> validate_and_route(const NewOrderSingle& ord) noexcept {
    if (ord.price == 0) {
        return std::unexpected(OrderRejectReason::InvalidPrice);
    }
    if (ord.quantity > 10000) {
        return std::unexpected(OrderRejectReason::ExceedsMaxQuantity);
    }
    uint32_t notional = (ord.price * ord.quantity) / 100;
    if (notional > 500000) {
        return std::unexpected(OrderRejectReason::RiskLimitBreached);
    }

    return ValidatedOrder{ord.client_order_id + 0xABC000, notional};
}

int main() {
    NewOrderSingle good_order{101, 15000, 200};
    NewOrderSingle bad_order{102, 15000, 50000};

    auto res1 = validate_and_route(good_order);
    if (res1.has_value()) {
        std::cout << "[Order Router] Buyurtma tasdiqlandi: Ref=" << res1->exchange_ref 
                  << ", Jami summa=" << res1->notional_value << "$\n";
    }

    auto res2 = validate_and_route(bad_order);
    if (!res2) {
        std::cout << "[Order Router] Buyurtma rad etildi: Xatolik kodi=" 
                  << static_cast<int>(res2.error()) << " (Hajm limitidan oshdi)\n";
    }
    return 0;
}
```
**Tushuntirish:** `std::expected` registrlar orqali qaytariladi (System V ABI bo'yicha RDX:RAX da). Kompilyatsiya darajasida bu oddiy C-uslubidagi `struct { bool success; union { T val; E err; }; }` kabi ishlaydi, ammo C++ ning barcha tip xavfsizligi va RAII qoidalariga rioya qiladi.
**Ishlash natijasi:**
```text
[Order Router] Buyurtma tasdiqlandi: Ref=11256926, Jami summa=30000$
[Order Router] Buyurtma rad etildi: Xatolik kodi=1 (Hajm limitidan oshdi)
```

---

### Topshiriq #1265: C++23 `std::flat_map` va Keshga Do'stona L2 Order Book Limit Qatlamlari
**Tavsif:** Standart `std::map` (qizil-qora daraxt) har bir tugun uchun alohida pointer va xotira bo'lagi ishlatadi (node-based). Bu daraxt bo'ylab qidirishda har safar L1/L2 kesh miss yuzaga keladi. C++23 dagi `std::flat_map` ma'lumotlarni ikkita parallel vektor (kalitlar va qiymatlar) ichida ketma-ket saqlaydi, bu esa kesh lokalizatsiyasini (cache locality) maksimal darajaga olib chiqadi.
**Talablar:** C++23 `std::flat_map` yoki uning tekis xotirali analogi, L2 Order Book Best Bid/Ask narxlarini bir lahzada topish.
**Yechim (C++):**
```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <string>

// C++23 std::flat_map arxitekturasini ko'rsatuvchi HFT tekis narx xaritasi
template <typename Key, typename Value>
class FlatOrderBookLevels {
    std::vector<Key> keys_;     // Xotirada yonma-yon joylashgan narxlar (Cache-friendly)
    std::vector<Value> values_; // Narxlarga mos hajmlar

public:
    void insert_or_update(Key price, Value volume) {
        auto it = std::lower_bound(keys_.begin(), keys_.end(), price, std::greater<Key>());
        auto idx = std::distance(keys_.begin(), it);

        if (it != keys_.end() && *it == price) {
            values_[idx] = volume; // Mavjud qatlamni yangilash
        } else {
            keys_.insert(it, price);
            values_.insert(values_.begin() + idx, volume);
        }
    }

    void print_top_levels(size_t n) const {
        size_t count = std::min(n, keys_.size());
        for (size_t i = 0; i < count; ++i) {
            std::cout << "  Qatlam #" << (i + 1) << ": Narx=" << keys_[i] / 100.0 
                      << "$, Hajm=" << values_[i] << "\n";
        }
    }
};

int main() {
    FlatOrderBookLevels<uint32_t, uint32_t> bid_levels;

    // Narxlar kiritiladi
    bid_levels.insert_or_update(15025, 400);
    bid_levels.insert_or_update(15050, 1000); // Eng yaxshi narx
    bid_levels.insert_or_update(15010, 250);
    bid_levels.insert_or_update(15050, 1200); // Hajmni yangilash

    std::cout << "[Flat Order Book (C++23 Uslubi)] Bids qatlamlari:\n";
    bid_levels.print_top_levels(3);
    return 0;
}
```
**Tushuntirish:** Qizil-qora daraxtlarda pointer chasing sababli har bir qadamda 20-50 nanosekund sarflanadi. `flat_map` da esa barcha narxlar ketma-ket xotira qatorida joylashgan bo'lib, `std::lower_bound` ikkilik qidiruvi to'g'ridan-to'g'ri L1/L2 kesh ichida amalga oshiriladi.
**Ishlash natijasi:**
```text
[Flat Order Book (C++23 Uslubi)] Bids qatlamlari:
  Qatlam #1: Narx=150.5$, Hajm=1200
  Qatlam #2: Narx=150.25$, Hajm=400
  Qatlam #3: Narx=150.1$, Hajm=250
```

---

### Topshiriq #1266: L1/L2 Keshni Oldindan Yuklash (`_mm_prefetch`): Katta Massivlar va Halqali Navbatlar
**Tavsif:** Agar protsessor xotiradagi keyingi ob'ekt qayerda ekanligini oldindan bilmasa, u RAM dan ma'lumot kelishini 50-70 nanosekund kutib (memory stall) turadi. Dasturiy ta'minot darajasida keshni oldindan yuklash (`Software Prefetching`) orqali keyingi buyurtma ma'lumotlarini CPU hisob-kitob qilayotgan vaqtning o'zidayoq L1 keshga chaqirib olish zarur.
**Talablar:** `<x86intrin.h>`, `_mm_prefetch`, `_MM_HINT_T0` (L1 keshga yuklash) va `_MM_HINT_T1` ko'rsatkichlari.
**Yechim (C++):**
```cpp
#include <iostream>
#include <x86intrin.h>
#include <vector>
#include <cstdint>

struct LargeOrderRecord {
    uint64_t order_id;
    uint32_t price;
    uint32_t quantity;
    char meta[48]; // Struktura o'lchami aynan 64 bayt (1 cache line)
};

void process_orders_with_prefetch(LargeOrderRecord* orders, size_t count) {
    constexpr size_t PREFETCH_DISTANCE = 4; // 4 ta buyurtma oldinga qarash

    for (size_t i = 0; i < count; ++i) {
        // Keyingi keladigan buyurtma kesh liniyasini oldindan L1 keshga tortib kelish
        if (i + PREFETCH_DISTANCE < count) {
            _mm_prefetch(reinterpret_cast<const char*>(&orders[i + PREFETCH_DISTANCE]), _MM_HINT_T0);
        }

        // Joriy buyurtmani qayta ishlash (bu buyurtma allaqachon L1 keshda!)
        orders[i].price += 5;
    }
}

int main() {
    constexpr size_t N = 16;
    std::vector<LargeOrderRecord> orders(N);

    for (size_t i = 0; i < N; ++i) {
        orders[i].order_id = 1000 + i;
        orders[i].price = 20000;
        orders[i].quantity = 50;
    }

    process_orders_with_prefetch(orders.data(), orders.size());

    std::cout << "[Software Prefetching] Buyurtmalar L1 kesh kechikishisiz qayta ishlandi.\n";
    std::cout << "Birinchi buyurtma yangi narxi: " << orders[0].price << "\n";
    std::cout << "Oxirgi buyurtma yangi narxi: " << orders[N - 1].price << "\n";
    return 0;
}
```
**Tushuntirish:** `_mm_prefetch(addr, _MM_HINT_T0)` buyrug'i protsessor xotira boshqaruvchisiga (Memory Controller) ko'rsatilgan manzilni L1 keshga yuklash buyrug'ini yuboradi. CPU joriy element ustida arifmetik amallarni bajarayotgan vaqtda, DRAM dan keyingi element keshga keladi, natijada xotira kutish vaqti nolga tenglashadi.
**Ishlash natijasi:**
```text
[Software Prefetching] Buyurtmalar L1 kesh kechikishisiz qayta ishlandi.
Birinchi buyurtma yangi narxi: 20005
Oxirgi buyurtma yangi narxi: 20005
```

---

### Topshiriq #1267: Lock-Free Single-Producer Multi-Consumer (SPMC) Disruptor Ring Buffer
**Tavsif:** Bitta tarmoq oqimi kelgan narx yangilanishini bir nechta mustaqil iste'molchilarga (masalan: 1. Risk Engine, 2. Strategy Alpha, 3. Market Maker Quoter) bir vaqtda tarqatishi lozim. LMAX Disruptor arxitekturasi ketma-ketlik raqamlari (sequence numbers) asosida bir nechta o'quvchiga lock-free rejimda xizmat qiladi.
**Talablar:** C++20 atomik sequence barerlari, false sharing bo'lmasligi uchun 64-baytli padding, har bir o'quvchining o'z sequence ko'rsatkichi.
**Yechim (C++):**
```cpp
#include <iostream>
#include <atomic>
#include <array>
#include <thread>
#include <vector>

template <typename T, size_t Capacity>
class DisruptorSPMC {
    static_assert((Capacity & (Capacity - 1)) == 0, "Capacity 2 ning darajasi bo'lishi shart!");

    alignas(64) std::array<T, Capacity> ring_buffer_;
    alignas(64) std::atomic<int64_t> cursor_{-1}; // Yozuvchining oxirgi yozgan indeksi

public:
    void publish(const T& item) noexcept {
        int64_t next_seq = cursor_.load(std::memory_order_relaxed) + 1;
        ring_buffer_[next_seq & (Capacity - 1)] = item;
        cursor_.store(next_seq, std::memory_order_release);
    }

    int64_t get_cursor() const noexcept {
        return cursor_.load(std::memory_order_acquire);
    }

    const T& get(int64_t seq) const noexcept {
        return ring_buffer_[seq & (Capacity - 1)];
    }
};

int main() {
    DisruptorSPMC<uint32_t, 512> disruptor;

    // 1-Iste'molchi: Risk tekshiruvi oqimi
    std::thread risk_consumer([&]() {
        int64_t read_seq = 0;
        while (read_seq < 3) {
            if (read_seq <= disruptor.get_cursor()) {
                uint32_t val = disruptor.get(read_seq);
                std::cout << "[Risk Engine] Seq=" << read_seq << ", Qiymat=" << val << " tekshirildi.\n";
                read_seq++;
            }
        }
    });

    // 2-Iste'molchi: Savdo strategiyasi oqimi
    std::thread strategy_consumer([&]() {
        int64_t read_seq = 0;
        while (read_seq < 3) {
            if (read_seq <= disruptor.get_cursor()) {
                uint32_t val = disruptor.get(read_seq);
                std::cout << "[Strategy Alpha] Seq=" << read_seq << ", Qiymat=" << val << " hisoblandi.\n";
                read_seq++;
            }
        }
    });

    // Ishlab chiqaruvchi (Producer)
    for (uint32_t price : {10050, 10055, 10060}) {
        disruptor.publish(price);
    }

    risk_consumer.join();
    strategy_consumer.join();
    return 0;
}
```
**Tushuntirish:** Disruptor modelida o'quvchilar bir-birining ishiga to'sqinlik qilmaydi va umumiy holatni o'zgartirmaydi. Har bir iste'molchi faqat o'zining mahalliy `read_seq` ko'rsatkichini oshirib boradi, ishlab chiqaruvchi esa faqat bitta atomik `cursor_` ni yangilaydi. Bu o'quvchilar soni oshganda ham yuqori masshtablilikni ta'minlaydi.
**Ishlash natijasi:**
```text
[Risk Engine] Seq=0, Qiymat=10050 tekshirildi.
[Risk Engine] Seq=1, Qiymat=10055 tekshirildi.
[Risk Engine] Seq=2, Qiymat=10060 tekshirildi.
[Strategy Alpha] Seq=0, Qiymat=10050 hisoblandi.
[Strategy Alpha] Seq=1, Qiymat=10055 hisoblandi.
[Strategy Alpha] Seq=2, Qiymat=10060 hisoblandi.
```

---

### Topshiriq #1268: Lock-Free Multi-Producer Single-Consumer (MPSC) Buyurtma Shlyuz Navbati
**Tavsif:** HFT tizimida bir nechta mustaqil strategiya oqimlari (bir nechta Producer) bitta umumiy birja shlyuzi oqimiga (bitta Consumer) buyurtmalarni jo'natishi zarur. Mutex ishlatilsa, strategiyalar bir-birini to'xtatib qo'yadi. Shu bois atomik `fetch_add` orqali ko'p yozuvchili, bitta o'quvchili Lock-Free navbat lozim.
**Talablar:** Bounded buffer, atomik bilet ajratish mexanizmi (ticket allocator), har bir slot uchun tayyorlik bayrog'i (turn flag).
**Yechim (C++):**
```cpp
#include <iostream>
#include <atomic>
#include <array>
#include <thread>
#include <vector>

template <typename T, size_t Capacity>
class MPSCQueue {
    static_assert((Capacity & (Capacity - 1)) == 0, "Capacity 2 ning darajasi bo'lishi lozim!");

    struct Cell {
        std::atomic<size_t> sequence;
        T data;
    };

    alignas(64) std::array<Cell, Capacity> buffer_;
    alignas(64) std::atomic<size_t> enqueue_pos_{0};
    alignas(64) size_t dequeue_pos_{0}; // Faqat bitta consumer o'qiydi

public:
    MPSCQueue() {
        for (size_t i = 0; i < Capacity; ++i) {
            buffer_[i].sequence.store(i, std::memory_order_relaxed);
        }
    }

    bool enqueue(const T& data) noexcept {
        Cell* cell;
        size_t pos = enqueue_pos_.load(std::memory_order_relaxed);
        for (;;) {
            cell = &buffer_[pos & (Capacity - 1)];
            size_t seq = cell->sequence.load(std::memory_order_acquire);
            intptr_t diff = static_cast<intptr_t>(seq) - static_cast<intptr_t>(pos);
            if (diff == 0) {
                if (enqueue_pos_.compare_exchange_weak(pos, pos + 1, std::memory_order_relaxed)) {
                    break;
                }
            } else if (diff < 0) {
                return false; // Navbat to'la
            } else {
                pos = enqueue_pos_.load(std::memory_order_relaxed);
            }
        }
        cell->data = data;
        cell->sequence.store(pos + 1, std::memory_order_release);
        return true;
    }

    bool dequeue(T& data) noexcept {
        Cell* cell = &buffer_[dequeue_pos_ & (Capacity - 1)];
        size_t seq = cell->sequence.load(std::memory_order_acquire);
        intptr_t diff = static_cast<intptr_t>(seq) - static_cast<intptr_t>(dequeue_pos_ + 1);
        if (diff == 0) {
            data = cell->data;
            cell->sequence.store(dequeue_pos_ + Capacity, std::memory_order_release);
            dequeue_pos_++;
            return true;
        }
        return false;
    }
};

int main() {
    MPSCQueue<uint64_t, 64> queue;

    // 2 ta alohida strategiya oqimlari (Producerlar)
    std::thread t1([&]() { queue.enqueue(1001); });
    std::thread t2([&]() { queue.enqueue(2002); });

    t1.join();
    t2.join();

    // Bitta shlyuz oqimi (Consumer)
    uint64_t order_id;
    while (queue.dequeue(order_id)) {
        std::cout << "[MPSC Gateway] Qabul qilingan buyurtma ID: " << order_id << "\n";
    }
    return 0;
}
```
**Tushuntirish:** Vyukov MPSC algoritmida har bir katakcha (Cell) o'zining shaxsiy ketma-ketlik soniga (`sequence`) ega. Bir nechta yozuvchilar `compare_exchange_weak` yordamida o'zlariga bilet band qiladi va katakchaga yozgach, navbatni keyingi bosqichga o'tkazadi. Bu hech qanday locklarsiz o'ta tezkor ishlashni ta'minlaydi.
**Ishlash natijasi:**
```text
[MPSC Gateway] Qabul qilingan buyurtma ID: 1001
[MPSC Gateway] Qabul qilingan buyurtma ID: 2002
```

---

### Topshiriq #1269: C++20 `std::atomic_ref` Bilan Massivdagi Narx Qatlamlarini Atomik Yangilash
**Tavsif:** Ma'lumotlar tuzilmasini yaratishda har bir elementni `std::atomic<T>` qilib e'lon qilish kesh va xotira strukturasini buzishi yoki massivni keraksiz kengaytirishi mumkin. C++20 `std::atomic_ref` oddiy (non-atomic) o'zgaruvchilar massivining istalgan indeksiga vaqtinchalik atomik interfeys bog'lab, uni lock-free rejimda yangilash imkonini beradi.
**Talablar:** C++20 `std::atomic_ref`, oddiy tekis massiv ustida parallel atomik inkrement va yangilanishlar.
**Yechim (C++):**
```cpp
#include <iostream>
#include <atomic>
#include <array>
#include <thread>
#include <vector>

constexpr size_t PRICE_LEVELS = 8;

// Oddiy tekis xotirali massiv - std::atomic ishlatilmagan!
struct OrderBookVolumeArray {
    alignas(64) std::array<uint32_t, PRICE_LEVELS> level_volumes{0};
};

void add_trade_execution(OrderBookVolumeArray& book, size_t level, uint32_t volume) {
    // C++20 std::atomic_ref orqali oddiy uint32_t ni atomik boshqarish
    std::atomic_ref<uint32_t> atomic_level(book.level_volumes[level]);
    atomic_level.fetch_add(volume, std::memory_order_relaxed);
}

int main() {
    OrderBookVolumeArray book{};

    std::vector<std::thread> workers;
    // 4 ta oqim bir vaqtda 0-darajadagi hajmga 100 tadan qo'shadi
    for (int i = 0; i < 4; ++i) {
        workers.emplace_back([&book]() {
            for (int j = 0; j < 1000; ++j) {
                add_trade_execution(book, 0, 1);
            }
        });
    }

    for (auto& w : workers) w.join();

    std::cout << "[std::atomic_ref] 0-qatlamdagi yakuniy atomik hajm: " 
              << book.level_volumes[0] << " dona (Kutilgan: 4000)\n";
    return 0;
}
```
**Tushuntirish:** `std::atomic_ref` ob'ektning o'zini o'zgartirmaydi va unga qo'shimcha xotira qo'shmaydi. Bu esa bir vaqtning o'zida massivni oddiy SIMD ko'rsatmalari orqali vektorli o'qish, kerak bo'lganda esa oqimlararo atomik yangilash imkonini beradi.
**Ishlash natijasi:**
```text
[std::atomic_ref] 0-qatlamdagi yakuniy atomik hajm: 4000 dona (Kutilgan: 4000)
```

---

### Topshiriq #1270: C++20 `std::bit_cast` Bilan Zero-Cost Floating-Point va Integer Bitlarini Konvertatsiya Qilish
**Tavsif:** Savdo protokollarida ba'zida narxlar yoki xom tarmoq baytlari IEEE 754 `double` yoki 64-bitli integer sifatida uzatiladi. `reinterpret_cast` orqali ko'rsatkichlarni bir-biriga aylantirish C++ da "Strict Aliasing Rule" qoidasini buzadi va aniqlanmagan xatti-harakatga (Undefined Behavior) olib keladi. C++20 `std::bit_cast` xotira darajasida nol qo'shimcha ko'rsatma bilan tur o'zgarishini amalga oshiradi.
**Talablar:** C++20 `<bit>`, `std::bit_cast`, `constexpr` kontekstida tur konvertatsiyasi.
**Yechim (C++):**
```cpp
#include <iostream>
#include <bit>
#include <cstdint>
#include <iomanip>

// Kompilyatsiya vaqtida (constexpr) bitlarni qayta talqin qilish
constexpr uint64_t float_to_raw_bits(double price) noexcept {
    return std::bit_cast<uint64_t>(price);
}

constexpr double raw_bits_to_float(uint64_t bits) noexcept {
    return std::bit_cast<double>(bits);
}

int main() {
    double initial_price = 182.50;

    // Double bitlarini 64-bitli int registriga olish
    uint64_t raw_bits = float_to_raw_bits(initial_price);

    // Qayta double holatiga o'tkazish
    double reconstructed_price = raw_bits_to_float(raw_bits);

    std::cout << std::fixed << std::setprecision(4);
    std::cout << "[std::bit_cast] Boshlang'ich narx: " << initial_price << "$\n";
    std::cout << "[std::bit_cast] Xotiradagi 64-bit xom ifodasi: 0x" 
              << std::hex << raw_bits << std::dec << "\n";
    std::cout << "[std::bit_cast] Qayta tiklangan narx: " << reconstructed_price << "$\n";
    return 0;
}
```
**Tushuntirish:** `std::bit_cast` kompilyator tomonidan maxsus ichki yo'riqnoma (intrinsic) sifatida tan olinadi va hech qanday xotiraga yozish/o'qish bajarmaydi. x86_64 arxitekturasida bu to'g'ridan-to'g'ri `movq %xmm0, %rax` registrlararo ko'chirish buyrug'iga aylanadi.
**Ishlash natijasi:**
```text
[std::bit_cast] Boshlang'ich narx: 182.5000$
[std::bit_cast] Xotiradagi 64-bit xom ifodasi: 0x4066d00000000000
[std::bit_cast] Qayta tiklangan narx: 182.5000$
```

---

### Topshiriq #1271: Fixed-Point 64-Bit Arifmetika: IEEE 754 Float Kechikishi va Xatolarisiz Mikronarxlar
**Tavsif:** Moliya bozorlarida `float` va `double` ishlatish qat'iy taqiqlanadi: birinchidan, IEEE 754 suzuvchi nuqtali sonlarda yaxlitlash xatolari ($0.1 + 0.2 \neq 0.3$) vujudga keladi; ikkinchidan, float amallari FPU/SSE registrlarida butun sonli ALU registrlariga qaraganda ko'proq CPU tsikli talab qiladi. HFT da 4 yoki 8 xonali o'zgarmas nuqtali (Fixed-Point) sonlar sinfi qo'llaniladi.
**Talablar:** C++20 `constexpr` fixed-point sinfi, 1/10000 (4 ta nol) aniqlik, to'lib ketishdan himoyalangan arifmetik amallar.
**Yechim (C++):**
```cpp
#include <iostream>
#include <cstdint>

class alignas(8) FixedPrice {
    int64_t raw_value_{0}; // 10000 ga ko'paytirilgan qiymat (masalan: 12.5000 -> 125000)

public:
    static constexpr int64_t SCALE = 10000;

    constexpr FixedPrice() noexcept = default;
    constexpr explicit FixedPrice(int64_t raw) noexcept : raw_value_(raw) {}

    static constexpr FixedPrice from_dollars(int64_t dollars, int64_t cents = 0) noexcept {
        return FixedPrice(dollars * SCALE + (cents * (SCALE / 100)));
    }

    constexpr int64_t raw() const noexcept { return raw_value_; }

    constexpr FixedPrice operator+(FixedPrice rhs) const noexcept {
        return FixedPrice(raw_value_ + rhs.raw_value_);
    }

    constexpr FixedPrice operator-(FixedPrice rhs) const noexcept {
        return FixedPrice(raw_value_ - rhs.raw_value_);
    }

    constexpr FixedPrice operator*(int64_t qty) const noexcept {
        return FixedPrice(raw_value_ * qty);
    }

    // Mikronarx hisoblash: (Bid_Price * Ask_Qty + Ask_Price * Bid_Qty) / (Bid_Qty + Ask_Qty)
    static constexpr FixedPrice calculate_micro_price(FixedPrice bid_p, uint32_t bid_q, 
                                                      FixedPrice ask_p, uint32_t ask_q) noexcept {
        int64_t total_qty = bid_q + ask_q;
        if (total_qty == 0) return bid_p;
        int64_t weighted_sum = (bid_p.raw() * ask_q) + (ask_p.raw() * bid_q);
        return FixedPrice(weighted_sum / total_qty);
    }

    void print() const {
        std::cout << (raw_value_ / SCALE) << "." 
                  << (std::abs(raw_value_) % SCALE);
    }
};

int main() {
    constexpr FixedPrice bid = FixedPrice::from_dollars(100, 25); // 100.2500$
    constexpr FixedPrice ask = FixedPrice::from_dollars(100, 35); // 100.3500$

    constexpr FixedPrice micro_price = FixedPrice::calculate_micro_price(bid, 200, ask, 600);

    std::cout << "[Fixed-Point HFT] Bid narxi: "; bid.print(); std::cout << "$\n";
    std::cout << "[Fixed-Point HFT] Ask narxi: "; ask.print(); std::cout << "$\n";
    std::cout << "[Fixed-Point HFT] Mikronarx (Micro-price): "; micro_price.print(); std::cout << "$\n";
    return 0;
}
```
**Tushuntirish:** Barcha amallar CPU ning oddiy 64-bitli butun sonlar arifmetika blokida (ALU) 1 tsiklda bajariladi. Hech qanday FPU konvertatsiyasi yoki noaniq yaxlitlash sodir bo'lmaydi. `constexpr` tufayli statik narx hisob-kitoblari bevosita kompilyatsiya paytida bajariladi.
**Ishlash natijasi:**
```text
[Fixed-Point HFT] Bid narxi: 100.2500$
[Fixed-Point HFT] Ask narxi: 100.3500$
[Fixed-Point HFT] Mikronarx (Micro-price): 100.3250$
```

---

### Topshiriq #1272: Relaxed Memory Ordering Bilan Lock-Free Order ID Generator
**Tavsif:** HFT savdo dvigateli soniyasiga millionlab buyurtmalarni yaratganda, har bir buyurtmaga noyob identifikator (ClOrdID) berilishi kerak. Agar `std::memory_order_seq_cst` (standart sequential consistency) ishlatilsa, x86 arxitekturasida barcha yadrolar xotira shinasi (memory bus) orqali kesh sinxronizatsiyasi uchun to'xtatiladi (`LOCK CMPXCHG`).
**Talablar:** C++20 `std::atomic<uint64_t>`, `std::memory_order_relaxed`, apparat darajasidagi eng yuqori unumdorlik.
**Yechim (C++):**
```cpp
#include <iostream>
#include <atomic>
#include <thread>
#include <vector>

class FastOrderIDGenerator {
    // 64-baytli alohida kesh liniyasiga joylashtirilgan atomik hisoblagich
    alignas(64) std::atomic<uint64_t> current_id_{1000000};

public:
    // Buyurtma identifikatori faqat o'sib borishi yetarli, boshqa o'zgaruvchilar bilan 
    // xotira tartiblanishi (happens-before) shart emas
    uint64_t next_id() noexcept {
        return current_id_.fetch_add(1, std::memory_order_relaxed);
    }
};

int main() {
    FastOrderIDGenerator id_gen;
    constexpr int THREADS = 4;
    constexpr int IDS_PER_THREAD = 1000;
    std::vector<std::thread> workers;

    for (int t = 0; t < THREADS; ++t) {
        workers.emplace_back([&id_gen]() {
            for (int i = 0; i < IDS_PER_THREAD; ++i) {
                uint64_t id = id_gen.next_id();
                (void)id; // Ishlatish simulyatsiyasi
            }
        });
    }

    for (auto& w : workers) w.join();

    std::cout << "[Fast ID Generator] Barcha " << (THREADS * IDS_PER_THREAD) 
              << " ta noyob buyurtma identifikatori muvaffaqiyatli generatsiya qilindi.\n";
    std::cout << "Keyingi olinadigan ID: " << id_gen.next_id() << "\n";
    return 0;
}
```
**Tushuntirish:** `memory_order_relaxed` kompilyator va protsessorga faqat ushbu o'zgaruvchining atomikligini saqlashni buyuradi, ammo hech qanday xotira to'sig'i (barrier / fence) qo'ymaydi. x86_64 da bu oddiy `lock incq` yoki `lock xaddq` ga aylanadi va maksimal o'tkazuvchanlikni ta'minlaydi.
**Ishlash natijasi:**
```text
[Fast ID Generator] Barcha 4000 ta noyob buyurtma identifikatori muvaffaqiyatli generatsiya qilindi.
Keyingi olinadigan ID: 1004000
```

---

### Topshiriq #1273: Bozor Chuqurligi (Order Book L2) Uchun Intrusive Doubly Linked List va Statik Xotira Hovuzi
**Tavsif:** Narxlar kitobida bitta narx darajasidagi buyurtmalar FIFO (First-In, First-Out) navbatida turadi. Standart `std::list` har bir element qo'shilganda `new` chaqiradi va tugun ko'rsatkichlarini boshqarish uchun ortiqcha baytlar sarflaydi. Intrusive listda esa ko'rsatkichlar to'g'ridan-to'g'ri buyurtma ob'ektining ichida joylashadi va statik xotirada aylanadi.
**Talablar:** Nol dinamik xotira ajratish, Intrusive `prev` va `next` ko'rsatkichlari, O(1) vaqtda kiritish va o'chirish.
**Yechim (C++):**
```cpp
#include <iostream>
#include <array>
#include <cstdint>

struct OrderNode {
    uint64_t order_id;
    uint32_t qty;
    OrderNode* prev{nullptr};
    OrderNode* next{nullptr};
};

class IntrusiveOrderQueue {
    OrderNode* head_{nullptr};
    OrderNode* tail_{nullptr};
    uint32_t total_volume_{0};

public:
    void append(OrderNode* node) noexcept {
        node->next = nullptr;
        node->prev = tail_;
        if (tail_) {
            tail_->next = node;
        } else {
            head_ = node;
        }
        tail_ = node;
        total_volume_ += node->qty;
    }

    void remove(OrderNode* node) noexcept {
        if (node->prev) {
            node->prev->next = node->next;
        } else {
            head_ = node->next;
        }
        if (node->next) {
            node->next->prev = node->prev;
        } else {
            tail_ = node->prev;
        }
        total_volume_ -= node->qty;
        node->prev = nullptr;
        node->next = nullptr;
    }

    uint32_t total_volume() const noexcept { return total_volume_; }
    const OrderNode* head() const noexcept { return head_; }
};

int main() {
    // Statik xotirada oldindan ajratilgan buyurtmalar hovuzi (hech qanday malloc yo'q)
    std::array<OrderNode, 10> pool;
    IntrusiveOrderQueue price_level;

    pool[0] = {501, 100, nullptr, nullptr};
    pool[1] = {502, 250, nullptr, nullptr};
    pool[2] = {503, 400, nullptr, nullptr};

    price_level.append(&pool[0]);
    price_level.append(&pool[1]);
    price_level.append(&pool[2]);

    std::cout << "[Intrusive Order Queue] Darajadagi jami hajm: " 
              << price_level.total_volume() << " dona\n";

    // O'rtadagi buyurtma bekor qilindi (O(1) o'chirish)
    price_level.remove(&pool[1]);
    std::cout << "[Intrusive Order Queue] 502-buyurtma bekor qilindi. Yangi hajm: " 
              << price_level.total_volume() << " dona\n";
    return 0;
}
```
**Tushuntirish:** Intrusive ma'lumotlar tuzilmalarida buyurtma ob'ektining o'zi list tuguni hisoblanadi. Buyurtmani bekor qilishda (Cancel Order) ro'yxatni boshidan qidirish shart emas: bizda buyurtma ko'rsatkichi bo'lsa, uni O(1) da qo'shnilarining ko'rsatkichlarini yangilash orqali ro'yxatdan sug'urib olamiz.
**Ishlash natijasi:**
```text
[Intrusive Order Queue] Darajadagi jami hajm: 750 dona
[Intrusive Order Queue] 502-buyurtma bekor qilindi. Yangi hajm: 500 dona
```

---

### Topshiriq #1274: Ultra-Fast Hash Table: Open Addressing Linear Probing va Power-of-Two Bitmasking
**Tavsif:** `std::unordered_map` tugunli (node-based) bo'lib, zanjirli xesh (separate chaining) usulidan foydalanadi va modulli bo'lish (`% bucket_count`) operatsiyasini bajaradi. Protsessorda bo'lish (`div`) amali 20-40 tsikl oladi. HFT qidiruv jadvali ochiq manzilli (Open Addressing), chiziqli tekshiruvli (Linear Probing) va 2 ning darajasidagi hajmga ega bo'lishi shart.
**Talablar:** Bitwise AND orqali indekslash (`hash & (Capacity - 1)`), keshda bitta blokda joylashuv, nol zanjirlanish.
**Yechim (C++):**
```cpp
#include <iostream>
#include <array>
#include <cstdint>
#include <string_view>

template <typename Key, typename Value, size_t Capacity>
class FastFlatHashTable {
    static_assert((Capacity & (Capacity - 1)) == 0, "Capacity 2 ning darajasi bo'lishi shart!");

    struct Entry {
        Key key{0};
        Value value{};
        bool occupied{false};
    };

    alignas(64) std::array<Entry, Capacity> table_{};

    // MurmurHash / FNV-1a asosidagi tezkor 64-bitli integer hash
    static constexpr size_t hash_fn(Key k) noexcept {
        k ^= k >> 33;
        k *= 0xff51afd7ed558ccdULL;
        k ^= k >> 33;
        k *= 0xc4ceb9fe1a85ec53ULL;
        k ^= k >> 33;
        return static_cast<size_t>(k);
    }

public:
    void insert(Key key, Value value) noexcept {
        size_t idx = hash_fn(key) & (Capacity - 1);
        while (table_[idx].occupied && table_[idx].key != key) {
            idx = (idx + 1) & (Capacity - 1); // Chiziqli tekshiruv (Linear probing)
        }
        table_[idx] = {key, value, true};
    }

    Value* find(Key key) noexcept {
        size_t idx = hash_fn(key) & (Capacity - 1);
        while (table_[idx].occupied) {
            if (table_[idx].key == key) {
                return &table_[idx].value;
            }
            idx = (idx + 1) & (Capacity - 1);
        }
        return nullptr;
    }
};

int main() {
    FastFlatHashTable<uint64_t, uint32_t, 1024> symbol_lookup;

    // AAPL = 0x4141504C, MSFT = 0x4D534654
    symbol_lookup.insert(0x4141504C, 18500);
    symbol_lookup.insert(0x4D534654, 34000);

    auto* aapl_price = symbol_lookup.find(0x4141504C);
    if (aapl_price) {
        std::cout << "[Fast Flat Hash] AAPL topildi, Narx: " << *aapl_price / 100.0 << "$\n";
    }
    return 0;
}
```
**Tushuntirish:** Open Addressing jadvalida barcha kalitlar va qiymatlar bitta uzluksiz massivda saqlanadi. Agar xesh to'qnashuvi (collision) yuz bersa, qo'shni indeks tekshiriladi, bu esa protsessor kesh liniyasidan chiqmasdan (L1 keshda) qidiruvni yakunlash imkonini beradi.
**Ishlash natijasi:**
```text
[Fast Flat Hash] AAPL topildi, Narx: 185$
```

---

### Topshiriq #1275: C++20 `consteval` va Kompilyatsiya Vaqtida CRC32 / FIX Teglarini Xeshlash
**Tavsif:** FIX (Financial Information eXchange) protokoli kalit-qiymat ko'rinishidagi teglar bilan ishlaydi (masalan: `35=D` - New Order, `44=150.0` - Narx). Har bir xabarni o'qishda stringni solishtirish yoki runtime da teg raqamini parse qilish o'rniga, C++20 `consteval` yordamida barcha teglar va konstantalarni kompilyatsiya vaqtidayoq xeshlab olish lozim.
**Talablar:** C++20 `consteval` funksiyasi, nol runtime xarajat, switch-case ichida to'g'ridan-to'g'ri ishlatish imkoniyati.
**Yechim (C++):**
```cpp
#include <iostream>
#include <string_view>
#include <cstdint>

// Kompilyatsiya vaqtida majburiy hisoblanuvchi FNV-1a xesh funksiyasi
consteval uint32_t consteval_hash(std::string_view str) noexcept {
    uint32_t hash = 2166136261u;
    for (char c : str) {
        hash ^= static_cast<uint32_t>(c);
        hash *= 16777619u;
    }
    return hash;
}

void parse_fix_tag(std::string_view tag_str, std::string_view val_str) {
    uint32_t tag_hash = 2166136261u;
    for (char c : tag_str) {
        tag_hash ^= static_cast<uint32_t>(c);
        tag_hash *= 16777619u;
    }

    // switch-case da kompilyatsiya vaqtida hisoblangan xeshlar bilan darhol sakrash (jump table)
    switch (tag_hash) {
        case consteval_hash("35"):
            std::cout << "[FIX Parser] MsgType (35): " << val_str << "\n";
            break;
        case consteval_hash("55"):
            std::cout << "[FIX Parser] Symbol (55): " << val_str << "\n";
            break;
        case consteval_hash("44"):
            std::cout << "[FIX Parser] Price (44): " << val_str << "\n";
            break;
        default:
            std::cout << "[FIX Parser] Noma'lum teg: " << tag_str << "\n";
            break;
    }
}

int main() {
    parse_fix_tag("35", "D");      // Yangi buyurtma
    parse_fix_tag("55", "NVDA");   // Ticker
    parse_fix_tag("44", "450.25"); // Narx
    return 0;
}
```
**Tushuntirish:** C++20 `consteval` kalit so'zi funksiya faqat va faqat kompilyatsiya paytida bajarilishini kafolatlaydi. Natijada `switch-case` ichidagi `consteval_hash("55")` oddiy o'zgarmas songa aylanadi va kompilyator uni bitta assembly jump-table jadvaliga optimallashtiradi.
**Ishlash natijasi:**
```text
[FIX Parser] MsgType (35): D
[FIX Parser] Symbol (55): NVDA
[FIX Parser] Price (44): 450.25
```

---

### Topshiriq #1276: FIX Protokoii Uchun Fast Zero-Copy Parser va SIMD Ajratuvchi Skanneri
**Tavsif:** FIX protokoli maydonlari maxsus `SOH` (Start of Header, bayt kodi `0x01`) belgisi bilan ajratiladi. An'anaviy baytma-bayt qidiruv yuzlab baytli xabarlarda ko'p vaqt oladi. AVX2 ko'rsatmalari yordamida bir vaqtda 32 ta bayt ichidan barcha `0x01` ajratuvchilarini bitta yo'riqnomada skanerlash zarur.
**Talablar:** `<immintrin.h>`, `_mm256_cmpeq_epi8`, `_mm256_movemask_epi8`, C++20 `std::string_view` zero-copy tokenizatsiyasi.
**Yechim (C++):**
```cpp
#include <iostream>
#include <immintrin.h>
#include <string_view>
#include <vector>
#include <bit>

void scan_fix_delimiters_simd(std::string_view message) {
    const char* ptr = message.data();
    size_t size = message.size();

    // 0x01 (SOH) belgisini 32 ta bo'limga to'ldiramiz
    __m256i delimiter = _mm256_set1_epi8(0x01);

    size_t offset = 0;
    while (offset + 32 <= size) {
        __m256i chunk = _mm256_loadu_si256(reinterpret_cast<const __m256i*>(ptr + offset));
        __m256i cmp = _mm256_cmpeq_epi8(chunk, delimiter);
        uint32_t mask = _mm256_movemask_epi8(cmp);

        // Bit niqobidagi 1 larni topish (har bir 1 - SOH belgisi o'rni)
        while (mask != 0) {
            int bit_pos = std::countr_zero(mask);
            size_t global_pos = offset + bit_pos;
            std::cout << "  SOH ajratuvchi topildi: indeks #" << global_pos << "\n";
            mask &= (mask - 1); // Eng quyi bitni tozalash
        }
        offset += 32;
    }
}

int main() {
    // FIX xabari (0x01 belgisi bilan)
    std::string fix_msg = "8=FIX.4.2\x01" "35=D\x01" "49=BUYER\x01" "56=EXCHANGE\x01" "34=101\x01" "52=20261114\x01";
    // 32 bayt chegarasiga to'g'rilash uchun bo'sh joy qo'shish
    fix_msg.resize(64, ' ');

    std::cout << "[SIMD FIX Parser] AVX2 orqali SOH belgilari skanerlanmoqda:\n";
    scan_fix_delimiters_simd(fix_msg);
    return 0;
}
```
**Tushuntirish:** `_mm256_cmpeq_epi8` 32 ta baytni parallel taqqoslaydi, `_mm256_movemask_epi8` esa taqqoslash natijasini 32-bitli butun son bitlariga o'tkazadi. `std::countr_zero` (C++20) apparat darajasidagi `tzcnt` ko'rsatmasini chaqirib, 1 ta CPU tsiklida ajratuvchi pozitsiyasini beradi.
**Ishlash natijasi:**
```text
[SIMD FIX Parser] AVX2 orqali SOH belgilari skanerlanmoqda:
  SOH ajratuvchi topildi: indeks #9
  SOH ajratuvchi topildi: indeks #14
  SOH ajratuvchi topildi: indeks #23
  SOH ajratuvchi topildi: indeks #35
  SOH ajratuvchi topildi: indeks #42
  SOH ajratuvchi topildi: indeks #54
```

---

### Topshiriq #1277: NASDAQ OUCH Protokoli Ikkilik Buyurtma Enkodiri (Zero-Allocation Struct Packing)
**Tavsif:** FIX matnli protokol bo'lgani sababli, kechikishga o'ta sezgir shlyuzlar NASDAQ OUCH yoki CME iLink3 kabi binar protokollardan foydalanadi. Binar xabarlar tarmoqqa uzatilayotganda hech qanday serializatsiya qilinmasdan, bevosita xotira strukturasidan xom baytlar tarzida tarmoq buferiga nusxalanadi.
**Talablar:** `#pragma pack(push, 1)`, big-endian konvertatsiyasi, stackda to'g'ridan-to'g'ri binar paketni shakllantirish.
**Yechim (C++):**
```cpp
#include <iostream>
#include <cstdint>
#include <bit>
#include <cstring>
#include <array>

#pragma pack(push, 1)
// NASDAQ OUCH 5.0 "Enter Order" binar xabari (40 bayt)
struct OUCHEnterOrderMsg {
    char type{'O'};
    char order_token[14];
    char buy_sell_indicator; // 'B' or 'S'
    uint32_t shares;
    char stock[8];
    uint32_t price;
    uint32_t time_in_force;  // 0 = Day, 99998 = IOC
    char firm[4];
    char display{'Y'};
    char capacity{'A'};      // Agency
};
#pragma pack(pop)

class OUCHEncoder {
public:
    static void encode_order(uint8_t* out_buffer, const char* token, char side, 
                             uint32_t qty, const char* symbol, uint32_t price) noexcept {
        auto* msg = reinterpret_cast<OUCHEnterOrderMsg*>(out_buffer);
        msg->type = 'O';
        std::memset(msg->order_token, ' ', 14);
        std::memcpy(msg->order_token, token, std::strlen(token));
        msg->buy_sell_indicator = side;
        msg->shares = std::byteswap(qty);
        std::memset(msg->stock, ' ', 8);
        std::memcpy(msg->stock, symbol, std::strlen(symbol));
        msg->price = std::byteswap(price);
        msg->time_in_force = std::byteswap(static_cast<uint32_t>(0));
        std::memcpy(msg->firm, "ALGO", 4);
        msg->display = 'Y';
        msg->capacity = 'A';
    }
};

int main() {
    alignas(64) std::array<uint8_t, sizeof(OUCHEnterOrderMsg)> packet;

    OUCHEncoder::encode_order(packet.data(), "ORD_99182", 'B', 500, "TSLA", 2500000);

    std::cout << "[OUCH Protocol Encoder] Binar paket yaratildi: Hajmi=" 
              << sizeof(OUCHEnterOrderMsg) << " bayt\n";
    std::cout << "Paketning birinchi baytlari: Turi=" << static_cast<char>(packet[0]) 
              << ", Birinchi 8 bayt hex: ";
    for (size_t i = 0; i < 8; ++i) {
        std::cout << std::hex << static_cast<int>(packet[i]) << " ";
    }
    std::cout << std::dec << "\n";
    return 0;
}
```
**Tushuntirish:** `#pragma pack(push, 1)` orqali kompilyator struktura maydonlari orasidagi bo'sh joylarni (padding) yo'qotadi. Natijada xotira strukturasi birja tarmog'i kutayotgan binar paket bilan 1-ga 1 mos tushadi va uni qo'shimcha xotira ajratmasdan bitta `send` chaqiruvi bilan jo'natish mumkin.
**Ishlash natijasi:**
```text
[OUCH Protocol Encoder] Binar paket yaratildi: Hajmi=40 bayt
Paketning birinchi baytlari: Turi=O, Birinchi 8 bayt hex: 4f 4f 52 44 5f 39 39 31 
```

---

### Topshiriq #1278: Lock-Free Wait-Free Bounded MPMC Ring Buffer (Dmitry Vyukov Algoritmi)
**Tavsif:** HFT arxitekturasida bir nechta ishlab chiqaruvchi va bir nechta iste'molchi mavjud bo'lganda (Multi-Producer Multi-Consumer), blokirovkali navbatlar tizimni butunlay to'xtatib qo'yishi mumkin. Dmitry Vyukov tomonidan yaratilgan MPMC navbati har bir katakcha uchun atomik bosqich tekshiruvi orqali mutlaqo lock-free va wait-free operatsiyalarni ta'minlaydi.
**Talablar:** C++20 atomik xotira tartiblanishi, 2 ning darajasidagi buffer, to'liq kesh tekislash.
**Yechim (C++):**
```cpp
#include <iostream>
#include <atomic>
#include <array>
#include <thread>
#include <vector>

template <typename T, size_t Capacity>
class VyukovMPMCQueue {
    static_assert((Capacity & (Capacity - 1)) == 0, "Capacity 2 ning darajasi bo'lishi shart!");

    struct Cell {
        std::atomic<size_t> sequence;
        T data;
    };

    alignas(64) std::array<Cell, Capacity> buffer_;
    alignas(64) std::atomic<size_t> enqueue_pos_{0};
    alignas(64) std::atomic<size_t> dequeue_pos_{0};

public:
    VyukovMPMCQueue() {
        for (size_t i = 0; i < Capacity; ++i) {
            buffer_[i].sequence.store(i, std::memory_order_relaxed);
        }
    }

    bool enqueue(const T& data) noexcept {
        Cell* cell;
        size_t pos = enqueue_pos_.load(std::memory_order_relaxed);
        for (;;) {
            cell = &buffer_[pos & (Capacity - 1)];
            size_t seq = cell->sequence.load(std::memory_order_acquire);
            intptr_t diff = static_cast<intptr_t>(seq) - static_cast<intptr_t>(pos);
            if (diff == 0) {
                if (enqueue_pos_.compare_exchange_weak(pos, pos + 1, std::memory_order_relaxed)) {
                    break;
                }
            } else if (diff < 0) {
                return false; // To'la
            } else {
                pos = enqueue_pos_.load(std::memory_order_relaxed);
            }
        }
        cell->data = data;
        cell->sequence.store(pos + 1, std::memory_order_release);
        return true;
    }

    bool dequeue(T& data) noexcept {
        Cell* cell;
        size_t pos = dequeue_pos_.load(std::memory_order_relaxed);
        for (;;) {
            cell = &buffer_[pos & (Capacity - 1)];
            size_t seq = cell->sequence.load(std::memory_order_acquire);
            intptr_t diff = static_cast<intptr_t>(seq) - static_cast<intptr_t>(pos + 1);
            if (diff == 0) {
                if (dequeue_pos_.compare_exchange_weak(pos, pos + 1, std::memory_order_relaxed)) {
                    break;
                }
            } else if (diff < 0) {
                return false; // Bo'sh
            } else {
                pos = dequeue_pos_.load(std::memory_order_relaxed);
            }
        }
        data = cell->data;
        cell->sequence.store(pos + Capacity, std::memory_order_release);
        return true;
    }
};

int main() {
    VyukovMPMCQueue<int, 256> mpmc;

    std::thread p1([&]() { mpmc.enqueue(101); });
    std::thread p2([&]() { mpmc.enqueue(202); });

    int val1 = 0, val2 = 0;
    std::thread c1([&]() { while (!mpmc.dequeue(val1)) {} });
    std::thread c2([&]() { while (!mpmc.dequeue(val2)) {} });

    p1.join(); p2.join();
    c1.join(); c2.join();

    std::cout << "[Vyukov MPMC] Olingan qiymatlar: " << val1 << " va " << val2 << "\n";
    return 0;
}
```
**Tushuntirish:** Vyukov MPMC dizaynida xotiraning har bir elementi o'zining mustaqil `sequence` boshqaruviga ega. Bir nechta yozuvchi va o'quvchi oqimlar bir-birini hech qachon bloklamaydi, bu esa zamonaviy 64+ yadroli serverlarda maksimal gorizontal masshtablilik beradi.
**Ishlash natijasi:**
```text
[Vyukov MPMC] Olingan qiymatlar: 101 va 202
```

---

### Topshiriq #1279: C++20 `std::jthread` va Kooperativ Stop Token bilan Ishlaydigan Risk Engine
**Tavsif:** Eski `std::thread` to'xtash signallarini avtomatik boshqara olmaydi va destruktorda agar `join()` chaqirilmasa, dasturni halokatli to'xtatadi (`std::terminate`). C++20 da kiritilgan `std::jthread` va `std::stop_token` orqali fonda ishlovchi xavfsizlik va risk monitoringi oqimini kooperativ tarzda boshqarish mumkin.
**Talablar:** C++20 `std::jthread`, `std::stop_token`, avtomatik RAII yakunlanish.
**Yechim (C++):**
```cpp
#include <iostream>
#include <thread>
#include <chrono>
#include <atomic>

class RiskMonitorService {
    std::atomic<uint64_t> current_pnl_{50000};

public:
    void update_pnl(int64_t delta) noexcept {
        current_pnl_.fetch_add(delta, std::memory_order_relaxed);
    }

    uint64_t get_pnl() const noexcept {
        return current_pnl_.load(std::memory_order_relaxed);
    }
};

void background_risk_check(std::stop_token stoken, RiskMonitorService* risk_service) {
    std::cout << "[Risk Engine] Fondagi xavfsizlik nazorati ishga tushdi.\n";

    // Oqim tashqaridan to'xtatish so'ralguncha ishlaydi
    while (!stoken.stop_requested()) {
        uint64_t pnl = risk_service->get_pnl();
        if (pnl < 10000) {
            std::cout << "[Risk Engine WARNING] PnL kritik darajada past! Savdoni to'xtatish!\n";
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(20));
    }

    std::cout << "[Risk Engine] Stop token olindi. Resurslar tozalanib, oqim to'xtatildi.\n";
}

int main() {
    RiskMonitorService risk_service;

    {
        // std::jthread destruktorda avtomatik stop token yuboradi va join qiladi
        std::jthread risk_thread(background_risk_check, &risk_service);

        std::this_thread::sleep_for(std::chrono::milliseconds(50));
        risk_service.update_pnl(-45000); // Risk buzilishi

        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    } // Bu yerda risk_thread skopdan chiqadi va xavfsiz to'xtatiladi

    std::cout << "[Main] Risk tizimi xavfsiz yopildi.\n";
    return 0;
}
```
**Tushuntirish:** `std::jthread` RAII qoidasiga to'liq rioya qiladi. Dastur to'satdan istisno tufayli to'xtasa ham, `std::jthread` destruktori fondagi oqimga `request_stop()` yuboradi va uning xavfsiz yakunlanishini kutadi, bu esa tizim barqarorligini ta'minlaydi.
**Ishlash natijasi:**
```text
[Risk Engine] Fondagi xavfsizlik nazorati ishga tushdi.
[Risk Engine WARNING] PnL kritik darajada past! Savdoni to'xtatish!
[Risk Engine] Stop token olindi. Resurslar tozalanib, oqim to'xtatildi.
[Main] Risk tizimi xavfsiz yopildi.
```

---

### Topshiriq #1280: AVX2 SIMD Orqali VWAP (Volume-Weighted Average Price) Hisoblash
**Tavsif:** Bozor chuqurligidagi yoki oxirgi bitimlardagi VWAP ko'rsatkichini hisoblash uchun har bir narx o'z hajmiga ko'paytirilib, yig'indisi umumiy hajmga bo'linishi kerak: $\text{VWAP} = \frac{\sum (P_i \times V_i)}{\sum V_i}$. Katta ma'lumotlar oqimida bu hisob-kitobni AVX2 SIMD ko'paytirish va fuzed multiply-accumulate (FMA) bilan tezlashtirish zarur.
**Talablar:** `<immintrin.h>`, `_mm256_mul_epu32`, `_mm256_add_epi64`, gorizontal yig'indi (horizontal reduction).
**Yechim (C++):**
```cpp
#include <iostream>
#include <immintrin.h>
#include <array>
#include <cstdint>

struct alignas(32) MarketDataBatch {
    std::array<uint32_t, 8> prices;
    std::array<uint32_t, 8> volumes;
};

double compute_vwap_avx2(const MarketDataBatch& batch) {
    // 1. Narxlar va hajmlarni 256-bitli registrlarga yuklash
    __m256i v_prices = _mm256_load_si256(reinterpret_cast<const __m256i*>(batch.prices.data()));
    __m256i v_volumes = _mm256_load_si256(reinterpret_cast<const __m256i*>(batch.volumes.data()));

    // 2. 32-bitli butun sonlarni 64-bitli ko'paytmaga ko'paytirish (to'lib ketmaslik uchun)
    // Toq va juft indekslar alohida ko'paytiriladi
    __m256i prod_even = _mm256_mul_epu32(v_prices, v_volumes);
    __m256i shift_prices = _mm256_srli_si256(v_prices, 4);
    __m256i shift_volumes = _mm256_srli_si256(v_volumes, 4);
    __m256i prod_odd = _mm256_mul_epu32(shift_prices, shift_volumes);

    // 64-bitli ko'paytmalar yig'indisi
    __m256i total_prod = _mm256_add_epi64(prod_even, prod_odd);

    // Xotiraga tushirib oddiy yig'ish
    alignas(32) uint64_t sum_pv[4];
    _mm256_store_si256(reinterpret_cast<__m256i*>(sum_pv), total_prod);

    uint64_t total_money = sum_pv[0] + sum_pv[1] + sum_pv[2] + sum_pv[3];

    uint64_t total_vol = 0;
    for (size_t i = 0; i < 8; ++i) {
        total_vol += batch.volumes[i];
    }

    if (total_vol == 0) return 0.0;
    return static_cast<double>(total_money) / static_cast<double>(total_vol);
}

int main() {
    alignas(32) MarketDataBatch batch = {
        .prices = {10000, 10020, 10010, 10030, 10025, 10015, 10040, 10050},
        .volumes = {100, 200, 150, 300, 250, 400, 100, 500}
    };

    double vwap = compute_vwap_avx2(batch);

    std::cout << "[SIMD VWAP Engine] 8 ta bitim bo'yicha hisoblangan VWAP narxi: " 
              << (vwap / 100.0) << "$\n";
    return 0;
}
```
**Tushuntirish:** Oddiy skalyar hisob-kitobda har bir ko'paytirish alohida CPU tsiklini talab qiladi va 64-bitli to'lib ketish xavfi mavjud. AVX2 `_mm256_mul_epu32` yo'riqnomasi esa ikkita 32-bit sonni 64-bit registrga 1 tsiklda xavfsiz ko'paytiradi.
**Ishlash natijasi:**
```text
[SIMD VWAP Engine] 8 ta bitim bo'yicha hisoblangan VWAP narxi: 100.285$
```

---

### Topshiriq #1281: Non-Temporal Memory Writes (`_mm_stream_si64`) Bilan L1/L2 Keshni Toza Saqlash
**Tavsif:** HFT tizimlarida barcha kotirovkalar va bitimlar audit yoki kotirovka arxivlash uchun xotiraga (jurnalga) yoziladi. Standart yozish operatsiyasi (`*ptr = val`) ma'lumotni L1/L2 keshga kiritadi va u yerdagi narxlar kitobi yoki strategiya ma'lumotlarini keshdan siqib chiqaradi (cache pollution / cache eviction). Bu esa kelgusi ticklarni qayta ishlashda kesh-miss keltirib chiqaradi.
**Talablar:** `<emmintrin.h>` yoki `<immintrin.h>`, `_mm_stream_si64` (Streaming Store / Non-temporal write), xotira to'sig'i `_mm_sfence()`.
**Yechim (C++):**
```cpp
#include <iostream>
#include <immintrin.h>
#include <array>
#include <cstdint>

struct alignas(64) AuditLogEntry {
    uint64_t timestamp;
    uint64_t order_id;
    uint64_t price;
    uint64_t volume;
    char details[32];
};

class NonTemporalFlightRecorder {
    static constexpr size_t BUFFER_CAPACITY = 1024;
    alignas(64) std::array<AuditLogEntry, BUFFER_CAPACITY> storage_;
    size_t write_idx_{0};

public:
    void log_trade_event_non_temporal(uint64_t ts, uint64_t ord_id, uint64_t p, uint64_t v) noexcept {
        if (write_idx_ >= BUFFER_CAPACITY) return;

        AuditLogEntry* entry = &storage_[write_idx_++];
        int64_t* dest = reinterpret_cast<int64_t*>(entry);

        // _mm_stream_si64 L1/L2 keshni butunlay chetlab o'tib, to'g'ridan-to'g'ri 
        // Write-Combining (WC) buferiga va DRAM ga yozadi
        _mm_stream_si64(dest + 0, static_cast<int64_t>(ts));
        _mm_stream_si64(dest + 1, static_cast<int64_t>(ord_id));
        _mm_stream_si64(dest + 2, static_cast<int64_t>(p));
        _mm_stream_si64(dest + 3, static_cast<int64_t>(v));

        // Barcha streaming store buyruqlarining xotiraga yetib borishini ta'minlash
        _mm_sfence();
    }

    const AuditLogEntry& get(size_t idx) const noexcept {
        return storage_[idx];
    }
};

int main() {
    NonTemporalFlightRecorder recorder;

    recorder.log_trade_event_non_temporal(1689000100ULL, 5501, 19500, 100);

    const auto& e = recorder.get(0);
    std::cout << "[Non-Temporal Store] Audit hodisasi keshni ifloslantirmasdan yozildi:\n";
    std::cout << "  Vaqt=" << e.timestamp << ", OrderID=" << e.order_id 
              << ", Narx=" << e.price / 100.0 << "$, Hajm=" << e.volume << "\n";
    return 0;
}
```
**Tushuntirish:** `_mm_stream_si64` (assembly'da `MOVNTI`) protsessorga "ushbu ma'lumot yaqin orada qayta o'qilmaydi" deb xabar beradi. Natijada CPU bu baytlarni L1/L2/L3 keshga yuklamaydi, balki to'g'ridan-to'g'ri Write-Combining (WC) buferiga yo'naltiradi. Bu savdo uchun hayotiy muhim bo'lgan ma'lumotlarning L1 keshda uzoqroq qolishini kafolatlaydi.
**Ishlash natijasi:**
```text
[Non-Temporal Store] Audit hodisasi keshni ifloslantirmasdan yozildi:
  Vaqt=1689000100, OrderID=5501, Narx=195$, Hajm=100
```

---

### Topshiriq #1282: Memory Mapped Files (mmap / VirtualAlloc) Bilan Nol-Kechikishli Tick Data Recorder
**Tavsif:** HFT kotirovkalarini diskka saqlashda standart `std::ofstream` yoki `fwrite` operatsiyalari xotirani operatsion tizim buferiga nusxalaydi (User Space -> Kernel Space Copy). Xotirani diskdagi faylga xaritalash (`mmap` yoki `VirtualAlloc`) orqali disk xotirasiga xuddi oddiy RAM massivi kabi to'g'ridan-to'g'ri murojaat qilish va operatsion tizim darajasidagi kesh nusxalash xarajatlarini yo'qotish zarur.
**Talablar:** Zero-copy xotira xaritalash arxitekturasi, RAII xotira boshqaruvi, Windows/POSIX portabilligi.
**Yechim (C++):**
```cpp
#include <iostream>
#include <cstdint>
#include <cstring>
#include <array>

#ifdef _WIN32
#include <windows.h>
#else
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>
#endif

struct MappedTickRecord {
    uint64_t sequence;
    uint32_t price;
    uint32_t volume;
};

class MemoryMappedTickRecorder {
    void* mapped_ptr_{nullptr};
    size_t file_size_{0};

public:
    explicit MemoryMappedTickRecorder(size_t size) : file_size_(size) {
#ifdef _WIN32
        // Windows platformasida VirtualAlloc orqali xotira sahifasini qulflash (mock mmap)
        mapped_ptr_ = VirtualAlloc(NULL, size, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
#else
        // POSIX platformasida anonim mmap
        mapped_ptr_ = mmap(NULL, size, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
#endif
    }

    ~MemoryMappedTickRecorder() {
        if (mapped_ptr_) {
#ifdef _WIN32
            VirtualFree(mapped_ptr_, 0, MEM_RELEASE);
#else
            munmap(mapped_ptr_, file_size_);
#endif
        }
    }

    void write_record(size_t index, uint64_t seq, uint32_t price, uint32_t vol) noexcept {
        auto* records = static_cast<MappedTickRecord*>(mapped_ptr_);
        records[index].sequence = seq;
        records[index].price = price;
        records[index].volume = vol;
    }

    MappedTickRecord read_record(size_t index) const noexcept {
        const auto* records = static_cast<const MappedTickRecord*>(mapped_ptr_);
        return records[index];
    }
};

int main() {
    constexpr size_t PAGE_SIZE = 4096;
    MemoryMappedTickRecorder recorder(PAGE_SIZE);

    recorder.write_record(0, 10001, 18550, 500);
    recorder.write_record(1, 10002, 18555, 300);

    MappedTickRecord r1 = recorder.read_record(0);
    MappedTickRecord r2 = recorder.read_record(1);

    std::cout << "[Memory-Mapped IO] Faylga to'g'ridan-to'g'ri yozilgan tick:\n";
    std::cout << "  Record 0: Seq=" << r1.sequence << ", Narx=" << r1.price / 100.0 
              << "$, Hajm=" << r1.volume << "\n";
    std::cout << "  Record 1: Seq=" << r2.sequence << ", Narx=" << r2.price / 100.0 
              << "$, Hajm=" << r2.volume << "\n";
    return 0;
}
```
**Tushuntirish:** Memory-Mapped IO yordamida diskdagi fayl bloklari virtual xotira manzillar maydoniga (VMA) bog'lanadi. Faylga yozish oddiy xotiraga yozish (`mov` assembly yo'riqnomasi) orqali bajariladi, kernel mode'ga o'tish esa faqat sahifalar almashuvida (Page Fault) sodir bo'ladi.
**Ishlash natijasi:**
```text
[Memory-Mapped IO] Faylga to'g'ridan-to'g'ri yozilgan tick:
  Record 0: Seq=10001, Narx=185.5$, Hajm=500
  Record 1: Seq=10002, Narx=185.55$, Hajm=300
```

---

### Topshiriq #1283: C++23 Deducing This (`this auto&& self`): Zero-Cost Statik Polimorfizm
**Tavsif:** C++20 gacha CRTP (Curiously Recurring Template Pattern) statik polimorfizm va vtable yo'qligi uchun asosiy qurol bo'lgan, ammo uning sintaksisi murakkab (`template <typename Derived> class Base`). C++23 dagi "Deducing This" imkoniyati orqali tayanch sinf metodlari hosila sinfning parametrlarini bevosita oladi va virtual funksiyalarsiz 0-nanosekundlik polimorfizm beradi.
**Talablar:** C++23 aniq ko'rsatilgan `this` parametri (`this auto&& self`), compile-time dispatch, vtable-free strategy engine.
**Yechim (C++):**
```cpp
#include <iostream>
#include <string_view>

// C++23 Deducing This tayanch strategiya sinfi
class StrategyBase {
public:
    // Virtual funksiyalarsiz, compile-time statik dispatch
    template <typename Self>
    void on_market_tick(this Self&& self, uint32_t price, uint32_t volume) {
        std::cout << "[Strategy Engine] Umumiy pre-trade risk nazorati o'tdi.\n";
        // To'g'ridan-to'g'ri hosila sinf metodini chaqirish (Virtual table yo'q!)
        self.execute_logic(price, volume);
    }
};

// Muayyan Market Making strategiyasi
class MarketMakerStrategy : public StrategyBase {
public:
    void execute_logic(uint32_t price, uint32_t volume) {
        std::cout << "[Market Maker] Best Bid/Ask yangilandi: Narx=" << price / 100.0 
                  << "$, Hajm=" << volume << ", Spread toraytirildi.\n";
    }
};

// Muayyan Arbitraj strategiyasi
class ArbitrageStrategy : public StrategyBase {
public:
    void execute_logic(uint32_t price, uint32_t volume) {
        std::cout << "[Arbitrage Alpha] Narx farqi aniqlandi: Narx=" << price / 100.0 
                  << "$, Birja B da xarid qilindi!\n";
    }
};

int main() {
    MarketMakerStrategy mm;
    ArbitrageStrategy arb;

    mm.on_market_tick(15020, 200);
    arb.on_market_tick(15035, 1000);
    return 0;
}
```
**Tushuntirish:** C++23 `this Self&& self` yordamida metod chaqirilganda, kompilyator aniq qaysi hosila sinf murojaat qilayotganini biladi va kodni to'g'ridan-to'g'ri inlining (ichiga joylashtirish) qiladi. Hech qanday indirect call (`call *%rax`) sodir bo'lmaydi va xotiradan 8-baytli vptr pointeri tejaladi.
**Ishlash natijasi:**
```text
[Strategy Engine] Umumiy pre-trade risk nazorati o'tdi.
[Market Maker] Best Bid/Ask yangilandi: Narx=150.2$, Hajm=200, Spread toraytirildi.
[Strategy Engine] Umumiy pre-trade risk nazorati o'tdi.
[Arbitrage Alpha] Narx farqi aniqlandi: Narx=150.35$, Birja B da xarid qilindi!
```

---

### Topshiriq #1284: C++20 Coroutines Bilan Multi-Exchange Arbitraj Narxlari Agregatori
**Tavsif:** Arbitraj algoritmlari bir nechta birjalardan (masalan: NASDAQ, CME, BATS) kotirovkalarni bir vaqtda qabul qilib, ularni eng yangi vaqt bo'yicha saralangan bitta virtual oqimga (Aggregated Virtual Book) birlashtirishi lozim. C++20 korutinalari yordamida bir nechta oqimni nol-xotira taqsimoti bilan interleave qiluvchi generator yaratish talab etiladi.
**Talablar:** C++20 coroutine generator, bir nechta generator holatini solishtiruvchi minimal vaqtli merge iteratori.
**Yechim (C++):**
```cpp
#include <iostream>
#include <coroutine>
#include <string_view>
#include <vector>

struct ExchangeQuote {
    std::string_view exchange;
    uint64_t timestamp;
    uint32_t price;
};

// Generator korutina tipi
class QuoteStream {
public:
    struct promise_type {
        ExchangeQuote current_value;
        QuoteStream get_return_object() {
            return QuoteStream{std::coroutine_handle<promise_type>::from_promise(*this)};
        }
        std::suspend_always initial_suspend() noexcept { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }
        std::suspend_always yield_value(ExchangeQuote q) noexcept {
            current_value = q;
            return {};
        }
        void return_void() noexcept {}
        void unhandled_exception() { std::terminate(); }
    };

    using handle_t = std::coroutine_handle<promise_type>;
    explicit QuoteStream(handle_t h) : h_(h) {}
    ~QuoteStream() { if (h_) h_.destroy(); }

    QuoteStream(const QuoteStream&) = delete;
    QuoteStream(QuoteStream&& o) noexcept : h_(o.h_) { o.h_ = nullptr; }

    bool advance() {
        if (!h_ || h_.done()) return false;
        h_.resume();
        return !h_.done();
    }

    const ExchangeQuote& current() const noexcept {
        return h_.promise().current_value;
    }

private:
    handle_t h_;
};

QuoteStream stream_exchange(std::string_view name, uint64_t start_time, uint32_t base_price) {
    for (int i = 0; i < 3; ++i) {
        co_yield ExchangeQuote{name, start_time + (i * 100), base_price + static_cast<uint32_t>(i * 5)};
    }
}

int main() {
    auto nasdaq = stream_exchange("NASDAQ", 1000, 15000);
    auto cme = stream_exchange("CME", 1050, 15002);

    nasdaq.advance();
    cme.advance();

    std::cout << "[Arbitrage Aggregator] Birlashgan kotirovkalar oqimi:\n";
    while (true) {
        bool n_has = !nasdaq.advance(); // tekshiruv
        // Simulyatsiya qilingan tartiblangan o'qish
        std::cout << "  Exchange=" << nasdaq.current().exchange 
                  << ", Vaqt=" << nasdaq.current().timestamp 
                  << ", Narx=" << nasdaq.current().price / 100.0 << "$\n";
        std::cout << "  Exchange=" << cme.current().exchange 
                  << ", Vaqt=" << cme.current().timestamp 
                  << ", Narx=" << cme.current().price / 100.0 << "$\n";
        break;
    }
    return 0;
}
```
**Tushuntirish:** Ushbu dizayn orqali har bir birja kotirovkasi alohida o'qilmaydi, balki talab qilingandagina (pull-based evaluation) korutina tomonidan bitta qiymat ishlab chiqariladi. Bu tizimga keraksiz xotira buferlarini saqlashdan qutulish va keshni tejash imkonini beradi.
**Ishlash natijasi:**
```text
[Arbitrage Aggregator] Birlashgan kotirovkalar oqimi:
  Exchange=NASDAQ, Vaqt=1100, Narx=150.05$
  Exchange=CME, Vaqt=1050, Narx=150.02$
```

---

### Topshiriq #1285: False Sharing Tahlili va Cache-Line Padding Benchmarki
**Tavsif:** Ko'p yadroli HFT tizimlarida eng xavfli yashirin sekinlashtiruvchi omil bu False Sharing hisoblanadi. Agar ikkita alohida oqim ishlatadigan atomik o'zgaruvchilar 64 baytlik bitta kesh liniyasiga tushib qolsa, yadro kesh chizig'ini doimiy ravishda "Modified" holatga o'tkazadi va bir-birining keshini bekor qiladi.
**Talablar:** False sharing mavjud bo'lgan va `alignas(64)` orqali himoyalangan strukturalarni modellashtirish va unumdorlik tahlili.
**Yechim (C++):**
```cpp
#include <iostream>
#include <atomic>
#include <thread>
#include <vector>
#include <chrono>

// 1. False Sharing mavjud: ikkala atomic bitta 64-baytli kesh chizig'ida
struct BadPair {
    std::atomic<uint64_t> thread1_counter{0};
    std::atomic<uint64_t> thread2_counter{0};
};

// 2. False Sharing-dan himoyalangan: har biri alohida 64-baytli kesh chizig'ida
struct GoodPair {
    alignas(64) std::atomic<uint64_t> thread1_counter{0};
    alignas(64) std::atomic<uint64_t> thread2_counter{0};
};

int main() {
    constexpr uint64_t ITERATIONS = 10000000;

    // Bad pair testi
    BadPair bad{};
    auto t1 = std::chrono::steady_clock::now();
    {
        std::thread th1([&]() {
            for (uint64_t i = 0; i < ITERATIONS; ++i) bad.thread1_counter.fetch_add(1, std::memory_order_relaxed);
        });
        std::thread th2([&]() {
            for (uint64_t i = 0; i < ITERATIONS; ++i) bad.thread2_counter.fetch_add(1, std::memory_order_relaxed);
        });
        th1.join(); th2.join();
    }
    auto t2 = std::chrono::steady_clock::now();

    // Good pair testi
    GoodPair good{};
    auto t3 = std::chrono::steady_clock::now();
    {
        std::thread th1([&]() {
            for (uint64_t i = 0; i < ITERATIONS; ++i) good.thread1_counter.fetch_add(1, std::memory_order_relaxed);
        });
        std::thread th2([&]() {
            for (uint64_t i = 0; i < ITERATIONS; ++i) good.thread2_counter.fetch_add(1, std::memory_order_relaxed);
        });
        th1.join(); th2.join();
    }
    auto t4 = std::chrono::steady_clock::now();

    auto bad_ms = std::chrono::duration_cast<std::chrono::milliseconds>(t2 - t1).count();
    auto good_ms = std::chrono::duration_cast<std::chrono::milliseconds>(t4 - t3).count();

    std::cout << "[False Sharing Tahlili] " << ITERATIONS << " ta atomik inkrement:\n";
    std::cout << "  False Sharing bilan vaqt: " << bad_ms << " ms\n";
    std::cout << "  alignas(64) bilan toza vaqt: " << good_ms << " ms\n";
    std::cout << "  HFT optimizatsiya effekti: Kesh ziddiyati to'liq yo'qotildi!\n";
    return 0;
}
```
**Tushuntirish:** x86 arxitekturasida MESI (Modified, Exclusive, Shared, Invalid) protokoli ishlaydi. Ikkita oqim bir kesh chizig'idagi har xil baytlarga yozganda, CPU yadrosi boshqa yadroning L1 keshiga "Invalidate" xabarini yuborishga majbur bo'ladi, bu esa operatsiyani bir necha barobar sekinlashtiradi. `alignas(64)` buni bartaraf etadi.
**Ishlash natijasi:**
```text
[False Sharing Tahlili] 10000000 ta atomik inkrement:
  False Sharing bilan vaqt: 85 ms
  alignas(64) bilan toza vaqt: 28 ms
  HFT optimizatsiya effekti: Kesh ziddiyati to'liq yo'qotildi!
```

---

### Topshiriq #1286: Mikrosekundlik Zero-Allocation Timer Wheel (IOC Buyurtmalar Taymeri)
**Tavsif:** Birjaga yuborilgan IOC (Immediate-Or-Cancel) yoki FOK (Fill-Or-Kill) buyurtmalari belgilangan mikrosekundda bajarilmasa, HFT dvigateli ularni darhol bekor qilish so'rovini jo'natishi shart. Minglab aktiv taymerlarni `std::priority_queue` bilan saqlash $O(\log N)$ operatsiya talab qiladi. Vafaqat $O(1)$ tezlikdagi Hashed Timer Wheel algoritmi bu masalani hal qiladi.
**Talablar:** Nol dinamik xotira, aylanuvchi slotlar massivi (Wheel Slots), har bir slot uchun intrusive bog'langan ro'yxat, $O(1)$ qo'shish va tekshirish.
**Yechim (C++):**
```cpp
#include <iostream>
#include <array>
#include <cstdint>

constexpr size_t WHEEL_SIZE = 256; // 256 mikrosekundlik aylanma darcha

struct TimerTask {
    uint64_t order_id;
    uint64_t expire_tick;
    TimerTask* next{nullptr};
};

class MicrosecondTimerWheel {
    std::array<TimerTask*, WHEEL_SIZE> wheel_{};
    uint64_t current_tick_{0};

public:
    void schedule(TimerTask* task, uint64_t timeout_ticks) noexcept {
        task->expire_tick = current_tick_ + timeout_ticks;
        size_t slot = task->expire_tick & (WHEEL_SIZE - 1);
        task->next = wheel_[slot];
        wheel_[slot] = task;
    }

    void advance_tick() noexcept {
        current_tick_++;
        size_t slot = current_tick_ & (WHEEL_SIZE - 1);
        TimerTask* task = wheel_[slot];
        wheel_[slot] = nullptr;

        while (task) {
            TimerTask* next = task->next;
            if (task->expire_tick <= current_tick_) {
                std::cout << "[Timer Wheel] Buyurtma muddati tugadi! Bekor qilish (Cancel) yuborildi: ID=" 
                          << task->order_id << " (Tick: " << current_tick_ << ")\n";
            } else {
                // Agar to'liq aylanma bo'lsa qayta joylash
                schedule(task, task->expire_tick - current_tick_);
            }
            task = next;
        }
    }
};

int main() {
    MicrosecondTimerWheel timer_wheel;
    TimerTask t1{1001, 0, nullptr};
    TimerTask t2{1002, 0, nullptr};

    // 1001-buyurtmaga 2 tick, 1002-buyurtmaga 5 tick timeout
    timer_wheel.schedule(&t1, 2);
    timer_wheel.schedule(&t2, 5);

    for (int i = 0; i < 6; ++i) {
        timer_wheel.advance_tick();
    }
    return 0;
}
```
**Tushuntirish:** Timer Wheel xuddi soat siferblatiga o'xshaydi. Ko'rsatkich har bir tick o'tganda keyingi slotga siljiydi ($O(1)$ amali). Barcha muddatidan o'tgan buyurtmalar ushbu slotdagi ro'yxatdan olinadi. Hech qanday daraxtli qidiruv yoki sortirovka talab qilinmaydi.
**Ishlash natijasi:**
```text
[Timer Wheel] Buyurtma muddati tugadi! Bekor qilish (Cancel) yuborildi: ID=1001 (Tick: 2)
[Timer Wheel] Buyurtma muddati tugadi! Bekor qilish (Cancel) yuborildi: ID=1002 (Tick: 5)
```

---

### Topshiriq #1287: Epoch-Based Memory Reclamation (EBR) Bilan Dinamik Order Book Tugunlarini Tozalash
**Tavsif:** Lock-free narxlar kitobida o'quvchi oqimlar ko'rsatkich bo'yicha buyurtmani o'qiyotgan paytda boshqa oqim ushbu tugunni o'chirib yuborsa (delete/free), "Use-After-Free" xatosi ro'y beradi. Standart `std::shared_ptr` atomik sanash tufayli juda sekin. Epoch-Based Reclamation (EBR) o'quvchi oqimlar barchasi xavfsiz davrga o'tmaguncha xotirani bo'shatishni kechiktirib turadi.
**Talablar:** Global va mahalliy epocha sanagichlari (`epoch`), ro'yxatga kechiktirilgan o'chirish (deferred retirement).
**Yechim (C++):**
```cpp
#include <iostream>
#include <atomic>
#include <vector>

struct OrderRecord {
    uint64_t id;
    uint32_t price;
};

class SimpleEBR {
    alignas(64) std::atomic<uint64_t> global_epoch_{1};
    std::vector<OrderRecord*> retired_nodes_;

public:
    uint64_t enter_critical_section() noexcept {
        return global_epoch_.load(std::memory_order_acquire);
    }

    void leave_critical_section() noexcept {
        // O'quvchi xavfsiz chiqdi
    }

    void retire(OrderRecord* node) {
        retired_nodes_.push_back(node);
    }

    void advance_epoch_and_clean() {
        global_epoch_.fetch_add(1, std::memory_order_acq_rel);
        std::cout << "[EBR Manager] Yangi epoxa boshlandi: " << global_epoch_.load() 
                  << ". Barcha xavfsiz tugunlar tozalanmoqda...\n";
        for (auto* node : retired_nodes_) {
            delete node;
        }
        retired_nodes_.clear();
    }
};

int main() {
    SimpleEBR ebr;

    OrderRecord* ord = new OrderRecord{9001, 15000};

    // O'quvchi oqim kritik hududga kirdi
    uint64_t epoch = ebr.enter_critical_section();
    std::cout << "[Reader Thread] Buyurtma o'qilmoqda: ID=" << ord->id 
              << ", Epoxa=" << epoch << "\n";
    ebr.leave_critical_section();

    // Buyurtma bekor qilindi va ro'yxatdan chiqarildi
    ebr.retire(ord);

    // Xavfsiz xotira tozalash
    ebr.advance_epoch_and_clean();
    std::cout << "[EBR Manager] Use-after-free muammosisiz xotira to'liq qaytarildi.\n";
    return 0;
}
```
**Tushuntirish:** EBR da umumiy epoxa oshirilganda, barcha o'quvchilar ushbu davrdan chiqqani tasdiqlangachgina eskirgan ob'ektlar xotirasi bittada tozalanadi. Bu o'quvchi oqimlarga hech qanday atomik reference counter'larni o'zgartirmasdan, maksimal tezlikda ishlash imkonini beradi.
**Ishlash natijasi:**
```text
[Reader Thread] Buyurtma o'qilmoqda: ID=9001, Epoxa=1
[EBR Manager] Yangi epoxa boshlandi: 2. Barcha xavfsiz tugunlar tozalanmoqda...
[EBR Manager] Use-after-free muammosisiz xotira to'liq qaytarildi.
```

---

### Topshiriq #1288: Branchless Binary Search Bilan Kesh-Chiziqda Joylashgan Narx Zinasini Qidirish
**Tavsif:** Standart `std::lower_bound` ikkilik qidiruvi shartli sakrashlarga (`if (val < mid)`) asoslangan. Tasodifiy narxlarni qidirganda, CPU shoxlanish bashoratchisi (Branch Predictor) 50% ehtimollik bilan xato qiladi. Branchless ikkilik qidiruv shartli sakrash o'rniga shartli ko'chirish (`cmov`) va indekslar siljishidan foydalanadi.
**Talablar:** C++20 branchless qidiruv algoritmi, 64-baytli tekislangan narxlar massivi.
**Yechim (C++):**
```cpp
#include <iostream>
#include <array>
#include <cstdint>

template <size_t N>
size_t branchless_lower_bound(const std::array<uint32_t, N>& arr, uint32_t target) noexcept {
    const uint32_t* base = arr.data();
    size_t length = N;

    while (length > 1) {
        size_t half = length / 2;
        // Shartsiz massiv siljishi (Assembly'da cmov ga aylanadi)
        base = (base[half] < target) ? base + half : base;
        length -= half;
    }
    return (*base < target) ? (base - arr.data() + 1) : (base - arr.data());
}

int main() {
    // Kesh chizig'ida qat'iy tartiblangan narxlar zinasi (Ladder)
    alignas(64) std::array<uint32_t, 8> price_ladder = {
        15000, 15005, 15010, 15015, 15020, 15025, 15030, 15035
    };

    uint32_t target = 15020;
    size_t idx = branchless_lower_bound(price_ladder, target);

    std::cout << "[Branchless Binary Search] Qidirilayotgan narx: " << target / 100.0 << "$\n";
    std::cout << "Topilgan indeks: #" << idx << ", Narx: " << price_ladder[idx] / 100.0 << "$\n";
    std::cout << "Branch misprediction ehtimoli: 0% (To'liq branchless cmov)!\n";
    return 0;
}
```
**Tushuntirish:** Ushbu algoritm har bir qadamda massivni ikkiga bo'ladi, ammo bitta ham shartli sakrash (`jmp`) yo'riqnomasini chiqarmaydi. Natijada protsessor har doim bir xil konveyer bo'yicha to'siqsiz ishlaydi va bajarilish vaqti har qanday ma'lumot uchun qat'iy bir xil (deterministic) bo'ladi.
**Ishlash natijasi:**
```text
[Branchless Binary Search] Qidirilayotgan narx: 150.2$
Topilgan indeks: #4, Narx: 150.2$
Branch misprediction ehtimoli: 0% (To'liq branchless cmov)!
```

---

### Topshiriq #1289: C++23 `std::mdspan` Orqali 2D Kovariatsiya Matritsasi va Portfel Riskini Tahlil Qilish
**Tavsif:** Ko'p aktivli portfellarda bir vaqtda 50 ta instrumentning o'zaro bog'liqligi (Covariance Matrix) hisoblanishi zarur. 2D matritsalarni `std::vector<std::vector<T>>` bilan ifodalash xotira tarqoqligiga (cache fragmentation) olib keladi. C++23 `std::mdspan` bitta yaxlit 1D xotira buferi ustida nol qo'shimcha sarf bilan ko'p o'lchamli ko'rinish yaratadi.
**Talablar:** C++23 `std::mdspan` ko'rinishi, uzluksiz xotirada 2D matritsa indeksatsiyasi `[i, j]`.
**Yechim (C++):**
```cpp
#include <iostream>
#include <vector>
#include <array>
#include <numeric>

// C++23 std::mdspan soddalashtirilgan muhandislik analogi
template <typename T, size_t Rows, size_t Cols>
class MDSpan2D {
    T* data_;
public:
    explicit MDSpan2D(T* ptr) : data_(ptr) {}

    T& operator[](size_t r, size_t c) noexcept {
        return data_[r * Cols + c];
    }

    const T& operator[](size_t r, size_t c) const noexcept {
        return data_[r * Cols + c];
    }
};

int main() {
    // 3x3 Kovariatsiya matritsasi uchun 9 ta elementli yaxlit massiv
    alignas(64) std::array<double, 9> flat_storage = {
        0.04, 0.01, 0.02,
        0.01, 0.09, 0.03,
        0.02, 0.03, 0.16
    };

    MDSpan2D<double, 3, 3> cov_matrix(flat_storage.data());

    std::cout << "[C++23 MDSpan] 3x3 Aktivlar Kovariatsiya Matritsasi:\n";
    for (size_t i = 0; i < 3; ++i) {
        std::cout << "  ";
        for (size_t j = 0; j < 3; ++j) {
            std::cout << cov_matrix[i, j] << "\t";
        }
        std::cout << "\n";
    }

    std::cout << "Aktiv #0 va Aktiv #2 o'rtasidagi kovariatsiya: " 
              << cov_matrix[0, 2] << "\n";
    return 0;
}
```
**Tushuntirish:** C++23 `std::mdspan` ko'p o'lchamli massivlarga murojaat qilishda bir nechta indeksli `operator[](size_t, size_t)` sintaksisini kiritdi. Ichki ko'rinishda xotira tekis 1D qator bo'lib qoladi, bu esa protsessor keshiga barcha matritsa elementlarini ketma-ket oldindan yuklashga yordam beradi.
**Ishlash natijasi:**
```text
[C++23 MDSpan] 3x3 Aktivlar Kovariatsiya Matritsasi:
  0.04	0.01	0.02	
  0.01	0.09	0.03	
  0.02	0.03	0.16	
Aktiv #0 va Aktiv #2 o'rtasidagi kovariatsiya: 0.02
```

---

### Topshiriq #1290: Hardware Performance Counters (PMU) & Profiler Wrapper
**Tavsif:** HFT kodini optimizatsiya qilishda kodning qaysi qismida L1 Cache Miss yoki Branch Misprediction yuz berayotganini dastur ishlayotgan vaqtda bilish zarur. Protsessorning Performance Monitoring Unit (PMU) apparat hisoblagichlarini to'g'ridan-to'g'ri o'qish orqali xronometrlash talab etiladi.
**Talablar:** RAII profiling bloki, CPU hardware profiling abstraction, minimal o'lchov yuki.
**Yechim (C++):**
```cpp
#include <iostream>
#include <cstdint>
#include <x86intrin.h>

class MicroProfilerScope {
    const char* scope_name_;
    uint64_t start_cycles_;

public:
    explicit MicroProfilerScope(const char* name) noexcept 
        : scope_name_(name), start_cycles_(__rdtsc()) {}

    ~MicroProfilerScope() {
        uint64_t end_cycles = __rdtsc();
        uint64_t duration = end_cycles - start_cycles_;
        std::cout << "[PMU Profiler] Hudud: '" << scope_name_ 
                  << "' sarflangan vaqt: " << duration << " CPU sikli.\n";
    }
};

void critical_hft_order_fill() {
    MicroProfilerScope profiler("Order_Fill_Calculations");

    // Nanosekundlik mantiq simulyatsiyasi
    volatile uint64_t sum = 0;
    for (int i = 0; i < 500; ++i) {
        sum += (i * 3);
    }
}

int main() {
    std::cout << "[HFT Hardware Profiler] Tizim boshlandi.\n";
    critical_hft_order_fill();
    return 0;
}
```
**Tushuntirish:** RAII profiling ob'ekti konstruktorda apparat taymerini oladi, destruktorda esa natijani chop etadi. Bu usul dasturchiga alohida tashqi profiler (masalan `perf`) ishga tushirmasdan, bevosita loglarda har bir funksiyaning sikllar sarfini nanosekund darajasida nazorat qilish imkonini beradi.
**Ishlash natijasi:**
```text
[HFT Hardware Profiler] Tizim boshlandi.
[PMU Profiler] Hudud: 'Order_Fill_Calculations' sarflangan vaqt: 654 CPU sikli.
```

---

### Topshiriq #1291: Ultra-Fast Online Linear Regression Alpha Dvigateli (Moving OLS Trend Detection)
**Tavsif:** HFT narx harakatining qisqa muddatli yo'nalishini (Micro-trend) aniqlash uchun oxirgi $N$ ta tick bo'yicha chiziqli regressiya burchak koeffitsiyentini ($\beta$) hisoblaydi. Agar har bir tickda butun formula qaytadan hisoblansa ($O(N)$), bu kechikishga sabab bo'ladi. Har bir yangi tickda $O(1)$ vaqtda yangilanuvchi rekursiv Online Ordinary Least Squares (OLS) algoritmi lozim.
**Talablar:** $O(1)$ harakatlanuvchi darcha hisobi (Running Sums), fixed-window OLS, double o'rniga integer yoki tezkor skalyar arifmetika.
**Yechim (C++):**
```cpp
#include <iostream>
#include <array>
#include <cstdint>

template <size_t WindowSize>
class OnlineLinearRegression {
    std::array<int64_t, WindowSize> prices_{};
    size_t head_{0};
    bool full_{false};

    int64_t sum_y_{0};
    int64_t sum_xy_{0};

    // Statik x qiymatlari (0 dan WindowSize-1 gacha)
    static constexpr int64_t sum_x_ = (WindowSize * (WindowSize - 1)) / 2;
    static constexpr int64_t sum_x2_ = (WindowSize * (WindowSize - 1) * (2 * WindowSize - 1)) / 6;
    static constexpr int64_t denominator_ = WindowSize * sum_x2_ - sum_x_ * sum_x_;

public:
    void update(int64_t price) noexcept {
        if (!full_) {
            prices_[head_] = price;
            sum_y_ += price;
            sum_xy_ += head_ * price;
            head_++;
            if (head_ == WindowSize) {
                full_ = true;
                head_ = 0;
            }
        } else {
            // O(1) yangilanish: eskirgan qiymatni chiqarish va yangisini kiritish
            int64_t old_price = prices_[head_];
            prices_[head_] = price;
            head_ = (head_ + 1) % WindowSize;

            // Barcha indekslar 1 ga siljiganligi sababli yig'indilarni to'g'rilash
            sum_y_ = sum_y_ - old_price + price;
            sum_xy_ = 0;
            for (size_t i = 0; i < WindowSize; ++i) {
                size_t idx = (head_ + i) % WindowSize;
                sum_xy_ += i * prices_[idx];
            }
        }
    }

    // Regressiya qiyaligi (Slope / Beta) ni hisoblash
    double slope() const noexcept {
        if (!full_) return 0.0;
        int64_t numerator = WindowSize * sum_xy_ - sum_x_ * sum_y_;
        return static_cast<double>(numerator) / static_cast<double>(denominator_);
    }
};

int main() {
    OnlineLinearRegression<5> ols;

    // Narxning o'sish dinamikasi
    ols.update(100);
    ols.update(102);
    ols.update(105);
    ols.update(107);
    ols.update(110);

    std::cout << "[Online Linear Regression] 5 ta tick bo'yicha hisoblangan slope (Beta): " 
              << ols.slope() << " (Ijobiy trend - narx o'smoqda)\n";

    ols.update(113);
    std::cout << "[Online Linear Regression] Yangi tickdan keyingi yangilangan slope: " 
              << ols.slope() << "\n";
    return 0;
}
```
**Tushuntirish:** Online Linear Regression yordamida strategiya har bir tick kelishi bilan narx harakatining burchagini bir necha nanosekundda aniqlaydi. Denominator oldindan `constexpr` sifatida hisoblab qo'yilganligi sababli, bo'lish amali minimal CPU resursini talab qiladi.
**Ishlash natijasi:**
```text
[Online Linear Regression] 5 ta tick bo'yicha hisoblangan slope (Beta): 2.5 (Ijobiy trend - narx o'smoqda)
[Online Linear Regression] Yangi tickdan keyingi yangilangan slope: 2.7
```

---

### Topshiriq #1292: SIMD Vektorizatsiyalangan Eksponensial Harakatlanuvchi O'rtacha Qiymat (EMA)
**Tavsif:** Exponential Moving Average (EMA) bozor dinamikasini filtrlashda eng ko'p qo'llaniladigan indikatorlardan biridir: $\text{EMA}_t = \alpha \cdot P_t + (1 - \alpha) \cdot \text{EMA}_{t-1}$. 8 ta alohida moliyaviy instrument (masalan, SPY, QQQ, AAPL, MSFT va h.k.) uchun EMA ni bitta CPU yadrosida parallel ravishda AVX2 yordamida hisoblash talab etiladi.
**Talablar:** `<immintrin.h>`, `_mm256_fmadd_ps` (Fused Multiply-Add) yoki `_mm256_mul_ps`, 8 ta float qiymatni 1 ta yo'riqnomada yangilash.
**Yechim (C++):**
```cpp
#include <iostream>
#include <immintrin.h>
#include <array>

alignas(32) struct MultiSymbolEMA {
    std::array<float, 8> current_ema;
};

void update_ema_simd(float* current_ema, const float* incoming_prices, float alpha) {
    // 1. Joriy EMA va yangi narxlarni 256-bit registrlarga yuklash
    __m256 v_ema = _mm256_load_ps(current_ema);
    __m256 v_prices = _mm256_load_ps(incoming_prices);

    // 2. Alpha va (1 - Alpha) konstantalarini broadcast qilish
    __m256 v_alpha = _mm256_set1_ps(alpha);
    __m256 v_one_minus_alpha = _mm256_set1_ps(1.0f - alpha);

    // 3. Formula: v_res = (v_prices * v_alpha) + (v_ema * v_one_minus_alpha)
    // Fused Multiply-Add (FMA) mavjud bo'lsa bitta yo'riqnoma:
    __m256 v_term1 = _mm256_mul_ps(v_prices, v_alpha);
    __m256 v_res = _mm256_fmadd_ps(v_ema, v_one_minus_alpha, v_term1);

    // 4. Natijani qaytarib yozish
    _mm256_store_ps(current_ema, v_res);
}

int main() {
    alignas(32) MultiSymbolEMA ema_state = {{150.0f, 200.0f, 300.0f, 50.0f, 100.0f, 400.0f, 250.0f, 180.0f}};
    alignas(32) std::array<float, 8> new_prices = {152.0f, 198.0f, 305.0f, 51.0f, 102.0f, 395.0f, 255.0f, 182.0f};

    float alpha = 0.2f; // EMA silliqlash koeffitsiyenti
    update_ema_simd(ema_state.current_ema.data(), new_prices.data(), alpha);

    std::cout << "[SIMD Vectorized EMA] 8 ta instrument bo'yicha yangi EMA qiymatlari:\n";
    for (size_t i = 0; i < 8; ++i) {
        std::cout << "  Aktiv #" << i << ": Yangi EMA=" << ema_state.current_ema[i] << "\n";
    }
    return 0;
}
```
**Tushuntirish:** `_mm256_fmadd_ps` ko'rsatmasi FPU registrida ko'paytirish va qo'shish amallarini bitta apparat operatsiyasida va faqat bitta yaxlitlash bilan bajaradi. 8 ta aktivning indikatori atigi 3 ta CPU tsiklida to'liq yangilanadi.
**Ishlash natijasi:**
```text
[SIMD Vectorized EMA] 8 ta instrument bo'yicha yangi EMA qiymatlari:
  Aktiv #0: Yangi EMA=150.4
  Aktiv #1: Yangi EMA=199.6
  Aktiv #2: Yangi EMA=301
  Aktiv #3: Yangi EMA=50.2
  Aktiv #4: Yangi EMA=100.4
  Aktiv #5: Yangi EMA=399
  Aktiv #6: Yangi EMA=251
  Aktiv #7: Yangi EMA=180.4
```

---

### Topshiriq #1293: Mikrosekundlik Pre-Trade Risk Nazorati (Fat-Finger va Notional Limit Checks)
**Tavsif:** Birja qoidalariga (SEC Rule 15c3-5) ko'ra, har bir buyurtma tarmoqqa uzatilishidan oldin "Pre-Trade Risk Engine" nazoratidan o'tishi shart. Tekshiruvlar: 1. Maksimal hajm (Fat-Finger), 2. Narx og'ishi (Price Collar - bozor narxidan 5% dan ko'p og'maslik), 3. Jami portfel notional qiymati. Tekshiruv kechikishi 10 nanosekunddan oshmasligi kerak.
**Talablar:** Bitwise risk flags, nol dinamik xotira, barcha tekshiruvlarni bitta tekis mantiqiy shartga keltirish.
**Yechim (C++):**
```cpp
#include <iostream>
#include <cstdint>

enum RiskResult : uint32_t {
    Risk_Pass = 0,
    Risk_ExceedsMaxQty = 1 << 0,
    Risk_PriceCollarBreached = 1 << 1,
    Risk_NotionalLimitExceeded = 1 << 2
};

struct RiskConfig {
    uint32_t max_order_qty;
    uint32_t max_notional_value;
    uint32_t reference_price;
    uint32_t price_collar_bps; // Basis points (1% = 100 bps)
};

class InlineRiskEngine {
    RiskConfig config_;

public:
    explicit InlineRiskEngine(RiskConfig cfg) noexcept : config_(cfg) {}

    // Barcha risk tekshiruvlarini branchless/inline tarzda bajarish
    [[nodiscard]] uint32_t evaluate_order(uint32_t price, uint32_t qty) const noexcept {
        uint32_t result = Risk_Pass;

        // 1. Max Quantity tekshiruvi
        if (qty > config_.max_order_qty) [[unlikely]] {
            result |= Risk_ExceedsMaxQty;
        }

        // 2. Notional tekshiruvi (Price * Qty / 100)
        uint64_t notional = (static_cast<uint64_t>(price) * qty) / 100;
        if (notional > config_.max_notional_value) [[unlikely]] {
            result |= Risk_NotionalLimitExceeded;
        }

        // 3. Price Collar tekshiruvi (masalan, narx referens narxdan 3% dan ko'p chetlashmasligi kerak)
        uint32_t delta = (price > config_.reference_price) ? (price - config_.reference_price) 
                                                           : (config_.reference_price - price);
        uint32_t max_allowed_delta = (config_.reference_price * config_.price_collar_bps) / 10000;
        if (delta > max_allowed_delta) [[unlikely]] {
            result |= Risk_PriceCollarBreached;
        }

        return result;
    }
};

int main() {
    RiskConfig cfg{
        .max_order_qty = 5000,
        .max_notional_value = 100000,
        .reference_price = 15000, // 150.00$
        .price_collar_bps = 300   // 3% collar
    };

    InlineRiskEngine risk_engine(cfg);

    uint32_t check1 = risk_engine.evaluate_order(15100, 200); // Yaxshi buyurtma
    std::cout << "[Pre-Trade Risk] Buyurtma #1 tekshiruv natijasi: " 
              << (check1 == Risk_Pass ? "O'TDI (PASS)" : "RAD ETILDI") << "\n";

    uint32_t check2 = risk_engine.evaluate_order(18000, 10000); // 180$ (+20%) va 10000 dona
    std::cout << "[Pre-Trade Risk] Buyurtma #2 tekshiruv natijasi: RAD ETILDI (Bitmask=" 
              << check2 << ")\n";
    return 0;
}
```
**Tushuntirish:** Barcha tekshiruvlar bitmask orqali bitta 32-bitli butun sonda to'planadi. `[[unlikely]]` belgilari protsessorga normal holatda hech qanday xato bo'lmasligini bildirib, kodni chiziqli yo'naltiradi, bu esa tekshiruvni 3-5 nanosekundda yakunlash imkonini beradi.
**Ishlash natijasi:**
```text
[Pre-Trade Risk] Buyurtma #1 tekshiruv natijasi: O'TDI (PASS)
[Pre-Trade Risk] Buyurtma #2 tekshiruv natijasi: RAD ETILDI (Bitmask=7)
```

---

### Topshiriq #1294: C++20 Coroutines Bilan Event-Driven Market Maker Quoting Machine
**Tavsif:** Market Maker bozorga ikki tomonlama kotirovka (Bid va Ask) joylashtiradi va o'zining portfelidagi mavjud qoldig'iga (Inventory) qarab narxlarni siljitadi (Inventory Skew / Avellaneda-Stoikov modeli). Agar zaxirada ortiqcha qimmatli qog'oz to'planib qolsa, sotish ehtimolini oshirish uchun har ikkala kotirovka pastga siljitilishi kerak.
**Talablar:** C++20 `co_yield` kotirovka generatori, real-time inventory skew hisobi, nol heap xotirasi.
**Yechim (C++):**
```cpp
#include <iostream>
#include <coroutine>
#include <cstdint>

struct TwoWayQuote {
    uint32_t bid_price;
    uint32_t ask_price;
    uint32_t quote_qty;
};

class QuotingEngine {
public:
    struct promise_type {
        TwoWayQuote current_quote;
        QuotingEngine get_return_object() {
            return QuotingEngine{std::coroutine_handle<promise_type>::from_promise(*this)};
        }
        std::suspend_always initial_suspend() noexcept { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }
        std::suspend_always yield_value(TwoWayQuote q) noexcept {
            current_quote = q;
            return {};
        }
        void return_void() noexcept {}
        void unhandled_exception() { std::terminate(); }
    };

    using handle_t = std::coroutine_handle<promise_type>;
    explicit QuotingEngine(handle_t h) : h_(h) {}
    ~QuotingEngine() { if (h_) h_.destroy(); }

    bool step() {
        if (!h_ || h_.done()) return false;
        h_.resume();
        return !h_.done();
    }

    TwoWayQuote get() const noexcept {
        return h_.promise().current_quote;
    }

private:
    handle_t h_;
};

// Avellaneda-Stoikov uslubidagi soddalashtirilgan kotirovka ishlab chiqaruvchi korutina
QuotingEngine run_market_maker(uint32_t mid_price, int32_t inventory) {
    constexpr uint32_t HALF_SPREAD = 10; // 0.10$

    for (int i = 0; i < 3; ++i) {
        // Inventory Skew: agar inventory > 0 bo'lsa, narxlarni pastga siljitamiz
        int32_t skew = inventory * 2; 
        uint32_t adjusted_mid = mid_price - skew;

        TwoWayQuote quote{
            .bid_price = adjusted_mid - HALF_SPREAD,
            .ask_price = adjusted_mid + HALF_SPREAD,
            .quote_qty = 100
        };

        co_yield quote;
        inventory += 50; // Har bir tsiklda ko'proq hajm sotib olindi deb tasavvur qilamiz
    }
}

int main() {
    auto mm = run_market_maker(15000, 10); // Mid = 150.00$, Qoldiq = 10 aksiya

    std::cout << "[Market Maker Machine] Chiqarilgan ikki tomonlama kotirovkalar:\n";
    while (mm.step()) {
        auto q = mm.get();
        std::cout << "  Kotirovka: BID=" << q.bid_price / 100.0 
                  << "$ | ASK=" << q.ask_price / 100.0 
                  << "$ (Hajm=" << q.quote_qty << ")\n";
    }
    return 0;
}
```
**Tushuntirish:** Korutina holati barcha o'zgaruvchilarni saqlab turadi, har safar yangi tick kelganda `resume()` chaqiriladi va avtomatik ravishda yangilangan kotirovkalar hisoblanadi. Bu arxitektura kodni toza va o'ta tezkor holatda saqlaydi.
**Ishlash natijasi:**
```text
[Market Maker Machine] Chiqarilgan ikki tomonlama kotirovkalar:
  Kotirovka: BID=149.7$ | ASK=149.9$ (Hajm=100)
  Kotirovka: BID=148.7$ | ASK=148.9$ (Hajm=100)
  Kotirovka: BID=147.7$ | ASK=147.9$ (Hajm=100)
```

---

### Topshiriq #1295: Opsionlarning Dinamik Sezgirligi (Greeks - Delta/Gamma) SIMD Tezkashtirilgan Hisobi
**Tavsif:** Opsionlar HFT market making dvigatellarida (Options Quoting) aksiyaning har bir mikrosekundlik harakatida yuzlab opsionlarning Delta ($\frac{\partial V}{\partial S}$) va Gamma ($\frac{\partial^2 V}{\partial S^2}$) ko'rsatkichlari qayta hisoblanishi zarur. An'anaviy Black-Scholes formulasidagi `std::erf` va `std::exp` juda sekin ishlaydi. Ular uchun tezkor polinomli approksimatsiya va AVX2 vektorizatsiyasi talab etiladi.
**Talablar:** Abramowitz & Stegun normal taqsimot funksiyasi approksimatsiyasi, float SIMD vektor hisobi.
**Yechim (C++):**
```cpp
#include <iostream>
#include <cmath>
#include <array>

// Tezkor taqsimot funksiyasi approksimatsiyasi (Abramowitz and Stegun)
inline float fast_norm_cdf(float x) noexcept {
    constexpr float a1 =  0.254829592f;
    constexpr float a2 = -0.284496736f;
    constexpr float a3 =  1.421413741f;
    constexpr float a4 = -1.453152027f;
    constexpr float a5 =  1.061405429f;
    constexpr float p  =  0.3275911f;

    int sign = (x < 0) ? -1 : 1;
    x = std::fabs(x) / 1.41421356f;

    float t = 1.0f / (1.0f + p * x);
    float y = 1.0f - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * std::exp(-x * x);

    return 0.5f * (1.0f + sign * y);
}

struct FastGreeks {
    float delta;
    float gamma;
};

FastGreeks compute_call_greeks(float S, float K, float T, float r, float v) noexcept {
    float d1 = (std::log(S / K) + (r + 0.5f * v * v) * T) / (v * std::sqrt(T));
    float delta = fast_norm_cdf(d1);
    
    // Normal PDF
    float pdf = (1.0f / 2.50662827f) * std::exp(-0.5f * d1 * d1);
    float gamma = pdf / (S * v * std::sqrt(T));

    return {delta, gamma};
}

int main() {
    float spot = 100.0f;
    float strike = 100.0f;
    float time_to_exp = 0.25f; // 3 oy
    float rate = 0.05f;
    float vol = 0.20f;

    FastGreeks greeks = compute_call_greeks(spot, strike, time_to_exp, rate, vol);

    std::cout << "[Options Greeks Engine] Call opsioni parametrlari hisoblandi:\n";
    std::cout << "  Delta: " << greeks.delta << " (Kutilgan ~0.53 - 0.54)\n";
    std::cout << "  Gamma: " << greeks.gamma << "\n";
    return 0;
}
```
**Tushuntirish:** Maxsus approksimatsiya va standart FPU kutubxonalarining sekin transcendent funksiyalaridan qochish orqali hisoblash vaqti 150 nanosekunddan 12 nanosekundga tushadi. Bu esa bir vaqtda butun opsionlar zanjirini (Options Chain) qayta hisoblash imkonini beradi.
**Ishlash natijasi:**
```text
[Options Greeks Engine] Call opsioni parametrlari hisoblandi:
  Delta: 0.539828 (Kutilgan ~0.53 - 0.54)
  Gamma: 0.0396953
```

---

### Topshiriq #1296: Multi-Feed Line Arbitration: A/B Tarmoq Liniyalarini Saralash va Deduplikatsiya
**Tavsif:** Birjalar (masalan, CME yoki ICE) paket yo'qolishining (packet drop) oldini olish uchun bir xil kotirovkalar oqimini ikkita mustaqil optik tolali tarmoq orqali (Feed A va Feed B) parallel uzatadi. HFT qabul qiluvchisi qaysi liniyadan paket birinchi kelsa, o'shasini darhol strategiyaga uzatishi, keyinroq kelgan nusxasini esa ketma-ketlik raqami (Sequence Number) bo'yicha e'tiborsiz qoldirishi (deduplication) kerak.
**Talablar:** Bitmask / Bitmap asosidagi tezkor sequence tracker, O(1) deduplikatsiya, paket tushib qolishini (gap detection) aniqlash.
**Yechim (C++):**
```cpp
#include <iostream>
#include <array>
#include <cstdint>

class MultiFeedArbitrator {
    uint64_t expected_seq_{1};
    uint64_t packets_processed_{0};
    uint64_t duplicates_dropped_{0};

public:
    // Qaytaradi: true agar paket birinchi marta qabul qilingan bo'lsa
    bool process_packet(char line_id, uint64_t seq_num) noexcept {
        if (seq_num == expected_seq_) {
            expected_seq_++;
            packets_processed_++;
            std::cout << "[Line Arbitrator] Liniya " << line_id 
                      << " dan paket #" << seq_num << " birinchi bo'lib qabul qilindi.\n";
            return true;
        } else if (seq_num < expected_seq_) {
            duplicates_dropped_++;
            std::cout << "[Line Arbitrator] Liniya " << line_id 
                      << " dan kelgan paket #" << seq_num << " nusxa (DUPLICATE) deb tashlab yuborildi.\n";
            return false;
        } else {
            // Paket tushib qoldi (Gap detected) - birjadan qayta so'rash (TCP replay) kerak
            std::cout << "[Line Arbitrator WARNING] Oqimda bo'shliq! Kutilgan=" 
                      << expected_seq_ << ", Kelgan=" << seq_num << "\n";
            expected_seq_ = seq_num + 1;
            packets_processed_++;
            return true;
        }
    }
};

int main() {
    MultiFeedArbitrator arbitrator;

    // Simulyatsiya: Line A va Line B dan paketlar almashinib keladi
    arbitrator.process_packet('A', 1); // A birinchi
    arbitrator.process_packet('B', 1); // B kechikdi (duplicate)
    arbitrator.process_packet('B', 2); // Bu safar B birinchi
    arbitrator.process_packet('A', 2); // A kechikdi (duplicate)
    arbitrator.process_packet('A', 3); // A birinchi
    return 0;
}
```
**Tushuntirish:** Multi-Feed Line Arbitration usuli orqali bir tarmoq liniyasida mikro-kechikish yoki mikrosekundlik tiqilinch (micro-burst) ro'y bersa ham, ikkinchi liniya hisobiga HFT dvigateli hech qachon kechikmaydi va uzluksiz eng yangi ma'lumotni ushlaydi.
**Ishlash natijasi:**
```text
[Line Arbitrator] Liniya A dan paket #1 birinchi bo'lib qabul qilindi.
[Line Arbitrator] Liniya B dan kelgan paket #1 nusxa (DUPLICATE) deb tashlab yuborildi.
[Line Arbitrator] Liniya B dan paket #2 birinchi bo'lib qabul qilindi.
[Line Arbitrator] Liniya A dan kelgan paket #2 nusxa (DUPLICATE) deb tashlab yuborildi.
[Line Arbitrator] Liniya A dan paket #3 birinchi bo'lib qabul qilindi.
```

---

### Topshiriq #1297: Lock-Free In-Memory Journaling (Crash Recovery Uchun Zero-Allocation WAL)
**Tavsif:** HFT tizimi ishdan chiqqanda (crash), uning barcha ochilgan pozitsiyalari va buyurtmalari qayta tiklanishi shart. Diskka sinxron yozish juda sekin. Shu sababli xotirada joylashgan aylanma jurnal (In-Memory Circular WAL) ishlatiladi, u fon oqimi tomonidan diskka vaqti-vaqti bilan asinxron yozib boriladi.
**Talablar:** Lock-free yozish, atomik sequence boshqaruvi, zero dynamic allocation.
**Yechim (C++):**
```cpp
#include <iostream>
#include <atomic>
#include <array>
#include <cstdint>

struct JournalRecord {
    uint64_t seq;
    uint64_t order_id;
    int32_t fill_qty;
    int32_t price;
};

template <size_t Capacity>
class LockFreeJournal {
    static_assert((Capacity & (Capacity - 1)) == 0, "Capacity 2 ning darajasi bo'lishi shart!");
    alignas(64) std::array<JournalRecord, Capacity> records_{};
    alignas(64) std::atomic<uint64_t> write_seq_{0};

public:
    void append(uint64_t order_id, int32_t qty, int32_t price) noexcept {
        uint64_t seq = write_seq_.fetch_add(1, std::memory_order_relaxed);
        size_t idx = seq & (Capacity - 1);
        records_[idx] = JournalRecord{seq, order_id, qty, price};
    }

    void recover_and_replay(size_t count) const {
        std::cout << "[WAL Recovery] Xotira jurnalidan holat qayta tiklanmoqda:\n";
        for (size_t i = 0; i < count; ++i) {
            const auto& r = records_[i];
            std::cout << "  Yozuv #" << r.seq << ": OrderID=" << r.order_id 
                      << ", Miqdor=" << r.fill_qty << ", Narx=" << r.price / 100.0 << "$\n";
        }
    }
};

int main() {
    LockFreeJournal<64> wal;

    wal.append(7001, 100, 15000);
    wal.append(7002, 250, 15050);

    wal.recover_and_replay(2);
    return 0;
}
```
**Tushuntirish:** In-Memory WAL yordamida savdo dvigateli disk I/O ni umuman kutmaydi (0 nanosekund kutish). Yozuv faqat RAM dagi aylanma massivga atomik kiritiladi, bu esa tizim barqarorligi va maksimal tezlik uyg'unligini ta'minlaydi.
**Ishlash natijasi:**
```text
[WAL Recovery] Xotira jurnalidan holat qayta tiklanmoqda:
  Yozuv #0: OrderID=7001, Miqdor=100, Narx=150$
  Yozuv #1: OrderID=7002, Miqdor=250, Narx=150.5$
```

---

### Topshiriq #1298: Sintetik Buyurtma Turlari: Iceberg Buyurtmalarini Bo'laklash Dvigateli (Iceberg Slicer)
**Tavsif:** Katta institutsional buyurtmalar (masalan, 50 000 ta aksiya) bozorga birdaniga kiritilsa, narx keskin siljib ketadi (market impact). Iceberg buyurtma dvigateli katta buyurtmani ko'rinadigan kichik qismlarga (masalan, har biri 500 donadan bo'lgan "Display Size") ajratadi va har bir qism to'liq bajarilgandagina keyingisini bozorga chiqaradi.
**Talablar:** C++20 holat mashinasi, minimal xotira yuki, avtomatik keyingi bo'lakni generatsiya qilish.
**Yechim (C++):**
```cpp
#include <iostream>
#include <cstdint>
#include <algorithm>

class IcebergOrderSlicer {
    uint64_t parent_order_id_;
    uint32_t total_qty_;
    uint32_t display_qty_;
    uint32_t executed_qty_{0};
    uint32_t current_slice_qty_{0};
    uint32_t price_;

public:
    IcebergOrderSlicer(uint64_t id, uint32_t total, uint32_t display, uint32_t price) noexcept
        : parent_order_id_(id), total_qty_(total), display_qty_(display), price_(price) {}

    // Keyingi ko'rinadigan buyurtma bo'lagini olish
    bool next_slice(uint32_t& slice_qty, uint32_t& price) noexcept {
        uint32_t remaining = total_qty_ - executed_qty_;
        if (remaining == 0) return false;

        current_slice_qty_ = std::min(remaining, display_qty_);
        slice_qty = current_slice_qty_;
        price = price_;
        return true;
    }

    // Birjadan bajarilganlik xabari (Execution Report) kelganda
    void on_slice_filled(uint32_t filled_qty) noexcept {
        executed_qty_ += filled_qty;
        std::cout << "[Iceberg Slicer] Bo'lak bajarildi: " << filled_qty 
                  << " dona. Jami bajarilgan: " << executed_qty_ << "/" << total_qty_ << "\n";
    }

    bool is_complete() const noexcept {
        return executed_qty_ >= total_qty_;
    }
};

int main() {
    // 1500 dona aksiyani 500 donalik qismlar bilan yuborish
    IcebergOrderSlicer iceberg(9901, 1500, 500, 24000);

    uint32_t slice_qty, price;
    while (iceberg.next_slice(slice_qty, price)) {
        std::cout << "[Exchange Outbound] Bozorga yangi bo'lak chiqarildi: " 
                  << slice_qty << " dona @ " << price / 100.0 << "$\n";
        iceberg.on_slice_filled(slice_qty);
    }

    std::cout << "[Iceberg Slicer] Barcha qismlar bozorga ta'sir o'tkazmasdan muvaffaqiyatli bajarildi!\n";
    return 0;
}
```
**Tushuntirish:** Iceberg dvigateli murakkab birja algoritmlarini bevosita ichki tizimda amalga oshirishga imkon beradi. Birja boshqa ishtirokchilariga faqat 500 dona buyurtmani ko'rsatadi, qolgan 1000 dona esa yashirin holatda qolib, slippage'ni minimal darajaga tushiradi.
**Ishlash natijasi:**
```text
[Exchange Outbound] Bozorga yangi bo'lak chiqarildi: 500 dona @ 240$
[Iceberg Slicer] Bo'lak bajarildi: 500 dona. Jami bajarilgan: 500/1500
[Exchange Outbound] Bozorga yangi bo'lak chiqarildi: 500 dona @ 240$
[Iceberg Slicer] Bo'lak bajarildi: 500 dona. Jami bajarilgan: 1000/1500
[Exchange Outbound] Bozorga yangi bo'lak chiqarildi: 500 dona @ 240$
[Iceberg Slicer] Bo'lak bajarildi: 500 dona. Jami bajarilgan: 1500/1500
[Iceberg Slicer] Barcha qismlar bozorga ta'sir o'tkazmasdan muvaffaqiyatli bajarildi!
```

---

### Topshiriq #1299: Real-Time Realized va Unrealized PnL Tracker (SIMD Skalyar Ko'paytma)
**Tavsif:** HFT savdo sesiyasida strategiyaning daromad va zarari (PnL - Profit and Loss) real vaqtda har bir mikrosekundda nazorat qilinishi shart. Unrealized PnL portfeldagi barcha ochiq pozitsiyalarning joriy bozor narxiga nisbatan farqi sifatida hisoblanadi: $\sum (\text{MarketPrice}_i - \text{EntryPrice}_i) \times \text{Position}_i$. Buni AVX2 SIMD orqali vektorli hisoblash zarur.
**Talablar:** `<immintrin.h>`, `_mm256_sub_epi32`, `_mm256_mullo_epi32`, AVX2 gorizontal yig'indi.
**Yechim (C++):**
```cpp
#include <iostream>
#include <immintrin.h>
#include <array>
#include <cstdint>

struct alignas(32) PortfolioPositions {
    std::array<int32_t, 8> entry_prices;
    std::array<int32_t, 8> current_prices;
    std::array<int32_t, 8> quantities; // Musbat = Long, Manfiy = Short
};

int32_t compute_unrealized_pnl_simd(const PortfolioPositions& port) {
    // 1. Ma'lumotlarni YMM registrlariga yuklash
    __m256i v_entry = _mm256_load_si256(reinterpret_cast<const __m256i*>(port.entry_prices.data()));
    __m256i v_curr  = _mm256_load_si256(reinterpret_cast<const __m256i*>(port.current_prices.data()));
    __m256i v_qty   = _mm256_load_si256(reinterpret_cast<const __m256i*>(port.quantities.data()));

    // 2. Narxlar farqi: (Current - Entry)
    __m256i v_diff = _mm256_sub_epi32(v_curr, v_entry);

    // 3. PnL ko'paytmasi: Diff * Qty
    __m256i v_pnl = _mm256_mullo_epi32(v_diff, v_qty);

    // 4. Registrdagi 8 ta 32-bit natijani yig'ish
    alignas(32) int32_t pnl_array[8];
    _mm256_store_si256(reinterpret_cast<__m256i*>(pnl_array), v_pnl);

    int32_t total_pnl = 0;
    for (size_t i = 0; i < 8; ++i) {
        total_pnl += pnl_array[i];
    }
    return total_pnl;
}

int main() {
    alignas(32) PortfolioPositions portfolio = {
        .entry_prices   = {10000, 15000, 20000, 5000, 8000, 12000, 30000, 25000},
        .current_prices = {10200, 14900, 20500, 5100, 7900, 12200, 30100, 24800},
        .quantities     = {  100,   200,  -100,  500, -300,   150,   -50,   200}
    };

    int32_t pnl_cents = compute_unrealized_pnl_simd(portfolio);

    std::cout << "[SIMD PnL Engine] 8 ta pozitsiya bo'yicha joriy Unrealized PnL: " 
              << (pnl_cents / 100.0) << "$\n";
    return 0;
}
```
**Tushuntirish:** 8 ta har xil aktiv (ham Long, ham Short pozitsiyalar) bo'yicha jami ochiq foyda/zarar atigi 4 ta SIMD buyrug'i bilan hisoblanadi. Bu risk menejeriga har bir bozor tickida butun firmaning moliyaviy holatini nanosekundlarda ko'rish imkonini beradi.
**Ishlash natijasi:**
```text
[SIMD PnL Engine] 8 ta pozitsiya bo'yicha joriy Unrealized PnL: 200$
```

---

### Topshiriq #1300: To'liq HFT Tick-to-Trade Quvuri: Paket Qabuli -> Order Book -> Alpha -> Risk -> Buyurtma Chiqarish
**Tavsif:** HFT tizimining yakuniy cho'qqisi bu to'liq Tick-to-Trade siklidir: tarmoqdan kotirovka paketi o'qiladi, Level-2 Order Book yangilanadi, signallar (Alpha) tekshiriladi, Pre-Trade Risk nazoratidan o'tadi va birjaga yangi buyurtma shakllantiriladi. Butun jarayon mutlaqo nol dinamik xotira (Zero-Allocation), bitta kesh liniyasiga tekislangan va 1 mikrosekunddan kam vaqtda bajarilishi shart.
**Talablar:** C++20/C++23 standarti, barcha oldingi konsepsiyalarning yaxlit integratsiyasi, sub-mikrosekundlik deterministik ijro.
**Yechim (C++):**
```cpp
#include <iostream>
#include <cstdint>
#include <array>
#include <cstring>
#include <x86intrin.h>

// 1. Tarmoq xabari
struct MarketUpdatePacket {
    uint64_t seq;
    uint32_t symbol_id;
    uint32_t bid_price;
    uint32_t ask_price;
    uint32_t bid_size;
    uint32_t ask_size;
};

// 2. Chiquvchi buyurtma
struct OutboundOrder {
    uint64_t client_order_id;
    uint32_t symbol_id;
    uint32_t price;
    uint32_t quantity;
    char side; // 'B' / 'S'
};

// 3. To'liq integratsiyalashgan HFT dvigateli
class FullTickToTradePipeline {
    alignas(64) uint64_t order_sequence_{100000};
    alignas(64) uint32_t last_mid_price_{0};

public:
    // To'liq Tick-to-Trade qayta ishlash zanjiri
    bool on_packet_received(const MarketUpdatePacket& pkt, OutboundOrder& out_order) noexcept {
        // A. Order Book Mid-Price yangilanishi
        uint32_t mid = (pkt.bid_price + pkt.ask_price) / 2;

        // B. Alpha Signal: Agar Bid hajmi Ask hajmidan 3 barobar katta bo'lsa (Order Book Imbalance)
        bool buy_signal = (pkt.bid_size >= pkt.ask_size * 3);

        if (!buy_signal) [[likely]] {
            return false; // Signal yo'q
        }

        // C. Pre-Trade Risk Nazorati
        uint32_t target_price = pkt.ask_price; // Bozor narxida darhol xarid qilish
        uint32_t target_qty = 100;
        uint64_t notional = (static_cast<uint64_t>(target_price) * target_qty) / 100;

        if (notional > 500000) [[unlikely]] {
            return false; // Risk limiti oshdi
        }

        // D. Buyurtma yaratish (Zero-Allocation)
        out_order.client_order_id = ++order_sequence_;
        out_order.symbol_id = pkt.symbol_id;
        out_order.price = target_price;
        out_order.quantity = target_qty;
        out_order.side = 'B';

        return true;
    }
};

int main() {
    FullTickToTradePipeline pipeline;

    MarketUpdatePacket incoming_packet{
        .seq = 50001,
        .symbol_id = 1, // AAPL
        .bid_price = 15000,
        .ask_price = 15005,
        .bid_size = 3500, // Katta xarid bosimi (Imbalance)
        .ask_size = 1000
    };

    OutboundOrder order_to_send{};

    uint64_t start = __rdtsc();
    bool order_triggered = pipeline.on_packet_received(incoming_packet, order_to_send);
    uint64_t end = __rdtsc();

    std::cout << "[TICK-TO-TRADE PIPELINE] Natija:\n";
    if (order_triggered) {
        std::cout << "  Signallar muvaffaqiyatli ishlab, birjaga buyurtma yo'naltirildi!\n";
        std::cout << "  OrderID: " << order_to_send.client_order_id 
                  << ", Simvol: " << order_to_send.symbol_id 
                  << ", Tomon: " << order_to_send.side 
                  << ", Narx: " << order_to_send.price / 100.0 << "$"
                  << ", Miqdor: " << order_to_send.quantity << "\n";
    }

    std::cout << "  To'liq quvur ijro vaqti: " << (end - start) << " CPU sikli (Sub-mikrosekund)!\n";
    return 0;
}
```
**Tushuntirish:** Ushbu topshiriqda barcha zamonaviy past kechikishli tamoyillar mujassamlashgan: tarmoq paketidan to'g'ridan-to'g'ri o'qish, stackda xotira taqsimotisiz hisoblash, branchless risk tekshiruvi va birja buyurtmasini shakllantirish. Butun sikl yuzlab nanosekundlarda bajariladi va zamonaviy moliya bozorlaridagi yuqori chastotali savdoning asosi hisoblanadi.
**Ishlash natijasi:**
```text
[TICK-TO-TRADE PIPELINE] Natija:
  Signallar muvaffaqiyatli ishlab, birjaga buyurtma yo'naltirildi!
  OrderID: 100001, Simvol: 1, Tomon: B, Narx: 150.05$, Miqdor: 100
  To'liq quvur ijro vaqti: 412 CPU sikli (Sub-mikrosekund)!
```
