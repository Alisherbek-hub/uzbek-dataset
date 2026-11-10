# C++ Dasturlash Tili - 16-Qism: Ko'p Oqimlilik (Multithreading), Sinxronizatsiya va Parallelizm

Ushbu qismda std::thread, mutex, lock_guard, unique_lock, scoped_lock, atomic, condition_variable, async/future, jthread, C++20 semaphores/latches va Thread Pool ga oid 50 ta amaliy topshiriq jamlangan.

---

# 751-Topshiriq: std::thread asoslari va oqim yaratish

## Topshiriq sharti:
Alohida oqimda funksiyani ishga tushirib, `.join()` orqali uning tugashini kuting.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <thread>

void oqimVazifasi() {
    std::cout << "Yordamchi oqim ishlamoqda...\n";
}

int main() {
    std::thread t(oqimVazifasi);
    t.join(); // Tugashini kutish majburiy
    std::cout << "Asosiy oqim davom etmoqda.\n";
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::thread` alohida OS oqimini yaratadi. `.join()` asosiy oqimni yordamchi oqim tugaguncha to'xtatib turadi.

## Ishlash natijasi:
```text
Yordamchi oqim ishlamoqda...\nAsosiy oqim davom etmoqda.
```

---

# 752-Topshiriq: Oqimga parametrlarni uzatish (std::ref)

## Topshiriq sharti:
Oqimga parametrlarni qiymat va havola (`std::ref`) bo'yicha uzatishni ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <thread>

void oshir(int& son) {
    son += 50;
}

int main() {
    int x = 10;
    std::thread t(oshir, std::ref(x)); // Havola uchun std::ref shart
    t.join();
    std::cout << "x ning yangi qiymati: " << x << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::thread` konstruktori parametrlarni nusxalaydi, shuning uchun havolalar uchun `std::ref` ishlatiladi.

## Ishlash natijasi:
```text
x ning yangi qiymati: 60
```

---

# 753-Topshiriq: Oqim identifikatori va sleep_for

## Topshiriq sharti:
`get_id()` orqali oqim ID sini ko'ring va `sleep_for` orqali 50ms kechiktiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <thread>
#include <chrono>

void salom() {
    std::cout << "Oqim ID: " << std::this_thread::get_id() << std::endl;
    std::this_thread::sleep_for(std::chrono::milliseconds(50));
}

int main() {
    std::thread t(salom);
    t.join();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::this_thread::get_id()` oqimning noyob tizim raqamini beradi.

## Ishlash natijasi:
```text
Oqim ID: ...
```

---

# 754-Topshiriq: Hardware Concurrency (CPU yadrolari soni)

## Topshiriq sharti:
`std::thread::hardware_concurrency()` orqali kompyuterdagi mantiqiy CPU yadrolari sonini aniqlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <thread>

int main() {
    unsigned int cores = std::thread::hardware_concurrency();
    std::cout << "Mavjud mantiqiy CPU yadrolari: " << cores << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bu parametr parallel algoritmlarda nechta oqim ochish kerakligini belgilashda asos hisoblanadi.

## Ishlash natijasi:
```text
Mavjud mantiqiy CPU yadrolari: ...
```

---

# 755-Topshiriq: Poyga holati (Data Race) va std::mutex

## Topshiriq sharti:
Bir vaqtda bitta umumiy o'zgaruvchini o'zgartirishdagi poyga holatini `std::mutex` bilan himoyalang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <thread>
#include <mutex>

int hisoblagich = 0;
std::mutex mtx;

void oshir() {
    for (int i = 0; i < 1000; ++i) {
        mtx.lock();
        hisoblagich++;
        mtx.unlock();
    }
}

int main() {
    std::thread t1(oshir);
    std::thread t2(oshir);
    t1.join();
    t2.join();
    std::cout << "Jami hisoblagich: " << hisoblagich << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Mutex (Mutual Exclusion) faqat bitta oqimga kritik bo'limga (Critical section) kirishga ruxsat beradi.

## Ishlash natijasi:
```text
Jami hisoblagich: 2000
```

---

# 756-Topshiriq: RAII Mutex boshqaruvi: std::lock_guard

## Topshiriq sharti:
Qo'lda unlock qilishni unutish va istisnolarda qotib qolishning oldini oluvchi `std::lock_guard` ni qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <thread>
#include <mutex>

int umumiySumma = 0;
std::mutex mtx;

void qosh(int x) {
    std::lock_guard<std::mutex> qulf(mtx);
    umumiySumma += x;
}

int main() {
    std::thread t1(qosh, 100);
    std::thread t2(qosh, 200);
    t1.join();
    t2.join();
    std::cout << "Summa: " << umumiySumma << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::lock_guard` RAII tamoyili asosida ishlaydi va istisno tashlansa ham mutexni avtomatik ochadi.

## Ishlash natijasi:
```text
Summa: 300
```

---

# 757-Topshiriq: std::unique_lock va moslashuvchanlik

## Topshiriq sharti:
Kechiktirib qulflash (`std::defer_lock`) va shartli o'zgaruvchilar bilan ishlovchi `std::unique_lock` ni ishlating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <thread>
#include <mutex>

std::mutex m;

void vazifa() {
    std::unique_lock<std::mutex> lock(m, std::defer_lock);
    lock.lock();
    std::cout << "Qulflangan qism\n";
    lock.unlock();
}

int main() {
    std::thread t(vazifa);
    t.join();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::unique_lock` `lock_guard` ga qaraganda ancha ko'p funksiyalarga ega va ko'chirilishi mumkin.

## Ishlash natijasi:
```text
Qulflangan qism
```

---

# 758-Topshiriq: Deadlock va C++17 std::scoped_lock

## Topshiriq sharti:
Ikki yoki undan ortiq mutexni bir vaqtda qulflashda `std::scoped_lock` orqali deadlock ning oldini oling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <thread>
#include <mutex>

std::mutex mtx1, mtx2;

void amal() {
    std::scoped_lock qulf(mtx1, mtx2);
    std::cout << "Ikkala resurs xavfsiz qulflandi\n";
}

int main() {
    std::thread t(amal);
    t.join();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::scoped_lock` deadlock xavfisiz barcha ko'rsatilgan mutexlarni atomik qulflaydi.

## Ishlash natijasi:
```text
Ikkala resurs xavfsiz qulflandi
```

---

# 759-Topshiriq: Atomik operatsiyalar: std::atomic<int>

## Topshiriq sharti:
Mutexlarsiz eng yuqori apparat tezligida hisoblagichni `std::atomic` bilan boshqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <thread>
#include <atomic>

std::atomic<int> atomikSon = 0;

void sanash() {
    for (int i = 0; i < 5000; ++i) {
        atomikSon++;
    }
}

int main() {
    std::thread t1(sanash);
    std::thread t2(sanash);
    t1.join();
    t2.join();
    std::cout << "Atomik natija: " << atomikSon.load() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::atomic` operatsiyalari operatsion tizim kontekst almashtirishlarisiz to'g'ridan-to'g'ri CPU instruksiyalari bilan bajariladi.

## Ishlash natijasi:
```text
Atomik natija: 10000
```

---

# 760-Topshiriq: Compare-And-Swap (CAS): compare_exchange_strong

## Topshiriq sharti:
Lock-free algoritmlarning asosi bo'lgan CAS operatsiyasini namoyish eting.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <atomic>

int main() {
    std::atomic<int> qiymat = 100;
    int kutilgan = 100;
    int yangi = 200;
    bool muvaffaqiyat = qiymat.compare_exchange_strong(kutilgan, yangi);
    std::cout << "Almashtirildimi: " << (muvaffaqiyat ? "Ha" : "Yo'q") 
              << ", Yangi qiymat: " << qiymat.load() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. CAS: agar joriy qiymat `kutilgan` ga teng bo'lsa, uni `yangi` qiymatga atomik almashtiradi.

## Ishlash natijasi:
```text
Almashtirildimi: Ha, Yangi qiymat: 200
```

---

# 761-Topshiriq: Shartli o'zgaruvchilar: std::condition_variable

## Topshiriq sharti:
Bir oqim boshqa oqimning xabarini kutib uxlashi va uyg'onishini amalga oshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>

std::mutex m;
std::condition_variable cv;
bool tayyor = false;

void ishchi() {
    std::unique_lock<std::mutex> lock(m);
    cv.wait(lock, [] { return tayyor; });
    std::cout << "Ishchi uyg'ondi va vazifani boshladi!\n";
}

int main() {
    std::thread t(ishchi);
    {
        std::lock_guard<std::mutex> lock(m);
        tayyor = true;
    }
    cv.notify_one();
    t.join();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `cv.wait()` mutexni ochib oqimni uxlatadi va signal kelganda uyg'onib mutexni qayta qulflaydi.

## Ishlash natijasi:
```text
Ishchi uyg'ondi va vazifani boshladi!
```

---

# 762-Topshiriq: Ishlab chiqaruvchi - Iste'molchi (Producer-Consumer)

## Topshiriq sharti:
Navbat orqali ma'lumot uzatuvchi va qabul qiluvchi klassik tizimni quring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <thread>
#include <queue>
#include <mutex>
#include <condition_variable>

std::queue<int> navbat;
std::mutex mtx;
std::condition_variable cv;
bool tugadi = false;

void producer() {
    for (int i = 1; i <= 3; ++i) {
        {
            std::lock_guard<std::mutex> lock(mtx);
            navbat.push(i);
        }
        cv.notify_one();
    }
    {
        std::lock_guard<std::mutex> lock(mtx);
        tugadi = true;
    }
    cv.notify_all();
}

void consumer() {
    while (true) {
        std::unique_lock<std::mutex> lock(mtx);
        cv.wait(lock, [] { return !navbat.empty() || tugadi; });
        while (!navbat.empty()) {
            std::cout << "Qabul qilindi: " << navbat.front() << "\n";
            navbat.pop();
        }
        if (tugadi) break;
    }
}

int main() {
    std::thread c(consumer);
    std::thread p(producer);
    p.join();
    c.join();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Tarmoqli serverlar va AI ma'lumotlar oqimining asosiy dizayn andozasi.

## Ishlash natijasi:
```text
Qabul qilindi: 1\nQabul qilindi: 2\nQabul qilindi: 3
```

---

# 763-Topshiriq: Asinxron hisoblashlar: std::async va std::future

## Topshiriq sharti:
`std::async` orqali fonda og'ir hisob-kitobni bajarib, natijasini kelajakda oling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <future>

int kvadrat(int x) {
    return x * x;
}

int main() {
    std::future<int> natija = std::async(std::launch::async, kvadrat, 9);
    std::cout << "Asosiy oqim boshqa ishlar bilan band...\n";
    int javob = natija.get();
    std::cout << "Javob: " << javob << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::async` oqim yaratish, qiymat qaytarish va istisnolarni boshqarishni to'liq avtomatlashtiradi.

## Ishlash natijasi:
```text
Asosiy oqim boshqa ishlar bilan band...\nJavob: 81
```

---

# 764-Topshiriq: std::promise va std::future orqali qiymat uzatish

## Topshiriq sharti:
Oqim ichida `promise.set_value()` orqali natijani yuklang va tashqarida oling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <thread>
#include <future>

void hisobla(std::promise<std::string> prom) {
    prom.set_value("1-Bit AI Kvantlash yakunlandi");
}

int main() {
    std::promise<std::string> p;
    std::future<std::string> f = p.get_future();
    std::thread t(hisobla, std::move(p));
    std::cout << "Status: " << f.get() << std::endl;
    t.join();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::promise` bir tomonlama qiymat uzatuvchi quvur bo'lib, `std::future` orqali qabul qilinadi.

## Ishlash natijasi:
```text
Status: 1-Bit AI Kvantlash yakunlandi
```

---

# 765-Topshiriq: future::wait_for va taymaut

## Topshiriq sharti:
Vazifa belgilangan vaqt ichida bajarilmasa taymaut xabarini bering.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <future>
#include <chrono>

int sekinFunksiya() {
    std::this_thread::sleep_for(std::chrono::milliseconds(200));
    return 42;
}

int main() {
    auto f = std::async(std::launch::async, sekinFunksiya);
    if (f.wait_for(std::chrono::milliseconds(50)) == std::future_status::timeout) {
        std::cout << "Kutish vaqti tugadi (Timeout)!" << std::endl;
    }
    f.wait();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `wait_for` tarmoq so'rovlari va uzoq hisob-kitoblarda tizim qotib qolmasligini ta'minlaydi.

## Ishlash natijasi:
```text
Kutish vaqti tugadi (Timeout)!
```

---

# 766-Topshiriq: std::packaged_task asoslari

## Topshiriq sharti:
Chaqiriluvchi funksiyani asinxron paketga o'rab `std::future` bog'lang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <future>
#include <thread>

int qosh(int a, int b) { return a + b; }

int main() {
    std::packaged_task<int(int, int)> task(qosh);
    std::future<int> res = task.get_future();
    std::thread t(std::move(task), 15, 25);
    std::cout << "Natija: " << res.get() << std::endl;
    t.join();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::packaged_task` vazifalar navbati (Task Queue) va Thread Pool qurishning asosiy poydevoridir.

## Ishlash natijasi:
```text
Natija: 40
```

---

# 767-Topshiriq: C++20 std::jthread (Avtomatik join qiluvchi oqim)

## Topshiriq sharti:
Destruktorda avtomatik `.join()` chaqiruvchi va `std::terminate` bermaydigan `std::jthread` ni qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <thread>

void vazifa() {
    std::cout << "jthread muvaffaqiyatli ishladi.\n";
}

int main() {
    {
        std::jthread jt(vazifa);
    }
    std::cout << "jthread xavfsiz tugatildi.\n";
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::jthread` C++20 da oddiy `std::thread` ning xatolarini tuzatgan xavfsiz o'rinbosaridir.

## Ishlash natijasi:
```text
jthread muvaffaqiyatli ishladi.\njthread xavfsiz tugatildi.
```

---

# 768-Topshiriq: C++20 std::stop_token orqali oqimni xavfsiz to'xtatish

## Topshiriq sharti:
Oqim ichida to'xtash so'rovini tekshirib toza chiqishni ta'minlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <thread>
#include <chrono>

void ishchi(std::stop_token st) {
    while (!st.stop_requested()) {
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
    }
    std::cout << "To'xtash so'rovi qabul qilindi va chiqildi.\n";
}

int main() {
    std::jthread jt(ishchi);
    std::this_thread::sleep_for(std::chrono::milliseconds(30));
    jt.request_stop();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::stop_token` C++20 da kooperativ to'xtatishning standart yo'lidir.

## Ishlash natijasi:
```text
To'xtash so'rovi qabul qilindi va chiqildi.
```

---

# 769-Topshiriq: O'qish/Yozish qulfi: std::shared_mutex (C++17)

## Topshiriq sharti:
Bir nechta oqim bir vaqtda o'qishi, ammo faqat bitta oqim yozishi mumkin bo'lgan Reader-Writer lock ni qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <thread>
#include <shared_mutex>

std::shared_mutex rwMtx;
int qiymat = 42;

void oquvchi() {
    std::shared_lock lock(rwMtx);
    std::cout << "O'qildi: " << qiymat << "\n";
}

void yozuvchi(int yangi) {
    std::unique_lock lock(rwMtx);
    qiymat = yangi;
}

int main() {
    std::thread t1(oquvchi);
    std::thread t2(yozuvchi, 99);
    std::thread t3(oquvchi);
    t1.join();
    t2.join();
    t3.join();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Keshlar va ma'lumotlar bazalarida o'qish amallari ko'p bo'lganda `shared_mutex` unumdorlikni bir necha barobar oshiradi.

## Ishlash natijasi:
```text
O'qildi: ...\nO'qildi: ...
```

---

# 770-Topshiriq: std::call_once va std::once_flag

## Topshiriq sharti:
Ko'p oqimli muhitda funksiya faqat va faqat bir marta chaqirilishini kafolatlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <thread>
#include <mutex>

std::once_flag flag;

void initsializatsiya() {
    std::cout << "Tizim bir marta ishga tushirildi!\n";
}

void ish() {
    std::call_once(flag, initsializatsiya);
}

int main() {
    std::thread t1(ish);
    std::thread t2(ish);
    t1.join();
    t2.join();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::call_once` xavfsiz bir martalik resurs ochish (Lazy Initialization) uchun xizmat qiladi.

## Ishlash natijasi:
```text
Tizim bir marta ishga tushirildi!
```

---

# 771-Topshiriq: thread_local saqlash muddati

## Topshiriq sharti:
Har bir oqim o'zining alohida o'zgaruvchi nusxasiga ega bo'lishini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <thread>

thread_local int oqimSanagich = 0;

void hisobla() {
    oqimSanagich++;
    std::cout << "Oqim: " << oqimSanagich << "\n";
}

int main() {
    std::thread t1(hisobla);
    std::thread t2(hisobla);
    t1.join();
    t2.join();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `thread_local` o'zgaruvchilar oqimlar o'rtasida bo'lishilmaydi.

## Ishlash natijasi:
```text
Oqim: 1\nOqim: 1
```

---

# 772-Topshiriq: C++20 std::latch (Marraga yetish sinxronizatsiyasi)

## Topshiriq sharti:
Barcha oqimlar tayyor bo'lmaguncha asosiy dastur kutib turishini `std::latch` bilan ta'minlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <thread>
#include <latch>

std::latch marra(2);

void vazifa(int id) {
    std::cout << "Oqim " << id << " tayyor\n";
    marra.count_down();
}

int main() {
    std::thread t1(vazifa, 1);
    std::thread t2(vazifa, 2);
    marra.wait();
    std::cout << "Barcha oqimlar tayyor! Dastur boshlandi.\n";
    t1.join(); t2.join();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::latch` bir martalik to'siq bo'lib, oqimlarning sinxron yetib kelishini kutadi.

## Ishlash natijasi:
```text
Oqim ... tayyor\nOqim ... tayyor\nBarcha oqimlar tayyor! Dastur boshlandi.
```

---

# 773-Topshiriq: C++20 std::counting_semaphore

## Topshiriq sharti:
Bir vaqtda resursdan faqat 2 ta oqim foydalanishiga ruxsat beruvchi semaforni qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <thread>
#include <semaphore>
#include <chrono>

std::counting_semaphore<2> sem(2);

void xizmat(int id) {
    sem.acquire();
    std::cout << "Oqim " << id << " resursdan foydalanmoqda\n";
    std::this_thread::sleep_for(std::chrono::milliseconds(20));
    sem.release();
}

int main() {
    std::thread t1(xizmat, 1);
    std::thread t2(xizmat, 2);
    t1.join(); t2.join();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Semaforlar bir vaqtda cheklangan miqdordagi ulanishlarni nazorat qiladi.

## Ishlash natijasi:
```text
Oqim ... resursdan foydalanmoqda\nOqim ... resursdan foydalanmoqda
```

---

# 774-Topshiriq: Oddiy Thread Pool (Oqimlar havzasi) skeleti

## Topshiriq sharti:
Doimiy ishchi oqimlar navbatdagi vazifalarni olib bajaruvchi pool tuzilmasini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <queue>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <functional>

class MiniThreadPool {
    std::vector<std::thread> workers;
    std::queue<std::function<void()>> tasks;
    std::mutex queue_mutex;
    std::condition_variable cv;
    bool stop = false;
public:
    MiniThreadPool(size_t threads) {
        for (size_t i = 0; i < threads; ++i) {
            workers.emplace_back([this] {
                while (true) {
                    std::function<void()> task;
                    {
                        std::unique_lock<std::mutex> lock(this->queue_mutex);
                        this->cv.wait(lock, [this] { return this->stop || !this->tasks.empty(); });
                        if (this->stop && this->tasks.empty()) return;
                        task = std::move(this->tasks.front());
                        this->tasks.pop();
                    }
                    task();
                }
            });
        }
    }
    void enqueue(std::function<void()> f) {
        {
            std::lock_guard<std::mutex> lock(queue_mutex);
            tasks.push(f);
        }
        cv.notify_one();
    }
    ~MiniThreadPool() {
        {
            std::lock_guard<std::mutex> lock(queue_mutex);
            stop = true;
        }
        cv.notify_all();
        for (std::thread& worker : workers) worker.join();
    }
};

int main() {
    {
        MiniThreadPool pool(2);
        pool.enqueue([] { std::cout << "Vazifa 1 bajarildi\n"; });
        pool.enqueue([] { std::cout << "Vazifa 2 bajarildi\n"; });
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Thread Pool oqimlarni qayta-qayta yaratish xarajatlarini yo'qotadi.

## Ishlash natijasi:
```text
Vazifa ... bajarildi\nVazifa ... bajarildi
```

---

# 775-Topshiriq: Parallel massiv yig'indisi (Multithreaded Sum)

## Topshiriq sharti:
Katta massivni ikki bo'lakka ajratib ikkita oqimda parallel hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <future>
#include <numeric>

long long oraliqSum(const std::vector<int>& v, size_t bosh, size_t oxir) {
    return std::accumulate(v.begin() + bosh, v.begin() + oxir, 0LL);
}

int main() {
    std::vector<int> v(1000000, 1);
    size_t yarmi = v.size() / 2;
    auto f1 = std::async(std::launch::async, oraliqSum, std::cref(v), 0, yarmi);
    auto f2 = std::async(std::launch::async, oraliqSum, std::cref(v), yarmi, v.size());
    long long jami = f1.get() + f2.get();
    std::cout << "Parallel yig'indi: " << jami << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Massiv qismlarga bo'linib turli yadrolarda parallel qayta ishlanadi.

## Ishlash natijasi:
```text
Parallel yig'indi: 1000000
```

---

# 776-Topshiriq: False Sharing muammosi va alignas(64)

## Topshiriq sharti:
Ikki oqim bir kesh liniyasidagi qo'shni o'zgaruvchilarni o'zgartirganda kesh to'qnashuvining oldini oling.

## Yechim (C++ kodi):
```cpp
#include <iostream>

struct alignas(64) HimoyalanganYadro {
    int hisob = 0;
};

int main() {
    std::cout << "alignas(64) o'zgaruvchini alohida kesh liniyasiga joylashtirib False Sharing ning oldini oladi." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. False Sharing ko'p yadroli tizimlarda tezlikni tushirishi mumkin.

## Ishlash natijasi:
```text
alignas(64) o'zgaruvchini alohida kesh liniyasiga joylashtirib False Sharing ning oldini oladi.
```

---

# 777-Topshiriq: Oddiy Spinlock: std::atomic_flag

## Topshiriq sharti:
Oqimni uxlatmasdan CPU siklida kutuvchi eng tezkor Spinlock qulfini tuzing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <atomic>
#include <thread>

class Spinlock {
    std::atomic_flag flag = ATOMIC_FLAG_INIT;
public:
    void lock() {
        while (flag.test_and_set(std::memory_order_acquire)) {}
    }
    void unlock() {
        flag.clear(std::memory_order_release);
    }
};

Spinlock sl;

void xavfsizChiqar() {
    sl.lock();
    std::cout << "Spinlock orqali o'tdi\n";
    sl.unlock();
}

int main() {
    std::thread t1(xavfsizChiqar);
    std::thread t2(xavfsizChiqar);
    t1.join(); t2.join();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Spinlock qisqa muddatli qulflashlar uchun mutex dan ham tezroq ishlaydi.

## Ishlash natijasi:
```text
Spinlock orqali o'tdi\nSpinlock orqali o'tdi
```

---

# 778-Topshiriq: C++20 atomic::wait va atomic::notify

## Topshiriq sharti:
C++20 da atomik o'zgaruvchi qiymat o'zgarishini mutex va cv siz to'g'ridan-to'g'ri kutish.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <atomic>
#include <thread>

std::atomic<int> signal = 0;

void kutuvchi() {
    signal.wait(0);
    std::cout << "Signal qabul qilindi: " << signal.load() << std::endl;
}

int main() {
    std::thread t(kutuvchi);
    std::this_thread::sleep_for(std::chrono::milliseconds(20));
    signal.store(1);
    signal.notify_one();
    t.join();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. OS ning futex mexanizmidan foydalanadi va minimal sarf-xarajat talab qiladi.

## Ishlash natijasi:
```text
Signal qabul qilindi: 1
```

---

# 779-Topshiriq: Parallel Neyron Tarmoq Qatlami (Parallel Dense Layer)

## Topshiriq sharti:
Neyronlar chiqishini oqimlar bo'ylab taqsimlab hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <thread>

void neyronHisobla(int id, float kirish, float vazn, float& chiqish) {
    chiqish = kirish * vazn;
}

int main() {
    float x = 0.8f;
    std::vector<float> vaznlar = {0.5f, -0.2f, 1.2f};
    std::vector<float> chiqishlar(3);
    std::vector<std::thread> oqimlar;

    for (int i = 0; i < 3; ++i) {
        oqimlar.emplace_back(neyronHisobla, i, x, vaznlar[i], std::ref(chiqishlar[i]));
    }
    for (auto& t : oqimlar) t.join();

    std::cout << "Neyronlar natijasi: ";
    for (float val : chiqishlar) std::cout << val << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Neyron tarmoqlarning parallel matritsa hisoblash mexanikasi.

## Ishlash natijasi:
```text
Neyronlar natijasi: 0.4 -0.16 0.96 
```

---

# 780-Topshiriq: C++20 std::barrier orqali tsiklli to'siq sinxronizatsiyasi

## Topshiriq sharti:
Har bir iteratsiyada barcha oqimlar kelishini kutuvchi qayta ishlatiluvchi to'siqni qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <thread>
#include <barrier>
#include <vector>

std::barrier tosiq(2);

void bosqichliIsh(int id) {
    for (int qadam = 1; qadam <= 2; ++qadam) {
        std::cout << "Oqim " << id << " qadam " << qadam << " boshladi\n";
        tosiq.arrive_and_wait();
    }
}

int main() {
    std::thread t1(bosqichliIsh, 1);
    std::thread t2(bosqichliIsh, 2);
    t1.join(); t2.join();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::barrier` `latch` dan farqli o'laroq bir necha sikl qayta ishlatiladi.

## Ishlash natijasi:
```text
Oqim ... qadam ... boshladi\nOqim ... qadam ... boshladi
```

---

# 781-Topshiriq: std::shared_future bilan bir natijani bir nechta oqimda kutish

## Topshiriq sharti:
Bitta asinxron natijani bir nechta mustaqil oqimlarga tarqatish.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <future>
#include <thread>

void iste'molchi(std::shared_future<int> sf, int id) {
    std::cout << "Oqim " << id << " qabul qildi: " << sf.get() << std::endl;
}

int main() {
    std::promise<int> p;
    std::shared_future<int> sf = p.get_future().share();
    std::thread t1(iste'molchi, sf, 1);
    std::thread t2(iste'molchi, sf, 2);
    p.set_value(555);
    t1.join(); t2.join();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::shared_future` bir nechta `.get()` chaqiruvlariga ruxsat beradi.

## Ishlash natijasi:
```text
Oqim ... qabul qildi: 555\nOqim ... qabul qildi: 555
```

---

# 782-Topshiriq: promise::set_exception orqali oqimlararo istisno uzatish

## Topshiriq sharti:
Yordamchi oqimda yuz bergan istisnoni asosiy oqimda `get()` orqali ushlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <thread>
#include <future>
#include <stdexcept>

void xatoliOqim(std::promise<void> p) {
    try {
        throw std::runtime_error("Oqim ichida avariya!");
    } catch (...) {
        p.set_exception(std::current_exception());
    }
}

int main() {
    std::promise<void> p;
    auto f = p.get_future();
    std::thread t(xatoliOqim, std::move(p));
    try {
        f.get();
    } catch (const std::exception& e) {
        std::cout << "Asosiy oqim xatoni ushladi: " << e.what() << std::endl;
    }
    t.join();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `promise.set_exception()` oqimlar o'rtasida istisnolarni xavfsiz transport qiladi.

## Ishlash natijasi:
```text
Asosiy oqim xatoni ushladi: Oqim ichida avariya!
```

---

# 783-Topshiriq: Oqimlar xavfsiz hisoblagich (Thread-Safe Counter sinfi)

## Topshiriq sharti:
Enkapsulyatsiyalangan va mutex bilan to'liq himoyalangan hisoblagich klassi.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <thread>
#include <mutex>

class XavfsizHisoblagich {
    mutable std::mutex m;
    int qiymat = 0;
public:
    void oshir() {
        std::lock_guard<std::mutex> lock(m);
        qiymat++;
    }
    int get() const {
        std::lock_guard<std::mutex> lock(m);
        return qiymat;
    }
};

int main() {
    XavfsizHisoblagich c;
    std::thread t1([&] { for (int i = 0; i < 500; ++i) c.oshir(); });
    std::thread t2([&] { for (int i = 0; i < 500; ++i) c.oshir(); });
    t1.join(); t2.join();
    std::cout << "Yakuniy hisob: " << c.get() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Klass ichiga mutexni yashirish va const metodlarda mutable mutex ishlatish.

## Ishlash natijasi:
```text
Yakuniy hisob: 1000
```

---

# 784-Topshiriq: Parallel Matritsa Ko'paytirish (GEMM multithreading)

## Topshiriq sharti:
Matritsaning har bir satrini alohida oqimga yuklab hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <thread>

int main() {
    int A[2][2] = {{1, 2}, {3, 4}};
    int B[2][2] = {{5, 6}, {7, 8}};
    int C[2][2] = {0};

    auto rowWorker = [&](int r) {
        for (int c = 0; c < 2; ++c) {
            for (int k = 0; k < 2; ++k) C[r][c] += A[r][k] * B[k][c];
        }
    };

    std::thread t0(rowWorker, 0);
    std::thread t1(rowWorker, 1);
    t0.join(); t1.join();

    std::cout << "C[0][0]=" << C[0][0] << ", C[1][1]=" << C[1][1] << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Satrlar bir-biriga bog'liq bo'lmagani sababli qulflashlarsiz parallel hisoblanadi.

## Ishlash natijasi:
```text
C[0][0]=19, C[1][1]=50
```

---

# 785-Topshiriq: Parallel qidiruv algoritmi

## Topshiriq sharti:
Katta massivni 2 oqimda qidirib topilgan birinchi indeksni xabar qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <atomic>
#include <thread>

int main() {
    std::vector<int> v = {10, 20, 30, 42, 50, 60};
    int qidirilayotgan = 42;
    std::atomic<int> topilganIndeks = -1;

    auto qidir = [&](size_t bosh, size_t oxir) {
        for (size_t i = bosh; i < oxir; ++i) {
            if (topilganIndeks != -1) return;
            if (v[i] == qidirilayotgan) {
                topilganIndeks = i;
                return;
            }
        }
    };

    std::thread t1(qidir, 0, 3);
    std::thread t2(qidir, 3, 6);
    t1.join(); t2.join();
    std::cout << "Indeks: " << topilganIndeks.load() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `topilganIndeks` atomik bayrog'i boshqa oqim topganda qidiruvni erta to'xtatadi.

## Ishlash natijasi:
```text
Indeks: 3
```

---

# 786-Topshiriq: Parallel MergeSort (Rekursiv multithreading)

## Topshiriq sharti:
Massivning ikkala yarmini alohida `std::async` bilan saralang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <future>

void parallelSort(std::vector<int>& v, size_t chap, size_t ong) {
    if (ong - chap <= 1) return;
    size_t orta = chap + (ong - chap) / 2;
    if (ong - chap > 1000) {
        auto f = std::async(std::launch::async, parallelSort, std::ref(v), chap, orta);
        parallelSort(v, orta, ong);
        f.wait();
    } else {
        std::sort(v.begin() + chap, v.begin() + ong);
        return;
    }
    std::inplace_merge(v.begin() + chap, v.begin() + orta, v.begin() + ong);
}

int main() {
    std::vector<int> v = {8, 3, 2, 9, 7, 1, 5, 4};
    std::sort(v.begin(), v.end());
    for (int x : v) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bo'lib tashla va hukmronlik qil (Divide and conquer) parallel hisoblash uchun ideal.

## Ishlash natijasi:
```text
1 2 3 4 5 7 8 9 
```

---

# 787-Topshiriq: Bounded Blocking Queue (Chegaralangan bloklanuvchi navbat)

## Topshiriq sharti:
Maksimal sig'imi to'lganda ishlab chiqaruvchini to'xtatib turuvchi xavfsiz navbat.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <queue>
#include <mutex>
#include <condition_variable>

class BoundedQueue {
    std::queue<int> q;
    size_t sigim;
    std::mutex m;
    std::condition_variable not_full, not_empty;
public:
    BoundedQueue(size_t s) : sigim(s) {}
    void push(int val) {
        std::unique_lock<std::mutex> lock(m);
        not_full.wait(lock, [this] { return q.size() < sigim; });
        q.push(val);
        not_empty.notify_one();
    }
    int pop() {
        std::unique_lock<std::mutex> lock(m);
        not_empty.wait(lock, [this] { return !q.empty(); });
        int val = q.front(); q.pop();
        not_full.notify_one();
        return val;
    }
};

int main() {
    BoundedQueue bq(2);
    bq.push(10);
    bq.push(20);
    std::cout << "Olingan: " << bq.pop() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ikkita condition variable orqali ham bo'shliq, ham to'lalik nazorat qilinadi.

## Ishlash natijasi:
```text
Olingan: 10
```

---

# 788-Topshiriq: Asinxron yuklagich simulyatsiyasi (Async Downloader)

## Topshiriq sharti:
Bir vaqtda 3 ta faylni yuklash simulyatsiyasini `std::async` bilan yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <future>
#include <vector>
#include <string>

std::string yukla(std::string fayl) {
    return fayl + " muvaffaqiyatli yuklandi";
}

int main() {
    std::vector<std::string> fayllar = {"model.bin", "vocab.txt", "config.json"};
    std::vector<std::future<std::string>> vazifalar;
    for (const auto& f : fayllar) {
        vazifalar.push_back(std::async(std::launch::async, yukla, f));
    }
    for (auto& v : vazifalar) {
        std::cout << v.get() << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Parallel tarmoq so'rovlarini asinxron boshqarish.

## Ishlash natijasi:
```text
model.bin muvaffaqiyatli yuklandi\nvocab.txt muvaffaqiyatli yuklandi\nconfig.json muvaffaqiyatli yuklandi
```

---

# 789-Topshiriq: 1-Bit LLM Kvantlangan Tenzor Ko'paytmasini Ko'p Oqimda Hisoblash

## Topshiriq sharti:
{-1, 0, 1} og'irliklar matritsasi va aktivatsiya vektorini ko'p oqimli hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <thread>
#include <cstdint>

// 1-Bit BitNet uslubidagi ternary GEMV
void bitnetRow(int r, const std::vector<int8_t>& W, const std::vector<float>& X, std::vector<float>& Y, int K) {
    float sum = 0.0f;
    for (int k = 0; k < K; ++k) {
        int8_t w = W[r * K + k];
        if (w == 1) sum += X[k];
        else if (w == -1) sum -= X[k];
        // w == 0 bo'lsa hech narsa qo'shilmaydi (nol ko'paytirish)
    }
    Y[r] = sum;
}

int main() {
    int N = 2, K = 4;
    std::vector<int8_t> W = {1, -1, 0, 1,   0, 1, 1, -1};
    std::vector<float> X = {1.5f, 2.0f, 3.0f, 0.5f};
    std::vector<float> Y(N, 0.0f);

    std::thread t0(bitnetRow, 0, std::cref(W), std::cref(X), std::ref(Y), K);
    std::thread t1(bitnetRow, 1, std::cref(W), std::cref(X), std::ref(Y), K);
    t0.join(); t1.join();

    std::cout << "Y[0] = " << Y[0] << ", Y[1] = " << Y[1] << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 1-Bit AI modellari ko'paytirishsiz (faqat qo'shish va ayirish bilan) parallel oqimlarda o'ta tez ishlaydi.

## Ishlash natijasi:
```text
Y[0] = 0, Y[1] = 4.5
```

---

# 790-Topshiriq: Memory Ordering: Relaxed vs Seq_cst

## Topshiriq sharti:
Eng bo'shashgan (relaxed) va eng qat'iy (sequentially consistent) xotira tartibi farqini tushuntiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <atomic>

int main() {
    std::atomic<int> a = 0;
    a.store(1, std::memory_order_relaxed); // Qo'shimcha xotira to'siqlari (memory fence) yo'q
    int val = a.load(std::memory_order_seq_cst); // Qat'iy global tartib
    std::cout << "Yuklangan qiymat: " << val << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `relaxed` tartib faqat atomiklikni kafolatlaydi, boshqa instruksiyalarni CPU qayta tartiblashi (reordering) mumkin.

## Ishlash natijasi:
```text
Yuklangan qiymat: 1
```

---

# 791-Topshiriq: Acquire-Release Semantikasi

## Topshiriq sharti:
Oqimlar o'rtasida ma'lumotlarni o'tkazishda `memory_order_release` va `acquire` juftligini qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <atomic>
#include <thread>

std::atomic<bool> tayyor = false;
int malumot = 0;

void producer() {
    malumot = 42;
    tayyor.store(true, std::memory_order_release); // malumot yozilishi bu yerdan o'tib ketmaydi
}

void consumer() {
    while (!tayyor.load(std::memory_order_acquire)) {} // tayyor bo'lgach malumot kafolatlangan
    std::cout << "Kafolatlangan ma'lumot: " << malumot << std::endl;
}

int main() {
    std::thread t2(consumer);
    std::thread t1(producer);
    t1.join(); t2.join();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Acquire-Release sinxronizatsiyasi to'liq mutex qulflari kabi ishlaydi, ammo apparat darajasida.

## Ishlash natijasi:
```text
Kafolatlangan ma'lumot: 42
```

---

# 792-Topshiriq: ABA muammosi tushunchasi (ABA Problem)

## Topshiriq sharti:
Lock-free ma'lumotlar tuzilmalarida qiymat A dan B ga, so'ng yana A ga qaytib kelganda ko'rsatkichlar xatosi kelib chiqishini tushuntiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "ABA Problem - qiymat A -> B -> A bo'lganda CAS ko'rsatkich o'zgarmadi deb xato o'ylaydi. "
              << "Yechim: Tagged pointerlar yoki std::atomic<std::shared_ptr>." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Lock-free tuzilmalarda versiya raqami yoki xotira xavfsizligi tizimlari (Hazard Pointers, RCU) talab qilinadi.

## Ishlash natijasi:
```text
ABA Problem - qiymat A -> B -> A bo'lganda CAS ko'rsatkich o'zgarmadi deb xato o'ylaydi. Yechim: Tagged pointerlar yoki std::atomic<std::shared_ptr>.
```

---

# 793-Topshiriq: Oqimlar xavfsiz Stack (Thread-Safe Stack)

## Topshiriq sharti:
Mutex bilan himoyalangan va `pop()` paytida qiymatni xavfsiz qaytaruvchi sinf.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <stack>
#include <mutex>
#include <memory>

class XavfsizStack {
    std::stack<int> s;
    std::mutex m;
public:
    void push(int x) {
        std::lock_guard<std::mutex> lock(m);
        s.push(x);
    }
    bool try_pop(int& value) {
        std::lock_guard<std::mutex> lock(m);
        if (s.empty()) return false;
        value = s.top();
        s.pop();
        return true;
    }
};

int main() {
    XavfsizStack st;
    st.push(777);
    int olingan;
    if (st.try_pop(olingan)) {
        std::cout << "Stackdan olindi: " << olingan << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `try_pop` bo'sh stekdan o'qishda crash bo'lishining oldini oladi.

## Ishlash natijasi:
```text
Stackdan olindi: 777
```

---

# 794-Topshiriq: Parallel Fibonachchi hisoblash (Asinxron)

## Topshiriq sharti:
`std::async` orqali katta Fibonachchi sonini parallel tarmoqlarda hisoblash.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <future>

int fibAsync(int n) {
    if (n <= 1) return n;
    if (n < 20) return fibAsync(n - 1) + fibAsync(n - 2);
    auto f1 = std::async(std::launch::async, fibAsync, n - 1);
    int f2 = fibAsync(n - 2);
    return f1.get() + f2;
}

int main() {
    std::cout << "fibAsync(10) = " << fibAsync(10) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kichik n larda oddiy rekursiya, katta n larda esa alohida oqimlar ishlatiladi.

## Ishlash natijasi:
```text
fibAsync(10) = 55
```

---

# 795-Topshiriq: CPU Affinity (Oqimni aniq yadroga bog'lash tushunchasi)

## Topshiriq sharti:
Oqimni belgilangan fizik CPU yadrosiga biriktirib kesh samaradorligini oshirish.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "CPU Affinity (Thread pinning) - oqimni ma'lum bir protsessor yadrosiga "
              << "qat'iy bog'lash orqali kesh sakrashlarini bartaraf etish." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Platformaga xos chaqiruvlar (`SetThreadAffinityMask` yoki `pthread_setaffinity_np`) orqali amalga oshiriladi.

## Ishlash natijasi:
```text
CPU Affinity (Thread pinning) - oqimni ma'lum bir protsessor yadrosiga qat'iy bog'lash orqali kesh sakrashlarini bartaraf etish.
```

---

# 796-Topshiriq: Oqimlararo global xabar tizimi (Event Bus asoslari)

## Topshiriq sharti:
Oqimlar o'rtasida xabarlarni tarqatuvchi markaziy sinf skeleti.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <functional>
#include <mutex>

class EventBus {
    std::vector<std::function<void(int)>> tinglovchilar;
    std::mutex m;
public:
    void obuna(std::function<void(int)> fn) {
        std::lock_guard<std::mutex> lock(m);
        tinglovchilar.push_back(fn);
    }
    void tarqat(int xabar) {
        std::lock_guard<std::mutex> lock(m);
        for (auto& t : tinglovchilar) t(xabar);
    }
};

int main() {
    EventBus bus;
    bus.obuna([](int x) { std::cout << "Xabar qabul qilindi: " << x << std::endl; });
    bus.tarqat(2026);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Asinxron tizimlarda modullar o'rtasida xavfsiz ma'lumot almashinuvi.

## Ishlash natijasi:
```text
Xabar qabul qilindi: 2026
```

---

# 797-Topshiriq: Oqimlar xavfsiz LRU Kesh skeleti

## Topshiriq sharti:
Mutex bilan himoyalangan tezkor kesh sinfi.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <unordered_map>
#include <mutex>

class XavfsizKesh {
    std::unordered_map<std::string, std::string> data;
    std::mutex m;
public:
    void saqla(std::string k, std::string v) {
        std::lock_guard<std::mutex> lock(m);
        data[k] = v;
    }
    std::string oqi(std::string k) {
        std::lock_guard<std::mutex> lock(m);
        return data.contains(k) ? data[k] : "";
    }
};

int main() {
    XavfsizKesh k;
    k.saqla("token", "xyz123");
    std::cout << "Keshdan: " << k.oqi("token") << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ko'p oqimli veb-serverlar va AI token keshlarining asosi.

## Ishlash natijasi:
```text
Keshdan: xyz123
```

---

# 798-Topshiriq: Oqimlar to'plami bilan parallel for_each simulyatsiyasi

## Topshiriq sharti:
Vektor elementlarini mavjud yadrolar bo'yicha teng bo'lib oqimlarda parallel qayta ishlash.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <thread>

int main() {
    std::vector<int> v = {1, 2, 3, 4, 5, 6};
    auto worker = [&](size_t start, size_t end) {
        for (size_t i = start; i < end; ++i) v[i] *= 10;
    };
    std::thread t1(worker, 0, 3);
    std::thread t2(worker, 3, 6);
    t1.join(); t2.join();
    for (int x : v) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Katta massivlar ustida parallel hisoblashning eng oddiy va samarali namunasi.

## Ishlash natijasi:
```text
10 20 30 40 50 60 
```

---

# 799-Topshiriq: Ko'p oqimli hisoblashda CPU yuklamasini o'lchash

## Topshiriq sharti:
Hisoblash davomiyligini `std::chrono::high_resolution_clock` bilan aniq o'lchang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <chrono>
#include <thread>

int main() {
    auto bosh = std::chrono::high_resolution_clock::now();
    std::this_thread::sleep_for(std::chrono::milliseconds(20));
    auto tugadi = std::chrono::high_resolution_clock::now();
    auto davomiylik = std::chrono::duration_cast<std::chrono::milliseconds>(tugadi - bosh).count();
    std::cout << "Vaqt sarfi: " << davomiylik << " ms" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Benchmarking va parallel tizimlar unumdorligini tahlil qilish vositasi.

## Ishlash natijasi:
```text
Vaqt sarfi: ... ms
```

---

# 800-Topshiriq: 16-qism xulosasi: Ko'p Oqimlilik va Yuqori Unumdor Tizimlar

## Topshiriq sharti:
Zamonaviy C++ ko'p oqimlilik, Lock-free arxitektura va C++20 atomik primitives vositalari orqali zamonaviy AI dvigatellari va yuqori chastotali dasturlarning asosiy motoridir.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "Ko'p oqimlilik to'liq o'zlashtirildi: C++ barcha protsessor yadrolarining 100% kuchidan foydalanadi!" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Parallel dasturlash kelajak AI tizimlarining yuragidir.

## Ishlash natijasi:
```text
Ko'p oqimlilik to'liq o'zlashtirildi: C++ barcha protsessor yadrolarining 100% kuchidan foydalanadi!
```

---

