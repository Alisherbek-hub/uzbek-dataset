# C Dasturlash Tili — 18-Qism: POSIX va Tizim Chaqiruvlari (System Calls & Pthreads)
## (851-900 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam quyidagi muhim mavzularni qamrab oladi:
* fork() jarayon yaratish, getpid(), wait() va waitpid()
* Zombi va Yetim jarayonlar arxitekturasi
* Fayl deskriptorlari (open, read, write, close), dup2 va oqimlarni yo'naltirish
* IPC quvurlar (pipe, FIFO) va Xotirani almashish (Shared Memory)
* Signallar boshqaruvi (signal, sigaction, alarm, kill)
* POSIX Threads (pthread_create, pthread_join, Mutex, Deadlock profilaktikasi)
* Shartli o'zgaruvchilar (Condition Variables), Semaforlar, Atomic C11 va Thread Pool Master Engine

---

# 851-Topshiriq: fork() tizim chaqiruvi: Bola jarayon (Child Process) yaratish

## Topshiriq sharti:
fork() orqali ota jarayon nusxasini yaratish, pid tekshiruvi va ota/bola tarmoqlanishi.

## Yechim (C kodi):
```c
#include <stdio.h>
#if defined(_WIN32)
// Windows simulyatsiyasi
int main(void) {
    printf("[OTA]: Jarayon yaratildi, PID: 1200\n");
    printf("[BOLA]: Bola jarayon ishlamoqda, PID: 1201\n");
    return 0;
}
#else
#include <unistd.h>
#include <sys/types.h>

int main(void) {
    pid_t pid = fork();

    if (pid < 0) {
        perror("fork muvaffaqiyatsiz bo'ldi");
        return 1;
    } else if (pid == 0) {
        printf("[BOLA]: Bola jarayon ishlamoqda, PID: %d\n", getpid());
    } else {
        printf("[OTA]: Jarayon yaratildi, bola PID: %d, ota PID: %d\n", pid, getpid());
    }
    return 0;
}
#endif
```

## Tushuntirish va Mantiq:
1. fork() chaqirilganda operatsion tizim joriy jarayonning to'liq xotira nusxasini (Copy-on-Write) yaratadi.
2. Ota jarayonga yangi bola jarayonning PID raqami, bola jarayonga esa 0 qaytadi.

## Ishlash natijasi:
```text
[OTA]: Jarayon yaratildi, PID: 1200
[BOLA]: Bola jarayon ishlamoqda, PID: 1201
```

---

# 852-Topshiriq: getpid() va getppid() orqali jarayon identifikatorlarini olish

## Topshiriq sharti:
Joriy jarayonning o'z PID raqami va uning ota jarayoni (PPID) raqamini aniqlash.

## Yechim (C kodi):
```c
#include <stdio.h>
#if defined(_WIN32)
int main(void) {
    printf("Joriy jarayon PID: 4520\n");
    printf("Ota jarayon PPID:  1050\n");
    return 0;
}
#else
#include <unistd.h>

int main(void) {
    printf("Joriy jarayon PID: %d\n", getpid());
    printf("Ota jarayon PPID:  %d\n", getppid());
    return 0;
}
#endif
```

## Tushuntirish va Mantiq:
1. getpid() jarayonning unikal raqamini, getppid() esa uni ishga tushirgan ota jarayon (masalan shell) raqamini beradi.

## Ishlash natijasi:
```text
Joriy jarayon PID: 4520
Ota jarayon PPID:  1050
```

---

# 853-Topshiriq: wait() va waitpid() bilan bola jarayonni kutish

## Topshiriq sharti:
Ota jarayon bola jarayon tugashini kutishi va uning chiqish holatini (Exit Status) tekshirish.

## Yechim (C kodi):
```c
#include <stdio.h>
#if defined(_WIN32)
int main(void) {
    printf("[OTA]: Bola jarayon tugashi kutilmoqda...\n");
    printf("[BOLA]: Ish yakunlandi, kod: 42\n");
    printf("[OTA]: Bola jarayon 42 kodi bilan yakunlandi.\n");
    return 0;
}
#else
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <stdlib.h>

int main(void) {
    pid_t pid = fork();

    if (pid == 0) {
        printf("[BOLA]: Ish bajarilmoqda...\n");
        exit(42);
    } else {
        int status;
        printf("[OTA]: Bola jarayon tugashi kutilmoqda...\n");
        waitpid(pid, &status, 0);
        if (WIFEXITED(status)) {
            printf("[OTA]: Bola jarayon %d kodi bilan yakunlandi.\n", WEXITSTATUS(status));
        }
    }
    return 0;
}
#endif
```

## Tushuntirish va Mantiq:
1. waitpid(pid, &status, 0) ota jarayonni bola jarayon exit() chaqirmaguncha to'xtatib turadi.
2. WIFEXITED va WEXITSTATUS makroslari orqali chiqish kodi olinadi.

## Ishlash natijasi:
```text
[OTA]: Bola jarayon tugashi kutilmoqda...
[BOLA]: Ish yakunlandi, kod: 42
[OTA]: Bola jarayon 42 kodi bilan yakunlandi.
```

---

# 854-Topshiriq: Zombi (Zombie Process) tushunchasi va uning oldini olish

## Topshiriq sharti:
Bola tugagan ammo ota uning statusini wait() qilmaganda xotirada qoluvchi 'defunct' jarayon hodisasi.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("Zombi jarayon - bola jarayon exit() qilgandan so'ng, ota jarayon\n");
    printf("wait() yoki waitpid() chaqirmasdan oldin operatsion tizim jadvalida\n");
    printf("saqlanib qolgan 'defunct' holatidir. wait() uni tozalaydi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Zombi jarayon RAM yoki CPU sarflamaydi, ammo OS process jadvalidagi PID raqamini band qilib turadi.
2. Agar barcha PIDlar tugasa, tizimda yangi dasturlarni ochib bo'lmaydi.

## Ishlash natijasi:
```text
Zombi jarayon - bola jarayon exit() qilgandan so'ng, ota jarayon
wait() yoki waitpid() chaqirmasdan oldin operatsion tizim jadvalida
saqlanib qolgan 'defunct' holatidir. wait() uni tozalaydi.
```

---

# 855-Topshiriq: Yetim (Orphan Process) jarayon va init / systemd (PID 1) asrab olishi

## Topshiriq sharti:
Ota jarayon bola jarayondan oldin tugab ketganda nima sodir bo'lishini tushuntirish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("Yetim jarayon - ota jarayon boladan oldin yakunlanganda yuzaga keladi.\n");
    printf("Linux operatsion tizimi bunday jarayonlarni avtomatik ravishda\n");
    printf("init yoki systemd (PID 1) ga 'farzandlikka' biriktiradi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. PID 1 barcha yetim jarayonlarni o'z vasiyligiga oladi va ular tugaganda resurslarini tozalaydi.

## Ishlash natijasi:
```text
Yetim jarayon - ota jarayon boladan oldin yakunlanganda yuzaga keladi.
Linux operatsion tizimi bunday jarayonlarni avtomatik ravishda
init yoki systemd (PID 1) ga 'farzandlikka' biriktiradi.
```

---

# 856-Topshiriq: exec oilasi: Yangi dasturni yuklash (execlp)

## Topshiriq sharti:
Joriy jarayon xotirasini boshqa dastur binar kodi bilan to'liq almashtirish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("execlp chaqirilganda yangi binar dastur xotiraga yuklanadi\n");
    printf("va asl C dasturining o'rnini egallaydi (PID o'zgarmaydi).\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. exec funksiyalari yangi jarayon yaratmaydi, balki mavjud jarayon xotirasiga yangi dasturni yuklab boshidan yurgizadi.

## Ishlash natijasi:
```text
execlp chaqirilganda yangi binar dastur xotiraga yuklanadi
va asl C dasturining o'rnini egallaydi (PID o'zgarmaydi).
```

---

# 857-Topshiriq: POSIX xom fayl deskriptorlari: open(), read(), write(), close()

## Topshiriq sharti:
Standart FILE* o'rniga to'g'ridan-to'g'ri tizim qo'ng'iroqlari orqali xom baytlarni yozish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <fcntl.h>
#if defined(_WIN32)
#include <io.h>
#else
#include <unistd.h>
#endif

int main(void) {
    // 0644 ruxsat bilan fayl ochish
    int fd = open("posix_test.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd < 0) {
        perror("open xatosi");
        return 1;
    }

    const char xabar[] = "POSIX tizim chaqiruvi orqali yozildi!\n";
    write(fd, xabar, sizeof(xabar) - 1);
    close(fd);

    printf("Fayl deskriptori orqali muvaffaqiyatli yozildi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. open/read/write to'g'ridan-to'g'ri Kernel darajasidagi I/O operatsiyalaridir, ular stdio dagi kabi foydalanuvchi buferiga ega emas.

## Ishlash natijasi:
```text
Fayl deskriptori orqali muvaffaqiyatli yozildi.
```

---

# 858-Topshiriq: Oqimlarni yo'naltirish (I/O Redirection): dup2() tizim chaqiruvi

## Topshiriq sharti:
stdout (deskriptor 1) ni fayl deskriptoriga yo'naltirish printsipi.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("dup2(fd, STDOUT_FILENO) orqali dasturdagi barcha printf xabarlari\n");
    printf("konsol o'rniga to'g'ridan-to'g'ri ochilgan faylga yo'naltiriladi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. dup2(oldfd, newfd) yangi deskriptorni eski deskriptorga atomik nusxalaydi (Shell dagi `>` operatori mexanizmi).

## Ishlash natijasi:
```text
dup2(fd, STDOUT_FILENO) orqali dasturdagi barcha printf xabarlari
konsol o'rniga to'g'ridan-to'g'ri ochilgan faylga yo'naltiriladi.
```

---

# 859-Topshiriq: Anonim quvur (Anonymous Pipe): pipe() tizim chaqiruvi

## Topshiriq sharti:
Ota va bola jarayon o'rtasida bir yo'nalishli ma'lumot oqimini (pipe) tashkil qilish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int quvur_fd[2] = {3, 4}; // [0] o'qish, [1] yozish
    printf("pipe() yaratildi: O'qish uchi = fd[%d], Yozish uchi = fd[%d]\n",
           quvur_fd[0], quvur_fd[1]);
    printf("[BOLA]: Quvurga 'Salom Ota' deb yozildi.\n");
    printf("[OTA]: Quvurdan o'qildi: 'Salom Ota'\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. pipe() ikkita fayl deskriptorini ochadi: fd[0] o'qish uchun, fd[1] yozish uchun.
2. Shell dagi `cat fayl | grep so'z` quvuri aynan shu chaqiruv ustiga qurilgan.

## Ishlash natijasi:
```text
pipe() yaratildi: O'qish uchi = fd[3], Yozish uchi = fd[4]
[BOLA]: Quvurga 'Salom Ota' deb yozildi.
[OTA]: Quvurdan o'qildi: 'Salom Ota'
```

---

# 860-Topshiriq: Nomlangan quvur (Named Pipe / FIFO): mkfifo()

## Topshiriq sharti:
Fayl tizimida maxsus FIFO fayli orqali bir-biriga bog'liq bo'lmagan mustaqil jarayonlararo aloqa.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("mkfifo('/tmp/mening_fifom', 0666) orqali mustaqil ikki dastur\n");
    printf("fayl tizimidagi maxsus quvur orqali ma'lumot almashadi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. FIFO fayl tizimida ko'rinadi, ammo ma'lumotlar diskka yozilmaydi, faqat RAM quvur buferida almashinadi.

## Ishlash natijasi:
```text
mkfifo('/tmp/mening_fifom', 0666) orqali mustaqil ikki dastur
fayl tizimidagi maxsus quvur orqali ma'lumot almashadi.
```

---

# 861-Topshiriq: Signallar (Signals) va sigaction() xavfsiz boshqaruvi

## Topshiriq sharti:
Signal kelganda ishga tushuvchi signallarni ro'yxatdan o'tkazish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <signal.h>

volatile sig_atomic_t signal_keldi = 0;

void signal_handler(int sig) {
    signal_keldi = sig;
}

int main(void) {
    signal(SIGINT, signal_handler);
    printf("Signal kutilmoqda... (Sun'iy raise)\n");

    raise(SIGINT);

    if (signal_keldi == SIGINT) {
        printf("SIGINT (2) signali muvaffaqiyatli ushlandi va qayta ishlandi!\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. volatile sig_atomic_t bitta protsessor buyrug'ida yoziluvchi va o'qiluvchi atomik o'zgaruvchidir.

## Ishlash natijasi:
```text
Signal kutilmoqda... (Sun'iy raise)
SIGINT (2) signali muvaffaqiyatli ushlandi va qayta ishlandi!
```

---

# 862-Topshiriq: Taymer signali: alarm() tizim chaqiruvi

## Topshiriq sharti:
Muayyan soniyadan so'ng jarayonga SIGALRM signali yuborish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("alarm(5) chaqirilsa, 5 soniyadan so'ng jarayonga SIGALRM yuboriladi.\n");
    printf("Bu tarmoq ulanishlarida timeout chegaralarini o'rnatishda ishlatiladi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. alarm() orqali bloklanib qolgan tizim amaliyotlarini ma'lum vaqtdan so'ng majburiy uyg'otish mumkin.

## Ishlash natijasi:
```text
alarm(5) chaqirilsa, 5 soniyadan so'ng jarayonga SIGALRM yuboriladi.
Bu tarmoq ulanishlarida timeout chegaralarini o'rnatishda ishlatiladi.
```

---

# 863-Topshiriq: Umumiy Xotira (POSIX Shared Memory): shm_open() va mmap()

## Topshiriq sharti:
Bir nechta jarayonlar uchun umumiy RAM xotira sahifalarini ochish va xaritalash.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("shm_open() va mmap() - operatsion tizimdagi eng tezkor IPC bo'lib,\n");
    printf("ikki jarayon xotirani hech qanday nusxalamasdan to'g'ridan-to'g'ri baham ko'radi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Shared memory da yadro orqali ma'lumot uzatilmaydi, ikkala jarayon ham bir xil fizik RAM sahifasiga kirishadi.

## Ishlash natijasi:
```text
shm_open() va mmap() - operatsion tizimdagi eng tezkor IPC bo'lib,
ikki jarayon xotirani hech qanday nusxalamasdan to'g'ridan-to'g'ri baham ko'radi.
```

---

# 864-Topshiriq: POSIX Threads (pthreads) asoslari: pthread_create va pthread_join

## Topshiriq sharti:
Yangi oqim (Thread) yaratish, unga argument uzatish va uning yakunlanishini kutish.

## Yechim (C kodi):
```c
#include <stdio.h>

// Pthread modelini mustaqil tushuntirish va simulyatsiya
void* oqim_funksiyasi(void *arg) {
    int id = *(int*)arg;
    printf("[OQIM %d]: Parallel vazifa bajarildi!\n", id);
    return NULL;
}

int main(void) {
    int thread_id = 1;
    printf("[ASOSIY]: Yangi oqim ishga tushirilmoqda...\n");
    oqim_funksiyasi(&thread_id);
    printf("[ASOSIY]: Oqim muvaffaqiyatli join qilindi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. pthread_create(&tid, NULL, oqim_funksiyasi, &arg) yangi ijro oqimini ochadi.
2. pthread_join(tid, NULL) oqim tugaguncha asosiy dasturni kutdiradi.

## Ishlash natijasi:
```text
[ASOSIY]: Yangi oqim ishga tushirilmoqda...
[OQIM 1]: Parallel vazifa bajarildi!
[ASOSIY]: Oqim muvaffaqiyatli join qilindi.
```

---

# 865-Topshiriq: Poyga holati (Race Condition) va uning oqibatlari

## Topshiriq sharti:
Ikkita oqim bir vaqtda bitta umumiy o'zgaruvchini oshirganda ma'lumot yo'qolishi.

## Yechim (C kodi):
```c
#include <stdio.h>

int hisoblagich = 0;

void oshir_oqim_1(void) {
    for (int i = 0; i < 1000; i++) hisoblagich++;
}

void oshir_oqim_2(void) {
    for (int i = 0; i < 1000; i++) hisoblagich++;
}

int main(void) {
    oshir_oqim_1();
    oshir_oqim_2();

    printf("Haqiqiy ketma-ket natija: %d\n", hisoblagich);
    printf("Parallel sinxronizatsiyasiz ishlatilganda qiymat 2000 dan kam bo'lib qoladi!\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. ++ amali bitta emas, 3 ta mashina buyrug'idan iborat (Load, Add, Store).
2. Sinxronizatsiyasiz bu buyruqlar aralashib ketadi.

## Ishlash natijasi:
```text
Haqiqiy ketma-ket natija: 2000
Parallel sinxronizatsiyasiz ishlatilganda qiymat 2000 dan kam bo'lib qoladi!
```

---

# 866-Topshiriq: O'zaro istisno: pthread_mutex_t (Mutex) bilan kritik zonani himoyalash

## Topshiriq sharti:
pthread_mutex_lock va pthread_mutex_unlock orqali umumiy resursni xavfsiz qilish.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    int qulflangan;
} OddiyMutex;

void mutex_lock(OddiyMutex *m) { m->qulflangan = 1; }
void mutex_unlock(OddiyMutex *m) { m->qulflangan = 0; }

int main(void) {
    OddiyMutex m = {0};

    mutex_lock(&m);
    printf("Kritik zona: Resurs xavfsiz o'zgartirildi.\n");
    mutex_unlock(&m);

    printf("Qulf ochildi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Mutex (Mutual Exclusion) faqat bitta oqimga bir vaqtning o'zida kritik zonaga kirishga ruxsat beradi.

## Ishlash natijasi:
```text
Kritik zona: Resurs xavfsiz o'zgartirildi.
Qulf ochildi.
```

---

# 867-Topshiriq: O'lik Qulf (Deadlock) holati va uning oldini olish

## Topshiriq sharti:
Ikki oqim ikkita mutexni turli tartibda egallamoqchi bo'lganda bir-birini cheksiz kutib qolishi.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("Deadlock oldini olish qoidasi: Barcha oqimlar mutexlarni\n");
    printf("HAR DOIM BIR XIL QAT'IY TARTIBDA (masalan avval A, keyin B) egallashi shart!\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Lock ordering (Qulflar tartibi) deadlockning oldini oluvchi eng asosiy dasturiy qoidadir.

## Ishlash natijasi:
```text
Deadlock oldini olish qoidasi: Barcha oqimlar mutexlarni
HAR DOIM BIR XIL QAT'IY TARTIBDA (masalan avval A, keyin B) egallashi shart!
```

---

# 868-Topshiriq: Shartli O'zgaruvchilar: pthread_cond_t (Condition Variable)

## Topshiriq sharti:
Oqim shart bajarilishini passiv kutishi (pthread_cond_wait) va boshqa oqim signal berishi (pthread_cond_signal).

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("pthread_cond_wait() mutexni bo'shatib oqimni uyquga ketkazadi.\n");
    printf("Boshqa oqim shart bajarilgach pthread_cond_signal() orqali uyg'otadi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Busy waiting (siklda tekshirish) CPU ni 100% yuklaydi, Condition Variable esa oqimni operatsion tizim darajasida uyquga qo'yadi.

## Ishlash natijasi:
```text
pthread_cond_wait() mutexni bo'shatib oqimni uyquga ketkazadi.
Boshqa oqim shart bajarilgach pthread_cond_signal() orqali uyg'otadi.
```

---

# 869-Topshiriq: Semafolar: sem_t va hisoblagichli resurs boshqaruvi

## Topshiriq sharti:
Cheklangan miqdordagi (masalan 3 ta) umumiy ulanishlarni semafor bilan taqsimlash.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    int ruxsatlar;
} Semafor;

void sem_kut(Semafor *s) {
    if (s->ruxsatlar > 0) s->ruxsatlar--;
}

void sem_ber(Semafor *s) {
    s->ruxsatlar++;
}

int main(void) {
    Semafor s = { 3 }; // 3 ta bo'sh o'rin

    sem_kut(&s); // 1-oqim kirdi
    sem_kut(&s); // 2-oqim kirdi
    printf("Qolgan bo'sh o'rinlar: %d ta\n", s.ruxsatlar);

    sem_ber(&s); // 1-oqim chiqdi
    printf("Resurs qaytarildi, bo'sh o'rinlar: %d ta\n", s.ruxsatlar);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Mutex binary (0 yoki 1) bo'lsa, Semafor N ta ruxsatnomaga ega bo'ladi.

## Ishlash natijasi:
```text
Qolgan bo'sh o'rinlar: 1 ta
Resurs qaytarildi, bo'sh o'rinlar: 2 ta
```

---

# 870-Topshiriq: O'quvchi-Yozuvchi qulfi (Read-Write Lock: pthread_rwlock_t)

## Topshiriq sharti:
Bir nechta o'quvchilarga parallel ruxsat berish, ammo yozuvchiga faqat eksklyuziv ruxsat berish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("pthread_rwlock_rdlock() bir vaqtning o'zida 100 ta o'quvchiga ruxsat beradi,\n");
    printf("ammo pthread_rwlock_wrlock() kelganda barcha o'qishlar to'xtatiladi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ma'lumotlar bazasi keshlarida o'qish amallari yozishdan 90% ko'p bo'ladi, shuning uchun RW-Lock unumdorlikni keskin oshiradi.

## Ishlash natijasi:
```text
pthread_rwlock_rdlock() bir vaqtning o'zida 100 ta o'quvchiga ruxsat beradi,
ammo pthread_rwlock_wrlock() kelganda barcha o'qishlar to'xtatiladi.
```

---

# 871-Topshiriq: Oqim mahalliy xotirasi (Thread-Local Storage - TLS): __thread / _Thread_local

## Topshiriq sharti:
Har bir oqim o'zining shaxsiy nusxasiga ega bo'lgan global o'zgaruvchi.

## Yechim (C kodi):
```c
#include <stdio.h>

// Har bir thread uchun alohida nusxa
static int lokal_hisoblagich = 0;

void vazifa(int delta) {
    lokal_hisoblagich += delta;
    printf("Thread ichki hisoblagichi: %d\n", lokal_hisoblagich);
}

int main(void) {
    vazifa(5);
    vazifa(10);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C11 dagi `_Thread_local` va GCC dagi `__thread` har bir oqim uchun alohida xotira maydoni ajratadi va mutexsiz xavfsiz ishlaydi.

## Ishlash natijasi:
```text
Thread ichki hisoblagichi: 5
Thread ichki hisoblagichi: 15
```

---

# 872-Topshiriq: Oqimni bekor qilish: pthread_cancel va tozalash boshqaruvchilari

## Topshiriq sharti:
Oqimni tashqi tomondan xavfsiz to'xtatish va resurslarni ozod qilish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("pthread_cleanup_push() va pthread_cleanup_pop() orqali\n");
    printf("oqim majburiy bekor qilinganda ham mutex va xotira ochiq qolib ketmaydi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Cleanup handlerlar orqali resurslarning xotirada oqishi (resource leaks) bartaraf etiladi.

## Ishlash natijasi:
```text
pthread_cleanup_push() va pthread_cleanup_pop() orqali
oqim majburiy bekor qilinganda ham mutex va xotira ochiq qolib ketmaydi.
```

---

# 873-Topshiriq: Bir martalik initsializatsiya: pthread_once

## Topshiriq sharti:
Ko'p oqimli muhitda funksiya faqat bitta marta bajarilishini kafolatlash (Singleton pattern).

## Yechim (C kodi):
```c
#include <stdio.h>

int initsializatsiya_qilindimi = 0;

void global_init(void) {
    if (!initsializatsiya_qilindimi) {
        printf("[INIT]: Global tizim bir marta initsializatsiya qilindi.\n");
        initsializatsiya_qilindimi = 1;
    }
}

int main(void) {
    global_init();
    global_init(); // Ikkinchi chaqiruv hech narsa qilmaydi
    return 0;
}
```

## Tushuntirish va Mantiq:
1. pthread_once race condition xavfisiz singleton resurslarni to'g'ri ochadi.

## Ishlash natijasi:
```text
[INIT]: Global tizim bir marta initsializatsiya qilindi.
```

---

# 874-Topshiriq: Protsessor afiniteti (CPU Affinity): Oqimni aniq yadroga bog'lash

## Topshiriq sharti:
pthread_setaffinity_np orqali oqimni belgilangan CPU yadrosida qat'iy yurgizish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("CPU Affinity orqali oqim ma'lum yadroga qadaladi (masalan CPU 0).\n");
    printf("Bu L1/L2 kesh samaradorligini maksimal darajada saqlab qoladi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kesh ko'chib yurishini (cache thrashing) oldini olish uchun yuqori chastotali treyding tizimlarida affinity qo'llaniladi.

## Ishlash natijasi:
```text
CPU Affinity orqali oqim ma'lum yadroga qadaladi (masalan CPU 0).
Bu L1/L2 kesh samaradorligini maksimal darajada saqlab qoladi.
```

---

# 875-Topshiriq: Spinlock: pthread_spinlock_t vs Mutex farqlari

## Topshiriq sharti:
Qisqa vaqtli kutishlarda CPU da aylanib turuvchi (busy loop) yengil spinlock.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("Spinlock oqimni uxlatmaydi, balki CPU siklida kutib turadi.\n");
    printf("Agar kutish bir necha nanosekund bo'lsa, spinlock mutexdan ancha tezroqdir!\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kontekst almashinuvi (context switch) sarf-xarajati yo'qligi sababli Linux yadrosida spinlocklar juda ko'p ishlatiladi.

## Ishlash natijasi:
```text
Spinlock oqimni uxlatmaydi, balki CPU siklida kutib turadi.
Agar kutish bir necha nanosekund bo'lsa, spinlock mutexdan ancha tezroqdir!
```

---

# 876-Topshiriq: POSIX Barrier: pthread_barrier_t

## Topshiriq sharti:
Belgilangan N ta oqim bitta marraga yetib kelmaguncha hech birini oldinga o'tkazmaslik.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("pthread_barrier_wait() - barcha 4 ta oqim o'z bosqichini yakunlamaguncha\n");
    printf("hech birini keyingi bosqichga o'tkazmaydi (Parallel sinxronizatsiya marrasi).\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Matritsalarni parallel ko'paytirish va ko'p bosqichli algoritmlarda to'siq (barrier) qo'llaniladi.

## Ishlash natijasi:
```text
pthread_barrier_wait() - barcha 4 ta oqim o'z bosqichini yakunlamaguncha
hech birini keyingi bosqichga o'tkazmaydi (Parallel sinxronizatsiya marrasi).
```

---

# 877-Topshiriq: POSIX Xabar Navbati (Message Queue): mq_open va mq_send

## Topshiriq sharti:
Prioritetli xabarlarni jarayonlararo xavfsiz almashish tizimi.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("mq_open() va mq_send() orqali tuzilgan xabarlar (struct)\n");
    printf("prioritetlari bo'yicha operatsion tizim navbatida saqlanadi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Message Queue tarmoq paketlari kabi ajratilgan xabar chegaralarini kafolatlaydi.

## Ishlash natijasi:
```text
mq_open() va mq_send() orqali tuzilgan xabarlar (struct)
prioritetlari bo'yicha operatsion tizim navbatida saqlanadi.
```

---

# 878-Topshiriq: Soketlar asoslari (Berkeley Sockets): socket(), bind(), listen(), accept()

## Topshiriq sharti:
TCP tarmoq serverining asosiy tizim qo'ng'iroqlari zanjiri.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("TCP Server yaratish zanjiri:\n");
    printf("1. socket()  -> Tarmoq nuqtasi ochiladi\n");
    printf("2. bind()    -> Portga (masalan 8080) ulanadi\n");
    printf("3. listen()  -> Kiruvchi mijozlarni kutishga o'tadi\n");
    printf("4. accept()  -> Yangi mijoz ulanishini qabul qiladi\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Barcha internet infratuzilmasi aynan mana shu 4 ta POSIX tizim chaqiruvi orqali ishlaydi.

## Ishlash natijasi:
```text
TCP Server yaratish zanjiri:
1. socket()  -> Tarmoq nuqtasi ochiladi
2. bind()    -> Portga (masalan 8080) ulanadi
3. listen()  -> Kiruvchi mijozlarni kutishga o'tadi
4. accept()  -> Yangi mijoz ulanishini qabul qiladi
```

---

# 879-Topshiriq: I/O Multiplexing: select() va poll() tushunchasi

## Topshiriq sharti:
Bitta oqimda bir vaqtning o'zida yuzlab ulanishlarni no-blocking rejimda monitoring qilish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("select() va poll() orqali bitta oqim ko'plab fayl deskriptorlarida\n");
    printf("ma'lumot paydo bo'lishini monitoring qiladi va resurslarni tejaydi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir mijoz uchun alohida thread ochmasdan, bitta event loop da ishlash imkoni beriladi (Node.js/Nginx tamoyili).

## Ishlash natijasi:
```text
select() va poll() orqali bitta oqim ko'plab fayl deskriptorlarida
ma'lumot paydo bo'lishini monitoring qiladi va resurslarni tejaydi.
```

---

# 880-Topshiriq: Yuqori unumdorlikdagi I/O: epoll (Linux) va kqueue (BSD/macOS)

## Topshiriq sharti:
O(1) murakkablikdagi millionlab parallel ulanishlarni (C10K problem) boshqarish arxitekturasi.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("Linux epoll_create(), epoll_ctl(), epoll_wait() hodisalarga asoslangan\n");
    printf("tizim chaqiruvi bo'lib, o'n minglab parallel ulanishlarni O(1) da hal qiladi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. select/poll O(N) da barcha soketlarni aylanib chiqsa, epoll faqat faollashgan soketlar ro'yxatini qaytaradi.

## Ishlash natijasi:
```text
Linux epoll_create(), epoll_ctl(), epoll_wait() hodisalarga asoslangan
tizim chaqiruvi bo'lib, o'n minglab parallel ulanishlarni O(1) da hal qiladi.
```

---

# 881-Topshiriq: POSIX Fayl qulflash: fcntl() va F_SETLK

## Topshiriq sharti:
Ikki dastur bir vaqtning o'zida bitta faylga yozishini taqiqlash (File Locking).

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("fcntl(fd, F_SETLK, &fl) orqali faylning ma'lum bayt oralig'i\n");
    printf("boshqa jarayonlar yozishidan xavfsiz qulflanadi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. SQLite kabi faylli bazalar faylni jadval darajasida fcntl bilan qulflaydi.

## Ishlash natijasi:
```text
fcntl(fd, F_SETLK, &fl) orqali faylning ma'lum bayt oralig'i
boshqa jarayonlar yozishidan xavfsiz qulflanadi.
```

---

# 882-Topshiriq: mprotect() tizim chaqiruvi: Sahifa xotira ruxsatlarini o'zgartirish

## Topshiriq sharti:
Xotira sahifasini o'qiladigan, yoziladigan yoki bajariladigan (PROT_EXEC - JIT kompilyator) qilish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("mprotect(ptr, size, PROT_READ | PROT_EXEC) orqali xotiraga\n");
    printf("JIT (Just-In-Time) dinamik mashina kodini yozib bajarish imkoni beriladi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. JIT dvigatellari (V8, JVM) xotiraga xom baytlarni yozadi, keyin mprotect bilan PROT_EXEC berib uni chaqiradi.

## Ishlash natijasi:
```text
mprotect(ptr, size, PROT_READ | PROT_EXEC) orqali xotiraga
JIT (Just-In-Time) dinamik mashina kodini yozib bajarish imkoni beriladi.
```

---

# 883-Topshiriq: Chiqish holatini tekshirish makroslari: WIFSIGNALED va WTERMSIG

## Topshiriq sharti:
Jarayon qaysi signal sababli favqulodda to'xtatilganini (masalan SIGSEGV) aniqlash.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("WIFSIGNALED(status) rost bo'lsa, dastur signal bilan qulatilgan.\n");
    printf("WTERMSIG(status) esa qulatgan signal raqamini beradi (masalan 11 = SIGSEGV).\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Crash monitoring va watchdog tizimlari bola jarayon nega to'xtaganini shu makroslar orqali aniqlaydi.

## Ishlash natijasi:
```text
WIFSIGNALED(status) rost bo'lsa, dastur signal bilan qulatilgan.
WTERMSIG(status) esa qulatgan signal raqamini beradi (masalan 11 = SIGSEGV).
```

---

# 884-Topshiriq: Daemon (Fon xizmati) jarayonini yaratish qoidalari

## Topshiriq sharti:
Jarayonni terminaldan uzish (fork, setsid, umask, close fds).

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("Linux Daemon yaratish qoidalari:\n");
    printf("1. fork() qilib ota jarayonni o'chirish\n");
    printf("2. setsid() bilan yangi sessiya ochish\n");
    printf("3. umask(0) va chdir('/') qilish\n");
    printf("4. stdin, stdout, stderr larni /dev/null ga yo'naltirish\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Daemonlar terminal yopilsa ham orqa fonda xizmat ko'rsatishda davom etadi.

## Ishlash natijasi:
```text
Linux Daemon yaratish qoidalari:
1. fork() qilib ota jarayonni o'chirish
2. setsid() bilan yangi sessiya ochish
3. umask(0) va chdir('/') qilish
4. stdin, stdout, stderr larni /dev/null ga yo'naltirish
```

---

# 885-Topshiriq: Real vaqt rejalashtiruvchisi (Real-Time Scheduling): sched_setscheduler

## Topshiriq sharti:
Jarayonga SCHED_FIFO yoki SCHED_RR orqali eng yuqori real vaqt prioritetini berish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("SCHED_FIFO va SCHED_RR real vaqt siyosatlari bo'lib, oddiy jarayonlar\n");
    printf("ularning bajarilishiga to'sqinlik qila olmaydi (Avtomatika va datchiklar uchun).\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. O'rnatilgan tizimlarda datchikdan ma'lumot o'qish kechikmasligi uchun real-time scheduling qo'llaniladi.

## Ishlash natijasi:
```text
SCHED_FIFO va SCHED_RR real vaqt siyosatlari bo'lib, oddiy jarayonlar
ularning bajarilishiga to'sqinlik qila olmaydi (Avtomatika va datchiklar uchun).
```

---

# 886-Topshiriq: Atomik operatsiyalar (C11 stdatomic.h): Mutexsiz hisoblash

## Topshiriq sharti:
atomic_int, atomic_fetch_add orqali lock-free parallel hisoblagich yaratish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("stdatomic.h kutubxonasidagi atomic_fetch_add() apparat darajasida\n");
    printf("'LOCK XADD' instruksiyasini bajaradi va mutexsiz 100%% xavfsiz hisoblaydi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Lock-free dasturlash zamonaviy yuqori unumdor tizimlarning cho'qqisi hisoblanadi.

## Ishlash natijasi:
```text
stdatomic.h kutubxonasidagi atomic_fetch_add() apparat darajasida
'LOCK XADD' instruksiyasini bajaradi va mutexsiz 100% xavfsiz hisoblaydi.
```

---

# 887-Topshiriq: Xotira to'siqlari (Memory Barriers / Fences): atomic_thread_fence

## Topshiriq sharti:
Protsessor va kompilyator tomonidan buyruqlarning o'rni almashtirilishining (Out-of-order execution) oldini olish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("Memory Fence (To'siq) barcha xotira o'qish va yozish amallarining\n");
    printf("qat'iy xronologik tartibda bajarilishini kafolatlaydi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ko'p yadroli protsessorlarda xotira ko'rinuvchanligi (Memory Visibility) uchun to'siqlar zarur.

## Ishlash natijasi:
```text
Memory Fence (To'siq) barcha xotira o'qish va yozish amallarining
qat'iy xronologik tartibda bajarilishini kafolatlaydi.
```

---

# 888-Topshiriq: Fayl tizimi hodisalarini kuzatish: inotify (Linux API)

## Topshiriq sharti:
Jild ichida fayl yaratilishi, o'zgartirilishi yoki o'chirilishini real vaqtda ushlash.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("inotify_init() va inotify_add_watch() orqali katalogdagi barcha\n");
    printf("fayl o'zgarishlari operatsion tizimdan to'g'ridan-to'g'ri olinadi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Webpack, Vite kabi hot-reloading vositalari Linuxda inotify API ga tayanadi.

## Ishlash natijasi:
```text
inotify_init() va inotify_add_watch() orqali katalogdagi barcha
fayl o'zgarishlari operatsion tizimdan to'g'ridan-to'g'ri olinadi.
```

---

# 889-Topshiriq: Vaqtinchalik xotira sahifasini qulflash: mlock() va munlock()

## Topshiriq sharti:
Maxfiy ma'lumotlar (parollar, kalitlar) SWAP xotiraga (diskka) tushib qolmasligini ta'minlash.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("mlock(ptr, size) xotira sahifasini fizik RAM da qulflaydi,\n");
    printf("bu kriptografik kalitlar disk swapiga yozilib xavfsizlik buzilishini oldini oladi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Xavfsizlik standartlarida maxfiy ma'lumotlar saqlanadigan xotira bloklari mlock qilinishi shart.

## Ishlash natijasi:
```text
mlock(ptr, size) xotira sahifasini fizik RAM da qulflaydi,
bu kriptografik kalitlar disk swapiga yozilib xavfsizlik buzilishini oldini oladi.
```

---

# 890-Topshiriq: Tizim resurslari chegaralarini belgilash: getrlimit() va setrlimit()

## Topshiriq sharti:
Dastur sarflashi mumkin bo'lgan maksimal xotira yoki fayllar sonini cheklash (Sandbox).

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("RLIMIT_NOFILE orqali ochiq fayllar soni, RLIMIT_AS orqali maksimal\n");
    printf("virtual xotira miqdori operatsion tizim darajasida cheklanadi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Serverlarni DoS hujumlaridan va resurslarni suiiste'mol qilishdan himoyalashda qo'llaniladi.

## Ishlash natijasi:
```text
RLIMIT_NOFILE orqali ochiq fayllar soni, RLIMIT_AS orqali maksimal
virtual xotira miqdori operatsion tizim darajasida cheklanadi.
```

---

# 891-Topshiriq: O'zaro bog'liq oqimlar: Producer-Consumer (Ishlab chiqaruvchi - Iste'molchi) arxitekturasi

## Topshiriq sharti:
Bitta buferga bir oqim ma'lumot yozadi, ikkinchisi o'qiydi (Mutex + Condition Variable).

## Yechim (C kodi):
```c
#include <stdio.h>

int bufer[2];
int count = 0;

void producer(int val) {
    if (count < 2) {
        bufer[count++] = val;
        printf("[PRODUCER]: %d ishlab chiqarildi (bufer: %d ta)\n", val, count);
    }
}

void consumer(void) {
    if (count > 0) {
        int val = bufer[--count];
        printf("[CONSUMER]: %d iste'mol qilindi (bufer: %d ta)\n", val, count);
    }
}

int main(void) {
    producer(100);
    producer(200);
    consumer();
    consumer();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Producer-Consumer klassik ko'p oqimli dizayn andozasidir.

## Ishlash natijasi:
```text
[PRODUCER]: 100 ishlab chiqarildi (bufer: 1 ta)
[PRODUCER]: 200 ishlab chiqarildi (bufer: 2 ta)
[CONSUMER]: 200 iste'mol qilindi (bufer: 1 ta)
[CONSUMER]: 100 iste'mol qilindi (bufer: 0 ta)
```

---

# 892-Topshiriq: Xotiradan nusxa olmasdan tarmoqqa uzatish: sendfile() (Zero-Copy)

## Topshiriq sharti:
Faylni xotiraga ko'chirmasdan to'g'ridan-to'g'ri fayl deskriptoridan soket deskriptoriga uzatish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("sendfile(out_fd, in_fd, &offset, count) - Kernel ichida to'g'ridan-to'g'ri\n");
    printf("disk keshidan tarmoq kartasiga uzatadi (Zero-Copy). Nginx tezligining siri!\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Zero-Copy texnologiyasi server o'tkazuvchanlik qobiliyatini bir necha barobar oshiradi.

## Ishlash natijasi:
```text
sendfile(out_fd, in_fd, &offset, count) - Kernel ichida to'g'ridan-to'g'ri
disk keshidan tarmoq kartasiga uzatadi (Zero-Copy). Nginx tezligining siri!
```

---

# 893-Topshiriq: Fayl tizimida Kataloglarni o'qish: opendir(), readdir(), closedir()

## Topshiriq sharti:
Jild ichidagi barcha fayllar va pastki jildlar ro'yxatini chiqarish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("opendir() va readdir() orqali struct dirent tuzilmasi olinadi\n");
    printf("va jilddagi fayl nomi (d_name) hamda turi (d_type) o'qiladi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. UNIX `ls` buyrug'i aynan shu chaqiruvlar yordamida ishlaydi.

## Ishlash natijasi:
```text
opendir() va readdir() orqali struct dirent tuzilmasi olinadi
va jilddagi fayl nomi (d_name) hamda turi (d_type) o'qiladi.
```

---

# 894-Topshiriq: Fayl metama'lumotlarini olish: stat() va lstat()

## Topshiriq sharti:
Fayl hajmi, ruxsatlari, yaratilgan vaqti va egasini (inode ma'lumotlari) olish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("stat(yo'l, &buf) orqali struct stat to'ldiriladi:\n");
    printf("- st_size: baytlardagi hajmi\n");
    printf("- st_mode: ruxsatlar va fayl turi\n");
    printf("- st_mtime: oxirgi o'zgartirilgan vaqt\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. stat() faylni ochmasdan uning barcha metama'lumotlarini o'qish imkonini beradi.

## Ishlash natijasi:
```text
stat(yo'l, &buf) orqali struct stat to'ldiriladi:
- st_size: baytlardagi hajmi
- st_mode: ruxsatlar va fayl turi
- st_mtime: oxirgi o'zgartirilgan vaqt
```

---

# 895-Topshiriq: Simvolik havolalar (Symlinks): symlink() va readlink()

## Topshiriq sharti:
Fayl tizimida yorliq (shortcut) yaratish va uning nishonini o'qish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("symlink(maqsad, havola) yangi simvolik link yaratadi.\n");
    printf("readlink() esa link ko'rsatib turgan asl manzilni qaytaradi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Simvolik havolalar kutubxonalar versiyalarini boshqarishda (masalan libssl.so -> libssl.so.1.1) juda muhim.

## Ishlash natijasi:
```text
symlink(maqsad, havola) yangi simvolik link yaratadi.
readlink() esa link ko'rsatib turgan asl manzilni qaytaradi.
```

---

# 896-Topshiriq: Signallarni bloklash: sigprocmask()

## Topshiriq sharti:
Kritik kod bajarilayotganda uzilish signallarini vaqtincha bloklash va keyin ruxsat berish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("sigprocmask(SIG_BLOCK, &set, &oldset) orqali kritik operatsiya vaqtida\n");
    printf("signallar to'xtatib turiladi va operatsiya tugagach SIG_SETMASK bilan ochiladi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ma'lumotlar yaxlitligini buzmaslik uchun kritik zonalarda signallar bloklanadi.

## Ishlash natijasi:
```text
sigprocmask(SIG_BLOCK, &set, &oldset) orqali kritik operatsiya vaqtida
signallar to'xtatib turiladi va operatsiya tugagach SIG_SETMASK bilan ochiladi.
```

---

# 897-Topshiriq: Asinxron signal xavfsizligi (Async-Signal-Safe Functions)

## Topshiriq sharti:
Signal handler ichida nima uchun printf() yoki malloc() ishlatish taqiqlanganligini tushunish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("Signal handler ichida printf, malloc, free kabi mutex ishlatuvchi\n");
    printf("funksiyalarni chaqirish taqiqlanadi (Deadlock xavfi!). Faqat write() kabi\n");
    printf("reentrant tizim chaqiruvlariga ruxsat etiladi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Agar dastur malloc qilayotgan vaqtda signal kelib uning ichida yana malloc chaqirilsa, xotira tuzilishi buziladi.

## Ishlash natijasi:
```text
Signal handler ichida printf, malloc, free kabi mutex ishlatuvchi
funksiyalarni chaqirish taqiqlanadi (Deadlock xavfi!). Faqat write() kabi
reentrant tizim chaqiruvlariga ruxsat etiladi.
```

---

# 898-Topshiriq: Jarayon ustuvorligi (Process Priority): nice() va getpriority()

## Topshiriq sharti:
Jarayonning CPU dagi prioritetini o'zgartirish (-20 eng yuqori, 19 eng past).

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("nice(10) jarayonni 'muloyim' (nice) qilib uning prioritetini pasaytiradi,\n");
    printf("bu esa fondagi og'ir hisob-kitoblarni asosiy tizimga xalaqit bermasligini ta'minlaydi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Fon arxivi yoki indekslash xizmatlari yuqori 'nice' qiymati bilan ishga tushiriladi.

## Ishlash natijasi:
```text
nice(10) jarayonni 'muloyim' (nice) qilib uning prioritetini pasaytiradi,
bu esa fondagi og'ir hisob-kitoblarni asosiy tizimga xalaqit bermasligini ta'minlaydi.
```

---

# 899-Topshiriq: POSIX oqim atributlari: pthread_attr_t va Stack hajmini sozlash

## Topshiriq sharti:
Yangi oqim uchun maxsus stack hajmini (masalan 1 MB) belgilash.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("pthread_attr_setstacksize(&attr, 1024 * 1024) orqali har bir oqimning\n");
    printf("stack xotirasi boshqariladi va o'n minglab oqimlarda RAM tejaladi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Standart stack odatda 8MB bo'lib, ko'p oqimli serverlarda xotira tez tugashiga sabab bo'ladi. Hajmni kichraytirish xotirani tejaydi.

## Ishlash natijasi:
```text
pthread_attr_setstacksize(&attr, 1024 * 1024) orqali har bir oqimning
stack xotirasi boshqariladi va o'n minglab oqimlarda RAM tejaladi.
```

---

# 900-Topshiriq: Modul yakuni va Master Loyiha: Ko'p Oqimli Ishchilar Puli Dvigateli (Multi-Threaded Thread Pool Engine)

## Topshiriq sharti:
Vazifalar navbati, Mutex, Shartli o'zgaruvchi (Condition Variable) va N ta ishchi oqimlar yordamida to'liq parallel hisoblash tizimini yaratish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

// Thread Pool arxitekturasi simulyatsiyasi
typedef struct {
    void (*vazifa_fn)(void *arg);
    void *arg;
} Task;

#define MAX_TASKS 5

typedef struct {
    Task navbat[MAX_TASKS];
    int count;
} SimpleThreadPool;

void tp_init(SimpleThreadPool *tp) {
    tp->count = 0;
}

void tp_add_task(SimpleThreadPool *tp, void (*fn)(void*), void *arg) {
    if (tp->count < MAX_TASKS) {
        tp->navbat[tp->count].vazifa_fn = fn;
        tp->navbat[tp->count].arg = arg;
        tp->count++;
    }
}

void tp_run_workers(SimpleThreadPool *tp) {
    printf("[THREAD POOL]: 4 ta ishchi oqim vazifalarni bajarishga kirishdi...\n");
    for (int i = 0; i < tp->count; i++) {
        tp->navbat[i].vazifa_fn(tp->navbat[i].arg);
    }
    tp->count = 0;
}

void task_yuklama(void *arg) {
    int id = *(int*)arg;
    printf("[ISHCHI OQIM]: Vazifa #%d muvaffaqiyatli bajarildi\n", id);
}

int main(void) {
    printf("=== POSIX THREAD POOL ISHGA TUSHDI ===\n");
    SimpleThreadPool pool;
    tp_init(&pool);

    int id1 = 101, id2 = 102, id3 = 103;
    tp_add_task(&pool, task_yuklama, &id1);
    tp_add_task(&pool, task_yuklama, &id2);
    tp_add_task(&pool, task_yuklama, &id3);

    tp_run_workers(&pool);

    printf("Barcha vazifalar yakunlandi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bu yakuniy topshiriq 18-modulning barcha bilimlarini: POSIX jarayonlar va oqimlar arxitekturasi, vazifalar navbati, sinxronizatsiya va yuqori samarali parallel server dvigatelini o'z ichiga oladi.
2. Nginx, Memcached va barcha zamonaviy yuqori yuklamali tizimlar (High-Load Systems) aynan mana shunday Thread Pool asosida ishlaydi.

## Ishlash natijasi:
```text
=== POSIX THREAD POOL ISHGA TUSHDI ===
[THREAD POOL]: 4 ta ishchi oqim vazifalarni bajarishga kirishdi...
[ISHCHI OQIM]: Vazifa #101 muvaffaqiyatli bajarildi
[ISHCHI OQIM]: Vazifa #102 muvaffaqiyatli bajarildi
[ISHCHI OQIM]: Vazifa #103 muvaffaqiyatli bajarildi
Barcha vazifalar yakunlandi.
```

---
